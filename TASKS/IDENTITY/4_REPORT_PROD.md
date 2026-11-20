# IDENTITY — ink + berry and the logo in production — the lead's report

> **Prompt:** `3_EXEC_PROMPT_PROD.md` · **Plan:** `2_PLAN_PROD.md` · **Lead:** this session (Claude Code, Opus 5.5)
> **Ran:** 2026-11-12 (Phases 1–4 up to `test:component`) and 2026-11-13 (after the machine's restart: `test:api`, the
> build, EC7, EC8, the push, CI). Working notes: `runs\LEAD_LOG.md`; outputs in `runs\`; the lanes' and the visual
> pass's reports in `lanes\REPORT_A.md`, `REPORT_B.md`, `REPORT_C.md`, `REPORT_VISUAL.md`.

## Status — READY FOR REVIEW

**PR #144** (https://github.com/Basel-Ghonaim/masaha/pull/144), `feat/ink-berry-identity`, head
**`4cff26c7de4ea1b4b8454ad48f1f440b9a0ae84b`**. CI green on that head: run 43440252687, ten jobs pass (lint,
format:check, typecheck, check:classes, check:links, check:conflicts, build, test:unit, test:component, test:api; the
CodeRabbit app skipped). GitHub `CLEAN`, `MERGEABLE`. Assigned to the owner; labels `feat`, `area:web`,
`area:design-system`, `area:api`, `area:docs`, `area:ci`. 81 files (16 added, 65 changed), +1528 / −292, 12 commits.
Over 25 files and a build check changed (`check:classes`): its review is a separate conversation (workflow §2, phase 7).

---

## 1. The pull request and its head

- #144, head `4cff26c7de4ea1b4b8454ad48f1f440b9a0ae84b`, base `main` `f58c12a8` (#143's merge). The number was read
  just before the push (last issue/PR 143) and `#PRNUM` replaced in every commit's tree; `gh pr create` gave #144.
