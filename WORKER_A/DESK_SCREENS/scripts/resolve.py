"""Resolves a conflicted file by choosing, for each conflict, the lines named: `ours` (HEAD, main) or
`theirs` (this branch's commit), line by line. Usage: python resolve.py <file> <choice per conflict>,
where a choice is a string of o/t per line pair, or 'O'/'T' for a whole side, or 'OT' for both, HEAD first."""
import sys
from pathlib import Path

path = Path(sys.argv[1])
choices = sys.argv[2:]
lines = path.read_text(encoding='utf-8').split('\n')
out, i, n = [], 0, 0
while i < len(lines):
    if not lines[i].startswith('<<<<<<< '):
        out.append(lines[i])
        i += 1
        continue
    j = lines.index('=======', i)
    k = next(x for x in range(j, len(lines)) if lines[x].startswith('>>>>>>> '))
    ours, theirs = lines[i + 1:j], lines[j + 1:k]
    choice = choices[n]
    n += 1
    if choice == 'O':
        out += ours
    elif choice == 'T':
        out += theirs
    elif choice == 'OT':
        out += ours + theirs
    elif choice == 'TO':
        out += theirs + ours
    else:
        if len(choice) != len(ours) or len(ours) != len(theirs):
            raise SystemExit(f'conflict {n}: {len(ours)} vs {len(theirs)} lines, choice {choice}')
        out += [o if c == 'o' else t for c, o, t in zip(choice, ours, theirs)]
    i = k + 1
if n != len(choices):
    raise SystemExit(f'{n} conflicts, {len(choices)} choices')
path.write_bytes('\n'.join(out).encode('utf-8'))
print(path.name, 'resolved', n)
