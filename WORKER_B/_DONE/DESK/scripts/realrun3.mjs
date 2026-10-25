// DESK PR 3's real run (plan §12.6): the API on 3321, masaha_b_dev. Reads the secrets from
// apps/api/.env into variables; never prints them.
import { execFileSync } from 'node:child_process';
import { randomUUID } from 'node:crypto';
import { readFileSync } from 'node:fs';

const ENV = readFileSync('C:/dev/masaha/app-b/apps/api/.env', 'utf8');
const envOf = (name) => (ENV.match(new RegExp(`^${name}=(.*)$`, 'm')) ?? [])[1]?.trim();
const PASSWORD = envOf('SEED_DEMO_PASSWORD');
const SECRET = envOf('JOBS_SECRET');
const DB_USER = new URL(envOf('DATABASE_URL')).username;
const LOG = 'C:/dev/masaha/workspace/WORKER_B/DESK/scripts/server.log';
const BASE = 'http://localhost:3321';
const API = `${BASE}/api/v1`;

const sql = (query) =>
  execFileSync('docker', ['exec', 'masaha-postgres-1', 'psql', '-U', DB_USER, '-d', 'masaha_b_dev', '-tAc', query], {
    encoding: 'utf8',
  }).trim();
const say = (...line) => console.log(...line);
const wait = (ms) => new Promise((r) => setTimeout(r, ms));

async function call(method, path, { token, body, headers = {} } = {}) {
  const response = await fetch(`${API}${path}`, {
    method,
    headers: {
      'content-type': 'application/json',
      ...(token ? { authorization: `Bearer ${token}` } : {}),
      ...headers,
    },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const text = await response.text();
  let json = null;
  try {
    json = JSON.parse(text);
  } catch {}
  return { status: response.status, json };
}

async function signIn(email) {
  const { status, json } = await call('POST', '/auth/login', { body: { email, password: PASSWORD } });
  if (status !== 200) throw new Error(`sign-in ${email}: ${status} ${JSON.stringify(json?.error)}`);
  return { token: json.data.accessToken, id: json.data.user.id };
}

const jobRanLines = () => readFileSync(LOG, 'utf8').split('\n').filter((l) => l.includes('job ran'));

// 0. Health and the timer's first run.
say('health', JSON.stringify(await (await fetch(`${BASE}/health`)).json()));
for (let i = 0; i < 60 && jobRanLines().length < 2; i++) await wait(1000);
say("the timer's first run: 'job ran' lines =", jobRanLines().length);
for (const line of jobRanLines()) say('  log:', line.slice(0, 200));

const owner = await signIn('demo-owner@example.com');
const reception = await signIn('demo-reception@example.com');
const spaceId = Number(sql("SELECT id FROM spaces WHERE slug = 'masaha-demo'"));
const S = `/manage/spaces/${spaceId}`;
say('space', spaceId, 'owner', owner.id, 'reception', reception.id);

const before = (await call('GET', `${S}/settings`, { token: owner.token })).json.data;
say('settings before', JSON.stringify({ maxStayMinutes: before.maxStayMinutes, receptionMayTypePrices: before.receptionMayTypePrices, autoCheckoutAtClosing: before.autoCheckoutAtClosing }));
say('PATCH settings maxStayMinutes 60 →', (await call('PATCH', `${S}/settings`, { token: owner.token, body: { maxStayMinutes: 60 } })).status);

// 1. A visit checked in three hours ago, at 5 ₪ / 25 ₪.
const visitId = Number(
  sql(`INSERT INTO visits (space_id, request_id, visitor_name, checked_in_at, hour_rate_agorot, day_rate_agorot, updated_at)
       VALUES (${spaceId}, gen_random_uuid(), 'Real run PR3', now() - interval '3 hours', 500, 2500, now()) RETURNING id`).split('\n')[0],
);
say('inserted visit', visitId, 'checked_in_at', sql(`SELECT checked_in_at FROM visits WHERE id = ${visitId}`));

const run = (headers) => call('POST', '/internal/jobs/run', { headers });
const noAuth = await run({});
say('jobs/run without the secret →', noAuth.status, JSON.stringify(noAuth.json?.error));
const wrong = await run({ authorization: 'Bearer not-the-secret' });
say('jobs/run with a wrong secret →', wrong.status);
const first = await run({ authorization: `Bearer ${SECRET}` });
say('jobs/run with the secret →', first.status, JSON.stringify(first.json?.data));
say('the visit now', sql(`SELECT checked_in_at, checked_out_at, checked_out_at - checked_in_at AS stay, checkout_method, charge_agorot FROM visits WHERE id = ${visitId}`));
const again = await run({ authorization: `Bearer ${SECRET}` });
say('jobs/run again →', again.status, JSON.stringify(again.json?.data));

const uncollected = await call('GET', `${S}/uncollected-visits?limit=50`, { token: owner.token });
const mine = uncollected.json?.data?.find((row) => row.visit.id === visitId);
say('GET uncollected-visits →', uncollected.status, 'total', uncollected.json?.meta?.totalRecords, 'ours:', JSON.stringify(mine && { id: mine.visit.id, paidAgorot: mine.paidAgorot, balanceAgorot: mine.balanceAgorot }));

// 2. An unpriced close by reception (switch off), listed, then priced by the owner.
say('PATCH settings receptionMayTypePrices false →', (await call('PATCH', `${S}/settings`, { token: owner.token, body: { receptionMayTypePrices: false, maxStayMinutes: null } })).status);
const noRate = Number(
  sql(`INSERT INTO visits (space_id, request_id, visitor_name, checked_in_at, updated_at)
       VALUES (${spaceId}, gen_random_uuid(), 'Real run PR3 no rate', now() - interval '20 minutes', now()) RETURNING id`).split('\n')[0],
);
const out = await call('POST', `${S}/visits/${noRate}/check-out`, {
  token: reception.token,
  headers: { 'idempotency-key': randomUUID() },
  body: { phone: '0599000123' },
});
say('reception check-out of a visit with no rate →', out.status, JSON.stringify({ charge: out.json?.data?.visit?.charge, method: out.json?.data?.visit?.checkoutMethod, customer: out.json?.data?.visit?.customer?.id }));
const unpriced = await call('GET', `${S}/unpriced-visits?limit=50`, { token: owner.token });
say('GET unpriced-visits →', unpriced.status, 'lists it:', Boolean(unpriced.json?.data?.some((v) => v.id === noRate)));
const refused = await call('PUT', `${S}/visits/${noRate}/charge`, { token: reception.token, body: { amountAgorot: 1000, reason: 'Real run' } });
say('reception PUT charge →', refused.status, refused.json?.error?.code);
const priced = await call('PUT', `${S}/visits/${noRate}/charge`, { token: owner.token, body: { amountAgorot: 1000, reason: 'Real run' } });
say('owner PUT charge →', priced.status, JSON.stringify(priced.json?.data?.charge));
const twice = await call('PUT', `${S}/visits/${noRate}/charge`, { token: owner.token, body: { amountAgorot: 1000, reason: 'Real run' } });
say('owner PUT charge again →', twice.status, twice.json?.error?.code);

// Put the settings back.
say('PATCH settings back →', (await call('PATCH', `${S}/settings`, { token: owner.token, body: { receptionMayTypePrices: before.receptionMayTypePrices, maxStayMinutes: before.maxStayMinutes } })).status);
say('audit', sql("SELECT string_agg(action, ', ' ORDER BY id DESC) FROM (SELECT id, action FROM audit_logs ORDER BY id DESC LIMIT 12) a"));
