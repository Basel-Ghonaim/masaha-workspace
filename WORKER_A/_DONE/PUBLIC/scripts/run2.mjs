// PR 2's real run: the Directory's map on the real app (web 5320, API 3320, worker A's masaha_dev).
// Reads only: no sign-in, no write. Screenshots to shots\pr2, the network logs beside them.
// Usage: node run2.mjs <case> [ar|en]
import { writeFileSync } from 'node:fs';
import { byText, driver, launch, SHOTS } from './cdp2.mjs';

const [only, onlyLanguage] = process.argv.slice(2);
const log = (...a) => console.log('·', ...a);
const clean = (text) => (text ?? '').replace(/[⁦-⁩]/g, '');
const ORIGIN = 'http://localhost:5320';
const THEME = { ar: 'light', en: 'dark' };
const t = (language, width) => `${language}-${THEME[language]}-${width}`;

async function start({ language, width, height = 900, base = '' }) {
  const b = await launch();
  const d = driver(b);
  const requests = [];
  await b.send('Network.enable');
  b.on((m) => {
    if (m.method === 'Network.requestWillBeSent') {
      const { url, headers } = m.params.request;
      const near = Object.entries(headers).find(([k]) => k.toLowerCase() === 'masaha-near');
      requests.push({ url, near: near ? near[1] : null });
    }
  });
  d.requests = requests;
  d.b = b;
  await d.viewport(width, height);
  await d.theme(THEME[language] === 'dark');
  await d.go(base + '/');
  await d.prefs(language, THEME[language]);
  return { b, d };
}

const W = {
  ar: { map: '^خريطة$', list: '^قائمة$', near: '^الأقرب إليّ$', details: 'عرض التفاصيل', close: 'إغلاق', centre: 'مركّز على موقعي', pickOnMap: 'حدّد موقعي على الخريطة', confirm: 'ثبّت الموقع هنا', back: '^رجوع$', change: 'تغيير الموقع', filters: '^الفلاتر', verified: 'المساحات الموثّقة فقط', stop: 'إيقاف الترتيب', clear: 'مسح موقعي', clearFilters: '^مسح الفلاتر$', show: '^عرض' },
  en: { map: '^Map$', list: '^List$', near: '^Nearest to me$', details: 'View details', close: 'Close', centre: 'Centre on my location', pickOnMap: 'Set my location on the map', confirm: 'Set location here', back: '^Back$', change: 'Change location', filters: '^Filters', verified: 'Verified spaces only', stop: 'Stop sorting', clear: 'Clear my location', clearFilters: '^Clear filters$', show: '^Show' },
};
const ALL = [['ar', 390], ['ar', 768], ['ar', 1440], ['en', 390], ['en', 768], ['en', 1440]];
const PAIRS = [['ar', 390], ['en', 1440]];
const pick = (list) => list.filter(([language]) => !onlyLanguage || language === onlyLanguage);

/** A real mouse press, as a person does (Radix reads pointer events). */
async function press(d, expression, what) {
  const at = await d.evaluate(
    `(() => { const el = ${expression}; if (!el) return null; el.scrollIntoView({ block: 'center' }); const r = el.getBoundingClientRect(); return { x: r.x + r.width / 2, y: r.y + r.height / 2 }; })()`,
  );
  if (at === null) throw new Error(`nothing to press: ${what}`);
  for (const type of ['mouseMoved', 'mousePressed', 'mouseReleased']) {
    await d.b.send('Input.dispatchMouseEvent', { type, x: at.x, y: at.y, button: 'left', clickCount: 1 });
  }
  await d.sleep(700);
}

const MAP = `document.querySelector('[role=application]')`;
const waitMap = (d) => d.until(`document.querySelectorAll('[role=application] .map-mark').length > 0`, 'the pins', 20000);
const mark = (name) => `[...document.querySelectorAll('[role=application] [role=button][aria-label]')].find((el) => el.getAttribute('aria-label').startsWith(${JSON.stringify(name)}))`;
const pane = (d) => d.evaluate(`document.querySelector('.leaflet-map-pane').style.transform`);
const activeName = (d) => d.evaluate(`(() => { const el = document.activeElement; return (el.getAttribute('aria-label') ?? el.textContent ?? el.tagName).trim().slice(0, 60); })()`);
const statusLine = async (d) => clean(await d.text(`document.querySelector('main [role=status]')`));

