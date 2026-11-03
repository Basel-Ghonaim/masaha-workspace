## Summary

PUBLIC, PR 1a of five: the site's «المساحات» becomes the Directory's list. A new web feature, `directory`, lists the publicly listed spaces 20 a page from `GET /spaces`: each card one link to the space's page, with its cover or the space's mark, its name, its area with its governorate (`lookups`' `AreaName` on the public catalogue, set by the page), its live status by word, «موثّقة» and today's hours on Gaza's calendar; no price. The search (paused typing), the order and the page live in the address. The site's shell gains its skip link and moves the focus to `main` on a new page. Two refactors first: the list's pages move from `space-links` to a new `shared/lists`, and the name and clock rules from `spaces` to `shared/lib`, so the site can use them. `lookups` offers the site its area filter (`AreaFilter`, set by the page from PR 1b) and `AreaName` takes a `source`.

The plan's PR 1 commits 1–5 (the owner's A13); the filters and near me are PR 1b.

## Scope / Acceptance criteria / Out of scope

**Scope:** `shared/lists` (new); `shared/lib` (`names/`, `time/clockOf`); `pages/site/shell` (`SkipLink`, `useMainFocus`, `main#main`); `features/lookups` (`AreaFilter`, `AreaName`'s `source`); `features/directory` (new); `pages/site/public/directory/DirectoryPage.tsx`; copy `site`, `lookups`, `directory` (both catalogues); docs `directory.md`, `lookups.md`, `architecture.md`, `foundation.md` §5, `overview.md`, `docs/README.md`, finding 130.

**Acceptance criteria (PR 1a's part of the plan's PR 1):**
- [x] `/spaces` lists the publicly listed spaces 20 a page from `GET /spaces`, each card a link to `/spaces/:slug` (the site's 404 until PR 3) with its cover or mark, its name (U3), its area with its governorate, its live status by word (or «لا تتوفر حالة مباشرة»), «موثّقة», today's hours on Gaza's calendar, and no price. — `useDirectoryList`, `DirectoryList`, `cardView`, `todayHours` tests; the real run.
- [x] The search (paused typing), the order and the page are in the address (and every filter key, read and sent, for a shared link): a reload, Back and a shared link show the same list; a value the server would refuse falls back to its default and never reaches the request. — `filtersOf`, `requestOf`, `useDirectoryFilters` tests; the real run.
- [x] Loading (skeleton cards), a failure (with its reference and «إعادة المحاولة»), offline, an empty directory, no match (with «مسح الفلاتر») and a page past the last are each their own state. — `useDirectoryList` tests 20–25.
- [x] The skip link reaches `#main`; a new page takes the focus to it; a new page of results takes the focus to the results' heading. — `SiteLayout` tests 3–4, `DirectoryList` test 28; the real run.
- [x] Every counted line through the catalogue's plural forms (the counts, the area filter's summary).
- [x] Lint, typecheck, `test:unit`, `test:component`, the production build, `check:build`, `check:classes`, `format:check`, `check:links` green locally; CI below.

**Out of scope (PR 1b):** the place, price and state filters, the filters' sidebar and sheet (`useMediaQuery`'s export, S6), near me and its privacy line, the distance on the card. Later PRs: the map, the space's page, Home and About. No API, `packages/shared`, schema, migration, seed or dependency change.

## Change type

Feature (web) with two refactors and documentation. Labels: `feat`, `area:web`, `area:docs`, `area:design-system` (foundation §5's status roles; the layer's code is unchanged in this PR).

## Evidence

Run locally on the head (the counts are the commands' own lines):
- `npm run lint`, `npm run typecheck` — exit 0.
- `npm run test:unit` — web `Test Files  102 passed (102)` / `Tests  888 passed (888)` (shared 233, api 797).
- `npm run test:component` — `Test Files  193 passed (193)` / `Tests  1257 passed (1257)` (run again after the last code change; the first run had finding 87's routes test at 3,076 ms, which passed alone in 2,232 ms).
- `NODE_ENV=production npm run build`, `npm run check:build` — "No dashboard code in the site's first download." / "No data-table or leaflet, nor Leaflet's stylesheet, in the site's first download."
- `npm run check:classes` — 1107 files; `npm run format:check` — clean; `npm run check:links` — 2497 links resolve.
- The first download, from the manifest: base 978,177 bytes → head 985,147 bytes, the same six chunks; no public page, `leaflet`, `data-table` or `dashboard` chunk in it.
- Finding 27, re-checked: in both builds, `PackagesPage`'s and `SettingsPage`'s chunks and `dashboard` still import each other — not resolved here; the owner's call.
- **Seen failing first:** every new test, except the repository's and `useDirectoryList`'s, which ran first after their code; each planned break was made and seen red, then restored (21 for the list, 5 for `lookups`, 2 for the shell).
- **Real run** (local headless Chrome over CDP, Arabic light and English dark at 390, 768 and 1440): the list, a search by an English name in Arabic, a search of diacritics only (no 422), no match and «مسح الفلاتر», the sort (by name, «الأفضل تطابقًا» with a search), a reload and a copied link, page 2 (the focus on the results; Back), the skip link and the focus after a header link, the first download on the production build, the results' columns' width break.
- **Not run:** `test:api` (no API or shared change; CI runs it). Not performed in the real run: `FULL`/`CLOSED` (not in the data; `cardView.unit.test.ts`), a cover that fails to load (`DirectoryList.component.test.tsx`).

**For the supervisor (decision 7):** the line for `DECISIONS_PUBLIC.md`, under U12 —
> **Superseded by the amendments at the top (2026-10-12):** U9's card part («the card keeps its four general cells and one «للطلاب» line») and U12's open point (whether the cells stay) — the card shows no price; U2's sort list loses «الأقل سعرًا»; the amenities are no filter. The web builds the amended rules (PUBLIC, PR 1).

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
