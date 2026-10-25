# Review — SUBSCRIPTIONS PR 2 (#106, `feat/subscriptions`)

**Head:** `d0acc06b4c3de7fdd5d800705fdfa14bc5d377bc` · `mergeStateStatus: CLEAN` · `gh pr checks 106`: every
lane green (build, check:classes, check:links, format:check, lint, test:api, test:component, test:unit,
typecheck, CodeRabbit). The head had not moved when the review ended. Base `origin/main`; 9 commits, 74 files.
Read only from commit objects (`git diff origin/main...d0acc06b`, `git show d0acc06b:<file>`); nothing run.

**Verdict:** no blocker and no fix round needed. The money, locks, keys and authorization hold as the plan
says. Two small should-fixes and the nits below go to PR 3's first commit (`0_CARRIED_FROM_106.md`); two
are findings to record.

## The five most important findings

### 1. A subscribe retry answers another customer's subscription — should-fix → PR 3's first commit
`apps/api/src/modules/desk/desk.service.ts:633-637`. `subscribe` looks up the key first
(`subscriptions.findByKey(space.id, key)`) and returns what it finds without comparing it with the path's
`customerId`. *Scenario:* a desk subscribes Sara with key K, then sends K again on
`POST …/customers/<Omar>/subscriptions` (a client that reuses a key across actions, or a retry the web sends
from the wrong screen). It gets 201 with Sara's subscription, her money and her debt, under Omar's URL.
Nothing is written, and the key is space-scoped, so nothing leaks outside the space. Still, the desk is told
Omar is subscribed when he is not. The payment route already handles the same case: a key that paid another
item is 409 (`desk.service.ts:319`, `:416`, `:516`). *Fix:* `if (made && made.customerId !== customerId)
throw AppError.conflict(undefined, 'This idempotency key made another subscription')`, plus one test and
one line in the contract's errors.

