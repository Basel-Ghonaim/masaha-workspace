import sys

ROOT = 'C:/dev/masaha/app/apps/web/src/shared/copy/'

EN = """  /** «اشتراك جديد» / «تجديد الاشتراك»: the subscription sheet (screen 16, K3). */
  sheet: {
    title: { new: 'New customer', subscribe: 'New subscription', renew: 'Renew subscription' },
    newText: 'The name and mobile, then the subscription and the payment.',
    close: 'Close',
    entry: {
      new: 'New customer',
      newNamed: ({ name }: { name: string }) => `New customer named “${name}”`,
      newNumber: 'New customer with this number',
      subscribe: 'New subscription',
      renew: 'Renew',
    },
    name: 'Name',
    phone: 'Mobile number',
    optional: 'Optional',
    noPhone:
      'This customer has no mobile number; add one from “Edit details” to remind them of the debt.',
    phoneRequired: ({ amount }: { amount: string }) =>
      `A mobile number is required: ${amount} stays owed, e.g. +970 59 000 0000`,
    package: 'Package',
    groups: { packages: 'The space’s packages — not shown to visitors' },
    noPackages: 'No packages offered yet.',
    packagesFailed: 'We couldn’t load the packages',
    validity: ({ count }: { count: number }) =>
      englishPlural(count, { one: '1 day', other: `${String(count)} days` }),
    rate: ({ rate, unit }: { rate: string; unit: string }) => `${rate} ${unit}`,
    from: 'From',
    to: 'To',
    toFromPackage: 'From the package',
    noEnd: 'No end date · it stays active until it is ended',
    custom: {
      title: 'Custom',
      terms: 'Set the terms and the price yourself',
      name: 'Subscription name',
      defaultName: 'Custom',
      audience: 'For',
      audiences: { GENERAL: 'Everyone', STUDENT: 'Students' },
      billing: 'Billing',
      billings: { FIXED: 'Fixed price', PER_HOUR: 'Per hour', PER_DAY: 'Per day' },
      price: 'Price (₪)',
      rate: 'Rate (₪)',
      limits: 'Limits — optional',
      limitNames: {
        totalDays: 'Total days',
        daysPerWeek: 'Days a week',
        hoursPerDay: 'Hours a day',
        totalHours: 'Total hours',
      },
      shift: 'Shift',
      reason: 'Reason for the price',
    },
    prior: {
      title: ({ amount }: { amount: string }) => `Owed from before: ${amount}`,
      item: ({ label, amount }: { label: string; amount: string }) => `${label} · ${amount}`,
      note: 'What you receive pays what was owed first, then the new subscription.',
    },
    submit: {
      save: ({ amount }: { amount: string }) => `Save and receive ${amount}`,
      renew: ({ amount }: { amount: string }) => `Renew and receive ${amount}`,
      saveNone: 'Save without payment',
      renewNone: 'Renew without payment',
    },
    half: {
      title: ({ name }: { name: string }) =>
        `${name} was added to the customers; the subscription wasn’t saved.`,
      retry: 'Save the subscription',
      closed: ({ name }: { name: string }) => `${name} is in the customers, with no subscription.`,
    },
    done: {
      new: ({ name }: { name: string }) => `Subscription saved · ${name}`,
      renewed: ({ name }: { name: string }) => `${name}’s subscription renewed`,
      charged: ({ name, amount }: { name: string; amount: string }) => `${name} · ${amount}`,
      part: ({ item, amount }: { item: string; amount: string }) => `${item}: ${amount} received`,
      earlier: 'An earlier debt',
      noPayment: 'No payment',
      owes: ({ amount }: { amount: string }) => `${amount} stays owed`,
      failed: 'We couldn’t save the subscription',
    },
  },
"""

