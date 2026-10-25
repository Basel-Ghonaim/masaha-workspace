import io, os
os.chdir('C:/dev/masaha/app-b')
def edit(path, pairs):
    t = io.open(path, encoding='utf-8', newline='').read()
    for old, new in pairs:
        assert t.count(old) == 1, (path, old[:70], t.count(old))
        t = t.replace(old, new)
    io.open(path, 'w', encoding='utf-8', newline='').write(t)

edit('docs/api/api-contract.md', [
("""#### `POST /manage/spaces/:spaceId/visits/:visitId/write-off` · 🏢""",
"""#### `PUT /manage/spaces/:spaceId/visits/:visitId/customer` · 🧾
«تسجيل دينًا» (DK-012): a closed visit's unpaid rest left to a customer by phone, with no payment.
- **Body** (`leaveToCustomerSchema`, `@masaha/shared/desk`): `{ phone, customerName? }`; `phone` required.
- **200:** `DeskVisit`, its `customer` the space's customer with that phone among those not archived, or a new one named `customerName` (else the visit's name); it stays uncollected, now with its customer, and counts in that customer's debt. An unpriced visit may be left too: its debt has a customer before it is priced. The same phone again answers the visit as it is, writing nothing. Built 2026-10-20, #PRNUM.
- **Errors:** `validation` (422) on the body, before anything is read; `forbidden` (403) for a reception or owner whose link ended meanwhile; `conflict` (409) `VISIT_WRITTEN_OFF` for a written-off visit, `VISIT_ALREADY_PAID` for one with nothing owed, `VISIT_HAS_CUSTOMER` for a visit that is already another customer's, and no code for a visit still open; `not_found` (404), also for a visit that is not the space's.
- **Audit:** `customer.created` for a new customer; `visit.leftToCustomer` (`after`: `{ customerId }`), in the change's own transaction.

#### `POST /manage/spaces/:spaceId/visits/:visitId/write-off` · 🏢"""),
("`VISIT_ALREADY_PAID` (writing off a visit with nothing owed, 2026-10-20, #PRNUM)",
 "`VISIT_ALREADY_PAID` (writing off, or leaving to a customer, a visit with nothing owed, 2026-10-20, #PRNUM)"),
("`VISIT_WRITTEN_OFF` (a payment on a written-off visit, from the ledger, 2026-10-20, #PRNUM)",
 "`VISIT_WRITTEN_OFF` (a payment on a written-off visit, from the ledger, or leaving it to a customer, 2026-10-20, #PRNUM)"),
])

edit('docs/architecture/data-model.md', [
("- **Unpaid visit:** a visit may be left unpaid, at its check-out or a later payment, only with a phone number.",
 "- **Unpaid visit:** a visit may be left unpaid, at its check-out or a later payment, only with a phone number; an uncollected visit may also be left to a customer by phone alone («تسجيل دينًا», DK-012, 2026-10-20, #PRNUM)."),
])

edit('docs/backend/conventions.md', [
("- **a visit's payment after its check-out**, its unpaid rest left to a customer by the same rule as the check-out's;\n",
 "- **a visit's payment after its check-out**, its unpaid rest left to a customer by the same rule as the check-out's, and **its debt left to a customer by phone** («تسجيل دينًا»);\n"),
])

edit('docs/backend/security.md', [
("a visit's payment after its check-out, `payments.record`, the staff's;",
 "a visit's payment after its check-out and its debt left to a customer, `payments.record`, the staff's;"),
])

