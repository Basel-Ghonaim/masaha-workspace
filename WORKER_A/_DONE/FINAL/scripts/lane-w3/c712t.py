p=r'C:\dev\masaha\app-lane-w3\apps\web\src\pages\dashboard\space\desk\DeskPage.component.test.tsx'
s=open(p,encoding='utf8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,a
    s=s.replace(a,b)
rep("type Answers = { occupancy?: () => FakeAnswer; uncollected?: () => FakeAnswer };",
"type Answers = {\n  occupancy?: () => FakeAnswer;\n  uncollected?: () => FakeAnswer;\n  checkOut?: () => FakeAnswer;\n};")
rep("""  uncollected = () => uncollectedPage([uncollectedVisit()]),
}: Answers = {}) {
  fakeTransport((request) => {
    const url = request.url ?? '';""","""  uncollected = () => uncollectedPage([uncollectedVisit()]),
  checkOut = () => ok(checkedOut(4000)),
}: Answers = {}) {
  const requests = fakeTransport((request) => {
    const url = request.url ?? '';
    if (url.endsWith('/check-out')) return checkOut();""")
rep("""  return render(
    <QueryClientProvider""","""  const view = render(
    <QueryClientProvider""")
rep("""    </QueryClientProvider>,
  );
}""","""    </QueryClientProvider>,
  );
  return { ...view, requests };
}

/** Sara, here on her subscription. */
const SARA_HERE = {
  ...NO_ONE_PRESENT,
  present: 1,
  people: [
    { kind: 'CHECK_IN', id: 3, customerId: 4, name: 'Sara Khalid', since: '2026-10-25T07:00:00.000Z' },
  ],
};""")
rep("import { uncollectedPage, uncollectedVisit, visitTerms } from '../../../../test/deskVisit';","import { checkedOut, subscriptionState } from '../../../../test/deskCustomer';\nimport { uncollectedPage, uncollectedVisit, visitTerms } from '../../../../test/deskVisit';\nimport { findToast } from '../../../../test/findToast';")
rep("""  it('shows the offline state""","""  it('opens a usage-based subscriber’s due after the tap, and receives it on the subscription', async () => {
    stubScreenWidth(1440);
    const user = userEvent.setup();
    const { requests } = renderDesk({
      occupancy: () => ok(SARA_HERE),
      checkOut: () =>
        ok({
          ...checkedOut(4000),
          subscription: subscriptionState({ name: 'Hours', billing: 'PER_HOUR', priceAgorot: 500 }),
        }),
    });
    await user.click(await screen.findByRole('button', { name: /Check out .*Sara Khalid/ }));

    const dialog = await screen.findByRole('dialog', { name: /Sara Khalid.* checked out/ });
    expect(dialog).toHaveAccessibleDescription(plain('Today 2:05 · paid ₪60') === 'Today 2:05 · paid ₪60' ? /Today .*2:05.* · paid .*₪60/ : '');
    expect(screen.getByText((content) => plain(content) === 'Left on Hours: ₪40')).toBeVisible();
    await user.click(screen.getByRole('button', { name: (name) => plain(name) === 'Receive ₪40' }));
    await vi.waitFor(() => {
      expect(requests.some((request) => request.url?.endsWith('/payments') === true)).toBe(true);
    });
    const payment = requests.find((request) => request.url?.endsWith('/payments') === true);
    expect(JSON.parse(String(payment?.data))).toEqual({
      subscriptionId: 1,
      amountAgorot: 4000,
      method: 'CASH',
    });
  });

  it('keeps a fixed subscriber’s check-out one tap, with its toast', async () => {
    stubScreenWidth(1440);
    const user = userEvent.setup();
    renderDesk({ occupancy: () => ok(SARA_HERE) });
    await user.click(await screen.findByRole('button', { name: /Check out .*Sara Khalid/ }));
    await findToast((content) => plain(content).startsWith('Sara Khalid checked out'));
    expect(screen.queryByRole('dialog')).toBeNull();
  });

  it('shows the offline state""")
open(p,'w',encoding='utf8',newline='').write(s)
