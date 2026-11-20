// The owner, second pass: what the first missed or measured badly — the calendar's today and range
// end hovered, the void dialog at 390, a photo lifted (mouse first, then keyboard) with true clips,
// LiveStatusControl's three tones (each response awaited), the account menu's item, the overlay
// scrim's painted pixel, the heatmap's overflow at 390, the input's focus box.
import { accounts, decodePng, hex, launch, pixel, RAW, sleep } from './lib.mjs';
import { checkVariant, curate, HEIGHTS, hoverTest, Results, TOKENS } from './checks.mjs';

const page = await launch('own2');
const results = new Results('own2');
const S = '/dashboard/spaces/26';
const isOpen = (sel) => page.evaluate(`!!document.querySelector(${JSON.stringify(sel)})`);
const escape = async () => {
  await page.key('Escape');
  await sleep(400);
};
let occupancyMode = 'people';
let fulfilledAt = 0;
const inAnHour = () => new Date(Date.now() + 3600_000).toISOString();
await page.fulfil('*/api/v1/manage/spaces/26/occupancy', (p) => p === '/api/v1/manage/spaces/26/occupancy', (body) => {
  const json = JSON.parse(body);
  const d = json.data;
  d.override = null;
  if (occupancyMode === 'people') d.status = 'AVAILABLE';
  if (occupancyMode === 'full') d.status = 'FULL';
  if (occupancyMode === 'closed') {
    d.status = 'AVAILABLE';
    d.override = { state: 'CLOSED', until: inAnHour() };
  }
  fulfilledAt = Date.now();
  return JSON.stringify(json);
});
await page.fulfil('*/api/v1/manage/spaces/26/photos', (p) => p === '/api/v1/manage/spaces/26/photos', (body) => {
  const json = JSON.parse(body);
  const list = Array.isArray(json.data) ? json.data : json.data?.photos;
  if (Array.isArray(list) && list.length) {
    const n = list.length;
    for (let i = n; i < 7; i += 1) {
      const copy = structuredClone(list[i % n]);
      if ('id' in copy) copy.id = (typeof copy.id === 'number' ? 900000 : 'x900000') + i;
      list.push(copy);
    }
  }
  return JSON.stringify(json);
});
/** Sets the live state and waits until the page has read it again. */
async function setMode(mode) {
  occupancyMode = mode;
  const before = Date.now();
  for (let i = 0; i < 9 && fulfilledAt < before; i += 1) {
    await page.evaluate(`document.dispatchEvent(new Event('visibilitychange')); dispatchEvent(new Event('focus')); true`);
    await sleep(5000);
  }
  await sleep(600);
  return fulfilledAt >= before;
}

