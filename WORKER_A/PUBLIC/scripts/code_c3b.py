import io

ROOT = 'C:/dev/masaha/app/apps/web/src/features/directory/'


def sub(path, old, new, count=1):
    s = io.open(ROOT + path, encoding='utf-8', newline='').read()
    assert s.count(old) == count, (path, old[:60], s.count(old))
    s = s.replace(old, new)
    io.open(ROOT + path, 'w', encoding='utf-8', newline='').write(s)


sub('services/nearPoint.ts', """import { isInGazaStrip } from '@masaha/shared/spaces';
import type { NearPoint } from '../types/NearState';""", """import { GAZA_STRIP_BOUNDS, isInGazaStrip } from '@masaha/shared/spaces';
import type { NearPoint } from '../types/NearState';""")
sub('services/nearPoint.ts', """/** The `Masaha-Near` header's value: `lat,lng`. */""", """/**
 * A point placed by hand on the map, rounded as the device's is and held inside the Strip's box,
 * whose edge the map lets the visitor pan a little past.
 */
export function pinnedPoint({ lat, lng }: { lat: number; lng: number }): NearPoint {
  const { south, north, west, east } = GAZA_STRIP_BOUNDS;
  const rounded = roundedPoint({ latitude: lat, longitude: lng });
  return {
    lat: Math.min(Math.max(rounded.lat, south), north),
    lng: Math.min(Math.max(rounded.lng, west), east),
  };
}

/** The `Masaha-Near` header's value: `lat,lng`. */""")

p = 'hooks/near/useNearMe.ts'
sub(p, """import { judgePosition } from '../../services/nearPoint';""", """import { judgePosition, pinnedPoint } from '../../services/nearPoint';""")
sub(p, """ * answer after it is dropped. Clearing drops the point and every answer ordered by distance from it.
 */""", """ * answer after it is dropped. Clearing drops the point and every answer ordered by distance from it.
 * A point may instead be placed by hand on the map (U7): rounded and kept as the device's is, and
 * «رجوع» restores whatever was there before the pick.
 */""")
sub(p, """  clear: () => void;
} {""", """  clear: () => void;
  startPick: () => void;
  cancelPick: () => void;
  placePin: (point: { lat: number; lng: number }) => void;
} {""")
sub(p, """    stop: nearMeStore.stopSorting,""", """    stop: nearMeStore.stopSorting,
    startPick: nearMeStore.startPick,
    cancelPick: nearMeStore.cancelPick,
    placePin: (point) => {
      nearMeStore.placePin(pinnedPoint(point));
    },""")

p = 'types/LocationStatusView.ts'
sub(p, """      stop: Action | null;
      clear: Action;
    }""", """      stop: Action | null;
      /** Beside a point set by hand: set it again on the map. */
      change: Action | null;
      clear: Action;
    }""")
sub(p, """ * Near me's state line: nothing; asking, with the privacy line; a location in use, said by where it
 * came from, with the approximation and the privacy line while it sorts the list, and the ways to
 * stop and to clear it; or refused or imprecise, with the fallbacks.
 */""", """ * Near me's state line: nothing (also while a point is picked on the map); asking, with the privacy
 * line; a location in use, said by where it came from, with the approximation and the privacy line
 * while it sorts the list, and the ways to stop, change and clear it; or refused or imprecise, with
 * the fallbacks.
 */""")

p = 'hooks/near/useLocationStatus.ts'
sub(p, """ * refused states offer choosing one's area instead.
 */""", """ * refused states offer choosing one's area or setting one's location on the map instead; a point
 * set by hand offers setting it again. While a point is picked, the line is hidden (U7).
 */""")
sub(p, """  clear,
  chooseArea,
}: {
  state: NearState;
  stop: () => void;
  clear: () => void;
  chooseArea: () => void;
}): LocationStatusView {""", """  clear,
  chooseArea,
  pickOnMap,
}: {
  state: NearState;
  stop: () => void;
  clear: () => void;
  chooseArea: () => void;
  /** Starts picking a point on the map, the map shown. */
  pickOnMap: () => void;
}): LocationStatusView {""")
sub(p, """    case 'idle':
      return { kind: 'none' };""", """    case 'idle':
    case 'picking':
      return { kind: 'none' };""")
sub(p, """        stop: sorting ? { label: words.stop, run: stop } : null,""", """        stop: sorting ? { label: words.stop, run: stop } : null,
        change: state.source === 'pin' ? { label: words.change, run: pickOnMap } : null,""")
sub(p, """        fallbacks: [{ label: words.chooseArea, run: chooseArea }],""", """        fallbacks: [
          { label: words.chooseArea, run: chooseArea },
          { label: words.pickOnMap, run: pickOnMap },
        ],""")

p = 'components/near/LocationStatus.tsx'
sub(p, """      const { stop, clear } = view;""", """      const { stop, change, clear } = view;""")
sub(p, """          <Button
            variant="link"
            size="sm"
            onClick={() => {
              clear.run();
              returnFocus();
            }}
          >""", """          {change !== null && (
            <Button variant="link" size="sm" onClick={change.run}>
              {change.label}
            </Button>
          )}
          <Button
            variant="link"
            size="sm"
            onClick={() => {
              clear.run();
              returnFocus();
            }}
          >""")

p = 'hooks/list/useDirectoryList.ts'
sub(p, """    chooseArea: () => {
      if (panel.wide) focusFilters();
      else panel.sheet.setOpen(true);
    },
  });""", """    chooseArea: () => {
      if (panel.wide) focusFilters();
      else panel.sheet.setOpen(true);
    },
    // A point set by hand: on the map, with every filter kept.
    pickOnMap: () => {
      near.startPick();
      filters.apply({ view: 'map' });
    },
  });""")
print('ok')
