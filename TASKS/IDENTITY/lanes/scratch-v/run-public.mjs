// The visual pass, public screens (guest): Home, the directory, its map, a space's page, sign in,
// register, forgot, the 404, the phone menu, the header at 360, a loading state; the public hover
// set; EC8, EC9 and the tab's icon.
import { readFileSync, writeFileSync } from 'node:fs';
import { BASE, decodePng, hex, launch, pixel, RAW, SHOTS, sleep } from './lib.mjs';
import { checkVariant, curate, focusProbe, HEIGHTS, hoverTest, matrix, Results } from './checks.mjs';

const ONLY = process.argv[2] ? process.argv[2].split(',') : null;
const want = (name) => !ONLY || ONLY.includes(name);
const page = await launch('pub');
const results = new Results(ONLY ? `pub-${ONLY.join('+')}` : 'pub');
const isPriority = (v) => (v.theme === 'light' && v.lang === 'ar' && v.width === 390) || (v.theme === 'dark' && v.lang === 'en' && v.width === 1440);

async function screen(name, { url, tall = true, open, focus = true, variants = matrix(), curateAs = {}, before }) {
  page.log(`== ${name} ${url}`);
  if (before) await before();
  await page.goto(url);
  for (const v of variants) {
    const record = await checkVariant(page, results, name, v, {
      tall,
      open,
      axe: isPriority(v),
      focus: isPriority(v) ? focus : false,
      focusShot: isPriority(v),
    });
    const key = `${v.theme}-${v.lang}-${v.width}`;
    if (curateAs[key]) curate(results, record.shot, curateAs[key]);
  }
}

const shotNames = (n, label) => ({ 'light-ar-390': `${n}-${label}-light-ar-390.png`, 'dark-en-1440': `${n}-${label}-dark-en-1440.png` });

