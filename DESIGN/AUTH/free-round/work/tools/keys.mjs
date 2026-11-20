// Keyboard check: tab through a page, list what receives focus in order, and photograph one focused control.
//   node keys.mjs <dir> [lang] [theme] [shotAfterNTabs]
import { spawn } from 'node:child_process';
import { writeFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..', '..');
const [dir, lang = 'ar', theme = 'light', shotAt = '6'] = process.argv.slice(2);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const proc = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', ['--headless=new', '--disable-gpu', '--hide-scrollbars',
  `--user-data-dir=${resolve(ROOT, 'work', 'chrome-profile')}`, '--remote-debugging-port=9334', 'about:blank'], { stdio: 'ignore' });
let ws;
for (let i = 0; i < 60 && !ws; i++) {
  try { const l = await (await fetch('http://127.0.0.1:9334/json/list')).json(); const p = l.find((t) => t.type === 'page'); if (p) ws = p.webSocketDebuggerUrl; } catch {}
  if (!ws) await sleep(250);
}
const sock = new WebSocket(ws); let id = 0; const pend = new Map();
sock.onmessage = (e) => { const m = JSON.parse(e.data); if (m.id && pend.has(m.id)) { pend.get(m.id)(m.result); pend.delete(m.id); } };
await new Promise((r) => (sock.onopen = r));
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pend.set(i, r); sock.send(JSON.stringify({ id: i, method, params })); });
await send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });
await send('Emulation.setFocusEmulationEnabled', { enabled: true });
await send('Page.enable');
await send('Page.navigate', { url: pathToFileURL(resolve(ROOT, 'work', dir, 'index.html')).href + `?lang=${lang}&theme=${theme}&capture=1` });
await sleep(2500);
const order = [];
for (let n = 1; n <= 16; n++) {
  await send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9 });
  await send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9 });
  await sleep(80);
  const { result } = await send('Runtime.evaluate', { returnByValue: true, expression: `(() => { const a = document.activeElement; const r = a.getBoundingClientRect();
    const cs = getComputedStyle(a); return (a.id || a.tagName.toLowerCase()) + ' "' + (a.getAttribute('aria-label') || a.textContent || a.placeholder || '').trim().slice(0, 28) + '" ' +
    Math.round(r.width) + 'x' + Math.round(r.height) + ' outline:' + cs.outlineStyle + ' ' + cs.outlineWidth + ' ' + cs.outlineColor; })()` });
  order.push(`${n}. ${result.value}`);
  if (String(n) === shotAt) {
    const shot = await send('Page.captureScreenshot', { format: 'png' });
    writeFileSync(resolve(process.env.SHOT_DIR || '.', `focus-${dir}-${lang}-${theme}.png`), Buffer.from(shot.data, 'base64'));
  }
}
console.log(order.join('\n'));
sock.close(); proc.kill();
