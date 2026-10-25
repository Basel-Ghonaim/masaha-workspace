// PR 3's real run, part 1: Arabic, light, 1440, as the demo owner — the staff page (add with a new
// email and with an existing one, the one-time dialog and its handover, the re-issue held and offered,
// deactivate and reactivate), then the settings (each card, the attendance card's one save, visit
// pricing, the reception switch, the reminder's inserts, refusals and restore). Every setting changed
// is put back. No password is printed. The network log is saved.
import { ADMIN, byText, log, OWNER, start, step, stop } from './common3.mjs';
import { byLabel } from './cdp3.mjs';

const SPACE = '/dashboard/spaces/7';
const NEW_EMAIL = `pr3-staff-${Date.now()}@example.com`;
const NEW_NAME = 'موظف تجريبي';

const { b, d } = await start({ language: 'ar', theme: 'light', width: 1440, who: OWNER, path: `${SPACE}/staff` });
await b.send('Browser.grantPermissions', { permissions: ['clipboardReadWrite', 'clipboardSanitizedWrite'] }).catch(() => undefined);

const dialog = `[...document.querySelectorAll('[role=dialog],[role=alertdialog]')].pop()`;
/** A field by the start of its label's text, inside `root`. */
const field = (root, label) =>
  `(() => { const l = [...${root}.querySelectorAll('label')].find((x) => x.textContent.trim().startsWith(${JSON.stringify(label)})); return l ? document.getElementById(l.htmlFor) : null; })()`;
const fieldError = (root, label) =>
  `(() => { const el = ${field(root, label)}; const ids = el?.getAttribute('aria-describedby'); return ids ? ids.split(' ').map((one) => document.getElementById(one)?.textContent).filter(Boolean).join(' | ') : null; })()`;
const button = (root, text) =>
  `[...${root}.querySelectorAll('button')].find((el) => el.textContent.replace(/[\\u2066-\\u2069]/g, '').trim() === ${JSON.stringify(text)})`;
const page = 'document';
const menu = (name) => byLabel('button', `^إجراءات: ${name}$`);
const menuItem = (text) => byText('[role=menuitem]', `^${text}`);
const rowText = (email) =>
  d.evaluate(`(() => { const r = [...document.querySelectorAll('tr')].find((tr) => tr.innerText.includes(${JSON.stringify(email)})); return r ? r.innerText.replace(/[\\u2066-\\u2069]/g, '').replace(/\\n+/g, ' / ') : null; })()`);
const clear = async (expression) => {
  await d.evaluate(`(() => { const el = ${expression}; el.scrollIntoView({ block: 'center' }); el.focus(); el.select(); return true; })()`);
  await d.key('Backspace', 'Backspace', 8);
};

