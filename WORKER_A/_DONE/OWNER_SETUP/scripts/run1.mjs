// PR 2's real run, part 1: Arabic, light, 1440 — the profile's prices row, «الأسعار المعلنة» saved,
// confirmed and its leave guard; a package added, edited, a repeated name refused, paused; «شهري صباحي»
// paused → its held-shift line → «إزالة الوردية», then put back. The network log is saved.
import { byText, log, OWNER, start, step, stop } from './common.mjs';

const SPACE = '/dashboard/spaces/7';
const NAME = 'مسائي طلاب';

const { b, d } = await start({
  language: 'ar',
  theme: 'light',
  width: 1440,
  who: OWNER,
  path: `${SPACE}/profile`,
});

/** The row of the package named `name`. */
const row = (name) =>
  `[...document.querySelectorAll('li')].find((li) => li.querySelector('span.text-label')?.textContent === ${JSON.stringify(name)})`;
const sheet = `document.querySelector('[role=dialog]')`;
/** A field of the sheet by its label's text. */
const field = (label) =>
  `(() => { const l = [...${sheet}.querySelectorAll('label')].find((x) => x.textContent.trim() === ${JSON.stringify(label)}); return l ? document.getElementById(l.htmlFor) : null; })()`;
/** The button of the section titled `title` whose text is `text`. */
const inSection = (title, text) =>
  `[...${d.section(title)}.querySelectorAll('button')].find((el) => el.textContent.trim() === ${JSON.stringify(text)})`;
const chip = (text) => byText('[role=dialog] [data-slot=toggle-group-item]', `^${text}$`);
const fieldError = (label) =>
  `(() => { const el = ${field(label)}; const id = el?.getAttribute('aria-describedby'); return id ? id.split(' ').map((one) => document.getElementById(one)?.textContent).join(' | ') : null; })()`;

await step('the profile’s prices row', async () => {
  await d.until(`!!${d.section('الأسعار')}`, 'prices row');
  log('prices row:', (await d.sectionText('الأسعار'))?.replace(/\n/g, ' / '));
  await d.shotSection('الأسعار', 'ar-light-1440-profile-prices-row');
  await d.click(byText(`#prices a`, 'الباقات والأسعار'), 'prices row link');
  await d.until(`location.pathname === '${SPACE}/packages'`, 'packages page');
  await d.until(`!!${d.section('الأسعار المعلنة')}`, 'published prices');
  await d.until(`!!document.querySelector('[data-slot=switch]')`, 'packages list');
  await d.sleep(800);
  log('h1:', await d.text(`document.querySelector('h1')`));
  await d.shot('ar-light-1440-packages-page');
});

await step('«الأسعار المعلنة» as a table, saved and confirmed', async () => {
  const header = await d.evaluate(
    `getComputedStyle(${d.section('الأسعار المعلنة')}.querySelector('[aria-hidden=true].hidden') ?? document.body).display`,
  );
  log('prices header row display at 1440:', header);
  await d.shotSection('الأسعار المعلنة', 'ar-light-1440-published-prices-table');
  const amount = `${d.section('الأسعار المعلنة')}.querySelector('li input[inputmode=decimal]')`;
  const before = await d.evaluate(`${amount}.value`);
  log('first amount before:', before);
  await d.typeAt(amount, '6');
  await d.until(`${d.section('الأسعار المعلنة')}.innerText.includes('تغييرات غير محفوظة')`, 'unsaved badge');
  await d.shotSection('الأسعار المعلنة', 'ar-light-1440-published-prices-unsaved');
  // The leave guard: the sidebar's «الإعدادات», then «البقاء».
  await d.click(byText('nav a', '^الإعلانات$'), 'sidebar link');
  await d.until(`!!document.querySelector('[role=alertdialog]')`, 'leave dialog');
  log('leave dialog:', await d.dialogText());
  await d.shot('ar-light-1440-published-prices-leave-guard');
  await d.click(byText('[role=alertdialog] button', '^البقاء$'), 'stay');
  log('still on:', await d.evaluate('location.pathname'));
  await d.click(inSection('الأسعار المعلنة', 'حفظ'), 'save');
  await d.until(`document.body.innerText.includes('حُفظ قسم')`, 'saved toast');
  log('toasts:', await d.toasts());
  await d.shotSection('الأسعار المعلنة', 'ar-light-1440-published-prices-saved');
  // Back as it was, then confirmed unchanged.
  await d.typeAt(amount, before);
  await d.click(inSection('الأسعار المعلنة', 'حفظ'), 'save back');
  await d.sleep(1500);
  await d.click(inSection('الأسعار المعلنة', 'المعلومات ما زالت صحيحة'), 'confirm');
  await d.until(`document.body.innerText.includes('المعلومات ما زالت صحيحة»') || document.body.innerText.includes('«الأسعار»: المعلومات')`, 'confirmed toast');
  log('toasts:', await d.toasts());
  log('prices card:', (await d.sectionText('الأسعار المعلنة'))?.split('\n').slice(0, 3).join(' / '));
  await d.shotSection('الأسعار المعلنة', 'ar-light-1440-published-prices-confirmed');
});

