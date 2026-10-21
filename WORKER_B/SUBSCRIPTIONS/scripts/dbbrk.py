"""A database break on masaha_b_test: CREATE OR REPLACE a migration's function with one change, run the
named test file (expect red), restore the migration's own text, compare the function's md5 before and
after, run green. Usage: python dbbrk.py <migration.sql> <id> <old> <new> <test file> [<-t name>]"""
import re, subprocess, sys
REPO = r'C:\dev\masaha\app-b'

def env_user():
    for line in open(REPO + r'\apps\api\.env', encoding='utf-8'):
        if line.startswith('TEST_DATABASE_URL='):
            return re.search(r'//([^:]+):', line).group(1)

USER = env_user()

def psql(sql):
    p = subprocess.run(['docker', 'exec', '-i', 'masaha-postgres-1', 'psql', '-v', 'ON_ERROR_STOP=1', '-U', USER,
                        '-d', 'masaha_b_test', '-tA'], input=sql.encode('utf-8'), capture_output=True)
    # Bytes, not text: on Windows a text pipe would turn the function's LF into CRLF.
    if p.returncode != 0:
        print(p.stderr.decode('utf-8', 'replace')); sys.exit(4)
    return p.stdout.decode('utf-8').strip()

def fn_md5(name):
    return psql(f"SELECT md5(prosrc) FROM pg_proc WHERE proname = '{name}';")

def run(test, name):
    cmd = ['npm', 'exec', '-w', '@masaha/api', '--', 'vitest', 'run', '--project', 'api', test]
    if name:
        cmd += ['-t', name]
    p = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, encoding='utf-8', errors='replace', shell=True)
    out = re.sub(r'\x1b\[[0-9;]*m', '', p.stdout + p.stderr)
    return p.returncode, out

def main():
    if sys.argv[2] == 'RESTORE':
        text = open(sys.argv[1], encoding='utf-8').read()
        m = re.search(r'CREATE (?:OR REPLACE )?FUNCTION "(\w+)".*?\$\$;', text, re.S)
        psql(m.group(0).replace('CREATE FUNCTION', 'CREATE OR REPLACE FUNCTION', 1))
        print('restored', m.group(1), fn_md5(m.group(1)))
        return
    migration, bid, old, new, test = sys.argv[1:6]
    name = sys.argv[6] if len(sys.argv) > 6 else None
    text = open(migration, encoding='utf-8').read()
    m = re.search(r'CREATE (?:OR REPLACE )?FUNCTION "(\w+)".*?\$\$;', text, re.S)
    fn, body = m.group(1), m.group(0)
    original = body.replace('CREATE FUNCTION', 'CREATE OR REPLACE FUNCTION', 1)
    if original.count(old) != 1:
        print(f'== {bid}: old text found {original.count(old)} times'); sys.exit(2)
    before = fn_md5(fn)
    psql(original.replace(old, new))
    try:
        code, out = run(test, name)
    finally:
        psql(original)
    after = fn_md5(fn)
    keep = [l.rstrip() for l in out.splitlines() if re.search(r'^\s+×|Tests\s+\d|AssertionError|Error:', l)]
    print(f'== {bid} ({fn}) broken run exit {code}')
    print('\n'.join(keep[:10]))
    print(f'   restored: md5 {"same" if before == after else "DIFFERENT"}')
    code2, out2 = run(test, name)
    green = [l.strip() for l in out2.splitlines() if re.search(r'Tests\s+\d', l)]
    print(f'   restored run exit {code2}: {green[-1] if green else "?"}')
    if code == 0:
        print(f'   !!! {bid} STAYED GREEN')

main()
