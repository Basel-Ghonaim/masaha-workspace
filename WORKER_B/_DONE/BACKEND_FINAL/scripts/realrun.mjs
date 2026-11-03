// The real run of BACKEND_FINAL (plan §10) against the API on 3321 and masaha_b_dev. Self-judging: one line per
// case, `PASS|FAIL <case> <status> <code>`, then `ALL PASS` (exit 0) or the count failed (exit 1). It never prints a
// secret, a token, a phone number or an email, and keeps no /auth/ body (only the access token, in memory).
// Its writes, named by the plan: R10 two `PUT /admin/settings/staleness` (to 1/1, then back), two
// `platformSettings.stalenessEdited` entries; R12 two `PATCH /me` (the demo owner's language to the other, then
// back), two `user.profileEdited` entries.
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';

const ENV = 'C:\\dev\\masaha\\app-b\\apps\\api\\.env';
const BASE = 'http://localhost:3321/api/v1';
const DEMO = 1;

function envOf(name) {
  const line = readFileSync(ENV, 'utf8').split(/\r?\n/).find((row) => row.startsWith(`${name}=`));
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

async function call(method, path, { token, body } = {}) {
  const headers = { 'Content-Type': 'application/json' };
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
  return { status: response.status, data: json?.data, meta: json?.meta, code: json?.error?.code ?? '-', text };
}

let failures = 0;
function report(name, answer, expected, check = () => true) {
  let held = false;
  try {
    held = check();
  } catch {
    held = false;
  }
  const ok = answer.status === expected.status && (expected.code === undefined || expected.code === answer.code) && held;
  if (!ok) failures += 1;
  console.log(`${ok ? 'PASS' : 'FAIL'} ${name} ${answer.status} ${answer.code}`);
  return ok;
}
function judge(name, ok) {
  if (!ok) failures += 1;
  console.log(`${ok ? 'PASS' : 'FAIL'} ${name}`);
}

async function signIn(email, password) {
  const login = await call('POST', '/auth/login', { body: { email, password } });
  const token = login.data?.accessToken;
  if (!token) {
    console.log(`FAIL sign-in ${login.status} ${login.code}`);
    process.exit(1);
  }
  return { token };
}

const health = await fetch('http://localhost:3321/health').then((r) => r.json());
judge(`health db ${health.db}`, health.db === 'up');

const demoPassword = envOf('SEED_DEMO_PASSWORD');
const owner = await signIn('demo-owner@example.com', demoPassword);
const reception = await signIn('demo-reception@example.com', demoPassword);
const directoryOwner = await signIn('demo-directory-owner@example.com', demoPassword);
const admin = await signIn(envOf('SEED_ADMIN_EMAIL'), envOf('SEED_ADMIN_PASSWORD'));
const space = (path) => `/manage/spaces/${DEMO}${path}`;
const FINANCE = ['/finance/income', '/finance/debts', '/finance/payers', '/finance/occupancy'];
const GAZA_TODAY = `(now() AT TIME ZONE 'Asia/Gaza')::date`;

// R1 — the owner's four finance reads.
const income = await call('GET', space('/finance/income'), { token: owner.token });
report('R1 income', income, { status: 200 }, () => typeof income.data.income.totalAgorot === 'number');
const debts = await call('GET', space('/finance/debts?limit=50'), { token: owner.token });
report('R1 debts', debts, { status: 200 }, () => typeof debts.meta.totals.owed.customers === 'number');
const payers = await call('GET', space('/finance/payers'), { token: owner.token });
report('R1 payers', payers, { status: 200 }, () => Array.isArray(payers.data));
const occupancy = await call('GET', space('/finance/occupancy'), { token: owner.token });
report('R1 occupancy', occupancy, { status: 200 }, () => occupancy.data.byDay.length === 14 && occupancy.data.byHour.length === 7);

// R2 — cross-checked by SQL.
const [monthIncome] = sql(`SELECT coalesce(sum(amount_agorot), 0) FROM payments WHERE space_id = ${DEMO}
  AND voided_at IS NULL
  AND received_at >= (date_trunc('month', now() AT TIME ZONE 'Asia/Gaza') AT TIME ZONE 'Asia/Gaza')
  AND received_at < ((date_trunc('month', now() AT TIME ZONE 'Asia/Gaza') + interval '1 month') AT TIME ZONE 'Asia/Gaza')`);
judge(`R2 the month's income ${income.data.income.totalAgorot} = SQL ${monthIncome}`, income.data.income.totalAgorot === Number(monthIncome));
const [debtors] = sql(`WITH b AS (
    SELECT u.customer_id, u.due_agorot - coalesce((SELECT sum(amount_agorot) FROM payments WHERE subscription_id = u.subscription_id AND voided_at IS NULL), 0) AS bal
    FROM subscription_usage(${DEMO}, NULL, ${GAZA_TODAY}, ${GAZA_TODAY} - ((extract(dow FROM ${GAZA_TODAY})::int + 1) % 7)) u
    UNION ALL
    SELECT v.customer_id, v.charge_agorot - coalesce((SELECT sum(amount_agorot) FROM payments WHERE visit_id = v.id AND voided_at IS NULL), 0)
    FROM visits v WHERE v.space_id = ${DEMO} AND v.customer_id IS NOT NULL AND v.checked_out_at IS NOT NULL AND v.written_off_at IS NULL)
  SELECT count(*) FROM (SELECT customer_id FROM b GROUP BY customer_id HAVING sum(greatest(bal, 0)) > 0) x`);
judge(`R2 debtors ${debts.meta.totals.owed.customers} = SQL ${debtors} (archived included)`, debts.meta.totals.owed.customers === Number(debtors));
const visitsByDay = new Map(
  sql(`SELECT (checked_in_at AT TIME ZONE 'Asia/Gaza')::date, count(*) FROM visits WHERE space_id = ${DEMO}
    AND checked_out_at IS NOT NULL
    AND checked_in_at >= ((date_trunc('day', now() AT TIME ZONE 'Asia/Gaza') - interval '13 days') AT TIME ZONE 'Asia/Gaza')
    GROUP BY 1`).map((row) => {
    const [d, n] = row.split('|');
    return [d, Number(n)];
  }),
);
judge(
  `R2 the 14 days' closed visits by Gaza day (${[...visitsByDay.values()].reduce((a, b) => a + b, 0)} visits)`,
  occupancy.data.byDay.every(({ date, visits }) => visits === (visitsByDay.get(date) ?? 0)),
);

// R3, R4 — refused.
for (const path of FINANCE) {
  report(`R3 reception ${path}`, await call('GET', space(`${path}?month=bad`), { token: reception.token }), { status: 403 });
  report(`R4 admin ${path}`, await call('GET', space(path), { token: admin.token }), { status: 404 });
  report(`R4 directory owner ${path}`, await call('GET', space(path), { token: directoryOwner.token }), { status: 404 });
}

// R5 — the owner's overview, each count equal to its list.
const totalOf = async (path) => (await call('GET', space(path), { token: owner.token })).meta?.totalRecords;
const overview = await call('GET', space('/overview'), { token: owner.token });
report('R5 the owner reads the overview', overview, { status: 200 }, () => !/agorot/i.test(overview.text));
const o = overview.data;
judge(`R5 uncollected ${o.attention.uncollectedVisits}`, o.attention.uncollectedVisits === (await totalOf('/uncollected-visits')));
judge(`R5 unpriced ${o.attention.unpricedVisits}`, o.attention.unpricedVisits === (await totalOf('/unpriced-visits')));
judge(`R5 open reports ${o.attention.openReports}`, o.attention.openReports === (await totalOf('/data-reports?status=OPEN')));
judge(`R5 running announcements ${o.announcements.running}`, o.announcements.running === (await totalOf('/announcements?state=RUNNING')));
judge(`R5 ending soon ${o.endingSoon.total}`, o.endingSoon.total === (await totalOf('/customers?status=ENDING_SOON')));
judge(`R5 customers owing ${o.attention.customersOwing} = debts' ${debts.meta.totals.owed.customers}`, o.attention.customersOwing === debts.meta.totals.owed.customers);

// R6, R7.
report('R6 reception overview', await call('GET', space('/overview'), { token: reception.token }), { status: 403 });
const r7a = await call('GET', space('/overview'), { token: admin.token });
report('R7 admin overview of a space', r7a, { status: 404 });
const r7b = await call('GET', space('/overview'), { token: directoryOwner.token });
report('R7 directory owner overview of the demo space', r7b, { status: 404 });

// R8 — the admin's overview, each tile equal to its list.
const adminTotal = async (path) => (await call('GET', path, { token: admin.token })).meta?.totalRecords;
const adminOverview = await call('GET', '/admin/overview', { token: admin.token });
report('R8 the admin reads the overview', adminOverview, { status: 200 });
const a = adminOverview.data;
for (const status of ['verified', 'unverified', 'hidden']) {
  judge(`R8 spaces ${status} ${a.spaces[status]}`, a.spaces[status] === (await adminTotal(`/admin/spaces?status=${status}`)));
}
judge(`R8 stale or missing ${a.spaces.staleOrMissing}`, a.spaces.staleOrMissing === (await adminTotal('/admin/spaces?stale=true')));
judge(`R8 completeness ${a.completeness.total}`, a.completeness.total === (await adminTotal('/admin/spaces?status=editable&stale=true')));
judge(`R8 open reports ${a.reports.open}`, a.reports.open === (await adminTotal('/admin/data-reports?status=OPEN')));
judge(`R8 awaiting the admin ${a.reports.awaitingAdmin}`, a.reports.awaitingAdmin === (await adminTotal('/admin/data-reports?status=OPEN&handledBy=ADMIN')));
judge(`R8 awaiting the owners ${a.reports.awaitingOwners}`, a.reports.awaitingOwners === (await adminTotal('/admin/data-reports?status=OPEN&handledBy=OWNER')));
const [newUsers] = sql(`SELECT count(*) FROM users WHERE created_at >= ((date_trunc('day', now() AT TIME ZONE 'Asia/Gaza') - interval '29 days') AT TIME ZONE 'Asia/Gaza')`);
judge(`R8 new users ${a.newUsers} = SQL ${newUsers}`, a.newUsers === Number(newUsers));
judge('R8 nothing of a space\'s operations', !/customer|capacity|present|agorot/i.test(adminOverview.text));

// R9.
report('R9 owner on /admin/overview', await call('GET', '/admin/overview', { token: owner.token }), { status: 403 });
report('R9 reception on /admin/overview', await call('GET', '/admin/overview', { token: reception.token }), { status: 403 });

// R10 — a saved threshold changes both overviews at once; put back.
const staleCount = (ov) => ov.data.attention.groups.stale.length + ov.data.attention.groups.missing.length;
const thresholds = await call('GET', '/admin/settings/staleness', { token: admin.token });
report('R10 read the thresholds (A)', thresholds, { status: 200 });
const A = thresholds.data;
const before = { owner: staleCount(overview), admin: a.spaces.staleOrMissing };
const tightened = await call('PUT', '/admin/settings/staleness', { token: admin.token, body: { stalenessDays: 1, priceStalenessDays: 1 } });
report('R10 PUT 1/1 (write 1 of 2)', tightened, { status: 200 });
const ownerAfter = await call('GET', space('/overview'), { token: owner.token });
const adminAfter = await call('GET', '/admin/overview', { token: admin.token });
judge(
  `R10 both overviews changed: owner ${before.owner}→${staleCount(ownerAfter)}, admin ${before.admin}→${adminAfter.data.spaces.staleOrMissing}`,
  staleCount(ownerAfter) > before.owner && adminAfter.data.spaces.staleOrMissing > before.admin,
);
const restored = await call('PUT', '/admin/settings/staleness', { token: admin.token, body: A });
report('R10 PUT A back (write 2 of 2)', restored, { status: 200 }, () => JSON.stringify(restored.data) === JSON.stringify(A));
const ownerBack = await call('GET', space('/overview'), { token: owner.token });
judge('R10 the owner\'s overview as before', staleCount(ownerBack) === before.owner);

// R11 — the stored contact answered as stored (compared, never printed).
const contact = await call('GET', '/settings/public');
const stored = Object.fromEntries(sql(`SELECT key, value #>> '{}' FROM settings WHERE key IN ('contactEmail', 'contactWhatsapp')`).map((row) => row.split('|')));
report('R11 the public contact as stored', contact, { status: 200 }, () =>
  (contact.data.email ?? null) === (stored.contactEmail || null) && (contact.data.whatsapp ?? null) === (stored.contactWhatsapp || null));

// R12 — /me, the language to the other and back.
const me = await call('GET', '/me', { token: owner.token });
report('R12 GET /me', me, { status: 200 }, () => ['ar', 'en'].includes(me.data.language));
const other = me.data.language === 'ar' ? 'en' : 'ar';
const switched = await call('PATCH', '/me', { token: owner.token, body: { language: other } });
report(`R12 PATCH language → ${other} (write 1 of 2)`, switched, { status: 200 }, () => switched.data.language === other);
const back = await call('PATCH', '/me', { token: owner.token, body: { language: me.data.language } });
report(`R12 PATCH language → ${me.data.language} (write 2 of 2)`, back, { status: 200 }, () => back.data.language === me.data.language);

// R13 — the visits by day.
const [from] = sql(`SELECT ${GAZA_TODAY} - 6`);
const [to] = sql(`SELECT ${GAZA_TODAY}`);
const ranged = await call('GET', space(`/visits?from=${from}&to=${to}`), { token: owner.token });
report(`R13 owner visits ${from}..${to} (${ranged.meta?.totalRecords})`, ranged, { status: 200 });
report('R13 reception with a range', await call('GET', space(`/visits?from=${from}&to=${to}`), { token: reception.token }), { status: 403 });
report('R13 reception today', await call('GET', space('/visits'), { token: reception.token }), { status: 200 });

console.log(failures === 0 ? 'ALL PASS' : `${failures} FAILED`);
process.exit(failures === 0 ? 0 : 1);
