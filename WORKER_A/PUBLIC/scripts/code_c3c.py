import io

ROOT = 'C:/dev/masaha/app/apps/web/src/features/directory/'


def sub(path, old, new, count=1):
    s = io.open(ROOT + path, encoding='utf-8', newline='').read()
    assert s.count(old) == count, (path, old[:60], s.count(old))
    s = s.replace(old, new)
    io.open(ROOT + path, 'w', encoding='utf-8', newline='').write(s)


p = 'hooks/map/useDirectoryMap.ts'
sub(p, """ * marks; a change of filter asks for the whole set again and clears the choice.
 */""", """ * marks; a change of filter asks for the whole set again and clears the choice. While a point is
 * picked by hand (U7), a crosshair stands at the centre, the marks cannot be chosen, and near me's
 * button, its line, «مركّز على موقعي» and the chosen space are hidden.
 */""")
sub(p, """    chooseArea: () => {
      panel.sheet.setOpen(true);
    },
  });""", """    chooseArea: () => {
      panel.sheet.setOpen(true);
    },
    pickOnMap: near.startPick,
  });""")
sub(p, """  const chosen = shownPins.find((pin) => pin.id === selection.selectedId) ?? null;
  const point = near.state.point;""", """  const picking = near.state.status === 'picking';
  const chosen = picking
    ? null
    : (shownPins.find((pin) => pin.id === selection.selectedId) ?? null);
  const point = near.state.point;""")
sub(p, """      user: point === null ? null : { point, label: words.map.you },""", """      user:
        point === null
          ? null
          : { point, label: near.state.source === 'pin' ? words.map.yourPin : words.map.you },""")
sub(p, """      pick: null,""", """      pick: picking ? { onPick: near.placePin, keys: words.pick.keys } : null,""")
sub(p, """    centre: point === null ? null : words.map.centre,""", """    centre: point === null || picking ? null : words.map.centre,
    pick: picking
      ? {
          title: words.pick.title,
          text: words.pick.text,
          confirm: words.pick.confirm,
          back: words.pick.back,
          place: near.placePin,
          cancel: near.cancelPick,
        }
      : null,""")

p = 'types/DirectoryMapView.ts'
sub(p, """  /** «مركّز على موقعي», while a point is held. */
  centre: string | null;""", """  /** «مركّز على موقعي», while a point is held. */
  centre: string | null;
  /** Picking a point by hand: the card over the map, placing the centre or going back. */
  pick: {
    title: string;
    text: string;
    confirm: string;
    back: string;
    place: (point: { lat: number; lng: number }) => void;
    cancel: () => void;
  } | null;""")

io.open(ROOT + 'components/map/PickCard.tsx', 'w', encoding='utf-8', newline='').write("""import { Button, Card, CardContent, CardFooter, CardHeader, CardTitle } from '@shared/design-system';
import type { MarkerMapControls } from '@shared/map';
import { useEffect, useId } from 'react';
import type { DirectoryMapView } from '../../types/DirectoryMapView';

/**
 * Setting one's location by hand (U7): a region over the map with its title and its text, which
 * promises the point is sent rounded and never stored; «ثبّت الموقع هنا» places the map's centre,
 * «رجوع» restores what was there. On opening, the focus moves to the map, whose arrow keys pan it
 * under the crosshair.
 */
export function PickCard({
  pick,
  map,
}: {
  pick: NonNullable<DirectoryMapView['pick']>;
  map: MarkerMapControls;
}) {
  const titleId = useId();
  const { focusMap } = map;
  useEffect(() => {
    focusMap();
  }, [focusMap]);

  return (
    <Card
      role="region"
      aria-labelledby={titleId}
      className="pointer-events-auto w-full max-w-sm shadow-overlay"
    >
      <CardHeader>
        <CardTitle>
          <h2 id={titleId}>{pick.title}</h2>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-body-sm text-muted-foreground">{pick.text}</p>
      </CardContent>
      <CardFooter>
        <Button
          className="flex-1"
          onClick={() => {
            pick.place(map.centre());
          }}
        >
          {pick.confirm}
        </Button>
        <Button variant="ghost" onClick={pick.cancel}>
          {pick.back}
        </Button>
      </CardFooter>
    </Card>
  );
}
""")

p = 'components/map/DirectoryMap.tsx'
sub(p, """import { MapNotice } from './MapNotice';""", """import { MapNotice } from './MapNotice';
import { PickCard } from './PickCard';""")
sub(p, """                <div className="flex items-end justify-between gap-3">
                  {selected !== null && !view.phone ? (""", """                <div className="flex items-end justify-between gap-3">
                  {view.pick !== null ? (
                    <PickCard pick={view.pick} map={controls} />
                  ) : selected !== null && !view.phone ? (""")
sub(p, """ * and «مركّز على موقعي» while a point is held. Closing the chosen space hands the focus back to its
 * mark.
 */""", """ * and «مركّز على موقعي» while a point is held, or, while a point is picked, the picking card in the
 * chosen space's place. Closing the chosen space hands the focus back to its mark.
 */""")

p = 'components/DirectoryView.tsx'
sub(p, """import { useRef } from 'react';""", """import { useEffect, useRef } from 'react';""")
sub(p, """/**
 * The map's view: the search and the filters' sheet (at every width, with no order), «الأقرب إليّ»
 * and its state line, then the map.
 */
function MapView({ slots }: { slots: DirectorySlots }) {
  const view = useDirectoryMap();
  const nearButton = useRef<HTMLButtonElement>(null);
  const { filters } = view;
""", """/**
 * The map's view: the search and the filters' sheet (at every width, with no order), «الأقرب إليّ»
 * and its state line, then the map. While a point is picked, the button is hidden; once placed or
 * given up, the focus returns to it.
 */
function MapView({ slots }: { slots: DirectorySlots }) {
  const view = useDirectoryMap();
  const nearButton = useRef<HTMLButtonElement>(null);
  const { filters } = view;
  const picking = view.pick !== null;
  const wasPicking = useRef(picking);
  useEffect(() => {
    if (wasPicking.current && !picking) nearButton.current?.focus();
    wasPicking.current = picking;
  }, [picking]);
""")
sub(p, """        <div className="flex justify-end">
          <NearMeButton ref={nearButton} button={view.near.button} />
        </div>""", """        {!picking && (
          <div className="flex justify-end">
            <NearMeButton ref={nearButton} button={view.near.button} />
          </div>
        )}""")
print('ok')
