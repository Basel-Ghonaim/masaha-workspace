"""Phase 1: list every source file, apply the placement rules, write manifest.csv and MAPPING.md.
Reads sources only; writes only under D:\\masahaWorkspace\\_SHARED\\MIGRATION."""
import csv, hashlib, os, re, sys
from collections import Counter, defaultdict

ROOT = r"D:\masahaWorkspace"
MIG = os.path.join(ROOT, "_SHARED", "MIGRATION")
S1 = r"C:\Users\basel\.prompt"
S2 = r"C:\Users\basel\Downloads\masaha-next"
S3 = r"C:\Users\basel\Downloads\masaha-handoffs"
S4 = r"C:\Users\basel\Downloads\masaha-prompts-archive-2026-10-08"
DL = r"C:\Users\basel\Downloads"

ACTIVE = {("WORKER_A", "GALLERY"), ("WORKER_B", "HARDEN"), ("DESIGN", "ROUND2")}
GROUP_OF = {"MASAHA_WORKER_A": "WORKER_A", "MASAHA_WORKER_B": "WORKER_B", "MASAHA_DESIGN": "DESIGN"}
SUFFIXES = sorted([
    "_PROMPT", "_PLAN", "_PLAN_REPLY", "_REPORT", "_FIXES", "_FIXES2", "_EXEC", "_ADDITION", "_ADDITION2",
    "_BUILD", "_SHOTS_REPLY", "_BROWSER_REPORT", "_BROWSER_ROUND2_REPORT", "_PR_BODY", "_REPORT_PART1",
    "_FIXES_REPORT", "-copilot-draft"], key=len, reverse=True)

# R4: PR number -> (group, task, evidence file (relative to S1), regex that finds the line)
PR = {
    50: ("WORKER_A", "S2B3A", r"MASAHA_WORKER_A\REPORT\S2B3A_FIXES_REPORT.md", r"PR #50"),
    57: ("WORKER_A", "S2B3B", r"MASAHA_WORKER_A\REPORT\S2B3B_REPORT.md", r"PR #57"),
    60: ("WORKER_B", "OWNERS", r"MASAHA_WORKER_B\REPORT\OWNERS_REPORT.md", r"pull/60"),
    62: ("WORKER_B", "USERS", r"MASAHA_WORKER_B\REPORT\USERS_REPORT.md", r"pull/62"),
    67: ("WORKER_B", "DELETED", r"MASAHA_WORKER_B\REPORT\DELETED_REPORT.md", r"pull/67"),
    68: ("WORKER_A", "WEBBASE", r"MASAHA_WORKER_A\REPORT\WEBBASE_REPORT.md", r"pull/68"),
    73: ("WORKER_B", "DIRECTORY", r"MASAHA_WORKER_B\REPORT\DIRECTORY_REPORT.md", r"pull/73"),
    74: ("WORKER_A", "S2B4A", r"MASAHA_WORKER_A\REPORT\S2B4A_REPORT.md", r"pull/74"),
    75: ("DESIGN", "FIX_ACCOUNT", r"MASAHA_DESIGN\REPORT\FIX_ACCOUNT_REPORT.md", r"pull/75"),
    76: ("DESIGN", "FIX_OWNER", r"MASAHA_DESIGN\REPORT\FIX_OWNER_REPORT.md", r"PR:\*\* #76"),
    78: ("WORKER_B", "SESSIONS", r"MASAHA_WORKER_B\REPORT\SESSIONS_REPORT.md", r"PR #78"),
    79: ("WORKER_A", "S2B4B", r"MASAHA_WORKER_A\REPORT\S2B4B_REPORT.md", r"\*\*#79\*\*"),
    82: ("WORKER_B", "OWNERSREAD", r"MASAHA_WORKER_B\REPORT\OWNERSREAD_REPORT.md", r"pull/82"),
    83: ("WORKER_B", "MANAGE", r"MASAHA_WORKER_B\REPORT\REVIEW_MANAGE_CODEX_REPORT.md", r"PR #83"),
    86: ("WORKER_B", "HARDEN", r"MASAHA_WORKER_B\REPORT\REVIEW86_OPENCODE_REPORT.md", r"PR #86, HARDEN"),
    84: ("WORKER_A", "ADMINLIST", r"MASAHA_WORKER_A\REPORT\ADMINLIST_REPORT.md", r"pull/84"),
}
# REVIEW_<X>_* in MASAHA_DESIGN -> FIX_<X>; evidence: FIX_<X>_PROMPT names REVIEW_<X>_REPORT
DESIGN_REVIEW = {"ACCOUNT": "FIX_ACCOUNT", "OWNER": "FIX_OWNER", "DESK": "FIX_DESK",
                 "PUBLIC": "FIX_PUBLIC", "SHARED": "FIX_SHARED"}

