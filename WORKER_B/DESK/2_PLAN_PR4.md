# DESK PR 4 — collecting a visit's debt, and writing one off (K6, DK-012), the API — the plan

> **Base:** `origin/main` at `abc28e73` (Merge #97, `feat/auto-checkout`, 2026-10-20). The prompt asked for a
> plan from `origin/main` + PR 3 at `e122b95d`. #97 merged while this plan was being written, and
> `git diff --stat e122b95d origin/main` is empty, so every file read at `e122b95d` is the same file on
> `main` now. **Worker:** B, `C:\dev\masaha\app-b`. **Folder:** `C:\dev\masaha\workspace\WORKER_B\DESK\`: this
> plan is `2_PLAN_PR4.md`, the report will be `4_REPORT_PR4.md`, and the executor's scripts go in `scripts\`
> (never committed).
> **One PR:** `feat/visit-debts`, about 45 files, one migration. It is over 25 files and touches
> authorization, money, a trigger and the schema, so it gets its own review conversation.
> **Read only from commit objects** (`git show`, `git grep`, `git ls-tree`). Nothing was run, built,
> installed or checked out. Where reading could not prove something, it is written as an **executor check**
> (§12.2), with what to do if it fails.
> **In parallel:** worker A's OWNER_SETUP (`apps/web`, `docs`). No code file is shared. Shared documents,
> each a likely text conflict: `docs/project/overview.md` (*Built* lines), `docs/architecture/findings/README.md`
> (findings 100 and 110 here; worker A numbers from 101), `docs/plans/v1-mvp.md` (step 7's and step 9's lines,
> the route table). The web's `errors.ts` catalogues are edited here, under worker B's licence (error lines
> only).
> **Finding numbers:** this PR records **110**. Folding finding 100 changes its status. Any other finding
> the executor records takes **111**, then 112, and so on.

> **Approved by the owner, 2026-10-20 — binding on the executor:**
> - **§13 as planned, Q1–Q7:** the four routes in `desk` (A1, A2 not taken); the three new codes and
>   `VISIT_NOT_PRICED`'s revised lines **with the Arabic as written** (A3 not taken); the migration with
>   the `CHECK` including "priced" (S4; A4 not taken) and the trigger's fourth rule (S1); ADR 0009's new row
>   with its *Revised* line; finding 100 folded (S2); S5's retry answer; finding 110 recorded.
> - **Carried from #97 first:** `0_CARRIED_FROM_97.md` exists — its items are this PR's **first two
>   commits** (`fix(jobs): keep closing stays past a failing one`; `fix(visits): close every stay by its
>   day's end` — the owner chose (b), widened: every stay due by 23:59 of its check-in's Gaza day). Its three
>   findings to record take **111, 112, 113**; this plan's own finding keeps **110**; any further one takes
>   114 and on (the block 110–119 is this PR's). The PR's description says "Carried from #97".

---

## 1. Summary

After this PR, the desk finishes a visit's money once the visit is closed. The API only:

- **Receive a payment** for a closed, priced visit: `POST /manage/spaces/:spaceId/payments` (🧾,
  `Idempotency-Key`). This is the build map's general route. Its body names the item (`visitId` now; step 8
  adds `subscriptionId`). The ledger checks every payment against the balance, so a payment above what is
  owed is refused (`PAYMENT_EXCEEDS_DUE`). Each payment records who took it. If part of the charge stays
  unpaid, the visit needs a customer: a phone finds or creates one, unless the visit already has a customer.
- **«تسجيل دينًا»** (DK-012): an uncollected visit with no customer becomes a customer's debt by a phone,
  with no payment. This is its own small route: `PUT …/visits/:visitId/customer`.
- **«لن يُحصَّل»** (K6), owner only (🏢): `POST …/visits/:visitId/write-off { reason }` writes off whatever is
  still owed on any closed, priced visit with a balance above zero. Payments already made stay. It is never a
  payment and never a deletion. `DELETE …/visits/:visitId/write-off` undoes it. Both are audited.
- **A written-off visit takes no payment.** The ledger's trigger refuses one with `VISIT_WRITTEN_OFF`, and
  the error line tells the desk to ask the owner to undo the write-off first. A written-off visit leaves the
  uncollected visits and the customer's debt.
- **Finding 100 folded:** the check-out and the new routes share one rule for an unpaid part, so a visit
  that already has a customer keeps that customer.

---

## 2. The contract

### Scope
1. Migration `visit_write_off`: `visits.written_off_at`, `written_off_by_id` (→ `users`) and
   `write_off_reason`, with a `CHECK` (§4 D2). `payments_guard_insert` is replaced so that a payment on a
   written-off visit raises `payments_visit_written_off`.
2. `DeskVisit.writeOff: { at, byId, reason } | null`, on every answer that carries a visit.
3. `POST /manage/spaces/:spaceId/payments` (🧾, `Idempotency-Key`): a visit's payment after its check-out.
4. `PUT /manage/spaces/:spaceId/visits/:visitId/customer` (🧾): «تسجيل دينًا».
5. `POST` and `DELETE /manage/spaces/:spaceId/visits/:visitId/write-off` (🏢): the write-off and its undo.
6. `can()`: a new action, `visits.writeOff`, for the owner only.
7. `GET …/uncollected-visits` leaves written-off visits out.
8. The check-out keeps a visit's customer (finding 100).
9. Error codes `VISIT_WRITTEN_OFF`, `VISIT_ALREADY_PAID` and `VISIT_HAS_CUSTOMER`. `VISIT_NOT_PRICED` is
   reused for the write-off, and both of its lines become general (§13 Q2).
10. Documents: the contract, the data model, conventions, security, ADR 0009's table, `payments.md`,
    `visits.md`, `desk.md`, the build map (step 7, step 9, the route table), `overview.md`, finding 100 and
    the new finding 110.

### Acceptance criteria
- [ ] A payment on a closed, priced visit is recorded with who took it and answered 201 with what remains.
      It is refused when above the balance (`PAYMENT_EXCEEDS_DUE`), on an unpriced visit
      (`VISIT_NOT_PRICED`), on a written-off visit (`VISIT_WRITTEN_OFF`), and on an open visit (409, no
      code). Each refusal comes from the ledger, writes nothing, and comes before any phone is asked for.
- [ ] If part stays unpaid and the visit has no customer, a phone is required (422). It finds or creates
      the customer. A visit that has a customer keeps it, and a phone that belongs to someone else is
      refused (`VISIT_HAS_CUSTOMER`). The same applies at the check-out (finding 100).
- [ ] A retry with the same key answers 201 with the first payment and records nothing. Two requests with
      one key at once record one payment. A key that paid another item is a conflict.
- [ ] «تسجيل دينًا» attaches the customer found or created by the phone, with no payment, and is audited.
      Sending the same phone again changes nothing. It is refused on a written-off visit
      (`VISIT_WRITTEN_OFF`), a paid one (`VISIT_ALREADY_PAID`), an open one (409), and one that already
      belongs to another customer (`VISIT_HAS_CUSTOMER`).
- [ ] The owner writes off the balance of any closed, priced visit with a required reason. The write-off
      records who, when and why, is audited, and leaves the payments as they were. An unpriced visit is
      refused (`VISIT_NOT_PRICED`), a settled one (`VISIT_ALREADY_PAID`), an open one (409). A second
      write-off answers the visit as it is. Reception is refused (403).
