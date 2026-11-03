// PUBLIC PR 3a's real run: the space's page and the carried items, in local headless Chrome over CDP.
// Reads only: GETs through the app, no sign-in, no write. Usage: node run3a.mjs <case>
import { byLabel, byText, driver, launch } from './cdp3a.mjs';

const which = process.argv[2];
const b = await launch();
const d = driver(b);
const api = [];
b.on((m) => {
  if (m.method === 'Network.requestWillBeSent' && m.params.request.url.includes('/api/v1/')) {
    const near = m.params.request.headers['Masaha-Near'];
    api.push(m.params.request.url.replace('http://localhost:5320', '') + (near ? `  [Masaha-Near ${near}]` : ''));
  }
});
await b.send('Network.enable');

const VARIANTS = { 'ar-light': ['ar', 'light'], 'en-dark': ['en', 'dark'] };

async function open(path, variant, width) {
  const [language, theme] = VARIANTS[variant];
  await d.viewport(width, 900);
  await d.theme(theme === 'dark');
  await d.go('/');
  await d.prefs(language, theme);
  await d.go(path);
}

/** What a space's page shows, read from the DOM. */
const pageFacts = () =>
  d.evaluate(`(() => {
    const strip = (t) => (t ?? '').replace(/[\\u2066-\\u2069]/g, '').trim();
    const main = document.querySelector('main');
    const sections = [...main.querySelectorAll('section[aria-labelledby]')].map((s) => strip(document.getElementById(s.getAttribute('aria-labelledby'))?.textContent));
    const aside = main.querySelector('aside');
    const bar = document.querySelector('[role=region][aria-label]:is(.fixed)');
    const today = main.querySelector('[aria-current=date]');
    const crumb = main.querySelector('nav[aria-label]');
    const back = [...main.querySelectorAll('a')].find((a) => /العودة إلى المساحات|Back to spaces/.test(a.textContent));
    const pin = main.querySelector('[role=img].map-pin');
    const directions = [...main.querySelectorAll('a')].find((a) => /الاتجاهات|Directions/.test(a.textContent));
    const h2 = [...main.querySelectorAll('h2')].map((h) => strip(h.textContent));
    return {
      title: document.title,
      h1: [...main.querySelectorAll('h1')].map((h) => strip(h.textContent)),
      h2,
      sections,
      aside: aside ? aside.getAttribute('aria-label') : null,
      bar: bar ? strip(bar.innerText).replace(/\\n/g, ' | ') : null,
      today: today ? strip(today.innerText).replace(/\\s+/g, ' ') : null,
      crumb: crumb ? strip(crumb.innerText).replace(/\\s+/g, ' ') + ' -> ' + [...crumb.querySelectorAll('a')].map((a) => a.getAttribute('href')).join(' ') : null,
      back: back ? back.getAttribute('href') : null,
      pin: pin ? pin.getAttribute('aria-label') + ' tabindex=' + pin.getAttribute('tabindex') : null,
      directions: directions ? directions.getAttribute('href') + ' target=' + directions.getAttribute('target') : null,
      tabs: [...main.querySelectorAll('[role=tab]')].map((t) => strip(t.textContent)),
      stale: [...main.querySelectorAll('[data-slot=badge]')].map((x) => strip(x.textContent)),
      contacts: [...main.querySelectorAll('a[href^="tel:"], a[href^="https://wa.me"], a[href^="mailto:"], a[href^="https://www.instagram"]')].map((a) => strip(a.innerText).replace(/\\s+/g, ' ') + ' => ' + a.getAttribute('href')).slice(0, 8),
      padFoot: getComputedStyle(main.querySelector('h1').closest('.flex-col').parentElement).paddingBottom,
    };
  })()`);

const waitPage = () => d.until(`!!document.querySelector('main h1')`, 'the page h1', 20000);

