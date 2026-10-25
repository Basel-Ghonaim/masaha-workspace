# DESK_SCREENS PR 4 — `feat/subscription-sheet` — the executor's report (written as it goes)

Executor: Claude Code (Opus 5.5), 2026-10-26, under `_SHARED\AUTONOMY_2026-10-25.md` (no stop until ready for review).

## What was read
`3_EXEC_PROMPT_PR4.md` whole; `_SHARED\AUTONOMY_2026-10-25.md`; `0_CARRIED_FROM_122.md` whole; `6_REVIEW_PR3_CLAUDE_CODE.md`
F1–F4; `2_PLAN.md`'s approval note, header, §1, §2 (PR 4), §3 *What the reading changed*, §4, §5, §6 (spec D), §7, §8 (PR 4),
§9 (PR 4), §10 (opening, PR 4 commits 1–4), §11 (PR 4, test 40, Review Focus), §12, §13; `4_REPORT_PR3.md`'s departures,
real run and decisions. In the repository: the contract's *Customers (managed)* and *Subscriptions (managed)*,
`GET /manage/spaces/:spaceId`; `packages/shared/src/{desk,customers,subscriptions,payments,packages,spaces}`; findings 101,
124, 125, 171 and the index; the desk feature's code, as each step needed it.

## Preconditions and first checks (§13)
- `origin/main` = `3855e37f` (#122 merged); `git status --short` empty; `git log -1` at `origin/main`. Docker up.
- **Base diff** `358765e3..origin/main`: only #121's files (favourites, data reports: merged before #122, absent from PR 3's
  unrebased head) — no file this PR touches. From `104d9d07`: `packages/shared` changed in `desk/requests.ts` (spec D),
  `subscriptions/requests.ts`, `payments/*`, `auth`, `core/errors`, `directory`, `data-reports`, `favorites`.
