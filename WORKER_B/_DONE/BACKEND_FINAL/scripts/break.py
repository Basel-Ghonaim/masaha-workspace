# usage: python break.py <tag> <file> <old1> <new1> [<old2> <new2> ...] -- <test files...>
import sys; sys.stdout.reconfigure(encoding="utf-8")
# Backs the file up, makes the edits (each old must occur once), runs the tests, restores by copy.
import sys, shutil, subprocess, os
tag, path, *rest = sys.argv[1:]
cut = rest.index('--')
pairs, tests = rest[:cut], rest[cut + 1:]
S = os.path.dirname(os.path.abspath(__file__))
bak = os.path.join(S, f'bak-{tag}')
shutil.copyfile(path, bak)
src = open(path, encoding='utf-8', newline='').read()
out_src = src
for i in range(0, len(pairs), 2):
    old, new = pairs[i], pairs[i + 1]
    assert out_src.count(old) == 1, f'old #{i//2} found {out_src.count(old)} times'
    out_src = out_src.replace(old, new)
open(path, 'w', encoding='utf-8', newline='').write(out_src)
lane = os.environ.get('LANE_CMD', 'test:api')
ws = os.environ.get('LANE_WS', '@masaha/api')
try:
    r = subprocess.run(f'npm run {lane} -w {ws} -- ' + ' '.join(tests), shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
    out = r.stdout + r.stderr
finally:
    shutil.copyfile(bak, path)
open(os.path.join(S, f'break-{tag}.txt'), 'w', encoding='utf-8', newline='').write(out)
lines = [l for l in out.splitlines() if ('FAIL' in l or '×' in l or 'Tests ' in l or 'Test Files' in l or 'AssertionError' in l)]
print('\n'.join(lines[:14]))
print('restored:', open(path, encoding='utf-8', newline='').read() == src)
