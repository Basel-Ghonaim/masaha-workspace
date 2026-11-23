# TABLE_NAME — report (2026-11-23)

## 1. The pull request

- **PR:** [#153](https://github.com/Basel-Ghonaim/masaha/pull/153), `fix/table-name-once`, open and **not merged**.
- **Head:** `ac1d323256f6880540c75609ad87a5a36353cd6d`.
- **State:** CI run 45200049085 succeeded on that head. GitHub says `CLEAN` / `MERGEABLE`. `main` is still `ff9094f2`.
- **Carried from #152:** C1 and C2, named in the description.

## 2. The commits

1. `375226a4` `fix(design-system): name a fitting table once` — N2, its tests, foundation §10 and §12.
2. `ac1d3232` `refactor(design-system): remove TableCaption` — N3.

Ten files, +90 −34. No `fixup!` left, no tool attribution.

## 3. What was run

**Locally, on the head:**

| Check | Result |
|---|---|
| `format:check`, `lint`, `typecheck` | pass |
| `check:classes`, `check:links`, `check:conflicts` | pass |
| `test:unit` | 2,711 passed (384 + 924 + 1,403) |
| `test:component` | 2,167 passed, 350 files |
| Production build, then `check:build` | pass |

**CI, on the head:** every job passed, `test:api` included. CodeRabbit skipped.

**axe-core in headless Chrome** (`masaha_dev`, Arabic and English, light and dark): 12 runs, **no violation**, no page
error.

| Table | Width | Container |
|---|---|---|
| Public page's hours | 390 | fits (356/356): no role, no name, no tab stop |
| Owner's prices | 390 | fits (314/314): **not a group**, no name, no tab stop |
| Owner's prices | 320 | overflows (260/244 Arabic, 298/244 English): **a named `group`**, tab stop |

At 320 the keyboard reached the container in all four combinations, and the ring is drawn whole in the two shots I
opened (Arabic light, English dark). Both servers were stopped by PID, and ports 3320 and 5320 are free. Shots:
`C:\Users\basel\Downloads\table-name-shots\head\`.

**Not run:**

- `test:api` locally, left to CI (N5).
- A real screen reader. The evidence is the rendered roles and names, and axe.
- A desktop width. The change adds no class or style.

## 4. Breaks and tests seen failing

**Failing first:** before the implementation, 5 tests failed, one each in `Table`, `ScrollRegion`, `DataTable`,
`SpaceDetails` and `SpacePricesCard`.

**Each break was made once, seen failing and restored from a backup copy:**

| Break | Failed |
|---|---|
| B1 `Table` stops asking for quiet | 4: `Table`, `DataTable`, `SpaceDetails`, `SpacePricesCard` |
| B2 quiet becomes the default | 5 `ScrollRegion` tests, the new default-group test among them |
| B3 the group never returns on overflow | 3: two `Table`, one `ScrollRegion` |
| B4 `aria-label` kept while quiet | 2: `Table`, `ScrollRegion` |
| B5 `aria-labelledby` kept while quiet | 1: `ScrollRegion` |

N3 removes unused code, so it has no test of its own. `typecheck`, the build and the search prove nothing used it.

## 5. Problems met

- Three tests outside `Table` asserted the old group on a fitting table (`DataTable`, `SpaceDetails`,
  `SpacePricesCard`). Each now asserts the new behaviour: a named table and no group.
- My first PR draft said the shots were reviewed and desktop was checked, before either was true. I opened the shots,
  and changed the desktop line to say it was not opened, before the push.

## 6. Anything unexpected

- The first targeted test run outlasted its 420 s limit and moved to the background, though Vitest itself took 14 s. I
  did not look into the wait.
- `taskkill` reported one PID as not found while stopping the servers: it had already exited with its parent tree. The
  ports were checked free afterwards.
- A `gh --jq` expression failed under PowerShell's quoting. The same check ran correctly in Git Bash.
- **A focused table that shrinks until it fits** loses its role, name and tab stop while it holds the focus. No test
  covers the focus there. The default region already drops its tab stop the same way.

## 7. Early conflict check

No other pull request is open, so there is nothing to check against.

## 8. Departures and decisions

- **Departure (N4):** the plan is short, was not written in plan mode, and the build did not stop after it.
- **Finding 229 is not edited.** It is a record, true as of its date, and documentation rules §1 do not allow this kind
  of change. Foundation §12 owns the current behaviour.
- **The prop** is `quietWhileFits`, optional, default `false`, set only by `Table`.

## Left for the owner

- **`.design-sync/config.json` still has `"TableCaption": null`** in its `componentSrcMap`. It is the only mention left.
  I left it because it is the sync tool's file and outside N3's list. Removing that line is a small follow-up.
- **Merging #153** is the owner's word.