- **Spec D as built (#118)** against §10: `subscribeSchema` = exactly one of `packageId`, `published`, `custom`
  (`invalid_choice` on `packageId`); `published: { period: 'WEEK'|'MONTH', audience, shiftId?, name }` (1–60), never a
  `priceId`; a price not found → 422 `invalid_choice` on `published`. `NewSubscription = { subscription, payments:
  { item, payment }[], debtAgorot }`; `SubscriptionStatement.renewal: { startsOn } | null`. The space's prices: `AdminSpace.prices:
  Price[]` (`period`, `audience`, `shiftId`, `labelAr`, `labelEn`, `amountAgorot`), read by `GET /manage/spaces/:id` (🧾 — reception
  reads it). `Customer`, `createCustomerSchema` `{ name, phone? }` unchanged. Recorded as departures below where §10 differs.
- **Check o:** `useSpaceShifts('owner', id)` reads `GET /manage/spaces/:id` (the owner's editor scope, 🧾): reception may read it.
- **Open PRs:** none at the start (`gh pr list --state open` → `[]`). Worker B's `feat/closure-extension` exists locally only.
- **Finding numbers:** the index's highest is 171; 160–164, 170, 171 taken; the next free is 165 (none planned: spec D taken).
- Branch: `git switch --no-track -c feat/subscription-sheet origin/main`.

## Carried from #122 (`0_CARRIED_FROM_122.md`)
Memory before the first run 4 427 548 KB free; an `app-b` node process ran (pid 5556; not a vitest of mine, never stopped).
1. **`0b022eea` fix(desk): return the focus after edit and archive (50)** — F1 confirmed real. New
   `components/menu/CustomerActions.component.test.tsx` (a file beyond the carried note's "62 or 63, or CustomerMenu's": the
   focus is `CustomerActions`' own, and only it mounts both dialogs from the menu). Red before the code
   (`scripts\p4-red-k1.txt`): "× gives the focus back to «⋯» once the edit is saved", "× gives the focus back to «⋯» once the
   owing archive's question is left" — `expect(element).toHaveFocus()`, "Tests 2 failed (2)" (a first run failed on my
   matcher missing the name's isolates; fixed in the test). The fix: `CustomerMenu` takes `triggerRef`; `CustomerActions` keeps
   the ref and passes `returnFocus` to both dialogs. Green: `components/menu` "Test Files 2 passed (2) · Tests 5 passed (5)".
2. **`c64c1db9` fix(desk): compare the edited phone normalised (46)** — `prepare` compares `normalisePhone(typed) ?? typed`
   (`@masaha/shared/core`, the normaliser `phoneSchema` applies). Red: "× sends nothing for the same number typed in its local
   form" ("Unable to find an element with the text: Nothing changed", `p4-red-k2.txt`); green "Tests 6 passed (6)".
3–4. **`18a47540` test(desk): retitle the idle test; archive present (50)** — test 67's second title now "says no idleness for a
   session refused otherwise; says it for a restore the server ended for idleness" (unit `refresh` "Tests 10 passed (10)"). F4's
   case "says a settled customer present is checked out first, in the at-once archive's toast" passes on the code (it tests
   existing code); **its break** — `lines` dropped from `archiveSettled`'s `toastFailed` — red: "× says a settled customer present
   is checked out first…", "Tests 1 failed | 5 passed (6)" (`p4-break-k4.txt`); restored from `bak-p4-k4.ts`.
- `npm run lint` exit 0; `npm run typecheck` exit 0.

## Commit 1 — `d2fbe2b5` feat(design-system): open the end sheet full width (50) — 6 files
- Test 69 (`Sheet.component.test.tsx`, "takes the full width below 768 px from either side, a quarter less from there on"):
  red before the code — "expect(element).toHaveClass("w-full md:w-3/4 md:max-w-sm")", "Tests 1 failed | 9 passed (10)"
  (`p4-red-c1-69.txt`); the red step is the plan's break (`w-3/4` kept). Green with `Sidebar`'s tests: "Test Files 2 passed (2) ·
  Tests 21 passed (21)". The width itself is measured in the real run (390, 768) with its own break.
- `start` and `end`: `w-full … md:w-3/4 md:max-w-sm`; `SheetBody` `min-w-0`. Docs: `foundation.md` §12's Sheet row; finding 101
  Resolved (status, *Resolution*, moved in the index); **beyond §9:** `packages.md`'s decision line and open-findings list (it named
  101 as open). The dashboard's phone sidebar keeps its own `w-72`; the site's start-side menu becomes full width on a phone (as S12
  says for `start`).
- check:links exit 0 ("2842 links … all resolve"); lint 0; typecheck 0.

## Commit 2 — `cfd74218` feat(packages): offer the packages to the desk (46) — 4 files
- Test 70 (`useOfferedPackages.component.test.tsx`): red — "TypeError: useOfferedPackages is not a function", "Tests 2 failed (2)";
  green "Tests 2 passed (2)". Its break (retired kept: the filter removed) red — "× lists the offered packages only, in the list's
  order", "Tests 1 failed | 1 passed (2)" (`p4-break-70.txt`); restored from `bak-p4-break-70.ts`.
- **Departure:** the failure case uses a 403 (sent once); a 500 is re-sent by the transport with its pause, past `waitFor`'s second.
- Docs: `packages.md` (*Who uses it*, the code map, *Web history*). lint 0; typecheck 0.

## Commit 3 — `03a7417d` feat(desk): subscribe a new or known customer (45) — 49 files
- **Red before the code:** 71 (`endOf`, `packageLine`) "TypeError: endOf is not a function", "Tests 3 failed (3)"
  (`p4-red-c3-71.txt`); 72 (`sheetRequest`) "TypeError: sheetSchema is not a function", "Tests 4 failed" (`p4-red-c3-72.txt`);
  the repository's case "TypeError: repository.createCustomer is not a function", "Tests 1 failed | 9 passed (10)". Green: 71 with
  `termsLine` "Tests 5 passed (5)"; 72 "Tests 4 passed (4)"; repository "Tests 10 passed (10)".
- **Tests 73–75 and 77 were written after the hook and the sheet** (a departure from "red first": the hook had to exist for the
  harness). Their first runs failed on my matchers (the isolates around a button's amount) and on one real gap (an empty reason
  said "This is too short." — now «هذا الحقل مطلوب.», `fieldLines`). Each is proven by its break instead, every one seen red:
  - 73 [role] «مخصّص» always offered → "× offers «Custom» only to whoever may type a price", "Tests 1 failed | 5 passed (6)";
  - 74 [key] one key for both → "× creates a new customer then subscribes them with two keys; a refused subscribe keeps the
    customer and is sent alone", "Tests 1 failed | 5 passed (6)";
  - 75 [money] the toast's price from the form → "× asks the prior debts plus the new price; the toast says the price, the parts
    and the debt from the answer, with the debt warning", "Tests 1 failed | 5 passed (6)" (also the supervisor's finding-171 test:
    the answer charges ₪160 where the sheet showed ₪150, and the toast says ₪160);
  - 77: the plan's break (autofocus off) **stayed green** — Radix's sheet focuses its first field itself, so the `autoFocus` was
    dead and is removed; the break that can change it, `onOpenAutoFocus` prevented, red: "× is titled by its mode, its first field
    focused", "Tests 1 failed | 3 passed (4)" (`p4-break-77b.txt`). A departure.
  - 71 off by one (`addDays(start, validityDays)`) → "AssertionError: expected '2026-12-01' to be '2026-11-30'"; 72 custom with
    `packageId` → "× sends custom terms with their reason, and no package", "Tests 2 failed | 2 passed (4)".
  Every break restored from its copy (`scripts\breaks_p4.py`, `bak-p4-break-*`).
- After the entries: `features/desk`, `features/packages`, `pages/dashboard` component "Test Files 43 passed (43) · Tests 224 passed
  (224)" (free memory 6 123 308 KB, no `app-b` vitest); unit `features/desk`, `shared/copy` "Test Files 21 passed (21) · Tests 86
  passed (86)" (test 40's parity included); lint 0; typecheck 0; check:links 0; format:check 0; check:classes 0.
- **Departures in commit 3:**
  - **The form:** one `useServerForm` whose schema is `sheetSchema(newCustomer)` — `createCustomerSchema` on the name and phone,
    `subscribeSchema` on the rest — so each field's error lands at the path the server names (`custom.reason`, `phone`, …).
    `SheetEntry`'s known customer is `Customer & { debtAgorot }` (§10: `& CustomerBalance`): the file's header and a list row hand
    only the debt; the sheet reads the file again for the items.
  - **`SheetChoices`** (beyond §9's types): what the page passes — the packages' state, list and retry, and the shifts.
    `mayTypePrice` is read by the sheet itself from `visit-terms` (the desk's own query), not passed by the page.
  - **Two page files beyond §9:** `pages/dashboard/space/SubscriptionSheetSlot.tsx` (the sheet with `packages`' and `spaces`'
    reads, mounted only while open) and `useSheetOpener.ts` (the page's one sheet and its opening count), shared by the three pages.
  - **Entries:** «زبون جديد» is a top-bar action on «مكتب الاستقبال» (in its «⋯» on a phone) and on «الزبائن» (not inside the list's
    toolbar: one place for a page's action, as the desk's); «زبون جديد باسم «X»» / «زبون جديد بهذا الرقم» a `link` button beside
    the visit's in the search (`useDeskSearch` gains `newCustomer`, a file beyond §9); «اشتراك جديد» an item of every customer's «⋯»
    (`CustomerMenu`, `CustomerActions`, `CustomerCard`, `CustomersList`, `CustomerFile`). Six existing tests pass the new
    `subscribe` prop.
  - **Dates:** the layer's `Input type="date"` for the start and a custom end (not the `DatePicker`: the smaller change; the start
    defaults to today, Gaza).
  - **DI-37's half state:** the footer's submit becomes «حفظ الاشتراك» (no separate button) and a warning `Alert` says the line.
  - **Copy beyond §10:** `sheet.close`, `entry.new/subscribe/renew`, `rate`, `custom.limitNames`, `prior.item`, `done.charged`
    («{name} · {amount}», the server's price), `done.part` («{item}: استُلم {amount}»), `done.earlier` («دين سابق»). The Arabic
    example phone written with the catalogue's own `⁦…⁩` escapes. `prior.total` not used (the total is in the title).
  - `termsLine` takes the five fields it reads (`Pick`), so a package passes too (file beyond §9).
- Docs: `desk.md` (*Web decisions* ×5, code map, *Web history*), `customers.md` (*Who uses it*), finding 125 Resolved (status,
  *Resolution*, the index).

## Commit 4 — `85cbe358` feat(desk): renew a subscription with its debts (47) — 24 files
- **Red before the code:** `sheetRequest`'s published case "× sends a published price by its key and the name the desk gives
  it, never a price id" ("AssertionError: expected false to deeply equal { subscription: { …(3) } }", `p4-red-c4-72.txt`); green
  "Tests 6 passed (6)". The renewal (76), the published subscribe, finding 171's two refusals, `publishedChoices` and
  `useSpacePrices` were written with or after their code; each proven by a break seen red:
  - 76 [state] the start computed (the statement's start not applied) → "× renews from the statement's start, with the renewed
    one; a renewal renewed meanwhile is worded", "Tests 1 failed | 9 passed (10)";
  - 171, prices not read again on the refusal → "× says a published price changed or removed, keeps the sheet, and reads the
    prices again", "× says a published price now lower than the amount, …", "Tests 2 failed | 8 passed (10)";
  - 171, the refusal's line not worded → "× says a published price changed or removed, …", "Tests 1 failed | 9 passed (10)";
  - 171, the prices not read afresh on opening (`refetchOnMount: 'always'` removed) → "× reads the prices again each time a
    screen opens, never showing the older read meanwhile", "Tests 1 failed (1)";
  - `publishedChoices` with custom-labelled prices kept → "× offers the standard week and month prices, named, sent by their
    key", "Tests 1 failed (1)"; `sheetRequest` with `published` dropped → "Tests 1 failed | 5 passed (6)".
- Head of commit 4: component `features/desk`, `features/packages`, `features/spaces/hooks/editor`, `pages/dashboard` "Test Files 50
  passed (50) · Tests 263 passed (263)" (free 5 982 508 KB); unit `features/desk`, `shared/copy` "Test Files 22 passed (22) · Tests
  89 passed (89)"; lint 0, typecheck 0, check:links 0, format:check 0, check:classes 0.
- **Departures in commit 4:**
  - **The prices' read** is `spaces`' new `useSpacePrices(place, spaceId)` (the editor's query, `refetchOnMount: 'always'`, nothing
    shown while it reads) with its own test; the page's `SubscriptionSheetSlot` passes it (`SheetChoices.prices`). Files beyond §9.
  - **`publishedChoices`** (a service beyond §9, with its unit test): the standard WEEK and MONTH prices; the value
    `price-{period}-{audience}-{shiftId|none}`; **the name sent is the line's title** — «شهري», «شهري · للطلاب», with the shift's
    name when it has one — so two published subscriptions stay told apart in a customer's file (the prompt's "the chosen word").
  - **Where «تجديد» is offered:** the file's latest subscription's card (the file's first), for a customer not archived. The search's
    pre-check-in dialog and the card's «⋯» do not offer it (its «اشتراك جديد» does a new one).
  - **The renewal's start** is applied when the statement answers; the submit waits for it. A renewal of a subscription made from a
    published price (no package, no typed price) offered no "current" line and chose the first — **corrected in the fix round (F3)**:
    it is matched back to its published line, and nothing is chosen when nothing matches.
  - **Copy beyond §10:** `sheet.published.gone` (finding 171's refusal line); `groups.published`, `published.WEEK/MONTH/students`,
    `changePackage` are §10's.
  - **Documents beyond the plan's list:** `spaces.md` (*Who uses it*, the code map, *Web history*) and `overview.md` (the Customers
    line: the dashboard's customers list, file and sheet — true since #122 and this PR).

## On the head (`85cbe358`, before the run's fix) — outputs `scripts\h4-*.txt`
- No `vitest` of `app-b` running (count 0); free memory 5 958 988 KB, then 5 921 644 KB.
- `npm run test:unit -w @masaha/web` → "Test Files 139 passed (139) · Tests 989 passed (989)" (exit 0).
- `npm run test:component -w @masaha/web -- src/features/desk src/features/packages src/features/spaces
  src/shared/design-system src/pages/dashboard src/shared/session src/shared/copy` (`src/features/spaces` added: commit 4 changes
  it) → "Test Files 106 passed (106) · Tests 706 passed (706)", 201 s (exit 0). Finding 87's family did not miss.
- `NODE_ENV=production npm run build` exit 0; `npm run check:build` exit 0 — "No showcase code in 57 build files", "No dashboard code
  in the site's first download.", "No data-table or leaflet, nor Leaflet's stylesheet, in the site's first download."; `check:classes`
  exit 0 ("… in 1444 files"); `format:check` exit 0; `check:links` exit 0 ("2848 links … all resolve"); `check:conflicts` exit 0.

## The real run (2026-10-26; local headless Chrome over CDP, `scripts\run4.mjs` on `scripts\cdp4.mjs`, PR 3's model)
- `docker start masaha-postgres-1`; `prisma migrate status` "Database schema is up to date!"; API on 3320 (`/health` ok, db up),
  web on 5320, from `C:\dev\masaha\app`, worker A's `masaha_dev`.
- **Inventory** (`scripts\inventory4.mjs`, GETs only → `inventory4.out.txt`): space 7's offered packages 5, 2, 4, 1, 3 (6 retired);
  published prices WEEK GENERAL ₪120, MONTH GENERAL ₪350, MONTH GENERAL shift 1 ₪250 (and HOUR/DAY); shifts 1, 2, 5; the owner may
  type a price, reception may not; «محمد عوض» (2) owed ₪50 on subscription 2 («أسبوعان، 6 أيام», EXPIRED), its statement's `renewal`
  2026-10-26; «رامي سالم» (5) with no subscription and no debt, for the owner's «مخصّص».
- **Carried F1, live** (`carried`, owner, reads only): «⋯» of «خالد» → «تعديل البيانات» → Escape → the focus on "إجراءات أخرى: خالد";
  «⋯» → «أرشفة…» (he owes ₪15) → the question → «رجوع» → the focus on "إجراءات أخرى: خالد". Shots `4-carried-edit-…`,
  `4-carried-archive-…`. (The edit was closed, not saved: a save would be a write the list does not name.)
- **S12 at 390** (`widthshot`): the sheet 390 px wide in a 390 px viewport (`4-width-reception-ar-light-390.png`).

### A slip in the real run — two writes not on the list (2026-10-26, ≈13:30Z)
The `touch` case (meant to read only) opened «محمد عوض»'s renewal and clicked «تغيير الباقة». **That button had no
`type="button"` inside the sheet's form, so it submitted it:** the first run renewed subscription 2 (new subscription **5**,
2026-10-26..2026-11-08, ₪150; the payment of ₪200 allocated ₪50 to subscription 2 and ₪150 to 5 — his debt now 0), and a second run
of the case (before I had looked) renewed subscription 5 (new subscription **6**, 2026-11-09..2026-11-22, ₪150 paid). Read back with
`inventory4.mjs` (GETs only). **Nothing was undone** (it would take more writes; reseeding is forbidden). The owner may end or keep
them. **The defect it found is fixed:** both of `PackageOptions`' buttons («تغيير الباقة» and the choices' «إعادة المحاولة») are now
`type="button"`; two tests, seen red first ("× shows every choice on «Change package», and sends nothing" and "× reads the choices
again on «Try again» when they failed, and sends nothing" — "expected [ { …(3) } ] to deeply equal []", "Tests 2 failed | 10 passed
(12)", `p4-red-fix-buttons.txt`), green "Test Files 2 passed (2) · Tests 16 passed (16)"; lint 0, typecheck 0 (only these files'
tests re-run, the rule for a fix after a lane passed). Folded into commit 4 (`--fixup` + autosquash): **`b0833303`**. The retry's
button was commit 3's; its fix rides in commit 4 with the change button's (one test harness change) — a departure.

### The real run's cases (after the fix; the web served the fixed tree)
- **Touch targets at 390** (`touch`, reception, touch emulation; reads only, re-run after the fix — the inventory then showed no new
  subscription): «تغيير الباقة» 44, «نقدًا» / «تحويل» 44, «لم يدفع شيئًا» 44, the submit 44, «إغلاق» 44; the choices' rows 68; the
  inputs 42 (the layer's field height; DI-16 names the row actions). `4-touch-reception-ar-light-390.png`.
- **New customer on the published «أسبوعي», paid in full** (`newcustomer`, reception, ar, 1440 — PR 4's write): «مشترك تجربة», the
  listed phone; the sheet listed «منشورة للزوار» (أسبوعي ₪120 · 7 أيام, شهري ₪350, شهري · صباحي ₪250) first, then «باقات المساحة — لا
  تظهر للزوار»; no «مخصّص» for reception. The subscribe was **blocked once** (`Network.setBlockedURLs`, no answer): the sheet said
  «أُضيف مشترك تجربة إلى الزبائن؛ لم يُحفظ الاشتراك.», «لم يصل الرد. أعد المحاولة — لن تُسجَّل مرتين.», the submit «حفظ الاشتراك»
  (DI-37 live, with no refused write); unblocked, «إعادة المحاولة» → saved; toast «حُفظ الاشتراك · مشترك تجربة | أسبوعي · ₪120 |
  أسبوعي: استُلم ₪120». Shots `4-newcustomer-{filled,half,done}-reception-ar-light-1440.png`. **Network** (`shots\pr4\4-newcustomer-network.txt`, the phone masked):
  - `13:28:52.812Z POST …/customers 201 Idempotency-Key: eb824386-…` body `{"name":"مشترك تجربة","phone":"<phone>"}` — customer 9;
  - `13:28:52.940Z`, `13:28:53.963Z`, `13:28:55.970Z POST …/customers/9/subscriptions failed () Idempotency-Key: 1abda1a7-…` (the
    transport's two re-sends, then «إعادة المحاولة» after unblocking):
  - `13:28:56.122Z POST …/customers/9/subscriptions 201 Idempotency-Key: 1abda1a7-…` body
    `{"published":{"period":"WEEK","audience":"GENERAL","name":"أسبوعي"},"startsOn":"2026-10-26","payment":{"amountAgorot":12000,"method":"CASH"}}`.
  **Two keys, each kept across its retries; `published` with its name and no `priceId`; the payment the amount recorded (12000).**
- **The owner's «مخصّص» with a reason** (`custom`, owner, ar, 1440 — PR 4's write) on **«رامي سالم» (customer 5)**: «⋯» → «اشتراك جديد»
  → «مخصّص» (offered: the owner may type a price) → the terms (name «مخصّص», الجميع, سعر ثابت, the limits, the shifts «بدون وردية ·
  صباحي · مسائي · مسائية», the reason), price 80, reason «عرض المالك لتجربة الأسبوع» → toast «حُفظ الاشتراك · رامي سالم | مخصّص · ₪80 |
  مخصّص: استُلم ₪80». Network: `13:29:18.656Z POST …/customers/5/subscriptions 201 Idempotency-Key: f250b8c8-…` body
  `{"custom":{"name":"مخصّص","billing":"FIXED","priceAgorot":8000,"audience":"GENERAL","reason":"عرض المالك لتجربة الأسبوع"},"startsOn":"2026-10-26","payment":{"amountAgorot":8000,"method":"CASH"}}`.
- **«محمد عوض»'s renewal with his debt, paid in part — NOT PERFORMED as planned.** The slip above had already renewed him twice (the
  first renewal paid his ₪50 debt in full, ₪200 over subscriptions 2 and 5); a third renewal would be a further write. What the case
  shows is proven by tests 75 (the parts and the debt from the answer) and 76 (the statement's start, `renewalOfId`,
  `SUBSCRIPTION_ALREADY_RENEWED`), and the renewal sheet is shown live in the layouts (one line, «تغيير الباقة», the start from the
  statement: 2026-11-23 for subscription 6).
- **Layouts** (`layouts`, reads only): reception's «زبون جديد» from the desk (the top bar from 768 px, the «⋯» at 390) and the owner's
  renewal of «محمد عوض»'s latest subscription, × Arabic light / English dark × 390, 768, 1440 — `4-new-reception-<tag>.png`,
  `4-renewal-owner-<tag>.png` (12 shots). The sheet's measured width: **390 of 390** at 390; **384** at 768 and 1440 (S12).
- **The width break** (`break-sheet-width.png`): removing `w-full` alone left the sheet 390 wide (its content fills a fixed panel), so
  that break cannot show the rule; the break that can — the old `w-3/4 max-w-sm` below 768 put back — showed **293 of 390**.
  Restored from its copy (`bak-p4-sheet-width.tsx`), `git status` clean. A departure (the break made differently).
- Servers stopped by process id (24780, 25984, 2508, 9912); 3320 and 5320 free.

## #PRNUM, push and the PR (2026-10-26)
- Open PRs just before the push: **#123** (worker B, `feat/closure-extension`, head `ff8743c8`). Shared files with this PR:
  `docs/features/subscriptions.md`, `docs/project/overview.md` (each side its own lines); `git merge-tree --write-tree HEAD
  origin/feat/closure-extension` → clean. No `errors.ts` edited here. Whichever merges second rebases, keeping both.
- The issues API's last number → 123; next **124**. `scripts\prnum4.sh 124` (PR 3's script, its branch, backup and description
  adapted, its checks kept) → "PRNUM OK #124 bc8fe86a (was b0833303)"; `git grep '#PRNUM' HEAD` empty. Checked again just before the
  push: 123. Local backup branch left: **`backup/subscription-sheet-pre-prnum`**.
- Final shas: `0b022eea`, `c64c1db9`, `18a47540` (carried), `96aad426` (1), `f5c0e0b6` (2), `75922ac8` (3), `bc8fe86a` (4).
- `git push -u origin feat/subscription-sheet`; `gh pr create --assignee @me --label feat --label area:web --label area:docs --label
  area:design-system`, title `feat(desk): subscribe a new or known customer`, description `scripts\pr-body-4.md` →
  **https://github.com/Basel-Ghonaim/masaha/pull/124** — the number answered equals the commits'.
- **Files: 70** (40 code, 20 tests, 10 documents), past the plan's ≈ 40 + the carried 8. Why it grew: the sheet's
  entries reach five existing components and three pages (+ two page files), spec D adds a `spaces` read and a service, six existing
  tests pass the new `subscribe` prop, and three documents beyond the plan's list (`spaces.md`, `overview.md`, `packages.md` in
  commit 1).

## Data left in `masaha_dev` (space 7)
- **Listed writes:** customer **9** «مشترك تجربة» (the listed phone) with its subscription from the published «أسبوعي» (₪120 paid,
  cash); «رامي سالم» (5)'s custom subscription «مخصّص» (₪80, reason «عرض المالك لتجربة الأسبوع», ₪80 paid, cash).
- **Not listed — the slip:** «محمد عوض» (2)'s subscription 2 renewed as **5** (2026-10-26..2026-11-08, ₪150; ₪200 received: ₪50 to
  subscription 2, ₪150 to 5) and 5 renewed as **6** (2026-11-09..2026-11-22, ₪150 paid). Left as they are; the owner decides.
- The listed «محمد عوض» renewal paid in part was not made (see the real run). Nothing else written: the carried case closed its
  dialogs, the layouts and the touch case read only (after the fix).

## Decisions taken without the owner (under `_SHARED\AUTONOMY_2026-10-25.md`)
1. **Finding 171 — the supervisor's decision for this run** (the prompt §2.8). Met: a published price changed between the read and
   the subscribe is charged silently. Options: an `amountAgorot` the server compares (API work); the sheet reading the prices again
   before confirming; accepting the silent charge. Chose (the supervisor's): no API change — the sheet reads the prices afresh each
   time it opens (`useSpacePrices`, `refetchOnMount: 'always'`, nothing shown from an older read), the toast says the price from the
   answer, a refusal for the price is worded and reads them again; finding 171 left Open with no line added. Undo: the owner takes
   the API option; the web then sends the amount and words its 409.
2. **The slip's two renewals.** Met: a read-only case submitted the sheet twice through a button that sent the form. Options: undo
   with more writes (ending subscriptions 5 and 6 — still writes, and the payments stay), reseed (forbidden), leave them. Chose: leave
   them, say so here and in the PR, and fix the defect with tests. Undo: the owner ends 5 and 6, or reseeds the local demo data.
3. **«محمد عوض»'s renewal paid in part not performed.** Met: after the slip, a third renewal would be another write. Chose: not
   performed; tests 75 and 76 prove it. Undo: the owner allows that write and the case runs.
4. **The published price's name** is the line's title («شهري · للطلاب», with a shift's name), not the bare word: two published
   subscriptions stay told apart in a file. Undo: send `words.published[period]` alone (`publishedChoices`).
5. **Where «زبون جديد» and «تجديد» live**: the page's top bar on «الزبائن» (not the list's toolbar), and «تجديد» on the file's latest
   subscription only. Undo: move the button into `CustomersFilters`; offer «تجديد» in the «⋯» or the pre-check-in dialog.
6. **Dates with the layer's `Input type="date"`** rather than the `DatePicker` (the smaller change). Undo: swap in `DatePicker`.
7. **Breaks that stayed green, made differently:** 77's autofocus (Radix focuses the first field; the dead `autoFocus` removed, the
   break `onOpenAutoFocus` prevented, red); the width break (`w-full` removed alone keeps 390 px; `w-3/4 max-w-sm` put back below 768
   shows 293). Undo: none needed.
8. **Tests written after their code** (73–77, the renewal, spec D's): each proven by its break seen red instead of a red-first run.
9. **The retry button's fix rides in commit 4** with the change button's (one test harness change), though the retry came in
   commit 3. Undo: split the fixup.

## CI and the end (2026-10-26) — the final report (the `final-report` skill's order is this file's sections above)
- `gh pr checks 124` on head **`bc8fe86a`** (run 40331873286, its head SHA the branch's): **all pass** — build 47s, check:classes
  34s, check:conflicts 25s, check:links 32s, format:check 38s, lint 2m23s, test:api 7m23s, test:component 13m20s, test:unit 1m49s,
  typecheck 1m2s, CodeRabbit (rate limited, pass). `gh pr view 124 --json mergeStateStatus` → **CLEAN**.
- Not run locally, CI judged on the head: the full `test:component` — pass; `test:unit` of `apps/api` and `packages/shared` — pass;
  `test:api` — pass.
- **Early conflict check:** open PRs #124 (this) and **#123** (`feat/closure-extension`, head `ff8743c8`): `git merge-tree
  --write-tree bc8fe86a origin/feat/closure-extension` → clean. Shared documents: `subscriptions.md`, `overview.md`.
- **Unexpected, noted:** the real run's slip (a button inside the sheet's form sent it; two renewals on the local data) — solved in
  the code, the data left as it is; removing `w-full` alone does not narrow the sheet (its content fills the fixed panel); Radix
  focuses the sheet's first field without `autoFocus`.
- `git status --short` clean; no rebase in progress; both servers stopped by process id; 3320 and 5320 free. Local backup branch
  left: `backup/subscription-sheet-pre-prnum`. Never merged; no Issue created.

## The review's fix round (2026-10-26) — `7_FIX_ROUND_PR4.md`, the review `6_REVIEW_PR4_CLAUDE_CODE.md` F1–F6
- **Start:** `gh pr view 123` → OPEN; the fixes made on the old base. Checked again before the push → **MERGED** (`e6737da5`).
- **Each fix: its test red, then green** (only the touched test files, lint, typecheck, Prettier — no full lane, by the owner's rule):
  - **F1** (a lost answer is not a refusal): new tests "says no answer, not «not saved», when the subscribe's answer is lost, and
    retries with its key" — red: "AssertionError: expected <div …(2)></div> to be null" (the half title shown), "Tests 1 failed | 13
    passed (14)" (`p4r-red-f1.txt`); and "retries a lost subscribe with the same key, the customer not created again" (a guard, green
    on the code). Fix: `refusedAfterCreate` — set only when the subscribe's failure is neither `network` nor `timeout`; the half
    title, the «حفظ الاشتراك» label and the closing toast follow it. Green "Tests 14 passed (14)". The refused case (test 74, the
    closing toast) unchanged and green.
  - **F2** (the focus after the sheet): new case in `CustomerActions.component.test.tsx` — «⋯» → «اشتراك جديد» → Escape → the focus on
    «⋯»; red "expect(element).toHaveFocus()", "Tests 1 failed | 2 passed (3)" (`p4r-red-f2.txt`; a first run failed on my fake answering
    `null` for the file). Fix: `OpenSheet = (entry, from)`; `CustomerActions` hands its «⋯», the search's link, the top-bar buttons and
    «تجديد» their own control, the desk's phone «⋯» item its trigger (a ref); `useSheetOpener` keeps it and gives `returnFocus`;
    `SubscriptionSheet`'s `onCloseAutoFocus` focuses it while `isConnected`, else Radix's default; the comment says so. Green:
    the touched files "Test Files 9 passed (9) · Tests 45 passed (45)", then with `routes` "Tests 76 passed (76)".
  - **F3** (a renewal preselects what it renews): two tests in 76's file — "renews a subscription from a published price with that
    price chosen, its amount on the submit" (red: "Unable to find role=\"button\" and name \"Change package\"") and "chooses nothing
    for a renewal it cannot match, the submit blocked until a choice" (red: "expect(element).not.toBeChecked()"), "Tests 2 failed | 14
    passed (16)" (`p4r-red-f3.txt`). Fix: `publishedOf(renews, published)` — the line whose title is the subscription's name, else a
    fixed, unlimited one of the same audience, shift and 7/30-day span; a renewal's first choice is what it renews or `''` (the submit
    blocked while nothing is offered-and-chosen). Green "Tests 16 passed (16)". The report's departure corrected above.
  - **F4** (the money claim able to fail): "sends the amount recorded, never the amount typed: ₪200 on a ₪150 price records ₪150" and
    "… ₪100 … records ₪100" — green on the code ("Tests 18 passed (18)"); its break (the typed `money.amount` sent) red: "× sends the
    amount recorded, never the amount typed: ₪200 on a ₪150 price records ₪150", "Tests 1 failed | 17 passed (18)"
    (`p4r-break-f4.txt`); restored from `bak-p4r-f4.ts`. (The ₪100 case cannot fail under that break: typed equals recorded.)
  - **F5** (no empty choices on a focus refetch): `useSpacePrices`' new case "keeps the prices shown while the space is read again
    behind them, and hides them for a refresh" (the reads after the first held until the test releases them) — red at the focus step:
    "AssertionError: expected 'loading' to be 'ready'", "Tests 1 failed | 1 passed (2)" (`p4r-red-f5.txt`). Fix: hidden only while no
    read since mount answered (`isFetchedAfterMount`, the smaller change: it keeps finding 171's fresh read on every opening and the
    app's focus refetch) or while a `refresh` (after a refusal) runs. Green "Tests 2 passed (2)" (a lint error in my test's `void`
    cast fixed first).
  - **F6**: `desk.md`'s code map names `OpenSheet`, the page's `SubscriptionSheetSlot` / `useSheetOpener`, `hooks/sheet/`, the four
    services and `components/sheet/`. `check:links` exit 0.
  - lint 0 and typecheck 0 after each fix; Prettier clean on the touched files.
- **Folds:** all six fixups into `feat(desk): renew a subscription with its debts` (see the decisions), `GIT_SEQUENCE_EDITOR=: git rebase
  -i --autosquash 3855e37f` → no `fixup!` left; then `git rebase origin/main` (onto #123's merge `e6737da5`) — **no conflict**;
  `subscriptions.md` and `overview.md` hold both PRs' lines. `npm run build -w @masaha/shared` exit 0; `npx prisma migrate deploy`
  exit 0 ("All migrations have been successfully applied." — `closure_extension_key` on `masaha_dev`); `npx prisma generate` exit 0.
- **On the rebased head:** typecheck 0, lint 0, Prettier clean; the touched test files (`hooks/sheet`, `components/sheet`,
  `components/menu`, `useSpacePrices`) "Test Files 5 passed (5) · Tests 30 passed (30)".
- **Shas:** `0a48a175`, `36ff6f17`, `4373a1f9` (carried), `5f1aab5c` (1), `77ee53ae` (2), `8363726c` (3), **`5682764b`** (4). `git grep
  '#PRNUM'` empty. `git push --force-with-lease=feat/subscription-sheet:bc8fe86a…` → head `5682764b`. Files: 70. The PR's description
  gained *Review fixes* (`scripts\pr-body-4r.md`, `gh pr edit 124`). No real run (the owner's rule); the local data unchanged.

### Decisions taken without the owner (this round)
1. **Every fix folded into commit 4** (`feat(desk): renew a subscription with its debts`), F2 and F6 included. Met: the hook, the sheet,
   `SheetEntry`, the entries' call sites and the code map line all carry commit 4's lines beside the fix (commit 4 rewrote the hook
   and changed the same files), so a fixup into commit 3 would conflict in the autosquash, and commit 3 would then name a type
   (`OpenSheet`) that only commit 4's code needs. Options: split (conflicts), fold into 4. Chose: fold into 4. Undo: split the
   commit by hand.
2. **F5 by `isFetchedAfterMount` plus a `refresh`-own loading**, not `refetchOnWindowFocus: false`: the smaller rule keeps the
   app's focus refetch (fresher prices behind the sheet) and finding 171's read on every opening. Undo: turn the focus refetch off
   for this query.
3. **F3's match falls back to audience, shift and span** when the name does not match (a published subscription renamed, or made in
   the other language): only a fixed price with no limits matches that way. Undo: match by name only.
- **CI on `5682764b`:** all pass — build 47s, check:classes 29s, check:conflicts 31s, check:links 36s, format:check 38s, lint 1m58s,
  test:api 6m41s, test:component 21m0s, test:unit 2m37s, typecheck 45s, CodeRabbit. `mergeStateStatus` → **CLEAN**. Open PRs: #124
  only. No rebase in progress; `git status --short` clean; no new `backup/*` branch (the old `backup/subscription-sheet-pre-prnum`
  stays).
