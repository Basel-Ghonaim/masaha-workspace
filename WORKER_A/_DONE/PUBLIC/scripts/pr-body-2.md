## Summary

PUBLIC, PR 2 of five: the site's Directory gains its map — the three plan commits for PR 2 (`feat/map`, `feat/directory-map`, `feat/directory-pick`), after six fix commits and two findings commits carried from #103's review.

**Carried from #103** (items 1–12, `0_CARRIED_FROM_103.md`):
1. Near me's focus and status — `2c2f9f37` (fix commit)
2. Stop locating when no answer comes — `2c2f9f37`
3. Clear what found nothing — `2c2f9f37`
4. Near me's privacy gates — `2c2f9f37`
5. No distance once the distance order stops — `2c2f9f37`
6. Reset the price on clearing — `2c2f9f37`
7. Close the sheet when it widens — `2c2f9f37`
8. Finding 130 widened to the focus shell — `2584d86f` (findings commit)
9. Finding 133, the place filter's cap — `2584d86f`
10. The stopped state's bare «مسح موقعي» — kept as is, no commit
11. DirectoryList's unwrapped comment — in `2c2f9f37`
12. —

**The map** (`shared/map`):
- `MarkerMap` — a generic map of many marks, lazy Leaflet, the visitor's point, a centre crosshair to pick a point, the viewport handed back; `MapMark` type (shape + tone).
- `shared/design-system/leaflet.css` — the four mark shapes, the selected ring, the crosshair, the user's point.

**The directory on the map** (`features/directory`):
- Pins query (`GET /map/spaces`) with the list's filters, re-ask within the viewport past 1,000 pins.
- «قائمة | خريطة» view switch (`?view=map`) at every width.
- The map view, its toolbar (search, sheet at every width, near me, state line), the legend, the selected space's card (from 768 px) and sheet (non-modal, below 768 px).
- Near me's map fallback: «حدّد موقعي على الخريطة» from the denied/imprecise line — centre crosshair, arrow keys pan, «ثبّت الموقع هنا» places the rounded point, «رجوع» restores the previous location.

**Copy:** `directory.view`, `directory.map`, `directory.pick`; `directory.near` (the map fallback).

**Docs:** `directory.md` (what it does, «The map on the web», four Web decisions — S12, U6/issue 21, issue 22, issues 19–20 — code map, Web history), finding 46's evidence line.

## Scope / Acceptance criteria / Out of scope

**Scope:** `shared/map` (`MarkerMap`, `LeafletMarkerMap`, `MapMark`, `markClass`, `MapFailed`, `MapMarkSample`, `MapLayers`, `leaflet.css`); `features/directory` (repository `pins`, hooks `usePinsQuery`, `useDirectoryMap`, `useSelectedPin`, `useViewSwitch`, `useNearMe` picking, services `pinMark`, `boundsText`, `nearPoint`, components `DirectoryView`, `ViewSwitch`, `DirectoryMap`, `MapLegend`, `SelectedCard`, `SelectedSheet`, `PickCard`, `MapNotice`, `SpaceSummary`); `pages/site/public/directory/DirectoryPage`; copy `directory` (both catalogues); docs `directory.md`, `architecture.md` §6, `foundation.md` §3.

