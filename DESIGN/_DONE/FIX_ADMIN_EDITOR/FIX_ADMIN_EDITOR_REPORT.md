# Design fix 2a: the admin's space editor (report)

Worker: the design-fix worker · worktree `C:\Users\basel\masaha-design` · branch `design/admin-editor`
PR [#61](https://github.com/Basel-Ghonaim/masaha/pull/61) · 2026-10-12 · CI green on the pushed head, GitHub shows **CLEAN**

## 1. The pull request and its head

Head `7aa508751c8b621b03b2d30420d29fce854fb1ae`: 8 commits, 14 files, every one inside `docs/design/`, +988 / −219.
Cut from `origin/main` `d7d800e`, which has not moved since. No rebase was needed.

## 2. The commits

| # | Commit | Decisions |
|---|---|---|
| 1 | `34deb33` `docs(design): add the prototype's check scripts` | E8 |
| 2 | `6f0900b` `docs(design): the profile fields as the code built` | AD-005, AD-010 (the #57 catch-up) |
| 3 | `bf7d432` `docs(design): five fact groups and a section nav` | E1, E7 |
| 4 | `dbf28e1` `docs(design): a creation form for a new space` | E2, S1 |
| 5 | `332d8e3` `docs(design): a checklist of what is missing` | E3 |
| 6 | `3b18fa9` `docs(design): hours, prices and contacts` | E4, S2–S4, S7, DI-12, 13, 14, 15 |
| 7 | `e6e22ce` `docs(design): the gallery acts at once` | E6, S5, S10 |
| 8 | `7aa5087` `docs(design): the verified space leads somewhere` | E5, DI-17 |

Subjects are 38–50 characters. There is no tool attribution. `CHANGES.md` › *Batch 2a* has one line per decision.

## 3. What was run, and what was not

| Check | Result |
|---|---|
| `node docs/design/scripts/check-parse.mjs` | 49/49 blocks, 40 pages and the modules, run before every commit |
| `node docs/design/scripts/check-classes.mjs` | 0 new dead classes. Seven known ones are reported: five from fix 1's DI-9 (its `h-28` is gone now), plus the Wordmark's two unstyled markers |
| **Browser matrix** (headless Chrome, scratchpad) | 12 targets × 390/768/1440 × ar/en × light/dark = **144 loads, 0 problems** |
| The quick pass (390 and 1440, both editor pages) | after every commit, as the reply asked |
| `npm run format:check` | passes. It cannot see this item: `.prettierignore` excludes `docs/design/` and `*.md` |
| `npm run check:links` | 1893 links in 107 documents and 990 source files resolve |
| CI on `7aa5087` | every job green (lint, typecheck, build, check:classes, check:links, format:check, the three test lanes) |

Each matrix load checks for:
- no blank render and no console error;
- no horizontal page overflow and **no control cut off past the viewport's edge** (AD-007's actual break: the page never scrolled, the controls were simply clipped);
- no `h2` drawn twice;
- F1's 20 px footer gap;
- one section navigation with exactly one marked section;
- navigation names equal to the card titles, and every chip landing on its anchor.

Each target also has its own assertions:
- the checklist's counts on `?id=white` and `?id=new`;
- «لم تُضف بعد» with no confirm on a missing group;
- the shift error on `?demo=shifterror`;
- «إضافة سعر» disabled at 40;
- one table *or* the cards, never both;
- one submit and two cards on the creation form;
- `?new=1` leading to it;
- `?unlink=focus` naming Ahmad;
- the list's «إضافة مساحة» linking the new page.

**By eye**, at 390, 768 and 1440: every changed section, Arabic and English, light and dark samples. This is where the four layout faults in §5 were found, none of which any assertion named.

**Not run:** the test lanes, `build`, `check:build`, lint and typecheck locally. There is no product code (workflow §2 phase 4's exception), and `docs/design/` is ignored by ESLint (`eslint.config.js:227`). CI ran them anyway.

## 4. The breaks made, and the checks seen failing first

- **The scripts:** `check-parse` failed on a planted unterminated JSX (47/48), and `check-classes` on a planted `zz-dead` class. Both were reverted.
- **The overflow assertion** failed on the old shift rows at 390 before E4 (`cut: … الوردية الصباحية`) and passes since. At 1440 it then caught the first prices table running past its card (1053 px in 836).
- **The class check caught two real dead classes in E4** (`align-top`, `md:pt-7`). Both became layout rules in `masaha.css`.
- **Breaks to the archive's contract:**
  - `Admin space edit.html?new=1` now redirects to `Admin space add.html` (approved: S1);
  - `?demo=fresh` is gone, because staleness now comes from the sample data (S9);
  - `Admin spaces.html?unlink=<id>` names that space's owner (approved: DI-17).
- *Corrected in the review fixes (R4):* this list first said that Golden Hub's and Number One Hub's
  galleries had become empty, as approved in the plan. They had, but it was **not** approved: the
  plan says "no sample data changes". The gallery is now empty only on a new space, and `?id=golden`
  shows its five tiles again.

## 5. Problems met, and how each was solved

1. **Blank screenshots at desktop widths.** A capture beyond the viewport (`captureBeyondViewport` or a clip below the fold) came back blank at 768 and 1440, though not at 390. The first "before" set was blank at those widths. The capture now grows the viewport to the page first. The befores were re-taken from a `git archive origin/main` copy served on 5347, so every before is from the clean tree.
2. **The prices table at 768.** Free-width inputs made it 1053 px in an 836 px card at 1440. Selects truncated their values at 768: «سا», «Everyo», «الوردية الصباحية» cut by 13 px. The fix is a fixed table layout with a `colgroup`, narrower cell padding, and the width moved from the label column (a typed label scrolls inside its box) to the shift column (a chosen name would be hidden). No select value now truncates at 768 in either language, a chosen shift included. This is measured, not just eyeballed.
3. **The hours card on a phone.** The header could not hold the title, «نسخ إلى كل الأيام» and the unsaved badge. Below 768 the action now leads the card's content instead (see §8). Also, the «لا تنطبق» helper listed six days with their ranges; past two days it now names the days only.
4. **The shift's time fields** sat 15 px narrower than its name fields (an artefact of the flex row). They now use the same grid as the names.
5. **The gallery's tile controls** wrapped onto three lines at 390. Now: the arrows and delete on one row, «اجعلها الغلاف» under them.
6. **Shared global scope.** The pages' Babel scripts share one global lexical scope, so the gallery redeclaring `PCard` would have thrown. It takes its card parts locally.
7. **A heredoc failed to parse.** Every edit after that ran from a script file in the scratchpad.
8. **The session ended mid-item** (after commit 6, with E6 written but not committed). On restart the tree was checked, the server restarted, and the work went on from that state. Nothing was lost.

## 6. Anything that behaved unexpectedly

- **One blank of the 40-price frame** (`?demo=pricelimit` at 390) in one matrix run, clean on reruns and in the 144-load matrix. It renders in 4–5 s, well inside the 30 s wait, so the cause is most likely load, not the page. Recorded, not dismissed, as in fix 1.
- **The prototype's map only draws Gaza City** (`data.js` bounds), so a valid coordinate elsewhere in the Strip places a pin outside the drawing. The field still accepts it and the contract's box still checks it. The web's map covers the whole Strip.
- **The full-page captures mark «الصور»** in the side list, because the page fits the stretched viewport and "at the bottom" marks the last section. At a normal viewport the marking follows the scroll.

## 7. The early conflict check

`gh pr list --state open` returns only #61, so there is nothing to check against. The branch descends directly from `origin/main` `d7d800e`.

## 8. Departures from the prompt and the plan

| Departure | Why |
|---|---|
| The plan wrote `?id=new&created=1`; the build uses `?id=new` | The toast comes through the existing hand-off, so `created` did nothing |
| The current section is tracked on scroll, not by `IntersectionObserver` | The same behaviour, simpler, and a chosen chip is marked before its scroll settles |
| Below 768, «نسخ إلى كل الأيام» leads the hours card's content rather than sitting in its header | The header had no room on a phone (§5.3). From 768 it is in the header, as decided |
| The pin hint says «واضغط مرة أخرى لنقله» where #57 says "drag" | The prototype's map can place a pin but not drag one |
| DI-14 removes the prices' stale paragraph | The plan's recommendation, approved: the badge replaces it |
| A second port, 5347 | To serve the clean tree for the re-taken befores. It was stopped, and both ports were checked free |
| `Admin owners.html?unlink=` is not changed | It hard-codes both the owner and the space, more than one expression; the reply leaves it for 2b's A4 |

## 9. What `Owner space profile.html` inherited (E7)

- the «المساحة» section, with the #57 fields: the grouped area, «اختياري», both landmarks, and the coordinates with the pin;
- `h2` titles;
- the chip navigation with the current section marked;
- the hours: «24 ساعة», labelled «من»/«إلى», the shift check and its helper, «نسخ إلى كل الأيام», the 10-shift limit, and 24:00 as an end;
- the contacts: seven types, the carrier, the stored form, and the 20-contact limit;
- the gallery's immediate actions;
- the «لم تُضف بعد» behaviour. It is never shown there, since the owner's sample space misses nothing.

**Not inherited:**
- the prices table: its card still links Packages & prices (batch 5);
- the checklist: not mounted there, as batch 5 decides;
- the stale badge: the page passes no dates;
- capacity stays as it was.

## 10. New design issues (none built)

- **DI-18 · a shift used by a package can still be removed on the owner's profile** *(prototype; for batch 5)*. DI-13 guards the shifts that saved *prices* use. On the owner's page the prices live in Packages & prices, so nothing is published and every shift is removable, though a package, a subscription or a visit may name it (the server answers 409). Better: the owner's editor reads which shifts the space's packages use and applies the same disabled-with-reason.
- **DI-19 · a long shift name truncates in the prices table at 768** *(prototype / web note)*. The columns now fit the sample's names in both languages. A name near the contract's 40 characters will still be cut in the select at 768 (it is whole when opened). Better: a `title` with the full name on the trigger. Or the web might switch to cards below `lg` if that reads better at 768.
- **DI-20 · «كل قسم يُحفظ وحده» on the unverified Alert and the owner's intro line** *(prototype)*. Both were written before the gallery lost its save. They are still true of the sections, but not of the photos, which save as each act happens. Better: «كل قسم يُحفظ وحده، والصور فور كل تغيير».

## 11. Owner's additions

None were asked for while the work ran.

## 12. Review focus: what no check exercises

- A screen reader on the chips' `aria-current`, the checklist's links and the photo live region; real keyboard focus.
- Touch scrolling of the chips row, and the current section at a boundary.
- Real photos of real sizes: the 413/415 paths were driven with generated files.
- The prototype's contact normaliser against `@masaha/shared`'s rules. It only approximates them, for the helper's wording.
- Whether the warning «لم تُضف بعد» beside the success «تمّت» reads as intended in the checklist (A8's colours).

## 13. Review fixes (2026-10-12)

From `PROMPT\FIX_ADMIN_EDITOR_FIXES.md`, R1–R11, all built. *From the owner* was still empty when
the work ran.

### 13.1 The pull request and its head

Head `1a08fcf3bf2cd700c5f11f4643495479b4b6d0c3`. Still 8 commits, the fixes folded into the commits of
their decisions (fixup + autosquash), pushed with `--force-with-lease`. CI is green on the head (10
checks) and GitHub shows **CLEAN**. One "Review fixes" comment was posted. The PR description
carries the final counts.

### 13.2 The commits, and the fixes in each

| Commit | Fixes |
|---|---|
| `e99d232` `docs(design): add the prototype's check scripts` | R9, R10 |
| `4af108b` `docs(design): the profile fields as the code built` | none (its `CHANGES.md` is unchanged) |
| `7f2a1e8` `docs(design): five fact groups and a section nav` | none |
| `14c649c` `docs(design): a creation form for a new space` | R11 (the README's page count) |
| `afba8f9` `docs(design): a checklist of what is missing` | none |
| `e5313d1` `docs(design): hours, prices and contacts` | R1, R2, R3, R7, R11 (the dead code) |
| `65b6dc6` `docs(design): the gallery acts at once` | R4, R6 |
| `1a08fcf` `docs(design): the verified space leads somewhere` | R5, R8 |

What each fix did:
- **R1:** an amount is above zero again, with the base's wording («مبلغ غير صحيح»). An empty one keeps «أدخل مبلغًا».
- **R2:** `useSection`'s save can take the values it saves, so the hours give a new shift its id in the section's state at its first save, and it keeps it.
- **R3:** the days' errors are part of the hours' check.
- **R4:** the gallery is empty only on `?id=new`.
- **R5:** the verified page's hours list the sample shifts, which the editor now shares (`SAMPLE_SHIFTS`).
- **R6:** only uploaded or uploading photos count toward the 10 and take the cover. A refused file takes no place, and files past the room are said in one line. The tile counter starts from the photos there are. «إعادة المحاولة» also waits while the gallery is full, a case R6's fix opened.
- **R7:** `ClockInput` passes a time up only once it is whole and valid, and Enter settles the box, then submits.
- **R8:** no dialog for a space with no owner.
- **R9:** the README and the script's header name the class check's blind spots. The baseline is by file. `check-parse.mjs` says how Babel really loads: the repository's `"type": "module"` makes Node load it as an ES module, which sets `globalThis.Babel`. The `self` line was not needed and is gone.
- **R10:** the baseline holds its final seven classes (eight uses, by file) from E8's commit on. **Why these seven:** five are fix 1's DI-9 classes on pages outside the editor (`-mt-3`, `hover:opacity-90` ×2, `md:max-w-32`, `md:w-44`, `md:w-72`), and two are the Wordmark's unstyled markers of option A (`wm-a`, `wm-word`). The editor's own two dead classes (`md:w-44` in the old hours row, `h-28` on the old photo tile) are dropped in E8's commit. They did nothing, so nothing on screen changes, and the later commits rewrite those lines anyway.
- **R11:** README says 40 pages; `savedOnce` and `out.limit` are gone.

`CHANGES.md`'s rows for E8, E4, E6, E5 and DI-17 now say what their commits hold, each row in its own commit.

### 13.3 What was run

| Check | Result |
|---|---|
| `check-parse.mjs` | 49/49 on the head; **both scripts pass at each of the 8 commits**, with the same 8 known dead uses from E8 on |
| `check-classes.mjs` | 0 new on the head; seen failing on a known class planted in a new file (`md:w-72` in `profile-b.jsx`) |
| Each fix driven in the browser | R1 0 refused · R2 a new shift saved, named by a saved price: its removal refused, and after a second hours save still refused and still named · R3 the save blocked, focus on the day's «إلى» · R7 `18:75` + Enter → `18:59`, saved · R4 five tiles · R6 a GIF plus 12 PNGs on an empty gallery → 1 refused tile, 10 photos, «لم تُضف صورتان», upload stopped, cover on the first photo · R5 the shifts listed · R8 no dialog on golden, «فك ربط أحمد؟» on focus |
| By eye | the price error at 768, the day error at 390, the gallery's note at 390 and 1440, the verified page's shifts at 1440 |
| Browser matrix | 13 targets × 12 = **156 loads, 0 problems**, with new assertions for R4, R5 and R8 |
| `format:check` / `check:links` | pass / 1893 links |
| The history | the final tree after the code fixups is identical to the tree verified before the rebase; each commit differs from its previous version only in the rows of `CHANGES.md` it owns |

**Not run:** the test lanes and the build, as in §3. CI ran them.

### 13.4 Breaks, and checks seen failing first

- The per-file baseline failed on a planted known class in a new file, then passed again.
- R6's first build still let a refused file take one of the free places: a GIF in a batch of 13 left 3 PNGs out instead of 2. The browser drive caught it, and it was fixed before the commit.

### 13.5 Problems met

1. **R10 against the history.** A baseline final at E8 would have failed the class check on commits 1–6, which still used `h-28` and `md:w-44`. Dropping those two dead classes in E8's commit keeps every commit passing. The later commits that rewrite those lines conflicted, as expected, and took their own versions. The gallery commit's version predated R1, so R1 was reapplied there; a diff confirmed it was the only difference.
2. **A wrong resolver for `CHANGES.md`.** The first automatic resolution of the rows' conflicts put every row into every commit. A fixup made at the head carries all the rows as "theirs". The row counts per commit gave it away (39 everywhere). The branch was reset to the verified pre-step head, `2fe0d6b`. The rule became "our rows, plus those this step adds". The counts then matched the originals (27, 28, 30, 31, 32, 36, 37, 39).
3. **The page's beforeunload guard blocks a scripted navigation** while a section is dirty. The test clears it before navigating.

### 13.6 Unexpected

- None beyond §13.5. The automated resolution needed checking against the row counts, which is how its first version was caught.

### 13.7 The early conflict check

`gh pr list --state open` returns only #61. Nothing to check against; `origin/main` is still `d7d800e`.

### 13.8 Departures, including the ones the review named

| Departure | Status |
|---|---|
| **DI-16 was built against the reply:** E4 took a price of 0 (`>= 0`) | not stated in the report before; **fixed (R1)** |
| The duplicate price says «سعر مكرّر: غيّر هذا الحقل», not the plan's «يتكرر سعر بالمدة والفئة نفسيهما» | named by the review; accepted as built |
| DI-12's English label field appears only once the Arabic has a value | named by the review; accepted as built (the contract takes `labelEn` only with `labelAr`) |
| «إعادة المحاولة» waits while the gallery is full | added beyond R6, because R6's counting made a full gallery with a failed tile possible |
| A local branch `backup/admin-editor-pre-fixes` keeps the pre-fix head `7aa5087` | for the owner to delete, as deleting branches is the owner's |

## 14. Review fixes, round 2 (2026-10-12)

From `PROMPT\FIX_ADMIN_EDITOR_FIXES2.md`: the owner's look at `1a08fcf`, with three changes, all built and nothing else.

### 14.1 The pull request and its head

Head `842948b74a2d04908ab3177cb6e9de11ee347989`, still 8 commits, the changes folded (fixup + autosquash) and pushed with `--force-with-lease`. CI is green on the head (10 checks) and GitHub shows **CLEAN**. One "Review fixes, round 2" comment was posted. The PR description's hours and E1 lines say the final state.

### 14.2 The commits, and the changes in each

| Commit | Changes |
|---|---|
| `e6a8328` `docs(design): five fact groups and a section nav` | **O3**: under the admin's amenities, «مرفق ليس في القائمة؟ إدارة قائمة المرافق» → `Admin lookups.html?tab=amenities`. `AmenitiesSection` takes the link from the page, so the owner's page, which sets none, keeps its amenities as they are |
| `7b0a5df` `docs(design): hours, prices and contacts` | **O1**: no «24 ساعة» switch. `allDay`, `rangeText`'s «24 ساعة», the copy's `allDay` and `dayError`'s exception are gone, and a day closing at midnight still ends at 24:00 (DI-15). **O2**: every day shows «مفتوحة» or «مغلقة» beside its switch, the word `aria-hidden`, since the switch keeps its own name |

The other six commits differ from round 1's only where these two carry forward. `CHANGES.md`'s E4 hours row and E1 row say it, and the hours row's missing full stop from round 1 is fixed.

O1's traces were checked:
- the verified page's read-only hours never showed the switch;
- `INDEX.md` has no row or frame for it. The board's "24-hour hours & shifts" frames mean the 24-hour clock of the original design, so they stay.

### 14.3 What was run

| Check | Result |
|---|---|
| Both scripts at each of the 8 commits | pass: 0 new dead uses, 48 or 49 blocks |
| Row counts of `CHANGES.md` per commit | unchanged: 27, 28, 30, 31, 32, 36, 37, 39 |
| The final tree | identical to the tree recorded before the rebase |
| `format:check` / `check:links` | pass / 1893 links |
| Quick browser pass | 26 loads, 0 problems. New assertions: no «24 ساعة» in the hours; every day's state shown; the lookups' link on the admin's editor; no link in the owner's amenities |
| By eye | the hours and the amenities at 390 and 1440, on `Admin space edit.html?id=golden` and `Owner space profile.html` |

**Not run:** the test lanes and the build, as in §3. CI ran them.

### 14.4 Breaks, problems, the unexpected

- **The break:** a frame or link to the 24-hour switch would now find nothing. None exists in `INDEX.md` or the board.
- **Problems:** none. The rebase needed no manual resolution (the `CHANGES.md` resolver of round 1 handled the rows).
- **Unexpected:** nothing.

### 14.5 The early conflict check

One other PR opened during this round: **#62** `feat(users): suspend, role and temporary password` (`feat/admin-users`, head `18e0edc`). `git merge-tree --write-tree 842948b 18e0edc`: **clean**. Its files are in `apps/api/` and `.claude/skills/open-pr/SKILL.md`, none in `docs/design/`.

### 14.6 Departures

None. The O3 link carries a short lead-in, «مرفق ليس في القائمة؟», to say when to follow it. That is a word inside the decision.
