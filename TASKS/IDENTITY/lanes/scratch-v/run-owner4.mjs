// The owner, fourth pass: the date picker open on its range at 390 (inside the payments' filter sheet).
import { accounts, launch, sleep } from './lib.mjs';
import { checkVariant, curate, Results } from './checks.mjs';

const page = await launch('own4');
const results = new Results('own4');
const isOpen = (sel) => page.evaluate(`!!document.querySelector(${JSON.stringify(sel)})`);
try {
  await page.viewport(390, 844);
  await page.signIn(accounts().owner, '/dashboard/spaces/26/payments?from=2026-11-01&to=2026-11-10');
  const open = async () => {
    if (!(await isOpen('[data-slot=sheet-content]'))) {
      await page.evaluate(`[...document.querySelectorAll('main [data-slot=sheet-trigger], [data-slot=data-table] [data-slot=sheet-trigger]')].find((e) => window.__vp.visible(e))?.click(); true`);
      await sleep(900);
    }
    if (!(await isOpen('[data-slot=date-picker-content]'))) {
      await page.evaluate(`[...document.querySelectorAll('[data-slot=sheet-content] [data-slot=date-picker-trigger]')].find((e) => window.__vp.visible(e))?.click(); true`);
      await sleep(900);
    }
  };
  for (const v of [{ theme: 'light', lang: 'ar', width: 390 }, { theme: 'dark', lang: 'en', width: 390 }, { theme: 'dark', lang: 'ar', width: 390 }]) {
    const record = await checkVariant(page, results, 'datepicker-range-390', v, { open, axe: v.lang === 'ar' && v.theme === 'light', focus: '[data-slot=date-picker-content]', focusShot: true });
    page.log(`  picker open: ${await isOpen('[data-slot=date-picker-content]')}, sheet open: ${await isOpen('[data-slot=sheet-content]')}`);
    if (v.theme === 'light') curate(results, record.shot, '17-date-picker-range-light-ar-390.png');
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
