import sys

ROOT = 'C:/dev/masaha/app-b-lane-f/'


def edit(path, pairs):
    p = ROOT + path
    s = open(p, encoding='utf-8', newline='').read()
    for old, new in pairs:
        assert s.count(old) == 1, (path, old[:60], s.count(old))
        s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)


CONTRACT = '''### Finance

The owner's finance (`finance`, [finance.md](../features/finance.md)): read models over the space's ledger, every figure computed by the server on Gaza's calendar ([data-model › Front desk and money](../architecture/data-model.md#front-desk-and-money)), every amount whole agorot. The web builds any CSV from these answers; there is no export route (the owner's decision 5). The routes sit under `/manage/spaces/:spaceId/finance` and answer as *Managed spaces* says: without an active `OWNER` or `RECEPTION` link at the live space, `not_found` (404), the admin included. Each is the owner's (`finance.read`): reception is `forbidden` (403) before the query is read. Nothing is written. Built 2026-10-29, #PRNUM.

- **The month** (`financeMonthQuery`, `@masaha/shared/finance`): `month`, `YYYY-MM`, a Gaza calendar month (`invalid_format` otherwise), the current one when absent; the current Gaza month and the 23 before it (`FINANCE_MONTHS_BACK`), `out_of_range` on `month` otherwise, never a month ahead. There is no free range of dates (the owner's decision 3).
- **Income is cash collected:** the payments not voided, each counted on the Gaza day it was received, a window running from a Gaza midnight to the next, its end left out. A written-off visit's payments count as received; what it forgave counts nowhere, and a debt is never income (the owner's decision 2).

```ts
IncomeSplit = { subscriptionsAgorot: number, visitsAgorot: number, totalAgorot: number }
IncomeReport = {
  month: string,                                        // YYYY-MM, as asked or the current
  income: IncomeSplit, previousMonth: IncomeSplit, today: IncomeSplit,
  allTime: IncomeSplit & { since: string | null },      // the Gaza day of the first payment not voided
  months: { month: string, income: IncomeSplit }[],     // 12, oldest first, ending with the current month
  visitsByDay: { date: string, agorot: number }[],      // the visits' 30 Gaza days, oldest first, ending today
  collections: {                                        // the month's, the largest first, then by id
    recordedBy: { id, name }, count: number, totalAgorot: number,
    byMethod: { CASH: number, TRANSFER: number }
  }[]
}
```

#### `GET /manage/spaces/:spaceId/finance/income` · 🏢
- **Query:** `month`.
- **200:** `IncomeReport`: the month's income by the kind of item paid, the month before it, today and all time; the 12 months ending with the current one and the visits' 30 days ending today, whatever the month asked; and each staff member's collections in the month — how many payments, their sum, and by method — named, one whose link ended included. The sums and the collections read one snapshot, so the month equals its bar.
- **Errors:** `forbidden` (403) for reception, before the query is read; `validation` (422) on `month`; `not_found` (404).

'''

edit('docs/api/api-contract.md', [
    ('PaymentsMeta = PaginationMeta & { totals: PaymentTotals }\n```\n\n### Announcements (managed)',
     'PaymentsMeta = PaginationMeta & { totals: PaymentTotals }\n```\n\n' + CONTRACT + '### Announcements (managed)'),
])

edit('docs/architecture/data-model.md', [
    ('Last Updated:** 2026-10-28', 'Last Updated:** 2026-10-29'),
    ('- **Income:** the payments that are not voided, counted by the day received: today, this month (against last month) and all time, split into visits and subscriptions.\n- **Collections:** the same payments grouped by who recorded them. Reception sees its own for today; the owner sees every staff member.',
     "- **Income:** the payments that are not voided, each counted on the Gaza day it was received — a window from a Gaza midnight to the next, its end left out: a month (against the month before), today and all time, split into visits and subscriptions; the last 12 months and the visits' last 30 days. A written-off visit's payments count as received; what it forgave does not, and a debt is never income (the owner's decision 2, 2026-10-29, #PRNUM).\n- **Collections:** the same payments grouped by who recorded them, by method. Reception sees its own for today; the owner sees each staff member's of a month, one whose link has ended included (2026-10-29, #PRNUM)."),
])

edit('docs/backend/conventions.md', [
    ('| `finance` | L5 | — (reads) | manage | Read model: finance and statistics, including the occupancy statistics |',
     "| [`finance`](../features/finance.md) | L5 | — (reads) | manage | Read model: the owner's finance — a month's income and the staff's collections; the ledger's aggregates through `payments` (§9) |"),
])

edit('docs/backend/security.md', [
    ('Last Updated:** 2026-10-27', 'Last Updated:** 2026-10-29'),
    ("- **A closure's extension is its owner's**",
     "- **A space's finance is its owner's** (`finance.read`): each route under `/manage/spaces/:spaceId/finance` asks `requireCan` before the query is read, so reception is refused (403); the admin, who has no link to a space, is refused by the boundary like any stranger. 2026-10-29, #PRNUM.\n- **A closure's extension is its owner's**"),
])

edit('docs/features/payments.md', [
    ("- Answers a space's balances paged and totalled, by the same aggregate:",
     "- Answers what a space received in windows of instants, the payments not voided, split by the kind of item paid; its first payment's time; and each staff member's collections in a window, by method — for [finance](finance.md)'s income.\n- Answers a space's balances paged and totalled, by the same aggregate:"),
    ("- **Finance** (the `finance` module) reads the balances' page and totals",
     "- **Finance** ([finance](finance.md)) reads the income and the collections, the balances' page and totals"),
    ("**The uncollected visits counted.**",
     "**The income and the collections.** One statement sums the space's payments not voided over many windows at once, the windows two arrays of instants unnested in their order (an open end is `-infinity` or `infinity`), each window a range of the payments' `space_id, received_at` index, split by the kind of item paid; one more groups a window's by who recorded them, counted, summed and summed by method, the largest first. The windows are their reader's, on Gaza's calendar; each reads in the caller's snapshot when given (2026-10-29, #PRNUM).\n\n**The uncollected visits counted.**"),
    ("- #PRNUM — a space's balances paged and totalled, and the uncollected visits counted, for finance and the owner's overview.",
     "- #PRNUM — a space's balances paged and totalled, and the uncollected visits counted, for finance and the owner's overview; the income over windows and the staff's collections, for finance."),
])
print('ok')
