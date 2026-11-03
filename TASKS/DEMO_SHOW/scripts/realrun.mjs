// The real run: local headless Chrome over CDP (Node's own WebSocket), Arabic, light, 1440 and 390.
// Signs in as each role through the sign-in form; never records a request or response body.
//   node realrun.mjs --app C:/dev/masaha/app-b --web http://localhost:5321 --out ../shots/b [--only public,admin,...] [--widths 1440,390]
import { spawn, execFileSync } from 'node:child_process';
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const arg = (name, fallback) => {
  const i = process.argv.indexOf(`--${name}`);
  return i > -1 ? process.argv[i + 1] : fallback;
};
const APP = arg('app', 'C:/dev/masaha/app-b');
const WEB = arg('web', 'http://localhost:5321');
const OUT = resolve(HERE, arg('out', '../shots/b'));
const ONLY = arg('only', 'public,admin,owner,reception,user').split(',');
const WIDTHS = arg('widths', '1440,390').split(',').map(Number);
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
mkdirSync(OUT, { recursive: true });

const env = Object.fromEntries(
  readFileSync(join(APP, 'apps/api/.env'), 'utf8')
    .split(/\r?\n/)
    .filter((l) => /^[A-Z_]+=/.test(l))
    .map((l) => [l.slice(0, l.indexOf('=')), l.slice(l.indexOf('=') + 1)]),
);
const dbName = new URL(env.DATABASE_URL).pathname.slice(1);
const sql = (q) => execFileSync('docker', ['exec', 'masaha-postgres-1', 'psql', '-U', 'masaha', '-d', dbName, '-Atc', q], { encoding: 'utf8' }).trim();
const palId = sql(`select id from spaces where slug='pal-hub'`);
const customerId = sql(`select c.id from customers c where c.space_id=${palId} and c.name='سارة خالد'`);

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const findings = [];
const chromes = [];

async function launch() {
  const port = 9300 + Math.floor(Math.random() * 600);
  const profile = mkdtempSync(join(tmpdir(), 'cdp-demo-'));
  const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`, '--no-first-run', '--no-default-browser-check', '--window-size=1440,1000', 'about:blank']);
  chromes.push(chrome);
  let targets;
  for (let i = 0; i < 60; i += 1) {
    try {
      targets = await (await fetch(`http://127.0.0.1:${port}/json`)).json();
      if (targets.some((t) => t.type === 'page')) break;
    } catch {}
    await sleep(200);
  }
  const page = targets.find((t) => t.type === 'page');
  const socket = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise((r) => socket.addEventListener('open', r));
  let id = 0;
  const pending = new Map();
  const errors = [];
  socket.addEventListener('message', (event) => {
    const m = JSON.parse(event.data);
    if (m.id !== undefined && pending.has(m.id)) {
      const { resolve: ok, reject } = pending.get(m.id);
      pending.delete(m.id);
      m.error ? reject(new Error(JSON.stringify(m.error))) : ok(m.result);
    } else if (m.method === 'Runtime.exceptionThrown') errors.push(m.params.exceptionDetails.text);
  });
  const send = (method, params = {}) => new Promise((ok, reject) => { id += 1; pending.set(id, { resolve: ok, reject }); socket.send(JSON.stringify({ id, method, params })); });
  await send('Page.enable');
  await send('Runtime.enable');
  const evaluate = async (expression) => {
    const r = await send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
    if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description ?? r.exceptionDetails.text);
    return r.result.value;
  };
  const viewport = (width, height) => send('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile: width < 768 });
  await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-color-scheme', value: 'light' }] });
  const until = async (expression, what, ms = 20000) => {
    const end = Date.now() + ms;
    while (Date.now() < end) {
      try { if (await evaluate(expression)) return; } catch {}
      await sleep(200);
    }
    throw new Error(`timed out: ${what}`);
  };
  const go = async (path) => {
    await send('Page.navigate', { url: WEB + path });
    await sleep(800);
    await until(`document.readyState === 'complete'`, 'load');
    // Until the loading skeletons and spinners are gone, at most 12 s.
    try { await until(`!document.querySelector('[aria-busy="true"], [data-loading="true"]')`, 'loaded', 12000); } catch {}
    await sleep(1600);
  };
  return { send, evaluate, viewport, until, go, errors };
}

async function signIn(b, email, password, next) {
  await b.go(`/login?next=${encodeURIComponent(next)}`);
  await b.until(`!!document.querySelector('input[type=email]')`, 'login form');
  for (const [selector, text] of [['input[type=email]', email], ['input[type=password]', password]]) {
    await b.evaluate(`(() => { const el = document.querySelector(${JSON.stringify(selector)}); el.focus(); el.select?.(); return true; })()`);
    await b.send('Input.insertText', { text });
  }
  await b.evaluate(`document.querySelector('form button[type=submit]').click(), true`);
  await b.until(`location.pathname === ${JSON.stringify(next.split('?')[0])}`, `landing on ${next}`, 25000);
  await sleep(1500);
}

