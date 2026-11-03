import io

BASE = r'C:\dev\masaha\app-lane-a\apps\web\src\shared\copy'

EDITS = {
    'english': [
        ("""    upcoming: 'Subscriptions can be extended once the closure has started.',
    reception: 'The owner extends subscriptions once the closure has started.',
""", """    upcoming: 'Subscriptions can be extended once the closure has started.',
    reception: 'The owner extends subscriptions once the closure has started.',
    extendedLock: 'Its subscriptions were extended, so it isn’t deleted and its end isn’t moved later.',
"""),
        ("""    new: 'New announcement',
    edit: 'Edit',
  },
""", """    new: 'New announcement',
    edit: 'Edit',
    end: 'End now',
    start: 'Start now',
    more: ({ type, period }: { type: string; period: string }) =>
      `More actions: ${type} · ${period}`,
    delete: 'Delete…',
    ended: 'The announcement has ended',
    closureEnded: 'The closure has ended · the status is automatic again',
    started: 'The announcement has started',
    undo: 'Undo',
    undone: 'The announcement is back as it was',
    undoFailed: 'We couldn’t undo it',
    failed: 'We couldn’t do that',
    startTooLong: 'Its end is more than 365 days from now; edit it first.',
  },
  /** The delete's dialog: it names the announcement and says what deleting it does now. */
  delete: {
    title: ({ type, period }: { type: string; period: string }) =>
      `Delete the announcement “${type} · ${period}”?`,
    runningClosure:
      'It leaves the space’s page, and the status is automatic again at once. It can’t be brought back.',
    running: 'It leaves the space’s page at once. It can’t be brought back.',
    upcoming: 'Visitors won’t see it. It can’t be brought back.',
    ended: 'It leaves this list. It can’t be brought back.',
    confirm: 'Delete',
    back: 'Back',
    done: 'Announcement deleted',
    failed: 'We couldn’t delete the announcement',
  },
"""),
    ],
    'arabic': [
        ("""    upcoming: 'يمكن تمديد الاشتراكات بعد أن يبدأ الإغلاق.',
    reception: 'يمدّد المالك الاشتراكات بعد بدء الإغلاق.',
""", """    upcoming: 'يمكن تمديد الاشتراكات بعد أن يبدأ الإغلاق.',
    reception: 'يمدّد المالك الاشتراكات بعد بدء الإغلاق.',
    extendedLock: 'مُدّدت اشتراكاته، فلا يُحذف ولا تُؤخَّر نهايته.',
"""),
        ("""    new: 'إعلان جديد',
    edit: 'تعديل',
  },
""", """    new: 'إعلان جديد',
    edit: 'تعديل',
    end: 'إنهاء الآن',
    start: 'ابدأ الآن',
    more: ({ type, period }: { type: string; period: string }) =>
      `إجراءات أخرى: ${type} · ${period}`,
    delete: 'حذف…',
    ended: 'انتهى الإعلان',
    closureEnded: 'انتهى الإغلاق · عادت الحالة تلقائية',
    started: 'بدأ الإعلان الآن',
    undo: 'تراجع',
    undone: 'أُعيد الإعلان كما كان',
    undoFailed: 'تعذّر التراجع',
    failed: 'تعذّر تنفيذ الإجراء',
    startTooLong: 'نهايته بعد أكثر من 365 يومًا من الآن؛ عدّلها أولًا.',
  },
  delete: {
    title: ({ type, period }: { type: string; period: string }) =>
      `حذف إعلان «${type} · ${period}»؟`,
    runningClosure: 'يختفي من صفحة المساحة، وتعود حالتها تلقائية فورًا. لا يمكن استرجاعه.',
    running: 'يختفي من صفحة المساحة فورًا. لا يمكن استرجاعه.',
    upcoming: 'لن يظهر للزوار. لا يمكن استرجاعه.',
    ended: 'يُحذف من القائمة. لا يمكن استرجاعه.',
    confirm: 'حذف',
    back: 'رجوع',
    done: 'حُذف الإعلان',
    failed: 'تعذّر حذف الإعلان',
  },
"""),
    ],
}

for name, pairs in EDITS.items():
    p = BASE + '\\' + name + '\\announcements.ts'
    s = io.open(p, encoding='utf8', newline='').read()
    for a, b in pairs:
        assert s.count(a) == 1, (name, a[:50])
        s = s.replace(a, b)
    io.open(p, 'w', encoding='utf8', newline='').write(s)
print('ok')
