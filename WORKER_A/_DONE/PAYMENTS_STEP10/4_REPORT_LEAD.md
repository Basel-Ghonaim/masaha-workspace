# PAYMENTS_STEP10 — the lead's run (PRs 2, 3, 4a, 4b + findings 169, 173 in one PR) — the report

Written as the work goes. Executor: worker A's lead (Claude Code), 2026-10-28, under `3_EXEC_PROMPT_LEAD.md` and the
autonomy rule.

## Status — READY FOR REVIEW

- **SERIOUS decisions: none.**
- **PR #129** https://github.com/Basel-Ghonaim/masaha/pull/129 · head `fcf46637` · CI green (every lane) · `CLEAN` · 248 files.
- 16 commits: Lane 0 three (findings 169, 173, the calendar pre-bundled for the component lane), lane A four (PR 2), lane B
  three (PR 3), lane C five (PR 4a, 4b commits 1–5), the lead's commit 6. Nothing left out.
- Findings resolved 8, 131, 169, 173; recorded 167, 168, 180. One defect found by the real run and fixed (LEAD-D12).
- Never merged; no Issue created; no force-push; nothing pushed to `main`.

## Start

- `git status --short` clean; `git fetch origin`; `origin/main` = `76661f7c` (#128 merged), as the prompt says.
- `git switch -c feat/step10-screens origin/main`; upstream unset (the branch is pushed only by name).
- Worktrees present before the run: `app` (main), `app-b` (detached, worker B — idle), `app-design`, `app-review` (detached). Not touched.
- Free memory at the start: 8,604,544 KB; 12 logical cores.

## Lane 0 — the foundation (by the lead)

### Commit L0-1 — `5104e227 perf(design-system): serve the calendar on its own` (50 chars) — finding 169

- `apps/web/src/shared/design-system/calendar.ts` (new entry: `Calendar`, `DatePicker` and their types), removed from
  the main barrel `index.ts`; `eslint.config.js` `LAYER_ENTRIES` gains `calendar.ts`; `apps/web/scripts/libraryChunks.ts`
  gains the `calendar` chunk (react-day-picker, date-fns); importers moved: `features/payments/…/LedgerFilters.tsx`
  and the showcase's `CalendarSection`, `DatePickerSection`, `DataTableSection`; tests `libraryChunks.unit.test.ts`,
  `layerEntries.unit.test.ts`; docs foundation §3 (the tree and the public-surface rule), architecture §3 (the heavy
  libraries' line), finding 169 → *Resolved* with its line, the index. 14 files.
- **Red** (unit, `scripts\l0-169-red-unit.txt`): "× place C:\repo\node_modules\react-day-picker\dist\esm\DayPicker.js in
  one library chunk", "× …/react-day-picker/dist/esm/locale.js…", "× …/date-fns/addDays.js…" — "Tests 4 failed | 13
  passed (17)". **Green:** "Tests 17 passed (17)".
- **Red** (the build, the group added, the calendar still drawn through the main barrel; `l0-169-checkbuild-red.txt`):
  `check:build` exit 1 — "_calendar-CpjILx3X.js is calendar's chunk in the site's first download."; first download
  1,140,164 bytes in 7 chunks (the calendar chunk 71,126 in it).
- **Red** (lint, the entry made but not allowed; `l0-169-red-entries.txt`): "× allows its calendar and date picker
  through their own entry" — `+ "feature → design-system (calendar.ts)"`. **Green** after `LAYER_ENTRIES`: "Tests 22
  passed (22)" (both script tests).
- **Green build:** `NODE_ENV=production npm run build` exit 0; `check:build` exit 0 — "No data-table or leaflet or
  calendar, nor Leaflet's stylesheet, in the site's first download."; **first download 1,064,781 bytes in 6 chunks**
  (`l0-firstDownload-head.txt`; design-system 281,292). Base for comparison: #127's head 1,140,210 (PR 1's
  measurement; `origin/main` is re-measured in the final verification), before #127 1,055,704.
- **Break** (the prompt's: the calendar drawn through the main barrel by a site page; `l0_break_169b.py`, backups
  `bak-l0-break-169b-*`, restored by copy, "restored True" ×2): `index.ts` re-exports `Calendar`, `HomePage` draws it →
  `check:build` exit 1 "_calendar-DqQTkaWf.js is calendar's chunk in the site's first download." (`l0-break-169b.txt`).
  A first try (`l0_break_169.py`, the calendar entry drawn by `SiteLayout`) stayed **green**: every site page and the
  site's shell are lazy, so a static import from them is outside the "first download" `check:build` guards (the
  entry and its static imports); the leak #127 met was the shared chunk's, which the barrel break reproduces.
  Recorded as LEAD-D3.
- Checks: the touched tests (`PaymentsLedger` 4 passed; `scripts` + showcase unit 160 passed); `npm run lint` 0;
  `npm run typecheck` 0; Prettier on the touched files clean; `check:links` "2938 links in 237 documents and 2109
  source files all resolve."

### Commit L0-2 — `cf0dcb0c fix(design-system): start a range on each click` (47 chars) — finding 173

