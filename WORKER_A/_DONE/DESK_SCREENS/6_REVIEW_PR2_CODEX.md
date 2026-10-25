# Review — DESK_SCREENS PR 2 (#119) — CODEX
Head: `8d087c5ede6dd5406148258477beb8b4e4106fd9` · checks: all pass · head moved during the review: no
Verdict: mergeable after small fixes

## Findings (verified defects only)

### F1 — should-fix · Upcoming subscription file errors leave the choice loading forever
- Where: `apps/web/src/features/desk/components/subscriber/PreCheckInDialog.tsx:49`
- Seen in the code: the dialog renders a skeleton whenever `dialog.reason === null`; `useSubscriberCheckIn` makes `reason` null both while the upcoming-subscription file is loading and when the query failed. The dialog does not render a file-query failure or retry action.
- Scenario: the receptionist opens check-in for a not-started subscription and the customer-file request fails → the dialog continues to show a loading skeleton with no explanation or recovery, while the choice remains actionable.
- Fix: distinguish loading from failure; render a localized failure and retry the customer-file query, and keep the start-date reason once it loads.

### F2 — should-fix · Named visit check-in leaves the search populated
- Where: `apps/web/src/pages/dashboard/space/desk/DeskPage.tsx:192`
- Seen in the code: the search's visit action only calls `visit.setOpen(true, name)`. The existing `useVisitDialog` closes and toasts after success but has no completion callback wired to `DeskSearch`'s `after.done`, which is the operation that clears and focuses the field.
- Scenario: staff type a name, choose «Check in a visit for …», and submit successfully → the dialog closes but the term and result groups remain in the search and focus does not return to it. Subscriber check-ins and check-outs do use the callback.
- Fix: pass a success callback from this named-visit entry to the dialog and call the search's clear-and-focus action after the successful check-in.

### F3 — should-fix · Names in another language have direction but no language metadata
- Where: `apps/web/src/features/desk/components/card/CustomerCard.tsx:54` (also `apps/web/src/features/occupancy/components/PresentMatches.tsx:38`)
- Seen in the code: customer and present-person names are placed in `dir="auto"` spans, with no `lang` attribute. The card's Arabic name in the English UI is the concrete cross-language case; the executor's report says the layout was visually fixed, but the code still has no language metadata.
- Scenario: an English-speaking screen reader encounters an Arabic customer name → it receives no language switch for pronunciation.
- Fix: provide the correct `lang` for cross-language names (and keep `dir="auto"`); apply the same treatment to names in the present matches and other name-bearing UI where language differs.

## Checklist 4.1–4.8

### 4.1 Keys and repeats

- ✔ Subscriber check-in uses `useIntentKey`, passes `key` through `Idempotency-Key`, renews only after success; mutation guards prevent another press while pending. Network retry retains the key.
- ✔ Subscriber check-out is an unkeyed `api.post`, not automatically retried by the keyed-write transport; on a lost answer, a toast offers a user-triggered retry. Busy guard prevents double submission.
- ✔ Payment dialog gets one key per mounted opening, and one submit produces one payment request. Changing the item after an error can submit a different body with the same key; the server contract says a key used for another item conflicts, and desk copy says to close and reopen, which creates a fresh opening/key. This is handled, though not tested directly.
- ✔ «Check in as a visit» uses `visitKey`, separate from the subscriber key.

### 4.2 The search

- ✔ One customers query after the 400 ms pause; schema parsing limits `q` to valid 1–60-character values; empty/invalid text disables the query and the groups. Query keys include the term. TanStack `keepPreviousData` can display the previous result during load, but once a newer answer lands it is keyed to the newer term; stale completion cannot overwrite that query's data.
- ✔ Present matches use name substrings and, only for check-ins, phone suffix digits after separator removal; visit digits cannot match. The second group excludes current present customer IDs. Arabic matching uses plain `includes` after lowercase, so it can miss alef variants such as `أ` versus `ا` (documented implementation departure; not listed as a defect absent evidence of a wider promised fold).
- ✔ Visit action is primary only when neither group matches; no-match copy promises no customer file.
- ✔ The accepted departure leaves present customers in the first group only. Staff see the matching present row with «خروج» there. The customer card group is filtered to exclude them, so it does not show a presence badge or checkout action.

### 4.3 Subscriber check-in and check-out

- ✔ `ACTIVE` and `ENDING_SOON` take the direct path; no subscription, `EXPIRED`, and `UPCOMING` open the choice; “anyway” is absent for no subscription.
- ✘ F1: the file is read only when the choice opens for an upcoming subscription, but a failed read is indistinguishable from loading and never gets a visible failure/retry.
- ✔ `MEMBER_ALREADY_CHECKED_IN` has customer-specific copy; server warnings are rendered after success; subscriber search actions clear and focus after success.
- ✔ Checkout duration uses answer timestamps; the “still owes” line appears only for positive `balanceAgorot`; its action targets that answer's subscription. No page-body focus target is forced. Present rows use the first progress line and open-check-in data refetches when occupancy's check-in IDs change.
- ✘ F2: successful named-visit check-in from the search does not clear or refocus it.

