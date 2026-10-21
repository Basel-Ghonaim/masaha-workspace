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
