# Review — PAYMENTS (#114, `feat/payments`)

- **Head:** `8ae243f07cfa06a6a7afc66bfbba176679e8be83`. Base `origin/main` at review start `5c0cdcba`.
- **CI:** `gh pr checks 114` was green on that head at the start: build, check:classes, check:conflicts,
  check:links, format:check, lint, test:api, test:component, test:unit, typecheck and CodeRabbit all passed.
  `mergeStateStatus` was `CLEAN`.
- **At the end:** the head **did not move** (`8ae243f0`). `mergeStateStatus` is now `UNKNOWN`: #115
  (`chore/demo-daily`, the demo seed) merged meanwhile (`origin/main` = `b2f13a47`). `git merge-tree
  --write-tree origin/main 8ae243f0` is clean (no conflicted paths). GitHub is still recomputing the state; it
  needs to show `CLEAN` again before the merge.
- **How I read it:** only from commit objects (`git diff origin/main...8ae243f0`, `git show 8ae243f0:<path>`).
  Nothing was run. Statements about runs, reds and breaks come from the executor's `4_REPORT.md` and are
  labelled that way.

**Verdict: mergeable.** I found no blocker and no should-fix. The four nits below are small. None needs a fix
round.

---

## Findings (most severe first)

### N1 — nit · reception's "403, never ignored" is not true for half a range or a malformed one
- **Where:** `docs/api/api-contract.md` › `GET …/payments` (*Who reads what* and *Errors*);
  `docs/backend/security.md` (the payments-list bullet); `docs/features/payments.md` (S6's decision and
  *Behaviour*). **Seen in the code:** `payments.manage.routes.ts` runs `validate(paymentsQuerySchema, 'query')`
  before the controller. The refusal `AppError.forbidden()` is in `payments.service.ts` `page()`, after
  validation.
- **Scenario:** reception sends `GET …/payments?from=2026-10-24`. The answer is **422** `{ to: ['required'] }`,
  not 403. The same happens for `?from=…&to=<before from>` (422 `out_of_range`) and for `?recordedById=0` (422).
  The documents say "a `from`, `to` or `recordedById` from it is `forbidden` (403), never ignored". That holds
  only for a query that passes validation.
- **Not a security problem:** a 422 still reads nothing, and it is not an ignored filter, so S6's intent holds.
  The documents are just imprecise.
- **Fix:** one clause in the contract: "the query is validated first (422); a valid range or `recordedById`
  from reception is then `forbidden`". Mirror it in security.md, or link to the contract from there.
- **Where the fix belongs:** worker B's next PR, first commit (DESK_API, through `0_CARRIED_FROM_114.md`).
  Documents only.

### N2 — nit · the two ranged lists count "92 days" differently (the executor's note)
- **Seen in the code:**
  - `packages/shared/src/payments/requests.ts:58`: `to > addDays(from, PAYMENTS_RANGE_MAX_DAYS - 1)` gives 92
    days with both ends counted.
  - `packages/shared/src/subscriptions/requests.ts:71`: `to > addDays(from, CHECK_IN_RANGE_MAX_DAYS)` gives 93
    days counted.
  - Both constants are `92`. Each list's documents describe its own rule correctly: the contract's check-ins
    list says "at most 92 days after it", and the payments list says "at most 92 days with both counted".
- **Which is right:** the payments list is. It is what the approved plan wrote (D2 and U1, "92 days, both
  included"), and a calendar quarter is at most 92 days. The check-ins list is not wrong by its own documents.
  It is looser by one day.
- **What breaks:** nothing a user meets. S5 justified the payments bound as "one bound for the desk's two ranged
  lists", and that is now false. The same constant name, `…_RANGE_MAX_DAYS = 92`, means two different spans.
  This is a trap for the screens (worker A) and for finance's later range.
- **Fix:** align the check-ins list to `CHECK_IN_RANGE_MAX_DAYS - 1` (its test, its contract line), or rename
  one constant. That changes a merged endpoint's behaviour, so the owner decides.
- **Where it belongs:** **a finding to record — 170.** Nothing changes in this PR.

### N3 — nit · a PR number inside a migration's comment
- **Seen in the code:** `apps/api/prisma/migrations/20261024133344_payment_void_guard/migration.sql:1` reads
  "(2026-10-24, #114)". It is the only migration in the tree carrying a PR number (`git grep "#[0-9][0-9]"`
  over `prisma/migrations`). The plan's D9 asked for it.
- **Consequence:** the `#PRNUM` rewrite changes the migration's checksum after it was applied locally. That
  forced departure 6 (a hand-set `_prisma_migrations` row on `masaha_b_test` and a reset of `masaha_b_dev`).
- **On the head it is harmless:** the file is final, the comment sits outside the function body, and CI's
  fresh database applied it (test:api green). **Do not edit the file now:** that would change its checksum
  again on every database that applied it.
- **Fix, for later plans:** keep `#PRNUM` out of migrations (date only, or no history line in SQL). This is a
  plan-template point for the supervisor; under the owner's rule a workflow-rule gap rides on the next worker
  item, as its own commit.
- **Where it belongs:** worker B's next PR (DESK_API) only if the owner wants it written down. No code.

### N4 — nit · cosmetics in `payments.repository.ts`
- **Line 291:** the `uncollectedPage` JSDoc line, "written off, not settled … and how many there are.", is
  well over the 100-column width. Prettier does not rewrap comments.
- **New constant not reused:** `ITEM_PAYMENT` (line 23) is new, but `paymentsOfSubscription` (line 269) and
  `paymentsOfVisits` (line 283) still spell out the same select inline. Those two lines predate this PR.
- **Fix:** rewrap the comment; use `ITEM_PAYMENT` in both selects.
- **Where it belongs:** DESK_API's first commit (it edits this file's neighbours anyway), or leave it.

