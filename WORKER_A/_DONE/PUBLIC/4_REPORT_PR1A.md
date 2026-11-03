# PUBLIC — PR 1a report (`feat/directory-list`, the Directory's list)

Executor: Claude Code (Opus 5.5), 2026-10-21. Plan: `2_PLAN.md` with the owner's approval note (A13 taken:
this PR is the plan's PR 1 commits 1–5 only).

## Final report (2026-10-21)

### 1. The pull request
**#101** https://github.com/Basel-Ghonaim/masaha/pull/101 — `feat(directory): list the spaces page by page`, head
**`e50d9222`** (the branch's head, `origin/feat/directory-list` the same). CI: all ten checks pass on it
(`build`, `check:classes`, `check:links`, `format:check`, `lint`, `test:api`, `test:component`, `test:unit`,
`typecheck`, CodeRabbit); `mergeStateStatus` **`CLEAN`**. Not merged.

### 2. The commits
| SHA | Subject (chars) |
|---|---|
| `653acb80` | refactor(space-links): share the list's pages (45) |
| `04281db4` | refactor(spaces): share the name and clock rules (48) |
| `c28099de` | feat(site): add a skip link and focus each page (47) |
| `d280c0db` | feat(lookups): offer the public areas to the site (49) |
| `e50d9222` | feat(directory): list the spaces page by page (45) |

99 files against `origin/main` (45 A, 45 M, 9 R); `#PRNUM` replaced by `#101` in each commit's tree.

### 3. What was run, and what was not
- Per commit: `lint`, `typecheck` (exit 0 each) and the touched test files.
- On the head, once each: `test:unit` — web `Tests  888 passed (888)`, api 797, shared 233; `test:component` —
  first run `1 failed | 1256 passed (1257)`, the failure finding 87's routes test at 3,076 ms (passed alone,
  2,232 ms: the standing exception); re-run after the real run's fix, `Test Files  193 passed (193)` / `Tests
  1257 passed (1257)`; production build; `check:build`, `check:classes` (1107 files), `format:check`,
  `check:links` (2497 links) — all green.
- The first download: base 978,177 → head 985,147 bytes, the same six chunks, no public page, `leaflet`,
  `data-table` or `dashboard` chunk.
- The real run (headless Chrome over CDP, Arabic light and English dark, 390/768/1440): every PR 1a case
  performed (§5 below) except, by design, `FULL`/`CLOSED` (not in the data; `cardView.unit.test.ts`) and a
  cover that fails to load (`DirectoryList` test 29). `masaha_dev` unchanged (GETs only).
- Not run: `test:api` locally (no API or shared change; CI ran it, green).

### 4. Breaks and tests seen failing first
- Breaks, each seen red and restored: shell tests 3–4 (2); lookups tests 5–9 (5); the list tests 10–16, 18–30,
  44 (21); the results' columns' width break in the real run (one 1216 px column). Each with its red line in
  §3 and §5 of the working log.
- Seen failing first: every new test, except `directoryRepository.unit.test.ts` and
  `useDirectoryList.component.test.tsx`, which ran first after their code (their breaks prove them).

### 5. Problems met, and how each was solved
- The lookups failure test answered a 500, which the transport retries past the test's wait → a 404 (my test).
- The offline test: a GET's network failure is retried for 3 s → fake timers advancing 3.1 s.
- The `DirectoryList` count and the first draft of the busy test were my test's defects → fixed.
- Four existing tests broke: the Directory page now needs a QueryClient and its `h1` is «مساحات العمل» →
  updated (`SiteLayout`, `authPages`, `changePasswordPage`).
- `useLanguage()` returns `string` → narrowed to `'ar' | 'en'` for the request.
- Real run: Radix's Select did not choose on `el.click()` nor by keys after a viewport resize closed it → real
  mouse events, the open-list shot taken without a resize.
- Real run: an English-only name aligned left in an Arabic card (`dir` on the `h3`) → `lang`/`dir` on an inner
  `span`, folded into commit 5, lanes re-run.
- Worker B's short API test runs → waited for 30 s of quiet before each full lane.

### 6. What behaved unexpectedly
- A root `npm run dev` started in the background produced a second **API** watcher (its log showed
  `@masaha/api dev`), not Vite; stopped by its id (10816) and Vite started with `npx vite` in `apps/web`. Cause
  not found.
- The dev server loads `pages/dashboard/routes.tsx` and a pre-bundled `@tanstack/react-table` on `/spaces`
  (unbundled development serving); the production first download was checked separately and is clean.
- Finding 27: neither build has a `SpaceLayout` chunk any more, but `PackagesPage` and `SettingsPage` import
  `dashboard` both ways, on `main` as on this branch — the finding stays open, for the owner.
- The CI watch in the background was stopped by Claude Code for low memory (not a failure); the owner reported
  CI green.
- `masaha_dev` holds many leftover test spaces («Shot Hub …», «Run Hub …»);
  the run read them, changed nothing.

### 7. The early conflict check
`gh pr list --state open` → only #101 itself. No other open PR: nothing to `merge-tree` against.

### 8. Departures from the prompt and the plan
- **The split of commit 5:** what only near me or the filters' UI reaches is PR 1b's — the repository's `near`
  argument and the `Masaha-Near` header (test 14's privacy half), `hasNear`, `distanceText` and the card's
  distance (test 17, design issue 9), the distance order's word, `card.distance`, the `placeFilter` slot.
  Tests 17 and 31–43 are 1b's. `filtersOf`/`requestOf` read and send every S5 key, as the plan's commit 5.
- **S6 (`useMediaQuery` in the layer's barrel)** is left to 1b, where the filters use it; `area:design-system`
  kept for foundation §5's status roles (the prompt gave S6 as its reason).
- The card's `h3` sits inside `CardTitle` (check b's fallback); its name's `lang`/`dir` on a span inside it.
- `useMainFocus` compares the path with the one it last focused for (StrictMode safety); same behaviour.
- The page-past-last rule is a second, inline instance of `space-links`' `usePageInRange` — for the review.
- `useDirectoryFilters` has no `applied` (the filters button's, 1b); `useAreaFilter` also returns its list's words.
- Four existing tests changed (above); 99 files rather than ≈ 63.
- The search and the sort each in a `Field` with a visually hidden label, so they line up in one row.

---

## Working log (written as the work went)

## 1. First checks (before any edit)

1. `git status --short` clean; `git switch main`; `git pull --ff-only` → `Already up to date.`; HEAD `2c4d78f9`.
2. The PR before: `gh pr view 99 --json state,mergeCommit` → `MERGED 2c4d78f9d566363b164ab369103de996d1b0fe68`.
3. The base diff `git diff --name-status cf3190a4 origin/main` (#99 and #100): of this PR's code files, only
   `shared/lib/index.ts` (+ `wholeNumberOf`), `shared/forms/index.ts` (+ `FailureLines`, `FormSchema` types) and
   `shared/copy/*/index.ts` (+ `spaceSettings`, `staff`) changed — additions the plan's edits sit beside, nothing
   the plan does not cover. `packages/shared` changed only in `core/errors`, `desk`, `visits` (not `directory`,
   `lookups`, `occupancy`, `spaces`, `core/gazaTime`) → `npm run build -w @masaha/shared` (exit 0). OWNER_SETUP's
   `4_REPORT_PR3.md` departures read: none touch this PR's files.
4. Open PRs: `gh pr list --state open` → none.
5. Checks against the code:
   - a. `useMediaQuery(query: string): boolean` in `shared/design-system/lib/useMediaQuery.ts` — holds.
   - b. `CardTitle` renders a `div` (no heading level) → the card's `h3` goes inside it (**departure**, the
     plan's fallback).
   - c. `useRefusalView` words `network` and `timeout` from `errors` (both keys present) — holds.
   - d. `ComboboxItem` takes `keywords` — holds.
   - e. eslint restricts only Leaflet and the layer's libraries; `zustand` is not restricted for `features/` —
     holds (used from PR 1b).
   - f. `useGovernoratesQuery({ enabled })` — holds.
6. Finding numbers: the index's highest is 113; 130 is free.
7. Data inventory (`scripts\inventory.mjs`, plain GETs; output `scripts\inventory.out.txt`): `docker start
   masaha-postgres-1`; `npx prisma migrate status` → `Database schema is up to date!` (21 migrations). The API on
   3320, then stopped by process id (7232, 26396, 24096); ports 3320/5320 free.
   - `GET /spaces?limit=50`: **35 listed spaces** (`totalRecords: 35`) → two pages at 20; areas Al-Rimal, North
     Gaza Strip, Al-Tuffah, An-Nasr, Al-Mawasi, Tal al-Hawa; 7 verified; 2 with a cover (`masaha-demo`,
     `gallery-test-space`); 5 with hours; 12 with an Arabic name (23 English only); live status `AVAILABLE` 1
     (`masaha-demo`), none 34; no `FULL`, no `CLOSED`.
   - `GET /map/spaces`: 200, 35 pins. `GET /spaces/:slug` each 200.
   - PR 1a's cases the data holds: the list, page 2, a cover and a mark, a live status and «لا تتوفر حالة
     مباشرة», «موثّقة», today's hours, a search by an English name in Arabic, the sort. `FULL`/`CLOSED`: not in
     the data (the plan's *Not performed, by design*: the unit test 15 proves the roles).

## 2. Branch

`git switch --no-track -c feat/directory-list origin/main` (at `2c4d78f9`).

## 3. Commits

### Commit 1 — `653acb80` `refactor(space-links): share the list's pages` (45)
- `git mv` of `ListPagination.tsx`, `pageItems.ts` (+ unit test), `paginationView.ts`, `PaginationView.ts`,
  `usePausedSearch.ts` to `shared/lists/` (unchanged, 100 % renames); `shared/lists/index.ts` (four exports,
  `pageItems` internal); the seven `space-links` importers read `@shared/lists` (the `git grep` found no other).
  `architecture.md`: §1's zone table gains `lists`; the status line names `shared/lists`' list pages and paused
  search.
- A move, no new test: `lint` exit 0; `typecheck` exit 0; `vitest run --project unit src/shared/lists` →
  `Tests  3 passed (3)`; `vitest run --project component src/features/space-links` → `Test Files  22 passed
  (22)` / `Tests  156 passed (156)`.

### Commit 2 — `04281db4` `refactor(spaces): share the name and clock rules` (48)
- `git mv` of `spaceName.ts` (+ unit test) and `SpaceNameView.ts` to `shared/lib/names/`; `clockOf` to
  `shared/lib/time/clockOf.ts` with its case moved from `clockTime.unit.test.ts` to `clockOf.unit.test.ts`
  (unchanged); `clockTime.ts` imports `clockOf`, keeps `minuteOf`/`settledClock`. Importers: the eight the plan
  lists, plus `hooks/hours/useReadOnlyHours.ts` and `services/hoursForm.ts` (`clockOf`'s, found by `git grep`).
  `space-links`' own `SpaceNameView` left as it is. `architecture.md`'s status line: «money, name and clock
  helpers».
- `lint` exit 0; `typecheck` exit 0; `vitest run --project unit src/shared/lib src/features/spaces` → `Test
  Files  18 passed (18)` / `Tests  93 passed (93)`; `--project component src/features/spaces` → `Test Files  23
  passed (23)` / `Tests  228 passed (228)`.

### Commit 3 — `bb3e3447` `feat(site): add a skip link and focus each page` (47)
- `SkipLink.tsx` (the plan's classes), `useMainFocus.ts`, `SiteLayout` (`<SkipLink />` first, `<main id="main"
  tabIndex={-1} … outline-none>`); `site.skipToContent` in both catalogues; `architecture.md` §2 › the site's
  shell; finding 130 and its index line.
- Shape: `useMainFocus` compares the path with the one it last placed the focus for (a ref holding the first
  load's path), not a "first render" flag — React's StrictMode runs an effect twice on mount in development, and
  a flag would move the focus on the first load there. Same behaviour as the plan's sentence.
- Tests 3 and 4 (`SiteLayout.component.test.tsx`), written first → red: `Tests  2 failed | 8 passed (10)`
  (`Unable to find an accessible element with the role "link" and name "تخطَّ إلى المحتوى"`; `expect(element).
  toHaveFocus()`). After the code → `Tests  10 passed (10)`.
- Breaks, each red, each restored from a copy: test 3, `href="#content"` → `Tests  1 failed | 9 passed (10)`;
  test 4, the effect keyed on `location.key` → `Tests  1 failed | 9 passed (10)`.
- `lint` exit 0; `typecheck` exit 0; `check:classes` → `No physical direction or arbitrary-value classes in 1068
  files.`

### Commit 4 — `070cb9a8` `feat(lookups): offer the public areas to the site` (49)
- `AreaFilter` (+ component test), `useAreaFilter` (+ component test); `AreaName`/`useAreaName` take `source`
  (`public` reads `useCatalogueQuery` only, `admin` `useGovernoratesQuery` only, each `enabled` by it);
  `SpaceEditPage` passes `source="admin"` (the one caller `git grep` found); `lookups.areaFilter` in both
  catalogues (§9's words); `lookups.md` (scope, *Who uses it*, the names, «The area filter», the web decision,
  code map, web history).
- Shape: `useAreaFilter` also hands back the list's words (`search`, `searchPlaceholder`, `list`, `none`)
  beside the plan's `label`, `summary`, `groups`, `loading`, `failure`; the failure's retry is an outline small
  `Button` in the list's empty text.
- Red first: `Tests  1 failed | 17 passed (18)` (`expected [ '/admin/governorates' ] to deeply equal [
  '/lookups' ]`), and the two new files failing to import `./useAreaFilter` / `./AreaFilter` (the code not
  written yet). My own test defect fixed: the failure case first answered a 500, which the transport retries
  (it timed out at 3 s); it answers a 404 now.
- Green: `vitest run --project component src/features/lookups` → `Tests  138 passed (138)`; with
  `src/pages/dashboard/admin` → `Test Files  7 passed (7)` / `Tests  32 passed (32)`.
- Breaks (`scripts\brk.py`: copy, change, run, restore), each red:
  - 5 a governorate with no area kept → `Tests  2 failed | 1 passed (3)`;
  - 6 the count for one area (`chosen(1)`) → `Tests  1 failed | 2 passed (3)` (`expected 'منطقة واحدة محددة'
    to be 'النصر'`);
  - 7 the retry left out → `Tests  1 failed | 2 passed (3)` (`expected [] to have a length of 2`);
  - 8 `keywords` left out → `Tests  1 failed (1)` (`Unable to find an accessible element with the role
    "option"`);
  - 9 `source` ignored → `Tests  1 failed | 3 passed (4)` (`expected '' to be 'Al-Rimal · Gaza'`).
- `lint` exit 0; `typecheck` exit 0; Prettier fixed two files of mine before the commit.

### Commit 5 — `57b7cdb9` (was `e01245a7`) `feat(directory): list the spaces page by page` (45)
- `features/directory/` (new): repository (+ unit), keys, `useDirectoryFilters` (+ component), `useDirectoryQuery`,
  `useDirectoryList` (+ component), services `filtersOf`, `requestOf`, `cardView`, `todayHours` (each + unit),
  types, components (`DirectoryList` (+ component), the card, its cover, badge and skeleton, the results, their
  states, the failure alert, the search, the sort); `DirectoryPage`; the `directory` copy section in both
  catalogues; test 44 in `routes.component.test.tsx`. Docs: `directory.md` (header, what it does, who, how it
  composes, «The directory's list on the web», *Web decisions*, code map, *Web history*), `architecture.md` (§2
  *Built so far*, §7 *Polling*), `foundation.md` §5 (Full `warning`, Closed neutral — §14.8), `overview.md`,
  `docs/README.md`.
- **The split of PR 1's commit-5 content (the plan does not say; the prompt asks):** what only near me or the
  filters' UI reaches is left to PR 1b, so 1a carries no code nothing in it can reach — the repository's `near`
  argument and the `Masaha-Near` header (test 14's privacy half), `hasNear`, `distanceText` and the card's
  distance (test 17, design issue 9), the `distance` order's word, `card.distance`, and the `placeFilter` slot
  (the page sets two slots; `AreaFilter`, commit 4, is set from 1b). Test 14 is taken without its privacy
  half; tests 17, 31–43 are 1b's. `filtersOf`/`requestOf` read and send every S5 key (a shared link's filters
  apply), as the plan's commit 5 has them.
- **Departures:**
  - `useDirectoryFilters` returns no `applied` count (it is the filters button's, 1b); `anyApplied` is there.
  - The "page past the last" rule is written inline in `useDirectoryList`, a second instance of `space-links`'
    `usePageInRange`, which the site cannot import (S2 moved only five pieces) — for the review.
  - Card title: an `h3` inside `CardTitle` (check b). The link is named by the `h3` (`aria-labelledby`).
  - The search and the sort each sit in a `Field` with a visually hidden label, so the two line up in one row.
  - **Four existing tests changed**, consequences of the plan's `h1` («مساحات العمل» / "Workspaces") and of the
    page now reading the API: `SiteLayout.component.test.tsx` (a query wrapper and a fake empty directory;
    two headings `Spaces` → `Workspaces`), `authPages.component.test.tsx` and
    `changePasswordPage.component.test.tsx` (one heading each).
  - Order of work: the repository and `useDirectoryList` were written before their tests ran (their tests were
    written first but run after the code); the breaks below prove each. All other new tests were seen red first.
  - Files: 99 in the diff against `origin/main` (45 A, 45 M, 9 R), above the plan's ≈ 63.
- Red first: the four service unit files → `Cannot find module` (not written yet); `useDirectoryFilters` →
  `Failed to resolve import`. My own test defects fixed: the `DirectoryList` count (four records, not two); the
  first draft of test 24 (rewritten to move to page 2 by navigation).
- Green: `vitest run --project unit src/features/directory` → `Test Files  5 passed (5)` / `Tests  12 passed (12)`;
  `--project component src/features/directory src/pages/site` → `Test Files  10 passed (10)` / `Tests  58 passed (58)`.
- Breaks (`scripts\breaks5.py`, output `scripts\breaks5.out.txt`), each red, each restored:
  10 `relevance` accepted without `q` → `1 failed | 4 passed (5)`; 11 `page=1` written → `2 failed | 3 passed
  (5)`; 12 `searchOf` hands the text back → `1 failed | 4 passed (5)`; 13 shekels sent → `1 failed (1)`; 14 the
  query left out of `params` → `1 failed (1)`; 15 `FULL` → `destructive` → `1 failed | 1 passed (2)`; 16
  `now.getUTCDay()` → `1 failed | 2 passed (3)`; 18 the page kept → `1 failed | 3 passed (4)`; 19 written on each
  key → `1 failed | 3 passed (4)`; 20 not `loading` while pending → `2 failed | 5 passed (7)`; 21 the retry does
  not refetch → `1 failed | 6 passed (7)`; 22 `errors.server` for every failure → `1 failed | 6 passed (7)`; 23
  one state for both → `1 failed | 6 passed (7)`; 24 no `placeholderData` → `1 failed | 6 passed (7)`; 25
  `replacePage` left out → `1 failed | 6 passed (7)`; 26 `count.all` always → `1 failed | 6 passed (7)`; 27 the
  results' heading left out → `3 failed | 2 passed (5)`; 28 the effect on the first render too → `1 failed | 4
  passed (5)`; 29 no `error` handler → `1 failed | 4 passed (5)`; 30 «الأفضل تطابقًا» always → `1 failed | 4
  passed (5)`; 44 the route's title left out → `1 failed | 4 passed (5)`.
- Test 27's [width]: axe and the names at 390 and 1440 (`stubScreenWidth`); in 1a nothing reads the width, so
  the DOM is the same at both — the width rule that differs (the filters) is 1b's.
- `lint` exit 0; `typecheck` exit 0; `check:classes` → `No physical direction or arbitrary-value classes in 1107
  files.`; `check:links` → `2497 links in 197 documents and 1587 source files all resolve.`; Prettier clean.

## 4. On the head (`e01245a7`), once each

No `vitest` of `app-b` running before each lane (waited twice for worker B's short API runs to end, then 30 s
quiet). Free memory before each: unit 5,010,456 KB; component 4,979,552 KB.
- `npm run test:unit` → exit 0: `Tests  233 passed (233)` (shared), `Tests  797 passed (797)` (api),
  `Test Files  102 passed (102)` / `Tests  888 passed (888)` (web).
- `npm run test:component` → exit 1: `Test Files  1 failed | 192 passed (193)` / `Tests  1 failed | 1256 passed
  (1257)`, `Duration  445.80s`; the one failure is `pages/dashboard/routes.component.test.tsx` › "lists the
  owner's eleven pages" (finding 87) at `3076ms`. Alone (free 6,321,452 KB): `✓ … 2232ms`, `Tests  1 passed | 45
  skipped (46)`. **The owner's standing exception applies; CI's `test:component` is the judge.**
- The site's routes test (finding 55), focused run: "shows the Directory under its title" `1366ms`; the file's
  five tests `Tests  5 passed (5)`.
- `NODE_ENV=production npm run build` → exit 0 (`✓ built in 2.38s`); `npm run check:build` → `No showcase code
  in 45 build files (1030 strings checked).` / `No dashboard code in the site's first download.` / `No
  data-table or leaflet, nor Leaflet's stylesheet, in the site's first download.`; `check:classes` → `No
  physical direction or arbitrary-value classes in 1107 files.`; `format:check` → `All matched files use
  Prettier code style!`; `check:links` → `2497 links in 197 documents and 1587 source files all resolve.`;
  `lint`, `typecheck` exit 0.
- **The first download** (`scripts\firstDownload.mjs`, the manifest's entry and its static imports;
  `firstDownload-base.txt`, `firstDownload-head.txt`): base (`origin/main` `2c4d78f9`, built detached, then
  back on the branch) **978,177 bytes**, 6 chunks; head **985,147 bytes**, the same 6 chunks (entry 254,540 →
  254,767; CSS 81,807 → 82,897; `jsx-runtime` 113,313 → 117,413; `routing` 514,013 → 515,566). No public page's
  chunk, no `leaflet`, no `data-table`, no `dashboard`, no `directory` in it.
- **Finding 27, re-checked:** neither build has a chunk of its own for the space shell (`SpaceLayout`), and
  `useQuery` and `publicSpacePath` now have chunks of their own; but in **both** builds `PackagesPage` and
  `SettingsPage`'s chunks import the `dashboard` chunk and are imported back by it. The two-way import the
  finding describes persists (with other chunks, unchanged by this PR), so it is **not** resolved here — the
  owner's call (§14.10).
- Not run: `test:api` (no API or shared change; CI runs it).

## 5. The real run

Local headless Chrome over CDP (no `playwright` MCP tools in this session): `scripts\cdp.mjs` (OWNER_SETUP's
driver, shots path changed), `scripts\run1a.mjs`, `firstDownloadRun.mjs`, `breakShot.mjs`; outputs
`scripts\run-*.txt`; screenshots and network logs in `shots\pr1a\`. `docker start masaha-postgres-1`;
`migrate status` up to date; the API on 3320 (`npm run dev -w @masaha/api`), Vite on 5320 (`npx vite --port
5320 --strictPort` in `apps/web` — a first `npm run dev` from the root started a second API watcher instead,
which I stopped by its id, 10816), and `vite preview` on 5321 for the production build. No sign-in; reads only.

| Case | Result | Shots |
|---|---|---|
| The list, Arabic light and English dark at 390, 768, 1440 | 20 cards; «35 مساحة في قطاع غزة» / "35 spaces in the Gaza Strip"; the demo space's cover, the marks of the rest; «متاح» / "Available" on the demo space, «لا تتوفر حالة مباشرة» on the others; «موثّقة»; «اليوم 08:00–22:00», «مغلقة اليوم»; the area «الرمال · غزة» / "Al-Rimal · Gaza City"; one, two, three columns | `1a-list-{ar-light,en-dark}-{390,768,1440}.png` |
| A search by an English name in Arabic | `Palm` → `?q=Palm`, 3 cards, «3 مساحات مطابقة», the trigger «الترتيب: الأفضل تطابقًا» | `1a-search-english-name-*-1440.png` |
| A search of diacritics only | the address loses `q`, the field keeps the text, its line «اكتب حرفًا من اسم المساحة أو منطقتها»; the log has no 422 (no 4xx at all) | `1a-search-diacritics-*-1440.png`, `1a-search-*-log.txt` |
| No match and «مسح الفلاتر» | `zzzzqq` → «لا توجد مساحات تطابق ما اخترت» with «مسح الفلاتر»; after it, the address and the field empty, 20 cards | `1a-no-match-*-1440.png` |
| The sort | closed list «الأحدث تحديثًا \| حسب الاسم»; «حسب الاسم» → `?sort=name`; with a search «الأفضل تطابقًا \| الأحدث تحديثًا \| حسب الاسم», and choosing it leaves `?q=Hub` (the default unwritten) | `1a-sort-{open,name,best-match}-*-1440.png` |
| A reload and a copied link | the same list both ways (`reload same list: true`, `copied link same list: true`, a fresh browser for the link) | — |
| Page 2 | at 390 and 1440, both themes: 15 cards, the focus on `h2 "النتائج"` / `"Results"`, the section scrolled to; Back → page 1, the same 20 cards | `1a-page-2-*-{390,1440}.png` |
| The skip link | the first Tab reaches «تخطَّ إلى المحتوى» / "Skip to content", shown; Enter → `main#main`; after the header's «عن مساحة», the focus is on `main#main` of About, and back on the Directory too | `1a-skip-link-*-1440.png` |
| The first download (production build, `vite preview`) | 21 scripts and styles on opening `/spaces`: the entry, its five static imports, the site shell, `DirectoryPage` and its imports; no `leaflet`, no `dashboard`, no `data-table` | `1a-first-download-log.txt`, `1a-first-download-preview-ar-light-1440.png` |
| Width break: the results' columns removed once | at 1440 one column (`gridTemplateColumns 1216px`); restored → three (`394.656px 394.672px 394.656px`) | `break-results-columns.png`, `restored-results-columns.png` |

- The `spaces` chunk among the Directory page's imports is `@masaha/shared/spaces` (the price periods and the
  ceiling `filtersOf` reads; 4,289 bytes), not `features/spaces`.
- The dev server loads `pages/dashboard/routes.tsx` and a pre-bundled `@tanstack/react-table` when the app
  starts — unbundled development serving; the production build is what the case is judged on (above, and
  `check:build`).
- **Found and fixed in the run:** an English-only name's `h3` carried `dir="ltr"` itself, so it sat at the left
  of an Arabic card; `lang`/`dir` moved to a `span` inside the `h3` (the test asserts it there), folded into
  commit 5 (`git commit --fixup`, autosquash). The list shots were retaken after it.
- Not performed, by design: `FULL` and `CLOSED` (not in the data, never made through the app — `cardView.unit.
  test.ts` proves the roles), a cover that fails to load (`DirectoryList.component.test.tsx`, test 29). Every
  other PR 1a case was performed; the data held each (two pages: 35 spaces).
- **Data left in `masaha_dev`:** nothing changed — only `GET`s, no sign-in.
- Servers stopped by id (4808, 25236, 32820, 25548, 16272); `Get-NetTCPConnection -LocalPort 3320,5320,5321
  -State Listen` empty; no headless Chrome left.

## 6. After the run's fix

`SpaceCard.tsx` and its test changed after the lanes passed, so on `57b7cdb9`: `lint`, `typecheck`, `format:check`
(`All matched files use Prettier code style!`), the production build, `check:build` (the three lines as above),
`check:classes` (`… in 1107 files.`) again; no `app-b` vitest, free 5,457,476 KB; `npm run test:component` →
exit 0, `Test Files  193 passed (193)` / `Tests  1257 passed (1257)`, `Duration  393.12s` (finding 87's test
passed in the lane this time). The unit lane covers no changed file (not re-run).

## 7. Push and the PR

- Truth check before the push: two sentences of `directory.md` that spoke of later work («will hold the map…»,
  «the space's page will say which») reworded to what holds now, folded into commit 5; `check:links` → `2497
  links … all resolve.`
- `#PRNUM` → `#101` (the latest issue/PR was #100, no open PR): `git filter-branch` over the five commits,
  `refs/original` removed; `git grep -n "#PRNUM" HEAD` empty; `git diff origin/main --stat` the same before and
  after (`99 files changed, 2576 insertions(+), 81 deletions(-)`).
- Commits (subject length): `653acb80` refactor(space-links): share the list's pages (45) · `04281db4`
  refactor(spaces): share the name and clock rules (48) · `c28099de` feat(site): add a skip link and focus each
  page (47) · `d280c0db` feat(lookups): offer the public areas to the site (49) · `e50d9222` feat(directory):
  list the spaces page by page (45). No tool attribution (`grep` of the bodies: 0).
- `git push -u origin feat/directory-list`; `gh pr create` → **#101**
  https://github.com/Basel-Ghonaim/masaha/pull/101, labels `feat`, `area:web`, `area:docs`, `area:design-system`,
  title = commit 5's subject; the description carries decision 7's line for `DECISIONS_PUBLIC.md`.
- **S6 and the `area:design-system` label:** the prompt names S6 (the layer's barrel exporting `useMediaQuery`)
  as this PR's; in the plan it serves only the filters' sidebar and sheet (commit 6, PR 1b), so 1a leaves the
  barrel unchanged rather than export what nothing uses. The label stays, for foundation §5's status roles.

## 8. CI and where the work stands

- `gh pr checks 101` on head `e50d9222`: pass — `check:classes`, `check:links`, `lint`, `test:unit`, `typecheck`,
  `format:check`, `build`, CodeRabbit; **pending — `test:api`, `test:component`**. `mergeStateStatus`:
  `UNSTABLE` (the pending jobs).
- My background watch of the checks was stopped by Claude Code because the machine ran low on memory (not a
  failure of the watch); per that notice it was not restarted. **CI green and `CLEAN` are not yet seen** — the
  next step is one `gh pr checks 101` / `gh pr view 101 --json mergeStateStatus` once the two jobs end, then the
  `final-report` step. If `test:component` fails on finding 87's test there, the standing rule says stop.
- Conflict check: no other open PR (`gh pr list --state open` → 0), so no `merge-tree` was needed.
- `git status --short` clean; ports 3320/5320/5321 free; no server or headless Chrome of mine running.
- Later, after the owner said CI was green: `gh pr checks 101` (read, not re-run) shows all ten pass on
  `e50d9222`, and `mergeStateStatus` is `CLEAN`. The final report is at the top.
