// Read-only data inventory for DESK_SCREENS PR 1a's real run: sign-ins and GETs only.
// The demo password is read from apps/api/.env and never printed.
import { readFileSync } from 'node:fs';

const base = 'http://localhost:3320/api/v1';
const env = readFileSync('C:/dev/masaha/app/apps/api/.env', 'utf8');
const password = /^SEED_DEMO_PASSWORD=(.*)$/m.exec(env)?.[1]?.trim().replace(/^["']|["']$/g, '');
if (!password) throw new Error('no SEED_DEMO_PASSWORD');

async function signIn(email) {
  const response = await fetch(`${base}/auth/login`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  const body = await response.json();
  if (!response.ok) throw new Error(`sign-in ${email}: ${response.status} ${JSON.stringify(body.error)}`);
  return { token: body.data.accessToken, user: body.data.user };
}

async function get(token, path) {
  const response = await fetch(base + path, { headers: { authorization: `Bearer ${token}` } });
  return { status: response.status, body: await response.json() };
}

const brief = (o) => JSON.stringify(o);

for (const email of ['demo-owner@example.com', 'demo-reception@example.com']) {
  const { token, user } = await signIn(email);
  console.log(`\n=== ${email} (id ${user.id}, role ${user.role}) links ${brief(user.spaces)}`);
  for (const { spaceId, role } of user.spaces) {
    const space = await get(token, `/manage/spaces/${spaceId}`);
    console.log(`-- space ${spaceId} (${role}) ${space.status} slug=${space.body.data?.slug} hours=${space.body.data?.hours ? 'y' : 'n'} shifts=${brief(space.body.data?.hours?.shifts?.map((s) => [s.id, s.nameAr, s.startsMinute, s.endsMinute]))}`);
    const occ = await get(token, `/manage/spaces/${spaceId}/occupancy`);
    const o = occ.body.data;
    console.log(`occupancy ${occ.status}: status=${o?.status} capacity=${o?.capacity} present=${o?.present} override=${brief(o?.override)}`);
    for (const p of o?.people ?? []) console.log(`   present ${p.kind} ${p.id} ${p.name} since ${p.since} charge=${p.chargeNowAgorot}`);
    const terms = await get(token, `/manage/spaces/${spaceId}/visit-terms`);
    console.log(`visit-terms ${terms.status}: ${brief(terms.body.data)}`);
    const unc = await get(token, `/manage/spaces/${spaceId}/uncollected-visits`);
    console.log(`uncollected ${unc.status}: total=${unc.body.meta?.totalRecords} ${brief(unc.body.data?.map((u) => [u.visit.id, u.visit.visitorName, u.balanceAgorot]))}`);
    const unp = await get(token, `/manage/spaces/${spaceId}/unpriced-visits`);
    console.log(`unpriced ${unp.status}: total=${unp.body.meta?.totalRecords} ${brief(unp.body.data?.map((u) => [u.id ?? u.visit?.id, u.visitorName ?? u.visit?.visitorName]))}`);
    const customers = [];
    for (let page = 1; ; page += 1) {
      const list = await get(token, `/manage/spaces/${spaceId}/customers?page=${page}&limit=50`);
      if (list.status !== 200) { console.log(`customers ${list.status} ${brief(list.body.error)}`); break; }
      customers.push(...list.body.data);
      if (page >= list.body.meta.totalPages) break;
    }
    console.log(`customers: ${customers.length}: ${customers.map((c) => `${c.id}:${c.name}:${c.phone}:debt${c.debtAgorot}`).join(' | ')}`);
    const pk = await get(token, `/manage/spaces/${spaceId}/packages`);
    console.log(`packages ${pk.status}: ${brief(pk.body.data?.map((p) => [p.id, p.nameAr, p.priceAgorot, p.status ?? p.isActive]))}`);
  }
}

const { token: dirToken, user: dirUser } = await signIn('demo-directory-owner@example.com');
console.log(`\n=== demo-directory-owner (id ${dirUser.id}) links: ${dirUser.spaces.length}`);
const managed = await get(dirToken, '/manage/spaces');
console.log(`GET /manage/spaces ${managed.status}: ${managed.body.data?.length}`);
for (const s of managed.body.data ?? []) {
  const occ = await get(dirToken, `/manage/spaces/${s.spaceId}/occupancy`);
  const o = occ.body.data;
  const ann = await get(dirToken, `/manage/spaces/${s.spaceId}/announcements/summary`);
  console.log(`${s.spaceId} ${s.slug} ${s.role}: status=${o?.status} capacity=${o?.capacity} present=${o?.present} override=${brief(o?.override)} announcements=${brief(ann.body.data)}`);
}
