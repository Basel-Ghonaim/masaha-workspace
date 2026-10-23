import io

ROOT = 'C:/dev/masaha/app/apps/web/src/features/directory/'


def sub(path, old, new, count=1):
    s = io.open(ROOT + path, encoding='utf-8', newline='').read()
    assert s.count(old) == count, (path, old[:60], s.count(old))
    s = s.replace(old, new)
    io.open(ROOT + path, 'w', encoding='utf-8', newline='').write(s)


def write(path, text):
    io.open(ROOT + path, 'w', encoding='utf-8', newline='').write(text)


# The view in the filters and the address.
p = 'types/DirectoryFilters.ts'
sub(p, """/**
 * The directory's filters, order and page, as the address holds them: the budget in whole shekels,
 * an order only when one is chosen.
 */""", """/** How the directory shows the spaces: a list a page at a time, or every pin on a map. */
export type DirectoryViewKind = 'list' | 'map';

/**
 * The directory's filters, order, page and view, as the address holds them: the budget in whole
 * shekels, an order only when one is chosen.
 */""")
sub(p, """  sort: DirectoryOrder | undefined;
  page: number;
};""", """  sort: DirectoryOrder | undefined;
  page: number;
  view: DirectoryViewKind;
};""")

p = 'services/filtersOf.ts'
sub(p, """// The address's keys (S5): q, area, period, min, max, available, verified, students, friday, sort,
// page. The budget is in whole shekels, named min and max; the request sends agorot.""", """// The address's keys (S5): q, area, period, min, max, available, verified, students, friday, sort,
// page, view. The budget is in whole shekels, named min and max; the request sends agorot.""")
sub(p, """    page: wholeIn(params.get('page'), Number.MAX_SAFE_INTEGER) ?? 1,
  };
}""", """    page: wholeIn(params.get('page'), Number.MAX_SAFE_INTEGER) ?? 1,
    view: params.get('view') === 'map' ? 'map' : 'list',
  };
}""")
sub(p, """ * The address of the filters, order and page, no default written: the period only with a bound,
 * the page from 2, the order only when it differs from the one the search gives.
 */""", """ * The address of the filters, order, page and view, no default written: the period only with a
 * bound, the page from 2, the order only when it differs from the one the search gives, the view only
 * for the map.
 */""")
sub(p, """  if (filters.page !== 1) params.set('page', String(filters.page));
  return params;""", """  if (filters.page !== 1) params.set('page', String(filters.page));
  if (filters.view === 'map') params.set('view', 'map');
  return params;""")

write('services/pinMark.ts', """import type { LiveStatus } from '@masaha/shared/occupancy';
import type { MapMark } from '@shared/map';

/** Each live state's mark (U6): a shape as well as a colour, so no state is told by colour alone. */
const MARKS = {
  AVAILABLE: { shape: 'filled', tone: 'success' },
  FULL: { shape: 'bar', tone: 'warning' },
  CLOSED: { shape: 'hollow', tone: 'neutral' },
} as const satisfies Record<LiveStatus, MapMark>;

/** A space with no live status, verified or not (design issue 21). */
const NONE: MapMark = { shape: 'dashed', tone: 'muted' };

/** A pin's mark from its live status: available filled, full barred, closed hollow, none dashed. */
export function pinMark(status: LiveStatus | null): MapMark {
  return status === null ? NONE : MARKS[status];
}
""")

write('services/boundsText.ts', """import type { MapBounds } from '@shared/map';

/** The box in view as the map's read takes it: `south,west,north,east`. */
export function boundsText({ south, west, north, east }: MapBounds): string {
  return [south, west, north, east].join(',');
}
""")

write('types/PinsRequest.ts', """import type { DirectoryRequest } from './DirectoryRequest';

/**
 * The map's query, named as the contract names it: the list's filters, with no order, page,
 * language or limit, and the box in view when the map asks within it (`south,west,north,east`).
 */
export type PinsRequest = Omit<DirectoryRequest, 'limit' | 'sort' | 'lang' | 'page'> & {
  bounds?: string;
};
""")

