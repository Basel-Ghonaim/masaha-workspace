// Read-only data inventory for PAYMENTS_STEP10 PR 1's real run: sign-ins and GETs only.
// The demo password is read from apps/api/.env and never printed; no /auth/ body is kept; phones are not printed.
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
  if (!response.ok) throw new Error(`sign-in ${email}: ${response.status} ${body.error?.code}`);
  return { token: body.data.accessToken, user: { id: body.data.user.id, name: body.data.user.name, spaces: body.data.user.spaces } };
}
async function get(token, path) {
  const response = await fetch(base + path, { headers: { authorization: `Bearer ${token}` } });
  return { status: response.status, body: await response.json() };
}
const brief = (o) => JSON.stringify(o);
const row = (p) =>
  `   pay ${p.id} ${p.amountAgorot} ${p.method} ${p.receivedAt} ${p.item.kind}#${p.item.id} cust=${p.customer?.id ?? '-'}:${p.customer?.name ?? '-'} by=${p.recordedBy.id}:${p.recordedBy.name} voided=${p.voided ? `${p.voided.by.name}: ${p.voided.reason}` : '-'}`;

const owner = await signIn('demo-owner@example.com');
console.log(`=== owner id ${owner.user.id} ${owner.user.name} links ${brief(owner.user.spaces)}`);
const reception = await signIn('demo-reception@example.com');
console.log(`=== reception id ${reception.user.id} ${reception.user.name} links ${brief(reception.user.spaces)}`);

for (const { spaceId, role } of owner.user.spaces) {
  if (role !== 'OWNER') continue;
  console.log(`\n-- space ${spaceId}`);
  const today = await get(owner.token, `/manage/spaces/${spaceId}/payments?voided=INCLUDE&limit=50`);
  console.log(`today ${today.status} totals ${brief(today.body.meta?.totals)} rows=${today.body.data?.length}`);
  for (const p of today.body.data ?? []) console.log(row(p));
  const month = await get(owner.token, `/manage/spaces/${spaceId}/payments?from=2026-09-27&to=2026-10-27&voided=INCLUDE&limit=50`);
  console.log(`month ${month.status} totals ${brief(month.body.meta?.totals)} pages=${month.body.meta?.totalPages} records=${month.body.meta?.totalRecords}`);
  for (const p of month.body.data ?? []) console.log(row(p));
  const voided = await get(owner.token, `/manage/spaces/${spaceId}/payments?from=2026-07-28&to=2026-10-27&voided=ONLY&limit=50`);
  console.log(`voided (92 days) ${voided.status} records=${voided.body.meta?.totalRecords}`);
  for (const p of voided.body.data ?? []) console.log(row(p));
  const staff = await get(owner.token, `/manage/spaces/${spaceId}/staff`);
  console.log(`staff ${staff.status}: ${brief((staff.body.data ?? []).map((m) => [m.userId, m.name, m.isActive]))}`);
  const unc = await get(owner.token, `/manage/spaces/${spaceId}/uncollected-visits?page=1`);
  console.log(`uncollected ${unc.status} records=${unc.body.meta?.totalRecords}`);
  for (const u of unc.body.data ?? []) console.log(`   visit ${u.visit.id} ${u.visit.visitorName} cust=${u.visit.customerId ?? '-'} paid=${u.paidAgorot} balance=${u.balanceAgorot} writeOff=${!!u.visit.writeOff}`);
  const owes = await get(owner.token, `/manage/spaces/${spaceId}/customers?payment=OWES&limit=50`);
  console.log(`customers owing ${owes.status} records=${owes.body.meta?.totalRecords}`);
  for (const c of owes.body.data ?? []) {
    console.log(`   customer ${c.id} ${c.name} debt=${c.debtAgorot} current=${brief(c.current)}`);
    const file = await get(owner.token, `/manage/spaces/${spaceId}/customers/${c.id}`);
    for (const s of file.body.data?.subscriptions ?? []) console.log(`      sub ${s.id} «${s.name}» ${s.status} due=${s.dueAgorot} paid=${s.paidAgorot} balance=${s.balanceAgorot}`);
    for (const u of file.body.data?.unpaidVisits ?? []) console.log(`      unpaid visit ${u.visit.id} balance=${u.balanceAgorot}`);
  }
}

for (const { spaceId, role } of reception.user.spaces) {
  const mine = await get(reception.token, `/manage/spaces/${spaceId}/payments?voided=INCLUDE&limit=50`);
  console.log(`\nreception at ${spaceId} (${role}) mine ${mine.status} totals ${brief(mine.body.meta?.totals)}`);
  for (const p of mine.body.data ?? []) console.log(row(p));
  const range = await get(reception.token, `/manage/spaces/${spaceId}/payments?from=2026-10-01&to=2026-10-27`);
  console.log(`reception range → ${range.status} ${range.body.error?.code ?? ''} ${range.body.error?.type ?? ''}`);
}
