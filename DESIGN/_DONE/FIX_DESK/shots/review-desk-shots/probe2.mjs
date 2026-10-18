import { spawn } from 'node:child_process';
import { writeFileSync } from 'node:fs';
const PORT = '9367';
const BASE = 'http://127.0.0.1:5348/';
const SHOTS = 'C:/Users/basel/Downloads/review-desk-shots';
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const jobs = [
  ['Desk.html?role=reception&lang=en&theme=dark', 390, 'PROBE-desk-390-en-dark.png'],
  ['Desk.html?role=reception&dialog=checkout&pid=pv0&received=20&lang=en', 1440, 'PROBE-checkout-1440-en.png'],
  ['Customer%20file.html?id=m14&tab=pays&theme=dark', 1440, 'PROBE-file-1440-dark.png'],
];
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const chrome = spawn(CHROME, ['--headless=new', '--remote-debugging-port=' + PORT, '--user-data-dir=' + SHOTS + '/.probe2', '--hide-scrollbars', 'about:blank'], { stdio: 'ignore' });
let ws;
for (let i = 0; i < 50 && !ws; i++) {
  try {
    const t = await (await fetch('http://127.0.0.1:' + PORT + '/json/list')).json();
    const p = t.find((x) => x.type === 'page');
    if (p) ws = p.webSocketDebuggerUrl;
  } catch {}
  if (!ws) await sleep(200);
}
const sock = new WebSocket(ws);
await new Promise((r) => sock.addEventListener('open', r, { once: true }));
let id = 0; const wait = new Map(); const errors = [];
sock.addEventListener('message', (e) => {
  const m = JSON.parse(e.data);
  if (m.id && wait.has(m.id)) { wait.get(m.id)(m); wait.delete(m.id); }
  if (m.method === 'Runtime.exceptionThrown') errors.push('exc');
});
const send = (method, params = {}) => new Promise((r) => { const n = ++id; wait.set(n, r); sock.send(JSON.stringify({ id: n, method, params })); });
await send('Runtime.enable'); await send('Page.enable');
const expr = "JSON.stringify({ blank: (!document.getElementById('ds-root')) || (!document.getElementById('ds-root').children.length), docW: document.documentElement.scrollWidth, winW: window.innerWidth })";
const out = [];
for (const [u, width, shot] of jobs) {
  errors.length = 0;
  await send('Emulation.setDeviceMetricsOverride', { width, height: width === 390 ? 844 : 1000, deviceScaleFactor: 1, mobile: width === 390 });
  await send('Page.navigate', { url: BASE + u });
  await sleep(7000);
  const r = await send('Runtime.evaluate', { expression: expr, returnByValue: true });
  const v = JSON.parse(r.result.result.value);
  const s = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false });
  writeFileSync(SHOTS + '/' + shot, Buffer.from(s.result.data, 'base64'));
  out.push(u + ' @' + width + ': blank=' + v.blank + ' overflow=' + (v.docW > v.winW + 1) + ' errors=' + (errors.length ? errors.join('|') : 'none'));
}
console.log(out.join('\n'));
sock.close(); chrome.kill();
