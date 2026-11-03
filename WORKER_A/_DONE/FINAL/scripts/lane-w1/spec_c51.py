REPO = r'C:\dev\masaha\app-lane-w1'
T = 'npm run test:component -w @masaha/web -- src/features/overview/components/owner'
H = r'apps\web\src\features\overview\hooks\owner\useOwnerOverview.ts'
A = r'apps\web\src\features\overview\services\attentionRows.ts'
AC = r'apps\web\src\features\overview\components\owner\AttentionCard.tsx'
BREAKS = [
    ('B110', H, "      now: words.present.now({",
     "      now: `${String(answer.attention.customersOwing * 2500)} ₪ ` + words.present.now({", T),
    ('B111', A, """  counted('reports', attention.openReports, { label: words.review, href: links.reports });
  counted('uncollected', attention.uncollectedVisits, {
    label: words.openDesk,
    href: links.desk,
  });""", """  counted('uncollected', attention.uncollectedVisits, {
    label: words.openDesk,
    href: links.desk,
  });
  counted('reports', attention.openReports, { label: words.review, href: links.reports });""", T),
    ('B112', r'apps\web\src\shared\copy\arabic\overview.ts', "            two: 'آخر تحديث قبل يومين',",
     "            two: `آخر تحديث قبل ${String(days)} يوم`,", T),
    ('B113', AC, """            {attention.allClear}
""", "", T),
    ('B114', H, """        capacity === null
          ? null
          : {
              value""", """        false
          ? null
          : {
              value""", T),
    ('B115', H, "endingSoon.first.slice(0, 5)", "endingSoon.first.slice(0, 6)", T),
    ('B116', r'apps\web\src\features\overview\hooks\owner\useOwnerOverview.ts', "    void result.refetch();", "    void 0;", T),
    ('B116b', r'apps\web\src\shared\routing\..\..\pages\dashboard\navigation.ts', "  { name: 'overview', segment: '', roles: OWNER },",
     "  { name: 'overview', segment: '', roles: BOTH },",
     'npm run test:component -w @masaha/web -- src/pages/dashboard/space/overview'),
    ('Boffline', r'apps\web\src\features\overview\hooks\useLoadFailure.ts', "const offline = error?.type === 'network';", "const offline = false;",
     'npm run test:component -w @masaha/web -- src/features/overview/hooks'),
]
