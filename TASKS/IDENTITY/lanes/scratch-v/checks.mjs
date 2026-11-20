// The checks run on each load (VISUAL.md §4), the hover test (§5) and the pixel samples (EC3).
import { copyFileSync, writeFileSync } from 'node:fs';
import { decodePng, hex, parseHex, pixel, RAW, SHOTS, sleep, within } from './lib.mjs';

export const HEIGHTS = { 360: 780, 390: 844, 768: 1024, 1440: 900 };
export const TOKENS = {
  light: { hover: '#dde5ed', wash: '#d7dfe6', muted: '#ecf4fc', accent: '#ffe3fd', ring: '#1a1f25', spark: '#b55bb3', primaryHover: '#3c4147', primary: '#1a1f25' },
  dark: { hover: '#2c3137', wash: '#3c4147', muted: '#2c3137', accent: '#471f46', ring: '#f7fbff', spark: '#d27ed0', primaryHover: '#c7cbd0', primary: '#f7fbff' },
};

export class Results {
  constructor(run) {
    this.run = run;
    this.file = `C:/dev/masaha/workspace/TASKS/IDENTITY/lanes/scratch-v/results-${run}.json`;
    this.data = { run, screens: {}, hover: [], ec: {}, notes: [], shots: [] };
  }
  screen(name) {
    this.data.screens[name] = this.data.screens[name] ?? { variants: {}, axe: {}, focus: {} };
    return this.data.screens[name];
  }
  note(text) {
    this.data.notes.push(text);
  }
  save() {
    writeFileSync(this.file, JSON.stringify(this.data, null, 1));
  }
}

/** Copies a raw shot to the owner's folder under a curated name. */
export function curate(results, raw, name) {
  copyFileSync(raw, `${SHOTS}/${name}`);
  results.data.shots.push(name);
}

/** Texts over a photo or a map: their ground read from the screen, the text hidden. */
async function imageContrast(page, images) {
  if (!images.length) return [];
  await page.evaluate(`(() => { const s = document.createElement('style'); s.id = '__vp_hide'; s.textContent = '*, *::before, *::after { transition: none !important; color: transparent !important; -webkit-text-fill-color: transparent !important; text-shadow: none !important; }'; document.head.appendChild(s); return true; })()`);
  await sleep(120);
  const img = decodePng(await page.shot());
  await page.evaluate(`(() => { const s = document.getElementById('__vp_hide'); s.textContent = '*, *::before, *::after { transition: none !important; }'; void document.body.offsetHeight; return true; })()`);
  await sleep(80);
  await page.evaluate(`document.getElementById('__vp_hide')?.remove(); true`);
  await sleep(300);
  const lum = ([r, g, b]) => {
    const f = (v) => {
      const c = v / 255;
      return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
    };
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
  };
  const out = [];
  for (const item of images) {
    const [x, y, w, h] = item.rect;
    const fg = parseHex(item.fg);
    const ratios = [];
    for (let yy = Math.max(0, y); yy < Math.min(img.height, y + h); yy += 1) {
      for (let xx = Math.max(0, x); xx < Math.min(img.width, x + w); xx += 1) {
        const p = pixel(img, xx, yy);
        const a = item.fgAlpha;
        const shown = fg.map((c, i) => c * a + p[i] * (1 - a));
        const [hi, lo] = [lum(shown), lum(p)].sort((m, n) => n - m);
        ratios.push((hi + 0.05) / (lo + 0.05));
      }
    }
    ratios.sort((m, n) => m - n);
    if (!ratios.length) continue;
    const min = ratios[0];
    const p10 = ratios[Math.floor(ratios.length * 0.1)];
    const median = ratios[Math.floor(ratios.length / 2)];
    out.push({ ...item, minRatio: +min.toFixed(2), p10: +p10.toFixed(2), median: +median.toFixed(2), fails: p10 < item.min });
  }
  return out;
}

