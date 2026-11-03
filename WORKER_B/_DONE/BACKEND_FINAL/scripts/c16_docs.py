def edit(p, pairs):
    s = open(p, encoding='utf-8', newline='').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old[:70], s.count(old))
        s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)

V = 'docs/plans/v1-mvp.md'
edit(V, [
    ('**Last Updated:** 2026-10-28', '**Last Updated:** 2026-10-29'),
    ("- **Settles:** charts and CSV exports.",
     "- **Settles:** charts and CSV exports: the API answers each chart's series and figure, aggregated on the server; the CSV is built in the browser from the JSON, so there is no export route (the owner's decisions 4 and 5, 2026-10-26)."),
    ("- **Built:** the platform's settings, on the API: the admin's three cards — the new-space defaults, the staleness thresholds and the contact — and the public contact (2026-10-28, #130).",
     "- **Built:** the platform's settings, on the API: the admin's three cards — the new-space defaults, the staleness thresholds and the contact — and the public contact (2026-10-28, #130).\n- **Built:** the space's finance, on the API: a month's income with the month before, today, all time, the last 12 months, the visits' last 30 days and each staff member's collections; who owes and who is in credit, with the totals and the reminder template; who paid in a month; and the occupancy statistics from closed stays — four reads, the owner's alone ([api-contract › Finance](../api/api-contract.md#finance), 2026-10-29, #PRNUM). Screen 19 remains planned."),
    ("- **Supported by:** conventions §9: [overview](../backend/conventions.md#overview).",
     "- **Supported by:** conventions §9: [overview](../backend/conventions.md#overview).\n- **Built:** both overviews, on the API: the owner's work queue — the fact groups missing or stale, the open reports, the uncollected and unpriced visits, the closures awaiting their extension, capacity, how many customers owe (a count, no amount), present now with the live status, the subscriptions ending soon and the running announcements; and the admin's — the spaces by status, the open reports by who handles them, the new users of the last 30 days and the spaces whose data is incomplete; each figure read from its owning module and equal to the list it links to ([api-contract › Overview](../api/api-contract.md#overview), 2026-10-29, #PRNUM). Screens 12 and 25 remain planned."),
    ("| GET / PATCH | `/me` | 👤 name, language |",
     "| GET / PATCH | `/me` | 👤 name, language (built, #PRNUM) |"),
    ("| GET | `/manage/spaces/:spaceId/visits` | 🧾 | a date range (the open visits are answered by `…/occupancy`, the uncollected by `…/uncollected-visits`, since step 7) |",
     "| GET | `/manage/spaces/:spaceId/visits` | 🧾 | a range of Gaza days, the owner's; reception today's only (built, #PRNUM). The open visits are answered by `…/occupancy`, the uncollected by `…/uncollected-visits`, since step 7 |"),
    ("| GET | `/manage/spaces/:spaceId/finance/...` | 🏢 | summary, income by month, visit income per day, debtors and payers, collections per staff member, occupancy (by hour, by day, peaks, average stay); CSV export |",
     "| GET | `/manage/spaces/:spaceId/finance/{income \\| debts \\| payers \\| occupancy}` | 🏢 | income by month, visit income per day, collections per staff member; debtors and those in credit, with the totals; payers in a month; occupancy (by hour, by day, peak, average stay). No export route: the web builds the CSV from the JSON (built, #PRNUM) |\n| GET | `/manage/spaces/:spaceId/overview` | 🏢 | the owner's work queue: counts, no amount (built, #PRNUM) |"),
    ("| GET | `/admin/stats` | aggregate numbers only |",
     "| GET | `/admin/overview` | the admin's tiles and the spaces with incomplete data, counts only; replaces the planned `/admin/stats` (built, #PRNUM) |"),
])

O = 'docs/project/overview.md'
s = open(O, encoding='utf-8', newline='').read()
anchor = next(l for l in s.split('\n') if l.startswith('- [Occupancy](../features/occupancy.md)'))
edit(O, [
    ('**Last Updated:** 2026-10-28', '**Last Updated:** 2026-10-29'),
    (anchor, anchor + "\n- [Finance](../features/finance.md): on the API, a space's income for a month and its windows, the staff's collections, who owes and who is in credit with the totals, who paid in a month, and the occupancy statistics — the owner's alone.\n- [Overview](../features/overview.md): on the API, the owner's overview, a work queue of counts with no amount, and the admin's, the platform's tiles and the spaces with incomplete data."),
])

R = 'docs/README.md'
s = open(R, encoding='utf-8', newline='').read()
anchor = next(l for l in s.split('\n') if l.startswith('- [payments.md](features/payments.md)'))
edit(R, [
    (anchor, anchor + "\n- [finance.md](features/finance.md) — a space's finance, the owner's alone: a month's income and the staff's collections, who owes and who is in credit, who paid in a month, and the occupancy statistics (API only).\n- [overview.md](features/overview.md) — the two overviews: the owner's work queue of counts with no amount, and the admin's tiles and the spaces with incomplete data (API only)."),
])

C = 'docs/backend/conventions.md'
edit(C, [
    ("the audit reader (§6): the owner's log and the admin's (2026-10-27, #128). **Not yet built:**",
     "the audit reader (§6): the owner's log and the admin's (2026-10-27, #128); `finance` (a space's income, debts, payers and occupancy statistics) and `overview` (the owner's and the admin's, composed from their owners' set-based counts), and Gaza's months and last days in `core` (2026-10-29, #PRNUM). **Not yet built:**"),
    ("  - a person's email corrected at the forced change;",
     "  - a person's email corrected at the forced change; a person's own name and language (`user.profileEdited`, never on the admin's log, 2026-10-29, #PRNUM);"),
])
print('ok')

edit(V, [
    ("#### Me\nBuilt: `POST /me/password`,",
     "#### Me\nBuilt: `GET` / `PATCH /me`, one's own account, its name and language (#PRNUM, [api-contract › Me](../api/api-contract.md#me)); `POST /me/password`,"),
    ("#### Managed spaces (`/manage/spaces/:spaceId/...`)\nBuilt: `GET /manage/spaces`, and",
     "#### Managed spaces (`/manage/spaces/:spaceId/...`)\nBuilt: the finance's four reads and the owner's overview ([Finance](../api/api-contract.md#finance), [Overview](../api/api-contract.md#overview)) and the visits by day (#PRNUM); `GET /manage/spaces`, and"),
    ("#### Admin (`/admin/...`, 🛡)\nBuilt: the lookups,",
     "#### Admin (`/admin/...`, 🛡)\nBuilt: the admin's overview, `GET /admin/overview` (#PRNUM, [Overview](../api/api-contract.md#overview)); the lookups,"),
])
print('ok2')
