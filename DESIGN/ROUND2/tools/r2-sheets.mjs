// r2-sheets — builds contact sheets from an evidence pack, so a slice reviewer opens a few images
// instead of hundreds: one sheet per base URL and width, showing its four frames (ar/en × light/dark)
// side by side, each labelled with its frame id.
// Usage: node r2-sheets.mjs <REVIEW> [--only B03]     Output: ..\packs\<REVIEW>\sheets\<base>-<width>.png

import { spawnSync } from 'node:child_process';
import { readdirSync, readFileSync, mkdirSync, writeFileSync, rmSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { tmpdir } from 'node:os';

const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const REVIEW = process.argv[2];
const oi = process.argv.indexOf('--only'); const ONLY = oi > 0 ? process.argv[oi + 1] : null;
if (!REVIEW) { console.error('usage: node r2-sheets.mjs <REVIEW> [--only B03]'); process.exit(2); }

const PACK = resolve(dirname(fileURLToPath(import.meta.url)), '..', 'packs', REVIEW);
const FRAMES = join(PACK, 'frames'); const SHEETS = join(PACK, 'sheets');
mkdirSync(SHEETS, { recursive: true });
const tmp = join(tmpdir(), 'r2-sheets-' + REVIEW); mkdirSync(tmp, { recursive: true });

// Layout per width: frames per row and the scale each frame is drawn at.
const LAYOUT = { 390: { cols: 4, scale: 1, h: 844 }, 768: { cols: 2, scale: 0.6, h: 1024 }, 1440: { cols: 2, scale: 0.5, h: 900 } };
const ORDER = ['ar-light', 'ar-dark', 'en-light', 'en-dark'];
const GAP = 16, LABEL = 28;

const ids = readdirSync(FRAMES).filter((f) => /^B\d+-\d+-(ar|en)-(light|dark)\.png$/.test(f)).map((f) => f.slice(0, -4));
const groups = new Map();
for (const id of ids) { const [b, w] = id.split('-'); if (ONLY && b !== ONLY) continue; const k = b + '-' + w; if (!groups.has(k)) groups.set(k, []); groups.get(k).push(id); }

// A PNG's height, read from its header (bytes 20–23).
const pngHeight = (file) => readFileSync(file).readUInt32BE(20);
const FULL_SCALE = { 390: 0.5, 768: 0.3, 1440: 0.2 };

let n = 0;
const jobs = [];
for (const [key, list] of [...groups].sort()) { jobs.push([key, list, false]); jobs.push([key, list, true]); }
for (const [key, list, full] of jobs) {
  const w = Number(key.split('-')[1]); const L = LAYOUT[w]; if (!L) continue;
  // First screens: the layout above. Whole pages: four in one row, scaled down, as tall as the longest.
  const cols = full ? 4 : L.cols, scale = full ? FULL_SCALE[w] : L.scale;
  const suffix = full ? '.full.png' : '.png';
  const heights = ORDER.map((m) => list.includes(`${key}-${m}`) ? pngHeight(join(FRAMES, `${key}-${m}${suffix}`)) : 0);
  const cellW = Math.round(w * scale), cellH = Math.round((full ? Math.max(...heights) : L.h) * scale);
  const rows = Math.ceil(ORDER.length / cols);
  const W = cols * cellW + (cols + 1) * GAP, H = rows * (cellH + LABEL) + (rows + 1) * GAP;
  const cells = ORDER.map((m, i) => {
    const id = `${key}-${m}`;
    if (!list.includes(id)) return `<div class="c"><div class="l">${id} — missing</div></div>`;
    const h = full ? Math.round(heights[i] * scale) : cellH;
    return `<div class="c"><div class="l">${id}${full ? ' · whole page' : ''}</div><img style="height:${h}px" src="${pathToFileURL(join(FRAMES, id + suffix)).href}"></div>`;
  }).join('');
  const html = `<!doctype html><meta charset="utf-8"><style>
    body{margin:0;background:#777;font:600 15px/1 Arial,sans-serif}
    .g{display:grid;grid-template-columns:repeat(${cols},${cellW}px);gap:${GAP}px;padding:${GAP}px;align-items:start}
    .l{height:${LABEL}px;line-height:${LABEL}px;color:#fff}
    img{display:block;width:${cellW}px;outline:1px solid #000}
  </style><div class="g">${cells}</div>`;
  const name = key + (full ? '-full' : '');
  const page = join(tmp, name + '.html'); writeFileSync(page, html);
  const r = spawnSync(CHROME, ['--headless=new', `--user-data-dir=${join(tmp, 'profile')}`, '--hide-scrollbars', '--allow-file-access-from-files',
    `--window-size=${W},${H}`, `--screenshot=${join(SHEETS, name + '.png')}`, pathToFileURL(page).href], { stdio: 'ignore', timeout: 60000 });
  if (r.status === 0) n++; else console.log('failed: ' + name);
}
rmSync(tmp, { recursive: true, force: true });
console.log(`${REVIEW}: ${n} sheets in ${SHEETS}`);
