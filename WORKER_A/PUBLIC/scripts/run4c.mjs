// PUBLIC PR 4's real run, #108's gaps (0_CARRIED_FROM_108.md item 8), in local headless Chrome over CDP.
// Usage: node run4c.mjs <part> — part: hidden | touch | bottom | gallery | escape.
import { driver, launch } from './cdp4.mjs';

const part = process.argv[2];
const b = await launch();
const d = driver(b);
const DIR = 'carried';
const occupancy = [];
await b.send('Network.enable');
const started = Date.now();
b.on((m) => {
  if (m.method === 'Network.requestWillBeSent' && m.params.request.url.endsWith('/occupancy'))
    occupancy.push(Math.round((Date.now() - started) / 1000));
});
const log = (...line) => console.log(...line);

async function open(path, language, dark, width) {
  await d.viewport(width);
  await d.go('/');
  await d.prefs(language, dark ? 'dark' : 'light');
  await d.theme(dark);
  await d.go(path);
  await d.until(`document.documentElement.lang === ${JSON.stringify(language)}`, 'language');
  await d.until(`!!document.querySelector('main h1')`, 'h1');
  await d.sleep(1500);
}

try {
  if (part === 'hidden') {
    // The status kept while the tab is hidden, then read again at once on return.
    await open('/spaces/noor-hub', 'en', true, 1440);
    await d.until(`/Available|Full|Closed now/.test(document.querySelector('main').innerText)`, 'live badge');
    log('reads after arrival (s):', JSON.stringify(occupancy));
    await d.shotIn(DIR, '4c-hidden-before-en-dark-1440');
    const { targetId } = await b.send('Target.createTarget', { url: 'about:blank' });
    await d.sleep(500);
    log('state after a second tab:', await d.evaluate('document.visibilityState'));
    const hiddenAt = occupancy.length;
    await d.sleep(75_000);
    log('reads while hidden 75 s:', occupancy.length - hiddenAt, JSON.stringify(occupancy));
    const targets = await b.send('Target.getTargets');
    const first = targets.targetInfos.find((t) => t.type === 'page' && t.targetId !== targetId);
    await b.send('Target.activateTarget', { targetId: first.targetId });
    await d.sleep(2000);
    log('state on return:', await d.evaluate('document.visibilityState'), 'reads (s):', JSON.stringify(occupancy));
    log('badge kept:', await d.evaluate(`/Available|Full|Closed now/.test(document.querySelector('main').innerText)`));
    await d.shotIn(DIR, '4c-hidden-after-return-en-dark-1440');
  }

  if (part === 'touch') {
    // A finger scroll over the place map at 390 moves the page.
    await b.send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 1 });
    await open('/spaces/noor-hub', 'ar', false, 390);
    await d.until(`!!document.querySelector('.leaflet-container')`, 'place map');
    await d.evaluate(`document.querySelector('.leaflet-container').scrollIntoView({ block: 'center' })`);
    await d.sleep(800);
    const box = await d.evaluate(`(() => { const r = document.querySelector('.leaflet-container').getBoundingClientRect(); return { x: Math.round(r.left + r.width / 2), y: Math.round(r.top + r.height / 2) }; })()`);
    const pane = `document.querySelector('.leaflet-map-pane').style.transform`;
    const before = { y: await d.evaluate('Math.round(scrollY)'), pane: await d.evaluate(pane) };
    await d.shotIn(DIR, '4c-touch-before-ar-light-390');
    await b.send('Input.synthesizeScrollGesture', { x: box.x, y: box.y, yDistance: -300, gestureSourceType: 'touch', speed: 800 });
    await d.sleep(1200);
    const after = { y: await d.evaluate('Math.round(scrollY)'), pane: await d.evaluate(pane) };
    log('finger at', JSON.stringify(box), 'scrollY', before.y, '→', after.y, '; map pane', before.pane, '→', after.pane);
    await d.shotIn(DIR, '4c-touch-after-ar-light-390');
    // The control: the same finger over the page's heading, away from the map.
    await d.evaluate('window.scrollTo(0, 0)');
    await d.sleep(500);
    const head = await d.evaluate(`(() => { const r = document.querySelector('main h1').getBoundingClientRect(); return { x: Math.round(r.left + r.width / 2), y: Math.round(r.top + r.height / 2) }; })()`);
    await b.send('Input.synthesizeScrollGesture', { x: head.x, y: head.y + 200, yDistance: -300, gestureSourceType: 'touch', speed: 800 });
    await d.sleep(1200);
    log('control over the page at', JSON.stringify(head), 'scrollY 0 →', await d.evaluate('Math.round(scrollY)'));
    // Touch events by hand over the map: a finger down, moving up 300 px, lifted.
    await d.evaluate(`document.querySelector('.leaflet-container').scrollIntoView({ block: 'center' })`);
    await d.sleep(600);
    const m = await d.evaluate(`(() => { const r = document.querySelector('.leaflet-container').getBoundingClientRect(); return { x: Math.round(r.left + r.width / 2), y: Math.round(r.top + r.height / 2), top: Math.round(r.top) }; })()`);
    const y0 = await d.evaluate('Math.round(scrollY)');
    await b.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: m.x, y: m.y + 100 }] });
    for (let step = 1; step <= 10; step += 1) {
      await b.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: m.x, y: m.y + 100 - step * 20 }] });
      await d.sleep(16);
    }
    await b.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
    await d.sleep(1200);
    log('touch events over the map at', JSON.stringify(m), 'scrollY', y0, '→', await d.evaluate('Math.round(scrollY)'), '; map pane', await d.evaluate(pane));
    await d.shotIn(DIR, '4c-touch-events-after-ar-light-390');
  }

  if (part === 'bottom') {
    // The page's foot at 390: with the bar the footer stays above it; without one, no blank band.
    for (const [slug, name] of [
      ['noor-hub', 'with-bar'],
      ['white-space', 'no-bar'],
    ]) {
      await open(`/spaces/${slug}`, 'ar', false, 390);
      await d.evaluate('window.scrollTo(0, document.documentElement.scrollHeight)');
      await d.sleep(800);
      const facts = await d.evaluate(`(() => {
        const bar = document.querySelector('[role=region][aria-label="التواصل السريع"]');
        const footer = document.querySelector('footer');
        const links = [...footer.querySelectorAll('a')];
        const lastLink = links[links.length - 1].getBoundingClientRect();
        return {
          bar: bar ? Math.round(bar.getBoundingClientRect().top) : null,
          lastFooterLinkBottom: Math.round(lastLink.bottom),
          footerPaddingBottom: getComputedStyle(footer).paddingBottom,
          footerBottom: Math.round(footer.getBoundingClientRect().bottom),
          viewport: innerHeight,
        };
      })()`);
      log(name, slug, JSON.stringify(facts));
      await d.shotIn(DIR, `4c-bottom-${name}-ar-light-390`);
    }
  }

  if (part === 'gallery') {
    for (const [language, dark, tag] of [
      ['ar', false, 'ar-light'],
      ['en', true, 'en-dark'],
    ]) {
      for (const width of [390, 768, 1440]) {
        await open('/spaces/masaha-demo', language, dark, width);
        await d.until(`document.querySelectorAll('main button img').length > 0`, 'gallery');
        const shown = await d.evaluate(`[...document.querySelectorAll('main button')].filter((el) => el.querySelector('img') && el.offsetParent !== null).length`);
        log(tag, width, 'tiles shown:', shown, 'pill:', await d.evaluate(`[...document.querySelectorAll('main button span')].map((s) => s.textContent).find((t) => /عرض كل الصور|View all photos/.test(t)) ?? null`));
        await d.evaluate(`document.querySelector('main button img').scrollIntoView({ block: 'center' })`);
        await d.sleep(500);
        await d.shotIn(DIR, `4c-gallery-${tag}-${width}`);
      }
    }
  }

  if (part === 'escape') {
    // After Escape closes the viewer, the focus is back on the tile that opened it.
    for (const [language, dark, tag, width, tile] of [
      ['ar', false, 'ar-light', 390, 1],
      ['en', true, 'en-dark', 1440, 3],
    ]) {
      await open('/spaces/masaha-demo', language, dark, width);
      await d.until(`document.querySelectorAll('main button img').length > 0`, 'gallery');
      const label = language === 'ar' ? `عرض الصورة ${tile}` : `View photo ${tile}`;
      await d.evaluate(`(() => { const el = [...document.querySelectorAll('main button')].find((b) => b.getAttribute('aria-label') === ${JSON.stringify(label)}); el.focus(); return true; })()`);
      await d.enter();
      await d.until(`!!document.querySelector('[role=dialog]')`, 'viewer');
      log(tag, 'viewer position:', await d.text(`document.querySelector('[role=dialog] p[dir=ltr]')`));
      await d.shotIn(DIR, `4c-viewer-${tag}-${width}`);
      await d.key('Escape', 'Escape', 27);
      await d.sleep(500);
      log(tag, 'dialog closed:', await d.evaluate(`!document.querySelector('[role=dialog]')`), 'focus on:', await d.evaluate(`document.activeElement?.getAttribute('aria-label')`), '(opened from', label + ')');
      await d.shotIn(DIR, `4c-viewer-closed-focus-${tag}-${width}`);
    }
  }
  log('page errors:', JSON.stringify(b.errors));
} catch (error) {
  log('FAILED:', error.message);
  await d.shotIn(DIR, `4c-failure-${part}`).catch(() => undefined);
  process.exitCode = 1;
} finally {
  b.chrome.kill();
}
