"""Commit 4: the directory's side — the saved ids, the card's and the page's slots."""
import sys

ROOT = r'C:\dev\masaha\app-lane-c\apps\web\src\features\directory'


def edit(path, old, new):
    full = ROOT + '\\' + path
    with open(full, encoding='utf8', newline='') as f:
        text = f.read()
    if text.count(old) != 1:
        sys.exit(f'{path}: anchor found {text.count(old)} times: {old[:70]}')
    text = text.replace(old, new, 1)
    with open(full, 'w', encoding='utf8', newline='') as f:
        f.write(text)


def write(path, text):
    with open(ROOT + '\\' + path, 'w', encoding='utf8', newline='') as f:
        f.write(text)


# The repository: the user's favourites, as cards.
R = 'repository\\directoryRepository.ts'
edit(R, """import {
  NEAR_HEADER,
  type DirectorySpace,
  type MapPins,
  type PublicSpace,
} from '@masaha/shared/directory';""", """import {
  NEAR_HEADER,
  type DirectorySpace,
  type FavoriteSpace,
  type MapPins,
  type PublicSpace,
} from '@masaha/shared/directory';""")
edit(R, """import type { DirectoryRequest } from '../types/DirectoryRequest';""", """import type { DirectoryRequest } from '../types/DirectoryRequest';
import type { FavoritesRequest } from '../types/FavoritesRequest';""")
edit(R, """  /** A publicly listed space's live status, by its slug. */
  status(slug: string): Promise<PublicOccupancy>;
}""", """  /** A publicly listed space's live status, by its slug. */
  status(slug: string): Promise<PublicOccupancy>;
  /**
   * The signed-in user's favourites, whole, as cards: newest saved first, or nearest first from the
   * point, which travels in the `Masaha-Near` header only; a space that left the directory by its name.
   */
  favorites(request: FavoritesRequest): Promise<FavoriteSpace[]>;
}""")
edit(R, """    status: (slug) => api.get<PublicOccupancy>(`/spaces/${encodeURIComponent(slug)}/occupancy`),
  };""", """    status: (slug) => api.get<PublicOccupancy>(`/spaces/${encodeURIComponent(slug)}/occupancy`),
    favorites: ({ near }) =>
      api.get<FavoriteSpace[]>(
        '/me/favorites',
        near === undefined
          ? undefined
          : { params: { sort: 'distance' }, headers: { [NEAR_HEADER]: nearHeader(near) } },
      ),
  };""")
write('types\\FavoritesRequest.ts', """import type { NearPoint } from './NearState';

/** How the user's favourites are asked for: newest saved first, or nearest first from a point. */
export type FavoritesRequest = { near?: NearPoint };
""")

# The keys: the favourites under the session's scope.
K = 'hooks\\queryKeys.ts'
edit(K, """import type { DirectoryRequest } from '../types/DirectoryRequest';""", """import type { DirectoryRequest } from '../types/DirectoryRequest';
import type { FavoritesRequest } from '../types/FavoritesRequest';""")
edit(K, """  status: (slug: string) => ['public', 'directory', 'status', slug] as const,
};""", """  status: (slug: string) => ['public', 'directory', 'status', slug] as const,
  /**
   * The signed-in user's favourites, under the session's scope: `{}` newest saved first (the hearts'
   * ids), `{ near }` nearest first. A favourite saved or removed reads the whole scope again (S13).
   */
  favorites: (request: FavoritesRequest) => ['me', 'favorites', request] as const,
};""")

write('hooks\\favorites\\useFavoriteIds.ts', """import type { FavoriteSpace } from '@masaha/shared/directory';
import type { AppError } from '@shared/errors';
import { useSession } from '@shared/session';
import { useQuery } from '@tanstack/react-query';
import { createDirectoryRepository } from '../../repository/directoryRepository';
import { directoryKeys } from '../queryKeys';

const repository = createDirectoryRepository();

const NEWEST = {};

/**
 * The ids of the spaces the signed-in user saved, listed or not, which the hearts read (S13): the
 * user's favourites, newest saved first, read only with a session; none (`null`) for a guest, or
 * until they have arrived.
 */
export function useFavoriteIds(): ReadonlySet<number> | null {
  const signedIn = useSession((state) => state.status === 'authenticated');
  // The repository rejects with the AppError the transport made (docs/frontend/architecture.md §7).
  const query = useQuery<FavoriteSpace[], AppError, ReadonlySet<number>>({
    queryKey: directoryKeys.favorites(NEWEST),
    queryFn: () => repository.favorites(NEWEST),
    enabled: signedIn,
    select: (favorites) => new Set(favorites.map((favorite) => favorite.space.id)),
  });
  return signedIn ? (query.data ?? null) : null;
}
""")

