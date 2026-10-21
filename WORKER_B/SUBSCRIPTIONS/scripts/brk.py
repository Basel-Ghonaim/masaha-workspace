"""One deliberate break: back up, edit, run the named test (expect red), restore from the backup,
check SHA-256, run it again (expect green). Usage: python brk.py <breaks.json> <id> [<id> ...]
Each JSON entry: {"id", "file", "old", "new", "lane": "api"|"unit"|"shared", "test": "<path in workspace>",
"name": optional -t filter}. Prints the red lines and the green line."""
import hashlib, io, json, os, re, shutil, subprocess, sys
REPO = r'C:\dev\masaha\app-b'
BK = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'breaks')

def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def run(e):
    lane = e['lane']
    if lane == 'shared':
        cmd = ['npm', 'exec', '-w', '@masaha/shared', '--', 'vitest', 'run', e['test']]
    else:
        cmd = ['npm', 'exec', '-w', '@masaha/api', '--', 'vitest', 'run', '--project', lane, e['test']]
    if e.get('name'):
        cmd += ['-t', e['name']]
    p = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, encoding='utf-8', errors='replace', shell=True)
    out = re.sub(r'\x1b\[[0-9;]*m', '', p.stdout + p.stderr)
    return p.returncode, out

def summary(out):
    keep = [l.rstrip() for l in out.splitlines()
            if re.search(r'^\s+×|Tests\s+\d|FAIL |AssertionError|Error:|expected', l)]
    return '\n'.join(keep[:14])

def main():
    entries = {e['id']: e for e in json.load(open(sys.argv[1], encoding='utf-8'))}
    for bid in sys.argv[2:]:
        e = entries[bid]
        path = os.path.join(REPO, e['file'])
        os.makedirs(BK, exist_ok=True)
        backup = os.path.join(BK, bid + '__' + os.path.basename(path))
        shutil.copyfile(path, backup)
        before = sha(path)
        s = io.open(path, encoding='utf-8', newline='').read()
        for old, new in e.get('edits') or [[e['old'], e['new']]]:
            if s.count(old) != 1:
                print(f'== {bid}: old text found {s.count(old)} times; nothing changed'); sys.exit(2)
            s = s.replace(old, new)
        io.open(path, 'w', encoding='utf-8', newline='').write(s)
        try:
            code, out = run(e)
        finally:
            shutil.copyfile(backup, path)
        after = sha(path)
        print(f'== {bid} ({e["file"]}) broken run exit {code}')
        print(summary(out))
        print(f'   restored: sha256 {"same" if before == after else "DIFFERENT"}')
        code2, out2 = run(e)
        green = [l.strip() for l in out2.splitlines() if re.search(r'Tests\s+\d', l)]
        print(f'   restored run exit {code2}: {green[-1] if green else "?"}')
        if code == 0:
            print(f'   !!! {bid} STAYED GREEN')
        if before != after or code2 != 0:
            print('   !!! RESTORE PROBLEM'); sys.exit(3)

main()
