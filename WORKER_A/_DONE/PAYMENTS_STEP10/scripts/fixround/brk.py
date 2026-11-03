"""A red step or a break: back a repository file up, change it, run the given tests, restore by copy.
Usage:
  python brk.py <name> <file> sha <commit> <lane> <test files...>        the file as it was at <commit>
  python brk.py <name> <file> swap <old-text-file> <new-text-file> <lane> <test files...>
<lane> is unit or component. Output in fixround/<name>.txt; prints the failing lines."""
import io, os, shutil, subprocess, sys

APP = 'C:/dev/masaha/app/'
HERE = os.path.dirname(os.path.abspath(__file__))
name, path, how = sys.argv[1], sys.argv[2], sys.argv[3]
if how == 'sha':
    commit, lane, tests = sys.argv[4], sys.argv[5], sys.argv[6:]
else:
    old_file, new_file, lane, tests = sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7:]
src = APP + path
bak = os.path.join(HERE, f'bak-{name}-{os.path.basename(path)}')
shutil.copyfile(src, bak)
try:
    if how == 'sha':
        data = subprocess.run(['git', 'show', f'{commit}:{path}'], cwd=APP, capture_output=True).stdout
        assert data, 'no such file at that commit'
        io.open(src, 'wb').write(data)
    else:
        s = io.open(src, encoding='utf8', newline='').read()
        old = io.open(old_file, encoding='utf8', newline='').read()
        new = io.open(new_file, encoding='utf8', newline='').read()
        assert s.count(old) == 1, f'the old text is found {s.count(old)} times'
        io.open(src, 'w', encoding='utf8', newline='').write(s.replace(old, new))
    r = subprocess.run(f'npm run test:{lane} -w @masaha/web -- ' + ' '.join(tests), cwd=APP, shell=True,
                       capture_output=True, text=True, encoding='utf8')
    out = r.stdout + r.stderr
    io.open(os.path.join(HERE, f'{name}.txt'), 'w', encoding='utf8', newline='').write(out)
    print(f'{name}: exit {r.returncode}')
    for line in out.splitlines():
        if any(k in line for k in ('×', 'Tests ', 'AssertionError', 'Unable to', 'expected ')):
            print('  ', line.strip()[:220])
finally:
    shutil.copyfile(bak, src)
    print('  restored', io.open(src, 'rb').read() == io.open(bak, 'rb').read())
