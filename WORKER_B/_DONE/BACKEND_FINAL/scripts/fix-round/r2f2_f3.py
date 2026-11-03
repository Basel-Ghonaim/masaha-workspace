import pathlib, sys
root = pathlib.Path(r"C:\dev\masaha\app-b")
def sub(rel, old, new):
    p = root / rel
    t = p.read_bytes().decode("utf-8")
    if t.count(old) != 1:
        sys.exit(f"{rel}: {t.count(old)} matches of {old[:40]!r}")
    p.write_bytes(t.replace(old, new).encode("utf-8"))
f = "docs/features/finance.md"
sub(f, "the space's totals, the uncollected visits apart, and its reminder template.",
       "the space's totals and the uncollected visits, the desk's list — an auto-closed visit left to a customer is in both, so the two are never added ([finding 193](../architecture/findings/193-a-visit-left-to-a-customer-is-both-a-debt-and-uncollected.md)) — and its reminder template.")
sub(f, "one `payments.incomeIn` over 45 windows at once", "one `payments.incomeIn` over 46 windows at once")
w = "apps/api/src/modules/finance/windows.ts"
sub(w, """/** Today in Gaza at `now`. */
export function todayWindow(now: Date): Window {
  return dayWindow(gazaClockOf(now).date);
}

""", "")
t = "apps/api/src/modules/finance/windows.unit.test.ts"
sub(t, "  monthWindow,\n  todayWindow,\n} from", "  monthWindow,\n} from")
sub(t, """  it('today and one day, from Gaza midnight to the next', () => {
    expect(todayWindow(NOW)).toEqual({""", """  it('one day, from Gaza midnight to the next', () => {
    expect(dayWindow('2026-10-29')).toEqual({""")
