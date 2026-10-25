// The real run of ANNOUNCEMENTS PR 3 (plan §12.6, PR 3) against the API on 3321 and masaha_b_dev, on the demo
// set. Self-judging: one line per case, `PASS|FAIL <case> <status> <code>`, then `ALL PASS` and exit 0, or exit
// 1 when any case fails. It never prints a secret, a token or a phone number.
//
// Run with the API up on 3321 (npm run dev -w @masaha/api) and the demo data seeded:
//   node C:\dev\masaha\workspace\WORKER_B\ANNOUNCEMENTS\scripts\realrun3.mjs
// It writes only demo-reception's favourite of one listed space, and removes it at the end.
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
  return {
    status: response.status,
    text,
    data: json?.data,
    code: json?.error?.code ?? '-',
    cache: response.headers.get('cache-control'),
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

const login = await call('POST', '/auth/login', {
  body: { email: 'demo-reception@example.com', password: envOf('SEED_DEMO_PASSWORD') },
});
if (!login.data) {
  console.log(`FAIL sign-in ${login.status} ${login.code}`);
  process.exit(1);
}
const token = login.data.accessToken;
console.log(`     user ${login.data.user.id}, role ${login.data.user.role}`);

// The data, read first: a listed space and its location.
const before = await call('GET', '/me/favorites', { token });
console.log(`     favourites before: ${Array.isArray(before.data) ? before.data.length : '?'}`);
const list = await call('GET', '/spaces?limit=1');
const listed = list.data?.[0];
if (!listed) {
  console.log('FAIL no listed space in the demo data');
  process.exit(1);
}
const page = await call('GET', `/spaces/${listed.slug}`);
const { lat, lng } = page.data.location;
const point = `${lat.toFixed(3)},${lng.toFixed(3)}`;
console.log(`     space ${listed.id} (${listed.slug}), listed`);

const save1 = await call('POST', `/me/favorites/${listed.id}`, { token });
report('save a listed space', save1, { status: 204 });
const save2 = await call('POST', `/me/favorites/${listed.id}`, { token });
report('save it again', save2, { status: 204 });

const mine = await call('GET', '/me/favorites', { token });
report('GET /me/favorites carries its card', mine, { status: 200 }, () => {
  const found = mine.data.filter((row) => row.space.id === listed.id);
  return (
    found.length === 1 &&
    found[0].listed === true &&
    found[0].space.slug === listed.slug &&
    'liveStatus' in found[0].space &&
    !('distanceMeters' in found[0].space)
  );
});

const nearest = await call('GET', '/me/favorites?sort=distance', {
  token,
  headers: { 'Masaha-Near': point },
});
report('sort=distance with Masaha-Near: distanceMeters, no-store', nearest, { status: 200 }, () => {
  const row = nearest.data.find((item) => item.space.id === listed.id);
  return typeof row.space.distanceMeters === 'number' && nearest.cache === 'no-store';
});
console.log(`     distanceMeters ${nearest.data?.find((i) => i.space.id === listed.id)?.space.distanceMeters}`);

const unordered = await call('GET', '/me/favorites', { token, headers: { 'Masaha-Near': point } });
report('the header without sort: invalid_choice on near', unordered, { status: 422 }, () =>
  unordered.text.includes('"near":["invalid_choice"]'),
);

const unknown = await call('POST', '/me/favorites/999999', { token });
report('save an unknown id', unknown, { status: 404 });

const removed = await call('DELETE', `/me/favorites/${listed.id}`, { token });
report('remove it', removed, { status: 204 });
const after = await call('GET', '/me/favorites', { token });
report('gone from the list', after, { status: 200 }, () =>
  after.data.every((row) => row.space.id !== listed.id),
);

for (const [method, path] of [
  ['GET', '/me/favorites'],
  ['POST', `/me/favorites/${listed.id}`],
  ['DELETE', `/me/favorites/${listed.id}`],
]) {
  report(`anonymous ${method} ${path.replace(/\d+$/, ':id')}`, await call(method, path), {
    status: 401,
  });
}

if (failures === 0) {
  console.log('ALL PASS');
  process.exit(0);
}
console.log(`${failures} FAILED`);
process.exit(1);
