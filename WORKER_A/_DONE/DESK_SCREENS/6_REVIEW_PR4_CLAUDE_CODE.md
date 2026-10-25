# Review — DESK_SCREENS PR 4 (#124) — Claude Code
Head: bc8fe86a9859b27ece1f86c3947c0046fffabb4a · checks: green (all 11 pass, incl. test:component, test:api) · head moved during the review: no (still `bc8fe86a`, CLEAN)
Verdict: mergeable after a fix round

Read only, from `C:\dev\masaha\app-design`, every read pinned to `bc8fe86a` (or `origin/main` for the API). 7 commits, 70 files;
no `apps/api`, no `packages/shared`, no `errors.ts` in the diff.

## Findings (verified defects only, most severe first)

### F1 — should-fix · A lost subscribe answer is told as "not saved", which invites a second subscription
- Where: `apps/web/src/features/desk/hooks/sheet/useSubscriptionSheet.ts:285`, `:398`, `:423` at bc8fe86a
- Seen in the code: `halfName` is set whenever `created !== null`, whatever the failure's kind; `half.title` («أُضيف {name} إلى
  الزبائن؛ لم يُحفظ الاشتراك.») shows for a network/timeout failure as for a refusal, and `close()` toasts `half.closed` («{name} في
  الزبائن بدون اشتراك.») unconditionally. DI-37 (plan §8) is written for a subscribe **refused** ("with the reason"); after a lost
  answer the server may have recorded the subscription and its payment. Also seen in the executor's real run (report: the half title
  and «لم يصل الرد…» shown together) — only in the report.
- Scenario: reception, new customer, «حفظ واستلام ₪120»; the customer is created; the subscribe lands on the server but its answer
  is lost → the sheet says the subscription was not saved; the receptionist closes → toast "X is in the customers, with no
  subscription" → they open «اشتراك جديد» on X (a new opening, a new key) and save → a **second subscription and a second payment**.
- Fix: set the half state (title and closing toast) only for a refusal (`failure.kind === 'refused'` / a 4xx); for a lost answer keep
  the «لم يصل الرد…» line and «إعادة المحاولة» with the same key, and on close say nothing definite (or say the outcome is unknown, check
  the file). A test: create 201, subscribe network failure → no «لم يُحفظ الاشتراك», no "with no subscription" toast on close.
  · Belongs: a fix round on this PR.

### F2 — should-fix · The sheet opened from a «⋯» menu item does not return the focus (F1 of #122, again)
- Where: `apps/web/src/features/desk/components/sheet/SubscriptionSheet.tsx:55` (no `onCloseAutoFocus`), `:29-30` (the comment
  "Closed, the focus returns to what opened it"); opened from `components/menu/CustomerMenu.tsx:52` and the desk's phone «⋯»
  (`pages/dashboard/space/desk/DeskPage.tsx`, «زبون جديد» item) at bc8fe86a
- Seen in the code: the sheet is mounted by the page and opened from a `DropdownMenuItem`; it passes no return target. This is
  exactly the mechanism commit `0b022eea`'s own body describes ("open from a menu item that has left the page by the time they close,
  so the focus fell to the body"), proven red by the executor for the edit and archive dialogs of the same menu. **Plausible** (not
  run here): same component, same opening path, no fix applied.
- Scenario: keyboard user, card's «⋯» → «اشتراك جديد» → Escape or save → focus on `body`, not on «⋯»; same from the desk's «⋯» on a
  phone. The sheet's own comment claims the opposite.
- Fix: the page's `useSheetOpener.open` takes (or records `document.activeElement` / a ref to) the trigger, and `SubscriptionSheet`
  passes `onCloseAutoFocus` to it when connected (as `CustomerFile`'s `PayDialog` does with `isConnected`); `CustomerActions` hands
  its «⋯» ref. A test like `CustomerActions.component.test.tsx`'s. · Belongs: a fix round on this PR.

### F3 — should-fix · Renewing a published-price subscription preselects the first published price, not the renewed one
- Where: `apps/web/src/features/desk/hooks/sheet/useSubscriptionSheet.ts:146-158` at bc8fe86a
- Seen in the code: `renewedValue` is `pkg-{id}` or `custom`, else `null`; a subscription made from a published price has neither
  (`packageId` null, `priceTyped` null), so `current` is null and `firstChoice = options[0]` — the first published line (on the demo
  data «أسبوعي» ₪120). The report records it as a departure ("offers no current line: the choices start at the first"), but the
  executor's own decision 4 made the subscription's `name` the line's title precisely so it can be told apart — the match is
  available (name, or audience + shift + the 7/30-day span).
- Scenario: «محمد» holds «شهري» (₪350, from the published month); reception presses «تجديد» → the sheet shows the full list with
  «أسبوعي» checked and «تجديد واستلام ₪120» → one press renews a month as a week at ₪120.
- Fix: map a published-origin subscription back to its line (`publishedChoices`' title = `renews.name`, or period by span +
  audience + shiftId) and offer it as the renewal's `current`; none matching → no preselection (choice empty, submit blocked until
  chosen) rather than the first. A test in 76's file. · Belongs: a fix round on this PR.

