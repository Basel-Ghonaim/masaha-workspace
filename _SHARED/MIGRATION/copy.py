"""Phase 2: copy every manifest row (no overwrite), verify targets, re-hash sources, write VERIFY.md."""
import csv, hashlib, os, shutil, sys

ROOT = r"D:\masahaWorkspace"
MIG = os.path.join(ROOT, "_SHARED", "MIGRATION")
ACTIVE = [os.path.join(ROOT, *p) for p in (("WORKER_A", "GALLERY"), ("WORKER_B", "HARDEN"), ("DESIGN", "ROUND2"))]
SRC_ROOTS = [r"C:\Users\basel\.prompt", r"C:\Users\basel\Downloads\masaha-next",
             r"C:\Users\basel\Downloads\masaha-handoffs",
             r"C:\Users\basel\Downloads\masaha-prompts-archive-2026-10-08"]
DL = r"C:\Users\basel\Downloads"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def is_active(t):
    return any(t == a or t.startswith(a + os.sep) for a in ACTIVE)


with open(os.path.join(MIG, "manifest.csv"), encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))

# 1. copy
for r in rows:
    t = r["target"]
    if os.path.exists(t):
        sys.exit(f"target exists: {t}")
    os.makedirs(os.path.dirname(t), exist_ok=True)
    shutil.copy2(r["source"], t)
print("copied", len(rows))

# 2. verify targets
mism = []
for r in rows:
    t = r["target"]
    if not os.path.isfile(t):
        mism.append(f"missing {t}")
    elif os.path.getsize(t) != int(r["size"]) or sha(t) != r["sha256"]:
        mism.append(f"differs {t}")
n_files = 0
for d, _, fs in os.walk(ROOT):
    if d == MIG or d.startswith(MIG + os.sep):
        continue
    n_files += len(fs)
kit = sum(1 for r in rows if r["target"].startswith(MIG + os.sep))
expected = len(rows) - kit

# 3. re-hash sources
changed_done, changed_active = [], []
for r in rows:
    s = r["source"]
    if not os.path.isfile(s):
        (changed_active if is_active(r["target"]) else changed_done).append(f"gone {s}")
    elif sha(s) != r["sha256"]:
        (changed_active if is_active(r["target"]) else changed_done).append(s)
known = {r["source"] for r in rows}
new_files = []
bases = list(SRC_ROOTS) + [os.path.join(DL, d) for d in os.listdir(DL) if d.endswith("-shots") and os.path.isdir(os.path.join(DL, d))]
for b in bases:
    for d, _, fs in os.walk(b):
        for x in fs:
            p = os.path.join(d, x)
            if p not in known:
                new_files.append(p)

L = ["# VERIFY\n",
     f"- Manifest rows: **{len(rows)}**; files copied: **{len(rows)}**.",
     f"- Files under `D:\\masahaWorkspace` excluding `_SHARED\\MIGRATION\\`: **{n_files}**; expected {expected} (rows {len(rows)} minus {kit} kit file(s) that live inside `_SHARED\\MIGRATION\\kit\\`). {'OK' if n_files == expected else 'MISMATCH'}.",
     f"- Target size/SHA-256 mismatches: **{len(mism)}**."]
L += [f"  - {m}" for m in mism]
L.append(f"- Done-task sources changed since the hash: **{len(changed_done)}**.")
L += [f"  - {m}" for m in changed_done]
L.append(f"- Active-task sources changed since the hash (expected; their copies are snapshots of before): **{len(changed_active)}**.")
L += [f"  - `{m}`" for m in changed_active]
L.append(f"- Source files not in the manifest (created after Phase 1): **{len(new_files)}**.")
L += [f"  - `{m}`" for m in new_files]
L.append("\nNo source was written, moved or deleted by this script.")
with open(os.path.join(MIG, "VERIFY.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
print("mismatches", len(mism), "count", n_files, expected, "done-changed", len(changed_done),
      "active-changed", len(changed_active), "new", len(new_files))
