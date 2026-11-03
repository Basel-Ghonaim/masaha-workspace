"""Commit 5: the account's «المفضّلة» — the users' link, the site's route, the near-me clear."""
import sys

ROOT = r'C:\dev\masaha\app-lane-c\apps\web\src'


def edit(path, old, new):
    full = ROOT + '\\' + path
    with open(full, encoding='utf8', newline='') as f:
        text = f.read()
    if text.count(old) != 1:
        sys.exit(f'{path}: anchor found {text.count(old)} times: {old[:70]}')
    text = text.replace(old, new, 1)
    with open(full, 'w', encoding='utf8', newline='') as f:
        f.write(text)


edit('features\\users\\components\\accountLinkIcons.ts', "import { FlagIcon, type IconProps } from '@shared/design-system';",
     "import { FlagIcon, HeartIcon, type IconProps } from '@shared/design-system';")
edit('features\\users\\components\\accountLinkIcons.ts', "  reports: FlagIcon,\n", "  favorites: HeartIcon,\n  reports: FlagIcon,\n")

edit('pages\\site\\navigation.ts', "export const ACCOUNT_LINKS: readonly AccountLink[] = [{ key: 'reports', to: SITE_PATHS.myReports }];",
     """export const ACCOUNT_LINKS: readonly AccountLink[] = [
  { key: 'favorites', to: SITE_PATHS.myFavorites },
  { key: 'reports', to: SITE_PATHS.myReports },
];""")

edit('pages\\site\\routes.tsx', """            children: [
              {
                path: SITE_PATHS.myReports,""", """            children: [
              {
                path: SITE_PATHS.myFavorites,
                handle: { title: (copy) => copy.favorites.list.title } satisfies TitledHandle,
                lazy: async () => {
                  const { FavoritesPage } = await import('./account/FavoritesPage');
                  return {
                    element: (
                      <RequireAuth>
                        <FavoritesPage />
                      </RequireAuth>
                    ),
                  };
                },
              },
              {
                path: SITE_PATHS.myReports,""")

# Clearing near me drops the favourites ordered from the point too.
edit('features\\directory\\hooks\\queryKeys.ts', """/** Whether a list's key holds a point: an answer ordered by distance, dropped with the location. */""",
     """/** Whether a key of the user's favourites holds a point: an answer ordered by distance from it. */
export function isNearFavorites(key: readonly unknown[]): boolean {
  const request = key[2];
  return key[1] === 'favorites' && typeof request === 'object' && request !== null && 'near' in request;
}

/** Whether a list's key holds a point: an answer ordered by distance, dropped with the location. */""")
edit('features\\directory\\hooks\\near\\useNearMe.ts', "import { directoryKeys, hasNear } from '../queryKeys';",
     "import { directoryKeys, hasNear, isNearFavorites } from '../queryKeys';")
edit('features\\directory\\hooks\\near\\useNearMe.ts', """ * answer after it is dropped. Clearing drops the point and every answer ordered by distance from it.""",
     """ * answer after it is dropped. Clearing drops the point and every answer ordered by distance from it,
 * the user's favourites among them.""")
edit('features\\directory\\hooks\\near\\useNearMe.ts', """      client.removeQueries({
        queryKey: directoryKeys.all,
        predicate: (query) => hasNear(query.queryKey),
      });""", """      client.removeQueries({
        queryKey: directoryKeys.all,
        predicate: (query) => hasNear(query.queryKey),
      });
      client.removeQueries({
        queryKey: ['me', 'favorites'],
        predicate: (query) => isNearFavorites(query.queryKey),
      });""")

edit('features\\directory\\index.ts', "export { DirectoryView } from './components/DirectoryView';",
     "export { DirectoryView } from './components/DirectoryView';\nexport { FavoritesView } from './components/favorites/FavoritesView';")
edit('features\\favorites\\index.ts', "export { FavoriteButton } from './components/FavoriteButton';",
     "export { FavoriteButton } from './components/FavoriteButton';\nexport { RemoveFavorite } from './components/RemoveFavorite';")
print('ok')
