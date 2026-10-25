"""B15 as the plan names it: `userId` added to the repository's select AND the mapper (two files)."""
import hashlib, io, os, re, shutil, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')
REPO = r'C:\dev\masaha\app-b'
BK = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'breaks')
D = os.path.join(REPO, 'apps', 'api', 'src', 'modules', 'data-reports')
EDITS = [
    (os.path.join(D, 'data-reports.repository.ts'), "const REPORT = {\n  id: true,\n", "const REPORT = {\n  id: true,\n  userId: true,\n"),
    (os.path.join(D, 'data-reports.mapper.ts'), "    decision: decisionOf(row),\n  };", "    decision: decisionOf(row),\n    ...{ userId: (row as unknown as { userId: number }).userId },\n  };"),
]
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
def run():
    p = subprocess.run(['npm', 'exec', '-w', '@masaha/api', '--', 'vitest', 'run', '--project', 'api',
                        'src/modules/data-reports/spaceReports.api.test.ts'], cwd=REPO, capture_output=True,
                       text=True, encoding='utf-8', errors='replace', shell=True)
    out = re.sub(r'\x1b\[[0-9;]*m', '', p.stdout + p.stderr)
    return p.returncode, out
before = {}
os.makedirs(BK, exist_ok=True)
for path, old, new in EDITS:
    shutil.copyfile(path, os.path.join(BK, 'B15__' + os.path.basename(path)))
    before[path] = sha(path)
    s = io.open(path, encoding='utf-8', newline='').read()
    assert s.count(old) == 1, path
    io.open(path, 'w', encoding='utf-8', newline='').write(s.replace(old, new))
try:
    code, out = run()
finally:
    for path, _, _ in EDITS:
        shutil.copyfile(os.path.join(BK, 'B15__' + os.path.basename(path)), path)
print(f'== B15 (repository select + mapper) broken run exit {code}')
print('\n'.join(l.rstrip() for l in out.splitlines() if re.search(r'^\s+×|Tests\s+\d|AssertionError', l))[:1500])
print('   restored: sha256', 'same' if all(sha(p) == before[p] for p in before) else 'DIFFERENT')
code2, out2 = run()
print(f'   restored run exit {code2}:', [l.strip() for l in out2.splitlines() if re.search(r'Tests\s+\d', l)][-1:])
