"""Breaks: brk.py make <name> | restore <name>. Backup in scripts/breaks/, SHA-256 checked, bytes kept."""
import hashlib, json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = r"C:\dev\masaha\app-b"
BREAKS = json.load(open(os.path.join(HERE, "breaks.json"), encoding="utf-8"))
os.makedirs(os.path.join(HERE, "breaks"), exist_ok=True)

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

cmd, name = sys.argv[1], sys.argv[2]
b = BREAKS[name]
path = os.path.join(REPO, b["file"])
backup = os.path.join(HERE, "breaks", name + ".bak")
if cmd == "make":
    shutil.copyfile(path, backup)
    before = sha(path)
    data = open(path, "rb").read()
    old, new = b["old"].encode("utf-8"), b["new"].encode("utf-8")
    assert data.count(old) == 1, f"{name}: {data.count(old)} occurrences"
    open(path, "wb").write(data.replace(old, new))
    print("BROKEN", name, before[:12], "->", sha(path)[:12])
else:
    want = sha(backup)
    shutil.copyfile(backup, path)
    assert sha(path) == want
    os.remove(backup)
    print("RESTORED", name, want[:12])
