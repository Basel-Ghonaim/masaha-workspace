# List or stage a file's hunks (zero context) against the index.
#   python hunks.py list <file>            -> numbered hunks with their first changed lines
#   python hunks.py stage <file> <i> [<j>…] -> stage only those hunks (git apply --cached)
import subprocess, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = 'C:/dev/masaha/app-lane-w4'
mode, path = sys.argv[1], sys.argv[2]
diff = subprocess.run(['git', 'diff', '--unified=0', '--no-color', '--', path], cwd=ROOT,
                      capture_output=True, text=True, encoding='utf8').stdout
lines = diff.split('\n')
head, hunks, cur = [], [], None
for line in lines:
    if line.startswith('@@'):
        cur = [line]; hunks.append(cur)
    elif cur is None:
        head.append(line)
    else:
        cur.append(line)
if mode == 'list':
    for i, h in enumerate(hunks):
        body = [l for l in h[1:] if l[:1] in '+-']
        print(f'[{i}] {h[0]}')
        for l in body[:3]:
            print('     ' + l[:150])
else:
    keep = [int(x) for x in sys.argv[3:]]
    patch = '\n'.join(head) + '\n' + '\n'.join('\n'.join(hunks[i]) for i in keep) + '\n'
    # A hunk's trailing empty string from the split is a blank context line; strip trailing blanks.
    patch = patch.rstrip('\n') + '\n'
    r = subprocess.run(['git', 'apply', '--cached', '--unidiff-zero', '-'], cwd=ROOT, input=patch,
                       capture_output=True, text=True, encoding='utf8')
    print('exit', r.returncode, r.stderr)
