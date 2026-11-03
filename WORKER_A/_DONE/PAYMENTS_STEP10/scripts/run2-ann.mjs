// PR 2's helpers and cases for run2.mjs (imported by it).
export function annCases({ CASES, session, finish, log, byText, writes, logWrites, toastText, dialogText, mainText, focused, tag, SPACE }) {
  const ANN = `${SPACE}/announcements`;
  const inDialog = (selector, pattern) => byText(`[role=dialog] ${selector}`, pattern);
  const radioByLabel = (pattern) =>
    `[...document.querySelectorAll('[role=dialog] button[role=radio]')].find((x) => new RegExp(${JSON.stringify(pattern)}).test(x.labels?.[0]?.innerText ?? x.innerText))`;
  const radioByText = (text, index = 0) =>
    `[...document.querySelectorAll('[role=dialog] button[role=radio]')].filter((x) => x.innerText.trim() === ${JSON.stringify(text)})[${index}]`;
  async function typeInto(d, expression, text) {
    await d.evaluate(`(() => { const el = ${expression}; el.focus(); el.select?.(); return true; })()`);
    await d.b.send('Input.insertText', { text });
    await d.sleep(150);
  }
  const textareaByLabel = (label) =>
    `[...document.querySelectorAll('[role=dialog] textarea')].find((x) => x.labels?.[0]?.innerText.includes(${JSON.stringify(label)}))`;
  async function setTime(d, index, value) {
    await d.evaluate(
      `(() => { const el = [...document.querySelectorAll('[role=dialog] input[type=time]')][${index}]; const set = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set; set.call(el, ${JSON.stringify(value)}); el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); return true; })()`,
    );
    await d.sleep(200);
  }
  async function pickDate(d, index, dayPattern) {
    await d.click(
      `[...document.querySelectorAll('[role=dialog] button')].filter((x) => (x.labels?.[0]?.innerText ?? '').startsWith('Date') || (x.labels?.[0]?.innerText ?? '').startsWith('التاريخ'))[${index}]`,
      'date trigger',
    );
    await d.sleep(700);
    await d.click(
      `[...document.querySelectorAll('[data-slot=calendar] button')].find((x) => new RegExp(${JSON.stringify(dayPattern)}).test(x.getAttribute('aria-label') ?? ''))`,
      `day ${dayPattern}`,
    );
    await d.sleep(500);
  }
  async function offline(d, on) {
    await d.b.send('Network.emulateNetworkConditions', { offline: on, latency: 0, downloadThroughput: -1, uploadThroughput: -1 });
  }
  const cardOf = (text) =>
    `[...document.querySelectorAll('main li, main article')].filter((x) => x.innerText.includes(${JSON.stringify(text)})).at(-1)`;
  const cardButton = (text, label) =>
    `[...((${cardOf(text)})?.querySelectorAll('button') ?? [])].find((x) => x.innerText.trim() === ${JSON.stringify(label)})`;
  const cardMore = (text) =>
    `[...((${cardOf(text)})?.querySelectorAll('button') ?? [])].find((x) => /^(More actions|إجراءات أخرى)/.test(x.getAttribute('aria-label') ?? ''))`;
  async function tab(d, name) {
    // Radix's tabs change on a mouse press, not a click.
    const ok = await d.evaluate(`(() => { const el = ${byText('main [role=tab]', `^${name}`)}; if (!el) return false; el.dispatchEvent(new MouseEvent('mousedown', { bubbles: true, button: 0 })); return true; })()`);
    if (!ok) throw new Error(`no tab ${name}`);
    await d.sleep(1800);
  }
  async function del(d, text) {
    await d.openMenu(cardMore(text), 'more');
    await d.click(byText('[role=menuitem]', '^(Delete|حذف)'), 'delete…');
    await d.sleep(800);
    log('delete dialog', await dialogText(d));
    return async () => {
      await d.click(byText('[role=alertdialog] button', '^(Delete|حذف)$'), 'confirm delete');
      await d.sleep(1800);
      log('toast', await toastText(d), 'focus', await focused(d));
    };
  }

  // Reception (writes: «إعلان تجربة» GENERAL now, no end — posted with an offline first send and one retry; its
  // English text added; «إنهاء الآن», «تراجع», «إنهاء الآن»; deleted from «منتهية». «عرض تجربة» OFFER from tomorrow
  // 09:00, «ابدأ الآن», deleted).
  CASES.annReception = async () => {
    const { b, d } = await session('reception', 'en', 1440, ANN);
    await d.click(byText('main button', '^New announcement$'), 'new');
    await d.sleep(800);
    log('focus on opening', await focused(d));
    await d.click(radioByLabel('^General'), 'general');
    await typeInto(d, textareaByLabel('Text in Arabic'), 'إعلان تجربة');
    await d.click(radioByText('No end'), 'no end');
    await d.sleep(300);
    await d.shot('2-sheet-new-reception-en-dark-1440');
    let from = writes(d).length;
    await offline(d, true);
    await d.click(inDialog('button', '^Publish$'), 'publish (offline)');
    await d.until(`document.querySelector('[role=dialog]')?.innerText.includes('Try again')`, 'the lost line', 40000);
    log('offline: dialog', await dialogText(d));
    await d.shot('2-sheet-lost-reception-en-dark-1440');
    await offline(d, false);
    await d.click(inDialog('button', '^Try again$'), 'retry');
    await d.sleep(3000);
    log('toast', await toastText(d));
    logWrites(d, from);
    log('post keys', [...new Set(writes(d).slice(from).map((r) => r.key))].join(', '));
    log('list', await mainText(d, 500));
    // Its English text added.
    from = writes(d).length;
    await d.click(cardButton('إعلان تجربة', 'Edit'), 'edit');
    await d.sleep(900);
    await typeInto(d, textareaByLabel('Text in English'), 'A test announcement');
    await d.click(inDialog('button', '^Save$'), 'save');
    await d.sleep(2000);
    log('toast', await toastText(d));
    // End now, undo, end now again.
    await d.click(cardButton('A test announcement', 'End now'), 'end now');
    await d.sleep(1500);
    log('toast', await toastText(d));
    await d.shot('2-end-now-toast-reception-en-dark-1440');
    await d.click(byText('[data-sonner-toast] button', '^Undo$'), 'undo');
    await d.sleep(2200);
    log('after undo', await mainText(d, 400), '| toast', await toastText(d));
    await d.click(cardButton('A test announcement', 'End now'), 'end now again');
    await d.sleep(1800);
    log('toast', await toastText(d), 'focus', await focused(d));
    // Deleted from «Ended».
    await tab(d, 'Ended');
    log('ended', await mainText(d, 400));
    const confirm1 = await del(d, 'A test announcement');
    await d.shot('2-delete-dialog-reception-en-dark-1440');
    await confirm1();
    logWrites(d, from);
    // The offer from tomorrow 09:00, started now, deleted.
    from = writes(d).length;
    await tab(d, 'Active');
    await d.click(byText('main button', '^New announcement$'), 'new');
    await d.sleep(800);
    await d.click(radioByLabel('^Offer'), 'offer');
    await typeInto(d, textareaByLabel('Text in Arabic'), 'عرض تجربة');
    await d.click(radioByText('At a time', 0), 'start at a time');
    await d.sleep(400);
    await pickDate(d, 0, 'October 29th, 2026');
    await setTime(d, 0, '09:00');
    await d.click(radioByText('No end'), 'no end');
    await d.sleep(300);
    log('sheet', await dialogText(d));
    await d.shot('2-sheet-offer-reception-en-dark-1440');
    await d.click(inDialog('button', '^Publish$'), 'publish');
    await d.sleep(2200);
    log('toast', await toastText(d));
    await tab(d, 'Scheduled');
    log('scheduled', await mainText(d, 500));
    await d.shot('2-scheduled-reception-en-dark-1440');
    await d.click(cardButton('عرض تجربة', 'Start now'), 'start now');
    await d.sleep(1800);
    log('toast', await toastText(d));
    await tab(d, 'Active');
    const confirm2 = await del(d, 'عرض تجربة');
    await confirm2();
    logWrites(d, from);
    await finish(b);
  };

  // The rest of the reception's case, from «منتهية» (the first run stopped there).
  CASES.annReception2 = async () => {
    const { b, d } = await session('reception', 'en', 1440, ANN);
    let from = writes(d).length;
    await tab(d, 'Ended');
    log('ended', await mainText(d, 400));
    const confirm1 = await del(d, 'A test announcement');
    await d.shot('2-delete-dialog-reception-en-dark-1440');
    await confirm1();
    logWrites(d, from);
    from = writes(d).length;
    await tab(d, 'Active');
    await d.click(byText('main button', '^New announcement$'), 'new');
    await d.sleep(800);
    await d.click(radioByLabel('^Offer'), 'offer');
    await typeInto(d, textareaByLabel('Text in Arabic'), 'عرض تجربة');
    await d.click(radioByText('At a time', 0), 'start at a time');
    await d.sleep(400);
    await pickDate(d, 0, 'October 29th, 2026');
    await setTime(d, 0, '09:00');
    await d.click(radioByText('No end'), 'no end');
    await d.sleep(300);
    log('sheet', await dialogText(d));
    await d.shot('2-sheet-offer-reception-en-dark-1440');
    await d.click(inDialog('button', '^Publish$'), 'publish');
    await d.sleep(2200);
    log('toast', await toastText(d));
    await tab(d, 'Scheduled');
    log('scheduled', await mainText(d, 500));
    await d.shot('2-scheduled-reception-en-dark-1440');
    await d.click(cardButton('عرض تجربة', 'Start now'), 'start now');
    await d.sleep(1800);
    log('toast', await toastText(d));
    await tab(d, 'Active');
    const confirm2 = await del(d, 'عرض تجربة');
    await confirm2();
    logWrites(d, from);
    await finish(b);
  };

  // The owner (writes: «إغلاق تجربة» CLOSURE from yesterday 08:00, no end; then «إنهاء الآن»; the extension applied
  // with 1 day — the approval note's write). Between, the guest's space page with the notice at its top (PR 4b).
  CASES.annClosure = async () => {
    const { b, d } = await session('owner', 'en', 1440, ANN);
    let from = writes(d).length;
    await d.click(byText('main button', '^New announcement$'), 'new');
    await d.sleep(800);
    await d.click(radioByLabel('closure'), 'closure');
    await typeInto(d, textareaByLabel('Text in Arabic'), 'إغلاق تجربة');
    await d.click(radioByText('At a time', 0), 'start at a time');
    await d.sleep(400);
    await pickDate(d, 0, 'October 27th, 2026');
    await setTime(d, 0, '08:00');
    await d.click(radioByText('No end'), 'no end');
    await d.sleep(300);
    log('sheet', await dialogText(d));
    await d.shot('2-sheet-closure-owner-en-dark-1440');
    await d.click(inDialog('button', '^Publish$'), 'publish');
    await d.sleep(2200);
    log('toast', await toastText(d));
    logWrites(d, from);
    log('list', await mainText(d, 600));
    await d.shot('2-closure-running-owner-en-dark-1440');
    await finish(b);
  };

  CASES.annClosureEndExtend = async () => {
    const { b, d } = await session('owner', 'en', 1440, ANN);
    const from = writes(d).length;
    await d.click(cardButton('إغلاق تجربة', 'End now'), 'end now');
    await d.sleep(1800);
    log('toast', await toastText(d));
    await tab(d, 'Ended');
    log('ended', await mainText(d, 600));
    await d.click(cardButton('إغلاق تجربة', 'Extend subscriptions'), 'extend');
    await d.sleep(2500);
    log('extension dialog', await dialogText(d));
    log('focus on opening', await focused(d));
    log('preview read', d.requests.filter((r) => r.url.includes('extend-subscriptions')).map((r) => `${r.method} ${r.url} ${r.status}`).join(' | '));
    await d.shot('2-extension-dialog-owner-en-dark-1440');
    const days = `[...document.querySelectorAll('[role=alertdialog] input, [role=dialog] input')].find((x) => x.type === 'number' || x.inputMode === 'numeric')`;
    await d.evaluate(`(() => { const el = ${days}; el.focus(); el.select(); return true; })()`);
    await d.b.send('Input.insertText', { text: '1' });
    await d.sleep(400);
    log('dialog with 1 day', await dialogText(d));
    await d.click(byText('[role=alertdialog] button, [role=dialog] button', '^Extend'), 'apply');
    await d.sleep(2500);
    log('toast', await toastText(d));
    log('card', await mainText(d, 700));
    logWrites(d, from);
    await d.shot('2-extended-owner-en-dark-1440');
    await finish(b);
  };

  CASES.annShots = async () => {
    for (const role of ['reception', 'owner']) {
      for (const language of ['ar', 'en']) {
        const { b, d } = await session(role, language, 1440, `${ANN}?state=ended`);
        for (const width of [390, 768, 1440]) {
          await d.viewport(width, 900);
          await d.go(`${ANN}?state=ended`);
          await d.sleep(2500);
          await d.shot(`2-ended-${role}-${tag(language, width)}`, 1600);
        }
        await finish(b);
      }
    }
  };

  CASES.annSheetWidth = async () => {
    for (const language of ['ar', 'en']) {
      const { b, d } = await session('reception', language, 768, ANN);
      for (const width of [390, 768, 1440]) {
        await d.viewport(width, 900);
        await d.go(ANN);
        await d.sleep(2000);
        await d.click(byText('main button', '^(New announcement|إعلان جديد)$'), 'new');
        await d.sleep(900);
        await d.click(radioByText(language === 'en' ? 'At a time' : 'في موعد', 0), 'start at a time');
        await d.sleep(500);
        const grid = await d.evaluate(`(() => { const t = document.querySelector('[role=dialog] input[type=time]'); const g = t?.closest('.grid'); return g ? getComputedStyle(g).gridTemplateColumns : 'none'; })()`);
        log(`${language} ${width} the date and time grid`, grid);
        await d.shot(`2-sheet-period-reception-${tag(language, width)}`, 1600);
        await d.key('Escape', 'Escape', 27);
        await d.sleep(500);
      }
      await finish(b);
    }
  };
}
