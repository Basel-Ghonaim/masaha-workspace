// Discovery: what each screen holds (buttons, slots, API calls), to write the checks against.
import { writeFileSync } from 'node:fs';
import { accounts, launch, RAW, sleep } from './lib.mjs';

const SUMMARY = `(() => {
  const vis = (e) => window.__vp.visible(e);
  const items = (q) => [...document.querySelectorAll(q)].filter(vis).slice(0, 60).map((e) => ({
    tag: e.tagName.toLowerCase(), slot: e.getAttribute('data-slot'), role: e.getAttribute('role'),
    text: window.__vp.textOf(e).slice(0, 50), label: e.getAttribute('aria-label'),
    state: e.getAttribute('data-state'), on: e.hasAttribute('data-on') || e.getAttribute('aria-pressed') === 'true' || e.getAttribute('aria-checked') === 'true',
    current: e.getAttribute('aria-current'), href: e.getAttribute('href'), cls: (e.getAttribute('class') || '').slice(0, 140),
  }));
  const slots = {};
  for (const e of document.querySelectorAll('[data-slot]')) slots[e.getAttribute('data-slot')] = (slots[e.getAttribute('data-slot')] || 0) + 1;
  return { url: location.pathname + location.search, title: document.title, h1: [...document.querySelectorAll('h1,h2')].slice(0, 8).map((h) => h.textContent.trim().slice(0, 60)),
    slots, buttons: items('button, a[data-slot=button], [role=tab], [role=radio], [role=checkbox], [role=menuitem], [role=switch]'),
    links: items('main a').slice(0, 25), height: document.documentElement.scrollHeight };
})()`;

const page = await launch('disc');
const out = {};
const look = async (name) => {
  await page.waitIdle();
  await sleep(500);
  out[name] = await page.evaluate(SUMMARY);
  out[name].api = page.apiLog.splice(0);
  out[name].console = page.takeConsole();
  await page.shot(`${RAW}/disc-${name}.png`);
  page.log(`looked at ${name} ${out[name].url}`);
};
try {
  await page.viewport(1440, 900);
  await page.goto('/');
  await page.storePrefs('light', 'en');
  await page.goto('/');
  await look('home');
  await page.spa('/spaces');
  await look('spaces');
  await page.spa('/spaces/pal-hub');
  await look('space');
  await page.spa('/no-such-page');
  await look('404');
  await page.spa('/login');
  await look('login');
  await page.spa('/register');
  await look('register');
  await page.spa('/forgot-password');
  await look('forgot');

  const acc = accounts();
  await page.signIn(acc.owner, '/dashboard/spaces/26');
  await page.storePrefs('light', 'en');
  await page.prefs('light', 'en');
  await look('owner-overview');
  for (const seg of ['desk', 'customers', 'payments', 'finance', 'packages', 'profile', 'announcements', 'reports', 'staff', 'audit', 'settings']) {
    await page.spa(`/dashboard/spaces/26/${seg}`);
    await look(`owner-${seg}`);
  }
  await page.spa('/me');
  await look('me');
  await page.spa('/me/favorites');
  await look('favorites');
  writeFileSync(`${RAW}/../discover.json`, JSON.stringify(out, null, 1));
  // sign out locally: a fresh load for the admin, its own sign-in
  await page.send('Network.clearBrowserCookies');
  await page.goto('about:blank', { blank: false, wait: false });
  await page.signIn(acc.admin, '/dashboard/admin');
  await page.prefs('light', 'en');
  await look('admin-overview');
  for (const seg of ['spaces', 'owners', 'users', 'lookups', 'reports', 'audit', 'settings']) {
    await page.spa(`/dashboard/admin/${seg}`);
    await look(`admin-${seg}`);
  }
  await page.spa('/dashboard/admin/spaces/26');
  await look('admin-space-26');
  page.log(`refreshes ${page.refreshes}, loads ${page.loads}, blocked ${JSON.stringify(page.blocked)}`);
} catch (error) {
  page.log(`ERROR ${error.stack}`);
} finally {
  writeFileSync(`${RAW}/../discover.json`, JSON.stringify(out, null, 1));
  await page.close();
}
