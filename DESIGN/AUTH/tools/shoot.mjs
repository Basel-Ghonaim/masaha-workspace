// shoot — the auth designs' captures (adapted from ROUND3\tools\shoot.mjs). One headless Chrome, through
// the grant script:
//   node C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs auth node shoot.mjs --job job.json
// job.json: { "base": "http://localhost:5410/", "out": "<dir>", "scale": 1|2, "full": true|false,
//   "reducedMotion": true, "probe": true,
//   "shots": [ { "name": "1-sign-in-slate-390-light", "path": "Sign in.html?v=slate&switcher=0", "width": 390,
//                "theme": "light", "lang": "ar" }, ... ] }
// The page reads ?theme= and ?lang=; the emulated colour scheme follows the theme. Writes <name>.png and,
// with probe, report.txt: horizontal overflow, text contrast under AA, text under 12 px, console errors.
import { spawn } from 'node:child_process';
import { mkdirSync, writeFileSync, readFileSync, rmSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { tmpdir } from 'node:os';

const args = process.argv.slice(2);
const opt = (n, d) => { const i = args.indexOf('--' + n); return i >= 0 ? args[i + 1] : d; };
const job = JSON.parse(readFileSync(resolve(opt('job', 'job.json')), 'utf8'));
const OUT = resolve(job.out); mkdirSync(OUT, { recursive: true });
const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const profile = join(tmpdir(), 'auth-shoot-' + process.pid);
const PORT = 9100 + Math.floor(Math.random() * 300);
const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`, '--hide-scrollbars', '--no-first-run', '--disable-extensions', '--font-render-hinting=none', 'about:blank'], { stdio: 'ignore' });
const cleanup = () => { try { chrome.kill(); } catch {} try { rmSync(profile, { recursive: true, force: true }); } catch {} };
process.on('exit', cleanup);
async function waitFor(fn, ms) { const t = Date.now(); while (Date.now() - t < ms) { try { const v = await fn(); if (v) return v; } catch {} await sleep(300); } throw new Error('timeout'); }
const version = await waitFor(async () => (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json(), 20000);
const ws = new WebSocket(version.webSocketDebuggerUrl);
await new Promise((r, j) => { ws.onopen = r; ws.onerror = j; });
let seq = 0; const pending = new Map(); const consoleErrors = []; let cur = '';
ws.onmessage = (ev) => { const m = JSON.parse(ev.data); if (m.id && pending.has(m.id)) { const { res, rej } = pending.get(m.id); pending.delete(m.id); m.error ? rej(new Error(m.error.message)) : res(m.result); } else if (m.method === 'Runtime.exceptionThrown') consoleErrors.push(cur + ': ' + (m.params.exceptionDetails?.exception?.description || m.params.exceptionDetails?.text || '').slice(0, 300)); else if (m.method === 'Log.entryAdded' && m.params.entry.level === 'error') consoleErrors.push(cur + ': ' + m.params.entry.text.slice(0, 300)); else if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') consoleErrors.push(cur + ': ' + JSON.stringify(m.params.args.map((a) => a.value || a.description)).slice(0, 300)); };
const send = (method, params = {}, sessionId) => new Promise((res, rej) => { const id = ++seq; pending.set(id, { res, rej }); ws.send(JSON.stringify({ id, method, params, sessionId })); });
const { targetId } = await send('Target.createTarget', { url: 'about:blank' });
const { sessionId: sid } = await send('Target.attachToTarget', { targetId, flatten: true });
await send('Page.enable', {}, sid); await send('Runtime.enable', {}, sid); await send('Log.enable', {}, sid);
const ev = (expression) => send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true }, sid).then((r) => r.result.value);

const PROBE = `(() => {
  const vis=(e)=>{const r=e.getBoundingClientRect();const cs=getComputedStyle(e);return r.width>0&&r.height>0&&cs.visibility!=='hidden'&&cs.display!=='none'&&+cs.opacity>0.05};
  const cv=document.createElement('canvas');cv.width=cv.height=1;const cx=cv.getContext('2d',{willReadFrequently:true});
  const rgba=(c)=>{cx.clearRect(0,0,1,1);cx.fillStyle='rgba(0,0,0,0)';cx.fillStyle=c;cx.fillRect(0,0,1,1);const d=cx.getImageData(0,0,1,1).data;return [d[0],d[1],d[2],d[3]/255]};
  const over=(t,b)=>[0,1,2].map(i=>t[i]*t[3]+b[i]*(1-t[3])).concat(1);
  const lum=(c)=>{const f=(v)=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4)};return 0.2126*f(c[0])+0.7152*f(c[1])+0.0722*f(c[2])};
  const ratio=(a,b)=>{const x=lum(a),y=lum(b);return (Math.max(x,y)+0.05)/(Math.min(x,y)+0.05)};
  const ground=(el)=>{const layers=[];for(let e=el;e&&e.nodeType===1;e=e.parentElement){const cs=getComputedStyle(e);if(/^(IMG|PICTURE|VIDEO|CANVAS)$/.test(e.tagName))return null;const c=rgba(cs.backgroundColor);if(c[3]>0){layers.push(c);if(c[3]>=0.999)break}}let g=[255,255,255,1];if(layers.length&&layers[layers.length-1][3]>=0.999)g=layers.pop();else{const b=rgba(getComputedStyle(document.body).backgroundColor);if(b[3]>0.99)g=b}for(let k=layers.length-1;k>=0;k--)g=over(layers[k],g);return g};
  const all=[...document.body.querySelectorAll('*')].filter(vis);
  const fails=[],tiny=[];
  for(const el of all){const tn=[...el.childNodes].find(n=>n.nodeType===3&&n.textContent.trim());if(!tn)continue;const r=el.getBoundingClientRect();if(r.width<2||r.height<2)continue;
    const cs=getComputedStyle(el);const size=parseFloat(cs.fontSize);if(size<12)tiny.push(size+'px «'+tn.textContent.trim().slice(0,30)+'»');
    const g=ground(el);if(!g)continue;let op=1;for(let e=el;e&&e.nodeType===1;e=e.parentElement)op*=+getComputedStyle(e).opacity;
    const fg0=rgba(cs.color);const fg=over([fg0[0],fg0[1],fg0[2],fg0[3]*op],g);const large=size>=24||(size>=18.66&&+cs.fontWeight>=700);const rr=ratio(fg,g);
    if(rr<(large?3:4.5)&&!el.closest('[disabled],[aria-disabled=true]'))fails.push(rr.toFixed(2)+' «'+tn.textContent.trim().slice(0,40)+'»')}
  const small=[...document.querySelectorAll('main a[href],main button,main input,header a[href],header button')].filter(vis).filter(e=>{const r=e.getBoundingClientRect();return r.height<24&&!e.closest('p')}).map(e=>(e.innerText||e.getAttribute('aria-label')||e.tagName).trim().slice(0,24)+' '+Math.round(e.getBoundingClientRect().height)+'px');
  const h1=document.querySelector('h1');
  return {overflowX:document.documentElement.scrollWidth>document.documentElement.clientWidth+1, scrollW:document.documentElement.scrollWidth, scrollH:document.documentElement.scrollHeight, fails:fails.slice(0,20), tiny:[...new Set(tiny)].slice(0,10), small, h1Top: h1?Math.round(h1.getBoundingClientRect().top):null, h1Size: h1?getComputedStyle(h1).fontSize:null};
})()`;

const report = [];
for (const s of job.shots) {
  const sep = s.path.includes('?') ? '&' : '?';
  const q = [s.lang === 'en' ? 'lang=en' : '', s.theme === 'dark' ? 'theme=dark' : ''].filter(Boolean).join('&');
  const url = (/^file:/.test(s.path) ? s.path : job.base + encodeURI(s.path)) + (q ? sep + q : '');
  cur = s.name;
  try {
    const mobile = s.width < 768; const H = s.height || (s.width <= 400 ? 844 : s.width < 1000 ? 1024 : s.width >= 1900 ? 1080 : 900);
    await send('Emulation.setDeviceMetricsOverride', { width: s.width, height: H, deviceScaleFactor: job.scale || 1, mobile }, sid);
    await send('Emulation.setTouchEmulationEnabled', mobile ? { enabled: true, maxTouchPoints: 5 } : { enabled: false }, sid);
    await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-color-scheme', value: s.theme || 'light' }, { name: 'prefers-reduced-motion', value: job.reducedMotion === false ? 'no-preference' : 'reduce' }] }, sid);
    await send('Page.navigate', { url: 'about:blank' }, sid); await sleep(100);
    await send('Page.navigate', { url }, sid);
    await waitFor(() => ev(`document.readyState==='complete' && !!document.querySelector('#ds-root > *, body > table, body > .lab')`), 15000).catch(() => {});
    await ev(`document.fonts.ready.then(()=>new Promise(r=>setTimeout(r,${s.settle || 700})))`);
    let full = job.full ? await ev('document.documentElement.scrollHeight') : 0;
    if (full > H + 4) { await send('Emulation.setDeviceMetricsOverride', { width: s.width, height: Math.min(full, 6000), deviceScaleFactor: job.scale || 1, mobile }, sid); await sleep(400); }
    const shot = await send('Page.captureScreenshot', { format: 'png' }, sid);
    writeFileSync(join(OUT, s.name + '.png'), Buffer.from(shot.data, 'base64'));
    if (job.probe) { const facts = await ev(PROBE); report.push({ name: s.name, url, ...facts }); }
    if (s.eval) console.log('EVAL', s.name, JSON.stringify(await ev(s.eval)));
    console.log(s.name);
  } catch (e) { report.push({ name: s.name, url, error: e.message }); console.log(s.name, 'FAIL', e.message); }
}
const lines = report.map((r) => { const p = []; if (r.error) p.push('ERROR ' + r.error); if (r.overflowX) p.push('OVERFLOW-X ' + r.scrollW); if (r.fails?.length) p.push('contrast: ' + r.fails.join(' | ')); if (r.tiny?.length) p.push('under 12px: ' + r.tiny.join(', ')); if (r.small?.length) p.push('small targets: ' + r.small.join(', ')); p.push('h1 ' + r.h1Top + 'px ' + r.h1Size); return r.name + ': ' + p.join(' ;; '); });
lines.push('', 'console errors:', ...consoleErrors);
if (job.probe) writeFileSync(join(OUT, 'report.txt'), lines.join('\n'));
console.log(consoleErrors.length ? consoleErrors.length + ' console errors' : 'no console errors');
cleanup();
process.exit(0);