try {
  await page.viewport(1440, 900);
  await page.goto('/');
  await page.storePrefs('light', 'ar');

  // ---- EC8: the icons, served; the tab's icon
  if (want('ec8')) {
    const ec8 = {};
    for (const [path, type] of [
      ['/favicon.svg', 'image/svg+xml'],
      ['/favicon.ico', 'image/x-icon|image/vnd.microsoft.icon'],
      ['/apple-touch-icon.png', 'image/png'],
    ]) {
      const response = await fetch(BASE + path);
      const body = Buffer.from(await response.arrayBuffer());
      ec8[path] = { status: response.status, type: response.headers.get('content-type'), bytes: body.length, ok: response.status === 200 && type.split('|').some((t) => (response.headers.get('content-type') ?? '').startsWith(t)) };
    }
    // The links on the page, and the icon request Chrome makes on a load.
    const iconRequests = [];
    page.onRequest = (request, type) => {
      if (/favicon|apple-touch|\.ico|icon/i.test(request.url)) iconRequests.push(`${type} ${request.url}`);
    };
    await page.goto('/');
    await sleep(1500);
    ec8.links = await page.evaluate(`[...document.querySelectorAll('link[rel~=icon], link[rel=apple-touch-icon], meta[name=theme-color]')].map((l) => l.outerHTML)`);
    ec8.iconRequests = iconRequests;
    page.onRequest = null;
    // The SVG under each scheme: its colours on a grey ground.
    await page.send('Emulation.setDefaultBackgroundColorOverride', { color: { r: 128, g: 128, b: 128, a: 1 } });
    for (const scheme of ['light', 'dark']) {
      await page.send('Emulation.setEmulatedMedia', { media: '', features: [{ name: 'prefers-color-scheme', value: scheme }] });
      await page.viewport(256, 256);
      await page.goto('/favicon.svg', { wait: false });
      await sleep(800);
      const file = `${RAW}/pub-ec8-favicon-${scheme}.png`;
      const img = decodePng(await page.shot(file));
      const counts = new Map();
      for (let i = 0; i < img.data.length; i += 4) {
        const h = hex([img.data[i], img.data[i + 1], img.data[i + 2]]);
        counts.set(h, (counts.get(h) ?? 0) + 1);
      }
      ec8[`svg-${scheme}`] = [...counts.entries()].filter(([h]) => h !== '#808080').sort((a, b) => b[1] - a[1]).slice(0, 4);
      curate(results, file, `ec8-favicon-svg-${scheme}.png`);
    }
    await page.send('Emulation.setEmulatedMedia', { media: '', features: [{ name: 'prefers-color-scheme', value: 'light' }] });
    await page.send('Emulation.setDefaultBackgroundColorOverride', {});
    results.data.ec.ec8 = ec8;
    page.log(`EC8 ${JSON.stringify(ec8)}`);
    results.save();
  }

  // ---- EC9: the rasters, opened and looked at
  if (want('ec9')) {
    const ec9 = {};
    const ico = readFileSync('C:/dev/masaha/app-design/apps/web/public/favicon.ico');
    const entries = [];
    for (let i = 0; i < ico.readUInt16LE(4); i += 1) {
      const o = 6 + i * 16;
      const size = ico.readUInt32LE(o + 8);
      const offset = ico.readUInt32LE(o + 12);
      entries.push({ w: ico[o] || 256, h: ico[o + 1] || 256, bpp: ico.readUInt16LE(o + 6), size, offset, png: ico.subarray(offset, offset + size) });
    }
    ec9.ico = entries.map(({ w, h, bpp, size }) => ({ w, h, bpp, size }));
    const ico16 = entries.find((e) => e.w === 16);
    writeFileSync(`${RAW}/pub-ec9-ico16.png`, ico16.png);
    const describePng = (name, buffer, { round = false } = {}) => {
      const img = decodePng(buffer);
      let minX = img.width;
      let minY = img.height;
      let maxX = -1;
      let maxY = -1;
      let transparent = 0;
      let outside = 0;
      const cx = img.width / 2;
      const cy = img.height / 2;
      for (let y = 0; y < img.height; y += 1) {
        for (let x = 0; x < img.width; x += 1) {
          const [r, g, b, a] = pixel(img, x, y);
          if (a < 255) transparent += 1;
          const ink = a > 32 && (r < 235 || g < 235 || b < 235);
          if (ink) {
            minX = Math.min(minX, x);
            minY = Math.min(minY, y);
            maxX = Math.max(maxX, x);
            maxY = Math.max(maxY, y);
            if (round && Math.hypot(x + 0.5 - cx, y + 0.5 - cy) > img.width / 2) outside += 1;
          }
        }
      }
      return {
        name,
        size: [img.width, img.height],
        corners: [pixel(img, 0, 0), pixel(img, img.width - 1, 0), pixel(img, 0, img.height - 1), pixel(img, img.width - 1, img.height - 1)].map((p) => `${hex(p)}/${p[3]}`),
        transparentPixels: transparent,
        drawingBox: [minX, minY, maxX, maxY],
        margins: { start: minX, top: minY, end: img.width - 1 - maxX, bottom: img.height - 1 - maxY },
        ...(round ? { inkOutsideRoundCrop: outside } : {}),
      };
    };
    ec9.apple = describePng('apple-touch-icon.png', readFileSync('C:/dev/masaha/app-design/apps/web/public/apple-touch-icon.png'));
    ec9.ico16 = describePng('favicon.ico 16', ico16.png);
    ec9.google = describePng('masaha-logo-120.png', readFileSync('C:/dev/masaha/workspace/TASKS/IDENTITY/google/masaha-logo-120.png'), { round: true });
    // Looked at, enlarged without smoothing, beside each other; the 120 also under a round crop.
    const b64 = (buffer) => buffer.toString('base64');
    const html = `<!doctype html><html><body style="margin:0;background:#c8c8c8;font:14px sans-serif">
      <div style="display:flex;gap:24px;padding:16px;align-items:flex-start">
        <figure style="margin:0"><img src="data:image/png;base64,${b64(readFileSync('C:/dev/masaha/app-design/apps/web/public/apple-touch-icon.png'))}" width="180" height="180"><figcaption>180 (1x)</figcaption></figure>
        <figure style="margin:0"><img src="data:image/png;base64,${b64(ico16.png)}" width="16" height="16"><figcaption>16 (1x)</figcaption></figure>
        <figure style="margin:0"><img src="data:image/png;base64,${b64(ico16.png)}" width="128" height="128" style="image-rendering:pixelated"><figcaption>16 at 8x</figcaption></figure>
        <figure style="margin:0"><img src="data:image/png;base64,${b64(readFileSync('C:/dev/masaha/workspace/TASKS/IDENTITY/google/masaha-logo-120.png'))}" width="120" height="120"><figcaption>120</figcaption></figure>
        <figure style="margin:0"><img src="data:image/png;base64,${b64(readFileSync('C:/dev/masaha/workspace/TASKS/IDENTITY/google/masaha-logo-120.png'))}" width="120" height="120" style="border-radius:50%"><figcaption>120, round crop</figcaption></figure>
      </div></body></html>`;
    await page.viewport(760, 260);
    await page.goto('about:blank', { wait: false });
    await page.send('Page.setDocumentContent', { frameId: (await page.send('Page.getFrameTree')).frameTree.frame.id, html });
    await sleep(600);
    const file = `${RAW}/pub-ec9-rasters.png`;
    await page.shot(file);
    curate(results, file, 'ec9-rasters.png');
    results.data.ec.ec9 = ec9;
    page.log(`EC9 ${JSON.stringify(ec9)}`);
    results.save();
  }

  // ---- the screens
  if (want('selftest')) {
    await page.goto('/');
    await page.viewport(1440, 900);
    const test = await page.evaluate(`(() => { const p = document.createElement('p'); p.id = '__vp_t'; p.textContent = 'self test words'; p.style.cssText = 'position:fixed;top:300px;left:300px;z-index:99999;color:#999999;background:#aaaaaa;font-size:14px;padding:8px'; document.body.appendChild(p); const r = window.__vp.contrastScan(); p.remove(); return r.failures.filter((f) => f.text.startsWith('self test')); })()`);
    results.data.selftest = test;
    page.log(`contrast self-test (expect one failure ~1.2): ${JSON.stringify(test)}`);
  }
  if (want('home')) await screen('home', { url: '/', curateAs: shotNames('01', 'home') });
  if (want('directory')) {
    await screen('directory', {
      url: '/spaces?period=MONTH&open=1&verified=1',
      focus: "js:document.querySelector('main a[aria-labelledby]')?.parentElement",
      curateAs: shotNames('02', 'directory'),
    });
  }
  if (want('map')) {
    const select = async () => {
      await page.evaluate(`(() => { const pins = [...document.querySelectorAll('.leaflet-marker-pane [role=button]')]; const on = pins.find((p) => p.getAttribute('aria-pressed') === 'true'); if (!on && pins[0]) pins[0].click(); return pins.length; })()`);
      await sleep(600);
    };
    await screen('map', {
      url: '/spaces?view=map&period=MONTH',
      tall: false,
      open: select,
      focus: true,
      curateAs: shotNames('03', 'map-selected'),
    });
  }
  if (want('space')) {
    // «+N»: the page's photos made seven (the demo has four), by the response, not by data.
    await page.fulfil('*/api/v1/spaces/pal-hub', (path) => path === '/api/v1/spaces/pal-hub', (body) => {
      const json = JSON.parse(body);
      const photos = json.data.photos;
      while (photos.length < 7) photos.push({ ...photos[photos.length % 4] });
      return JSON.stringify(json);
    });
    await screen('space', { url: '/spaces/pal-hub', curateAs: shotNames('04', 'space-page') });
    await page.clearFulfils();
  }
  if (want('signin')) await screen('signin', { url: '/login', curateAs: shotNames('05', 'sign-in') });
  if (want('register')) await screen('register', { url: '/register', curateAs: { 'light-ar-390': '06-register-light-ar-390.png' } });
  if (want('forgot')) await screen('forgot', { url: '/forgot-password', curateAs: { 'dark-en-1440': '07-forgot-dark-en-1440.png' } });
  if (want('404')) await screen('404', { url: '/no-such-page', curateAs: shotNames('08', '404') });

  // ---- the phone menu (guest), at 390 and 360, both directions
  if (want('phonemenu')) {
    const openMenu = async () => {
      const isOpen = await page.evaluate(`!!document.querySelector('[data-slot=sheet-content]')`);
      if (!isOpen) {
        await page.evaluate(`document.querySelector('header button[aria-haspopup=dialog], header [data-slot=sheet-trigger]')?.click(); true`);
        await sleep(700);
      }
    };
    const variants = [];
    for (const width of [390, 360]) for (const lang of ['ar', 'en']) for (const theme of ['light', 'dark']) variants.push({ theme, lang, width });
    page.log('== phonemenu');
    await page.goto('/spaces');
    for (const v of variants) {
      const record = await checkVariant(page, results, 'phonemenu', v, {
        tall: false,
        open: openMenu,
        axe: v.width === 390 && ((v.theme === 'light' && v.lang === 'ar') || (v.theme === 'dark' && v.lang === 'en')),
        focus: v.width === 390 ? '[data-slot=sheet-content]' : false,
      });
      if (v.width === 390 && v.theme === 'light') curate(results, record.shot, `09-phone-menu-light-${v.lang}-390.png`);
      // The drawer's logo at the inline start.
      const drawer = record.logo.find((l) => l.where.includes('sheet-header'));
      page.log(`    drawer logo ${v.lang}: ${JSON.stringify(drawer && { size: drawer.size, dir: drawer.dir, startGap: drawer.startGap, pos: drawer.pos })}`);
    }
  }

  // ---- EC14: the header at 360 (guest), both languages and themes
  if (want('header360')) {
    page.log('== header360');
    await page.goto('/');
    const ec14 = [];
    for (const lang of ['ar', 'en']) {
      for (const theme of ['light', 'dark']) {
        await page.viewport(360, HEIGHTS[360]);
        await page.prefs(theme, lang);
        const header = await page.evaluate(`(() => {
          const h = document.querySelector('header');
          const row = h.firstElementChild;
          const kids = [...row.querySelectorAll('button, a')].filter((e) => window.__vp.visible(e)).map((e) => { const r = e.getBoundingClientRect(); return { el: window.__vp.sel(e).split(' > ').pop(), text: window.__vp.textOf(e).slice(0, 20), left: Math.round(r.left), right: Math.round(r.right), w: Math.round(r.width) }; });
          const overlaps = [];
          for (let i = 0; i < kids.length; i += 1) for (let j = i + 1; j < kids.length; j += 1) if (kids[i].left < kids[j].right - 1 && kids[j].left < kids[i].right - 1) overlaps.push([kids[i].el, kids[j].el]);
          return { scrollWidth: document.documentElement.scrollWidth, clientWidth: document.documentElement.clientWidth, rowScroll: row.scrollWidth, rowClient: row.clientWidth, kids, overlaps, outside: kids.filter((k) => k.left < 0 || k.right > 360) };
        })()`);
        const file = `${RAW}/pub-header360-${theme}-${lang}.png`;
        await page.shot(file, { x: 0, y: 0, width: 360, height: 72 });
        if (theme === 'light') curate(results, file, `10-header-360-guest-${lang}.png`);
        ec14.push({ who: 'guest', theme, lang, ...header, ok: header.scrollWidth <= header.clientWidth && header.rowScroll <= header.rowClient && !header.overlaps.length && !header.outside.length });
        page.log(`  EC14 guest ${theme}-${lang}: ${JSON.stringify(ec14.at(-1))}`);
      }
    }
    results.data.ec.ec14 = ec14;
    results.save();
  }

  // ---- a loading state: the directory's request held
  if (want('loading')) {
    page.log('== loading');
    let release;
    const until = new Promise((resolve) => {
      release = resolve;
    });
    page.holds.push({ match: (path) => path.startsWith('/api/v1/spaces?') && path.includes('q=loading'), until });
    await page.goto('/spaces?q=loading', { wait: false });
    await sleep(2500);
    for (const v of [{ theme: 'light', lang: 'ar', width: 390 }, { theme: 'dark', lang: 'en', width: 1440 }, { theme: 'dark', lang: 'ar', width: 390 }, { theme: 'light', lang: 'en', width: 1440 }]) {
      // checkVariant waits for quiet; a held request is older than the window it counts after 15 s.
      await page.viewport(v.width, HEIGHTS[v.width]);
      await page.evaluate(`localStorage.setItem('masaha.theme', '${v.theme}'); localStorage.setItem('masaha.language', '${v.lang}'); dispatchEvent(new StorageEvent('storage', { key: 'masaha.theme' })); dispatchEvent(new StorageEvent('storage', { key: 'masaha.language' })); true`);
      await sleep(700);
      const key = `${v.theme}-${v.lang}-${v.width}`;
      const record = {
        key,
        skeletons: await page.evaluate(`[...document.querySelectorAll('[data-slot=skeleton]')].filter((e) => window.__vp.visible(e)).map((e) => window.__vp.hex(window.__vp.parse(getComputedStyle(e).backgroundColor))).filter((v, i, a) => a.indexOf(v) === i)`),
        count: await page.evaluate(`document.querySelectorAll('[data-slot=skeleton]').length`),
        sea: await page.vp('seaScan'),
        overflow: await page.vp('overflow'),
        contrast: await page.vp('contrastScan'),
        console: page.takeConsole(),
      };
      if (isPriority(v)) record.axe = await page.axe();
      const file = `${RAW}/pub-loading-${key}.png`;
      await page.shot(file);
      record.shot = file;
      if (isPriority(v)) curate(results, file, `11-loading-${key}.png`);
      results.screen('loading').variants[key] = record;
      page.log(`  loading ${key}: skeleton fills ${JSON.stringify(record.skeletons)} (${record.count}), sea ${record.sea.hitCount}, contrast fails ${record.contrast.failures.length}, axe ${record.axe?.map((a) => a.id)}`);
    }
    release();
    page.holds = [];
    await sleep(500);
    results.save();
  }

  // ---- §5 the public hover set, 1440, light and dark
  if (want('hover')) {
    page.log('== public hover set');
    for (const theme of ['light', 'dark']) {
      await page.viewport(1440, 900);
      await page.goto('/spaces?period=MONTH');
      await page.prefs(theme, 'en');
      await hoverTest(page, results, 'outline button (header sign in)', { target: `document.querySelector('header a[data-slot=button][href="/login"]')`, shotName: `20-hover-outline-button-${theme}.png` });
      await hoverTest(page, results, 'chip beside a chip that is on (List/Map)', {
        target: `document.querySelector('[data-slot=toggle-group-item][data-state=off]')`,
        selected: `document.querySelector('[data-slot=toggle-group-item][data-state=on]')`,
        shotName: `21-hover-chip-${theme}.png`,
      });
      await hoverTest(page, results, 'subscription choice (segmented)', {
        target: `[...document.querySelectorAll('[data-slot=segmented-control-item]')].find((e) => e.getAttribute('data-state') !== 'checked' && !e.hasAttribute('data-checked'))`,
        selected: `[...document.querySelectorAll('[data-slot=segmented-control-item]')].find((e) => e.getAttribute('data-state') === 'checked' || e.hasAttribute('data-checked'))`,
        kind: 'wash',
        selectedKind: 'card',
        shotName: `22-hover-subscription-choice-${theme}.png`,
      });
      await hoverTest(page, results, 'space card', {
        target: `document.querySelector('main a [data-slot=card]')`,
        sample: (r) => ({ x: r.left + 12, y: r.top + r.h - 8 }),
        shotName: `23-hover-space-card-${theme}.png`,
      });
      await page.spa('/spaces/pal-hub');
      await hoverTest(page, results, 'contact tile', {
        target: `[...document.querySelectorAll('main a')].find((a) => /^(https:\\/\\/wa\\.me|tel:|mailto:)/.test(a.getAttribute('href') || ''))`,
        sample: (r) => ({ x: r.left + r.w - 6, y: r.top + 4 }),
        shotName: `24-hover-contact-tile-${theme}.png`,
      });
      await hoverTest(page, results, 'desktop tabs (hours)', {
        target: `document.querySelector('[data-slot=tabs-trigger][data-state=inactive]')`,
        selected: `document.querySelector('[data-slot=tabs-trigger][data-state=active]')`,
        kind: 'wash',
        selectedKind: 'card',
      });
      await page.spa('/login');
      await hoverTest(page, results, 'primary button (sign in)', {
        target: `document.querySelector('form button[type=submit]')`,
        kind: 'primary',
        shotName: `25-hover-primary-${theme}.png`,
      });
    }
    results.save();
  }
  // ---- §5 a sort header: no production table sorts, so the design system's showcase table (dev only)
  if (want('sorthdr')) {
    for (const theme of ['light', 'dark']) {
      await page.viewport(1440, 900);
      await page.goto(`/__showcase/preview/data/data-table?theme=${theme}&lang=en`);
      await sleep(800);
      await hoverTest(page, results, 'sort header (showcase DataTable; no production table sorts)', {
        target: `[...document.querySelectorAll('[data-slot=table-head] button')].find((b) => window.__vp.visible(b))`,
        kind: 'wash',
        sample: (r) => ({ x: r.left + 3, y: r.top + 3 }),
        shotName: `27-hover-sort-header-showcase-${theme}.png`,
      });
    }
  }
  page.log(`refreshes ${page.refreshes}, loads ${page.loads}, blocked ${JSON.stringify(page.blocked)}`);
  results.data.blocked = page.blocked;
  results.data.loads = page.loads;
} catch (error) {
  page.log(`ERROR ${error.stack}`);
  results.note(`ERROR ${error.message}`);
} finally {
  results.save();
  const closed = await page.close();
  results.data.chrome = closed;
  results.save();
}
