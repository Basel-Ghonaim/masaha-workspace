import io, os
os.chdir('C:/dev/masaha/app-b')


def sub(p, old, new):
    s = io.open(p, encoding='utf-8', newline='').read()
    assert s.count(old) == 1, (p, old[:60], s.count(old))
    io.open(p, 'w', encoding='utf-8', newline='').write(s.replace(old, new))


c = 'docs/api/api-contract.md'
sub(c, """- **Audit:** `visit.priced` (`after`: `{ chargeAgorot, reason }`), in the change's own transaction.

### Internal
""", """- **Audit:** `visit.priced` (`after`: `{ chargeAgorot, reason }`), in the change's own transaction.

#### `GET /manage/spaces/:spaceId/uncollected-visits` · 🧾
- **Query:** `page`, `limit` (§4).
- **200:** a page of `UncollectedVisit` (`@masaha/shared/payments`): the space's visits closed by the auto check-out and not fully paid, the unpriced ones included, the latest closed first, then by id; a voided payment counts for nothing. A manual check-out's visit is never listed: its unpaid rest is a customer's debt. `meta` the pagination. Built 2026-10-20, #PRNUM.
- **Errors:** `validation` (422) on the query; `not_found` (404).

```ts
UncollectedVisit = {
  visit: DeskVisit,
  paidAgorot: number,             // what was paid on it, voided payments left out
  balanceAgorot: number | null    // what is still owed; null while it has no charge (unpriced)
}
```

### Internal
""")

v = 'docs/backend/conventions.md'
sub(v, "- **Uncollected visits** (closed by the auto check-out and left unpaid) → `payments`, which owns the balance.",
    "- **Uncollected visits** (closed by the auto check-out and left unpaid) → `payments`, which owns the balance: `visits` names the space's visits closed by the auto check-out, with their charges; `payments` sums their payments in one grouped query and computes each balance by its pure rule (`balance.ts`), so the settled ids are known before `visits` pages the rest, newest closed first (§5) (2026-10-20, #PRNUM).")

d = 'docs/architecture/data-model.md'
sub(d, "- **Uncollected visits:** visits closed by the auto check-out and left unpaid.",
    "- **Uncollected visits:** visits closed by the auto check-out and left unpaid, the unpriced ones included (2026-10-20, #PRNUM).")

p = 'docs/features/payments.md'
sub(p, "The API is built for a visit's payment; no web screen yet.", "The API is built for a visit's payment and the uncollected visits; no web screen yet.")
sub(p, "- Finds the payment a check-out's idempotency key already recorded, so a retry never records a second one.\n",
    "- Finds the payment a check-out's idempotency key already recorded, so a retry never records a second one.\n- Answers a space's uncollected visits: closed by the auto check-out and not fully paid, with what was paid and what is still owed.\n")
sub(p, "at a visit's check-out. No route of its own yet; no web screen.",
    "at a visit's check-out; and, through its own route, the uncollected visits, which the owner's «يحتاج انتباهك» will count. No web screen yet.")
sub(p, "- **Owns** the `payments` table and its audit entries.", "- **Owns** the `payments` table and its audit entries; the balance's pure rule (`balance.ts`: the due less what was paid).")
sub(p, "- **Leaves** the visit, its charge and its customer to [`visits`](visits.md) and `customers`;",
    "- **Reads** from [`visits`](visits.md) the visits closed by the auto check-out, with their charges, and a page of them.\n- **Leaves** the visit, its charge and its customer to [`visits`](visits.md) and `customers`;")
sub(p, "\n## Decisions\n", """
**The uncollected visits.** `visits` names the space's visits closed by the auto check-out, with their charges; the ledger sums what was paid on each in one grouped query, voided payments left out, and computes each balance; the settled ones (balance ≤ 0) are left out before `visits` pages the rest, the latest closed first, so every page is full and the total right. An unpriced visit has no due and is never settled. Read without a lock.

## Decisions
""")
sub(p, "- **Audited `payment.recorded`, with the visit, the amount and the method.** 2026-10-20, #95.",
    "- **Audited `payment.recorded`, with the visit, the amount and the method.** 2026-10-20, #95.\n- **The uncollected visits are composed without repeating the balance: `visits` names them, the ledger decides which are settled, before the page is cut.** *Why:* the balance is the ledger's rule, in one place; filtering a page after it is fetched would leave pages short ([conventions §5](../backend/conventions.md#5-pagination)). Three queries over the space's auto-closed visits, fine at v1's scale. 2026-10-20, #PRNUM.")
sub(p, "- **API:** `apps/api/src/modules/payments/`, entry `index.ts`: the service, the repository and the mapper.",
    "- **API:** `apps/api/src/modules/payments/`, entry `index.ts`: the service, the repository, the mapper, the controller and the manage router, and the balance's rule (`balance.ts`).")
sub(p, "the response (`VisitPayment`).", "the responses (`VisitPayment`, `UncollectedVisit`).")
sub(p, "- #95 — a visit's payment at its check-out; the ledger's translation table; finding 15 resolved.\n",
    "- #95 — a visit's payment at its check-out; the ledger's translation table; finding 15 resolved.\n- #PRNUM — the uncollected visits.\n")

o = 'docs/project/overview.md'
sub(o, "and a price typed by hand with its reason; the auto check-out of open stays at their due time (",
    "and a price typed by hand with its reason; the auto check-out of open stays at their due time; the unpriced visits the owner prices, and the uncollected visits (")

m = 'docs/plans/v1-mvp.md'
sub(m, "the auto check-out of open visits and subscription check-ins at their due time, run every 5 minutes (#PRNUM, [api-contract › Internal](../api/api-contract.md#internal)); the rest of the step remains planned.",
    "the auto check-out of open visits and subscription check-ins at their due time, run every 5 minutes (#PRNUM, [api-contract › Internal](../api/api-contract.md#internal)); the unpriced visits and their pricing, and the uncollected visits (#PRNUM). The step's API is built; its screen remains planned.")
sub(m, "| GET | `/manage/spaces/:spaceId/visits` | 🧾 | `?open=true`, `?uncollected=true` or a date range |",
    "| GET | `/manage/spaces/:spaceId/visits` | 🧾 | a date range (the open visits are answered by `…/occupancy`, the uncollected by `…/uncollected-visits`, since step 7) |")
print('ok')
