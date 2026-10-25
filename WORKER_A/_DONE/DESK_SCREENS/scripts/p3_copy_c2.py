import io
AR = """  /** «ملف الزبون»: a customer's file (screen 15). */
  file: {
    title: 'ملف الزبون',
    breadcrumb: 'مسار التنقّل',
    notFound: { title: 'لم نجد هذا الزبون', text: 'ربما ليس من زبائن هذه المساحة.' },
    balance: 'الرصيد',
    archived: 'مؤرشف',
    here: 'حاضر الآن',
    loadFailed: 'تعذّر تحميل ملف الزبون',
    unpaid: { title: 'زيارات غير مدفوعة', unpriced: 'بدون سعر بعد' },
    subscriptions: {
      title: 'الاشتراكات',
      none: 'لا توجد اشتراكات',
      onlyVisits: 'هذا الزبون يأتي بزيارات فقط.',
    },
    card: {
      dates: ({ from, to }: { from: string; to: string }) => `${from} – ${to}`,
      typed: 'سعر يدوي',
      terms: {
        totalDays: ({ count }: { count: number }) =>
          arabicPlural(count, {
            zero: `${String(count)} يوم`,
            one: 'يوم واحد',
            two: 'يومان',
            few: `${String(count)} أيام`,
            many: `${String(count)} يومًا`,
            other: `${String(count)} يوم`,
          }),
        daysPerWeek: ({ count }: { count: number }) => `${String(count)} بالأسبوع`,
        hoursPerDay: ({ count }: { count: number }) => `${String(count)} س باليوم`,
        totalHours: ({ count }: { count: number }) => `${String(count)} س إجمالًا`,
        student: 'للطلاب',
        none: 'بدون شروط إضافية',
      },
      due: 'المستحق',
      dueSoFar: 'المستحق حتى الآن',
      paid: 'المدفوع',
      left: 'المتبقي',
      pay: { paid: 'مدفوع', partial: 'مدفوع جزئيًا', unpaid: 'غير مدفوع' },
      receiveLeft: 'استلام المتبقي',
    },
  },
"""
EN = """  /** «ملف الزبون»: a customer's file (screen 15). */
  file: {
    title: 'Customer file',
    breadcrumb: 'Breadcrumb',
    notFound: {
      title: 'We couldn’t find this customer',
      text: 'They may not be a customer of this space.',
    },
    balance: 'Balance',
    archived: 'Archived',
    here: 'Here now',
    loadFailed: 'We couldn’t load the customer’s file',
    unpaid: { title: 'Unpaid visits', unpriced: 'Not priced yet' },
    subscriptions: {
      title: 'Subscriptions',
      none: 'No subscriptions',
      onlyVisits: 'This customer only comes for visits.',
    },
    card: {
      dates: ({ from, to }: { from: string; to: string }) => `${from} – ${to}`,
      typed: 'Typed price',
      terms: {
        totalDays: ({ count }: { count: number }) =>
          englishPlural(count, { one: '1 day', other: `${String(count)} days` }),
        daysPerWeek: ({ count }: { count: number }) => `${String(count)} a week`,
        hoursPerDay: ({ count }: { count: number }) => `${String(count)} h a day`,
        totalHours: ({ count }: { count: number }) => `${String(count)} h in all`,
        student: 'Students',
        none: 'No extra terms',
      },
      due: 'Due',
      dueSoFar: 'Due so far',
      paid: 'Paid',
      left: 'Left',
      pay: { paid: 'Paid', partial: 'Partly paid', unpaid: 'Unpaid' },
      receiveLeft: 'Receive what’s left',
    },
  },
"""
def ins(path, block, end):
    s = io.open(path, encoding='utf-8', newline='').read()
    assert s.count(end) == 1
    s = s.replace(end, block + end)
    io.open(path, 'w', encoding='utf-8', newline='').write(s)
ins('arabic/desk.ts', AR, "} satisfies Catalogue['desk'];")
ins('english/desk.ts', EN, "} as const;")
