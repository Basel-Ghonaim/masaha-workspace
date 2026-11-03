"""Runs §10's breaks: for each, a backup copy, the change, the named test file, the output kept, the file restored from the copy.

Usage: python breaks.py <set> [<break id> ...]   (run from anywhere; paths are apps/web-relative)
Each break's output is scripts/break-<id>.txt; a summary line per break is printed: RED / GREEN (not red) and the exit code.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

WEB = Path("C:/dev/masaha/app/apps/web")
SCRIPTS = Path("C:/dev/masaha/workspace/WORKER_A/PAYMENTS_STEP10/scripts")
SETS = json.loads((SCRIPTS / "breaks.json").read_text(encoding="utf-8"))


def run(brk):
    target = WEB / brk["file"]
    backup = SCRIPTS / f"bak-break-{brk['id']}{target.suffix}"
    shutil.copyfile(target, backup)
    try:
        text = target.read_text(encoding="utf-8")
        for old, new in brk["edits"]:
            if text.count(old) != 1:
                return f"{brk['id']}: SETUP FAILED — the text to break occurs {text.count(old)} times"
            text = text.replace(old, new)
        target.write_bytes(text.encode("utf-8"))
        result = subprocess.run(
            f"npx vitest run --project {brk['lane']} {brk['test']}",
            cwd=WEB, shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace",
            env={**os.environ, **brk.get("env", {})},
        )
        out = result.stdout + result.stderr
        (SCRIPTS / f"break-{brk['id']}.txt").write_text(out, encoding="utf-8")
        failing = [line.strip() for line in out.splitlines() if line.strip().startswith(("×", "FAIL"))]
        state = "RED" if result.returncode != 0 else "GREEN (not red)"
        return f"{brk['id']}: {state} exit {result.returncode} — {failing[:3]}"
    finally:
        shutil.copyfile(backup, target)


def main():
    name, ids = sys.argv[1], sys.argv[2:]
    for brk in SETS[name]:
        if ids and brk["id"] not in ids:
            continue
        print(run(brk), flush=True)
    status = subprocess.run("git status --short", cwd=WEB, shell=True, capture_output=True, text=True)
    print("git status after restore:\n" + status.stdout)


main()
