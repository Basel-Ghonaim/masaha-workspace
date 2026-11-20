# AXE_FIXES — the report (finding 224)

## 1. The pull request and its head

**PR #150** — https://github.com/Basel-Ghonaim/masaha/pull/150 — `fix/axe-224`, head
**`97afb7aec35ec3abbb754b7d876535fc3ae54354`**. CI passed on that head (every job: build, check:classes, check:conflicts,
check:links, format:check, lint, test:api 5m41s, test:component 5m49s, test:unit, typecheck; CodeRabbit skipped);
GitHub shows **`CLEAN`**. Labels `fix`, `area:web`, `area:design-system`, `area:docs`; assigned to the owner. Not merged.

## 2. The commits

| SHA | Subject (chars) | What |
|---|---|---|
| `c2e001f4` | `feat(design-system): add ScrollRegion` (37) | the component, its `index.ts` and root export, its 6 tests, the showcase section, registry entry and fixtures (ar, en), foundation §3, §10, §12 and its date |
| `b5236f45` | `fix(web): let the keyboard scroll two strips` (44) | `PhotosView` (the phone row in `ScrollRegion`, the `ul` `w-max` and unnamed), `OccupancyTab` (the heatmap alone in it, named by the heading; `CardContent` no longer scrolls), their tests, the spaces and finance *Web history* lines and dates |
| `97afb7ae` | `fix(map): keep the mark's tooltip for the eye` (45) | `LeafletMarkerMap` (the tooltip's `add` handler sets `aria-hidden`; a `MutationObserver` removes the mark's `aria-describedby`), 2 tests, architecture §6's two lines and date, finding 224 Resolved and the index |

Each has a body saying why; no attribution; no `fixup!`. `#PRNUM` was replaced with `#150` in each commit's tree
(`filter-branch --tree-filter`) just before the push; a diff of each commit before and after shows no other change.
**19 files** (the plan's table listed 19 and its text said 18 — a miscount in the plan).

## 3. What was run, and what was not

On `5afba618` (the head before the `#150` substitution, which then changed only that number in five documents;
`format:check` and `check:links` ran again after it). Heavy runs through the grant script, one at a time.

| Check | Result |
|---|---|
| `format:check` | clean |
| `check:classes` | clean, 1994 files |
| `check:links` | 2788 links in 264 documents and 2695 source files |
| `check:conflicts` | none |
| `lint` | clean |
| `typecheck` | clean |
| `test:unit` | 29 / 77 / 196 files; 384 / 924 / 1403 tests — passed |
| `test:component` | 350 files, 2160 tests — passed |
| `build` (`NODE_ENV=production`) | passed (waited ~10 min on the grant script for 4 GB free) |
| `check:build` | passed (no showcase, no dashboard or heavy library in the first download) |
| **`test:api`** | **not run locally** — no API code; the owner's allowance (X6). CI passed it. |

No run was killed for memory.

### The Chrome pass (X4)

`scripts/axe.mjs` (task folder): headless Chrome over CDP with Node's own `WebSocket`; the API (3320) and the web (5320)
on `masaha_dev`'s demo set; signed in as `demo-owner@example.com` by `POST /api/v1/auth/login` from the page on 5320
(the password read from `apps/api/.env`, never printed; no rate-limit row needed clearing); language and theme set in
`localStorage`, checked on `<html>`; `node_modules/axe-core/axe.min.js` (4.13.0) injected, `axe.run(document)`. The
owner's space is **26, with 4 photos** (3 in the phone row) — the row fits exactly at 390 (316 of 316 px), so the
photos were also run at **320**, where it overflows (304 of 246). No photo was added. Run on `main` first
(`out-main.json`, `out-main-map.json`), then on the branch (`out-branch.json`, `out-branch-rings.json`).

Violations (rule, nodes) per screen; every variant listed is 2 themes × 2 languages unless said:

| Screen | `main` | Branch |
|---|---|---|
| Map, a mark chosen — 390 | `aria-tooltip-name` (1), all 4 | none, all 4 |
| Map, a mark chosen — 1440 | `aria-tooltip-name` (1), all 4 | none, all 4 |
| Map, another mark hovered — 390 / 1440 | `aria-tooltip-name` (2), all 8 | none, all 8 |
| Finance › Occupancy — 390 | `scrollable-region-focusable` (1, the card content), all 4 | none, all 4 |
| Finance › Occupancy — 1440 | none | none |
| Profile «الصور» — 390 | none | none |
| Profile «الصور» — 1440 | none | none |
| Profile «الصور» — 320 | `scrollable-region-focusable` (2: the photos' `ul`, the prices table's `div[data-slot="table-container"]`), 3 of 4 — en/dark timed out loading the photos on `main`'s run | `scrollable-region-focusable` (1: **the prices table's container only**), all 4 |

No other rule on any run; no page error. On the branch's map runs every `.map-tooltip` has `aria-hidden="true"` and no
mark carries `aria-describedby` (on `main`: the tooltip `role="tooltip"`, not hidden; 1 mark described when chosen, 2
when another is hovered). The strips' tab stops: Occupancy `tabindex="0"` at 390 (576 over 316), none at 1440 (fits);
photos none at 390 (fits), `tabindex="0"` at 320.

