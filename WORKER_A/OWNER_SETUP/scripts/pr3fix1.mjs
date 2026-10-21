// PR 3's fix round, a short real run: the reminder left as the catalogue's text after a language
// switch saves nothing (Arabic light → English, English dark → Arabic, at 1440 and 390); the add
// sheet's reworded line for an email that has an account; the settings' loading heard. Shots to
// shots/pr3-fixes. No setting is changed; no password printed.
import { mkdirSync } from 'node:fs';
import { log, OWNER, ADMIN, start, step, stop } from './common3.mjs';

const SHOTS = 'C:/dev/masaha/workspace/WORKER_A/OWNER_SETUP/shots/pr3-fixes';
mkdirSync(SHOTS, { recursive: true });
const SPACE = '/dashboard/spaces/7';

for (const [language, theme, other, width] of [
  ['ar', 'light', 'en', 1440],
  ['ar', 'light', 'en', 390],
  ['en', 'dark', 'ar', 1440],
  ['en', 'dark', 'ar', 390],
]) {
  const tag = `${language}-${theme}-${width}`;
  const { b, d } = await start({ language, theme, width, who: OWNER, path: `${SPACE}/settings` });
  const shot = async (name, height) => {
    const { writeFileSync } = await import('node:fs');
    if (height) await d.viewport(width, height);
    const { data } = await b.send('Page.captureScreenshot', { format: 'png' });
    writeFileSync(`${SHOTS}/${name}.png`, Buffer.from(data, 'base64'));
    if (height) await d.viewport(width, 900);
    console.log('shot', name);
  };
  await step(`${tag} reminder after a language switch`, async () => {
    await d.until(`!!document.querySelector('main textarea')`, 'reminder');
    const area = `document.querySelector('main textarea')`;
    log(`${tag} reminder before:`, (await d.evaluate(`${area}.value`)).slice(0, 30));
    // The interface's own switch: the language button in the top bar.
    await d.evaluate(`localStorage.setItem('masaha.language', ${JSON.stringify(other)}); true`);
    await d.evaluate(`(() => { const b = [...document.querySelectorAll('header button, button')].find((x) => /^(English|العربية)$/.test(x.textContent.trim())); b?.click(); return !!b; })()`);
    await d.until(`document.documentElement.lang === ${JSON.stringify(other)}`, 'language switched');
    await d.sleep(800);
    log(`${tag} reminder after switch:`, (await d.evaluate(`${area}.value`)).slice(0, 30));
    const card = `${area}.closest('[data-slot=card]')`;
    const mark = d.requests.length;
    await d.click(`[...${card}.querySelectorAll('button[type=submit]')][0]`, 'save');
    await d.sleep(1200);
    log(`${tag} note:`, await d.evaluate(`${card}.querySelector('[role=status]')?.textContent ?? null`));
    log(`${tag} writes:`, d.requests.slice(mark).filter((r) => !r.startsWith('GET')).length);
    await d.evaluate(`(() => { ${card}.scrollIntoView({ block: 'start' }); return true; })()`);
    await d.sleep(300);
    await shot(`${tag}-reminder-after-language-switch`);
  });
  if (width === 1440) {
    await step(`${tag} the add sheet's line for an email that has an account`, async () => {
      await d.go(`${SPACE}/staff`);
      await d.until(`document.querySelector('main')?.innerText.includes('@example.com')`, 'staff');
      const addLabel = other === 'ar' ? 'إضافة موظف' : 'Add staff member';
      await d.click(`[...document.querySelectorAll('button')].find((x) => x.textContent.trim() === ${JSON.stringify(addLabel)})`, 'add');
      await d.until(`!!document.querySelector('[role=dialog] form')`, 'sheet');
      const inputs = `[...document.querySelectorAll('[role=dialog] input')]`;
      await d.typeAt(`${inputs}[0]`, 'Existing');
      await d.typeAt(`${inputs}[1]`, ADMIN.email);
      await d.click(`document.querySelector('[role=dialog] button[type=submit]')`, 'create');
      await d.until(`[...document.querySelectorAll('[role=dialog] [id$=-error]')].some((e) => e.textContent.length > 0)`, 'email line');
      log(`${tag} email line:`, await d.evaluate(`[...document.querySelectorAll('[role=dialog] [id$=-error]')].map((e) => e.textContent).join(' | ')`));
      await shot(`${tag}-staff-add-existing-line`);
    });
  }
  log(`${tag} /admin/ requests:`, d.requests.filter((r) => r.includes('/admin/')).length, '| page errors:', JSON.stringify(b.errors));
  stop(b);
}
