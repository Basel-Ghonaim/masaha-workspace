// Re-check of the lead's fixes at 5e8a3b7b (F1–F4), screenshot pixels, 1440 en (390 for F3),
// light and dark; axe on the phone menu (light-ar-390) and the desk (dark-en-1440).
import { accounts, decodePng, hex, launch, pixel, RAW, sleep } from './lib.mjs';
import { checkVariant, curate, Results } from './checks.mjs';

const page = await launch('rechk');
const results = new Results('recheck');
const S = '/dashboard/spaces/26';
const out = {};
const isOpen = (sel) => page.evaluate(`!!document.querySelector(${JSON.stringify(sel)})`);
const escape = async () => {
  await page.key('Escape');
  await sleep(400);
};
const px = async (points) => {
  const img = decodePng(await page.shot());
  return points.map(([x, y]) => hex(pixel(img, x, y)));
};
const rectOf = (expr) => page.evaluate(`(() => { const e = (${expr}); if (!e) return null; e.scrollIntoView({ block: 'center' }); const r = e.getBoundingClientRect(); return { left: r.left, top: r.top, w: r.width, h: r.height, x: r.left + r.width / 2, y: r.top + r.height / 2 }; })()`);
const bgOf = (expr) => page.evaluate(`(() => { const e = (${expr}); return e ? getComputedStyle(e).backgroundColor : null; })()`);
/** Rest and hovered pixel of an element, at a point inside its fill. */
async function restHover(label, expr, at, clipName) {
  await page.mouse(2, 2);
  await sleep(450);
  const r = await rectOf(expr);
  if (!r) return { label, missing: true };
  const p = at(r);
  const [rest] = await px([[p.x, p.y]]);
  const restBg = await bgOf(expr);
  await page.mouse(r.x, r.y);
  await sleep(550);
  const [hovered] = await px([[p.x, p.y]]);
  const hoverBg = await bgOf(expr);
  if (clipName) {
    const file = `${RAW}/rechk-${clipName}.png`;
    await page.shot(file, { x: Math.max(0, r.left - 24), y: Math.max(0, r.top - 24), width: r.w + 48, height: r.h + 48 });
    curate(results, file, `${clipName}.png`);
  }
  await page.mouse(2, 2);
  await sleep(300);
  const record = { label, at: [Math.round(p.x), Math.round(p.y)], rest, hovered, restBg, hoverBg };
  page.log(`  ${label}: rest ${rest} -> hovered ${hovered} (computed ${restBg} -> ${hoverBg})`);
  return record;
}

