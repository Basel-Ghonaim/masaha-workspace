// The visual pass (IDENTITY, T23): headless Chrome over CDP with Node 24's built-in WebSocket.
// One Chrome per run, its own profile (cdp-profile-<run>), stopped by its PID at the end.
// Every API request is paused by Fetch: GETs go on; a write is refused (only sign-in and the
// session's refresh pass), so no data is ever written. Credentials are read from apps/api/.env
// inside the run and never printed.
import { execSync, spawn } from 'node:child_process';
import { appendFileSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { createServer } from 'node:net';
import { join } from 'node:path';
import { inflateSync } from 'node:zlib';

export const SCRATCH = 'C:/dev/masaha/workspace/TASKS/IDENTITY/lanes/scratch-v';
export const RAW = `${SCRATCH}/raw`;
export const SHOTS = 'C:/Users/basel/Downloads/identity-prod-shots';
export const BASE = 'http://localhost:5323';
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const AXE = readFileSync('C:/dev/masaha/app-design/node_modules/axe-core/axe.min.js', 'utf8');
const INPAGE = readFileSync(join(SCRATCH, 'inpage.js'), 'utf8');
mkdirSync(RAW, { recursive: true });
mkdirSync(SHOTS, { recursive: true });

export const sleep = (ms) => new Promise((done) => setTimeout(done, ms));
const stamp = () => new Date().toISOString().slice(11, 19);

/** The accounts' secrets, read here and kept in memory only. */
export function accounts() {
  const env = Object.fromEntries(
    readFileSync('C:/dev/masaha/app-design/apps/api/.env', 'utf8')
      .split(/\r?\n/)
      .map((line) => line.match(/^([A-Z_]+)=(.*)$/))
      .filter(Boolean)
      .map(([, key, value]) => [key, value.replace(/^["']|["']$/g, '')]),
  );
  return {
    owner: { email: 'demo-owner@example.com', password: env.SEED_DEMO_PASSWORD },
    reception: { email: 'demo-reception@example.com', password: env.SEED_DEMO_PASSWORD },
    admin: { email: env.SEED_ADMIN_EMAIL, password: env.SEED_ADMIN_PASSWORD },
  };
}

async function freePort() {
  return new Promise((resolve, reject) => {
    const server = createServer();
    server.on('error', reject);
    server.listen(0, '127.0.0.1', () => {
      const { port } = server.address();
      server.close(() => resolve(port));
    });
  });
}

/** Chrome processes whose command line names this run's profile. */
export function profileProcesses(run) {
  try {
    const out = execSync(
      `powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \\"Name='chrome.exe'\\" | Where-Object { $_.CommandLine -like '*cdp-profile-${run}*' } | Select-Object -ExpandProperty ProcessId"`,
      { encoding: 'utf8' },
    );
    return out.split(/\s+/).filter(Boolean).map(Number);
  } catch {
    return [];
  }
}

export async function launch(run, { log: logFile } = {}) {
  const port = await freePort();
  const profile = `${SCRATCH}/cdp-profile-${run}`;
  rmSync(profile, { recursive: true, force: true });
  const chrome = spawn(
    CHROME,
    [
      '--headless=new',
      `--remote-debugging-port=${port}`,
      `--user-data-dir=${profile}`,
      '--no-first-run',
      '--no-default-browser-check',
      '--hide-scrollbars',
      '--mute-audio',
      '--force-color-profile=srgb',
      '--disable-features=Translate',
      'about:blank',
    ],
    { stdio: 'ignore' },
  );
  const logPath = logFile ?? `${SCRATCH}/run-${run}.log`;
  writeFileSync(logPath, '');
  const log = (...parts) => {
    const text = `${stamp()} ${parts.map((p) => (typeof p === 'string' ? p : JSON.stringify(p))).join(' ')}`;
    console.log(text);
    appendFileSync(logPath, `${text}\n`);
  };
  log(`chrome pid ${chrome.pid}, port ${port}, profile cdp-profile-${run}`);

  let target;
  for (let tries = 0; tries < 150 && !target; tries += 1) {
    try {
      const list = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
      target = list.find((entry) => entry.type === 'page')?.webSocketDebuggerUrl;
    } catch {
      // not up yet
    }
    if (!target) await sleep(200);
  }
  if (!target) throw new Error('no page target');
  const ws = new WebSocket(target);
  await new Promise((resolve, reject) => {
    ws.onopen = resolve;
    ws.onerror = reject;
  });
  let nextId = 0;
  const pending = new Map();
  const listeners = new Map();
  ws.onmessage = ({ data }) => {
    const message = JSON.parse(data);
    if (message.id) {
      const waiting = pending.get(message.id);
      if (!waiting) return;
      pending.delete(message.id);
      if (message.error) waiting.reject(new Error(`${waiting.method}: ${message.error.message}`));
      else waiting.resolve(message.result);
      return;
    }
    for (const fn of listeners.get(message.method) ?? []) fn(message.params);
  };
  const send = (method, params = {}) =>
    new Promise((resolve, reject) => {
      const id = ++nextId;
      pending.set(id, { resolve, reject, method });
      ws.send(JSON.stringify({ id, method, params }));
    });
  const on = (method, fn) => {
    if (!listeners.has(method)) listeners.set(method, []);
    listeners.get(method).push(fn);
    return () => listeners.set(method, (listeners.get(method) ?? []).filter((f) => f !== fn));
  };

  const page = new Page({ send, on, log, run, chrome });
  await page.init();
  return page;
}

export class Page {
  constructor({ send, on, log, run, chrome }) {
    Object.assign(this, { send, on, log, run, chrome });
    this.inflight = new Map();
    this.consoleBuffer = [];
    this.blocked = [];
    this.refreshes = 0;
    this.loads = 0;
    this.holds = []; // { match: (url) => bool, until: Promise }
    this.fulfils = []; // { match, body: (original) => newBody }
    this.apiLog = [];
    this.width = 1440;
    this.height = 900;
  }

  async init() {
    const { send, on } = this;
    await send('Page.enable');
    await send('Runtime.enable');
    await send('Log.enable');
    await send('Network.enable');
    await send('Page.bringToFront');
    await send('Page.addScriptToEvaluateOnNewDocument', { source: INPAGE });
    on('Runtime.consoleAPICalled', ({ type, args }) => {
      if (type === 'error' || type === 'assert') {
        const text = args.map((a) => a.value ?? a.description ?? a.type).join(' ');
        this.consoleBuffer.push({ kind: `console.${type}`, text: text.slice(0, 400) });
      }
    });
    on('Runtime.exceptionThrown', ({ exceptionDetails }) => {
      this.consoleBuffer.push({
        kind: 'exception',
        text: (exceptionDetails.exception?.description ?? exceptionDetails.text).slice(0, 400),
      });
    });
    on('Log.entryAdded', ({ entry }) => {
      if (entry.level === 'error') {
        this.consoleBuffer.push({ kind: `log.${entry.source}`, text: `${entry.text} ${entry.url ?? ''}`.slice(0, 400) });
      }
    });
    on('Network.requestWillBeSent', ({ requestId, request, type }) => {
      this.inflight.set(requestId, { url: request.url, type, at: Date.now() });
      if (this.onRequest) this.onRequest(request, type);
    });
    const done = ({ requestId }) => this.inflight.delete(requestId);
    on('Network.loadingFinished', done);
    on('Network.loadingFailed', (params) => {
      const entry = this.inflight.get(params.requestId);
      done(params);
      if (entry && !params.canceled && !/BLOCKED_BY_CLIENT/.test(params.errorText) && !entry.url.startsWith('data:')) {
        this.consoleBuffer.push({ kind: 'network.failed', text: `${params.errorText} ${entry.url}` });
      }
    });
    on('Network.responseReceived', ({ response, type }) => {
      if (response.status >= 400 && !response.url.endsWith('/auth/refresh')) {
        this.consoleBuffer.push({ kind: 'network.status', text: `${response.status} ${response.url}` });
      }
    });
    // Every API request pauses here: a GET goes on (or is held or fulfilled), a write is refused.
    await this.setFetchPatterns();
    on('Fetch.requestPaused', (params) => void this.paused(params));
  }

  async setFetchPatterns() {
    const patterns = [{ urlPattern: '*/api/*', requestStage: 'Request' }];
    for (const f of this.fulfils) patterns.push({ urlPattern: f.pattern, requestStage: 'Response' });
    await this.send('Fetch.enable', { patterns });
  }

  /** Rewrites the body of a response whose URL matches `pattern` (a CDP glob) and `match`. */
  async fulfil(pattern, match, body) {
    this.fulfils.push({ pattern, match, body });
    await this.setFetchPatterns();
  }

  async clearFulfils() {
    this.fulfils = [];
    await this.setFetchPatterns();
  }

  async paused({ requestId, request, responseStatusCode, responseHeaders }) {
    const { url, method } = request;
    const path = url.replace(/^https?:\/\/[^/]+/, '');
    try {
      if (responseStatusCode !== undefined) {
        const fulfil = this.fulfils.find((f) => f.match(path));
        if (fulfil && responseStatusCode === 200) {
          const { body, base64Encoded } = await this.send('Fetch.getResponseBody', { requestId });
          const original = base64Encoded ? Buffer.from(body, 'base64').toString('utf8') : body;
          const changed = fulfil.body(original);
          this.log(`fulfilled ${path} (${original.length} -> ${changed.length} bytes)`);
          await this.send('Fetch.fulfillRequest', {
            requestId,
            responseCode: 200,
            responseHeaders: (responseHeaders ?? []).filter((h) => !/^(content-length|content-encoding|etag)$/i.test(h.name)),
            body: Buffer.from(changed).toString('base64'),
          });
        } else {
          await this.send('Fetch.continueRequest', { requestId });
        }
        return;
      }
      const allowedWrite = method === 'POST' && /\/api\/v1\/auth\/(login|refresh)$/.test(path);
      if (method !== 'GET' && method !== 'HEAD' && method !== 'OPTIONS' && !allowedWrite) {
        this.blocked.push(`${method} ${path}`);
        this.log(`BLOCKED write ${method} ${path}`);
        await this.send('Fetch.failRequest', { requestId, errorReason: 'BlockedByClient' });
        return;
      }
      if (/\/auth\/refresh$/.test(path)) this.refreshes += 1;
      this.apiLog.push(`${method} ${path}`);
      for (const hold of this.holds) {
        if (hold.match(path)) {
          this.log(`holding ${path}`);
          await hold.until;
        }
      }
      await this.send('Fetch.continueRequest', { requestId });
    } catch (error) {
      this.log(`fetch handler error ${error.message} for ${path}`);
      try {
        await this.send('Fetch.continueRequest', { requestId });
      } catch {
        // gone
      }
    }
  }

  takeConsole() {
    const out = this.consoleBuffer;
    this.consoleBuffer = [];
    return out;
  }

  async evaluate(expression, { awaitPromise = true } = {}) {
    const { result, exceptionDetails } = await this.send('Runtime.evaluate', {
      expression,
      awaitPromise,
      returnByValue: true,
    });
    if (exceptionDetails) {
      throw new Error(`evaluate: ${exceptionDetails.exception?.description ?? exceptionDetails.text}`);
    }
    return result.value;
  }

  /** In-page helper call: __vp.<fn>(...args). */
  async vp(fn, ...args) {
    return this.evaluate(`window.__vp.${fn}(...${JSON.stringify(args)})`);
  }

  async viewport(width, height) {
    this.width = width;
    this.height = height;
    await this.send('Emulation.setDeviceMetricsOverride', {
      width,
      height,
      deviceScaleFactor: 1,
      mobile: false,
    });
    await sleep(150);
  }

  async waitIdle({ quiet = 600, timeout = 20000 } = {}) {
    const start = Date.now();
    let calmSince = Date.now();
    while (Date.now() - start < timeout) {
      const now = Date.now();
      // Long-lived requests (a held one, a stream) older than 15 s do not count.
      const busy = [...this.inflight.values()].filter((r) => now - r.at < 15000 && r.url.startsWith('http://localhost'));
      if (busy.length > 0) calmSince = now;
      if (now - calmSince >= quiet) {
        const settled = await this.evaluate('window.__vp ? window.__vp.settled() : true').catch(() => true);
        if (settled) return true;
      }
      await sleep(100);
    }
    return false;
  }

  async goto(url, { blank = true, wait = true } = {}) {
    if (blank) {
      await this.send('Page.navigate', { url: 'about:blank' });
      await sleep(200);
    }
    const loaded = new Promise((resolve) => {
      const off = this.on('Page.loadEventFired', () => {
        off();
        resolve();
      });
    });
    this.loads += 1;
    await this.send('Page.navigate', { url: /^[a-z]+:/.test(url) ? url : BASE + url });
    await Promise.race([loaded, sleep(20000)]);
    if (wait) await this.waitIdle();
  }

  /** A client-side navigation: the router hears popstate; no reload, no refresh. */
  async spa(path) {
    await this.evaluate(
      `history.pushState(null, '', ${JSON.stringify(path)}); dispatchEvent(new PopStateEvent('popstate', { state: null })); true`,
    );
    await sleep(300);
    await this.waitIdle();
  }

  async url() {
    return this.evaluate('location.pathname + location.search');
  }

  /** The theme and the language, through the store's storage listener: no reload. */
  async prefs(theme, lang) {
    await this.evaluate(`(() => {
      localStorage.setItem('masaha.theme', ${JSON.stringify(theme)});
      localStorage.setItem('masaha.language', ${JSON.stringify(lang)});
      dispatchEvent(new StorageEvent('storage', { key: 'masaha.theme' }));
      dispatchEvent(new StorageEvent('storage', { key: 'masaha.language' }));
      return true;
    })()`);
    for (let i = 0; i < 30; i += 1) {
      const ok = await this.evaluate(
        `document.documentElement.dataset.theme === ${JSON.stringify(theme)} && document.documentElement.lang === ${JSON.stringify(lang)}`,
      );
      if (ok) break;
      await sleep(100);
    }
    await sleep(250);
    await this.waitIdle({ quiet: 400 });
  }

  /** Sets the stored preferences before a load (for a page not yet open). */
  async storePrefs(theme, lang) {
    await this.evaluate(
      `localStorage.setItem('masaha.theme', ${JSON.stringify(theme)}); localStorage.setItem('masaha.language', ${JSON.stringify(lang)}); true`,
    );
  }

  async key(key, { code, vk, text, modifiers = 0 } = {}) {
    const KEYS = {
      Tab: [9, 'Tab'],
      Enter: [13, 'Enter', '\r'],
      Escape: [27, 'Escape'],
      ' ': [32, 'Space', ' '],
      ArrowDown: [40, 'ArrowDown'],
      ArrowUp: [38, 'ArrowUp'],
      ArrowLeft: [37, 'ArrowLeft'],
      ArrowRight: [39, 'ArrowRight'],
    };
    const [windowsVirtualKeyCode, keyCode, keyText] = KEYS[key] ?? [vk, code, text];
    const base = { key, code: code ?? keyCode, windowsVirtualKeyCode, nativeVirtualKeyCode: windowsVirtualKeyCode, modifiers };
    await this.send('Input.dispatchKeyEvent', { type: keyText ? 'keyDown' : 'rawKeyDown', ...base, text: keyText, unmodifiedText: keyText });
    await this.send('Input.dispatchKeyEvent', { type: 'keyUp', ...base });
    await sleep(120);
  }

  async mouse(x, y, type = 'mouseMoved', extra = {}) {
    await this.send('Input.dispatchMouseEvent', { type, x, y, button: extra.button ?? 'none', buttons: extra.buttons ?? 0, clickCount: extra.clickCount ?? 0, pointerType: 'mouse' });
  }

  async click(x, y) {
    await this.mouse(x, y, 'mouseMoved');
    await this.mouse(x, y, 'mousePressed', { button: 'left', buttons: 1, clickCount: 1 });
    await this.mouse(x, y, 'mouseReleased', { button: 'left', buttons: 0, clickCount: 1 });
    await sleep(200);
  }

  async insertText(text) {
    await this.send('Input.insertText', { text });
  }

  /** Screenshot of the viewport (never beyond it: RTL pages shift). Returns the PNG buffer. */
  async shot(file, clip) {
    const params = { format: 'png' };
    if (clip) {
      // A clip is in the document's coordinates: the scroll is added to a viewport rectangle.
      const [sx, sy] = await this.evaluate('[window.scrollX, window.scrollY]');
      params.clip = { ...clip, x: clip.x + sx, y: clip.y + sy, scale: 1 };
    }
    const { data } = await this.send('Page.captureScreenshot', params);
    const buffer = Buffer.from(data, 'base64');
    if (file) writeFileSync(file, buffer);
    return buffer;
  }

  async ensureAxe() {
    const has = await this.evaluate('typeof window.axe !== "undefined"');
    if (!has) {
      await this.send('Runtime.evaluate', { expression: AXE, returnByValue: false });
    }
  }

  async axe() {
    await this.ensureAxe();
    return this.evaluate(`(async () => {
      const result = await axe.run(document, { resultTypes: ['violations'] });
      return result.violations.map((v) => ({
        id: v.id, impact: v.impact, help: v.help,
        nodes: v.nodes.slice(0, 12).map((n) => ({
          target: n.target.join(' '),
          html: n.html.slice(0, 160),
          data: n.any?.[0]?.data && typeof n.any[0].data === 'object' ? n.any[0].data : undefined,
          summary: (n.failureSummary || '').slice(0, 300),
        })),
        count: v.nodes.length,
      }));
    })()`);
  }

  /** Signs in through /login?next=… and waits for the page. */
  async signIn(account, next) {
    await this.goto(`/login?next=${encodeURIComponent(next)}`);
    await this.evaluate('document.querySelector("input[type=email], input[name=email]")?.focus(); true');
    await this.insertText(account.email);
    await this.evaluate('document.querySelector("input[type=password]")?.focus(); true');
    await this.insertText(account.password);
    await this.evaluate('document.querySelector("form button[type=submit]")?.click(); true');
    for (let i = 0; i < 100; i += 1) {
      await sleep(200);
      const path = await this.evaluate('location.pathname').catch(() => '');
      if (path.startsWith(next.split('?')[0]) && path !== '/login') break;
    }
    await this.waitIdle();
    const path = await this.url();
    this.log(`signed in (${account.email.startsWith('demo') ? account.email : 'admin'}) at ${path}`);
    return path;
  }

  async close() {
    const pid = this.chrome.pid;
    try {
      execSync(`taskkill /PID ${pid} /T /F`, { stdio: 'ignore' });
    } catch {
      // already gone
    }
    await sleep(1500);
    let left = profileProcesses(this.run);
    for (const other of left) {
      try {
        execSync(`taskkill /PID ${other} /T /F`, { stdio: 'ignore' });
      } catch {
        // gone
      }
    }
    if (left.length) await sleep(1000);
    left = profileProcesses(this.run);
    this.log(`chrome ${pid} stopped by PID; cdp-profile-${this.run} processes left: ${left.length}`);
    return { pid, left };
  }
}

// ---- PNG decoding (Chrome's screenshots: 8-bit RGB or RGBA, not interlaced)
export function decodePng(buffer) {
  let offset = 8;
  let width = 0;
  let height = 0;
  let colorType = 6;
  const idat = [];
  while (offset < buffer.length) {
    const length = buffer.readUInt32BE(offset);
    const type = buffer.toString('ascii', offset + 4, offset + 8);
    const data = buffer.subarray(offset + 8, offset + 8 + length);
    if (type === 'IHDR') {
      width = data.readUInt32BE(0);
      height = data.readUInt32BE(4);
      if (data[8] !== 8) throw new Error(`bit depth ${data[8]}`);
      colorType = data[9];
      if (data[12] !== 0) throw new Error('interlaced');
    } else if (type === 'IDAT') idat.push(data);
    else if (type === 'IEND') break;
    offset += 12 + length;
  }
  const channels = colorType === 6 ? 4 : colorType === 2 ? 3 : colorType === 4 ? 2 : 1;
  const raw = inflateSync(Buffer.concat(idat));
  const stride = width * channels;
  const out = new Uint8Array(width * height * 4);
  let prev = new Uint8Array(stride);
  for (let y = 0; y < height; y += 1) {
    const filter = raw[y * (stride + 1)];
    const line = raw.subarray(y * (stride + 1) + 1, (y + 1) * (stride + 1));
    const cur = new Uint8Array(stride);
    for (let x = 0; x < stride; x += 1) {
      const a = x >= channels ? cur[x - channels] : 0;
      const b = prev[x];
      const c = x >= channels ? prev[x - channels] : 0;
      let v = line[x];
      if (filter === 1) v += a;
      else if (filter === 2) v += b;
      else if (filter === 3) v += (a + b) >> 1;
      else if (filter === 4) {
        const p = a + b - c;
        const pa = Math.abs(p - a);
        const pb = Math.abs(p - b);
        const pc = Math.abs(p - c);
        v += pa <= pb && pa <= pc ? a : pb <= pc ? b : c;
      }
      cur[x] = v & 255;
    }
    for (let x = 0; x < width; x += 1) {
      const o = (y * width + x) * 4;
      if (channels >= 3) {
        out[o] = cur[x * channels];
        out[o + 1] = cur[x * channels + 1];
        out[o + 2] = cur[x * channels + 2];
        out[o + 3] = channels === 4 ? cur[x * channels + 3] : 255;
      } else {
        out[o] = out[o + 1] = out[o + 2] = cur[x * channels];
        out[o + 3] = channels === 2 ? cur[x * channels + 1] : 255;
      }
    }
    prev = cur;
  }
  return { width, height, data: out };
}

export function pixel(img, x, y) {
  const o = (Math.round(y) * img.width + Math.round(x)) * 4;
  return [img.data[o], img.data[o + 1], img.data[o + 2], img.data[o + 3]];
}

export const hex = ([r, g, b]) => `#${[r, g, b].map((v) => v.toString(16).padStart(2, '0')).join('')}`;
export const parseHex = (h) => [1, 3, 5].map((i) => Number.parseInt(h.slice(i, i + 2), 16));
export const within = (a, b, tol = 1) => a.every((v, i) => Math.abs(v - b[i]) <= tol);
