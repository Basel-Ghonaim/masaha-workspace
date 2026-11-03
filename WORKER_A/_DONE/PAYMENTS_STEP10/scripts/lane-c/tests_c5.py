"""Commit 5's test edits: the section's and the layout's «المفضّلة», RemoveFavorite's held press."""
import sys

ROOT = r'C:\dev\masaha\app-lane-c\apps\web\src'


def edit(path, old, new):
    full = ROOT + '\\' + path
    with open(full, encoding='utf8', newline='') as f:
        text = f.read()
    if text.count(old) != 1:
        sys.exit(f'{path}: anchor found {text.count(old)} times: {old[:70]}')
    text = text.replace(old, new, 1)
    with open(full, 'w', encoding='utf8', newline='') as f:
        f.write(text)


edit('features\\users\\components\\AccountMenuSection.component.test.tsx', """          links={[{ key: 'reports', to: '/me/reports' }]}
        />
      </MemoryRouter>,
    );
    const section = within(screen.getByRole('group', { name: 'Account' }));

    expect(section.getByRole('link', { name: 'My reports' })).toHaveAttribute(""", """          links={[
            { key: 'favorites', to: '/me/favorites' },
            { key: 'reports', to: '/me/reports' },
          ]}
        />
      </MemoryRouter>,
    );
    const section = within(screen.getByRole('group', { name: 'Account' }));

    expect(section.getAllByRole('link').map((link) => link.textContent)).toEqual([
      'Favourites',
      'My reports',
    ]);
    expect(section.getByRole('link', { name: 'Favourites' })).toHaveAttribute(
      'href',
      '/me/favorites',
    );
    expect(section.getByRole('link', { name: 'My reports' })).toHaveAttribute(""")

p = 'pages\\site\\account\\AccountLayout.component.test.tsx'
edit(p, """  fakeTransport((request) => (request.url === '/me/reports' ? reportsPage([]) : ok(null)));""", """  fakeTransport((request) =>
    request.url === '/me/reports'
      ? reportsPage([])
      : request.url === '/me/favorites'
        ? ok([])
        : ok(null),
  );""")
edit(p, """    const current = within(navigation).getByRole('link', { name: 'My reports' });
    expect(current).toHaveAttribute('aria-current', 'page');
    expect(current).toHaveAttribute('href', '/me/reports');""", """    const links = within(navigation).getAllByRole('link');
    expect(links.map((link) => link.textContent)).toEqual(['Favourites', 'My reports']);
    const current = within(navigation).getByRole('link', { name: 'My reports' });
    expect(current).toHaveAttribute('aria-current', 'page');
    expect(current).toHaveAttribute('href', '/me/reports');
    expect(within(navigation).getByRole('link', { name: 'Favourites' })).not.toHaveAttribute(
      'aria-current',
    );""")
full = ROOT + '\\' + p
with open(full, encoding='utf8', newline='') as f:
    text = f.read().rstrip()
assert text.endswith('});')
text = text[:-3] + """
  it('opens «Favourites» signed in, under the same navigation; axe-clean', async () => {
    establishSession(aSession(), { source: 'signIn' });
    const { container } = renderSiteAt('/me/favorites');

    const navigation = await screen.findByRole('navigation', { name: 'My account' });
    expect(within(navigation).getByRole('link', { name: 'Favourites' })).toHaveAttribute(
      'aria-current',
      'page',
    );
    expect(
      await screen.findByRole('heading', { level: 1, name: 'Favourites' }),
    ).toBeInTheDocument();
    expect(await screen.findByText('You haven’t saved any spaces yet')).toBeInTheDocument();
    expect(await axe(container)).toHaveNoViolations();
  });
});
"""
with open(full, 'w', encoding='utf8', newline='') as f:
    f.write(text)

p = 'features\\favorites\\components\\RemoveFavorite.component.test.tsx'
edit(p, """import { aSession } from '../../../test/fakeSession';""", """import type { FakeAnswer } from '../../../test/fakeAdapter';
import { aSession, deferred } from '../../../test/fakeSession';""")
edit(p, """    const requests = fakeTransport(() => ({ status: 204 }));""", """    const first = deferred<FakeAnswer>();
    const requests = fakeTransport((request) =>
      request.method === 'delete' ? first.promise : { status: 204 },
    );""")
edit(p, """    await userEvent.click(remove);
    // Held while it is sent: a second press sends nothing more.
    await userEvent.click(remove);
    const line = await findToast('Removed from favourites');""", """    await userEvent.click(remove);
    // Held while it is sent: a second press sends nothing more.
    expect(remove).toHaveAttribute('aria-disabled', 'true');
    await userEvent.click(remove);
    await act(async () => {
      first.resolve({ status: 204 });
      await first.promise;
    });
    const line = await findToast('Removed from favourites');""")
print('ok')
