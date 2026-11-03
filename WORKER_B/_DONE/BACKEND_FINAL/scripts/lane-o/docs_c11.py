R = 'C:/dev/masaha/app-b-lane-o/'
TAG = '2026-10-29, #PRNUM'


def edit(path, pairs):
    p = R + path
    s = open(p, encoding='utf-8', newline='').read()
    for old, new in pairs:
        assert s.count(old) == 1, (path, old[:70], s.count(old))
        s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)


edit('docs/api/api-contract.md', [
 ("""  at: string                                  // the instant read
}
```

#### `GET /manage/spaces/:spaceId/overview` · 🏢""", """  at: string                                  // the instant read
}

AdminOverview = {
  spaces: {                                   // none deleted
    verified: number,                         // = GET /admin/spaces?status=verified's total
    unverified: number,                       // = ?status=unverified's
    hidden: number,                           // = ?status=hidden's
    unverifiedNoOwner: number,                // «بلا مالك»: an unverified space has no active owner, so = unverified
    staleOrMissing: number                    // = ?stale=true's
  },
  reports: {                                  // the open reports of the live spaces: = GET /admin/data-reports?status=OPEN's total
    open: number,
    awaitingAdmin: number,                    // an unverified space's: the admin decides them
    awaitingOwners: number                    // a verified space's
  },
  newUsers: number,                           // the accounts created since the Gaza midnight 29 days before today
  completeness: {                             // «اكتمال البيانات»: = ?status=editable&stale=true
    total: number,
    first: { id: number, nameEn: string, nameAr: string | null, hidden: boolean,
             missing: FactGroup[], stale: { group: FactGroup, days: number }[] }[]   // ≤ 5, by English name, then id
  },
  at: string
}
```

#### `GET /manage/spaces/:spaceId/overview` · 🏢"""),
 ("""- **Errors:** `forbidden` (403) for reception, which has no overview; `not_found` (404) for anyone who is not the space's staff, the admin included (the boundary).
""", """- **Errors:** `forbidden` (403) for reception, which has no overview; `not_found` (404) for anyone who is not the space's staff, the admin included (the boundary).

#### `GET /admin/overview` · 🛡
- **200:** `AdminOverview`: the platform's figures only, never a space's customers, visits, subscriptions, payments, capacity or presence ([ADR 0002](../architecture/decisions/0002-authorization-model.md)). Replaces the planned `GET /admin/stats` (the owner's OD4).
- **Errors:** `unauthorized` (401), `forbidden` (403), and `forbidden` (403) `PASSWORD_CHANGE_REQUIRED`, by `/admin`'s guard.
"""),
])

edit('docs/backend/conventions.md', [
 ("""- **It never imports `finance`:** the figures both show come from `payments`.
- Figures are fetched in parallel, one `Promise.all` at one instant,""",
  """- **The admin's figures** come from `space-links` (`adminSpaces.counts`, `staleEditable`: the admin's spaces list's own query, through `spaces`' `listing.count` and `listing.page`), `data-reports` (`openCounts`) and `users` (`countCreatedSince`, since `lastDaysSince` in `@masaha/shared/core`, the audit's own last-30-days rule) (""" + TAG + """).
- **It never imports `finance`:** the figures both show come from `payments`.
- Figures are fetched in parallel, one `Promise.all` at one instant,"""),
])

edit('docs/backend/security.md', [
 ("""- **The owner's overview is the owner's** (`space.overview.read`): `requireCan` refuses reception, which has none; the admin, who has no link to a space, is refused by the boundary like any stranger. It holds no amount (2026-10-29, #PRNUM).
""", """- **The owner's overview is the owner's** (`space.overview.read`): `requireCan` refuses reception, which has none; the admin, who has no link to a space, is refused by the boundary like any stranger. It holds no amount (2026-10-29, #PRNUM).
- **The admin's overview is the platform's figures only** (`/admin/overview`, behind `/admin`'s guard): never a space's customers, visits, subscriptions, payments, capacity or presence; no `can()` action of its own, as every admin route (2026-10-29, #PRNUM).
"""),
])

