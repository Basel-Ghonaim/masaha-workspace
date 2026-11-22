# TABLE_SCROLL — report (finding 229, with C1–C2 carried from #150)

## 1. Pull request and head

- **PR:** #152, https://github.com/Basel-Ghonaim/masaha/pull/152. Branch `fix/table-scroll-229`, assigned to the owner, labels `fix`, `area:web`, `area:design-system`, `area:docs`.
- **Head:** `a7c584148f453b8dd682146954649d466055b207`.
- **Status:** CI is all green on that head; `CodeRabbit` was skipped. GitHub shows `CLEAN` / `MERGEABLE`. Nothing has been merged.

## 2. Commits

1. `9ad9dbff chore: carry #150's two notes`
   - **C1:** Finance › Occupancy's doc comment rewrapped at 100 columns, words unchanged. Both of its first lines were over 100 (101 and 123).
   - **C2:** foundation §3's categories table gains Meter, BarChart, Heatmap and Refreshing.
2. `a7c58414 fix(design-system): reach a wide table by keyboard`
   - **`Table`:** now scrolls inside the layer's `ScrollRegion`. It takes exactly one name, `aria-label` or `aria-labelledby` (the type is `ScrollRegionName`, now exported inside the layer), and gives it to both the table and its group. The focus ring is drawn inside the container (`-outline-offset-2`).
   - **Callers:** PricesView and HoursSection pass their caption's words as `aria-label` instead of a hidden caption. `DataTable` and the showcase were already named this way and are unchanged.
   - **Tests:** the Table test is rewritten; the DataTable, SpacePricesCard and SpaceDetails tests are extended.
   - **Docs:** finding 229 recorded and Resolved, with an index line; foundation §10 and §12; a change-log line in each of spaces.md and directory.md. `#PRNUM` was replaced with #152 just before the push.

## 3. What was run

Local, on the head, each heavy command through `heavy.mjs table`:

| Check | Result |
|---|---|
| `format:check`, `check:classes`, `check:links` (2,794 links), `check:conflicts` | clean |
| `lint`, `typecheck` | clean |
| `test:unit` | 29 + 77 + 196 files, 384 + 924 + 1403 tests, all pass |
| `test:component` | 350 files, 2164 tests, all pass |
| Production build (`NODE_ENV=production`) and `check:build` | clean |
| axe-core in headless Chrome | 24 screens, no violation (§3a) |

**CI judged:** every lane plus build, lint and typecheck; `test:api` passed in 5m44s.

**Not run locally:** `test:api`, left to CI as T5 says, because no API code changes. E2E was not run either; it is not part of a Work Item.

### 3a. axe per screen

Every screen was checked in Arabic and English, light and dark, on `masaha_dev`'s demo data (Pal Hub, space 26). No rule was reported on any screen.

| Screen | Width | Rules | Table container |
|---|---|---|---|
| Public space page, hours (guest) | 320 | none | group «ساعات العمل الأسبوعية» / "Weekly opening hours"; 286/286, no tab stop |
| Public space page, hours (guest) | 390 | none | 356/356, no tab stop |
| Owner's profile, «الأسعار المعلنة» | 320 | none | group «الأسعار المعلنة» / "Published prices"; **260/244 (ar), 298/244 (en), tab stop** |
| Owner's profile, «الأسعار المعلنة» | 390 | none | 314/314, no tab stop |
| Customers (`DataTable`) | 390 | none | cards, no table |
| Customers (`DataTable`) | 768 | none | group «زبائن المساحة» / "The space’s customers"; 623/623 |

