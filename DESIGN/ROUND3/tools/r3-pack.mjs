// r3-pack — renders the real web app (app-dr, ports 5336/3336) in one headless Chrome and saves the
// review's evidence pack: for each base state × width × language × theme, a viewport PNG, a whole-page
// PNG and a JSON of measured facts. Adapted from round 2's r2-pack.mjs (the prototype) to the app:
// signed-in roles (one browser context each, signed in once through the API and reused), the language
// and theme written to localStorage before the page's own scripts run (masaha.language / masaha.theme),
// a held request (loading states) or a request answered with a failure or a 429 (CDP Fetch), and
// scripted steps (clicks, typing, keys) to open Sheets, dialogs and menus.
//
// Usage (run through the grant script — a Chrome batch is heavy):
//   node C:\dev\masaha\workspace\TASKS\IDENTITY\scripts\heavy.mjs dr node r3-pack.mjs <inventory.json>
//        [--part PU] [--only ID,ID] [--widths 390,768,1440] [--langs ar,en] [--themes light,dark] [--tabs 3]
// Output: ..\pack\<PART>\frames\<ID>-<w>-<lang>-<theme>.{png,full.png,json}, ..\pack\<PART>\run-<time>.log
//
// Never prints a secret: the passwords are read from app-dr's apps/api/.env and only sent to the API.

