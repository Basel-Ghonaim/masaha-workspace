# TABLE_SCROLL — plan (finding 229, with C1–C2 carried from #150)

Branch `fix/table-scroll-229` from `origin/main` `9b4c4fc1`. PR expected **#152** (checked: #150 last PR, #151 the
design Issue). T4: the plan does not stop the work.

## Contract

**Scope.** The layer's `Table` scrolls sideways in a container nothing can focus (axe `scrollable-region-focusable` at
320 px on the space page's «الأسعار المعلنة»). The container becomes the layer's `ScrollRegion`: a named group, a
tab stop only while the table overflows, once for every table (the prices, the public hours, every `DataTable`).
Plus #150's notes C1 (a comment past 100 columns) and C2 (foundation §3's categories lag §12).

**Acceptance criteria.**
- [ ] `Table` takes exactly one name, `aria-label` or `aria-labelledby` (a type error otherwise); the table and its
      scrolling group both carry it, written once by the caller.
- [ ] The group is no tab stop while the table fits, a tab stop once it overflows; the one focus style, drawn inside
      the container so a card's `overflow-hidden` never clips it.
- [ ] Prices and hours name their tables through `aria-label` (their sr-only captions go); `DataTable` unchanged.
- [ ] axe in Chrome: no `scrollable-region-focusable` on the space page at 320/390 and on a `DataTable` page at 390,
      ar/en, light/dark; the focus ring whole at 390.
- [ ] Finding 229 recorded and Resolved; foundation §10, §12 updated; C1, C2 done.

**Out of scope.** Anything else noticed (recorded in the report); `TableCaption` stays exported, unchanged.

## Related findings

Open findings 23, 65, 152, 215, 221: none touches tables or scrolling; none folded. 224 (resolved) is the precedent.

## Files

Commit 1 — `chore: carry #150's two notes` (C1–C2)
- `apps/web/src/features/finance/components/OccupancyTab.tsx` — the doc comment rewrapped at 100, words unchanged.
- `docs/frontend/design-system/foundation.md` §3 — `display` + Meter, `data` + BarChart, Heatmap, `feedback` +
  Refreshing.

Commit 2 — `fix(design-system): reach a wide table by keyboard`
- `shared/design-system/components/data/Table/Table.tsx` — `Table`'s props: the table's own, without `aria-label` /
  `aria-labelledby`, plus `ScrollRegionName` (exported from `ScrollRegion` for it). The container is
  `<ScrollRegion data-slot="table-container" className="relative w-full focus-visible:-outline-offset-2" {...name}>`;
  the table gets the same name.
- `.../display/ScrollRegion/ScrollRegion.tsx`, `index.ts` — export the `ScrollRegionName` type (layer-internal use; not
  added to the layer's root surface).
- `features/spaces/components/prices/PricesView.tsx` — `<Table aria-label={table.caption}>`, the raw sr-only caption
  removed.
- `features/directory/components/page/HoursSection.tsx` — `<Table aria-label={hours.caption}>`, its sr-only
  `TableCaption` removed (and its import).
- `DataTable.tsx`, showcase `TableSection.tsx` — already `aria-label`; no change.
- Tests (below); `docs/architecture/findings/229-a-table-that-scrolls-sideways-cannot-be-reached-by-the-keyboard.md`
  (Resolved) and the index's Resolved list; foundation §10 (the scrolling line names `Table`), §12 (the Table row:
  its name, the group and the inset ring); `docs/features/directory.md` and `spaces.md` change log lines only if their
  described behaviour changes (they do not describe the table's caption or scrolling — checked, so none).

## Tests, each with its break

`Table.component.test.tsx` (the `ResizeObserver` and the widths stubbed in the test, as ScrollRegion's test does):
1. *The table and its scrolling group carry the caller's one name* (`aria-label`; and `aria-labelledby` to a heading).
   Break: drop `{...name}` from the group → fails.
2. *No tab stop while the table fits.* Break: `tabIndex={0}` always in ScrollRegion → fails.
3. *A tab stop once it overflows, focused by Tab.* Break: the container back to a plain `div` → fails.
4. *No axe violation while it overflows.* Break: the group unnamed (`role="group"` kept, name dropped) — axe or test 1.
5. *Takes exactly one name* (`@ts-expect-error`, proven by `typecheck`). Break: make the name optional → typecheck
   fails on the unused directive.
The existing caption test becomes an `aria-label` one (same assertions).

Callers:
- `SpacePricesCard.component.test.tsx` — the prices' group named by the caption («…» from the catalogue). Break:
  `aria-label={columns.price}` in PricesView → fails.
- `SpaceDetails.component.test.tsx` — the hours' table and group named «ساعات العمل الأسبوعية». Break: hours'
  `aria-label={hours.title}` → fails.
- `DataTable.component.test.tsx` — the table's group named by `label`. Break: Table without the group's name → fails.

**Review focus:** the name is said by the group and by the table (one string); the Table's overflow while `DataTable`
switches to cards (no Table drawn); RTL scrolling with the arrow keys (browser behaviour).

## Commits

1. `chore: carry #150's two notes` — C1, C2.
2. `fix(design-system): reach a wide table by keyboard` — Table, callers, tests, finding 229, §10, §12.

## Verification

Grant script for heavy commands: format:check, lint, typecheck, check:classes, check:links, check:conflicts,
test:unit, test:component, production build + check:build. `test:api` left to CI (T5). axe in headless Chrome over
CDP (script in `TASKS\TABLE_SCROLL\scripts\`): space page with prices and hours as a guest at 320 and 390; one
`DataTable` page as the demo owner at 390; ar/en, light/dark; Tab to an overflowing table, focus-ring shots at 390
light and dark in `Downloads\table-scroll-shots\`. Servers stopped by PID, 3320 and 5320 checked free.

## Decisions taken

- **Reuse `ScrollRegion`** rather than share its measuring: one component owns the rule (foundation §10), its tests
  already prove the measuring; it observes its direct child, the table, so a table that grows is measured again.
- **The name: the caller's `aria-label` or `aria-labelledby`, typed as required, given to both the group and the
  table.** The words exist once (one prop, one catalogue key); nothing names the table without its group. The two
  sr-only captions become `aria-label`, which `DataTable` already uses, so every table is named one way. Rejected:
  moving the name to the group and leaving the table unnamed (as #150's photo list) — a table's name is what table
  navigation lists, and twenty component tests rely on it; and labelling the group by the caption's id — needs a
  context between `Table` and `TableCaption`, and a table without a caption would leave the group unnamed. A screen
  reader may hear the name as it enters the group and again for the table: the accepted pattern for a scrolling
  table (a named, focusable container around a named table).
- **The ring inset** (`-outline-offset-2`): both frames around a table (Card, DataTable's) clip their content, so the
  layer's outline at +2 would be cut; inset, it is whole. Same outline, width and colour.
- **`TableCaption` stays** (a visible caption is still a use; an `aria-label` then names the table).