**Focus ring:** the prices container at 320 was reached by Tab (two presses), in all four language and theme combinations. Its outline is solid 2px at -2px, in the `ring` colour (rgb(26,31,37) light, rgb(247,251,255) dark), and `:focus-visible` matched. It is whole on all four sides. The shots are in `C:\Users\basel\Downloads\table-scroll-shots\branch\`, as `ring-profile-*-320.png` plus each screen's full shot. The script is `scripts/axe.mjs` and its output `scripts/out-branch.json`.

## 4. Breaks, and the tests seen failing

The tests were written against the new code. Each break below was made once, the test seen failing, and the code restored from a `cp` backup.

| # | Break | Failed |
|---|---|---|
| B1 | The group left unnamed | Table "scrolls in a group of the same one name", Table "becomes a tab stop", and the DataTable, SpacePricesCard and SpaceDetails name tests (5) |
| B2 | `tabIndex={0}` always | Table "is no tab stop while it fits" |
| B3 | Never a tab stop | Table "becomes a tab stop once it overflows" |
| B4 | The table left unnamed (only the group named) | 8 tests in Table, DataTable, SpacePricesCard and SpaceDetails |
| B5 | Prices named by `columns.price` | SpacePricesCard |
| B6 | Hours named by `hours.title` | SpaceDetails |
| B7 | Never a tab stop, aimed at the jsdom axe test | only the tab-stop test failed. **The axe test did not fail**: jsdom has no layout, so axe cannot apply `scrollable-region-focusable` there. It stays a general axe check, as in ScrollRegion's own test, and the Chrome pass owns the rule. |
| B8 | Name made optional (`TableProps = ComponentProps<'table'>`) | `tsc`: TS2578, both `@ts-expect-error` directives unused |

## 5. Problems met and how each was solved

- **Docker was not running.** I started Docker Desktop and `npm run db:up`, and `masaha-postgres-1` came up healthy. **Both are still running.**
- **Not enough memory.** The grant script waited 19 tries (about 38 minutes) at 3.4–3.7 GB free. Claude Code then stopped every background task of the session for low machine memory: both dev servers, the queued Chrome run and a watch loop. I stopped the orphaned children by PID (tsx watch 17732, API 24600, vite 13420), checked that the ports were free, and recorded the state in `3_STATUS.md`. After the owner freed memory, I ran the heavy checks before restarting the servers, to keep memory free.
- **A stray `cat > file` waited on stdin** and blocked a shell for 2 minutes. I stopped it and made the edit with the Edit tool instead.
- **Two fixups** went into commit 2 before the push (the Chrome result in finding 229, then #PRNUM → #152), autosquashed on `origin/main`. No `fixup!` is left.

## 6. Anything unexpected

- The jsdom axe test cannot catch the finding's own rule (B7). Only the Chrome pass proves it.
- No table overflows at 390 with the demo data. The prices table overflows only at 320.
- The phone's overlay scrollbar is drawn just inside the ring's bottom edge on the focused prices table. The ring itself is not clipped.
- Killing the background dev servers left their child processes holding 3320 and 5320, as the "stop dev server" note warns. Both times they were stopped by PID, and the ports were checked free at the end.

## 7. Early conflict check

`gh pr list --state open` shows only #152. There are no other open PRs, so there is nothing to merge-tree against.

## 8. Differences from the prompt

- **Prices checked on the owner's profile, not the public page.** The public page draws its prices as a grid (directory.md), not a `Table`. The prices table that fails axe is on the owner's profile, and also on Packages & prices and the admin's editor. So the Chrome pass checks the public page for the hours and the profile for the prices. Finding 229's evidence says "the owner's space profile" accordingly.
- **`DataTable` checked at 768 as well as 390.** At 390 it draws cards and no table, so 768 was added to check its table.
- **Ring captured at 320, not 390.** It can only be captured on an overflowing table, and none overflows at 390.
- **C1 rewrapped two lines, not one.** The comment's first line was also over 100 (101), so the whole comment was rewrapped with its words unchanged.

## Decisions taken (from `2_PLAN.md`)

- **Reuse `ScrollRegion`** rather than share its measuring. One component owns the rule, and its tests already prove the measuring.
- **One required name, given to both the table and its group.** The caller writes the words once, and the type keeps a table from going unnamed.
  - Rejected: moving the name to the group alone, which would leave tables unnamed in table navigation and break about 20 tests.
  - Rejected: labelling the group by the caption's id, which needs context wiring and leaves the group unnamed when there is no caption.
  - Cost: a screen reader may say the name for the group and again for the table. This is the common pattern for a scrolling table.
- **The ring inset,** because both frames around a table clip what overflows them.
- **`TableCaption` stays exported** and unchanged.

## Left and recorded

- Nothing outside scope was changed.
- `TableCaption` is now used by no production caller (only a visible caption would use it). It is noted here and not removed.
- Docker Desktop and the database container are still running from this session.
