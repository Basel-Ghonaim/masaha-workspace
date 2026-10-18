# Design fix 6: the front desk, in the prototype — the last batch

Planner: Claude Code (Opus 5.5). Planned in `C:\Users\basel\masaha-design-b`, detached at `origin/main`
`1240736`, tree clean, fetched; batch 5 read from `origin/design/owner` at `5a22676` (PR #76, open, being
rebased). Subagents used: 0 of 2. No branch cut, no file of the repository edited.

**How this plan was checked.** Every line of code below was built first in a **scratch copy** of the
prototype, taken outside the repository from `origin/design/owner` (`git archive`, so batch 5's shell,
plurals and data are under it), served on a scratch port and opened headless at 390, 768 and 1440, Arabic
and English, light and dark: 0 blank pages, 0 horizontal overflow, 0 console errors or warnings, and the
screenshots looked at. The board's 67 existing frames on the desk's five pages also still open (0 blank,
0 overflow, 0 errors at 390 and 1440), and batch 5's pages that read the desk's data (overview, Finance,
announcements, staff, packages, settings, audit, data reports) still render. The scratch copy is not the build: the executor builds from this plan, in the
repository, commit by commit, and checks again.

**How to read this plan.** It is an execution script. Every user-facing string is in the code as
`tr('عربي', 'English')`; the tables in §3 list the new ones. Where a step says *quote*, the lines are the
current code, to find the place — find by the text, never by a line number. *Replace from A up to B* means:
from the first line that starts with A (inclusive) up to the first later line that starts with B
(exclusive). Code blocks are copied **exactly**, indentation included. Nothing is "as appropriate": where a
choice existed it is taken, and §4 says why.

**Where to build.** In `C:\Users\basel\masaha-design-b` (this worktree), on branch `design/desk`, the
prototype served on **5347**. Batch 5's worktree, `masaha-design`, is cleaned once #76 merges.

---

## 1. Summary and contract

### Summary

Batch 6 of the design review — the front desk — applied to the prototype: **one desk search** that finds
the people present first, then the customers, then «تسجيل زيارة باسم «…»» with the typed name carried
(K1); **one money block** wherever money is taken — check-out, «استلام دفعة», the subscription sheet —
with what is due, what was received (filled with it), the method, a live line for the debt or the change,
and a submit that names the amount (K2); **a renewal with a debt pays the old balance first** (K3); **no
hidden money** — the customer file lists unpaid visits and the visits' payments through the customer, and
«دفعاتي اليوم» shows a voided payment struck with who and why (K4); the weekday warning becomes **the
count** (K5); the owner's **«لن يُحصَّل»** write-off (K6); the desk keeps its **toasts with the amount**
(K7); and the smaller items DK-003, DK-006–DK-008, DK-010–DK-018, DK-020–DK-023, plus batch 5's DI-35
(`Desk.html#unpaid`) and DI-36 (`Payments.html?month=`). After this batch the screenshots in
`docs/design/screens/` are regenerated once (not this batch's work).

### Scope

`docs/design/` only:
- the desk's pages and modules: `prototype/Desk.html`, `Customers.html`, `Customer file.html`,
  `Payments.html`, `My payments.html`, `masaha/desk-core.jsx`, `masaha/desk-sheet.jsx`, `masaha/desk-data.js`;
- `masaha/masaha.css`: **one layout rule** (the desk's order below and from 1280; tokens none);
- **one line each**, once #76 has merged, in `Owner overview.html` (DI-35) and `Finance.html` (DI-36);
- the shared archive files, this batch's part only: `CHANGES.md` (*Batch 6*), `INDEX.md` (a *Batch 6*
  parameters table, section 56, and the labels of the twelve desk frames §4 S8 relabels), the board
  `Flows - states.html` (section 56 below batch 5's, and the same twelve labels), `README.md`'s counts,
  `SCREENS.md`'s rows 13–17 (their board sections gain 56).

### Acceptance criteria (the reviewer ticks each)

- [ ] **AC1 · K1** — Searching on the desk shows «حاضر الآن» rows (name, its badge, «منذ …», «خروج») before
  the customers' cards, then «تسجيل زيارة باسم «X»» and «زبون جديد باسم «X»»; `?q=لمى` shows Lama (present,
  a visit) and Salma (a customer). With no match, «تسجيل زيارة باسم «X»» is the primary button. A digits-only
  term (≥ 2 digits) matches a mobile's end and offers «تسجيل زيارة» and «زبون جديد بهذا الرقم». Both carry
  what was typed into their dialog. The present list has no search of its own.
- [ ] **AC2 · K2** — The check-out, «استلام دفعة» and the sheet each show one money block: the calculation
  once, «المستحق», «المستلم الآن (₪)» filled with what is due, «الطريقة» (hidden at 0), the live line, and
  a submit naming the amount: «خروج واستلام 12 ₪», «تسجيل 150 ₪», «حفظ واستلام 300 ₪»; at 0 «خروج بدون
  دفع», «حفظ بدون دفع». 20 ₪ received for 12 ₪ says «الباقي للزبون 8 ₪» and records 12. Less than due on a
  visit with no customer says «المتبقي 7 ₪ يصبح دينًا على هبة المصري — رقم الجوال مطلوب» and shows the
  name and mobile; «لم يدفع شيئًا» sets 0. The check-out has no «خروج بدون دفع» mode any more.
- [ ] **AC3 · K3** — `Customers.html?role=reception&renew=m6`: a warning «مستحق من قبل 150 ₪ · اشتراك
  سبتمبر» with «يُطبَّق المستلم عليه أولًا، ثم على التجديد.» and no button; the block «اشتراك سبتمبر 150 ₪ /
  التجديد: شهري طلاب 250 ₪ / المجموع 400 ₪»; the submit «تجديد واستلام 400 ₪»; after it, one payment on
  September and one on the renewal, and the toast names both.
- [ ] **AC4 · K4** — `Customer file.html?id=m14`: «زيارات غير مدفوعة» lists the 28 Sep visit (12 ₪,
  «تحصيل»); «الدفعات» lists the 21 Sep visit payment (matched by `customerId`). `My payments.html?role=
  reception`: Farah's 6 ₪ struck, «ألغاها أحمد: سُجّلت بالخطأ», and the figures 45 / 59 / 104 ₪ (4
  payments) leave it out. Every money toast names the amount, the item and the method.
- [ ] **AC5 · K5** — `Desk.html?role=reception&dialog=warn&cid=m12`: «استُنفدت أيام هذا الأسبوع» with
  «هذا الأسبوع 3 من 3»; no weekday names anywhere on the desk's pages.
- [ ] **AC6 · K6** — The owner sees «لن يُحصَّل…» in each uncollected row's «⋯» (desk and file); it opens
  an `AlertDialog` with a required «السبب», the destructive «لن يُحصَّل» and «رجوع»; confirmed, the visit
  leaves the list and the debt, and the toast says so with the reason. Reception has no «⋯» there.
- [ ] **AC7 · K7** — Check-in, check-out and every money action raise a success toast; money's names the
  amount (and the change or the debt left).
- [ ] **AC8 · DK-003** — At 390 and 768 the desk reads: search, the uncollected card (title «4 زيارات غير
  محصّلة · 36 ₪», three rows, «عرض الكل»), then «الحاضرون الآن 27 / 40» with «الآن | السجل» beside it,
  said once. At 1440 the card is the side column. Empty (`?state=empty`): no card below 1280.
- [ ] **AC9 · DK-006–DK-008** — The sheet has no steps; a new customer's «رقم الجوال» drops «اختياري»
  while something stays unpaid, and the error moves focus to it. A renewal shows «شهري طلاب · 250 ₪ · 1
  أكتوبر – 30 أكتوبر» and «تغيير الباقة»; packages are one line each. «مخصّص» with no end shows «بلا حدّ ·
  يبقى نشطًا حتى يُنهى» with the warning icon, or «بلا تاريخ نهاية · ينتهي عند استهلاك 20 ساعة».
- [ ] **AC10 · DK-010, DK-020** — A fixed-price subscriber's «خروج» acts at once (toast «سُجّل خروج محمد
  العطار» / «4 س 35 د»); a usage-based one opens the dialog filled with what is owed so far. `pid=pv5`
  (Ahmad, checked in as the customer): «لم يدفع شيئًا» asks for no mobile.
- [ ] **AC11 · DK-012** — The uncollected rows with no customer (Yazan, Iyad) offer «تحصيل» (the pay dialog
  on the visit: «تحصيل زيارة · يزن الأسطل») and «تسجيل دينًا» (name + mobile).
- [ ] **AC12 · DK-013, DK-014, DK-022, DK-017** — Card, file header and Customers row show the actions by
  state in one order; «تعديل البيانات» edits the name and mobile with PHONE_TAKEN on the field; «مؤرشف»
  (owner) lists Abeer with «استرجاع»; status chips «الكل · نشط · ينتهي قريبًا · منتهٍ · مؤرشف»;
  Customers and Payments are five-column tables at 768.
- [ ] **AC13 · DK-016** — The void is the destructive item of each live payment row's «⋯» on Payments and in
  the file (visit payments included), owner only; its `AlertDialog` repeats amount, customer, date.
- [ ] **AC14 · DK-018** — `?fail=checkout|pay|sheet|visit` show «لم يصل الرد. أعد المحاولة — لن تُسجَّل
  مرتين.» inside the dialog; `?state=ratelimit` shows the 429 warning in it; `?fail=sheet-pay&half=1` shows
  «حُفظ الاشتراك؛ لم تُسجَّل الدفعة 90 ₪» and the payment-only retry.
- [ ] **AC15 · DK-021, DK-023** — The check-out's line reads «تقريب لأعلى بعد 15 دقيقة»; the visit dialog
  names the rate («تُحسب 3 ₪ للساعة · حتى 15 ₪»), shows «الوردية» on the morning shift and no «طالب» by
  default; `?demo=studentprices` shows «طالب», `?demo=noshifts` hides «الوردية».
- [ ] **AC16 · P1** — On a phone the desk's bottom bar holds «تسجيل زيارة» only; «استلام دفعة» and «زبون
  جديد» are in the top bar's «⋯» (from 768, buttons in the top bar). Customers keeps «زبون جديد» above
  the list; Payments keeps «تصدير CSV».
- [ ] **AC17 · DI-35, DI-36** — The overview's uncollected row links `Desk.html#unpaid`, which lands on the
  card. Finance › الديون › «عرض الكل» opens `Payments.html?month=<the month chosen>`, filtered to it.
- [ ] **AC18 · states** — Each changed page keeps loading, empty, error, offline, 403 and 404
  (`?state=…`), and none blanks, errors or overflows at 390 / 768 / 1440, ar/en, light/dark.
- [ ] **AC19 · board** — Section 56 at top 160000 with 37 frames as §6 lists; `INDEX.md` §56 has the same
  37 rows; twelve old desk frames relabelled in both; `README.md`'s counts true; `SCREENS.md` rows 13–17
  name 56.
- [ ] **AC20 · boundaries** — `git diff --stat origin/main` lists only §5's files; `shared.jsx`, `owner.jsx`,
  `owner-data.js`, `admin.jsx`, `profile-*.jsx`, the account pages, `_ds/`, `_vendor/`, `screens/` untouched;
  `Owner overview.html` and `Finance.html` differ by one line each.

### Out of scope

- **DK-024 (with OW-010)** — the sheet full width below `md`: the design system's (worker A). The desk's
  sheet stays ¾ wide at 390 in the vendored bundle; its fields are single-column so nothing overflows.
- **K8 / DK-019** — «الحاضرون الآن» answered whole and the log as a paged read by day: the API's (worker B,
  step 7) and the docs' (api-contract §4). The prototype already draws one list.
- **The rules changed** (api-contract §4, ADR 0009's table rows for editing/archiving a customer, the data
  model's write-off): the docs', with steps 7–8.
- **The API keys of DK-018** and K6's write-off endpoint (steps 7–8).
- Everything in §4's design issues not marked *build*.
- Batch 5's files beyond the two lines; `shared.jsx` (the account batch's), `owner.jsx`, `owner-data.js`.

---

## 2. Reading done

- **This prompt** (`PROMPT\FIX_DESK_PROMPT.md`), **`DECISIONS_DESK.md`** (K1–K8, the smaller DK items, the
  rule changes), **`DECISIONS_SHARED.md`** with its amendments (P1's bottom bar, P8's desk exception, P9's
  archive), **`DECISIONS_OWNER.md`** (DI-10's shell, O5's plurals, O3's queue row), **`REPORT\
  REVIEW_DESK_REPORT.md`** whole (§2.1–§2.5, DK-001…DK-024, §3b–§4).
- **Batch 5's plan and report** (`PLAN\FIX_OWNER_PLAN.md` §4 DI-35/DI-36 and §7–§9 for the procedure's
  shape; `REPORT\FIX_OWNER_REPORT.md` §3–§7: the hooks crash, the missing imports, the stale Chrome, the
  flaky first load) and **`PROMPT\FIX_OWNER_FIXES.md`** (the rebase and three fixes: none touches a desk
  file).
- **The desk's current code**, whole: `Desk.html`, `Customers.html`, `Customer file.html`, `Payments.html`,
  `My payments.html`, `masaha/desk-core.jsx`, `desk-sheet.jsx`, `desk-data.js`; and from `shared.jsx`:
  `useActionRun`, `ActionButton`, `ActionAlert`, `actionFails`, `RATE_LIMIT_LINE`, `PageActions`,
  `FilterSheet`, `ResultCount`, `usePaged`, `DateField`, `PageToaster`.
