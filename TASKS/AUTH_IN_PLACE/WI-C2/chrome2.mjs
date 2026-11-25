// WI-C2's fix round, the plan's Review Focus checks in a real headless Chrome over CDP: (a) a
// temporary password's history after a sign-in over the page; (b) the overlay over a card's heart on
// Home and the directory, the focus back on that heart; (c) slow 3G and offline: the loading line and
// the chunk's retry. Needs the API on 3323 and the web on 5323 (app-design). Secrets are read from the
// API's .env and never printed. Usage: node chrome2.mjs [temporary|cards|network|all]
import { spawn } from 'node:child_process';
import { mkdirSync, mkdtempSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const MODE = process.argv[2] ?? 'all';
const APP = 'C:/dev/masaha/app-design';
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const WEB = 'http://localhost:5323';
const API = `${WEB}/api/v1`;
const SPACE = '/spaces/pal-hub';
const OWNER = 'demo-owner@example.com';
const RECEPTION = 'demo-reception@example.com';
const SHOTS = 'C:/Users/basel/Downloads/c2-shots';
const OUT = `C:/dev/masaha/workspace/TASKS/AUTH_IN_PLACE/WI-C2/chrome2-out-${MODE}.json`;
mkdirSync(SHOTS, { recursive: true });
const ENV = readFileSync(`${APP}/apps/api/.env`, 'utf8');
const secret = (name) =>
  new RegExp(`^${name}=(.*)$`, 'm')
    .exec(ENV)?.[1]
    ?.trim()
    .replace(/^["']|["']$/g, '');
const DEMO_PASSWORD = secret('SEED_DEMO_PASSWORD');
const ADMIN_EMAIL = secret('SEED_ADMIN_EMAIL');
const ADMIN_PASSWORD = secret('SEED_ADMIN_PASSWORD');
if (!DEMO_PASSWORD || !ADMIN_EMAIL || !ADMIN_PASSWORD) throw new Error('a seed secret is missing');
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
const socket = new WebSocket(targets.find((t) => t.type === 'page').webSocketDebuggerUrl);
await new Promise((resolve) => socket.addEventListener('open', resolve));
let id = 0;
const pending = new Map();
const pageErrors = [];
socket.addEventListener('message', (event) => {
  const message = JSON.parse(event.data);
  if (message.id !== undefined && pending.has(message.id)) {
    const { resolve, reject } = pending.get(message.id);
    pending.delete(message.id);
    if (message.error) reject(new Error(JSON.stringify(message.error)));
    else resolve(message.result);
  } else if (message.method === 'Runtime.exceptionThrown') {
    pageErrors.push(message.params.exceptionDetails.exception?.description ?? 'exception');
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
  if (result.exceptionDetails) throw new Error(result.exceptionDetails.exception?.description ?? 'evaluate failed');
  return result.result.value;
};
await send('Page.enable');
await send('Runtime.enable');
await send('Network.enable');

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
async function go(path, lang = 'en') {
  await send('Page.navigate', { url: 'about:blank' });
  await sleep(200);
  await send('Page.navigate', { url: `${WEB}${path}` });
  await waitFor('document.readyState === "complete"');
  await evaluate(`localStorage.setItem('masaha.language', '${lang}'); localStorage.setItem('masaha.theme', 'light'); true`);
  await send('Page.reload');
  await sleep(300);
  await waitFor('document.readyState === "complete"');
  await waitFor('document.querySelector("h1")', 15000);
  await sleep(800);
}
async function signedOut() {
  await send('Network.clearBrowserCookies');
  await evaluate('(() => { try { localStorage.clear(); } catch { /* about:blank */ } return true; })()');
}
async function shot(name) {
  const { data } = await send('Page.captureScreenshot', { format: 'png' });
  writeFileSync(`${SHOTS}/${name}.png`, Buffer.from(data, 'base64'));
}
const dialog = 'document.querySelector("[data-slot=adaptive-dialog-content]")';
const inDialog = (selector) => `${dialog}?.querySelector(${JSON.stringify(selector)})`;
const buttonByText = (text, root = dialog) =>
  `[...(${root}?.querySelectorAll('button') ?? [])].find(b => b.textContent.trim() === ${JSON.stringify(text)})`;
async function typeInto(selector, text) {
  await evaluate(`${selector}.focus(); true`);
  await send('Input.insertText', { text });
  await sleep(50);
}
const historyState = `(() => ({ length: history.length, path: location.pathname + location.search, marked: Boolean(history.state && history.state.masahaOverlay) }))()`;

async function signInThere(email, password) {
  await typeInto(inDialog('input[type=email]'), email);
  await typeInto(inDialog('input[autocomplete=current-password]'), password);
  await evaluate(`${buttonByText('Sign in')}.click(); true`);
}

/** The API, as Node: signed in as `email`, its access token. */
async function apiSignIn(email, password) {
  const answer = await fetch(`${API}/auth/login`, {
    method: 'POST',
    headers: { 'content-type': 'application/json', origin: WEB },
    body: JSON.stringify({ email, password }),
  });
  const body = await answer.json();
  if (!answer.ok) throw new Error(`sign-in ${answer.status} ${body.error?.code ?? ''}`);
  return body.data.accessToken;
}

async function temporary() {
  // A temporary password for the demo reception account, issued by the admin (its recovery).
  const admin = await apiSignIn(ADMIN_EMAIL, ADMIN_PASSWORD);
  const found = await (
    await fetch(`${API}/admin/users?email=${encodeURIComponent(RECEPTION)}`, {
      headers: { authorization: `Bearer ${admin}` },
    })
  ).json();
  const userId = found.data?.[0]?.id;
  const issued = await fetch(`${API}/admin/users/${userId}/temporary-password`, {
    method: 'POST',
    headers: { authorization: `Bearer ${admin}`, origin: WEB },
  });
  const temporaryPassword = (await issued.json()).data?.temporaryPassword;
  results['temporary password issued'] = issued.status;
  if (!temporaryPassword) return;

  await viewport(390);
  await signedOut();
  // The page before, so Back has somewhere to go: Home, then the space.
  await go('/', 'en');
  await evaluate(`(() => { const a = [...document.querySelectorAll('a')].find(l => l.getAttribute('href') === '${SPACE}'); if (a) { a.click(); return true; } location.assign('${SPACE}'); return false; })()`);
  await waitFor(`location.pathname === '${SPACE}'`, 10000);
  await waitFor('document.querySelector("button[aria-pressed]")', 15000);
  await sleep(800);
  results['history on the space page'] = await evaluate(historyState);
  await evaluate('document.querySelector("button[aria-pressed]").click(); true');
  await waitFor(inDialog('input[type=email]'), 10000);
  results['history with the overlay open'] = await evaluate(historyState);
  await evaluate(`(() => {
    const log = (window.__log = []);
    const t0 = performance.now();
    const describe = (state) => JSON.stringify({ key: state?.key, idx: state?.idx, mark: state?.masahaOverlay ? 'M' : '' });
    for (const name of ['pushState', 'replaceState', 'back', 'go']) {
      const original = history[name].bind(history);
      history[name] = (...args) => {
        log.push(Math.round(performance.now() - t0) + ' ' + name + ' ' + (name.endsWith('State') ? describe(args[0]) + ' ' + (args[2] ?? '') : String(args[0] ?? '')) + ' at ' + location.pathname);
        return original(...args);
      };
    }
    addEventListener('popstate', () => log.push(Math.round(performance.now() - t0) + ' popstate ' + describe(history.state) + ' ' + location.pathname));
    return true;
  })()`);
  await signInThere(RECEPTION, temporaryPassword);
  const started = Date.now();
  const timeline = [];
  for (const at of [100, 300, 600, 1000, 2000, 4000]) {
    await sleep(Math.max(0, at - (Date.now() - started)));
    timeline.push({
      at,
      ...(await evaluate(
        `({ ...${historyState}, title: document.title, main: document.querySelector('main')?.innerText?.slice(0, 60), overlay: Boolean(${dialog}) })`,
      )),
    });
  }
  results['timeline after the sign-in'] = timeline;
  results['history calls'] = await evaluate('window.__log');
  results['history on the change page'] = await evaluate(historyState);
  await shot('temporary-change-390-en');
  // Back from the change page: where does it go, and is there a dead step?
  await evaluate('history.back(); true');
  await sleep(1500);
  results['after one Back'] = await evaluate(historyState);
  await evaluate('history.forward(); true');
  await sleep(1500);
  results['after Forward'] = await evaluate(historyState);
  if (!(await evaluate(`location.pathname === '/change-password'`))) {
    await send('Page.navigate', { url: `${WEB}/change-password?next=${encodeURIComponent(SPACE)}` });
    await waitFor(`location.pathname === '/change-password'`, 10000);
  }
  // Back to the demo password, so the demo data is as it was; the action then runs on its page.
  await waitFor('document.querySelector("[autocomplete=new-password]")', 10000);
  await typeInto('document.querySelector("[autocomplete=new-password]")', DEMO_PASSWORD);
  await evaluate(`[...document.querySelectorAll('button[type=submit]')].at(-1).click(); true`);
  await waitFor(`location.pathname === '${SPACE}'`, 15000);
  await waitFor(`document.querySelector("button[aria-pressed]")?.getAttribute('aria-pressed') === 'true'`, 10000);
  results['after the change: page, heart'] = await evaluate(
    `location.pathname + ' ' + document.querySelector("button[aria-pressed]")?.getAttribute('aria-pressed')`,
  );
  await shot('temporary-done-390-en');
  // Clean up: the reception account's favourite removed again.
  await evaluate('document.querySelector("button[aria-pressed]").click(); true');
  await sleep(1500);
  results['demo password restored'] = await apiSignIn(RECEPTION, DEMO_PASSWORD).then(() => true, (e) => String(e));
}

async function cards() {
  for (const [path, label] of [
    ['/', 'home'],
    ['/spaces', 'directory'],
  ]) {
    for (const width of [390, 1440]) {
      await viewport(width);
      await signedOut();
      await go(path, 'en');
      const ok = await waitFor('document.querySelector("main button[aria-pressed][aria-label^=Save]")', 15000);
      if (!ok) {
        results[`${label} ${width} heart`] = 'no heart found';
        continue;
      }
      const name = await evaluate(
        `(() => { const h = document.querySelector("main button[aria-pressed][aria-label^=Save]"); h.scrollIntoView({ block: 'center' }); h.focus(); h.click(); return h.getAttribute('aria-label'); })()`,
      );
      await waitFor(inDialog('input[type=email]'), 10000);
      await sleep(400);
      await shot(`card-${label}-${width}-en`);
      await signInThere(OWNER, DEMO_PASSWORD);
      await waitFor(`!${dialog}`, 10000);
      // The page may now read in the account's language (finding 231): the heart is found by its space.
      const heartOf = `[...document.querySelectorAll('main button[aria-pressed]')].find(b => /Pal Hub|بال هاب/.test(b.getAttribute('aria-label') ?? ''))`;
      await waitFor(`${heartOf}?.getAttribute('aria-pressed') === 'true'`, 10000);
      await sleep(1200);
      results[`${label} ${width}`] = await evaluate(
        `(() => { const a = document.activeElement; const h = ${heartOf}; return { path: location.pathname, pressed: h?.getAttribute('aria-pressed'), focusOnThatHeart: a === h, focus: a?.getAttribute('aria-label') ?? a?.tagName }; })()`,
      );
      // Clean up: the favourite removed again.
      await evaluate(`${heartOf}?.click(); true`);
      await sleep(1500);
    }
  }
}

async function network() {
  await viewport(390);
  // Slow 3G: the overlay opens at once, its title and a short loading line while the forms load.
  await signedOut();
  await go(SPACE, 'en');
  await send('Network.emulateNetworkConditions', {
    offline: false,
    latency: 2000,
    downloadThroughput: (500 * 1024) / 8,
    uploadThroughput: (500 * 1024) / 8,
  });
  await evaluate('document.querySelector("button[aria-pressed]").focus(); document.querySelector("button[aria-pressed]").click(); true');
  await waitFor(dialog, 5000);
  await sleep(300);
  results['slow 3G, at once'] = await evaluate(
    `({ title: ${dialog}?.querySelector('[data-slot=adaptive-dialog-title]')?.textContent, loading: Boolean(${dialog}?.querySelector('[data-slot=spinner]')), form: Boolean(${inDialog('input[type=email]')}), focus: document.activeElement?.getAttribute('data-slot') })`,
  );
  await shot('slow3g-loading-390-en');
  const loaded = Date.now();
  await waitFor(inDialog('input[type=email]'), 60000);
  results['slow 3G, the forms after (ms)'] = Date.now() - loaded;
  await shot('slow3g-loaded-390-en');
  await send('Network.emulateNetworkConditions', { offline: false, latency: 0, downloadThroughput: -1, uploadThroughput: -1 });

  // Offline: the forms cannot load; the line and «Try again»; back online, the retry loads them.
  await signedOut();
  await go(SPACE, 'en');
  await send('Network.emulateNetworkConditions', { offline: true, latency: 0, downloadThroughput: -1, uploadThroughput: -1 });
  await evaluate('document.querySelector("button[aria-pressed]").focus(); document.querySelector("button[aria-pressed]").click(); true');
  await waitFor(inDialog('[role=alert]'), 20000);
  results['offline'] = await evaluate(
    `({ alert: ${inDialog('[role=alert]')}?.textContent, retry: Boolean(${buttonByText('Try again')}) })`,
  );
  await shot('offline-failed-390-en');
  await send('Network.emulateNetworkConditions', { offline: false, latency: 0, downloadThroughput: -1, uploadThroughput: -1 });
  // The connection back, as the browser sees it, before the guest presses «Try again».
  await waitFor('navigator.onLine', 5000);
  await sleep(1500);
  const requested = [];
  const failed = [];
  const watch = (event) => {
    const message = JSON.parse(event.data);
    if (message.method === 'Network.requestWillBeSent') requested.push(message.params.request.url.replace(WEB, '').slice(0, 80));
    if (message.method === 'Network.loadingFailed') failed.push(message.params.errorText);
  };
  socket.addEventListener('message', watch);
  await evaluate(`${buttonByText('Try again')}.focus(); ${buttonByText('Try again')}.click(); true`);
  await waitFor(inDialog('input[type=email]'), 20000);
  socket.removeEventListener('message', watch);
  results['requests after the retry'] = { count: requested.length, first: requested.slice(0, 6), failed: failed.slice(0, 4) };
  results['alert after the retry'] = await evaluate(`${inDialog('[role=alert]')}?.textContent ?? null`);
  await sleep(300);
  results['back online, after the retry'] = await evaluate(
    `({ form: Boolean(${inDialog('input[type=email]')}), focus: document.activeElement?.getAttribute('data-slot') })`,
  );
  await shot('offline-retried-390-en');
}

try {
  if (MODE === 'temporary' || MODE === 'all') await temporary();
  if (MODE === 'cards' || MODE === 'all') await cards();
  if (MODE === 'network' || MODE === 'all') await network();
} catch (error) {
  results.error = String(error.stack ?? error);
} finally {
  results.pageErrors = pageErrors;
  writeFileSync(OUT, JSON.stringify(results, null, 2));
  socket.close();
  chrome.kill();
  console.log('written', OUT);
}
