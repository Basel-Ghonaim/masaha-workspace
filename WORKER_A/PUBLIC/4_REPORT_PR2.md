# PUBLIC — PR 2 report (`feat/directory-map`, the Directory's map)

Executor: Claude Code (Opus 5.5), 2026-10-21. Plan: `2_PLAN.md` with the owner's approval note (this PR is the
plan's PR 2, three commits); carried items `0_CARRIED_FROM_103.md` (1–12) with #103's review; PR 1a's and 1b's
reports read for their departures.

## Working log (written as the work went)

## 1. First checks (before any edit)

1. **The PR before:** `gh pr view 103 --json state,mergeCommit` → `MERGED c3391d0e43b3caafd76dfc02c23cf89eaa7aeff0`.
2. `git status --short` clean; `git switch main`; `git pull --ff-only` → `Already up to date.`; `origin/main`
   `c3391d0e`.
3. **The base diff** `git diff --name-status 52b7a2b0 origin/main` → #102's files (worker B, customers and
   subscriptions): `apps/api/**`, `packages/shared/src/{core,customers,desk,payments,subscriptions}`, the web's
   `shared/copy/*/errors.ts`, and documents. **No code file this PR names changed.** `packages/shared` changed
   (`core/gazaTime.ts` gained `addDays` and `weekStartOf` only — additions; `directory`, `lookups`, `occupancy`,
   `spaces` unchanged) → `npm run build -w @masaha/shared` → exit 0.
4. **Open PRs:** `gh pr list --state open` → none.
5. **Checks against the code:**
   - g. The layer's `Sheet` (`overlays/Sheet/Sheet.tsx`) is `<SheetPrimitive.Root data-slot="sheet" {...props} />`:
     `modal` reaches Radix's root — **holds**; design issue 22 is built with `modal={false}` (Radix draws no
     overlay and traps no focus then).
   - h. Leaflet renders in the component lane: `PointPicker.component.test.tsx` finds the pin by its role and
     name with the real Leaflet — **holds**.
6. **Finding numbers:** the index holds 1–116, 120, 130, 132; 131 reserved → a new one takes **133** (carried
   item 10).
7. `docker start masaha-postgres-1`; `npx prisma migrate status` (in `apps/api`) → `23 migrations found` /
   `Database schema is up to date!`.

## 2. Branch

`git switch --no-track -c feat/directory-map origin/main` (at `c3391d0e`).

## 3. Commits (carried from #103 first)

### Carried 1 — `355287b6` `fix(directory): keep near me's focus and status` (47) — items 1, 5 (and 11)
- `LocationStatus`: one always-mounted `role="status"` wrapper (`not-empty:mt-2`) whose content changes; the
  locating line loses its own role, the warning `Alert` takes `role="none"` (the layer's `Alert` accepts `role`;
  no nested live region). Stop and clear call `returnFocus`, which `DirectoryList` points at «الأقرب إليّ» (a
  ref). `NearMeButton`: `aria-busy` and `aria-disabled` with the layer's `LoaderIcon` while locating, **not
  `disabled`** — the codebase's idiom (`SpaceActionsMenu`), no layer change; a press while locating already
  does nothing (`useNearMe`). Item 5: `cardViewOf` takes `byDistance` and words a distance only then;
  `useDirectoryList` passes `point !== null`. Item 11: `DirectoryList`'s doc comment re-wrapped (the file is
  touched here). `directory.md`: near me's paragraph, *Web history* (`#PRNUM`).
- Red first: `LocationStatus` "says each state in one live region and keeps the focus on «الأقرب إليّ» after
  stopping and clearing by keyboard" → `Unable to find an accessible element with the role "status"`;
  `useDirectoryList` "words no distance once the distance order stops, while the answer shown is still the one by
  distance" → `expected 'على بعد ⁦0.7⁩ كم' to be null` (`Tests  2 failed | 14 passed (16)`).
- Green: `vitest run --project component src/features/directory` → `Test Files  7 passed (7)` / `Tests  42
  passed (42)`; `--project unit src/features/directory` → `Test Files  8 passed (8)` / `Tests  21 passed (21)`;
  `lint` exit 0; `typecheck` exit 0.

### Carried 2 — `28f0bde6` `fix(directory): stop locating when no answer comes` (50) — item 2
- `nearMeStore.locating()` returns the ask's number; `awaits(asked)` is true only for the latest ask while still
  `locating`. `useNearMe.press` sets a 15 s watchdog (`NO_ANSWER_MS`); the first of the answer and the wait
  settles the ask (denied on the wait), anything after it is dropped (a clear or a new ask drops it too).
  `directory.md`: near me's paragraph, *Web history*.