# The slots: the card's action and the page's heart.
S = 'types\\DirectorySlots.ts'
edit(S, """import type { ReactNode } from 'react';

/**
 * What the page sets in the directory's list: the links to the spaces, the areas' names, and the
 * place filter.
 */""", """import type { SpaceNameView } from '@shared/lib';
import type { ReactNode } from 'react';

/** A space as an action on its card or its page is handed it: whether the user saved it too. */
export type ActionSpace = { id: number; name: SpaceNameView; saved: boolean };

/**
 * What the page sets in the directory's list: the links to the spaces, the areas' names, the place
 * filter, and an action on each card.
 */""")
edit(S, """  placeFilter: (value: number[], onChange: (ids: number[]) => void) => ReactNode;
};""", """  placeFilter: (value: number[], onChange: (ids: number[]) => void) => ReactNode;
  /** An action on a space's card, beside its link: the favourite's heart. */
  cardAction?: (space: ActionSpace) => ReactNode;
};""")

V = 'types\\SpacePageView.ts'
edit(V, """/** A space, as a page's slot is handed it: its slug, its name as shown, and whether it is verified. */
export type SlotSpace = { slug: string; name: SpaceNameView; verified: boolean };""",
     """/** A space, as a page's slot is handed it: its id and slug, its name as shown, and whether it is verified. */
export type SlotSpace = { id: number; slug: string; name: SpaceNameView; verified: boolean };""")
edit('hooks\\page\\useSpacePage.ts', """        : { slug: space.slug, name, verified: space.isVerified },""",
     """        : { id: space.id, slug: space.slug, name, verified: space.isVerified },""")

# The card: the action beside its link, never inside it.
C = 'components\\card\\SpaceCard.tsx'
edit(C, """ * hours, and how far it is while the list is ordered by distance. No price.
 */
export function SpaceCard({
  card,
  href,
  areaName,
}: {
  card: SpaceCardView;
  href: string;
  areaName: ReactNode;
}) {""", """ * hours, and how far it is while the list is ordered by distance. No price. An action the page sets
 * (the heart) stands over the cover's corner, beside the link and never inside it.
 */
export function SpaceCard({
  card,
  href,
  areaName,
  action,
}: {
  card: SpaceCardView;
  href: string;
  areaName: ReactNode;
  action?: ReactNode;
}) {""")
edit(C, """  return (
    <Link
      to={href}""", """  const link = (
    <Link
      to={href}""")
edit(C, """      </Card>
    </Link>
  );
}""", """      </Card>
    </Link>
  );

  return action === undefined ? (
    link
  ) : (
    <div className="relative h-full">
      {link}
      <div className="absolute end-3 top-3">{action}</div>
    </div>
  );
}""")

DR = 'components\\list\\DirectoryResults.tsx'
edit(DR, """import type { DirectorySlots } from '../../types/DirectorySlots';""", """import { useFavoriteIds } from '../../hooks/favorites/useFavoriteIds';
import type { DirectorySlots } from '../../types/DirectorySlots';""")
edit(DR, """  const shown = useRef(page);
""", """  const shown = useRef(page);
  const saved = useFavoriteIds();
""")
edit(DR, """              href={slots.spaceLink(card.slug)}
              areaName={slots.areaName(card.areaId)}
            />""", """              href={slots.spaceLink(card.slug)}
              areaName={slots.areaName(card.areaId)}
              action={slots.cardAction?.({
                id: card.key,
                name: card.name,
                saved: saved?.has(card.key) ?? false,
              })}
            />""")
edit(DR, """ * replaces the address and so changes the page shown.
 */""", """ * replaces the address and so changes the page shown. Each card carries the page's action, told
 * whether the user saved the space.
 */""")

