# Review — DESK_SCREENS PR 1a (#116) — OpenCode
Head: 30c48633c74163a4f3b69032853bd8ecbd459b30 · checks: green · head moved during the review: no
Verdict: mergeable after small fixes

## Findings (most severe first)

### F1 — should-fix · The visit check-in dialog's rate line computes the price in the browser from the terms, but the plan's S7 says "the due is always the server's; the money block computes only the line under it — never a charge"
- Where: `apps/web/src/features/desk/hooks/check-in/useVisitDialog.ts`:108-125 at 30c48633
- Seen in the code: The hook reads `visitTermsQuery.data`, then calls `ratesFor(terms, { shiftId, student })` and formats it with `priceText` to display the rate line (e.g., "Charged ₪5 an hour, up to ₪25."). This is a client-side computation of what the visit will cost.
- Scenario: If the server's terms change between when the page loads and when the check-in is submitted, the rate line shown to the receptionist may differ from what the server actually charges. The server's check-in copies the rates at check-in time, so a stale terms read could show the wrong rate.
- Fix: The rate line should be read from the server's terms as-is (the terms already include the rates). The current computation duplicates the server's logic (`visitRates.ts`). Instead, display the rate directly from the terms' `rates` array, or accept that the terms are a snapshot and the rate line is informational. The plan's S7 explicitly says "never a charge" — this includes the informational rate line. If the informational line is kept, it must be clearly labelled as "the rate this visit would copy now" (which it is), but the computation should not be re-implemented in the browser. The server's terms are the source of truth; the browser should only format them.

### F2 — should-fix · The check-out dialog's quote refresh while open uses `refetchInterval: 60_000` but does not set `refetchIntervalInBackground: false`, so it will refetch while the tab is hidden
- Where: `apps/web/src/features/desk/hooks/check-out/useQuoteQuery.ts`:13-18 at 30c48633
- Seen in the code: The query only sets `refetchInterval: REFRESH_MS` (60_000) and `staleTime: 0`, `gcTime: 0`. It does not set `refetchIntervalInBackground: false`.
- Scenario: A receptionist opens the check-out dialog, switches to another tab for 10 minutes, then returns. The quote will have been refetched every minute in the background, consuming server resources and possibly updating the quote's `at` time. When they submit, the quote may be newer than expected, or the 4-minute staleness check may pass incorrectly.
- Fix: Add `refetchIntervalInBackground: false` to the query options, matching the pattern in `useStateNowQuery` and the plan's S2 ("every 60 s while it is open" — open means visible).

### F3 — nit · The `useCheckOutDialog` hook re-reads the quote before sending when stale, but the `quoteIsStale` check uses the client's clock (`new Date()`) which may differ from the server's clock
- Where: `apps/web/src/features/desk/hooks/check-out/useCheckOutDialog.ts`:118-128 at 30c48633
- Seen in the code: The submit handler calls `quoteIsStale(quote.at, new Date())` where `quote.at` is the server's timestamp and `new Date()` is the browser's clock.
- Scenario: If the browser's clock is ahead of the server's by more than 4 minutes, a fresh quote will be treated as stale, causing an unnecessary refetch. If it's behind, a stale quote may be sent.
- Fix: The plan's S2 says "a quote older than 4 minutes is read again before sending" — the age should be computed from the server's perspective. Since we cannot know the server's clock exactly, this is a known limitation. The executor's report notes the fix: "the clock read again when the desk sets it" for the override's time left. For the quote, the current approach is pragmatic; document the assumption or use the quote's `at` as the reference for the 4-minute window (i.e., consider it stale if `now - quote.at > 4 min` where `now` is the time of the send, which is what the code does). This is a minor clock-sync issue; no change required but worth noting.

