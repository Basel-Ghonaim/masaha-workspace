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
    ('each tab\'s empty state; the pages only past one page.\n',
     'each tab\'s empty state; the pages only past one page.\n\n'
     '**The sheet on the web** (`AnnouncementSheet`). «إعلان جديد», at the end of the tabs\' row and in an empty '
     'tab, and «تعديل», on a running or upcoming card, open the end sheet, full width on a phone, its first '
     'focus on the checked type\'s radio: the type with what it does; the Arabic text, required; the English '
     'one, «اختياري»; «يبدأ: الآن · في موعد» (a new one only: an edit moves the start by its date and time) and '
     '«ينتهي: في موعد · بلا موعد», each date on a calendar («29 سبتمبر 2026») and its time, on Gaza\'s clock and '
     'sent as its instant, never the browser\'s; a closure\'s line, «تظهر المساحة «مغلق الآن» للزوار طوال هذه '
     'الفترة، ويُنبَّه الاستقبال عند تسجيل الحضور.»; the preview of the space\'s page, drawn by the page\'s own '
     'pieces (an item, or a closure\'s notice). The post carries one `Idempotency-Key` per opening of the sheet, '
     'kept across the transport\'s re-sends, a second press and «إعادة المحاولة»; no answer says «لم يصل الرد. '
     'أعد المحاولة — لن يُنشر مرتين.». An edit sends only what changed, once and with no key (`textEn: null` for '
     'an English text cleared, `endsAt: null` for «بلا موعد»); one that changed nothing says «لم يتغيّر شيء» and '
     'sends nothing. The server\'s period refusals land on their time fields; `CLOSURE_EXTENDED`, a 404 and a '
     '403 are worded, a 404 or a 409 reads the list again, a 404 or a 403 with no code the user\'s spaces. Done, '
     'the whole space is read again and the toast names the tab the announcement went to, with «عرض», which '
     'opens it. Closed, the focus goes back to the control that opened the sheet.\n'),
    ('- **An English text missing shows the Arabic, marked** `lang="ar" dir="rtl"` (DI-27). 2026-10-28, '
     '#PRNUM.\n',
     '- **An English text missing shows the Arabic, marked** `lang="ar" dir="rtl"` (DI-27). 2026-10-28, '
     '#PRNUM.\n'
     '- **The post carries one key per opening of the sheet** (S4): kept across the transport\'s re-sends, a '
     'second press, «إعادة المحاولة» and an edit of the form; a new opening is a new intent. An edit is '
     'idempotent by design: sent once, with no key. 2026-10-28, #PRNUM.\n'
     '- **Gaza\'s clock for every date and time** (S9): the sheet\'s date and time are Gaza\'s wall clock, sent '
     'as `gazaInstant(date, minute)`; a loaded instant is shown by `gazaClockOf`. 2026-10-28, #PRNUM.\n'
     '- **Every write reads the whole space again** (S12): a closure written, ended, started or deleted changes '
     'the space\'s state now, and an extension moves subscriptions\' ends. 2026-10-28, #PRNUM.\n'
     '- **The sheet\'s first focus is the checked type\'s radio** (DI-21), placed by the sheet itself, with the '
     'layer\'s ring. 2026-10-28, #PRNUM.\n'
     '- **The date over the time below 640 px, the date\'s trigger with the short month and the year** '
     '(DI-22). 2026-10-28, #PRNUM.\n'
     '- **Each write\'s toast names the tab it went to, with «عرض»** (DI-24): an announcement that moves tab is '
     'never lost from sight. 2026-10-28, #PRNUM.\n'
     '- **The preview draws the public page\'s own pieces on a muted surface** (DI-25): `AnnouncementItem` and '
     '`ClosureNotice`, the components the space\'s page will set. 2026-10-28, #PRNUM.\n'
     '- **A closure\'s consequence said in the sheet** (DI-29), as a warning. 2026-10-28, #PRNUM.\n'
     '- **The period\'s refusals on their fields, in the contract\'s words** (DI-30): «البداية بين 30 يومًا مضت '
     'و365 يومًا قادمة.», «النهاية بعد الآن، وبعد البداية، وخلال 365 يومًا منها.». 2026-10-28, #PRNUM.\n'),
    ('the repository in `repository/`; the keys and the list\'s tab in the address and its view (`list/`) in '
     '`hooks/`; the address\'s query (`announcementsQueryOf`), the period\'s words (`periodText`), a type\'s '
     '(`typeView`) and the text in the interface\'s language (`textOf`) in `services/`; the list, its card and a '
     'closure\'s line (`list/`) in `components/`.',
     'the repository in `repository/`; the keys, the list\'s tab in the address and its view (`list/`), the '
     'sheet and its post and edit (`sheet/`) and the writes\' shared invalidation (`useAnnouncementsWrite`) in '
     '`hooks/`; the address\'s query (`announcementsQueryOf`), the period\'s words (`periodText`), a type\'s '
     '(`typeView`), the text in the interface\'s language (`textOf`) and the sheet\'s requests '
     '(`sheetRequest`) in `services/`; the list, its card and a closure\'s line (`list/`), the sheet, its type '
     'and its period (`sheet/`), the public page\'s item and closure notice, not exported yet (`public/`), and '
     'the toasts (`toast/`) in `components/`.'),
    ('- #PRNUM — «الإعلانات», the owner\'s and reception\'s: the announcements by state, with their counts.\n',
     '- #PRNUM — «الإعلانات», the owner\'s and reception\'s: the announcements by state, with their counts; a new '
     'announcement and its edit in a sheet, with the preview of the space\'s page.\n'),
])

edit(r'frontend\architecture.md', [
    ('`desk`\'s operations span several capabilities, so they invalidate the whole `[\'space\', spaceId]` '
     'prefix, without importing the other features.',
     '`desk`\'s operations span several capabilities, so they invalidate the whole `[\'space\', spaceId]` '
     'prefix, without importing the other features. So do `announcements`\' writes (a closure changes the state '
     'now and an extension the subscriptions) (2026-10-28, #PRNUM).'),
])
print('ok')
