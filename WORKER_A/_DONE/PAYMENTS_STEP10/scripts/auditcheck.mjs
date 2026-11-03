// Read-only: space 7's audit log today, as the owner (GET only; the password from apps/api/.env, never printed).
import { readFileSync } from 'node:fs';
const base = 'http://localhost:3320/api/v1';
const env = readFileSync('C:/dev/masaha/app/apps/api/.env', 'utf8');
const password = /^SEED_DEMO_PASSWORD=(.*)$/m.exec(env)?.[1]?.trim().replace(/^["']|["']$/g, '');
const r = await fetch(`${base}/auth/login`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ email: 'demo-owner@example.com', password }) });
const token = (await r.json()).data.accessToken;
const res = await fetch(`${base}/manage/spaces/7/audit-log?from=2026-10-28&to=2026-10-28&limit=50`, { headers: { authorization: `Bearer ${token}` } });
const body = await res.json();
console.log(res.status, body.error?.code ?? '', 'records', body.meta?.totalRecords);
for (const e of (body.data ?? []).slice(0, 12)) console.log(JSON.stringify({ at: e.at ?? e.createdAt, action: e.action, entity: e.entity, after: e.after }));
