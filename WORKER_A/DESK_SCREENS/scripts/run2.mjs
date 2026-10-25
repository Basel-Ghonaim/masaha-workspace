// DESK_SCREENS PR 2's real run: the desk's search, a subscriber's check-in and check-out, «استلام».
// Usage: node run2.mjs <case>   cases: layouts searchnet sarain touch saraout yusuf rami
// The demo password is read from apps/api/.env and never printed; no phone is printed. Enter is sent with
// its text ('\r'). Writes only PR 2's listed writes (§13), as reception at masaha-demo: «سارة» checked in
// and out and «استلام» 5 ₪ on her subscription; «يوسف» checked in and out; «رامي»'s visit paid from
// «استلام دفعة». Every other case reads only.
import { readFileSync, writeFileSync } from 'node:fs';
import { byLabel, byText, driver, launch, SHOTS } from './cdp2.mjs';

const env = readFileSync('C:/dev/masaha/app/apps/api/.env', 'utf8');
const PASSWORD = /^SEED_DEMO_PASSWORD=(.*)$/m.exec(env)?.[1]?.trim().replace(/^["']|["']$/g, '');
if (!PASSWORD) throw new Error('no SEED_DEMO_PASSWORD');
const ACCOUNTS = { owner: 'demo-owner@example.com', reception: 'demo-reception@example.com' };
const THEME = { ar: 'light', en: 'dark' };
const tag = (language, width) => `${language}-${THEME[language]}-${width}`;
const clean = (text) => (text ?? '').replace(/[\u2066-\u2069]/g, '').replace(/\+?\d{9,}/g, '<phone>');
const log = (...a) => console.log('·', ...a.map((x) => (typeof x === 'string' ? clean(x) : x)));
const W = {
  ar: { checkIn: '^حضور ', anyway: '^تسجيل على أي حال$', retry: '^إعادة المحاولة$', receive: '^استلام$', pay: '^استلام دفعة$', pick: '^اختيار$', checkOut: '^خروج ', more: 'إجراءات أخرى' },
  en: { checkIn: '^Check in ', anyway: '^Check in anyway$', retry: '^Try again$', receive: '^Receive$', pay: '^Receive a payment$', pick: '^Choose$', checkOut: '^Check out ', more: 'More actions' },
};
const SEARCH = 'input[type=search][aria-controls]';

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
  await d.prefs(language, THEME[language]);
  await d.go(desk);
  await d.until(`!!document.querySelector(${JSON.stringify(SEARCH)})`, 'the search', 20000);
  await d.sleep(2000);
  return { b, d };
}

const toastText = (d) => d.evaluate(`[...document.querySelectorAll('[data-sonner-toast]')].map((t) => t.getAttribute('data-type') + ': ' + t.innerText.replace(/\\n+/g, ' | ')).join(' || ')`);
const dialogText = (d) => d.evaluate(`(document.querySelector('[role=dialog]')?.innerText ?? '').replace(/\\n+/g, ' | ')`);
const resultsText = (d) => d.evaluate(`(() => { const box = document.querySelector(${JSON.stringify(SEARCH)}); const r = document.getElementById(box.getAttribute('aria-controls')); return (r?.innerText ?? '').replace(/\\n+/g, ' | '); })()`);
const lines = (requests) => requests.map((r) => `${r.at} ${r.method} ${r.url} ${r.status ?? '(no answer)'} Idempotency-Key: ${r.key ?? 'none'}`);
const writes = (d) => d.requests.filter((r) => r.method !== 'GET');
const focused = (d) => d.evaluate(`(() => { const el = document.activeElement; return el ? el.tagName + ' ' + (el.getAttribute('type') ?? '') + ' ' + (el.getAttribute('aria-label') ?? el.textContent ?? '').slice(0, 40) : 'none'; })()`);

/** Types `text` into the search a character at a time, `gap` ms apart, then waits for the results. */
async function search(d, text, gap = 120) {
  await d.evaluate(`(() => { const el = document.querySelector(${JSON.stringify(SEARCH)}); el.focus(); el.select(); return true; })()`);
  for (const char of text) {
    await d.b.send('Input.insertText', { text: char });
    await d.sleep(gap);
  }
  await d.sleep(1500);
}

async function typeIn(d, selector, text) {
  await d.evaluate(`(() => { const el = document.querySelector(${JSON.stringify(selector)}); el.focus(); el.select?.(); return true; })()`);
  await d.b.send('Input.insertText', { text });
  await d.sleep(300);
}

const offline = (d, on) =>
  d.b.send('Network.emulateNetworkConditions', { offline: on, latency: 0, downloadThroughput: -1, uploadThroughput: -1 });

function saveNetwork(d, name) {
  const all = lines(writes(d));
  for (const line of all) log('  ', line);
  writeFileSync(`${SHOTS}/2-${name}-network.txt`, `${all.join('\n')}\n`);
}

const cases = {
  /** After the name's alignment fix: the card and the picker, English dark at 390 and 1440 (reads only). */
  async namefix() {
    for (const width of [390, 1440]) {
      const { b, d } = await session('owner', 'en', width);
      try {
        await search(d, 'سارة');
        const offset = await d.evaluate(`(() => { const h = document.querySelector('main h3'); const s = h.querySelector('span'); return Math.round(s.getBoundingClientRect().left - h.getBoundingClientRect().left); })()`);
        log(tag('en', width), "the card's name from its heading's start:", offset, 'px');
        await d.shot(`2-namefix-owner-${tag('en', width)}`, 1100);
      } finally {
        b.chrome.kill();
      }
    }
  },

  /** The search, its groups and a card, and the pay dialog's picker, both roles, both languages, 3 widths. */
  async layouts() {
    for (const role of ['owner', 'reception']) {
      for (const language of ['ar', 'en']) {
        for (const width of [390, 768, 1440]) {
          const { b, d } = await session(role, language, width);
          try {
            log(role, tag(language, width), 'focused on arrival:', await focused(d));
            await search(d, 'سارة');
            await d.until(`document.querySelectorAll('h3').length > 0`, 'a card', 15000);
            const grid = await d.evaluate(`[...document.querySelectorAll('main ul.grid > li')].map((li) => Math.round(li.getBoundingClientRect().width))`);
            log('   results:', await resultsText(d), '· card widths:', JSON.stringify(grid));
            await d.shot(`2-search-${role}-${tag(language, width)}`, 1400);
            await search(d, 'زائر لمرة');
            log('   no match:', await resultsText(d));
            await d.shot(`2-nomatch-${role}-${tag(language, width)}`, 1100);
            if (width >= 768) {
              await d.click(byText('main ~ * button, header button, button', W[language].pay), 'receive a payment');
            } else {
              await d.openMenu(byLabel('button', `^${W[language].more}$`), 'the page menu');
              await d.click(byText('[role=menuitem]', W[language].pay), 'receive a payment');
            }
            await d.until(`!!document.querySelector('[role=dialog] li')`, 'the debtors', 15000);
            await d.sleep(800);
            log('   pay picker:', await dialogText(d));
            await d.shot(`2-pay-picker-${role}-${tag(language, width)}`);
          } finally {
            b.chrome.kill();
          }
        }
      }
    }
  },

  /** The search asks the server once typing pauses: «سارة» typed a letter each 120 ms. */
  async searchnet() {
    const { b, d } = await session('reception', 'ar', 1440);
    try {
      const before = d.requests.length;
      await search(d, 'سارة', 120);
      const asked = d.requests.slice(before).filter((r) => r.url.includes('/customers'));
      log('typed 4 letters 120 ms apart → customer searches:', asked.length);
      for (const line of lines(asked)) log('  ', line);
      writeFileSync(`${SHOTS}/2-search-network.txt`, `${lines(asked).join('\n')}\n`);
    } finally {
      b.chrome.kill();
    }
  },

  /** Reception: «سارة»'s «حضور» (expired → the choice), «تسجيل على أي حال» first sent offline, then retried. */
  async sarain() {
    const language = 'ar';
    const width = 1440;
    const { b, d } = await session('reception', language, width);
    try {
      await search(d, 'سارة');
      await d.click(byLabel('button', W[language].checkIn), 'حضور');
      await d.until(`!!document.querySelector('[role=dialog]')`, 'the choice');
      await d.sleep(600);
      log('the choice:', await dialogText(d));
      await d.shot(`2-sara-choice-reception-${tag(language, width)}`);
      await offline(d, true);
      await d.click(byText('[role=dialog] button', W[language].anyway), 'check in anyway');
      await d.until(`!!document.querySelector('[role=dialog] [role=alert]')`, 'the lost answer', 30000);
      log('offline — the dialog says:', await d.text(`document.querySelector('[role=dialog] [role=alert]')`));
      await d.shot(`2-sara-lost-reception-${tag(language, width)}`);
      await offline(d, false);
      await d.click(byText('[role=dialog] [role=alert] button', W[language].retry), 'retry');
      await d.until(`document.querySelectorAll('[data-sonner-toast]').length > 0`, 'the toast', 20000);
      await d.sleep(2500);
      log('toast:', await toastText(d));
      log('the search after:', JSON.stringify(await d.evaluate(`document.querySelector(${JSON.stringify(SEARCH)}).value`)), '· focused:', await focused(d));
      await d.shot(`2-sara-in-reception-${tag(language, width)}`, 1300);
      const posts = writes(d);
      log('check-in requests:', posts.length, '· distinct keys:', new Set(posts.map((r) => r.key)).size);
      saveNetwork(d, 'sara-in');
    } finally {
      b.chrome.kill();
    }
  },

  /** The touch targets at 390 with touch emulation, «سارة» present: «خروج», «حضور», «استلام …», the bar. */
  async touch() {
    const { b, d } = await session('reception', 'ar', 390);
    try {
      await b.send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
      await d.go('/dashboard/spaces/7/desk');
      await d.until(`!!document.querySelector(${JSON.stringify(SEARCH)})`, 'the search', 20000);
      await d.sleep(1500);
      await search(d, 'ي');
      const sizes = await d.evaluate(`(() => ({
        coarse: matchMedia('(pointer: coarse)').matches,
        buttons: [...document.querySelectorAll('main button')].filter((el) => /^(حضور|خروج|استلام|تسجيل زيارة)/.test(el.textContent.replace(/[\\u2066-\\u2069]/g, ''))).map((el) => ({ name: (el.getAttribute('aria-label') ?? el.textContent).replace(/[\\u2066-\\u2069]/g, ''), height: el.getBoundingClientRect().height })),
        bar: document.querySelector('[data-slot=page-action-bar] button')?.getBoundingClientRect().height ?? null,
      }))()`);
      log('pointer coarse:', sizes.coarse, "· the bar's button:", sizes.bar, 'px');
      for (const x of sizes.buttons) log('  ', x.name, x.height, 'px');
      writeFileSync(`${SHOTS}/2-touch-sizes.txt`, clean(JSON.stringify(sizes, null, 2)));
      await d.shot('2-touch-reception-ar-light-390', 1400);
    } finally {
      b.chrome.kill();
    }
  },

  /** Reception: «سارة»'s one-tap «خروج» from the search, then «استلام» 5 ₪ from its toast, first sent offline. */
  async saraout() {
    const language = 'ar';
    const width = 1440;
    const { b, d } = await session('reception', language, width);
    try {
      log('present list:', await d.evaluate(`(document.querySelector('main section[aria-labelledby]')?.innerText ?? '').replace(/\\n+/g, ' | ')`));
      await search(d, 'سارة');
      log('results:', await resultsText(d));
      await d.shot(`2-sara-present-reception-${tag(language, width)}`, 1300);
      await d.click(`(() => { const box = document.querySelector(${JSON.stringify(SEARCH)}); const r = document.getElementById(box.getAttribute('aria-controls')); return ${byLabel('button', W[language].checkOut).replace('document.querySelectorAll', 'r.querySelectorAll')}; })()`, 'خروج in the search');
      await d.until(`document.querySelectorAll('[data-sonner-toast]').length > 0`, 'the toast', 20000);
      await d.sleep(2000);
      log('toast:', await toastText(d));
      log('the search after:', JSON.stringify(await d.evaluate(`document.querySelector(${JSON.stringify(SEARCH)}).value`)), '· focused:', await focused(d));
      await d.shot(`2-sara-out-reception-${tag(language, width)}`);
      await d.click(byText('[data-sonner-toast] button', W[language].receive), 'استلام in the toast');
      await d.until(`!!document.querySelector('[role=dialog] input[inputmode=decimal]')`, 'the pay dialog', 15000);
      await d.sleep(800);
      await typeIn(d, '[role=dialog] input[inputmode=decimal]', '5');
      log('pay dialog:', await dialogText(d));
      await d.shot(`2-sara-pay-reception-${tag(language, width)}`);
      await offline(d, true);
      await d.enter();
      await d.until(`!!document.querySelector('[role=dialog] [role=alert]')`, 'the lost answer', 30000);
      log('offline — the dialog says:', await d.text(`document.querySelector('[role=dialog] [role=alert]')`));
      await offline(d, false);
      await d.click(byText('[role=dialog] [role=alert] button', W[language].retry), 'retry');
      await d.until(`[...document.querySelectorAll('[data-sonner-toast]')].some((t) => t.innerText.includes('المتبقي'))`, 'the payment toast', 20000);
      await d.sleep(2000);
      log('toast:', await toastText(d));
      await d.shot(`2-sara-paid-reception-${tag(language, width)}`);
      const pays = writes(d).filter((r) => r.url.endsWith('/payments'));
      log('payment requests:', pays.length, '· distinct keys:', new Set(pays.map((r) => r.key)).size);
      saveNetwork(d, 'sara-out');
    } finally {
      b.chrome.kill();
    }
  },

  /** Reception, English dark at 768: «يوسف» checked in in one tap, then out from the search. */
  async yusuf() {
    const language = 'en';
    const width = 768;
    const { b, d } = await session('reception', language, width);
    try {
      await search(d, 'يوسف');
      await d.shot(`2-yusuf-card-reception-${tag(language, width)}`, 1100);
      await d.click(byLabel('button', W[language].checkIn), 'check in');
      await d.until(`document.querySelectorAll('[data-sonner-toast]').length > 0`, 'the toast', 20000);
      await d.sleep(2500);
      log('toast:', await toastText(d), '· dialog opened:', await d.evaluate(`!!document.querySelector('[role=dialog]')`));
      log('focused after:', await focused(d));
      await d.shot(`2-yusuf-in-reception-${tag(language, width)}`, 1100);
      await d.evaluate(`document.querySelectorAll('[data-sonner-toast] button[aria-label]').forEach((x) => x.click())`);
      await search(d, 'يوسف');
      log('results:', await resultsText(d));
      await d.click(byLabel('button', W[language].checkOut), 'check out');
      await d.until(`[...document.querySelectorAll('[data-sonner-toast]')].some((t) => /checked out/.test(t.innerText))`, 'the toast', 20000);
      await d.sleep(2000);
      log('toast:', await toastText(d));
      await d.shot(`2-yusuf-out-reception-${tag(language, width)}`, 1100);
      saveNetwork(d, 'yusuf');
    } finally {
      b.chrome.kill();
    }
  },

  /** Reception at 390: «رامي»'s visit debt paid from «استلام دفعة» (the page's «⋯»). */
  async rami() {
    const language = 'ar';
    const width = 390;
    const { b, d } = await session('reception', language, width);
    try {
      await d.openMenu(byLabel('button', `^${W[language].more}$`), 'the page menu');
      await d.click(byText('[role=menuitem]', W[language].pay), 'استلام دفعة');
      await d.until(`!!document.querySelector('[role=dialog] li')`, 'the debtors', 15000);
      await d.sleep(800);
      log('picker:', await dialogText(d));
      await d.click(`(() => { const li = [...document.querySelectorAll('[role=dialog] li')].find((x) => x.innerText.includes('رامي')); return li ? li.querySelector('button') : null; })()`, 'اختيار رامي');
      await d.until(`!!document.querySelector('[role=dialog] input[inputmode=decimal]')`, 'the items', 15000);
      await d.sleep(800);
      log('items:', await dialogText(d));
      await d.shot(`2-rami-pay-reception-${tag(language, width)}`, 1100);
      await d.enter();
      await d.until(`document.querySelectorAll('[data-sonner-toast]').length > 0`, 'the toast', 20000);
      await d.sleep(2000);
      log('toast:', await toastText(d));
      await d.shot(`2-rami-paid-reception-${tag(language, width)}`);
      saveNetwork(d, 'rami');
    } finally {
      b.chrome.kill();
    }
  },
};

const name = process.argv[2];
if (!cases[name]) throw new Error(`no case ${name}`);
console.log(`== ${name}`);
await cases[name]();
