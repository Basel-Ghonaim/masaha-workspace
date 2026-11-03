
### The folds

- R1's fixes folded first (two autosquash runs; R1-F2 split over its two homes from saved copies), each after
  `npm run lint` and `npm run typecheck` on the tree; `backup/step10-pre-fold-r1f2` before the split; the tree after
  identical to it.
- R2's and R3's fixes: committed as cumulative stages (`scripts\fixround\stages.py`, each home's part only, the head
  then identical to every saved final file), lint 0 and typecheck 0 on that tree (lint first flagged an unused
  `waitFor` in the R3-F1 test — removed, a sixth fixup), then one `rebase -i --autosquash` with stops after «list every
  space's reports» and «list a user's favourite spaces» for the document pass (`docpass.py`: finding 184's file and
  index line, 167 and 184 in `data-reports.md`'s *Open findings*; 187's index line). `backup/step10-pre-fold-r2r3`
  first. Conflicts, each resolved to that commit's own content plus the fix: `useDecideSheet.ts` (the owner's then the
  admin's description, the stale-status guard kept); the *Open findings* lists and the index (the union, by number);
  at «report wrong information» the space page's test, `SiteLayout.tsx` and `overview.md` (that commit's versions plus
  the report's leaving test, `useGuestIntents`, the R3-F4 line — typecheck 0 and the page's, shell's and report's tests
  28/28 at that commit); at «save a space from its card» the same two files (that commit's versions plus the fix's
  lines, then the favourite's leaving test and the heart's one name — typecheck 0, 33/33 at that commit); at «list a
  user's favourite spaces» `overview.md` (both lines); at the last commit the space page's test (its final version).
- **After:** the tree = `backup/step10-pre-fold-r2r3` + the document pass's 11 lines (3 files); 16 commits, every
  subject unchanged, no `fixup!` left, no `#PRNUM`, no rebase in progress.

### The runs (memory through `scripts\heavy.mjs`)

- While fixing: only the touched test files; lint and typecheck before each fold.
- **Memory:** worker B ran meanwhile. On 2026-10-28 the grant waited 19 tries (15:01–15:40 UTC, 2.6–3.9 GB free); the
  typecheck granted at 15:40 (4.4 GB) was **killed by Claude Code** for critically low system memory (0.7 GB free);
  the slot released by hand and logged; the run paused until the owner said "retry now". Then (6.5 GB free) typecheck 0,
  lint 1 → fixed → 0.
- **On the final head `819e1eea`** (2026-10-29, granted at 4.3–5.2 GB free): `npm run lint` 0 (143 s); `npm run
  typecheck` 0 (47 s); `npm run test:unit -w @masaha/web` "Test Files 157 passed (157) · Tests 1075 passed (1075)";
  `npm run test:component -w @masaha/web` "Test Files 300 passed (300) · Tests 1744 passed (1744)" (377 s);
  `check:links` "2993 links in 242 documents and 2281 source files all resolve."; `check:classes` (1659 files);
  `check:conflicts`; `format:check` — all pass. No API or shared change: `test:api` is CI's.

### Push and CI

- `origin/main` moved to `e3b2f97b` (#130, worker B: `apps/api`, documents; nothing of this PR) — #129 stayed `CLEAN`,
  no rebase.
- `git push --force-with-lease=feat/step10-screens:fcf46637bf84ab2de598abf0f8080bb42f8964f2` → "+ fcf46637...819e1eea
  (forced update)".
- **CI on `819e1eeaa442cf3e871e50fbb0c217a1730dcffa`:** build, lint, typecheck, test:unit, test:component, test:api,
  check:classes, check:links, check:conflicts, format:check — all pass; CodeRabbit skipping. `mergeStateStatus`
  **CLEAN**; 254 files.
- The PR's description gains *Review fixes* (each finding and its commit; findings 184 and 187; R3-F1 as the owner's
  decision on DI-58).

### The commits after the round

`4ebc2785` perf(design-system): serve the calendar on its own (50) · `18db0601` fix(design-system): start a range on
each click (47) · `a23896a7` test(web): pre-bundle the calendar for jsdom (44) · `ddaa3db2` feat(announcements): list
a space's announcements (49) · `220e9a76` feat(announcements): post and edit an announcement (50) · `582c609d`
feat(announcements): end, start or delete one (45) · `f44adca3` feat(announcements): extend after a closure (43) ·
`9bb9e8e8` feat(design-system): add a removable filter tag (47) · `357c9754` feat(data-reports): decide a space's
reports (44) · `34a8dcd8` feat(data-reports): list every space's reports (46) · `1001c70f` feat(data-reports): show a
user's own reports (45) · `7f35b865` feat(data-reports): report wrong information (44) · `59a3d0ba`
feat(design-system): add the heart icon (39) · `454eb88d` feat(favorites): save a space from its card (43) ·
`3a8888d1` feat(favorites): list a user's favourite spaces (47) · `819e1eea` feat(announcements): show a space's
announcements (49).

### Decisions taken without the owner (this round) — none SERIOUS

- **FR-D1 — R1-F2: the dialogs held by the list**, not the openers kept rendered: only the list survives a card that
  leaves its tab (`ANNOUNCEMENT_NOT_STARTED`, 404). *Undo:* move the dialogs back under their openers.
- **FR-D2 — R2-F2: the decided report read from page 1 of «الكل»** (no route reads one report), and «تمت المراجعة» when
  it is not there. *Undo:* drop the read; the guard alone.
- **FR-D3 — R3-F2: the shell signals through `@shared/routing`** (`noteSitePage` / `onGuestLeaving`) rather than
  importing the features: importing `data-reports` in the site's shell would have brought the table library to every
  site visit (finding 180's cost) and slowed the shell's tests. *Undo:* the shell calls each feature's drop.
- **FR-D4 — R1-F4's red seen under `TZ=UTC`** (this machine runs on Gaza's zone, where the test cannot fail; CI runs
  UTC). *Undo:* none needed.
- **FR-D5 — finding numbers 184 and 187** as the round's file named them.

### Leftovers

- Backup branches (local): `backup/step10-pre-review-fix` (`fcf46637`), `backup/step10-pre-fold-r1f2`,
  `backup/step10-pre-fold-r2r3`, and the first round's (named above). `git status --short` clean; no rebase in progress.
- No real run this round (the fixes are proven by their tests); the data stays as it was.
