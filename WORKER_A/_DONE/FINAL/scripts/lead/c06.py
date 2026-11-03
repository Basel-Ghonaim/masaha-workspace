import os

ROOT = 'C:/dev/masaha/app/apps/web/src/'


def edit(p, old, new):
    path = ROOT + p
    s = open(path, encoding='utf8').read()
    assert s.count(old) == 1, (p, old[:70])
    s = s.replace(old, new)
    open(path, 'w', encoding='utf8', newline='').write(s)


def write(p, text):
    path = ROOT + p
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf8', newline='').write(text)


def stub(path, name, unit, depth):
    up = '../' * depth
    write(path, f"""import {{ PageHeader }} from '{up}shell/PageHeader';

/**
 * {name}: its route and title are the foundation's; its screen is {unit}'s, which replaces this body.
 * Until then, the title in the top bar and nothing more.
 */
export function {path.rsplit('/', 1)[1][:-4]}() {{
  return <PageHeader />;
}}
""")


D = 'pages/dashboard/'
stub(D + 'space/overview/OverviewPage.tsx', "The owner's overview (screen 12)", 'U5 (D5.1)', 2)
stub(D + 'space/finance/FinancePage.tsx', 'Finance (screen 19)', 'U5 (D5.3–D5.5)', 2)
stub(D + 'space/audit/AuditPage.tsx', "The owner's audit log (O13, finding 14)", 'U6 (D6.1)', 2)
stub(D + 'admin/overview/OverviewPage.tsx', "The admin's overview (screen 25)", 'U5 (D5.2)', 2)
stub(D + 'admin/audit/AuditPage.tsx', "The admin's audit log (screen 31)", 'U6 (D6.1)', 2)
stub(D + 'admin/settings/SettingsPage.tsx', 'The platform settings (screen 32)', 'U6 (D6.2)', 2)

edit(D + 'routes.tsx', """const ADMIN_PAGES: Partial<Record<DashboardPageName, RouteObject['lazy']>> = {
  spaces: async () => {""", """const ADMIN_PAGES: Partial<Record<DashboardPageName, RouteObject['lazy']>> = {
  overview: async () => {
    const { OverviewPage } = await import('./admin/overview/OverviewPage');
    return { element: <OverviewPage /> };
  },
  audit: async () => {
    const { AuditPage } = await import('./admin/audit/AuditPage');
    return { element: <AuditPage /> };
  },
  platformSettings: async () => {
    const { SettingsPage } = await import('./admin/settings/SettingsPage');
    return { element: <SettingsPage /> };
  },
  spaces: async () => {""")
edit(D + 'routes.tsx', """  announcements: async () => {
    const { AnnouncementsPage } = await import('./space/announcements/AnnouncementsPage');
    return <AnnouncementsPage />;
  },""", """  announcements: async () => {
    const { AnnouncementsPage } = await import('./space/announcements/AnnouncementsPage');
    return <AnnouncementsPage />;
  },
  audit: async () => {
    const { AuditPage } = await import('./space/audit/AuditPage');
    return <AuditPage />;
  },""")
edit(D + 'routes.tsx', """  desk: async () => {
    const { DeskPage } = await import('./space/desk/DeskPage');
    return <DeskPage />;
  },""", """  desk: async () => {
    const { DeskPage } = await import('./space/desk/DeskPage');
    return <DeskPage />;
  },
  finance: async () => {
    const { FinancePage } = await import('./space/finance/FinancePage');
    return <FinancePage />;
  },""")
edit(D + 'routes.tsx', """  myPayments: async () => {""", """  overview: async () => {
    const { OverviewPage } = await import('./space/overview/OverviewPage');
    return <OverviewPage />;
  },
  myPayments: async () => {""")

# --- the account's settings page
write('pages/site/account/settings/AccountSettingsPage.tsx', """import { useCopy } from '@shared/copy';

/**
 * «إعدادات حسابي» (screen 9): its route and title are the foundation's; its screen is U9's (D9.2),
 * which replaces this body. Until then, the page's heading and nothing more.
 */
export function AccountSettingsPage() {
  const copy = useCopy();

  return <h1 className="text-heading-1">{copy.users.settings.title}</h1>;
}
""")
edit('pages/site/navigation.ts', """import { CHANGE_PASSWORD_PATH, RESET_PASSWORD_PATH } from '@shared/routing';""", """import { ACCOUNT_SETTINGS_PATH, CHANGE_PASSWORD_PATH, RESET_PASSWORD_PATH } from '@shared/routing';""")
edit('pages/site/navigation.ts', """  /** The signed-in user's favourites (screen 10), under the account's layout. */
  myFavorites: '/me/favorites',""", """  /** The signed-in user's favourites (screen 10), under the account's layout. */
  myFavorites: '/me/favorites',
  /** The signed-in user's own settings (screen 9), under the account's layout. */
  mySettings: ACCOUNT_SETTINGS_PATH,""")
edit('pages/site/navigation.ts', """  { key: 'reports', to: SITE_PATHS.myReports },
];""", """  { key: 'reports', to: SITE_PATHS.myReports },
  { key: 'settings', to: SITE_PATHS.mySettings },
];""")
edit('pages/site/routes.tsx', """                  const { MyReportsPage } = await import('./account/MyReportsPage');
                  return {
                    element: (
                      <RequireAuth>
                        <MyReportsPage />
                      </RequireAuth>
                    ),
                  };
                },
              },""", """                  const { MyReportsPage } = await import('./account/MyReportsPage');
                  return {
                    element: (
                      <RequireAuth>
                        <MyReportsPage />
                      </RequireAuth>
                    ),
                  };
                },
              },
              {
                path: SITE_PATHS.mySettings,
                handle: { title: (copy) => copy.users.settings.title } satisfies TitledHandle,
                lazy: async () => {
                  const { AccountSettingsPage } = await import(
                    './account/settings/AccountSettingsPage'
                  );
                  return {
                    element: (
                      <RequireAuth>
                        <AccountSettingsPage />
                      </RequireAuth>
                    ),
                  };
                },
              },""")

# --- copy: the account's settings title and its link; the three new sections, empty
edit('shared/copy/english/site.ts', """    reports: 'My reports',
  },""", """    reports: 'My reports',
    settings: 'Account settings',
  },""")
edit('shared/copy/english/users.ts', """  /** The dashboard's account menu: the way back to the public site. */""", """  /** «إعدادات حسابي» (screen 9): its title, which its route and the page's heading show. */
  settings: { title: 'Account settings' },
  /** The dashboard's account menu: the way back to the public site. */""")
edit('shared/copy/arabic/users.ts', """  publicSite: 'الموقع العام',""", """  settings: { title: 'إعدادات حسابي' },
  publicSite: 'الموقع العام',""")
s = open(ROOT + 'shared/copy/arabic/site.ts', encoding='utf8').read()
print('arabic site account:', s[s.find('account: {'):s.find('account: {') + 120])

for name, const, about in (
    ('overview', 'OVERVIEW', "The owner's and the admin's overviews (screens 12 and 25): U5's words."),
    ('finance', 'FINANCE', "Finance (screen 19), the owner's alone: U5's words."),
    ('audit', 'AUDIT', "The audit logs, the owner's and the admin's (O13, screen 31): U6's words."),
):
    write(f'shared/copy/english/{name}.ts', f"""/** {about} */
export const {const} = {{}} as const;
""")
    write(f'shared/copy/arabic/{name}.ts', f"""import type {{ Catalogue }} from '../shape';

export const {const} = {{}} satisfies Catalogue['{name}'];
""")
print('done')
