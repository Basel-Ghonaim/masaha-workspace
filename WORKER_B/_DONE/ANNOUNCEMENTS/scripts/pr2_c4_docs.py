import io, os
os.chdir(r'C:\dev\masaha\app-b')

def edit(p, pairs):
    s = io.open(p, encoding='utf-8', newline='').read()
    for o, n in pairs:
        assert s.count(o) == 1, (p, o)
        s = s.replace(o, n)
    io.open(p, 'w', encoding='utf-8', newline='').write(s)

edit('docs/plans/v1-mvp.md', [
("**Last Updated:** 2026-10-24", "**Last Updated:** 2026-10-25"),
("Built: `POST /me/password`, the password change and the forced change at first sign-in ([api-contract §5](../api/api-contract.md#5-endpoints)).",
 "Built: `POST /me/password`, the password change and the forced change at first sign-in ([api-contract §5](../api/api-contract.md#5-endpoints)); `GET /me/reports`, the user's own reports with the replies (#PRNUM, [api-contract › Data reports](../api/api-contract.md#data-reports))."),
("| GET | `/me/reports` | 👤 with the resolution note |", "| GET | `/me/reports` | 👤 with the resolution note (built, #PRNUM) |"),
("`GET /spaces/:slug/occupancy`, a space's live status alone ([api-contract §5](../api/api-contract.md#directory-public)).",
 "`GET /spaces/:slug/occupancy`, a space's live status alone ([api-contract §5](../api/api-contract.md#directory-public)); `POST /spaces/:slug/reports`, a signed-in user's report of a listed space, 10 an hour (#PRNUM, [api-contract › Data reports](../api/api-contract.md#data-reports))."),
("| POST | `/spaces/:slug/reports` | 👤 | report wrong information |", "| POST | `/spaces/:slug/reports` | 👤 | report wrong information (built, #PRNUM) |"),
("[Customers (managed)](../api/api-contract.md#customers-managed)).", "[Customers (managed)](../api/api-contract.md#customers-managed)); and the space's data reports, the owner's list and decision (#PRNUM, [Data reports](../api/api-contract.md#data-reports))."),
("| 🏢 | resolve with an optional note, or dismiss (the owner keeps them once the space is verified) |", "| 🏢 | resolve with an optional note, or dismiss with a required one (the owner keeps them once the space is verified; built, #PRNUM) |"),
("a space's photos, `/admin/spaces/:spaceId/photos`: the list, an upload, a removal and the order ([api-contract §5](../api/api-contract.md#5-endpoints)).",
 "a space's photos, `/admin/spaces/:spaceId/photos`: the list, an upload, a removal and the order ([api-contract §5](../api/api-contract.md#5-endpoints)); the data reports, `/admin/data-reports`: every report with its reporter, and the decision of an unverified space's (#PRNUM)."),
("| read all; resolve (with an optional note) or dismiss those of unverified spaces |", "| read all; resolve (with an optional note) or dismiss (with a required one) those of unverified spaces (built, #PRNUM) |"),
("`CLOSURE_IN_FORCE` at check-in (#112, [api-contract › Announcements (managed)](../api/api-contract.md#announcements-managed)). The screens remain planned.",
 "`CLOSURE_IN_FORCE` at check-in (#112, [api-contract › Announcements (managed)](../api/api-contract.md#announcements-managed)); data reports, on the API: a signed-in user's report (10 an hour, a repeat answering the open one), the user's own with the replies, the owner's and the admin's lists and decisions, the reporter anonymous to the owner (#PRNUM, [api-contract › Data reports](../api/api-contract.md#data-reports)). The screens remain planned."),
])

edit('docs/project/overview.md', [
("**Last Updated:** 2026-10-24", "**Last Updated:** 2026-10-25"),
("- Data reports about the space, resolved with an optional note. Audit log. Settings.", "- Data reports about the space, resolved with an optional note, or dismissed with a reply. Audit log. Settings."),
("- Data reports (resolved with an optional note). Users (", "- Data reports (resolved with an optional note, or dismissed with a reply). Users ("),
("- [Occupancy](../features/occupancy.md): on the API,", "- [Data reports](../features/data-reports.md): on the API, a signed-in user's report of a listed space's wrong information and their own reports with the replies; the owner's and the admin's lists and decisions, the reporter anonymous to the owner.\n- [Occupancy](../features/occupancy.md): on the API,"),
])

edit('docs/README.md', [
("- [desk.md](features/desk.md)", "- [data-reports.md](features/data-reports.md) — a space's data reports: a signed-in user's report (10 an hour, a repeat answering the open one), their own with the replies, and the owner's and the admin's lists and decisions, the reporter anonymous to the owner (API only).\n- [desk.md](features/desk.md)"),
])

edit('docs/backend/conventions.md', [
("`data-reports` (a user's report of a listed space, 2026-10-25, #PRNUM)", "`data-reports` (a user's report of a listed space, their own, and the owner's and the admin's lists and decisions, 2026-10-25, #PRNUM)"),
])