let occupancyMode = 'people';
let fulfilledAt = 0;
await page.fulfil('*/api/v1/manage/spaces/26/occupancy', (p) => p === '/api/v1/manage/spaces/26/occupancy', (body) => {
  const json = JSON.parse(body);
  json.data.override = occupancyMode === 'closed' ? { state: 'CLOSED', until: new Date(Date.now() + 3600_000).toISOString() } : null;
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
  await page.viewport(1440, 900);
  await page.signIn(accounts().owner, `${S}/desk`);
  out.head = await page.evaluate(`getComputedStyle(document.documentElement).getPropertyValue('--primary-hover').trim()`);

  // ---- F1: primary hovered (the desk's check-in, the calendar's range end), the scrim, secondary (below with F4)
  for (const theme of ['light', 'dark']) {
    await page.viewport(1440, 900);
    await page.spa(`${S}/desk`);
    await page.prefs(theme, 'en');
    out[`primary-desk-${theme}`] = await restHover(`primary (Check in a visit) ${theme}`, `[...document.querySelectorAll('button')].find((e) => /^Check in a visit$/.test(e.textContent.trim()) && window.__vp.visible(e))`, (r) => ({ x: r.x, y: r.top + 3 }), `F1-primary-hover-${theme}`);
    // The scrim: the check-in dialog over the sidebar's plain ground.
    await page.mouse(2, 2);
    const at = [120, 790];
    const [ground] = await px([at]);
    await page.evaluate(`[...document.querySelectorAll('button')].find((e) => /^Check in a visit$/.test(e.textContent.trim()) && window.__vp.visible(e))?.click(); true`);
    await sleep(1200);
    const [painted] = await px([at]);
    const computed = await page.evaluate(`(() => { const o = document.querySelector('[data-slot=dialog-overlay], [data-slot=sheet-overlay], [data-slot=alert-dialog-overlay]'); return o ? getComputedStyle(o).backgroundColor : null; })()`);
    const g = [1, 3, 5].map((i) => Number.parseInt(ground.slice(i, i + 2), 16));
    const a = theme === 'light' ? 0.5 : 0.7;
    const want = hex([13, 18, 23].map((c, i) => Math.round(c * a + g[i] * (1 - a))));
    out[`scrim-${theme}`] = { at, ground, painted, computed, wantInk: want };
    page.log(`  scrim ${theme}: ground ${ground} -> painted ${painted} (computed ${computed}); ink n-950 @ ${a}: ${want}`);
    const sfile = `${RAW}/rechk-scrim-${theme}.png`;
    await page.shot(sfile);
    if (theme === 'dark') curate(results, sfile, `F1-dialog-scrim-${theme}-en-1440.png`);
    await escape();
    // The calendar's range end (primary), hovered.
    await page.spa(`${S}/payments?from=2026-11-01&to=2026-11-10`);
    await page.evaluate(`document.querySelector('[data-slot=date-picker-trigger]')?.click(); true`);
    await sleep(900);
    out[`primary-calendar-${theme}`] = await restHover(`primary (calendar range end) ${theme}`, `document.querySelector('[data-slot=date-picker-content] button[data-range-end]')`, (r) => ({ x: r.left + 4, y: r.y }));
    if (await isOpen('[data-slot=date-picker-content]')) await escape();
  }

  // ---- F4 (and F1's secondary): the live-status control, neutral tone (CLOSED by hand), now the secondary variant
  await page.spa(`${S}/desk`);
  for (const theme of ['light', 'dark']) {
    await page.viewport(1440, 900);
    await page.prefs(theme, 'en');
    const read = await setMode('closed');
    const word = await page.evaluate(`document.querySelector('[data-slot=popover-trigger]')?.textContent.trim()`);
    const cls = await page.evaluate(`document.querySelector('[data-slot=popover-trigger]')?.getAttribute('class')`);
    out[`live-neutral-${theme}`] = { read, word, secondary: /bg-secondary/.test(cls ?? ''), ...(await restHover(`live status neutral (secondary) ${theme}`, `document.querySelector('[data-slot=popover-trigger]')`, (r) => ({ x: r.left + 6, y: r.top + 4 }), `F4-live-status-neutral-${theme}`)) };
    page.log(`    («${word}», state read again: ${read})`);
  }
  await setMode('people');
  // The secondary hover's colour, computed beside the inks (oklab, as fixed; oklch for comparison).
  out.secondaryProbe = await page.evaluate(`(() => {
    const p = document.createElement('div'); document.body.appendChild(p);
    const r = {};
    for (const [k, v] of Object.entries({ 'light oklab': 'color-mix(in oklab, #ecf4fc, #1a1f25 8%)', 'dark oklab': 'color-mix(in oklab, #2c3137, #f7fbff 8%)', 'light oklch (before)': 'color-mix(in oklch, #ecf4fc, #1a1f25 8%)', 'dark oklch (before)': 'color-mix(in oklch, #2c3137, #f7fbff 8%)' })) { p.style.backgroundColor = v; const c = getComputedStyle(p).backgroundColor; r[k] = c + ' = ' + window.__vp.hex(window.__vp.parse(c)); }
    p.remove(); return r;
  })()`);
  page.log(`  secondary probe ${JSON.stringify(out.secondaryProbe)}`);

  // ---- F2: the photos, lifted by a mouse drag and by the keyboard; a photo merely focused
  await page.viewport(1440, 900);
  await page.spa(`${S}/profile`);
  for (const theme of ['light', 'dark']) {
    await page.prefs(theme, 'en');
    if (!(await isOpen('[data-slot=sheet-content]'))) {
      await page.evaluate(`[...document.querySelectorAll('button')].find((e) => /^(Manage photos)$/.test(e.textContent.trim()))?.click(); true`);
      await sleep(1200);
      await page.waitIdle();
    }
    const tile = (i) => `[...document.querySelectorAll('.cursor-grab')].filter((e) => window.__vp.visible(e))[${i}]`;
    const info = (i) =>
      page.evaluate(`(() => { const t = ${tile(i)}; if (!t) return null; const cs = getComputedStyle(t); const r = t.getBoundingClientRect(); return { outline: cs.outlineStyle + ' ' + cs.outlineWidth + ' ' + window.__vp.hex(window.__vp.parse(cs.outlineColor)) + ' offset ' + cs.outlineOffset, fv: t.matches(':focus-visible'), rect: [r.left, r.top, r.width, r.height] }; })()`);
    const edges = async (r) => {
      const [x, y, w, h] = r;
      const [top0, top1, top2, start0, start1, outside] = await px([[x + w / 2, y + 0.5], [x + w / 2, y + 1.5], [x + w / 2, y + 2.5], [x + 0.5, y + h / 2], [x + 1.5, y + h / 2], [x + w / 2, y - 3]]);
      return { top0, top1, top2, start0, start1, outside };
    };
    // A mouse drag on a tile not focused.
    await page.evaluate(`document.activeElement?.blur?.(); ${tile(2)}?.scrollIntoView({ block: 'center' }); true`);
    await sleep(300);
    const m0 = await info(2);
    const cx = m0.rect[0] + m0.rect[2] / 2;
    const cy = m0.rect[1] + m0.rect[3] / 2;
    await page.mouse(cx, cy, 'mouseMoved');
    await page.mouse(cx, cy, 'mousePressed', { button: 'left', buttons: 1, clickCount: 1 });
    for (let i = 1; i <= 8; i += 1) {
      await page.send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: cx + i * 4, y: cy + i * 2, button: 'left', buttons: 1, pointerType: 'mouse' });
      await sleep(50);
    }
    await sleep(400);
    const mouse = await info(2);
    mouse.edges = await edges(mouse.rect);
    const mfile = `${RAW}/rechk-photo-mouse-${theme}.png`;
    await page.shot(mfile, { x: Math.max(0, mouse.rect[0] - 24), y: Math.max(0, mouse.rect[1] - 24), width: mouse.rect[2] + 48, height: mouse.rect[3] + 48 });
    curate(results, mfile, `F2-photo-lifted-mouse-${theme}.png`);
    await page.key('Escape');
    await page.send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: cx, y: cy, button: 'left', buttons: 1, pointerType: 'mouse' });
    await page.mouse(cx, cy, 'mouseReleased', { button: 'left', buttons: 0, clickCount: 1 });
    await sleep(600);
    // The keyboard: a Tab onto a tile (focused only), then Space (lifted).
    await page.evaluate(`(() => { const t = ${tile(1)}; t.scrollIntoView({ block: 'center' }); const p = document.createElement('span'); p.id = '__vp_p'; p.tabIndex = -1; t.parentElement.insertBefore(p, t); p.focus(); return true; })()`);
    await page.key('Tab');
    await sleep(250);
    const focused = await info(1);
    focused.edges = await edges(focused.rect);
    await page.key(' ');
    await sleep(600);
    const keyboard = await info(1);
    keyboard.edges = await edges(keyboard.rect);
    const kfile = `${RAW}/rechk-photo-keyboard-${theme}.png`;
    await page.shot(kfile, { x: Math.max(0, keyboard.rect[0] - 24), y: Math.max(0, keyboard.rect[1] - 24), width: keyboard.rect[2] + 48, height: keyboard.rect[3] + 48 });
    curate(results, kfile, `F2-photo-lifted-keyboard-${theme}.png`);
    await page.key('Escape');
    await sleep(500);
    await page.evaluate(`document.getElementById('__vp_p')?.remove(); true`);
    out[`photo-${theme}`] = { mouse, focused, keyboard };
    page.log(`  photo ${theme}: mouse ${mouse.outline} fv ${mouse.fv} ${JSON.stringify(mouse.edges)}; focused ${focused.outline} ${JSON.stringify(focused.edges)}; keyboard ${keyboard.outline} fv ${keyboard.fv} ${JSON.stringify(keyboard.edges)}`);
  }
  if (await isOpen('[data-slot=sheet-content]')) await escape();

  // ---- F3: the site's phone menu at 390, the current page (Spaces) and another entry (Home)
  await page.spa('/spaces');
  const openMenu = async () => {
    if (await isOpen('[data-slot=sheet-content]')) return;
    await page.evaluate(`document.querySelector('header [data-slot=sheet-trigger]')?.click(); true`);
    await sleep(800);
  };
  for (const theme of ['light', 'dark']) {
    await page.viewport(390, 844);
    await page.prefs(theme, 'en');
    await openMenu();
    const cur = `document.querySelector('[data-slot=sheet-content] nav a[aria-current=page]')`;
    const other = `[...document.querySelectorAll('[data-slot=sheet-content] nav a:not([aria-current=page])')][0]`;
    const point = (r) => ({ x: r.left + r.w - 8, y: r.top + 3 });
    const c = await restHover(`phone menu current (Spaces) ${theme}`, cur, point);
    const o = await restHover(`phone menu other (Home) ${theme}`, other, point);
    // Both in one shot, the other hovered.
    const ro = await rectOf(other);
    const rc = await rectOf(cur);
    await page.mouse(ro.x, ro.y);
    await sleep(500);
    const file = `${RAW}/rechk-phone-menu-${theme}.png`;
    await page.shot(file, { x: 0, y: Math.max(0, Math.min(ro.top, rc.top) - 16), width: 390, height: Math.abs(rc.top - ro.top) + ro.h + 32 });
    curate(results, file, `F3-phone-menu-current-vs-hover-${theme}-390.png`);
    await page.mouse(2, 2);
    out[`menu-${theme}`] = { current: c, other: o };
    await escape();
  }

  // ---- axe: the phone menu light-ar-390, the desk dark-en-1440 (with the full §4 checks)
  const menuRecord = await checkVariant(page, results, 'phonemenu-recheck', { theme: 'light', lang: 'ar', width: 390 }, { open: openMenu, axe: true, focus: '[data-slot=sheet-content]' });
  out.axeMenu = menuRecord.axe;
  await escape();
  await page.spa(`${S}/desk`);
  const deskRecord = await checkVariant(page, results, 'desk-recheck', { theme: 'dark', lang: 'en', width: 1440 }, { axe: true, focus: true, tall: true });
  out.axeDesk = deskRecord.axe;
  page.log(`  axe menu ${JSON.stringify(out.axeMenu.map((v) => v.id))}; axe desk ${JSON.stringify(out.axeDesk.map((v) => v.id))}`);
  out.blocked = page.blocked;
  out.loads = page.loads;
  out.refreshes = page.refreshes;
} catch (error) {
  page.log(`ERROR ${error.stack}`);
  out.error = error.message;
} finally {
  results.data.ec = out;
  results.save();
  results.data.chrome = await page.close();
  results.save();
}