**Acceptance criteria (the plan's PR 2):**
- [x] «قائمة | خريطة» switches the view (`?view=map`) at every width; the map shows every space that passes the filters as a pin whose state is a shape as well as a colour, the legend in the map; past 1,000 pins it says so and asks again within the viewport.
- [x] A pin is a named, focusable button; choosing one shows its card (a non-modal bottom sheet on a phone, a card in the map from 768 px), «عرض التفاصيل» leading to its page.
- [x] «حدّد موقعي على الخريطة» (from the state line) shows a centre crosshair; «ثبّت الموقع هنا» places the rounded point and sorts by distance; «رجوع» returns to the location before; the arrow keys pan.
- [x] Leaflet and its stylesheet stay out of the site's first download (`check:build`) and arrive only with the map.
- [x] The same checks and CI as PR 1.

**Out of scope:** the space's page (PR 3), Home and About (PR 4). No API, `packages/shared`, schema, migration, seed or dependency change.

## Change type

Feature (web) with documentation. Labels: `feat`, `area:web`, `area:design-system`, `area:docs`.

## Evidence

Run locally on the head (the commands' own lines):
- `npm run lint`, `npm run typecheck` — exit 0 (on each commit).
- `npm run test:unit -w @masaha/web` — `Test Files  108 passed (108)` / `Tests  903 passed (903)` (`scripts/lane2-unit.txt`).
- `npm run test:component -w @masaha/web -- src/shared/map src/features/directory src/pages/site src/shared/design-system` — `Test Files  57 passed (57)` / `Tests  360 passed (360)` (`scripts/lane2-component.txt`).
- `NODE_ENV=production npm run build`, `npm run check:build` — `✓ built in 2.04s`; "No showcase code in 49 build files (1028 strings checked)." / "No dashboard code in the site's first download." / "No data-table or leaflet, nor Leaflet's stylesheet, in the site's first download."
- `npm run check:classes` — `No physical direction or arbitrary-value classes in 1166 files.`
- `npm run format:check` — clean; `npm run check:links` — `2569 links in 205 documents and 1672 source files all resolve.`
- The first download: **992,328 bytes, 7 chunks** (entry 254,998; CSS 83,197; `jsx-runtime` 123,714; `routing` 236,489 and `design-system` chunk 279,426 together 515,915; `react-dom`, `direction`, `mutation` unchanged). No `leaflet`, `data-table`, `dashboard`, `directory`, `DirectoryPage` or `HomePage`. The map's marks and crosshair live in the lazy `MapLayers-*.css` with Leaflet's stylesheet; `not-empty:mt-2` reached the entry's CSS.
- **Seen failing first:** the map commit's tests (47–49), the directory map commit's tests (50–57), the pick commit's tests (59–60). Own breaks on the map's keyboard/fallback, the bound re-ask, the sheet's width/modal, and the pick's privacy/rounding/clamp — each seen red, then restored.
- **Real run** on `masaha_dev` (local headless Chrome over CDP, Arabic light and English dark):
  - **Centre case** (`node run2.mjs centre`, exit 0): granted on the map at 390 and 1440 — state line shows distance order, privacy line, stop and clear; «مركّز على موقعي» does not move the map (already centred). Screenshots: `2-centre-ar-light-390.png`, `2-centre-en-dark-1440.png`.
  - **Leaflet case** (`node run2.mjs leaflet`, exit 0): dev Leaflet requests before «خريطة»: 0 — after: 5 (LeafletMarkerMap.tsx, leaflet.css, leaflet.js, react-leaflet.js, MapLayers.tsx). Screenshot: `2-leaflet-dev.png`. Log first line: `before «خريطة»: 0`.
  - **Carried case** (`node run2.mjs carried`, exit 0): the carried items 1 and 3 verified in the browser (focus/state line, clear on no match).
- **Privacy in the network log:** ar 390: 15 API requests, 1 with `Masaha-Near` (`31.41,34.302`) on `sort=distance`; en 1440: 21 requests, 1 (`31.568,34.395`); no coordinate in any URL (the map's `bounds` aside).
- **Not run locally (CI judges):** the full `test:component` lane, `test:unit` of `apps/api` and `packages/shared`, `test:api`.
- **Not performed in the browser (seed-dependent):** the FULL barred pin (`sada-space` was AVAILABLE at run time; tests 50 and 55 prove it); «مركّز على موقعي» with a granted location; the carried items' browser cases beyond what the script covers (their component tests prove them).

## Screenshots

Taken in the real run (RTL and LTR, light and dark, 390, 768 and 1440 where applicable); attached by the owner.
- Pins by state and legend: `2-pins-ar-light-390.png`, `2-pins-ar-light-768.png`, `2-pins-ar-light-1440.png`, `2-pins-en-dark-390.png`, `2-pins-en-dark-768.png`, `2-pins-en-dark-1440.png`.
- Selected space card/sheet at three widths: `2-select-*`, `2-select-panned-*-390`.
- Filter on the map (sheet at 1440 too): `2-filter-*`.
- Pick location on map (denied → crosshair → arrows → place → change → back): `2-pick-*`.
- Centre granted: `2-centre-ar-light-390.png`, `2-centre-en-dark-1440.png`.
- Leaflet lazy load: `2-leaflet-dev.png`.
- Details navigation: `2-details-*`.

## Definition of Done checklist

- [x] Acceptance criteria met, scope kept.
- [x] Lint and typecheck clean; build passes.
- [x] Tests added in the owning lane and passing.
- [x] No hardcoded user-facing text; both catalogues (ar, en) updated.
- [x] UI checked in RTL and LTR, light and dark, phone and desktop.
- [x] Authorization enforced on the server for any protected action (public reads only).
- [x] Triggered documentation updated in this PR; no deferred document's trigger met.
- [x] Each fact has one home; nothing claimed that is not built.
- [x] Every claim above names the test or command that proves it.
- [x] Atomic history, pushed, PR description complete.