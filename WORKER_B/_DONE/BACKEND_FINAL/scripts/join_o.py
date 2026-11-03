# Resolves a rebase conflict by keeping both sides, ours (HEAD) first, theirs after; with per-file overrides
# that pick lines from each side. usage: python join_o.py <file> [mode]
#   mode 'both' (default): HEAD lines then theirs; 'table': HEAD's row of the first line, theirs' row of the last.
import re, sys
path = sys.argv[1]
mode = sys.argv[2] if len(sys.argv) > 2 else 'both'
s = open(path, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in s else '\n'
pat = re.compile(r'<<<<<<< [^\n]*\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n', re.S)
def repl(m):
    ours, theirs = m.group(1), m.group(2)
    if mode == 'both':
        return ours + theirs
    if mode == 'table':
        o = ours.splitlines(True); t = theirs.splitlines(True)
        return o[0] + t[-1]
    raise SystemExit('mode?')
out, n = pat.subn(repl, s)
assert '<<<<<<<' not in out and '>>>>>>>' not in out
open(path, 'w', encoding='utf-8', newline='').write(out)
print(path, 'resolved', n)