- `Calendar.tsx`: in range mode `resetOnSelect` by default (`{...(props.mode === 'range' && { resetOnSelect: true })}`
  before the caller's props, so a caller may still set it); the `DateRange` and component comments say what a range
  click does. Test in `Calendar.component.test.tsx` ("starts a range on a first click, ends it on the second, and
  starts afresh on a third"). Docs: foundation §12's Calendar row, finding 173 → *Resolved*, the index. 5 files.
- **Red** (`l0-173-red.txt`): the first click gave `"to": 2026-09-06T21:00:00.000Z` for `undefined`, the third
  extended the range (`from` 7, `to` 14) — "Tests 1 failed | 10 passed (11)". **Green** (`l0-173-green.txt`): Calendar,
  DatePicker and the ledger's component tests (its F1 test included) "Test Files 3 passed (3) · Tests 20 passed (20)".
- `npm run lint` 0; `npm run typecheck` 0; Prettier clean; `check:links` all resolve.

### The seams — what Lane 0 holds and what it leaves (LEAD-D1)

- **Met:** the prompt asks for seams (the new pages' route entries, the copy namespaces) "if the catalogue's types
  allow it". The dashboard falls back to `PlaceholderPage` for a page with no entry, so an entry needs a page file;
  the copy index is alphabetical, and the three new sections sit in three separate places (`announcements` first,
  `dataReports` after `dashboard`, `favorites` after `errors`); the site's routes and navigation are lane C's alone.
- **Options:** (a) stub pages and empty copy sections in a `chore(web)` seam commit the lanes then fill; (b) no seam
  commit: each lane adds its own entries in their alphabetical places, and the joins keep both sides.
- **Chose (b).** A stub page or an empty catalogue section is scaffolding, not a unit (the prompt: "a seam commit
  only if it is a real unit"), and it would turn the plan's "A" files into "M" ones; the lanes' additions do not
  share lines. **Undo:** none needed; a conflict at the join is resolved by keeping both sides.
- **The real cross-lane dependency** is not a seam: PR 4a extends the `features/data-reports` that PR 3's commit 2
  creates. **LEAD-D2:** lane C first builds the heart icon (commit 3, independent) and reads, then hands over; once
  lane B's commit 2 exists, lane C rebases onto it and builds commits 1, 2, 4, 5, then puts its commits in the plan's
  order. Lane B hands over after its commit 2, before commit 3. *Undo:* none needed.

### Lane 0 — the lanes' setup

- Worktrees (`git worktree add -b lane/<x> C:\dev\masaha\app-lane-<x> feat/step10-screens`, at `cf0dcb0c`):
  `app-lane-a` (`lane/a`), `app-lane-b` (`lane/b`), `app-lane-c` (`lane/c`); `apps/web/.env` and `apps/api/.env`
  copied (not printed); `npm ci` one worktree at a time (exit 0 ×3); `npm run build -w @masaha/shared` (0 ×3).
  LEAD-D4: own worktrees rather than the Agent tool's isolation, so their paths, branches and installs are known.
- **The grant (LEAD-D5):** a sub-agent runs in the background and cannot wait on a question to the lead, so the
  lead's grant of a heavy run is a script the lead wrote, `scripts\heavy.mjs`: two slots (a directory made
  atomically), the free memory read before each grant (≥ 4 GB), a 2-minute wait between tries (45 at most), each
  grant, wait and end logged to `scripts\heavy-grants.log` (UTC times), which the lead reads. Every heavy run of the
  lanes and of the lead goes through it. *Undo:* the lead grants by message instead.
- Lane prompts: `scripts\lanes\LANE_COMMON.md` (the rules) and `LANE_A.md`, `LANE_B.md`, `LANE_C.md`. Finding ranges:
  A 174–175, B 176–177, C 178–179, the lead 180+.

### The base's first download and the data inventory (while the lanes ran)

- **`origin/main` (`76661f7c`) built** (detached in `C:\dev\masaha\app`, back on the branch after, tree clean;
  through the grant): first download **1,140,210 bytes** in 6 chunks, `design-system` 361,726
  (`lead-firstDownload-base.txt`) — #127's head's figure exactly.
- **The data inventory** (read-only; `scripts\inventory2.mjs` → `inventory2.out.txt`; four sign-ins, passwords read
  from `apps/api/.env`, never printed, no `/auth/` body kept; GETs only). `docker start masaha-postgres-1`
  (healthy); `npx prisma migrate status` "29 migrations … Database schema is up to date!"; the API on 3320, stopped by
  its process ids (24416, 15640, 21900), "listening: 0" after.
  - `demo-owner` = 14 «أحمد الشوا», OWNER of 7 (`masaha-demo`); `demo-reception` = 15 «ليلى النجار», RECEPTION of 7;
    `demo-directory-owner` = 39 «سامي الحلو», OWNER of 13 verified spaces (48 `noor-hub` …); the admin = 1.
  - Space 7's announcements: summary `{"running":0,"upcoming":0,"ended":0,"closuresAwaitingExtension":0}`; its page's
    `announcements: []`. (The list read answered 422: the inventory sent lower-case `state`; the contract's values
    are upper-case — a script slip, the summary answers the same question.)
  - Data reports: space 7's 0, the admin's 0, reception's own 0. Reception's favourites: none.
  - The directory: 59 listed; verified `noor-hub` (48, `demo-directory-owner`'s), unverified listed `tuffah-place`
    (56), `freelancers-house` (57); `masaha-demo` verified. No space has a running closure: the run's own closure on
    `masaha-demo` (PR 2's named write) is the one the space page's notice shows (PR 4b's case), taken while it runs.

## The lanes as they ran

- **LEAD-D6 — the lanes' reports returned as text.** The harness refuses a sub-agent's Write of a report file
  ("Subagents should return findings as text"); each lane returns its report in its reply, and the lead saves it as
  `scripts\lane-<x>\REPORT.md`. *Undo:* none needed.
- **Lane C, phase 1** (10:00): `f837a282 feat(design-system): add the heart icon` (39) — red, green, break #71 red;
  lint 0, typecheck 0 through the grant. Hand-over: waiting for lane B's commit 2. `scripts\lane-c\REPORT.md`.
- **Lane B, hand-over** (≈ 10:30): `0406e833` (FilterTag, 47), `a9096f31` (the owner's reports, 44); every break red;
  lint/typecheck 0 after fixes. `scripts\lane-b\REPORT.md`. Its one local miss, routes › "refuses reception the
  owner's payments with the 403 inside the shell", fails alone on Lane 0's files too (finding 55/87's family).
- Lane C continued with `<B2>` = `a9096f31` (rebase `--onto a9096f31 cf0dcb0c lane/c`); lane B continued with its
  commit 3.

- **Lane B DONE** (≈ 10:55): `lane/b` head `30d41fbb` (3 commits); lint 0, typecheck 0, `test:unit` 147/147 files
  (1028 tests), `test:component` 271/272 files (1606/1607) — the one miss below. `scripts\lane-b\REPORT.md`.
- **The routes miss, checked by the lead** (finding 55/87's family, LEAD-D7): routes › "refuses reception the owner’s
  payments with the 403 inside the shell" run alone in `C:\dev\masaha\app`: on Lane 0's head `cf0dcb0c` red 3065,
  3046, 3044, 3079 ms; on `origin/main` `76661f7c` passed once, then red 3045, 3089 ms — the same 3 s wait missed on
  the base, while three lanes loaded the machine. Not caused by any lane; re-run in the final verification (machine
  quiet) and CI judges.
- **Lane A DONE** (≈ 11:05): `lane/a` head `df4b8a88` (4 commits); lint 0, typecheck 0, `test:unit` 149/149 files
  (1038 tests), `test:component` 273/274 files (1620/1621) — the same routes miss only. `scripts\lane-a\REPORT.md`.

## The joins

- **Lane A** → `feat/step10-screens`: `backup/step10-pre-join-a` at `cf0dcb0c`; `git merge --ff-only lane/a` (lane A
  branched from the PR branch's head): `fcc42f60`, `8e64db2d`, `0ec5a23e`, `df4b8a88`, unchanged.
- **Lane B** → rebased onto the PR branch in its worktree (`backup/step10-lane-b-pre-join` at `30d41fbb`). Conflicts,
  each kept both sides (`scripts\join_resolve.py`, written for it): commit 2 — the routes test's imports (lane A's
  `../../test/announcement`, then lane B's `../../test/dataReport`) and architecture §2's *Built so far* line (lane B's
  «بلاغات البيانات» clause after lane A's «الإعلانات» one); commit 3 — the same import (lane B's line widened to
  `adminReport`, lane A's kept) and the same line (lane B's admin clause after «users»' actions, lane A's kept).
  Result `72d7d74e`, `ced180b1`, `89f07515`. On it: `npm run typecheck` 0, `npm run lint` 0 (through the grant);
  `routes.component.test.tsx` "Tests 1 failed | 61 passed (62)" — the known miss alone (3443 ms); the copy's unit
  tests (parity) "Tests 33 passed (33)". `backup/step10-pre-join-b` at `df4b8a88`; `git merge --ff-only lane/b`.
- Worktrees `app-lane-a` and `app-lane-b` removed (`git worktree remove`, both clean); branches `lane/a`, `lane/b`
  kept until the PR is open.

- **Lane C DONE** (≈ 11:50): `lane/c` head `b8f70b7d` on `a9096f31` (5 commits in the plan's order); lint 0,
  typecheck 0, `test:unit` 149/149 files (1032 tests), `test:component` 284/285 files (1650/1651) — the routes miss.
  `scripts\lane-c\REPORT.md`.
- **Lane C** → rebased in its worktree with `git rebase --onto feat/step10-screens a9096f31 lane/c`
  (`backup/step10-lane-c-pre-join` at `b8f70b7d`). Conflicts against lane B's commit 3 (both added beside the owner's
  parts), each kept both sides, the admin's first and the user's after (`scripts\join_c1.py`, `join_c1_docs.py`,
  `join_c2.py`, `join_resolve.py`):
  - commit 1: `hooks/queryKeys.ts` (the type import merged `AdminReportsQuery, MyReportsQuery, SpaceReportsQuery`; the
    `adminAll`/`admin` keys, then `mineAll`/`mine`), `index.ts` (the admin's exports, then `MyReportsList`), the
    repository (`adminReports`, `decideAdmin`, then `myReports`, in the interface and the factory), its unit test (the
    fixtures' import merged; the admin's tests, then the user's), copy `dataReports.ts` ×2 (the `admin` section, then
    `mine`), `src/test/dataReport.ts` (the import merged; `adminReport()`, then `myReport()`), `data-reports.md` (the
    authority and scope lines naming both, the admin's and the user's *Behaviour* paragraphs, the code map naming both
    pages, both *Web history* lines), `overview.md` (the user's clause after the admin's), architecture §2's line (the
    account's clause and "the account's settings (screen 9)" applied onto the joined line);
  - commit 2: the repository's type import (`CreateReportRequest` added), the findings index (167 then 168),
    `data-reports.md` (the report's words added onto the joined lines);
  - commit 4: architecture §7's invalidation line (the favourites' sentence after the announcements' one);
  - commit 5: architecture §2's line (the account's «المفضّلة» clause), `overview.md`'s Favourites line. A first
    resolution of the latter duplicated three lines (a multi-line hunk joined whole); caught at once by a diff against
    the joined side, redone from it with the one change; no commit carried it.
  - **The check:** every file whose lane-C content changed in the join is one lane A or B also touched; every file the
    joined branch differs in from the PR branch is one lane C changed (scripted comparison, nothing unexpected).
  Result `9651782a`, `2f577f37`, `2b96ac52`, `7570e69a`, `d2079b42`. On it: typecheck 0, lint 0 (the grant);
  `routes` (dashboard and site) + `features/data-reports` "Tests 2 failed | 124 passed (126)" — the routes 403 miss
  (7171 ms) and site routes › "shows the Directory under its title" (3028 ms, finding 87's "site tests opening
  `/spaces`"; the site routes file alone "Tests 13 passed (13)"); data-reports + copy unit "Tests 56 passed (56)".
  `backup/step10-pre-join-c` at `89f07515`; `git merge --ff-only lane/c`; worktree `app-lane-c` removed.

## Commit 6 — `48715d8c feat(announcements): show a space's announcements` (49 chars) — by the lead, on the joined branch

- `features/announcements`: `services/runningClosure.ts` (+ unit), `types/PublicAnnouncement.ts`,
  `hooks/public/usePublicAnnouncements.ts`, `components/public/SpaceAnnouncements.tsx` (+ test),
  `ClosureNotice.tsx` M — `ClosureNotice({ items })` (the page's) beside `ClosureAlert({ item, notice })` (the
  presentational warning, which the sheet's preview now imports) (+ test), `index.ts` (`ClosureNotice`,
  `SpaceAnnouncements`). `features/directory`: `SpacePageView.announcements`, `useSpacePage`, `SpaceDetails`'s
  `notice` slot (above the page, in a wrapper `empty:hidden lg:col-span-12` so no closure takes no gap) and
  `announcements` slot (after the status card, before the prices — one place serves both widths, the status
  being the aside from 1024 px). `pages/site/public/space/SpacePage.tsx` sets both; its test gains U8's order at 390 and
  1440. Fixture `publicAnnouncement()` in `src/test/announcement.ts`. Docs: `announcements.md` (scope, *Who uses
  it*, DI-59's web decision, code map, *Web history*), `directory.md` (the page's announcements, decision 4's line,
  the open findings, *Web history*), `overview.md`, finding 131 → *Resolved*, the index. 22 files.
- **Red** (`c6_red.py`: the new files removed and the changed ones put back as at HEAD, then restored by copy,
  "restored True"; `c6-red.txt`): unit "Cannot find module './runningClosure'"; component "Failed to resolve import
  "./SpaceAnnouncements""; `ClosureNotice` ×3 "TypeError: Cannot read properties of undefined (reading 'text')"; the
  space page ×2 "Unable to find an accessible element with the role "status"" — "Tests 5 failed | 4 passed (9)".
  The unit file was first seen red alone before its code ("Cannot find module './runningClosure'",
  `c6-red-unit.txt`). **Green:** unit 5/5; public components + sheet 8/8; space page 6/6; then announcements +
  directory page components "Test Files 13 passed (13) · Tests 73 passed (73)", announcements + copy unit 66/66.
- **Breaks** (`c6_breaks.py`, each from a backup copy, restored by copy, "restored True"): **82** `>=` on the end →
  "× passes over a closure ending at now" ("expected { id: 1, type: 'CLOSURE', …(4) } to be null"); **83** the closure
  repeated (the filter dropped) → "× lists the others by their start, the running closure not repeated…", "× draws
  nothing when only the running closure…", and both U8 order tests; **84a** the announcements after the prices → both
  U8 order tests "expected false to be true"; **84b** the notice drawn after the head → both red (re-run after the
  test's selector was reworded for lint: red again).
- Checks: typecheck 0; lint 1 (`no-unnecessary-condition` on an optional chain in the new test) → the notice found by
  `getByText(…, { selector: '[role="status"] *' })` → lint 0; `check:links` "2982 links in 239 documents and 2278
  source files all resolve."; `check:classes` "No physical direction or arbitrary-value classes in 1656 files.";
  Prettier clean.
- **LEAD-D8 — the public pieces' types and split.** *Met:* §9 says `ClosureNotice({ items })` exported, while lane A's
  sheet preview draws `ClosureNotice({ item, notice })`; `features/announcements` may not import
  `@masaha/shared/directory` (its `PublicAnnouncement`). *Chose:* the presentational warning renamed `ClosureAlert`
  (the preview's), `ClosureNotice({ items })` the page's; a local `PublicAnnouncement` type as `Pick<Announcement,
  …>` of the same fields; one hook (`usePublicAnnouncements`) builds both views. *Undo:* rename back and pass views.
- **LEAD-D9 — the warning is the layer's polite `role="status"`.** The layer's warning `Alert` is announced politely
  (only `destructive` is `role="alert"`); a notice present when the page loads is no interruption, so the layer's
  rule is kept. Lane A noted the same for the sheet's preview. *Undo:* pass `role="alert"`.

## The final verification

### First pass, on `48715d8c` (commit 6 as first made)

- `npm run build -w @masaha/shared` 0; `npm run lint` 0; `npm run typecheck` 0; `npm run test:unit` (every workspace):
  shared "Test Files 25 passed (25) · Tests 263 passed (263)", api "71 passed (71) · 879 passed (879)", web "157
  passed (157) · 1071 passed (1071)"; `npm run test:api` (beside the others, through the grant) "Test Files 97 passed
  (97) · Tests 1246 passed (1246)".
- `npm run test:component`: **"Test Files 3 failed | 297 passed (300) · Tests 2 failed | 1724 passed | 6 skipped"** —
  `SpacePage.component.test.tsx`'s `beforeAll` (lane C's preload of the lazy page, LC-17) "Hook timed out in 10000ms"
  (its 6 tests skipped), site routes › "shows a space’s page titled by its name; at 1440…" (5 s), dashboard routes'
  403 (known). Alone, on a quiet machine: the site routes' space page test still red (5,014 ms twice), while on lane
  C's head `d2079b42` the same file passed "13 passed (13)" twice: **commit 6 made the space page's cold load slower.**
- `NODE_ENV=production npm run build` 0; `check:build` 0 (all three lines); first download 1,094,709 bytes.
- **Check 5.k** (`scripts\check5k.mjs` over the manifest): the space page's chunk reaches `data-table` and `calendar`
  (×2), «بلاغاتي»'s reaches `data-table`; every other site page none. → **finding 180** (LEAD-D10, below).

### The cause, found (LEAD-D11 — not SERIOUS: a test-lane timing defect, fixed at its root)

- A probe test (temporary, never committed; `src/zzprobe`, removed) timed cold imports in the component lane:
  `@features/directory` 4,170 ms (the shared modules), then `data-reports` 549, `favorites` 90, **`announcements`
  4,264**, `SpacePage` 1,144 — and split further: **`react-day-picker` 3,260 ms**, then its locale barrel 396, the
  calendar entry 63, `announcements` only 478. The calendar's library, read module by module with date-fns's
  hundreds of files, costs a test file ≈ 3.3 s on its first import: the space page paid it once it set
  `announcements`' pieces (whose entry reaches the sheet's date fields), and so has `PaymentsPage` since #127 — the
  routes test's 403 that missed locally on `main` too.
- **Tried and dropped** (each recorded, nothing committed of it): a `beforeAll` preload in the site routes test (green
  alone twice, but in the full lane its own hook passed 10 s and skipped 13 tests); loading `announcements`' public
  pieces lazily in `SpacePage` (the cost then fell on the file's next tests: "Home’s search…" 3.8 s); the calendar's
  locales by subpath (`react-day-picker/locale/ar`, `/en-US`: −0.5 s only, not the cause). Each reverted from backup
  copies / `git show HEAD:` into the file, a fold redone so commit 6 is again exactly its first content (`git diff
  backup/step10-pre-fold-preload` empty for those files).
- **Chose:** the component lane pre-bundles `react-day-picker` with Vitest's documented dependency optimizer (one
  config entry, `deps.optimizer.client`, on the component project; the build untouched): the probe's
  `react-day-picker` 3,260 → 8 ms; the three slow files (site routes, space page, dashboard routes) "Test Files 3
  passed (3) · Tests 81 passed (81)" twice — the dashboard's 403 included, which misses on `main` locally. Its own
  commit, `test(web): pre-bundle the calendar for jsdom` (44), placed in Lane 0 after `cf0dcb0c` (scripted reorder,
  `backup/step10-pre-reorder`; the tree identical after). Its red: the same tests red without it (the runs above).
  *Undo:* drop the commit; the tests then miss their waits on a slow machine.

### Finding 180 (LEAD-D10)

- Recorded (the plan's conditional finding, check 5.k; the lead's range): "A site page's chunk reaches the table's and
  the calendar's libraries" — through `data-reports`' and `announcements`' one entry, which also exports their
  dashboard screens; sizes `data-table` 37,286, `calendar` 71,119 + 4,564 bytes; not in the first download. Folded
  into commit 6 with its index line and a line in `announcements.md` and `data-reports.md` (*Open findings*).
  *Undo:* drop the file and the lines.

### Second pass, on the head `ab5f72bd` (16 commits)

- `npm run build -w @masaha/shared` 0; `npm run lint` 0; `npm run typecheck` 0.
- `npm run test:unit`: shared "25 passed (25) · 263 passed (263)"; api "71 passed (71) · 879 passed (879)"; web
  "157 passed (157) · 1071 passed (1071)".
- `npm run test:component`: "Test Files 1 failed | 299 passed (300) · Tests 1 failed | 1731 passed (1732)" (443.59 s,
  free memory 5,997,116 KB before) — the one: `authPages` › /login › "sends a signed-in user on to the page they came
  for, under RequireGuest" (3,038 ms, "expected '/login?next=%2Fabout' to be '/about'"), a file this PR does not touch
  (finding 87's family, its sibling `changePasswordPage` is named there); alone "Tests 14 passed (14)" twice. The space
  page, the site routes and the dashboard routes all passed in the full lane.
- `npm run test:api` (beside, through the grant): "Test Files 97 passed (97) · Tests 1246 passed (1246)".
- `NODE_ENV=production npm run build` 0; `npm run check:build` 0 — "No showcase code in 73 build files (1011 strings
  checked).", "No dashboard code in the site's first download.", "No data-table or leaflet or calendar, nor Leaflet's
  stylesheet, in the site's first download."
- `check:classes` "No physical direction or arbitrary-value classes in 1656 files."; `check:links` "2987 links in 240
  documents and 2278 source files all resolve."; `check:conflicts` "No conflict markers found."; `format:check` "All
  matched files use Prettier code style!".
- **The first download:** base `origin/main` **1,140,210** → head **1,094,709** bytes (6 chunks; −45,501): design-system
  361,726 → 282,145 (finding 169), `jsx-runtime` 190,119 → 215,462 (Rolldown's shared chunk; no feature module's code
  in it — the entry's strings `/me/favorites`, `data-reports`, `/announcements` are its route paths and preload lists).
  Against Lane 0 alone (1,064,781) the screens add 29,928.

## A defect found in the real run, fixed (LEAD-D12)

- **Met:** PR 4b's guest case: a guest's heart on `sada-space` → the prompt → «Sign in» → back on the page, the
  favourite saved (`POST /api/v1/me/favorites/49 204`, no key) and said («حُفظت Sada Space في المفضّلة»), but the
  page's heart read `aria-pressed="false"` 3 s later; on a reload it read `true`. Reproduced in the component lane
  with a server that holds the save (a new test in `SpacePage.component.test.tsx`, "shows the heart pressed once a
  guest’s held favourite is saved on their return"): red — "Unable to find role="button" and name `/^Remove .Noor
  Hub. from favourites$/`" (`fix-heart-red.txt`).
- **Cause** (instrumented from backup copies, restored): on the return, the hearts' first `GET /me/favorites` is still
  on its way when the held save lands; `writeFavorite` then invalidates `['me']`, and TanStack Query's invalidation
  joins a first read that has no data yet instead of restarting it (`fetch` cancels an in-flight read only when the
  query has data), so the ids keep the answer from before the save — no second read was sent.
- **Fix** (`features/favorites/hooks/favoriteWrite.ts`): the in-flight reads of `['me']` cancelled, then invalidated, so
  the read starts again after the write (the requests then: `post /me/favorites/7`, `get /me/favorites` with it saved).
  Green: the space page and `features/favorites` "Tests 20 passed (20)"; `features/directory`, `features/favorites`,
  `pages/site` "Test Files 34 passed (34) · Tests 180 passed (180)"; lint 0; typecheck 0. Folded into
  `feat(favorites): save a space from its card` (now `78bf71e1`; `backup/step10-pre-fold-heart`). Not SERIOUS by §6's
  list (no money, role or private data): a favourite saved but shown unsaved until the next read. *Undo:* revert the
  three lines; the heart then lags until a refetch.
- Not re-shown in the browser: a second guest save would be a write beyond §13's list; the test owns the proof.

## The real run (2026-10-28, `masaha_dev`; scripts `run2.mjs`, `run2-ann.mjs`, `run2-breaks.mjs` on `cdp2.mjs`; shots `shots\lead\`)

- The API on 3320 and the web on 5320 (`npm run dev`), started for the run; `masaha-postgres-1` up. Headless Chrome over
  CDP; Enter sent with its text; no `/auth/` body kept; no phone printed. Every line below is from
  `scripts\run2-log.txt` and the cases' output.
- **PR 3 — before the run, the named script** (`reports3.mjs`, as `demo-reception`, `POST /api/v1/spaces/:slug/reports`):
  `masaha-demo` HOURS «تجربة: الساعات» → 201 id 1; `noor-hub` (verified, `demo-directory-owner`'s) PRICES → 201 id 2;
  `tuffah-place` (unverified, listed) OTHER «تجربة: أخرى» → 201 id 3.
- **PR 3, the owner** (ar 1440): «بلاغات البيانات» — "بلاغ واحد", the report «زائر · 28 أكتوبر», the day only; «فتح» → the
  sheet «بلاغ عن ساعات العمل», **its first focus on the reply's textarea** (LB-D7 confirmed in a browser); the reply
  «صحّحنا الساعات», «تم التصحيح» → toast «عُلّم «تم التصحيح» | في «تمت المراجعة» | أُرسل الردّ لصاحب البلاغ. | عرض»; the
  focus back on «فتح»; `PATCH /api/v1/manage/spaces/7/data-reports/1 200 Idempotency-Key: none body:
  {"status":"RESOLVED","note":"صحّحنا الساعات"}`. Shots `3-owner-*` (ar light / en dark × 390, 768, 1440).
- **PR 3, the admin** (ar 1440): the intro, the chips, «المساحة» / «كل المساحات», «الحقل»; 3 rows, the reporter named
  (ليلى النجار) and «يعالجه» (الإدارة / المالك); the space combobox searched «نور» → «كل المساحات | نور هب» → the address
  `?space=48` and the tag «إزالة فلتر المساحة» (shots at 1440, 390, 768); the verified space's report «عرض» → read-only
  «مساحة موثّقة — يقرّر مالكها هذا البلاغ. للاطلاع فقط. | عرض المساحة»; «مسح الفلاتر» → the address empty; tuffah-place's
  «فتح» → «ردّ فريقنا», the reply «تجربة: لا يلزم تعديل», «لم يُعتمد» → `PATCH /api/v1/admin/data-reports/3 200
  Idempotency-Key: none body: {"status":"DISMISSED","note":"تجربة: لا يلزم تعديل"}`. English dark at 390, 768, 1024 (the
  table from 1024, cards below), 1440.
- **PR 4a** (reception): «بلاغاتي» — 3 reports, «ردّ فريقنا» / «ردّ إدارة المساحة» with the replies, the chips, the
  account's navigation «حسابي» (ar/en × 390, 768, 1440). From `noor-hub`'s page: «الإبلاغ عن معلومة غير صحيحة» → the
  dialog «بلاغك عن نور هب يصل إلى إدارة المساحة، وتجد ردّها في «بلاغاتي».», its first focus on the field's select;
  «المرافق», «إرسال» → toast «أرسلنا بلاغك إلى إدارة المساحة. ستجد ردّها في «بلاغاتي». | عرض بلاغاتي»; the focus back on
  the button; `POST /api/v1/spaces/noor-hub/reports 201 Idempotency-Key: none body: {"field":"AMENITIES"}`. **The same
  again** → info toast «أرسلت بلاغًا عن هذا من قبل، وما زال قيد المراجعة.»; `POST … 200` (the open one, S15). **As a
  guest** (en): the button → «Sign in to report information», «Create account → /register?next=%2Fspaces%2Fnoor-hub |
  Sign in → /login?next=%2Fspaces%2Fnoor-hub» → signed in → back on `/spaces/noor-hub` with the report's dialog open →
  closed, **0 writes**.
- **PR 4b** (reception): a Directory card's heart «Save Radwan Study Hall to favourites», **pressed at once** (`true`
  before the answer), toast «Added to favourites | Radwan Study Hall | Undo» → «Undo» → not pressed; `POST
  /api/v1/me/favorites/51 204 Idempotency-Key: none`, `DELETE /api/v1/me/favorites/51 204 Idempotency-Key: none`. Home's
  first card (ar) → «أُضيفت إلى المفضّلة | قاعة الرضوان للدراسة | تراجع», `POST …/51 204`. `noor-hub`'s page at 390: the
  heart in the name's block → saved, `POST …/48 204`. **The guest's heart** on `sada-space` → «Sign in to save spaces to
  your favourites» → signed in → toast «حُفظت Sada Space في المفضّلة», `POST …/49 204`, and the heart unpressed:
  **LEAD-D12's defect, fixed** (above). «المفضّلة»: «3 مساحات محفوظة», the cards with their status; «الأقرب إليّ» (the
  device's point by CDP geolocation, the permission granted) → «مرتبة حسب المسافة من موقعك…», 0.3 / 1.5 / 2.5 km, `GET
  /api/v1/me/favorites?sort=distance 200`; a card's heart → «أُزيلت من المفضّلة | نور هب | تراجع» → «تراجع»; `DELETE …/48
  204`, `POST …/48 204` (no key). Shots ar/en × 390, 768, 1440.
- **PR 2, reception** (en 1440): «New announcement» → the sheet, its first focus on the checked type's radio; General,
  «إعلان تجربة», «No end»; **the post offline** (CDP) → the sheet's lost line «No answer came back. Try again — it won’t be
  published twice.» with «Try again» → online, «Try again» → toast «Announcement published | In “Active” | Show». **The
  network log: four `POST /api/v1/manage/spaces/7/announcements`, all `Idempotency-Key:
  1cc56cf9-aa48-4979-9be2-7eb3265e90f8` — three `failed (net::ERR_INTERNET_DISCONNECTED)` (the transport's re-sends), then
  201; one announcement** («Active 1»). The first script then stopped at the «Ended» tab (Radix's tabs change on a mouse
  press, not a click), so the next writes' network lines were not kept; **the audit log** of space 7, read after as the
  owner (`auditcheck.out.txt`), gives them in order: `announcement.edited` 13:29:21 (its English text; «Announcement
  saved»), `announcement.ended` 13:29:24 («The announcement has ended | In “Ended” | Undo»), `announcement.edited`
  13:29:26 («Undo» → «The announcement is back as it was»), `announcement.ended` 13:29:28 (the focus on the «Active» tab
  once the card left). Continued (`annReception2`): «Ended» → «⋯» → «Delete…» → «Delete the announcement “General · 28
  October 15:29–15:29”? | It leaves this list. It can’t be brought back.» → `DELETE …/announcements/2 204` (no key); an
  Offer «عرض تجربة» from **29 October 09:00** (the calendar and the time) → `POST …/announcements 201 Idempotency-Key:
  9b2acc81-… body: {"type":"OFFER","textAr":"عرض تجربة","startsAt":"2026-10-29T07:00:00.000Z"}` (Gaza's 09:00 that day) →
  «Scheduled» → «Start now» → `POST …/announcements/3/start 200` (no key) → «Delete…» («It leaves the space’s page at
  once…») → `DELETE …/3 204`.
- **PR 2, the owner**: a Temporary closure «إغلاق تجربة» from **27 October 08:00** (yesterday), no end, its line «Visitors
  see the space as “Closed now”…», the preview the closure's notice → `POST …/announcements 201 Idempotency-Key:
  2f246030-… body: {"type":"CLOSURE","textAr":"إغلاق تجربة","startsAt":"2026-10-27T06:00:00.000Z"}`; reception's card reads
  «يمدّد المالك الاشتراكات بعد بدء الإغلاق.», the owner's offers «تمديد الاشتراكات» (shots `2-active-*`, both roles, ar/en
  × 390, 768, 1440). **While it ran, the space page as a guest** (ar/en × 390, 768, 1440): the notice «إغلاق تجربة |
  إعلان من إدارة المساحة · من 27 أكتوبر 08:00 · بلا نهاية» above the name at every width, the status «مغلق الآن»; no
  announcements section (the running closure was the only one, DI-59). Then «End now» → «The closure has ended · the
  status is automatic again | In “Ended” | Undo», `POST …/4/end 200`; «Extend subscriptions» → `GET
  …/4/extend-subscriptions 200`, the dialog «The extension moves 4 subscriptions. | Those the closure covered, and their
  renewals not started yet… | The closure’s days: 2 days (27 October – 28 October)», its first focus on the days; **1
  typed** → «Extend 4 subscriptions» → `POST …/4/extend-subscriptions 201 Idempotency-Key: dcb8f9db-… body: {"days":1}`;
  toast «Subscriptions extended | 4 subscriptions · 1 day»; the card «Extended 4 subscriptions · 1 day · أحمد الشوا · 28
  October | Its subscriptions were extended, so it isn’t deleted and its end isn’t moved later.» **The preview's count
  4; the subscriptions moved: 4** (#128's count: those the closure covered and their renewals not started). Shots
  `2-ended-*` (both roles, ar/en × 390, 768, 1440).
- **Width breaks** (from backup copies, restored by copy, "restored true"): the sheet's date and time at 768 `162px
  162px`, with `sm:grid-cols-2` removed `336px` (one column, `break-sheet-period-reception-ar-light-768.png`); at 390
  one column (357px) in both languages. The favourites' grid at 1440 `290.656px 290.672px 290.656px`, with
  `xl:grid-cols-3` removed `444px 444px` (`break-favorites-grid-reception-ar-light-1440.png`; a first try replaced only
  the first of the file's two grids, the gone spaces', and stayed three: redone on both).
- **Touch targets** at 390 with touch emulation: the announcements' «⋯» 44×44; the page's heart 44×44; a card's heart
  44×44; `FilterTag`'s remove button 44×44.
- **The refresh limit:** after ≈ 40 sign-ins the API answered `POST /auth/refresh` 429 (30 per 15 minutes): the last
  two sessions came up as a guest (a card's heart then read «حفظ»; its size stands). The account menu's case waited for
  the window.
- **Not performed, by design:** a 429 on a dialog (their tests own it); `FAVORITES_LIMIT_REACHED` (200 saves); «إزالة» of
  a space that left the directory (no favourite of reception's has left, and the data is never changed to make one —
  test 81 owns it); a second guest save to show LEAD-D12's fix in a browser (a write beyond §13; the new test owns it);
  the announcements section beside a running closure (no other announcement ran then; tests 83, 84).
- **The account menu** (reception, after the refresh window): desktop (ar 1440) «المفضّلة → /me/favorites | بلاغاتي →
  /me/reports | لوحة التحكم → /dashboard | تسجيل الخروج»; the phone menu (en 390) «… | Favourites → /me/favorites | My
  reports → /me/reports | Dashboard → /dashboard». Shots `4a-account-menu-*`.
- The servers stopped by their process ids (the API's tsx watch, server and pino; Vite), then once more after a short
  read-only start for the audit entry below; `Get-NetTCPConnection -LocalPort 3320,5320 -State Listen` → "listening: 0".

### Every write of the run, and what it left in `masaha_dev`

- **Data reports:** 1 (`masaha-demo` HOURS «تجربة: الساعات», RESOLVED by the owner, reply «صحّحنا الساعات»); 2
  (`noor-hub` PRICES, OPEN — a verified space's, the owner's to decide); 3 (`tuffah-place` OTHER «تجربة: أخرى», DISMISSED
  by the admin, «تجربة: لا يلزم تعديل»); 4 (`noor-hub` AMENITIES, OPEN, from the page; its repeat wrote nothing). All
  by `demo-reception`.
- **Favourites of `demo-reception`:** 48 `noor-hub` (saved on its page; removed and restored by «تراجع» on «المفضّلة»),
  49 `sada-space` (the guest's, on the return), 51 `radwan-study-hall` (Home's; the Directory's save had been undone).
- **Announcements of space 7:** 2 «إعلان تجربة» (GENERAL; posted, edited, ended, undone, ended, deleted), 3 «عرض تجربة»
  (OFFER; posted, started, deleted) — both deleted (soft); 4 «إغلاق تجربة» (CLOSURE, 27 October 08:00 → ended 28
  October 15:39, **extended**) — stays, in «منتهية».
- **The extension (the approval note's write, 1 day, no undo):** the audit entry `closure.subscriptionsExtended` →
  `{"days":1,"subscriptionIds":[3,5,7],"renewalIds":[6]}` — subscriptions 3, 5 and 7 of `masaha-demo` and the renewal 6
  moved by one day: the preview's 4.
- Nothing else was written: every other request of the run was a GET (the network logs, `run2-log.txt`).

### Third pass, on the head `921b1a2e` (after LEAD-D12's fold)

- `npm run test:component`: **"Test Files 300 passed (300) · Tests 1733 passed (1733)"** (397.63 s) — no miss.
- `npm run test:unit -w @masaha/web`: "Test Files 157 passed (157) · Tests 1071 passed (1071)".
- `npm run lint` 0; `npm run typecheck` 0; `NODE_ENV=production npm run build` 0; `check:build` 0 (the three lines);
  first download 1,094,709 bytes; `check:classes` (1656 files), `check:links` (2987 links), `check:conflicts`,
  `format:check` — all pass. `test:api` and the shared/api unit lanes: the second pass's (only web files changed since).

## Push, the PR, CI

- Just before the push: `origin/main` `76661f7c` (unmoved); open PRs none; `gh api "repos/Basel-Ghonaim/masaha/issues?state=all&per_page=1" --jq '.[0].number'` → 128, so **129**.
- `scripts\prnum-lead.sh 129` (a temporary branch rewritten by `git filter-branch --tree-filter` over `origin/main..`,
  checked — no `#PRNUM` in any commit's tree, only number lines changed, the same files, commits and subjects — then
  the branch moved onto it; no `reset --hard`): "PRNUM OK #129 fcf46637 (was 921b1a2e)"; `git diff
  backup/step10-pre-prnum HEAD`: 16 files, 94 lines, every one a `#PRNUM` → `#129`; the description's `#PRNUM` none.
- `git push -u origin feat/step10-screens` (a new branch); `gh pr create --assignee @me --label feat --label area:web
  --label area:docs --label area:design-system --title "feat(web): announcements, data reports, favourites"` (50) →
  **https://github.com/Basel-Ghonaim/masaha/pull/129** — the number the commits carry; no second push.
- **CI on `fcf46637bf84ab2de598abf0f8080bb42f8964f2`:** build pass (39 s), check:classes pass, check:conflicts pass,
  check:links pass, format:check pass, lint pass (1m53s), test:api pass (6m6s), test:component pass (4m53s), test:unit
  pass (1m18s), typecheck pass (52 s); CodeRabbit skipping. `mergeStateStatus` **CLEAN**; 248 files.
- No `Co-Authored-By`, "generated with" or tool name in any commit message; no `fixup!` left.

## The commits (final)

`4ebc2785 perf(design-system): serve the calendar on its own` (50) · `18db0601 fix(design-system): start a range on
each click` (47) · `a23896a7 test(web): pre-bundle the calendar for jsdom` (44) · `ddaa3db2 feat(announcements): list a
space's announcements` (49) · `74000c57 feat(announcements): post and edit an announcement` (50) · `2279134a
feat(announcements): end, start or delete one` (45) · `2fa45cf8 feat(announcements): extend after a closure` (43) ·
`7d892c86 feat(design-system): add a removable filter tag` (47) · `44e8ee1f feat(data-reports): decide a space's
reports` (44) · `dc427a54 feat(data-reports): list every space's reports` (46) · `fda9559c feat(data-reports): show a
user's own reports` (45) · `c9739dcd feat(data-reports): report wrong information` (44) · `97ec50fe
feat(design-system): add the heart icon` (39) · `1285d9ab feat(favorites): save a space from its card` (43) ·
`0b75e262 feat(favorites): list a user's favourite spaces` (47) · `fcf46637 feat(announcements): show a space's
announcements` (49).

## Memory and the grants

- Every heavy run went through `scripts\heavy.mjs` (`scripts\heavy-grants.log`, UTC): two slots at most, ≥ 4 GB free
  at each grant. Waits: lane C's typecheck once ("both slots taken", 10:42). **No kill** in any lane or in the lead's
  runs. Free memory before the lead's full lanes: 5,734,580 KB (first component pass), 5,997,116 KB (second), 4,972,360
  KB (the pass with the preload that skipped a file's tests — a hook timeout, not a kill).

## Decisions taken without the owner

None **SERIOUS** (§6's list: no money, role, private data, plan decision or redesign touched).

- **LEAD-D1** — no seam commit; each lane added its own entries (alphabetical, apart). *Undo:* none needed.
- **LEAD-D2** — PR 4a waits on PR 3's commit 2: lane C built the heart first, then rebased onto lane B's commit 2.
- **LEAD-D3** — finding 169's break made through the main barrel from a site page (Home); a first break from the site's
  lazy shell stayed green, since a lazy page is outside the first download `check:build` guards.
- **LEAD-D4** — the lanes' worktrees made by the lead (`git worktree add`), not by the Agent tool.
- **LEAD-D5** — the heavy runs' grant by a script (two slots, ≥ 4 GB, logged), since a background sub-agent cannot wait
  on a question. *Undo:* grant by message.
- **LEAD-D6** — the lanes' reports returned as text (the harness refuses a sub-agent's report file) and saved by the lead.
- **LEAD-D7** — the routes test's 403 miss checked on `main` and Lane 0 (red on both under load) → later found to be
  the calendar's cold import (LEAD-D11).
- **LEAD-D8** — the public pieces: `ClosureAlert` (presentational, the sheet's preview) and `ClosureNotice({ items })`
  (the page's), a local `PublicAnnouncement` type (the feature may not import the directory's). *Undo:* rename back.
- **LEAD-D9** — the closure's notice keeps the layer's polite `role="status"` for a warning. *Undo:* `role="alert"`.
- **LEAD-D10** — finding 180 recorded (check 5.k: the space page's and «بلاغاتي»'s chunks reach `data-table` /
  `calendar` through the features' one entry). *Undo:* drop the finding.
- **LEAD-D11** — react-day-picker pre-bundled for the component lane (`deps.optimizer.client`), its own Lane 0 commit;
  a test preload, a lazy load of the page's pieces and the locales by subpath tried and dropped. *Undo:* drop the
  commit.
- **LEAD-D12** — the real run's defect (a guest's favourite saved on the return but shown unpressed): the scope's
  in-flight reads cancelled before the invalidation, with a test, folded into `feat(favorites): save a space from its
  card`. *Undo:* revert the three lines.
- **The lanes' decisions** (each in its report): lane A LA-D1–D15 (LA-D1: #128's count worded «يشمل التمديد {n}
  اشتراكات.» with its line); lane B LB-D1–D17; lane C LC-D1–D21. None SERIOUS.
- **Observation, not a decision:** while the favourites' ids are on their way, a heart is drawn unpressed (S13's
  design); a press then saves again (204, idempotent).

## Leftovers

- **Branches (local):** `feat/step10-screens` (the PR's); backups `backup/step10-pre-join-a`, `-pre-join-b`,
  `-pre-join-c`, `backup/step10-lane-b-pre-join`, `backup/step10-lane-c-pre-join`, `backup/step10-pre-fold-180`,
  `-pre-fold-preload`, `-pre-unpreload`, `-pre-reorder`, `-pre-fold-heart`, `-pre-prnum` (all mine; kept for the
  owner; delete after the merge). The lane branches `lane/a`, `lane/b`, `lane/c` deleted once the PR was open.
- **Worktrees:** `app-lane-a`, `app-lane-b`, `app-lane-c` removed (`git worktree remove`; their leftover
  `node_modules\@masaha` junctions deleted, the folders gone). `app-b`, `app-design`, `app-review` untouched.
- `git status --short` clean in `C:\dev\masaha\app`; ports 3320 and 5320 free; `masaha-postgres-1` left running (it was
  running at the start).
- Outside the repository: this report, `scripts\` (the lanes' folders, the run's scripts and logs, the backups) and
  `shots\lead\`.

## Not run locally, or not as planned

- The final-report skill's format: the prompt's §9 reply and this report are the ones the owner asked for.
- Nothing else: every lane of §5 ran on the head, and CI ran them all again.
## The reviews' fix round (2026-10-28)

From `6_REVIEW_LEAD_R1_CLAUDE_CODE.md`, `…_R2_…`, `…_R3_…` and `7_FIX_ROUND_LEAD.md` (the owner: every finding fixed,
nothing carried; R3-F1 option (a) on DI-58). Done by the lead alone, no sub-agents; worker B ran on the machine.

### The base

- `git fetch origin`: `origin/main` `76661f7c` (unmoved); `gh pr view 129 --json mergeStateStatus` → `CLEAN` → **no
  rebase**. `backup/step10-pre-review-fix` at `fcf46637` before the first fold.

### Each fix (the red before the fix, the green after, the break; outputs in `scripts\fixround\`)

- **R1-F1 (blocker)** → `feat(announcements): post and edit an announcement`. `editRequestOf` decides "changed" at the
  sheet's precision: the typed Gaza date and minute against the loaded instant's `gazaClockOf` date and minute
  (`sameMinute`), start and end alike. Tests: `sheetRequest.unit.test.ts` (a loaded start `…T05:00:42.123Z` and end
  `…T15:00:07.900Z`: nothing changed → `{}`, only `textEn` → `{ textEn }`, the start or the end moved one minute → sent on
  the minute typed); `useAnnouncementSheet.component.test.tsx` («Save» untouched on a start posted «now» says «Nothing
  changed», sends nothing) with the fixture `announcementPostedNow()` in `src/test/announcement.ts`. **Red:** "× sends
  nothing for a start and an end the user did not move, though loaded with their seconds", "× sends a start or an end
  moved by one minute, on the minute typed" — "Tests 2 failed | 10 passed (12)"; the component "× says nothing changed
  for a start posted «now»…" — "Tests 1 failed | 8 passed (9)" (`r1f1-red-comp.txt`, `sheetRequest.ts` as at `fcf46637`).
  **Green:** 12/12 and 9/9. **Break:** the code as before (millisecond compare) — the same reds. `announcements.md`'s
  sheet paragraph says it.
- **R1-F2** → `feat(announcements): end, start or delete one` (the delete) and `feat(announcements): extend after a
  closure` (the extension). The opened delete and extension dialogs are **held by the list** (`AnnouncementsList`, as it
  holds the sheet: `CardDialog` = `{ kind, … }` with the card's key and the opener), the openers (`AnnouncementMenu`'s
  «حذف…», `ExtensionAction`) only open them; closed, the focus goes back to the opener while it is there, else to the
  card's first action, else the next card's or the tab (`useCardFocus.settle`, beside `leave`). Tests in
  `AnnouncementsList.component.test.tsx`: the extension answered `409 CLOSURE_ALREADY_EXTENDED`, the list read again with
  the closure extended → the dialog and its line stay until «Back», then the focus on a card's action or the tab; the
  delete answered `CLOSURE_EXTENDED` likewise. **Red** (the six files as at HEAD, `CardDialog.ts` removed): both "Unable
  to find an accessible element with the role "alertdialog"" — "Tests 2 failed | 6 passed (8)". **Green:** 8/8; the
  feature's 12 files / 63 tests. **Break:** the focus not placed once the opener is gone → both red ("expected <body …>
  not to be <body …>"). Split over its two homes (the delete-only state built from saved copies, checked — typecheck 0,
  63 tests — and folded first, then the extension); the tree after the fold identical to the pre-fold backup.
- **R1-F3** → `feat(announcements): post and edit an announcement`. Finding 169's resolution: "…which only the ledger's
  filters, the announcement sheet's period and the showcase import"; finding 180 already named the sheet's date fields.
- **R1-F4** → the same commit. `PeriodFields` passes `today={dayOf(gazaClockOf(new Date()).date)}`. Test in
  `AnnouncementSheet.component.test.tsx` at 22:30 UTC on 21 October (Gaza's 22nd): the calendar's `aria-current="date"`
  day is `2026-10-22`. **Red under `TZ=UTC`** (CI's zone): "× marks Gaza’s today in its calendar, not the browser’s" —
  "Tests 1 failed | 2 passed (3)". **Green** under UTC, New York and Gaza's zone. On this machine (Gaza's zone) the
  test cannot fail without the fix — its red was seen under `TZ=UTC`, which CI runs (F2's lesson, recorded).
- **R1's outside line** → `feat(announcements): show a space's announcements`: its *Web history* line starts "#129 —".
- **R2-F1** → `feat(data-reports): list every space's reports`: *Open findings* lists 167 (the reviewer's line) — by
  the document pass, below.
- **R2-F2** → `feat(data-reports): decide a space's reports` (the owner's, the sheet) and `…list every space's reports`
  (the admin's). While the opened report is gone from the page shown (decided elsewhere, under «جديدة»), the list's hook
  reads page 1 of the same scope's «الكل» (the chip's own query, key and cache; the admin's with its space and field)
  and the sheet takes the report from it — its status and its decision; and once `REPORT_ALREADY_DECIDED` says it is
  decided, the sheet never draws a stale «جديد»: «تمت المراجعة» (`dataReports.chips.decided`) until it is read. Tests in
  `SpaceReportsList.component.test.tsx` under `?status=open` (409, then the page without the row: with «الكل» holding it
  → «Not accepted» and its reply, no «New»; with «الكل» not holding it → «Reviewed», no «New») and
  `AdminReportsList.component.test.tsx` (the admin's). **Red:** "Unable to find an element with the text: Not accepted"
  / "…: Reviewed" — "Tests 2 failed | 4 passed (6)"; the admin's "…: Corrected" — "Tests 1 failed | 3 passed (4)".
  **Green:** the feature's 11 files / 54 tests. **Breaks:** the «الكل» read disabled → the first red; the stale guard
  dropped → the second red; the admin's read disabled → its red.
- **R2-F3** → `…list every space's reports`. `FilterTags` keeps the focus: a tag removed hands it to the button now at
  its place (the next tag's, else «مسح الفلاتر»), «مسح الفلاتر» or the last tag gone to the count (`onEmptied`). Tests:
  remove the first of two tags → the second's button; remove the second → «Clear filters», then «Clear filters» → the
  count. **Red:** both `toHaveFocus` — "Tests 2 failed | 4 passed (6)". **Green** twice. **Break:** the keeper never
  acting → both red.
- **R2-F4** → `…list every space's reports`: **finding 184** recorded ("A report's «تعديل الحقل» may not scroll to its
  section"; Plausible — not run in a browser), linked from `data-reports.md`'s *Open findings* and the index.
- **R3-F1** → `feat(favorites): list a user's favourite spaces`. «إزالة» of a space that left says «أُزيلت {name} من
  المفضّلة. لا يمكن حفظها من جديد ما دامت خارج الدليل.» / "{name} removed from favourites. It can’t be saved again
  while it’s out of the directory." (`favorites.removedLeft`, both catalogues), with **no «تراجع»** (`writeFavorite`'s
  `say: 'left'`, `useFavoriteToggle`'s `say`). Test 81's undo case is now "no «Undo»" (one `DELETE`, no button in the
  toast). **Red:** the toast's line not found — "Tests 1 failed (1)". **Green:** 5 files / 17 tests. **Break:** the
  undo restored (`say: 'undoable'`) → red. `favorites.md` and `directory.md` corrected; **finding 187** recorded ("A
  favourite just removed cannot be saved again for an undo"), linked from `favorites.md` and the index.
- **R3-F2** → `feat(data-reports): report wrong information` (the report, the shared signal, the shell) and
  `feat(favorites): save a space from its card` (the favourite). Each held intent lets itself go after 15 minutes
  (`HOLD_MS`, a timer), and when a guest lands on another page of the site: the site's shell reports each page it shows
  (`useGuestIntents` → `@shared/routing`'s `noteSitePage`), and each intent registers to let go (`onGuestLeaving`). The
  sign-in and register pages are outside the site's shell, so the round trip through them keeps the intent. S14 kept:
  memory only. Tests: the intents' unit tests (held 15 minutes less a millisecond kept, 15 minutes let go); the space
  page's "a guest who leaves for another page" — the held favourite not saved by a later sign-in, the held report's
  dialog not opened on the return signed in. **Red:** unit "expected undefined to be 900000" (`HOLD_MS` absent); the
  page's "expected [ { …(19) } ] to have a length of +0 but got 1" and "Unable to find role="heading" and name "Noor
  Hub"" (the dialog opened over it) — "Tests 2 failed | 7 passed (9)". **Green:** 9/9 and 7/7. **Break:** the shell not
  reporting its pages → both page tests red.
- **R3-F3** → `feat(favorites): save a space from its card`. The heart keeps one name, «حفظ {name} في المفضّلة», with
  `aria-pressed` (the WAI-ARIA toggle). Tests 77 and the toggle's updated. **Red:** "× keeps its one name and is
  pressed…", the toggle's label — "Tests 2 failed | 6 passed (8)". **Green:** 12 files / 74 tests. **Break:** its red
  (the changing name). `favorites.md`'s heart paragraph says it, a departure from §9's two names.
- **R3-F4** → `feat(data-reports): report wrong information`: `overview.md` names the report from a space's page.

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
