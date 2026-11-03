# PUBLIC — PR 1b report (`feat/directory-filters`, the Directory's filters and near me)

Executor: Claude Code (Opus 5.5), 2026-10-21. Plan: `2_PLAN.md` with the owner's approval note (A13: this PR is
the plan's PR 1 commits 6–7), PR 1a's report (its split of commit 5), `0_CARRIED_FROM_101.md` (items 1–11).

## Final report (2026-10-21)

### 1. The pull request
**#103** https://github.com/Basel-Ghonaim/masaha/pull/103 — `feat(directory): filter by place, price and state`,
head **`52b7a2b0`** (`origin/feat/directory-filters` the same). CI: all ten checks pass on it (`build`,
`check:classes`, `check:links`, `format:check`, `lint`, `test:api`, `test:component` 15m31s, `test:unit`,
`typecheck`, CodeRabbit); `mergeStateStatus` **`CLEAN`**. Not merged. **DEMO_SEED was waived for this PR by the
owner (2026-10-21)**: the real run used the current `masaha_dev`.

### 2. The commits
| SHA | Subject (chars) |
|---|---|
| `dafc816c` | refactor(lists): share the page-in-range rule (45) — carried 6 |
| `50fe2c75` | fix(directory): keep the focus while searching (46) — carried 1, 8 |
| `3c837b30` | fix(directory): offer a retry after a limit (43) — carried 2, 10 |
| `21de283d` | fix(directory): drop a budget below its minimum (47) — carried 3 |
| `b82d213b` | fix(site): focus the page after signing in (42) — carried 5 |
| `52e31433` | fix(directory): read a card's details (37) — carried 7 |
| `ec0f4709` | fix(directory): say no count of zero (36) — carried 11 |
| `2fe598c5` | docs(findings): record a paged list's silent wait (49) — carried 9, finding 132 |
| `0c6a43ec` | feat(directory): filter by place, price and state (49) — the plan's commit 6 |
| `52b7a2b0` | feat(directory): sort the spaces nearest first (46) — the plan's commit 7 |

Carried item 4: checked, no change (true once commit 6 wires `AreaFilter`). 66 files against `origin/main`
(2,238 insertions, 125 deletions); `#PRNUM` → `#103` in each commit's tree.

### 3. What was run, and what was not
- Per commit: `lint`, `typecheck` (exit 0 each) and the touched test files.
- On the head, once each (§4, §8): web `test:unit` `Tests  897 passed (897)`; the component lane over the folders
  this PR touches `Tests  623 passed (623)` (run again after the real run's fix, the same count); production build;
  `check:build`, `check:classes` (1133 files), `format:check`, `check:links` (2499 links) — all green. The first
  download 985,147 → 989,912 bytes, the same six chunks, no `leaflet`/`data-table`/`dashboard`/`directory`.
- Not run locally (CI judges): the full `test:component` lane, `test:unit` of `apps/api` and `packages/shared`,
  `test:api` — all green on CI on `52b7a2b0`.
- The real run (§7): every case of §1.9 performed in Arabic light and English dark, widths as §3.4, with the
  privacy proof in the network log. Not performed in the browser: carried item 2 (the limit needs 1,200 guest
  requests) and item 5 (a sign-in writes a refresh token — data); their component tests prove them.
  `masaha_dev` unchanged.

### 4. Breaks and tests seen failing first
- Seen red first: every carried fix's test (items 1, 2, 3, 5, 7, 8, 11), `priceBounds`, `nearPoint`,
  `distanceText`, the repository's privacy half, `useNearMe`. Item 10's test (existing code) by its own break.
- Written after their code (departure), each proven by its planned break, red: tests 32, 33, 34, 35, 41, 42, 43
  and design issue 14's count.
- Own breaks for privacy, bounds and widths, each red then restored: rounding, accuracy, the point in the query,
  `toFixed`, ask on mount, the point in `localStorage`, the raw point on imprecise, `removeQueries` left out,
  accept 0, both drawn (35), the sheet at every width (43); and in the real run the sidebar's grid removed once
  (the sidebar full width above the results at 1440). Each red line in §3 and §7.

### 5. Problems met, and how each was solved
- The refresh-failure test first read the result before the render → `waitFor` (my test).
- The break helper failed on Windows' console code page → `python -X utf8`; shell quoting stripped quotes in two
  break specs → specs from JSON files.
- The filters button's name ran into the count's words («الفلاتر3 …») → a literal space, the codebase's idiom.
- «أخرى»'s chips are pressed buttons, not radios (my test).
- The tool turned `⁦` escapes into literal characters; a clean-up pass also rewrote PR 1a's
  `todayHours.unit.test.ts` → restored with `git restore` (its only diff was mine).
- Resetting the near-me store in `afterEach` re-rendered after `matchMedia` was unstubbed → reset in `beforeEach`.
- Real run: the «الفلاتر» button sat above the sort's control at 390/768 → `items-end`, folded into commit 6.
- The API started from the scripts folder failed (`ENOENT package.json`) → started from the repository.

### 6. What behaved unexpectedly
- A backgrounded command's `cd` did not take: the first API start ran in the scripts folder.
- `URLSearchParams` writes the areas' comma as `%2C` (`?area=2%2C3`, PR 1a's `paramsOf`); read back the same, and a
  pasted `?area=2,3` works. Not changed — for the review.