async function shoot(b, role, name, path) {
  for (const width of WIDTHS) {
    await b.viewport(width, width < 768 ? 844 : 1000);
    await b.go(path);
    const height = await b.evaluate(`Math.min(document.documentElement.scrollHeight, ${width < 768 ? 6000 : 4200})`);
    await b.viewport(width, Math.max(height, width < 768 ? 844 : 1000));
    await sleep(700);
    const { data } = await b.send('Page.captureScreenshot', { format: 'png' });
    const file = `${role}-${name}-${width}.png`;
    writeFileSync(join(OUT, file), Buffer.from(data, 'base64'));
    const text = await b.evaluate('document.body.innerText');
    const full = /ممتلئ|Full\b/.test(text);
    const broken = /حدث خطأ|تعذّر|تعذر|Something went wrong|Not found|غير موجودة/.test(text);
    findings.push({ file, path, full, broken, chars: text.length, errors: b.errors.splice(0) });
    console.log(`${file}${full ? '  FULL!' : ''}${broken ? '  error text?' : ''}`);
  }
}

try {
  if (ONLY.includes('public')) {
    const b = await launch();
    await b.go('/');
    await b.evaluate(`localStorage.setItem('masaha.language','ar'); localStorage.setItem('masaha.theme','light'); true`);
    for (const [name, path] of [['home', '/'], ['directory', '/spaces'], ['map', '/spaces?view=map'], ['space-pal-hub', '/spaces/pal-hub'], ['space-branch-hub', '/spaces/branch-hub'], ['space-noor-hub', '/spaces/noor-hub'], ['space-masahat', '/spaces/masahat']]) await shoot(b, 'public', name, path);
  }
  const roles = {
    admin: { email: env.SEED_ADMIN_EMAIL, password: env.SEED_ADMIN_PASSWORD, pages: [['overview', '/dashboard/admin'], ['spaces', '/dashboard/admin/spaces'], ['owners', '/dashboard/admin/owners'], ['users', '/dashboard/admin/users'], ['reports', '/dashboard/admin/reports'], ['audit', '/dashboard/admin/audit']] },
    owner: { email: 'demo-owner@example.com', password: env.SEED_DEMO_PASSWORD, pages: [['overview', `/dashboard/spaces/${palId}`], ['desk', `/dashboard/spaces/${palId}/desk`], ['customers', `/dashboard/spaces/${palId}/customers`], ['customer-file', `/dashboard/spaces/${palId}/customers/${customerId}`], ['payments', `/dashboard/spaces/${palId}/payments`], ['finance', `/dashboard/spaces/${palId}/finance`], ['packages', `/dashboard/spaces/${palId}/packages`], ['announcements', `/dashboard/spaces/${palId}/announcements`], ['reports', `/dashboard/spaces/${palId}/reports`], ['staff', `/dashboard/spaces/${palId}/staff`], ['audit', `/dashboard/spaces/${palId}/audit`]] },
    reception: { email: 'demo-reception@example.com', password: env.SEED_DEMO_PASSWORD, pages: [['desk', `/dashboard/spaces/${palId}/desk`], ['my-payments', `/dashboard/spaces/${palId}/my-payments`]] },
    user: { email: 'demo-user@example.com', password: env.SEED_DEMO_PASSWORD, pages: [['favorites', '/me/favorites'], ['reports', '/me/reports']] },
  };
  for (const [role, r] of Object.entries(roles)) {
    if (!ONLY.includes(role)) continue;
    const b = await launch();
    await b.go('/');
    await b.evaluate(`localStorage.setItem('masaha.language','ar'); localStorage.setItem('masaha.theme','light'); true`);
    await b.viewport(1440, 1000);
    await signIn(b, r.email, r.password, r.pages[0][1]);
    for (const [name, path] of r.pages) await shoot(b, role, name, path);
  }
} finally {
  for (const c of chromes) c.kill();
  writeFileSync(join(OUT, 'findings.json'), JSON.stringify(findings, null, 2));
  const bad = findings.filter((f) => f.full || f.broken || f.errors.length);
  console.log(`${findings.length} shots; flagged: ${bad.map((f) => `${f.file}${f.full ? ' FULL' : ''}${f.broken ? ' error-text' : ''}${f.errors.length ? ' js-error' : ''}`).join(', ') || 'none'}`);
}
