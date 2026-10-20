// PR 2's real run, part 2: Packages & prices at each width — «الأسعار المعلنة» a table at 1440 and
// cards at 768 and 390, the packages, and the sheet — in Arabic light and English dark. Usage:
// node run2.mjs <ar|en> <light|dark> <width>...
import { byText, log, OWNER, start, stop } from './common.mjs';

const [language, theme, ...widths] = process.argv.slice(2);
const PATH = '/dashboard/spaces/7/packages';
const prices = language === 'ar' ? 'الأسعار المعلنة' : 'Published prices';
const add = language === 'ar' ? 'باقة جديدة' : 'New package';

const { b, d } = await start({ language, theme, width: Number(widths[0]), who: OWNER, path: PATH });

for (const width of widths.map(Number)) {
  const tag = `${language}-${theme}-${String(width)}`;
  await d.viewport(width, 900);
  await d.go(PATH);
  await d.until(`!!${d.section(prices)}`, 'published prices');
  await d.until(`!!document.querySelector('[role=switch]')`, 'packages list');
  await d.sleep(800);
  const header = await d.evaluate(
    `getComputedStyle(${d.section(prices)}.querySelector('[aria-hidden=true].hidden')).display`,
  );
  const scroll = await d.evaluate('document.documentElement.scrollWidth > innerWidth');
  log(tag, 'prices header display:', header, '· horizontal scroll:', scroll);
  await d.shot(`${tag}-packages-page`);
  await d.shotSection(prices, `${tag}-published-prices`);
  await d.evaluate(`(() => { const el = [...document.querySelectorAll('h2')].find((h) => h.textContent === ${JSON.stringify(language === 'ar' ? 'الباقات الخاصة' : 'Private packages')}); el?.scrollIntoView({ block: 'start' }); return true; })()`);
  await d.sleep(400);
  await d.shot(`${tag}-private-packages`);
  await d.click(byText('button', `^${add}$`), 'new package');
  await d.until(`!!document.querySelector('[role=dialog]')`, 'sheet');
  await d.sleep(600);
  await d.shot(`${tag}-package-sheet`);
  await d.key('Escape', 'Escape', 27);
  await d.sleep(500);
}

log('page errors:', b.errors.length);
log('requests:', d.requests.length, 'admin:', d.requests.filter((r) => r.includes('/admin/')).length);
d.saveLog(`${language}-${theme}-network-log`);
stop(b);
