"""Commit 4's tests: the renewal (76), the published price (spec D) and finding 171's refusal."""
W = 'C:/dev/masaha/app/apps/web/src/features/desk/'


def edit(path, pairs):
    p = W + path
    s = open(p, encoding='utf-8').read()
    for old, new in pairs:
        assert s.count(old) == 1, (path, old[:80], s.count(old))
        s = s.replace(old, new)
    open(p, 'w', encoding='utf-8', newline='').write(s)


edit('components/sheet/SubscriptionSheet.component.test.tsx', [
    ("""        choices={{ state: 'ready', packages: [OPEN_MONTH], retry: vi.fn(), shifts: [] }}""",
     """        choices={{
          state: 'ready',
          packages: [OPEN_MONTH],
          retry: vi.fn(),
          prices: { state: 'ready', list: [], refresh: vi.fn() },
          shifts: [],
        }}"""),
])

edit('hooks/sheet/useSubscriptionSheet.component.test.tsx', [
    ("""import type { SpacePackage } from '@masaha/shared/packages';""",
     """import type { SpacePackage } from '@masaha/shared/packages';
import type { Price } from '@masaha/shared/spaces';"""),
    ("""/** A line with the Unicode isolates around its values removed, as a reader hears it. */""",
     """/** The space's published student month, ₪200. */
const STUDENT_MONTH: Price = {
  period: 'MONTH',
  audience: 'STUDENT',
  shiftId: null,
  labelAr: null,
  labelEn: null,
  amountAgorot: 20000,
};

/** A line with the Unicode isolates around its values removed, as a reader hears it. */"""),
    ("""    write = () => subscribed(),
    mayTypePrice = false,
    file = customerFile(),
  }: {
    write?: (request: Request) => FakeAnswer;
    mayTypePrice?: boolean;
    file?: ReturnType<typeof customerFile>;
  } = {},
) {
  const requests = fakeTransport((request) => {
    if (request.method === 'get' && request.url?.endsWith('/visit-terms') === true) {
      return ok(visitTerms({ mayTypePrice }));
    }
    if (request.method === 'get') return ok(file);
    return write(request);
  });
  const onClose = vi.fn();""", """    write = () => subscribed(),
    mayTypePrice = false,
    file = customerFile(),
    statement,
    prices = [],
  }: {
    write?: (request: Request) => FakeAnswer;
    mayTypePrice?: boolean;
    file?: ReturnType<typeof customerFile>;
    statement?: FakeAnswer;
    prices?: Price[];
  } = {},
) {
  const requests = fakeTransport((request) => {
    if (request.method === 'get' && request.url?.endsWith('/visit-terms') === true) {
      return ok(visitTerms({ mayTypePrice }));
    }
    if (request.method === 'get' && request.url?.includes('/subscriptions/') === true) {
      return statement ?? ok({});
    }
    if (request.method === 'get') return ok(file);
    return write(request);
  });
  const onClose = vi.fn();
  const refreshPrices = vi.fn();"""),
    ("""        choices={{ state: 'ready', packages: [TEN_DAYS], retry: vi.fn(), shifts: [] }}""",
     """        choices={{
          state: 'ready',
          packages: [TEN_DAYS],
          retry: vi.fn(),
          prices: { state: 'ready', list: prices, refresh: refreshPrices },
          shifts: [],
        }}"""),
    ("""  return { requests, onClose };
}""", """  return { requests, onClose, refreshPrices };
}"""),
])

TESTS = """
  it('renews from the statement’s start, with the renewed one; a renewal renewed meanwhile is worded', async () => {
    const user = userEvent.setup();
    const renews = subscriptionState({ id: 4, packageId: 3, name: '10 days', endsOn: '2026-11-04' });
    const statement = (renewal: { startsOn: string } | null) =>
      ok({ ...renews, paidAgorot: 15000, balanceAgorot: 0, renewal, renewedById: null });
    let renewal: { startsOn: string } | null = { startsOn: '2026-11-05' };
    const { requests } = renderSheet(
      { mode: 'renew', customer: customerRow(), renews },
      {
        statement: statement({ startsOn: '2026-11-05' }),
        write: () => {
          renewal = null;
          return refused(409, { type: 'conflict', code: 'SUBSCRIPTION_ALREADY_RENEWED' });
        },
      },
    );

    const sheet = await screen.findByRole('dialog', { name: 'Renew subscription' });
    expect(await within(sheet).findByText('10 days')).toBeVisible();
    expect(within(sheet).getByRole('button', { name: 'Change package' })).toBeVisible();
    await waitFor(() => {
      expect(within(sheet).getByLabelText('From')).toHaveValue('2026-11-05');
    });
    await user.click(within(sheet).getByRole('button', { name: /Renew and receive .?₪150.?$/ }));

    expect(await within(sheet).findByText(/This subscription was already renewed\\./)).toBeVisible();
    expect(posts(requests).map(({ body }) => body)).toEqual([
      {
        packageId: 3,
        startsOn: '2026-11-05',
        renewalOfId: 4,
        payment: { amountAgorot: 15000, method: 'CASH' },
      },
    ]);
    expect(renewal).toBeNull();
  });

  it('subscribes from a published price by its key and name, never a price id, at the price’s amount', async () => {
    const user = userEvent.setup();
    const { requests } = renderSheet(
      { mode: 'subscribe', customer: customerRow() },
      { prices: [STUDENT_MONTH] },
    );

    const choice = await screen.findByRole('radio', { name: /Monthly · students/ });
    expect(choice).toBeChecked();
    await user.click(screen.getByRole('button', { name: /Save and receive .?₪200.?$/ }));

    await findToast(heard('Subscription saved · Sara Khalid'));
    const [sent] = posts(requests);
    expect(sent?.body).toEqual({
      published: { period: 'MONTH', audience: 'STUDENT', name: 'Monthly · students' },
      startsOn: expect.stringMatching(/^\\d{4}-\\d{2}-\\d{2}$/) as unknown,
      payment: { amountAgorot: 20000, method: 'CASH' },
    });
    expect(sent?.body).not.toHaveProperty('priceId');
  });

  it.each([
    ['changed or removed', refused(422, { type: 'validation', errors: { published: ['invalid_choice'] } }), /This published price changed or was removed/],
    ['now lower than the amount', refused(409, { type: 'conflict', code: 'PAYMENT_EXCEEDS_DUE' }), /The amount is more than is due now/],
  ])('says a published price %s, keeps the sheet, and reads the prices again', async (_case, answer, line) => {
    const user = userEvent.setup();
    const { refreshPrices, onClose } = renderSheet(
      { mode: 'subscribe', customer: customerRow() },
      { prices: [STUDENT_MONTH], write: () => answer },
    );

    await screen.findByRole('radio', { name: /Monthly · students/ });
    await user.click(screen.getByRole('button', { name: /Save and receive .?₪200.?$/ }));

    expect(await screen.findByText(line)).toBeVisible();
    expect(refreshPrices).toHaveBeenCalledTimes(1);
    expect(onClose).not.toHaveBeenCalled();
    expect(screen.getByRole('radio', { name: /Monthly · students/ })).toBeChecked();
  });
});
"""

p = W + 'hooks/sheet/useSubscriptionSheet.component.test.tsx'
s = open(p, encoding='utf-8').read().rstrip()
assert s.endswith('});')
s = s[:-3].rstrip() + '\n' + TESTS
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