**Focus rings** (Tab pressed until the strip had the focus — 2 presses for the photos, 7 for Occupancy;
`:focus-visible`, `outline: solid 2px`, `ring` — `rgb(26,31,37)` light, `rgb(247,251,255)` dark): photos at 320 ar
light / ar dark / en light, Occupancy at 390 ar light / ar dark / en light — each ring whole on its four sides, not
clipped (read from the shots).

Shots: `C:\Users\basel\Downloads\axe-fixes-shots\` — `main\` and `main-map\` (baseline), `branch\` (each strip screen at
390 and 320, the map with a mark chosen at 390 and 1440, both themes and languages), `branch-rings\` (the rings and the
strip screens again). Never in the repository.

Servers stopped by PID after each pass; 3320 and 5320 checked free (the API's `tsx watch` stayed alive once after its
port's process died and was stopped by its own PID).

## 4. The breaks, and the tests seen failing first

Each made once, the test file run in its lane, then restored from a backup copy (`breaks-log.md` in the task folder).

- **`ScrollRegion.component.test.tsx`** (6): no `role="group"` → 4 fail; `tabIndex={0}` always → 2 (fits; fits
  again); never measured → 1 (becomes a tab stop); comparison reversed → 1; children not observed → 1 (watches its
  content); both names optional → `typecheck` fails, TS2578 on the two `@ts-expect-error` lines.
- **`PhotosSection.component.test.tsx`**: the `ul`'s `aria-label` back → the phone test fails; the row in a plain
  `div` → fails (no group).
- **`OccupancyTab.component.test.tsx`**: the heatmap in a plain `div` → fails (no group *Peak hours*); the empty state
  in a `ScrollRegion` too → fails.
- **`MarkerMap.component.test.tsx`**: both new tests written first and **seen failing on `main`'s code** (the tooltip
  not `aria-hidden`). Then: the tooltip's handler dropped → 2 fail (at the `aria-hidden` assertion, before axe); hidden
  only when permanent → the passing test fails; the observer not started (the one removal in the effect kept) → the
  passing test fails; no removal at all → 2 fail.

## 5. Problems met, and how each was solved

1. **The map's first baseline never chose a mark** (8 runs timed out): the script clicked the first `.map-mark`,
   which was outside the map's box or under its legend. It now clicks a mark whose centre is inside the map's box and
   is the topmost element there (`elementFromPoint`); the map was rerun alone on `main` (`main-map`).
2. **The ring shots were cut from the wrong place:** `Page.captureScreenshot`'s clip is in page coordinates; the
   scroll offset is now added. Rerun (`branch-rings`); the bad shots were deleted.
3. **The session ended mid-run** (the machine restarted overnight): Docker Desktop and `masaha-postgres-1` were down,
   the API could not connect, and the grant script's `heavy-slot-1` stayed taken by my cut run. I checked no process
   held it, removed it with a `CLEAR` line in `heavy-grants.log`, started Docker Desktop and the container, and
   restarted the servers.
4. **The Arabic of the photos' name:** the plan said «الصور الأخرى»; the catalogue's is «باقي الصور». The spaces history
   line uses the catalogue's.
5. A lint error in the new test (`no-unnecessary-type-assertion` on the observer stub's `this`), fixed before commit 1.

## 6. Anything that behaved unexpectedly

- **A second `scrollable-region-focusable` at 320**: the profile's «الأسعار المعلنة» table container
  (`div[data-slot="table-container"]`, the layer's `Table`) scrolls with nothing focusable, on `main` too. Not one of
  finding 224's places (its *Resolves when* names those screens, measured at 390), so not fixed; the owner may want a
  finding — `ScrollRegion` would serve it.
- **Leaflet sets `aria-describedby` after its own events and never removes it** (confirmed by the break: a single
  removal in the effect is undone by the next focus).
- `main`'s run of the photos at 320 in English/dark timed out loading the photos; the branch's four runs loaded.
- Claude Code stopped my background CI watcher for low memory; CI was then read with a bounded foreground loop.
- An `npm install -g` process I did not start was running when the session resumed; I did not touch it.
- **Recorded, not fixed** (as planned): foundation §3's category table lags §12 — `display` lacks `Meter`, `data`
  lacks `BarChart` and `Heatmap`, `feedback` lacks `Refreshing`.

## 7. Early conflict check

`gh pr list --state open`: only #150. No other open pull request to check.

## 8. Departures from the prompt, and decisions taken

- **No plan mode** for the plan (stated in `2_PLAN.md`): the prompt asked for the plan saved and a stop.
- **The finding's resolution states the Chrome results,** so the branch's Chrome pass ran before commit 3 was made,
  and the full local verification after it (the order of Phase 2's §2 and §3 swapped; both on the final code).
- **The photos also at 320** (the prompt's fallback): space 26, 4 photos, as said above.
- **The Chrome script also hovers a second mark** (a passing tooltip), beyond the prompt's "a mark selected".
- Ring shots for English: one theme (light) per strip, as the plan said ("Arabic, and English once").
- The approved decisions as built: the `MutationObserver` (§5.1), `ScrollRegion`'s name kept with its doc comment
  saying it is a group, `w-max` on the photo `ul`, no `ref`, architecture §6's two lines.

**Stopped. Not merged.** The supervisor's own Chrome pass (X4) and the owner's word remain.