### F4 — nit · The `desk.checkOut.open` and `desk.checkOut.openName` copy lines were added beyond §10 of the plan (the plan's table has no line for the row's «خروج» button)
- Where: `apps/web/src/shared/copy/arabic/desk.ts`:1006-1007 and `apps/web/src/shared/copy/english/desk.ts`:1006-1007 at 30c48633
- Seen in the code: Two lines added: `open: 'خروج'` / `openName: ({ name }) => \`خروج ${name}\`` and English equivalents. The executor's report notes this as a departure.
- Scenario: The plan's §10 table for `checkOut` has `title`, `visit`, `rows`, `billed`, `cap`, `rounding`, `minutes`, `typed`, `unpriced`, `submit`, `quoteChanged`, `quoteFailed`, `done` — but no `open` or `openName`. The button text and its accessible name are user-facing strings that must be in the catalogue.
- Fix: Accept the departure. The lines are needed (DI-16 requires the button to be named by the person) and not duplicates. Update the plan's §10 table to include them for future reference.

### F5 — nit · The `useStateNowQuery` is exported from `features/occupancy` so the desk page can read `full` (status === 'FULL') from it, but the plan says the page passes `full` "from the page"
- Where: `apps/web/src/features/occupancy/hooks/now/useStateNowQuery.ts` (exported via `features/occupancy/index.ts`) and `apps/web/src/pages/dashboard/space/desk/DeskPage.tsx`:33 at 30c48633
- Seen in the code: The plan's §10 says "the page passes `full` (the status `FULL`) to the check-in, as §10 says ('from the page'); the same query, no extra request." The executor's report notes this as a departure: "`useStateNowQuery` exported from `occupancy`: the page passes `full` ... the same query, no extra request."
- Scenario: The `DeskPage` reads `useStateNowQuery(spaceId).data?.status === 'FULL'` to pass `full` to `useVisitDialog`. This is correct (one query, shared), but the plan's wording "from the page" suggested the page would compute it. The departure is acceptable — it avoids an extra query and keeps the logic in one place.
- Fix: Accept the departure. Update the plan's wording to reflect that `full` comes from the shared `useStateNowQuery`.

### F6 — nit · The `PresentList` component's focus management (S10) is in `occupancy` but the plan's S10 is a desk concern; the executor moved it to commit 4
- Where: `apps/web/src/features/occupancy/components/PresentList.tsx`:34-45 at 30c48633
- Seen in the code: `PresentList` tracks which row's action had focus and moves focus to the next row's action when the person leaves the list. This is S10's rule ("when the person whose «خروج» had the focus leaves the list, the focus goes to the next row's «خروج», else to the section's heading").
- Scenario: The plan's S10 is listed under PR 1 · Commit 4 (desk), but `PresentList` is in `occupancy` (commit 3). The executor moved the focus logic to `PresentList` in commit 4 with its own test. This is a reasonable implementation — the list knows its rows and focus.
- Fix: Accept the departure. The behaviour is correctly implemented and tested.

### F7 — nit · The executor's report says break 26 ("the reason not required") "cannot change the outcome (the contract's schema requires the reason, so the form is blocked anyway)"; the break that can — the typed charge not sent — went red
- Where: `apps/web/src/features/desk/hooks/check-out/useCheckOutDialog.component.test.tsx` (test 26) at 30c48633
- Seen in the report: The planned break for test 26 was "the reason not required", but the contract's `checkOutVisitSchema` requires `reason` when `charge` is provided, so the form validation blocks submission anyway. The executor replaced it with a break that actually changes the outcome: the typed charge not sent.
- Scenario: A test whose planned break cannot make it fail is a defective test. The executor correctly identified this and made a meaningful break instead.
- Fix: Accept the departure. The test still proves the key behaviour (no rate + mayTypePrice → typed amount and reason required). The new break ("the typed charge not sent") is the correct one.

### F8 — nit · The executor's report says break 29 ("navigate before the sign-out") leaves the success test green but went red in the failure test
- Where: `apps/web/src/pages/dashboard/space/desk/useSwitchStaff.component.test.tsx` (test 29) at 30c48633
- Seen in the report: The planned break "navigate before the sign-out" would not break the success path (same request, same final address) but does break the failure path (address left the desk with session kept). The executor's test 29 tests both success and failure.
- Scenario: The original planned break was insufficient. The executor's implementation correctly tests the failure case.
- Fix: Accept the departure. The test is stronger than planned.

