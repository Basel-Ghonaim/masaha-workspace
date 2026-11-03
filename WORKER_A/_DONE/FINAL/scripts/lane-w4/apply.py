# Apply exact-text edits to repository files, from an edits file with no escapes:
#   @@@ relative/path/from/worktree
#   <<<
#   old text (lines)
#   ===
#   new text (lines)
#   >>>
# Each old text must occur exactly once. Files are read and written as UTF-8, newlines kept.
import sys, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = 'C:/dev/masaha/app-lane-w4'
src = open(sys.argv[1], encoding='utf8').read().split('\n')
edits = []
i = 0
cur = None
while i < len(src):
    line = src[i]
    if line.startswith('@@@ '):
        cur = line[4:].strip(); i += 1; continue
    if line == '<<<':
        j = src.index('===', i + 1); k = src.index('>>>', j + 1)
        edits.append((cur, '\n'.join(src[i + 1:j]), '\n'.join(src[j + 1:k])))
        i = k + 1; continue
    i += 1
files = {}
for rel, old, new in edits:
    p = os.path.join(ROOT, rel)
    if rel not in files:
        files[rel] = open(p, encoding='utf8', newline='').read()
    s = files[rel]
    crlf = '\r\n' in s
    o, n = (old.replace('\n', '\r\n'), new.replace('\n', '\r\n')) if crlf else (old, new)
    c = s.count(o)
    if c != 1:
        print('FAIL', rel, 'count', c, repr(old[:80])); sys.exit(1)
    files[rel] = s.replace(o, n)
for rel, s in files.items():
    open(os.path.join(ROOT, rel), 'w', encoding='utf8', newline='').write(s)
    print('wrote', rel)
