import io

BASE = r'C:\dev\masaha\app-lane-a\apps\web\src\shared\copy'

EN = """  /** A closure's extension of the subscriptions it covered, the owner's, once the closure started. */
  extension: {
    action: 'Extend subscriptions',
    title: 'Extend the subscriptions this closure covered?',
    covered: ({ count }: { count: number }) =>
      englishPlural(count, {
        one: 'The extension moves 1 subscription.',
        other: `The extension moves ${String(count)} subscriptions.`,
      }),
    text: 'Those the closure covered, and their renewals not started yet; each moves by the days below. It can’t be undone, nor applied again for this closure.',
    days: 'Number of days',
    daysHelper: ({ days, first, last }: { days: string; first: string; last: string }) =>
      `The closure’s days: ${days} (${first} – ${last})`,
    daysRange: 'Between 1 and 365 days',
    submit: ({ count }: { count: number }) =>
      englishPlural(count, {
        one: 'Extend 1 subscription',
        other: `Extend ${String(count)} subscriptions`,
      }),
    count: ({ count }: { count: number }) =>
      englishPlural(count, { one: '1 subscription', other: `${String(count)} subscriptions` }),
    dayCount: ({ count }: { count: number }) =>
      englishPlural(count, { one: '1 day', other: `${String(count)} days` }),
    line: ({
      count,
      days,
      name,
      date,
    }: {
      count: string;
      days: string;
      name: string;
      date: string;
    }) => `Extended ${count} · ${days} · ${name} · ${date}`,
    none: 'This closure covered no subscription, so there is nothing to extend.',
    applied: ({ count, days }: { count: string; days: string }) =>
      `This closure’s subscriptions were already extended: ${count} · ${days}.`,
    done: 'Subscriptions extended',
    doneText: ({ count, days }: { count: string; days: string }) => `${count} · ${days}`,
    failed: 'We couldn’t extend them',
    loadFailed: 'We couldn’t work out the subscriptions covered',
    lost: 'No answer came back. Try again — they won’t be extended twice.',
    back: 'Back',
  },
"""

AR = """  extension: {
    action: 'تمديد الاشتراكات',
    title: 'تمديد الاشتراكات التي شملها الإغلاق؟',
    covered: ({ count }: { count: number }) =>
      arabicPlural(count, {
        zero: 'لا يشمل التمديد أي اشتراك.',
        one: 'يشمل التمديد اشتراكًا واحدًا.',
        two: 'يشمل التمديد اشتراكين.',
        few: `يشمل التمديد ${String(count)} اشتراكات.`,
        many: `يشمل التمديد ${String(count)} اشتراكًا.`,
        other: `يشمل التمديد ${String(count)} اشتراك.`,
      }),
    text: 'هي التي شملها الإغلاق، وتجديداتها التي لم تبدأ بعد؛ يتأخر كلٌّ منها بعدد الأيام أدناه. لا يمكن التراجع، ولا التمديد مرة ثانية لهذا الإغلاق.',
    days: 'عدد الأيام',
    daysHelper: ({ days, first, last }: { days: string; first: string; last: string }) =>
      `أيام الإغلاق: ${days} (${first} – ${last})`,
    daysRange: 'بين 1 و365 يومًا',
    submit: ({ count }: { count: number }) =>
      arabicPlural(count, {
        zero: `مدّد ${String(count)} اشتراك`,
        one: 'مدّد اشتراكًا واحدًا',
        two: 'مدّد اشتراكين',
        few: `مدّد ${String(count)} اشتراكات`,
        many: `مدّد ${String(count)} اشتراكًا`,
        other: `مدّد ${String(count)} اشتراك`,
      }),
    count: ({ count }: { count: number }) =>
      arabicPlural(count, {
        zero: 'لا اشتراكات',
        one: 'اشتراك واحد',
        two: 'اشتراكان',
        few: `${String(count)} اشتراكات`,
        many: `${String(count)} اشتراكًا`,
        other: `${String(count)} اشتراك`,
      }),
    dayCount: ({ count }: { count: number }) =>
      arabicPlural(count, {
        zero: 'لا أيام',
        one: 'يوم واحد',
        two: 'يومان',
        few: `${String(count)} أيام`,
        many: `${String(count)} يومًا`,
        other: `${String(count)} يوم`,
      }),
    line: ({
      count,
      days,
      name,
      date,
    }: {
      count: string;
      days: string;
      name: string;
      date: string;
    }) => `مُدّد ${count} · ${days} · ${name} · ${date}`,
    none: 'لم يشمل هذا الإغلاق أي اشتراك، فلا شيء يُمدَّد.',
    applied: ({ count, days }: { count: string; days: string }) =>
      `مُدّدت اشتراكات هذا الإغلاق من قبل: ${count} · ${days}.`,
    done: 'مُدّدت الاشتراكات',
    doneText: ({ count, days }: { count: string; days: string }) => `${count} · ${days}`,
    failed: 'تعذّر التمديد',
    loadFailed: 'تعذّر حساب الاشتراكات المشمولة',
    lost: 'لم يصل الرد. أعد المحاولة — لن تُمدَّد مرتين.',
    back: 'رجوع',
  },
"""

MARK = '  list: {\n'
for name, block, imp in (
    ('english', EN, "import { englishPlural } from '../plural';\n\n"),
    ('arabic', AR, "import { arabicPlural } from '../plural';\n"),
):
    p = BASE + '\\' + name + '\\announcements.ts'
    s = io.open(p, encoding='utf8', newline='').read()
    assert s.count(MARK) == 1
    s = s.replace(MARK, block + MARK)
    s = imp + s
    io.open(p, 'w', encoding='utf8', newline='').write(s)
print('ok')
