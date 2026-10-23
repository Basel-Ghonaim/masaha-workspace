# SUBSCRIPTIONS PR 2 (`feat/subscriptions`) — phase 1's report (Claude Code)

Written as the work goes. Phase 1 builds; phase 2 runs the lanes, the real run, the PR number, the push and CI.

## Preconditions and 12.1 (2026-10-22)
- `gh pr view 102 --json state` → `MERGED 43b34cd3…`; `gh pr list --state merged --head chore/directory-demo-set` →
  `104 5a0cda1a…`. `origin/main` = `5a0cda1a`. No open PR.
- `git diff --name-status a86645f5 origin/main` (PR 1's head after its fix round → main): #103 (directory filters,
  `apps/web` and docs) and #104 (DEMO_SEED). Code files this PR names: only `apps/api/src/db/seed/demo.ts`, whose one
  change is `gazaClock` exported (used by `demoDirectory.ts`) — nothing the plan's seed edit depends on.
  `demoDirectory.ts` seeds spaces' price lists, no package and no subscription: the migration's backfill and finding
  80's `> 0` touch none of its rows. `run.ts` also seeds the directory set; not this PR's file.
- Findings on main: 120 (PR 1), 130 and 132 (worker A). 121–123 free, as the carried file numbers them.
- `git switch --no-track -c feat/subscriptions origin/main`; `docker start masaha-postgres-1`; `apps/api/.env` names
  `masaha_b_dev`, `masaha_b_test` and `PORT=3321` (counted by pattern, not printed); `npm run build -w @masaha/shared`
  exit 0; `prisma migrate status` → 23 migrations, up to date.

## Carried from #102

### Item 1 — the phone search in any form — `0529fef0` `fix(customers): find a phone in any form` (40)
- **Tests first:** U3 (`customerSearch.unit.test.ts`) gains a whole-number case (`0599000205`, `0521234567`,
  `00970599000205`, `059-900-0205`, `+972 52 123 4567` → `{ phone: E.164 }`) and separators in the suffix case
  (`059-900`, `(059) 9.00` → `059900`); T22 (`desk/customers.api.test.ts`) gains a `+972` customer and `?q=0521234567`,
  `?q=00970599000205`, `?q=059-900-0777`, `?q=02-05`.
- **Red:** unit `Tests  2 failed | 1 passed (3)` — `expected { phoneDigits: '0599000205' } to deeply equal { phone:
  '+970599000205' }`, `expected { name: '059-900' } to deeply equal { phoneDigits: '059900' }`; api (`-t "q finds"`)
  `Tests  1 failed | 5 skipped (6)` — `expected [] to deeply equal [ 'Dana' ]`.
