ROOT = 'C:/dev/masaha/app-b-lane-f/'
NL = chr(10)
FENCE = chr(96) * 3


def edit(path, pairs):
    p = ROOT + path
    s = open(p, encoding='utf-8', newline='').read()
    for old, new in pairs:
        assert s.count(old) == 1, (path, old[:60], s.count(old))
        s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)


BULLET = "- **Occupancy statistics** come from closed stays only — the visits and the subscription check-ins, those closed by the auto check-out included, open ones left out (the owner's decision 7) — each counted on the Gaza day of its check-in ([data-model › Front desk and money](../architecture/data-model.md#front-desk-and-money), *Occupancy statistics*)."

TYPES = """OccupancyReport = {
  month: string,
  averageStayMinutes: { all: number | null, members: number | null, visits: number | null },   // whole minutes; null: no stay
  peakHour: number | null,                              // 0–23, the month's
  averageDailyAttendance: number | null,                // one decimal
  byDay: { date: string, visits: number, members: number }[],   // 14 Gaza days, oldest first, ending today
  byHour: { weekday: number, hours: number[] }[]        // 7 (0 = Sunday … 6), each 24 averages, one decimal
}
"""

ROUTE = """#### `GET /manage/spaces/:spaceId/finance/occupancy` · 🏢
- **Query:** `month`.
- **200:** `OccupancyReport`: the month's figures over its days up to today — the average stay (all, members, visits), the peak hour (the hour of the day with the most presence, ties the earliest) and the average daily attendance (visits and members, a member once a day, over the days with any); visits and members per day over the 14 days ending today; the average present per Gaza weekday and hour over the 28 days before today (the stays overlapping each hour, summed, ÷ 4), today left out. The 14 and the 28 days end with today whatever the month asked. Each figure stands alone: read in parallel, with no snapshot.
- **Errors:** `forbidden` (403) for reception, before the query is read; `validation` (422) on `month`; `not_found` (404).

"""

edit('docs/api/api-contract.md', [
    ("it is counted apart (`uncollected`, the desk's list, [Front desk (managed)](#front-desk-managed)).",
     "it is counted apart (`uncollected`, the desk's list, [Front desk (managed)](#front-desk-managed))." + NL + BULLET),
    ("Payer = { customer: { id, name }, paidAgorot: number, lastPaidAt: string }  // in the month" + NL,
     "Payer = { customer: { id, name }, paidAgorot: number, lastPaidAt: string }  // in the month" + NL + TYPES),
    ('`not_found` (404).' + NL + NL + '### Announcements (managed)',
     '`not_found` (404).' + NL + NL + ROUTE + '### Announcements (managed)'),
])

edit('docs/architecture/data-model.md', [
    ("- **Occupancy statistics:** peak hours and average stay, from visits and subscription check-ins.",
     "- **Occupancy statistics:** from closed stays only — visits and subscription check-ins, the auto check-out's included, open ones left out (the owner's decision 7) — each on the Gaza day of its check-in: visits and members per day (a member counted once a day); the average present per Gaza weekday and hour, the stays overlapping each hour summed over the 28 days before today and divided by 4; a month's peak hour, the hour of the day with the most presence (ties the earliest); its average daily attendance, visits and members over the days with any; and its average stay in whole minutes, members and visits apart (2026-10-29, #PRNUM)."),
])

edit('docs/backend/conventions.md', [
    ("who owes and who is in credit, who paid in a month; the ledger's aggregates through `payments` (§9) |",
     "who owes and who is in credit, who paid in a month, and the occupancy statistics; the ledger's aggregates through `payments` (§9) |"),
])

edit('docs/features/finance.md', [
    ("- Answers who paid in a month, each customer with what they paid then, the latest first, paged." + NL,
     "- Answers who paid in a month, each customer with what they paid then, the latest first, paged." + NL + "- Answers the occupancy statistics from closed stays: visits and members per day over the 14 days ending today; the average present per Gaza weekday and hour over the 28 days before today; and a month's average stay, peak hour and average daily attendance." + NL),
    ("Who paid in a month it reads in its own query, over the payments and the items they paid (R7).",
     "Who paid in a month it reads in its own query, over the payments and the items they paid, and the occupancy statistics over the `visits` and `check_ins` tables (R7: they are `finance`'s, [conventions §9](../backend/conventions.md#9-placements)); it writes neither."),
    ("**Who paid.**", "**Occupancy.** Closed stays only, the auto check-out's included: a `WITH` of the space's visits and check-ins closed and checked in within the range read, bounded on their `space_id, checked_in_at` indexes (a stay never crosses its check-in's Gaza day). Per day, one statement over the days' windows: the visits checked in, and the members, each once (`count(DISTINCT customer_id)`). Per hour slot (`hourSlots`, every hour of each Gaza day labelled by Gaza's weekday and hour, so a daylight-saving day has 23 or 25), one statement: the stays overlapping it. The pure grid (`occupancyGrid.ts`) sums the 28 days' slots per weekday and hour and divides by 4, one decimal, half up; takes the month's peak hour (ties the earliest); and averages the month's daily attendance over the days with any. The average stay is the database's, rounded to whole minutes. Five statements in parallel, no snapshot: each figure stands alone." + NL + NL + "**Who paid.**"),
    ("- **The aggregates are `payments`', not `finance`'s** (S3).",
     "- **Occupancy statistics are `finance`'s, from closed stays; the 28 days leave today out and divide by 4** (the owner's decisions 7, Q3). *Why:* an open stay has no length yet; without today each weekday counts exactly four times, so the divisor is the same for every cell. 2026-10-29, #PRNUM.\n- **The month's figures read its days up to today; the 14 and the 28 days always end with today** (D11). *Why:* the month chosen is a period of the tabs, the charts' windows are fixed (the owner's decision 3). 2026-10-29, #PRNUM.\n- **No snapshot for the occupancy** (D12). *Why:* no figure must equal another, and the five reads run in parallel. 2026-10-29, #PRNUM.\n- **The aggregates are `payments`', not `finance`'s** (S3)."),
    ("its repository (who paid), its mapper, its windows (`windows.ts`)",
     "its repository (who paid, the stays), its mapper, its windows (`windows.ts`), the occupancy grid (`occupancyGrid.ts`)"),
    ("who paid in a month." + NL, "who paid in a month; the occupancy statistics." + NL),
])
print('ok')
