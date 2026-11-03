import os
os.chdir(r'C:\dev\masaha\app-lane-w2\apps\web\src')
def edit(p,pairs):
    s=open(p,encoding='utf8').read()
    for a,b in pairs:
        assert s.count(a)==1,(p,a[:70]); s=s.replace(a,b)
    open(p,'w',encoding='utf8',newline='').write(s)
edit('features/space-links/hooks/add-owner/useAddOwnerForm.component.test.tsx',[
("""    [
      'ALREADY_OWNER',
      'This email is already an owner’s — link them to the space from their row in the list.',
    ],
  ])""","""    // With no owner named (no `details`), the code's own line.
    ['ALREADY_OWNER', 'This person is already an owner. Link them to the space instead.'],
  ])"""),
])
T='features/space-links/components/add-owner/AddOwner.component.test.tsx'
s=open(T,encoding='utf8').read().rstrip('\n')
assert s.endswith('});')
s=s[:-3]+"""
  it('ALREADY_OWNER offers «اربطه بالمساحة» opening the link dialog for that owner', async () => {
    const hadi: AdminUserRow = {
      ...RIMA,
      id: 3,
      name: 'Hadi Saleh',
      email: 'hadi@example.com',
      role: 'OWNER',
      spaces: [{ id: 9, nameEn: 'Palm Hub', nameAr: null }],
    };
    const { requests } = renderSheet({
      users: [hadi],
      add: () =>
        refused(409, { type: 'conflict', code: 'ALREADY_OWNER', details: { userId: 3 } } as never),
    });

    await fill('hadi@example.com', 'Hadi');
    await userEvent.click(screen.getByRole('button', { name: 'Create account and link' }));

    const email = screen.getByRole('textbox', { name: 'Email address' });
    expect(await screen.findByText('This email is already an owner’s.')).toBeInTheDocument();
    expect(email).toHaveAccessibleDescription('This email is already an owner’s.');
    const link = screen.getByRole('button', { name: 'Link them to the space' });
    await waitFor(() => {
      expect(link).toBeEnabled();
    });
    await userEvent.click(link);

    const dialog = await screen.findByRole('dialog', {
      name: (name) => name.replace(/[⁦-⁩]/g, '') === 'Link Hadi Saleh to a space',
    });
    // The space chosen in the sheet stays chosen.
    expect(within(dialog).getByRole('combobox', { name: /^Space/ })).toHaveTextContent('Focus Hub');
    expect(
      requests.filter((request) => request.url === '/admin/users').map((r): unknown => r.params),
    ).toEqual([{ email: 'hadi@example.com' }]);
  });
});
"""
open(T,'w',encoding='utf8',newline='').write(s)
