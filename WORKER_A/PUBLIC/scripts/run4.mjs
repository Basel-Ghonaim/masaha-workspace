// PUBLIC PR 4's real run: Home, About, the offline state and the footer, in local headless Chrome over CDP.
// Usage: node run4.mjs <part> — part: layouts | home | about | offline | none (About with no contact).
import { writeFileSync } from 'node:fs';
import { byText, driver, launch } from './cdp4.mjs';

const part = process.argv[2];
const b = await launch();
const d = driver(b);
const requests = [];
await b.send('Network.enable');
b.on((m) => {
  if (m.method === 'Network.requestWillBeSent') {
    const { url, headers } = m.params.request;
    if (url.includes('/api/')) requests.push({ url, near: headers['Masaha-Near'] ?? null });
  }
});
const log = (...line) => console.log(...line);

/** Opens `path` in a language and theme, at a width. */
async function open(path, language, dark, width) {
  await d.viewport(width);
  await d.go('/');
  await d.prefs(language, dark ? 'dark' : 'light');
  await d.theme(dark);
  await d.go(path);
  await d.until(`document.documentElement.lang === ${JSON.stringify(language)}`, 'language ' + language);
  await d.until(`!!document.querySelector('main h1')`, 'h1 on ' + path);
  await d.sleep(1200);
}

/** A full-page shot: the viewport grown to the page's height, then back. */
async function fullShot(name, width) {
  const height = await d.evaluate('document.documentElement.scrollHeight');
  await d.viewport(width, Math.min(height, 6000));
  await d.sleep(500);
  await d.shot(name);
  await d.viewport(width);
}

const VARIANTS = [
  ['ar', false, 'ar-light'],
  ['en', true, 'en-dark'],
];

