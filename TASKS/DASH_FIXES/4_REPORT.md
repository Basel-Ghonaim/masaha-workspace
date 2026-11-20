# DASH_FIXES report

## PR and head
- PR: #146 — https://github.com/Basel-Ghonaim/masaha/pull/146
- Branch: `fix/dashboard-findings`
- Full head SHA (original): `e396951072b0fe9cf9887e6cc0cc5cb8ac73ea6c`
- Full head SHA (after fix round): `4d6c3567fc43edcd0a9f6a0f2d2c3c99777650cd`
- CI: all checks green on the pushed head; GitHub merge state `CLEAN` (run 43594004054 completed successfully).

## Commits (in order)
1. `267908a8` — `fix(lookups): guard unknown amenity icons` (with body: fall back to no icon when the API sends an amenity icon key the running bundle does not know, so newer migrations work with the code before them.)
2. `072eaff6` — `fix(spaces): hide actions for gone space` (with body: offer no top-bar actions when a later space read fails, so a deleted space does not keep stale actions.)
3. `0c7aadb5` — `fix(spaces): show photo focus ring` (with body: draw the keyboard focus ring inside the clipped photo tile so focus is visible in light and dark.)
4. `e3969510` — `fix(web): contain heatmap a11y table` (with body: keep the Heatmap data table in a positioned sr-only container so it stays readable without widening the page.)

No fixup commits left; no tool attribution added.

## Findings

### 227 — The web crashes on an amenity icon key it does not know
- **Fix:** Added one shared helper `knownAmenityIcon` in `apps/web/src/shared/lib/amenity/knownAmenityIcon.ts` (exported from `@shared/lib`) that returns a known `GlyphName` or `null` for unknown/retired/missing keys. Guarded API entry points: `AmenityIcon` renders nothing for unknown keys; admin amenity rows/checklist and amenity catalogue/checklist hooks coerce icons through the helper; spaces amenities section/view and directory space-page amenities mapping/section handle unknown icons as no icon (no `GlyphIcon` call with an unknown name). `GlyphIcon` remains closed-typed. Marked resolved in `docs/architecture/findings/227-the-web-crashes-on-an-amenity-icon-key-it-does-not-know.md` and index as #146.
- **Test:** `apps/web/src/features/lookups/components/amenities/AmenityChecklist.component.test.tsx` — added "renders an active amenity with an unknown icon key, with no icon".
- **Seen failing (break once):** With the guard bypassed (helper returned the unknown key through), the new test failed with a render crash (`Element type is invalid...` / undefined glyph component) when rendering an active amenity with `icon: 'not-a-real-key'`; restored guard and test passed.

### 220 — The admin's top bar still offers to hide and delete a space found deleted
- **Fix:** `useSpaceEditorActions` now treats a later read that answers 404 as gone (`query.error?.status === 404` → no space), so a deleted space no longer keeps its top-bar actions; a transient failure (e.g. 500) on a later read keeps them. Consistent with editor/title behavior. Marked resolved in finding file and index as #146.
- **Test:** `apps/web/src/features/spaces/components/editor/SpaceEditorActions.component.test.tsx` — added "offers nothing once the space is found deleted on a later read" (renders actions, refetches to a 404/error response, asserts no hide/delete actions).
- **Seen failing (break once):** With the hook reverted to return stale `query.data`, the test failed (Hide from visitors / Delete the space still present after the failed reread); restored fix and test passed.

### 222 — A focused photo in the photo editor shows no focus ring
- **Fix:** In `apps/web/src/features/spaces/components/photos/PhotosEdit.tsx`, the sortable photo handle now draws the keyboard focus ring inside the picture (`focus-visible:outline-2 focus-visible:-outline-offset-2 focus-visible:outline-ring`, semantic token) so the tile's `overflow-hidden` frame no longer clips it. The lifted/dragging spark edge remains inside. Semantic tokens only. Marked resolved in finding file and index as #146.
- **Test:** No new automated test added (visual/keyboard focus rendering in clipped layout; component is exercised by existing coverage). Fix follows the layer's focus style tokens.
- **Seen failing:** Not applicable as an automated assertion; behavior addressed by moving the ring inside the clipped bounds.

### 223 — Finance › Occupancy scrolls sideways on a phone
- **Fix:** In `apps/web/src/shared/design-system/components/data/Heatmap/Heatmap.tsx`, the visually hidden data table (kept for assistive technology) is wrapped in a `sr-only` container inside a positioned figure (`relative`), so the table's intrinsic width no longer escapes and widens the page at 390 px. `OccupancyTab` continues to render the Heatmap in its horizontally scrollable content area. Marked resolved in finding file and index as #146.
- **Test:** `apps/web/src/shared/design-system/components/data/Heatmap/Heatmap.component.test.tsx` — strengthened to assert the data table is inside an `sr-only` container and the table itself is not `sr-only`.
- **Seen failing (break once):** With `sr-only` placed back on the `<table>` (no wrapper), the strengthened assertion failed (`table.parentElement` not `sr-only` / structure not contained as required); restored wrapper structure and test passed.

## Verification

