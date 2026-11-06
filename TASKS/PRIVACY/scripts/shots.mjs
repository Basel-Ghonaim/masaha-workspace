// The privacy page's screenshots: local headless Chrome over CDP, Node's own WebSocket.
// Each page is shot whole by sizing the viewport to its height (RTL shifts with captureBeyondViewport).
import { spawn } from 'node:child_process';
import { mkdirSync, mkdtempSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const WEB = 'http://localhost:5320';
const SHOTS = 'C:/dev/masaha/workspace/TASKS/PRIVACY/shots/web';
mkdirSync(SHOTS, { recursive: true });
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
  } else if (message.method === 'Fetch.requestPaused') {
    // The API is not started (its timer would write masaha_dev): the public contact is answered
    // here with a sample; any other API call is answered 503, as an API that is down.
    const { requestId, request } = message.params;
    const contact = request.url.includes('/api/v1/settings/public');
    const body = contact
      ? { success: true, data: { email: 'hello@masaha.example', whatsapp: '+970599000099' } }
      : { success: false, error: { type: 'internal', message: 'API not started' } };
    send('Fetch.fulfillRequest', {
      requestId,
      responseCode: contact ? 200 : 503,
      responseHeaders: [{ name: 'Content-Type', value: 'application/json' }],
      body: Buffer.from(JSON.stringify(body)).toString('base64'),
    });
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
  if (result.exceptionDetails) throw new Error(result.exceptionDetails.text);
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
const viewport = (width, height) =>
  send('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile: width < 768 });

await send('Page.enable');
await send('Runtime.enable');
await send('Fetch.enable', { patterns: [{ urlPattern: '*/api/v1/*' }] });

const report = [];
async function shoot(name, path, language, theme, width, ready) {
  await viewport(width, 900);
  await send('Page.navigate', { url: `${WEB}/` });
  await until(`document.readyState === 'complete'`, 'home');
  await evaluate(
    `localStorage.setItem('masaha.language', '${language}'); localStorage.setItem('masaha.theme', '${theme}'); true`,
  );
  await send('Page.navigate', { url: 'about:blank' });
  await sleep(150);
  await send('Page.navigate', { url: `${WEB}${path}` });
  await until(ready, `${name} ready`);
  await sleep(1200);
  const facts = await evaluate(`(() => ({
    dir: document.documentElement.dir,
    lang: document.documentElement.lang,
    theme: document.documentElement.dataset.theme,
    title: document.title,
    overflow: document.documentElement.scrollWidth > innerWidth,
    height: document.documentElement.scrollHeight,
    email: [...document.querySelectorAll('main a[href^="mailto:"]')].map((a) => a.textContent),
    rawTag: /<\\/?[a-z]+[ >]/i.test(document.querySelector('main')?.innerText ?? ''),
    strong: document.querySelectorAll('main strong').length,
  }))()`);
  await viewport(width, Math.min(facts.height, 16000));
  await sleep(400);
  const { data } = await send('Page.captureScreenshot', { format: 'png' });
  writeFileSync(`${SHOTS}/${name}.png`, Buffer.from(data, 'base64'));
  report.push({ name, ...facts });
}

const privacyReady = `!!document.querySelector('main h1') && document.querySelectorAll('main h2').length === 11`;
try {
  await shoot('privacy-ar-light-1280', '/privacy', 'ar', 'light', 1280, privacyReady);
  await shoot('privacy-ar-light-390', '/privacy', 'ar', 'light', 390, privacyReady);
  await shoot('privacy-en-light-1280', '/privacy', 'en', 'light', 1280, privacyReady);
  await shoot('privacy-ar-dark-1280', '/privacy', 'ar', 'dark', 1280, privacyReady);
  await shoot('home-footer-ar-1280', '/', 'ar', 'light', 1280, `!!document.querySelector('footer a[href="/privacy"]')`);
  await shoot('register-ar-390', '/register', 'ar', 'light', 390, `!!document.querySelector('main a[href="/privacy"]')`);
  await shoot('register-en-1280', '/register', 'en', 'light', 1280, `!!document.querySelector('main a[href="/privacy"]')`);
} finally {
  console.log(JSON.stringify(report, null, 1));
  console.log('errors', JSON.stringify(errors));
  socket.close();
  chrome.kill();
}
