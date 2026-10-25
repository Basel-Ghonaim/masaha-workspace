## Summary

Step 8's second PR, on the API: subscribing a customer from a package or custom terms; renewing, with an optional amount the server allocates over the customer's debts oldest first, one payment per item under one `Idempotency-Key`; a subscription's payment through the desk's payment route; the statement; corrections — limits, dates and name by the staff, price and billing by the owner with a reason; ending early. Finding 80 is resolved in the same migration.

**Carried from #102** (the review of #102, `0_CARRIED_FROM_102.md`; the PR's first commits):
1. **The phone search finds a number typed in any form** — a whole number the phone field accepts (`0521234567`, `00970…`, `059-900-0205`) matches that phone exactly; otherwise the suffix match drops the phone field's separators (review 3 with 9's separators). `fix(customers): find a phone in any form`, its tests seen red first.
2. **The three documents made untrue by #102** — `occupancy.md` (only `announcements` lacks a capability document), `payments.md` (the uncollected visits' decision says what is built); **ADR 0015's line on keys gets its *Revised* line in this PR's C2, as planned**: customers carry the key since #102, subscriptions since #106.
3. **Reception reads an archived customer's file** — kept (the owner's word); the contract says so in one line.
4. **`CUSTOMER_ARCHIVED`'s comment** says "edited".
5. **Findings recorded:** 121 (the auto check-out can stall behind stays that always fail), 122 (`subscription_usage` overflows on extreme usage-based prices), 123 (a delayed retry of a customer edit can revert another desk's edit).
6. **An index on the visits' customer** — `visits_customer_id_closed_idx ON visits (customer_id) WHERE customer_id IS NOT NULL AND checked_out_at IS NOT NULL`, in this PR's migration: a page's balances read its customers' closed visits by index (10.97 ms → 2.08 ms; one customer's file 9.69 ms → 0.72 ms, at 40,000 visits, `EXPLAIN (ANALYZE)`, a rolled-back seed).

## Scope / Acceptance criteria / Out of scope

**Scope**
1. Migration `subscription_terms`: `subscriptions.request_id` (UUID, required, backfilled), `price_reason` (with its `CHECK`, backfilled for the dev data), `renewal_of_id` (unique with the customer, the same customer's); the trigger `subscriptions_guard_price` (a fixed price never below what is paid); finding 80 (`packages` and `subscriptions` prices above zero); the visits' index (carried item 6).
2. `POST …/customers/:customerId/subscriptions` (🧾, `Idempotency-Key`): from a package or custom, a renewal, an optional payment allocated oldest debt first; `meta.warnings`.
3. `POST …/payments` takes `subscriptionId`, exactly one of it and `visitId`.
4. `GET …/subscriptions/:subscriptionId` (🧾): the statement.
5. `PATCH …/subscriptions/:subscriptionId` (🧾): limits, dates and the name; `PUT …/subscriptions/:subscriptionId/price` (🏢): price and billing, with a reason; `POST …/subscriptions/:subscriptionId/end` (🧾).
6. `can()`: `subscriptions.correctPrice` (owner). ADR 0009's table gains the subscription rows.
7. Error codes `SUBSCRIPTION_ALREADY_RENEWED`, `SUBSCRIPTION_ENDED`, `PRICE_BELOW_PAID`, and the warning `CUSTOMER_HAS_DEBT`.
8. Finding 80 resolved.

**Acceptance criteria**
- [x] A subscription from a package copies its terms, its end `validityDays` after its start (inclusive); a retired package or another space's is refused `invalid_choice` on `packageId`.
- [x] A custom subscription carries a reason and who typed its price; reception types it only where the space allows it (403 `PRICE_TYPING_NOT_ALLOWED`).
- [x] The start date: the request's, else the day after the renewed subscription's end while it is still running, else today. A subscription is renewed at most once (`SUBSCRIPTION_ALREADY_RENEWED`).
- [x] An amount given is allocated by the server: the customer's older unpaid items oldest first, each at most its balance, the rest to the new subscription; one payment per item; the ledger refuses a rest above a fixed price (`PAYMENT_EXCEEDS_DUE`) and the whole request writes nothing; `CUSTOMER_HAS_DEBT` warns when an older debt remains. A retry with the same key answers the first subscription and its payments.
- [x] `POST …/payments` with `subscriptionId` records a payment on a subscription of the space; exactly one of `visitId` and `subscriptionId` (422 otherwise); a fixed price is never exceeded (the ledger); a usage-based one may hold credit.
- [x] The statement answers the subscription's status, progress, due, paid, balance, its check-ins and its payments whole, and the renewal's proposed start while it is not renewed.
- [x] The staff correct limits, dates and the name (the owner's choice, A3); only the owner corrects price and billing, with a reason (reception 403 before the body is read); a fixed price below what is paid is refused by the database (`PRICE_BELOW_PAID`); an ended subscription is not corrected (`SUBSCRIPTION_ENDED`); each correction audited, a correction that changes nothing writes nothing.
- [x] Ending early sets the end to today (its start, if it has not started), records who and when, and changes no money; the subscription is `EXPIRED` from then; a repeat answers it as it is.

**Out of scope:** subscription check-ins and *present* defined once (PR 3); the screens 14, 15, 16 and the desk's subscriber parts (worker A's later items); every web change but the catalogue lines; an export of customers or phones; voids, the payments list, collections, finance (steps 9 / 11); closure extensions (step 10); a payment inside a subscriber's check-out.

## Change type

feat — API code, the shared contract, tests and documents; a migration (subscriptions' key, price reason, renewal link; the price trigger; finding 80; the visits' index); the new codes' catalogue lines in apps/web (worker B's licence).

## New error codes (the Arabic needs the owner's approval)

As §13 Q2 of the plan wrote them (approved there, 2026-10-20):

| Code | Answer | English | Arabic |
|---|---|---|---|
| `SUBSCRIPTION_ALREADY_RENEWED` | 409 | This subscription was already renewed. | جُدّد هذا الاشتراك بالفعل. |
| `SUBSCRIPTION_ENDED` | 409 | This subscription was ended early; it is no longer corrected. | أُنهي هذا الاشتراك مبكرًا، فلم يعد يُعدَّل. |
| `PRICE_BELOW_PAID` | 409 | The new price is less than what was already paid; void a payment first. | السعر الجديد أقل مما دُفع؛ تُلغى دفعة أولًا. |
| `CUSTOMER_HAS_DEBT` | warning | The customer still owes on an earlier item. | ما زال على الزبون دين سابق. |

## Evidence

- `lint`, `typecheck` (each commit, `git rebase -x` with the client regenerated per commit, and on the head), `build -w @masaha/shared`: exit 0 each.
- `test:unit`: Test Files  105 passed (105); Tests  897 passed (897).
- `test:api`: Test Files  76 passed (76); Tests  1088 passed (1088).
- `format:check`, `check:links`: All matched files use Prettier code style!; 2591 links in 169 documents and 1658 source files all resolve.
- **Seen failing first** (each in its lane, before its code): U3 of the phone search (`expected { phoneDigits: '0599000205' } to deeply equal { phone: '+970599000205' }`) and T22 (`expected [] to deeply equal [ 'Dana' ]`); D1–D5 (`Unknown argument idempotencyKey` … `promise resolved … instead of rejecting`); U5 (subscribe, payment, renewal); T1–T9 (`expected 404 to be 201`); T10–T14 (`expected 422 to be 201`); U1–U3 (`Cannot find module`); T15–T22 (`expected [] to match object [ { visitId: 1, … } ]`); T23–T24 (`expected 404 to be 200`); U4, U6, the corrections' schemas, T26–T30 (`expected 404 to be 200`); T32–T34 (`expected 404 to be 200`). Seen green only, said: T25 and the corrections' not-found test (a missing route also answers 404) and T31 (it rests on the payments' trigger, which already existed — its proof is B38).
- **Deliberate breaks, each red then restored** (sha256 or md5 the same, green again): B1–B41 of the plan and one for the name's correction (A3): B1, B2, B3, B4, B5, B6 (subscribe and payment parts), B7, B8–B12 (database: the reason's check, the `> 0` checks, the renewal's and the key's unique indexes, the price trigger), B13–B41, B38 (database: the payments trigger's subscription ceiling), B-name. The red line of each is in the executor's report.
- **Real run on 3321** (`masaha_b_dev`, `scripts\realrun2.mjs`): PASS precondition: رامي owes 1500 on one visit, no subscription; the package أسبوعي (12000, fixed) 200 -; PASS subscribe with a payment: two payments (the visit 1500, the new one 5000), no CUSTOMER_HAS_DEBT 201 -; PASS the same key: the same body 201 -; PASS a renewal: starts the day after the renewed one ends 201 -; PASS a second renewal with another key 409 SUBSCRIPTION_ALREADY_RENEWED; PASS a payment above a fixed price 409 PAYMENT_EXCEEDS_DUE; PASS the statement: paid 5000, its payment listed, renewed by the renewal 200 -; PASS reception's price correction 403 -; PASS the owner's price below what is paid 409 PRICE_BELOW_PAID; PASS ending it early: EXPIRED, ended by reception 200 -; audit (latest first): subscription.ended, subscription.created, payment.recorded, payment.recorded, subscription.created, space.photoAdded, space.photoAdded, space.photoAdded, space.photoAdded, space.photoAdded; ALL PASS.
- **Not run:** `test:component`, the web's `build`, `check:build`, `check:classes` — two catalogues of strings, whose parity the typecheck enforces; CI runs them.

**Departures from the plan, stated:**
- The renewal's self-relation through `(renewalOfId, customerId)` is kept, with `@@unique([renewalOfId, customerId])` in place of `@unique` on `renewalOfId`: Prisma refuses a one-to-one relation without a unique key on its fields. The foreign key makes a renewal's customer the renewed one's, so the pair is unique exactly when `renewal_of_id` is — the same rule, both halves in the database (D3).
- The data model's *Checked by the service* gains no "a renewal of the customer's own subscription": the database enforces it (the foreign key above); the service's 422 is only the earlier answer.
- `prisma migrate dev --create-only` refuses a non-interactive shell; the migration was written from `prisma migrate diff --from-config-datasource --to-schema`, then edited as the plan says (the backfill before `NOT NULL`, the raw SQL appended).
- A usage-based subscription's payment answers its balance as computed, below zero while it holds credit.

## Screenshots

None: API and documents only.

## Definition of Done checklist

- [x] Acceptance criteria met, scope kept.
- [x] Lint and typecheck clean; `packages/shared` builds.
- [x] Tests added in the owning lanes, each seen failing.
- [x] No hardcoded user-facing text (codes only; both catalogues).
- [x] Authorization on the server (the boundary, `requireCan`, `can()` under the space's lock).
- [x] Triggered documentation updated in this PR.
- [x] One home per fact; nothing claimed that is not built.
- [x] Every claim names its test or command.
- [x] Atomic history, pushed.
