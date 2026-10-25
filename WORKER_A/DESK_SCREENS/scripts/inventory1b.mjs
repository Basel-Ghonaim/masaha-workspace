// Read-only data inventory for DESK_SCREENS PR 1b's real run: sign-ins and GETs only.
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
async function all(token, path) {
  const rows = [];
  for (let page = 1; ; page += 1) {
    const r = await get(token, `${path}?page=${page}&limit=50`);
    if (r.status !== 200) return { status: r.status, rows, error: r.body.error };
    rows.push(...r.body.data);
    if (page >= (r.body.meta?.totalPages ?? 1)) return { status: 200, rows, total: r.body.meta?.totalRecords };
  }
}
const brief = (o) => JSON.stringify(o);

for (const email of ['demo-owner@example.com', 'demo-reception@example.com']) {
  const { token, user } = await signIn(email);
  console.log(`\n=== ${email} (id ${user.id}) links ${brief(user.spaces)}`);
  for (const { spaceId, role } of user.spaces) {
    const occ = await get(token, `/manage/spaces/${spaceId}/occupancy`);
    const o = occ.body.data;
    console.log(`-- space ${spaceId} (${role}) occupancy ${occ.status}: status=${o?.status} capacity=${o?.capacity} present=${o?.present}`);
    const terms = await get(token, `/manage/spaces/${spaceId}/visit-terms`);
    console.log(`visit-terms ${terms.status}: mayTypePrice=${terms.body.data?.mayTypePrice}`);
    const unc = await all(token, `/manage/spaces/${spaceId}/uncollected-visits`);
    console.log(`uncollected ${unc.status}: total=${unc.total}`);
    for (const u of unc.rows) {
      const v = u.visit;
      console.log(`   visit ${v.id} ${v.visitorName} method=${v.checkoutMethod} in=${v.checkedInAt} out=${v.checkedOutAt} customer=${brief(v.customer)} charge=${v.charge?.amountAgorot ?? null} paid=${u.paidAgorot} balance=${u.balanceAgorot} writeOff=${brief(v.writeOff)}`);
    }
    const unp = await all(token, `/manage/spaces/${spaceId}/unpriced-visits`);
    console.log(`unpriced ${unp.status}: total=${unp.total} ${unp.error ? brief(unp.error) : ''}`);
    for (const v of unp.rows) console.log(`   visit ${v.id} ${v.visitorName} method=${v.checkoutMethod} customer=${brief(v.customer)}`);
  }
}