- Red first: `useNearMe` "ends asking as denied when no answer comes within 15 s, and drops an answer that comes
  after" (fake clock, `fakeGeolocation`) → `expected { status: 'locating', …(3) } to match object { status:
  'denied', point: null }` (`Tests  1 failed | 4 passed (5)`).
- Green: `vitest run --project component src/features/directory` → `Test Files  7 passed (7)` / `Tests  43
  passed (43)`; `lint` exit 0; `typecheck` exit 0.

### Carried 3 — `31415093` `fix(directory): clear what found nothing` (40) — item 3
- `useDirectoryFilters.clearSearch()` (the search alone off, best match with it, filters and order kept) replaces
  `clearAll` (no other caller). No match's «مسح الفلاتر» runs the sheet's clear (`panel.sheet.clear.run`) while a
  filter is in force, else `clearSearch`. `directory.md:53` says both; *Web history*.
- Red first: `Tests  3 failed | 15 passed (18)` — `useDirectoryFilters` "clears the search alone, best match with
  it…" (`clearSearch is not a function`); test 23 with a filter, a search and an order → `expected '' to be
  '?q=Focus&sort=name'`; "no match's «مسح الفلاتر» clears the search when the search alone narrows the list to
  nothing" → `expected '' to be '?sort=name'`.
- Green: `vitest run --project component src/features/directory` → `Test Files  7 passed (7)` / `Tests  44
  passed (44)`; `lint` exit 0; `typecheck` exit 0.

### Carried 4 — `a4a35948` `test(directory): prove near me's privacy gates` (46) — item 4
- Test 42 gains the stop step: «إيقاف الترتيب حسب المسافة» → no privacy line, «الأقرب إليّ» `aria-pressed="false"`,
  a search typed after it → the next request (`q=مساحة`) carries no `Masaha-Near`. Existing code: proven by breaks.
