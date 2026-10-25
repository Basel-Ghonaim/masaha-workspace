// DESK_SCREENS PR 4's real run: the subscription sheet. Usage: node run4.mjs <case>
//   cases: layouts newcustomer renewal custom carried touch widthshot
// The demo password is read from apps/api/.env and never printed; no phone is printed; an /auth/
// request's body is never kept. Enter is sent with its text ('\r'). Writes only PR 4's listed writes
// (§13), on masaha-demo: as reception — a new customer «مشترك تجربة» (+970599000305) on the published
// «أسبوعي», paid in full; «محمد عوض»'s renewal with his debt, paid in part; as owner — «مخصّص» with a
// reason on «رامي سالم». Every other case reads only.
import { readFileSync, writeFileSync } from 'node:fs';
import { byLabel, byText, driver, launch, SHOTS } from './cdp4.mjs';

const env = readFileSync('C:/dev/masaha/app/apps/api/.env', 'utf8');
const PASSWORD = /^SEED_DEMO_PASSWORD=(.*)$/m.exec(env)?.[1]?.trim().replace(/^["']|["']$/g, '');
if (!PASSWORD) throw new Error('no SEED_DEMO_PASSWORD');
const ACCOUNTS = { owner: 'demo-owner@example.com', reception: 'demo-reception@example.com' };
const THEME = { ar: 'light', en: 'dark' };
const tag = (language, width) => `${language}-${THEME[language]}-${width}`;
const clean = (text) => (text ?? '').replace(/[\u2066-\u2069]/g, '').replace(/\+?\d{9,}/g, '<phone>');
const log = (...a) => console.log('·', ...a.map((x) => (typeof x === 'string' ? clean(x) : x)));
const SPACE = '/dashboard/spaces/7';
const DESK = `${SPACE}/desk`;
const LIST = `${SPACE}/customers`;
const file = (id) => `${LIST}/${String(id)}`;
// The inventory's records (scripts\inventory4.out.txt).
const KHALED = 8;
const RAMI = 5;
const MOHAMMAD = 2;
const NEW_PHONE = ['+97059', '9000305'].join('');

async function session(role, language, width, landing = DESK) {
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
  await d.go(landing);
  await d.sleep(2500);
  return { b, d };
}

const toastText = (d) => d.evaluate(`[...document.querySelectorAll('[data-sonner-toast]')].map((t) => t.getAttribute('data-type') + ': ' + t.innerText.replace(/\\n+/g, ' | ')).join(' || ')`);
const sheetText = (d) => d.evaluate(`(document.querySelector('[role=dialog]')?.innerText ?? '').replace(/\\n+/g, ' | ')`);
const line = (r) =>
  `${r.at} ${r.method} ${r.url} ${r.status ?? '(no answer)'} Idempotency-Key: ${r.key ?? 'none'}${r.body ? ` body: ${clean(r.body)}` : ''}`;
const writes = (d) => d.requests.filter((r) => r.method !== 'GET' && !r.url.includes('/auth/'));

function saveNetwork(d, name, all = writes(d)) {
  const text = all.map(line);
  for (const l of text) log('  ', l);
  writeFileSync(`${SHOTS}/4-${name}-network.txt`, `${text.join('\n')}\n`);
}

/** The sheet's field by its label's start, focused, its text replaced. */
async function fill(d, label, text) {
  const ok = await d.evaluate(`(() => {
    const sheet = document.querySelector('[role=dialog]');
    const lab = [...sheet.querySelectorAll('label')].find((l) => new RegExp(${JSON.stringify(label)}).test(l.textContent.replace(/[\\u2066-\\u2069]/g, '')));
    const el = lab && document.getElementById(lab.htmlFor);
    if (!el) return false;
    el.scrollIntoView({ block: 'center' });
    el.focus();
    el.select?.();
    return true;
  })()`);
  if (!ok) throw new Error(`no field ${label}`);
  await d.b.send('Input.insertText', { text });
  await d.sleep(200);
}

const radio = (value) => `document.querySelector('[role=dialog] [role=radio][value=${JSON.stringify(value)}]')`;
const submit = `document.querySelector('[role=dialog] form button[type=submit]')`;
const sheetWidth = (d) => d.evaluate(`({ sheet: Math.round(document.querySelector('[role=dialog]').getBoundingClientRect().width), viewport: innerWidth })`);

async function openNew(d, width) {
  if (width >= 768) {
    await d.click(byText('main button, header button', '^(زبون جديد|New customer)$'), 'new customer');
  } else {
    await d.openMenu(byLabel('button', '^(إجراءات أخرى|More actions)$'), 'the desk’s «⋯»');
    await d.click(byText('[role=menuitem]', '^(زبون جديد|New customer)$'), 'new customer item');
  }
  await d.until(`!!document.querySelector('[role=dialog] [role=radio]')`, 'the sheet’s choices');
  await d.sleep(800);
}

async function openRenewal(d) {
  await d.until(`!!document.querySelector('main h3')`, 'the file');
  await d.click(byText('main button', '^(تجديد|Renew)$'), 'renew');
  await d.until(`!!document.querySelector('[role=dialog]') && /(تغيير الباقة|Change package)/.test(document.querySelector('[role=dialog]').innerText)`, 'the renewal sheet');
  await d.sleep(800);
}

async function fullSheetShot(d, name) {
  await d.shot(name);
}

const cases = {
  /** The sheet at three widths, both languages: reception's new customer, the owner's renewal (reads only). */
  async layouts() {
    for (const language of ['ar', 'en']) {
      for (const width of [390, 768, 1440]) {
        {
          const { b, d } = await session('reception', language, width, DESK);
          try {
            await openNew(d, width);
            log('reception new', tag(language, width), JSON.stringify(await sheetWidth(d)));
            log('   ', await sheetText(d));
            await fullSheetShot(d, `4-new-reception-${tag(language, width)}`);
          } finally {
            b.chrome.kill();
          }
        }
        {
          const { b, d } = await session('owner', language, width, file(MOHAMMAD));
          try {
            await openRenewal(d);
            log('owner renewal', tag(language, width), JSON.stringify(await sheetWidth(d)));
            log('   ', await sheetText(d));
            await fullSheetShot(d, `4-renewal-owner-${tag(language, width)}`);
          } finally {
            b.chrome.kill();
          }
        }
      }
    }
  },

  /**
   * Reception: «مشترك تجربة» on the published «أسبوعي», paid in full. The subscribe is blocked once
   * (no answer), so the customer is saved and the subscribe is sent again, alone, with its key.
   */
  async newcustomer() {
    const { b, d } = await session('reception', 'ar', 1440, DESK);
    try {
      await openNew(d, 1440);
      await fill(d, '^الاسم', 'مشترك تجربة');
      await fill(d, '^رقم الجوال', NEW_PHONE);
      await d.click(radio('price-WEEK-GENERAL-none'), 'the published weekly');
      await d.sleep(500);
      log('sheet:', await sheetText(d));
      await d.shot(`4-newcustomer-filled-reception-${tag('ar', 1440)}`);
      await b.send('Network.setBlockedURLs', { urls: ['*/customers/*/subscriptions*'] });
      await d.click(submit, 'save');
      await d.until(`/لم يصل الرد/.test(document.querySelector('[role=dialog]')?.innerText ?? '')`, 'the lost line', 30000);
      log('after the blocked subscribe:', await sheetText(d));
      await d.shot(`4-newcustomer-half-reception-${tag('ar', 1440)}`);
      await b.send('Network.setBlockedURLs', { urls: [] });
      await d.click(byText('[role=dialog] button', '^(إعادة المحاولة|Try again)$'), 'try again');
      await d.until(`!document.querySelector('[role=dialog]')`, 'the sheet closed', 20000);
      await d.sleep(800);
      log('toast:', await toastText(d));
      await d.shot(`4-newcustomer-done-reception-${tag('ar', 1440)}`);
      saveNetwork(d, 'newcustomer');
    } finally {
      b.chrome.kill();
    }
  },

  /** Reception: «محمد عوض»'s renewal over his ₪50 debt, ₪120 received of ₪200 (the toast's parts). */
  async renewal() {
    const { b, d } = await session('reception', 'ar', 1440, file(MOHAMMAD));
    try {
      await openRenewal(d);
      log('sheet:', await sheetText(d));
      log('from:', await d.evaluate(`document.querySelector('[role=dialog] input[type=date]').value`));
      await fill(d, '^المستلم الآن', '120');
      await d.sleep(500);
      log('submit:', await d.text(submit));
      await d.shot(`4-renewal-filled-reception-${tag('ar', 1440)}`);
      await d.click(submit, 'renew');
      await d.until(`!document.querySelector('[role=dialog]')`, 'the sheet closed', 20000);
      await d.sleep(800);
      log('toast:', await toastText(d));
      await d.shot(`4-renewal-done-reception-${tag('ar', 1440)}`);
      saveNetwork(d, 'renewal');
    } finally {
      b.chrome.kill();
    }
  },

  /** The owner: «مخصّص» with a reason on «رامي سالم», paid in full. */
  async custom() {
    const { b, d } = await session('owner', 'ar', 1440, file(RAMI));
    try {
      await d.until(`!!document.querySelector('main h1, main h2')`, 'the file');
      await d.openMenu(byLabel('button', '^(إجراءات أخرى|More actions): رامي سالم$'), 'the «⋯»');
      await d.click(byText('[role=menuitem]', '^اشتراك جديد$'), 'new subscription');
      await d.until(`!!document.querySelector('[role=dialog] [role=radio]')`, 'the sheet');
      await d.click(radio('custom'), 'custom');
      await d.sleep(500);
      await fill(d, '^السعر', '80');
      await fill(d, '^سبب السعر', 'عرض المالك لتجربة الأسبوع');
      await d.sleep(500);
      log('sheet:', await sheetText(d));
      await d.shot(`4-custom-filled-owner-${tag('ar', 1440)}`);
      await d.click(submit, 'save');
      await d.until(`!document.querySelector('[role=dialog]')`, 'the sheet closed', 20000);
      await d.sleep(800);
      log('toast:', await toastText(d));
      await d.shot(`4-custom-done-owner-${tag('ar', 1440)}`);
      saveNetwork(d, 'custom');
    } finally {
      b.chrome.kill();
    }
  },

  /** Carried F1 live: the focus back on «⋯» after the edit (closed) and the owing archive's question. */
  async carried() {
    const { b, d } = await session('owner', 'ar', 1440, LIST);
    try {
      await d.until(`document.querySelectorAll('main a[href*="/customers/"]').length > 0`, 'the rows');
      const trigger = byLabel('button', '^إجراءات أخرى: خالد$');
      const focused = () => d.evaluate(`(document.activeElement?.getAttribute('aria-label') ?? document.activeElement?.tagName ?? '').replace(/[\\u2066-\\u2069]/g, '')`);
      await d.openMenu(trigger, 'khaled’s «⋯»');
      await d.click(byText('[role=menuitem]', '^تعديل البيانات$'), 'edit');
      await d.until(`!!document.querySelector('[role=dialog]')`, 'the edit dialog');
      await d.key('Escape', 'Escape', 27);
      await d.sleep(600);
      log('after the edit dialog, the focus:', await focused());
      await d.shot(`4-carried-edit-owner-${tag('ar', 1440)}`);
      await d.openMenu(trigger, 'khaled’s «⋯» again');
      await d.click(byText('[role=menuitem]', '^أرشفة…$'), 'archive');
      await d.until(`!!document.querySelector('[role=alertdialog]')`, 'the archive question');
      await d.click(byText('[role=alertdialog] button', '^رجوع$'), 'back');
      await d.sleep(600);
      log('after the archive question, the focus:', await focused());
      await d.shot(`4-carried-archive-owner-${tag('ar', 1440)}`);
      saveNetwork(d, 'carried');
    } finally {
      b.chrome.kill();
    }
  },

  /** Touch targets at 390 in the sheet. */
  async touch() {
    const { b, d } = await session('reception', 'ar', 390, file(MOHAMMAD));
    try {
      await b.send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 1 });
      await d.go(file(MOHAMMAD));
      await openRenewal(d);
      const heights = (selector) => d.evaluate(`[...document.querySelectorAll(${JSON.stringify(selector)})].slice(0, 30).map((el) => (el.getAttribute('aria-label') ?? el.textContent).replace(/[\\u2066-\\u2069]/g, '').slice(0, 30) + ' ' + Math.round(el.getBoundingClientRect().height))`);
      log('renewal sheet:', JSON.stringify(await heights('[role=dialog] button, [role=dialog] input')));
      await d.click(byText('[role=dialog] button', '^تغيير الباقة$'), 'change package');
      await d.sleep(500);
      log('radios:', await d.evaluate(`document.querySelectorAll('[role=dialog] [role=radio]').length`));
      log('choices:', JSON.stringify(await d.evaluate(`[...document.querySelectorAll('[role=dialog] [role=radio]')].map((el) => (el.closest('label')?.textContent ?? '').replace(/[\u2066-\u2069]/g, '').slice(0, 24) + ' ' + Math.round(el.closest('label')?.getBoundingClientRect().height ?? 0))`)));
      await d.shot(`4-touch-reception-${tag('ar', 390)}`);
    } finally {
      b.chrome.kill();
    }
  },

  /** The width break's shot: the sheet at 390 (the class removed by hand, then restored). */
  async widthshot() {
    const { b, d } = await session('reception', 'ar', 390, DESK);
    try {
      await openNew(d, 390);
      log('sheet width at 390:', JSON.stringify(await sheetWidth(d)));
      await d.shot(process.argv[3] ?? `4-width-reception-${tag('ar', 390)}`);
    } finally {
      b.chrome.kill();
    }
  },
};

const run = cases[process.argv[2]];
if (!run) throw new Error(`no case ${process.argv[2]}`);
await run();