H = 'components\\home\\HomeSpaces.tsx'
edit(H, """import { useHomeSpaces } from '../../hooks/home/useHomeSpaces';""", """import { useFavoriteIds } from '../../hooks/favorites/useFavoriteIds';
import { useHomeSpaces } from '../../hooks/home/useHomeSpaces';
import type { DirectorySlots } from '../../types/DirectorySlots';""")
edit(H, """ * state and «تصفّح كل المساحات». The page sets the links to the spaces, the areas' names, the
 * Directory's addresses and what «اختر منطقتك» does.
 */
export function HomeSpaces({
  spaceLink,
  areaName,
  links,
  chooseArea,
}: {
  spaceLink: (slug: string) => string;
  areaName: (areaId: number) => ReactNode;
  /** The Directory's list, its spaces available now, and its map. */
  links: { list: string; available: string; map: string };
  chooseArea: () => void;
}) {""", """ * state and «تصفّح كل المساحات». The page sets the links to the spaces, the areas' names, the
 * Directory's addresses, what «اختر منطقتك» does, and an action on each card (the heart).
 */
export function HomeSpaces({
  spaceLink,
  areaName,
  links,
  chooseArea,
  cardAction,
}: {
  spaceLink: (slug: string) => string;
  areaName: (areaId: number) => ReactNode;
  /** The Directory's list, its spaces available now, and its map. */
  links: { list: string; available: string; map: string };
  chooseArea: () => void;
  cardAction?: DirectorySlots['cardAction'];
}) {""")
edit(H, """  const navigate = useNavigate();
""", """  const navigate = useNavigate();
  const saved = useFavoriteIds();
""")
edit(H, """              href={spaceLink(card.slug)}
              areaName={areaName(card.areaId)}
            />""", """              href={spaceLink(card.slug)}
              areaName={areaName(card.areaId)}
              action={cardAction?.({
                id: card.key,
                name: card.name,
                saved: saved?.has(card.key) ?? false,
              })}
            />""")

SH = 'components\\page\\SpaceHeader.tsx'
edit(SH, """ * language), its other name under it, its area, «موثّقة», and «لا توجد صور بعد» with no photo. The
 * title row holds the name alone (decision 4).
 */
export function SpaceHeader({
  header,
  areaName,
}: {
  header: NonNullable<SpacePageView['header']>;
  areaName: ReactNode;
}) {
  return (
    <div className="flex flex-col gap-2">
      <h1 className="text-heading-1" lang={header.name.lang} dir={header.name.dir}>
        {header.name.text}
      </h1>""", """ * language), its other name under it, its area, «موثّقة», and «لا توجد صور بعد» with no photo. The
 * title row holds the name and the page's action beside it, the heart (PU-014).
 */
export function SpaceHeader({
  header,
  areaName,
  action,
}: {
  header: NonNullable<SpacePageView['header']>;
  areaName: ReactNode;
  action?: ReactNode;
}) {
  return (
    <div className="flex flex-col gap-2">
      <div className="flex items-start justify-between gap-3">
        <h1 className="min-w-0 text-heading-1" lang={header.name.lang} dir={header.name.dir}>
          {header.name.text}
        </h1>
        {action !== undefined && <div className="shrink-0">{action}</div>}
      </div>""")

SD = 'components\\page\\SpaceDetails.tsx'
edit(SD, """import { useSpacePage } from '../../hooks/page/useSpacePage';""", """import { useFavoriteIds } from '../../hooks/favorites/useFavoriteIds';
import { useSpacePage } from '../../hooks/page/useSpacePage';""")
edit(SD, """import type { DirectorySlots } from '../../types/DirectorySlots';""", """import type { ActionSpace, DirectorySlots } from '../../types/DirectorySlots';""")
edit(SD, """ * The page sets the area's name, the link back to the directory and the platform's contact, and the
 * report of wrong information, drawn last in the main column (U8).
 */""", """ * The page sets the area's name, the link back to the directory and the platform's contact, the
 * heart beside the name, and the report of wrong information, drawn last in the main column (U8).
 */""")
edit(SD, """  ownerContact,
  report,
}: {""", """  ownerContact,
  heart,
  report,
}: {""")
edit(SD, """  ownerContact: ReactNode;
  /** The report of the space's wrong information, at the end of its sections. */""", """  ownerContact: ReactNode;
  /** The favourite's heart, beside the space's name, told whether the user saved it. */
  heart?: (space: ActionSpace) => ReactNode;
  /** The report of the space's wrong information, at the end of its sections. */""")
edit(SD, """  const gallery = useGallery(view.photos, view.header?.name.text ?? '');
""", """  const gallery = useGallery(view.photos, view.header?.name.text ?? '');
  const saved = useFavoriteIds();
""")
edit(SD, """        <SpaceHeader header={view.header} areaName={areaName(view.header.areaId)} />""", """        <SpaceHeader
          header={view.header}
          areaName={areaName(view.header.areaId)}
          action={
            heart === undefined || view.space === null
              ? undefined
              : heart({
                  id: view.space.id,
                  name: view.space.name,
                  saved: saved?.has(view.space.id) ?? false,
                })
          }
        />""")

I = 'index.ts'
edit(I, """export type { DirectorySlots } from './types/DirectorySlots';""", """export type { ActionSpace, DirectorySlots } from './types/DirectorySlots';""")
print('ok')
