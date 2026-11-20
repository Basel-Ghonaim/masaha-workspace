// cap-before — round 3 (design lead): the "before" captures of every R3-10 page.
// Public pages from the live site (read only, paced; never submits a form); signed-in pages from app-dr (5336/3336).
// One headless Chrome. Viewport + full page (the viewport resized to the page's height: avoids the RTL shift of
// captureBeyondViewport), plus a JSON of measured facts per frame.
// Usage: node heavy.mjs design node cap-before.mjs [--only id,id] [--out dir]
import { spawn } from 'node:child_process';
import { mkdirSync, writeFileSync, readFileSync, rmSync, existsSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { tmpdir } from 'node:os';

const HERE = dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const opt = (n, d) => { const i = args.indexOf('--' + n); return i >= 0 ? args[i + 1] : d; };
const OUT = resolve(opt('out', join(HERE, '..', 'before')));
const ONLY = opt('only', null)?.split(',');
const LIVE = 'https://masaha-omega.vercel.app';
const LOCAL = 'http://localhost:5336';
const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const env = Object.fromEntries(readFileSync('C:\\dev\\masaha\\app-dr\\apps\\api\\.env', 'utf8').split(/\r?\n/).filter((l) => /^[A-Z_]+=/.test(l)).map((l) => { const i = l.indexOf('='); return [l.slice(0, i), l.slice(i + 1).replace(/^["']|["']$/g, '')]; }));

const MAIN = ['home', 'spaces', 'space', 'login', 'account'];
const PAGES = [
  { id: 'home', base: LIVE, path: '/' },
  { id: 'spaces', base: LIVE, path: '/spaces' },
  { id: 'spaces-filters', base: LIVE, path: '/spaces', widths: [390], step: 'filters' },
  { id: 'map', base: LIVE, path: '/spaces?view=map', settle: 4000 },
  { id: 'space', base: LIVE, path: '/spaces/branch-hub' },
  { id: 'space-unverified-nophoto-hours', base: LIVE, path: '/spaces/jreas-hub', themes: ['light'] },
  { id: 'about', base: LIVE, path: '/about' },
  { id: 'privacy', base: LIVE, path: '/privacy', themes: ['light'] },
  { id: 'login', base: LIVE, path: '/login' },
  { id: 'register', base: LIVE, path: '/register' },
  { id: 'forgot', base: LIVE, path: '/forgot-password' },
  { id: 'reset', base: LIVE, path: '/reset-password#token=round3-before-capture-not-a-token' },
  { id: '404', base: LIVE, path: '/this-page-does-not-exist' },
  { id: 'account', base: LOCAL, path: '/me', auth: true },
  { id: 'favorites', base: LOCAL, path: '/me/favorites', auth: true },
  { id: 'reports', base: LOCAL, path: '/me/reports', auth: true, themes: ['light'] },
  { id: 'forced-change', base: LOCAL, path: '/change-password', auth: true, forced: true },
  { id: 'home-signed-in', base: LOCAL, path: '/', auth: true, themes: ['light'] },
];
const jobs = [];
for (const p of PAGES) {
  if (ONLY && !ONLY.includes(p.id)) continue;
  for (const w of p.widths || [390, 1440]) for (const theme of p.themes || ['light', 'dark']) for (const lang of MAIN.includes(p.id) ? ['ar', 'en'] : ['ar']) jobs.push({ ...p, w, theme, lang, key: `${p.id}-${w}-${lang}-${theme}` });
}

const profile = join(tmpdir(), 'r3-before-profile');
if (existsSync(profile)) rmSync(profile, { recursive: true, force: true });
const PORT = 9400 + Math.floor(Math.random() * 400);
const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`, '--hide-scrollbars', '--no-first-run', '--disable-extensions', '--font-render-hinting=none', 'about:blank'], { stdio: 'ignore' });
process.on('exit', () => { try { chrome.kill(); } catch {} });
async function waitFor(fn, ms) { const t = Date.now(); while (Date.now() - t < ms) { try { const v = await fn(); if (v) return v; } catch {} await sleep(300); } throw new Error('timeout'); }
const version = await waitFor(async () => (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json(), 20000);
const ws = new WebSocket(version.webSocketDebuggerUrl);
await new Promise((r, j) => { ws.onopen = r; ws.onerror = j; });
let seq = 0; const pending = new Map(); let onEvent = () => {};
ws.onmessage = (ev) => { const m = JSON.parse(ev.data); if (m.id && pending.has(m.id)) { const { res, rej } = pending.get(m.id); pending.delete(m.id); m.error ? rej(new Error(m.error.message)) : res(m.result); } else if (m.method) onEvent(m); };
const send = (method, params = {}, sessionId) => new Promise((res, rej) => { const id = ++seq; pending.set(id, { res, rej }); ws.send(JSON.stringify({ id, method, params, sessionId })); });

const { browserContextId: guestCtx } = await send('Target.createBrowserContext', { disposeOnDetach: false });
const { browserContextId: userCtx } = await send('Target.createBrowserContext', { disposeOnDetach: false });
async function tab(ctx) {
  const { targetId } = await send('Target.createTarget', { url: 'about:blank', browserContextId: ctx });
  const { sessionId } = await send('Target.attachToTarget', { targetId, flatten: true });
  await send('Page.enable', {}, sessionId); await send('Runtime.enable', {}, sessionId);
  return { targetId, sessionId };
}
const ev = (sid, expression) => send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true }, sid).then((r) => r.result.value);

let signedIn = false;
async function signIn(sid) {
  await send('Page.navigate', { url: `${LOCAL}/favicon.svg` }, sid); await sleep(800);
  const r = await ev(sid, `fetch('/api/v1/auth/login',{method:'POST',credentials:'include',headers:{'content-type':'application/json'},body:JSON.stringify(${JSON.stringify({ email: 'demo-user@example.com', password: env.SEED_DEMO_PASSWORD })})}).then(r=>r.status)`);
  if (r !== 200) throw new Error('sign-in answered ' + r);
  signedIn = true;
}

const PROBE = `(() => {
  const all=[...document.body.querySelectorAll('*')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&getComputedStyle(e).visibility!=='hidden'});
  const count=(f)=>{const m=new Map();for(const e of all){const v=f(e);if(v)m.set(v,(m.get(v)||0)+1)}return Object.fromEntries([...m].sort((a,b)=>b[1]-a[1]).slice(0,14))};
  const textEls=all.filter(e=>[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()));
  const fs=new Map();for(const e of textEls){const cs=getComputedStyle(e);const k=cs.fontSize+'/'+cs.fontWeight;fs.set(k,(fs.get(k)||0)+1)}
  const h=(s)=>{const e=document.querySelector(s);if(!e)return null;const cs=getComputedStyle(e);return {text:e.innerText.slice(0,90),size:cs.fontSize,weight:cs.fontWeight,lh:cs.lineHeight,family:cs.fontFamily.slice(0,40)}};
  return { title:document.title, url:location.href, scrollH:document.documentElement.scrollHeight, overflowX:document.documentElement.scrollWidth>document.documentElement.clientWidth,
    h1:h('h1'), h2s:[...document.querySelectorAll('h2,h3')].slice(0,12).map(e=>e.tagName+' '+getComputedStyle(e).fontSize+' «'+e.innerText.slice(0,50)+'»'),
    fontSizes:Object.fromEntries([...fs].sort((a,b)=>b[1]-a[1]).slice(0,14)),
    radii:count(e=>{const r=getComputedStyle(e).borderRadius;return r&&r!=='0px'?r:null}),
    shadows:count(e=>{const s=getComputedStyle(e).boxShadow;return s&&s!=='none'?s.slice(0,60):null}),
    borders:all.filter(e=>getComputedStyle(e).borderTopWidth!=='0px'&&getComputedStyle(e).borderTopStyle!=='none').length,
    imgs:[...document.images].filter(i=>i.getBoundingClientRect().width>0).map(i=>Math.round(i.getBoundingClientRect().width)+'x'+Math.round(i.getBoundingClientRect().height)),
    svgs:document.querySelectorAll('svg').length, buttons:document.querySelectorAll('button,a[href]').length,
    text:document.body.innerText.replace(/\\s+/g,' ').slice(0,1500) };
})()`;

const WAIT_IMGS = `new Promise(res=>{const t0=Date.now();const tick=()=>{const h=document.querySelector('h1');const imgs=[...document.images].filter(i=>{const r=i.getBoundingClientRect();return r.bottom>0&&r.top<innerHeight});const done=h&&imgs.every(i=>i.complete);if(done||Date.now()-t0>9000)setTimeout(()=>res(1),600);else setTimeout(tick,250)};tick()})`;
mkdirSync(OUT, { recursive: true });
const guest = await tab(guestCtx);
const user = await tab(userCtx);
let lastLive = 0;
const log = [];
for (const j of jobs) {
  const t = j.auth ? user : guest; const sid = t.sessionId;
  try {
    if (j.auth && !signedIn) await signIn(sid);
    if (j.base === LIVE) { const wait = 2500 - (Date.now() - lastLive); if (wait > 0) await sleep(wait); lastLive = Date.now(); }
    const mobile = j.w < 768; const H = mobile ? 844 : 900;
    await send('Emulation.setDeviceMetricsOverride', { width: j.w, height: H, deviceScaleFactor: mobile ? 2 : 1, mobile }, sid);
    await send('Emulation.setTouchEmulationEnabled', mobile ? { enabled: true, maxTouchPoints: 5 } : { enabled: false }, sid);
    await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-color-scheme', value: j.theme }] }, sid);
    const { identifier } = await send('Page.addScriptToEvaluateOnNewDocument', { source: `try{localStorage.setItem('masaha.language','${j.lang}');localStorage.setItem('masaha.theme','${j.theme}')}catch(e){}` }, sid);
    if (j.forced) {
      await send('Fetch.enable', { patterns: [{ urlPattern: '*/api/v1/auth/refresh*', requestStage: 'Response' }, { urlPattern: '*/api/v1/me', requestStage: 'Response' }] }, sid);
      onEvent = async (m) => {
        if (m.method !== 'Fetch.requestPaused' || m.sessionId !== sid) return;
        const p = m.params; try {
          const b = await send('Fetch.getResponseBody', { requestId: p.requestId }, sid);
          let body = b.base64Encoded ? Buffer.from(b.body, 'base64').toString('utf8') : b.body;
          body = body.replace('"mustChangePassword":false', '"mustChangePassword":true');
          await send('Fetch.fulfillRequest', { requestId: p.requestId, responseCode: p.responseStatusCode, responseHeaders: p.responseHeaders, body: Buffer.from(body).toString('base64') }, sid);
        } catch (e) { await send('Fetch.continueRequest', { requestId: p.requestId }, sid).catch(() => {}); }
      };
    }
    await send('Page.navigate', { url: 'about:blank' }, sid); await sleep(150);
    await send('Page.navigate', { url: j.base + j.path }, sid);
    await sleep(j.settle || 2600);
    await ev(sid, `document.fonts.ready.then(()=>1)`);
    await ev(sid, WAIT_IMGS);
    if (j.step === 'filters') {
      const ok = await ev(sid, `(()=>{const b=[...document.querySelectorAll('button')].find(b=>/الفلاتر|Filters/.test(b.innerText));if(b){b.click();return true}return false})()`);
      await sleep(900); if (!ok) log.push(j.key + ': no filters button');
    }
    // viewport
    const vp = await send('Page.captureScreenshot', { format: 'jpeg', quality: 82 }, sid);
    writeFileSync(join(OUT, j.key + '.jpg'), Buffer.from(vp.data, 'base64'));
    const facts = await ev(sid, PROBE);
    writeFileSync(join(OUT, j.key + '.json'), JSON.stringify(facts, null, 1));
    // full page by resizing (capped)
    if (!j.step && j.id !== 'map') {
      const full = Math.min(facts.scrollH || H, 7000);
      if (full > H + 20) {
        await send('Emulation.setDeviceMetricsOverride', { width: j.w, height: full, deviceScaleFactor: 1, mobile }, sid);
        await sleep(900); await ev(sid, WAIT_IMGS);
        const fp = await send('Page.captureScreenshot', { format: 'jpeg', quality: 72 }, sid);
        writeFileSync(join(OUT, j.key + '.full.jpg'), Buffer.from(fp.data, 'base64'));
      }
    }
    if (j.forced) { await send('Fetch.disable', {}, sid); onEvent = () => {}; }
    await send('Page.removeScriptToEvaluateOnNewDocument', { identifier }, sid);
    log.push(j.key + ': ok ' + facts.title + (facts.overflowX ? ' OVERFLOW-X' : ''));
    console.log(j.key, 'ok');
  } catch (e) { log.push(j.key + ': FAIL ' + e.message); console.log(j.key, 'FAIL', e.message); }
}
writeFileSync(join(OUT, '_log.txt'), log.join('\n'));
chrome.kill();
process.exit(0);
