"""Commit 3's documents: data-reports.md (the admin's Web parts), space-links.md, architecture §2,
overview, finding 167 and its index line."""
ROOT = 'C:/dev/masaha/app-lane-b/docs/'


def edit(rel, pairs):
    path = ROOT + rel
    with open(path, encoding='utf8', newline='') as handle:
        text = handle.read()
    for old, new in pairs:
        assert text.count(old) == 1, (rel, old[:70], text.count(old))
        text = text.replace(old, new)
    with open(path, 'w', encoding='utf8', newline='') as handle:
        handle.write(text)


edit('features/data-reports.md', [
    (
        "The API is built; on the web, the owner's «بلاغات البيانات».",
        "The API is built; on the web, the owner's and the admin's «بلاغات البيانات».",
    ),
    (
        "any page group: the owner's list of a space's reports and the decision sheet.",
        "any page group: the owner's list of a space's reports, the admin's list of every space's, and the decision sheet.",
    ),
    (
        "- **The admin,** under `/admin/data-reports`: every report, and the decision of an unverified space's. The admin's screen is not built.",
        "- **The admin,** under `/admin/data-reports`: every report, and the decision of an unverified space's. On the dashboard, the admin reads «بلاغات البيانات» (`/dashboard/admin/reports`), filters it by one space with [space-links](space-links.md)' search, and decides an unverified space's report in the same sheet (2026-10-28, #PRNUM).",
    ),
    (
        "Closed, the sheet gives the focus back to its «فتح», or, that row gone, to the count.\n",
        "Closed, the sheet gives the focus back to its «فتح», or, that row gone, to the count.\n"
        "\n**The admin's reports on the web** (`features/data-reports`, composed by `pages/dashboard/admin/DataReportsPage.tsx`). «بلاغات البيانات» says the admin decides unverified spaces' reports and reads verified spaces' for reference, then the same chips, the space — [space-links](space-links.md)' `AdminSpaceFilter`, which the page sets: a search of the platform's spaces on the server, «كل المساحات» first, which clears it — and the field, every filter and the page in the address (`?status=&field=&space=&page=`), inline from 768 px and in a bottom sheet below it whose button counts what applies. The space and the field in force show under them at every width as removable tags («المساحة: {name}», «الحقل: {field}», each «إزالة فلتر …», [finding 8](../architecture/findings/8-the-stress-tests-applied-filter-tag-has-no-component.md)) beside «مسح الفلاتر», which takes both off; a space no report on the page names says «مساحة محددة». It lists `GET /admin/data-reports` 20 a page: until 1024 px a card each, from it a table of eight columns — the space, a link to its editor; the field; the report; the reporter, by name; the day; the status; «يعالجه» («الإدارة» `info` while the space is unverified, «المالك» `neutral` once verified); «فتح», or «عرض» for a verified space's. Its states as the owner's; a filter that matches nothing offers «عرض الكل», which takes every filter off. The sheet names the reporter («{name} · {day}») and its reply is «ردّ فريقنا»; «تعديل الحقل» leads to the field's section of the space's editor. A verified space's report opens read-only: «مساحة موثّقة — يقرّر مالكها هذا البلاغ. للاطلاع فقط.» with «عرض المساحة», no reply and no buttons. A 403 — the space verified meanwhile — says «هذه المساحة موثّقة: يقرّر مالكها هذا البلاغ.», the admin's reports are read again and the sheet is read-only.\n",
    ),
    (
        "- **The decision is sent once, with no key** (S4)",
        "- **The admin's chips are the owner's; the space and the field are fields** (DI-32, P5): the same «الكل · جديدة · تمت المراجعة»; the space a search on the server, the field a select. 2026-10-28, #PRNUM.\n"
        "- **A verified space's report is read-only for the admin, not a dead end** (DI-38): its notice says the owner decides it, with «عرض المساحة» to the space's editor. *Why:* the server refuses the admin's decision there (`can()` with \"verified\"). 2026-10-28, #PRNUM.\n"
        "- **«يعالجه» per row, from the space's verification now** (DI-39): «الإدارة» or «المالك»; no filter of it, which the API cannot serve ([finding 167](../architecture/findings/167-the-admins-reports-cannot-be-filtered-by-who-handles-them.md)). 2026-10-28, #PRNUM.\n"
        "- **The filters in force are shown as removable tags at every width** (DI-40): a `?space=` link and the phone's sheet would otherwise hide them; `FilterTag` from the layer (finding 8). 2026-10-28, #PRNUM.\n"
        "- **The admin's list stays cards until 1024 px** (DI-43, A7): eight columns need the width; `cardsBelow=\"lg\"`. 2026-10-28, #PRNUM.\n"
        "- **The decision is sent once, with no key** (S4)",
    ),
    (
        "entry `index.ts` (`SpaceReportsList`), read by `pages/dashboard/space/reports/DataReportsPage.tsx`, which gives each field's place:",
        "entry `index.ts` (`SpaceReportsList`, `AdminReportsList`, `AdminSpaceFilterSlot`), read by `pages/dashboard/space/reports/DataReportsPage.tsx` and `pages/dashboard/admin/DataReportsPage.tsx`, which give each field's place (`pages/dashboard/fieldSections.ts`, the editor's anchors) and, for the admin, set [space-links](space-links.md)' `AdminSpaceFilter`:",
    ),
    (
        "the owner's list and its chip in the address (`space/`), and the decision sheet's view and its write (`decide/`) in `hooks/`; the address's query (`reportsQueryOf`)",
        "the owner's list and its chip in the address (`space/`), the admin's list and its filters in the address (`admin/`), and the decision sheet's view and its write (`decide/`) in `hooks/`; the addresses' queries (`reportsQueryOf`, `adminReportsQueryOf`)",
    ),
    (
        "the owner's list (`space/`), the decision sheet (`decide/`), the status chips and the decision's toast in `components/`.",
        "the owner's list (`space/`), the admin's list, its filters and its tags (`admin/`), the decision sheet (`decide/`), the parts both lists share, the status chips and the decision's toast in `components/`.",
    ),
    (
        "- 2026-10-28, #PRNUM — «بلاغات البيانات», the owner's: the space's reports by status, the reporter a visitor and the day only, and the decision sheet.\n",
        "- 2026-10-28, #PRNUM — «بلاغات البيانات», the owner's: the space's reports by status, the reporter a visitor and the day only, and the decision sheet; the admin's: every space's reports by status, space and field, the filters in force as tags, the reporter named, a verified space's report read-only.\n",
    ),
])

