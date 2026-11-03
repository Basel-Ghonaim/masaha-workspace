import os
os.chdir(r'C:\dev\masaha\app-lane-w2\apps\web\src')
def edit(p,pairs):
    s=open(p,encoding='utf8').read()
    for a,b in pairs:
        assert s.count(a)==1,(p,a[:70]); s=s.replace(a,b)
    open(p,'w',encoding='utf8',newline='').write(s)
def imp(p, line, after_prefix="import "):
    s=open(p,encoding='utf8').read()
    if line in s: return
    s=line+"\n"+s
    open(p,'w',encoding='utf8',newline='').write(s)

E='features/spaces/components/editor/SpaceEditor.component.test.tsx'
edit(E,[("""  it('shows each day with its state and switch, its two times when open, and the copy in its header', async () => {
    renderEditor();""","""  it('shows each day with its state and switch, its two times when open, and the copy in its header', async () => {
    stubScreenWidth(768);
    renderEditor();"""),
("""    const header = hours.querySelector('[data-slot=card-header]') as HTMLElement;
    expect(within(header).getByRole('button', { name: 'Copy to all days' })).toBeEnabled();
  });""","""    const header = hours.querySelector('[data-slot=card-header]') as HTMLElement;
    expect(within(header).getByRole('button', { name: 'Copy to all days' })).toBeEnabled();
  });

  it('a section’s header action leads its content below 768', async () => {
    stubScreenWidth(390);
    renderEditor();
    const hours = await waitFor(() => section('Opening hours'));

    const header = hours.querySelector('[data-slot=card-header]') as HTMLElement;
    expect(within(header).queryByRole('button', { name: 'Copy to all days' })).toBeNull();
    const content = hours.querySelector('[data-slot=card-content]') as HTMLElement;
    const copy = within(content).getByRole('button', { name: 'Copy to all days' });
    // First in the content, before the days.
    const saturday = within(content).getByRole('switch', { name: 'Open on Saturday' });
    expect(copy.compareDocumentPosition(saturday) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
  });

  it('a verified space’s notice leads to its reports, to correct a fact', async () => {
    renderEditor({
      read: () => ok({ ...SPACE, isVerified: true, owners: [{ id: 6, name: 'Sami' }] }),
    });

    const link = await screen.findByRole('link', { name: /reports$/ });
    expect(link).toHaveAttribute('href', '/reports?space=7');
    expect(link.parentElement?.textContent?.replace(/[\\u2066-\\u2069]/g, '')).toBe(
      'To correct a fact: Focus Hub’s reports',
    );
  });"""),
])
imp(E,"import { stubScreenWidth } from '../../../../test/screenWidth';")

M='features/spaces/components/menu/SpaceActionsMenu.component.test.tsx'
s=open(M,encoding='utf8').read().rstrip('\n'); assert s.endswith('});')
s=s[:-3]+"""
  it('a verified row’s menu reads «عرض (يعدّلها المالك)»; an unverified one’s «تعديل»', async () => {
    renderMenus();

    await userEvent.click(screen.getByRole('button', { name: /Palm Hub/ }));
    expect(await screen.findByRole('menuitem', { name: 'View (its owner edits it)' })).toHaveAttribute(
      'href',
      '/spaces/9',
    );
    await userEvent.keyboard('{Escape}');
    await userEvent.click(screen.getByRole('button', { name: /فوكس|Focus Hub/ }));
    expect(await screen.findByRole('menuitem', { name: 'Edit' })).toHaveAttribute('href', '/spaces/7');
  });
});
"""
open(M,'w',encoding='utf8',newline='').write(s)

H='features/spaces/hooks/hide/useSetSpaceHidden.component.test.tsx'
s=open(H,encoding='utf8').read().rstrip('\n'); assert s.endswith('});')
s=s[:-3]+"""
  it('hiding offers «تراجع» that shows it again', async () => {
    const { result, requests } = renderHidden(() => ({ status: 204 }));

    await act(() => result.current.hidden.mutateAsync({ ...PALM, isHidden: true }));
    const hidden = await toastTitled('Palm Hub is hidden from the site');
    await userEvent.click(within(hidden.closest('li') ?? hidden).getByRole('button', { name: 'Undo' }));

    expect(await toastTitled('Palm Hub is visible again')).toBeVisible();
    const puts = requests.filter(({ method }) => method === 'put').map(bodyOf);
    expect(puts).toEqual([{ isHidden: true }, { isHidden: false }]);
    // The undo's own toast offers no undo of its own.
    const shown = await toastTitled('Palm Hub is visible again');
    expect(within(shown.closest('li') ?? shown).queryByRole('button', { name: 'Undo' })).toBeNull();
  });
});
"""
open(H,'w',encoding='utf8',newline='').write(s)
imp(H,"import userEvent from '@testing-library/user-event';")

A='features/space-links/components/admin-list/AdminSpacesList.component.test.tsx'
s=open(A,encoding='utf8').read().rstrip('\n'); assert s.endswith('});')
s=s[:-3]+"""
  it('the phone’s sheet closes on «عرض N نتيجة»; clear is disabled with none', async () => {
    stubScreenWidth(390);
    renderList('/spaces');
    await screen.findAllByText('Focus Hub');

    await userEvent.click(screen.getByRole('button', { name: 'Filters' }));
    const sheet = await screen.findByRole('dialog', { name: 'Filters' });
    expect(within(sheet).getByRole('button', { name: 'Clear filters' })).toBeDisabled();
    await userEvent.click(within(sheet).getByRole('button', { name: 'Show 2 results' }));
    await waitFor(() => {
      expect(screen.queryByRole('dialog', { name: 'Filters' })).not.toBeInTheDocument();
    });
  });
});
"""
open(A,'w',encoding='utf8',newline='').write(s)