- The description (`runs\pr-body.md`): Summary; Scope / Acceptance criteria / Out of scope; Change type; Evidence
  (each command and its counts, the tests seen failing, the breaks, the visual pass, what was not run); Screenshots
  (in the owner's `Downloads\identity-prod-shots\`, 48 files, to be attached by the owner); the DoD checklist.

## 2. The commits

The plan's §15 units, C1 and C6 first (the shared layer), and a twelfth for the visual pass's older defects. Each
lints and typechecks on its own (§3).

| # | sha | subject (length) | plan | made by |
|---|---|---|---|---|
| 1 | `c602db41` | feat(design-system): adopt ink and berry identity (49) | C1 | lead |
| 2 | `199f9da8` | feat(design-system): add the logo (33) | C6 | lead |
| 3 | `e1cc1a7f` | feat(design-system): tell hover from selected (45) | C2 | lane A (+ lead's folds) |
| 4 | `c74e8c79` | feat(web): underline links in running text (42) | C3 | lane A (+ folds) |
| 5 | `38c695a4` | feat(design-system): mark what matters in spark (47) | C4 | lane A (+ folds) |
| 6 | `2a4b8ace` | fix(web): raise the skeleton and photo count (44) | C5 | lane B (+ fold) |
| 7 | `4c732ea5` | feat(web): show the logo in every shell (39) | C7 | lane B (+ fold) |
| 8 | `b4cf3236` | feat(web): add the favicon and home-screen icon (47) | C8 | lane C (+ fold) |
| 9 | `37ef1039` | feat(auth): draw the reset email in ink (39) | C9 | lane C (+ fold) |
| 10 | `1111a22f` | docs(design): make berry the prototype's default (48) | C10 | lane C (+ fold) |
| 11 | `39dc9f31` | docs(findings): record the 404 bar and sea shots (48) | C11 (findings 220, 221) | lane C |
| 12 | `4cff26c7` | docs(findings): record what the visual pass found (49) | new (findings 222–225) | lead |

Each with a body that says why; no tool attribution; staged by path; no `fixup!` left.

## 3. What was run, and what was not

### On the head (all through the grant script, one heavy run at a time)

| Command | Result |
|---|---|
| `npm run lint` · `npm run typecheck`, **per commit** | commits 1–9 exit 0 each (`runs\per-commit\summary.txt`, pre-rewrite shas 502e2ca3 … 5fa394d3). Commits 10–12: `git diff --name-only 5fa394d3 HEAD -- . ':!docs'` → **empty (0 files)**; `eslint .` ignores `docs/design/` and lints no Markdown; the tsconfigs include only src, test, scripts — their lint and typecheck equal commit 9's (the supervisor's ruling). The loop also ran 6b713f99 and 5e8a3b7b: 0 / 0 (§6) |
| `format:check` · `check:classes` · `check:links` · `check:conflicts` | 0 · 0 (1989 files) · 0 (3296 links, 226 documents, 2684 sources) · 0 |
| `test:unit` (2026-11-12 14:24 UTC, 52 s) | web 197 files / 1385 tests · shared 77 / 924 · api 28 / 323 — all passed |
| `test:component` (14:37 UTC, 502 s) | 348 files / 2120 tests — all passed, no miss |
| `test:api` (2026-11-13 13:28 UTC, 1371 s, on `masaha_design_test`) | 125 files / 1432 tests — all passed |
| `NODE_ENV=production npm run build` · `check:build` | 0 · 0 ("No showcase code in 77 build files …", "No data-table or leaflet or calendar or sortable … in the site's first download") |
| The prototype's `check-parse.mjs` · `check-classes.mjs` | "52/52 blocks parsed, from 42 pages and the modules" · "361 classes used, 5 dead uses, 0 new" — run at the C10 fix's tree; `git diff --name-only 4bf65b66 HEAD -- docs/design` is empty, so it stands for the head (§6) |
| `test:unit` / `test:component` stand for the head `4cff26c7`: they ran at `5e8a3b7b`, which differs only by `#PRNUM` → `#144` in two documents (3 lines) |

### The real run — the visual pass (T23), by a fourth sub-agent, and its re-check

- API (3323) and web (5323) from this folder; the supervisor's comparison servers were already down (ports free).
- Coverage: the full matrix (390 / 768 / 1440 × ar / en × light / dark) on 18 screens; subsets for the dialogs, the
  date picker, the contacts sheet, the drawers, the phone menu, a loading state, a FilterTag; the hover set at 1440.
- Clean: no Sea value in any computed colour, pseudo-element or stylesheet; no spark text; no painted-contrast
  failure; the focus ring visible in every context (but the photo tiles, finding 222); overflow only F5 (finding 223);
  the status colours exact; no app console error.
- Four defects of this item found and fixed (§5), re-checked in the browser: all pass.
- Servers stopped by their tasks and then by PID (tsx watch, pino-pretty, vite, the server child); ports free.

### Not run, and why
- E2E smoke: an end-of-project lane.
- `pointer-coarse` sizes: the 390 pass used a desktop pointer.
- Photo grounds: the demo photo files answer 404 in this folder's local storage; the «+N» scrim is proven by the
  token test over white and black instead.
- EC8 in production (the deployed `/favicon.svg` answering `image/svg+xml`): after the merge, the owner's.
- EC12 (Google's branding facts on the day) and the upload: the owner's steps (plan §16), after the merge.
- EC13 after the F1 fix: the prototype's primary hover now mixes in OKLab as production does; its painted value was
  not re-measured (production's was: `#3c4147` / `#c7cbd0`).

### EC results

| EC | Result |
|---|---|
| EC1 | On `main` `f58c12a8`: ADR 0019 (ours), last finding 219 → 220, 221 (and 222–225), PR #144 (confirmed). The inventory command: 56 files, nothing beyond §7.1 (the preview on #143's head had SidebarSection too; C6 removed its tile). #143's ContactsSheet, ContactsView, PhotosEdit, PhotosView read as the plan's rows; its fix round (`29a25054..14d3bb6e`, 47 files, 3 added) added no colour class. Lane A's own run of the new rule: 40 classes in 20 files, every one a §7.1 row. MissingChecklist no longer exists (#143 removed it; its successor link in ProfileHeader was already underlined) |
| EC2 | `masaha_dev` holds the demo set but **no `masaha-demo`**: the demo owner and reception hold `pal-hub` (space 26); the directory lists 37 (the 24 among them); the three accounts sign in. Recorded and used, not stopped. `masaha_design_test` exists |
| EC3 | The test's maths reproduces the trial once mixes are quantised to 8 bits as painted (fg on the dark tint 13.011 vs 13.01, mfg 5.496 vs 5.50, fg on the wash 12.306 / 9.905 vs 12.31 / 9.90). Chrome's painted values: dark accent `#471f46` exact; the wash `#d7dee6` / `#3d4147` within 1/255; **`primary-hover` failed** (`#463e40` for `#3c4147`) → the cause found (F1) and fixed; after: `#3c4147` / `#c7cbd0` exact |
| EC4 | Machado severity 1 on linear RGB reproduces the trial within 0.001: ink↔red light .346 (.190, .319), dark .329 (.365, .278); spark↔red light .191 (protan .220, deutan .184), dark .156 (.154, .158). Kept |
| EC5 | `cn` keeps the spark utilities in their colour groups; the production CSS holds `.border-spark`, `.outline-spark`, `.fill-spark`, `.after\:bg-spark:after`, `.focus-visible\:outline-spark:focus-visible`, `.data-\[active\=true\]\:before\:bg-spark[data-active=true]:before`, `.data-on\:border-spark:where([data-state=on])`, the map's `outline:3px solid var(--spark)`; no `text-spark`; in dev the visual pass saw the bar, the chip's edge and the line tabs' indicator |
| EC6 | `h-10` 109.53 × 40, `h-9` 98.58 × 36, the mark `size-9` 36 × 36; `transform: none` up the tree; the drawer's logo at the inline start in both directions; the component's mark at 64 px against `masaha-mark-berry.svg`: 0 of 4096 pixels differ by more than 8/255 |
| EC7 | Before (C1's head on the old main): 1,084,364 B / gzip 321,778. On the new main: `main` 1,105,713 / 326,759; the head 1,121,394 / 334,832 → **+15,681 B, +8,073 gzip**, all in the layer's chunk (the logo's paths, in the site's header). Over the plan's 5–6 KB compressed estimate; `check:build` has no size budget (PA4, optimising the paths, is the owner's later call) |
| EC8 | Dev server and `vite preview` of the build: `/favicon.svg` 200 `image/svg+xml` (14 988 B), `/favicon.ico` 200 `image/x-icon` (2 112 B, identical to `public/`), `/apple-touch-icon.png` 200 `image/png` (3 264 B); the built `index.html` holds the three links and two `theme-color` metas; Chrome requests `/favicon.svg` on load and it switches under emulated `prefers-color-scheme` (`#1a1f25`/`#b55bb3` → `#f7fbff`/`#d27ed0`). Production after the merge: the owner's |
| EC9 | Lane C: the `.ico` (16, 32, 48 RGBA PNG entries of the app icon), the 180 (mark on white, full bleed), the Google 120 (`TASKS\IDENTITY\google\masaha-logo-120.png`, mark 96 px centred, nothing beyond 56 px from the centre); `favicon.svg` pixel-identical to the owner's mark files in both schemes. The visual pass confirmed each |
| EC10 | Lane A: the wash given to DataTable's sort header, the calendar's today, FilterTag's remove, the contact tile (fill moved to the `<li>`), SegmentedControl's unchecked segment, the `md` Tabs track. Outline buttons and chips with their own card fill on muted grounds (MoneyBlock, PackageRow paused, OwnersCard, RemoveFavorite, PhotoTile) left with `hover`: their own fill changes, so the hover shows (lane A's decision 4, accepted) |
| EC11 | axe in Chrome on every screen: no colour-contrast violation; only older violations (`aria-tooltip-name` on the map's tooltip; `scrollable-region-focusable` on two strips): finding 224. Clean on the re-checked phone menu and desk |
| EC12 | Not done: the owner's, before the upload |
| EC13 | The prototype (berry by default) equals production on the primary at rest, the sidebar's current item and its bar, a chip on, the hovers; the primary hover then had the same hue loss in both; now both mix in OKLab (not re-measured, above) |
| EC14 | At 360, guest and signed in, ar / en, light / dark: no overflow, no overlap |

## 4. The breaks made, and the tests seen failing first

Seen failing first (red lines in `runs\` and the lanes' reports):
- **T1–T11** (the token test): on Sea's tokens "Tests 66 failed | 128 passed (194)" (`c1-red-tokens.txt`); green 194.
- **T16** (Logo): the component removed → "Failed to resolve import ./Logo"; green 10/10.
- **T17** (SidebarHeader): "2 failed | 12 passed (14)" before the API; green.
- **T12** (lane A): "Tests 23 failed | 91 passed (114)"; green 114.
- **T20** (lane A): "1 failed | 11 passed (12)"; green 12.
- **T18, T19** (lane B): "4 failed | 85 passed (89)"; green 89.
- **T13–T15** (lane C): "Tests 5 failed (5)"; green 8 with the CSP test.
- **T22** (lane C): "3 failed | 6 passed (9)"; green 9.
- **The resolver refusing OKLCH** (F1's fix): "4 failed | 191 passed (195)" on the old `primary-hover`; green 195.

Breaks made, each from a backup copy, red, restored by copy:
- **Tokens (`c1-break-*.txt`):** a wrong transfer exponent (8 red); a hex-only resolver (29); hover set to the tint (6,
  the two "hover is not the selected tint" among them); a coral dark spark `#ef7b62` (4); the skeleton on n-100 (2);
  the scrim at 60 % (1, over white); a paler spark (7); a leftover `brand-500` (1); `--color-spark` (1); a
  `text-spark` utility (1); a dark role missing (5).
- **Logo (`c6-break-*.txt`):** the name dropped (6); not hidden (2); `rtl:-scale-x-100` (2); the dots on
  `fill-primary` (2); a cropped frame (1).
- **SidebarHeader:** the mode branch swapped (3).
- **`check:classes`:** the rule removed (23); narrowed to `hover:` (10, a `focus:bg-accent` red).
- **Button:** `hover:underline` back; `border-spark` on the outline variant.
- **Shells:** the text wordmark back; the logo without its label; the «م» tile back; the name read twice.
- **Icons and e-mail:** a link dropped; the dark rule removed; a 32-only `.ico`; a Sea hex in the e-mail; the
  underline removed.

## 5. Problems met, and how each was solved

- **The showcase registry's red between C6's two parts.** The registry test wants an entry for every component folder;
  the entry needs the layer's index, a #143 file. Committed the Logo with that one known red, which the post-merge part
  of C6 turned green (folded, so no final commit is red). LEAD-D1.
- **A claim made too early.** C1's foundation line on the identity's colours named the browser's icons, built in C8:
  narrowed in C1, widened back in C8's fold.
- **The visual pass's four defects of this item** (`lanes\REPORT_VISUAL.md`), each fixed in its commit and re-checked
  in Chrome:
  - **F1 — the ink's hovers painted warm** (EC3 failed): Chrome treats a near-grey's hue as missing in OKLCH, so
    `color-mix(in oklch, n-900, n-50 18%)` painted `#463e40` (hue 0), the secondary button's hover `#e8dcdf`, the
    overlay's scrim warm. Every token mix now in OKLab (`primary-hover`, `overlay-scrim`; C1), the Button's secondary
    hover in OKLab (C2), the prototype's primary hover too (C10), foundation §5 and §11 say why; the token test's
    resolver refuses an OKLCH mix it cannot model (red first). Destructive stays OKLCH (the red keeps its hue). LEAD-D4.
  - **F2 — a lifted photo showed no edge**: the tile's frame (`overflow-hidden`) clipped the outline, and the focus
    ring won over the spark. The lifted edge is drawn inside (`-outline-offset-2`) and takes the focus-visible outline
    while lifted (C4). The plain focus ring's clipping is older: finding 222.
  - **F3 — the phone menu's current page looked hovered in dark** (`secondary` = `hover` = n-800): its current entry
    takes the selected tint and no ghost variant at all (`variant={current ? null : 'ghost'}`, `matchPath` on the same
    `to`/`end` NavLink uses), so it keeps the tint under the pointer without relying on Tailwind's variant order (C2).
    LEAD-D5.
  - **F4 — the neutral live-status trigger had no hover in dark** (`hover` = its `secondary` fill): it takes the
    Button's secondary variant, whose hover mixes toward the foreground (C2). LEAD-D6.
- **Memory.** A per-commit loop and a queued prototype check were stopped by Claude Code for low memory; not restarted
  without the owner's word. Their results were accounted for: the loop's shell had in fact finished; the prototype's
  result stands, its files unchanged. The supervisor's ruling made the grant single-slot under 8 GB. LEAD-D8.
- **The grant script crashed under memory pressure.** PowerShell failed to start inside its memory reading (status
  3221225794): a run's END crashed (commit 10's lint reported 1 with eslint printing nothing), and a slot was left behind
  twice (13:36 UTC, and the outage's). A failed reading now counts as 0 KB (the run waits); the stale slots freed (one
  by the supervisor, "super CLEAR").
- **The machine's outage cut `test:api`** (2026-11-12 14:46 UTC, the session ended with it). Resumed the next day from
  `test:api` after the supervisor's check; green.
- **A red in the cut `test:api`** (`desk/customers.api.test.ts` › "each filter applies before the page is cut",
  5248 ms): a file this item does not touch; green in the full re-run — the loaded machine's timeout.
- **SiteAccount's first test missed its 3 s wait** in a nine-file run (3057 ms) and passed alone 5/5: rule 8's missing
  warm-up, recorded as finding 225 (lane B saw the same gap in three auth test files).
- **EC2's `masaha-demo` missing**: the demo owner's space is `pal-hub` (26) in `masaha_dev`; the pass used it.

## 6. Anything that behaved unexpectedly, even unsolved

- Chrome drops the OKLCH hue of the ink's near-greys (chroma ≈ 0.014): `oklch(from #1a1f25 l c h)` computes to
  `oklch(0.2369 0.0137 none)`. The trial's prototype had the same warm hover; nobody had measured it.
- The per-commit loop's shell **survived** the harness's stop and carried on (207501fc "lint 1 typecheck 127" — the
  grant's crash and the `tsc` I stopped; then 6b713f99 and 5e8a3b7b 0/0; then "back on feat/ink-berry-identity"). My
  own checkout of the branch raced its checkout of 6b713f99 (a docs-only difference; no effect on lint or tsc).
- The early EC7 "+21,371 B after C6" compared with the old main: it measured #143's growth; on the new main C6 adds
  22 B (the Logo is shaken out until a site page draws it), and the growth comes with C7.
- `C:\dev\masaha\app-pr143` no longer existed when the lanes were set up; the comparison servers were down at the
  visual pass.
- The visual agent left two `tail -f` watchers (and their bash) after its first report: stopped by PID.
- Lane C: a fractional raster size left a seam where the mark's two mirrored halves meet (re-rendered at whole pixels);
  .NET's `System.Drawing.Icon` cannot read the `.ico`'s PNG frames (Windows' WIC can).
- Lane A: the inventory found the column of a class one further than its hand count (16, not 15): the test's
  expectation was wrong and fixed by recounting.
- The demo photos answer 404 from this folder's storage; Google's sign-in button answers 403 on `localhost:5323`.

## 7. The early conflict check

`gh pr list --state open` lists only #144: no other open pull request, so no `git merge-tree` to run.

## 8. Departures from the prompt and the plan, with their reasons

**The prompt's own departures from the plan (as instructed):**
1. The run took the shape of the prompt's §3–§6.
2. The lead started before #143 merged, then waited (merged 2026-11-12 10:31 UTC; the wait script saw it at check 3).
3. The plan's finding 219 became 220.
4. The report is here, in `4_REPORT_PROD.md`.
5. The commits keep the plan's units, C1 and C6 first.
6. No file #143 changes was edited before its merge (checked before each commit of Phase 1).

**The owner's updates:**
- C11 records two findings: 220 (the admin's 404 top bar) and 221 (the README's Sea shots). Its subject became
  `docs(findings): record the 404 bar and sea shots`.
- The supervisor's ruling after the memory stop: commits 10–12 by the docs-only proof, the grant single-slot under
  8 GB, then resume.

**The lead's, each with its reason:**
- **A twelfth commit** with findings 222–225 (the visual pass's older defects and the warm-up gap). They are separate
  from C11's two, and the plan's range of six numbers (219–224, shifted by one) is kept: 220–225.
- **`primary-hover` mixes in OKLab, not the plan's OKLCH,** and so do `overlay-scrim`, the secondary button's hover and
  the prototype's primary hover. EC3 found Chrome's OKLCH result warm. The token test's resolver refuses OKLCH (the
  plan's T2 named OKLCH among the mixes it reads).
- **SiteMenu and LiveStatusControl** changed, beyond §7.1's tables: they are the visual pass's F3 and F4.
- **The lifted photo's edge is drawn inside the picture** (F2), not as the plan's plain `outline-spark`.
- **T8's dark tint check covers `sidebar-accent` too** (the same mix). LEAD-D3.
- **Lane C rendered the rasters inside C8,** where the prompt listed them in Phase 4: it owns `public/` and T15.
  Its Chrome went through the grant, and no other lane ran Chrome. LEAD-D2.
- **The showcase's Logo section,** with SidebarHeader's API and callers, came with C6's post-merge part, as the prompt
  said. That left one known red between the two parts (LEAD-D1).
- **The visual pass was a fourth sub-agent;** its re-check was the same agent.
- **EC2:** the demo space is `pal-hub`, not `masaha-demo`. It was used, not stopped (the demo set is present).
- **The prototype checks' result was reused** at the head (its files unchanged) after the queued re-run was stopped for
  memory.
- **The grant script** got two changes: single-slot under 8 GB (the supervisor), and a failed memory reading counting
  as 0 KB (the lead).

## The lanes, summarised

- **Lane A** (`lane/a` `d724321e`; `lanes\REPORT_A.md`)
  - C2, C3, C4: 26, 6 and 5 files. T12 (33 new cases) and T20 were seen red; four breaks; T21 green (21 component
    files, 200 tests).
  - Its decisions:
    - the calendar's range middle takes no ghost variant;
    - `check:classes`' rule also reads `group-`/`peer-` forms, opacity and `!`; it does not read arbitrary
      `data-[state=open]:` spellings (a known gap);
    - one variant parser serves both finders;
    - EC10's outline buttons with their own fill are left with `hover`;
    - ShowcaseNav hovers only off the current entry.
  - Found, not fixed: LiveStatusControl and SiteMenu (both became F3 and F4, fixed); PhotosEdit's keyboard lift (F2,
    fixed).
- **Lane B** (`lane/b` `0f921ab7`; `REPORT_B.md`)
  - C5 and C7: 2 and 7 files. T18 and T19 were seen red (4); four breaks; ten files, 150 tests green.
  - Its decisions: T19 written in Arabic; the focus shell's test strengthened in place; one comment in AdminLayout.
  - Noted: three auth test files without a warm-up (now finding 225); no axe test renders the admin's header.
- **Lane C** (`lane/c` `df7c6ffb`; `REPORT_C.md`)
  - C8–C11: the icons, the e-mail, the prototype, findings 220 and 221. T13–T15 and T22 seen red; five breaks.
  - The rasters rendered in headless Chrome and packed by a script; the Chrome processes stopped by PID.
  - Its decisions:
    - the 120 at 96 px with clear space;
    - the 180 from the mark on white;
    - a comment in `index.html`;
    - extra assertions (the links' order, no other colour);
    - `ink` / `onInk` names;
    - an unknown `?identity=` gives berry.
  - Noted: the prototype's `Reset email.html` and `Wordmark.html` keep Sea's tab icon; the prototype and production
    lay out the e-mail's English link differently (older).
- **Grants:** no lane run was killed; lane A waited 4 times and lane C twice, for memory.

## The joins

- **Order A, B, C.** A by fast-forward (it branched at the head). B and C were rebased in their worktrees
  (`--onto feat/ink-berry-identity 22ddac1c`), with no conflict, then fast-forwarded.
- **On the joined head:**
  - lint 0, typecheck 0, `check:classes` clean;
  - the lanes' component files and both routes tests: 37 files, 361 tests;
  - web unit: 17 files, 457 tests; api auth/email: 18 tests.
- **The lanes' document lines** were folded into their commits (`fold_docs.py`: one fixup per commit, in commit order;
  autosquash clean):
  - foundation §3 (e) and the leaflet paragraph;
  - §5 (hover is not selected, links underlined);
  - §11;
  - §12 rows (Table, DataTable, Select/Combobox, Calendar, ToggleGroup, SegmentedControl, Sidebar, FilterTag, Tabs,
    DropdownMenu, Button, Sortable, Skeleton);
  - §16 (where it shows, the browser's icons, the reset e-mail);
  - `setup.md`'s commands row and `CLAUDE.md`'s commands line.
- **Worktrees:** the three lanes' were removed (`git worktree remove`, each clean). No other worktree was touched.

## Memory and the grants

`scripts\heavy.mjs` (adapted from BACKEND_FINAL's) logged 237 grants, 97 of them the lead's. At first it granted with
≥ 4 GB free, two slots at most, the lead first (a lead marker held the lanes back). From 2026-11-12 it allows one slot
under 8 GB, and a failed memory reading counts as 0 KB. The other worker ("we") used the same script and its rules.

Waits: the lead's full lanes waited 1–30 minutes for memory or for the other worker's run (`test:unit` 14:16–14:24,
`test:component` behind the other worker's `test:api`, `test:api` 13:06–13:28 on 2026-11-13). No heavy run of the
lead's was killed by memory. Two background shells were stopped by Claude Code's memory guard: the per-commit loop
(which in fact finished) and the queued prototype check. The machine's outage cut one `test:api`.

## Decisions taken without the owner (LEAD-D…) — none SERIOUS (no money, role, private data or redesign)

1. **D1:** the Logo committed with the registry's one known red until C6's post-merge part.
2. **D2:** lane C renders the rasters.
3. **D3:** T8 covers `sidebar-accent`.
4. **D4:** every token mix, the secondary hover and the prototype's primary hover in OKLab; the resolver refuses OKLCH.
5. **D5:** SiteMenu's current entry is selected, with no hover.
6. **D6:** LiveStatusControl's neutral tone uses the secondary variant.
   - Its open state loses the outline's `aria-expanded` hover fill: Review Focus.
7. **D7:** findings 222–225 in a commit of their own.
8. **D8:** the grant script's changes: single-slot under 8 GB (the supervisor), and a failed reading counting as 0 KB.

Each is undone by reverting its fold or commit (`backup/*` below).

## Review Focus (beyond the plan's §11)

- **LiveStatusControl's neutral trigger** no longer marks its open popover with a fill (the secondary variant has no
  `aria-expanded` style).
- **SiteMenu's current entry** derives "current" with `matchPath` beside NavLink's own `aria-current`.
  Review that the two agree for every `SITE_LINKS` entry (`end` defaults to false in both).
- **The lifted photo's edge is inset by 2 px over the picture.** The merely focused photo's ring is still clipped
  (finding 222).
- **The token test no longer reads OKLCH.** A future token written in OKLCH fails it by design.

## Leftovers, for the owner

- **Branches:**
  - `lane/a`, `lane/b`, `lane/c` (local, joined);
  - `backup/ink-berry-identity-1`, `-2`, `-3`, `-pre-join-a`, `-pre-join-b`, `-pre-join-c`, `-pre-fold`,
    `-pre-visual-fold`, `-pre-prnum`;
  - `backup/lane-b-pre-join`, `backup/lane-c-pre-join`.

  None was deleted (deleting branches is the owner's).
- **Not committed:**
  - the Google PNG, `TASKS\IDENTITY\google\masaha-logo-120.png`;
  - 48 screenshots in `C:\Users\basel\Downloads\identity-prod-shots\`.
- **Scratch:**
  - the lanes' and the pass's folders, `lanes\scratch-a`, `-b`, `-c` and `-v`;
  - the lead's scripts, in the session scratchpad and `runs\`.
- **The owner's steps after the merge:**
  - check that production's `/favicon.svg` answers `image/svg+xml` (EC8);
  - Google Branding (plan §16, EC12): the 120 px PNG above;
  - the README's shots (finding 221).
- **Findings opened:**
  - 220: the admin's 404 top bar;
  - 221: the README's Sea shots;
  - 222: a focused photo's ring is clipped;
  - 223: the occupancy page scrolls sideways at 390;
  - 224: axe flags the map's tooltip and two scroll strips;
  - 225: four site test files have no warm-up.