- **Batch 5 as it will merge** (`git show origin/design/owner:<path>`), the lines this plan relies on:
  - `masaha/owner.jsx` — `OwnerShell({ current, title, state, theme, setTheme, bottomAction, actions,
    loadError, children })` calls `useHashLanding()` first (so `Desk.html#unpaid` scrolls to `id="unpaid"`),
    draws `bottomAction` below 768 only, and `PageActions` folds `actions` into «⋯» below 768 (an action
    with `bottom: true` is left out there); `Num`, `Counted({ n, ar, en })`, `countText`, `IS_OWNER`,
    `roleQ`, and the forms `F_MINUTES`, `F_SUBSCRIBERS`, `F_VISITS` (this plan uses them, never redefines
    them); `const O = window.OWNER;` is global.
  - `Owner overview.html` — `queueRows()`: `if (unpaid) rows.push({ key: 'unpaid', … action: tr('فتح
    المكتب', 'Open the desk'), href: 'Desk.html' });` (DI-35's one line).
  - `Finance.html` — `DebtsTab({ month })`: `<Button variant="link" size="sm" asChild><a
    href="Payments.html">{tr('عرض الكل', 'View all')}</a></Button>` (DI-36's one line).
  - `masaha/owner-data.js` — `?demo=` is a comma list (`demo(k)`), with `noshifts`; the desk's data reads
    the same parameter the same way.
  - `Owner settings.html` — the visit pricing card starts: round up after **15** minutes, the cap **on**,
    student prices for visits **on** (the desk's `SETTINGS` matches).
  - `masaha/profile-a.jsx` `SAMPLE_SHIFTS`: the morning shift 08:00–13:00, the evening 13:00–18:00 (the
    desk's `SHIFT_LIST` matches; the demo clock 12:40 is in the morning shift).
- **The design system's bundle** (`_ds/…/_ds_bundle.js`): the exports (no Collapsible, no Accordion);
  `Button` variants `primary · secondary · outline · ghost · destructive · link` and sizes `sm · md · lg ·
  icon` (**no `default`** — an unknown size or variant leaves a button unstyled); `DropdownMenuItem
  variant="destructive"`; `ToggleGroup` wraps (`flex-wrap`); `Field` takes `className`; `Input` passes
  `ref` and the field's `aria-invalid` to the `<input>`; React 19.
- **The prebuilt CSS**: every class this plan uses was checked against `_ds_bundle.css` + `styles.css` +
  `masaha.css` (§9 lists the dead ones to avoid).
- **The rules**: `docs/architecture/data-model.md` (Customer, Visit, Payment, Unpaid visit, Uncollected
  visits, Visit charge and its fallbacks, Subscription status, the ledger's constraints: a visit's or a
  fixed subscription's payments never exceed its charge; a visit left unpaid needs a phone; a visit closed
  by the automatic check-out may have no customer); ADR 0008 (live status a state); ADR 0009 (the
  permissions table: void, finance owner-only; check-in/out, payments, renewals both); ADR 0010 (one
  payment per item, oldest first; append-only; credit only on a usage-based subscription; warn, never
  block); ADR 0015 (idempotency keys); `docs/frontend/design-system/foundation.md` §9 (widths), §10 (submit
  stays enabled; focus to the first invalid field), §13 rows 13–17; `docs/project/overview.md` (*Not in
  v1*: no online payment, no QR, no booking — nothing here touches them); `docs/design/README.md`,
  `CHANGES.md` (batches 1–5), `INDEX.md`, `SCREENS.md`, `scripts/check-*.mjs`.

---

## 3. The decisions, as they will be built

Each block is one commit (§6). It names the decisions it builds, their strings, states and parameters, then
the exact edits. A block's code uses only names defined by its own or an earlier block.

### 3.1 Check-out takes money in one block — K2 (check-out), DK-004, DK-010, DK-020, DK-021, K7, DK-018 (commit 1)

**What is built.**

| Decision | On screen |
|---|---|
| K2 / DK-004 | `MoneyBlock`: the calculation, «المستحق 12 ₪» (a usage-based subscriber: «المستحق حتى الآن»), «المستلم الآن (₪)» filled with what is due, «الطريقة» when more than 0 is received, the live line (`aria-live="polite"`), the name and mobile under it when a visit with no customer leaves owing, «لم يدفع شيئًا» while something is received |
| DK-021 | «4 س × 3 ₪ = 12 ₪ · تقريب لأعلى بعد 15 دقيقة» — the minutes from the space's settings (`D.SETTINGS.roundAfter`); «السقف: سعر اليوم 15 ₪» only when the cap is on (`SETTINGS.cap`) and applied |
| DK-010 | `OutButton`: a fixed-price subscriber (or one with no subscription) checks out at once with the button's `loading`; others open the dialog |
| DK-020 | «تسجيل كزيارة» checks the visit in with the customer's id; its check-out needs no mobile |
| K7 / K4 | the check-out toast: title «سُجّل خروج X», description by case (table below) |
| DK-018 | inside the dialog: `ActionAlert` with «لم يصل الرد. أعد المحاولة — لن تُسجَّل مرتين.» (`?fail=checkout`); `MoneyRateNote` (`?state=ratelimit`) |

**New strings** (all in the code as `tr()`):

| Arabic | English |
|---|---|
| المستلم الآن (₪) | Received now (₪) |
| الطريقة (the label of the method, was «طريقة الدفع») | Method |
| الباقي للزبون {8 ₪} | Change to give back: {₪8} |
| يصبح له رصيد {8 ₪} | Becomes credit: {₪8} |
| المتبقي {7 ₪} يصبح دينًا على {X} | The remaining {₪7} becomes a debt for {X} |
| المتبقي {12 ₪} يبقى على اشتراك {X} | The remaining {₪12} stays on the subscription of {X} |
| المتبقي {3 ₪} يبقى غير محصّل | The remaining {₪3} stays uncollected |
| (appended to the debt line) — رقم الجوال مطلوب | (appended) — a mobile number is required |
| يُسجَّل المبلغ كاملًا. | Paid in full. |
| لا شيء مستحق الآن. | Nothing is due now. |
| لم يدفع شيئًا | Paid nothing |
| تقريب لأعلى بعد {15 دقيقة} | rounded up after {15 min} |
| السقف: سعر اليوم | Cap: the day price |
| لا يوجد سعر بالساعة — سعر اليوم | No hourly price — the day price |
| يُحسب من الحضور: … للساعة / لليوم | Billed from attendance: … per hour / per day |
| اليوم {3} س · المدفوع {30 ₪} | Today {3} h · Paid {₪30} |
| المستحق حتى الآن | Due so far |
| مشترك · يُحسب من الحضور | Subscriber · billed from attendance |
| مبلغ الزيارة (₪) · helper «لا يوجد سعر ساعة ولا سعر يوم منشور.» | Visit amount (₪) · "There’s no published hour or day price." |
| يُضاف إلى ملف {X} | Added to the file of {X} |
| خروج واستلام {12 ₪} · خروج بدون دفع | Check out and take {₪12} · Check out without paying |
| لم يصل الرد. أعد المحاولة — لن تُسجَّل مرتين. | No answer came back. Try again — it won’t be recorded twice. |
| لم يُسجَّل شيء. إعادة المحاولة بعد ذلك لن تسجّله مرتين. (under the 429 line) | Nothing was recorded. Trying again after that won’t record it twice. |
| Toast description: استُلم {12 ₪} نقدًا / تحويلًا عن الزيارة [· الباقي للزبون {8 ₪}] | {₪12} received in cash / by transfer for the visit [· {₪8} change] |
| … · المتبقي {7 ₪} دين على {X} ; لم يدفع · المتبقي … | … · {₪7} left as a debt for {X} ; Not paid · … |
| (subscriber, fixed) {4 س 35 د} ; (usage) استُلم … عن {sub} [· المتبقي … على الاشتراك] ; لم يدفع الآن | {4h 35m} ; … for {sub} [· … left on the subscription] ; No payment now |

**States:** working = the submit's `loading` (700 ms, `useActionRun('checkout')`); success = the toast;
failure = `?fail=checkout` (the Alert inside, the toast with «إعادة المحاولة»); 429 = `?state=ratelimit`;
offline/403/404/error = the shell's (unchanged). **Parameters:** `?dialog=checkout&pid=<id>&received=<₪>`
(new: `received`); `&debt=1` now means `received=0`; a fixed-price subscriber's `pid` checks out on load.

**Edits — `masaha/desk-data.js`**

1. Replace from `  const PRICES = {` up to `  const WEEKDAYS =` with:
```js
  const PRICES = { hour: 3, day: 15, week: 90, month: 300, studentMonth: 250, studentHour: null, studentDay: null };
  // Demo: ?prices=dayonly (no hour price) or ?prices=none (no hour and no day price).
  const PM = new URLSearchParams(location.search).get('prices');
  if (PM === 'dayonly' || PM === 'none') PRICES.hour = null;
  if (PM === 'none') PRICES.day = null;
  // The fix phase's sample states, a comma list as on the owner's pages: ?demo=noshifts,nocap,nostudent,studentprices.
  const DEMO = (new URLSearchParams(location.search).get('demo') || '').split(',');
  if (DEMO.includes('studentprices')) { PRICES.studentHour = 2; PRICES.studentDay = 10; }
  // DK-021, DK-023: the space's settings (SpaceSettings), as Owner settings starts them: round up after
  // 15 minutes, the cap at the day price on, student prices for visits on.
  const SETTINGS = { roundAfter: 15, cap: !DEMO.includes('nocap'), studentVisits: !DEMO.includes('nostudent') };
  // «طالب» changes a visit's rate only when the setting is on and the space publishes a student hour or day price.
  const STUDENT_VISITS = SETTINGS.studentVisits && (PRICES.studentHour != null || PRICES.studentDay != null);
  // The space's shifts, as the profile's sample saves them; ?demo=noshifts: none saved.
  const SHIFT_LIST = DEMO.includes('noshifts') ? [] : [{ id: 'am', from: '08:00', to: '13:00' }, { id: 'pm', from: '13:00', to: '18:00' }];
```
2. Replace the five lines from `  const visits = [` (that line, `  const present = [`, its two `...` lines and
   `  ].sort(…);`) with:
```js
  const visits = [[T('هبة المصري', 'Heba Al-Masri'), '08:40', true], [T('تالا شراب', 'Tala Sharab'), '09:25'], [T('روان مهنا', 'Rawan Muhanna'), '10:05', true], [T('آدم الحلو', 'Adam Al-Helou'), '10:50'], [T('جنى أبو ندى', 'Jana Abu Nada'), '11:15'], [T('أحمد الشوا', 'Ahmad Al-Shawa'), '11:40', false, 'm5'], [T('حسن الطويل', 'Hasan Al-Taweel'), '12:05'], [T('لمى الكرد', 'Lama Al-Kurd'), '12:20']];
  // DK-020: a visit may be checked in as a customer (pv5: Ahmad, whose subscription has ended).
  const present = [
    ...subPresent.map(([cid, since], i) => ({ id: 'ps' + i, kind: 'sub', customerId: cid, since })),
    ...visits.map(([name, since, student, cid], i) => ({ id: 'pv' + i, kind: 'visit', name, since, student: !!student && STUDENT_VISITS, customerId: cid || null }))
  ].sort((a, b) => (a.since < b.since ? 1 : -1));
```
3. Replace from `  // Visits: rounded up to the next hour after a 10-minute grace, capped at the day price.` up to
   `  const findCustomer =` with:
```js
  // A visit's rates: the student ones where «طالب» counts and the space has them, else the general ones.
  const visitRates = (student) => {
    const s = student && STUDENT_VISITS;
    return { hour: s && PRICES.studentHour != null ? PRICES.studentHour : PRICES.hour, day: s && PRICES.studentDay != null ? PRICES.studentDay : PRICES.day };
  };
  // DK-021: the space's rounding (up after SETTINGS.roundAfter minutes), capped at the day price when the cap is on.
  const visitCharge = (inT, outT = NOW, student = false) => {
    const mins = Math.max(0, toMin(outT) - toMin(inT));
    const r = visitRates(student);
    if (!r.hour) return r.day ? { mode: 'day', mins, hours: 0, day: r.day, amount: r.day } : { mode: 'manual', mins, hours: 0, amount: null };
    const hours = Math.max(1, Math.floor(mins / 60) + (mins % 60 > SETTINGS.roundAfter ? 1 : 0));
    const byHour = hours * r.hour;
    const capped = SETTINGS.cap && r.day != null && byHour > r.day;
    return { mode: 'hour', mins, hours, hour: r.hour, day: r.day, byHour, capped, amount: capped ? r.day : byHour };
  };
  // The shift in progress now, or '' outside every shift.
  const currentShift = () => { const s = SHIFT_LIST.find((x) => toMin(x.from) <= toMin(NOW) && toMin(NOW) < toMin(x.to)); return s ? s.id : ''; };
```
4. After the line `  const methodLabel = { cash: T('نقدًا', 'Cash'), transfer: T('تحويل', 'Transfer') };` insert:
```js
  // K4: the method inside a sentence («استُلم 12 ₪ نقدًا»).
  const methodIn = { cash: T('نقدًا', 'in cash'), transfer: T('تحويلًا', 'by transfer') };
```
5. In the `return { … }` at the end, before the line that starts `    toMin, hm, daysBetween,` insert the line:
```js
    SETTINGS, STUDENT_VISITS, SHIFT_LIST, visitRates, currentShift, methodIn,
```

**Edits — `masaha/desk-core.jsx`**

1. After the line `const phoneOk = (v) => normPhone(v).replace(/\D/g, '').length === 12;` insert:
```jsx
// K4: a stay and a payment in words, for a toast («4 س 35 د», «استُلم 12 ₪ نقدًا»).
const durText = (mins) => { const h = Math.floor(mins / 60), m = mins % 60; return LANG === 'en' ? (h ? h + 'h ' : '') + m + 'm' : (h ? h + ' س ' : '') + m + ' د'; };
const paidLine = (n, method) => tr(`استُلم ${$(n)} ${D.methodIn[method]}`, `${$(n)} received ${D.methodIn[method]}`);
// DK-018: a money request carries its key (ADR 0015), so its failure says a retry is safe.
const MONEY_RETRY = tr('لم يصل الرد. أعد المحاولة — لن تُسجَّل مرتين.', 'No answer came back. Try again — it won’t be recorded twice.');
// Foundation §10: a failed submit moves focus to the first invalid field of the open dialog or sheet.
const focusInvalid = () => setTimeout(() => { const bad = document.querySelector('[role=dialog] [aria-invalid="true"], [role=alertdialog] [aria-invalid="true"]'); if (bad) bad.focus(); });
// DK-010: a subscriber on a fixed price has nothing to settle at check-out, so it is one tap.
const isQuickOut = (p) => { if (p.kind !== 'sub') return false; const s = D.currentSub(D.findCustomer(p.customerId)); return !s || s.billing.type === 'fixed'; };
```
2. Replace the `checkInVisit` method — quote:
```jsx
    checkInVisit(name, student, shift) {
      D.present.unshift({ id: 'n' + Date.now(), kind: 'visit', name, student, shift, since: D.NOW });
      bump(); close(); toast.success(tr(`سُجّلت زيارة ${name}`, `Visit for ${name} checked in`));
    },
```
   with:
```jsx
    // DK-020: a visit may be checked in as a customer, whose file it then joins.
    checkInVisit(name, student, shift, customerId) {
      D.present.unshift({ id: 'n' + Date.now(), kind: 'visit', name, student: !!student, shift, customerId: customerId || null, since: D.NOW });
      bump(); close(); toast.success(tr(`سُجّلت زيارة ${name}`, `Visit for ${name} checked in`));
    },
```
3. Replace the `checkOut` method — from `    checkOut(pid, { received = 0,` up to `    // Applies to one item, or to the oldest first.` — with:
```jsx
    // K2 + K7: `recorded` is what the ledger takes — never more than a visit's charge; `change` is
    // handed back. What stays unpaid becomes the debt of the visit's customer, found or made by phone.
    checkOut(pid, { recorded = 0, change = 0, method = 'cash', debt, due } = {}) {
      const i = D.present.findIndex((p) => p.id === pid); const p = D.present[i];
      D.present.splice(i, 1);
      const mins = D.toMin(D.NOW) - D.toMin(p.since);
      const c = p.customerId ? D.findCustomer(p.customerId) : null;
      const who = c ? c.name : p.name;
      let desc;
      if (p.kind === 'visit') {
        const charge = due != null ? due : D.visitCharge(p.since, D.NOW, p.student).amount;
        const left = charge - recorded;
        let debtor = c;
        if (left > 0 && !debtor) {
          const phone = normPhone(debt.phone);
          debtor = D.customers.find((x) => !x.archived && x.phone === phone);
          if (!debtor) { debtor = { id: 'c' + Date.now(), name: debt.name || p.name, phone, subs: [] }; D.customers.unshift(debtor); }
        }
        if (recorded > 0) D.visitPays.unshift({ id: 'vp' + Date.now(), customerId: debtor ? debtor.id : null, name: debtor ? debtor.name : p.name, date: D.TODAY, time: D.NOW, amount: recorded, method, by: ME });
        if (left > 0) D.unpaid.unshift({ id: 'u' + Date.now(), customerId: debtor.id, date: D.TODAY, in: p.since, out: D.NOW, amount: left, how: 'left' });
        desc = left > 0
          ? (recorded > 0 ? paidLine(recorded, method) + ' · ' : tr('لم يدفع · ', 'Not paid · ')) + tr(`المتبقي ${$(left)} دين على ${debtor.name}`, `${$(left)} left as a debt for ${debtor.name}`)
          : paidLine(recorded, method) + tr(' عن الزيارة', ' for the visit') + (change > 0 ? tr(` · الباقي للزبون ${$(change)}`, ` · ${$(change)} change`) : '');
      } else {
        const s = c && D.currentSub(c);
        if (s) { s.used.todayMin = (s.used.todayMin || 0) + mins; if (s.billing.type === 'usage' || s.terms.hourBalance) s.used.hours = (s.used.hours || 0) + Math.ceil(mins / 60); }
        desc = durText(mins);
        if (s && s.billing.type === 'usage') {
          if (recorded > 0) s.pays.push([D.TODAY, D.NOW, recorded, method, ME]);
          const left = Math.max(0, D.due(s, c) - D.paid(s));
          desc = (recorded > 0 ? paidLine(recorded, method) + tr(` عن ${s.name}`, ` for ${s.name}`) : tr('لم يدفع الآن', 'No payment now')) + (left > 0 ? tr(` · المتبقي ${$(left)} على الاشتراك`, ` · ${$(left)} left on the subscription`) : '');
        }
      }
      bump(); close();
      toast.success(tr(`سُجّل خروج ${who}`, `${who} checked out`), { description: desc });
    },
```
4. In `WarnDialog`, quote:
```jsx
                <ActionButton actionKey="warn" onAction={() => desk.checkInVisit(c.name, !!c.student, null)}>{tr('تسجيل كزيارة', 'Check in as a visit')}</ActionButton>
```
   replace with:
```jsx
                <ActionButton actionKey="warn" onAction={() => desk.checkInVisit(c.name, !!c.student && D.STUDENT_VISITS, D.currentShift() || null, c.id)}>{tr('تسجيل كزيارة', 'Check in as a visit')}</ActionButton>
```
5. In `MethodToggle`, quote `    <DK.Field label={tr('طريقة الدفع', 'Method')}>` → replace with
   `    <DK.Field label={tr('الطريقة', 'Method')}>`.
6. Replace from `// 4.4 Check-out` up to `// 4.6 Receive payment` (the whole old `CheckoutDialog`) with:
```jsx
// K2: one money block wherever money is taken — what is due, what is received (filled with what is
// due), the method, and a live line: the debt that remains, or the change to give back. `open`: a
// usage-based subscription has no ceiling, so more than is due becomes credit, not change.
const moneyOf = (due, value, open) => {
  const rec = Math.max(0, Number(value) || 0);
  return open
    ? { rec, recorded: rec, left: Math.max(0, due - rec), change: 0, credit: Math.max(0, rec - due) }
    : { rec, recorded: Math.min(rec, due), left: Math.max(0, due - rec), change: Math.max(0, rec - due), credit: 0 };
};
function MoneyBlock({ calc, due, dueLabel, dueField, open, value, onValue, method, onMethod, error, remainder, who, phoneNote, none = true, children }) {
  const m = moneyOf(due, value, open);
  const rest = remainder === 'sub' ? tr('يبقى على اشتراك', 'stays on the subscription of') + ' ' + who
    : remainder === 'uncollected' ? tr('يبقى غير محصّل', 'stays uncollected')
    : tr('يصبح دينًا على', 'becomes a debt for') + ' ' + who;
  const line = m.change > 0 ? <>{tr('الباقي للزبون', 'Change to give back:')} <Money n={m.change} /></>
    : m.credit > 0 ? <>{tr('يصبح له رصيد', 'Becomes credit:')} <Money n={m.credit} /></>
    : m.left > 0 ? <>{tr('المتبقي', 'The remaining')} <Money n={m.left} /> {rest}{phoneNote ? tr(' — رقم الجوال مطلوب', ' — a mobile number is required') : ''}</>
    : due > 0 ? tr('يُسجَّل المبلغ كاملًا.', 'Paid in full.') : tr('لا شيء مستحق الآن.', 'Nothing is due now.');
  const nothing = () => { onValue('0'); setTimeout(() => { const tel = document.querySelector('[role=dialog] input[type=tel]'); if (tel) tel.focus(); }); };
  return (
    <div className="flex flex-col gap-4 rounded-lg bg-muted p-3">
      {calc && <div className="flex flex-col gap-1 text-body-sm">{calc}</div>}
      {dueField || <p className="text-heading-3">{dueLabel || tr('المستحق', 'Due')} <Money n={due} /></p>}
      <div className="grid gap-4 md:grid-cols-2">
        <DK.Field label={tr('المستلم الآن (₪)', 'Received now (₪)')} error={error}><DK.Input inputMode="numeric" dir="ltr" value={value} onChange={(e) => onValue(e.target.value.replace(/[^\d]/g, ''))} /></DK.Field>
        {m.rec > 0 && <MethodToggle value={method} onChange={onMethod} />}
      </div>
      <p aria-live="polite" className="text-body-sm">{line}</p>
      {m.left > 0 && children}
      {none && m.rec > 0 && <DK.Button type="button" variant="outline" className="self-start" onClick={nothing}>{tr('لم يدفع شيئًا', 'Paid nothing')}</DK.Button>}
    </div>
  );
}

// DK-018: the 429 inside a money dialog says that nothing was recorded, so the retry is safe too.
function MoneyRateNote() {
  if (pageParams.get('state') !== 'ratelimit') return null;
  return <DK.Alert variant="warning"><DK.AlertTitle>{RATE_LIMIT_LINE}</DK.AlertTitle><DK.AlertDescription>{tr('لم يُسجَّل شيء. إعادة المحاولة بعد ذلك لن تسجّله مرتين.', 'Nothing was recorded. Trying again after that won’t record it twice.')}</DK.AlertDescription></DK.Alert>;
}

// «خروج» on a row, a card or the file: one tap for a fixed-price subscriber (DK-010), the dialog otherwise.
function OutButton({ p, size, variant = 'outline' }) {
  const desk = useDesk();
  const { busy, run } = useActionRun('checkout');
  const quick = isQuickOut(p);
  return <DK.Button size={size} variant={variant} loading={quick && busy} aria-label={tr('خروج ', 'Check out ') + nameOf(p)} onClick={() => (quick ? run(() => desk.checkOut(p.id)) : desk.open('checkout', { presentId: p.id }))}><DK.LogOutIcon />{tr('خروج', 'Check out')}</DK.Button>;
}

// 4.4 Check-out: a visit, or a subscriber billed from attendance.
function CheckoutDialog({ dlg, onClose }) {
  const desk = useDesk();
  const p = dlg && D.present.find((x) => x.id === dlg.presentId);
  const [received, setReceived] = React.useState(''); const [method, setMethod] = React.useState('cash');
  const [dName, setDName] = React.useState(''); const [dPhone, setDPhone] = React.useState(''); const [err, setErr] = React.useState({});
  const [manualAmt, setManualAmt] = React.useState('');
  const c = p && p.customerId ? D.findCustomer(p.customerId) : null;
  const s = p && p.kind === 'sub' && c ? D.currentSub(c) : null;
  const ch0 = p && p.kind === 'visit' ? D.visitCharge(p.since, D.NOW, p.student) : null;
  const ch = ch0 && (ch0.mode === 'manual' ? { ...ch0, amount: Number(manualAmt) || 0 } : ch0);
  // A usage-based subscriber: what the subscription owes so far, today included.
  const subDue = s ? Math.max(0, D.due(s, c) - D.paid(s)) : 0;
  const due = ch ? ch.amount : subDue;
  React.useEffect(() => { if (p) { setManualAmt(''); setReceived(dlg.received != null ? dlg.received : ch0 && ch0.mode === 'manual' ? '' : String(due)); setMethod('cash'); setDName(p.kind === 'visit' ? p.name : ''); setDPhone(''); setErr({}); } }, [dlg && dlg.presentId]);
  const { busy, run } = useActionRun('checkout');
  if (!p) return <DK.Dialog open={false}><DK.DialogContent closeLabel="" /></DK.Dialog>;
  const mins = D.toMin(D.NOW) - D.toMin(p.since);
  const m = moneyOf(due, received, !!s);
  // An unpaid visit needs a phone; a visit checked in as a customer already has its debtor (DK-020).
  const needPhone = !!ch && !c && m.left > 0;
  const match = needPhone && phoneOk(dPhone) ? D.customers.find((x) => !x.archived && x.phone === normPhone(dPhone)) : null;
  const finish = () => {
    if (ch && ch.mode === 'manual' && !(ch.amount > 0)) { setErr({ manual: tr('أدخل مبلغ الزيارة', 'Enter the visit amount') }); return focusInvalid(); }
    if (needPhone) {
      const e = {};
      if (!dName.trim()) e.name = tr('أدخل الاسم', 'Enter the name');
      if (!phoneOk(dPhone)) e.phone = tr('رقم الجوال مطلوب ليُسجَّل المبلغ دينًا، مثل +970 59 000 0000', 'A mobile number is needed to record the debt, e.g. +970 59 000 0000');
      setErr(e); if (Object.keys(e).length) return focusInvalid();
    }
    run(() => desk.checkOut(p.id, { recorded: m.recorded, change: m.change, method, due, debt: { name: dName.trim(), phone: dPhone } }));
  };
  // DK-021: the line says the space's own rule; the cap only when it is on and applied.
  const calc = ch && ch.mode === 'hour' ? <>
    <span><Num>{ch.hours}</Num> {tr('س', 'h')} × <Money n={ch.hour} /> = <Money n={ch.byHour} /> · {tr('تقريب لأعلى بعد', 'rounded up after')} <Counted n={D.SETTINGS.roundAfter} ar={F_MINUTES.ar} en={F_MINUTES.en} /></span>
    {ch.capped && <span>{tr('السقف: سعر اليوم', 'Cap: the day price')} <Money n={ch.day} /></span>}
  </> : ch && ch.mode === 'day' ? <span>{tr('لا يوجد سعر بالساعة — سعر اليوم', 'No hourly price — the day price')} <Money n={ch.day} /></span>
    : s ? <>
      <span>{s.name} · {tr('يُحسب من الحضور:', 'Billed from attendance:')} <Money n={s.billing.rate} /> {s.billing.unit === 'hour' ? tr('للساعة', 'per hour') : tr('لليوم', 'per day')}</span>
      <span>{tr('اليوم', 'Today')} <Num>{Math.ceil(mins / 60)}</Num> {tr('س', 'h')} · {tr('المدفوع', 'Paid')} <Money n={D.paid(s)} /></span>
    </> : null;
  const dueField = ch && ch.mode === 'manual' ? (
    <DK.Field label={tr('مبلغ الزيارة (₪)', 'Visit amount (₪)')} labelEnd={<DK.Badge variant="info">{tr('سعر يدوي', 'Manual price')}</DK.Badge>} helper={tr('لا يوجد سعر ساعة ولا سعر يوم منشور.', 'There’s no published hour or day price.')} error={err.manual}>
      <DK.Input inputMode="numeric" dir="ltr" value={manualAmt} onChange={(e) => { const v = e.target.value.replace(/[^\d]/g, ''); setManualAmt(v); setReceived(v); }} autoFocus />
    </DK.Field>
  ) : null;
  const label = m.recorded > 0 ? <>{tr('خروج واستلام', 'Check out and take')} <Money n={m.recorded} /></> : tr('خروج بدون دفع', 'Check out without paying');
  return (
    <DK.Dialog open onOpenChange={(o) => !o && onClose()}>
      <DK.DialogContent closeLabel={tr('إغلاق', 'Close')}>
        <DK.DialogHeader>
          <DK.DialogTitle>{tr('تسجيل خروج', 'Check out')} · {nameOf(p)}</DK.DialogTitle>
          <DK.DialogDescription>{p.kind === 'visit' ? tr('زيارة', 'Visit') + (p.student ? tr(' · طالب', ' · student') : '') : tr('مشترك · يُحسب من الحضور', 'Subscriber · billed from attendance')}</DK.DialogDescription>
        </DK.DialogHeader>
        <div className="flex flex-col gap-4">
          <dl className="flex flex-col divide-y">
            <Row k={tr('الدخول', 'In')} v={<Num>{p.since}</Num>} />
            <Row k={tr('الخروج', 'Out')} v={<Num>{D.NOW}</Num>} />
            <Row k={tr('المدة', 'Duration')} v={durLabel(mins)} />
          </dl>
          <MoneyBlock calc={calc} due={due} dueLabel={s ? tr('المستحق حتى الآن', 'Due so far') : undefined} dueField={dueField} open={!!s} value={received} onValue={setReceived} method={method} onMethod={setMethod}
            remainder={s ? 'sub' : 'debt'} who={c ? c.name : dName.trim() || p.name} phoneNote={needPhone}>
            {needPhone && (
              <div className="grid gap-3 md:grid-cols-2">
                <DK.Field label={tr('الاسم', 'Name')} error={err.name}><DK.Input value={dName} onChange={(e) => setDName(e.target.value)} /></DK.Field>
                <DK.Field label={tr('رقم الجوال', 'Mobile number')} error={err.phone} helper={match ? tr('يُضاف إلى ملف ', 'Added to the file of ') + match.name : undefined}><DK.Input type="tel" dir="ltr" placeholder="+970 59 000 0000" value={dPhone} onChange={(e) => setDPhone(e.target.value)} /></DK.Field>
              </div>
            )}
          </MoneyBlock>
          <MoneyRateNote />
          <ActionAlert for="checkout">{MONEY_RETRY}</ActionAlert>
        </div>
        <DK.DialogFooter className="flex flex-wrap gap-2">
          <DK.Button loading={busy} onClick={finish}><DK.LogOutIcon />{label}</DK.Button>
        </DK.DialogFooter>
      </DK.DialogContent>
    </DK.Dialog>
  );
}
```
   Keep one blank line before `// 4.6 Receive payment`.
7. The last line, `Object.assign(window, { … ME });` → replace `ME });` at its end with
   `ME, durText, paidLine, MONEY_RETRY, focusInvalid, isQuickOut, moneyOf, MoneyBlock, MoneyRateNote, OutButton });`

**Edits — `Desk.html`** (the inline script)

1. Quote:
```jsx
  if (d === 'checkout') return { kind: 'checkout', presentId: pageParams.get('pid'), debt: pageParams.get('debt') === '1' };
```
   replace with:
```jsx
  // DK-010: a fixed-price subscriber has no dialog — DeskInner checks them out on load instead.
  if (d === 'checkout') { const p = DESK.present.find((x) => x.id === pageParams.get('pid')); if (p && isQuickOut(p)) return null; return { kind: 'checkout', presentId: pageParams.get('pid'), received: pageParams.get('debt') === '1' ? '0' : pageParams.get('received') }; }
```
2. In `Detail`, quote `const v = DESK.visitCharge(p.since);` → replace with
   `const v = DESK.visitCharge(p.since, DESK.NOW, p.student);`
3. In `PresentList`, quote the line that starts `  const out = (p) => <Button variant="outline" size="sm"` (one line,
   ending `</Button>;`) → replace the whole line with `  const out = (p) => <OutButton p={p} size="sm" />;`
4. In `PresentList`'s `name` column, quote `cell: ({ row }) => row.original.kind === 'sub' ? <a className="text-label text-foreground"`
   → replace `row.original.kind === 'sub'` with `row.original.customerId` (a visit checked in as a customer links to its file).
5. In `DeskInner`, after the line `  const [tab, setTab] = React.useState(pageParams.get('tab') === 'log' ? 'log' : 'now');` insert:
```jsx
  // DK-010: ?dialog=checkout&pid=<a fixed-price subscriber> checks them out on load, as the tap does.
  React.useEffect(() => { const p = DESK.present.find((x) => x.id === pageParams.get('pid')); if (pageParams.get('dialog') === 'checkout' && p && isQuickOut(p)) setTimeout(() => desk.checkOut(p.id), 300); }, []);
```

### 3.2 Collect, record a debt, write off — K2 («استلام دفعة»), DK-012, K6, DK-003 (the card), DI-35, DK-018 (commit 2)

| Decision | On screen |
|---|---|
| K2 | `PayDialog` with the money block: due = the item's remainder (or the balance, oldest first); more is change, except a usage-based subscription chosen alone (credit); submit «تسجيل 150 ₪»; no «لم يدفع شيئًا» (there is nothing to leave) and no «more than what's left» error any more |
| DK-012 | an uncollected visit with no customer: «تحصيل» opens the pay dialog **on the visit** («تحصيل زيارة · يزن الأسطل», the line «خروج تلقائي عند الإغلاق · أمس 15:20–18:00»); «تسجيل دينًا» opens `DebtDialog` (name, mobile) |
| K6 | the owner's «⋯» › «لن يُحصَّل…» (destructive) → `ReasonDialog` (`AlertDialog`): «لن يُحصَّل مبلغ هذه الزيارة؟», the description below, «السبب» required, «رجوع», destructive «لن يُحصَّل»; the visit moves to `D.writtenOff` with the reason, who and when |
| DK-003 (card) | `UnpaidCard`: `id="unpaid"`; the title «4 زيارات غير محصّلة · 36 ₪» (O5's forms); three rows then «عرض الكل» / «عرض أقل» (`aria-expanded`); below 1280 nothing when empty |
| DI-35 | the overview's queue row links `Desk.html#unpaid` |

**New strings:**

| Arabic | English |
|---|---|
| تحصيل زيارة · {X} | Collect a visit · {X} |
| خروج تلقائي عند الإغلاق · خرج بدون دفع (kept) · اليوم · أمس | Auto check-out at closing · Left without paying · today · yesterday |
| تسجيل {9 ₪} · تسجيل الدفعة | Record {₪9} · Record payment |
| تسجيل دين · {X} | Record a debt · {X} |
| {9 ₪} تبقى دينًا على صاحب هذا الرقم، ويُنشأ له ملف زبون إن لم يكن له ملف. | {₪9} stays as a debt for the owner of this number; a customer record is created if there is none. |
| تسجيل دينًا · تسجيل الدين | Record as a debt · Record the debt |
| لن يُحصَّل… · لن يُحصَّل | Write off… · Write off |
| لن يُحصَّل مبلغ هذه الزيارة؟ | Write off this visit? |
| {X} · {28 سبتمبر} · {12 ₪}. تخرج الزيارة من «غير محصّل» ومن دين الزبون. ليست دفعة ولا حذفًا: تبقى في السجل مع السبب واسمك، ولا يمكن التراجع. | {X} · {28 Sep} · {₪12}. The visit leaves «Not collected» and the customer’s debt. It isn’t a payment or a deletion: it stays on record with the reason and your name, and it can’t be undone. |
| السبب · اكتب السبب | Reason · Write the reason |
| إجراءات أخرى لزيارة {X} (the «⋯»'s name) | More actions for the visit of {X} |
| زيارة واحدة / زيارتان / {n} زيارات / {n} زيارة غير محصّلة (F_UNCOLLECTED) | {n} visit(s) not collected |
| عرض الكل · عرض أقل | Show all · Show fewer |
| Toasts: استُلم {150 ₪} نقدًا — {X} · {اشتراك سبتمبر 150 ₪} · المتبقي {0 ₪} [· الباقي للزبون …] | {₪150} received in cash — {X} · {the September subscription ₪150} · {₪0} left [· … change] |
| (no customer) {X} · زيارة {28 سبتمبر} [· المتبقي {3 ₪} غير محصّل] | {X} · visit of {28 Sep} [· {₪3} still uncollected] |
| سُجّل {9 ₪} دينًا على {X} | {₪9} recorded as a debt for {X} |
| لن يُحصَّل {12 ₪} · {X} — السبب: … | {₪12} written off · {X} — Reason: … |

**States:** `?fail=pay`, `?fail=debt`, `?fail=writeoff` (inside each dialog); `?state=ratelimit` (pay);
`?state=loading` (the card's skeleton, kept); `?state=empty` (no rows: the card absent below 1280, «لا توجد
مبالغ غير محصّلة.» at 1280+). **Parameters (new):** `?dialog=pay&vid=<u>`, `?dialog=debt&vid=<u>`,
`?writeoff=<u>` (owner), `?unpaid=all`, `Desk.html#unpaid`.

**Edits — `masaha/desk-data.js`**

1. Replace from `  // Unpaid visits: left without paying, or checked out automatically at closing.` up to
   `  // Visits paid today (not tied to a customer): for «دفعاتي اليوم».` with:
```js
  // Unpaid visits: left without paying, or checked out automatically at closing. DK-012: a visit the
  // automatic check-out closed may have no customer, only the name it was checked in with.
  const unpaid = [
    { id: 'u1', customerId: 'm10', date: TODAY, in: '09:00', out: '11:10', amount: 9, how: 'left' },
    { id: 'u2', customerId: 'm14', date: '2026-09-28', in: '14:00', out: CLOSE, amount: 12, how: 'auto' },
    { id: 'u3', customerId: null, name: T('يزن الأسطل', 'Yazan Al-Astal'), date: '2026-09-28', in: '15:20', out: CLOSE, amount: 9, how: 'auto' },
    { id: 'u4', customerId: null, name: T('إياد الشرفا', 'Iyad Al-Sharafa'), date: '2026-09-27', in: '16:10', out: CLOSE, amount: 6, how: 'auto' }
  ];
  // K6: visits the owner wrote off («لن يُحصَّل»), with the reason, who and when — never a payment.
  const writtenOff = [];
```
2. After the line `  const findCustomer = (id) => customers.find((c) => c.id === id);` insert:
```js
  // K1: one search for the desk, the payment picker and Customers — a name, or the mobile's last digits.
  const searchCustomers = (term) => {
    const t = term.trim(); const digits = t.replace(/\D/g, '');
    const byDigits = digits.length >= 2 && digits === t.replace(/[\s+]/g, '');
    return customers.filter((c) => !c.archived && (c.name.includes(t) || (byDigits && (c.phone || '').replace(/\D/g, '').endsWith(digits))));
  };
```
3. In the `return { … }`: change `present, unpaid, visitPays,` to `present, unpaid, writtenOff, visitPays,`, and at the
   start of the line commit 1 added (`    SETTINGS, STUDENT_VISITS,`) write `    searchCustomers, SETTINGS, STUDENT_VISITS,`.

**Edits — `masaha/desk-core.jsx`**

1. After the line `const focusInvalid = …` (commit 1's) insert:
```jsx
// A day in a row's line: «اليوم», «أمس», or the date.
const dayWord = (iso) => (iso === D.TODAY ? tr('اليوم', 'today') : iso === D.addDays(D.TODAY, -1) ? tr('أمس', 'yesterday') : D.fmtDate(iso));
// O5's forms for the desk's own counted words.
const F_UNCOLLECTED = { ar: { one: 'زيارة واحدة غير محصّلة', two: 'زيارتان غير محصّلتين', few: '{n} زيارات غير محصّلة', many: '{n} زيارة غير محصّلة', other: '{n} زيارة غير محصّلة' }, en: ['{n} visit not collected', '{n} visits not collected'] };
```
2. Replace the `pay` method — from `    // Applies to one item, or to the oldest first.` up to `    saveSubscription(` — with:
```jsx
    // ADR 0010 rule 2: one payment per item, to one item or to the oldest first. A usage-based
    // subscription chosen alone takes more than it owes, as credit. K4: the toast names it all.
    pay(cid, amount, method, note, itemId, change = 0) {
      const c = D.findCustomer(cid);
      let left = amount; const parts = [];
      const items = D.openItems(c).filter((it) => !itemId || it.id === itemId);
      for (const it of items) {
        if (left <= 0) break;
        const s = it.kind === 'sub' ? c.subs.find((x) => x.id === it.id) : null;
        const take = s && s.billing.type === 'usage' && itemId ? left : Math.min(left, it.due - it.paid); left -= take;
        if (s) s.pays.push([D.TODAY, D.NOW, take, method, ME, null, note]);
        else { const u = D.unpaid.find((x) => x.id === it.id); u.amount -= take; if (u.amount <= 0) D.unpaid.splice(D.unpaid.indexOf(u), 1); D.visitPays.unshift({ id: 'vp' + Date.now() + it.id, customerId: c.id, name: c.name, date: D.TODAY, time: D.NOW, amount: take, method, by: ME }); }
        parts.push((s ? s.debtLabel || s.name : tr('زيارة ', 'Visit ') + D.fmtDate(it.date)) + ' ' + $(take));
      }
      bump(); close();
      toast.success(paidLine(amount, method), { description: c.name + ' · ' + parts.join(tr('، ', ', ')) + tr(` · المتبقي ${$(D.balance(c))}`, ` · ${$(D.balance(c))} left`) + (change > 0 ? tr(` · الباقي للزبون ${$(change)}`, ` · ${$(change)} change`) : '') });
    },
    // DK-012: a payment on an uncollected visit that has no customer.
    payVisit(uid, amount, method, note, change = 0) {
      const u = D.unpaid.find((x) => x.id === uid);
      u.amount -= amount; if (u.amount <= 0) D.unpaid.splice(D.unpaid.indexOf(u), 1);
      D.visitPays.unshift({ id: 'vp' + Date.now(), customerId: null, name: u.name, date: D.TODAY, time: D.NOW, amount, method, by: ME });
      bump(); close();
      toast.success(paidLine(amount, method), { description: u.name + tr(' · زيارة ', ' · visit of ') + D.fmtDate(u.date) + (u.amount > 0 ? tr(` · المتبقي ${$(u.amount)} غير محصّل`, ` · ${$(u.amount)} still uncollected`) : '') + (change > 0 ? tr(` · الباقي للزبون ${$(change)}`, ` · ${$(change)} change`) : '') });
    },
    // DK-012: «تسجيل دينًا» — the phone finds the customer or makes one, as at an unpaid check-out.
    attachDebt(uid, name, phone) {
      const u = D.unpaid.find((x) => x.id === uid); const ph = normPhone(phone);
      let c = D.customers.find((x) => !x.archived && x.phone === ph);
      if (!c) { c = { id: 'c' + Date.now(), name, phone: ph, subs: [] }; D.customers.unshift(c); }
      u.customerId = c.id;
      bump(); close();
      toast.success(tr(`سُجّل ${$(u.amount)} دينًا على ${c.name}`, `${$(u.amount)} recorded as a debt for ${c.name}`));
    },
    // K6: out of «غير محصّل» and the debt, kept with the reason, who and when.
    writeOff(uid, reason) {
      const u = D.unpaid.find((x) => x.id === uid); const who = u.customerId ? D.findCustomer(u.customerId).name : u.name;
      D.unpaid.splice(D.unpaid.indexOf(u), 1); D.writtenOff.push({ ...u, reason, by: ME, on: D.TODAY });
      bump(); close();
      toast.success(tr(`لن يُحصَّل ${$(u.amount)} · ${who}`, `${$(u.amount)} written off · ${who}`), { description: tr('السبب: ', 'Reason: ') + reason });
    },
```
3. After the provider's line `      <PayDialog dlg={dlg && dlg.kind === 'pay' ? dlg : null} onClose={close} />` insert:
```jsx
      <DebtDialog dlg={dlg && dlg.kind === 'debt' ? dlg : null} onClose={close} />
      <WriteOffDialog dlg={dlg && dlg.kind === 'writeoff' ? dlg : null} onClose={close} />
```
4. Replace from `// 4.6 Receive payment` up to `Object.assign(window,` (the whole old `PayDialog`) with these two blocks, one after the other:
```jsx
// 4.6 Receive payment: a customer's open items, oldest first or one of them; or, from the uncollected
// list, one visit that has no customer (DK-012). The money block names what is recorded.
function PayDialog({ dlg, onClose }) {
  const desk = useDesk();
  const [cid, setCid] = React.useState(null); const [q, setQ] = React.useState('');
  const [item, setItem] = React.useState('auto'); const [amount, setAmount] = React.useState(''); const [method, setMethod] = React.useState('cash'); const [note, setNote] = React.useState(''); const [err, setErr] = React.useState();
  const v = dlg && dlg.visitId ? D.unpaid.find((x) => x.id === dlg.visitId) : null;
  const c = cid && D.findCustomer(cid);
  const items = c ? D.openItems(c) : [];
  const leftOf = (id) => { if (id === 'auto') return D.balance(c); const it = items.find((i) => i.id === id); return it ? it.due - it.paid : 0; };
  const chosen = c && item !== 'auto' ? c.subs.find((x) => x.id === item) : null;
  // A usage-based subscription takes more than it owes, as credit (ADR 0010 rule 4).
  const open = !!chosen && chosen.billing.type === 'usage';
  const due = v ? v.amount : c ? leftOf(item) : 0;
  React.useEffect(() => { if (dlg) { setCid(dlg.customerId || null); setQ(''); setItem(dlg.itemId || 'auto'); setMethod('cash'); setNote(''); setErr(); } }, [dlg]);
  React.useEffect(() => { if (v) setAmount(String(v.amount)); else if (c) setAmount(String(leftOf(item) || '')); }, [dlg, cid, item]);
  const term = q.trim();
  const results = term ? D.searchCustomers(term).slice(0, 6) : D.customers.filter((x) => !x.archived && D.balance(x) > 0).slice(0, 6);
  const m = moneyOf(due, amount, open);
  const { busy, run } = useActionRun('pay');
  const submit = (e) => {
    e.preventDefault();
    if (!(m.recorded > 0)) { setErr(tr('أدخل مبلغًا أكبر من صفر', 'Enter an amount above zero')); return focusInvalid(); }
    setErr();
    run(() => (v ? desk.payVisit(v.id, m.recorded, method, note, m.change) : desk.pay(c.id, m.recorded, method, note, item === 'auto' ? null : item, m.change)));
  };
  const how = (u) => <>{u.how === 'auto' ? tr('خروج تلقائي عند الإغلاق', 'Auto check-out at closing') : tr('خرج بدون دفع', 'Left without paying')} · {dayWord(u.date)} <Num>{u.in + '–' + u.out}</Num></>;
  const submitLabel = m.recorded > 0 ? <>{tr('تسجيل', 'Record')} <Money n={m.recorded} /></> : tr('تسجيل الدفعة', 'Record payment');
  const tail = (
    <>
      <DK.Field label={tr('ملاحظة', 'Note')} labelEnd={<span className="text-caption text-muted-foreground">{tr('اختياري', 'Optional')}</span>}><DK.Input value={note} onChange={(e) => setNote(e.target.value)} /></DK.Field>
      <MoneyRateNote />
      <ActionAlert for="pay">{MONEY_RETRY}</ActionAlert>
    </>
  );
  return (
    <DK.Dialog open={!!dlg} onOpenChange={(o) => !o && onClose()}>
      <DK.DialogContent closeLabel={tr('إغلاق', 'Close')}>
        <DK.DialogHeader>
          <DK.DialogTitle>{v ? tr('تحصيل زيارة', 'Collect a visit') + ' · ' + v.name : tr('استلام دفعة', 'Receive a payment') + (c ? ' · ' + c.name : '')}</DK.DialogTitle>
          <DK.DialogDescription>{v ? how(v) : c ? <>{tr('المتبقي عليه', 'Balance')} <Money n={D.balance(c)} /></> : tr('اختر الزبون', 'Choose the customer')}</DK.DialogDescription>
        </DK.DialogHeader>
        {v ? (
          <form onSubmit={submit} noValidate className="flex flex-col gap-4">
            <MoneyBlock due={due} value={amount} onValue={setAmount} method={method} onMethod={setMethod} error={err} remainder="uncollected" none={false} />
            {tail}
            <DK.DialogFooter className="flex flex-wrap gap-2"><DK.Button type="submit" loading={busy}>{submitLabel}</DK.Button></DK.DialogFooter>
          </form>
        ) : !c ? (
          <div className="flex flex-col gap-3">
            <DK.Input role="searchbox" aria-label={tr('ابحث بالاسم أو آخر أرقام الجوال', 'Search by name or last digits')} placeholder={tr('الاسم أو آخر أرقام الجوال', 'Name or last digits of the mobile')} startIcon={<DK.SearchIcon />} value={q} onChange={(e) => setQ(e.target.value)} autoFocus />
            {!term && <p className="text-caption text-muted-foreground">{tr('عليهم مبالغ:', 'Customers who owe:')}</p>}
            <ul className="flex flex-col divide-y rounded-lg border border-border">
              {results.length ? results.map((x) => (
                <li key={x.id} className="flex items-center justify-between gap-3 px-3 py-2">
                  <span className="flex min-w-0 flex-col"><span className="text-label">{x.name}</span><span dir="ltr" className="self-start text-caption text-muted-foreground">{x.phone}</span></span>
                  <span className="flex items-center gap-2"><BalanceBadge c={x} /><DK.Button size="sm" variant="outline" onClick={() => setCid(x.id)}>{tr('اختيار', 'Choose')}</DK.Button></span>
                </li>
              )) : <li className="px-3 py-3 text-body-sm text-muted-foreground">{tr('لا يوجد زبون بهذا الاسم أو الرقم.', 'No customer with this name or number.')}</li>}
            </ul>
          </div>
        ) : items.length === 0 ? (
          <p className="text-body">{tr('لا يوجد مبلغ مستحق على هذا الزبون.', 'This customer owes nothing.')}</p>
        ) : (
          <form onSubmit={submit} noValidate className="flex flex-col gap-4">
            <DK.Field label={tr('تُطبَّق الدفعة على', 'Apply the payment to')}>
              <DK.RadioGroup value={item} onValueChange={setItem}>
                <DK.Field label={tr('الأقدم أولًا', 'Oldest first')} orientation="horizontal"><DK.RadioGroupItem value="auto" /></DK.Field>
                {items.map((it) => (
                  <DK.Field key={it.id} orientation="horizontal" label={<span className="flex flex-col"><span>{it.label}</span><span className="text-caption text-muted-foreground">{tr('المستحق', 'Due')} <Money n={it.due} /> · {tr('المدفوع', 'Paid')} <Money n={it.paid} /> · {tr('المتبقي', 'Left')} <Money n={it.due - it.paid} /></span></span>}><DK.RadioGroupItem value={it.id} /></DK.Field>
                ))}
              </DK.RadioGroup>
            </DK.Field>
            <MoneyBlock due={due} open={open} value={amount} onValue={setAmount} method={method} onMethod={setMethod} error={err} remainder="debt" who={c.name} none={false} />
            {tail}
            <DK.DialogFooter className="flex flex-wrap gap-2">
              <DK.Button type="submit" loading={busy}>{submitLabel}</DK.Button>
              {!dlg.customerId && <DK.Button type="button" variant="ghost" onClick={() => setCid(null)}>{tr('زبون آخر', 'Another customer')}</DK.Button>}
            </DK.DialogFooter>
          </form>
        )}
      </DK.DialogContent>
    </DK.Dialog>
  );
}

// P9: an irreversible act felt by others asks with an AlertDialog whose reason is required — voiding
// a payment, and K6's write-off. The action repeats the verb, `destructive`; the dismiss is «رجوع».
function ReasonDialog({ open, onClose, title, description, action, actionKey, onConfirm }) {
  const [reason, setReason] = React.useState(''); const [err, setErr] = React.useState();
  React.useEffect(() => { if (open) { setReason(''); setErr(); } }, [open]);
  const { busy, run } = useActionRun(actionKey);
  const go = () => { if (!reason.trim()) { setErr(tr('اكتب السبب', 'Write the reason')); return focusInvalid(); } run(() => onConfirm(reason.trim())); };
  return (
    <DK.AlertDialog open={!!open} onOpenChange={(o) => !o && onClose()}>
      <DK.AlertDialogContent>
        <DK.AlertDialogHeader>
          <DK.AlertDialogTitle>{title}</DK.AlertDialogTitle>
          <DK.AlertDialogDescription>{description}</DK.AlertDialogDescription>
        </DK.AlertDialogHeader>
        <DK.Field label={tr('السبب', 'Reason')} error={err}><DK.Textarea rows={2} value={reason} onChange={(e) => setReason(e.target.value)} /></DK.Field>
        <ActionAlert for={actionKey} />
        <DK.AlertDialogFooter>
          <DK.AlertDialogCancel>{tr('رجوع', 'Back')}</DK.AlertDialogCancel>
          <DK.Button variant="destructive" loading={busy} onClick={go}>{action}</DK.Button>
        </DK.AlertDialogFooter>
      </DK.AlertDialogContent>
    </DK.AlertDialog>
  );
}

// K6: the owner's «لن يُحصَّل» — with a reason, recorded and audited; never a payment, never a deletion.
function WriteOffDialog({ dlg, onClose }) {
  const desk = useDesk();
  const u = dlg && D.unpaid.find((x) => x.id === dlg.visitId);
  const who = u ? (u.customerId ? D.findCustomer(u.customerId).name : u.name) : '';
  return (
    <ReasonDialog open={!!u} onClose={onClose} actionKey="writeoff" title={tr('لن يُحصَّل مبلغ هذه الزيارة؟', 'Write off this visit?')} action={tr('لن يُحصَّل', 'Write off')} onConfirm={(reason) => desk.writeOff(u.id, reason)}
      description={u && <>{who} · {D.fmtDate(u.date)} · <Money n={u.amount} />. {tr('تخرج الزيارة من «غير محصّل» ومن دين الزبون. ليست دفعة ولا حذفًا: تبقى في السجل مع السبب واسمك، ولا يمكن التراجع.', 'The visit leaves «Not collected» and the customer’s debt. It isn’t a payment or a deletion: it stays on record with the reason and your name, and it can’t be undone.')}</>} />
  );
}

// DK-012: a visit with no customer (the automatic check-out closed it) becomes a debt by a name and a
// phone, which find the customer or make one — the rule of an unpaid check-out.
function DebtDialog({ dlg, onClose }) {
  const desk = useDesk();
  const u = dlg && D.unpaid.find((x) => x.id === dlg.visitId);
  const [name, setName] = React.useState(''); const [phone, setPhone] = React.useState(''); const [err, setErr] = React.useState({});
  React.useEffect(() => { if (u) { setName(u.name || ''); setPhone(''); setErr({}); } }, [dlg]);
  const { busy, run } = useActionRun('debt');
  const match = phoneOk(phone) ? D.customers.find((x) => !x.archived && x.phone === normPhone(phone)) : null;
  const submit = (e) => {
    e.preventDefault();
    const x = {};
    if (!name.trim()) x.name = tr('أدخل الاسم', 'Enter the name');
    if (!phoneOk(phone)) x.phone = tr('رقم الجوال مطلوب ليُسجَّل المبلغ دينًا، مثل +970 59 000 0000', 'A mobile number is needed to record the debt, e.g. +970 59 000 0000');
    setErr(x); if (Object.keys(x).length) return focusInvalid();
    run(() => desk.attachDebt(u.id, name.trim(), phone));
  };
  return (
    <DK.Dialog open={!!u} onOpenChange={(o) => !o && onClose()}>
      <DK.DialogContent closeLabel={tr('إغلاق', 'Close')}>
        {u && <>
          <DK.DialogHeader>
            <DK.DialogTitle>{tr('تسجيل دين', 'Record a debt')} · {u.name}</DK.DialogTitle>
            <DK.DialogDescription><Money n={u.amount} /> {tr('تبقى دينًا على صاحب هذا الرقم، ويُنشأ له ملف زبون إن لم يكن له ملف.', 'stays as a debt for the owner of this number; a customer record is created if there is none.')}</DK.DialogDescription>
          </DK.DialogHeader>
          <form onSubmit={submit} noValidate className="flex flex-col gap-4">
            <DK.Field label={tr('الاسم', 'Name')} error={err.name}><DK.Input value={name} onChange={(e) => setName(e.target.value)} /></DK.Field>
            <DK.Field label={tr('رقم الجوال', 'Mobile number')} error={err.phone} helper={match ? tr('يُضاف إلى ملف ', 'Added to the file of ') + match.name : undefined}><DK.Input type="tel" dir="ltr" placeholder="+970 59 000 0000" value={phone} onChange={(e) => setPhone(e.target.value)} autoFocus /></DK.Field>
            <ActionAlert for="debt" />
            <DK.DialogFooter><DK.Button type="submit" loading={busy}>{tr('تسجيل الدين', 'Record the debt')}</DK.Button></DK.DialogFooter>
          </form>
        </>}
      </DK.DialogContent>
    </DK.Dialog>
  );
}

// An uncollected visit's row: on the desk with its name, its actions under it (the side column is
// narrow); in the customer's file without, on one line from 768. Its actions:
// «تحصيل», «تسجيل دينًا» when it has no customer (DK-012), and the owner's «لن يُحصَّل» (K6).
function UnpaidRow({ u, showName }) {
  const desk = useDesk();
  const c = u.customerId ? D.findCustomer(u.customerId) : null;
  const who = c ? c.name : u.name;
  const how = u.how === 'auto' ? tr('خروج تلقائي عند الإغلاق', 'Auto check-out at closing') : tr('خرج بدون دفع', 'Left without paying');
  return (
    <li className={'flex flex-col gap-2 px-5 py-3' + (showName ? '' : ' md:flex-row md:items-center md:justify-between')}>
      <div className="flex min-w-0 flex-col">
        {showName && (c ? <a className="text-label text-foreground" href={roleQ('Customer file.html?id=' + c.id)}>{who}</a> : <span className="text-label">{who}</span>)}
        <span className={showName ? 'text-caption text-muted-foreground' : 'text-body-sm'}>{how} · {dayWord(u.date)} <Num>{u.in + '–' + u.out}</Num></span>
      </div>
      <div className="flex flex-wrap items-center gap-2">
        <span className="text-label"><Money n={u.amount} /></span>
        <DK.Button size="sm" variant="outline" onClick={() => (c ? desk.open('pay', { customerId: c.id, itemId: u.id }) : desk.open('pay', { visitId: u.id }))}>{tr('تحصيل', 'Collect')}</DK.Button>
        {!c && <DK.Button size="sm" variant="outline" onClick={() => desk.open('debt', { visitId: u.id })}>{tr('تسجيل دينًا', 'Record as a debt')}</DK.Button>}
        {IS_OWNER && (
          <DK.DropdownMenu dir={DIR}>
            <DK.DropdownMenuTrigger asChild><DK.Button variant="ghost" size="icon" aria-label={tr('إجراءات أخرى لزيارة ', 'More actions for the visit of ') + who}><DK.EllipsisVerticalIcon /></DK.Button></DK.DropdownMenuTrigger>
            <DK.DropdownMenuContent align="end"><DK.DropdownMenuItem variant="destructive" onSelect={() => desk.open('writeoff', { visitId: u.id })}>{tr('لن يُحصَّل…', 'Write off…')}</DK.DropdownMenuItem></DK.DropdownMenuContent>
          </DK.DropdownMenu>
        )}
      </div>
    </li>
  );
}

```
5. In the last line, after `OutButton` add `, dayWord, F_UNCOLLECTED, ReasonDialog, UnpaidRow`.

**Edits — `Desk.html`**

1. Replace from `function UnpaidCard() {` up to `const LOG = () =>` with the block below, **then, in it, change
   `'section-anchor desk-unpaid'` to `'section-anchor'`** (commit 4 adds `desk-unpaid` together with its CSS
   rule; a class with no rule fails `check-classes.mjs`):
```jsx
// DK-003: the money to chase, compact — its count and total in the title, the first three rows and
// «عرض الكل». DI-35: `#unpaid` is where the overview's queue lands. Below xl nothing shows when it is empty.
const UNPAID_SHOWN = 3;
function UnpaidCard() {
  const [all, setAll] = React.useState(pageParams.get('unpaid') === 'all');
  const list = DESK.unpaid;
  const total = list.reduce((a, u) => a + u.amount, 0);
  const shown = all ? list : list.slice(0, UNPAID_SHOWN);
  return (
    <Card id="unpaid" className={'section-anchor desk-unpaid' + (list.length || st === 'loading' ? '' : ' hidden xl:flex')}>
      <CardHeader>
        <CardTitle><h2>{list.length ? <><Counted n={list.length} ar={F_UNCOLLECTED.ar} en={F_UNCOLLECTED.en} /> · <Money n={total} /></> : tr('غير محصّل', 'Not collected')}</h2></CardTitle>
        <CardDescription>{tr('زيارات خرجت بدون دفع أو سُجّل خروجها تلقائيًا عند الإغلاق.', 'Visits that left unpaid or were checked out automatically at closing.')}</CardDescription>
      </CardHeader>
      <CardContent className="p-0">
        {st === 'loading' ? <div className="flex flex-col gap-3 px-5 pb-5"><Skeleton className="h-10 w-full" /><Skeleton className="h-10 w-full" /></div>
        : list.length ? <>
          <ul className="divide-y">{shown.map((u) => <UnpaidRow key={u.id} u={u} showName />)}</ul>
          {list.length > UNPAID_SHOWN && <div className="border-t px-5 py-3"><Button variant="link" size="sm" className="px-0" aria-expanded={all} onClick={() => setAll(!all)}>{all ? tr('عرض أقل', 'Show fewer') : tr('عرض الكل', 'Show all')}</Button></div>}
        </> : <p className="flex items-center gap-2 px-5 pb-5 text-body-sm text-muted-foreground"><CircleCheckIcon className="size-4" aria-hidden="true" />{tr('لا توجد مبالغ غير محصّلة.', 'Nothing left to collect.')}</p>}
      </CardContent>
    </Card>
  );
}

```
2. Quote:
```jsx
  if (d === 'pay') return { kind: 'pay', customerId: cid, itemId: pageParams.get('item') };
```
   replace with:
```jsx
  if (d === 'pay') return { kind: 'pay', customerId: cid, itemId: pageParams.get('item'), visitId: pageParams.get('vid') };
  if (d === 'debt') return { kind: 'debt', visitId: pageParams.get('vid') };
  if (pageParams.get('writeoff') && IS_OWNER) return { kind: 'writeoff', visitId: pageParams.get('writeoff') };
```

**Edit — `Owner overview.html`** (batch 5's file; DI-35's one line). In `queueRows()`, quote
`action: tr('فتح المكتب', 'Open the desk'), href: 'Desk.html' });` → replace `href: 'Desk.html'` with
`href: 'Desk.html#unpaid'`. Nothing else in the file changes.

### 3.3 The sheet in one step, the debt first — K3, DK-005, DK-006, DK-007, DK-008, DK-018 (commit 3)

| Decision | On screen |
|---|---|
| DK-006 | no steps; a new customer: «الاسم», «رقم الجوال» (its «اختياري» only while nothing stays unpaid), then the rest; an existing customer without a mobile gets the mobile field too; the error «رقم الجوال مطلوب: يبقى 250 ₪ دينًا، مثل +970 59 000 0000» moves focus to it |
| K3 / DK-005 | a renewal: the warning «مستحق من قبل 150 ₪ · اشتراك سبتمبر» — «يُطبَّق المستلم عليه أولًا، ثم على التجديد.» — no button; the block's lines per old item and «التجديد: شهري طلاب 250 ₪», «المجموع 400 ₪»; the money applied oldest first, one payment per item, the rest to the renewal |
| DK-007 | renewal: «الباقة» as one line «شهري طلاب · 250 ₪ · 1 أكتوبر – 30 أكتوبر» and the link «تغيير الباقة»; new: each package one line, its name and price, its terms under, «مخصّص» last |
| DK-008 | custom with no «إلى»: «بلا تاريخ نهاية · ينتهي عند استهلاك 20 ساعة» (hours, days, or both «… أو 10 أيام، أيهما أسبق»), or «بلا حدّ · يبقى نشطًا حتى يُنهى» with `TriangleAlertIcon` (`text-warning`); the subscription is saved with `to: null` |
| K2 | the money block; submit «حفظ واستلام 300 ₪» / «تجديد واستلام 400 ₪»; at 0 «حفظ بدون دفع» / «تجديد بدون دفع» |
| DK-018 | `?fail=sheet` — the Alert inside; `?fail=sheet-pay` — submitted, the subscription is saved and the payment fails: the sheet stays with «حُفظ الاشتراك؛ لم تُسجَّل الدفعة 90 ₪», «لن يُحفظ الاشتراك مرة ثانية. أعد محاولة الدفعة وحدها، أو أغلق ويبقى المبلغ دينًا.», the method, and «إعادة المحاولة: تسجيل 90 ₪»; `&half=1` shows that state on open, for the board |

**New strings:**

| Arabic | English |
|---|---|
| الاسم والجوال، ثم الاشتراك والدفع. (the new customer's sheet description) | The name and mobile, then the subscription and the payment. |
| مستحق من قبل {150 ₪} · {اشتراك سبتمبر} | Owed from before: {₪150} · {the September subscription} |
| يُطبَّق المستلم عليه أولًا، ثم على التجديد. | What you receive pays it first, then the renewal. |
| التجديد: {name} — يُحسب من الحضور | The renewal: {name} — billed from attendance |
| المجموع | Total |
| تغيير الباقة | Change package |
| بلا تاريخ نهاية · ينتهي عند استهلاك {20 ساعة} [أو {10 أيام}، أيهما أسبق] | No end date · ends when {20 hours} [or {10 days}] are used[, whichever comes first] |
| بلا حدّ · يبقى نشطًا حتى يُنهى | No limit · stays active until it is ended |
| رقم الجوال مطلوب: يبقى {250 ₪} دينًا، مثل +970 59 000 0000 | A mobile number is required: {₪250} stays owed, e.g. +970 59 000 0000 |
| رقم الجوال مطلوب لاشتراك يُحسب من الحضور، مثل +970 59 000 0000 | A mobile number is required for a subscription billed from attendance, e.g. +970 59 000 0000 |
| حفظ واستلام {300 ₪} · تجديد واستلام {400 ₪} · حفظ بدون دفع · تجديد بدون دفع | Save and take {₪300} · Renew and take {₪400} · Save without payment · Renew without payment |
| حُفظ الاشتراك؛ لم تُسجَّل الدفعة {90 ₪} | The subscription was saved; the payment was not recorded: {₪90} |
| لن يُحفظ الاشتراك مرة ثانية. أعد محاولة الدفعة وحدها، أو أغلق ويبقى المبلغ دينًا. | The subscription won’t be saved twice. Retry the payment alone, or close and the amount stays owed. |
| إعادة المحاولة: تسجيل {90 ₪} | Try again: record {₪90} |
| Toasts: جُدّد اشتراك {X} / حُفظ الاشتراك · {X} — {sub} · استُلم {400 ₪} نقدًا: {اشتراك سبتمبر 150 ₪، شهري طلاب 250 ₪} [· المتبقي {…} دين] ; بدون دفع | {X}’s subscription renewed / Subscription saved · {X} — {sub} · {₪400} received in cash: {…} [· {…} owed] ; No payment |

Removed: «الخطوة 1 من 2», «التالي», «السابق», «دفعة الآن», «يمكن أن تكون دفعة جزئية.», «يمكنك التجديد
الآن واستلام المبلغ لاحقًا.» and the Alert's «استلام دفعة».

**Edits — `masaha/desk-sheet.jsx`: replace the whole file** with:
```jsx
// 4.5 New customer / new subscription / renewal — one step (DK-006): the customer, the package, the
// dates and the money block (K2). A renewal with a debt takes the old balance first (K3).
const DS5 = window.MasahaDesignSystem;
const D5 = window.DESK;

// DK-007: a package is one line — its name and price, its terms as a caption.
function PkgOption({ value, title, amount, terms, tag }) {
  return (
    <DS5.Field orientation="horizontal" className="px-3 py-2" label={
      <span className="flex min-w-0 flex-col">
        <span className="flex flex-wrap items-center gap-2 text-label">{title}{amount != null && <span>· <Money n={amount} /></span>}{tag}</span>
        <span className="text-caption text-muted-foreground">{terms}</span>
      </span>
    }><DS5.RadioGroupItem value={value} /></DS5.Field>
  );
}
const Opt = () => <span className="text-caption text-muted-foreground">{tr('اختياري', 'Optional')}</span>;
const NumIn = ({ label, value, onChange, error }) => <DS5.Field label={label} labelEnd={<Opt />} error={error}><DS5.Input inputMode="numeric" dir="ltr" value={value} onChange={(e) => onChange(e.target.value.replace(/[^\d]/g, ''))} /></DS5.Field>;
// DK-008's counted words, after «استهلاك».
const F_HOURS_GEN = { ar: { one: 'ساعة واحدة', two: 'ساعتين', few: '{n} ساعات', many: '{n} ساعة', other: '{n} ساعة' }, en: ['{n} hour', '{n} hours'] };
const F_DAYS_GEN = { ar: { one: 'يوم واحد', two: 'يومين', few: '{n} أيام', many: '{n} يومًا', other: '{n} يوم' }, en: ['{n} day', '{n} days'] };

function SubscriptionSheet({ dlg, onClose }) {
  const desk = useDesk();
  const c = dlg && dlg.customerId ? D5.findCustomer(dlg.customerId) : null;
  const cur = c && D5.currentSub(c);
  const renew = !!dlg && dlg.mode === 'renew';
  const [name, setName] = React.useState(''); const [phone, setPhone] = React.useState('');
  const [pk, setPk] = React.useState('month'); const [start, setStart] = React.useState(D5.TODAY);
  const [showPk, setShowPk] = React.useState(true);
  const [priceEdit, setPriceEdit] = React.useState(false); const [price, setPrice] = React.useState('');
  const [cu, setCu] = React.useState({});
  // null: «المستلم الآن» follows what is due; typing takes it over.
  const [received, setReceived] = React.useState(null); const [method, setMethod] = React.useState('cash');
  const [err, setErr] = React.useState({});
  // DK-018: the subscription saved and its payment not — the sheet stays, to retry the payment alone.
  const [half, setHalf] = React.useState(null);
  const saveRef = React.useRef(null);
  const { busy, run } = useActionRun('sheet');
  const payRun = useActionRun('sheet-pay');
  React.useEffect(() => {
    if (!dlg) return;
    setName(c ? c.name : dlg.name || ''); setPhone(c ? c.phone || '' : dlg.phone || '');
    const startPk = renew && cur ? cur.pkg : dlg.pkg || 'month';
    setPk(startPk); setShowPk(!(renew && cur && cur.pkg !== 'custom'));
    setStart(renew && cur && cur.to && D5.subStatus(cur) !== 'expired' ? D5.addDays(cur.to, 1) : D5.TODAY);
    setPriceEdit(false); setPrice(''); setMethod('cash'); setErr({}); setHalf(null);
    setReceived(dlg.payNow ? String(dlg.payNow) : null);
    setCu(dlg.custom || { to: '', totalDays: '', daysPerWeek: '', hoursPerDay: '', hourBalance: '', billing: 'fixed', amount: '', unit: 'hour', rate: String(D5.PRICES.hour), shift: '', title: '', note: '' });
  }, [dlg]);
  // ?half=1: the frame of a payment that failed after the save (with ?fail=sheet-pay).
  React.useEffect(() => { if (!dlg || !dlg.half) return undefined; const t = setTimeout(() => saveRef.current && saveRef.current(true), 50); return () => clearTimeout(t); }, [dlg]);
  if (!dlg) return <DS5.Sheet open={false}><DS5.SheetContent closeLabel="" /></DS5.Sheet>;

  const P = D5.pkg(pk); const custom = pk === 'custom';
  const setC = (x) => setCu((y) => ({ ...y, ...x }));
  const publishedRate = cu.unit === 'hour' ? D5.PRICES.hour : D5.PRICES.day;
  const manual = custom ? (cu.billing === 'fixed' ? cu.amount !== '' : Number(cu.rate) !== publishedRate) : priceEdit && price !== '' && Number(price) !== P.amount;
  const usage = custom && cu.billing === 'usage';
  const newDue = usage ? 0 : custom ? Number(cu.amount) || 0 : priceEdit && price !== '' ? Number(price) : P.amount;
  // DK-008: a custom subscription keeps no end it was not given.
  const end = custom ? cu.to || null : D5.addDays(start, P.days - 1);
  // K3: a renewal takes what is owed from before first — every open item, oldest first.
  const prior = renew && c ? D5.openItems(c) : [];
  const priorTotal = prior.reduce((a, i) => a + i.due - i.paid, 0);
  const due = priorTotal + newDue;
  const value = received == null ? String(due) : received;
  const m = moneyOf(due, value, usage);
  const askName = !c; const askPhone = !c || !c.phone;
  const unpaidAfter = usage || m.left > 0;
  const itemLabel = (i) => { if (i.kind === 'visit') return tr('زيارة ', 'Visit ') + D5.fmtDate(i.date); const s = c.subs.find((x) => x.id === i.id); return s.debtLabel || s.name; };
  const subName = custom ? cu.title.trim() || tr('مخصّص', 'Custom') : P.name;

  const saveNow = (failPay) => {
    const n = (v) => (v === '' || v == null ? undefined : Number(v));
    const sub = custom
      ? { id: 's' + Date.now(), pkg: 'custom', name: subName, from: start, to: end, terms: { totalDays: n(cu.totalDays), daysPerWeek: n(cu.daysPerWeek), hoursPerDay: n(cu.hoursPerDay), hourBalance: n(cu.hourBalance) }, used: {}, billing: usage ? { type: 'usage', unit: cu.unit, rate: Number(cu.rate) } : { type: 'fixed', amount: newDue }, manual, shift: cu.shift || null, note: cu.note, pays: [] }
      : { id: 's' + Date.now(), pkg: pk, name: P.name, from: start, to: end, terms: { totalDays: P.totalDays, daysPerWeek: P.daysPerWeek, hourBalance: P.hourBalance }, used: {}, billing: { type: 'fixed', amount: newDue }, manual, pays: [] };
    const saved = desk.saveSubscription({ customerId: c && c.id, name: name.trim(), phone }, sub, failPay ? null : { recorded: m.recorded, method, renew });
    if (failPay) setHalf({ customerId: saved.id, amount: m.recorded });
  };
  saveRef.current = saveNow;
  const submit = (e) => {
    e.preventDefault();
    const x = {};
    if (askName && !name.trim()) x.name = tr('أدخل الاسم', 'Enter the name');
    if (askPhone && phone && !phoneOk(phone)) x.phone = tr('رقم غير مكتمل، مثل +970 59 000 0000', 'Incomplete number, e.g. +970 59 000 0000');
    else if (askPhone && unpaidAfter && !phoneOk(phone)) x.phone = usage
      ? tr('رقم الجوال مطلوب لاشتراك يُحسب من الحضور، مثل +970 59 000 0000', 'A mobile number is required for a subscription billed from attendance, e.g. +970 59 000 0000')
      : tr(`رقم الجوال مطلوب: يبقى ${D5.money(m.left)} دينًا، مثل +970 59 000 0000`, `A mobile number is required: ${D5.money(m.left)} stays owed, e.g. +970 59 000 0000`);
    if (custom && cu.billing === 'fixed' && !(Number(cu.amount) > 0)) x.amount = tr('أدخل السعر', 'Enter the price');
    if (custom && cu.to && cu.to < start) x.to = tr('تاريخ النهاية قبل البداية', 'The end is before the start');
    setErr(x); if (Object.keys(x).length) return focusInvalid();
    run(() => saveNow(actionFails('sheet-pay') && m.recorded > 0));
  };

  const hb = Number(cu.hourBalance) || 0; const td = Number(cu.totalDays) || 0;
  const endNote = !custom || cu.to ? null : hb || td ? (
    <p className="text-caption text-muted-foreground">
      {tr('بلا تاريخ نهاية · ينتهي عند استهلاك ', 'No end date · ends when ')}
      {hb ? <Counted n={hb} ar={F_HOURS_GEN.ar} en={F_HOURS_GEN.en} /> : null}{hb && td ? tr(' أو ', ' or ') : null}{td ? <Counted n={td} ar={F_DAYS_GEN.ar} en={F_DAYS_GEN.en} /> : null}
      {tr('', ' are used')}{hb && td ? tr('، أيهما أسبق', ', whichever comes first') : null}
    </p>
  ) : (
    <p className="flex items-center gap-2 text-caption text-muted-foreground"><DS5.TriangleAlertIcon className="size-4 text-warning" aria-hidden="true" />{tr('بلا حدّ · يبقى نشطًا حتى يُنهى', 'No limit · stays active until it is ended')}</p>
  );
  const calc = prior.length ? <>
    {prior.map((i) => <span key={i.id}>{itemLabel(i)} <Money n={i.due - i.paid} /></span>)}
    <span>{tr('التجديد: ', 'The renewal: ')}{subName} {usage ? tr('— يُحسب من الحضور', '— billed from attendance') : <Money n={newDue} />}</span>
  </> : usage ? <span>{tr('يُحسب من الحضور:', 'Billed from attendance:')} <Money n={Number(cu.rate) || 0} /> {cu.unit === 'hour' ? tr('للساعة', 'per hour') : tr('لليوم', 'per day')}</span> : null;
  const submitLabel = m.recorded > 0
    ? <>{renew ? tr('تجديد واستلام', 'Renew and take') : tr('حفظ واستلام', 'Save and take')} <Money n={m.recorded} /></>
    : renew ? tr('تجديد بدون دفع', 'Renew without payment') : tr('حفظ بدون دفع', 'Save without payment');
  const title = renew ? tr('تجديد الاشتراك', 'Renew subscription') : c ? tr('اشتراك جديد', 'New subscription') : tr('زبون جديد', 'New customer');

  return (
    <DS5.Sheet open onOpenChange={(o) => !o && onClose()}>
      <DS5.SheetContent side="end" closeLabel={tr('إغلاق', 'Close')}>
        <DS5.SheetHeader>
          <DS5.SheetTitle>{title}</DS5.SheetTitle>
          <DS5.SheetDescription>{c ? c.name : tr('الاسم والجوال، ثم الاشتراك والدفع.', 'The name and mobile, then the subscription and the payment.')}</DS5.SheetDescription>
        </DS5.SheetHeader>
        <form onSubmit={submit} noValidate className="flex min-h-0 flex-1 flex-col">
          <DS5.SheetBody className="flex flex-col gap-5 py-2">
            {half ? <>
              <DS5.Alert variant="destructive">
                <DS5.AlertTitle>{tr('حُفظ الاشتراك؛ لم تُسجَّل الدفعة', 'The subscription was saved; the payment was not recorded:')} <Money n={half.amount} /></DS5.AlertTitle>
                <DS5.AlertDescription>{tr('لن يُحفظ الاشتراك مرة ثانية. أعد محاولة الدفعة وحدها، أو أغلق ويبقى المبلغ دينًا.', 'The subscription won’t be saved twice. Retry the payment alone, or close and the amount stays owed.')}</DS5.AlertDescription>
              </DS5.Alert>
              <MethodToggle value={method} onChange={setMethod} />
            </> : <>
              {askName && <DS5.Field label={tr('الاسم', 'Name')} error={err.name}><DS5.Input value={name} onChange={(e) => setName(e.target.value)} autoFocus /></DS5.Field>}
              {askPhone && (
                <DS5.Field label={tr('رقم الجوال', 'Mobile number')} labelEnd={unpaidAfter ? undefined : <Opt />} error={err.phone}>
                  <DS5.Input type="tel" dir="ltr" placeholder="+970 59 000 0000" value={phone} onChange={(e) => setPhone(e.target.value)} />
                </DS5.Field>
              )}
              {prior.length > 0 && (
                <DS5.Alert variant="warning">
                  <DS5.AlertTitle>{tr('مستحق من قبل', 'Owed from before:')} <Money n={priorTotal} /> · {prior.map(itemLabel).join(tr('، ', ', '))}</DS5.AlertTitle>
                  <DS5.AlertDescription>{tr('يُطبَّق المستلم عليه أولًا، ثم على التجديد.', 'What you receive pays it first, then the renewal.')}</DS5.AlertDescription>
                </DS5.Alert>
              )}
              {showPk ? (
                <DS5.Field label={tr('الباقة', 'Package')}>
                  <DS5.RadioGroup value={pk} onValueChange={(v) => { setPk(v); setPriceEdit(false); setPrice(''); setReceived(null); }}>
                    <p className="text-caption text-muted-foreground">{tr('منشورة للزوار', 'Published')}</p>
                    <div className="flex flex-col divide-y rounded-lg border border-border">
                      {D5.PACKAGES.filter((p) => p.isPublic).map((p) => <PkgOption key={p.id} value={p.id} title={p.name} amount={p.amount} terms={p.terms} />)}
                    </div>
                    <p className="pt-2 text-caption text-muted-foreground">{tr('خاصة بالمكتب — لا تظهر للزوار', 'Desk only — not shown to visitors')}</p>
                    <div className="flex flex-col divide-y rounded-lg border border-border">
                      {D5.PACKAGES.filter((p) => !p.isPublic).map((p) => <PkgOption key={p.id} value={p.id} title={p.name} amount={p.amount} terms={p.terms} tag={<DS5.Badge variant="neutral">{tr('خاصة', 'Private')}</DS5.Badge>} />)}
                      <PkgOption value="custom" title={tr('مخصّص', 'Custom')} terms={tr('حدّد الشروط والسعر بنفسك', 'Set the terms and price yourself')} />
                    </div>
                  </DS5.RadioGroup>
                </DS5.Field>
              ) : (
                // DK-007: a renewal is nearly always the same package — one line, and the list on demand.
                <div className="flex flex-col gap-2">
                  <span className="text-label">{tr('الباقة', 'Package')}</span>
                  <div className="flex flex-wrap items-center justify-between gap-2 rounded-lg border border-border p-3">
                    <span className="text-label">{P.name} · <Money n={newDue} /> · {D5.fmtDate(start)} – {D5.fmtDate(end)}</span>
                    <DS5.Button type="button" variant="link" size="sm" className="px-0" onClick={() => setShowPk(true)}>{tr('تغيير الباقة', 'Change package')}</DS5.Button>
                  </div>
                </div>
              )}
              <div className="grid gap-3">
                <DateField label={tr('من', 'From')} value={start} onChange={setStart} />
                {custom ? <DateField label={tr('إلى', 'To')} labelEnd={<Opt />} error={err.to} value={cu.to} onChange={(x) => setC({ to: x })} />
                  : <DateField label={tr('إلى', 'To')} helper={tr('تُحسب من الباقة', 'From the package')} value={end} disabled onChange={() => {}} />}
                {endNote}
              </div>
              {!custom && (priceEdit ? (
                <DS5.Field label={tr('السعر (₪)', 'Price (₪)')} labelEnd={manual ? <DS5.Badge variant="info">{tr('سعر يدوي', 'Manual price')}</DS5.Badge> : null}>
                  <DS5.Input inputMode="numeric" dir="ltr" value={price} placeholder={String(P.amount)} onChange={(e) => { setPrice(e.target.value.replace(/[^\d]/g, '')); setReceived(null); }} autoFocus />
                </DS5.Field>
              ) : <DS5.Button type="button" variant="link" size="sm" className="self-start px-0" onClick={() => { setPriceEdit(true); setPrice(String(P.amount)); }}>{tr('تعديل السعر', 'Change price')}</DS5.Button>)}
              {custom && (
                <div className="flex flex-col gap-4 rounded-lg border border-border p-3">
                  <p className="text-caption text-muted-foreground">{tr('كل الحقول اختيارية ويمكن جمعها.', 'Every field is optional and they can be combined.')}</p>
                  <div className="grid grid-cols-2 gap-3">
                    <NumIn label={tr('عدد الأيام الكلي', 'Total days')} value={cu.totalDays} onChange={(v) => setC({ totalDays: v })} />
                    <NumIn label={tr('أيام بالأسبوع', 'Days a week')} value={cu.daysPerWeek} onChange={(v) => setC({ daysPerWeek: v })} />
                    <NumIn label={tr('ساعات باليوم', 'Hours a day')} value={cu.hoursPerDay} onChange={(v) => setC({ hoursPerDay: v })} />
                    <NumIn label={tr('رصيد ساعات', 'Hour balance')} value={cu.hourBalance} onChange={(v) => setC({ hourBalance: v })} />
                  </div>
                  <DS5.Field label={tr('طريقة الحساب', 'Billing')}>
                    <DS5.ToggleGroup type="single" value={cu.billing} onValueChange={(v) => { if (v) { setC({ billing: v }); setReceived(null); } }}>
                      <DS5.ToggleGroupItem value="fixed">{tr('سعر ثابت', 'Fixed price')}</DS5.ToggleGroupItem>
                      <DS5.ToggleGroupItem value="usage">{tr('حسب الاستخدام', 'By usage')}</DS5.ToggleGroupItem>
                    </DS5.ToggleGroup>
                  </DS5.Field>
                  {cu.billing === 'fixed' ? (
                    <DS5.Field label={tr('السعر (₪)', 'Price (₪)')} error={err.amount} labelEnd={cu.amount ? <DS5.Badge variant="info">{tr('سعر يدوي', 'Manual price')}</DS5.Badge> : null}><DS5.Input inputMode="numeric" dir="ltr" value={cu.amount} onChange={(e) => { setC({ amount: e.target.value.replace(/[^\d]/g, '') }); setReceived(null); }} /></DS5.Field>
                  ) : (
                    <div className="grid gap-3 md:grid-cols-2">
                      <DS5.Field label={tr('الوحدة', 'Unit')}>
                        <DS5.ToggleGroup type="single" value={cu.unit} onValueChange={(v) => v && setC({ unit: v, rate: String(v === 'hour' ? D5.PRICES.hour : D5.PRICES.day) })}>
                          <DS5.ToggleGroupItem value="hour">{tr('بالساعة', 'Per hour')}</DS5.ToggleGroupItem>
                          <DS5.ToggleGroupItem value="day">{tr('باليوم', 'Per day')}</DS5.ToggleGroupItem>
                        </DS5.ToggleGroup>
                      </DS5.Field>
                      <DS5.Field label={tr('السعر (₪)', 'Rate (₪)')} helper={manual ? undefined : tr('من السعر المنشور', 'From the published price')} labelEnd={manual ? <DS5.Badge variant="info">{tr('سعر يدوي', 'Manual price')}</DS5.Badge> : null}><DS5.Input inputMode="numeric" dir="ltr" value={cu.rate} onChange={(e) => setC({ rate: e.target.value.replace(/[^\d]/g, '') })} /></DS5.Field>
                    </div>
                  )}
                  {D5.SHIFT_LIST.length > 0 && (
                    <DS5.Field label={tr('الوردية', 'Shift')} labelEnd={<Opt />}>
                      <DS5.ToggleGroup type="single" value={cu.shift} onValueChange={(v) => setC({ shift: v || '' })}>
                        {D5.SHIFT_LIST.map((x) => <DS5.ToggleGroupItem key={x.id} value={x.id}>{D5.SHIFTS[x.id]}</DS5.ToggleGroupItem>)}
                      </DS5.ToggleGroup>
                    </DS5.Field>
                  )}
                  <DS5.Field label={tr('اسم الاشتراك', 'Subscription name')} labelEnd={<Opt />}><DS5.Input placeholder={tr('مخصّص', 'Custom')} value={cu.title} onChange={(e) => setC({ title: e.target.value })} /></DS5.Field>
                  <DS5.Field label={tr('ملاحظة', 'Note')} labelEnd={<Opt />}><DS5.Textarea rows={2} value={cu.note} onChange={(e) => setC({ note: e.target.value })} /></DS5.Field>
                </div>
              )}
              <MoneyBlock calc={calc} due={due} dueLabel={prior.length ? tr('المجموع', 'Total') : undefined} open={usage} value={value} onValue={setReceived} method={method} onMethod={setMethod}
                remainder={usage ? 'sub' : 'debt'} who={c ? c.name : name.trim() || tr('الزبون', 'the customer')} phoneNote={askPhone && !phoneOk(phone)} />
              <MoneyRateNote />
              <ActionAlert for="sheet">{MONEY_RETRY}</ActionAlert>
            </>}
          </DS5.SheetBody>
          <DS5.SheetFooter className="flex flex-row gap-2">
            {half
              ? <DS5.Button type="button" className="flex-1" loading={payRun.busy} onClick={() => payRun.run(() => desk.pay(half.customerId, half.amount, method, '', null))}>{tr('إعادة المحاولة: تسجيل', 'Try again: record')} <Money n={half.amount} /></DS5.Button>
              : <DS5.Button type="submit" className="flex-1" loading={busy}>{submitLabel}</DS5.Button>}
          </DS5.SheetFooter>
        </form>
      </DS5.SheetContent>
    </DS5.Sheet>
  );
}
Object.assign(window, { SubscriptionSheet });
```

**Edits — `masaha/desk-core.jsx`.** Replace the `saveSubscription` method — from `    saveSubscription({ customerId, name, phone }, sub, payNow) {`
up to `    // P9: a settled customer is archived at once and can be put back from the toast.` — with:
```jsx
    // K3 + K4: the subscription, then its money — on a renewal, oldest first across what was owed
    // before, one payment per item, the rest on the new subscription. `payment` null: the payment
    // failed after the save (DK-018), so the sheet stays open and nothing is said yet.
    saveSubscription({ customerId, name, phone }, sub, payment) {
      let c = customerId && D.findCustomer(customerId);
      if (!c) { c = { id: 'c' + Date.now(), name, phone: phone ? normPhone(phone) : '', subs: [] }; D.customers.unshift(c); }
      else if (!c.phone && phone) c.phone = normPhone(phone);
      const prior = payment && payment.renew ? D.openItems(c) : [];
      c.subs.unshift(sub);
      if (!payment) { bump(); return c; }
      let left = payment.recorded; const parts = [];
      for (const it of prior) {
        if (left <= 0) break;
        const take = Math.min(left, it.due - it.paid); left -= take;
        if (it.kind === 'sub') { const s = c.subs.find((x) => x.id === it.id); s.pays.push([D.TODAY, D.NOW, take, payment.method, ME]); parts.push((s.debtLabel || s.name) + ' ' + $(take)); }
        else { const u = D.unpaid.find((x) => x.id === it.id); u.amount -= take; if (u.amount <= 0) D.unpaid.splice(D.unpaid.indexOf(u), 1); D.visitPays.unshift({ id: 'vp' + Date.now() + it.id, customerId: c.id, name: c.name, date: D.TODAY, time: D.NOW, amount: take, method: payment.method, by: ME }); parts.push(tr('زيارة ', 'Visit ') + D.fmtDate(it.date) + ' ' + $(take)); }
      }
      if (left > 0) { sub.pays.push([D.TODAY, D.NOW, left, payment.method, ME]); parts.push(sub.name + ' ' + $(left)); }
      bump(); close();
      const owed = D.balance(c);
      toast.success(payment.renew ? tr(`جُدّد اشتراك ${c.name}`, `${c.name}’s subscription renewed`) : tr(`حُفظ الاشتراك · ${c.name}`, `Subscription saved · ${c.name}`), {
        description: sub.name + ' · ' + (payment.recorded > 0 ? paidLine(payment.recorded, payment.method) + (parts.length > 1 ? ': ' + parts.join(tr('، ', ', ')) : '') : tr('بدون دفع', 'No payment')) + (owed > 0 ? tr(` · المتبقي ${$(owed)} دين`, ` · ${$(owed)} owed`) : '')
      });
      return c;
    },
```

**Edits — `masaha/desk-data.js`**

1. Replace the line that starts `  const subStatus = (sub) => { const d = daysBetween(TODAY, sub.to);` with these two lines:
```js
  // DK-008: a subscription with no end date stays active until it is ended.
  const subStatus = (sub) => { if (!sub.to) return 'active'; const d = daysBetween(TODAY, sub.to); return d < 0 ? 'expired' : d <= 7 ? 'soon' : 'active'; };
```
2. In `progress`, quote `    out.push(subStatus(sub) === 'expired' ? T(` → replace with `    out.push(!sub.to ? T('بلا تاريخ نهاية', 'No end date') : subStatus(sub) === 'expired' ? T(` (the rest of the line unchanged).
3. In `openItems`, quote `label: s.name + ' · ' + fmtDate(s.from) + ' – ' + fmtDate(s.to),` → replace with
   `label: s.name + ' · ' + fmtDate(s.from) + ' – ' + (s.to ? fmtDate(s.to) : T('بلا تاريخ نهاية', 'No end date')),`

**Edit — `Desk.html`.** In `initialDialog`, the `sheet` line: after `payNow: pageParams.get('paynow')` add
`, half: pageParams.get('half') === '1'` (inside the object).

### 3.4 One desk search, ordered for phones — K1, DK-001, DK-002, DK-003, DK-023, P1 (commit 4)

| Decision | On screen |
|---|---|
| K1 / DK-001 / DK-002 | `DeskSearch`: the search, then (in a `aria-live="polite"` region) `SearchResults`: «حاضر الآن» (h2, `text-label text-muted-foreground`) — rows of name (a link when on file), `KindBadge`, «منذ 12:20», `OutButton`; «زبائن» — up to 6 `CustomerCard`s of customers not present; then «تسجيل زيارة باسم «X»» (`primary` when nothing matched, else `outline`) and «زبون جديد باسم «X»» (`outline`); a digits-only term: «تسجيل زيارة» and «زبون جديد بهذا الرقم» (the digits go to «رقم الجوال»). Nothing matched: `EmptyState` «لا أحد بهذا الاسم أو الرقم» / «زائر لمرة واحدة؟ سجّل له زيارة.» holding the two buttons |
| DK-003 | below 1280: the search, the uncollected card, then the present section; from 1280 the card is the side column (`masaha.css`); the section's h2 «الحاضرون الآن 27 / 40» with `Tabs` «الآن | السجل» beside it; the table's summary «19 مشتركًا · 8 زيارات» (O5's forms) |
| P1 | page actions «استلام دفعة», «زبون جديد», «تسجيل زيارة» (primary, `bottom: true`); the «زبون جديد» button beside the search is gone |
| DK-023 | `VisitDialog`: the description names the rate — «تُحسب 3 ₪ للساعة · حتى 15 ₪.» (cap on), «تُحسب بسعر اليوم 15 ₪.» (no hour price), the manual line (no price); «طالب» only when `D.STUDENT_VISITS`; «الوردية» only when the space has shifts, set to the one in progress; the name carried from the search |

**New strings:**

| Arabic | English |
|---|---|
| البحث (the search section's name) | Search |
| حاضر الآن · زبائن | Here now · Customers |
| تسجيل زيارة باسم «X» · زبون جديد باسم «X» | Check in a visit for «X» · New customer named «X» |
| زبون جديد بهذا الرقم | New customer with this number |
| لا أحد بهذا الاسم أو الرقم | No one by this name or number |
| زائر لمرة واحدة؟ سجّل له زيارة. | A one-off visitor? Check in a visit. |
| تُحسب {3 ₪} للساعة · حتى {15 ₪}. · تُحسب بسعر اليوم {15 ₪}. | Charged {₪3} an hour · up to {₪15}. · Charged at the day price {₪15}. |
| (the summary) {19 مشتركًا} · {8 زيارات} | {19 subscribers} · {8 visits} |

Removed: «ابحث بين الحاضرين», «لا يوجد حاضر بهذا الاسم.», «لا يوجد زبون بهذا الاسم أو الرقم» (the desk's),
«إذا كان يزور لمرة واحدة، سجّل له زيارة.», the summary's «الحاضرون الآن 27 / 40 · …».

**States:** search results are live; the present list keeps `?state=loading|empty`; `?tab=log` keeps the
log. **Parameters:** `?q=` (now finds everyone), `?dialog=visit&vname=<name>`, `?demo=noshifts`,
`?demo=studentprices`, `?demo=nostudent`, `?demo=nocap` (a comma list, as on the owner's pages).

**Edits — `Desk.html`**

1. Replace from `function PresentList() {` up to `// DK-003: the money to chase, compact` with:
```jsx
function PresentList() {
  const rows = DESK.present;
  const subs = rows.filter((p) => p.kind === 'sub').length;
  const mins = (p) => DESK.toMin(DESK.NOW) - DESK.toMin(p.since);
  const columns = [
    { id: 'name', header: tr('الاسم', 'Name'), cell: ({ row }) => row.original.customerId ? <a className="text-label text-foreground" href={roleQ('Customer file.html?id=' + row.original.customerId)}>{nameOf(row.original)}</a> : <span className="text-label">{nameOf(row.original)}</span> },
    { id: 'kind', header: tr('النوع', 'Type'), cell: ({ row }) => <KindBadge p={row.original} /> },
    { id: 'since', header: tr('منذ', 'Since'), cell: ({ row }) => <Num>{row.original.since}</Num> },
    { id: 'dur', header: tr('المدة', 'Duration'), cell: ({ row }) => durLabel(mins(row.original)) },
    // SH-007: six columns; the usage line is the one that can wait for 1024.
    { id: 'detail', header: tr('الاستخدام', 'Usage'), meta: { className: 'hidden lg-col' }, cell: ({ row }) => <span className="text-body-sm"><Detail p={row.original} /></span> },
    { id: 'act', header: () => <span className="sr-only">{tr('إجراءات', 'Actions')}</span>, cell: ({ row }) => <div className="flex justify-end"><OutButton p={row.original} size="sm" /></div> }
  ];
  // DK-003: «27 / 40» is said once, in the section's heading; the table's line splits it.
  return (
    <DataTable label={tr('الحاضرون الآن', 'Present now')} columns={columns} data={rows} getRowId={(r) => r.id} loading={st === 'loading'}
      summary={<span><Counted n={subs} ar={F_SUBSCRIBERS.ar} en={F_SUBSCRIBERS.en} /> · <Counted n={rows.length - subs} ar={F_VISITS.ar} en={F_VISITS.en} /></span>}
      renderCard={(p) => (
        <div className="flex items-start justify-between gap-3">
          <div className="flex min-w-0 flex-col gap-1">
            <span className="text-label">{nameOf(p)}</span>
            <span><KindBadge p={p} /></span>
            <span className="text-caption text-muted-foreground">{tr('منذ', 'Since')} <Num>{p.since}</Num> · {durLabel(mins(p))}</span>
            <span className="text-caption"><Detail p={p} /></span>
          </div>
          <OutButton p={p} size="sm" />
        </div>
      )}
      empty={<EmptyState icon={<UsersIcon />} title={tr('لا أحد حاضر الآن', 'No one is here right now')} description={tr('ابحث عن زبون أو سجّل زيارة لأول من يصل.', 'Search for a customer, or check in a visit for the first arrival.')} />} />
  );
}

```
2. Replace from `function DeskSearch() {` up to `ReactDOM.createRoot(` (the old `DeskSearch`, `DeskScreen` and `DeskInner`) with:
```jsx
// K1 (DK-001, DK-002): one search finds everyone — the people here first, with «خروج»; then the
// customers on file, with «حضور»; then the two ways in for what was typed, which they carry.
const RESULTS_MAX = 6;
function PresentRow({ p }) {
  return (
    <li className="flex items-center justify-between gap-3 px-4 py-3">
      <div className="flex min-w-0 flex-col gap-1">
        {p.customerId ? <a className="text-label text-foreground" href={roleQ('Customer file.html?id=' + p.customerId)}>{nameOf(p)}</a> : <span className="text-label">{nameOf(p)}</span>}
        <span className="flex flex-wrap items-center gap-2 text-caption text-muted-foreground"><KindBadge p={p} /><span>{tr('منذ', 'Since')} <Num>{p.since}</Num></span></span>
      </div>
      <OutButton p={p} size="sm" />
    </li>
  );
}
function SearchResults({ term }) {
  const desk = useDesk();
  const t = term.trim(); const digits = t.replace(/\D/g, '');
  const byDigits = digits.length >= 2 && digits === t.replace(/[\s+]/g, '');
  const phoneOf = (p) => (p.customerId ? DESK.findCustomer(p.customerId).phone || '' : '');
  const here = DESK.present.filter((p) => nameOf(p).includes(t) || (byDigits && phoneOf(p).replace(/\D/g, '').endsWith(digits)));
  const people = DESK.searchCustomers(t).filter((c) => !DESK.presentOf(c.id)).slice(0, RESULTS_MAX);
  const none = !here.length && !people.length;
  // A one-off visit is the common case (glossary › Visit): it leads when nothing matches.
  const visitBtn = <Button variant={none ? 'primary' : 'outline'} onClick={() => desk.open('visit', { name: byDigits ? '' : t })}><LogInIcon />{byDigits ? tr('تسجيل زيارة', 'Check in a visit') : <>{tr('تسجيل زيارة باسم', 'Check in a visit for')} «{t}»</>}</Button>;
  const newBtn = <Button variant="outline" onClick={() => desk.open('sheet', byDigits ? { mode: 'new', phone: t } : { mode: 'new', name: t })}>{byDigits ? tr('زبون جديد بهذا الرقم', 'New customer with this number') : <>{tr('زبون جديد باسم', 'New customer named')} «{t}»</>}</Button>;
  if (none) return <Card><EmptyState icon={<SearchXIcon />} title={tr('لا أحد بهذا الاسم أو الرقم', 'No one by this name or number')} description={tr('زائر لمرة واحدة؟ سجّل له زيارة.', 'A one-off visitor? Check in a visit.')}>{visitBtn}{newBtn}</EmptyState></Card>;
  return (
    <div className="flex flex-col gap-4">
      {here.length > 0 && (
        <section aria-labelledby="results-here" className="flex flex-col gap-2">
          <h2 id="results-here" className="text-label text-muted-foreground">{tr('حاضر الآن', 'Here now')}</h2>
          <ul className="flex flex-col divide-y rounded-lg border border-border bg-card">{here.map((p) => <PresentRow key={p.id} p={p} />)}</ul>
        </section>
      )}
      {people.length > 0 && (
        <section aria-labelledby="results-customers" className="flex flex-col gap-2">
          <h2 id="results-customers" className="text-label text-muted-foreground">{tr('زبائن', 'Customers')}</h2>
          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">{people.map((c) => <CustomerCard key={c.id} c={c} />)}</div>
        </section>
      )}
      <div className="flex flex-wrap gap-2">{visitBtn}{newBtn}</div>
    </div>
  );
}
// The results come straight after the search in the page's order, in a live region.
function DeskSearch() {
  const [q, setQ] = React.useState(pageParams.get('q') || '');
  return (
    <section aria-label={tr('البحث', 'Search')} className="flex flex-col gap-4">
      <Input role="searchbox" size="lg" aria-label={tr('ابحث بالاسم أو آخر أرقام الجوال', 'Search by name or last digits of the mobile')} placeholder={tr('الاسم أو آخر أرقام الجوال', 'Name or last digits of the mobile')} startIcon={<SearchIcon />} value={q} onChange={(e) => setQ(e.target.value)} autoFocus />
      <div aria-live="polite">{q.trim() && <SearchResults term={q} />}</div>
    </section>
  );
}

function DeskScreen() {
  const [theme, setTheme] = useTheme();
  return (
    <DeskProvider initial={initialDialog}>
      <DeskInner theme={theme} setTheme={setTheme} />
    </DeskProvider>
  );
}
function DeskInner({ theme, setTheme }) {
  const desk = useDesk();
  const [tab, setTab] = React.useState(pageParams.get('tab') === 'log' ? 'log' : 'now');
  // DK-010: ?dialog=checkout&pid=<a fixed-price subscriber> checks them out on load, as the tap does.
  React.useEffect(() => { const p = DESK.present.find((x) => x.id === pageParams.get('pid')); if (pageParams.get('dialog') === 'checkout' && p && isQuickOut(p)) setTimeout(() => desk.checkOut(p.id), 300); }, []);
  // P1, amended: the bottom bar holds only the page's purpose, used all day. «استلام دفعة» and «زبون
  // جديد» are page actions: in the top bar from 768, in its «⋯» on a phone.
  const bottom = <Button className="w-full" onClick={() => desk.open('visit')}><LogInIcon />{tr('تسجيل زيارة', 'Check in a visit')}</Button>;
  const pageActions = [
    { key: 'pay', label: tr('استلام دفعة', 'Receive payment'), onClick: () => desk.open('pay', {}) },
    { key: 'new', label: tr('زبون جديد', 'New customer'), onClick: () => desk.open('sheet', { mode: 'new' }) },
    { key: 'visit', label: tr('تسجيل زيارة', 'Check in a visit'), icon: <LogInIcon />, variant: 'primary', bottom: true, onClick: () => desk.open('visit') }
  ];
  return (
    <OwnerShell current="desk" title={tr('مكتب الاستقبال', 'Front desk')} state={publicState(DESK.present.length, DESK.capacity)} theme={theme} setTheme={setTheme} actions={pageActions} bottomAction={bottom}>
      <DeskSearch />
      {/* DK-003: below xl the money to chase comes before the people here; from xl it is the side column (masaha.css). */}
      <div className="desk-now flex flex-col gap-6">
        <UnpaidCard />
        <section aria-labelledby="present-title" className="desk-present flex min-w-0 flex-col gap-4">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <h2 id="present-title" className="text-heading-3">{tr('الحاضرون الآن', 'Present now')} <Num>{DESK.present.length + ' / ' + DESK.capacity}</Num></h2>
            <Tabs value={tab} onValueChange={setTab}>
              <TabsList aria-label={tr('الحضور', 'Attendance')}>
                <TabsTrigger value="now">{tr('الآن', 'Now')}</TabsTrigger>
                <TabsTrigger value="log">{tr('السجل', 'Log')}</TabsTrigger>
              </TabsList>
            </Tabs>
          </div>
          {tab === 'now' ? <PresentList /> : <LogTab />}
        </section>
      </div>
    </OwnerShell>
  );
}
```
3. In `UnpaidCard`, change `'section-anchor'` back to `'section-anchor desk-unpaid'` (one place).
4. In `initialDialog`, quote `  if (d === 'visit') return { kind: 'visit' };` → replace with
   `  if (d === 'visit') return { kind: 'visit', name: pageParams.get('vname') || '' };`

**Edits — `masaha/desk-core.jsx`**

1. Replace from `// 4.3 Visit: a name only — no customer record.` up to `function WarnDialog(` with:
```jsx
// 4.3 Visit: a name, with the name the search carried (DK-002), and only the choices the space uses
// (DK-023): «طالب» where it changes the rate, «الوردية» where the space has shifts, on the one now.
function VisitDialog({ dlg, onClose }) {
  const desk = useDesk();
  const [name, setName] = React.useState(''); const [student, setStudent] = React.useState(false); const [shift, setShift] = React.useState(''); const [err, setErr] = React.useState();
  React.useEffect(() => { if (dlg) { setName(dlg.name || ''); setStudent(false); setShift(D.currentShift()); setErr(); } }, [dlg]);
  const { busy, run } = useActionRun('visit');
  const submit = (e) => { e.preventDefault(); if (!name.trim()) { setErr(tr('أدخل الاسم', 'Enter the name')); return focusInvalid(); } run(() => desk.checkInVisit(name.trim(), student, shift || null)); };
  const r = D.visitRates(student);
  const rate = r.hour ? <>{tr('تُحسب', 'Charged')} <Money n={r.hour} /> {tr('للساعة', 'an hour')}{D.SETTINGS.cap && r.day ? <> · {tr('حتى', 'up to')} <Money n={r.day} /></> : null}.</>
    : r.day ? <>{tr('تُحسب بسعر اليوم', 'Charged at the day price')} <Money n={r.day} />.</> : tr('لا يوجد سعر منشور؛ تُدخل المبلغ عند الخروج.', 'No published price; you enter the amount at check-out.');
  return (
    <DK.Dialog open={!!dlg} onOpenChange={(o) => !o && onClose()}>
      <DK.DialogContent closeLabel={tr('إغلاق', 'Close')}>
        <DK.DialogHeader>
          <DK.DialogTitle>{tr('تسجيل زيارة', 'Check in a visit')}</DK.DialogTitle>
          <DK.DialogDescription>{rate} {tr('لا يُنشأ ملف زبون.', 'No customer record is created.')}</DK.DialogDescription>
        </DK.DialogHeader>
        <form onSubmit={submit} noValidate className="flex flex-col gap-4">
          {desk.full() && <FullAlert />}
          <DK.Field label={tr('الاسم', 'Name')} error={err}><DK.Input value={name} onChange={(e) => setName(e.target.value)} autoFocus /></DK.Field>
          {D.STUDENT_VISITS && <DK.Field label={tr('طالب', 'Student')} orientation="horizontal"><DK.Switch checked={student} onCheckedChange={setStudent} /></DK.Field>}
          {D.SHIFT_LIST.length > 0 && (
            <DK.Field label={tr('الوردية', 'Shift')} labelEnd={<span className="text-caption text-muted-foreground">{tr('اختياري', 'Optional')}</span>}>
              <DK.ToggleGroup type="single" value={shift} onValueChange={(v) => setShift(v || '')}>
                {D.SHIFT_LIST.map((x) => <DK.ToggleGroupItem key={x.id} value={x.id}>{D.SHIFTS[x.id]}</DK.ToggleGroupItem>)}
              </DK.ToggleGroup>
            </DK.Field>
          )}
          <MoneyRateNote />
          <ActionAlert for="visit">{MONEY_RETRY}</ActionAlert>
          <DK.DialogFooter><DK.Button type="submit" loading={busy}><DK.LogInIcon />{desk.full() ? tr('تسجيل على أي حال', 'Check in anyway') : tr('تسجيل الزيارة', 'Check in')}</DK.Button></DK.DialogFooter>
        </form>
      </DK.DialogContent>
    </DK.Dialog>
  );
}

```
2. In the provider, quote `      <VisitDialog open={dlg && dlg.kind === 'visit'} onClose={close} />` → replace with
   `      <VisitDialog dlg={dlg && dlg.kind === 'visit' ? dlg : null} onClose={close} />`

**Edit — `masaha/masaha.css`.** Append at the end of the file:
```css
/* DK-003: below xl the desk reads search → uncollected → present; from xl the uncollected card is the
   side column again, beside the present list, as before. */
@media(min-width:1280px){.desk-now{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));column-gap:1.5rem;align-items:start}.desk-now>.desk-present{grid-column:1/span 8;grid-row:1}.desk-now>.desk-unpaid{grid-column:9/span 4;grid-row:1}}
```

### 3.5 The week's warning uses the count — K5 (commit 5)

| Decision | On screen |
|---|---|
| K5 / DK-009 | check-in warning `week`: «استُنفدت أيام هذا الأسبوع» / the progress line «هذا الأسبوع 3 من 3»; Mayar's subscription is «3 أيام بالأسبوع» (days per week 3, used 3 this week) |

| Arabic | English |
|---|---|
| استُنفدت أيام هذا الأسبوع | This week’s days are used up |
| 3 أيام بالأسبوع (Mayar's subscription's name; was «3 أيام ثابتة») | 3 days a week |

Removed: «اليوم ليس من أيامه», «أيامه: السبت، الاثنين، الأربعاء».

**Edits — `masaha/desk-data.js`**

1. In customer `m12`'s line, quote `{ name: T('3 أيام ثابتة', '3 fixed days'), terms: { weekDays: ['sat', 'mon', 'wed'] }, billing` →
   replace with `{ name: T('3 أيام بالأسبوع', '3 days a week'), terms: { daysPerWeek: 3 }, used: { week: 3 }, billing`.
2. In `progress`, delete the line that starts `    if (t.weekDays) out.push(T('أيامه: ', 'Days: ')`.
3. In `termsLine`, delete the line that starts `    if (t.weekDays) parts.push(`.
   (`WEEKDAYS` and `TODAY_KEY` stay exported: Finance's heatmap reads `WEEKDAYS`.)

**Edits — `masaha/desk-core.jsx`**

1. In `checkInWarnings`, quote `    if (s.terms.weekDays && !s.terms.weekDays.includes(D.TODAY_KEY)) w.push({ id: 'notday', sub: s });` → replace with:
```jsx
    // K5: the model holds days a week as a count, so the warning is the count used up — never which days.
    if (s.terms.daysPerWeek && (s.used.week || 0) >= s.terms.daysPerWeek) w.push({ id: 'week', sub: s });
```
2. In `WarnDialog`'s `texts`, quote the line that starts `    notday: (w) => [tr('اليوم ليس من أيامه'` → replace the whole line with:
```jsx
    week: (w) => [tr('استُنفدت أيام هذا الأسبوع', 'This week’s days are used up'), D.progress(w.sub, c).find((l) => l.startsWith(tr('هذا الأسبوع', 'This week')))],
```

### 3.6 Customers: actions by state, archive — DK-013, DK-014, DK-022, DK-017 (commit 6)

| Decision | On screen |
|---|---|
| DK-013 | `CustomerActions` (desk card, `sm`; file header, `md`): «حضور» (primary, `LogInIcon`) or `OutButton` (primary); «استلام 42 ₪» (`secondary`) when the balance is above 0; «تجديد» (`outline`) when ending soon or ended; «⋯» (`ghost` `icon`, `EllipsisVerticalIcon`) holding `CustomerMenuItems`: «اشتراك جديد», «تعديل البيانات», «ملف الزبون» (not in the file), and the owner's separator + «أرشفة». The Customers row's «⋯» holds the state's three first, then a separator, then the rest (`full`). The card loses its five-button footer and «ملف الزبون» (the name links to the file) |
| DK-014 | «تعديل البيانات» → `EditCustomerDialog`: «الاسم» (required), «رقم الجوال» («اختياري», helper «إليه يُرسل تذكير الدين على واتساب.»), «حفظ»; PHONE_TAKEN «هذا الرقم مسجّل لزبون آخر: سلمى الريس» on the field. Archive: settled → at once with «تراجع»; owing → `ArchiveDialog` (moved into the provider). Archived = `c.archived = { by, on }`, never removed: out of the desk search and the picker, listed under «مؤرشف» with «استرجاع» (owner) |
| DK-022 | status: a `ToggleGroup` of chips «الكل · نشط · ينتهي قريبًا · منتهٍ» + the owner's «مؤرشف», outside the filter sheet, by the count; «بدون اشتراك» only under «نوع الاشتراك»; the filter sheet's badge counts type and payment |
| DK-017 | Customers: «الاسم» (the mobile under), «الاشتراك» («حتى 20 أكتوبر» under, or «بلا تاريخ نهاية»), «الحالة», «الرصيد», «⋯» — at every width from 768 |

**New strings:**

| Arabic | English |
|---|---|
| استلام {42 ₪} | Receive {₪42} |
| إجراءات أخرى: {X} · إجراءات: {X} (the «⋯»'s names) | More actions: {X} · Actions: {X} |
| تعديل البيانات · حفظ | Edit details · Save |
| إليه يُرسل تذكير الدين على واتساب. | Debt reminders go to this number on WhatsApp. |
| هذا الرقم مسجّل لزبون آخر: {X} | This number belongs to another customer: {X} |
| رقم غير مكتمل، مثل +970 59 000 0000 (kept) | Incomplete number, e.g. +970 59 000 0000 |
| استرجاع · مؤرشف · الكل · تصفية حسب الحالة | Restore · Archived · All · Filter by status |
| الاشتراك (column, was «الاشتراك الحالي») · حتى {date} · بلا تاريخ نهاية | Subscription · until {date} · No end date |
| لا يوجد زبائن مؤرشفون | No archived customers |
| (archive dialog) … غير مسدّدة. يبقى المبلغ في سجله، ويخرج من البحث ومن المكتب، ويبقى تحت «مؤرشف» في الزبائن. | … unpaid. The amount stays on their record; they leave the search and the desk, and stay under «Archived» in Customers. |
| Toasts: استُرجع {X} · حُفظت بيانات {X} | {X} restored · {X}’s details saved |

**Parameters:** `Customers.html?status=archived` (and `active`, `soon`, `expired`); `Customers.html?edit=<id>`,
`Customer file.html?edit=1`, both with `&taken=1`; `Customers.html?archive=<id>` kept (owner).
**States:** `?fail=edit`; the list's loading/empty kept; an empty «مؤرشف»: «لا يوجد زبائن مؤرشفون».

**Edits — `masaha/desk-data.js`**

1. Customer `m15`'s line ends `] }` and is the last of the array (followed by `  ];`): add a comma at its end, then insert after it:
```js
    // DK-014: archived, never deleted.
    { id: 'm16', name: T('عبير حسونة', 'Abeer Hassouna'), phone: '+970 59 000 1016', archived: { by: A, on: '2026-09-10' }, subs: [S('s16', 'week', '2026-08-03', '2026-08-09', { pays: [['2026-08-03', '09:40', 90, 'cash', A]] })] }
```
2. Quote `  const customerStatus = (c) => (currentSub(c) ? subStatus(currentSub(c)) : 'none');` → replace with
   `  const customerStatus = (c) => (c.archived ? 'archived' : currentSub(c) ? subStatus(currentSub(c)) : 'none');`
3. In `statusBadge`, quote `none: ['neutral', T('بدون اشتراك', 'No subscription')] };` → replace with
   `none: ['neutral', T('بدون اشتراك', 'No subscription')], archived: ['neutral', T('مؤرشف', 'Archived')] };`

**Edits — `masaha/desk-core.jsx`**

1. Replace from `    // P9: a settled customer is archived at once and can be put back from the toast.` up to the provider's
   `  };` line (the end of `api`; the old `archive` and `archiveOwing`) with these two blocks, one after the other:
```jsx
    // DK-014: archived, never deleted — out of the search and the desk, under «مؤرشف» in Customers.
    // P9: a settled customer is archived at once and can be put back from the toast.
    archive(cid) {
      const c = D.findCustomer(cid); c.archived = { by: ME, on: D.TODAY }; bump();
      toast(tr(`أُرشف ${c.name}`, `${c.name} archived`), { action: { label: tr('تراجع', 'Undo'), onClick: () => { delete c.archived; bump(); } } });
    },
    // A customer who owes is archived only after the dialog that names the debt, so there is
    // no undo after it: the confirmation was the decision.
    archiveOwing(cid) {
      const c = D.findCustomer(cid); c.archived = { by: ME, on: D.TODAY }; bump(); close();
      toast.success(tr(`أُرشف ${c.name} · عليه ${$(D.balance(c))}`, `${c.name} archived · owes ${$(D.balance(c))}`));
    },
    askArchive(cid) { if (D.balance(D.findCustomer(cid)) > 0) open('archive', { customerId: cid }); else api.archive(cid); },
    restore(cid) {
      const c = D.findCustomer(cid); delete c.archived; bump();
      toast.success(tr(`استُرجع ${c.name}`, `${c.name} restored`));
    },
    saveCustomer(cid, name, phone) {
      const c = D.findCustomer(cid); c.name = name; c.phone = phone ? normPhone(phone) : '';
      bump(); close(); toast.success(tr(`حُفظت بيانات ${name}`, `${name}’s details saved`));
    }
```
2. After the provider's `WriteOffDialog` line insert:
```jsx
      <EditCustomerDialog dlg={dlg && dlg.kind === 'edit' ? dlg : null} onClose={close} />
      <ArchiveDialog dlg={dlg && dlg.kind === 'archive' ? dlg : null} onClose={close} />
```
3. In `CustomerCard`: quote the comment `// 4.2 Customer card: who, where, what's left, one tap for each action.` → replace with
   `// 4.2 Customer card: who, where, what's left; its actions by state (DK-013). The name opens the file.`;
   and replace the whole `<DK.CardFooter className="flex flex-wrap gap-2">` … `</DK.CardFooter>` element (eight lines:
   the opening tag, the check-in/out pair on two lines, the four other buttons, the closing tag) with the one line `      <DK.CardFooter><CustomerActions c={c} where="card" /></DK.CardFooter>`
4. Insert before `function FullAlert() {`:
```jsx
// DK-013: one set of a customer's actions, in one order, wherever they are. `full`: the Customers
// row, whose «⋯» holds them all; elsewhere the state's actions are buttons beside the «⋯».
function CustomerMenuItems({ c, full, where }) {
  const desk = useDesk();
  const here = D.presentOf(c.id); const bal = D.balance(c); const st = D.customerStatus(c);
  return (
    <>
      {full && <>
        {here
          ? <DK.DropdownMenuItem onSelect={() => (isQuickOut(here) ? desk.checkOut(here.id) : desk.open('checkout', { presentId: here.id }))}>{tr('خروج', 'Check out')}</DK.DropdownMenuItem>
          : <DK.DropdownMenuItem onSelect={() => desk.tapCheckIn(c.id)}>{tr('حضور', 'Check in')}</DK.DropdownMenuItem>}
        {bal > 0 && <DK.DropdownMenuItem onSelect={() => desk.open('pay', { customerId: c.id })}><span>{tr('استلام', 'Receive')} <Money n={bal} /></span></DK.DropdownMenuItem>}
        {(st === 'soon' || st === 'expired') && <DK.DropdownMenuItem onSelect={() => desk.open('sheet', { mode: 'renew', customerId: c.id })}>{tr('تجديد', 'Renew')}</DK.DropdownMenuItem>}
        <DK.DropdownMenuSeparator />
      </>}
      <DK.DropdownMenuItem onSelect={() => desk.open('sheet', { mode: 'subscribe', customerId: c.id })}>{tr('اشتراك جديد', 'New subscription')}</DK.DropdownMenuItem>
      <DK.DropdownMenuItem onSelect={() => desk.open('edit', { customerId: c.id })}>{tr('تعديل البيانات', 'Edit details')}</DK.DropdownMenuItem>
      {where !== 'file' && <DK.DropdownMenuItem asChild><a href={roleQ('Customer file.html?id=' + c.id)}>{tr('ملف الزبون', 'Customer file')}</a></DK.DropdownMenuItem>}
      {IS_OWNER && <><DK.DropdownMenuSeparator /><DK.DropdownMenuItem onSelect={() => desk.askArchive(c.id)}>{tr('أرشفة', 'Archive')}</DK.DropdownMenuItem></>}
    </>
  );
}
// On the desk's card and the file's header: «حضور» or «خروج» first; «استلام 42 ₪» only when they
// owe; «تجديد» only when ending soon or ended; the rest in «⋯». An archived customer: «استرجاع».
function CustomerActions({ c, where }) {
  const desk = useDesk();
  const here = D.presentOf(c.id); const bal = D.balance(c); const st = D.customerStatus(c);
  const size = where === 'card' ? 'sm' : undefined;
  if (c.archived) return IS_OWNER ? <DK.Button size={size} variant="outline" onClick={() => desk.restore(c.id)}>{tr('استرجاع', 'Restore')}</DK.Button> : null;
  return (
    <div className="flex flex-wrap items-center gap-2">
      {here ? <OutButton p={here} size={size} variant="primary" /> : <DK.Button size={size} onClick={() => desk.tapCheckIn(c.id)}><DK.LogInIcon />{tr('حضور', 'Check in')}</DK.Button>}
      {bal > 0 && <DK.Button size={size} variant="secondary" onClick={() => desk.open('pay', { customerId: c.id })}>{tr('استلام', 'Receive')} <Money n={bal} /></DK.Button>}
      {(st === 'soon' || st === 'expired') && <DK.Button size={size} variant="outline" onClick={() => desk.open('sheet', { mode: 'renew', customerId: c.id })}>{tr('تجديد', 'Renew')}</DK.Button>}
      <DK.DropdownMenu dir={DIR}>
        <DK.DropdownMenuTrigger asChild><DK.Button variant="ghost" size="icon" aria-label={tr('إجراءات أخرى: ', 'More actions: ') + c.name}><DK.EllipsisVerticalIcon /></DK.Button></DK.DropdownMenuTrigger>
        <DK.DropdownMenuContent align="end"><CustomerMenuItems c={c} where={where} /></DK.DropdownMenuContent>
      </DK.DropdownMenu>
    </div>
  );
}

// DK-014: the name and the mobile are put right at the desk (both roles). The mobile is where a debt
// reminder goes, and is unique among the space's customers that are not archived (PHONE_TAKEN).
function EditCustomerDialog({ dlg, onClose }) {
  const desk = useDesk();
  const c = dlg && D.findCustomer(dlg.customerId);
  const [name, setName] = React.useState(''); const [phone, setPhone] = React.useState(''); const [err, setErr] = React.useState({});
  const takenBy = (v) => (phoneOk(v) ? D.customers.find((x) => x.id !== (c && c.id) && !x.archived && x.phone === normPhone(v)) : null);
  const takenLine = (o) => tr('هذا الرقم مسجّل لزبون آخر: ', 'This number belongs to another customer: ') + o.name;
  // ?taken=1: the frame of PHONE_TAKEN — Salma's number typed, as the server answers it.
  React.useEffect(() => { if (c) { const other = dlg.taken ? D.findCustomer('m8') : null; setName(c.name); setPhone(other ? other.phone : c.phone || ''); setErr(other ? { phone: takenLine(other) } : {}); } }, [dlg]);
  const { busy, run } = useActionRun('edit');
  const submit = (e) => {
    e.preventDefault();
    const x = {}; const other = takenBy(phone);
    if (!name.trim()) x.name = tr('أدخل الاسم', 'Enter the name');
    if (phone && !phoneOk(phone)) x.phone = tr('رقم غير مكتمل، مثل +970 59 000 0000', 'Incomplete number, e.g. +970 59 000 0000');
    else if (other) x.phone = takenLine(other);
    setErr(x); if (Object.keys(x).length) return focusInvalid();
    run(() => desk.saveCustomer(c.id, name.trim(), phone));
  };
  return (
    <DK.Dialog open={!!c} onOpenChange={(o) => !o && onClose()}>
      <DK.DialogContent closeLabel={tr('إغلاق', 'Close')}>
        {c && <>
          <DK.DialogHeader><DK.DialogTitle>{tr('تعديل البيانات', 'Edit details')}</DK.DialogTitle><DK.DialogDescription>{c.name}</DK.DialogDescription></DK.DialogHeader>
          <form onSubmit={submit} noValidate className="flex flex-col gap-4">
            <DK.Field label={tr('الاسم', 'Name')} error={err.name}><DK.Input value={name} onChange={(e) => setName(e.target.value)} autoFocus /></DK.Field>
            <DK.Field label={tr('رقم الجوال', 'Mobile number')} labelEnd={<span className="text-caption text-muted-foreground">{tr('اختياري', 'Optional')}</span>} error={err.phone} helper={err.phone ? undefined : tr('إليه يُرسل تذكير الدين على واتساب.', 'Debt reminders go to this number on WhatsApp.')}>
              <DK.Input type="tel" dir="ltr" placeholder="+970 59 000 0000" value={phone} onChange={(e) => setPhone(e.target.value)} />
            </DK.Field>
            <ActionAlert for="edit" />
            <DK.DialogFooter><DK.Button type="submit" loading={busy}>{tr('حفظ', 'Save')}</DK.Button></DK.DialogFooter>
          </form>
        </>}
      </DK.DialogContent>
    </DK.Dialog>
  );
}

// P9 (DK-014): a customer who owes is archived only after the dialog that names the debt — no undo after.
function ArchiveDialog({ dlg, onClose }) {
  const desk = useDesk();
  const c = dlg && D.findCustomer(dlg.customerId);
  return (
    <DK.AlertDialog open={!!c} onOpenChange={(o) => !o && onClose()}>
      <DK.AlertDialogContent>
        <DK.AlertDialogHeader>
          <DK.AlertDialogTitle>{tr('أرشفة', 'Archive')} {c && c.name}{tr('؟', '?')}</DK.AlertDialogTitle>
          <DK.AlertDialogDescription>{tr('عليه', 'They owe')} <Money n={c ? D.balance(c) : 0} /> {tr('غير مسدّدة. يبقى المبلغ في سجله، ويخرج من البحث ومن المكتب، ويبقى تحت «مؤرشف» في الزبائن.', 'unpaid. The amount stays on their record; they leave the search and the desk, and stay under «Archived» in Customers.')}</DK.AlertDialogDescription>
        </DK.AlertDialogHeader>
        <DK.AlertDialogFooter>
          <DK.AlertDialogCancel>{tr('رجوع', 'Back')}</DK.AlertDialogCancel>
          <DK.AlertDialogAction variant="destructive" onClick={() => desk.archiveOwing(c.id)}>{tr('أرشفة رغم الدين', 'Archive anyway')}</DK.AlertDialogAction>
        </DK.AlertDialogFooter>
      </DK.AlertDialogContent>
    </DK.AlertDialog>
  );
}

```
5. In the last line, after `UnpaidRow` add `, CustomerActions, CustomerMenuItems`.

**Edit — `Customers.html`.** Replace the inline `<script type="text/babel">` (the one without `src`, through its
`</script>`) with:
```html
<script type="text/babel">
const { DirectionProvider, Button, DataTable, EmptyState, Input, Select, SelectTrigger, SelectValue, SelectContent, SelectItem, ToggleGroup, ToggleGroupItem, DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, SearchIcon, UsersIcon, EllipsisVerticalIcon } = window.MasahaDesignSystem;
const st = pageParams.get('state');
if (st === 'empty') DESK.customers.length = 0;
const kindLabel = { month: tr('شهري', 'Monthly'), week: tr('أسبوعي', 'Weekly'), package: tr('باقة', 'Package'), custom: tr('مخصّص', 'Custom'), none: tr('بدون اشتراك', 'No subscription') };
const kindOf = (c) => { const s = DESK.currentSub(c); return s ? DESK.subKind(s) : 'none'; };
const renew = pageParams.get('renew');
const initial = renew ? { kind: 'sheet', mode: 'renew', customerId: renew }
  : pageParams.get('sheet') === 'new' ? { kind: 'sheet', mode: 'new' }
  : pageParams.get('archive') && IS_OWNER ? { kind: 'archive', customerId: pageParams.get('archive') }
  : pageParams.get('edit') ? { kind: 'edit', customerId: pageParams.get('edit'), taken: pageParams.get('taken') === '1' } : null;
// DK-022: the status is one fact, so one filter, of chips; «بدون اشتراك» lives under the type only.
// DK-014: «مؤرشف» lists the archived customers, for the owner, who archives and restores them.
const STATUSES = () => [['all', tr('الكل', 'All')], ['active', DESK.statusBadge.active[1]], ['soon', DESK.statusBadge.soon[1]], ['expired', DESK.statusBadge.expired[1]], ...(IS_OWNER ? [['archived', DESK.statusBadge.archived[1]]] : [])];

function Filter({ label, value, onChange, options }) {
  return (
    <div className="md:w-44"><Select value={value} onValueChange={onChange}>
      <SelectTrigger aria-label={label}><SelectValue /></SelectTrigger>
      <SelectContent>{options.map(([v, l]) => <SelectItem key={v} value={v}>{l}</SelectItem>)}</SelectContent>
    </Select></div>
  );
}

function CustomersInner({ theme, setTheme }) {
  const desk = useDesk();
  const [q, setQ] = React.useState('');
  const [kind, setKind] = React.useState(pageParams.get('kind') || 'all');
  const [status, setStatus] = React.useState(STATUSES().some(([k]) => k === pageParams.get('status')) ? pageParams.get('status') : 'all');
  const [pay, setPay] = React.useState(pageParams.get('pay') || 'all');
  // The desk's search rule (K1): a name, or the mobile's last digits.
  const t = q.trim(); const digits = t.replace(/\D/g, ''); const byDigits = digits.length >= 2 && digits === t.replace(/[\s+]/g, '');
  const matches = (c) => !t || c.name.includes(t) || (byDigits && (c.phone || '').replace(/\D/g, '').endsWith(digits));
  const list = DESK.customers.filter((c) => (status === 'archived' ? !!c.archived : !c.archived && (status === 'all' || DESK.customerStatus(c) === status)) && (kind === 'all' || kindOf(c) === kind) && (pay === 'all' || (pay === 'owes' ? DESK.balance(c) > 0 : pay === 'credit' ? DESK.credit(c) > 0 : DESK.balance(c) === 0 && DESK.credit(c) === 0)) && matches(c));
  // DK-013: the row's «⋯» holds the customer's actions in their one order; an archived row, «استرجاع».
  const actions = (c) => (c.archived
    ? (IS_OWNER ? <Button size="sm" variant="outline" onClick={() => desk.restore(c.id)}>{tr('استرجاع', 'Restore')}</Button> : null)
    : (
      <DropdownMenu dir={DIR}>
        <DropdownMenuTrigger asChild><Button variant="ghost" size="icon" aria-label={tr('إجراءات: ', 'Actions: ') + c.name}><EllipsisVerticalIcon /></Button></DropdownMenuTrigger>
        <DropdownMenuContent align="end"><CustomerMenuItems c={c} full /></DropdownMenuContent>
      </DropdownMenu>
    ));
  const sub = (c) => DESK.currentSub(c);
  const until = (s) => (s.to ? tr('حتى ', 'until ') + DESK.fmtDate(s.to) : tr('بلا تاريخ نهاية', 'No end date'));
  // DK-017: five columns from 768 — the phone under the name, the end under the subscription.
  const columns = [
    { id: 'name', header: tr('الاسم', 'Name'), cell: ({ row }) => <span className="flex flex-col"><a className="text-label text-foreground" href={roleQ('Customer file.html?id=' + row.original.id)}>{row.original.name}</a>{row.original.phone ? <span className="text-caption text-muted-foreground"><Ltr>{row.original.phone}</Ltr></span> : null}</span> },
    { id: 'sub', header: tr('الاشتراك', 'Subscription'), cell: ({ row }) => sub(row.original) ? <span className="flex flex-col"><span>{sub(row.original).name}</span><span className="text-caption text-muted-foreground">{until(sub(row.original))}</span></span> : <span className="text-muted-foreground">—</span> },
    { id: 'status', header: tr('الحالة', 'Status'), cell: ({ row }) => <StatusBadge c={row.original} /> },
    { id: 'bal', header: tr('الرصيد', 'Balance'), cell: ({ row }) => DESK.balance(row.original) > 0 || DESK.credit(row.original) > 0 ? <BalanceBadge c={row.original} /> : <span className="text-body-sm text-muted-foreground">{tr('مسدّد', 'Settled')}</span> },
    { id: 'act', header: () => <span className="sr-only">{tr('إجراءات', 'Actions')}</span>, cell: ({ row }) => <div className="flex justify-end">{actions(row.original)}</div> }
  ];
  const paged = usePaged(list);
  const add = () => desk.open('sheet', { mode: 'new' });
  return (
    <OwnerShell current="customers" title={tr('الزبائن', 'Customers')} state={publicState(DESK.present.length, DESK.capacity)} theme={theme} setTheme={setTheme}>
      <DataTable label={tr('زبائن المساحة', 'Customers of the space')} columns={columns} data={paged.rows} getRowId={(r) => r.id} loading={st === 'loading'}
        summary={paged.summary} pagination={paged.nav}
        toolbar={<div className="flex flex-col gap-3">
          <div className="flex flex-col gap-2 md:flex-row md:flex-wrap md:items-center">
            <Input role="searchbox" aria-label={tr('ابحث بالاسم أو آخر أرقام الجوال', 'Search by name or last digits')} placeholder={tr('الاسم أو آخر أرقام الجوال', 'Name or last digits of the mobile')} startIcon={<SearchIcon />} value={q} onChange={(e) => setQ(e.target.value)} className="md:max-w-xs" />
            <FilterSheet count={list.length} active={[kind, pay].filter((x) => x !== 'all').length} onClear={() => { setKind('all'); setPay('all'); }}>
              <Filter label={tr('نوع الاشتراك', 'Subscription type')} value={kind} onChange={setKind} options={[['all', tr('كل الأنواع', 'All types')], ['month', kindLabel.month], ['week', kindLabel.week], ['package', kindLabel.package], ['custom', kindLabel.custom], ['none', kindLabel.none]]} />
              <Filter label={tr('الدفع', 'Payment')} value={pay} onChange={setPay} options={[['all', tr('كل حالات الدفع', 'All payment states')], ['owes', tr('عليه دين', 'Owes money')], ['credit', tr('له رصيد', 'In credit')], ['settled', tr('مسدّد', 'Settled')]]} />
            </FilterSheet>
          </div>
          <div className="flex flex-wrap items-center justify-between gap-3">
            <ToggleGroup type="single" value={status} onValueChange={(v) => v && setStatus(v)} aria-label={tr('تصفية حسب الحالة', 'Filter by status')}>
              {STATUSES().map(([k, l]) => <ToggleGroupItem key={k} value={k}>{l}</ToggleGroupItem>)}
            </ToggleGroup>
            <div className="flex items-center gap-3">
              <ResultCount>{tr('عدد الزبائن', 'Customers')}: <Num>{list.length}</Num></ResultCount>
              <Button onClick={add}>{tr('زبون جديد', 'New customer')}</Button>
            </div>
          </div>
        </div>}
        renderCard={(c) => (
          <div className="flex items-start justify-between gap-3">
            <div className="flex min-w-0 flex-col gap-1">
              <a className="self-start text-label text-foreground" href={roleQ('Customer file.html?id=' + c.id)}>{c.name}</a>
              {c.phone && <span dir="ltr" className="self-start text-caption text-muted-foreground">{c.phone}</span>}
              <span className="text-caption text-muted-foreground">{sub(c) ? <>{sub(c).name} · {until(sub(c))}</> : tr('بدون اشتراك', 'No subscription')}</span>
              <span className="flex flex-wrap gap-2"><StatusBadge c={c} /><BalanceBadge c={c} /></span>
            </div>
            {actions(c)}
          </div>
        )}
        empty={<EmptyState icon={<UsersIcon />} title={status === 'archived' ? tr('لا يوجد زبائن مؤرشفون', 'No archived customers') : DESK.customers.length ? tr('لا يوجد زبائن يطابقون البحث', 'No customers match') : tr('لا يوجد زبائن بعد', 'No customers yet')} description={status === 'archived' ? undefined : DESK.customers.length ? tr('جرّب اسمًا أو رقمًا آخر، أو غيّر الفلاتر.', 'Try another name or number, or change the filters.') : tr('يُضاف الزبون عند أول اشتراك، أو عندما يخرج زائر بدون دفع.', 'Customers are added with their first subscription, or when a visitor leaves without paying.')}>
          {!DESK.customers.length && <Button onClick={add}>{tr('زبون جديد', 'New customer')}</Button>}
        </EmptyState>} />
    </OwnerShell>
  );
}
function CustomersScreen() { const [theme, setTheme] = useTheme(); return <DeskProvider initial={initial}><CustomersInner theme={theme} setTheme={setTheme} /></DeskProvider>; }
ReactDOM.createRoot(document.getElementById('ds-root')).render(<DirectionProvider dir={DIR}><CustomersScreen /></DirectionProvider>);
</script>
```

**Edits — `Customer file.html`**

1. In `FileInner`, replace the `<CardFooter className="flex flex-wrap gap-2">` element (its five buttons and the
   WhatsApp link) with:
```jsx
        <CardFooter className="flex flex-wrap items-center gap-2">
          <CustomerActions c={c} where="file" />
          {c.phone && bal > 0 && <Button variant="ghost" asChild><a href={wa} target="_blank" rel="noopener">{tr('تذكير على واتساب', 'WhatsApp reminder')}</a></Button>}
        </CardFooter>
```
2. Replace the line that starts `function FileScreen() {` with:
```jsx
// DK-014: ?edit=1 opens «تعديل البيانات» (with &taken=1, its PHONE_TAKEN).
const fileInitial = pageParams.get('edit') === '1' ? { kind: 'edit', customerId: c.id, taken: pageParams.get('taken') === '1' } : null;
function FileScreen() { const [theme, setTheme] = useTheme(); return <DeskProvider initial={fileInitial}><FileInner theme={theme} setTheme={setTheme} /></DeskProvider>; }
```

### 3.7 The customer file hides no money — K4, DK-011, DK-016 (commit 7)

| Decision | On screen |
|---|---|
| DK-011 | the first tab «المستحقات والاشتراكات»: a `Card` «زيارات غير مدفوعة» / «تُحسب في رصيده.» of `UnpaidRow`s (date and times, how, the charge, «تحصيل», the owner's «⋯») before the subscriptions; the no-subscription `EmptyState` keeps «هذا الزبون يأتي بزيارات فقط.» only when no visit is owed; a subscription with no end shows «بلا تاريخ نهاية» |
| K4 | «الدفعات» = the subscriptions' payments + `DESK.visitPaysOf(c.id)` (by the visit's customer, never the name); a voided one: `PaidAmount` — struck, «ألغاها أحمد: …» |
| DK-016 / DK-017 | five columns: «التاريخ» (the time under), «عن», «المبلغ» (the method under), «سجّلها», and the owner's «⋯» (`PaymentMenu`: the destructive «إلغاء الدفعة…») on every live payment, visits' included; `VoidDialog` (`ReasonDialog`): «إلغاء الدفعة؟», «50 ₪ · رهف قديح · 15 سبتمبر · تحويل. تبقى ظاهرة مشطوبة مع السبب واسمك، ولا تُحسب في الدخل ولا في التسليم. لا يمكن التراجع.», destructive «إلغاء الدفعة», «رجوع» |

**New strings:** «المستحقات والاشتراكات» / "Dues and subscriptions"; «زيارات غير مدفوعة» / "Unpaid visits";
«تُحسب في رصيده.» / "They count in the balance."; «ألغاها {أحمد}: {reason}» / "Voided by {Ahmad}: {reason}";
«إلغاء الدفعة…» / "Void payment…"; «إلغاء الدفعة؟» / "Void this payment?"; the void's description above /
"It stays visible, struck through, with the reason and your name, and counts in neither income nor the
handover. It can’t be undone."; «إجراءات الدفعة: {50 ₪} · {X}» / "Payment actions: {₪50} · {X}"; toast
«أُلغيت الدفعة {50 ₪}» — «{X} · السبب: …» / "{₪50} payment voided" — "{X} · Reason: …". Removed: «أُلغيت:»,
the plain «إلغاء الدفعة» button, «تبقى ظاهرة مشطوبة مع السبب.» (the old `Dialog`).

**Parameters:** `Customer file.html?void=1` (the newest live payment, owner), `?writeoff=<u>` (owner),
`?tab=subs|att|pays` kept. **States:** `?fail=void`, `?fail=writeoff`.

**Edits — `masaha/desk-data.js`**

1. Replace the line `  // Visits paid today (not tied to a customer): for «دفعاتي اليوم».` with:
```js
  // Visit payments: by name, or through the visit's customer (`customerId`, K4) once it has one.
```
2. Before the line that starts `  visitPays.push({ id: 'ovx',` insert:
```js
  // K4: a visit paid as a customer's (Malek's, on file since an unpaid visit) — reached through the customer.
  visitPays.push({ id: 'vpm14', customerId: 'm14', name: T('مالك صيام', 'Malek Siam'), date: '2026-09-21', time: '17:05', amount: 12, method: 'cash', by: A });
```
3. After the line `  const findCustomer = (id) => customers.find((c) => c.id === id);` insert
   `  const visitPaysOf = (cid) => visitPays.filter((v) => v.customerId === cid);`
4. In the `return`, write `    searchCustomers, visitPaysOf, SETTINGS,` for `    searchCustomers, SETTINGS,`.

**Edits — `masaha/desk-core.jsx`**

1. Insert before the line `    saveCustomer(cid, name, phone) {`:
```jsx
    // DK-016: a void is the owner's, once, with the reason; the payment stays, struck (ADR 0010 rule 3).
    voidPayment(row, reason) {
      if (row.type === 'sub') { row.ref[5] = reason; row.ref[7] = ME; } else { row.ref.voided = reason; row.ref.voidedBy = ME; }
      bump(); close();
      toast.success(tr(`أُلغيت الدفعة ${$(row.amount)}`, `${$(row.amount)} payment voided`), { description: row.who + tr(' · السبب: ', ' · Reason: ') + reason });
    },
```
2. After the provider's `ArchiveDialog` line insert `      <VoidDialog dlg={dlg && dlg.kind === 'void' ? dlg : null} onClose={close} />`
3. Insert before `// DK-012: a visit with no customer (the automatic check-out closed it)`:
```jsx
// K4: a payment's amount — a voided one stays, struck through, with who voided it and why (ADR 0010
// rule 3); `method`: the method under it, as DK-017's five columns put it.
function PaidAmount({ r, method }) {
  return (
    <span className="flex flex-col">
      {r.voided ? <span className="strike text-muted-foreground"><Money n={r.amount} /></span> : <span className="text-label"><Money n={r.amount} /></span>}
      {method && <span className="text-caption text-muted-foreground">{D.methodLabel[r.method]}</span>}
      {r.voided && <span className="text-caption text-muted-foreground">{tr('ألغاها', 'Voided by')} {D.by(r.voidedBy)}: {r.voided}</span>}
    </span>
  );
}
// DK-016: the void sits in the row's «⋯», the destructive item, for the owner, on a payment not voided.
function PaymentMenu({ r }) {
  const desk = useDesk();
  if (!IS_OWNER || r.voided) return null;
  return (
    <DK.DropdownMenu dir={DIR}>
      <DK.DropdownMenuTrigger asChild><DK.Button variant="ghost" size="icon" aria-label={tr('إجراءات الدفعة: ', 'Payment actions: ') + D.money(r.amount) + ' · ' + r.who}><DK.EllipsisVerticalIcon /></DK.Button></DK.DropdownMenuTrigger>
      <DK.DropdownMenuContent align="end"><DK.DropdownMenuItem variant="destructive" onSelect={() => desk.open('void', { row: r })}>{tr('إلغاء الدفعة…', 'Void payment…')}</DK.DropdownMenuItem></DK.DropdownMenuContent>
    </DK.DropdownMenu>
  );
}
// P9 + DK-016: the AlertDialog repeats the amount, the customer and the date, and asks why.
function VoidDialog({ dlg, onClose }) {
  const desk = useDesk();
  const r = dlg && dlg.row;
  return (
    <ReasonDialog open={!!r} onClose={onClose} actionKey="void" title={tr('إلغاء الدفعة؟', 'Void this payment?')} action={tr('إلغاء الدفعة', 'Void payment')} onConfirm={(reason) => desk.voidPayment(r, reason)}
      description={r && <><Money n={r.amount} /> · {r.who} · {D.fmtDate(r.date)} · {D.methodLabel[r.method]}. {tr('تبقى ظاهرة مشطوبة مع السبب واسمك، ولا تُحسب في الدخل ولا في التسليم. لا يمكن التراجع.', 'It stays visible, struck through, with the reason and your name, and counts in neither income nor the handover. It can’t be undone.')}</>} />
  );
}

```
4. In the last line, after `CustomerMenuItems` add `, PaidAmount, PaymentMenu`.

**Edits — `Customer file.html`**

1. Replace from `function SubsTab({ bump }) {` up to `function AttendanceTab()` with:
```jsx
// K4 (DK-011): every amount in the balance is an item here — the unpaid visits first, each to collect.
function SubsTab({ bump }) {
  const [ending, setEnding] = React.useState(pageParams.get('end') ? c.subs[0] : null);
  const endNow = () => { const s = ending; s.to = DESK.TODAY; setEnding(null); bump(); window.MasahaDesignSystem.toast.success(tr('انتهى الاشتراك اليوم', 'Subscription ended today'), { description: s.name }); };
  const visits = DESK.unpaid.filter((u) => u.customerId === c.id);
  return (
    <div className="flex flex-col gap-4">
      {visits.length > 0 && (
        <Card>
          <CardHeader><CardTitle>{tr('زيارات غير مدفوعة', 'Unpaid visits')}</CardTitle><CardDescription>{tr('تُحسب في رصيده.', 'They count in the balance.')}</CardDescription></CardHeader>
          <CardContent className="p-0"><ul className="divide-y">{visits.map((u) => <UnpaidRow key={u.id} u={u} />)}</ul></CardContent>
        </Card>
      )}
      {!c.subs.length && <Card><EmptyState icon={<UsersIcon />} title={tr('لا توجد اشتراكات', 'No subscriptions')} description={visits.length ? undefined : tr('هذا الزبون يأتي بزيارات فقط.', 'This customer only comes for visits.')} /></Card>}
      {c.subs.map((s, i) => { const [pv, pl] = DESK.payBadge[DESK.payStatus(s, c)]; const [sv, sl] = DESK.statusBadge[DESK.subStatus(s)]; return (
        <Card key={s.id}>
          <CardHeader>
            <CardTitle className="flex flex-wrap items-center gap-2">{s.name}{s.manual && <Badge variant="info">{tr('سعر يدوي', 'Manual price')}</Badge>}</CardTitle>
            <CardDescription>{DESK.fmtDate(s.from, true)} – {s.to ? DESK.fmtDate(s.to, true) : tr('بلا تاريخ نهاية', 'No end date')} · {DESK.termsLine(s)}</CardDescription>
            <CardAction className="flex flex-wrap gap-2">{i === 0 && <Badge variant={sv}>{sl}</Badge>}<Badge variant={pv}>{pl}</Badge></CardAction>
          </CardHeader>
          <CardContent className="flex flex-col gap-3">
            <dl className="grid grid-cols-3 gap-3 rounded-lg bg-muted p-3">
              <div className="flex flex-col"><dt className="text-caption text-muted-foreground">{s.billing.type === 'usage' ? tr('المستحق حتى الآن', 'Due so far') : tr('المستحق', 'Due')}</dt><dd className="text-label"><Money n={DESK.due(s, c)} /></dd></div>
              <div className="flex flex-col"><dt className="text-caption text-muted-foreground">{tr('المدفوع', 'Paid')}</dt><dd className="text-label"><Money n={DESK.paid(s)} /></dd></div>
              <div className="flex flex-col"><dt className="text-caption text-muted-foreground">{tr('المتبقي', 'Left')}</dt><dd className="text-label"><Money n={Math.max(0, DESK.due(s, c) - DESK.paid(s))} /></dd></div>
            </dl>
            <ul className="flex flex-col gap-1 text-body-sm text-muted-foreground">{DESK.progress(s, c).map((l, k) => <li key={k}>{l}</li>)}</ul>
            {s.note && <p className="text-body-sm">{tr('ملاحظة:', 'Note:')} {s.note}</p>}
          </CardContent>
          {i === 0 && DESK.subStatus(s) !== 'expired' && s.to !== DESK.TODAY && <CardFooter><Button variant="ghost" size="sm" onClick={() => setEnding(s)}>{tr('إنهاء الاشتراك', 'End subscription')}</Button></CardFooter>}
        </Card>
      ); })}
      <AlertDialog open={!!ending} onOpenChange={(o) => !o && setEnding(null)}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>{tr('إنهاء الاشتراك اليوم؟', 'End the subscription today?')}</AlertDialogTitle>
            <AlertDialogDescription>{ending && <>{ending.name} · {tr('يصبح تاريخ النهاية', 'The end date becomes')} {DESK.fmtDate(DESK.TODAY, true)}{ending.to ? <> {tr('بدل', 'instead of')} {DESK.fmtDate(ending.to, true)}</> : null}. {tr('المبالغ المدفوعة والمستحقة لا تتغيّر.', 'Amounts paid and due don’t change.')}</>}</AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>{tr('رجوع', 'Back')}</AlertDialogCancel>
            <AlertDialogAction variant="destructive" onClick={endNow}>{tr('إنهاء الاشتراك', 'End subscription')}</AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}

```
2. Replace from `function PaymentsTab({ bump }) {` up to `function FileInner(` with:
```jsx
// K4 (DK-011): the customer's payments — the subscriptions', and the visits' through the visit's
// customer, never by name. Each row as Payments draws it, so the void is one dialog.
const filePays = () => {
  const out = [];
  c.subs.forEach((s) => s.pays.forEach((p, i) => out.push({ id: s.id + '-' + i, ref: p, type: 'sub', item: s.name, date: p[0], time: p[1], amount: p[2], method: p[3], by: p[4], voided: p[5] || null, voidedBy: p[7] || null, who: c.name })));
  DESK.visitPaysOf(c.id).forEach((v) => out.push({ id: v.id, ref: v, type: 'visit', item: tr('زيارة', 'Visit'), date: v.date, time: v.time, amount: v.amount, method: v.method, by: v.by, voided: v.voided || null, voidedBy: v.voidedBy || null, who: c.name }));
  return out.sort((a, b) => (a.date + a.time < b.date + b.time ? 1 : -1));
};
// DK-017's five columns: the date (its time under it), the item, the amount (its method under it),
// who recorded it, and the owner's «⋯» (DK-016) — on visit payments too.
function PaymentsTab() {
  const pays = filePays();
  if (!pays.length) return <Card><EmptyState icon={<UsersIcon />} title={tr('لا توجد دفعات بعد', 'No payments yet')} /></Card>;
  return (
    <Card>
      <CardContent className="p-0">
        <Table>
          <TableHeader><TableRow><TableHead>{tr('التاريخ', 'Date')}</TableHead><TableHead>{tr('عن', 'For')}</TableHead><TableHead>{tr('المبلغ', 'Amount')}</TableHead><TableHead>{tr('سجّلها', 'Recorded by')}</TableHead>{IS_OWNER && <TableHead><span className="sr-only">{tr('إجراءات', 'Actions')}</span></TableHead>}</TableRow></TableHeader>
          <TableBody>{pays.map((x) => (
            <TableRow key={x.id}>
              <TableCell><span className="flex flex-col"><span>{DESK.fmtDate(x.date)}</span><span className="text-caption text-muted-foreground"><Num>{x.time}</Num></span></span></TableCell>
              <TableCell>{x.item}</TableCell>
              <TableCell><PaidAmount r={x} method /></TableCell>
              <TableCell>{DESK.by(x.by)}</TableCell>
              {IS_OWNER && <TableCell className="text-end"><PaymentMenu r={x} /></TableCell>}
            </TableRow>
          ))}</TableBody>
        </Table>
      </CardContent>
    </Card>
  );
}

```
3. Quote `          <TabsTrigger value="subs">{tr('الاشتراكات', 'Subscriptions')}</TabsTrigger>` → replace the label with
   `{tr('المستحقات والاشتراكات', 'Dues and subscriptions')}`.
4. Quote `: <PaymentsTab bump={desk.bump} />}` → replace with `: <PaymentsTab />}`.
5. Replace commit 6's two lines (`// DK-014: ?edit=1 opens …` and `const fileInitial = …`) with:
```jsx
// ?edit=1 opens «تعديل البيانات» (DK-014; &taken=1, its PHONE_TAKEN); ?void=1 the void of the first payment
// not voided (owner); ?writeoff=<visit> the owner's «لن يُحصَّل» (K6).
const fileInitial = pageParams.get('edit') === '1' ? { kind: 'edit', customerId: c.id, taken: pageParams.get('taken') === '1' }
  : pageParams.get('void') && IS_OWNER ? { kind: 'void', row: filePays().find((r) => !r.voided) }
  : pageParams.get('writeoff') && IS_OWNER ? { kind: 'writeoff', visitId: pageParams.get('writeoff') } : null;
```

### 3.8 My payments show what was voided — DK-015, K4 (commit 8)

| Decision | On screen |
|---|---|
| DK-015 | a voided payment of Sami's today (Farah, 6 ₪) stays in the list, `PaidAmount` struck with «ألغاها أحمد: سُجّلت بالخطأ»; the figures count only live payments: cash 45 ₪, transfer 59 ₪, total 104 ₪, «4 دفعات»; below 768 one `Card` with three rows «نقدًا للتسليم», «تحويل», «المجموع · 4 دفعات»; from 768 the three `StatCard`s («نقدًا للتسليم» first); the caption «خطأ في دفعة؟ يلغيها صاحب المساحة، وتظهر هنا مشطوبة.» |

**New strings:** «نقدًا للتسليم» / "Cash to hand over"; «خطأ في دفعة؟ يلغيها صاحب المساحة، وتظهر هنا
مشطوبة.» / "A mistake in a payment? The space’s owner voids it, and it shows here struck through.";
F_PAYMENTS «دفعة واحدة · دفعتان · {n} دفعات · {n} دفعة» / "{n} payment(s)". Removed: the cash card's helper
«للتسليم نقدًا».

**Edits — `masaha/desk-data.js`.** Replace the line that starts `    { id: 'vp1', name: T('فرح جابر', 'Farah Jaber'),` with:
```js
    // DK-015: the owner voided one of Sami's today, so the handover shows it struck.
    { id: 'vp1', name: T('فرح جابر', 'Farah Jaber'), date: TODAY, time: '10:02', amount: 6, method: 'cash', by: SM, voided: T('سُجّلت بالخطأ', 'Recorded by mistake'), voidedBy: A },
```
**Edits — `masaha/desk-core.jsx`.** After the line `const F_UNCOLLECTED = …` insert:
```jsx
const F_PAYMENTS = { ar: { zero: 'لا دفعات', one: 'دفعة واحدة', two: 'دفعتان', few: '{n} دفعات', many: '{n} دفعة', other: '{n} دفعة' }, en: ['{n} payment', '{n} payments'] };
```
and in the last line, after `PaymentMenu` add `, F_PAYMENTS`.

**Edit — `My payments.html`.** Replace the inline `<script type="text/babel">` through its `</script>` with:
```html
<script type="text/babel">
const { DirectionProvider, Card, CardContent, StatCard, DataTable, EmptyState, Badge, CircleCheckIcon } = window.MasahaDesignSystem;
// Reception's own payments today, for the end-of-shift handover — a voided one too, struck (DK-015).
function rowsFor(by) {
  const out = [];
  DESK.customers.forEach((c) => c.subs.forEach((s) => s.pays.forEach((p, i) => { if (p[0] === DESK.TODAY && p[4] === by) out.push({ id: s.id + i, time: p[1], who: c.name, item: s.name, amount: p[2], method: p[3], voided: p[5] || null, voidedBy: p[7] || null }); })));
  DESK.visitPays.forEach((v) => { if (v.date === DESK.TODAY && v.by === by) out.push({ id: v.id, time: v.time, who: v.name, item: tr('زيارة', 'Visit'), amount: v.amount, method: v.method, voided: v.voided || null, voidedBy: v.voidedBy || null }); });
  return out.sort((a, b) => (a.time < b.time ? 1 : -1));
}
function MineInner({ theme, setTheme }) {
  const rows = pageParams.get('state') === 'empty' ? [] : rowsFor(DESK.SAMI);
  // ADR 0010 rule 3: a voided payment counts nowhere — not in the figures to hand over.
  const live = rows.filter((r) => !r.voided);
  const sum = (m) => live.filter((r) => !m || r.method === m).reduce((a, r) => a + r.amount, 0);
  const count = <Counted n={live.length} ar={F_PAYMENTS.ar} en={F_PAYMENTS.en} />;
  const paged = usePaged(rows);
  const columns = [
    { id: 'time', header: tr('الوقت', 'Time'), cell: ({ row }) => <Num>{row.original.time}</Num> },
    { id: 'who', header: tr('الاسم', 'Name'), cell: ({ row }) => <span className="text-label">{row.original.who}</span> },
    { id: 'item', header: tr('عن', 'For'), cell: ({ row }) => row.original.item },
    { id: 'method', header: tr('الطريقة', 'Method'), cell: ({ row }) => <Badge variant={row.original.method === 'cash' ? 'neutral' : 'info'}>{DESK.methodLabel[row.original.method]}</Badge> },
    { id: 'amount', header: tr('المبلغ', 'Amount'), cell: ({ row }) => <PaidAmount r={row.original} /> }
  ];
  return (
    <OwnerShell current="my-payments" title={tr('دفعاتي اليوم', 'My payments today')} state={publicState(DESK.present.length, DESK.capacity)} theme={theme} setTheme={setTheme}>
      <p className="text-body-sm text-muted-foreground">{tr('الدفعات التي سجّلتها أنت اليوم، لتسليمها في نهاية الوردية.', 'The payments you recorded today, for the end-of-shift handover.')} · {DESK.fmtDate(DESK.TODAY, true)}</p>
      {/* DK-015: on a phone the three figures are one card, the cash to hand over first. */}
      <Card className="md:hidden"><CardContent><dl className="flex flex-col divide-y">
        <Row k={tr('نقدًا للتسليم', 'Cash to hand over')} v={<Money n={sum('cash')} />} />
        <Row k={tr('تحويل', 'Transfer')} v={<Money n={sum('transfer')} />} />
        <Row k={<>{tr('المجموع', 'Total')} · {count}</>} v={<Money n={sum()} />} />
      </dl></CardContent></Card>
      <div className="hidden gap-4 md:grid md:grid-cols-3">
        <StatCard label={tr('نقدًا للتسليم', 'Cash to hand over')} value={<Money n={sum('cash')} />} />
        <StatCard label={tr('تحويل', 'Transfer')} value={<Money n={sum('transfer')} />} helper={tr('وصلت إلى حساب المساحة', 'Received in the space’s account')} />
        <StatCard label={tr('المجموع', 'Total')} value={<Money n={sum()} />} helper={count} />
      </div>
      <p className="text-caption text-muted-foreground">{tr('خطأ في دفعة؟ يلغيها صاحب المساحة، وتظهر هنا مشطوبة.', 'A mistake in a payment? The space’s owner voids it, and it shows here struck through.')}</p>
      <DataTable label={tr('دفعاتي اليوم', 'My payments today')} columns={columns} data={paged.rows} getRowId={(r) => r.id} loading={pageParams.get('state') === 'loading'}
        summary={paged.summary} pagination={paged.nav}
        renderCard={(r) => (<div className="flex items-start justify-between gap-3"><div className="flex flex-col gap-1"><span className="text-label">{r.who}</span><span className="text-caption text-muted-foreground"><Num>{r.time}</Num> · {r.item} · {DESK.methodLabel[r.method]}</span></div><PaidAmount r={r} /></div>)}
        empty={<EmptyState icon={<CircleCheckIcon />} title={tr('لم تسجّل أي دفعة اليوم', 'You haven’t recorded any payments today')} />} />
    </OwnerShell>
  );
}
function MineScreen() { const [theme, setTheme] = useTheme(); return <DeskProvider><MineInner theme={theme} setTheme={setTheme} /></DeskProvider>; }
ReactDOM.createRoot(document.getElementById('ds-root')).render(<DirectionProvider dir={DIR}><MineScreen /></DirectionProvider>);
</script>
```

### 3.9 Payments: five columns, a month — DK-016, DK-017, A7, DI-36 (commit 9)

| Decision | On screen |
|---|---|
| DK-017 | five columns from 768: «التاريخ» (the time under), «الزبون» (a link when on file; the item under), «المبلغ» (`PaidAmount` with the method), «سجّلها», «⋯» |
| DK-016 | the void in the row's «⋯» (`PaymentMenu`), the card's too; the dialog is the file's `VoidDialog` (in the provider); `?void=1` opens it on the newest live payment |
| A7 | «إظهار الملغاة» is a `ToggleGroup type="multiple"` chip by the count («تصفية سريعة»), not a `Switch` |
| DI-36 | `?month=YYYY-MM` sets the range to that month (to today in the current one); Finance › الديون › «عرض الكل» links `Payments.html?month=<month>` |

**New strings:** «التاريخ» (was «التاريخ والوقت») / "Date"; «تصفية سريعة» / "Quick filter" (the chip group's name,
as Admin spaces); the count «{n} دفعة» now through F_PAYMENTS. Removed: the `Switch` «إظهار الملغاة» field,
the plain «إلغاء الدفعة» buttons, the page's own void `Dialog`.

**Edits — `masaha/desk-data.js`.** In `ledger`, quote `who: v.name, item: T('زيارة', 'Visit'), type: 'visit' }));` →
replace with `who: v.name, customerId: v.customerId || null, item: T('زيارة', 'Visit'), type: 'visit' }));`

**Edit — `Payments.html`.** Replace the inline `<script type="text/babel">` (the one after
`<script type="text/babel" src="masaha/finance.jsx"></script>`) through its `</script>` with:
```html
<script type="text/babel">
const { DirectionProvider, Button, Badge, DataTable, EmptyState, Select, SelectTrigger, SelectValue, SelectContent, SelectItem, Field, ToggleGroup, ToggleGroupItem, CircleCheckIcon, SearchXIcon } = window.MasahaDesignSystem;
const st = pageParams.get('state');
// DI-36: ?month=YYYY-MM — Finance's «عرض الكل» opens its month here (to today in the current one).
const monthRange = (ym) => { const from = dayDate(ym + '-01'); const last = new Date(from); last.setMonth(last.getMonth() + 1); last.setDate(0); return { from, to: ym === DESK.TODAY.slice(0, 7) ? dayDate(DESK.TODAY) : last }; };
const month0 = pageParams.get('month');
const range0 = pageParams.get('range') === 'today' ? { from: dayDate(DESK.TODAY), to: dayDate(DESK.TODAY) }
  : /^\d{4}-\d{2}$/.test(month0 || '') ? monthRange(month0) : { from: dayDate('2026-09-01'), to: dayDate(DESK.TODAY) };
// ?void=1: the void of the newest payment not voided.
const voidInitial = pageParams.get('void') && st !== 'empty' ? { kind: 'void', row: DESK.ledger().find((r) => !r.voided) } : null;

function Pick({ label, value, onChange, options }) {
  return <Field label={label}><Select value={value} onValueChange={onChange}><SelectTrigger><SelectValue /></SelectTrigger><SelectContent>{options.map(([v, l]) => <SelectItem key={v} value={v}>{l}</SelectItem>)}</SelectContent></Select></Field>;
}

function PaymentsInner({ theme, setTheme }) {
  const [range, setRange] = React.useState(range0);
  const [staff, setStaff] = React.useState(pageParams.get('staff') || 'all'); const [method, setMethod] = React.useState('all'); const [type, setType] = React.useState('all');
  const [showVoid, setShowVoid] = React.useState(pageParams.get('voided') === '1');
  const all = st === 'empty' ? [] : DESK.ledger();
  const rows = all.filter((r) => inRange(r.date, range) && (staff === 'all' || r.by === staff) && (method === 'all' || r.method === method) && (type === 'all' || r.type === type) && (showVoid || !r.voided));
  const live = rows.filter((r) => !r.voided);
  const sum = (m) => live.filter((r) => !m || r.method === m).reduce((a, r) => a + r.amount, 0);
  const exportCsv = () => downloadCSV('masaha-payments', [tr('التاريخ', 'Date'), tr('الوقت', 'Time'), tr('الاسم', 'Name'), tr('عن', 'For'), tr('المبلغ', 'Amount'), tr('الطريقة', 'Method'), tr('سجّلها', 'Recorded by'), tr('ملغاة', 'Voided')], rows.map((r) => [r.date, r.time, r.who, r.item, r.amount, DESK.methodLabel[r.method], DESK.by(r.by), r.voided || '']));
  const paged = usePaged(rows);
  // DK-017: five columns from 768 — the time under the date, the item under the customer, the method
  // under the amount; DK-016: the void in the row's «⋯».
  const columns = [
    { id: 'date', header: tr('التاريخ', 'Date'), cell: ({ row }) => <span className="flex flex-col"><span>{DESK.fmtDate(row.original.date)}</span><span className="text-caption text-muted-foreground"><Num>{row.original.time}</Num></span></span> },
    { id: 'who', header: tr('الزبون', 'Customer'), cell: ({ row }) => <span className="flex flex-col">{row.original.customerId ? <a className="text-foreground" href={'Customer file.html?id=' + row.original.customerId}>{row.original.who}</a> : <span>{row.original.who}</span>}<span className="text-caption text-muted-foreground">{row.original.item}</span></span> },
    { id: 'amount', header: tr('المبلغ', 'Amount'), cell: ({ row }) => <PaidAmount r={row.original} method /> },
    { id: 'by', header: tr('سجّلها', 'Recorded by'), cell: ({ row }) => DESK.by(row.original.by) },
    { id: 'act', header: () => <span className="sr-only">{tr('إجراءات', 'Actions')}</span>, cell: ({ row }) => <div className="flex justify-end"><PaymentMenu r={row.original} /></div> }
  ];
  return (
    <OwnerShell current="payments" title={tr('الدفعات', 'Payments')} state={publicState(DESK.present.length, DESK.capacity)} theme={theme} setTheme={setTheme} actions={[{ key: 'csv', label: tr('تصدير CSV', 'Export CSV'), onClick: exportCsv }]}>
      <DataTable label={tr('سجل الدفعات', 'Payments ledger')} columns={columns} data={paged.rows} getRowId={(r) => r.id} loading={st === 'loading'}
        summary={paged.summary} pagination={paged.nav}
        toolbar={<div className="flex flex-col gap-3">
          <FilterSheet count={rows.length} active={[staff, method, type].filter((x) => x !== 'all').length} onClear={() => { setStaff('all'); setMethod('all'); setType('all'); }}><div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
            <RangePicker value={range} onChange={setRange} />
            <Pick label={tr('الموظف', 'Staff')} value={staff} onChange={setStaff} options={[['all', tr('كل الموظفين', 'All staff')], [DESK.AHMAD, DESK.by(DESK.AHMAD)], [DESK.SAMI, DESK.by(DESK.SAMI)]]} />
            <Pick label={tr('الطريقة', 'Method')} value={method} onChange={setMethod} options={[['all', tr('كل الطرق', 'All methods')], ['cash', DESK.methodLabel.cash], ['transfer', DESK.methodLabel.transfer]]} />
            <Pick label={tr('النوع', 'Type')} value={type} onChange={setType} options={[['all', tr('كل الأنواع', 'All types')], ['visit', tr('زيارات', 'Visits')], ['sub', tr('اشتراكات', 'Subscriptions')]]} />
          </div></FilterSheet>
          {/* A7: a switch is not a filter field — «إظهار الملغاة» is a chip by the count. */}
          <div className="flex flex-wrap items-center justify-between gap-3">
            <ToggleGroup type="multiple" value={showVoid ? ['voided'] : []} onValueChange={(v) => setShowVoid(v.includes('voided'))} aria-label={tr('تصفية سريعة', 'Quick filter')}><ToggleGroupItem value="voided">{tr('إظهار الملغاة', 'Show voided')}</ToggleGroupItem></ToggleGroup>
            <ResultCount><span className="flex flex-wrap gap-x-4 gap-y-1"><span className="text-label">{tr('المجموع', 'Total')} <Money n={sum()} /></span><span>{DESK.methodLabel.cash} <Money n={sum('cash')} /></span><span>{DESK.methodLabel.transfer} <Money n={sum('transfer')} /></span><span><Counted n={live.length} ar={F_PAYMENTS.ar} en={F_PAYMENTS.en} /></span></span></ResultCount>
          </div>
        </div>}
        renderCard={(r) => (
          <div className="flex items-start justify-between gap-3">
            <div className="flex min-w-0 flex-col gap-1">
              <span className="text-label">{r.who}</span>
              <span className="text-caption text-muted-foreground">{DESK.fmtDate(r.date)} · <Num>{r.time}</Num> · {r.item} · {DESK.methodLabel[r.method]} · {DESK.by(r.by)}</span>
              <PaidAmount r={r} />
            </div>
            <PaymentMenu r={r} />
          </div>
        )}
        empty={<EmptyState icon={all.length ? <SearchXIcon /> : <CircleCheckIcon />} title={all.length ? tr('لا توجد دفعات تطابق الفلاتر', 'No payments match the filters') : tr('لا توجد دفعات بعد', 'No payments yet')} description={all.length ? tr('غيّر الفترة أو الفلاتر.', 'Change the period or filters.') : tr('تظهر هنا كل دفعة تُسجَّل في مكتب الاستقبال.', 'Every payment recorded at the front desk shows up here.')} />} />
    </OwnerShell>
  );
}
function PaymentsScreen() { const [theme, setTheme] = useTheme(); return <DeskProvider initial={voidInitial}><PaymentsInner theme={theme} setTheme={setTheme} /></DeskProvider>; }
ReactDOM.createRoot(document.getElementById('ds-root')).render(<DirectionProvider dir={DIR}><PaymentsScreen /></DirectionProvider>);
</script>
```

**Edit — `Finance.html`** (batch 5's file; DI-36's one line). In `DebtsTab`, quote
`<a href="Payments.html">{tr('عرض الكل', 'View all')}</a>` → replace with
`<a href={'Payments.html?month=' + month}>{tr('عرض الكل', 'View all')}</a>`. Nothing else in the file changes.

### 3.10 The board and the index (commit 10)

**`Flows - states.html`.** After the last frame of batch 5's section (the line whose label is «Audit log · the
space's — desktop 1440», at top 157650) and before `</body>`, add these 38 lines exactly (the section, then 37
frames; `src` with `%20`, `&amp;` and the Arabic percent-encoded, as the board's newer frames):

```html
<div class="section" style="left:40px;top:160000px"><h2>Batch 6 — the front desk</h2><p>One search, here first · one money block · the old debt first · no hidden money · a write-off with a reason · customers by state · the week as a count</p></div>
<div class="frame" style="left:40px;top:160090px"><p>Desk · one search, here first — desktop 1440</p><iframe loading="lazy" src="Desk.html?role=reception&amp;q=%D9%84%D9%85%D9%89" width="1440" height="1000" title="Desk · one search, here first — desktop 1440"></iframe></div>
<div class="frame" style="left:1512px;top:160090px"><p>Desk · one search, here first — phone 390</p><iframe loading="lazy" src="Desk.html?role=reception&amp;q=%D9%84%D9%85%D9%89" width="390" height="844" title="Desk · one search, here first — phone 390"></iframe></div>
<div class="frame" style="left:1982px;top:160090px"><p>Desk · nothing found: the visit leads — phone 390</p><iframe loading="lazy" src="Desk.html?role=reception&amp;q=%D8%B3%D9%84%D9%8A%D9%85" width="390" height="844" title="Desk · nothing found: the visit leads — phone 390"></iframe></div>
<div class="frame" style="left:2452px;top:160090px"><p>Desk · ordered for the phone — phone 390</p><iframe loading="lazy" src="Desk.html?role=reception" width="390" height="844" title="Desk · ordered for the phone — phone 390"></iframe></div>
<div class="frame" style="left:2922px;top:160090px"><p>Desk · a mobile's last digits — phone 390</p><iframe loading="lazy" src="Desk.html?role=reception&amp;q=1006" width="390" height="844" title="Desk · a mobile's last digits — phone 390"></iframe></div>
<div class="frame" style="left:40px;top:161170px"><p>Desk · every uncollected row, the owner's «⋯» — desktop 1440</p><iframe loading="lazy" src="Desk.html?unpaid=all" width="1440" height="1000" title="Desk · every uncollected row, the owner's «⋯» — desktop 1440"></iframe></div>
<div class="frame" style="left:1512px;top:161170px"><p>Write-off · a reason, never a payment (owner) — phone 390</p><iframe loading="lazy" src="Desk.html?writeoff=u2" width="390" height="844" title="Write-off · a reason, never a payment (owner) — phone 390"></iframe></div>
<div class="frame" style="left:1982px;top:161170px"><p>Uncollected · a debt by name and mobile — phone 390</p><iframe loading="lazy" src="Desk.html?role=reception&amp;dialog=debt&amp;vid=u3" width="390" height="844" title="Uncollected · a debt by name and mobile — phone 390"></iframe></div>
<div class="frame" style="left:2452px;top:161170px"><p>Uncollected · collect a visit with no customer — phone 390</p><iframe loading="lazy" src="Desk.html?role=reception&amp;dialog=pay&amp;vid=u3" width="390" height="844" title="Uncollected · collect a visit with no customer — phone 390"></iframe></div>
<div class="frame" style="left:2922px;top:161170px"><p>Desk · landed from the overview's queue — phone 390</p><iframe loading="lazy" src="Desk.html#unpaid" width="390" height="844" title="Desk · landed from the overview's queue — phone 390"></iframe></div>
<div class="frame" style="left:40px;top:162250px"><p>Check-out · more handed over: the change — desktop 1440</p><iframe loading="lazy" src="Desk.html?role=reception&amp;dialog=checkout&amp;pid=pv0&amp;received=20" width="1440" height="1000" title="Check-out · more handed over: the change — desktop 1440"></iframe></div>
<div class="frame" style="left:1512px;top:162250px"><p>Check-out · leaves owing, the mobile asked — phone 390</p><iframe loading="lazy" src="Desk.html?role=reception&amp;dialog=checkout&amp;pid=pv0&amp;received=5" width="390" height="844" title="Check-out · leaves owing, the mobile asked — phone 390"></iframe></div>
<div class="frame" style="left:1982px;top:162250px"><p>Check-out · a visit as the customer, nothing paid — phone 390</p><iframe loading="lazy" src="Desk.html?role=reception&amp;dialog=checkout&amp;pid=pv5&amp;received=0" width="390" height="844" title="Check-out · a visit as the customer, nothing paid — phone 390"></iframe></div>
<div class="frame" style="left:2452px;top:162250px"><p>Check-out · billed from attendance — phone 390</p><iframe loading="lazy" src="Desk.html?role=reception&amp;dialog=checkout&amp;pid=ps2" width="390" height="844" title="Check-out · billed from attendance — phone 390"></iframe></div>
<div class="frame" style="left:2922px;top:162250px"><p>Check-out · a fixed-price subscriber, one tap — phone 390</p><iframe loading="lazy" src="Desk.html?role=reception&amp;dialog=checkout&amp;pid=ps0" width="390" height="844" title="Check-out · a fixed-price subscriber, one tap — phone 390"></iframe></div>
<div class="frame" style="left:40px;top:163330px"><p>Visit · the shift now, the rate named — desktop 1440</p><iframe loading="lazy" src="Desk.html?role=reception&amp;dialog=visit&amp;vname=%D8%B3%D9%84%D9%8A%D9%85" width="1440" height="1000" title="Visit · the shift now, the rate named — desktop 1440"></iframe></div>
<div class="frame" style="left:1512px;top:163330px"><p>Visit · student prices, no shifts — phone 390</p><iframe loading="lazy" src="Desk.html?role=reception&amp;dialog=visit&amp;demo=noshifts,studentprices" width="390" height="844" title="Visit · student prices, no shifts — phone 390"></iframe></div>
<div class="frame" style="left:1982px;top:163330px"><p>Check-in · this week's days used up — phone 390</p><iframe loading="lazy" src="Desk.html?role=reception&amp;dialog=warn&amp;cid=m12" width="390" height="844" title="Check-in · this week's days used up — phone 390"></iframe></div>
<div class="frame" style="left:2452px;top:163330px"><p>Check-out · a retry that is safe — phone 390</p><iframe loading="lazy" src="Desk.html?role=reception&amp;dialog=checkout&amp;pid=pv0&amp;fail=checkout" width="390" height="844" title="Check-out · a retry that is safe — phone 390"></iframe></div>
<div class="frame" style="left:2922px;top:163330px"><p>Check-out · too many attempts — phone 390</p><iframe loading="lazy" src="Desk.html?role=reception&amp;dialog=checkout&amp;pid=pv0&amp;state=ratelimit" width="390" height="844" title="Check-out · too many attempts — phone 390"></iframe></div>
<div class="frame" style="left:40px;top:164410px"><p>Renewal · the old debt first, one total — desktop 1440</p><iframe loading="lazy" src="Customers.html?role=reception&amp;renew=m6" width="1440" height="1000" title="Renewal · the old debt first, one total — desktop 1440"></iframe></div>
<div class="frame" style="left:1512px;top:164410px"><p>Renewal · the old debt first — phone 390</p><iframe loading="lazy" src="Customers.html?role=reception&amp;renew=m6" width="390" height="844" title="Renewal · the old debt first — phone 390"></iframe></div>
<div class="frame" style="left:1982px;top:164410px"><p>New customer · one step — phone 390</p><iframe loading="lazy" src="Desk.html?role=reception&amp;dialog=sheet&amp;mode=new&amp;name=%D8%B3%D9%84%D9%8A%D9%85" width="390" height="844" title="New customer · one step — phone 390"></iframe></div>
<div class="frame" style="left:2452px;top:164410px"><p>Custom · no end, no limit — phone 390</p><iframe loading="lazy" src="Desk.html?role=reception&amp;dialog=sheet&amp;mode=subscribe&amp;cid=m3&amp;pkg=custom" width="390" height="844" title="Custom · no end, no limit — phone 390"></iframe></div>
<div class="frame" style="left:2922px;top:164410px"><p>Sheet · saved, the payment failed — phone 390</p><iframe loading="lazy" src="Desk.html?role=reception&amp;dialog=sheet&amp;mode=renew&amp;cid=m7&amp;fail=sheet-pay&amp;half=1" width="390" height="844" title="Sheet · saved, the payment failed — phone 390"></iframe></div>
<div class="frame" style="left:40px;top:165490px"><p>Receive payment · the amount on the button — phone 390</p><iframe loading="lazy" src="Desk.html?role=reception&amp;dialog=pay&amp;cid=m6" width="390" height="844" title="Receive payment · the amount on the button — phone 390"></iframe></div>
<div class="frame" style="left:510px;top:165490px"><p>Customer file · actions by state — phone 390</p><iframe loading="lazy" src="Customer%20file.html?id=m6" width="390" height="844" title="Customer file · actions by state — phone 390"></iframe></div>
<div class="frame" style="left:980px;top:165490px"><p>Edit details · the mobile taken — phone 390</p><iframe loading="lazy" src="Customer%20file.html?id=m6&amp;edit=1&amp;taken=1" width="390" height="844" title="Edit details · the mobile taken — phone 390"></iframe></div>
<div class="frame" style="left:1450px;top:165490px"><p>Customers · archived, «استرجاع» (owner) — phone 390</p><iframe loading="lazy" src="Customers.html?status=archived" width="390" height="844" title="Customers · archived, «استرجاع» (owner) — phone 390"></iframe></div>
<div class="frame" style="left:1920px;top:165490px"><p>My payments · a void struck, one card — phone 390</p><iframe loading="lazy" src="My%20payments.html?role=reception" width="390" height="844" title="My payments · a void struck, one card — phone 390"></iframe></div>
<div class="frame" style="left:2390px;top:165490px"><p>Payments · void: the reason (owner) — phone 390</p><iframe loading="lazy" src="Payments.html?void=1" width="390" height="844" title="Payments · void: the reason (owner) — phone 390"></iframe></div>
<div class="frame" style="left:40px;top:166414px"><p>Customer file · unpaid visits first — desktop 1440</p><iframe loading="lazy" src="Customer%20file.html?id=m14" width="1440" height="1000" title="Customer file · unpaid visits first — desktop 1440"></iframe></div>
<div class="frame" style="left:1512px;top:166414px"><p>Customer file · the visit's payment, the void in «⋯» — desktop 1440</p><iframe loading="lazy" src="Customer%20file.html?id=m14&amp;tab=pays" width="1440" height="1000" title="Customer file · the visit's payment, the void in «⋯» — desktop 1440"></iframe></div>
<div class="frame" style="left:40px;top:167494px"><p>Customers · five columns, status chips — tablet 768</p><iframe loading="lazy" src="Customers.html" width="768" height="1024" title="Customers · five columns, status chips — tablet 768"></iframe></div>
<div class="frame" style="left:888px;top:167494px"><p>Payments · five columns, voided shown — tablet 768</p><iframe loading="lazy" src="Payments.html?range=today&amp;voided=1" width="768" height="1024" title="Payments · five columns, voided shown — tablet 768"></iframe></div>
<div class="frame" style="left:1736px;top:167494px"><p>Payments · a month from Finance — desktop 1440</p><iframe loading="lazy" src="Payments.html?month=2026-08" width="1440" height="1000" title="Payments · a month from Finance — desktop 1440"></iframe></div>
<div class="frame" style="left:40px;top:168598px"><p>My payments · the handover — desktop 1440</p><iframe loading="lazy" src="My%20payments.html?role=reception" width="1440" height="1000" title="My payments · the handover — desktop 1440"></iframe></div>
```

The frames, for reading: row 1 (top 160090) the search; row 2 (161170) the uncollected visits; row 3 (162250)
check-out; row 4 (163330) the visit dialog, the week's warning, the failures; row 5 (164410) the sheet; row 6
(165490, phones only, 470 px apart from 40) payment, the file, editing, archived, my payments, void; row 7 (166414)
the file at 1440; row 8 (167494) Customers and Payments at **768 × 1024**, a month at 1440; row 9 (168598) my
payments at 1440. No frame overlaps another or batch 5's last row (157650 + 1035).

**Relabels (S8)** — in the board (each old label appears in two lines, twice per line: `<p>` and `title`) and in
`INDEX.md` (two rows each), replace every occurrence of the left text with the right; nothing else in those lines:

| Old text | New text |
|---|---|
| `Desk · no result → «زبون جديد باسم …»` | `Desk · no result → «تسجيل زيارة باسم …»` |
| `Not one of his days` | `This week’s days used up` |
| `Subscriber · monthly` | `Subscriber · monthly → one tap, no dialog` |
| `Step 1 · customer` | `New customer · one step` |
| `Step 2 · package + partial payment` | `Renewal · a partial payment` |
| `Step 2 · «مخصّص»` | `«مخصّص» · no end, no limit` |

**`INDEX.md`**

1. After the *Batch 5* parameters table (`### Batch 5 — the owner's management` and its rows), add:
```markdown
### Batch 6 — the front desk

| Parameter | Where | What it shows |
|---|---|---|
| `Desk.html?q=<text>` | the desk | the one search: «حاضر الآن» first, then the customers, then «تسجيل زيارة باسم «…»» and «زبون جديد باسم «…»» (K1); two digits or more match a mobile's end |
| `?dialog=checkout&pid=<id>&received=<₪>` | the desk | the check-out's money block with that amount received: less → the debt line (and the mobile, for a visit with no customer), more → the change. `&debt=1` is `received=0`. A fixed-price subscriber's `pid` (`ps0`) checks out on load, as the one tap does |
| `?dialog=pay&vid=<visit>` · `?dialog=debt&vid=<visit>` | the desk | an uncollected visit with no customer: collected on the visit, or recorded as a debt by name and mobile (DK-012) |
| `?writeoff=<visit>` | `Desk.html`, `Customer file.html` (owner) | «لن يُحصَّل»: its reason asked (K6) |
| `?unpaid=all` · `Desk.html#unpaid` | the desk | the uncollected card with every row; the card, where the overview's queue lands (DI-35) |
| `?dialog=visit&vname=<name>` | the desk | the visit dialog with the name carried |
| `?demo=noshifts` · `studentprices` · `nostudent` · `nocap` | the desk's pages | no shift saved (no «الوردية»); a student hour and day price, 2 ₪ and 10 ₪ («طالب» shows); student prices for visits off; the day-price cap off — a comma list, as on the owner's pages |
| `?fail=sheet` · `?fail=sheet-pay&half=1` | the subscription sheet | the save failing; the subscription saved and its payment not, retried alone (DK-018) |
| `?fail=checkout` · `pay` · `visit` · `debt` · `writeoff` · `void` · `edit` | the desk's dialogs | that action failing inside its dialog; money's says a retry is safe |
| `?state=ratelimit` | the desk's money dialogs | the 429 inside the dialog: nothing was recorded, a retry is safe |
| `Customers.html?status=archived` | Customers (owner) | «مؤرشف»: the archived customers with «استرجاع» (DK-014); `active` · `soon` · `expired` the other chips |
| `Customers.html?edit=<id>` · `Customer file.html?edit=1` | the customer | «تعديل البيانات»; `&taken=1` its PHONE_TAKEN on the mobile |
| `Customer file.html?void=1` · `Payments.html?void=1` | owner | the void's `AlertDialog` for the newest payment not voided (the void is in the row's «⋯») |
| `Payments.html?month=2026-08` | Payments | one month, as Finance's «عرض الكل» opens it (DI-36) |
```
2. At the end of the file, after §55's table, add section 56, exactly:
```markdown
## 56 · Batch 6 — the front desk

Added by the desk's fix (`CHANGES.md` › *Batch 6*). No screenshot yet: `screens/` is regenerated once, at the end of the fix phase.

| Frame | Prototype URL | Viewport | Screenshot |
|---|---|---|---|
| Desk · one search, here first — desktop 1440 | `Desk.html?role=reception&q=لمى` | 1440×1000 | — |
| Desk · one search, here first — phone 390 | `Desk.html?role=reception&q=لمى` | 390×844 | — |
| Desk · nothing found: the visit leads — phone 390 | `Desk.html?role=reception&q=سليم` | 390×844 | — |
| Desk · ordered for the phone — phone 390 | `Desk.html?role=reception` | 390×844 | — |
| Desk · a mobile's last digits — phone 390 | `Desk.html?role=reception&q=1006` | 390×844 | — |
| Desk · every uncollected row, the owner's «⋯» — desktop 1440 | `Desk.html?unpaid=all` | 1440×1000 | — |
| Write-off · a reason, never a payment (owner) — phone 390 | `Desk.html?writeoff=u2` | 390×844 | — |
| Uncollected · a debt by name and mobile — phone 390 | `Desk.html?role=reception&dialog=debt&vid=u3` | 390×844 | — |
| Uncollected · collect a visit with no customer — phone 390 | `Desk.html?role=reception&dialog=pay&vid=u3` | 390×844 | — |
| Desk · landed from the overview's queue — phone 390 | `Desk.html#unpaid` | 390×844 | — |
| Check-out · more handed over: the change — desktop 1440 | `Desk.html?role=reception&dialog=checkout&pid=pv0&received=20` | 1440×1000 | — |
| Check-out · leaves owing, the mobile asked — phone 390 | `Desk.html?role=reception&dialog=checkout&pid=pv0&received=5` | 390×844 | — |
| Check-out · a visit as the customer, nothing paid — phone 390 | `Desk.html?role=reception&dialog=checkout&pid=pv5&received=0` | 390×844 | — |
| Check-out · billed from attendance — phone 390 | `Desk.html?role=reception&dialog=checkout&pid=ps2` | 390×844 | — |
| Check-out · a fixed-price subscriber, one tap — phone 390 | `Desk.html?role=reception&dialog=checkout&pid=ps0` | 390×844 | — |
| Visit · the shift now, the rate named — desktop 1440 | `Desk.html?role=reception&dialog=visit&vname=سليم` | 1440×1000 | — |
| Visit · student prices, no shifts — phone 390 | `Desk.html?role=reception&dialog=visit&demo=noshifts,studentprices` | 390×844 | — |
| Check-in · this week's days used up — phone 390 | `Desk.html?role=reception&dialog=warn&cid=m12` | 390×844 | — |
| Check-out · a retry that is safe — phone 390 | `Desk.html?role=reception&dialog=checkout&pid=pv0&fail=checkout` | 390×844 | — |
| Check-out · too many attempts — phone 390 | `Desk.html?role=reception&dialog=checkout&pid=pv0&state=ratelimit` | 390×844 | — |
| Renewal · the old debt first, one total — desktop 1440 | `Customers.html?role=reception&renew=m6` | 1440×1000 | — |
| Renewal · the old debt first — phone 390 | `Customers.html?role=reception&renew=m6` | 390×844 | — |
| New customer · one step — phone 390 | `Desk.html?role=reception&dialog=sheet&mode=new&name=سليم` | 390×844 | — |
| Custom · no end, no limit — phone 390 | `Desk.html?role=reception&dialog=sheet&mode=subscribe&cid=m3&pkg=custom` | 390×844 | — |
| Sheet · saved, the payment failed — phone 390 | `Desk.html?role=reception&dialog=sheet&mode=renew&cid=m7&fail=sheet-pay&half=1` | 390×844 | — |
| Receive payment · the amount on the button — phone 390 | `Desk.html?role=reception&dialog=pay&cid=m6` | 390×844 | — |
| Customer file · actions by state — phone 390 | `Customer file.html?id=m6` | 390×844 | — |
| Edit details · the mobile taken — phone 390 | `Customer file.html?id=m6&edit=1&taken=1` | 390×844 | — |
| Customers · archived, «استرجاع» (owner) — phone 390 | `Customers.html?status=archived` | 390×844 | — |
| My payments · a void struck, one card — phone 390 | `My payments.html?role=reception` | 390×844 | — |
| Payments · void: the reason (owner) — phone 390 | `Payments.html?void=1` | 390×844 | — |
| Customer file · unpaid visits first — desktop 1440 | `Customer file.html?id=m14` | 1440×1000 | — |
| Customer file · the visit's payment, the void in «⋯» — desktop 1440 | `Customer file.html?id=m14&tab=pays` | 1440×1000 | — |
| Customers · five columns, status chips — tablet 768 | `Customers.html` | 768×1024 | — |
| Payments · five columns, voided shown — tablet 768 | `Payments.html?range=today&voided=1` | 768×1024 | — |
| Payments · a month from Finance — desktop 1440 | `Payments.html?month=2026-08` | 1440×1000 | — |
| My payments · the handover — desktop 1440 | `My payments.html?role=reception` | 1440×1000 | — |
```
3. The six relabels above, in their rows.

**`README.md`.** Count, do not add: `grep -c 'class="frame"' "docs/design/prototype/Flows - states.html"` and
`grep -c 'class="section"' …`; write those in the `INDEX.md` row of *What is here* («(N frames in M sections)»).
After #76 merges as planned the result is **570 frames in 56 sections**; if the count differs, write the count.
The pages' count (41) and the screenshots' (437) do not change.

**`SCREENS.md`.** In rows 13, 14, 15, 16 and 17 of *Owner and reception dashboard*, append `, 56` to the board-sections
column (row 13 then ends `… 50, 51, 52, 56 |`).

---

## 4. Stronger decisions and design issues (the owner answers before the build)

### Stronger decisions (built as recommended unless the reply says otherwise)

| | What | Why | Cost | Recommend |
|---|---|---|---|---|
| **S1** | «طالب» shows only where it changes the rate: the setting on **and** a student hour or day price published. Focus Hub publishes only a student month, so the switch is hidden by default; `?demo=studentprices` (2 ₪ / 10 ₪) shows it and the rate it names | DK-023 says "when student visit prices are on"; with no student visit price the switch would record an audience that changes nothing (the data model's fallback for this case is in doubt: DI-41) | none | **yes** · *no:* `STUDENT_VISITS = SETTINGS.studentVisits` in `desk-data.js` (one line) and the rate line keeps the general rate |
| **S2** | K5's words are neutral: «استُنفدت أيام هذا الأسبوع» with «هذا الأسبوع 3 من 3» | «استنفد أيامه» is masculine; the sample's subscriber is Mayar, and the model holds no gender | none | **yes** · *no:* the title `tr('استنفد أيامه هذا الأسبوع', …)` |
| **S3** | K3's warning is neutral: «مستحق من قبل 150 ₪ · اشتراك سبتمبر» | DK-005's «عليها» needs a gender the model does not hold | none | **yes** · *no:* «عليه 150 ₪ من اشتراك سبتمبر» (the old masculine) |
| **S4** | «الطريقة» is hidden while nothing is received; «لم يدفع شيئًا» hides once the amount is 0; «استلام دفعة» has no «لم يدفع شيئًا» | at 0 there is no method to record; in «استلام دفعة» there is nothing to leave unpaid | none | **yes** · *no:* always show both |
| **S5** | In «استلام دفعة», more than is owed is **change** (recorded: what is owed), not the old error «أكبر من المتبقي» — except a usage-based subscription chosen alone, which takes it as credit | K2's live line covers it; ADR 0010 rule 4 (credit only on usage) and the ledger's ceiling | none | **yes** |
| **S6** | The old `?dialog=checkout&pid=ps0` checks Mohammed out on load (the toast shows) | the dialog no longer exists for him (DK-010); the old frame then shows what the tap does | none | **yes** · *no:* the URL opens nothing |
| **S7** | A digits-only search offers «تسجيل زيارة» and «زبون جديد بهذا الرقم», carrying the digits into «رقم الجوال» | K1 carries what was typed; a number is not a name | none | **yes** · *no:* carry the digits as a name |
| **S8** | **Relabel the board's twelve desk frames whose state moved** (§3.10's table), as batch 5 relabelled eight; URLs and screenshot links unchanged | their labels would be untrue («Step 1», «Not one of his days», «Subscriber · monthly» now a tap) | none | **yes** · *no:* leave them (they are not this batch's frames) |
| **S9** | The uncollected card's three-row disclosure applies **at every width**, the side column too | one behaviour; four rows already make a long side column | none | **yes** · *no:* show every row from 1280 |
| **S10** | «عرض الكل» carries no count in parentheses | batch 5 removed «( 2 )»; the title already counts | none | **yes** |
| **S11** | The sample changes to show the states: four uncollected visits (Yazan's and Iyad's with no customer); a voided payment of Sami's today (Farah, 6 ₪, by Ahmad); Ahmad Al-Shawa present as a visit **as the customer** in place of «ريم بكر» (the count stays 27); Mayar's «3 أيام بالأسبوع»; an archived customer (Abeer); a visit payment of Malek's through his `customerId` | each decision needs a frame that is true without a demo flag | small | **yes** |
| **S12** | One search rule everywhere: a name, or two digits or more that are the whole term, matching a mobile's end — on the desk, the payment picker (was 3) and Customers (was digits inside any term) | K1 says one search; three rules found different people | none | **yes** |
| **S13** | «مؤرشف» is the owner's chip; reception has no way to list archived customers | archiving and restoring are the owner's (the proposed ADR 0009 rows) | none | **yes** · *no:* reception sees the chip without «استرجاع» |
| **S14** | The usage-based subscriber's check-out is filled with what is owed so far (the balance), and «لم يدفع شيئًا» leaves it on the subscription | K2: "filled with what is due"; DK-010's «المستحق حتى الآن 63 ₪» | none | **yes** |
| **S15** | The void becomes an `AlertDialog` with its reason (one `ReasonDialog`, shared with K6's write-off), on Payments and in the file | DK-016/§2.5 say `AlertDialog`; the pages each had their own `Dialog` | none | **yes** |
| **S16** | The board gains its **first 768 frames** (Customers, Payments) | DK-017 is about 768; foundation §13's amendment checks lists at 768 | none | **yes** |
| **S17** | `SCREENS.md`'s rows 13–17 name section 56 | the prompt lists `CHANGES`, `INDEX`, the board and README; SCREENS points each screen to its board sections, and would otherwise omit this batch | none | **yes** · *no:* leave SCREENS |

**Under each answer:** "approve S1–S17" → build as written. Any *no* → the change in its row's last column, nothing
else.

### Design issues (recorded; none is built unless the reply says so)

| | Issue | Better | Level | Recommend |
|---|---|---|---|---|
| **DI-41** | The data model says a student visit takes "the hour and day prices of its audience"; when the space publishes no student hour or day price, the rate is undefined | The model's *Visit charge* says each missing student price falls back to the general one (as this plan's `visitRates` does) | docs (data model) | Record for the docs, with step 7 |
| **DI-42** | The owner's audit sample (`owner-data.js`, batch 5's) has no write-off (`visit_written_off`) and no void today | The audit names K6's act when the API has it | web/API (step 7) | Record; not this batch's file |
| **DI-43** | `Sheet side="end"` stays ¾ wide at 390 (DK-024/OW-010, as DI-39) | full width below `md` | design system | Record (worker A) |
| **DI-44** | The desk's capacity is fixed (`DESK.capacity` 40); the owner's `?demo=nocapacity` sets only `OWNER.capacity`, so the desk still says «27 / 40» there | one capacity in the sample | prototype | Record for a later item |
| **DI-45** | The sample's customers carry `student: true` (Rahaf), but a Customer has no audience in the model; «تسجيل كزيارة» uses it | the visit's audience is chosen at check-in (as `VisitDialog` does), not stored on the customer | prototype | Record; harmless while `STUDENT_VISITS` is false |
| **DI-46** | Review §3c: a desk price's badge «سعر يدوي» should name who typed it («سعر يدوي · سامي», ADR 0010 rule 6) | the file's badge names the person | prototype | Record (not in `DECISIONS_DESK.md`) |
| **DI-47** | Archiving a customer leaves the uncollected visits of theirs on the desk's list (the model says nothing) | decide whether an archived customer's uncollected visits stay listed | docs | Record |

---

## 5. The files, their owners and the boundaries

| File | Owner this round | This batch's change |
|---|---|---|
| `prototype/Desk.html` | this batch | §3.1–§3.4 |
| `prototype/Customers.html` | this batch | §3.6 (the inline script) |
| `prototype/Customer file.html` | this batch | §3.6, §3.7 |
| `prototype/Payments.html` | this batch | §3.9 (the inline script) |
| `prototype/My payments.html` | this batch | §3.8 (the inline script) |
| `prototype/masaha/desk-core.jsx` | this batch | §3.1–§3.8 |
| `prototype/masaha/desk-sheet.jsx` | this batch | §3.3 (whole file) |
| `prototype/masaha/desk-data.js` | this batch | §3.1–§3.9 |
| `prototype/masaha/masaha.css` | shared; this batch's one rule | §3.4 (append only) |
| `prototype/Owner overview.html` | batch 5 (merged) | **one line**, §3.2 (DI-35) |
| `prototype/Finance.html` | batch 5 (merged) | **one line**, §3.9 (DI-36) |
| `prototype/Flows - states.html` | shared | section 56 + twelve labels (§3.10) |
| `CHANGES.md` | shared | *Batch 6* only |
| `INDEX.md` | shared | *Batch 6* parameters, §56, twelve labels |
| `README.md` | shared | the frame/section count only |
| `SCREENS.md` | shared | rows 13–17's sections column only |

**Never edited:** `masaha/shared.jsx`, `auth.jsx`, `account.jsx` and the account pages; `masaha/owner.jsx`,
`owner-data.js`, `finance.jsx`, `admin.jsx`, `admin-data.js`, `profile-a.jsx`, `profile-b.jsx`, `space-parts.jsx`,
`data.js`, `details-data.js`, `i18n.js`; `Admin space edit.html` and every admin page; every other owner page;
`_ds/`, `_vendor/`; `docs/design/screens/`, `docs/design/scripts/`; anything outside `docs/design/`. Issue #72 is
not this batch's. **If any step seems to need one of these, stop and write it in the report.**

No other design batch runs; workers A, B and the media worker work outside `docs/design/`. The open PRs at
planning time: #76 (batch 5, must merge first), #77 (`feat/space-photos`), #78 (`feat/session-ends`).

---

## 6. The commits, in order

All `docs(design): …`; each subject's length counted (≤ 50). Each commit's `CHANGES.md` line goes in it; the first
creates the section. Stage by path only (`git add <path> …`), never `-A` or `.`.

**The section heading (commit 1 adds it, after the last line of *Batch 5*'s table, before any heading that follows
it):**
```markdown
## Batch 6 — the front desk (YYYY-MM-DD)

Reviewed as DK-001…DK-024; decided in `DECISIONS_DESK.md` (K1–K8 and the smaller items), with the desk's
amendments of P1, P8 and P9 (`DECISIONS_SHARED.md`). The design-system item (DK-024, with OW-010), the API's
(K8's whole read, K6's write-off, DK-018's keys: steps 7–8) and the rule changes (api-contract §4, ADR 0009's
table, the data model's write-off) are the web's, the API's and the docs'.

| Decision | What changed | Where |
|---|---|---|
```
(`YYYY-MM-DD`: the date of commit 1, `date +%F`.)

| # | Subject (chars) | Files |
|---|---|---|
| 1 | `docs(design): check-out takes money in one block` (48) | `masaha/desk-data.js`, `masaha/desk-core.jsx`, `Desk.html`, `CHANGES.md` |
| 2 | `docs(design): collect, record a debt, write off` (47) | `masaha/desk-data.js`, `masaha/desk-core.jsx`, `Desk.html`, `Owner overview.html`, `CHANGES.md` |
| 3 | `docs(design): the sheet in one step, debt first` (47) | `masaha/desk-sheet.jsx`, `masaha/desk-core.jsx`, `masaha/desk-data.js`, `Desk.html`, `CHANGES.md` |
| 4 | `docs(design): one desk search, ordered for phones` (49) | `Desk.html`, `masaha/desk-core.jsx`, `masaha/masaha.css`, `CHANGES.md` |
| 5 | `docs(design): the week's warning uses the count` (47) | `masaha/desk-data.js`, `masaha/desk-core.jsx`, `CHANGES.md` |
| 6 | `docs(design): customers: actions by state, archive` (50) | `masaha/desk-data.js`, `masaha/desk-core.jsx`, `Customers.html`, `Customer file.html`, `CHANGES.md` |
| 7 | `docs(design): the customer file hides no money` (46) | `masaha/desk-data.js`, `masaha/desk-core.jsx`, `Customer file.html`, `CHANGES.md` |
| 8 | `docs(design): my payments show what was voided` (46) | `masaha/desk-data.js`, `masaha/desk-core.jsx`, `My payments.html`, `CHANGES.md` |
| 9 | `docs(design): payments: five columns, a month` (45) | `masaha/desk-data.js`, `Payments.html`, `Finance.html`, `CHANGES.md` |
| 10 | `docs(design): the board's desk frames` (37) | `Flows - states.html`, `INDEX.md`, `README.md`, `SCREENS.md`, `CHANGES.md` |

(All paths under `docs/design/prototype/` except `CHANGES.md`, `INDEX.md`, `README.md`, `SCREENS.md`, under
`docs/design/`.)

**The `CHANGES.md` lines**, one table row per commit, in order:

1. `| **K2, DK-004, DK-010, DK-020, DK-021** | Check-out takes money in **one block**, the shape every place that takes money now has: what is due with its calculation once («4 س × 3 ₪ = 12 ₪ · تقريب لأعلى بعد 15 دقيقة», the space's own rounding, and «السقف: سعر اليوم» only when the cap is on and applies); «المستلم الآن», filled with what is due; «الطريقة»; a live line — «المتبقي 7 ₪ يصبح دينًا على هبة المصري — رقم الجوال مطلوب», the name and mobile under it, or «الباقي للزبون 8 ₪» when more is handed over, which the ledger never records; «لم يدفع شيئًا»; and a submit that names the money, «خروج واستلام 12 ₪». The «خروج بدون دفع» mode is gone. **A fixed-price subscriber leaves in one tap** from the row, the card or the file, the toast saying how long they stayed (\`?dialog=checkout&pid=ps0\` does it on load); one billed from attendance keeps the dialog, filled with what is owed so far. «تسجيل كزيارة» checks the visit in **as the customer**, so «لم يدفع شيئًا» needs no mobile and the debt lands in their file. Every check-out toast names the amount, the item and the method (K7); a failure says «لم يصل الرد. أعد المحاولة — لن تُسجَّل مرتين.» (\`?fail=checkout\`) and a 429 that nothing was recorded (DK-018) | \`masaha/desk-core.jsx\` (\`MoneyBlock\`, \`OutButton\`, \`CheckoutDialog\`), \`desk-data.js\`, \`Desk.html\` |`
2. `| **K2, DK-012, K6, DK-003, DI-35** | «استلام دفعة» takes the same block, its submit «تسجيل 150 ₪»; more than is owed is change, except on a usage-based subscription chosen alone, where it is credit. The uncollected list holds **visits with no customer**, as the automatic check-out leaves them: each collects on the visit itself («تحصيل زيارة · يزن الأسطل») or becomes a debt by a name and a mobile («تسجيل دينًا»). **The owner writes a visit off** — «لن يُحصَّل…» in the row's «⋯», an \`AlertDialog\` with a required reason; out of the list and the debt, never a payment and never a deletion (\`?writeoff=u2\`). The card is compact — «4 زيارات غير محصّلة · 36 ₪», three rows and «عرض الكل» (\`?unpaid=all\`) — and \`#unpaid\` is where the overview's queue now lands | \`masaha/desk-core.jsx\` (\`PayDialog\`, \`DebtDialog\`, \`ReasonDialog\`, \`UnpaidRow\`), \`desk-data.js\`, \`Desk.html\`, \`Owner overview.html\` |`
3. `| **K3, DK-005–DK-008, DK-018** | The subscription sheet is **one step**: a new customer's name and mobile first — «اختياري» only while nothing stays unpaid — then the package, the dates and the money block, «حفظ واستلام 300 ₪». **A renewal with a debt takes the old balance first**: «مستحق من قبل 150 ₪ · اشتراك سبتمبر — يُطبَّق المستلم عليه أولًا، ثم على التجديد.», the block filled with 150 + 250, one payment per item, «تجديد واستلام 400 ₪»; the warning keeps no button. A renewal shows its package in one line with «تغيير الباقة»; new, each package is one line. A custom subscription with no end says so — «بلا تاريخ نهاية · ينتهي عند استهلاك 20 ساعة», or «بلا حدّ · يبقى نشطًا حتى يُنهى» with its warning icon — and keeps no end it was not given. When the payment fails after the save, the sheet says «حُفظ الاشتراك؛ لم تُسجَّل الدفعة 90 ₪» and retries the payment alone (\`?fail=sheet-pay\`) | \`masaha/desk-sheet.jsx\`, \`desk-core.jsx\`, \`desk-data.js\`, \`Desk.html\` |`
4. `| **K1, DK-001–DK-003, DK-023, P1** | **One desk search finds everyone**: «حاضر الآن» first, each with «خروج»; then the customers on file; then «تسجيل زيارة باسم «لمى»» and «زبون جديد باسم «لمى»», which carry the name — the visit is the primary one when nothing matches, and a number typed goes into «رقم الجوال». The present list loses its own search. **On a phone the desk reads search → uncollected → present**; from 1280 the uncollected card is the side column again. «الحاضرون الآن 27 / 40» is said once, with «الآن \\| السجل» beside it. «استلام دفعة» and «زبون جديد» are page actions (the top bar from 768, its «⋯» on a phone); the bottom bar keeps «تسجيل زيارة». The visit dialog asks only what the space uses — «طالب» where a student price exists (\`?demo=studentprices\`), «الوردية» where the space has shifts, on the one in progress (\`?demo=noshifts\`) — and names the rate, «تُحسب 3 ₪ للساعة · حتى 15 ₪» | \`Desk.html\`, \`masaha/desk-core.jsx\` (\`VisitDialog\`), \`masaha.css\` |`
5. `| **K5** | The check-in warning the model can serve: «استُنفدت أيام هذا الأسبوع» with «هذا الأسبوع 3 من 3»; the weekdays («أيامه: السبت، الاثنين، الأربعاء») are gone from the sample and the progress lines | \`masaha/desk-data.js\`, \`desk-core.jsx\` |`
6. `| **DK-013, DK-014, DK-017, DK-022** | A customer's actions **by state**, in one order on the desk's card, the file's header and the Customers row: «حضور» or «خروج» first, «استلام 42 ₪» only when they owe, «تجديد» only when ending soon or ended, and «اشتراك جديد», «تعديل البيانات», «ملف الزبون» and the owner's «أرشفة» in «⋯». **«تعديل البيانات»** puts the name and the mobile right («هذا الرقم مسجّل لزبون آخر: سلمى الريس», \`?edit=m6&taken=1\`). An archived customer stays under **«مؤرشف»**, the owner's chip, with «استرجاع»; a settled one is archived at once with «تراجع», one who owes after the dialog naming the debt. The status filter is chips — «الكل · نشط · ينتهي قريبًا · منتهٍ · مؤرشف» — and «بدون اشتراك» is only a type. The table has **five columns from 768**, the mobile under the name and the end under the subscription | \`Customers.html\`, \`Customer file.html\`, \`masaha/desk-core.jsx\` (\`CustomerActions\`, \`EditCustomerDialog\`, \`ArchiveDialog\`), \`desk-data.js\` |`
7. `| **K4, DK-011, DK-016** | **The customer file hides no money**: its first tab, «المستحقات والاشتراكات», lists the unpaid visits — the date and times, the charge, «تحصيل», and the owner's «لن يُحصَّل…» — before the subscriptions, and says «visits only» only when nothing is owed. «الدفعات» lists the visits' payments **through the visit's customer**, not the name, in five columns, each voided one struck with «ألغاها أحمد: …»; **the void is in the row's «⋯»**, for visit payments too, and its \`AlertDialog\` repeats the amount, the customer and the date | \`Customer file.html\`, \`masaha/desk-core.jsx\` (\`PaidAmount\`, \`PaymentMenu\`, \`VoidDialog\`), \`desk-data.js\` |`
8. `| **DK-015, K4** | «دفعاتي اليوم» shows the payment the owner voided, **struck through with «ألغاها أحمد: سُجّلت بالخطأ»**, and leaves it out of the figures to hand over. On a phone the three figures are one card, «نقدًا للتسليم» first; under them, «خطأ في دفعة؟ يلغيها صاحب المساحة، وتظهر هنا مشطوبة.» | \`My payments.html\`, \`masaha/desk-core.jsx\`, \`desk-data.js\` |`
9. `| **DK-016, DK-017, A7, DI-36** | Payments has **five columns from 768** — the time under the date, the item under the customer, the method under the amount — and **the void in each row's «⋯»**, its \`AlertDialog\` as the file's. «إظهار الملغاة» is a chip by the count. \`?month=2026-08\` opens a month, and Finance's «عرض الكل» carries its month there | \`Payments.html\`, \`Finance.html\`, \`masaha/desk-data.js\` |`
10. `| **Board** | A new section, «Batch 6 — the front desk», with 37 frames of the states above — the board's first at 768 — listed in \`INDEX.md\` §56; the board's twelve desk frames whose state moved are relabelled | \`Flows - states.html\`, \`INDEX.md\`, \`README.md\`, \`SCREENS.md\` |`

In `CHANGES.md` each line is written **without** the backslashes shown above (they are only this plan's escaping
of `` ` `` and `|`; line 4's `\\|` is written `\|`, the table's escaped pipe).

**`INDEX.md` rows:** all in commit 10 (§3.10): the *Batch 6* parameters table, section 56's 37 rows, the twelve
relabels.

---

## 7. The executor's procedure

0. **Before anything:** read this plan whole, and `DECISIONS_DESK.md`. Do not start before the owner's reply to §4
   is in `C:\Users\basel\.prompt\MASAHA_DESIGN\PROMPT\FIX_DESK_PLAN_REPLY.md` (or the executor prompt); apply its
   answers.
1. **#76 must be in `main`.** In Git Bash, in `C:\Users\basel\masaha-design-b`:
   ```bash
   git fetch origin --prune
   gh pr view 76 --json state,mergeCommit --jq '.state + " " + .mergeCommit.oid'   # must print MERGED <sha>
   git merge-base --is-ancestor <that sha> origin/main && echo "in main"            # must print: in main
   git status --short                                                               # must print nothing
   ```
   If #76 is not merged, **stop** and say so. Then check that batch 5's two lines this plan edits are as quoted:
   `grep -n "href: 'Desk.html' });" "docs/design/prototype/Owner overview.html"` (one line) and
   `grep -n 'href="Payments.html">' docs/design/prototype/Finance.html` (one line). If either differs, stop.
   Also `git log --oneline 1240736..origin/main -- docs/design/prototype/masaha/desk-*.* docs/design/prototype/Desk.html docs/design/prototype/Customers.html "docs/design/prototype/Customer file.html" docs/design/prototype/Payments.html "docs/design/prototype/My payments.html"`
   must print nothing; if it prints a commit, stop and report (a desk file moved since this plan).
2. **Branch:** `git switch --no-track -c design/desk origin/main`.
3. **Server** (a background shell; note its PID):
   ```bash
   cd "/c/Users/basel/masaha-design-b/docs/design/prototype" && python -m http.server 5347 --bind 127.0.0.1
   ```
4. **The browser-check script** — save outside the repo as `C:\Users\basel\Downloads\design-fix-desk\tools\pass.mjs`:
   ```js
   // node pass.mjs <base> <urls.txt> <outdir> [--all] [--shots] [--port=9334] [--widths=390,768,1440]
   // A line of urls.txt: a URL, optionally a TAB and a JS expression run after the load (a click).
   import { spawn } from 'node:child_process';
   import { readFileSync, mkdirSync, writeFileSync } from 'node:fs';
   import { join } from 'node:path';
   const [base, list, out] = process.argv.slice(2);
   const all = process.argv.includes('--all'), shots = process.argv.includes('--shots');
   const portArg = process.argv.find((a) => a.startsWith('--port=')); const PORT = portArg ? portArg.slice(7) : '9334';
   const wArg = process.argv.find((a) => a.startsWith('--widths=')); const WIDTHS = wArg ? wArg.slice(9).split(',').map(Number) : [390, 768, 1440];
   const CHROME = process.env.CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
   mkdirSync(out, { recursive: true });
   const chrome = spawn(CHROME, ['--headless=new', '--remote-debugging-port=' + PORT, '--user-data-dir=' + join(out, '.profile'), '--hide-scrollbars', 'about:blank'], { stdio: 'ignore' });
   const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
   let ws;
   for (let i = 0; i < 50 && !ws; i++) { try { const t = await (await fetch('http://127.0.0.1:' + PORT + '/json/list')).json(); const p = t.find((x) => x.type === 'page'); if (p) ws = p.webSocketDebuggerUrl; } catch {} if (!ws) await sleep(200); }
   const sock = new WebSocket(ws); await new Promise((r) => sock.addEventListener('open', r, { once: true }));
   let id = 0; const wait = new Map(); const errors = [];
   sock.addEventListener('message', (e) => { const m = JSON.parse(e.data); if (m.id && wait.has(m.id)) { wait.get(m.id)(m); wait.delete(m.id); } if (m.method === 'Runtime.exceptionThrown') errors.push(m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text); if (m.method === 'Runtime.consoleAPICalled' && (m.params.type === 'error' || m.params.type === 'warning') && !String(m.params.args[0] && m.params.args[0].value).includes('in-browser Babel')) errors.push(m.params.type + ': ' + m.params.args.map((a) => a.value ?? a.description).join(' ').slice(0, 300)); });
   const send = (method, params = {}) => new Promise((r) => { const n = ++id; wait.set(n, r); sock.send(JSON.stringify({ id: n, method, params })); });
   await send('Runtime.enable'); await send('Page.enable');
   const withQ = (u, q) => { if (!q) return u; const [p, h] = u.split('#'); return p + (p.includes('?') ? '&' : '?') + q + (h ? '#' + h : ''); };
   const variants = all ? ['', 'lang=en', 'theme=dark', 'lang=en&theme=dark'] : ['', 'lang=en&theme=dark'];
   const rows = ['url\twidth\tblank\toverflow\terrors'];
   for (const line of readFileSync(list, 'utf8').split(/\r?\n/).map((s) => s.trim()).filter(Boolean)) {
     const [u0, js] = line.split('\t');
     for (const q of variants) { const url = withQ(u0, q);
       for (const width of WIDTHS) {
         errors.length = 0;
         await send('Emulation.setDeviceMetricsOverride', { width, height: width === 390 ? 844 : 1000, deviceScaleFactor: 1, mobile: width === 390 });
         await send('Page.navigate', { url: base + url });
         await sleep(3500);
         if (js) { await send('Runtime.evaluate', { expression: js }); await sleep(1500); }
         const r = await send('Runtime.evaluate', { expression: "JSON.stringify({ blank: !document.getElementById('ds-root') || !document.getElementById('ds-root').children.length, overflow: document.documentElement.scrollWidth > window.innerWidth + 1 })", returnByValue: true });
         const v = JSON.parse(r.result.result.value);
         rows.push([url, width, v.blank, v.overflow, errors.join(' | ')].join('\t'));
         if (shots) { const s = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false }); writeFileSync(join(out, (url + (js ? '_js' : '')).replace(/[^\w]+/g, '_').slice(0, 90) + '-' + width + '.png'), Buffer.from(s.result.data, 'base64')); }
       } }
   }
   writeFileSync(join(out, 'pass.tsv'), rows.join('\n')); console.log(rows.join('\n'));
   sock.close(); chrome.kill();
   ```
   Run it from the `tools` folder: `node pass.mjs http://127.0.0.1:5347/ urls-<n>.txt "C:/Users/basel/Downloads/design-fix-desk/pass-<n>" --shots`.
   If a run ends with `Detected unsettled top-level await`, the browser closed under it: kill its Chrome (port
   9334) and run that list again.
   **A list of at most 8 URLs per run** (each run of 8 URLs × 2 variants × 3 widths takes about 3 minutes; the tool's
   10-minute limit kills a longer one). Before each run, check nothing listens on 9334 (`netstat -ano | grep 9334`);
   if a stale Chrome does, kill that PID (batch 5's phantom errors came from a stale browser). A row with `true` in
   *blank* or *overflow*, or any *errors*, is a failure to fix before committing; a first-URL blank with no errors is
   the cold Babel compile — run that URL again. **Before trusting it,** run it once on `Desk.html?state=404` (blank
   must be `false`) and on `Nope.html` (blank must be `true`).
   Arabic in a URL file is fine (UTF-8); the screenshots of two Arabic searches share a file name — look at them one
   run at a time.
5. **Before images** (on the clean branch, before the first edit): `urls-before.txt` with `Desk.html?role=reception`,
   `Desk.html?role=reception&q=لمى`, `Desk.html?role=reception&dialog=checkout&pid=pv0`,
   `Customers.html?role=reception&renew=m6`, `Customer%20file.html?id=m10`, `My%20payments.html?role=reception`,
   `Payments.html`, `Customers.html` (8), with `--shots` into `C:\Users\basel\Downloads\design-fix-desk\before\`.
   Never commit images.
6. **At every commit**, in this order:
   ```bash
   node docs/design/scripts/check-parse.mjs && node docs/design/scripts/check-classes.mjs
   git diff --stat            # only the commit's files (§6)
   git add <each file by path> && git commit -m "<subject>"
   ```
   then the pass script on the commit's URLs (below) with `--shots`, **and look at the PNGs yourself** at 390, 768 and
   1440. A commit is done when both are clean. (`check-classes.mjs` prints "gone … drop it from KNOWN" lines for
   other files: they are batch 5's to fix, not errors.)

   | After commit | URLs (one file each, ≤ 8) | Look for |
   |---|---|---|
   | 1 | `Desk.html?role=reception&dialog=checkout&pid=pv0`, `…pid=pv0&received=20`, `…pid=pv0&received=5`, `…pid=pv5&received=0`, `…pid=ps2`, `…pid=ps0`, `…pid=pv0&fail=checkout&state=ratelimit`, `…pid=pv0&prices=none` (each `Desk.html?role=reception&dialog=checkout&` + the rest) | the calculation once, «تقريب لأعلى بعد 15 دقيقة»; the line under the amount changes with it; 20 → «الباقي للزبون 8 ₪» and the button «خروج واستلام 12 ₪»; 5 → the debt line with «— رقم الجوال مطلوب» and the two fields; pv5 at 0 → no mobile fields, «خروج بدون دفع»; ps2 → «المستحق حتى الآن 42 ₪»; ps0 → no dialog, the toast «سُجّل خروج محمد العطار» / «4 س 35 د», 26 / 40; the failure Alert and the 429 inside; `prices=none` → «مبلغ الزيارة (₪)» |
   | 2 | `Desk.html`, `Desk.html?unpaid=all`, `Desk.html?writeoff=u2`, `Desk.html?role=reception&dialog=debt&vid=u3`, `Desk.html?role=reception&dialog=pay&vid=u3`, `Desk.html?role=reception&dialog=pay&cid=m6`, `Desk.html?role=reception&dialog=pay`, `Owner%20overview.html` | the card's title with its forms, three rows, «عرض الكل»; the rows' actions under each row in the side column at 1440 (no orphan «⋯»); no «⋯» for reception; the write-off dialog's words; the two dialogs on a visit with no customer; the picker lists who owes; the overview loads (its link: open it and see the desk scroll to the card) |
   | 3 | `Customers.html?role=reception&renew=m6`, the same + TAB + `document.querySelector('[role=dialog] button[type=submit]').click()`, `Desk.html?role=reception&dialog=sheet&mode=new&name=سليم`, `Desk.html?role=reception&dialog=sheet&mode=subscribe&cid=m3&pkg=custom`, `Desk.html?role=reception&dialog=sheet&mode=renew&cid=m7&fail=sheet-pay&half=1`, `Desk.html?role=reception&dialog=sheet&mode=renew&cid=m7&paynow=50`, `Desk.html?role=reception&dialog=sheet&mode=new&fail=sheet` | no step text; the renewal's one-line package, the warning with no button, «المجموع 400 ₪», «تجديد واستلام 400 ₪»; after the click, the toast naming both items; packages one line each in the ¾ sheet at 390 (nothing cut at its edge); «بلا حدّ · يبقى نشطًا حتى يُنهى» with its icon; the half-saved state; `paynow=50` → «المتبقي 40 ₪ يصبح دينًا على خالد النجار» |
   | 4 | `Desk.html?role=reception&q=لمى`, `Desk.html?role=reception&q=سليم`, `Desk.html?role=reception`, `Desk.html?role=reception&q=1006`, `Desk.html?role=reception&dialog=visit&vname=سليم`, `Desk.html?role=reception&dialog=visit&demo=noshifts,studentprices`, `Desk.html?role=reception&state=empty`, `Desk.html?role=reception&tab=log` | here-first results; the primary visit button with no match; at 390 and 768 the card before «الحاضرون الآن 27 / 40»; at 1440 the side column; the summary «19 مشتركًا · 8 زيارات»; top-bar «⋯» at 390 holds «استلام دفعة» and «زبون جديد»; the visit dialog's rate line and the morning shift chosen; `studentprices` → «طالب», no shifts; empty → no card at 390 |
   | 5 | `Desk.html?role=reception&dialog=warn&cid=m12`, `Desk.html?role=reception&q=ميار`, `Customer%20file.html?id=m12` | the week warning; «هذا الأسبوع 3 من 3» on the card and in the file; no weekday names |
   | 6 | `Customers.html`, `Customers.html?status=archived`, `Customers.html?role=reception`, `Customers.html?archive=m6`, `Customers.html?edit=m6&taken=1`, `Customer%20file.html?id=m6`, `Customer%20file.html?id=m16`, `Desk.html?role=reception&q=رهف` | five columns at 768 and 1440, nothing wrapping into a third line; the chips wrap cleanly at 390; reception has no «مؤرشف» chip; the row menu's order (state first, separator, rest); the archive dialog's new words; the taken mobile's error; the file header's buttons with their height (not collapsed), «⋯» last; Abeer's file: «مؤرشف» badge and «استرجاع» only |
   | 7 | `Customer%20file.html?id=m14`, `Customer%20file.html?id=m14&tab=pays`, `Customer%20file.html?id=m10`, `Customer%20file.html?id=m6&tab=pays`, `Customer%20file.html?id=m6&tab=pays&role=reception`, `Customer%20file.html?id=m1&tab=pays&void=1`, `Customer%20file.html?id=m14&writeoff=u2` | the unpaid visits card first, on one line from 768; Dana (m10): the card and «لا توجد اشتراكات» with no «visits only»; the visit payment in Malek's payments with its «⋯»; Rahaf's voided 50 ₪ struck, «ألغاها أحمد: سُجّلت مرتين بالخطأ»; reception: no «⋯»; the void `AlertDialog` |
   | 8 | `My%20payments.html?role=reception`, `My%20payments.html?role=reception&state=empty`, `My%20payments.html?role=reception&state=loading` | Farah's 6 ₪ struck with the line; 45 / 59 / 104 ₪ and «4 دفعات»; one card at 390, three StatCards at 768 and 1440; the caption |
   | 9 | `Payments.html`, `Payments.html?void=1`, `Payments.html?month=2026-08`, `Payments.html?voided=1`, `Payments.html?range=today&voided=1`, `Finance.html?tab=debts`, `Payments.html?state=empty` | five columns at 768; the «⋯» on live rows only; the chip by the count; August's range in the picker; Finance's «عرض الكل» href carries `?month=` (hover it or read the DOM) |
   | 10 | the 34 distinct frame URLs of §3.10 (in five files of ≤ 7) with `--all` (2 languages × 2 themes × 3 widths: about 5 minutes a file), then open `Flows%20-%20states.html` and scroll to the bottom | the section's frames load; nothing overlaps batch 5's last row |
7. **After images:** the commit-10 run's shots are the after images. Copy one pair per decision into
   `C:\Users\basel\Downloads\design-fix-desk\pairs\` named `<decision>-<width>-before.png` / `-after.png` for K1 (desk
   search, 390), K2 (check-out, 390), K3 (renewal, 1440), K4 (file m14, 1440; my payments, 390), K5 (390), K6 (390),
   DK-003 (desk, 390), DK-013 (card, 390), DK-017 (Customers, 768), DK-016 (Payments, 768). Never commit them.
8. **The head's checks** (from the repo root): this worktree has no `node_modules`; run `npm ci` (Node 24, as
   `.nvmrc`), then `npm run format:check` and `npm run check:links`; both must pass. If `npm ci` cannot run, say so in
   the report — CI runs both on the PR. Say honestly that `.prettierignore` excludes `docs/design/` and Markdown, so
   `format:check` sees none of this batch's files; `check:links` checks `CHANGES.md`, `INDEX.md`, `README.md` and
   `SCREENS.md`.
9. **Push and the PR:**
   ```bash
   git push -u origin design/desk
   gh pr create --assignee @me --title "design: the front desk" --label docs --label area:docs --body-file "C:/Users/basel/Downloads/design-fix-desk/PR_BODY.md"
   ```
   **The PR description** (write it to `PR_BODY.md`; fill the bracketed results with what was run):
   ```markdown
   ## Summary
   Batch 6 of the design review — the front desk — applied to the prototype: one desk search, here first (K1); one
   money block wherever money is taken (K2); a renewal pays the old debt first (K3); no hidden money in the file or
   in «دفعاتي اليوم» (K4); the week's warning as a count (K5); the owner's «لن يُحصَّل» (K6); the desk's toasts with
   the amount (K7); and DK-003, DK-006–DK-008, DK-010–DK-018, DK-020–DK-023, with batch 5's DI-35 and DI-36.
   Decisions: `DECISIONS_DESK.md`; record: `docs/design/CHANGES.md` › *Batch 6*. The last design batch: the
   screenshots are regenerated once after it.

   ## Scope
   `docs/design/` only: the desk's five pages and three modules, one layout rule in `masaha.css`, one line each in
   `Owner overview.html` (DI-35) and `Finance.html` (DI-36), the board (section 56 and twelve relabels), `CHANGES.md`,
   `INDEX.md`, `README.md`'s counts, `SCREENS.md` rows 13–17.

   ## Acceptance criteria
   - [x] K1: one search — the people here first, then customers, then the two ways in, carrying the name
   - [x] K2: one money block in check-out, «استلام دفعة» and the sheet; the change and the debt said; the amount on the button
   - [x] K3: a renewal with a debt is paid oldest first, one payment per item
   - [x] K4: the file's unpaid visits and visit payments; «دفعاتي اليوم» shows a void struck
   - [x] K5: «استُنفدت أيام هذا الأسبوع · 3 من 3»
   - [x] K6: the owner's write-off with a reason
   - [x] K7: check-in, check-out and money toasts, with the amount
   - [x] DK-003: the desk ordered for the phone; DK-010: one-tap check-out; DK-012: uncollected visits with no customer
   - [x] DK-013/014/017/022: actions by state, editing, archive and restore, five columns at 768, status chips
   - [x] DK-016/018/021/023: the void in «⋯»; safe retries and the half-saved sheet; the space's rounding; the visit dialog's choices
   - [x] DI-35 `Desk.html#unpaid`; DI-36 `Payments.html?month=`
   - [x] No changed page blanks, errors or overflows at 390/768/1440, ar/en, light/dark

   ## Out of scope
   DK-024 (the design system's sheet width); K8/DK-019 (the API's whole present read, step 7); the rule changes
   (api-contract §4, ADR 0009's rows, the data model's write-off) and DK-018's keys (steps 7–8); DI-41–DI-47
   (recorded); batch 5's files beyond the two lines; `shared.jsx`.

   ## Change type
   docs (design archive)

   ## Evidence
   - `node docs/design/scripts/check-parse.mjs` — [result] at each of the 10 commits
   - `node docs/design/scripts/check-classes.mjs` — [result] at each commit
   - The browser pass (`pass.mjs`): [N] URLs × 4 variants × 3 widths on the head — [0 blank, 0 overflow, 0 console errors]
   - Each changed page looked at, at 390, 768 and 1440
   - `npm run format:check` — [result] (`docs/design/` and Markdown are excluded by `.prettierignore`)
   - `npm run check:links` — [result]

   ## Screenshots
   Before/after pairs per decision were taken locally and are not committed. [Attach them by drag and drop, or list them.]

   ## Definition of Done
   - [x] Scope verified: only `docs/design/` files of the batch
   - [x] Atomic commits, Conventional Commits, subjects ≤ 50 characters
   - [x] `CHANGES.md` says only what is built
   - [x] `INDEX.md`, the board, `README.md` and `SCREENS.md` agree
   - [x] No object rest, no generic top-level name; no class missing from the prebuilt CSS
   - [x] CI green and the PR `CLEAN`
   ```
10. **CI and CLEAN** — no `jq`; poll with a bound:
    ```bash
    for i in $(seq 1 30); do gh pr checks <n> && break; sleep 30; done
    gh pr view <n> --json mergeStateStatus --jq .mergeStateStatus     # expect CLEAN
    ```
    If `main` moved and the PR conflicts, rebase onto `origin/main` keeping both sides of `CHANGES.md`, `INDEX.md`,
    the board and `README.md` (the counts recounted, never summed by hand), then `git push --force-with-lease`.
11. **The conflict check** against every open PR:
    ```bash
    gh pr list --state open --json number,headRefName --jq '.[] | "\(.number) \(.headRefName)"'
    # for each: git fetch origin <head> && git merge-tree --write-tree --name-only HEAD FETCH_HEAD; echo "exit $?"
    ```
    Expected: clean against each (no other design PR is open).
12. **The report** — `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\FIX_DESK_REPORT.md`, sections: 1 the PR (number,
    URL) and its head SHA; 2 the commits (SHA, exact subject); 3 what was run and its results (each command; the
    pass's totals per commit and on the head); 4 problems met and how they were solved; 5 anything unexpected; 6 the
    conflict check per open PR; 7 departures from this plan, each with why; 8 DI-41–DI-47 restated as recorded.
13. **Stop everything:** the server (by its PID; `taskkill //PID <pid> //F` if needed), every Chrome the script
    started (`netstat -ano | grep 9334` → kill that PID), every background shell; then `netstat -ano | grep 5347` and
    `netstat -ano | grep 9334` print nothing. **Never merge.**

---

## 8. The reviewer's checklist

For each item: open the file, verify, open the frames (at 390, 768, 1440; ar and en; light and dark).

| Item | File(s) and what to verify | Frames |
|---|---|---|
| AC1 K1 | `Desk.html` `SearchResults`, `PresentRow`, `DeskSearch`: the order, `aria-live`, the `primary` only when `none`, the digits branch; `desk-data.js` `searchCustomers` excludes archived; no searchbox in `PresentList` | §3.10 #1–#5 |
| AC2 K2 | `desk-core.jsx` `moneyOf` (closed: `recorded = min(rec, due)`, open: credit), `MoneyBlock` (the line's five cases, `aria-live`), the three submit labels; `CheckoutDialog` has no `debtMode` | #11–#14, #26 |
| AC3 K3 | `desk-sheet.jsx` `prior`, `calc`, the warning without a button; `desk-core.jsx` `saveSubscription` loops `prior` oldest first, then the rest on `sub` | #21, #22; click its submit |
| AC4 K4 | `Customer file.html` `filePays` uses `visitPaysOf`; `My payments.html` `rowsFor` reads `voided`/`voidedBy` for both kinds; `live` excludes voided; `paidLine` in every money toast | #30, #32, #33, #37 |
| AC5 K5 | `desk-data.js` no `weekDays`; `desk-core.jsx` `checkInWarnings` `week`, `texts.week` | #18 |
| AC6 K6 | `ReasonDialog`, `WriteOffDialog`, `api.writeOff` (to `writtenOff`, never a payment); `UnpaidRow`'s «⋯» behind `IS_OWNER` | #6, #7 |
| AC7 K7 | every `toast.success` in the provider (check-in, check-out, pay, payVisit, attachDebt, writeOff, saveSubscription, voidPayment) | #15 |
| AC8 DK-003 | `Desk.html` `DeskInner` order; `masaha.css` rule; `UnpaidCard` `hidden xl:flex` when empty | #4, #6, #10 |
| AC9 DK-006–008 | `desk-sheet.jsx`: no `step`; `askPhone`/`unpaidAfter`; `showPk`; `endNote`; `end` is `null` for custom with no «إلى» | #23, #24 |
| AC10 DK-010/020 | `isQuickOut`, `OutButton`; `Desk.html` initial + effect; `WarnDialog` passes `c.id` | #13, #15 |
| AC11 DK-012 | `PayDialog` `v` branch, `DebtDialog`, `api.payVisit`/`attachDebt` | #8, #9 |
| AC12 DK-013/014/017/022 | `CustomerActions`, `CustomerMenuItems` (order), `EditCustomerDialog` (taken), `ArchiveDialog`, `api.archive`/`restore` set/delete `archived` (never `splice`); `Customers.html` `STATUSES`, five columns | #27–#29, #34 |
| AC13 DK-016 | `PaymentMenu` (owner, live only, `variant="destructive"`), `VoidDialog`; no void button outside a «⋯» | #31, #33, #35 |
| AC14 DK-018 | `MONEY_RETRY` in `ActionAlert` children of checkout, pay, sheet, visit; `MoneyRateNote`; the sheet's `half` | #19, #20, #25 |
| AC15 DK-021/023 | `visitCharge` uses `SETTINGS.roundAfter` and `SETTINGS.cap`; `VisitDialog`'s rate line, `STUDENT_VISITS`, `SHIFT_LIST`, `currentShift()` | #11, #16, #17 |
| AC16 P1 | `DeskInner` `pageActions`; no «زبون جديد» beside the search | #4 at 390 (open «⋯») |
| AC17 DI-35/36 | `git diff origin/main -- "docs/design/prototype/Owner overview.html" docs/design/prototype/Finance.html` = two one-line changes | #10, #36 |
| AC18 states | `?state=loading|empty|error|offline|403|404` on the five pages; each `?fail=` of the INDEX table | as listed |
| AC19 board | section at top 160000 and 37 frames; `INDEX.md` §56 37 rows; the six relabels × 2 in both; README's count = `grep -c` | — |
| AC20 boundaries | `git diff --stat origin/main` lists only §5's files | — |
| Hazards | §9 — grep the changed files for `...` inside `{ }` destructuring, for a top-level `name`, for `size="default"` or `variant="default"`, for the dead classes | — |

## 9. The hazards

- **Babel's shared globals.** Every page's modules and inline scripts share one global scope. **No object rest
  destructuring** (`const { a, ...rest } = props` or `function X({ a, ...p })`) anywhere — its `_excluded` helper is
  page-wide (DI-27). Object spread into a new object (`{ ...u, reason }`, `{ ...x, ...p }`) is fine; so is array
  destructuring. **No top-level `name`**, `title`, `status`, `open`, `type`, `data`, `list`, `rows` or other generic
  name. The new top-level names are exactly these, each defined once (checked free in every page that loads them):
  `desk-core.jsx` — `durText`, `paidLine`, `MONEY_RETRY`, `focusInvalid`, `dayWord`, `F_UNCOLLECTED`, `F_PAYMENTS`,
  `isQuickOut`, `moneyOf`, `MoneyBlock`, `MoneyRateNote`, `OutButton`, `ReasonDialog`, `WriteOffDialog`, `PaidAmount`,
  `PaymentMenu`, `VoidDialog`, `DebtDialog`, `UnpaidRow`, `CustomerMenuItems`, `CustomerActions`,
  `EditCustomerDialog`, `ArchiveDialog`; `desk-sheet.jsx` — `F_HOURS_GEN`, `F_DAYS_GEN`; `Desk.html` — `UNPAID_SHOWN`,
  `RESULTS_MAX`, `PresentRow`, `SearchResults`; `Customers.html` — `STATUSES`; `Customer file.html` — `filePays`,
  `fileInitial`; `Payments.html` — `monthRange`, `month0`, `voidInitial`. Before adding any other, grep it across
  `masaha/*.jsx` and the page. **`O`, `D`, `DK`, `D5`, `DS5`, `ME`, `$`, `Money`, `Row` already exist** — never
  redeclare them (`Customer file.html`'s top-level `c` is its own; functions that need a customer use a local `c`).
- **Hooks** are called unconditionally and before any early return: `SubscriptionSheet` calls all its `useState`,
  `useRef`, both `useActionRun` and both `useEffect` before `if (!dlg) return …`; `CheckoutDialog`'s `useActionRun`
  is before its early return; never `useIsTablet() && !useIsDesktop()` (batch 5's crash).
- **The design system's names.** `Button` variants are `primary · secondary · outline · ghost · destructive · link`
  and sizes `sm · md · lg · icon`; leave `size` unset for the default (`md`). `"default"` is **neither** — it draws a
  button with no height or colour. The pages' imports: each page destructures the components it uses; a component
  used and not destructured blanks the page (batch 5's `RadioGroup`). This plan's page scripts list their imports;
  the modules use `DK.`/`DS5.`.
- **The prebuilt CSS.** A class not in `_ds_bundle.css`, `styles.css` or `masaha.css` is silently dead.
  `check-classes.mjs` must pass — it reads `className={'…'}` strings too, so `desk-unpaid` waits for commit 4's rule.
  Dead and **not** to be used: `line-through` (use `strike`), `opacity-60`, `order-first`, `xl:order-none`,
  `underline`, `list-none`, `border-s-2`, `md:table-cell`. Conditional classes used here, all present: `hidden`,
  `xl:flex`, `md:flex-row`, `md:items-center`, `md:justify-between`, `text-body-sm`, `text-caption`,
  `text-muted-foreground`.
- **The vendored bundle** (`prototype/_ds/`, `_vendor/`) is never edited.
- **Truth to the API and the data model.** A payment is never edited or deleted — only voided, with who and why, and a
  voided one counts nowhere (not in «دفعاتي اليوم»'s figures); a visit's and a fixed subscription's payments never
  exceed its charge (the change is handed back, never recorded); credit only on a usage-based subscription; a visit
  left unpaid has a phone or a customer; a write-off is not a payment and deletes nothing; a customer is archived,
  never removed (`archived`, not `splice`); **live status is a state, never a public count** — «27 / 40» is staff-only;
  no weekday in a subscription (K5); no online payment, QR or booking (*Not in v1*).
- **Look with your eyes.** The scripts and the pass see blanks, errors and overflow, not layout: the scratch build of
  this plan found two layout faults only by looking (a «⋯» orphaned in the narrow side column; buttons collapsed by an
  unknown size). Every changed page at 390, 768 and 1440.
- **Git Bash's path conversion** turns an argument that starts with `//` into a path; if a command must pass one, set
  `MSYS_NO_PATHCONV=1`. Never `cd` into `node_modules`.
- **Never commit images; never merge; stop every server, Chrome and shell you start.**

---

## 10. Decisions needed from the owner

1. **S1–S17:** approve as recommended, or name the ones to drop. S1 (the student switch hidden by default), S8 (the
   twelve relabels) and S11 (the sample's changes) matter most.
2. **DI-41–DI-47:** record as routed (recommended) — DI-41 and DI-47 to the docs with step 7; DI-42 to the API/web
   worker; DI-43 to worker A; DI-44–DI-46 for a later prototype item.
3. **Where to build:** `C:\Users\basel\masaha-design-b` (recommended; batch 5's worktree is cleaned when #76
   merges), or name another.
