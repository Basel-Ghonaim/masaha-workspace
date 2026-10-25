// DESK_SCREENS PR 3's real run: «الزبائن», «ملف الزبون», the statement, edit / archive / restore, the end,
// the carried fixes and the idle sign-out. Usage: node run3.mjs <case>
//   cases: idle layouts filters edit archive end carried1 carried2 touch
// The demo password is read from apps/api/.env and never printed; no phone is printed. Enter is sent with
// its text ('\r'). Writes only PR 3's listed writes (§13 + the approval note's §14.11), on masaha-demo:
// as the owner — «نور حسن»'s phone set then cleared; «زائر تجربة 2» archived then restored; «يوسف»'s
// subscription ended; as reception — a named visit from the search (carried item 2), checked out at once,
// paid. Every other case reads only.
import { readFileSync, writeFileSync } from 'node:fs';
import { byLabel, byText, driver, launch, SHOTS } from './cdp3.mjs';

const env = readFileSync('C:/dev/masaha/app/apps/api/.env', 'utf8');
const PASSWORD = /^SEED_DEMO_PASSWORD=(.*)$/m.exec(env)?.[1]?.trim().replace(/^["']|["']$/g, '');
if (!PASSWORD) throw new Error('no SEED_DEMO_PASSWORD');
const ACCOUNTS = { owner: 'demo-owner@example.com', reception: 'demo-reception@example.com' };
const THEME = { ar: 'light', en: 'dark' };
const tag = (language, width) => `${language}-${THEME[language]}-${width}`;
const clean = (text) => (text ?? '').replace(/[\u2066-\u2069]/g, '').replace(/\+?\d{9,}/g, '<phone>');
const log = (...a) => console.log('·', ...a.map((x) => (typeof x === 'string' ? clean(x) : x)));
const SPACE = '/dashboard/spaces/7';
const LIST = `${SPACE}/customers`;
const file = (id) => `${LIST}/${String(id)}`;
// The inventory's records (scripts\inventory3.out.txt).
const SARA = 1;
const NOUR = 3;
const YOUSEF = 4;
const VISITOR2 = 6;

async function session(role, language, width, landing = LIST) {
  const b = await launch();
  const d = driver(b);
  d.b = b;
  d.requests = [];
  await b.send('Network.enable');
  b.on((m) => {
    if (m.method === 'Network.requestWillBeSent' && m.params.request.url.includes('/api/v1/')) {
      d.requests.push({
        id: m.params.requestId,
        at: new Date().toISOString(),
        method: m.params.request.method,
        url: m.params.request.url.replace(/^https?:\/\/localhost:\d+/, ''),
        key: m.params.request.headers['Idempotency-Key'] ?? null,
        // An auth request's body holds the password: never kept.
        body: m.params.request.url.includes('/auth/') ? null : (m.params.request.postData ?? null),
      });
    }
    if (m.method === 'Network.responseReceived') {
      const r = d.requests.find((x) => x.id === m.params.requestId);
      if (r) r.status = m.params.response.status;
    }
    if (m.method === 'Network.loadingFailed') {
      const r = d.requests.find((x) => x.id === m.params.requestId);
      if (r) r.status = `failed (${m.params.errorText})`;
    }
  });
  await d.viewport(width, 900);
  await d.theme(THEME[language] === 'dark');
  await d.go('/');
  await d.prefs(language, THEME[language]);
  await d.go(`/login?next=${encodeURIComponent(landing)}`);
  await d.until(`!!document.querySelector('input[type=email]')`, 'login form');
  await d.type('input[type=email]', ACCOUNTS[role]);
  await d.type('input[type=password]', PASSWORD);
  await d.click(`document.querySelector('form button[type=submit]')`, 'sign in');
  await d.until(`location.pathname === ${JSON.stringify(landing.split('?')[0])}`, 'landing', 20000);
  await d.prefs(language, THEME[language]);
  await d.sleep(2500);
  return { b, d };
}

const toastText = (d) => d.evaluate(`[...document.querySelectorAll('[data-sonner-toast]')].map((t) => t.getAttribute('data-type') + ': ' + t.innerText.replace(/\\n+/g, ' | ')).join(' || ')`);
const dialogText = (d) => d.evaluate(`(document.querySelector('[role=dialog],[role=alertdialog]')?.innerText ?? '').replace(/\\n+/g, ' | ')`);
const mainText = (d) => d.evaluate(`(document.querySelector('main')?.innerText ?? '').replace(/\\n+/g, ' | ').slice(0, 600)`);
const line = (r) =>
  `${r.at} ${r.method} ${r.url} ${r.status ?? '(no answer)'} Idempotency-Key: ${r.key ?? 'none'}${r.body ? ` body: ${clean(r.body)}` : ''}`;
const writes = (d) => d.requests.filter((r) => r.method !== 'GET' && !r.url.includes('/auth/'));
const offline = (d, on) =>
  d.b.send('Network.emulateNetworkConditions', { offline: on, latency: 0, downloadThroughput: -1, uploadThroughput: -1 });

function saveNetwork(d, name, all = writes(d)) {
  const text = all.map(line);
  for (const l of text) log('  ', l);
  writeFileSync(`${SHOTS}/3-${name}-network.txt`, `${text.join('\n')}\n`);
}

/** Opens the full page height for a shot, then takes it. */
async function fullShot(d, name) {
  const height = await d.evaluate('Math.min(4000, Math.max(900, document.documentElement.scrollHeight))');
  await d.shot(name, height);
}

async function openMenu(d, name) {
  await d.openMenu(byLabel('button', `^(إجراءات أخرى|More actions): ${name}$`), `the «⋯» of ${name}`);
}

const cases = {
  /** Reception left on the desk, untouched for 16 minutes; then one click: the server's idle end. */
  async idle() {
    const { b, d } = await session('reception', 'ar', 1440, `${SPACE}/desk`);
    try {
      const start = new Date();
      log('idle from', start.toISOString());
      await d.sleep(16 * 60 * 1000);
      log('idle until', new Date().toISOString());
      const where = await d.evaluate('location.pathname + location.search');
      log('the page after 16 minutes, untouched:', where);
      if (!where.startsWith('/login')) {
        await d.click(byText('a', '^الزبائن$'), 'the sidebar’s customers');
      }
      await d.until(`location.pathname === '/login'`, 'sign-in', 20000);
      await d.sleep(1500);
      log('landed', await d.evaluate('location.pathname + location.search'));
      log('line:', await d.evaluate(`document.querySelector('[role=status]')?.innerText ?? 'none'`));
      await d.shot(`3-idle-reception-${tag('ar', 1440)}`);
      saveNetwork(d, 'idle', d.requests.filter((r) => Date.parse(r.at) > start.getTime() + 15 * 60 * 1000 || r.url.includes('/auth/')));
    } finally {
      b.chrome.kill();
    }
  },

  /** The list, the file and a statement, both roles, both languages, three widths (reads only). */
  async layouts() {
    for (const role of ['owner', 'reception']) {
      for (const language of ['ar', 'en']) {
        for (const width of [390, 768, 1440]) {
          const { b, d } = await session(role, language, width);
          try {
            await d.until(`document.querySelectorAll('main a[href*="/customers/"]').length > 0`, 'the rows');
            log(role, tag(language, width), 'table:', await d.evaluate(`!!document.querySelector('main table')`));
            await fullShot(d, `3-list-${role}-${tag(language, width)}`);
            await d.go(file(NOUR));
            await d.until(`!!document.querySelector('main h3')`, 'the cards');
            const toggle = byText('main button', '^(عرض الكشف|Show the statement)$');
            await d.click(toggle, 'show the statement');
            await d.until(`!!document.querySelector('main h4')`, 'the statement');
            await d.sleep(800);
            log(role, tag(language, width), 'file:', await mainText(d));
            log(role, 'title:', await d.evaluate('document.title'));
            await fullShot(d, `3-file-${role}-${tag(language, width)}`);
            if (width === 1440) {
              await d.go(file(SARA));
              await d.until(`!!document.querySelector('main h3')`, 'sara’s cards');
              await d.click(byText('main button', '^(عرض الكشف|Show the statement)$'), 'sara’s statement');
              await d.until(`!!document.querySelector('main h4')`, 'sara’s statement');
              await d.sleep(800);
              await fullShot(d, `3-statement-sara-${role}-${tag(language, width)}`);
            }
          } finally {
            b.chrome.kill();
          }
        }
      }
    }
  },

  /** Reception's filters in the address; the sheet at 390; the owner's «مؤرشف» and its empty state. */
  async filters() {
    for (const width of [1440, 390]) {
      const { b, d } = await session('reception', 'ar', width);
      try {
        await d.until(`document.querySelectorAll('main a[href*="/customers/"]').length > 0`, 'the rows');
        log('reception chips:', await d.evaluate(`[...document.querySelectorAll('[role=radiogroup] [role=radio]')].map((r) => r.textContent).join(', ')`));
        await d.click(byText('[role=radio]', '^ينتهي قريبًا$'), 'ending soon');
        await d.sleep(1500);
        log('ending soon:', await d.evaluate('location.search'), await mainText(d));
        await d.shot(`3-filter-status-reception-${tag('ar', width)}`);
        if (width === 390) {
          await d.click(byText('main button', 'الفلاتر'), 'the sheet');
          await d.until(`!!document.querySelector('[role=dialog]')`, 'the sheet');
          await d.shot(`3-filter-sheet-reception-${tag('ar', width)}`);
          await d.key('Escape', 'Escape', 27);
          await d.go(`${LIST}?kind=NONE&payment=OWES`);
          await d.sleep(2500);
          log('kind+payment:', await mainText(d));
          await d.click(byText('main button', 'الفلاتر'), 'the sheet again');
          await d.until(`!!document.querySelector('[role=dialog]')`, 'the sheet');
          log('sheet:', await dialogText(d));
          await d.shot(`3-filter-sheet-applied-reception-${tag('ar', width)}`);
        } else {
          await d.go(`${LIST}?status=ARCHIVED`);
          await d.sleep(2500);
          log('reception ?status=ARCHIVED:', await d.evaluate('location.search'), await mainText(d));
          await d.go(`${LIST}?q=${encodeURIComponent('زائر')}`);
          await d.sleep(2500);
          log('search زائر:', await mainText(d));
          await d.shot(`3-filter-search-reception-${tag('ar', width)}`);
        }
      } finally {
        b.chrome.kill();
      }
    }
    const { b, d } = await session('owner', 'en', 1440, `${LIST}?status=ARCHIVED`);
    try {
      log('owner archived:', await mainText(d));
      await d.shot(`3-filter-archived-owner-${tag('en', 1440)}`);
    } finally {
      b.chrome.kill();
    }
  },

  /** The owner edits «نور حسن»'s phone (the first save sent offline: no answer, never re-sent), then clears it. */
  async edit() {
    const { b, d } = await session('owner', 'ar', 1440, file(NOUR));
    try {
      await d.until(`!!document.querySelector('main h3')`, 'the file');
      await openMenu(d, 'نور حسن');
      await d.click(byText('[role=menuitem]', '^تعديل البيانات$'), 'edit');
      await d.until(`!!document.querySelector('[role=dialog] input[type=tel]')`, 'the dialog');
      await d.type('[role=dialog] input[type=tel]', '+970599000304');
      await d.shot(`3-edit-form-owner-${tag('ar', 1440)}`);
      await offline(d, true);
      await d.click(byText('[role=dialog] button[type=submit]', '^حفظ$'), 'save offline');
      await d.until(`!!document.querySelector('[role=dialog] [role=alert]')`, 'the lost line', 20000);
      await d.sleep(6000);
      log('lost:', await dialogText(d));
      await d.shot(`3-edit-lost-owner-${tag('ar', 1440)}`);
      await offline(d, false);
      await d.click(byText('[role=dialog] button', '^إعادة المحاولة$'), 'retry');
      await d.until(`!document.querySelector('[role=dialog]')`, 'closed', 20000);
      log('toast:', await toastText(d));
      await d.sleep(2000);
      log('header:', await mainText(d));
      await d.shot(`3-edit-saved-owner-${tag('ar', 1440)}`);
      await openMenu(d, 'نور حسن');
      await d.click(byText('[role=menuitem]', '^تعديل البيانات$'), 'edit again');
      await d.until(`!!document.querySelector('[role=dialog] input[type=tel]')`, 'the dialog');
      await d.evaluate(`(() => { const el = document.querySelector('[role=dialog] input[type=tel]'); el.focus(); el.select(); return true; })()`);
      await d.key('Delete', 'Delete', 46);
      await d.enter();
      await d.until(`!document.querySelector('[role=dialog]')`, 'closed', 20000);
      log('toast:', await toastText(d));
      await d.sleep(1500);
      log('header:', await mainText(d));
      saveNetwork(d, 'edit');
    } finally {
      b.chrome.kill();
    }
  },

  /** The owner archives «زائر تجربة 2» (owes: the dialog), then restores them from «مؤرشف». */
  async archive() {
    const { b, d } = await session('owner', 'ar', 1440, file(VISITOR2));
    try {
      await d.until(`!!document.querySelector('main h2')`, 'the file');
      await openMenu(d, 'زائر تجربة 2');
      await d.shot(`3-archive-menu-owner-${tag('ar', 1440)}`);
      await d.click(byText('[role=menuitem]', '^أرشفة…$'), 'archive');
      await d.until(`!!document.querySelector('[role=alertdialog]')`, 'the question');
      log('question:', await dialogText(d));
      await d.shot(`3-archive-dialog-owner-${tag('ar', 1440)}`);
      await d.click(byText('[role=alertdialog] button', '^أرشفة رغم الدين$'), 'archive anyway');
      await d.until(`!document.querySelector('[role=alertdialog]')`, 'closed', 20000);
      log('toast:', await toastText(d));
      await d.sleep(2000);
      log('header:', await mainText(d));
      await d.shot(`3-archive-done-owner-${tag('ar', 1440)}`);
      await d.go(`${LIST}?status=ARCHIVED`);
      await d.until(`!!${byText('main button', '^استرجاع$')}`, 'the restore');
      await d.shot(`3-archive-list-owner-${tag('ar', 1440)}`);
      await d.click(byText('main button', '^استرجاع$'), 'restore');
      await d.sleep(2500);
      log('toast:', await toastText(d));
      log('list:', await mainText(d));
      await d.shot(`3-archive-restored-owner-${tag('ar', 1440)}`);
      saveNetwork(d, 'archive');
    } finally {
      b.chrome.kill();
    }
  },

  /** The owner ends «يوسف»'s subscription (the approval note's §14.11). */
  async end() {
    const { b, d } = await session('owner', 'en', 1440, file(YOUSEF));
    try {
      await d.go(file(YOUSEF));
      await d.until(`!!document.querySelector('main h3')`, 'the card');
      await d.click(byText('main button', '^End subscription$'), 'end');
      await d.until(`!!document.querySelector('[role=alertdialog]')`, 'the question');
      log('question:', await dialogText(d));
      await d.shot(`3-end-dialog-owner-${tag('en', 1440)}`);
      await d.click(byText('[role=alertdialog] button', '^End subscription$'), 'confirm');
      await d.until(`!document.querySelector('[role=alertdialog]')`, 'closed', 20000);
      log('toast:', await toastText(d));
      await d.sleep(2500);
      log('card:', await mainText(d));
      await d.shot(`3-end-done-owner-${tag('en', 1440)}`);
      saveNetwork(d, 'end');
    } finally {
      b.chrome.kill();
    }
  },

  /** Carried item 1, live: the file's read blocked by CDP (that one URL), its failure and retry. */
  async carried1() {
    const { b, d } = await session('reception', 'ar', 1440, LIST);
    try {
      const url = `*/api/v1/manage/spaces/7/customers/${String(SARA)}`;
      await b.send('Network.setBlockedURLs', { urls: [url] });
      await d.click(byText('main a', '^سارة خالد$'), 'sara’s file');
      await d.until(`!!document.querySelector('main [role=alert]')`, 'the failure', 20000);
      log('failure:', await mainText(d));
      await d.shot(`3-carried1-failed-reception-${tag('ar', 1440)}`);
      await b.send('Network.setBlockedURLs', { urls: [] });
      await d.click(byText('main [role=alert] button', '^إعادة المحاولة$'), 'retry');
      await d.until(`!!document.querySelector('main h3')`, 'the file', 20000);
      await d.shot(`3-carried1-retried-reception-${tag('ar', 1440)}`);
      saveNetwork(d, 'carried1', d.requests.filter((r) => r.url.includes(`/customers/${String(SARA)}`)));
    } finally {
      b.chrome.kill();
    }
  },

  /** Carried item 2, live: a visit by name from the search clears and focuses it; then checked out, paid. */
  async carried2() {
    const SEARCH = 'input[type=search][aria-controls]';
    const name = 'زائر تجربة 5';
    const { b, d } = await session('reception', 'ar', 1440, `${SPACE}/desk`);
    try {
      await d.until(`!!document.querySelector(${JSON.stringify(SEARCH)})`, 'the search');
      await d.type(SEARCH, name);
      await d.sleep(1800);
      await d.click(byText('main button', `^تسجيل زيارة باسم «${name}»$`), 'the named visit');
      await d.until(`!!document.querySelector('[role=dialog]')`, 'the visit dialog');
      await d.shot(`3-carried2-dialog-reception-${tag('ar', 1440)}`);
      await d.enter();
      await d.until(`!document.querySelector('[role=dialog]')`, 'closed', 20000);
      await d.sleep(800);
      const state = await d.evaluate(`(() => { const box = document.querySelector(${JSON.stringify(SEARCH)}); return { value: box.value, focused: document.activeElement === box }; })()`);
      log('after the check-in, the search:', JSON.stringify(state), 'toast:', await toastText(d));
      await d.shot(`3-carried2-cleared-reception-${tag('ar', 1440)}`);
      await d.click(byLabel('main button', `^خروج ${name}$`), 'its check-out');
      await d.until(`!!document.querySelector('[role=dialog] button[type=submit]')`, 'the check-out');
      await d.sleep(1500);
      log('check-out:', await dialogText(d));
      await d.click(`document.querySelector('[role=dialog] button[type=submit]')`, 'check out, paid');
      await d.until(`!document.querySelector('[role=dialog]')`, 'closed', 20000);
      log('toast:', await toastText(d));
      saveNetwork(d, 'carried2');
    } finally {
      b.chrome.kill();
    }
  },

  /** Touch targets at 390: the computed heights of the list's and the file's controls (reads only). */
  async touch() {
    const { b, d } = await session('owner', 'ar', 390, LIST);
    try {
      await b.send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 1 });
      await d.go(LIST);
      await d.until(`document.querySelectorAll('main a[href*="/customers/"]').length > 0`, 'the rows');
      const heights = (selector) => d.evaluate(`[...document.querySelectorAll(${JSON.stringify(selector)})].slice(0, 30).map((el) => (el.getAttribute('aria-label') ?? el.textContent).replace(/[\\u2066-\\u2069]/g, '').slice(0, 30) + ' ' + Math.round(el.getBoundingClientRect().height))`);
      log('list:', JSON.stringify(await heights('main button, main [role=radio]')));
      await d.go(file(SARA));
      await d.until(`!!document.querySelector('main h3')`, 'the file');
      log('file:', JSON.stringify(await heights('main button')));
    } finally {
      b.chrome.kill();
    }
  },

  /** The width break: the file's cards' grid, at 1440 (the class removed by hand, then restored). */
  async gridshot() {
    const { b, d } = await session('owner', 'en', 1440, file(SARA));
    try {
      await d.until(`!!document.querySelector('main h3')`, 'the file');
      const columns = await d.evaluate(`getComputedStyle(document.querySelector('main section .grid')).gridTemplateColumns`);
      log('the cards’ grid columns:', columns);
      await fullShot(d, process.argv[3] ?? `3-grid-owner-${tag('en', 1440)}`);
    } finally {
      b.chrome.kill();
    }
  },
};

const run = cases[process.argv[2]];
if (!run) throw new Error(`no case ${process.argv[2]}`);
await run();
