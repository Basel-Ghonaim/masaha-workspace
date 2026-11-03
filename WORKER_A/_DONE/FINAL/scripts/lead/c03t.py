ROOT = 'C:/dev/masaha/app/apps/web/src/'


def edit(p, old, new):
    path = ROOT + p
    s = open(path, encoding='utf8').read()
    assert s.count(old) == 1, (p, old[:60])
    s = s.replace(old, new)
    open(path, 'w', encoding='utf8', newline='').write(s)


T = 'pages/dashboard/routes.component.test.tsx'
edit(T, """  'Staff',
  'Settings',
];
const RECEPTION_PAGES""", """  'Staff',
  'Audit log',
  'Settings',
];
const RECEPTION_PAGES""")
edit(T, """  'Audit log',
  'Settings',
];

/** The desk's state now""", """  'Audit log',
  'Platform settings',
];

/** The desk's state now""")
edit(T, """/** Signs in a user (id 1) with `fields`; their spaces are answered from their links. */
function signIn(fields: Partial<SessionUser>) {
  const { user } = aSession(fields);
  establishSession({ user, accessToken: 'token-1' }, { source: 'signIn' });
  fakeTransport((request) => {""", """/**
 * Signs in a user (id 1) with `fields`; their spaces are answered from their links, and the sidebar's
 * count of open reports by `openReports` (none by default).
 */
function signIn(fields: Partial<SessionUser>, { openReports = 0 }: { openReports?: number } = {}) {
  const { user } = aSession(fields);
  establishSession({ user, accessToken: 'token-1' }, { source: 'signIn' });
  fakeTransport((request) => {
    // The sidebar's count of the open reports: a page of one asked, its total read.
    if (request.url?.endsWith('/data-reports') === true) {
      return reportsPage([], { total: openReports });
    }""")
edit(T, """/** The names of the pages a sidebar lists, in order: its first list (the foot is another). */
async function pagesIn(navigation: string) {
  const nav = await screen.findByRole('navigation', { name: navigation });
  const [pages] = within(nav).getAllByRole('list');
  return pages
    ? within(pages)
        .getAllByRole('link')
        .map((link) => link.textContent)
    : [];
}""", """/** The names of the pages a sidebar lists, in order, across its groups (the foot's list is not one). */
async function pagesIn(navigation: string) {
  const nav = await screen.findByRole('navigation', { name: navigation });
  return within(nav)
    .getAllByRole('list')
    .filter((list) => list.closest('[data-slot="sidebar-footer"]') === null)
    .flatMap((list) => within(list).getAllByRole('link'))
    .map((link) => link.textContent);
}

/** The names of the groups a sidebar draws, in order. */
async function groupsIn(navigation: string) {
  const nav = await screen.findByRole('navigation', { name: navigation });
  return within(nav)
    .queryAllByRole('group')
    .map((group) => group.getAttribute('aria-labelledby'))
    .map((id) => (id === null ? null : document.getElementById(id)?.textContent));
}""")
edit(T, """  it('lists the owner’s eleven pages, the overview marked as the page shown', async () => {""", """  it('lists the owner’s twelve pages, the overview marked as the page shown', async () => {""")
edit(T, """  it('lists the admin’s eight pages under the platform’s own header', async () => {""", """  it('draws the owner’s pages in four groups named by task, the overview first and ungrouped', async () => {
    asOwner();
    renderDashboard('/dashboard/spaces/7');

    expect(await groupsIn('Space dashboard')).toEqual([
      'Today',
      'Money',
      'The space',
      'Team & settings',
    ]);
    const nav = within(screen.getByRole('navigation', { name: 'Space dashboard' }));
    expect(nav.getByText('Today')).toBeVisible();
    const team = within(nav.getByRole('group', { name: 'Team & settings' }));
    expect(team.getAllByRole('link').map((link) => link.textContent)).toEqual([
      'Staff',
      'Audit log',
      'Settings',
    ]);
    expect(nav.getByRole('link', { name: 'Audit log' })).toHaveAttribute(
      'href',
      '/dashboard/spaces/7/audit',
    );
  });

  it('draws reception’s four pages with no group names', async () => {
    asReception();
    renderDashboard('/dashboard/spaces/7/desk');

    expect(await pagesIn('Space dashboard')).toEqual(RECEPTION_PAGES);
    expect(await groupsIn('Space dashboard')).toEqual([]);
  });

  it('keeps the group names for assistive technology only on the rail', async () => {
    stubScreenWidth(800);
    asOwner();
    renderDashboard('/dashboard/spaces/7');

    const nav = within(await screen.findByRole('navigation', { name: 'Space dashboard' }));
    expect(nav.getByText('Money')).toHaveClass('sr-only');
    expect(nav.getByRole('group', { name: 'Money' })).toBeInTheDocument();
  });

  it('counts the open reports on the owner’s «Data reports», named for a reader, and shows none at zero', async () => {
    signIn({ role: 'OWNER', spaces: [{ spaceId: 7, role: 'OWNER' }] }, { openReports: 3 });
    renderDashboard('/dashboard/spaces/7');
    const nav = within(await screen.findByRole('navigation', { name: 'Space dashboard' }));

    await waitFor(() => {
      expect(nav.getByRole('link', { name: 'Data reports' })).toHaveAccessibleDescription(
        '3 new reports',
      );
    });
  });

  it('shows no count on «Data reports» with no open report', async () => {
    asOwner();
    renderDashboard('/dashboard/spaces/7');
    const nav = within(await screen.findByRole('navigation', { name: 'Space dashboard' }));

    await new Promise((resolve) => setTimeout(resolve, 50));
    expect(nav.getByRole('link', { name: 'Data reports' })).not.toHaveAccessibleDescription();
  });

  it('counts the reports waiting for the admin on the admin’s «Data reports»', async () => {
    signIn({ role: 'ADMIN' }, { openReports: 2 });
    renderDashboard('/dashboard/admin');
    const nav = within(await screen.findByRole('navigation', { name: 'Platform admin' }));

    await waitFor(() => {
      expect(nav.getByRole('link', { name: 'Data reports' })).toHaveAccessibleDescription(
        '2 reports waiting for the admin',
      );
    });
    expect(await groupsIn('Platform admin')).toEqual(['Spaces', 'The platform']);
  });

  it('lists the admin’s eight pages under the platform’s own header', async () => {""")
print('done')
