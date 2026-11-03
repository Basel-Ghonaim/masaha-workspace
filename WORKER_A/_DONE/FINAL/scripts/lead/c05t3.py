ROOT = 'C:/dev/masaha/app/apps/web/src/'
p = ROOT + 'pages/dashboard/routes.component.test.tsx'
s = open(p, encoding='utf8').read()
old = """  it('opens the drawer with the pages and the language, and closes it when a page is chosen', async () => {"""
new = """  it('keeps the top bar to the trigger and the page; the drawer opens with the account, its foot holding the language and the theme', async () => {
    const user = userEvent.setup();
    stubScreenWidth(390);
    asOwner();
    renderDashboard('/dashboard/spaces/7');

    const bar = within(await screen.findByRole('banner'));
    expect(bar.getByRole('button', { name: /Account menu/ }).parentElement).toHaveClass(
      'hidden',
      'md:flex',
    );

    await user.click(bar.getByRole('button', { name: 'Menu' }));
    const drawer = within(await screen.findByRole('dialog', { name: 'Space dashboard' }));
    const account = drawer.getByRole('button', { name: /Account menu/ });
    const switcher = await drawer.findByRole('button', { name: heard('Switch space: Focus Hub') });
    expect(account.compareDocumentPosition(switcher) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    expect(account).toHaveTextContent('· Owner');
    expect(drawer.getByRole('button', { name: 'العربية' })).toBeInTheDocument();
    expect(drawer.getByRole('button', { name: 'Dark theme' })).toBeInTheDocument();
  });

""" + old
assert s.count(old) == 1
s = s.replace(old, new)
open(p, 'w', encoding='utf8', newline='').write(s)
print('ok')
