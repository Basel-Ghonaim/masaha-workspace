import os
os.chdir(r'C:\dev\masaha\app-b')

def rep(p, old, new, count=1):
    s = open(p, encoding='utf-8', newline='').read()
    assert s.count(old) == count, (p, old, s.count(old))
    s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)

p = 'docs/api/api-contract.md'
rep(p, "The statement is the staff's read; subscribing is the staff's (🧾), refused with `forbidden` (403) before its body is read for whoever may not, and again for an owner or reception whose link ended meanwhile.",
    "The statement is the staff's read; subscribing and correcting a subscription's limits, dates and name are the staff's (🧾); correcting its price and billing is the owner's (🏢). Each write is refused with `forbidden` (403) before its body is read for whoever may not, and again for an owner or reception whose link ended meanwhile.")
rep(p, "and a typed price's `reason`, else `null`).",
    "and a typed price's `reason`, else `null`); `subscription.corrected` (`before` and `after`: only the fields that changed); `subscription.priceCorrected` (`before`: `{ billing, priceAgorot }`; `after`: the same with `reason`). A correction that changes nothing writes nothing.")
s = open(p, encoding='utf-8', newline='').read()
marker = "### Front desk (managed)"
i = s.index(marker)
s = s[:i] + """#### `PATCH /manage/spaces/:spaceId/subscriptions/:subscriptionId` · 🧾
- **Body** (`correctSubscriptionSchema`, `@masaha/shared/subscriptions`): `{ name?, startsOn?, endsOn?, totalDays?, daysPerWeek?, hoursPerDay?, totalHours? }`, a package's bounds; `null` clears the end or a limit. Only the fields set to a new value change; the price, the billing, the audience, the shift and the package are not corrected here (the name is, the owner's decision on Q8, 2026-10-22, #PRNUM).
- **200:** `SubscriptionState`, as of the answer.
- **Errors**, each writing nothing: `validation` (422) on the body, before anything is read; `forbidden` (403) for an owner or reception whose link ended meanwhile; `not_found` (404) for a subscription that is not the space's; `conflict` (409) `SUBSCRIPTION_ENDED` for one ended early; `validation` (422) `out_of_range` on `endsOn` for an end before the start.

#### `PUT /manage/spaces/:spaceId/subscriptions/:subscriptionId/price` · 🏢
- **Body** (`correctPriceSchema`): `{ billing, priceAgorot, reason }`, both terms together, with why (1–200 characters). Reception is refused `forbidden` (403) before the body is read.
- **200:** `SubscriptionState`: the price recorded as typed by the owner, with the reason (`priceTyped`); the same billing and price answer it as it is and write nothing.
- **Errors**, each writing nothing: `validation` (422) on the body; `forbidden` (403); `not_found` (404) for a subscription that is not the space's; `conflict` (409) `SUBSCRIPTION_ENDED` for one ended early, and `PRICE_BELOW_PAID`, from the database, for a fixed price below what was paid on it (voided payments left out).

""" + s[i:]
open(p, 'w', encoding='utf-8', newline='').write(s)
rep(p, "`CUSTOMER_HAS_DEBT` (warning only: a subscribe whose customer still owes on an earlier item; the subscription is made with `meta.warnings`, 2026-10-22, #PRNUM).",
    "`CUSTOMER_HAS_DEBT` (warning only: a subscribe whose customer still owes on an earlier item; the subscription is made with `meta.warnings`, 2026-10-22, #PRNUM) · `SUBSCRIPTION_ENDED` (correcting a subscription ended early, 2026-10-22, #PRNUM) · `PRICE_BELOW_PAID` (a fixed price corrected below what was paid on it, from the database, 2026-10-22, #PRNUM).")

p = 'docs/architecture/decisions/0009-space-scoped-reception-role.md'
rep(p, "the owner alone archives a customer and restores them. #102\n",
    "the owner alone archives a customer and restores them. #102\n> **Revised:** 2026-10-22 — rule 5: owner and reception correct a subscription's limits, dates and name; the owner alone corrects its price or billing, with a reason. #PRNUM\n")
rep(p, "   | Archive or restore a customer | – | ✓ |\n",
    "   | Archive or restore a customer | – | ✓ |\n   | Correct a subscription's limits, dates and name | ✓ | ✓ |\n   | Correct a subscription's price or billing, with a reason | – | ✓ |\n")

