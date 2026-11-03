import os
root = r'C:\dev\masaha\app-lane-t\apps\web\src'
def w(rel, text):
    open(os.path.join(root, rel), 'w', encoding='utf8', newline='').write(text)
def rep(rel, old, new):
    p = os.path.join(root, rel); s = open(p, encoding='utf8').read()
    assert s.count(old) == 1, (rel, old)
    open(p, 'w', encoding='utf8', newline='').write(s.replace(old, new))

w(r'features\data-reports\public.ts', """// What the site draws of data reports, apart from the dashboard's lists in index.ts, so a site
// page's chunk never reaches the table's library (finding 180, docs/frontend/architecture.md §3).
export { MyReportsList } from './components/mine/MyReportsList';
export { ReportAction } from './components/report/ReportAction';
""")
rep(r'features\data-reports\index.ts', """export { MyReportsList } from './components/mine/MyReportsList';
export { ReportAction } from './components/report/ReportAction';
""", "")
w(r'features\announcements\public.ts', """// What the site's space page draws of announcements, apart from the dashboard's list in index.ts,
// so a site page's chunk never reaches the calendar's library (finding 180,
// docs/frontend/architecture.md §3).
export { ClosureNotice } from './components/public/ClosureNotice';
export { SpaceAnnouncements } from './components/public/SpaceAnnouncements';
""")
rep(r'features\announcements\index.ts', """export { ClosureNotice } from './components/public/ClosureNotice';
export { SpaceAnnouncements } from './components/public/SpaceAnnouncements';
""", "")
w(r'features\platform-settings\public.ts', """// What the site draws of the platform's settings, its contact, apart from what the dashboard draws
// in index.ts (finding 180, docs/frontend/architecture.md §3).
export { PlatformContact } from './components/PlatformContact';
""")
w(r'features\platform-settings\index.ts', """// The dashboard's parts of the platform's settings; the site's contact is public.ts's (finding 180,
// docs/frontend/architecture.md §3). None is built yet.
export {};
""")
rep(r'pages\site\account\MyReportsPage.tsx', "from '@features/data-reports';", "from '@features/data-reports/public';")
rep(r'pages\site\public\about\AboutPage.tsx', "from '@features/platform-settings';", "from '@features/platform-settings/public';")
rep(r'pages\site\public\space\SpacePage.tsx', "from '@features/announcements';", "from '@features/announcements/public';")
rep(r'pages\site\public\space\SpacePage.tsx', "from '@features/data-reports';", "from '@features/data-reports/public';")
rep(r'pages\site\public\space\SpacePage.tsx', "from '@features/platform-settings';", "from '@features/platform-settings/public';")
