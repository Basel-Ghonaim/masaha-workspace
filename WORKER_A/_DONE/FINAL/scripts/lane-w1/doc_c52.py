p = r'C:\dev\masaha\app-lane-w1\docs\features\overview.md'
s = open(p, encoding='utf8', newline='').read()

def rep(old, new):
    global s
    assert s.count(old) == 1, old[:60]
    s = s.replace(old, new)

rep("The API is built; on the web, the owner's overview (screen 12).",
    "The API is built; on the web, the owner's overview (screen 12) and the admin's (screen 25).")
rep("under `/admin/overview`. The admin's screen (25) is to come, worker A's.",
    "under `/admin/overview`. On the web, «نظرة عامة» at `/dashboard/admin`, the admin's landing (2026-10-29, #PRNUM).")
rep("""Its states: three blocks while it loads; a failure, «تعذّر تحميل النظرة العامة» with «إعادة المحاولة»; offline, its own state.
""", """Its states: three blocks while it loads; a failure, «تعذّر تحميل النظرة العامة» with «إعادة المحاولة»; offline, its own state.

**The admin's screen** (`AdminOverview`, screen 25). One read, never polled, as the owner's. «ملخص المنصة», five tiles, each a link to the list it counts with its helper: the spaces (verified, unverified, hidden), the open reports (the admin's, the owners'), the stale or missing data (`?stale=true`), the unverified spaces with no owner (`?status=unverified`), and the new users of the last 30 days (the users list); two columns from 768 px, three from 1024 px, five from 1280 px. «اكتمال البيانات» lists five of the spaces the admin edits — the name in the interface's language, «غير موثّقة» and «مخفية» when hidden, a warning per missing group and per stale one with its days, «تعديل» to its editor — and «عرض الكل», with the total past five, to `?status=editable&stale=true`. Under it, the note that a space's operating data is its management's.
""")
rep("""- **Every link is the page's** (architecture §3): `OwnerOverviewLinks`. 2026-10-29, #PRNUM.
""", """- **Every link is the page's** (architecture §3): `OwnerOverviewLinks`, `AdminOverviewLinks`. 2026-10-29, #PRNUM.
- **A fifth tile, «مستخدمون جدد»** (DI7, OV4), to the users list, newest first: the list has no date filter, so it shows the list, not the 30 days. 2026-10-29, #PRNUM.
- **The stale tile names no threshold** (DI8, OV6): «حسب حدود الحداثة في إعدادات المنصة، أو لم تُضف بعد». 2026-10-29, #PRNUM.
- **A missing group is a warning, never destructive** (A8). 2026-10-29, #PRNUM.
- **«عرض الكل» leads to `?status=editable&stale=true`** (158, the owner's OD3 (a)), so the card's total equals the list it opens. 2026-10-29, #PRNUM.
""")
rep("entry `index.ts` (`OwnerOverview`, `OwnerOverviewLinks`), read by `pages/dashboard/space/overview/OverviewPage.tsx`, which passes the links and sets `occupancy`'s `LiveStatusControl` in the top bar:",
    "entry `index.ts` (`OwnerOverview`, `OwnerOverviewLinks`, `AdminOverview`, `AdminOverviewLinks`), read by `pages/dashboard/space/overview/OverviewPage.tsx`, which passes the links and sets `occupancy`'s `LiveStatusControl` in the top bar, and `pages/dashboard/admin/overview/OverviewPage.tsx`:")
rep("the keys, the query and the view (`owner/`) and the failure's view", "the keys, each screen's query and view (`owner/`, `admin/`) and the failure's view")
rep("the screen and its cards (`owner/`) and the failure", "each screen and its cards (`owner/`, `admin/`) and the failure")
rep("- 2026-10-29, #PRNUM — the owner's overview (screen 12).\n", "- 2026-10-29, #PRNUM — the owner's overview (screen 12); the admin's (screen 25).\n")
open(p, 'w', encoding='utf8', newline='').write(s)
print('ok')
