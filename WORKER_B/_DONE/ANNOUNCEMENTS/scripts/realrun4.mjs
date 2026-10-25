// The real run of ANNOUNCEMENTS PR 4 (plan §12.6, PR 4) against the API on 3321 and masaha_b_dev, on the demo
// space. Self-judging: one line per case, `PASS|FAIL <case> <status> <code>`, then `ALL PASS` and exit 0, or exit
// 1 when any case fails. It never prints a secret, a token or a phone number, and keeps no /auth/ body.
//
// Run with the API up on 3321 (npm run dev -w @masaha/api) and the demo data seeded:
//   node C:\dev\masaha\workspace\WORKER_B\ANNOUNCEMENTS\scripts\realrun4.mjs
// Its writes, named by the exec prompt: reception's closure announcement (started two days ago, ending in an hour),
// the owner's extension (the covered subscriptions' ends moved three days) with its rows, and the closure's end.
import { execFileSync } from 'node:child_process';
import { randomUUID } from 'node:crypto';
import { readFileSync } from 'node:fs';

const ENV = 'C:\\dev\\masaha\\app-b\\apps\\api\\.env';
const BASE = 'http://localhost:3321/api/v1';
const SPACE = 'masaha-demo';

/** A variable of apps/api/.env, never printed. */
function envOf(name) {
  const line = readFileSync(ENV, 'utf8')
    .split(/\r?\n/)
    .find((row) => row.startsWith(`${name}=`));
  if (!line) throw new Error(`${name} is not set in apps/api/.env`);
  return line.slice(name.length + 1).trim().replace(/^"(.*)"$/, '$1');
}

/** A read-only query on masaha_b_dev, its rows as `a|b` lines. */
function sql(query) {
  return execFileSync(
    'docker',
    ['exec', 'masaha-postgres-1', 'psql', '-U', 'masaha', '-d', 'masaha_b_dev', '-At', '-c', query],
    { encoding: 'utf8' },
  )
    .split(/\r?\n/)
    .filter(Boolean);
}

