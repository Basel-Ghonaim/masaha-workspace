// PR 1b's real run: the Directory's filters and near me on the real app (web 5320, API 3320, worker A's
// masaha_dev). Reads only: no sign-in, no write. Screenshots to shots\pr1b, the network logs beside them.
// Usage: node run1b.mjs <case> [ar|en]
import { writeFileSync } from 'node:fs';
import { byText, driver, launch, SHOTS } from './cdp1b.mjs';

const [only, onlyLanguage] = process.argv.slice(2);
const log = (...a) => console.log('·', ...a);
const clean = (text) => (text ?? '').replace(/[⁦-⁩]/g, '');
const ORIGIN = 'http://localhost:5320';

async function start({ language, theme, width, height = 900 }) {
  const b = await launch();
  const d = driver(b);
  const requests = [];
  await b.send('Network.enable');
  b.on((m) => {
    if (m.method === 'Network.requestWillBeSent') {
      const { url, headers } = m.params.request;
      if (url.includes('/api/v1/')) {
        const near = Object.entries(headers).find(([k]) => k.toLowerCase() === 'masaha-near');
        requests.push({ url: url.replace(/^.*\/api\/v1/, ''), near: near ? near[1] : null });
      }
    }
  });
  d.requests = requests;
  d.b = b;
  await d.viewport(width, height);
  await d.theme(theme === 'dark');
  await d.go('/');
  await d.prefs(language, theme);
  return { b, d };
}

const words = {
  ar: {
    filters: 'الفلاتر', near: 'الأقرب إليّ', stop: 'إيقاف الترتيب', clear: 'مسح موقعي',
    choose: 'اختر منطقتك', day: '^يوم$', available: 'متاحة الآن فقط', verified: 'المساحات الموثّقة فقط',
    students: 'أسعار للطلاب', friday: 'مفتوحة يوم الجمعة', areas: ['الرمال', 'النصر'],
  },
  en: {
    filters: 'Filters', near: 'Nearest to me', stop: 'Stop sorting', clear: 'Clear my location',
    choose: 'Choose your area', day: '^Day$', available: 'Available now only', verified: 'Verified spaces only',
    students: 'Student prices', friday: 'Open on Friday', areas: ['Al-Rimal', 'An-Nasr'],
  },
};
const THEME = { ar: 'light', en: 'dark' };
/** Every other case: once in Arabic light at 390, once in English dark at 1440 (§3.4). */
const PAIRS = [
  ['ar', 390],
  ['en', 1440],
].filter(([language]) => !onlyLanguage || language === onlyLanguage);

const search = (d) => d.evaluate('location.search');
const countLine = async (d) => clean(await d.text(`document.querySelector('main p[aria-live]')`));
const cardsShown = (d) =>
  d.evaluate(`document.querySelectorAll('section[aria-labelledby] a[href^="/spaces/"]').length`);
const waitCards = (d) => d.until(`document.querySelectorAll('section[aria-labelledby] a[href^="/spaces/"]').length > 0`, 'cards');
const settle = (d) => d.sleep(1500);

/** A real mouse press on the element `expression` returns, as a person does (Radix reads pointer events). */
async function press(d, expression, what) {
  const at = await d.evaluate(
    `(() => { const el = ${expression}; if (!el) return null; el.scrollIntoView({ block: 'center' }); const r = el.getBoundingClientRect(); return { x: r.x + r.width / 2, y: r.y + r.height / 2 }; })()`,
  );
  if (at === null) throw new Error(`nothing to press: ${what}`);
  for (const type of ['mouseMoved', 'mousePressed', 'mouseReleased']) {
    await d.b.send('Input.dispatchMouseEvent', { type, x: at.x, y: at.y, button: 'left', clickCount: 1 });
  }
  await d.sleep(600);
}

