// EC4: calls each new read once on the generated year (masaha_b_test via the API on 3321), after a warm-up,
// and prints each route's wall time. The statements' own durations come from PostgreSQL's log. No /auth/ body kept.
const BASE = 'http://localhost:3321/api/v1';
async function signIn(email) {
  const r = await fetch(`${BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password: 'ec4-pass-1234' }),
  });
  if (r.status !== 200) throw new Error(`sign-in ${r.status}`);
  const token = (await r.json()).data.accessToken;
  return token;
}
const owner = await signIn('user2@example.com');
const admin = await signIn('user5000@example.com');
const routes = [
  [owner, '/manage/spaces/1/finance/income'],
  [owner, '/manage/spaces/1/finance/debts'],
  [owner, '/manage/spaces/1/finance/debts?state=CREDIT'],
  [owner, '/manage/spaces/1/finance/payers'],
  [owner, '/manage/spaces/1/finance/occupancy'],
  [owner, '/manage/spaces/1/overview'],
  [owner, '/manage/spaces/1/visits'],
  [admin, '/admin/overview'],
  [admin, '/admin/data-reports?handledBy=ADMIN'],
];
for (const pass of ['warm', 'measured']) {
  for (const [token, path] of routes) {
    const t = performance.now();
    const r = await fetch(BASE + path, { headers: { Authorization: `Bearer ${token}` } });
    await r.arrayBuffer();
    if (pass === 'measured') console.log(`${r.status} ${Math.round(performance.now() - t)} ms  ${path}`);
  }
  if (pass === 'warm') console.log('--- MEASURED FROM', new Date().toISOString());
}
