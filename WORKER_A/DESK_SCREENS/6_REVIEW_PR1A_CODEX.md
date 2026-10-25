# Review — DESK_SCREENS PR 1a (#116) — Codex
Head: 30c48633c74163a4f3b69032853bd8ecbd459b30 · checks: green · head moved: no
Verdict: mergeable

## Findings (most severe first)

None.

## Checklist 4.1 – 4.11

### 4.0 First steps
✔ Head matches the stated SHA; PR merge state CLEAN. Every listed check passed. Four commit subjects: `feat(desk): check visitors in and out at the desk` (49 chars), `feat(occupancy): show the desk who is present` (45), `feat(dashboard): add the page's bottom action bar` (49), `feat(api): keep one idempotency key per intent` (46). Each has a body. No subject/body names an AI tool and no `Co-Authored-By` line appears.

### 4.1 Idempotency key

✔ One key is held by each open check-in/check-out dialog; retries and edits retain it. Check-in calls `renew()` only when changing closed→open; checkout gets a fresh key when its dialog mounts on opening. Errors do not renew. Closing and starting a new opening is a new intent. `quoteIsStale` uses `> 4 minutes`, as S2 requires. The write transport retries only keyed writes; manual override writes are unkeyed. Lost network/timeout failures expose a safe retry line.
✔ Check-in and check-out attach `Idempotency-Key`; terms and quote GETs do not. Payment is the check-out's embedded payment and shares its key. The repository test verifies these two write routes and plain reads. Transport retry test coverage and executor's offline network log are consistent; the latter is report-only evidence.

### 4.2 Money
✔ Quote is the source for due; agorot remain integers. The money helper caps recorded visit payment at due, shows change, and sends `money.recorded`. Received defaults to due until edited. Stale quotes refresh before sending; changed charge blocks send. Boundary 4:00 exactly is fresh, 4:00.001 stale, consistent with “older than 4 minutes.”
✔ Debt form requires phone if no customer and any balance remains. `mayTypePrice` comes from visit terms; typed price requires amount and schema-required reason; reception without permission closes unpriced. Toast amount/method come from `VisitCheckOut`; remainder is derived from its returned visit charge and payment. Money rendering uses `priceText`/`shekelsOf`, with LTR price spans.

### 4.3 Authorization and roles
✔ UI gates price entry with server `mayTypePrice`; server contract refuses unauthorized price entry and every desk route has server role authorization. Check-out maps 403 to a no-longer-open message and invalidates `['me']`. Desk's route reads occupancy, visit terms, and `/manage/spaces/:id` for shifts. The contract marks all three as staff-readable; no owner-only settings route is read.

### 4.4 Present list and live status
✔ Occupancy uses 30s polling, disables background polling, and refetches always on focus. Existing data remains on refresh failure; first-load failure has retry. Gaza clock is used for displayed times and shift selection; durations use server instants; override remaining rounds up. Tests cover midnight and the 30s visibility behavior. Capacity count uses settled occupancy response, no uncollected sum.
✔ Status control offers all override durations, clear-to-automatic, closed-state reason and `SPACE_NOT_OPEN` refusal.


### 4.5 Bottom action bar and toasts
✔ Bar is below 768 px, top action above; shell reserves content padding while slot filled. The shared routing store is ref-counted and each page slot releases it on effect cleanup. `shared/routing` imports no feature/page modules; provider reads it and offsets the toaster.

### 4.6 Accessibility and RTL
✔ One route title `h1`; present section has heading; dialogs have title, autofocus and return focus; row action labels include person name; money group has accessible label; touch sizing is design-system default with executor report measuring 44/44/48 px (report evidence only). Classes use logical direction conventions per CI. Money inputs/time values set LTR/auto direction and inserted names are isolated or `dir=auto`.

### 4.7 Words
✔ New English/Arabic catalogues have matching typed shapes; counted lines use plural helpers (Arabic six forms). `Check out` / `Check out {name}` are used in the row action and provide distinct visible/accessible names; they fill a real user-facing gap. No `PRNUM` remains in `docs` or `apps`. Contract route errors relevant here have catalogue entries: check-in warnings are separate warning lines; check-out includes `VISIT_ALREADY_CLOSED`, `PAYMENT_EXCEEDS_DUE`, `VISIT_NOT_PRICED` (unpriced payment impossible in UI), `VISIT_HAS_CUSTOMER`, `PRICE_TYPING_NOT_ALLOWED`, generic conflict/forbidden/not_found/validation; override `SPACE_NOT_OPEN` is in shared errors. Server error codes for routes not implemented in 1a (collect, debt, write-off, pricing) are outside this PR.

