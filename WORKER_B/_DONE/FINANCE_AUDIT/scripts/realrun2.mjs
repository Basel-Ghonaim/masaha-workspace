// The real run of FINANCE_AUDIT PR 2 (plan §12.6, PR 2; exec prompt §5) against the API on 3321 and masaha_b_dev.
// Self-judging: one line per case, `PASS|FAIL <case> <status> <code>`, then `ALL PASS` and exit 0, or the count
// failed and exit 1. It never prints a secret, a token, a contact value or a phone number, and keeps no /auth/ body
// (only the access token, in memory).
//
// Its writes, each put back to the value read before it: the contact (a test email and number, then the original
// values), the staleness thresholds (1 and 1 days, then the original), the new-space defaults (the auto check-out
// switched, then the original). No space is created (§12.6 names no such write: T3 proves the copy).
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';

const ENV = 'C:\\dev\\masaha\\app-b\\apps\\api\\.env';
const BASE = 'http://localhost:3321/api/v1';
const DEMO = 1;

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
/** The stored settings, as a fingerprint (md5 of each value), so nothing is printed. */
const storedPrint = () => sql(`SELECT key || ':' || md5(value::text) FROM settings ORDER BY key`).join(' ');
const auditCount = () => Number(sql('SELECT count(*) FROM audit_logs')[0]);

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
  return {
    status: response.status,
    data: json?.data,
    meta: json?.meta,
    code: json?.error?.code ?? '-',
    type: json?.error?.type,
    headers: response.headers,
  };
}

let failures = 0;
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
  const token = login.data?.accessToken;
  if (!token) {
    console.log(`FAIL sign-in ${login.status} ${login.code}`);
    process.exit(1);
  }
  return token;
}

const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);

const health = await fetch('http://localhost:3321/health').then((r) => r.json());
console.log(`${health.db === 'up' ? 'PASS' : 'FAIL'} health db ${health.db}`);
if (health.db !== 'up') failures += 1;

const demoPassword = envOf('SEED_DEMO_PASSWORD');
const owner = await signIn('demo-owner@example.com', demoPassword);
// The demo's reception account has the global role USER: the "user" of the refusals.
const user = await signIn('demo-reception@example.com', demoPassword);
const admin = await signIn(envOf('SEED_ADMIN_EMAIL'), envOf('SEED_ADMIN_PASSWORD'));

const printBefore = storedPrint();
const auditBefore = auditCount();
console.log(`     settings before: ${printBefore}`);
console.log(`     audit entries before: ${auditBefore}`);

// The admin reads each card.
const defaults = await call('GET', '/admin/settings/new-space-defaults', { token: admin });
report('admin reads the new-space defaults', defaults, { status: 200 }, () =>
  typeof defaults.data.autoCheckoutAtClosing === 'boolean' && 'visitRoundingMinutes' in defaults.data);
const staleness = await call('GET', '/admin/settings/staleness', { token: admin });
report(`admin reads the thresholds (${JSON.stringify(staleness.data)})`, staleness, { status: 200 }, () =>
  Number.isInteger(staleness.data.stalenessDays) && Number.isInteger(staleness.data.priceStalenessDays));
const contact = await call('GET', '/admin/settings/contact', { token: admin });
report(
  `admin reads the contact (email ${contact.data?.email ? 'set' : 'null'}, whatsapp ${contact.data?.whatsapp ? 'set' : 'null'})`,
  contact,
  { status: 200 },
  () => 'email' in contact.data && 'whatsapp' in contact.data,
);

// The same values again write nothing, on each card (and prove the originals round-trip before any write).
for (const [path, value] of [
  ['new-space-defaults', defaults.data],
  ['staleness', staleness.data],
  ['contact', contact.data],
]) {
  const put = await call('PUT', `/admin/settings/${path}`, { token: admin, body: value });
  report(`PUT ${path} with the same values writes nothing`, put, { status: 200 }, () =>
    same(put.data, value) && auditCount() === auditBefore && storedPrint() === printBefore);
}
if (storedPrint() !== printBefore) {
  console.log('FAIL the originals did not round-trip: no write performed');
  process.exit(1);
}

/** The newest audit entry, as the admin's log answers it (its values never printed). */
async function newestEntry() {
  const log = await call('GET', '/admin/audit-log?period=ALL&limit=1', { token: admin });
  return log.data?.[0];
}
const writes = [];

// The contact: a test email and number, then the originals back.
const TEST_CONTACT = { email: 'Realrun2@Example.com', whatsapp: '0599 000 001' };
const putContact = await call('PUT', '/admin/settings/contact', { token: admin, body: TEST_CONTACT });
writes.push('contact → test');
report('admin saves the contact: normalised, answered as saved', putContact, { status: 200 }, () =>
  putContact.data.email === 'realrun2@example.com' && putContact.data.whatsapp === '+970599000001');
const contactEntry = await newestEntry();
report('…audited on the admin\'s log, no entity id, only what changed', { status: 200, code: '-' }, { status: 200 }, () =>
  contactEntry.action === 'platformSettings.contactEdited' &&
  same(contactEntry.target, { type: 'platformSettings', id: null, name: null, nameAr: null, deleted: false }) &&
  contactEntry.space === null &&
  same(
    Object.keys(contactEntry.after).sort(),
    ['email', 'whatsapp'].filter((k) => contact.data[k] !== putContact.data[k]),
  ));
