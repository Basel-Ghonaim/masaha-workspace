import os, shutil
L = 'C:/dev/masaha/app-lane-w2/apps/web/src/features/lookups/'
N = 'C:/dev/masaha/workspace/WORKER_A/FINAL/scripts/lane-w2/c614/new/'
for f in ['useEditGovernorateForm.ts', 'useEditAreaForm.ts', 'useEditAmenityForm.ts']:
    shutil.copyfile(N + f, L + 'hooks/edit/' + f)


def edit(p, pairs):
    s = open(p, encoding='utf8', newline='').read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old)
        s = s.replace(old, new)
    open(p, 'w', encoding='utf8', newline='').write(s)


edit(L + 'hooks/list/useRowViews.ts', [
("""  ): RowControlsView => ({
    shown: {""", """  ): RowControlsView => ({
    // Where the row stands, counted from 1: in each arrow's name, and said once it has moved.
    moved: copy.lookups.row.moved({ name, position: index + 1, count }),
    shown: {"""),
("""      label: copy.lookups.row.moveUp({ name }),""", """      label: copy.lookups.row.moveUp({ name, position: index + 1, count }),"""),
("""      label: copy.lookups.row.moveDown({ name }),""", """      label: copy.lookups.row.moveDown({ name, position: index + 1, count }),"""),
])

edit(L + 'types/RowControlsView.ts', [
("""/** A row's controls, ready to render: its two arrows and its shown switch, each named. */
export type RowControlsView = {
  shown: SwitchControl;""", """/**
 * A row's controls, ready to render: its two arrows, named with where the row stands, and its shown
 * switch, each named; and the line said once the row has moved (`moved`), where it now stands.
 */
export type RowControlsView = {
  moved: string;
  shown: SwitchControl;"""),
])

edit(L + 'components/list/RowControls.tsx', [
("""import { useLayoutEffect, useRef, type ReactNode } from 'react';""",
 """import { useLayoutEffect, useRef, useState, type ReactNode } from 'react';"""),
("""/**
 * A row's controls, for a governorate, an area or an amenity: its two arrows, its shown switch, then
 * its edit sheet (`children`). A control that waits
 * on the server stays in the focus order and ignores presses, so the keyboard keeps its place; and
 * when a move carries the row elsewhere and the focus falls to the page, it comes back to the control
 * pressed, or to the row's next one that can take it.
 */""", """/**
 * A row's controls, for a governorate, an area or an amenity: its two arrows, its shown switch, then
 * its edit sheet (`children`). A control that waits
 * on the server stays in the focus order and ignores presses, so the keyboard keeps its place; and
 * when a move carries the row elsewhere and the focus falls to the page, it comes back to the control
 * pressed, or to the row's next one that can take it. Once an arrow's move has landed, a polite live
 * region says where the row now stands; a row that only made room says nothing.
 */"""),
("""  const pressed = useRef<Which | null>(null);
""", """  const pressed = useRef<Which | null>(null);
  // The row's place as last seen, whether an arrow of it was pressed since, and what was said.
  const [seen, setSeen] = useState(controls.moved);
  const [moving, setMoving] = useState(false);
  const [said, setSaid] = useState('');
  if (controls.moved !== seen) {
    setSeen(controls.moved);
    if (moving) {
      setSaid(controls.moved);
      setMoving(false);
    }
  }
"""),
("""    pressed.current = which;
    if (!controls[which].waiting) act();
  };""", """    pressed.current = which;
    if (controls[which].waiting) return;
    if (which !== 'shown') setMoving(true);
    act();
  };"""),
("""      {children}
    </div>""", """      {children}
      <span role="status" className="sr-only">
        {said}
      </span>
    </div>"""),
])

edit('C:/dev/masaha/app-lane-w2/apps/web/src/pages/dashboard/admin/LookupsPage.tsx', [
(""" * their areas first, then the amenities, with the page's hint under the tabs. The tab shown is kept
 * in the address.""", """ * their areas first, then the amenities, with the tab's own hint under the tabs. The tab shown is
 * kept in the address."""),
("""        <p className="text-body-sm text-muted-foreground">{copy.lookups.hint}</p>""",
 """        <p className="text-body-sm text-muted-foreground">
          {tab === 'amenities' ? copy.lookups.amenities.hint : copy.lookups.governorates.hint}
        </p>"""),
])
print('ok')