function saveLog(d, name) {
  writeFileSync(`${SHOTS}/${name}-log.txt`, d.requests.filter((r) => r.url.includes('/api/v1/') || /leaflet|MapLayers|LeafletMarkerMap/i.test(r.url)).map((r) => `${r.url.replace(/^https?:\/\/localhost:\d+/, '')}${r.near ? `  [Masaha-Near: ${r.near}]` : ''}`).join('\n') + '\n');
}

async function selectPin(d, slug) {
  const name = await d.evaluate(`fetch('/api/v1/map/spaces').then((r) => r.json()).then((j) => { const p = j.data.pins.find((x) => x.slug === ${JSON.stringify(slug)}); return document.documentElement.lang === 'en' ? p.nameEn : (p.nameAr ?? p.nameEn); })`);
  const at = mark(name);
  await d.evaluate(`(() => { const el = ${at}; el.focus(); return true; })()`);
  await d.key('Enter', 'Enter', 13);
  await d.sleep(1200);
  return name;
}

const cases = {
  // «خريطة»: the pins by state and the legend, at every width in both languages.
  async pins() {
    for (const [language, width] of pick(ALL)) {
      const { b, d } = await start({ language, width });
      try {
        await d.go('/spaces');
        await d.until(`!!${byText('[role=radio]', W[language].map)}`, 'the view switch');
        await press(d, byText('[role=radio]', W[language].map), 'map');
        await waitMap(d);
        await d.sleep(2500);
        const counts = await d.evaluate(`['filled','bar','hollow','dashed'].map((s) => s + '=' + document.querySelectorAll('[role=application] .map-mark-' + s).length).join(' ')`);
        log(language, width, 'address:', await d.evaluate('location.search'), 'marks:', counts);
        log(language, width, 'legend:', clean(await d.text(`document.querySelector('ul[aria-label]')`)).replace(/\n+/g, ' | '));
        log(language, width, 'FULL pin label:', clean(await d.evaluate(`${mark(language === 'en' ? 'Sada' : 'صدى')}?.getAttribute('aria-label') ?? 'not found'`)));
        await d.shot(`2-pins-${t(language, width)}`);
      } finally {
        b.chrome.kill();
      }
    }
  },

  // A chosen pin: its card at 768 and 1440, its sheet at 390 with the map still panning.
  async select() {
    for (const [language, width] of pick(ALL)) {
      const { b, d } = await start({ language, width });
      try {
        await d.go('/spaces?view=map');
        await waitMap(d);
        await d.sleep(2000);
        const name = await selectPin(d, 'sada-space');
        const dialog = await d.evaluate(`!!document.querySelector('[role=dialog]')`);
        const region = await d.evaluate(`[...document.querySelectorAll('[role=region]')].map((r) => r.innerText.replace(/\\n+/g, ' | ')).join(' // ')`);
        log(language, width, 'chose', name, '— sheet:', dialog, '— focus on:', clean(await activeName(d)));
        log(language, width, dialog ? 'sheet:' : 'card:', clean(dialog ? await d.text(`document.querySelector('[role=dialog]')`) : region).replace(/\n+/g, ' | '));
        await d.shot(`2-select-${t(language, width)}`);
        if (dialog) {
          const before = await pane(d);
          await d.evaluate(`${MAP}.focus(); true`);
          for (let i = 0; i < 3; i += 1) await d.key('ArrowUp', 'ArrowUp', 38);
          await d.sleep(800);
          const after = await pane(d);
          log(language, width, 'sheet open, arrows pan the map:', before !== after, before, '→', after, '— sheet still open:', await d.evaluate(`!!document.querySelector('[role=dialog]')`));
          await d.shot(`2-select-panned-${t(language, width)}`);
        }
        await press(d, `[...document.querySelectorAll('[role=region] button, [role=dialog] button')].find((el) => el.getAttribute('aria-label') === ${JSON.stringify(W[language].close)})`, 'close');
        log(language, width, 'closed — focus on:', clean(await activeName(d)));
      } finally {
        b.chrome.kill();
      }
    }
  },

  // «عرض التفاصيل» leads to the space's page (the site's 404 until PR 3).
  async details() {
    for (const [language, width] of pick(PAIRS)) {
      const { b, d } = await start({ language, width });
      try {
        await d.go('/spaces?view=map');
        await waitMap(d);
        await d.sleep(2000);
        await selectPin(d, 'tal-al-hawa-desks');
        await press(d, byText('a', W[language].details), 'details');
        await d.sleep(1500);
        log(language, width, 'after «عرض التفاصيل»:', await d.evaluate('location.pathname'));
        await d.shot(`2-details-${t(language, width)}`);
      } finally {
        b.chrome.kill();
      }
    }
  },

  // A filter on the map: the sheet at every width, «المساحات الموثّقة فقط».
  async filter() {
    for (const [language, width] of pick(PAIRS)) {
      const { b, d } = await start({ language, width });
      try {
        await d.go('/spaces?view=map');
        await waitMap(d);
        await d.sleep(2000);
        const before = await d.evaluate(`document.querySelectorAll('[role=application] .map-mark').length`);
        await press(d, byText('main button', W[language].filters), 'filters');
        await d.until(`!!document.querySelector('[role=dialog]')`, 'the sheet');
        await press(d, `[...document.querySelectorAll('[role=dialog] [role=switch]')].find((el) => document.querySelector('label[for="' + el.id + '"]')?.textContent.includes(${JSON.stringify(W[language].verified)}))`, 'verified');
        await d.sleep(1500);
        log(language, width, 'sheet primary:', clean(await d.text(byText('[role=dialog] button', W[language].show))));
        await d.shot(`2-filter-sheet-${t(language, width)}`);
        await press(d, byText('[role=dialog] button', W[language].show), 'show');
        await d.sleep(1500);
        const after = await d.evaluate(`document.querySelectorAll('[role=application] .map-mark').length`);
        log(language, width, 'address:', await d.evaluate('location.search'), 'marks before:', before, 'after:', after);
        await d.shot(`2-filter-${t(language, width)}`);
        saveLog(d, `2-filter-${t(language, width)}`);
      } finally {
        b.chrome.kill();
      }
    }
  },

  // «حدّد موقعي على الخريطة» from the denied state → the crosshair → the arrows pan → «ثبّت الموقع هنا»
  // (sorted, «تغيير الموقع»); then «رجوع» from a second pick. The privacy proof in the log.
  async pick() {
    for (const [language, width] of pick(PAIRS)) {
      const { b, d } = await start({ language, width });
      try {
        await b.send('Browser.setPermission', { permission: { name: 'geolocation' }, setting: 'denied', origin: ORIGIN });
        await d.go('/spaces');
        await d.until(`document.querySelectorAll('section[aria-labelledby] a[href^="/spaces/"]').length > 0`, 'cards');
        await d.sleep(1500);
        await d.click(byText('main button', W[language].near), 'near me');
        await d.sleep(2000);
        log(language, width, 'denied — state line:', (await statusLine(d)).replace(/\n+/g, ' | '));
        await d.shot(`2-pick-denied-${t(language, width)}`);
        await press(d, byText('main button', W[language].pickOnMap), 'pick on the map');
        await waitMap(d);
        await d.sleep(2500);
        log(language, width, 'address:', await d.evaluate('location.search'), 'crosshair:', await d.evaluate(`!!document.querySelector('.map-crosshair')`), 'focus on:', clean(await activeName(d)), 'described by:', clean(await d.evaluate(`document.getElementById(${MAP}.getAttribute('aria-describedby'))?.textContent`)));
        log(language, width, 'marks tabbable:', await d.evaluate(`[...document.querySelectorAll('[role=application] .map-mark')].filter((m) => m.tabIndex >= 0).length`), 'near button shown:', await d.evaluate(`!!${byText('main button', W[language].near)}`));
        await d.shot(`2-pick-crosshair-${t(language, width)}`);
        // At the fitted zoom a wide screen already shows the whole box the map is held to: zoom in once
        // with the map's «+», as a person would, then pan with the arrows.
        if (width >= 1024) {
          await press(d, `document.querySelector('.leaflet-control-zoom-in')`, 'zoom in');
          await d.sleep(800);
          await d.evaluate(`${MAP}.focus(); true`);
        }
        const before = await pane(d);
        for (let i = 0; i < 4; i += 1) await d.key(width >= 1024 ? 'ArrowUp' : 'ArrowLeft', width >= 1024 ? 'ArrowUp' : 'ArrowLeft', width >= 1024 ? 38 : 37);
        await d.sleep(800);
        log(language, width, 'arrows pan:', before !== (await pane(d)), before, '→', await pane(d));
        await d.shot(`2-pick-panned-${t(language, width)}`);
        await press(d, byText('[role=region] button', W[language].confirm), 'confirm');
        await d.sleep(1500);
        log(language, width, 'placed — state line:', (await statusLine(d)).replace(/\n+/g, ' | '), '— focus on:', clean(await activeName(d)), '— user point:', clean(await d.evaluate(`document.querySelector('.map-user')?.getAttribute('aria-label') ?? 'none'`)));
        await d.shot(`2-pick-placed-${t(language, width)}`);
        await press(d, byText('[role=radio]', W[language].list), 'list');
        await d.until(`document.querySelectorAll('section[aria-labelledby] a[href^="/spaces/"]').length > 0`, 'cards');
        await d.sleep(2000);
        log(language, width, 'the list, sorted — first cards:', clean(JSON.stringify(await d.evaluate(`[...document.querySelectorAll('section[aria-labelledby] a[href^="/spaces/"]')].slice(0, 3).map((a) => a.innerText.split('\\n').filter((x) => /كم|km/.test(x)).join(''))`))), 'sort:', clean(await d.text(`document.querySelector('main [role=combobox]')`)));
        await d.shot(`2-pick-sorted-list-${t(language, width)}`);
        await press(d, byText('main button', W[language].change), 'change location');
        await waitMap(d);
        await d.sleep(2000);
        await press(d, byText('[role=region] button', W[language].back), 'back');
        await d.sleep(1200);
        log(language, width, 'after «رجوع» — state line:', (await statusLine(d)).replace(/\n+/g, ' | '), '— user point:', clean(await d.evaluate(`document.querySelector('.map-user')?.getAttribute('aria-label') ?? 'none'`)));
        await d.shot(`2-pick-back-${t(language, width)}`);
        saveLog(d, `2-pick-${t(language, width)}`);
        const api = d.requests.filter((r) => r.url.includes('/api/v1/'));
        const withHeader = api.filter((r) => r.near !== null);
        log(language, width, 'PRIVACY: api requests', api.length, 'with header', withHeader.length, 'headers', JSON.stringify(withHeader.map((r) => r.near)), 'all on sort=distance:', withHeader.every((r) => r.url.includes('sort=distance')), 'coordinate in a URL:', api.filter((r) => /3[14]\.\d{2,}/.test(decodeURIComponent(r.url)) && !r.url.includes('bounds=')).length);
      } finally {
        b.chrome.kill();
      }
    }
  },

  // «مركّز على موقعي»: a device location granted on the map, the map moved away, then centred on it.
  async centre() {
    for (const [language, width] of pick(PAIRS)) {
      const { b, d } = await start({ language, width });
      try {
        await b.send('Browser.setPermission', { permission: { name: 'geolocation' }, setting: 'granted', origin: ORIGIN });
        await b.send('Emulation.setGeolocationOverride', { latitude: 31.5017, longitude: 34.4668, accuracy: 30 });
        await d.go('/spaces?view=map');
        await waitMap(d);
        await d.sleep(1500);
        await d.click(byText('main button', W[language].near), 'near me');
        await d.sleep(2000);
        log(language, width, 'granted on the map — state line:', (await statusLine(d)).replace(/\n+/g, ' | '), 'user point:', clean(await d.evaluate(`document.querySelector('.map-user')?.getAttribute('aria-label') ?? 'none'`)));
        const before = await pane(d);
        await press(d, byText('main button', W[language].centre), 'centre');
        await d.sleep(1200);
        log(language, width, '«مركّز على موقعي» moved the map:', before !== (await pane(d)));
        await d.shot(`2-centre-${t(language, width)}`);
      } finally {
        b.chrome.kill();
      }
    }
  },

  // The network log: Leaflet's code and stylesheet only after «خريطة» (the dev server, then the production
  // build on the preview at 5321).
  async leaflet() {
    for (const [base, label] of [['', 'dev'], ['http://localhost:5321', 'build']]) {
      const { b, d } = await start({ language: 'ar', width: 1440, base });
      try {
        await d.go(base + '/spaces');
        await d.sleep(3000);
        const isLeaflet = (r) => /leaflet|MapLayers|LeafletMarkerMap/i.test(r.url);
        const before = d.requests.filter(isLeaflet).map((r) => r.url);
        await press(d, byText('[role=radio]', W.ar.map), 'map');
        await d.until(`!!document.querySelector('.leaflet-container')`, 'Leaflet', 20000);
        await d.sleep(2000);
        const after = d.requests.filter(isLeaflet).map((r) => r.url.replace(/^https?:\/\/localhost:\d+/, ''));
        log(label, 'Leaflet requests before «خريطة»:', before.length, '— after:', after.length, JSON.stringify(after));
        writeFileSync(`${SHOTS}/2-leaflet-${label}-log.txt`, `before «خريطة»: ${before.length}\n${before.join('\n')}\nafter «خريطة»:\n${after.join('\n')}\n`);
        await d.shot(`2-leaflet-${label}`);
      } finally {
        b.chrome.kill();
      }
    }
  },

  // Carried 1: the focus on «الأقرب إليّ» after stop and clear (by keyboard); carried 3: no match's
  // «مسح الفلاتر» keeps the search.
  async carried() {
    for (const [language, width] of pick(PAIRS)) {
      const { b, d } = await start({ language, width });
      try {
        await b.send('Browser.setPermission', { permission: { name: 'geolocation' }, setting: 'granted', origin: ORIGIN });
        await b.send('Emulation.setGeolocationOverride', { latitude: 31.5017, longitude: 34.4668, accuracy: 30 });
        await d.go('/spaces');
        await d.until(`document.querySelectorAll('section[aria-labelledby] a[href^="/spaces/"]').length > 0`, 'cards');
        await d.sleep(1500);
        await d.evaluate(`${byText('main button', W[language].near)}.focus(); true`);
        await d.key('Enter', 'Enter', 13);
        await d.sleep(2500);
        await d.evaluate(`${byText('main button', W[language].stop)}.focus(); true`);
        await d.key('Enter', 'Enter', 13);
        await d.sleep(1000);
        log(language, width, 'after stop — focus on:', clean(await activeName(d)));
        await d.evaluate(`${byText('main button', W[language].clear)}.focus(); true`);
        await d.key('Enter', 'Enter', 13);
        await d.sleep(1000);
        log(language, width, 'after clear — focus on:', clean(await activeName(d)));
        await d.shot(`2-carried-focus-${t(language, width)}`);
        await d.go('/spaces?q=Hub&available=1&friday=1&students=1');
        await d.until(`!!${byText('main button', W[language].clearFilters)}`, 'no match');
        await d.shot(`2-carried-nomatch-${t(language, width)}`);
        await press(d, byText('main button', W[language].clearFilters), 'clear filters');
        await d.sleep(1500);
        log(language, width, 'no match «مسح الفلاتر» → address:', decodeURIComponent(await d.evaluate('location.search')), 'search field:', await d.evaluate(`document.querySelector('main input[type=search]').value`));
        await d.shot(`2-carried-cleared-${t(language, width)}`);
      } finally {
        b.chrome.kill();
      }
    }
  },
};

for (const [name, run] of Object.entries(cases)) {
  if (only && only !== name) continue;
  console.log(`== ${name}`);
  await run();
}
