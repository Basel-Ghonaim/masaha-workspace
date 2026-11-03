"""F3: the statement's «⋯» (owner only, not on a voided payment) and its focus fallback, in Statement's test."""
from pathlib import Path

p = Path("C:/dev/masaha/app/apps/web/src/features/desk/components/statement/Statement.component.test.tsx")
t = p.read_text(encoding="utf-8")

old = "import { render, screen, within } from '@testing-library/react';"
assert t.count(old) == 1
t = t.replace(old, "import { render, screen, waitFor, within } from '@testing-library/react';")

old = "import { fakeTransport, ok, restoreTransport } from '../../../../test/fakeTransport';"
assert t.count(old) == 1
t = t.replace(
    old,
    "import { fakeTransport, ok, restoreTransport } from '../../../../test/fakeTransport';\n"
    "import { paymentRow } from '../../../../test/paymentRow';",
)

add = """
/** A statement with a payment not voided (₪50, id 7) beside the voided one; `voided` voids it too. */
function statementWith(voided: boolean): SubscriptionStatement {
  const payment = STATEMENT.payments[0];
  if (payment === undefined) throw new Error('the statement has a payment');
  return {
    ...STATEMENT,
    payments: [
      {
        ...payment,
        id: 7,
        amountAgorot: 5000,
        receivedAt: '2026-10-01T09:00:00Z',
        voided: voided ? { at: '2026-10-27T09:00:00Z', byId: 14, reason: 'Twice' } : null,
      },
      payment,
    ],
  };
}

/** A customer's file with one subscription, its statement opened; the void's answer voids the payment. */
async function openStatement(owner: boolean) {
  let voided = false;
  const requests = fakeTransport((request) => {
    if (request.method === 'post') {
      voided = true;
      return ok(paymentRow({ id: 7 }));
    }
    return request.url === '/manage/spaces/7/subscriptions/3'
      ? ok(statementWith(voided))
      : ok(customerFile({ subscriptions: [SUBSCRIPTION] }));
  });
  render(
    <QueryClientProvider client={createQueryClient()}>
      <main>
        <h1>Sara Khalid</h1>
        <CustomerFile spaceId={7} customerId={4} owner={owner} subscribe={() => undefined} />
      </main>
    </QueryClientProvider>,
  );
  await userEvent.click(await screen.findByRole('button', { name: 'Show the statement' }));
  const payments = await screen.findByRole('heading', { level: 4, name: 'Payments' });
  return { requests, payments };
}

/** A «⋯» of a payment, its name heard without the isolates. */
const paymentActions = () =>
  screen
    .queryAllByRole('button')
    .filter((button) =>
      (button.getAttribute('aria-label') ?? '').replace(/[⁦-⁩]/g, '').startsWith('Payment actions'),
    );

describe('Statement › a payment’s void', () => {
  it('offers the owner «⋯» on the payment not voided only; reception none', async () => {
    stubScreenWidth(1440);
    await openStatement(true);
    await waitFor(() => {
      expect(paymentActions()).toHaveLength(1);
    });
    expect(paymentActions()[0]?.getAttribute('aria-label')?.replace(/[⁦-⁩]/g, '')).toBe(
      'Payment actions: ₪50 · Sara Khalid',
    );
  });

  it('offers reception no «⋯»', async () => {
    stubScreenWidth(1440);
    await openStatement(false);
    expect(await screen.findByText('Voided: Entered twice')).toBeVisible();
    expect(paymentActions()).toHaveLength(0);
  });

  it('gives the focus to the payments’ heading once the voided payment’s «⋯» leaves', async () => {
    stubScreenWidth(1440);
    const user = userEvent.setup();
    const { requests, payments } = await openStatement(true);

    await waitFor(() => {
      expect(paymentActions()).toHaveLength(1);
    });
    await user.click(paymentActions()[0] as HTMLElement);
    await user.click(await screen.findByRole('menuitem', { name: 'Void payment…' }));
    await user.type(await screen.findByRole('textbox', { name: 'Reason' }), 'Twice');
    await user.click(screen.getByRole('button', { name: 'Void payment' }));

    // The answer lands, the statement is read again with the payment voided, and its «⋯» leaves.
    await waitFor(() => {
      expect(paymentActions()).toHaveLength(0);
    });
    await waitFor(() => {
      expect(payments).toHaveFocus();
    });
    expect(requests.filter(({ method }) => method === 'post').map(({ url }) => url)).toEqual([
      '/manage/spaces/7/payments/7/void',
    ]);
  });
});
"""
t = t.rstrip("\n") + "\n" + add
p.write_bytes(t.encode("utf-8"))
print("f3 test ok")
