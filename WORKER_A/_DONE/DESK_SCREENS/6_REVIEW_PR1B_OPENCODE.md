# Review — DESK_SCREENS PR 1b (#117) — OpenCode
Head: a1193e77a63f57ed7110195fd70f2440206e4dc2 · checks: green (all 11 passed) · head moved during the review: no
Verdict: mergeable after small fixes

### Commits
- `336982e2` `feat(desk): collect the uncollected visits` (42 chars, body present, no AI tool named, no Co-Authored-By trailer)
- `a1193e77` `feat(desk): price the unpriced visits` (37 chars, body present, no AI tool named, no Co-Authored-By trailer)

## Findings (verified defects only, most severe first)

### F1 — should-fix · Stale `uncollectedPage` past the last page displays empty card with no pagination controls
- Where: [useUncollectedCard.ts](file:///C:/dev/masaha/app-design/apps/web/src/features/desk/hooks/uncollected/useUncollectedCard.ts#L47-L148) and [UncollectedCard.tsx](file:///C:/dev/masaha/app-design/apps/web/src/features/desk/components/uncollected/UncollectedCard.tsx#L87-L127) at `a1193e77`
- Seen in the code: The executor departed from the plan by storing the uncollected list page in the URL (`PAGE_PARAM = 'uncollectedPage'`), but did not use the list helper [`usePageInRange`](file:///C:/dev/masaha/app-design/apps/web/src/shared/lists/hooks/usePageInRange.ts). When the requested page exceeds `meta.totalPages`, the API returns 200 with `data: []` and `meta: { totalRecords: N, totalPages: 1, currentPage: page }`. Because `items.length === 0`, `useUncollectedCard` sets `state: 'empty'`. In `UncollectedCard.tsx`, `card.state === 'empty'` renders only `<p>{card.empty}</p>` («لا توجد مبالغ غير محصّلة.» / "Nothing left to collect."), skipping the rows, the toggle button, and `ListPagination` entirely.
- Scenario: Staff is browsing page 2 of uncollected visits (`?uncollectedPage=2`). The visits on page 2 are collected or written off (or a voided payment is settled) such that only 1 page remains (`totalPages: 1`). On re-query, the user sees "Nothing left to collect", even though uncollected visits remain on page 1. Because pagination controls are omitted in the empty state, the user has no UI mechanism to return to page 1 without manually editing the browser URL.
- Fix: Wire [`usePageInRange`](file:///C:/dev/masaha/app-design/apps/web/src/shared/lists/hooks/usePageInRange.ts) into [`useUncollectedCard.ts`](file:///C:/dev/masaha/app-design/apps/web/src/features/desk/hooks/uncollected/useUncollectedCard.ts) (passing `answer`, `placeholder: query.isPlaceholderData`, `page`, and a `replacePage` callback that updates search params), and guard `card.state === 'empty'` with `total === 0`.

## Checklist 4.1 – 4.8

### 4.1 Collect («تحصيل») — money and the key
- ✔ One idempotency key per collect intent: kept across a retry and a double press, never renewed on an error, renewed only after a success or a new opening. Sent as `Idempotency-Key` header via `withIdempotencyKey(key)` in `deskRepository.ts`.
- ✔ The amount defaults to what the row owes (`due = balanceAgorot ?? 0`); the amount sent is never above what it owes (`Math.min(received, due)` via `moneyOf`); a remainder on a row with no customer requires a mobile phone and customer name before submission; `VISIT_WRITTEN_OFF` (from `errors.ts` fallback) and `PAYMENT_EXCEEDS_DUE` (in `desk.refusals`) are worded.
- ✔ After success, the uncollected list (and anything showing the same visit) is refreshed: `useReceivePayment` calls `settle(spaceId)`, which invalidates query key `['space', spaceId]`, refreshing uncollected visits, quotes, terms, and occupancy.

### 4.2 Debt («تسجيل دين») and the write-off — no key, never re-sent
- ✔ «تسجيل دين», the write-off and its undo carry no key and are never retried automatically: `useLeaveToCustomer`, `useWriteOff`, and `useUndoWriteOff` pass no key to `deskRepository`, so the transport executes them once without retry. A lost network response displays `failure.lost` with a manual "Try again" action (finding 115).
- ✔ The write-off requires a reason (trimmed non-empty validated by `writeOffVisitSchema`); offered to the space owner only (`DeskAbilities.writeOff` derived from session link role `OWNER`); a 403 response from the server is worded via `desk.refusals.forbidden`.
- ✔ The undo is offered from the write-off's toast, which stays until closed (`duration: Infinity`, DI-29); it undoes once via `undoWriteOff`; a second trigger causes no harm because the contract specifies `DELETE .../write-off` on a visit not written off returns 200 with the visit unchanged.
- ✔ An unpriced row has no «⋯» menu: `useUncollectedCard` sets `more: abilities.writeOff && balanceAgorot !== null ? ... : null`. Consistent with contract rule where `POST .../write-off` on an unpriced visit is refused with `VISIT_NOT_PRICED`.

### 4.3 The uncollected list (and #114)
- ✔ No filter by checkout method or customer in the web: every row answered by the server is rendered. A hand-closed row reads «خروج يدوي · …» (`words.howManual`), which accurately reflects hand-closed visits returned under #114.
- ✘ (→ F1) Counts come from `answer?.meta.totalRecords` without money sum (DI-3); 3 rows shown before «عرض الكل» (DI-23); page sits in URL (`uncollectedPage`), but does not fall back to the last page when stale because `usePageInRange` is not used.
- ✔ Days read «اليوم» / «أمس» / a formatted date on Gaza's calendar via `dayWord.ts` using `gazaClockOf` and `timeZone: 'Asia/Gaza'`, independent of the browser's local time zone.

### 4.4 The unpriced list — the main departure to judge
- ✔ «بدون سعر» displays the first page only with no pagination controls, while the title counts all. Staff can reach and price subsequent visits: pricing an item invalidates `['space', spaceId]`, which refetches page 1, allowing the next unpriced visit from the server to move into the first page. The departure is acceptable as written in `2_PLAN.md` §10 Commit 6 ("The card sits under the uncollected one (xl side column), absent with none").
- ✔ Only users who may type a price see the card (`mayTypePrice` from visit terms), and the server refuses others (`PRICE_TYPING_NOT_ALLOWED` worded and invalidates terms query). The price requires both an amount and a reason; `VISIT_ALREADY_PRICED` is worded.

### 4.5 Words, accessibility, RTL
- ✔ Every user-facing string is defined in both Arabic and English catalogues with matching keys; counted lines use plural helpers (`arabicPlural` / `englishPlural`); no hard-coded text in components or hooks.
- ✔ All dialogs are titled and manage focus correctly (initial autofocus and `onCloseAutoFocus` returning focus to the trigger or heading, DI-30); each row's «⋯» menu is named by the visitor's name; touch targets meet or exceed 44px; amounts use `priceText` with `isolate()`; names have `dir="auto"` and `self-start`.

### 4.6 Tests (each must be able to fail)
- ✔ All planned tests 31–39 and 41 are present (detailed in table below).
- ✔ Test 38's final break [role] waits 200ms and fails if the query is enabled when `mayTypePrice` is false; if pricing stops working, PUT assertion, toast presence, and `onClose` callbacks fail.
- ✔ Tests 35, 37, and 39 will turn red upon regression: test 35 asserts reason validation, toast action presence, DELETE execution, and toast dismissal; test 37 asserts primary class, accessible name, axe cleanliness, and focus return; test 39 asserts Gaza midnight date difference.

### 4.7 Architecture, scope, documents
- ✔ `shared/` never imports from `features/` or `pages/`; `features/desk` imports only within its boundary or via barrels; `apps/api` and `packages/shared` have 0 changes; semantic design system tokens used.
- ✔ `desk.md`, `payments.md`, and `visits.md` accurately describe the implemented web features; history entries end with `2026-10-25, #117`; no `#PRNUM` markers remain in the repository.
- ✔ Findings 110, 112, 115, and 164 are accurately updated in `docs/architecture/findings/` and indexed in `README.md`.

### 4.8 The executor's departures
- Judged in "Departures judged" below.

## Tests table (4.6)

| # | Lane · file | Title / Requirement | Status |
|---|---|---|---|
| 31 | component · [`useUncollectedCard.component.test.tsx`](file:///C:/dev/masaha/app-design/apps/web/src/features/desk/hooks/uncollected/useUncollectedCard.component.test.tsx) | Counts visits from page meta, no money sum; three rows then all; open on `#uncollected` | Present |
| 32 | component · [`useUncollectedCard.component.test.tsx`](file:///C:/dev/masaha/app-design/apps/web/src/features/desk/hooks/uncollected/useUncollectedCard.component.test.tsx) | Owner sees «لن يُحصَّل…», reception does not | Present |
| 33 | component · [`useCollectDialog.component.test.tsx`](file:///C:/dev/masaha/app-design/apps/web/src/features/desk/hooks/collect/useCollectDialog.component.test.tsx) | Pays visit with key; remainder asks phone; `VISIT_WRITTEN_OFF` and `VISIT_NOT_PRICED` worded | Present |
| 34 | component · [`useDebtDialog.component.test.tsx`](file:///C:/dev/masaha/app-design/apps/web/src/features/desk/hooks/debt/useDebtDialog.component.test.tsx) | Leaves visit to phone with name; no key, never re-sent after no answer; `VISIT_HAS_CUSTOMER` worded | Present |
| 35 | component · [`useWriteOffDialog.component.test.tsx`](file:///C:/dev/masaha/app-design/apps/web/src/features/desk/hooks/write-off/useWriteOffDialog.component.test.tsx) | Requires reason; toast offers «تراجع», which undoes it once | Present |
| 36 | component · [`useWriteOffDialog.component.test.tsx`](file:///C:/dev/masaha/app-design/apps/web/src/features/desk/hooks/write-off/useWriteOffDialog.component.test.tsx) | Words write-off refused 403 for reception | Present |
| 37 | component · [`UncollectedCard.component.test.tsx`](file:///C:/dev/masaha/app-design/apps/web/src/features/desk/components/uncollected/UncollectedCard.component.test.tsx) | «تحصيل» is primary; row menus named by visit; focus returns after dialog; axe-clean at 390 | Present |
| 38 | component · [`useUnpricedCard.component.test.tsx`](file:///C:/dev/masaha/app-design/apps/web/src/features/desk/hooks/unpriced/useUnpricedCard.component.test.tsx) & [`usePriceDialog.component.test.tsx`](file:///C:/dev/masaha/app-design/apps/web/src/features/desk/hooks/unpriced/usePriceDialog.component.test.tsx) | Read only for whoever may type price; prices visit with reason; `VISIT_ALREADY_PRICED` worded | Present (split into two files per §9) |
| 39 | unit · [`dayWord.unit.test.ts`](file:///C:/dev/masaha/app-design/apps/web/src/features/desk/services/dayWord.unit.test.ts) | Today, yesterday, else date, on Gaza's calendar | Present |
| 41 | component · [`useWriteOffDialog.component.test.tsx`](file:///C:/dev/masaha/app-design/apps/web/src/features/desk/hooks/write-off/useWriteOffDialog.component.test.tsx) | Write-off or its undo with no answer is not re-sent by itself (no idempotency key) | Present |

## Departures judged (4.8)

1. **`uncollected.howManual` added for hand-closed rows:** **Accepted.** Under merged PR #114, uncollected visits include priced visits closed by hand with no customer whose payment was voided. Distinguishing «خروج تلقائي عند الإغلاق» from «خروج يدوي» satisfies DI-2 ("each row says how it closed").
2. **Reusing `errors.VISIT_WRITTEN_OFF` rather than adding duplicate in `desk.refusals`:** **Accepted.** PR #114 added the error to the shared error catalogue, and `useServerForm` automatically falls back to `errors[code]`.
3. **`DeskAbilities` holds `writeOff` only:** **Accepted.** Complies with the principle "no type nothing reads", deferring `archive` until PR 3.
4. **Hiding «⋯» on unpriced uncollected rows:** **Accepted.** The contract specifies that `POST .../write-off` on an unpriced visit is rejected with 409 `VISIT_NOT_PRICED`; an unpriced visit must be priced before it can be written off.
5. **Additional type and test fixture files (`UncollectedItem.ts`, `deskVisit.ts`):** **Accepted.** Appropriate modularization preventing duplication across components and tests.
6. **URL query parameter for uncollected pagination (`uncollectedPage`):** **Accepted in principle, but defect noted (see F1).** Adding URL state is standard for paged lists, but omitting `usePageInRange` causes an empty card without controls on stale pages.
7. **Reusing `occupancy.present.refreshFailed`:** **Accepted.** Avoids duplicate copy for background refresh failures.
8. **Writing finding 112 evidence line in PR 1b:** **Accepted.** Fulfills the deferred documentation commitment.
9. **PR size bound (48 files vs 45 prompt target):** **Accepted.** Explicitly requested and approved by repository owner ("Keep PR 1b at ~48").
10. **Break 38 test adjustment:** **Accepted.** Waiting 200ms allows asynchronous TanStack Query dispatch to be properly verified.
11. **No pagination on «بدون سعر»:** **Accepted.** §10 Commit 6 of the plan specified no pagination controls for `UnpricedCard`, treating it as a dynamic queue where items disappear as they are priced and subsequent items flow into page 1.
12. **Splitting test 38 into `useUnpricedCard` and `usePriceDialog`:** **Accepted.** Directly aligns with §9 structure.
13. **Adding `self-start` to visitor names in `UncollectedRow` and `UnpricedCard`:** **Accepted.** Fixes alignment stretching for RTL/LTR text mix.

## Not checked, and why
- **No local code execution / test commands:** Reviewer operates under strict read-only constraints (§1). CI checks passed green on head `a1193e77` for all 11 lanes.
- **No manual database mutations or dev server launches:** Verified data flows and network behaviors via static code analysis, contracts, and the executor's CDP logs and screenshots.