/** Three Tabs from the start of `root` (the page, a dialog, a sheet): what holds the focus, and its ring. */
export async function focusProbe(page, rootSelector = null) {
  await page.evaluate(`(() => {
    document.getElementById('__vp_probe')?.remove();
    const root = ${rootSelector ? (rootSelector.startsWith('js:') ? `(${rootSelector.slice(3)})` : `document.querySelector(${JSON.stringify(rootSelector)})`) : 'null'} ?? document.body;
    const probe = document.createElement('span');
    probe.id = '__vp_probe'; probe.tabIndex = -1; probe.style.cssText = 'position:absolute;width:1px;height:1px;overflow:hidden';
    root.insertBefore(probe, root.firstChild);
    probe.focus();
    return document.activeElement === probe;
  })()`);
  const steps = [];
  for (let i = 0; i < 3; i += 1) {
    await page.key('Tab');
    await sleep(150);
    steps.push(await page.vp('focusInfo'));
  }
  await page.evaluate(`document.getElementById('__vp_probe')?.remove(); true`);
  const last = steps[2];
  const theme = await page.evaluate('document.documentElement.dataset.theme');
  const ringOk =
    last.el !== 'body' &&
    last.outline.style !== 'none' &&
    last.outline.width === '2px' &&
    (last.outline.color === last.ring || last.outline.color === last.sidebarRing);
  return { steps, ok: ringOk && last.inView && last.focusVisible, theme };
}

/**
 * One variant of a screen: the viewport, the preferences, then every check of §4. `open` re-opens an
 * overlay the change closed. Returns the variant's record.
 */
export async function checkVariant(page, results, name, v, opts = {}) {
  const { theme, lang, width } = v;
  const key = `${theme}-${lang}-${width}`;
  const base = HEIGHTS[width];
  await page.viewport(width, base);
  await page.prefs(theme, lang);
  if (opts.open) await opts.open(v);
  await page.waitIdle({ quiet: 400 });
  await sleep(opts.settle ?? 250);
  let height = base;
  if (opts.tall) {
    const full = await page.evaluate('Math.max(document.documentElement.scrollHeight, document.body.scrollHeight)');
    height = Math.min(Math.max(full, base), 7000);
    if (height !== base) {
      await page.viewport(width, height);
      await sleep(350);
    }
  }
  const record = { key, height };
  record.overflow = await page.vp('overflow');
  record.sea = await page.vp('seaScan');
  record.spark = await page.vp('sparkScan');
  const contrast = await page.vp('contrastScan');
  record.logo = await page.vp('logoScan');
  record.status = await page.vp('statusScan');
  const file = `${RAW}/${results.run}-${name}-${key}.png`;
  await page.shot(file);
  record.shot = file;
  contrast.images = await imageContrast(page, contrast.images);
  record.contrast = contrast;
  if (opts.axe) {
    record.axe = await page.axe();
    results.screen(name).axe[key] = record.axe;
  }
  if (opts.focus !== undefined && opts.focus !== false) {
    record.focus = await focusProbe(page, opts.focus === true ? null : opts.focus);
    results.screen(name).focus[key] = record.focus;
    if (opts.focusShot) {
      const focusFile = `${RAW}/${results.run}-${name}-${key}-focus.png`;
      await page.shot(focusFile);
      record.focusShot = focusFile;
    }
    await page.evaluate('document.activeElement && document.activeElement !== document.body && document.activeElement.blur && document.activeElement.blur(); true');
  }
  record.console = page.takeConsole();
  if (height !== base) await page.viewport(width, base);
  results.screen(name).variants[key] = record;
  results.save();
  const flags = [
    record.overflow.over && 'OVERFLOW',
    record.sea.hitCount && `SEA ${record.sea.hitCount}`,
    record.sea.sheetHits.length && `SEA-SHEET ${record.sea.sheetHits.length}`,
    record.spark.textHits.length && `SPARK-TEXT ${record.spark.textHits.length}`,
    record.spark.buttonHits.length && `SPARK-BUTTON ${record.spark.buttonHits.length}`,
    contrast.failures.length && `CONTRAST ${contrast.failures.length}`,
    contrast.images.some((i) => i.fails) && 'CONTRAST-IMAGE',
    record.status.mismatches.length && `STATUS ${record.status.mismatches.length}`,
    record.status.tokenMismatch.length && 'STATUS-TOKEN',
    record.axe?.length && `AXE ${record.axe.map((a) => a.id).join(',')}`,
    record.focus && !record.focus.ok && 'FOCUS',
    record.console.length && `CONSOLE ${record.console.length}`,
  ].filter(Boolean);
  page.log(`  ${name} ${key}: ${flags.join(' | ') || 'clean'} (checked ${contrast.checked} texts, ${record.sea.elements} elements)`);
  return record;
}

/** The variants of the matrix, the priority pair first. */
export function matrix({ widths = [390, 768, 1440], full = true } = {}) {
  const priority = [
    { theme: 'light', lang: 'ar', width: 390 },
    { theme: 'dark', lang: 'en', width: 1440 },
  ].filter((v) => widths.includes(v.width));
  if (!full) return priority;
  const rest = [];
  for (const width of widths) {
    for (const lang of ['ar', 'en']) {
      for (const theme of ['light', 'dark']) {
        if (!priority.some((p) => p.theme === theme && p.lang === lang && p.width === width)) rest.push({ theme, lang, width });
      }
    }
  }
  return [...priority, ...rest];
}

