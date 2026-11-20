// Capture directions with headless Chrome over the DevTools Protocol (Node 24, no dependencies).
// Why not `chrome --screenshot --window-size=390,...`: headless Chrome will not lay a window out narrower
// than 500px, so a 390 capture is really a 500px page cropped. Device-metrics emulation gives a true 390.
// The viewport is set to the page's measured height and captured as a viewport (never "beyond viewport"),
// so right-to-left pages are not shifted sideways.
//
//   node capture.mjs <dir> all                      the hand-over set: 8 views + 2 states x 2 widths
//   node capture.mjs <dir> 1440-ar-light 390-en-dark-wrong ...
//   node capture.mjs <dir> 1440-ar-light-from "&from=elevate"   (extra query string, optional, last: it applies to
//                                                                EVERY spec in the call, so give it its own call)
import { spawn, execFileSync } from 'node:child_process';
import { writeFileSync, mkdirSync, existsSync, unlinkSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..', '..');
const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const PROFILE = resolve(ROOT, 'work', 'chrome-profile');
const OUT = resolve(ROOT, 'work', 'captures');
const PORT = 9333;
const MIN_H = { 1440: 900, 1024: 768, 768: 1024, 390: 844 };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const ALL = [];
for (const w of [1440, 390]) for (const l of ['ar', 'en']) for (const t of ['light', 'dark']) ALL.push(`${w}-${l}-${t}`);
for (const w of [1440, 390]) for (const s of ['wrong', 'submitting']) ALL.push(`${w}-ar-light-${s}`);

function freeGB() {
  try {
    const kb = execFileSync('powershell', ['-NoProfile', '-Command', '(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory'], { encoding: 'utf8' });
    return parseInt(kb, 10) / 1024 / 1024;
  } catch { return 99; }
}
async function waitMemory() {
  for (let i = 0; i < 6; i++) {
    const g = freeGB();
    if (g >= 4) return;
    console.log(`  free memory ${g.toFixed(1)} GB < 4 GB, waiting a minute`);
    await sleep(60000);
  }
}

async function launch() {
  await waitMemory();
  const proc = spawn(CHROME, ['--headless=new', '--disable-gpu', '--hide-scrollbars', `--user-data-dir=${PROFILE}`,
    `--remote-debugging-port=${PORT}`, '--window-size=1440,900', 'about:blank'], { stdio: 'ignore' });
  for (let i = 0; i < 60; i++) {
    try {
      const list = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
      const page = list.find((t) => t.type === 'page');
      if (page) return { proc, wsUrl: page.webSocketDebuggerUrl };
    } catch { /* not up yet */ }
    await sleep(250);
  }
  proc.kill(); throw new Error('Chrome did not start');
}

function client(wsUrl) {
  const ws = new WebSocket(wsUrl);
  let id = 0; const pending = new Map(); const waiters = [];
  ws.onmessage = (ev) => {
    const msg = JSON.parse(ev.data);
    if (msg.id && pending.has(msg.id)) { const { res, rej } = pending.get(msg.id); pending.delete(msg.id); msg.error ? rej(new Error(msg.error.message)) : res(msg.result); }
    else if (msg.method) for (const w of waiters.slice()) if (w.method === msg.method) { waiters.splice(waiters.indexOf(w), 1); w.res(msg.params); }
  };
  const ready = new Promise((r, j) => { ws.onopen = r; ws.onerror = j; });
  return {
    ready,
    send: (method, params = {}) => new Promise((res, rej) => { const i = ++id; pending.set(i, { res, rej }); ws.send(JSON.stringify({ id: i, method, params })); }),
    once: (method, timeout = 20000) => new Promise((res) => { const w = { method, res }; waiters.push(w); setTimeout(() => res(null), timeout); }),
    close: () => ws.close(),
  };
}

function urlFor(dir, lang, theme, state, extra) {
  const q = `lang=${lang}&theme=${theme}&capture=1` + (state ? `&state=${state}` : '') + (extra || '');
  return pathToFileURL(resolve(ROOT, 'work', dir, 'index.html')).href + '?' + q;
}

async function captureOne(c, dir, spec, extra) {
  const [w, lang, theme, state] = spec.split('-');
  const width = parseInt(w, 10), mobile = width < 600, h0 = MIN_H[width] || 900;
  await c.send('Emulation.setDeviceMetricsOverride', { width, height: h0, deviceScaleFactor: 1, mobile });
  await c.send('Emulation.setTouchEmulationEnabled', { enabled: mobile });
  const loaded = c.once('Page.loadEventFired');
  await c.send('Page.navigate', { url: urlFor(dir, lang, theme, state, extra) });
  await loaded;
  await c.send('Runtime.evaluate', { expression: 'document.fonts.ready.then(() => new Promise(r => setTimeout(r, 700)))', awaitPromise: true });
  const { result } = await c.send('Runtime.evaluate', { expression: 'Math.ceil(document.documentElement.scrollHeight)', returnByValue: true });
  const h = Math.max(h0, result.value || h0);
  if (h !== h0) {
    await c.send('Emulation.setDeviceMetricsOverride', { width, height: h, deviceScaleFactor: 1, mobile });
    await c.send('Runtime.evaluate', { expression: 'new Promise(r => setTimeout(r, 500))', awaitPromise: true });
  }
  // ZOOM="x,y,w,h,scale" writes a magnified detail to the scratch folder instead (for close inspection only)
  const zoom = process.env.ZOOM ? process.env.ZOOM.split(',').map(Number) : null;
  const shot = await c.send('Page.captureScreenshot', zoom
    ? { format: 'png', clip: { x: zoom[0], y: zoom[1], width: zoom[2], height: zoom[3], scale: zoom[4] || 2 } }
    : { format: 'png', captureBeyondViewport: false });
  const dest = zoom ? resolve(process.env.ZOOM_DIR || OUT, `zoom-${dir}-${spec}.png`) : resolve(OUT, `${dir}-${spec}.png`);
  if (existsSync(dest)) unlinkSync(dest);
  writeFileSync(dest, Buffer.from(shot.data, 'base64'));
  console.log(`${dir}-${spec}.png  ${width}x${h}`);
}

const [dir, ...rest] = process.argv.slice(2);
let extra = '';
if (rest.length && rest[rest.length - 1].startsWith('&')) extra = rest.pop();
const specs = rest.length === 1 && rest[0] === 'all' ? ALL : rest;
mkdirSync(OUT, { recursive: true });

for (let attempt = 1; attempt <= 2; attempt++) {
  let chrome;
  try {
    chrome = await launch();
    const c = client(chrome.wsUrl); await c.ready;
    await c.send('Page.enable');
    for (const s of specs) await captureOne(c, dir, s, extra);
    c.close(); chrome.proc.kill();
    break;
  } catch (e) {
    console.log(`  run failed (attempt ${attempt}): ${e.message}`);
    if (chrome) chrome.proc.kill();
    if (attempt === 2) process.exitCode = 1;
    await sleep(2000);
  }
}
