// WI-B's Chrome pass: the berry on the main action, in a real headless Chrome over CDP.
// Six screens (home, a space page, the directory, sign-in, the owner's desk, the admin's spaces) at
// 390 and 1440, Arabic and English, light and dark. For each: a viewport shot, every visible
// control's colours (to diff before against after), each main action's colour, its hover (1440)
// and its focus ring, and axe. Plus the desk's visit dialog, light, 1440, Arabic.
// Usage: node berry.mjs <before|after> [regex]: with a regex, only the runs it matches, merged into
// the label's earlier results. Needs the API on 3320 and the web on 5320. The passwords are
// read from the API's .env and never printed.
import { spawn } from 'node:child_process';
import { existsSync, mkdirSync, mkdtempSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const LABEL = process.argv[2] ?? 'run';
const ONLY = process.argv[3] ? new RegExp(process.argv[3]) : null;
const APP = 'C:/dev/masaha/app';
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const WEB = 'http://localhost:5320';
const SPACE_ID = 26;
const SLUG = 'pal-hub';
const SHOTS = `C:/Users/basel/Downloads/berry-shots/raw/${LABEL}`;
const OUT = `C:/dev/masaha/workspace/TASKS/BERRY_PRIMARY/scripts/out-${LABEL}.json`;
mkdirSync(SHOTS, { recursive: true });
const AXE = readFileSync(`${APP}/node_modules/axe-core/axe.min.js`, 'utf8');
const ENV = readFileSync(`${APP}/apps/api/.env`, 'utf8');
const env = (key) =>
  new RegExp(`^${key}=(.*)$`, 'm')
    .exec(ENV)?.[1]
    ?.trim()
    .replace(/^["']|["']$/g, '');
const OWNER = { email: 'demo-owner@example.com', password: env('SEED_DEMO_PASSWORD') };
const ADMIN = { email: env('SEED_ADMIN_EMAIL'), password: env('SEED_ADMIN_PASSWORD') };
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
socket.addEventListener('message', (event) => {
  const message = JSON.parse(event.data);
  if (message.id !== undefined && pending.has(message.id)) {
    const { resolve, reject } = pending.get(message.id);
    pending.delete(message.id);
    if (message.error) reject(new Error(JSON.stringify(message.error)));
    else resolve(message.result);
  } else if (message.method === 'Runtime.exceptionThrown') {
    errors.push(message.params.exceptionDetails.text);
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
const until = async (expression, what, ms = 30000) => {
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
    deviceScaleFactor: phone ? 2 : 1,
    mobile: phone,
  });
}

async function go(path) {
  await send('Page.navigate', { url: 'about:blank' });
  await sleep(120);
  await send('Page.navigate', { url: `${WEB}${path}` });
}

async function prefs(lang, theme) {
  await go('/__nothing');
  await until('document.readyState === "complete"', 'origin');
  await evaluate(
    `localStorage.setItem('masaha.language', ${JSON.stringify(lang)}); localStorage.setItem('masaha.theme', ${JSON.stringify(theme)}); true`,
  );
}

async function signIn(who) {
  await send('Network.clearBrowserCookies');
  await go('/__nothing');
  await until('document.readyState === "complete"', 'origin');
  const status = await evaluate(`fetch('/api/v1/auth/login', {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, credentials: 'include',
      body: JSON.stringify({ email: ${JSON.stringify(who.email)}, password: ${JSON.stringify(who.password)} }),
    }).then((r) => r.status)`);
  if (status !== 200) throw new Error(`sign-in ${status}`);
}

/** Every visible control: its words, whether it is the main action, and its painted colours. */
const CONTROLS = `(() => [...document.querySelectorAll('button, a, [role="button"], [role="tab"], input[type="checkbox"], [role="switch"], [role="radio"]')]
  .filter((el) => el.getClientRects().length > 0 && getComputedStyle(el).visibility !== 'hidden')
  .map((el) => { const s = getComputedStyle(el); return {
    name: (el.getAttribute('aria-label') ?? el.textContent ?? '').replace(/\\s+/g, ' ').trim().slice(0, 50),
    tag: el.tagName.toLowerCase(), slot: el.dataset.slot ?? null,
    main: el.classList.contains('bg-main-action'),
    bg: s.backgroundColor, color: s.color, border: s.borderTopColor }; }))()`;

/** The main actions in view or in the page, with their painted colours. */
const MAINS = `[...document.querySelectorAll('.bg-main-action')].filter((el) => el.getClientRects().length > 0)
  .map((el) => { const s = getComputedStyle(el); return { name: el.textContent.replace(/\\s+/g, ' ').trim().slice(0, 50), bg: s.backgroundColor, color: s.color }; })`;

async function runAxe() {
  if (!(await evaluate('typeof window.axe !== "undefined"'))) await evaluate(`${AXE}; true`);
  return evaluate(`axe.run(document, { resultTypes: ['violations'] }).then((r) => r.violations.map((v) => ({
      id: v.id, impact: v.impact, nodes: v.nodes.length, targets: v.nodes.slice(0, 3).map((n) => n.target.join(' ')) })))`);
}

async function shot(file, clip) {
  const { data } = await send('Page.captureScreenshot', { format: 'png', ...(clip && { clip: { ...clip, scale: 1 } }) });
  writeFileSync(`${SHOTS}/${file}.png`, Buffer.from(data, 'base64'));
}

const press = async (key, code, keyCode) => {
  await send('Input.dispatchKeyEvent', { type: 'rawKeyDown', key, code, windowsVirtualKeyCode: keyCode });
  await send('Input.dispatchKeyEvent', { type: 'keyUp', key, code, windowsVirtualKeyCode: keyCode });
};

/** The first main action in the page, centred: its box in page coordinates. */
async function firstMain() {
  return evaluate(`(() => { const el = [...document.querySelectorAll('.bg-main-action')].find((e) => e.getClientRects().length > 0);
    if (!el) return null; el.scrollIntoView({ block: 'center' }); const b = el.getBoundingClientRect();
    return { x: b.x, y: b.y, w: b.width, h: b.height, sx: scrollX, sy: scrollY }; })()`);
}

async function hoverAndFocus(base, width) {
  const result = {};
  const box = await firstMain();
  if (!box) return { none: true };
  await sleep(300);
  const crop = { x: Math.max(0, box.x - 16) + box.sx, y: Math.max(0, box.y - 16) + box.sy, width: box.w + 32, height: box.h + 32 };
  if (width >= 768) {
    await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: box.x + box.w / 2, y: box.y + box.h / 2 });
    await sleep(350);
    result.hover = await evaluate(`(() => { const el = [...document.querySelectorAll('.bg-main-action')].find((e) => e.getClientRects().length > 0);
      return { hovered: el.matches(':hover'), bg: getComputedStyle(el).backgroundColor }; })()`);
    await shot(`${base}-hover`, crop);
    await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: 1, y: 1 });
    await sleep(250);
  }
  await press('Shift', 'ShiftLeft', 16);
  await evaluate(`[...document.querySelectorAll('.bg-main-action')].find((e) => e.getClientRects().length > 0).focus(); true`);
  // transition-colors moves the outline from currentColor to the ring over 150 ms: read it after.
  await sleep(400);
  result.focus = await evaluate(`(() => { const el = document.activeElement; const s = getComputedStyle(el);
    return { main: el.classList.contains('bg-main-action'), focusVisible: el.matches(':focus-visible'), outline: s.outlineStyle + ' ' + s.outlineWidth + ' ' + s.outlineColor, offset: s.outlineOffset }; })()`);
  await shot(`${base}-focus`, crop);
  await evaluate('document.activeElement?.blur(); true');
  return result;
}

