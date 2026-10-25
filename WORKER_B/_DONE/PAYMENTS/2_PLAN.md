# PAYMENTS — payments voided, the payments list and «دفعاتي اليوم», on the API (build map step 9) — the plan

> **Approved by the owner, 2026-10-24 — binding on the executor** (it wins where the plan below differs):
> - **Q1 — as recommended:** D5; S1 and S2 taken (A3, A4, A5 not taken). **Correction by the supervisor
>   (approved with Q1):** S1 adds only a visit that **is priced** and owes after a void. D8's predicate is
>   `AND (v.checkout_method = 'AUTO' OR (v.customer_id IS NULL AND v.charge_agorot IS NOT NULL))` — a visit
>   closed by hand **unpriced** stays out of the uncollected visits (it is the unpriced visits' list's, #97). A
>   test: a manual, unpriced, customer-less visit is not listed uncollected; break: the clause dropped → red. The
>   documents' S1 wording says "a priced visit closed by hand with no customer that owes again after a void".
> - **Q2 — as recommended:** no key; a second void answers it as it is; the locks in D6's order (S7).
> - **Q3 — as recommended:** one route narrowed by `can()`, reception's other filters 403 (S6; A1 not taken);
>   20 / 50 a page; both ends or neither, at most 92 days, today by default (S5; A8 not taken); `kind` and
>   `voided` (S4); `meta.totals` (S3; A2 not taken).
> - **Q4 — one PR** (A7 not taken).
> - **Q5 — the documents** as §5 *Rules the item touches* proposes, with Q1's correction.
> - **Q6 — `VISIT_WRITTEN_OFF` reused**, both lines reworded as proposed (the Arabic approved: «سُجّلت هذه
>   الزيارة «لن يُحصَّل»؛ يتراجع المالك عن ذلك أولًا قبل استلام أي دفعة لها أو إلغاء إحدى دفعاتها.»).
> - **Carried:** `WORKER_B\ANNOUNCEMENTS\0_CARRIED_FROM_112.md` items 1–6 are the first commits, as decided.
> - **The owner's standing rules:** a small fix a review defers is the next PR's first commit
>   (`0_CARRIED_FROM_<n>.md`); a test seen red before its code is its own break, a separate break only for a guard
>   the red step did not prove; fix rounds run only what the change touches; a full lane killed for memory is
>   re-run once, then CI judges; a demo account or data lacking a real-run case → stop and report.

> **Base:** `origin/main` at `104d9d07` (Merge #112, `feat/announcements`, ANNOUNCEMENTS PR 1, 2026-10-24). Every
> point below was read on that tree; nothing this plan builds on is unmerged.
> **Worker:** B, in `C:\dev\masaha\app-b`. **Folder:** `C:\dev\masaha\workspace\WORKER_B\PAYMENTS\`: this plan
> `2_PLAN.md`; the report `4_REPORT_PR<n>.md`; the executor's scripts in `scripts\` (never committed).
> **One PR** (§13 Q4): **`feat/payments`**, title `feat(payments): void payments and list them` (43), ≈ 44
> files, one migration (a trigger function replaced; no table changes). It touches authorization, a transaction,
> a database rule and money: its own review conversation (one reviewer, no subagents).
> **Read only from commit objects** (`git show origin/main:…`, `git grep`, `git ls-tree`) and the workspace's
> files. Nothing was run, built, installed or checked out. Every point reading could not prove is an **executor
> check** (§12.2), with what to do if it fails.
> **Beside it:**
> - **Worker A's DESK_SCREENS** (screens 13–16) will hand worker B up to three API specs: an allocation preview,
>   the statement read in one snapshot (finding 124), reception's idle sign-out on the server. **Not this
>   item's.** The files this PR edits that those specs will likely edit too — each a likely text conflict:
>   `desk/desk.service.ts`, `desk/desk.manage.routes.ts`, `desk/desk.controller.ts` (the allocation preview and
>   the statement), `payments/payments.service.ts`, `payments/payments.repository.ts`, `payments/index.ts`
>   (`itemBalances`, `paymentsOfSubscription`, `allocate`), `packages/shared/src/payments/responses.ts`,
>   api-contract *Front desk (managed)* and *Subscriptions (managed)*, `features/payments.md`, `features/desk.md`.
>   This PR's routes: `POST …/payments/:paymentId/void` (desk's router) and `GET …/payments` (payments' router);
>   neither is a route those specs name.
> - **`TASKS\CONFLICT_GUARD_BASEL`** (CI, `package.json`, `apps/api/scripts/`, the findings index, a few
>   documents): this PR touches none of the first three; the findings index only if a finding is recorded (none
>   planned); its documents — re-read at §12.1, any shared one named in the report. **`TASKS\DEMO_DAILY_BASEL`**
>   (the demo seed): this PR does not edit the seed, but its real run (§12.6) reads the demo payments (A1); a
>   merged change to them is re-read at §12.1.
> - **ANNOUNCEMENTS PRs 2–4** (`WORKER_B\ANNOUNCEMENTS\2_PLAN.md`, after this item) share: `apps/api/src/app.ts`;
>   `docs/api/api-contract.md`, `docs/architecture/data-model.md`, `docs/backend/conventions.md`,
>   `docs/backend/security.md`, `docs/plans/v1-mvp.md`, `docs/project/overview.md`, `docs/README.md` (if its map
>   line changes); `docs/features/announcements.md` and `docs/features/subscriptions.md` (this PR's carried
>   commits; PR 4); `apps/api/src/modules/subscriptions/{index,subscriptions.service,subscriptions.repository}.ts`
>   (this PR's `namesOf`; PR 4 adds `closures/` files and may touch `index.ts`). The migrations are separate
>   folders: no text conflict; PR 4's is created after this one merges, so its timestamp is later.
> **Finding numbers:** this item's start at **170**. None is planned; any finding the executor records takes
> **170**, then 171, in order.

---

## 1. Summary

Step 9's API: the owner corrects a payment by voiding it, and each staff member's collections are seen.

- **Carried from #112** (first, as decided by the owner 2026-10-24): start now holds the 365-day period bound
  (a code fix, its test red first); four document fixes.
- **The void.** The owner voids a payment with a reason (`POST …/payments/:paymentId/void`), audited
  `payment.voided`; a second void answers the voided payment as it is, its first reason kept. It changes one row
  — the payment's void columns — and nothing else is rewritten: every balance, debt, credit, payment status,
  the uncollected visits and a fixed price's floor are derived, so the next read answers them without it (§4
  D5).
- **Two consequences made explicit:** a visit fully paid at a manual check-out, with no customer, owes again once
  its payment is voided and has nowhere to show — it becomes **uncollected** (S1, needs the owner); and a
  written-off visit's payments are **not voided until the write-off is undone**, the ledger's fourth rule both
  ways, held by the database (S2, needs the owner).
- **The list.** `GET …/payments`: the owner reads every payment of a range of Gaza days, filtered by staff,
  method, item kind and voided state, newest first, paged, with the totals of the whole filter in `meta`
  (received, by method, count, voided); **reception reads its own, today**, on the same route, `can()` narrowing
  it — «دفعاتي اليوم», voided ones listed and marked.

No new error code and no table change. The reused code `VISIT_WRITTEN_OFF` keeps its key; its two catalogue
lines, which speak only of taking a payment, are reworded to cover a void too (§13 Q6) — the only web change. No refund, no credit across items, no editable payment, no online payment (ADR 0010; overview *Not in
v1*).

---

## 2. The contract

### Scope
1. **Carried from #112** (`0_CARRIED_FROM_112.md`, items 1–6): `announcements.start()` refuses an end more than
   365 days after now; conventions §9's bullet moved; `announcements.md` states the public read; the contract's
   "will read" and the retry-after-delete line; history lines in order.
2. Migration `payment_void_guard`: `payments_guard_change` replaced, the void of a written-off visit's payment
   refused (`payments_visit_written_off`, already translated to `VISIT_WRITTEN_OFF`).
3. `@masaha/shared/payments`: `voidPaymentSchema`, `paymentsQuerySchema` and their constants; `PaymentRow`,
   `PaymentItem`, `PaymentTotals`, `PaymentsMeta`.
4. `POST /manage/spaces/:spaceId/payments/:paymentId/void` (🏢, `requireCan('payments.void')`), in `desk`.
5. `GET /manage/spaces/:spaceId/payments` (🧾; the owner's whole ledger, reception's own today), in `payments`.
6. The uncollected visits include a visit closed by hand with no customer that owes after a void (S1).
7. `subscriptions.namesOf` (the list's subscription names); `payments` gains `users`, `customers`,
   `subscriptions` as dependencies.
8. Documents: api-contract, data-model, conventions, security, `features/{payments,desk,subscriptions,
   announcements}.md` and the *Who uses it* lines the new reads add, v1-mvp, overview.

### Acceptance criteria
- [ ] Start now on an upcoming announcement whose end would fall more than 365 days after now is 422
      `endsAt: out_of_range`, writing nothing; the carried documents say what `0_CARRIED_FROM_112.md` says.
- [ ] The owner voids a payment with a reason (1–200 characters, required): 200 with the payment as the list
      shows it, its void at now, by the owner, with the reason; audited `payment.voided`; the payment counts
      nowhere from then on — the item's paid and balance, the customer's debt and credit, the uncollected visits,
      the list's totals.
- [ ] A second void answers the voided payment as it is, its first reason and voider kept, writing nothing; two
      at once void it once.
- [ ] Reception is 403 before the body is read; a stranger, another space's owner and the admin are 404; another
      space's payment, or an unknown id, is 404; an owner whose link ended while the void waited is 403.
- [ ] A written-off visit's payment is refused 409 `VISIT_WRITTEN_OFF`, by the database; once the write-off is
      undone it is voided.
- [ ] Voiding one payment changes no other row: another payment of the same item, the other parts of a renewal's
      allocation, the visit, the subscription and the write-off stay as they were.
- [ ] A visit paid in full at a manual check-out with no customer, its payment voided, is listed in the
      uncollected visits with what it owes; an open visit never is.
- [ ] The owner's list: a range of Gaza days (`from`–`to`, both included, at most 92 days; neither → today),
      `recordedById`, `method`, `kind`, `voided` (`INCLUDE` default, `EXCLUDE`, `ONLY`); newest received first,
      then id descending; paged (§4); each row names the item, its customer, who recorded it and the void (who,
      when, why); `meta.totals` over the whole filter but `voided` and the page: received, by method, the count,
      and the voided count and amount.
- [ ] Reception's list is its own payments of today (Gaza), voided ones listed and marked, totals its own;
      `from`, `to` or `recordedById` from reception is 403; another space's payments are never listed.

### Out of scope
- Screen 17 (`Payments.html`, `My payments.html`): worker A's later item. The prototype's CSV export: no route
  here (a finance export is step 11's, OPEN_DECISIONS point 3).
- Income and collections by period, debtors (step 11, `finance`); the owner's overview (step 12).
- DESK_SCREENS' three API specs (header).
- A refund, a transfer of credit, an edit or delete of a payment (ADR 0010); an undo of a void.
- An idempotency key on the void (ADR 0015 rule 2: an update is idempotent by design).

---

## 3. The reading done, and what it changed

From `origin/main` at `104d9d07`: `CLAUDE.md`; `docs/development/testing.md` (§1–§4); `docs/backend/conventions.md`
(whole); `security.md` (*Authorization*); ADR 0010 and 0015 (whole), 0009 (the void's row); `docs/architecture/
data-model.md` (*Conventions*, *Entities › Operations*, *Front desk and money*, *Constraints*, *Checked by the
service*); `docs/api/api-contract.md` (§1–§4, *Front desk (managed)* whole, §6's list); `docs/features/
payments.md` (whole); `docs/plans/v1-mvp.md` (steps 8–10, the route table); the findings index (the payments
lines; 110, 112, 124); `git grep void` over `docs/`; the payments migration, `visit_write_off` and
`subscription_terms` (their triggers); `schema.prisma` (`Payment`, `AuditLog`); the code of `payments` (whole),
`desk` (service, routes, index), `shared/auth/can.ts` (the payments actions), `shared/errors/constraintCodes.ts`,
`subscriptions/index.ts` and its service's functions, `visits` (service's functions, `deskVisitsOf`),
`customers` (`namesOf`), `users` (`namesFor`), `announcements` (`start()`, `period.ts`), `app.ts` (the services'
order and the mounts), `packages/shared` (`payments/*`, `core/{envelope,pagination,fields,gazaTime}.ts`,
`subscriptions/requests.ts`' `checkInsQuerySchema`), `apps/api/test/locks.ts`, `db/payments.api.test.ts`
(titles), the demo seed's payments; the prototype's screens 28 (`01-my-payments-today`) and 32
(`01-ledger-this-month`); `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_DESK.md` (K4, DK-016, DK-017),
`DECISIONS_OWNER.md` (no money on the overview); `_SHARED\OPEN_DECISIONS.md`; `WORKER_B\ANNOUNCEMENTS\
{0_CARRIED_FROM_112, 2_PLAN, 3_EXEC_PROMPT_PR1 (§2–§3), 6_REVIEW_PR1_CLAUDE_CODE (F1–F6)}.md`; `WORKER_B\
SUBSCRIPTIONS\scripts\prnum-fix109.sh`.

**What the reading changed:**
- **Most of step 9 is built.** Balances, credit and debts are read where the desk answers them: the customer's
  file, the statement, the customers list's payment filter, the uncollected visits (#100, #102, #106). Recording
  is built. What is left is **the void and the list** — nothing else is added.
- **The `can()` actions exist:** `payments.void` (owner), `payments.read` (owner), `payments.readOwn` (staff:
  "the payments the actor recorded today"). No change to `can.ts`.
- **The database already holds "voided once" and "append-only"** (`payments_guard_change`), and every read of
  money already leaves voided payments out (`balancesOf`, `paidFor`, `uncollectedPage`, the price floor). So the
  void writes one row and rewrites nothing (D5).
- **A void can leave a debt with no home.** A manual check-out with no customer is always fully paid (a part
  left unpaid requires a phone); the uncollected visits are the auto-closed ones only, and the debt counts visits
  with a customer only. Its payment voided, such a visit owes and shows nowhere — contradicting data model
  *Checked by the service* ("a visit left unpaid at a manual check-out … has a customer"). → S1.
- **A written-off visit's write-off is "what it still owed"**, and its audit records that amount
  (`visit.writtenOff`, `balanceAgorot`). A void after it would silently forgive more than the owner wrote off.
  The payments' insert trigger already refuses a payment on a written-off visit under the constraint name
  `payments_visit_written_off`, which the translation table maps to `VISIT_WRITTEN_OFF`. → S2: the same rule on
  the void, the same name, no new code, no table change.
- **Every desk money write takes the space's lock first** (`lockAtDesk`), as do the subscriptions' writes and the
  write-off and its undo: a void taking it first serialises with all of them (D6).
- **The two routes split by the boundary `payments.md` states:** the transaction, the space's lock and `can()`
  are `desk`'s; the ledger's reads are `payments`'. So the void is a `desk` orchestration, and the list is
  `payments`' own read (D1).
- **`meta` may carry what an endpoint adds** (`core/envelope.ts`: "the pagination of a list, or what an endpoint
  adds, such as the front desk's warnings"): the totals ride in `meta` with the pagination, one request on the
  desk's weak connection (S3).
- **The prototype's ledger** filters by period, staff, method and **type**, with a «إظهار الملغاة» toggle, and its
  footer sums the total, cash, transfer and the count; «دفعاتي اليوم» shows cash, transfer and total cards, voided
  ones struck through and out of the cards (K4). The list's filters and totals follow it (S4).
- **The check-ins list's range rule** (`checkInsQuerySchema`: both ends or neither, `to` at most 92 days after
  `from`) is the precedent for the range (S5).
- **Carried item 4:** `start()` sets `startsAt = now` without `periodErrors`; `periodErrors(…, 'edit', { startsAt:
  true, endsAt: false })` checks exactly the end's 365-day bound against the new start (the window holds for
  now; the end is after the start, the announcement being upcoming).

### Assumptions (each re-read by §12.1)
- **A1** — the demo space holds: the visit «هبة» closed `MANUAL`, no customer, charge 1,500, paid 1,500 by
  `demo-reception` a day back; the visit «رامي» closed `MANUAL` with the customer رامي, charge 1,500, unpaid; the
  subscription «every other day» with a voided 20,000 (reason «سُجّلت مرتين») and a live 20,000; and no payment
  received today (each `pay(…)` is 1 day back or more).
- **A2** — nothing between `104d9d07` and the branch's base changes a code file §7 names.

---

## 4. The decisions as built

### The owner's decisions, as built
1. **Append-only** (ADR 0010 rules 3–5): the void sets `voidedAt`, `voidedById`, `voidReason` on one row; the
   trigger keeps everything else (already built). The owner only (`payments.void`), with a reason. Audited
   `payment.voided`, the owner's; never on the admin's list (conventions §6's default deny: payments are a
   space's).
2. **The list** at `GET …/payments`: the owner sees all, with the date, staff and method filters (+ kind and
   voided, S4); reception its own, today (Gaza's day); voided ones listed and marked.
3. **The void** at `POST …/payments/:paymentId/void` (🏢, reason required).
4. **No refunds, no credit across items, no editable payment.**
5. **Downstream of a void:** D5 (S1, S2 need the owner).
6. **Idempotency and races:** D6.
7. **The list's shape:** D2, D4 (S3–S5).
8. **The cut:** one PR (§13 Q4).
9. **Documents this proves wrong:** §5 *Rules the item touches* (Q5).

### D1 — routes

| Route | Access | Body / query | 2xx | Module |
|---|---|---|---|---|
| `POST /manage/spaces/:spaceId/payments/:paymentId/void` | 🏢 `requireCan('payments.void')` | `voidPaymentSchema` | **200** `PaymentRow` | `desk` (orchestrates), `payments` (the row) |
| `GET /manage/spaces/:spaceId/payments` | 🧾 (boundary; `can('payments.read')` narrows) | `paymentsQuerySchema` | **200** `PaymentRow[]`, `meta: PaymentsMeta` | `payments` |

- **Placement and levels:** the void spans the space's lock, `can()` and the ledger → `desk` (L5), as the
  payment's record is; `payments` (L4) answers the row. The list reads `payments`' own table and names its rows
  through `visits` (L3, `deskVisitsOf`), `subscriptions` (L3, `namesOf`, new), `customers` (L2, `namesOf`) and
  `users` (L1, `namesFor`): all lower than `payments`; no level rule breaks (§12.2 check 2).
- **Mounting:** the desk's router (mounted first, `app.ts` line 508) gains the void; the payments' router (line
  511) gains `GET /payments`. `POST /payments` stays the desk's; Express passes a `GET` through the desk's router
  (§12.2 check 4).
- `:paymentId` parsed as the desk's other ids are (`not_found` when not a positive integer, as they answer).
- **Reads ask no `requireCan`** (#86): the list's narrowing is the service's `can()`, before any query.

### D2 — the shapes (`@masaha/shared/payments`)

```ts
// requests.ts
PAYMENT_KINDS = ['VISIT', 'SUBSCRIPTION'] as const
PAYMENT_VOID_FILTERS = ['INCLUDE', 'EXCLUDE', 'ONLY'] as const
PAYMENTS_RANGE_MAX_DAYS = 92                       // the check-ins list's bound (S5)
VOID_REASON_MAX_LENGTH = 200
voidPaymentSchema = z.object({ reason: textSchema(1, VOID_REASON_MAX_LENGTH) })
paymentsQuerySchema = paginationQuerySchema.extend({
  from: dateSchema.optional(), to: dateSchema.optional(),           // Gaza dates, both included
  recordedById: z.coerce.number().int().positive().optional(),
  method: z.enum(PAYMENT_METHODS).optional(),
  kind: z.enum(PAYMENT_KINDS).optional(),
  voided: z.enum(PAYMENT_VOID_FILTERS).default('INCLUDE'),
}).superRefine(…)   // one end without the other → 'required' on the missing one;
                    // to < from, or to > addDays(from, 91) → 'out_of_range' on 'to'  (92 days, both included)
VoidPaymentRequest, PaymentsQuery = z.infer<…>

// responses.ts
PaymentItem =
  | { kind: 'VISIT'; id: number; visitorName: string | null }
  | { kind: 'SUBSCRIPTION'; id: number; name: string }
PaymentRow = {
  id, amountAgorot, method, note: string | null, receivedAt,
  item: PaymentItem,
  customer: { id: number; name: string } | null,      // the visit's customer, or the subscription's
  recordedBy: { id: number; name: string },
  voided: { at: string; by: { id: number; name: string }; reason: string } | null,
}
PaymentTotals = {
  count: number,                                      // payments not voided
  receivedAgorot: number,                             // their sum
  byMethod: { CASH: number; TRANSFER: number },       // their sum by method, agorot
  voided: { count: number; amountAgorot: number },
}
PaymentsMeta = PaginationMeta & { totals: PaymentTotals }
```
- `92` days counted with `to` included: `to = addDays(from, 91)` passes, `addDays(from, 92)` is refused (U1).
- The note is answered as recorded (1–200, already bounded); no phone in a row (the list never needs one).

### D3 — the list's window (`payments/paymentsWindow.ts`, pure)
`paymentsWindow({ from, to }, now): { from: Date; to: Date }` — instants, `to` exclusive:
- neither given → today: `d = gazaClockOf(now).date`; `{ from: gazaInstant(d, 0), to: gazaInstant(addDays(d, 1), 0) }`;
- both → `{ from: gazaInstant(from, 0), to: gazaInstant(addDays(to, 1), 0) }`.
Reception's window is always today's. A payment counts in the day it was **received** (ADR 0010 rule 5).

### D4 — the list (`payments`)
`payments.page(actor, space, query): Promise<{ rows: PaymentRow[]; total: number; totals: PaymentTotals }>`:
1. **Narrowing first, before any query:** `mayReadAll = can(actor, 'payments.read', { links: space.links })`.
   Not the owner: `query.from`, `query.to` or `query.recordedById` present → `AppError.forbidden()`; else the
   filter is `{ recordedById: actor.id }` and today's window (S6). The owner: the query's filters and window.
2. `filter = { spaceId, from, to, recordedById?, method?, kind? }` (no `voided`): the totals' filter.
3. In parallel (conventions §5): `repository.page(filter, voided, { skip, take })` (`findMany`, `orderBy:
   [{ receivedAt: 'desc' }, { id: 'desc' }]`, `select` = `ItemPaymentRow`), `repository.count(filter, voided)`,
   `repository.totals(filter)` (`groupBy(['method'])` on `voidedAt: null` with `_sum`/`_count`, and `aggregate` on
   `voidedAt: { not: null }`).
4. `rowsOf(space.id, rows)`: the names (D7), mapped by `toPaymentRow`.
- `kind` → `{ visitId: { not: null } }` or `{ subscriptionId: { not: null } }`; `voided` → `voidedAt: null`
  (`EXCLUDE`), `{ not: null }` (`ONLY`), nothing (`INCLUDE`).
- **Index:** `payments_space_id_received_at_idx` (`spaceId, receivedAt`) serves the window and the order; the
  other filters apply on its rows. No new index (data model › *Indexes only for queries that run*).
- **Read without a lock** (as the other lists); the totals and the page are four statements outside a
  transaction: a payment landing between them shows on the next read (the same weakening as finding 124's,
  bounded by one list; Review Focus).

### D5 — what a void changes downstream (decision 5)
The void writes one row. Every figure is derived on read, each already leaving voided payments out — nothing
else is rewritten, and no other row is touched:

| Item | After its payment is voided |
|---|---|
| A visit with a customer (manual or auto check-out) | Owes again: in its customer's debt (`balancesOf`) and the file's unpaid visits; an auto-closed one also in the uncollected visits |
| A visit paid in full at a manual check-out, no customer | Owes again: **in the uncollected visits** (S1), where the desk leaves it to a customer («تسجيل دينًا»), takes its payment, or the owner writes it off |
| A written-off visit's payment | **Refused** `VISIT_WRITTEN_OFF` until the write-off is undone (S2), so the write-off's recorded amount stays what was forgiven |
| A fixed subscription | Its paid falls, its balance and payment status follow; its price floor falls with it (`subscriptions_price_below_paid` counts payments not voided): a correction may then lower the price |
| A usage-based subscription | Its credit shrinks, or a debt appears |
| A renewal's allocated payment | Only that payment's item owes again; the allocation's other parts stay; nothing is re-allocated; the subscribe's `CUSTOMER_HAS_DEBT` was a warning of its moment, not re-raised |
| A retry of the request that recorded it | Answers the payment as recorded (its `VisitPayment` carries no void), and the sums as of the retry, which show the void (stated in the contract; A6 offers the void in the answer) |

### D6 — the void, its idempotency and races (`desk.voidPayment`)
`voidPayment(actor, space, paymentId, { reason }): Promise<PaymentRow>`, one transaction, in this order:
1. `lockAtDesk(actor, space, tx, 'payments.void')`: the space's lock (404 when gone), then `can()` on
   `linksUnder(tx)` else 403.
2. `payments.lockIn(space.id, paymentId, tx)` (`SELECT … FOR UPDATE`, the space's) → none: 404 `Payment not found`.
3. Voided already → `payments.rowsOf(space.id, [locked], tx)`, answered as it is (its first reason and voider),
   nothing written, nothing audited (ADR 0015 rule 2).
4. `payments.void({ spaceId, row: locked, at: now(), byId: actor.id, reason }, tx)`: the update (the trigger may
   refuse a written-off visit's: `VISIT_WRITTEN_OFF`, through the table); audit `payment.voided` (entity the
   payment, the space's entry; `after: { visitId | subscriptionId, amountAgorot, method, reason }`); the row by
   `rowsOf`.
- **No key** (rule 2): the payment's id is the action's identity.
- **Locks, in one order:** the space's row, then the payment's row, then (inside the trigger) the visit's row
  `FOR SHARE` for a visit's payment. A payment's record takes the space's row, then the item's (the insert
  trigger), then inserts; a write-off and its undo the space's, then the visit's; a subscription's correction the
  space's, then the subscription's. Every one takes the space's row first, so none interleaves with a void; the
  payment's row lock makes two voids safe on its own (T12).

| Race | What decides | Test |
|---|---|---|
| Two voids of one payment | The payment's row lock; the second reads it voided and answers it as it is | T12 (B13) |
| A void and a write-off of its visit | The space's lock; the void reads the committed write-off; the trigger refuses | T13 (B14) |
| An owner's link ended while the void waits | `can()` on `linksUnder(tx)` | T6 (B9) |
| A void and a new payment of the same item | The space's lock; the payment's ceiling counts after the void | Review Focus (the ledger's insert trigger, proven by `db/payments.api.test.ts`) |
| A void and a price correction, a check-out, an undo of a write-off | The space's lock | Review Focus |

### D7 — the rows' names (`payments.rowsOf`)
`rowsOf(spaceId, rows: ItemPaymentRow[], tx?): Promise<PaymentRow[]>`, set-based, at most a page (50):
- visits: `visits.deskVisitsOf(spaceId, visitIds, tx)` → visitor name, customer `{ id, name }`;
- subscriptions: `subscriptions.namesOf(spaceId, subscriptionIds, tx)` (new: one `findMany`, `select { id, name,
  customerId }`) → `Map<id, { name, customerId }>`; their customers' names `customers.namesOf(spaceId, ids, tx)`;
- people: `users.namesFor([...recordedByIds, ...voidedByIds], tx)`.
Three or four queries in parallel; a missing name is a bug (thrown, as `statement` does).

### D8 — the uncollected visits widened (S1, `payments.repository.uncollectedPage`)
```sql
WHERE v.space_id = ${spaceId} AND v.checked_out_at IS NOT NULL
  AND (v.checkout_method = 'AUTO' OR v.customer_id IS NULL)
  AND v.written_off_at IS NULL
  AND (v.charge_agorot IS NULL OR v.charge_agorot - coalesce(p.paid, 0) > 0)
```
A manual check-out with no customer is fully paid when closed, so only a void brings it here; `checked_out_at IS
NOT NULL` keeps open visits out (they have no customer and no charge). Its order and paging unchanged.

### D9 — the migration `payment_void_guard` (S2)
Raw SQL only (no Prisma schema change):
```sql
-- The ledger's fourth rule, both ways (<the day's date>, #PRNUM): a written-off visit takes no payment, and its
-- payments are not voided until the write-off is undone, so a write-off keeps covering what the visit owed when
-- it was written off. The function is the payments migration's, with only that read added after its checks.
CREATE OR REPLACE FUNCTION "payments_guard_change"() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  <the payments migration's body, unchanged, up to its last IF … END IF>
  IF NEW."visit_id" IS NOT NULL THEN
    PERFORM 1 FROM "visits" WHERE "id" = NEW."visit_id" AND "written_off_at" IS NOT NULL FOR SHARE;
    IF FOUND THEN
      RAISE EXCEPTION 'payments_visit_written_off: a written-off visit''s payment is voided once the write-off is undone'
        USING ERRCODE = 'check_violation', TABLE = 'payments', CONSTRAINT = 'payments_visit_written_off';
    END IF;
  END IF;
  RETURN NEW;
END;
$$;
```
The trigger itself (`BEFORE UPDATE OR DELETE`) is unchanged. `constraintCodes.ts` unchanged: the name is mapped.

### D10 — the code (interfaces; the commit in brackets)

| Where | What |
|---|---|
| `announcements/announcements.service.ts` | `start()`: after the state check, `periodErrors({ startsAt: at, endsAt: current.endsAt }, at, 'edit', { startsAt: true, endsAt: false })` → `AppError.validation(errors)` [C0a] |
| `prisma/migrations/<ts>_payment_void_guard/migration.sql` | D9 [C1] |
| `packages/shared/src/payments/{requests,responses,index}.ts` | D2 [C2: `voidPaymentSchema`, `PaymentRow`, `PaymentItem`; C4: the query, `PaymentTotals`, `PaymentsMeta`] |
| `payments/payments.repository.ts` | + `lockIn(spaceId, id, tx): Promise<ItemPaymentRow \| null>` (raw `SELECT "id" … FOR UPDATE`, then the row), `void(id, { at, byId, reason }, tx): Promise<ItemPaymentRow>` [C2]; `uncollectedPage` (D8) [C3]; + `page`, `count`, `totals` (D4) [C4] |
| `payments/payments.service.ts` | deps + `users`, `customers`, `subscriptions`; + `lockIn`, `void`, `rowsOf` [C2]; + `page(actor, space, query)` [C4] |
| `payments/{payments.mapper,paymentsWindow}.ts` | + `toPaymentRow(row, names)` [C2]; `paymentsWindow` (D3) [C4] |
| `payments/payments.{controller,manage.routes}.ts`, `index.ts` | + `list`; `GET /payments` (`validate(paymentsQuerySchema, 'query')`); exports `PaymentRow` types only through shared [C4] |
| `subscriptions/subscriptions.{service,repository}.ts` | + `namesOf(spaceId, ids, tx?)` [C2] |
| `desk/desk.{service,controller,manage.routes}.ts` | + `voidPayment` (D6); `POST /payments/:paymentId/void` (`requireCan('payments.void')` → `validate(voidPaymentSchema)`) [C2] |
| `app.ts` | `createPaymentsService({ audit, visits, users, customers, subscriptions })` [C2] |

---

## 5. Stronger decisions, and Proposed alternatives

### S1 — a voided visit with no customer is uncollected — **recommended, needs the owner (Q1)**
*What:* the uncollected visits include a visit closed by hand, with no customer, that owes (D8). *Why:* only a
void can make one; without this it owes and shows in no list, no debt, no count — the owner voids a cash slip
and the money vanishes from every screen. The uncollected list already offers what such a visit needs («تسجيل
دينًا», a payment, the write-off). *Cost:* one predicate, one test; the data model's *Uncollected visits* and
*Checked by the service*, the contract's line "A manual check-out's visit is never listed", conventions §9 and
`payments.md` reworded. *Alternatives:* A5 (the void asks a phone), or leave it (not recommended).

### S2 — a written-off visit's payment is not voided until the write-off is undone — **recommended, needs the owner (Q1)**
*What:* the ledger's fourth rule both ways, in the trigger (D9), answered `VISIT_WRITTEN_OFF`. *Why:* the
write-off records what it forgave (`visit.writtenOff`'s `balanceAgorot`); a void after it would raise what the
visit owed while it stays written off, so the owner would forgive money nobody decided to forgive, unseen. The
owner undoes the write-off (one action), voids, and writes off again on the true rest. The database owns the
ledger's rules (ADR 0015 rule 7; conventions §13), so the rule is the trigger's, every path covered. *Cost:* one
migration replacing a function, one database test, one API test; no new code, no table change. *Alternatives:*
A3 (the desk checks it), A4 (allow it).

### S3 — the totals in `meta`, and the void answering the list's row — **recommended, planned**
`meta = { …pagination, totals }`: one request for the ledger's footer and «دفعاتي اليوم»'s cards, on the desk's
weak connection; `meta` already carries what an endpoint adds (`core/envelope.ts`). The void answers the
`PaymentRow` the list shows, so the screen replaces its row. *Cost:* one meta type. *Alternative A2.*

### S4 — two filters beyond the decision's three — **recommended, planned**
`kind` (visit or subscription: the prototype's «النوع») and `voided` (`INCLUDE` | `EXCLUDE` | `ONLY`: «إظهار
الملغاة»), defaulting to `INCLUDE` so «دفعاتي اليوم» lists voided ones marked (K4); the totals never count a
voided payment as received, whatever the filter. *Cost:* two `where` clauses, their test lines.

### S5 — the range: both ends or neither, at most 92 days, today by default — **recommended, needs the owner (Q3)**
The check-ins list's rule (`checkInsQuerySchema`), one bound for the desk's two ranged lists; a quarter covers
the ledger's screen («هذا الشهر», a chosen period). Longer periods are finance's (step 11). *Cost:* none.
*Alternative A8 (366 days).*

### S6 — reception's out-of-scope filters are refused, not ignored — **recommended, planned**
Reception sending `from`, `to` or `recordedById` gets 403 before any query. *Why:* an ignored filter would answer
a page that looks like what was asked and is not; a refusal shows the screen's bug at once. `method`, `kind`,
`voided` and the page stay open to reception (its own rows). *Cost:* one branch, its test and break.

### S7 — the void locks the payment's row — **recommended, planned**
Under the space's lock every writer is serialised, but the void's own safety does not lean on it: `FOR UPDATE` on
the payment makes two voids decide in turn whatever path a future writer takes (conventions §13 "a future writer
takes it too" covers the space; this covers the row). *Cost:* one raw statement.

### Rules the item touches, stated (Q5 — the documents this proves wrong, as proposals)
- **data-model › *Uncollected visits*** — "visits closed by the auto check-out, left unpaid and not written off"
  → "+ a visit closed by hand with no customer that owes again after a void" (S1).
- **data-model › *Checked by the service*** — "a visit left unpaid at a manual check-out, or at a later payment,
  has a customer" → "+ unless a void leaves it owing: it is then uncollected" (S1).
- **data-model › *Constraints* (the ledger)** and **conventions §13 *The ledger's rules*** — "a written-off visit
  takes no payment" → "+ and its payments are not voided until the write-off is undone" (S2).
- **api-contract `GET …/uncollected-visits`** — "A manual check-out's visit is never listed: its unpaid rest is a
  customer's debt" → "…unless a void leaves one with no customer owing: it is listed" (S1).
- **conventions §9 *Composed reads*, *Uncollected visits*** — the same; + "**The payments list** → `payments`,
  naming its rows through `visits`, `subscriptions`, `customers` and `users`".
- **finding 110**'s third point (the prototype's `unpaid` list holds visits checked out by hand) stays open as
  written: S1 lists only a voided one, not every manual unpaid visit. Its file is not edited.
- No ADR changes: ADR 0010 rules 3–5 and ADR 0015 rule 2 are what is built.

### Proposed alternatives (the owner may prefer them)
- **A1 — reception's list on its own route** (`GET …/payments/mine`, `payments.readOwn`). Clearer shape (no
  refused filters), one more route; the build map's table names one route narrowed. **Not recommended.**
- **A2 — the totals in `GET …/payments/summary`** (the announcements' precedent). Two requests per screen on a
  weak connection. **Not recommended.**
- **A3 — S2 checked by `desk`** under the visit's lock, no migration. A second owner of a ledger rule
  (ADR 0015's rejected alternative); a future void path would miss it. **Not recommended.**
- **A4 — a written-off visit's payment voided freely.** Simpler; the write-off then covers more than it recorded,
  silently. **Not recommended.**
- **A5 — the void asks a phone** when it would leave a visit with no customer owing (the payment's rule). The owner
  voiding an old cash slip often has no phone; S1 lets the desk decide later. **Not recommended.**
- **A6 — `VisitPayment` gains `voided`**, so a retry of a check-out, a payment or a subscribe answers the void.
  Changes three answers' shared type, which worker A's screens read. **Not recommended now;** the contract states
  the behaviour (D5).
- **A7 — two PRs** (the void, then the list). The void's answer is the list's row, built once; two PRs would edit
  the same contract sections and features twice. **Not recommended** (§13 Q4).
- **A8 — a 366-day range** (a year in one request). Larger totals scans; the period screens are finance's.

---

## 6. Related findings

| Finding | Folded? | Why, and the cost |
|---|---|---|
| **124** A statement's sums and its payments come from different snapshots | No | DESK_SCREENS hands it to worker B as its own spec (header); the void changes neither read |
| **110** The desk prototype's uncollected visits disagree with the owner's decisions | No | A prototype finding for worker A's screen item; S1 adds one kind of visit to the list, stated in Q5 |
| **112** A key that closed a visit with no payment is not remembered | No | The check-out's key; the void has none |
| **113** The uncollected read grows with every auto-closed visit (resolved) | — | D8 keeps its one-query shape; the widened predicate stays inside the same statement |
| **17** Expired rate-limit counters are never swept | No | No limit here |

No new finding is planned. Numbers **170** and on are this item's.

---

## 7. The files it edits

`apps/api`, `packages/shared`, `docs`, and in `apps/web` only the `VISIT_WRITTEN_OFF` line of the two catalogues
(`apps/web/src/shared/copy/{english,arabic}/errors.ts`, worker B's licence: a code's text follows what the API
answers it for; §13 Q6). No dependency, no seed.

| Commit | Files |
|---|---|
| C0a | `apps/api/src/modules/announcements/{announcements.service.ts, lifecycle.api.test.ts}`; `docs/api/api-contract.md`; `docs/features/announcements.md` |
| C0b | `docs/backend/conventions.md`; `docs/features/{announcements,desk,subscriptions}.md`; `docs/api/api-contract.md` |
| C1 | + `apps/api/prisma/migrations/<ts>_payment_void_guard/migration.sql`; `apps/api/src/db/payments.api.test.ts`; web `copy/{english,arabic}/errors.ts` (the one line each); `docs/architecture/data-model.md`; `docs/backend/conventions.md`; `docs/features/payments.md` |
| C2 | shared `payments/{requests,responses,index}.ts`, + `payments/requests.unit.test.ts`; api `payments/{payments.repository,payments.service,payments.mapper,index}.ts`; `subscriptions/{subscriptions.service,subscriptions.repository}.ts`; `desk/{desk.service,desk.controller,desk.manage.routes}.ts`, + `desk/void.api.test.ts`; `app.ts`; docs `api-contract.md`, `conventions.md` (§9 the desk), `security.md`, `features/{payments,desk,subscriptions,visits,customers,users}.md` (*Who uses it* where a read is new to the caller — `git grep` the boundary lines first) |
| C3 | `payments/payments.repository.ts`, `payments/uncollected.api.test.ts`; docs `api-contract.md`, `data-model.md`, `conventions.md`, `features/payments.md` |
| C4 | shared `payments/{requests,responses,index}.ts`, `payments/requests.unit.test.ts`; api + `payments/paymentsWindow.ts` (+ `paymentsWindow.unit.test.ts`), `payments/{payments.repository,payments.service,payments.controller,payments.manage.routes}.ts`, + `payments/list.api.test.ts`; docs `api-contract.md`, `conventions.md`, `security.md`, `features/payments.md`, `plans/v1-mvp.md`, `project/overview.md`, `docs/README.md` (only if its `payments.md` line names the capability's contents) |

≈ 44 distinct files. **Over about 60 → stop and ask.**

---

## 8. Design issues

No screen is built. Points for worker A's screen-17 item, not findings:
- **The CSV export** («تصدير CSV») has no route: an export is the owner's, later, in finance (OPEN_DECISIONS
  point 3).
- **The owner's toggle «إظهار الملغاة»** maps to `voided=EXCLUDE` when off; the footer reads `meta.totals`, which
  never counts a voided payment as received, so the sums do not change with the toggle — only the rows.
- **«دفعاتي اليوم»'s cards** are `meta.totals.byMethod` and `receivedAgorot`, `count`; voided rows struck through
  with `voided.by.name` and `voided.reason` (K4).
- **The void dialog's toast** (DK-018) can name what the item now owes only from a re-read (the file, the
  statement, the uncollected list): the void answers the row, not the item's sums.
- **A voided manual visit appears in «غير محصّلة»** (S1): the tab's copy should not say "closed at closing time".

---

## 9. Tests — lane, title, the break each catches

Every test is seen failing first in its own lane; every expectation is written by hand; a fixed clock through
`createTestApp({ clock })`; instants with their offset; Gaza dates as strings. Roles in each API file (testing
§4): the space's **owner**, its **reception**, a **stranger** (a signed-in USER), **another space's owner**, the
**admin**. B-numbers are §12.5's breaks, each run once, its red lines recorded. **A test seen red before its code
is its own break**; the B's below are the separate breaks for guards the red step does not prove.

### C0a (carried item 4)
- T0 `announcements/lifecycle.api.test.ts`: `start now refuses an end more than 365 days after now, 422 endsAt
  out_of_range, writing nothing` (an upcoming announcement starting in 300 days and ending 365 days after that;
  the row's `startsAt` and the audit unchanged) — its red step is its break (the fix absent → 200).

### Unit
- U1 `packages/shared payments/requests.unit.test.ts` [C2, C4]: `a void needs a reason of 1–200 characters`
  [C2]; `the payments query: both ends or neither, to not before from, at most 92 days with both included; the
  methods, kinds and void filters; recordedById positive; voided INCLUDE by default` [C4] — B1: the 92-day bound
  removed.
- U2 `payments/paymentsWindow.unit.test.ts` [C4]: `today in Gaza when no range is given (23:30 UTC is the next
  Gaza day); a range from its first Gaza midnight to the midnight after its last day` — B2: `to` exclusive of its
  own day (`gazaInstant(to, 0)`); B3: the UTC date instead of `gazaClockOf`.

### API — `db/payments.api.test.ts` [C1] (existing, gaining)
- D1 `a written-off visit's payment is not voided: payments_visit_written_off; once undone it is` — B4
  (database): the payments migration's `payments_guard_change` body restored on `masaha_b_test`.

### API — `desk/void.api.test.ts` [C2] (new)
- T1 `the owner voids a payment with a reason: 200 with the row, its void at now by the owner with the reason;
  audited payment.voided` — B5: the audit removed.
- T2 `reception is 403 before the body is read (an empty body), a stranger, another space's owner and the admin
  not_found` — B6: `requireCan('payments.void')` removed (reception's empty body then answers 422).
- T3 `a missing or blank reason is 422, writing nothing`.
- T4 `a second void answers it as it is, its first reason and voider, writing nothing and auditing nothing` — B7:
  the "voided already" branch removed (the trigger then answers 500).
- T5 `another space's payment, or an unknown id, is not_found` — B8: `lockIn` without the space filter.
- T6 `an owner whose link ended while the void waits on the space's lock is 403, writing nothing` (`whileHeld`:
  the space's row held; the owner's link deactivated meanwhile) — B9: `can()` on `space.links`.
- T7 `a written-off visit's payment is VISIT_WRITTEN_OFF, writing nothing; once the write-off is undone it is
  voided` — covered by B4 (the endpoint reaching the trigger, ADR 0015 rule 9).
- T8 `a fixed subscription paid in full, its payment voided: the statement answers paid 0, its balance the
  price; the price may then be corrected below the old paid` (hand-counted) — B10: `voided_at IS NULL` dropped
  from `balancesOf`'s subscriptions branch.
- T9 `a visit with a customer, its payment voided, counts in the customer's debt and the file's unpaid visits; a
  usage-based subscription's credit shrinks by it` — covered by B10's twin on the visits branch (B11).
- T10 `voiding one of an item's two payments leaves the other, the item and every other payment as they were`
  (all payment rows compared before and after; a renewal's allocation of two parts too) — B12: the update by the
  item (`updateMany` on `subscriptionId`) instead of the id.
- T11 `a retry of the payment's request after its void answers it, 201, records nothing, the sums showing the
  void` — B23: `findByKey` skipped in `receivePayment` (the retry then 500s on the unique key).
- T12 `two voids at once void it once: the second answers the first's reason` (`whileHeld`: the payment's row
  held; the test's transaction voids it meanwhile) — B13: `FOR UPDATE` removed from `lockIn` (the request's
  update then meets the trigger: 500).
- T13 `a void waiting while its visit is written off is VISIT_WRITTEN_OFF` (`whileHeld`: the space's row held; the
  visit written off meanwhile) — B14: `lockAtDesk` skipped (the request never waits: `waitingOnLock` fails).

### API — `payments/uncollected.api.test.ts` [C3] (existing, gaining)
- T15 `a visit paid in full at a manual check-out with no customer, its payment voided, is uncollected with its
  balance; with a customer it is not (its customer's debt); an open visit never is` — B15: the predicate back to
  `checkout_method = 'AUTO'`; B16: `checked_out_at IS NOT NULL` dropped (an open visit listed).

### API — `payments/list.api.test.ts` [C4] (new)
- T16 `the owner lists a range newest received first, then by id, paged; each row names its item, its customer,
  who recorded it, and a void's who, when and why` — B17: `orderBy` id ascending.
- T17 `the range counts Gaza days, both included (23:30 on to in, 00:00 after it out); recordedById, method, kind
  and voided filter` — covered by B2's twin at the route (B18: the window's `lt` as `lte`).
- T18 `the totals cover the whole filter but voided and the page: received, by method, the count, the voided
  count and amount; a voided payment is never received` — B19: the totals from the page's rows; B20: the
  `voidedAt: null` dropped from the received sum.
- T19 `no range lists today's (Gaza) payments only`.
- T20 `reception lists its own payments of today: another receptionist's, the owner's and its own of yesterday
  absent; its own voided one listed and marked; the totals its own` — B21: the narrowing skipped (reception read
  as the owner).
- T21 `reception's from, to or recordedById is 403 before anything is read` — B22: the refusal removed
  (narrowed silently).
- T22 `a range over 92 days is 422 out_of_range on to; half a range required` — covered by U1's B1 at the route.
- T23 `a stranger, another space's owner and the admin not_found; another space's payments never listed` — B24:
  the `spaceId` filter dropped; the boundary's 404s are the mount's (the router inside `manage`).

### Not tested, and said
- Four statements of the list outside a transaction (D4): a payment between them is the next read's.
- A void and a new payment of one item at once: the insert trigger's ceiling, proven by `db/payments.api.test.ts`
  ("leaves out voided payments", "is a fixed subscription's price, never exceeded"); the space's lock orders them.

---

## 10. Review Focus — inputs no planned test exercises

- A void racing a subscription's price correction or a check-out: both behind the space's lock (D6); not raced
  in a test.
- A renewal's retry after one of its parts was voided: `findByKeys` answers the parts as recorded (D5's last row).
- A payment received at 23:59:59.999 Gaza on a DST night: `gazaInstant` is pinned by `core/gazaTime.unit.test.ts`.
- A receptionist whose link is deactivated: their payments stay in the owner's list under their name; their own
  list is gone with the link (the boundary).
- A page of 50 rows naming 50 visits, 50 subscriptions and their customers: four set queries, bounded by the page.
- An owner filtering by a `recordedById` that is no staff of the space: an empty page, no error (a filter, not a
  path id).
- The admin never sees `payment.voided` (conventions §6's allowlist): no audit reader is built.

---

## 11. The commits

Conventional Commits; subjects counted (≤ 50); a body that says why; no tool attribution; staged by path. Every new
decision and history line ends with `<the day's date>, #PRNUM`.

### PR — `feat/payments`, title `feat(payments): void payments and list them` (43)
| # | Subject | Chars | Holds |
|---|---|---|---|
| C0a | `fix(announcements): hold the period on start now` | 48 | carried item 4: `start()`, T0; the contract's start line (the 365-day bound); `announcements.md` (behaviour, a *Revised* line) |
| C0b | `docs(announcements): state the public read` | 42 | carried items 1, 2, 3, 5, 6 (body names each): conventions §9's bullet moved; `announcements.md` the public read (*What it does*, *Who uses it*, *Behaviour*, the #112 line); the contract's "will read" and the POST's retry-after-delete line; `desk.md`'s and `subscriptions.md`'s `#112` last |
| C1 | `feat(db): keep a written-off visit's payments` | 45 | migration `payment_void_guard` (D9); D1; the `VISIT_WRITTEN_OFF` catalogue lines (Q6); api-contract §6's line for it ("…or voiding one of its payments"); data model (*Constraints*: the fourth rule both ways); conventions §13; `payments.md` (*Owns*) |
| C2 | `feat(payments): void a payment` | 30 | shared `voidPaymentSchema`, `PaymentRow`; `lockIn`, `void`, `rowsOf`, `toPaymentRow`; `subscriptions.namesOf`; the desk's `voidPayment` and route; U1 (its void part), T1–T13; contract (the void, `PaymentRow`, the retry-after-void lines on the check-out and `POST …/payments`); conventions §9 (*The front desk*: the void); security (*Authorization*: `requireCan('payments.void')`); `payments.md`, `desk.md`, the *Who uses it* lines |
| C3 | `feat(payments): show a voided visit uncollected` | 47 | D8; T15; contract (`uncollected-visits`); data model (*Uncollected visits*, *Checked by the service*); conventions §9; `payments.md` |
| C4 | `feat(payments): list a space's payments` | 39 | the query, `PaymentTotals`, `PaymentsMeta`; `paymentsWindow` (U2); `page`; the route; U1 (its query part), T16–T23; contract (`GET …/payments`); conventions §9 (the payments list); security (reception's own, by `can()`); `payments.md`; v1-mvp (step 9 *Built*, the two rows); overview (*Built*) |

The carried commits come first, before the plan's own, and the description names them under "Carried from #112".

---

## 12. Verification and the procedure

### 12.1 Before the branch
```powershell
Set-Location C:\dev\masaha\app-b
git fetch origin
git status --short --branch            # clean, detached at origin/main
git log --oneline -10 origin/main
git diff --name-status 104d9d07 origin/main
gh pr list --state open --json number,title,headRefName,headRefOid,files
Get-ChildItem C:\dev\masaha\workspace\WORKER_B\ANNOUNCEMENTS -Filter '0_CARRIED_FROM_*.md'
Get-ChildItem C:\dev\masaha\workspace\WORKER_B\PAYMENTS -Filter '0_CARRIED_FROM_*.md'
```
- **A2:** a change on `origin/main` since `104d9d07` to a code file of §7 → stop and ask. A change to the demo
  seed → re-read A1; a difference a real-run case needs → stop and report.
- **An open PR** editing a code file of §7 (DESK_SCREENS' specs, CONFLICT_GUARD): stop and ask. Its shared
  documents: re-read on the merged tree before editing; name them in the report.
- **`0_CARRIED_FROM_112.md`** is read whole with the review's F1–F6; its items are C0a–C0b. If it now names more
  items than 1–6, or contradicts this plan: stop and ask. Any other `0_CARRIED_FROM_<n>.md` naming this item:
  stop and ask.

```powershell
git switch --no-track -c feat/payments origin/main
docker start masaha-postgres-1         # never npm run db:up; never npm ci
npm run build -w @masaha/shared
```
- `apps/api/.env` names `masaha_b_dev` / `masaha_b_test` and `PORT=3321` (`Select-String` by pattern; never print
  the file).
- After any merged migration: `npm exec -w @masaha/api -- prisma generate`, `npm run db:migrate` (applies to
  `masaha_b_dev`); `prisma migrate status` → up to date. If `node_modules` misses a package: stop and ask.

**Memory: one full test run at a time on this machine.** Before each full lane, write the free memory into the
report and check that nothing of worker A's runs:
```powershell
Get-CimInstance Win32_OperatingSystem | Select-Object FreePhysicalMemory
Get-CimInstance Win32_Process -Filter "Name = 'node.exe'" |
  Where-Object { $_.CommandLine -match 'vitest|tsc' } | Select-Object ProcessId, CommandLine
```
- A `vitest` (or `tsc`) under `C:\dev\masaha\app\` (worker A's): wait for it to end; never stop it.
- **A full lane killed for low memory is re-run once, when the machine is quieter** (the free memory recorded
  again); **killed again → record it, carry on, and CI's run of that lane on the pushed head judges it** (red there
  → stop).

### 12.2 First checks (each when its code exists)
1. **The migration, created once:** `npm exec -w @masaha/api -- prisma migrate dev --create-only --name
   payment_void_guard` **once**, then `Get-ChildItem apps/api/prisma/migrations | Select-Object -Last 2`. The
   schema does not change, so Prisma makes an empty `migration.sql`: write D9 into it. **If it creates no folder**
   ("already in sync"): create `apps/api/prisma/migrations/<UTC yyyyMMddHHmmss>_payment_void_guard/migration.sql`
   by hand (as the earliest raw migrations were) and say so. **Never run `--create-only` twice** (a second run
   applies the first). Copy the function's body from `20260929120300_payments/migration.sql` and add only D9's
   block. `npm run db:migrate`; `masaha_b_test` is migrated by the API lane's global setup — confirm in the first
   API run's output. `psql … -c "\sf payments_guard_change"` on `masaha_b_test` shows the new block.
2. **The level rule:** `npm run lint` passes with D1's imports (`payments` → `users`, `customers`,
   `subscriptions`). A refusal: stop and ask.
3. **The services' order in `app.ts`:** `users`, `customers`, `subscriptions` are built before `payments` (read:
   lines 295, 356, 362 before 388). If a merge moved them: build `payments` after them, and say so.
4. **Two routers on `/payments`:** `GET …/payments` reaches the payments' router (T16) and `POST` still the desk's
   (`desk/payments.api.test.ts` green). If Express answers 404 for the `GET`: stop and ask.
5. **`PERFORM … FOR SHARE` in the trigger** (D1, T7): if PostgreSQL refuses the locking clause there, use
   `SELECT 1 INTO … FROM "visits" … FOR SHARE` with a declared variable, and say so; if neither: stop and ask.
6. **`sendSuccess`' `meta`** takes `PaymentsMeta` (`buildPaginationMeta(query, total)` spread with `totals`). If its
   type refuses the extra key: widen the call's type parameter only, never the helper; if impossible: stop and ask.
7. **`:paymentId`** is parsed by the helper the desk's controller uses for `:visitId`; none → stop and ask.
8. **The demo data (A1)** on `masaha_b_dev`: `SELECT id, visit_id, subscription_id, amount_agorot, received_at,
   voided_at FROM payments WHERE space_id = (SELECT id FROM spaces WHERE slug = 'masaha-demo') ORDER BY id;` —
   the «هبة» payment, the voided duplicate, none today. Otherwise: stop and report (§12.6).

### 12.3 Implement, commit by commit
- Stage **by path** (never `-A` or `.`), `git status --short` before each commit; after each commit `npm run lint`
  and `npm run typecheck`.
- Inside each commit: the test first, run red in its lane (the red output in the report); the code, then green; the
  commit's documents (Appendix A).
- **No new error code.** If one proves needed: stop and ask. (Were one approved, its steps, in order: the code in
  `packages/shared/src/core/errors.ts`; its text in both `apps/web/src/shared/copy/{arabic,english}/errors.ts`;
  its line in api-contract §6; the test that provokes it; each code with its English and Arabic in the PR
  description, the Arabic for the owner's approval.)
- Each commit message in a UTF-8 file, **no BOM, LF line endings**, with a body; `git commit -F <file>`.
- **A fix before the push** folds into its commit:
  ```powershell
  git commit --fixup=<sha> -- <paths>
  $env:GIT_SEQUENCE_EDITOR=':'; git rebase -i --autosquash $(git merge-base HEAD origin/main); Remove-Item Env:GIT_SEQUENCE_EDITOR
  git rebase -x "npm run lint && npm run typecheck" $(git merge-base HEAD origin/main)
  ```
- **Fix rounds** (after a review) run only what the change touches: its lanes' files, lint, typecheck, and the
  head's lanes again only where a file they cover changed.

### 12.4 Verification on the head (phase 4)
- One at a time, each **once, on the head** (re-run only if a file it covers changed after it passed): `npm run
  lint` · `npm run typecheck` · `npm run test:unit` · `npm run test:api` (the full API lane stays local:
  authorization, a transaction, the schema) · `npm run format:check` · `npm run check:links` · `npm run build -w
  @masaha/shared` (the shared package changes).
- Also: `git grep -n "#PRNUM"` lists only documents (before §12.7); `git diff --stat origin/main -- apps/web` shows
  only the two `errors.ts`, one line each; `git diff --stat origin/main -- package.json package-lock.json` is empty.
- **Not run locally — CI judges:** `test:component`, the web's `build`, `check:build`, `check:classes`: the web change is
  one catalogue string in each language, whose parity the typecheck and the unit lane's catalogue test enforce;
  report them under "Not run locally (CI judges)".

### 12.5 The breaks — every one run, its red recorded
- For each B of §9: back up the file into `scripts\breaks\` (this folder), make the one edit, run the named test file
  in its lane, copy the red lines into the report, restore **from the backup** (never `git checkout`; SHA-256 before
  and after, no CRLF change — Python writes with `newline=""`), run it green, then `git diff --stat` shows only the
  item's own work. The scripts (`scripts\brk.py` and its JSON, as SUBSCRIPTIONS did) stay uncommitted.
- **The database break** (B4, on `masaha_b_test` only, through `docker exec masaha-postgres-1 psql`): the payments
  migration's `CREATE OR REPLACE FUNCTION "payments_guard_change"` re-run; D1 and T7 red; restore by re-running
  D9's statement; green.
- **Every permission, money rule, idempotency rule and race has its break:**
  - permissions — owner, reception, admin, another space's staff, stranger: B6, B8, B9, B21, B22, B24 (and T2's
    boundary 404s);
  - money rules: B4 (written-off), B10–B11 (a voided payment counts nowhere), B12 (one row only), B15–B16 (the
    uncollected), B19–B20 (the totals), B1–B3, B18 (the window);
  - idempotency: B7 (a second void), B23 (a retry after a void);
  - races: B9, B13, B14.
- **A break that stays green: stop**, unless it is plainly your own test's defect, or the plan's break cannot
  change the outcome; then make the break that can, see it red, and state it as a departure.

### 12.6 The real run (API on 3321, `masaha_b_dev`)
Start `npm run dev -w @masaha/api` in the background (log to `scripts\server.log`, deleted afterwards);
`curl.exe -s http://localhost:3321/health` → `db: up`. Sign in as `demo-owner@example.com`,
`demo-reception@example.com` and `demo-directory-owner@example.com` (`SEED_DEMO_PASSWORD` read from
`apps/api/.env` into a variable, never printed). The script is `scripts\realrun1.mjs`, each case printing `PASS|FAIL`
with its status, and `ALL PASS` at the end. **A demo account or data that does not hold what a case needs → stop
and report; never change data through the app to get past it.** The run's own writes, named: one payment by
reception (case 4), one partial payment, one write-off and its undo on «رامي»'s visit (case 9), and the voids of
cases 6, 8 and 9 — the features under test.
1. Owner `GET …/payments?from=<today−10>&to=<today>` → the demo's six payments, newest first; `meta.totals`:
   received 47,500, cash 37,500, transfer 10,000, count 5, voided 1 / 20,000 (A1, hand-counted); the duplicate
   carries `voided.reason` «سُجّلت مرتين» and `voided.by.name`.
2. Reception `GET …/payments` → `[]`, totals all 0 (no payment today, A1).
3. Reception `GET …/payments?from=<today>&to=<today>` → 403.
4. Reception `POST …/payments { visitId: <رامي's>, amountAgorot: 500, method: CASH }` (a key) → 201; reception `GET
   …/payments` → that one, totals 500 cash.
5. Reception `POST …/payments/<id>/void { reason }` → 403.
6. Owner voids «هبة»'s payment (reason R1) → 200 voided; again with reason R2 → 200, reason R1; `GET
   …/uncollected-visits` → «هبة»'s visit, balance 1,500.
7. The directory owner on the demo space's `GET …/payments` and the void → 404.
8. Owner voids case 4's payment → 200; reception `GET …/payments` → it, marked voided by the owner; totals received 0,
   voided 1 / 500.
9. Reception pays 500 more on «رامي»'s visit (a key) → 201; owner `POST …/visits/<id>/write-off { reason }` → 200;
   owner voids that 500 → 409 `VISIT_WRITTEN_OFF`; owner `DELETE …/write-off` → 200; the void again → 200.
- `SELECT action, entity_id FROM audit_logs ORDER BY id DESC LIMIT 12` (three or four `payment.voided`, no
  duplicate for case 6's second call); `SELECT id, voided_at IS NOT NULL, void_reason FROM payments WHERE space_id
  = …`.
- Stop the server by its process ids (the `tsx watch` child, the server, `pino-pretty`); `Get-NetTCPConnection
  -LocalPort 3321 -ErrorAction SilentlyContinue` prints nothing.

### 12.7 The PR number, push and PR
Just before the push: `scripts\prnum.sh` modelled on `WORKER_B\SUBSCRIPTIONS\scripts\prnum-fix109.sh` (branch
`feat/payments`, its backup branch, the description `scripts\pr-body.md`), run with the expected number: it computes
the next number, rewrites `#PRNUM` in `docs` of every commit (`filter-branch --tree-filter`), deletes
`refs/original`, refuses if `#PRNUM` remains or the rewrite changed more than the number, and prints `PRNUM OK #<n>`
or `PRNUM STOP: …`. Then `npm run check:links; npm run format:check`; `git push -u origin feat/payments`.
- `gh label list`: `feat`, `area:api`, `area:docs`, `area:web` must exist (create a missing one with a description and colour).
- At once:
  ```powershell
  gh pr create --assignee @me --label feat --label area:api --label area:docs --label area:web `
    --title "feat(payments): void payments and list them" --body-file C:\dev\masaha\workspace\WORKER_B\PAYMENTS\scripts\pr-body.md
  ```
- GitHub's number must equal `n`; if not, fix the documents (a fixup into the commits that hold it) and `git push
  --force-with-lease`.

### 12.8 CI, CLEAN, conflicts, report
- `gh pr checks <n> --watch` (bounded), then `gh pr view <n> --json headRefOid,mergeStateStatus`: green **on the
  pushed head** (= `git rev-parse HEAD`) and `CLEAN`. Never merge; never rebase a `CLEAN` PR.
- **Conflicts:** for every other open PR, `git merge-tree --write-tree HEAD <its headRefOid>`; record clean or the
  conflicted paths. Documents only: the fast path when its turn comes. Code: stop and ask.
- **The report**, `4_REPORT_PR1.md` in this folder, written **as the work goes**: after the first checks, after each
  commit (sha, subject with its length, red, green), after each break, after the real run, after the push. It holds
  each command run or not, §12.2's results, the owner's answers to §13 as built, problems and their solutions,
  anything unexpected, the conflict check, every departure with why.
- **Write nothing outside the repository** except this folder's report and `scripts\`.
- **Never leave silently:** an executor that would leave a carried item, a review nit or a planned break undone
  stops and asks.

### 12.9 The PR description
```markdown
## Summary
The owner voids a payment with a reason (idempotent, audited; a written-off visit's payment once the write-off is undone); the payments list: the owner's ledger by Gaza days, staff, method, kind and void, with its totals; reception's own payments of today. A visit closed by hand with no customer that owes after a void is uncollected.

### Carried from #112
- start now holds the 365-day bound (`start()`, its test red first);
- conventions §9's announcements bullet moved; `announcements.md` states the public read; the contract's "will read" and the retry-after-delete line; `#112` last in `desk.md` and `subscriptions.md`.

## Scope / Acceptance criteria / Out of scope
<§2>

## Change type
feat — API code, the shared contract, tests and documents; a migration (the payments' change trigger replaced: a written-off visit's payment is voided once the write-off is undone). No new error code; `VISIT_WRITTEN_OFF`'s two catalogue lines reworded to cover a void (the Arabic for the owner's approval: <Q6's line>).

## Evidence
- `lint`, `typecheck` (each commit), `test:unit`, `test:api`, `format:check`, `check:links`, `build -w @masaha/shared`: <results>.
- Seen failing first: <each test, its red line>.
- Deliberate breaks, each red then restored: <B1–B24>.
- Real run on 3321: <statuses>.
- Not run locally (CI judges): `test:component`, the web's `build`, `check:build`, `check:classes` — the web change is one catalogue line per language.

## Screenshots
None: API and documents only.

## Definition of Done checklist
- [x] Acceptance criteria met, scope kept.
- [x] Lint and typecheck clean; `packages/shared` builds.
- [x] Tests added in the owning lanes, each seen failing.
- [x] No hardcoded user-facing text (codes only).
- [x] Authorization on the server (the boundary, `requireCan('payments.void')`, `can()` under the lock, the list's narrowing).
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

**The owner's standing exception — memory:** a full lane **killed for low memory** is re-run **once** when the
machine is quieter (no `vitest` of `C:\dev\masaha\app\` running, the free memory recorded); killed again → record
it, carry on, and **CI's run of that lane on the pushed head is the judge** — red there → stop.

**A plan that proves false against the code:** stop, say exactly what and why, and offer the fix — do not choose it
yourself. **A break that stays green:** stop — unless it is plainly your own test's defect, or the plan's break
cannot change the outcome; then make the break that can, see it red, and state it as a departure. **Anything you
would leave undone: stop and ask** — never silently.

**Never claim a result you did not see:** a command passed only if you saw its own output say so; copy that line
(read it by its exit code, not the tail). A break counts only when you saw it red.

### Stop and ask
- `origin/main` changed a code file of §7 since `104d9d07`; an open PR edits one; a carried file contradicts this
  plan or names more items.
- Any change needed in `apps/web` beyond Q6's two catalogue lines, a dependency, a new error code, or a schema change beyond D9.
- More than about 60 files.
- The migration not creatable as §12.2 check 1 says; the trigger's locking clause refused in both forms.
- The level rule refusing an import of D1; Express not reaching the `GET` (check 4).
- A real-run case the demo data cannot hold (A1).
- A break that stays green (§12.5's exception aside).
- A failure not understood after three root-cause fixes; CI failing for a reason not reproduced locally after three.
- A conflict with another open PR in a code file.
- An item you would leave undone (a carried item, a review nit, a break).
- The owner's answer to §13 changing a test or a rule beyond what it says.

---

## 13. Decisions needed from the owner

1. **Q1 — what a void changes (decision 5):** nothing rewritten, every figure derived (D5); **S1** — a visit paid
   in full at a manual check-out with no customer, its payment voided, is listed uncollected; **S2** — a
   written-off visit's payment is not voided until the write-off is undone (the database's, `VISIT_WRITTEN_OFF`).
   *Recommended:* both. *Otherwise:* S1 → A5 (the void asks a phone) or nothing; S2 → A3 (the desk checks it, no
   migration) or A4 (allowed).
2. **Q2 — the void's idempotency and races (decision 6):** no key; a second void answers it as it is, the first
   reason kept; the space's lock, then the payment's row (`FOR UPDATE`), then the visit's in the trigger (D6, S7).
   *Recommended:* as written.
3. **Q3 — the list's shape (decision 7):** one route, `can()` narrowing reception to its own today, its other
   filters refused 403 (S6; A1 a separate route); paged 20 / 50 (§4); `from`–`to` Gaza days, both or neither, at
   most **92 days**, today by default (S5; A8 366); newest received first, then id; `kind` and `voided` filters
   (S4); `meta.totals` — received, by method, count, voided count and amount — over the filter but `voided` and
   the page (S3; A2 a summary route); each row the item, its customer, who recorded it and the void.
   *Recommended:* as written.
4. **Q4 — the cut (decision 8):** **one PR**, ≈ 44 files, six commits (two carried). *Why:* the void answers the
   list's row, and both edit the same contract section and capability; ≈ 44 files is under the size where a split
   helps the review. *Otherwise:* A7 — PR 1 the void and the uncollected (≈ 30), PR 2 the list (≈ 20).
5. **Q5 — the documents this proves wrong (decision 9), as proposals:** data model *Uncollected visits* and
   *Checked by the service* (S1), its ledger constraints and conventions §13 (S2), the contract's uncollected
   line (S1), conventions §9 (the uncollected line; the payments list). Applied only as approved with Q1.
6. **Q6 — no new error code; `VISIT_WRITTEN_OFF` reused for the void, its text reworded.** Its catalogue lines say
   today only "…before it takes a payment", which would mislead after a refused void. *Recommended* — the same
   key, both lines reworded (the Arabic for your approval):

   | Language | Today | Proposed |
   |---|---|---|
   | English | This visit was written off; the owner must undo the write-off before it takes a payment. | This visit was written off; the owner must undo the write-off before it takes a payment or one of its payments is voided. |
   | Arabic | سُجّلت هذه الزيارة «لن يُحصَّل»؛ يتراجع المالك عن ذلك أولًا قبل استلام أي دفعة لها. | سُجّلت هذه الزيارة «لن يُحصَّل»؛ يتراجع المالك عن ذلك أولًا قبل استلام أي دفعة لها أو إلغاء إحدى دفعاتها. |

   A void's other refusals are generic (403, 404, 422). *Otherwise:* a code of its own,
   `PAYMENT_VISIT_WRITTEN_OFF` (409), its own constraint name in the trigger and the translation table, and both
   catalogue lines (the `add-error-code` steps, §12.3).

---

## Appendix A — the documents, line by line (the commit in brackets)

Every new decision and history line ends with `<the day's date>, #PRNUM`; *Last Updated* on each document changed.

1. **`api-contract.md`** —
   - [C0a] `POST …/announcements/:announcementId/start`: "an end that would fall more than 365 days after now is
     refused, 422 `out_of_range` on `endsAt`".
   - [C0b] `GET …/announcements/summary`: "the owner's overview will read the same count"; `POST …/announcements`:
     "a retry of a deleted announcement answers it as it was, deleted from every read".
   - [C2] *Front desk (managed)*: the opening line names the void as the owner's (🏢); new `#### POST
     /manage/spaces/:spaceId/payments/:paymentId/void · 🏢` — body `{ reason }` (1–200, required); **200**
     `PaymentRow`; a voided payment answered as it is, its first reason kept, writing nothing; what it changes
     (counts nowhere; nothing rewritten; S1, S2); errors in order: `forbidden` (403) for reception at the route
     before the body, `validation` (422) on the body, `forbidden` for an owner whose link ended meanwhile,
     `not_found` (404) for a payment not the space's, `conflict` (409) `VISIT_WRITTEN_OFF`; audit `payment.voided`
     (`after`: `{ visitId | subscriptionId, amountAgorot, method, reason }`); `PaymentItem`, `PaymentRow`. The
     check-out's and `POST …/payments`' retry lines: "a retry after the payment was voided answers it as recorded;
     the sums show the void".
   - [C3] `GET …/uncollected-visits`: S1's sentence replacing "A manual check-out's visit is never listed…".
   - [C4] new `#### GET /manage/spaces/:spaceId/payments · 🧾`: the query (D2), the window (Gaza days, received),
     the order, the narrowing (reception's own today; its `from`, `to`, `recordedById` → 403), **200** a page of
     `PaymentRow` with `meta` the pagination and `totals`; `PaymentTotals`, `PaymentsMeta`; errors (`validation`,
     `forbidden`, `not_found`).
2. **`data-model.md`** — [C1] *Constraints › The payment ledger*: "…and a written-off visit takes no payment, nor is
   one of its payments voided until the write-off is undone (`payments_visit_written_off`)"; [C3] *Uncollected
   visits* and *Checked by the service* (S1).
3. **`conventions.md`** — [C0b] §9 *Composed reads*: the announcements bullet below the customers list's last
   sub-bullet; [C1] §13 *The ledger's rules*: the fourth rule both ways; [C2] §9 *The front desk*: "**the void of a
   payment** by the owner, under the space's lock then the payment's row"; [C3] §9 *Uncollected visits* (S1); [C4]
   §9 *Composed reads*: "**The payments list** → `payments`, naming its rows through `visits`, `subscriptions`,
   `customers` and `users`; reception's narrowed by `can()`".
4. **`security.md`** — *Authorization*: [C2] `requireCan('payments.void')` on the void, before the body; [C4] the
   payments list: the owner's whole, reception's own today, decided by `can('payments.read')` before any query.
5. **`docs/features/payments.md`** — [C1] *Owns*: the fourth rule both ways; [C2] *What it does* (the void's row,
   `lockIn`, `rowsOf`), *Reads* (+ `users`, `customers`, `subscriptions` for the names), *Behaviour* (the void),
   *Decisions* (S2, S7, the void in `desk`), *Code map*; [C3] *The uncollected visits* (S1), a *Revised* line on its
   decision; [C4] *What it does* (the list), *Who uses it* (the owner's ledger, reception's «دفعاتي اليوم»; no
   screen yet), *Behaviour* (the list, the window, the totals), *Decisions* (S3–S6), *History* (`#PRNUM`).
6. **`docs/features/desk.md`** — [C0b] `#112` last; [C2] the void's orchestration (*What it does*, *Behaviour*,
   *History*).
7. **`docs/features/announcements.md`** — [C0a] start now's bound (*Behaviour*; a *Revised* line under S5's
   decision); [C0b] the public read (item 2).
8. **`docs/features/subscriptions.md`** — [C0b] `#112` last; [C2] *Who uses it*: `namesOf` for the payments list.
9. **`visits.md`, `customers.md`, `users.md`** — [C2] *Who uses it*: `payments` (the list's names), only where the
   line does not already name it (`git grep -n "payments" docs/features/{visits,customers,users}.md` first).
10. **`v1-mvp.md`** — [C4] step 9 *Built*: "payments voided by the owner, a written-off visit's once the write-off is
    undone; the payments list, the owner's and reception's own today (#PRNUM) — step 9's API is complete; the screen
    remains"; the two route rows into the managed spaces' *Built* sentence.
11. **`overview.md`** — [C4] *Built*: a *Payments* line (on the API).
12. **`docs/README.md`** — [C4] only if its `payments.md` map line lists the capability's contents.

## Appendix B — Claude Code skills, only a map

| Step | Skill (if the executor is Claude Code) |
|---|---|
| §12.1, the branch | `start-work-item` (its git part) |
| Each test red first, each break | `superpowers:test-driven-development` (workflow §10) |
| A new error code (none planned; §12.3) | `add-error-code` |
| Any failure | `superpowers:systematic-debugging` |
| §12.4 before any claim | `superpowers:verification-before-completion` |
| §12.7–12.8 | `open-pr`, then `final-report` |

Only a map: the plan and the documents decide, and a skill that disagrees with them loses.