# R6: shots folder -> (group-or-path, task, evidence)
SHOTS = {
    "adminlist-shots": ("WORKER_A", "ADMINLIST", "ADMINLIST_PLAN/PROMPT/REPORT name it"),
    "gallery-shots": ("WORKER_A", "GALLERY", "GALLERY_PLAN/REPORT name it"),
    "media-shots": ("TASKS", "MEDIA", "MEDIA_REPORT names it"),
    "amenities-shots": ("TASKS", "AMENITIES", "AMENITIES_PLAN/PROMPT/REPORT name it"),
    "r2-shots": ("DESIGN", "ROUND2", "ROUND2 prompts/reports and ROUND2_GENERATOR_PROMPT name it"),
    "s2b3a-shots": ("WORKER_A", "S2B3A", "S2B3A_PROMPT names it"),
    "s2b3b-shots": ("WORKER_A", "S2B3B", "S2B3B_PLAN/PROMPT/REPORT name it"),
    "s2b4a-shots": ("WORKER_A", "S2B4A", "S2B4A_PLAN/PROMPT/REPORT name it"),
    "s2b4b-shots": ("WORKER_A", "S2B4B", "S2B4B_PLAN/PROMPT/REPORT name it"),
    "webbase-shots": ("WORKER_A", "WEBBASE", "WEBBASE_PLAN/PROMPT/REPORT name it"),
    "pr59-shots": ("DESIGN", "FIX_SHARED", "SHOTS59_PROMPT names it; FIX_SHARED_REPORT names design/shared and #59 (owner ruling 5)"),
    "review-desk-shots": ("DESIGN", "FIX_DESK", "REVIEW_DESK_BUILD_PROMPT / REVIEW_DESK_OPENCODE_REPORT name it; REVIEW_DESK -> FIX_DESK"),
}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def walk(base):
    for d, _, fs in os.walk(base):
        for f in fs:
            yield os.path.join(d, f)


def first_line(rel, rx):
    try:
        with open(os.path.join(S1, rel), encoding="utf-8", errors="replace") as f:
            for ln in f:
                if re.search(rx, ln):
                    return f"{rel}: {ln.strip()[:120]}"
    except OSError:
        pass
    return f"{rel}: (no line matched {rx})"


def stem_task(name):
    s = name
    for suf in SUFFIXES:
        # suffix sits before the extension (or right before -copilot-draft's extension)
        base, ext = os.path.splitext(s)
        if base.endswith(suf) and len(base) > len(suf):
            return base[: -len(suf)]
    return os.path.splitext(s)[0]


def task_dir(group, task):
    if group == "TASKS":
        return os.path.join("TASKS", "_DONE", task)
    if (group, task) in ACTIVE:
        return os.path.join(group, task)
    return os.path.join(group, "_DONE", task)


OVERRIDE = {
    "ROUND2_GENERATOR_PROMPT.md": ("DESIGN", "ROUND2", "owner ruling 3: belongs with ROUND2"),
    "desk-scratch-reference.diff": ("DESIGN", "FIX_DESK", "owner ruling 3"),
    "FIX_SHARED_REVIEW_LINKS.md": ("DESIGN", "FIX_SHARED", "owner ruling 4"),
    "SHOTS59_PROMPT.md": ("DESIGN", "FIX_SHARED", "owner ruling 5: FIX_SHARED_REPORT line 4 names PR #59; its plan/report name branch design/shared"),
    "REVIEW_ADMIN_PROMPT.md": ("DESIGN", "REVIEW_ADMIN", "owner ruling 2: own task; the review behind FIX_ADMIN_EDITOR and FIX_ADMIN_REST"),
    "REVIEW_ADMIN_REPORT.md": ("DESIGN", "REVIEW_ADMIN", "owner ruling 2: own task; the review behind FIX_ADMIN_EDITOR and FIX_ADMIN_REST"),
}


