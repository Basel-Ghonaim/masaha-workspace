// FINAL's real run, part 1: a tour of every screen by every role (plan §11, read-only). Headless Chrome over
// CDP on the dev servers (web 5320, API 3320, masaha_dev). Each screen: English in dark at 390 and 1440 (plus 768
// where a layout changes) and Arabic in light at 1440 — text checks logged PASS/FAIL, the shots saved to
// FINAL\shots\tour\ (for the owner; the lead opens only a few). Passwords read from apps/api/.env, never printed;
// no /auth/ request body kept; phones masked. GETs only: no case of this file writes anything.
// Usage: node tour.mjs <role|all>
import { appendFileSync, readFileSync } from 'node:fs';
import { driver, launch } from './cdp.mjs';

const env = readFileSync('C:/dev/masaha/app/apps/api/.env', 'utf8');
const value = (name) =>
  new RegExp(`^${name}=(.*)$`, 'm').exec(env)?.[1]?.trim().replace(/^["']|["']$/g, '');
const ACCOUNTS = {
  owner: ['demo-owner@example.com', value('SEED_DEMO_PASSWORD')],
  reception: ['demo-reception@example.com', value('SEED_DEMO_PASSWORD')],
  admin: [value('SEED_ADMIN_EMAIL'), value('SEED_ADMIN_PASSWORD')],
  user: [process.env.RUN_USER_EMAIL, process.env.RUN_USER_PASSWORD],
};
const OUT = 'C:/dev/masaha/workspace/WORKER_A/FINAL/scripts/tour-log.txt';
const clean = (t) =>
  (t ?? '').replace(/[\u2066-\u2069]/g, '').replace(/\+?\d{9,}/g, '<phone>').replace(/\s+/g, ' ');
const log = (...a) => {
  const text = a.map((x) => (typeof x === 'string' ? clean(x) : JSON.stringify(x))).join(' ');
  console.log(text);
  appendFileSync(OUT, `${new Date().toISOString()} ${text}\n`);
};

const S = '/dashboard/spaces/7';
const A = '/dashboard/admin';
// [path, English texts that must show, { wide: shoot 768 too, absent: texts that must not show, forbidden: a 403 }]
const SCREENS = {
  guest: [
    ['/', ['Find a workspace'], { wide: true }],
    ['/spaces', ['Workspaces'], { wide: true }],
    ['/spaces?view=map', ['Workspaces'], {}],
    ['/about', ['About Masaha'], { wide: true }],
    ['/login', ['Sign in', 'Back to home'], {}],
    ['/register', ['Create account'], {}],
    ['/forgot-password', ['Forgot password', 'Back to sign in'], {}],
    ['/no-such-page', ['Page not found'], {}],
  ],
  user: [
    ['/me', ['Account settings', 'Profile', 'Preferences', 'Signing in'], { wide: true }],
    ['/me/favorites', ['Favourites'], {}],
    ['/me/reports', ['My reports'], {}],
    ['/dashboard/admin', ['If you think this is a mistake'], {}],
  ],
  owner: [
    [S, ['Needs your attention', 'Present now', 'Subscriptions ending this week'], { wide: true, absent: ['₪', 'ILS'] }],
    [`${S}/desk`, ['Log'], { wide: true }],
    [`${S}/customers`, ['Customers'], { wide: true }],
    [`${S}/payments`, ['Payments'], {}],
    [`${S}/finance`, ['Income', 'Debts', 'Occupancy'], { wide: true }],
    [`${S}/finance?tab=debts`, ['Total owed', 'Uncollected visits'], {}],
    [`${S}/finance?tab=occupancy`, ['Average stay', 'Peak hours'], {}],
    [`${S}/packages`, ['Available at the desk'], {}],
    [`${S}/profile`, ['Space profile'], {}],
    [`${S}/announcements`, ['Announcements'], {}],
    [`${S}/reports`, ['Data reports'], {}],
    [`${S}/staff`, ['Collected this month', 'Added'], { wide: true }],
    [`${S}/audit`, ['Audit log', 'Events:'], { wide: true }],
    [`${S}/settings`, ['My account', 'Personal settings'], {}],
  ],
  reception: [
    [`${S}/desk`, ['Front desk'], { wide: true }],
    [`${S}/customers`, ['Customers'], {}],
    [`${S}/my-payments`, ['My payments today'], {}],
    [`${S}/announcements`, ['Announcements'], {}],
    [`${S}/finance`, ['You don’t have access to this page'], {}],
    [`${S}/audit`, ['You don’t have access to this page'], {}],
  ],
  admin: [
    [A, ['Platform summary', 'Data completeness', 'New users'], { wide: true }],
    [`${A}/spaces`, ['Spaces'], { wide: true }],
    [`${A}/spaces?status=editable&stale=true`, ['Kept by the admin'], {}],
    [`${A}/owners`, ['Space owners'], {}],
    [`${A}/reports`, ['Data reports', 'Handled by'], {}],
    [`${A}/users`, ['Users'], {}],
    [`${A}/lookups`, ['Lookups'], {}],
    [`${A}/audit`, ['Audit log', 'Platform events only'], { wide: true }],
    [`${A}/settings`, ['Platform settings', 'Platform contact', 'Data freshness', 'Defaults for new spaces'], { wide: true }],
  ],
};
// The sidebar's groups, checked once per dashboard role (finding 165).
const GROUPS = {
  owner: ['Today', 'Money', 'The space', 'Team & settings'],
  admin: ['Spaces', 'The platform'],
};

async function open(language, width) {
  const b = await launch();
  const d = driver(b);
  d.requests = [];
  await b.send('Network.enable');
  b.on((m) => {
    if (m.method === 'Network.requestWillBeSent' && m.params.request.url.includes('/api/v1/')) {
      d.requests.push({
        id: m.params.requestId,
        method: m.params.request.method,
        url: m.params.request.url.replace(/^https?:\/\/localhost:\d+/, ''),
        key: m.params.request.headers['Idempotency-Key'] ?? null,
      });
    }
    if (m.method === 'Network.responseReceived') {
      const r = d.requests.find((x) => x.id === m.params.requestId);
      if (r) r.status = m.params.response.status;
    }
  });
  await d.viewport(width, 900);
  await d.theme(language === 'en');
  await d.go('/');
  await d.prefs(language, language === 'en' ? 'dark' : 'light');
  return { b, d };
}

async function signIn(d, role) {
  const [email, password] = ACCOUNTS[role];
  await d.go('/login');
  await d.until(`!!document.querySelector('input[type=email]')`, 'login form');
  await d.type('input[type=email]', email);
  await d.type('input[type=password]', password);
  await d.click(`document.querySelector('form button[type=submit]')`, 'sign in');
  await d.until(`location.pathname !== '/login'`, 'signed in', 20000);
  await d.sleep(1500);
}

/**
 * Signing in applies the account's saved language; the tour then switches to its own with the header's
 * toggle, as a person would (this device's choice only, DI20).
 */
async function useLanguage(d, language) {
  await d.sleep(1000);
  if ((await d.evaluate('document.documentElement.lang')) === language) return;
  const label = language === 'en' ? 'English' : 'العربية';
  await d.click(
    `[...document.querySelectorAll('button')].find((el) => el.textContent.trim() === ${JSON.stringify(label)} && el.offsetParent !== null)`,
    'the language toggle',
  );
  await d.until(`document.documentElement.lang === ${JSON.stringify(language)}`, `the ${language} interface`, 10000);
}

/**
 * Goes to `path` inside the app, as a link does, with no reload: every reload restores the session by
 * a refresh, and the refresh's rate limit (rightly) refuses a tour that reloads thirty pages a minute.
 */
async function inApp(d, path) {
  await d.evaluate(
    `window.history.pushState(null, '', ${JSON.stringify(path)}); window.dispatchEvent(new PopStateEvent('popstate', { state: null })); true`,
  );
  await d.until(`location.pathname + location.search === ${JSON.stringify(path)}`, `at ${path}`, 10000);
}

const pageText = (d) =>
  d.evaluate(`(document.body.innerText ?? '').replace(/[\\u2066-\\u2069]/g, '')`);

async function tour(role) {
  let pass = 0;
  let fail = 0;
  for (const [language, widths] of [
    ['en', [1440, 390]],
    ['ar', [1440]],
  ]) {
    const { b, d } = await open(language, widths[0]);
    if (role !== 'guest') {
      await signIn(d, role);
      await useLanguage(d, language);
    }
    for (const [path, texts, opts] of SCREENS[role]) {
      const ws = opts.wide && language === 'en' ? [1440, 768, 390] : widths;
      for (const width of ws) {
        await d.viewport(width, 900);
        if (role === 'guest') await d.go(path);
        else await inApp(d, path);
        await d.sleep(2500);
        const name = `${role}${path.replaceAll('/', '_').replace(/[?=&]/g, '-')}-${language}-${width}`;
        if (language === 'en' && width === 1440) {
          const text = await pageText(d);
          const missing = texts.filter((t) => !text.includes(t));
          const present = (opts.absent ?? []).filter((t) => text.includes(t));
          const errors = d.requests.filter((r) => typeof r.status === 'number' && r.status >= 500);
          const ok = missing.length === 0 && present.length === 0 && errors.length === 0;
          ok ? (pass += 1) : (fail += 1);
          const h1 = ok ? '' : await d.evaluate(`[...document.querySelectorAll('h1')].map((h) => h.innerText).join(' / ')`);
          log(ok ? 'PASS' : 'FAIL', role, path, ok ? '' : `h1: ${h1}`, missing.length ? `missing: ${missing.join(' | ')}` : '', present.length ? `present: ${present.join(' | ')}` : '', errors.length ? `5xx: ${errors.map((r) => r.url).join(', ')}` : '');
          const groups = GROUPS[role];
          if (groups && path === SCREENS[role][0][0]) {
            const nav = await d.evaluate(`[...document.querySelectorAll('nav [role=group]')].map((g) => document.getElementById(g.getAttribute('aria-labelledby'))?.textContent)`);
            const same = JSON.stringify(nav) === JSON.stringify(groups);
            same ? (pass += 1) : (fail += 1);
            log(same ? 'PASS' : 'FAIL', role, 'sidebar groups', JSON.stringify(nav));
          }
        }
        await d.shotIn('tour', name);
      }
    }
    const fives = d.requests.filter((r) => typeof r.status === 'number' && r.status >= 500);
    log('NET', role, language, `${d.requests.length} API requests, writes: ${d.requests.filter((r) => r.method !== 'GET' && !r.url.includes('/auth/')).map((r) => `${r.method} ${r.url} ${r.status}`).join(', ') || 'none'}; 5xx: ${fives.length}`);
    if (d.errors?.length) log('PAGE ERRORS', role, language, d.errors.slice(0, 5).join(' || '));
    b.chrome.kill();
  }
  log('TOTAL', role, `pass ${pass}, fail ${fail}`);
}

const which = process.argv[2] ?? 'all';
for (const role of which === 'all' ? Object.keys(SCREENS) : [which]) {
  if (role === 'user' && !ACCOUNTS.user[0]) {
    log('SKIP user (no RUN_USER_EMAIL: R1 registers it first)');
    continue;
  }
  await tour(role);
}
