// AXE_FIXES (finding 224): axe-core in a real, headless Chrome on the three places — the owner's
// profile «الصور», Finance › Occupancy, and the directory's map with a mark chosen and one hovered —
// at 390 and 1440 (and 320 for the photos), light and dark, Arabic and English. Records every
// violation per run, the sideways scrollers found, and captures each strip's focus ring at 390/320.
// Usage: node axe.mjs <label>   (label: main | branch). Needs the API on 3320 and the web on 5320.
import { spawn } from 'node:child_process';
import { mkdirSync, mkdtempSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const LABEL = process.argv[2] ?? 'run';
// Optional: the screens to run, comma-separated (photos,occupancy,map); all by default.
const ONLY = process.argv[3]?.split(',') ?? ['photos', 'occupancy', 'map'];
const APP = 'C:/dev/masaha/app';
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const WEB = 'http://localhost:5320';
const SPACE = 26;
const OUT = `C:/dev/masaha/workspace/TASKS/AXE_FIXES/scripts/out-${LABEL}.json`;
const SHOTS = `C:/Users/basel/Downloads/axe-fixes-shots/${LABEL}`;
mkdirSync(SHOTS, { recursive: true });
const AXE = readFileSync(`${APP}/node_modules/axe-core/axe.min.js`, 'utf8');
// Read here, never printed.
const PASSWORD = /^SEED_DEMO_PASSWORD=(.*)$/m
  .exec(readFileSync(`${APP}/apps/api/.env`, 'utf8'))?.[1]
  ?.trim()
  .replace(/^["']|["']$/g, '');
if (!PASSWORD) throw new Error('SEED_DEMO_PASSWORD missing');
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
  const result = await send('Runtime.evaluate', {
    expression,
    awaitPromise: true,
    returnByValue: true,
  });
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
  await sleep(150);
  await send('Page.navigate', { url: `${WEB}${path}` });
}

async function prefs(lang, theme) {
  await go('/__nothing');
  await until('document.readyState === "complete"', 'origin');
  await evaluate(
    `localStorage.setItem('masaha.language', ${JSON.stringify(lang)}); localStorage.setItem('masaha.theme', ${JSON.stringify(theme)}); true`,
  );
}

async function signIn() {
  await go('/login');
  await until('document.readyState === "complete"', 'login page');
  const status = await evaluate(`fetch('/api/v1/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ email: 'demo-owner@example.com', password: ${JSON.stringify(PASSWORD)} }),
    }).then((r) => r.status)`);
  console.log('sign-in status', status);
  if (status !== 200) throw new Error(`sign-in ${status}`);
}

/** Every element that scrolls sideways with more than it shows, and its name, role and tab stop. */
const SCROLLERS = `(() => [...document.querySelectorAll('body *')]
  .filter((el) => {
    const s = getComputedStyle(el);
    return (s.overflowX === 'auto' || s.overflowX === 'scroll') && el.scrollWidth > el.clientWidth
      && el.getClientRects().length > 0;
  })
  .map((el) => ({
    tag: el.tagName.toLowerCase(),
    slot: el.dataset.slot ?? null,
    role: el.getAttribute('role'),
    label: el.getAttribute('aria-label') ?? (el.getAttribute('aria-labelledby') ? document.getElementById(el.getAttribute('aria-labelledby'))?.textContent : null),
    tabindex: el.getAttribute('tabindex'),
    scroll: el.scrollWidth, client: el.clientWidth,
  })))()`;

/** The fitting regions: the layer's scroll regions that show all they hold. */
const REGIONS = `[...document.querySelectorAll('[data-slot="scroll-region"]')].map((el) => ({
  label: el.getAttribute('aria-label') ?? document.getElementById(el.getAttribute('aria-labelledby') ?? '')?.textContent ?? null,
  tabindex: el.getAttribute('tabindex'), scroll: el.scrollWidth, client: el.clientWidth }))`;

async function runAxe() {
  const has = await evaluate('typeof window.axe !== "undefined"');
  if (!has) await evaluate(`${AXE}; true`);
  return evaluate(`axe.run(document, { resultTypes: ['violations'] }).then((r) => r.violations.map((v) => ({
      id: v.id, impact: v.impact, nodes: v.nodes.length,
      targets: v.nodes.slice(0, 4).map((n) => n.target.join(' ')) })))`);
}

async function state() {
  return evaluate(`({ lang: document.documentElement.lang, dir: document.documentElement.dir,
    theme: document.documentElement.dataset.theme,
    pageScroll: document.documentElement.scrollWidth, pageClient: document.documentElement.clientWidth })`);
}

const press = async (key, code, keyCode, shift = false) => {
  const modifiers = shift ? 8 : 0;
  await send('Input.dispatchKeyEvent', { type: 'rawKeyDown', key, code, windowsVirtualKeyCode: keyCode, modifiers });
  await send('Input.dispatchKeyEvent', { type: 'keyUp', key, code, windowsVirtualKeyCode: keyCode, modifiers });
};

/** Tab from the page's start until a sideways strip of the layer has the focus; shoot its ring. */
async function ringShot(name) {
  const found = await evaluate(
    `!!document.querySelector('[data-slot="scroll-region"][tabindex="0"]')`,
  );
  if (!found) return { name, focused: false, why: 'no scroll region with a tab stop' };
  await evaluate(`document.activeElement?.blur(); window.scrollTo(0, 0); document.body.focus(); true`);
  for (let i = 0; i < 80; i += 1) {
    await press('Tab', 'Tab', 9);
    await sleep(40);
    const on = await evaluate(
      `document.activeElement?.matches('[data-slot="scroll-region"]') ?? false`,
    );
    if (on) {
      await evaluate(`document.activeElement.scrollIntoView({ block: 'center' }); true`);
      await sleep(400);
      const box = await evaluate(`(() => { const b = document.activeElement.getBoundingClientRect();
        const s = getComputedStyle(document.activeElement);
        return { x: b.x + scrollX, y: b.y + scrollY, w: b.width, h: b.height, outline: s.outlineStyle + ' ' + s.outlineWidth + ' ' + s.outlineColor,
          focusVisible: document.activeElement.matches(':focus-visible') }; })()`);
      const m = 16;
      const { data } = await send('Page.captureScreenshot', {
        format: 'png',
        clip: {
          x: Math.max(0, box.x - m),
          y: Math.max(0, box.y - m),
          width: box.w + 2 * m,
          height: box.h + 2 * m,
          scale: 1,
        },
      });
      writeFileSync(`${SHOTS}/${name}.png`, Buffer.from(data, 'base64'));
      return { name, focused: true, tabs: i + 1, ...box };
    }
  }
  return { name, focused: false, why: 'not reached in 80 tabs' };
}

async function fullShot(name) {
  const { data } = await send('Page.captureScreenshot', { format: 'png' });
  writeFileSync(`${SHOTS}/${name}.png`, Buffer.from(data, 'base64'));
}

const centreOf = (selector) =>
  evaluate(`(() => { const b = document.querySelector(${JSON.stringify(selector)}).getBoundingClientRect();
    return { x: Math.round(b.x + b.width / 2), y: Math.round(b.y + b.height / 2) }; })()`);
const mouse = async (type, { x, y }) =>
  send('Input.dispatchMouseEvent', { type, x, y, button: 'left', clickCount: type === 'mouseMoved' ? 0 : 1 });

const results = [];
const rings = [];

async function screen(kind, width, lang, theme) {
  const tag = `${kind}-${lang}-${theme}-${width}`;
  const entry = { screen: kind, width, lang, theme };
  try {
    if (kind === 'photos') {
      await go(`/dashboard/spaces/${SPACE}/profile#photos`);
      await until(`document.querySelectorAll('#photos img').length > 0`, `${tag} photos`);
      await evaluate(`document.getElementById('photos').scrollIntoView({ block: 'start' }); true`);
    } else if (kind === 'occupancy') {
      await go(`/dashboard/spaces/${SPACE}/finance?tab=occupancy`);
      await until(`!!document.querySelector('[data-slot="heatmap-cell"]')`, `${tag} heatmap`);
    } else {
      await go('/spaces?view=map');
      await until(`document.querySelectorAll('.map-mark').length > 1`, `${tag} marks`);
      await sleep(800);
    }
    await sleep(900);
    entry.state = await state();
    if (kind === 'map') {
      // A mark chosen by a click: its tooltip permanent. The mark clicked is one drawn on top at
      // its centre, inside the map's box (not under its legend or a card).
      entry.marks = await evaluate(`document.querySelectorAll('.map-mark').length`);
      const PICK = (mark) => `(() => { const box = document.querySelector('[role="application"]').getBoundingClientRect();
        const m = [...document.querySelectorAll('.map-mark')].find((el) => {
          if (${mark === 'other' ? "el.getAttribute('aria-pressed') === 'true'" : 'false'}) return false;
          const b = el.getBoundingClientRect(); const x = b.x + b.width / 2, y = b.y + b.height / 2;
          return b.width > 0 && x > box.left + 40 && x < box.right - 40 && y > box.top + 60 && y < box.bottom - 120
            && y < innerHeight * 0.6 && (document.elementFromPoint(x, y) === el || el.contains(document.elementFromPoint(x, y)));
        });
        if (!m) return null; m.dataset.axe = '${mark}'; return true; })()`;
      await evaluate(`document.querySelector('[role="application"]').scrollIntoView({ block: 'start' }); true`);
      await sleep(400);
      if (!(await evaluate(PICK('chosen')))) throw new Error('no mark in view to click');
      const at = await centreOf('[data-axe="chosen"]');
      await mouse('mouseMoved', at);
      await mouse('mousePressed', at);
      await mouse('mouseReleased', at);
      await until(`!!document.querySelector('.map-mark[aria-pressed="true"]')`, `${tag} chosen`, 10000);
      await sleep(700);
      entry.tooltip = await evaluate(`[...document.querySelectorAll('.map-tooltip')].map((t) => ({
        role: t.getAttribute('role'), hidden: t.getAttribute('aria-hidden'), text: t.textContent }))`);
      entry.describedby = await evaluate(`[...document.querySelectorAll('.map-mark')].filter((m) => m.hasAttribute('aria-describedby')).length`);
      entry.violations = await runAxe();
      await fullShot(`${tag}-chosen`);
      // Another mark hovered: a passing tooltip beside it.
      await mouse('mouseMoved', { x: 2, y: 2 });
      await sleep(300);
      const other = await evaluate(PICK('other'));
      if (other) {
        await mouse('mouseMoved', await centreOf('[data-axe="other"]'));
        await sleep(600);
        entry.hoverTooltip = await evaluate(`[...document.querySelectorAll('.map-tooltip')].map((t) => ({
          hidden: t.getAttribute('aria-hidden'), text: t.textContent }))`);
        entry.hoverDescribedby = await evaluate(`[...document.querySelectorAll('.map-mark')].filter((m) => m.hasAttribute('aria-describedby')).length`);
        entry.hoverViolations = await runAxe();
      } else {
        entry.hoverViolations = 'no other mark in view';
      }
    } else {
      entry.scrollers = await evaluate(SCROLLERS);
      entry.regions = await evaluate(REGIONS);
      entry.violations = await runAxe();
      if (width < 768) await fullShot(tag);
      if (width < 768 && (lang === 'ar' || theme === 'light')) rings.push(await ringShot(`ring-${tag}`));
    }
  } catch (error) {
    entry.error = String(error.message ?? error);
  }
  results.push(entry);
  const brief = (list) =>
    Array.isArray(list) ? list.map((v) => `${v.id}(${v.nodes})`).join(' ') || 'none' : String(list);
  console.log(tag, entry.error ?? brief(entry.violations), entry.hoverViolations ? `| hover: ${brief(entry.hoverViolations)}` : '');
}

try {
  await viewport(1440);
  await signIn();
  for (const lang of ['ar', 'en']) {
    for (const theme of ['light', 'dark']) {
      await prefs(lang, theme);
      for (const width of [390, 1440]) {
        await viewport(width);
        for (const kind of ['photos', 'occupancy', 'map'].filter((k) => ONLY.includes(k))) await screen(kind, width, lang, theme);
      }
      await viewport(320);
      if (ONLY.includes('photos')) await screen('photos', 320, lang, theme);
    }
  }
} finally {
  writeFileSync(OUT, JSON.stringify({ label: LABEL, results, rings, errors }, null, 1));
  console.log('rings', JSON.stringify(rings));
  console.log('page errors', errors.length, JSON.stringify(errors.slice(0, 5)));
  socket.close();
  chrome.kill();
}
