// DESK_SCREENS PR 1b's real run: «غير محصّل» and «بدون سعر» on the desk, as the owner and as reception, Arabic
// light and English dark. Usage: node run1b.mjs <case>   cases: layouts writeoff debt collect touch names
// The demo password is read from apps/api/.env and never printed. Enter is sent with its text ('\r'). Writes
// only PR 1b's listed writes (§13), each named in its case: on «خالد»'s visit (3) at masaha-demo, the owner's
// write-off and its undo, reception's «تسجيل دين» to +970599000303, then «تحصيل» 10 ₪ cash.
import { readFileSync, writeFileSync } from 'node:fs';
import { byLabel, byText, driver, launch, SHOTS } from './cdp1b.mjs';

const env = readFileSync('C:/dev/masaha/app/apps/api/.env', 'utf8');
const PASSWORD = /^SEED_DEMO_PASSWORD=(.*)$/m.exec(env)?.[1]?.trim().replace(/^["']|["']$/g, '');
if (!PASSWORD) throw new Error('no SEED_DEMO_PASSWORD');
const ACCOUNTS = { owner: 'demo-owner@example.com', reception: 'demo-reception@example.com' };
const THEME = { ar: 'light', en: 'dark' };
const tag = (language, width) => `${language}-${THEME[language]}-${width}`;
const clean = (text) => (text ?? '').replace(/[\u2066-\u2069]/g, '');
const log = (...a) => console.log('·', ...a);
const KHALID = 'خالد';
const W = {
  ar: { more: 'إجراءات أخرى', rowMore: `إجراءات أخرى لزيارة ${KHALID}`, writeOff: '^لن يُحصَّل…$', confirm: '^لن يُحصَّل$', undo: '^تراجع$', collect: '^تحصيل$', debt: '^تسجيل دين$', debtSubmit: '^تسجيل الدين$', retry: '^إعادة المحاولة$', showAll: '^عرض الكل' },
  en: { more: 'More actions', rowMore: `More actions for ${KHALID}’s visit`, writeOff: '^Write off…$', confirm: '^Write off$', undo: '^Undo$', collect: '^Collect$', debt: '^Record a debt$', debtSubmit: '^Record the debt$', retry: '^Try again$', showAll: '^Show all' },
};

async function session(role, language, width) {
  const b = await launch();
  const d = driver(b);
  d.b = b;
  d.requests = [];
  await b.send('Network.enable');
  b.on((m) => {
    if (m.method === 'Network.requestWillBeSent' && m.params.request.url.includes('/api/v1/manage/')) {
      d.requests.push({
        id: m.params.requestId,
        at: new Date().toISOString(),
        method: m.params.request.method,
        url: m.params.request.url.replace(/^https?:\/\/localhost:\d+/, ''),
        key: m.params.request.headers['Idempotency-Key'] ?? null,
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
  const desk = '/dashboard/spaces/7/desk';
  await d.go(`/login?next=${encodeURIComponent(desk)}`);
  await d.until(`!!document.querySelector('input[type=email]')`, 'login form');
  await d.type('input[type=email]', ACCOUNTS[role]);
  await d.type('input[type=password]', PASSWORD);
  await d.click(`document.querySelector('form button[type=submit]')`, 'sign in');
  await d.until(`location.pathname === ${JSON.stringify(desk)}`, 'the desk', 20000);
  // A sign-in takes the account's language; the case's language is set again, then the desk read anew.
  await d.prefs(language, THEME[language]);
  await d.go(desk);
  await d.until(`!!document.querySelector('#uncollected li')`, 'the uncollected rows', 20000);
  await d.sleep(2000);
  return { b, d };
}

const toastText = (d) => d.evaluate(`[...document.querySelectorAll('[data-sonner-toast]')].map((t) => t.getAttribute('data-type') + ': ' + t.innerText.replace(/[\\u2066-\\u2069]/g, '').replace(/\\n+/g, ' | ')).join(' || ')`);
const dialogText = (d) => d.evaluate(`(document.querySelector('[role=dialog], [role=alertdialog]')?.innerText ?? '').replace(/[\\u2066-\\u2069]/g, '').replace(/\\n+/g, ' | ')`);
const cardText = (d) => d.evaluate(`(document.querySelector('#uncollected')?.innerText ?? '').replace(/[\\u2066-\\u2069]/g, '').replace(/\\n+/g, ' | ')`);
/** Khalid's row's control matching `pattern`. */
const inKhalid = (pattern) => `(() => { const row = [...document.querySelectorAll('#uncollected li')].find((li) => li.innerText.includes(${JSON.stringify(KHALID)})); return row ? [...row.querySelectorAll('button')].find((el) => new RegExp(${JSON.stringify(pattern)}).test(el.textContent.replace(/[\\u2066-\\u2069]/g, ''))) : null; })()`;
const lines = (requests) => requests.map((r) => `${r.at} ${r.method} ${r.url} ${r.status ?? '(no answer)'} Idempotency-Key: ${r.key ?? 'none'}`);
const writes = (d) => d.requests.filter((r) => r.method !== 'GET');

async function typeIn(d, selector, text) {
  await d.evaluate(`(() => { const el = document.querySelector(${JSON.stringify(selector)}); el.focus(); el.select?.(); return true; })()`);
  await d.b.send('Input.insertText', { text });
  await d.sleep(200);
}

const cases = {
  /** The desk's layouts that change with width, both roles, both languages: the card's rows and its «⋯». */
  async layouts() {
    for (const role of ['owner', 'reception']) {
      for (const language of ['ar', 'en']) {
        for (const width of [390, 768, 1440]) {
          const { b, d } = await session(role, language, width);
          try {
            const box = await d.evaluate(`(() => { const r = (s) => { const e = document.querySelector(s); if (!e) return null; const b = e.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top), Math.round(b.width)]; }; return { list: r('main section[aria-labelledby]'), card: r('#uncollected'), unpriced: document.querySelectorAll('main [role=region]').length - 1 }; })()`);
            log(role, tag(language, width), 'present list [x, y, w]:', JSON.stringify(box.list), '· uncollected card:', JSON.stringify(box.card), '· other regions:', box.unpriced);
            log('   card:', await cardText(d));
            await d.shot(`1b-desk-${role}-${tag(language, width)}`, 1400);
            if (role === 'owner' && width === 390) {
              await d.openMenu(byLabel('#uncollected button', W[language].rowMore), 'the row menu');
              await d.shot(`1b-row-menu-owner-${tag(language, width)}`);
            }
          } finally {
            b.chrome.kill();
          }
        }
      }
    }
  },

  /** The owner writes «خالد»'s visit off with a reason, then undoes it from the toast. */
  async writeoff() {
    const language = 'ar';
    const width = 1440;
    const { b, d } = await session('owner', language, width);
    try {
      await d.openMenu(byLabel('#uncollected button', W[language].rowMore), 'the row menu');
      await d.click(byText('[role=menuitem]', W[language].writeOff), 'write off…');
      await d.until(`!!document.querySelector('[role=alertdialog] textarea')`, 'the write-off dialog');
      await d.sleep(500);
      log('dialog:', await dialogText(d));
      await typeIn(d, '[role=alertdialog] textarea', 'تجربة الشطب والتراجع (PR 1b)');
      await d.shot(`1b-writeoff-dialog-owner-${tag(language, width)}`);
      await d.click(byText('[role=alertdialog] button', W[language].confirm), 'write off');
      await d.until(`document.querySelectorAll('[data-sonner-toast]').length > 0`, 'the toast', 20000);
      await d.sleep(2000);
      log('toast:', await toastText(d));
      log('card after:', await cardText(d));
      log('focus after:', clean(await d.evaluate(`document.activeElement?.getAttribute('aria-label') ?? document.activeElement?.textContent ?? ''`)));
      await d.shot(`1b-writeoff-toast-owner-${tag(language, width)}`);
      // The toast stays: 12 s later it is still there, and nothing was sent again.
      await d.sleep(12000);
      log('12 s later — toast:', await toastText(d));
      await d.click(byText('[data-sonner-toast] button', W[language].undo), 'undo');
      await d.until(`[...document.querySelectorAll('[data-sonner-toast]')].some((t) => t.innerText.includes('أُعيدت'))`, 'the undone toast', 20000);
      await d.sleep(2000);
      log('after «تراجع» — toast:', await toastText(d));
      log('card after:', await cardText(d));
      await d.shot(`1b-writeoff-undone-owner-${tag(language, width)}`);
      await d.sleep(12000);
      const all = lines(writes(d));
      log('the writes, 12 s after the undo:', all.length);
      for (const line of all) log('  ', line);
      writeFileSync(`${SHOTS}/1b-writeoff-network.txt`, `${all.join('\n')}\n`);
    } finally {
      b.chrome.kill();
    }
  },

  /** Reception leaves «خالد»'s visit to +970599000303, on a phone. */
  async debt() {
    const language = 'ar';
    const width = 390;
    const { b, d } = await session('reception', language, width);
    try {
      await d.click(inKhalid(W[language].debt), 'record a debt');
      await d.until(`!!document.querySelector('[role=dialog] input[type=tel]')`, 'the debt dialog');
      await d.sleep(500);
      log('dialog:', await dialogText(d));
      log('focused:', await d.evaluate(`document.activeElement?.type + ' ' + (document.activeElement?.value ?? '')`));
      await typeIn(d, '[role=dialog] input[type=tel]', '+970599000303');
      await d.shot(`1b-debt-dialog-reception-${tag(language, width)}`);
      await d.enter();
      await d.until(`document.querySelectorAll('[data-sonner-toast]').length > 0`, 'the toast', 20000);
      await d.sleep(2000);
      log('toast:', await toastText(d));
      log('card after:', await cardText(d));
      await d.shot(`1b-debt-toast-reception-${tag(language, width)}`);
      const all = lines(writes(d));
      for (const line of all) log('  ', line);
      writeFileSync(`${SHOTS}/1b-debt-network.txt`, `${all.join('\n')}\n`);
    } finally {
      b.chrome.kill();
    }
  },

  /** Reception collects 10 ₪ cash on «خالد»'s visit, the first send offline, then «إعادة المحاولة». */
  async collect() {
    const language = 'en';
    const width = 1440;
    const { b, d } = await session('reception', language, width);
    try {
      await d.click(inKhalid(W[language].collect), 'collect');
      await d.until(`!!document.querySelector('[role=dialog] input[inputmode=decimal]')`, 'the collect dialog');
      await d.sleep(500);
      await typeIn(d, '[role=dialog] input[inputmode=decimal]', '10');
      await d.sleep(500);
      log('dialog:', await dialogText(d));
      await d.shot(`1b-collect-dialog-reception-${tag(language, width)}`);
      await b.send('Network.emulateNetworkConditions', { offline: true, latency: 0, downloadThroughput: -1, uploadThroughput: -1 });
      await d.enter();
      await d.until(`!!document.querySelector('[role=dialog] [role=alert]')`, 'the lost answer', 30000);
      log('offline — the dialog says:', clean(await d.text(`document.querySelector('[role=dialog] [role=alert]')`)).replace(/\n+/g, ' | '));
      await d.shot(`1b-collect-lost-reception-${tag(language, width)}`);
      await b.send('Network.emulateNetworkConditions', { offline: false, latency: 0, downloadThroughput: -1, uploadThroughput: -1 });
      await d.click(byText('[role=dialog] [role=alert] button', W[language].retry), 'retry');
      await d.until(`document.querySelectorAll('[data-sonner-toast]').length > 0`, 'the toast', 20000);
      await d.sleep(2500);
      log('toast:', await toastText(d));
      log('card after:', await cardText(d));
      await d.shot(`1b-collect-toast-reception-${tag(language, width)}`);
      const posts = writes(d);
      const keys = [...new Set(posts.map((r) => r.key))];
      const all = lines(posts);
      log('the payment requests:', all.length, '· distinct keys:', keys.length);
      for (const line of all) log('  ', line);
      writeFileSync(`${SHOTS}/1b-collect-network.txt`, `${all.join('\n')}\ndistinct keys: ${keys.length}\n`);
    } finally {
      b.chrome.kill();
    }
  },

  /** After the names' alignment fix: reception, English dark, at 390 and 1440 (reads only). */
  async names() {
    for (const width of [390, 1440]) {
      const { b, d } = await session('reception', 'en', width);
      try {
        const left = await d.evaluate(`[...document.querySelectorAll('#uncollected li span[dir=auto]')].map((el) => [el.textContent, Math.round(el.getBoundingClientRect().left - el.closest('li').getBoundingClientRect().left)])`);
        log(tag('en', width), 'names and their offset from the row start:', JSON.stringify(left));
        await d.shot(`1b-names-fixed-reception-${tag('en', width)}`, 1000);
      } finally {
        b.chrome.kill();
      }
    }
  },
  /** The touch targets at 390 with touch emulation: «تحصيل», «تسجيل دين», the row's «⋯» and the bar's button. */
  async touch() {
    const language = 'ar';
    const width = 390;
    for (const role of ['reception', 'owner']) {
      const { b, d } = await session(role, language, width);
      try {
        await b.send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
        await b.send('Emulation.setEmitTouchEventsForMouse', { enabled: true, configuration: 'mobile' });
        await d.go('/dashboard/spaces/7/desk');
        await d.until(`!!document.querySelector('#uncollected li button')`, 'a row action', 20000);
        await d.sleep(1500);
        const sizes = await d.evaluate(`(() => ({
          coarse: matchMedia('(pointer: coarse)').matches,
          rows: [...document.querySelectorAll('#uncollected li button')].map((el) => ({ name: (el.getAttribute('aria-label') ?? el.textContent).replace(/[\\u2066-\\u2069]/g, ''), height: el.getBoundingClientRect().height, width: el.getBoundingClientRect().width })),
          bar: document.querySelector('[data-slot=page-action-bar] button')?.getBoundingClientRect().height ?? null,
        }))()`);
        log(role, 'pointer coarse:', sizes.coarse, '· the bar\'s button:', sizes.bar, 'px');
        for (const row of sizes.rows) log('  ', row.name, row.height, '×', row.width, 'px');
        writeFileSync(`${SHOTS}/1b-touch-sizes-${role}.txt`, JSON.stringify(sizes, null, 2));
        await d.shot(`1b-touch-${role}-${tag(language, width)}`);
      } finally {
        b.chrome.kill();
      }
    }
  },
};

const name = process.argv[2];
if (!cases[name]) throw new Error(`no case ${name}`);
console.log(`== ${name}`);
await cases[name]();
