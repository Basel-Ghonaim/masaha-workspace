EN = r'C:\dev\masaha\app-lane-w1\apps\web\src\shared\copy\english\spaceSettings.ts'
AR = r'C:\dev\masaha\app-lane-w1\apps\web\src\shared\copy\arabic\spaceSettings.ts'

def edit(path, pairs):
    s = open(path, encoding='utf8', newline='').read()
    for old, new in pairs:
        assert s.count(old) == 1, (path, old)
        s = s.replace(old, new)
    open(path, 'w', encoding='utf8', newline='').write(s)

edit(EN, [
    ("    autoOutHelp: 'Whoever is still in is checked out at closing time.',",
     "    autoOutHelp:\n      'Whoever is still in is checked out at closing. Unpaid visits show under «Uncollected».',"),
    ("    description: 'A ready WhatsApp message to remind a customer of a debt; you send it yourself.',",
     "    description:\n      'A ready WhatsApp message reminding a customer of their debt; it opens from the customer’s file and from Finance, and you send it.',"),
    ("""  /** A save's refusals, in the owner's words""",
     """  /** The last card: the owner's own account, kept on the personal settings page. */
  account: {
    title: 'My account',
    description: 'Your name, password, language and theme.',
    action: 'Personal settings',
  },
  /** A save's refusals, in the owner's words"""),
])
edit(AR, [
    ("    autoOutHelp: 'يُسجَّل خروج من بقي عند موعد الإغلاق.',",
     "    autoOutHelp: 'يُسجَّل خروج من بقي عند موعد الإغلاق. الزيارات غير المدفوعة تظهر في «غير محصّل».',"),
    ("    description: 'رسالة واتساب جاهزة لتذكير زبون بدينه؛ ترسلها أنت.',",
     "    description:\n      'رسالة واتساب جاهزة لتذكير زبون بدينه، تُفتح من ملف الزبون ومن المالية، وترسلها أنت.',"),
])
s = open(AR, encoding='utf8', newline='').read()
i = s.index('  refusals: {')
s = s[:i] + """  account: {
    title: 'حسابي',
    description: 'الاسم وكلمة المرور واللغة والمظهر.',
    action: 'الإعدادات الشخصية',
  },
""" + s[i:]
open(AR, 'w', encoding='utf8', newline='').write(s)
print('ok')
