# python resolve.py <findings-file> <resolution text>
import sys, re
p, text = sys.argv[1], sys.argv[2]
s = open(p, encoding='utf8', newline='').read()
m = re.search(r'^\*\*Status:\*\* Open · \*\*Date:\*\* (\S+)$', s, re.M)
assert m, 'status line'
s = s[:m.start()] + f'**Status:** Resolved · **Date:** {m.group(1)} · **Resolved:** 2026-10-29' + s[m.end():]
s = s.rstrip('\n') + '\n\n**Resolution (#PRNUM):** ' + text + '\n'
open(p, 'w', encoding='utf8', newline='').write(s)
