import io

ROOT = r'C:\dev\masaha\app-lane-a\docs'


def edit(path, pairs):
    p = ROOT + '\\' + path
    s = io.open(p, encoding='utf8', newline='').read()
    for old, new in pairs:
        assert s.count(old) == 1, (path, old[:60])
        s = s.replace(old, new)
    io.open(p, 'w', encoding='utf8', newline='').write(s)


edit(r'features\announcements.md', [
    ('**Last Updated:** 2026-10-26', '**Last Updated:** 2026-10-28'),
    ('The API is built; no screen yet.',
     'The API is built; on the dashboard, the owner\'s and reception\'s «الإعلانات».'),
    ('> **Scope:** the API module `announcements` (L2); `@masaha/shared/announcements`.',
     '> **Scope:** the API module `announcements` (L2); `@masaha/shared/announcements`; the web feature '
     '`features/announcements`, any page group: screen 18, and the public pieces a space\'s page sets '
     '(PR 4).'),
    ('they post, edit, end, start and delete. The screens are not built.',
     'they post, edit, end, start and delete. On the dashboard, both read «الإعلانات» '
     '(`/dashboard/spaces/:spaceId/announcements`, 2026-10-28, #PRNUM).'),
    ('**An extended closure.** Once its subscriptions were extended',
     '**The announcements on the web** (`features/announcements`, composed by '
     '`pages/dashboard/space/announcements/`). «الإعلانات», the owner\'s and reception\'s, reads the managed '
     'list and its summary (S2): the tabs «نشطة · مجدولة · منتهية», each with the summary\'s count (a skeleton '
     'while it loads), the tab and the page in the address (`?state=upcoming|ended&page=`, running not written; '
     'a value the server would refuse falls back to running, a change replaces the address and returns to page '
     '1). Each announcement of the tab is a card, in the server\'s order: its type as its heading\'s badge — '
     '`warning` for an outage or a closure, `neutral` otherwise —, its period on Gaza\'s clock («1 أكتوبر '
     '08:00–18:00», «1 أكتوبر 08:00 – 3 أكتوبر 18:00», «من 1 أكتوبر 08:00 · بلا نهاية», the year when it is '
     'not this one), its text in the interface\'s language — the Arabic, marked as Arabic, when an English one '
     'is missing — and a closure\'s line: «يمكن تمديد الاشتراكات بعد أن يبدأ الإغلاق.» for the owner on one not '
     'started, «يمدّد المالك الاشتراكات بعد بدء الإغلاق.» for reception on one started and not extended. No '
     'status badge: the tab says it. Its states: three skeleton cards while it loads, the list marked busy; a '
     'failure with its reference and a retry; a failed refresh over the cards shown; each tab\'s empty state; '
     'the pages only past one page.\n\n'
     '**An extended closure.** Once its subscriptions were extended'),
    ('- **No title and no author on an announcement** (O9). *Why:* the design shows neither; the audit '
     'records who. 2026-10-24, #112.\n',
     '- **No title and no author on an announcement** (O9). *Why:* the design shows neither; the audit '
     'records who. 2026-10-24, #112.\n\n'
     '### Web decisions\n\n'
     '- **One web feature holds screen 18** (S2): `announcements` calls this module\'s writes and the managed '
     'list, its summary and a closure\'s extension that [`subscriptions`](subscriptions.md) composes at the same '
     'path, the contract\'s one section — an exception to "names match the backend" '
     '([architecture §3](../frontend/architecture.md#3-capabilities-features)). *Why:* one audience, the staff, '
     'works them on one screen; a `subscriptions` feature for one dialog would put a cross-feature dialog in the '
     'page. 2026-10-28, #PRNUM.\n'
     '- **The tab and the page in the address** (S8): `?state=upcoming|ended&page=`, running not written; a '
     'value the server would refuse falls back; a change replaces the address and returns to page 1. '
     '2026-10-28, #PRNUM.\n'
     '- **No status badge on a card; the type\'s badge only** (DI-15): `warning` for an outage or a closure, '
     '`neutral` otherwise (OW-014). *Why:* the tab already says the state. 2026-10-28, #PRNUM.\n'
     '- **A loading state of three skeleton cards, the counts as skeletons** (DI-23), the list `aria-busy`. '
     '2026-10-28, #PRNUM.\n'
     '- **The pages show only past one page** (DI-26): the tab already counts. 2026-10-28, #PRNUM.\n'
     '- **An English text missing shows the Arabic, marked** `lang="ar" dir="rtl"` (DI-27). 2026-10-28, '
     '#PRNUM.\n'),
    ('- `packages/shared/src/announcements/` — the requests and answers.\n',
     '- `packages/shared/src/announcements/` — the requests and answers.\n'
     '- **Web:** `apps/web/src/features/announcements/`, entry `index.ts` (`AnnouncementsList`), read by '
     '`pages/dashboard/space/announcements/AnnouncementsPage.tsx`, which reads the role at the space: the '
     'repository in `repository/`; the keys and the list\'s tab in the address and its view (`list/`) in '
     '`hooks/`; the address\'s query (`announcementsQueryOf`), the period\'s words (`periodText`), a type\'s '
     '(`typeView`) and the text in the interface\'s language (`textOf`) in `services/`; the list, its card and a '
     'closure\'s line (`list/`) in `components/`. Words: the catalogue\'s `announcements` section; the refusals '
     'are `errors`\'.\n'),
    ('- 2026-10-26, #123 — an extended closure guarded by the database (`CLOSURE_EXTENDED`).\n',
     '- 2026-10-26, #123 — an extended closure guarded by the database (`CLOSURE_EXTENDED`).\n\n'
     '### Web history\n\n'
     '- #PRNUM — «الإعلانات», the owner\'s and reception\'s: the announcements by state, with their counts.\n'),
])

