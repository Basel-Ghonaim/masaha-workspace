REPO = r'C:\dev\masaha\app-lane-w1'
F = r'apps\web\src\features\finance'
U = 'npm run test:unit -w @masaha/web -- src/features/finance/services'
C = 'npm run test:component -w @masaha/web -- src/features/finance/components'
BREAKS = [
    ('B121', F + r'\services\months.ts', "length: FINANCE_MONTHS_BACK + 1", "length: FINANCE_MONTHS_BACK + 2", U),
    ('B122', F + r'\services\monthChange.ts', "  if (previous <= 0) return null;\n", "", U),
    ('B123', F + r'\hooks\income\useIncomeTab.ts', "value: shown(report.allTime.totalAgorot),", "value: shown(report.income.totalAgorot),", C),
    ('B124', F + r'\components\FinanceScreen.tsx', "<IncomeTab spaceId={spaceId} asked={screen.asked} />", "<IncomeTab spaceId={spaceId} asked={undefined} />", C),
    ('B125', F + r'\services\incomeCsv.ts', "shekelsText(income.totalAgorot),", "String(income.totalAgorot),", U),
    ('B126', F + r'\hooks\useFinanceExport.ts', "    toast.success(words.done, { description: file.name });\n", "", C),
    ('B127', r'apps\web\src\pages\dashboard\navigation.ts', "  { name: 'finance', segment: 'finance', roles: OWNER, group: 'money' },",
     "  { name: 'finance', segment: 'finance', roles: BOTH, group: 'money' },",
     'npm run test:component -w @masaha/web -- src/pages/dashboard/space/finance'),
]
