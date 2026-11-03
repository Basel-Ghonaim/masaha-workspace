## Summary

PUBLIC, PR 1b of five: the site's Directory gains its filters and near me (the plan's PR 1 commits 6–7, cut by the owner's A13), after eight small commits carried from #101's review.

- **The filters:** the place (`lookups`' `AreaFilter`, set by the page in the list's `placeFilter` slot), «متاحة الآن فقط» and «المساحات الموثّقة فقط», the price (a period and a budget «من» «إلى» in whole shekels, each refused bound said and left out), and «أخرى» (student prices, open on Friday); each applies at once, in the address. They are drawn once per width: a sidebar from 1024 px, a bottom sheet below it, whose button is its own trigger and counts the filters in force, and whose primary button counts the spaces they leave in Arabic agreement. The design system's barrel exports `useMediaQuery` for it (S6).
- **Near me:** «الأقرب إليّ» asks for the location only when pressed; a position less precise than 2 km or outside the Strip is not used; of any other only the point rounded to three decimals is kept, in memory only. While it sorts, the list is asked with `sort=distance` and the point in `Masaha-Near`, never in the query; each card says how far it is. Stopping keeps the point; «مسح موقعي» drops it and every answer ordered by distance. The privacy line shows only while a location is asked or sent; a refused or imprecise one offers «اختر منطقتك».

**Carried from #101** (the owner's decisions of 2026-10-21, `0_CARRIED_FROM_101.md`):
1. The focus moves to the results only for a page the visitor chose (a push), never for a search, an order or a page past the last — `50fe2c75`.
2. After a rate limit's countdown the failure stays with its retry — `3c837b30`.
3. A hand-edited budget with its maximum under its minimum never reaches the server — `21de283d`.
4. `lookups.md`'s lines 18 and 104 — checked, true once commit 6 wires `AreaFilter`; no change.
5. The site's `main` takes the focus after signing in (a shell opened by navigation); the focus shell's own lack added to finding 130 — `b82d213b`.
6. `usePageInRange` moves to `shared/lists`; the inline copy goes — `dafc816c`.
7. A card's details are its link's description, read after its name — `52e31433`.
8. The count is announced only from a real answer — `50fe2c75`.
9. No visible loading sign on the next page — recorded as **finding 132**, not built — `2fe598c5`.
10. A failed refresh over the cards gains its test — `3c837b30`.
11. A count of zero draws no line — `ec0f4709`.

## Scope / Acceptance criteria / Out of scope

