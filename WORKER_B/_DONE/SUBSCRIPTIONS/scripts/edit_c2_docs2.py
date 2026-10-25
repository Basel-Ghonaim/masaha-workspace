import os
os.chdir(r'C:\dev\masaha\app-b')

def rep(p, old, new, count=1):
    s = open(p, encoding='utf-8', newline='').read()
    assert s.count(old) == count, (p, old, s.count(old))
    s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)

# ADR 0015
p = 'docs/architecture/decisions/0015-idempotency-and-concurrency.md'
rep(p, "> **Status:** Accepted · **Date:** 2026-10-01\n",
    "> **Status:** Accepted · **Date:** 2026-10-01\n> **Revised:** 2026-10-22 — rule 4 is done: customers carry the key since #102 (nullable: a customer the desk makes from a visit's phone is made under that check-out's or payment's key), and subscriptions since #PRNUM. #PRNUM\n")

# conventions §13
p = 'docs/backend/conventions.md'
rep(p, "Today payments, visits, check-ins and customers have it, in the Prisma field `idempotencyKey`,",
    "Today payments, visits, check-ins, customers and subscriptions have it, in the Prisma field `idempotencyKey`,")
rep(p, "  - Customers have it since 2026-10-21, #102, optional: a customer the desk creates from an unpaid visit's phone carries none. Subscriptions have none yet; step 8's next PR adds it ([plan, step 8](../plans/v1-mvp.md#sequence-inside-the-build)).",
    "  - Customers have it since 2026-10-21, #102, optional: a customer the desk creates from an unpaid visit's phone carries none. Subscriptions have it since 2026-10-22, #PRNUM, required: every subscription is a desk create.")

# security.md
p = 'docs/backend/security.md'
rep(p, "and a customer's archive and restore (`customers.archive`, the owner's, 2026-10-21, #102), ask `can()` first,",
    "a customer's archive and restore (`customers.archive`, the owner's, 2026-10-21, #102), and subscribing a customer (`subscriptions.manage`, the staff's, 2026-10-22, #PRNUM), ask `can()` first,")
rep(p, "the desk's writes, and the customers' writes;", "the desk's writes, the customers' writes and the subscriptions';")
rep(p, "**Last Updated:** 2026-10-21", "**Last Updated:** 2026-10-22")

# subscriptions.md
p = 'docs/features/subscriptions.md'
rep(p, "- Answers a space's subscriptions — of one customer, or by id — each with its status, its progress and its amount due, as of a time.",
    "- Answers a space's subscriptions — of one customer, or by id — each with its status, its progress and its amount due, as of a time.\n- Writes a subscription the desk makes, from a package's terms or typed ones, with its idempotency key, audited ([desk](desk.md)).")
rep(p, "- **The front desk** ([desk](desk.md)), which reads who is present before it archives a customer.",
    "- **The front desk** ([desk](desk.md)), which subscribes a customer through it, and reads who is present before it archives one.")
rep(p, "**The states.** `statesOf`", "**The create.** `create` writes the subscription the desk composed, in the desk's transaction: its terms and dates, its key, the package it copies or who typed its price and why; a shift that is not the space's is refused by its foreign key, which it answers as `refused`. Audited `subscription.created` with its terms, `packageId`, `renewalOfId` and the reason. `findByKey` answers a retry's subscription.\n\n**The states.** `statesOf`")
rep(p, "- **A subscription of at most seven days by its dates is ending soon on its last day only.**",
    "- **A subscription carries the client's idempotency key, required, unique within the space.** *Why:* every subscription is a desk create, and a retried one must not make two ([ADR 0015](../architecture/decisions/0015-idempotency-and-concurrency.md), rule 4); the seed's rows were given keys of their own. 2026-10-22, #PRNUM.\n- **A typed price's reason is stored beside who typed it, and the database keeps them together, never blank.** *Why:* every hand-typed price carries a reason (data model › Hand-typed prices); a `CHECK` is the one place both writers meet. 2026-10-22, #PRNUM.\n- **A subscription of at most seven days by its dates is ending soon on its last day only.**")