try {
  if (part === 'layouts') {
    for (const [language, dark, tag] of VARIANTS) {
      for (const width of [390, 768, 1440]) {
        await open('/', language, dark, width);
        await d.until(`document.querySelectorAll('main a[href^="/spaces/"]').length > 0`, 'home cards');
        await d.until(`document.querySelectorAll('main a[href^="/spaces?area="]').length > 0`, 'area cards');
        log(tag, width, 'home h2s:', await d.evaluate(`[...document.querySelectorAll('main h2')].map((h) => h.textContent).join(' | ')`));
        log(tag, width, 'home cards:', await d.evaluate(`document.querySelectorAll('main a[href^="/spaces/"]').length`), 'area cards:', await d.evaluate(`[...document.querySelectorAll('main a[href^="/spaces?area="], main a[href="/spaces"]')].map((a) => a.textContent.replace(/[\\u2066-\\u2069]/g, '')).join(' / ')`));
        await fullShot(`4-home-${tag}-${width}`, width);
        await open('/about', language, dark, width);
        log(tag, width, 'about h2s:', await d.evaluate(`[...document.querySelectorAll('main h2')].map((h) => h.textContent).join(' | ')`));
        await fullShot(`4-about-${tag}-${width}`, width);
      }
    }
  }

  if (part === 'home') {
    for (const [language, dark, tag, width] of [
      ['ar', false, 'ar-light', 390],
      ['en', true, 'en-dark', 1440],
    ]) {
      // The hero's search, submitted by Enter, opens the Directory with q.
      await open('/', language, dark, width);
      await d.type('form[role=search] input[type=search]', language === 'ar' ? 'نور' : 'Noor Hub');
      await d.enter();
      await d.until(`location.pathname === '/spaces'`, 'directory from the search');
      await d.sleep(1500);
      log(tag, 'search →', await d.evaluate('location.pathname + location.search'));
      await d.shot(`4-home-search-${tag}-${width}`);

      // «متاحة الآن»: its cards, and «عرض الكل» to the available list.
      await open('/', language, dark, width);
      await d.until(`document.querySelectorAll('main a[href^="/spaces/"]').length > 0`, 'available cards');
      log(tag, 'available h2:', await d.text(`document.querySelector('main section h2')`), 'view all:', await d.evaluate(`[...document.querySelectorAll('main section a')].find((a) => /عرض الكل|View all/.test(a.textContent))?.getAttribute('href')`));
      await d.shot(`4-home-available-${tag}-${width}`);

      // Near me: a point in Gaza City at 30 m.
      requests.length = 0;
      await b.send('Browser.grantPermissions', { permissions: ['geolocation'], origin: 'http://localhost:5320' });
      await b.send('Emulation.setGeolocationOverride', { latitude: 31.5148, longitude: 34.4521, accuracy: 30 });
      await d.click(byText('main button', language === 'ar' ? 'الأقرب إليّ' : 'Nearest to me'), 'near me');
      await d.until(`/المساحات الأقرب إليك|Spaces nearest you/.test(document.querySelector('main section h2')?.textContent ?? '')`, 'nearest title');
      await d.sleep(1500);
      log(tag, 'nearest h2:', await d.text(`document.querySelector('main section h2')`));
      log(tag, 'status line:', (await d.text(`document.querySelector('main section [role=status]')`))?.replace(/\n/g, ' '));
      log(tag, 'first distances:', await d.evaluate(`[...document.querySelectorAll('main a[href^="/spaces/"]')].slice(0, 3).map((a) => (a.textContent.match(/(على بعد|away)[^ ]*.{0,14}/) ?? [''])[0]).join(' | ')`));
      const near = requests.filter((r) => r.near !== null);
      log(tag, 'near requests:', JSON.stringify(near.map((r) => ({ url: r.url.replace('http://localhost:5320', ''), near: r.near }))));
      log(tag, 'urls with a coordinate:', requests.filter((r) => /31\.5|34\.4/.test(r.url)).length);
      await d.shot(`4-home-nearest-${tag}-${width}`);
      const homeOrder = await d.evaluate(`[...document.querySelectorAll('main a[href^="/spaces/"]')].map((a) => a.getAttribute('href')).join(' ')`);
      await d.click(`[...document.querySelectorAll('main section a')].find((a) => /عرض الكل|View all/.test(a.textContent))`, 'view all');
      await d.until(`location.pathname === '/spaces' && document.querySelectorAll('main a[href^="/spaces/"]').length > 0`, 'directory list');
      await d.sleep(1500);
      const listOrder = await d.evaluate(`[...document.querySelectorAll('main a[href^="/spaces/"]')].map((a) => a.getAttribute('href')).slice(0, 6).join(' ')`);
      log(tag, 'view all →', await d.evaluate('location.pathname + location.search'), 'same first six:', homeOrder === listOrder);
      log(tag, 'home order:', homeOrder);
      log(tag, 'list order:', listOrder);
      await d.shot(`4-home-viewall-nearest-${tag}-${width}`);
      await b.send('Emulation.clearGeolocationOverride');

      // «تصفّح حسب المنطقة».
      await open('/', language, dark, width);
      await d.until(`document.querySelectorAll('main a[href^="/spaces?area="]').length > 0`, 'area cards');
      await d.evaluate(`[...document.querySelectorAll('main h2')].find((h) => /تصفّح حسب المنطقة|Browse by area/.test(h.textContent)).scrollIntoView({ block: 'start' })`);
      await d.sleep(500);
      await d.shot(`4-home-areas-${tag}-${width}`);
      const firstArea = await d.evaluate(`document.querySelector('main a[href^="/spaces?area="]').getAttribute('href')`);
      await d.click(`document.querySelector('main a[href^="/spaces?area="]')`, 'first area');
      await d.until(`location.pathname === '/spaces'`, 'area → directory');
      await d.sleep(1500);
      log(tag, 'area card', firstArea, '→', await d.evaluate('location.pathname + location.search'), 'count line:', await d.text(`document.querySelector('main p[aria-live]')`));

      // The owners' card → About's #owners.
      await open('/', language, dark, width);
      await d.click(`[...document.querySelectorAll('main a')].find((a) => a.getAttribute('href') === '/about#owners')`, 'owners card');
      await d.until(`location.pathname === '/about' && !!document.getElementById('owners')`, 'about#owners');
      await d.sleep(1200);
      log(tag, 'owners →', await d.evaluate('location.pathname + location.hash'), 'scrollY', await d.evaluate('Math.round(scrollY)'), 'owners top', await d.evaluate(`Math.round(document.getElementById('owners').getBoundingClientRect().top)`));
      await d.shot(`4-home-owners-to-about-${tag}-${width}`);

      // The footer: «تصفّح المساحات» first; its «تواصل معنا» → About's #contact from another page.
      await open('/spaces', language, dark, width);
      log(tag, 'footer links:', await d.evaluate(`[...document.querySelectorAll('footer a')].map((a) => a.textContent + ' ' + a.getAttribute('href')).join(' | ')`));
      await d.evaluate(`document.querySelector('footer').scrollIntoView({ block: 'end' })`);
      await d.sleep(400);
      await d.shot(`4-footer-${tag}-${width}`);
      await d.click(`[...document.querySelectorAll('footer a')].find((a) => a.getAttribute('href') === '/about#contact')`, 'footer contact');
      await d.until(`location.pathname === '/about' && !!document.getElementById('contact')`, 'about#contact');
      await d.sleep(1200);
      log(tag, 'footer contact →', await d.evaluate('location.pathname + location.hash'), 'scrollY', await d.evaluate('Math.round(scrollY)'), 'contact top', await d.evaluate(`Math.round(document.getElementById('contact').getBoundingClientRect().top)`));
      await d.shot(`4-about-contact-from-footer-${tag}-${width}`);
    }
  }

  if (part === 'about' || part === 'none') {
    for (const [language, dark, tag, width] of [
      ['ar', false, 'ar-light', 390],
      ['en', true, 'en-dark', 1440],
    ]) {
      await open('/about', language, dark, width);
      const sections = await d.evaluate(`[...document.querySelectorAll('main section[id]')].map((s) => s.id + ': ' + [...s.querySelectorAll('a')].map((a) => a.textContent.trim() + ' ' + a.getAttribute('href')).join(', ')).join(' | ')`);
      log(tag, part, 'anchored sections:', sections);
      log(tag, 'university line:', await d.evaluate(`/universit|جامعة/i.test(document.querySelector('main').textContent)`));
      if (part === 'about') {
        await d.evaluate(`[...document.querySelectorAll('main h2')].find((h) => /ماذا تعني الحالة|What does the status mean/.test(h.textContent)).scrollIntoView({ block: 'start' })`);
        await d.sleep(400);
        log(tag, 'legend:', (await d.text(`document.querySelector('main dl')`))?.replace(/\n/g, ' / '));
        await d.shot(`4-about-legend-${tag}-${width}`);
      }
      await d.evaluate(`document.getElementById('contact').scrollIntoView({ block: 'start' })`);
      await d.sleep(400);
      await d.shot(`4-about-contact-${part === 'none' ? 'none' : 'email'}-${tag}-${width}`);
      // From Home's owners' card, as the about part checks the anchors too.
      if (part === 'about') {
        await open('/', language, dark, width);
        await d.click(`[...document.querySelectorAll('main a')].find((a) => a.getAttribute('href') === '/about#owners')`, 'owners card');
        await d.until(`location.pathname === '/about' && !!document.getElementById('owners')`, 'about#owners');
        await d.sleep(1200);
        log(tag, 'home owners → about: scrollY', await d.evaluate('Math.round(scrollY)'), 'owners top', await d.evaluate(`Math.round(document.getElementById('owners').getBoundingClientRect().top)`));
      }
    }
  }

  if (part === 'offline') {
    for (const [language, dark, tag, width] of [
      ['ar', false, 'ar-light', 390],
      ['en', true, 'en-dark', 1440],
    ]) {
      // Home loaded; then offline, and a page whose code has not arrived yet.
      await open('/', language, dark, width);
      await b.send('Network.emulateNetworkConditions', { offline: true, latency: 0, downloadThroughput: -1, uploadThroughput: -1 });
      await d.sleep(300);
      log(tag, 'navigator.onLine:', await d.evaluate('navigator.onLine'));
      await d.evaluate(`[...document.querySelectorAll('a')].find((a) => a.getAttribute('href') === '/about').click()`);
      await d.until(`/لا يوجد اتصال بالإنترنت|No internet connection/.test(document.querySelector('main h1')?.textContent ?? '')`, 'offline state');
      await d.sleep(500);
      log(tag, 'offline h1:', await d.text(`document.querySelector('main h1')`), 'icon:', await d.evaluate(`document.querySelector('main svg')?.getAttribute('class')`));
      log(tag, 'buttons and links:', await d.evaluate(`[...document.querySelectorAll('main button, main a')].map((el) => el.textContent).join(' | ')`));
      await d.shot(`4-offline-${tag}-${width}`);
      await d.click(byText('main button', 'إعادة المحاولة|Try again'), 'retry');
      await d.sleep(500);
      log(tag, 'after retry, still on', await d.evaluate('location.pathname'), 'status:', await d.text(`document.querySelector('main [role=status]')`), 'button disabled:', await d.evaluate(`!!document.querySelector('main button')?.disabled`));
      await d.shot(`4-offline-still-${tag}-${width}`);
      // «الرئيسية»: Home's code has arrived already, so it leads home; then back online.
      await d.click(`[...document.querySelectorAll('main a')].find((a) => a.getAttribute('href') === '/')`, 'home link');
      await d.until(`location.pathname === '/' && !!document.querySelector('form[role=search]')`, 'home again');
      await b.send('Network.emulateNetworkConditions', { offline: false, latency: 0, downloadThroughput: -1, uploadThroughput: -1 });
      await d.sleep(1500);
      log(tag, 'home again:', await d.text(`document.querySelector('main h1')`), 'cards:', await d.evaluate(`document.querySelectorAll('main a[href^="/spaces/"]').length`));
      await d.shot(`4-offline-home-again-${tag}-${width}`);
      // The connection coming back retries by itself: offline on a page not yet loaded, then online.
      await open('/', language, dark, width);
      await b.send('Network.emulateNetworkConditions', { offline: true, latency: 0, downloadThroughput: -1, uploadThroughput: -1 });
      await d.evaluate(`[...document.querySelectorAll('a')].find((a) => a.getAttribute('href') === '/about').click()`);
      await d.until(`/لا يوجد اتصال بالإنترنت|No internet connection/.test(document.querySelector('main h1')?.textContent ?? '')`, 'offline again');
      await b.send('Network.emulateNetworkConditions', { offline: false, latency: 0, downloadThroughput: -1, uploadThroughput: -1 });
      await d.until(`location.pathname === '/about' && /عن مساحة|About Masaha/.test(document.querySelector('main h1')?.textContent ?? '')`, 'about after reconnect', 20000);
      log(tag, 'online again → reloaded into', await d.evaluate('location.pathname'), await d.text(`document.querySelector('main h1')`));
    }
  }

  log('page errors:', JSON.stringify(b.errors));
} catch (error) {
  log('FAILED:', error.message);
  await d.shot(`4-failure-${part}`).catch(() => undefined);
  process.exitCode = 1;
} finally {
  writeFileSync(`C:/dev/masaha/workspace/WORKER_A/PUBLIC/scripts/run4-${part}-requests.json`, JSON.stringify(requests, null, 1));
  b.chrome.kill();
}
