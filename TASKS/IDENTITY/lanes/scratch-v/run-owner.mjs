// The visual pass, the owner (demo-owner, space 26): overview, the desk with the check-in dialog,
// Payments with «إلغاء الدفعة» open, a date picker open on a range, the space profile (a Sheet, the
// photos with «+N», a contact and a photo lifted), Finance (charts, heatmap), the rail (768) and the
// drawer (390); /me and the favourites, the phone menu signed in, the header at 360 signed in; the
// owner's hover set, LiveStatusControl's tones, and EC3's painted pixels.
import { writeFileSync } from 'node:fs';
import { accounts, decodePng, hex, launch, pixel, RAW, sleep } from './lib.mjs';
import { checkVariant, curate, focusProbe, HEIGHTS, hoverTest, matrix, Results, TOKENS } from './checks.mjs';

const ONLY = process.argv[2] ? process.argv[2].split(',') : null;
const want = (name) => !ONLY || ONLY.includes(name);
const page = await launch('own');
const results = new Results(ONLY ? `own-${ONLY.join('+')}` : 'own');
const isPriority = (v) => (v.theme === 'light' && v.lang === 'ar' && v.width === 390) || (v.theme === 'dark' && v.lang === 'en' && v.width === 1440);
const S = '/dashboard/spaces/26';
const shotNames = (n, label) => ({ 'light-ar-390': `${n}-${label}-light-ar-390.png`, 'dark-en-1440': `${n}-${label}-dark-en-1440.png` });
const textIs = (sel, re) => `[...document.querySelectorAll(${JSON.stringify(sel)})].find((e) => ${re}.test(e.textContent.trim()) && window.__vp.visible(e))`;

// ---- the responses the demo lacks, made in the browser (never in the data)
let occupancyMode = 'people';
const inAnHour = () => new Date(Date.now() + 3600_000).toISOString();
const since = (min) => new Date(Date.now() - min * 60_000).toISOString();
await page.fulfil('*/api/v1/manage/spaces/26/occupancy', (p) => p === '/api/v1/manage/spaces/26/occupancy', (body) => {
  const json = JSON.parse(body);
  writeFileSync(`${RAW}/../orig-occupancy.json`, body);
  const d = json.data;
  if (occupancyMode === 'people' || occupancyMode === 'full' || occupancyMode === 'closed') {
    d.people = [
      { kind: 'VISIT', id: 900001, customerId: null, name: 'سامي عودة', audience: 'GENERAL', since: since(95), chargeNowAgorot: 1000 },
      { kind: 'VISIT', id: 900002, customerId: null, name: 'Rana Haddad', audience: 'STUDENT', since: since(40), chargeNowAgorot: 400 },
      { kind: 'VISIT', id: 900003, customerId: null, name: 'محمد الأغا', audience: 'GENERAL', since: since(12), chargeNowAgorot: null },
    ];
    d.present = 3;
  }
  if (occupancyMode === 'full') d.status = 'FULL';
  if (occupancyMode === 'closed') d.override = { state: 'CLOSED', until: inAnHour() };
  return JSON.stringify(json);
});
let photosPadded = false;
await page.fulfil('*/api/v1/manage/spaces/26/photos', (p) => p === '/api/v1/manage/spaces/26/photos', (body) => {
  writeFileSync(`${RAW}/../orig-photos.json`, body);
  const json = JSON.parse(body);
  const list = Array.isArray(json.data) ? json.data : json.data?.photos;
  if (Array.isArray(list) && list.length) {
    const n = list.length;
    for (let i = n; i < 7; i += 1) {
      const copy = structuredClone(list[i % n]);
      if ('id' in copy) copy.id = (typeof copy.id === 'number' ? 900000 : 'x900000') + i;
      if ('position' in copy) copy.position = i;
      if ('order' in copy) copy.order = i;
      list.push(copy);
    }
    photosPadded = true;
  }
  return JSON.stringify(json);
});
const refetchNow = async () => {
  await page.evaluate(`document.dispatchEvent(new Event('visibilitychange')); dispatchEvent(new Event('focus')); true`);
  await sleep(1200);
  await page.waitIdle({ quiet: 400 });
};

