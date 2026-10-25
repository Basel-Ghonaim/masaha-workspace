// The real run of SUBSCRIPTIONS PR 1 (plan §12.6) against the API on 3321 and masaha_b_dev. Prints each case's
// status and the facts it checks — never a phone number or a secret. Run: node realrun1.mjs <password>
import { randomUUID } from 'node:crypto';

const BASE = 'http://localhost:3321/api/v1';
const password = process.argv[2];

async function call(method, path, { token, body, key } = {}) {
  const headers = { 'Content-Type': 'application/json' };
  if (token) headers.Authorization = `Bearer ${token}`;
  if (key) headers['Idempotency-Key'] = key;
  const response = await fetch(`${BASE}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });
  const json = await response.json().catch(() => null);
  return { status: response.status, json };
}

const signIn = async (email) =>
  (await call('POST', '/auth/login', { body: { email, password } })).json.data.accessToken;

const owner = await signIn('demo-owner@example.com');
const reception = await signIn('demo-reception@example.com');
const spaces = (await call('GET', '/manage/spaces', { token: reception })).json.data;
const spaceId = spaces[0].spaceId;
const base = `/manage/spaces/${spaceId}`;
const line = (label, value) => console.log(`${label}: ${value}`);

const key = randomUUID();
// A number no demo customer holds; printed only as "a fresh phone".
const phone = `+97059${String(Date.now()).slice(-7)}`;
const created = await call('POST', `${base}/customers`, {
  token: reception,
  key,
  body: { name: 'تجربة التشغيل', phone },
});
line('create (fresh key)', `${created.status} id ${created.json?.data?.id}`);
const retried = await call('POST', `${base}/customers`, {
  token: reception,
  key,
  body: { name: 'تجربة التشغيل', phone },
});
line('create (same key)', `${retried.status} id ${retried.json?.data?.id} same=${retried.json?.data?.id === created.json?.data?.id}`);
const taken = await call('POST', `${base}/customers`, {
  token: reception,
  key: randomUUID(),
  body: { name: 'آخر', phone },
});
line('create (another key, same phone)', `${taken.status} ${taken.json?.error?.code} ${JSON.stringify(taken.json?.error?.errors)}`);

const names = (r) => (r.json?.data ?? []).map((row) => `${row.name} (debt ${row.debtAgorot}, credit ${row.creditAgorot}, ${row.current?.status ?? 'none'})`);
const owes = await call('GET', `${base}/customers?payment=OWES`, { token: reception });
line('list ?payment=OWES', `${owes.status} ${JSON.stringify(names(owes))}`);
const ending = await call('GET', `${base}/customers?status=ENDING_SOON`, { token: reception });
line('list ?status=ENDING_SOON', `${ending.status} ${JSON.stringify(names(ending))}`);
const byDigits = await call('GET', `${base}/customers?q=0599000205`, { token: reception });
line('list ?q=<the number of رامي>', `${byDigits.status} ${JSON.stringify((byDigits.json?.data ?? []).map((r) => r.name))}`);

const rami = byDigits.json?.data?.[0];
const file = await call('GET', `${base}/customers/${rami?.id}`, { token: reception });
const f = file.json?.data;
line(
  'file of رامي',
  `${file.status} debt ${f?.debtAgorot} credit ${f?.creditAgorot} subscriptions ${f?.subscriptions?.length} unpaid visits ${JSON.stringify(
    (f?.unpaidVisits ?? []).map((u) => ({ visit: u.visit.id, customer: u.visit.customer?.name, charge: u.visit.charge?.amountAgorot, paid: u.paidAgorot, balance: u.balanceAgorot })),
  )}`,
);

const id = created.json?.data?.id;
const byReception = await call('POST', `${base}/customers/${id}/archive`, { token: reception });
line('archive by reception', byReception.status);
const archived = await call('POST', `${base}/customers/${id}/archive`, { token: owner });
line('archive by the owner', `${archived.status} archivedAt set=${Boolean(archived.json?.data?.archivedAt)}`);
const archivedList = await call('GET', `${base}/customers?status=ARCHIVED`, { token: reception });
line('reception ?status=ARCHIVED', archivedList.status);
const restored = await call('POST', `${base}/customers/${id}/restore`, { token: owner });
line('restore by the owner', `${restored.status} archivedAt=${restored.json?.data?.archivedAt}`);