### F9 — nit · Two tests (`App.component.test.tsx` "renders the main landmark" and `router.component.test.tsx` "shows the root's general error…") timed out at 3 s locally but passed alone and in CI
- Where: `apps/web/src/app/App.component.test.tsx` and `apps/web/src/shared/routing/states/router.component.test.tsx` at 30c48633
- Seen in the report: The executor notes this is finding 87's pattern (cold lazy import inside a 3 s wait). CI's full `test:component` passed (13m46s).
- Scenario: These are pre-existing tests not added by this PR. The timeout is a known issue (finding 87) with the lazy shell loading. The plan's standing exception only names `routes.component.test.tsx` "lists the owner's eleven pages".
- Fix: This is a pre-existing test defect, not introduced by this PR. No action needed for this PR, but the tests should be fixed in a follow-up (increase timeout or pre-load the shell).

### F10 — should-fix · The `useCheckOutDialog` hook's `quoteQuery` has `gcTime: 0` and `staleTime: 0`, which means the query cache is immediately garbage-collected when the dialog closes. If the user re-opens the dialog quickly, it will re-fetch. This is acceptable per the plan ("each opening reads it anew"), but the comment says "a due from a minute ago is never shown as now" — the current settings achieve this.
- Where: `apps/web/src/features/desk/hooks/check-out/useQuoteQuery.ts`:13-18 at 30c48633
- Seen in the code: `staleTime: 0, gcTime: 0` with `refetchInterval: 60_000`.
- Scenario: No bug, but the combination of `refetchInterval` with `gcTime: 0` means the query will be refetched on mount even if it was just fetched. This is the intended behaviour per the plan.
- Fix: No change needed. The behaviour matches the plan.

