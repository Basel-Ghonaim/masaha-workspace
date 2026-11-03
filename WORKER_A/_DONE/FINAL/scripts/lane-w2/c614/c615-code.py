import os
os.chdir('C:/dev/masaha/app-lane-w2/apps/web/src')


def edit(p, pairs):
    s = open(p, encoding='utf8', newline='').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old)
        s = s.replace(old, new)
    open(p, 'w', encoding='utf8', newline='').write(s)


edit('features/lookups/hooks/amenities/useAmenityChecklist.ts', [
("""import { useCatalogueQuery } from '../area/useCatalogueQuery';""",
 """import type { RetiredAmenity } from '../../types/RetiredAmenity';
import { useCatalogueQuery } from '../area/useCatalogueQuery';"""),
("""/**
 * A space's amenities to tick, ready to render: the platform's active amenities, in order, named in
 * the interface's language, and any retired one the space still has (`linked`), marked, so it is
 * seen and can be left out; a retired one it does not have is never offered. Ticking one adds it to
 * the value, unticking it takes it out. While the list loads, or once it has failed, it says so.
 *
 * That is the admin's list (`source`). The public catalogue an owner reads names only the active
 * amenities: a retired one the space still has stays in the value, unseen, never toggled, and one
 * line counts them (`retiredKept`). On either list, one ticked but not linked that is retired
 * before the save is no longer offered, and the next toggle drops it from the value.
 */
export function useAmenityChecklist({
  source,
  value,
  linked,
  onValueChange,
}: {
  source: LookupsSource;
  value: number[];
  linked: number[];
  onValueChange: (ids: number[]) => void;
}) {""", """/**
 * A space's amenities to tick, ready to render: the platform's active amenities, in order, named in
 * the interface's language, and any retired one the space still has (`linked`), marked, so it is
 * seen and can be left out; a retired one it does not have is never offered. Ticking one adds it to
 * the value, unticking it takes it out. While the list loads, or once it has failed, it says so.
 *
 * From the admin's list (`source`) a retired one is named by that list and marked «غير نشط». The
 * public catalogue an owner reads names only the active amenities: the retired ones the space holds
 * come named with the space's read (`retired`, in the platform's order), listed after the others,
 * marked «لم يعد في قائمة المنصة», ticked while the value holds them, and left out of the next
 * save once unticked (finding 99). On either list, one ticked but not linked that is retired before
 * the save is no longer offered, and the next toggle drops it from the value.
 */
export function useAmenityChecklist({
  source,
  value,
  linked,
  retired = [],
  onValueChange,
}: {
  source: LookupsSource;
  value: number[];
  linked: number[];
  retired?: readonly RetiredAmenity[];
  onValueChange: (ids: number[]) => void;
}) {"""),
("""  const offered =
    source === 'admin'
      ? (adminList.data ?? []).filter((amenity) => amenity.isActive || linked.includes(amenity.id))
      : (catalogue.data?.amenities ?? []).map((amenity) => ({ ...amenity, isActive: true }));
  const isOffered = (id: number) => offered.some((amenity) => amenity.id === id);
  const unseen =
    source === 'public' && catalogue.data !== undefined
      ? value.filter((id) => linked.includes(id) && !isOffered(id)).length
      : 0;""", """  const active = (catalogue.data?.amenities ?? []).map((amenity) => ({ ...amenity, isActive: true }));
  const offered =
    source === 'admin'
      ? (adminList.data ?? []).filter((amenity) => amenity.isActive || linked.includes(amenity.id))
      : catalogue.data === undefined
        ? []
        : [
            ...active,
            // The space's own retired amenities, which the catalogue no longer names.
            ...retired
              .filter(({ id }) => linked.includes(id) && !active.some((one) => one.id === id))
              .map((amenity) => ({ ...amenity, isActive: false })),
          ];
  const isOffered = (id: number) => offered.some((amenity) => amenity.id === id);
  const retiredMark =
    source === 'admin'
      ? copy.lookups.amenities.row.inactive
      : copy.lookups.amenityChecklist.retired;"""),
("""      inactive: !amenity.isActive,
      toggle:""", """      /** The badge of a retired amenity, or none. */
      mark: amenity.isActive ? null : retiredMark,
      toggle:"""),
("""    retiredKept: unseen === 0 ? null : copy.lookups.amenityChecklist.retiredKept({ count: unseen }),
""", ""),
("""      retry: copy.status.retry,
      inactive: copy.lookups.amenities.row.inactive,
""", """      retry: copy.status.retry,
"""),
])

edit('features/lookups/components/amenities/AmenityChecklist.tsx', [
("""import type { LookupsSource } from '../../types/LookupsSource';""",
 """import type { LookupsSource } from '../../types/LookupsSource';
import type { RetiredAmenity } from '../../types/RetiredAmenity';"""),
("""/**
 * A space's amenities to tick, from the platform's list, as a group named by `label`: the active
 * ones, and a retired one the space still has (`linked`), marked inactive. It hands back the
 * amenities chosen. While the list loads, or once it has failed, it says so, with a way to try again.
 * Read from the public catalogue (`source`), a retired one the space has stays chosen, unseen, and a
 * line under the list counts them.
 */""", """/**
 * A space's amenities to tick, from the platform's list, as a group named by `label`: the active
 * ones, and a retired one the space still has (`linked`), marked. It hands back the amenities
 * chosen. While the list loads, or once it has failed, it says so, with a way to try again. Read
 * from the public catalogue (`source`), a retired one the space holds is named from the space's read
 * (`retired`), marked «لم يعد في قائمة المنصة», and left out once unticked.
 */"""),
("""  linked,
  onValueChange,
  disabled,
}: {
  source: LookupsSource;
  label: string;
  value: number[];
  linked: number[];
  onValueChange: (ids: number[]) => void;
  disabled: boolean;
}) {
  const checklist = useAmenityChecklist({ source, value, linked, onValueChange });""", """  linked,
  retired,
  onValueChange,
  disabled,
}: {
  source: LookupsSource;
  label: string;
  value: number[];
  linked: number[];
  retired?: readonly RetiredAmenity[];
  onValueChange: (ids: number[]) => void;
  disabled: boolean;
}) {
  const checklist = useAmenityChecklist({ source, value, linked, retired, onValueChange });"""),
("""                    {item.inactive && ' '}
                    {item.inactive && <Badge variant="neutral">{words.inactive}</Badge>}""",
 """                    {item.mark !== null && ' '}
                    {item.mark !== null && <Badge variant="neutral">{item.mark}</Badge>}"""),
("""      {checklist.retiredKept !== null && (
        <p className="text-body-sm text-muted-foreground">{checklist.retiredKept}</p>
      )}
""", ""),
])

open('features/lookups/types/RetiredAmenity.ts', 'w', encoding='utf8', newline='').write(
"""/**
 * A retired amenity a space still holds, named by the space's read (`retiredAmenities`), which the
 * public catalogue no longer names.
 */
export type RetiredAmenity = { id: number; nameAr: string; nameEn: string };
""")

edit('shared/copy/english/lookups.ts', [
("""    /** The retired amenities a space keeps, which the public catalogue no longer names. */
    retiredKept: ({ count }: { count: number }) =>
      englishPlural(count, {
        one: 'One amenity no longer on the platform’s list stays linked to the space.',
        other: `${String(count)} amenities no longer on the platform’s list stay linked to the space.`,
      }),""", """    /** The badge of a retired amenity a space still holds, on an owner's checklist. */
    retired: 'No longer on the platform’s list',"""),
])
print('ok')
