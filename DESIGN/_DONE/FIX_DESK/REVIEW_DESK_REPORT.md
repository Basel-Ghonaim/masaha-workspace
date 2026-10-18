# Design review 6 — the front desk

Reviewer: `design-review-desk` · 2026-10-11 · archive from `origin/main` `b66ddfe`, served on
`http://127.0.0.1:5345/` · evidence: `C:\Users\basel\Downloads\design-review-desk\DK-0xx.png`.
Scope: screens 13–17 (Desk, Customers, Customer file, the subscription sheet, Payments and «دفعاتي
اليوم»), board sections 20–28, 31–32, the desk frames of 41 and 50–52. Settled decisions
(`DECISIONS_SHARED/ADMIN/PUBLIC.md`) are not reported again. Their application is listed in one place
(§2.5).

## 1. Summary

1. **The desk has two searches, and the main one cannot find a visitor who is present.** One search
   should find everyone, present people first. It should always offer «تسجيل زيارة باسم «…»» and
   carry the typed name into the dialog (DK-001, DK-002).
2. **The money is entered three different ways.** Check-out, the subscription sheet and «استلام دفعة»
   should share one money block: what is due, what was received (filled in with the amount due), the
   method, and a live line saying what becomes a debt or what change to give back. The button says
   the amount (DK-004).
3. **Two money mistakes are hidden today:**
   - the customer file shows a visit debt in the balance but in no tab (DK-011);
   - «دفعاتي اليوم» shows a voided payment as an ordinary row (DK-015).
4. **Renewing a customer who owes money loses the renewal.** «استلام دفعة» inside the sheet replaces
   the sheet. Renewing and paying both takes 6 taps today, and 2 with the proposal (DK-005).
5. **On a phone, the uncollected visits sit 4,100 px down**, below every present card. The desk
   should be ordered for the phone: search, then uncollected, then present now (DK-003). Fixed-price
   subscribers should check out in one tap (DK-010).

## 2. Patterns (level: pattern)

The desk is used all day, standing, often on a phone, with customers waiting. These patterns aim at
**speed**: one search, one tap to the common action, and the name typed once. They also aim at
**money safety**: every amount is seen before it is recorded, every recorded amount is seen
afterwards, and every mistake has a visible path to a void.

### 2.1 One desk search (DK-001)
The desk's search finds **anyone**: the people present (open visits by name, and subscribers) with
«خروج», then customers on file with «حضور». The last rows are always «تسجيل زيارة باسم «X»» and
«زبون جديد باسم «X»», each opening its dialog with the name filled in. The present list keeps no
second search.

**Pages:** Desk; the customer card; «استلام دفعة»'s picker, which uses the same search.

### 2.2 One money block (DK-004)
One block wherever money is taken: check-out of a visit, check-out of a usage-based subscriber,
«استلام دفعة», and new or renewed subscriptions. Built from `Field` + `Input dir="ltr"` +
`ToggleGroup` (the method) in a `muted` panel:
- **«المستحق»:** the calculation is shown once;
- **«المستلم الآن»:** filled in with what is due (today the sheet starts at 0, behind a switch);
- **«الطريقة»;**
- **a live line, `aria-live`:** «المتبقي 7 ₪ يصبح دينًا على هبة — رقم الجوال مطلوب» (the phone
  `Field` appears inline), or «الباقي للزبون 8 ₪» when more is received than is due;
- **the submit names the money:** «خروج واستلام 12 ₪», «حفظ واستلام 300 ₪», «تسجيل 150 ₪»;
- **«لم يدفع شيئًا»:** an `outline` button that sets the amount to 0 and shows the phone. It replaces
  check-out's separate «خروج بدون دفع» mode.

### 2.3 A recorded payment stays visible and correctable (DK-015, DK-016, DK-018)
- **Before the server answers:** the failure state says a retry is safe. If a combined action
  (subscription + payment) fails halfway, the message says which part was saved.
- **After it is recorded:**
  - the toast names the amount, the item and the method;
  - «دفعاتي اليوم» shows a voided payment struck through, with who voided it and why;
  - reception is told how a mistake is corrected (the owner voids it).
- **Voiding:** the owner voids from the row's «⋯» on every list, visit payments included.

### 2.4 Customer actions by state (DK-013)
One set of actions, in one order, on the desk's customer card, the customer file's header and the
Customers row menu:
- the primary action is «حضور» or «خروج»;
- «استلام 42 ₪» appears only when the customer owes, with the amount on the button;
- «تجديد» appears only when the subscription is ending soon or has expired;
- «اشتراك جديد», «تعديل البيانات», «ملف الزبون» and, for the owner, «أرشفة» go in «⋯».

### 2.5 How this batch applies the settled decisions (not issues)
- **P1:** the desk's phone bottom bar holds **«تسجيل زيارة» only**. «استلام دفعة» and «زبون جديد»
  move to the top bar's «⋯» on a phone, and to `PageHeader` actions from `md` (with §2.1 they are
  also reached from the search). Customers keeps «زبون جديد» in a row above the list. Payments keeps
  «تصدير CSV» as its header action.
