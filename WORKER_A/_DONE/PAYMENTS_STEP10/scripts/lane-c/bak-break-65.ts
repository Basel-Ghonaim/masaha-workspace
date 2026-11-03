import { useStore } from 'zustand';
import { createStore } from 'zustand/vanilla';

// A guest's report waiting for their sign-in (S14): in memory only, never in the address, so no link
// can open the dialog by itself; module-level, as the directory's near-me store, so it outlives the
// space's page while the guest signs in. A reload, or a recovery by email, loses it (finding 168).
const store = createStore<{ held: string | null }>()(() => ({ held: null }));

/** Holds the report a guest pressed on the space `slug`, until they come back signed in. */
export function holdReport(slug: string): void {
  store.setState({ held: slug });
}

/** Whether a report is held for `slug`: true once, the intent then cleared; another slug's is kept. */
export function takeReport(slug: string): boolean {
  if (store.getState().held !== slug) return false;
  store.setState({ held: null });
  return true;
}

/** Lets go of a held report: the guest closed the sign-in without going on. */
export function dropReport(): void {
  store.setState({ held: null });
}

/** The space whose report is held, if any; the component renders again when it changes. */
export function useHeldReport(): string | null {
  return useStore(store, (state) => state.held);
}
