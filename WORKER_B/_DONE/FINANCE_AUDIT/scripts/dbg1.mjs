import { readFileSync } from 'node:fs';
const env = (n) => readFileSync('C:/dev/masaha/app-b/apps/api/.env', 'utf8').split(/\r?\n/).find((r) => r.startsWith(n + '=')).slice(n.length + 1).trim().replace(/^"(.*)"$/, '$1');
const B = 'http://localhost:3321/api/v1';
const login = await fetch(B + '/auth/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email: 'demo-owner@example.com', password: env('SEED_DEMO_PASSWORD') }) }).then((r) => r.json());
const token = login.data.accessToken;
const r = await fetch(B + '/manage/spaces/1/audit-log?limit=5', { headers: { Authorization: 'Bearer ' + token } }).then((x) => x.json());
console.log(JSON.stringify(r.data.map((e) => ({ id: e.id, action: e.action, actor: e.actor, target: e.target.name }))));
console.log(JSON.stringify(r.meta.actors));
