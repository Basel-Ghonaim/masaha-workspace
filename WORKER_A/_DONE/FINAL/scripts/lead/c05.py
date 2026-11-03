import os

ROOT = 'C:/dev/masaha/app/apps/web/src/'


def edit(p, old, new):
    path = ROOT + p
    s = open(path, encoding='utf8').read()
    assert s.count(old) == 1, (p, old[:70])
    s = s.replace(old, new)
    open(path, 'w', encoding='utf8', newline='').write(s)


def write(p, text):
    path = ROOT + p
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf8', newline='').write(text)


# --- the account's settings path, which both groups link to
edit('shared/routing/returnUrl.ts', """/**
 * Where a reset link opens,""", """/**
 * The signed-in user's own settings (screen 9): the site routes it, and the dashboard's account menu
 * links to it, so its path lives where both groups read it.
 */
export const ACCOUNT_SETTINGS_PATH = '/me';

/**
 * Where a reset link opens,""")
edit('shared/routing/index.ts', """export { CHANGE_PASSWORD_PATH, RESET_PASSWORD_PATH, SIGN_IN_PATH } from './returnUrl';""", """export {
  ACCOUNT_SETTINGS_PATH,
  CHANGE_PASSWORD_PATH,
  RESET_PASSWORD_PATH,
  SIGN_IN_PATH,
} from './returnUrl';""")

# --- copy
edit('shared/copy/english/users.ts', """  /** The site's account menu: its links to the account's pages (P4). */
  account: {
    links: { favorites: 'Favourites', reports: 'My reports' },
  },""", """  /** The site's account menu: its links to the account's pages (P4). */
  account: {
    links: { favorites: 'Favourites', reports: 'My reports', settings: 'Account settings' },
  },
  /** The role beside the name in the dashboard's account menu: the role at the space, or the admin. */
  roles: { OWNER: 'Owner', RECEPTION: 'Reception', ADMIN: 'Admin' },
  /** The dashboard's account menu: the way back to the public site. */
  publicSite: 'Public site',
  /** The account menu's label with a role: the name, then the role. */
  nameWithRole: ({ name, role }: { name: string; role: string }) => `${name} · ${role}`,""")
edit('shared/copy/arabic/users.ts', """    links: { favorites: 'المفضّلة', reports: 'بلاغاتي' },""", """    links: { favorites: 'المفضّلة', reports: 'بلاغاتي', settings: 'إعدادات حسابي' },""")

print('check arabic account block')