const SCREENS = [
  { key: 'home', path: '/', who: null, ready: 'h1' },
  { key: 'space', path: `/spaces/${SLUG}`, who: null, ready: 'h1', widths: [390, 800, 1440] },
  { key: 'directory', path: '/spaces', who: null, ready: 'h1' },
  { key: 'signin', path: '/login', who: null, ready: 'form' },
  { key: 'desk', path: `/dashboard/spaces/${SPACE_ID}/desk`, who: OWNER, ready: 'h1' },
  { key: 'admin', path: '/dashboard/admin/spaces', who: ADMIN, ready: 'h1' },
  { key: 'packages', path: `/dashboard/spaces/${SPACE_ID}/packages`, who: OWNER, ready: 'h1' },
];
const results = ONLY && existsSync(OUT) ? JSON.parse(readFileSync(OUT, 'utf8')) : {};
let signedAs = null;
for (const screen of SCREENS) {
  if (screen.who !== signedAs) {
    if (screen.who) await signIn(screen.who);
    else await send('Network.clearBrowserCookies');
    signedAs = screen.who;
  }
  for (const width of screen.widths ?? [390, 1440]) {
    for (const lang of ['ar', 'en']) {
      for (const theme of ['light', 'dark']) {
        const base = `${screen.key}-${width}-${lang}-${theme}`;
        if (ONLY && !ONLY.test(base)) continue;
        try {
          await viewport(width);
          await prefs(lang, theme);
          await go(screen.path);
          await until(`!!document.querySelector(${JSON.stringify(screen.ready)})`, `${base} ready`);
          await sleep(1800);
          const state = await evaluate(`({ lang: document.documentElement.lang, theme: document.documentElement.dataset.theme, path: location.pathname,
            overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth })`);
          // React Router restores a path's scroll from the last run: start each shot at the top.
          await evaluate('window.scrollTo(0, 0); true');
          await sleep(300);
          await shot(base);
          if (await firstMain()) {
            await sleep(300);
            await shot(`${base}-main`);
          }
          const controls = await evaluate(CONTROLS);
          const mains = await evaluate(MAINS);
          const interact = await hoverAndFocus(base, width);
          const axe = await runAxe();
          results[base] = { state, mains, interact, axe, controls };
          console.log(base, state.path, state.lang, state.theme, 'mains', mains.length, 'axe', axe.length);
        } catch (error) {
          results[base] = { error: String(error) };
          console.log(base, 'ERROR', String(error));
        }
      }
    }
  }
}

// The desk's visit dialog: an overlay's confirming action, light, 1440, Arabic and English.
for (const lang of ['ar', 'en']) {
  const base = `desk-dialog-1440-${lang}-light`;
  if (ONLY && !ONLY.test(base)) continue;
  try {
    if (signedAs !== OWNER) await signIn(OWNER);
    signedAs = OWNER;
    await viewport(1440);
    await prefs(lang, 'light');
    await go(`/dashboard/spaces/${SPACE_ID}/desk`);
    await until('!!document.querySelector("h1")', 'desk');
    await sleep(1500);
    await evaluate(`(() => { const b = [...document.querySelectorAll('header button')].find((e) => /تسجيل زيارة|Check in a visit/.test(e.textContent)); b.click(); return true; })()`);
    await until('!!document.querySelector("[role=dialog]")', 'visit dialog');
    await sleep(800);
    await shot(base);
    const mains = await evaluate(MAINS);
    const axe = await runAxe();
    results[base] = { mains, axe };
    console.log(base, 'mains', mains.length, 'axe', axe.length);
  } catch (error) {
    results[base] = { error: String(error) };
    console.log(base, 'ERROR', String(error));
  }
}

results.errors = errors;
writeFileSync(OUT, JSON.stringify(results, null, 1));
console.log('page errors', errors.length);
socket.close();
chrome.kill();
