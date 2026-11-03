# Review of #132 — R5: the front desk, the customers and the payments — Claude Code, Claude Opus 5.5
Head: a12c0790 · commits 21 · checks: green (all 10 pass, CodeRabbit skipping) · head moved during the review: no
Verdict for my range: mergeable after a fix round

Everything below was read from commit objects at `a12c0790` (the working tree of `app-design` is `e6737da5`, old
`main`, and was not used). Nothing was run, fetched or written except this file.

## Findings (verified defects only, most severe first)

### R5-F1 — should-fix · On a phone or tablet, an owner with nothing uncollected cannot reach «لن تُحصَّل» or its undo (finding 212 left open)
- Where: `apps/web/src/features/desk/components/uncollected/UncollectedCard.tsx:89` at a12c0790 (`card.state === 'empty' && !writtenOff ? 'hidden xl:flex'`); `docs/architecture/findings/212-an-owner-on-a-phone-cannot-reach-the-written-off-visits.md` (Status: Open)
- Seen in the code: the toggle to «لن تُحصَّل» sits in the card's header. When «غير محصّل» is empty the whole card, toggle included, is `hidden` below `xl`. The only way back into the view is `?writtenOffPage=` in the address. The lane saw this (LW3-D9 "gap") and recorded it as finding 212 rather than fixing it.
- Scenario: the owner writes off the space's last uncollected visit on a phone and closes the toast. The card is now empty and disappears below 1280 px. The written-off visit and its «تراجع» are now unreachable at 390 and 768 until another visit goes uncollected. That is the case 164 was opened for («a screen offers their undo there»).
- Fix: keep the card's header, with its toggle, below `xl` for the owner even when empty; hide only the empty body line. A test at a phone width, as 212's *Resolves when* asks. Then mark 212 Resolved and remove it from the index's *Open* list. The approval note says nothing carries, and §3.2 says *Open* holds exactly the deployment's six. · Belongs: a fix round on #132 (folded into `001c2501`, with 212's record dropped as the lead did for 206 and 210)

### R5-F2 — should-fix · A customer checked in as their visit (160) shows as «غير حاضر» on the search card, and their present row does not link to their file
- Where: `apps/web/src/pages/dashboard/space/desk/DeskPage.tsx:147` (`customerIds` built from `CHECK_IN` people only); `apps/web/src/features/desk/hooks/card/useCustomerCard.ts:25` and `components/card/CustomerCard.tsx:120` (the «غير حاضر» badge, shown unconditionally); root cause `packages/shared/src/occupancy/responses.ts:17` (a `VISIT` `PresentPerson` has no `customerId`)
- Seen in the code: `902dd226` makes «تسجيل كزيارة» send `customerId`, so a known customer can now be present through an open visit. The page only knows present customers through subscriber check-ins. So:
  - the search keeps that customer among its cards;
  - the card says «غير حاضر», offers «حضور», and puts them under "not present" in the pay dialog's `presentIds`;
  - their row in «الحاضرون الآن» and in the search's present group is not a link to the file.
  D7.8 says «غير حاضر» shows "when the customer is not present". LW3-D11 put it on every card instead, assuming present people never reach the cards; with 160 built in the same PR, that assumption no longer holds. LW3-D10 records the missing link for the same reason. The prototype (`masaha/desk-core.jsx:231`) shows «حاضر منذ …» (info) on a present customer's card and «غير حاضر» otherwise.
- Scenario: Sara's subscription has expired. Reception taps «حضور» → «تسجيل كزيارة», and her visit is recorded on her file. A minute later reception searches "Sara":
  - the present group lists "Sara", not as a link;
  - below it, Sara's card reads «غير حاضر» with «حضور».
  The screen says the opposite of what is true, and tapping «حضور» on a running subscription gets the server's `MEMBER_ALREADY_CHECKED_IN`.
