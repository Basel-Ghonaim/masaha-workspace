import pathlib, sys
root = pathlib.Path(r"C:\dev\masaha\app-b")
def sub(rel, old, new):
    p = root / rel
    t = p.read_bytes().decode("utf-8")
    if t.count(old) != 1:
        sys.exit(f"{rel}: {t.count(old)} matches of {old[:40]!r}")
    p.write_bytes(t.replace(old, new).encode("utf-8"))
sub("docs/features/overview.md",
    "of the uncollected visits only how many; the capacity is set when it is not `null`.",
    "of the uncollected visits only how many; the capacity is set when it is not `null`. An auto-closed visit left to a customer is counted in both: an uncollected visit, and its customer among those who owe, as the desk's list and the debts keep it ([finding 193](../architecture/findings/193-a-visit-left-to-a-customer-is-both-a-debt-and-uncollected.md)).")
sub("docs/architecture/findings/193-a-visit-left-to-a-customer-is-both-a-debt-and-uncollected.md",
    "\n\nThe choice is the owner's:",
    "\n\nThe owner's overview reads the same two figures (`GET …/overview`, #131): `uncollectedVisits` and `customersOwing` both count such a visit, and [overview](../../features/overview.md) says so. Each is a count of its own list, so neither is wrong; they are never added either.\n\nThe choice is the owner's:")
