"""Commit 5's words: favorites.list, site.account.favorites, users.account.links.favorites."""
import sys

ROOT = r'C:\dev\masaha\app-lane-c\apps\web\src\shared\copy'


def edit(path, old, new):
    full = ROOT + '\\' + path
    with open(full, encoding='utf8', newline='') as f:
        text = f.read()
    if text.count(old) != 1:
        sys.exit(f'{path}: anchor found {text.count(old)} times')
    text = text.replace(old, new, 1)
    with open(full, 'w', encoding='utf8', newline='') as f:
        f.write(text)


edit('english\\favorites.ts', "/** A signed-in user's favourites on the site: the heart on the cards and on a space's page. */",
     "/**\n * A signed-in user's favourites on the site: the heart on the cards and on a space's page, and the\n * account's «المفضّلة».\n */")
edit('english\\favorites.ts', """  manage: 'Manage favourites',
} as const;""", """  manage: 'Manage favourites',
  /** The account's «المفضّلة» (screen 10). */
  list: {
    title: 'Favourites',
    description: 'The spaces you saved, with their status now.',
    count: ({ count }: { count: number }) =>
      englishPlural(count, {
        one: `${String(count)} saved space`,
        other: `${String(count)} saved spaces`,
      }),
    /** A space that left the directory (C7). */
    gone: 'This space is no longer listed in the directory',
    remove: 'Remove',
    empty: {
      title: 'You haven’t saved any spaces yet',
      text: 'Tap the heart on any space’s page to find it here.',
    },
    loadFailed: 'We couldn’t load your favourites',
    region: 'Saved spaces',
  },
} as const;""")
edit('english\\favorites.ts', "/**\n * A signed-in user's favourites", "import { englishPlural } from '../plural';\n\n/**\n * A signed-in user's favourites")
edit('arabic\\favorites.ts', "import type { Catalogue } from '../shape';", "import { arabicPlural } from '../plural';\nimport type { Catalogue } from '../shape';")
edit('arabic\\favorites.ts', """  manage: 'إدارة المفضّلة',
} satisfies Catalogue['favorites'];""", """  manage: 'إدارة المفضّلة',
  list: {
    title: 'المفضّلة',
    description: 'المساحات التي حفظتها، بحالتها الآن.',
    count: ({ count }: { count: number }) =>
      arabicPlural(count, {
        zero: 'لا مساحات محفوظة',
        one: 'مساحة واحدة محفوظة',
        two: 'مساحتان محفوظتان',
        few: `${String(count)} مساحات محفوظة`,
        many: `${String(count)} مساحة محفوظة`,
        other: `${String(count)} مساحة محفوظة`,
      }),
    gone: 'لم تعد هذه المساحة معروضة في الدليل',
    remove: 'إزالة',
    empty: {
      title: 'لم تحفظ أي مساحة بعد',
      text: 'اضغط على القلب في صفحة أي مساحة لتجدها هنا.',
    },
    loadFailed: 'تعذّر تحميل المفضّلة',
    region: 'المساحات المحفوظة',
  },
} satisfies Catalogue['favorites'];""")

edit('english\\site.ts', """    navigation: 'My account',
    reports: 'My reports',""", """    navigation: 'My account',
    favorites: 'Favourites',
    reports: 'My reports',""")
edit('arabic\\site.ts', """    navigation: 'حسابي',
    reports: 'بلاغاتي',""", """    navigation: 'حسابي',
    favorites: 'المفضّلة',
    reports: 'بلاغاتي',""")
edit('english\\users.ts', "    links: { reports: 'My reports' },", "    links: { favorites: 'Favourites', reports: 'My reports' },")
edit('arabic\\users.ts', "    links: { reports: 'بلاغاتي' },", "    links: { favorites: 'المفضّلة', reports: 'بلاغاتي' },")
print('ok')
