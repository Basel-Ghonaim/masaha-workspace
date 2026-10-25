p='C:/dev/masaha/app/apps/web/src/pages/dashboard/routes.component.test.tsx'
s=open(p,encoding='utf-8',newline='').read()
anchor='describe("the owner\'s staff", () => {'
assert s.count(anchor)==1
block='''describe("the space's front desk", () => {
  // The page loads lazily, as the profile does: its first transform is done before the test.
  beforeAll(async () => {
    await import('./space/desk/DeskPage');
  });

  /** The desk's reads: who is present, the visit terms and the space, each from the managed route. */
  function serveDesk() {
    return fakeTransport((request) => {
      if (request.url === '/manage/spaces/7/occupancy') {
        return ok({
          status: 'AVAILABLE',
          capacity: 40,
          present: 1,
          override: null,
          people: [
            {
              kind: 'VISIT',
              id: 12,
              name: 'Omar',
              since: '2026-07-01T07:00:00.000Z',
              chargeNowAgorot: 500,
            },
          ],
        });
      }
      if (request.url === '/manage/spaces/7/visit-terms') {
        return ok({
          rounding: { rule: 'UP_AFTER_MINUTES', minutes: 15 },
          capAtDayPrice: true,
          mayTypePrice: false,
          rates: [{ shiftId: null, general: { hourAgorot: 500, dayAgorot: 2500 }, student: null }],
        });
      }
      if (request.url === '/manage/spaces/7') return ok({ ...ADDED, isVerified: true });
      if (request.url === '/manage/spaces') return ok([FOCUS]);
      return ok([]);
    });
  }

  it.each([
    ['the owner', asOwner],
    ['reception', asReception],
  ])('shows %s the desk under its title, with who is present and their check-out', async (_, as) => {
    as();
    const requests = serveDesk();
    renderDashboard('/dashboard/spaces/7/desk');

    await topBarTitle('Front desk');
    expect(
      await screen.findByRole('heading', { level: 2, name: 'Present now 1 / 40' }),
    ).toBeInTheDocument();
    expect(await screen.findByRole('button', { name: heard('Check out Omar') })).toBeInTheDocument();
    const bar = within(await screen.findByRole('banner'));
    expect(bar.getByRole('button', { name: 'Check in a visit' })).toBeInTheDocument();
    expect(bar.getByRole('button', { name: 'Switch staff' })).toBeInTheDocument();
    expect(requests.map(({ url }) => url)).toContain('/manage/spaces/7/visit-terms');
  });

  it('puts «Check in a visit» in the bar at the foot below 768 px, and «Switch staff» in the «⋯» menu', async () => {
    const user = userEvent.setup();
    stubScreenWidth(390);
    asReception();
    serveDesk();
    renderDashboard('/dashboard/spaces/7/desk');

    await topBarTitle('Front desk');
    const action = await screen.findByRole('button', { name: 'Check in a visit' });
    expect(screen.getByRole('banner')).not.toContainElement(action);
    expect(screen.getByRole('main')).not.toContainElement(action);
    await user.click(within(screen.getByRole('banner')).getByRole('button', { name: 'More actions' }));
    expect(await screen.findByRole('menuitem', { name: 'Switch staff' })).toBeInTheDocument();
  });
});

'''
s=s.replace(anchor, block+anchor,1)
open(p,'w',encoding='utf-8',newline='').write(s)