edit('features/space-links.md', [
    (
        "- **The admin,** through the spaces list, on the dashboard's spaces page, the admin's routes on one space, the users list, on the dashboard's owners and users pages, and adding an owner.\n",
        "- **The admin,** through the spaces list, on the dashboard's spaces page, the admin's routes on one space, the users list, on the dashboard's owners and users pages, and adding an owner.\n"
        "- **The admin's data reports,** which filter by one space (`AdminSpaceFilter`: the spaces' search, «كل المساحات» first; [data-reports](data-reports.md), 2026-10-28, #PRNUM).\n",
    ),
])

edit('frontend/architecture.md', [
    (
        "[users](../features/users.md)' actions, the add-space page,",
        "[users](../features/users.md)' actions, «بلاغات البيانات», the admin's list of [data-reports](../features/data-reports.md) with [space-links](../features/space-links.md)' one-space search in its filters (2026-10-28, #PRNUM), the add-space page,",
    ),
])

edit('project/overview.md', [
    (
        "on the dashboard, the owner's «بلاغات البيانات» with the decision sheet.\n",
        "on the dashboard, the owner's and the admin's «بلاغات البيانات» with the decision sheet, the admin's filtered by status, space and field.\n",
    ),
])

edit('architecture/findings/README.md', [
    (
        "- [166. The ledger's staff filter cannot name a space's other owners](166-the-ledgers-staff-filter-cannot-name-a-spaces-other-owners.md)\n",
        "- [166. The ledger's staff filter cannot name a space's other owners](166-the-ledgers-staff-filter-cannot-name-a-spaces-other-owners.md)\n"
        "- [167. The admin's reports cannot be filtered by who handles them](167-the-admins-reports-cannot-be-filtered-by-who-handles-them.md)\n",
    ),
])

with open(ROOT + 'architecture/findings/167-the-admins-reports-cannot-be-filtered-by-who-handles-them.md', 'w', encoding='utf8', newline='') as handle:
    handle.write(
        "# 167. The admin's reports cannot be filtered by who handles them\n"
        "\n"
        "**Status:** Open · **Date:** 2026-10-28\n"
        "\n"
        "**Evidence:** the admin's «بلاغات البيانات» (#PRNUM) shows «يعالجه» on each report — «الإدارة» while its space is unverified, «المالك» once verified — from `AdminReport.space.verified` (DI-39). The design's filter by who handles a report (R2-AD-UX-003) has no parameter: `GET /admin/data-reports` filters by status, field and space only ([api-contract › Data reports](../../api/api-contract.md#data-reports)), so the admin cannot list only the reports the admin decides. The page offers no such filter (A8).\n"
        "\n"
        "**Resolves when:** `GET /admin/data-reports` takes a `verified` (or handled-by) filter and the admin's list offers it; or the owner accepts the per-row «يعالجه» as enough.\n"
    )
print('ok')
