"""Breaks from backup copies: `python brk.py <spec.json> [ids...]`.

Each break: copy the file to bak-break-<id>.<ext>, replace `old` by `new` (once, must exist), run its
test command from the worktree into break-<id>.txt, then copy the backup back. Prints each exit code.
"""
import json
import os
import shutil
import subprocess
import sys

WT = r'C:\dev\masaha\app-lane-c'
HERE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(HERE, sys.argv[1]), encoding='utf8') as f:
    breaks = json.load(f)
only = set(sys.argv[2:])
for item in breaks:
    if only and item['id'] not in only:
        continue
    path = os.path.join(WT, item['file'])
    backup = os.path.join(HERE, f"bak-break-{item['id']}{os.path.splitext(path)[1]}")
    shutil.copy2(path, backup)
    try:
        with open(path, encoding='utf8', newline='') as f:
            text = f.read()
        if text.count(item['old']) != 1:
            print(item['id'], 'ANCHOR', text.count(item['old']))
            continue
        with open(path, 'w', encoding='utf8', newline='') as f:
            f.write(text.replace(item['old'], item['new'], 1))
        out = os.path.join(HERE, f"break-{item['id']}.txt")
        with open(out, 'w', encoding='utf8') as f:
            code = subprocess.run(item['cmd'], cwd=WT, shell=True, stdout=f, stderr=subprocess.STDOUT).returncode
        print(item['id'], 'exit', code)
    finally:
        shutil.copy2(backup, path)
