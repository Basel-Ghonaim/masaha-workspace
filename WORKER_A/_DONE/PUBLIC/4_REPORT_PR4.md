# PUBLIC PR 4 — execution report (`feat/home-about`, Home, About and the error states)

Executor: Claude Code (Opus 5.5), 2026-10-24. Written as the work goes.

## First checks

- `gh pr view 108 --json state` → `MERGED` at `dec7bd37db4b76871b8f00efa4c1a8375bce393b`.
- `gh pr list --state open` → none open.
- `C:\dev\masaha\app` on `main`, clean; `git pull --ff-only`; `HEAD` = `origin/main` = `dec7bd37`.
- `npm run build -w @masaha/shared` → exit 0.
- **Base diff** `git diff --name-status 88caa228 origin/main` (#108's reviewed head → main): worker B's #109
  (subscription check-ins): `apps/api/**`, `packages/shared/src/{core/errors,desk/responses,subscriptions/*}`,
  `apps/web/src/shared/copy/*/errors.ts`, docs (api-contract, data-model, findings 111/124/125 and the index,
  backend, features customers/desk/occupancy/payments/subscriptions, v1-mvp, overview). No code file this plan
  names for PR 4; `packages/shared`'s `directory`, `lookups`, `occupancy`, `spaces` responses unchanged.
- **Check 5k** (`ScrollRestoration` and the hash): `RootLayout.tsx` renders React Router 8's
  `<ScrollRestoration />`; proven in the real run (below).
- **Check 5l** (`foundation.md` §12 names the icon set's members): it does not (§12 is the component inventory;
  §8 states the mirroring rule only) → not edited.
- **Finding numbers:** the index's highest is 136; a new one takes 137 and on.
- **`PR 3b`'s report has no `Departures` section** (searched); its notes: the scoped component lane had 5
  failures in 3 files (unnamed), hidden-tab and map touch-scroll not exercised (item 8 here).
- Docker: `docker start masaha-postgres-1` → healthy. `npx prisma migrate status` (in `apps/api`) →
  `Database schema is up to date!` — nothing deployed.

## Data inventory (read-only, `scripts\inventory4.mjs`, output `scripts\inventory4.out.txt`)

API on 3320 (PID 1672 of the `npm` wrapper). Plain `GET`s only:
- 59 listed spaces; cards' live states: `AVAILABLE` 11, `CLOSED` 3, none 45; no `FULL` (not performed, by
  design).
- `availableNow=true&limit=6` → 6 cards (Home's «متاحة الآن» holds; its empty state is not producible with this
  data → proven by test 83).