rep(p, "- **API:** `apps/api/src/modules/subscriptions/`, entry `index.ts`: the service (the auto check-out included), the repository,",
    "- **API:** `apps/api/src/modules/subscriptions/`, entry `index.ts`: the service (the create and the auto check-out included), the repository,")
rep(p, "`SUBSCRIPTION_STATUSES` and the responses (`DeskSubscription`, `SubscriptionProgress`, `SubscriptionState`).",
    "`SUBSCRIPTION_STATUSES` and the responses (`DeskSubscription`, with its renewed one and its typed price, `SubscriptionProgress`, `SubscriptionState`).")
s = open(p, encoding='utf-8', newline='').read().rstrip('\n') + "\n- #PRNUM — a subscription's key, typed price's reason and renewed one; the create, audited.\n"
open(p, 'w', encoding='utf-8', newline='').write(s)
rep(p, "**Last Updated:** 2026-10-21", "**Last Updated:** 2026-10-22")

# desk.md
p = 'docs/features/desk.md'
rep(p, "- Archives a customer, as the owner, unless they are present.",
    "- Archives a customer, as the owner, unless they are present.\n- Subscribes a customer, from a package of the space or terms typed by whoever may type a price, once per idempotency key.")
rep(p, "the customer found or created by phone, and the archive's column, to [`customers`](customers.md);",
    "the customer found or created by phone, and the archive's column, to [`customers`](customers.md); a package's terms to [`packages`](packages.md); the subscription and its audit to [`subscriptions`](subscriptions.md);")
rep(p, "`customers.archive` (the owner's) for a customer's archive.",
    "`customers.archive` (the owner's) for a customer's archive; `subscriptions.manage` (the staff's) for subscribing, then its `Idempotency-Key`.")
rep(p, "**The write-off and its undo.**",
    "**Subscribing.** In one transaction, in this order: the space's lock and `can()` (`subscriptions.manage`); the subscription this key already made, for a retry, answered as of now; the customer, the space's (else 404) and not archived (`CUSTOMER_ARCHIVED`); the terms — a package of the space that is offered (else `invalid_choice` on `packageId`), copied, its end `validityDays` after its start, both days included; or typed, by whoever may type a price (`prices.typeByHand`, else `PRICE_TYPING_NOT_ALLOWED`), with its reason, its end as sent and never before its start; the start date, the one sent, else today; then the subscription, through `subscriptions`. Answered 201 with its state, what was paid and what it owes, and the customer's debt.\n\n**The write-off and its undo.**")
rep(p, "- **The warnings never refuse;", "- **A package's terms are copied into the subscription when it is made; the package is offered (not retired) and the space's.** *Why:* a subscription is a snapshot ([ADR 0010](../architecture/decisions/0010-manual-payment-ledger.md)): a later edit of the package changes no subscription made from it. 2026-10-22, #PRNUM.\n- **The warnings never refuse;")
s = open(p, encoding='utf-8', newline='').read().rstrip('\n') + "\n- #PRNUM — subscribing a customer, from a package or custom terms.\n"
open(p, 'w', encoding='utf-8', newline='').write(s)
rep(p, "**Last Updated:** 2026-10-21", "**Last Updated:** 2026-10-22")

# packages.md
p = 'docs/features/packages.md'
rep(p, "- **The space's reception,** through the API: reads them, for the front desk, which will choose from them when it makes a subscription.",
    "- **The space's reception,** through the API: reads them, for the front desk, which chooses from them when it makes a subscription.\n- **The front desk** ([desk](desk.md)): a subscription copies an offered package's terms when it is made (`termsOf`), and keeps them whatever the package becomes.")
rep(p, "- #PRNUM — the database refuses a free package (finding 80).",
    "- #PRNUM — the database refuses a free package (finding 80); a package's terms read for a subscription to copy.")
print('ok')
