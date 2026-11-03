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
    ('whose action holds the focus leaves its tab, the next card\'s first action takes it, else the tab shown.\n',
     'whose action holds the focus leaves its tab, the next card\'s first action takes it, else the tab shown.\n\n'
     '**A closure\'s extension on the web** ([`subscriptions`](subscriptions.md)\' routes, S2). A closure\'s card '
     'says where its extension stands: «يمكن تمديد الاشتراكات بعد أن يبدأ الإغلاق.» for the owner on one not '
     'started; on one started and not extended, «يمدّد المالك الاشتراكات بعد بدء الإغلاق.» for reception and '
     '«تمديد الاشتراكات» for the owner; once extended, to both, «مُدّد {count} · {days} · {name} · {date}». '
     '«تمديد الاشتراكات» opens an alert dialog that reads the preview at each opening: how many subscriptions '
     'the extension moves now — those the closure covered and their renewals not started yet, as the server '
     'counts them —, the closure\'s Gaza days, and the days, prefilled with the proposal and typed (1–365, '
     'Arabic digits read). The typed days are sent with one `Idempotency-Key` per opening, kept across the '
     'transport\'s re-sends and «إعادة المحاولة»; a failure stays in the dialog with the days kept — '
     '`CLOSURE_ALREADY_EXTENDED` reads the list again, so the card shows the extension; '
     '`ANNOUNCEMENT_NOT_STARTED`, a 403 and no answer are worded. A closure that covered none says «لم يشمل '
     'هذا الإغلاق أي اشتراك، فلا شيء يُمدَّد.» and one extended meanwhile says so, each with «رجوع» only. Done, '
     'the whole space is read again and the toast says «مُدّدت الاشتراكات» with how many and by how many days.\n'),
    ('- **The period\'s refusals on their fields, in the contract\'s words** (DI-30)',
     '- **The extension carries one key per opening of its dialog** (S4): the typed days sent, never the '
     'proposal; a retry from the same dialog answers the first. 2026-10-28, #PRNUM.\n'
     '- **An extension that would move nothing is not offered** (S11): the preview\'s `subscriptions` 0 says so '
     'with «رجوع» only. *Why:* the server would mark the closure extended for nothing, and it could never be '
     'extended once its subscriptions are corrected. 2026-10-28, #PRNUM.\n'
     '- **A failed extension stays in its dialog, the days kept** (DI-19). 2026-10-28, #PRNUM.\n'
     '- **The count is what the extension moves, not "the active subscriptions"** (DI-20): the preview\'s, '
     'those the closure covered (any running on one of its days) and, since #128, their renewals not started; '
     'the dialog says «يشمل التمديد {n} اشتراكات.» and names both, and the days field is prefilled with the '
     'proposal, the closure\'s days under it. 2026-10-28, #PRNUM.\n'
     '- **A closure\'s card says where its extension stands, by role** (DI-28): the owner\'s line before it '
     'starts, reception\'s once it has, and the extension once applied, to both. 2026-10-28, #PRNUM.\n'
     '- **The period\'s refusals on their fields, in the contract\'s words** (DI-30)'),
    ('a card\'s actions and the delete\'s dialog (`actions/`), the',
     'a card\'s actions and the delete\'s dialog (`actions/`), the extension\'s preview, apply and dialog '
     '(`extension/`), the'),
    ('the «⋯» and the delete\'s dialog (`actions/`), the public',
     'the «⋯» and the delete\'s dialog (`actions/`), the extension\'s action and dialog (`extension/`), the '
     'public'),
    ('start now and delete.\n',
     'start now and delete; the owner\'s extension of a closure\'s subscriptions.\n'),
])

edit(r'features\subscriptions.md', [
    ('On the web, «الإعلانات» reads the managed list and its summary ([announcements](announcements.md), '
     '2026-10-28, #PRNUM).',
     'On the web, «الإعلانات» reads the managed list and its summary, and the owner extends a closure\'s '
     'subscriptions from it ([announcements](announcements.md), 2026-10-28, #PRNUM).'),
])

edit(r'project\overview.md', [
    ('on the dashboard, the owner\'s and reception\'s «الإعلانات»: the announcements by state, with their '
     'counts.\n',
     'on the dashboard, the owner\'s and reception\'s «الإعلانات»: the announcements by state, with their '
     'counts, posted and edited in a sheet with the preview of the space\'s page, ended (with an undo), '
     'started and deleted, and the owner\'s extension of a closure\'s subscriptions by the days typed, once.\n'),
])

edit(r'frontend\design-system\foundation.md', [
    ('the owner can then extend all active subscriptions by the closure days',
     'the owner can then extend the subscriptions it covered, by the days typed, once'),
])
print('ok')
