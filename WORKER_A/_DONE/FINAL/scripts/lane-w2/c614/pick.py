import sys, re
# pick.py <file> <choice per conflict: h|o|ho|oh|lines spec>  — per conflict, keep HEAD (h), ours (o), both.
# A spec "L:h1,o2" keeps line 1 of HEAD then line 2 of ours (1-based), for line-level merges.
p = sys.argv[1]
choices = sys.argv[2:]
s = open(p, encoding='utf8', newline='').read()
pat = re.compile(r'<<<<<<< [^\n]*\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n', re.S)
it = iter(choices)


def sub(m):
    c = next(it)
    h, o = m.group(1), m.group(2)
    if c.startswith('L:'):
        hl, ol = h.splitlines(True), o.splitlines(True)
        out = []
        for part in c[2:].split(','):
            src = hl if part[0] == 'h' else ol
            out.append(src[int(part[1:]) - 1])
        return ''.join(out)
    return '' if c == 'x' else ''.join({'h': h, 'o': o}[ch] for ch in c)


s = pat.sub(sub, s)
assert '<<<<<<<' not in s
open(p, 'w', encoding='utf8', newline='').write(s)
print('ok', p)
