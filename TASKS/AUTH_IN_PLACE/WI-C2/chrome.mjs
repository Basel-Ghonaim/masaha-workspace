// WI-C2's Chrome pass: the sign-in over a space's page in a real headless Chrome, over CDP.
// Needs the API on 3323 and the web on 5323 (app-design). Shots to Downloads\c2-shots; findings to
// chrome-out.json beside this file. The demo owner's password is read from the API's .env and never
// printed. Usage: node chrome.mjs [matrix|flows|google|all]
import { spawn } from 'node:child_process';
import { mkdirSync, mkdtempSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const MODE = process.argv[2] ?? 'all';
const APP = 'C:/dev/masaha/app-design';
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const WEB = 'http://localhost:5323';
const SPACE = '/spaces/pal-hub';
const OWNER = 'demo-owner@example.com';
const SHOTS = 'C:/Users/basel/Downloads/c2-shots';
const OUT = `C:/dev/masaha/workspace/TASKS/AUTH_IN_PLACE/WI-C2/chrome-out-${MODE}.json`;
mkdirSync(SHOTS, { recursive: true });
const AXE = readFileSync(`${APP}/node_modules/axe-core/axe.min.js`, 'utf8');
const ENV = readFileSync(`${APP}/apps/api/.env`, 'utf8');
const PASSWORD = /^SEED_DEMO_PASSWORD=(.*)$/m
  .exec(ENV)?.[1]
  ?.trim()
  .replace(/^["']|["']$/g, '');
if (!PASSWORD) throw new Error('SEED_DEMO_PASSWORD missing');
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const results = {};

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

/** A CDP session on one page target. */
async function connect(url) {
  const socket = new WebSocket(url);
  await new Promise((resolve) => socket.addEventListener('open', resolve));
  let id = 0;
  const pending = new Map();
  const errors = [];
  const listeners = [];
  socket.addEventListener('message', (event) => {
    const message = JSON.parse(event.data);
    if (message.id !== undefined && pending.has(message.id)) {
      const { resolve, reject } = pending.get(message.id);
      pending.delete(message.id);
      if (message.error) reject(new Error(JSON.stringify(message.error)));
      else resolve(message.result);
    } else if (message.method === 'Runtime.exceptionThrown') {
      errors.push(message.params.exceptionDetails.exception?.description ?? 'exception');
    } else if (message.method) {
      for (const listener of listeners) listener(message);
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
      throw new Error(result.exceptionDetails.exception?.description ?? 'evaluate failed');
    }
    return result.result.value;
  };
  await send('Page.enable');
  await send('Runtime.enable');
  return { send, evaluate, errors, listeners, close: () => socket.close() };
}

const browser = null && await connect(
  (await (await fetch(`http://127.0.0.1:${port}/json/version`)).json()).webSocketDebuggerUrl,
).catch(() => null);

const page = await connect(targets.find((t) => t.type === 'page').webSocketDebuggerUrl);
const { send, evaluate } = page;

async function viewport(width) {
  await send('Emulation.setDeviceMetricsOverride', {
    width,
    height: width < 768 ? 844 : 900,
    deviceScaleFactor: 1,
    mobile: width < 768,
  });
}

async function waitFor(expression, ms = 8000) {
  const end = Date.now() + ms;
  while (Date.now() < end) {
    if (await evaluate(`Boolean(${expression})`).catch(() => false)) return true;
    await sleep(100);
  }
  return false;
}

async function go(path, { lang, theme } = {}) {
  await send('Page.navigate', { url: 'about:blank' });
  await sleep(200);
  await send('Page.navigate', { url: `${WEB}${path}` });
  await waitFor('document.readyState === "complete"');
  if (lang || theme) {
    await evaluate(
      `localStorage.setItem('masaha.language', '${lang}'); localStorage.setItem('masaha.theme', '${theme}'); true`,
    );
    await send('Page.reload');
    await sleep(300);
    await waitFor('document.readyState === "complete"');
  }
  await waitFor('document.querySelector("h1")', 15000);
  await sleep(400);
}

async function shot(name) {
  const { data } = await send('Page.captureScreenshot', { format: 'png' });
  writeFileSync(`${SHOTS}/${name}.png`, Buffer.from(data, 'base64'));
}

async function axe(label) {
  const has = await evaluate('typeof window.axe !== "undefined"');
  if (!has) await evaluate(`${AXE}; true`);
  const violations = await evaluate(
    `axe.run(document, { resultTypes: ['violations'] }).then(r => r.violations.map(v => ({ id: v.id, impact: v.impact, nodes: v.nodes.map(n => n.target.join(' ')).slice(0, 4) })))`,
  );
  results[`axe ${label}`] = violations;
  return violations;
}

const dialog = 'document.querySelector("[data-slot=adaptive-dialog-content]")';
const inDialog = (selector) => `${dialog}?.querySelector(${JSON.stringify(selector)})`;
const buttonByText = (text) =>
  `[...(${dialog}?.querySelectorAll('button') ?? [])].find(b => b.textContent.trim() === ${JSON.stringify(text)})`;
const heart = 'document.querySelector("button[aria-pressed]")';
const active = `(() => { const a = document.activeElement; return a ? (a.getAttribute('data-slot') || a.getAttribute('aria-label') || a.getAttribute('autocomplete') || a.tagName) : null; })()`;

async function typeInto(selector, text) {
  await evaluate(`${inDialog(selector)}.focus(); true`);
  await send('Input.insertText', { text });
  await sleep(50);
}

async function key(keyName, code, keyCode, shift = false) {
  const modifiers = shift ? 8 : 0;
  await send('Input.dispatchKeyEvent', { type: 'keyDown', key: keyName, code, windowsVirtualKeyCode: keyCode, modifiers });
  await send('Input.dispatchKeyEvent', { type: 'keyUp', key: keyName, code, windowsVirtualKeyCode: keyCode, modifiers });
  await sleep(150);
}

async function openOverlay() {
  await evaluate(`${heart}.focus(); ${heart}.click(); true`);
  await waitFor(inDialog('input[type=email]'), 10000);
  await sleep(500);
}

async function signedOut() {
  await send('Network.enable');
  await send('Network.clearBrowserCookies');
  await evaluate('(() => { try { localStorage.clear(); } catch { /* about:blank */ } return true; })()');
}

const words = {
  ar: { create: 'إنشاء حساب', forgot: 'نسيت كلمة المرور؟', signIn: 'تسجيل الدخول', send: 'أرسل رابط الاستعادة', report: 'الإبلاغ عن معلومة غير صحيحة' },
  en: { create: 'Create account', forgot: 'Forgot password?', signIn: 'Sign in', send: 'Send reset link', report: 'Report wrong information' },
};

async function matrix() {
  for (const width of [390, 1440]) {
    await viewport(width);
    for (const lang of ['ar', 'en']) {
      for (const theme of ['light', 'dark']) {
        const tag = `${width}-${lang}-${theme}`;
        await signedOut();
        await go(SPACE, { lang, theme });
        await openOverlay();
        results[`focus on open ${tag}`] = await evaluate(active);
        results[`form ${tag}`] = await evaluate(`${dialog}?.getAttribute('data-form')`);
        await shot(`signin-${tag}`);
        await axe(`signin ${tag}`);
        await evaluate(`${buttonByText(words[lang].create)}.click(); true`);
        await sleep(400);
        results[`focus on register ${tag}`] = await evaluate(active);
        await shot(`register-${tag}`);
        await axe(`register ${tag}`);
        await evaluate(`${buttonByText(words[lang].signIn)}.click(); true`);
        await sleep(300);
        await evaluate(`${buttonByText(words[lang].forgot)}.click(); true`);
        await waitFor(buttonByText(words[lang].send));
        await sleep(300);
        results[`focus on forgot ${tag}`] = await evaluate(active);
        await shot(`forgot-${tag}`);
        await axe(`forgot ${tag}`);
      }
    }
  }
}

async function flows() {
  for (const [width, lang] of [
    [390, 'ar'],
    [1440, 'en'],
  ]) {
    const w = words[lang];
    const tag = `${width}-${lang}`;
    await viewport(width);

    // Escape (wide) or Back (phone) closes it; the focus goes back to the heart; the action let go.
    await signedOut();
    await go(SPACE, { lang, theme: 'light' });
    const historyBefore = await evaluate('history.length');
    await openOverlay();
    results[`history entry added ${tag}`] = (await evaluate('history.length')) - historyBefore;
    if (width === 390) await evaluate('history.back(); true');
    else await key('Escape', 'Escape', 27);
    await sleep(600);
    results[`closed by ${width === 390 ? 'Back' : 'Escape'} ${tag}`] = await evaluate(`!${dialog}`);
    results[`focus after close ${tag}`] = await evaluate(active);
    results[`url after close ${tag}`] = await evaluate('location.pathname');
    results[`held intent after close ${tag}`] = await evaluate("localStorage.getItem('masaha.heldIntent')");

    // Wrong password: the alert, the overlay open.
    await openOverlay();
    await typeInto('input[type=email]', OWNER);
    await typeInto('input[autocomplete=current-password]', 'not-the-password-1');
    await evaluate(`${buttonByText(w.signIn)}.click(); true`);
    await waitFor(inDialog('[role=alert]'));
    results[`wrong password alert ${tag}`] = await evaluate(`${inDialog('[role=alert]')}?.textContent`);
    await shot(`wrong-${tag}`);
    await axe(`wrong ${tag}`);

    // The real sign-in from the heart: closed, the page kept, the heart saved, the focus on it.
    await evaluate(`${inDialog('input[autocomplete=current-password]')}.select(); true`);
    await send('Input.insertText', { text: PASSWORD });
    const urlBefore = await evaluate('location.href');
    await evaluate(`${buttonByText(w.signIn)}.click(); true`);
    await waitFor(`!${dialog}`, 10000);
    await waitFor(`${heart}?.getAttribute('aria-pressed') === 'true'`, 10000);
    await sleep(600);
    results[`signed in, closed ${tag}`] = await evaluate(`!${dialog}`);
    results[`url kept ${tag}`] = (await evaluate('location.href')) === urlBefore;
    results[`heart pressed ${tag}`] = await evaluate(`${heart}?.getAttribute('aria-pressed')`);
    results[`focus on heart ${tag}`] = await evaluate(`document.activeElement === ${heart}`);
    results[`toasts ${tag}`] = await evaluate(
      `[...document.querySelectorAll('[data-sonner-toast]')].map(t => t.textContent)`,
    );
    await shot(`signed-in-saved-${tag}`);
    // Clean up: the demo owner's favourite removed again.
    await evaluate(`${heart}.click(); true`);
    await sleep(1500);

    // The report: signed out, the report link, the sign-in, its dialog open.
    await signedOut();
    await go(SPACE, { lang, theme: 'light' });
    await evaluate(
      `[...document.querySelectorAll('button')].find(b => b.textContent.trim() === ${JSON.stringify(w.report)}).click(); true`,
    );
    await waitFor(inDialog('input[type=email]'), 10000);
    await typeInto('input[type=email]', OWNER);
    await typeInto('input[autocomplete=current-password]', PASSWORD);
    await evaluate(`${buttonByText(w.signIn)}.click(); true`);
    await waitFor('document.querySelector("[data-slot=dialog-content] textarea, [data-slot=dialog-content] form")', 10000);
    await sleep(500);
    results[`report dialog open ${tag}`] = await evaluate(
      'document.querySelector("[data-slot=dialog-content] [data-slot=dialog-title]")?.textContent',
    );
    await shot(`report-open-${tag}`);
    await key('Escape', 'Escape', 27);

    // The reset request: the link sent with its NEW line; then A1 from a second tab.
    await signedOut();
    await go(SPACE, { lang, theme: 'light' });
    await openOverlay();
    await typeInto('input[type=email]', OWNER);
    await evaluate(`${buttonByText(w.forgot)}.click(); true`);
    await waitFor(buttonByText(w.send));
    await evaluate(`${buttonByText(w.send)}.click(); true`);
    await waitFor(`${dialog}?.textContent.includes('•••')`, 10000);
    await sleep(500);
    results[`sent view ${tag}`] = await evaluate(`${dialog}?.textContent`);
    await shot(`sent-${tag}`);
    await axe(`sent ${tag}`);
    const second = await send('Target.createTarget', { url: `${WEB}/about` });
    await sleep(2500);
    const list = await (await fetch(`http://127.0.0.1:${port}/json`)).json();
    const other = await connect(list.find((t) => t.id === second.targetId).webSocketDebuggerUrl);
    await other.evaluate(`localStorage.setItem('masaha.recoveredAt', String(Date.now())); true`);
    await sleep(800);
    other.close();
    await send('Target.activateTarget', { targetId: targets.find((t) => t.type === 'page').id }).catch(() => undefined);
    results[`A1 email filled ${tag}`] = await evaluate(`${inDialog('input[type=email]')}?.value`);
    results[`A1 focus ${tag}`] = await evaluate(active);
    results[`A1 notice ${tag}`] = await evaluate(`${inDialog('[role=status]')}?.textContent`);
    await shot(`changed-${tag}`);
    await axe(`changed ${tag}`);
  }

  // The reset link's page, opened from the email's link in this browser, a favourite held: its line.
  await viewport(390);
  await signedOut();
  await go(SPACE, { lang: 'ar', theme: 'light' });
  await openOverlay();
  await typeInto('input[type=email]', OWNER);
  await evaluate(`${buttonByText(words.ar.forgot)}.click(); true`);
  await waitFor(buttonByText(words.ar.send));
  await evaluate(`${buttonByText(words.ar.send)}.click(); true`);
  await waitFor(`${dialog}?.textContent.includes('•••')`, 10000);
  await sleep(1500);
  const log = readFileSync(
    'C:/Users/basel/AppData/Local/Temp/claude/f145cdd22201fd2b/850f2d73-eb05-4c81-abf5-39fe482055ec/scratchpad/api.log',
    'utf8',
  );
  const links = [...log.matchAll(/https?:\/\/[^\s"]*reset-password#token=[A-Za-z0-9_-]+/g)];
  const link = links.at(-1)?.[0];
  results['reset link found in the log'] = Boolean(link);
  if (link) {
    const path = new URL(link);
    await send('Page.navigate', { url: `${WEB}${path.pathname}${path.hash}` });
    await waitFor('document.querySelector("[autocomplete=new-password]")', 15000);
    await sleep(800);
    results['reset page return line'] = await evaluate(
      `[...document.querySelectorAll('[role=status]')].map(s => s.textContent)`,
    );
    await shot('reset-form-390-ar-light');
    await axe('reset form 390 ar light');
  }
}

async function google() {
  for (const width of [390, 1440]) {
    await viewport(width);
    await signedOut();
    await go(SPACE, { lang: 'en', theme: 'light' });
    await openOverlay();
    const ready = await waitFor(inDialog('iframe'), 10000);
    results[`google iframe in overlay ${width}`] = ready;
    if (!ready) continue;
    await sleep(1500);
    await shot(`google-${width}-en-light`);
    // Keyboard: from the email field, Shift+Tab reaches Google's frame; Tab returns to the email.
    await evaluate(`${inDialog('input[type=email]')}.focus(); true`);
    await key('Tab', 'Tab', 9, true);
    results[`shift-tab from email ${width}`] = await evaluate(
      '(() => { const a = document.activeElement; return [a?.tagName, a?.getAttribute("role"), a?.getAttribute("aria-labelledby") ? document.getElementById(a.getAttribute("aria-labelledby"))?.textContent : a?.textContent?.trim().slice(0, 40), Boolean(a?.closest("[data-slot=adaptive-dialog-content]"))].join(" | "); })()',
    );
    // Enter on Google's own button opens its window, as a press does.
    const beforeEnter = (await (await fetch(`http://127.0.0.1:${port}/json`)).json()).map((t) => t.url);
    await key('Enter', 'Enter', 13);
    await sleep(3000);
    const afterEnter = (await (await fetch(`http://127.0.0.1:${port}/json`)).json()).map((t) => t.url);
    results[`enter on Google's button ${width}`] = afterEnter
      .filter((u) => !beforeEnter.includes(u))
      .map((u) => u.split('?')[0]);
    for (const t of (await (await fetch(`http://127.0.0.1:${port}/json`)).json()).filter((t) => t.url.includes('accounts.google.com') && t.type === 'page')) {
      await fetch(`http://127.0.0.1:${port}/json/close/${t.id}`);
    }
    await sleep(1000);
    results[`after Enter, overlay open ${width}`] = await evaluate(`Boolean(${dialog})`);
    await evaluate(`${inDialog('input[type=email]')}.focus(); true`);
    await key('Tab', 'Tab', 9, true);
    await key('Tab', 'Tab', 9);
    results[`tab back ${width}`] = await evaluate(active);
    // The popup: a click on the frame's button opens Google's window; closing it shows nothing.
    const box = await evaluate(
      `(() => { const r = ${inDialog('iframe')}.getBoundingClientRect(); return { x: r.x + r.width / 2, y: r.y + r.height / 2 }; })()`,
    );
    const before = (await (await fetch(`http://127.0.0.1:${port}/json`)).json()).length;
    for (const type of ['mousePressed', 'mouseReleased']) {
      await send('Input.dispatchMouseEvent', { type, x: box.x, y: box.y, button: 'left', clickCount: 1 });
    }
    await sleep(3000);
    const after = await (await fetch(`http://127.0.0.1:${port}/json`)).json();
    const popup = after.find((t) => t.type === 'page' && t.url.includes('accounts.google.com'));
    results[`popup opened ${width}`] = popup ? popup.url.split('?')[0] : `targets ${before} -> ${after.length}`;
    if (popup) {
      await fetch(`http://127.0.0.1:${port}/json/close/${popup.id}`);
      await sleep(1000);
    }
    results[`after popup closed, overlay open ${width}`] = await evaluate(`Boolean(${dialog})`);
    results[`after popup closed, alert ${width}`] = await evaluate(`${inDialog('[role=alert]')}?.textContent ?? null`);
  }
}

try {
  if (MODE === 'matrix' || MODE === 'all') await matrix();
  if (MODE === 'flows' || MODE === 'all') await flows();
  if (MODE === 'google' || MODE === 'all') await google();
} catch (error) {
  results.error = String(error.stack ?? error);
} finally {
  results.pageErrors = page.errors;
  writeFileSync(OUT, JSON.stringify(results, null, 2));
  page.close();
  browser?.close();
  chrome.kill();
  console.log('written', OUT);
}
