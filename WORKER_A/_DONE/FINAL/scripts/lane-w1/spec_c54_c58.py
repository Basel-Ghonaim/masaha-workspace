REPO = r'C:\dev\masaha\app-lane-w1'
F = r'apps\web\src\features\finance'
U = 'npm run test:unit -w @masaha/web -- src/features/finance/services'
D = 'npm run test:component -w @masaha/web -- src/features/finance/components/DebtsTab'
O = 'npm run test:component -w @masaha/web -- src/features/finance/components/OccupancyTab'
H = F + r'\hooks\debts\useDebtsTab.ts'
X = F + r'\hooks\debts\useDebtsExport.ts'
BREAKS = [
    ('B128', H, "value: words.visits({ count: totals.uncollected.visits }),",
     "value: words.visits({ count: totals.uncollected.visits + totals.owed.customers }),", D),
    ('B129', H, """      row.customer.phone === null
        ? null
        : {""", """      false
        ? null
        : {""", D),
    ('B130', F + r'\services\reminderText.ts', "fillReminder(template, { ...values, name: first })", "fillReminder(template, values)", U),
    ('B131', X, "        if (!answer.meta.hasNextPage) break;", "        break;", D),
    ('B132', X, """    } catch {
      const copy = currentCopy();""", """    } catch {
      save({ name: 'partial.csv', text: '' });
      const copy = currentCopy();""", D),
    ('B133', H, "                to: monthEnd < today ? monthEnd : today,", "                to: monthEnd,", D),
    ('B134', F + r'\services\stayText.ts', "  return `${String(Math.floor(minutes / 60))}:${String(minutes % 60).padStart(2, '0')}`;",
     "  return (minutes / 60).toFixed(2);", 'npm run test:unit -w @masaha/web -- src/features/finance/services/stayText'),
    ('B135', F + r'\hooks\occupancy\useOccupancyTab.ts', """    first === undefined || last === undefined
      ? []
      : Array.from({ length: last - first + 1 }, (_, index) => first + index);""",
     """    first === undefined || last === undefined
      ? []
      : Array.from({ length: 24 }, (_, index) => index);""", O),
    ('B136', F + r'\hooks\occupancy\useOccupancyTab.ts', """          report.peakHour === null
            ? words.none""", """          report.peakHour === null
            ? '0'""", O),
    ('B137', F + r'\services\occupancyCsv.ts', "const HOURS = Array.from({ length: 24 },", "const HOURS = Array.from({ length: 23 },",
     'npm run test:unit -w @masaha/web -- src/features/finance/services/occupancyCsv'),
    ('B141', r'apps\web\src\pages\dashboard\space\SettingsPage.tsx', "          <AccountCard />\n", "",
     'npm run test:component -w @masaha/web -- src/pages/dashboard/space/SettingsPage'),
    ('B141b', r'apps\web\src\shared\copy\english\spaceSettings.ts', " Unpaid visits show under «Uncollected».',", "',",
     'npm run test:component -w @masaha/web -- src/pages/dashboard/space/SettingsPage'),
    ('B142', r'apps\web\src\pages\dashboard\space\PackagesPage.tsx', "      <p className=\"text-body-sm text-muted-foreground\">{copy.packages.pageLine}</p>\n", "",
     'npm run test:component -w @masaha/web -- src/pages/dashboard/space/PackagesPage'),
    ('B142b', r'apps\web\src\features\packages\components\list\PackageRow.tsx', """        <span className="text-label text-foreground">{row.price}</span>
""", "", 'npm run test:component -w @masaha/web -- src/features/packages/components'),
    ('B142c', r'apps\web\src\shared\copy\english\packages.ts', "  description: 'Never shown to visitors · chosen at the desk when creating a subscription',",
     "  description: 'Never shown to visitors.',", 'npm run test:component -w @masaha/web -- src/features/packages/components'),
]
