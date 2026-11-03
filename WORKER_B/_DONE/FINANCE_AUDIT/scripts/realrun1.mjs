// The real run of FINANCE_AUDIT PR 1 (plan §12.6, PR 1) against the API on 3321 and masaha_b_dev. Self-judging:
// one line per case, `PASS|FAIL <case> <status> <code>`, then `ALL PASS` and exit 0, or the count failed and exit
// 1. It never prints a secret, a token or a phone number, and keeps no /auth/ body (only the access token, in
// memory).
//
// Run with the API up on 3321 (npm run dev -w @masaha/api) and the demo data seeded:
//   node C:\dev\masaha\workspace\WORKER_B\FINANCE_AUDIT\scripts\realrun1.mjs
// Its writes, named by the plan: the admin hides, then shows, the demo space (1) and one unverified directory
// space (10, Tuffah Place): four `PUT /admin/spaces/:id/hidden`, four audit entries.
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';

const ENV = 'C:\\dev\\masaha\\app-b\\apps\\api\\.env';
const BASE = 'http://localhost:3321/api/v1';
const DEMO = 1;
const UNVERIFIED = 10;

// The admin's list (apps/api/src/modules/audit/platformEvents.ts), copied to judge each row.
const PLATFORM_ACTIONS = new Set([
  'space.created', 'space.profileEdited', 'space.hoursEdited', 'space.pricesEdited', 'space.amenitiesEdited',
  'space.contactsEdited', 'space.profileConfirmed', 'space.hoursConfirmed', 'space.pricesConfirmed',
  'space.amenitiesConfirmed', 'space.contactsConfirmed', 'space.photoAdded', 'space.photoRemoved',
  'space.photosReordered', 'space.hidden', 'space.unhidden', 'space.deleted', 'space.restored',
  'space.ownerLinked', 'space.ownerUnlinked', 'governorate.added', 'governorate.edited', 'governorate.hidden',
  'governorate.restored', 'area.added', 'area.edited', 'area.hidden', 'area.restored', 'amenity.added',
  'amenity.edited', 'amenity.hidden', 'amenity.restored', 'dataReport.resolved', 'dataReport.dismissed',
]);
const PLATFORM_ACCOUNT_ACTIONS = new Set([
  'user.created', 'user.roleChanged', 'user.suspended', 'user.unsuspended', 'user.temporaryPasswordIssued',
  'user.temporaryPasswordHandedOver', 'user.emailChanged',
]);

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

async function signIn(email, password) {
  const login = await call('POST', '/auth/login', { body: { email, password } });
  // An /auth/ answer is used once for its token and never kept.
  const token = login.data?.accessToken;
  const id = login.data?.user?.id;
  if (!token) {
    console.log(`FAIL sign-in ${login.status} ${login.code}`);
    process.exit(1);
  }
  return { token, id };
}

const health = await fetch('http://localhost:3321/health').then((r) => r.json());
console.log(`${health.db === 'up' ? 'PASS' : 'FAIL'} health db ${health.db}`);
if (health.db !== 'up') failures += 1;

const demoPassword = envOf('SEED_DEMO_PASSWORD');
const owner = await signIn('demo-owner@example.com', demoPassword);
const reception = await signIn('demo-reception@example.com', demoPassword);
const directoryOwner = await signIn('demo-directory-owner@example.com', demoPassword);
const admin = await signIn(envOf('SEED_ADMIN_EMAIL'), envOf('SEED_ADMIN_PASSWORD'));

// The owner's log: 200, and its count is the space's entries since the Gaza midnight 29 days back.
const since = `((date_trunc('day', now() AT TIME ZONE 'Asia/Gaza') - interval '29 days') AT TIME ZONE 'Asia/Gaza')`;
const [expectedCount] = sql(`SELECT count(*) FROM audit_logs WHERE space_id = ${DEMO} AND created_at >= ${since}`);
const ownerLog = await call('GET', `/manage/spaces/${DEMO}/audit-log?limit=50`, { token: owner.token });
report(`owner reads the space's log (${ownerLog.meta?.totalRecords} entries, SQL ${expectedCount})`, ownerLog, { status: 200 }, () =>
  ownerLog.meta.totalRecords === Number(expectedCount) && Array.isArray(ownerLog.meta.actors));
report('reception is refused', await call('GET', `/manage/spaces/${DEMO}/audit-log`, { token: reception.token }), {
  status: 403,
});
report(
  "the directory owner on the demo space is not_found",
  await call('GET', `/manage/spaces/${DEMO}/audit-log`, { token: directoryOwner.token }),
  { status: 404 },
);