- **P8's exception does not fit the desk.** On a phone the row a check-in or check-out changes is
  usually off screen (DK-003). The desk keeps a success toast for check-in and check-out, and every
  money action keeps one with its amount.
- **P9 at the desk:**
  - checking out a fixed-price subscriber is reversible (check in again) and affects no one: act at
    once (DK-010);
  - a money check-out is its own confirmation, the amount on the button;
  - «إنهاء الاشتراك» stays an `AlertDialog`: it is felt by the customer, and the desk has no way to
    undo it;
  - a void stays an `AlertDialog`, with its reason `Textarea`: irreversible, and felt in staff
    totals;
  - archiving is DK-014.
- **A7:** Payments' «إظهار الملغاة» `Switch` becomes a `ToggleGroup` chip beside the count.
- **P9's words:** WarnDialog's «إلغاء» becomes «رجوع». «إلغاء الدفعة» stays as the verb.

## 3. Issues

### DK-001 — One search finds everyone at the desk
- **Type:** improvement · **Level:** pattern · **Impact:** high
- **Where:**
  - frame: 21 «Desk · search results — phone 390»;
  - URL: `http://127.0.0.1:5345/Desk.html?role=reception&q=لمى`;
  - screenshot: `docs/design/screens/21-front-desk-reception-vs-owner/06-desk-search-results-phone-390.webp`.
- **Evidence:** `DK-001.png`. Searching «لمى» finds «سلمى الريس» but not «لمى الكرد», who is present
  on a visit. Nothing stops a second visit for her.
- **What is wrong:**
  - The main search covers customers on file only. Visitors, who are most of the people checking
    out, are found only by a second «ابحث بين الحاضرين» field under the tabs.
  - With the keyboard, the three page buttons sit between the search and its results (Tab × 4 to
    reach the first result).
- **Proposal:** §2.1. The results are an `aria-live` list:
  1. «حاضر الآن» rows: name, `Badge` (visit or the subscription), «منذ 12:20», `Button`
     «خروج»;
  2. «زبائن» rows: the customer card, as in DK-013;
  3. the two «… باسم «X»» rows.

  Results come straight after the search in the DOM. The present list loses its own search.
- **Why it is better:** one place to look, for both check-in and check-out. A present visitor can no
  longer be checked in twice by mistake. Check-out loses the scroll to the second search.
- **Cost:** M
- **Rule:** foundation §13 row 13 (check in by name or a customer); data model › Operations › Visit.

### DK-002 — The typed name is lost, and the visit should lead the no-result state
- **Type:** defect · **Level:** page · **Impact:** high
- **Where:**
  - frame: 21 «Desk · no result → «زبون جديد باسم …» — phone 390»;
  - URL: `…/Desk.html?role=reception&q=سليم`;
  - screenshot: `screens/21-front-desk-reception-vs-owner/08-desk-no-result-phone-390.webp`.
- **Evidence:** `DK-002.png`. «تسجيل زيارة» from the empty state opens the dialog with an empty name;
  the probe read `""`.
- **What is wrong:**
  - The name typed in the search must be typed again.
  - The primary button is «زبون جديد باسم», although a one-off visit is the common case («Daily
    visitors are visits, not customers», glossary).
- **Proposal:**
  - The no-result state's primary is «تسجيل زيارة باسم «سليم»». «زبون جديد باسم «سليم»» is
    `outline`.
  - Both pass the name (the prototype already reads `vname`).
- **Why it is better:** the common case is one tap, and the name is typed once.
- **Cost:** S
- **Rule:** glossary › Visit.

### DK-003 — The desk on a phone: uncollected visits are 4,100 px down
- **Type:** improvement · **Level:** page · **Impact:** high
- **Where:**
  - frame: 21 «Desk · reception (سامي) — phone 390»;
  - URL: `…/Desk.html?role=reception` at 390;
  - screenshot: `screens/21-front-desk-reception-vs-owner/02-desk-reception-phone-390.webp`.
- **Evidence:** `DK-003.png`. The «غير محصّل» card starts at y = 4,139 px on a 4,410 px page, after 27
  present cards of about 135 px each.
- **What is wrong:**
  - Below `xl` the money the desk should chase is at the very bottom.
  - The phone also stacks a full-width «زبون جديد», the «الآن | السجل» tabs, a second search and a
    two-button bottom bar before the first person.
  - «الحاضرون الآن 27 / 40» is shown twice (heading and table summary).
- **Proposal:** on every width below `xl`, in this order:
  1. the search (DK-001);
  2. «غير محصّل» as a compact `Card` when it is not empty: «2 زيارة غير محصّلة · 21 ₪», with its
     rows inside a disclosure (first 3 shown, «عرض الكل»), and nothing at all when it is empty;
  3. «الحاضرون الآن 27 / 40» (once) with `Tabs` «الآن | السجل» in its header;
  4. the present list.

  The page actions follow P1 (§2.5). At `xl` the side column stays.
