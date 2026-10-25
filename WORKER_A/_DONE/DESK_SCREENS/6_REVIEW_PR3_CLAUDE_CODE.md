# Review — DESK_SCREENS PR 3 (#122) — Claude Code (light)
Head: 358765e3937e92562e10eeccbbf6b6ccf5ac0d74 · checks: green (all 11 pass; merge state CLEAN) · head moved during the review: no
Verdict: mergeable (no blocker; F1 is a small should-fix, F2–F4 are nits — per the review-verdict rule they ride as the next PR's first commit, named in its description)

Read from commit objects at `358765e3` only (`git show` / `git diff origin/main...358765e3`); no checkout, no runs. "Seen" = in the code or test at that sha; "report" = only in `4_REPORT_PR3.md`.

## Findings (verified defects only, most severe first)

### F1 — should-fix (plausible) · the edit and archive dialogs have a focus-return option nobody passes
- Where: `apps/web/src/features/desk/components/edit/EditCustomerDialog.tsx:30,47` and `components/archive/ArchiveDialog.tsx:25,39` at 358765e3; the only callers are `components/menu/CustomerActions.tsx:58-66`.
- Seen in the code: both dialogs document and implement `returnFocus` ("Closed, the focus returns to what opened it, or where `returnFocus` says"). `git grep returnFocus` finds no caller of either dialog that passes it, production or test (`CustomerActions` renders `<EditCustomerDialog spaceId customer onClose>` and `<ArchiveDialog dialog>` only). Both dialogs are opened from a `DropdownMenuItem`'s `onSelect` (`CustomerMenu.tsx:41,43`), and that item has left the DOM by the time the dialog closes.
- Scenario: a keyboard or screen-reader user opens «⋯» → «تعديل البيانات» (or «أرشفة…» on a customer who owes), then saves or goes back → the focus is not given back to «⋯». Radix restores it to the element focused when the dialog mounted (the unmounted menu item), so it most likely falls to `<body>`. Plausible, not run: this is Radix's behaviour, and the report's real run does not check focus after these dialogs. The dead option is verified; the focus loss is not.
- Fix: have `CustomerActions` keep a ref to the «⋯» trigger (or to the row's control) and pass `returnFocus` to both dialogs, with an assertion in test 62 or 63 that the focus returns. Or drop the option from both dialogs and their doc lines, since nothing uses it (the rule against options nothing passes).

### F2 — nit · the edit compares the typed phone with the stored one before normalising
- Where: `apps/web/src/features/desk/hooks/edit/useEditDialog.ts:46-52` at 358765e3.
- Seen in the code: `prepare` sends `phone` when `typed !== customer.phone`. `customer.phone` is stored E.164 (`+970599000201`), and the schema normalises only afterwards. Test 62's first case shows it: typing `0599000304` is sent as `+970599000304`.
- Scenario: the user opens the dialog, retypes the same number in local form (`0599000201`) and saves → `{ phone: '+970599000201' }` is sent although nothing changed. «لم يتغيّر شيء» is not shown, and a write goes out. Finding 123's rule is that an unchanged field is not sent. The same happens with a number typed with inner spaces. The harm is small, because the server accepts it as the same number.
- Fix: compare the schema's normalised phone with `customer.phone`, not the raw text.

### F3 — nit · test 67's second case has a title that says the opposite of what it asserts
- Where: `apps/web/src/shared/session/services/refresh.unit.test.ts` (the second added `it`, lines ≈104–113 of the diff) at 358765e3.
- Seen in the code: the title is "says no idleness for a session refused otherwise, **or found ended by the restore**", but the last assertions are `restoreSession()` refused `SESSION_IDLE` → `getSessionEnd()` is `'idle'`.
- Scenario: someone reads the title as the rule "a restore never says idle" and "fixes" the code to match it; the test would then fail on its body, but the title would mislead first.
- Fix: retitle — "says no idleness for a session refused otherwise; says it for a restore the server ended for idleness".

### F4 — nit · test 63 proves "present" on one of the two archive paths; the other is untested
- Where: `apps/web/src/features/desk/hooks/archive/useArchiveFlow.component.test.tsx:126-138`; the untested code is `hooks/archive/useArchiveFlow.ts:58-69` (`archiveSettled`) at 358765e3.
- Seen in the code: "says a customer present is checked out first" runs only through the debt dialog (`debtAgorot: 5000`). A customer with no debt who is present (the commoner case) archives at once, and its refusal is worded by `toastFailed(words.failed, …, { lines })` — a different code path, with a toast and no dialog. It has no test. Neither has the at-once archive's lost-answer toast with «Try again» (`retry: archiveSettled`).
- Scenario: a regression in `lines` for the at-once path (the `MEMBER_ALREADY_CHECKED_IN` line dropped) leaves test 63 green. Then the owner gets the generic "We couldn't archive them" for a present customer, with no hint to check them out first.
- Fix: one more case in this file — `debtAgorot: 0`, answer 409 `MEMBER_ALREADY_CHECKED_IN`, assert the toast says "Sara Khalid is here now; check them out before archiving."

## Axes A1–A6

**A1 — Money. ✔ seen.**
- Every amount is the server's. `useCustomerFile.ts:158-166` uses `dueAgorot`, `paidAgorot` and `balanceAgorot` as answered. The only arithmetic is `Math.max(0, balanceAgorot)` for «المتبقي» (line 165), and the header's debt and credit come from `balanceView(file)`.
- What the floor hides: a usage-based subscription in credit shows left ₪0 and no credit line on its card. The credit appears only in the header badge, and only when the customer has no debt, because `balanceView` says debt first (`balanceView.ts:20-24`, DI-40). That is the approved design (the server never offsets one with the other), not a defect.
- Voided payments: `useStatement.ts:67-79` marks each with «ملغاة» and the reason; `Statement.tsx:105` strikes the amount. Nothing in the web adds payments up, so a voided one cannot be counted as paid; the card's «المدفوع» is the server's `paidAgorot`.
- `payStatus.ts:18-20` follows the plan, balance ≤ 0 → paid:
  - nothing paid and owing → unpaid ✔.
  - overpaid or in credit → paid ✔ (unit case with −500).
  - zero due and nothing paid (a usage-based subscription with no usage yet, or a free one) → «مدفوع». The plan says so, and the unit test does not pin that edge. No change needed.
- Invalidation: every desk write `settle`s with `['space', spaceId]` (`useDeskWrite.ts:16`), the prefix of the file, the list, the statement, the search and the unpaid lists (`queryKeys.ts`). Edit, archive, restore, end and payment all call it (`git grep "settle("`). An open statement is refetched; a closed one is marked stale and read again on opening. I found no path to a stale balance beyond the 30 s `staleTime` between writes by another desk.

**A2 — The edit. ✔ seen.**
- Only the differing fields are sent (`useEditDialog.ts:45-53`). A cleared phone is `null`, and only when the customer had one. An empty body sends nothing and says «لم يتغيّر شيء» (lines 55-58).
- No key: the repository call is a plain `api.patch` (`deskRepository.ts:155`). `installRetry` re-sends only a GET or a request with an `Idempotency-Key` (`retry.ts:41-43`), so a lost answer is the user's «إعادة المحاولة» (test 62 asserts one PATCH after 10 s, then a second by the user).
- "As loaded" if the file refetches while the dialog is open: it means as loaded when the dialog opened. `useServerForm.ts:84` builds the resolver once (`useState(() => schemaResolver(schema, prepare))`), so `prepare` keeps the first render's `customer`, and `defaultValues` are frozen the same way. A field the other desk changed meanwhile is therefore not sent back unless the user retypes it. This depends on that one-time capture, and no test pins it (nit, not a defect: a refetch-while-open case in test 62 would).
- See F2 for the one way an unchanged phone is still sent.

**A3 — Archive, restore and the roles. ✔ seen** (F1 and F4 are the only remarks).
- Owner only: `useArchiveFlow.ts:85-110` returns `archive` and `restore` as `null` unless `owner`. `owner` is read from the session's link at the space (`CustomersPage.tsx:17`, `CustomerPage.tsx:53`). The list offers «مؤرشف» for the owner only (`useCustomersList.ts:131`), and reception's `?status=ARCHIVED` is dropped before the query (`customersQueryOf.ts:50`; `useCustomersFilters.component.test.tsx:71-77`).
- Reception sees «ملف الزبون» and «تعديل البيانات» (both are the staff's in the contract). I found no control shown to reception that the server refuses.
- Settled: `archiveSettled` archives at once with a «تراجع» toast action → `runRestore`. `mutateAsync` still resolves after the row unmounts, and `settle` is a mutation option, so the undo works from the list, where the row leaves. Sonner closes the toast on the action, and test 63 asserts the URLs are exactly `[archive, restore]`, so exactly one restore. The run is guarded by `isPending`.
- Owing: the `AlertDialog` names the debt from the row's or file's `debtAgorot`. Present: the dialog path shows the 409 line and stays open (tested); the at-once path is F4.
- Not a defect, noted: a row's debt can be up to a stale-time old. A customer who has just been charged elsewhere would then archive at once, and the server allows archiving a customer who owes.

**A4 — The end. ✔ seen.**
- Offered only while `ended === null && status !== 'EXPIRED'` (`useEndDialog.ts:62-63`).
- The dialog's end is `startsOn > today ? startsOn : endsOn < today ? endsOn : today` (lines 39-44), the contract's rule: today, its start if not started, never later than its end. `textWas` appears only when the end changes. Tests cover the running case and the not-started case.
- One `POST …/end`, no key (test 66 asserts the header is absent and one POST after 10 s without an answer). `run` is guarded by `isPending`. `settle` reads the file again (test 66 counts the second GET).
- `today` is computed on each render, so a card left open past Gaza midnight is wrong only until its next render. Negligible.

**A5 — The idle line. ✔ seen.**
- `endedBy: 'idle'` is set in one place, `refresh.ts:43`: the refresh is refused with `endsSession(failure)` (401, or 403 suspended) and `failure.code === 'SESSION_IDLE'`. The restore and the transport's 401 both go through `renew()`, so both are covered. Any other refusal calls `endSession({ endedBy: null })`.
- Cleared by `establishSession` (`store.ts`, first line), so by every sign-in, restore or refresh that succeeds. Every `endSession()` without an argument (sign-out, a restore with no hint) sets it to `null`. A normal sign-out cannot show the line.
- The sign-in page shows it only while `useSessionEnd() === 'idle'` (`SignInPage.tsx`).
- A non-reception user: the server idles reception only, so the only way to see the line is to sign in from a browser whose previous session was reception's idle one. That is the plan's "until the next sign-in".
- A race I did not count as a defect: a deliberate sign-out answered while an idle refresh is in flight could end `idle`. It needs an idle session being signed out at the same moment.

**A6 — The list's address and the tests. ✔ seen** (F3, F4 only).
- `customersQueryOf.ts:43-55` reads `q`, `status`, `kind`, `payment` and `page` through `customersQuerySchema.shape`, the server's own rules. A refused value falls back (unit case with `q` of 61 characters, `GONE`, `PLAN`, `MAYBE`, `page=0`, `page=abc`). `ARCHIVED` is kept for the owner only. `packageId` is never read. Each choice calls `apply`, which writes with `replace: true` and `page: 1` (`useCustomersFilters.ts:41-43`, test 55). The search writes after the pause, also to page 1. The pages are links with the filters kept.
- Routes warm-up: the report measured the desk page's first import at 10.8 s in the jsdom lane. That is vite-node transforming the module graph with no tree-shaking, and `DeskPage` imports the `@features/desk` barrel, which now also exports `CustomersList` and `CustomerFile`. It is the file's own idiom (the other describes warm up lazy pages the same way). It does not show a user-met slowness. What it does not prove either way: the production desk chunk's size. `check:build` only checks the site's first download, not the desk chunk. `? not checked` — one `dist` look at the desk chunk for TanStack Table would settle it.

## Tests 54–68 (one line each)
- 54 present · `customersQueryOf.unit.test.ts`: the break (`ARCHIVED` kept for reception) fails the second case ✔.
- 55 present · `useCustomersFilters.component.test.tsx`: the page kept after a filter fails the first case; the paused search is covered ✔.
- 56 present · `useCustomersList.component.test.tsx`: loading, failure with reference and retry, four empty states, rows kept while the next page loads; one empty state fails the `it.each` ✔. The "failed again over the rows" state is not in the plan's list and is untested.
- 57 present · `CustomersList.component.test.tsx`: five columns at 1440, cards and the filter sheet with its count at 390, chips named, axe at both; the sheet at 1440 fails it ✔.
- 58 present · `payStatus.unit.test.ts`, `termsLine.unit.test.ts`: partial when nothing paid fails the unpaid case ✔. The zero-due edge is not pinned.
- 59 present · `useCustomerFile.component.test.tsx`: due/paid/left are asserted with a balance (3000) different from due − paid (5000), so a computed left fails ✔. The `Math.max(0, …)` floor has no case (nit).
- 60 present · `CustomerFile.component.test.tsx`: one h1, h2 sections, h3 cards, axe ✔. The breadcrumb's name is proven in 61, not here.
- 61 present · `routes.component.test.tsx`: both roles, title from the name, "Customer file" while loading, the trail ✔.
- 62 present, with a gap · `useEditDialog.component.test.tsx`: only the changed field, nothing, `null`, one PATCH after no answer, `PHONE_TAKEN` on the phone; the whole form sent fails four cases ✔. Gaps: F2, and no refetch-while-open case (A2).
- 63 present, weaker · `useArchiveFlow.component.test.tsx`: settled with exactly one restore, the dialog naming the debt, present via the dialog, `PHONE_TAKEN` on restore, reception offered neither ✔; F4 is the missing path.
- 64 present, on a weaker break · `CustomerMenu.component.test.tsx`: named by the customer, «Archive…» `data-variant="destructive"`, Escape returns the focus to the trigger. The accepted break (the trigger's label) is the one that can fail it, as the report shows. The trigger's `aria-label` is also what names the content, so an outcome-changing break exists ✔. The focus after the edit and archive dialogs is not tested (F1).
- 65 present · `useStatement.component.test.tsx`, `Statement.component.test.tsx`: read only when opened, "Here now", auto check-out, voided with «Voided» and its reason; `voided` always `null` fails ✔.
- 66 present · `useEndDialog.component.test.tsx`: its red step is its break (accepted). Would fail if the end were re-sent (a keyed send would be re-sent by the transport and the POST count would pass 1), if the card were not read again (GET count 2), or if the old end were not said. The "offers no end for an ended one" case passes by counting one button and the first render's button stays mounted; it fails if the second offered one, so it works, but fragilely.
- 67 present · `refresh.unit.test.ts`: `endedBy` not set fails both cases ✔; F3 (title).
- 68 present · `authPages.component.test.tsx`: its red step is its break (accepted). Always-shown fails the first case (absent by default); the second proves the line, in a `status` role, above the form ✔.

## The four decisions
1. **`changePasswordPage` miss at 3,472 ms, left to CI** — accepted. The file is outside this PR, it passes alone and in its folder, and the CI `test:component` passed on the head.
2. **Carried item 1's pre-check-in dialog not shown live** — accepted on substance, flagged on procedure. The substitute (blocking the file's own URL over CDP, then retrying) shows the same failure branch live, and the dialog's own failure is proven by its red/break test. But the approval note's standing rule says "a demo account or data lacking a real-run case → stop and report". The executor did not stop and report; the autonomy file (`_SHARED\AUTONOMY_2026-10-25.md`) may have allowed this, and I did not read it. The owner should say whether the substitute stands.
3. **Two layout fixes found by the run, folded into commits 2 and 1** — accepted. Both are small, found by a real run, folded per the owner's rule, with only the touched lanes re-run (`components/customers` + routes, 57 tests green; lint and typecheck).
4. **The idle run started again** — accepted; no file changed during the run, and the final run (network log in the report) shows the refresh's 401 `SESSION_IDLE` ending the session with the line. Outside the four, the report's own slip (the demo password logged, then scrubbed) is recorded there with the owner's rotation suggestion; I did not look at the workspace files for it.

## Not checked, and why
- Nothing was run (lint, typecheck, tests, build, browser): the rules forbid it. CI's green on the head is the only evidence for the lanes.
- Radix's focus restoration after a dialog opened from a menu item (F1): read from the code only.
- Production desk chunk size and tree-shaking of the `@features/desk` barrel (A6): needs a build.
- Copy wording, layout, CSS, documentation style, file naming and the docs diff (finding 123's resolution, 162/163, the capability documents): out of the light review's scope.
- The `DeskSearch` / `PreCheckInDialog` / `VisitDialog` changes for the two carried #119 items: not one of the six axes. I read only their reported tests and results.
- `Statement` and `CustomersFilters` markup beyond what axes A1 and A6 need.