edit('docs/features/desk.md', [
("- Receives a payment for a closed visit after its check-out, once per idempotency key; the rest left unpaid by the check-out's rule.\n",
 "- Receives a payment for a closed visit after its check-out, once per idempotency key; the rest left unpaid by the check-out's rule.\n- Leaves an uncollected visit's debt to a customer by phone, with no payment («تسجيل دينًا»).\n"),
("and `payments.record` (the staff's) for the payment, each then reading its `Idempotency-Key`;",
 "and `payments.record` (the staff's) for the payment, each then reading its `Idempotency-Key`, and for «تسجيل دينًا», which needs none;"),
("\n**The write-off and its undo.**",
 "\n**«تسجيل دينًا».** In one transaction, in this order: the space's lock and `can()` (`payments.record`); the visit's row (`FOR UPDATE`), not the space's → 404, still open → 409; written off → `VISIT_WRITTEN_OFF`; nothing owed → `VISIT_ALREADY_PAID` (an unpriced visit has a debt to leave); then the unpaid-part rule; the visit's own customer again → the visit as it is; else its customer is set, audited `visit.leftToCustomer`.\n\n**The write-off and its undo.**"),
("- **A retried payment answers the first payment, with the visit and the two sums as of now.**",
 "- **«تسجيل دينًا» is its own `PUT …/visits/:visitId/customer`, not the payment route with no amount.** *Why:* a `POST …/payments` that records no payment would answer \"created\" for nothing and spend a key; setting a visit's customer is idempotent by design (the same phone finds the same customer under the space's lock), so it needs no key. 2026-10-20, #PRNUM.\n- **A retried payment answers the first payment, with the visit and the two sums as of now.**"),
("- **Shared:** `packages/shared/src/desk/`: the check-out's and the payment's requests (`checkOutVisitSchema`, `receivePaymentSchema`);",
 "- **Shared:** `packages/shared/src/desk/`: the check-out's, the payment's and «تسجيل دينًا»'s requests (`checkOutVisitSchema`, `receivePaymentSchema`, `leaveToCustomerSchema`);"),
("a visit's payment after its check-out; a visit's customer kept at an unpaid check-out (finding 100).",
 "a visit's payment after its check-out; a visit's customer kept at an unpaid check-out (finding 100); «تسجيل دينًا»."),
])

edit('docs/features/visits.md', [
("- Writes a closed visit off, and undoes it, in the desk's transaction: audited `visit.writtenOff` and `visit.writeOffUndone`.\n",
 "- Writes a closed visit off, and undoes it, in the desk's transaction: audited `visit.writtenOff` and `visit.writeOffUndone`.\n- Leaves a closed visit's unpaid rest to a customer, in the desk's transaction (`leaveTo`), audited `visit.leftToCustomer`.\n"),
("a visit's write-off, its columns and `writeOff` on every visit answered.",
 "a visit's write-off, its columns and `writeOff` on every visit answered; a closed visit left to a customer (`leaveTo`)."),
])

edit('docs/README.md', [
("the check-out with its payment and a visit's payment after it, each idempotent; the owner's write-off of a visit's unpaid rest (API only).",
 "the check-out with its payment and a visit's payment after it, each idempotent; a visit's debt left to a customer by phone; the owner's write-off of a visit's unpaid rest (API only)."),
])

edit('docs/plans/v1-mvp.md', [
("**Goal:** the staff run the day at the desk: check in and out, the visit charge and its payment at check-out, live status with the manual override, auto check-out, uncollected visits.",
 "**Goal:** the staff run the day at the desk: check in and out, the visit charge and its payment at check-out, live status with the manual override, auto check-out, uncollected visits: collecting one, its debt by phone, and its write-off."),
("the unpriced visits and their pricing, and the uncollected visits (#97). The step's API is built; its screen remains planned.",
 "the unpriced visits and their pricing, and the uncollected visits (#97); a visit's payment after its check-out, its debt to a customer by phone, and the owner's write-off with its undo (#PRNUM). The step's API is built; its screen remains planned."),
("**Goal:** payments are received and voided, and balances, credit, debts and each staff member's collections today are seen.",
 "**Goal:** payments are voided, and balances, credit, debts and each staff member's collections today are seen; a visit's payment after its check-out is received since step 7 (#PRNUM), a subscription's with step 8."),
("| GET / POST | `/manage/spaces/:spaceId/payments` | 🧾 | record one payment for one visit or subscription; list: the owner sees all (date, staff and method filters), reception its own today |",
 "| GET | `/manage/spaces/:spaceId/payments` | 🧾 | list: the owner sees all (date, staff and method filters), reception its own today. Recording one is built (`POST`, a visit's since step 7; a subscription's with step 8) |"),
("and a visitor's check-in and check-out (`POST …/visits`, `POST …/visits/:visitId/check-out`)",
 "a visitor's check-in and check-out (`POST …/visits`, `POST …/visits/:visitId/check-out`), and a visit's debt: its payment after the check-out (`POST …/payments`), «تسجيل دينًا» (`PUT …/visits/:visitId/customer`) and the owner's write-off (`POST` / `DELETE …/visits/:visitId/write-off`) (#PRNUM)"),
("reception reads, sets and clears the live status's override, and checks visitors in and out.",
 "reception reads, sets and clears the live status's override, checks visitors in and out, receives a visit's payment and records its debt; the owner writes a visit off."),
])

edit('docs/project/overview.md', [
("the unpriced visits the owner prices, and the uncollected visits ([visits]",
 "the unpriced visits the owner prices, and the uncollected visits, collecting a visit's debt or the owner's write-off ([visits]"),
])
print('ok')
