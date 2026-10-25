// DESK_SCREENS PR 1a's real run: the desk as the owner and as reception, Arabic light and English dark.
// Usage: node run1a.mjs <case>   cases: offline checkin2 layouts touch checkout1 checkout2 override closure
// widthbreak switch. The demo password is read from apps/api/.env and never printed. Enter is sent with its
// text ('\r'). Writes only PR 1a's listed writes (§13), each named in its case.
import { readFileSync, writeFileSync } from 'node:fs';
import { byLabel, byText, driver, launch, SHOTS } from './cdp1a.mjs';


const env = readFileSync('C:/dev/masaha/app/apps/api/.env', 'utf8');
const PASSWORD = /^SEED_DEMO_PASSWORD=(.*)$/m.exec(env)?.[1]?.trim().replace(/^["']|["']$/g, '');
if (!PASSWORD) throw new Error('no SEED_DEMO_PASSWORD');
const ACCOUNTS = {
  owner: 'demo-owner@example.com',
  reception: 'demo-reception@example.com',
  directory: 'demo-directory-owner@example.com',
};
const THEME = { ar: 'light', en: 'dark' };
const tag = (language, width) => `${language}-${THEME[language]}-${width}`;
const clean = (text) => (text ?? '').replace(/[\u2066-\u2069]/g, '');
const log = (...a) => console.log('·', ...a);
const W = {
  ar: { checkIn: '^تسجيل زيارة$', more: 'إجراءات أخرى', switchStaff: '^تبديل الموظف$', none: '^لم يدفع شيئًا$', full: 'ممتلئ', d30: '^30 د$', back: 'العودة للحالة التلقائية', out: (name) => `^خروج ${name}$` },
  en: { checkIn: '^Check in a visit$', more: 'More actions', switchStaff: '^Switch staff$', none: '^Paid nothing$', full: 'Full', d30: '^30 min$', back: 'Back to the automatic status', out: (name) => `^Check out ${name}$` },
};

async function session(role, language, width, space = 7) {
  const b = await launch();
  const d = driver(b);
  d.b = b;
  d.requests = [];
  await b.send('Network.enable');
  b.on((m) => {
    if (m.method === 'Network.requestWillBeSent' && m.params.request.url.includes('/api/v1/manage/')) {
      d.requests.push({
        id: m.params.requestId,
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
  const desk = `/dashboard/spaces/${space}/desk`;
  await d.go(`/login?next=${encodeURIComponent(desk)}`);
  await d.until(`!!document.querySelector('input[type=email]')`, 'login form');
  await d.type('input[type=email]', ACCOUNTS[role]);
  await d.type('input[type=password]', PASSWORD);
  await d.click(`document.querySelector('form button[type=submit]')`, 'sign in');
  await d.until(`location.pathname === ${JSON.stringify(desk)}`, 'the desk', 20000);
  // A sign-in takes the account's language; the case's language is set again, then the desk read anew.
  await d.prefs(language, THEME[language]);
  await d.go(desk);
  await d.until(`!!document.querySelector('main section[aria-labelledby] h2')`, 'the present list', 20000);
  await d.sleep(2500);
  return { b, d };
}

async function openCheckIn(d, language, width) {
  const where = width < 768 ? '[data-slot=page-action-bar] button' : 'header button';
  await d.click(byText(where, W[language].checkIn), 'check in a visit');
  await d.until(`!!document.querySelector('[role=dialog] input')`, 'the check-in dialog');
  await d.sleep(500);
}

async function typeIn(d, selector, text) {
  await d.evaluate(`(() => { const el = document.querySelector(${JSON.stringify(selector)}); el.focus(); el.select?.(); return true; })()`);
  await d.b.send('Input.insertText', { text });
  await d.sleep(200);
}

const toastText = (d) => d.evaluate(`[...document.querySelectorAll('[data-sonner-toast]')].map((t) => t.getAttribute('data-type') + ': ' + t.innerText.replace(/[\\u2066-\\u2069]/g, '').replace(/\\n+/g, ' | ')).join(' || ')`);
const dialogText = (d) => d.evaluate(`(document.querySelector('[role=dialog]')?.innerText ?? '').replace(/[\\u2066-\\u2069]/g, '').replace(/\\n+/g, ' | ')`);
const presentRows = (d) => d.evaluate(`[...document.querySelectorAll('main [data-present-action]')].length`);

async function checkIn(d, language, width, name, { offline = false } = {}) {
  await openCheckIn(d, language, width);
  await typeIn(d, '[role=dialog] input', name);
  if (offline) {
    await d.b.send('Network.emulateNetworkConditions', { offline: true, latency: 0, downloadThroughput: -1, uploadThroughput: -1 });
  }
  await d.click(`document.querySelector('[role=dialog] button[type=submit]')`, 'submit');
  return name;
}

const cases = {
  /** Reception checks in «زائر تجربة 1» with the first send offline, then «إعادة المحاولة» online: one key. */
  async offline() {
    const language = 'ar';
    const width = 1440;
    const { b, d } = await session('reception', language, width);
    try {
      await checkIn(d, language, width, 'زائر تجربة 1', { offline: true });
      await d.until(`!!document.querySelector('[role=dialog] [role=alert]')`, 'the lost answer', 20000);
      log('offline — the dialog says:', clean(await d.text(`document.querySelector('[role=dialog] [role=alert]')`)).replace(/\n+/g, ' | '));
      await d.shot(`1a-offline-lost-reception-${tag(language, width)}`);
      await b.send('Network.emulateNetworkConditions', { offline: false, latency: 0, downloadThroughput: -1, uploadThroughput: -1 });
      await d.click(byText('[role=dialog] [role=alert] button', '^إعادة المحاولة$'), 'retry');
      await d.until(`document.querySelectorAll('[data-sonner-toast]').length > 0`, 'the toast', 20000);
      await d.sleep(1500);
      log('online retry — toast:', await toastText(d));
      await d.shot(`1a-offline-retried-reception-${tag(language, width)}`);
      const posts = d.requests.filter((r) => r.method === 'POST' && r.url.endsWith('/visits'));
      const keys = [...new Set(posts.map((r) => r.key))];
      const lines = posts.map((r) => `${r.method} ${r.url} ${r.status} Idempotency-Key: ${r.key}`);
      log('the check-in requests:', lines.length, '· distinct keys:', keys.length);
      for (const line of lines) log('  ', line);
      await d.sleep(3000);
      const named = await d.evaluate(`[...document.querySelectorAll('main [data-present-action]')].filter((el) => (el.querySelector('button')?.getAttribute('aria-label') ?? '').includes('زائر تجربة 1')).length`);
      log('rows of «زائر تجربة 1» in the present list:', named);
      writeFileSync(`${SHOTS}/1a-offline-network.txt`, `${lines.join('\n')}\ndistinct keys: ${keys.length}\nrows of «زائر تجربة 1»: ${named}\n`);
    } finally {
      b.chrome.kill();
    }
  },

  /** Reception checks in «زائر تجربة 2» from the bar at the foot, on a phone. */
  async checkin2() {
    const language = 'ar';
    const width = 390;
    const { b, d } = await session('reception', language, width);
    try {
      await d.shot(`1a-bar-reception-${tag(language, width)}`);
      await openCheckIn(d, language, width);
      await typeIn(d, '[role=dialog] input', 'زائر تجربة 2');
      log('check-in dialog:', await dialogText(d));
      await d.shot(`1a-checkin-dialog-reception-${tag(language, width)}`);
      await d.click(`document.querySelector('[role=dialog] button[type=submit]')`, 'submit');
      await d.until(`document.querySelectorAll('[data-sonner-toast]').length > 0`, 'the toast', 20000);
      await d.sleep(1200);
      log('toast:', await toastText(d));
      await d.shot(`1a-checkin-toast-reception-${tag(language, width)}`);
      const post = d.requests.filter((r) => r.method === 'POST');
      log('requests:', post.map((r) => `${r.method} ${r.url} ${r.status} key ${r.key}`).join(' ; '));
    } finally {
      b.chrome.kill();
    }
  },

  /** The desk's layouts that change with width, both roles, both languages. */
  async layouts() {
    for (const role of ['owner', 'reception']) {
      for (const language of ['ar', 'en']) {
        for (const width of [390, 768, 1440]) {
          const { b, d } = await session(role, language, width);
          try {
            log(role, tag(language, width), 'rows:', await presentRows(d), '· table:', await d.evaluate(`!!document.querySelector('main table')`), '· bar shown:', await d.evaluate(`!document.querySelector('[data-slot=page-action-bar]').hidden`));
            await d.shot(`1a-desk-${role}-${tag(language, width)}`);
            if (width === 390) {
              await d.openMenu(byLabel('header button', W[language].more), 'more');
              await d.shot(`1a-desk-menu-${role}-${tag(language, width)}`);
            }
          } finally {
            b.chrome.kill();
          }
        }
      }
    }
  },

  /** The touch targets at 390 with touch emulation: «خروج» and the bar's «تسجيل زيارة». */
  async touch() {
    const language = 'ar';
    const width = 390;
    const { b: b2, d } = await session('reception', language, width);
    try {
      await b2.send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
      await b2.send('Emulation.setEmitTouchEventsForMouse', { enabled: true, configuration: 'mobile' });
      await d.go('/dashboard/spaces/7/desk');
      await d.until(`!!document.querySelector('main [data-present-action] button')`, 'a row action', 20000);
      await d.sleep(1500);
      const sizes = await d.evaluate(`(() => {
        const coarse = matchMedia('(pointer: coarse)').matches;
        const out = [...document.querySelectorAll('main [data-present-action] button')].map((el) => ({ name: el.getAttribute('aria-label'), height: el.getBoundingClientRect().height }));
        const bar = document.querySelector('[data-slot=page-action-bar] button');
        return { coarse, rows: out, bar: bar ? bar.getBoundingClientRect().height : null };
      })()`);
      log('pointer coarse:', sizes.coarse);
      for (const row of sizes.rows) log('  «خروج»', clean(row.name), row.height, 'px');
      log('  the bar\'s «تسجيل زيارة»', sizes.bar, 'px');
      writeFileSync(`${SHOTS}/1a-touch-sizes.txt`, JSON.stringify(sizes, null, 2));
      await d.shot(`1a-touch-reception-${tag(language, width)}`);
    } finally {
      b2.chrome.kill();
    }
  },

  /** Reception checks «زائر تجربة 1» out, paid cash, with the change line. */
  async checkout1() {
    const language = 'en';
    const width = 1440;
    const { b, d } = await session('reception', language, width);
    try {
      await d.click(byLabel('main button', W[language].out('زائر تجربة 1')), 'check out 1');
      await d.until(`!!document.querySelector('[role=dialog] input[inputmode=decimal]')`, 'the money block', 20000);
      await d.sleep(800);
      log('check-out dialog (filled):', await dialogText(d));
      await typeIn(d, '[role=dialog] input[inputmode=decimal]', '20');
      log('after 20:', await dialogText(d));
      await d.shot(`1a-checkout-change-reception-${tag(language, width)}`);
      await d.click(`document.querySelector('[role=dialog] button[type=submit]')`, 'submit');
      await d.until(`document.querySelectorAll('[data-sonner-toast]').length > 0`, 'the toast', 20000);
      await d.sleep(1200);
      log('toast:', await toastText(d));
      await d.shot(`1a-checkout-paid-reception-${tag(language, width)}`);
      log('requests:', d.requests.filter((r) => r.method === 'POST').map((r) => `${r.method} ${r.url} ${r.status} key ${r.key}`).join(' ; '));
    } finally {
      b.chrome.kill();
    }
  },

  /** Reception checks «زائر تجربة 2» out with nothing received, left to +970599000301. */
  async checkout2() {
    const language = 'ar';
    const width = 390;
    const { b, d } = await session('reception', language, width);
    try {
      await d.click(byLabel('main button', W[language].out('زائر تجربة 2')), 'check out 2');
      await d.until(`!!document.querySelector('[role=dialog] input[inputmode=decimal]')`, 'the money block', 20000);
      await d.sleep(800);
      await d.click(byText('[role=dialog] button', W[language].none), 'paid nothing');
      await typeIn(d, '[role=dialog] input[type=tel]', '+970599000301');
      log('check-out dialog:', await dialogText(d));
      await d.shot(`1a-checkout-debt-reception-${tag(language, width)}`, 1400);
      await d.click(`document.querySelector('[role=dialog] button[type=submit]')`, 'submit');
      await d.until(`document.querySelectorAll('[data-sonner-toast]').length > 0`, 'the toast', 20000);
      await d.sleep(1200);
      await d.viewport(width, 900);
      log('toast:', await toastText(d));
      await d.shot(`1a-checkout-debt-toast-reception-${tag(language, width)}`);
      log('requests:', d.requests.filter((r) => r.method === 'POST').map((r) => `${r.method} ${r.url} ${r.status} key ${r.key}`).join(' ; '));
    } finally {
      b.chrome.kill();
    }
  },

  /** The owner sets «ممتلئ» for 30 minutes, then returns to the automatic status. */
  async override() {
    for (const [language, width] of [['ar', 1440], ['en', 390]]) {
      const { b, d } = await session('owner', language, width);
      try {
        const trigger = `document.querySelector('header [data-slot=popover-trigger]')`;
        log(tag(language, width), 'trigger before:', clean(await d.evaluate(`${trigger}.getAttribute('aria-label')`)), '· shows:', clean(await d.text(trigger)));
        await d.click(trigger, 'the status control');
        await d.until(`!!document.querySelector('[data-slot=popover-content]')`, 'the panel');
        await d.shot(`1a-override-panel-owner-${tag(language, width)}`);
        if (language === 'ar') {
          await d.click(byText('[data-slot=popover-content] [role=radio]', W[language].full), 'full');
          await d.click(byText('[data-slot=popover-content] button', W[language].d30), '30 minutes');
          await d.until(`document.querySelectorAll('[data-sonner-toast]').length > 0`, 'the toast', 15000);
          await d.sleep(1000);
          log('set — toast:', await toastText(d), '· trigger:', clean(await d.evaluate(`${trigger}.getAttribute('aria-label')`)), '· shows:', clean(await d.text(trigger)));
          await d.shot(`1a-override-set-owner-${tag(language, width)}`);
          await d.click(trigger, 'the status control again');
          await d.until(`!!document.querySelector('[data-slot=popover-content]')`, 'the panel');
          await d.shot(`1a-override-inforce-owner-${tag(language, width)}`);
          await d.click(byText('[data-slot=popover-content] button', W[language].back), 'back to automatic');
          await d.sleep(1500);
          log('cleared — toast:', await toastText(d), '· trigger:', clean(await d.evaluate(`${trigger}.getAttribute('aria-label')`)));
          await d.shot(`1a-override-cleared-owner-${tag(language, width)}`);
          log('requests:', d.requests.filter((r) => r.url.includes('status-override')).map((r) => `${r.method} ${r.url} ${r.status}`).join(' ; '));
        }
      } finally {
        b.chrome.kill();
      }
    }
  },

  /** At the directory set's closure space: «زائر تجربة 3», the warning, then out unpaid to +970599000302. */
  async closure() {
    const language = 'ar';
    const width = 1440;
    const { b, d } = await session('directory', language, width, 52);
    try {
      const trigger = `document.querySelector('header [data-slot=popover-trigger]')`;
      log('the control at a closed space — disabled:', await d.evaluate(`${trigger}.disabled`), '· reason:', clean(await d.text(`${trigger}.parentElement`)));
      await d.shot(`1a-closure-desk-owner-${tag(language, width)}`);
      await checkIn(d, language, width, 'زائر تجربة 3');
      await d.until(`document.querySelectorAll('[data-sonner-toast]').length > 0`, 'the toast', 20000);
      await d.sleep(1500);
      log('toast:', await toastText(d));
      await d.shot(`1a-closure-warning-owner-${tag(language, width)}`);
      log('the check-in:', d.requests.filter((r) => r.method === 'POST').map((r) => `${r.method} ${r.url} ${r.status} key ${r.key}`).join(' ; '));
      await d.sleep(2500);
      await d.click(byLabel('main button', W[language].out('زائر تجربة 3')), 'check out 3');
      await d.until(`!!document.querySelector('[role=dialog] form')`, 'the check-out', 20000);
      await d.sleep(1000);
      if (await d.evaluate(`!!document.querySelector('[role=dialog] input[inputmode=decimal]')`)) {
        await d.click(byText('[role=dialog] button', W[language].none), 'paid nothing');
      }
      await typeIn(d, '[role=dialog] input[type=tel]', '+970599000302');
      log('check-out dialog:', await dialogText(d));
      await d.shot(`1a-closure-checkout-owner-${tag(language, width)}`);
      await d.click(`document.querySelector('[role=dialog] button[type=submit]')`, 'submit');
      await d.until(`[...document.querySelectorAll('[data-sonner-toast]')].some((t) => t.innerText.includes('خروج'))`, 'the check-out toast', 20000);
      await d.sleep(1200);
      log('toast:', await toastText(d));
      await d.shot(`1a-closure-out-owner-${tag(language, width)}`);
    } finally {
      b.chrome.kill();
    }
  },

  /** The desk at 1440 for the width break (the page's grid removed by hand around this run). */
  async widthbreak() {
    const language = 'ar';
    const width = 1440;
    const { b, d } = await session('owner', language, width);
    try {
      const listWidth = await d.evaluate(`Math.round(document.querySelector('main section[aria-labelledby]').getBoundingClientRect().width)`);
      const mainWidth = await d.evaluate(`Math.round(document.querySelector('main').getBoundingClientRect().width)`);
      log('the list\'s width:', listWidth, 'of main\'s', mainWidth);
      await d.shot(`1a-width-${process.argv[3] ?? 'grid'}-owner-${tag(language, width)}`);
    } finally {
      b.chrome.kill();
    }
  },

  /** Reception's «تبديل الموظف»: signed out, on sign-in with the desk to return to. */
  async switch() {
    const language = 'en';
    const width = 1440;
    const { b, d } = await session('reception', language, width);
    try {
      await d.click(byText('header button', W[language].switchStaff), 'switch staff');
      await d.until(`location.pathname === '/login'`, 'sign-in', 15000);
      await d.sleep(1000);
      log('after «Switch staff»:', decodeURIComponent(await d.evaluate('location.pathname + location.search')));
      await d.shot(`1a-switch-reception-${tag(language, width)}`);
    } finally {
      b.chrome.kill();
    }
  },
};

const name = process.argv[2];
if (!cases[name]) throw new Error(`no case ${name}`);
console.log(`== ${name}`);
await cases[name]();
