# TABLE_NAME — plan (short, per N4; the build follows without a stop)

## 1. Summary

A `Table` that fits stops saying its name twice: its scrolling container is a plain box until the table overflows. The
unused `TableCaption` is removed.

## 2. Contract

- **Scope:** C1 and C2 of `0_CARRIED_FROM_152.md`, as N2 and N3 settle them.
- **Acceptance criteria:**
  - A `Table` that fits exposes no `group`, no container name and no tab stop, and one named `table`.
  - A `Table` that overflows has the named group and the tab stop, as today.
  - A default `ScrollRegion` that fits is still a named group. Photos, Occupancy and the showcase do not change.
  - `ScrollRegion` still takes exactly one name.
  - `TableCaption` and its two exports are gone.
  - axe reports no violation on the hours at 390 and the prices at 320 and 390, Arabic and English, light and dark.
- **Out of scope:** everything else (N1). API, schema, dependencies, database writes.

## 3. Reading done

CLAUDE.md, workflow, testing, documentation rules, foundation §10 and §12, finding 229, the open findings' titles,
`Table`, `ScrollRegion`, their tests, `ScrollRegionSection.tsx`, the TABLE_SCROLL axe script.

## 4. Decisions as built

- **N2:** `ScrollRegion` gains an optional boolean `quietWhileFits`, default `false`. While it is set and the content
  fits, the element renders no `role`, `aria-label`, `aria-labelledby` or `tabIndex`. `Table` alone sets it. The name
  stays required by the type, so a quiet region still has its name ready for when it overflows.
- **N3:** remove the `TableCaption` function and its exports from `Table/index.ts` and the layer's `index.ts`.

## 5. Stronger decisions

None. N2's accepted double name while overflowing stays as decided.

## 6. Related findings

- **229:** not reopened and **not edited.** It is a record, true as of its date, and documentation rules §1 allow a
  record only three kinds of change. The current behaviour goes in foundation §12, its owner.
- The open findings (23, 65, 152, 215, 221) do not touch this item.

## 7. Files

- `apps/web/src/shared/design-system/components/display/ScrollRegion/ScrollRegion.tsx` and its test
- `apps/web/src/shared/design-system/components/data/Table/Table.tsx`, `index.ts` and its test
- `apps/web/src/shared/design-system/index.ts`
- Tests that assert the old group on a fitting table: `DataTable.component.test.tsx`,
  `SpaceDetails.component.test.tsx`, `SpacePricesCard.component.test.tsx`
- `docs/frontend/design-system/foundation.md` (§12's ScrollRegion and Table rows; §10 stays true)

**Recorded, not changed:** `.design-sync/config.json` keeps a `"TableCaption": null` line in its `componentSrcMap`. It
is the design-sync tool's map, outside N3's list. To be named in the report.

## 8. Design issues

None. Nothing visible changes.

## 9. Tests (component lane) and the break each catches

| Test | Break |
|---|---|
| `Table` that fits: no `group`, one named `table`, no tab stop | `Table` stops passing `quietWhileFits` |
| `Table` overflows: named group (label and labelledby) and tab stop | the role or name is never restored on overflow |
| Default `ScrollRegion` that fits is a named group | `quietWhileFits` defaults to `true` |
| `ScrollRegion` quiet: plain while it fits, named group on overflow, plain again | the quiet branch ignores `overflows` |
| Hours, prices and `DataTable`: named table, no group while fitting | as the first row |

## 10. Review Focus

- A focused table that shrinks back to fitting loses its role and tab stop while focused. No test covers the focus
  there; the default region already drops its tab stop the same way.
- Real screen-reader speech is not run. The accessibility attributes and axe are the evidence.

## 11. Commits

1. `fix(design-system): name a fitting table once` — N2, its tests, foundation.
2. `refactor(design-system): remove TableCaption` — N3.

## 12. Verification

`format:check`, `lint`, `typecheck`, `check:classes`, `check:links`, `check:conflicts`, `test:unit`, `test:component`,
a production build, `check:build`, the Chrome pass. **`test:api` is left to CI** (N5: no API code).

## 13. Decisions needed from the owner

None to proceed.
