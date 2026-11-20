// r3-sheets — contact sheets from the round 3 pack (adapted from round 2's r2-sheets.mjs): per base
// state and width, its four frames (ar light, ar dark, en light, en dark) side by side, each labelled
// with its frame id; one sheet of the first screens, one of the whole pages. Rendered in one headless
// Chrome over CDP (faster than one Chrome per sheet).
// Usage (a Chrome batch: through the grant script):
//   node C:\dev\masaha\workspace\TASKS\IDENTITY\scripts\heavy.mjs dr node r3-sheets.mjs <PART> [--only ID,ID]
// Output: ..\pack\<PART>\sheets\<ID>-<width>.png and <ID>-<width>-full.png

import { spawn } from 'node:child_process';
import { readdirSync, readFileSync, mkdirSync, writeFileSync, rmSync, existsSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { tmpdir } from 'node:os';

const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const PART = process.argv[2];
const oi = process.argv.indexOf('--only'); const ONLY = oi > 0 ? process.argv[oi + 1].split(',') : null;
if (!PART) { console.error('usage: node r3-sheets.mjs <PART> [--only ID,ID]'); process.exit(2); }
const PACK = resolve(dirname(fileURLToPath(import.meta.url)), '..', 'pack', PART);
const FRAMES = join(PACK, 'frames'); const SHEETS = join(PACK, 'sheets');
mkdirSync(SHEETS, { recursive: true });
const tmp = join(tmpdir(), 'r3-sheets-' + PART); mkdirSync(tmp, { recursive: true });

const LAYOUT = { 390: { cols: 4, scale: 1, h: 844 }, 768: { cols: 2, scale: 0.6, h: 1024 }, 1440: { cols: 2, scale: 0.5, h: 900 } };
const FULL_SCALE = { 390: 0.5, 768: 0.3, 1440: 0.2 };
const ORDER = ['ar-light', 'ar-dark', 'en-light', 'en-dark'];
const GAP = 16, LABEL = 28;
const RE = /^(.+)-(390|768|1440)-(ar|en)-(light|dark)\.png$/;
const ids = readdirSync(FRAMES).filter((f) => RE.test(f)).map((f) => f.slice(0, -4));
const groups = new Map();
for (const id of ids) { const [, b, w] = RE.exec(id + '.png'); if (ONLY && !ONLY.includes(b)) continue; const k = b + '-' + w; if (!groups.has(k)) groups.set(k, { b, w: Number(w), list: [] }); groups.get(k).list.push(id); }
const pngSize = (file) => { const buf = readFileSync(file); return [buf.readUInt32BE(16), buf.readUInt32BE(20)]; };

const profile = join(tmp, 'profile');
const DEBUG_PORT = 9337;
const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${DEBUG_PORT}`, `--user-data-dir=${profile}`, '--hide-scrollbars', '--allow-file-access-from-files', '--no-first-run', 'about:blank'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const cleanup = () => { try { chrome.kill(); } catch {} };
process.on('exit', cleanup);
let version; for (let i = 0; i < 80 && !version; i++) { try { version = await (await fetch(`http://127.0.0.1:${DEBUG_PORT}/json/version`)).json(); } catch { await sleep(250); } }
const ws = new WebSocket(version.webSocketDebuggerUrl);
await new Promise((r, j) => { ws.onopen = r; ws.onerror = j; });
let seq = 0; const pending = new Map(); let loadFired = null;
ws.onmessage = (ev) => { const m = JSON.parse(ev.data); if (m.id && pending.has(m.id)) { const { res, rej } = pending.get(m.id); pending.delete(m.id); m.error ? rej(new Error(m.error.message)) : res(m.result); } else if (m.method === 'Page.loadEventFired' && loadFired) loadFired(); };
const send = (method, params = {}, sessionId) => new Promise((res, rej) => { const id = ++seq; pending.set(id, { res, rej }); ws.send(JSON.stringify({ id, method, params, sessionId })); });
const { targetId } = await send('Target.createTarget', { url: 'about:blank' });
const { sessionId } = await send('Target.attachToTarget', { targetId, flatten: true });
await send('Page.enable', {}, sessionId);

let n = 0, failed = 0;
for (const [key, { w, list }] of [...groups].sort()) {
  const L = LAYOUT[w]; if (!L) continue;
  for (const full of [false, true]) {
    const cols = full ? 4 : L.cols, scale = full ? FULL_SCALE[w] : L.scale;
    const suffix = full ? '.full.png' : '.png';
    const sizes = ORDER.map((m) => { const f = join(FRAMES, `${key}-${m}${suffix}`); return existsSync(f) ? pngSize(f) : null; });
    const cellW = Math.round(w * scale);
    const cellH = Math.round((full ? Math.max(...sizes.map((s) => (s ? s[1] : 0))) : L.h) * scale);
    const rows = Math.ceil(ORDER.length / cols);
    const W = cols * cellW + (cols + 1) * GAP, H = rows * (cellH + LABEL) + (rows + 1) * GAP;
    const cells = ORDER.map((m, i) => {
      const id = `${key}-${m}`;
      if (!sizes[i]) return `<div class="c"><div class="l">${id} — missing</div></div>`;
      const h = full ? Math.round(sizes[i][1] * scale) : cellH;
      return `<div class="c"><div class="l">${id}${full ? ' · whole page' : ''}</div><img style="height:${h}px" src="${pathToFileURL(join(FRAMES, id + suffix)).href}"></div>`;
    }).join('');
    const html = `<!doctype html><meta charset="utf-8"><style>body{margin:0;background:#777;font:600 15px/1 Arial,sans-serif}.g{display:grid;grid-template-columns:repeat(${cols},${cellW}px);gap:${GAP}px;padding:${GAP}px;align-items:start}.l{height:${LABEL}px;line-height:${LABEL}px;color:#fff}img{display:block;width:${cellW}px;outline:1px solid #000}</style><div class="g">${cells}</div>`;
    const name = key + (full ? '-full' : '');
    const page = join(tmp, name + '.html'); writeFileSync(page, html);
    try {
      await send('Emulation.setDeviceMetricsOverride', { width: W, height: Math.min(H, 16000), deviceScaleFactor: 1, mobile: false }, sessionId);
      const loaded = new Promise((r) => { loadFired = r; setTimeout(r, 15000); });
      await send('Page.navigate', { url: pathToFileURL(page).href }, sessionId);
      await loaded; await sleep(200);
      const { data } = await send('Page.captureScreenshot', { format: 'png' }, sessionId);
      writeFileSync(join(SHEETS, name + '.png'), Buffer.from(data, 'base64')); n++;
    } catch (e) { failed++; console.log('failed: ' + name + ' ' + e.message); }
  }
}
ws.close(); cleanup();
rmSync(tmp, { recursive: true, force: true });
console.log(`${PART}: ${n} sheets in ${SHEETS}${failed ? `, ${failed} failed` : ''}`);
