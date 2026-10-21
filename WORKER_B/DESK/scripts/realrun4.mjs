// DESK PR 4's real run (plan §12.6): the API on 3321, masaha_b_dev. Reads the password from
// apps/api/.env into a variable; never prints it.
import { execFileSync } from 'node:child_process';
import { randomUUID } from 'node:crypto';
import { readFileSync } from 'node:fs';

const ENV = readFileSync('C:/dev/masaha/app-b/apps/api/.env', 'utf8');
const envOf = (name) => (ENV.match(new RegExp(`^${name}=(.*)$`, 'm')) ?? [])[1]?.trim();
const PASSWORD = envOf('SEED_DEMO_PASSWORD');
const DB_USER = new URL(envOf('DATABASE_URL')).username;
const BASE = 'http://localhost:3321';
const API = `${BASE}/api/v1`;

const sql = (query) =>
  execFileSync('docker', ['exec', 'masaha-postgres-1', 'psql', '-U', DB_USER, '-d', 'masaha_b_dev', '-tAc', query], {
    encoding: 'utf8',
  }).trim();
const say = (...line) => console.log(...line);

async function call(method, path, { token, body, headers = {} } = {}) {
  const response = await fetch(`${API}${path}`, {
    method,
    headers: {
      'content-type': 'application/json',
      ...(token ? { authorization: `Bearer ${token}` } : {}),
      ...headers,
    },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const text = await response.text();
  let json = null;
  try {
    json = JSON.parse(text);
  } catch {}
  return { status: response.status, json };
}

async function signIn(email) {
  const { status, json } = await call('POST', '/auth/login', { body: { email, password: PASSWORD } });
  if (status !== 200) throw new Error(`sign-in ${email}: ${status} ${JSON.stringify(json?.error)}`);
  return { token: json.data.accessToken, id: json.data.user.id };
}
const brief = ({ status, json }) =>
  `${status} ${json?.error ? JSON.stringify({ type: json.error.type, code: json.error.code, errors: json.error.errors }) : ''}`;

say('health', JSON.stringify(await (await fetch(`${BASE}/health`)).json()));
const owner = await signIn('demo-owner@example.com');
const reception = await signIn('demo-reception@example.com');
const spaceId = Number(sql("SELECT id FROM spaces WHERE slug = 'masaha-demo'"));
const S = `/manage/spaces/${spaceId}`;
say('space', spaceId, 'owner', owner.id, 'reception', reception.id);

// Two visits closed AUTO yesterday, 2,500 and 1,500 agorot, no customer.
const insert = (name, charge) =>
  Number(
    sql(`INSERT INTO visits (space_id, request_id, visitor_name, checked_in_at, checked_out_at, checkout_method, charge_agorot, updated_at)
         VALUES (${spaceId}, '${randomUUID()}', '${name}', now() - interval '1 day' - interval '9 hours', now() - interval '1 day', 'AUTO', ${charge}, now())
         RETURNING id`).split('\n')[0],
  );
const A = insert('Real run A', 2500);
const B = insert('Real run B', 1500);
say('visits A', A, 'B', B);

const listed = async () => {
  const r = await call('GET', `${S}/uncollected-visits?limit=50`, { token: owner.token });
  return r.json.data.map(({ visit }) => visit.id).filter((id) => id === A || id === B);
};
const pay = (body, key = randomUUID()) =>
  call('POST', `${S}/payments`, { token: reception.token, body, headers: { 'Idempotency-Key': key } });

say('1. uncollected lists', JSON.stringify(await listed()));
const r2 = await pay({ visitId: A, amountAgorot: 1000, method: 'CASH' });
say('2. pay 1000, no phone →', brief(r2));
const key = randomUUID();
const r3 = await pay({ visitId: A, amountAgorot: 1000, method: 'CASH', phone: '0599000124' }, key);
say('3. with phone →', brief(r3), 'balance', r3.json?.data?.balanceAgorot, 'customer', JSON.stringify(r3.json?.data?.visit?.customer));
const r4 = await pay({ visitId: A, amountAgorot: 1000, method: 'CASH', phone: '0599000124' }, key);
say('4. same key →', brief(r4), 'same payment', r4.json?.data?.payment?.id === r3.json?.data?.payment?.id);
const r5 = await pay({ visitId: A, amountAgorot: 2000, method: 'CASH' });
say('5. 2000, new key →', brief(r5));
const r6 = await call('PUT', `${S}/visits/${B}/customer`, { token: reception.token, body: { phone: '0599000125' } });
say('6. debt by phone B →', brief(r6), JSON.stringify(r6.json?.data?.customer));
const auditsBefore = sql('SELECT count(*) FROM audit_logs');
const r6b = await call('PUT', `${S}/visits/${B}/customer`, { token: reception.token, body: { phone: '0599000125' } });
say('6b. again →', brief(r6b), 'audit rows unchanged', sql('SELECT count(*) FROM audit_logs') === auditsBefore);
const r7 = await call('POST', `${S}/visits/${A}/write-off`, { token: reception.token, body: { reason: 'Real run' } });
say('7. write-off as reception →', brief(r7));
const r8 = await call('POST', `${S}/visits/${A}/write-off`, { token: owner.token, body: { reason: 'Real run' } });
say('8. write-off as owner →', brief(r8), JSON.stringify(r8.json?.data?.writeOff));
say('9. uncollected lists', JSON.stringify(await listed()));
const r10 = await pay({ visitId: A, amountAgorot: 500, method: 'CASH' });
say('10. pay on written-off A →', brief(r10));
const r11 = await call('DELETE', `${S}/visits/${A}/write-off`, { token: owner.token });
say('11. undo as owner →', brief(r11), 'writeOff', JSON.stringify(r11.json?.data?.writeOff), 'listed', JSON.stringify(await listed()));
const r12 = await pay({ visitId: A, amountAgorot: 1500, method: 'CASH' });
say('12. pay the rest →', brief(r12), 'balance', r12.json?.data?.balanceAgorot);
say('audit:', sql('SELECT action FROM audit_logs ORDER BY id DESC LIMIT 10').split('\n').join(', '));
