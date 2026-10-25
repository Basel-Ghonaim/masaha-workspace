p = 'C:/dev/masaha/app/apps/web/src/features/desk/hooks/sheet/useSubscriptionSheet.component.test.tsx'
s = open(p, encoding='utf-8').read()
TESTS = """
  it.each([
    ['₪200 on a ₪150 price records ₪150', '200', 15000],
    ['₪100 on a ₪150 price records ₪100', '100', 10000],
  ])('sends the amount recorded, never the amount typed: %s', async (_case, typed, recorded) => {
    const user = userEvent.setup();
    const { requests } = renderSheet({ mode: 'subscribe', customer: customerRow() });

    await screen.findByRole('radio', { name: /10 days/ });
    const received = screen.getByRole('textbox', { name: 'Received now (₪)' });
    await user.clear(received);
    await user.type(received, typed);
    await user.click(screen.getByRole('button', { name: /Save and receive/ }));

    await findToast(heard('Subscription saved · Sara Khalid'));
    const [sent] = posts(requests);
    expect(sent?.body).toMatchObject({ payment: { amountAgorot: recorded, method: 'CASH' } });
  });
});
"""
s = s.rstrip()
assert s.endswith('});')
s = s[:-3].rstrip() + '\n' + TESTS
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
