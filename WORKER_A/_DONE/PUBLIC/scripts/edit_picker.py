import io

ROOT = 'C:/dev/masaha/app/apps/web/src/shared/map/components/'


def sub(path, old, new, count=1):
    s = io.open(ROOT + path, encoding='utf-8', newline='').read()
    assert s.count(old) == count, (path, old[:60], s.count(old))
    s = s.replace(old, new)
    io.open(ROOT + path, 'w', encoding='utf-8', newline='').write(s)


p = 'LeafletPointPicker.tsx'
sub(p, """import { directionOf, isolate, useLanguage } from '@shared/localisation';
import {
  divIcon,
  type LatLngBoundsExpression,
  type Map as LeafletMap,
  type Marker as LeafletMarker,
} from 'leaflet';
import { useEffect, useRef, useState } from 'react';
import {
  AttributionControl,
  MapContainer,
  Marker,
  TileLayer,
  ZoomControl,
  useMap,
  useMapEvents,
} from 'react-leaflet';
import { useTileStatus } from '../hooks/useTileStatus';
import { formatCoordinates } from '../services/coordinates';
import type { MapBounds } from '../types/MapBounds';
import type { MapPoint } from '../types/MapPoint';
import type { PointPickerProps } from '../types/PointPickerProps';
import { MapFailed } from './MapFailed';

// OpenStreetMap's standard tiles, in both themes, and the page its attribution links to.
const TILES = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png';
const COPYRIGHT = 'https://www.openstreetmap.org/copyright';
const MAX_ZOOM = 19;
""", """import { isolate, useLanguage } from '@shared/localisation';
import { divIcon, type Map as LeafletMap, type Marker as LeafletMarker } from 'leaflet';
import { useEffect, useRef, useState } from 'react';
import { MapContainer, Marker, useMap, useMapEvents } from 'react-leaflet';
import { useTileStatus } from '../hooks/useTileStatus';
import { formatCoordinates } from '../services/coordinates';
import { cornersOf } from '../services/mapBox';
import type { MapPoint } from '../types/MapPoint';
import type { PointPickerProps } from '../types/PointPickerProps';
import { MapFailed } from './MapFailed';
import { MapLayers, MAX_ZOOM } from './MapLayers';
""")
sub(p, """/** A box as Leaflet takes it: its south-west and north-east corners. */
function cornersOf({ south, north, west, east }: MapBounds, margin = 0): LatLngBoundsExpression {
  const lat = (north - south) * margin;
  const lng = (east - west) * margin;
  return [
    [south - lat, west - lng],
    [north + lat, east + lng],
  ];
}

/** The attribution, linked to OpenStreetMap's copyright page; Leaflet writes it as markup. */
function attributionOf(words: string): string {
  const text = words.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
  return `<a href="${COPYRIGHT}" target="_blank" rel="noreferrer">${text}</a>`;
}

""", "")
sub(p, """  const copy = useCopy();
  const language = useLanguage();
  const rtl = directionOf(language) === 'rtl';
  const tiles = useTileStatus();""", """  const copy = useCopy();
  const tiles = useTileStatus();""")
sub(p, """          <TileLayer
            url={TILES}
            maxZoom={MAX_ZOOM}
            attribution={attributionOf(copy.map.attribution)}
            eventHandlers={tiles.handlers}
          />
          <ZoomControl
            position={rtl ? 'topright' : 'topleft'}
            zoomInTitle={copy.map.zoomIn}
            zoomOutTitle={copy.map.zoomOut}
          />
          <AttributionControl position={rtl ? 'bottomleft' : 'bottomright'} prefix={false} />
""", """          <MapLayers tileEvents={tiles.handlers} />
""")
sub(p, "      {tiles.failed && <MapFailed />}", "      {tiles.failed && <MapFailed line={copy.map.failed} />}")

p = 'PointPicker.tsx'
sub(p, """import { Skeleton } from '@shared/design-system';
import { lazy, Suspense } from 'react';
import type { PointPickerProps } from '../types/PointPickerProps';
import { MapFailed } from './MapFailed';

// Leaflet and its stylesheet load with the map, never before (docs/frontend/architecture.md §6).
// When its code cannot be fetched, as offline, the map says so as it does when its tiles fail.
const LeafletPointPicker = lazy(() =>
  import('./LeafletPointPicker').then(
    ({ LeafletPointPicker: picker }) => ({ default: picker }),
    () => ({ default: MapFailed }),
  ),
);
""", """import { useCopy } from '@shared/copy';
import { Skeleton } from '@shared/design-system';
import { lazy, Suspense } from 'react';
import type { PointPickerProps } from '../types/PointPickerProps';
import { MapFailed } from './MapFailed';

/** The picker's line when its code cannot be fetched: the one it shows when its tiles fail. */
function PickerFailed() {
  return <MapFailed line={useCopy().map.failed} />;
}

// Leaflet and its stylesheet load with the map, never before (docs/frontend/architecture.md §6).
// When its code cannot be fetched, as offline, the map says so as it does when its tiles fail.
const LeafletPointPicker = lazy(() =>
  import('./LeafletPointPicker').then(
    ({ LeafletPointPicker: picker }) => ({ default: picker }),
    () => ({ default: PickerFailed }),
  ),
);
""")
print('ok')