- [ ] Undoing a write-off clears it and is audited with what the write-off was. The visit is uncollected (or
      the customer's debt) again and may be paid. Undoing a visit that was not written off writes nothing.
- [ ] A written-off visit is not among the uncollected visits.
- [ ] Every write takes the space's lock first and decides `can()` on the links read under that lock.
      Each race in §4 D5 has its test and its break.

### Out of scope
- The desk's screen (its «غير محصّلة» tab, the dialogs) and every web change except the catalogue lines.
  That is worker A's later item.
- The shared desk device: idle sign-out and «تبديل الموظف». The owner moved it to the desk's screen item.
- Voids, the payments list (`GET …/payments`), collections per staff member, finance: step 9.
- A subscription's payment on the same route, and customer debt as a read (the customers list and file):
  step 8. This PR writes the data model's *Customer debt* line only.
- An amount spread over several items (ADR 0010 rule 2): step 8, with subscriptions.
- Finding 17's sweep: the next small item (A4 of the first plan).

---

## 3. The reading done, and what it changed

On `e122b95d` (= `origin/main`'s tree now): `CLAUDE.md`, `docs/development/workflow.md` and `testing.md`
(§3–§4); `docs/backend/conventions.md` (§2, §4, §6, §7–§9, §13); `security.md` (*Authorization*); ADR 0009 (its
table and *Revised* lines), ADR 0010, ADR 0015 (through conventions §13); `docs/architecture/data-model.md`
(whole: *Operations*, *Front desk and money*, *Constraints worth stating*, *Checked by the service*);
`docs/api/api-contract.md` (§1, §4, *Front desk (managed)*, §6); `docs/features/payments.md` and `desk.md`
(whole), `visits.md` (its sections); `docs/plans/v1-mvp.md` (steps 7–9, *Ordering notes*, the managed route
table); the findings index and finding 100; `C:\dev\masaha\workspace\WORKER_B\DESK\2_PLAN.md` (the approval
note, A3, §4, §5, §9, §12, §13), `3_EXEC_PROMPT_PR3.md` (§2–§5), `4_REPORT_PR3.md`;
`C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_DESK.md` (K6, DK-012, *Rules changed*); the code of
`payments`, `desk`, `visits` (service, repository, mapper, routes, controller, index), `customers`,
`shared/auth/can.ts`, `shared/errors/constraintCodes.ts`, `db/checkViolation.ts`, `shared/audit/writeAudit.ts`;
`packages/shared/src/{payments,desk,visits}/*`, `core/errors.ts`; `schema.prisma` (Customer, Visit, Payment,
AuditLog); migration `20261020074552_desk_visit_charge` (the current `payments_guard_insert`, whole);
`apps/api/test/{locks,factories}.ts`, `payments/uncollected.api.test.ts` (its fixtures),
`desk/checkOut.api.test.ts` (its titles and race pattern); the two web `errors.ts` catalogues (the `VISIT_*`
lines); the prototype's `desk-core.jsx` (`payVisit`, `attachDebt`, `writeOff`, `PayDialog`, the debt dialog,
`WriteOffDialog`, `UnpaidRow`) and `desk-data.js` (`unpaid`, `writtenOff`).

**What the reading changed:**
- **The route's owner is `desk`, not `payments`** (D1). The rule for an unpaid part (a phone leaves the debt
  to a customer) already lives in the desk's check-out. A second route that needs the same rule belongs to
  the same orchestrator, or the rule would end up with two homes.
- **Finding 100 is folded** (§6). The new routes need the rule that "a visit with a customer keeps it". The
  check-out has the opposite behaviour today, so writing the rule once means the check-out changes too.
- **The ledger's refusals answer before the phone is asked for** (D4). To have both the right codes and
  "services do not repeat the ledger's rules" (conventions §13), the payment is inserted before the
  customer is attached.
- **The prototype disagrees with the owner's decisions** in three places (finding 110): its write-off says
  "it can't be undone"; a partial payment of an uncollected visit leaves the rest "uncollected" with no
  phone; its uncollected list also holds manual check-outs left unpaid («خرج بدون دفع»), which the contract
  excludes. Recorded for the screen's item. Nothing here follows the prototype on these points.

---

## 4. The decisions as built

### The owner's decisions (2026-10-20), as built
- **O1, one PR:** C0 (only if `0_CARRIED_FROM_97.md` exists) and C1–C4 (§11). Not split.
- **O2, the general payment route:** `POST /manage/spaces/:spaceId/payments`, the body naming its item
  (`visitId`); `Idempotency-Key` (ADR 0015); only a closed, priced visit; never above the balance (the
  ledger); `recordedById` is the caller. An unpaid part follows *Unpaid visit*, unless the visit has a
  customer.
- **O3, «تسجيل دينًا»:** its own route, `PUT …/visits/:visitId/customer` (D1, why).
- **O4, the write-off:** owner only (`visits.writeOff`); any closed, priced visit with a balance above zero;
  the remainder only; a reason required; who, when and why recorded and audited; an unpriced visit refused
  with the existing `VISIT_NOT_PRICED` (D3).
- **O5, the undo:** owner only; it clears the three columns, and the audit keeps the write-off. A payment
  on a written-off visit is refused with `VISIT_WRITTEN_OFF`.
- **O6, what a write-off changes:** the visit leaves the uncollected visits now, and the debt by the data
  model's definition (the debt read comes in step 8).
- **O7, the documents:** Appendix A.
- **O8, not here:** §2 *Out of scope*.

### D1 — the routes and their answers
| Route | Access | Body | 2xx answer |
|---|---|---|---|
| `POST /manage/spaces/:spaceId/payments` | 🧾 `requireCan('payments.record')`, `Idempotency-Key` | `{ visitId, amountAgorot, method, note?, phone?, customerName? }` (`receivePaymentSchema`) | **201** `ReceivedPayment = { visit: DeskVisit, payment: VisitPayment, paidAgorot, balanceAgorot }` |
| `PUT /manage/spaces/:spaceId/visits/:visitId/customer` | 🧾 `requireCan('payments.record')` | `{ phone, customerName? }` (`leaveToCustomerSchema`) | **200** `DeskVisit` |
| `POST /manage/spaces/:spaceId/visits/:visitId/write-off` | 🏢 `requireCan('visits.writeOff')` | `{ reason }` (`writeOffVisitSchema`) | **200** `DeskVisit` |
| `DELETE /manage/spaces/:spaceId/visits/:visitId/write-off` | 🏢 `requireCan('visits.writeOff')` | — | **200** `DeskVisit` |

- **Why these shapes.**
  - **`visitId` in the body, flat.** It mirrors the ledger's "exactly one of `visit_id` or
    `subscription_id`". Step 8 adds `subscriptionId` with an "exactly one" refinement, which breaks no
    client.
  - **«تسجيل دينًا» as its own `PUT`, not the payment route with no amount.** A `POST /payments` that records
    no payment would answer "created" for nothing and spend an idempotency key on no row. Setting the
    visit's customer is idempotent by design: the same phone finds the same customer under the space's
    lock, which is the customers' "find or create" of #95. So it needs no key, as conventions §13 says
    of updates (customers have no key until step 8).
  - **The write-off as a sub-resource: `POST` creates it, `DELETE` undoes it.**
- **Where they live: `desk`** (L5), beside the check-out (conventions §9 *The front desk*, R4). Each route
  spans `visits` (the lock, the state, the columns), `customers` (found or created) and `payments` (the
  insert, the balance), in one transaction. The rule for an unpaid part keeps one home. The future
  `GET /payments` (step 9) is a read, so it goes on `payments`' router. One path split across two routers by
  method is fine in Express.
- **`payments.record`** (the staff's, already in the table) guards both desk routes. «تسجيل دينًا» is a
  money item, not a customer edit.
- **The answers.** `paidAgorot` and `balanceAgorot` are computed as of the answer. A retry answers the first
  payment and the visit, with those two **as of the retry**: the same rule as S3 of #95 (they describe now,
  not the payment), stated in the contract.
- **Write-off and undo are idempotent by design:** a second write-off answers the visit as it is (the first
  reason kept, nothing written, nothing audited), and so does an undo with nothing to undo. This follows
  "a repeated check-out returns the closed record" and the override's `DELETE`.

### D2 — the schema
- `Visit` gains `writtenOffAt DateTime? @map("written_off_at") @db.Timestamptz(3)`,
  `writtenOffById Int? @map("written_off_by_id")` (relation `writtenOffBy User? @relation("VisitWrittenOffBy",
  …, onDelete: Restrict)`; `User` gains `visitsWrittenOff Visit[] @relation("VisitWrittenOffBy")`) and
  `writeOffReason String? @map("write_off_reason")`, each with a `///` line.
- **`visits_write_off_check`:** the three columns are set together, the reason is never blank, and only a
  closed, priced visit can be written off:
  ```sql
  ALTER TABLE "visits" ADD CONSTRAINT "visits_write_off_check"
    CHECK (
      ("written_off_at" IS NULL) = ("written_off_by_id" IS NULL)
      AND ("written_off_at" IS NULL) = ("write_off_reason" IS NULL)
      AND ("write_off_reason" IS NULL OR btrim("write_off_reason") <> '')
      AND ("written_off_at" IS NULL OR ("checked_out_at" IS NOT NULL AND "charge_agorot" IS NOT NULL))
    );
  ```
  *Why in the database:* the same shape as the typed charge's reason (`visits_charge_reason_check`). The
  service checks the same states first and answers their codes; the `CHECK` is the backstop, and reaching
  it would be a bug (500).
- **Undo clears the three columns.** The history lives in the audit: `visit.writtenOff`, then
  `visit.writeOffUndone` with `before` set to what it was. *Why:* one write-off at a time, and the audit is
  already the record of who did what. A history table would be a second record. *Cost:* a re-write-off
  after an undo overwrites the columns, which is fine because the audit keeps both.
- **No index:** the uncollected read already filters a space's auto-closed visits through
  `@@index([spaceId, checkedOutAt])`.