try {
  const acc = accounts();
  await page.viewport(1440, 900);
  await page.signIn(acc.owner, `${S}/payments`);

  // ---- the calendar: today and the range end, hovered (1440, light and dark)
  await page.spa(`${S}/payments?from=2026-11-01&to=2026-11-10`);
  for (const theme of ['light', 'dark']) {
    await page.viewport(1440, 900);
    await page.prefs(theme, 'en');
    if (!(await isOpen('[data-slot=date-picker-content]'))) {
      await page.evaluate(`document.querySelector('[data-slot=date-picker-trigger]')?.click(); true`);
      await sleep(800);
    }
    await hoverTest(page, results, 'today in the calendar (beside a range day)', {
      target: `document.querySelector('[data-slot=date-picker-content] button[aria-current=date]')`,
      selected: `document.querySelector('[data-slot=date-picker-content] button[data-range-middle]')`,
      kind: 'wash',
      sample: (r) => ({ x: r.left + 4, y: r.top + r.h / 2 }),
      shotName: `26-hover-calendar-today-${theme}.png`,
    });
    await hoverTest(page, results, 'calendar range end (filled) hovered', {
      target: `document.querySelector('[data-slot=date-picker-content] button[data-range-end]')`,
      kind: 'primary',
      sample: (r) => ({ x: r.left + 4, y: r.top + r.h / 2 }),
    });
    await hoverTest(page, results, 'calendar range middle day hovered (keeps the tint?)', {
      target: `[...document.querySelectorAll('[data-slot=date-picker-content] button[data-range-middle]')][2]`,
      kind: 'accent',
      sample: (r) => ({ x: r.left + 4, y: r.top + r.h / 2 }),
    });
    if (await isOpen('[data-slot=date-picker-content]')) await escape();
  }

  // ---- the void dialog at 390 (the row's menu found by its name)
  const openVoid = async () => {
    if (await isOpen('[role=alertdialog]')) return;
    const ok = await page.evaluate(`(() => { const t = [...document.querySelectorAll('[data-slot=dropdown-menu-trigger]')].find((e) => /Payment actions|إجراءات الدفعة/.test(e.getAttribute('aria-label') || '') && window.__vp.visible(e)); if (!t) return false; t.scrollIntoView({ block: 'center' }); t.focus(); return true; })()`);
    if (!ok) return;
    await page.key('Enter');
    await sleep(600);
    await page.evaluate(`(() => { const i = [...document.querySelectorAll('[role=menuitem]')].find((e) => /إلغاء الدفعة|Void payment/.test(e.textContent)); i?.click(); return !!i; })()`);
    await sleep(800);
  };
  for (const v of [{ theme: 'light', lang: 'ar', width: 390 }, { theme: 'dark', lang: 'ar', width: 390 }, { theme: 'dark', lang: 'en', width: 768 }]) {
    const record = await checkVariant(page, results, 'void-dialog-390', v, { open: openVoid, axe: v.theme === 'light', focus: '[role=alertdialog]', focusShot: true });
    page.log(`  void dialog open: ${await isOpen('[role=alertdialog]')}`);
    if (v.theme === 'light') curate(results, record.shot, '18-void-payment-dialog-light-ar-390.png');
  }
  if (await isOpen('[role=alertdialog]')) await escape();

  // ---- the overlay scrim, painted (the check-in dialog over the sidebar's plain ground)
  await page.spa(`${S}/desk`);
  for (const theme of ['light', 'dark']) {
    await page.viewport(1440, 900);
    await page.prefs(theme, 'en');
    await page.mouse(2, 2);
    const at = { x: 120, y: 790 };
    const before = hex(pixel(decodePng(await page.shot()), at.x, at.y));
    await page.evaluate(`(() => { const b = [...document.querySelectorAll('button')].find((e) => /^(Check in a visit)$/.test(e.textContent.trim()) && window.__vp.visible(e)); b?.click(); return !!b; })()`);
    await sleep(1200);
    const after = hex(pixel(decodePng(await page.shot()), at.x, at.y));
    const scrim = await page.evaluate(`(() => { const o = document.querySelector('[data-slot=dialog-overlay], [data-slot=sheet-overlay], [data-slot=alert-dialog-overlay]'); return o ? getComputedStyle(o).backgroundColor : null; })()`);
    const g = [1, 3, 5].map((i) => Number.parseInt(before.slice(i, i + 2), 16));
    const a = theme === 'light' ? 0.5 : 0.7;
    const want = hex([13, 18, 23].map((c, i) => Math.round(c * a + g[i] * (1 - a))));
    results.data.ec[`scrim-${theme}`] = { at, ground: before, painted: after, computed: scrim, wantInk: want };
    page.log(`  scrim ${theme}: ground ${before} -> painted ${after} (computed ${scrim}); n-950 @ ${a} would paint ${want}`);
    await escape();
  }

  // ---- LiveStatusControl, each tone, hovered (each response awaited)
  for (const theme of ['light', 'dark']) {
    await page.viewport(1440, 900);
    await page.prefs(theme, 'en');
    for (const [mode, tone] of [['people', 'success'], ['full', 'warning'], ['closed', 'neutral']]) {
      const read = await setMode(mode);
      const word = await page.evaluate(`document.querySelector('[data-slot=popover-trigger]')?.textContent.trim()`);
      await hoverTest(page, results, `live status control (${tone} tone)`, {
        target: `document.querySelector('[data-slot=popover-trigger]')`,
        sample: (r) => ({ x: r.left + 4, y: r.top + 4 }),
        shotName: `37-hover-live-status-${tone}-${theme}.png`,
      });
      page.log(`    (state read again: ${read}; the trigger says «${word}»)`);
    }
  }
  await setMode('people');

  // ---- a menu item, the account menu opened by Enter (the visible trigger)
  for (const theme of ['light', 'dark']) {
    await page.viewport(1440, 900);
    await page.prefs(theme, 'en');
    await page.evaluate(`(() => { const t = [...document.querySelectorAll('[data-slot=dropdown-menu-trigger]')].find((e) => /^Account menu/.test(e.getAttribute('aria-label') || '') && window.__vp.visible(e)); t?.focus(); return !!t; })()`);
    await page.key('Enter');
    await sleep(700);
    await hoverTest(page, results, 'menu item (account menu, opened by Enter)', {
      target: `[...document.querySelectorAll('[role=menuitem]')].filter((e) => window.__vp.visible(e))[1]`,
      selected: `[...document.querySelectorAll('[role=menuitem]')].filter((e) => window.__vp.visible(e))[0]`,
      selectedKind: 'highlighted',
      sample: (r) => ({ x: r.left + r.w - 6, y: r.top + 3 }),
      shotName: `36-hover-menu-item-${theme}.png`,
    });
    await escape();
  }

  // ---- the heatmap at 390: what overflows the page, outside any scrolling box
  await page.spa(`${S}/finance`);
  await page.viewport(390, HEIGHTS[390]);
  for (const lang of ['ar', 'en']) {
    await page.prefs('light', lang);
    await page.evaluate(`(() => { const t = [...document.querySelectorAll('[role=tab]')].find((e) => /Occupancy|الإشغال/.test(e.textContent)); t?.focus(); return !!t; })()`);
    await page.key('Enter');
    await sleep(1200);
    await page.waitIdle();
    const over = await page.evaluate(`(() => {
      const d = document.documentElement;
      const out = [];
      for (const el of document.body.querySelectorAll('*')) {
        const r = el.getBoundingClientRect();
        if (r.width === 0 || (r.right <= d.clientWidth + 0.5 && r.left >= -0.5)) continue;
        let clipped = false;
        for (let n = el.parentElement; n && n !== document.body; n = n.parentElement) {
          const cs = getComputedStyle(n);
          if (cs.overflowX !== 'visible' || cs.clipPath !== 'none') { clipped = true; break; }
        }
        if (!clipped && !out.some((o) => o.node.contains(el))) out.push({ node: el, rect: [Math.round(r.left), Math.round(r.right)], cs: getComputedStyle(el).position });
      }
      return { scrollWidth: d.scrollWidth, clientWidth: d.clientWidth, heatmap: !!document.querySelector('[data-slot=heatmap]'), offenders: out.slice(0, 8).map((o) => ({ el: window.__vp.sel(o.node), rect: o.rect, position: o.cs, cls: (o.node.getAttribute('class') || '').slice(0, 160) })) };
    })()`);
    results.data.ec[`heatmapOverflow-${lang}`] = over;
    page.log(`  heatmap 390 ${lang}: ${JSON.stringify(over).slice(0, 900)}`);
    const file = `${RAW}/own2-heatmap-390-${lang}.png`;
    await page.shot(file);
    if (lang === 'ar') curate(results, file, '22-finance-heatmap-overflow-light-ar-390.png');
  }

  // ---- the profile's photos: a mouse drag on a fresh tile, then a keyboard lift (true clips)
  await page.viewport(1440, 900);
  await page.spa(`${S}/profile`);
  for (const theme of ['light', 'dark']) {
    await page.prefs(theme, 'en');
    if (!(await isOpen('[data-slot=sheet-content]'))) {
      await page.evaluate(`(() => { const b = [...document.querySelectorAll('button')].find((e) => /^(Manage photos)$/.test(e.textContent.trim())); b?.click(); return !!b; })()`);
      await sleep(1200);
      await page.waitIdle();
    }
    const tile = (i) => `[...document.querySelectorAll('.cursor-grab')].filter((e) => window.__vp.visible(e))[${i}]`;
    const info = (i, how) =>
      page.evaluate(`(() => {
        const t = ${tile(i)};
        if (!t) return null;
        const cs = getComputedStyle(t);
        const r = t.getBoundingClientRect();
        const o = parseFloat(cs.outlineWidth) + parseFloat(cs.outlineOffset || 0);
        const clippers = [];
        for (let n = t.parentElement; n && n !== document.body; n = n.parentElement) {
          const ns = getComputedStyle(n);
          if (ns.overflow !== 'visible' || ns.clipPath !== 'none') {
            const nr = n.getBoundingClientRect();
            if (nr.left > r.left - o || nr.top > r.top - o || nr.right < r.right + o || nr.bottom < r.bottom + o) clippers.push({ el: window.__vp.sel(n).split(' > ').slice(-2).join(' > '), rect: [nr.left, nr.top, nr.width, nr.height].map(Math.round) });
          }
        }
        return { how: ${JSON.stringify(how)}, el: window.__vp.sel(t).split(' > ').slice(-3).join(' > '), focused: document.activeElement === t, focusVisible: t.matches(':focus-visible'), cls: t.getAttribute('class'), outline: cs.outlineStyle + ' ' + cs.outlineWidth + ' ' + window.__vp.hex(window.__vp.parse(cs.outlineColor)) + ' offset ' + cs.outlineOffset, rect: [r.left, r.top, r.width, r.height].map(Math.round), clippedBy: clippers };
      })()`);
    const edgeOf = async (r) => {
      const img = decodePng(await page.shot());
      return {
        top: hex(pixel(img, r[0] + r[2] / 2, r[1] - 3)),
        start: hex(pixel(img, r[0] - 3, r[1] + r[3] / 2)),
        insideTop: hex(pixel(img, r[0] + r[2] / 2, r[1] + 1)),
      };
    };
    // Mouse first: the focus elsewhere, a press, a move past the activation distance.
    await page.evaluate(`document.activeElement?.blur?.(); true`);
    await page.evaluate(`${tile(2)}?.scrollIntoView({ block: 'center' }); true`);
    await sleep(300);
    const m0 = await info(2, 'rest');
    const cx = m0.rect[0] + m0.rect[2] / 2;
    const cy = m0.rect[1] + m0.rect[3] / 2;
    await page.mouse(cx, cy, 'mouseMoved');
    await page.mouse(cx, cy, 'mousePressed', { button: 'left', buttons: 1, clickCount: 1 });
    for (let i = 1; i <= 8; i += 1) {
      await page.send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: cx + i * 4, y: cy + i * 2, button: 'left', buttons: 1, pointerType: 'mouse' });
      await sleep(50);
    }
    await sleep(400);
    const mouse = await info(2, 'mouse drag');
    const mouseEdge = await edgeOf(mouse.rect);
    const mfile = `${RAW}/own2-photo-lifted-mouse-${theme}.png`;
    await page.shot(mfile, { x: Math.max(0, mouse.rect[0] - 30), y: Math.max(0, mouse.rect[1] - 30), width: mouse.rect[2] + 60, height: mouse.rect[3] + 60 });
    curate(results, mfile, `30-photo-lifted-mouse-${theme}-en-1440.png`);
    await page.key('Escape');
    await page.send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: cx, y: cy, button: 'left', buttons: 1, pointerType: 'mouse' });
    await page.mouse(cx, cy, 'mouseReleased', { button: 'left', buttons: 0, clickCount: 1 });
    await sleep(600);
    // The keyboard: Tab onto a tile is replaced by a focus with keyboard modality (a Tab from the one before).
    await page.evaluate(`(() => { const t = ${tile(1)}; t.scrollIntoView({ block: 'center' }); const p = document.createElement('span'); p.id = '__vp_p'; p.tabIndex = -1; t.parentElement.insertBefore(p, t); p.focus(); return true; })()`);
    await page.key('Tab');
    await sleep(200);
    const kRest = await info(1, 'keyboard focus');
    await page.key(' ');
    await sleep(600);
    const keyboard = await info(1, 'keyboard lift');
    const keyboardEdge = await edgeOf(keyboard.rect);
    const kfile = `${RAW}/own2-photo-lifted-keyboard-${theme}.png`;
    await page.shot(kfile, { x: Math.max(0, keyboard.rect[0] - 30), y: Math.max(0, keyboard.rect[1] - 30), width: keyboard.rect[2] + 60, height: keyboard.rect[3] + 60 });
    curate(results, kfile, `29-photo-lifted-keyboard-${theme}-en-1440.png`);
    await page.key('Escape');
    await sleep(500);
    await page.evaluate(`document.getElementById('__vp_p')?.remove(); true`);
    results.data.ec[`photoLifted2-${theme}`] = { mouse, mouseEdge, kRest, keyboard, keyboardEdge, spark: TOKENS[theme].spark, ring: TOKENS[theme].ring };
    page.log(`  photo ${theme}: mouse ${mouse.outline} edge ${JSON.stringify(mouseEdge)} clipped ${JSON.stringify(mouse.clippedBy)}; keyboard ${keyboard.outline} fv ${keyboard.focusVisible} edge ${JSON.stringify(keyboardEdge)} clipped ${JSON.stringify(keyboard.clippedBy)}`);
  }
  if (await isOpen('[data-slot=sheet-content]')) await escape();

  // ---- an input's focus box (the contacts sheet): the ring on its box, not on the input
  for (const theme of ['light', 'dark']) {
    await page.prefs(theme, 'en');
    await page.evaluate(`(() => { const b = [...document.querySelectorAll('button[aria-label]')].find((e) => /Contacts/.test(e.getAttribute('aria-label'))); b?.click(); return !!b; })()`);
    await sleep(900);
    await page.evaluate(`(() => { const i = document.querySelector('[data-slot=sheet-content] [data-slot=input]'); const p = document.createElement('span'); p.id = '__vp_p'; p.tabIndex = -1; i.closest('[data-slot=input-group]').parentElement.insertBefore(p, i.closest('[data-slot=input-group]')); p.focus(); return true; })()`);
    await page.key('Tab');
    await sleep(250);
    const box = await page.evaluate(`(() => { const a = document.activeElement; const g = a.closest('[data-slot=input-group]'); const cs = g && getComputedStyle(g); return { focused: window.__vp.sel(a).split(' > ').pop(), box: g ? cs.outlineStyle + ' ' + cs.outlineWidth + ' ' + window.__vp.hex(window.__vp.parse(cs.outlineColor)) + ' border ' + window.__vp.hex(window.__vp.parse(cs.borderTopColor)) : null }; })()`);
    results.data.ec[`inputFocus-${theme}`] = box;
    page.log(`  input focus ${theme}: ${JSON.stringify(box)}`);
    await page.evaluate(`document.getElementById('__vp_p')?.remove(); true`);
    await escape();
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
