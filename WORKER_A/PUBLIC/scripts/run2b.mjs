// PR 2's three real-run cases left, re-scripted by the supervisor (2026-10-22) from run2.mjs:
// - Enter is sent with its text ('\r'), so a native button activates (run2.mjs's key() sent none);
// - «مركّز على موقعي» is pressed after the map is panned away, and judged by where the user point stands;
// - Leaflet's log on the dev server (5320) and on the production build's preview (5321).
// Reads only: no sign-in, no write. Usage: node run2b.mjs <centre|leaflet|carried> [ar|en]
import { writeFileSync } from 'node:fs';
import { byText, driver, launch, SHOTS } from './cdp2.mjs';

const [only, onlyLanguage] = process.argv.slice(2);
const log = (...a) => console.log('·', ...a);
const clean = (text) => (text ?? '').replace(/[⁦-⁩]/g, '');
const ORIGIN = 'http://localhost:5320';
const THEME = { ar: 'light', en: 'dark' };
const t = (language, width) => `${language}-${THEME[language]}-${width}`;
const PAIRS = [['ar', 390], ['en', 1440]];
const pick = (list) => list.filter(([language]) => !onlyLanguage || language === onlyLanguage);
const W = {
  ar: { map: '^خريطة$', near: '^الأقرب إليّ$', centre: 'مركّز على موقعي', stop: 'إيقاف الترتيب', clear: 'مسح موقعي', clearFilters: '^مسح الفلاتر$' },
  en: { map: '^Map$', near: '^Nearest to me$', centre: 'Centre on my location', stop: 'Stop sorting', clear: 'Clear my location', clearFilters: '^Clear filters$' },
};

async function start({ language, width, height = 900, base = '' }) {
  const b = await launch();
  const d = driver(b);
  const requests = [];
  await b.send('Network.enable');
  b.on((m) => {
    if (m.method === 'Network.requestWillBeSent') requests.push({ url: m.params.request.url });
  });
  d.requests = requests;
  d.b = b;
  await d.viewport(width, height);
  await d.theme(THEME[language] === 'dark');
  await d.go(base + '/');
  await d.prefs(language, THEME[language]);
  return { b, d };
}

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

/** Focus the element, then a real Enter (keyDown with its text, as a keyboard sends it). */
async function enterOn(d, expression, what) {
  const ok = await d.evaluate(`(() => { const el = ${expression}; if (!el) return false; el.scrollIntoView({ block: 'center' }); el.focus(); return document.activeElement === el; })()`);
  if (!ok) throw new Error(`nothing to focus: ${what}`);
  await d.b.send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13, text: '\r', unmodifiedText: '\r' });
  await d.b.send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13 });
  await d.sleep(400);
}

const MAP = `document.querySelector('[role=application]')`;
const waitMap = (d) => d.until(`document.querySelectorAll('[role=application] .map-mark').length > 0`, 'the pins', 20000);
const activeName = (d) => d.evaluate(`(() => { const el = document.activeElement; return (el.getAttribute('aria-label') ?? el.textContent ?? el.tagName).trim().slice(0, 60); })()`);
const statusLine = async (d) => clean(await d.text(`document.querySelector('main [role=status]')`));
/** The user point's distance, in px, from the map's centre (null when not drawn). */
const userOffset = (d) =>
  d.evaluate(`(() => { const m = ${MAP}, u = document.querySelector('.map-user'); if (!m || !u) return null; const a = m.getBoundingClientRect(), b = u.getBoundingClientRect(); return Math.round(Math.hypot(b.x + b.width / 2 - (a.x + a.width / 2), b.y + b.height / 2 - (a.y + a.height / 2))); })()`);

const cases = {
  async centre() {
    for (const [language, width] of pick(PAIRS)) {
      const { b, d } = await start({ language, width });
      try {
        await b.send('Browser.setPermission', { permission: { name: 'geolocation' }, setting: 'granted', origin: ORIGIN });
        await b.send('Emulation.setGeolocationOverride', { latitude: 31.5017, longitude: 34.4668, accuracy: 30 });
        await d.go('/spaces?view=map');
        await waitMap(d);
        await d.sleep(1500);
        await press(d, byText('main button', W[language].near), 'near me');
        await d.sleep(2500);
        log(language, width, 'granted — user point:', clean(await d.evaluate(`document.querySelector('.map-user')?.getAttribute('aria-label') ?? 'none'`)), '· offset from centre:', await userOffset(d));
        // Pan away: focus the map, then arrows (Leaflet's keyboard), a long way.
        await d.evaluate(`(() => { ${MAP}.focus(); return true; })()`);
        for (let i = 0; i < 12; i++) {
          await d.b.send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'ArrowUp', code: 'ArrowUp', windowsVirtualKeyCode: 38 });
          await d.b.send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'ArrowUp', code: 'ArrowUp', windowsVirtualKeyCode: 38 });
          await d.sleep(120);
        }
        await d.sleep(800);
        const away = await userOffset(d);
        log(language, width, 'after panning away — offset from centre:', away);
        await d.shot(`2-centre-away-${t(language, width)}`);
        await press(d, byText('main button', W[language].centre), 'centre');
        await d.sleep(1500);
        const back = await userOffset(d);
        log(language, width, 'after «مركّز على موقعي» — offset from centre:', back, back !== null && away !== null && back < 20 && away > back ? 'CENTRED' : 'NOT CENTRED');
        await d.shot(`2-centre-${t(language, width)}`);
      } finally {
        b.chrome.kill();
      }
    }
  },

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

  async carried() {
    for (const [language, width] of pick(PAIRS)) {
      const { b, d } = await start({ language, width });
      try {
        await b.send('Browser.setPermission', { permission: { name: 'geolocation' }, setting: 'granted', origin: ORIGIN });
        await b.send('Emulation.setGeolocationOverride', { latitude: 31.5017, longitude: 34.4668, accuracy: 30 });
        await d.go('/spaces');
        await d.until(`document.querySelectorAll('section[aria-labelledby] a[href^="/spaces/"]').length > 0`, 'cards');
        await d.sleep(1500);
        await enterOn(d, byText('main button', W[language].near), 'near me');
        await d.sleep(2500);
        log(language, width, 'Enter on near me — state line:', (await statusLine(d)).replace(/\n+/g, ' | '));
        await enterOn(d, byText('main button', W[language].stop), 'stop');
        await d.sleep(1000);
        log(language, width, 'after stop (Enter) — focus on:', clean(await activeName(d)));
        await enterOn(d, byText('main button', W[language].near), 'near me again');
        await d.sleep(2500);
        await enterOn(d, byText('main button', W[language].clear), 'clear');
        await d.sleep(1000);
        log(language, width, 'after clear (Enter) — focus on:', clean(await activeName(d)));
        await d.shot(`2-carried-focus-${t(language, width)}`);
        await d.go('/spaces?q=Hub&available=1&friday=1&students=1');
        await d.until(`!!${byText('main button', W[language].clearFilters)}`, 'no match');
        await d.shot(`2-carried-nomatch-${t(language, width)}`);
        await press(d, byText('main button', W[language].clearFilters), 'clear filters');
        await d.sleep(1500);
        log(language, width, 'no match «مسح الفلاتر» → address:', decodeURIComponent(await d.evaluate('location.search')), '· search field:', await d.evaluate(`document.querySelector('main input[type=search]').value`));
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
