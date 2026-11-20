# Review of #141 (PR-B) — Claude Code, Opus 5.5
Head: 4109534ca08cd31e7e693f5f6fdd96991dfaa4f9 · commits 1 · files 14 · checks: green (10 pass, CodeRabbit skipped; `CLEAN`) · head moved: no
Verdict: mergeable after a fix round

Every read was pinned to the head (`git show`/`git grep`/`git diff origin/main...<HEAD>`). Library behaviour was
read in the installed sources of the same versions (`C:\dev\masaha\app\node_modules`: `@dnd-kit/core` 6.3.1,
`sortable` 10.0.0, `utilities` 3.2.2, `accessibility` 3.1.1; `@radix-ui/react-dismissable-layer`). Nothing
was run.

## Findings (verified defects only, most severe first)

### F1 — should-fix · Escape on a lifted item closes the Sheet around the list
- **Where:** `apps/web/src/shared/design-system/components/fields/Sortable/Sortable.tsx:185-191`; the claim in
  `docs/frontend/design-system/foundation.md:390` («Escape puts it back (and is kept from an overlay around the
  list)») and in the PR's acceptance list; the test at `Sortable.component.test.tsx:105-127`.
- **Seen in the code:** the layer's `Sheet` and `Dialog` are Radix `Dialog`. Radix's `DismissableLayer` listens for
  Escape on `document` **in the capture phase** (`react-dismissable-layer/dist/index.mjs:91-106`:
  `ownerDocument.addEventListener("keydown", handleKeyDown, { capture: true })`, then `if (!event.defaultPrevented)
  onDismiss()`). The Sortable's `preventDefault()` and `stopPropagation()` run later, in React's handler on the
  handle (target/bubble phase), after Radix has already dismissed. The test's "overlay" is a plain
  `<div onKeyDown>`, a React bubble handler, which `stopPropagation` does stop, so the test passes and would never
  catch the real case.
- **Scenario:** PR-C's contacts Sheet (C2, T41). A keyboard user lifts a contact with Space and presses Escape to put
  it back. If the Sheet has no changes, it closes. If it has changes, it asks «تجاهل التغييرات؟». The same happens on
  Escape during a mouse drag: dnd-kit's own Escape listener is on `document` in the bubble phase
  (`core.esm.js:1448`), so Radix runs first there too.
- **Fix:** while an item is lifted (or being dragged), the Sortable listens for `keydown` on `window` in the capture
  phase, which runs before Radix's listener on `document`. On Escape it calls `preventDefault()`, so Radix skips
  `onDismiss`, and it cancels the lift there. The `stopPropagation` comes out. The test should render the list inside
  the layer's open `Sheet`, lift, press Escape, then assert the Sheet is still open and the item is back. That test
  fails at this head. · **Belongs:** a fix round on #141, folded into `4109534c`.

### F2 — should-fix · A lift outlives the focus, and every re-render pulls the focus back to it
- **Where:** `Sortable.tsx:151-155` (the `useLayoutEffect` has no dependency list) and `:169-180` (no blur handling).
- **Seen in the code:** the lift ends only on Space/Enter, Escape, Tab or a change in the item set. A mouse click
  elsewhere does not end it. While it lasts, the effect runs after **every** render of the Sortable and calls
  `handle.focus()` whenever the focus is somewhere else.
- **Scenario:** PR-C's contacts Sheet. A user lifts a row's grip, then clicks a row's value field and types. Each
  keystroke updates the parent's draft, which re-renders the Sortable, which puts the focus back on the grip, so the
  typing is cut after one character. The page also keeps showing the lifted order (`aria-pressed="true"`). If the
  user then lifts another item, the first lift's moves are dropped silently, with no «أُعيدت» said.
- **Fix:** end the lift when the focus leaves the handle for another element. Use a `blur` whose `relatedTarget` is
  an element; a null `relatedTarget` is the node's own DOM move and should be ignored. End it by dropping, as Tab
  does (§4.2). The refocus should run only after the sortable's own steps (keyed on the lift), not after every
  render. The test: lift, focus an input outside the list, re-render the parent, then assert the input keeps the
  focus and nothing is lifted. · **Belongs:** fix round, `4109534c`.

