import io
AR = """  /** A subscription's statement, opened in its card (DI-43). */
  statement: {
    show: 'عرض الكشف',
    hide: 'إخفاء الكشف',
    loadFailed: 'تعذّر تحميل الكشف',
    checkIns: 'الحضور',
    columns: { day: 'اليوم', in: 'الدخول', out: 'الخروج', duration: 'المدة' },
    here: 'حاضر الآن',
    auto: 'خروج تلقائي',
    noCheckIns: 'لا حضور بعد.',
    payments: 'الدفعات',
    noPayments: 'لا دفعات بعد.',
    voided: 'ملغاة',
    voidedReason: ({ reason }: { reason: string }) => `أُلغيت: ${reason}`,
    renewal: ({ date }: { date: string }) => `التجديد يبدأ في ${date}`,
  },
  /** Ending a subscription early. */
  end: {
    action: 'إنهاء الاشتراك',
    title: 'إنهاء الاشتراك اليوم؟',
    text: ({ name, end }: { name: string; end: string }) =>
      `${name} · يصبح تاريخ النهاية ${end}. المبالغ المدفوعة والمستحقة لا تتغيّر.`,
    textWas: ({ name, end, was }: { name: string; end: string; was: string }) =>
      `${name} · يصبح تاريخ النهاية ${end} بدل ${was}. المبالغ المدفوعة والمستحقة لا تتغيّر.`,
    confirm: 'إنهاء الاشتراك',
    back: 'رجوع',
    done: ({ name }: { name: string }) => `انتهى الاشتراك «${name}» اليوم`,
    failed: 'تعذّر إنهاء الاشتراك',
  },
"""
EN = """  /** A subscription's statement, opened in its card (DI-43). */
  statement: {
    show: 'Show the statement',
    hide: 'Hide the statement',
    loadFailed: 'We couldn’t load the statement',
    checkIns: 'Attendance',
    columns: { day: 'Day', in: 'In', out: 'Out', duration: 'Duration' },
    here: 'Here now',
    auto: 'Auto check-out',
    noCheckIns: 'No attendance yet.',
    payments: 'Payments',
    noPayments: 'No payments yet.',
    voided: 'Voided',
    voidedReason: ({ reason }: { reason: string }) => `Voided: ${reason}`,
    renewal: ({ date }: { date: string }) => `A renewal would start on ${date}`,
  },
  /** Ending a subscription early. */
  end: {
    action: 'End subscription',
    title: 'End the subscription today?',
    text: ({ name, end }: { name: string; end: string }) =>
      `${name} · The end date becomes ${end}. Amounts paid and due don’t change.`,
    textWas: ({ name, end, was }: { name: string; end: string; was: string }) =>
      `${name} · The end date becomes ${end} instead of ${was}. Amounts paid and due don’t change.`,
    confirm: 'End subscription',
    back: 'Back',
    done: ({ name }: { name: string }) => `“${name}” ended today`,
    failed: 'We couldn’t end the subscription',
  },
"""
def rep(path, old, new):
    s = io.open(path, encoding='utf-8', newline='').read()
    assert s.count(old) == 1, (path, s.count(old))
    io.open(path, 'w', encoding='utf-8', newline='').write(s.replace(old, new))
rep('arabic/desk.ts', "} satisfies Catalogue['desk'];", AR + "} satisfies Catalogue['desk'];")
rep('english/desk.ts', "} as const;", EN + "} as const;")