p = 'docs/backend/security.md'
rep(p, "and subscribing a customer (`subscriptions.manage`, the staff's, 2026-10-22, #PRNUM), ask `can()` first,",
    "subscribing a customer and correcting a subscription's limits, dates and name (`subscriptions.manage`, the staff's), and correcting its price or billing (`subscriptions.correctPrice`, the owner's, 2026-10-22, #PRNUM), ask `can()` first,")

p = 'docs/architecture/data-model.md'
s = open(p, encoding='utf-8', newline='').read()
i = s.index("- **Hand-typed prices.**")
j = s.index("\n", i)
s = s[:j] + " A subscription's price and billing are corrected later by the owner only, with a reason, recorded as a price the owner typed; never below what was paid on a fixed price (2026-10-22, #PRNUM)." + s[j:]
open(p, 'w', encoding='utf-8', newline='').write(s)

p = 'docs/backend/conventions.md'
rep(p, "a written-off visit takes none ([data-model.md](../architecture/data-model.md#constraints-worth-stating)).",
    "a written-off visit takes none, and a fixed price never falls below what was paid on it (`subscriptions_price_below_paid`, the subscriptions' trigger, 2026-10-22, #PRNUM) ([data-model.md](../architecture/data-model.md#constraints-worth-stating)).")

p = 'docs/features/subscriptions.md'
rep(p, "- Writes a subscription the desk makes, from a package's terms or typed ones, with its idempotency key, audited ([desk](desk.md)).",
    "- Writes a subscription the desk makes, from a package's terms or typed ones, with its idempotency key, audited ([desk](desk.md)).\n- Corrects a subscription: its limits, dates and name, by the staff; its price and billing, by the owner, with a reason; each audited.")
rep(p, "- It has no route of its own yet: its reads are composed by the desk ([conventions §9](../backend/conventions.md#9-placements)).",
    "- Its manage router sits below `/manage/spaces/:spaceId`, behind the one boundary that admits the space's staff: the corrections (`requireCan('subscriptions.manage')`; the price `requireCan('subscriptions.correctPrice')`, the owner's). Its reads and the subscribe are composed by the desk ([conventions §9](../backend/conventions.md#9-placements)).")
rep(p, "**The renewal's start**", "**The corrections.** Each in its transaction: the space's lock, `can()` on the links read under it, the subscription's row (`FOR UPDATE`, 404 when not the space's), ended → `SUBSCRIPTION_ENDED`. The staff's: only the fields set to a new value (`subscriptionChange.ts`, pure), `null` clearing a limit or the end, an end before the start → `out_of_range`, audited `subscription.corrected`. The owner's: billing and price together, recorded as the owner's typed price with the reason, audited `subscription.priceCorrected`; a fixed price below what was paid is refused by the trigger `subscriptions_guard_price` (`PRICE_BELOW_PAID`). A correction that changes nothing writes nothing.\n\n**The renewal's start**")
rep(p, "- **A subscription of at most seven days by its dates is ending soon on its last day only.**",
    "- **The price and billing are corrected on a route of their own, the owner's; the limits, dates and name on another, the staff's.** *Why:* a route the owner alone may call is refused before its body is read (security › Authorization), as the visit's charge; the owner chose the name correctable by the staff (Q8, A3). 2026-10-22, #PRNUM.\n- **A fixed price never falls below what was paid on it: a database trigger.** *Why:* changing the price is the other way round the payments' ceiling; the ledger's rules are the database's (S2). 2026-10-22, #PRNUM.\n- **A subscription of at most seven days by its dates is ending soon on its last day only.**")
rep(p, "`renewal.ts`).", "`renewal.ts`, `subscriptionChange.ts`), the controller and the manage router (the corrections).")
rep(p, "`SUBSCRIPTION_STATUSES` and the responses", "`SUBSCRIPTION_STATUSES`, the corrections' requests (`correctSubscriptionSchema`, `correctPriceSchema`) and the responses")
rep(p, "the row's lock; the renewal's proposed start.", "the row's lock; the renewal's proposed start; the corrections, the price the owner's.")
print('ok')
