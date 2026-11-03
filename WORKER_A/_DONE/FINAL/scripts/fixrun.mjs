// The fix round's short real run (7_FIX_ROUND.md §4): items 6, 10, 13, 19, 20 and 24, on the dev
// servers (web 5320, API 3320, masaha_dev), headless Chrome over CDP. Read-only: GETs, the owner's
// sign-in and its refreshes only; no reset is sent. Passwords read from apps/api/.env, never printed;
// no /auth/ body kept; phones masked in the log. Shots in FINAL\shots\fix\.
// Usage: node fixrun.mjs
import { appendFileSync, readFileSync } from 'node:fs';
import { byText, driver, launch } from './cdp.mjs';

const env = readFileSync('C:/dev/masaha/app/apps/api/.env', 'utf8');
const value = (name) =>
  new RegExp(`^${name}=(.*)$`, 'm').exec(env)?.[1]?.trim().replace(/^["']|["']$/g, '');
const OWNER = ['demo-owner@example.com', value('SEED_DEMO_PASSWORD')];
const S = '/dashboard/spaces/7';
const OUT = 'C:/dev/masaha/workspace/WORKER_A/FINAL/scripts/fixrun-log.txt';
const clean = (t) =>
  (t ?? '').replace(/[\u2066-\u2069]/g, '').replace(/\+?\d{9,}/g, '<phone>').replace(/\s+/g, ' ');
let pass = 0;
let fail = 0;
const log = (...a) => {
  const text = a.map((x) => (typeof x === 'string' ? clean(x) : JSON.stringify(x))).join(' ');
  console.log(text);
  appendFileSync(OUT, `${new Date().toISOString()} ${text}\n`);
};
const check = (name, ok, detail = '') => {
  if (ok) pass += 1;
  else fail += 1;
  log(ok ? 'PASS' : 'FAIL', name, detail);
};

async function inApp(d, path) {
  await d.evaluate(
    `window.history.pushState(null, '', ${JSON.stringify(path)}); window.dispatchEvent(new PopStateEvent('popstate', { state: null })); true`,
  );
  await d.until(`location.pathname + location.search === ${JSON.stringify(path)}`, `at ${path}`, 10000);
  await d.sleep(1500);
}

async function signIn(d) {
  await d.go('/login');
  await d.until(`!!document.querySelector('input[type=email]')`, 'login form');
  await d.type('input[type=email]', OWNER[0]);
  await d.type('input[type=password]', OWNER[1]);
  await d.click(`document.querySelector('form button[type=submit]')`, 'sign in');
  await d.until(`location.pathname !== '/login'`, 'signed in', 20000);
  await d.sleep(2000);
}

async function useLanguage(d, language) {
  await d.sleep(800);
  if ((await d.evaluate('document.documentElement.lang')) === language) return;
  const label = language === 'en' ? 'English' : 'العربية';
  await d.click(
    `[...document.querySelectorAll('button')].find((el) => el.textContent.trim() === ${JSON.stringify(label)} && el.offsetParent !== null)`,
    'the language toggle',
  );
  await d.until(`document.documentElement.lang === ${JSON.stringify(language)}`, `the ${language} interface`, 10000);
}

const shotIn = (d, name) => d.shotIn('fix', name);

/** Whether an element's right edge stays inside the viewport. */
const inside = (expression) =>
  `(() => { const el = ${expression}; if (!el) return null; const r = el.getBoundingClientRect(); return r.left >= 0 && r.right <= innerWidth + 0.5; })()`;

async function guestCases(b, d) {
  // 19: the map view's row at 390, both languages: «الفلاتر» on the screen, no sideways scroll.
  for (const language of ['ar', 'en']) {
    await d.viewport(390, 844);
    await d.go('/');
    await d.prefs(language, 'light');
    await d.go('/spaces?view=map');
    await d.until(`!!document.querySelector('input[type=search]')`, 'the map search', 20000);
    await d.sleep(1500);
    const trigger = byText('button', language === 'ar' ? 'الفلاتر' : 'Filters');
    const visible = await d.evaluate(inside(trigger));
    const scrolls = await d.evaluate('document.documentElement.scrollWidth > innerWidth');
    check(`19 map row at 390 (${language})`, visible === true && !scrolls, `trigger inside: ${String(visible)}, sideways: ${String(scrolls)}`);
    await shotIn(d, `19-map-390-${language}`);
  }

  // 24: next kept through the recovery, read-only: the links' hrefs, no reset sent.
  await d.viewport(1440, 1000);
  await d.go('/');
  await d.prefs('en', 'light');
  await d.go('/login?next=%2Fabout');
  await d.until(`!!document.querySelector('input[type=email]')`, 'login form');
  const forgot = await d.evaluate(`${byText('a', 'Forgot')}?.getAttribute('href') ?? null`);
  check('24 sign-in → forgot carries next', forgot === '/forgot-password?next=%2Fabout', forgot);
  await d.go('/forgot-password?next=%2Fabout');
  await d.until(`!!${byText('a', 'Back to sign in')}`, 'forgot page', 15000);
  const back = await d.evaluate(`${byText('a', 'Back to sign in')}.getAttribute('href')`);
  check('24 forgot → back to sign in carries next', back === '/login?next=%2Fabout', back);
  await d.go('/forgot-password?next=%2F%2Fevil.example');
  await d.until(`!!${byText('a', 'Back to sign in')}`, 'forgot page (off-site next)', 15000);
  const dropped = await d.evaluate(`${byText('a', 'Back to sign in')}.getAttribute('href')`);
  check('24 an off-site next is dropped', dropped === '/login', dropped);
  await d.go('/reset-password?next=%2Fabout');
  await d.sleep(2500);
  const resetLinks = await d.evaluate(
    `[...document.querySelectorAll('main a')].map((a) => a.textContent.trim() + ' ' + a.getAttribute('href'))`,
  );
  check(
    '24 reset page links carry next',
    resetLinks.length > 0 && resetLinks.every((line) => line.endsWith('?next=%2Fabout') || !/login|forgot/.test(line)),
    resetLinks.join(' | '),
  );
  await shotIn(d, '24-reset-next-1440-en');
}

async function ownerCases(b, d) {
  await d.viewport(1440, 1000);
  await d.go('/');
  await d.prefs('ar', 'light');
  await signIn(d);
  await useLanguage(d, 'ar');

  // 6: finance in Arabic — the debts' counted tiles and the occupancy's stay in their own direction.
  await inApp(d, `${S}/finance?tab=debts`);
  await d.until(`document.querySelectorAll('[data-slot="stat-card"]').length >= 4`, 'debts tiles', 20000);
  const debts = await d.evaluate(
    `[...document.querySelectorAll('[data-slot="stat-card"] dd:first-of-type')].map((dd) => [dd.textContent.replace(/[\\u2066-\\u2069]/g, ''), !!dd.querySelector('[dir="ltr"]')])`,
  );
  check('6 debts tiles: amounts ltr, counts not', debts.length === 4 && debts[0][1] && debts[1][1] && !debts[2][1] && !debts[3][1], JSON.stringify(debts));
  await shotIn(d, '6-finance-debts-1440-ar');
  await inApp(d, `${S}/finance?tab=occupancy`);
  await d.until(`document.querySelectorAll('[data-slot="stat-card"]').length >= 3`, 'occupancy tiles', 20000);
  const occupancy = await d.evaluate(
    `[...document.querySelectorAll('[data-slot="stat-card"] dd:first-of-type')].map((dd) => [dd.textContent.replace(/[\\u2066-\\u2069]/g, ''), !!dd.querySelector('[dir="ltr"]')])`,
  );
  check('6 occupancy: stay not ltr, peak ltr', occupancy.length === 3 && !occupancy[0][1] && occupancy[1][1], JSON.stringify(occupancy));
  await shotIn(d, '6-finance-occupancy-1440-ar');

  // 10: the desk at 390 — the owner reaches «لن تُحصَّل» from «غير محصّل»'s header.
  await d.viewport(390, 844);
  await inApp(d, `${S}/desk`);
  await d.sleep(2500);
  const toggle = await d.evaluate(`(() => { const el = ${byText('button', '^لن تُحصَّل$')}; return el ? el.offsetParent !== null : null; })()`);
  check('10 «لن تُحصَّل» reachable at 390', toggle === true, String(toggle));
  await shotIn(d, '10-desk-390-ar');

  // 13: the customers list's «⋯» on a slow connection — one held, busy item, then every item in place.
  await d.viewport(1440, 1000);
  await inApp(d, `${S}/customers`);
  await d.until(`document.querySelectorAll('table tbody tr').length > 0`, 'customers rows', 20000);
  await b.send('Network.enable');
  await b.send('Network.emulateNetworkConditions', { offline: false, latency: 2500, downloadThroughput: -1, uploadThroughput: -1 });
  await d.openMenu(`document.querySelector('table tbody tr button[aria-label^="إجراءات أخرى"]')`, 'a row «⋯»');
  await d.sleep(600);
  const reading = await d.evaluate(
    `[...document.querySelectorAll('[role=menuitem]')].map((el) => [el.textContent.trim(), el.getAttribute('aria-busy'), el.getAttribute('aria-disabled')])`,
  );
  check('13 while reading: one held busy item alone', reading.length === 1 && reading[0][1] === 'true' && reading[0][2] === 'true', JSON.stringify(reading));
  await shotIn(d, '13-customers-menu-reading-1440-ar');
  await d.sleep(4500);
  const ready = await d.evaluate(`[...document.querySelectorAll('[role=menuitem]')].map((el) => el.textContent.trim())`);
  check('13 once read: the items in place', ready.length > 1 && ready.includes('ملف الزبون'), JSON.stringify(ready));
  await shotIn(d, '13-customers-menu-ready-1440-ar');
  await d.key('Escape', 'Escape', 27);
  await b.send('Network.emulateNetworkConditions', { offline: false, latency: 0, downloadThroughput: -1, uploadThroughput: -1 });

  // 20: «اختر منطقتك» from the favourites → the place filter focused at 1440. The favourites' button
  // shows once near me is refused (no location here); without a favourite to show it, the same
  // in-app navigation the button makes is made by the history (a POP, which the shell's rule takes too).
  await inApp(d, '/me/favorites');
  await b.send('Emulation.setGeolocationOverride', {});
  const near = await d.evaluate(`!!${byText('button', 'الأقرب إليّ')}`);
  if (near) {
    await d.click(byText('button', 'الأقرب إليّ'), 'near me');
    await d.until(`!!${byText('button', 'اختر منطقتك')}`, '«اختر منطقتك»', 20000);
    await d.click(byText('button', 'اختر منطقتك'), '«اختر منطقتك»');
    await d.until(`location.pathname === '/spaces'`, 'the directory', 15000);
  } else {
    log('20 no favourite to show near me: the navigation is made in the app, by the history');
    await inApp(d, '/spaces?filters=open');
  }
  await d.sleep(2500);
  const focused = await d.evaluate(
    `(() => { const form = document.getElementById('directory-filters-form'); return !!form && form.contains(document.activeElement); })()`,
  );
  const where = await d.evaluate(`document.activeElement ? document.activeElement.tagName + '#' + document.activeElement.id : null`);
  check('20 the place filter has the focus at 1440', focused === true, String(where));
  await shotIn(d, '20-favourites-filters-1440-ar');
}

const b = await launch();
const d = driver(b);
log('fixrun start, chrome pid', b.pid);
try {
  await guestCases(b, d);
  await ownerCases(b, d);
} catch (error) {
  fail += 1;
  log('FAIL run', String(error));
} finally {
  log('errors in page', b.errors.length, b.errors.slice(0, 3));
  log(`fixrun done: ${String(pass)} pass, ${String(fail)} fail`);
  b.chrome.kill();
}
