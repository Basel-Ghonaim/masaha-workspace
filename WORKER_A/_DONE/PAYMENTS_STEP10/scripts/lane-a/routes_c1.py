p = r'C:\dev\masaha\app-lane-a\apps\web\src\pages\dashboard\routes.component.test.tsx'
s = open(p, encoding='utf8', newline='').read()
imp_old = "import { customerFile, customerRow, customersPage } from '../../test/deskCustomer';\n"
imp_new = "import { announcement, announcementsPage, announcementsSummary } from '../../test/announcement';\n" + imp_old
assert imp_old in s
s = s.replace(imp_old, imp_new, 1)
s = s.rstrip('\n') + '\n' + '''
describe("the space's announcements", () => {
  // The page loads lazily, as the payments' do: its first transform is done before the test.
  beforeAll(async () => {
    await import('./space/announcements/AnnouncementsPage');
  });

  /** The announcements' reads, answered as the server would, with one running announcement. */
  const serveAnnouncements = () =>
    fakeTransport((request) => {
      if (request.url === '/manage/spaces/7/announcements/summary')
        return ok(announcementsSummary());
      if (request.url === '/manage/spaces/7/announcements')
        return announcementsPage([announcement()]);
      if (request.url === '/manage/spaces') return ok([FOCUS]);
      return ok([]);
    });

  it('shows the owner the announcements under «Announcements», by state', async () => {
    asOwner();
    serveAnnouncements();
    renderDashboard('/dashboard/spaces/7/announcements');

    await topBarTitle('Announcements');
    expect(
      await screen.findByRole('tablist', { name: 'Announcement status' }),
    ).toBeInTheDocument();
    const list = await screen.findByRole('region', { name: 'Announcements' });
    expect(
      await within(list).findByText('A design workshop on Thursday evening'),
    ).toBeInTheDocument();
  });

  it('shows reception the same announcements under «Announcements»', async () => {
    asReception();
    serveAnnouncements();
    renderDashboard('/dashboard/spaces/7/announcements');

    await topBarTitle('Announcements');
    const list = await screen.findByRole('region', { name: 'Announcements' });
    expect(
      await within(list).findByText('A design workshop on Thursday evening'),
    ).toBeInTheDocument();
  });
});
'''
open(p, 'w', encoding='utf8', newline='').write(s)
