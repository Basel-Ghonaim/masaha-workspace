import os
os.chdir(r'C:\dev\masaha\app-b')

def rep(p, old, new, count=1):
    s = open(p, encoding='utf-8', newline='').read()
    assert s.count(old) == count, (p, old, s.count(old))
    s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)

p = 'docs/api/api-contract.md'
rep(p, "- **Body** (`receivePaymentSchema`, `@masaha/shared/desk`): `{ visitId, amountAgorot, method, note?, phone?, customerName? }`: the visit it pays, and a payment as at the check-out. Step 8 adds `subscriptionId`, one of the two.",
    "- **Body** (`receivePaymentSchema`, `@masaha/shared/desk`): `{ visitId?, subscriptionId?, amountAgorot, method, note?, phone?, customerName? }`: exactly one item it pays, a visit or a subscription (neither: `required` on `visitId`; both: `invalid_choice` on `subscriptionId`, 2026-10-22, #PRNUM), and a payment as at the check-out.")
rep(p, "- **201:** `ReceivedPayment`: the visit, the payment recorded with the caller as who took it, and what the visit was paid and still owes.",
    "- **201:** `ReceivedPayment`: the visit or the subscription it paid (the other `null`), the payment recorded with the caller as who took it, and what the item was paid and still owes.")
rep(p, "- **Only a closed visit:** an open one is paid at its check-out.",
    "- **A subscription's payment** (2026-10-22, #PRNUM): a subscription of the space (another space's, or none: `invalid_choice` on `subscriptionId`), its row locked; ended, expired or an archived customer's, it still takes one, its debt being owed. The ledger refuses an amount above a fixed price (`PAYMENT_EXCEEDS_DUE`); a usage-based subscription takes any amount, and its `balanceAgorot` is below zero while it holds credit. No phone is asked: a subscription has its customer.\n- **Only a closed visit:** an open one is paid at its check-out.")
rep(p, "`not_found` (404) for a visit that is not the space's; `conflict` (409) with no code for a key that paid another item, and for a visit still open;",
    "`not_found` (404) for a visit that is not the space's, `validation` (422) `invalid_choice` on `subscriptionId` for a subscription that is not; `conflict` (409) with no code for a key that paid another item, and for a visit still open;")
rep(p, "- **Audit:** `payment.recorded`; `customer.created` for a new customer;",
    "- **Audit:** `payment.recorded` (`after`: `{ visitId | subscriptionId, amountAgorot, method }`); `customer.created` for a new customer;")
rep(p, "ReceivedPayment = { visit: DeskVisit, payment: VisitPayment, paidAgorot: number, balanceAgorot: number }",
    "ReceivedPayment = {\n  visit: DeskVisit | null, subscription: SubscriptionState | null,   // the item paid; the other null\n  payment: VisitPayment, paidAgorot: number, balanceAgorot: number   // below zero: a usage-based subscription's credit\n}")

p = 'docs/features/payments.md'
rep(p, "- **Audited `payment.recorded`, with the visit, the amount and the method.** 2026-10-20, #95.",
    "- **Audited `payment.recorded`, with the visit, the amount and the method.** 2026-10-20, #95. Revised: with its item, the visit or the subscription. 2026-10-22, #PRNUM.\n- **One `record` for both items, the item named as `{ visitId }` or `{ subscriptionId }`.** *Why:* the ledger is one table and one trigger; the desk decides which item a request pays, the ledger only records and checks it. 2026-10-22, #PRNUM.")
s = open(p, encoding='utf-8', newline='').read()
i = s.index("### API history")
j = s.index("\n### ", i + 5) if "\n### " in s[i + 5:] else len(s)
block = s[i:j].rstrip('\n') + "\n- #PRNUM — a payment on a subscription, through the desk's payment route; `record` for both items.\n"
s = s[:i] + block + s[j:]
open(p, 'w', encoding='utf-8', newline='').write(s)

p = 'docs/features/desk.md'
rep(p, "- Receives a payment for a closed visit after its check-out, once per idempotency key; the rest left unpaid by the check-out's rule.",
    "- Receives a payment for a closed visit after its check-out, once per idempotency key; the rest left unpaid by the check-out's rule. Or a payment on a subscription of the space.")
rep(p, "**«تسجيل دينًا».**", "**A subscription's payment** (the same route, `subscriptionId` instead of `visitId`). In the same transaction, after the space's lock and `can()` (`payments.record`): the subscription's row (`FOR UPDATE`), not the space's → `invalid_choice` on `subscriptionId`; the payment this key recorded, for another item → 409, for this one a retry, answered with the sums as of now; then the payment, which the ledger checks against a fixed price. Answered with the subscription's state, what was paid and what it owes (below zero while a usage-based one holds credit). An ended subscription, or an archived customer's, still takes one.\n\n**«تسجيل دينًا».**")
s = open(p, encoding='utf-8', newline='').read().rstrip('\n')
s = s.replace("\n- #PRNUM — subscribing a customer, from a package or custom terms.", "\n- #PRNUM — subscribing a customer, from a package or custom terms; a payment on a subscription.")
open(p, 'w', encoding='utf-8', newline='').write(s + "\n")
print('ok')
