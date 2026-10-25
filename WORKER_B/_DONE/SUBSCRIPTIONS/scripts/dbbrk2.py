"""A database break on masaha_b_test: run the break SQL, run the named test (expect red), run the restore SQL
(the migration's own statements), check the schema's fingerprint is back, run green.
Usage: python dbbrk2.py <cases.json> <id>"""
import json, re, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')
REPO = r'C:\dev\masaha\app-b'

def env_user():
    for line in open(REPO + r'\apps\api\.env', encoding='utf-8'):
        if line.startswith('TEST_DATABASE_URL='):
            return re.search(r'//([^:]+):', line).group(1)
USER = env_user()

def psql(sql, db='masaha_b_test'):
    p = subprocess.run(['docker', 'exec', '-i', 'masaha-postgres-1', 'psql', '-v', 'ON_ERROR_STOP=1', '-U', USER,
                        '-d', db, '-tA'], input=sql.encode('utf-8'), capture_output=True)
    if p.returncode != 0:
        print('PSQL ERROR', p.stderr.decode('utf-8', 'replace')); sys.exit(4)
    return p.stdout.decode('utf-8').strip()

FINGERPRINT = """SELECT md5(string_agg(x, '|' ORDER BY x)) FROM (
  SELECT conname || ':' || pg_get_constraintdef(oid) AS x FROM pg_constraint
    WHERE conrelid IN ('subscriptions'::regclass, 'packages'::regclass, 'payments'::regclass)
  UNION ALL SELECT indexname || ':' || indexdef FROM pg_indexes WHERE tablename IN ('subscriptions', 'visits', 'payments')
  UNION ALL SELECT tgname || ':' || pg_get_triggerdef(t.oid) FROM pg_trigger t WHERE NOT tgisinternal
  UNION ALL SELECT proname || ':' || md5(prosrc) FROM pg_proc WHERE proname IN ('subscriptions_guard_price', 'payments_guard_insert')
) s;"""

def run(test, name):
    cmd = ['npm', 'exec', '-w', '@masaha/api', '--', 'vitest', 'run', '--project', 'api', test]
    if name:
        cmd += ['-t', name]
    p = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, encoding='utf-8', errors='replace', shell=True)
    out = re.sub(r'\x1b\[[0-9;]*m', '', p.stdout + p.stderr)
    lines = [l for l in out.splitlines() if re.search(r'Tests |AssertionError|Error:|expected|×', l)]
    return p.returncode, lines

case = json.load(open(sys.argv[1], encoding='utf-8'))[sys.argv[2]]
before = psql(FINGERPRINT)
print(f"[{sys.argv[2]}] test == dev before: {before == psql(FINGERPRINT, 'masaha_b_dev')}")
psql(case['break'])
code, lines = run(case['test'], case.get('name'))
print(f"[{sys.argv[2]}] BROKEN exit {code}")
for l in lines[:8]: print('   ', l.strip()[:220])
# A broken test may leave rows a restored unique index refuses; the lane resets the database before every test.
if case.get('clean'): psql('TRUNCATE subscriptions CASCADE;')
psql(case['restore'])
after = psql(FINGERPRINT)
print(f"[{sys.argv[2]}] fingerprint restored: {before == after}")
code2, lines2 = run(case['test'], case.get('name'))
print(f"[{sys.argv[2]}] RESTORED exit {code2}", [l.strip() for l in lines2 if 'Tests ' in l])
