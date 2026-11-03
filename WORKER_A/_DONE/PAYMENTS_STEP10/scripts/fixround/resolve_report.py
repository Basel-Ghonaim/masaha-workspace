"""Resolves the report's fixup at «report wrong information»: each file as that commit has it, plus the fix."""
import io, re, subprocess

APP = 'C:/dev/masaha/app/'


def ours(f):
    return subprocess.run(['git', 'show', f':2:{f}'], cwd=APP, capture_output=True).stdout.decode('utf8')


def write(f, s):
    io.open(APP + f, 'w', encoding='utf8', newline='').write(s)
    subprocess.run(['git', 'add', f], cwd=APP, check=True)
    print('resolved', f)


def sub1(s, a, b):
    assert s.count(a) == 1, a[:60]
    return s.replace(a, b)


# The space page's test: lane C's first version, the `/spaces` answer, and the report's leaving test.
f = 'apps/web/src/pages/site/public/space/SpacePage.component.test.tsx'
s = ours(f)
s = sub1(s, """  fakeTransport((request) =>
    request.url === '/lookups'
      ? ok({ governorates: [], areas: [], amenities: [] })""", """  fakeTransport((request) =>
    request.url === '/spaces'
      ? ok([], 200)
      : request.url === '/lookups'
        ? ok({ governorates: [], areas: [], amenities: [] })""")
s = sub1(s, """      : request.url?.endsWith('/occupancy')
        ? ok({ status: null })
        : ok(publicSpace()),""", """        : request.url?.endsWith('/occupancy')
          ? ok({ status: null })
          : ok(publicSpace()),""")
s = s.rstrip('\n')
assert s.endswith('});')
s = s[:-3] + """
  describe('a guest who leaves for another page', () => {
    it('lets the held report go: back on the page signed in, its dialog does not open', async () => {
      stubScreenWidth(1440);
      await becomeGuest();
      const router = await renderSpacePage();

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

# The site's shell: this commit's, with the guest's held actions let go on another page.
f = 'apps/web/src/pages/site/shell/SiteLayout.tsx'
s = ours(f)
s = sub1(s, "import { SkipLink } from './SkipLink';\n", "import { SkipLink } from './SkipLink';\nimport { useGuestIntents } from './useGuestIntents';\n")
s = sub1(s, " * footer's room under it (`useFooterRoom`).\n */",
         " * footer's room under it (`useFooterRoom`). A guest's held actions are let go once they land on\n * another page of the site (`useGuestIntents`).\n */")
s = sub1(s, "  useMainFocus();\n", "  useMainFocus();\n  useGuestIntents();\n")
write(f, s)

# The overview: this commit's lines, the Data reports line naming the report from a space's page.
f = 'docs/project/overview.md'
s = ours(f)
s = sub1(s, "on the site, a signed-in user's «بلاغاتي» with the replies.",
         "on the site, the report of wrong information from a space's page and a signed-in user's «بلاغاتي» with the replies.")
write(f, s)
