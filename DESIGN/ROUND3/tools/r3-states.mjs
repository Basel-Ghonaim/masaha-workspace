// r3-states — writes the review's NAMED STATES into masaha_dr_dev only, through the API on 3336 (the
// way the app itself writes them) and, for one display name, SQL. Each is listed in the summary.
//   NS1  people present at Pal Hub (space 26): two visits and two subscribers checked in by reception
//   NS2  payments today: reception 20 ₪ cash on subscription 20; the owner 50 ₪ by transfer on subscription 17
//   NS3  Pal Hub's live status set by hand to FULL until closing (the owner)
//   NS4  a long Arabic name on unverified space 19 (SQL: name_ar only)
//   NS5  a forced password change: the admin issues a temporary password to user 45; kept, never printed,
//        in the scratchpad file named by R3_EXTRA_ACCOUNTS for the pack's "forced" role
// Usage: node r3-states.mjs NS1,NS2,NS3,NS4,NS5      (each is idempotent enough to run once)
import { readFileSync, writeFileSync } from 'node:fs';
import { execSync } from 'node:child_process';
import { randomUUID } from 'node:crypto';

const API = 'http://localhost:3336/api/v1';
const ORIGIN = 'http://localhost:5336';
const env = Object.fromEntries(readFileSync('C:\\dev\\masaha\\app-dr\\apps\\api\\.env', 'utf8').split(/\r?\n/).filter((l) => /^[A-Z_]+=/.test(l)).map((l) => { const i = l.indexOf('='); return [l.slice(0, i), l.slice(i + 1).replace(/^["']|["']$/g, '')]; }));
const which = (process.argv[2] || '').split(',');
const sql = (q) => execSync(`docker exec masaha-postgres-1 psql -U masaha -d masaha_dr_dev -qAtc "${q}"`, { encoding: 'utf8' }).trim();
sql('delete from rate_limits');

async function login(email, password) {
  const r = await fetch(API + '/auth/login', { method: 'POST', headers: { 'content-type': 'application/json', origin: ORIGIN }, body: JSON.stringify({ email, password }) });
  const j = await r.json(); if (r.status !== 200) throw new Error(`sign-in ${email}: ${r.status} ${j.error?.type}`);
  return j.data.accessToken;
}
async function call(token, method, path, body, key = false) {
  const headers = { authorization: 'Bearer ' + token, origin: ORIGIN };
  if (body) headers['content-type'] = 'application/json';
  if (key) headers['idempotency-key'] = randomUUID();
  const r = await fetch(API + path, { method, headers, body: body ? JSON.stringify(body) : undefined });
  const j = r.status === 204 ? null : await r.json();
  console.log(`${method} ${path} → ${r.status}${j && !j.success ? ' ' + j.error.type + ' ' + (j.error.code || '') + ' ' + JSON.stringify(j.error.errors || {}) : ''}`);
  return j?.data;
}
const demo = env.SEED_DEMO_PASSWORD;

if (which.includes('NS1') || which.includes('NS2')) {
  const rec = await login('demo-reception@example.com', demo);
  if (which.includes('NS1')) {
    await call(rec, 'POST', '/manage/spaces/26/visits', { visitorName: 'ريم أبو عمرة' }, true);
    await call(rec, 'POST', '/manage/spaces/26/visits', { visitorName: 'Omar Saleh' }, true);
    await call(rec, 'POST', '/manage/spaces/26/check-ins', { subscriptionId: 17 }, true);
    await call(rec, 'POST', '/manage/spaces/26/check-ins', { subscriptionId: 31 }, true);
  }
  if (which.includes('NS2')) await call(rec, 'POST', '/manage/spaces/26/payments', { subscriptionId: 20, amountAgorot: 2000, method: 'CASH' }, true);
}
if (which.includes('NS2') || which.includes('NS3')) {
  const own = await login('demo-owner@example.com', demo);
  if (which.includes('NS2')) await call(own, 'POST', '/manage/spaces/26/payments', { subscriptionId: 17, amountAgorot: 5000, method: 'TRANSFER' }, true);
  if (which.includes('NS3')) await call(own, 'PUT', '/manage/spaces/26/status-override', { state: 'FULL', duration: 'UNTIL_CLOSING' });
}
if (which.includes('NS4')) {
  sql("update spaces set name_ar = 'دار النصيرات للدراسة والعمل المشترك للطلاب والخريجين' where id = 19");
  console.log('NS4: space 19 name_ar → ' + sql('select name_ar from spaces where id = 19'));
}
if (which.includes('NS5')) {
  const adm = await login(env.SEED_ADMIN_EMAIL, env.SEED_ADMIN_PASSWORD);
  const issued = await call(adm, 'POST', '/admin/users/45/temporary-password');
  if (issued?.temporaryPassword) {
    const file = process.env.R3_EXTRA_ACCOUNTS;
    writeFileSync(file, JSON.stringify({ forced: { email: 'shereen.arafat@example.com', password: issued.temporaryPassword } }));
    console.log('NS5: temporary password kept in ' + file + ' (not printed)');
  }
}
sql('delete from rate_limits');
