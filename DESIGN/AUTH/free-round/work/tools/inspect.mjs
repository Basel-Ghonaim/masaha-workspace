// Evaluate an expression in a direction's page (headless Chrome over CDP) and print the result.
//   node inspect.mjs <dir> "<query string>" "<js expression>" [width]
import { spawn } from 'node:child_process';
import { resolve, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..', '..');
const [dir, query, expr, width = '1440'] = process.argv.slice(2);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const proc = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', ['--headless=new', '--disable-gpu', '--hide-scrollbars',
  `--user-data-dir=${resolve(ROOT, 'work', 'chrome-profile')}`, '--remote-debugging-port=9335', 'about:blank'], { stdio: 'ignore' });
let ws;
for (let i = 0; i < 60 && !ws; i++) {
  try { const l = await (await fetch('http://127.0.0.1:9335/json/list')).json(); const p = l.find((t) => t.type === 'page'); if (p) ws = p.webSocketDebuggerUrl; } catch {}
  if (!ws) await sleep(250);
}
const sock = new WebSocket(ws); let id = 0; const pend = new Map();
sock.onmessage = (e) => { const m = JSON.parse(e.data); if (m.id && pend.has(m.id)) { pend.get(m.id)(m.result); pend.delete(m.id); } };
await new Promise((r) => (sock.onopen = r));
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pend.set(i, r); sock.send(JSON.stringify({ id: i, method, params })); });
const w = parseInt(width, 10);
await send('Emulation.setDeviceMetricsOverride', { width: w, height: w < 600 ? 844 : 900, deviceScaleFactor: 1, mobile: w < 600 });
await send('Page.navigate', { url: pathToFileURL(resolve(ROOT, 'work', dir, 'index.html')).href + '?' + query });
await sleep(2500);
const r = await send('Runtime.evaluate', { expression: expr, returnByValue: true });
console.log(typeof r.result.value === 'string' ? r.result.value : JSON.stringify(r.result.value ?? r, null, 1));
sock.close(); proc.kill();
