def edit(p, pairs):
    s = open(p, encoding='utf-8', newline='').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old[:60], s.count(old))
        s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)

edit('docs/features/payments.md', [
    ("**Last Updated:** 2026-10-27", "**Last Updated:** 2026-10-29"),
    ("- Answers customers' debt and credit, the ids of those who owe or are in credit, and one customer's items with their balances — each computed in the database, by one aggregate query — and the payments of visits, voided ones marked, for a customer's file.",
     "- Answers customers' debt and credit, the ids of those who owe or are in credit, and one customer's items with their balances — each computed in the database, by one aggregate query — and the payments of visits, voided ones marked, for a customer's file.\n- Answers a space's balances paged and totalled, by the same aggregate: who owes or is in credit, the largest first, with the item still owing made first; the totals owed and in credit, each with how many customers; and the uncollected visits counted — all, what the priced ones still owe, the unpriced apart."),
    ("and, through its own route, the uncollected visits, which the owner's «يحتاج انتباهك» will count.",
     "and, through its own route, the uncollected visits, which the owner's «يحتاج انتباهك» will count.\n- **Finance** (the `finance` module) reads the balances' page and totals and the uncollected visits' counts for its debts; **the owner's overview** (the `overview` module) reads how many customers owe and how many visits are uncollected, never an amount ([conventions › Composed reads](../backend/conventions.md#composed-reads))."),
    ("**The uncollected visits.** One query and its count",
     "**The balances paged and totalled.** One statement over the balance aggregate of every customer of the space, an archived one's kept (it is still owed): per customer the debt or the credit, those above zero, the largest first, then by customer id, a page cut and counted over the same rows (`count(*) OVER ()`; past the last page counted apart); who owes with the item still owing made first, a visit before a subscription made at the same instant, then by id. The totals sum the same per-customer figures: owed and in credit, each with how many customers — a customer owing on one item and in credit on another is in both, as a credit never offsets another item's debt. Each reads in the caller's snapshot when given (2026-10-29, #PRNUM).\n\n**The uncollected visits counted.** The uncollected list's own `FROM` (one function both read), counted: all of them, what the priced ones still owe (charge − paid), and how many have no charge yet; one statement (2026-10-29, #PRNUM).\n\n**The uncollected visits.** One query and its count"),
    ("- #114 — the owner's void of a payment, a written-off visit's once the write-off is undone (the ledger's fourth rule both ways); a visit closed by hand with no customer that owes after a void, uncollected; the payments list with its totals, reception's own of today.",
     "- #114 — the owner's void of a payment, a written-off visit's once the write-off is undone (the ledger's fourth rule both ways); a visit closed by hand with no customer that owes after a void, uncollected; the payments list with its totals, reception's own of today.\n- #PRNUM — a space's balances paged and totalled, and the uncollected visits counted, for finance and the owner's overview."),
])

# the decision line, after decision 59 (debt computed in the database)
edit('docs/features/payments.md', [
    ("(step 8's plan, S9). 2026-10-21, #102.",
     "(step 8's plan, S9). 2026-10-21, #102.\n- **The balances' page and totals, and the uncollected counts, are this module's, not their readers'** (S3 of the plan). *Why:* the voided payment left out, the balance rule and the uncollected rule keep one home each; `finance` and `overview` read them, and `overview` may not import `finance`. Their totals read the same aggregate as the customers list's filter, so the figures agree. 2026-10-29, #PRNUM."),
])

edit('docs/backend/conventions.md', [
    ("  - `desk`, `finance` (debtors) and `overview` (total owed) all use the same APIs. None of them computes a status or a balance.",
     "  - `desk`, `finance` (debtors) and `overview` (how many owe, a count — never an amount, the owner's O3) all use the same APIs. None of them computes a status or a balance.\n  - **A space's balances paged and totalled, and its uncollected visits counted, are `payments`' too** (`balancesPage`, `balanceTotals`, `uncollectedTotals`), over the same aggregate and the uncollected list's own `FROM`: finance's debts and the overview's counts read them, never their own sums. 2026-10-29, #PRNUM."),
])
print('ok')
