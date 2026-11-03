EN = r'C:\dev\masaha\app-lane-w1\apps\web\src\shared\copy\english\packages.ts'
AR = r'C:\dev\masaha\app-lane-w1\apps\web\src\shared\copy\arabic\packages.ts'

def edit(path, pairs):
    s = open(path, encoding='utf8', newline='').read()
    for old, new in pairs:
        assert s.count(old) == 1, (path, old)
        s = s.replace(old, new)
    open(path, 'w', encoding='utf8', newline='').write(s)

edit(EN, [
    ("""  title: 'Private packages',
  description: 'Never shown to visitors.',""",
     """  /** The page's line, at its top: the published week and month prices are sold at the desk too. */
  pageLine: 'Week and month prices are also chosen at the desk when creating a subscription.',
  title: 'Private packages',
  description: 'Never shown to visitors · chosen at the desk when creating a subscription',"""),
    ("""    text: 'Create a package such as “10 days” or “20 hours”.',""",
     """    text: 'Create a package like «10 days» or «20 hours» to pick at the desk.',"""),
    ("""  available: 'Available',
  availableNamed: ({ name }: { name: string }) => `${name}: available`,""",
     """  available: 'Available at the desk',
  availableNamed: ({ name }: { name: string }) => `${name}: available at the desk`,"""),
    ("""    description: 'Private — never shown to visitors.',""",
     """    description: 'Private — never shown to visitors; chosen at the front desk.',"""),
])
edit(AR, [
    ("""  title: 'الباقات الخاصة',
  description: 'لا تظهر للزوار.',""",
     """  pageLine: 'أسعار الأسبوع والشهر تُختار أيضًا في المكتب عند إنشاء اشتراك.',
  title: 'الباقات الخاصة',
  description: 'لا تظهر للزوار · تُختار في المكتب عند إنشاء اشتراك',"""),
    ("""    text: 'أنشئ باقة مثل «10 أيام» أو «20 ساعة».',""",
     """    text: 'أنشئ باقة مثل «10 أيام» أو «20 ساعة» لتختارها في المكتب.',"""),
    ("""  available: 'متاحة',
  availableNamed: ({ name }: { name: string }) => `${name}: متاحة`,""",
     """  available: 'متاحة في المكتب',
  availableNamed: ({ name }: { name: string }) => `${name}: متاحة في المكتب`,"""),
    ("""    description: 'باقة خاصة — لا تظهر للزوار.',""",
     """    description: 'باقة خاصة — لا تظهر للزوار، وتُختار في مكتب الاستقبال.',"""),
])
print('ok')
