# Review — PUBLIC PR 2 (#105, `feat/directory-map`)

**Head:** `f0fc8a7395958124fb216893e1735db78c2dee39`. It had not moved when the review ended (`gh pr view 105` read again at the end), so there is no head diff to check.

**Base and CI:**
- base `origin/main` `5a0cda1a`; the branch sits on `c3391d0e`; `mergeStateStatus: CLEAN`;
- `gh pr checks 105`: all ten green (build, which runs `check:build` in `ci.yml:43`; check:classes; check:links; format:check; lint; test:api; test:component 12m46s; test:unit; typecheck; CodeRabbit).

**Commits:** five.
- `2c2f9f37 fix(directory): carry #103's review fixes` (41)
- `2584d86f docs(findings): record #103's review findings` (45)
- `3a4ea837 feat(map): show many marks and pick a centre` (44)
- `c1c46310 feat(directory): show the spaces on a map` (41)
- `f0fc8a73 feat(directory): set my location on the map` (43)

**Verdict: mergeable, no blocker.** The position's privacy holds today. Five findings are should-fix:
- the pick outlives the map;
- the chosen space is out of reach for a keyboard or a screen reader;
- the raw centre of the pick can go out in `bounds` past 1,000 pins;
- the map's near-me line claims a sort;
- the first load of the pins shows nothing.

Each is small. Under the owner's rule they go to **PUBLIC PR 3's first commit** (through `0_CARRIED_FROM_105.md`). The owner may prefer a fix round for 1 and 2, since both sit on the PR's main flows.

**What I saw and what I only read.** I read the code, the tests, the documents and the commit messages through commit objects only. I ran no test, build, server or browser.

These come **from the executor's report only** (`4_REPORT_PR2.md`):
- every red step and every break;
- the local lane counts;
- the first download's sizes;
- the real run, its widths and its logs;
- the supervisor's redone cases (`run2b`): the Leaflet requests before and after «خريطة», «مركّز على موقعي» centring, and carried items 1 and 3 in the browser;
- the dark-theme observation;
- `masaha_dev` left unchanged.

I saw no screenshot.

---

## The five most important findings

### 1. The pick outlives the map, so the location from before is hidden and comes back as a crosshair — should-fix
- **Where:**
  - `hooks/near/nearMeStore.ts:48-58`: `startPick` saves `beforePick` and sets `{ ...IDLE, status: 'picking' }`, and only `cancelPick` or `placePin` leaves it.
  - `components/DirectoryView.tsx:31`: `MapView` has no cleanup.
  - `hooks/near/useLocationStatus.ts:32`: `picking` → `none`.
  - `hooks/list/useDirectoryList.ts:106-109`: `pickOnMap` writes the view with `replace`.
- **Scenario (seen in the code):**
  - A visitor holds a pin's location, so the list is sorted, and presses «تغيير الموقع». The map opens with the crosshair.
  - They then leave by «قائمة», by Back (the address was replaced, so Back leaves the page), or by a link. Nothing calls `cancelPick`, and the module-level store stays `picking` with `point: null`.
  - On the list:
    - the state line is gone;
    - «الأقرب إليّ» is off;
    - the list is no longer sorted.
  - The location from before still sits in `beforePick`, unseen.
  - Choosing «خريطة» later reopens the map **in picking mode**, unasked: the crosshair shows, and `PickCard`'s mount effect moves the focus to the map.
  - Pressing «الأقرب إليّ» on the list instead asks the device again.
  - So «رجوع» restores the location exactly only if the visitor leaves through «رجوع».
  - No position leaks.
- **Fix:**
  - End the pick when the map's view unmounts: `useEffect(() => () => nearMeStore.cancelPick(), [])` in `MapView` or `useDirectoryMap`.
  - Test: start a pick from a pin's line, switch to «قائمة», and see the pin's line and the sort again.
- **Where its fix belongs:** small → **PUBLIC PR 3's first commit**.

### 2. A keyboard or screen-reader visitor cannot easily reach the chosen space — should-fix
- **Where:**
  - `shared/map/components/LeafletMarkerMap.tsx:130-160`: the overlay `div` comes after the `MapContainer` in the DOM. Every mark is `tabindex="0"` (`:215`), in Leaflet's marker pane.
  - `components/map/SelectedSheet.tsx` → the layer's `SheetContent`, which renders in `SheetPrimitive.Portal` (`overlays/Sheet/Sheet.tsx:60`), at the end of `body`.
