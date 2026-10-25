p='C:/dev/masaha/app/apps/web/src/features/occupancy/components/PresentList.component.test.tsx'
s=open(p,encoding='utf-8',newline='').read()
s=s.replace("import { render, screen, within } from '@testing-library/react';","import { act, render, screen, waitFor, within } from '@testing-library/react';",1)
s=s.rstrip()
assert s.endswith('});')
s=s[:-3]+'''
  it('moves the focus to the next row’s action when the focused person leaves, and to the heading when no one is left', async () => {
    stubScreenWidth(1440);
    let people = NOW.people;
    fakeTransport(() => ok({ ...NOW, present: people.length, people }));
    const client = createQueryClient();
    render(
      <QueryClientProvider client={client}>
        <main>
          <PresentList spaceId={7} action={action} />
        </main>
      </QueryClientProvider>,
    );

    act(() => {
      screen.getByRole('button', { name: 'Check out Omar' }).focus();
    });
    await act(async () => {
      await screen.findByRole('button', { name: 'Check out Omar' });
    });
    screen.getByRole('button', { name: 'Check out Omar' }).focus();
    people = NOW.people.filter(({ name }) => name !== 'Omar');
    await act(async () => {
      await client.refetchQueries();
    });
    await waitFor(() => {
      expect(screen.getByRole('button', { name: 'Check out Sara' })).toHaveFocus();
    });

    people = [];
    await act(async () => {
      await client.refetchQueries();
    });
    await waitFor(() => {
      expect(screen.getByRole('heading', { level: 2, name: 'Present now 0 / 40' })).toHaveFocus();
    });
  });
});
'''
open(p,'w',encoding='utf-8',newline='').write(s)