---

## Departures (from `4_REPORT.md`), judged

1. **Tests written after their code; red got by holding back the route or the schema.** The red this gives
   proves only that the route or the export exists. It does not prove each guard, so the owner's "a red before
   its code is its own break" does not apply here. I checked that every guard still has a break that would turn
   it red:
   - The report lists B1–B24 (B16 replaced by B16b), plus B4 and BQ1, each red then restored. That is the
     executor's claim; I did not run them. Reading the code and the tests, each break would turn its test red.
   - The tests with no break of their own fall to an obvious one:
     - **T3:** without `validate(voidPaymentSchema)`, a blank or missing reason meets the payments CHECK
       (`num_nonnulls(...) IN (0, 3)`, a non-blank reason) and answers 500, not 422.
     - **T19:** covered at unit level by B3.
     - **T22:** covered at the route's schema by B1.
   - **Accepted** as a process departure. TDD's order was not followed, and the coverage is intact.
2. **D1's red through B4** (the old function restored on `masaha_b_test`). This is exactly "the code absent"
   for a migration that the lane's setup applies before any test. **Accepted.**
3. **An existing uncollected test's fixture gained a customer.** **Accepted; the change is right.**
   - **Seen in the code:** `desk.service.ts` `checkOutVisit` sets `leftUnpaid = charge === null || paid <
     charge` and then calls `customerFor`, which requires a phone when the visit has no customer.
   - So a manual, priced, customer-less, unpaid visit cannot be reached through the app. Under the approved D8
     it would be listed.
   - The test keeps its intent: a manual check-out's unpaid rest is a customer's debt, not listed.
