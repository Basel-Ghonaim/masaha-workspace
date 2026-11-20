// The owner, third pass: why the occupancy heatmap's page is wider than 390 (each suspect hidden in
// turn, the page's width read again).
import { accounts, launch, sleep } from './lib.mjs';
import { HEIGHTS, Results } from './checks.mjs';

const page = await launch('own3');
const results = new Results('own3');
try {
  await page.viewport(1440, 900);
  await page.signIn(accounts().owner, '/dashboard/spaces/26/finance');
  await page.viewport(390, HEIGHTS[390]);
  for (const lang of ['ar', 'en']) {
    await page.prefs('light', lang);
    await page.evaluate(`(() => { const t = [...document.querySelectorAll('[role=tab]')].find((e) => /Occupancy|الإشغال/.test(e.textContent)); t?.focus(); return !!t; })()`);
    await page.key('Enter');
    await sleep(1200);
    await page.waitIdle();
    const probe = await page.evaluate(`(() => {
      const d = document.documentElement;
      const width = () => d.scrollWidth;
      const out = { start: width(), client: d.clientWidth, suspects: [] };
      const suspects = [
        ['the heatmap sr-only table', '[data-slot=heatmap] table'],
        ['the heatmap figcaption', '[data-slot=heatmap] figcaption'],
        ['the skip link', '#root > div > a.sr-only, #root a[href="#main"]'],
        ['the heatmap figure', '[data-slot=heatmap]'],
      ];
      for (const [name, sel] of suspects) {
        const els = [...document.querySelectorAll(sel)];
        if (!els.length) { out.suspects.push({ name, found: 0 }); continue; }
        const r = els[0].getBoundingClientRect();
        const cs = getComputedStyle(els[0]);
        const saved = els.map((e) => e.style.display);
        els.forEach((e) => { e.style.display = 'none'; });
        const w = width();
        els.forEach((e, i) => { e.style.display = saved[i]; });
        out.suspects.push({ name, found: els.length, position: cs.position, rect: [r.left, r.right, r.width].map(Math.round), widthWhenHidden: w });
      }
      return out;
    })()`);
    results.data.ec[`heatmap-${lang}`] = probe;
    page.log(`heatmap 390 ${lang}: ${JSON.stringify(probe)}`);
  }
  results.data.loads = page.loads;
  results.data.blocked = page.blocked;
} catch (error) {
  page.log(`ERROR ${error.stack}`);
} finally {
  results.save();
  results.data.chrome = await page.close();
  results.save();
}
