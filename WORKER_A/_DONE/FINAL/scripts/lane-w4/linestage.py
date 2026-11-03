# Stage part of a file's changes, line by line, against the index (not the work tree).
#   python linestage.py <file> list           -> numbered changes (index vs work tree)
#   python linestage.py <file> stage 0 2 5-7  -> the index gets the index's text plus those changes
# A change is a run of lines replaced, inserted or deleted; an insertion of several lines is split
# into one change per line, and a replacement of n lines by n lines into one change per line.
import difflib, os, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = 'C:/dev/masaha/app-lane-w4'
path, mode = sys.argv[1], sys.argv[2]
old = subprocess.run(['git', 'show', f':{path}'], cwd=ROOT, capture_output=True).stdout.decode('utf8')
new = open(os.path.join(ROOT, path), encoding='utf8', newline='').read()
a, b = old.split('\n'), new.split('\n')
changes = []  # (i1, i2, j1, j2)
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
    if tag == 'equal':
        continue
    if tag == 'insert':
        for j in range(j1, j2):
            changes.append((i1, i1, j, j + 1))
    elif tag == 'delete':
        for i in range(i1, i2):
            changes.append((i, i + 1, j1, j1))
    elif tag == 'replace' and i2 - i1 == j2 - j1:
        for k in range(i2 - i1):
            changes.append((i1 + k, i1 + k + 1, j1 + k, j1 + k + 1))
    else:
        changes.append((i1, i2, j1, j2))
if mode == 'list':
    for n, (i1, i2, j1, j2) in enumerate(changes):
        print(f'[{n}] -{i2 - i1} +{j2 - j1} @ {i1 + 1}')
        for line in a[i1:i2][:1]:
            print('    - ' + line[:140])
        for line in b[j1:j2][:2]:
            print('    + ' + line[:140])
    sys.exit(0)
keep = set()
for arg in sys.argv[3:]:
    if '-' in arg:
        x, y = arg.split('-'); keep.update(range(int(x), int(y) + 1))
    else:
        keep.add(int(arg))
out, pos = [], 0
for n, (i1, i2, j1, j2) in enumerate(changes):
    out.extend(a[pos:i1])
    out.extend(b[j1:j2] if n in keep else a[i1:i2])
    pos = i2
out.extend(a[pos:])
text = '\n'.join(out).encode('utf8')
sha = subprocess.run(['git', 'hash-object', '-w', '--stdin'], cwd=ROOT, input=text,
                     capture_output=True).stdout.decode().strip()
mode_bits = subprocess.run(['git', 'ls-files', '-s', '--', path], cwd=ROOT, capture_output=True,
                           text=True).stdout.split(' ')[0] or '100644'
r = subprocess.run(['git', 'update-index', '--cacheinfo', f'{mode_bits},{sha},{path}'], cwd=ROOT,
                   capture_output=True, text=True)
print('staged', path, 'changes', sorted(keep), r.returncode, r.stderr)