- **Why it is better:**
  - On a phone, the money to collect and the first present person are both on the first screen.
  - Each section has one job.
- **Cost:** S
- **Rule:** foundation §9 (phone single column); P1 as amended.

### DK-004 — One money block for every place money is taken
- **Type:** improvement · **Level:** pattern · **Impact:** high
- **Where:**
  - frame: 23 «Visit · 4 h × 3 ₪ = 12 ₪ — phone 390»;
  - URL: `…/Desk.html?role=reception&dialog=checkout&pid=pv0`;
  - screenshot: `screens/23-check-out/02-visit-4-h-3-12-phone-390.webp`;
  - also 24 «Step 2 · package + partial payment» and 25 «Open items».
- **Evidence:** `DK-004.png`. With 5 ₪ received, a debt block appears under the method, and the
  submit still reads «خروج ودفع».
- **What is wrong:**
  - Check-out pre-fills what was received, while the sheet hides the payment behind «دفعة الآن»,
    which starts off.
  - Check-out has a second mode for not paying.
  - When 20 ₪ is received for 12 ₪, the prototype silently records 12 ₪ (toast «دُفع 12 ₪»), and
    the change to give back is shown nowhere.
  - No submit says how much is being recorded.
- **Proposal:** §2.2, on the checkout dialog, `PayDialog` and `SubscriptionSheet`. The «دفعة الآن»
  switch and the `debtMode` state go.
- **Why it is better:** the same three fields everywhere. The amount is seen before it is recorded,
  and the change is told. A partial payment and a debt are visible facts, not modes.
- **Cost:** M
- **Rule:** ADR 0010 rules 2 and 4; data model › Unpaid visit (a phone is required).

### DK-005 — Renewal with a debt: «استلام دفعة» throws the renewal away
- **Type:** defect · **Level:** page · **Impact:** high
- **Where:**
  - frame: 24 «Renewal with an unpaid September — phone 390»;
  - URL: `…/Customers.html?role=reception&renew=m6`;
  - screenshot: `screens/24-new-customer-subscription-sheet/08-renewal-with-an-unpaid-september-phone-390.webp`.
- **Evidence:** `DK-005.png`. After the Alert's «استلام دفعة», the only dialog open is «استلام دفعة ·
  رهف قديح»: the sheet and its choices are gone (one dialog slot, `desk.open`).
- **What is wrong:** paying the old debt and renewing takes six taps across two dialogs, and the
  renewal is entered twice.
- **Proposal:**
  - The renewal's money block (§2.2) is filled in with **old balance + new price** (150 + 250).
  - It is applied **oldest first**: one payment for September, one for the new subscription (ADR
    0010 rule 2).
  - The Alert keeps its warning, without a button: «عليها 150 ₪ من اشتراك سبتمبر · يُطبَّق المستلم
    عليه أولًا».
  - The submit reads «تجديد واستلام 400 ₪».
- **Why it is better:** renewing and paying both takes 2 taps instead of 6, nothing is lost, and the
  ledger keeps one payment per item.
- **Cost:** M
- **Rule:** ADR 0010 rules 2 and 7 (warn, never block).

### DK-006 — The sheet asks for the phone at the end, then sends you back to step 1
- **Type:** defect · **Level:** page · **Impact:** medium
- **Where:**
  - frame: 24 «Step 1 · customer — phone 390»;
  - URL: `…/Desk.html?role=reception&dialog=sheet&mode=new&name=سليم`;
  - screenshot: `screens/24-new-customer-subscription-sheet/02-step-1-customer-phone-390.webp`.
- **Evidence:** `DK-006.png`. Saving a usage-based subscription without a phone returns to «الخطوة 1
  من 2». The field shows its error while still labelled «اختياري».
- **What is wrong:**
  - Whether the phone is needed is decided by step 2 (anything unpaid), but it is asked in step 1.
  - Two steps for two fields.
- **Proposal:**
  - **One step.** For a new customer the sheet opens with «الاسم» and «رقم الجوال», then the package,
    the dates and the money block.
  - The phone's requirement is said by the money block's live line («المتبقي 250 ₪ يصبح دينًا — رقم
    الجوال مطلوب»), and the error moves focus to the field.
  - «اختياري» is dropped whenever something stays unpaid.
- **Why it is better:** no bounce back; one submit; the rule is told where it arises.
- **Cost:** S
- **Rule:** foundation §10 (validation on submit, focus to the first invalid field).

### DK-007 — Renewal on a phone: the package list pushes the money out of sight
- **Type:** improvement · **Level:** page · **Impact:** medium
- **Where:** frame 24 «Renewal with an unpaid September — phone 390», as DK-005.
- **Evidence:** `DK-007.png`. Seven package cards (about 750 px) come before «من»; the payment is
  below the fold.
- **What is wrong:** a renewal is nearly always the same package, but the sheet shows every package
  as a tall card.
