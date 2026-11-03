"""Move finding N's line in docs/architecture/findings/README.md from its group to `## Resolved`,
in number order. Usage: python resolve_index.py <app root> <N> [<N> ...]"""
import io, re, sys

root, numbers = sys.argv[1], [int(n) for n in sys.argv[2:]]
p = root + '/docs/architecture/findings/README.md'
s = io.open(p, encoding='utf8', newline='').read()
lines = s.split('\n')


def num(line):
    m = re.match(r'- \[(\d+)\.', line)
    return int(m.group(1)) if m else None


for n in numbers:
    i = next(k for k, l in enumerate(lines) if num(l) == n)
    line = lines.pop(i)
    start = lines.index('## Resolved')
    end = next((k for k in range(start + 1, len(lines)) if lines[k].startswith('## ')), len(lines))
    entries = [k for k in range(start + 1, end) if num(lines[k]) is not None]
    at = next((k for k in entries if num(lines[k]) > n), entries[-1] + 1)
    lines.insert(at, line)
io.open(p, 'w', encoding='utf8', newline='').write('\n'.join(lines))
print('moved', numbers)
