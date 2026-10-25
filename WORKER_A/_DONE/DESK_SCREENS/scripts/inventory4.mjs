// Read-only data inventory for DESK_SCREENS PR 4's real run: sign-ins and GETs only.
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
async function all(token, path, extra = '') {
  const rows = [];
  for (let page = 1; ; page += 1) {
    const r = await get(token, `${path}?page=${page}&limit=50${extra}`);
    if (r.status !== 200) return { status: r.status, rows, error: r.body.error };
    rows.push(...r.body.data);
    if (page >= (r.body.meta?.totalPages ?? 1)) return { status: 200, rows, total: r.body.meta?.totalRecords };
  }
}
const brief = (o) => JSON.stringify(o);

const filters = [
  ...['UPCOMING', 'ACTIVE', 'ENDING_SOON', 'EXPIRED', 'ARCHIVED'].map((s) => `&status=${s}`),
  ...['PACKAGE', 'CUSTOM', 'NONE'].map((k) => `&kind=${k}`),
  ...['OWES', 'CREDIT', 'SETTLED'].map((p) => `&payment=${p}`),
];

for (const email of ['demo-owner@example.com', 'demo-reception@example.com']) {
  const { token, user } = await signIn(email);
  console.log(`\n=== ${email} (id ${user.id}) links ${brief(user.spaces)}`);
  for (const { spaceId, role } of user.spaces) {
    const occ = await get(token, `/manage/spaces/${spaceId}/occupancy`);
    const o = occ.body.data;
    console.log(`-- space ${spaceId} (${role}) occupancy ${occ.status}: present=${o?.present}`);
    for (const p of o?.people ?? []) console.log(`   present ${p.kind} ${p.id} ${p.name} customer=${p.customerId ?? '-'}`);
    const pk = await get(token, `/manage/spaces/${spaceId}/packages`);
    for (const p of pk.body.data ?? []) console.log(`   package ${p.id} «${p.name}» active=${p.isActive} ${p.billing} ${p.priceAgorot} validity=${p.validityDays} audience=${p.audience} shift=${p.shiftId}`);
    const sp = await get(token, `/manage/spaces/${spaceId}`);
    console.log(`   space ${sp.status} shifts=${brief(sp.body.data?.hours?.shifts?.map((x) => [x.id, x.nameAr]))}`);
    for (const pr of sp.body.data?.prices ?? []) console.log(`   price ${pr.period} ${pr.audience} shift=${pr.shiftId} label=${pr.labelAr} ${pr.amountAgorot}`);
    const terms = await get(token, `/manage/spaces/${spaceId}/visit-terms`);
    console.log(`   terms ${terms.status} mayTypePrice=${terms.body.data?.mayTypePrice}`);
    const customers = await all(token, `/manage/spaces/${spaceId}/customers`);
    console.log(`customers ${customers.status}: total=${customers.total}`);
    for (const c of customers.rows) {
      console.log(`   customer ${c.id} ${c.name} phone=${mask(c.phone)} archived=${c.archivedAt ?? '-'} debt=${c.debtAgorot} credit=${c.creditAgorot} current=${brief(c.current)}`);
      const file = await get(token, `/manage/spaces/${spaceId}/customers/${c.id}`);
      const fd = file.body.data;
      console.log(`      file ${file.status}: present=${brief(fd?.present)}`);
      for (const s of fd?.subscriptions ?? []) {
        console.log(`      sub ${s.id} «${s.name}» ${s.status} ${s.billing} pkg=${s.packageId} price=${s.priceAgorot} ${s.startsOn}..${s.endsOn} ended=${brief(s.ended)} typed=${!!s.priceTyped} due=${s.dueAgorot} paid=${s.paidAgorot} balance=${s.balanceAgorot}`);
        const st = await get(token, `/manage/spaces/${spaceId}/subscriptions/${s.id}`);
        const sd = st.body.data;
        console.log(`         statement ${st.status}: checkIns=${sd?.checkIns?.length} open=${sd?.checkIns?.filter((x) => !x.checkedOutAt).length} auto=${sd?.checkIns?.filter((x) => x.checkoutMethod === 'AUTO').length} payments=${sd?.payments?.length} voided=${sd?.payments?.filter((p) => p.voided).length} renewal=${brief(sd?.renewal)} renewedBy=${sd?.renewedById}`);
      }
      for (const u of fd?.unpaidVisits ?? []) {
        console.log(`      unpaid visit ${u.visit.id} ${u.visit.visitorName} charge=${u.visit.charge?.amountAgorot ?? null} paid=${u.paidAgorot} balance=${u.balanceAgorot} voided=${u.payments.filter((p) => p.voided).length}`);
      }
    }
  }
}
