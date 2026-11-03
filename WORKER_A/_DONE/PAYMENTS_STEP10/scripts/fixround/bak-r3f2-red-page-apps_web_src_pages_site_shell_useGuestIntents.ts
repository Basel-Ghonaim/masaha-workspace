import { dropReport } from '@features/data-reports';
import { dropFavorite } from '@features/favorites';
import { useSession } from '@shared/session';
import { useEffect } from 'react';
import { useLocation } from 'react-router';

/** The last page the site's shell showed: where a guest's held action was pressed. */
let shown: string | null = null;

/**
 * Bounds a guest's held favourite and report to their round trip through the sign-in (S14, #129's
 * review): when a guest lands on a page of the site other than the one the shell last showed — the
 * one they pressed on — the held actions are let go, so a later sign-in in the tab saves nothing and
 * opens nothing. The sign-in and register pages are outside the site's shell, so going through them
 * and back keeps them; each also lets go by itself after its time.
 */
export function useGuestIntents(): void {
  const { pathname } = useLocation();
  const guest = useSession((state) => state.status === 'anonymous');

  useEffect(() => {
    if (guest && shown !== null && shown !== pathname) {
      dropFavorite();
      dropReport();
    }
    shown = pathname;
  }, [guest, pathname]);
}