try {
  if (which === 'verified') {
    // The order at each width, both variants; the breadcrumb, the back link and the bar.
    for (const variant of ['ar-light', 'en-dark']) {
      for (const width of [390, 768, 1440]) {
        await open('/spaces?q=Noor', variant, width);
        await d.until(`!!document.querySelector('a[href="/spaces/noor-hub"]')`, 'the card');
        await d.click(`document.querySelector('a[href="/spaces/noor-hub"]')`, 'the card');
        await waitPage();
        await d.until(`!!document.querySelector('main [role=img].map-pin')`, 'the map pin', 20000);
        await d.sleep(1500);
        console.log(variant, width, JSON.stringify(await pageFacts(), null, 1));
        const height = await d.evaluate('document.documentElement.scrollHeight');
        await d.shot(`3a-verified-${variant}-${width}`, Math.min(height, 6000));
      }
    }
  } else if (which === 'hours') {
    // «عرض كل الأيام» on a space whose grouped rows are more than two.
    for (const [variant, width] of [['ar-light', 390], ['en-dark', 1440]]) {
      for (const slug of ['masaha-demo', 'deir-al-balah-campus', 'noor-hub', 'hours-hub']) {
        await open(`/spaces/${slug}`, variant, width);
        await waitPage();
        const toggle = await d.evaluate(`!!${byText('main button', 'عرض كل الأيام|Show all days')}`);
        if (!toggle) continue;
        const rows = () => d.evaluate(`[...document.querySelectorAll('main table tbody tr')].map((r) => r.innerText.replace(/[\\u2066-\\u2069]/g, '').replace(/\\s+/g, ' ')).join(' / ')`);
        console.log(variant, width, slug, 'grouped:', await rows());
        await d.evaluate(`${byText('main button', 'عرض كل الأيام|Show all days')}.scrollIntoView({ block: 'center' })`);
        await d.shot(`3a-hours-${variant}-${width}`);
        await d.click(byText('main button', 'عرض كل الأيام|Show all days'), 'show all');
        console.log(variant, width, slug, 'all:', await rows(), 'expanded:', await d.evaluate(`${byText('main button', 'عرض مختصر|Show less')}?.getAttribute('aria-expanded')`));
        await d.shot(`3a-hours-all-${variant}-${width}`);
        break;
      }
    }
  } else if (which === 'unverified') {
    // The notice and its dialog; the contact as the web's .env holds it (the caller sets it).
    const label = process.argv[3];
    for (const [variant, width] of [['ar-light', 390], ['en-dark', 1440]]) {
      await open('/spaces/tuffah-place', variant, width);
      await waitPage();
      console.log(variant, width, JSON.stringify(await pageFacts(), null, 1));
      const notice = await d.text(`document.querySelector('main [data-slot=alert]')`);
      const hidden = await d.text(`[...document.querySelectorAll('main p')].find((p) => /لا نعرض الأسعار|We don’t show/.test(p.textContent))`);
      console.log('notice:', notice?.replace(/\n/g, ' | '), '\nhidden prices:', hidden);
      if (label === 'email') await d.shot(`3a-unverified-${variant}-${width}`, Math.min(await d.evaluate('document.documentElement.scrollHeight'), 5000));
      await d.click(byText('main button', 'تواصل معنا|Contact us'), 'contact us');
      await d.until(`!!document.querySelector('[role=dialog]')`, 'the dialog');
      await d.sleep(400);
      const dialog = await d.evaluate(`(() => { const x = document.querySelector('[role=dialog]'); return { text: x.innerText.replace(/[\\u2066-\\u2069]/g, '').replace(/\\n/g, ' | '), links: [...x.querySelectorAll('a')].map((a) => a.getAttribute('href') + ' target=' + a.getAttribute('target')) }; })()`);
      console.log('dialog:', JSON.stringify(dialog));
      await d.viewport(width, 900);
      await d.shot(`3a-dialog-${label}-${variant}-${width}`);
    }
  } else if (which === 'stale') {
    for (const [variant, width] of [['ar-light', 390], ['en-dark', 1440]]) {
      await open('/spaces/sabra-lab', variant, width);
      await waitPage();
      const facts = await pageFacts();
      console.log(variant, width, 'badges:', facts.stale, 'sections:', facts.sections);
      const check = await d.text(`document.querySelector('main section [data-slot=alert]')`);
      console.log('check line:', check);
      await d.evaluate(`[...document.querySelectorAll('main [data-slot=badge]')].find((x) => /قد يكون|May have/.test(x.textContent))?.scrollIntoView({ block: 'center' })`);
      await d.shot(`3a-stale-${variant}-${width}`);
    }
  } else if (which === 'unknown') {
    for (const [variant, width] of [['ar-light', 390], ['en-dark', 1440]]) {
      await open('/spaces/no-such-space', variant, width);
      await waitPage();
      const text = await d.text(`document.querySelector('main')`);
      const link = await d.evaluate(`${byText('main a', 'تصفّح المساحات|Browse spaces')}?.getAttribute('href')`);
      console.log(variant, width, 'main:', text.replace(/\n/g, ' | '), 'browse ->', link, 'title:', await d.evaluate('document.title'));
      await d.shot(`3a-unknown-${variant}-${width}`);
    }
  } else if (which === 'carried') {
    // The carried items a browser shows, ar light 390 and en dark 1440 (768 for the picking card).
    await b.send('Browser.resetPermissions');
    for (const [variant, width] of [['ar-light', 390], ['en-dark', 1440], ['ar-light', 768]]) {
      const tag = `${variant}-${width}`;
      // 5: the pins' first load, on a slow connection.
      await open('/spaces', variant, width);
      // The map's code first, then the pins held back 8 s, as on a weak connection.
      await d.go('/spaces?view=map');
      await d.until(`document.querySelectorAll('.map-mark').length > 0`, 'the pins (warm-up)', 30000);
      await d.go('/');
      await b.send('Fetch.enable', { patterns: [{ urlPattern: '*/api/v1/map/spaces*' }] });
      const held = (m) => {
        if (m.method === 'Fetch.requestPaused') setTimeout(() => { b.send('Fetch.continueRequest', { requestId: m.params.requestId }).catch(() => undefined); }, 8000);
      };
      b.on(held);
      await d.go('/spaces?view=map');
      await d.until(`!!${byText('p', 'جارٍ تحميل المساحات|Loading spaces')}`, 'the loading line', 20000);
      console.log(tag, 'loading line, busy:', await d.evaluate(`document.querySelector('section[aria-busy]')?.getAttribute('aria-busy')`));
      await d.shot(`3a-carried-loading-${tag}`);
      await d.until(`document.querySelectorAll('.map-mark').length > 0`, 'the pins after the hold', 30000);
      await b.send('Fetch.disable');
      await d.until(`document.querySelectorAll('.map-mark').length > 0`, 'the pins', 30000);
      await d.until(`!${byText('p', 'جارٍ تحميل المساحات|Loading spaces')}`, 'the loading line gone', 20000);

      // 1: the pick ends with the map. Denied → set on the map → placed → change → «قائمة» → «خريطة».
      await d.click(byText('button', 'الأقرب إليّ|Nearest to me'), 'near me');
      await d.until(`!!${byText('button', 'حدّد موقعي على الخريطة|Set my location on the map')}`, 'denied line', 25000);
      await d.click(byText('button', 'حدّد موقعي على الخريطة|Set my location on the map'), 'pick on map');
      await d.until(`!!document.querySelector('.map-crosshair')`, 'the crosshair');
      await d.sleep(800);
      console.log(tag, 'crosshair after StrictMode mount:', await d.evaluate(`!!document.querySelector('.map-crosshair')`));
      if (width === 768) {
        // 6: the picking card under the map at 768.
        const under = await d.evaluate(`(() => { const card = ${byText('[role=region]', 'حدّد موقعك على الخريطة|Set your location on the map')}; const map = document.querySelector('[role=application]'); return { inOverlay: !!card?.closest('.absolute'), after: !!(map.compareDocumentPosition(card) & 4) }; })()`);
        console.log(tag, 'picking card:', JSON.stringify(under));
        await d.evaluate(`document.querySelector('[role=application]').scrollIntoView({ block: 'start' })`);
        await d.shot(`3a-carried-pickunder-${tag}`, 1200);
        await d.viewport(width, 900);
      }
      await d.click(byText('button', 'ثبّت الموقع هنا|Set location here'), 'place');
      await d.until(`!!${byText('button', 'تغيير الموقع|Change location')}`, 'pin line');
      // 4: the map's own near-me line.
      const mapLine = await d.text(`document.querySelector('[role=status]')`);
      console.log(tag, 'map line:', mapLine?.replace(/\n/g, ' | '));
      await d.shot(`3a-carried-mapline-${tag}`);
      await d.click(byText('button', 'تغيير الموقع|Change location'), 'change');
      await d.until(`!!document.querySelector('.map-crosshair')`, 'crosshair again');
      await d.click(byText('[role=radio]', '^(قائمة|List)$'), 'list');
      await d.until(`!!${byText('p', 'الموقع الذي حدّدته|the point you set')}`, 'the list pin line', 20000);
      const listLine = await d.text(`[...document.querySelectorAll('[role=status]')].find((s) => /حدّدته|you set/.test(s.textContent))`);
      console.log(tag, 'list after leaving the pick:', listLine?.replace(/\n/g, ' | '), '| sort requests:', api.filter((u) => u.includes('sort=distance')).slice(-1));
      await d.shot(`3a-carried-pickends-list-${tag}`);
      await d.click(byText('[role=radio]', '^(خريطة|Map)$'), 'map');
      await d.until(`!!document.querySelector('[role=application]')`, 'map again', 20000);
      await d.sleep(1000);
      console.log(tag, 'crosshair on reopening:', await d.evaluate(`!!document.querySelector('.map-crosshair')`));
      await d.shot(`3a-carried-pickends-map-${tag}`);
      if (width === 768) continue;

      // 2: the overlay before the pins; 7: Escape; the phone's line.
      await d.click(byText('button', 'مسح موقعي|Clear my location'), 'clear');
      await d.until(`document.querySelectorAll('.map-mark[tabindex="0"]').length > 0`, 'marks tabbable');
      await d.evaluate(`document.querySelector('.map-mark[tabindex="0"]').focus()`);
      await d.enter();
      await d.sleep(800);
      const order = await d.evaluate(`(() => {
        const marks = [...document.querySelectorAll('.map-mark')];
        const details = ${byText('a', 'عرض التفاصيل|View details')};
        const legend = document.querySelector('[aria-label="دليل الخريطة"], [aria-label="Map legend"]');
        const first = marks[0];
        return { detailsBeforePins: !!details && !!(details.compareDocumentPosition(first) & 4), legendBeforePins: !!(legend.compareDocumentPosition(first) & 4), live: [...document.querySelectorAll('section [role=status].sr-only')].map((s) => s.textContent.replace(/[\\u2066-\\u2069]/g, '')).join('') };
      })()`);
      console.log(tag, 'order:', JSON.stringify(order));
      // Tab from the view switch: what comes first inside the map's section.
      await d.evaluate(`document.querySelector('[role=radio][aria-checked=true]').focus()`);
      const seq = [];
      for (let i = 0; i < 8; i += 1) {
        await d.tab();
        seq.push(await d.evaluate(`(() => { const a = document.activeElement; return (a.getAttribute('aria-label') ?? a.textContent).replace(/[\\u2066-\\u2069]/g, '').trim().slice(0, 40); })()`));
      }
      console.log(tag, 'tab order from the view switch:', seq.join(' → '));
      await d.shot(`3a-carried-chosen-${tag}`);
      if (width >= 768) {
        await d.evaluate(`document.querySelector('.map-mark[aria-pressed=true]').focus()`);
        await d.key('Escape', 'Escape', 27);
        console.log(tag, 'Escape on the pin: card gone', await d.evaluate(`!${byText('a', 'عرض التفاصيل|View details')}`), 'focus on pin', await d.evaluate(`document.activeElement.classList.contains('map-mark')`));
        await d.enter();
        await d.sleep(500);
        await d.evaluate(`${byText('a', 'عرض التفاصيل|View details')}.focus()`);
        await d.key('Escape', 'Escape', 27);
        console.log(tag, 'Escape in the card: card gone', await d.evaluate(`!${byText('a', 'عرض التفاصيل|View details')}`), 'focus on pin', await d.evaluate(`document.activeElement.classList.contains('map-mark')`));
        await d.shot(`3a-carried-escape-${tag}`);
      }
    }
  } else if (which === 'breakwidth') {
    await open('/spaces/noor-hub', 'ar-light', 1440);
    await waitPage();
    await d.sleep(1500);
    console.log('main column width:', await d.evaluate(`Math.round(document.querySelector('main h1').closest('.flex-col').parentElement.getBoundingClientRect().width) + ' of ' + Math.round(document.querySelector('main h1').closest('.flex-col').parentElement.parentElement.getBoundingClientRect().width)`));
    await d.shot(`break-main-column`, 1800);
  }
  console.log('API requests:', api.length);
  for (const url of api) console.log('  ', url);
  console.log('page errors:', b.errors.length ? b.errors : 'none');
} catch (error) {
  console.log('FAILED:', error.message);
  process.exitCode = 1;
} finally {
  b.chrome.kill();
}
