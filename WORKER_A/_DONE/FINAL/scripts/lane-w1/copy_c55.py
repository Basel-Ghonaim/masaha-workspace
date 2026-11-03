EN = r'C:\dev\masaha\app-lane-w1\apps\web\src\shared\copy\english\finance.ts'
AR = r'C:\dev\masaha\app-lane-w1\apps\web\src\shared\copy\arabic\finance.ts'

en_block = r"""  /** The space's occupancy, from closed stays (D5.5). */
  occupancy: {
    stay: {
      label: 'Average stay',
      value: ({ time }: { time: string }) => `${time} h`,
      helper: ({ members, visits, month }: { members: string; visits: string; month: string }) =>
        `Members ${members} · visits ${visits} · ${month}`,
    },
    peak: { label: 'Peak hour' },
    attendance: { label: 'Average daily attendance' },
    none: '—',
    noStays: ({ month }: { month: string }) => `No closed stays in ${month}`,
    heatmap: {
      title: 'Peak hours',
      description: 'Average people present per hour · last 4 weeks',
      chart: 'Average people present by day and hour',
      unit: 'people',
      fewer: 'Fewer',
      more: 'More',
      day: 'Day',
      empty: 'No closed stays in the last 4 weeks',
    },
    byDay: {
      title: 'Visits and members per day',
      description: 'Last 14 days',
      chart: 'Visits and members per day, last 14 days',
      period: 'Day',
      members: 'Members',
      visits: 'Visits',
    },
    csv: { day: 'Day' },
  },
"""

ar_block = r"""  occupancy: {
    stay: {
      label: 'متوسط مدة الجلوس',
      value: ({ time }: { time: string }) => `${time} س`,
      helper: ({ members, visits, month }: { members: string; visits: string; month: string }) =>
        `المشتركون ${members} · الزيارات ${visits} · ${month}`,
    },
    peak: { label: 'ساعة الذروة' },
    attendance: { label: 'متوسط الحضور اليومي' },
    none: '—',
    noStays: ({ month }: { month: string }) => `لا جلسات مغلقة في ${month}`,
    heatmap: {
      title: 'ساعات الذروة',
      description: 'متوسط الحاضرين لكل ساعة · آخر 4 أسابيع',
      chart: 'متوسط الحاضرين حسب اليوم والساعة',
      unit: 'أشخاص',
      fewer: 'أقل',
      more: 'أكثر',
      day: 'اليوم',
      empty: 'لا جلسات مغلقة في آخر 4 أسابيع',
    },
    byDay: {
      title: 'الزيارات والمشتركون يوميًا',
      description: 'آخر 14 يومًا',
      chart: 'الزيارات والمشتركون يوميًا، آخر 14 يومًا',
      period: 'اليوم',
      members: 'مشتركون',
      visits: 'زيارات',
    },
    csv: { day: 'اليوم' },
  },
"""

for path, block, end in ((EN, en_block, '} as const;\n'), (AR, ar_block, "} satisfies Catalogue['finance'];\n")):
    s = open(path, encoding='utf8', newline='').read()
    assert s.count(end) == 1 and s.endswith(end)
    s = s[: -len(end)] + block + end
    open(path, 'w', encoding='utf8', newline='').write(s)
print('ok')