edit('docs/features/overview.md', [
 ("""- Holds no amount anywhere: the debts and the uncollected visits are counts (the owner's O3).
""", """- Answers the admin's overview of the platform in one read (screen 25): the spaces verified, unverified, hidden, unverified with no owner, and stale or missing; the open data reports, by who handles them; the accounts created in the last 30 Gaza days; and «اكتمال البيانات», the first five spaces whose facts the admin keeps with a group stale or missing, and their total.
- Holds no amount anywhere: the debts and the uncollected visits are counts (the owner's O3); the admin's holds nothing of a space's operations.
"""),
 ("""- **The space's owner,** under `/manage/spaces/:spaceId/overview`. Reception has none and is refused (the owner's OV3). The owner's screen (12) is to come, worker A's.
""", """- **The space's owner,** under `/manage/spaces/:spaceId/overview`. Reception has none and is refused (the owner's OV3). The owner's screen (12) is to come, worker A's.
- **The admin,** under `/admin/overview`. The admin's screen (25) is to come, worker A's.
"""),
 ("""the state at a glance from [`occupancy`](occupancy.md).
""", """the state at a glance from [`occupancy`](occupancy.md); for the admin, the spaces' counts and the spaces to complete from [`space-links`](space-links.md), the open reports by who handles them from [`data-reports`](data-reports.md), the new accounts from [`users`](users.md).
"""),
 ("""- Its manage router sits at `/overview` below `/manage/spaces/:spaceId`, behind the one boundary that admits the space's staff; its route asks `requireCan('space.overview.read')`.
""", """- Its manage router sits at `/overview` below `/manage/spaces/:spaceId`, behind the one boundary that admits the space's staff; its route asks `requireCan('space.overview.read')`. Its admin router sits at `/overview` inside `/admin`, behind its one guard.
"""),
 ("""## Decisions
""", """**The admin's overview** (`adminOverview.ts`). One instant; one `Promise.all` of four reads: `adminSpaces.counts` (verified, unverified, hidden, stale or missing, each its list's total), `adminSpaces.staleEditable` (five named), `dataReports.openCounts` and `users.countCreatedSince` from `lastDaysSince(at, 30)` — the Gaza midnight 29 days before today, the audit's own rule. «بلا مالك» is the unverified count: a space is verified exactly when it has an active owner (OD2).

## Decisions
"""),
 ("""- **Not polled** (OV7)""", """- **`GET /admin/overview` replaces the planned `/admin/stats`, and `can()`'s unused `platform.stats.read` is removed** (the owner's OD4). *Why:* the admin's routes are guarded once by `/admin`'s role guard, so the action guarded nothing. 2026-10-29, #PRNUM.
- **«بلا مالك» equals the unverified tile** (the owner's OD2 (a)): unverified and not hidden. *Why:* "verified" is an active owner link, so the two are one set. 2026-10-29, #PRNUM.
- **«اكتمال البيانات»'s full list is `GET /admin/spaces?status=editable&stale=true`** (the owner's OD3 (a)): the unverified spaces, hidden ones included — those the admin can act on. *Why:* the card's total must equal the list it opens. 2026-10-29, #PRNUM.
- **No «بدون صور» in «اكتمال البيانات»** (EC9): the listing's row carries no photo count, and the owner's OV4 does not ask for it. 2026-10-29, #PRNUM.
- **New users: the last 30 Gaza days, every role** (OV5), by the audit log's own rule, moved to `@masaha/shared/core` (`lastDaysSince`) since `overview` cannot import `audit`. 2026-10-29, #PRNUM.
- **Not polled** (OV7)"""),
 ("""- `apps/api/src/modules/overview/` — the module: one file per screen (`ownerOverview.ts`), the service joining them, its controller and its manage router.""",
  """- `apps/api/src/modules/overview/` — the module: one file per screen (`ownerOverview.ts`, `adminOverview.ts`), the service joining them, its controller and its manage and admin routers."""),
 ("""- 2026-10-29, #PRNUM — the owner's overview (`GET /manage/spaces/:spaceId/overview`), with a set-based count added in each owning module.
""", """- 2026-10-29, #PRNUM — the owner's overview (`GET /manage/spaces/:spaceId/overview`) and the admin's (`GET /admin/overview`), with a set-based count added in each owning module.
"""),
])
print('ok')
