p = r'C:\dev\masaha\app-lane-w2\apps\web\src\features\lookups\components\list\GovernoratesSection.component.test.tsx'
s = open(p, encoding='utf8', newline='').read()
def rep(old, new, n=1):
    global s
    assert s.count(old) == n, (old, s.count(old))
    s = s.replace(old, new)
rep("heard('Move up: Gaza City')", "heard('Move up: Gaza City — 1 of 2')")
rep("heard('Move down: Al-Rimal')", "heard('Move down: Al-Rimal — 1 of 2')", 2)
rep("""    expect(document.activeElement?.getAttribute('aria-label')?.replace(/[⁦-⁩]/g, '')).toMatch(
      /: Al-Rimal$/,
    );
  });""", """    expect(document.activeElement?.getAttribute('aria-label')?.replace(/[⁦-⁩]/g, '')).toBe(
      'Move up: Al-Rimal — 2 of 2',
    );
  });

  it('an arrow’s name holds its position; a move is announced', async () => {
    let list = [GAZA, RAFAH];
    renderSection((request) => {
      if (request.method === 'get') return ok(list);
      list = [{ ...GAZA, areas: [...GAZA.areas].reverse() }, RAFAH];
      return { status: 204 };
    });
    const gaza = await cardOf('Gaza City');
    const [rimal, shujaiyya] = within(gaza).getAllByRole('listitem') as [HTMLElement, HTMLElement];
    expect(
      within(shujaiyya).getByRole('button', { name: heard('Move up: Ash-Shuja’iyya — 2 of 2') }),
    ).toBeInTheDocument();
    // Nothing is said before a move.
    expect(within(rimal).getByRole('status')).toHaveTextContent('');

    await userEvent.click(
      within(rimal).getByRole('button', { name: heard('Move down: Al-Rimal — 1 of 2') }),
    );

    await waitFor(() => {
      expect(within(rimal).getByRole('status').textContent?.replace(/[⁦-⁩]/g, '')).toBe(
        'Al-Rimal: 2 of 2',
      );
    });
    expect(
      within(rimal).getByRole('button', { name: heard('Move up: Al-Rimal — 2 of 2') }),
    ).toBeInTheDocument();
    // The row that made room moved too, but said nothing: only the row moved is announced.
    expect(within(shujaiyya).getByRole('status')).toHaveTextContent('');
    expect(
      within(shujaiyya).getByRole('button', { name: heard('Move up: Ash-Shuja’iyya — 1 of 2') }),
    ).toBeInTheDocument();
  });""")
open(p, 'w', encoding='utf8', newline='').write(s)

p = r'C:\dev\masaha\app-lane-w2\apps\web\src\features\lookups\components\list\AmenitiesSection.component.test.tsx'
s = open(p, encoding='utf8', newline='').read()
rep("heard('Move up: Internet')", "heard('Move up: Internet — 1 of 2')")
rep("heard('Move down: Halls for rent')", "heard('Move down: Halls for rent — 2 of 2')")
rep("heard('Move down: Internet')", "heard('Move down: Internet — 1 of 2')")
open(p, 'w', encoding='utf8', newline='').write(s)

p = r'C:\dev\masaha\app-lane-w2\apps\web\src\features\lookups\hooks\list\useAmenityRow.component.test.tsx'
s = open(p, encoding='utf8', newline='').read()
rep("toBe('تحريك لأعلى: ⁨إنترنت⁩')", "toMatch(/^تحريك لأعلى: ⁨إنترنت⁩ — \d+ من \d+$/)")
open(p, 'w', encoding='utf8', newline='').write(s)
