// The visual pass, the admin: overview, spaces, a space's editor, the rail (768) and the drawer (390),
// the reports with a FilterTag; the admin's header read once; EC6 (the sizes and the mark at 64 px).
import { readFileSync } from 'node:fs';
import { accounts, decodePng, launch, RAW, sleep } from './lib.mjs';
import { checkVariant, curate, HEIGHTS, hoverTest, matrix, Results } from './checks.mjs';

const ONLY = process.argv[2] ? process.argv[2].split(',') : null;
const want = (name) => !ONLY || ONLY.includes(name);
const page = await launch('adm');
const results = new Results(ONLY ? `adm-${ONLY.join('+')}` : 'adm');
const isPriority = (v) => (v.theme === 'light' && v.lang === 'ar' && v.width === 390) || (v.theme === 'dark' && v.lang === 'en' && v.width === 1440);
const A = '/dashboard/admin';
const shotNames = (n, label) => ({ 'light-ar-390': `${n}-${label}-light-ar-390.png`, 'dark-en-1440': `${n}-${label}-dark-en-1440.png` });
const isOpen = (sel) => page.evaluate(`!!document.querySelector(${JSON.stringify(sel)})`);
const escape = async () => {
  await page.key('Escape');
  await sleep(400);
};

async function screen(name, { path, tall = true, open, focus = true, variants = matrix(), curateAs = {} }) {
  page.log(`== ${name} ${path}`);
  if (path) await page.spa(path);
  for (const v of variants) {
    try {
      const record = await checkVariant(page, results, name, v, { tall, open, axe: isPriority(v), focus: isPriority(v) ? focus : false, focusShot: isPriority(v) });
      const key = `${v.theme}-${v.lang}-${v.width}`;
      if (curateAs[key]) curate(results, record.shot, curateAs[key]);
    } catch (error) {
      page.log(`  ${name} ${JSON.stringify(v)} ERROR ${error.message}`);
      results.note(`${name} ${JSON.stringify(v)}: ${error.message}`);
    }
  }
}

