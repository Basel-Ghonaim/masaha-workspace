// The real run of PAYMENTS (plan §12.6) against the API on 3321 and masaha_b_dev, freshly reseeded. Self-judging:
// one line per case, `PASS|FAIL <case> <status> <code>`, then `ALL PASS` and exit 0, or exit 1 when any case fails.
// It never prints a secret or a phone number. Run it once: its writes are named in the report.
//   node C:\dev\masaha\workspace\WORKER_B\PAYMENTS\scripts\realrun1.mjs
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
  return {
    status: response.status,
    json,
    data: json?.data,
    meta: json?.meta,
    code: json?.error?.code ?? '-',
  };
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

const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const totalsOf = (count, received, cash, transfer, voidedCount, voidedAmount) => ({
  count,
  receivedAgorot: received,
  byMethod: { CASH: cash, TRANSFER: transfer },
  voided: { count: voidedCount, amountAgorot: voidedAmount },
});

const signIn = async (email) =>
  (await call('POST', '/auth/login', { body: { email, password } })).data?.accessToken;
const owner = await signIn('demo-owner@example.com');
const reception = await signIn('demo-reception@example.com');
const directoryOwner = await signIn('demo-directory-owner@example.com');
if (!owner || !reception || !directoryOwner) {
  console.log('FAIL sign-in - -');
  process.exit(1);
}
const spaces = (await call('GET', '/manage/spaces', { token: owner })).data ?? [];
const spaceId = spaces[0]?.spaceId;
const base = `/manage/spaces/${spaceId}`;

// Gaza's today and ten days back, as dates.
const today = new Intl.DateTimeFormat('en-CA', { timeZone: 'Asia/Gaza' }).format(new Date());
const shift = (date, days) => {
  const day = new Date(`${date}T00:00:00Z`);
  day.setUTCDate(day.getUTCDate() + days);
  return day.toISOString().slice(0, 10);
};
const range = `?from=${shift(today, -10)}&to=${today}`;

// 1. The owner's ledger of the last ten days: the demo's six payments.
const ledger = await call('GET', `${base}/payments${range}`, { token: owner });
const rows = ledger.data ?? [];
const duplicate = rows.find((row) => row.voided !== null);
const heba = rows.find((row) => row.item.kind === 'VISIT' && row.item.visitorName === 'هبة');
report('1 owner: six payments newest first, totals 47500 (cash 37500, transfer 10000), count 5, voided 1/20000', ledger, { status: 200 }, () =>
  rows.length === 6 &&
  rows.every((row, i) => i === 0 || rows[i - 1].receivedAt >= row.receivedAt) &&
  same(ledger.meta.totals, totalsOf(5, 47_500, 37_500, 10_000, 1, 20_000)) &&
  duplicate.voided.reason === 'سُجّلت مرتين' &&
  typeof duplicate.voided.by.name === 'string' &&
  duplicate.voided.by.name.length > 0 &&
  heba !== undefined,
);

// 2–3. Reception's own today: none yet; a range refused.
const mineEmpty = await call('GET', `${base}/payments`, { token: reception });
report('2 reception today: [] and totals 0', mineEmpty, { status: 200 }, () =>
  mineEmpty.data.length === 0 && same(mineEmpty.meta.totals, totalsOf(0, 0, 0, 0, 0, 0)),
);
report(
  '3 reception with from/to: 403',
  await call('GET', `${base}/payments?from=${today}&to=${today}`, { token: reception }),
  { status: 403 },
);

// The visit of «رامي», closed by hand and owed by its customer.
const customers = await call('GET', `${base}/customers?q=${encodeURIComponent('رامي')}`, {
  token: owner,
});
const rami = customers.data?.[0];
const file = await call('GET', `${base}/customers/${rami?.id}`, { token: owner });
const ramiVisit = file.data?.unpaidVisits?.find((row) => row.visit.visitorName === 'رامي');
report('precondition: رامي owes 1500 on his manual visit', file, { status: 200 }, () =>
  ramiVisit.balanceAgorot === 1_500 && ramiVisit.visit.checkoutMethod === 'MANUAL',
);
const visitId = ramiVisit?.visit.id;

