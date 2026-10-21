// PR 1a's real run: the Directory's list on the real app (web 5320, API 3320, worker A's masaha_dev).
// Reads only: no sign-in, no write. Screenshots to shots\pr1a, the network log beside them.
import { writeFileSync } from 'node:fs';
import { byText, driver, launch, SHOTS } from './cdp.mjs';

const only = process.argv[2]; // a case's name, to run one alone
const log = (...a) => console.log('·', ...a);
const clean = (text) => (text ?? '').replace(/[⁦-⁩]/g, '');

async function start({ language, theme, width }) {
  const b = await launch();
  const d = driver(b);
  const requests = [];
  await b.send('Network.enable');
  b.on((m) => {
    if (m.method === 'Network.requestWillBeSent') {
      const { url, headers } = m.params.request;
      if (url.includes('/api/v1/')) {
        const near = Object.entries(headers).find(([k]) => k.toLowerCase() === 'masaha-near');
        requests.push(`API ${url.replace(/^.*\/api\/v1/, '')}${near ? ` [Masaha-Near: ${near[1]}]` : ''}`);
      } else if (/\.(m?js|tsx?|jsx|css)(\?|$)/.test(url) || url.includes('/src/') || url.includes('/node_modules/')) {
        requests.push(`ASSET ${url.replace('http://localhost:5320', '')}`);
      }
    }
    if (m.method === 'Network.responseReceived' && m.params.response.url.includes('/api/v1/')) {
      requests.push(`  -> ${m.params.response.status} ${m.params.response.url.replace(/^.*\/api\/v1/, '')}`);
    }
  });
  d.requests = requests;
  await d.viewport(width, 900);
  await d.theme(theme === 'dark');
  await d.go('/');
  await d.prefs(language, theme);
  return { b, d };
}

const cards = (d) =>
  d.evaluate(
    `[...document.querySelectorAll('section[aria-labelledby] a[href^="/spaces/"]')].map((a) => a.querySelector('h3')?.textContent)`,
  );
const active = (d) =>
  d.evaluate(
    `(() => { const el = document.activeElement; return el ? \`\${el.tagName.toLowerCase()}#\${el.id} "\${(el.textContent ?? '').trim().slice(0, 40)}"\` : null; })()`,
  );
const waitCards = (d) =>
  d.until(`document.querySelectorAll('section[aria-labelledby] a[href^="/spaces/"]').length > 0`, 'cards');

/** Presses the mouse on the option whose text matches, as a person does: Radix chooses on pointer events. */
async function choose(b, d, pattern) {
  const at = await d.evaluate(
    `(() => { const el = [...document.querySelectorAll('[role=option]')].find((o) => new RegExp(${JSON.stringify(pattern)}).test(o.textContent)); if (!el) return null; const r = el.getBoundingClientRect(); return { x: r.x + r.width / 2, y: r.y + r.height / 2 }; })()`,
  );
  if (at === null) throw new Error(`no option ${pattern}`);
  for (const type of ['mouseMoved', 'mousePressed', 'mouseReleased']) {
    await b.send('Input.dispatchMouseEvent', { type, x: at.x, y: at.y, button: 'left', clickCount: 1 });
  }
  await d.sleep(1200);
}

const MATRIX = [
  ['ar', 'light'],
  ['en', 'dark'],
];
const WIDTHS = [390, 768, 1440];
const HEIGHT = { 390: 2600, 768: 2200, 1440: 1700 };