### D3 — the codes
| Code | Type | Raised by | When |
|---|---|---|---|
| `VISIT_WRITTEN_OFF` (new) | 409 | the ledger (`payments_visit_written_off` → the translation table); «تسجيل دينًا»'s service | a payment, or a debt by phone, on a written-off visit |
| `VISIT_ALREADY_PAID` (new) | 409 | the write-off's and «تسجيل دينًا»'s services | the visit's balance is ≤ 0: nothing to write off or leave to anyone |
| `VISIT_HAS_CUSTOMER` (new) | 409 | the desk's unpaid-part rule (check-out, payment, «تسجيل دينًا») | the phone finds or would create a customer other than the visit's |
| `VISIT_NOT_PRICED` (reused) | 409 | the ledger (payments, as today); the write-off's service | a payment on, or a write-off of, a visit with no charge |
| `PAYMENT_EXCEEDS_DUE` (as is) | 409 | the ledger | above the balance |

- **A second write-off is not an error**, so it gets no code (D1). An open visit is 409 with no code, as
  the pricing route does: it is paid, or left to a customer, at its check-out.
- **`VISIT_NOT_PRICED` is reused**, not a new code. It is one rule (a visit with no price is priced first).
  Its approved lines speak of a payment only, so both become general: §13 Q2, for the owner's approval.
- **Why `VISIT_ALREADY_PAID` and not 409 with no code:** two desks can collect the last part while the owner
  writes the visit off. That is a race the user can see, not a client bug.

