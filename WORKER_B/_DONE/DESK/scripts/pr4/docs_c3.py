import io, os
os.chdir('C:/dev/masaha/app-b')
def edit(path, pairs):
    t = io.open(path, encoding='utf-8', newline='').read()
    for old, new in pairs:
        assert t.count(old) == 1, (path, old[:70], t.count(old))
        t = t.replace(old, new)
    io.open(path, 'w', encoding='utf-8', newline='').write(t)

# --- api-contract
edit('docs/api/api-contract.md', [
("Built for a visit's check-in and check-out ([Front desk (managed)](#front-desk-managed));",
 "Built for a visit's check-in and check-out, and a visit's payment after its check-out (2026-10-20, #PRNUM) ([Front desk (managed)](#front-desk-managed));"),
("The check-in and the check-out send an `Idempotency-Key` (§1), read before the body;",
 "The check-in, the check-out and the payment send an `Idempotency-Key` (§1), read before the body;"),
("- **A part left unpaid,** the whole of an unpriced close included, needs a `phone`: the visit is then left to the space's customer with that phone among those not archived, or to a new one named `customerName` (else the visit's name), and counts in that customer's debt.",
 "- **A part left unpaid,** the whole of an unpriced close included, needs a `phone` when the visit has no customer: the visit is then left to the space's customer with that phone among those not archived, or to a new one named `customerName` (else the visit's name), and counts in that customer's debt. A visit with a customer keeps it, and needs no phone; a phone that is not its customer's is refused (409 `VISIT_HAS_CUSTOMER`, 2026-10-20, #PRNUM)."),
("`required` on `phone` when any part is left unpaid;",
 "`required` on `phone` when any part is left unpaid on a visit with no customer;"),
("`VISIT_ALREADY_CLOSED` for a payment on a visit another key already closed, and no code for a key that paid another visit;",
 "`VISIT_ALREADY_CLOSED` for a payment on a visit another key already closed, `VISIT_HAS_CUSTOMER` for a phone that is not the visit's customer's, and no code for a key that paid another visit;"),
("""#### `GET /manage/spaces/:spaceId/visits/:visitId` · 🧾""",
"""#### `POST /manage/spaces/:spaceId/payments` · 🧾 · `Idempotency-Key`
- **Body** (`receivePaymentSchema`, `@masaha/shared/desk`): `{ visitId, amountAgorot, method, note?, phone?, customerName? }`: the visit it pays, and a payment as at the check-out. Step 8 adds `subscriptionId`, one of the two.
- **201:** `ReceivedPayment`: the visit, the payment recorded with the caller as who took it, and what the visit was paid and still owes. A **retry** with the same key answers 201 with the first payment and records nothing; the visit and the two sums are as of the retry, as the warnings of a check-in are (ADR 0015's "same body", weakened for them). Built 2026-10-20, #PRNUM.
- **Only a closed visit:** an open one is paid at its check-out. The ledger checks the payment first, so its refusals come before any phone is asked for. **If part stays unpaid,** the check-out's rule applies: a visit with a customer keeps it; one with none needs a `phone`, whose customer is found or created.
- **Errors**, in this order, each writing nothing: `validation` (422) on `idempotencyKey` (§1), then on the body, before anything is read; `forbidden` (403) for a reception or owner whose link ended meanwhile; `not_found` (404) for a visit that is not the space's; `conflict` (409) with no code for a key that paid another item, and for a visit still open; from the ledger, `VISIT_WRITTEN_OFF` for a written-off visit, `VISIT_NOT_PRICED` for one with no charge, `PAYMENT_EXCEEDS_DUE` above what is owed; then `validation` (422) `required` on `phone` when part stays unpaid on a visit with no customer, and `conflict` (409) `VISIT_HAS_CUSTOMER` for a phone that is not the visit's customer's.
- **Audit:** `payment.recorded`; `customer.created` for a new customer; `visit.leftToCustomer` (`after`: `{ customerId }`) when the visit gains its customer, each in the change's own transaction.

```ts
ReceivedPayment = { visit: DeskVisit, payment: VisitPayment, paidAgorot: number, balanceAgorot: number }
```

#### `GET /manage/spaces/:spaceId/visits/:visitId` · 🧾"""),
("`VISIT_ALREADY_PAID` (writing off a visit with nothing owed, 2026-10-20, #PRNUM).",
 "`VISIT_ALREADY_PAID` (writing off a visit with nothing owed, 2026-10-20, #PRNUM) · `VISIT_WRITTEN_OFF` (a payment on a written-off visit, from the ledger, 2026-10-20, #PRNUM) · `VISIT_HAS_CUSTOMER` (a phone that is not the customer's of a visit that has one, 2026-10-20, #PRNUM)."),
])