- `sort=distance&limit=6` with `Masaha-Near: 31.515,34.450` → 6 cards with distances.
- `GET /map/spaces` → 59 pins, not truncated; pins carry `areaId`; 17 areas hold pins (area 2: 21, area 1: 11 …).
  (The script's "catalogue areas: 0" line is its own mistake: the catalogue nests areas under governorates.)
- Carried item 8: 3+ photos → `noor-hub` (3), `masaha-demo` (5); no space with 6+ photos (item 2 proven by its
  test); a page with the phone bar → `noor-hub`; a page without a bar → `white-space` (verified, email only).

## Branch

`git switch --no-track -c feat/home-about origin/main` (at `dec7bd37`).

## Carried from #108 — commits (shas before the final rebase; the push section gives the final ones)

| Item | Commit | Subject (chars) | Red before the code | Green after |
|---|---|---|---|---|
| 1 | `087e0f84` | `fix(directory): keep the status on a failed read` (48) | `× keeps the last live status when a later refresh fails` — `expected document not to contain element, found <p>تعذّر قراءة الحالة الآن</p>` | `SpaceDetails.component.test.tsx` `Tests 8 passed (8)` |
| 2 | `ad518212` | `fix(directory): count every photo in the viewer` (47) | `× counts every photo in the viewer’s position…` — `Unable to find an element with the text: 1 / 7` (it read `1 / 5`) | `Tests 1 passed \| 11 skipped (12)` |
| 3 | `0385cdaf` | `fix(directory): show one tile on a phone` (40) | `× with 2/3/5 photos, a phone shows the first tile alone` — `expect(element).toHaveClass("grid-cols-1")` | `Tests 12 passed (12)` |
| 4 | `834ecfa0` | `test(directory): drive the refresh by page events` (49) | test only (the code exists) | `Tests 1 passed (1)` |
| 6 | `b5a2eeff` | `fix(site): reserve the bar's room only with a bar` (49) | `× … a space with neither` — `expect(element).not.toHaveClass("pb-24")` (the pathname rule) | both cases pass (`routes.component.test.tsx` + `shell/`: `22 passed`, the 2 failures below excepted) |
| 7 | `ca5ff70e` | `test(map): prove the place map lets a phone scroll` (50) | test only (the code exists) | `PlaceMap.component.test.tsx` `Tests 2 passed (2)` |
| 5 | `b0fbef40` | `docs: say which live status stands for a closure` (48) | docs | — |

Item 1's first subject was 53 characters; amended to 48 before anything else. Item 1's test was reformatted
by Prettier, folded into its commit (`--fixup` + autosquash).

**Breaks:**
- Item 1, 2, 3, 6: the red step is the break (the old code; for item 6 the pathname rule).
- Item 4 (test 77): first, both breaks stayed **green** with the test as first rewritten — a defect of the
  test: it counted the requests synchronously right after `vi.advanceTimersByTime`, before a background
  poll's request could be sent, and `refetchOnWindowFocus` removed falls back to the app's default `true`,
  which refetches anyway once the 30 s `staleTime` has passed. Fixed in the test (`advanceTimersByTimeAsync`,
  and a second return at once while the status is still fresh). Then:
  - `refetchIntervalInBackground: true` → `AssertionError: expected [ '/spaces/noor-hub/occupancy', …(2) ] to have a length of 2 but got 3` (red).
  - `refetchOnWindowFocus` removed → `AssertionError: expected [ '/spaces/noor-hub/occupancy', …(2) ] to have a length of 4 but got 3` (red).
  - Restored; green.
- Item 7: `dragging` on → `expect(element).not.toHaveClass("leaflet-grab")` (red); `touchZoom` on →
  `expect(element).not.toHaveClass("leaflet-touch-zoom")` (red). Restored; green.

**Item 6's design:** `SiteLayout` keeps a `footerRoom` flag and offers `reserveFooterRoom` through its
outlet's context (`shell/footerRoom.ts`: `SiteOutletContext`, `useFooterRoom(reserved)`); `SpacePage` calls
`useFooterRoom(useSpaceContactBar(slug))` (`directory` exports `useSpaceContactBar`: the space has a WhatsApp
or a phone); `SiteFooter({ barRoom })` adds `pb-24 md:pb-0` only then.

Lint and typecheck: `npm run lint` exit 0 and `npm run typecheck` exit 0 after items 1, 2 and 6 (6 runs).

### A pre-existing local failure (not this PR's code)

`src/pages/site/routes.component.test.tsx` › **"shows the Directory under its title"** and
`src/pages/site/shell/SiteLayout.component.test.tsx` › **"marks the current page's link, and only it, as the
current page"** fail locally at their 3 s wait (`Unable to find role="main"` / `role="heading"`, 3027–3192 ms)
**on clean `HEAD` too** (`git stash`, same command: the same two failures, `Tests 2 failed | 20 passed (22)`).
Both wait on the Directory page's lazy chunk; with `--testTimeout=60000` and a 50 s wait (diagnostic only, not
kept) "shows the Directory" passes. Free memory 4,896,644 KB; one `app-b` node process (eslint). CI passed
both on #108. Recorded; see the head's lanes.

## The plan's PR 4 commits