- **Proposal:**
  - **In renewal mode,** the current package is a one-line summary («شهري طلاب · 250 ₪ · 1–30
    أكتوبر») with a `link` «تغيير الباقة» that opens the list.
  - **In new mode,** each package is one line (name and price, with the terms as a `caption`),
    grouped as now, and «مخصّص» last.
- **Why it is better:** the dates and the money are on the first screen of a renewal.
- **Cost:** S
- **Rule:** lens B5 (progressive disclosure).

### DK-008 — A custom subscription invents a 30-day end
- **Type:** defect · **Level:** page · **Impact:** medium
- **Where:**
  - frame: 24 «Step 2 · «مخصّص»» (both widths);
  - URL: `…/Desk.html?role=reception&dialog=sheet&mode=subscribe&cid=m3&pkg=custom`;
  - screenshot: `screens/24-new-customer-subscription-sheet/06-step-2-phone-390.webp`.
- **Evidence:** `DK-008.png`. «إلى» is optional and left empty, yet the summary reads «29 سبتمبر 2026 –
  28 أكتوبر 2026» (`desk-sheet.jsx`: `cu.to || addDays(start, 29)`).
- **What is wrong:** the data model allows no end date (scenario 4, an hours pack «with no end
  date»), so the summary states a limit that will not be stored.
- **Proposal:** the summary says what will happen:
  - «بلا تاريخ نهاية · ينتهي عند استهلاك 20 ساعة»;
  - or, with no end and no total, «بلا حدّ · يبقى نشطًا حتى يُنهى» (`caption`, with the `warning`
    icon, so it is never colour alone).
- **Why it is better:** the desk sees the real terms before saving.
- **Cost:** S
- **Rule:** data model › Subscription scenarios 4; Subscription status.

### DK-009 — «اليوم ليس من أيامه» needs data the model does not have
- **Type:** defect · **Level:** page · **Impact:** medium
- **Where:**
  - frame: 22 «Not one of his days — phone 390»;
  - URL: `…/Desk.html?role=reception&dialog=warn&cid=m12`;
  - screenshot: `screens/22-check-in-warnings/06-not-one-of-his-days-phone-390.webp`.
- **Evidence:** `DK-009.png`. The warning comes from `terms.weekDays` (`desk-data.js`, customer m12).
- **What is wrong:**
  - The data model stores **days per week** (a count), not which days.
  - The sheet only asks «أيام بالأسبوع».
  - The API cannot serve this warning.
