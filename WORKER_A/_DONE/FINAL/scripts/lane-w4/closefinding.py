# Close a finding: python closefinding.py <n> "<resolution line>"
import sys, glob, os
sys.stdout.reconfigure(encoding='utf-8')
n, line = sys.argv[1], sys.argv[2]
[p] = glob.glob(f'C:/dev/masaha/app-lane-w4/docs/architecture/findings/{n}-*.md')
s = open(p, encoding='utf8', newline='').read()
head = '**Status:** Open · **Date:** '
i = s.index(head)
j = s.index('\n', i)
date = s[i + len(head):j].strip()
s = s[:i] + f'**Status:** Resolved · **Date:** {date} · **Resolved:** 2026-10-29' + s[j:]
s = s.rstrip('\n') + f'\n\n**Resolution (#PRNUM):** {line}\n'
open(p, 'w', encoding='utf8', newline='').write(s)
print('closed', os.path.basename(p))
