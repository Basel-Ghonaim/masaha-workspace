import subprocess, os
D = 'C:/dev/masaha/workspace/WORKER_A/FINAL/scripts/lane-w2/c614/'
R = 'C:/dev/masaha/app-lane-w2'
W = 'apps/web/src/'


def brk(label, rel, old, new, *tests, unit=False):
    open(D + label + '-old.txt', 'w', encoding='utf8', newline='').write(old)
    open(D + label + '-new.txt', 'w', encoding='utf8', newline='').write(new)
    lane = 'test:unit' if unit else 'test:component'
    cmd = ['python', D + 'brk.py', R, label, W + rel, D + label + '-old.txt', D + label + '-new.txt', '--',
           'npm', 'run', lane, '-w', '@masaha/web', '--'] + list(tests)
    out = subprocess.run(cmd, capture_output=True, text=True, encoding='utf8', errors='replace')
    print('==', label)
    print(out.stdout[-1500:], out.stderr[-500:])


N = 'src/features/data-reports/components/notice'
brk('B173', 'features/data-reports/hooks/notice/useReportNotice.ts',
    "        if (!resolving.isPending && !blocked) resolving.mutate();",
    "        if (!resolving.isPending && !blocked) setResolved(true);", N)
brk('B174', 'features/data-reports/hooks/notice/useReportNotice.ts',
    "  const who = 'reporter' in report ? report.reporter.name : words.notice.visitor;",
    "  const who = 'reporter' in report ? report.reporter.name : 'Huda Saleh';", N)
brk('B174b', 'features/data-reports/hooks/notice/useReportNotice.ts',
    "  if (elsewhere || (!resolved && report.status !== 'OPEN')) return null;",
    "  if (elsewhere) return null;", N)
brk('B174c', 'features/data-reports/hooks/notice/useReportNotice.ts',
    "    'space' in report && (report.space.id !== spaceId || report.space.verified);",
    "    'space' in report && report.space.id !== spaceId;", N)
brk('B175', 'pages/dashboard/fieldSections.ts',
    "  return `${page}?report=${String(reportId)}${landingOf(field)}`;",
    "  return `${page}${landingOf(field)}`;", 'src/pages/dashboard/fieldSections.unit.test.ts', unit=True)
brk('B175b', 'features/data-reports/components/space/SpaceReportsList.tsx',
    "          editLink={fieldLink(list.sheet.report.field, list.sheet.report.id)}",
    "          editLink={fieldLink(list.sheet.report.field, 0)}", 'src/features/data-reports/components/space')
brk('B176', 'features/data-reports/hooks/space/useSpaceReports.ts',
    "  const addressed = reportIdOf(params.get('open'));",
    "  const addressed = reportIdOf(null);", 'src/features/data-reports/components/space')
brk('B176b', 'features/data-reports/hooks/admin/useAdminReports.ts',
    "  const addressed = reportIdOf(params.get('open'));",
    "  const addressed = reportIdOf(null);", 'src/features/data-reports/components/admin')
