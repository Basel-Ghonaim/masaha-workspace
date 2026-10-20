// r2-pack — renders every frame of one review in a local headless Chrome and saves an evidence pack:
// for each URL × width × language × theme, a viewport PNG, a full-page PNG and a JSON of measured facts.
// No model is involved; the facts and captures are what the slice reviewers judge.
//
// Usage (from any folder):
//   node r2-pack.mjs <REVIEW> <PORT> <urls-file> [--widths 390,768,1440] [--langs ar,en] [--themes light,dark] [--tabs 4]
// e.g. node r2-pack.mjs PU-DF 5410 PU-DF.urls.txt
//
// The urls file: one prototype URL per line (relative to docs/design/prototype), without lang= or theme=;
// blank lines and lines starting with # are ignored. Output: ..\packs\<REVIEW>\ (frames\, index.md, summary.md).

import { spawn, execSync } from 'node:child_process';
import { mkdirSync, writeFileSync, readFileSync, existsSync, rmSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { tmpdir } from 'node:os';

const HERE = dirname(fileURLToPath(import.meta.url));
const WORKTREE = 'C:\\dev\\masaha\\app-design';
const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const HEIGHTS = { 390: 844, 768: 1024, 1440: 900 };
const FULL_CAP = 8000;

const args = process.argv.slice(2);
const opt = (name, dflt) => { const i = args.indexOf('--' + name); return i >= 0 ? args[i + 1] : dflt; };
const [REVIEW, PORT, URLS_FILE] = args;
if (!REVIEW || !PORT || !URLS_FILE) { console.error('usage: node r2-pack.mjs <REVIEW> <PORT> <urls-file> [options]'); process.exit(2); }
const WIDTHS = opt('widths', '390,768,1440').split(',').map(Number);
const LANGS = opt('langs', 'ar,en').split(',');
const THEMES = opt('themes', 'light,dark').split(',');
const TABS = Number(opt('tabs', '4'));
const ONLY = opt('only', null); // e.g. B03 — re-render one base URL

const OUT = resolve(HERE, '..', 'packs', REVIEW);
const FRAMES = join(OUT, 'frames');
mkdirSync(FRAMES, { recursive: true });

const bases = readFileSync(resolve(HERE, URLS_FILE), 'utf8').split(/\r?\n/).map((l) => l.trim()).filter((l) => l && !l.startsWith('#'));
const baseId = (i) => 'B' + String(i + 1).padStart(2, '0');
const withMode = (u, lang, theme) => {
  const [pathq, hash] = u.split('#');
  const extra = [lang === 'en' ? 'lang=en' : '', theme === 'dark' ? 'theme=dark' : ''].filter(Boolean).join('&');
  const joined = extra ? pathq + (pathq.includes('?') ? '&' : '?') + extra : pathq;
  return encodeURI(joined) + (hash ? '#' + hash : '');
};

const jobs = [];
bases.forEach((u, i) => {
  if (ONLY && baseId(i) !== ONLY) return;
  for (const w of WIDTHS) for (const lang of LANGS) for (const theme of THEMES)
    jobs.push({ base: baseId(i), url: u, w, lang, theme, id: `${baseId(i)}-${w}-${lang}-${theme}` });
});

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// ---- the prototype server and Chrome ----
const server = spawn('python', ['-m', 'http.server', PORT, '--bind', '127.0.0.1', '--directory', 'docs/design/prototype'], { cwd: WORKTREE, stdio: 'ignore' });
const profile = join(tmpdir(), 'r2-pack-' + REVIEW);
if (existsSync(profile)) rmSync(profile, { recursive: true, force: true });
const DEBUG_PORT = 9300 + (Number(PORT) % 100);
const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${DEBUG_PORT}`, `--user-data-dir=${profile}`, '--hide-scrollbars', '--no-first-run', '--no-default-browser-check', '--disable-extensions', 'about:blank'], { stdio: 'ignore' });

const cleanup = () => { try { chrome.kill(); } catch {} try { server.kill(); } catch {} };
process.on('exit', cleanup);
process.on('SIGINT', () => { cleanup(); process.exit(130); });

async function waitFor(fn, ms, what) {
  const t0 = Date.now();
  while (Date.now() - t0 < ms) { try { const v = await fn(); if (v) return v; } catch {} await sleep(250); }
  throw new Error('timed out waiting for ' + what);
}

await waitFor(async () => (await fetch(`http://127.0.0.1:${PORT}/`)).ok, 15000, 'the prototype server');
const version = await waitFor(async () => (await fetch(`http://127.0.0.1:${DEBUG_PORT}/json/version`)).json(), 20000, 'Chrome');

// ---- a minimal CDP client over the browser WebSocket (flat sessions) ----
const ws = new WebSocket(version.webSocketDebuggerUrl);
await new Promise((r, j) => { ws.onopen = r; ws.onerror = j; });
let seq = 0; const pending = new Map(); const listeners = new Map();
ws.onmessage = (ev) => {
  const m = JSON.parse(ev.data);
  if (m.id && pending.has(m.id)) { const { res, rej } = pending.get(m.id); pending.delete(m.id); m.error ? rej(new Error(m.error.message)) : res(m.result); return; }
  if (m.method && m.sessionId && listeners.has(m.sessionId)) listeners.get(m.sessionId)(m.method, m.params);
};
const send = (method, params = {}, sessionId) => new Promise((res, rej) => { const id = ++seq; pending.set(id, { res, rej }); ws.send(JSON.stringify({ id, method, params, sessionId })); });

// The facts read on the rendered page. Kept plain so a text-only reviewer can judge from them.
const PROBE = `(() => {
  const vw = innerWidth, vh = innerHeight;
  const short = (s, n = 80) => (s || '').replace(/\\s+/g, ' ').trim().slice(0, n);
  const label = (el) => {
    const t = short(el.innerText || el.getAttribute('aria-label') || el.getAttribute('placeholder') || el.value || '', 60);
    return el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (t ? ' «' + t + '»' : '');
  };
  const visible = (el) => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none' && +cs.opacity !== 0; };
  const all = [...document.body.querySelectorAll('*')].filter(visible);
  const clipped = [], offscreen = [], scrollers = [];
  for (const el of all) {
    const cs = getComputedStyle(el), r = el.getBoundingClientRect();
    if (r.width <= 2 || r.height <= 2) continue; // screen-reader-only text, not a visible box
    const ox = cs.overflowX, oy = cs.overflowY;
    if (el.scrollWidth > el.clientWidth + 1 && el.clientWidth > 0) {
      if (ox === 'auto' || ox === 'scroll') scrollers.push({ el: label(el), scrollWidth: el.scrollWidth, clientWidth: el.clientWidth });
      else if (ox === 'hidden' || ox === 'clip' || cs.textOverflow === 'ellipsis') clipped.push({ el: label(el), axis: 'x', content: el.scrollWidth, box: el.clientWidth, ellipsis: cs.textOverflow === 'ellipsis' });
    }
    if (el.scrollHeight > el.clientHeight + 1 && el.clientHeight > 0 && (oy === 'hidden' || oy === 'clip') && el.children.length === 0)
      clipped.push({ el: label(el), axis: 'y', content: el.scrollHeight, box: el.clientHeight, lineClamp: cs.webkitLineClamp || null });
    if (el.children.length === 0 && (el.innerText || '').trim() && (r.right > vw + 1 || r.left < -1)) {
      let p = el.parentElement, inScroller = false;
      while (p) { const o = getComputedStyle(p).overflowX; if (o === 'auto' || o === 'scroll' || o === 'hidden' || o === 'clip') { inScroller = true; break; } p = p.parentElement; }
      if (!inScroller) offscreen.push({ el: label(el), left: Math.round(r.left), right: Math.round(r.right) });
    }
  }
  const fixed = all.filter((el) => ['fixed', 'sticky'].includes(getComputedStyle(el).position)).map((el) => { const r = el.getBoundingClientRect(); return { el: label(el), position: getComputedStyle(el).position, top: Math.round(r.top), bottom: Math.round(r.bottom), height: Math.round(r.height) }; });
  const imgs = [...document.images].filter((i) => i.complete && i.naturalWidth === 0 && i.getAttribute('src')).map((i) => i.getAttribute('src'));
  const heads = [...document.querySelectorAll('h1,h2,h3')].filter(visible).map((h) => h.tagName.toLowerCase() + ' ' + short(h.innerText, 70));
  const dialogs = [...document.querySelectorAll('[role=dialog],[role=alertdialog]')].filter(visible).map((d) => label(d));
  const toasts = [...document.querySelectorAll('[data-sonner-toast]')].map((t) => short(t.innerText, 120));
  return {
    title: document.title, htmlLang: document.documentElement.lang, dir: document.documentElement.dir,
    theme: document.documentElement.dataset.theme || 'light',
    viewport: [vw, vh], page: { scrollWidth: document.documentElement.scrollWidth, clientWidth: document.documentElement.clientWidth, scrollHeight: document.documentElement.scrollHeight },
    horizontalPageOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
    textLength: (document.body.innerText || '').trim().length,
    headings: heads, dialogs, toasts, fixedOrSticky: fixed, brokenImages: imgs,
    clipped: clipped.slice(0, 40), offscreen: offscreen.slice(0, 40), sideScrollers: scrollers.slice(0, 20),
    text: (document.body.innerText || '').replace(/\\n{3,}/g, '\\n\\n').slice(0, 6000),
  };
})()`;

async function renderOne(job) {
  const { targetId } = await send('Target.createTarget', { url: 'about:blank' });
  const { sessionId } = await send('Target.attachToTarget', { targetId, flatten: true });
  const errors = []; let inflight = 0, lastNet = Date.now(), loaded = false;
  listeners.set(sessionId, (method, p) => {
    if (method === 'Runtime.exceptionThrown') errors.push('exception: ' + (p.exceptionDetails.exception?.description || p.exceptionDetails.text).split('\n')[0]);
    else if (method === 'Runtime.consoleAPICalled' && (p.type === 'error' || p.type === 'warning') && !String(p.args[0]?.value || '').includes('in-browser Babel transformer')) errors.push(p.type + ': ' + p.args.map((a) => a.value ?? a.description ?? '').join(' ').slice(0, 300));
    else if (method === 'Log.entryAdded' && p.entry.level === 'error') errors.push('log: ' + p.entry.text.slice(0, 300));
    else if (method === 'Network.requestWillBeSent') { inflight++; lastNet = Date.now(); }
    else if (method === 'Network.loadingFinished' || method === 'Network.loadingFailed') { inflight = Math.max(0, inflight - 1); lastNet = Date.now(); if (method === 'Network.loadingFailed' && !p.canceled) errors.push('network: ' + p.errorText); }
    else if (method === 'Page.loadEventFired') loaded = true;
  });
  try {
    for (const d of ['Page', 'Runtime', 'Log', 'Network']) await send(d + '.enable', {}, sessionId);
    const h = HEIGHTS[job.w] || 900;
    await send('Emulation.setDeviceMetricsOverride', { width: job.w, height: h, deviceScaleFactor: 1, mobile: job.w < 768 }, sessionId);
    await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-color-scheme', value: job.theme === 'dark' ? 'dark' : 'light' }] }, sessionId);
    const url = `http://127.0.0.1:${PORT}/` + withMode(job.url, job.lang, job.theme);
    await send('Page.navigate', { url }, sessionId);
    const t0 = Date.now();
    while (Date.now() - t0 < 20000 && !(loaded && inflight === 0 && Date.now() - lastNet > 900)) await sleep(150);
    await sleep(700); // let React and the in-browser Babel settle
    const shot = async (file, full) => {
      if (full) {
        const { result } = await send('Runtime.evaluate', { expression: 'document.documentElement.scrollHeight', returnByValue: true }, sessionId);
        const fh = Math.min(FULL_CAP, Math.max(h, result.value));
        await send('Emulation.setDeviceMetricsOverride', { width: job.w, height: fh, deviceScaleFactor: 1, mobile: job.w < 768 }, sessionId);
        await sleep(400);
      }
      const { data } = await send('Page.captureScreenshot', { format: 'png' }, sessionId);
      writeFileSync(join(FRAMES, file), Buffer.from(data, 'base64'));
    };
    const { result } = await send('Runtime.evaluate', { expression: PROBE, returnByValue: true }, sessionId);
    await shot(job.id + '.png', false);
    await shot(job.id + '.full.png', true);
    const facts = { id: job.id, base: job.base, url, width: job.w, lang: job.lang, mode: job.theme, consoleErrors: errors, ...result.value };
    writeFileSync(join(FRAMES, job.id + '.json'), JSON.stringify(facts, null, 1));
    return facts;
  } finally {
    listeners.delete(sessionId);
    await send('Target.closeTarget', { targetId }).catch(() => {});
  }
}

const results = []; let next = 0, done = 0;
async function worker() {
  while (next < jobs.length) {
    const job = jobs[next++];
    try { results.push(await renderOne(job)); }
    catch (e) { results.push({ id: job.id, base: job.base, url: job.url, width: job.w, lang: job.lang, mode: job.theme, failed: String(e.message || e) }); }
    done++; if (done % 20 === 0 || done === jobs.length) console.log(`${done}/${jobs.length}`);
  }
}
await Promise.all(Array.from({ length: TABS }, worker));
ws.close();
cleanup();

// ---- index and summary ----
results.sort((a, b) => a.id.localeCompare(b.id));
const git = (a) => { try { return execSync('git ' + a, { cwd: WORKTREE }).toString().trim(); } catch { return '?'; } };
const idx = ['# Evidence pack — ' + REVIEW, '', `- HEAD: \`${git('rev-parse HEAD')}\``, `- origin/main: \`${git('rev-parse origin/main')}\``, `- design identical to origin/main: ${git('diff --quiet HEAD origin/main -- docs/design && echo yes') === 'yes' ? 'yes' : 'NO — stop'}`, '', `Rendered ${new Date().toISOString()} from \`${WORKTREE}\` on port ${PORT}. Each frame has \`<id>.png\` (first screen), \`<id>.full.png\` (whole page, capped at ${FULL_CAP}px) and \`<id>.json\` (facts) in \`frames\\\`.`, '', '## Base URLs', ''];
bases.forEach((u, i) => { if (!ONLY || baseId(i) === ONLY) idx.push(`- **${baseId(i)}** \`${u}\``); });
writeFileSync(join(OUT, 'index.md'), idx.join('\n') + '\n');

const sum = ['# Measured anomalies — ' + REVIEW, '', 'Only frames where the probe measured something are listed. A listed fact is a lead, not yet an issue: open the frame\'s PNG and JSON before writing one. A frame not listed had none of these measurements, but may still show a defect to the eye.', ''];
for (const r of results) {
  const lines = [];
  if (r.failed) lines.push('- render failed: ' + r.failed);
  else {
    if (r.consoleErrors.length) lines.push('- console: ' + r.consoleErrors.slice(0, 5).join(' | '));
    if (r.horizontalPageOverflow) lines.push(`- page scrolls sideways: scrollWidth ${r.page.scrollWidth} > ${r.page.clientWidth}`);
    if (r.textLength < 80) lines.push(`- near-blank: ${r.textLength} characters of text`);
    if (r.brokenImages.length) lines.push('- broken images: ' + r.brokenImages.join(', '));
    for (const c of r.clipped) lines.push(`- clipped ${c.axis}: ${c.el} — content ${c.content}px in ${c.box}px${c.ellipsis ? ' (ellipsis)' : ''}${c.lineClamp && c.lineClamp !== 'none' ? ' (line-clamp ' + c.lineClamp + ')' : ''}`);
    for (const o of r.offscreen) lines.push(`- off the screen: ${o.el} — left ${o.left}, right ${o.right} (viewport ${r.viewport[0]})`);
  }
  if (lines.length) sum.push(`### ${r.id}`, '', '`' + (r.url || '') + '`', '', ...lines, '');
}
writeFileSync(join(OUT, 'summary.md'), sum.join('\n') + '\n');
console.log(`pack: ${OUT} — ${results.length} frames, ${results.filter((r) => r.failed).length} failed`);