### F4 — should-fix · Test 72's "the payment is the recorded amount" cannot fail
- Where: `apps/web/src/features/desk/services/sheetRequest.unit.test.ts` (first case) and
  `hooks/sheet/useSubscriptionSheet.ts:273` at bc8fe86a
- Seen in the code: the mapping that makes the payment the recorded amount is the hook's line 273
  (`typeof money.amount === 'number' ? money.recorded : money.amount`). The unit test only echoes `payment.amountAgorot` through
  `sheetInput`; every hook test sends exactly the due (75: 17000; 74: 15000; published: 20000), where typed = recorded. Replacing
  line 273 by `money.amount` leaves every test green. The check-out has its equivalent (`useCheckOutDialog` "sends … the recorded
  amount, never the typed amount above the due"); the sheet does not.
- Scenario: a regression sending the typed amount: a fixed package of ₪150, ₪200 typed (₪50 change) → 409 `PAYMENT_EXCEEDS_DUE`
  instead of a ₪150 payment; nothing catches it.
- Fix: one hook test: ₪200 typed on ₪150 → body `payment.amountAgorot: 15000`; and ₪100 typed → 10000 (a known customer, so no phone
  rule). · Belongs: a fix round on this PR (with F1–F3).

### F5 — nit · A focus refetch empties the published choices while the sheet is open
- Where: `apps/web/src/features/spaces/hooks/editor/useSpacePrices.ts:33-34` at bc8fe86a
- Seen in the code: `state`/`prices` follow `isFetching`, not only the first read since mount; the app's `QueryClient` sets
  `refetchOnWindowFocus: true` and `staleTime: 30_000` (`shared/api/query/queryClient.ts`). TanStack v5 refetches a stale active query
  on focus, so every return to the window after 30 s turns `PackageOptions` into skeletons (the radio group unmounted) and blocks the
  submit until it answers. Plausible as described (not run); no money effect (the choice key survives, `ready` gates the reset).
- Scenario: receptionist alt-tabs to check a phone number, comes back → the choices flash to skeletons, a focused radio loses focus.
- Fix: hide only until a read since mount answered (`isFetchedAfterMount`), or `refetchOnWindowFocus: false` on this query; the
  re-read after a refusal can keep its own loading. · Belongs: the next PR's first commit, or with the fix round.

### F6 — nit · `desk.md`'s web code map does not name the sheet's files
- Where: `docs/features/desk.md` *Code map › Web* at bc8fe86a
- Seen in the code: the entry list gains `SubscriptionSheet`, `SheetEntry`, `SheetChoices`, but the per-folder enumeration (hooks,
  services, components) names nothing of `hooks/sheet/`, `services/{endOf,packageLine,publishedChoices,sheetRequest}`,
  `components/sheet/`; the page's `SubscriptionSheetSlot`/`useSheetOpener` are not named either. Incomplete rather than false.
- Fix: add "the subscription sheet, its form and its two writes" to hooks, "a subscription's end, a package's line, the published
  choices, the sheet's request" to services, "the sheet" to components. · Belongs: the fix round.

## Tests 69–77 and the carried tests (one line each)
- 69 `Sheet.component.test.tsx` — present; asserts the classes on both sides and `min-w-0`; fails with `w-3/4` kept (seen red in the
  report). Width measured only in the real run (report).
- 70 `useOfferedPackages.component.test.tsx` — present (2 cases); break "retired kept" red per report.
- 71 `endOf.unit.test.ts` + `packageLine.unit.test.ts` — present; 30 from the 1st → the 30th, 1-day, month/year rollover; fails off by one.
- 72 `sheetRequest.unit.test.ts` — present: package id only, custom with reason and no package, reason refused, customer apart,
  published by key + name with no `priceId`/`packageId`, `renewalOfId`. **Weaker:** the recorded-amount clause cannot fail (F4).
- 73 `useSubscriptionSheet` "offers «Custom» only to whoever…" + "requires the reason…" — present; written after the code, its break
  ("always offered") red per report.
- 74 same — present: two posts, two different keys, refused subscribe → retry sends the subscribe alone with the same key and body;
  plus the closing toast case. Not covered: the half state after a lost answer (F1).
- 75 same — present and strong: due ₪20 + ₪150 = ₪170 sent as 17000; the toast's price ₪160 from the answer (finding 171), the parts
  by item, «₪10 stays owed», `CUSTOMER_HAS_DEBT` line. Would fail with the toast from the form.
- 76 same — present: start from `renewal.startsOn` (2026-11-05), `renewalOfId: 4`, 409 `SUBSCRIPTION_ALREADY_RENEWED` worded and the
  sheet turning into "New subscription". Not covered: renewal of a published-price subscription (F3).
- 77 `SubscriptionSheet.component.test.tsx` — present: title by mode, the name focused, DI-45 (no `svg` in the line), axe at 390 and
  1440. The plan's break (autofocus off) was dead (Radix focuses the first field); the replacement break is a fair one.
- Spec D / 171 extras — published subscribe (body, no `priceId`), the two refusals (line, `refresh` called once, fields kept),
  «تغيير الباقة» and «إعادة المحاولة» send nothing (the real run's slip, red first per report), `useSpacePrices` refetch on mount.
- Carried F1 `CustomerActions.component.test.tsx` — present, two cases (edit saved, owing archive's «رجوع»), focus on «⋯»; red before.
- Carried F2 `useEditDialog` "sends nothing for the same number typed in its local form" — present; would fail on the raw compare.
- Carried F3 — `refresh.unit.test.ts` retitled as the carried note says.
- Carried F4 `useArchiveFlow` "says a settled customer present is checked out first…" — present; its break (lines dropped) red per report.
- Not planned, not tested: DI-53's known-customer no-phone line (no test names it).

## Finding 171 as built
Built as the supervisor's provisional choice said (seen in the code): `SubscriptionSheetSlot` is mounted only while open (keyed by
the opening), `useSpacePrices` uses `refetchOnMount: 'always'` and shows nothing until that read answers; the request is
`published: { period, audience, shiftId?, name }` with no amount (`sheetRequest.ts`); the toast's price is
`subscription.priceAgorot` from the answer (`deskToasts.tsx` `toastSubscribed`); `errors.published` or `PAYMENT_EXCEEDS_DUE` →
`choices.prices.refresh()`, fields kept, `published.gone` line for the 422. Finding 171's file is untouched in the diff. Holes left:
- **A price raised after the read is still charged without a stop**: the payment sent is the old total, the server records it and
  leaves the difference as debt; the toast says the higher price and «يبقى … دينًا» — said, but only in a toast. For a **new**
  customer this also bypasses K2: `needsPhone` was computed on the old price (nothing owed), so a debt is left on a customer with no
  phone. This is the API-side option 171 keeps open; worth one line in the PR so the owner sees it.
- The **packages** are not re-read on opening (`useOfferedPackages` uses the list's default query, `staleTime` 30 s, shown while
  refetching): a package price edited meanwhile has the same silent-debt path. Outside 171's wording; a finding candidate if the
  owner wants parity.
- The focus-refetch flicker (F5).

## Departures and decisions taken without the owner, judged
1. Finding 171 (supervisor's) — built as said; holes above. Acceptable as provisional.
2. The slip's two renewals left in `masaha_dev` (subscriptions 5 and 6 of «محمد عوض») — only in the report. Right not to undo with
   more writes; the defect (buttons without `type="button"`) is fixed with tests (seen: `PackageOptions.tsx:46`, `:70`). The owner
   decides the data.
3. «محمد عوض»'s partial renewal not performed — acceptable; 75/76 cover the parts and the start, but nothing live shows a partial
   renewal's toast.
4. Published name = the line's title («شهري · للطلاب», + shift name) — sound, and it makes F3's fix possible; ≤ 60 enforced by slice.
5. «زبون جديد» in the page top bars; «تجديد» only on the file's latest card — acceptable; reception gets «تجديد» too (fine: no typed price).
6. `Input type="date"` instead of `DatePicker` — acceptable, smaller; flag for the owner's design taste only.
7. Breaks made differently (77's autofocus, the width) — both justified; the width break in the real run is the meaningful one.
8. Tests written after code, proven by breaks — accepted by the run's rules; F4 shows one clause no break covered.
9. The retry button's fix folded into commit 4 though the button is commit 3's — harmless; commit 3 alone has the submit-on-retry bug,
   which only matters for bisecting.
- Other departures (from §10): one `useServerForm` with `sheetSchema(newCustomer)` (good: errors at server paths);
  `SheetEntry`'s known customer `Customer & { debtAgorot }` and the file read again for items (fine); `mayTypePrice` read by the sheet
  from `visit-terms` rather than passed (fine: one owner, the server's answer); extra page files `SubscriptionSheetSlot`/`useSheetOpener`
  (fine, S1); `termsLine` taking a `Pick` (fine); extra copy keys (both catalogues, parity under test 40); `spaces.md`, `overview.md`,
  `packages.md` updated beyond the list (true to the code). Renewal of a published-price subscription with no current line → F3.
- Files 70 vs ≈ 48 planned: the growth reason given is true to the diff.

## Checked and fine
- **Keys (S4):** two `useIntentKey()` per mounted sheet, the sheet remounted per opening (`key={sheet.opening}` on all three pages);
  create with key 1, subscribe with key 2; a failed create leaves `created` null so a retry re-sends the create with the same key (the
  API answers the same customer by `findByKey`); a refused subscribe keeps `created` and re-sends only the subscribe; no `renew()` is
  ever called inside an opening. The API writes nothing on a refusal, so the same key after a 4xx is safe (`desk.service.ts`).
- **Request:** exactly one of `packageId` / `published` / `custom` from `choice`; the package carries its id only (DI-50, no price
  field); `published` from the map, no `priceId`; custom with its reason, offered only with `mayTypePrice` (`isCustom` also requires
  `customChoice`); the schema is the contract's `subscribeSchema`; payment omitted at 0.
- **Due:** `priorTotal + newPrice` (0 for usage billing, `open` → credit); nothing computed that the answer gives (toast from
  `NewSubscription`, labels matched by item key, the new one by id).
- **Dates:** `endOf = addDays(start, n − 1)`; week 7 / month 30; start defaults to Gaza's date (`gazaClockOf`); the renewal start
  from `renewal.startsOn`, the submit blocked until it answers; `null` → `SUBSCRIPTION_ALREADY_RENEWED`'s line, no `renewalOfId`.
- **Roles / K2 / DI-53:** «مخصّص» hidden without `mayTypePrice`; phone asked only of a new customer, required while `money.left > 0`,
  checked before the create; a known customer without a phone gets the non-blocking line.
- **Carried F1–F4:** done as the carried file says; F2 compares `normalisePhone(typed) ?? typed`.
- **S12:** `start`/`end` `w-full … md:w-3/4 md:max-w-sm`, `SheetBody` `min-w-0`; no showcase file changed; finding 101 Resolved truthfully
  (status, resolution, index moved); `foundation.md` §12 row true.
- **Documents:** `desk.md` decisions true to the code (sheet, decision 3, two keys/DI-37 for a refusal, DI-50/52/53, renewal, spec D,
  171 as the supervisor's), `customers.md`, `subscriptions.md`, `packages.md`, `spaces.md`, `overview.md` true; finding 125 Resolved with
  #124; finding 171 untouched; no finding 165 (spec D taken).
- **Commits:** 7, subjects ≤ 50, each with a body, Conventional; no `fixup!`, no tool attribution.
- Arabic plural of `validity` (one/two/few/many/other) correct.

## Not checked, and why
- Nothing run (review rules): the focus behaviour of F2 and the refetch flicker of F5 are reasoned from the code and the executor's
  own red F1 test, not observed.
- The real-run screenshots and network log (`shots\pr4\`) — only in the report; not opened.
- `useServerForm`'s double-submit handling beyond `isSubmitting`/the button's `loading` — existing code; a double press re-sends with
  the same keys, which the API answers idempotently.
- The API's own handling of `published` (#118, merged) — taken from the contract and the report, not re-reviewed.
