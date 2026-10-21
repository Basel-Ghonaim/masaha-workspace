// Fix round 1's real run (read-only): the list, ?payment=OWES and رامي's file, compared with the first run.
const BASE = 'http://localhost:3321/api/v1';
const password = process.argv[2];
const call = async (path, token) => {
  const r = await fetch(`${BASE}${path}`, { headers: { Authorization: `Bearer ${token}` } });
  return { status: r.status, json: await r.json() };
};
const login = await fetch(`${BASE}/auth/login`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email: 'demo-reception@example.com', password }),
});
const token = (await login.json()).data.accessToken;
const spaceId = (await call('/manage/spaces', token)).json.data[0].spaceId;
const base = `/manage/spaces/${spaceId}`;
const rows = (r) => (r.json.data ?? []).map((x) => `${x.name} ${x.debtAgorot}/${x.creditAgorot}`);
const all = await call(`${base}/customers?limit=50`, token);
console.log(`list: ${all.status} total ${all.json.meta.totalRecords} ${JSON.stringify(rows(all))}`);
const owes = await call(`${base}/customers?payment=OWES`, token);
console.log(`?payment=OWES: ${owes.status} ${JSON.stringify(rows(owes))}`);
const rami = (await call(`${base}/customers?q=0599000205`, token)).json.data[0];
const file = await call(`${base}/customers/${rami.id}`, token);
const f = file.json.data;
console.log(`file of رامي: ${file.status} debt ${f.debtAgorot} credit ${f.creditAgorot} unpaid ${JSON.stringify(f.unpaidVisits.map((u) => [u.visit.id, u.paidAgorot, u.balanceAgorot]))}`);
