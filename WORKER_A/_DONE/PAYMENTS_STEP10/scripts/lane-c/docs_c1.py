"""Commit 1's documents."""
import sys

ROOT = r'C:\dev\masaha\app-lane-c\docs'


def edit(path, old, new):
    full = ROOT + '\\' + path
    with open(full, encoding='utf8', newline='') as f:
        text = f.read()
    if text.count(old) != 1:
        sys.exit(f'{path}: anchor found {text.count(old)} times: {old[:60]}')
    text = text.replace(old, new, 1)
    with open(full, 'w', encoding='utf8', newline='') as f:
        f.write(text)


D = 'features\\data-reports.md'
edit(D, "The API is built; on the web, the owner's «بلاغات البيانات».",
     "The API is built; on the web, the owner's «بلاغات البيانات» and a signed-in user's «بلاغاتي».")
edit(D, "any page group: the owner's list of a space's reports and the decision sheet.",
     "any page group: the owner's list of a space's reports and the decision sheet; the user's own reports.")
edit(D, "- **A signed-in user,** through the API: `POST /spaces/:slug/reports`, and their own, `GET /me/reports`. The space page's report button and the account's reports are not built.",
     "- **A signed-in user,** through the API: `POST /spaces/:slug/reports`, and their own, `GET /me/reports`. On the site, the user reads «بلاغاتي» (`/me/reports`) and the replies, linked from the account menu (2026-10-28, #PRNUM). The space page's report button is not built.")
edit(D, """Closed, the sheet gives the focus back to its «فتح», or, that row gone, to the count.
""", """Closed, the sheet gives the focus back to its «فتح», or, that row gone, to the count.

**The user's reports on the web** (`features/data-reports`, composed by `pages/site/account/MyReportsPage.tsx` in the account's layout, signed-in only). «بلاغاتي» says what it lists, then «الكل · قيد المراجعة · تمت المراجعة» — the owner's list's rule: the chip and the page in the address (`?status=open|decided&page=`), a chip back to the first page — and the count. It lists `GET /me/reports` 20 a page, newest first, a card each: the space as its heading, a link to its page while it is listed, its name as muted text once it left with «لم تعد هذه المساحة معروضة في الدليل»; «{field} · أُرسل {day}», the day on Gaza's calendar; the status as the reporter reads it («قيد المراجعة» `info`, «تم التصحيح» `success`, «لم يُعتمد» `neutral`); the message in its own direction, a message over 160 characters folded to two lines with «عرض المزيد» / «عرض أقل»; and the reply, in its own direction, labelled «ردّ إدارة المساحة» or «ردّ فريقنا» by who replied. Its states: three skeleton cards while loading, a failure with its reference and a retry, a failed refresh over the cards shown, «لم ترسل أي بلاغ بعد» with «تصفّح المساحات», and «لا توجد بلاغات هنا» under a chip.
""")
edit(D, """- **The decision is sent once, with no key** (S4): the same decision again answers the report as it is, so a lost answer is retried from the sheet. 2026-10-28, #PRNUM.
""", """- **The decision is sent once, with no key** (S4): the same decision again answers the report as it is, so a lost answer is retried from the sheet. 2026-10-28, #PRNUM.
- **«بلاغاتي»'s two empty states** (DI-53): none sent yet says how to report, with «تصفّح المساحات»; none under a chip says only that. 2026-10-28, #PRNUM.
- **A long message folds by its length, never by measuring** (DI-54): over 160 characters, two lines with «عرض المزيد» (`aria-expanded`, `aria-controls`), so the toggle is there from the first drawing. 2026-10-28, #PRNUM.
- **A chip returns «بلاغاتي» to its first page** (DI-55, S8), the owner's list's address rule reused. 2026-10-28, #PRNUM.
- **The reply is labelled by who replied** (DI-56): `repliedBy` `SPACE` «ردّ إدارة المساحة», `MASAHA` «ردّ فريقنا» — "our team", never «فريق مساحة», which reads as the space's. A space that left is named as text with its line (C7). 2026-10-28, #PRNUM.
""")
edit(D, "- **Web:** `apps/web/src/features/data-reports/`, entry `index.ts` (`SpaceReportsList`), read by `pages/dashboard/space/reports/DataReportsPage.tsx`, which gives each field's place:",
     "- **Web:** `apps/web/src/features/data-reports/`, entry `index.ts` (`SpaceReportsList`, `MyReportsList`), read by `pages/dashboard/space/reports/DataReportsPage.tsx`, which gives each field's place, and `pages/site/account/MyReportsPage.tsx`, which gives the spaces' and the directory's links:")
edit(D, "the owner's list (`space/`), the decision sheet (`decide/`), the status chips and the decision's toast in `components/`.",
     "the owner's list (`space/`), the decision sheet (`decide/`), the status chips and the decision's toast in `components/`; the user's reports, their view in `hooks/mine/`, their list and card in `components/mine/`, the card's type in `types/MyReportCardView.ts`.")
edit(D, """- 2026-10-28, #PRNUM — «بلاغات البيانات», the owner's: the space's reports by status, the reporter a visitor and the day only, and the decision sheet.
""", """- 2026-10-28, #PRNUM — «بلاغات البيانات», the owner's: the space's reports by status, the reporter a visitor and the day only, and the decision sheet.
- 2026-10-28, #PRNUM — «بلاغاتي»: a signed-in user's own reports, the replies labelled by who replied, a space that left named as text; linked from the account menu.
""")
print('ok')
