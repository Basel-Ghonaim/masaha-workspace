p = r'C:\dev\masaha\app-lane-w2\apps\web\src\features\lookups\components\sheet\AmenitySheet.component.test.tsx'
s = open(p, encoding='utf8', newline='').read()
def rep(old, new):
    global s
    assert s.count(old) == 1, old
    s = s.replace(old, new)
rep("""  it('shows the Active switch alone, with its hint', async () => {
    await renderSection();

    const sheet = await editInternet();

    const active = within(sheet).getByRole('switch', { name: 'Active' });
    expect(within(sheet).getAllByRole('switch')).toEqual([active]);
    expect(active).toBeChecked();
    expect(active).toHaveAccessibleDescription(
      'Inactive: not offered in forms; spaces that have it keep it.',
    );
  });""", """  it('the edit sheet has no active switch', async () => {
    await renderSection();

    const sheet = await editInternet();

    expect(within(sheet).getAllByRole('textbox')).toHaveLength(2);
    expect(within(sheet).getByRole('radiogroup', { name: 'Icon' })).toBeInTheDocument();
    expect(within(sheet).queryByRole('switch')).not.toBeInTheDocument();
    // The row keeps its switch: the one control of whether it is offered.
    expect(screen.getByRole('switch', { name: heard('Active: Internet') })).toBeChecked();
  });

  it('a list of 11 offers «الترتيب» and moves the amenity there', async () => {
    const eleven: AdminAmenity[] = Array.from({ length: 11 }, (_, index) => ({
      ...INTERNET,
      id: 20 + index,
      key: `amenity_${String(index + 1)}`,
      nameEn: `Amenity ${String(index + 1)}`,
    }));
    const requests = fakeTransport((request) =>
      request.method === 'get'
        ? ok(eleven)
        : request.method === 'put'
          ? { status: 204 }
          : ok(eleven[0]),
    );
    const Wrapper = queryWrapper();
    render(
      <Wrapper>
        <AmenitiesSection />
      </Wrapper>,
    );
    await screen.findByRole('list');

    await userEvent.click(screen.getByRole('button', { name: heard('Edit: Amenity 1') }));
    const sheet = await screen.findByRole('dialog', { name: 'Edit amenity' });
    const position = within(sheet).getByRole('textbox', { name: 'Position' });
    expect(position).toHaveValue('1');
    expect(position).toHaveAccessibleDescription('From 1 to 11');
    await userEvent.clear(position);
    await userEvent.type(position, '3');
    await userEvent.click(within(sheet).getByRole('button', { name: 'Save' }));

    await waitFor(() => {
      expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    });
    const writes = requests.filter(({ method }) => method !== 'get');
    expect(writes.map(({ method, url }) => `${String(method)} ${String(url)}`)).toEqual([
      'patch /admin/amenities/20',
      'put /admin/amenities/order',
    ]);
    expect(bodyOf(writes[1])).toEqual({ ids: [21, 22, 20, 23, 24, 25, 26, 27, 28, 29, 30] });
  });""")
rep("import { render, screen, within } from '@testing-library/react';", "import { render, screen, waitFor, within } from '@testing-library/react';")
rep("import { fakeTransport, ok, restoreTransport } from '../../../../test/fakeTransport';", "import { bodyOf, fakeTransport, ok, restoreTransport } from '../../../../test/fakeTransport';")
open(p, 'w', encoding='utf8', newline='').write(s)