- **Proposal (recommended):** replace it with the warning the model can serve: «استنفد أيامه هذا
  الأسبوع · 3 من 3». Drop «أيامه: السبت، الاثنين، الأربعاء» from the progress lines.
  **Alternative (the owner's choice):** add weekdays to the subscription's limits (data model and
  sheet).
- **Why it is better:** the screen promises only what the system knows.
- **Cost:** S
- **Rule:** data model › Operations › Subscription; Subscription progress.

### DK-010 — Checking out a fixed-price subscriber: a dialog with nothing to decide
- **Type:** improvement · **Level:** page · **Impact:** medium
- **Where:**
  - frame: 23 «Subscriber · monthly — phone 390»;
  - URL: `…/Desk.html?role=reception&dialog=checkout&pid=ps0`;
  - screenshot: `screens/23-check-out/08-subscriber-monthly-phone-390.webp`.
- **Evidence:** `DK-010.png`. The dialog shows the times and «صالح حتى 20 أكتوبر», with one button.
- **What is wrong:** 19 of the 27 present are subscribers, and each check-out costs an extra tap for
  information only.
- **Proposal:**
  - **A fixed-price subscriber** checks out from the row in one tap, and the toast says «سُجّل خروج
    محمد العطار · 4 س 35 د». P9: reversible by checking in again, and it affects no one else. No
    undo is needed, so no reopening endpoint is needed.
  - **A usage-based subscriber** keeps the dialog, with the money block (§2.2) for an optional
    payment («المستحق حتى الآن 63 ₪»).
- **Why it is better:** 3 taps become 2 on the most frequent check-out.
- **Cost:** S
- **Rule:** P9.

### DK-011 — The customer file hides unpaid visits
- **Type:** defect · **Level:** page · **Impact:** high
- **Where:**
  - frame: 27 «Memberships · partly paid» (the file's structure);
  - URL: `…/Customer file.html?id=m10`.
- **Evidence:** `DK-011.png`. Dana owes 9 ₪ (the header's balance), but «الاشتراكات» says «هذا الزبون
  يأتي بزيارات فقط» and «الدفعات» says «لا توجد دفعات بعد».
- **What is wrong:**
  - A visit left unpaid is the commonest way a person becomes a customer (data model), yet the file
    shows the debt but not the item.
  - Visit payments are matched to the file by name.
- **Proposal:**
  - The first tab becomes **«المستحقات والاشتراكات»**. Before the subscriptions, a «زيارات غير
    مدفوعة» `Card` lists each unpaid visit: the date, «09:00–11:10», the charge, and «تحصيل» (the pay
    dialog on that item).
  - The empty state says nothing about «visits only» while a visit is owed.
  - «الدفعات» lists the payments of the customer's visits through the visit's customer, not the
    name.
- **Why it is better:** every amount in the balance can be seen and collected from the file.
- **Cost:** S
- **Rule:** data model › Customer debt, Unpaid visit; ADR 0010 rule 4.

### DK-012 — An uncollected visit without a customer cannot be collected as drawn
- **Type:** defect · **Level:** page · **Impact:** medium
- **Where:**
  - frame: 21 «Desk · reception (سامي) — desktop 1440», the «غير محصّل» card;
  - URL: `…/Desk.html`.
- **Evidence:** `DK-012.png`. The auto-checked-out row («مالك صيام · خروج تلقائي عند الإغلاق · أمس»)
  has a customer, and «تحصيل» opens the customer's pay dialog.
- **What is wrong:** a visit closed by the auto check-out «may have none» (data model › Checked by the
  service). A by-name visit has no customer, so the drawn flow has nothing to open.
- **Proposal:** an uncollected row shows the visit's name and two actions:
  - «تحصيل»: the pay dialog on the **visit item**, with no customer step;
  - «تسجيل دينًا»: `outline`; name and phone, which attach the customer (the same rule as an unpaid
    check-out).
- **Why it is better:** the list works for the case the model says is normal.
- **Cost:** S
- **Rule:** data model › Uncollected visits; Unpaid visit. See also §4, rule 2.

### DK-013 — Customer actions by state
- **Type:** improvement · **Level:** pattern · **Impact:** medium
- **Where:**
  - frame: 20 «1 · Search «رهف» → card»;
  - URL: `…/Desk.html?role=reception&q=نور`;
  - screenshot: `screens/20-flow-front-desk/01-1-search-card.webp`;
  - also 27 (file header) and 26 (row menu).
- **Evidence:** `DK-013.png`. Five `sm` buttons on three rows («خروج · دفع · تجديد · اشتراك جديد ·
  ملف الزبون»), the same set on the file's header, a different order in the Customers menu.
- **What is wrong:**
  - Every action has the same weight whatever the customer's state.
  - «تجديد» and «اشتراك جديد» are both shown on an active subscription.
- **Proposal:** §2.4. The card's name links to the file, so «ملف الزبون» leaves the card. The money
  button carries the amount («استلام 42 ₪»).
- **Why it is better:** a card shows at most two or three buttons on one row, and the right one is
  first.
- **Cost:** S
- **Rule:** lens B2 (one primary action).

### DK-014 — No way to edit a customer, and archive promises a restore that has no place
- **Type:** defect · **Level:** page · **Impact:** medium
- **Where:**
  - frame: 26 «Archive with debt (owner) — phone 390»;
  - URL: `…/Customers.html?archive=m6`;
  - screenshot: `screens/26-customers-reception-vs-owner/08-archive-with-debt-owner-phone-390.webp`.
- **Evidence:** `DK-014.png`. «يمكنك استرجاعه لاحقًا», but no filter or page lists archived
  customers.
- **What is wrong:**
  - A misspelt name or a wrong phone (which a debt and its WhatsApp reminder depend on) cannot be
    corrected anywhere, although `PATCH /customers/:id` is planned.
  - The archive dialog also adds an undo toast after the dialog.
- **Proposal:**
  - **Editing:** «تعديل البيانات» in the customer's «⋯» opens a `Dialog` with «الاسم» and «رقم
    الجوال» (`PHONE_TAKEN` shown on the field).
  - **Archived customers:** a «مؤرشف» choice in the Customers status filter, with «استرجاع» on the
    row (as A3 does for deleted spaces).
  - **P9:** a settled customer is archived at once, with «تراجع». A customer who owes gets the
    `AlertDialog` naming the debt, with no toast undo.
- **Why it is better:** the data can be fixed at the desk, and the promise in the dialog is true.
- **Cost:** S
- **Rule:** data model › Customer (archived, never deleted); P9; §4, rule 3.

### DK-015 — «دفعاتي اليوم» shows a voided payment as an ordinary row
- **Type:** defect · **Level:** page · **Impact:** high
- **Where:**
  - frame: 28 «My payments today — desktop 1440»;
  - URL: `…/My payments.html?role=reception`;
  - screenshot: `screens/28-reception-only/01-my-payments-today-desktop-1440.webp`.
- **Evidence:** `DK-015.png`. Sami's 6 ₪ payment was marked voided in the data; its row is unchanged
  (`My payments.html` reads no void into its rows or columns).
- **What is wrong:**
  - At handover the cash must match the total. A payment the owner voided must be seen as voided, or
    reception counts money that does not count.
  - Reception also has no word on how a mistake it made gets corrected.
- **Proposal:**
  - A voided row is struck through, with «ألغاها أحمد: سُجّلت بالخطأ», and excluded from the cards.
  - A `caption` under the cards: «خطأ في دفعة؟ يلغيها صاحب المساحة، وتظهر هنا مشطوبة».
  - On a phone, the three `StatCard`s become one `Card` with three rows, «نقدًا للتسليم» first.
- **Why it is better:**
  - The handover adds up.
  - Reception knows the one path to correct a mistake without owner rights (ADR 0009).
- **Cost:** S
- **Rule:** ADR 0010 rule 3 (a voided payment counts nowhere); ADR 0009 (collections today: own).

### DK-016 — Void sits on every row as a plain button
- **Type:** improvement · **Level:** pattern (Payments, Customer file) · **Impact:** medium
- **Where:**
  - frame: 32 «Ledger · this month»;
  - URL: `…/Payments.html` at 768;
  - screenshot: `screens/32-payments-owner/01-ledger-this-month-desktop-1440.webp`.
- **Evidence:** `DK-016.png`. «إلغاء الدفعة» repeats on every row and card as a `ghost` button, the
  same weight as the data.
- **What is wrong:**
  - An irreversible act is one stray tap away on every line.
  - The customer file offers it for subscription payments only, not for visit payments.
- **Proposal:**
  - The void moves into each row's «⋯» `DropdownMenu`, as the `destructive` item «إلغاء الدفعة…»,
    on Payments and the file. In the file, visit payments get it too.
  - The `AlertDialog` (P9) repeats the amount, the customer and the date.
- **Why it is better:**
  - One deliberate extra tap on the one irreversible act (2 taps become 3).
  - Rows read as data.
- **Cost:** S
- **Rule:** P9; ADR 0010 rule 3.

### DK-017 — Customers and Payments at 768: which columns survive
- **Type:** improvement · **Level:** page · **Impact:** low
- **Where:**
  - frames: 26 «Customers · owner» and 32 «Ledger · this month» (no 768 frame);
  - URLs: `…/Customers.html` and `…/Payments.html` at 768.
- **Evidence:** `DK-017.png` (Customers, 7 columns at 768); `DK-016.png` (Payments, 7 columns,
  names wrapping to two lines).
- **What is wrong:** both tables keep 7 columns at 768 (SH-007: more than five becomes cards or names
  a priority).
- **Proposal:** keep tables from `md` with **5 columns** (Desk's present list already fits 6 at 768):
  - **Customers:**
    - «الاسم» (the phone under it);
    - «الاشتراك» («حتى 20 أكتوبر» under it);
    - «الحالة»;
    - «الرصيد»;
    - «⋯».
  - **Payments:**
    - «التاريخ» (the time under it);
    - «الزبون» (the item under it);
    - «المبلغ» (the method under it);
    - «سجّلها»;
    - «⋯».
  - Cards below `md`.
- **Why it is better:** the scanning column (name, amount) stays wide, and nothing wraps.
- **Cost:** S
- **Rule:** SH-007; foundation §9 (as amended).

### DK-018 — Money actions: a retry that is safe, and a failure that names what was saved
- **Type:** improvement · **Level:** pattern · **Impact:** high
- **Where:**
  - frames 22–25 and 27 (every desk dialog); none draws a failure;
  - URL: `…/Desk.html?role=reception&dialog=checkout&pid=pv0`.
- **Evidence:** `DK-018.png` (the check-out dialog, where the failure appears). The prototype has no
  failure state for check-in, check-out, payment, subscription or void.
- **What is wrong:**
  - On the desk's weak connection a request can succeed while its answer is lost (ADR 0015). The
    person at the desk must know whether to try again.
  - The sheet sends two writes (the subscription, then its payment), so it can half-succeed.
- **Proposal:** applying P8's dialog failure, money actions say:
  - «لم يصل الرد. أعد المحاولة — لن تُسجَّل مرتين.» (destructive `Alert` inside the dialog; the
    retry reuses the action's key);
  - for the sheet: «حُفظ الاشتراك؛ لم تُسجَّل الدفعة 300 ₪» with «إعادة المحاولة» for the payment
    only;
  - a 429 says the same, with its wait.

  Subscriptions need their key first (ADR 0015 rule 4, step 8).
- **Why it is better:** no one records a payment twice «to be sure», or skips one that was not
  saved.
- **Cost:** S (design), with the API's keys
- **Rule:** ADR 0015 rules 1, 3 and 4; API contract §1 (Idempotency-Key), §3 (429).

### DK-019 — The present list needs one whole read
- **Type:** defect · **Level:** page · **Impact:** medium
- **Where:**
  - frame: 21 «Desk · owner (أحمد) — desktop 1440»;
  - URL: `…/Desk.html`.
- **Evidence:** `DK-019.png`. One list of 27, visits and subscribers mixed and sorted by «منذ»,
  searched locally.
- **What is wrong:**
  - The plan serves it from two paged lists (`GET /visits?open=true`, `GET /check-ins?open=true`, 20
    a page, at most 50).
  - Two paged lists cannot be merged in order, searched or counted («27 / 40») on the client past the
    first page. The «السجل» tab has the same problem.
- **Proposal:**
  - A composed read, «الحاضرون الآن», answered **whole**: it is bounded by the people present. It
    holds the kind, the name, `since`, today's usage line and the visit's charge so far.
  - The log is a paged composed read by day.

  This is a §4 exception (§4, rule 1). For worker B: step 7.
- **Why it is better:** the page can be served exactly as designed, with one request.
- **Cost:** M (API)
- **Rule:** API contract §4; plan › Planned API surface (visits, check-ins).

### DK-020 — «تسجيل كزيارة» drops the customer
- **Type:** improvement · **Level:** page · **Impact:** medium
- **Where:**
  - frame: 22 «Expired → «تسجيل كزيارة» / «تجديد» — phone 390»;
  - URL: `…/Desk.html?role=reception&dialog=warn&cid=m5`;
  - screenshot: `screens/22-check-in-warnings/04-expired-phone-390.webp`.
- **Evidence:** `DK-020.png`. The visit is created by name only (`checkInVisit(c.name, …)`).
- **What is wrong:**
  - If the expired subscriber leaves without paying, the desk must type his phone again to record a
    debt the system could have attached.
  - The visit is also missing from his file.
- **Proposal:** the visit is checked in **as the customer**, which the model allows («by name, as a
  customer, or both»). At check-out, «لم يدفع شيئًا» needs no phone, and the visit appears in his
  file.
- **Why it is better:** one fewer field to type, and the debt lands on the right person.
- **Cost:** S
- **Rule:** data model › Operations › Visit.

### DK-021 — The check-out shows a hard-coded rounding rule
- **Type:** defect · **Level:** page · **Impact:** low
- **Where:** frame 23 «Visit · 4 h × 3 ₪ = 12 ₪», as DK-004.
- **Evidence:** `DK-021.png`. «4 س · تقريب لأعلى بعد 10 دقائق».
- **What is wrong:** the rounding rule is the space's setting (the default rounds up after 15
  minutes), and the cap can be turned off. The line must not state a rule of its own.
- **Proposal:** the line is built from the space's settings: «4 س · تقريب لأعلى بعد 15 دقيقة».
  «السقف: سعر اليوم» appears only when the cap is on and applied.
- **Why it is better:** the desk can explain the charge truthfully to the customer.
- **Cost:** S
- **Rule:** data model › Visit charge; Setting › newSpaceDefaults.

### DK-022 — «بدون اشتراك» is a choice in two filters
- **Type:** defect · **Level:** page · **Impact:** low
- **Where:**
  - frame: 26 «Filter · owes money»;
  - URL: `…/Customers.html` at 390, the filter sheet.
- **Evidence:** `DK-022.png`. The status list repeats the type filter's «بدون اشتراك».
- **What is wrong:** the same fact can be filtered two ways, and the two can contradict each other.
- **Proposal:**
  - «بدون اشتراك» stays only under «نوع الاشتراك».
  - «الحالة» is «نشط · ينتهي قريبًا · منتهٍ», three choices, so P5's `ToggleGroup` chips (plus
    «مؤرشف», DK-014).
- **Why it is better:** one place per fact, and fewer taps to filter.
- **Cost:** S
- **Rule:** foundation §13 row 14; P5.

### DK-023 — The visit dialog shows choices the space may not use
- **Type:** improvement · **Level:** page · **Impact:** low
- **Where:**
  - frame: 22 «Visit dialog — phone 390»;
  - URL: `…/Desk.html?role=reception&dialog=visit`;
  - screenshot: `screens/22-check-in-warnings/02-visit-dialog-phone-390.webp`.
- **Evidence:** `DK-023.png`. «طالب» and «الوردية» are always shown.
- **What is wrong:**
  - Student rates apply to visits only when the space's settings allow them.
  - Shifts exist only when the space defines them.
- **Proposal:**
  - «طالب» is shown only when student visit prices are on.
  - «الوردية» is shown only when the space has shifts, defaulting to the shift in progress.
  - The `DialogDescription` names the rate that will apply («تُحسب 3 ₪ للساعة · حتى 15 ₪»).
- **Why it is better:** most spaces get a one-field dialog: type the name, press Enter (Enter
  already submits).
- **Cost:** S
- **Rule:** data model › Visit charge.

### DK-024 — The subscription sheet is three-quarters wide on a phone
- **Type:** improvement · **Level:** design system · **Impact:** medium
- **Where:**
  - frame: 24 (all phone frames);
  - URL: `…/Desk.html?role=reception&dialog=sheet&mode=renew&cid=m7` at 390.
- **Evidence:** `DK-024.png`. `Sheet side="end"` is about 293 px wide on a 390 phone. The desk's
  longest form gets 293 px, and the page behind stays visible.
- **What is wrong:** on a phone the side panel wastes a quarter of the width, and the tall form
  scrolls inside it.
- **Proposal:** `Sheet side="end"` is full width below `md` (the layer's `SheetContent` responsive
  width). The footer stays fixed.
- **Why it is better:**
  - Every field and the money block get the full width.
  - The two footer buttons fit side by side.
- **Cost:** S
- **Rule:** foundation §12 `Sheet`; §9.

## 3b. Tap counts on a phone (390, reception)

A tap is a press on a control. Typing is noted separately.

| Task | Today | Proposed |
|---|---|---|
| Check in a subscriber (no warning) | 2 (search, «حضور») + name | 2 |
| Check in a visitor after a search with no result | 3 + the name typed **twice** | 3 + the name once (DK-002); or 2 from the bottom bar, unchanged |
| Check out a visitor paying the exact amount | 3 (the second search, «خروج», «خروج ودفع») + a scroll past the first block | 3 with no scroll (DK-001), the amount on the button |
| Check out a visitor who leaves owing | 5 + phone | 4 + phone (DK-004); 3 with no typing when the visitor is a customer (DK-020) |
| Check out a fixed-price subscriber | 3 | 2 (DK-010) |
| New customer + subscription paid in full, from a search | 6 (+1 for another package) | 4 (+1) (DK-006, DK-004) |
| Renewal for a customer who owes, paying both | 6, and the renewal entered twice | 2 (DK-005) |
| Collect an uncollected visit | 2 after a 4,100 px scroll | 2, on the first screen (DK-003) |
| Receive a payment from a customer | 3 | 3, the amount on the button (DK-013) |
| Void a payment (owner) | 2 + reason | 3 + reason, deliberately (DK-016) |

## 3c. Owner vs reception — is each difference right?

- **Desk:** identical for both. **Right:** check-in/out, present/capacity, the override and payments
  are both roles' (ADR 0009 table).
- **Customers › «أرشفة»:** owner only. **Right in practice, but undocumented:** ADR 0009's table does
  not name archiving or editing a customer (§4, rule 3). Editing (DK-014) should be both roles'.
  Archiving should stay the owner's: it hides a debtor from the desk.
- **Customer file › void:** owner only. **Right** (ADR 0009, 0010).
- **Customer file › «إنهاء الاشتراك»:** both roles. **Right** («the desk can end any subscription
  early»).
- **Customer file › payments tab:** reception sees every payment of that customer, any date and any
  staff. **Right:** it answers «did I pay?». ADR 0009's «own, today» is about collections, not a
  customer's statement.
- **Customer file › WhatsApp reminder:** both roles. **Right:** a link a person sends by hand, not an
  automated notification.
- **Sheet › «تعديل السعر», custom price:** both roles. **Right** (ADR 0009: «custom»). The «سعر يدوي»
  badge shows the owner in the file who typed it; the file should name who («سعر يدوي · سامي»), as
  the model records (ADR 0010 rule 6).
- **Payments vs «دفعاتي اليوم»:** **right.** The gap is DK-015: a void must reach reception's view.

## 4. Rules in doubt

1. **API contract §4 (every list pages)** makes the desk's present list unservable as one ordered,
   searchable, counted list (DK-019). **Proposed:** an exception, like the lookups. «الحاضرون الآن»
   is answered whole, bounded by the people present.
2. **Uncollected visits have no end state** (data model). A visitor who left unseen at closing stays
   in «غير محصّل» and in debt forever: there is no void for a charge, and no write-off. **Proposed
   for the owner to decide:** an owner-only «لن يُحصَّل» with a reason, recorded and audited, which
   removes the visit from the uncollected list and the debt. It is never a payment and never a
   deletion. If declined, the desk card shows only the last 7 days with «عرض الكل».
3. **ADR 0009's permission table** does not name archiving, restoring or editing a customer.
   **Proposed:** add the rows (edit: both roles; archive and restore: owner).
4. **Days per week without which days** (data model), DK-009. The owner decides whether
   subscriptions gain weekdays. Until then the warning uses the count.

## 5. Not reviewed

- **Real failure and 429 states:** the prototype draws none, so DK-018 is reasoned from ADR 0015 and
  the contract, not seen.
- **The override popover** (P2, settled) and «ضبط الحالة» outside opening hours: looked at, and not
  reported.
- **Owner overview and Finance:** another review's scope, apart from their use of the same ledger.
- **A screen reader pass:** the keyboard pass was done with CDP key events. Focus moves into each
  dialog (check-out opens on the amount field), stays trapped, and Escape returns it to the row's
  «خروج». Enter submits the visit dialog. Live-region wording was checked from the source only.
- **Touch target sizes:** not measured. The decided 44 × 44 hit area (AD-030) covers the desk's `sm`
  buttons.
- **The section 41 date picker** in the attendance statement: seen at 390 and 1440, and it works; its
  component is the design system's.
- **Widths and themes:**
  - every page was captured in Arabic light at 390, 768 and 1440;
  - English at 390 (and 768 or 1440 for Desk and the customer file);
  - dark at 390 (Desk, the customer file, Payments);
  - dark at 1440 only through the board's own section 50 frames.

  Dialogs at 768 were spot-checked (check-out, sheet). No horizontal scroll was found on the pages
  measured: Desk, Customers and Payments at 768; Desk and the customer file at 390.