edit('docs/backend/security.md', [
("Resolving its data reports follows the same rule. `can()` decides, from the links on the request",
 "Resolving its data reports follows the same rule: on `/admin/data-reports`, `can()` reads the space's links under its lock, so an owner linked while the admin's decision waits makes it `forbidden` (2026-10-25, #PRNUM). `can()` decides, from the links on the request"),
])

edit('docs/api/api-contract.md', [
("""MyReport = SpaceReport & {
  space: { id: number, slug: string, nameEn: string, nameAr: string | null, listed: boolean }
}
```""", """MyReport = SpaceReport & {
  space: { id: number, slug: string, nameEn: string, nameAr: string | null, listed: boolean }
}

AdminReport = SpaceReport & {
  space: { id: number, slug: string, nameEn: string, nameAr: string | null, verified: boolean },
  reporter: { id: number, name: string },
  decidedBy: { id: number, name: string } | null
}
```"""),
("""`conflict` (409) `REPORT_ALREADY_DECIDED`. Built 2026-10-25, #PRNUM.
""", """`conflict` (409) `REPORT_ALREADY_DECIDED`. Built 2026-10-25, #PRNUM.

#### `GET /admin/data-reports` · 🛡
- **Query:** `status` (`OPEN` or `DECIDED`), `field`, `spaceId` (a positive id) and §4's `page` and `limit`, each optional; `invalid_choice` or `validation` otherwise.
- **200:** `AdminReport[]`, every space's, newest first, then id, with §4's `meta`: who reported and who decided, by name, and whether the space is verified now. A soft-deleted space's reports are left out ([ADR 0007](../architecture/decisions/0007-soft-delete.md)). Built 2026-10-25, #PRNUM.

#### `PATCH /admin/data-reports/:reportId` · 🛡
- **Body:** `{ status: 'RESOLVED' | 'DISMISSED', note? }`.
- **200:** `AdminReport`, decided now with `repliedBy: 'MASAHA'`; the same decision again answers it as it is.
- **Errors**, each writing nothing: `validation` (422) on the body; `not_found` (404) for no such report, or a deleted space's; `forbidden` (403) for a verified space's report — its owner decides it — also when an owner was linked while the decision waited (the links read under the space's lock); `conflict` (409) `REPORT_ALREADY_DECIDED`, also when the owner decided it first. Built 2026-10-25, #PRNUM.
"""),
])

edit('docs/features/data-reports.md', [
("""- Pages a space's reports for its owner, by status and field, never showing who reported; lets the owner resolve one, with a reply or none, or dismiss it with a reply. A decided report is final; the same decision again answers it as it is.
""", """- Pages a space's reports for its owner, by status and field, never showing who reported; lets the owner resolve one, with a reply or none, or dismiss it with a reply. A decided report is final; the same decision again answers it as it is.
- Pages every report for the admin, by status, field and space, with who reported and who decided and whether the space is verified; lets the admin decide an unverified space's.
"""),
("""Reception is refused. The owner's screen is not built.""", """Reception is refused. The owner's screen is not built.
- **The admin,** under `/admin/data-reports`: every report, and the decision of an unverified space's. The admin's screen is not built."""),
("""a space's names to `spaces` (`namesWithDeleted`),""", """a space's names to `spaces` (`namesWithDeleted`), whether a space is verified to `space-links` (`verifiedSpaceIds`, `linksAt` under the lock), the people's names to `users` (`namesFor`),"""),
("""- A decision is audited in its own transaction""", """- Its admin router sits at `/data-reports` inside `/admin`, behind `requireRole('ADMIN')`; its decision asks `can()` on the links `space-links` reads under the space's lock.
- A decision is audited in its own transaction"""),
("""Lock order: the space's row, then the report's;""", """The admin's decision is the same, with any space's report, the links read through `space-links` under the lock (so the admin decides an unverified space's only, and an owner linked meanwhile makes it `forbidden`), and the side `ADMIN`. The owner and the admin at once: the second waits on the space's lock and finds the report decided. Lock order: the space's row, then the report's;"""),
("""**Decide.**""", """**The admin's list.** A page of every report whose space is not deleted, newest first, by status, field and space, with who reported and who decided; then the spaces' names, the verified spaces' ids and the people's names, one query each.

**Decide.**"""),
("""- **The owner never sees who reported** (O12). *Why:* a reporter must not fear the space; the admin, who answers for the platform, sees them.""", """- **The owner never sees who reported; the admin does** (O12). *Why:* a reporter must not fear the space; the admin, who answers for the platform, sees them.
- **The admin decides an unverified space's reports only, read under the space's lock** (`can()` with "verified", [conventions § `data-reports`](../backend/conventions.md#data-reports)). *Why:* once an owner joins, the space answers for itself; an owner linked while the admin's decision waits must win. 2026-10-25, #PRNUM."""),
("""the owner's list and decision.""", """the owner's and the admin's lists and decisions."""),
("its site and manage routers,", "its site, manage and admin routers,"),
])
print('ok')
