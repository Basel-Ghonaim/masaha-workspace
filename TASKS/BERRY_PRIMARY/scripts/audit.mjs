// WI-B2's audit: every screen's and overlay's painted main action, in a headless Chrome over CDP.
// Light theme; as a guest, the demo owner and the admin; at 1440 and 390. Each role signs in once and
// moves between routes inside the app (history + popstate), so the refresh limiter (30 / 15 min) is
// never reached. Routes in Arabic; overlays in English (their triggers found by their words). Then
// dark on five screens: no berry painted anywhere. axe on the auth views and the sign-in overlay.
// Usage: node audit.mjs [regex]. Needs the API on 3320 and the web on 5320. Passwords read from the
// API's .env, never printed.
import { spawn } from 'node:child_process';
import { mkdirSync, mkdtempSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const ONLY = process.argv[2] ? new RegExp(process.argv[2]) : null;
const APP = 'C:/dev/masaha/app';
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const WEB = 'http://localhost:5320';
const SPACE_ID = 26;
const SLUG = 'pal-hub';
const SHOTS = 'C:/Users/basel/Downloads/berry-audit-shots/raw';
const OUT = 'C:/dev/masaha/workspace/TASKS/BERRY_PRIMARY/scripts/out-audit.json';
mkdirSync(SHOTS, { recursive: true });
const AXE = readFileSync(`${APP}/node_modules/axe-core/axe.min.js`, 'utf8');
const ENV = readFileSync(`${APP}/apps/api/.env`, 'utf8');
const env = (key) =>
  new RegExp(`^${key}=(.*)$`, 'm')
    .exec(ENV)?.[1]
    ?.trim()
    .replace(/^["']|["']$/g, '');
const OWNER = { key: 'owner', email: 'demo-owner@example.com', password: env('SEED_DEMO_PASSWORD') };
const ADMIN = { key: 'admin', email: env('SEED_ADMIN_EMAIL'), password: env('SEED_ADMIN_PASSWORD') };
const GUEST = { key: 'guest' };
if (!OWNER.password || !ADMIN.email || !ADMIN.password) throw new Error('a seed credential is missing');
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const port = 9300 + Math.floor(Math.random() * 600);
const profile = mkdtempSync(join(tmpdir(), 'cdp-'));
const chrome = spawn(CHROME, [
  '--headless=new',
  `--remote-debugging-port=${port}`,
  `--user-data-dir=${profile}`,
  '--no-first-run',
  '--no-default-browser-check',
  'about:blank',
]);
console.log('chrome pid', chrome.pid);
let targets = [];
for (let i = 0; i < 50; i += 1) {
  try {
    targets = await (await fetch(`http://127.0.0.1:${port}/json`)).json();
    if (targets.some((t) => t.type === 'page')) break;
  } catch {
    /* not up yet */
  }
  await sleep(200);
}
const socket = new WebSocket(targets.find((t) => t.type === 'page').webSocketDebuggerUrl);
await new Promise((resolve) => socket.addEventListener('open', resolve));
let id = 0;
const pending = new Map();
const errors = [];
let refreshes = 0;
socket.addEventListener('message', (event) => {
  const message = JSON.parse(event.data);
  if (message.id !== undefined && pending.has(message.id)) {
    const { resolve, reject } = pending.get(message.id);
    pending.delete(message.id);
    if (message.error) reject(new Error(JSON.stringify(message.error)));
    else resolve(message.result);
  } else if (message.method === 'Runtime.exceptionThrown') {
    errors.push(message.params.exceptionDetails.text);
  } else if (message.method === 'Network.responseReceived') {
    const { url, status } = message.params.response;
    if (url.includes('/auth/refresh')) {
      refreshes += 1;
      if (status === 429) errors.push(`refresh 429 at ${url}`);
    }
  }
});
const send = (method, params = {}) =>
  new Promise((resolve, reject) => {
    id += 1;
    pending.set(id, { resolve, reject });
    socket.send(JSON.stringify({ id, method, params }));
  });
const evaluate = async (expression) => {
  const result = await send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
  if (result.exceptionDetails) {
    throw new Error(result.exceptionDetails.exception?.description ?? result.exceptionDetails.text);
  }
  return result.result.value;
};
const until = async (expression, what, ms = 20000) => {
  const end = Date.now() + ms;
  while (Date.now() < end) {
    try {
      if (await evaluate(expression)) return;
    } catch {
      /* page changing */
    }
    await sleep(150);
  }
  throw new Error(`timed out: ${what}`);
};
await send('Page.enable');
await send('Runtime.enable');
await send('Network.enable');

async function viewport(width) {
  const phone = width < 768;
  await send('Emulation.setDeviceMetricsOverride', {
    width,
    height: phone ? 844 : 900,
    deviceScaleFactor: 1,
    mobile: phone,
  });
  await sleep(400);
}
async function load(path) {
  await send('Page.navigate', { url: 'about:blank' });
  await sleep(120);
  await send('Page.navigate', { url: `${WEB}${path}` });
  await until('document.readyState === "complete"', `load ${path}`);
}
async function prefs(lang, theme) {
  await load('/__nothing');
  await evaluate(
    `localStorage.setItem('masaha.language', ${JSON.stringify(lang)}); localStorage.setItem('masaha.theme', ${JSON.stringify(theme)}); true`,
  );
}
async function signIn(who) {
  await send('Network.clearBrowserCookies');
  if (!who.email) return;
  await load('/__nothing');
  const status = await evaluate(`fetch('/api/v1/auth/login', {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, credentials: 'include',
      body: JSON.stringify({ email: ${JSON.stringify(who.email)}, password: ${JSON.stringify(who.password)} }),
    }).then((r) => r.status)`);
  if (status !== 200) throw new Error(`sign-in ${status}`);
}
/** Moves inside the app, as a link would: no page load, so no refresh. */
async function nav(path) {
  await evaluate(
    `window.history.pushState(null, '', ${JSON.stringify(path)}); window.dispatchEvent(new PopStateEvent('popstate')); true`,
  );
  await sleep(300);
  await until(
    `!!document.querySelector('h1') && !document.querySelector('[data-slot="skeleton"]')`,
    `ready ${path}`,
  ).catch(() => {});
  await sleep(1200);
  await evaluate('window.scrollTo(0, 0); true');
  await sleep(200);
}

/** The painted buttons: the main actions, in the page and in view, any berry fill, the filled ink. */
const MEASURE = `(() => {
  const vw = innerWidth, vh = innerHeight;
  const shown = (el) => el.getClientRects().length > 0 && getComputedStyle(el).visibility !== 'hidden';
  const inView = (el) => { const b = el.getBoundingClientRect(); return b.bottom > 0 && b.top < vh && b.right > 0 && b.left < vw; };
  const hue = (bg) => { const m = /rgba?\\((\\d+), (\\d+), (\\d+)(?:, ([\\d.]+))?/.exec(bg); if (!m) return null;
    if (m[4] !== undefined && Number(m[4]) < 0.5) return null;
    const [r, g, b] = [m[1], m[2], m[3]].map((v) => v / 255); const max = Math.max(r, g, b), min = Math.min(r, g, b), d = max - min;
    if (d < 0.15) return null; let h = max === r ? ((g - b) / d) % 6 : max === g ? (b - r) / d + 2 : (r - g) / d + 4; h *= 60; if (h < 0) h += 360; return h; };
  const overlays = [...document.querySelectorAll('[role="dialog"], [role="alertdialog"]')].filter(shown);
  const where = (el) => overlays.some((o) => o.contains(el)) ? 'overlay' : 'page';
  const name = (el) => (el.getAttribute('aria-label') ?? el.textContent ?? '').replace(/\\s+/g, ' ').trim().slice(0, 40);
  const buttons = [...document.querySelectorAll('[data-slot="button"]')].filter(shown);
  const row = (el) => ({ name: name(el), where: where(el), inView: inView(el), bg: getComputedStyle(el).backgroundColor });
  const mains = buttons.filter((el) => el.classList.contains('bg-main-action')).map(row);
  const berry = buttons.filter((el) => { const h = hue(getComputedStyle(el).backgroundColor); return h !== null && h > 270 && h < 345; }).map(row);
  const ink = buttons.filter((el) => el.classList.contains('bg-primary')).map(row);
  return { path: location.pathname, h1: document.querySelector('h1')?.textContent?.trim().slice(0, 50) ?? null,
    overlay: overlays.map((o) => (o.querySelector('h2')?.textContent ?? o.getAttribute('aria-label') ?? '').trim().slice(0, 50)),
    overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth,
    theme: document.documentElement.dataset.theme, lang: document.documentElement.lang, mains, berry, ink };
})()`;

async function runAxe() {
  if (!(await evaluate('typeof window.axe !== "undefined"'))) await evaluate(`${AXE}; true`);
  return evaluate(`axe.run(document, { resultTypes: ['violations'] }).then((r) => r.violations.map((v) => ({
      id: v.id, impact: v.impact, nodes: v.nodes.length, targets: v.nodes.slice(0, 3).map((n) => n.target.join(' ')) })))`);
}
async function shot(file) {
  const { data } = await send('Page.captureScreenshot', { format: 'png' });
  writeFileSync(`${SHOTS}/${file}.png`, Buffer.from(data, 'base64'));
}
const press = async (key, code, keyCode) => {
  await send('Input.dispatchKeyEvent', { type: 'rawKeyDown', key, code, windowsVirtualKeyCode: keyCode });
  await send('Input.dispatchKeyEvent', { type: 'keyUp', key, code, windowsVirtualKeyCode: keyCode });
};
const slug = (text) => text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

/** The links in the page whose href matches `pattern`, deduplicated. */
const links = (pattern) =>
  evaluate(`[...new Set([...document.querySelectorAll('a[href]')].map((a) => a.getAttribute('href')).filter((h) => ${pattern}.test(h)))]`);

const results = { routes: {}, overlays: {}, dark: {}, axe: {}, errors, refreshes: 0 };

async function record(bucket, key, extra = {}) {
  if (ONLY && !ONLY.test(key)) return;
  const measured = await evaluate(MEASURE);
  await shot(key);
  results[bucket][key] = { ...measured, ...extra };
  const mainsPage = measured.mains.filter((m) => m.where === 'page');
  const mainsOverlay = measured.mains.filter((m) => m.where === 'overlay');
  console.log(
    key,
    measured.path,
    `page ${mainsPage.length} (view ${mainsPage.filter((m) => m.inView).length})`,
    `overlay ${mainsOverlay.length}`,
    `berry ${measured.berry.length}`,
    measured.overflow ? 'OVERFLOW' : '',
  );
}

/** Opens the overlay a control named `label` opens, measures it, closes it with Escape. */
async function overlay(key, label, { within = 'document', nth = 0 } = {}) {
  if (ONLY && !ONLY.test(key)) return;
  try {
    const opened = await evaluate(`(() => {
      const root = ${within === 'document' ? 'document' : `document.querySelector(${JSON.stringify(within)})`};
      const all = [...root.querySelectorAll('button, a, [role="button"]')].filter((el) => el.getClientRects().length > 0 &&
        new RegExp(${JSON.stringify(label)}).test((el.getAttribute('aria-label') ?? el.textContent ?? '').replace(/\\s+/g, ' ').trim()));
      const el = all[${nth}]; if (!el) return [...root.querySelectorAll('button, a[data-slot="button"]')].filter((e) => e.getClientRects().length > 0)
        .map((e) => (e.getAttribute('aria-label') ?? e.textContent ?? '').replace(/\\s+/g, ' ').trim().slice(0, 40)).join(' | '); el.scrollIntoView({ block: 'center' }); el.click(); return true; })()`);
    if (opened !== true) {
      results.overlays[key] = { missing: label, seen: opened };
      console.log(key, 'TRIGGER NOT FOUND', label, '::', opened);
      return;
    }
    await until(`[...document.querySelectorAll('[role="dialog"], [role="alertdialog"]')].some((o) => o.getClientRects().length > 0)`, `${key} open`, 8000);
    await sleep(900);
    await record('overlays', key, { trigger: label });
    if (/signin|auth/.test(key)) results.axe[key] = await runAxe();
  } catch (error) {
    results.overlays[key] = { error: String(error) };
    console.log(key, 'ERROR', String(error));
  } finally {
    await press('Escape', 'Escape', 27);
    await sleep(600);
    await until(`![...document.querySelectorAll('[role="dialog"], [role="alertdialog"]')].some((o) => o.getClientRects().length > 0)`, 'closed', 5000).catch(async () => {
      await press('Escape', 'Escape', 27);
      await sleep(600);
    });
  }
}

const SITE_GUEST = ['/', '/spaces', `/spaces/${SLUG}`, '/about', '/privacy', '/login', '/register', '/forgot-password', '/reset-password', '/no-such-page'];
const AUTH = new Set(['/login', '/register', '/forgot-password', '/reset-password']);
const SITE_SIGNED = ['/me/favorites', '/me/reports', '/me/settings'];

async function routesFor(who, extra) {
  await signIn(who);
  await prefs('ar', 'light');
  await load(who === GUEST ? '/' : '/dashboard');
  await until('!!document.querySelector("h1")', 'landing').catch(() => {});
  await sleep(1500);
  const paths = [...(who === GUEST ? SITE_GUEST : [])];
  if (who !== GUEST) {
    paths.push(...(await extra()));
    paths.push(...SITE_SIGNED);
  }
  const unique = [...new Set(paths)];
  console.log(who.key, 'routes', unique.length);
  for (const width of [1440, 390]) {
    await viewport(width);
    for (const path of unique) {
      const key = `${who.key}-${width}-${slug(path) || 'home'}`;
      if (ONLY && !ONLY.test(key)) continue;
      try {
        await nav(path);
        await record('routes', key);
        if (who === GUEST && AUTH.has(path)) results.axe[key] = await runAxe();
      } catch (error) {
        results.routes[key] = { error: String(error) };
        console.log(key, 'ERROR', String(error));
      }
    }
  }
}

// --- Routes, in Arabic ---
await routesFor(GUEST);
await routesFor(OWNER, async () => {
  await evaluate(`window.history.pushState(null, '', '/dashboard/spaces/${SPACE_ID}/customers'); window.dispatchEvent(new PopStateEvent('popstate')); true`);
  await sleep(2500);
  const pages = ['', 'desk', 'customers', 'payments', 'finance', 'packages', 'profile', 'announcements', 'reports', 'staff', 'audit', 'settings'];
  return [...pages.map((s) => `/dashboard/spaces/${SPACE_ID}${s ? `/${s}` : ''}`), ...(await links('/\\/customers\\/\\d+/')).slice(0, 1)];
});
await routesFor(ADMIN, async () => {
  await evaluate(`window.history.pushState(null, '', '/dashboard/admin/spaces'); window.dispatchEvent(new PopStateEvent('popstate')); true`);
  await sleep(2500);
  const pages = ['', 'spaces', 'spaces/new', 'owners', 'reports', 'users', 'lookups', 'audit', 'settings'];
  return [...pages.map((s) => `/dashboard/admin${s ? `/${s}` : ''}`), ...(await links('/^\\/dashboard\\/admin\\/spaces\\/\\d+/')).slice(0, 1)];
});

// --- Overlays, in English ---
async function overlaysFor(who, plan) {
  await signIn(who);
  await prefs('en', 'light');
  await load(who === GUEST ? '/' : '/dashboard');
  await sleep(1500);
  for (const width of [1440, 390]) {
    await viewport(width);
    for (const [path, list] of plan) {
      const resolved = typeof path === 'function' ? await path() : path;
      if (!resolved) continue;
      await nav(resolved);
      for (const [name, label, options] of list) {
        if (options?.phone && width >= 768) continue;
        await overlay(`${who.key}-${width}-${name}`, label, options);
      }
    }
  }
}
const space = (page) => `/dashboard/spaces/${SPACE_ID}/${page}`;
await overlaysFor(GUEST, [
  ['/spaces', [['directory-filters', '^Filters', { phone: true }]]],
  [`/spaces/${SLUG}`, [['signin-prompt', 'Report wrong information'], ['site-menu', '^Menu$', { phone: true }]]],
]);
let customerFile = null;
await overlaysFor(OWNER, [
  [space('desk'), [['desk-visit', '^Check in a visit$']]],
  [space('customers'), [['customers-new', '^New customer$'], ['customers-filters', '^Filters', { phone: true }]]],
  [
    async () => {
      if (customerFile) return customerFile;
      await nav(space('customers'));
      customerFile = (await links('/\\/customers\\/\\d+/'))[0] ?? null;
      return customerFile;
    },
    [['customer-subscription', 'subscription'], ['customer-edit', '^Edit']],
  ],
  [space('staff'), [['staff-add', '^Add staff member$']]],
  [space('announcements'), [['announcement-new', 'New announcement']]],
  [space('packages'), [['package-new', 'New package']]],
  [space('profile'), [['profile-edit', '^Edit the contacts'], ['profile-hours', 'opening hours']]],
  [space('payments'), [['ledger-filters', '^Filters', { phone: true }]]],
  [space('audit'), [['audit-filters', '^Filters', { phone: true }]]],
]);
await overlaysFor(ADMIN, [
  ['/dashboard/admin/spaces', [['spaces-filters', '^Filters', { phone: true }]]],
  [
    async () => {
      await nav('/dashboard/admin/spaces');
      return (await links('/^\\/dashboard\\/admin\\/spaces\\/\\d+/'))[0] ?? null;
    },
    [['space-link-owner', '^Link an owner']],
  ],
  ['/dashboard/admin/owners', [['owners-add', 'Add owner']]],
  ['/dashboard/admin/users', [['users-temporary', 'temporary password']]],
  ['/dashboard/admin/lookups', [['lookups-amenity', '^Add amenity'], ['lookups-governorate', 'Add governorate']]],
  ['/dashboard/admin/reports', [['reports-filters', '^Filters', { phone: true }]]],
  ['/dashboard/admin/audit', [['audit-filters', '^Filters', { phone: true }]]],
]);

// --- Dark, on five screens: no berry anywhere ---
const DARK = [
  [GUEST, '/'],
  [GUEST, `/spaces/${SLUG}`],
  [GUEST, '/login'],
  [OWNER, space('desk')],
  [ADMIN, '/dashboard/admin/spaces'],
];
let darkAs = null;
for (const width of [1440, 390]) {
  for (const [who, path] of DARK) {
    const key = `dark-${who.key}-${width}-${slug(path) || 'home'}`;
    if (ONLY && !ONLY.test(key)) continue;
    try {
      if (darkAs !== who) {
        await signIn(who);
        await prefs('ar', 'dark');
        await load(who === GUEST ? '/' : '/dashboard');
        await sleep(1500);
        darkAs = who;
      }
      await viewport(width);
      await nav(path);
      await record('dark', key);
    } catch (error) {
      results.dark[key] = { error: String(error) };
      console.log(key, 'ERROR', String(error));
    }
  }
}

results.refreshes = refreshes;
writeFileSync(OUT, JSON.stringify(results, null, 1));
console.log('page errors', errors.length, 'refreshes', refreshes);
socket.close();
chrome.kill();
