"""Rebuild the findings index's three groups from each finding file's own status line (S2, OD9).

Keeps the index's head (everything before `## Open`) as it is; lists each finding once, under its
status's group, by number, as `- [N. Title](file.md)`. Prints the counts and the Open group's numbers.
Usage: python index_findings.py <repo>
"""
import os
import re
import sys

repo = sys.argv[1]
folder = os.path.join(repo, 'docs', 'architecture', 'findings')
index = os.path.join(folder, 'README.md')
groups = {'Open': [], 'Accepted': [], 'Resolved': []}
for name in os.listdir(folder):
    if name == 'README.md' or not name.endswith('.md'):
        continue
    text = open(os.path.join(folder, name), encoding='utf8').read()
    head = re.search(r'^# (\d+)\. (.+)$', text, re.M)
    status = re.search(r'^\*\*Status:\*\* (Open|Accepted|Resolved)\b', text, re.M)
    assert head and status, name
    groups[status.group(1)].append((int(head.group(1)), head.group(2).strip(), name))

s = open(index, encoding='utf8').read()
top = s[: s.index('## Open')]
body = ''
for group in ('Open', 'Accepted', 'Resolved'):
    rows = sorted(groups[group])
    body += f'## {group}\n\n' + ''.join(f'- [{n}. {t}]({f})\n' for n, t, f in rows) + '\n'
open(index, 'w', encoding='utf8', newline='').write(top + body.rstrip('\n') + '\n')
print({g: len(v) for g, v in groups.items()})
print('Open:', [n for n, _, _ in sorted(groups['Open'])])