import { spawn, execSync } from 'node:child_process';
import { mkdirSync, writeFileSync, readFileSync, existsSync, rmSync, appendFileSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { tmpdir } from 'node:os';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROUND3 = resolve(HERE, '..');
const BASE = 'http://localhost:5336';
const API_ENV = 'C:\\dev\\masaha\\app-dr\\apps\\api\\.env';
const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const HEIGHTS = { 390: 844, 768: 1024, 1440: 900 };
const FULL_CAP = 9000;
const CLEAR_EVERY = 18; // frames between two clears of masaha_dr_dev's rate_limits rows

const args = process.argv.slice(2);
const opt = (name, dflt) => { const i = args.indexOf('--' + name); return i >= 0 ? args[i + 1] : dflt; };
const INVENTORY = args[0];
if (!INVENTORY) { console.error('usage: node r3-pack.mjs <inventory.json> [--part PU] [--only ID,ID] [options]'); process.exit(2); }
const WIDTHS = opt('widths', '390,768,1440').split(',').map(Number);
const LANGS = opt('langs', 'ar,en').split(',');
const THEMES = opt('themes', 'light,dark').split(',');
const TABS = Number(opt('tabs', '3'));
const PART = opt('part', null);
const ONLY = opt('only', null)?.split(',');
const OUT = resolve(opt('out', join(ROUND3, 'pack'))); // live checks write elsewhere (e.g. ..\live\DK)

// ---- secrets (never printed) ----
const envText = readFileSync(API_ENV, 'utf8');
const env = Object.fromEntries(envText.split(/\r?\n/).filter((l) => /^[A-Z_]+=/.test(l)).map((l) => { const i = l.indexOf('='); return [l.slice(0, i), l.slice(i + 1).replace(/^["']|["']$/g, '')]; }));
const ACCOUNTS = {
  user: { email: 'demo-user@example.com', password: env.SEED_DEMO_PASSWORD },
  owner: { email: 'demo-owner@example.com', password: env.SEED_DEMO_PASSWORD },
  reception: { email: 'demo-reception@example.com', password: env.SEED_DEMO_PASSWORD },
  admin: { email: env.SEED_ADMIN_EMAIL, password: env.SEED_ADMIN_PASSWORD },
};
// Accounts made by a named state (NS5's forced change), kept in a scratchpad file, never printed.
if (process.env.R3_EXTRA_ACCOUNTS && existsSync(process.env.R3_EXTRA_ACCOUNTS)) Object.assign(ACCOUNTS, JSON.parse(readFileSync(process.env.R3_EXTRA_ACCOUNTS, 'utf8')));

// ---- the inventory ----
const inventory = JSON.parse(readFileSync(resolve(INVENTORY), 'utf8'));
const bases = inventory.filter((b) => (!PART || b.part === PART) && (!ONLY || ONLY.includes(b.id)) && !b.skip);
const jobs = [];
for (const b of bases) {
  for (const w of b.widths || WIDTHS) {
    if (!WIDTHS.includes(w)) continue;
    for (const lang of b.langs || LANGS) for (const theme of b.themes || THEMES) {
      if (!LANGS.includes(lang) || !THEMES.includes(theme)) continue;
      jobs.push({ base: b, w, lang, theme, id: `${b.id}-${w}-${lang}-${theme}` });
    }
  }
}
// Signed-in roles last-in-group so the guest frames never wait on a sign-in; same role together.
const roleOrder = { visitor: 0, user: 1, owner: 2, reception: 3, admin: 4 };
jobs.sort((a, b) => ((roleOrder[a.base.role] ?? 5) - (roleOrder[b.base.role] ?? 5)) || 0);

const stampNow = () => new Date().toISOString().replace(/[:T]/g, '-').slice(0, 19);
const LOGDIR = join(OUT, PART || 'ALL');
mkdirSync(LOGDIR, { recursive: true });
const RUNLOG = join(LOGDIR, `run-${stampNow()}.log`);
const log = (t) => { appendFileSync(RUNLOG, `${new Date().toISOString().slice(11, 19)} ${t}\n`); };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function clearRateLimits() {
  try { execSync('docker exec masaha-postgres-1 psql -U masaha -d masaha_dr_dev -qAtc "delete from rate_limits"', { stdio: 'ignore' }); log('rate_limits cleared (masaha_dr_dev)'); }
  catch (e) { log('rate_limits clear failed: ' + String(e.message).split('\n')[0]); }
}

// ---- Chrome ----
const profile = join(tmpdir(), 'r3-pack-profile');
if (existsSync(profile)) rmSync(profile, { recursive: true, force: true });
const DEBUG_PORT = 9336;
const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${DEBUG_PORT}`, `--user-data-dir=${profile}`, '--hide-scrollbars', '--no-first-run', '--no-default-browser-check', '--disable-extensions', '--font-render-hinting=none', '--disable-features=Translate', 'about:blank'], { stdio: 'ignore' });
const cleanup = () => { try { chrome.kill(); } catch {} };
process.on('exit', cleanup);
process.on('SIGINT', () => { cleanup(); process.exit(130); });

async function waitFor(fn, ms, what) {
  const t0 = Date.now();
  while (Date.now() - t0 < ms) { try { const v = await fn(); if (v) return v; } catch {} await sleep(250); }
  throw new Error('timed out waiting for ' + what);
}
await waitFor(async () => (await fetch(`${BASE}/`)).ok, 20000, 'the web server on 5336');
const version = await waitFor(async () => (await fetch(`http://127.0.0.1:${DEBUG_PORT}/json/version`)).json(), 20000, 'Chrome');

const ws = new WebSocket(version.webSocketDebuggerUrl);
await new Promise((r, j) => { ws.onopen = r; ws.onerror = j; });
let seq = 0; const pending = new Map(); const listeners = new Map();
ws.onmessage = (ev) => {
  const m = JSON.parse(ev.data);
  if (m.id && pending.has(m.id)) { const { res, rej } = pending.get(m.id); pending.delete(m.id); m.error ? rej(new Error(m.error.message)) : res(m.result); return; }
  if (m.method && m.sessionId && listeners.has(m.sessionId)) listeners.get(m.sessionId)(m.method, m.params);
};
const send = (method, params = {}, sessionId) => new Promise((res, rej) => { const id = ++seq; pending.set(id, { res, rej }); ws.send(JSON.stringify({ id, method, params, sessionId })); });

// ---- one browser context per role, signed in once through the API ----
const contexts = {};
async function contextOf(key) {
  if (contexts[key]) return contexts[key];
  const { browserContextId } = await send('Target.createBrowserContext', { disposeOnDetach: false });
  contexts[key] = { id: browserContextId, signedIn: false, signing: null };
  // a context for "nearest to me": the location granted (its point set per tab) or refused
  if (key.endsWith(':geo:granted')) await send('Browser.grantPermissions', { permissions: ['geolocation'], origin: BASE, browserContextId });
  if (key.endsWith(':geo:denied')) await send('Browser.setPermission', { permission: { name: 'geolocation' }, setting: 'denied', origin: BASE, browserContextId });
  return contexts[key];
}
async function signIn(role, key = role) {
  const ctx = await contextOf(key);
  if (ctx.signing) return ctx.signing;
  ctx.signing = (async () => {
    const acc = ACCOUNTS[role];
    if (!acc?.password) throw new Error(`no password for ${role} in app-dr's .env`);
    const { targetId } = await send('Target.createTarget', { url: 'about:blank', browserContextId: ctx.id });
    const { sessionId } = await send('Target.attachToTarget', { targetId, flatten: true });
    try {
      await send('Page.enable', {}, sessionId);
      await send('Page.navigate', { url: `${BASE}/favicon.svg` }, sessionId);
      await sleep(800);
      const expr = `fetch('/api/v1/auth/login', { method: 'POST', credentials: 'include', headers: { 'content-type': 'application/json' }, body: JSON.stringify(${JSON.stringify({ email: acc.email, password: acc.password })}) }).then(async (r) => r.status + ' ' + ((await r.json())?.data?.user?.role || ''))`;
      const { result } = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true }, sessionId);
      if (!String(result.value).startsWith('200')) throw new Error(`sign-in of ${role} answered ${String(result.value).split(' ')[0]}`);
      ctx.signedIn = true;
      log(`signed in: ${role} (${String(result.value).split(' ')[1]})`);
    } finally {
      await send('Target.closeTarget', { targetId }).catch(() => {});
      ctx.signing = null;
    }
  })();
  return ctx.signing;
}

// ---- the facts read on the rendered page ----
const SEA = ['#eafbfc', '#d5f4f5', '#b3e6e8', '#85d0d4', '#50b3b8', '#15959b', '#02787d', '#096165', '#05494c', '#023235', '#001d1f',
  '#f4fcfe', '#eaf5f7', '#dbe6e9', '#c7d1d4', '#9da7a9', '#747e80', '#5c6567', '#464f51', '#2a3234', '#182022', '#0c1315'];
const SPARK = ['#fef3fe', '#ffe3fd', '#fac8f7', '#eba5e8', '#d27ed0', '#b55bb3', '#934791', '#773a75', '#5a2a59', '#3f1b3e', '#260d25'];
const PROBE = (phase) => `(() => {
  const SEA = ${JSON.stringify(SEA)}, SPARK = ${JSON.stringify(SPARK)};
  const vw = innerWidth, vh = innerHeight;
  const coarse = matchMedia('(pointer: coarse)').matches;
  const short = (s, n = 80) => (s || '').replace(/\\s+/g, ' ').trim().slice(0, n);
  const label = (el) => {
    const t = short(el.getAttribute('aria-label') || el.innerText || el.getAttribute('placeholder') || el.value || el.getAttribute('title') || '', 60);
    return el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (el.getAttribute('role') ? '[role=' + el.getAttribute('role') + ']' : '') + (t ? ' «' + t + '»' : '');
  };
  const cv = document.createElement('canvas'); cv.width = cv.height = 1;
  const cx = cv.getContext('2d', { willReadFrequently: true });
  const cache = new Map();
  const rgba = (css) => {
    if (!css) return [0, 0, 0, 0];
    if (cache.has(css)) return cache.get(css);
    cx.clearRect(0, 0, 1, 1); cx.fillStyle = 'rgba(0,0,0,0)'; cx.fillStyle = css; cx.fillRect(0, 0, 1, 1);
    const d = cx.getImageData(0, 0, 1, 1).data; const v = [d[0], d[1], d[2], d[3] / 255];
    cache.set(css, v); return v;
  };
  const hex = (c) => '#' + c.slice(0, 3).map((x) => Math.round(x).toString(16).padStart(2, '0')).join('');
  const near = (c, list, tol) => list.find((h) => { const r = parseInt(h.slice(1, 3), 16), g = parseInt(h.slice(3, 5), 16), b = parseInt(h.slice(5, 7), 16); return Math.abs(r - c[0]) <= tol && Math.abs(g - c[1]) <= tol && Math.abs(b - c[2]) <= tol; });
  const over = (t, b) => { const a = t[3] + b[3] * (1 - t[3]); if (a === 0) return [0, 0, 0, 0]; return [0, 1, 2].map((i) => (t[i] * t[3] + b[i] * b[3] * (1 - t[3])) / a).concat(a); };
  const lum = (c) => { const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]); };
  const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  const visible = (el) => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none' && +cs.opacity !== 0; };
  const srOnly = (el) => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el); return r.width <= 2 || r.height <= 2 || (cs.clip && cs.clip !== 'auto' && cs.position === 'absolute') || cs.clipPath === 'inset(50%)'; };
  const pageGround = rgba(getComputedStyle(document.body).backgroundColor)[3] > 0 ? rgba(getComputedStyle(document.body).backgroundColor) : rgba(getComputedStyle(document.documentElement).backgroundColor);
  const opacityOf = (el) => { let o = 1; for (let e = el; e && e.nodeType === 1; e = e.parentElement) o *= +getComputedStyle(e).opacity; return o; };
  const ancestors = (el) => { const l = []; for (let e = el; e && e.nodeType === 1; e = e.parentElement) l.push(e); return l; };
  const groundAt = (el, x, y) => {
    let list = null;
    if (x >= 0 && y >= 0 && x < vw && y < vh) { const st = document.elementsFromPoint(x, y); const i = st.indexOf(el); if (i >= 0) list = st.slice(i); }
    if (!list) list = ancestors(el);
    const layers = []; let image = false;
    for (const e of list) {
      const cs = getComputedStyle(e);
      if (/^(IMG|VIDEO|CANVAS|PICTURE)$/.test(e.tagName) || (e.classList && (e.classList.contains('leaflet-tile') || e.classList.contains('leaflet-container')))) { image = true; break; }
      if (cs.backgroundImage && cs.backgroundImage !== 'none' && !/^linear-gradient\\(rgba\\(0, 0, 0, 0\\)/.test(cs.backgroundImage)) { image = true; break; }
      const c = rgba(cs.backgroundColor);
      if (c[3] > 0) { layers.push(c); if (c[3] >= 0.999) break; }
    }
    let g = pageGround[3] > 0 ? pageGround : [255, 255, 255, 1];
    if (!layers.length || layers[layers.length - 1][3] < 0.999) g = over(g, [255, 255, 255, 1]); else g = [255, 255, 255, 1];
    for (let k = layers.length - 1; k >= 0; k--) g = over(layers[k], g);
    return { g, image };
  };
  const all = [...document.body.querySelectorAll('*')].filter(visible);

  // contrast of every visible text against its painted ground
  const textFails = []; let textChecked = 0, textOverImage = 0, textExempt = 0;
  const seenText = new Set();
  for (const el of all) {
    const tn = [...el.childNodes].find((n) => n.nodeType === 3 && n.textContent.trim());
    if (!tn || srOnly(el) || seenText.has(el)) continue;
    seenText.add(el);
    const range = document.createRange(); range.selectNodeContents(tn); const rr = range.getBoundingClientRect();
    if (rr.width < 1 || rr.height < 1) continue;
    const cs = getComputedStyle(el);
    const fg0 = rgba(cs.color); const op = opacityOf(el);
    const disabled = !!el.closest('[disabled],[aria-disabled="true"],[data-disabled]');
    const { g, image } = groundAt(el, rr.left + rr.width / 2, rr.top + rr.height / 2);
    if (image) { textOverImage++; continue; }
    const fg = over([fg0[0], fg0[1], fg0[2], fg0[3] * op], g);
    const size = parseFloat(cs.fontSize), weight = +cs.fontWeight || 400;
    const large = size >= 24 || (size >= 18.66 && weight >= 700);
    const r = ratio(fg, g); textChecked++;
    if (r < (large ? 3 : 4.5)) {
      if (disabled || op < 0.6) { textExempt++; continue; }
      textFails.push({ text: short(tn.textContent, 50), el: label(el), fg: hex(fg0) + (fg0[3] < 1 ? '@' + fg0[3].toFixed(2) : '') + (op < 1 ? ' op' + op.toFixed(2) : ''), ground: hex(g), ratio: +r.toFixed(2), size, weight, need: large ? 3 : 4.5, y: Math.round(rr.top + scrollY) });
    }
  }
  // placeholders
  for (const el of all.filter((e) => /^(INPUT|TEXTAREA)$/.test(e.tagName) && e.placeholder && !e.value)) {
    const pc = rgba(getComputedStyle(el, '::placeholder').color); const r0 = el.getBoundingClientRect();
    const { g } = groundAt(el, r0.left + 4, r0.top + r0.height / 2); const r = ratio(over(pc, g), g); textChecked++;
    if (r < 4.5 && !el.disabled) textFails.push({ text: '(placeholder) ' + short(el.placeholder, 40), el: label(el), fg: hex(pc), ground: hex(g), ratio: +r.toFixed(2), size: parseFloat(getComputedStyle(el).fontSize), need: 4.5 });
  }

  // touch targets
  const INTERACTIVE = 'a[href],button,input:not([type=hidden]),select,textarea,summary,[role=button],[role=link],[role=tab],[role=checkbox],[role=switch],[role=radio],[role=menuitem],[role=menuitemcheckbox],[role=menuitemradio],[role=option],[role=combobox],[role=slider],[tabindex]:not([tabindex="-1"])';
  const need = coarse ? 44 : 40;
  const small = []; let targets = 0;
  const pseudoBox = (el, r) => {
    let best = { w: r.width, h: r.height };
    for (const p of ['::before', '::after']) {
      const s = getComputedStyle(el, p);
      if (s.content === 'none' || s.content === 'normal' || s.position !== 'absolute') continue;
      const n = (v) => (v && v.endsWith('px') ? parseFloat(v) : null);
      const t = n(s.top), rt = n(s.right), b = n(s.bottom), l = n(s.left), w = n(s.width), h = n(s.height);
      const W = l !== null && rt !== null ? r.width - l - rt : w; const H = t !== null && b !== null ? r.height - t - b : h;
      if (W && H) best = { w: Math.max(best.w, W), h: Math.max(best.h, H) };
    }
    return best;
  };
  for (const el of all.filter((e) => e.matches(INTERACTIVE))) {
    if (srOnly(el) || el.closest('[aria-hidden="true"]')) continue;
    const r = el.getBoundingClientRect(); targets++;
    const cs = getComputedStyle(el);
    const inline = el.tagName === 'A' && cs.display === 'inline' && el.parentElement && [...el.parentElement.childNodes].some((n) => n !== el && n.nodeType === 3 && n.textContent.trim());
    const hit = pseudoBox(el, r);
    if ((hit.w < need - 0.5 || hit.h < need - 0.5) && !inline) {
      // a control inside a larger clickable row or label counts by that row (e.g. a checkbox in its label)
      const host = el.closest('label');
      if (host && host !== el) { const hr = host.getBoundingClientRect(); if (hr.width >= need && hr.height >= need) continue; }
      small.push({ el: label(el), w: Math.round(r.width), h: Math.round(r.height), hit: Math.round(hit.w) + 'x' + Math.round(hit.h), need, y: Math.round(r.top + scrollY) });
    }
  }

  // Sea's old values, and the spark as text or on an action
  const sea = [], sparkText = [], sparkAction = [], sparkMarks = [];
  const ACTION = 'a[href],button,[role=button],[role=link],[role=tab],[role=menuitem],[role=option],[role=switch],[role=checkbox],[role=radio],input,select,textarea';
  for (const el of all) {
    const cs = getComputedStyle(el);
    const props = { color: cs.color, background: cs.backgroundColor, border: parseFloat(cs.borderTopWidth) || parseFloat(cs.borderInlineStartWidth) ? (parseFloat(cs.borderTopWidth) ? cs.borderTopColor : cs.borderInlineStartColor) : null, outline: cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) ? cs.outlineColor : null, fill: el instanceof SVGElement ? cs.fill : null, stroke: el instanceof SVGElement && cs.stroke !== 'none' ? cs.stroke : null, decoration: cs.textDecorationLine !== 'none' ? cs.textDecorationColor : null };
    for (const [prop, css] of Object.entries(props)) {
      if (!css || css === 'none') continue;
      const c = rgba(css); if (c[3] < 0.05) continue;
      if (prop === 'color' && !(el.innerText || '').trim()) continue;
      const s = near(c, SEA, 2); if (s && sea.length < 30) sea.push({ el: label(el), prop, value: hex(c), sea: s });
      const k = near(c, SPARK, 3);
      if (k) {
        const isAction = el.matches(ACTION) || (el.closest(ACTION) && prop !== 'fill' && prop !== 'stroke' && prop !== 'background' && prop !== 'border');
        const state = ['aria-pressed', 'aria-checked', 'aria-selected', 'aria-current', 'data-state'].map((a) => el.getAttribute(a) ? a + '=' + el.getAttribute(a) : '').filter(Boolean).join(' ');
        const row = { el: label(el), prop, value: hex(c), spark: k, state, inAction: !!el.closest(ACTION) };
        if (prop === 'color' || prop === 'decoration') { if (sparkText.length < 30) sparkText.push(row); }
        else if (el.matches(ACTION)) { if (sparkAction.length < 30) sparkAction.push(row); }
        else if (sparkMarks.length < 40) sparkMarks.push(row);
      }
    }
  }

  // clipping and overflow (as round 2)
  const clipped = [], offscreen = [];
  for (const el of all) {
    const cs = getComputedStyle(el), r = el.getBoundingClientRect();
    if (r.width <= 2 || r.height <= 2) continue;
    if (el.scrollWidth > el.clientWidth + 1 && el.clientWidth > 0 && (cs.overflowX === 'hidden' || cs.overflowX === 'clip' || cs.textOverflow === 'ellipsis') && (el.innerText || '').trim())
      clipped.push({ el: label(el), axis: 'x', content: el.scrollWidth, box: el.clientWidth, ellipsis: cs.textOverflow === 'ellipsis' });
    if (el.children.length === 0 && (el.innerText || '').trim() && (r.right > vw + 1 || r.left < -1)) {
      let p = el.parentElement, inScroller = false;
      while (p) { const o = getComputedStyle(p).overflowX; if (o === 'auto' || o === 'scroll' || o === 'hidden' || o === 'clip') { inScroller = true; break; } p = p.parentElement; }
      if (!inScroller) offscreen.push({ el: label(el), left: Math.round(r.left), right: Math.round(r.right) });
    }
  }
  const imgs = [...document.images].filter((i) => i.complete && i.naturalWidth === 0 && i.getAttribute('src')).map((i) => i.getAttribute('src'));
  const heads = [...document.querySelectorAll('h1,h2,h3')].filter(visible).map((h) => h.tagName.toLowerCase() + ' ' + short(h.innerText, 70));
  const dialogs = [...document.querySelectorAll('[role=dialog],[role=alertdialog],[role=menu],[role=listbox]')].filter(visible).map((d) => label(d));
  const toasts = [...document.querySelectorAll('[data-sonner-toast]')].map((t) => short(t.innerText, 120));
  const landmarks = [...document.querySelectorAll('header,nav,main,footer,aside,[role=banner],[role=navigation],[role=main],[role=contentinfo]')].filter(visible).map((l) => l.tagName.toLowerCase() + (l.getAttribute('aria-label') ? ' «' + short(l.getAttribute('aria-label'), 40) + '»' : ''));
  const busy = [...document.querySelectorAll('[aria-busy="true"]')].length;
  const skeletons = [...document.querySelectorAll('[data-slot=skeleton],.animate-pulse')].filter(visible).length;
  return {
    phase: ${JSON.stringify(phase)},
    title: document.title, htmlLang: document.documentElement.lang, dir: document.documentElement.dir,
    theme: document.documentElement.dataset.theme || '(none)', coarse,
    viewport: [vw, vh], page: { scrollWidth: document.documentElement.scrollWidth, clientWidth: document.documentElement.clientWidth, scrollHeight: document.documentElement.scrollHeight },
    horizontalPageOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
    textLength: (document.body.innerText || '').trim().length,
    headings: heads, landmarks, dialogs, toasts, busy, skeletons, brokenImages: imgs,
    contrast: { checked: textChecked, overImage: textOverImage, exemptDisabled: textExempt, fails: textFails.slice(0, 60), failCount: textFails.length },
    targets: { checked: targets, need, small: small.slice(0, 50), smallCount: small.length },
    seaValues: sea, sparkAsText: sparkText, sparkOnAction: sparkAction, sparkMarks: sparkMarks,
    clipped: clipped.slice(0, 40), offscreen: offscreen.slice(0, 40),
    text: (document.body.innerText || '').replace(/\\n{3,}/g, '\\n\\n').slice(0, 7000),
  };
})()`;

const FOCUS_PROBE = `(() => {
  const el = document.activeElement; if (!el || el === document.body) return { el: '(body)' };
  const short = (s, n = 60) => (s || '').replace(/\\s+/g, ' ').trim().slice(0, n);
  const cs = getComputedStyle(el); const r = el.getBoundingClientRect();
  const cv = document.createElement('canvas'); cv.width = cv.height = 1; const cx = cv.getContext('2d', { willReadFrequently: true });
  const rgba = (css) => { cx.clearRect(0, 0, 1, 1); cx.fillStyle = 'rgba(0,0,0,0)'; cx.fillStyle = css; cx.fillRect(0, 0, 1, 1); const d = cx.getImageData(0, 0, 1, 1).data; return [d[0], d[1], d[2], d[3] / 255]; };
  const hex = (c) => '#' + c.slice(0, 3).map((x) => Math.round(x).toString(16).padStart(2, '0')).join('');
  const lum = (c) => { const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]); };
  let g = null; for (let e = el.parentElement; e; e = e.parentElement) { const c = rgba(getComputedStyle(e).backgroundColor); if (c[3] > 0.99) { g = c; break; } }
  g = g || [255, 255, 255, 1];
  const oc = rgba(cs.outlineColor); const ow = parseFloat(cs.outlineWidth) || 0;
  const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  return {
    el: el.tagName.toLowerCase() + (el.getAttribute('role') ? '[role=' + el.getAttribute('role') + ']' : '') + ' «' + short(el.getAttribute('aria-label') || el.innerText || el.value || '') + '»',
    focusVisible: el.matches(':focus-visible'), inViewport: r.bottom > 0 && r.top < innerHeight && r.right > 0 && r.left < innerWidth,
    rect: [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)],
    outline: cs.outlineStyle === 'none' || !ow ? 'none' : cs.outlineStyle + ' ' + ow + 'px ' + hex(oc) + ' offset ' + cs.outlineOffset,
    outlineVsGround: cs.outlineStyle === 'none' || !ow ? null : +ratio(oc, g).toFixed(2), ground: hex(g),
    boxShadow: cs.boxShadow === 'none' ? null : cs.boxShadow.slice(0, 80),
  };
})()`;

// ---- steps ----
const pick = (v, lang) => (v && typeof v === 'object' && !Array.isArray(v) ? v[lang] : v);
const FIND = (sel, within, nth) => `(() => {
  const sel = ${JSON.stringify(sel)}, within = ${JSON.stringify(within || null)}, nth = ${nth || 0};
  const visible = (el) => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; };
  const norm = (s) => (s || '').replace(/[\\u2066-\\u2069\\u200e\\u200f\\u061c]/g, '').replace(/\\s+/g, ' ').trim();
  let root = document;
  if (within) { const w = [...document.querySelectorAll(within.replace(/^css:/, ''))].filter(visible).pop(); if (!w) return null; root = w; }
  let found = [];
  if (sel.startsWith('css:')) found = [...root.querySelectorAll(sel.slice(4))].filter(visible);
  else if (sel.startsWith('field:')) {
    const want = norm(sel.slice(6));
    const labels = [...root.querySelectorAll('label')].filter((l) => norm(l.innerText) === want || norm(l.innerText).startsWith(want + ' '));
    found = labels.map((l) => (l.htmlFor && document.getElementById(l.htmlFor)) || l.querySelector('input,textarea,select,button,[role=combobox]')).filter((el) => el && visible(el));
  }
  else {
    const want = norm(sel.replace(/^(text|label):/, ''));
    const pool = [...root.querySelectorAll('a,button,[role],input,label,summary,[tabindex],h1,h2,h3,span,div,li,p')].filter(visible);
    const name = (el) => norm(el.getAttribute('aria-label') || el.innerText || el.value || el.getAttribute('title') || '');
    const exact = pool.filter((el) => name(el) === want);
    const inter = (l) => l.filter((el) => el.matches('a,button,[role],input,summary,[tabindex],label'));
    found = inter(exact).length ? inter(exact) : exact;
    if (!found.length) { const part = pool.filter((el) => name(el).includes(want)); found = inter(part).length ? inter(part) : part; found = found.sort((a, b) => name(a).length - name(b).length); }
  }
  const el = found[nth]; if (!el) return null;
  el.scrollIntoView({ block: 'center', inline: 'center' });
  const r = el.getBoundingClientRect();
  window.__r3el = el;
  return { x: r.left + r.width / 2, y: r.top + r.height / 2, tag: el.tagName };
})()`;

async function evaluate(sessionId, expression, awaitPromise = false) {
  const { result, exceptionDetails } = await send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise }, sessionId);
  if (exceptionDetails) throw new Error('eval: ' + (exceptionDetails.exception?.description || exceptionDetails.text).split('\n')[0]);
  return result.value;
}
async function find(sessionId, sel, within, nth, ms = 7000) {
  const t0 = Date.now();
  while (Date.now() - t0 < ms) { const v = await evaluate(sessionId, FIND(sel, within, nth)); if (v) return v; await sleep(250); }
  throw new Error('step target not found: ' + sel + (within ? ' within ' + within : ''));
}
async function clickAt(sessionId, x, y) {
  await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y }, sessionId);
  await send('Input.dispatchMouseEvent', { type: 'mousePressed', x, y, button: 'left', clickCount: 1 }, sessionId);
  await send('Input.dispatchMouseEvent', { type: 'mouseReleased', x, y, button: 'left', clickCount: 1 }, sessionId);
}
const KEYS = { Backspace: 8, Delete: 46, Enter: 13, Escape: 27, Tab: 9, ArrowDown: 40, ArrowUp: 38, ArrowLeft: 37, ArrowRight: 39, Space: 32, End: 35, Home: 36 };
async function key(sessionId, k, shift = false) {
  const code = KEYS[k]; const text = k === 'Enter' ? '\r' : k === 'Space' ? ' ' : undefined;
  await send('Input.dispatchKeyEvent', { type: 'keyDown', key: k === 'Space' ? ' ' : k, code: k === 'Space' ? 'Space' : k, windowsVirtualKeyCode: code, nativeVirtualKeyCode: code, modifiers: shift ? 8 : 0, text }, sessionId);
  await send('Input.dispatchKeyEvent', { type: 'keyUp', key: k === 'Space' ? ' ' : k, code: k === 'Space' ? 'Space' : k, windowsVirtualKeyCode: code, nativeVirtualKeyCode: code, modifiers: shift ? 8 : 0 }, sessionId);
}
async function runSteps(sessionId, steps, lang, settle) {
  let shotN = 0;
  for (const raw of steps || []) {
    const s = raw[lang] && typeof raw[lang] === 'object' ? raw[lang] : raw; // a step may be per language
    if (s.width && !s.width.includes?.(settle.w)) continue;
    if (s.click) { const t = await find(sessionId, pick(s.click, lang), pick(s.within, lang), s.nth); await sleep(150); await clickAt(sessionId, t.x, t.y); }
    else if (s.type) { const t = await find(sessionId, pick(s.type, lang), pick(s.within, lang), s.nth); await clickAt(sessionId, t.x, t.y); await evaluate(sessionId, 'window.__r3el.select?.()'); await send('Input.insertText', { text: String(pick(s.text, lang)) }, sessionId); }
    else if (s.clear) { const t = await find(sessionId, pick(s.clear, lang), pick(s.within, lang), s.nth); await clickAt(sessionId, t.x, t.y); await evaluate(sessionId, 'window.__r3el.select?.()'); await key(sessionId, 'Backspace'); }
    else if (s.key) { for (let i = 0; i < (s.times || 1); i++) { await key(sessionId, s.key, s.shift); await sleep(80); } }
    else if (s.focus) { await find(sessionId, pick(s.focus, lang), pick(s.within, lang), s.nth); await evaluate(sessionId, 'window.__r3el.focus()'); }
    else if (s.scroll) { await find(sessionId, pick(s.scroll, lang), pick(s.within, lang), s.nth); }
    else if (s.waitFor) { await find(sessionId, pick(s.waitFor, lang), pick(s.within, lang), s.nth, s.ms || 10000); }
    else if (s.eval) { await evaluate(sessionId, pick(s.eval, lang), true); }
    else if (s.shot) { await sleep(300); const { data } = await send('Page.captureScreenshot', { format: 'png' }, sessionId); const d = join(OUT, settle.part, 'frames'); mkdirSync(d, { recursive: true }); writeFileSync(join(d, `${settle.id}.step${++shotN}-${s.shot}.png`), Buffer.from(data, 'base64')); settle.focusLog.push({ shot: s.shot, focus: await evaluate(sessionId, FOCUS_PROBE) }); continue; }
    if (s.wait) await sleep(s.wait);
    await settle.idle(4000);
    await sleep(s.after ?? 350);
  }
}

// ---- one frame ----
const ENVELOPE = (status) => {
  const type = { 400: 'bad_request', 401: 'unauthorized', 403: 'forbidden', 404: 'not_found', 409: 'conflict', 422: 'validation', 429: 'rate_limit', 500: 'server', 503: 'service_unavailable' }[status] || 'server';
  return Buffer.from(JSON.stringify({ success: false, error: { type, message: 'simulated by the review capture tool', requestId: '00000000-0000-4000-8000-000000000000' } })).toString('base64');
};
const globToRe = (g) => new RegExp('^' + g.replace(/[.+^${}()|[\]\\]/g, '\\$&').replace(/\*/g, '.*').replace(/\?/g, '\\?') + '$');

async function renderOne(job) {
  const b = job.base;
  const role = b.role || 'visitor';
  const key = b.geo ? `${role}:geo:${b.geo === 'denied' ? 'denied' : 'granted'}` : role;
  const ctx = await contextOf(key);
  if (role !== 'visitor' && !ctx.signedIn) await signIn(role, key);
  const { targetId } = await send('Target.createTarget', { url: 'about:blank', browserContextId: ctx.id });
  const { sessionId } = await send('Target.attachToTarget', { targetId, flatten: true });
  const errors = [], apiErrors = []; let inflight = new Set(), lastNet = Date.now(), loaded = false;
  const held = new Set(); const simulated = [];
  const holdRe = b.hold ? globToRe(b.hold.url) : null;
  const fails = [].concat(b.fail || []).map((f) => ({ ...f, re: globToRe(f.url) }));
  const mocks = [].concat(b.mock || []).map((m) => ({ ...m, re: globToRe(m.url) }));
  const failRe = fails.length || mocks.length ? true : null;
  const patches = [].concat(b.patch || []).map((x) => ({ ...x, re: globToRe(x.url) }));
  listeners.set(sessionId, (method, p) => {
    if (method === 'Runtime.exceptionThrown') errors.push('exception: ' + (p.exceptionDetails.exception?.description || p.exceptionDetails.text).split('\n')[0]);
    else if (method === 'Runtime.consoleAPICalled' && (p.type === 'error' || p.type === 'warning') && !/Download the React DevTools|\[vite\]/.test(String(p.args[0]?.value || ''))) errors.push(p.type + ': ' + p.args.map((a) => a.value ?? a.description ?? '').join(' ').slice(0, 300));
    else if (method === 'Log.entryAdded' && p.entry.level === 'error' && !(p.entry.url || '').includes('/api/')) errors.push('log: ' + p.entry.text.slice(0, 300) + (p.entry.url ? ' ' + p.entry.url.replace(BASE, '') : ''));
    else if (method === 'Network.requestWillBeSent') { inflight.add(p.requestId); lastNet = Date.now(); }
    else if (method === 'Network.responseReceived') { if (p.response.url.includes('/api/') && p.response.status >= 400 && !simulated.includes(p.response.url)) apiErrors.push(p.response.status + ' ' + p.response.url.replace(BASE, '')); }
    else if (method === 'Network.loadingFinished' || method === 'Network.loadingFailed') { inflight.delete(p.requestId); lastNet = Date.now(); if (method === 'Network.loadingFailed' && !p.canceled && !held.has(p.requestId)) errors.push('network: ' + p.errorText); }
    else if (method === 'Page.loadEventFired') loaded = true;
    else if (method === 'Fetch.requestPaused' && p.responseStatusCode !== undefined) {
      // response stage: a real answer patched (a field set, an item appended), then given to the page
      const pt = patches.find((x) => x.re.test(p.request.url) && (!x.method || x.method === p.request.method));
      (async () => {
        try {
          if (!pt) throw new Error('no patch');
          const { body, base64Encoded } = await send('Fetch.getResponseBody', { requestId: p.requestId }, sessionId);
          const json = JSON.parse(base64Encoded ? Buffer.from(body, 'base64').toString('utf8') : body);
          const walk = (path) => { const keys = path.split('.'); let o = json; for (const k of keys.slice(0, -1)) o = o?.[/^\d+$/.test(k) ? Number(k) : k]; return [o, keys[keys.length - 1]]; };
          for (const [path, v] of Object.entries(pt.set || {})) { const [o, k] = walk(path); if (o) o[/^\d+$/.test(k) ? Number(k) : k] = v; }
          for (const [path, v] of Object.entries(pt.push || {})) { const [o, k] = walk(path + '.x'); if (Array.isArray(o)) o.push(v); }
          simulated.push(p.request.url);
          await send('Fetch.fulfillRequest', { requestId: p.requestId, responseCode: p.responseStatusCode, responseHeaders: (p.responseHeaders || []).filter((h) => !/^content-length$/i.test(h.name)), body: Buffer.from(JSON.stringify(json)).toString('base64') }, sessionId);
        } catch { send('Fetch.continueRequest', { requestId: p.requestId }, sessionId).catch(() => {}); }
      })();
    }
    else if (method === 'Fetch.requestPaused') {
      const u = p.request.url, m = p.request.method;
      if (!failRe && !holdRe) { send('Fetch.continueRequest', { requestId: p.requestId }, sessionId).catch(() => {}); return; }
      if (holdRe && holdRe.test(u) && (!b.hold.method || b.hold.method === m)) { held.add(p.networkId); inflight.delete(p.networkId); return; }
      const mk = mocks.find((x) => x.re.test(u) && (!x.method || x.method === m));
      if (mk) {
        simulated.push(u);
        send('Fetch.fulfillRequest', { requestId: p.requestId, responseCode: mk.status || 200, responseHeaders: [{ name: 'content-type', value: 'application/json' }], body: mk.status === 204 ? '' : Buffer.from(JSON.stringify(mk.json)).toString('base64') }, sessionId).catch(() => {});
        return;
      }
      const fl = fails.find((x) => x.re.test(u) && (!x.method || x.method === m));
      if (fl && fl.status === 0) { simulated.push(u); held.add(p.networkId); send('Fetch.failRequest', { requestId: p.requestId, errorReason: 'InternetDisconnected' }, sessionId).catch(() => {}); return; }
      if (fl) {
        simulated.push(u);
        const st = fl.status || 500;
        const headers = [{ name: 'content-type', value: 'application/json' }];
        if (st === 429) headers.push({ name: 'retry-after', value: '60' }, { name: 'ratelimit-policy', value: '300;w=900' }, { name: 'ratelimit', value: 'limit=300, remaining=0, reset=60' });
        send('Fetch.fulfillRequest', { requestId: p.requestId, responseCode: st, responseHeaders: headers, body: ENVELOPE(st) }, sessionId).catch(() => {});
        return;
      }
      send('Fetch.continueRequest', { requestId: p.requestId }, sessionId).catch(() => {});
    }
  });
  const idle = async (ms) => { const t0 = Date.now(); while (Date.now() - t0 < ms && !([...inflight].filter((id) => !held.has(id)).length === 0 && Date.now() - lastNet > 700)) await sleep(120); };
  try {
    for (const d of ['Page', 'Runtime', 'Log', 'Network']) await send(d + '.enable', {}, sessionId);
    const patterns = [...(holdRe || failRe ? [{ urlPattern: '*/api/*', requestStage: 'Request' }] : []), ...patches.map((x) => ({ urlPattern: x.url, requestStage: 'Response' }))];
    if (patterns.length) await send('Fetch.enable', { patterns }, sessionId);
    if (b.geo && b.geo !== 'denied') await send('Emulation.setGeolocationOverride', { latitude: b.geo.lat, longitude: b.geo.lng, accuracy: b.geo.accuracy || 50 }, sessionId);
    const h = HEIGHTS[job.w] || 900; const mobile = job.w < 768; const touch = job.w < 1024;
    await send('Emulation.setDeviceMetricsOverride', { width: job.w, height: h, deviceScaleFactor: 1, mobile }, sessionId);
    await send('Emulation.setTouchEmulationEnabled', { enabled: touch, maxTouchPoints: touch ? 5 : 0 }, sessionId);
    await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-color-scheme', value: job.theme }, { name: 'prefers-reduced-motion', value: b.reducedMotion ? 'reduce' : 'no-preference' }] }, sessionId);
    await send('Emulation.setFocusEmulationEnabled', { enabled: true }, sessionId);
    const pre = `try { localStorage.setItem('masaha.language', ${JSON.stringify(job.lang)}); localStorage.setItem('masaha.theme', ${JSON.stringify(job.theme)}); ${b.storage ? Object.entries(b.storage).map(([k, v]) => `localStorage.setItem(${JSON.stringify(k)}, ${JSON.stringify(v)});`).join(' ') : ''} } catch (e) {}`;
    await send('Page.addScriptToEvaluateOnNewDocument', { source: pre }, sessionId);
    const url = BASE + pick(b.url, job.lang).replaceAll('{lang}', job.lang).replaceAll('{theme}', job.theme);
    await send('Page.navigate', { url }, sessionId);
    const t0 = Date.now();
    while (Date.now() - t0 < 25000 && !(loaded && [...inflight].filter((id) => !held.has(id)).length === 0 && Date.now() - lastNet > 900)) await sleep(150);
    await evaluate(sessionId, 'document.fonts.ready.then(() => true)', true).catch(() => {});
    await sleep(500);
    if (role !== 'visitor') {
      const hint = await evaluate(sessionId, `document.cookie.includes('masaha_session=1')`);
      if (!hint) throw Object.assign(new Error('signed out (no session hint)'), { signedOut: true });
    }
    const settle = { w: job.w, idle, part: b.part, id: job.id, focusLog: [] };
    await runSteps(sessionId, b.steps, job.lang, settle);
    await sleep(b.settle ?? 450);
    const outDir = join(OUT, b.part, 'frames'); mkdirSync(outDir, { recursive: true });
    // first screen: facts read at this viewport, then the capture
    const first = await evaluate(sessionId, PROBE('first-screen'));
    const shot = async (file) => { const { data } = await send('Page.captureScreenshot', { format: 'png' }, sessionId); writeFileSync(join(outDir, file), Buffer.from(data, 'base64')); };
    await shot(job.id + '.png');
    // the whole page: the viewport stretched to the page's height, facts read again there (every text in view)
    const sh = await evaluate(sessionId, 'Math.max(document.documentElement.scrollHeight, document.body.scrollHeight)');
    const fh = Math.min(FULL_CAP, Math.max(h, sh));
    let whole = first;
    if (fh > h + 4) {
      await send('Emulation.setDeviceMetricsOverride', { width: job.w, height: fh, deviceScaleFactor: 1, mobile }, sessionId);
      await sleep(450);
      whole = await evaluate(sessionId, PROBE('whole-page'));
    }
    await shot(job.id + '.full.png');
    // focus after Tab: back to the first screen, three Tab presses from the top of the document
    await send('Emulation.setDeviceMetricsOverride', { width: job.w, height: h, deviceScaleFactor: 1, mobile }, sessionId);
    await sleep(250);
    const focus = [];
    if (!b.noTab) {
      await evaluate(sessionId, `(() => { const d = [...document.querySelectorAll('[role=dialog],[role=alertdialog]')].pop(); if (!d) { document.activeElement?.blur?.(); window.scrollTo(0, 0); } return true; })()`);
      for (let i = 0; i < (b.tabStops || 3); i++) { await key(sessionId, 'Tab', !!b.shiftTab); await sleep(160); focus.push(await evaluate(sessionId, FOCUS_PROBE)); }
    }
    const facts = {
      id: job.id, base: b.id, part: b.part, screen: b.screen, state: b.state, role, url, width: job.w, lang: job.lang, mode: job.theme,
      langOk: first.htmlLang === job.lang && first.dir === (job.lang === 'ar' ? 'rtl' : 'ltr'), themeOk: first.theme === job.theme,
      held: b.hold ? `${b.hold.method || '*'} ${b.hold.url} (${held.size} held)` : null,
      simulated: fails.length || mocks.length ? [...fails.map((f) => `${f.method || '*'} ${f.url} → ${f.status || 500}`), ...mocks.map((x) => `${x.method || '*'} ${x.url} → mocked ${x.status || 200} (${x.note || 'data'})`)].join('; ') + ` — simulated by the capture tool at the network layer, ${simulated.length} answered` : null,
      consoleErrors: errors, apiErrors, focusAfterTab: focus, stepShots: settle.focusLog, firstScreen: first, wholePage: whole === first ? '(same as firstScreen)' : whole,
    };
    writeFileSync(join(outDir, job.id + '.json'), JSON.stringify(facts, null, 1));
    return { id: job.id, base: b.id, part: b.part, ok: true, langOk: facts.langOk, themeOk: facts.themeOk, errors: errors.length, apiErrors: apiErrors.length };
  } finally {
    listeners.delete(sessionId);
    await send('Target.closeTarget', { targetId }).catch(() => {});
  }
}

// ---- the run ----
log(`run: ${jobs.length} frames from ${bases.length} bases (${PART || 'all parts'}), widths ${WIDTHS}, ${LANGS}, ${THEMES}, ${TABS} tabs`);
const results = []; let next = 0, done = 0, sinceClear = 0;
clearRateLimits();
async function worker() {
  while (next < jobs.length) {
    const job = jobs[next++];
    if (++sinceClear >= CLEAR_EVERY) { sinceClear = 0; clearRateLimits(); }
    let r;
    for (let attempt = 1; attempt <= 2; attempt++) {
      try { r = await renderOne(job); break; }
      catch (e) {
        if (e.signedOut && attempt === 1) { log(`${job.id}: signed out, signing in again`); for (const [k, c] of Object.entries(contexts)) if (k.split(':')[0] === (job.base.role || 'visitor')) c.signedIn = false; continue; }
        if (attempt === 1 && /timed out|Target closed|not found/.test(String(e.message))) { log(`${job.id}: retry after ${e.message}`); await sleep(1500); continue; }
        r = { id: job.id, base: job.base.id, part: job.base.part, ok: false, failed: String(e.message || e) };
      }
    }
    if (!r.ok) log(`FAILED ${job.id}: ${r.failed}`);
    results.push(r);
    done++; if (done % 24 === 0 || done === jobs.length) { console.log(`${done}/${jobs.length}`); log(`${done}/${jobs.length}`); }
  }
}
await Promise.all(Array.from({ length: TABS }, worker));
ws.close();
cleanup();
const failed = results.filter((r) => !r.ok);
const wrong = results.filter((r) => r.ok && (!r.langOk || !r.themeOk));
writeFileSync(join(LOGDIR, `results-${stampNow()}.json`), JSON.stringify(results, null, 1));
log(`done: ${results.length} frames, ${failed.length} failed, ${wrong.length} with a wrong language or theme`);
console.log(`pack ${PART || 'ALL'}: ${results.length} frames, ${failed.length} failed, ${wrong.length} wrong lang/theme — log ${RUNLOG}`);
for (const f of failed.slice(0, 30)) console.log('  failed ' + f.id + ': ' + f.failed);
