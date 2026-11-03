import pathlib, re, sys
p = pathlib.Path(r"C:\dev\masaha\app-b\docs\api\api-contract.md")
t = p.read_bytes().decode("utf-8")
mode = sys.argv[1]  # 'theirs-first' keeps the fixup's lines; 'union' keeps head's who-owes and adds theirs' extra
def fix(m):
    ours = m.group(1).splitlines(keepends=True)
    theirs = m.group(2).splitlines(keepends=True)
    if mode == "fixup-whoowes":
        return "".join(l for l in theirs if l.startswith("- **Who owes**"))
    if mode == "keep-head-whoowes-add-theirs":
        who = [l for l in ours if l.startswith("- **Who owes**")]
        rest = [l for l in theirs if not l.startswith("- **Who owes**")]
        return "".join(who + rest)
    sys.exit("mode")
new, n = re.subn(r"<<<<<<< [^\n]*\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n", fix, t, flags=re.S)
if n != 1: sys.exit(f"{n} conflicts")
p.write_bytes(new.encode("utf-8"))
