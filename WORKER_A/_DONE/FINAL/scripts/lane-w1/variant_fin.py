import os, re
STAGE = os.environ['STAGE']  # c53 | c54 | c55
W = 'apps/web/src/'
F = W + 'features/finance/'

income = [
    'repository/financeRepository.ts', 'repository/financeRepository.unit.test.ts',
    'hooks/queryKeys.ts', 'hooks/useFinanceTabs.ts', 'hooks/useFinanceScreen.ts',
    'hooks/useLoadFailure.ts', 'hooks/useMoney.ts',
    'hooks/income/useIncomeQuery.ts', 'hooks/income/useIncomeTab.ts', 'hooks/income/useMonthCollections.ts',
    'services/months.ts', 'services/months.unit.test.ts', 'services/monthLabel.ts',
    'services/monthChange.ts', 'services/monthChange.unit.test.ts', 'services/shekels.ts',
    'services/incomeCsv.ts', 'services/incomeCsv.unit.test.ts',
    'components/LoadFailure.tsx', 'components/MonthField.tsx', 'components/ChartCard.tsx',
    'components/CollectionsTable.tsx', 'components/IncomeTab.tsx', 'components/IncomeTab.component.test.tsx',
    'components/FinanceExport.tsx', 'types/FinanceLinks.ts', 'index.ts',
]
debts = [
    'hooks/debts/useDebtsQuery.ts', 'hooks/debts/usePayersQuery.ts', 'hooks/debts/useDebtsTab.ts',
    'hooks/debts/useDebtsExport.ts', 'services/dateText.ts', 'services/reminderText.ts',
    'services/reminderText.unit.test.ts', 'services/debtsCsv.ts', 'components/DebtorRow.tsx',
    'components/DebtsTab.tsx', 'components/DebtsTab.component.test.tsx',
]
occupancy = [
    'hooks/occupancy/useOccupancyQuery.ts', 'hooks/occupancy/useOccupancyTab.ts',
    'services/stayText.ts', 'services/stayText.unit.test.ts', 'services/weekdays.ts',
    'services/occupancyCsv.ts', 'services/occupancyCsv.unit.test.ts',
    'components/OccupancyTab.tsx', 'components/OccupancyTab.component.test.tsx',
]
files = {'c53': income, 'c54': debts, 'c55': occupancy}[STAGE]
PLAIN = [F + f for f in files if f not in ('components/FinanceScreen.tsx', 'hooks/useFinanceExport.ts')]
if STAGE == 'c53':
    PLAIN += [W + 'pages/dashboard/space/finance/FinancePage.tsx',
              W + 'pages/dashboard/space/finance/FinancePage.component.test.tsx',
              'docs/features/finance.md']
else:
    PLAIN += ['docs/features/finance.md']


def cut_block(text, start_marker, end_marker):
    a = text.index(start_marker)
    b = text.index(end_marker, a)
    return text[:a] + text[b:]


def screen(text):
    if STAGE in ('c53',):
        text = text.replace("import { DebtsTab } from './DebtsTab';\n", '')
        text = cut_block(text, '      <TabsContent value="debts">', '      <TabsContent value="occupancy">')
    if STAGE in ('c53', 'c54'):
        text = text.replace("import { OccupancyTab } from './OccupancyTab';\n", '')
        text = cut_block(text, '      <TabsContent value="occupancy">', '    </Tabs>')
    if STAGE == 'c53':
        text = text.replace("""export function FinanceScreen({
  spaceId,
  spaceName,
  links,
}: {""", """export function FinanceScreen({
  spaceId,
}: {""")
    return text


def export(text):
    if STAGE == 'c55':
        return text
    text = text.replace("import { occupancyCsv } from '../services/occupancyCsv';\n", '')
    text = text.replace("import { useOccupancyQuery } from './occupancy/useOccupancyQuery';\n", '')
    text = text.replace("  const occupancy = useOccupancyQuery(spaceId, tabs.asked, tabs.tab === 'occupancy').data;\n", '')
    text = cut_block(text, "  if (tabs.tab === 'occupancy') {", '  return {\n    more: words.more,\n    label: words.income,')
    text = text.replace("import { gazaClockOf } from '@masaha/shared/core';\n", '')
    text = text.replace("import { useMoney } from './useMoney';\n", '')
    text = text.replace("  const { language } = useMoney();\n", '')
    if STAGE == 'c53':
        text = text.replace("import { useDebtsExport } from './debts/useDebtsExport';\n", '')
        text = cut_block(text, '  const debts = useDebtsExport(spaceId, saved);', '  return {\n    more: words.more,\n    label: words.income,')
        text = text.replace(
            " (the debts' from\n * every page, read in turn), saved on the owner's device,",
            ", saved on the\n * owner's device,",
        )
    return text


def copy(text):
    if STAGE == 'c55':
        return text
    end = text.rindex('} ')
    marker = '  occupancy: {\n    stay:'
    a = text.rfind('  /** The space', 0, text.index(marker)) if '  /** The space' in text else -1
    a = a if a != -1 and a > text.index('  debts: {') else text.index(marker)
    text = text[:a] + text[end:]
    if STAGE == 'c53':
        end = text.rindex('} ')
        b = text.index('  debts: {')
        doc = text.rfind('  /** Who owes', 0, b)
        text = text[: doc if doc != -1 else b] + text[end:]
        text = text.replace("import { englishPlural } from '../plural';\n\n", '')
        text = text.replace("import { arabicPlural } from '../plural';\n", '')
    return text


VARIANTS = {
    F + 'components/FinanceScreen.tsx': screen,
    F + 'hooks/useFinanceExport.ts': export,
    W + 'shared/copy/english/finance.ts': copy,
    W + 'shared/copy/arabic/finance.ts': copy,
}
ALLOW_SAME = STAGE == 'c55'