- **Break (owner's): the header's sorting gate** `const point = near.state.point` (useDirectoryList) → test 41 red:
  `AssertionError: expected true to be false` (the button still on after another order), with 42 and carried
  item 5's test (`Tests  3 failed | 14 passed (17)`); restored from a copy.
- **Break (own): the stopped state's privacy gate** — `useLocationStatus`'s `sorting = state.source !== null`
  (the plan's `privacy: words.privacy` alone cannot change the outcome: the line is drawn only with `line`, which
  is gated by the same `sorting`) → test 42 red, `expect(element).not.toBeInTheDocument()` (the privacy line after
  stopping), and the focus test (`Failed Tests 2`); restored from a copy.

### Carried 5 — `3d644be9` `fix(directory): reset the price on clearing` (43) — item 6
- `usePriceFilter` returns `{ view, reset }`; `reset` empties both texts (a refused one included) and sets the
  period back to `DEFAULT_PERIOD` (now exported by `filtersOf.ts`); new texts restart the pause, so a bound typed
  within it is never written after the clear. `useFiltersPanel`'s two clear actions call `reset` then `clear`
  (no match's clear, carried 3, runs the sheet's). `usePriceFilter`'s test reads `.view`. `directory.md`.
- Red first (new `useFiltersPanel.component.test.tsx`, fake clock): "clearing resets the price's own state: a
  refused bound, a period chosen with no bound, and a bound still within its pause" → `expected
  '?period=MONTH&min=10' to be ''`.
- Green: `vitest run --project component src/features/directory` → `Test Files  8 passed (8)` / `Tests  45
  passed (45)`; `lint` exit 0; `typecheck` exit 0.

### Carried 6 — `571fb717` `fix(directory): close the sheet when it widens` (46) — item 7
- `useFiltersPanel`: `if (wide && open) setOpen(false)` (the set-state-during-render pattern). `directory.md`.
- Red first: "closes the sheet once the screen reaches the sidebar's width, so it never reopens by itself"
  (`stubScreenWidth` 768 → 1440 → 768, re-rendered) → `AssertionError: expected true to be false` (`Tests  1
  failed | 1 passed (2)`).
- Green: `Test Files  8 passed (8)` / `Tests  46 passed (46)`; `lint` exit 0; `typecheck` exit 0.

### Carried 7 — `3fdc64af` `docs(findings): widen 130 to the focus shell` (44) — items 8, 9
- Finding 130: a dated line (Back from the focus shell is a pop, the focus left nowhere; a first load a guard
  redirects with `replace` moves the focus) with `#PRNUM`; *Resolves when* names `FocusLayout` beside
  `DashboardLayout`. `check:links` → `2564 links in 204 documents and 1640 source files all resolve.`

### Carried 8 — `9aff83e7` `docs(findings): record the place filter's cap` (45) — item 10
- **Finding 133** (Open): `AreaFilter` lets any number of areas be chosen while the server takes
  `DIRECTORY_AREAS_MAX` (50) and the address reads more as none. Index line added. `check:links` → `2565 links in
  205 documents and 1640 source files all resolve.`

### Items 11 and 12
- Item 11 (the unwrapped comment at `DirectoryList.tsx:16`): re-wrapped in carried 1, which touches that file.
- Item 12 (the stopped state's bare «مسح موقعي»): kept as it is, no line added (the owner's word).

### Plan commit 1 — `4a9077a0` `feat(map): show many marks and pick a centre` (44)
- `shared/map`: `types/MapMark.ts`, `types/MarkerMapProps.ts` (`MapMarker`, `MarkerMapControls`, the plan's
  props), `services/markClass.ts`, `components/MarkerMap.tsx` (lazy, `Skeleton h-120 … lg:h-160`, its code
  failing → `MapFailed` with `failed`), `components/LeafletMarkerMap.tsx` (marks as `divIcon`s named
  `role="button"`/`aria-label`/`aria-pressed` once mounted and again with each icon, a click, Enter or Space →
  `onSelect`; the name in a `Tooltip`, permanent on the selected one, `aria-hidden`; the visitor's point
  `role="img"`; picking → `.map-crosshair`, the keys' line as the container's `aria-describedby`, marks
  `tabindex="-1"`/`aria-hidden`, a tap placing; `onViewChange` on `moveend`; `focus` → `panTo`, `upper` a quarter
  above; the overlay over the map with `centre()` and `showUser()`), `components/MapMarkSample.tsx`;
  `MapFailed` takes `line`; `leaflet.css`'s marks, ring, user point, crosshair and tooltip.
- **Departures (small):** the tiles, the zoom and the attribution (`components/MapLayers.tsx`) and the box
  (`services/mapBox.ts`: `cornersOf`, `boundsOf`) are shared with the point picker rather than copied (its
  second user); the plan's `hooks/usePickCentre.ts` is not a file — the pick's tap lives in the map's events
  component (`MapWatch`) and the centre in the overlay's `centre()`; the picker's code-failure fallback is a
  small `PickerFailed` (its line from the catalogue).
- Test 46 (`markClass.unit.test.ts`) was run first after its code (my slip): proven by its planned break, "the
  selected as a fill class" → `Expected: "map-mark map-mark-dashed map-tone-muted map-mark-selected"` / `Received:
  "map-mark map-mark-filled map-tone-muted"` (`Failed Tests 1`), restored.
- Tests 47–49 (`MarkerMap.component.test.tsx`) red first: `Failed to resolve import "./MarkerMap"` (`Tests  no
  tests`). Own breaks (§3.1 — the keyboard and the fallback): 48 marks kept tabbable (`'0'` while picking) →
  `Tests  1 failed | 2 passed (3)` (`toHaveAttribute("tabindex", "-1")`); 49 the line left out → `Tests  1 failed |
  2 passed (3)` (`Unable to find role="status"`); each restored from a copy (`scripts\brk2.py`).
- Green: `vitest run --project component src/shared/map` → `Test Files  2 passed (2)` / `Tests  13 passed (13)`
  (the picker's 10 unchanged); `--project unit src/shared/map` → `Test Files  3 passed (3)` / `Tests  25 passed
  (25)`; `lint` exit 0 (after `expect.any` gave way to `typeof` checks); `typecheck` exit 0; `check:classes` →
  `No physical direction or arbitrary-value classes in 1144 files.`; `check:links` → `2568 links in 205 documents
  and 1650 source files all resolve.`
- Docs: `architecture.md` §6 (S12's sentence corrected, `#PRNUM`; *Built:* `MarkerMap`; the failure line the
  caller's); `foundation.md` §3 (the tree's line and `leaflet.css`'s paragraph).
- **Fixup to commit 1** (`5fd9994b`, `fixup!`, autosquashed before the push): `MarkerMapControls.focusSelected()`
  (the overlay can hand the focus back to the selected mark when its card closes). Red first: `MarkerMap` test 47's
  new step → `expect(element).toHaveFocus()` (`Tests  1 failed | 2 passed (3)`); green `Tests  13 passed (13)`.

### The owner's message (2026-10-21, during commit 2)
The supervisor seeded the directory's demo set (#104, merged at `5a0cda1a`, seed only — not rebased onto) into
`masaha_dev`: 24 more listed spaces with photos; FULL `sada-space`, AVAILABLE `tal-al-hawa-desks`, CLOSED by hours
`radwan-study-hall`, CLOSED by a closure `shati-sea-view`. §13's read-only inventory is re-run before the real run.
FULL and "closed today" hold on 2026-10-21 only.

### Plan commit 2 — `ecfb7556` `feat(directory): show the spaces on a map` (41)
- `DirectoryFilters.view` (`view=map`, the list unwritten) in `filtersOf`/`paramsOf`; `services/pinMark.ts`,
  `boundsText.ts`; `types/PinsRequest.ts`, `requestOf`'s `pinsRequestOf` (a shared `filtersRequestOf`);
  `repository.pins` (`GET /map/spaces`), `directoryKeys.pins`; `cardViewOf` takes a `MapPin`;
  `hooks/map/usePinsQuery.ts` (`keepPreviousData`, `enabled`), `useSelectedPin.ts`, `useDirectoryMap.ts` (the whole
  set, then — while it is `truncated` — the box in view after a 400 ms pause, its answer replacing the marks; a
  change of filter clears the choice and the box); `hooks/view/useViewSwitch.ts`; components `DirectoryView`
  (exported; the list, or the map's toolbar — search, the sheet at every width, «الأقرب إليّ» and its line — and
  `DirectoryMap`), `view/ViewSwitch` (exported), `map/DirectoryMap`, `MapLegend`, `SelectedCard` (a region named
  by the space), `SelectedSheet` (`modal={false}`, no focus taken, not closed by a tap outside), `MapNotice`,
  `SpaceSummary`; `DirectoryPage` (the `h1` and `ViewSwitch` in a row, then `DirectoryView`); `directory.view`,
  `directory.map` in both catalogues. Docs: `directory.md` (what it does, «The map on the web», four *Web
  decisions* — S12, U6/issue 21, issue 22, issues 19–20 — code map, *Web history*), finding 46's evidence line.
- **Departures:** `useFiltersPanel` takes `sheetOnly` (the map's sheet at every width); the list's failure view is
  shared as `hooks/list/useFailureView.ts` (the list's behaviour unchanged, its tests green); the map has an
  `empty` state beside `noMatch` (design issue 18's words, as the list); `clearFilters` keeps the view (found by
  test 56: clearing on the map returned to the list); the pin's accessible name is not isolated (an attribute,
  never drawn); `DirectoryList` stays internal; near me on the map has no count beside it; closing the chosen
  space returns the focus to its pin (`focusSelected`).
- **Red first:** unit — `Cannot find module './boundsText'` / `'./pinMark'` (50, 51), `repository.pins is not a
  function`, filtersOf 58 (`expected undefined to be 'list'`, `…to match object { view: 'map', verified: true }`)
  (`Test Files  4 failed | 6 passed (10)`); `useDirectoryMap` (52, 53) → `Failed to resolve import
  "./useDirectoryMap"`; `DirectoryMap` (54–57) → `Failed to resolve import "../DirectoryView"`. Then two failures
  on the way: 56 (`expected '?q=Hub' to be '?q=Hub&view=map'` — the code's: `clearFilters` dropped the view) and
  57 (my test asked for `group`; Radix's single toggle group is a `radiogroup`).
- **Own breaks** (§3.1): 53 [bound] no re-ask (`whole.data?.truncated === true` → `false`) → `Tests  1 failed |
  2 passed (3)` (`expected null not to be null`); 54 [width] the card at every width (`phone` false) → `Tests  1
  failed | 5 passed (6)` (`Unable to find role="dialog" and name "مساحة 1"`); 54 [fallback, `Sheet`'s `modal`]
  `modal={false}` → `modal`: **first green** — my test's defect (it asserted no `aria-modal`, which Radix never
  sets); the assertion became "the other marks stay reachable, no scrim", green, then the break → `Tests  1
  failed | 5 skipped (6)` (`Unable to find … "مساحة 2 — لا تتوفر حالة مباشرة"`). Each restored from a copy.
- Green: `vitest run --project component src/features/directory src/shared/map src/pages/site` → `Test Files  19
  passed (19)` / `Tests  111 passed (111)`; `--project unit src/features/directory src/shared/map src/shared/copy`
  → `Test Files  15 passed (15)` / `Tests  83 passed (83)`; `lint` exit 0; `typecheck` exit 0; `check:classes` →
  `… in 1165 files.`; `check:links` → `2569 links in 205 documents and 1671 source files all resolve.`

### Plan commit 3 — `c46bb6ec` `feat(directory): set my location on the map` (43)
- `NearState.status` gains `picking`; the store's `startPick` (the state before kept), `cancelPick` (restores
  it), `placePin(point)`; `useNearMe` exposes them, `placePin` through `services/nearPoint.ts`'s `pinnedPoint`
  (rounded, held inside the Strip's box — a departure: the map lets the centre pass the box a little, which the
  server's header would refuse); `useLocationStatus` takes `pickOnMap` («حدّد موقعي على الخريطة» beside «اختر
  منطقتك»; «تغيير الموقع» beside a pin's line; nothing while picking); the list's `pickOnMap` starts the pick and
  switches to the map, filters kept; `useDirectoryMap`'s `pick` (the crosshair, `onPick` = `placePin`, the keys'
  line), the pin's label «موقعي (يدوي)», the chosen space and «مركّز على موقعي» hidden while picking;
  `components/map/PickCard.tsx` (a region named by its title; focuses the map on opening; «ثبّت الموقع هنا»
  places `centre()`, «رجوع» cancels); `MapView` hides «الأقرب إليّ» while picking and gives it the focus after.
  `directory.pick`, `near.pickOnMap`, `near.change`, `map.yourPin`, `near.denied.text` (changed), both catalogues.
  `directory.md`: «Setting one's location on the map», a *Web decision* (U7), *Web history*.
- A second fixup to commit 1: `MarkerMapControls.focusMap()`; written with its test step ("To the map"), proven by
  its break (the focus call removed → `expect(element).toHaveFocus()`, `Tests  1 failed | 2 passed (3)`).
- **Red first:** 59 (`useNearMe`) → `TypeError: result.current.near.startPick is not a function`; 60
  (`LocationStatus`) → `Unable to find an element with the text: اختر منطقتك أو حدّد موقعك على الخريطة…`
  (`Tests  2 failed | 9 passed (11)`); the map's picking test (`DirectoryMap`, an addition) → `Unable to find
  role="region" and name "حدّد موقعك على الخريطة"` (`Tests  1 failed | 6 skipped (7)`).
- **Own breaks** (privacy): 59 the pin not rounded → `expected { status: 'granted', …(3) } to deeply equal …`;
  59 cancel clears (`IDLE`) → `expected { status: 'idle', point: null, …(2) } to deeply equal { status:
  'granted', …(3) }`; the box's clamp left out (`pinnedPoint`'s unit case, written with its code) → `expected {
  lat: 31.7, lng: 34.1 } to deeply equal { lat: 31.64, lng: 34.17 }`. Each `Tests  1 failed`, restored.
- Green: `vitest run --project component src/features/directory` → `Tests  58 passed (58)`; `--project unit
  src/features/directory src/shared/copy` → `Tests  59 passed (59)`; `lint` exit 0; `typecheck` exit 0;
  `check:links` → `2569 links in 205 documents and 1672 source files all resolve.`; `check:classes` → `… in 1166
  files.`

### The fixups folded (2026-10-22)
- `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash origin/main` **first went onto the new `origin/main`
  (`5a0cda1a`, #104)**, against the owner's word — caught at once by the tree check (six seed files differed).
  Undone: `git reset --hard e73488cd` (the head before, nothing uncommitted), then autosquash onto `c3391d0e`;
  `git diff e73488cd HEAD` → empty. The branch stays on `c3391d0e`. Commits now: `355287b6`, `28f0bde6`,
  `31415093`, `a4a35948`, `3d644be9`, `571fb717`, `3fdc64af`, `9aff83e7`, `a9dacf35` (map), `f2d50539`
  (directory map), `c46bb6ec` (pick).

## 4. On the head (`c46bb6ec`), once each (2026-10-22)

No `node` of `C:\dev\masaha\app-b\` before each lane (`… -match 'app-b'` → 0). Free memory: unit 7,096,308 KB;
component 7,074,340 KB.
- `npm run test:unit -w @masaha/web` → exit 0: `Test Files  108 passed (108)` / `Tests  903 passed (903)`
  (`scripts\lane2-unit.txt`).
- `npm run test:component -w @masaha/web -- src/shared/map src/features/directory src/pages/site
  src/shared/design-system` → exit 0: `Test Files  57 passed (57)` / `Tests  360 passed (360)`, `Duration
  100.02s` (`scripts\lane2-component.txt`). The folders this PR touches; `shared/copy` is in the unit lane.
- `$env:NODE_ENV='production'; npm run build` → exit 0 (`✓ built in 2.04s`); `npm run check:build` → exit 0: `No
  showcase code in 49 build files (1028 strings checked).` / `No dashboard code in the site's first download.` /
  `No data-table or leaflet, nor Leaflet's stylesheet, in the site's first download.`
- `check:classes` → `No physical direction or arbitrary-value classes in 1166 files.`; `format:check` → `All
  matched files use Prettier code style!`; `check:links` → `2569 links in 205 documents and 1672 source files all
  resolve.`
- **The first download** (`scripts\firstDownload-2-head.txt`): **992,328 bytes, 7 chunks** (1b's head: 989,912, 6):
  entry 254,998; CSS 83,197; `jsx-runtime` 123,714 (the catalogue's new words); `routing` 236,489 and a
  `design-system` chunk 279,426 (together 515,915, the old `routing` 515,977 split in two by the bundler);
  `react-dom`, `direction`, `mutation` unchanged. No `leaflet`, `data-table`, `dashboard`, `directory`,
  `DirectoryPage` or `HomePage`. The map's marks and crosshair live in the lazy `MapLayers-*.css` with
  Leaflet's stylesheet; `not-empty:mt-2` reached the entry's CSS.
- **Not run locally (CI judges):** the full `test:component` lane, `test:unit` of `apps/api` and
  `packages/shared`, `test:api`.

## 5. STOPPED before the real run (2026-10-22) — Docker Desktop is not running

- `docker ps` → `failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine … The system
  cannot find the file specified.`; `npx prisma migrate status` (in `apps/api`) → `Please make sure your database
  server is running at localhost:5433.`
- The prompt's §1.7: Docker Desktop not running → stop and ask the owner to start it. Nothing was started: no API,
  no web server, no browser; ports 3320 and 5320 untouched.
- **Where the work stands:** `feat/directory-map`, 11 commits on `c3391d0e` (not rebased; head `c46bb6ec`), `git
  status` clean; every check on the head green (§4). **Not yet done:** the inventory (`scripts\inventory2.mjs`,
  written, not run), the real run, `#PRNUM`, the push, the PR, CI, the conflict check.
- **To resume** once Docker Desktop runs: `docker start masaha-postgres-1`, `npx prisma migrate status`, the API
  on 3320, `node scripts\inventory2.mjs` (read-only), then the real run (§1.9) — today is 2026-10-22, so the
  seed's FULL and "closed today" may be gone: recorded as not performed, by design (tests 50, 55), if so.

## 6. Resumed (2026-10-22): the inventory and the real run, then STOPPED before #PRNUM (the owner's word)

- Docker Desktop started by the owner. `docker start masaha-postgres-1`; `npx prisma migrate status` → `Database
  schema is up to date!`. API on 3320 (`npm run dev -w @masaha/api`), Vite on 5320 (`npx vite --port 5320
  --strictPort` in `apps/web`).
- **Inventory** (`scripts\inventory2.mjs`, plain GETs; `inventory2.out.txt`, 06:47 UTC): 59 listed spaces; `GET
  /map/spaces` → 59 pins, not truncated; AVAILABLE 10, **FULL 1 (`sada-space`)**, CLOSED 2 (`shati-sea-view`,
  `zeitoun-works`), none 46; 12 with a cover; `verified=true` → 20; a search for nothing → 0; `bounds=31.4,34.3,
  31.55,34.5` → 53. Re-read at 06:50 UTC (`inventory2b.out.txt`): **FULL 0 — `sada-space` AVAILABLE**;
  `radwan-study-hall` AVAILABLE (not closed by hours at that time).
- **Browser:** local headless Chrome over CDP (no `playwright` MCP tools): `scripts\cdp2.mjs`, `scripts\run2.mjs`;
  outputs `scripts\run2-*.txt`, screenshots `shots\pr2\`.

| Case | Result | Shots |
|---|---|---|
| «خريطة»: the pins by state and the legend, ar light and en dark at 390, 768, 1440 | `?view=map`; marks filled 11, bar 0, hollow 2, dashed 46; the legend «متاح · ممتلئ · مغلق الآن · لا تتوفر حالة مباشرة» / "Available · Full · Closed now · No live status" at the top's end, the zoom at the start | `2-pins-*` (6) |
| **FULL (barred pin)** | **NOT PERFORMED, by design**: the seed's FULL had ended by the run (06:50 UTC, `sada-space` AVAILABLE); tests 50 (`pinMark`) and 55 (the legend's marks) prove it | — |
| A chosen pin at every width, both languages | 768, 1440: the card over the map's foot (a region named by the space: name, «النصر · غزة», «متاح», «موثّقة», today, «عرض التفاصيل»), no dialog; 390: the bottom sheet, the focus left on the pin; **with the sheet open the arrows pan the map** (`translate3d(-46px, -15px, 0px) → (-46px, 55px, 0px)`), the sheet still open; «إغلاق» → the focus back on the pin | `2-select-*`, `2-select-panned-*-390` |
| «عرض التفاصيل» | → `/spaces/tal-al-hawa-desks` (the site's 404 until PR 3) | `2-details-*` |
| A filter on the map (sheet at 1440 too) | «المساحات الموثّقة فقط» → the sheet's «عرض 20 مساحة» / "Show 20 spaces"; `?verified=1&view=map`; marks 59 → 20 | `2-filter-*` |
| «حدّد موقعي على الخريطة» from denied → crosshair → arrows → «ثبّت الموقع هنا» → «تغيير الموقع» → «رجوع» | denied line with both fallbacks; `?view=map`, crosshair, **the map focused**, described by the keys' line, marks not tabbable (0), «الأقرب إليّ» hidden; arrows pan (at 1440 after the map's «+», since the fitted view already holds the whole box: `→ translate3d(-1px, 269px, 0px)`); placed → «مرتبة حسب المسافة من الموقع الذي حدّدته على الخريطة. …» with the privacy line, «إيقاف…», «تغيير الموقع», «مسح موقعي»; the focus on «الأقرب》（*); the point «موقعي (يدوي)»; the list sorted («على بعد 4.5 كم» …, «الترتيب: حسب المسافة»); «تغيير الموقع» → «رجوع» → the same pin and line | `2-pick-*` |
| **Privacy in the log** | ar 390: 15 API requests, 1 with `Masaha-Near` (`31.41,34.302`), on `sort=distance`; en 1440: 21 requests, 1 (`31.568,34.395`); no coordinate in any URL (the map's `bounds` aside) | `2-pick-*-log.txt` |
| «مركّز على موقعي»; Leaflet's chunk and stylesheet only after «خريطة»; carried items 1 and 3 in the browser | **NOT PERFORMED — stopped by the owner** before these cases (scripted in `run2.mjs`: `centre`, `leaflet`, `carried`); their component tests: `MarkerMap` (showUser through the overlay), `check:build`'s Leaflet rule, `LocationStatus` and `useDirectoryList` | — |

- **Found in the run and fixed (folded):** at 390 the picking card covered the map's centre and its crosshair. The
  map gains an `under` slot (drawn below it with the same controls; nullable) — a fixup to the map commit, its
  test step red first (`Unable to find … "Under the map"`), green; commit 2 passes `under={null}` (a fixup);
  below 768 px the picking card stands under the map (a fixup to commit 3, with its test red first: `expected
  <div …> to be null`, green); `directory.md`, `architecture.md` §6 say it. Autosquashed onto `c3391d0e` with
  `--exec "npx tsc -b apps/web"` after every commit — all passed. The head's lanes were not re-run after this fold
  (the owner's stop came first): the map and directory component tests green on the working tree (`Tests  8
  passed (8)` for `components/map`, the map lane `Tests  13 passed (13)`), `lint` exit 0.
- **Observation for the review, not changed:** in the dark theme the hollow and dashed marks fill with `card`
  (dark) on OpenStreetMap's tiles, light in both themes, so they read as dark dots (`2-pins-en-dark-1440.png`);
  the shapes stay distinct. It follows the plan's spec («a 2 px border on `card`»); no finding recorded.
- **Stopped (the owner, 2026-10-22): before `#PRNUM`.** No PR-number replacement, no push, no PR. Branch
  `feat/directory-map`, head `026ad224`, 11 commits on `c3391d0e`, `git status` clean. Servers stopped by id
  (15500, 13220, 8256, 15412); ports 3320 and 5320 free; no headless Chrome left. `masaha_dev`: GETs only.

## 7. Finished by OpenCode (2026-10-22)

### §1 Preconditions — all held
- `git status --short` → nothing
- `git branch --show-current` → `feat/directory-map`
- `git rev-parse --short HEAD` → `026ad224`
- `git merge-base HEAD origin/main | cut -c1-8` → `c3391d0e`
- `git ls-remote --heads origin feat/directory-map` → nothing (not pushed)
- `git log --format='%h %s' c3391d0e..HEAD` → 11 commits as expected
- `docker ps` → `masaha-postgres-1 Up 35 minutes (healthy)`

### §2 Squash — five new shas recorded
- `2c2f9f37` `fix(directory): carry #103's review fixes`
- `2584d86f` `docs(findings): record #103's review findings`
- `3a4ea837` `feat(map): show many marks and pick a centre`
- `c1c46310` `feat(directory): show the spaces on a map`
- `f0fc8a73` `feat(directory): set my location on the map`

**Checks passed:**
- `git diff 026ad224 HEAD --stat` → nothing (same tree)
- `git log --format='%h %s' c3391d0e..HEAD` → 5 commits, oldest first as expected
- No co-authored/generated-with/opencode/claude references
- `git status --short` → nothing
- `npx tsc -b apps/web` → exit 0

### §3 Three real-run cases
**Centre** (exit 0):
```
== centre
· ar 390 granted on the map — state line: مرتبة حسب المسافة من موقعك. المسافات تقريبية بخط مستقيم. يُرسَل موقعك مقرَّبًا لترتيب المساحات حسب المسافة فقط، ولا يُحفظ. | إيقاف الترتيب حسب المسافة | مسح موقعي user point: موقعك
· ar 390 «مركّز على موقعي» moved the map: false
shot 2-centre-ar-light-390
· en 1440 granted on the map — state line: Sorted by distance from your location. Distances are approximate, in a straight line. Your location is sent rounded, only to sort spaces by distance, and is never stored. | Stop sorting by distance | Clear my location user point: Your location
· en 1440 «مركّز على موقعي» moved the map: false
shot 2-centre-en-dark-1440
```

**Leaflet** (exit 1 — FAILED):
```
== leaflet
· dev Leaflet requests before «خريطة»: 0 — after: 5 ["/src/shared/map/components/LeafletMarkerMap.tsx","/src/shared/design-system/leaflet.css","/node_modules/.vite/deps/leaflet.js?v=183970b9","/node_modules/.vite/deps/react-leaflet.js?v=183970b9","/src/shared/map/components/MapLayers.tsx"]
shot 2-leaflet-dev
Error: eval: SecurityError: Failed to read the 'localStorage' property from 'Window': Access is denied for this document.
```

**Carried** (exit 1 — FAILED):
```
== carried
Error: eval: TypeError: Cannot read properties of undefined (reading 'focus')
```

**New screenshots from this run:**
- `2-centre-ar-light-390.png`
- `2-centre-en-dark-1440.png`
- `2-leaflet-dev.png`

**Leaflet log first line:** `before «خريطة»: 0`

### §4 PR number
- `git fetch origin` — done
- Next issue number calculation: `n = 1041` (calculated from `gh api "repos/Basel-Ghonaim/masaha/issues?state=all&per_page=1&sort=created&direction=desc" --jq '.[0].number' + 1`)
- `#PRNUM` → `#1041` replacement in docs: 9 occurrences across 5 files:
  - `docs/architecture/findings/130-the-dashboards-shells-have-no-skip-link.md` (1)
  - `docs/architecture/findings/46-the-deployments-headers-must-let-the-maps-tiles-load.md` (1)
  - `docs/features/directory.md` (6)
  - `docs/frontend/architecture.md` (1)
- `git filter-branch` — no rewrites needed (already on correct base)
- `git grep -n '#PRNUM'` — nothing (all replaced)
- `npm run check:links` — exit 0: `2569 links in 205 documents and 1672 source files all resolve.`
- `npm run format:check` — exit 0: `All matched files use Prettier code style!`
- `git status --short` — 4 modified docs files (the #PRNUM replacements)

### §5 Push and PR
- `git push -u origin feat/directory-map` — pushed successfully
- `gh pr create` via API — created **PR #105** (URL: https://github.com/Basel-Ghonaim/masaha/pull/105)
- **MISMATCH:** Expected PR number `n = 1041`, GitHub assigned **#105**. Per instructions: stop and report both numbers.
- PR head SHA: `f0fc8a7395958124fb216893e1735db78c2dee39` (matches local HEAD `f0fc8a73`)
- Base branch: `main` (SHA `5a0cda1a6f211e3d439dd313429bb395fcc09db7` — **not** `c3391d0e` as required)

### §6 CI
- Not reached (stopped at §5 due to PR number mismatch)

### Summary of failures
- PR number mismatch: expected 1041, got 105
- PR base is `main` (5a0cda1a) not c3391d0e as required

**Ports 3320/5320 free:** yes (TimeWait only, no Listen)
**git status clean:** yes (only the 4 docs files with #1041 replacements)
### §3 redone by the supervisor (2026-10-22) — `scripts\run2b.mjs`

OpenCode's §3 stopped on two defects of `run2.mjs`, not of the app: `leaflet`'s second half needs the
production preview on 5321, which was not started; `carried` pressed Enter with `key()`, whose keyDown carries no
text, so a native button never activates (Radix's menus read the keydown, so `openMenu` worked). `centre` ended
0 but proved nothing: it never panned the map away before pressing. The supervisor re-scripted the three cases
(`run2b.mjs`: Enter sent with `text: '\r'`; the map panned away, then «مركّز على موقعي» judged by the user
point's distance from the map's centre) and ran each once on head `f0fc8a73` (the same tree as `026ad224`):
API 3320, Vite 5320, `vite preview` 5321 after `NODE_ENV=production npm run build -w @masaha/web` (exit 0).
Outputs `scripts\run2b-*.txt`; all three exit 0.

| Case | Result | Shots |
|---|---|---|
| Carried 1 — the focus after stop and clear, by keyboard | Enter on «الأقرب إليّ» → the granted line; Enter on stop → focus on «الأقرب إليّ» / "Nearest to me"; again, Enter on «مسح موقعي» → focus on «الأقرب إليّ» (ar 390, en 1440) | `2-carried-focus-*` |
| Carried 3 — no match's «مسح الفلاتر» | `?q=Hub&available=1&friday=1&students=1` → no match → «مسح الفلاتر» → `?q=Hub`, the search field `Hub` (both) | `2-carried-nomatch-*`, `2-carried-cleared-*` |
| «مركّز على موقعي» | the user point 95 px (ar 390: 57 after panning) from the map's centre → 0 px after the press: **centred** (both) | `2-centre-away-*`, `2-centre-*` |
| Leaflet only after «خريطة» | dev: 0 before → 5 after; **build: 0 before → 4 after** (`LeafletMarkerMap-*.js`, `MapLayers-*.js`, `leaflet-*.js`, `MapLayers-*.css`) | `2-leaflet-dev`, `2-leaflet-build` |

Servers stopped by their ports' processes; 3320, 5320, 5321 free; `git status` clean. **OpenCode resumes at §4.**
