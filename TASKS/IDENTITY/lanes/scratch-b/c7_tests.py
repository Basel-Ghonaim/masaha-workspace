"""C7's tests (T18, T19): written before the shells change, so each is seen failing first."""
from pathlib import Path

ROOT = Path(r"C:\dev\masaha\app-design-lane-b\apps\web\src")


def edit(relative, old, new):
    path = ROOT / relative
    with open(path, encoding="utf-8", newline="") as handle:
        text = handle.read()
    if text.count(old) != 1:
        raise SystemExit(f"{relative}: expected one match, found {text.count(old)}")
    text = text.replace(old, new)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    print(f"edited {relative}")


# T18 — the site's header and the phone menu.
edit(
    "pages/site/shell/SiteLayout.component.test.tsx",
    """  it('links the footer to about, to the privacy policy and to the contact section', async () => {""",
    """  it('draws the logo in the header’s home link, which it names «Masaha», and «مساحة» in Arabic', async () => {
    const user = userEvent.setup();
    await renderSite('/');
    const home = within(screen.getByRole('banner')).getByRole('link', { name: 'Masaha' });

    expect(within(home).getByRole('img', { name: 'Masaha' })).toBeInTheDocument();

    await user.click(within(screen.getByRole('banner')).getByRole('button', { name: 'العربية' }));

    const homeInArabic = within(screen.getByRole('banner')).getByRole('link', { name: 'مساحة' });
    expect(within(homeInArabic).getByRole('img', { name: 'مساحة' })).toBeInTheDocument();
  });

  it('links the footer to about, to the privacy policy and to the contact section', async () => {""",
)

edit(
    "pages/site/shell/SiteLayout.component.test.tsx",
    """  it('offers «تخطَّ إلى المحتوى» first, leading to the page’s main content', async () => {""",
    """  it('draws the logo, named «Masaha», at the head of the phone menu, which keeps its own name', async () => {
    const user = userEvent.setup();
    await renderSite('/');

    await user.click(screen.getByRole('button', { name: 'Menu' }));

    const menu = within(screen.getByRole('dialog', { name: 'Menu' }));
    expect(menu.getByRole('img', { name: 'Masaha' })).toBeInTheDocument();
  });

  it('offers «تخطَّ إلى المحتوى» first, leading to the page’s main content', async () => {""",
)

# T18 — the focus shell's header (the forced change).
edit(
    "pages/site/auth/changePasswordPage.component.test.tsx",
    """  it('shows the change in the focus shell, whose short header offers only the wordmark and sign-out', async () => {""",
    """  it('shows the change in the focus shell, whose short header offers only the logo, linking home, and sign-out', async () => {""",
)
edit(
    "pages/site/auth/changePasswordPage.component.test.tsx",
    """    expect(header.getByRole('link', { name: 'Masaha' })).toBeInTheDocument();
""",
    """    const home = header.getByRole('link', { name: 'Masaha' });
    expect(home).toHaveAttribute('href', '/');
    expect(within(home).getByRole('img', { name: 'Masaha' })).toBeInTheDocument();
""",
)

# T19 — the admin's sidebar header.
edit(
    "pages/dashboard/routes.component.test.tsx",
    """  it('shows the admin the lookups page: its title in the top bar, and the governorates', async () => {""",
    """  it('heads the admin’s sidebar with the logo hidden from assistive technology, «مساحة» read once beside «إدارة المنصة», and no «م» tile', async () => {
    startPreferences('ar');
    stubScreenWidth(1280);
    signIn({ role: 'ADMIN' });
    renderDashboard('/dashboard/admin');

    const nav = await screen.findByRole('navigation', { name: 'لوحة إدارة المنصة' });
    const header = nav.querySelector<HTMLElement>('[data-slot="sidebar-header"]');
    if (header === null) throw new Error('The sidebar has no header');
    const head = within(header);
    expect(head.queryByText('م')).not.toBeInTheDocument();
    expect(header.querySelector('[data-slot="logo"]')).toHaveAttribute('aria-hidden', 'true');
    expect(head.queryByRole('img')).not.toBeInTheDocument();
    expect(head.getByText('مساحة')).toHaveClass('sr-only');
    expect(head.getByText('إدارة المنصة')).not.toHaveClass('sr-only');
  });

  it('shows the admin the lookups page: its title in the top bar, and the governorates', async () => {""",
)
