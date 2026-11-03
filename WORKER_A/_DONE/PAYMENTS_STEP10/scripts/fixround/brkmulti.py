"""A red step over several files: each changed file put back as at <commit>, each new file removed, the
tests run, everything restored by copy.
Usage: python brkmulti.py <name> <commit> <lane> --changed <files...> --new <files...> --tests <files...>"""
import io, os, shutil, subprocess, sys

APP = 'C:/dev/masaha/app/'
HERE = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]
name, commit, lane = args[0], args[1], args[2]
groups, key = {'--changed': [], '--new': [], '--tests': []}, None
for a in args[3:]:
    if a in groups:
        key = a
    else:
        groups[key].append(a)
files = groups['--changed'] + groups['--new']
baks = {}
for f in files:
    b = os.path.join(HERE, f'bak-{name}-' + f.replace('/', '_'))
    shutil.copyfile(APP + f, b)
    baks[f] = b
try:
    for f in groups['--changed']:
        data = subprocess.run(['git', 'show', f'{commit}:{f}'], cwd=APP, capture_output=True).stdout
        assert data, f
        io.open(APP + f, 'wb').write(data)
    for f in groups['--new']:
        os.remove(APP + f)
    r = subprocess.run(f'npm run test:{lane} -w @masaha/web -- ' + ' '.join(groups['--tests']), cwd=APP,
                       shell=True, capture_output=True, text=True, encoding='utf8')
    out = r.stdout + r.stderr
    io.open(os.path.join(HERE, f'{name}.txt'), 'w', encoding='utf8', newline='').write(out)
    print(f'{name}: exit {r.returncode}')
    for line in out.splitlines():
        if any(k in line for k in ('×', 'Tests ', 'AssertionError', 'Unable to', 'Error:')):
            print('  ', line.strip()[:220])
finally:
    for f, b in baks.items():
        shutil.copyfile(b, APP + f)
    print('  restored', all(io.open(APP + f, 'rb').read() == io.open(b, 'rb').read() for f, b in baks.items()))
