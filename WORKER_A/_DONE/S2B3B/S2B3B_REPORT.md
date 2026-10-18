# S2b-3b — Add a space, with its pin on the map · Report

Worker A · branch `feat/admin-add-space` · 2026-10-10

## 1. The pull request and its head

- **PR #57:** https://github.com/Basel-Ghonaim/masaha/pull/57, `feat(spaces): add a space with its map pin`.
- **Labels:** `feat`, `area:web`, `area:design-system`, `area:ci`, `area:docs`. Assigned to the owner. Not merged.
- **Head:** `36507590ff1783bb988883707318121c62b4a5ad`, rebased on `main` at `49cd088` after #56 merged.
- **State:** CI green on that head (build, check:classes, format:check, lint, test:api, test:component, test:unit, typecheck); GitHub shows `CLEAN`.

## 2. The commits

1. `df998c9` fix(design-system): keep the data table off the site
2. `a5ba2ac` feat(map): add a point picker on OpenStreetMap
3. `9808044` feat(forms): let a form prepare its values
4. `26d7c10` feat(lookups): add the area field
5. `3650759` feat(spaces): add a space with its map pin

## 3. What was run, and what was not

Every lane ran once on `774056e`, one at a time. That head's code is identical to the pushed head's: since then, only documents changed (see below).

| Check | Result |
|---|---|
| `test:unit` | 158 + 622 + 718 passed |
| `test:component` | 784 passed, 123 files |
| `test:api` | 534 passed, 33 files |
| `NODE_ENV=production npm run build`, then `check:build` | passes: no showcase, no dashboard code, no data-table or leaflet, nor Leaflet's stylesheet, in the first download |
| `lint`, `typecheck`, `check:classes`, `format:check` | clean |
| Links of the changed documents (scratchpad script) | all resolve |