- Radix's Dialog trigger carries `aria-controls` only while the sheet is open (its `aria-expanded` always).
- Sorting by distance again within 30 s reuses the cached answer (one header request in the log, not two).
- The first download's `jsx-runtime` chunk grew 4,202 bytes: the catalogue's new words live in it.

### 7. The early conflict check
`gh pr list --state open` → #103 (this) and #102 (`feat/customers`, worker B, head `900eebb4`): `git merge-tree
--write-tree origin/feat/directory-filters origin/feat/customers` → exit 0, tree `4641b9f7`, **clean**.

### 8. Departures from the prompt and the plan
- **DEMO_SEED waived by the owner (2026-10-21)**; the run used the current `masaha_dev`, which held every case.
- Tests 32–35, 41–43 written after their code (each proven by its break).
- `useFiltersPanel` returns the whole filters view; the «₪» sign is a catalogue word; a period chosen before any
  bound is kept in the hook's state; one 400 ms pause over both bounds.
- `distances.*` words not added (a card shows a distance only while sorted, so the line would be false); with a
  point held but not sorting, only «مسح موقعي» and no privacy line. `sorted.pin` added so the line is total over
  `source`.
- Pressing «الأقرب إليّ» returns to page 1.
- Item 11: the Arabic zero form takes the counted line's words (the type needs six forms; never drawn).
- Finding 132 is item 9's (131 reserved). A test helper `src/test/fakeGeolocation.ts` (three test files use it).
- Carried items 2 and 5 not shown in the browser (no data change; their tests prove them).

---

## Earlier: where the work stood — STOPPED before the push (2026-10-21, superseded by the owner's decision, §6)

**Why:** the prompt's §1.8 — PR 1b's real run needs worker B's DEMO_SEED merged and seeded into `masaha_dev` by
the supervisor. **DEMO_SEED is not on `main`**: `origin/main` is still `befd96f9` (#101's merge); the only open PR
is worker B's #102 (`feat/customers`). So: no real run, no `#PRNUM` replacement, no push, no PR.

**Done, local only** on `feat/directory-filters` (10 commits on `origin/main` `befd96f9`, head `19f67a73`):
the eight carried commits (items 1–3, 5–11; item 4 checked), the plan's commits 6 and 7, every check on the head
green (§4). `git status --short` clean; no server running; ports 3320 and 5320 free.

