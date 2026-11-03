import { useContext, useEffect, useRef } from 'react';
import { UNSAFE_NavigationContext, useLocation, useNavigationType } from 'react-router';
import { isFirstPage } from './firstPage';

/** The element a location's hash names, if the page holds one. */
function namedBy(hash: string): HTMLElement | null {
  if (hash.length < 2) return null;
  try {
    return document.getElementById(decodeURIComponent(hash.slice(1)));
  } catch {
    return null;
  }
}

/**
 * Where the focus goes when the page changes, in every shell (130, SH-018): the document's first page
 * keeps it where the browser leaves it, however it arrived (a guard's replace on load included);
 * after it, every change of path moves it to the page's `main` (a Back or Forward included), or to
 * the element the hash names when the page holds one, also when only the hash changes (an anchored
 * section's heading). A change of the search alone moves nothing; the scroll is left to
 * `ScrollRestoration`. The shell's `main` is `id="main"` with `tabIndex={-1}`.
 */
export function useMainFocus(): void {
  const { pathname, hash } = useLocation();
  const arrival = useNavigationType();
  // The router's history, by its navigator: the first page is told apart per history.
  const { navigator } = useContext(UNSAFE_NavigationContext);
  const placed = useRef<{ pathname: string; hash: string } | null>(null);

  useEffect(() => {
    const before = placed.current;
    if (before?.pathname === pathname && before.hash === hash) return;
    placed.current = { pathname, hash };
    if (isFirstPage(navigator, arrival)) return;

    if (before?.pathname === pathname) {
      namedBy(hash)?.focus({ preventScroll: true });
      return;
    }
    (namedBy(hash) ?? document.getElementById('main'))?.focus({ preventScroll: true });
  }, [pathname, hash, arrival, navigator]);
}