/** Every page of the admin's log, all time. */
async function adminLog(query = '') {
  const rows = [];
  let last;
  for (let page = 1; page <= 20; page += 1) {
    last = await call('GET', `/admin/audit-log?period=ALL&limit=50&page=${page}${query}`, { token: admin.token });
    if (last.status !== 200) return { answer: last, rows };
    rows.push(...last.data);
    if (!last.meta.hasNextPage) break;
  }
  return { answer: last, rows };
}

const isPlatform = (row) =>
  PLATFORM_ACTIONS.has(row.action) || (PLATFORM_ACCOUNT_ACTIONS.has(row.action) && row.space === null);
const before = await adminLog();
const off = before.rows.filter((row) => !isPlatform(row)).map((row) => row.action);
report(
  `admin reads the platform's events (${before.rows.length}; every action on the list; off-list: ${off.join(',') || 'none'})`,
  before.answer,
  { status: 200 },
  () => off.length === 0,
);
const [platformCount] = sql(
  `SELECT count(*) FROM audit_logs WHERE action = ANY(ARRAY['${[...PLATFORM_ACTIONS].join("','")}']) OR (action = ANY(ARRAY['${[...PLATFORM_ACCOUNT_ACTIONS].join("','")}']) AND space_id IS NULL)`,
);
console.log(`     the admin's rows ${before.rows.length}, SQL by the same list ${platformCount}`);
if (before.rows.length !== Number(platformCount)) {
  failures += 1;
  console.log('FAIL the admin row count differs from SQL');
}

// The run's writes: hide, then show, the demo space and one unverified directory space.
const writes = [];
for (const spaceId of [DEMO, UNVERIFIED]) {
  for (const isHidden of [true, false]) {
    const put = await call('PUT', `/admin/spaces/${spaceId}/hidden`, { token: admin.token, body: { isHidden } });
    writes.push(`${spaceId}:${isHidden}`);
    report(`admin sets space ${spaceId} hidden ${isHidden}`, put, { status: 204 });
  }
}

const after = await adminLog();
const fresh = after.rows.filter((row) => !before.rows.some((old) => old.id === row.id));
const named = (row) => ({ action: row.action, target: row.target.name, space: row.space?.id });
console.log(`     the admin's new rows: ${JSON.stringify(fresh.map(named))}`);
report("the admin's log shows the four, with names", after.answer, { status: 200 }, () =>
  fresh.length === 4 &&
  fresh.filter((row) => row.target.id === DEMO && row.target.name === 'Demo Space').length === 2 &&
  fresh.filter((row) => row.target.id === UNVERIFIED && row.target.name === 'Tuffah Place').length === 2 &&
  fresh.every((row) => ['space.hidden', 'space.unhidden'].includes(row.action) && row.actor.kind === 'PERSON'));

const ownerAfter = await call('GET', `/manage/spaces/${DEMO}/audit-log?limit=5`, { token: owner.token });
const mine = ownerAfter.data?.filter((row) => fresh.some((f) => f.id === row.id)) ?? [];
report("the owner's log shows the demo space's two, the actor MASAHA with no id or name", ownerAfter, { status: 200 }, () =>
  mine.length === 2 &&
  mine.every((row) => JSON.stringify(row.actor) === '{"kind":"MASAHA"}') &&
  ownerAfter.data.every((row) => row.actor.id !== admin.id));

const searched = await call('GET', `/manage/spaces/${DEMO}/audit-log?q=${encodeURIComponent('Demo Space')}&limit=50`, {
  token: owner.token,
});
report(`q=Demo Space finds them (${searched.meta?.totalRecords} entries)`, searched, { status: 200 }, () =>
  mine.every((row) => searched.data.some((found) => found.id === row.id)) &&
  searched.data.every((row) => row.target.type === 'space' && row.target.id === DEMO));

console.log(
  'NOT PERFORMED the carried extension of a renewal chain: the demo space has no closure left unextended (its one ' +
    'closure, id 2, was extended by #123\'s run) and no renewal that starts after today; creating them through the ' +
    'app is a write the run may not make. Proven by T-C1–T-C4 (extension.api.test.ts).',
);
console.log(`     writes: ${writes.join(' ')}`);
console.log(failures === 0 ? 'ALL PASS' : `${failures} FAILED`);
process.exit(failures === 0 ? 0 : 1);
