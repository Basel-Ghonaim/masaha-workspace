"""Join lane C's commit 1 docs onto lane B's commit 3: the user's parts added to the admin's lines."""
import io, re

R = 'C:/dev/masaha/app-lane-c/'
C = re.compile(r'<<<<<<< [^\n]*\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n', re.S)


def sub1(text, old, new):
    assert text.count(old) == 1, old[:60]
    return text.replace(old, new)


p = R + 'docs/features/data-reports.md'
s = io.open(p, encoding='utf8', newline='').read()
blocks = list(C.finditer(s))
assert len(blocks) == 4
out = []
last = 0
for i, m in enumerate(blocks):
    ours, theirs = m.group(1), m.group(2)
    if i == 0:
        r = sub1(ours, "on the web, the owner's and the admin's «بلاغات البيانات».",
                 "on the web, the owner's and the admin's «بلاغات البيانات» and a signed-in user's «بلاغاتي».")
        r = sub1(r, "the admin's list of every space's, and the decision sheet.",
                 "the admin's list of every space's, and the decision sheet; the user's own reports.")
    elif i == 1:
        r = ours + '\n' + theirs
    elif i == 2:
        r = sub1(ours, '(`SpaceReportsList`, `AdminReportsList`, `AdminSpaceFilterSlot`)',
                 '(`SpaceReportsList`, `AdminReportsList`, `AdminSpaceFilterSlot`, `MyReportsList`)')
        r = sub1(r, "set [space-links](space-links.md)' `AdminSpaceFilter`: the repository",
                 "set [space-links](space-links.md)' `AdminSpaceFilter`, and `pages/site/account/MyReportsPage.tsx`, which gives the spaces' and the directory's links: the repository")
        r = sub1(r, "the decision's toast in `components/`. Words:",
                 "the decision's toast in `components/`; the user's reports, their view in `hooks/mine/`, their list and card in `components/mine/`, the card's type in `types/MyReportCardView.ts`. Words:")
    else:
        mine = [l for l in theirs.rstrip('\n').split('\n') if '«بلاغاتي»' in l]
        assert len(mine) == 1
        r = ours + mine[0] + '\n'
    out.append(s[last:m.start()] + r)
    last = m.end()
out.append(s[last:])
t = ''.join(out)
assert '<<<<<<<' not in t
io.open(p, 'w', encoding='utf8', newline='').write(t)
print('ok data-reports.md')
