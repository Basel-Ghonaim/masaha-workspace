// PAYMENTS_STEP10 PR 1's real run: «الدفعات», «إلغاء الدفعة…» (ledger and statement), «دفعاتي اليوم».
// Usage: node run1.mjs <case>   cases: pay mine ledger voidLedger voidStatement mineAfter touch width
// The demo password is read from apps/api/.env and never printed; no /auth/ request's body is kept; no
// phone is printed. Enter is sent with its text ('\r'). Writes only PR 1's named writes (§13): as
// reception, ₪1 cash on subscription 1 (customer 1) and ₪1 on visit 3 (customer 8); as the owner, the
// void of the visit's ₪1 from the ledger and of the subscription's ₪1 from its statement («دفعة تجربة»).
import { readFileSync, writeFileSync } from 'node:fs';
import { byLabel, byText, driver, launch, SHOTS } from './cdp1.mjs';

const env = readFileSync('C:/dev/masaha/app/apps/api/.env', 'utf8');
const PASSWORD = /^SEED_DEMO_PASSWORD=(.*)$/m.exec(env)?.[1]?.trim().replace(/^["']|["']$/g, '');
if (!PASSWORD) throw new Error('no SEED_DEMO_PASSWORD');
const ACCOUNTS = { owner: 'demo-owner@example.com', reception: 'demo-reception@example.com' };
const THEME = { ar: 'light', en: 'dark' };
const tag = (language, width) => `${language}-${THEME[language]}-${width}`;
const clean = (text) => (text ?? '').replace(/[\u2066-\u2069]/g, '').replace(/\+?\d{9,}/g, '<phone>');
const log = (...a) => console.log('·', ...a.map((x) => (typeof x === 'string' ? clean(x) : x)));
const SPACE = '/dashboard/spaces/7';
const LEDGER = `${SPACE}/payments`;
const MINE = `${SPACE}/my-payments`;
const file = (id) => `${SPACE}/customers/${String(id)}`;
// The inventory's records (scripts\inventory1.out.txt).
const SARA = 1;
const KHALID = 8;
const REASON = 'دفعة تجربة';

async function session(role, language, width, landing) {
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
  // The account's language may have replaced the stored one on sign-in: the page is opened again.
  await d.go(landing);
  await d.until(`document.documentElement.lang === ${JSON.stringify(language)}`, `the ${language} interface`, 20000);
  await d.sleep(2500);
  return { b, d };
}

const toastText = (d) => d.evaluate(`[...document.querySelectorAll('[data-sonner-toast]')].map((t) => t.getAttribute('data-type') + ': ' + t.innerText.replace(/\\n+/g, ' | ')).join(' || ')`);
const dialogText = (d) => d.evaluate(`(document.querySelector('[role=dialog],[role=alertdialog]')?.innerText ?? '').replace(/\\n+/g, ' | ')`);
const mainText = (d) => d.evaluate(`(document.querySelector('main')?.innerText ?? '').replace(/\\n+/g, ' | ').slice(0, 1500)`);
const focused = (d) => d.evaluate(`(() => { const el = document.activeElement; return el ? el.tagName + ' ' + (el.getAttribute('aria-label') ?? el.innerText ?? '').replace(/\\n+/g, ' | ').slice(0, 120) : 'none'; })()`);
const line = (r) =>
  `${r.at} ${r.method} ${r.url} ${r.status ?? '(no answer)'} Idempotency-Key: ${r.key ?? 'none'}${r.body ? ` body: ${clean(r.body)}` : ''}`;
const writes = (d) => d.requests.filter((r) => r.method !== 'GET' && !r.url.includes('/auth/'));
const ledgerReads = (d) => d.requests.filter((r) => r.method === 'GET' && /\/payments(\?|$)/.test(r.url));

function saveNetwork(d, name, all = writes(d)) {
  const text = all.map(line);
  for (const l of text) log('  ', l);
  writeFileSync(`${SHOTS}/1-${name}-network.txt`, `${text.join('\n')}\n`);
}

async function fullShot(d, name) {
  const height = await d.evaluate('Math.min(4000, Math.max(900, document.documentElement.scrollHeight))');
  await d.shot(name, height);
}

/** Types `text` into the dialog's field labelled `label`. */
async function fill(d, label, text) {
  const ok = await d.evaluate(`(() => {
    const dialog = document.querySelector('[role=dialog],[role=alertdialog]');
    const lab = [...dialog.querySelectorAll('label')].find((l) => new RegExp(${JSON.stringify(label)}).test(l.textContent.replace(/[\\u2066-\\u2069]/g, '')));
    const el = lab && document.getElementById(lab.htmlFor);
    if (!el) return false;
    el.scrollIntoView({ block: 'center' });
    el.focus();
    el.select?.();
    return true;
  })()`);
  if (!ok) throw new Error(`no field ${label}`);
  await d.b.send('Input.insertText', { text });
  await d.sleep(300);
}

const submit = `document.querySelector('[role=dialog] button[type=submit],[role=alertdialog] button[type=submit]')`;

/** Receives ₪1 in the payment dialog that is open, and waits for it to close. */
async function payOne(d, name) {
  await d.until(`!!document.querySelector('[role=dialog]')`, 'the payment dialog');
  await fill(d, '^المستلم الآن', '1');
  log(name, 'dialog:', await dialogText(d));
  await d.shot(`1-pay-${name}-reception-${tag('ar', 1440)}`);
  await d.click(submit, 'record');
  await d.until(`!document.querySelector('[role=dialog]')`, 'the dialog closed', 20000);
  await d.sleep(800);
  log(name, 'toast:', await toastText(d));
}

/** Voids the payment whose «⋯» is named `who`, with the run's reason. */
async function voidOne(d, who, name) {
  // The amount reads «‏1 ₪» in Arabic (a right-to-left mark first) and "₪1" in English.
  const trigger = byLabel('button', `^(إجراءات الدفعة|Payment actions): (.?1.₪|₪1) · ${who}$`);
  log(name, 'the «⋯» labels:', await d.evaluate(`[...document.querySelectorAll('main [data-row-action]')].slice(0, 3).map((el) => el.getAttribute('aria-label').replace(/[⁦-⁩]/g, ''))`));
  await d.openMenu(trigger, `the «⋯» of ₪1 · ${who}`);
  log(name, 'menu:', await d.evaluate(`[...document.querySelectorAll('[role=menu]')].map((m) => m.getAttribute('aria-label') + ' → ' + m.innerText).join(' || ')`));
  await d.click(byText('[role=menuitem]', '^(إلغاء الدفعة…|Void payment…)$'), 'void payment…');
  await d.until(`!!document.querySelector('[role=alertdialog]')`, 'the void dialog');
  log(name, 'focus on opening:', await focused(d));
  log(name, 'dialog:', await dialogText(d));
  await d.shot(`1-void-${name}-dialog-owner-${tag('ar', 1440)}`);
  await d.b.send('Input.insertText', { text: REASON });
  await d.sleep(300);
  await d.click(submit, 'void');
  await d.until(`!document.querySelector('[role=alertdialog]')`, 'the dialog closed', 20000);
  await d.sleep(2500);
  log(name, 'toast:', await toastText(d));
  log(name, 'focus after:', await focused(d));
  await d.shot(`1-void-${name}-done-owner-${tag('ar', 1440)}`);
}

const cases = {
  /** Reception: ₪1 on Sara's subscription (its «استلام المتبقي») and ₪1 on Khalid's visit («تحصيل»). */
  async pay() {
    const { b, d } = await session('reception', 'ar', 1440, file(SARA));
    try {
      await d.until(`!!document.querySelector('main h3')`, 'the cards');
      await d.click(byText('main button', '^استلام المتبقي$'), 'receive the rest');
      await payOne(d, 'subscription');
      await d.go(file(KHALID));
      await d.until(`!!document.querySelector('main h2')`, 'the file');
      await d.click(byText('main button', '^تحصيل$'), 'collect');
      await payOne(d, 'visit');
      saveNetwork(d, 'pay');
    } finally {
      b.chrome.kill();
    }
  },

  /** Reception's «دفعاتي اليوم», both languages, three widths (reads only). */
  async mine(name = 'mine') {
    for (const language of ['ar', 'en']) {
      for (const width of [390, 768, 1440]) {
        const { b, d } = await session('reception', language, width, MINE);
        try {
          await d.until(`[...document.querySelectorAll('main section, main [role=region]')].length > 0 && !document.querySelector('main [data-slot=skeleton]')`, 'the figures', 20000);
          await d.sleep(1000);
          log(name, tag(language, width), await mainText(d));
          await fullShot(d, `1-${name}-reception-${tag(language, width)}`);
          if (width === 1440 && language === 'ar') saveNetwork(d, name, ledgerReads(d));
        } finally {
          b.chrome.kill();
        }
      }
    }
  },

  /** The owner's ledger: today, a range, a staff member, «إظهار الملغاة», the phone's sheet (reads only). */
  async ledger() {
    for (const language of ['ar', 'en']) {
      for (const width of [390, 768, 1440]) {
        const { b, d } = await session('owner', language, width, LEDGER);
        try {
          await d.until(`!!document.querySelector('main p[aria-live]')`, 'the totals', 20000);
          await d.sleep(1000);
          log('today', tag(language, width), await mainText(d));
          await fullShot(d, `1-ledger-today-owner-${tag(language, width)}`);
          await d.go(`${LEDGER}?from=2026-09-27&to=2026-10-27&voided=1`);
          await d.until(`!!document.querySelector('main p[aria-live]') && /2026/.test(document.querySelector('main p[aria-live]').innerText)`, 'the month', 20000);
          await d.sleep(1000);
          log('month', tag(language, width), await mainText(d));
          await fullShot(d, `1-ledger-month-owner-${tag(language, width)}`);
          if (width === 390) {
            await d.click(byLabel('main button', '(فلتر|filter)'), 'the filters button');
            await d.until(`!!document.querySelector('[role=dialog]')`, 'the sheet');
            await d.sleep(600);
            log('sheet', tag(language, width), await dialogText(d));
            await d.shot(`1-ledger-sheet-owner-${tag(language, width)}`);
          }
          if (width === 1440 && language === 'ar') {
            await d.go(`${LEDGER}?from=2026-09-27&to=2026-10-27&staff=14`);
            await d.until(`!!document.querySelector('main p[aria-live]')`, 'the staff filter', 20000);
            await d.sleep(1000);
            log('staff=14', await mainText(d));
            await fullShot(d, `1-ledger-staff-owner-${tag(language, width)}`);
            await d.go(`${LEDGER}?from=2026-07-01&to=2026-10-27`);
            await d.sleep(2500);
            log('a 119-day address, dropped:', await d.evaluate('location.search'), await d.text(`document.querySelector('main p[aria-live]')`));
            saveNetwork(d, 'ledger', ledgerReads(d));
          }
        } finally {
          b.chrome.kill();
        }
      }
    }
  },

  /** The owner voids the visit's ₪1 from the ledger. */
  async voidLedger() {
    const { b, d } = await session('owner', 'ar', 1440, LEDGER);
    try {
      await d.until(`!!document.querySelector('main p[aria-live]')`, 'the totals', 20000);
      await d.sleep(1000);
      log('before:', await mainText(d));
      await voidOne(d, 'خالد', 'ledger');
      log('after:', await mainText(d));
      saveNetwork(d, 'void-ledger');
    } finally {
      b.chrome.kill();
    }
  },

  /** The owner voids the subscription's ₪1 from its statement in Sara's file. */
  async voidStatement() {
    const { b, d } = await session('owner', 'ar', 1440, file(SARA));
    try {
      await d.until(`!!document.querySelector('main h3')`, 'the cards');
      await d.click(byText('main button', '^عرض الكشف$'), 'show the statement');
      await d.until(`!!document.querySelector('main h4')`, 'the statement');
      await d.sleep(800);
      await fullShot(d, `1-statement-owner-${tag('ar', 1440)}`);
      await voidOne(d, 'سارة خالد', 'statement');
      await fullShot(d, `1-statement-after-owner-${tag('ar', 1440)}`);
      saveNetwork(d, 'void-statement');
    } finally {
      b.chrome.kill();
    }
  },

  /** Reception's «دفعاتي اليوم» after the voids. */
  async mineAfter() {
    await cases.mine('mine-after');
  },

  /** At 390 with touch: the ledger's «⋯» hit area. */
  async touch() {
    const { b, d } = await session('owner', 'ar', 390, `${LEDGER}?from=2026-09-27&to=2026-10-27`);
    try {
      await b.send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
      await d.go(`${LEDGER}?from=2026-09-27&to=2026-10-27`);
      await d.until(`!!document.querySelector('main [data-row-action]')`, 'a row action', 20000);
      const sizes = await d.evaluate(`[...document.querySelectorAll('main [data-row-action]')].slice(0, 3).map((el) => { const r = el.getBoundingClientRect(); return Math.round(r.width) + '×' + Math.round(r.height); })`);
      log('«⋯» hit areas at 390, touch:', sizes);
    } finally {
      b.chrome.kill();
    }
  },

  /** The 768 shot of the filters' grid, as it stands (the width break runs it again with the class removed). */
  async width(name = 'width') {
    const { b, d } = await session('owner', 'ar', 768, LEDGER);
    try {
      await d.until(`!!document.querySelector('main p[aria-live]')`, 'the totals', 20000);
      await d.sleep(1500);
      const columns = await d.evaluate(`(() => { const grid = document.querySelector('main .grid'); return grid ? getComputedStyle(grid).gridTemplateColumns : 'none'; })()`);
      log(name, 'filters grid columns at 768:', columns);
      await d.shot(`${name}-owner-${tag('ar', 768)}`);
    } finally {
      b.chrome.kill();
    }
  },
};

/** The desk's write-off dialog (existing code), opened and cancelled: where its first focus lands. */
cases.writeOffFocus = async () => {
  const { b, d } = await session('owner', 'ar', 1440, `${SPACE}/desk`);
  try {
    await d.until(`!!document.querySelector('main [aria-label^="إجراءات أخرى لزيارة"]')`, 'an uncollected row', 20000);
    await d.openMenu(`document.querySelector('main [aria-label^="إجراءات أخرى لزيارة"]')`, 'the row «⋯»');
    await d.click(byText('[role=menuitem]', '^لن يُحصَّل…$'), 'write off…');
    await d.until(`!!document.querySelector('[role=alertdialog]')`, 'the write-off dialog');
    await d.sleep(500);
    log('write-off dialog focus on opening:', await focused(d));
    await d.shot(`1-writeoff-focus-owner-${tag('ar', 1440)}`);
    await d.click(byText('[role=alertdialog] button', '^رجوع$'), 'back');
    await d.sleep(500);
    log('writes:', writes(d).length);
  } finally {
    b.chrome.kill();
  }
};

const which = process.argv[2];
if (!cases[which]) throw new Error(`no case ${which}`);
await cases[which](process.argv[3]);