AR = """  /** «اشتراك جديد» / «تجديد الاشتراك»: the subscription sheet (screen 16, K3). */
  sheet: {
    title: { new: 'زبون جديد', subscribe: 'اشتراك جديد', renew: 'تجديد الاشتراك' },
    newText: 'الاسم والجوال، ثم الاشتراك والدفع.',
    close: 'إغلاق',
    entry: {
      new: 'زبون جديد',
      newNamed: ({ name }: { name: string }) => `زبون جديد باسم «${name}»`,
      newNumber: 'زبون جديد بهذا الرقم',
      subscribe: 'اشتراك جديد',
      renew: 'تجديد',
    },
    name: 'الاسم',
    phone: 'رقم الجوال',
    optional: 'اختياري',
    noPhone: 'لا رقم جوال لهذا الزبون؛ أضفه من «تعديل البيانات» لتذكيره بالدين.',
    phoneRequired: ({ amount }: { amount: string }) =>
      `رقم الجوال مطلوب: يبقى ${amount} دينًا، مثل \u200e+970 59 000 0000`,
    package: 'الباقة',
    groups: { packages: 'باقات المساحة — لا تظهر للزوار' },
    noPackages: 'لا باقات متاحة بعد.',
    packagesFailed: 'تعذّر تحميل الباقات',
    validity: ({ count }: { count: number }) =>
      arabicPlural(count, {
        zero: `${String(count)} يوم`,
        one: 'يوم واحد',
        two: 'يومان',
        few: `${String(count)} أيام`,
        many: `${String(count)} يومًا`,
        other: `${String(count)} يوم`,
      }),
    rate: ({ rate, unit }: { rate: string; unit: string }) => `${rate} ${unit}`,
    from: 'من',
    to: 'إلى',
    toFromPackage: 'تُحسب من الباقة',
    noEnd: 'بلا تاريخ نهاية · يبقى نشطًا حتى يُنهى',
    custom: {
      title: 'مخصّص',
      terms: 'حدّد الشروط والسعر بنفسك',
      name: 'اسم الاشتراك',
      defaultName: 'مخصّص',
      audience: 'لمن',
      audiences: { GENERAL: 'الجميع', STUDENT: 'الطلاب' },
      billing: 'طريقة الحساب',
      billings: { FIXED: 'سعر ثابت', PER_HOUR: 'بالساعة', PER_DAY: 'باليوم' },
      price: 'السعر (₪)',
      rate: 'سعر الوحدة (₪)',
      limits: 'الحدود — اختيارية',
      limitNames: {
        totalDays: 'مجموع الأيام',
        daysPerWeek: 'أيام بالأسبوع',
        hoursPerDay: 'ساعات باليوم',
        totalHours: 'مجموع الساعات',
      },
      shift: 'الوردية',
      reason: 'سبب السعر',
    },
    prior: {
      title: ({ amount }: { amount: string }) => `مستحق من قبل: ${amount}`,
      item: ({ label, amount }: { label: string; amount: string }) => `${label} · ${amount}`,
      note: 'يُطبَّق المستلم على المستحق من قبل أولًا، ثم على الاشتراك الجديد.',
    },
    submit: {
      save: ({ amount }: { amount: string }) => `حفظ واستلام ${amount}`,
      renew: ({ amount }: { amount: string }) => `تجديد واستلام ${amount}`,
      saveNone: 'حفظ بدون دفع',
      renewNone: 'تجديد بدون دفع',
    },
    half: {
      title: ({ name }: { name: string }) => `أُضيف ${name} إلى الزبائن؛ لم يُحفظ الاشتراك.`,
      retry: 'حفظ الاشتراك',
      closed: ({ name }: { name: string }) => `${name} في الزبائن بدون اشتراك.`,
    },
    done: {
      new: ({ name }: { name: string }) => `حُفظ الاشتراك · ${name}`,
      renewed: ({ name }: { name: string }) => `جُدّد اشتراك ${name}`,
      charged: ({ name, amount }: { name: string; amount: string }) => `${name} · ${amount}`,
      part: ({ item, amount }: { item: string; amount: string }) => `${item}: استُلم ${amount}`,
      earlier: 'دين سابق',
      noPayment: 'بدون دفع',
      owes: ({ amount }: { amount: string }) => `يبقى ${amount} دينًا`,
      failed: 'تعذّر حفظ الاشتراك',
    },
  },
"""

for path, add, end in [
    ('english/desk.ts', EN, '} as const;'),
    ('arabic/desk.ts', AR, "} satisfies Catalogue['desk'];"),
]:
    p = ROOT + path
    s = open(p, encoding='utf-8').read()
    if 'sheet: {' in s and '«اشتراك جديد» / «تجديد الاشتراك»' in s:
        sys.exit('already there: ' + path)
    i = s.rindex(end)
    s = s[:i] + add + s[i:]
    open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
