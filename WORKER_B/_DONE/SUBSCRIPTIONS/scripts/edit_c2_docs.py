import os
os.chdir(r'C:\dev\masaha\app-b')

def rep(p, old, new, count=1):
    s = open(p, encoding='utf-8', newline='').read()
    assert s.count(old) == count, (p, old, s.count(old))
    s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)

p = 'docs/api/api-contract.md'
rep(p, "and a customer's creation (2026-10-21, #102, [Customers (managed)](#customers-managed));",
    "a customer's creation (2026-10-21, #102, [Customers (managed)](#customers-managed)), and a subscription's (2026-10-22, #PRNUM, [Subscriptions (managed)](#subscriptions-managed));")
rep(p, """SubscriptionState = {
  id, customerId, packageId: number | null, name,
  startsOn: string | null, endsOn: string | null,                 // Gaza dates, YYYY-MM-DD
  totalDays, daysPerWeek, hoursPerDay, totalHours: number | null,
  billing: "FIXED" | "PER_HOUR" | "PER_DAY", priceAgorot, audience, shiftId: number | null,
  ended: { at, byId } | null,""", """SubscriptionState = {
  id, customerId, packageId: number | null, renewalOfId: number | null, name,
  startsOn: string | null, endsOn: string | null,                 // Gaza dates, YYYY-MM-DD
  totalDays, daysPerWeek, hoursPerDay, totalHours: number | null,
  billing: "FIXED" | "PER_HOUR" | "PER_DAY", priceAgorot, audience, shiftId: number | null,
  priceTyped: { byId, reason } | null,                            // a price typed at the desk
  ended: { at, byId } | null,""")
rep(p, """  unpaidVisits: { visit: DeskVisit, payments: ItemPayment[], paidAgorot, balanceAgorot: number | null }[]
}
```

### Front desk (managed)""", """  unpaidVisits: { visit: DeskVisit, payments: ItemPayment[], paidAgorot, balanceAgorot: number | null }[]
}
```

### Subscriptions (managed)

A customer's subscriptions, at the desk: made from a package of the space or typed there ([data-model › Front desk and money](../architecture/data-model.md#front-desk-and-money)). The endpoints sit under `/manage/spaces/:spaceId` and answer as *Managed spaces* says: without an active `OWNER` or `RECEPTION` link at the live space, `not_found` (404). Subscribing is the staff's (🧾), refused with `forbidden` (403) before its body is read for whoever may not, and again for an owner or reception whose link ended meanwhile. Built 2026-10-22, #PRNUM.

- **Audit**, in the change's own transaction ([conventions §6](../backend/conventions.md#6-audit)), with the subscription as the entity and its space as the entry's: `subscription.created` (`after`: its customer, its terms and dates, `packageId`, `renewalOfId`, and a typed price's `reason`, else `null`).

```ts
NewSubscription = {
  subscription: SubscriptionState & { paidAgorot, balanceAgorot },   // as of the answer
  payments: { item: { visitId } | { subscriptionId }, payment: VisitPayment }[],
  debtAgorot: number                                                 // the customer's, as of the answer
}
```

#### `POST /manage/spaces/:spaceId/customers/:customerId/subscriptions` · 🧾 · `Idempotency-Key`
- **Body:** exactly one of `packageId` and `custom` (both or neither: `invalid_choice` on `packageId`), and `startsOn?`, a Gaza date.
  - `packageId`: a package of the space that is offered; the subscription copies its name, limits, billing, price, audience and shift, and ends `validityDays` after its start, both days included.
  - `custom`: typed at the desk, by the owner always and by reception only where the space's settings allow it — `{ name, endsOn?, totalDays?, daysPerWeek?, hoursPerDay?, totalHours?, billing, priceAgorot, audience, shiftId?, reason }`, a package's fields and bounds with an optional end instead of a validity, and the price's reason, 1–200 characters, recorded with who typed it ([data-model › Hand-typed prices](../architecture/data-model.md#front-desk-and-money)).
  - **The start date:** the one sent, else today (Gaza).
- **201:** `NewSubscription`; a retry with the same key answers the first subscription as it is now, 201, and writes nothing.
- **Errors**, in this order, each writing nothing: `validation` (422) on `idempotencyKey` (§1), then on the body, before anything is read; `forbidden` (403) for an owner or reception whose link ended meanwhile; `not_found` (404) for a customer that is not the space's, also for a space deleted meanwhile; `conflict` (409) `CUSTOMER_ARCHIVED` for an archived customer; `validation` (422) `invalid_choice` on `packageId` for a package that is not the space's or is retired; `forbidden` (403) `PRICE_TYPING_NOT_ALLOWED` for custom terms reception may not type; `validation` (422) `out_of_range` on `custom.endsOn` for an end before the start, `invalid_choice` on `custom.shiftId` for a shift that is not the space's.

### Front desk (managed)""")
rep(p, "**Last Updated:** 2026-10-22", "**Last Updated:** 2026-10-22")
print('ok')
