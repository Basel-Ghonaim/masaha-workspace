import os
os.chdir(r'C:\dev\masaha\app-lane-w3\apps\web\src')
def edit(p, pairs):
    s=open(p,encoding='utf8').read()
    for a,b in pairs:
        assert s.count(a)==1,(p,a)
        s=s.replace(a,b)
    open(p,'w',encoding='utf8',newline='').write(s)
edit('shared/copy/arabic/desk.ts',[("    clearEnd: 'بلا تاريخ نهاية',","    clearEnd: 'بلا تاريخ نهاية',\n    calendar: { previous: 'الشهر السابق', next: 'الشهر التالي' },")])
edit('shared/copy/english/desk.ts',[("    clearEnd: 'No end date',","    clearEnd: 'No end date',\n    calendar: { previous: 'Previous month', next: 'Next month' },")])
s=open('features/desk/components/sheet/SubscriptionSheet.tsx',encoding='utf8').read()
s=s.replace("import { PriorDebts } from './PriorDebts';","import { DateField } from './DateField';\nimport { PriorDebts } from './PriorDebts';",1)
open('features/desk/components/sheet/SubscriptionSheet.tsx','w',encoding='utf8',newline='').write(s)
