import os
os.chdir(r'C:\dev\masaha\app-lane-w3\apps\web\src\shared\copy')
def edit(p, pairs):
    s=open(p,encoding='utf8').read()
    for a,b in pairs:
        assert s.count(a)==1,(p,a)
        s=s.replace(a,b)
    open(p,'w',encoding='utf8',newline='').write(s)
edit('arabic/desk.ts',[
("    groups: { published: 'منشورة للزوار', packages: 'باقات المساحة — لا تظهر للزوار' },","    groups: { published: 'منشورة للزوار', packages: 'خاصة بالمكتب — لا تظهر للزوار' },\n    private: 'خاصة',"),
("    noEnd: 'بلا تاريخ نهاية · يبقى نشطًا حتى يُنهى',","""    noEnd: 'بلا تاريخ نهاية · يبقى نشطًا حتى يُنهى',
    noEndLimit: ({ limit }: { limit: string }) => `بلا تاريخ نهاية · ينتهي عند استهلاك ${limit}`,
    endOrLimit: ({ date, limit }: { date: string; limit: string }) =>
      `ينتهي في ${date} أو عند استهلاك ${limit}، أيهما أسبق`,
    limitDays: ({ count }: { count: number }) =>
      arabicPlural(count, {
        zero: 'لا أيام',
        one: 'يوم واحد',
        two: 'يومين',
        few: `${String(count)} أيام`,
        many: `${String(count)} يومًا`,
        other: `${String(count)} يوم`,
      }),
    limitHours: ({ count }: { count: number }) =>
      arabicPlural(count, {
        zero: 'لا ساعات',
        one: 'ساعة واحدة',
        two: 'ساعتين',
        few: `${String(count)} ساعات`,
        many: `${String(count)} ساعة`,
        other: `${String(count)} ساعة`,
      }),
    clearEnd: 'بلا تاريخ نهاية',
    total: 'المجموع',
    calcItem: ({ item, balance }: { item: string; balance: string }) => `${item}: ${balance}`,
    calcNew: ({ name, price }: { name: string; price: string }) => `الاشتراك: ${name} ${price}`,
    calcRenewal: ({ name, price }: { name: string; price: string }) => `التجديد: ${name} ${price}`,
    fromPublished: 'من السعر المنشور',
    byAttendance: {
      PER_HOUR: ({ rate }: { rate: string }) => `يُحسب من الحضور: ${rate} للساعة`,
      PER_DAY: ({ rate }: { rate: string }) => `يُحسب من الحضور: ${rate} لليوم`,
    },"""),
])
edit('english/desk.ts',[
("    groups: { published: 'Published to visitors', packages: 'The space’s packages — not shown to visitors' },","x"),
] if False else [])
s=open('english/desk.ts',encoding='utf8').read()
i=s.index("    groups: {")
j=s.index("\n",s.index("packages:",i))
print(repr(s[i:j+60]))
