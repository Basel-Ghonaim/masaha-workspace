"""One break: back up a file, make one exact edit, run a test file in its lane, restore, verify.

Usage: python brk.py <spec.json>
spec: {"name": str, "edits": [{"file": rel, "old": str, "new": str}], "cwd": rel, "cmd": [..]}
Paths relative to C:/dev/masaha/app-b. Prints the result lines; exit 0 when the run was red.
"""
import hashlib, io, json, os, re, shutil, subprocess, sys

ROOT = 'C:/dev/masaha/app-b'
BACKUP = os.path.join(os.environ.get('TEMP', '.'), 'desk-breaks')


def sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def main():
    specs = json.load(io.open(sys.argv[1], encoding='utf-8'))
    only = sys.argv[2:]
    worst = 0
    for spec in specs if isinstance(specs, list) else [specs]:
        if only and not any(spec['name'].startswith(o) for o in only):
            continue
        code = one(spec)
        print('  -> ' + ('RED' if code == 0 else 'NOT RED' if code == 1 else 'NOT MADE'))
        worst = max(worst, code)
    return worst


def one(spec):
    os.makedirs(BACKUP, exist_ok=True)
    saved = []
    try:
        for edit in spec['edits']:
            path = os.path.join(ROOT, edit['file'])
            if path not in [p for p, _, _ in saved]:
                copy = os.path.join(BACKUP, os.path.basename(path) + '.bak')
                shutil.copyfile(path, copy)
                saved.append((path, copy, sha(path)))
            text = io.open(path, encoding='utf-8', newline='').read()
            n = text.count(edit['old'])
            if n != 1:
                print(f'EDIT NOT APPLIED ({n} matches) in {edit["file"]}: {edit["old"][:80]!r}')
                return 2
            io.open(path, 'w', encoding='utf-8', newline='').write(text.replace(edit['old'], edit['new']))
        run = subprocess.run(spec['cmd'], cwd=os.path.join(ROOT, spec.get('cwd', '.')),
                             capture_output=True, text=True, encoding='utf-8', errors='replace',
                             shell=True)
        out = re.sub(r'\x1b\[[0-9;]*m', '', run.stdout + run.stderr)
        lines = [l for l in out.splitlines()
                 if re.search(r'Tests  |Test Files|AssertionError|Error:|EDIT', l)]
        print(f'== {spec["name"]}: exit {run.returncode}')
        for l in lines[:12]:
            print('  ' + l.strip())
        return 0 if run.returncode != 0 else 1
    finally:
        for path, copy, digest in saved:
            shutil.copyfile(copy, path)
            ok = sha(path) == digest
            print(f'  restored {os.path.relpath(path, ROOT)}: {"sha ok" if ok else "SHA MISMATCH"}')


if __name__ == '__main__':
    sys.exit(main())
