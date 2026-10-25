p = 'C:/dev/masaha/app/apps/web/src/features/desk/hooks/sheet/useSubscriptionSheet.component.test.tsx'
s = open(p, encoding='utf-8').read()
TESTS = """
  it('renews a subscription from a published price with that price chosen, its amount on the submit', async () => {
    const renews = subscriptionState({
      id: 4,
      packageId: null,
      priceTyped: null,
      name: 'Monthly',
      priceAgorot: 35000,
      startsOn: '2026-10-01',
      endsOn: '2026-10-30',
    });
    renderSheet(
      { mode: 'renew', customer: customerRow(), renews },
      {
        prices: [
          { ...STUDENT_MONTH, period: 'WEEK', audience: 'GENERAL', amountAgorot: 12000 },
          { ...STUDENT_MONTH, audience: 'GENERAL', amountAgorot: 35000 },
        ],
        statement: () =>
          ok({
            ...renews,
            paidAgorot: 35000,
            balanceAgorot: 0,
            renewal: { startsOn: '2026-10-31' },
            renewedById: null,
          }),
      },
    );

    const sheet = await screen.findByRole('dialog', { name: 'Renew subscription' });
    expect(await within(sheet).findByRole('button', { name: 'Change package' })).toBeVisible();
    expect(within(sheet).getByText('Monthly')).toBeVisible();
    expect(
      await within(sheet).findByRole('button', { name: /Renew and receive .?₪350.?$/ }),
    ).toBeEnabled();
  });

  it('chooses nothing for a renewal it cannot match, the submit blocked until a choice', async () => {
    const user = userEvent.setup();
    const renews = subscriptionState({
      id: 4,
      packageId: null,
      priceTyped: null,
      name: 'An old offer',
      priceAgorot: 9000,
      startsOn: '2026-10-01',
      endsOn: '2026-10-10',
    });
    renderSheet(
      { mode: 'renew', customer: customerRow(), renews },
      {
        prices: [{ ...STUDENT_MONTH, period: 'WEEK', audience: 'GENERAL', amountAgorot: 12000 }],
        statement: () =>
          ok({
            ...renews,
            paidAgorot: 9000,
            balanceAgorot: 0,
            renewal: { startsOn: '2026-10-26' },
            renewedById: null,
          }),
      },
    );

    const weekly = await screen.findByRole('radio', { name: /Weekly/ });
    await waitFor(() => {
      expect(screen.getByLabelText('From')).toHaveValue('2026-10-26');
    });
    expect(weekly).not.toBeChecked();
    expect(screen.getByRole('radio', { name: /10 days/ })).not.toBeChecked();
    const submit = screen.getByRole('button', { name: /Renew without payment/ });
    expect(submit).toBeDisabled();
    await user.click(weekly);
    expect(screen.getByRole('button', { name: /Renew and receive .?₪120.?$/ })).toBeEnabled();
  });
});
"""
s = s.rstrip()
assert s.endswith('});')
s = s[:-3].rstrip() + '\n' + TESTS
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
