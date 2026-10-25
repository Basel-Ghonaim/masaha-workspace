"""Stage only the hunks of one file whose text contains a given marker.

Usage: python stage_hunks.py <file> <marker> [<marker> ...]
"""
import subprocess
import sys

path, markers = sys.argv[1], sys.argv[2:]
diff = subprocess.run(
    ['git', 'diff', '-U0', '--', path], capture_output=True, check=True
).stdout.decode('utf-8')
lines = diff.splitlines(keepends=True)
head, hunks, current = [], [], None
for line in lines:
    if line.startswith('@@'):
        current = [line]
        hunks.append(current)
    elif current is None:
        head.append(line)
    else:
        current.append(line)
chosen = [h for h in hunks if any(m in ''.join(h) for m in markers)]
if not chosen:
    sys.exit(f'no hunk matches in {path}')
patch = ''.join(head) + ''.join(''.join(h) for h in chosen)
subprocess.run(
    ['git', 'apply', '--cached', '--unidiff-zero', '-'], input=patch.encode('utf-8'), check=True
)
print(f'{path}: staged {len(chosen)} of {len(hunks)} hunks')
