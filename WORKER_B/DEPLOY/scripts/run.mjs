// DEPLOY's production-shaped proof: headless Chrome over CDP against serve.mjs (vercel.json's headers
// and rewrites over the production build) in front of the function (api.mjs) on masaha_b_dev.
// Every page × ar/en × 390/1440: CSP violations (the page's own securitypolicyviolation events and
// the console's security messages), deep-link reloads, the map's tiles, a gallery, Google's button,
// the admin's add-space map, a photo picked but never sent (the POST is failed before it leaves).
// The admin's password is read from apps/api/.env and never printed; no request body is kept.
import { execSync } from 'node:child_process';
import { appendFileSync, readFileSync, writeFileSync } from 'node:fs';
import { byText, driver, launch } from './cdp.mjs';

const env = readFileSync('C:/dev/masaha/app-b/apps/api/.env', 'utf8');
const value = (name) =>
  new RegExp(`^${name}=(.*)$`, 'm').exec(env)?.[1]?.trim().replace(/^["']|["']$/g, '');
const ADMIN = { email: value('SEED_ADMIN_EMAIL'), password: value('SEED_ADMIN_PASSWORD') };
const PHOTO = 'C:/dev/masaha/workspace/WORKER_B/DEPLOY/scripts/photo.jpg';
const OUT = 'C:/dev/masaha/workspace/WORKER_B/DEPLOY/scripts/run-log.txt';
writeFileSync(OUT, '');
const log = (...a) => {
  const text = a.map((x) => (typeof x === 'string' ? x : JSON.stringify(x))).join(' ');
  console.log('·', text);
  appendFileSync(OUT, `${new Date().toISOString()} ${text}\n`);
};

const COLLECT = `
  document.addEventListener('securitypolicyviolation', (e) => {
    window.cspReport(JSON.stringify({ directive: e.violatedDirective, blocked: e.blockedURI, source: e.sourceFile, line: e.lineNumber, sample: e.sample }));
  });`;

const totals = { pages: 0, violations: [], console: [], reloads: { ok: 0, bad: [] }, checks: [] };

async function open(language, width) {
  const b = await launch();
  const d = driver(b);
  const violations = [];
  const consoleErrors = [];
  const documents = [];
  await b.send('Runtime.addBinding', { name: 'cspReport' });
  await b.send('Page.addScriptToEvaluateOnNewDocument', { source: COLLECT });
  await b.send('Log.enable');
  await b.send('Network.enable');
  // A photo upload is failed before it is sent: the shrink and the preview run, no write is made.
  await b.send('Fetch.enable', { patterns: [{ urlPattern: '*/photos*', requestStage: 'Request' }] });
  b.on((m) => {
    if (m.method === 'Runtime.bindingCalled' && m.params.name === 'cspReport') violations.push(JSON.parse(m.params.payload));
    if (m.method === 'Log.entryAdded' && (m.params.entry.level === 'error' || m.params.entry.source === 'security')) {
      consoleErrors.push(`${m.params.entry.source}: ${m.params.entry.text} ${m.params.entry.url ?? ''}`.slice(0, 300));
    }
    if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') {
      consoleErrors.push(`console: ${m.params.args.map((x) => x.value ?? x.description ?? '').join(' ')}`.slice(0, 300));
    }
    if (m.method === 'Network.responseReceived' && m.params.type === 'Document') {
      documents.push({ url: m.params.response.url, status: m.params.response.status });
    }
    if (m.method === 'Fetch.requestPaused') {
      const { requestId, request } = m.params;
      if (request.method === 'POST') {
        log('photo upload held and failed before sending:', request.method, request.url.replace(/^https?:\/\/localhost:\d+/, ''));
        totals.checks.push('photo POST stopped before sending');
        void b.send('Fetch.failRequest', { requestId, errorReason: 'BlockedByClient' });
      } else {
        void b.send('Fetch.continueRequest', { requestId });
      }
    }
  });
  await d.viewport(width, 900);
  await d.go('/');
  await d.prefs(language, language === 'ar' ? 'light' : 'dark');
  return { b, d, violations, consoleErrors, documents };
}

async function page(ctx, tag, path, ready, what) {
  const { d } = ctx;
  await d.go(path);
  await d.until(ready, `${what} at ${path}`, 25000);
  await d.sleep(1200);
  await d.shotIn(tag, what.replace(/\W+/g, '-'));
  totals.pages += 1;
  log(tag, 'ok', path, what);
}

async function reload(ctx, tag, path, ready) {
  const { b, d, documents } = ctx;
  await d.go(path);
  await d.until(ready, `before reload ${path}`, 25000);
  const before = documents.length;
  await b.send('Page.reload', { ignoreCache: true });
  await d.sleep(1500);
  try {
    await d.until(ready, `after reload ${path}`, 25000);
    const doc = documents.slice(before).find((x) => new URL(x.url).pathname === path.split('?')[0]);
    const pathname = await d.evaluate('location.pathname');
    if (doc?.status === 200 && pathname === path.split('?')[0]) {
      totals.reloads.ok += 1;
      log(tag, 'reload ok', path, doc.status);
    } else {
      totals.reloads.bad.push(`${tag} ${path} ${doc?.status} ${pathname}`);
      log(tag, 'reload BAD', path, doc?.status, pathname);
    }
  } catch (error) {
    totals.reloads.bad.push(`${tag} ${path} ${error.message}`);
    log(tag, 'reload BAD', path, error.message);
  }
}

const ROOT_DRAWN = `document.querySelector('#root')?.children.length > 0 && !!document.querySelector('main, [role=main], h1')`;
const TILE_LOADED = `[...document.querySelectorAll('img.leaflet-tile')].some((img) => img.complete && img.naturalWidth > 0 && img.src.includes('tile.openstreetmap.org'))`;
const GALLERY_LOADED = `[...document.querySelectorAll('img')].some((img) => img.src.includes('/api/v1/files/') && img.complete && img.naturalWidth > 0)`;
const GOOGLE_BUTTON = `!!document.querySelector('iframe[src*="accounts.google.com/gsi/"]')`;

async function run(language, width) {
  const tag = `${language}-${width}`;
  // The proof's own requests come from one address; each context starts with masaha_b_dev's
  // rate-limit counters cleared (the one write besides none: the photo POST is failed unsent).
  execSync(`docker exec masaha-postgres-1 psql -U masaha -d masaha_b_dev -tAc "delete from rate_limits"`);
  const ctx = await open(language, width);
  const { d } = ctx;
  try {
    await page(ctx, tag, '/', ROOT_DRAWN, 'home');
    await page(ctx, tag, '/spaces', ROOT_DRAWN, 'directory');
    await d.click(byText('button, a, [role=tab], [role=radio]', language === 'ar' ? '^\\s*خريطة\\s*$' : '^\\s*Map\\s*$'), 'the map toggle');
    await d.until(TILE_LOADED, 'directory map tiles', 25000);
    await d.sleep(1500);
    await d.shotIn(tag, 'directory-map');
    totals.checks.push(`${tag} directory map tiles loaded`);
    await page(ctx, tag, '/spaces/noor-hub', GALLERY_LOADED, 'space gallery');
    await page(ctx, tag, '/login', GOOGLE_BUTTON, 'sign-in with Google button');
    totals.checks.push(`${tag} Google button iframe drawn`);
    await page(ctx, tag, '/register', ROOT_DRAWN, 'register');

    for (const path of ['/spaces', '/spaces/noor-hub', '/login', '/about', '/no-such-page']) {
      await reload(ctx, tag, path, ROOT_DRAWN);
    }

    // The admin: the add-space map, and a photo picked on a space's editor.
    await d.go('/login?next=%2Fdashboard%2Fadmin%2Fspaces%2Fnew');
    await d.until(`!!document.querySelector('input[type=email]')`, 'login form');
    await d.type('input[type=email]', ADMIN.email);
    await d.type('input[type=password]', ADMIN.password);
    await d.click(`document.querySelector('form button[type=submit]')`, 'sign in');
    await d.until(`location.pathname === '/dashboard/admin/spaces/new'`, 'the add-space page', 25000);
    await d.until(TILE_LOADED, 'add-space map tiles', 25000);
    await d.sleep(1500);
    await d.shotIn(tag, 'admin-add-space-map');
    totals.pages += 1;
    totals.checks.push(`${tag} admin add-space map tiles loaded`);
    await reload(ctx, tag, '/dashboard/admin/spaces/new', TILE_LOADED);

    let picked = false;
    for (const id of [3, 5, 6, 7, 8, 9, 10, 12]) {
      await d.go(`/dashboard/admin/spaces/${id}`);
      try {
        await d.until(`!!document.querySelector('input[type=file]')`, 'a photo input', 8000);
      } catch {
        continue;
      }
      const { root } = await ctx.b.send('DOM.getDocument', { depth: -1, pierce: true });
      const { nodeId } = await ctx.b.send('DOM.querySelector', { nodeId: root.nodeId, selector: 'input[type=file]' });
      await ctx.b.send('DOM.setFileInputFiles', { nodeId, files: [PHOTO] });
      await d.sleep(4000);
      await d.shotIn(tag, `admin-photo-picked-space-${id}`);
      totals.pages += 1;
      log(tag, 'photo picked on space', id);
      picked = true;
      break;
    }
    if (!picked) log(tag, 'NO photo input found');
  } catch (error) {
    log(tag, 'ERROR', error.message);
    await d.shotIn(tag, 'error').catch(() => {});
    totals.checks.push(`${tag} ERROR ${error.message}`);
  } finally {
    for (const v of ctx.violations) totals.violations.push({ tag, ...v });
    for (const c of ctx.consoleErrors) totals.console.push(`${tag} ${c}`);
    log(tag, 'csp violations', ctx.violations.length, 'console errors', ctx.consoleErrors.length);
    ctx.b.chrome.kill();
  }
}

for (const language of ['ar', 'en']) {
  for (const width of [390, 1440]) {
    await run(language, width);
  }
}
log('TOTAL pages', totals.pages, 'reloads ok', totals.reloads.ok, 'bad', totals.reloads.bad.length);
log('CSP violations', totals.violations.length, totals.violations);
log('console errors', totals.console.length, totals.console);
log('checks', totals.checks);
process.exit(0);