async function call(method, path, { token, body, headers: extra = {} } = {}) {
  const headers = { 'Content-Type': 'application/json', ...extra };
  if (token) headers.Authorization = `Bearer ${token}`;
  const response = await fetch(`${BASE}${path}`, {
    method,
    headers,
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const text = await response.text();
  let json = null;
  try {
    json = JSON.parse(text);
  } catch {
    json = null;
  }
  // An /auth/ answer is used once for its token and never kept.
  return { status: response.status, data: json?.data, code: json?.error?.code ?? '-' };
}

let failures = 0;
/** One case: PASS when the status and the code are the expected ones and `check` holds. */
function report(name, answer, expected, check = () => true) {
  let held = false;
  try {
    held = check();
  } catch {
    held = false;
  }
  const ok = answer.status === expected.status && (expected.code ?? '-') === answer.code && held;
  if (!ok) failures += 1;
  console.log(`${ok ? 'PASS' : 'FAIL'} ${name} ${answer.status} ${answer.code}`);
  return ok;
}

async function signIn(email) {
  const login = await call('POST', '/auth/login', {
    body: { email, password: envOf('SEED_DEMO_PASSWORD') },
  });
  if (!login.data) {
    console.log(`FAIL sign-in ${email} ${login.status} ${login.code}`);
    process.exit(1);
  }
  return { token: login.data.accessToken, id: login.data.user.id };
}

const reception = await signIn('demo-reception@example.com');
const owner = await signIn('demo-owner@example.com');
const [spaceId] = sql(`SELECT id FROM spaces WHERE slug = '${SPACE}'`);
console.log(`     space ${spaceId} (${SPACE}); reception ${reception.id}, owner ${owner.id}`);
const base = `/manage/spaces/${spaceId}/announcements`;

// The covered subscriptions, by the rule written here by hand: Gaza's today and the two days before.
const today = sql("SELECT (now() AT TIME ZONE 'Asia/Gaza')::date")[0];
const first = sql("SELECT ((now() AT TIME ZONE 'Asia/Gaza')::date - 2)")[0];
const coveredRule = `space_id = ${spaceId} AND ended_at IS NULL AND ends_on IS NOT NULL
  AND ends_on >= '${first}'::date AND (starts_on IS NULL OR starts_on <= '${today}'::date)`;
const before = new Map(
  sql(`SELECT id, ends_on FROM subscriptions WHERE ${coveredRule} ORDER BY id`).map((row) =>
    row.split('|'),
  ),
);
console.log(`     covered ${first}..${today}: subscriptions ${[...before.keys()].join(', ')}`);
for (const [id, end] of before) console.log(`       ${id} ends ${end}`);

const now = Date.now();
const posted = await call('POST', base, {
  token: reception.token,
  headers: { 'Idempotency-Key': randomUUID() },
  body: {
    type: 'CLOSURE',
    textAr: 'مغلق للصيانة',
    startsAt: new Date(now - 2 * 86_400_000).toISOString(),
    endsAt: new Date(now + 3_600_000).toISOString(),
  },
});
report('reception posts a closure started two days ago, ending in an hour', posted, { status: 201 }, () =>
  posted.data.state === 'RUNNING',
);
const closureId = posted.data?.id;
console.log(`     closure ${closureId}`);
const extendPath = `${base}/${closureId}/extend-subscriptions`;

const preview = await call('GET', extendPath, { token: reception.token });
report('the preview proposes 3 days and counts the covered', preview, { status: 200 }, () =>
  preview.data.proposedDays === 3 &&
  preview.data.firstDay === first &&
  preview.data.lastDay === today &&
  preview.data.subscriptions === before.size &&
  preview.data.applied === null,
);

const refused = await call('POST', extendPath, {
  token: reception.token,
  headers: { 'Idempotency-Key': randomUUID() },
  body: { days: 3 },
});
report('reception extends: 403', refused, { status: 403 });

const key = randomUUID();
const extended = await call('POST', extendPath, {
  token: owner.token,
  headers: { 'Idempotency-Key': key },
  body: { days: 3 },
});
report('the owner extends by 3 days with key E', extended, { status: 201 }, () =>
  extended.data.days === 3 && extended.data.subscriptions === before.size,
);
const retry = await call('POST', extendPath, {
  token: owner.token,
  headers: { 'Idempotency-Key': key },
  body: { days: 3 },
});
report('E again answers the same', retry, { status: 201 }, () =>
  JSON.stringify(retry.data) === JSON.stringify(extended.data),
);
const again = await call('POST', extendPath, {
  token: owner.token,
  headers: { 'Idempotency-Key': randomUUID() },
  body: { days: 3 },
});
report('another key: CLOSURE_ALREADY_EXTENDED', again, {
  status: 409,
  code: 'CLOSURE_ALREADY_EXTENDED',
});

const after = new Map(
  sql(`SELECT id, ends_on FROM subscriptions WHERE id IN (${[...before.keys()].join(',')})`).map(
    (row) => row.split('|'),
  ),
);
const moved = [...before].every(([id, end]) => {
  const expected = new Date(Date.parse(`${end}T00:00:00Z`) + 3 * 86_400_000).toISOString().slice(0, 10);
  console.log(`       ${id} ends ${after.get(id)} (was ${end})`);
  return after.get(id) === expected;
});
report('each covered end three days later', { status: moved ? 200 : 0, code: '-' }, { status: 200 });

const retyped = await call('PATCH', `${base}/${closureId}`, {
  token: owner.token,
  body: { type: 'GENERAL' },
});
report('PATCH type GENERAL: CLOSURE_EXTENDED', retyped, { status: 409, code: 'CLOSURE_EXTENDED' });
const deleted = await call('DELETE', `${base}/${closureId}`, { token: owner.token });
report('DELETE: CLOSURE_EXTENDED', deleted, { status: 409, code: 'CLOSURE_EXTENDED' });
const ended = await call('POST', `${base}/${closureId}/end`, { token: owner.token });
report('end now: 200 ENDED', ended, { status: 200 }, () => ended.data.state === 'ENDED');

const [extensionId] = sql(`SELECT id FROM closure_extensions WHERE announcement_id = ${closureId}`);
const links = sql(
  `SELECT subscription_id FROM subscription_extensions WHERE closure_extension_id = ${extensionId} ORDER BY 1`,
);
console.log(`     extension ${extensionId}; its rows: ${links.join(', ')}`);
report('one subscription_extensions row each', { status: 200, code: '-' }, { status: 200 }, () =>
  links.join(',') === [...before.keys()].join(','),
);
const audit = sql(
  `SELECT action FROM audit_logs WHERE entity_type = 'announcement' AND entity_id = ${closureId} ORDER BY id`,
);
console.log(`     audit: ${audit.join(', ')}`);

console.log(failures === 0 ? 'ALL PASS' : `${failures} FAILED`);
process.exit(failures === 0 ? 0 : 1);