- **Scenario (seen in the code; not tried with a screen reader):**
  - From 768 px, Enter on a pin shows the card. The focus stays on the pin, as designed.
  - In the tab order, though, the card's «عرض التفاصيل» comes after **every remaining pin**, the zoom and the attribution: 58 Tab presses with today's 59 spaces, and up to 999 past the ceiling.
  - «مركّز على موقعي» sits in the same place.
  - Below 768 px the sheet is a portal after the site's footer, and nothing announces it:
    - it takes no focus (by design);
    - it is no live region;
    - only the pin's `aria-pressed` changes.
  - A screen-reader visitor on a phone double-taps a pin, hears "pressed", and has to find the details after the footer.
- **Fix (small, within the owner's design):**
  - Draw the overlay before the map in the DOM, with its own stacking above the panes. This puts the card, the legend and «مركّز على موقعي» before the pins in the tab order.
  - For the sheet, add one polite line in `DirectoryMap`, such as «{name}: التفاصيل في أسفل الصفحة». Or render the sheet in place rather than in a portal (a layer option).
  - Both need a test of the order.
  - Moving the focus to the card is the other way, but it reverses U6's focus rule, so it is the owner's choice.
- **Where its fix belongs:** **PUBLIC PR 3's first commit**. The owner may prefer a fix round, since it is the map's main flow for these visitors.

### 3. Past 1,000 pins, the pick sends its unrounded centre in `bounds` — should-fix, plausible (not reachable with today's data)
- **Where:**
  - `hooks/map/useDirectoryMap.ts:62-70`: `onViewChange` is given whenever the whole set is `truncated`, picking included.
  - `services/boundsText.ts:4`: full float precision.
  - `LeafletMarkerMap.tsx` `MapWatch`: `moveend`.
- **Scenario (seen in the code):**
  - While picking, the visitor pans the crosshair onto their home.
  - 400 ms after each pause, `GET /map/spaces?bounds=s,w,n,e` goes out. The box's centre is the crosshair's raw point, to about 1 m and **unrounded**, in a URL that hosts log. It goes out even if they then press «رجوع».
  - This breaks the pick card's own promise («يُرسَل مقرَّبًا ولا يُحفظ»).
  - The same happens after «مركّز على موقعي»: `setView(user.point)` → `moveend` → a box centred exactly on the rounded point.
  - The prompt sets `bounds` apart, but here the box carries the position itself.
  - It needs more than 1,000 listed spaces, so it does not happen today.
- **Fix:**
  - Give no `onViewChange` while picking. The pick needs no pins.
  - Round the box outward to two decimals (about 1 km) in `boundsText`. That also lets nearby pans share a cache key.
  - Unit-test both.
- **Where its fix belongs:** small → **PUBLIC PR 3's first commit**. If the owner prefers, record it as a finding, since it cannot be reached yet.

### 4. On the map, near me says the spaces are sorted and the location sent, while the map sends nothing — should-fix (the owner's word)
- **Where:**
  - `hooks/map/useDirectoryMap.ts:92-100` uses the list's `useLocationStatus` unchanged;
  - `useLocationStatus.ts:36-43`;
  - `pinsRequestOf` carries no point, and the repository's `pins` sends no header.
- **Scenario:**
  - **Seen in the code:** on the map, a granted location shows «مرتبة حسب المسافة من موقعك. المسافات تقريبية بخط مستقيم. يُرسَل موقعك مقرَّبًا لترتيب المساحات حسب المسافة فقط، ولا يُحفظ.» with «إيقاف الترتيب حسب المسافة».
  - **Read in the report's §7 log only:** the real run's text, "granted on the map — state line: مرتبة حسب المسافة من موقعك…".
  - The map is not ordered, and no map request carries `Masaha-Near`.
  - The line states what this screen does not do ("claim only what is true").
  - `directory.md`'s "the privacy line shows only while a location is asked or sent" is not true on the map either.
  - It errs on the safe side for privacy, but it is false.
- **Fix:** on the map, a line of its own, for example «موقعك ظاهر على الخريطة. تُرتَّب القائمة حسب المسافة منه.», with no privacy sentence, and no stop button or a reworded one. Its wording is the owner's.
- **Where its fix belongs:** small → **PUBLIC PR 3's first commit**, after the owner approves the words.

### 5. While the pins first load, the map shows nothing, and `directory.md` says loading is shown — should-fix
- **Where:**
  - `hooks/map/useDirectoryMap.ts:138`: `busy: answer !== undefined && …`, so it is false before the first answer.
  - `components/map/DirectoryMap.tsx`: nothing reads `state === 'loading'`.
  - `docs/features/directory.md` › «The map on the web»: "Loading, a failure …, an empty directory and no match … are each said over or above the map".
- **Scenario (seen in the code):**
  - On a weak connection, the tiles arrive before the pins. For seconds, the visitor sees a map with no pins, no sign of loading, and `aria-busy="false"`.
  - It reads as a Strip with no spaces.
  - The `Skeleton` covers only the Leaflet code's arrival.
- **Fix:**
  - Mark the section busy while `whole.isPending`.
  - Draw a muted line over the map's foot (the `MapNotice` look), for example «جارٍ تحميل المساحات…», in both catalogues.
  - Test it with a held answer.
- **Where its fix belongs:** small → **PUBLIC PR 3's first commit**.

---

## The rest

### 6. From 768 to 1023 px, the picking card may cover the crosshair — should-fix, plausible
- **Where:**
  - `DirectoryMap.tsx:28-30, 68-70`: the card goes under the map only below 768 px.
  - the map is `h-120` (480 px) until `lg:h-160`.
- **Scenario (my arithmetic, not run; the real run did the pick only at 390 and 1440):**
  - The card is about 220 px tall: the layer's `--card-padding` of 20 px three times, the title, about three lines of text and the buttons.
  - It stands on `pb-8` at the overlay's foot, so its top is near 230 px. The crosshair spans 224–256 px at the centre.
  - It is `max-w-sm` at the start edge, so at 768 px it spans the map's centre horizontally too.
  - The fix folded after the real run is therefore probably needed up to 1024 px.
- **Fix:** put the card under the map below `lg` (the map's own height breakpoint), with the test's width moved.
- **Where:** **PUBLIC PR 3's first commit**.

### 7. Escape does not close the card from 768 px — nit
- **Where:** `SelectedCard.tsx`; no key handler in `DirectoryMap`. The sheet closes on Escape (Radix) and hands the focus back. The card has only «إغلاق».
- **Fix:** Escape on the map, or in the card, runs the same `close`.
- **Where:** **PUBLIC PR 3's first commit**.

### 8. No test of the sheet's «إغلاق» or Escape returning the focus to the pin — nit
- **Where:** `DirectoryMap.component.test.tsx`: test 54's phone case stops at "the focus stays on the mark". Only the card's «إغلاق» is asserted. The sheet's return was seen only in the real run (from the report).
- **Where:** **PUBLIC PR 3's first commit**, with item 7.

### 9. Each render of the map rebuilds every marker — nit, plausible
- **Where:**
  - `useDirectoryMap.ts:115-129`: `cardViewOf` runs for every pin on every render, with today's hours among it;
  - `LeafletMarkerMap.tsx:221`: a new `eventHandlers` object per mark, which react-leaflet unbinds and binds again;
  - `MarksMap` re-renders each `PlaceMark`.
- **Scenario:** each key typed in the map's search re-renders the view, so up to 1,000 marks are rebuilt per key. On a weak phone that can make typing lag. I did not measure it.
- **Fix:** memoise the markers on the answer and the language, and give stable handlers (or `memo(PlaceMark)`).
- **Where:** **a finding to record**, or the next PR if the owner wants it now.

### 10. Dark theme: the hollow and dashed marks are dark dots on the always-light tiles — nit (the executor's observation, judged)
- **Where:** `leaflet.css`: `.map-mark-hollow span` and `.map-mark-dashed span` fill with `var(--card)`, and the filled marks are edged on `var(--card)`.
- **Judgement (from the code; I did not see `2-pins-en-dark-1440.png`):**
  - The plan's spec is followed. The four shapes stay distinct, since no filled mark is muted.
  - But the legend shows the same marks on the dark card, where they read as hollow, while on the light tiles they read as filled dark discs. The legend and the map then disagree in dark theme only.
  - The tiles do not follow the theme, so the marks drawn on them should not either.
- **Fix:** draw the marks with the light theme's values inside `.leaflet-container`, for example by giving the map pane the light tokens. That is a layer change, so it is the owner's design call.
- **Where:** **a finding to record**.

### 11. The ceiling is written into the copy — nit
- `directory.map.truncated` hard-codes «1000» / "1,000", while `@masaha/shared/directory` exports `MAP_PINS_CEILING`. If the server's ceiling changes, the line is wrong.
- **Fix:** take `{count}` from the constant, formatted for each language.
- **Where:** **PUBLIC PR 3's first commit**.

### 12. A catalogue comment says what the code does not — nit
- `shared/copy/english/directory.ts`, `map.pin`: "the space's name, isolated". The code deliberately does not isolate it (`useDirectoryMap.ts:121`, the reported departure).
- **Where:** **PUBLIC PR 3's first commit** (one line).

### 13. The layer calls the Sheet always modal — nit
- `overlays/Sheet/Sheet.tsx:12` says "It is a modal dialog: it traps the focus". Foundation's Sheet row says nothing of `modal={false}`, which the directory now uses (design issue 22).
- The next caller will read the layer's own contract as false.
- **Fix:** one clause in the comment and in foundation's Sheet row: non-modal on request, with no scrim and no trap, as the directory's chosen space.
- **Where:** **PUBLIC PR 3's first commit**. It touches the layer's documents, so it needs `area:design-system`.

### 14. The overview's build line omits the site's map — nit
- `docs/project/overview.md:22` still ends "on the site, the directory's list: search, filters, sort, pages and near me." The plan's PR 2 document list left the overview out.
- The line now understates what is built. That is not a false claim, but it is one place the build state should be complete.
- **Where:** **PUBLIC PR 3's first commit**, or with PR 3's own overview edit.

### 15. The 15 s watchdog counts the time spent at the permission prompt — nit, plausible
- **Where:** `useNearMe.ts:57-61`.
- **Scenario:**
  - A visitor reads the browser's prompt for more than 15 s, then allows it.
  - The ask has already ended as denied, so the answer is dropped and «تعذّر تحديد موقعك» shows.
  - A second press works, since the permission is now given.
  - This is the owner's ≈ 15 s, which favours the stuck case.
- **Where:** **a finding to record**, or accept it as it is.

### 16. The map's container is always `role="application"` — nit, plausible
- **Where:** `LeafletMarkerMap.tsx:72-77`.
- **Scenario:** in a screen reader, an application switches off browse mode for everything inside it: the marks' names, the tooltips and the attribution's link. It is needed for the arrow keys, but it also applies outside the pick.
- **Fix:** keep it, but name it in `architecture.md` §6, or apply it only while picking. Not tried with a screen reader.
- **Where:** **a finding to record**.

---

## The executor's departures, judged
- **Shared `MapLayers` and `mapBox`:** right. The point picker is their second user, and they are moved without change. The picker's failure line still comes from the catalogue (`PickerFailed`).
- **No `usePickCentre` file:** fine. The tap is in `MapWatch` and the centre is `controls.centre()`, with no logic lost.
- **`focusSelected`, `focusMap`, and the nullable `under` slot:** right.
  - `focusMap` is stable while picking: `user` is `null` then, since `startPick` empties the point, so `PickCard`'s mount effect runs once.
  - `under` fixes the phone. See finding 6 for 768–1023 px.
- **`sheetOnly` on `useFiltersPanel`:** right. One hook, the sheet at every width on the map, and carried item 7's close rule is unaffected (`wide` is false).
- **`useFailureView` shared:** right. The list's code is unchanged in behaviour.
- **The map's empty state:** right. It uses design issue 18's words.
- **`clearFilters` keeping the view:** right, and found by the test. `clearSearch` and `apply` keep it too, through `filtersOf`.
- **The hand-placed point clamped to the Strip's box:** right. The server's header would refuse a point outside it, and the visitor's point is drawn where it was clamped, so the move is visible.
- **A pin's accessible name not isolated:** acceptable. Bidi isolation in an attribute changes nothing a screen reader reads. The catalogue's comment is wrong (finding 12).
- **Test 46 written after its code:** allowed under §3 with its break. The break is recorded in the report (report only).
- **The two extra tests:** "asks only once when the whole set fits", and the picking card under the map. Both are useful, with no production code only for them.
- **The dark-theme marks:** finding 10.
- **The supervisor's §3 redo (`run2b`):** the report says the failures were in `run2.mjs`, not in the app. The code agrees on the Enter case: Leaflet's marker and the layer's buttons need a real key event with text. Read only.

## The carried items (`0_CARRIED_FROM_103.md`), each seen in the code
1. **Done.**
   - `LocationStatus` is one always-mounted `role="status"`, its Alert `role="none"` (no nested region).
   - Stop and clear call `returnFocus`, set on «الأقرب إليّ» in both views.
   - `NearMeButton` uses `aria-busy` and `aria-disabled` with a loader, not `disabled`, and `press` ignores a press while locating.
   - The test exists.
2. **Done.**
   - `NO_ANSWER_MS = 15_000`. `settle` lets the first of the answer and the wait win.
   - `awaits(asked)` drops a late answer, a clear or a new ask.
   - Tested with the fake clock.
3. **Done.**
   - No match runs `panel.sheet.clear.run` while `applied > 0`, else `clearSearch` (the search off, best match with it, filters and order kept), on the list and on the map alike.
   - `directory.md` says both.
4. **Done** (a test).
   - Test 42's stop step exists.
   - The header gate's break (test 41 red) is from the report only.
5. **Done.** `cardViewOf` takes `byDistance`, which the list sets from `point !== null`. The map passes `false`.
6. **Done.** `usePriceFilter` returns `reset`, which empties both texts and sets the period to `DEFAULT_PERIOD`. The new texts restart the pause, and with no bounds it writes nothing.
7. **Done.** `if (wide && open) setOpen(false)`, tested with `stubScreenWidth`.
8. **Recorded.** It is finding 130's dated line (pop, and a guard's `replace` on a first load).
9. **Done.** Finding 130's *Resolves when* names `FocusLayout`.
10. **Recorded** as finding 133 (Open, with its index line), naming `DIRECTORY_AREAS_MAX` and `AreaFilter`.
11. **Done.** The comment is re-wrapped.
12. **Kept**, with no line added.

The squashed commit's body (items 1–7 and 11) is true to what it holds. The docs commit covers items 8–10.

## Checked and fine
- **The position's privacy, today:**
  - The device's and the hand-placed point are rounded before the store, through `judgePosition` and `pinnedPoint`.
  - The store is module-level and memory-only.
  - `Masaha-Near` goes only on the list's request with `byDistance`.
  - `pinsRequestOf` and `repository.pins` carry no point and no header.
  - Neither `filtersOf` nor `paramsOf` holds a point or `bounds`.
  - Nothing new is logged or stored.
  - The map's user point and «مركّز على موقعي» read the store's rounded point only (`showUser` → `setView(user.point)`).
  - «رجوع» restores the whole state from before (`beforePick`), its sorting included, and is tested (59). Finding 1 is the exception.
  - The privacy line shows only in `locating` and in granted-while-sorting (finding 4 on the map).
- **Weight and loading:**
  - `leaflet.css` is imported only by `LeafletMarkerMap` and `LeafletPointPicker`.
  - `MarkerMap` is `lazy` with a `Skeleton`, and its failed import draws the caller's line.
  - The barrel exports only lazy wrappers, `MapMarkSample` and `markClass` (no Leaflet).
  - CI's `check:build` is green.
  - The viewport is re-asked only while `truncated`, after a 400 ms pause, one request per pause; a change of filter resets the box and the choice.
- **The keyboard:**
  - Marks are `role="button"`, named, `aria-pressed`, `tabindex` 0, and out of the tab order with `aria-hidden` while picking.
  - Enter and Space select. Leaflet's own Enter→click repeats the same id, which is harmless.
  - A `DivIcon` reuses its element, so the focus survives the selected icon (test 54 asserts it).
  - The phone sheet is `modal={false}`, with no scrim, no auto-focus on open or close, and not closed from outside. Escape and «إغلاق» run `focusSelected`.
  - The keys' line is the container's `aria-describedby` while picking.
  - After placing or «رجوع», the focus goes back to «الأقرب إليّ» (`MapView`'s effect).
  - Live regions are not nested.
- **Hand-edited links:**
  - `view` other than `map` is the list.
  - `sort=distance` is dropped, and `relevance` is dropped without `q`.
  - A refused `q` (tashkeel only) is dropped in `filtersOf`, so it never reaches the map's request.
  - `page` is ignored on the map, and the switch writes page 1.
- **The design system, copy and RTL:**
  - The marks, crosshair, user point and tooltip are in `leaflet.css` inside the layer, on semantic tokens only.
  - The features use layout classes only.
  - The map box is `dir="ltr"`, with the zoom at the start and the attribution at the end per language (`MapLayers`).
  - The legend sits at the end of the overlay's top row; the card and «مركّز على موقعي» are at the foot, in the page's direction.
  - Every new string is in both catalogues, and the Arabic `satisfies Catalogue['directory']`.
  - §9's words are written as given, the legend's words from `terms.liveStatuses`.
  - `ViewSwitch` is a single `ToggleGroup` named by its `Field` (`aria-labelledby`).
- **The documents:**
  - `directory.md`: what it does, «The map on the web» (except finding 5's sentence), the pick, five *Web decisions*, the code map and *Web history*.
  - `architecture.md` §6: S12's sentence corrected, *Built:* `MarkerMap`, the caller's failure line.
  - foundation §3: the tree and the `leaflet.css` paragraph.
  - Findings 46, 130 and 133 and the index line.
  - All say only what this PR built, one fact per home (`#PRNUM` aside, as known).
- **Scope and commits:**
  - Only `apps/web` and `docs`.
  - Five atomic commits, the carried ones first, subjects 41–45, each body saying why.
  - The author is the owner, with no tool attribution in any message.
