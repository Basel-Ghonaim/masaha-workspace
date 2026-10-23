// The real run of SUBSCRIPTIONS PR 2 (plan §12.6, PR 2) against the API on 3321 and masaha_b_dev, written by
// phase 1 and run by phase 2. Self-judging: one line per case, `PASS|FAIL <case> <status> <code>`, then the audit
// log's last ten actions; the exit code is 1 when any case fails. It never prints a secret or a phone number.
//
// Run from anywhere, with the API up on 3321 (npm run dev -w @masaha/api) and the demo data seeded:
//   node C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\scripts\realrun2.mjs
// Precondition (checked as the first case): the demo customer «رامي سالم» owes ₪15 on one visit and has no
// subscription — the demo seed's state. The run changes it (see the hand-over); run it once.
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
/** One case: PASS when the status and the code are the expected ones and `check` holds. */
function report(name, answer, expected, check = () => true) {
  const ok = answer.status === expected.status && (expected.code ?? '-') === answer.code && check();
  if (!ok) failures += 1;
  console.log(`${ok ? 'PASS' : 'FAIL'} ${name} ${answer.status} ${answer.code}`);
  return ok;
}

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

// The demo customer and package, by name.
const found = await call('GET', `${base}/customers?q=${encodeURIComponent('رامي سالم')}`, {
  token: reception,
});
const rami = found.data?.[0];
const weekly = (await call('GET', `${base}/packages`, { token: reception })).data?.find(
  (pack) => pack.name === 'أسبوعي' && pack.isActive,
);
const file = await call('GET', `${base}/customers/${rami?.id}`, { token: reception });
report(
  'precondition: رامي owes 1500 on one visit, no subscription; the package أسبوعي (12000, fixed)',
  file,
  { status: 200 },
  () =>
    file.data.subscriptions.length === 0 &&
    file.data.unpaidVisits.length === 1 &&
    file.data.unpaidVisits[0].balanceAgorot === 1_500 &&
    weekly?.priceAgorot === 12_000 &&
    weekly?.billing === 'FIXED',
);
const visitId = file.data?.unpaidVisits?.[0]?.visit?.id;

// 1. Subscribing from a package with a payment that covers the old debt and part of the new price.
const key = randomUUID();
const body = { packageId: weekly?.id, payment: { amountAgorot: 6_500, method: 'CASH' } };
const subscribed = await call('POST', `${base}/customers/${rami?.id}/subscriptions`, {
  token: reception,
  key,
  body,
});
const sub1 = subscribed.data?.subscription;
report(
  'subscribe with a payment: two payments (the visit 1500, the new one 5000), no CUSTOMER_HAS_DEBT',
  subscribed,
  { status: 201 },
  () =>
    subscribed.data.payments.length === 2 &&
    subscribed.data.payments[0].item.visitId === visitId &&
    subscribed.data.payments[0].payment.amountAgorot === 1_500 &&
    subscribed.data.payments[1].item.subscriptionId === sub1.id &&
    subscribed.data.payments[1].payment.amountAgorot === 5_000 &&
    sub1.paidAgorot === 5_000 &&
    sub1.balanceAgorot === 7_000 &&
    !(subscribed.json.meta?.warnings ?? []).includes('CUSTOMER_HAS_DEBT'),
);

// 2. The same key: the same body.
const retried = await call('POST', `${base}/customers/${rami?.id}/subscriptions`, {
  token: reception,
  key,
  body,
});
report(
  'the same key: the same body',
  retried,
  { status: 201 },
  () => JSON.stringify(retried.data) === JSON.stringify(subscribed.data),
);

// 3. A renewal of that subscription, then a second renewal of it with another key.
const renewal = await call('POST', `${base}/customers/${rami?.id}/subscriptions`, {
  token: reception,
  key: randomUUID(),
  body: { packageId: weekly?.id, renewalOfId: sub1?.id },
});
report(
  'a renewal: starts the day after the renewed one ends',
  renewal,
  { status: 201 },
  () => {
    const next = new Date(`${sub1.endsOn}T00:00:00Z`);
    next.setUTCDate(next.getUTCDate() + 1);
    return (
      renewal.data.subscription.renewalOfId === sub1.id &&
      renewal.data.subscription.startsOn === next.toISOString().slice(0, 10)
    );
  },
);
const again = await call('POST', `${base}/customers/${rami?.id}/subscriptions`, {
  token: reception,
  key: randomUUID(),
  body: { packageId: weekly?.id, renewalOfId: sub1?.id },
});
report('a second renewal with another key', again, {
  status: 409,
  code: 'SUBSCRIPTION_ALREADY_RENEWED',
});

// 4. A payment above the fixed price (5000 paid of 12000; 12000 more).
const above = await call('POST', `${base}/payments`, {
  token: reception,
  key: randomUUID(),
  body: { subscriptionId: sub1?.id, amountAgorot: 12_000, method: 'CASH' },
});
report('a payment above a fixed price', above, { status: 409, code: 'PAYMENT_EXCEEDS_DUE' });

// 5. The statement.
const statement = await call('GET', `${base}/subscriptions/${sub1?.id}`, { token: reception });
report(
  'the statement: paid 5000, its payment listed, renewed by the renewal',
  statement,
  { status: 200 },
  () =>
    statement.data.paidAgorot === 5_000 &&
    statement.data.payments.length === 1 &&
    statement.data.renewedById === renewal.data.subscription.id &&
    statement.data.renewal === null,
);

// 6. Reception's price correction; 7. the owner's below what is paid.
const byReception = await call('PUT', `${base}/subscriptions/${sub1?.id}/price`, {
  token: reception,
  body: { billing: 'FIXED', priceAgorot: 4_000, reason: 'تجربة التشغيل' },
});
report("reception's price correction", byReception, { status: 403 });
const below = await call('PUT', `${base}/subscriptions/${sub1?.id}/price`, {
  token: owner,
  body: { billing: 'FIXED', priceAgorot: 4_000, reason: 'تجربة التشغيل' },
});
report("the owner's price below what is paid", below, { status: 409, code: 'PRICE_BELOW_PAID' });

// 8. Ending it early.
const ended = await call('POST', `${base}/subscriptions/${sub1?.id}/end`, { token: reception });
report(
  'ending it early: EXPIRED, ended by reception',
  ended,
  { status: 200 },
  () => ended.data.status === 'EXPIRED' && ended.data.ended !== null,
);

// The audit log's last ten actions, from masaha_b_dev (the database's user from DATABASE_URL, not printed).
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
    'SELECT action FROM audit_logs ORDER BY id DESC LIMIT 10',
  ],
  { encoding: 'utf8' },
);
console.log('audit (latest first):', actions.trim().split(/\r?\n/).join(', '));

console.log(failures === 0 ? 'ALL PASS' : `${failures} FAIL`);
process.exit(failures === 0 ? 0 : 1);
