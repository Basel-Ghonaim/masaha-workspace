ROOT = 'C:/dev/masaha/app/apps/web/src/'


def edit(p, old, new):
    path = ROOT + p
    s = open(path, encoding='utf8').read()
    assert s.count(old) == 1, (p, old[:60])
    s = s.replace(old, new)
    open(path, 'w', encoding='utf8', newline='').write(s)


edit('features/platform-settings/public.ts', """export { PlatformContact } from './components/PlatformContact';""", """export { PlatformContact } from './components/PlatformContact';
export { usePlatformContact } from './hooks/usePlatformContact';""")

edit('pages/site/auth/ForgotPasswordPage.tsx', """import { ForgotPasswordCard } from '@features/auth';""", """import { ForgotPasswordCard } from '@features/auth';
import { usePlatformContact } from '@features/platform-settings/public';""")
edit('pages/site/auth/ForgotPasswordPage.tsx', """ * The forgotten password: the recovery's card, with the site's ways out: back to sign in (carrying
 * `next`), the contact for someone who cannot reach their email, and on to the new password once a
 * link is open.
 */
export function ForgotPasswordPage() {
  const copy = useCopy();
  const words = copy.auth.forgotPassword;
  const { search } = useLocation();
""", """ * The forgotten password: the recovery's card, with the site's ways out: back to sign in (carrying
 * `next`), the contact for someone who cannot reach their email — the platform's WhatsApp when the
 * admin set one (foundation §13 #7), else the about page's contact — and on to the new password once
 * a link is open.
 */
export function ForgotPasswordPage() {
  const copy = useCopy();
  const words = copy.auth.forgotPassword;
  const { search } = useLocation();
  const contact = usePlatformContact();
  const whatsapp =
    contact.state === 'ready'
      ? contact.channels.find((channel) => channel.kind === 'whatsapp')
      : undefined;
""")
edit('pages/site/auth/ForgotPasswordPage.tsx', """          <Link to={SITE_PATHS.contact}>{words.contactUs}</Link>""", """          {whatsapp ? (
            <a href={whatsapp.href} target="_blank" rel="noopener">
              {words.contactUs}
            </a>
          ) : (
            <Link to={SITE_PATHS.contact}>{words.contactUs}</Link>
          )}""")

edit('pages/site/auth/forgotPasswordPage.component.test.tsx', """  it('carries the return page back to sign in', async () => {""", """  it('opens the platform’s WhatsApp for someone who cannot reach their email, when it is set', async () => {
    renderSite('/forgot-password');
    fakeTransport((request) =>
      request.url === '/settings/public'
        ? ok({ email: null, whatsapp: '+970599000000' })
        : ok({ step: 'request' }),
    );
    const main = within(await screen.findByRole('main'));

    await waitFor(() => {
      expect(main.getByRole('link', { name: 'Contact us' })).toHaveAttribute(
        'href',
        'https://wa.me/970599000000',
      );
    });
    expect(main.getByRole('link', { name: 'Contact us' })).toHaveAttribute('target', '_blank');
  });

  it('carries the return page back to sign in', async () => {""")
print('ok')