### F3 — should-fix · Space or Enter on a control inside a whole-tile handle lifts the tile
- **Where:** `Sortable.tsx:169-180` (`keyDown` never checks `event.target`); the documented pattern at
  `foundation.md:390` («the whole tile dragged», «a click on a button inside an item stays a click»).
- **Seen in the code:** keydown bubbles from a button inside the element carrying `handleProps` to the handle's
  `onKeyDown`. That handler calls `preventDefault()` on Space or Enter, which cancels the button's activation, and
  lifts the tile. Separately, a `role="button"` with a focusable child is axe's `nested-interactive` violation.
- **Scenario (plausible, PR-C):** P5's delete button on each photo tile, with `handleProps` on the whole tile, as the
  row and deviation 2 suggest. A keyboard user tabs to «حذف» and presses Enter. The tile lifts and the delete dialog
  never opens. T48 (axe in the photos' edit state) would then fail.
- **Fix:** in `keyDown`, return early when `event.target !== event.currentTarget` and nothing is lifted. The
  foundation row should say a control inside an item sits **beside** the handle element, never inside it. The test:
  a button inside a handle, Enter on it, then assert its click fires and nothing is said. · **Belongs:** fix round,
  `4109534c`.

### F4 — should-fix · Escape after moving an item earlier loses the focus
- **Where:** `Sortable.tsx:185-191` together with `:151-155`.
- **Seen in the code:** Escape restores `items`, so React moves the `<li>` nodes back. The comment at `:150`
  acknowledges that moving an element can lose the focus, but the refocus runs only while `lifted !== null`, and
  Escape has just made it null. React's keyed reorder moves the item that went up. Example: lift «بريد» (third),
  press ArrowUp twice so the order is c, a, b, then Escape back to a, b, c. React moves `c`, the focused node, and a
  moved focused node loses the focus (the reason `moveBefore` exists). The focus goes to `body`, or to the Sheet's
  container inside Radix's `FocusScope`. The Escape test moves an item **down**, so the focused node stays put and
  the test passes.
- **Scenario:** any keyboard user who lifts an item, moves it up, and cancels. They lose their place in the list.
- **Fix:** refocus after a cancel too, e.g. a "return the focus to this id" ref set by lift, move and cancel and
  read by the effect. The test: lift the last item, ArrowUp twice, Escape, then assert the handle has the focus. That
  test is jsdom-provable if jsdom applies focus fixup on a move, as the ArrowDown test already relies on (see
  *Not checked*). · **Belongs:** fix round, `4109534c`.

### F5 — should-fix · The showcase's grid sets `touch-action: none`, so a swipe on it never scrolls
- **Where:** `apps/web/src/pages/showcase/sections/fields/SortableSection.tsx:65` (the tile) and `:96` (the
  handle); the claim «a finger after a 250 ms press, so a swipe still scrolls» (`foundation.md:390`, PR summary).
- **Seen in the code:** `touch-none` on the whole tile stops the browser from panning any touch that starts on it.
  dnd-kit's `TouchSensor` does not need it: it adds a non-passive `touchmove` listener (`core.esm.js:1710-1717`) and
  calls `preventDefault` only once the drag has started (`:1560-1562`). The deviation to `MouseSensor` +
  `TouchSensor` was made precisely so a swipe still scrolls, and this class undoes it.
- **Scenario:** the showcase at 360 px. The two-column grid fills the width, and a swipe up on it does not scroll the
  page. The report's touch run checked only that "a quick swipe moves nothing". PR-C's photo grid at 390 px, ten
  photos in two columns, is the same case if it copies the model.
- **Fix:** remove `touch-none` from the tile. A small grip may keep it, but does not need it. The row should say an
  item must not set `touch-action: none`. Re-run EC4 with the swipe scrolling. · **Belongs:** fix round, `4109534c`.

### F6 — should-fix · The items' motion is dnd-kit's own and ignores reduced motion
- **Where:** `Sortable.tsx:301` (`useSortable({ id, disabled, attributes })`, so the default transition applies)
  and `:313` (`transition` inline).
- **Seen in the code:** `useSortable` defaults to `{ duration: 200, easing: 'ease' }` (`sortable.esm.js:377-380`),
  written inline as `transform 200ms ease` while items move aside during a mouse or touch drag. Foundation §5 allows
  150/250 ms with `cubic-bezier(.2, 0, 0, 1)`, «off under `prefers-reduced-motion`». The layer turns motion off
  through `--duration-*` (`tokens/primitives.css:118-123`), which this inline value never reads.
- **Scenario:** a user with reduced motion drags a photo, and the other tiles still slide at 200 ms with an easing
  outside the design system.
- **Fix:** pass `transition: { duration: reduced ? 0 : 250, easing: 'var(--easing-standard)' }`. dnd-kit writes
  `${duration}ms ${easing}`. Read `reduced` from the layer's `useMediaQuery('(prefers-reduced-motion: reduce)')`.
  · **Belongs:** fix round, `4109534c`.

### F7 — should-fix · A mouse or touch drag overwrites its own «رُفع» before it is said (plausible)
- **Where:** `Sortable.tsx:209-221` (`dragStart` / `dragOver`).
- **Seen in the code:** when a sortable drag starts, the first collision is the active item itself, so dnd-kit fires
  `onDragOver` right after `onDragStart`, from an effect one render later. dnd-kit's own sortable stories skip that
  first `onDragOver` for this reason. Here it replaces «رُفع X، في الموضع 2 من 3» with «نُقل X إلى الموضع 2 من 3»
  in the same assertive region.
- **Scenario:** a screen-reader user dragging by touch or mouse hears "moved to position 2" at the start and never
  hears the lift.
- **Fix:** skip a `dragOver` whose `over.id` equals the last one said, starting from the active id at
  `dragStart`. · **Belongs:** fix round, `4109534c`.

### F8 — should-fix · T28 does not prove that a list ignores the backward arrow
- **Where:** `apps/web/src/shared/design-system/lib/sortableKeys.unit.test.ts:15-18`.
- **Seen in the code:** the list case asserts only `ArrowLeft` in RTL and `ArrowRight` in LTR, which are both the
  **forward** arrow. The `backward` branch's `layout === 'grid' ? … : null` is never exercised for a list.
- **Scenario:** with the break `case backward: return clamp(index - 1);`, `ArrowRight` moves a contact up in an
  Arabic list, and every test stays green.
- **Fix:** add `sortableStep(1, 4, 'ArrowRight', 'list', 'rtl')` and `('ArrowLeft', 'list', 'ltr')` → `null`, and
  see each fail on that break. · **Belongs:** fix round, `4109534c`.

### F9 — should-fix · Foundation §3 says `check:build` verifies the sortable entry; at this head it does not
- **Where:** `docs/frontend/design-system/foundation.md:88` («…and `@shared/design-system/sortable` … Only the pages
  that draw them import these entries, so their libraries stay out of the site's first download, which
  `check:build` verifies»).
- **Seen in the code:** `scripts/libraryChunks.ts` has no `sortable` group (deviation 1), so `check:build` knows
  nothing of dnd-kit until PR-C.
- **Fix:** add "(the sortable list's from the PR whose page first draws it)", or say it in the row, and remove it
  in PR-C. · **Belongs:** fix round, `4109534c`.

### F10 — nit · Every handle is a toggle button "not pressed" at rest
- **Where:** `Sortable.tsx:324`. `aria-pressed` is `false` at rest. dnd-kit sets it to `true` only while dragging
  and leaves it unset otherwise (`core.esm.js:3436`). A screen reader therefore says «… غير مضغوط» on every handle.
- **Fix:** `lifted || isDragging ? true : undefined`. · **Belongs:** fix round, `4109534c`.

### F11 — nit · A new `items` array each render defeats dnd-kit's reference check (plausible)
- **Where:** `Sortable.tsx:142` (`lifted?.order ?? [...items]`) → `:247`.
- **Seen in the code:** `SortableContext` memoises on the prop's reference (`sortable.esm.js:308`) and `useSortable`
  compares `items !== previous.items` (`:531`). Every render, including each `dragOver` announcement, counts as
  "items changed" and sets `transform 0ms linear` on items whose index equals their last new index, so an item
  sliding back can snap into place.
- **Fix:** `lifted?.order ?? items`. · **Belongs:** fix round, `4109534c`.

### F12 — nit · Repeated words go unsaid; a stale lift can return
- The same `held` words twice leave the live region unchanged, so the second refusal is silent
  (`Sortable.tsx:173-175`).
- A lift that ended because the item set changed stays in state (`:141`). If the set changes back, for example a
  photo added and then deleted, it reappears with its old order.
- **Fix:** clear and re-set `said`, or key the region, for a repeat. Clear `lift` when its members differ.
  · **Belongs:** fix round, `4109534c`.

## The test matrix rows of this PR (present / missing / weaker · would it fail on its break?)

- **T28 `sortableKeys`** — **weaker** (F8). The RTL/LTR grid arrows, ArrowUp/Down ±1 in both layouts, Home/End and
  the clamp at both ends are present, and each would fail on its break; the author made the "direction ignored"
  break and saw 2 red. Missing: the list's backward arrow. ArrowDown at the last index is not asserted, which is
  acceptable since the clamp is the same code.
- **T28b `Sortable`:**
  - Present:
    - Space lifts and says «2 من 3».
    - ArrowDown moves and says it; the focus stays.
    - Space drops with `onMove` once; an unchanged drop calls nothing.
    - Tab drops.
    - `disabled` says `held` and moves nothing.
    - The role description, instructions and the list's name are the caller's; no Latin text at rest.
    - axe at rest and lifted.
  - **Escape — weaker (F1):** it would fail if `stopPropagation` were removed (that break was seen red), but it would
    never fail on the real break, the Radix overlay around the list.
  - Not proven:
    - Enter as a lift and drop key: `LIFT_KEYS` without `'Enter'` stays green.
    - The focus after Escape (F4).
    - `SILENT`: dnd-kit's English announcements fire only on a pointer drag, which the lane does not perform.
      Removing `SILENT` stays green. This is accepted by the plan (R-2: "the component lane proves the keyboard path
      only"); a `fireEvent` mouse drag past 6 px would close the gap.
- **Lint and entry rows (`layerEntries.unit.test.ts`)** — present. Each package is refused outside the layer, allowed
  inside, and the fourth entry is allowed. Both were seen red (restriction removed: 3 red; entry: red before
  `LAYER_ENTRIES`).
- **§12 check / acceptance 6 (`check:build` holds dnd-kit out of the first download) and the `libraryChunks`
  rows** — moved to PR-C (deviation 1). At this head the build contains no dnd-kit at all, since nothing outside the
  development-only showcase imports `@shared/design-system/sortable` (checked with `git grep`; the main `index.ts`
  does not export it).

## Decisions, ODs, DIs and SDs of this PR (built / departed, judged)

- **P4 / C2 (keyboard and screen reader: pick up, move, drop, each announced, no visible buttons):** built in the
  layer. Space/Enter, the arrows, Home/End and Tab are as in §4.2, and every word comes from props. Defects: F1, F2,
  F4 and F7. F3 matters to P4's tiles.
- **The dependency (approved 2026-11-08; §6):** built.
  - `@dnd-kit/core` ^6.3.1, `sortable` ^10.0.0, `utilities` ^3.2.2 in `apps/web` `dependencies`, with caret ranges.
  - Lockfile peers: `react >=16.8.0`, `react-dom >=16.8.0`, sortable's `@dnd-kit/core ^6.3.0`, so React 19 is in
    range. The versions are within §6's 6.3.x / 10.0.x / 3.2.x and are 11–24 months old.
  - `@dnd-kit/accessibility` 3.1.1 comes transitively and is covered by `@dnd-kit/*`.
- **SD3 (the layer's own keyboard mode, by index):** built. There is no `KeyboardSensor`, and `listeners` holds only
  `onMouseDown` / `onTouchStart`.
- **§4.2 activation constraints:** mouse 6 px and touch 250 ms / 5 px, both built. The showcase undoes the touch
  constraint's purpose (F5).
- **EC3:** built and confirmed in dnd-kit's source:
  - `announce(undefined)` is ignored (`useAnnouncement`).
  - `HiddenText` carries the caller's instructions.
  - `attributes.roleDescription` replaces «sortable».
- **OD1 (a):** respected. This PR is the second of three and touches no file of #140.
- **Lint (b) for `@dnd-kit/*`:** built.
- **§8 component API:** departed in two points, both judged below. `className` was also added, which is sound.
- DI-1…8, SD1–2 and SD4–7 belong to other PRs; nothing of them is here.

## The report's deviations, judged

1. **The `sortable` chunk moves to PR-C:** sound. `libraryProblems` fails for a `LIBRARY_CHUNKS` name with no chunk,
   and this head has no importer. PR-C now owes the group, its unit rows, the chunk's measured size (EC2) and
   architecture.md's heavy-library lines.
2. **`handleProps` only, with the layer drawing the `<li>`:** acceptable. A single ref on the moving node is cleaner.
   The whole-tile use needs F3's guard and the row's "controls beside the handle".
3. **`words.roleDescription`:** sound (EC3).
4. **`MouseSensor` + `TouchSensor` instead of `PointerSensor`:** sound. A pointer sensor with a 6 px distance would
   start a drag on a finger's swipe. It is undone in the showcase by `touch-none` (F5).
5. **`EllipsisVerticalIcon` as the showcase's grip:** acceptable (development-only; GripVertical comes with PR-C).
6. **EC2's size given as an upper bound from unminified ESM:** acceptable as a consequence of deviation 1. The built
   chunk size is owed in PR-C.
7. **EC4's "a delete tap stays a click" deferred to PR-C:** acceptable, but the swipe-scroll half of EC4 was not
   shown (F5).

## Documents

- `foundation.md` §3 is updated: the tree, the category row, the public surface and enforcement (b). §12's row is
  updated, and Last Updated is 2026-11-10.
- False as written:
  - «kept from an overlay around the list» (F1).
  - «so a swipe still scrolls», as the showcase models it (F5).
  - §3's «which `check:build` verifies» for the sortable entry (F9).
  - The PR description repeats the first two.
- Owed in PR-C, not here: `docs/frontend/architecture.md:163` and `:167` (the heavy libraries and their chunks) gain
  `sortable` together with the `libraryChunks` group.
- No deferred document's trigger is met. A new dependency is not a §7 trigger beyond foundation (§3: "every wrapped
  library is added to (b) in the same PR", which is done).

## Scope and commits

- One commit, `4109534c` `feat(design-system): add a sortable list`, exactly §14's B1. It is under 50 characters,
  its body explains why, and it has no tool attribution.
- 14 files, all in §8's PR-B list, except `libraryChunks.ts` and its test, which moved (deviation 1).
- No file of #140 or PR-C. Nothing on *Not in v1*. No hardcoded user-facing text in the layer: every word is a prop,
  and the showcase's words come from fixtures in both languages.
- Labels are `feat`, `area:web`, `area:design-system`, `area:docs`; the PR is assigned to the owner.
- No finding is needed (217 stays free): every defect above belongs to this PR's fix round.

## Not checked, and why

- Nothing was run (reviewer rules): no lanes, build, showcase or browser. F4's focus loss rests on the DOM's
  focus-fixup on a moved node and React's keyed-move order, read but not observed.
- Whether jsdom applies focus fixup on a moved node is unverified. If it does not, the ArrowDown test's `toHaveFocus`
  does not prove the refocus effect. The author's breaks did not include removing that effect.
- F7's effect on real speech, F11's visual snap, a real phone's swipe (F5) and a real screen reader were not
  observed (Review Focus §13).
- The screenshots in `Downloads\wi141-shots` were not opened.
