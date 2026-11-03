EN = r'C:\dev\masaha\app-lane-w1\apps\web\src\shared\copy\english\finance.ts'
AR = r'C:\dev\masaha\app-lane-w1\apps\web\src\shared\copy\arabic\finance.ts'

en_block = r"""  /** Who owes, who is in credit, and who paid in the month (D5.4). */
  debts: {
    tiles: {
      owed: 'Total owed',
      credit: 'Customer credit',
      creditHelper: ({ customers }: { customers: string }) => `${customers} paid in advance`,
      paid: ({ month }: { month: string }) => `Paid in ${month}`,
      uncollected: 'Uncollected visits',
      uncollectedHelper: ({ amount }: { amount: string }) => `${amount} · never added to the debts`,
      unpriced: ({ count }: { count: number }) => ` · ${String(count)} with no price`,
    },
    customers: ({ count }: { count: number }) =>
      englishPlural(count, {
        one: `${String(count)} customer`,
        other: `${String(count)} customers`,
      }),
    visits: ({ count }: { count: number }) =>
      englishPlural(count, { one: `${String(count)} visit`, other: `${String(count)} visits` }),
    owes: {
      title: 'Customers who owe',
      description: 'Largest first',
      archived: 'Archived',
      since: ({ date, item }: { date: string; item: string }) =>
        `Since ${date} · oldest item: ${item}`,
      items: { VISIT: 'Visit', SUBSCRIPTION: 'Subscription' },
      amount: ({ amount }: { amount: string }) => `Owes ${amount}`,
      whatsapp: 'WhatsApp reminder',
      receive: 'Receive payment',
      empty: 'No one owes anything',
      pages: 'Pages of customers who owe',
    },
    credit: {
      title: 'In credit',
      description: 'Paid in advance beyond their use',
      amount: ({ amount }: { amount: string }) => `In credit ${amount}`,
      none: 'No one is in credit.',
      pages: 'Pages of customers in credit',
    },
    payers: {
      line: ({ paid, date }: { paid: string; date: string }) => `${paid} · last paid ${date}`,
      viewAll: 'View all',
      none: 'No one paid this month.',
    },
    csv: {
      name: 'Name',
      phone: 'Phone',
      amount: 'Amount',
      since: 'Since',
      oldest: 'Oldest item',
      archived: 'Archived',
      yes: 'Yes',
    },
    exportFailed: 'Couldn’t export the debts',
  },
"""

ar_block = r"""  debts: {
    tiles: {
      owed: 'مجموع الديون',
      credit: 'أرصدة للزبائن',
      creditHelper: ({ customers }: { customers: string }) => `${customers} دفعوا مقدمًا`,
      paid: ({ month }: { month: string }) => `دفعوا في ${month}`,
      uncollected: 'زيارات غير محصّلة',
      uncollectedHelper: ({ amount }: { amount: string }) => `${amount} · لا تُجمع مع الديون`,
      unpriced: ({ count }: { count: number }) => ` · ${String(count)} بلا سعر`,
    },
    customers: ({ count }: { count: number }) =>
      arabicPlural(count, {
        zero: 'لا زبائن',
        one: 'زبون واحد',
        two: 'زبونان',
        few: `${String(count)} زبائن`,
        many: `${String(count)} زبونًا`,
        other: `${String(count)} زبون`,
      }),
    visits: ({ count }: { count: number }) =>
      arabicPlural(count, {
        zero: 'لا زيارات',
        one: 'زيارة واحدة',
        two: 'زيارتان',
        few: `${String(count)} زيارات`,
        many: `${String(count)} زيارة`,
        other: `${String(count)} زيارة`,
      }),
    owes: {
      title: 'عليهم مبالغ',
      description: 'الأكبر أولًا',
      archived: 'مؤرشف',
      since: ({ date, item }: { date: string; item: string }) => `منذ ${date} · أقدم بند: ${item}`,
      items: { VISIT: 'زيارة', SUBSCRIPTION: 'اشتراك' },
      amount: ({ amount }: { amount: string }) => `عليه ${amount}`,
      whatsapp: 'تذكير على واتساب',
      receive: 'استلام دفعة',
      empty: 'لا توجد ديون',
      pages: 'صفحات من عليهم مبالغ',
    },
    credit: {
      title: 'لهم رصيد',
      description: 'دفعوا مقدمًا أكثر مما استخدموا',
      amount: ({ amount }: { amount: string }) => `له ${amount}`,
      none: 'لا أرصدة للزبائن.',
      pages: 'صفحات من لهم رصيد',
    },
    payers: {
      line: ({ paid, date }: { paid: string; date: string }) => `${paid} · آخر دفعة ${date}`,
      viewAll: 'عرض الكل',
      none: 'لم يدفع أحد في هذا الشهر.',
    },
    csv: {
      name: 'الاسم',
      phone: 'الهاتف',
      amount: 'المبلغ',
      since: 'منذ',
      oldest: 'أقدم بند',
      archived: 'مؤرشف',
      yes: 'نعم',
    },
    exportFailed: 'تعذّر تصدير الديون',
  },
"""

for path, block, end, imp in (
    (EN, en_block, '} as const;\n', "import { englishPlural } from '../plural';\n\n"),
    (AR, ar_block, "} satisfies Catalogue['finance'];\n", "import { arabicPlural } from '../plural';\n"),
):
    s = open(path, encoding='utf8', newline='').read()
    assert s.count(end) == 1 and s.endswith(end)
    s = s[: -len(end)] + block + end
    if imp not in s:
        s = imp + s
    open(path, 'w', encoding='utf8', newline='').write(s)
print('ok')
