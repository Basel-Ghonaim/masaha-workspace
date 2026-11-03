ROOT = 'C:/dev/masaha/app-b-lane-f/'


def edit(path, pairs):
    p = ROOT + path
    s = open(p, encoding='utf-8', newline='').read()
    for old, new in pairs:
        assert s.count(old) == 1, (path, old[:60], s.count(old))
        s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)


CONTRACT = '''- **Who owes** is the ledger's one balance rule ([data-model › Front desk and money](../architecture/data-model.md#front-desk-and-money), *Customer debt*), as the customers list's: a written-off visit, a voided payment and an unpriced visit owe nothing; credit on one subscription never offsets another item's debt, so one customer may both owe and be in credit. **An archived customer's debt is kept,** marked `archived` (it is still owed). A walk-in's uncollected visit is no customer's debt: it is counted apart (`uncollected`, the desk's list, [Front desk (managed)](#front-desk-managed)).

```ts
BalanceRow = {
  customer: { id, name, phone: string | null, archived: boolean },
  amountAgorot: number,                                 // OWES: the debt; CREDIT: the credit
  oldestItem: {                                         // OWES only; null in credit
    kind: 'VISIT' | 'SUBSCRIPTION', id,
    name: string | null,                                // a visit's visitor, else its customer; a subscription's name
    since: string                                       // the Gaza day it was made
  } | null
}
DebtsMeta = §4's meta & {
  totals: {
    owed: { agorot: number, customers: number },        // every customer who owes, archived ones included
    credit: { agorot: number, customers: number },
    uncollected: { visits: number, owedAgorot: number, unpriced: number }   // the desk's list, counted
  },
  reminderTemplate: string | null                       // the space's; null: the catalogue's default
}
Payer = { customer: { id, name }, paidAgorot: number, lastPaidAt: string }  // in the month
```

'''

ROUTES = '''#### `GET /manage/spaces/:spaceId/finance/debts` · 🏢
- **Query** (`debtsQuerySchema`): `state`, `OWES` (the default) or `CREDIT` (`invalid_choice` otherwise); `page`, `limit` (§4).
- **200:** a page of `BalanceRow`: who owes, or who is in credit, the largest amount first, then by customer id, each with their phone (for the reminder, a WhatsApp link the web builds); who owes with the item still owing made first, a visit before a subscription made at the same instant; `meta: DebtsMeta`, the pagination, the space's totals over every customer, and its reminder template. The page, its totals and the template read one snapshot, so the rows of every page add up to the totals. A CSV of every debtor is the web's, from the pages.
- **Errors:** `forbidden` (403) for reception, before the query is read; `validation` (422) on the query; `not_found` (404).

#### `GET /manage/spaces/:spaceId/finance/payers` · 🏢
- **Query** (`payersQuerySchema`): `month`; `page`, `limit` (§4).
- **200:** a page of `Payer`: each customer whose items were paid in the month — the payments not voided, a visit's customer or a subscription's; a walk-in's payment names no one and is left out — with what they paid in it and when they last paid, the latest first, then by customer id; an archived customer included; `meta` the pagination. Read apart, as every list.
- **Errors:** `forbidden` (403) for reception, before the query is read; `validation` (422) on the query; `not_found` (404).

'''

NL = chr(10)
FENCE = chr(96) * 3
BULLET, TYPES = CONTRACT.split(FENCE + 'ts' + NL, 1)
TYPES = TYPES.split(FENCE, 1)[0]
edit('docs/api/api-contract.md', [
    ("never income (the owner's decision 2)." + NL + NL + FENCE + 'ts' + NL + 'IncomeSplit',
     "never income (the owner's decision 2)." + NL + BULLET.rstrip(NL) + NL + NL + FENCE + 'ts' + NL + 'IncomeSplit'),
    ('    byMethod: { CASH: number, TRANSFER: number }' + NL + '  }[]' + NL + '}' + NL + FENCE,
     '    byMethod: { CASH: number, TRANSFER: number }' + NL + '  }[]' + NL + '}' + NL + TYPES + FENCE),
    ('`not_found` (404).' + NL + NL + '### Announcements (managed)',
     '`not_found` (404).' + NL + NL + ROUTES + '### Announcements (managed)'),
])

edit('docs/backend/conventions.md', [
    ("Read model: the owner's finance — a month's income and the staff's collections; the ledger's aggregates through `payments` (§9) |",
     "Read model: the owner's finance — a month's income and the staff's collections, who owes and who is in credit, who paid in a month; the ledger's aggregates through `payments` (§9) |"),
])

edit('docs/features/customers.md', [
    ('Last Updated:** 2026-10-26', 'Last Updated:** 2026-10-29'),
    ("- **[`payments`](payments.md),** which names a subscription's customer in the payments it answers.\n",
     "- **[`payments`](payments.md),** which names a subscription's customer in the payments it answers.\n- **[`finance`](finance.md),** which reads its debtors' names, phones and whether each is archived, and its payers' names.\n"),
    ("the contacts of a set of customers, for the check-ins' lists.\n",
     "the contacts of a set of customers, for the check-ins' lists.\n- #PRNUM — the contacts answer whether each customer is archived, for finance's debts.\n"),
])

