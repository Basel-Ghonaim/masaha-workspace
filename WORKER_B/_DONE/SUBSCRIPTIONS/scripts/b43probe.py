"""Scratch: T26 at 70,000 ids with a 60 s timeout, run in the background while pg_stat_activity is sampled, to
find which statement runs long. The test file is restored from its backup and compared by SHA-256."""
import hashlib, io, os, re, shutil, subprocess, time
REPO = r'C:\dev\masaha\app-b'
TEST = os.path.join(REPO, r'apps\api\src\modules\desk\customers.api.test.ts')
BK = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'breaks', 'probe__customers.api.test.ts')
USER = next(re.search(r'//([^:]+):', l).group(1) for l in open(REPO + r'\apps\api\.env', encoding='utf-8')
            if l.startswith('TEST_DATABASE_URL='))
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def edit(old, new):
    s = io.open(TEST, encoding='utf-8', newline='').read(); assert s.count(old) == 1
    io.open(TEST, 'w', encoding='utf-8', newline='').write(s.replace(old, new))
shutil.copyfile(TEST, BK); before = sha(TEST)
try:
    edit('generate_series(1, 30000) n', 'generate_series(1, 70000) n')
    edit('expect(total(response)).toBe(30_000);\n  });', 'expect(total(response)).toBe(70_000);\n  }, 60_000);')
    proc = subprocess.Popen(['npm', 'exec', '-w', '@masaha/api', '--', 'vitest', 'run', '--project', 'api',
                             'src/modules/desk/customers.api.test.ts', '-t', 'one parameter'], cwd=REPO,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    for _ in range(12):
        time.sleep(5)
        out = subprocess.run(['docker', 'exec', 'masaha-postgres-1', 'psql', '-U', USER, '-d', 'masaha_b_test', '-tAc',
                              "SELECT round(extract(epoch FROM now()-query_start))::int || 's | ' || "
                              "regexp_replace(left(query, 400), '\\s+', ' ', 'g') FROM pg_stat_activity "
                              "WHERE datname = 'masaha_b_test' AND state = 'active' AND pid <> pg_backend_pid()"],
                             capture_output=True, text=True, encoding='utf-8').stdout.strip()
        if out:
            print(out); print('---')
        if proc.poll() is not None:
            break
    proc.wait()
finally:
    shutil.copyfile(BK, TEST)
    print('restored sha256', 'same' if sha(TEST) == before else 'DIFFERENT')
