// The real run of SUBSCRIPTIONS PR 3 (plan §12.6, PR 3) against the API on 3321 and masaha_b_dev.
// Self-judging: one line per case, `PASS|FAIL <case> <status> <code>`, `NOT RUN <case>: <why>` for a case the
// demo data cannot show, then the audit log's last actions; exit 0 only when every case passed and ran
// (`ALL PASS`), 2 when one could not run, 1 on a failure. It never prints a secret or a phone number.
//   node C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\scripts\realrun3.mjs
// It writes: one check-in of «محمد عوض» on his split-week subscription, and its check-out.
import { execFileSync } from 'node:child_process';
import { randomUUID } from 'node:crypto';
import { readFileSync } from 'node:fs';

const ENV = 'C:\\dev\\masaha\\app-b\\apps\\api\\.env';
const BASE = 'http://localhost:3321/api/v1';

/** A variable of apps/api/.env, never printed. */
function envOf(name) {
  const line = readFileSync(ENV, 'utf8')
    .split(/\r?\n/)
    .find((row) => row.startsWith(`${name}=`));
  if (!line) throw new Error(`${name} is not set in apps/api/.env`);
  return line.slice(name.length + 1).trim().replace(/^"(.*)"$/, '$1');
}

const password = envOf('SEED_DEMO_PASSWORD');