def place_s1(rel):
    parts = rel.split("\\")
    name = parts[-1]
    if name in OVERRIDE and len(parts) >= 2 and parts[0] == "MASAHA_DESIGN" and parts[1] in ("PLAN", "PROMPT", "REPORT"):
        g, t, ev = OVERRIDE[name]
        return os.path.join(task_dir(g, t), name), "R1/owner", ev
    if len(parts) == 1 and name == "HANDOFF.md":
        return "HANDOFF.md", "R7", "S1 HANDOFF.md"
    top = parts[0]
    if top in ("MASAHA_AMENITIES", "MASAHA_MEDIA"):
        t = "AMENITIES" if top == "MASAHA_AMENITIES" else "MEDIA"
        ev = ""
        m = re.match(r"REVIEW(\d+)", name)
        if m:
            ev = f"REVIEW{m.group(1)} sits in {top}; R3 by folder"
        return os.path.join("TASKS", "_DONE", t, name), "R3", ev
    if top == "MASAHA_DESIGN":
        if len(parts) == 2 and (name.startswith("DECISIONS_") or name == "REVIEW_LENS.md"):
            return os.path.join("DESIGN", "DECISIONS", name), "R2", ""
        if parts[1] == "ROUND2":
            return os.path.join("DESIGN", "ROUND2", *parts[2:]), "R2", ""
    if top in GROUP_OF and len(parts) == 3 and parts[1] in ("PLAN", "PROMPT", "REPORT", "files"):
        group = GROUP_OF[top]
        if name.startswith("REVIEW"):
            m = re.match(r"REVIEW(\d+)", name)
            if m and "-" not in name[len("REVIEW"):len("REVIEW") + 8].split("_")[0]:
                n = int(m.group(1))
                if n in PR:
                    g, t, evf, rx = PR[n]
                    return os.path.join(task_dir(g, t), name), "R4", f"PR #{n} -> {t}; " + first_line(evf, rx)
                return os.path.join("_SHARED", "UNSORTED", "S1", rel), "R7", f"REVIEW{n}: no PR evidence"
            if name.startswith("REVIEW82-83_"):
                ev = first_line(PR[83][2], PR[83][3])
                return os.path.join(task_dir("WORKER_B", "MANAGE"), name), "R4", "covers #82 and #83; later of the two -> MANAGE; " + ev
            if name.startswith("REVIEW_MANAGE_"):
                return os.path.join(task_dir("WORKER_B", "MANAGE"), name), "R4", "REVIEW_MANAGE_* -> MANAGE (PR #83): " + first_line(PR[83][2], PR[83][3])
            m = re.match(r"REVIEW_([A-Z]+)(_|\.)", name)
            if top == "MASAHA_DESIGN" and m:
                x = m.group(1)
                if x in DESIGN_REVIEW:
                    t = DESIGN_REVIEW[x]
                    return (os.path.join(task_dir("DESIGN", t), name), "R4",
                            first_line(rf"MASAHA_DESIGN\PROMPT\{t}_PROMPT.md", rf"REVIEW_{x}_REPORT"))
                return (os.path.join("_SHARED", "UNSORTED", "S1", rel), "R7",
                        f"REVIEW_{x}: FIX_ADMIN_EDITOR and FIX_ADMIN_REST both cite REVIEW_ADMIN_REPORT as 'the review behind them'; no evidence picks one")
            return os.path.join("_SHARED", "UNSORTED", "S1", rel), "R7", "REVIEW* name matches no R4 pattern"
        t = stem_task(name)
        return os.path.join(task_dir(group, t), name), "R1", ""
    return os.path.join("_SHARED", "UNSORTED", "S1", rel), "R7", ""


