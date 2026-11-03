REPO = r'C:\dev\masaha\app-lane-w1'
T = 'npm run test:component -w @masaha/web -- src/features/overview/components/admin'
H = r'apps\web\src\features\overview\hooks\admin\useAdminOverview.ts'
C = r'apps\web\src\features\overview\components\admin\CompletenessCard.tsx'
BREAKS = [
    ('B117', H, """        {
          key: 'users',
          label: words.tiles.users.label,
          value: String(answer.newUsers),
          helper: words.tiles.users.helper,
          href: links.users,
        },
""", "", T),
    ('B118', C, """<Badge key={group.key} variant="warning">""", """<Badge key={group.key} variant="destructive">""", T),
    ('B118b', H, "completeness.first.slice(0, FIRST)", "completeness.first", T),
    ('B119', r'apps\web\src\pages\dashboard\admin\overview\OverviewPage.tsx', "?status=editable&stale=true`", "?status=editable&stale=1`",
     'npm run test:component -w @masaha/web -- src/pages/dashboard/admin/overview'),
    ('B120', r'apps\web\src\features\overview\components\admin\AdminOverview.tsx', """        {overview.privacy}
""", "", T),
]
