"""Commit 3's words: dataReports.admin (both languages) and spaceLinks.choices.allSpaces."""
COPY = 'C:/dev/masaha/app-lane-b/apps/web/src/shared/copy/'


def edit(rel, pairs):
    path = COPY + rel
    with open(path, encoding='utf8', newline='') as handle:
        text = handle.read()
    for old, new in pairs:
        assert text.count(old) == 1, (rel, old[:60], text.count(old))
        text = text.replace(old, new)
    with open(path, 'w', encoding='utf8', newline='') as handle:
        handle.write(text)


EN_ADMIN = """  /** The admin's «بلاغات البيانات»: every space's reports. */
  admin: {
    label: 'Data reports',
    intro:
      'The admin decides unverified spaces’ reports. Verified spaces’ reports are decided by their owner and shown here for reference.',
    columns: {
      space: 'Space',
      field: 'Field',
      report: 'Report',
      reporter: 'Reporter',
      date: 'Date',
      status: 'Status',
      handledBy: 'Handled by',
      actions: 'Actions',
    },
    handledBy: { admin: 'Admin', owner: 'Owner' },
    space: 'Space',
    chosen: 'A chosen space',
    field: 'Field',
    allFields: 'All fields',
    tags: {
      space: ({ name }: { name: string }) => `Space: ${name}`,
      field: ({ field }: { field: string }) => `Field: ${field}`,
      removeSpace: 'Remove the space filter',
      removeField: 'Remove the field filter',
      clear: 'Clear filters',
    },
    filters: {
      title: 'Filters',
      show: ({ count }: { count: number }) =>
        englishPlural(count, { one: 'Show 1 report', other: `Show ${String(count)} reports` }),
      none: 'No results — change the filters',
    },
    readOnly: 'Verified space — its owner decides this report. For reference only.',
    openSpace: 'View the space',
    forbiddenVerified: 'This space is verified: its owner decides this report.',
  },
"""

AR_ADMIN = """  admin: {
    label: 'بلاغات البيانات',
    intro:
      'تقرّر الإدارة بلاغات المساحات غير الموثّقة. بلاغات المساحات الموثّقة يقرّرها مالكها، وتظهر هنا للاطلاع.',
    columns: {
      space: 'المساحة',
      field: 'الحقل',
      report: 'البلاغ',
      reporter: 'المُبلِّغ',
      date: 'التاريخ',
      status: 'الحالة',
      handledBy: 'يعالجه',
      actions: 'إجراءات',
    },
    handledBy: { admin: 'الإدارة', owner: 'المالك' },
    space: 'المساحة',
    chosen: 'مساحة محددة',
    field: 'الحقل',
    allFields: 'كل الحقول',
    tags: {
      space: ({ name }: { name: string }) => `المساحة: ${name}`,
      field: ({ field }: { field: string }) => `الحقل: ${field}`,
      removeSpace: 'إزالة فلتر المساحة',
      removeField: 'إزالة فلتر الحقل',
      clear: 'مسح الفلاتر',
    },
    filters: {
      title: 'الفلاتر',
      show: ({ count }: { count: number }) =>
        arabicPlural(count, {
          zero: `عرض ${String(count)} بلاغ`,
          one: 'عرض البلاغ',
          two: 'عرض البلاغين',
          few: `عرض ${String(count)} بلاغات`,
          many: `عرض ${String(count)} بلاغًا`,
          other: `عرض ${String(count)} بلاغ`,
        }),
      none: 'لا نتائج — غيّر الفلاتر',
    },
    readOnly: 'مساحة موثّقة — يقرّر مالكها هذا البلاغ. للاطلاع فقط.',
    openSpace: 'عرض المساحة',
    forbiddenVerified: 'هذه المساحة موثّقة: يقرّر مالكها هذا البلاغ.',
  },
"""

edit('english/dataReports.ts', [
    ("    show: 'Show',\n  },\n} as const;\n", "    show: 'Show',\n  },\n" + EN_ADMIN + "} as const;\n"),
])
edit('arabic/dataReports.ts', [
    ("    show: 'عرض',\n  },\n} satisfies Catalogue['dataReports'];\n",
     "    show: 'عرض',\n  },\n" + AR_ADMIN + "} satisfies Catalogue['dataReports'];\n"),
])
edit('english/spaceLinks.ts', [
    ("    atDesk: 'Front desk',\n",
     "    atDesk: 'Front desk',\n    /** The space filter's first choice, which clears it. */\n    allSpaces: 'All spaces',\n"),
])
edit('arabic/spaceLinks.ts', [
    ("    atDesk: 'مكتب استقبال',\n", "    atDesk: 'مكتب استقبال',\n    allSpaces: 'كل المساحات',\n"),
])
print('ok')