### 2. `subscriptions.md` still says the module has no route — should-fix (documents) → PR 3's first commit
`docs/features/subscriptions.md:4` (the *Authority* line at the head): "its endpoints, once it has its own,
by the API contract. The API's reads are built; no route of its own and no web screen yet." This PR gives
the module its own manage router: `PATCH …/subscriptions/:id`, `PUT …/price` and `POST …/end`
(`subscriptions.manage.routes.ts`). The document's own *How it composes the platform* now says so, so the
file contradicts itself. That breaks "claim only what is true". *Fix:* "its endpoints by the API contract
([Subscriptions (managed)](…#subscriptions-managed)). The API is built (the corrections and the end its own
routes; the subscribe and the statement the desk's); no web screen yet."

### 3. The exact phone match dropped the suffix fallback — nit (plausible) → PR 3's first commit
`apps/api/src/modules/customers/customerSearch.ts:16-17` with `customers.repository.ts` (`phone = …`).
When `normalisePhone(q)` reads a number, the search matches only `phone = <E.164>` and no longer tries the
suffix. `normalisePhone` keeps an explicit country code for a non-Palestinian mobile (`core/phone.ts`:
`given ?? (mobile ? '972' : '970')`). So a customer stored as `+970521234567`, typed with `+970`, is no
longer found by `0521234567`: that input now normalises to `+972521234567`. Before this PR, the suffix
`0521234567` matched the digits `970521234567`. The same holds for a landline stored under `+972`. This is
rare, but it is a regression for the carried item's own goal ("found in any form"). *Fix:* when a whole
number is read, match `phone = $1 OR <digits> LIKE '%' || <its national digits with the trunk 0>`. Or,
simpler, keep the suffix condition beside the exact one. Add one U3 case and one T22 case.

### 4. The statement's sums and its listed payments come from different snapshots — nit / finding to record
`apps/api/src/modules/desk/desk.service.ts:858-868`. `statement` runs `withMoney` (paid and balance, through
`itemBalances`), `paymentsOfSubscription`, `checkInsOf` and `renewedBy` as separate queries on the pool
(`Promise.all`, no transaction). A payment or a check-out that commits between them gives a statement whose
`paidAgorot` is not the sum of the non-voided `payments` it lists, or whose `progress.minutesUsed` is not
the sum of its `checkIns[].minutes`. To an accountant, that reads as a broken statement. The window is
milliseconds and a reload fixes it. The customer file (#102) has the same shape, also "read without a lock".
*Fix (either):* read the statement in one `REPEATABLE READ` transaction (the reads already accept a `tx`),
or record a finding naming both reads. My recommendation is a finding now, decided with the statement's
screen item.

### 5. The allocation's order cannot be previewed by the client — finding to record (plausible)
`payments.repository.ts:211-213` orders a customer's items by `created_at, kind <> 'VISIT', id`, and
`allocate` follows that order. No answer exposes the key it sorts on: `SubscriptionState` carries no
`createdAt`. The file lists subscriptions "the latest started first" and unpaid visits by their own order.
So the desk's renewal sheet cannot show which debts an amount will settle before it is sent; it learns
only after, from `NewSubscription.payments`. Example: a renewal made today that starts next month sorts
after a visit from yesterday, but its `startsOn` suggests the opposite. This is not wrong today (the server
decides, D7), but the subscriber-desk screen item will want a preview. *Record:* the allocation order is not
exposed, and the screen either shows the result only or the API adds `createdAt` (or a quote).

## The rest

6. **`CUSTOMER_HAS_DEBT` on a retry counts items newer than the subscription** — nit → PR 3.
   `desk.service.ts:242-245` warns on any other item with a balance above zero, not only older ones. On a
   first request every other item is older, so this is correct there. On a later retry (S7: "as of now"),
   a renewal of this subscription made since, still unpaid, raises "still owes on an *earlier* item". The
   contract says "an item older than the new subscription". *Fix:* compare the item's `createdAt` (in
   `ItemBalance`) with the subscription's, or keep only the items before it in `itemBalances`' order.

7. **The statement counts minutes a second time, in TypeScript** — nit → PR 3 or record.
   `desk.service.ts:878-880` computes `Math.floor((out − in) / 60000)`. `subscription_usage` computes the
   same with `floor(extract(epoch …)/60)` (`20261021082345_subscription_usage/migration.sql:27`). They agree
   today (both whole minutes, timestamps in ms), but S1 promised "one function … so no second copy exists".
   *Fix:* answer each check-in's minutes from SQL (`checkInsOf` selecting the same expression), or state the
   exception in `subscriptions.md`.

8. **Past the 49th debt, the rest becomes credit while older debts stay unpaid** — nit / record.
   `allocation.ts:22` slices the debts to 49 and gives the whole rest to the new subscription. If the new
   one is usage-based, an amount larger than the first 49 balances becomes credit on it while debts 50 and
   on stay owed, against "oldest first". If it is fixed, the request is refused `PAYMENT_EXCEEDS_DUE` with
   no hint why. The cap is planned and unit-tested (U2), and 50 debts on one customer is far-fetched, so
   recording it in `payments.md`'s decision ("the rest beyond the 49th is the new subscription's") is
   enough.

9. **The contract dates the owner's decision on the archived file 2026-10-22** — nit → PR 3.
   `api-contract.md`, *Customers (managed)* (`GET …/customers/:customerId`): "the owner's decision,
   2026-10-22, #106". `0_CARRIED_FROM_102.md` records it as "Decided by the owner (2026-10-21)". If the
   date names the decision rather than the PR, it should be 2026-10-21.

10. **The PR description's checklist says every test was seen failing** — nit (description only, fix in place).
    "Tests added in the owning lanes, each seen failing" is checked, while the *Evidence* lists three seen
    green only (T25, the corrections' not-found, T31). Reword the item: "each seen failing, but three,
    named in Evidence".

## The executor's departures, judged

- **The renewal's unique key on `(renewal_of_id, customer_id)`: sound, still one renewal.** I saw it in
  the migration: the foreign key `subscriptions_renewal_of_id_customer_id_fkey (renewal_of_id,
  customer_id) → subscriptions (id, customer_id)` makes every renewal of S carry S's customer, so two
  renewals of S share the pair and the unique index refuses the second. `customer_id` is `NOT NULL`, so
  `MATCH SIMPLE` never skips the check while `renewal_of_id` is set. `ON UPDATE CASCADE` can only move both
  renewals together, and no code updates a subscription's customer. D3 asserts P2002 and P2003
  (`db/subscriptions.api.test.ts`). The service checks first under the lock (`desk.service.ts:644-651`),
  and the race test T22 inserts the rival renewal while the request waits.
- **No "checked by the service" line:** acceptable. The database enforces it and the service also checks
  (`:646`), so the line would have been true; leaving it out drops nothing.
- **A usage-based subscription's payment answers a balance below zero:** acceptable and documented (the
  contract's `ReceivedPayment` comment, `desk/responses.ts`). It matches the file's rows and
  `NewSubscription.subscription`. The visit branch keeps `?? 0`, where a balance below zero cannot occur.
- **`custom.endsOn` / `custom.shiftId`:** correct. Field errors are keyed by the dotted request path
  (`packages/shared/src/core/fieldErrors.ts`, `path.map(String).join('.')`), and the contract names both.
- **Tests seen green only before their code:** T25 and the corrections' not-found test would turn red
  without the space scope (`lockIn … AND s.space_id`, `statesOf(space.id, …)` through
  `subscription_usage(spaceId, …)`): the guard is real, only its red was not seen. T31 exercises the
  pre-existing insert trigger, and its proof is B38 (I read it in the report, I did not run it).
- **Breaks, lanes, the real run, the migration on both B databases and the EXPLAIN numbers:** read in
  `4_REPORT_PR2.md` only. I did not run them. On the index, I saw in the code that `balancesOf`'s visits
  branch carries `v.customer_id IS NOT NULL AND v.checked_out_at IS NOT NULL` literally
  (`payments.repository.ts:93`), so the partial index's predicate is provable by the planner. That is
  consistent with the reported `Index Scan using visits_customer_id_closed_idx`.

## Where each fix belongs

- **Fix round on this PR:** none.
- **PR 3's first commit, through `0_CARRIED_FROM_106.md`:** 1 (the retry's customer, with its test), 2
  (`subscriptions.md`), 3 (the suffix fallback, with U3/T22 cases), 6 (the warning's "older"), 9 (the date),
  and 7 if the owner wants the minutes from SQL.
- **Findings to record:** 4 (the statement's snapshots, with the file's), 5 (the allocation order not
  exposed, for the subscriber-desk screen), 8 (the 49-debt rest), unless the owner prefers 8 as a
  `payments.md` decision line.
- **In place, now:** 10 (the PR description's checklist line).

## Checked and fine

- **Money in integers:** amounts are `int` agorot everywhere (`paymentSchema`, `correctPriceSchema` 1 to
  `PRICE_MAX_AGOROT`, the custom terms' `createPackageSchema` bounds). `allocate` only takes `min` and
  subtracts integers, and skips parts of zero.
- **`PAYMENT_EXCEEDS_DUE`** is the insert trigger's for a fixed subscription (`FOR UPDATE` on its row). A
  subscribe's rest above a fixed new price rolls back the whole transaction (T17, B27). A subscription's
  payment route reaches the same trigger (T11, B22).
- **S2:** `subscriptions_guard_price`, `BEFORE UPDATE OF billing, price_agorot`, sums the non-voided
  payments and covers `PER_HOUR → FIXED` (D4). `correctPrice` is the only path that changes a price, and
  `PATCH` cannot. The trigger's row lock serialises against the insert trigger's `FOR UPDATE`, and both
  service paths hold the space's lock first. `PRICE_BELOW_PAID` is translated (`constraintCodes.ts`, T30,
  B37).
- **Oldest first:** one order (`itemBalances`: `created_at`, visit first, id) serves the allocation; the
  new subscription is excluded by id. Debts are read under the space's lock after `lockAtDesk` (T21, B29).
  Voided payments are excluded in `balancesOf`, both triggers and the statement's paid.
- **Locks:** subscribe, pay, correct, price and end each take the space's lock, then `can()` on
  `linksUnder(tx)`, then the subscription's row `FOR UPDATE`, then the items through the trigger. That is
  the same order everywhere, and the auto check-out touches only open stays, never an allocation item.
- **Keys:** subscriptions carry `request_id` (required, backfilled, unique per space; D5). The retry is
  read first under the lock (T6, B18/B19). A renewal's or subscribe's payments use
  `derivedKey(key, index)`, a valid UUID v8 per `idempotencyKeySchema` (U3), and are found again in one
  query, in key order (T18, B28). S7's "as of now" is stated in the contract.
- **Authorization:** the subscribe uses `requireCan('subscriptions.manage')` before the key and the body.
  The price uses `requireCan('subscriptions.correctPrice')` (owner-only in `can.ts`, U6) before `validate`,
  and T29 sends reception an invalid body and gets 403. `PATCH` and end are the staff's, as D1 says. Every
  id is scoped to the space: the customer (`findIn`), the package (`termsOf` → `findIn(spaceId, …)`),
  `renewalOfId` and `subscriptionId` (`lockIn … AND s.space_id`), a custom shift (the composite foreign key
  → `invalid_choice`), and the statement (`statesOf(space.id, …)`, `checkInsOf`/`paymentsOfSubscription`
  by `spaceId`). Strangers and the admin get 404 at the boundary (T7, T25, T34, the corrections' test).
- **End (D10):** `max(today, startsOn)`, then never later than `endsOn`, with who and when. A repeat
  answers as it is. No money changes. `EXPIRED` from then (T32–T33, B39–B41).
- **Corrections (D8, A3):** only the fields that changed (`subscriptionChange`, U4, B5), the name included
  (B-name). An end before the start is `out_of_range`. An ended subscription is `SUBSCRIPTION_ENDED`. A
  no-op writes nothing.
- **Carried items:** 1 `normalisePhone` plus the separators `[\s+\-.()]` (but see 3). 2 `occupancy.md`,
  ADR 0015's *Revised*, `payments.md`. 3 the contract's archived-file line. 4 the error's comment says
  "edited". 5 findings 121–123 with index lines. 6 the index (above).
- **Migration:** one new directory. Nothing dropped but the two price checks it replaces (`> 0`, finding 80
  resolved and moved in the index). The backfill comes before `SET NOT NULL`. The reason check is as D9.
- **Documents:** the contract (routes, bodies, errors in order, the four codes in §6 with glosses, §4's
  exception), data model *Constraints* and *Hand-typed prices*, ADR 0009's two rows and *Revised*, ADR
  0015's *Revised*, conventions §9/§13, security, `desk.md`, `customers.md`, `payments.md`, `packages.md`,
  v1-mvp, overview. All true to the code (but 2 and 9), with `#106` in place of `#PRNUM`.
- **Scope and commits:** only `apps/api`, `packages/shared`, `docs` and the two web catalogues (four lines
  each, the Arabic as Q2 approved). Subjects are 32–49 characters, the bodies say why, and there is no tool
  attribution in commits or the PR.