/** Copies the password, chooses WhatsApp, and presses «تم» in the one-time dialog. */
async function handOver(prefix) {
  await d.until(`!!${dialog} && ${dialog}.innerText.includes('نسخ')`, 'one-time dialog');
  log(`${prefix} one-time dialog:`, (await d.dialogText()).replace(/\/ [A-Za-z0-9!@#$%^&*_\-+=]{8,} \//, '/ [password] /'));
  await d.click(button(dialog, 'نسخ'), 'copy');
  await d.click(byText('[role=dialog] label', '^واتساب$'), 'WhatsApp');
  await d.shot(`ar-light-1440-${prefix}-one-time-dialog`);
  await d.click(button(dialog, 'تم'), 'done');
  await d.until(`!document.querySelector('[role=dialog]')`, 'dialog closed');
  await d.sleep(600);
  log(`${prefix} toasts:`, await d.toasts());
  log(`${prefix} focus after:`, await d.evaluate(`(document.activeElement?.getAttribute('aria-label') ?? document.activeElement?.textContent ?? '').replace(/[\\u2066-\\u2069]/g, '')`));
}

await step('the staff page', async () => {
  await d.until(`!!document.querySelector('table') && document.querySelector('table').innerText.includes('@')`, 'staff table');
  await d.sleep(500);
  log('h1:', await d.text(`document.querySelector('h1')`));
  log('page:', (await d.text(`document.querySelector('main')`)).replace(/\n+/g, ' / '));
  await d.shot('ar-light-1440-staff-page');
});

await step('add with a new email', async () => {
  await d.click(button(page, 'إضافة موظف'), 'add');
  await d.until(`!!document.querySelector('[role=dialog] form')`, 'add sheet');
  log('sheet:', await d.dialogText());
  await d.shot('ar-light-1440-staff-add-sheet');
  await d.typeAt(field(dialog, 'الاسم'), NEW_NAME);
  await d.typeAt(field(dialog, 'البريد'), NEW_EMAIL);
  await d.click(button(dialog, 'إنشاء حساب الاستقبال'), 'create');
  await handOver('staff-added');
  await d.until(`document.querySelector('table').innerText.includes(${JSON.stringify(NEW_EMAIL)})`, 'new row');
  log('new row:', await rowText(NEW_EMAIL));
  await d.shot('ar-light-1440-staff-added-row');
});

await step('add with an email that has an account', async () => {
  await d.click(button(page, 'إضافة موظف'), 'add');
  await d.until(`!!document.querySelector('[role=dialog] form')`, 'add sheet');
  await d.typeAt(field(dialog, 'الاسم'), 'حساب موجود');
  await d.typeAt(field(dialog, 'البريد'), ADMIN.email);
  await d.click(button(dialog, 'إنشاء حساب الاستقبال'), 'create');
  await d.until(`(${fieldError(dialog, 'البريد')} ?? '').length > 0`, 'email line');
  log('email line:', await d.evaluate(fieldError(dialog, 'البريد')));
  await d.shot('ar-light-1440-staff-add-existing-refused');
  await d.key('Escape', 'Escape', 27);
  await d.until(`!document.querySelector('[role=dialog]')`, 'sheet closed');
});

await step('a new temporary password on the new row', async () => {
  await d.openMenu(menu(NEW_NAME), 'new row menu');
  log('menu:', await d.text(`document.querySelector('[role=menu]')`));
  await d.shot('ar-light-1440-staff-new-row-menu');
  await d.click(menuItem('كلمة مرور مؤقتة جديدة'), 'reissue');
  await d.until(`!!document.querySelector('[role=alertdialog]')`, 'reissue confirm');
  log('reissue confirm:', await d.dialogText());
  log('focused:', await d.evaluate(`document.activeElement?.textContent`));
  await d.shot('ar-light-1440-staff-reissue-confirm');
  await d.click(button(`document.querySelector('[role=alertdialog]')`, 'إصدار'), 'issue');
  await handOver('staff-reissued');
});

const demoName = await d.evaluate(`(() => { const r = [...document.querySelectorAll('tr')].find((tr) => tr.innerText.includes('demo-reception@example.com')); return r?.querySelector('[dir=auto]')?.textContent ?? null; })()`);
log('demo receptionist:', demoName);

await step('the demo receptionist’s re-issue held', async () => {
  await d.openMenu(menu(demoName), 'demo menu');
  log('demo menu:', (await d.text(`document.querySelector('[role=menu]')`)).replace(/\n+/g, ' / '));
  await d.shot('ar-light-1440-staff-reissue-held');
  await d.key('Escape', 'Escape', 27);
});

await step('deactivate and reactivate the demo receptionist', async () => {
  await d.openMenu(menu(demoName), 'demo menu');
  await d.click(menuItem('إيقاف وصوله'), 'deactivate');
  await d.until(`!!document.querySelector('[role=alertdialog]')`, 'deactivate dialog');
  log('deactivate dialog:', await d.dialogText());
  log('focused:', await d.evaluate(`document.activeElement?.textContent`));
  await d.shot('ar-light-1440-staff-deactivate-dialog');
  await d.click(button(`document.querySelector('[role=alertdialog]')`, 'إيقاف الوصول'), 'confirm');
  await d.until(`!document.querySelector('[role=alertdialog]')`, 'dialog closed');
  await d.sleep(600);
  log('row after:', await rowText('demo-reception@example.com'));
  log('toasts:', await d.toasts());
  await d.shot('ar-light-1440-staff-deactivated');
  await d.openMenu(menu(demoName), 'demo menu');
  log('deactivated menu:', (await d.text(`document.querySelector('[role=menu]')`)).replace(/\n+/g, ' / '));
  await d.shot('ar-light-1440-staff-deactivated-menu');
  await d.click(menuItem('إعادة وصوله'), 'reactivate');
  await d.until(`(${'document.querySelector("table")'}.innerText.includes('demo-reception@example.com')) && ![...document.querySelectorAll('tr')].find((tr) => tr.innerText.includes('demo-reception@example.com')).innerText.includes('بلا وصول')`, 'reactivated');
  log('row reactivated:', await rowText('demo-reception@example.com'));
  log('toasts:', await d.toasts());
  await d.shot('ar-light-1440-staff-reactivated');
});

d.saveLog('ar-light-1440-staff-network-log');
const staffRequests = d.requests.length;

// ---------------------------------------------------------------- settings
await d.nav(`${SPACE}/settings`);
const card = (title) => d.section(title);
const settingsBefore = {};

await step('the settings page', async () => {
  await d.until(`!!${card('الحضور والحالة المباشرة')} && !!${card('رسالة التذكير')}`, 'settings cards');
  await d.sleep(500);
  log('h1:', await d.text(`document.querySelector('h1')`));
  for (const title of ['الحضور والحالة المباشرة', 'تسعير الزيارات', 'الاستقبال', 'رسالة التذكير']) {
    log(`card ${title}:`, (await d.sectionText(title)).replace(/\n+/g, ' / '));
  }
  settingsBefore.capacity = await d.evaluate(`${field(card('الحضور والحالة المباشرة'), 'السعة')}.value`);
  settingsBefore.stay = await d.evaluate(`${field(card('الحضور والحالة المباشرة'), 'خروج تلقائي بعد')}.value`);
  log('before: capacity', settingsBefore.capacity, 'stay hours', settingsBefore.stay);
  await d.shot('ar-light-1440-settings-page');
});

await step('the attendance card: capacity and stay limit in one save, then the limit cleared', async () => {
  const c = card('الحضور والحالة المباشرة');
  await d.typeAt(field(c, 'السعة'), '35');
  await d.typeAt(field(c, 'خروج تلقائي بعد'), '5');
  await d.until(`${c}.innerText.includes('تغييرات غير محفوظة')`, 'unsaved');
  await d.shotSection('الحضور والحالة المباشرة', 'ar-light-1440-attendance-unsaved');
  const mark = d.requests.length;
  await d.click(button(c, 'حفظ'), 'save');
  await d.until(`!${c}.innerText.includes('تغييرات غير محفوظة')`, 'saved');
  await d.sleep(500);
  log('attendance writes:', d.requests.slice(mark).filter((r) => !r.startsWith('GET')).join(' ; '));
  log('toasts:', await d.toasts());
  await d.shotSection('الحضور والحالة المباشرة', 'ar-light-1440-attendance-saved');
  await clear(field(c, 'خروج تلقائي بعد'));
  const mark2 = d.requests.length;
  await d.click(button(c, 'حفظ'), 'save');
  await d.until(`!${c}.innerText.includes('تغييرات غير محفوظة')`, 'saved');
  await d.sleep(500);
  log('cleared writes:', d.requests.slice(mark2).filter((r) => !r.startsWith('GET')).join(' ; '));
  // A capacity of 0 is refused on its field before anything is sent.
  await d.typeAt(field(c, 'السعة'), '0');
  const mark3 = d.requests.length;
  await d.click(button(c, 'حفظ'), 'save');
  await d.until(`(${fieldError(c, 'السعة')} ?? '').length > 0`, 'capacity line');
  log('capacity 0:', await d.evaluate(fieldError(c, 'السعة')), 'sent:', d.requests.length - mark3);
  await d.shotSection('الحضور والحالة المباشرة', 'ar-light-1440-attendance-refused');
  await d.click(button(c, 'تجاهل التغييرات'), 'discard');
  log('after discard:', await d.evaluate(`${field(c, 'السعة')}.value`));
  // Put back as it was.
  await d.typeAt(field(c, 'السعة'), settingsBefore.capacity);
  if (settingsBefore.stay) await d.typeAt(field(c, 'خروج تلقائي بعد'), settingsBefore.stay);
  await d.click(button(c, 'حفظ'), 'save');
  await d.sleep(1200);
  log('restored: capacity', await d.evaluate(`${field(c, 'السعة')}.value`), 'stay', await d.evaluate(`${field(c, 'خروج تلقائي بعد')}.value`));
});

const radio = (root, label) =>
  `(() => { const l = [...${root}.querySelectorAll('label')].find((x) => x.textContent.trim() === ${JSON.stringify(label)}); return l ? document.getElementById(l.htmlFor) : null; })()`;

await step('visit pricing', async () => {
  const c = card('تسعير الزيارات');
  const checked = await d.evaluate(`[...${c}.querySelectorAll('[role=radio]')].find((r) => r.getAttribute('aria-checked') === 'true')?.value`);
  const minutes = await d.evaluate(`${field(c, 'دقائق التقريب')}.value`);
  log('pricing before:', checked, minutes);
  if (checked !== 'UP_AFTER_MINUTES' || minutes !== '10') {
    await d.click(radio(c, 'تقريب لأعلى بعد'), 'up after');
    await d.typeAt(field(c, 'دقائق التقريب'), '10');
    await d.click(button(c, 'حفظ'), 'save');
    await d.sleep(1200);
  }
  log('example at 10:', await d.text(`[...${c}.querySelectorAll('p')].find((p) => p.textContent.includes(' = '))`));
  await d.shotSection('تسعير الزيارات', 'ar-light-1440-pricing-up-after-10');
  await d.click(radio(c, 'لأقرب نصف ساعة'), 'half');
  log('minutes disabled:', await d.evaluate(`${field(c, 'دقائق التقريب')}.disabled`));
  let mark = d.requests.length;
  await d.click(button(c, 'حفظ'), 'save');
  await d.until(`!${c}.innerText.includes('تغييرات غير محفوظة')`, 'saved');
  await d.sleep(400);
  log('half writes:', d.requests.slice(mark).filter((r) => !r.startsWith('GET')).join(' ; '));
  log('toasts:', await d.toasts());
  await d.shotSection('تسعير الزيارات', 'ar-light-1440-pricing-half');
  await d.click(radio(c, 'تقريب لأعلى بعد'), 'up after');
  await d.typeAt(field(c, 'دقائق التقريب'), '15');
  log('example at 15:', await d.text(`[...${c}.querySelectorAll('p')].find((p) => p.textContent.includes(' = '))`));
  mark = d.requests.length;
  await d.click(button(c, 'حفظ'), 'save');
  await d.until(`!${c}.innerText.includes('تغييرات غير محفوظة')`, 'saved');
  log('up-after-15 writes:', d.requests.slice(mark).filter((r) => !r.startsWith('GET')).join(' ; '));
  await d.shotSection('تسعير الزيارات', 'ar-light-1440-pricing-up-after-15');
  // Put back as it was.
  if (checked === 'UP_AFTER_MINUTES') {
    await d.typeAt(field(c, 'دقائق التقريب'), minutes);
  } else {
    await d.click(radio(c, checked === 'NEAREST_HALF_HOUR' ? 'لأقرب نصف ساعة' : 'بالدقيقة'), 'rule back');
  }
  await d.click(button(c, 'حفظ'), 'save');
  await d.sleep(1200);
  log('pricing restored:', await d.evaluate(`[...${c}.querySelectorAll('[role=radio]')].find((r) => r.getAttribute('aria-checked') === 'true')?.value`), await d.evaluate(`${field(c, 'دقائق التقريب')}.value`));
});

await step('the reception switch', async () => {
  const c = card('الاستقبال');
  const sw = `${c}.querySelector('[role=switch]')`;
  const before = await d.evaluate(`${sw}.getAttribute('aria-checked')`);
  await d.click(sw, 'switch');
  await d.shotSection('الاستقبال', 'ar-light-1440-reception-unsaved');
  const mark = d.requests.length;
  await d.click(button(c, 'حفظ'), 'save');
  await d.until(`!${c}.innerText.includes('تغييرات غير محفوظة')`, 'saved');
  await d.sleep(400);
  log('reception writes:', d.requests.slice(mark).filter((r) => !r.startsWith('GET')).join(' ; '));
  log('toasts:', await d.toasts());
  await d.shotSection('الاستقبال', 'ar-light-1440-reception-saved');
  await d.click(sw, 'switch back');
  await d.click(button(c, 'حفظ'), 'save');
  await d.sleep(1200);
  log('reception restored:', before, '→', await d.evaluate(`${sw}.getAttribute('aria-checked')`));
});

await step('the reminder', async () => {
  const c = card('رسالة التذكير');
  const area = `${c}.querySelector('textarea')`;
  const original = await d.evaluate(`${area}.value`);
  log('reminder before:', original);
  // Insert each token at the caret: an empty text, then each at its own place.
  await d.typeAt(area, 'مرحبًا ، عليك . من ');
  for (const [at, label] of [[7, 'إدراج الاسم'], [17, 'إدراج المبلغ']]) {
    await d.evaluate(`(() => { const t = ${area}; t.setSelectionRange(${at}, ${at}); return true; })()`);
    await d.click(byLabel('button', `^${label}$`), label);
  }
  await d.evaluate(`(() => { const t = ${area}; t.setSelectionRange(t.value.length, t.value.length); return true; })()`);
  await d.click(byLabel('button', '^إدراج المساحة$'), 'space');
  log('after inserts:', await d.evaluate(`${area}.value`), '| caret', await d.evaluate(`${area}.selectionStart`), '| focus in field', await d.evaluate(`document.activeElement === ${area}`));
  log('preview:', await d.text(`[...${c}.querySelectorAll('p')].pop()`));
  await d.shotSection('رسالة التذكير', 'ar-light-1440-reminder-inserted');
  // Without {المبلغ}.
  await d.typeAt(area, 'مرحبًا {الاسم}، تذكير من {المساحة}.');
  await d.click(button(c, 'حفظ'), 'save');
  await d.until(`(${fieldError(c, 'نص الرسالة')} ?? '').length > 0`, 'amount line');
  log('missing amount:', await d.evaluate(fieldError(c, 'نص الرسالة')));
  await d.shotSection('رسالة التذكير', 'ar-light-1440-reminder-missing-amount');
  // A placeholder off the list.
  await d.typeAt(area, 'مرحبًا {الاسم الكامل}، عليك {المبلغ}.');
  await d.click(button(c, 'حفظ'), 'save');
  await d.until(`(${fieldError(c, 'نص الرسالة')} ?? '').includes('الكامل')`, 'unknown line');
  log('unknown placeholder:', (await d.evaluate(fieldError(c, 'نص الرسالة'))).replace(/[⁦-⁩]/g, ''));
  await d.shotSection('رسالة التذكير', 'ar-light-1440-reminder-unknown');
  // A valid one, saved.
  await d.typeAt(area, 'مرحبًا {الاسم}، عليك {المبلغ} في {المساحة}. شكرًا.');
  let mark = d.requests.length;
  await d.click(button(c, 'حفظ'), 'save');
  await d.until(`!${c}.innerText.includes('تغييرات غير محفوظة')`, 'saved');
  await d.sleep(400);
  log('reminder writes:', d.requests.slice(mark).filter((r) => !r.startsWith('GET')).join(' ; '));
  log('toasts:', await d.toasts());
  await d.shotSection('رسالة التذكير', 'ar-light-1440-reminder-saved');
  // Restore the default, saved as none.
  await d.click(button(c, 'استعادة النص الافتراضي'), 'restore');
  log('restored text:', await d.evaluate(`${area}.value`));
  mark = d.requests.length;
  await d.click(button(c, 'حفظ'), 'save');
  await d.until(`!${c}.innerText.includes('تغييرات غير محفوظة')`, 'saved');
  log('restore writes:', d.requests.slice(mark).filter((r) => !r.startsWith('GET')).join(' ; '));
  await d.shotSection('رسالة التذكير', 'ar-light-1440-reminder-restored');
  if (original !== (await d.evaluate(`${area}.value`))) log('NOTE: the reminder was', JSON.stringify(original), 'before the run');
});

d.saveLog('ar-light-1440-network-log');
log('requests: staff', staffRequests, 'total', d.requests.length, '/admin/:', d.requests.filter((r) => r.includes('/admin/')).length);
log('page errors:', JSON.stringify(b.errors));
stop(b);
