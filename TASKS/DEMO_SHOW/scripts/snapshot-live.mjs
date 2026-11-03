// Snapshots the live site's spaces (public GETs only) into live-spaces.json, and downloads each
// space's live cover (its page-size photo) into live-covers/<slug>.webp. Read-only.
import { mkdir, writeFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const BASE = 'https://masaha-omega.vercel.app/api/v1';

async function get(path) {
  const res = await fetch(BASE + path, { headers: { accept: 'application/json' } });
  if (!res.ok) throw new Error(`GET ${path}: ${res.status}`);
  const body = await res.json();
  if (!body.success) throw new Error(`GET ${path}: not success`);
  return body;
}

const list = await get('/spaces?limit=50');
const spaces = [];
for (const card of list.data) {
  const page = await get(`/spaces/${encodeURIComponent(card.slug)}`);
  spaces.push({ card, page: page.data });
}
await writeFile(
  join(here, 'live-spaces.json'),
  JSON.stringify({ takenAt: new Date().toISOString(), spaces }, null, 2),
);

await mkdir(join(here, 'live-covers'), { recursive: true });
for (const { card, page } of spaces) {
  const first = page.photos?.[0];
  const url = first?.page ?? first?.card ?? card.cover;
  if (!url || !url.startsWith('https://res.cloudinary.com/')) {
    console.log(`${card.slug}: no live cover`);
    continue;
  }
  const res = await fetch(url);
  if (!res.ok) throw new Error(`photo ${card.slug}: ${res.status}`);
  await writeFile(join(here, 'live-covers', `${card.slug}.webp`), Buffer.from(await res.arrayBuffer()));
  console.log(`${card.slug}: ${page.photos?.length ?? 0} photo(s), cover saved`);
}
console.log(`${spaces.length} spaces`);
