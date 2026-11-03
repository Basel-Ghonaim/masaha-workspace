// The site's first download from a production build's manifest: the entry and every chunk it imports
// statically, with their bytes; and whether the space shell's chunk and the dashboard chunk import
// each other (finding 27). Usage: node firstDownload.mjs <apps/web/dist>
import { readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const dist = process.argv[2];
const manifest = JSON.parse(readFileSync(join(dist, '.vite', 'manifest.json'), 'utf8'));
const entryKey = Object.keys(manifest).find((key) => manifest[key].isEntry);
const seen = new Set();
const order = [];
(function walk(key) {
  if (seen.has(key)) return;
  seen.add(key);
  order.push(key);
  for (const next of manifest[key].imports ?? []) walk(next);
})(entryKey);

let total = 0;
for (const key of order) {
  const chunk = manifest[key];
  const files = [chunk.file, ...(chunk.css ?? [])];
  for (const file of files) {
    const bytes = statSync(join(dist, file)).size;
    total += bytes;
    console.log(`${String(bytes).padStart(9)}  ${file}  (${key})`);
  }
}
console.log(`${String(total).padStart(9)}  total, ${order.length} chunks`);
const names = order.map((key) => manifest[key].file).join(' ');
for (const word of ['leaflet', 'data-table', 'dashboard', 'directory', 'DirectoryPage', 'HomePage']) {
  console.log(`${word} in the first download: ${names.includes(word)}`);
}

// Finding 27: the space shell's chunk and the dashboard chunk.
const byFile = Object.fromEntries(Object.entries(manifest).map(([key, chunk]) => [key, chunk]));
const find = (pattern) => Object.keys(byFile).filter((key) => pattern.test(key) || pattern.test(byFile[key].file));
const shells = find(/SpaceLayout/);
const dashboards = Object.keys(byFile).filter((key) => /^_?dashboard/.test(byFile[key].name ?? '') || /dashboard-/.test(byFile[key].file));
console.log('space shell chunks:', shells.map((key) => byFile[key].file).join(', ') || 'none');
console.log('dashboard chunks:', dashboards.map((key) => byFile[key].file).join(', ') || 'none');
for (const shell of shells) {
  for (const dashboard of dashboards) {
    const a = (byFile[shell].imports ?? []).includes(dashboard);
    const b = (byFile[dashboard].imports ?? []).includes(shell);
    console.log(`${byFile[shell].file} imports ${byFile[dashboard].file}: ${a}; back: ${b}`);
  }
}
