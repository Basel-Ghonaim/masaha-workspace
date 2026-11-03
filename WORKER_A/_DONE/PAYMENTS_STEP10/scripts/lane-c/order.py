"""GIT_SEQUENCE_EDITOR: move the heart icon's pick after commit 2's (the plan's order 1, 2, 3, 4, 5)."""
import sys

path = sys.argv[1]
with open(path, encoding='utf8', newline='') as f:
    lines = f.read().split('\n')
heart = [i for i, line in enumerate(lines) if line.startswith('pick ') and 'add the heart icon' in line]
report = [i for i, line in enumerate(lines) if line.startswith('pick ') and 'report wrong information' in line]
if len(heart) != 1 or len(report) != 1:
    sys.exit('lines not found')
line = lines.pop(heart[0])
target = [i for i, l in enumerate(lines) if l.startswith('pick ') and 'report wrong information' in l][0]
lines.insert(target + 1, line)
with open(path, 'w', encoding='utf8', newline='') as f:
    f.write('\n'.join(lines))