- Fix: carry `customerId: number | null` on the `VISIT` `PresentPerson` (an answer change, no migration; the open visit's customer is already joined for its name). Add `VISIT` people with a customer to `customerIds`, and link their rows through `PresentName`. Show «غير حاضر» only for a customer the page does not hold present. Update the contract's `PresentPerson` line. · Belongs: a fix round on #132 (the shared/API part folded into `9f801981`, outside my range; the web part into `eaf2f978` and `3827ee48`)

### R5-F3 — should-fix · «استلام {amount}» and «أقدم بند: {item}» name the oldest visit, not the oldest owing item
- Where: `apps/web/src/features/desk/hooks/customer-actions/useStateActions.ts:141` (`const [oldest] = openItems(file, …)`), via `apps/web/src/features/desk/services/openItems.ts:55` (`return [...visits, ...subscriptions]`)
- Seen in the code: `openItems` puts every unpaid visit first (sorted by close time), then every owing subscription. The state action takes element 0 as "the oldest owing item" (DI32), and the pay dialog describes it as «أقدم بند: {item}». The server's own idea of oldest goes by `createdAt` across both kinds:
  - finance's `BalanceRow.oldestItem` (`payments.repository.ts:174`);
  - the subscribe's allocation (contract §Subscriptions: "the oldest first, a visit before a subscription made at the same instant").
- Scenario: a customer owes ₪200 on a monthly subscription made 2026-09-01 and ₪20 on a visit from yesterday.
  - Finance › Debts names the subscription as the oldest item; its «استلام دفعة» leads to the file (DI15).
  - The file's header then offers «استلام ₪20», described «أقدم بند: زيارة أمس».
  A false label on a money action, and different from what the screen the owner came from just said.
- Fix: choose the earliest owing item across both kinds by the date the file carries (a visit's close, a subscription's start, or add `createdAt` to `SubscriptionWithMoney`), matching the server's rule. Leave `openItems`' list order alone. Add a test with an older subscription and a newer visit. · Belongs: a fix round on #132 (folded into `84375a56`)

### R5-F4 — should-fix (plausible) · The customers list's «⋯» inserts its state items above the open menu once the file arrives, under the user's tap
- Where: `apps/web/src/features/desk/components/menu/CustomerActions.tsx:64` (`read: … state === 'menu' && menuOpened`) and `components/menu/CustomerMenu.tsx:55` (the state items rendered first)
- Seen in the code: the row's menu opens with «ملف الزبون» first. The file read starts only on open. When it answers, «خروج» / «حضور» / «استلام …» / «تجديد» are prepended, with no placeholder while it loads. «خروج» for a subscriber and «حضور» are one-tap writes, with no dialog.
- Scenario: the owner opens «⋯» on a present subscriber's row and taps the top item to open «ملف الزبون». If the file answers in between, which is the normal read time on a slow connection, the top item is now «خروج», and the tap checks the subscriber out. Keyboard users get the same effect: the item under the focus moves. Plausible, not reproduced: it depends on the read's timing. The insertion itself is in the code.
- Fix: reserve the state items' place while the file reads (a held, `aria-busy` item, or skeleton rows) so nothing moves under the pointer. Or start the read on the trigger's hover or focus and open the menu with the items already in place. · Belongs: a fix round on #132 (folded into `84375a56`)

### R5-F5 — nit · Every row of «لن تُحصَّل» has a button named only «تراجع»
- Where: `apps/web/src/features/desk/components/written-off/WrittenOffVisits.tsx:75`
- Seen in the code: the button has no accessible name of its own. The desk's convention names a row's control by its person (`checkInName`, `checkOut.openName`, the uncollected «⋯»'s `more({name})`).
- Scenario: with three written-off visits, a screen reader's button list reads «تراجع، تراجع، تراجع», and nothing says which visit each one undoes.
- Fix: `aria-label` «تراجع عن شطب زيارة {name} · {day}» in both catalogues. · Belongs: a fix round on #132 (folded into `001c2501`)

### R5-F6 — nit · With no saved template, the WhatsApp reminder's language follows the staff's interface, while the space's name is always Arabic
- Where: `apps/web/src/features/desk/hooks/file/useCustomerFile.ts` (the `reminder` block: `file.reminderTemplate ?? copy.spaceSettings.reminder.defaultText`) and `apps/web/src/pages/dashboard/space/customers/CustomerPage.tsx` (`space.nameAr ?? space.nameEn`)
- Seen in the code: the default text comes from the catalogue of whoever is signed in. The space's name is Arabic first (LW3-D13).
- Scenario: reception working in English sends an Arabic-speaking customer "Hi Sara, a reminder that ₪45 is due at مساحة النور…". The space's own default would be one language.
- Fix: fill the default from one language, the space's (Arabic) catalogue, or use `nameEn` when the English default is used. · Belongs: a fix round on #132 (folded into `f631ea57`)

## The checklist (lines 1–7, each answered)

**1. Every commit of my range read** (each with `git show`, files at the head where a later commit changed them: `useCustomerFile.ts`, `DeskPage.tsx`, `UncollectedCard.tsx`, `useSubscriptionSheet.ts`, `CustomerFile.tsx`, `FileHeader.tsx` were read at a12c0790):
- `f78c1f46` C7.1 — the write-off dialog places the focus on its reason (`onOpenAutoFocus`); 172 resolved.
- `62b90d57` C7.2 — «الآن | السجل»; `useDayLogQuery` reads both lists whole; `logRows` merges them; 20 a page.
- `2daa4143` C7.6 — DOM order search → uncollected → present; the empty card hidden below xl; the offline state.
- `15feecfd` C7.9 — full by `present ≥ capacity` with the ratio; `Switch`, deselectable shift chips; rate, cap and day-only lines; money block side by side from md.
- `ca8bce43` C7.10 — `usePhoneOwner` (400 ms, `limit=2`) in check-out and «تسجيل دين».
- `2e572b17` C7.11 — `limited` line on 429 in money dialogs; `PhoneInput` placeholder; icons; the large search.
- `5ed2e8b2` C7.12 — usage-based subscriber's check-out opens `UsageOutDialog` from the answer; fixed subscriptions stay one tap.
- `4a591222` C7.13 — `DateField`; `endNote`; the earlier-debt warning, its calc and «المجموع»; the published rate prefilled; «خاصة».
- `e7d0cd63` C7.14 — `visits.md` names the desk's screen.
- `001c2501` C7.3 — «لن تُحصَّل» view, `GET …/written-off-visits`, «تراجع» with no key and no retry; 164 resolved.
- `902dd226` C7.4 — «تسجيل كزيارة» sends `customerId`; the "not added to the file" note removed; 160 resolved.
- `f9be0553` C7.5 — `published.amountAgorot` sent; `PUBLISHED_PRICE_CHANGED` re-reads the prices and keeps the sheet; 171 resolved.
- `eaf2f978` C7.7 — subscribers' names link; plan badge; «زيارة · طالب»; time alone; «اختياري»; «ساعتين».
- `3827ee48` C7.8 — card progress, «غير حاضر», «تجديد» (statement read first); the pre-check-in's «تجديد» and «اشتراك جديد».
- `84375a56` C8.1 — `useStateActions` / `StateButtons` / `StateDialogs`; the list's «⋯» and the file's header.
- `f631ea57` C8.2 — «تذكير على واتساب» from `reminderTemplate` and `whatsappLink`.
- `71bcb39f` C8.3 — `paymentLines`: «سجّلها {name}» and «ألغاها {name}: {reason}» in the statement and on the file's unpaid visits; 162 resolved.
- `5d082659` C8.4 — `CorrectAction` / `CorrectSheet`: PATCH then PUT, only the changed fields; 163 resolved.
- `c0e37ea3` C8.5 — `KIND_ORDER` puts MONTH and WEEK first.
- `c60865c0` C8.6 — «زبون جديد» by the count and in the empty state; ranges; the file's write-off, «تُحسب في رصيده.», «حاضر منذ», the only-visits line; ledger and «دفعاتي اليوم» icons and ranges.
- `d41b079f` C8.7 — `useSpaceOwners` and `ledgerPeople`, «{name} · صاحب المساحة»; 166 resolved.
- Also read: `5c1dabd8` (W3's record of finding 212), which my role file does not list.
- The role file groups my commits as U7 12 / U8 9. By the plan, `eaf2f978` and `3827ee48` are U7's C7.7 and C7.8 (U7 14, U8 7), as the lead's report says.

**2. The plan's decisions built as approved:**
- D7.1–D7.6, D7.9–D7.14, D8.2–D8.7: built as written; small departures judged below.
- D7.7: departs. Customers' visits do not link (R5-F2).
- D7.8: departs. «غير حاضر» is shown unconditionally (R5-F2).
- D8.1: built, but «أقدم بند» is not the oldest item (R5-F3), and the list's state items shift (R5-F4).
- D7.2 / DI19: built, but unreachable below xl when the card is empty (R5-F1).
- OD10's supersessions in my range are recorded where they live: desk DI-14 (`desk.md:146`) and DI-48 (`desk.md:153`).

**3. Money, roles, privacy, keys and locks:**
- *The price sent (171 (a)).* The amount sent is the one shown (`publishedChoices` request `amountAgorot`). On `PUBLISHED_PRICE_CHANGED`:
  - the sheet stays open and calls `prices.refresh()` (plus `settle` on the 409);
  - the failure area says «لم يُسجَّل شيء. تغيّر هذا السعر…»;
  - nothing is retried by itself;
  - the next press uses the same `subscribeKey`, which is safe: the contract writes nothing on a refusal, so nothing is stored under the key;
  - the new map reaches `prepare` through `useSheetForm`'s ref, so the resubmit carries the new amount;
  - the payment refills with the new due only while untouched;
  - the recorded amount is the server's answer (toast from `answer.data`).
  OK.
- *Written-off visits.* Owner only: the toggle and the query are gated on `abilities.writeOff`, the route is 🏢, and a test proves reception never reads it. The undo is `DELETE` with no key, mutation retry 0, its refusal worded through `toastUndoFailed`, and `settle` re-reads both views. The reason gets the focus first. OK, apart from R5-F1.
- *A customer's visit (160).* `customerId` is sent. At check-out, `customer` comes from the quote's visit, so no phone is asked and the debt lands on the customer. OK, apart from R5-F2's presence.
- *Corrections (163).* PATCH 🧾 for name, dates and limits; PUT 🏢 for the price, rendered for the owner only. Each sent once with no key, as the contract says. Agorot via `agorotOf`; a blank limit clears it to `null`. OK.
- *Keys.* Each subscriber check-in, visit, pay, usage payment and subscribe has one key per intent, renewed after success or on reopening. OK.
- *WhatsApp.* `wa.me/{digits of the stored E.164}?text=`. The text is the template filled with the first name, the amount and the space; no other personal data. OK (R5-F6 is about language only).
- *Statement (162).* Both roles see the names, as the finding asks. OK.
- *Ledger (166).* The owners come from the managed space read, deduplicated, owner-only page. OK.
- *Roles.* Every write in my range is the server's to refuse. The UI hides price typing, write-off, corrections' price, archive, the log's other days and the written-off view from reception, and the server refuses each. No role is offered what the server forbids.
- *Locks.* None in my range (web only).

**4. Planned tests and breaks:** T200–T244 are each present, with a break the lane reports turning it red (`scripts\lane-w3\notes.md`). I read in the code T204–T206, T208 and the correction tests' shape; the others only in the report. Weaker:
- T208 never presses «حفظ» again after the re-read. A regression that keeps sending the old `amountAgorot` (a stale map in `useSheetForm`) would pass it. Add one resubmit asserting the new amount and the same key.
- T209 relies on a `Textarea` mock that drops `autoFocus` (LW3-D1). Acceptable.
- No test covers R5-F1–F4.

**5. Each screen against its prototype and §4.1:**
- 13 Front desk: G13.1–G13.19 and G13.24 are built in the code. Gaps: R5-F1 (the written-off view below xl) and R5-F2 (a customer's visit: presence and link, G13.5).
- 14 Customers: G14.1–G14.4 and GX.1 built; R5-F4.
- 15 Customer details: G15.1–G15.7, 162 and 163 built; R5-F3.
- 16 Subscription sheet: G16.1–G16.5 and 171 built.
- 17 Payments: G17.1, GX.1 and 166 built.
- Both languages: every new string is in both catalogues (`desk.ts`, `occupancy.ts`, `payments.ts`).
- Loading, empty, error and offline states: present in the log, the written-off view, the lists and the file.
- 390 / 768 / 1440 and dark: **not seen**. The lead's real run toured these pages read-only, and the plan's desk write cases (R19–R24) were not performed (`4_REPORT_LEAD.md` › *The real run*).

**6. Findings my range closes:**
- 160, 162, 163, 166, 171, 172: built as each *Resolves when* says.
- 164: its read and its screen are built, but the undo is unreachable on a phone or tablet when nothing is uncollected (R5-F1, finding 212). Resolved only once R5-F1 is fixed.
- 212: opened by this lane and left *Open*. That departs from §3.2 (the *Open* group should hold exactly the deployment's six) and from "nothing carries".

**7. Documents:**
- `desk.md`, `occupancy.md`, `visits.md` (*Authority* and web history), `subscriptions.md`, `payments.md` and `spaces.md` match the code, with `#132` in the history lines.
- `desk.md:77` truthfully says each card shows «غير حاضر», but that describes R5-F2's defect; it changes with the fix.
- `desk.md:86` defines «أقدم بند» as "the unpaid visits … then the subscriptions", the R5-F3 rule; it changes with the fix.
- Finding files 160/162/163/164/166/171/172 read `Resolved` with a `**Resolution (#132):**` line. 164's should wait for R5-F1.

## Decisions taken without the owner in my range, judged
- **LW3-D1** (the test mock drops `autoFocus`): acceptable. Only the dialog's own handler can pass.
- **LW3-D2** (the tabs above both panels; view, day and page in the address; reception's visits with no range): sound.
- **LW3-D3** (offline drawn in each list): sound.
- **LW3-D4** (money block side by side from md everywhere; a capped line leaves out "= amount"): sound. h × rate does not equal the capped charge, and the web never prices.
- **LW3-D5** (two phone matches say nothing): sound.
- **LW3-D6** (one `PhoneInput`): sound.
- **LW3-D7** (the usage dialog lives in DeskPage, its own key, focus to the present heading): sound.
- **LW3-D8** (the end note counts days, else hours; the shift's rate, else the plain one; prefilled only while untouched): acceptable.
- **LW3-D9** (the written-off view's toggle hidden with the empty card; recorded as 212 instead of fixed): **wrong**. It leaves a gap on screen 13 in the last build PR (R5-F1).
- **LW3-D10** (only subscribers' names link): **wrong as a silent limit**. Building 160 made customers' visits ordinary, and the fix was a small answer change that should have been raised (R5-F2).
- **LW3-D11** («غير حاضر» on every card): **wrong**. It is false for a customer here on a visit (R5-F2).
- **LW3-D12** (`StateActions` and `useStateActions`; the list's «⋯» reads the file on open; «حضور» only on ACTIVE/ENDING_SOON; the oldest item = `openItems[0]`):
  - the component split: sound;
  - the read on open: acceptable, but its unplaced insertion is R5-F4;
  - `openItems[0]` as oldest: wrong (R5-F3).
- **LW3-D13** (the space's name Arabic first; the first-name rule local): acceptable (R5-F6 is a nit).
- **LW3-D14** («سجّلها {name}»; voids by the ledger's line): sound.
- **LW3-D15** (one form; only fields changed against the last answer; PATCH then PUT; Radix's own first focus kept): sound.
- **LW3-D16–D18**: sound.
- **LEAD-D9** (a fresh W3 agent took over from the report): acceptable. Its decisions are judged above.

## Outside my range
- `packages/shared/src/occupancy/responses.ts:17` / U2's `9f801981` (D2.13): the `VISIT` `PresentPerson` gained `audience` but not the `customerId` that 160 made necessary. That is the root of R5-F2; its fix touches that commit.
- The lead's index (`a12c0790`) lists 204 and 212 as *Open*, against §3.2's "exactly 23, 33, 46, 64, 65, 152". 204 is lane L's.

## Not checked, and why
- The rendering at 390 / 768 / 1440, dark and both languages, and axe in a browser: no servers or runs are allowed. I read only the code and the lead's report, which shows no desk write case performed.
- The tests' red-then-green: only in `scripts\lane-w3\notes.md`. I re-ran nothing.
- The prototypes: compared in the code for the search card (`desk-core.jsx`) and the file header (`Customer file.html`) only, not page by page for every line of screens 13–17.
- The API side of 160, 162, 164 and 171 (`347e32de`, `47ccd91d`, `c675195f`, `1879e0b1`): another reviewer's range. I read only the contract lines my web code relies on.
