EN = r'C:\dev\masaha\app-lane-w1\apps\web\src\shared\copy\english\overview.ts'
AR = r'C:\dev\masaha\app-lane-w1\apps\web\src\shared\copy\arabic\overview.ts'

en_block = r"""  /** The admin's overview of the platform (screen 25): nothing of a space's operations. */
  admin: {
    tiles: {
      label: 'Platform summary',
      spaces: {
        label: 'Spaces',
        helper: ({
          verified,
          unverified,
          hidden,
        }: {
          verified: string;
          unverified: string;
          hidden: string;
        }) => `${verified} verified · ${unverified} unverified · ${hidden} hidden`,
      },
      reports: {
        label: 'Open data reports',
        helper: ({ admin, owners }: { admin: string; owners: string }) =>
          `${admin} waiting for the admin · ${owners} waiting for owners`,
      },
      stale: {
        label: 'Stale or missing data',
        helper: 'By the platform’s freshness limits, or not added yet',
      },
      unverified: {
        label: 'Unverified spaces, no owner',
        helper: 'The admin edits them until an owner is linked',
      },
      users: { label: 'New users', helper: 'Last 30 days' },
    },
    completeness: {
      title: 'Data completeness',
      description:
        'The spaces the admin edits — the unverified ones, hidden ones included — that miss something or hold stale data. Verified spaces are their owners’ to update.',
      missing: ({ group }: { group: string }) => `${group} · not added yet`,
      stale: ({ group, days }: { group: string; days: number }) =>
        englishPlural(days, {
          one: `${group} · ${String(days)} day`,
          other: `${group} · ${String(days)} days`,
        }),
      edit: 'Edit',
      viewAll: 'View all',
      viewAllCounted: ({ total }: { total: string }) => `View all (${total})`,
      none: 'No space misses anything.',
    },
  },
"""

ar_block = r"""  admin: {
    tiles: {
      label: 'ملخص المنصة',
      spaces: {
        label: 'المساحات',
        helper: ({
          verified,
          unverified,
          hidden,
        }: {
          verified: string;
          unverified: string;
          hidden: string;
        }) => `${verified} موثّقة · ${unverified} غير موثّقة · ${hidden} مخفية`,
      },
      reports: {
        label: 'بلاغات مفتوحة',
        helper: ({ admin, owners }: { admin: string; owners: string }) =>
          `${admin} بانتظار الإدارة · ${owners} بانتظار المالكين`,
      },
      stale: {
        label: 'بيانات قديمة أو ناقصة',
        helper: 'حسب حدود الحداثة في إعدادات المنصة، أو لم تُضف بعد',
      },
      unverified: {
        label: 'مساحات غير موثّقة بلا مالك',
        helper: 'تعدّلها الإدارة حتى يُربط مالكها',
      },
      users: { label: 'مستخدمون جدد', helper: 'آخر 30 يومًا' },
    },
    completeness: {
      title: 'اكتمال البيانات',
      description:
        'المساحات التي تعدّلها الإدارة — غير الموثّقة، والمخفية منها — وينقصها شيء أو فيها بيانات قديمة. الموثّقة يحدّثها مالكوها.',
      missing: ({ group }: { group: string }) => `${group} · لم تُضف بعد`,
      stale: ({ group, days }: { group: string; days: number }) =>
        arabicPlural(days, {
          zero: `${group} · اليوم`,
          one: `${group} · يوم واحد`,
          two: `${group} · يومان`,
          few: `${group} · ${String(days)} أيام`,
          many: `${group} · ${String(days)} يومًا`,
          other: `${group} · ${String(days)} يوم`,
        }),
      edit: 'تعديل',
      viewAll: 'عرض الكل',
      viewAllCounted: ({ total }: { total: string }) => `عرض الكل (${total})`,
      none: 'لا مساحات ينقصها شيء.',
    },
  },
"""

for path, block, end in ((EN, en_block, '} as const;\n'), (AR, ar_block, '} satisfies Catalogue[\'overview\'];\n')):
    s = open(path, encoding='utf8', newline='').read()
    assert s.count(end) == 1 and s.endswith(end)
    s = s[: -len(end)] + block + end
    open(path, 'w', encoding='utf8', newline='').write(s)
print('ok')