/** The filters' form: the sheet's below 1024 px (opened), else the sidebar's. */
async function openFilters(d, language, width) {
  if (width >= 1024) return `document.querySelector('aside#directory-filters')`;
  await press(d, byText('main button', `^${words[language].filters}`), 'the filters button');
  await d.until(`!!document.querySelector('[role=dialog]')`, 'the sheet');
  return `document.querySelector('[role=dialog]')`;
}
const within = (root, selector, pattern) =>
  `[...(${root})?.querySelectorAll(${JSON.stringify(selector)}) ?? []].find((el) => new RegExp(${JSON.stringify(pattern)}).test(el.textContent.replace(/[\\u2066-\\u2069]/g, '')))`;

async function closeSheet(d, width) {
  if (width >= 1024) return;
  await d.key('Escape', 'Escape', 27);
  await d.sleep(400);
}

function saveLog(d, name) {
  writeFileSync(`${SHOTS}/${name}-log.txt`, d.requests.map((r) => `${r.url}${r.near ? `  [Masaha-Near: ${r.near}]` : ''}`).join('\n') + '\n');
}

/** The privacy proof over a log: no coordinate in a URL; the header only with sort=distance, three decimals at most. */
function privacy(requests) {
  const coordinate = /3[14]\.\d{2,}/;
  const inUrl = requests.filter((r) => coordinate.test(decodeURIComponent(r.url)));
  const headerWithoutDistance = requests.filter((r) => r.near !== null && !/sort=distance/.test(r.url));
  const distanceWithoutHeader = requests.filter((r) => r.near === null && /sort=distance/.test(r.url));
  const tooFine = requests.filter((r) => r.near !== null && !/^-?\d{1,3}(\.\d{1,3})?,-?\d{1,3}(\.\d{1,3})?$/.test(r.near));
  return {
    requests: requests.length,
    withHeader: requests.filter((r) => r.near !== null).length,
    coordinateInUrl: inUrl.length,
    headerWithoutDistance: headerWithoutDistance.length,
    distanceWithoutHeader: distanceWithoutHeader.length,
    moreThanThreeDecimals: tooFine.length,
  };
}