(Shas before the final rebase. After a doc fixup folded into items 1 and 3 — `directory.md`'s live-status and
gallery lines — the carried shas changed; the push section gives the final list.)

| # | Commit | Subject (chars) | Red before the code | Green after | Break |
|---|---|---|---|---|---|
| 1 | `23b052e4` | `feat(routing): offer home and say a failed retry` (48) | test 80: `× offers the caller’s way on…` — `toHaveClass("lucide-wifi-off")`; `× retries once…` — `aria-busy`; `× says the problem is on our side…` — text not found | `src/shared/routing` `Tests 62 passed (62)`; `RetryState.component.test.tsx` `Tests 3 passed (3)` | reload anyway → `AssertionError: expected "vi.fn()" to not be called at all, but actually been called 1 times` (red) |
| 2 | `32bc0e39` | `feat(lookups): list the public areas for home` (45) | test 81: `Failed to resolve import "./usePublicAreas"` (module not written) | `Tests 3 passed (3)` | governorate left out → `AssertionError: expected [ …(3) ] to deeply equal [ …(3) ]` (red) |
| 3 | `6901cce7` | `feat(directory): offer home its spaces and counts` (49) | tests 82, 83: `Failed to resolve import "./useAreaCounts"` / `"./useHomeSpaces"` | `hooks/home` `Tests 4 passed (4)` | 82: count areas, not pins → `expected [ [ 2, 1 ], [ 7, 1 ] ] to deeply equal [ [ 2, 3 ], [ 7, 1 ] ]`; 83: `limit` left out → `expected [ { availableNow: true } ] to deeply equal [ { limit: 6, availableNow: true } ]` and `… [ { sort: 'distance' } ] …` (red) |

- Commit 1: the site's **three** boundaries use `SiteRouteError` (the plan says "two": `SiteLayout`'s and
  `FocusLayout`'s; `FocusLayout` has two routes — sign-in and the forced password change — each with its own
  boundary). The routes test's offline case now also checks «Try again» and «Home» in `main`.
  `foundation.md` §12 not edited (check 5l).
- Commit 2: `PublicArea` lives in `lookups/types/PublicArea.ts`, as the feature keeps its types.
- Commit 3: **`useHomeSpaces({ chooseArea, openMap })`** takes the two callbacks its state line needs (the
  plan's signature shows `useHomeSpaces()`; «اختر منطقتك» and «حدّد موقعي على الخريطة» must act) — a
  departure of interface only. The empty state while sorting by distance (an empty directory) uses the
  Directory's `empty` words with «تصفّح كل المساحات». The history line "carried from #108" sits in commit 3's
  `directory.md` (an earlier commit would conflict with commit 3's line beside it). Lint first flagged
  `no-unsafe-return` in the new tests (`request.params` is `any`); fixed before the commit.
- Lint and typecheck after commits 1, 2 and 3: exit 0 each.
| 4 | `833315e9` | `feat(site): build the home page` (31) | test 84: `Failed to resolve import "./useAreaCards"`; then my own test's mistake (`4 مساحة` for Arabic's *few*, `4 مساحات`), fixed in the test | `public/home` `Tests 2 passed (2)`; test 85's Home case `Tests 1 passed` | 84: areas with no space kept → `expected [ { key: '11', …(3) }, …(3) ] to deeply equal [ … …(2) ]`; 85: `q` not encoded → `AssertionError: expected '?q=Hub & Co' to be '?q=Hub%20%26%20Co'` (red) |
| 5 | `e78bbc99` | `feat(site): build the about page` (32) | tests 85 (About, footer) and 86 written after the code: their breaks stand for red | `Tests 2 passed \| 11 skipped (13)` | 86: a hard-coded email in About → `AssertionError: expected [ <a …(1)></a> ] to deeply equal []` (red) |

- Commit 4: `navigation.ts`' `OWNERS_ANCHOR` and `SITE_PATHS.owners` land in commit 4 (the plan puts them in
  commit 5), since the owners' card links there.
