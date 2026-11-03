// Read-only: reception's favourites (GET only; the password from apps/api/.env, never printed).
import { readFileSync } from 'node:fs';
const base = 'http://localhost:3320/api/v1';
const env = readFileSync('C:/dev/masaha/app/apps/api/.env', 'utf8');
const password = /^SEED_DEMO_PASSWORD=(.*)$/m.exec(env)?.[1]?.trim().replace(/^["']|["']$/g, '');
const r = await fetch(`${base}/auth/login`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ email: 'demo-reception@example.com', password }) });
const token = (await r.json()).data.accessToken;
const fav = await (await fetch(`${base}/me/favorites`, { headers: { authorization: `Bearer ${token}` } })).json();
console.log(fav.data.map((f) => `${f.space.id} ${f.space.slug} listed=${f.listed} savedAt=${f.savedAt}`).join('\n'));
