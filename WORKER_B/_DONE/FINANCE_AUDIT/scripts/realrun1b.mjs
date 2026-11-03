// Read-only re-judgement of realrun1's owner case (its first check matched the target, not the actor):
// the run's own entries 52–53 (space 1 hidden, shown) are MASAHA, no actor carries the admin's id, q finds them.
import { readFileSync } from 'node:fs';
const env = (n) => readFileSync('C:/dev/masaha/app-b/apps/api/.env', 'utf8').split(/\r?\n/).find((r) => r.startsWith(n + '=')).slice(n.length + 1).trim().replace(/^"(.*)"$/, '$1');
const B = 'http://localhost:3321/api/v1';
const signIn = async (email, password) => (await fetch(B + '/auth/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email, password }) }).then((r) => r.json())).data;
const owner = await signIn('demo-owner@example.com', env('SEED_DEMO_PASSWORD'));
const admin = await signIn(env('SEED_ADMIN_EMAIL'), env('SEED_ADMIN_PASSWORD'));
const get = (p) => fetch(B + p, { headers: { Authorization: 'Bearer ' + owner.accessToken } }).then(async (r) => ({ status: r.status, ...(await r.json()) }));
const log = await get('/manage/spaces/1/audit-log?limit=50');
const mine = log.data.filter((e) => [52, 53].includes(e.id));
const ok1 = log.status === 200 && mine.length === 2 && mine.every((e) => JSON.stringify(e.actor) === '{"kind":"MASAHA"}') &&
  log.data.every((e) => e.actor.id !== admin.user.id) && log.meta.actors.every((a) => a.id !== admin.user.id);
console.log(`${ok1 ? 'PASS' : 'FAIL'} the owner's log shows the demo space's two (52, 53) as MASAHA; no actor carries the admin's id ${log.status}`);
const q = await get('/manage/spaces/1/audit-log?q=' + encodeURIComponent('Demo Space') + '&limit=50');
const ok2 = q.status === 200 && [52, 53].every((id) => q.data.some((e) => e.id === id));
console.log(`${ok2 ? 'PASS' : 'FAIL'} q=Demo Space finds 52 and 53 (${q.meta.totalRecords} entries) ${q.status}`);
console.log(ok1 && ok2 ? 'ALL PASS' : 'FAILED');
process.exit(ok1 && ok2 ? 0 : 1);
