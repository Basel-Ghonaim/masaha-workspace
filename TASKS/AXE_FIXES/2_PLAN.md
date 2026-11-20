# AXE_FIXES — the plan (finding 224)

> Worker: Claude Code (Opus 5.5), main folder `C:\dev\masaha\app`, on `main` `05822b5e` (clean, equal to
> `origin/main`, checked after `git fetch`). Branch to cut on approval: `fix/axe-224`. Expected PR **#150**
> (`gh pr list --state all --limit 1` → #149 last; the latest Issue is #126).
>
> **An override, stated:** the `write-plan` skill plans in plan mode and saves on the exit's approval. The prompt
> (the owner's instruction, which ranks first) asks for the plan saved to this file and a STOP, with the approval in
> the conversation; so it is written here directly, and nothing is built until the reply approves it.

## 1. Summary

axe-core in Chrome reports two rules on three places. The fix:

- **A new design-system component, `ScrollRegion`** (`display`): a `div` that scrolls sideways, `role="group"`, named
  (a required `aria-label` or `aria-labelledby`), a tab stop **only while its content overflows** (measured by
  `ResizeObserver`), with the layer's one focus style. Its showcase section, its registry entry, its rows in
  foundation §3 and §12, and one line in §10.
- **The photos' phone row** and **«ساعات الذروة»'s heatmap** sit in it, so the keyboard can scroll them
  (`scrollable-region-focusable`).
- **The map's tooltip** is hidden from assistive technology, both of its instances, and the mark loses Leaflet's
  `aria-describedby` to it (`aria-tooltip-name`).
- Finding 224 Resolved; architecture §6 and the two capability documents' histories updated.

## 2. The contract

**Scope.** Finding 224's three places, one PR, web only (X1).

**Acceptance criteria.**
- [ ] `ScrollRegion` exists in `components/display/ScrollRegion/`, its own `index.ts`, exported from the layer's root;
      `role="group"`; typed so exactly one of `aria-label` / `aria-labelledby` is required; `tabIndex={0}` only while
      `scrollWidth > clientWidth`, measured again when it or its direct children resize; the one focus style; no
      built-in words; props extend the `div`'s.
- [ ] Its showcase section and registry entry; foundation §3 (its name in `display`), §10 (one line), §12 (its row).
- [ ] Below 768 px the photos' row is a `ScrollRegion` named «الصور الأخرى» / *The other photos*; the list inside keeps
      its list role with no name of its own; the 768 px grid is unchanged.
- [ ] «ساعات الذروة»: `CardContent` no longer scrolls; the Heatmap alone sits in a `ScrollRegion` named by the card's
      heading; the empty state stays outside it; the card stays the region.
- [ ] Every Leaflet tooltip of a mark (the passing and the permanent instance) is `aria-hidden="true"`; the mark
      carries no `aria-describedby`; its name is unchanged.
- [ ] Component tests as in §9, each seen failing on its break; axe clean in each.
- [ ] axe-core in a real Chrome: no `aria-tooltip-name` and no `scrollable-region-focusable` on the three screens,
      390 and 1440, light and dark, Arabic and English, and no new violation; every rule reported listed per screen.
- [ ] Finding 224 Resolved (status line, a dated resolution naming #150, the index moved to *Resolved*).

**Out of scope.** Any other finding; the gaps in foundation §3's category table other than `ScrollRegion` (recorded in
the report, §6 below); the map's other parts; the API, schema, dependencies, the database (read only, in the Chrome
pass, and a sign-in rate-limit row if one blocks it).

## 3. Reading done

`CLAUDE.md`; `docs/development/workflow.md` (whole); `docs/development/testing.md` (whole);
`docs/architecture/documentation.md` (whole); `docs/frontend/architecture.md` §6; `foundation.md` §3, §10, §11, §12;
the findings README and findings 222, 223, 224; `docs/features/spaces.md` («الصور», *Web history*),
`docs/features/finance.md` (*Occupancy*, *Web decisions*, *Web history*), `docs/features/directory.md` (*The map on
the web*, *Web history*); the owner's decisions X1–X7.

Code: `PhotosView.tsx`, `PhotosSection.tsx`, `PhotosSection.component.test.tsx`; `OccupancyTab.tsx`,
`OccupancyTab.component.test.tsx`; `LeafletMarkerMap.tsx`, `MarkerMap.component.test.tsx`,
`DirectoryMap.component.test.tsx`; `Card.tsx`, `Heatmap.tsx`, `Meter/` (a display component's shape and test);
the showcase's `registry.tsx`, `MeterSection.tsx`, `fixtures.json`; `componentSetup.ts`; `useGoogleButton.ts` (the
repository's `ResizeObserver` precedent); Leaflet 1.9.4 (`leaflet-src.js`: `Tooltip._initLayout` ~10725,
`openTooltip` ~10925, `_setAriaDescribedByOnLayer` ~10998, `Map._layerAdd` ~6880); react-leaflet 5.0.0 and
`@react-leaflet/core` 3.0.0 (`Tooltip.js`, `component.js`, `div-overlay.js`, `events.js`); axe-core 4.13.0 is in
`node_modules`; the model script `CONTACT_RULES/scripts/shots.mjs`.

**What the code showed beyond the prompt:**
1. **The photo `ul` is as wide as its scroller**, its items overflowing it (`flex gap-2`, a block box). A
   `ResizeObserver` on the scroller's children would never see a photo added. The `ul` takes `w-max`, so its box is its
   content's width and its resize is seen.
2. **Leaflet sets `aria-describedby` after its own events.** `openTooltip` calls `openOn(map)` → `_layerAdd` →
   `onAdd` (the container made once per instance, `role="tooltip"`) → the tooltip's `add` event → and only then
   `_setAriaDescribedByOnLayer`. It sets it on every opening (each hover and focus of a passing one) and **never
   removes it on close**, so today a mark keeps pointing at a container no longer in the page. No event comes after
   it, so a handler cannot simply remove it (§4.4).
3. **react-leaflet's `Tooltip` takes `eventHandlers`**, bound on the tooltip instance before it is bound to the mark
   (`useEventHandlers` runs before the lifecycle effect), so even the permanent instance, which opens at once, is
   caught on its first `add`.
4. **The repository's lint (react-hooks 7)** forbids a synchronous `setState` in an effect; a `ResizeObserver`
   callback may set state (`useGoogleButton`'s precedent). A real `ResizeObserver` reports each target once when
   observed, so the first measure needs no effect of its own.
5. architecture §6 says "the marks' tooltips and the attribution's link are not read by browsing": after this item the
   tooltips are not read at all; the line changes (§7).

## 4. The settled decisions, as they will be built

### 4.1 `ScrollRegion` (X2)

`apps/web/src/shared/design-system/components/display/ScrollRegion/ScrollRegion.tsx`, its `index.ts`, exported from
the layer's `index.ts` (alphabetical, beside `Refreshing` / `Separator`).

```ts
type ScrollRegionName =
  | { 'aria-label': string; 'aria-labelledby'?: never }
  | { 'aria-labelledby': string; 'aria-label'?: never };

export type ScrollRegionProps = Omit<
  ComponentProps<'div'>,
  'role' | 'tabIndex' | 'ref' | 'aria-label' | 'aria-labelledby'
> & ScrollRegionName;
```

- Renders `<div data-slot="scroll-region" role="group" tabIndex={overflows ? 0 : undefined} …>`, classes
  `overflow-x-auto focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring` merged with the
  caller's through `cn`.
- `overflows` is state, `false` at first. One effect, run once: a `ResizeObserver` observes the element and each of
  its element children; its callback sets `overflows` to `element.scrollWidth > element.clientWidth`; it disconnects
  on unmount. No synchronous measure (finding 4 of §3).
- `ref` is not taken (no caller needs one; taking it would mean merging two refs). A doc comment says what is
  measured: its own box and its direct children's, so a caller's content sizes itself (as the photos' `w-max`).
- No words; no colour but the layer's `ring`.

**Showcase:** `pages/showcase/sections/display/ScrollRegionSection.tsx`; the registry's entry
`entry('display', 'ScrollRegion', 'scrollRegion', …)` appended at the end (the order built); `fixtures.json`'s
`scrollRegion` in `ar` and `en`: a title, two captions, the region's label and a list of items. Two groups: a row of
eight small `Card`s (`w-40 shrink-0`) that overflows at 360 and 768 (a tab stop), and a row of two that fits (none).

**foundation.md:** §3's `display` row gains `ScrollRegion` (only it); §10 gains one line — *"A region that scrolls
sideways is reached by the keyboard: `ScrollRegion` (`display`) is a named group and a tab stop while its content
overflows."*; §12's `display` table gains its row (named group, the tab stop while it overflows, re-measured on a
resize, the one focus style, no words). Header *Last Updated* → 2026-11-18.

### 4.2 The photos' phone row

`PhotosView.tsx`, the branch below 768 px:

```tsx
<ScrollRegion aria-label={gallery.view.others}>
  <ul className="flex w-max gap-2 pb-1">…unchanged items…</ul>
</ScrollRegion>
```

The list keeps its role and loses its name (the name is said once, by the group). The 768 px grid's `ul` keeps its
`aria-label`, untouched. The doc comment says the row is reached by the keyboard while it overflows.

### 4.3 «ساعات الذروة»

`OccupancyTab.tsx`: `CardContent` loses `overflow-x-auto`; inside it the empty state as today, or
`<ScrollRegion aria-labelledby={headingId}><Heatmap … className="min-w-xl md:min-w-0" /></ScrollRegion>`. The card
keeps `role="region"` and its `aria-labelledby`. The doc comment's "its content scrolling sideways" becomes "its
heatmap scrolling sideways below 768 px, reached by the keyboard".

### 4.4 The map's tooltip (X3)

`LeafletMarkerMap.tsx`, `PlaceMark`:

- The `Tooltip` gets `eventHandlers={TOOLTIP_EVENTS}`, a module constant `{ add: hideTooltip }`, where
  `hideTooltip({ target })` sets `aria-hidden="true"` on `target.getElement()`. It runs on every opening of either
  instance (the `key`'s passing and permanent ones), before Leaflet's `aria-describedby`. A module constant, so a
  render of the caller rebinds nothing (the test "binds no mark's handlers again" stays true).
- The mark's existing effect (run for each new element of the mark) also starts a `MutationObserver` on the element,
  `attributeFilter: ['aria-describedby']`, that removes the attribute whenever Leaflet sets it, and removes any already
  there; it disconnects in the effect's cleanup. The mark's `aria-label`, `aria-pressed`, `tabindex` are unchanged.
- The comment above the `Tooltip` says why: the mark's own name says the space; the tooltip is for the eye.

### 4.5 Documents

- **Finding 224:** status `Resolved`; a *Resolution (2026-11-18, #150)* paragraph: the component, the two places, the
  tooltip, the tests, and the Chrome pass's result (written from the run, never ahead of it). The index: removed from
  *Open*, inserted in *Resolved* between 223 and 225. Same commit as the tooltip (§11).
- **architecture §6** (the mechanism's home): the `MarkerMap` line — "its name shows beside it on hover and always
  beside the selected one" + ", for the eye: hidden from assistive technology, with no description on the mark, since
  the mark's name says it (2026-11-18, #150)"; the `role="application"` line drops "the marks' tooltips and" (they are
  no longer read at all). A platform document: listed in §13 for the approval.
- **spaces.md** *Web history*: `- 2026-11-18, #150 — the phone's row of photos in the layer's ScrollRegion, named «الصور الأخرى», reached by the keyboard while it overflows (finding 224).`
  *Last Updated* → 2026-11-18. «الصور»'s behaviour line is left as is: the visible row is unchanged, and the keyboard
  rule is the layer's (§10), linked by the history line's finding.
- **finance.md** *Web history*: `- 2026-11-18, #150 — «ساعات الذروة»'s heatmap in the layer's ScrollRegion, named by its heading, reached by the keyboard below 768 px (finding 224).`
  *Last Updated* → 2026-11-18.
- **directory.md:** no change. Its line "its name shows beside it" stays true; the tooltip's hiding is `shared/map`'s
  mechanism, whose home is architecture §6 (one home per fact).

`#PRNUM` is written in every one of these, and replaced with the real number just before the push.

## 5. Stronger decisions

1. **How the mark loses `aria-describedby`.** *What:* a `MutationObserver` on the mark's element (planned), against
   overriding Leaflet's private `_setAriaDescribedByOnLayer` on the marker instance (a one-line no-op).
   *Why:* the observer uses the DOM's public contract only and survives a Leaflet upgrade that renames the private
   method; the override is synchronous and smaller but reaches into Leaflet's internals with a cast.
   *Cost:* one observer per mark (up to the 1,000-pin ceiling), each filtered to one attribute of one element; the
   attribute lives for one microtask before it goes. **Recommendation: the observer.**
2. **The photo `ul` takes `w-max`** (not in the prompt). *Why:* without it the content's growth is invisible to the
   `ResizeObserver` (§3, finding 1). *Cost:* none visible: the row already starts at the inline start.
   **Recommendation: take it.**
3. **`ScrollRegion` takes no `ref`.** *Why:* no caller needs one, and a ref would have to be merged with the
   component's own. *Cost:* a future caller that needs one adds the merge then. **Recommendation: as planned.**
4. No rule of the documents is contradicted or weakened. The group of the same name as its card's region (Occupancy)
   is X2's choice (`landmark-unique`); it stays.

## 6. Related findings

Open: 23, 65, 152, 215, 221 — none touches these files or rules: **not folded** (X1: finding 224 alone).

**Recorded, not fixed** (for the report; the prompt gives no finding range, so no finding file is written): foundation
§3's category table lags §12 — `display` lacks `Meter`, `data` lacks `BarChart` and `Heatmap`, `feedback` lacks
`Refreshing`. And Leaflet never removes the `aria-describedby` it sets, which this item's observer makes moot for the
marks.

## 7. The files

Web only; no other open item (no other worker runs), so no file is shared.

| File | Change |
|---|---|
| `apps/web/src/shared/design-system/components/display/ScrollRegion/ScrollRegion.tsx` | new (§4.1) |
| `…/display/ScrollRegion/index.ts` | new |
| `…/display/ScrollRegion/ScrollRegion.component.test.tsx` | new (§9) |
| `apps/web/src/shared/design-system/index.ts` | its export |
| `apps/web/src/pages/showcase/sections/display/ScrollRegionSection.tsx` | new |
| `apps/web/src/pages/showcase/registry.tsx` | its import and entry |
| `apps/web/src/pages/showcase/fixtures.json` | `scrollRegion`, ar and en |
| `docs/frontend/design-system/foundation.md` | §3, §10, §12, header date |
| `apps/web/src/features/spaces/components/photos/PhotosView.tsx` | §4.2 |
| `apps/web/src/features/spaces/components/photos/PhotosSection.component.test.tsx` | §9 |
| `apps/web/src/features/finance/components/OccupancyTab.tsx` | §4.3 |
| `apps/web/src/features/finance/components/OccupancyTab.component.test.tsx` | §9 |
| `docs/features/spaces.md`, `docs/features/finance.md` | a history line each, header date |
| `apps/web/src/shared/map/components/LeafletMarkerMap.tsx` | §4.4 |
| `apps/web/src/shared/map/components/MarkerMap.component.test.tsx` | §9 |
| `docs/frontend/architecture.md` | §6, two lines |
| `docs/architecture/findings/224-the-maps-tooltip-and-two-scrolling-strips-fail-axe.md`, `findings/README.md` | Resolved |

18 files. Task folder only (never committed): `scripts/axe.mjs`, `4_REPORT.md`; shots to
`C:\Users\basel\Downloads\axe-fixes-shots\`.

## 8. Design issues

None. The screens look as they did: the only visible change is the focus ring on a strip given the keyboard's focus,
which is the layer's own.

## 9. Tests — lane, test, break

All in the **component** lane (rendering and focus, testing §1). jsdom has no layout: sizes and `ResizeObserver` are
stubbed in the test (the platform's seam, rule 3); `componentSetup.ts`'s do-nothing stand-in is replaced per test with
`vi.stubGlobal` and restored by `vi.unstubAllGlobals()`.

**`ScrollRegion.component.test.tsx`** (new):
1. *Is a group named by its label, and by the element its `aria-labelledby` names.* `getByRole('group', { name })`
   for each form. **Break:** drop `role="group"` → not found.
2. *Is no tab stop while its content fits.* `scrollWidth` and `clientWidth` stubbed (`vi.spyOn(Element.prototype,
   'scrollWidth', 'get')`, 300 / 300), the stubbed observer's callback run under `act` → no `tabindex`.
   **Break:** `tabIndex={0}` always → fails.
3. *Becomes a tab stop once its content overflows, and leaves the order when it fits again.* Starts fitting; the
   stub changes to 600 / 300 and the observer reports → `tabindex="0"`, and `userEvent.tab()` focuses it; back to
   300 → no `tabindex`. **Break:** the observer not started (no measure) → fails; the comparison reversed → fails.
4. *Watches its own box and its children's.* The stubbed observer records its targets: the element and its child.
   **Break:** observe the element only → fails.
5. *Has no accessibility violations*, overflowing: `axe(container)`.
6. *Its name is required:* a `// @ts-expect-error` render with neither name, and one with both — `typecheck` proves it.
   **Break:** make both optional → `typecheck` fails on the unused directive.

**`PhotosSection.component.test.tsx`** — the phone's test (about line 80) changes: it finds
`getByRole('group', { name: 'The other photos' })`, the `list` within it, asserts the list
`not.toHaveAccessibleName()`, and the same two `src`s. The 1440 test keeps the grid's named list. **Break:** restore
the `ul`'s `aria-label` → the list is named → fails; render the `ul` without `ScrollRegion` → no group → fails.

**`OccupancyTab.component.test.tsx`** — a test (or the third test extended): inside the region *Peak hours* a
`group` named *Peak hours* holds the heatmap (its figure or hidden table found within it); and in the empty-state test,
`queryByRole('group')` within the region is `null`. **Break:** wrap the empty state in the `ScrollRegion` too → fails;
drop the `ScrollRegion` → fails. The existing axe test still runs.

**`MarkerMap.component.test.tsx`** — two tests:
1. *A selected mark's tooltip is hidden from assistive technology and describes nothing; axe-clean.* `selectedId: 2`;
   wait for the `.map-tooltip` holding *Sea Desk*; it has `aria-hidden="true"`; `await waitFor` the mark *Sea Desk —
   No live status* `not.toHaveAttribute('aria-describedby')` (after the tooltip is seen open, so the wait cannot pass
   vacuously); its name unchanged; `axe(container)` clean. **Break:** drop the `add` handler → fails (and axe's
   `aria-tooltip-name` is expected to fail too, noted when seen); drop the observer → the `aria-describedby`
   assertion fails.
2. *A passing tooltip is hidden the same way.* `fireEvent.focus` on *Focus Hub — Available* → its `.map-tooltip`
   appears, `aria-hidden="true"`, no `aria-describedby`. **Break:** hide only when `selected` → fails.

Each break is made once, seen failing in its lane, and restored (reported).

## 10. Review Focus — inputs no test exercises

- Real layout: the strip's overflow at 390 vs 1440, the ring whole and unclipped, RTL scrolling — the Chrome pass.
- A `ScrollRegion` whose direct children are replaced after mount (only the children at mount are observed); neither
  caller does it.
- A sub-pixel overflow (`scrollWidth` is rounded): a 1 px false tab stop is possible in theory.
- A mark whose element Leaflet rebuilds (a new icon on selection): the effect re-runs and observes the new element; a
  passing tooltip's focus listeners on such a rebuilt element are Leaflet's and unchanged.
- A map at the 1,000-pin ceiling: 1,000 observers (cost, not behaviour).

## 11. Commits

Conventional, subject ≤ 50 characters, a body saying why, no attribution, no `fixup!` left; staged by path.

1. `feat(design-system): add ScrollRegion` — the component, its `index.ts`, the root export, its test, the showcase
   section, the registry entry, the fixtures, foundation §3 / §10 / §12.
2. `fix(web): let the keyboard scroll two strips` — `PhotosView`, `OccupancyTab`, their tests, the spaces and finance
   history lines.
3. `fix(map): keep the mark's tooltip for the eye` — `LeafletMarkerMap`, its test, architecture §6, finding 224
   Resolved and the index.

Lint and typecheck on each commit; the lanes once, on the head.

## 12. Verification (Phase 2)

Heavy runs through `node C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs axe <command…>`, from the root, one
at a time; a run killed for memory is retried once, then left to CI and said.

`npm run format:check`, `lint`, `typecheck`, `check:classes`, `check:links`, `check:conflicts`, `test:unit`,
`test:component`; then `NODE_ENV=production npm run build` and `check:build`. **Not run: `test:api`** — no API code;
the owner's allowance (X6); CI runs it, said in the PR's Evidence.

**The Chrome pass (X4)**, `C:\dev\masaha\workspace\TASKS\AXE_FIXES\scripts\axe.mjs`, modelled on `shots.mjs`
(headless Chrome over CDP, Node's own `WebSocket`), run through the grant script:
- **Servers:** the API (`npm run dev -w @masaha/api`, 3320) and the web (`npm run dev`, 5320) in the background, on
  `masaha_dev` with its demo set; their PIDs noted.
- **Which space:** read-only `SELECT`s on `masaha_dev` find the demo owner's space, its photo count, and its closed
  stays in the last four weeks. The thumbnails overflow at 390 with five photos or more (four others at 96 px + 8 px
  gaps exceed the ~326 px inside the card). If the demo owner's space has fewer, the demo directory owner's space with
  the most photos is used (same seeded password), else 320 px; the space and its count are said. No photo is added.
- **Sign-in:** the script reads `SEED_DEMO_PASSWORD` from `apps/api/.env` itself and never prints it; it posts
  `/api/auth/login` from the page (the session's cookie set by the answer), then navigates. A 429: the sign-in
  rate-limit row is deleted in `masaha_dev` only, and said.
- **Language and theme:** set in `localStorage` (`masaha.language`, `masaha.theme`) on the origin before each load;
  the result checked on `<html>`'s `lang`/`dir` and `data-theme`.
- **Screens,** each at 390×844 (mobile) and 1440×900, light and dark, ar and en (8 runs each, 24 in all): the owner's
  profile at «الصور»; Finance › Occupancy with the heatmap drawn; the directory's map (`/spaces?view=map`) with a mark
  chosen by a click, plus one hovered (a passing tooltip). Paths are taken from the app's own links.
- **axe:** `node_modules/axe-core/axe.min.js` injected by `Runtime.evaluate`, `axe.run(document)`; every violation's
  rule id and count recorded per run; the strips' `tabindex` recorded (expected `0` at 390, none where it fits).
  Pass: no `aria-tooltip-name`, no `scrollable-region-focusable`, no rule absent from a run on `main` — the same
  script is run once on `main`'s code first, so a "new" violation is judged against a baseline, not a memory.
- **Focus rings:** at 390, light and dark (Arabic, and English once), Tab pressed (`Input.dispatchKeyEvent`, bounded
  to 60 presses) until `document.activeElement` is the strip; a clipped screenshot with a margin around it, the ring
  checked whole. Shots to `C:\Users\basel\Downloads\axe-fixes-shots\`, curated, never in the repository.
- **After:** the servers and Chrome stopped by PID; `netstat` shows 3320 and 5320 free.

Then `open-pr` (the PR's Evidence: each check, the axe table, the shots' folder, `test:api` left to CI), wait for
`gh pr checks` green on the pushed head and `CLEAN`, then `final-report` to `4_REPORT.md`. Never merge.

## 13. Decisions needed from the owner

1. **Approve this plan** (the contract, the 18 files, the three commits).
2. **architecture §6's two lines** (a platform document): approved with the plan, or left as they are.
3. **§5.1:** the `MutationObserver` (recommended) or the private-method override.

## Proposed alternatives

1. **The tooltip's `aria-describedby`:** the private override instead of the observer — see §5.1; recommended
   against.
2. **The component's name.** `ScrollRegion` keeps axe's and WCAG's term ("scrollable region") though its role is
   `group`; a name like `ScrollStrip` would not suggest `role="region"`. Small; **recommendation: keep `ScrollRegion`**,
   its doc comment saying it is a group, not a region.
3. Otherwise **none**: the overflow-only tab stop and the `group` role (X2) are kept as the supervisor set them.