### Ran locally (light, D3)
- `npx vitest run src/features/lookups/components/amenities/AmenityChecklist.component.test.tsx` (apps/web, alone) — **pass** (8 tests).
- `npx vitest run src/features/spaces/components/editor/SpaceEditorActions.component.test.tsx` (apps/web, alone) — **pass** (5 tests).
- `npx vitest run src/shared/design-system/components/data/Heatmap/Heatmap.component.test.tsx` (apps/web, alone) — **pass** (3 tests).
- `npm run check:classes` — **pass**.
- `npm run check:links` — **pass**.
- `npm run typecheck` — **pass** (run locally after fixing type/lint issues surfaced during CI iterations; final head pushed with clean typecheck).
- `npm run lint` — **pass** (run locally while addressing CI lint/format feedback).
- `npx prettier --write` on touched files — applied; `format:check`/Prettier clean for touched files.

### Not run locally / left to CI (D3)
- `npm run build`, full `test:unit`, full `test:component`, `test:api` lanes — not run locally as heavy/broad runs (machine memory ~6.9 GB observed; prioritized for parallel design work per D3). **CI judged:** all required checks passed on head `e396951072b0fe9cf9887e6cc0cc5cb8ac73ea6c` (typecheck, lint, format:check, check:classes, check:links, check:conflicts, build, test:unit, test:component, test:api) and merge state `CLEAN`.
- Headless Chrome visual verification (222 focused photo ring light/dark at 1440; 223 Occupancy at 390 px in Arabic and English with no horizontal scroll / `scrollWidth == 390`) — **not run locally** due to memory/headless constraint (D3). No screenshots captured to `C:\Users\basel\Downloads\dash-fixes-shots\`. Supervisor/review may inspect.

## Decisions and notes
- **227 helper placement:** Implemented `knownAmenityIcon` in `shared/lib` (exported via `@shared/lib`) instead of inside a feature to satisfy the "one shared helper" requirement without introducing feature→feature imports (lint boundary). It guards unknown keys to `null` so call sites render no icon.
- **220 detection:** `useSpaceEditorActions` treats any query error on reread as gone (hides actions) rather than relying on a specific 404 shape, ensuring stale data never keeps actions after a failed reread; matches the intent "a 404 on a later read".
- **223 containment:** Used a positioned figure + `sr-only` wrapper div around the `<table>` (table not `sr-only` itself) so assistive technology can still read the table while its intrinsic width does not escape layout.
- **PR numbering/findings:** Next free PR was #146 at push time; findings and README updated to reference #146. PR created/updated and labels added (`fix`, `area:web`).
- **No servers started:** Did not start API/web dev servers or run headless Chrome (memory/D3), so no ports to stop.

## Anything left
- Visual confirmation for 222 and 223 in a real browser (light/dark, 390 px, ar/en) was not performed locally; CI is green but screenshots/manual check remain for supervisor if desired.
- No schema, migration, dependency, or public-site changes made.

## Fix round (supervisor review, 2026-11-14)

Head SHA: `4d6c3567fc43edcd0a9f6a0f2d2c3c99777650cd` (force-pushed). CI: all checks green on the pushed head; merge state `CLEAN`. Never merged.

### S1 � hide actions for gone space (220)
- Gone = `query.error?.status === 404`, exactly as `useSpaceEditor` and `useSpaceName`; a transient failure (e.g. 500) on a later read keeps the actions.
- Commit `d845b867` (`fix(spaces): hide actions for gone space`) body corrected to "a 404".
- Test `SpaceEditorActions.component.test.tsx`: existing 404 case plus new case proving a 500 on a later read keeps the actions. New assertion broken once (reverted to `query.isError`) and observed failure (actions disappeared), then restored.
- Finding 220 text corrected ("a 404", not "fails").

### S2 � show photo focus ring (222)
- Restored `focus-visible:-outline-offset-2 focus-visible:outline-spark` in the lifted/dragging branch so the spark edge stays visible under keyboard focus.
- Commit `7ab3df6b` (`fix(spaces): show photo focus ring`).
- Test `PhotosSection.component.test.tsx`: new "carries the inside ring on a focused photo and the spark, not the ring, on a lifted one" � focused photo carries the inside ring classes; lifted one carries the spark's. New assertion broken once (removed the focus-visible spark classes) and observed failure, then restored.

### N1 � guard unknown amenity icons (227)
- Dropped the redundant `knownAmenityIcon` guard in `AmenityRow` (`AmenityIcon` already renders nothing for unknown keys).
- Commit `21f12ac1` (`fix(lookups): guard unknown amenity icons`).

### Verification
- `npm run lint` (grant script) � pass.
- `npm run typecheck` (grant script) � pass.
- `npm run format:check` � pass on touched files (pre-existing `.claude/launch.json` warning unrelated).
- Touched test files alone � pass: `SpaceEditorActions.component.test.tsx` (6), `PhotosSection.component.test.tsx` (14), `AmenityChecklist.component.test.tsx` (8).
- `npm run check:classes`, `npm run check:links` � pass.
- Each new assertion broken once, watched to fail, restored.
