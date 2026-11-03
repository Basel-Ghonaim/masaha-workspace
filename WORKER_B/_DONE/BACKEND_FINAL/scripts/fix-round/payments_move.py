"""Move the desk's web sentences from payments.md's Finance bullet back to the front desk bullet.
Modes: 'tree' edits the working file; 'ours'/'theirs' resolve one conflict in it, taking the Finance
bullet's wording from that side and the front desk bullet from ours."""
import pathlib, re, sys
p = pathlib.Path(r"C:\dev\masaha\app-b\docs\features\payments.md")
WEB = (" On the web, the desk's screen lists the uncollected visits and records a payment on one "
       "([desk](desk.md), 2026-10-25, #117); «استلام دفعة» records a payment on one of a customer's "
       "items, a visit or a subscription (2026-10-25, #119).")
def move(desk, fin):
    if not fin.rstrip("\n").endswith(WEB): sys.exit("finance bullet lacks the web sentences")
    fin = fin.rstrip("\n")[: -len(WEB)] + "\n"
    if not desk.rstrip("\n").endswith(WEB): desk = desk.rstrip("\n") + WEB + "\n"
    return desk, fin
t = p.read_bytes().decode("utf-8")
mode = sys.argv[1]
if mode == "tree":
    lines = t.splitlines(keepends=True)
    d = next(i for i, l in enumerate(lines) if l.startswith("- **The front desk**"))
    f = next(i for i, l in enumerate(lines) if l.startswith("- **Finance**"))
    lines[d], lines[f] = move(lines[d], lines[f])
    p.write_bytes("".join(lines).encode("utf-8"))
else:
    def fix(m):
        ours = m.group(1).splitlines(keepends=True); theirs = m.group(2).splitlines(keepends=True)
        src = ours if mode == "ours" else theirs
        desk = next(l for l in ours if l.startswith("- **The front desk**"))
        fin = next(l for l in src if l.startswith("- **Finance**"))
        if not fin.rstrip("\n").endswith(WEB):
            desk2 = desk if desk.rstrip("\n").endswith(WEB) else desk.rstrip("\n") + WEB + "\n"
            return desk2 + fin
        return "".join(move(desk, fin))
    new, n = re.subn(r"<<<<<<< [^\n]*\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n", fix, t, flags=re.S)
    if n != 1: sys.exit(f"{n} conflicts")
    p.write_bytes(new.encode("utf-8"))