// 4. Reception records 500 on it; its own list shows that one.
const paid = await call('POST', `${base}/payments`, {
  token: reception,
  key: randomUUID(),
  body: { visitId, amountAgorot: 500, method: 'CASH' },
});
report('4a reception pays 500 on رامي: 201, balance 1000', paid, { status: 201 }, () =>
  paid.data.balanceAgorot === 1_000,
);
const fourthId = paid.data?.payment?.id;
const mineOne = await call('GET', `${base}/payments`, { token: reception });
report('4b reception today: that one, totals 500 cash', mineOne, { status: 200 }, () =>
  mineOne.data.length === 1 &&
  mineOne.data[0].id === fourthId &&
  same(mineOne.meta.totals, totalsOf(1, 500, 500, 0, 0, 0)),
);

// 5. Reception never voids.
report(
  '5 reception voids: 403',
  await call('POST', `${base}/payments/${fourthId}/void`, {
    token: reception,
    body: { reason: 'Mistake' },
  }),
  { status: 403 },
);

// 6. The owner voids «هبة»'s payment; again, with another reason; her visit is uncollected.
const voidHeba = await call('POST', `${base}/payments/${heba?.id}/void`, {
  token: owner,
  body: { reason: 'R1: cash not in the drawer' },
});
report('6a owner voids هبة: 200 voided R1', voidHeba, { status: 200 }, () =>
  voidHeba.data.voided.reason === 'R1: cash not in the drawer',
);
const again = await call('POST', `${base}/payments/${heba?.id}/void`, {
  token: owner,
  body: { reason: 'R2: another reason' },
});
report('6b again with R2: 200, reason R1, same answer', again, { status: 200 }, () =>
  again.data.voided.reason === 'R1: cash not in the drawer' && same(again.data, voidHeba.data),
);
const uncollected = await call('GET', `${base}/uncollected-visits?limit=50`, { token: owner });
report('6c uncollected: هبة with balance 1500', uncollected, { status: 200 }, () =>
  uncollected.data.some(
    (row) => row.visit.id === heba.item.id && row.balanceAgorot === 1_500 && row.paidAgorot === 0,
  ),
);

// 7. Another space's owner reaches neither route.
report(
  '7a directory owner lists the demo space: 404',
  await call('GET', `${base}/payments`, { token: directoryOwner }),
  { status: 404 },
);
report(
  '7b directory owner voids: 404',
  await call('POST', `${base}/payments/${fourthId}/void`, {
    token: directoryOwner,
    body: { reason: 'Not mine' },
  }),
  { status: 404 },
);

// 8. The owner voids case 4's payment; reception sees it marked.
report(
  '8a owner voids case 4: 200',
  await call('POST', `${base}/payments/${fourthId}/void`, {
    token: owner,
    body: { reason: 'Recorded on the wrong visit' },
  }),
  { status: 200 },
);
const mineVoided = await call('GET', `${base}/payments`, { token: reception });
report('8b reception today: it, voided by the owner; received 0, voided 1/500', mineVoided, { status: 200 }, () =>
  mineVoided.data.length === 1 &&
  mineVoided.data[0].voided?.reason === 'Recorded on the wrong visit' &&
  same(mineVoided.meta.totals, totalsOf(0, 0, 0, 0, 1, 500)),
);

// 9. A written-off visit's payment: refused until the write-off is undone.
const more = await call('POST', `${base}/payments`, {
  token: reception,
  key: randomUUID(),
  body: { visitId, amountAgorot: 500, method: 'CASH' },
});
report('9a reception pays 500 more on رامي: 201', more, { status: 201 });
const moreId = more.data?.payment?.id;
report(
  '9b owner writes the visit off: 200',
  await call('POST', `${base}/visits/${visitId}/write-off`, {
    token: owner,
    body: { reason: 'Left the city' },
  }),
  { status: 200 },
);
report(
  '9c owner voids that 500: 409 VISIT_WRITTEN_OFF',
  await call('POST', `${base}/payments/${moreId}/void`, {
    token: owner,
    body: { reason: 'Wrong amount' },
  }),
  { status: 409, code: 'VISIT_WRITTEN_OFF' },
);
report(
  '9d owner undoes the write-off: 200',
  await call('DELETE', `${base}/visits/${visitId}/write-off`, { token: owner }),
  { status: 200 },
);
report(
  '9e the void again: 200',
  await call('POST', `${base}/payments/${moreId}/void`, {
    token: owner,
    body: { reason: 'Wrong amount' },
  }),
  { status: 200 },
);

console.log(failures === 0 ? 'ALL PASS' : `${failures} FAILED`);
process.exit(failures === 0 ? 0 : 1);
