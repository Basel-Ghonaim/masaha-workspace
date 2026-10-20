# SUBSCRIPTIONS — customers, subscriptions and subscription check-ins, on the API (build map step 8) — the plan

> **Base:** `origin/main` at `abc28e73` (Merge #97, `feat/auto-checkout`, 2026-10-20). DESK PR 4
> (`feat/visit-debts`, planned in `C:\dev\masaha\workspace\WORKER_B\DESK\2_PLAN_PR4.md`) is **not built**; this
> plan builds on it as that plan describes it, and **its executor starts only after DESK PR 4 has merged**
> (§12.1 checks what merged against what this plan assumes).
> **Worker:** B, in `C:\dev\masaha\app-b`. **Folder:** `C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\`: this plan
> `2_PLAN.md`; the reports `4_REPORT_PR<n>.md`; the executor's scripts in `scripts\` (never committed).
> **Three PRs in sequence**, each cut from the latest `origin/main` once the one before it has merged:
> **PR 1** `feat/customers` (≈ 42 files, one migration) · **PR 2** `feat/subscriptions` (≈ 52 files, one
> migration) · **PR 3** `feat/subscription-check-ins` (≈ 38 files, no migration). Each is over 25 files and
> touches authorization, money, transactions or the schema: each gets its own review conversation.
> **Read only from commit objects** (`git show origin/main:…`, `git grep`, `git ls-tree`). Nothing was run,
> built, installed or checked out. Every point reading could not prove is an **executor check** (§12.2 of each
> PR), with what to do if it fails.
> **In parallel:** worker A's OWNER_SETUP (`apps/web`, `docs`). No code file is shared. Shared documents, each a
> likely text conflict (the fast path, workflow §9): `docs/project/overview.md` (*Built* lines),
> `docs/architecture/findings/README.md` (the index), `docs/plans/v1-mvp.md` (step 8's lines and the route
> table), `docs/README.md` (the map's feature lines), and the web's `apps/web/src/shared/copy/{arabic,english}/errors.ts`
> (the error lines only, worker B's licence) if OWNER_SETUP touches them.
> **Finding numbers:** this item's start at **120** (worker A's run from 101; DESK PR 4 holds 110–119). This plan
> records **120** (PR 1); any other finding an executor records takes **121**, then 122, and so on, across the
> three PRs, in order.

> **Approved by the owner, 2026-10-20 — binding on every executor of this plan:**
> - **§13 as planned:** Q1 S1 (`subscription_usage`; A1 not taken); Q2 the nine codes **with the Arabic as
>   written**; Q3 the migrations; Q4 the attendance rules (whole minutes, a per-hour due half up — not the
>   space's visit rounding); Q5 "shorter than a week"; Q6 S4 `UPCOMING` and S5; Q7 S3 and S6; Q9 **finding 113
>   folded into PR 1** (C6); Q10 ADR 0009's four rows and ADR 0015's *Revised* line; Q11 the list by name, then
>   id. S2, S8, S9, S10 and S11 as planned.
> - **Changed from the plan — Q8, A3 taken:** a subscription's **name is correctable by the staff** in the
>   corrections' `PATCH` (limits, dates and the name; the price and billing stay on the owner's `PUT …/price`);
>   audited as the other corrections; one test and its break. The rest of Q8 as planned (the archive refused
>   while present; the subscriber's payment through `POST …/payments`, not inside the check-out).
> - **Each PR has its own execution prompt** (`3_EXEC_PROMPT_PR<n>.md`); an executor builds only the PR its
>   prompt names; a `0_CARRIED_FROM_<n>.md` from the previous PR's review, if any, is that PR's first commit.

---

## 1. Summary

Step 8's API: the staff keep customers on file and run their subscriptions.

- **PR 1 — customers.** A customer created (idempotent: customers gain their key, ADR 0015 rule 4), edited
  (both roles), archived and restored (the owner). The customers list: paged, searched by name or a phone's
  last digits, filtered by the current subscription's status and kind and by payment state — **the payment
  filter and every debt computed in the database**, by one aggregate query of `payments` (the owner's decision
  6). The customer's file: the customer, the debt and the credit, every subscription with its status, progress
  and balance, the unpaid visits with their payments (K4), and who is present. Subscription **status and
  progress** arrive as pure rules (`subscriptions`), on attendance counted by one database function (§5 S1).
- **PR 2 — subscriptions and their money.** A new subscription from a package or custom (the hand-typed price
  rule, #92); a renewal, its start date proposed by the server (decision 3), at most one per subscription; an
  optional amount the **server** allocates oldest debt first, one payment per item, in one transaction under
  one `Idempotency-Key` (K3, decision 8); a payment on a subscription through DESK PR 4's `POST …/payments`
  (`subscriptionId`, "exactly one of"); the statement (progress, check-ins, payments, the renewal's proposed
  start); correcting one — limits and dates by the staff, price and billing by the owner only with a reason,
  every correction audited (decision 4); ending one early, the status only (decision 5).
- **PR 3 — subscription check-ins.** In `desk`, beside the visit's (decision 9): check-in naming its
  subscription, with the full space's and the limits' warnings, never a block; check-out; the open and dated
  lists. *Present* becomes one helper in `occupancy` (decision 10; DESK PR 4's finding on #95's nit 7 resolved).

Nothing in `apps/web` except the error codes' catalogue lines. No export of customers or phones for anyone
(decision 7). No booking, online payment, QR or claiming (overview *Not in v1*).

---

## 2. The contract

### Scope

**PR 1 — `feat/customers`**
1. Migration `customer_key`: `customers.request_id` (UUID, nullable), unique within the space.
2. Migration `subscription_usage`: the database function `subscription_usage(space, customer, today,
   week_start)` — each subscription's days used, minutes used, days this week, minutes today, and amount due
   (§4 D3).
3. `@masaha/shared/customers` (new, L2), `@masaha/shared/subscriptions` (new, L3), `core/gazaTime.ts` gains
   `addDays` and `weekStartOf` (Saturday).
4. `POST /manage/spaces/:spaceId/customers` (🧾, `Idempotency-Key`), `PATCH …/customers/:customerId` (🧾).
5. `POST …/customers/:customerId/archive` and `POST …/customers/:customerId/restore` (🏢).
6. `GET …/customers` (🧾): paged, `q`, `status`, `kind`, `packageId`, `payment`; `GET …/customers/:customerId`
   (🧾): the file.
7. `subscriptions`: the pure status and progress rules; the states of a space's or a customer's subscriptions.
8. `payments`: the customers' balances and the per-item balances, in SQL; the payment filter as ids.
9. `can()`: `customers.archive` (owner). ADR 0009's table gains the customer rows.
10. Error code `CUSTOMER_ARCHIVED`; `PHONE_TAKEN` and `MEMBER_ALREADY_CHECKED_IN` used for the first time.
11. Finding 120 recorded. (Finding 113, if the owner folds it: the uncollected visits paged in SQL, §6.)

**PR 2 — `feat/subscriptions`**
1. Migration `subscription_terms`: `subscriptions.request_id` (UUID, required, backfilled), `price_reason`
   (with its `CHECK`, backfilled for the dev data), `renewal_of_id` (unique, the same customer's); the trigger
   `subscriptions_guard_price` (a fixed price never below what is paid); finding 80 (`packages` and
   `subscriptions` prices above zero).
2. `POST …/customers/:customerId/subscriptions` (🧾, `Idempotency-Key`): from a package or custom, a renewal,
   an optional payment allocated oldest debt first; `meta.warnings`.
3. `POST …/payments` (DESK PR 4's) takes `subscriptionId`, exactly one of it and `visitId`.
4. `GET …/subscriptions/:subscriptionId` (🧾): the statement.
5. `PATCH …/subscriptions/:subscriptionId` (🧾): limits and dates; `PUT …/subscriptions/:subscriptionId/price`
   (🏢): price and billing, with a reason; `POST …/subscriptions/:subscriptionId/end` (🧾).
6. `can()`: `subscriptions.correctPrice` (owner). ADR 0009's table gains the subscription rows.
7. Error codes `SUBSCRIPTION_ALREADY_RENEWED`, `SUBSCRIPTION_ENDED`, `PRICE_BELOW_PAID`, and the warning
   `CUSTOMER_HAS_DEBT`.
8. Finding 80 resolved.

**PR 3 — `feat/subscription-check-ins`**
1. `occupancy/present.ts`: *present* defined once (decision 10).
2. `POST …/check-ins` (🧾, `Idempotency-Key`) and `POST …/check-ins/:checkInId/check-out` (🧾), in `desk`.
3. `GET …/check-ins?open=true` (whole) and `GET …/check-ins?from=&to=` (paged).
4. Warnings `SUBSCRIPTION_NOT_STARTED`, `SUBSCRIPTION_EXPIRED`, `DAYS_PER_WEEK_USED`, `HOURS_PER_DAY_USED`;
   `MEMBER_ALREADY_CHECKED_IN` and `CUSTOMER_ARCHIVED` refuse.
5. DESK PR 4's finding for #95's nit 7 (expected number 111 — §12.1 reads it) resolved.

### Acceptance criteria

**PR 1**
- [ ] A customer is created with a name and an optional phone, audited; a retry with the same key answers the
      first customer, 201, never a second; a phone another customer of the space holds (not archived) is
      refused 409 `PHONE_TAKEN` with `errors.phone = ["not_unique"]`, writing nothing.
- [ ] Owner and reception edit a customer's name and phone; an archived one is refused `CUSTOMER_ARCHIVED`; an
      edit that changes nothing writes nothing; every change audited with before and after.
- [ ] Only the owner archives and restores (reception 403 before anything is read); a present customer is not
      archived (`MEMBER_ALREADY_CHECKED_IN`); an owing customer is (the confirm is the web's, DK-014); a
      restore whose phone another customer now holds is refused `PHONE_TAKEN`; a repeat answers as it is.
- [ ] The list pages the space's customers, archived ones only for `status=ARCHIVED` (the owner's; reception
      403); `q` matches a name (Arabic folded as the directory's search) or, when it is digits only (two or
      more), a phone's last digits; `status`, `kind`/`packageId` and `payment` filter **before** the page is
      cut: every page full, the total right.
- [ ] Debt, credit and the payment filter are computed by one SQL query of `payments`; no request reads every
      payment, visit or check-in into memory; a voided payment counts for nothing; a written-off visit is no
      debt; credit is only a usage-based subscription's.
- [ ] The file answers the customer, the debt, the credit, each subscription with status, progress, due, paid
      and balance, the unpaid visits with their payments (voided ones marked), and who is present.
- [ ] Status and progress follow the data model (Gaza dates, Saturday-to-Friday weeks), every branch a unit test.

**PR 2**
- [ ] A subscription from a package copies its terms, its end `validityDays` after its start (inclusive); a
      retired package or another space's is refused `invalid_choice` on `packageId`.
- [ ] A custom subscription carries a reason and who typed its price; reception types it only where the space
      allows it (403 `PRICE_TYPING_NOT_ALLOWED`).
- [ ] The start date: the request's, else the day after the renewed subscription's end while it is still
      running, else today. A subscription is renewed at most once (`SUBSCRIPTION_ALREADY_RENEWED`).
- [ ] An amount given is allocated by the server: the customer's older unpaid items oldest first, each at most
      its balance, the rest to the new subscription; one payment per item; the ledger refuses a rest above a
      fixed price (`PAYMENT_EXCEEDS_DUE`) and the whole request writes nothing; `CUSTOMER_HAS_DEBT` warns when
      an older debt remains. A retry with the same key answers the first subscription and its payments.
- [ ] `POST …/payments` with `subscriptionId` records a payment on a subscription of the space; exactly one of
      `visitId` and `subscriptionId` (422 otherwise); a fixed price is never exceeded (the ledger); a usage-based
      one may hold credit.
- [ ] The statement answers the subscription's status, progress, due, paid, balance, its check-ins and its
      payments whole, and the renewal's proposed start while it is not renewed.
- [ ] The staff correct limits and dates; only the owner corrects price and billing, with a reason (reception
      403 before the body is read); a fixed price below what is paid is refused by the database
      (`PRICE_BELOW_PAID`); an ended subscription is not corrected (`SUBSCRIPTION_ENDED`); each correction
      audited, a correction that changes nothing writes nothing.
- [ ] Ending early sets the end to today (its start, if it has not started), records who and when, and changes
      no money; the subscription is `EXPIRED` from then; a repeat answers it as it is.

**PR 3**
- [ ] A check-in names a subscription of the space; its customer must not be archived (`CUSTOMER_ARCHIVED`)
      nor present by a check-in or a visit (`MEMBER_ALREADY_CHECKED_IN`); it warns, never refuses:
      `SPACE_FULL`, `OUTSIDE_OPENING_HOURS`, `SUBSCRIPTION_NOT_STARTED`, `SUBSCRIPTION_EXPIRED`,
      `DAYS_PER_WEEK_USED`, `HOURS_PER_DAY_USED`, in that order; one transaction under the space's lock; a retry
      answers the same check-in, 201.
- [ ] Check-out closes it now, `MANUAL`, audited, and answers the subscription's due, paid and balance; a check-out
      of a closed check-in answers it as it is.
- [ ] The open list is whole; the dated list pages a Gaza date range, latest first.
- [ ] *Present* has one definition in `occupancy`, used by the staff's read, the check-in warnings (visit and
      subscription) and the directory.

### Out of scope
- The screens 14, 15, 16 and the desk's subscriber parts: worker A's later items. Every web change but the
  catalogue lines.
- An export of customers or phones, for anyone (decision 7); the owner's later export is step 11's.
- Voids, the payments list, collections, finance, the debt reminder: step 9 / 11.
- Merging duplicate customers (v1 has none); a customer as a platform user (`userId`, unused in v1).
- Closure extensions of subscriptions (step 10).
- «تسجيل كزيارة» as the customer (DK-020): a visit checked in as a customer is not built here.
- A payment taken inside the check-out of a subscriber: the desk calls `POST …/payments` after it (§4 D11).
- The shared desk device (the desk's screen item).

---

## 3. The reading done, and what it changed

From `origin/main` at `abc28e73`: `CLAUDE.md`; `docs/development/workflow.md` (§2–§4, §7, §9) and
`testing.md` (§3–§4); `docs/backend/conventions.md` (whole: §4, §5, §6, §7–§9, §11, §13); `security.md`
(*Authorization*); ADR 0009 (with its *Revised* lines), 0010, 0015; `docs/architecture/data-model.md` (whole);
`docs/api/api-contract.md` (§1–§4, *Packages*, *Front desk (managed)*, *Internal*, §6); `docs/features/payments.md`,
`visits.md`, `desk.md` (whole); `docs/plans/v1-mvp.md` (steps 7–9, the managed route table);
`docs/project/overview.md` (*Built*, the v1 lines); the findings index and finding 80;
`C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_DESK.md` (whole); `C:\dev\masaha\workspace\_SHARED\OPEN_DECISIONS.md`;
`C:\dev\masaha\workspace\WORKER_B\DESK\2_PLAN.md` (the approval note, §4–§5, §11–§14, Appendix A),
`2_PLAN_PR4.md` (whole: D1–D7, S1–S5, §9, §12, §13), `3_EXEC_PROMPT_PR3.md` (§2), `0_CARRIED_FROM_97.md`,
`6_REVIEW_PR2_CLAUDE_CODE.md` (nits 7–9) and `6_REVIEW_PR3_CLAUDE_CODE.md` (item 7); `schema.prisma` (the
enums, `SpaceSettings`, `SpaceOccupancy`, `Customer` … `AuditLog`); the migrations `front_desk`, `payments`,
`reception_typed_prices`, `desk_visit_charge`; the code of `customers`, `subscriptions`, `payments` (whole),
`desk` (whole), `visits` (service, repository's exports), `occupancy` (service), `packages` (service,
`packageTerms.ts`, index), `spaces` (the lock, the week), `shared/auth` (`can.ts`, `spaceAccess.ts`, index);
`packages/shared` (`core/{fields,pagination,phone,idempotencyKey,envelope,gazaTime,errors}.ts`,
`packages/*`, `visits/requests.ts`, `desk/requests.ts`, `payments/requests.ts`, `package.json`);
`eslint.config.js` (the level map); `apps/api/test/{factories,locks}.ts` (signatures);
`apps/api/src/db/subscriptions.api.test.ts` (titles); the demo seed (`db/seed/demo.ts`, `demo.api.test.ts`);
`app.ts` (the wiring); the web's `errors.ts` (the existing customer and check-in lines); the prototype's
`Customers.html` (the filters), `desk-data.js` (status, progress, due, balance, credit, search) and
`desk-core.jsx` (`checkInWarnings`); `docs/design/SCREENS.md` (14–16).

**What the reading changed:**
- **The customers' status and progress land in PR 1, not PR 2.** The file shows every subscription's status
  and balance, and the list filters by status: both need the rules. PR 2 keeps every write.
- **A subscription's amount due must be computed in the database** for decision 6 to hold: a usage-based
  subscription's due is its attendance times its rate, so a debt computed in SQL needs the attendance in SQL.
  One database function, owned by `subscriptions`, counts it, and every read uses it (S1). The status and
  progress stay pure TypeScript on those counts (conventions §8).
- **The prototype's filters** (`Customers.html`): status chips (active, ending soon, expired, and archived for
  the owner), a kind (by package, custom, none) and a payment state (owes, in credit, settled), on the
  customer's **current** subscription. The API follows them (§4 D4).
- **`PHONE_TAKEN`, `MEMBER_ALREADY_CHECKED_IN` and `CHECK_IN_ALREADY_CLOSED` exist** in the catalogue,
  unused. The first two are used here; the third stays unused (a repeated check-out answers the closed record,
  conventions §13).
- **Subscriptions have no idempotency key, no price reason and no link to what they renew.** PR 2's migration
  adds the three. The seed's two typed prices have no reason: the migration backfills them (§4 D9).
- **A renewal's payments need one key each** (the ledger's unique `(space, request_id)`), but the request has
  one: they derive theirs from it (S6).
- **A price correction below what is paid** would leave a fixed-price subscription in credit, which the ledger
  forbids; the insert trigger cannot see an update, so a trigger on `subscriptions` refuses it (S2).

---

## 4. The decisions as built

### The owner's decisions (2026-10-20), as built
1. **Three PRs** (§1). The reading shows no better cut; the status rules move into PR 1 (§3).
2. **Two active subscriptions for one customer are allowed:** no constraint; a check-in names its subscription
   (`subscriptionId` in its body); the desk may preselect (a web behaviour).
3. **The renewal's start date:** D7.
4. **Correcting:** D8. **5. Ending early:** D10.
6. **The list's payment filter and debts in the database:** D3, D5 — `payments`' one aggregate query.
7. **Phone privacy (OPEN_DECISIONS point 3, settled):** the list is paged (at most 50) and searched, for both
   roles; no export route exists for anyone. PR 1's report updates point 3 (§12.8).
8. **The renewal with a debt is one request:** D7, the allocation; the build map's route row rewritten.
9. **Subscription check-ins in `desk`:** D11; the paths `/check-ins` kept.
10. **One definition of *present*:** D12, in PR 3.
- **Unchanged (settled):** editing both roles, archiving the owner's; an owing customer may be archived; limits
  warn; status from the end date or the total, whichever first; a typed price needs a reason; no merging.

### D1 — routes and answers

| PR | Route | Access | Key | Body / query | 2xx |
|---|---|---|---|---|---|
| 1 | `POST /manage/spaces/:spaceId/customers` | 🧾 `requireCan('customers.manage')` | ✓ | `{ name, phone? }` | **201** `Customer` |
| 1 | `PATCH …/customers/:customerId` | 🧾 `requireCan('customers.manage')` | — | `{ name?, phone? }` (`null` clears the phone) | **200** `Customer` |
| 1 | `POST …/customers/:customerId/archive` | 🏢 `requireCan('customers.archive')` | — | — | **200** `Customer` |
| 1 | `POST …/customers/:customerId/restore` | 🏢 `requireCan('customers.archive')` | — | — | **200** `Customer` |
| 1 | `GET …/customers` | 🧾 | — | `?q=&status=&kind=&packageId=&payment=&page=&limit=` | **200** `CustomerRow[]`, `meta` |
| 1 | `GET …/customers/:customerId` | 🧾 | — | — | **200** `CustomerFile` |
| 2 | `POST …/customers/:customerId/subscriptions` | 🧾 `requireCan('subscriptions.manage')` | ✓ | `subscribeSchema` (D7) | **201** `NewSubscription`, `meta.warnings?` |
| 2 | `POST …/payments` (DESK PR 4's) | 🧾 `requireCan('payments.record')` | ✓ | + `subscriptionId` (D6) | **201** `ReceivedPayment` |
| 2 | `GET …/subscriptions/:subscriptionId` | 🧾 | — | — | **200** `SubscriptionStatement` |
| 2 | `PATCH …/subscriptions/:subscriptionId` | 🧾 `requireCan('subscriptions.manage')` | — | `{ startsOn?, endsOn?, totalDays?, daysPerWeek?, hoursPerDay?, totalHours? }` | **200** `SubscriptionState` |
| 2 | `PUT …/subscriptions/:subscriptionId/price` | 🏢 `requireCan('subscriptions.correctPrice')` | — | `{ billing, priceAgorot, reason }` | **200** `SubscriptionState` |
| 2 | `POST …/subscriptions/:subscriptionId/end` | 🧾 `requireCan('subscriptions.manage')` | — | — | **200** `SubscriptionState` |
| 3 | `POST …/check-ins` | 🧾 `requireCan('attendance.record')` | ✓ | `{ subscriptionId }` | **201** `DeskCheckIn`, `meta.warnings?` |
| 3 | `POST …/check-ins/:checkInId/check-out` | 🧾 `requireCan('attendance.record')` | — | — | **200** `CheckInCheckOut` |
| 3 | `GET …/check-ins` | 🧾 | — | `?open=true` **or** `?from=&to=&page=&limit=` | **200** `DeskCheckIn[]` (whole for `open`, `meta` for a range) |

- **Placement** (conventions §7–§9, R4): an operation spanning modules is `desk`'s: the list and the file
  (composed reads, §9), the archive (it asks *present*), the subscribe (customers, packages, subscriptions,
  payments), the statement (subscriptions and payments), the check-ins (decision 9) and the payment
  (DESK PR 4). A write of one module is its own router: the customer's create, edit and restore
  (`customers`); the subscription's corrections and its end (`subscriptions`); the check-ins' lists
  (`subscriptions`, a read of `check_ins` with `customers`' names).
- **Price and billing on their own `PUT …/price`, 🏢:** a route the owner alone may call is refused before its
  body is read (security › Authorization), as the visit's `PUT …/charge`; a `PATCH` holding both would need a
  code of its own for reception's price. *Alternative A2.*
- **Reads ask no `requireCan`** (#86's decision, the boundary is the staff's check); `status=ARCHIVED` is the
  owner's, checked by the service (`can(actor, 'customers.archive', …)`, 403).
- **Path ids** answer `not_found` (404) when not the space's; **body ids** (`packageId`, `renewalOfId`,
  `subscriptionId`) `invalid_choice` (422), as the visit's `shiftId`.

### D2 — the shapes (`@masaha/shared`)

```ts
// customers (L2)
CUSTOMER_NAME_MAX_LENGTH = 60
createCustomerSchema = z.object({ name: textSchema(1, 60), phone: phoneSchema.optional() })
updateCustomerSchema = z.object({ name: textSchema(1, 60), phone: phoneSchema.nullable() }).partial()
Customer = { id, name, phone: string | null, archivedAt: string | null }

// subscriptions (L3)
SUBSCRIPTION_STATUSES = ['UPCOMING', 'ACTIVE', 'ENDING_SOON', 'EXPIRED'] as const
SubscriptionProgress = { daysUsed, daysThisWeek, minutesUsed, minutesToday }   // closed stays' minutes; days with any check-in
DeskSubscription = {
  id, customerId, packageId: number | null, renewalOfId: number | null, name,
  startsOn: string | null, endsOn: string | null,                  // Gaza dates, YYYY-MM-DD
  totalDays, daysPerWeek, hoursPerDay, totalHours: number | null,
  billing: 'FIXED' | 'PER_HOUR' | 'PER_DAY', priceAgorot, audience, shiftId: number | null,
  priceTyped: { byId: number, reason: string } | null,              // a desk-typed or corrected price
  ended: { at: string, byId: number } | null,
}
SubscriptionState = DeskSubscription & { status, progress: SubscriptionProgress, dueAgorot: number }
correctSubscriptionSchema = z.object({ startsOn, endsOn: isoDate.nullable(), totalDays…totalHours: count.nullable() }).partial()
correctPriceSchema = z.object({ billing: z.enum(SUBSCRIPTION_BILLINGS), priceAgorot: 1–PRICE_MAX_AGOROT, reason: textSchema(1, 200) })
checkInsQuerySchema = open=true | { from: isoDate, to: isoDate (≥ from, ≤ 92 days later), page, limit }

// payments (L4)
ItemPayment = VisitPayment & { voided: { at, byId, reason } | null }
CustomerBalance = { debtAgorot: number, creditAgorot: number }

// desk (L5)
CUSTOMER_STATUS_FILTERS = [...SUBSCRIPTION_STATUSES, 'ARCHIVED']; CUSTOMER_KINDS = ['PACKAGE', 'CUSTOM', 'NONE']
PAYMENT_FILTERS = ['OWES', 'CREDIT', 'SETTLED']
customersQuerySchema = paginationQuerySchema.extend({ q: textSchema(1, 60).optional(),
  status: z.enum(CUSTOMER_STATUS_FILTERS).optional(), kind: z.enum(CUSTOMER_KINDS).optional(),
  packageId: id.optional(), payment: z.enum(PAYMENT_FILTERS).optional() })   // packageId implies PACKAGE; with another kind: invalid_choice on kind
CustomerRow = Customer & { current: { id, name, endsOn, status } | null } & CustomerBalance
CustomerFile = { customer: Customer } & CustomerBalance & {
  present: { kind: 'CHECK_IN', id, subscriptionId, since } | { kind: 'VISIT', id, since } | null,
  subscriptions: (SubscriptionState & { paidAgorot, balanceAgorot })[],   // the latest started first, then id desc
  unpaidVisits: { visit: DeskVisit, payments: ItemPayment[], paidAgorot, balanceAgorot: number | null }[],   // oldest first
}
subscribeSchema = z.object({
  packageId: id.optional(),
  custom: z.object({ name, endsOn?, totalDays?…totalHours?, billing, priceAgorot, audience, shiftId?, reason }).optional(),
  startsOn: isoDate.optional(), renewalOfId: id.optional(),
  payment: paymentSchema.optional(),
}).refine(exactly one of packageId and custom)   // both or neither: invalid_choice on packageId
NewSubscription = { subscription: SubscriptionState & { paidAgorot, balanceAgorot },
                    payments: { item: { visitId } | { subscriptionId }, payment: VisitPayment }[], debtAgorot }
SubscriptionStatement = SubscriptionState & { paidAgorot, balanceAgorot,
  customer: { id, name, phone }, checkIns: { id, checkedInAt, checkedOutAt, checkoutMethod, minutes: number | null }[],
  payments: ItemPayment[], renewal: { startsOn: string } | null, renewedById: number | null }
DeskCheckIn = { id, customer: { id, name, phone }, subscription: SubscriptionState,
                checkedInAt, checkedOutAt: string | null, checkoutMethod: 'MANUAL' | 'AUTO' | null }
CheckInCheckOut = DeskCheckIn & { paidAgorot, balanceAgorot }
ReceivedPayment (DESK PR 4) → { visit: DeskVisit | null, subscription: SubscriptionState | null, payment, paidAgorot, balanceAgorot }
```
- `isoDate`: a `YYYY-MM-DD` calendar date that exists (`invalid_format`), in `core/fields.ts` (`dateSchema`).
- **`ReceivedPayment` gains `subscription` and its `visit` becomes nullable:** additive for the item it names;
  no client reads it yet (DESK PR 4 has no screen).

### D3 — attendance and the amount due in the database (S1)

PR 1's migration `subscription_usage` (raw SQL only; Prisma creates the empty migration, the executor appends):

```sql
-- A subscription's attendance and amount due (docs/architecture/data-model.md › Derived values), for the
-- set-based reads: one row per subscription of the space (of one customer, when given). A day is used by any
-- check-in on it, open or closed; minutes count closed stays only, whole minutes each. The week's start is
-- the caller's (the shared calendar's Saturday), never computed here. Prisma compares no function, so later
-- migrations leave it alone; src/db/subscriptions.api.test.ts proves it.
CREATE FUNCTION "subscription_usage"(p_space_id integer, p_customer_id integer, p_today date, p_week_start date)
RETURNS TABLE ("subscription_id" integer, "customer_id" integer, "usage_based" boolean,
               "days_used" integer, "days_this_week" integer, "minutes_used" integer,
               "minutes_today" integer, "due_agorot" integer)
LANGUAGE sql STABLE AS $$
  SELECT s."id", s."customer_id", s."billing" <> 'FIXED',
         count(DISTINCT c.day)::integer,
         count(DISTINCT c.day) FILTER (WHERE c.day >= p_week_start AND c.day <= p_today)::integer,
         coalesce(sum(c.minutes), 0)::integer,
         coalesce(sum(c.minutes) FILTER (WHERE c.day = p_today), 0)::integer,
         CASE s."billing"
           WHEN 'FIXED' THEN s."price_agorot"
           WHEN 'PER_DAY' THEN count(DISTINCT c.day)::integer * s."price_agorot"
           ELSE round(coalesce(sum(c.minutes), 0) * s."price_agorot" / 60.0)::integer
         END
  FROM "subscriptions" s
  LEFT JOIN LATERAL (
    SELECT ("ci"."checked_in_at" AT TIME ZONE 'Asia/Gaza')::date AS day,
           CASE WHEN "ci"."checked_out_at" IS NULL THEN NULL
                ELSE floor(extract(epoch FROM "ci"."checked_out_at" - "ci"."checked_in_at") / 60)::integer
           END AS minutes
    FROM "check_ins" "ci" WHERE "ci"."subscription_id" = s."id"
  ) c ON true
  WHERE s."space_id" = p_space_id AND (p_customer_id IS NULL OR s."customer_id" = p_customer_id)
  GROUP BY s."id";
$$;
```
- **Rules it holds** (each a new data-model line, §13 Q4): a day is used by any check-in on it; minutes count
  closed stays only, each its whole minutes; a per-hour due is minutes × rate ÷ 60, rounded half up (`round`
  on numeric), as a visit's per-minute charge; a per-day due is days × rate.
- **Who reads it:** `subscriptions` (states, progress, warnings) and `payments` (balances, debts) — each in
  its own repository by `$queryRaw`. No TypeScript copy of the due exists.
- **The function names no index:** `check_ins_subscription_id_checked_in_at_idx` serves the lateral join;
  `subscriptions_space_id_ends_on_idx` the space's rows.

### D4 — the customers list (composed by `desk`, conventions §5, §9)
1. **The current subscription** of a customer (`subscriptions/currentSubscription.ts`, pure): of their
   subscriptions, the first by status rank (`ACTIVE` and `ENDING_SOON` 0, `UPCOMING` 1, `EXPIRED` 2), then
   the latest `startsOn` (none last), then the highest id. The row's `status` and `kind` are its; a customer
   with none has `current: null` (kind `NONE`). *Why:* two actives are allowed (decision 2); the row shows the
   one that is running.
2. **`status`/`kind`/`packageId` → ids:** `subscriptions.customerIdsBy(spaceId, filter, now)`: one query (the
   function joined to the space's subscriptions: id, customer, package, dates, end, totals, usage), the pure
   status and current rules in TypeScript, the matching customers' ids. `kind=NONE` answers the ids **with**
   a subscription, applied as an exclusion. *Cost:* one compact row per subscription of the space, read into
   memory when a status or kind filter is asked (§5 S10; alternative A1).
3. **`payment` → ids:** `payments.customerIdsByPayment(spaceId, 'OWES' | 'CREDIT', now)`: one SQL query (D5),
   only the ids; `SETTLED` is an exclusion of both.
4. **The page:** `customers.page(spaceId, { q, archived, include: number[][], exclude: number[] }, page)` —
   raw SQL, each id list **one array parameter** (`"id" = ANY(${ids}::integer[])`), so no bind-parameter limit
   (finding 113's cause); then the count; ordered by `name`, then `id`. `q`: `searchTermsOf(q)`
   (`customers/customerSearch.ts`, pure): digits only after removing spaces and `+` and at least two →
   `regexp_replace("phone", '\D', '', 'g') LIKE '%' || digits`; else `masaha_search_text("name") LIKE '%' ||
   masaha_search_text(q) || '%'` (the directory's function, data model › Search).
5. **The rows:** for the page's ids only, `subscriptions.currentOf(spaceId, ids, now)` and
   `payments.customerBalances(spaceId, ids, now)`.
- **Archived:** excluded unless `status=ARCHIVED`, which lists only them (the owner's).

### D5 — balances in SQL (`payments`, decision 6)
One query shape in `payments.repository.ts` (`$queryRaw`), the items of a space:
```sql
WITH items AS (
  SELECT 'SUBSCRIPTION' AS kind, u.subscription_id AS id, u.customer_id, u.due_agorot AS due,
         u.usage_based, s.created_at
  FROM subscription_usage(${spaceId}, ${customerId}, ${today}::date, ${weekStart}::date) u
  JOIN subscriptions s ON s.id = u.subscription_id
  UNION ALL
  SELECT 'VISIT', v.id, v.customer_id, v.charge_agorot, false, v.created_at
  FROM visits v
  WHERE v.space_id = ${spaceId} AND v.customer_id IS NOT NULL AND v.checked_out_at IS NOT NULL
    AND v.written_off_at IS NULL AND (${customerId}::integer IS NULL OR v.customer_id = ${customerId})
), paid AS (
  SELECT visit_id, subscription_id, sum(amount_agorot)::integer AS paid
  FROM payments WHERE space_id = ${spaceId} AND voided_at IS NULL GROUP BY visit_id, subscription_id
)
SELECT … FROM items i LEFT JOIN paid p ON (i.kind = 'VISIT' AND p.visit_id = i.id)
                                        OR (i.kind = 'SUBSCRIPTION' AND p.subscription_id = i.id)
```
- `customerBalances(spaceId, customerIds, now)` → per customer `debt = Σ greatest(due − paid, 0)`,
  `credit = Σ greatest(paid − due, 0) FILTER (WHERE usage_based)`, for `customer_id = ANY(ids)`.
- `customerIdsByPayment(spaceId, 'OWES' | 'CREDIT', now)` → the same aggregate, `HAVING` debt > 0 (credit > 0).
- `itemBalances(spaceId, customerId, now, tx?)` → each item `{ kind, id, dueAgorot: number | null, paidAgorot,
  balanceAgorot: number | null, createdAt }`, ordered `created_at, kind ('VISIT' first), id` — the file's rows
  and the allocation's order (D7). An unpriced visit has no due and no balance, and is never debt.
- **The balance stays one rule** (`balance.ts`, due − paid): the SQL applies the same subtraction; T-PR1-24
  pins that the file's balances equal `balanceOf` on the same rows (Review Focus).
- **It reads `visits`' and `subscriptions`' columns and `subscriptions`' function, never writes** — the
  owner's decision 6, an exception to "only read models read other modules' tables" stated in conventions §9
  (§5 S9). It needs DESK PR 4's `visits.written_off_at` (§12.1).

### D6 — a subscription's payment (`POST …/payments`, PR 2)
`receivePaymentSchema` gains `subscriptionId: id.optional()`; `visitId` becomes optional; a refinement:
exactly one (`required` on `visitId` when neither; `invalid_choice` on `subscriptionId` when both). The desk's
`receivePayment` branches after its common opening (DESK PR 4's `lockAtDesk(…, 'payments.record')`):
1. `subscriptions.lockIn(space.id, subscriptionId, tx)` (`FOR UPDATE`; not the space's → 422 `invalid_choice` on
   `subscriptionId`).
2. `payments.findByKey(space.id, key, tx)`: for another item → 409 (no code); for this subscription → the first
   payment, sums as of now (DESK PR 4's S5).
3. `payments.record(tx, { …, subscriptionId })`: the trigger refuses above a fixed price (`PAYMENT_EXCEEDS_DUE`);
   a usage-based subscription takes any amount (credit).
4. Its balance from `payments.itemBalances` (the item), answered `{ visit: null, subscription, payment,
   paidAgorot, balanceAgorot }`. No phone rule: a subscription always has its customer. An ended, expired or
   archived customer's subscription takes payments (its debt is still owed).
- `payments.recordForVisit` becomes `record(payment: NewPayment, tx)` with `item: { visitId } | { subscriptionId }`;
  audited `payment.recorded`, `after: { visitId | subscriptionId, amountAgorot, method }`.

### D7 — subscribing and renewing (`desk.subscribe`, PR 2)
In one transaction, in this order:
1. `lockAtDesk(actor, space, tx, 'subscriptions.manage')`.
2. `subscriptions.findByKey(space.id, key, tx)` → a retry: the first subscription (state as of now), its
   payments by their derived keys (S6: `payments.findByKeys(space.id, derivedKeys(key), tx)`), the debt as of
   now, warnings as of now; 201.
3. `customers.findIn(space.id, customerId, tx)` → none: 404; archived: 409 `CUSTOMER_ARCHIVED`.
4. `renewalOfId`: `subscriptions.lockIn(…)`; not this customer's: 422 `invalid_choice` on `renewalOfId`; already
   renewed (`renewedById` set): 409 `SUBSCRIPTION_ALREADY_RENEWED` (the unique key the backstop).
5. Terms: `packageId` → `packages.termsOf(space.id, packageId, tx)` (not the space's, or retired: 422
   `invalid_choice` on `packageId`), `priceTyped` none; `custom` → `can(actor, 'prices.typeByHand', { links,
   receptionMayTypePrices })` else 403 `PRICE_TYPING_NOT_ALLOWED`; `priceTyped` the actor with the reason.
6. Dates: `startsOn = request.startsOn ?? proposedStart(renewed, today)` (`subscriptions/renewal.ts`, pure: the
   renewed one's `endsOn + 1` while its status is not `EXPIRED` and it has an end not before today, else today);
   a package's `endsOn = addDays(startsOn, validityDays − 1)`; a custom one's `endsOn` as sent, none allowed; an
   `endsOn` before `startsOn`: 422 `out_of_range` on `endsOn`.
7. `subscriptions.create(actor.id, { …, key, renewalOfId }, tx)`, audited `subscription.created` (`after`: the
   terms, `packageId`, `renewalOfId`, `reason`).
8. **The payment, if any:** `payments.itemBalances(space.id, customerId, now, tx)` — the customer's older items
   with a balance above zero, oldest first (D5's order), the new subscription last; `allocate(amount, items)`
   (`payments/allocation.ts`, pure: each item `min(rest, balance)`, the rest to the new subscription, which
   takes it whole); at most `ALLOCATION_MAX_ITEMS = 50` items, the 49 oldest debts and the new one. One
   `payments.record` per part, in that order, key `derivedKey(key, index)`; the trigger locks each item's row
   as it goes (conventions §13's order: oldest first). A rest above a fixed new price: the trigger's
   `PAYMENT_EXCEEDS_DUE`, the whole request undone.
9. **Warnings:** `CUSTOMER_HAS_DEBT` when an item older than the new subscription still has a balance above zero
   after the payments (ADR 0010 rule 7). The answer: `NewSubscription`, 201.

### D8 — corrections (`subscriptions`, PR 2)
- **Limits and dates** (`PATCH`, staff): under the space's lock, `can('subscriptions.manage')` on the links
  under it; `lockIn` (404); ended → 409 `SUBSCRIPTION_ENDED`; the change by `subscriptionChange` (pure, as
  `packageChange`: only the fields set to a new value; `null` clears a limit or the end); the dates checked
  (`endsOn ≥ startsOn`, 422 `out_of_range`); nothing changed → nothing written; audited
  `subscription.corrected` (`before`/`after`: the changed fields).
- **Price and billing** (`PUT …/price`, owner): the same opening with `subscriptions.correctPrice`; ended →
  `SUBSCRIPTION_ENDED`; the same billing and price → nothing written; else `billing`, `priceAgorot`,
  `priceSetById = actor`, `priceReason = reason`; audited `subscription.priceCorrected` (`before`: `{ billing,
  priceAgorot }`, `after`: the same with `reason`). A fixed price below the non-voided payments: the trigger
  (S2), `PRICE_BELOW_PAID`.
- **Not correctable:** the name, the audience, the shift, the package (alternative A3 if the owner wants the name).

### D9 — PR 2's migration `subscription_terms`
Prisma's part (from the schema): `idempotencyKey String @map("request_id") @db.Uuid` with
`@@unique([spaceId, idempotencyKey])`; `priceReason String? @map("price_reason")`; `renewalOfId Int?
@unique @map("renewal_of_id")` with `renewalOf Subscription? @relation("SubscriptionRenewal", fields:
[renewalOfId, customerId], references: [id, customerId], onDelete: NoAction)` and `renewedBy Subscription?
@relation("SubscriptionRenewal")`. The raw SQL appended:
```sql
-- Existing rows (the demo seed's) get a key of their own before the column is required.
UPDATE "subscriptions" SET "request_id" = gen_random_uuid() WHERE "request_id" IS NULL;
ALTER TABLE "subscriptions" ALTER COLUMN "request_id" SET NOT NULL;
-- A typed price's reason comes with who typed it, and is never blank (data model › Hand-typed prices).
UPDATE "subscriptions" SET "price_reason" = 'Typed before reasons were recorded'
  WHERE "price_set_by_id" IS NOT NULL AND "price_reason" IS NULL;
ALTER TABLE "subscriptions" ADD CONSTRAINT "subscriptions_price_reason_check" CHECK (
  ("price_set_by_id" IS NULL) = ("price_reason" IS NULL)
  AND ("price_reason" IS NULL OR btrim("price_reason") <> ''));
-- Finding 80: no package and no subscription is free.
ALTER TABLE "packages" DROP CONSTRAINT "packages_price_check";
ALTER TABLE "packages" ADD CONSTRAINT "packages_price_check" CHECK ("price_agorot" > 0);
ALTER TABLE "subscriptions" DROP CONSTRAINT "subscriptions_price_check";
ALTER TABLE "subscriptions" ADD CONSTRAINT "subscriptions_price_check" CHECK ("price_agorot" > 0);
-- The ledger (ADR 0010 rule 4): a fixed price never falls below what was paid on it; only a usage-based
-- subscription holds credit. The insert trigger guards payments; this guards the price.
CREATE FUNCTION "subscriptions_guard_price"() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE paid bigint;
BEGIN
  IF NEW."billing" = 'FIXED' THEN
    SELECT COALESCE(sum("amount_agorot"), 0) INTO paid FROM "payments"
      WHERE "subscription_id" = NEW."id" AND "voided_at" IS NULL;
    IF paid > NEW."price_agorot" THEN
      RAISE EXCEPTION 'subscriptions_price_below_paid: % agorot paid exceeds the price %', paid, NEW."price_agorot"
        USING ERRCODE = 'check_violation', TABLE = 'subscriptions', CONSTRAINT = 'subscriptions_price_below_paid';
    END IF;
  END IF;
  RETURN NEW;
END;
$$;
CREATE TRIGGER "subscriptions_guard_price" BEFORE UPDATE OF "billing", "price_agorot" ON "subscriptions"
  FOR EACH ROW EXECUTE FUNCTION "subscriptions_guard_price"();
```
- **Why the backfill text is English:** it is never shown as a reason a user typed; the two dev rows are the
  seed's, and the seed is changed to give its own reasons (production holds no subscription: no route wrote one).
- `constraintCodes.ts`: `subscriptions_price_below_paid → { type: 'conflict', code: 'PRICE_BELOW_PAID' }`.

### D10 — ending early (`subscriptions`, PR 2)
Under the space's lock and `can('subscriptions.manage')`; `lockIn` (404); already ended → answered as it is,
nothing written; else `endedAt = now`, `endedById = actor`, `endsOn = max(today, startsOn ?? today)` (never
later than it was: `min(that, endsOn)` when it has one, but never before `startsOn`); audited
`subscription.ended` (`before: { endsOn }`, `after: { endsOn, endedAt }`). No payment, no refund, no
proration; an open check-in on it stays open. **The status:** an ended subscription is `EXPIRED` at once (S5).

### D11 — subscription check-ins (`desk`, PR 3)
**Check-in** (`checkInSubscriber`), in one transaction, the visit's order (decision 9):
1. `lockAtDesk(actor, space, tx, 'attendance.record')`; `now`.
2. `subscriptions.findCheckInByKey(space.id, key, tx)` → a retry: that check-in, its warnings as of now
   computed **without it** (its own day and minutes left out, so the same warnings answer twice), 201.
3. `subscriptions.lockIn(space.id, subscriptionId, tx)` → none: 422 `invalid_choice` on `subscriptionId`.
4. `customers.findIn` → archived: 409 `CUSTOMER_ARCHIVED`.
5. Present: an open check-in or an open visit of the customer (`occupancy.isPresent(space.id, customerId,
   tx)`, D12) → 409 `MEMBER_ALREADY_CHECKED_IN` (the partial unique index the backstop for check-ins).
6. Warnings: `occupancy.checkInWarnings(space.id, now, tx)` (`SPACE_FULL`, `OUTSIDE_OPENING_HOURS`), then
   `subscriptionWarnings(state, today)` (`subscriptions/limits.ts`, pure): `UPCOMING` →
   `SUBSCRIPTION_NOT_STARTED`; `EXPIRED` → `SUBSCRIPTION_EXPIRED`; `daysPerWeek` and `daysThisWeek ≥
   daysPerWeek` with no check-in today yet → `DAYS_PER_WEEK_USED`; `hoursPerDay` and `minutesToday ≥
   hoursPerDay × 60` → `HOURS_PER_DAY_USED`.
7. `subscriptions.checkIn(actor.id, { spaceId, key, customerId, subscriptionId, checkedInAt: now }, tx)`,
   audited `checkIn.checkedIn` (`after: { subscriptionId, customerId }`). 201 `DeskCheckIn`.

**Check-out** (`checkOutSubscriber`): `lockAtDesk(…, 'attendance.record')`; `subscriptions.lockCheckInIn(space.id,
checkInId, tx)` (`FOR UPDATE`; not the space's → 404); closed → answered as it is, nothing written; else
`checkedOutAt = now`, `MANUAL`, audited `checkIn.checkedOut` (`after: { checkedOutAt }`). The answer adds the
subscription's due, paid and balance (`payments.itemBalances`), so a usage-based subscriber's desk shows what
the stay cost; the payment is `POST …/payments` (D6). No key: an update is idempotent by design.

**The lists** (`subscriptions`): `open=true` → the space's open check-ins, the earliest first, whole (bounded by
who is present; §4's exceptions gain it); `from`/`to` → check-ins whose Gaza check-in date is in the range,
latest first then id desc, paged. Each with its customer's name (`customers.namesOf`) and its subscription's
state.

### D12 — *present*, once (`occupancy/present.ts`, PR 3)
- `presentIn(spaceId, tx?)` → `{ visits: OpenVisit[]; checkIns: OpenCheckIn[]; count }` — the read's people and
  the warnings' count; `presentCountsIn(spaceIds)` → `Map` — the directory's; `isPresent(spaceId, customerId,
  tx)` — the check-in's refusal. **The definition** (open visits plus open subscription check-ins, of the
  space) is written once, in this file's comment and its two sources; `occupancy.service.ts`'s `peopleIn`,
  `liveStatusFor` and `checkInWarnings` call it, and no other count of *present* remains.

### D13 — the status and progress rules (`subscriptions`, pure, PR 1)
`subscriptionStatus(s, usage, today)` (`subscriptions/subscriptionStatus.ts`), in this order:
1. `ended` → `EXPIRED` (S5);
2. `startsOn > today` → `UPCOMING` (S4);
3. `endsOn < today`, or `totalDays` and `daysUsed ≥ totalDays`, or `totalHours` and `minutesUsed ≥ totalHours × 60`
   → `EXPIRED`;
4. ending soon, whichever comes first: an end date with `endsOn − today ≤ 7` days — except a subscription of at
   most 7 days by its dates, which is ending soon on its last day only (§13 Q5); or `totalDays` with
   `totalDays − daysUsed ≤ 20 % of totalDays`; or `totalHours` with `totalHours × 60 − minutesUsed ≤ 20 % of it`
   → `ENDING_SOON`;
5. else `ACTIVE` (no end and no total: active until ended).
- `progressOf(usage)`: the four counts as the function answers them. **Gaza:** `today = gazaClockOf(now).date`,
  `weekStart = weekStartOf(today)` (`core/gazaTime.ts`: the Saturday on or before), `addDays(date, n)` — pure,
  calendar-only, unit-tested in `packages/shared`.
- **Dates on the wire** are Gaza calendar dates (`YYYY-MM-DD`); a `@db.Date` is read with
  `toISOString().slice(0, 10)` and written as `new Date(date + 'T00:00:00Z')`, never through a zone
  (conventions §11).

### D14 — idempotency, locks, order and races
- **Keys** (ADR 0015 rule 4 done): customers (`request_id`, nullable — the desk's phone flow creates customers
  under another record's key), subscriptions (required), check-ins (exists), payments (exists; a renewal's derive
  theirs, S6). Each read first, under the space's lock (conventions §13, S1 of #95); the unique key the backstop.
- **Lock order:** the space's row; then the subscription's (`FOR UPDATE`, corrections, end, payment, a renewed
  one); then the items' rows in the allocation's order, oldest first (the payment trigger's `FOR UPDATE`); a
  check-in's row (check-out). The auto check-out takes a check-in's row only; the visit check-out an open
  visit's (never an allocation item, which is closed); so no two orders cross.

| Race | What decides | Test |
|---|---|---|
| Two desks renew one subscription | The space's lock; the second sees `renewedById` → `SUBSCRIPTION_ALREADY_RENEWED` | PR2 T22 |
| One key sent twice at once (subscribe, check-in, customer) | Read first under the lock | PR1 T4, PR2 T16, PR3 T5 |
| Two desks pay the same debt (one by renewal) | The lock; the second's `itemBalances` sees the first's payment | PR2 T21 |
| A payment while the owner lowers a fixed price | Price first → the insert's ceiling; payment first → the price trigger | PR2 T30, T31 |
| A check-in while a subscription is ended or corrected | The lock; the check-in's warnings read it as committed | PR3 T9 |
| A check-in while the customer is archived | The lock; `CUSTOMER_ARCHIVED` | PR3 T10 |
| A link ended while a write waits | `can()` on `linksUnder(tx)` | PR1 T9, T15; PR2 T8, T28; PR3 T8 |

### D15 — the code, PR by PR (interfaces; the commit in brackets)

`Now = { today: string; weekStart: string }` (from the one clock: `gazaClockOf(now()).date`, `weekStartOf(today)`).

**PR 1**
| Where | What |
|---|---|
| `customers/customers.repository.ts` | + `findByKey(spaceId, key, tx)`, `findIn(spaceId, id, tx?)`, `create(spaceId, { name, phone, key }, tx)` (the existing one gains `key?`), `update(id, data, tx)`, `setArchived(id, at: Date \| null, tx)`, `page(spaceId, { q, archived, include: number[][], exclude: number[] }, page): { rows, total }` (raw SQL, D4) [C1, C2, C5] |
| `customers/customers.service.ts` | deps `{ runInTransaction, audit, spaces, now }`; + `create(actor, space, key, request)`, `edit(actor, space, id, request)`, `restore(actor, space, id)` (each its transaction, the space's lock, `can()` under it); `findIn`, `archive(tx, actor, space, id)` (for `desk`), `page(…)` [C1, C2, C5] |
| `customers/customers.{controller,manage.routes,mapper}.ts` | `POST /customers` (`requireCan('customers.manage')` → `requireIdempotencyKey` → `validate`), `PATCH /customers/:customerId`, `POST /customers/:customerId/restore` (`requireCan('customers.archive')`); `toCustomer(row)` [C1, C2] |
| `subscriptions/subscriptions.repository.ts` | + `statesIn(spaceId, { customerId?, ids? }, now: Now, tx?)` → rows: the subscription's columns joined to `subscription_usage` [C3] |
| `subscriptions/subscriptions.service.ts` | + `statesOf(spaceId, { customerId?, ids? }, now: Date, tx?): Promise<SubscriptionState[]>`; `customerIdsBy(spaceId, { status?, kind?, packageId? }, now): Promise<{ include?: number[]; exclude?: number[] }>`; `currentOf(spaceId, customerIds, now): Promise<Map<customerId, SubscriptionState>>`; `openCheckInOf(spaceId, customerId, tx?)` [C3, C5] |
| `payments/payments.repository.ts`, `payments.service.ts` | + `customerBalances(spaceId, customerIds, now: Date, tx?): Promise<Map<number, CustomerBalance>>`; `customerIdsByPayment(spaceId, 'OWES' \| 'CREDIT', now): Promise<number[]>`; `itemBalances(spaceId, customerId, now, tx?): Promise<ItemBalance[]>`; `paymentsFor(spaceId, { visitIds?, subscriptionIds? }, tx?): Promise<ItemPayment[]>` [C4, C5] |
| `visits/visits.service.ts` | + `deskVisitsOf(spaceId, ids, tx?): Promise<DeskVisit[]>`; `openOf(spaceId, customerId, tx?)` [C5] |
| `desk/desk.service.ts` | + `archiveCustomer(actor, space, id)`; `customers(actor, space, query): { rows: CustomerRow[]; total }`; `customerFile(space, id): CustomerFile` [C2, C5] |
| `desk/desk.manage.routes.ts` | + `POST /customers/:customerId/archive` (`requireCan('customers.archive')`), `GET /customers` (`validate(customersQuerySchema, 'query')`), `GET /customers/:customerId` [C2, C5] |
| `app.ts` | `customers` built with `runInTransaction`, `spaces`, `now`; `subscriptions` with `now`; `payments` with `subscriptions`, `now`; `desk` with `subscriptions`; the customers' manage router mounted [C1–C5] |

**PR 2**
| Where | What |
|---|---|
| `packages/packages.service.ts` | + `termsOf(spaceId, packageId, tx): Promise<PackageTerms & { id, validityDays, isActive } \| null>` [C2] |
| `subscriptions/subscriptions.service.ts` | + `findByKey(spaceId, key, tx)`, `lockIn(spaceId, id, tx)` (`FOR UPDATE`; `null` when not the space's), `create(actorId, NewSubscription, tx)` (audited), `correct(actor, space, id, request)`, `correctPrice(actor, space, id, request)`, `end(actor, space, id)` (each its transaction) [C2, C4, C6, C7] |
| `subscriptions/{renewal,subscriptionChange}.ts` | `proposedStart(renewed: SubscriptionState \| null, today): string`; `subscriptionChange(current, edit): { data, before, after }` [C4, C6] |
| `subscriptions/subscriptions.{controller,manage.routes}.ts` | `PATCH /subscriptions/:subscriptionId`, `PUT /subscriptions/:subscriptionId/price` (`requireCan('subscriptions.correctPrice')`), `POST /subscriptions/:subscriptionId/end` [C6, C7] |
| `payments/payments.service.ts`, `allocation.ts` | `record(payment: NewPayment, tx): Promise<VisitPayment>` (replaces `recordForVisit`); `findByKeys(spaceId, keys, tx)`; `allocate(amount, items: { item; balanceAgorot }[], last: item): { parts: { item; amountAgorot }[] }` [C3, C4] |
| `shared/http/idempotencyKey.ts` | + `derivedKey(key: string, index: number): string` [C4] |
| `desk/desk.service.ts` | + `subscribe(actor, space, customerId, key, request): Promise<{ result: NewSubscription; warnings }>`; `receivePayment` gains the subscription branch; `statement(space, id): Promise<SubscriptionStatement>` [C2–C5] |
| `desk/desk.manage.routes.ts` | + `POST /customers/:customerId/subscriptions` (`requireCan('subscriptions.manage')` → key → `validate(subscribeSchema)`), `GET /subscriptions/:subscriptionId` [C2, C5] |

**PR 3**
| Where | What |
|---|---|
| `occupancy/present.ts`, `occupancy.service.ts` | `presentIn`, `presentCountsIn`, `isPresent` (D12); the service's three readers call them [C1] |
| `subscriptions/subscriptions.service.ts`, `limits.ts` | + `findCheckInByKey`, `checkIn(actorId, NewCheckIn, tx)`, `lockCheckInIn(spaceId, id, tx)`, `checkOut(actorId, id, at, tx)`, `checkInsIn(spaceId, query, now)`; `subscriptionWarnings(state, { checkedInToday: boolean }): DomainErrorCode[]` [C2–C4] |
| `subscriptions/subscriptions.{controller,manage.routes}.ts` | + `GET /check-ins` (`validate(checkInsQuerySchema, 'query')`) [C4] |
| `desk/desk.service.ts`, routes | + `checkInSubscriber(actor, space, key, request)`, `checkOutSubscriber(actor, space, checkInId)`; `POST /check-ins`, `POST /check-ins/:checkInId/check-out` (`requireCan('attendance.record')`, the first with the key) [C2, C3] |

---

## 5. Stronger decisions, and Proposed alternatives

### S1 — attendance and the amount due computed by one database function — **recommended, planned**
*What:* `subscription_usage` (D3) is the only place a subscription's days, minutes and due are counted; the
status and progress rules stay pure TypeScript on its counts. *Why:* decision 6 puts debts in the database, and a
usage-based debt is attendance × rate, so attendance must be countable there; one function serves the list,
the file, the statement, the warnings and the debts, so no second copy exists. The directory's search
functions are the precedent (data model › Search). *Cost:* conventions §8's *Pure rules* line for "the amount
due" changes to "a database function owned by `subscriptions`"; its branches are proven in the API lane, not the
unit lane; PostgreSQL's zone data reads Gaza dates for days used (finding 120). *Alternative A1* goes further.

### S2 — a fixed price never below what was paid, in a trigger — **recommended, planned**
The ledger's "never above the amount due" (conventions §13) is the database's; an update of the price is a way
round the insert trigger. A trigger on `subscriptions` closes it, with its own constraint and code. *Cost:* one
trigger, one translation line, one db test, one code.

### S3 — a subscription is renewed at most once — **recommended, planned**
`renewal_of_id` unique, the same customer's. Two desks renewing one subscription at once would otherwise make two
renewals with two keys. *Cost:* one column, one code. The statement's `renewal` and `renewedById` come from it.

### S4 — an `UPCOMING` status — **recommended, planned**
A renewal starting after today is not "active" yet; the data model's three statuses would call it active, and the
desk's "preselect when only one is active" (decision 2) would see two. *Cost:* one status, one warning
(`SUBSCRIPTION_NOT_STARTED`, the date range limit's), the data model's *Subscription status* gains it.
*Alternative A4:* none (a future start only warns at check-in).

### S5 — an ended subscription is `EXPIRED` at once — **recommended, planned**
The data model moves its end to today, which keeps it *ending soon* until midnight; decision 5 says ending changes
the status. *Cost:* one branch, one data-model line.

### S6 — a renewal's payments derive their keys from the request's — **recommended, planned**
`derivedKey(key, index)` (`shared/http/idempotencyKey.ts`: SHA-256 of `key/index`, formatted as a UUID) for each
part, in the allocation's order. A retry finds the subscription by its key, then its payments by the derived keys
(at most 50, one query). *Why:* the ledger's key is unique per payment and stays so; no column is added to an
append-only table whose trigger lists its columns. *Alternative A6:* a `group_key` on payments.

### S7 — retries answer the warnings, sums and debt as of now — **weakens ADR 0015's "same body", stated**
As #95's warnings (S3) and DESK PR 4's sums (S5): the records are the first ones; the advice and the money
describe now. A check-in's limit warnings leave the check-in itself out, so they answer the same twice.

### S8 — finding 80 folded into PR 2's migration — **recommended, planned**
The front desk's migration is the one the finding names; subscriptions get the same rule (no free subscription;
the API already refuses 0).

### S9 — `payments`' balance query reads `visits`' and `subscriptions`' data — **a rule touched, stated**
Conventions R7 lets only the read models read other modules' tables. Decision 6 gives the aggregate query to the
module that owns the balance; it reads, never writes, and reads a subscription's due only through its owner's
function. Conventions §9's *Composed reads* gains the line.

### S10 — the status and kind filters read one compact row per subscription — **weaker than decision 6's reason, stated**
The status is a pure TypeScript rule (conventions §8), so the filter evaluates it on the space's subscriptions
(id, customer, package, dates, totals and counts: one query). It grows with the subscriptions, not with
payments or check-ins, and its ids reach the customers' query as one array parameter. *Alternative A1* removes it.

### S11 — a present customer is not archived — **recommended, planned**
An archived customer at the desk could not check out by the list; `MEMBER_ALREADY_CHECKED_IN` refuses it.

### Rules the item touches, stated
- **ADR 0009's table** gains: "Edit a customer | ✓ | ✓"; "Archive or restore a customer | – | ✓" (PR 1);
  "Correct a subscription's limits and dates; end it early | ✓ | ✓"; "Correct a subscription's price or
  billing, with a reason | – | ✓" (PR 2) — each with a *Revised* line (`<date>, #PRNUM`).
- **ADR 0015 rule 4** is done: a *Revised* line (PR 2): "customers and subscriptions carry the key; a renewal's
  payments derive theirs".
- **api-contract §4's exceptions** gain: the customer file's lists, the statement's check-ins and payments
  (bounded by one customer, one subscription), the open check-ins (bounded by who is present).
- **The level map** is unchanged; `@masaha/shared` gains `customers` (L2) and `subscriptions` (L3).

### Proposed alternatives (the owner may prefer them)
- **A1 — the status in SQL too.** A function `subscription_status(…, today)` beside `subscription_usage`, so the
  status filter is computed in the database (S10 gone). *Cost:* the status rule leaves TypeScript (conventions
  §8), its branches proven only in the API lane. **Not recommended:** the status is the rule the web will want to
  show too, and the filter's read is bounded by subscriptions.
- **A2 — one `PATCH` for every correction**, the service refusing reception's price with a new code. Not
  recommended (D1).
- **A3 — the name correctable** by the staff in the `PATCH`. Cheap; the owner's call.
- **A4 — no `UPCOMING`** (S4 not taken).
- **A5 — the subscriber's check-out takes a payment** in its body (one request at the desk, a key). Not
  recommended: `POST …/payments` already does it; two routes for one payment.
- **A6 — a `group_key` column on payments** instead of derived keys (S6). Not recommended: the append-only
  trigger's column list changes, and a ledger column for a request's sake.

---

## 6. Related findings

| Finding | Folded? | Why, and the cost |
|---|---|---|
| **80** The database still takes a package with a price of zero | **Yes, PR 2 C1** (S8) | The migration the finding names; + subscriptions. Status → Resolved, resolution line, index moved |
| **113** (DESK PR 4's, expected: the uncollected read grows with every auto-closed visit; #97 review 7) | **Proposed, PR 1 C6** (§13 Q9) | PR 1 builds the balance in SQL; `uncollectedIn` can page in one query on it, removing the `notIn` list. *Cost:* ≈ 4 files (`payments.repository.ts`, `payments.service.ts`, `visits` loses `autoClosedIn`/`autoClosedPage`'s `notIn`), the existing tests unchanged as its proof. Not folded unless the owner says |
| **111** (DESK PR 4's, expected: one helper for *present*; #95 nit 7) | **Yes, PR 3 C1** (decision 10) | D12. Status → Resolved |
| **112** (DESK PR 4's, expected: a key that closed a visit unpaid is not remembered) | No | A visit's rule; PR 2's keys are read by their own record |
| **97** The visit-rounding rule is written twice | No | Settings validation; untouched |
| **77** The race helper counts any waiting backend | No | The new races use `whileHeld` / `waitingOnLock` as the existing ones do |
| **84** A person cannot work at two spaces' front desks | No | Untouched |
| **120** (new) Gaza dates are read by two zone databases | Recorded, PR 1 C3 | `subscription_usage` dates check-ins with PostgreSQL's zone data, the rest of the API with Node's (conventions §11). Both lag Palestine's decrees alike, but they can lag differently: a check-in in the hour around midnight on a transition night could count on a different day in the two. *Resolves when:* both read one source, or a test pins one transition in PostgreSQL as U2 of #94 does in Node |

The numbers 111–113 are DESK PR 4's expected ones (its approval note); §12.1 reads the merged index and uses the
real numbers.

---

## 7. The files it edits

Only `apps/api`, `packages/shared`, `docs`, and the two web catalogues' error lines (worker B's licence). No
dependency. **Shared with worker A's OWNER_SETUP:** documents only (header note).

| PR | Code (new +) | Documents |
|---|---|---|
| 1 | `schema.prisma` (`Customer.idempotencyKey`); + 2 migrations; `db/front-desk.api.test.ts`, `db/subscriptions.api.test.ts`; shared: `core/gazaTime.ts` (+ test), `core/fields.ts` (`dateSchema`, + test), `core/errors.ts`, + `customers/{requests,responses,index}.ts` (+ test), + `subscriptions/{requests,responses,index}.ts`, `desk/{requests,responses}.ts` (+ test), `payments/responses.ts`; web: 2 catalogues; api: `shared/auth/{can,can.unit.test}.ts`; `customers/` `customers.{service,repository}.ts`, `index.ts`, + `customerSearch.ts` (+ test), + `customers.{controller,manage.routes,mapper}.ts`, + `customers.api.test.ts`; `subscriptions/` `subscriptions.{service,repository}.ts`, `index.ts`, + `subscriptionStatus.ts` (+ test), + `currentSubscription.ts` (+ test), + `subscriptions.mapper.ts`; `payments/payments.{service,repository}.ts`, `payments.mapper.ts`, + `balances.api.test.ts`; `visits/visits.service.ts` (`deskVisitsOf`, `openOf`); `desk/desk.{service,controller,manage.routes}.ts`, + `desk/customers.api.test.ts`, + `desk/customerFile.api.test.ts`, + `desk/archive.api.test.ts`; `app.ts` | `api-contract.md`, `data-model.md`, `conventions.md`, `security.md`, ADR 0009, + `features/customers.md`, + `features/subscriptions.md`, `features/desk.md`, `features/payments.md`, `docs/README.md`, `plans/v1-mvp.md`, `project/overview.md`, + finding 120, findings index — ≈ 42 |
| 2 | `schema.prisma`; + migration; `db/subscriptions.api.test.ts`, `db/payments.api.test.ts`, `db/seed/demo.ts`, `test/factories.ts`; shared: `core/errors.ts`, `subscriptions/{requests,responses}.ts` (+ test), `desk/{requests,responses}.ts` (+ test), `payments/requests.ts`?; web: 2 catalogues; api: `shared/auth/{can,can.unit.test}.ts`, `shared/http/idempotencyKey.ts` (+ `idempotencyKey.unit.test.ts`), `shared/errors/constraintCodes.ts`; `packages/packages.{service,repository}.ts` (`termsOf`); `subscriptions/` service, repository, mapper, + `renewal.ts` (+ test), + `subscriptionChange.ts` (+ test), + `subscriptions.{controller,manage.routes}.ts`, + `corrections.api.test.ts`, + `end.api.test.ts`; `payments/` service, repository, + `allocation.ts` (+ test); `desk/desk.{service,controller,manage.routes}.ts`, + `desk/subscribe.api.test.ts`, + `desk/renewal.api.test.ts`, + `desk/statement.api.test.ts`, `desk/payments.api.test.ts`; existing tests whose exact answers change (check 6); `app.ts` | `api-contract.md`, `data-model.md`, `conventions.md`, `security.md`, ADR 0009, ADR 0015, `features/{subscriptions,desk,payments,packages}.md`, `plans/v1-mvp.md`, `project/overview.md`, finding 80, index — ≈ 52 |
| 3 | + `occupancy/present.ts`, `occupancy/occupancy.service.ts`, `occupancy/present.api.test.ts`; shared: `core/errors.ts`, `subscriptions/{requests,responses}.ts` (+ test), `desk/responses.ts`; web: 2 catalogues; api: `subscriptions/` service, repository, + `limits.ts` (+ test), controller, routes, + `checkIns.api.test.ts`; `desk/desk.{service,controller,manage.routes}.ts`, + `desk/subscriberCheckIn.api.test.ts`, + `desk/subscriberCheckOut.api.test.ts`; `app.ts` | `api-contract.md`, `data-model.md`, `conventions.md`, `security.md`, `features/{occupancy,subscriptions,desk}.md`, `plans/v1-mvp.md`, `project/overview.md`, finding 111, index — ≈ 38 |

Over about 70 in one PR → stop and ask.

---

## 8. Design issues

No screen is built. The API follows the prototype's filters and the decisions K3, K4, K5, DK-007, DK-008, DK-010,
DK-013, DK-014, DK-020 (not built), DK-022, DK-023. Two points for the screens' items, not findings: the prototype's
`subStatus` knows no upcoming subscription (S4), and its per-hour due rounds an open stay up (`Math.ceil`), where
this plan counts closed stays' minutes (§13 Q4).

---

## 9. Tests — lane, title, the break each catches

Every test is seen failing first in its own lane; every expectation is written by hand. A fixed clock through
`createTestApp({ clock })`; instants with their offset (`stay()`); Gaza dates as strings. Roles in each API file:
the owner, reception of this space, a stranger, an owner of another space, the admin (testing §4). B-numbers are
§12.5's breaks, each run once, its red lines recorded.

### PR 1
**Unit**
- U1 `core/gazaTime.unit.test.ts`: `addDays crosses a month, a year and a leap day`; `weekStartOf answers the
  Saturday on or before, a Saturday itself` — B1: the week from Sunday (`(dayOfWeek + 7) % 7`).
- U2 `core/fields.unit.test.ts`: `a date is YYYY-MM-DD and exists` (`2026-02-30` refused) — B2: a regex only.
- U3 `customers/customerSearch.unit.test.ts`: `digits only, two or more, search the phone; anything else the
  name` (`'05 99'` digits, `'5'` name, `'سارة 1'` name) — B3: one digit counts.
- U4 `subscriptions/subscriptionStatus.unit.test.ts`, one test per branch of D13: ended; upcoming; past its end;
  total days used; total hours used; 7 days left → ending soon, 8 → active; a 7-day subscription only on its last
  day; 20 % of days left; 4 of 20 hours left (scenario 4); no end and no total → active — B4–B9: each branch
  removed or two swapped (the order: ended before upcoming, B5).
- U5 `subscriptions/currentSubscription.unit.test.ts`: `a running one before an upcoming before an expired; the
  latest start among equals; none → null` — B10: by id only.
- U6 `customers/requests.unit.test.ts`: `a name 1–60, a phone normalised or invalid_format; an edit may clear the
  phone` — B11: `phone: phoneSchema` without `.nullable()` on the edit.
- U7 `desk/requests.unit.test.ts`: `the list's filters take their lists only; packageId with kind CUSTOM or NONE is
  invalid_choice` — B12: the refinement removed.
- U8 `can.unit.test.ts`: `customers.archive: the space's owner only` (six actors) — B13: `'staff'`.

**API — `db/subscriptions.api.test.ts`** [C3]
- D1 `subscription_usage counts the days with a check-in, open or closed, once each, by Gaza date` (two stays on
  one Gaza day; one at 23:30 UTC that is the next Gaza day) — B14 (database): `::date` without `AT TIME ZONE`.
- D2 `it counts closed stays' whole minutes, today's and this week's from the dates given` — B15 (database): the
  open stay's minutes counted (`now()`).
- D3 `the due: a fixed price; days × the day rate; minutes × the hour rate ÷ 60, half up` (90 min at 333 → 500) —
  B16 (database): `floor` for `round`.
- D4 `one customer's subscriptions only, when named; another space's never` — B17 (database): the space filter
  dropped.

**API — `customers/customers.api.test.ts`** [C1, C2]
- T1 `the staff create a customer with a name and a phone, audited customer.created` — B18: the audit removed.
- T2 `a phone another customer holds is refused 409 PHONE_TAKEN on phone; an archived customer's phone is free` —
  B19: `findByPhone` without `archivedAt: null` (→ refused wrongly) and B20: the check removed (→ 500 from P2002).
- T3 `a retry with the same key answers the first customer, 201, never a second` — B21: `findByKey` skipped.
- T4 `two requests with one key at once make one customer` (`waitingOnLock({ count: 2 })`) — B22: the space's
  lock removed from the create.
- T5 `refuses a missing or invalid key, and an invalid body, with 422 before anything is read` — B23:
  `requireIdempotencyKey` removed.
- T6 `owner and reception edit name and phone, audited customer.edited with only what changed; the same values
  write nothing` — B24: the no-change check removed.
- T7 `an edit to another customer's phone is PHONE_TAKEN; clearing the phone is allowed`.
- T8 `answers not_found to a stranger, another space's owner and the admin, on every route` — B25: the router
  mounted outside `manage`.
- T9 `a reception link ended while the create waits on the space's lock is refused 403, writing nothing`
  (`whileHeld`) — B26: `can()` on `space.links`.
- T10 `restore: the owner only (reception 403 before anything is read); a phone another holds now → PHONE_TAKEN;
  not archived → as it is` — B27: `requireCan('customers.archive')` removed.

**API — `desk/archive.api.test.ts`** [C2]
- T11 `the owner archives a customer, audited customer.archived; again → as it is` — B28: the "already" branch
  removed (a second audit).
- T12 `an owing customer is archived; a present one is refused MEMBER_ALREADY_CHECKED_IN` — B29: the present check
  removed.
- T13 `reception is refused 403 before the body is read` — covered by B13.
- T14 `an archived customer's edit is CUSTOMER_ARCHIVED` — B30: the archived check removed from the edit.
- T15 `an owner whose link ended while the archive waited is refused 403` — B31: `can()` on `space.links`.

**API — `payments/balances.api.test.ts`** [C4]
- T16 `a customer's debt is the sum of positive balances: a fixed subscription partly paid, a per-hour one by its
  minutes, an unpaid visit` (hand-computed agorot) — B32: `greatest(…, 0)` removed (credit offsets debt).
- T17 `credit is only a usage-based subscription's; a fixed one paid in full is settled` — B33: the
  `usage_based` filter removed.
- T18 `a voided payment counts for nothing; a written-off visit is no debt; an unpriced visit is no debt` — B34:
  `voided_at IS NULL` dropped; B35: `written_off_at IS NULL` dropped.
- T19 `the payment filter's ids: owes, in credit; another space's customers never` — B36: the space filter of
  `paid` dropped.
- T20 `itemBalances lists a customer's items oldest first, visits before subscriptions at the same instant` —
  B37: `ORDER BY id`.

**API — `desk/customers.api.test.ts`** [C5]
- T21 `the list pages the space's customers by name, with each one's current subscription, status, debt and
  credit` — B38: `current` by id only (the expired one shown).
- T22 `q finds a name with its hamza or ta marbuta folded, and a phone by its last digits` — B39: the name match
  without `masaha_search_text`.
- T23 `each filter applies before the page is cut: every page full, the total right` (status, kind, packageId,
  payment owes/credit/settled; `limit=1`, two pages) — B40: the payment filter applied to the page after it is
  fetched.
- T24 `kind NONE lists customers with no subscription; SETTLED those with no debt and no credit` — B41: the
  exclusions applied as inclusions.
- T25 `archived customers only under status ARCHIVED, the owner's; reception 403` — B42: the `can()` check
  removed.
- T26 `the ids reach the query as one parameter: 70,000 ids filter without error` (seeded by `generate_series`
  in one `INSERT … SELECT`; Review Focus if too slow — check 7) — B43: `{ in: ids }` through Prisma.

**API — `desk/customerFile.api.test.ts`** [C5]
- T27 `the file answers the customer, the debt and credit, each subscription's status, progress, due, paid and
  balance, the unpaid visits with their payments, voided ones marked` (exact keys) — B44: `voided` dropped from
  the payments query.
- T28 `who is present: an open check-in or an open visit, or none` — B45: the visit's side missing.
- T29 `another space's customer, and an unknown one, are not_found`.
- T30 `the file's balances equal balanceOf on its rows` (the pin of D5) — B46: the SQL subtracting `paid`
  twice.

### PR 2
**Unit**
- U1 `subscriptions/renewal.unit.test.ts`: `a running renewed one → the day after its end; expired or ended →
  today; no end → today` — B1: `endsOn` instead of `endsOn + 1`.
- U2 `payments/allocation.unit.test.ts`: `oldest first, each at most its balance, the rest to the new one; an
  amount below the first debt pays only it; nothing owed → all to the new one; 50 items at most` — B2: the
  newest first; B3: no `min` (an item overpaid).
- U3 `shared/http/idempotencyKey.unit.test.ts`: `a derived key is a UUID, the same for the same key and index,
  different for another index or key` — B4: the index left out of the hash.
- U4 `subscriptions/subscriptionChange.unit.test.ts`: `only the fields set to a new value; null clears` — B5:
  every sent field counted as changed.
- U5 `subscriptions/requests.unit.test.ts` / `desk/requests.unit.test.ts`: `subscribe takes exactly one of a
  package and custom terms; a custom price needs a reason; a payment names exactly one item` — B6: the
  refinements removed.
- U6 `can.unit.test.ts`: `subscriptions.correctPrice: the space's owner only` — B7: `'staff'`.

**API — `db/subscriptions.api.test.ts`, `db/payments.api.test.ts`** [C1]
- D1 `a typed price's reason comes with who typed it, never blank` — B8 (database): drop
  `subscriptions_price_reason_check`.
- D2 `a package and a subscription cost more than nothing` (finding 80) — B9 (database): the old `>= 0`
  constraints restored.
- D3 `a subscription is renewed once, by the same customer's` — B10 (database): drop the unique index on
  `renewal_of_id`.
- D4 `a fixed price never falls below what is paid: subscriptions_price_below_paid; usage-based may` — B11
  (database): drop the trigger.
- D5 `two subscriptions never share a key in a space` — B12 (database): drop the unique index.

**API — `desk/subscribe.api.test.ts`** [C2]
- T1 `a subscription from a package copies its terms, ending validityDays after its start, audited
  subscription.created` — B13: `addDays(startsOn, validityDays)` (one day too long).
- T2 `a retired package, or another space's, is invalid_choice on packageId` — B14: the `isActive` check removed.
- T3 `a custom subscription records who typed its price and why` — B15: `priceTyped` not stored.
- T4 `reception types a custom price only where the space allows it: 403 PRICE_TYPING_NOT_ALLOWED` — B16:
  `can('prices.typeByHand')` skipped.
- T5 `an archived customer is CUSTOMER_ARCHIVED; another space's or unknown customer not_found` — B17: the
  archived check removed.
- T6 `a retry with the same key answers the first subscription, 201; two at once make one` — B18: `findByKey`
  skipped; B19: the lock removed (the race).
- T7 `refuses a missing key, an invalid body, before anything is read`.
- T8 `a reception link ended while waiting is refused 403` (`whileHeld`) — B20: `can()` on `space.links`.
- T9 `the start date: the one sent; else today` and `endsOn before startsOn is out_of_range`.

**API — `desk/payments.api.test.ts`** [C3] (DESK PR 4's file, gaining)
- T10 `a payment on a subscription of the space is recorded, 201, with what remains` — B21: the subscription
  branch reading the visit's balance.
- T11 `a fixed subscription is never paid above its price: PAYMENT_EXCEEDS_DUE, writing nothing; a per-hour one
  takes credit` — B22: `PAYMENT_EXCEEDS_DUE`'s translation line removed (→ 500).
- T12 `exactly one item: both or neither refused 422` — covered by B6.
- T13 `another space's subscription is invalid_choice on subscriptionId; a key that paid a visit is a conflict`
  — B23: the item check of the key compares visits only.
- T14 `an ended subscription, and an archived customer's, still take a payment`.

**API — `desk/renewal.api.test.ts`** [C4]
- T15 `a renewal starts the day after the running one's end, or today once it expired` — B24: the proposal
  ignored (always today).
- T16 `an amount pays the older debts oldest first, one payment each, the rest to the new subscription;
  CUSTOMER_HAS_DEBT when one remains` (a visit debt 1,500, a subscription 5,000, a new 30,000; amount 4,000 →
  1,500, 2,500, 0) — B25: the allocation newest first; B26: the warning computed before the payments.
- T17 `a rest above a fixed new price is PAYMENT_EXCEEDS_DUE and nothing is written: no subscription, no
  payment` — B27: the payments recorded outside the transaction.
- T18 `a retry answers the same subscription and the same payments, their keys derived from the request's` —
  B28: `findByKeys` skipped (→ 500 on the unique key).
- T19 `the payments are audited each, payment.recorded, after subscription.created`.
- T20 `a renewal of another customer's subscription is invalid_choice on renewalOfId`.
- T21 `two desks paying one debt: the second, while waiting, sees the first's payment and pays only what is
  left` (`whileHeld`: a payment inserted meanwhile) — B29: `itemBalances` read before `lockAtDesk`.
- T22 `two renewals of one subscription: the second is SUBSCRIPTION_ALREADY_RENEWED` (`whileHeld`: the first
  renewal inserted meanwhile) — B30: the renewed check removed (the unique key then answers 500).

**API — `desk/statement.api.test.ts`** [C5]
- T23 `the statement answers the status, progress, due, paid, balance, its check-ins with their minutes and its
  payments, voided ones marked, whole` (scenario 1, hand-computed) — B31: an open check-in's minutes counted.
- T24 `a running subscription proposes its renewal's start; a renewed one answers renewedById and no proposal` —
  B32: `renewal` not cleared once renewed.
- T25 `another space's subscription is not_found`.

**API — `subscriptions/corrections.api.test.ts`** [C6]
- T26 `the staff correct limits and dates, audited subscription.corrected with only what changed; the same values
  write nothing` — B33: `subscriptionChange` replaced by the whole body.
- T27 `endsOn before startsOn is out_of_range; an ended subscription is SUBSCRIPTION_ENDED` — B34: the ended
  check removed.
- T28 `a reception link ended while the correction waits is refused 403` — B35: `can()` on `space.links`.
- T29 `the owner corrects the price and billing with a reason, recorded as the price typed, audited
  subscription.priceCorrected; reception 403 before the body is read` — B36: `requireCan('subscriptions.correctPrice')`
  removed (reception's invalid body then answers 422).
- T30 `a fixed price below what is paid is PRICE_BELOW_PAID, writing nothing` — B37: the translation line
  removed (→ 500).
- T31 `a payment that waited while the owner lowered the price is refused PAYMENT_EXCEEDS_DUE` (`whileHeld`:
  the price lowered meanwhile) — B38: the trigger's ceiling skipped for `subscription_id` (the payments
  migration's function, database break).

**API — `subscriptions/end.api.test.ts`** [C7]
- T32 `ending early sets the end to today, records who and when, audited subscription.ended; the money is
  unchanged; the status EXPIRED` — B39: `endsOn` left as it was.
- T33 `an upcoming one ends on its start; again → as it is, nothing audited` — B40: `endsOn = today` (the
  `CHECK` then answers 500).
- T34 `the staff end; a stranger and the admin not_found; a link ended meanwhile 403` — B41: `can()` on
  `space.links`.

### PR 3
**Unit**
- U1 `subscriptions/limits.unit.test.ts`: `each warning alone, then all in order; days a week only when today is
  not counted yet; hours at exactly the limit` — B1: `>` for `≥`; B2: the "today not counted" condition dropped.
- U2 `subscriptions/requests.unit.test.ts`: `open=true or a range of at most 92 days, to not before from` — B3:
  the bound removed.

**API — `occupancy/present.api.test.ts`** [C1]
- T1 (existing T3–T5 of #94 kept green) and T2 `the read, the check-in's warning and the directory count the same
  people present` (one open visit, one open check-in, a capacity of 2: the read 2, `SPACE_FULL` at the next
  check-in, the directory `FULL`) — B4: the directory's count from visits only.

**API — `desk/subscriberCheckIn.api.test.ts`** [C2]
- T3 `the staff check a subscriber in, audited checkIn.checkedIn, answered with the subscription's state` —
  B5: the audit removed.
- T4 `each warning: full, outside hours, not started, expired, days used this week, hours used today — never a
  refusal` — B6: the subscription warnings computed after the check-in is created (a day counted).
- T5 `a retry answers the same check-in and the same warnings, 201; two at once make one` — B7: `findCheckInByKey`
  skipped; B8: the lock removed.
- T6 `a customer present by a check-in or a visit is refused MEMBER_ALREADY_CHECKED_IN, writing nothing` — B9:
  the visit side of `isPresent` dropped.
- T7 `another space's subscription is invalid_choice on subscriptionId; an archived customer CUSTOMER_ARCHIVED`
  — B10: the archived check removed.
- T8 `a stranger, another space's owner and the admin not_found; a link ended while waiting 403` — B11: `can()`
  on `space.links`.
- T9 `a check-in waiting while the subscription is ended warns SUBSCRIPTION_EXPIRED` (`whileHeld`: `ended_at`
  set meanwhile) — B12: the subscription read before `lockAtDesk`.
- T10 `a check-in waiting while the customer is archived is refused CUSTOMER_ARCHIVED` (`whileHeld`) — covered by
  B12's twin: the customer read before the lock (B13).
- T11 `refuses a missing key and an invalid body before anything is read`.

**API — `desk/subscriberCheckOut.api.test.ts`** [C3]
- T12 `check-out closes it now, MANUAL, audited checkIn.checkedOut, answered with the subscription's due, paid and
  balance` (a per-hour subscription: the minutes now counted) — B14: `checkoutMethod` left null (the `CHECK`
  then 500).
- T13 `a closed check-in answers as it is, nothing audited` — B15: the closed branch removed.
- T14 `another space's check-in not_found; a link ended while waiting 403` — B16: `can()` on `space.links`.

**API — `subscriptions/checkIns.api.test.ts`** [C4]
- T15 `open=true answers every open check-in, the earliest first, whole` — B17: a `take` left from paging.
- T16 `a date range pages the check-ins by Gaza date, latest first, the total right` (a check-in at 23:30 UTC on
  the range's last Gaza day included) — B18: the range by UTC date.
- T17 `refuses a stranger and the admin with not_found; an invalid range with 422`.

### Not tested, and said
- The 50-item cap of an allocation: unit-tested only (U2); no API test seeds 50 debts.
- The two zone databases (finding 120): recorded, not testable without a transition night's data.

---

## 10. Review Focus — inputs no planned test exercises

- A subscription with check-ins in the hour around a daylight-saving change (finding 120).
- A customer list of a space with tens of thousands of subscriptions and a status filter (S10's read).
- A correction that moves `startsOn` after existing check-ins: they still count; the progress may show days
  before the start.
- A renewal of an `UPCOMING` subscription: proposed the day after its end, as a running one.
- An allocation where an older usage-based subscription's due grows while the request waits (a check-out
  committed under the space's lock first: then it is seen).
- Clearing the phone of a customer who owes a visit's debt (allowed; the debt keeps its customer).
- A subscription corrected from `PER_HOUR` to `FIXED` whose payments exceed the new price: `PRICE_BELOW_PAID`.
- The SQL balance and `balanceOf` agreeing on every item kind (T30 of PR 1 pins one set).

---

## 11. The commits

Conventional Commits; subjects counted (≤ 50); a body that says why; no tool attribution; staged by path. Every new
decision and history line ends with `<the day's date>, #PRNUM`. **C0**, in each PR, only if a
`0_CARRIED_FROM_<n>.md` naming that PR exists when its executor starts: its items, as it says, in that PR's first
commit(s), each red first, then green, with its break; the description says "Carried from #n".

### PR 1 — `feat/customers`, title `feat(desk): keep customers on file` (34)
| # | Subject | Chars | Holds |
|---|---|---|---|
| C1 | `feat(customers): create and edit a customer` | 43 | migration `customer_key`; shared `customers`; the create (key) and the edit; U3, U6, T1–T9; contract *Customers (managed)*; data model (*Idempotency*, *Customer*); `customers.md` (first); conventions §13 |
| C2 | `feat(customers): archive and restore a customer` | 47 | `customers.archive` (U8), the desk's archive, the restore, `CUSTOMER_ARCHIVED`; T10–T15; ADR 0009's row; security |
| C3 | `feat(subscriptions): derive status and progress` | 47 | migration `subscription_usage`; `gazaTime` (U1), `dateSchema` (U2), `subscriptionStatus` (U4), `currentSubscription` (U5), the states read; D1–D4; data model (*Subscription status*, *progress*, *Amount due*, S4, S5); `subscriptions.md` (first); conventions §8; finding 120 + index |
| C4 | `feat(payments): compute debts in the database` | 45 | D5's queries; T16–T20; data model (*Customer debt*); `payments.md`; conventions §9 (S9) |
| C5 | `feat(desk): list customers and read their file` | 46 | the list (D4) and the file; U7, T21–T30; contract; §4's exceptions; `desk.md`; v1-mvp; overview |
| C6 | *only if the owner folds 113:* `fix(payments): page uncollected visits in SQL` | 45 | `uncollectedIn` on one query; finding 113 resolved |

### PR 2 — `feat/subscriptions`, title `feat(desk): run customers' subscriptions` (40)
| # | Subject | Chars | Holds |
|---|---|---|---|
| C1 | `feat(db): store a subscription's key and reason` | 47 | schema, migration `subscription_terms` (D9), seed and factory keys, D1–D5; data model *Constraints*; finding 80 resolved + index |
| C2 | `feat(desk): subscribe a customer` | 32 | `subscribeSchema` (no payment yet), `packages.termsOf`, `subscriptions.create`, the start date; T1–T9; contract; `subscriptions.md`, `desk.md`, `packages.md`; ADR 0015's *Revised*; conventions §13 |
| C3 | `feat(desk): receive a subscription's payment` | 44 | D6; `payments.record`; T10–T14; contract; `payments.md` |
| C4 | `feat(desk): renew, paying the oldest debt first` | 47 | renewal (U1), allocation (U2), derived keys (U3), `SUBSCRIPTION_ALREADY_RENEWED`, `CUSTOMER_HAS_DEBT`; T15–T22; contract; data model; conventions §9, §13 (S6); v1-mvp's route row (decision 8) |
| C5 | `feat(desk): read a subscription's statement` | 43 | T23–T25; contract; §4's exceptions |
| C6 | `feat(subscriptions): correct a subscription` | 43 | U4, U6, the two routes, `SUBSCRIPTION_ENDED`, `PRICE_BELOW_PAID`; T26–T31; ADR 0009's rows; security |
| C7 | `feat(subscriptions): end a subscription early` | 45 | D10; T32–T34; data model; overview; v1-mvp |

### PR 3 — `feat/subscription-check-ins`, title `feat(desk): check subscribers in and out` (40)
| # | Subject | Chars | Holds |
|---|---|---|---|
| C1 | `refactor(occupancy): define present once` | 40 | D12; T1–T2; `occupancy.md`; finding 111 resolved + index |
| C2 | `feat(desk): check a subscriber in` | 33 | D11 check-in, `limits.ts` (U1), the four warnings; T3–T11; contract; data model (*Full warning*, *Subscription limits*); `desk.md`, `subscriptions.md` |
| C3 | `feat(desk): check a subscriber out` | 34 | T12–T14; contract |
| C4 | `feat(subscriptions): list check-ins` | 36 | U2, T15–T17; contract (§4 exception); v1-mvp (the `/check-ins` rows built); overview |

---

## 12. Verification and the procedure

**The same procedure for each PR**, with that PR's branch and checks. The executor of PR *n* reads this whole
plan and builds only PR *n*.

### 12.1 Before the branch
```powershell
Set-Location C:\dev\masaha\app-b
git fetch origin
git status --short --branch            # clean, detached at origin/main
git log --oneline -8 origin/main
git diff --name-status abc28e73 origin/main
gh pr list --state open --json number,title,headRefName,headRefOid,files
Get-ChildItem C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS -Filter '0_CARRIED_FROM_*.md'
```
- **PR 1:** DESK PR 4 merged (`gh pr list --state merged --search "feat/visit-debts" --json number,mergeCommit`);
  else stop. The diff must hold DESK PR 4's §7 files (and its carried commits) and worker A's web and docs; then
  **re-read DESK PR 4's merged payment route against this plan**: `receivePaymentSchema`, `ReceivedPayment`,
  `lockAtDesk`'s action parameter, `payments.balancesOf` / `paidFor(tx)`, `customerFor`, `visits.writtenOffAt`
  and the uncollected read's `writtenOffAt: null`, and the merged findings index (the numbers of 111–113). **A
  difference this plan does not cover → stop and ask.** Any other change to a code file this PR names → stop
  and ask.
- **PR 2 and PR 3:** the same diff from `abc28e73`; PR 1's (and PR 2's) files must hold what this plan says; any
  other change to a code file this PR names → stop and ask.
- An open PR that edits a code file of this PR: stop and ask. Its documents: re-read the shared ones on the
  merged tree before editing.
- `0_CARRIED_FROM_<n>.md` naming this PR: read it whole; its items are C0 (§11). If they contradict this plan:
  stop and ask.

```powershell
git switch --no-track -c <feat/customers | feat/subscriptions | feat/subscription-check-ins> origin/main
docker start masaha-postgres-1         # never npm run db:up; never npm ci
npm run build -w @masaha/shared
```
- `apps/api/.env` names `masaha_b_dev` / `masaha_b_test` and `PORT=3321` (`Select-String` by pattern; never print
  the file).
- After a merged migration (DESK PR 4's, PR 1's, PR 2's): `npm exec -w @masaha/api -- prisma generate`, `npm run
  db:migrate` (applies to `masaha_b_dev`); `prisma migrate status` → up to date. No `npm install` is needed (no
  dependency changes); if `node_modules` is missing a package: stop and ask.

**Memory: one full test run at a time on this machine.** Before each full lane, write the free memory into the
report and check that nothing of worker A's runs:
```powershell
Get-CimInstance Win32_OperatingSystem | Select-Object FreePhysicalMemory
Get-CimInstance Win32_Process -Filter "Name = 'node.exe'" |
  Where-Object { $_.CommandLine -match 'vitest|tsc' } | Select-Object ProcessId, CommandLine
```
- A `vitest` (or `tsc`) under `C:\dev\masaha\app\` (worker A's): wait for it to end; never stop it.
- **A lane killed for memory stops the work:** no retry, the report written, `Status: STOPPED`.

### 12.2 First checks (each when its code exists)

**PR 1**
1. **The migrations, each created once:** after the schema edit, `npm exec -w @masaha/api -- prisma migrate dev
   --create-only --name customer_key`, **once**, then `Get-ChildItem apps/api/prisma/migrations | Select-Object
   -Last 2`; keep Prisma's column and unique index. Then `npm run db:migrate`. For the function: `prisma migrate
   dev --create-only --name subscription_usage` **once** with no schema change (an empty migration), list the
   folder, append D3's SQL under a raw-SQL header, `npm run db:migrate`. **If Prisma refuses an empty
   migration:** create the folder `<UTC timestamp>_subscription_usage` by hand with the `migration.sql`, then
   `npm run db:migrate`, and say so. On a data-loss refusal (not expected: a nullable column): `prisma migrate diff
   --from-migrations apps/api/prisma/migrations --to-schema-datamodel apps/api/prisma/schema.prisma --script`
   into the folder, then append, and say so. `masaha_b_test` is migrated by the API lane's global setup; confirm
   it with the first API run's output.
2. **The function on both databases:** `docker exec masaha-postgres-1 psql -U <the .env user> -d <db> -c "SELECT
   count(*) FROM subscription_usage(1, NULL, current_date, current_date)"` answers a number on each.
3. **`masaha_search_text` exists** (the directory's migration): `\df masaha_search_text` on `masaha_b_test`. If
   not: stop and ask.
4. **Prisma's `$queryRaw` with an array:** `${ids}::integer[]` binds one parameter (T26 proves it). If it does
   not compile or binds per element: `Prisma.sql` with `ARRAY[...]` is not acceptable (that is per element) —
   stop and ask.
5. **A `@db.Date` round trip:** a test's `startsOn: new Date('2026-10-20T00:00:00Z')` reads back as
   `'2026-10-20'` through D13's rule. If Prisma shifts it: stop and ask.
6. **The level rule:** `npm run lint` passes with `desk` importing `customers`, `subscriptions`, `payments`,
   `visits`, `occupancy`; `payments` importing `subscriptions`; `subscriptions` importing `customers` and
   `packages`. A refusal: stop and ask.
7. **T26's size:** if 70,000 ids make the test slower than Vitest's 5 s: seed 20,000 and say so (the point is
   above 65,535 bind parameters only through Prisma's `in`; with one array parameter any size proves it — keep
   the largest that runs under 5 s, never below 66,000 if it fits).

**PR 2**
1. **The migration, created once:** `prisma migrate dev --create-only --name subscription_terms` **once**, then
   list the folder. Prisma's `ADD COLUMN "request_id" UUID NOT NULL` would fail on the seeded rows: **edit it**
   to `ADD COLUMN "request_id" UUID;` and put D9's `UPDATE … SET NOT NULL` before the unique index; keep the
   `price_reason`, `renewal_of_id` columns, the unique index and the foreign key; append the rest of D9. On a
   refusal: `migrate diff --script` as PR 1 check 1. Then `npm run db:migrate`; check that
   `apps/api/src/generated/prisma/models/Subscription.ts` names `idempotencyKey`, `priceReason` and `renewalOfId`.
2. **The self-relation through `(renewalOfId, customerId)`:** `prisma validate` accepts it. If not: the relation
   on `renewalOfId` → `id` alone, and the same customer checked by the service (422 `invalid_choice`), and say so.
3. **The trigger's error:** `checkViolationOf` reads `subscriptions_price_below_paid:` (T30). If 500: stop and ask.
4. **DESK PR 4's `receivePaymentSchema`:** `visitId` becomes optional with the refinement; DESK PR 4's tests that
   omit `visitId` expect `required` on `visitId` — keep that answer (the refinement's message on `visitId`).
5. **The seed:** `npm run db:seed` with `SEED_DEMO=true` on `masaha_b_dev` after the migration runs clean twice
   (demo.api.test's "changes nothing when run again" stays green).
6. **The exact-key tests:** `ReceivedPayment` gains `subscription: null`: DESK PR 4's `desk/payments.api.test.ts`
   `toEqual`s gain it by hand, nothing else.

**PR 3**
1. **`occupancy.checkInWarnings`'s callers:** after D12, `git grep -n "openIn\|openCheckInsIn\|openCountsIn\|openCheckInCountsIn" apps/api/src/modules/occupancy`
   lists only `present.ts`.
2. **The level rule:** `desk` importing `subscriptions` and `occupancy`.
3. **The partial unique index's backstop:** a second open check-in for one customer, by raw insert, is refused
   (`check_ins_customer_id_key`); T6 covers the service.

### 12.3 Implement, commit by commit
- Stage **by path** (never `-A` or `.`), `git status --short` before each commit; after each commit `npm run lint`
  and `npm run typecheck`.
- Inside each commit: the test first, run red in its lane (the red output in the report); the code, then green; the
  commit's documents (Appendix A).
- Error codes follow `add-error-code`: the code in `packages/shared`, both catalogues, its line in api-contract §6,
  the test that provokes it.
- Each commit message in a UTF-8 file, **no BOM, LF line endings**, with a body; `git commit -F <file>`.
- **A fix before the push** folds into its commit:
  ```powershell
  git commit --fixup=<sha> -- <paths>
  $env:GIT_SEQUENCE_EDITOR=':'; git rebase -i --autosquash $(git merge-base HEAD origin/main); Remove-Item Env:GIT_SEQUENCE_EDITOR
  git rebase -x "npm run lint && npm run typecheck" $(git merge-base HEAD origin/main)
  ```

### 12.4 Verification on the head (phase 4)
- One at a time, each **once, on the head** (re-run only if a file it covers changed after it passed): `npm run
  lint` · `npm run typecheck` · `npm run test:unit` · `npm run test:api` · `npm run format:check` · `npm run
  check:links` · `npm run build -w @masaha/shared` (the shared package changes in every PR).
- Also: `git grep -n "#PRNUM"` lists only documents (before §12.7); `git diff --stat origin/main -- apps/web`
  shows only the two `errors.ts`; `git diff --stat origin/main -- package.json package-lock.json` is empty.
- **Not run, with why:** `test:component`, the web's `build`, `check:build`, `check:classes`: the web change is two
  catalogue files of strings, whose parity the typecheck enforces; CI runs them on the pushed head.

### 12.5 The breaks — every one run, its red recorded
- For each B of §9: back up the file into `scripts\breaks\` (this folder), make the one edit, run the named test
  file in its lane, copy the red lines into the report, restore **from the backup** (never `git checkout`; SHA-256
  before and after, no CRLF change — Python writes with `newline=""`), run it green, then `git diff --stat` shows
  only the item's own work. The scripts (`scripts\brk.py` and its JSON, as DESK did) stay uncommitted.
- **Database breaks** (on `masaha_b_test` only, through `docker exec masaha-postgres-1 psql`):
  - PR 1 B14–B17: `CREATE OR REPLACE FUNCTION subscription_usage` with the one change; D1–D4 red; restore by
    re-running the migration's `CREATE OR REPLACE` text; green.
  - PR 2 B8–B12: drop the constraint, index or trigger; restore by re-running the migration's statement; green.
    B38: `CREATE OR REPLACE` the payments trigger with the subscription's ceiling skipped; T31 red; restore with
    DESK PR 4's migration's function (the latest), `prosrc LIKE '%payments_visit_written_off%'` → `t`.
- Every permission (PR 1 B13, B25–B27, B31, B42; PR 2 B7, B16, B20, B35, B36, B41; PR 3 B11, B16), every money
  rule (PR 1 B16, B32–B36, B46; PR 2 B2, B3, B11, B21, B22, B25, B27, B37, B38; PR 3 B14), every idempotency key
  (PR 1 B21–B23; PR 2 B4, B18, B19, B28; PR 3 B7, B8) and every race (PR 1 B22, B26; PR 2 B19, B29, B30, B38;
  PR 3 B8, B12, B13) has its break.
- **A break that stays green: stop**, unless it is plainly your own test's defect, or the plan's break cannot
  change the outcome (a bound already excluded by another rule); then make the break that can, see it red, and
  state it as a departure.

### 12.6 The real run (API on 3321, `masaha_b_dev`)
Start `npm run dev -w @masaha/api` in the background (log to `scripts\server.log`, deleted afterwards); `curl.exe -s
http://localhost:3321/health` → `db: up`. Sign in as `demo-owner@example.com` and `demo-reception@example.com`
(`SEED_DEMO_PASSWORD` read from `apps/api/.env` into a variable, never printed). The script is
`scripts\realrun<n>.mjs`. Record each status.
- **PR 1:** reception `POST …/customers { name, phone }` with a fresh key → 201; the same again → 201, the same id;
  another key, the same phone → 409 `PHONE_TAKEN`; `GET …/customers?payment=OWES` lists the demo's owing customers
  (رامي, محمد); `?status=ENDING_SOON` the hours pack's; `?q=0599000205` → رامي by digits; `GET
  …/customers/<rami>` → the visit debt 1,500 with its customer; reception `POST …/archive` → 403; the owner → 200;
  reception `?status=ARCHIVED` → 403; the owner `POST …/restore` → 200.
- **PR 2:** reception subscribes a demo customer from a package with a payment that covers an old debt and part of
  the new price → 201, two payments, `CUSTOMER_HAS_DEBT` absent; the same key → the same body; a renewal of the
  same subscription with another key → 409 `SUBSCRIPTION_ALREADY_RENEWED`; `POST …/payments { subscriptionId,
  amountAgorot }` above a fixed price → 409 `PAYMENT_EXCEEDS_DUE`; `GET …/subscriptions/<id>` → the statement;
  reception `PUT …/price` → 403; the owner below what is paid → 409 `PRICE_BELOW_PAID`; `POST …/end` → 200,
  `EXPIRED`. `SELECT action FROM audit_logs ORDER BY id DESC LIMIT 10`.
- **PR 3:** reception `POST …/check-ins { subscriptionId }` for the split-week customer → 201 with
  `DAYS_PER_WEEK_USED` if the demo week holds three days, else none (record which); the same key → the same id;
  the present demo subscriber (سارة) → 409 `MEMBER_ALREADY_CHECKED_IN`; `GET …/occupancy` counts the new one;
  `POST …/check-ins/<id>/check-out` → 200 with the balance; `GET …/check-ins?open=true`; `GET
  …/check-ins?from=<today−7>&to=<today>`.
- Stop the server by its process ids (the `tsx watch` child, the server, `pino-pretty`); `Get-NetTCPConnection
  -LocalPort 3321 -ErrorAction SilentlyContinue` prints nothing. Leave the demo data as it is, and say what changed.

### 12.7 The PR number, push and PR
Just before the push, in Git Bash:
```bash
n=$(( $(gh api "repos/{owner}/{repo}/issues?state=all&per_page=1&sort=created&direction=desc" --jq '.[0].number') + 1 ))
base=$(git merge-base HEAD origin/main)
git filter-branch -f --tree-filter "grep -rl '#PRNUM' docs | xargs -r sed -i 's/#PRNUM/#$n/g'" $base..HEAD
git for-each-ref --format='%(refname)' refs/original/ | xargs -r -n1 git update-ref -d
git grep -n '#PRNUM' ; echo "expect nothing above; PR will be #$n"
npm run check:links; npm run format:check
git push -u origin <branch>
```
- `gh label list`: `feat`, `area:api`, `area:docs`, `area:web` must exist (create a missing one with a description
  and a colour).
- Then at once:
  ```powershell
  gh pr create --assignee @me --label feat --label area:api --label area:docs --label area:web `
    --title "<the PR's title, §11>" --body-file <§12.9's text, saved in scripts\>
  ```
- GitHub's number must equal `n`; if not, fix the documents (a fixup into the commits that hold it) and `git push
  --force-with-lease`.

### 12.8 CI, CLEAN, conflicts, report
- `gh pr checks <n> --watch` (bounded), then `gh pr view <n> --json headRefOid,mergeStateStatus`: green **on the
  pushed head** (= `git rev-parse HEAD`) and `CLEAN`. Never merge; never rebase a `CLEAN` PR.
- **Conflicts:** for every other open PR, `git merge-tree --write-tree HEAD <its headRefOid>`; record clean or the
  conflicted paths. Documents only: the fast path when its turn comes. Code: stop and ask.
- **The report**, `4_REPORT_PR<n>.md` in this folder, written **as the work goes**: after the first checks, after
  each commit (sha, subject with its length, red, green), after each break, after the real run, after the push. It
  holds each command run or not, §12.2's results, the owner's answers to §13 as built, problems and their
  solutions, anything unexpected, the conflict check, every departure with why.
- **PR 1's report** updates `C:\dev\masaha\workspace\_SHARED\OPEN_DECISIONS.md` point 3: "**settled (#n,
  <date>):** a paged, searched list (at most 50 a page) for the owner and reception; no export and no whole list
  for anyone in step 8; an export is the owner's, later, in finance" (the supervisor commits nothing there).

### 12.9 The PR description
```markdown
## Summary
<PR 1: customers created (idempotent), edited, archived and restored; the list paged, searched and filtered, debts and the payment filter in the database; the customer's file; subscription status and progress.
 PR 2: subscribing from a package or custom, renewing with the server's allocation oldest debt first, a subscription's payment, the statement, corrections (price and billing the owner's, with a reason), ending early; finding 80.
 PR 3: subscription check-in with its warnings, check-out, the open and dated lists; present defined once.>
<"Carried from #n": each item, if C0 exists>

## Scope / Acceptance criteria / Out of scope
<§2, this PR's part>

## Change type
feat — API code, the shared contract, tests and documents; <PR 1: two migrations (customers' key; the attendance function) | PR 2: a migration (subscriptions' key, price reason, renewal link; the price trigger; finding 80) | PR 3: none>; the new codes' catalogue lines in apps/web (worker B's licence).

## New error codes (the Arabic needs the owner's approval)
<this PR's lines of §13 Q2>

## Evidence
- `lint`, `typecheck` (each commit), `test:unit`, `test:api`, `format:check`, `check:links`, `build -w @masaha/shared`: <results>.
- Seen failing first: <each test, its red line>.
- Deliberate breaks, each red then restored: <the PR's B-list>.
- Real run on 3321: <statuses>.
- Not run: `test:component`, the web's `build`, `check:build`, `check:classes` — two catalogues of strings; CI runs them.

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
```

### The executor's stop rule — a test you cannot run stops the work
A test **failing** because its code is not written yet is the plan's red step — normal. A test, lane or command you
**cannot run** is not: it errors before any test runs (the database unreachable, Docker down, a port taken, a module
or `dist` missing, a migration pending, `No test files found`, a Vitest or TypeScript startup error, the whole run
timing out, a crash with no result); a break you could not make or run; a real-run case you could not perform.
**Then stop at once** — never skip, `.skip` or delete a test, never change a config, a timeout, `.env`, a script or a
lane, never mock what the plan does not, never run a narrower command and call it the lane, never call it "flaky" and
move on. Write the command, its exact error and where you were into the report, and reply with the exec prompt's
final shape, `Status: STOPPED`.

**A plan that proves false against the code:** stop too, say exactly what and why, and offer the fix — do not choose
it yourself. **A break that stays green:** stop — unless it is plainly your own test's defect, or the plan's break
cannot change the outcome (a bound already excluded by another rule); then make the break that can, see it red, and
state it as a departure.

**Never claim a result you did not see:** a command passed only if you saw its own output say so; copy that line
(read it by its exit code, not the tail). A break counts only when you saw it red.

### Stop and ask
- DESK PR 4 is not merged, or merged with a shape §12.1's re-read does not match; `origin/main` changed a code file
  of §7 otherwise; an open PR edits one of them; a carried file contradicts this plan.
- A change is needed in `apps/web` beyond the two catalogues, a dependency, an error code not in §13 Q2, or a schema
  change beyond D3 and D9.
- More than about 70 files in one PR.
- A migration cannot be made as §12.2 says; Prisma refuses the function or the self-relation and check 2's fallback
  does not apply.
- `checkViolationOf` does not name `subscriptions_price_below_paid`; an array does not bind as one parameter.
- The level rule refuses an import of §12.2.
- A break that stays green (§12.5's exception aside).
- A failure not understood after three root-cause fixes; CI failing for a reason not reproduced locally after three.
- A conflict with another open PR in a code file.
- The owner's answer to §13 changes a test or a rule beyond what it says.

---

## 13. Decisions needed from the owner

1. **Q1 — S1:** attendance and the amount due computed by one database function (`subscription_usage`), the status
   and progress pure TypeScript on its counts; conventions §8's line changed. *Alternative A1:* the status in SQL too.
2. **Q2 — the new codes and their lines (the Arabic for your approval):**

   | Code | PR | Answer | English | Arabic |
   |---|---|---|---|---|
   | `CUSTOMER_ARCHIVED` | 1 | 409 | This customer is archived; the owner restores them first. | هذا الزبون مؤرشف؛ يسترجعه المالك أولًا. |
   | `SUBSCRIPTION_ALREADY_RENEWED` | 2 | 409 | This subscription was already renewed. | جُدّد هذا الاشتراك بالفعل. |
   | `SUBSCRIPTION_ENDED` | 2 | 409 | This subscription was ended early; it is no longer corrected. | أُنهي هذا الاشتراك مبكرًا، فلم يعد يُعدَّل. |
   | `PRICE_BELOW_PAID` | 2 | 409 | The new price is less than what was already paid; void a payment first. | السعر الجديد أقل مما دُفع؛ تُلغى دفعة أولًا. |
   | `CUSTOMER_HAS_DEBT` | 2 | warning | The customer still owes on an earlier item. | ما زال على الزبون دين سابق. |
   | `SUBSCRIPTION_NOT_STARTED` | 3 | warning | The subscription has not started yet; the check-in was recorded anyway. | لم يبدأ الاشتراك بعد، وسُجّل الحضور رغم ذلك. |
   | `SUBSCRIPTION_EXPIRED` | 3 | warning | The subscription has expired; the check-in was recorded anyway. | انتهى الاشتراك، وسُجّل الحضور رغم ذلك. |
   | `DAYS_PER_WEEK_USED` | 3 | warning | This week's days are used up; the check-in was recorded anyway. | استنفد أيامه هذا الأسبوع، وسُجّل الحضور رغم ذلك. |
   | `HOURS_PER_DAY_USED` | 3 | warning | Today's hours are used up; the check-in was recorded anyway. | استنفد ساعاته اليوم، وسُجّل الحضور رغم ذلك. |

   Reused as they are: `PHONE_TAKEN`, `MEMBER_ALREADY_CHECKED_IN` (its name keeps "member"; renaming it is churn
   for no reader), `PRICE_TYPING_NOT_ALLOWED`, `PAYMENT_EXCEEDS_DUE`, `SPACE_FULL`, `OUTSIDE_OPENING_HOURS`.
3. **Q3 — the schema:** PR 1's two migrations (`customers.request_id`; the function); PR 2's (`subscriptions.request_id`
   required and backfilled, `price_reason` with its `CHECK` and the dev backfill, `renewal_of_id` unique, the price
   trigger, finding 80). PR 3: none.
4. **Q4 — the attendance rules (D3):** a day is used by any check-in on it, open or closed; minutes count closed
   stays only, whole minutes each; a per-hour due is minutes × rate ÷ 60, half up (not per started hour, as the
   prototype's `Math.ceil` on an open stay). *Otherwise:* say which unit.
5. **Q5 — "shorter than a week":** a subscription of at most 7 days by its dates is ending soon on its last day only;
   a longer one from 7 days before its end.
6. **Q6 — S4 and S5:** an `UPCOMING` status; an ended subscription `EXPIRED` at once.
7. **Q7 — S3 and S6:** a subscription renewed at most once; a renewal's payments with derived keys, at most 50 items.
8. **Q8 — the routes (D1):** the price on its own `PUT …/price` (🏢); the name not correctable (A3 otherwise); the
   archive refused while present (S11); the subscriber's payment after the check-out, not inside it (A5).
9. **Q9 — finding 113 folded** into PR 1 (C6), or left to its own item.
10. **Q10 — ADR 0009's four rows and ADR 0015's *Revised* line** (§5).
11. **Q11 — the list's order:** by name, then id. *Otherwise:* the newest first.

---

## Appendix A — the documents, line by line (the commit in brackets)

Every new decision and history line ends with `<the day's date>, #PRNUM`; *Last Updated* on each document changed.

### PR 1
1. **`api-contract.md`** — new section *Customers (managed)* before *Front desk (managed)*: the create (key, 201, retry,
   `PHONE_TAKEN`), the edit, the archive and the restore (🏢, `CUSTOMER_ARCHIVED`, `MEMBER_ALREADY_CHECKED_IN`), the
   list (query, `CustomerRow`, "every filter before the page", archived only for `status=ARCHIVED`, no export), the file
   (`CustomerFile`); `Customer`, `CustomerBalance`, `SubscriptionState`, `ItemPayment`; audit names `customer.created`,
   `customer.edited`, `customer.archived`, `customer.restored` [C1, C2, C5]; §1's *Idempotency key* "Built for …" + "a
   customer's creation" [C1]; §4's exceptions: the file's lists [C5]; §6: `CUSTOMER_ARCHIVED`, `PHONE_TAKEN`'s gloss
   [C2].
2. **`data-model.md`** — *Conventions › Idempotency*: + customers (nullable: the desk's phone flow) [C1]; *Derived
   values*: *Subscription progress* (D3's units), *Subscription status* (`UPCOMING`, ended → expired, "at most 7 days"),
   *Amount due* (minutes ÷ 60 half up; computed by `subscription_usage`) [C3]; *Customer debt*: "… computed in the
   database by `payments`" [C4]; *Constraints*: the customers' key [C1].
3. **`conventions.md`** — header *Built*: + "customers and the composed customers list and file" [C5]; §8 *Pure rules*:
   "subscription progress and status in `subscriptions`; a subscription's attendance and amount due in its database
   function `subscription_usage`" (S1) [C3]; §9 *Composed reads*: the list's three resolutions (D4) and the balance query
   (S9) [C4, C5]; §13 *Idempotency*: "Subscriptions and customers have none yet" → "customers have it since #PRNUM;
   subscriptions with step 8's next PR" [C1].
4. **`security.md`** — *Authorization*: `requireCan` on the customers' writes; the archive and restore (🏢) [C1, C2].
5. **ADR 0009** — *Revised* line and two rows (§5) [C2].
6. **`docs/features/customers.md`** (new, the capability template) [C1, C2]; **`subscriptions.md`** (new: status,
   progress, the function, the states; *API decisions*: S1, S4, S5, D13) [C3]; **`desk.md`** — the list, the file, the
   archive [C2, C5]; **`payments.md`** — the balances in SQL (S9) [C4].
7. **`docs/README.md`** — the map's lines for `customers.md` and `subscriptions.md` [C1, C3].
8. **Finding 120** + its index line under *Open* [C3].
9. **`v1-mvp.md`** — step 8 *Built*: "customers created, edited, archived and restored; the list and the file, debts in
   the database (#PRNUM)"; the route table's customers rows into the *Built* sentence, + the archive and restore [C5].
10. **`overview.md`** — *Built*: a *Customers* line (on the API) [C5].

### PR 2
1. **`api-contract.md`** — new section *Subscriptions (managed)*: the subscribe (body, the start date, the renewal, the
   allocation, the retry, `NewSubscription`, warnings), the statement, the corrections, the end; `POST …/payments`'
   `subscriptionId`; audit names `subscription.created`, `subscription.corrected`, `subscription.priceCorrected`,
   `subscription.ended`, `payment.recorded`'s `subscriptionId` [C2–C7]; §1 + "a subscription's creation, its
   payments' keys derived" [C2, C4]; §4: the statement [C5]; §6: the four codes [C4, C6].
2. **`data-model.md`** — *Constraints*: the price reason, the renewal's uniqueness, the price trigger, prices above zero
   [C1]; *Front desk and money*: *Hand-typed prices* + the correction; *A renewal with a debt* (K3: the server allocates
   oldest first, one payment per item); *Subscription status*: ending early [C2–C7]; *Checked by the service*: "a
   renewal of the customer's own subscription" [C4].
3. **`conventions.md`** — §9 *The front desk*: subscribing and renewing as built, with the allocation [C4]; §13: keys
   for subscriptions; the derived keys (S6) [C2, C4]; *The ledger's rules*: + "a fixed price never below what is paid"
   (S2) [C6].
4. **`security.md`** — the subscriptions' `requireCan` list; the price correction (🏢) [C2, C6].
5. **ADR 0009** two rows + *Revised*; **ADR 0015** *Revised* (rule 4 done) [C2, C6].
6. **`subscriptions.md`, `desk.md`, `payments.md`, `packages.md`** (*Who uses it*: subscriptions copy a package's terms)
   [C2–C7].
7. **Finding 80** resolved, index moved [C1].
8. **`v1-mvp.md`** — step 8 *Built* + subscriptions; the route row "new or renewal, from a package or custom; warns
   when the customer has a balance" → "…; an optional amount the server allocates oldest debt first, one payment per
   item, under one key" (decision 8); the subscriptions rows into *Built* [C4, C7].
9. **`overview.md`** — *Built*: the *Customers* line gains subscriptions [C7].

### PR 3
1. **`api-contract.md`** — *Front desk (managed)*: the subscriber's check-in (body, warnings in order, refusals, retry),
   check-out, the lists; §4: the open check-ins; §6: the four warnings [C2–C4].
2. **`data-model.md`** — *Full warning* (subscription too), *Subscription limits* (the four warnings, K5's count) [C2].
3. **`conventions.md`** — §9 *occupancy*: "*present* is `present.ts`'s, used by the read, the warnings and the
   directory" [C1]; §9 *The front desk*: the subscriber's check-in and check-out [C2, C3].
4. **`security.md`** — `requireCan('attendance.record')` on the check-ins [C2].
5. **`occupancy.md`** [C1]; **`desk.md`**, **`subscriptions.md`** [C2–C4].
6. **Finding 111** resolved, index moved [C1].
7. **`v1-mvp.md`** — step 8 *Built* complete; the `/check-ins` rows into *Built* [C4]. **`overview.md`** [C4].

## Appendix B — Claude Code skills, only a map

| Step | Skill (if the executor is Claude Code) |
|---|---|
| §12.1, the branch | `start-work-item` (its git part) |
| Each test red first, each break | `superpowers:test-driven-development` (workflow §10) |
| Each new error code (§13 Q2) | `add-error-code` |
| Any failure | `superpowers:systematic-debugging` |
| §12.4 before any claim | `superpowers:verification-before-completion` |
| §12.7–12.8 | `open-pr`, then `final-report` |

Only a map: the plan and the documents decide, and a skill that disagrees with them loses.
