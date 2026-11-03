// Read-only data inventory for the lead's real run (PRs 2, 3, 4a, 4b): sign-ins and GETs only.
// Passwords are read from apps/api/.env and never printed; no /auth/ body is kept; no phone is printed.
import { readFileSync } from 'node:fs';

const base = 'http://localhost:3320/api/v1';
const env = readFileSync('C:/dev/masaha/app/apps/api/.env', 'utf8');
const read = (name) => /^NAME=(.*)$/m.source.replace('NAME', name);
const value = (name) =>
  new RegExp(read(name), 'm').exec(env)?.[1]?.trim().replace(/^["']|["']$/g, '');
const demoPassword = value('SEED_DEMO_PASSWORD');
const adminEmail = value('SEED_ADMIN_EMAIL');
const adminPassword = value('SEED_ADMIN_PASSWORD');
if (!demoPassword || !adminEmail || !adminPassword) throw new Error('missing a seed variable');

async function signIn(email, password) {
  const response = await fetch(`${base}/auth/login`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  const body = await response.json();
  if (!response.ok) throw new Error(`sign-in: ${response.status} ${body.error?.code}`);
  return { token: body.data.accessToken, user: body.data.user };
}
async function get(token, path) {
  const response = await fetch(base + path, {
    headers: token ? { authorization: `Bearer ${token}` } : {},
  });
  return { status: response.status, body: await response.json() };
}
const j = (o) => JSON.stringify(o);

const owner = await signIn('demo-owner@example.com', demoPassword);
const reception = await signIn('demo-reception@example.com', demoPassword);
const dirOwner = await signIn('demo-directory-owner@example.com', demoPassword);
const admin = await signIn(adminEmail, adminPassword);
for (const [label, s] of Object.entries({ owner, reception, dirOwner, admin })) {
  console.log(`=== ${label}: id ${s.user.id} ${s.user.name} role ${s.user.role} spaces ${j(s.user.spaces)}`);
}

console.log('\n--- announcements of space 7 (owner)');
for (const state of ['running', 'upcoming', 'ended']) {
  const list = await get(owner.token, `/manage/spaces/7/announcements?state=${state}&limit=50`);
  console.log(`${state}: ${list.status} records=${list.body.meta?.totalRecords}`);
  for (const a of list.body.data ?? [])
    console.log(`   #${a.id} ${a.type} ${a.state} ${a.startsAt} → ${a.endsAt} «${a.textAr.slice(0, 40)}» en=${a.textEn ? 'yes' : 'no'} ext=${j(a.extension ?? null)}`);
}
const summary = await get(owner.token, '/manage/spaces/7/announcements/summary');
console.log(`summary ${summary.status} ${j(summary.body.data)}`);

console.log('\n--- data reports');
const spaceReports = await get(owner.token, '/manage/spaces/7/data-reports?limit=50');
console.log(`space 7: ${spaceReports.status} records=${spaceReports.body.meta?.totalRecords} ${j((spaceReports.body.data ?? []).map((r) => [r.id, r.field, r.status]))}`);
const adminReports = await get(admin.token, '/admin/data-reports?limit=50');
console.log(`admin: ${adminReports.status} records=${adminReports.body.meta?.totalRecords} ${j((adminReports.body.data ?? []).map((r) => [r.id, r.space?.slug, r.field, r.status]))}`);
const myReports = await get(reception.token, '/me/reports?limit=50');
console.log(`reception's own: ${myReports.status} records=${myReports.body.meta?.totalRecords}`);

console.log('\n--- favourites');
const fav = await get(reception.token, '/me/favorites');
console.log(`reception's favourites: ${fav.status} ${j((fav.body.data ?? []).map((f) => [f.space?.id ?? f.id, f.space?.slug ?? f.slug, f.listed ?? f.space?.listed]))}`);

console.log('\n--- the directory');
const dir = await get(null, '/spaces?limit=50');
console.log(`spaces: ${dir.status} records=${dir.body.meta?.totalRecords}`);
for (const s of dir.body.data ?? [])
  console.log(`   ${s.id} ${s.slug} verified=${s.verified ?? s.isVerified} status=${s.status?.state ?? s.liveStatus ?? j(s.status)} `);
for (const { spaceId } of dirOwner.user.spaces ?? []) {
  const sp = await get(dirOwner.token, `/manage/spaces/${spaceId}`);
  console.log(`dir-owner's space ${spaceId}: ${sp.status} ${sp.body.data?.slug} verified=${sp.body.data?.verified ?? sp.body.data?.isVerified} listed=${sp.body.data?.listed ?? sp.body.data?.isListed}`);
}
const demo = await get(null, '/spaces/masaha-demo');
console.log(`masaha-demo page: ${demo.status} keys ${Object.keys(demo.body.data ?? {}).join(',')}`);
console.log(`   announcements: ${j(demo.body.data?.announcements ?? null)}`);