- Commit 5: About's legend uses `directory`'s exported `LiveStatusBadge` and a new exported `statusViewOf`
  (the live state → word and role rule, extracted from `cardViewOf`, so the rule keeps one home; the plan
  names only `LiveStatusBadge`). Design issue 41's note: the note's text, then a «تواصل معنا» link to
  `#contact`. The site's footer test in `SiteLayout.component.test.tsx` is unchanged; test 85 checks the first
  link.
- Lint and typecheck after commits 4 and 5: exit 0 each.
- **`origin/main` moved** meanwhile: worker B's #110 (`fix/subscriber-checkout-due`) merged at `8fc5939e`
  (API, `docs/api/api-contract.md`, findings 126–127 and the index, `docs/features/desk.md`).
  `git merge-tree --write-tree HEAD origin/main` → exit 0, no conflict. Branch: 53 files against its base.

## On the head (`c2c62afd`, before `#PRNUM`)

No `app-b` node process before each lane (count 0); free memory 4,433,468 KB (unit), 4,420,476 KB (scoped
component, first run), 4,821,076 KB (second run).
- `npm run test:unit -w @masaha/web` → exit 0, `Test Files 115 passed (115)`, `Tests 918 passed (918)`.
- `npm run test:component -w @masaha/web -- src/shared/routing src/shared/map src/shared/design-system
  src/features/directory src/features/lookups src/pages/site` — **first run exit 1**: `Test Files 1 failed |
  97 passed (98)`, `Tests 2 failed | 601 passed (603)`; failing: `src/pages/site/shell/SiteLayout.component.test.tsx`
  › "renders the header, the page in the main landmark, and the footer" and › "switches to the other language,
  and <html>'s lang and dir follow" — both expected the old placeholder's `h1` «Home»/«الرئيسية»; Home's `h1`
  is now «Find a workspace in the Gaza Strip». Fixed in that test (a file the plan's list does not name),
  folded into commit 4. **Second run exit 0**: `Test Files 98 passed (98)`, `Tests 603 passed (603)` — the
  two pre-existing timing failures recorded above did not recur (the shell's "marks the current page's link"
  and the routes' "shows the Directory" both passed). No other folder's files changed (`shared/copy` and
  `pages/showcase` have unit tests only, in the unit lane).
- `NODE_ENV=production npm run build` → exit 0.
- `npm run check:build` → exit 0: "No showcase code in 54 build files (1020 strings checked). No dashboard code
  in the site's first download. No data-table or leaflet, nor Leaflet's stylesheet, in the site's first
  download."
- `npm run check:classes` → exit 0: "No physical direction or arbitrary-value classes in 1234 files."
- `npm run format:check` → exit 0: "All matched files use Prettier code style!"
- `npm run check:links` → exit 0: "2628 links in 214 documents and 1765 source files all resolve."
- `npm run lint`, `npm run typecheck` → exit 0.
- **First download** (`scripts\firstDownload.mjs`): base `dec7bd37` 1,002,500 B in 7 chunks → head
  1,010,782 B in 6 chunks (+8,282 B: the routing states' icon and line, the site's boundary); no `leaflet`,
  `data-table`, `dashboard`, `directory`, `DirectoryPage` or `HomePage` in it (`firstDownload-4-base.txt`,
  `firstDownload-4-head.txt`).

**Not run locally (CI judges):** the full `test:component` lane, `test:unit` of `apps/api` and
`packages/shared`, `test:api`.

## The real run (local headless Chrome over CDP: `scripts\cdp4.mjs`, `run4.mjs`, `run4c.mjs`)

API on 3320 and web on 5320 from `C:\dev\masaha\app`, worker A's `masaha_dev`. `apps/web/.env` had no
`VITE_CONTACT_*`; `VITE_CONTACT_EMAIL=hello@example.com` added for the email-alone cases, then the file restored
from its backup for the no-contact cases (md5 `698e9fa2…` before and after; never committed). Shots in
`C:\dev\masaha\workspace\WORKER_A\PUBLIC\shots\pr4\` (42) and `shots\pr4\carried\` (17). No page error in any run.
Outputs: `scripts\run4-*.txt`, `run4c-*.txt`, the network log `run4-home-requests.json`.

**Layouts** (`run4-layouts.txt`): Home and About in Arabic light and English dark at 390, 768 and 1440 —
`4-home-{ar-light,en-dark}-{390,768,1440}.png`, `4-about-…` (12 full-page shots). Home: «متاحة الآن» with 6
cards, «تصفّح حسب المنطقة» with the 21 areas that hold spaces then «كل المناطق · قطاع غزة · 59 مساحة», the
owners' card; About: its four sections in order, «تواصل معنا» before «لأصحاب المساحات».

**PR 4 cases** (each in Arabic light at 390 and English dark at 1440):
- The hero's search, submitted by Enter (sent with its text) → `/spaces?q=%D9%86%D9%88%D8%B1` and
  `/spaces?q=Noor%20Hub` — `4-home-search-*`.
- «متاحة الآن»: 6 cards, «عرض الكل» → `/spaces?available=1` — `4-home-available-*`.
- Near me (`Browser.grantPermissions` + a point in Gaza City at 30 m): the heading «المساحات الأقرب إليك» /
  "Spaces nearest you", the state line with the privacy line, «على بعد 0.6 كم»; **the log:** one request
  `GET /api/v1/spaces?limit=6&sort=distance` with `Masaha-Near: 31.515,34.452` (three decimals), no URL holding a
  coordinate — `4-home-nearest-*`. «عرض الكل» → `/spaces`, its first six in Home's order (`same first six:
  true`) — `4-home-viewall-nearest-*`.
- «تصفّح حسب المنطقة»: `4-home-areas-*`; the first card → `/spaces?area=1`, «11 مساحة مطابقة» / "11 matching
  spaces" (its card said 11).
- The owners' card → `/about#owners`, scrolled (scrollY 1011 at 390, 739 at 1440: the page's end, the section
  being near it) — `4-home-owners-to-about-*`. **Check 5k holds:** `ScrollRestoration` scrolls to the hash
  arriving from another page; no effect added.
- The footer: «تصفّح المساحات» `/spaces` first, then «عن مساحة», «تواصل معنا» — `4-footer-*`; its «تواصل معنا»
  from `/spaces` → `/about#contact`, scrolled — `4-about-contact-from-footer-*`.
- About: the legend (متاح · ممتلئ · مغلق الآن · لا تتوفر حالة مباشرة, each with its line) — `4-about-legend-*`;
  the contact with the email alone: both `#contact` and `#owners` hold «بريد hello@example.com»
  `mailto:hello@example.com` — `4-about-contact-email-*`; with none: both sections keep their text and hold no
  link — `4-about-contact-none-*`; no university line in either.
- The offline state (`Network.emulateNetworkConditions` offline, `navigator.onLine` false, then the About link,
  whose code had not arrived): «لا يوجد اتصال بالإنترنت» with `lucide-wifi-off`, «إعادة المحاولة» and
  «الرئيسية» — `4-offline-*`; «إعادة المحاولة» while still offline: still on `/about`, «ما زال الاتصال
  مفقودًا.» / "Still no connection.", the button enabled — `4-offline-still-*`; «الرئيسية» → Home (its code had
  arrived), then back online, its 6 cards — `4-offline-home-again-*`. **Departure in the case's order:** the
  first try went online *before* pressing «الرئيسية»; the browser's `online` event reloads the page (by design,
  RouteErrorState), so the page became About before the link could be pressed. Recorded as a second case: offline
  on About, then online → reloaded into About («عن مساحة» / "About Masaha").
