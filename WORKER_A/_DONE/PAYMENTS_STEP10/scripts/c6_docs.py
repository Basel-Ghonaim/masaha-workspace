"""Commit 6's documents: announcements.md, directory.md, overview.md, finding 131 resolved."""
import io

APP = 'C:/dev/masaha/app/'


def edit(path, pairs):
    p = APP + path
    s = io.open(p, encoding='utf8', newline='').read()
    for a, b in pairs:
        assert s.count(a) == 1, (path, a[:70])
        s = s.replace(a, b)
    io.open(p, 'w', encoding='utf8', newline='').write(s)
    print('ok', path)


edit('docs/features/announcements.md', [
    ("screen 18, and the public pieces a space's page sets (PR 4).",
     "screen 18, and the public pieces a space's page sets: its running closure's notice and its other announcements."),
    ("- **[`directory`](directory.md),** whose space page reads its running and upcoming announcements.\n",
     "- **[`directory`](directory.md),** whose space page reads its running and upcoming announcements. On the site, the space's page shows them: a running closure's notice at its top, the others after its status (2026-10-28, #PRNUM).\n"),
    ("- **The preview draws the public page's own pieces on a muted surface** (DI-25): `AnnouncementItem` and `ClosureNotice`, the components the space's page will set. 2026-10-28, #PRNUM.\n",
     "- **The preview draws the public page's own pieces on a muted surface** (DI-25): `AnnouncementItem` and the closure's warning (`ClosureAlert`), the components the space's page sets. 2026-10-28, #PRNUM.\n"
     "- **A running closure is the page's top notice, never repeated in its announcements** (DI-59, U8: «the closure Alert stays at the top»): the first `CLOSURE` that has started and has no end, or ends after now (`runningClosure`), is a warning above the page with its text and «إعلان من إدارة المساحة · {period}»; the section «الإعلانات», after the status and before the prices, lists the others by their start, an upcoming closure among them, and is left out when none is left. *Why:* one closure said twice reads as two. 2026-10-28, #PRNUM.\n"),
    ("entry `index.ts` (`AnnouncementsList`), read by `pages/dashboard/space/announcements/AnnouncementsPage.tsx`, which reads the role at the space:",
     "entry `index.ts` (`AnnouncementsList`, `ClosureNotice`, `SpaceAnnouncements`), read by `pages/dashboard/space/announcements/AnnouncementsPage.tsx`, which reads the role at the space, and by `pages/site/public/space/SpacePage.tsx`, which sets the public pieces in the directory's slots:"),
    ("the writes' shared invalidation (`useAnnouncementsWrite`) in `hooks/`;",
     "the writes' shared invalidation (`useAnnouncementsWrite`), and the public page's view (`public/`) in `hooks/`;"),
    ("the sheet's requests (`sheetRequest`) in `services/`;",
     "the sheet's requests (`sheetRequest`) and the running closure (`runningClosure`) in `services/`;"),
    ("the public page's item and closure notice, not exported yet (`public/`),",
     "the public page's item, its closure's notice and its announcements' section (`public/`),"),
])
s = io.open(APP + 'docs/features/announcements.md', encoding='utf8').read()
web = s[s.index('### Web history'):]
last = [l for l in web.split('\n') if l.startswith('- ')][-1]
edit('docs/features/announcements.md', [
    (last + '\n',
     last + "\n- 2026-10-28, #PRNUM — on the site, a space's page shows its running closure's notice at its top and its other announcements after its status (finding 131).\n"),
])

edit('docs/features/directory.md', [
    ("The page's announcements are answered by the API, not shown on the site yet.\n",
     "The page shows its announcements: a running closure's notice at its top, the others after its status, both drawn by [`announcements`](announcements.md) in the page's slots.\n"),
    ("at the end of the main column (2026-10-28, #PRNUM).",
     "at the end of the main column (2026-10-28, #PRNUM). The closure's notice is built: the details carry the space's announcements, and the page sets `announcements`' notice in the `notice` slot above the page and its section in the `announcements` slot after the status, before the prices (U8, 2026-10-28, #PRNUM)."),
    ("- [131](../architecture/findings/131-the-space-page-cannot-show-a-closures-notice.md): the space page cannot show a closure's notice.\n", ""),
    ("- 2026-10-28, #PRNUM — «المفضّلة»: the user's favourites as cards, newest saved first or nearest first, and the spaces that left with «إزالة».\n",
     "- 2026-10-28, #PRNUM — «المفضّلة»: the user's favourites as cards, newest saved first or nearest first, and the spaces that left with «إزالة».\n"
     "- 2026-10-28, #PRNUM — the page's announcements: the `notice` and `announcements` slots, in U8's order (finding 131).\n"),
])

edit('docs/project/overview.md', [
    ("and the owner's extension of a closure's subscriptions by the days typed, once.",
     "and the owner's extension of a closure's subscriptions by the days typed, once; on the site, a space's page's running closure at its top and its other announcements after its status."),
])

edit('docs/architecture/findings/131-the-space-page-cannot-show-a-closures-notice.md', [
    ("**Status:** Open · **Date:** 2026-10-22", "**Status:** Resolved · **Date:** 2026-10-22"),
])
p = APP + 'docs/architecture/findings/131-the-space-page-cannot-show-a-closures-notice.md'
s = io.open(p, encoding='utf8', newline='').read().rstrip('\n')
s += ("\n\n**Resolution (2026-10-28, #PRNUM):** the space's page shows its running and upcoming announcements"
      " and a running closure's notice at the top: `GET /spaces/:slug` carries them since #112, and the page"
      " sets `announcements`' warning above its sections (a closure that has started and has not ended) and its"
      " section «الإعلانات» after the status, before the prices, the running closure not repeated there (U8,"
      " DI-59).\n")
io.open(p, 'w', encoding='utf8', newline='').write(s)
print('ok 131')
