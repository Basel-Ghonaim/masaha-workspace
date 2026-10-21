// PR 3's real run, part 2: reception refused /staff and /settings; then the staff page, its add sheet
// and a row's menu, and the settings page, Arabic light at 768 and 390 and English dark at 1440, 768
// and 390, with no horizontal scroll at any width. Nothing is changed.
import { byText, log, OWNER, RECEPTION, start, step, stop } from './common3.mjs';
import { byLabel } from './cdp3.mjs';

const SPACE = '/dashboard/spaces/7';

{
  const { b, d } = await start({ language: 'ar', theme: 'light', width: 1440, who: RECEPTION, path: `${SPACE}/desk` });
  for (const page of ['staff', 'settings']) {
    await step(`reception refused ${page}`, async () => {
      const mark = d.requests.length;
      await d.go(`${SPACE}/${page}`);
      await d.until(`document.querySelector('main')?.innerText.includes('لا تملك صلاحية')`, '403');
      log(`reception ${page}:`, (await d.text(`document.querySelector('main')`)).replace(/\n+/g, ' / '));
      log(`sidebar has it:`, await d.evaluate(`[...document.querySelectorAll('nav a')].some((a) => a.textContent.trim() === ${JSON.stringify(page === 'staff' ? 'الموظفون' : 'الإعدادات')})`));
      log(`requests to /${page}:`, d.requests.slice(mark).filter((r) => r.includes(`/${page}`) || r.includes('/capacity')).length);
      await d.shot(`ar-light-1440-reception-${page}-403`);
    });
  }
  log('page errors:', JSON.stringify(b.errors));
  stop(b);
}

for (const [language, theme, widths] of [
  ['ar', 'light', [768, 390]],
  ['en', 'dark', [1440, 768, 390]],
]) {
  const { b, d } = await start({ language, theme, width: widths[0], who: OWNER, path: `${SPACE}/staff` });
  const add = language === 'ar' ? 'إضافة موظف' : 'Add staff member';
  const menuName = language === 'ar' ? '^إجراءات: ' : '^Actions: ';
  for (const width of widths) {
    const tag = `${language}-${theme}-${width}`;
    await step(`${tag} staff`, async () => {
      await d.viewport(width, 900);
      await d.go(`${SPACE}/staff`);
      await d.until(`document.querySelector('main')?.innerText.includes('demo-reception@example.com')`, 'staff list');
      await d.sleep(500);
      log(`${tag} table shown:`, await d.evaluate(`!!document.querySelector('main table')`), '| overflow:', await d.evaluate(`document.documentElement.scrollWidth > innerWidth`));
      await d.shot(`${tag}-staff-page`);
      await d.openMenu(byLabel('button', menuName + '.*'), 'a row menu');
      await d.shot(`${tag}-staff-row-menu`);
      await d.key('Escape', 'Escape', 27);
      await d.click(byText('button', `^${add}$`), 'add');
      await d.until(`!!document.querySelector('[role=dialog] form')`, 'sheet');
      await d.sleep(400);
      await d.shot(`${tag}-staff-add-sheet`);
      await d.key('Escape', 'Escape', 27);
    });
    await step(`${tag} settings`, async () => {
      await d.go(`${SPACE}/settings`);
      await d.until(`!!document.querySelector('main textarea')`, 'settings cards');
      await d.sleep(500);
      log(`${tag} settings overflow:`, await d.evaluate(`document.documentElement.scrollWidth > innerWidth`));
      await d.shot(`${tag}-settings-page`, 2400);
      await d.viewport(width, 900);
    });
  }
  d.saveLog(`${language}-${theme}-network-log`);
  log(`${language}-${theme} requests:`, d.requests.length, '/admin/:', d.requests.filter((r) => r.includes('/admin/')).length);
  log('page errors:', JSON.stringify(b.errors));
  stop(b);
}
