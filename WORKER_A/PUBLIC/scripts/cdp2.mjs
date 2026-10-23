// Local headless Chrome over CDP, with Node's own WebSocket: real screenshots of the real app.
import { spawn } from 'node:child_process';
import { mkdirSync, mkdtempSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
export const WEB = 'http://localhost:5320';
export const SHOTS = 'C:/dev/masaha/workspace/WORKER_A/PUBLIC/shots/pr2';
mkdirSync(SHOTS, { recursive: true });

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

export async function launch() {
  const port = 9300 + Math.floor(Math.random() * 600);
  const profile = mkdtempSync(join(tmpdir(), 'cdp-'));
  const chrome = spawn(CHROME, [
    '--headless=new',
    `--remote-debugging-port=${port}`,
    `--user-data-dir=${profile}`,
    '--no-first-run',
    '--no-default-browser-check',
    '--window-size=1440,1000',
    'about:blank',
  ]);
  let targets;
  for (let i = 0; i < 50; i += 1) {
    try {
      targets = await (await fetch(`http://127.0.0.1:${port}/json`)).json();
      if (targets.some((t) => t.type === 'page')) break;
    } catch {
      /* not up yet */
    }
    await sleep(200);
  }
  const page = targets.find((t) => t.type === 'page');
  const socket = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise((resolve) => socket.addEventListener('open', resolve));
  let id = 0;
  const pending = new Map();
  const listeners = [];
  socket.addEventListener('message', (event) => {
    const message = JSON.parse(event.data);
    if (message.id !== undefined && pending.has(message.id)) {
      const { resolve, reject } = pending.get(message.id);
      pending.delete(message.id);
      if (message.error) reject(new Error(JSON.stringify(message.error)));
      else resolve(message.result);
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
  await send('Page.enable');
  await send('Runtime.enable');
  const errors = [];
  listeners.push((m) => {
    if (m.method === 'Runtime.exceptionThrown') errors.push(m.params.exceptionDetails.text);
  });
  return { chrome, send, errors, pid: chrome.pid, on: (listener) => listeners.push(listener) };
}

export function driver(b) {
  const evaluate = async (expression) => {
    const result = await b.send('Runtime.evaluate', {
      expression,
      awaitPromise: true,
      returnByValue: true,
    });
    if (result.exceptionDetails) throw new Error(`eval: ${result.exceptionDetails.exception?.description ?? result.exceptionDetails.text}`);
    return result.result.value;
  };
  const d = {
    evaluate,
    sleep,
    async viewport(width, height = 900) {
      await b.send('Emulation.setDeviceMetricsOverride', {
        width,
        height,
        deviceScaleFactor: 1,
        mobile: width < 768,
      });
    },
    async theme(dark) {
      await b.send('Emulation.setEmulatedMedia', {
        features: [{ name: 'prefers-color-scheme', value: dark ? 'dark' : 'light' }],
      });
    },
    async go(url) {
      await b.send('Page.navigate', { url: 'about:blank' });
      await sleep(150);
      await b.send('Page.navigate', { url: url.startsWith('http') ? url : WEB + url });
      await sleep(1500);
    },
    /** Waits until `expression` is truthy, or fails with `what`. */
    async until(expression, what, ms = 15000) {
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
    },
    async prefs(language, theme) {
      await evaluate(
        `localStorage.setItem('masaha.language', ${JSON.stringify(language)}); localStorage.setItem('masaha.theme', ${JSON.stringify(theme)}); true`,
      );
    },
    async type(selector, text) {
      await evaluate(`(() => { const el = document.querySelector(${JSON.stringify(selector)}); el.focus(); el.select?.(); return true; })()`);
      await b.send('Input.insertText', { text });
      await sleep(100);
    },
    /** Clicks the element `expression` returns (a JS expression giving an element). */
    async click(expression, what) {
      const ok = await evaluate(`(() => { const el = ${expression}; if (!el) return false; el.scrollIntoView({ block: 'center' }); el.click(); return true; })()`);
      if (!ok) throw new Error(`no element to click: ${what}`);
      await sleep(400);
    },
    /** Opens a Radix menu: focus its trigger and press Enter. */
    async openMenu(expression, what) {
      const ok = await evaluate(`(() => { const el = ${expression}; if (!el) return false; el.scrollIntoView({ block: 'center' }); el.focus(); return true; })()`);
      if (!ok) throw new Error(`no menu trigger: ${what}`);
      await b.send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13 });
      await b.send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13 });
      await sleep(500);
    },
    async key(key, code = key, keyCode = 0) {
      await b.send('Input.dispatchKeyEvent', { type: 'keyDown', key, code, windowsVirtualKeyCode: keyCode });
      await b.send('Input.dispatchKeyEvent', { type: 'keyUp', key, code, windowsVirtualKeyCode: keyCode });
      await sleep(300);
    },
    async shot(name, height) {
      if (height) {
        const metrics = await evaluate('({ w: innerWidth })');
        await d.viewport(metrics.w, height);
        await sleep(300);
      }
      const { data } = await b.send('Page.captureScreenshot', { format: 'png' });
      writeFileSync(`${SHOTS}/${name}.png`, Buffer.from(data, 'base64'));
      console.log('shot', name);
    },
    text: (expression) => evaluate(`(() => { const el = ${expression}; return el ? el.innerText : null; })()`),
  };
  return d;
}

/** A button, link, menu item or option whose text (isolates removed) matches `pattern`. */
export const byText = (selector, pattern) =>
  `[...document.querySelectorAll(${JSON.stringify(selector)})].find((el) => new RegExp(${JSON.stringify(pattern)}).test(el.textContent.replace(/[\\u2066-\\u2069]/g, '')))`;

/** An element by its accessible label (aria-label), isolates removed. */
export const byLabel = (selector, pattern) =>
  `[...document.querySelectorAll(${JSON.stringify(selector)})].find((el) => new RegExp(${JSON.stringify(pattern)}).test((el.getAttribute('aria-label') ?? '').replace(/[\\u2066-\\u2069]/g, '')))`;

export async function signInAsAdmin(d, admin, next) {
  await d.go(`/login?next=${encodeURIComponent(next)}`);
  await d.until(`!!document.querySelector('input[type=email]')`, 'login form');
  await d.type('input[type=email]', admin.email);
  await d.type('input[type=password]', admin.password);
  await d.click(`document.querySelector('form button[type=submit]')`, 'sign in');
  await d.until(`location.pathname === ${JSON.stringify(next.split('?')[0])}`, 'landing on ' + next, 20000);
  await sleep(1500);
}
