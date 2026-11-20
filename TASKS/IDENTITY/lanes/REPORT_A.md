# Lane A report: IDENTITY C2, C3, C4

(Saved by the lead from the lane's final message, 2026-11-12.)

All three commits are on `lane/a`, which is at **`d724321ec3f82a56d81367a2c0831e7f392291f8`**. The tree is clean, and `git log --oneline 22ddac1c..lane/a` shows exactly my three commits. No commit has `Co-Authored-By` or a "generated with" line. Every file was staged by path, and each commit was linted and typechecked before it was made.

## Commits

1. **`f23df5b11b9611024ef71556199dcf294dda8fec`**: `feat(design-system): tell hover from selected` (45 characters), 26 files.
   - **Script and its test:** `apps/web/scripts/checkClasses.ts`, `checkClasses.unit.test.ts`.
   - **The layer:** Button, Calendar, DropdownMenu, Select, Combobox, Table, DataTable, Input, ToggleGroup, Tabs, SegmentedControl, Sidebar, FilterTag, `leaflet.css` (the zoom buttons' hover).
   - **Features and pages:** SpaceCard, ContactList, DebtsTab, PlatformTiles, OwnerOverview, AreaCards, ContactsSheet (the handle), ContactsView (the `<li>`/`<a>` change).
   - **Showcase:** ShowcaseNav, SortableSection (the handle).
2. **`eff37f8a47b0b908588d3778fa7c4de92523d22a`**: `feat(web): underline links in running text` (42 characters), 6 files: `Button.tsx` (the link variant and its comment), `Button.component.test.tsx` (T20), RegisterPage (2 links), AboutPage (the `#contact` link), SiteFooter (4 links), the showcase's FieldSection.
3. **`d724321ec3f82a56d81367a2c0831e7f392291f8`**: `feat(design-system): mark what matters in spark` (47 characters), 5 files: Tabs (`line` indicator `after:bg-spark`), `leaflet.css` (`outline: 3px solid var(--spark)` and its comment), ContactsSheet (`border-spark`), PhotosEdit (`outline-spark`), SortableSection (`border-spark`, grid and list).

## Tests

**T12** (`scripts/checkClasses.unit.test.ts`, unit lane), 33 new cases:
- **Red, before the rule.** I exported a temporary stub that returned `[]`; it was never committed.
  - `FAIL |unit| scripts/checkClasses.unit.test.ts > findSelectedTintHoverClasses > flags the tint as a hover in a CSS @apply`
  - `AssertionError: expected [] to deeply equal [ 'hover:bg-accent' ]`
  - `Tests  23 failed | 91 passed (114)`
- **First run after the rule:** one case failed. My hand-counted column was 15, the code said 16. I recounted by hand and 16 is right, so I fixed the expectation.
- **Green:** `Test Files  1 passed (1)`, `Tests  114 passed (114)`.
- **Break 1, the rule removed** (the finder's predicate set to `false`): `Failed Tests 23`, `FAIL … flags the selected tint under a hover or highlight variant: hover:bg-accent`, `AssertionError: expected [] to deeply equal [ 'hover:bg-accent' ]`. Restored by copy, checked with `cmp`.
- **Break 2, narrowed to `hover` only:** `Tests  10 failed | 104 passed (114)`, `FAIL … flags the selected tint under a hover or highlight variant: focus:bg-accent`, `AssertionError: expected [] to deeply equal [ 'focus:bg-accent' ]`. Restored by copy, checked with `cmp`.

**T20** (`Button.component.test.tsx`, component lane):
- **Red, before the Button change:** `FAIL |component| …Button.component.test.tsx > Button > underlines the link variant at rest, not only under the pointer`, `expect(element).toHaveClass("underline") Expected the element to have class: underline`, `Tests  1 failed | 11 passed (12)`.
- **Green:** `Tests  12 passed (12)`.
- **Break 1, `hover:underline` put back:** `FAIL … > underlines the link variant at rest, not only under the pointer`, `expect(element).not.toHaveClass("hover:underline") Expected the element not to have class: hover:underline`. Restored by copy.
- **Break 2, `border-spark` on the outline variant:** `FAIL … > draws the outline variant without the spark, which never marks an action`, `AssertionError: expected 'inline-flex shrink-0 items-center jus…' not to match /spark/`, `Tests  1 failed | 11 passed (12)`. Restored by copy.

**T21**, the existing tests of every touched file, all green:
- **Commit 1, component lane:** 21 files, 200 tests passed. Button, Calendar, DropdownMenu, Select, Combobox, Table, DataTable, Input, ToggleGroup, Tabs, SegmentedControl, Sidebar, FilterTag, SpaceCard, SpaceDetails (ContactList), DebtsTab, AdminOverview (PlatformTiles), OwnerOverview, HomePage (AreaCards), ContactsSheet, and SpaceEditor (ContactsView: its links are found by name and its axe checks are clean).
- **Commit 1, unit lane:** `checkClasses`, `leaflet`, `registry`: 3 files, 126 passed.
- **Commit 2:** Button, authPages, AboutPage, SiteLayout: 4 files, 48 passed.
- **Commit 3:** Tabs, ContactsSheet, PhotosSection (component, 36 passed); `leaflet` and `registry` (unit, 12 passed).

## Commands run and their results

- **Every heavy command went through the grant script.**
  - Typecheck: exit 0, once per commit.
  - ESLint on my files: exit 0, once per commit.
  - Test runs: as listed above.
  - Waits: 4 memory waits (under 4 GB, about 2 minutes each).
  - No run was killed and none gave up. Every `exit 1` in the grant log is one of the intended reds or breaks above.
- **Light commands, no grant:**
  - `npm run check:classes` passes at each commit's head: "No physical direction, arbitrary-value or selected-tint hover classes in 1989 files."
  - `npx prettier --check` is clean on every touched file; `--write` was run only on ShowcaseNav, Button and FieldSection.

## The inventory and EC10

**The inventory (the rule run before any fix).** It found 40 classes in 20 files. Every file is a row of the plan's §7.1, so there are **no files beyond the plan's table**.

**MissingChecklist does not exist at 22ddac1c.** #143 deleted it (commit `89bb16cc`). The link that took its place, in ProfileHeader, is already underlined, so the C3 row needed no edit.

**EC10, changed.** Each now hovers with the wash:
- DataTable's sort header (`hover:bg-hover-on-muted hover:text-foreground`)
- the Calendar's today (`hover:bg-hover-on-muted`)
- FilterTag's remove button
- the ContactsView tile (the muted fill moved to the `<li>`; the `<a>` keeps its focus ring and its name)
- SegmentedControl's unchecked segment
- the `md` Tabs track

**EC10, searched and left unchanged** (see decision 4):
- Outline Buttons and chips inside a muted container, each with its own card fill:
  - `features/desk/components/money/MoneyBlock.tsx`: its outline toggle button and its ToggleGroup chips
  - `features/packages/components/list/PackageRow.tsx` when the package is paused: «clear shift» and «edit»
  - `pages/site/public/home/OwnersCard.tsx`
  - `features/favorites/components/RemoveFavorite.tsx`, drawn inside the muted card of `UnlistedFavorite.tsx`
  - `features/spaces/components/photos/PhotoTile.tsx`: the remove button sits over the photo
- No ghost Button and no other written `hover:` class sits in any of these muted containers: AnnouncementSheet, DecideSheet, MyReportCard, PricesSection, AdminOverview, PackageSheet, ReminderCard, AmenitiesView, PrivacyNote, ProfileHeader, PhotosView, Gallery, SpaceCover, TemporaryPasswordDialog, ShowcasePage main.

## Decisions I took without the lead (what, why, how to undo)

1. **Calendar range middle.** `variant={modifiers.range_middle ? null : 'ghost'}`.
   - *Why:* a selected range must keep its tint under the pointer. The ghost's `hover:bg-hover` would otherwise compete with `data-range-middle:bg-accent` by variant order. The other fix, `hover:bg-accent`, is now refused by T12.
   - *Undo:* `variant="ghost"`.
   - Today's day takes the wash only when it is neither filled nor in the range middle.
2. **The rule goes slightly beyond the brief's list.** It also counts `group-` and `peer-` forms with a `/name` (shadcn's Sidebar uses `peer-hover/menu-button:text-sidebar-accent-foreground`), an opacity (`/50`) and an important mark (`!`). Each has a test.
   - *Undo:* drop the two `.replace` normalisations and those 5 cases.
   - *Known gap, recorded:* arbitrary spellings such as `data-[state=open]:` and `aria-[expanded=true]:` are not counted.
3. **One variant parser for both finders.** `utilityOf` became `splitVariants` (it returns the variants and the utility), so the arbitrary-value and tint finders share it. The existing tests are green.
   - The test file still uses `'bg-(--brand-600)'` as an arbitrary-value sample string. The brief named only the comment, which now reads `bg-(--spark-500)`.
4. **EC10: outline Buttons and chips on muted grounds were not given the wash.**
   - *Why:* D1's defect is a control with no fill of its own, whose hover vanishes into the ground. These change their own card fill on hover (card to `hover`, 1.26 in dark), so the hover shows.
   - The brief's text ("a ghost or outline Button … each takes hover-on-muted") can be read the other way.
   - *To apply it:* add `hover:bg-hover-on-muted` to each listed button. For PackageRow, only when paused. RemoveFavorite would need its caller's context. The chips would take `not-data-on:hover:bg-hover-on-muted`.
5. **ShowcaseNav** applies its hover classes only when the entry is not current, using NavLink's `isActive`. The Sidebar's collapsed branch keeps its now-redundant `relative` (no drive-by).
6. **T20 break 2** replaced the outline's `border-(--card-border)` with `border-spark` rather than adding it beside. The effect on the class string is the same.

## Found, not fixed

- **`features/occupancy/components/LiveStatusControl.tsx`.** The neutral tone is an outline Button with `bg-secondary`. In dark its hover (n-800) equals its rest fill, so it shows no hover. The success and warning tones now hover grey (they hovered with the tint before). The wash is not the fix, because it would replace the button's own fill. This may be worth a finding.
- **`pages/site/shell/SiteMenu.tsx` (lane B).** The current entry is `aria-[current=page]:bg-secondary` on a ghost Button. Whether it keeps its look under the pointer depends on variant order, and in dark `secondary` equals `hover`.
- **PhotosEdit, for the visual pass.**
  - On a photo lifted by the keyboard, `focus-visible:outline-ring` (the ink) wins over `outline-spark`. A keyboard lift therefore shows the ink ring and a mouse drag shows the spark.
  - The picture sits inside PhotoTile's `overflow-hidden` frame, so an outline drawn outside it may be clipped.

## The document lines, ready to paste

### C2

- **foundation §3 *Enforcement* (line 99).**
  - Replace: "`check:classes` forbids (d) arbitrary-value classes outside the layer; palette classes do not exist, because the Tailwind palette is reset."
  - With: "`check:classes` forbids (d) arbitrary-value classes outside the layer, and (e) the selected tint as a hover anywhere, the layer included: `bg-accent`, `text-accent-foreground`, `bg-sidebar-accent` or `text-sidebar-accent-foreground` under a hover or highlight variant (`hover:`, `focus:`, `focus-visible:`, `aria-expanded:`, `data-open:`, `has-data-open:`, `data-[selected=true]:`, `data-highlighted:`), alone or compounded (`md:hover:`, `not-data-active:hover:`), read on another element (`group-hover:`, `peer-hover/…:`) or with an opacity or important mark; palette classes do not exist, because the Tailwind palette is reset."
- **foundation §5 *Usage rules*.** Add after the bullet "**Text over a photo** …":
  - "- **Hover is not selected.** A hover is the neutral `hover` fill; selected is the spark's tint (`accent`, `sidebar-accent`). They differ by hue and, where the design gives one, a second mark: the sidebar's current item has a 3 px `spark` bar at its inline start, a chip that is on a `spark` edge and a check. Selected keeps its tint under the pointer: an item hovers only while it is not selected (`not-data-on:`, `not-data-active:`, `not-data-[active=true]:`, or the caller's own condition), never by the order Tailwind emits its variants in. A control drawn on a `muted` or `secondary` ground hovers with `hover-on-muted`: in dark, `hover` equals `muted` and would vanish there."
- **foundation §11.**
  - Replace the bullet "- **A hover never fades a fill.** A filled variant's hover mixes the fill toward the foreground (`hover:bg-[color-mix(in_oklch,var(--primary),var(--foreground)_12%)]`), which raises its label's contrast in both themes; `bg-primary/90` drops the light theme's white label below AA. Outline and ghost hovers use `accent`."
  - With: "- **A hover never fades a fill.** `bg-primary/90` drops the light theme's white label below AA. The ink's hover is its own role (`hover:bg-primary-hover`); secondary and destructive mix their fill toward the foreground (`hover:bg-[color-mix(in_oklch,var(--destructive),var(--foreground)_12%)]`), which raises the label's contrast in both themes. Outline and ghost variants, rows, and menu and list items hover with `hover` (`hover:bg-hover hover:text-hover-foreground`), never `accent`, which means selected (§5; `check:classes` refuses it, §3); on a `muted` or `secondary` ground, with `hover-on-muted`."
- **foundation §12, Table + DataTable.**
  - Replace "a row takes `accent` when hovered and while its row menu is open" with "a row takes `hover` when hovered and while its row menu is open, never the selected tint".
  - Replace "its header becomes a button with an arrow, and `aria-sort` says the order;" with "its header becomes a button with an arrow, hovering with `hover-on-muted` on the muted header row, and `aria-sort` says the order;".
- **foundation §12, Select / Combobox.** After "a chosen option is `aria-checked` with a check at its end, because cmdk keeps `aria-selected` for the highlighted one" add " · the highlighted item (pointer or arrow keys) takes `hover`, never the selected tint".
- **foundation §12, Calendar / DatePicker.** Replace "chosen days on `primary`, the inside of a range on `accent`" with "chosen days on `primary`, hovering with `primary-hover`; the inside of a range on `accent`, kept under the pointer; today's cell on `muted`, its day hovering with `hover-on-muted`".
- **foundation §12, ToggleGroup.** Replace "when on, the `accent` pair, a `primary` edge and a check at the start" with "when on, the `accent` pair (selected), a `spark` edge and a check at the start, kept under the pointer; a chip that is off hovers with `hover`".
- **foundation §12, SegmentedControl.** Replace "a segment `muted-foreground` at the `label` size, `foreground` on hover;" with "a segment `muted-foreground` at the `label` size, on hover `foreground` over the `hover-on-muted` wash;".
- **foundation §12, Sidebar.** Replace "shown expanded and in the drawer · `SidebarText`" with "shown expanded and in the drawer · an item hovers with `hover`; the current page keeps `sidebar-accent` under the pointer, with a 3 px `spark` bar at its inline start, clipped by its radius · `SidebarText`".
- **Optional, not asked for.**
  - FilterTag: "· its remove button hovers with `hover-on-muted`".
  - Tabs `default`: "a tab that is not active hovers with `hover`, on the `md` track with `hover-on-muted`".
  - DropdownMenu: "· a highlighted item takes `hover`".
- **`docs/development/setup.md`, line 59 (commands table).**
  - Replace the row's ending "use a token utility ([foundation §2](../frontend/design-system/foundation.md#2-principles)) |"
  - With: "use a token utility ([foundation §2](../frontend/design-system/foundation.md#2-principles)). Also fails on the selected tint shown as a hover (`hover:bg-accent`, `focus:text-accent-foreground`, `data-[selected=true]:bg-sidebar-accent` …) anywhere in `apps/web/src`, the design system included; use `hover` ([foundation §5](../frontend/design-system/foundation.md#5-semantic-roles)) |"
- **`CLAUDE.md`, line 79.** Replace "(no physical direction classes; no arbitrary values outside the design system)" with "(no physical direction classes; no arbitrary values outside the design system; no selected tint as a hover)".

### C3

- **foundation §5 *Usage rules*.** Add the bullet: "- **Links in running text are underlined.** The ink is also the text's colour, so a link inside a sentence, a note or the footer is underlined at rest (`text-primary underline underline-offset-4`), not only under the pointer; so is the link Button."
- **foundation §12, Button.** Replace "primary, secondary, outline, ghost, destructive, link · sizes" with "primary, secondary, outline, ghost, destructive, link (underlined at rest) · sizes".

### C4

- **foundation §12, Tabs.** Replace "`line`: underlined, for the sections of a page" with "`line`: underlined, for the sections of a page, the active tab marked by a line in the `spark`".
- **foundation §12, Sortable.** Insert before "· its slide follows `--duration-medium`": "· the caller draws the item it lifts (`renderItem`'s `lifted` and `dragging`) with a `spark` edge: the contacts' row `border-spark` with the floating shadow, a photo `outline-spark` ·".
- **foundation §3, the map's stylesheet paragraph.** Replace "the selected one ringed on `primary`, never filled;" with "the selected one ringed in the `spark`, never filled;".

## Files

- **Worktree:** `C:\dev\masaha\app-design-lane-a`.
- **Scratch folder:** `C:\dev\masaha\workspace\TASKS\IDENTITY\lanes\scratch-a\`, holding the edit scripts `c2_edits.py`, `c3_edits.py`, `c4_edits.py`, the break scripts, the backup copies and the commit messages.
