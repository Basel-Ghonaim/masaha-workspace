p=r'C:\dev\masaha\app-lane-w3\apps\web\src\features\desk\components\sheet\SubscriptionSheet.component.test.tsx'
s=open(p,encoding='utf8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,a
    s=s.replace(a,b)
rep("function renderSheet(entry: SheetEntry) {\n  fakeTransport((request) =>\n    request.url?.endsWith('/visit-terms') === true\n      ? ok(visitTerms({ mayTypePrice: true }))\n      : ok(customerFile()),\n  );",
"""function renderSheet(
  entry: SheetEntry,
  { file = customerFile(), prices = [] }: { file?: CustomerFile; prices?: Price[] } = {},
) {
  fakeTransport((request) =>
    request.url?.endsWith('/visit-terms') === true
      ? ok(visitTerms({ mayTypePrice: true }))
      : ok(file),
  );""")
rep("          prices: { state: 'ready', list: [], refresh: vi.fn() },","          prices: { state: 'ready', list: prices, refresh: vi.fn() },")
rep("import type { SpacePackage } from '@masaha/shared/packages';","import type { CustomerFile } from '@masaha/shared/desk';\nimport type { SpacePackage } from '@masaha/shared/packages';\nimport type { Price } from '@masaha/shared/spaces';")
rep("import { render, screen, waitFor, within } from '@testing-library/react';","import { render, screen, waitFor, within } from '@testing-library/react';\nimport userEvent from '@testing-library/user-event';")
rep("import { visitTerms } from '../../../../test/deskVisit';","import { deskVisit, visitTerms } from '../../../../test/deskVisit';")
rep("""  it.each([390, 1440])""","""  it('asks its dates with the layer’s date pickers, says a package’s end, and marks the desk’s packages private', async () => {
    const user = userEvent.setup();
    const sheet = renderSheet({ mode: 'subscribe', customer: customerRow() });
    const option = (await within(sheet).findByRole('radio', { name: /Open month/ })).closest(
      'label',
    );
    expect(option).toHaveTextContent('Private');
    expect(within(sheet).getByText('For the desk only — never shown to visitors')).toBeVisible();
    expect(sheet.querySelector('input[type="date"]')).toBeNull();
    expect(within(sheet).getByRole('button', { name: /^From / })).toHaveAttribute(
      'aria-haspopup',
      'dialog',
    );
    // A package's end is said from its validity, not a field.
    expect(within(sheet).queryByRole('textbox', { name: /^To/ })).toBeNull();
    expect(within(sheet).getByText('From the package')).toBeVisible();

    await user.click(within(sheet).getByRole('radio', { name: /Custom/ }));
    expect(await within(sheet).findByRole('button', { name: 'To No end date' })).toBeVisible();
    expect(within(sheet).getByText('No end date · it stays active until it is ended')).toBeVisible();
    await user.type(within(sheet).getByRole('textbox', { name: 'Total days' }), '12');
    expect(within(sheet).getByText('No end date · ends once 12 days are used')).toBeVisible();
  });

  it('warns of an earlier debt, lists it and the new one in the block, its due «Total»', async () => {
    const owing = customerFile({
      debtAgorot: 2000,
      unpaidVisits: [
        {
          visit: deskVisit({
            id: 9,
            checkedOutAt: '2026-07-01T09:00:00.000Z',
            checkoutMethod: 'AUTO',
          }),
          payments: [],
          paidAgorot: 0,
          balanceAgorot: 2000,
        },
      ],
    });
    const sheet = renderSheet(
      { mode: 'subscribe', customer: customerRow({ debtAgorot: 2000 }) },
      { file: owing },
    );
    await within(sheet).findByRole('radio', { name: /Open month/ });
    const plain = (text: string | null) => (text ?? '').replace(/[⁦-⁩]/g, '');
    const warning = await within(sheet).findByText((_, element) =>
      element?.getAttribute('data-slot') === 'alert-title'
        ? plain(element.textContent) === 'Owed from before: ₪20'
        : false,
    );
    expect(warning.closest('[data-slot="alert"]')).toHaveAttribute('data-variant', 'warning');
    const money = within(sheet).getByRole('group', { name: 'Payment' });
    const lines = within(money)
      .getAllByRole('listitem')
      .map((item) => plain(item.textContent));
    expect(lines.at(-1)).toBe('Subscription: Open month ₪300');
    expect(lines).toHaveLength(2);
    expect(lines[0]).toMatch(/: ₪20$/);
    expect(within(money).getByText('Total')).toBeVisible();
  });

  it('prefills a usage-based custom rate from the published price, and says how it is charged', async () => {
    const user = userEvent.setup();
    const hour: Price = {
      period: 'HOUR',
      audience: 'GENERAL',
      shiftId: null,
      labelAr: null,
      labelEn: null,
      amountAgorot: 500,
    };
    const sheet = renderSheet({ mode: 'subscribe', customer: customerRow() }, { prices: [hour] });
    await user.click(await within(sheet).findByRole('radio', { name: /Custom/ }));
    await user.click(within(sheet).getByRole('radio', { name: 'Per hour' }));
    const rate = within(sheet).getByRole('textbox', { name: 'Rate (₪)' });
    expect(rate).toHaveValue('5');
    expect(rate).toHaveAccessibleDescription('From the published price');
    expect(
      within(sheet).getByText((content) => content.replace(/[⁦-⁩]/g, '') === 'Charged by attendance: ₪5 an hour'),
    ).toBeVisible();
  });

  it.each([390, 1440])""")
open(p,'w',encoding='utf8',newline='').write(s)
