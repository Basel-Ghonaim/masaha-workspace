## Summary

Resolves finding 224: axe-core in Chrome reported `aria-tooltip-name` on the directory map's tooltip beside a chosen mark, and `scrollable-region-focusable` on the space profile's phone row of photos and on Finance › Occupancy's «ساعات الذروة».

- **`ScrollRegion`** (design system, `display`): content that scrolls sideways, reached by the keyboard. A named `group` (one of `aria-label` / `aria-labelledby` required by its type), a tab stop only while its content overflows, measured by a `ResizeObserver` on itself and its direct children, with the layer's one focus style and no words. A group, not a region, so Occupancy's card (a region of the same name) can hold it. Showcase section, foundation §3, §10, §12.
- **The photos' phone row** sits in it, named «باقي الصور» once; the list inside keeps its role with no name, and is as wide as its photos (`w-max`) so the strip sees it grow. The 768 px grid is unchanged.
- **«ساعات الذروة»**: the heatmap alone sits in it, named by the card's heading; `CardContent` no longer scrolls; the empty state stays outside.
- **The map's tooltip**: hidden from assistive technology each time Leaflet adds it (passing and permanent), and a `MutationObserver` removes the `aria-describedby` Leaflet sets on the mark at every opening and never takes back. The mark's name is unchanged. architecture §6 updated.

## Scope / Acceptance criteria / Out of scope

**Scope:** finding 224's three places; web only.

- [x] `ScrollRegion`: named group, tab stop only while overflowing, re-measured on resize, one focus style, no words; showcase and foundation rows.
- [x] Photos' phone row: a group named once, its list unnamed.
- [x] «ساعات الذروة»: the heatmap alone in a group named by the heading; the empty state outside; the card stays the region.
- [x] Every mark tooltip `aria-hidden="true"`; no `aria-describedby` on the mark.
- [x] axe-core in Chrome: no `aria-tooltip-name`, no `scrollable-region-focusable` on the three screens, 390 and 1440, light and dark, Arabic and English.
- [x] Finding 224 Resolved.

**Out of scope:** any other finding; the API, schema, dependencies; the prices table's container at 320 px (see Evidence); the gaps of foundation §3's category table other than `ScrollRegion`.

## Change type

Fix (accessibility), with a new design-system component.

## Evidence

On the head before the `#150` substitution (`5afba618`; the substitution changed only that number in five documents, after which `format:check` and `check:links` ran again):

| Check | Result |
|---|---|
| `format:check` · `check:classes` · `check:links` · `check:conflicts` | clean (`check:links`: 2788 links in 264 documents and 2695 source files) |
| `lint` · `typecheck` | clean |
| `test:unit` | 29 + 77 + 196 files, 384 + 924 + 1403 tests, passed |
| `test:component` | 350 files, 2160 tests, passed |
| `build` (`NODE_ENV=production`) · `check:build` | passed |
| `test:api` | **not run locally**: no API code changes (the owner's allowance); CI runs it |

**Seen failing** (each break made once and restored):
- `ScrollRegion.component.test.tsx`: no `role="group"` → 4 fail; `tabIndex={0}` always → 2; no measure → 1; comparison reversed → 1; own box only observed → 1; both names optional → `typecheck` fails on the two `@ts-expect-error` lines.
- `PhotosSection.component.test.tsx`: the list named again → fails; no `ScrollRegion` → fails.
- `OccupancyTab.component.test.tsx`: the heatmap without `ScrollRegion` → fails; the empty state in a strip → fails.
- `MarkerMap.component.test.tsx`: both new tests failed on `main`'s code; the tooltip's handler dropped → 2 fail; hidden only when permanent → the passing one fails; the observer not started → the passing one fails; no removal → 2 fail.

**axe-core 4.13.0 in headless Chrome** (CDP), `masaha_dev`'s demo data, signed in as the demo owner, space 26; `main` first, then this branch:

| Screen | `main` | This branch |
|---|---|---|
| Map, a mark chosen, 390 and 1440 × light/dark × ar/en | `aria-tooltip-name` (1) in all 8 | none in all 8 |
| Map, another mark hovered | `aria-tooltip-name` (2) in all 8 | none in all 8 |
| Finance › Occupancy, 390 | `scrollable-region-focusable` (1) in all 4 | none |
| Finance › Occupancy, 1440 | none | none |
| Profile «الصور», 390 and 1440 | none (the four photos' row fits at 390) | none |
| Profile «الصور», 320 | `scrollable-region-focusable` (2): the photos' row and the prices table's container, in 3 of 4 (en/dark timed out loading on `main`'s run) | `scrollable-region-focusable` (1): the prices table's container only, in all 4 |

No other rule was reported on any run. The demo space has four photos, whose row fits exactly at 390 (316 px of 316), so the strip was also checked at 320, where it overflows and is a tab stop. **The prices table's container at 320** (`div[data-slot="table-container"]` in «الأسعار المعلنة») was already on `main` and is not one of finding 224's places; it is left for the owner (the report names it). On the map, every tooltip is `aria-hidden="true"` and no mark carries `aria-describedby`, in every run (on `main` the chosen and the hovered marks did).

## Screenshots

Local only, never committed: `C:\Users\basel\Downloads\axe-fixes-shots\` — `main/`, `main-map/` (the baseline), `branch/` (each screen, phone and desktop, light and dark, Arabic and English, the map with a mark chosen), `branch-rings/` (the focus ring on each strip, reached by Tab: the photos at 320 and Occupancy at 390, light and dark, whole on its four sides).

## Definition of Done checklist

- [x] Acceptance criteria met, scope kept (19 files).
- [x] Lint and typecheck clean; build passes.
- [x] Tests in the owning lane (component), passing; each seen failing.
- [x] No hardcoded user-facing text; no new strings (`ScrollRegion` has no words).
- [x] UI checked in RTL and LTR, light and dark, phone and desktop (Chrome, axe).
- [x] No protected action changed.
- [x] Triggered documentation updated: foundation §3, §10, §12; architecture §6; spaces and finance histories; finding 224 Resolved.
- [x] Each fact has one home.
- [x] Every claim names its test or command.
- [x] Atomic history (three commits), pushed.
