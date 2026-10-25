// DESK_API's real run on 3321 (masaha_b_dev, the demo data). Prints PASS|FAIL per case and ALL PASS.
// Never prints a secret, a token or a phone. Writes: reception's own session's last_activity_at moved
// back 16 minutes (O3), and one subscription made by reception from the demo space's month price.
import { execFileSync } from 'node:child_process';
import { randomUUID } from 'node:crypto';
import { readFileSync } from 'node:fs';

const API = 'http://localhost:3321/api/v1';
const env = Object.fromEntries(
  readFileSync('C:/dev/masaha/app-b/apps/api/.env', 'utf8')
    .split(/\r?\n/)
    .filter((line) => /^[A-Z_]+=/.test(line))
    .map((line) => [line.slice(0, line.indexOf('=')), line.slice(line.indexOf('=') + 1).replace(/^"|"$/g, '')]),
);
const db = new URL(env.DATABASE_URL);
const PASSWORD = env.SEED_DEMO_PASSWORD;

function sql(query) {
  return execFileSync(
    'docker',
    ['exec', '-e', 'PGPASSWORD', 'masaha-postgres-1', 'psql', '-U', decodeURIComponent(db.username),
      '-d', db.pathname.slice(1), '-tAc', query],
    { env: { ...process.env, PGPASSWORD: decodeURIComponent(db.password) }, encoding: 'utf8' },
  ).trim();
}

let failures = 0;
function check(name, ok, detail) {
  console.log(`${ok ? 'PASS' : 'FAIL'} ${name}${detail ? ` — ${detail}` : ''}`);
  if (!ok) failures += 1;
}

async function call(method, path, { auth, body, cookie, key } = {}) {
  const headers = { 'content-type': 'application/json' };
  if (auth) headers.authorization = `Bearer ${auth}`;
  if (cookie) headers.cookie = cookie;
  if (key) headers['idempotency-key'] = key;
  const response = await fetch(`${API}${path}`, { method, headers, body: body && JSON.stringify(body) });
  const text = await response.text();
  return { status: response.status, body: text ? JSON.parse(text) : null, setCookie: response.headers.getSetCookie() };
}

async function signIn(email) {
  const answer = await call('POST', '/auth/login', { body: { email, password: PASSWORD } });
  if (answer.status !== 200) throw new Error(`sign-in ${email}: ${answer.status}`);
  const token = answer.body.data.accessToken;
  const sid = JSON.parse(Buffer.from(token.split('.')[1], 'base64url').toString()).sid;
  const refresh = answer.setCookie.find((c) => c.startsWith('masaha_refresh=')).split(';')[0];
  return { token, sid, refresh };
}

const db0 = db.pathname.slice(1);
check('database is masaha_b_dev', db0 === 'masaha_b_dev', db0);
const spaceId = Number(sql(`SELECT id FROM spaces WHERE slug = 'masaha-demo'`));
check('demo space found', spaceId > 0, `id ${spaceId}`);

// 1–2. The owner reads a statement and a file: their sums agree with their lists.
const owner = await signIn('demo-owner@example.com');
const subscriptionId = Number(sql(`SELECT s.id FROM subscriptions s WHERE s.space_id = ${spaceId}
  AND EXISTS (SELECT 1 FROM payments p WHERE p.subscription_id = s.id) ORDER BY s.id LIMIT 1`));
check('a demo subscription with payments exists', subscriptionId > 0, `id ${subscriptionId}`);
const statement = await call('GET', `/manage/spaces/${spaceId}/subscriptions/${subscriptionId}`, { auth: owner.token });
const st = statement.body?.data;
const listedPaid = (st?.payments ?? []).filter((p) => p.voided === null).reduce((s, p) => s + p.amountAgorot, 0);
const listedMinutes = (st?.checkIns ?? []).reduce((s, c) => s + (c.minutes ?? 0), 0);
check('1 statement 200, paid = listed payments, minutes = listed check-ins, balance = due − paid',
  statement.status === 200 && st.paidAgorot === listedPaid && st.progress.minutesUsed === listedMinutes &&
  st.balanceAgorot === st.dueAgorot - st.paidAgorot,
  `${statement.status} paid ${st?.paidAgorot}/${listedPaid} minutes ${st?.progress?.minutesUsed}/${listedMinutes}`);
