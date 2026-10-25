p = 'C:/dev/masaha/app/apps/web/src/features/desk/hooks/sheet/useSubscriptionSheet.component.test.tsx'
s = open(p, encoding='utf-8').read()
TESTS = """
  it('says no answer, not «not saved», when the subscribe’s answer is lost, and retries with its key', async () => {
    const user = userEvent.setup();
    let lose = true;
    const { requests, onClose } = renderSheet(
      { mode: 'new', name: 'Sara Khalid', phone: '0599000305' },
      {
        write: (request) => {
          if (request.url === '/manage/spaces/7/customers') {
            return ok({ id: 9, name: 'Sara Khalid', phone: '+970599000305', archivedAt: null }, 201);
          }
          return lose ? { failure: 'ERR_NETWORK' } : subscribed();
        },
      },
    );

    await user.click(await screen.findByRole('button', { name: /Save and receive .?₪150.?$/ }));
    expect(
      await screen.findByText('No answer came back. Try again — it won’t be recorded twice.', {}, { timeout: 8000 }),
    ).toBeVisible();
    expect(screen.queryByText(/the subscription wasn’t saved/)).toBeNull();
    const lost = posts(requests).filter(({ url }) => url?.endsWith('/subscriptions') === true);
    expect(new Set(lost.map(({ key }) => key)).size).toBe(1);

    // Closed now, the sheet says nothing definite: the subscription may have been recorded.
    await user.click(screen.getByRole('button', { name: 'Close' }));
    expect(onClose).toHaveBeenCalledTimes(1);
    expect(screen.queryByText(/with no subscription/)).toBeNull();
  });

  it('retries a lost subscribe with the same key, the customer not created again', async () => {
    const user = userEvent.setup();
    let lose = true;
    const { requests } = renderSheet(
      { mode: 'new', name: 'Sara Khalid', phone: '0599000305' },
      {
        write: (request) => {
          if (request.url === '/manage/spaces/7/customers') {
            return ok({ id: 9, name: 'Sara Khalid', phone: '+970599000305', archivedAt: null }, 201);
          }
          return lose ? { failure: 'ERR_NETWORK' } : subscribed();
        },
      },
    );

    await user.click(await screen.findByRole('button', { name: /Save and receive .?₪150.?$/ }));
    await screen.findByText('No answer came back. Try again — it won’t be recorded twice.', {}, { timeout: 8000 });
    lose = false;
    await user.click(screen.getByRole('button', { name: 'Try again' }));
    await findToast(heard('Subscription saved · Sara Khalid'));
    const sent = posts(requests);
    expect(sent.filter(({ url }) => url === '/manage/spaces/7/customers')).toHaveLength(1);
    const subscribes = sent.filter(({ url }) => url?.endsWith('/subscriptions') === true);
    expect(new Set(subscribes.map(({ key }) => key)).size).toBe(1);
  });
});
"""
s = s.rstrip()
assert s.endswith('});')
s = s[:-3].rstrip() + '\n' + TESTS
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
