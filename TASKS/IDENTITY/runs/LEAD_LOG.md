# IDENTITY prod — the lead's log (facts for 4_REPORT_PROD.md)

## Phase 1 (2026-11-12)
- Branch `feat/ink-berry-identity` cut `--no-track` from `origin/main` `f0709d28`. Next numbers read at the start:
  last ADR 0018, last issue/PR #143.
- heavy.mjs adapted to `TASKS\IDENTITY\scripts\heavy.mjs` (≥ 4 GB, two slots, the lead first: a lead waiting leaves
  `heavy-lead-waiting`, lanes do not take a slot while it exists; lead retries every 60 s, lanes 120 s).
- EC3: the test's maths reproduces the trial's figures once the mixes are quantised to 8 bits as painted (fg on dark
  tint 13.011 vs 13.01; mfg 5.496 vs 5.50; fg on the wash light 12.306 vs 12.31, dark 9.905 vs 9.90); unquantised they
  were 0.02–0.03 off. The test quantises (`painted`). Chrome's painted check is in the visual pass.
- EC4: Machado severity 1 on linear RGB reproduces the trial: ink↔red light .346 (.190, .319), dark .329 (.365, .278);
  spark↔red light .191 (protan .220, deutan .184), dark .156 (.154, .158). Kept.
- EC5 (cn part): tailwind-merge keeps border-/bg-/outline-/fill-spark and bg-(--skeleton) in their colour groups
  (`border-input border-spark` → `border-spark`, `border-2 border-spark` kept both).