const pub = await call('GET', '/settings/public');
report('GET /settings/public (anonymous) answers the saved contact, cached 5 minutes', pub, { status: 200 }, () =>
  same(pub.data, putContact.data) && pub.headers.get('cache-control') === 'public, max-age=300');
const backContact = await call('PUT', '/admin/settings/contact', { token: admin, body: contact.data });
writes.push('contact → original');
report('admin puts the contact back', backContact, { status: 200 }, () => same(backContact.data, contact.data));
const contactLog = await call('GET', '/admin/audit-log?period=ALL&actions=platformSettings.contactEdited&limit=5', {
  token: admin,
});
report(`the admin's log shows platformSettings.contactEdited (${contactLog.meta?.totalRecords} in all)`, contactLog, { status: 200 }, () =>
  contactLog.data.length >= 2 && contactLog.data.slice(0, 2).every((row) => row.target.id === null));

// A threshold applied at once: the demo space's stale groups under 1 day.
const groupsOf = async () =>
  (await call('GET', `/admin/spaces/${DEMO}`, { token: admin })).data;
const space = await groupsOf();
const dayMs = 24 * 60 * 60 * 1000;
const expectedUnder1 = Object.entries(space.updatedAt)
  .filter(([, at]) => at !== null && Date.now() - new Date(at).getTime() > dayMs)
  .map(([group]) => group)
  .sort();
const putStale = await call('PUT', '/admin/settings/staleness', {
  token: admin,
  body: { stalenessDays: 1, priceStalenessDays: 1 },
});
writes.push('staleness → 1/1');
const under1 = await groupsOf();
report(
  `a threshold applies at once: stale groups ${JSON.stringify(space.staleGroups)} → ${JSON.stringify(under1.staleGroups)}`,
  putStale,
  { status: 200 },
  () => same([...under1.staleGroups].sort(), expectedUnder1),
);
const staleEntry = await newestEntry();
report('…audited platformSettings.stalenessEdited, only what changed', { status: 200, code: '-' }, { status: 200 }, () =>
  staleEntry.action === 'platformSettings.stalenessEdited' &&
  same(staleEntry.after, Object.fromEntries(Object.entries({ stalenessDays: 1, priceStalenessDays: 1 }).filter(([k, v]) => staleness.data[k] !== v))));
const backStale = await call('PUT', '/admin/settings/staleness', { token: admin, body: staleness.data });
writes.push('staleness → original');
const back = await groupsOf();
report('admin puts the thresholds back; the stale groups as before', backStale, { status: 200 }, () =>
  same(backStale.data, staleness.data) && same(back.staleGroups, space.staleGroups));

// The new-space defaults: one switch flipped, then the original back.
const flipped = { ...defaults.data, autoCheckoutAtClosing: !defaults.data.autoCheckoutAtClosing };
const putDefaults = await call('PUT', '/admin/settings/new-space-defaults', { token: admin, body: flipped });
writes.push('defaults → autoCheckoutAtClosing flipped');
const defaultsEntry = await newestEntry();
report('admin saves the defaults; audited with only the switch', putDefaults, { status: 200 }, () =>
  same(putDefaults.data, flipped) &&
  defaultsEntry.action === 'platformSettings.newSpaceDefaultsEdited' &&
  same(Object.keys(defaultsEntry.after), ['autoCheckoutAtClosing']));
const backDefaults = await call('PUT', '/admin/settings/new-space-defaults', { token: admin, body: defaults.data });
writes.push('defaults → original');
report('admin puts the defaults back', backDefaults, { status: 200 }, () => same(backDefaults.data, defaults.data));
console.log(
  'NOT PERFORMED a new space after a default changed: §12.6 names no space creation; proven by T3 ' +
    '(adminSettings.api.test.ts, B6 red).',
);

// The refusals.
for (const [who, token, status] of [
  ['a guest', undefined, 401],
  ['a user (the reception account, role USER)', user, 403],
  ['an owner', owner, 403],
]) {
  for (const path of ['new-space-defaults', 'staleness', 'contact']) {
    report(`${who} GET /admin/settings/${path}`, await call('GET', `/admin/settings/${path}`, { token }), { status });
    report(`${who} PUT /admin/settings/${path}`, await call('PUT', `/admin/settings/${path}`, { token, body: {} }), {
      status,
    });
  }
}

const printAfter = storedPrint();
const auditAfter = auditCount();
console.log(`     settings after: ${printAfter}`);
console.log(`     audit entries after: ${auditAfter} (+${auditAfter - auditBefore}: contact ×2, staleness ×2, defaults ×2)`);
if (printAfter !== printBefore || auditAfter - auditBefore !== 6) {
  failures += 1;
  console.log('FAIL the settings are not as before, or the run wrote other than its six entries');
}
console.log(`     writes: ${writes.join(' · ')}`);
console.log(failures === 0 ? 'ALL PASS' : `${failures} FAILED`);
process.exit(failures === 0 ? 0 : 1);
