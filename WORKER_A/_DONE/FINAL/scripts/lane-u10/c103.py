import sys
def edit(p, reps):
    s = open(p, encoding='utf8', newline='').read()
    for a, b in reps:
        n = s.count(a)
        if n != 1:
            sys.exit('%s count %d: %s' % (p, n, a[:70]))
        s = s.replace(a, b)
    open(p, 'w', encoding='utf8', newline='').write(s)
R = r'C:\dev\masaha\app-lane-u10\apps\web\src\pages\dashboard\routes.tsx'
edit(R, [
 ("/** The 404's title, for each branch's pages that are not there. */\nconst NOT_FOUND = { title: (copy) => copy.status.notFound.title } satisfies TitledHandle;\n",
  "/** The 404's title, for each branch's pages that are not there. */\nconst NOT_FOUND = { title: (copy) => copy.status.notFound.title } satisfies TitledHandle;\n\n/** A navigation item's screen. Every item has one: an item without one fails the routes' build. */\nfunction screenOf<Page>(pages: Partial<Record<DashboardPageName, Page>>, name: DashboardPageName) {\n  const page = pages[name];\n  if (page === undefined) throw new Error(`The dashboard page \"${name}\" has no screen.`);\n  return page;\n}\n"),
 ("/** The admin's pages that have a screen, each loaded lazily; the others show their placeholder. */",
  "/** The admin's pages, each loaded lazily. */"),
 ("/** The space's pages that have a screen, each loaded lazily; the others show their placeholder. */",
  "/** The space's pages, each loaded lazily. */"),
 ("""            lazy:
              ADMIN_PAGES[name] ??
              (async () => {
                const { PlaceholderPage } = await import('./PlaceholderPage');
                return { element: <PlaceholderPage /> };
              }),
""",
  """            lazy: screenOf(ADMIN_PAGES, name),
"""),
 ("""          ...SPACE_NAV.map(({ name, segment, roles }): RouteObject => ({
            ...placeOf(segment),
            handle: titleOf(name),
            lazy: async () => {
              const page = SPACE_PAGES[name];
              const element = page
                ? await page()
                : await import('./PlaceholderPage').then(({ PlaceholderPage }) => (
                    <PlaceholderPage />
                  ));
              return { element: <RequireSpaceRole roles={roles}>{element}</RequireSpaceRole> };
            },
          })),
""",
  """          ...SPACE_NAV.map(({ name, segment, roles }): RouteObject => {
            const page = screenOf(SPACE_PAGES, name);
            return {
              ...placeOf(segment),
              handle: titleOf(name),
              lazy: async () => ({
                element: <RequireSpaceRole roles={roles}>{await page()}</RequireSpaceRole>,
              }),
            };
          }),
"""),
])
edit(r'C:\dev\masaha\app-lane-u10\apps\web\src\pages\dashboard\routes.component.test.tsx', [
 ("      () => import('./PlaceholderPage'),\n", ""),
])
edit(r'C:\dev\masaha\app-lane-u10\apps\web\scripts\dashboardOnly.unit.test.ts', [
 ("'/repo/apps/web/src/pages/dashboard/PlaceholderPage.tsx',", "'/repo/apps/web/src/pages/dashboard/DashboardLanding.tsx',"),
])
edit(r'C:\dev\masaha\app-lane-u10\docs\frontend\architecture.md', [
 ("so is the `dashboard` group's shell, with its navigation per role and a placeholder for each page not built yet (§2)",
  "so is the `dashboard` group's shell, with its navigation per role and a screen for each of its pages (§2)"),
 ("the `/dashboard` redirect, one `PlaceholderPage`, which shows a page's title in the top bar until the page is built, and in `admin/`",
  "the `/dashboard` redirect, and in `admin/`"),
])
print('ok')