**What the owner decides:**
1. **Wait for DEMO_SEED** (the approval note's (3)): once merged and seeded, the next run does §13's inventory
   again, the real run, `#PRNUM`, the push and the PR from this branch (rebased only if `main` moved).
2. **Or run on what `masaha_dev` already holds.** The read-only inventory (`scripts\inventory1b.mjs`, output
   `scripts\inventory1b.out.txt`) shows **every case the real run needs is already there**: 35 listed spaces;
   six areas with spaces (Al-Rimal 19, North Gaza Strip 9, An-Nasr 3, Al-Mawasi 2, Al-Tuffah 1, Tal al-Hawa 1);
   a day budget of 10–30 ₪ → 4 spaces; 7 verified, 28 unverified; one available (`masaha-demo`,
   `availableNow=true` → 1); `studentPrices=true` → 2; `openFriday=true` → 3; `sort=distance` from
   `31.5,34.46` answers distances (`offline-tiles-hub-66154=700`, …). `FULL`/`CLOSED`: none (not needed by 1b).

## Working log (written as the work went)

## 1. First checks (before any edit)

1. **The PR before:** `gh pr view 101 --json state,mergeCommit` → `MERGED befd96f966441fb3bab297cdc216f3bc832b707f`.
2. `git status --short` clean; `git switch main`; `git pull --ff-only` → `Already up to date.`; `origin/main`
   `befd96f9`.
3. **The base diff** `git diff --name-status e50d9222 origin/main` → empty (only #101's merge commit). No
   `packages/shared` change.
4. **Open PRs:** `gh pr list --state open` → none. (Worker B's DEMO_SEED is not on `main` yet: checked again
   before the real run, §1.8 of the prompt.)
5. **Checks against the code (commits 6–7):**
   - a. `useMediaQuery(query: string): boolean` in `shared/design-system/lib/useMediaQuery.ts`, internal (used
     by `DataTable` and `Sidebar`) — holds.
   - e. eslint's `LAYER_ONLY_IMPORTS` and `MAP_ONLY_IMPORTS` do not name `zustand`; `shared/session` and
     `shared/preferences` already use it — holds.
   - (b, c, d, f were PR 1a's and held or took their fallback there.)
6. **Finding numbers:** the index holds 1–113 and 130; 131 is reserved (the closure's notice) → a new one takes
   **132**.
7. `docker ps` → `masaha-postgres-1 Up … (healthy)`; `npx prisma migrate status` (in `apps/api`) → `21
   migrations found` / `Database schema is up to date!`.

## 2. Branch

`git switch --no-track -c feat/directory-filters origin/main` (at `befd96f9`).

## 3. Commits (carried from #101 first)

### Carried 1 — `dafc816c` `refactor(lists): share the page-in-range rule` (45) — item 6
- `git mv features/space-links/hooks/usePageInRange.ts shared/lists/hooks/usePageInRange.ts` (100 % rename),
  exported from `shared/lists/index.ts`; `useAdminSpacesList`, `useAdminUsersList` and `useDirectoryList` read it
  from `@shared/lists`; the inline copy in `useDirectoryList` is gone. `architecture.md` §1's zone table and the
  status line name the rule.
- A move, no new test: `lint` exit 0; `typecheck` exit 0; `vitest run --project component src/features/space-links
  src/features/directory` → `Test Files  25 passed (25)` / `Tests  172 passed (172)`.

### Carried 2 — `6327f53a` `fix(directory): keep the focus while searching` (46) — items 1, 8
- `DirectoryResults`: the focus moves to the results' heading only when the page changed under a **push**
  (`useNavigationType() === NavigationType.Push`; the pages are links); a search, an order or a page past the
  last (replace) leave it. `useDirectoryList`: the count is worded from a real answer only (React's
  set-state-during-render pattern, as `usePausedSearch`); while the answer is a placeholder it keeps its last
  line. `directory.md`: the behaviour paragraph, *Web history*.
- Tests written first, red: `Tests  3 failed | 12 passed (15)` — "leaves the focus in the search when a search
  typed on page 2 brings the first page back" (`Expected element with focus:` the search, received the heading);
  "moves nothing when a pasted page past the last is replaced by the last" (`Received element is focused`);
  "keeps the last count while the next answer loads…" (`expected '21 مساحة مطابقة' to be '21 مساحة في قطاع
  غزة'`). Each red step is the test's break (§3.1).
- Green: `vitest run --project component src/features/directory` → `Test Files  3 passed (3)` / `Tests  19
  passed (19)`. `lint` exit 0 (after comparing with `NavigationType.Push`, not the string — lint's
  `no-unsafe-enum-comparison`); `typecheck` exit 0; Prettier clean.

### Carried 3 — `9695810d` `fix(directory): offer a retry after a limit` (43) — items 2, 10
- `useDirectoryList`'s `failureOf` builds the failure whenever there is an error; once a rate limit's count has
  ended (the refusal's view gone) its line is `errors.rate_limit` and the retry is offered again, as the admin's
  spaces list keeps it. `directory.md`: the behaviour paragraph, *Web history*.
- Test (item 2), written first, red: `Tests  1 failed | 9 passed (10)` — "after too many requests, waits out the
  count, then offers «إعادة المحاولة» again" (`expected undefined to be 'تعذّر تحميل المساحات'`); green after.
- Test (item 10), "a failed refresh keeps the cards and says so, and «إعادة المحاولة» asks again": existing code,
  so its own break — `refreshFailure: null && failureOf(` → `Tests  1 failed | 9 passed (10)` (`expected null
  not to be null`), restored. (Its first draft read the result without waiting for the render: my test's
  defect, fixed with a `waitFor`.)
- Green: `vitest run --project component src/features/directory` → `Test Files  3 passed (3)` / `Tests  21
  passed (21)`; `lint` exit 0; `typecheck` exit 0; Prettier clean.

### Carried 4 — `892f0443` `fix(directory): drop a budget below its minimum` (47) — item 3
- `filtersOf` leaves `max` out when it is under `min` (the minimum kept; equal bounds kept). Test 10 gains
  `min=50&max=10` (→ `max: undefined`) and `min=10&max=10`. `directory.md`: S5's line, *Web history*.
- Red first: `Tests  1 failed | 4 passed (5)` ("falls back to the default for each value the server would
  refuse": `expected { … } to match object { min: 50, max: undefined }`); green: `vitest run --project unit
  src/features/directory` → `Test Files  5 passed (5)` / `Tests  12 passed (12)`. Commit 6's `priceBounds`
  applies the same rule in the fields; `filtersOf` keeps it for the address (the case stays proven here).
- `lint` exit 0; `typecheck` exit 0; Prettier clean.

### Carried 5 — `b7e78bf4` `fix(site): focus the page after signing in` (42) — item 5
- `useMainFocus`: on mount, `placed` is the path only when the navigation type is `Pop` (a first load or a
  reload); after a push or a replace (as `RequireGuest`'s landing once signed in) it starts empty, so the new
  shell's first page takes the focus. Finding 130 gains a dated line (`#PRNUM`) for the focus shell's own lack;
  `architecture.md` §2's shell sentence names the arrival from the focus shell.
- Test in `authPages.component.test.tsx`, written first, red: "moves the focus to the site's main content once
  signed in, the sign-in button gone" → `Tests  1 failed | 11 passed (12)` (`Expected element with focus:` main);
  green: `vitest run --project component src/pages/site` → `Test Files  7 passed (7)` / `Tests  43 passed (43)`
  (the shell's own first-load and search-only cases still pass).
- `lint` exit 0; `typecheck` exit 0; Prettier clean.

### Carried 6 — `980d77b8` `fix(directory): read a card's details` (37) — item 7
- `SpaceCard`: the link keeps `aria-labelledby` (the name) and gains `aria-describedby` naming each detail in
  turn — the area, the status (`LiveStatusBadge` takes an `id`), «موثّقة» and today's hours when drawn. One id
  per detail, because a single block's flat text ran two inline details into one word («متاحموثّقة», seen in
  the first draft's red output). Test 27 asserts the description (`toHaveAccessibleDescription('الرمال · غزة
  متاح موثّقة')`). `directory.md`: the card's sentence, *Web history*.
- Red first: `Tests  2 failed | 5 passed (7)` (test 27 at 390 and 1440: `Expected element to have accessible
  description` … `Received:` empty); green: `Test Files  3 passed (3)` / `Tests  21 passed (21)`.
- `lint` exit 0; `typecheck` exit 0; Prettier clean.

### Carried 7 — `e5450dc4` `fix(directory): say no count of zero` (36) — item 11
- `useDirectoryList`: a real answer of 0 records words the count `''` (the empty directory's or no match's own
  state says it). The two Arabic zero lines («لا توجد مساحات في قطاع غزة بعد», «لا توجد مساحات مطابقة») leave
  the catalogue; `ArabicPlural` requires all six forms, so `zero` takes the counted line's words («{n} مساحة …»,
  never drawn), the pattern §9 uses for `show(n)`. English has no zero form. `directory.md`, *Web history*.
- Red first: `Tests  1 failed | 9 passed (10)` (`expected 'لا توجد مساحات في قطاع غزة بعد' to be ''`); green:
  `Test Files  3 passed (3)` / `Tests  21 passed (21)`; `vitest run --project unit src/shared/copy` → `Tests  33
  passed (33)` (the catalogues' parity).
- `lint` exit 0; `typecheck` exit 0; Prettier clean (after `--write` on `useDirectoryList.ts`).

### Carried 8 — `ef54005e` `docs(findings): record a paged list's silent wait` (49) — item 9
- **Finding 132** (Open): every paged list (the Directory; the admin's spaces, owners and users lists) shows the
  next page's wait by `aria-busy` only, `ListPagination` marking the old page current; *Resolves when* the design
  gives a paged list a quiet loading sign, taken from `shared/lists` — the owner's call. Index line added.
  `check:links` → `2498 links in 198 documents and 1587 source files all resolve.`

### Item 4 (a check, no change)
`lookups.md`'s lines 18 and 104 are made true by commit 6's wiring (the page sets `AreaFilter` in the
`placeFilter` slot) — checked against commit 6's code, below.
Checked after commit 6: line 18 («on the site's Directory, through its page, the area filter and a card's area
name») and line 104 («filters by `lookups`' `AreaFilter` … both set by the page») now hold — `DirectoryPage`
sets `AreaFilter` in the list's `placeFilter` slot. **No change needed.**

### Commit 6 — `a8a35844` `feat(directory): filter by place, price and state` (49)
- `shared/design-system/index.ts` exports `useMediaQuery` (S6); foundation §3 (the tree and a *Width* rule).
  `services/priceBounds.ts` (`MAX_SHEKELS` moved here, `filtersOf` imports it); `hooks/filters/usePriceFilter.ts`,
  `useFiltersPanel.ts`; `types/FiltersView.ts`; `useDirectoryFilters` gains `applied` (filters in force, design
  issue 14) and `clearFilters` (keeps the search and the order); `useDirectoryList` returns `filters`;
  `DirectorySlots.placeFilter`; components `filters/FiltersForm`, `PriceFilter`, `FiltersSidebar`, `FiltersSheet`;
  `DirectoryList`'s layout (the sheet's button beside the sort below 1024 px; from 1024 px `lg:grid
  lg:grid-cols-12`, the sidebar `lg:col-span-3`, the results `lg:col-span-9`); `DirectoryPage` sets `AreaFilter`;
  `directory.filters` in both catalogues. Docs: `directory.md` (header, what it does, how it composes, «The
  directory's filters on the web», six *Web decisions*, S7's line, code map, *Web history*), `overview.md`'s
  *Built* line (filters).
- **Shape departures (small):** `useFiltersPanel` returns the whole `FiltersView` (the place, the price, the
  switches, «أخرى», the sheet, the sidebar), not only the plan's `{ wide, sheet, sidebar }`, so `useDirectoryList`
  stays one hook calling it once; the shekel sign is a catalogue word (`filters.currency`, «₪»), so the field
  holds no hard-coded text; `usePriceFilter` keeps a period chosen before any bound in its own state (the
  address writes a period only with a bound, S5) and writes both bounds after one 400 ms pause (one timer
  over both fields, so a minimum changed under a typed maximum re-applies it).
- **Red first:** `priceBounds.unit.test.ts` (test 31) → `Error: Cannot find module './priceBounds'` (`Test
  Files  1 failed`); its bound break (accept 0: `typed < 1` → `typed < 0`) → `Tests  1 failed | 2 passed (3)`
  (`expected { min: +0 } to deeply equal { minError: 'invalid' }`).
- **Written after their code (departure; each proven by its break, red):**
  - test 32 `usePriceFilter.component.test.tsx` — break "apply an invalid bound" (the raw text written) →
    `Tests  1 failed | 1 passed (2)` (`expected '?period=DAY&min=10&max=NaN' to be '?period=DAY&min=10'`);
  - test 33 (390, 768) — break "a plain `Button` with `onClick`" → `Tests  2 failed | 6 skipped (8)`
    (`toHaveAttribute("aria-expanded", "false")`);
  - test 34 — break «عرض {n} نتيجة» → `Tests  4 failed | 1 passed | 3 skipped (8)` (`Unable to find … "عرض
    المساحتين"`, «عرض 12 مساحة», «عرض 3 مساحات», «عرض المساحة»);
  - test 35 [width] — break "both drawn" → `Tests  1 failed | 7 skipped (8)` (`not.toBeInTheDocument()`);
  - design issue 14 (`useDirectoryFilters`: "counts the filters in force, not their values…") — break "each
    area counted" → `Tests  1 failed | 4 passed (5)` (`expected 6 to be 4`).
- My test's defects fixed on the way: the button's name ran «الفلاتر» into the count's words → a literal space
  in `FiltersSheet` (the codebase's idiom, `AmenityChecklist`); «أخرى»'s chips are pressed buttons, not radios.
- Green: `vitest run --project component src/features/directory src/features/lookups src/pages/site` → `Test
  Files  38 passed (38)` / `Tests  213 passed (213)`; `--project unit src/features/directory src/shared/copy` →
  `Test Files  8 passed (8)` / `Tests  48 passed (48)`. `lint` exit 0; `typecheck` exit 0; Prettier clean;
  `check:classes` → `No physical direction or arbitrary-value classes in 1118 files.`; `check:links` → `2498
  links in 198 documents and 1598 source files all resolve.`

### Commit 7 — `19f67a73` `feat(directory): sort the spaces nearest first` (46)
- `types/NearState.ts`, `LocationStatusView.ts`; `services/nearPoint.ts` (`MAX_ACCURACY_METRES`, `roundedPoint`,
  `judgePosition`, `nearHeader`), `distanceText.ts`, `focusFilters.ts` (the sidebar's and the form's ids, and
  «اختر منطقتك»'s scroll and focus); `hooks/near/nearMeStore.ts` (Zustand, module-level, never persisted),
  `useNearMe.ts`, `useLocationStatus.ts`; the repository's `near` argument and the `Masaha-Near` header (PR 1a's
  split); keys `list(request, near)` and `hasNear`; `requestOf(…, { byDistance })` (`sort=distance`, no `lang`);
  `useDirectoryQuery(request, near)`; `useDirectoryList` (the distance order, «حسب المسافة» shown and chosen,
  another order stops it; the button's press returns to page 1; `near.button`, `near.status`); the card's
  distance (`cardView`, `SpaceCard`, described too); `NearMeButton`, `LocationStatus`; `directory.near`,
  `card.distance`, `sort.options.distance` in both catalogues; a test helper `src/test/fakeGeolocation.ts` (the
  browser's seam, used by three test files). Docs: `directory.md` (header, what it does, how it composes, «Near
  me on the web», five *Web decisions*, code map, *Web history*), `architecture.md` §3 › *Where state lives*,
  `overview.md` (near me).
- **Departures:** the words `distances.device` / `distances.pin` are not added: on the Directory a card shows a
  distance only while the list is ordered by distance (the server sends `distanceMeters` only then), so «المسافات
  من موقعك.» would be false once the order stops; while the point is kept but not sorting, the state line shows
  «مسح موقعي» alone and no privacy line (nothing is sent). `sorted.pin` is added so the line is total over
  `source` (the type has `pin`, PR 2 sets it). The press returns to page 1 when past it (a change of order, as
  the sort's).
- **Red first:** `nearPoint.unit.test.ts` (36), `distanceText.unit.test.ts` (17) → `Cannot find module`; the
  repository's privacy half of 14 → `Tests  1 failed | 15 passed (16)` (`expected undefined to be
  '31.521,34.453'`); `useNearMe.component.test.tsx` (37–40) → `Failed to resolve import "./nearMeStore"`.
- **Breaks (privacy, bounds, state — their own, red, restored):** 36 no rounding → `Tests  2 failed | 1 passed
  (3)` (`expected { lat: 31.5214497, lng: 34.4525501 } to deeply equal { lat: 31.521, lng: 34.453 }`); 36 the
  accuracy check left out → `Tests  1 failed | 2 passed (3)`; 14 the point added to `params` → `Tests  1 failed
  | 1 passed (2)`; 17 `toFixed(1)` → `Tests  1 failed (1)` (`expected '1.0' to be '1'`); 37 ask on mount →
  `Tests  4 failed (4)`; 38 the point written to `localStorage` → `Tests  1 failed | 3 passed (4)` (`expected
  '{"lat":31.501,"lng":34.467}' not to match /31\.50|34\.46/`); 39 the raw point kept on imprecise → `Tests  1
  failed | 3 passed (4)`; 40 `removeQueries` left out → `Tests  1 failed | 3 passed (4)`.
- **Written after their code (departure; proven by their breaks):** 41 (`useDirectoryList`) — `sort=distance`
  left out → `Tests  1 failed | 10 passed (11)` (`expected null to be 'على بعد ⁦0.7⁩ كم'`); 42 — the
  privacy line in `denied` → `Tests  1 failed | 2 passed (3)`; 43 — the fallback left out → `Tests  2 failed | 1
  passed (3)`; 43 [width] — the sheet opened at every width → `Tests  1 failed | 2 passed (3)` (`toHaveFocus()`).
  `requestOf`'s distance case was added with its code.
- On the way: the tool turned my `⁦` escapes into literal characters, and a clean-up pass also rewrote
  `todayHours.unit.test.ts` (PR 1a's, outside this change) — restored with `git restore` (its only diff was
  mine); the store reset moved to `beforeEach` (reset in `afterEach`, it re-rendered after `matchMedia` was
  unstubbed: an unhandled `window.matchMedia is not a function`).
- Green: `vitest run --project component src/features/directory src/features/lookups src/pages/site` → `Test
  Files  40 passed (40)` / `Tests  221 passed (221)`; `--project unit src/features/directory src/shared/copy` →
  `Test Files  10 passed (10)` / `Tests  54 passed (54)`; `lint` exit 0; `typecheck` exit 0; Prettier clean;
  `check:classes` → `… in 1133 files.`; `check:links` → `2499 links in 198 documents and 1613 source files all
  resolve.`

## 4. On the head (`19f67a73`), once each

No `node` of `C:\dev\masaha\app-b\` running before each lane (`Get-CimInstance … -match 'app-b'` → 0). Free memory
before each: unit 4,658,412 KB; component 4,595,048 KB.
- `npm run test:unit -w @masaha/web` → exit 0: `Test Files  105 passed (105)` / `Tests  897 passed (897)`
  (`scripts\lane1b-unit.txt`).
- `npm run test:component -w @masaha/web -- src/features/directory src/features/lookups src/features/space-links
  src/pages/site src/shared/lists src/shared/design-system` → exit 0: `Test Files  100 passed (100)` / `Tests  623
  passed (623)`, `Duration  181.16s` (`scripts\lane1b-component.txt`). The folders the PR touches; `src/test/`
  (one new helper, no test of its own) and `shared/copy` (unit lane) add none.
- `$env:NODE_ENV='production'; npm run build` → exit 0 (`✓ built in 1.65s`); `npm run check:build` → exit 0: `No
  showcase code in 46 build files (1028 strings checked).` / `No dashboard code in the site's first download.` /
  `No data-table or leaflet, nor Leaflet's stylesheet, in the site's first download.`
- `check:classes` → `No physical direction or arbitrary-value classes in 1133 files.`; `format:check` → `All
  matched files use Prettier code style!`; `check:links` → `2499 links in 198 documents and 1613 source files all
  resolve.`
- **The first download** (`scripts\firstDownload.mjs`; `firstDownload-1b-head.txt`): base = PR 1a's head record
  (`firstDownload-head.txt`, the same tree: `git diff e50d9222 origin/main` is empty) **985,147 bytes**, 6 chunks;
  head **989,912 bytes**, the same 6 chunks (entry 254,767 → 254,854; CSS 82,897 → 82,962; `jsx-runtime` 117,413 →
  121,615, the catalogue's new words; `routing` 515,566 → 515,977). No `leaflet`, `data-table`, `dashboard`,
  `directory`, `DirectoryPage` or `HomePage` in it.
- **Not run locally (CI judges):** the full `test:component` lane, `test:unit` of `apps/api` and
  `packages/shared`, `test:api`.

## 5. The data check and the stop

- `git fetch origin`; `git log origin/main` → `befd96f9` still the latest (#101's merge); `gh pr list --state all`
  → #102 OPEN (`feat/customers`, worker B), no DEMO_SEED PR merged. **§1.8's condition holds: stop before the
  push.**
- The inventory, read-only (the API on 3320 from `npm run dev -w @masaha/api`; plain `GET`s, no sign-in):
  `scripts\inventory1b.mjs` → `scripts\inventory1b.out.txt` (figures in the summary at the top). The API then
  stopped by process id (15256, 27972, 11588); `Get-NetTCPConnection -LocalPort 3320,5320 -State Listen` → none.
- **The real run: NOT PERFORMED** — stopped by §1.8 before it (no screenshot taken; `shots\pr1b\` not created).
- **The early conflict check:** `git merge-tree --write-tree HEAD origin/feat/customers` (#102) → exit 0, a tree,
  no conflict (it shares only documents and `shared/copy/*/errors.ts`, which this branch does not touch; the
  findings index gains lines on both sides).
- **Data left in `masaha_dev`:** nothing changed (GETs only).

## 6. The owner's decision (2026-10-21)

**DEMO_SEED waived for this PR by the owner (2026-10-21):** the real run uses what `masaha_dev` holds (the
inventory of §5 shows every case 1b needs). The work continues from the prompt's §1.9: the real run, `#PRNUM`,
the push, the PR, CI green and `CLEAN`, the conflict check against #102. No data is changed.

## 7. The real run (on the current `masaha_dev`, DEMO_SEED waived)

Local headless Chrome over CDP (no `playwright` MCP tools in this session): `scripts\cdp1b.mjs` (PR 1a's driver,
shots path `shots\pr1b`), `scripts\run1b.mjs` (cases `layout`, `grid`, `place`, `budget`, `switches`, `near`,
`carried`), `breakShot1b.mjs`; outputs `scripts\run1b-*.txt`; screenshots and network logs in `shots\pr1b\`. The
API on 3320 (`npm run dev -w @masaha/api`; a first start from the scripts folder failed with `ENOENT
package.json` — restarted from the repository), Vite on 5320 (`npx vite --port 5320 --strictPort` in
`apps/web`). No sign-in; reads only. Near me through CDP: `Browser.setPermission` (`geolocation`, granted or
denied, origin `http://localhost:5320`) and `Emulation.setGeolocationOverride`.

| Case | Result | Shots |
|---|---|---|
| The filters' sheet at 390 and 768, both languages (`?verified=1&students=1`) | the button «الفلاتر 2» / "Filters 2", its name «الفلاتر فلتران مطبّقان» / "Filters 2 filters applied", `aria-expanded` false → true; no sidebar; the sheet titled «الفلاتر», its primary «عرض المساحة» / "Show 1 space", then «مسح الفلاتر» | `1b-filters-{ar-light,en-dark}-{390,768}-{closed,sheet}.png` |
| The sidebar at 1440, both languages | an aside named «الفلاتر» / "Filters", no Filters button, the results three columns of 291 px beside it; a card's description read after its name: «الرمال · غزة \| متاح \| موثّقة \| اليوم 08:00–22:00» (item 7) | `1b-filters-{ar-light,en-dark}-1440.png` |
| The results' grid, the whole list, both languages at 390 / 768 / 1440 | 20 cards; one column (358 px), two (336.5 px), three beside the sidebar (291 px) | `1b-grid-*.png` |
| The place filter (Arabic 390 in the sheet, English 1440 in the sidebar) | الرمال and النصر chosen → the summary «منطقتان محددتان» / "2 areas chosen", `?area=2%2C3`, «22 مساحة مطابقة» (19 + 3), the sheet's «عرض 22 مساحة» | `1b-place-open-*.png`, `1b-place-*.png` |
| The budget, a day from 10 to 30 ₪ | `?period=DAY&min=10&max=30`, «4 مساحات مطابقة» / "4 matching spaces"; the help line «يُطبَّق «من» و«إلى» على سعر اليوم» | `1b-budget-*.png`, `1b-budget-*-log.txt` |
| An inverted range (30, then 10) | the maximum's line «أقل من الحد الأدنى» / "Below the minimum", the address `?period=DAY&min=30` (no `max`, no 422), the sheet's «لا نتائج — غيّر الفلاتر» | `1b-budget-inverted-*.png` |
| Each switch and «أخرى» | `?available=1` → 1 («عرض المساحة»); `?verified=1` → 7 («عرض 7 مساحات»); `?students=1` → 2 («عرض المساحتين»); `?friday=1` → 3 («عرض 3 مساحات»); each switch `aria-checked`, each chip `aria-pressed` | `1b-{available,verified,students,friday}-*.png` |
| Near me granted (31.5017, 34.4668 at 30 m) | the button pressed; «مرتبة حسب المسافة من موقعك. المسافات تقريبية بخط مستقيم.» with the privacy line; the sort «الترتيب: حسب المسافة»; cards «على بعد 0.7 كم», «على بعد 0.9 كم», «على بعد 1.2 كم» / "0.7 km away"; «إيقاف الترتيب حسب المسافة» → the order «الأحدث تحديثًا», «مسح موقعي» alone, no privacy line; pressed again → sorted (no new ask); «مسح موقعي» → no line | `1b-near-{granted,stopped,cleared}-*.png` |
| Near me denied | «تعذّر تحديد موقعك» / «اختر منطقتك لتصفّح مساحاتها.» with «اختر منطقتك», no privacy line; «اختر منطقتك» → the place filter focused: in the sheet at 390, in the sidebar at 1440 | `1b-near-denied-*.png`, `1b-near-choose-area-*.png` |
| Near me imprecise (5,000 m) and out of the Strip (Cairo, 20 m) | «تعذّر تحديد موقعك بدقة» / «يبدو أن موقعك خارج قطاع غزة، أو أن هامش الخطأ فيه أكبر من 2 كم، فلم نستخدمه.»; no privacy line; no request with the header | `1b-near-{imprecise,outside}-*.png` |
| **The privacy proof in the network log** | Arabic 390: 20 API requests, **1 with `Masaha-Near`, on `/spaces?limit=20&sort=distance`, value `31.502,34.467`** (three decimals); English 1440: 19 requests, the same. **No coordinate in any URL; no header without `sort=distance`; none with more than three decimals; after «مسح موقعي», 3 and 2 requests, none with the header** | `1b-near-*-log.txt` |
| Carried 1: a search typed on page 2 | `?page=2` → «Hub» typed → `?q=Hub`, the focus still in the search field (`INPUT type=search`, value «Hub»), «26 مساحة مطابقة» | `1b-carried-search-focus-*.png` |
| **Width break:** the sidebar's grid (`lg:grid lg:grid-cols-12 lg:items-start lg:gap-6`) removed once | at 1440 the sidebar full width (1216 px) above the results (y 970); restored → the sidebar 286 px beside the results 906 px | `break-filters-beside-results.png`, `restored-filters-beside-results.png` |

- **Found and fixed in the run:** at 390 and 768 the «الفلاتر» button sat a few pixels above the sort's control
  (the sort's `Field` keeps its visually hidden label's gap) → the row `flex items-end gap-3`; folded into commit 6
  (`--fixup`, autosquash → `b5d38340`; commit 7 → `565fc879`); the layout shots retaken after it.
- **Not performed in the browser:** carried item 2 (the rate limit takes 1,200 guest requests in a window — not
  a reading of the page; `useDirectoryList` test "after too many requests…" proves it) and carried item 5 (a
  sign-in writes a `RefreshToken` row: it would change data; `authPages` test "moves the focus to the site's
  main content once signed in" proves it). `FULL`/`CLOSED`: not in the data, not needed by 1b.
- Observation (not changed, PR 1a's `paramsOf`): `URLSearchParams` writes the areas' comma as `%2C`
  (`?area=2%2C3`); read back the same, and a pasted `?area=2,3` works too.
- **Data left in `masaha_dev`:** nothing changed — only `GET`s, no sign-in.
- Servers stopped by id (33344, 4664, 13652, 24200); `Get-NetTCPConnection -LocalPort 3320,5320 -State Listen` →
  none; no headless Chrome left.

## 8. After the run's fix, `#PRNUM`, the push and the PR

- The fix folded: `git commit --fixup a8a35844`, `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash origin/main`. On
  the new head: `lint`, `typecheck` exit 0; the component lane (the same folders) → `Test Files  100 passed
  (100)` / `Tests  623 passed (623)`, `Duration  215.75s` (no `app-b` node; free 2,226,896 KB); the production
  build exit 0; `check:build` its three lines; the first download 989,912 bytes, unchanged; `check:classes` →
  `… in 1133 files.`; `format:check` → clean. The unit lane covers no changed file (not re-run).
- `#PRNUM` → `#103` (the latest issue/PR was #102, checked again right before `gh pr create`): `git
  filter-branch` over the ten commits, `refs/original` removed; `git grep -n "#PRNUM" HEAD` → 0; `git diff
  origin/main --stat` the same before and after (`66 files changed, 2238 insertions(+), 125 deletions(-)`); no CR
  in the docs' diff; no tool attribution in the bodies (0).
- Commits (subject length): `dafc816c` refactor(lists): share the page-in-range rule (45) · `50fe2c75`
  fix(directory): keep the focus while searching (46) · `3c837b30` fix(directory): offer a retry after a limit
  (43) · `21de283d` fix(directory): drop a budget below its minimum (47) · `b82d213b` fix(site): focus the page
  after signing in (42) · `52e31433` fix(directory): read a card's details (37) · `ec0f4709` fix(directory): say
  no count of zero (36) · `2fe598c5` docs(findings): record a paged list's silent wait (49) · `0c6a43ec`
  feat(directory): filter by place, price and state (49) · `52b7a2b0` feat(directory): sort the spaces nearest
  first (46).
- `git push -u origin feat/directory-filters`; `gh pr create` → **#103**
  https://github.com/Basel-Ghonaim/masaha/pull/103, labels `feat`, `area:web`, `area:docs`, `area:design-system`,
  title = commit 6's subject, the description with "Carried from #101" (`scripts\pr-body-1b.md`). Head `52b7a2b0`.
- **The conflict check:** `git merge-tree --write-tree origin/feat/directory-filters origin/feat/customers` (#102,
  head `900eebb4`) → exit 0, tree `4641b9f7`, no conflict.
