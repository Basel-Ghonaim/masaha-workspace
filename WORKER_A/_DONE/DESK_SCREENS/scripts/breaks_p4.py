"""Makes one break, runs its test files, restores from a copy. Usage: breaks_p4.py <name>"""
import shutil
import subprocess
import sys

APP = 'C:/dev/masaha/app/'
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
S = 'C:/dev/masaha/workspace/WORKER_A/DESK_SCREENS/scripts/'
SHEET = 'apps/web/src/features/desk/hooks/sheet/useSubscriptionSheet.ts'

BREAKS = {
    '76': (SHEET,
           "    if (renewalStart !== undefined) setValue('startsOn', renewalStart);" + chr(10),
           '',
           ['src/features/desk/hooks/sheet']),
    '171r': (SHEET,
           '        choices.prices.refresh();' + chr(10) + '      }',
           '      }',
           ['src/features/desk/hooks/sheet']),
    '171w': (SHEET,
           "      failure?.kind === 'refused' && refusal?.errors?.published !== undefined",
           "      false && refusal?.errors?.published !== undefined",
           ['src/features/desk/hooks/sheet']),
    'pubc': ('apps/web/src/features/desk/services/publishedChoices.ts',
           " || one.labelAr !== null) return [];",
           ") return [];",
           ['src/features/desk/services/publishedChoices'], 'unit'),
    'pubr': ('apps/web/src/features/desk/services/sheetRequest.ts',
           '      ? { published: price }',
           '      ? {}',
           ['src/features/desk/services/sheetRequest'], 'unit'),
    '171': ('apps/web/src/features/spaces/hooks/editor/useSpacePrices.ts',
           "    refetchOnMount: 'always'," + chr(10),
           '',
           ['src/features/spaces/hooks/editor/useSpacePrices']),
    '77b': ('apps/web/src/features/desk/components/sheet/SubscriptionSheet.tsx',
           '        closeLabel={view.closeLabel}' + chr(10),
           '        closeLabel={view.closeLabel}' + chr(10) + '        onOpenAutoFocus={(event) => { event.preventDefault(); }}' + chr(10),
           ['src/features/desk/components/sheet']),
    '77': ('apps/web/src/features/desk/components/sheet/SubscriptionSheet.tsx',
           '                    autoFocus' + chr(10),
           '',
           ['src/features/desk/components/sheet']),
    '73': (SHEET,
           'const customChoice: PackageChoice | null = mayTypePrice\n',
           'const customChoice: PackageChoice | null = mayTypePrice || true\n',
           ['src/features/desk/hooks/sheet']),
    '74': (SHEET,
           '  const subscribeKey = useIntentKey().key;\n',
           '  const subscribeKey = createKey;\n',
           ['src/features/desk/hooks/sheet']),
    '75': (SHEET,
           '      toastSubscribed(customer.name, answer.data, {\n',
           '      toastSubscribed(customer.name, { ...answer.data, subscription: { ...answer.data.subscription, priceAgorot: newPrice } }, {\n',
           ['src/features/desk/hooks/sheet']),
}

name = sys.argv[1]
path, old, new, tests, *lane = BREAKS[name]
lane = lane[0] if lane else 'component'
full = APP + path
backup = S + 'bak-p4-break-' + name
shutil.copyfile(full, backup)
try:
    text = open(full, encoding='utf-8').read()
    assert text.count(old) == 1, 'break anchor not found once'
    open(full, 'w', encoding='utf-8', newline='').write(text.replace(old, new))
    out = S + 'p4-break-' + name + '.txt'
    with open(out, 'w', encoding='utf-8') as log:
        code = subprocess.call(
            'npm run test:' + lane + ' -w @masaha/web -- ' + ' '.join(tests),
            shell=True, cwd=APP, stdout=log, stderr=subprocess.STDOUT)
    print('break', name, 'exit', code)
    for line in open(out, encoding='utf-8', errors='replace'):
        if '×' in line or 'Tests ' in line or 'Test Files' in line:
            print(line.rstrip())
finally:
    shutil.copyfile(backup, full)
    print('restored', name)