### 4.4 Payment

- ✔ `openItems` lists unpaid priced visits oldest first, skips unpriced visits, then owing subscriptions; a zero-balance usage subscription is available when selected from its card/toast.
- ✔ Amount is initialized from the selected item's remaining balance and updates only while untouched. Fixed items are capped by the money block's due; usage items can exceed the due and show the credit note. `PAYMENT_EXCEEDS_DUE` has a localized domain line.
- ✔ The page picker uses `payment=OWES` and stable-sorts current present customer IDs first. Test 53 does prove the order with one present and one non-present debtor; the executor did not demonstrate it live.
- ✔ Successful writes invalidate `['space', spaceId]`, which covers search customers, customer file, uncollected list and occupancy/open check-ins, including the present usage line.

### 4.5 Dates, words, accessibility, RTL

- ✔ `dayText` parses the ISO date at UTC midnight and formats in UTC, preserving the date's own day in any browser zone.
- ✔ Arabic and English catalogues share the new keys, including plural helper count lines; no newly added hard-coded user-facing component text was observed. Phone is `dir="ltr"`.
- ✘ F3: cross-language names get automatic direction but no `lang` metadata.
- ✔ Input type `search` provides `searchbox`; it is labelled and controls results; result sections use `h2`, customer cards use `h3`; count uses polite live region; arrival autofocus uses the 768 px media query. Dialogs have titles and their trigger/focus restoration paths; see F1 for the missing file-load failure.

### 4.6 Tests (each must be able to fail)

- ✔ 42 — `apps/web/src/features/occupancy/services/matchesPerson.unit.test.ts`; substring, suffix and visit-vs-phone behavior. Its digit-regression break covers a live assertion and would fail after the module exists.
- ✔ 43 — `apps/web/src/features/occupancy/hooks/present/usePresentMatches.component.test.tsx`; first group and empty term; empty-term break exercises the assertion.
- ✔ 44 — `apps/web/src/features/desk/hooks/search/useDeskSearch.component.test.tsx`; pause/debounce request, present exclusion and visit primary; request-per-key break hits a regression assertion.
- ✔ 45 — same file; failure/retry and offline are asserted and can fail after implementation.
- ✔ 46 — `apps/web/src/features/desk/components/search/DeskSearch.component.test.tsx`; naming, controls, heading levels, count live region, width autofocus and axe checks; autofocus break is a regression assertion.
- ✔ 47 — `apps/web/src/features/desk/services/{balanceView,statusView}.unit.test.ts`; money tones and statuses.
- ✔ 48 — `apps/web/src/features/desk/hooks/subscriber/useSubscriberCheckIn.component.test.tsx`; direct active, no subscription and expired choice paths, retry key; the “dialog always” break exercises those expectations.
- ✔ 49 — same file; already-here refusal and warning copy, plus success callback/focus. The “search kept” break is a regression assertion. It checks the callback and focus, not the actual search text becoming empty; `useDeskSearch` separately covers clearing.
- ✔ 50 — `apps/web/src/features/desk/hooks/subscriber/useCheckOutSubscriber.component.test.tsx`; one tap, no key, toast and retained focus while row leaves; focus-loss break is a regression assertion. The executor's documented departure tests retained focus, not next-row focus in this feature test.
- ✔ 51 — `apps/web/src/features/desk/services/progressLines.unit.test.ts`; ordered limit/billing/end lines; its end-first break changes the tested order and would fail.
- ✔ 52 — `apps/web/src/features/desk/services/openItems.unit.test.ts`; visit ordering, unpriced omission and subscriptions.
- ✔ 53 — `apps/web/src/features/desk/hooks/pay/usePayDialog.component.test.tsx`; one present debtor before one non-present debtor, item/payment/key, amount follows item while untouched, usage credit. The test assertion distinguishes the two rows, so order regression fails.
- ✔ Routes fake server answers `GET …/check-ins` with `[]`; this only supplies the empty open-check-ins list needed for page rendering and was not seen masking a routes-test behavior.
- CI reports all lanes green. Tests/builds were not run locally under the prompt's explicit prohibition.

### 4.7 Architecture, scope, documents

- ✔ No `shared/` → feature/page dependency observed. Desk imports `PresentMatches`/`matchesPerson` via `occupancy/index.ts`. Diff has no API or `packages/shared` changes; new utility classes use semantic tokens. CI class check passes.
- ✔ Listed web docs describe this PR's built scope; decision/history entries carry date and `#119`; `git grep PRNUM` returned no matches in `docs` or `apps`.
- ✔ Finding 160 text matches the implementation: the visit request has no customer ID, and visit-by-name is explicitly not added to the file. It is present in the findings index.

### 4.8 Departures and decisions taken without the owner