/** Moves a real pointer onto an element; returns its centre. `expr` is JS returning the element. */
async function rectOfExpr(page, expr) {
  return page.evaluate(`(() => { const el = (${expr}); if (!el) return null; el.scrollIntoView({ block: 'center', inline: 'nearest' }); const r = el.getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2, left: r.left, top: r.top, w: r.width, h: r.height }; })()`);
}
const describeExpr = (page, expr) => page.evaluate(`(() => { const el = (${expr}); return el ? window.__vp.describe(el) : null; })()`);

/**
 * §5: the rest, hovered and selected fills of an item and the selected one beside it, with a real
 * pointer. `kind`: 'hover' (expects the neutral hover) or 'wash' (the ink's wash over muted).
 */
export async function hoverTest(page, results, label, { target, selected = null, kind = 'hover', selectedKind = 'accent', shotName = null, pad = 24, sample = null }) {
  const theme = await page.evaluate('document.documentElement.dataset.theme');
  const lang = await page.evaluate('document.documentElement.lang');
  const t = TOKENS[theme];
  await page.mouse(2, 2);
  await sleep(450);
  const rect = await rectOfExpr(page, target);
  if (!rect) {
    const miss = { label, theme, lang, missing: target };
    results.data.hover.push(miss);
    page.log(`  hover ${label} (${theme}): target missing`);
    return miss;
  }
  await sleep(250);
  const rest = await describeExpr(page, target);
  const selRest = selected ? await describeExpr(page, selected) : null;
  const r2 = await rectOfExpr(page, target);
  await page.mouse(r2.x, r2.y);
  await sleep(500);
  const hovered = await describeExpr(page, target);
  let pixelSample = null;
  let shot = null;
  const selRect = selected ? await rectOfExpr(page, selected) : null;
  // A shot of the pair, the target hovered.
  {
    const boxes = [r2, selRect].filter(Boolean);
    const x0 = Math.max(0, Math.min(...boxes.map((b) => b.left)) - pad);
    const y0 = Math.max(0, Math.min(...boxes.map((b) => b.top)) - pad);
    const x1 = Math.min(page.width, Math.max(...boxes.map((b) => b.left + b.w)) + pad);
    const y1 = Math.min(page.height, Math.max(...boxes.map((b) => b.top + b.h)) + pad);
    const file = `${RAW}/${results.run}-hover-${label.replace(/[^a-z0-9]+/gi, '-')}-${theme}-${lang}.png`;
    // The hovered target's own pixel (EC3): a point inside its fill, away from its words.
    const full = decodePng(await page.shot());
    const sx = sample ? sample(r2) : { x: r2.left + r2.w / 2, y: r2.top + 3 };
    pixelSample = { at: [Math.round(sx.x), Math.round(sx.y)], hex: hex(pixel(full, sx.x, sx.y)) };
    await page.shot(file, { x: x0, y: y0, width: x1 - x0, height: y1 - y0 });
    shot = file;
    if (shotName) curate(results, file, shotName);
  }
  let selHover = null;
  if (selRect) {
    await page.mouse(selRect.x, selRect.y);
    await sleep(500);
    selHover = await describeExpr(page, selected);
  }
  await page.mouse(2, 2);
  await sleep(300);
  const want = kind === 'wash' ? t.wash : kind === 'primary' ? t.primaryHover : t.hover;
  const hoverPainted = hovered.painted;
  const verdict = {
    hoverIsToken: hoverPainted === want || hovered.bgHex === want,
    hoverChanged: hoverPainted !== rest.painted,
    selectedKeeps: selRest ? selRest.painted === selHover.painted && selRest.bgHex === selHover.bgHex : null,
    selectedIsAccent: selRest ? selRest.bgHex === t.accent : null,
    differ: selRest ? selRest.painted !== hoverPainted : null,
  };
  const record = { label, theme, lang, kind, want, rest, hovered, selRest, selHover, verdict, pixelSample, shot };
  results.data.hover.push(record);
  results.save();
  page.log(
    `  hover ${label} (${theme}/${lang}): rest ${rest.painted} -> hover ${hoverPainted} (bg ${hovered.bg}) want ${want}${selRest ? `; selected ${selRest.painted}/${selRest.bgHex} -> under pointer ${selHover.painted}` : ''} :: ${JSON.stringify(verdict)}`,
  );
  return record;
}

export { within, parseHex };