**Scope:** `features/directory` (the filters: `priceBounds`, `usePriceFilter`, `useFiltersPanel`, `FiltersForm`, `PriceFilter`, `FiltersSidebar`, `FiltersSheet`; near me: `nearPoint`, `distanceText`, `nearMeStore`, `useNearMe`, `useLocationStatus`, `NearMeButton`, `LocationStatus`, the repository's header, the keys' point); `shared/design-system/index.ts` (`useMediaQuery`); `shared/lists` (`usePageInRange`); `features/space-links` (two imports); `pages/site` (`DirectoryPage`'s slot, `useMainFocus`); copy `directory` (both catalogues); a test helper `src/test/fakeGeolocation.ts`; docs `directory.md`, `foundation.md` §3, `architecture.md` (§1, §2, §3), `overview.md`, findings 130 and 132.

**Acceptance criteria (PR 1b's part of the plan's PR 1):**
- [x] The place filter, the price filter, the two switches and «أخرى» are in the address: a reload, Back and a shared link show the same list; a value the server would refuse falls back and never reaches the request. — `filtersOf`, `priceBounds`, `usePriceFilter`, `useDirectoryFilters` tests; the real run.
- [x] Below 1024 px the filters open in a bottom sheet from a button that says whether it is open and how many filters apply; its primary button counts the spaces (Arabic agreement); from 1024 px they are a sidebar. — `FiltersSheet.component.test.tsx` (390, 768, 1440); the real run at the three widths.
- [x] «الأقرب إليّ» asks for the location only when pressed; the point is rounded to three decimals before anything keeps it, kept in memory only, sent only in `Masaha-Near` with `sort=distance`; «إيقاف الترتيب حسب المسافة» keeps it, «مسح موقعي» drops it and every answer ordered by distance; a denied, unavailable, imprecise or out-of-Strip location says so and offers «اختر منطقتك»; the privacy line shows only where a location is being sent. — `nearPoint`, `directoryRepository`, `useNearMe`, `useDirectoryList`, `LocationStatus` tests; the real run's network log.
- [x] Every counted line through the catalogue's plural forms (the filters' count, the sheet's primary).
- [x] Lint, typecheck, `test:unit`, `test:component`, the production build, `check:build`, `check:classes`, `format:check`, `check:links` green; CI below.

**Out of scope:** the map and its point picked by hand (PR 2), the space's page (PR 3), Home and About (PR 4). No API, `packages/shared`, schema, migration, seed or dependency change.

## Change type

Feature (web) with one refactor, seven small fixes carried from #101 and documentation. Labels: `feat`, `area:web`, `area:docs`, `area:design-system` (the layer's barrel exports `useMediaQuery`).

## Evidence

Run locally on the head (the commands' own lines):
- `npm run lint`, `npm run typecheck` — exit 0 (on each commit).
- `npm run test:unit -w @masaha/web` — `Test Files  105 passed (105)` / `Tests  897 passed (897)`.
- `npm run test:component -w @masaha/web -- src/features/directory src/features/lookups src/features/space-links src/pages/site src/shared/lists src/shared/design-system` — `Test Files  100 passed (100)` / `Tests  623 passed (623)` (run again after the real run's fix).
- `NODE_ENV=production npm run build`, `npm run check:build` — "No dashboard code in the site's first download." / "No data-table or leaflet, nor Leaflet's stylesheet, in the site's first download."
- `npm run check:classes` — 1133 files; `npm run format:check` — clean; `npm run check:links` — 2499 links resolve.
- The first download: 985,147 → 989,912 bytes, the same six chunks (the catalogue's new words); no `leaflet`, `data-table`, `dashboard` or `directory` in it.
- **Seen failing first:** each carried fix's test, and the services' and `useNearMe`'s tests. Tests written after their code (the price filter's hook, the sheet's three, near me's list and state line) are each proven by their planned break, seen red. The privacy, bound and width guards each have their own break, seen red, then restored (rounding, accuracy, the point in the query, ask on mount, storage, the raw point, the cache's distance answers, accept 0, both drawn, the sheet at every width).
- **Real run** on the current `masaha_dev` (**DEMO_SEED waived for this PR by the owner, 2026-10-21**), local headless Chrome over CDP, Arabic light and English dark: the sheet at 390 and 768 and the sidebar and the results' grid at 1440 in both; the place filter (two areas, «منطقتان محددتان»); the budget (a day, 10–30 ₪; an inverted range's line, no 422); each switch and «أخرى»; near me granted, stopped, sorted again, cleared; denied, imprecise (5 km), outside the Strip (Cairo); «اختر منطقتك» (the sheet at 390, the sidebar at 1440); a search typed on page 2 keeps the focus; the sidebar's grid width break. **The privacy proof in the network log:** no coordinate in any URL; `Masaha-Near` only on the `sort=distance` request, `31.502,34.467` (three decimals); none after «مسح موقعي».
- **Not run locally (CI judges):** the full `test:component` lane, `test:unit` of `apps/api` and `packages/shared`, `test:api` (no API or shared change). **Not performed in the browser:** carried item 2's rate limit (1,200 guest requests; its `useDirectoryList` test) and item 5's sign-in (it writes a refresh token: data; its `authPages` test). No data changed in `masaha_dev`.

## Screenshots

Taken in the real run (RTL and LTR, light and dark, 390, 768 and 1440); attached by the owner.

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
