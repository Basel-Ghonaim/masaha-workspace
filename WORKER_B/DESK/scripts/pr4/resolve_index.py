"""Resolve a findings-index conflict by keeping both sides, then order the Open list by number."""
import io, re
p = 'C:/dev/masaha/app-b/docs/architecture/findings/README.md'
t = io.open(p, encoding='utf-8', newline='').read()
t = re.sub(r'^<<<<<<< [^\n]*\n(.*?)^=======\n(.*?)^>>>>>>> [^\n]*\n', lambda m: m.group(1) + m.group(2), t, flags=re.S | re.M)
assert '<<<<<<<' not in t and '>>>>>>>' not in t
head, rest = t.split('## Open\n', 1)
body, tail = rest.split('\n## Accepted', 1)
lines = body.strip('\n').split('\n')
assert all(l.startswith('- [') for l in lines), lines
seen = []
for l in lines:
    if l not in seen:
        seen.append(l)
seen.sort(key=lambda l: int(re.match(r'- \[(\d+)\.', l).group(1)))
t = head + '## Open\n\n' + '\n'.join(seen) + '\n\n## Accepted' + tail
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('resolved', len(seen), 'open')