const cases = {
  // The list at every width, both languages: cards, the cover or the mark, the status, hours, verified.
  async list() {
    for (const [language, theme] of MATRIX) {
      for (const width of WIDTHS) {
        const { b, d } = await start({ language, theme, width });
        try {
          await d.go('/spaces');
          await waitCards(d);
          await d.sleep(1500);
          const text = clean(await d.text(`document.querySelector('main')`));
          log(language, width, 'count line:', clean(await d.text(`document.querySelector('main p[aria-live]')`)));
          if (width === 1440) log(language, 'main text:', text.replace(/\n+/g, ' / ').slice(0, 900));
          await d.shot(`1a-list-${language}-${theme}-${width}`, HEIGHT[width]);
          if (width === 1440) writeFileSync(`${SHOTS}/1a-list-${language}-${theme}-log.txt`, d.requests.join('\n') + '\n');
        } finally {
          b.chrome.kill();
        }
      }
    }
  },

  // A search by an English name in Arabic; a search of diacritics only; no match and its clear.
  async search() {
    for (const [language, theme] of MATRIX) {
      const { b, d } = await start({ language, theme, width: 1440 });
      try {
        await d.go('/spaces');
        await waitCards(d);
        await d.type('input[type=search]', 'Palm');
        await d.until(`location.search.includes('q=Palm')`, 'q in the address');
        await d.sleep(1500);
        log(language, 'search Palm:', await d.evaluate('location.search'), await cards(d), clean(await d.text(`document.querySelector('main p[aria-live]')`)));
        log(language, 'sort trigger:', clean(await d.text(`document.querySelector('[role=combobox]')`)));
        await d.shot(`1a-search-english-name-${language}-${theme}-1440`, 1000);

        await d.type('input[type=search]', 'َِ');
        await d.sleep(1500);
        log(language, 'diacritics: address', await d.evaluate('location.search'), 'error:', clean(await d.text(`document.querySelector('[data-slot=field] p.text-destructive')`)));
        await d.shot(`1a-search-diacritics-${language}-${theme}-1440`, 1000);

        await d.type('input[type=search]', 'zzzzqq');
        await d.until(`location.search.includes('q=zzzzqq')`, 'q zzzz');
        await d.sleep(1500);
        log(language, 'no match:', clean(await d.text(`document.querySelector('section[aria-labelledby]')`)).replace(/\n+/g, ' / '));
        await d.shot(`1a-no-match-${language}-${theme}-1440`, 1000);
        await d.click(byText('button', language === 'ar' ? '^مسح الفلاتر$' : '^Clear filters$'), 'clear');
        await d.sleep(1500);
        log(language, 'after clear: address', JSON.stringify(await d.evaluate('location.search')), 'field', JSON.stringify(await d.evaluate(`document.querySelector('input[type=search]').value`)), 'cards', (await cards(d)).length);
        writeFileSync(`${SHOTS}/1a-search-${language}-${theme}-log.txt`, d.requests.join('\n') + '\n');
      } finally {
        b.chrome.kill();
      }
    }
  },

  // The sort: by name; a search's best match; a reload and a copied link show the same list.
  async sort() {
    for (const [language, theme] of MATRIX) {
      const { b, d } = await start({ language, theme, width: 1440 });
      try {
        await d.go('/spaces');
        await waitCards(d);
        await d.openMenu(`document.querySelector('[role=combobox]')`, 'sort');
        log(language, 'options:', clean(await d.evaluate(`[...document.querySelectorAll('[role=option]')].map((o) => o.textContent).join(' | ')`)));
        await d.shot(`1a-sort-open-${language}-${theme}-1440`);
        await choose(b, d, language === 'ar' ? 'حسب الاسم' : 'By name');
        await d.sleep(1500);
        const address = await d.evaluate('location.pathname + location.search');
        const before = await cards(d);
        log(language, 'by name:', address, before.slice(0, 6));
        await d.shot(`1a-sort-name-${language}-${theme}-1440`, 1700);
        await d.go(address);
        await waitCards(d);
        await d.sleep(1000);
        const after = await cards(d);
        log(language, 'reload same list:', JSON.stringify(before) === JSON.stringify(after));
        // A copied link: a fresh browser at the same address.
        const fresh = await start({ language, theme, width: 1440 });
        try {
          await fresh.d.go(address);
          await waitCards(fresh.d);
          await fresh.d.sleep(1000);
          log(language, 'copied link same list:', JSON.stringify(before) === JSON.stringify(await cards(fresh.d)));
        } finally {
          fresh.b.chrome.kill();
        }
        await d.type('input[type=search]', 'Hub');
        await d.until(`location.search.includes('q=Hub')`, 'q Hub');
        await d.sleep(1500);
        log(language, 'search + chosen order trigger:', clean(await d.text(`document.querySelector('[role=combobox]')`)));
        await d.openMenu(`document.querySelector('[role=combobox]')`, 'sort');
        log(language, 'options with a search:', clean(await d.evaluate(`[...document.querySelectorAll('[role=option]')].map((o) => o.textContent).join(' | ')`)));
        await choose(b, d, language === 'ar' ? 'الأفضل تطابقًا' : 'Best match');
        await d.sleep(1500);
        log(language, 'best match:', await d.evaluate('location.search'), clean(await d.text(`document.querySelector('[role=combobox]')`)), await cards(d));
        await d.shot(`1a-sort-best-match-${language}-${theme}-1440`, 1200);
        writeFileSync(`${SHOTS}/1a-sort-${language}-${theme}-log.txt`, d.requests.join('\n') + '\n');
      } finally {
        b.chrome.kill();
      }
    }
  },

  // Page 2: the focus on the results; Back returns to page 1.
  async pages() {
    for (const [language, theme] of MATRIX) {
      for (const width of [390, 1440]) {
        const { b, d } = await start({ language, theme, width });
        try {
          await d.go('/spaces');
          await waitCards(d);
          const first = await cards(d);
          log(language, width, 'page 1 cards:', first.length, 'pages:', clean(await d.text(`document.querySelector('nav[aria-label]:last-of-type')`)));
          const pager = language === 'ar' ? 'الصفحة 2' : 'Page 2';
          await d.click(`document.querySelector('a[aria-label="${pager}"]')`, 'page 2');
          await d.until(`location.search === '?page=2'`, 'page 2');
          await d.sleep(1500);
          log(language, width, 'page 2:', (await cards(d)).length, 'focus:', await active(d), 'scrollY', await d.evaluate('scrollY'));
          await d.shot(`1a-page-2-${language}-${theme}-${width}`, width === 390 ? 1400 : 1000);
          await d.evaluate('history.back(); true');
          await d.sleep(1500);
          log(language, width, 'back:', JSON.stringify(await d.evaluate('location.search')), 'same as page 1:', JSON.stringify(first) === JSON.stringify(await cards(d)));
          if (width === 1440) writeFileSync(`${SHOTS}/1a-pages-${language}-${theme}-log.txt`, d.requests.join('\n') + '\n');
        } finally {
          b.chrome.kill();
        }
      }
    }
  },

  // The skip link from the page's top, and the focus after a header link.
  async skip() {
    for (const [language, theme] of MATRIX) {
      const { b, d } = await start({ language, theme, width: 1440 });
      try {
        await d.go('/spaces');
        await waitCards(d);
        await d.key('Tab', 'Tab', 9);
        log(language, 'first Tab:', await active(d));
        await d.shot(`1a-skip-link-${language}-${theme}-1440`, 700);
        await d.key('Enter', 'Enter', 13);
        await d.sleep(400);
        log(language, 'after Enter:', await active(d), 'hash', await d.evaluate('location.hash'));
        await d.click(byText('header nav a', language === 'ar' ? '^عن مساحة$' : '^About Masaha$'), 'about');
        await d.sleep(1500);
        log(language, 'after the header link:', await d.evaluate('location.pathname'), await active(d));
        await d.click(byText('header nav a', language === 'ar' ? '^المساحات$' : '^Spaces$'), 'spaces');
        await waitCards(d);
        await d.sleep(800);
        log(language, 'back on spaces:', await active(d));
      } finally {
        b.chrome.kill();
      }
    }
  },
};

for (const [name, run] of Object.entries(cases)) {
  if (only && only !== name) continue;
  console.log(`== ${name}`);
  try {
    await run();
  } catch (error) {
    console.log('FAILED', name, String(error.message ?? error));
  }
}
