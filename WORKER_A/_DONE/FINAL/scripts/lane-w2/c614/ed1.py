p = r'C:\dev\masaha\app-lane-w2\apps\web\src\features\lookups\components\sheet\LookupSheet.component.test.tsx'
s = open(p, encoding='utf8', newline='').read()
def rep(old, new):
    global s
    assert s.count(old) == 1, old
    s = s.replace(old, new)
rep("import { fakeTransport, ok, restoreTransport } from '../../../../test/fakeTransport';",
    "import { bodyOf, fakeTransport, ok, restoreTransport } from '../../../../test/fakeTransport';")
rep("""/** A name with the Unicode isolates""", """/** Eleven areas of Gaza City, in order: more than ten, so a sheet offers a position. */
const ELEVEN = Array.from({ length: 11 }, (_, index) => ({
  id: 100 + index,
  governorateId: 2,
  nameAr: `منطقة ${String(index + 1)}`,
  nameEn: `Area ${String(index + 1)}`,
  isActive: true,
}));

/** A name with the Unicode isolates""")
rep("""    await userEvent.click(within(sheet).getByRole('switch', { name: 'Active' }));
    await userEvent.click(within(sheet).getByRole('button', { name: 'Save' }));""",
"""    await userEvent.click(within(sheet).getByRole('button', { name: 'Save' }));""")
open(p, 'w', encoding='utf8', newline='').write(s)
