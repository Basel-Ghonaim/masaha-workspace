"""Usage: edit.py <file> <specfile>. specfile holds blocks: <<<OLD\n...\n===\n...\n>>> ; each OLD must occur once."""
import sys
path, spec = sys.argv[1], sys.argv[2]
text = open(path, encoding='utf8', newline='').read()
blocks = open(spec, encoding='utf8', newline='').read().split('<<<OLD\n')[1:]
for b in blocks:
    old, rest = b.split('\n===\n', 1)
    new = rest.rsplit('\n>>>', 1)[0]
    if '\r\n' in text:
        old = old.replace('\n', '\r\n'); new = new.replace('\n', '\r\n')
    n = text.count(old)
    if n != 1:
        sys.exit(f'{path}: OLD occurs {n} times: {old[:80]!r}')
    text = text.replace(old, new)
open(path, 'w', encoding='utf8', newline='').write(text)
print('ok', path)
