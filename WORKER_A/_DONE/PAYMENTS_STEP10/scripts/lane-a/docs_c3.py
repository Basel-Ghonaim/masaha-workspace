import io

p = r'C:\dev\masaha\app-lane-a\docs\features\announcements.md'
s = io.open(p, encoding='utf8', newline='').read()
pairs = [
    ('opens it. Closed, the focus goes back to the control that opened the sheet.\n',
     'opens it. Closed, the focus goes back to the control that opened the sheet.\n\n'
     '**End now, start now and delete on the web.** Each card\'s footer holds its actions by its state: a '
     'running one «تعديل», «إنهاء الآن» and the «⋯»; an upcoming one «تعديل», «ابدأ الآن» and the «⋯»; an ended '
     'one the «⋯» alone, its card its view. The «⋯», named «إجراءات أخرى: {type} · {period}», holds «حذف…»; an '
     'extended closure has none, and its line says «مُدّدت اشتراكاته، فلا يُحذف ولا تُؤخَّر نهايته.». Each write '
     'is sent once, with no key. «إنهاء الآن» acts at once: its toast says «انتهى الإعلان» (a closure «انتهى '
     'الإغلاق · عادت الحالة تلقائية») and «في «منتهية»», with «تراجع», one `PATCH` giving back the old end — '
     'except on an extended closure, whose end may only come earlier, which offers «عرض». «ابدأ الآن» says '
     '«بدأ الإعلان الآن» and «في «نشطة»», with «عرض». A failure is an error toast with its line '
     '(`ANNOUNCEMENT_NOT_STARTED`, an end that a start would put past 365 days, a 403) and «إعادة المحاولة», '
     'which sends it once more. «حذف…» asks first, naming the announcement («حذف إعلان «{type} · {period}»؟») '
     'and the true consequence of its state now — a running closure reopens the space at once, a running one '
     'leaves the space\'s page, an upcoming one is never seen, an ended one leaves the list; none can be '
     'brought back —; a refusal stays in the dialog, `CLOSURE_EXTENDED` read again from the list. When the card '
     'whose action holds the focus leaves its tab, the next card\'s first action takes it, else the tab shown.\n'),
    ('- **The period\'s refusals on their fields, in the contract\'s words** (DI-30)',
     '- **End now, start now and delete are sent once, with no key** (S4): each is idempotent by design, so a '
     'repeat answers as it is; no answer is said with «إعادة المحاولة», never re-sent by itself. 2026-10-28, '
     '#PRNUM.\n'
     '- **An ended announcement has no «تعديل»; its card is its view** (DI-16). An action that cannot apply is '
     'left out, its reason said on the card, never a disabled menu item ([finding 105](../architecture/findings/'
     '105-a-held-menu-item-may-be-unreachable.md)). 2026-10-28, #PRNUM.\n'
     '- **The actions by state, and «تراجع» only where it can work** (DI-17): end now\'s undo restores the old '
     'end by `PATCH`, which an extended closure would refuse (`CLOSURE_EXTENDED`), so it is not offered there; '
     'an extended closure has no delete. 2026-10-28, #PRNUM.\n'
     '- **The delete names the announcement and its true consequence by state** (DI-18), with «لا يمكن '
     'استرجاعه.»: no route restores one. 2026-10-28, #PRNUM.\n'
     '- **The period\'s refusals on their fields, in the contract\'s words** (DI-30)'),
    ('the sheet and its post and edit (`sheet/`) and the writes\' shared invalidation',
     'the sheet and its post and edit (`sheet/`), a card\'s actions and the delete\'s dialog (`actions/`), the '
     'focus kept when a card leaves (`list/useCardFocus`) and the writes\' shared invalidation'),
    ('the sheet, its type and its period (`sheet/`), the public',
     'the sheet, its type and its period (`sheet/`), the «⋯» and the delete\'s dialog (`actions/`), the public'),
    ('a new announcement and its edit in a sheet, with the preview of the space\'s page.\n',
     'a new announcement and its edit in a sheet, with the preview of the space\'s page; end now with its undo, '
     'start now and delete.\n'),
]
for a, b in pairs:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
io.open(p, 'w', encoding='utf8', newline='').write(s)
print('ok')