### 4.8 Tests
✔ Tests 1–30 and 40 are present (table below). Key, money, role, state, warn checks exercise actual hooks/repository/transport and observe request bodies, headers or visible outcomes. Test 7 uses a changed mutation (compute a charge from rates/stay) because occupancy response has no rates; the replacement still fails if the view stops using server `chargeNowAgorot`. Test 26 replacement (typed charge not sent) fails on request-body assertion; required-reason omission itself is guarded by shared schema validation. Test 29's navigation-before-sign-out mutation is caught in the sign-out failure path where address must remain. The report describes two local 3s timeouts; both ran alone and CI's full component lane passed. Plausible load sensitivity of lazy shell tests, not a demonstrated product defect.

### 4.9 Architecture and scope
✔ Shared boundaries hold; `desk`/`occupancy` do not import each other; route lazily loads desk only in dashboard. No API/shared package or design-system diff; no PR 1b implementation. Semantic tokens used. Findings 160 (PR 2), 162 and 163 (PR 3), 164 (PR 1b) are explicitly scheduled later in plan; 161 alone is due now and is documented.

### 4.10 Documents
✔ Web descriptions cover present list, check-in/out, not the later uncollected/debt/write-off work; API description includes already-built API capabilities. Decision/history additions use date and #116. Architecture rules align with code. Overview/README updates are brief and no `PRNUM` marker remains. The new finding 161 records the deliberately omitted daily log.

### 4.11 Executor departures judged
- Break 7: accepted. The occupancy payload exposes server charge but not rates, so the described browser-rate break could not be applied; the alternate mutation checked the view's server charge.
- Break 26: accepted. Schema already requires the reason; dropping the typed charge was a meaningful alternative mutation and the test asserts the submitted charge/reason.
- Break 29: accepted. Navigating early has no success-path observable difference; failure-path assertion that the user remains on desk with session intact is the right outcome check.
- Extra `checkOut.open` and `openName`: accepted; needed visible and named row action.
- No `DeskAbilities` type: accepted; no ability consumer exists in PR 1a and adding unused code would be unjustified.
- PresentList focus rule in occupancy: accepted; row action lifecycle belongs with the list and is tested.
- Exporting state-now query: accepted; page consumes the shared query to pass the full state to check-in.
- Route test transport answers desk reads: accepted, needed because reception lands on the real desk.
- Checkout form restructuring: accepted; preserves contract and avoids ref access during render.

## Tests table (4.8)

| # | file | present / missing / weaker |
|---:|---|---|
| 1 | `shared/api/idempotency/withIdempotencyKey.unit.test.ts` | present |
| 2 | `shared/api/idempotency/useIntentKey.component.test.tsx` | present |
| 3 | `shared/api/client/request.unit.test.ts` | present |
| 4 | `pages/dashboard/shell/DashboardLayout.component.test.tsx` | present |
| 5 | `features/occupancy/repository/occupancyRepository.unit.test.ts` | present |
| 6 | `features/occupancy/hooks/now/useStateNowQuery.component.test.tsx` | present |
| 7 | `features/occupancy/hooks/now/usePresentList.component.test.tsx` | present |
| 8 | same | present |
| 9 | `features/occupancy/services/{stayDuration,overrideLeft}.unit.test.ts` | present |
| 10 | `features/occupancy/components/PresentList.component.test.tsx` | present |
| 11–12 | `features/occupancy/hooks/status/useLiveStatusControl.component.test.tsx` | present |
| 13 | `features/occupancy/components/LiveStatusControl.component.test.tsx` | present |
| 14 | `features/desk/services/visitRates.unit.test.ts` | present |
| 15 | `features/desk/services/currentShift.unit.test.ts` | present |
| 16 | `features/desk/services/moneyOf.unit.test.ts` | present |
| 17 | `features/desk/services/quoteAge.unit.test.ts` | present |
| 18 | `features/desk/services/warningLines.unit.test.ts` | present |
| 19 | `features/desk/repository/deskRepository.unit.test.ts` | present |
| 20–21 | `features/desk/hooks/check-in/useVisitDialog.component.test.tsx` | present |
| 22 | `features/desk/hooks/money/useMoneyBlock.component.test.tsx` | present |
| 23–27 | `features/desk/hooks/check-out/useCheckOutDialog.component.test.tsx` | present |
| 28 | `features/desk/components/check-out/CheckOutDialog.component.test.tsx` | present |
| 29 | `pages/dashboard/space/desk/useSwitchStaff.component.test.tsx` | present |
| 30 | `pages/dashboard/routes.component.test.tsx` | present |
| 40 | `shared/copy/catalogues.unit.test.ts` (existing) | present |

## Not checked, and why

No executable code/tests/build were run, per the review prompt's read-only restrictions. CI checks were green. The executor report's real-run details, screenshots and test break outputs were not independently available for verification; treated as report-only evidence. Repository code was reviewed at the specified commit via `git show`.



