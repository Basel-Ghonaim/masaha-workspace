# usage: python findings_move.py <number> [<to-group>=Resolved] : moves an index line to its group, by number
import re, sys
num = int(sys.argv[1]); group = sys.argv[2] if len(sys.argv) > 2 else 'Resolved'
p = 'docs/architecture/findings/README.md'
lines = open(p, encoding='utf-8', newline='').read().split('\n')
idx = [i for i, l in enumerate(lines) if l.startswith(f'- [{num}. ')]
assert len(idx) == 1, idx
entry = lines.pop(idx[0])
start = lines.index(f'## {group}')
i = start + 1
while i < len(lines) and not lines[i].startswith('- ['): i += 1
while i < len(lines) and lines[i].startswith('- ['):
    n = int(re.match(r'- \[(\d+)\.', lines[i]).group(1))
    if n > num: break
    i += 1
lines.insert(i, entry)
open(p, 'w', encoding='utf-8', newline='').write('\n'.join(lines))
print('moved', num, 'to', group, 'at line', i + 1)