async function call(method, path, { token, body, key } = {}) {
  const headers = { 'Content-Type': 'application/json' };
  if (token) headers.Authorization = `Bearer ${token}`;
  if (key) headers['Idempotency-Key'] = key;
  const response = await fetch(`${BASE}${path}`, {
    method,
    headers,
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const json = await response.json().catch(() => null);
  return { status: response.status, json, data: json?.data, code: json?.error?.code ?? '-' };
}

let failures = 0;
let notRun = 0;
/** One case: PASS when the status and the code are the expected ones and `check` holds. */
function report(name, answer, expected, check = () => true) {
  let ok = false;
  try {
    ok = answer.status === expected.status && (expected.code ?? '-') === answer.code && check();
  } catch {
    ok = false;
  }
  if (!ok) failures += 1;
  console.log(`${ok ? 'PASS' : 'FAIL'} ${name} ${answer.status} ${answer.code}`);
  return ok;
}

/** An instant's Gaza calendar date, YYYY-MM-DD. */
const gazaDate = (instant) =>
  new Date(instant).toLocaleDateString('en-CA', { timeZone: 'Asia/Gaza' });
const today = gazaDate(Date.now());
const daysBefore = (date, n) =>
  new Date(Date.parse(`${date}T00:00:00Z`) - n * 86_400_000).toISOString().slice(0, 10);

const signIn = async (email) =>
  (await call('POST', '/auth/login', { body: { email, password } })).data?.accessToken;
const owner = await signIn('demo-owner@example.com');
const reception = await signIn('demo-reception@example.com');
if (!owner || !reception) {
  console.log('FAIL sign-in - -');
  process.exit(1);
}
const spaceId = (await call('GET', '/manage/spaces', { token: reception })).data?.[0]?.spaceId;
const base = `/manage/spaces/${spaceId}`;
const customerNamed = async (name) =>
  (await call('GET', `${base}/customers?q=${encodeURIComponent(name)}`, { token: reception })).data?.[0];

// The split-week customer, his subscription and its statement as they are before the run.
const mohammed = await customerNamed('محمد عوض');
const file = await call('GET', `${base}/customers/${mohammed?.id}`, { token: reception });
const split = file.data?.subscriptions?.find((s) => s.name === 'أسبوعان، 6 أيام');
const before = await call('GET', `${base}/subscriptions/${split?.id}`, { token: reception });
const occupancyBefore = await call('GET', `${base}/occupancy`, { token: reception });
report(
  `precondition: محمد not present; his split-week subscription (3 days a week) read; ${String(
    occupancyBefore.data?.present,
  )} present`,
  before,
  { status: 200 },
  () => file.data.present === null && split.daysPerWeek === 3 && occupancyBefore.status === 200,
);
// What its limits should warn of now, from the state before (limits.ts' rule).
const checkedInToday = before.data.checkIns.some((c) => gazaDate(c.checkedInAt) === today);
const expectedLimits = [
  ...(before.data.status === 'UPCOMING' ? ['SUBSCRIPTION_NOT_STARTED'] : []),
  ...(before.data.status === 'EXPIRED' ? ['SUBSCRIPTION_EXPIRED'] : []),
  ...(before.data.progress.daysThisWeek >= 3 && !checkedInToday ? ['DAYS_PER_WEEK_USED'] : []),
];
console.log(
  `     before: status ${before.data.status}, days this week ${before.data.progress.daysThisWeek}, ` +
    `checked in today ${String(checkedInToday)}; the limits expected: ${JSON.stringify(expectedLimits)}`,
);

const LIMITS = ['SUBSCRIPTION_NOT_STARTED', 'SUBSCRIPTION_EXPIRED', 'DAYS_PER_WEEK_USED', 'HOURS_PER_DAY_USED'];
const key = randomUUID();
const first = await call('POST', `${base}/check-ins`, {
  token: reception,
  key,
  body: { subscriptionId: split.id },
});
const warnings = first.json?.meta?.warnings ?? [];
report(
  `reception checks محمد in: warnings ${JSON.stringify(warnings)}`,
  first,
  { status: 201 },
  () =>
    JSON.stringify(warnings.filter((w) => LIMITS.includes(w))) === JSON.stringify(expectedLimits) &&
    first.data.customer.id === mohammed.id &&
    first.data.checkedOutAt === null,
);
const checkInId = first.data?.id;

const retry = await call('POST', `${base}/check-ins`, {
  token: reception,
  key,
  body: { subscriptionId: split.id },
});
report('the same key: the same check-in and the same warnings', retry, { status: 201 }, () =>
  retry.data.id === checkInId &&
  JSON.stringify(retry.json?.meta?.warnings ?? []) === JSON.stringify(warnings),
);

// The plan's case: the present demo subscriber, سارة.
const sara = await customerNamed('سارة خالد');
const saraFile = await call('GET', `${base}/customers/${sara?.id}`, { token: reception });
if (saraFile.data?.present === null) {
  notRun += 1;
  console.log('NOT RUN سارة present → 409: سارة is not present in the demo data (her open check-in was closed)');
} else {
  const saraSub = saraFile.data.subscriptions[0];
  report(
    'سارة, present: refused',
    await call('POST', `${base}/check-ins`, {
      token: reception,
      key: randomUUID(),
      body: { subscriptionId: saraSub.id },
    }),
    { status: 409, code: 'MEMBER_ALREADY_CHECKED_IN' },
  );
}
// The same rule on the run's own check-in: محمد, present now, with another key.
report(
  'SUBSTITUTE محمد, present by the run\'s check-in, another key: refused',
  await call('POST', `${base}/check-ins`, {
    token: reception,
    key: randomUUID(),
    body: { subscriptionId: split.id },
  }),
  { status: 409, code: 'MEMBER_ALREADY_CHECKED_IN' },
);

const occupancy = await call('GET', `${base}/occupancy`, { token: reception });
report(
  `the occupancy counts him: ${String(occupancy.data?.present)} present`,
  occupancy,
  { status: 200 },
  () =>
    occupancy.data.present === occupancyBefore.data.present + 1 &&
    occupancy.data.people.some((p) => p.kind === 'CHECK_IN' && p.id === checkInId),
);

const open = await call('GET', `${base}/check-ins?open=true`, { token: reception });
report(`the open check-ins: ${String(open.data?.length)}, his among them, no meta`, open, { status: 200 }, () =>
  open.data.some((c) => c.id === checkInId) && open.json.meta === undefined,
);

const out = await call('POST', `${base}/check-ins/${checkInId}/check-out`, { token: reception });
report(
  `check-out: MANUAL, paid ${String(out.data?.paidAgorot)}, balance ${String(out.data?.balanceAgorot)}`,
  out,
  { status: 200 },
  () =>
    out.data.checkoutMethod === 'MANUAL' &&
    out.data.checkedOutAt !== null &&
    Number.isInteger(out.data.paidAgorot) &&
    Number.isInteger(out.data.balanceAgorot),
);
const again = await call('POST', `${base}/check-ins/${checkInId}/check-out`, { token: reception });
report('check-out again: answered as it is', again, { status: 200 }, () =>
  again.data.checkedOutAt === out.data.checkedOutAt,
);

const range = await call('GET', `${base}/check-ins?from=${daysBefore(today, 7)}&to=${today}`, {
  token: reception,
});
report(
  `the last week's check-ins: ${String(range.json?.meta?.totalRecords)}, his first`,
  range,
  { status: 200 },
  () => range.data[0].id === checkInId && range.json.meta.totalRecords >= 1,
);

// The audit log's last actions, from masaha_b_dev (the database's user from DATABASE_URL, not printed).
const url = new URL(envOf('DATABASE_URL'));
const actions = execFileSync(
  'docker',
  [
    'exec',
    'masaha-postgres-1',
    'psql',
    '-U',
    decodeURIComponent(url.username),
    '-d',
    url.pathname.slice(1),
    '-tA',
    '-c',
    'SELECT action FROM audit_logs ORDER BY id DESC LIMIT 4',
  ],
  { encoding: 'utf8' },
);
console.log('audit (latest first):', actions.trim().split(/\r?\n/).join(', '));

if (failures > 0) console.log(`${failures} FAIL`);
else if (notRun > 0) console.log(`${notRun} NOT RUN, the rest PASS`);
else console.log('ALL PASS');
process.exit(failures > 0 ? 1 : notRun > 0 ? 2 : 0);
