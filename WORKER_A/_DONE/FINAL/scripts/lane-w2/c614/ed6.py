p = 'C:/dev/masaha/app-lane-w2/apps/web/src/pages/dashboard/routes.component.test.tsx'
s = open(p, encoding='utf8', newline='').read()
old = """  it('names its tabs after the page, with its hint under them', async () => {
    openLookups('');

    expect(await screen.findByRole('tablist', { name: 'Lookups' })).toBeInTheDocument();
    expect(
      screen.getByText(
        'Hidden: not shown in filters and forms. Spaces already using it stay as they are. The order here is the display order.',
      ),
    ).toBeInTheDocument();
  });"""
new = """  it('names its tabs after the page, each tab with its own hint under them', async () => {
    openLookups('');
    const governorates =
      'Hidden: not shown in filters and forms. Spaces already using it stay as they are. The order here is the display order.';
    const amenities =
      'An inactive amenity is offered in no form; the spaces that have it keep it. The order here is the order shown.';

    expect(await screen.findByRole('tablist', { name: 'Lookups' })).toBeInTheDocument();
    expect(screen.getByText(governorates)).toBeInTheDocument();
    expect(screen.queryByText(amenities)).not.toBeInTheDocument();

    await userEvent.click(screen.getByRole('tab', { name: 'Amenities' }));

    expect(await screen.findByText(amenities)).toBeInTheDocument();
    expect(screen.queryByText(governorates)).not.toBeInTheDocument();
  });"""
assert s.count(old) == 1
s = s.replace(old, new)
open(p, 'w', encoding='utf8', newline='').write(s)
print('ok')
