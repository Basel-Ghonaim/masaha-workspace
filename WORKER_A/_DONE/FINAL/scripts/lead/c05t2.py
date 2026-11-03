ROOT = 'C:/dev/masaha/app/apps/web/src/'


def edit(p, old, new):
    path = ROOT + p
    s = open(path, encoding='utf8').read()
    assert s.count(old) == 1, (p, old[:70])
    s = s.replace(old, new)
    open(path, 'w', encoding='utf8', newline='').write(s)


S = 'pages/site/shell/SiteLayout.component.test.tsx'
edit(S, """  it('opens the phone menu with the links, the language and sign-in, and closes it when a link is chosen', async () => {""", """  it('keeps the language in the header at every width, and the theme there from 768 px only (SH-005)', async () => {
    await renderSite('/');
    const header = within(screen.getByRole('banner'));

    expect(header.getByRole('button', { name: 'العربية' })).not.toHaveClass('hidden');
    expect(header.getByRole('button', { name: 'Dark theme' })).toHaveClass('hidden', 'md:inline-flex');
  });

  it('opens the phone menu with the links, the theme and sign-in, and closes it when a link is chosen', async () => {""")
edit(S, """    expect(menu.getByRole('button', { name: 'العربية' })).toBeInTheDocument();""", """    expect(menu.getByRole('button', { name: 'Dark theme' })).toBeInTheDocument();
    expect(menu.queryByRole('button', { name: 'العربية' })).not.toBeInTheDocument();""")

A = 'pages/site/shell/SiteAccount.component.test.tsx'
edit(A, """    expect(await accountButton()).toBeInTheDocument();
    expect(
      within(screen.getByRole('banner')).queryByRole('link', { name: 'Sign in' }),
    ).not.toBeInTheDocument();
  });""", """    expect(await accountButton()).toBeInTheDocument();
    expect(
      within(screen.getByRole('banner')).queryByRole('link', { name: 'Sign in' }),
    ).not.toBeInTheDocument();
  });

  it('shows the account as its avatar at every width, the first name beside it from 768 px', async () => {
    signIn();
    renderSite('/');

    const button = await accountButton();
    expect(button).not.toHaveClass('hidden');
    expect(within(button).getByText('Sara')).toHaveClass('hidden', 'md:inline');
  });""")
print('done')
