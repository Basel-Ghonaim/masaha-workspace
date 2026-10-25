// Read-only data inventory for DESK_SCREENS PR 2's real run: sign-ins and GETs only.
// The demo password is read from apps/api/.env and never printed; phones are masked.
import { readFileSync } from 'node:fs';

const base = 'http://localhost:3320/api/v1';
const env = readFileSync('C:/dev/masaha/app/apps/api/.env', 'utf8');
const password = /^SEED_DEMO_PASSWORD=(.*)$/m.exec(env)?.[1]?.trim().replace(/^["']|["']$/g, '');
if (!password) throw new Error('no SEED_DEMO_PASSWORD');

const mask = (phone) => (phone ? `…${phone.slice(-3)}` : null);

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
    for (const p of o?.people ?? []) console.log(`   present ${p.kind} ${p.id} ${p.name} since=${p.since} customer=${p.customerId ?? '-'}`);
    const open = await get(token, `/manage/spaces/${spaceId}/check-ins?open=true`);
    console.log(`open check-ins ${open.status}: ${open.body.data?.length}`);
    for (const c of open.body.data ?? []) console.log(`   checkIn ${c.id} ${c.customer.name} sub=${c.subscription.id} ${c.subscription.status}`);
    const unc = await all(token, `/manage/spaces/${spaceId}/uncollected-visits`);
    console.log(`uncollected ${unc.status}: total=${unc.total}`);
    const customers = await all(token, `/manage/spaces/${spaceId}/customers`);
    console.log(`customers ${customers.status}: total=${customers.total}`);
    for (const c of customers.rows) {
      console.log(`   customer ${c.id} ${c.name} phone=${mask(c.phone)} debt=${c.debtAgorot} credit=${c.creditAgorot} current=${brief(c.current)}`);
      const file = await get(token, `/manage/spaces/${spaceId}/customers/${c.id}`);
      const f = file.body.data;
      console.log(`      file ${file.status}: present=${brief(f?.present)}`);
      for (const s of f?.subscriptions ?? []) {
        console.log(`      sub ${s.id} «${s.name}» ${s.status} ${s.billing} price=${s.priceAgorot} ${s.startsOn}..${s.endsOn} limits d=${s.totalDays} dpw=${s.daysPerWeek} hpd=${s.hoursPerDay} th=${s.totalHours} due=${s.dueAgorot} paid=${s.paidAgorot} balance=${s.balanceAgorot} progress=${brief(s.progress)}`);
      }
      for (const u of f?.unpaidVisits ?? []) {
        console.log(`      unpaid visit ${u.visit.id} ${u.visit.visitorName} charge=${u.visit.charge?.amountAgorot ?? null} paid=${u.paidAgorot} balance=${u.balanceAgorot}`);
      }
    }
  }
}