const file = await call('GET', `/manage/spaces/${spaceId}/customers/${st.customerId}`, { auth: owner.token });
const fd = file.body?.data;
const balances = [...(fd?.subscriptions ?? []).map((s) => s.balanceAgorot), ...(fd?.unpaidVisits ?? []).map((v) => v.balanceAgorot ?? 0)];
check('2 file 200, each subscription balance = due − paid, debt = positive balances',
  file.status === 200 && fd.subscriptions.every((s) => s.balanceAgorot === s.dueAgorot - s.paidAgorot) &&
  fd.debtAgorot === balances.filter((b) => b > 0).reduce((s, b) => s + b, 0),
  `${file.status} debt ${fd?.debtAgorot}`);

// 3. Reception idle past 15 minutes, by moving its own session's last use back (the real 15 minutes not waited).
const desk = await signIn('demo-reception@example.com');
const active = await call('GET', '/manage/spaces', { auth: desk.token });
check('3a reception active → 200', active.status === 200, String(active.status));
sql(`UPDATE refresh_tokens SET last_activity_at = now() - interval '16 minutes' WHERE family_id = ${Number(desk.sid)}`);
const idle = await call('GET', '/manage/spaces', { auth: desk.token });
check('3b reception idle 16 min → 401 SESSION_IDLE, session kept',
  idle.status === 401 && idle.body?.error?.code === 'SESSION_IDLE' &&
  Number(sql(`SELECT count(*) FROM refresh_tokens WHERE family_id = ${Number(desk.sid)}`)) > 0,
  `${idle.status} ${idle.body?.error?.code}`);
const refreshed = await call('POST', '/auth/refresh', { cookie: desk.refresh });
check('3c its refresh → 401 SESSION_IDLE, cookies cleared, session gone',
  refreshed.status === 401 && refreshed.body?.error?.code === 'SESSION_IDLE' &&
  refreshed.setCookie.some((c) => /^masaha_refresh=;/.test(c)) &&
  Number(sql(`SELECT count(*) FROM refresh_tokens WHERE family_id = ${Number(desk.sid)}`)) === 0,
  `${refreshed.status} ${refreshed.body?.error?.code}`);

// 4. Reception subscribes a demo customer from the demo space's published month price.
const desk2 = await signIn('demo-reception@example.com');
const price = Number(sql(`SELECT amount_agorot FROM space_prices WHERE space_id = ${spaceId}
  AND period = 'MONTH' AND audience = 'GENERAL' AND shift_id IS NULL AND label_ar IS NULL`));
check('the demo space publishes a general month price', price > 0, `${price} agorot`);
const customerId = Number(sql(`SELECT id FROM customers WHERE space_id = ${spaceId} AND archived_at IS NULL ORDER BY id LIMIT 1`));
const made = await call('POST', `/manage/spaces/${spaceId}/customers/${customerId}/subscriptions`, {
  auth: desk2.token, key: randomUUID(),
  body: { published: { period: 'MONTH', audience: 'GENERAL', name: 'شهري' } },
});
const sub = made.body?.data?.subscription;
const ends = sub && new Date(Date.parse(`${sub.startsOn}T00:00:00Z`) + 29 * 86_400_000).toISOString().slice(0, 10);
check('4 reception subscribes from the month price → 201, FIXED at its amount, 30 days, nothing typed',
  made.status === 201 && sub.priceAgorot === price && sub.billing === 'FIXED' && sub.endsOn === ends &&
  sub.packageId === null && sub.priceTyped === null,
  `${made.status} subscription ${sub?.id} ${sub?.startsOn}→${sub?.endsOn}`);

// 5. The owner is never idle-bound: its requests answer and its session's last use is never renewed.
const before = sql(`SELECT max(last_activity_at) FROM refresh_tokens WHERE family_id = ${Number(owner.sid)}`);
await new Promise((resolve) => setTimeout(resolve, 1_500));
const again = await call('GET', '/manage/spaces', { auth: owner.token });
const after = sql(`SELECT max(last_activity_at) FROM refresh_tokens WHERE family_id = ${Number(owner.sid)}`);
check('5 the owner → 200, its session never renewed (not idle-bound)', again.status === 200 && before === after,
  `${again.status}`);

console.log(failures === 0 ? 'ALL PASS' : `${failures} FAILED`);
process.exit(failures === 0 ? 0 : 1);
