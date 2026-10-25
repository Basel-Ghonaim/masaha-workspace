import io, os
os.chdir('C:/dev/masaha/app-b')


def sub(p, old, new):
    s = io.open(p, encoding='utf-8', newline='').read()
    assert s.count(old) == 1, (p, old[:60], s.count(old))
    io.open(p, 'w', encoding='utf-8', newline='').write(s.replace(old, new))


c = 'docs/api/api-contract.md'
sub(c, """- **Errors:** `not_found` (404).

### Internal
""", """- **Errors:** `not_found` (404).

#### `GET /manage/spaces/:spaceId/unpriced-visits` · 🧾
- **Query:** `page`, `limit` (§4).
- **200:** a page of `DeskVisit`: the space's closed visits with no charge — closed unpriced at the desk, or by the auto check-out with no rate — the latest closed first, then by id; `meta` the pagination. Built 2026-10-20, #PRNUM.
- **Errors:** `validation` (422) on the query; `not_found` (404).

#### `PUT /manage/spaces/:spaceId/visits/:visitId/charge` · 🧾
- **Body** (`priceVisitSchema`, `@masaha/shared/visits`): `amountAgorot`, whole agorot from 1 to 10,000,000; `reason`, 1–200 characters, required. The check-out's typed `charge` takes the same shape.
- **200:** `DeskVisit`, its charge typed: `typedById` the caller, its `reason`, no rounding. Whoever may type a price types it, by the space's settings (the owner always; reception where they allow it). Built 2026-10-20, #PRNUM.
- **Errors:** `validation` (422) on the body, before anything is read; `forbidden` (403) `PRICE_TYPING_NOT_ALLOWED` for reception where the space's settings do not allow it, and no code for an owner or reception whose link ended meanwhile; `conflict` (409) `VISIT_ALREADY_PRICED` for a visit with a charge, and no code for a visit still open (it is priced at its check-out); `not_found` (404), also for a visit that is not the space's.
- **Audit:** `visit.priced` (`after`: `{ chargeAgorot, reason }`), in the change's own transaction.

### Internal
""")
sub(c, "`VISIT_ALREADY_CLOSED` (a payment on a visit another check-out already closed: not recorded).",
    "`VISIT_ALREADY_CLOSED` (a payment on a visit another check-out already closed: not recorded) · `VISIT_ALREADY_PRICED` (pricing a visit that already has a charge).")

d = 'docs/architecture/data-model.md'
sub(d, "never free, left to a customer by phone, for the owner to price (2026-10-20, #95).",
    "never free, left to a customer by phone, for the owner to price (2026-10-20, #95).\n- **Unpriced visit:** a closed visit with no charge — closed unpriced at the desk, or by the auto check-out with no rate. It is priced later, once, by whoever may type a price, with its reason, recorded with who typed it; it takes no payment until then (2026-10-20, #PRNUM).")

s = 'docs/backend/security.md'
sub(s, "else `forbidden` (403) `PRICE_TYPING_NOT_ALLOWED` ([data-model › Front desk and money](../architecture/data-model.md#front-desk-and-money)). 2026-10-20, #95.",
    "else `forbidden` (403) `PRICE_TYPING_NOT_ALLOWED` ([data-model › Front desk and money](../architecture/data-model.md#front-desk-and-money)). 2026-10-20, #95. Pricing an unpriced visit later is decided the same way, after `requireCan('attendance.record')` at its route and the staff's `can()` under the space's lock. 2026-10-20, #PRNUM.")

f = 'docs/features/visits.md'
sub(f, "- Closes every open visit whose auto check-out time has passed, at that time, charged to it: the timed job `visits.autoCheckOut`.",
    "- Closes every open visit whose auto check-out time has passed, at that time, charged to it: the timed job `visits.autoCheckOut`.\n- Lists a space's unpriced visits, and prices one by hand, with its reason, for whoever may type a price.")
sub(f, "- **Asks** `can()`'s `prices.typeByHand` for the terms' `mayTypePrice`, from the boundary's links.",
    "- **Asks** `can()`'s `prices.typeByHand` for the terms' `mayTypePrice`, from the boundary's links; and, under the space's lock (`spaces.lock`), for pricing an unpriced visit.")
sub(f, "- Its manage router holds the two reads, behind the boundary that admits the space's staff, which is their check;",
    "- Its manage router holds the reads, behind the boundary that admits the space's staff, which is their check, and the pricing, behind `requireCan('attendance.record')`;")
sub(f, "\n## Decisions\n", """
**The unpriced visits.** The space's closed visits with no charge, the latest closed first, then by id, paged, read without a lock. **The pricing:** in one transaction, the space's lock; `can()` on the links read under it, the staff's, then `prices.typeByHand` by the space's switch; the visit's row (`FOR UPDATE`), the space's only; refused while open, or once it has a charge; its charge, who typed it and why, no rounding; audited `visit.priced`.

## Decisions
""")
sub(f, "- **At most 500 visits a run;", """- **An unpriced visit is priced once, by whoever may type a price, under the space's lock; a visit with a charge is refused (`VISIT_ALREADY_PRICED`), an open one too.** *Why:* a typed charge is the owner's decision with its reason, not to be overwritten silently; an open visit is priced at its check-out (Q4 of the desk's plan). 2026-10-20, #PRNUM.
- **At most 500 visits a run;""")
sub(f, "- #PRNUM — the auto check-out of visits.\n", "- #PRNUM — the auto check-out of visits; the unpriced visits and their pricing.\n")
sub(f, "- **Shared:** `packages/shared/src/visits/`: the check-in's request (`checkInVisitSchema`);",
    "- **Shared:** `packages/shared/src/visits/`: the check-in's request (`checkInVisitSchema`) and a price typed by hand (`priceVisitSchema`, which the check-out's typed charge reuses);")

k = 'docs/features/desk.md'
sub(k, "or none for whoever may not: an unpriced close.", "or none for whoever may not: an unpriced close, which the owner prices later through [`visits`](visits.md).")
print('ok')
