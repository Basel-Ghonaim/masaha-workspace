// Check 5.k: for each site page's chunk, the chunks it reaches by static imports, and whether
// data-table, calendar, leaflet or the dashboard are among them. Usage: node check5k.mjs <apps/web/dist>
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

const dist = process.argv[2];
const manifest = JSON.parse(readFileSync(join(dist, '.vite', 'manifest.json'), 'utf8'));
const reach = (key, seen = new Set()) => {
  if (seen.has(key)) return seen;
  seen.add(key);
  for (const next of manifest[key]?.imports ?? []) reach(next, seen);
  return seen;
};
const pages = Object.keys(manifest).filter((key) => /pages\/site\/.*Page\.tsx$|SiteLayout\.tsx$|AccountLayout\.tsx$/.test(key));
for (const page of pages) {
  const names = [...reach(page)].map((key) => manifest[key].name ?? key);
  const heavy = names.filter((name) => /data-table|calendar|leaflet|dashboard/.test(name));
  const own = manifest[page].file;
  console.log(`${page.replace('src/pages/site/', '')} (${own}): reaches ${names.length} chunks; heavy: ${heavy.join(', ') || 'none'}`);
}