# --- data model
edit('docs/architecture/data-model.md', [
("- **Unpaid visit:** a visit may be left unpaid only with a phone number. It then belongs to the space's customer with that phone among those not archived (created if new, with the name given or the visit's), and its charge counts in that customer's debt (2026-10-20, #95).",
 "- **Unpaid visit:** a visit may be left unpaid, at its check-out or a later payment, only with a phone number. It then belongs to the space's customer with that phone among those not archived (created if new, with the name given or the visit's), and its charge counts in that customer's debt (2026-10-20, #95); unless the visit already has a customer, which it keeps (2026-10-20, #PRNUM)."),
("- a visit left unpaid at a manual check-out has a customer",
 "- a visit left unpaid at a manual check-out, or at a later payment, has a customer"),
])

# --- conventions
edit('docs/backend/conventions.md', [
("the idempotent creates of the desk (a visit's check-in, and its payment at its check-out, §13)",
 "the idempotent creates of the desk (a visit's check-in, and its payment at its check-out or after it, §13)"),
("- **the write-off of a visit's unpaid rest** by the owner, and its undo;\n",
 "- **a visit's payment after its check-out**, its unpaid rest left to a customer by the same rule as the check-out's;\n- **the write-off of a visit's unpaid rest** by the owner, and its undo;\n"),
])

# --- security
edit('docs/backend/security.md', [
("and the desk's writes (`attendance.record`, the staff's; a visit's write-off",
 "and the desk's writes (`attendance.record`, the staff's; a visit's payment after its check-out, `payments.record`, the staff's; a visit's write-off"),
])

# --- desk.md
edit('docs/features/desk.md', [
("- Writes off, as the owner, what a closed, priced visit still owes, with a reason, and undoes it.\n",
 "- Receives a payment for a closed visit after its check-out, once per idempotency key; the rest left unpaid by the check-out's rule.\n- Writes off, as the owner, what a closed, priced visit still owes, with a reason, and undoes it.\n"),
("`attendance.record` (the staff's) for the check-in and the check-out, which then read their `Idempotency-Key`;",
 "`attendance.record` (the staff's) for the check-in and the check-out, and `payments.record` (the staff's) for the payment, each then reading its `Idempotency-Key`;"),
("Any part left unpaid needs a phone: the customer with it is found or created. Then the visit is closed,",
 "Any part left unpaid follows the one unpaid-part rule (below). Then the visit is closed,"),
("\n**The write-off and its undo.**",
 "\n**The unpaid-part rule** (one helper, for the check-out and the payment). A visit with a customer keeps it and needs no phone; a phone that is not its customer's is refused (`VISIT_HAS_CUSTOMER`). A visit with none needs a phone, whose customer is found among those not archived, or created with the name given, else the visit's.\n\n**The payment after the check-out.** In one transaction, in this order: the space's lock and `can()` (`payments.record`); the visit's row (`FOR UPDATE`), not the space's → 404; the payment this key recorded, for a retry, answered with the visit and the sums as they are now; a key that paid another item → 409; an open visit → 409. Then the payment is inserted, which the ledger checks (written off, unpriced, above the balance); then what the visit was paid and still owes; if anything remains, the unpaid-part rule, and the visit's customer set when it changes. The rows are taken in this order: the space's, the visit's, the payment, the customer.\n\n**The write-off and its undo.**"),
("- **A part left unpaid needs a phone, whose customer is found among those not archived, or created with the name given, else the visit's.** *Why:* a debt always has someone to collect from (data model › Unpaid visit); a found customer keeps the name they have. 2026-10-20, #95.\n",
 "- **A part left unpaid needs a phone, whose customer is found among those not archived, or created with the name given, else the visit's.** *Why:* a debt always has someone to collect from (data model › Unpaid visit); a found customer keeps the name they have. 2026-10-20, #95.\n- **A visit that has a customer keeps it, at the check-out and at a later payment; a phone that is not its customer's is refused (`VISIT_HAS_CUSTOMER`).** *Why:* one rule for an unpaid part, in one helper; another phone would move a customer's debt to someone else ([finding 100](../architecture/findings/100-an-unpaid-check-out-moves-a-visits-customer-to-the-phones.md)). The phone is compared with the visit's customer's own. 2026-10-20, #PRNUM.\n- **The payment after the check-out is its own route in `desk`, `POST …/payments`, its body naming the visit.** *Why:* the unpaid-part rule lives here, beside the check-out; the body mirrors the ledger's one item, so step 8 adds `subscriptionId` without breaking a client. 2026-10-20, #PRNUM.\n- **The payment is inserted before the customer is attached.** *Why:* the ledger's refusals (written off, unpriced, above the balance) answer their code before a phone is asked for, and no service repeats them; a 422 on the phone after the insert rolls it back. 2026-10-20, #PRNUM.\n- **A retried payment answers the first payment, with the visit and the two sums as of now.** *Why:* the desk shows what remains on a weak connection; the sums describe now, as a check-in's warnings do (the owner's answer, Q6 of the plan). 2026-10-20, #PRNUM.\n"),
("- **Shared:** `packages/shared/src/desk/`: the check-out's request (`checkOutVisitSchema`); the warnings (`DESK_WARNINGS`) and the check-out's answer (`VisitCheckOut`).",
 "- **Shared:** `packages/shared/src/desk/`: the check-out's and the payment's requests (`checkOutVisitSchema`, `receivePaymentSchema`); the warnings (`DESK_WARNINGS`), the check-out's answer (`VisitCheckOut`) and the payment's (`ReceivedPayment`). The write-off's request (`writeOffVisitSchema`) is `visits`'."),
("- #PRNUM — the owner's write-off of a visit's unpaid rest, and its undo.",
 "- #PRNUM — the owner's write-off of a visit's unpaid rest, and its undo; a visit's payment after its check-out; a visit's customer kept at an unpaid check-out (finding 100)."),
])