4. **B16 → B16b.**
   - **Seen in the migrations:** `visits_checkout_method_check` (`checked_out_at IS NULL` = `checkout_method IS
     NULL`) and `visits_charge_check` (no charge on an open visit).
   - So, with Q1's clause in place, an open visit fails both arms of D8's predicate. `checked_out_at IS NOT
     NULL` alone cannot change the outcome.
   - B16b (that clause and Q1's dropped together) lists the open visit. **Accepted** under §12.5's exception.
     Keeping the redundant clause as a guard is fine.
5. **The payments service gains the clock.** `page()` needs "today". D10 omitted it, and conventions §11's one
   clock is passed in from `app.ts` (`now: clock`). **Accepted;** the plan's omission.
6. **`#PRNUM` replaced before the real run, the migration's comment included, and a hand-set checksum row.**
   - **Seen:** the head's file carries `#114`, and its function body is byte-identical to
     `20260929120300_payments`'s `payments_guard_change` plus D9's block (compared line by line).
   - CI applies the file fresh and test:api is green on the head. So **the head's migration is exactly what a
     fresh database applies.**
   - The hand-set `_prisma_migrations.checksum` on `masaha_b_test` is local metadata only, and correct because
     the comment lies outside the body.
   - **Accepted;** the root cause is N3.
7. **The shared `UncollectedVisit` comment** (`packages/shared/src/payments/responses.ts`). A comment that would
   otherwise be false after S1, in the same commit (C3). **Accepted.**
- **The executor's 92/93 note:** see N2. The payments list's 92 days, both ends counted, is right and as
  approved. A finding is owed (170). No change is owed in this PR.

---

## Checked and fine

**Authorization**
- `desk.manage.routes.ts`: `requireCan('payments.void')` runs before `validate(voidPaymentSchema)`.
  `desk.service.ts` `voidPayment` calls `lockAtDesk(…, 'payments.void')`, which takes the space's lock and then
  runs `can()` on `linksUnder(tx)`.
- The list's `can('payments.read')` runs before any query. Reception's filter is forced to `recordedById:
  actor.id` and today's window. The query's `from`/`to` are never passed to the window for reception.
- Another space's payment: `lockIn`'s `space_id` filter answers 404. The list's `spaceId` filter is in every
  statement (page, count, both totals) and in each naming query.
- The boundary returns 404 for a stranger, another space's owner and the admin. `can.ts`: `payments.read` and
  `payments.void` are `'owner'`.

**The void (D6)**
- The order is: space lock, then the payment's row `FOR UPDATE`, then (inside the trigger) the visit `FOR
  SHARE`.
- A second void returns the row as it is through `rowsOf`, with no write and no audit. A second owner waits on
  the space's lock; the row lock alone is proven by T12.
- No deadlock cycle: every money writer takes the space's row first.
  - Payment insert: space, then visit `FOR UPDATE`.
  - Write-off and undo: space, then visit.
  - Price correction (`subscriptions.service.ts:115`): space, then subscription.
  - The auto check-out touches only open visits, which never carry payments.
- `PERFORM … FOR SHARE` raises `payments_visit_written_off`, which `constraintCodes.ts:14` maps to 409
  `VISIT_WRITTEN_OFF`.

**Downstream (D5)**
- Every money read already filters `voided_at IS NULL` / `voidedAt: null`:
  - `balancesOf`, both branches (repository lines 125 and 133);
  - `paidFor` (line 182);
  - the uncollected query;
  - the insert ceiling (the payments, `desk_visit_charge` and `visit_write_off` migrations);
  - `subscriptions_price_below_paid` (`subscription_terms` line 47).
- The void writes one row (`update where id`). T10 compares every payment, visit and subscription row.

**The uncollected widening (D8 + Q1)**
- The predicate matches the owner's correction exactly: AUTO, or customer-less and priced. Unpriced manual
  visits and open visits stay out (test plus constraints).
- `leaveToCustomer` and `writeOffVisit` carry no AUTO-only condition, so the uncollected list's actions work on
  such a visit.
- It is the only reader of "uncollected" in the API.

**The list (D2–D4)**
- `paymentsWindow` runs from `gazaInstant(from, 0)` to `gazaInstant(addDays(to, 1), 0)` with `lt`. Today comes
  from `gazaClockOf(now)`, and the unit test pins the 23:30 UTC case.
- Order is `receivedAt desc, id desc`. Paging uses `toSkip` and `limit` ≤ 50.
- `totals` uses `paymentsWhere(filter)` with no void filter: received by method on `voidedAt: null`, voided
  apart. Each row carries names only, no phone (`DeskVisit.customer`'s phone is dropped).
- Seven statements a request, bounded by the page.
- A void later takes a payment out of its received day's totals (ADR 0010 rule 5, cash basis). This matches
  "a voided payment counts nowhere".
- `customers.namesOf` and `users.findNames` do not filter archived or suspended rows, so an archived customer's
  subscription or a departed receptionist never makes a row's name throw.

**The migration**
- `CREATE OR REPLACE FUNCTION` only; the trigger and the schema are untouched. `payments_guard_change` has no
  other definition.

**Carried from #112**
- `start()` runs `periodErrors({ startsAt: at, endsAt: current.endsAt }, at, 'edit', { startsAt: true, endsAt:
  false })` and returns 422, writing nothing. Its test, `lifecycle.api.test.ts`, checks the row and the audit.
- The documents follow `0_CARRIED_FROM_112.md` items 1–3, 5 and 6:
  - item 1: conventions §9's bullet moved below the customers list's sub-bullets;
  - item 2: `announcements.md`'s public read, `directory` in *Who uses it*, and the history line;
  - item 3: "will read" in the contract;
  - item 5: the retry-after-delete line;
  - item 6: `#112` last in `desk.md` and `subscriptions.md`.

**The documents**
- These read true to the code: the contract (the void, `PaymentRow`, the list, `PaymentTotals`, the uncollected
  sentence, the retry lines, `VISIT_WRITTEN_OFF` in §6), data-model, conventions §9 and §13, security,
  `payments.md`, `desk.md`, the *Who uses it* lines in `subscriptions.md`, `customers.md`, `users.md` and
  `visits.md`, v1-mvp, the overview's *Payments* line and the `docs/README.md` map line.
- S1's wording follows Q1's correction. `#114` is in place, with no `#PRNUM` left.
- One home per fact: the 92-day rule is stated in the contract and as a decision in `payments.md`, as for the
  check-ins list.

**Scope and commits**
- Scope: `apps/api`, `packages/shared`, `docs`, and in `apps/web` only the two `VISIT_WRITTEN_OFF` lines (the
  Arabic as approved). No dependency, no seed.
- Six commits, subjects of 48, 42, 45, 30, 47 and 39 characters, each with a body and no attribution. They are
  atomic by plan (C0a–C4).
- 39 files.