async function screen(name, { path, tall = true, open, focus = true, variants = matrix(), curateAs = {}, afterEach }) {
  page.log(`== ${name} ${path}`);
  if (path) await page.spa(path);
  for (const v of variants) {
    try {
      const record = await checkVariant(page, results, name, v, {
        tall,
        open,
        axe: isPriority(v),
        focus: isPriority(v) ? focus : false,
        focusShot: isPriority(v),
      });
      const key = `${v.theme}-${v.lang}-${v.width}`;
      if (curateAs[key]) curate(results, record.shot, curateAs[key]);
      if (afterEach) await afterEach(v, record);
    } catch (error) {
      page.log(`  ${name} ${JSON.stringify(v)} ERROR ${error.message}`);
      results.note(`${name} ${JSON.stringify(v)}: ${error.message}`);
    }
  }
}

const clickText = (sel, re) => page.evaluate(`(() => { const e = ${textIs(sel, re)}; if (e) { e.click(); return true; } return false; })()`);
const isOpen = (sel) => page.evaluate(`!!document.querySelector(${JSON.stringify(sel)})`);
const escape = async () => {
  await page.key('Escape');
  await sleep(400);
};

try {
  const acc = accounts();
  await page.viewport(1440, 900);
  await page.signIn(acc.owner, `${S}/desk`);
  results.data.signedInAs = 'demo-owner';
  // How Chrome computes the oklch mixes (primary-hover's hue): probes on a scratch element.
  results.data.ec.oklchProbe = await page.evaluate(`(() => {
    const out = {};
    const probe = document.createElement('div');
    document.body.appendChild(probe);
    for (const [k, v] of Object.entries({
      'light primary-hover (oklch)': 'color-mix(in oklch, #1a1f25, #f7fbff 18%)',
      'dark primary-hover (oklch)': 'color-mix(in oklch, #f7fbff, #0d1217 18%)',
      'light primary-hover (oklab)': 'color-mix(in oklab, #1a1f25, #f7fbff 18%)',
      'dark primary-hover (oklab)': 'color-mix(in oklab, #f7fbff, #0d1217 18%)',
      'oklch(from #1a1f25)': 'oklch(from #1a1f25 l c h)',
      'oklch(from #f7fbff)': 'oklch(from #f7fbff l c h)',
      'secondary hover light (oklch, older)': 'color-mix(in oklch, #ecf4fc, #1a1f25 8%)',
      'overlay-scrim light (oklch)': 'color-mix(in oklch, #0d1217 50%, transparent)',
      'var(--primary-hover)': 'var(--primary-hover)',
    })) {
      probe.style.backgroundColor = '';
      probe.style.backgroundColor = v;
      const c = getComputedStyle(probe).backgroundColor;
      out[k] = c + ' = ' + window.__vp.hex(window.__vp.parse(c));
    }
    probe.remove();
    return out;
  })()`);
  page.log(`oklch probe ${JSON.stringify(results.data.ec.oklchProbe)}`);

  // ---- the desk, its rail at 768 in the matrix
  if (want('desk')) {
    await screen('desk', { path: `${S}/desk`, curateAs: { ...shotNames('12', 'desk'), 'light-ar-768': '13-owner-rail-light-ar-768.png' } });
  }
  // ---- the check-in dialog
  if (want('checkin')) {
    const openCheckIn = async () => {
      if (await isOpen('[role=dialog]')) return;
      await clickText('button', /^(Check in a visit|تسجيل دخول زيارة|.*زيارة)$/);
      await sleep(700);
      if (!(await isOpen('[role=dialog]'))) {
        // the phone: the action may sit in the page's action bar or a menu
        await page.evaluate(`(() => { const b = [...document.querySelectorAll('button')].find((e) => /Check in a visit|زيارة/.test(e.textContent) && window.__vp.visible(e)); b?.click(); return !!b; })()`);
        await sleep(700);
      }
    };
    await screen('checkin-dialog', {
      path: `${S}/desk`,
      tall: false,
      open: openCheckIn,
      focus: '[role=dialog]',
      variants: matrix({ full: false }).concat([{ theme: 'dark', lang: 'ar', width: 390 }, { theme: 'light', lang: 'en', width: 1440 }, { theme: 'light', lang: 'ar', width: 768 }]),
      curateAs: shotNames('14', 'check-in-dialog'),
    });
    await escape();
  }
  // ---- the overview
  if (want('overview')) await screen('overview', { path: S, curateAs: shotNames('15', 'owner-overview') });

  // ---- Payments: a range chosen in the date picker, then «إلغاء الدفعة» open
  if (want('payments')) {
    await page.viewport(1440, 900);
    await page.spa(`${S}/payments`);
    const chooseRange = async () => {
      await page.evaluate(`document.querySelector('[data-slot=date-picker-trigger]')?.click(); true`);
      await sleep(600);
      const days = await page.evaluate(`[...document.querySelectorAll('button[data-day]')].map((b) => b.getAttribute('data-day'))`);
      page.log(`  calendar days ${days[0]}..${days.at(-1)}`);
      await page.evaluate(`document.querySelector('button[data-day="2026-11-01"]')?.click(); true`);
      await sleep(300);
      await page.evaluate(`document.querySelector('button[data-day="2026-11-10"]')?.click(); true`);
      await sleep(900);
      await page.waitIdle();
      if (await isOpen('[data-slot=popover-content]')) await escape();
    };
    await chooseRange();
    const rows = await page.evaluate(`document.querySelectorAll('[data-slot=table-body] [data-slot=table-row]').length`);
    page.log(`  payments rows after the range: ${rows}; url ${await page.url()}`);
    results.note(`payments rows with the range 1–10 Nov: ${rows}`);
    await screen('payments', { path: null, variants: matrix({ full: false }).concat([{ theme: 'dark', lang: 'ar', width: 768 }]), curateAs: shotNames('16', 'payments') });
    // The date picker, open on its range.
    const openPicker = async () => {
      if (await isOpen('[data-slot=popover-content]')) return;
      await page.evaluate(`document.querySelector('[data-slot=date-picker-trigger]')?.click(); true`);
      await sleep(700);
    };
    await screen('datepicker-range', {
      path: null,
      tall: false,
      open: openPicker,
      focus: '[data-slot=popover-content]',
      variants: matrix({ full: false }).concat([{ theme: 'dark', lang: 'ar', width: 1440 }]),
      curateAs: shotNames('17', 'date-picker-range'),
    });
    // §5: today in the calendar beside a day of the range, 1440 light and dark.
    for (const theme of ['light', 'dark']) {
      await page.viewport(1440, 900);
      await page.prefs(theme, 'en');
      await openPicker();
      await hoverTest(page, results, 'today in the calendar (beside a range day)', {
        target: `document.querySelector('[data-slot=popover-content] button[aria-current=date]')`,
        selected: `document.querySelector('[data-slot=popover-content] button[data-range-middle]')`,
        kind: 'wash',
        sample: (r) => ({ x: r.left + 3, y: r.top + r.h / 2 }),
        shotName: `26-hover-calendar-today-${theme}.png`,
      });
      await hoverTest(page, results, 'calendar range end (filled) hovered', {
        target: `document.querySelector('[data-slot=popover-content] button[data-range-end]')`,
        kind: 'primary',
        sample: (r) => ({ x: r.left + 3, y: r.top + r.h / 2 }),
      });
      await escape();
    }
    // The void dialog from a row's menu.
    const openVoid = async () => {
      if (await isOpen('[role=alertdialog]')) return;
      const trigger = await page.evaluate(`(() => { const t = [...document.querySelectorAll('[data-slot=table-body] [data-slot=dropdown-menu-trigger]')].find((e) => window.__vp.visible(e)); if (!t) return false; t.focus(); return true; })()`);
      if (!trigger) return;
      await page.key('Enter');
      await sleep(500);
      await clickText('[role=menuitem]', /(إلغاء الدفعة|Void payment)/);
      await sleep(700);
    };
    if (rows > 0) {
      await screen('void-dialog', {
        path: null,
        tall: false,
        open: openVoid,
        focus: '[role=alertdialog]',
        variants: matrix({ full: false }).concat([{ theme: 'dark', lang: 'ar', width: 390 }, { theme: 'light', lang: 'en', width: 1440 }]),
        curateAs: shotNames('18', 'void-payment-dialog'),
      });
      await escape();
      // §5: a payments row and a sort header, 1440.
      for (const theme of ['light', 'dark']) {
        await page.viewport(1440, 900);
        await page.prefs(theme, 'en');
        await hoverTest(page, results, 'payments row', { target: `document.querySelector('[data-slot=table-body] [data-slot=table-row]')`, sample: (r) => ({ x: r.left + r.w / 2, y: r.top + 3 }) });
        await hoverTest(page, results, 'sort header (payments)', {
          target: `[...document.querySelectorAll('[data-slot=table-head] button')].find((b) => window.__vp.visible(b))`,
          kind: 'wash',
          sample: (r) => ({ x: r.left + 3, y: r.top + 3 }),
          shotName: `27-hover-sort-header-${theme}.png`,
        });
      }
    } else {
      results.note('payments: no row in 1–10 Nov; the void dialog not reached');
    }
  }

  // ---- the space profile: «+N», a Sheet (the contacts), a contact and a photo lifted
  if (want('profile')) {
    await screen('profile', { path: `${S}/profile`, curateAs: { ...shotNames('19', 'owner-profile'), 'light-en-768': '19-owner-profile-photos-plus-n-light-en-768.png' } });
    results.note(`profile photos padded to seven by the response: ${photosPadded}`);
    const plusN = await page.evaluate(`[...document.querySelectorAll('main *')].filter((e) => /^\\+\\s?\\d+$|^\\+[\\u0660-\\u0669\\d]+$/.test(e.textContent.trim()) && e.children.length === 0).map((e) => window.__vp.describe(e))`);
    results.data.ec.plusN = plusN;
    page.log(`  +N elements: ${JSON.stringify(plusN).slice(0, 600)}`);
    const openContacts = async () => {
      if (await isOpen('[data-slot=sheet-content]')) return;
      await page.evaluate(`(() => { const b = [...document.querySelectorAll('button[aria-label]')].find((e) => /Contacts|جهات التواصل|التواصل/.test(e.getAttribute('aria-label')) && window.__vp.visible(e)); b?.click(); return !!b; })()`);
      await sleep(900);
    };
    await screen('contacts-sheet', {
      path: null,
      tall: false,
      open: openContacts,
      focus: '[data-slot=sheet-content]',
      variants: matrix({ full: false }).concat([{ theme: 'dark', lang: 'ar', width: 768 }, { theme: 'light', lang: 'en', width: 1440 }]),
      curateAs: shotNames('20', 'contacts-sheet'),
    });
    // A contact lifted by the keyboard: Space on its handle, then Escape (nothing saved).
    for (const theme of ['light', 'dark']) {
      await page.viewport(1440, 900);
      await page.prefs(theme, 'en');
      await openContacts();
      const handle = `[...document.querySelectorAll('[data-slot=sheet-content] .cursor-grab')].find((e) => window.__vp.visible(e))`;
      const ok = await page.evaluate(`(() => { const h = ${handle}; if (!h) return false; h.focus(); return document.activeElement === h; })()`);
      await page.key(' ');
      await sleep(500);
      const lifted = await page.evaluate(`(() => {
        const h = ${handle};
        const item = h?.closest('li, [data-slot=sortable-item], [role=listitem]') ?? h?.parentElement;
        const all = [...document.querySelectorAll('[data-slot=sheet-content] *')].filter((e) => { const cs = getComputedStyle(e); return cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) > 0; }).map((e) => ({ el: window.__vp.sel(e), outline: getComputedStyle(e).outlineStyle + ' ' + getComputedStyle(e).outlineWidth + ' ' + window.__vp.hex(window.__vp.parse(getComputedStyle(e).outlineColor)) }));
        const bordered = [...document.querySelectorAll('[data-slot=sheet-content] *')].filter((e) => window.__vp.hex(window.__vp.parse(getComputedStyle(e).borderTopColor)) === '${TOKENS[theme].spark}' && parseFloat(getComputedStyle(e).borderTopWidth) > 0).map((e) => window.__vp.sel(e));
        return { handleFocused: document.activeElement === h, handle: h && window.__vp.describe(h), item: item && window.__vp.describe(item), outlines: all.slice(0, 6), sparkEdges: bordered.slice(0, 6), live: [...document.querySelectorAll('[aria-live], [role=status]')].map((e) => e.textContent.trim()).filter(Boolean).slice(0, 3) };
      })()`);
      const file = `${RAW}/own-contact-lifted-keyboard-${theme}.png`;
      await page.shot(file);
      curate(results, file, `28-contact-lifted-keyboard-${theme}-en-1440.png`);
      await page.key('Escape');
      await sleep(500);
      const after = await page.evaluate(`({ sheetOpen: !!document.querySelector('[data-slot=sheet-content]'), focused: window.__vp.sel(document.activeElement) })`);
      results.data.ec[`contactLifted-${theme}`] = { focused: ok, lifted, after };
      page.log(`  contact lifted (${theme}): ${JSON.stringify({ ok, lifted, after }).slice(0, 900)}`);
    }
    if (await isOpen('[data-slot=sheet-content]')) await escape();
    // The photos editor: a photo lifted by the keyboard, then by a mouse drag (cancelled).
    for (const theme of ['light', 'dark']) {
      await page.viewport(1440, 900);
      await page.prefs(theme, 'en');
      if (!(await isOpen('[data-slot=sheet-content]'))) {
        await clickText('button', /^(Manage photos|إدارة الصور)$/);
        await sleep(1000);
        await page.waitIdle();
      }
      const tileSel = `[...document.querySelectorAll('.cursor-grab')].filter((e) => window.__vp.visible(e) && e.closest('[data-slot=sheet-content], main'))[1]`;
      const info = async (how) =>
        page.evaluate(`(() => {
          const t = ${tileSel};
          if (!t) return null;
          const cs = getComputedStyle(t);
          const r = t.getBoundingClientRect();
          const o = parseFloat(cs.outlineWidth) + parseFloat(cs.outlineOffset || 0);
          const clippers = [];
          for (let n = t.parentElement; n && n !== document.body; n = n.parentElement) {
            const ns = getComputedStyle(n);
            if (ns.overflow !== 'visible' || ns.overflowX !== 'visible' || ns.clipPath !== 'none') {
              const nr = n.getBoundingClientRect();
              if (nr.left > r.left - o || nr.top > r.top - o || nr.right < r.right + o || nr.bottom < r.bottom + o) clippers.push({ el: window.__vp.sel(n), overflow: ns.overflow, rect: [nr.left, nr.top, nr.right, nr.bottom].map(Math.round) });
            }
          }
          return { how: ${JSON.stringify(how)}, el: window.__vp.sel(t), focused: document.activeElement === t, focusVisible: t.matches(':focus-visible'), cls: t.getAttribute('class'), outline: cs.outlineStyle + ' ' + cs.outlineWidth + ' ' + window.__vp.hex(window.__vp.parse(cs.outlineColor)) + ' offset ' + cs.outlineOffset, rect: [r.left, r.top, r.width, r.height].map(Math.round), clippedBy: clippers, ring: window.__vp.hex(window.__vp.parse(window.__vp.token('ring'))), spark: window.__vp.hex(window.__vp.parse(window.__vp.token('spark'))) };
        })()`);
      const rest = await info('rest');
      if (!rest) {
        results.note(`photos editor: no draggable tile found (${theme})`);
        page.log('  photos: no tile');
        continue;
      }
      await page.evaluate(`(() => { const t = ${tileSel}; t.scrollIntoView({ block: 'center' }); t.focus(); return true; })()`);
      await page.key(' ');
      await sleep(500);
      const keyboard = await info('keyboard lift');
      const r = keyboard.rect;
      const clip = { x: Math.max(0, r[0] - 24), y: Math.max(0, r[1] - 24), width: r[2] + 48, height: r[3] + 48 };
      const kfile = `${RAW}/own-photo-lifted-keyboard-${theme}.png`;
      await page.shot(kfile, clip);
      curate(results, kfile, `29-photo-lifted-keyboard-${theme}-en-1440.png`);
      const kimg = decodePng(await page.shot());
      const edge = [pixel(kimg, r[0] + r[2] / 2, r[1] - 3), pixel(kimg, r[0] - 3, r[1] + r[3] / 2)].map(hex);
      await page.key('Escape');
      await sleep(500);
      // A mouse drag: pressed, moved past the activation distance, read, cancelled by Escape, released where it began.
      const t2 = await info('before drag');
      const cx = t2.rect[0] + t2.rect[2] / 2;
      const cy = t2.rect[1] + t2.rect[3] / 2;
      await page.mouse(cx, cy, 'mouseMoved');
      await page.mouse(cx, cy, 'mousePressed', { button: 'left', buttons: 1, clickCount: 1 });
      for (let i = 1; i <= 6; i += 1) {
        await page.send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: cx + i * 6, y: cy + i * 3, button: 'left', buttons: 1, pointerType: 'mouse' });
        await sleep(60);
      }
      await sleep(300);
      const mouse = await info('mouse drag');
      const mfile = `${RAW}/own-photo-lifted-mouse-${theme}.png`;
      await page.shot(mfile, { x: Math.max(0, mouse.rect[0] - 24), y: Math.max(0, mouse.rect[1] - 24), width: mouse.rect[2] + 48, height: mouse.rect[3] + 48 });
      if (theme === 'light') curate(results, mfile, `30-photo-lifted-mouse-${theme}-en-1440.png`);
      await page.key('Escape');
      await page.send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: cx, y: cy, button: 'left', buttons: 1, pointerType: 'mouse' });
      await page.mouse(cx, cy, 'mouseReleased', { button: 'left', buttons: 0, clickCount: 1 });
      await sleep(500);
      results.data.ec[`photoLifted-${theme}`] = { rest, keyboard, keyboardEdgePixels: edge, mouse };
      page.log(`  photo lifted (${theme}): keyboard ${keyboard.outline} focusVisible ${keyboard.focusVisible} clipped ${JSON.stringify(keyboard.clippedBy)} edge px ${edge}; mouse ${mouse.outline}`);
    }
    if (await isOpen('[data-slot=sheet-content]')) await escape();
  }

  // ---- Finance: the income charts, then the occupancy heatmap
  if (want('finance')) {
    await screen('finance-income', { path: `${S}/finance`, curateAs: shotNames('21', 'finance-charts') });
    const toOccupancy = async () => {
      const on = await page.evaluate(`!!document.querySelector('[data-slot=heatmap]')`);
      if (!on) {
        const tab = await page.evaluate(`(() => { const t = [...document.querySelectorAll('[role=tab]')].find((e) => /Occupancy|الإشغال/.test(e.textContent)); if (!t) return false; t.focus(); return true; })()`);
        if (tab) {
          await page.key('Enter');
          await sleep(300);
          await page.evaluate(`(() => { const t = [...document.querySelectorAll('[role=tab]')].find((e) => /Occupancy|الإشغال/.test(e.textContent)); t?.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true, button: 0 })); t?.dispatchEvent(new MouseEvent('mousedown', { bubbles: true })); t?.click(); return true; })()`);
        }
        await sleep(900);
        await page.waitIdle();
      }
    };
    await screen('finance-heatmap', { path: null, open: toOccupancy, curateAs: shotNames('22', 'finance-heatmap') });
    // §5: the desktop tabs (pill, on muted).
    for (const theme of ['light', 'dark']) {
      await page.viewport(1440, 900);
      await page.prefs(theme, 'en');
      await hoverTest(page, results, 'desktop tabs (finance)', {
        target: `document.querySelector('[data-slot=tabs-trigger][data-state=inactive]')`,
        selected: `document.querySelector('[data-slot=tabs-trigger][data-state=active]')`,
        kind: 'wash',
        selectedKind: 'card',
        sample: (r) => ({ x: r.left + 4, y: r.top + 3 }),
        shotName: `31-hover-desktop-tabs-${theme}.png`,
      });
    }
  }

  // ---- the drawer at 390 (the owner's sidebar in its sheet)
  if (want('drawer')) {
    await page.spa(`${S}/desk`);
    const openDrawer = async () => {
      if (await isOpen('[data-slot=sheet-content]')) return;
      await page.evaluate(`document.querySelector('[data-slot=sidebar-trigger]')?.click(); true`);
      await sleep(800);
    };
    await screen('owner-drawer', {
      path: null,
      tall: false,
      open: openDrawer,
      focus: '[data-slot=sheet-content]',
      variants: [{ theme: 'light', lang: 'ar', width: 390 }, { theme: 'dark', lang: 'en', width: 390 }, { theme: 'dark', lang: 'ar', width: 390 }, { theme: 'light', lang: 'en', width: 390 }],
      curateAs: { 'light-ar-390': '32-owner-drawer-light-ar-390.png', 'dark-en-390': '32-owner-drawer-dark-en-390.png' },
    });
    await escape();
  }

  // ---- §5 the owner's hover set on the desk, 1440 light and dark; LiveStatusControl's tones; EC3
  if (want('hover')) {
    for (const theme of ['light', 'dark']) {
      await page.viewport(1440, 900);
      await page.spa(`${S}/desk`);
      await page.prefs(theme, 'en');
      await hoverTest(page, results, 'desk row (present now)', {
        target: `document.querySelector('[data-slot=tabs-content][data-state=active] [data-slot=table-body] [data-slot=table-row]')`,
        sample: (r) => ({ x: r.left + r.w - 20, y: r.top + 3 }),
        shotName: `33-hover-desk-row-${theme}.png`,
      });
      await hoverTest(page, results, 'sidebar item beside the current one', {
        target: `[...document.querySelectorAll('[data-slot=sidebar-menu-button]:not([data-active=true])')].find((e) => /Customers|الزبائن/.test(e.textContent))`,
        selected: `document.querySelector('[data-slot=sidebar-menu-button][data-active=true]')`,
        sample: (r) => ({ x: r.left + r.w - 10, y: r.top + 3 }),
        shotName: `34-hover-sidebar-${theme}.png`,
      });
      await hoverTest(page, results, 'chip beside a chip that is on (uncollected)', {
        target: `document.querySelector('[data-slot=toggle-group-item][data-state=off]')`,
        selected: `document.querySelector('[data-slot=toggle-group-item][data-state=on]')`,
      });
      await hoverTest(page, results, 'outline button (Switch staff)', { target: textIs('button', /^(Switch staff|تبديل الموظف)$/) });
      await hoverTest(page, results, 'primary button (Check in a visit)', { target: textIs('button', /^(Check in a visit|تسجيل زيارة)$/), kind: 'primary', shotName: `35-hover-primary-${theme}.png` });
      await hoverTest(page, results, 'line tabs (Now/Log)', {
        target: `document.querySelector('[data-slot=tabs-trigger][data-state=inactive]')`,
        selected: `document.querySelector('[data-slot=tabs-trigger][data-state=active]')`,
        selectedKind: 'line',
      });
      // A menu item, the account menu opened by Enter.
      await page.evaluate(`document.querySelector('[data-slot=dropdown-menu-trigger][aria-label^="Account"], [data-slot=dropdown-menu-trigger][aria-label*="الحساب"]')?.focus(); true`);
      await page.key('Enter');
      await sleep(600);
      await hoverTest(page, results, 'menu item (account menu)', {
        target: `[...document.querySelectorAll('[role=menuitem]')].filter((e) => window.__vp.visible(e))[1]`,
        selected: `[...document.querySelectorAll('[role=menuitem]')].find((e) => e.hasAttribute('data-highlighted'))`,
        selectedKind: 'highlighted',
        shotName: `36-hover-menu-item-${theme}.png`,
      });
      await escape();
      // EC3: the dark accent, painted (the sidebar's current item at rest).
      const cur = await page.evaluate(`(() => { const e = document.querySelector('[data-slot=sidebar-menu-button][data-active=true]'); const r = e.getBoundingClientRect(); return { x: r.right - 12, y: r.top + 3, bar: window.__vp.styleOf(e, '::before') }; })()`);
      await page.mouse(2, 2);
      await sleep(400);
      const img = decodePng(await page.shot());
      results.data.ec[`accent-${theme}`] = { at: [cur.x, cur.y], painted: hex(pixel(img, cur.x, cur.y)), bar: cur.bar };
      page.log(`  EC3 accent ${theme}: ${hex(pixel(img, cur.x, cur.y))} bar ${JSON.stringify(cur.bar)}`);
      // LiveStatusControl, each tone, hovered.
      for (const mode of ['people', 'full', 'closed']) {
        occupancyMode = mode;
        await refetchNow();
        await hoverTest(page, results, `live status control (${mode === 'people' ? 'success' : mode === 'full' ? 'warning' : 'neutral'} tone)`, {
          target: `document.querySelector('[data-slot=popover-trigger]')`,
          kind: 'tone',
          sample: (r) => ({ x: r.left + 4, y: r.top + 4 }),
          shotName: `37-hover-live-status-${mode}-${theme}.png`,
        });
      }
      occupancyMode = 'people';
      await refetchNow();
    }
  }

  // ---- the site, signed in: /me, the favourites, the phone menu, the header at 360
  if (want('site')) {
    await screen('me', { path: '/me', curateAs: shotNames('38', 'me') });
    await screen('favorites', { path: '/me/favorites', curateAs: { 'light-ar-390': '39-favorites-light-ar-390.png' } });
    // §5 on /me: a chip beside the chip that is on (language, theme), 1440.
    for (const theme of ['light', 'dark']) {
      await page.viewport(1440, 900);
      await page.spa('/me');
      await page.prefs(theme, 'en');
      await hoverTest(page, results, 'chip beside a chip that is on (/me theme)', {
        target: `[...document.querySelectorAll('[data-slot=toggle-group-item][data-state=off]')].pop()`,
        selected: `[...document.querySelectorAll('[data-slot=toggle-group-item][data-state=on]')].pop()`,
        shotName: `40-hover-chip-me-${theme}.png`,
      });
    }
    // The phone menu signed in: its current page's entry under the pointer (SiteMenu).
    const openMenu = async () => {
      if (await isOpen('[data-slot=sheet-content]')) return;
      await page.evaluate(`document.querySelector('header [data-slot=sheet-trigger]')?.click(); true`);
      await sleep(800);
    };
    await page.spa('/spaces');
    await screen('phonemenu-signed-in', {
      path: null,
      tall: false,
      open: openMenu,
      focus: '[data-slot=sheet-content]',
      variants: [{ theme: 'light', lang: 'ar', width: 390 }, { theme: 'dark', lang: 'en', width: 390 }, { theme: 'light', lang: 'en', width: 360 }, { theme: 'dark', lang: 'ar', width: 360 }],
      curateAs: { 'light-ar-390': '41-phone-menu-signed-in-light-ar-390.png' },
    });
    for (const theme of ['light', 'dark']) {
      await page.viewport(390, HEIGHTS[390]);
      await page.prefs(theme, 'en');
      await openMenu();
      await hoverTest(page, results, 'phone menu: the current page entry vs another', {
        target: `[...document.querySelectorAll('[data-slot=sheet-content] nav a:not([aria-current=page])')][0]`,
        selected: `document.querySelector('[data-slot=sheet-content] nav a[aria-current=page]')`,
        selectedKind: 'secondary',
        shotName: `42-hover-phone-menu-current-${theme}.png`,
      });
      await escape();
    }
    // EC14 signed in: the header at 360 with the avatar.
    const ec14 = [];
    for (const lang of ['ar', 'en']) {
      for (const theme of ['light', 'dark']) {
        await page.viewport(360, HEIGHTS[360]);
        await page.prefs(theme, lang);
        const header = await page.evaluate(`(() => {
          const row = document.querySelector('header').firstElementChild;
          const kids = [...row.querySelectorAll('button, a')].filter((e) => window.__vp.visible(e)).map((e) => { const r = e.getBoundingClientRect(); return { el: window.__vp.sel(e).split(' > ').pop(), left: Math.round(r.left), right: Math.round(r.right), w: Math.round(r.width) }; });
          const overlaps = [];
          for (let i = 0; i < kids.length; i += 1) for (let j = i + 1; j < kids.length; j += 1) if (kids[i].left < kids[j].right - 1 && kids[j].left < kids[i].right - 1) overlaps.push([kids[i].el, kids[j].el]);
          return { scrollWidth: document.documentElement.scrollWidth, clientWidth: document.documentElement.clientWidth, rowScroll: row.scrollWidth, rowClient: row.clientWidth, kids, overlaps, outside: kids.filter((k) => k.left < 0 || k.right > 360) };
        })()`);
        const file = `${RAW}/own-header360-${theme}-${lang}.png`;
        await page.shot(file, { x: 0, y: 0, width: 360, height: 72 });
        if (theme === 'dark') curate(results, file, `43-header-360-signed-in-${lang}-dark.png`);
        ec14.push({ who: 'signed in', theme, lang, ...header, ok: header.scrollWidth <= header.clientWidth && header.rowScroll <= header.rowClient && !header.overlaps.length && !header.outside.length });
        page.log(`  EC14 signed in ${theme}-${lang}: ${JSON.stringify(ec14.at(-1)).slice(0, 500)}`);
      }
    }
    results.data.ec.ec14 = ec14;
  }
  page.log(`refreshes ${page.refreshes}, loads ${page.loads}, blocked ${JSON.stringify(page.blocked)}`);
  results.data.blocked = page.blocked;
  results.data.loads = page.loads;
  results.data.refreshes = page.refreshes;
} catch (error) {
  page.log(`ERROR ${error.stack}`);
  results.note(`ERROR ${error.message}`);
} finally {
  results.save();
  results.data.chrome = await page.close();
  results.save();
}
