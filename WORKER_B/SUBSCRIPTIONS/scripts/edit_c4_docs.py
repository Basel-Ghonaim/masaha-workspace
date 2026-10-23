import os
os.chdir(r'C:\dev\masaha\app-b')

def rep(p, old, new, count=1):
    s = open(p, encoding='utf-8', newline='').read()
    assert s.count(old) == count, (p, old, s.count(old))
    s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)

p = 'docs/api/api-contract.md'
rep(p, "and a subscription's (2026-10-22, #PRNUM, [Subscriptions (managed)](#subscriptions-managed));",
    "and a subscription's (2026-10-22, #PRNUM, [Subscriptions (managed)](#subscriptions-managed)), whose payments take keys derived from its own (SHA-256 of the key and the payment's place, as a UUID), so its retry finds them;")
rep(p, "- **Body:** exactly one of `packageId` and `custom` (both or neither: `invalid_choice` on `packageId`), and `startsOn?`, a Gaza date.",
    "- **Body:** exactly one of `packageId` and `custom` (both or neither: `invalid_choice` on `packageId`), and `startsOn?`, a Gaza date, `renewalOfId?`, the subscription it renews, and `payment?` (`{ amountAgorot, method, note? }`, a payment's bounds).")
rep(p, "  - **The start date:** the one sent, else today (Gaza).",
    "  - **The start date:** the one sent; else, for a renewal, the day after the renewed one's end while it is not expired and its end is not before today; else today (Gaza).\n  - **A renewal** renews one of the customer's own subscriptions, at most once (the database's unique key behind the check).\n  - **The payment** (K3, decision 8): the server allocates the amount over the customer's items that still owe, the oldest first (a visit before a subscription made at the same instant, then by id), each at most its balance, and gives the rest to the new subscription; at most 50 items, the 49 oldest debts and the new one. One payment per item, in that order, audited `payment.recorded` each, all in the request's transaction: the ledger refuses a rest above a fixed new price (`PAYMENT_EXCEEDS_DUE`), and then nothing is written, the subscription included.\n  - **Warning:** `meta.warnings` holds `CUSTOMER_HAS_DEBT` while an item older than the new subscription still owes after the payments (ADR 0010 rule 7); it never refuses.")
rep(p, "- **201:** `NewSubscription`; a retry with the same key answers the first subscription as it is now, 201, and writes nothing.",
    "- **201:** `NewSubscription`; a retry with the same key answers the first subscription and the payments of its derived keys, the money and the warning as of now, 201, and writes nothing.")
rep(p, "`conflict` (409) `CUSTOMER_ARCHIVED` for an archived customer; `validation` (422) `invalid_choice` on `packageId`",
    "`conflict` (409) `CUSTOMER_ARCHIVED` for an archived customer; `validation` (422) `invalid_choice` on `renewalOfId` for a subscription that is not the customer's, `conflict` (409) `SUBSCRIPTION_ALREADY_RENEWED` for one renewed already; `validation` (422) `invalid_choice` on `packageId`")
rep(p, "`invalid_choice` on `custom.shiftId` for a shift that is not the space's.\n",
    "`invalid_choice` on `custom.shiftId` for a shift that is not the space's; `conflict` (409) `PAYMENT_EXCEEDS_DUE` from the ledger.\n")
rep(p, "· `CUSTOMER_ARCHIVED` (editing an archived customer, 2026-10-21, #102).",
    "· `CUSTOMER_ARCHIVED` (editing an archived customer, 2026-10-21, #102) · `SUBSCRIPTION_ALREADY_RENEWED` (renewing a subscription renewed already, 2026-10-22, #PRNUM) · `CUSTOMER_HAS_DEBT` (warning only: a subscribe whose customer still owes on an earlier item; the subscription is made with `meta.warnings`, 2026-10-22, #PRNUM).")

p = 'docs/architecture/data-model.md'
rep(p, "- **A change to the space's settings or capacity applies from then on:**",
    "- **A renewal with a debt** (K3, the owner's decision 8, 2026-10-22, #PRNUM): a new subscription, or a renewal, may come with an amount; the server allocates it over the customer's items that still owe, the oldest first, each at most its balance, the rest to the new subscription — one payment per item, all or nothing. A renewal starts, unless the desk says otherwise, the day after the renewed one's end while it runs, else today; a subscription is renewed at most once. The desk is warned while an older debt remains.\n- **A change to the space's settings or capacity applies from then on:**")

p = 'docs/backend/conventions.md'
rep(p, "- **subscribing or renewing** with its payment, and the warning when the customer has a balance.",
    "- **subscribing or renewing**: the terms from a package or typed, the renewal's start proposed by `subscriptions` (`proposedStart`), and an optional amount `payments` allocates (`allocate`, pure) over the customer's debts, oldest first, one payment each under a key derived from the request's; the warning when an older debt remains (2026-10-22, #PRNUM).")