- C1 `e3a3f6bf feat(design-system): adopt ink and berry identity` (48): primitives, semantic, tailwind, the token test,
  ADR 0019, the map. Red on Sea: `runs\c1-red-tokens.txt` "Tests 66 failed | 128 passed (194)". Green
  `c1-green-tokens.txt` "194 passed". Breaks (`c1-break-*.txt`), all red and restored: t9-transfer 8 failed; t2
  hex-only resolver 29; t7 hover = spark-100 6 (incl. both "hover is not the selected tint"); t8 coral #ef7b62 4; t6
  skeleton n-100 2; t4 scrim 60 % 1 (over #ffffff); t5 paler spark 7; t3 brand left 1; t11 --color-spark 1; t11
  text-spark utility 1; t1 a dark role missing 5. lint 0, typecheck 0.
- EC7 before C6 (C1's head, production build): first download JS 8 chunks, 1,084,364 bytes, gzip 321,778
  (`runs\ec7-before-c6.txt`). check:build 0.
- C6 part 1 `875848e7 feat(design-system): add the logo` (33): Logo.tsx, drawing.ts, index.ts, the test (T16). Red
  with the component removed: "Failed to resolve import ./Logo" (`c6-red-logo-missing.txt`); green 10/10. Breaks
  (`c6-break-*.txt`): name dropped 6 failed; not hidden 2; rtl:-scale-x-100 2; dots fill-primary 2; cropped frame 1;
  all restored. lint 0, typecheck 0 (after two lint fixes before the commit).
- Head `875848e7`: test:unit 1 failed | 1307 passed (web) — `registry.unit.test.ts` "no entry for display/Logo": the
  showcase entry needs the layer's index (a #143 file); it turns green with the rest of C6 after the merge
  (LEAD-D1). api 323/323, shared 921/921. Production build 0, check:build 0, first download unchanged.
- `backup/ink-berry-identity-1` at `875848e7`.
- #143's head moved 29a25054 → 14d3bb6e during Phase 1 (its fix round).
- Lane prompts written: `lanes\LANE_A.md`, `LANE_B.md`, `LANE_C.md` (placeholders `<BASE>`, `<EC1-A>`, `<EC1-C>`).

## Decisions taken without the owner
- LEAD-D1: the showcase registry's known red between C6 part 1 and the merge (above); no committed state of the final
  history is red (the entry folds into C6).
- LEAD-D2: lane C renders the rasters (it owns `public/` and T15); its Chrome batch goes through the grant; no other
  lane runs Chrome; the visual pass starts only after the lanes.
- LEAD-D3: T8's dark tint check covers `sidebar-accent` too (the same mix), beside the plan's `accent`.

## Phase 2
- Wait started (background `wait-143.mjs`, log `runs\wait-143.log`).
- #143 MERGED `f58c12a8` at 10:31 UTC (wait log check 3, 10:32:42). The owner also said so in the conversation.

## Phase 2 — on the merge
- `git rebase origin/main`: no conflict (no commit of mine touched a #143 file). C1 `0d38c255`, C6 `cbf8310e`;
  `backup/ink-berry-identity-2` at `cbf8310e`.
- C1's foundation part (Status, Last Updated, intro, §4 tiers/palette/`skeleton` row, §5 intro/roles/values/verified/
  usage rules, §15 row 1 and the closing line) applied by `post_docs.py c1` (dry-run beforehand on #143's files), one
  claim narrowed ("the logo's files write by hand"; the icons' clause is lane C's C8 fold). Fixup → C1.
- C6's rest: index export; `SidebarHeader({ mark, logo })`; T17 (3 tests) red before the code: "2 failed | 12
  passed (14)" (`c6-t17-red.txt`: the desktop and drawer tests; the rail one passes on the old code by design); green
  24/24 with Logo; break (branch swapped) "3 failed | 11 passed (14)", restored; AdminLayout passes its tile as both
  (C7 replaces it); SidebarSection on the Logo; LogoSection + registry + fixtures (ar/en); foundation §3 display row,
  §12 Logo row and Sidebar's SidebarHeader clause, §15 row 5, §16 (forms, sizes, clear space, never, name, source);
  the map's foundation line. Fixup → C6; `backup/ink-berry-identity-3`; autosquash; C6's body extended (amend).
- Head `22ddac1c`: C1 `72307999` lint 0 typecheck 0 (checked out alone); C6 `22ddac1c` lint 0 typecheck 0;
  test:unit 0 (web 196 files / 1346, api 323, shared 921); routes.component 70/70; build 0; check:build 0;
  check:links 3279 links resolve.
- EC7 after C6: 1,105,735 bytes (+21,371), gzip 326,775 (+4,997): the Logo is in the layer's chunk once exported.
- EC1 on `f58c12a8`: ADR 0019 (ours), last finding 219 → **220** (404 top bar) and **221** (README's Sea shots),
  last PR #143 → #144 expected; the inventory (`runs\ec1-inventory.txt`): 56 files, the preview's minus
  SidebarSection (C6 removed its tile) — nothing beyond §7.1; #143's ContactsSheet, ContactsView, PhotosEdit,
  PhotosView read as the plan's rows; its fix round (29a25054..14d3bb6e, 47 files, 3 added) added no colour class.
- The owner's update (2026-11-12): C11 records two findings, 220 then 221 — lane C's prompt updated (subject
  `docs(findings): record the 404 bar and sea shots`, 48).
- `C:\dev\masaha\app-pr143` no longer exists at the lanes' setup (worktree list).

## Phase 3 — the lanes
- Worktrees `app-design-lane-a/b/c` on `lane/a|b|c` at `22ddac1c`; .env copied; npm ci 0 and shared build 0 each,
  one at a time through the grant. Disk after: 18 GB free.
- Lane A launched first (after its install), then B and C after theirs.
- Lane B done first (≈ 11:09 UTC; `0f921ab7`, 2 commits), lane C (`df7c6ffb`, 4 commits), lane A last (`d724321e`,
  3 commits). Reports saved `lanes\REPORT_A.md`, `REPORT_B.md`, `REPORT_C.md`.

## The joins (order A, B, C)
- A: `backup/ink-berry-identity-pre-join-a`; `git merge --ff-only lane/a` (lane A branched at the head).
- B: `backup/lane-b-pre-join`; rebased in its worktree `--onto feat/ink-berry-identity 22ddac1c`, no conflict;
  `backup/ink-berry-identity-pre-join-b`; ff. C: the same (`backup/lane-c-pre-join`, `…-pre-join-c`), no conflict.
- On the joined head: lint 0, typecheck 0, check:classes clean (1989 files); the lanes' component files + both routes
  tests "37 passed / 361"; web unit (scripts, design-system, showcase) "17 / 457"; api auth/email "18".
- The lanes' document lines folded (`fold_docs.py`, one fixup per commit in commit order; `backup/ink-berry-identity-
  pre-fold`): C2 foundation §3 (e), §5 hover-not-selected, §11, §12 Table/DataTable/Select-Combobox/Calendar/
  ToggleGroup/SegmentedControl/Sidebar + the three optional rows (FilterTag, Tabs default, DropdownMenu), setup.md,
  CLAUDE.md; C3 §5 links rule, §12 Button; C4 §12 Tabs line, Sortable, §3 leaflet; C5 §12 Skeleton; C7 §16 Where it
  shows; C8 §16 browser's icons + §5's identity-colours clause ("and the browser's icons"); C9 §16 the reset e-mail.
  Autosquash clean: 11 commits, no fixup left; only the 3 docs differ from pre-fold. check:links 3290 resolve.
- Worktrees `app-design-lane-a/b/c` removed (`git worktree remove`, each clean). Branches lane/a|b|c kept until the PR.

## Phase 4
- Ports 3323, 5323, 3326, 5326 all free before starting (the supervisor's comparison servers were down) — no wait.
- API (`npm run dev -w @masaha/api`, 3323) and web (`npm run dev`, 5323) started from this folder (background tasks).
- EC2: `masaha_dev` has no `masaha-demo`; the demo owner (id 2) and reception (id 3) hold `pal-hub` (space 26); the
  directory lists 37 (the 24 of the demo set among them); the admin signs in with the password. Enough for the pass;
  recorded, not stopped (the demo set is present, its space named otherwise).
- Head `5862e2a4`: format:check 0, check:conflicts 0, check:links 0 (3290), check:classes 0. `#PRNUM` once
  (foundation Status).
- Visual pass sub-agent launched (`lanes\VISUAL.md`).
- Visual pass report saved (`lanes\REPORT_VISUAL.md`); its leftover watchers (two `tail -f`, PIDs 20956, 33356, and
  their bash 5020, 25396) stopped by PID; no `cdp-profile` Chrome, no `http.server` left.

## The visual pass's findings, handled (LEAD-D4 … D9)
- F1 (EC3 ✗, the item's): Chrome treats a near-grey's OKLCH hue as missing, so the oklch mixes of the ink neutrals
  painted warm (`primary-hover` #463e40 for #3c4147; Button secondary #e8dcdf; overlay-scrim warm). LEAD-D4: every
  token mix in OKLab (`primary-hover`, `overlay-scrim`, C1); the token test's resolver now refuses OKLCH (it cannot
  model Chrome's rule) — red on the old tokens "4 failed | 191 passed (195)" (`fix-f1-red.txt`, Unsupported mix
  ×2 per theme), green 195/195 after; foundation §5 values "(OKLab)" + the why line (C1); Button secondary hover
  `in_oklab`, §11's wording (C2); the prototype's primary hover `in oklab` + its CHANGES row (C10) so EC13 holds.
  Destructive stays OKLCH (the red keeps its hue: Chrome takes the red's hue for the missing grey one; PA6).
- F2 (the item's C4): the lifted photo's edge `outline-2 -outline-offset-2 outline-spark` + `focus-visible:` the same,
  so it is drawn inside the picture (the frame clipped it) and stands in for the ink ring while lifted (C4). The
  focus ring of a merely focused photo, clipped the same way, is older: finding 222.
- F3 (the item's): SiteMenu's current entry is the selected tint (`bg-accent text-accent-foreground`) with no ghost
  variant (`variant={current ? null : 'ghost'}`, `matchPath` on the same `to`/`end` NavLink uses), so it keeps the
  tint under the pointer without relying on variant order; hover elsewhere stays `hover` (C2). LEAD-D5.
- F4 (the item's): LiveStatusControl's neutral tone takes the Button's `secondary` variant (its own hover mix), the
  outline's `hover` being equal to `secondary` in dark (C2). LEAD-D6. Its open state no longer takes the outline's
  `aria-expanded:bg-hover` (the secondary variant has none) — Review Focus.
- F5, F6 (older): findings 223 (the heatmap's hidden table widens the page at 390) and 224 (axe: the map's tooltip,
  two scrolling strips). Plus finding 225: four site test files without rule 8's warm-up — SiteAccount's first test
  missed its 3 s wait in a nine-file run (3057 ms), passed alone 5/5 (`fix-c2-siteaccount-alone.txt`).
- New commit `docs(findings): record what the visual pass found` (49) with 222–225 (the plan's range of six, shifted
  by one: 220–225). LEAD-D7.
- Tests on the fixes: Button + site shell + occupancy 52/53 (the SiteAccount miss above), photos 27/27; lint 0 on the
  touched files; typecheck 0; check:classes clean; prototype check-parse 52/52, check-classes 0 new; check:links 3296.
- `backup/ink-berry-identity-pre-visual-fold`; autosquash clean → 12 commits, head `5e8a3b7b`.
- The visual agent re-checks F1–F4 on the running servers (SendMessage).
- The visual agent's re-check at `5e8a3b7b`: F1–F4 all pass (appended to `lanes\REPORT_VISUAL.md`); axe on the phone
  menu and the desk clean. 48 files in `Downloads\identity-prod-shots\`.
- Servers stopped: the two background tasks (TaskStop), then by PID the leftovers (tsx watch 4756, pino-pretty 7920,
  vite 13896, the server child 16844); ports 3323 and 5323 free.

## The complete verification
- Per-commit lint + typecheck (`per-commit.sh`, `runs\per-commit\`): 9 of 12 commits green (lint 0, typecheck 0 each:
  502e2ca3, 67d5c997, 6f192079, cc44128c, d7b00d09, 70831d84, f548604e, 5fdcdab1, 5fa394d3). **Stopped by Claude
  Code for low memory** during 207501fc's typecheck (13:28 UTC; another worker's API test was waiting at 2.7 GB free).
  Cleanup: the orphaned `tsc -b` (5932) stopped by PID, the stale `heavy-slot-1` freed, the folder back on the branch.
  Not restarted without the owner's word (the harness's rule). The three unchecked commits (207501fc, 6b713f99,
  5e8a3b7b) change only `docs/` (the prototype, findings), which neither eslint nor tsc reads.
- **Correction:** the loop's shell survived the task's stop and carried on: 207501fc "lint 1 typecheck 127" (eslint
  printed no error — the grant script itself crashed reading free memory at the run's end, PowerShell failing to
  start under pressure, status 3221225794; the typecheck was the `tsc` I stopped), then 6b713f99 lint 0 typecheck 0,
  5e8a3b7b lint 0 typecheck 0, "back on feat/ink-berry-identity 5e8a3b7b". My own checkout of the branch raced its
  checkout of 6b713f99 (docs-only difference, no effect on what eslint and tsc read).
- The supervisor's answer (relayed by the owner): resume now. (1) Commits 10–12 need no per-commit run:
  `git diff --name-only 5fa394d3 HEAD -- . ':!docs'` → empty (0 files); `eslint .` ignores docs/design and lints no
  Markdown; the tsconfigs include only src, test, scripts — their lint and typecheck equal commit 9's. (2) The grant
  becomes single-slot under 8 GB free. (3) The lanes one at a time, the build, EC8, the push, the PR, CI, the report.
- heavy.mjs changes (LEAD-D8): single slot while free < 8 GB (a run takes only slot 1, and only while slot 2 is free;
  a second slot only with ≥ 8 GB free); a failed memory reading counts as 0 KB (it waits instead of crashing with a
  slot taken). A stale `heavy-slot-1` (13:36:24 UTC, no GRANT, no holder — the other worker's attempt crashed the same
  way) freed. The other worker ("we") uses the same script, so the rule holds for both.
- Full lanes at `5e8a3b7b`, one at a time through the grant: **test:unit** exit 0 (granted 14:24:31 UTC after a wait
  for memory, 52 s): web 197 files / 1385 tests, shared 77 / 924, api 28 / 323. **test:component** exit 0 (granted
  14:37:44 after the other worker's test:api, 502 s): 348 files / 2120 tests, no miss.
- **test:api** granted 14:46:21 UTC, cut by the machine's outage (internet lost, restart; the session ended with it).
  Its partial output kept as `final-test-api-cut-by-outage.txt`. The supervisor checked after the restart: the branch
  at `5e8a3b7b` clean; Docker and the databases intact; the slot-1 it left cleared ("super CLEAR", 2026-11-13
  13:04 UTC); test:unit and test:component stand for this head. Resumed 2026-11-13 from test:api.
- **test:api** re-run (granted 2026-11-13 13:28:48 UTC after waits for memory, 1371 s): exit 0, 125 files / 1432
  tests on `masaha_design_test`. The cut run's red (`desk/customers.api.test.ts` › "each filter applies before the
  page is cut", 5248 ms, a file this item does not touch) passed in the full re-run: the loaded machine's timeout.
- **Build:** `NODE_ENV=production npm run build` 0; `check:build` 0. **EC5 (build):** the built CSS holds `.border-spark`,
  `.outline-spark`, `.fill-spark`, `.after\:bg-spark:after`, `.focus-visible\:outline-spark:focus-visible`,
  `.data-\[active\=true\]\:before\:bg-spark[data-active=true]:before`, `.data-on\:border-spark:where([data-state=on])`
  and `.map-mark-selected span{outline:3px solid var(--spark)…}`; no `text-spark`.
- **EC8 (vite preview of the build, port 5329):** `/favicon.svg` 200 `image/svg+xml` 14 988 B, `/favicon.ico` 200
  `image/x-icon` 2 112 B (identical to `public/`), `/apple-touch-icon.png` 200 `image/png` 3 264 B; the built
  `index.html` holds the three links and both `theme-color` metas; unknown paths answer `text/html` (the SPA), the
  icons their own types. The preview stopped (task + PID 2668), 5329 free.
- **EC7:** `origin/main` `f58c12a8` built (checked out detached, back on the branch after, tree clean): first download
  1,105,713 B, gzip 326,759 (`ec7-main.txt`). Head: 1,121,394 B, gzip 334,832 (`ec7-after.txt`): **+15,681 B,
  +8,073 gzip**, all in the layer's chunk (`design-system` 293,137 → 308,809; gzip 84,458 → 92,537): the logo's paths
  in the site's header. The earlier "+21,371 after C6" compared with the old main, so it measured #143; on the new
  main C6 adds 22 B (the Logo is shaken out until a site page draws it). Over the plan's 5–6 KB compressed estimate;
  no size budget in check:build.
- Light checks on the head `5e8a3b7b`: format:check 0, check:classes 0 (1989), check:links 0 (3296 / 226 / 2684),
  check:conflicts 0.
- **Prototype checks:** the queued run (waiting for slot 1, held by the other worker's test:component) was stopped by
  Claude Code for low memory (2026-11-13 ≈ 14:08 UTC); not restarted (the harness's rule). Its lead-waiting marker
  removed. Not needed: `git diff --name-only 4bf65b66 HEAD -- docs/design` is empty, and at that tree (the C10 fix)
  `check-parse` gave "52/52 blocks parsed, from 42 pages and the modules", `check-classes` "361 classes used, 5 dead
  uses, 0 new" (`fix-c10-parse.txt`, `fix-c10-classes.txt`).
- Files: 81 (16 added, 65 changed), +1528 / −292; 12 commits.

## Push and the PR
- Before the push: `git fetch origin` (main still `f58c12a8`, no rebase needed); the last issue/PR 143; no open PR.
- `backup/ink-berry-identity-pre-prnum` at `5e8a3b7b`; `git filter-branch --tree-filter "grep -rl '#PRNUM' docs |
  xargs -r sed -i 's/#PRNUM/#144/g'" origin/main..HEAD` (12 commits rewritten; `refs/original` deleted); `#PRNUM` 0;
  the diff against the backup: 2 files, 3 lines (foundation's Status and the OKLab line, finding 222). Commit messages
  hold no placeholder and no tool attribution; subjects 33–49 characters.
- Pushed `git push -u origin feat/ink-berry-identity`; `gh pr create` at once: **#144** (as expected), head
  `4cff26c7de4ea1b4b8454ad48f1f440b9a0ae84b`, assigned to the owner, labels feat, area:web, area:api,
  area:design-system, area:docs, area:ci. Body: `runs\pr-body.md`.
- The commits (final): c602db41 C1, 199f9da8 C6 (logo), e1cc1a7f C2, c74e8c79 C3, 38c695a4 C4, 2a4b8ace C5,
  4c732ea5 C7, b4cf3236 C8, 37ef1039 C9, 1111a22f C10, 39dc9f31 C11, 4cff26c7 C12.
- The early conflict check: no other open PR (`gh pr list --state open` empty), so no `git merge-tree` to run.
