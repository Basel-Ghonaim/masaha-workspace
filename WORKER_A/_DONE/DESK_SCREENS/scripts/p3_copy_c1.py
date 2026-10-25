import io
AR = """  /** «الزبائن»: the space's customers, searched and filtered (S11). */
  customers: {
    label: 'زبائن المساحة',
    columns: {
      name: 'الاسم',
      subscription: 'الاشتراك',
      status: 'الحالة',
      balance: 'الرصيد',
      actions: 'إجراءات',
    },
    status: { label: 'تصفية حسب الحالة', all: 'الكل', ARCHIVED: 'مؤرشف' },
    kind: {
      label: 'نوع الاشتراك',
      options: {
        all: 'كل الأنواع',
        PACKAGE: 'باقة',
        CUSTOM: 'مخصّص',
        NONE: 'بدون اشتراك',
      },
    },
    payment: {
      label: 'الدفع',
      options: {
        all: 'كل حالات الدفع',
        OWES: 'عليه دين',
        CREDIT: 'له رصيد',
        SETTLED: 'مسدّد',
      },
    },
    filters: {
      title: 'الفلاتر',
      applied: ({ count }: { count: number }) =>
        arabicPlural(count, {
          zero: 'لا فلاتر مطبّقة',
          one: 'فلتر واحد مطبّق',
          two: 'فلتران مطبّقان',
          few: `${String(count)} فلاتر مطبّقة`,
          many: `${String(count)} فلترًا مطبّقًا`,
          other: `${String(count)} فلتر مطبّق`,
        }),
      show: ({ count }: { count: number }) =>
        arabicPlural(count, {
          zero: `عرض ${String(count)} زبون`,
          one: 'عرض الزبون',
          two: 'عرض الزبونين',
          few: `عرض ${String(count)} زبائن`,
          many: `عرض ${String(count)} زبونًا`,
          other: `عرض ${String(count)} زبون`,
        }),
      clear: 'مسح الفلاتر',
      close: 'إغلاق',
    },
    count: ({ count }: { count: number }) =>
      arabicPlural(count, {
        zero: 'لا زبائن',
        one: 'زبون واحد',
        two: 'زبونان',
        few: `${String(count)} زبائن`,
        many: `${String(count)} زبونًا`,
        other: `${String(count)} زبون`,
      }),
    empty: {
      title: 'لا يوجد زبائن بعد',
      text: 'يُضاف الزبون عند أول اشتراك، أو عندما يخرج زائر بدون دفع.',
    },
    noMatch: {
      title: 'لا يوجد زبائن يطابقون البحث',
      text: 'جرّب اسمًا أو رقمًا آخر، أو غيّر الفلاتر.',
    },
    archivedEmpty: 'لا يوجد زبائن مؤرشفون',
    loadFailed: 'تعذّر تحميل الزبائن',
    pagination: {
      label: 'صفحات الزبائن',
      previous: 'السابق',
      next: 'التالي',
      page: ({ page }: { page: number }) => `الصفحة ${String(page)}`,
      summary: ({ page, total }: { page: number; total: number }) =>
        `الصفحة ${String(page)} من ${String(total)}`,
      more: 'صفحات أخرى',
    },
  },
"""
EN = """  /** «الزبائن»: the space's customers, searched and filtered (S11). */
  customers: {
    label: 'The space’s customers',
    columns: {
      name: 'Name',
      subscription: 'Subscription',
      status: 'Status',
      balance: 'Balance',
      actions: 'Actions',
    },
    status: { label: 'Filter by status', all: 'All', ARCHIVED: 'Archived' },
    kind: {
      label: 'Subscription type',
      options: {
        all: 'All types',
        PACKAGE: 'Package',
        CUSTOM: 'Custom',
        NONE: 'No subscription',
      },
    },
    payment: {
      label: 'Payment',
      options: {
        all: 'All payment states',
        OWES: 'Owes money',
        CREDIT: 'In credit',
        SETTLED: 'Settled',
      },
    },
    filters: {
      title: 'Filters',
      applied: ({ count }: { count: number }) =>
        englishPlural(count, { one: '1 filter applied', other: `${String(count)} filters applied` }),
      show: ({ count }: { count: number }) =>
        englishPlural(count, { one: 'Show 1 customer', other: `Show ${String(count)} customers` }),
      clear: 'Clear filters',
      close: 'Close',
    },
    count: ({ count }: { count: number }) =>
      englishPlural(count, { one: '1 customer', other: `${String(count)} customers` }),
    empty: {
      title: 'No customers yet',
      text: 'A customer is added with their first subscription, or when a visitor leaves without paying.',
    },
    noMatch: {
      title: 'No customers match',
      text: 'Try another name or number, or change the filters.',
    },
    archivedEmpty: 'No archived customers',
    loadFailed: 'We couldn’t load the customers',
    pagination: {
      label: 'Pages of customers',
      previous: 'Previous',
      next: 'Next',
      page: ({ page }: { page: number }) => `Page ${String(page)}`,
      summary: ({ page, total }: { page: number; total: number }) =>
        `Page ${String(page)} of ${String(total)}`,
      more: 'More pages',
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