def place_s2(rel):
    parts = rel.split("\\")
    if len(parts) == 1:
        return os.path.join("_SHARED", "MAP_AR.md"), "R7", "S2 MAP_AR.md -> _SHARED\\MAP_AR.md (layout §2)"
    top = parts[0]
    if top == "WORKSPACE":
        return os.path.join("_SHARED", "MIGRATION", "kit", *parts[1:]), "R5", ""
    m = re.match(r"([AB])_(.+)$", top)
    if m:
        g = "WORKER_A" if m.group(1) == "A" else "WORKER_B"
        return os.path.join(task_dir(g, m.group(2)), "kit", *parts[1:]), "R5", ""
    return os.path.join("_SHARED", "UNSORTED", "S2", rel), "R7", ""


def main():
    if os.path.isdir(ROOT):
        extra = [e for e in os.listdir(ROOT) if e != "_SHARED"]
        sh = [e for e in os.listdir(os.path.join(ROOT, "_SHARED")) if e != "MIGRATION"]
        if extra or sh:
            sys.exit(f"target not empty: {extra} {sh}")
    rows = []

    def add(src, tgt, rule, ev):
        rows.append([src, os.path.getsize(src), sha(src), os.path.join(ROOT, tgt), rule, ev])

    for p in walk(S1):
        rel = os.path.relpath(p, S1)
        t, r, e = place_s1(rel); add(p, t, r, e)
    for p in walk(S2):
        rel = os.path.relpath(p, S2)
        t, r, e = place_s2(rel); add(p, t, r, e)
    for p in walk(S3):
        add(p, os.path.join("_SHARED", "HANDOFFS", os.path.relpath(p, S3)), "R7", "S3 as it is")
    for p in walk(S4):
        add(p, os.path.join("_SHARED", "ARCHIVE_2026-10-08", os.path.relpath(p, S4)), "R7", "S4 as it is")
    for d in sorted(os.listdir(DL)):
        full = os.path.join(DL, d)
        if os.path.isdir(full) and d.endswith("-shots"):
            for p in walk(full):
                rel = os.path.relpath(p, full)
                if d in SHOTS:
                    g, t, ev = SHOTS[d]
                    add(p, os.path.join(task_dir(g, t), "shots", d, rel), "R6", ev)
                else:
                    add(p, os.path.join("_SHARED", "ARCHIVE_2026-10-08", "shots", d, rel), "R6/owner", "owner ruling 1: folder dated 2026-09-28..2026-10-07, before the 2026-10-08 archive")

    # checks
    problems = []
    srcs = Counter(r[0] for r in rows)
    tgts = Counter(r[3].lower() for r in rows)
    problems += [f"dup source {k}" for k, v in srcs.items() if v > 1]
    problems += [f"dup target {k}" for k, v in tgts.items() if v > 1]
    for r in rows:
        if not os.path.abspath(r[3]).startswith(ROOT + os.sep):
            problems.append(f"outside root {r[3]}")
        if len(r[3]) >= 240:
            problems.append(f"long path ({len(r[3])}) {r[3]}")
        for pre in (r"C:\Users\basel\masaha", ):
            if r[0].startswith(pre + "\\") or r[0].startswith(pre + "-"):
                problems.append(f"repo source {r[0]}")

    with open(os.path.join(MIG, "manifest.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["source", "size", "sha256", "target", "rule", "evidence"])
        w.writerows(rows)

    # MAPPING.md
    def sk(src):
        for k, b in (("S1", S1), ("S2", S2), ("S3", S3), ("S4", S4)):
            if src.startswith(b + "\\"):
                return k
        return "S5"
    per_src = Counter(sk(r[0]) for r in rows)
    bytes_src = defaultdict(int)
    for r in rows:
        bytes_src[sk(r[0])] += r[1]
    per_dir = Counter()
    tasks = defaultdict(lambda: [0, set()])
    for r in rows:
        rel = os.path.relpath(r[3], ROOT).split("\\")
        if rel[0] in ("WORKER_A", "WORKER_B", "DESIGN") and len(rel) > 2:
            key = rel[:3] if rel[1] == "_DONE" else rel[:2]
            if rel[0] == "DESIGN" and rel[1] == "DECISIONS":
                key = rel[:2]
        elif rel[0] == "TASKS":
            key = rel[:3]
        else:
            key = rel[:2] if len(rel) > 2 else rel[:1]
        per_dir["\\".join(key)] += 1
    L = []
    L.append("# MAPPING — Phase 1 plan\n")
    L.append(f"Total files: **{len(rows)}**, bytes: **{sum(r[1] for r in rows):,}**.\n")
    L.append("## Per source key\n\n| key | files | bytes |\n|---|---|---|")
    for k in ("S1", "S2", "S3", "S4", "S5"):
        L.append(f"| {k} | {per_src[k]} | {bytes_src[k]:,} |")
    L.append("\n## Per target folder\n\n| folder | files |\n|---|---|")
    for k, v in sorted(per_dir.items()):
        L.append(f"| `{k}` | {v} |")
    # task list
    task_pr = {}
    for n, (g, t, *_ ) in PR.items():
        task_pr.setdefault((g, t), []).append(n)
    known_prs = {  # from the reports (grep lines), main PR of each task
        ("WORKER_A", "ADMINLIST"): [84], ("WORKER_A", "S2B3A"): [50], ("WORKER_A", "S2B3B"): [57],
        ("WORKER_A", "S2B4A"): [74], ("WORKER_A", "S2B4B"): [79], ("WORKER_A", "WEBBASE"): [68],
        ("WORKER_B", "OWNERS"): [60], ("WORKER_B", "USERS"): [62], ("WORKER_B", "DELETED"): [67],
        ("WORKER_B", "DIRECTORY"): [73], ("WORKER_B", "SESSIONS"): [78], ("WORKER_B", "OWNERSREAD"): [82],
        ("WORKER_B", "MANAGE"): [83], ("WORKER_B", "HARDEN"): [86], ("DESIGN", "FIX_ACCOUNT"): [75], ("DESIGN", "FIX_OWNER"): [76], ("DESIGN", "FIX_SHARED"): [59],
        ("DESIGN", "FIX_ADMIN_EDITOR"): [61], ("DESIGN", "FIX_ADMIN_REST"): [66], ("DESIGN", "FIX_PUBLIC"): [65], ("DESIGN", "FIX_DESK"): [80],
        ("TASKS", "AMENITIES"): [64], ("TASKS", "MEDIA"): [77],
    }
    seen = set()
    for r in rows:
        rel = os.path.relpath(r[3], ROOT).split("\\")
        if rel[0] in ("WORKER_A", "WORKER_B", "DESIGN") and rel[1] != "DECISIONS" and len(rel) >= 3:
            t = rel[2] if rel[1] == "_DONE" else rel[1]
            seen.add((rel[0], t, "done" if rel[1] == "_DONE" else "active"))
        elif rel[0] == "TASKS":
            seen.add(("TASKS", rel[2], "done"))
    L.append("\n## Task list\n\n| group | task | state | PR(s) | files |\n|---|---|---|---|---|")
    cnt = Counter()
    for r in rows:
        rel = os.path.relpath(r[3], ROOT).split("\\")
        if rel[0] in ("WORKER_A", "WORKER_B", "DESIGN") and rel[1] != "DECISIONS" and len(rel) >= 3:
            cnt[(rel[0], rel[2] if rel[1] == "_DONE" else rel[1])] += 1
        elif rel[0] == "TASKS":
            cnt[("TASKS", rel[2])] += 1
    for g, t, st in sorted(seen):
        prs = ", ".join(f"#{n}" for n in known_prs.get((g, t), [])) or "unknown"
        L.append(f"| {g} | {t} | {st} | {prs} | {cnt[(g, t)]} |")
    L.append("\nPRs for AMENITIES (#64) and MEDIA (#77) come from their folders' REVIEW64/REVIEW77 files and reports. "
             "HARDEN's #86 (`fix/space-api-hardening`, still open) is named by REVIEW86_OPENCODE_REPORT.md and confirmed with `gh pr view 86`. GALLERY and ROUND2 have no merged PR yet.\n")
    uns = [r for r in rows if r[3].startswith(os.path.join(ROOT, "_SHARED", "UNSORTED"))]
    L.append(f"\n## UNSORTED — {len(uns)} files\n")
    byfolder = Counter()
    for r in uns:
        rel = os.path.relpath(r[3], os.path.join(ROOT, "_SHARED", "UNSORTED")).split("\\")
        byfolder["\\".join(rel[:2] if rel[0] == "S5" else rel[:1])] += 1
    for k, v in sorted(byfolder.items()):
        L.append(f"- `{k}`: {v}")
    L.append("\nS1/S2 files in UNSORTED, and why:\n")
    for r in uns:
        if "\\S5\\" not in r[3]:
            L.append(f"- `{os.path.relpath(r[0], S1)}` — {r[5]}")
    L.append("\n## R4 decisions (evidence)\n")
    for r in rows:
        if r[4] == "R4":
            L.append(f"- `{os.path.basename(r[0])}` -> `{os.path.relpath(r[3], ROOT)}` — {r[5]}")
    L.append("\n## R6 decisions\n")
    seen_s = set()
    for r in rows:
        if r[4].startswith("R6"):
            d = os.path.relpath(r[0], DL).split("\\")[0]
            if d not in seen_s:
                seen_s.add(d)
                L.append(f"- `{d}` -> `{os.path.relpath(r[3], ROOT).split('shots')[0]}shots\\{d}` — {r[5]}" if r[4] == "R6"
                         else f"- `{d}` -> `_SHARED\\UNSORTED\\S5\\{d}` — {r[5]}")
    L.append("\n## PR evidence for the FIX_* tasks (gh pr list --state merged --limit 100, branch design/<part>)\n")
    for t, br, n, ti in (("FIX_SHARED", "design/shared", 59, "design: apply the shared layer's decisions"),
                         ("FIX_ADMIN_EDITOR", "design/admin-editor", 61, "design: the admin's space editor"),
                         ("FIX_ADMIN_REST", "design/admin-rest", 66, "design: the rest of the admin's dashboard"),
                         ("FIX_PUBLIC", "design/public", 65, "design: the public site"),
                         ("FIX_ACCOUNT", "design/account", 75, "design: the account and signing in"),
                         ("FIX_OWNER", "design/owner", 76, "design: the owner's management"),
                         ("FIX_DESK", "design/desk", 80, "design: the front desk")):
        L.append(f"- {t}: #{n} `{br}` \"{ti}\"")
    L.append("- GALLERY (feat/space-gallery) and ROUND2: no merged PR matches; PR left blank. HARDEN: #86 is open, not merged. REVIEW_ADMIN has no PR of its own (the review behind FIX_ADMIN_EDITOR #61 and FIX_ADMIN_REST #66).")
    L.append("- `pr59-shots` and `SHOTS59_PROMPT.md` joined FIX_SHARED: FIX_SHARED_PLAN/REPORT name `design/shared`; the report names PR #59.")
    L.append("- The 14 shots folders no report names (ds1, f10, f5b2, f5b3a, f5b3b, f5b3c2, f6b, f6c2, s2a2, s2a3, wi-f5b3c1, wi7, wi8, wi9) go whole to `_SHARED\\ARCHIVE_2026-10-08\\shots\\<folder>\\`: owner ruling, they are dated 2026-09-28 to 2026-10-07, before the archive. README.md will say so.")
    L.append("\n## Unsure\n")
    L.append("- FIX_ADMIN_EDITOR (#61) and FIX_ADMIN_REST (#66) are matched by branch name only; their reports were not checked for the PR.")
    L.append("- AMENITIES (#64) and MEDIA (#77): numbers come from the REVIEW64/REVIEW77 file names; the gh list agrees (feat/space-own-amenities, feat/space-photos).")
    L.append("\n## Check results\n")
    L.append("- every source file has exactly one row; no shared targets; no target outside `D:\\masahaWorkspace`; all target paths < 240 chars"
             if not problems else "- PROBLEMS:\n" + "\n".join(f"  - {p}" for p in problems))
    L.append(f"- longest target path: {max(len(r[3]) for r in rows)} chars")
    with open(os.path.join(MIG, "MAPPING.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print(len(rows), sum(r[1] for r in rows), "problems:", problems[:10], "unsorted:", len(uns))


main()