- **Code:** `searchTermsOf` answers `{ phone }` when `normalisePhone(q)` reads a number (matched `phone = $1`);
  else drops `[\s+\-.()]` (the phone field's separators and `+`) before the digits test. The repository's page
  comment rewrapped within 100 columns (review 9's cosmetic point; the file was touched).
- **Green:** unit `Tests  3 passed (3)`; api `desk/customers.api.test.ts` `Tests  6 passed (6)`.
- Documents: contract (`q`), `customers.md` (two lines, a history line `#PRNUM`). `lint` exit 0, `typecheck` exit 0.

### Items 2–5 — the documents, the comment, findings 121–123 — `bb221048` `docs(customers): say what the customers' PR built` (49)
- **Item 2:** `occupancy.md` — only `announcements` lacks a capability document; `subscriptions` and `customers` linked.
  `payments.md` — the uncollected visits' decision head says what is built (paged by the ledger in one SQL query), the
  first form kept as its history. **ADR 0015's *Revised* line lands in C2 as planned** (customers since #102,
  subscriptions since this PR) — said in the PR's description.
- **Item 3:** the contract's `GET …/customers/:customerId` gains "an archived customer's file is answered to the owner
  and reception alike: their debts are still collected at the desk (the owner's decision, 2026-10-22, #PRNUM)".
- **Item 4:** `CUSTOMER_ARCHIVED`'s comment in `packages/shared/src/core/errors.ts` says "edited no more".
- **Item 5:** findings **121** (the auto check-out stalling behind stays that always fail — the three fixes the review
  lists), **122** (`subscription_usage` overflowing `integer`), **123** (a delayed edit retry; the customers' screen
  item, screens 14 and 15, with finding 115) — files and index lines (Open).
- `lint` exit 0, `typecheck` exit 0 (on this commit).

### Item 6 — the visits' index (in C1's migration)
- **Measured** (`scripts\i6-explain.sql` → `i6-explain.out`; one transaction on `masaha_b_test`, rolled back): PR 1's
  scale seed (2,000 customers each with a fixed subscription paid in part, 30,000 walk-in visits) **plus 10,000
  closed visits by the customers (5 each), each paid in part**; `EXPLAIN (ANALYZE, BUFFERS)` of the two reads that
  ask for customers, exactly as `balancesOf` builds them; then the index created, `ANALYZE visits`, the same again.

  | Query | Before | After |
  |---|---|---|
  | `customerBalances` (a page of 20) | 10.97 ms — `Seq Scan on visits v` (10,000 rows kept, **32,000 removed by filter**), then a hash semi-join on the 20 ids | **2.08 ms** — `Index Scan using visits_customer_id_closed_idx` (5 rows × 20 loops) |
  | `itemBalances` (one customer) | 9.69 ms — the same seq scan, 32,000 removed | **0.72 ms** — the index, 5 rows |

- **The index:** `visits_customer_id_closed_idx ON visits (customer_id) WHERE customer_id IS NOT NULL AND
  checked_out_at IS NOT NULL` (Prisma `@@index([customerId], map: …, where: …)`, the `partialIndexes` feature). *Why
  these columns:* the branch asks for given customers' closed visits; a customer belongs to one space (the foreign key
  through `(customer_id, space_id)`), so `space_id` adds nothing; walk-ins (most visits) and open visits (already
  indexed by `visits_customer_id_key`) are left out, so the index grows with customers' closed visits only.
  `written_off_at` stays a filter (a write-off is undone at times; the index does not churn). `customerIdsByPayment`
  (the whole space) is unchanged by it, as expected.

## PR 2 — C1 `feat(db): store a subscription's key and reason`

### §12.2 check 1 — migration `subscription_terms`, created once
- `prisma migrate dev --create-only --name subscription_terms` **once** → refused, nothing created: `Error: Prisma
  Migrate has detected that the environment is non-interactive, which is not supported.` (it also listed the data-loss
  step: "Added the required column `request_id` … There are 4 rows in this table"). `ls` unchanged.
- **The fallback, as PR 1:** `prisma migrate diff --from-config-datasource --to-schema prisma/schema.prisma --script`
  (read-only; `masaha_b_dev` up to date) into a hand-made `20261022071444_subscription_terms/migration.sql` (UTC).
  (`--from-migrations` was tried first and refused for want of a shadow database; nothing written by it.) Then edited
  as check 1 says: `ADD COLUMN "request_id" UUID;`, D9's backfill and `SET NOT NULL` before the unique index; Prisma's
  columns, unique indexes and foreign key kept; D9's raw SQL appended under a raw-SQL header; item 6's index is
  Prisma's own (from the schema).
- `npm run db:migrate` → `Your database is now in sync with your schema.` (`masaha_b_dev`); `prisma generate` →
  `✔ Generated Prisma Client (7.10.0)`; `models/Subscription.ts` names `idempotencyKey`, `priceReason`, `renewalOfId`;
  `prisma migrate status` → `Database schema is up to date!`. `masaha_b_test`: migrated by the API lane's global setup
  (the D-tests ran green on the new columns, and the break script's schema fingerprint of `masaha_b_test` equals
  `masaha_b_dev`'s).

### §12.2 check 2 — the self-relation — **departure, stated**
- `prisma validate` refused the relation as D9 wrote it (`renewalOfId Int? @unique` + the relation through
  `[renewalOfId, customerId]`): `A one-to-one relation must use unique fields on the defining side. Either add an
  @@unique([renewalOfId, customerId]) attribute to the model, or change the relation to one-to-many.`
- **Built:** the relation through `(renewalOfId, customerId)` exactly as planned, with `@@unique([renewalOfId,
  customerId])` **in place of** `@unique` on `renewalOfId` → `The schema … is valid`. *Why not check 2's fallback*
  (the relation on `renewalOfId → id` alone, the customer checked by the service): it would drop a database guarantee
  the plan wants, while this keeps both. *Why it is the same rule:* the foreign key makes a renewal's customer the
  renewed one's, so two renewals of one subscription always share the pair: the pair is unique exactly when
  `renewal_of_id` is. D3 proves both halves (a second renewal → P2002; another customer's → P2003). One index, named
  `subscriptions_renewal_of_id_customer_id_key` (B10 drops it).

### §12.2 check 5 — the seed
- `npm run db:seed` twice on `masaha_b_dev` (`SEED_DEMO=true` present by pattern) → both exit 0, `The demo space
  exists; left unchanged.` (its two typed prices were backfilled by the migration's English reason; a fresh seed now
  writes its own Arabic reasons and the four keys). `src/db` (with `seed/demo.api.test.ts` "changes nothing when run
  again") → `Test Files  8 passed (8)`, `Tests  105 passed (105)`.

### C1 committed — `de6904e8` (now `90db34b6`, after the fold below) `feat(db): store a subscription's key and reason` (47)
- **Tests first** (D1–D5): `db/subscriptions.api.test.ts` — "carries a typed price's reason with who typed it, never
  blank" (D1), "costs more than nothing, as a package does (finding 80)" (D2), "is renewed once, by one of the same
  customer's subscriptions" (D3), "never shares its key with another subscription of the space" (D5); scenario 3 gains
  its reason; `db/payments.api.test.ts` — "a fixed price never falls below what is paid:
  subscriptions_price_below_paid; usage-based may" (D4, with a voided payment and a `PER_HOUR → FIXED` change).
- **Red:** `Tests  6 failed | 29 passed (35)` — `Unknown argument idempotencyKey` / `priceReason` / `renewalOfId`
  (`PrismaClientValidationError`), and `promise resolved … instead of rejecting` (zero prices; the price lowered).
- **Green:** `Test Files  2 passed (2)`, `Tests  35 passed (35)`.
- The factory's `createSubscription` and the demo seed's four subscriptions gain a key; the two typed ones a reason.
- Documents: data model *Constraints* (keys, the renewal, prices above zero, the reason's check, the price trigger);
  finding 80 Resolved + index moved; `packages.md` (the decision's tail, the open-findings line, a history line).
- `lint` exit 0 · `typecheck` exit 0 · Prettier clean on the touched files.

### C1's breaks (database, `masaha_b_test`; `scripts\dbbrk2.py` + `c1-breaks.json`, output `c1-breaks.out`)
| Break | Edit | Red | Restored |
|---|---|---|---|
| B8 | drop `subscriptions_price_reason_check` | D1 `promise resolved "{ id: 1, … }" instead of rejecting` | green, `1 passed` |
| B9 | both price checks back to `>= 0` | D2 `promise resolved … instead of rejecting` | green |
| B10 | drop `subscriptions_renewal_of_id_customer_id_key` | D3 `promise resolved "{ id: 3, … }" instead of rejecting` | green |
| B11 | drop the trigger `subscriptions_guard_price` | D4 `promise resolved … instead of rejecting` | green |
| B12 | drop `subscriptions_space_id_request_id_key` | D5 `promise resolved "{ id: 2, … }" instead of rejecting` | green |
- **A defect of my script, fixed:** the first run crashed printing (Windows console encoding) after each break and
  before its restore; then B8's and B9's restores were refused by the rows the broken test had left (`check constraint
  … is violated by some row`). Each was restored by hand after `TRUNCATE subscriptions CASCADE` on `masaha_b_test`
  (the lane resets it before every test anyway); the script now truncates before a restore. **After all five: the
  schema fingerprint (constraints, indexes, triggers, the two functions' source) of `masaha_b_test` equals
  `masaha_b_dev`'s** — `test == dev: True`.

### C1, a fix folded in (found while running C2's neighbours)
- Running the modules C2 touches showed two C1 consequences I had missed by running only `src/db` at C1: the 1,000-row
  test in `desk/customers.api.test.ts` inserts subscriptions by raw SQL without the now-required `request_id`
  (`null value in column "request_id" … violates not-null constraint`), and T17 of `payments/balances.api.test.ts`
  lowered a fixed price under what was paid directly ("the price's guard is the next PR's") — now refused by the
  trigger (`subscriptions_price_below_paid: 30000 agorot paid exceeds the price 20000`).
- **Fixed in C1** (`--fixup` + autosquash): the raw insert gains `gen_random_uuid()`; T17 now expects the lowering
  refused (`subscriptions_price_below_paid`) and the customer still settled. **Consequence, stated:** PR 1's B33 (the
  `usage_based` filter on credit dropped) can no longer be made red by any data — the database now forbids a fixed
  subscription paid above its price — so the filter is defence in depth behind S2's trigger.
- Then `git rebase -x` (lint + typecheck per commit). **First attempt failed at `0529fef0` — the environment, not the
  commit:** the git-ignored Prisma client was generated from the newer schema, so the seed and the factory at that
  commit lacked the now-required key (`TS2322` in `demo.ts`, `factories.ts`). Aborted (`git rebase --abort`, back to
  `14a49e3a`), re-run with `prisma generate` and `npm run build -w @masaha/shared` inside each step → `PASS-0529fef0`,
  `PASS-bb221048`, `PASS-90db34b6`, `PASS-14a49e3a`. C1 is now **`90db34b6`**.

## C2 committed — `14a49e3a` `feat(desk): subscribe a customer` (32)
- **A document read beyond the prompt's list, said:** the plan's D2 (the shared shapes, lines 279–338): C2 needs
  `subscribeSchema`, `NewSubscription` and `DeskSubscription`'s `renewalOfId` and `priceTyped`, which only D2 gives.
- **Tests first.** U5 (`packages/shared/src/desk/requests.unit.test.ts`): "subscribe takes exactly one of a package and
  custom terms", "a custom price needs a reason; the terms take a package's bounds and an optional end" — red `Tests  2
  failed | 5 passed (7)`, `TypeError: Cannot read properties of undefined (reading 'parse')`. T1–T9
  (`desk/subscribe.api.test.ts`, 9 tests) — red `Tests  9 failed (9)`, `expected 404 to be 201` (no route).
- **Green:** U5 `Tests  7 passed (7)`; T1–T9 `Tests  9 passed (9)` (after one defect of my test: `not_found` is the
  error's `type`, not its `code`). The customer file's exact answer gains `renewalOfId: null` and `priceTyped: null`
  (its test updated by hand, nothing else); `desk` + `customers` + `subscriptions` + `payments` + `packages` +
  `occupancy` API files run once → the two C1 consequences above, then `Test Files  4 passed (4)` on the four files
  involved.
- **Built:** `subscribeSchema` (a package's terms without the validity, `endsOn?` and the reason, 1–200; exactly one of
  `packageId` and `custom` → `invalid_choice` on `packageId`); `DeskSubscription` gains `renewalOfId` and `priceTyped`;
  `NewSubscription` (`payments: []` until C4); `packages.termsOf`; `subscriptions.findByKey` / `create` (audited
  `subscription.created`; a foreign shift → `refused`, answered `invalid_choice` on `custom.shiftId`); `desk.subscribe`
  (D7 steps 1–3, 5–7); `POST …/customers/:customerId/subscriptions` (`requireCan('subscriptions.manage')` → key →
  `validate`).
- **Small choices, stated:** the out-of-range end and a foreign shift are reported on `custom.endsOn` /
  `custom.shiftId` (their request paths; a package's end is computed and cannot be out of range). T3 gains the foreign
  shift case (the branch would otherwise be untested).
- Documents: contract (§1's key list, `SubscriptionState`'s two fields, a new *Subscriptions (managed)* with the
  subscribe), ADR 0015 *Revised* (rule 4 done: customers since #102, subscriptions since #PRNUM), conventions §13,
  security (the boundary's `requireCan` list), `subscriptions.md`, `desk.md`, `packages.md`.
- `lint` exit 0 · `typecheck` exit 0 · Prettier clean.

### C2's breaks (`scripts\brk.py` + `c2.json`, output `c2-breaks.out`) — each red, restored (sha256 same), green
| Break | Edit | Red |
|---|---|---|
| B6 (subscribe part) | the refinement → `() => true` | `expected null to deeply equal { packageId: [ 'invalid_choice' ] }` |
| B13 | `addDays(startsOn, validityDays)` | T1 `expected { … } to deeply equal { … }` (the end a day late) |
| B14 | the `isActive` check removed | T2 `expected 201 to be 422` |
| B15 | `priceSetById`/`priceReason` not stored | T3 `expected { … } to match object { subscription: … }` |
| B16 | `can('prices.typeByHand')` skipped (`&&` → `\|\|`) | T4 `expected 201 to be 403` |
| B17 | the archived check removed | T5 `expected 201 to be 409` |
| B18 | `findByKey` skipped | T6 `expected [ 201, 500 ] to deeply equal [ 201, 201 ]` (the unique key's 500) |
| B19 | the space's lock removed (links read, `can()` kept) | T6 `Error: 2 request(s) never waited on a lock` — the race harness refuses a race that cannot interleave (finding 52's guard) |
| B20 | `can()` on `space.links` (the lock kept) | T8 `expected 201 to be 403` |

## C3 committed — `e5b8d312` `feat(desk): receive a subscription's payment` (44)
- **Tests first.** U5's payment part (`packages/shared/src/desk/requests.unit.test.ts`, "a payment names exactly one
  item: a visit or a subscription") — red `Tests  1 failed | 7 passed (8)`. T10–T14 (`desk/payments.api.test.ts`, a new
  `describe`: "a payment on a subscription of the space is recorded, 201, with what remains; audited payment.recorded;
  a retry answers it", "a fixed subscription is never paid above its price: PAYMENT_EXCEEDS_DUE, writing nothing; a
  per-hour one takes credit", "exactly one item: both or neither refused 422 before anything is read", "another space's
  subscription is invalid_choice on subscriptionId; a key that paid a visit is a conflict, and the reverse", "an ended
  subscription, and an archived customer's, still take a payment"), and §12.2 check 6 (the first visit test gains
  `subscription: null`) — red `Tests  6 failed | 12 passed (18)`: `expected 422 to be 201` (the schema still required
  `visitId`), `expected { phone: [ 'required' ] } to deeply equal { Object (subscriptionId) }`, `expected { visitId:
  [ 'required' ] } to deeply equal …`, and the visit's answer lacking `subscription`.
- **Green:** U5 `Tests  8 passed (8)`; `desk/payments` + `desk/subscribe` + `desk/checkOut` → `Test Files  3 passed (3)`,
  `Tests  49 passed (49)`.
- **§12.2 check 4:** DESK PR 4's tests that omit `visitId` keep `required` on `visitId` — the "neither" refinement runs
  with Zod's `when` (only for an object body), so a body with no item *and* a bad amount answers both
  (`{ visitId: ['required'], amountAgorot: ['out_of_range'] }`, DESK PR 4's own test, unchanged and green).
- **Built (D6):** `receivePaymentSchema` (`visitId?`, `subscriptionId?`, exactly one); `ReceivedPayment` (`visit:
  DeskVisit | null`, `subscription: SubscriptionState | null`); `payments.record(NewPayment)` with `item: { visitId } |
  { subscriptionId }` replacing `recordForVisit` (audit `after: { visitId | subscriptionId, amountAgorot, method }`);
  `payments.findByKey` answers the subscription too; `subscriptions.lockIn` (`FOR UPDATE`, `null` when not the
  space's); the desk's `subscriptionPayment` branch; a shared helper `withMoney` (a subscription's state and money)
  now serves the subscribe's answer as well.
- **A choice, stated:** a usage-based subscription's `balanceAgorot` is answered as computed — below zero while it
  holds credit (T11: `-5000`), as the customer file's rows already are; the visit branch keeps its `?? 0`.
- Documents: contract (`POST …/payments`: body, the subscription's paragraph, errors, audit, `ReceivedPayment`),
  `payments.md` (what it does, a revised and a new decision, history), `desk.md`.
- `lint` exit 0 · `typecheck` exit 0 · Prettier clean.

### C3's breaks (`scripts\brk.py` + `c3.json`, output `c3-breaks.out`) — each red, restored (sha256 same), green
| Break | Edit | Red |
|---|---|---|
| B6 (payment part) | both refinements → `() => true` | `expected null to deeply equal { Object (subscriptionId) }` |
| B21 | the subscription's money read from a visit's item | T10 `expected { visit: null, …(4) } to deeply equal { visit: null, …(4) }` (paid 0) |
| B22 | `payments_within_due`'s translation line removed | T11 `expected 500 to be 409` |
| B23 | the key's item check ignores a visit's payment | T13 `expected 201 to be 409` |

## C4 committed — `44ca6d89` `feat(desk): renew, paying the oldest debt first` (47)
- **Tests first.** U1 `subscriptions/renewal.unit.test.ts`, U2 `payments/allocation.unit.test.ts`, U3
  `shared/http/idempotencyKey.unit.test.ts` — red `Test Files  3 failed (3)` (`Cannot find module './allocation.ts'`,
  `'./renewal.ts'`, `TypeError: derivedKey is not a function`: the code not written yet). U5 gains "a renewal names the
  renewed subscription; a payment takes a payment's bounds" — red `expected { packageId: 3 } to deeply equal {
  packageId: 3, renewalOfId: 5, …(1) }`. T15–T22 (`desk/renewal.api.test.ts`, 9 tests: T16 split in two — the debt left,
  and the debts settled, which B26 needs) — red `Tests  9 failed (9)` (`expected [] to match object [ { visitId: 1,
  …(2) }, …(1) ]`, `expected 201 to be 409`, `expected 201 to be 422`, …).
- **Green:** units `Tests  6 passed (6)`; U5 `Tests  9 passed (9)`; T1–T22 `Tests  18 passed (18)`; `desk/payments` +
  `desk/checkOut` `Tests  40 passed (40)`.
- **Built (D7 steps 2, 4, 6, 8, 9; S3, S6):** `subscribeSchema` gains `renewalOfId?` and `payment?`;
  `subscriptions.lockIn` answers `renewedById`; `proposedStart` (`renewal.ts`, pure); `allocate` and
  `ALLOCATION_MAX_ITEMS = 50` (`payments/allocation.ts`, pure, typed on the item union); `derivedKey` (SHA-256 of
  `key/index`, as an RFC 9562 version-8 UUID, which `idempotencyKeySchema` accepts); `payments.findByKeys` (one
  query); the desk's `allocatePayment` and `subscribed` (the answer and `CUSTOMER_HAS_DEBT`, computed after the
  payments, also on a retry).
- **New codes** (`add-error-code`: shared, both catalogues with §13 Q2's text as approved, contract §6, provoked by
  T22 and T16): `SUBSCRIPTION_ALREADY_RENEWED` (409) — "This subscription was already renewed." / «جُدّد هذا الاشتراك
  بالفعل.»; `CUSTOMER_HAS_DEBT` (warning) — "The customer still owes on an earlier item." / «ما زال على الزبون دين
  سابق.».
- **Departure, stated:** Appendix A's data-model line "*Checked by the service*: a renewal of the customer's own
  subscription" is not written: the database enforces it (C1's foreign key through `(renewalOfId, customerId)`, stated
  under *Constraints*); the service's 422 is only the earlier, kinder answer.
- Documents: contract (§1's derived keys, the subscribe's body, start date, renewal, payment, warning, retry and
  errors, §6), data model (*A renewal with a debt*), conventions §9 (the desk's subscribing) and §13 (derived keys),
  ADR 0015's *Revised* line (+ derived keys), v1-mvp (the route row, decision 8; the payments row), `desk.md`,
  `payments.md`, `subscriptions.md`.
- `lint` exit 0 (after `eslint --fix` of an unneeded `as unknown` in my test) · `typecheck` exit 0 · Prettier clean.

### C4's breaks (`scripts\brk.py` + `c4.json`, output `c4-breaks.out`) — each red, restored (sha256 same), green
| Break | Edit | Red |
|---|---|---|
| B1 | `endsOn` instead of `endsOn + 1` | U1 `expected '2026-10-30' to be '2026-10-31'` |
| B2 | the debts newest first | U2 three reds, e.g. `expected { item: { visitId: 12 } … } to deeply equal { item: { visitId: 49 } … }` |
| B3 | no `min` (an item overpaid) | U2 `expected [ { item: { visitId: 1 }, …(1) } ] to have a length of 50 but got 1` |
| B4 | the index left out of the hash | U3 `expected '13e7f3eb-…' not to be '13e7f3eb-…'` |
| B24 | the proposal ignored (always today) | T15 `expected { … } to match object { subscription: { …(4) } }` |
| B25 | the allocation newest first (API) | T16 `expected [ { visitId: null, …(3) } ] to match object [ { visitId: 1, …(2) }, …(1) ]` |
| B26 | the warning computed before the payments | T16b `expected { warnings: [ 'CUSTOMER_HAS_DEBT' ] } to be undefined` |
| B27 | the payments recorded outside the transaction (the default client) | T17 `expected 500 to be 409` |
| B28 | `findByKeys` skipped | T18 `expected { … } to deeply equal { … }` (the retry's payments empty) |
| B29 | `itemBalances` read before `lockAtDesk` | T21 `expected 409 to be 201` (the visit paid twice, refused by the ledger) |
| B30 | the renewed check removed | T22 `expected 500 to be 409` (the unique key) |

## C5 committed — `468fcf58` `feat(desk): read a subscription's statement` (43)
- **Tests first** (`desk/statement.api.test.ts`): T23 (scenario 1 hand-computed: 240 + 300 + 180 = 720 minutes × ₪5 an hour
  = 6,000 due, an open check-in today counting its day but no minutes, a payment kept and one voided → paid 2,000,
  balance 4,000, `ENDING_SOON`, the renewal proposed for 2026-10-24), T24, T25 — red `Tests  2 failed | 1 passed (3)`
  (`expected 404 to be 200`, `expected undefined to match object { …(2) }`). **T25 could not be seen red:** before the
  route exists, its 404s are the router's own — the same status it asserts; no break is planned for it.
- **Green:** `Tests  3 passed (3)`; with `renewal.api.test.ts` `Tests  12 passed (12)`.
- **Built:** `SubscriptionStatement` / `StatementCheckIn` (shared); `subscriptions.checkInsOf`, `renewedBy`;
  `payments.paymentsOfSubscription` (a method of its own beside `paymentsFor`, which stays the visits'); the desk's
  `statement` (read without a lock; `withMoney`'s transaction made optional for it); `GET …/subscriptions/:subscriptionId`.
- **A slip of my edit script, fixed before the commit:** re-running a half-applied script doubled three methods
  (`TS2300 Duplicate identifier`); the second copies were removed and the diff checked by hand; then `typecheck` exit 0,
  `lint` exit 0.
- Documents: contract (the statement's route and shape, §4's exception), `desk.md`.

### C5's breaks (`c5.json`, output `c5-breaks.out`) — each red, restored (sha256 same), green
| Break | Edit | Red |
|---|---|---|
| B31 | an open check-in's minutes counted (to now) | T23 `expected { id: 1, customerId: 1, …(25) } to deeply equal { … }` |
| B32 | `renewal` not cleared once renewed | T24 `expected { … } to match object { renewal: null, renewedById: 2 }` |

## C6 committed — `d85aa469` `feat(subscriptions): correct a subscription` (43)
- **The owner's A3, as built:** the staff's `PATCH` corrects limits, dates **and the name**; audited as the other
  corrections; its test is T26 (the name among the fields) and U4's second case, its break **B-name** below.
- **Tests first.** U4 `subscriptions/subscriptionChange.unit.test.ts` (2 tests) and U6 (`can.unit.test.ts` gains
  `'subscriptions.correctPrice': OWNER_ONLY`) — red `Test Files  2 failed (2)`, `Tests  14 failed | 404 passed (418)`
  (`Cannot find module`; the unknown action allowed to no one). The shared schemas' test
  (`packages/shared/src/subscriptions/requests.unit.test.ts`) — red `Cannot find module './requests.ts'`. T26–T31 +
  one access test (`subscriptions/corrections.api.test.ts`, 7) — red `Tests  5 failed | 2 passed (7)` (`expected 404 to
  be 200` … no route). **Two passed before the code, stated:** the not-found test (a missing route answers 404 too) and
  **T31** (a payment waiting while the price is lowered), which rests on the payments' trigger that already exists — its
  proof is B38, below.
- **Green:** U4 + U6 `Tests  420 passed (420)`; shared `Tests  2 passed (2)`; API `Tests  7 passed (7)`.
- **Built (D8):** `correctSubscriptionSchema` (name, `startsOn`, `endsOn?|null`, the four limits `|null`) and
  `correctPriceSchema` (`billing`, `priceAgorot`, `reason` 1–200) in a new `subscriptions/requests.ts`;
  `subscriptionChange.ts` (pure); the service's `correct` / `correctPrice` (each its transaction: the space's lock,
  `can()` under it, `lockIn`, ended → `SUBSCRIPTION_ENDED`); the module's first controller and manage router;
  `can()`'s `subscriptions.correctPrice` (owner); `constraintCodes`' `subscriptions_price_below_paid →
  PRICE_BELOW_PAID`; `subscriptions` gains the clock (`now`) for its answers.
- **§12.2 check 3:** `checkViolationOf` names `subscriptions_price_below_paid` — T30 answers 409 `PRICE_BELOW_PAID`
  (and B37 turns it into 500).
- **New codes** (`add-error-code`; §13 Q2's text): `SUBSCRIPTION_ENDED` (409) — "This subscription was ended early; it
  is no longer corrected." / «أُنهي هذا الاشتراك مبكرًا، فلم يعد يُعدَّل.»; `PRICE_BELOW_PAID` (409) — "The new price is
  less than what was already paid; void a payment first." / «السعر الجديد أقل مما دُفع؛ تُلغى دفعة أولًا.».
- Documents: contract (the two routes, audit, §6), ADR 0009 (two rows + *Revised*; "end it early" joins the first row
  with C7), security, data model (*Hand-typed prices*: the correction), conventions (the ledger's rules + S2),
  `subscriptions.md`.
- `lint` exit 0 · `typecheck` exit 0 · Prettier clean.

### C6's breaks (`c6.json` → `c6-breaks.out`; B38 by `dbbrk.py` → `c6-b38.out`) — each red, restored, green
| Break | Edit | Red |
|---|---|---|
| B5 | every sent field counted as changed | U4 `expected { data: { name: 'شهري', …(4) } … } to deeply equal { data: { …(3) } … }` |
| B-name (A3) | `name` left out of the correctable fields | T26 `expected { … } to match object { id: 1, name: 'شهري — مسائي', …(5) }` |
| B7 | `subscriptions.correctPrice: 'staff'` | U6 `expected true to be false` (reception's two cases) |
| B33 | `subscriptionChange` replaced by the whole body | T26 `expected [ { actorId: 2, …(6) } ] to deeply equal [ … ]` |
| B34 | the ended check removed | T27 `expected 200 to be 409` |
| B35 | `can()` on `space.links` | T28 `expected 200 to be 403` |
| B36 | `requireCan('subscriptions.correctPrice')` removed | T29 `expected 422 to be 403` (reception's invalid body read) |
| B37 | `PRICE_BELOW_PAID`'s translation line removed | T30 `expected 500 to be 409` |
| B38 (database) | `payments_guard_insert`: a subscription's ceiling skipped (`SELECT NULL::integer INTO due`) | T31 `expected 201 to be 409`; restored from `20261020124728_visit_write_off`'s function: md5 same, `prosrc LIKE '%payments_visit_written_off%'` → `t`, the schema fingerprint of `masaha_b_test` = `masaha_b_dev`'s |

## C7 committed — `3d6bf290` `feat(subscriptions): end a subscription early` (45)
- **Tests first** (`subscriptions/end.api.test.ts`, 4): T32, T33, a third test for the clamps D10 states ("one already
  past its end keeps its end; one with no dates ends today"), T34 — red `Tests  4 failed (4)` (`expected 404 to be
  200`, `expected undefined to match object { endsOn: '2026-09-30' }`).
- **Green:** `Tests  4 passed (4)`; with `corrections.api.test.ts` `Tests  11 passed (11)`.
- **Built (D10):** the service's `end` (its end today, its start if not started, never later than it was; who and when;
  audited `subscription.ended`; a repeat answers as it is); `repository.end`; `POST …/subscriptions/:subscriptionId/end`
  (`requireCan('subscriptions.manage')`). The corrections' opening is split: `lockSubscription` (the lock, `can()`,
  the row) shared, `lockForCorrection` adding the ended refusal — behaviour of C6 unchanged (its 7 tests green).
- Documents: contract (the route, audit), data model (ending early, exactly), ADR 0009 (the row and its *Revised* line
  gain "end it early"), security, `subscriptions.md`, `overview.md` (*Built*: the customers' line gains subscriptions),
  v1-mvp (step 8 *Built*, the routes' *Built* line, the two subscription rows).
- `lint` exit 0 · `typecheck` exit 0 · Prettier clean.

### C7's breaks (`c7.json` → `c7-breaks.out`) — each red, restored (sha256 same), green
| Break | Edit | Red |
|---|---|---|
| B39 | `endsOn` left as it was | T32 `expected { … } to match object { id: 1, startsOn: '2026-10-01', …(5) }` |
| B40 | `endsOn = today` (an upcoming one too) | T33 `expected 500 to be 200` (the dates' `CHECK`) |
| B41 | `can()` on `space.links` | T34 `expected 200 to be 403` |

## 12.4 on the head (`3d6bf290`), phase 1's part
- `npm run build -w @masaha/shared` exit 0 · `npm run lint` exit 0 (`> eslint .`, no problem) · `npm run typecheck` exit 0
  (every workspace, the web's two catalogues included).
- `git grep -n "#PRNUM"` → documents only: `api-contract.md` (8), `data-model.md` (7), ADR 0009 (1), ADR 0015 (1), finding
  80 (1), `conventions.md` (4), `security.md` (1), `customers.md` (1), `desk.md` (2), `packages.md` (2), `payments.md` (4),
  `subscriptions.md` (5), `v1-mvp.md` (3).
- `git diff --stat origin/main -- apps/web` → only `copy/arabic/errors.ts` and `copy/english/errors.ts` (4 lines each).
- `git diff --stat origin/main -- package.json package-lock.json` → empty.
- `git status --short` clean; no server was started in phase 1; port 3321: nothing listening.
- **Not run in phase 1, by the owner's split:** `test:unit`, `test:api` (the full lanes), `format:check`, `check:links`,
  the real run — phase 2's. Each touched test file ran in its lane at its commit (above). Prettier was checked on every
  touched TypeScript file at each commit.

## Stop and ask — the PR's size
- `git diff --stat origin/main` → **74 files** (45 `apps/api`, 8 `packages/shared`, 2 `apps/web`, 19 `docs`). The plan's
  §7 estimated ≈ 52 and its *Stop and ask* says "more than about 70 files in one PR". The difference is the carried items
  (14 files: the phone search 6, the documents and findings 8 — not in the plan's estimate), two test files the plan did
  not foresee touching (`desk/customers.api.test.ts`'s raw insert, `payments/balances.api.test.ts`), the module's first
  controller and router, and the shared `subscriptions/requests.ts` with its test.
- **The question for the owner:** keep PR 2 as one PR of 74 files (recommended: its commits are atomic, the carried ones
  first; PR 1 was answered the same way), or split it. Everything phase 2 needs is ready; phase 2 should start only on
  the owner's word.

## The first checks (§12.2, PR 2)
1. The migration, created once — ✔ (the non-TTY refusal, then `migrate diff`, as PR 1; edited as written).
2. The self-relation — ✔ with a departure (`@@unique([renewalOfId, customerId])`; above).
3. The trigger's error — ✔ (`PRICE_BELOW_PAID`, T30; B37).
4. `receivePaymentSchema` — ✔ (`required` on `visitId` kept, beside the other errors, through Zod's `when`).
5. The seed — ✔ (twice on `masaha_b_dev`, unchanged; `src/db` green).
6. The exact-key tests — ✔ (`subscription: null` in DESK PR 4's first payment test; the customer file gains
   `renewalOfId` and `priceTyped`).

## Hand-over to phase 2
- **Branch:** `feat/subscriptions`, **head `3d6bf2908b2b0964178a6662b9c92ef52fde0e20`**, not pushed, cut from
  `origin/main` `5a0cda1a`.
- **Commits** (sha, subject, length):
  1. `0529fef0` fix(customers): find a phone in any form (40) — carried item 1
  2. `bb221048` docs(customers): say what the customers' PR built (49) — carried items 2–5
  3. `90db34b6` feat(db): store a subscription's key and reason (47) — C1, with carried item 6's index
  4. `14a49e3a` feat(desk): subscribe a customer (32) — C2
  5. `e5b8d312` feat(desk): receive a subscription's payment (44) — C3
  6. `44ca6d89` feat(desk): renew, paying the oldest debt first (47) — C4
  7. `468fcf58` feat(desk): read a subscription's statement (43) — C5
  8. `d85aa469` feat(subscriptions): correct a subscription (43) — C6
  9. `3d6bf290` feat(subscriptions): end a subscription early (45) — C7
- **The PR's title** (§11): `feat(desk): run customers' subscriptions` (40).
- **Labels** (§12.7): `feat`, `area:api`, `area:docs`, `area:web`.
- **The description:** `C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\scripts\pr2-body.md` — phase 2 fills in the three
  `<phase 2: …>` lines (`test:unit`, `test:api`, `format:check` / `check:links`, the real run) and `#PRNUM` becomes
  the number (§12.7's `filter-branch` covers the documents only; the description has one `#PRNUM`, in carried item 2).
- **The real run:** `node C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\scripts\realrun2.mjs` with the API on 3321
  (`npm run dev -w @masaha/api`, `curl.exe -s http://localhost:3321/health` → `db: up`). Self-judging: nine `PASS|FAIL`
  lines, then the audit's ten actions, then `ALL PASS` (exit 0) or `<n> FAIL` (exit 1). It reads `SEED_DEMO_PASSWORD`
  and `DATABASE_URL` from `apps/api/.env` itself and prints neither, nor any phone. Checked against the code by reading
  only (and `node --check`, syntax only).
- **Preconditions phase 2 must hold:**
  - Docker's `masaha-postgres-1` running; `masaha_b_dev` migrated to `20261022071444_subscription_terms` (done in phase 1:
    `prisma migrate status` → up to date) and the Prisma client generated at the head (done: the last `rebase -x` step
    ran `prisma generate` on the head's schema). `masaha_b_test` is migrated by the API lane's global setup (already at
    the head's migration: its schema fingerprint equals `masaha_b_dev`'s).
  - `npm run build -w @masaha/shared` at the head before the lanes (done in phase 1; redo if anything changes).
  - **The demo data as the seed left it for «رامي سالم»**: one unpaid visit of ₪15, no subscription, and the package
    «أسبوعي» (₪120, fixed) offered — the script's first case checks it and fails otherwise. **Run it once:** it changes
    the demo data — رامي's visit paid (₪15), two «أسبوعي» subscriptions for him (the first paid ₪50 and ended today,
    the second its renewal, unpaid), and their audit entries. Say so in the report ("leave the demo data as it is, and say
    what changed").
  - Stop the API by its process ids afterwards; port 3321 free; `scripts\server.log` deleted.
- **Memory:** one full lane at a time; worker A's `vitest` under `C:\dev\masaha\app\` waited for, never stopped.

## Phase 2 (OpenCode, 2026-10-22)

### §1 Preconditions — all held
- `git status --short` → clean
- `git branch --show-current` → `feat/subscriptions`
- `git rev-parse --short HEAD` → `3d6bf290`
- `git ls-remote --heads origin feat/subscriptions` → nothing
- `docker ps --format '{{.Names}} {{.Status}}'` → `masaha-postgres-1 Up 3 hours (healthy)`
- `Get-NetTCPConnection -LocalPort 3321 -State Listen` → nothing
- `gh pr view 105 --json state --jq .state` → `MERGED`
- `gh pr list --state open --json number --jq '.[].number'` → nothing
- No `vitest` processes running

### §2 The lanes — each once, one at a time
| Lane | Exit | Result lines |
|---|---|---|
| `npm run build -w @masaha/shared` | 0 | (no result lines to show) |
| `npm run test:unit` | 0 | `Test Files  105 passed (105)`; `Tests  897 passed (897)` |
| `npm run test:api` | 0 | `Test Files  76 passed (76)`; `Tests  1088 passed (1088)` |
| `npm run format:check` | 0 | `All matched files use Prettier code style!` |
| `npm run check:links` | 0 | `2591 links in 169 documents and 1658 source files all resolve.` |

All lanes exited 0.

### §3 The real run — once only
- API started on 3321; health `{"status":"ok","db":"up","timestamp":"2026-10-22T10:01:29.131Z"}` within 60 s.
- `node realrun2.mjs` exit 0, output:
```
PASS precondition: رامي owes 1500 on one visit, no subscription; the package أسبوعي (12000, fixed) 200 -
PASS subscribe with a payment: two payments (the visit 1500, the new one 5000), no CUSTOMER_HAS_DEBT 201 -
PASS the same key: the same body 201 -
PASS a renewal: starts the day after the renewed one ends 201 -
PASS a second renewal with another key 409 SUBSCRIPTION_ALREADY_RENEWED
PASS a payment above a fixed price 409 PAYMENT_EXCEEDS_DUE
PASS the statement: paid 5000, its payment listed, renewed by the renewal 200 -
PASS reception's price correction 403 -
PASS the owner's price below what is paid 409 PRICE_BELOW_PAID
PASS ending it early: EXPIRED, ended by reception 200 -
audit (latest first): subscription.ended, subscription.created, payment.recorded, payment.recorded, subscription.created, space.photoAdded, space.photoAdded, space.photoAdded, space.photoAdded, space.photoAdded
ALL PASS
```
- **What changed in the demo data:** رامي's ₪15 visit was paid; two «أسبوعي» subscriptions created for him — the first paid ₪50 and ended today, the second its unpaid renewal; audit entries for both subscriptions, both payments, and the ending.
- API stopped; port 3321 free; `git status --short` clean.

### §4 The PR number
```
PRNUM OK #106 d0acc06b (was 3d6bf290)
```
`check:links` exit 0; `format:check` exit 0; `git status --short` clean.

### §5 Push and PR
- Push exit 0
- `gh pr create` → #106 https://github.com/Basel-Ghonaim/masaha/pull/106
- Labels: `feat`, `area:api`, `area:docs`, `area:web`

### §6 CI
- `gh pr checks 106 --watch --interval 60` → all checks passed on head `d0acc06b4c3de7fdd5d800705fdfa14bc5d377bc`
  - `format:check` pass 34s
  - `test:unit` pass 1m33s
  - `build` pass 44s
  - `lint` pass 1m50s
  - `check:classes` pass 33s
  - `check:links` pass 36s
  - `typecheck` pass 45s
  - `test:api` pass 4m25s
  - `test:component` pass 16m6s
  - `CodeRabbit` pass
- `gh pr view 106 --json headRefOid,mergeStateStatus` → head `d0acc06b4c3de7fdd5d800705fdfa14bc5d377bc`, `mergeStateStatus: CLEAN`
- Local `git rev-parse HEAD` → `d0acc06b4c3de7fdd5d800705fdfa14bc5d377bc` (matches)

### §6 Conflict check with other open PRs
- `gh pr list --state open` → only #106 (this PR). No other open PRs to check.

### §7 Final state
- Port 3321 free: **yes**
- `git status --short`: **clean**
- Report: `C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\4_REPORT_PR2.md`
