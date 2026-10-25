import { readFileSync } from 'node:fs';
const env = readFileSync('C:/dev/masaha/app-b/apps/api/.env', 'utf8').split(/\r?\n/);
const pw = env.find((l) => l.startsWith('SEED_DEMO_PASSWORD=')).slice(19).trim().replace(/^"(.*)"$/, '$1');
const B = 'http://localhost:3321/api/v1';
const login = async (email) => (await (await fetch(`${B}/auth/login`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email, password: pw }) })).json()).data?.accessToken;
const r = await login('demo-reception@example.com');
const o = await login('demo-owner@example.com');
const d = await login('demo-directory-owner@example.com');
console.log('signed in:', !!r, !!o, !!d);
const mine = (await (await fetch(`${B}/manage/spaces`, { headers: { Authorization: `Bearer ${r}` } })).json()).data;
console.log('reception spaces:', mine.map((s) => `${s.spaceId}:${s.slug}:${s.role}`).join(', '));
const s = mine[0];
const occ = await (await fetch(`${B}/spaces/${s.slug}/occupancy`)).json();
console.log('public occupancy:', JSON.stringify(occ.data ?? occ.error));
for (const st of ['RUNNING', 'UPCOMING', 'ENDED']) {
  const l = await (await fetch(`${B}/manage/spaces/${s.spaceId}/announcements?state=${st}`, { headers: { Authorization: `Bearer ${r}` } })).json();
  console.log(st, l.meta?.totalRecords, l.data?.map((a) => a.type).join(','));
}
const p = await (await fetch(`${B}/spaces/${s.slug}`)).json();
console.log('page announcements:', p.data?.announcements?.length);
