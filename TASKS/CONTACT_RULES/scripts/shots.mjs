// CONTACT_RULES C5's captures (finding 226): the showcase's DataTable at 1440 px, its first row
// hovered, its ghost «⋯» hovered, and its menu open with the pointer on the menu, in Arabic, light
// and dark; and the «⋯» hovered in English, light and dark. Local headless Chrome over CDP with
// Node's own WebSocket; only the web's dev server on 5337 is needed.
import { spawn } from 'node:child_process';
import { mkdirSync, mkdtempSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const WEB = 'http://localhost:5337';
const SHOTS = 'C:/Users/basel/Downloads/contact-rules-shots';
const ROW = 'tbody tr[data-slot="table-row"]';
const CELL = `${ROW} td`;
const TRIGGER = `${ROW} button[aria-haspopup="menu"]`;
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
const q = (selector) => `document.querySelector(${JSON.stringify(selector)})`;
const centreOf = (selector, scroll) =>
  evaluate(`(() => {
    const element = ${q(selector)};
    if (${scroll ? 'true' : 'false'}) element.scrollIntoView({ block: 'center' });
    const box = element.getBoundingClientRect();
    return { x: Math.round(box.x + box.width / 2), y: Math.round(box.y + box.height / 2) };
  })()`);
const pointer = ({ x, y }) => send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y });
const fills = () =>
  evaluate(`(() => ({
    row: getComputedStyle(${q(ROW)}).backgroundColor,
    trigger: getComputedStyle(${q(TRIGGER)}).backgroundColor,
    expanded: ${q(TRIGGER)}.getAttribute('aria-expanded'),
    theme: document.documentElement.dataset.theme,
    dir: document.documentElement.dir,
  }))()`);

await send('Page.enable');
await send('Runtime.enable');
await send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });

const report = [];
async function open(lang, theme) {
  await send('Page.navigate', { url: 'about:blank' });
  await sleep(200);
  await send('Page.navigate', { url: `${WEB}/__showcase/preview/data/data-table?theme=${theme}&lang=${lang}` });
  await until(`!!${q(TRIGGER)}`, `the table (${lang}, ${theme})`);
  await sleep(800);
  await pointer({ x: 1, y: 1 });
  await sleep(200);
}
async function shot(name) {
  await sleep(400);
  const { data } = await send('Page.captureScreenshot', { format: 'png' });
  writeFileSync(`${SHOTS}/${name}.png`, Buffer.from(data, 'base64'));
  report.push({ name, ...(await fills()) });
}
const press = async (type) =>
  send('Input.dispatchKeyEvent', { type, key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13 });

try {
  for (const theme of ['light', 'dark']) {
    await open('ar', theme);
    await pointer(await centreOf(CELL, true));
    await shot(`row-hover-ar-${theme}-1440`);
    await pointer(await centreOf(TRIGGER, false));
    await shot(`ghost-hover-ar-${theme}-1440`);
    // Radix opens the menu from the keyboard; then the pointer leaves the row for the menu.
    await evaluate(`${q(TRIGGER)}.focus(); true`);
    await press('keyDown');
    await press('keyUp');
    await until(`${q(TRIGGER)}.getAttribute('aria-expanded') === 'true'`, 'the menu open');
    await pointer(await centreOf('[role="menuitem"]', false));
    await shot(`menu-open-ar-${theme}-1440`);
  }
  for (const theme of ['light', 'dark']) {
    await open('en', theme);
    await pointer(await centreOf(TRIGGER, true));
    await shot(`ghost-hover-en-${theme}-1440`);
  }
} finally {
  console.log(JSON.stringify(report, null, 1));
  console.log('errors', JSON.stringify(errors));
  socket.close();
  chrome.kill();
}
