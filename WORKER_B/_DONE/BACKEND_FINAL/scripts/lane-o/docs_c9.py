import re
R = 'C:/dev/masaha/app-b-lane-o/'
def edit(path, pairs, date=True):
    p = R + path
    s = open(p, encoding='utf-8', newline='').read()
    for old, new in pairs:
        assert s.count(old) == 1, (path, old[:60], s.count(old))
        s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)

CONTRACT = '''### Overview

The overviews (`overview`, [conventions › `overview`](../backend/conventions.md#overview)): one read per screen, composed from the modules that own each figure, read in parallel at one instant (`at`) with no lock and no snapshot, so each count equals the list it links to read alone, to within a write between two of its reads. They write nothing and nothing polls them: the web reads one again on returning to its page. **No amount anywhere** (the owner's O3): the debts and the uncollected visits are counts. Built 2026-10-29, #PRNUM.

```ts
GroupsFreshness = {
  missing: FactGroup[],                       // never saved
  stale: { group: FactGroup, days: number }[] // by the thresholds saved now (Platform settings); days: Gaza days since its date
}

OwnerOverview = {
  attention: {                                // «يحتاج انتباهك»
    groups: GroupsFreshness,
    openReports: number,                      // = GET …/data-reports?status=OPEN's total
    uncollectedVisits: number,                // = GET …/uncollected-visits' total
    unpricedVisits: number,                   // = GET …/unpriced-visits' total
    closuresAwaitingExtension: number,        // = GET …/announcements/summary's
    capacitySet: boolean,
    customersOwing: number                    // the customers who owe, archived ones kept: Finance's debtors, counted
  },
  presentNow: {                               // as GET …/occupancy reads it
    visits: number, members: number, total: number,
    capacity: number | null,
    status: LiveStatus | null                 // as the public sees it
  },
  endingSoon: {
    total: number,                            // = GET …/customers?status=ENDING_SOON's total
    first: { customer: { id, name }, subscription: { id, name, endsOn: string | null } }[]   // ≤ 5: by end date, none last, then id
  },
  announcements: {
    running: number,                          // = GET …/announcements?state=RUNNING's total
    types: AnnouncementType[]                 // the running ones' types, each once, in ANNOUNCEMENT_TYPES' order
  },
  at: string                                  // the instant read
}
```

#### `GET /manage/spaces/:spaceId/overview` · 🏢
- **200:** `OwnerOverview`.
- **Errors:** `forbidden` (403) for reception, which has no overview; `not_found` (404) for anyone who is not the space's staff, the admin included (the boundary).

### Internal'''
edit('docs/api/api-contract.md', [('### Internal', CONTRACT)])

edit('docs/backend/conventions.md', [
 ("| `overview` | L5 | — | manage, admin | Read composition for the two overview screens (§9) |",
  "| [`overview`](../features/overview.md) | L5 | — (reads through its owners) | manage, admin | Read composition for the two overview screens (§9) |"),
 ('''### `overview`
- One read-composition module, one file per screen (owner, admin), and one aggregate endpoint per screen because the users' connection is weak.
- **No logic:** every figure comes from its owning module.
- **It never imports `finance`:** the figures both show come from `payments`.
- Figures are fetched in parallel.
''', '''### `overview`
- One read-composition module, one file per screen (owner, admin), and one aggregate endpoint per screen because the users' connection is weak.
- **No logic:** every figure comes from its owning module, through a set-based read added where it had none (2026-10-29, #PRNUM): the groups missing and stale from `spaces` (`listing.freshnessOf`, with their Gaza days), the open reports from `data-reports` (`openCountOf`), the unpriced visits from `visits` (`unpricedCount`), the closures awaiting their extension and the running count from `subscriptions`' `closures.summary`, the running types from `announcements` (`runningTypes`), the subscriptions ending soon from `subscriptions` (`endingSoon`, the customers list's rule), the uncollected visits and how many owe from `payments` (`uncollectedTotals`, `balanceTotals`), and present now, the capacity and the live status from `occupancy` (`glance`).
- **No repository** (S20): an aggregate of its own would write a rule a second time, and its count would drift from the list it links to.
- **It never imports `finance`:** the figures both show come from `payments`.
- Figures are fetched in parallel, one `Promise.all` at one instant, **with no snapshot** (S21): each is a count standing alone, and a snapshot would run them one after another on one connection.
'''),
])

edit('docs/backend/security.md', [
 ("**Last Updated:** 2026-10-27", "**Last Updated:** 2026-10-29"),
 ('''- **A closure's extension is its owner's**''', '''- **The owner's overview is the owner's** (`space.overview.read`): `requireCan` refuses reception, which has none; the admin, who has no link to a space, is refused by the boundary like any stranger. It holds no amount (2026-10-29, #PRNUM).
- **A closure's extension is its owner's**'''),
])

edit('docs/frontend/design-system/foundation.md', [
 ("> **Last Updated:** 2026-10-28", "> **Last Updated:** 2026-10-29"),
 ("12. **Overview** (O) — present now / capacity and the live status, income today and this month, total debt, subscriptions ending this week, active announcements, new reports",
  "12. **Overview** (O) — needs attention (missing or stale groups, new reports, uncollected visits, a closure awaiting its extension, capacity not set, customers who owe — counts, no amounts, O3), present now / capacity and the live status, subscriptions ending this week, active announcements"),
])
print('ok')