# --- payments.md
edit('docs/features/payments.md', [
("- Records the payment of a visit, taken at its check-out, once per idempotency key.",
 "- Records the payment of a visit, taken at its check-out or after it, once per idempotency key."),
("- Answers what one visit was paid and still owes, in the desk's transaction (`balanceOfVisit`), for the write-off.",
 "- Answers what one visit was paid and still owes, in the desk's transaction (`balanceOfVisit`), for the write-off and the payment after the check-out."),
("the whole check-out then writes nothing.\n",
 "the whole check-out then writes nothing.\n\n**A visit's payment after its check-out.** The same insert, in the desk's transaction, before any customer is attached; the trigger refuses, in its order, a written-off visit (`payments_visit_written_off` → `VISIT_WRITTEN_OFF`), one with no charge, and an amount above the balance.\n"),
])

# --- finding 100
p = 'docs/architecture/findings/100-an-unpaid-check-out-moves-a-visits-customer-to-the-phones.md'
edit(p, [
("**Status:** Open · **Date:** 2026-10-20", "**Status:** Resolved · **Date:** 2026-10-20"),
])
t = io.open(p, encoding='utf-8', newline='').read().rstrip('\n') + "\n\n**Resolution (2026-10-20, #PRNUM):** the desk's one rule for an unpaid part keeps a visit's customer at the check-out and at a later payment; a phone that belongs to someone else is refused `VISIT_HAS_CUSTOMER`. The empty name cannot happen: a visit with no customer has a name, by its `CHECK`.\n"
io.open(p, 'w', encoding='utf-8', newline='').write(t)
idx = 'docs/architecture/findings/README.md'
line = "- [100. An unpaid check-out moves a visit's customer to the phone's](100-an-unpaid-check-out-moves-a-visits-customer-to-the-phones.md)\n"
t = io.open(idx, encoding='utf-8', newline='').read()
assert t.count(line) == 1
t = t.replace(line, '')
last = "- [88. The upgrade confirm shows no front desks](88-the-upgrade-confirm-shows-no-front-desks.md)\n"
assert t.count(last) == 1
t = t.replace(last, last + line)
io.open(idx, 'w', encoding='utf-8', newline='').write(t)
print('ok')