try {
  const acc = accounts();
  await page.viewport(1440, 900);
  await page.signIn(acc.admin, A);
  results.data.signedInAs = 'admin';

  if (want('overview')) await screen('admin-overview', { path: A, curateAs: { ...shotNames('44', 'admin-overview'), 'light-ar-768': '45-admin-rail-light-ar-768.png', 'dark-en-768': '45-admin-rail-dark-en-768.png' } });
  if (want('spaces')) await screen('admin-spaces', { path: `${A}/spaces`, curateAs: shotNames('46', 'admin-spaces') });
  if (want('editor')) await screen('admin-space-editor', { path: `${A}/spaces/26`, curateAs: shotNames('47', 'admin-space-editor') });

  // ---- the admin's header, read once; the logo's sizes (EC6) at each width
  if (want('header')) {
    const ec6 = [];
    await page.spa(A);
    for (const width of [1440, 768, 390]) {
      await page.viewport(width, HEIGHTS[width]);
      for (const lang of ['ar', 'en']) {
        await page.prefs('light', lang);
        if (width === 390) {
          await page.evaluate(`document.querySelector('[data-slot=sidebar-trigger]')?.click(); true`);
          await sleep(800);
        }
        const read = await page.evaluate(`(() => {
          const h = [...document.querySelectorAll('[data-slot=sidebar-header]')].find((e) => window.__vp.visible(e));
          if (!h) return null;
          const parts = [];
          const walk = (n) => {
            if (n.nodeType === 3) { const t = n.textContent.trim(); if (t) parts.push(t); return; }
            if (n.nodeType !== 1) return;
            if (n.getAttribute('aria-hidden') === 'true') return;
            if (n.getAttribute('aria-label')) { parts.push('[' + n.getAttribute('role') + ' ' + n.getAttribute('aria-label') + ']'); return; }
            for (const c of n.childNodes) walk(c);
          };
          walk(h);
          return { read: parts.join(' · '), logos: window.__vp.logoScan().filter((l) => l.where.includes('sidebar-header')) };
        })()`);
        ec6.push({ width, lang, ...read });
        page.log(`  admin header ${width} ${lang}: ${JSON.stringify(read).slice(0, 700)}`);
        if (width === 390) await escape();
      }
    }
    results.data.ec.adminHeader = ec6;
  }

  // ---- EC6: the component's mark at 64 px against masaha-mark-berry.svg at 64 px, on white
  if (want('ec6')) {
    await page.spa(A);
    await page.viewport(768, 1024);
    await page.prefs('light', 'en');
    const ref = readFileSync('C:/dev/masaha/app-design/docs/design/prototype/masaha/logo/masaha-mark-berry.svg', 'utf8')
      .replace(/<\?xml[^>]*>/, '')
      .replace('<svg ', '<svg width="64" height="64" style="display:block" ')
      .replace(/id="h"/g, 'id="vp-ref-h"')
      .replace(/id="d"/g, 'id="vp-ref-d"')
      .replace(/url\(#h\)/g, 'url(#vp-ref-h)')
      .replace(/url\(#d\)/g, 'url(#vp-ref-d)');
    const placed = await page.evaluate(`(() => {
      const mark = [...document.querySelectorAll('[data-slot=sidebar-header] svg[data-slot=logo]')].find((e) => window.__vp.visible(e));
      if (!mark) return null;
      const box = document.createElement('div');
      box.id = '__vp_ec6';
      box.style.cssText = 'position:fixed;left:0;top:0;z-index:2147483647;background:#fff;display:flex;gap:16px;padding:16px';
      const a = document.createElement('div'); a.style.cssText = 'width:64px;height:64px;background:#fff';
      const clone = mark.cloneNode(true); clone.style.width = '64px'; clone.style.height = '64px'; clone.style.display = 'block';
      a.appendChild(clone);
      const b = document.createElement('div'); b.style.cssText = 'width:64px;height:64px;background:#fff';
      b.innerHTML = ${JSON.stringify(ref)};
      box.append(a, b);
      document.body.appendChild(box);
      const ra = a.getBoundingClientRect(); const rb = b.getBoundingClientRect();
      return { a: [ra.left, ra.top], b: [rb.left, rb.top], cls: mark.getAttribute('class'), size: [mark.getBoundingClientRect().width, mark.getBoundingClientRect().height] };
    })()`);
    await sleep(400);
    if (placed) {
      const one = decodePng(await page.shot(`${RAW}/adm-ec6-component.png`, { x: placed.a[0], y: placed.a[1], width: 64, height: 64 }));
      const two = decodePng(await page.shot(`${RAW}/adm-ec6-reference.png`, { x: placed.b[0], y: placed.b[1], width: 64, height: 64 }));
      const pair = `${RAW}/adm-ec6-pair.png`;
      await page.shot(pair, { x: 0, y: 0, width: 176, height: 96 });
      curate(results, pair, '48-ec6-mark-64-component-vs-file.png');
      let differing = 0;
      let worst = 0;
      for (let i = 0; i < one.data.length; i += 4) {
        const d = Math.max(Math.abs(one.data[i] - two.data[i]), Math.abs(one.data[i + 1] - two.data[i + 1]), Math.abs(one.data[i + 2] - two.data[i + 2]));
        worst = Math.max(worst, d);
        if (d > 8) differing += 1;
      }
      const total = one.data.length / 4;
      results.data.ec.ec6mark = { ...placed, differing, total, percent: +((differing / total) * 100).toFixed(3), worst, ok: differing / total <= 0.01 };
      page.log(`  EC6 mark: ${differing}/${total} differ > 8 (${((differing / total) * 100).toFixed(2)} %), worst ${worst}`);
    } else {
      results.note('EC6: the rail mark was not found at 768');
    }
    await page.evaluate(`document.getElementById('__vp_ec6')?.remove(); true`);
  }

  // ---- the drawer at 390
  if (want('drawer')) {
    await page.spa(A);
    const openDrawer = async () => {
      if (await isOpen('[data-slot=sheet-content]')) return;
      await page.evaluate(`document.querySelector('[data-slot=sidebar-trigger]')?.click(); true`);
      await sleep(800);
    };
    await screen('admin-drawer', {
      path: null,
      tall: false,
      open: openDrawer,
      focus: '[data-slot=sheet-content]',
      variants: [{ theme: 'light', lang: 'ar', width: 390 }, { theme: 'dark', lang: 'en', width: 390 }, { theme: 'dark', lang: 'ar', width: 390 }, { theme: 'light', lang: 'en', width: 390 }],
      curateAs: { 'light-ar-390': '49-admin-drawer-light-ar-390.png', 'dark-en-390': '49-admin-drawer-dark-en-390.png' },
    });
    await escape();
  }

  // ---- the reports with a FilterTag (the space), and §5 on the admin's tables, 1440
  if (want('reports')) {
    await screen('admin-reports-filtered', { path: `${A}/reports?space=26`, variants: matrix({ full: false }), curateAs: { 'dark-en-1440': '50-admin-reports-filter-tag-dark-en-1440.png' } });
    for (const theme of ['light', 'dark']) {
      await page.viewport(1440, 900);
      await page.spa(`${A}/reports?space=26`);
      await page.prefs(theme, 'en');
      await hoverTest(page, results, "FilterTag's remove", {
        target: `document.querySelector('[data-slot=filter-tag] button')`,
        kind: 'wash',
        sample: (r) => ({ x: r.left + r.w / 2, y: r.top + 2 }),
        shotName: `51-hover-filter-tag-remove-${theme}.png`,
      });
      await page.spa(`${A}/spaces`);
      await hoverTest(page, results, 'sort header (admin spaces)', {
        target: `[...document.querySelectorAll('[data-slot=table-head] button')].find((b) => window.__vp.visible(b))`,
        kind: 'wash',
        sample: (r) => ({ x: r.left + 3, y: r.top + 3 }),
      });
      await hoverTest(page, results, 'admin spaces row', { target: `document.querySelector('[data-slot=table-body] [data-slot=table-row]')`, sample: (r) => ({ x: r.left + r.w / 2, y: r.top + 3 }) });
      await hoverTest(page, results, 'admin sidebar item beside the current one', {
        target: `[...document.querySelectorAll('[data-slot=sidebar-menu-button]:not([data-active=true])')][1]`,
        selected: `document.querySelector('[data-slot=sidebar-menu-button][data-active=true]')`,
        sample: (r) => ({ x: r.left + r.w - 10, y: r.top + 3 }),
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
  results.data.chrome = await page.close();
  results.save();
}