rep(p, "- **A retry returns the first result**, with the same status and body, never a conflict.",
    "- **One request, several records:** a subscribe's payments each take a key derived from the request's (`derivedKey(key, index)`, `shared/http`: the SHA-256 of `key/index` as a UUID), in the allocation's order, so the ledger's key stays one per payment and a retry finds them all in one query. 2026-10-22, #PRNUM.\n- **A retry returns the first result**, with the same status and body, never a conflict.")

p = 'docs/architecture/decisions/0015-idempotency-and-concurrency.md'
rep(p, "and subscriptions since #PRNUM. #PRNUM\n", "and subscriptions since #PRNUM. A renewal's payments derive their keys from the request's, one per item it pays. #PRNUM\n")

p = 'docs/plans/v1-mvp.md'
rep(p, "| new or renewal, from a package or custom; warns when the customer has a balance |",
    "| new or renewal, from a package or custom; an optional amount the server allocates oldest debt first, one payment per item, under one key; warns while an older debt remains |")
rep(p, "Recording one is built (`POST`, a visit's since step 7; a subscription's with step 8) |",
    "Recording one is built (`POST`, a visit's since step 7; a subscription's since #PRNUM) |")

p = 'docs/features/subscriptions.md'
rep(p, "**The states.** `statesOf`", "**The renewal's start** (`renewal.ts`, pure): `proposedStart(renewed, today)` — the day after the renewed one's end while it is not expired and its end is not before today, else today. `lockIn` locks a subscription's row and answers the one that renewed it, if any.\n\n**The states.** `statesOf`")
rep(p, "and the pure rules (`subscriptionStatus.ts`, `currentSubscription.ts`).", "and the pure rules (`subscriptionStatus.ts`, `currentSubscription.ts`, `renewal.ts`).")
rep(p, "- #PRNUM — a subscription's key, typed price's reason and renewed one; the create, audited.",
    "- #PRNUM — a subscription's key, typed price's reason and renewed one; the create, audited; the row's lock; the renewal's proposed start.")

p = 'docs/features/payments.md'
rep(p, "- #PRNUM — a payment on a subscription, through the desk's payment route; `record` for both items.",
    "- #PRNUM — a payment on a subscription, through the desk's payment route; `record` for both items; the allocation of a subscribe's amount, oldest debt first, and the payments of derived keys found in one query.")
rep(p, "- **One `record` for both items,", "- **A subscribe's amount is allocated by a pure rule here (`allocation.ts`): the debts oldest first, each at most its balance, the rest to the new subscription, at most 50 items.** *Why:* the balance is this module's rule; the desk reads the items and records the parts, the ledger checks each (K3; ADR 0010). 2026-10-22, #PRNUM.\n- **One `record` for both items,")

p = 'docs/features/desk.md'
rep(p, "- Subscribes a customer, from a package of the space or terms typed by whoever may type a price, once per idempotency key.",
    "- Subscribes a customer, from a package of the space or terms typed by whoever may type a price, once per idempotency key; renews one of their subscriptions, at most once; allocates an amount given over their debts, oldest first, the rest to the new subscription; warns while an older debt remains.")
rep(p, "the start date, the one sent, else today; then the subscription, through `subscriptions`. Answered 201 with its state, what was paid and what it owes, and the customer's debt.",
    "the subscription it renews, locked, the customer's own (else `invalid_choice` on `renewalOfId`) and not renewed yet (`SUBSCRIPTION_ALREADY_RENEWED`), read before the terms; the start date, the one sent, else the renewal's proposal (`proposedStart`), else today; then the subscription, through `subscriptions`; then the payment, if any: the customer's items that still owe, read under the lock, allocated oldest first by `payments`' `allocate`, one payment per part under the key `derivedKey(key, index)`, each checked by the ledger (above a fixed new price: `PAYMENT_EXCEEDS_DUE`, the whole request undone). A retry finds the subscription by its key, then its payments by the 50 keys it may have derived, in one query. Answered 201 with its state, what was paid and what it owes, the payments, the customer's debt, and `CUSTOMER_HAS_DEBT` in `meta.warnings` while an older item owes. The rows are taken in this order: the space's, the renewed subscription's, then each paid item's, oldest first (the ledger's trigger).")
s = open(p, encoding='utf-8', newline='').read()
s = s.replace("\n- #PRNUM — subscribing a customer, from a package or custom terms; a payment on a subscription.",
              "\n- #PRNUM — subscribing a customer, from a package or custom terms; a payment on a subscription; a renewal with its payment allocated oldest debt first.")
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
