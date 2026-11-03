"""Resolves «save a space from its card» over the report's fix: that commit's files plus the fix's lines."""
import io, subprocess

APP = 'C:/dev/masaha/app/'


def theirs(f):
    return subprocess.run(['git', 'show', f':3:{f}'], cwd=APP, capture_output=True).stdout.decode('utf8')


def write(f, s):
    io.open(APP + f, 'w', encoding='utf8', newline='').write(s)
    subprocess.run(['git', 'add', f], cwd=APP, check=True)
    print('resolved', f)


def sub1(s, a, b):
    assert s.count(a) == 1, a[:60]
    return s.replace(a, b)


f = 'apps/web/src/pages/site/shell/SiteLayout.tsx'
s = theirs(f)
s = sub1(s, "import { SkipLink } from './SkipLink';\n", "import { SkipLink } from './SkipLink';\nimport { useGuestIntents } from './useGuestIntents';\n")
s = sub1(s, " * once they are back (`ResumeFavorite`), whatever page they land on.\n */",
         " * once they are back (`ResumeFavorite`), whatever page they land on; a guest's held favourite and\n * report are let go once they land on another page of the site (`useGuestIntents`).\n */")
s = sub1(s, "  useMainFocus();\n", "  useMainFocus();\n  useGuestIntents();\n")
write(f, s)

f = 'apps/web/src/pages/site/public/space/SpacePage.component.test.tsx'
s = theirs(f)
s = sub1(s, """  const requests = fakeTransport((request) =>
    request.url === '/lookups'
      ? ok({ governorates: [], areas: [], amenities: [] })
      : request.url?.endsWith('/occupancy')
        ? ok({ status: null })
        : request.url === '/me/favorites'
          ? ok([])
          : request.method === 'post'
            ? { status: 204 }
            : ok(publicSpace()),""", """  const requests = fakeTransport((request) =>
    request.url === '/spaces'
      ? ok([], 200)
      : request.url === '/lookups'
        ? ok({ governorates: [], areas: [], amenities: [] })
        : request.url?.endsWith('/occupancy')
          ? ok({ status: null })
          : request.url === '/me/favorites'
            ? ok([])
            : request.method === 'post'
              ? { status: 204 }
              : ok(publicSpace()),""")
s = s.rstrip('\n')
assert s.endswith('});')
s = s[:-3] + """
  describe('a guest who leaves for another page', () => {
    it('lets the held report go: back on the page signed in, its dialog does not open', async () => {
      stubScreenWidth(1440);
      await becomeGuest();
      const { router } = await renderSpacePage();

      await userEvent.click(screen.getByRole('button', { name: 'Report wrong information' }));
      await screen.findByRole('dialog', { name: 'Sign in to report information' });
      await act(() => router.navigate('/spaces'));
      await screen.findByRole('heading', { level: 1, name: 'Workspaces' });

      act(() => {
        establishSession(aSession(), { source: 'signIn' });
      });
      await act(() => router.navigate('/spaces/noor-hub'));
      await screen.findByRole('heading', { level: 1, name: 'Noor Hub' });
      await act(() => new Promise((resolve) => setTimeout(resolve, 100)));
      expect(screen.queryByRole('dialog')).toBeNull();
    });
  });
});
"""
write(f, s)
