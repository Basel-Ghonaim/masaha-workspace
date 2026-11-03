"""Commit 4: the site's pages set the hearts; the shell resumes a guest's favourite."""
import sys

ROOT = r'C:\dev\masaha\app-lane-c\apps\web\src\pages\site'


def edit(path, old, new):
    full = ROOT + '\\' + path
    with open(full, encoding='utf8', newline='') as f:
        text = f.read()
    if text.count(old) != 1:
        sys.exit(f'{path}: anchor found {text.count(old)} times: {old[:70]}')
    text = text.replace(old, new, 1)
    with open(full, 'w', encoding='utf8', newline='') as f:
        f.write(text)


edit('navigation.ts', """  /** The signed-in user's own reports (screen 11), under the account's layout. */
  myReports: '/me/reports',""", """  /** The signed-in user's own reports (screen 11), under the account's layout. */
  myReports: '/me/reports',
  /** The signed-in user's favourites (screen 10), under the account's layout. */
  myFavorites: '/me/favorites',""")

p = 'public\\space\\SpacePage.tsx'
edit(p, """import { useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router';
import { SITE_PATHS } from '../../navigation';
import { useFooterRoom } from '../../shell/footerRoom';
import { SignInPrompt, type SignInReason } from '../SignInPrompt';""", """import { Link, useNavigate, useParams } from 'react-router';
import { SITE_PATHS } from '../../navigation';
import { useFooterRoom } from '../../shell/footerRoom';
import { useHeart } from '../useHeart';
import { useSignInPrompt } from '../useSignInPrompt';""")
edit(p, """ * platform's contact in an unverified space's dialog, and data-reports' «الإبلاغ عن معلومة غير
 * صحيحة» at their end; a guest's press of it asks them to sign in, with the reason.""", """ * platform's contact in an unverified space's dialog, favorites' heart beside its name, and
 * data-reports' «الإبلاغ عن معلومة غير صحيحة» at their end; a guest's press of either asks them to
 * sign in, with the reason.""")
edit(p, """  const navigate = useNavigate();
  // The sign-in a guest's action asked for, and what lets its held action go if they close it.
  const [prompt, setPrompt] = useState<{ reason: SignInReason; cancel: () => void } | null>(null);
  const signIn = (reason: SignInReason, cancel: () => void) => {
    setPrompt({ reason, cancel });
  };
""", """  const navigate = useNavigate();
  const { signIn, prompt } = useSignInPrompt();
  const heart = useHeart(signIn);
""")
edit(p, """        report={(space) => (""", """        heart={(space) => heart(space)}
        report={(space) => (""")
edit(p, """      <SignInPrompt
        reason={prompt?.reason ?? null}
        onClose={() => {
          prompt?.cancel();
          setPrompt(null);
        }}
      />
    </div>""", """      {prompt}
    </div>""")

p = 'public\\directory\\DirectoryPage.tsx'
edit(p, """import { publicSpacePath } from '@shared/routing';
""", """import { publicSpacePath } from '@shared/routing';
import { useHeart } from '../useHeart';
import { useSignInPrompt } from '../useSignInPrompt';
""")
edit(p, """ * space's area named and the place filtered by lookups.
 */
export function DirectoryPage() {
  const copy = useCopy();
""", """ * space's area named and the place filtered by lookups, and favorites' heart on each card; a guest's
 * press of it asks them to sign in, with the reason.
 */
export function DirectoryPage() {
  const copy = useCopy();
  const { signIn, prompt } = useSignInPrompt();
  const heart = useHeart(signIn);
""")
edit(p, """      <DirectoryView spaceLink={publicSpacePath} areaName={areaName} placeFilter={placeFilter} />
    </div>""", """      <DirectoryView
        spaceLink={publicSpacePath}
        areaName={areaName}
        placeFilter={placeFilter}
        cardAction={(space) => heart(space, { onCover: true })}
      />
      {prompt}
    </div>""")

p = 'public\\home\\HomePage.tsx'
edit(p, """import { SITE_PATHS } from '../../navigation';
""", """import { SITE_PATHS } from '../../navigation';
import { useHeart } from '../useHeart';
import { useSignInPrompt } from '../useSignInPrompt';
""")
edit(p, """ * «تصفّح حسب المنطقة», which near me's «اختر منطقتك» scrolls to and focuses; and the owners' card.
 */
export function HomePage() {
  const words = useCopy().site.home;
  const areasHeading = useRef<HTMLHeadingElement>(null);
""", """ * «تصفّح حسب المنطقة», which near me's «اختر منطقتك» scrolls to and focuses; and the owners' card.
 * Each space's card carries favorites' heart; a guest's press of it asks them to sign in.
 */
export function HomePage() {
  const words = useCopy().site.home;
  const areasHeading = useRef<HTMLHeadingElement>(null);
  const { signIn, prompt } = useSignInPrompt();
  const heart = useHeart(signIn);
""")
edit(p, """          areasHeading.current?.focus({ preventScroll: true });
        }}
      />""", """          areasHeading.current?.focus({ preventScroll: true });
        }}
        cardAction={(space) => heart(space, { onCover: true })}
      />""")
edit(p, """      <OwnersCard />
    </div>""", """      <OwnersCard />
      {prompt}
    </div>""")

p = 'shell\\SiteLayout.tsx'
edit(p, """import { useState } from 'react';
import { Outlet } from 'react-router';""", """import { ResumeFavorite } from '@features/favorites';
import { useState } from 'react';
import { Outlet, useNavigate } from 'react-router';
import { SITE_PATHS } from '../navigation';""")
edit(p, """ * takes the focus when another page opens. A page with a bar fixed at its foot reserves the
 * footer's room under it (`useFooterRoom`).
 */
export function SiteLayout() {
  useMainFocus();""", """ * takes the focus when another page opens. A page with a bar fixed at its foot reserves the
 * footer's room under it (`useFooterRoom`). A guest's favourite, held while they signed in, is saved
 * once they are back (`ResumeFavorite`), whatever page they land on.
 */
export function SiteLayout() {
  useMainFocus();
  const navigate = useNavigate();""")
edit(p, """      <SiteFooter barRoom={footerRoom} />
    </div>""", """      <SiteFooter barRoom={footerRoom} />
      <ResumeFavorite
        manage={() => {
          void navigate(SITE_PATHS.myFavorites);
        }}
      />
    </div>""")
print('ok')