edit(r'features\subscriptions.md', [
    ('**Last Updated:** 2026-10-27', '**Last Updated:** 2026-10-28'),
    ('- **The space\'s staff**, who read the managed announcements list and its summary through it, and a '
     'closure\'s extension\'s preview; **the owner**, who extends a closure\'s subscriptions.\n',
     '- **The space\'s staff**, who read the managed announcements list and its summary through it, and a '
     'closure\'s extension\'s preview; **the owner**, who extends a closure\'s subscriptions. On the web, '
     '«الإعلانات» reads the managed list and its summary ([announcements](announcements.md), 2026-10-28, '
     '#PRNUM).\n'),
])

edit(r'frontend\architecture.md', [
    ('each of those capabilities gets a web feature of its own only with a screen of its own (step 9\'s '
     'payments) (S1, 2026-10-24, #116).',
     'each of those capabilities gets a web feature of its own only with a screen of its own (step 9\'s '
     'payments) (S1, 2026-10-24, #116). **`announcements`** holds screen 18: the announcements module\'s writes '
     'and the managed list, its summary and a closure\'s extension that `subscriptions` composes at the same '
     'path, the contract\'s one section (S2, 2026-10-28, #PRNUM).'),
    ('and «دفعاتي اليوم», reception\'s own payments of today with the handover\'s figures (2026-10-27, #127),',
     'and «دفعاتي اليوم», reception\'s own payments of today with the handover\'s figures (2026-10-27, #127), '
     '«الإعلانات», the owner\'s and reception\'s announcements of [announcements](../features/announcements.md) '
     'by state (2026-10-28, #PRNUM),'),
])

edit(r'project\overview.md', [
    ('after a closure, the owner\'s extension of the subscriptions it covered, previewed first, once per '
     'closure.\n',
     'after a closure, the owner\'s extension of the subscriptions it covered, previewed first, once per '
     'closure; on the dashboard, the owner\'s and reception\'s «الإعلانات»: the announcements by state, with '
     'their counts.\n'),
])
print('ok')