The changes after `774056e`, all documents:
- `46ac4f2` changed only the PR number the two capability documents cite (#56 → #57);
- the rebase on `main` resolved a conflict in the findings index (§7).

On those heads, `format:check` and the link check ran again (workflow §9's fast path), and CI ran every lane on the pushed head.

### The manifest (the site's first download)

| | Script | Stylesheet | TanStack Table | Leaflet |
|---|---|---|---|---|
| `main` (`bcb2e04`) | 824,828 B | 78,368 B | in `api-*.js` | — |
| commit 1 | 783,964 B | 78,368 B | its own lazy `data-table` chunk, 37 kB | — |
| head | 790,176 B | 78,754 B | lazy | its own lazy `leaflet` chunk, 153 kB; its stylesheet (16.6 kB) belongs to `LeafletPointPicker`'s lazy chunk |

The 6 kB growth from commit 1 to the head is mostly the new catalogue lines, which are in the build by design. The dashboard's chunk imports only the small `map` wrapper.

### The real run in a browser

Headless Chrome over CDP, with real mouse events on the map, against the API on 3320 and the web on 5320. Signing in made the interface Arabic, the account's language.
- **A click** placed the pin at 31.44148, 34.39545, named «الدبوس عند …».
- **A drag** moved it to 31.37005, 34.56024.
- **The first space** went back to the list with «أُضيفت Map Click Hub …».
- **The second** was placed by pasting `31.5317, 34.4669`, and saved.
- **Outside the Strip:** `32.0853, 34.7818` was refused on its field («هذه النقطة خارج قطاع غزة»), with the focus on it, and nothing was sent.
- **Tiles blocked** (`Network.setBlockedURLs` on `tile.openstreetmap.org`): «لم تُحمَّل الخريطة. أدخل الإحداثيات بدلًا منها.» showed, and the form still sent, back to the list with its toast.
- **The console** stayed clean.
- **Afterwards:** the servers were stopped, and ports 3320 and 5320 checked free.

### Screenshots

32 shots in `C:\Users\basel\Downloads\s2b3b-shots`, not committed:
- **The empty form** in all eight combinations of RTL and LTR, light and dark, phone and desktop.
- **The other states** in four of them (desktop RTL light, desktop LTR dark, phone RTL dark, phone LTR light): the list with "Add space", the field errors, the map with its pin and coordinates, coordinates outside the Strip, the toast on the list, and the failed tiles.

### Not run

- **E2E:** the lane does not exist yet.
- **The lazy chunk failing offline:** not provoked in a browser. In development, Vite serves modules, not the built chunk. The fallback is one `catch` in `PointPicker`'s `lazy` that renders the same line as failed tiles.
- **Every lane again after `774056e`:** not run, because only documents changed. CI ran them on the pushed head.

## 4. The breaks made, and the tests seen failing first

Every new test was seen red before its code existed, as a missing module or function, or a failed assertion. Where the code came first, the test was proven by reverting that code once (testing §3, rule 5). Each break below was made once, seen failing, and restored, with a scratchpad script that rewrites the file and runs the lane.

- **`PointPicker`, 8 breaks**, each failing 1 to 7 tests: the attribution control dropped; the zoom titles left in Leaflet's English; the controls not mirrored; the pin not renamed; the tile error ignored; the map unnamed; the map laid out in the page's direction; a pin drawn with no point.
- **`useAddSpaceForm` and `useCreateSpace`, 8 breaks:** no `prepare` (10 tests); no 409 line; no field lines (5); `onCreated` before the list arrived; no toast; the map writing nothing (2); the pin's refusal not checked again; the area handed nowhere (6).
- **`AddSpaceForm`, 7 breaks:**
  - the landmark, or the Arabic name, not marked "Optional";
  - the coordinates, or the Arabic name, in the page's direction;
  - the pin not given to the map;
  - the area field outside its Field (3);
  - the coordinates without their hint.
- **The area field, 4 breaks:** the group label dropped; names always Arabic; the choice handed back as text; the admin's path read instead of `/lookups`.
- **The page, 2 breaks:** no return to the list; the add page listed in the sidebar (3 tests).
- **The lint rules:** the tests of `data.ts`, `leaflet.css` and the Leaflet restriction failed before the config changed.
- **`check:build`, each break a static import into `app/main.tsx`, seen failing and reverted:**
  - `DataTable` → "_data-table-….js is data-table's chunk in the site's first download."
  - `LeafletPointPicker` → the `leaflet` chunk, and "assets/index-….css holds Leaflet's stylesheet".
  - `leaflet.css` alone → the stylesheet line.
  - A group that matches nothing (S3) → 'No "data-table" chunk in the build'.

## 5. Problems met, and how each was solved

- **The `data-table` chunk and the `space-links` chunk imported each other.** TanStack Table v9 depends on `@tanstack/store`, `@tanstack/react-store` and React's `use-sync-external-store` shim. Left out of the group, they landed in the `space-links` chunk, which the table then imported back.
  - **Solved:** the group takes them too, and the manifest shows the table's chunk importing only `jsx-runtime`.
  - **Checked:** the shim is used only by the table today (Zustand lists it, but the site's Zustand doesn't use it). If the site ever does, `check:build` fails loudly.
- **The `leaflet` group couldn't sit in commit 2.** With S3, a library group with no chunk fails the check, and until the add page imports the picker, Leaflet is in no build. So the group and its test cases moved to commit 5. Commit 2 keeps the stylesheet check and the lint rules.
- **At the design's height (256 px), the map opened at zoom 9,** the Strip a thin sliver, too small to place a pin on.
  - **Solved:** the map is 400 px tall. At that height it opens at zoom 10 on desktop, with whole-zoom (crisp) tiles. On a phone the width binds and it opens at zoom 9, still zoomable.
  - Folded into commit 2 as a fixup.
- **On a phone, the coordinates' example "31.52, 34.45" broke across two lines.** Solved: its space is a no-break space, which the parser still reads.
- **Leaflet's panes stack up to z-index 1000.** `leaflet.css` isolates the map's container, so the map stays under the sticky top bar and the overlays.
- **A blank optional field would read as `too_short`, and an empty pin as `invalid_format`.** This is why S8's `prepare` exists: `toFieldErrors` must read the prepared input. Built as approved.
- **PR #56 was taken by the owner's `docs/small-fixes` PR** while I wrote "#56" in `spaces.md` and `lookups.md`. Corrected to #57 and folded into commits 4 and 5.
- **#56 merged during the item, and the findings index conflicted** (both sides added to *Open*). Rebased on `main`, keeping both: 46 and 48 in *Open*, 45 in *Resolved*.
- **Tooling, in the scratchpad only:**
  - importing the preferences module from the page gave a second instance, so I set the stored keys and reloaded instead;
  - a CDP Enter key didn't submit the sign-in form, so the script clicks its button;
  - the Write tool turns `\u` escapes into literal characters, so the tests name the isolates and the no-break space with `String.fromCodePoint` constants.

## 6. Anything that behaved unexpectedly

- **`npm install` cleared `"dev": true`** on five existing packages in `package-lock.json` (ajv, fast-json-stable-stringify, json-schema-traverse, punycode, uri-js). That is npm's own recalculation, not a dependency of the map. `npm audit` lists high findings in `braces`/`micromatch` (through `eslint-plugin-boundaries`) and `deepmerge-ts` (through Prisma). Both were there before, and neither comes from Leaflet.
- **Leaflet ran in jsdom** better than the plan's *Review Focus* expected. It mounts at zero size, fits its bounds, and creates tile `img` elements, so the tile failure is proven in the component lane, not only by hand.
- **The dev database now holds the spaces made by the real run and the shots.** They are in `masaha_dev`: "Map Click Hub 66154", "Pasted Hub 66154", "Offline Tiles Hub 66154", and eight "Shot Hub …". The owner may delete them from the list's menu.
- **During phase 4,** the API lane's command was moved to the background and the next command was rejected (the session was interrupted). The lane finished green (534 passed). The build, `check:build` and the static checks were then run again on the same head, and passed.

## 7. The early conflict check

- **#56 (`docs/small-fixes`)**, checked before it merged with `git merge-tree --write-tree`: a conflict in `docs/architecture/findings/README.md` only. It has since merged, and this branch was rebased on it (§5).
- **Other open pull requests now:** none. `gh pr list --state open` shows only #57, and `git merge-tree` against `origin/main` is clean.

## 8. Departures from the prompt and the plan

1. **The map is 400 px tall,** not the design's 250 px (§5). The design's map is an illustration; with real tiles, its height made the Strip too small to place a pin on. The owner may ask for another height.
2. **The coordinates' example uses a no-break space** (§5).
3. **The `leaflet` chunk group arrived in commit 5,** not commit 2 (§5).
4. **The `data-table` group also takes TanStack's store and React's shim** (§5), so the table's chunk imports nothing back.
5. **`design-system/index.ts`:** besides dropping the DataTable lines, its header comment now names the second entry. Nothing else in the barrel changed.
6. **Finding 47 is unused.** Neither react-day-picker nor cmdk was in the first download, before or after.
7. **Finding 27 stays open, its file untouched** (the reply's change 1). The study is in the PR description:
   - the dashboard ↔ SpaceLayout cycle is in the manifest before this PR and after it;
   - a group's `test` sees only a module's id, and `$initial` marks only what the entry reaches;
   - a catch-all group would take the site's lazy pages, and pulling the dashboard group's dependencies in would take React.
8. **New Arabic lines** beyond the plan's approved list are in the PR, for approval: the form's labels, the map's name, the hint, the coordinates' helper, the failure's title, the field errors, «تكبير» and «تصغير», the area field's placeholder «اختر المنطقة», and the breadcrumb's name «مسار التنقل».


---

# Review fixes, round 1 (`S2B3B_FIXES.md`) · 2026-10-11

## 1. The pull request and its head

- **PR #57.** Head: `c3cd8cdb6517f9d376f2d18cc4525e6fe827852a`, rebased on `main` at `82cb03a` after #58 merged.
- **State:** CI green on that head (build, check:classes, check:links, format:check, lint, test:api, test:component, test:unit, typecheck); GitHub shows `CLEAN`.
- **The one "Review fixes" comment:** https://github.com/Basel-Ghonaim/masaha/pull/57#issuecomment-6098932598.
- **The description** is updated to the final state.

## 2. The commits

1. `65d2b85` fix(design-system): keep the table off the site (reworded: 47 characters)
2. `ffbe6b1` feat(map): add a point picker on OpenStreetMap
3. `9860908` feat(forms): let a form prepare its values
4. `780ddc7` feat(lookups): add the area field
5. `0ab6977` feat(spaces): add a space with its map pin
6. `c3cd8cd` docs(findings): record finding 47 (new)

Every fix was folded into the commit it corrects (fixup and autosquash). Commit 1 was reworded during the same rebase.

## 3. The fixes, each checked against the code first

None of the items was wrong. In one place the testing differs from the list (item 1).

1. **R1 · the list after a creation** (in commit 5).
   - **The fix:** `useRefreshAdmin` gains `includeInactive`, which only the creation passes. The admin scope is then refreshed with `refetchType: 'all'`, so the spaces list the add page left is fetched and awaited before the toast and `onCreated`. The other writes are unchanged.
   - **The JSDoc** of `useCreateSpace` and `useAddSpaceForm`, and `spaces.md`'s D2 decision, say what holds now.
   - **The test differs from the list:** it mounts no list, and seeds the list's cache with `queryClient.query`, not `setQueryData`. A cache seeded by `setQueryData` has no query function, so refetching it fetches nothing and the test would prove nothing. (`prefetchQuery` would also do, but it is deprecated in this TanStack Query version, and lint refuses it.)
   - **Seen failing** on the old code: the list's GET was never made. The break, back to active lists only, fails it again.
2. **R2 · tile failures** (in commit 2).
   - **The fix:** `services/tileCycle.ts`, a pure verdict per Leaflet load cycle. `loading` resets the count, each `tileerror` counts, and `load` sets the status: failed if any tile of the cycle failed, cleared if none did. `useTileStatus` holds it in a reducer. The `loaded` ref is gone.
   - **A fresh start per map:** the language key moved from the `MapContainer` to a component that holds the status with the map, so a rebuilt map starts fresh.
   - **The unit tests** (6) failed under two breaks: a failure that sticks, and a `loading` that resets nothing. The second exposed a redundancy: `load` had reset the count too, so the reset now lives on `loading` alone, as the fix's wording says.
   - **The component tests:** jsdom lays the map out at zero size, so each load asks for one tile. The tests settle loads by firing that tile's `load` or `error`; a pin moved far away pans the map into a second load. The old `loaded` guard, restored once, fails "says so too when a later load fails, after an earlier one loaded".
   - **By hand** in the browser (§5).
3. **R3:** commit 1's subject is now 47 characters.
4. **R4:** `libraryChunkOf` is removed (commit 1). The test checks which `LIBRARY_CHUNKS` entries' `test` match each module id: exactly the expected one, or none. Its data lines are unchanged, so commit 5's Leaflet cases still apply on top.
5. **R6 · dates:** `architecture.md` and `foundation.md` in commit 2 (which edits both); `overview.md` in commit 5.
6. **R7 · finding 46** is linked from architecture §6's "When it cannot load" (commit 2) and from `spaces.md`'s *Open findings* (commit 5).
7. **R8 · the index's numbering sentence** (commit 2): "A new finding takes the next free number in the range its Work Item's prompt gives, so two workers never take the same one", linking workflow §9 *Conflicts*.
8. **R5 · the lock file:** unchanged, said in one line in the PR description.

## 4. What was run, and what was not

- **Lint and typecheck** on each of the five rewritten commits (a script that checks each out): all clean. Then on the head, which adds the documents-only `docs(findings)`: clean.
- **On the head `c3cd8cd`, once each:**
  - `test:unit`: 158 + 644 + 724 passed;
  - `test:component`: 786 passed;
  - `NODE_ENV=production npm run build`, then `check:build`: no data-table or leaflet, nor Leaflet's stylesheet, in the first download;
  - `check:links`: 1848 links in 142 documents and 977 source files resolve;
  - `format:check`: clean.
- **The real run** (headless Chrome over CDP, API on 3320, web on 5320):
  - **Item 1:** a space added from the list ("Arrival Hub 77491") was already a row in the first frame that showed the list, with its toast.
  - **Item 2:** with 10 tiles loaded, the tile server blocked and the map dragged, the line showed under a part-blank map. Screenshot: `Downloads\s2b3b-shots\review-fixes-tiles-failed-after-a-pan.png`.
  - The console stayed clean; the servers were stopped and the ports checked free.
- **Not run:** `test:api`, as the fixes asked: nothing on the API changed, and CI ran it (pass).

## 5. Problems met, and how each was solved

- **The rebase conflicted with commit 1's fixup in `libraryChunks.unit.test.ts`.** Its context lines held commit 5's Leaflet cases, which don't exist at commit 1. Resolved commit by commit: the new assertions without the Leaflet lines at commit 1, the picker's module in the "other chunks" list at commit 2, and the Leaflet cases back at commit 5. The final tree was compared with the one before the rebase: identical.
- **The rebase on `main` after #58** conflicted in `CLAUDE.md` (twice) and `setup.md`: both PRs edit the *Commands*. Both sides kept, the new `check:links` line and this PR's `check:build` wording. The tree then differed from before only by #58's own changes.
- **The add-space page's routes test timed out under load** (one full component run in four).
  - **Measured:** cold and alone, the page's first lazy load takes 2.5–2.7 s, and the test 4.8–5.0 s. Run alone beside a full lane, it failed three out of three at its first wait.
  - **The fix, in the test** (commit 5): a `beforeAll` imports the add page and the list page, and the values are pasted rather than typed key by key. No timeout raised (finding 28's rule).
  - **The proof:** beside a full lane, three out of three passed in 2.7–2.9 s. Before the list page was also warmed, they took 4.2–5.0 s.

## 6. Anything that behaved unexpectedly

- **Finding 47, an older test that races.** "opens the drawer with the pages and the language, and closes it when a page is chosen" failed in two of the first three full component runs, at about 1.1 s, and passed alone. It reads the top bar's title right after choosing "Customers", before the lazy page has replaced the overview's. Recorded as finding 47 (its own commit), not fixed: it is older than this item, and the item's code doesn't touch it.
- **The 429 test** ("keeps every menu waiting out a 429…", also older) timed out at 5 s once, in the same heavily loaded run as the first two failures. It didn't recur in the three later full runs, so it isn't recorded as a finding.
- **The session was interrupted** between the push and CI's result. CI finished on the same head, all green.
- **The dev database** holds one more space from the real run: "Arrival Hub 77491".

## 7. The early conflict check

- **Open pull requests other than #57:** none (`gh pr list --state open`).
- **#58** merged before the push, and the branch was rebased on it (§5).

## 8. Departures from the fixes list

1. **Item 1's test** seeds the list's cache with `queryClient.query`, not `setQueryData`, for the reason in §3.
2. **Item 2's cycle** resets its count on `loading` alone; `load` gives the verdict. This is the list's wording; my first version reset on both, which a break showed was redundant.
3. **Outside the list:** the routes test's warm-up and pasting (§5), and finding 47 (§6), both found while running the checks the list asked for.