await step('a package added: two limits, per day, students, a shift', async () => {
  await d.click(byText('button', '^باقة جديدة$'), 'new package');
  await d.until(`!!${sheet}`, 'sheet');
  await d.typeAt(field('اسم الباقة'), NAME);
  await d.click(chip('عدد الأيام'), 'limit totalDays');
  await d.click(chip('ساعات باليوم'), 'limit hoursPerDay');
  await d.typeAt(field('عدد الأيام'), '١٢');
  await d.typeAt(field('ساعات باليوم'), '5');
  await d.click(chip('باليوم'), 'per day');
  await d.typeAt(field('سعر اليوم (₪)'), '18.5');
  await d.click(chip('الطلاب'), 'students');
  await d.click(chip('مسائي'), 'evening shift');
  await d.sleep(400);
  log('sheet:', await d.dialogText());
  await d.shot('ar-light-1440-package-sheet-new');
  await d.click(byText('[role=dialog] button[type=submit]', 'حفظ الباقة'), 'save package');
  await d.until(`!${sheet}`, 'sheet closed');
  await d.until(`!!${row(NAME)}`, 'new row');
  log('toasts:', await d.toasts());
  log('row:', (await d.text(row(NAME)))?.replace(/\n/g, ' / '));
  await d.shot('ar-light-1440-package-added');
});

await step('the package edited', async () => {
  await d.click(`${row(NAME)}.querySelector('button[aria-label^="تعديل"]')`, 'edit');
  await d.until(`!!${sheet}`, 'edit sheet');
  log('edit sheet title:', await d.text(`${sheet}.querySelector('h2')`));
  await d.typeAt(field('الصلاحية (أيام)'), '45');
  await d.click(byText('[role=dialog] button[type=submit]', 'حفظ الباقة'), 'save edit');
  await d.until(`!${sheet}`, 'sheet closed');
  await d.sleep(600);
  log('row:', (await d.text(row(NAME)))?.replace(/\n/g, ' / '));
  await d.shot('ar-light-1440-package-edited');
});

await step('a repeated name refused', async () => {
  await d.click(byText('button', '^باقة جديدة$'), 'new package');
  await d.until(`!!${sheet}`, 'sheet');
  await d.typeAt(field('اسم الباقة'), NAME);
  await d.typeAt(field('السعر الكلي (₪)'), '20');
  await d.click(byText('[role=dialog] button[type=submit]', 'حفظ الباقة'), 'save');
  await d.until(`(${fieldError('اسم الباقة')} ?? '').includes('اسم مستخدم')`, 'name refused');
  log('name error:', await d.evaluate(fieldError('اسم الباقة')));
  await d.shot('ar-light-1440-package-name-refused');
  await d.key('Escape', 'Escape', 27);
  await d.until(`!${sheet}`, 'sheet closed');
});

await step('the new package paused by its switch', async () => {
  await d.click(`${row(NAME)}.querySelector('[role=switch]')`, 'switch');
  await d.until(`${row(NAME)}.innerText.includes('موقوفة')`, 'paused');
  log('row:', (await d.text(row(NAME)))?.replace(/\n/g, ' / '));
  log('switch:', await d.evaluate(`${row(NAME)}.querySelector('[role=switch]').getAttribute('aria-label').replace(new RegExp('[' + String.fromCharCode(0x2066) + '-' + String.fromCharCode(0x2069) + ']', 'g'), '')`));
  await d.shot('ar-light-1440-package-paused');
});

await step('«شهري صباحي» paused → its held shift → «إزالة الوردية», then put back', async () => {
  const MORNING = 'شهري صباحي';
  await d.click(`${row(MORNING)}.querySelector('[role=switch]')`, 'switch');
  await d.until(`${row(MORNING)}.innerText.includes('ما زالت تحجز')`, 'held shift line');
  log('row:', (await d.text(row(MORNING)))?.replace(/\n/g, ' / '));
  await d.evaluate(`${row(MORNING)}.scrollIntoView({ block: 'center' })`);
  await d.shot('ar-light-1440-package-held-shift');
  await d.click(byText(`li button`, '^إزالة الوردية$'), 'clear shift');
  await d.until(`!${row(MORNING)}.innerText.includes('ما زالت تحجز')`, 'shift cleared');
  log('row after clear:', (await d.text(row(MORNING)))?.replace(/\n/g, ' / '));
  await d.shot('ar-light-1440-package-shift-cleared');
  // Put back as the demo had it: the shift chosen again, then offered again.
  await d.click(`${row(MORNING)}.querySelector('button[aria-label^="تعديل"]')`, 'edit');
  await d.until(`!!${sheet}`, 'edit sheet');
  await d.click(chip('صباحي'), 'morning shift');
  await d.click(byText('[role=dialog] button[type=submit]', 'حفظ الباقة'), 'save');
  await d.until(`!${sheet}`, 'sheet closed');
  await d.click(`${row(MORNING)}.querySelector('[role=switch]')`, 'switch back on');
  await d.until(`!${row(MORNING)}.innerText.includes('موقوفة')`, 'offered again');
  log('row put back:', (await d.text(row(MORNING)))?.replace(/\n/g, ' / '));
});

log('page errors:', d.errors?.length ?? b.errors.length);
log('requests:', d.requests.length, 'admin:', d.requests.filter((r) => r.includes('/admin/')).length);
d.saveLog('ar-light-1440-network-log');
stop(b);
