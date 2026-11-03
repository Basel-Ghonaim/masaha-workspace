"""Commit 1's documents: architecture §2, overview, foundation §13 screen 11."""
import sys

ROOT = r'C:\dev\masaha\app-lane-c\docs'


def edit(path, old, new):
    full = ROOT + '\\' + path
    with open(full, encoding='utf8', newline='') as f:
        text = f.read()
    if text.count(old) != 1:
        sys.exit(f'{path}: anchor found {text.count(old)} times: {old[:70]}')
    text = text.replace(old, new, 1)
    with open(full, 'w', encoding='utf8', newline='') as f:
        f.write(text)


A = 'frontend\\architecture.md'
edit(A, """  - Built: `RootLayout`; `SiteLayout`, with the site's header, footer and phone menu; `FocusLayout`; `DashboardLayout`, inside each of the dashboard's two branches.
  - Not built yet: `AccountLayout`, with the first account screen.""",
     """  - Built: `RootLayout`; `SiteLayout`, with the site's header, footer and phone menu; `FocusLayout`; `DashboardLayout`, inside each of the dashboard's two branches; `AccountLayout`, inside `SiteLayout`, with «بلاغاتي» (2026-10-28, #PRNUM).""")
edit(A, "the site's 404, and the pages of `auth/`; in `pages/dashboard`",
     "the site's 404, the pages of `auth/`, and in `account/` the account's layout, its navigation named «حسابي», with «بلاغاتي», the user's reports of [data-reports](../features/data-reports.md), signed-in only (2026-10-28, #PRNUM); in `pages/dashboard`")

O = 'project\\overview.md'
edit(O, "on the dashboard, the owner's «بلاغات البيانات» with the decision sheet.",
     "on the dashboard, the owner's «بلاغات البيانات» with the decision sheet; on the site, a signed-in user's «بلاغاتي» with the replies.")

F = 'frontend\\design-system\\foundation.md'
edit(F, "11. **My reports** — submitted reports, their status and the resolution note («ردّ إدارة المساحة» or «ردّ فريق مساحة»)",
     "11. **My reports** — submitted reports, their status and the resolution note («ردّ إدارة المساحة» or «ردّ فريقنا»)")
print('ok')
