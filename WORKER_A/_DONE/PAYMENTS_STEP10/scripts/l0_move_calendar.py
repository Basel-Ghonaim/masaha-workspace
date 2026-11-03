import io, re

ROOT = r'C:\dev\masaha\app\apps\web\src'


def rw(path, fn):
    p = ROOT + '\\' + path
    s = io.open(p, encoding='utf8', newline='').read()
    t = fn(s)
    assert t != s, path
    io.open(p, 'w', encoding='utf8', newline='').write(t)


def barrel(s):
    a = "export { Calendar, type CalendarProps, type DateRange } from './components/fields/Calendar';\n"
    b = (
        "export {\n  DatePicker,\n  DatePickerContent,\n  DatePickerTrigger,\n"
        "  type DatePickerContentProps,\n  type DatePickerTriggerProps,\n"
        "} from './components/fields/DatePicker';\n"
    )
    assert a in s and b in s
    return s.replace(a, '').replace(b, '')


rw(r'shared\design-system\index.ts', barrel)

NAMES = ['Calendar', 'DatePicker', 'DatePickerContent', 'DatePickerTrigger', 'type DateRange']


def move(s):
    m = re.search(r"import \{\n((?:  [^\n]*\n)+)\} from '@shared/design-system';\n", s)
    assert m
    lines = [l.strip().rstrip(',') for l in m.group(1).splitlines()]
    moved = [l for l in lines if l in NAMES]
    kept = [l for l in lines if l not in NAMES]
    assert moved
    main = "import {\n" + ''.join(f"  {l},\n" for l in kept) + "} from '@shared/design-system';\n"
    if len(kept) == 0:
        main = ''
    order = {n: i for i, n in enumerate(NAMES)}
    moved.sort(key=lambda n: order[n])
    one = "import { " + ', '.join(moved) + " } from '@shared/design-system/calendar';\n"
    if len(one) > 101:
        one = "import {\n" + ''.join(f"  {l},\n" for l in moved) + "} from '@shared/design-system/calendar';\n"
    return s[: m.start()] + main + one + s[m.end():]


for f in [
    r'features\payments\components\ledger\LedgerFilters.tsx',
    r'pages\showcase\sections\data\DataTableSection.tsx',
    r'pages\showcase\sections\fields\DatePickerSection.tsx',
]:
    rw(f, move)


def single(s):
    a = "import { Calendar, type DateRange } from '@shared/design-system';\n"
    assert a in s
    return s.replace(a, "import { Calendar, type DateRange } from '@shared/design-system/calendar';\n")


rw(r'pages\showcase\sections\fields\CalendarSection.tsx', single)
print('done')
