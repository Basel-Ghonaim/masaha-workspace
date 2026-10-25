"""B43, a scratch run: T26 at 70,000 ids (above PostgreSQL's 65,535 parameters) with a 60 s timeout, first with
the code as it is (one array parameter: green), then with the ids bound one parameter each (red). Both files are
backed up, restored and compared by SHA-256; nothing here is committed."""
import hashlib, io, os, re, shutil, subprocess
REPO = r'C:\dev\masaha\app-b'
BK = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'breaks')
TEST = os.path.join(REPO, r'apps\api\src\modules\desk\customers.api.test.ts')
REPO_FILE = os.path.join(REPO, r'apps\api\src\modules\customers\customers.repository.ts')

def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def edit(p, old, new):
    s = io.open(p, encoding='utf-8', newline='').read()
    assert s.count(old) == 1, old
    io.open(p, 'w', encoding='utf-8', newline='').write(s.replace(old, new))
def run():
    p = subprocess.run(['npm', 'exec', '-w', '@masaha/api', '--', 'vitest', 'run', '--project', 'api',
                        'src/modules/desk/customers.api.test.ts', '-t', 'one parameter', '--reporter=verbose'],
                       cwd=REPO, capture_output=True, text=True, encoding='utf-8', errors='replace', shell=True)
    out = re.sub(r'\x1b\[[0-9;]*m', '', p.stdout + p.stderr)
    keep = [l.rstrip() for l in out.splitlines() if re.search(r'one parameter|Tests\s+\d|Error|bind|parameter', l)]
    return p.returncode, '\n'.join(keep[:12])

backups = {}
for p in (TEST, REPO_FILE):
    b = os.path.join(BK, 'B43__' + os.path.basename(p)); shutil.copyfile(p, b); backups[p] = (b, sha(p))
try:
    edit(TEST, 'generate_series(1, 30000) n', 'generate_series(1, 70000) n')
    edit(TEST, 'expect(total(response)).toBe(30_000);\n  });', 'expect(total(response)).toBe(70_000);\n  }, 60_000);')
    code, out = run()
    print(f'== B43 control (70,000 ids, the code as it is) exit {code}\n{out}')
    edit(REPO_FILE, 'Prisma.sql`id IN (SELECT unnest(${[...ids]}::integer[]))`',
         'Prisma.sql`id IN (${Prisma.join([...ids])})`')
    code, out = run()
    print(f'== B43 broken (70,000 ids bound one each) exit {code}\n{out}')
finally:
    for p, (b, h) in backups.items():
        shutil.copyfile(b, p)
        print('restored', os.path.basename(p), 'sha256', 'same' if sha(p) == h else 'DIFFERENT')
