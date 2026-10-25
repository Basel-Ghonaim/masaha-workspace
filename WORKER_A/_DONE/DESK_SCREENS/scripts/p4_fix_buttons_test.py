p = 'C:/dev/masaha/app/apps/web/src/features/desk/hooks/sheet/useSubscriptionSheet.component.test.tsx'
s = open(p, encoding='utf-8').read()
rep = [
    ("""    statement,
    prices = [],
  }: {""", """    statement,
    prices = [],
    state = 'ready',
  }: {"""),
    ("""    prices?: Price[];
  } = {},""", """    prices?: Price[];
    state?: 'ready' | 'failed';
  } = {},"""),
    ("""  const refreshPrices = vi.fn();""", """  const refreshPrices = vi.fn();
  const retryPackages = vi.fn();"""),
    ("""          state: 'ready',
          packages: [TEN_DAYS],
          retry: vi.fn(),""", """          state,
          packages: [TEN_DAYS],
          retry: retryPackages,"""),
    ("""  return { requests, onClose, refreshPrices };""", """  return { requests, onClose, refreshPrices, retryPackages };"""),
]
for a, b in rep:
    assert s.count(a) == 1, a
    s = s.replace(a, b)

TESTS = """
  it('shows every choice on «Change package», and sends nothing', async () => {
    const user = userEvent.setup();
    const renews = subscriptionState({ id: 4, packageId: 3, name: '10 days' });
    const { requests } = renderSheet(
      { mode: 'renew', customer: customerRow(), renews },
      {
        statement: () =>
          ok({
            ...renews,
            paidAgorot: 15000,
            balanceAgorot: 0,
            renewal: { startsOn: '2026-11-05' },
            renewedById: null,
          }),
      },
    );

    await user.click(await screen.findByRole('button', { name: 'Change package' }));
    expect(await screen.findByRole('radio', { name: /10 days/ })).toBeChecked();
    expect(posts(requests)).toEqual([]);
  });

  it('reads the choices again on «Try again» when they failed, and sends nothing', async () => {
    const user = userEvent.setup();
    const { requests, retryPackages, refreshPrices } = renderSheet(
      { mode: 'subscribe', customer: customerRow() },
      { state: 'failed' },
    );

    await user.click(await screen.findByRole('button', { name: 'Try again' }));
    expect(retryPackages).toHaveBeenCalledTimes(1);
    expect(refreshPrices).toHaveBeenCalledTimes(1);
    expect(posts(requests)).toEqual([]);
  });
});
"""
s = s.rstrip()
assert s.endswith('});')
s = s[:-3].rstrip() + '\n' + TESTS
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