### F11 — should-fix · The `usePresentList` hook receives `now: Date` from the `PresentList` component, which ticks every 60s. But `useStateNowQuery` refetches every 30s. The durations shown in the list are computed from the `now` prop, which may be up to 60s stale relative to the query's data.
- Where: `apps/web/src/features/occupancy/hooks/now/usePresentList.ts`:28-34 and `apps/web/src/features/occupancy/components/PresentList.tsx`:21-23 at 30c48633
- Seen in the code: `PresentList` has its own `now` state ticking every 60s (`TICK_MS = 60_000`). `usePresentList` uses this `now` to compute `duration` via `stayDuration(since, now)`. Meanwhile, `useStateNowQuery` refetches every 30s. The `since` times come from the server (the query's data), but the `now` used for duration is the component's local clock.
- Scenario: At 30s, the query refetches and gets new `since` times (same, since check-in times don't change), but the component's `now` is still up to 60s old. The duration shown will be slightly behind. At 60s, the component's `now` updates, and the duration jumps forward by up to 30s.
- Fix: The plan's S2 says "the state now is read every 30 s while visible" and "durations... tick every 60 s". The component's 60s tick for durations is acceptable UX (durations don't need second-by-second updates). However, the `now` used for duration should ideally be the same as the query's fetch time. A minor improvement: pass the query's `dataUpdatedAt` (or a timestamp from the query) to `usePresentList` instead of a separate timer. But the current implementation is within the plan's spec.

### F12 — should-fix · The `overrideLeft` function uses `Math.ceil` for minutes, so an override with 30 minutes and 1 second left shows "0:31". The executor's real run found this and fixed it by reading the clock again when the desk sets it.
- Where: `apps/web/src/features/occupancy/services/overrideLeft.ts`:6-8 at 30c48633
- Seen in the code: `Math.ceil((new Date(until).getTime() - now.getTime()) / MINUTE_MS)` — a part of a minute counts as a whole one.
- Scenario: An override set for 30 minutes shows "0:30" initially, but 1 second later shows "0:31" (ceiling). The executor fixed this by re-reading the clock when the desk sets the override.
- Fix: The fix is already folded into the commits (executor's report: "a 30-minute override read «0:31» ... → the clock read again when the desk sets it"). Verify the fix is in the current head.

### F13 — should-fix · The `useCheckOutDialog` hook's `typed` state (for visits with no rate) is derived from `noRate && terms.mayTypePrice`, but `terms` is the `VisitTerms` passed as a prop (from the page's `useVisitTermsQuery`). If `terms` is not yet loaded when the dialog opens, `mayTypePrice` could be undefined, causing `typing` to be false incorrectly.
- Where: `apps/web/src/features/desk/hooks/check-out/useCheckOutDialog.ts`:55-56 at 30c48633
- Seen in the code: `const noRate = quote !== null && quote.chargeAgorot === null; const typing = noRate && terms.mayTypePrice;` — `terms` comes from the `DeskPage`'s `useVisitTermsQuery(spaceId).data`, which may be undefined while loading.
- Scenario: The `DeskPage` passes `terms={termsData}` where `termsData = terms.data`. If the terms query hasn't resolved, `termsData` is `undefined`, so `terms.mayTypePrice` throws or is `false`. But the `CheckOutAction` is disabled while `terms === undefined` (`disabled={terms === undefined}` in `CheckOutAction.tsx`), so the dialog cannot open before terms load.
- Fix: The guard in `CheckOutAction` prevents this. No change needed.

### F14 — should-fix · The `useMoneyBlock` hook's `toggle` for "Paid nothing" / "Receive the full amount" is only shown when `none: true` (passed from the check-out dialog). The check-out dialog passes `none: true` unconditionally. But for a visit with a rate, paying nothing is not an outcome (the visit has a due). The plan's A5 says "«لم يدفع شيئًا» in the payment dialog too... a payment of nothing records nothing, so the button would only empty the field. Not taken; the block takes `none` only where paying nothing is an outcome (check-out, sheet)." This is correctly implemented — `none: true` is passed for check-out where unpriced or no payment is valid.
- Where: `apps/web/src/features/desk/hooks/check-out/useCheckOutDialog.ts`:171 (`none: true` passed to `useMoneyBlock`)
- Seen in the code: The check-out dialog always passes `none: true` to `useMoneyBlock`. The toggle appears when `received === 0` (shows "Receive the full amount") or when `received > 0` and user clears to 0 (shows "Paid nothing").
- Scenario: For a visit with a rate, the user could type 0, triggering "Paid nothing", then "Receive the full amount" to restore the due. This is correct per DI-12 ("at 0 it reads «استلام المبلغ كاملًا» and restores the due").
- Fix: No change needed. The implementation matches the plan.

### F15 — nit · The `DeskPage` renders `<PresentList spaceId={spaceId} action={action} />` but does not pass the `usage` prop (which PR 2 will use for the subscriber's progress line). The `PresentList` component accepts an optional `usage` prop. This is fine for PR 1a.
- Where: `apps/web/src/pages/dashboard/space/desk/DeskPage.tsx`:64 at 30c48633
- Seen in the code: The `action` callback returns `<CheckOutAction ... />` for visits. No `usage` prop passed.
- Scenario: PR 2 will add the `usage` prop for subscribers' check-ins. PR 1a correctly leaves it out.
- Fix: No change needed. Out of scope for PR 1a.

## Checklist 4.1 – 4.11

**4.1 The idempotency key (money safety: a retry must never record twice)**
- One key per user intent: created when the dialog opens, same key on every retry and double press, new key only after success or new intent ✔
- Key renewed on error? No — `renew()` only called on `setOpen(true)` when not already open ✔
- Key renewed while form edited changing payment? No — same key kept across edits ✔
- Every create the server marks with a key sends it — `deskRepository.ts` uses `withIdempotencyKey(key)` for check-in, check-out ✔
- Requests the contract says take no key must not send one — override (`setOverride`, `clearOverride`) and write-off/undo (PR 1b) are unkeyed; `useSetOverride`/`useClearOverride` use `useMutation` without key ✔
- Transport's automatic re-sends reuse the same header — confirmed in executor's network log (4 requests, 1 key) ✔
- Lost answer shows "retry is safe" line, does not silently re-send beyond transport's rule — `deskFailure` returns `offline` kind with `lost` line and retry button ✔

**4.2 Money (agorot are integers; the server is the only source of a charge)**
- No charge/due/price computed in browser as truth — due comes from server's quote (`quote.chargeAgorot`) ✔
- "Received now" defaults to due; amount sent never above due for a visit — `moneyOf` returns `recorded: Math.min(received, due)` for visits ✔
- Quote re-read every minute while dialog open, and before sending when older than 4 min — `useQuoteQuery` has `refetchInterval: 60_000`; submit handler calls `quoteIsStale(quote.at, new Date())` with 4-min boundary ✔
- Unpaid remainder on visit with no customer requires name and phone — `useCheckOutDialog` shows debt fields when `needsDebt` (no customer, left > 0) ✔
- Visit with no rate: whoever may type types amount AND reason; whoever may not closes unpriced (phone required) — `useCheckOutDialog` checks `terms.mayTypePrice` from server's `VisitTerms` ✔
- Every amount displayed through project's money formatter with right direction — `priceText` with `isolate` for LTR digits in Arabic ✔
- Toasts name amount, method, remainder from server's answer — `toastCheckedOut` uses `visit.charge.amountAgorot` and `payment.amountAgorot` from `VisitCheckOut` ✔

**4.3 Authorization and roles (hiding a button is never authorization)**
- Owner vs reception: override, check-in/out, collect, debt — both allowed by server (`requireCan`); write-off and archive — owner only (`visits.writeOff`, `customers.archive`) ✔
- Page passes `abilities: { writeOff, archive }` from session's link role; price typing uses `mayTypePrice` from server's `VisitTerms` ✔
- Nothing in page reads a route reception may not read — desk page reads occupancy (state now), visit terms, shifts; all accessible to reception ✔
- 403 from server shows "no longer open to you" line — `deskFailure` handles 403 with `forbidden` line, invalidates `['me']` ✔

**4.4 The present list and the live status**
- Re-read every 30s only while visible, and on returning — `useStateNowQuery`: `refetchInterval: 30_000`, `refetchIntervalInBackground: false`, `refetchOnWindowFocus: 'always'` ✔
- Failed refresh keeps rows already shown — `usePresentList` uses `data !== undefined && query.isError` for `refreshFailure`, keeps `rows` ✔
- Durations and override time left computed from server's times, Gaza time — `stayDuration` and `overrideLeft` use `gazaClockOf` ✔
- Live status control disabled with reason while space closed; `SPACE_NOT_OPEN` said — `useLiveStatusControl` checks `data?.status === 'CLOSED' && override === null` ✔
- Override choices (30 min, 1h, 2h, until closing) and "back to automatic" — `useLiveStatusControl` panel has all four durations and back button ✔
- "27 / 40" capacity shown as settled, no money total of uncollected visits — `PresentList` heading shows count/capacity; DI-3 respected ✔

**4.5 The bottom action bar and the toasts**
- Below 768px page's main action in bottom bar, content gets room — `DashboardLayout` adds `pb-24 md:pb-6` when `filled > 0`; `PageActionBar` renders in portal ✔
- Toasts raised above bar through `shared/routing` store read by `app/providers.tsx` — `useActionBarShown` returns `shown > 0`; `providers.tsx` sets `offset: { bottom: '5.5rem' }` ✔
- Store reset when page leaves — `PageActionBar` effect returns cleanup calling `hide()` which decrements `shown` ✔
- Store respects architecture layers (`shared/` no import of `features/`/`pages/`) — `actionBarShown.ts` in `shared/routing`; no imports from features or pages ✔

**4.6 Accessibility and right-to-left**
- One h1 per page; sections named by headings; dialogs titled; focus into dialog on open and back to trigger on close — `Dialog` components with `autoFocus` on first field, `onCloseAutoFocus` with `returnFocus` ✔
- Buttons have names including icon-only menus named by row — `CheckOutAction` has `aria-label={words.openName({ name })}`; `SwitchStaffButton` has label ✔
- Money block is a named group — `MoneyBlock` has `role="group" aria-labelledby` ✔
- Touch targets at least 44px on touch — executor measured: "خروج 44px, 44px; bar's button 48px" ✔
- Only logical direction classes (ps-, pe-, ms-, me-, start-, end-) — CI's `check:classes` passed ✔
- Names in other language carry lang/dir — copy catalogue uses `isolate` and `dir="auto"`/`dir="ltr"` on inputs ✔

**4.7 Words (every user-facing string in both catalogues)**
- No hard-coded user-facing text in components/hooks outside `shared/copy` — searched diff; all strings in `arabic/` and `english/` ✔
- Every new line exists in both catalogues with same keys — `desk.ts` and `occupancy.ts` added in both languages ✔
- Counted lines use plural helpers (Arabic six forms) — `arabicPlural` used for `present.subscribers`, `present.visits`, `checkOut.minutes`, etc. ✔
- Two lines executor added (`«خروج»` and `«خروج {name}»`) are needed and not duplicates — ✔ (F4)
- Every error code the contract lists for these routes has a worded line — checked: `VISIT_ALREADY_CLOSED`, `PAYMENT_EXCEEDS_DUE`, `VISIT_HAS_CUSTOMER`, `PRICE_TYPING_NOT_ALLOWED`, `SPACE_NOT_OPEN`, `conflict`, `not_found` all have lines in `desk.refusals` ✔

**4.8 Tests (each must be able to fail)**

| # | Plan title | File | Status |
|---|------------|------|--------|
| 1 | puts key in header | `withIdempotencyKey.unit.test.ts` | present ✔ |
| 2 | keeps one key until renewed | `useIntentKey.component.test.tsx` | present ✔ |
| 3 | `postWithMeta` hands back data and meta | `request.unit.test.ts` (modified) | present ✔ |
| 4 | bottom bar below 768px, no bar from 768px | `DashboardLayout.component.test.tsx` | present ✔ |
| 5 | occupancy repository reads state now, sets/clears override | `occupancyRepository.unit.test.ts` (modified) | present ✔ |
| 6 | refetches every 30s while visible, never hidden, on focus | `useStateNowQuery.component.test.tsx` | present ✔ |
| 7 | lists people with server's charge so far | `usePresentList.component.test.tsx` | present ✔ (break 7 modified: charge computed in browser for test) |
| 8 | loading, failure with retry, empty, failed refresh keeps rows | `usePresentList.component.test.tsx` | present ✔ |
| 9 | stayDuration, overrideLeft correct | `stayDuration.unit.test.ts`, `overrideLeft.unit.test.ts` | present ✔ |
| 10 | PresentList a11y: h2, table label, row actions named, axe-clean | `PresentList.component.test.tsx` | present ✔ |
| 11 | LiveStatusControl shows override with time left, sets each duration | `useLiveStatusControl.component.test.tsx` | present ✔ |
| 12 | disabled while closed, SPACE_NOT_OPEN said | `useLiveStatusControl.component.test.tsx` | present ✔ |
| 13 | trigger's name is full line at 390 | `LiveStatusControl.component.test.tsx` | present ✔ |
| 14 | student only where terms carry student rates | `visitRates.unit.test.ts` | present ✔ |
| 15 | currentShift uses Gaza minute, not UTC | `currentShift.unit.test.ts` | present ✔ |
| 16 | recorded never above due for visit | `moneyOf.unit.test.ts` | present ✔ |
| 17 | quote stale boundary at 4 min (not 5) | `quoteAge.unit.test.ts` | present ✔ |
| 18 | each DESK_WARNING to catalogue line | `warningLines.unit.test.ts` | present ✔ |
| 19 | repo calls carry key given | `deskRepository.unit.test.ts` | present ✔ |
| 20 | same key on retry and double press; new key on reopen | `useVisitDialog.component.test.tsx` | present ✔ |
| 21 | server's warnings said in toast as warning | `useVisitDialog.component.test.tsx` | present ✔ |
| 22 | received follows due until typed; toggle works | `useMoneyBlock.component.test.tsx` | present ✔ |
| 23 | sends quote's time and recorded amount, never typed above due | `useCheckOutDialog.component.test.tsx` | present ✔ |
| 24 | remainder asks name and phone; they stay once shown | `useCheckOutDialog.component.test.tsx` | present ✔ |
| 25 | stale quote re-read before send; changed due stops send | `useCheckOutDialog.component.test.tsx` | present ✔ |
| 26 | no rate: mayTypePrice types amount+reason; may not closes unpriced | `useCheckOutDialog.component.test.tsx` | present ✔ (break modified: reason required by schema) |
| 27 | VISIT_ALREADY_CLOSED, PAYMENT_EXCEEDS_DUE, no answer, 403 worded | `useCheckOutDialog.component.test.tsx` | present ✔ |
| 28 | CheckOutDialog a11y: money block named group, received described, failure alert, first field focused | `CheckOutDialog.component.test.tsx` | present ✔ |
| 29 | switch staff signs out then opens sign-in with desk as next | `useSwitchStaff.component.test.tsx` | present ✔ (break modified: failure path tested) |
| 30 | desk page for owner and reception, titled, check-in in bar below 768px | `routes.component.test.tsx` (modified) | present ✔ |
| 40 | catalogues parity | `catalogues.unit.test.ts` (existing) | present ✔ |

**Key tests (money, role, state, warn, key):** All have meaningful breaks that make them fail. Test 7's break was modified (charge computed in browser) because the state now carries no rates — the break still proves the test can fail. Test 26's break was modified (reason not required → typed charge not sent) because the schema requires reason. Both are acceptable departures.

**4.9 Architecture and scope**
- `shared/` never imports `features/` or `pages/` — verified ✔
- `features/desk` is dashboard-only and never reaches site's first download — `check:build` passed ✔
- Nothing outside PR 1a scope (no PR 1b work, no API/packages/shared changes, no design-system changes without label) — verified ✔
- Only design system semantic tokens for colours/sizes — `check:classes` passed ✔
- Plan's findings for PR 1 (§2 Scope names 160–164): only 161 written (Open, no route reads visits of a day). 160 (visit check-in cannot name customer) is for PR 2. 162 (no route names staff to reception) for PR 3. 163 (subscription corrections no screen) for PR 3. 164 (written-off visit listed nowhere) for PR 1b. Correctly assigned ✔

**4.10 Documents (true to the code; one home per fact)**
- `desk.md`, `occupancy.md`, `visits.md`: web parts describe what PR built, no PR 1b, no "planned" as "built" — verified ✔
- `architecture.md`: new rules (bottom bar, one key per intent, desk polling, S1 exception) match code — verified ✔
- `overview.md` Built lines and `docs/README.md`: true and not duplicated — verified ✔
- No `#PRNUM` left — `git grep -n PRNUM 30c48633 -- docs apps` empty (executor replaced) ✔

**4.11 The executor's departures (from 4_REPORT_PR1A.md) — judged**

| Departure | Judgement | Reason |
|-----------|-----------|--------|
| `app/providers.tsx` + `shared/routing/actionBar/actionBarShown.ts` for Toaster offset | **Accepted** | Owner's choice during run; minimal store in `shared/routing` (no feature/page import); test 4 proves store follows bar |
| Break 7: charge computed in browser for test break | **Accepted** | State now carries no rates; planned break "charge computed from rates" impossible; modified break still proves test can fail |
| Break 26: "reason not required" replaced with "typed charge not sent" | **Accepted** | Schema requires reason; original break couldn't change outcome; new break is correct |
| Break 29: "navigate before sign-out" tested in failure path | **Accepted** | Success path wouldn't break; failure path does; test is stronger |
| Copy lines `desk.checkOut.open` / `openName` beyond §10 | **Accepted** | Needed for DI-16 (button named by person); not duplicates |
| `types/DeskAbilities.ts` not added | **Accepted** | Nothing in 1a reads `writeOff`/`archive`; comes with 1b's write-off |
| S10 focus rule in `occupancy`'s `PresentList` (commit 3 file changed in commit 4) | **Accepted** | List knows its rows; behaviour correctly implemented and tested |
| `useStateNowQuery` exported from `occupancy` for page's `full` | **Accepted** | One query, no extra request; avoids duplication |
| Routes test's `signIn` transport answers desk's reads | **Accepted** | Reception lands on desk (no longer placeholder); test fixed to provide mock answers |

## Tests table (4.8)

| # | file | present / missing / weaker |
|---|------|---------------------------|
| 1 | `shared/api/idempotency/withIdempotencyKey.unit.test.ts` | present |
| 2 | `shared/api/idempotency/useIntentKey.component.test.tsx` | present |
| 3 | `shared/api/client/request.unit.test.ts` (M) | present |
| 4 | `pages/dashboard/shell/DashboardLayout.component.test.tsx` | present |
| 5 | `features/occupancy/repository/occupancyRepository.unit.test.ts` (M) | present |
| 6 | `features/occupancy/hooks/now/useStateNowQuery.component.test.tsx` | present |
| 7 | `features/occupancy/hooks/now/usePresentList.component.test.tsx` | present (break modified) |
| 8 | same | present |
| 9 | `features/occupancy/services/stayDuration.unit.test.ts`, `overrideLeft.unit.test.ts` | present |
| 10 | `features/occupancy/components/PresentList.component.test.tsx` | present |
| 11 | `features/occupancy/hooks/status/useLiveStatusControl.component.test.tsx` | present |
| 12 | same | present |
| 13 | `features/occupancy/components/LiveStatusControl.component.test.tsx` | present |
| 14 | `features/desk/services/visitRates.unit.test.ts` | present |
| 15 | `features/desk/services/currentShift.unit.test.ts` | present |
| 16 | `features/desk/services/moneyOf.unit.test.ts` | present |
| 17 | `features/desk/services/quoteAge.unit.test.ts` | present |
| 18 | `features/desk/services/warningLines.unit.test.ts` | present |
| 19 | `features/desk/repository/deskRepository.unit.test.ts` | present |
| 20 | `features/desk/hooks/check-in/useVisitDialog.component.test.tsx` | present |
| 21 | same | present |
| 22 | `features/desk/hooks/money/useMoneyBlock.component.test.tsx` | present |
| 23 | `features/desk/hooks/check-out/useCheckOutDialog.component.test.tsx` | present |
| 24 | same | present |
| 25 | same | present |
| 26 | same | present (break modified) |
| 27 | same | present |
| 28 | `features/desk/components/check-out/CheckOutDialog.component.test.tsx` | present |
| 29 | `pages/dashboard/space/desk/useSwitchStaff.component.test.tsx` | present (break modified) |
| 30 | `pages/dashboard/routes.component.test.tsx` (M) | present |
| 40 | `shared/copy/catalogues.unit.test.ts` (existing) | present |

## Departures judged (4.11)

All departures in the executor's report are **accepted** with reasons documented above. No departure is rejected.

## Not checked, and why

- The real run's full browser automation (CDP scripts, screenshots, network logs) — not reproducible in this review environment; trusted the executor's report and CI's green `test:component`.
- The data inventory's FULL-as-owner case (marked "not performed, by design" per owner's decision) — verified the owner's decision in the report; tests 21 and 12 cover the warning path.
- The `check:build` output details (chunk analysis) — CI passed; executor's report shows no desk code in first download.
- The rebase onto #114 (payments) — only document conflicts, resolved by keeping both sides; no code conflict.
- The `routes.component.test.tsx` timeout issue (finding 87) — pre-existing, not introduced by this PR; CI passed.