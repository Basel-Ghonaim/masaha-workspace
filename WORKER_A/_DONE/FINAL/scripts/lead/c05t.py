ROOT = 'C:/dev/masaha/app/apps/web/src/'


def edit(p, old, new):
    path = ROOT + p
    s = open(path, encoding='utf8').read()
    assert s.count(old) == 1, (p, old[:70])
    s = s.replace(old, new)
    open(path, 'w', encoding='utf8', newline='').write(s)


A = 'features/users/components/AccountMenu.component.test.tsx'
edit(A, """  it('links the account’s pages it is given, before the dashboard', async () => {""", """  it('leads into the dashboard first, then links the account’s pages it is given', async () => {""")
edit(A, """            { key: 'reports', to: '/me/reports' },
          ]}""", """            { key: 'reports', to: '/me/reports' },
            { key: 'settings', to: '/me' },
          ]}""")
edit(A, """    expect(items.map((item) => item.textContent)).toEqual([
      'Favourites',
      'My reports',
      'Dashboard',
      'Sign out',
    ]);
    expect(items[0]).toHaveAttribute('href', '/me/favorites');
    expect(items[1]).toHaveAttribute('href', '/me/reports');""", """    expect(items.map((item) => item.textContent)).toEqual([
      'Dashboard',
      'Favourites',
      'My reports',
      'Account settings',
      'Sign out',
    ]);
    expect(items[1]).toHaveAttribute('href', '/me/favorites');
    expect(items[2]).toHaveAttribute('href', '/me/reports');
    expect(items[3]).toHaveAttribute('href', '/me');""")

C = 'features/users/components/CompactAccountMenu.component.test.tsx'
edit(C, """function renderMenu(user: SessionUser) {
  render(
    <MemoryRouter>
      <CompactAccountMenu user={user} dashboardPath="/dashboard" />
    </MemoryRouter>,
  );""", """function renderMenu(user: SessionUser, role?: string) {
  render(
    <MemoryRouter>
      <CompactAccountMenu user={user} role={role} />
    </MemoryRouter>,
  );""")
edit(C, """  it('leads a user with a space to the dashboard path it is given', async () => {
    await userEvent.click(renderMenu({ ...USER, spaces: [{ spaceId: 7, role: 'OWNER' }] }));

    const menu = within(await screen.findByRole('menu'));
    expect(menu.getByRole('menuitem', { name: 'Dashboard' })).toHaveAttribute('href', '/dashboard');
  });

  it('links none of the site’s account pages: the dashboard and sign-out only', async () => {
    await userEvent.click(renderMenu({ ...USER, spaces: [{ spaceId: 7, role: 'OWNER' }] }));

    const items = within(await screen.findByRole('menu')).getAllByRole('menuitem');
    expect(items.map((item) => item.textContent)).toEqual(['Dashboard', 'Sign out']);
  });

  it('leads the admin to the dashboard', async () => {
    await userEvent.click(renderMenu({ ...USER, role: 'ADMIN' }));

    expect(
      within(await screen.findByRole('menu')).getByRole('menuitem', { name: 'Dashboard' }),
    ).toBeInTheDocument();
  });

  it('offers no dashboard to a user with no role and no space', async () => {
    await userEvent.click(renderMenu(USER));

    expect(
      within(await screen.findByRole('menu')).queryByRole('menuitem', { name: 'Dashboard' }),
    ).not.toBeInTheDocument();
  });""", """  it('offers the public site and the account’s settings, not the way into the dashboard', async () => {
    await userEvent.click(renderMenu({ ...USER, spaces: [{ spaceId: 7, role: 'OWNER' }] }));

    const items = within(await screen.findByRole('menu')).getAllByRole('menuitem');
    expect(items.map((item) => item.textContent)).toEqual([
      'Public site',
      'Account settings',
      'Sign out',
    ]);
    expect(items[0]).toHaveAttribute('href', '/');
    expect(items[1]).toHaveAttribute('href', '/me');
  });

  it('names the role it is given beside the name', async () => {
    await userEvent.click(renderMenu({ ...USER, spaces: [{ spaceId: 7, role: 'OWNER' }] }, 'Owner'));

    expect(
      within(await screen.findByRole('menu')).getByText('Sara Ahmad · Owner'),
    ).toBeInTheDocument();
  });""")

D = 'pages/dashboard/shell/DashboardLayout.component.test.tsx'
edit(D, """          <DashboardLayout label="Space dashboard" header={null}>""", """          <DashboardLayout label="Space dashboard" role="Owner" header={null}>""")

edit('pages/dashboard/shell/DashboardLanguageToggle.tsx', """export function DashboardLanguageToggle({ className }: { className: string }) {""", """export function DashboardLanguageToggle({ className }: { className?: string }) {""")
print('done')
