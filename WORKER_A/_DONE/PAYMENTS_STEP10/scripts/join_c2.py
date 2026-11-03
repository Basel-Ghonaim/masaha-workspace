"""Join lane C's commit 2 onto the joined branch: keep both sides."""
import io, re

R = 'C:/dev/masaha/app-lane-c/'
C = re.compile(r'<<<<<<< [^\n]*\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n', re.S)


def fix(path, fn):
    p = R + path
    s = io.open(p, encoding='utf8', newline='').read()
    t = C.sub(fn, s)
    assert '<<<<<<<' not in t and '>>>>>>>' not in t, path
    io.open(p, 'w', encoding='utf8', newline='').write(t)
    print('ok', path)


def sub1(text, old, new):
    assert text.count(old) == 1, old[:70]
    return text.replace(old, new)


fix('apps/web/src/features/data-reports/repository/dataReportsRepository.ts', lambda m: m.group(1) + m.group(2))
fix('docs/architecture/findings/README.md', lambda m: m.group(1) + m.group(2))


def docs(m):
    ours = m.group(1)
    if ours.startswith('> **Authority:**'):
        r = sub1(ours, "the owner's and the admin's «بلاغات البيانات» and a signed-in user's «بلاغاتي».",
                 "the owner's and the admin's «بلاغات البيانات», a signed-in user's «بلاغاتي» and the report from a space's page.")
        return sub1(r, "and the decision sheet; the user's own reports.",
                    "and the decision sheet; the user's own reports, and the report's button and dialog a space's page sets.")
    r = sub1(ours, '`AdminSpaceFilterSlot`, `MyReportsList`)', '`AdminSpaceFilterSlot`, `MyReportsList`, `ReportAction`)')
    r = sub1(r, "`AdminSpaceFilter`, and `pages/site/account/MyReportsPage.tsx`, which gives the spaces' and the directory's links:",
             "`AdminSpaceFilter`, `pages/site/account/MyReportsPage.tsx`, which gives the spaces' and the directory's links, and `pages/site/public/space/SpacePage.tsx`, which sets the report in the directory's slot with the site's sign-in:")
    return sub1(r, '`types/MyReportCardView.ts`. Words:',
                "`types/MyReportCardView.ts`; the report, its write and its dialog's view in `hooks/report/`, a guest's held report in `hooks/intent/reportIntent.ts`, its button and dialog in `components/report/`, its toast in `components/toast/`. Words:")


fix('docs/features/data-reports.md', docs)