- **Not performed, by design:** the general error (needs a code change; test 80 and the routes test own it);
  Home's empty «لا توجد مساحات متاحة الآن» (the data has 11 available; test 83 owns it); `FULL` (no space
  holds it; never made through the app).

**Carried item 8 (#108's gaps)** — `shots\pr4\carried\`:
- The status kept while the tab is hidden, then refreshed on return (English dark 1440, `noor-hub`): a second
  tab (`Target.createTarget`) makes the page truly `hidden` (a probe, `probe4-hidden.mjs`, saw the real
  `visibilitychange` events); reads at 4 s; **none in 75 s hidden**; activated again → `visible` and a read at
  once (82 s); the badge kept — `4c-hidden-before-…`, `4c-hidden-after-return-…`.
- A finger over the place map at 390 (`noor-hub`, touch emulation): `Input.synthesizeScrollGesture` moved
  nothing — not even over plain text (a control: scrollY 0 → 0), so the tool does not drive scrolling here; with
  real touch events (`Input.dispatchTouchEvent`, a finger moving 200 px up over the map) the page scrolled
  **1622 → 1807** while the map's pane stayed `translate3d(0px, 0px, 0px)` — `4c-touch-*`.
- The page's bottom at 390: `noor-hub` with the bar — the footer's last link ends at 780, the bar starts at 835,
  the footer padded 96 px; `white-space` without a bar — padding 0, no band — `4c-bottom-with-bar-…`,
  `4c-bottom-no-bar-…`.
- The gallery (`masaha-demo`, 5 photos) at 390, 768, 1440 in both: one tile at 390, five from 768, the pill
  «عرض كل الصور (5)» / "View all photos (5)" — `4c-gallery-{ar-light,en-dark}-{390,768,1440}.png`.
- **Escape and the focus: the first run found the focus NOT back on the tile** (`document.activeElement` the
  body: the viewer has no trigger of its own, so Radix had nowhere to return it). **Fixed here, with a test:**
  `61e16baa fix(directory): return the focus to the photo tile` (50) — red first: `× hands the focus back to the
  tile that opened the viewer when Escape closes it` — `expect(element).toHaveFocus()`; green: `Tests 13 passed
  (13)`; the red step is its break. Re-run: «عرض الصورة 1» and "View photo 3" focused again after Escape —
  `4c-viewer-*`, `4c-viewer-closed-focus-*`. Placed among the carried commits (rebase).
- After that fix (the lanes had passed): the touched file (`SpaceDetails.component.test.tsx`, 13 passed),
  `lint`, `typecheck`, `format:check`, `check:links` re-run, each exit 0.

**Servers stopped by process id** (31220, 33532, 11600, 28196 and their npm wrappers); ports 3320 and 5320 not
listening; `git status --short` clean. **Data left in `masaha_dev`:** nothing (plain `GET`s only; no sign-in).

## Push and the PR

- Next number: `gh pr list --state all --limit 1` → 110 and the issues API → 110; expected **111**.
- `scripts\prnum4.sh 111` (adapted from `prnum3b.sh`: branch `feat/home-about`, backup
  `backup/home-about-pre-prnum`, its checks kept) → `PRNUM OK #111 daed4f5c (was 373e2029)`; `git grep "#PRNUM"`
  empty in every commit; `git diff --stat dec7bd37 HEAD` 54 files, as before.
- Pushed `feat/home-about`; `gh pr create … --label feat --label area:web --label area:docs --label
  area:design-system`, title `feat(site): build the home page` → **#111** (the number expected); head
  `daed4f5c384a3787a00516081e2dc701eed4f9ec`.
- Conflict check: no other open PR; `git merge-tree --write-tree origin/feat/home-about origin/main` (main at
  `8fc5939e`, with #110) → exit 0.

## CI

- **First head `daed4f5c`:** every check green but **`test:component` red**: `Test Files 1 failed | 210 passed
  (211)` — `src/app/App.component.test.tsx` › "starts, and still changes its language and theme, in a browser
  that blocks storage": `TestingLibraryElementError: Unable to find role="heading" and name "Home"` (it expected
  Home's old placeholder heading; `src/app` is outside the scoped lane). Fixed in that test (Home's `h1`
  «Find a workspace in the Gaza Strip»; the document title stays "Home · Masaha"), folded into commit 4;
  re-run: `src/app` `Test Files 4 passed (4)`, `Tests 9 passed (9)`; `lint` and `typecheck` exit 0. The
  "Invalid blocker state transition" lines in that log belong to tests that passed (their own scenario).
  Force-pushed (`--force-with-lease`); 55 files.
- **Final head `036335346cd16be9a719e9a4745d244b1549cc08`** (the run's `headSha` the same): `gh pr checks 111`
  — build, check:classes, check:links, format:check, lint, test:api, **test:component (`Test Files 211 passed
  (211)`)**, test:unit, typecheck all **pass**; CodeRabbit pass (rate limited). `mergeStateStatus` **CLEAN**.
  No other open PR. `git status --short` clean; ports 3320 and 5320 free.

## Final commits (on `dec7bd37`)

| sha | subject (chars) |
|---|---|
| `37b78534` | `fix(directory): keep the status on a failed read` (48) — carried 1 |
| `db4bfed5` | `fix(directory): count every photo in the viewer` (47) — carried 2 |
| `f6825122` | `fix(directory): show one tile on a phone` (40) — carried 3 |
| `8de20ec1` | `test(directory): drive the refresh by page events` (49) — carried 4 |
| `da292924` | `fix(site): reserve the bar's room only with a bar` (49) — carried 6 |
| `6ae7dbc5` | `test(map): prove the place map lets a phone scroll` (50) — carried 7 |
| `61e16baa` | `fix(directory): return the focus to the photo tile` (50) — carried 8 (found in the real run) |
| `acc9330b` | `docs: say which live status stands for a closure` (48) — carried 5 |
| `ab6707d6` | `feat(routing): offer home and say a failed retry` (48) — plan 1 |
| `e6322b43` | `feat(lookups): list the public areas for home` (45) — plan 2 |
| `433dfe00` | `feat(directory): offer home its spaces and counts` (49) — plan 3 |
| `e1446008` | `feat(site): build the home page` (31) — plan 4 |
| `03633534` | `feat(site): build the about page` (32) — plan 5 |

## Departures from the plan (summary)

1. The site's **three** boundaries use `SiteRouteError` (the plan says two; `FocusLayout` has two routes).
2. `useHomeSpaces({ chooseArea, openMap })` takes the callbacks its state line needs (the plan shows no argument).
3. `OWNERS_ANCHOR` / `SITE_PATHS.owners` in commit 4, not 5 (the owners' card needs them).
4. `directory` also exports `statusViewOf` beside `LiveStatusBadge` (the live state's word and role keep one home).
5. Two tests outside the plan's file list updated for Home's real heading: `pages/site/shell/SiteLayout.component.test.tsx`
   (seen in the scoped lane) and `app/App.component.test.tsx` (seen in CI).
6. The carried history line sits in commit 3's `directory.md` (an earlier commit would conflict beside it).
7. Test 77's first rewrite let both breaks stay green (a test defect), fixed before its commit.
8. The real run's offline case: «الرئيسية» pressed while still offline (Home's code had arrived), since going
   online first reloads the page by design; the reload on reconnect recorded as its own case.
9. Carried item 8's finger scroll used `Input.dispatchTouchEvent`; `Input.synthesizeScrollGesture` moves
   nothing in this headless Chrome (proven by a control over plain text).
10. A ninth carried commit: the focus return after Escape, found missing by the real run (the carried file
    says such a gap is a fix here, with a test).

No new finding recorded (137 not used). No data changed in `masaha_dev`; no migration deployed.
Files written outside the repository: this report, `shots\pr4\`, `scripts\` only.
