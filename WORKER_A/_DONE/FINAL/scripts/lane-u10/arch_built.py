import sys
p = r'C:\dev\masaha\app-lane-u10\docs\frontend\architecture.md'
s = open(p, encoding='utf8', newline='').read()
reps = [
 ("«بلاغاتي», the user's reports of [data-reports](../features/data-reports.md), each signed-in only (2026-10-28, #129);",
  "«بلاغاتي», the user's reports of [data-reports](../features/data-reports.md), each signed-in only (2026-10-28, #129), and «إعدادات حسابي» at `/me`, one's own settings of [users](../features/users.md) (2026-10-29, #PRNUM);"),
 ("and in `admin/` the lookups page ([lookups](../features/lookups.md)),",
  "and in `admin/` «نظرة عامة», the admin's landing of [overview](../features/overview.md), the lookups page ([lookups](../features/lookups.md)),"),
 ("their paths are in `navigation.ts` but not in the sidebar; and in `space/`",
  "their paths are in `navigation.ts` but not in the sidebar; «سجل التدقيق», the platform's log of [audit](../features/audit.md), and «إعدادات المنصة», the cards of [platform-settings](../features/platform-settings.md) (2026-10-29, #PRNUM); and in `space/` «نظرة عامة», the owner's landing of [overview](../features/overview.md) (2026-10-29, #PRNUM),"),
 ("after the attendance card the page composes from them and [occupancy](../features/occupancy.md)'s capacity,",
  "after the attendance card the page composes from them and [occupancy](../features/occupancy.md)'s capacity, then its account card, «حسابي», leading to `/me` (2026-10-29, #PRNUM),"),
 ("with [desk](../features/desk.md)'s check-out in each row and its visit's check-in (2026-10-24, #116),",
  "with [desk](../features/desk.md)'s check-out in each row and its visit's check-in (2026-10-24, #116), and desk's «السجل» and the owner's «لن تُحصَّل» (2026-10-29, #PRNUM),"),
 ("«تعديل الحقل» leading to Packages & prices or the space profile (2026-10-28, #129), each space page",
  "«تعديل الحقل» leading to Packages & prices or the space profile (2026-10-28, #129), «المالية والتقارير», the owner's tabs of [finance](../features/finance.md), and «سجل التدقيق», the space's log of [audit](../features/audit.md), in «الفريق والإعدادات» (2026-10-29, #PRNUM), each space page"),
 (" each space page with a screen loaded lazily from the routes' own map. The dashboard's other screens (the rest of `admin/` and of `space/`) and the account's settings (screen 9) are not built yet.\n",
  " each space page with a screen loaded lazily from the routes' own map. Every screen of v1 is built (2026-10-29, #PRNUM).\n"),
 ("; the rest of the layout tree is not yet. What each capability built",
  ". What each capability built"),
]
for a, b in reps:
    n = s.count(a)
    if n != 1:
        sys.exit('count %d: %s' % (n, a[:70]))
    s = s.replace(a, b)
open(p, 'w', encoding='utf8', newline='').write(s)
print('ok')
