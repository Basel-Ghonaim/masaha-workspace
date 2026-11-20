// shoot — round 3: capture and check a direction's mock-up pages in one headless Chrome.
// Run it through the grant script (a Chrome batch is heavy):
//   node C:\dev\masaha\workspace\TASKS\IDENTITY\scripts\heavy.mjs design-a node shoot.mjs --dir A [--pages home.html,spaces.html?filters=open] [--widths 390,768,1440] [--langs ar,en] [--themes light,dark] [--full] [--out shots]
// Each page is opened as file:///…/directions/<dir>/<page> with ?lang=<ar|en>&theme=<light|dark> appended (the mock-ups
// read both from the address). Writes <dir>\<out>\<page>-<w>-<lang>-<theme>.jpg (viewport; with --full also .full.jpg)
// and <dir>\<out>\report.json + report.txt: horizontal overflow, text contrast under 4.5:1 (3:1 for large text), text
// under 12 px, focusable elements without a visible focus style (sampled), images that failed, console errors.
import { spawn } from 'node:child_process';
import { mkdirSync, writeFileSync, rmSync, existsSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { tmpdir } from 'node:os';

const HERE = dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const opt = (n, d) => { const i = args.indexOf('--' + n); return i >= 0 ? args[i + 1] : d; };
const DIR = resolve(HERE, '..', 'directions', opt('dir', 'A'));
const PAGES = opt('pages', 'home.html').split(',');
const WIDTHS = opt('widths', '390,1440').split(',').map(Number);
const LANGS = opt('langs', 'ar,en').split(',');
const THEMES = opt('themes', 'light,dark').split(',');
const FULL = args.includes('--full');
const OUT = join(DIR, opt('out', 'shots'));
const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
mkdirSync(OUT, { recursive: true });

const profile = join(tmpdir(), 'r3-shoot-' + process.pid);
const PORT = 9500 + Math.floor(Math.random() * 400);
const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`, '--hide-scrollbars', '--no-first-run', '--disable-extensions', '--font-render-hinting=none', '--allow-file-access-from-files', 'about:blank'], { stdio: 'ignore' });
const cleanup = () => { try { chrome.kill(); } catch {} try { rmSync(profile, { recursive: true, force: true }); } catch {} };
process.on('exit', cleanup);
async function waitFor(fn, ms) { const t = Date.now(); while (Date.now() - t < ms) { try { const v = await fn(); if (v) return v; } catch {} await sleep(300); } throw new Error('timeout'); }
const version = await waitFor(async () => (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json(), 20000);
const ws = new WebSocket(version.webSocketDebuggerUrl);
await new Promise((r, j) => { ws.onopen = r; ws.onerror = j; });
let seq = 0; const pending = new Map(); const consoleErrors = [];
ws.onmessage = (ev) => { const m = JSON.parse(ev.data); if (m.id && pending.has(m.id)) { const { res, rej } = pending.get(m.id); pending.delete(m.id); m.error ? rej(new Error(m.error.message)) : res(m.result); } else if (m.method === 'Runtime.exceptionThrown') consoleErrors.push(cur + ': ' + (m.params.exceptionDetails?.exception?.description || m.params.exceptionDetails?.text || '').slice(0, 200)); else if (m.method === 'Log.entryAdded' && m.params.entry.level === 'error') consoleErrors.push(cur + ': ' + m.params.entry.text.slice(0, 200)); };
const send = (method, params = {}, sessionId) => new Promise((res, rej) => { const id = ++seq; pending.set(id, { res, rej }); ws.send(JSON.stringify({ id, method, params, sessionId })); });
const { targetId } = await send('Target.createTarget', { url: 'about:blank' });
const { sessionId: sid } = await send('Target.attachToTarget', { targetId, flatten: true });
await send('Page.enable', {}, sid); await send('Runtime.enable', {}, sid); await send('Log.enable', {}, sid);
const ev = (expression) => send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true }, sid).then((r) => r.result.value);
let cur = '';

const PROBE = `(() => {
  const vis=(e)=>{const r=e.getBoundingClientRect();const cs=getComputedStyle(e);return r.width>0&&r.height>0&&cs.visibility!=='hidden'&&cs.display!=='none'&&+cs.opacity>0.05};
  const cv=document.createElement('canvas');cv.width=cv.height=1;const cx=cv.getContext('2d',{willReadFrequently:true});
  const rgba=(c)=>{cx.clearRect(0,0,1,1);cx.fillStyle='rgba(0,0,0,0)';cx.fillStyle=c;cx.fillRect(0,0,1,1);const d=cx.getImageData(0,0,1,1).data;return [d[0],d[1],d[2],d[3]/255]};
  const over=(t,b)=>[0,1,2].map(i=>t[i]*t[3]+b[i]*(1-t[3])).concat(1);
  const lum=(c)=>{const f=(v)=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4)};return 0.2126*f(c[0])+0.7152*f(c[1])+0.0722*f(c[2])};
  const ratio=(a,b)=>{const x=lum(a),y=lum(b);return (Math.max(x,y)+0.05)/(Math.min(x,y)+0.05)};
  const ground=(el)=>{const layers=[];for(let e=el;e&&e.nodeType===1;e=e.parentElement){const cs=getComputedStyle(e);if(/^(IMG|PICTURE|VIDEO|CANVAS)$/.test(e.tagName)||(cs.backgroundImage&&cs.backgroundImage!=='none'&&!cs.backgroundImage.startsWith('linear-gradient')))return null;const c=rgba(cs.backgroundColor);if(c[3]>0){layers.push(c);if(c[3]>=0.999)break}}let g=[255,255,255,1];if(layers.length&&layers[layers.length-1][3]>=0.999)g=layers.pop();else{const b=rgba(getComputedStyle(document.documentElement).backgroundColor);if(b[3]>0.99)g=b}for(let k=layers.length-1;k>=0;k--)g=over(layers[k],g);return g};
  const all=[...document.body.querySelectorAll('*')].filter(vis);
  const fails=[],tiny=[];let checked=0;
  for(const el of all){const tn=[...el.childNodes].find(n=>n.nodeType===3&&n.textContent.trim());if(!tn)continue;const r=el.getBoundingClientRect();if(r.width<2||r.height<2)continue;
    const cs=getComputedStyle(el);const size=parseFloat(cs.fontSize);if(size<12)tiny.push(size+'px «'+tn.textContent.trim().slice(0,30)+'»');
    const g=ground(el);if(!g)continue;let op=1;for(let e=el;e&&e.nodeType===1;e=e.parentElement)op*=+getComputedStyle(e).opacity;
    const fg0=rgba(cs.color);const fg=over([fg0[0],fg0[1],fg0[2],fg0[3]*op],g);const large=size>=24||(size>=18.66&&+cs.fontWeight>=700);const rr=ratio(fg,g);checked++;
    if(rr<(large?3:4.5)&&!el.closest('[disabled],[aria-disabled=true]'))fails.push(rr.toFixed(2)+' «'+tn.textContent.trim().slice(0,40)+'» '+cs.color+' on rgb('+g.slice(0,3).map(Math.round)+') '+size+'px')}
  const foc=[...document.querySelectorAll('a[href],button,input,select,textarea,[tabindex]:not([tabindex="-1"])')].filter(vis);
  return {overflowX:document.documentElement.scrollWidth>document.documentElement.clientWidth+1, scrollW:document.documentElement.scrollWidth, scrollH:document.documentElement.scrollHeight, checked, fails:fails.slice(0,40), tiny:[...new Set(tiny)].slice(0,20), focusables:foc.length, brokenImgs:[...document.images].filter(i=>i.complete&&i.naturalWidth===0).map(i=>i.src.slice(-60)), lang:document.documentElement.lang, dir:document.documentElement.dir};
})()`;
// focus visibility: tab through the first N stops and compare the element's outline/box-shadow/border with and without focus
const FOCUS = `(async () => { const out=[]; const els=[...document.querySelectorAll('a[href],button,input,select,textarea,[tabindex]:not([tabindex="-1"])')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0}).slice(0,25);
  for(const e of els){const s0=getComputedStyle(e);const a=[s0.outlineStyle,s0.outlineWidth,s0.boxShadow,s0.borderColor,s0.backgroundColor].join('|');e.focus({focusVisible:true});await new Promise(r=>setTimeout(r,170));const s1=getComputedStyle(e);const b=[s1.outlineStyle,s1.outlineWidth,s1.boxShadow,s1.borderColor,s1.backgroundColor].join('|');if(document.activeElement===e&&a===b)out.push(e.tagName.toLowerCase()+' «'+(e.getAttribute('aria-label')||e.innerText||e.value||'').trim().slice(0,30)+'»');e.blur()} return out })()`;

const report = [];
for (const page of PAGES) for (const w of WIDTHS) for (const lang of LANGS) for (const theme of THEMES) {
  const [file, query] = page.split('?');
  const url = pathToFileURL(join(DIR, file)).href + '?' + (query ? query + '&' : '') + `lang=${lang}&theme=${theme}`;
  const name = page.replace(/[?=&#]/g, '_').replace(/\.html/, '') + `-${w}-${lang}-${theme}`;
  cur = name;
  try {
    const mobile = w < 768; const H = w === 390 ? 844 : w === 768 ? 1024 : 900;
    await send('Emulation.setDeviceMetricsOverride', { width: w, height: H, deviceScaleFactor: 1, mobile }, sid);
    await send('Emulation.setTouchEmulationEnabled', mobile ? { enabled: true, maxTouchPoints: 5 } : { enabled: false }, sid);
    await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-color-scheme', value: theme }] }, sid);
    await send('Page.navigate', { url: 'about:blank' }, sid); await sleep(120);
    await send('Page.navigate', { url }, sid); await sleep(1400);
    await ev(`document.fonts.ready.then(()=>new Promise(r=>setTimeout(r,500)))`);
    await ev(`new Promise(res=>{const t0=Date.now();const k=()=>{const im=[...document.images].filter(i=>{const r=i.getBoundingClientRect();return r.bottom>0&&r.top<innerHeight});if(im.every(i=>i.complete)||Date.now()-t0>6000)res(1);else setTimeout(k,200)};k()})`);
    const vp = await send('Page.captureScreenshot', { format: 'jpeg', quality: 80 }, sid);
    writeFileSync(join(OUT, name + '.jpg'), Buffer.from(vp.data, 'base64'));
    const facts = await ev(PROBE);
    facts.unfocusedVisible = w === 1440 && theme === 'light' ? await ev(FOCUS) : undefined;
    if (FULL && facts.scrollH > H + 20) {
      await send('Emulation.setDeviceMetricsOverride', { width: w, height: Math.min(facts.scrollH, 8000), deviceScaleFactor: 1, mobile }, sid);
      await sleep(600);
      const fp = await send('Page.captureScreenshot', { format: 'jpeg', quality: 70 }, sid);
      writeFileSync(join(OUT, name + '.full.jpg'), Buffer.from(fp.data, 'base64'));
    }
    report.push({ name, ...facts });
    console.log(name, facts.overflowX ? 'OVERFLOW' : '', facts.fails.length ? facts.fails.length + ' contrast' : '', facts.tiny.length ? 'tiny' : '', facts.brokenImgs.length ? 'broken-img' : '', facts.unfocusedVisible?.length ? facts.unfocusedVisible.length + ' no-focus-style' : '');
  } catch (e) { report.push({ name, error: e.message }); console.log(name, 'FAIL', e.message); }
}
writeFileSync(join(OUT, 'report.json'), JSON.stringify({ report, consoleErrors }, null, 1));
const lines = [];
for (const r of report) { const p = []; if (r.error) p.push('ERROR ' + r.error); if (r.overflowX) p.push('OVERFLOW-X ' + r.scrollW); if (r.fails?.length) p.push('contrast: ' + r.fails.join(' | ')); if (r.tiny?.length) p.push('under 12px: ' + r.tiny.join(', ')); if (r.brokenImgs?.length) p.push('broken images: ' + r.brokenImgs.join(', ')); if (r.unfocusedVisible?.length) p.push('no visible focus: ' + r.unfocusedVisible.join(', ')); lines.push(r.name + ': ' + (p.length ? p.join(' ;; ') : 'clean')); }
lines.push('', 'console errors:', ...consoleErrors);
writeFileSync(join(OUT, 'report.txt'), lines.join('\n'));
cleanup();
process.exit(0);
