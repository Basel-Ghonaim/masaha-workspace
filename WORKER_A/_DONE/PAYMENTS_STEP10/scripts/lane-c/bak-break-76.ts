import type { SpaceNameView } from '@shared/lib';

/** A favourite a guest pressed: the space, and its name as the card or the page showed it. */
export type HeldFavorite = { spaceId: number; name: SpaceNameView };

// A guest's favourite waiting for their sign-in (S14): in memory only, never in the address, so no
// link can save a space by itself; module-level, as the directory's near-me store, so it outlives the
// page while the guest signs in. A reload, or a recovery by email, loses it (finding 168).
let held: HeldFavorite | null = null;

/** Holds the favourite a guest pressed, until they come back signed in. */
export function holdFavorite(favorite: HeldFavorite): void {
  held = favorite;
}

/** The favourite held, once: it is cleared as it is taken. */
export function takeFavorite(): HeldFavorite | null {
  const taken = held;
  held = null;
  return taken;
}

/** Lets go of a held favourite: the guest closed the sign-in without going on. */
export function dropFavorite(): void {
  held = null;
}