const cases = {
  // The filters' sheet at 390 and 768 (its count, its button), the sidebar at 1440, and the results'
  // grid beside it: Arabic light and English dark at the three widths.
  async layout() {
    for (const language of ['ar', 'en'].filter((l) => !onlyLanguage || l === onlyLanguage)) {
      for (const width of [390, 768, 1440]) {
        const { b, d } = await start({ language, theme: THEME[language], width });
        try {
          await d.go('/spaces?verified=1&students=1');
          await waitCards(d);
          await settle(d);
          const name = `1b-filters-${language}-${THEME[language]}-${width}`;
          if (width < 1024) {
            const button = await d.evaluate(`(() => { const el = ${byText('main button', `^${words[language].filters}`)}; return el ? { text: el.textContent, expanded: el.getAttribute('aria-expanded'), controls: el.getAttribute('aria-controls') } : null; })()`);
            log(language, width, 'filters button:', JSON.stringify(button), 'sidebar:', await d.evaluate(`!!document.querySelector('aside#directory-filters')`));
            await d.shot(`${name}-closed`);
            await openFilters(d, language, width);
            await d.sleep(600);
            const sheet = await d.evaluate(`(() => { const s = document.querySelector('[role=dialog]'); const t = document.querySelector('main button[aria-controls]'); return { title: s.querySelector('h2')?.textContent, buttons: [...s.querySelectorAll('button')].map((x) => x.textContent.trim()).filter(Boolean).slice(-3), expanded: t?.getAttribute('aria-expanded') }; })()`);
            log(language, width, 'sheet:', JSON.stringify(sheet));
            await d.shot(`${name}-sheet`);
          } else {
            const sidebar = await d.evaluate(`(() => { const a = document.querySelector('aside#directory-filters'); return { label: a?.getAttribute('aria-label'), filtersButton: !!${byText('main button', `^${words[language].filters}`)}, columns: getComputedStyle(document.querySelector('section[aria-labelledby] > div.grid')).gridTemplateColumns }; })()`);
            log(language, width, 'sidebar:', JSON.stringify(sidebar));
            const card = await d.evaluate(`(() => { const a = document.querySelector('section[aria-labelledby] a[href^="/spaces/"]'); return { name: a.querySelector('h3').textContent, describedBy: (a.getAttribute('aria-describedby') ?? '').split(' ').map((id) => document.getElementById(id)?.textContent).join(' | ') }; })()`);
            log(language, width, 'first card:', clean(JSON.stringify(card)));
            await d.shot(name, 1700);
          }
          log(language, width, 'count:', await countLine(d));
        } finally {
          b.chrome.kill();
        }
      }
    }
  },

  // The results' grid beside the sidebar from 1024 px, the whole list: both themes, three widths.
  async grid() {
    for (const language of ['ar', 'en'].filter((l) => !onlyLanguage || l === onlyLanguage)) {
      for (const width of [390, 768, 1440]) {
        const { b, d } = await start({ language, theme: THEME[language], width });
        try {
          await d.go('/spaces');
          await waitCards(d);
          await settle(d);
          const columns = await d.evaluate(`getComputedStyle(document.querySelector('section[aria-labelledby] > div.grid')).gridTemplateColumns`);
          log(language, width, 'cards:', await cardsShown(d), 'columns:', columns, 'count:', await countLine(d));
          await d.shot(`1b-grid-${language}-${THEME[language]}-${width}`, { 390: 2400, 768: 2000, 1440: 1700 }[width]);
        } finally {
          b.chrome.kill();
        }
      }
    }
  },

  // The place filter: two areas, the summary.
  async place() {
    for (const [language, width] of PAIRS) {
      const { b, d } = await start({ language, theme: THEME[language], width });
      try {
        await d.go('/spaces');
        await waitCards(d);
        const root = await openFilters(d, language, width);
        await press(d, `${root}.querySelector('[role=combobox]')`, 'the area filter');
        await d.until(`document.querySelectorAll('[role=option]').length > 0`, 'the areas');
        for (const area of words[language].areas) {
          await press(d, byText('[role=option]', `^${area}`), area);
        }
        await d.shot(`1b-place-open-${language}-${THEME[language]}-${width}`);
        await d.key('Escape', 'Escape', 27);
        await d.sleep(1200);
        const trigger = clean(await d.text(`${root}.querySelector('[role=combobox]')`));
        log(language, width, 'summary:', trigger, 'address:', await search(d), 'count:', await countLine(d));
        await d.shot(`1b-place-${language}-${THEME[language]}-${width}`, width < 1024 ? 900 : 1600);
        await closeSheet(d, width);
        log(language, width, 'cards:', await cardsShown(d), 'count after closing:', await countLine(d));
      } finally {
        b.chrome.kill();
      }
    }
  },

  // The budget: a day's price from 10 to 30 shekels; then an inverted range and its line.
  async budget() {
    for (const [language, width] of PAIRS) {
      const { b, d } = await start({ language, theme: THEME[language], width });
      try {
        await d.go('/spaces');
        await waitCards(d);
        const root = await openFilters(d, language, width);
        await d.click(within(root, 'button', words[language].day), 'the day chip');
        const inputs = `${root}.querySelectorAll('input[inputmode=numeric]')`;
        await d.evaluate(`(() => { const [a] = ${inputs}; a.id ||= 'budget-min'; const [, z] = ${inputs}; z.id ||= 'budget-max'; return [a.id, z.id]; })()`);
        const ids = await d.evaluate(`[...${inputs}].map((el) => el.id)`);
        await d.type(`[id="${ids[0]}"]`, '10');
        await d.type(`[id="${ids[1]}"]`, '30');
        await d.until(`location.search.includes('max=30')`, 'the budget in the address');
        await settle(d);
        log(language, width, 'address:', await search(d), 'count:', await countLine(d), 'help:', clean(await d.text(`${root}.querySelector('[role=group] p.text-caption')`)));
        await d.shot(`1b-budget-${language}-${THEME[language]}-${width}`, width < 1024 ? 900 : 1600);
        await d.type(`[id="${ids[0]}"]`, '30');
        await d.type(`[id="${ids[1]}"]`, '10');
        await d.sleep(1500);
        const errors = await d.evaluate(`[...(${root}).querySelectorAll('[id$="-error"]')].map((el) => el.textContent)`);
        log(language, width, 'inverted — address:', await search(d), 'lines:', JSON.stringify(errors));
        await d.shot(`1b-budget-inverted-${language}-${THEME[language]}-${width}`, width < 1024 ? 900 : 1600);
        saveLog(d, `1b-budget-${language}-${THEME[language]}-${width}`);
      } finally {
        b.chrome.kill();
      }
    }
  },

  // Each switch, and «أخرى»'s two chips.
  async switches() {
    for (const [language, width] of PAIRS) {
      for (const [key, label, kind] of [
        ['available', words[language].available, 'switch'],
        ['verified', words[language].verified, 'switch'],
        ['students', words[language].students, 'chip'],
        ['friday', words[language].friday, 'chip'],
      ]) {
        const { b, d } = await start({ language, theme: THEME[language], width });
        try {
          await d.go('/spaces');
          await waitCards(d);
          const root = await openFilters(d, language, width);
          if (kind === 'switch') {
            await d.click(`(() => { const label = ${within(root, 'label', `^${label}`)}; return label && document.getElementById(label.htmlFor); })()`, label);
          } else {
            await d.click(within(root, 'button', `${label}`), label);
          }
          await d.until(`location.search.includes(${JSON.stringify(key + '=1')})`, key);
          await settle(d);
          const state = await d.evaluate(kind === 'switch'
            ? `(() => { const label = ${within(root, 'label', `^${label}`)}; return document.getElementById(label.htmlFor).getAttribute('aria-checked'); })()`
            : `${within(root, 'button', `${label}`)}.getAttribute('aria-pressed')`);
          log(language, width, key, 'address:', await search(d), 'state:', state, 'count:', await countLine(d));
          await d.shot(`1b-${key}-${language}-${THEME[language]}-${width}`, width < 1024 ? 900 : 1600);
          if (width < 1024) {
            const show = await d.evaluate(`[...document.querySelectorAll('[role=dialog] button')].map((x) => x.textContent.trim()).filter(Boolean).slice(-2)`);
            log(language, width, key, 'sheet footer:', clean(JSON.stringify(show)));
          }
        } finally {
          b.chrome.kill();
        }
      }
    }
  },

  // Near me: granted (sorted, distances, the privacy line, stop, clear), denied, imprecise, out of the
  // Strip; «اختر منطقتك»; and the privacy proof in the network log.
  async near() {
    for (const [language, width] of PAIRS) {
      const t = `${language}-${THEME[language]}-${width}`;
      const all = [];
      for (const [kind, position, permission] of [
        ['granted', { latitude: 31.5017, longitude: 34.4668, accuracy: 30 }, 'granted'],
        ['denied', null, 'denied'],
        ['imprecise', { latitude: 31.5017, longitude: 34.4668, accuracy: 5000 }, 'granted'],
        ['outside', { latitude: 30.0444, longitude: 31.2357, accuracy: 20 }, 'granted'],
      ]) {
        const { b, d } = await start({ language, theme: THEME[language], width });
        try {
          await b.send('Browser.setPermission', { permission: { name: 'geolocation' }, setting: permission, origin: ORIGIN });
          if (position) await b.send('Emulation.setGeolocationOverride', position);
          await d.go('/spaces');
          await waitCards(d);
          await settle(d);
          const before = d.requests.length;
          await d.click(byText('main button', `^${words[language].near}$`), 'near me');
          await d.sleep(2500);
          const line = clean(await d.text(`document.querySelector('main p[aria-live]').parentElement.parentElement`));
          log(language, width, kind, 'state line:', line.replace(/\n+/g, ' / '));
          log(language, width, kind, 'pressed:', await d.evaluate(`${byText('main button', `^${words[language].near}$`)}.getAttribute('aria-pressed')`), 'sort:', clean(await d.text(`document.querySelector('main [role=combobox]')`)));
          await d.shot(`1b-near-${kind}-${t}`, width < 1024 ? 1400 : 1300);
          if (kind === 'granted') {
            const distances = await d.evaluate(`[...document.querySelectorAll('section[aria-labelledby] a[href^="/spaces/"]')].slice(0, 4).map((a) => [a.querySelector('h3').textContent, [...a.querySelectorAll('p')].map((p) => p.textContent).join(' | ')])`);
            log(language, width, 'distances:', clean(JSON.stringify(distances)));
            await d.click(byText('main button', words[language].stop), 'stop');
            await settle(d);
            log(language, width, 'stopped — line:', clean(await d.text(`document.querySelector('main p[aria-live]').parentElement.parentElement`)).replace(/\n+/g, ' / '), 'sort:', clean(await d.text(`document.querySelector('main [role=combobox]')`)));
            await d.shot(`1b-near-stopped-${t}`, width < 1024 ? 1400 : 1300);
            await d.click(byText('main button', `^${words[language].near}$`), 'near me again');
            await settle(d);
            log(language, width, 'again — pressed:', await d.evaluate(`${byText('main button', `^${words[language].near}$`)}.getAttribute('aria-pressed')`));
            const atClear = d.requests.length;
            await d.click(byText('main button', words[language].clear), 'clear');
            await settle(d);
            await d.go('/spaces?page=2');
            await waitCards(d);
            await settle(d);
            log(language, width, 'cleared — line:', clean(await d.text(`document.querySelector('main p[aria-live]').parentElement.parentElement`)).replace(/\n+/g, ' / '));
            const afterClear = d.requests.slice(atClear);
            log(language, width, 'after «clear»: requests', afterClear.length, 'with the header', afterClear.filter((r) => r.near !== null).length);
            await d.shot(`1b-near-cleared-${t}`, width < 1024 ? 1400 : 1300);
          } else {
            log(language, width, kind, 'requests with the header after pressing:', d.requests.slice(before).filter((r) => r.near !== null).length);
            await d.click(byText('main button', words[language].choose), 'choose your area');
            await d.sleep(800);
            const focus = await d.evaluate(`(() => { const el = document.activeElement; return { tag: el.tagName, role: el.getAttribute('role'), inSheet: !!el.closest('[role=dialog]'), inSidebar: !!el.closest('aside#directory-filters') }; })()`);
            log(language, width, kind, '«choose your area» → focus:', JSON.stringify(focus));
            if (kind === 'denied') await d.shot(`1b-near-choose-area-${t}`);
          }
          saveLog(d, `1b-near-${kind}-${t}`);
          all.push(...d.requests);
        } finally {
          b.chrome.kill();
        }
      }
      log(language, width, 'PRIVACY PROOF:', JSON.stringify(privacy(all)));
    }
  },

  // Carried 1: a search typed on page 2 keeps the focus in the field.
  async carried() {
    for (const [language, width] of PAIRS) {
      const { b, d } = await start({ language, theme: THEME[language], width });
      try {
        await d.go('/spaces?page=2');
        await waitCards(d);
        await settle(d);
        await d.type('main input[type=search]', 'Hub');
        await d.until(`location.search === '?q=Hub'`, 'the search in the address');
        await d.sleep(2500);
        const focus = await d.evaluate(`(() => { const el = document.activeElement; return { tag: el.tagName, type: el.type, value: el.value }; })()`);
        log(language, width, 'after typing on page 2 — address:', await search(d), 'focus:', JSON.stringify(focus), 'count:', await countLine(d));
        await d.shot(`1b-carried-search-focus-${language}-${THEME[language]}-${width}`);
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
