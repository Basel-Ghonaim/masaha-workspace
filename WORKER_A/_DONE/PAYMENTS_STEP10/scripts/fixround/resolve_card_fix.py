"""Resolves the favourite's fixup at «save a space from its card»: the space page's test as that commit has
it, plus the favourite's leaving test and the heart's one name."""
import io, subprocess

APP = 'C:/dev/masaha/app/'
f = 'apps/web/src/pages/site/public/space/SpacePage.component.test.tsx'
s = subprocess.run(['git', 'show', f':2:{f}'], cwd=APP, capture_output=True).stdout.decode('utf8')


def sub1(s, a, b):
    assert s.count(a) == 1, a[:60]
    return s.replace(a, b)


s = sub1(s, """    const heart = await screen.findByRole(
      'button',
      { name: /^Remove .Noor Hub. from favourites$/, hidden: true },
      { timeout: 4000 },
    );
    expect(heart).toHaveAttribute('aria-pressed', 'true');""", """    const heart = screen.getByRole('button', {
      name: /^Save .Noor Hub. to favourites$/,
      hidden: true,
    });
    await waitFor(
      () => {
        expect(heart).toHaveAttribute('aria-pressed', 'true');
      },
      { timeout: 4000 },
    );""")
s = sub1(s, """  describe('a guest who leaves for another page', () => {
""", """  describe('a guest who leaves for another page', () => {
    it('lets the held favourite go: a later sign-in in the tab saves nothing', async () => {
      stubScreenWidth(1440);
      await becomeGuest();
      const { router, requests } = await renderSpacePage();

      await userEvent.click(screen.getByRole('button', { name: /^Save .Noor Hub. to favourites$/ }));
      await screen.findByRole('dialog', { name: 'Sign in to save spaces to your favourites' });
      // Not through the prompt's links: the guest goes elsewhere on the site.
      await act(() => router.navigate('/spaces'));
      await screen.findByRole('heading', { level: 1, name: 'Workspaces' });

      act(() => {
        establishSession(aSession(), { source: 'signIn' });
      });
      await act(() => new Promise((resolve) => setTimeout(resolve, 100)));
      expect(requests.filter(({ method }) => method === 'post')).toHaveLength(0);
    });

""")
io.open(APP + f, 'w', encoding='utf8', newline='').write(s)
subprocess.run(['git', 'add', f], cwd=APP, check=True)
print('resolved', f)
