// PR 3's real-run preparation (plan §13, §14.9, the named script): three reports as demo-reception through
// POST /api/v1/spaces/:slug/reports — masaha-demo (HOURS «تجربة: الساعات»), noor-hub, a verified space of
// demo-directory-owner's (PRICES), tuffah-place, an unverified listed space (OTHER «تجربة: أخرى»).
// The password is read from apps/api/.env and never printed; no /auth/ body is kept.
import { readFileSync } from 'node:fs';

const base = 'http://localhost:3320/api/v1';
const env = readFileSync('C:/dev/masaha/app/apps/api/.env', 'utf8');
const password = /^SEED_DEMO_PASSWORD=(.*)$/m.exec(env)?.[1]?.trim().replace(/^["']|["']$/g, '');
const signIn = await fetch(`${base}/auth/login`, {
  method: 'POST',
  headers: { 'content-type': 'application/json' },
  body: JSON.stringify({ email: 'demo-reception@example.com', password }),
});
const token = (await signIn.json()).data.accessToken;
const reports = [
  ['masaha-demo', { field: 'HOURS', message: 'تجربة: الساعات' }],
  ['noor-hub', { field: 'PRICES' }],
  ['tuffah-place', { field: 'OTHER', message: 'تجربة: أخرى' }],
];
for (const [slug, body] of reports) {
  const response = await fetch(`${base}/spaces/${slug}/reports`, {
    method: 'POST',
    headers: { 'content-type': 'application/json', authorization: `Bearer ${token}` },
    body: JSON.stringify(body),
  });
  const answer = await response.json();
  console.log(`POST /spaces/${slug}/reports ${JSON.stringify(body)} → ${response.status} id ${answer.data?.id} status ${answer.data?.status}`);
}
