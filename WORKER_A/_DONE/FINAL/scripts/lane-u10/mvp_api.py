import sys
p = r'C:\dev\masaha\app-lane-u10\docs\plans\v1-mvp.md'
s = open(p, encoding='utf8', newline='').read()
reps = [
 ("Moves into [api-contract.md](../api/api-contract.md) endpoint by endpoint as each is built.",
  "Every route below is built and owned by [api-contract.md](../api/api-contract.md); nothing remains planned (2026-10-29, #PRNUM)."),
 ("`GET /manage/spaces`, and the API-only profile, facts, confirmations, photo, package and staff routes below,",
  "`GET /manage/spaces`, and the profile, facts, confirmations and photo routes below (#83), the package routes (#87) and the staff routes (#90),"),
 ("and the space's data reports, the owner's list and decision (#120, [Data reports](../api/api-contract.md#data-reports)).\n",
  "and the space's data reports, the owner's list and decision (#120, [Data reports](../api/api-contract.md#data-reports)); the written-off visits (`GET …/written-off-visits`), a visit's check-in for its customer, a subscription sold at the published price the desk showed, and one data report read by its id (2026-10-29, #PRNUM).\n"),
 ("the owner writes a visit off. The web screen and later\ndashboard modules remain planned ([api-contract §5](../api/api-contract.md#5-endpoints)).",
  "the owner writes a visit off. Each route's screens are in its step of the [build map](#sequence-inside-the-build) ([api-contract §5](../api/api-contract.md#5-endpoints))."),
 ("| the profile and all facts (read), the profile (edit) |", "| the profile and all facts (read), the profile (edit) (built, #83) |"),
 ("on the same logic as the admin's ([api-contract §5](../api/api-contract.md#spaces-the-admin)) |", "on the same logic as the admin's ([api-contract §5](../api/api-contract.md#spaces-the-admin)) (built, #83) |"),
 ("as the admin's confirm does ([api-contract §5](../api/api-contract.md#spaces-the-admin)) |", "as the admin's confirm does ([api-contract §5](../api/api-contract.md#spaces-the-admin)) (built, #83) |"),
 ("on the admin's service ([api-contract › Photos](../api/api-contract.md#photos)) |", "on the admin's service ([api-contract › Photos](../api/api-contract.md#photos)) (built, #83) |"),
 ("handed over ([api-contract › Staff (managed)](../api/api-contract.md#staff-managed)) |", "handed over ([api-contract › Staff (managed)](../api/api-contract.md#staff-managed)) (built, #90) |"),
 ("never public ([api-contract › Packages (managed)](../api/api-contract.md#packages-managed)) |", "never public ([api-contract › Packages (managed)](../api/api-contract.md#packages-managed)) (built, #87) |"),
 ("| list (search; filters: subscription type, status, payment), create |", "| list (search; filters: subscription type, status, payment), create (built, #102) |"),
 ("| details with subscriptions, balances and debt; edit |", "| details with subscriptions, balances and debt; edit (built, #102) |"),
 ("warns while an older debt remains |", "warns while an older debt remains (built, #106) |"),
 ("the owner its price and billing, with a reason |", "the owner its price and billing, with a reason (built, #106) |"),
 ("| end early: the end becomes today (its start, if it has not started) |", "| end early: the end becomes today (its start, if it has not started) (built, #106) |"),
 ("limit and full-space warnings in `meta.warnings` |", "limit and full-space warnings in `meta.warnings` (built, #109) |"),
 ("`/manage/spaces/:spaceId/check-ins/:checkInId/check-out` | 🧾 | |", "`/manage/spaces/:spaceId/check-ins/:checkInId/check-out` | 🧾 | built (#109) |"),
]
for a, b in reps:
    n = s.count(a)
    if n != 1:
        sys.exit('count %d: %s' % (n, a[:60]))
    s = s.replace(a, b)
open(p, 'w', encoding='utf8', newline='').write(s)
print('ok')