### D4 — each write's order of checks (all in one transaction, the space's lock first)
**Common opening** (`lockAtDesk(actor, space, tx, action)`, the check-out's helper given the action):
`spaces.lock` (404 when gone), then `linksUnder(tx)`, then `can(actor, action, { links })` (403).

**`receivePayment`** (`payments.record`):
1. `visits.lockIn(space.id, visitId, tx)` (`FOR UPDATE`; not the space's → 404).
2. `payments.findByKey(space.id, key, tx)`: for another item → 409 (no code); for this visit → the retry's
   answer (the first payment, the visit as it is now, the paid and the balance now).
3. Visit open → 409 (no code).
4. `payments.recordForVisit(…)`. The trigger refuses, in its order: written off (`VISIT_WRITTEN_OFF`), no
   charge (`VISIT_NOT_PRICED`), above the balance (`PAYMENT_EXCEEDS_DUE`). The service repeats none of
   them (conventions §13).
5. `payments.balancesOf(space.id, [{ id, chargeAgorot }], tx)`: what remains after this payment.
6. If anything remains, then `customerFor(...)`, the unpaid-part rule (below), and the visit's customer is
   set if it changed (`visits.leaveTo`).
7. Answer `{ visit, payment, paidAgorot, balanceAgorot }`.

**`leaveToCustomer`** (`payments.record`, «تسجيل دينًا»):
1. `lockIn` → 404.
2. Open → 409.
3. Written off → `VISIT_WRITTEN_OFF` (this is the debt's own rule; no payment is inserted, so no trigger
   runs).
4. `balancesOf` → a balance ≤ 0 → `VISIT_ALREADY_PAID`. An unpriced visit (no balance) is allowed: its debt
   gets a customer before it is priced, as at an unpriced close.
5. `customerFor(...)`. The same customer as the visit's → answer the visit and write nothing.
6. `visits.leaveTo(…)`, audited `visit.leftToCustomer` (`after: { customerId }`), plus `customer.created`
   when the customer is new.

**`writeOff`** (`visits.writeOff`):
1. `lockIn` → 404.
2. Open → 409.
3. Already written off → answer the visit, write nothing.
4. No charge → `VISIT_NOT_PRICED`.
5. `balancesOf` → ≤ 0 → `VISIT_ALREADY_PAID`.
6. `visits.writeOff(…, { at: now(), byId: actor.id, reason, balanceAgorot })`, audited `visit.writtenOff`
   (`after: { reason, balanceAgorot }`: the amount written off).

**`undoWriteOff`** (`visits.writeOff`):
1. `lockIn` → 404.
2. Not written off → answer the visit, write nothing.
3. `visits.undoWriteOff(…)`, audited `visit.writeOffUndone` (`before: { writtenOffAt, writtenOffById,
   reason }`).

**The unpaid-part rule, one helper in `desk`** (`customerFor(actor, space, locked, { phone, customerName },
tx)`), used by the check-out, the payment and «تسجيل دينًا»:
- **The visit has a customer:** no phone is needed. A phone sent that finds a customer other than the
  visit's, or finds none (and so would create one), → `VISIT_HAS_CUSTOMER`. Otherwise the visit's customer.
- **The visit has none:** a phone is required (422 `required` on `phone`). `customers.findOrCreateByPhone`
  with `customerName ?? locked.visitorName ?? ''`. The `''` cannot happen: a visit with no customer has a
  name, by the `CHECK` "a name or a customer".

**Lock order:** the space's row, the visit's row (the trigger's `FOR UPDATE` on the same row, already held),
the payment, then the customer. Under the space's lock, every desk write at the space runs in turn, so the
payment-then-customer order of `receivePayment` cannot cross the check-out's customer-then-payment order.

### D5 — the races, each with its test (§9)
| Race | What decides | Test |
|---|---|---|
| Two desks collect one visit, two keys | The space's lock serialises them. The second's insert sees the first's payment (the trigger sums under the visit's row lock), and its balance is read inside the transaction | T21 |
| One key sent twice at once | The key is read first, under the space's lock; the unique key is the backstop | T20 |
| A payment while the owner writes the visit off | Write-off first → the payment's insert meets the trigger (`VISIT_WRITTEN_OFF`); payment first → the write-off writes off only the rest, or `VISIT_ALREADY_PAID` | T22, T9 |
| Two desks record the debt to two phones | The second, under the lock, sees the first's customer → `VISIT_HAS_CUSTOMER` | T33 |
| A link ended while a write waits | `can()` on the links read under the space's lock → 403 | T5, T23, T32 |

### D6 — the uncollected read
`visits.autoClosedIn` and `autoClosedPage` gain `writtenOffAt: null` in their `where` (the same filter in
both, so the settled ids and the page come from the same set).

### D7 — the shared package
- `@masaha/shared/visits`:
  - `writeOffVisitSchema = z.object({ reason: textSchema(1, WRITE_OFF_REASON_MAX_LENGTH) })`, with
    `WRITE_OFF_REASON_MAX_LENGTH = 200`, and `WriteOffVisitRequest`;
  - `VisitWriteOff = { at: string; byId: number; reason: string }`;
  - `DeskVisit` gains `writeOff: VisitWriteOff | null`.
- `@masaha/shared/desk`:
  - `receivePaymentSchema = paymentSchema.extend({ visitId: positive whole id; phone: phoneSchema.optional();
    customerName: textSchema(1, VISITOR_NAME_MAX_LENGTH).optional() })`, `ReceivePaymentRequest`;
  - `leaveToCustomerSchema = z.object({ phone: phoneSchema; customerName: textSchema(1,
    VISITOR_NAME_MAX_LENGTH).optional() })`, `LeaveToCustomerRequest`;
  - `ReceivedPayment = { visit: DeskVisit; payment: VisitPayment; paidAgorot: number; balanceAgorot:
    number }`.
- The positive id: whatever `checkInVisitSchema`'s `shiftId` uses (executor check 5).

---

## 5. Stronger decisions, and Proposed alternatives

### S1 — the written-off refusal lives in the ledger's trigger — **recommended, planned**
The prompt says "a payment on a written-off visit is refused". This plan puts that rule in
`payments_guard_insert`, as a fourth rule beside "within the due" and "once charged". *Why:* conventions §13
gives the ledger's rules to the database alone, so every future insert path is covered by one rule (step 8's
subscriptions do not touch it; step 9's routes would). The trigger already locks the visit's row, so the
race with a write-off is decided there. *Cost:* the function is copied whole once more in the migration, and
there is one more database test. *Alternative:* the desk's service checks `writtenOffAt` under the visit's
lock. That is simpler, but it would be a ledger rule held in a service.

### S2 — finding 100 folded: one unpaid-part rule for the check-out and the new routes — **recommended, planned**
The owner's decision 2 says "unless the visit already has one" for the payment route. The check-out does the
opposite today. Writing one helper resolves the finding at no extra code. *Cost:* one check-out test (a
visit given a customer by the factory), the finding's status and resolution line, and its index line moved.

### S3 — the payment is inserted before the customer is attached — **recommended, planned**
This keeps the ledger's code first: an unpriced or written-off visit, or an amount too high, answers its
409 rather than a 422 for the phone. And no service repeats the trigger's checks. *Cost:* the lock order
written in `desk.md` changes from "the customer, the payment" to "the payment, the customer" for this route,
and is stated. A 422 on the phone, raised after the insert, rolls the insert back.

### S4 — the write-off's shape in a `CHECK` — **recommended, planned**
Together, never blank, only on a closed and priced visit (D2). This is stronger than the prompt's
"together, non-blank, only on a closed visit": "priced" is added, so the rule that an unpriced visit is
priced first holds in the database too.

### S5 — a retried payment answers the paid amount and the balance as of now — **weakens ADR 0015's "same body", stated**
The payment and the visit are the first ones. The two sums describe now, as #95's warnings do. *Alternative:*
store nothing and answer only `{ visit, payment }`; the desk would then read the balance from
`uncollected-visits` or the customer file. **Recommended as planned:** the toast «المتبقي …» needs the sum,
on a weak connection.

### Rules the item touches, stated
- **ADR 0009's table** gains a row: "Write off a visit's unpaid rest that will not be collected, with a
  reason; undo it | – | ✓", with a *Revised* line (2026-10-20, K6, #PRNUM). This is a decision-level line,
  per the ADR style. §13 Q4.
- **ADR 0010 is unchanged.** A write-off is not a payment, so the ledger's decisions stand. The data model
  owns what a write-off removes from the debt (K6's *Rules changed*: data model only).
- **Conventions §9 *The front desk*** gains: "receiving a visit's payment after its check-out; leaving its
  debt to a customer by phone; its write-off and undo". The level map is unchanged.
- **Conventions §13 *The ledger's rules*:** "the three payment rules" becomes four: "… and a written-off visit
  takes no payment".

### Proposed alternatives (the owner may prefer them)
- **A1 — the routes in `payments`, not `desk`.** *What:* `payments` (L4, above `visits` and `customers`)
  orchestrates the payment, the debt and the write-off. *Why:* it owns the ledger, the balance and the debt;
  the build map's `/payments` would be one module's. *Cost:* the unpaid-part rule would live in two modules
  (the check-out stays in `desk`), unless the check-out's part moves too, which is a refactor of #95's code.
  **Not recommended.**
- **A2 — «تسجيل دينًا» on the payment route with no amount.** *What:* `POST /payments { visitId, phone }`, with
  no `amountAgorot`. *Why:* one route for the desk's "collect" dialog. *Cost:* a 201 with no payment, a key
  spent on nothing, and an optional amount on a ledger route. **Not recommended.**
- **A3 — a code of its own for the unpriced write-off** (`WRITE_OFF_NOT_PRICED`), so `VISIT_NOT_PRICED`'s
  approved lines stay as they are. *Cost:* one more code, and two lines to approve instead of two revised.
- **A4 — no `CHECK` for "priced"** (S4 weaker), if the owner prefers the prompt's wording to the letter.
  Not recommended.

---

## 6. Related findings
| Finding | Folded? | Why, and the cost |
|---|---|---|
| **100** An unpaid check-out moves a visit's customer to the phone's | **Yes** (S2), C3 | The payment route needs "a visit with a customer keeps it". One helper resolves both. Status → Resolved, a resolution line (2026-10-20, #PRNUM), the index line moved under *Resolved* |
| **110** (new) The desk prototype's uncollected visits disagree with the owner's decisions | Recorded, C2 | Evidence: `desk-core.jsx` `WriteOffDialog` says the write-off "can't be undone" (the owner made it reversible); `PayDialog`'s `remainder="uncollected"` leaves a partial payment's rest with no phone (the owner requires one); `desk-data.js`'s `unpaid` lists «خرج بدون دفع» visits, which the contract keeps out of the uncollected visits. *Resolves when:* the desk's screen item builds the tab and the dialogs to the contract, or the prototype is corrected first. No prototype edit here: it is worker A's design archive |
| **17** Expired counters and sessions never swept | No | The next small item (A4 of the first plan, taken) |
| **97** The visit-rounding rule is written twice | No | It concerns settings validation, which this PR does not touch |
| **77** The race helper counts any waiting backend | No | The new races use `whileHeld` / `waitingOnLock`, as the existing ones do |

---

## 7. The files it edits

Only `apps/api`, `packages/shared`, `docs`, and the two web catalogues (worker B's licence: the error
lines). No dependency, no `package.json`.

| Area | Files |
|---|---|
| Schema | `apps/api/prisma/schema.prisma`; + `apps/api/prisma/migrations/<ts>_visit_write_off/migration.sql` |
| DB tests | `apps/api/src/db/front-desk.api.test.ts`, `apps/api/src/db/payments.api.test.ts` |
| Shared | `packages/shared/src/core/errors.ts`; `visits/{requests,responses}.ts`, `visits/requests.unit.test.ts`; `desk/{requests,responses}.ts`, `desk/requests.unit.test.ts` |
| Web (catalogues only) | `apps/web/src/shared/copy/{arabic,english}/errors.ts` |
| Platform | `apps/api/src/shared/auth/can.ts`, `can.unit.test.ts`; `apps/api/src/shared/errors/constraintCodes.ts` |
| `visits` | `visits.repository.ts`, `visits.service.ts`, `visits.mapper.ts`, `index.ts` (if a type is exported) |
| `payments` | `payments.repository.ts` (`paidFor` takes `tx?`), `payments.service.ts` (`balancesOf`, `uncollectedIn` unchanged) |
| `desk` | `desk.service.ts`, `desk.controller.ts`, `desk.manage.routes.ts`; + `desk/payments.api.test.ts`, + `desk/debt.api.test.ts`, + `desk/writeOff.api.test.ts`; `desk/checkOut.api.test.ts` |
| Existing tests whose exact visits gain `writeOff: null` | as found by check 4: of `checkIn`, `checkOut`, `visits`, `unpriced`, `uncollected`, `autoCheckOut`, `jobs` and the seed's `.api.test.ts`, only those that `toEqual` a whole `DeskVisit` |
| `payments` test | `payments/uncollected.api.test.ts` (the written-off visit left out) |
| Docs | `docs/api/api-contract.md`, `docs/architecture/data-model.md`, `docs/backend/conventions.md`, `docs/backend/security.md`, `docs/architecture/decisions/0009-space-scoped-reception-role.md`, `docs/features/{payments,visits,desk}.md`, `docs/plans/v1-mvp.md`, `docs/project/overview.md`, finding 100, + finding 110, `docs/architecture/findings/README.md`; `docs/README.md` only if its map lines for `desk.md`/`payments.md` name what is built (check 9) |

About 40–48 files. Over about 70 → stop and ask.

---

## 8. Design issues

No screen is built. The design points the API serves, or departs from, are in finding 110 (the prototype's
write-off "can't be undone"; the remainder with no phone; manual check-outs in its uncollected list).
Worker A's screen item will need them.

---

## 9. Tests — lane, title, the break each catches

Every test is seen failing first in its own lane, and every expectation is written by hand. Fixed clock
through `createTestApp({ clock })`; instants are written with their offset. Roles in each API file: the
owner, reception of this space, a stranger, an owner of another space, the admin. The B-numbers are §12.5's
breaks, each run once with its red lines recorded.

### Unit
- **U1** `can.unit.test.ts` [C2]: `visits.writeOff: the space's owner only` (six actors: USER, reception
  here, reception elsewhere, owner elsewhere, owner here, ADMIN). **B1:** `'visits.writeOff': 'staff'`.
- **U2** `packages/shared/src/visits/requests.unit.test.ts` [C2]: `a write-off takes a reason of 1–200
  characters, never blank` (`required`, `too_short` / whatever `textSchema` answers for blank, `too_long`).
  **B2:** `reason: z.string()`.
- **U3** `packages/shared/src/desk/requests.unit.test.ts` [C3]: `a payment names its visit and takes the
  payment's bounds, and an optional phone and name` (missing `visitId` → `required`; `0` →
  `out_of_range`/the id rule; a bad phone → `invalid_format`). **B3:** `visitId` optional.
- **U4** same file [C4]: `a debt by phone needs the phone` (`required`, `invalid_format`). **B4:**
  `phone: phoneSchema.optional()`.

### API — `apps/api/src/db/front-desk.api.test.ts` [C1]
- **D1** `a write-off has its time, who and a non-blank reason together, only on a closed, priced visit`
  (raw updates of a visit, each refused `visits_write_off_check`: one column alone; a blank reason; on an
  open visit; on an unpriced one; all three on a closed priced one accepted). **B5 (database):** `ALTER TABLE
  visits DROP CONSTRAINT visits_write_off_check` on `masaha_b_test`, restored after.

### API — `apps/api/src/db/payments.api.test.ts` [C1]
- **D2** `a written-off visit takes no payment: payments_visit_written_off; once undone it does` (insert
  refused while written off; the columns cleared, the same insert accepted). **B6 (database):** the function
  of `20261020074552_desk_visit_charge` restored by `CREATE OR REPLACE` on `masaha_b_test`; restored after
  with the new migration's function.

### API — `apps/api/src/modules/desk/writeOff.api.test.ts` [C2]
- **T1** `the owner writes off an uncollected visit's balance with a reason: answered with its write-off, gone
  from the uncollected visits, audited visit.writtenOff` (`after: { reason, balanceAgorot }`). **B7:**
  `writtenOffAt: null` dropped from `autoClosedPage` (the page and its count).
- **T2** `a partly paid visit has only its remainder written off; its payments stay` (audit `balanceAgorot` =
  charge − paid; the payment rows unchanged). **B8:** the balance taken as the charge (paid ignored).
- **T3** `a customer's unpaid visit from a manual check-out is written off too`. **B9:** the write-off
  refused unless `checkoutMethod` is `AUTO`.
- **T4** `refuses reception with 403 before the body is read; a stranger, another space's owner and the admin
  with not_found` (reception sends an invalid body and gets 403, not 422). **B10:** the route's
  `requireCan('visits.writeOff')` removed (reception's invalid body then answers 422).
- **T5** `an owner whose link ended while the write-off waited on the space's lock is refused 403, writing
  nothing` (`whileHeld`). **B11:** `can()` on `space.links` instead of `linksUnder(tx)`.
- **T6** `refuses an unpriced visit (409 VISIT_NOT_PRICED), an open one (409), a paid one (409
  VISIT_ALREADY_PAID), writing nothing`. **B12:** the no-charge check removed (the `CHECK` then answers
  500). **B13:** the balance check removed (→ 200).
- **T7** `a second write-off answers the visit as it is: the first reason kept, nothing audited`. **B14:**
  the "already written off" branch removed.
- **T8** `refuses a missing or blank reason with 422 before anything is read`. **B15:** `validate` removed.
- **T9** `a payment committed while the write-off waits: only the rest is written off; a full one refuses it
  VISIT_ALREADY_PAID` (`whileHeld`: the test holds the space's row and inserts a payment meanwhile).
  **B16:** the balance read before `lockAtDesk` (outside the transaction).
- **T10** `the owner undoes a write-off: cleared, uncollected again, audited visit.writeOffUndone with what it
  was` (`before: { writtenOffAt, writtenOffById, reason }`). **B17:** the undo writes the audit but does not
  clear the columns.
- **T11** `undoing a visit not written off answers it as it is, writing nothing`. **B18:** the
  "not written off" branch removed (an audit is written).
- **T12** `reception may not undo (403); the space's other routes still answer it` (`DELETE` as reception →
  403). Covered by B1 (the action is the one rule).

### API — `apps/api/src/modules/desk/payments.api.test.ts` [C3]
- **T13** `the staff receive a payment for an uncollected visit: 201, recorded with who took it, with what
  was paid and what remains; audited payment.recorded`. **B19:** `balanceAgorot` read before the insert.
- **T14** `paid in full, the visit leaves the uncollected visits`. No break of its own: B19 and the existing
  B5 of #97 cover the rule.
- **T15** `a part left unpaid on a visit with no customer needs a phone (422 required, writing nothing); with
  one, the customer is found or created, audited customer.created`. **B20:** the phone rule skipped.
- **T16** `a visit with a customer keeps it: no phone needed; another customer's phone is refused 409
  VISIT_HAS_CUSTOMER, writing nothing`. **B21:** the helper writes the phone's customer over the visit's
  (#95's behaviour).
- **T17** `the ledger refuses, before any phone is asked: above the balance PAYMENT_EXCEEDS_DUE; an unpriced
  visit VISIT_NOT_PRICED; a written-off one VISIT_WRITTEN_OFF — each writing nothing` (each sent with no
  phone and leaving a rest). **B22:** the phone rule moved before the insert (→ 422). **B23:** the
  `payments_visit_written_off` line removed from `CONSTRAINT_CODES` (→ 500).
- **T18** `an open visit is refused 409 with no code: it is paid at its check-out`. **B24:** the open check
  removed (the trigger then answers `VISIT_NOT_PRICED`).
- **T19** `a retry with the same key answers 201 with the first payment and records nothing; a key that paid
  another item is a conflict`. **B25:** `findByKey` removed (→ 500 on the unique key).
- **T20** `two requests with one key at once record one payment, both answered 201 with it` (the
  check-out's two-request race pattern, `waitingOnLock({ count: 2 })` or as T-PR2-8 did). **B26:** the
  space's lock removed from `lockAtDesk` for this route.
- **T21** `two desks at once: the second sees the first's payment, so its rest is settled and needs no phone`
  (`whileHeld`: hold the space's row, insert 1,000 of a 2,000 charge meanwhile; the request pays 1,000 with
  no phone → 201, balance 0). **B27:** the balance read outside the transaction, before the lock (→ 422).
- **T22** `a payment waiting while the owner writes the visit off is refused VISIT_WRITTEN_OFF` (`whileHeld`:
  the write-off's three columns set meanwhile). **B6** (the database function restored) turns it to 201 too;
  record it on this test as well.
- **T23** `a reception link ended while the payment waits is refused 403, writing nothing`. **B28:** `can()`
  on `space.links`.
- **T24** `answers the owner and reception; refuses a stranger, another space's owner and the admin with
  not_found; a visit of another space is not_found`. **B29:** `requireCan('visits.writeOff')` on this route
  (reception → 403).
- **T25** `refuses a missing or invalid key, and an invalid body, with 422 before anything is read`.
  **B30:** `requireIdempotencyKey` removed.

### API — `apps/api/src/modules/desk/checkOut.api.test.ts` [C3]
- **T26** `a visit with a customer keeps it at an unpaid check-out; another customer's phone is refused 409
  VISIT_HAS_CUSTOMER` (the open visit created with `customerId` by the factory). **B31:** the check-out's own
  `findOrCreateByPhone` call restored (#95's code).

### API — `apps/api/src/modules/desk/debt.api.test.ts` [C4]
- **T27** `the staff record an uncollected visit as the debt of the phone's customer, found or created; it
  stays uncollected, with its customer; audited visit.leftToCustomer`. **B32:** `visits.leaveTo` not called.
- **T28** `an unpriced visit can be recorded as a debt` (before it is priced). **B33:** a no-charge refusal
  added.
- **T29** `the same phone again answers the visit as it is, writing nothing; another phone is refused 409
  VISIT_HAS_CUSTOMER`. **B34:** the "same customer" branch removed (a second audit).
- **T30** `refuses a written-off visit VISIT_WRITTEN_OFF, a paid one VISIT_ALREADY_PAID, an open one 409,
  writing nothing`. **B35:** the written-off check removed. **B36:** the balance check removed.
- **T31** `refuses a missing or malformed phone with 422 before anything is read`. **B37:** `validate`
  removed.
- **T32** `answers the owner and reception; not_found to the three others; a reception link ended meanwhile →
  403`. **B38:** `can()` on `space.links`.
- **T33** `two desks recording two phones at once: the second is refused VISIT_HAS_CUSTOMER` (`whileHeld`:
  the visit's customer set meanwhile). **B39:** the visit read without its lock (`findIn` before
  `lockAtDesk`).

### API — `apps/api/src/modules/payments/uncollected.api.test.ts` [C2]
- **T34** `a written-off visit is not listed, nor counted; undone, it is again`. **B7** as T1 (the count's
  side).

### Not tested, and said
- The customer debt as a read: not built (step 8). Only its data model line changes.
- The `'' ` name fallback in `customerFor`: unreachable by the `CHECK` (D4).

---

## 10. Review Focus — inputs no planned test exercises
- A visit both written off and with payments, then a void (step 9): the balance stays `due − paid`, and the
  write-off's recorded amount (in the audit) no longer equals it. Accepted: the audit records what was
  written off then.
- A write-off undone after the visit's customer was archived: the visit counts in an archived customer's
  debt (the debt read is step 8's).
- `customerFor` with a phone that finds an **archived** customer of the same number: `findByPhone` skips
  archived ones, so a new customer is created (#95's rule), and for a visit with a customer that becomes
  `VISIT_HAS_CUSTOMER`.
- The retry answered with the current sums (S5): sums that moved because of another desk between the two
  requests.
- `DELETE …/write-off` on an open visit: it is never written off, so the answer is the visit as it is.

---

## 11. The commits

Conventional Commits; subjects counted (≤ 50); a body that says why; no tool attribution; staged by path.

| # | Subject (chars) | Holds |
|---|---|---|
| C0 | *only if* `0_CARRIED_FROM_97.md` exists when the executor starts: its items, as it says, in this PR's first commit; subject by its content | the owner's carried rule (`review-verdict-rule`); the description names "Carried from #97" |
| C1 | `feat(visits): store a visit's write-off` (39) | schema, migration (columns, FK, `CHECK`, the trigger's fourth rule), D1, D2, `DeskVisit.writeOff` and the mapper, the exact-key tests gaining `writeOff: null`, data model *Visit* entity and *Constraints* lines |
| C2 | `feat(desk): write a visit off, and undo it` (42) | `visits.writeOff` in `can()` (U1), `writeOffVisitSchema` (U2), `VISIT_ALREADY_PAID` (+ `VISIT_NOT_PRICED`'s two revised lines), the two routes, D6, T1–T12, T34; finding 110; their documents |
| C3 | `feat(desk): receive a payment for a visit` (41) | `receivePaymentSchema` (U3), `ReceivedPayment`, `VISIT_WRITTEN_OFF` and `VISIT_HAS_CUSTOMER`, `CONSTRAINT_CODES` line, `customerFor` (finding 100), `balancesOf`, T13–T26; their documents; finding 100 resolved |
| C4 | `feat(desk): leave a visit's debt to a customer` (46) | `leaveToCustomerSchema` (U4), the route, T27–T33; their documents |

**PR title:** `feat(desk): collect or write off a visit's debt` (47).

---

## 12. Verification and the procedure

### 12.1 Before the branch
```powershell
Set-Location C:\dev\masaha\app-b
git fetch origin
git status --short --branch            # clean
gh pr view 97 --json state,mergeCommit # MERGED (abc28e73)
git log --oneline -5 origin/main
git diff --name-status e122b95d origin/main
gh pr list --state open --json number,title,headRefName,headRefOid,files
Test-Path C:\dev\masaha\workspace\WORKER_B\DESK\0_CARRIED_FROM_97.md
```
- **The diff:** if a code file this plan names (§7) has changed in a way the plan does not cover: **stop and
  ask**. If only documents changed, re-read the shared ones on the merged tree before editing them.
- **An open PR** that edits a code file of this PR: stop and ask.
- **`0_CARRIED_FROM_97.md`:** if it exists, read it whole. Its items are C0, built as it says, each red first,
  then green, with its break. This plan does not guess its content. If its items contradict this plan: stop
  and ask.

```powershell
git switch --no-track -c feat/visit-debts origin/main
docker start masaha-postgres-1         # never npm run db:up; never npm ci
npm run build -w @masaha/shared
```
- `apps/api/.env` must name `masaha_b_dev` / `masaha_b_test` and `PORT=3321` (`Select-String` by pattern;
  never print the file).
- `npm exec -w @masaha/api -- prisma migrate status` → up to date (both B databases are at `main`'s
  migrations since #95; #97 added none).

**Memory: one full test run at a time on this machine.** Before each full lane, write the free memory into
the report, and check that nothing of worker A's runs:
```powershell
Get-CimInstance Win32_OperatingSystem | Select-Object FreePhysicalMemory
Get-CimInstance Win32_Process -Filter "Name = 'node.exe'" |
  Where-Object { $_.CommandLine -match 'vitest|tsc' } | Select-Object ProcessId, CommandLine
```
- A `vitest` or `tsc` under `C:\dev\masaha\app\` (worker A's): wait for it to end. Never stop it.
- **A lane killed for memory stops the work:** no retry, the report written, `Status: STOPPED`.

### 12.2 First checks (each when its code exists)
1. **The migration, created once** (after the schema edit):
   ```powershell
   npm exec -w @masaha/api -- prisma migrate dev --create-only --name visit_write_off
   Get-ChildItem apps/api/prisma/migrations | Select-Object -Last 2
   ```
   - Run it **once**, then list the folder. Keep Prisma's `ALTER TABLE … ADD COLUMN …` and `AddForeignKey`.
   - Append the raw-SQL header as in `desk_visit_charge`, then D2's `CHECK`, then
     `CREATE OR REPLACE FUNCTION "payments_guard_insert"()`, **copied whole from
     `20261020074552_desk_visit_charge`**, with only these changes:
     - `DECLARE` gains `written_off boolean;`;
     - the visit's `SELECT` becomes `SELECT "charge_agorot", "written_off_at" IS NOT NULL INTO due,
       written_off FROM "visits" WHERE "id" = NEW."visit_id" FOR UPDATE;`;
     - after `IF NOT FOUND THEN RETURN NEW; END IF;`, add:
       ```sql
       IF written_off THEN
         RAISE EXCEPTION 'payments_visit_written_off: a written-off visit takes no payment'
           USING ERRCODE = 'check_violation', TABLE = 'payments', CONSTRAINT = 'payments_visit_written_off';
       END IF;
       ```
     with a comment line "A written-off visit takes no payment until the owner undoes it (K6)".
   - **On a data-loss refusal** (not expected: three nullable columns): `prisma migrate diff
     --from-migrations apps/api/prisma/migrations --to-schema-datamodel apps/api/prisma/schema.prisma
     --script` into the folder, then append, and say so in the report.
   - Then `npm run db:migrate` (this applies to `masaha_b_dev` and regenerates the client; check that
     `apps/api/src/generated/prisma/models/Visit.ts` names `writtenOffAt`). `masaha_b_test` is migrated by
     the API lane's global setup: confirm it with `prisma migrate status` against the test URL, or with the
     first API run's output.
   - Prove the function on both databases: `docker exec masaha-postgres-1 psql -U <the .env user> -d
     <db> -c "SELECT prosrc LIKE '%payments_visit_written_off%' FROM pg_proc WHERE proname =
     'payments_guard_insert'"` → `t` on each.
2. **`checkViolationOf` reads the new name:** its pattern `^([a-z0-9_]+): ` matches
   `payments_visit_written_off:`. T17 proves it end to end. If it answers 500: stop and ask.
3. **Two nested `FOR UPDATE`s on the visit** (the service's `lockIn`, then the trigger's) in one
   transaction, as in #95's check-out: T13 and T22 green prove it. A wait or a deadlock: stop and ask.
4. **The exact-key tests:** after C1's mapper change, run the API lane's files that hold a `DeskVisit`
   (`git grep -n "checkoutMethod: '" -- 'apps/api/src/**/*.test.ts'` lists them). Each `toEqual` of a whole
   visit fails until it gains `writeOff: null`. That is the red of C1's read; record which ones. Add
   `writeOff: null` by hand to each and change nothing else. A `toMatchObject` stays as it is.
5. **The positive id in `receivePaymentSchema`:** use the same helper `checkInVisitSchema`'s `shiftId`, or
   `parseId`'s rule, uses. If the shared package has no such schema: `z.number().int().min(1)`, and say so.
6. **`lockAtDesk` taking an action:** `can()`'s typing must accept `'payments.record'` and
   `'visits.writeOff'` (both `SpaceAction`s). Typecheck proves it.
7. **The level rule:** `npm run lint` passes with `desk` importing `visits`, `customers` and `payments` (as
   it does today). A refusal: stop and ask.
8. **`paidFor` with a `tx`:** the repository function gains `tx: Tx = prisma` and is used inside the
   transaction by `balancesOf`. `uncollectedIn` keeps calling it without `tx`.
9. **`docs/README.md`:** read its map lines for `desk.md` and `payments.md`. If they list what is built,
   add the new routes in the same words. Otherwise leave the file alone.

### 12.3 Implement, commit by commit
- Stage **by path** (never `-A` or `.`), and run `git status --short` before each commit. After each commit,
  `npm run lint` and `npm run typecheck`.
- Inside each commit:
  1. the test first, run red in its lane, with the red output in the report;
  2. the code, then green;
  3. the commit's documents (Appendix A).
- Error codes follow `add-error-code`: the code in `packages/shared`, both catalogues, its line in
  api-contract §6, the test that provokes it.
- Each commit message goes in a UTF-8 file, **no BOM, LF line endings**, with a body; commit with
  `git commit -F <file>`.
- **A fix before the push** folds into its commit:
  ```powershell
  git commit --fixup=<sha> -- <paths>
  $env:GIT_SEQUENCE_EDITOR=':'; git rebase -i --autosquash $(git merge-base HEAD origin/main); Remove-Item Env:GIT_SEQUENCE_EDITOR
  git rebase -x "npm run lint && npm run typecheck" $(git merge-base HEAD origin/main)
  ```

### 12.4 Verification on the head (phase 4)
- One at a time, each **once, on the head** (re-run only if a file the lane covers changed after it
  passed): `npm run lint` · `npm run typecheck` · `npm run test:unit` · `npm run test:api` ·
  `npm run format:check` · `npm run check:links` · `npm run build -w @masaha/shared` (the shared package
  changes).
- Also:
  - `git grep -n "#PRNUM"` lists only documents (before §12.7);
  - `git diff --stat origin/main -- apps/web` shows only the two `errors.ts`;
  - `git diff --stat origin/main -- package.json package-lock.json` is empty.
- **Not run, with why:** `test:component`, the web's `build`, `check:build`, `check:classes`. The web's
  change is two catalogue files of strings, whose parity the typecheck enforces; CI runs them on the
  pushed head.

### 12.5 The breaks — every one run, its red recorded
- For each B in §9: back up the file into `scripts\breaks\` (this folder), make the one edit, run the named
  test file in its lane, copy the red lines into the report, restore **from the backup** (never
  `git checkout`; compare SHA-256 before and after, no CRLF change), run it green, then check that
  `git diff --stat` shows only the item's own work. The scripts (`scripts\brk.py` and its JSON, as PR 3
  did) stay in this folder, uncommitted.
- **Database breaks:**
  - **B5:** `ALTER TABLE visits DROP CONSTRAINT visits_write_off_check` on `masaha_b_test`; D1 red; restore
    by re-running D2's `ADD CONSTRAINT` there; D1 green.
  - **B6:** on `masaha_b_test`, `CREATE OR REPLACE` the function from `desk_visit_charge`'s text; D2 and
    T22 red; restore with the new migration's function; both green; `prosrc LIKE
    '%payments_visit_written_off%'` → `t`.
- Every permission (B1, B10, B11, B28, B29, B38), every money rule (B8, B12, B13, B16, B19, B20, B22, B23,
  B24, B27, B35, B36), every idempotency key (B25, B26, B30) and every race (B11, B16, B26, B27, B6 on T22,
  B39) has its break.
- **A break that stays green: stop**, unless it is plainly your own test's defect, or the plan's break cannot
  change the outcome (a bound already excluded by another rule). In that case, make the break that can, see
  it red, and state it as a departure.

### 12.6 The real run (API on 3321, `masaha_b_dev`)
- Start `npm run dev -w @masaha/api` in the background (log to `scripts\server.log`, deleted afterwards);
  `curl.exe -s http://localhost:3321/health` → `db: up`.
- Sign in as `demo-owner@example.com` and `demo-reception@example.com`. Read `SEED_DEMO_PASSWORD` from
  `apps/api/.env` into a variable and never print it. The script is `scripts\realrun4.mjs`.
- Insert, through `psql`, two visits of space 1 closed `AUTO` yesterday with charges of 2,500 and 1,500
  agorot, and no customer.
- Walk the cases, recording each status:
  1. `GET …/uncollected-visits` lists both.
  2. As reception, `POST …/payments { visitId: A, amountAgorot: 1000, method: CASH }` with no phone → **422**
     `phone`.
  3. The same with `phone: "0599000124"` → **201**, `balanceAgorot 1500`, the customer created.
  4. The same key again → **201**, the same payment.
  5. `amountAgorot: 2000` with a new key → **409 `PAYMENT_EXCEEDS_DUE`**.
  6. As reception, `PUT …/visits/B/customer { phone: "0599000125" }` → **200**; again → 200, writing
     nothing.
  7. As reception, `POST …/visits/A/write-off` → **403**.
  8. As the owner, with `{ reason: "Real run" }` → **200**, `writeOff` set.
  9. `GET …/uncollected-visits` → A is gone.
  10. As reception, `POST …/payments` on A → **409 `VISIT_WRITTEN_OFF`**.
  11. As the owner, `DELETE …/visits/A/write-off` → **200**, cleared; A is listed again.
  12. The payment of the rest → **201**, `balanceAgorot 0`.
- Then `SELECT action FROM audit_logs ORDER BY id DESC LIMIT 10` through `psql`.
- Stop the server by its process ids (the `tsx watch` child, the server, `pino-pretty`); `Get-NetTCPConnection
  -LocalPort 3321 -ErrorAction SilentlyContinue` prints nothing. Leave the demo data as it is, and say what
  it holds.

### 12.7 The PR number, push and PR
Just before the push, in Git Bash:
```bash
n=$(( $(gh api "repos/{owner}/{repo}/issues?state=all&per_page=1&sort=created&direction=desc" --jq '.[0].number') + 1 ))
base=$(git merge-base HEAD origin/main)
git filter-branch -f --tree-filter "grep -rl '#PRNUM' docs | xargs -r sed -i 's/#PRNUM/#$n/g'" $base..HEAD
git for-each-ref --format='%(refname)' refs/original/ | xargs -r -n1 git update-ref -d
git grep -n '#PRNUM' ; echo "expect nothing above; PR will be #$n"
npm run check:links; npm run format:check
git push -u origin feat/visit-debts
```
- `gh label list`: `feat`, `area:api`, `area:docs`, `area:web` must exist.
- Then at once:
  ```powershell
  gh pr create --assignee @me --label feat --label area:api --label area:docs --label area:web `
    --title "feat(desk): collect or write off a visit's debt" --body-file <§12.9's text, saved in scripts\>
  ```
- GitHub's number must equal `n`. If it does not, fix the documents (a fixup into the commits that hold
  it) and `git push --force-with-lease`.

### 12.8 CI, CLEAN, conflicts, report
- `gh pr checks <n> --watch` (bounded), then `gh pr view <n> --json headRefOid,mergeStateStatus`: green **on
  the pushed head** (= `git rev-parse HEAD`) and `CLEAN`. Never merge, and never rebase a `CLEAN` PR.
- **Conflicts:** for every other open PR, `git merge-tree --write-tree HEAD <its headRefOid>`, and record
  clean or the conflicted paths. Documents only (`overview.md`, the findings index, `v1-mvp.md`): the fast
  path when their turn comes. Code: stop and ask.
- **The report**, `4_REPORT_PR4.md`, written **as the work goes**: after the first checks, after each
  commit (sha, subject and its length, red, green), after each break, after the real run, after the push.
  It holds:
  - each command, run or not;
  - §12.2's results;
  - the owner's answers to §13 as built;
  - problems and their solutions, and anything unexpected;
  - the conflict check;
  - every departure from this plan, with why.
- **`C:\dev\masaha\workspace\_SHARED\OPEN_DECISIONS.md`:** if it records K6 or DK-012 as open, mark them built
  (#n). Point 4 (the shared device) stays open; its *Settle in* becomes the desk's screen item.

### 12.9 The PR description
```markdown
## Summary
The desk finishes a closed visit's money: a payment after the check-out (POST …/payments), «تسجيل دينًا» (a debt to the phone's customer), and the owner's write-off («لن يُحصَّل») with its undo; a written-off visit takes no payment and leaves the uncollected visits. Finding 100 resolved: a visit's customer is kept.
<"Carried from #97": each item, if C0 exists>

## Scope / Acceptance criteria / Out of scope
<§2>

## Change type
feat — API code, the shared contract, tests and documents; a migration (three columns, a CHECK, the payments trigger's fourth rule); the new codes' catalogue lines in apps/web (worker B's licence).

## New error codes (the Arabic needs the owner's approval)
<§13 Q2's table, and VISIT_NOT_PRICED's two revised lines>

## Evidence
- `lint`, `typecheck` (each commit), `test:unit`, `test:api`, `format:check`, `check:links`, `build -w @masaha/shared`: <results>.
- Seen failing first: <each test, its red line>.
- Deliberate breaks, each red then restored: <B1–B39>.
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
A test **failing** because its code is not written yet is the plan's red step, and normal. A test, lane or
command you **cannot run** is not. That means it errors before any test runs: the database unreachable,
Docker down, a port taken, a module or `dist` missing, a migration pending, `No test files found`, a Vitest
or TypeScript startup error, the whole run timing out, a crash with no result. It also covers a break you
could not make or run, and a real-run case you could not perform.

**Then stop at once.** Never skip, `.skip` or delete a test. Never change a config, a timeout, `.env`, a
script or a lane. Never mock what the plan does not mock. Never run a narrower command and call it the lane,
and never call a failure "flaky" and move on. Write the command, its exact error and where you were into the
report, and reply with the exec prompt's final shape, `Status: STOPPED`.

**A plan that proves false against the code:** stop too, say exactly what and why, and offer the fix; do
not choose it yourself. **A break that stays green:** stop, unless it is plainly your own test's defect, or
the plan's break cannot change the outcome (a bound already excluded by another rule). In that case, make
the break that can, see it red, and state it as a departure.

**Never claim a result you did not see.** A command passed only if you saw its own output say so; copy that
line, and read it by its exit code, not the tail. A break counts only when you saw it red.

### Stop and ask
- `origin/main` has changed a code file of §7 in a way this plan does not cover; or an open PR edits one of
  them; or `0_CARRIED_FROM_97.md` contradicts this plan.
- A change is needed in `apps/web` beyond the two catalogues, a dependency, an error code not in §13 Q2, or a
  schema change beyond D2.
- More than about 70 files.
- The migration cannot be made as check 1 says, or the function cannot be copied whole.
- `checkViolationOf` does not name `payments_visit_written_off` (check 2); two `FOR UPDATE`s wait or
  deadlock (check 3).
- The level rule refuses an import (check 7).
- A break that stays green (§12.5's exception aside).
- A failure not understood after three root-cause fixes; CI failing for a reason not reproduced locally
  after three.
- A conflict with another open PR in a code file.
- The owner's answer to §13 changes a test or a rule beyond what it says.

---

## 13. Decisions needed from the owner

1. **Q1 — the routes (D1):** `POST /payments` (`visitId` in the body), «تسجيل دينًا» as
   `PUT …/visits/:visitId/customer`, and the write-off as `POST` / `DELETE …/visits/:visitId/write-off`, all
   in `desk`. *Alternatives:* A1 (in `payments`), A2 (the debt on the payment route).
2. **Q2 — the codes and their lines (the Arabic for your approval):**
   | Code | Answer | English | Arabic |
   |---|---|---|---|
   | `VISIT_WRITTEN_OFF` | 409 | This visit was written off; the owner must undo the write-off before it takes a payment. | سُجّلت هذه الزيارة «لن يُحصَّل»؛ يتراجع المالك عن ذلك أولًا قبل استلام أي دفعة لها. |
   | `VISIT_ALREADY_PAID` | 409 | This visit is already paid in full. | دُفع مبلغ هذه الزيارة كاملًا. |
   | `VISIT_HAS_CUSTOMER` | 409 | This visit is already another customer's debt. | هذه الزيارة دينٌ على زبون آخر بالفعل. |
   | `VISIT_NOT_PRICED` (revised, reused for the write-off) | 409 | This visit has no price yet; price it first. | لم تُسعَّر هذه الزيارة بعد؛ سعّرها أولًا. |

   *Alternative A3:* keep `VISIT_NOT_PRICED`'s lines and add `WRITE_OFF_NOT_PRICED`.
3. **Q3 — the schema (D2, S4):** one migration, `visit_write_off`, with three columns, a `CHECK` (together,
   non-blank, only on a closed **and priced** visit) and the trigger's fourth rule (S1). An undo clears the
   columns; the audit keeps the history.
4. **Q4 — ADR 0009's table:** a row for the write-off and its undo (owner only), with a *Revised* line.
5. **Q5 — finding 100 folded (S2):** the check-out keeps a visit's customer; a phone that belongs to someone
   else is refused `VISIT_HAS_CUSTOMER`.
6. **Q6 — S5:** a retried payment answers the first payment with the paid amount and the balance as of now.
7. **Q7 — finding 110:** recorded for the desk's screen item (the prototype's "can't be undone", the
   remainder with no phone, manual check-outs in its uncollected list). The prototype is not edited here.

---

## Appendix A — the documents, line by line (the commit in brackets)

Every new decision and history line ends with `2026-10-20, #PRNUM`. *Last Updated* changes on each
document edited.

1. **`docs/api/api-contract.md`**
   - *Front desk (managed)*'s intro: the payment after the check-out, the debt and the write-off [C2–C4].
   - `DeskVisit` gains `writeOff: { at, byId, reason } | null`, with the comment "set while written off"
     [C1].
   - `POST …/visits/:visitId/write-off` and `DELETE …` (🏢; body; 200; "a second answers it as it is"; errors
     as D3; audit `visit.writtenOff` `{ reason, balanceAgorot }`, `visit.writeOffUndone` `before`) [C2].
   - `POST …/payments` (🧾, key; body; 201 `ReceivedPayment`; retry rule S5; the unpaid rule; errors in D4's
     order; audit) [C3].
   - `PUT …/visits/:visitId/customer` (🧾; body; 200; errors; audit `visit.leftToCustomer`) [C4].
   - `UncollectedVisit`'s paragraph: "… and not written off" [C2].
   - §1's *Idempotency key* "Built for …": + "a visit's payment after its check-out" [C3].
   - §6: the three codes, and `VISIT_NOT_PRICED`'s gloss "(a payment on, or a write-off of, a visit with no
     charge)" [C2, C3].
2. **`docs/architecture/data-model.md`**
   - *Visit* entity: "… It may be written off by the owner, with who, when and why, and the write-off
     undone" [C1].
   - *Constraints worth stating*: the write-off's `CHECK`, and the ledger's bullet "… and a written-off visit
     takes no payment (`payments_visit_written_off`)" [C1].
   - *Front desk and money*:
     - a new bullet **Written-off visit** (K6): "the owner may write off what is still owed on a closed,
       priced visit, with a required reason, recorded with who and when; payments made stay; it is never a
       payment and never a deletion; it can be undone; a written-off visit takes no payment until then" [C2];
     - *Uncollected visits*: "… left unpaid and not written off, the unpriced ones included" [C2];
     - *Customer debt*: "… and unpaid visits not written off" [C2];
     - *Unpaid visit*: "… left unpaid at its check-out or a later payment, … unless the visit already has a
       customer, which it keeps" [C3].
   - *Checked by the service*: "a visit left unpaid at a manual check-out, **or at a later payment**, has a
     customer" [C3].
3. **`docs/backend/conventions.md`**
   - Header *Built*: + "the desk's payment after a check-out" [C3].
   - §9 *The front desk*: + "receiving a visit's payment after its check-out, and leaving its debt to a
     customer by phone; the owner's write-off and its undo" [C2–C4].
   - §13 *The ledger's rules*: "three" → "four … and a written-off visit takes no payment" [C1].
   - §13 *Idempotency*: "Today payments, visits and check-ins have it" stays as it is [—].
4. **`docs/backend/security.md`**
   - Header and *Authorization*: `requireCan` on the desk's payment and debt (`payments.record`) and the
     write-off (`visits.writeOff`, the owner's) [C2–C4].
5. **ADR 0009:** a *Revised* line and the table's row (§13 Q4) [C2].
6. **`docs/features/desk.md`**
   - *What it does*: + the payment, the debt, the write-off [C2–C4].
   - *Behaviour and flows*: D4's four flows, the order and the unpaid helper [C2–C4].
   - *API decisions*: D1, S2, S3, S5; the write-off idempotent by design [C2–C4].
   - *Code map* and *API history* [C2–C4].
   - The line "the shared desk device is not settled …: step 9" → "… the desk's screen item" [C2].
7. **`docs/features/payments.md`**
   - *What it does*: + the balance of a visit for the desk (`balancesOf`); the uncollected visits leave
     written-off ones out [C2, C3].
   - *Responsibility boundary*: the fourth ledger rule [C1].
   - *Behaviour*: the payment after the check-out (the trigger's order) [C3].
   - *API decisions*: S1 [C1]. *API history* [C3].
8. **`docs/features/visits.md`**
   - *What it does* and *Responsibility boundary*: owns the write-off's columns, the customer left to
     (`leaveTo`), audits `visit.writtenOff` / `visit.writeOffUndone` / `visit.leftToCustomer` [C1–C4].
   - *API history* [C1–C4].
9. **`docs/plans/v1-mvp.md`**
   - Step 7: *Goal* + "collecting an uncollected visit, its debt by phone, and its write-off"; *Built* + "a
     visit's payment after its check-out, its debt to a customer by phone, and the owner's write-off with its
     undo (#PRNUM)" [C2–C4].
   - Step 9: *Goal* → "payments are voided, and each staff member's collections and the finance are seen; a
     visit's payment after its check-out is received since step 7 (#PRNUM), a subscription's with step 8"
     [C3].
   - Route table: the `GET / POST …/payments` row → `GET` only (the list), and the built `POST` into the
     *Built* sentence with the write-off and the customer routes [C2–C4].
   - The *Built* sentence's access line: + "reception receives a visit's payment and records its debt; the
     owner writes a visit off" [C3, C4].
10. **`docs/project/overview.md`** — the *Front desk* line: + "collecting a visit's debt, or the owner's
    write-off" [C4].
11. **Finding 100** — *Status:* Resolved; *Resolution (2026-10-20, #PRNUM):* "the desk's one rule for an
    unpaid part keeps a visit's customer at the check-out and at a later payment; a phone that belongs to
    someone else is refused `VISIT_HAS_CUSTOMER`; the empty name cannot happen (a visit with no customer
    has a name, by its `CHECK`)". The index line moves to *Resolved* [C3].
12. **Finding 110** (new) — §6's evidence and *Resolves when*; its index line under *Open* [C2].
13. **`docs/README.md`** — only as check 9 says [C3].

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