- ✔ Input has no `size` prop: using its layer default is an acceptable design-system boundary.
- ✔ Cards omit presence badge and checkout because present customers are in the first group; a customer who is currently present is still check-outable from search's first group.
- ✔ Cards hold their own view/actions; `useCustomerCard(row)` keeps state per card.
- ✔ `useVisitDialog.setOpen(open, visitorName?)` is a local extension that seeds the named visit.
- ✔ UTC date formatting preserves the ISO date's own day; accepted over the plan's Gaza timezone.
- ✔ Extra fixture and focused unit/component test files are in scope.
- ✔ Checkout focus test retains focus on the busy control until the present row leaves; the executor says next-row focus is occupancy's existing list behavior.
- ✔ Checkout toast payment action arrived with the payment dialog and appears only while a positive balance remains.
- ✔ No shift is sent for the named visit; the shared visit schema makes `shiftId` optional, so no-shift rates apply.
- ✔ Extra `checkInName` copy provides an accessible name.
- ✔ Payment picker reuses the common customer query hook and its OWES filter.
- ✔ Payment dialog remounts per opening, yielding a fresh opening key.
- ✔ Payment dialog's extra component test is useful and in scope.
- ✔ Decision 1 (no live “present debtor” run): accepted; report says no debtor was present and creating one required an extra write outside the approved real-run cases. Test 53 proves ordering in code.
- ✔ Decision 2 (name alignment fix after head lanes): accepted; report says targeted tests, lint, typecheck and classes were rerun, and the local screenshots showed the alignment issue.
- ✔ Decision 3 (listed departures): accepted for the reasons above. The named-visit search completion remains F2; the report's departure set did not account for that path.

## Tests table (4.6)

| # | file | present / missing / weaker |
|---|---|---|
| 42 | `matchesPerson.unit.test.ts` | present; red step is its digit-break assertion |
| 43 | `usePresentMatches.component.test.tsx` | present; red step is its empty-term break |
| 44 | `useDeskSearch.component.test.tsx` | present; red step is request-per-key break |
| 45 | `useDeskSearch.component.test.tsx` | present |
| 46 | `DeskSearch.component.test.tsx` | present; red step is focus-width break |
| 47 | `balanceView.unit.test.ts`, `statusView.unit.test.ts` | present |
| 48 | `useSubscriberCheckIn.component.test.tsx` | present; red step is dialog-always break |
| 49 | `useSubscriberCheckIn.component.test.tsx` | weaker: success callback/focus tested, not actual search value clearing |
| 50 | `useCheckOutSubscriber.component.test.tsx` | weaker: retained focus is tested, not next-row focus here; recorded departure says occupancy owns handoff |
| 51 | `progressLines.unit.test.ts` | present; end-first break changes the tested ordering |
| 52 | `openItems.unit.test.ts` | present |
| 53 | `usePayDialog.component.test.tsx` | present; present-first order is tested with two rows |

## Departures and decisions judged (4.8)

Accepted departures: default `Input` size; no presence badge/checkout on filtered customer cards; cards derive per-card view; visit dialog accepts the typed name; UTC day formatting; extra fixture and focused tests; checkout test scope around retained focus; payment toast action added with payment; no shift on visit; accessible check-in name; shared query hook with OWES; payment dialog remount per opening; additional payment dialog test. Their observed behavior and reasons are recorded in checklist 4.8 above.

Decisions without the owner:

1. **Debtors-present-first not shown live.** Met: no debtor was present while picker was open. Options in the report: make an extra check-in write or rely on test 53. Chose not to make an unlisted write, and the code test compares present Rami before non-present Khalid. Accepted. Undo is the live demo decision only.
2. **Name alignment fix after the head's lanes.** Met: report says Arabic name aligned to the far end in English card/picker. Options: leave for review or fix. Chose inline `dir="auto"` span and `self-start`, then targeted tests/lint/typecheck/classes. Accepted as a contained visual correction; F3 identifies the remaining accessibility metadata gap. Undo via the two named class/markup edits, as report states.
3. **Other departures in the report.** Chose smaller/local changes under the autonomy rule: default input size, first-group-only present, local row view, UTC day, checkout focus responsibility in occupancy, toast action with payment, omit shift, extra copy/tests and query/key mounting choices. Accepted as scope-preserving; see checklist 4.8. The named-visit callback is a verified gap rather than an accepted departure.

## Not checked, and why

- No local tests, build, server or database were run, as the review prompt explicitly forbids them. CI status was read from GitHub and is green; executor's local runs and live-demo observations are attributed to `4_REPORT_PR2.md`, not independently reproduced.
- The full 390/768/1440 real run and its network traces were not independently reproduced.
- The first `git fetch origin` failed because the shared worktree's `FETCH_HEAD` path was denied. The explicit PR-head fetch succeeded and the exact requested SHA was reviewed. Final `gh pr view 119 --json headRefOid` returned the same SHA, so head did not move.