p = 'services/requestOf.ts'
sub(p, """import { DEFAULT_PAGE_SIZE } from '@masaha/shared/core';
import type { Language } from '@shared/copy';
import type { DirectoryFilters } from '../types/DirectoryFilters';
import type { DirectoryRequest } from '../types/DirectoryRequest';
""", """import { DEFAULT_PAGE_SIZE } from '@masaha/shared/core';
import type { Language } from '@shared/copy';
import type { MapBounds } from '@shared/map';
import type { DirectoryFilters } from '../types/DirectoryFilters';
import type { DirectoryRequest } from '../types/DirectoryRequest';
import type { PinsRequest } from '../types/PinsRequest';
import { boundsText } from './boundsText';

/** The filters as the list and the map send them alike: what is left out is the server's default. */
function filtersRequestOf(filters: DirectoryFilters): Omit<PinsRequest, 'bounds'> {
  const bounded = filters.min !== undefined || filters.max !== undefined;
  return {
    ...(filters.q !== undefined && { q: filters.q }),
    ...(filters.areas.length > 0 && { area: filters.areas.join(',') }),
    ...(bounded && { period: filters.period }),
    ...(filters.min !== undefined && { priceMin: filters.min * 100 }),
    ...(filters.max !== undefined && { priceMax: filters.max * 100 }),
    ...(filters.studentPrices && { studentPrices: true }),
    ...(filters.openFriday && { openFriday: true }),
    ...(filters.verified && { verified: true }),
    ...(filters.availableNow && { availableNow: true }),
  };
}
""")
sub(p, """  const sort = byDistance ? 'distance' : filters.sort;
  const bounded = filters.min !== undefined || filters.max !== undefined;
  return {
    limit: DEFAULT_PAGE_SIZE,
    ...(filters.q !== undefined && { q: filters.q }),
    ...(filters.areas.length > 0 && { area: filters.areas.join(',') }),
    ...(bounded && { period: filters.period }),
    ...(filters.min !== undefined && { priceMin: filters.min * 100 }),
    ...(filters.max !== undefined && { priceMax: filters.max * 100 }),
    ...(filters.studentPrices && { studentPrices: true }),
    ...(filters.openFriday && { openFriday: true }),
    ...(filters.verified && { verified: true }),
    ...(filters.availableNow && { availableNow: true }),
    ...(sort !== undefined && { sort }),""", """  const sort = byDistance ? 'distance' : filters.sort;
  return {
    limit: DEFAULT_PAGE_SIZE,
    ...filtersRequestOf(filters),
    ...(sort !== undefined && { sort }),""")
s = io.open(ROOT + p, encoding='utf-8', newline='').read()
s += """
/**
 * The map's request: the list's filters, the whole set, within the box in view once the map asks
 * within it (past the pins' ceiling).
 */
export function pinsRequestOf(filters: DirectoryFilters, inView: MapBounds | null): PinsRequest {
  return { ...filtersRequestOf(filters), ...(inView !== null && { bounds: boundsText(inView) }) };
}
"""
io.open(ROOT + p, 'w', encoding='utf-8', newline='').write(s)

p = 'repository/directoryRepository.ts'
sub(p, """import { NEAR_HEADER, type DirectorySpace } from '@masaha/shared/directory';""", """import { NEAR_HEADER, type DirectorySpace, type MapPins } from '@masaha/shared/directory';""")
sub(p, """import type { NearPoint } from '../types/NearState';
""", """import type { NearPoint } from '../types/NearState';
import type { PinsRequest } from '../types/PinsRequest';
""")
sub(p, """  list(request: DirectoryRequest, near: NearPoint | null): Promise<Page<DirectorySpace[]>>;
}""", """  list(request: DirectoryRequest, near: NearPoint | null): Promise<Page<DirectorySpace[]>>;
  /** The map's pins: every space that passes the filters, up to the ceiling, or within the box. */
  pins(request: PinsRequest): Promise<MapPins>;
}""")
sub(p, """        ...(near !== null && { headers: { [NEAR_HEADER]: nearHeader(near) } }),
      }),
  };""", """        ...(near !== null && { headers: { [NEAR_HEADER]: nearHeader(near) } }),
      }),
    pins: (request) => api.get<MapPins>('/map/spaces', { params: request }),
  };""")

p = 'hooks/queryKeys.ts'
sub(p, """import type { NearPoint } from '../types/NearState';
""", """import type { NearPoint } from '../types/NearState';
import type { PinsRequest } from '../types/PinsRequest';
""")
sub(p, """    ['public', 'directory', 'list', request, near] as const,
};""", """    ['public', 'directory', 'list', request, near] as const,
  /** The map's pins, one key per request. */
  pins: (request: PinsRequest) => ['public', 'directory', 'pins', request] as const,
};""")

p = 'services/cardView.ts'
sub(p, """import type { DirectorySpace } from '@masaha/shared/directory';""", """import type { DirectorySpace, MapPin } from '@masaha/shared/directory';""")
sub(p, """ * the order stops says no distance. No price.
 */
export function cardViewOf(
  space: DirectorySpace,""", """ * the order stops says no distance. A map's pin makes the same card, its area by its id. No price.
 */
export function cardViewOf(
  space: DirectorySpace | MapPin,""")
sub(p, """    areaId: space.area.id,""", """    areaId: 'areaId' in space ? space.areaId : space.area.id,""")
sub(p, """      !byDistance || space.distanceMeters === undefined
        ? null""", """      !byDistance || !('distanceMeters' in space) || space.distanceMeters === undefined
        ? null""")
print('ok')