edit('docs/features/subscriptions.md', [
    ("and the customers' names and phones for the check-ins' lists from [`customers`](customers.md).",
     "and the customers' names and phones for the check-ins' lists from [`customers`](customers.md) (a check-in's customer answered with those two alone)."),
])

edit('docs/features/finance.md', [
    ("statistics_placeholder", "statistics_placeholder"),
] if False else [
    ("Answers a month's income, the payments not voided, by the kind of item paid: the month (the current Gaza month by default, at most 23 back), the month before it, today and all time with its first day; the last 12 months and the visits' last 30 days, by Gaza day; and each staff member's collections in the month, by method.\n",
     "Answers a month's income, the payments not voided, by the kind of item paid: the month (the current Gaza month by default, at most 23 back), the month before it, today and all time with its first day; the last 12 months and the visits' last 30 days, by Gaza day; and each staff member's collections in the month, by method.\n- Answers who owes and who is in credit, by the ledger's one balance rule, the largest first, paged, with their phones, an archived customer kept and marked, and the item still owing made first; the space's totals, the uncollected visits apart, and its reminder template.\n- Answers who paid in a month, each customer with what they paid then, the latest first, paged.\n"),
    ("- **Reads** the income and the collections from [payments](payments.md), whose aggregates hold the one \"voided left out\" rule; the names of who recorded a payment from [users](users.md).",
     "- **Reads** the income, the collections, the balances' page and totals and the uncollected visits' counts from [payments](payments.md), whose aggregates hold the one \"voided left out\" and balance rules; the names of who recorded a payment from [users](users.md); the debtors' contacts and the payers' names from [customers](customers.md); the oldest item's name from [subscriptions](subscriptions.md) and [visits](visits.md); the reminder template from `space-settings`. Who paid in a month it reads in its own query, over the payments and the items they paid (R7)."),
    ("so a payment at 23:30 on a month's last day counts in that month and that day, and no zone is read in the database.\n",
     "so a payment at 23:30 on a month's last day counts in that month and that day, and no zone is read in the database.\n\n**Who owes.** In one snapshot: `payments.balancesPage` (the page, by `state`), `balanceTotals` and `uncollectedTotals`, and the space's settings; then, in the same snapshot, the page's customers' contacts (`archived` from `archivedAt`), its oldest subscriptions' names and its oldest visits as the desk sees them — a visit named by its visitor, else its customer. The item's day is the Gaza day it was made. Every amount comes from the ledger; `finance` adds none.\n\n**Who paid.** One statement over the month's payments not voided, each joined to its visit or subscription by primary key for the customer (`coalesce`), grouped by customer: the sum, the latest payment, and how many customers over the same rows (`count(*) OVER ()`; past the last page counted apart); then the page's names. Read apart, as every list; an archived customer is a payer like any other.\n"),
    ("- **The aggregates are `payments`', not `finance`'s** (S3).",
     "- **The debts read one snapshot: the page, the totals, the uncollected counts, the names and the template** (S2). *Why:* the page's rows must add up to its totals across pages read in turn; the names ride in it, since `deskVisitsOf` takes the snapshot's transaction (EC6). 2026-10-29, #PRNUM.\n- **An archived customer's debt is kept and marked** (Q2). *Why:* it is still owed, and the desk collects it; the customers list's `payment=OWES` leaves archived customers out, so its total may be smaller than `totals.owed.customers`. 2026-10-29, #PRNUM.\n- **Who paid is `finance`'s own query; the voided rule is written there a second time, as a `WHERE`** (D12). *Why:* it groups the month's payments by their items' customers, which no ledger function answers; its sums are no balance. 2026-10-29, #PRNUM.\n- **The aggregates are `payments`', not `finance`'s** (S3)."),
    ("- `apps/api/src/modules/finance/` — the module: its service, its mapper, its windows (`windows.ts`), its controller and its manage router.\n- `packages/shared/src/finance/` — the month's query and its bound, the answers.",
     "- `apps/api/src/modules/finance/` — the module: its service, its repository (who paid), its mapper, its windows (`windows.ts`), its controller and its manage router.\n- `packages/shared/src/finance/` — the month's query and its bound, the debts' and the payers' queries, the answers."),
    ("- #PRNUM — a month's income: the month, the month before, today and all time, the 12 months, the visits' 30 days and the staff's collections.",
     "- #PRNUM — a month's income: the month, the month before, today and all time, the 12 months, the visits' 30 days and the staff's collections; who owes and who is in credit, with the totals and the reminder template; who paid in a month."),
])

edit('docs/features/payments.md', [
    ("- **Finance** ([finance](finance.md)) reads the income and the collections, the balances' page and totals",
     "- **Finance** ([finance](finance.md)) reads the income and the collections, for its income; the balances' page and totals"),
])
print('ok')
