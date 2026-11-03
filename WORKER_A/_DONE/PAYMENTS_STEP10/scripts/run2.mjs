// The lead's real run (PAYMENTS_STEP10 PRs 2, 3, 4a, 4b): headless Chrome over CDP on the dev servers.
// Usage: node run2.mjs <case>. Passwords are read from apps/api/.env and never printed; no /auth/ request's
// body is kept; no phone is printed. Enter is sent with its text ('\r'). Writes only the plan's §13 named
// writes, each named in its case.
import { appendFileSync, readFileSync, writeFileSync } from 'node:fs';
import { byLabel, byText, driver, launch } from './cdp2.mjs';
import { annCases } from './run2-ann.mjs';

const env = readFileSync('C:/dev/masaha/app/apps/api/.env', 'utf8');
const value = (name) =>
  new RegExp(`^${name}=(.*)$`, 'm').exec(env)?.[1]?.trim().replace(/^["']|["']$/g, '');
const ACCOUNTS = {
  owner: ['demo-owner@example.com', value('SEED_DEMO_PASSWORD')],
  reception: ['demo-reception@example.com', value('SEED_DEMO_PASSWORD')],
  admin: [value('SEED_ADMIN_EMAIL'), value('SEED_ADMIN_PASSWORD')],
};
const THEME = { ar: 'light', en: 'dark' };
export const tag = (language, width) => `${language}-${THEME[language]}-${width}`;
const clean = (text) =>
  (text ?? '').replace(/[\u2066-\u2069]/g, '').replace(/\+?\d{9,}/g, '<phone>').replace(/\s+/g, ' ');
const OUT = 'C:/dev/masaha/workspace/WORKER_A/PAYMENTS_STEP10/scripts/run2-log.txt';
const log = (...a) => {
  const text = a.map((x) => (typeof x === 'string' ? clean(x) : JSON.stringify(x))).join(' ');
  console.log('·', text);
  appendFileSync(OUT, `${new Date().toISOString()} [${CASE}] ${text}\n`);
};
const CASE = process.argv[2];
const SPACE = '/dashboard/spaces/7';

async function open(language, width) {
  const b = await launch();
  const d = driver(b);
  d.b = b;
  d.requests = [];
  await b.send('Network.enable');
  b.on((m) => {
    if (m.method === 'Network.requestWillBeSent' && m.params.request.url.includes('/api/v1/')) {
      d.requests.push({
        id: m.params.requestId,
        at: new Date().toISOString(),
        method: m.params.request.method,
        url: m.params.request.url.replace(/^https?:\/\/localhost:\d+/, ''),
        key: m.params.request.headers['Idempotency-Key'] ?? null,
        // An auth request's body holds the password: never kept.
        body: m.params.request.url.includes('/auth/') ? null : (m.params.request.postData ?? null),
      });
    }
    if (m.method === 'Network.responseReceived') {
      const r = d.requests.find((x) => x.id === m.params.requestId);
      if (r) r.status = m.params.response.status;
    }
    if (m.method === 'Network.loadingFailed') {
      const r = d.requests.find((x) => x.id === m.params.requestId);
      if (r) r.status = `failed (${m.params.errorText})`;
    }
  });
  await d.viewport(width, 900);
  await d.theme(THEME[language] === 'dark');
  await d.go('/');
  await d.prefs(language, THEME[language]);
  return { b, d };
}

/** A session signed in as `role`, landed on `landing`, in `language` at `width`. */
async function session(role, language, width, landing) {
  const { b, d } = await open(language, width);
  if (role !== 'guest') await signIn(d, role, landing);
  await d.prefs(language, THEME[language]);
  await d.go(landing);
  await d.until(`document.documentElement.lang === ${JSON.stringify(language)}`, `the ${language} interface`, 20000);
  await d.sleep(2500);
  return { b, d };
}

async function signIn(d, role, landing) {
  const [email, password] = ACCOUNTS[role];
  if (!(await d.evaluate(`location.pathname === '/login'`))) {
    await d.go(`/login?next=${encodeURIComponent(landing)}`);
  }
  await d.until(`!!document.querySelector('input[type=email]')`, 'login form');
  await d.type('input[type=email]', email);
  await d.type('input[type=password]', password);
  await d.click(`document.querySelector('form button[type=submit]')`, 'sign in');
  await d.until(`location.pathname === ${JSON.stringify(landing.split('?')[0].split('#')[0])}`, 'landing', 20000);
}

const toastText = (d) =>
  d.evaluate(`[...document.querySelectorAll('[data-sonner-toast]')].map((t) => (t.getAttribute('data-type') ?? '') + ': ' + t.innerText.replace(/\\n+/g, ' | ')).join(' || ')`);
const dialogText = (d) =>
  d.evaluate(`[...document.querySelectorAll('[role=dialog],[role=alertdialog]')].map((x) => x.innerText.replace(/\\n+/g, ' | ')).join(' || ')`);
const mainText = (d, n = 1500) =>
  d.evaluate(`(document.querySelector('main')?.innerText ?? '').replace(/\\n+/g, ' | ').slice(0, ${n})`);
const focused = (d) =>
  d.evaluate(`(() => { const el = document.activeElement; return el ? el.tagName + ' ' + (el.getAttribute('aria-label') ?? el.innerText ?? '').replace(/\\n+/g, ' | ').slice(0, 120) : 'none'; })()`);
const line = (r) =>
  `${r.method} ${r.url} ${r.status ?? '(no answer)'} Idempotency-Key: ${r.key ?? 'none'}${r.body ? ` body: ${clean(r.body)}` : ''}`;
const writes = (d) => d.requests.filter((r) => r.method !== 'GET' && !r.url.includes('/auth/'));
const logWrites = (d, from = 0) => writes(d).slice(from).forEach((r) => log('NET', line(r)));

/** Shots of `path` at each width, one session per language. */
async function shots(role, name, path, widths = [390, 768, 1440], { ready, languages = ['ar', 'en'], after } = {}) {
  for (const language of languages) {
    const { b, d } = await session(role, language, widths[0], path);
    for (const width of widths) {
      await d.viewport(width, 900);
      await d.go(path);
      if (ready) await d.until(ready, `${name} ready`, 20000);
      await d.sleep(1800);
      if (after) await after(d, language, width);
      await d.shot(`${name}-${role}-${tag(language, width)}`, 1600);
    }
    b.chrome.kill();
  }
}

async function finish(b) {
  b.chrome.kill();
}

const CASES = {};

// ---- PR 3: the owner's reports and the decision (write: report 1 «تم التصحيح» with «صحّحنا الساعات»).
CASES.reportsOwnerShots = () =>
  shots('owner', '3-owner-reports', `${SPACE}/reports`, [390, 768, 1440], {
    ready: `document.querySelector('main')?.innerText.includes('${'HOURS'}') || document.querySelectorAll('main table, main [data-slot=card], main li').length > 0`,
  });

CASES.reportsOwnerDecide = async () => {
  const { b, d } = await session('owner', 'ar', 1440, `${SPACE}/reports`);
  log('list', await mainText(d, 600));
  await d.click(byText('main button', '^فتح$'), 'open the report');
  await d.sleep(800);
  log('sheet', await dialogText(d));
  log('focus on opening', await focused(d));
  await d.shot('3-owner-decide-sheet-owner-ar-light-1440');
  await d.type('[role=dialog] textarea', 'صحّحنا الساعات');
  const before = writes(d).length;
  await d.click(byText('[role=dialog] button', '^تم التصحيح$'), 'corrected');
  await d.sleep(1500);
  log('toast', await toastText(d));
  log('focus after', await focused(d));
  logWrites(d, before);
  await d.shot('3-owner-decided-owner-ar-light-1440');
  await d.click(byText('main button', '^تمت المراجعة$'), 'decided chip');
  await d.sleep(1200);
  log('decided list', await mainText(d, 600));
  await d.shot('3-owner-decided-list-owner-ar-light-1440');
  await finish(b);
};

// ---- PR 3: the admin's reports (write: report 3, tuffah-place, «لم يُعتمد» with a reply).
CASES.reportsAdmin = async () => {
  const { b, d } = await session('admin', 'ar', 1440, '/dashboard/admin/reports');
  log('list', await mainText(d, 900));
  await d.shot('3-admin-reports-admin-ar-light-1440', 1600);
  // The space filter: the combobox, searched on the server.
  await d.click(byText('main button[role=combobox], main [role=combobox]', 'المساحة|كل المساحات|مساحة'), 'space filter');
  await d.sleep(600);
  await d.b.send('Input.insertText', { text: 'نور' });
  await d.sleep(1500);
  log('options', await d.evaluate(`[...document.querySelectorAll('[role=option]')].map((o) => o.innerText).join(' | ')`));
  await d.click(`[...document.querySelectorAll('[role=option]')].find((o) => /نور/.test(o.innerText))`, 'noor option');
  await d.sleep(1500);
  log('address', await d.evaluate('location.search'));
  log('tags', await d.evaluate(`[...document.querySelectorAll('main button[aria-label]')].map((x) => x.getAttribute('aria-label')).filter((x) => /إزالة|Remove/.test(x)).join(' | ')`));
  await d.shot('3-admin-filtered-admin-ar-light-1440', 1600);
  for (const width of [390, 768]) {
    await d.viewport(width, 900);
    await d.sleep(1200);
    await d.shot(`3-admin-filtered-admin-ar-light-${width}`, 1600);
  }
  await d.viewport(1440, 900);
  await d.sleep(800);
  // The verified space's report: read-only.
  await d.click(byText('main button', '^(فتح|عرض)$'), 'open noor report');
  await d.sleep(800);
  log('verified sheet', await dialogText(d));
  await d.shot('3-admin-verified-readonly-admin-ar-light-1440');
  await d.key('Escape', 'Escape', 27);
  await d.sleep(500);
  // Clear the filters; the unverified one decided.
  await d.click(byText('main button', 'مسح الفلاتر'), 'clear filters');
  await d.sleep(1500);
  log('address after clear', await d.evaluate('location.search'));
  const rows = await d.evaluate(`[...document.querySelectorAll('main tr')].map((r) => r.innerText.replace(/\\n+/g, ' | ')).join(' || ')`);
  log('rows', rows);
  await d.click(`[...document.querySelectorAll('main tr')].find((r) => /tuffah|تفاح/i.test(r.innerText))?.querySelector('button')`, 'open tuffah report');
  await d.sleep(800);
  log('unverified sheet', await dialogText(d));
  await d.type('[role=dialog] textarea', 'تجربة: لا يلزم تعديل');
  const before = writes(d).length;
  await d.click(byText('[role=dialog] button', '^لم يُعتمد$'), 'not accepted');
  await d.sleep(1500);
  log('toast', await toastText(d));
  logWrites(d, before);
  await d.shot('3-admin-dismissed-admin-ar-light-1440');
  await finish(b);
};

CASES.reportsAdminShots = () =>
  shots('admin', '3-admin-reports', '/dashboard/admin/reports', [390, 768, 1024, 1440], { languages: ['en'] });

// ---- PR 4a: «بلاغاتي», the report from a space's page, its repeat, the guest's report.
CASES.myReportsShots = () => shots('reception', '4a-my-reports', '/me/reports', [390, 768, 1440]);

CASES.reportFromPage = async () => {
  const { b, d } = await session('reception', 'ar', 1440, '/spaces/noor-hub');
  const run = async (label) => {
    await d.click(byText('main button', 'الإبلاغ عن معلومة غير صحيحة'), 'report button');
    await d.sleep(800);
    log(`${label} dialog`, await dialogText(d));
    log(`${label} focus on opening`, await focused(d));
    await d.click(`document.querySelector('[role=dialog] [role=combobox]')`, 'field select');
    await d.sleep(500);
    await d.click(`[...document.querySelectorAll('[role=option]')].find((o) => /المرافق/.test(o.innerText))`, 'amenities');
    await d.sleep(300);
    if (label === 'first') await d.shot('4a-report-dialog-reception-ar-light-1440');
    const before = writes(d).length;
    await d.click(byText('[role=dialog] button', '^إرسال$'), 'send');
    await d.sleep(1500);
    log(`${label} toast`, await toastText(d));
    log(`${label} focus after`, await focused(d));
    logWrites(d, before);
    await d.shot(`4a-report-${label}-toast-reception-ar-light-1440`);
  };
  await run('first');
  await d.sleep(4000);
  await run('repeat');
  await finish(b);
};

CASES.reportGuest = async () => {
  const { b, d } = await session('guest', 'en', 1440, '/spaces/noor-hub');
  await d.click(byText('main button', 'Report wrong information'), 'report button');
  await d.sleep(800);
  log('prompt', await dialogText(d));
  log('links', await d.evaluate(`[...document.querySelectorAll('[role=dialog] a')].map((a) => a.innerText + ' → ' + a.getAttribute('href')).join(' | ')`));
  await d.shot('4a-guest-prompt-guest-en-dark-1440');
  await d.click(byText('[role=dialog] a', '^Sign in$'), 'sign in link');
  await d.sleep(1500);
  log('at', await d.evaluate('location.pathname + location.search'));
  await signIn(d, 'reception', '/spaces/noor-hub');
  await d.sleep(2500);
  log('back on', await d.evaluate('location.pathname'));
  log('dialog after sign-in', await dialogText(d));
  await d.shot('4a-guest-back-dialog-reception-en-dark-1440');
  await d.key('Escape', 'Escape', 27);
  await d.sleep(800);
  log('dialog after close', await dialogText(d));
  log('writes', writes(d).length);
  await finish(b);
};

// ---- PR 4b: the hearts (writes: a Directory card's save then «تراجع»; Home's first card saved; noor-hub's
// page heart saved; on «المفضّلة», one removed by its heart then «تراجع»; a guest's heart on sada-space saved).
const heartOf = (scope) =>
  `[...document.querySelectorAll('${scope} button[aria-pressed]')].find((x) => /حفظ|Save|إزالة|Remove/.test(x.getAttribute('aria-label') ?? ''))`;

CASES.heartDirectory = async () => {
  const { b, d } = await session('reception', 'en', 1440, '/spaces');
  await d.until(`!!(${heartOf('main')})`, 'a card heart', 20000);
  const label = await d.evaluate(`(${heartOf('main')}).getAttribute('aria-label')`);
  log('heart', label, 'pressed', await d.evaluate(`(${heartOf('main')}).getAttribute('aria-pressed')`));
  const before = writes(d).length;
  await d.click(heartOf('main'), 'heart');
  log('pressed at once', await d.evaluate(`(${heartOf('main')}).getAttribute('aria-pressed')`));
  await d.sleep(1200);
  log('toast', await toastText(d));
  await d.shot('4b-heart-directory-reception-en-dark-1440');
  await d.click(byText('[data-sonner-toast] button', '^Undo$'), 'undo');
  await d.sleep(1500);
  log('after undo pressed', await d.evaluate(`(${heartOf('main')}).getAttribute('aria-pressed')`));
  log('toast after undo', await toastText(d));
  logWrites(d, before);
  await finish(b);
};

CASES.heartHome = async () => {
  const { b, d } = await session('reception', 'ar', 1440, '/');
  await d.until(`!!(${heartOf('main')})`, 'a card heart', 20000);
  log('heart', await d.evaluate(`(${heartOf('main')}).getAttribute('aria-label')`));
  const before = writes(d).length;
  await d.click(heartOf('main'), 'heart');
  await d.sleep(1500);
  log('toast', await toastText(d));
  logWrites(d, before);
  await d.shot('4b-heart-home-reception-ar-light-1440');
  await finish(b);
};

CASES.heartPage = async () => {
  const { b, d } = await session('reception', 'ar', 390, '/spaces/noor-hub');
  await d.until(`!!(${heartOf('main')})`, 'the page heart', 20000);
  log('heart beside h1', await d.evaluate(`(() => { const h = document.querySelector('main h1'); const x = ${heartOf('main')}; return h.parentElement.contains(x) || h.parentElement.parentElement.contains(x); })()`));
  const before = writes(d).length;
  await d.click(heartOf('main'), 'heart');
  await d.sleep(1500);
  log('toast', await toastText(d));
  logWrites(d, before);
  await d.shot('4b-heart-page-reception-ar-light-390');
  await finish(b);
};

CASES.heartGuest = async () => {
  const { b, d } = await session('guest', 'en', 1440, '/spaces/sada-space');
  await d.until(`!!(${heartOf('main')})`, 'the page heart', 20000);
  await d.click(heartOf('main'), 'heart');
  await d.sleep(800);
  log('prompt', await dialogText(d));
  await d.shot('4b-guest-prompt-guest-en-dark-1440');
  await d.click(byText('[role=dialog] a', '^Sign in$'), 'sign in link');
  await d.sleep(1200);
  log('at', await d.evaluate('location.pathname + location.search'));
  const before = writes(d).length;
  await signIn(d, 'reception', '/spaces/sada-space');
  await d.sleep(3000);
  log('toast', await toastText(d));
  log('pressed', await d.evaluate(`(${heartOf('main')})?.getAttribute('aria-pressed')`));
  logWrites(d, before);
  await d.shot('4b-guest-saved-reception-1440');
  await finish(b);
};

async function nearPoint(d) {
  await d.b.send('Browser.grantPermissions', { permissions: ['geolocation'], origin: 'http://localhost:5320' });
  // Gaza City, near the Rimal.
  await d.b.send('Emulation.setGeolocationOverride', { latitude: 31.52, longitude: 34.45, accuracy: 20 });
}

CASES.favorites = async () => {
  for (const language of ['ar', 'en']) {
    const { b, d } = await session('reception', language, 1440, '/me/favorites');
    await nearPoint(d);
    for (const width of [390, 768, 1440]) {
      await d.viewport(width, 900);
      await d.go('/me/favorites');
      await d.sleep(2500);
      if (width === 1440) log(`${language} list`, await mainText(d, 700));
      await d.shot(`4b-favorites-reception-${tag(language, width)}`, 1600);
    }
    if (language === 'ar') {
      await d.click(byText('main button', 'الأقرب إليّ'), 'near me');
      await d.sleep(3000);
      log('near: address', await d.evaluate('location.search'), 'list', await mainText(d, 700));
      log('near reads', d.requests.filter((r) => r.url.includes('/me/favorites')).map((r) => `${r.method} ${r.url} ${r.status}`).join(' | '));
      await d.shot('4b-favorites-near-reception-ar-light-1440', 1600);
      // A favourite removed by its heart, then «تراجع».
      const before = writes(d).length;
      log('remove', await d.evaluate(`(${heartOf('main')}).getAttribute('aria-label')`));
      await d.click(heartOf('main'), 'heart (remove)');
      await d.sleep(1500);
      log('toast', await toastText(d));
      await d.shot('4b-favorites-removed-reception-ar-light-1440', 1600);
      await d.click(byText('[data-sonner-toast] button', '^تراجع$'), 'undo');
      await d.sleep(2000);
      log('after undo', await mainText(d, 500));
      logWrites(d, before);
    }
    await finish(b);
  }
};

CASES.heartCheck = async () => {
  const { b, d } = await session('reception', 'en', 1440, '/spaces/sada-space');
  await d.until(`!!(${heartOf('main')})`, 'the page heart', 20000);
  for (let i = 0; i < 6; i += 1) {
    log(`t+${i}s pressed`, await d.evaluate(`(${heartOf('main')}).getAttribute('aria-pressed')`), await d.evaluate(`(${heartOf('main')}).getAttribute('aria-label')`));
    await d.sleep(1000);
  }
  log('reads', d.requests.filter((r) => r.url.includes('/me/favorites')).map((r) => `${r.method} ${r.url} ${r.status}`).join(' | '));
  await finish(b);
};

const ANN = `${SPACE}/announcements`;
const controls = (d, scope = '[role=dialog]') =>
  d.evaluate(`[...document.querySelectorAll('${scope} input, ${scope} textarea, ${scope} button, ${scope} [role=radio], ${scope} [role=combobox]')].map((x) => [x.tagName, x.getAttribute('role'), x.getAttribute('type'), x.id, x.getAttribute('aria-label'), (x.labels?.[0]?.innerText ?? ''), (x.innerText ?? '').slice(0, 30), x.getAttribute('aria-checked') ?? x.getAttribute('data-state')].join(' ~ ')).join(' ¶ ')`);

CASES.annProbe = async () => {
  const { b, d } = await session('reception', 'en', 1440, ANN);
  log('main', await mainText(d, 600));
  await d.click(byText('main button', '^New announcement$'), 'new');
  await d.sleep(1000);
  console.log(await controls(d));
  log('focus on opening', await focused(d));
  await d.key('Escape', 'Escape', 27);
  await finish(b);
};

CASES.spacePageClosure = async () => {
  for (const language of ['ar', 'en']) {
    const { b, d } = await session('guest', language, 1440, '/spaces/masaha-demo');
    for (const width of [390, 768, 1440]) {
      await d.viewport(width, 900);
      await d.go('/spaces/masaha-demo');
      await d.until(`!!document.querySelector('main h1')`, 'the page', 20000);
      await d.sleep(2500);
      const order = await d.evaluate(`(() => {
        const notice = [...document.querySelectorAll('main [role=status]')].find((x) => x.innerText.includes('إغلاق تجربة'));
        const h1 = document.querySelector('main h1');
        const prices = [...document.querySelectorAll('main h2')].find((x) => /الأسعار|Prices/.test(x.innerText));
        const section = [...document.querySelectorAll('main h2')].find((x) => /^(الإعلانات|Announcements)$/.test(x.innerText.trim()));
        const after = (a, z) => !!a && !!z && !!(a.compareDocumentPosition(z) & Node.DOCUMENT_POSITION_FOLLOWING);
        return { notice: notice ? notice.innerText.split(String.fromCharCode(10)).join(' | ') : null, noticeBeforeName: after(notice, h1), section: !!section, sectionBeforePrices: after(section, prices) };
      })()`);
      log(`${language} ${width}`, order);
      await d.shot(`4b-space-closure-guest-${tag(language, width)}`, 1600);
    }
    await finish(b);
  }
};

CASES.annActiveShots = async () => {
  for (const role of ['reception', 'owner']) {
    for (const language of ['ar', 'en']) {
      const { b, d } = await session(role, language, 1440, `${SPACE}/announcements`);
      for (const width of [390, 768, 1440]) {
        await d.viewport(width, 900);
        await d.go(`${SPACE}/announcements`);
        await d.sleep(2500);
        if (width === 1440) log(`${role} ${language}`, await mainText(d, 500));
        await d.shot(`2-active-${role}-${tag(language, width)}`, 1600);
      }
      await finish(b);
    }
  }
};

const hitArea = (d, expression) =>
  d.evaluate(`(() => { const el = ${expression}; if (!el) return null; const r = el.getBoundingClientRect(); return Math.round(r.width) + 'x' + Math.round(r.height) + ' ' + (el.getAttribute('aria-label') ?? el.innerText).slice(0, 60); })()`);

CASES.touch = async () => {
  const out = [];
  const touchOn = async (d) => {
    await d.b.send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
    await d.b.send('Emulation.setEmitTouchEventsForMouse', { enabled: true });
  };
  {
    const { b, d } = await session('reception', 'ar', 390, `${SPACE}/announcements`);
    await touchOn(d);
    await d.go(`${SPACE}/announcements`);
    await d.sleep(2500);
    out.push(['announcements «⋯»', await hitArea(d, `[...document.querySelectorAll('main button')].find((x) => /^إجراءات أخرى/.test(x.getAttribute('aria-label') ?? ''))`)]);
    await d.go('/spaces');
    await d.sleep(3000);
    out.push(['the heart (card)', await hitArea(d, `[...document.querySelectorAll('main button[aria-pressed]')][0]`)]);
    await d.go('/spaces/noor-hub');
    await d.sleep(3000);
    out.push(['the heart (page)', await hitArea(d, `[...document.querySelectorAll('main button[aria-pressed]')][0]`)]);
    await finish(b);
  }
  {
    const { b, d } = await session('admin', 'ar', 390, '/dashboard/admin/reports?space=48');
    await touchOn(d);
    await d.go('/dashboard/admin/reports?space=48');
    await d.sleep(3000);
    out.push(['FilterTag', await hitArea(d, `[...document.querySelectorAll('main button[aria-label]')].find((x) => /إزالة فلتر/.test(x.getAttribute('aria-label')))`)]);
    await d.shot('3-admin-filtertag-admin-ar-light-390', 1200);
    await finish(b);
  }
  for (const [what, area] of out) log('touch', what, area);
};

CASES.accountMenu = async () => {
  for (const [language, width] of [['ar', 1440], ['en', 390]]) {
    const { b, d } = await session('reception', language, width, '/spaces');
    await d.shot(`debug-account-${language}-${width}`, 900);
    log('size', await d.evaluate('innerWidth + "x" + innerHeight'));
    log('buttons', await d.evaluate(`[...document.querySelectorAll('button')].slice(0, 12).map((x) => (x.getAttribute('aria-label') ?? '') + '/' + x.innerText.trim().slice(0, 20) + '/' + (x.getAttribute('aria-haspopup') ?? '')).join(' | ')`));
    if (width === 1440) {
      await d.openMenu(`[...document.querySelectorAll('button')].find((x) => /^(قائمة الحساب|Account menu)/.test(x.getAttribute('aria-label') ?? ''))`, 'account menu');
    } else {
      await d.click(`[...document.querySelectorAll('button')].find((x) => /^(القائمة|Menu)$/.test((x.getAttribute('aria-label') ?? x.innerText).trim()))`, 'phone menu');
      await d.sleep(800);
    }
    log(`${language} ${width} menu`, await d.evaluate(`[...document.querySelectorAll('[role=menu] a, [role=dialog] a, [role=menu] [role=menuitem]')].map((x) => x.innerText.trim() + ' → ' + (x.getAttribute('href') ?? '')).join(' | ')`));
    await d.shot(`4a-account-menu-reception-${tag(language, width)}`, 1000);
    await finish(b);
  }
};

annCases({ CASES, session, finish, log, byText, writes, logWrites, toastText, dialogText, mainText, focused, tag, SPACE });

const name = process.argv[2];
if (!CASES[name]) {
  console.error(`cases: ${Object.keys(CASES).join(' ')}`);
  process.exit(2);
}
writeFileSync(`C:/dev/masaha/workspace/WORKER_A/PAYMENTS_STEP10/scripts/run2-${name}.json`, '[]');
try {
  await CASES[name]();
} catch (error) {
  log('ERROR', String(error.message ?? error));
  process.exitCode = 1;
}
process.exit(process.exitCode ?? 0);
