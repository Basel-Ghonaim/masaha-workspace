# FINAL — the lead's run (every screen of v1, every open finding — one PR) — the report

Written as the run goes. Times are local (Gaza) unless marked UTC (the grant log's).

## Status — READY FOR REVIEW

PR **#132** (https://github.com/Basel-Ghonaim/masaha/pull/132) · head **`a12c0790`** · CI green on that head (every
check) · **CLEAN** · 124 commits · 1001 files (+30,656 / −4,328; ≈ 40 % of the lines are lane A1's re-indented race
tests and the lanes' new tests).

## Start (2026-10-29, ≈ 16:27)

- The waiting script printed `READY 16:27`; `3_EXEC_PROMPT_LEAD.md`, `AUTONOMY_2026-10-25.md`, `2_PLAN.md` (2,929
  lines, whole), `SUPERVISOR_DECISIONS.md`, the two earlier lead reports' named sections and `heavy.mjs` read.
- `C:\dev\masaha\app`: `git status --short` empty; `main` = `origin/main` = `ce671b37`.
- `npm ci` 0; `npm run build -w @masaha/shared` 0; `npx prisma migrate status` on `masaha_dev` and `masaha_test`:
  "29 migrations found … Database schema is up to date!". Container `masaha-postgres-1` up (healthy). Docker Compose
  v5.5.1 (EC6: ≥ 2.23.1).
- Branch `feat/final` cut from `origin/main` (`ce671b37`).
- Machine: 16 GB, 12 cores; **5.8 GB free** at the start (the owner's "about 10 GB" not free yet).
- Grant script `scripts\heavy.mjs` (copied from PAYMENTS_STEP10's, adapted: 60 tries; never two `test:api` started
  within 60 s of each other), log `scripts\heavy-grants.log` (UTC).

## The foundation (U0)

- **C0.1** `75c6bc04 feat(shared): carry a refusal's details` (39) — D0.1. T1 (`errorHandler.api.test.ts` › "carries
  the details of a refusal that names a record") and T2 (`toAppError.unit.test.ts` › "keeps the record a refusal
  names, in the contract’s shape only") green (22/22, 17/17). B1 (the handler drops `details`) → "Tests 1 failed | 21
  passed (22)"; B2 (`toAppError` ignores `details`) → "Tests 1 failed | 16 passed (17)" (`scripts\lead\break-B1.txt`,
  `break-B2.txt`; each restored by copy). Typecheck 0, lint 0, prettier clean. (The code was written before its tests:
  the breaks are its red, as LANE_COMMON allows.)
- **C0.2** `37a84e65 feat(shared): refuse a published price changed` (46) — D0.2 by the `add-error-code` skill's
  steps (code, both catalogues, contract §6; the provoking test is lane A2's T64). T3: the catalogues' parity test
  green 6/6; B3 (the Arabic line removed) → "× ar has exactly the lines English has … Tests 1 failed | 5 passed (6)".
  Typecheck 0.
- **C0.3** `f70ee787 feat(web): group the dashboard's navigation` (43) — D0.3 (165, 14's place, GSH.1/5/6, G23.2,
  G28.3). EC1: the layer's `SidebarGroupLabel` was already `sr-only` on the rail; the rail's divider between groups
  added in the layer's `SidebarGroup` (`first:` resets). Count hooks in `data-reports` (`useOpenReportsCount`,
  `useAdminReportsCount`; keys under the existing `dataReports` prefix — the plan wrote `data-reports`, the code's
  prefix is `dataReports`). T4–T8 in `routes.component.test.tsx` (13 navigation tests green). Breaks: B4 (one flat
  group) 3 red · B5 (`grouped` always) × reception has no group names ("expected [ 'Today', 'The space' ] to deeply
  equal []") · B6 (no rail rule) × "Expected the element to have class" · B7 (audit `BOTH`) × reception's four pages
  · B8 (badge at 0) × "shows no count…". Typecheck first red (SpaceLayout's `spaceId` may be `undefined`: the hook
  takes `number | undefined`), then 0; lint 0.
- **C0.4** `0379d85e feat(web): skip to the content in every shell` (45) — D0.4 (130, G5.6, carried 1). `SkipLink`
  moved by `git mv`; `useMainFocus` rewritten in `shared/routing/focus/` with `firstPage.ts`. **LEAD-D5:** the "first
  page" is told apart per router history (the router's navigator, `UNSAFE_NavigationContext`) and a guard's replace
  by "no press or key since the history began", instead of one module-level flag — a module flag would make every
  later test file's first render (and the existing "not on the first load" test) wrong, and resetting it for tests
  would be test-only production code. T9–T12 (`useMainFocus.component.test.tsx`, 5 tests), T13 (skip link first in
  the dashboard and the focus shell, the site's existing). Breaks: B9 × 4 · B10 × "moves the focus to main…" · **B11
  first stayed green** — the test's two shells were one component type, so React reused the focused `main`; the test
  now uses two component types, and B11 is red ("× focuses the site’s main on Back from the focus shell") · B12 × hash
  · B13 × skip link first. Typecheck 0, lint 0.
- **C0.5** `d05903c3 feat(web): give the account its place on a phone` (47) — D0.5. `ACCOUNT_SETTINGS_PATH = '/me'`
  in `shared/routing` (the dashboard's menu links it; pages groups cannot import each other); `DrawerAccountMenu`
  (users) + `DrawerAccount` (shell); `AccountMenuContent` takes `place` (`site` | `dashboard`); «الموقع العام» uses
  `StoreIcon` (the layer has no globe icon). T14/T15 (routes, phone), T16/T17 (CompactAccountMenu), T18 (SiteLayout,
  SiteAccount). Breaks: B14 × "Expected the element to have class" · B15 × "Dark theme" not in the drawer · B16 ×
  the dashboard's items · B17 × "names the role" · B18 × `hidden md:inline-flex`. Typecheck 0, lint 0.
- **C0.6** `f1bf19d9 feat(web): route the screens still to come` (42) — D0.6. Six stub pages, `/me` with its stub,
  the three copy sections empty. T19 (`pageTitles.unit.test.ts` › "cover the screens still to come…"); B19 (the
  `/me` route without its handle) × both languages' title tests. Typecheck 0, lint 0, `test:unit -w @masaha/web` 157
  files / 1077 tests green.
- **Finding 87's family while building U0:** the first test of `SiteLayout`, `SiteAccount` and the dashboard routes
  file missed its 3 s wait under the lanes' load (body empty); the probe gave "renders the header" a 20 s wait and it
  passed — a cold lazy import, not U0's. Lane T's C4.3 warms these files.
  - **New code for the PR description:** `PUBLISHED_PRICE_CHANGED` — en "This price changed since the sheet opened.
    Check the new amount, then confirm." · ar «تغيّر هذا السعر منذ فتحت النافذة. راجع المبلغ الجديد، ثم أكّد.» (the
    Arabic needs the owner's approval).

## The lanes

- **LEAD-D1 — eight lanes, as §9.4 proposes** (A1 U1, A2 U2, L U3, T U4, W1 U5, W2 U6, W3 U7+U8, W4 U9), at most six
  running at once, by the memory (5.8 GB free at the start). W3 holds U7 and U8 in one lane (both in `features/desk`,
  §9.2 item 6 orders U7 first through C7.1). *Undo:* none needed.
- **LEAD-D2 — lane L starts with the API lanes, after C0.2, not after U0 whole.** Its files (the layer, `shared/lists`,
  `shared/lib`, the forms copy, `reminderTemplate.ts`) are none of U0's; W1, W3 and W4 build on it, so it starting
  early shortens their wait. Rebased onto `feat/final` at the join like the others. *Undo:* start it after U0.
- Lane prompts: `scripts\lanes\LANE_COMMON.md` and `LANE_<x>.md`; setup script `scripts\mklane.sh`; break helper
  `scripts\brk.py`. Finding ranges: A1 200–201, A2 202–203, L 204–205, T 206–207, W1 208–209, W2 210–211, W3 212–213,
  W4 214–215, the lead 216–219.
- **A1, A2, L set up** (16:5x): worktrees `C:\dev\masaha\app-lane-{a1,a2,l}` on `lane/{a1,a2,l}` at `37a84e65`;
  `.env` copied (A1's `TEST_DATABASE_URL` → `masaha_a_lane_a1_test`; A2's → `masaha_a_lane_a2_test` and its
  `DATABASE_URL` → `masaha_a_lane_a2_dev`); `npm ci` one at a time (0 ×3); shared build 0 ×3. Databases made in the
  shared container (`CREATE DATABASE` ×3, user `masaha`) and `npx prisma migrate deploy` on each ("All migrations have
  been successfully applied" ×3). Launched in the background.

- **Lane L DONE** (≈ 17:45): 10 commits + `docs: record finding 204`; report `scripts\lane-l\REPORT.md` (every
  red, every break red, lint/typecheck 0, unit web 162/1089, shared 27/273, component whole 7 failed — 2 its own,
  folded; 5 finding 87's family, green on re-run/alone). Decisions LL-D1–LL-D10, none SERIOUS. New finding **204**
  (a CSV value that reads as a formula, left for the owner).
- **T set up and launched** at `f1bf19d9` (U0 whole), told to hand over after C4.1.
- **W1 and W3 set up and launched** at `56e639c6` (U0 + lane L), each told to build the commits whose needs are in
  their base first and hand over for the rest.

- **The session ended** (2026-10-29, ≈ 18:10, after T's C4.1 join and W2's worktree; W2 not yet launched) and was
  resumed 2026-10-30 14:54 by the owner's "continue work now". Every lane agent had stopped mid-work. State found: A1
  17/17 commits (its final lint was running — slot left behind); A2 12/15 commits; T at `4550b5b2`, nothing begun on
  C4.2; W1 and W3 with uncommitted work (W1 the overview feature, W3 C7.1's test and the log's merge); W2 worktree
  ready, never launched; W4 not made. No lane process left running; the stale `heavy-slot-1` removed; the container
  up (healthy, restarted with the machine), the three lane databases there. 7.4 GB free. Each lane resumed by
  message, told to re-check its tree and re-run whatever was interrupted.

- **W2 launched** (2026-10-30 ≈ 15:00) at `4550b5b2`; **W4's worktree** made at `4550b5b2` and W4 launched once A1
  reported (six lanes at once kept).
- **Lane A1 DONE** (≈ 16:20): 17 commits, every red and break recorded (B20–B49); lint 0, typecheck 0, unit shared
  28/272, api 76/908, web 157/1076, **test:api whole on its database 117 files / 1347 tests, exit 0**; component
  whole 5 failed (timeouts and "Unable to find role=main" in files it did not touch; alone green but site routes'
  "shows the Directory under its title", finding 87). Findings closed 17, 21, 69, 77, 78, 79, 91, 92, 93; LA1-D1–D10,
  none SERIOUS. Report `scripts\lane-a1\REPORT.md`.

- **Stopped by the owner** (2026-10-30, "stop now"; resume from the same point). Every lane agent stopped; the
  leftover processes (W3's vitest, W1's grant wait) killed; slots cleared. At the stop: A2 15/15 commits (heavy checks
  next); T C4.2–C4.5 + finding 206 made; W1 9 commits (C5.6, C5.10 waiting for A1, now joined); W2 6 commits + work
  on C6.11; W3 5 commits + work on C7.11; W4 work on C9.4's tests, no commit yet. Resume steps in `scripts\RESUME.md`.

- **Resumed by the owner's "continue the work"** (2026-10-31). Found as left: every lane's commits and uncommitted
  files intact, no lane process, no slot; Docker Desktop was down — started it and `masaha-postgres-1` (healthy).
  7.1 GB free. All six lanes resumed by message from their own last steps; W1 told to rebase onto `0a1979e1` (A1)
  now (clean tree), W2 and W4 once their uncommitted work is committed.

- **Lane W2 HAND-OVER** (2026-10-31): 14/17 commits on `0a1979e1`; findings 14, 73, 74, 83, 89, 94, 95, 158 closed;
  report `scripts\lane-w2\REPORT.md`. Its context ran out before C6.14 (buildable). **LEAD-D8:** a fresh W2 agent
  takes the lane over from its report and notes (C6.14 now; C6.10, C6.15 after A2; then the lane-wide runs) — the
  first agent's decisions kept. *Undo:* none needed.

## The joins

- **Lane L** → `backup/final-lane-l-pre-join` at `19785eb8`; `git rebase f1bf19d9` in its worktree: no conflict
  (11 commits, `bf140be4` … `56e639c6`). On it: typecheck 0, lint 0 (`scripts\lead\join-l-*.txt`);
  `test:component` over `src/pages`, `features/users`, `shared/routing`, `shared/lists`, `shared/design-system`: 4
  failed | 575 passed | 12 skipped — each the first test of its file at 3.0–3.1 s (finding 87's family); alone:
  `authPages` 14/14, site `routes` 13/13; `SiteLayout` alone still missed its first test at 3,059 ms, and with the
  wait raised it passed at **3,814 ms** (a cold import just past 3 s; C4.3 warms that file). `backup/final-pre-join-l`
  at `f1bf19d9`; `git merge --ff-only lane/l` → `feat/final` at `56e639c6`; worktree `app-lane-l` removed.

- **Lane T's C4.1** → rebased onto `56e639c6` (no conflict) → `4550b5b2`; typecheck 0, lint 0; `scripts` unit 159/159;
  component (space page, account, data-reports, announcements, platform-settings) 26 files / 134; ff-only.
- **Lane A1** → `backup/final-lane-a1-pre-join` at `b328768f`; `git rebase 4550b5b2`: no conflict (17 commits).
  On it: typecheck 0, lint 0, `test:unit -w @masaha/web` 163 files / 1098 tests, component (staff, space-links, users,
  StaffPage, admin pages) 47 files / 271 tests (`scripts/lead/join-a1-*.txt`); the API is unchanged by the rebase (U0's
  envelope was already in A1's base), so its whole `test:api` stands. `backup/final-pre-join-a1` at `4550b5b2`;
  ff-only → `feat/final` at `0a1979e1`; worktree `app-lane-a1` removed.

- **Lane W1** (DONE, 11 commits, rebased by itself onto `0a1979e1`, no conflict) → typecheck 0, lint 0 on its head
  (its own lint/typecheck had not been re-run after a fixture fold); its component lane's 4 finding-87 misses (App ×2,
  router, routes' reception 403) are left to T's warm-up and the final run. `backup/final-pre-join-w1` at `0a1979e1`;
  ff-only → `feat/final` at `a52fc3e2`; worktree removed. **LEAD-D6:** W1's two decisions it marked SERIOUS (LW1-D1 a
  new key `staff.reissue.refusedAdmin` so the re-activation's line stays true; LW1-D2 `?page=` / `?credit=` for the
  debts tab's two lists) accepted — neither touches money, a role, private data, a key or a lock; both keep the plan's
  intent. Recorded under *Decisions taken without the owner*.

- **Lane T DONE** (2026-10-31): C4.2–C4.5 + finding 206; findings 27, 48, 55, 87, 98, 180 closed; the warm-up took
  SiteLayout's first test from 3,814 ms to 369 ms. Report `scripts\lane-t\REPORT-DONE.md`. Rebased onto `a52fc3e2`
  (`backup/final-lane-t-pre-join2` at `5957dd65`): no conflict.
- **LEAD-D7 — finding 206 fixed in this PR, not left open.** A production build of the joined branch failed
  `check:build`'s showcase-strings rule: lane L's chart fixtures held the bare month ticks يوليو, أغسطس, سبتمبر, Jul,
  Aug, Oct and the unit ILS, which date-fns and `priceText` also write. The lead reworded them («يوليو 26», "Jul 26", …;
  the unit "shekel amounts") as a `--fixup` of `a5747df7 feat(design-system): draw bar charts and a heatmap`, folded at
  the final autosquash; the build then passes every rule ("No showcase code in 72 build files (1070 strings checked)",
  `scripts\lead\fix206-*.txt`); registry 9/9, BarChart/Heatmap 7/7. Since the defect never reaches `main`, the commit
  `docs: record finding 206` is **dropped** at that same fold (a finding opened and fixed within one PR is no record).
  *Undo:* keep the commit and mark 206 Resolved.
- **Lane T** joined: on `cf333c5b` typecheck 0, lint 0; the six warmed route files + App + router 8 files / 117 tests
  green (the first-test misses of W1 and A1 gone). `backup/final-pre-join-t` at `a52fc3e2`; ff-only → `feat/final` at
  `cf333c5b`; worktree removed.
- **Lane A2** (DONE; report `scripts\lane-a2\REPORT.md`; M1 `20261029144213_subscription_usage_bigint`, M2
  `20261029154841_subscription_published_period`) → `backup/final-lane-a2-pre-join` at `c17e1b18`; `git rebase
  cf333c5b`, two conflict rounds, each resolved keeping both sides (`scripts\lead\join_a2_contract1.py`,
  `join_a2_reclaim.py`): **a9cdfcd7** (the stall) — `shared/jobs/index.ts` (`SWEEP_BATCH` and `JobDone` both
  exported), `jobs.ts` (both declarations), the contract's `POST /internal/jobs/run` (A1's sweeps and A2's stall merged
  into each bullet); **5519f558** (the reclaim) — `app.ts`'s jobs list (the two sweeps, then `photos.reclaimOrphans`),
  `jobs.api.test.ts` (both sides' lines; the stalled test's list five entries), the contract (the reclaim bullet after
  the merged ones). The other 13 commits applied cleanly. On it: typecheck 0, lint 0, unit shared 28/277, api 76/912,
  web 172/1126; **test:api whole on `masaha_a_lane_a2_test`: 2 failed | 1372 passed (1374)** — `auth/password.api` ›
  "leaves a recovery bound to no link reading sent…" (green on re-run: timing) and `jobs.api` › "a run whose failures
  fill the batch answers 500…" — **a semantic join conflict**: its expected "job ran" list lacked A1's two sweep jobs.
  Fixed inside the stall commit itself (`git rebase -i` with an `edit` stop at it, the two lines added, amended; the
  reclaim commit's line then met them and both kept; `backup/final-a2-pre-stallfix`); jobs + password 55/55.
  `backup/final-pre-join-a2` at `cf333c5b`; ff-only → `feat/final` at `a417ed04`; worktree removed.
- **W2's second agent** (HAND-OVER, 15/17: C6.14 made) resumed after A2's join for C6.10, C6.15 and the lane runs.
  **W3's first agent** (HAND-OVER, 9 commits: C7.1, C7.2, C7.6, C7.9–C7.14; context spent) → **LEAD-D9:** a fresh W3
  agent takes the lane from its report and notes (rebase onto `a417ed04`, the 12 commits left, the lane runs).
- **Lane W4 DONE** (16 commits; C9.4's WhatsApp line and T264 wait for W2's C6.4) → `backup/final-lane-w4-pre-join` at
  `1ac69a7b`; `git rebase a417ed04`: one conflict, `authPages.component.test.tsx` (lane T's `beforeAll` warm-up and
  W4's `renderSite(path, client)` both kept). On it: lint 0; unit web 174/1137; component (site pages, users, auth,
  directory, favorites, lookups, shared/routing, shared/map, app) 119 files / 680 tests, all green — lane T's warm-up
  removed W4's finding-87 misses; typecheck first 2 (the worktree's Prisma client predated M2 — `prisma generate`),
  then 0. `backup/final-pre-join-w4` at `a417ed04`; ff-only → `feat/final` at `63e8a9f9`; worktree removed. **Left
  for a fold into C9.4 after W2's join:** the WhatsApp line of «لا يمكنك الوصول إلى بريدك؟» and T264.
- **Lane W2 DONE** (17 commits + finding 210; second agent; report `scripts\lane-w2\REPORT.md`) →
  `backup/final-lane-w2-pre-join` at `bb05d6aa`; `git rebase 63e8a9f9`: four doc conflicts (data-reports.md ×2,
  lookups.md ×2, all History / behaviour lines of two lanes), each kept both (`scripts\lead\keep_both.py`), lookups.md
  read after. On it: typecheck 0, lint 0, unit web 181/1164, **component whole 330 files / 1952 tests, exit 0**.
  `backup/final-pre-join-w2` at `63e8a9f9`; ff-only → `99b99a25`; worktree removed.
- **LEAD-D10 — finding 210 fixed in U0's code, not left open.** W2 found that `useMainFocus` focused a hash-named card
  (a `div` that takes no focus), so the editor's later hash changes moved no focus. Fix: the hook focuses the named
  element when it takes focus, else its first focusable heading; a new test "focuses the heading of a card the hash
  names when the card takes no focus itself" (B210f, the old behaviour → ×); architecture §2's line says it.
  Committed `2c7e33ba fixup! feat(web): skip to the content in every shell`; `docs: record finding 210` dropped at the
  final fold, as 206's. Focus + editor tests 42/42 (then 43).
- **C9.4's WhatsApp line folded** (`4895884a fixup! fix(auth): keep next and the way back`): `platform-settings/public`
  exports `usePlatformContact`; the forgot page's «تواصل معنا» opens the platform's WhatsApp (`wa.me`, new tab) when set,
  else `/about#contact`; T264 "opens the platform’s WhatsApp for someone who cannot reach their email, when it is set"
  green, B264 ×; the forgot page 6/6; eslint 0, web tsc 0.

- **Lane W3 DONE** (third agent; 22 commits: U7's 14, U8's 7, finding 212; findings 160, 162, 163, 164, 166, 171, 172
  closed; report `scripts\lane-w3\REPORT.md`) → `backup/final-lane-w3-pre-join` at `3b333337`; `git rebase 4895884a`:
  one History conflict (spaces.md, both kept). On it: typecheck 0, lint 0, unit web 184/1172; component whole 338/339
  files, 2004/2006 tests — `AccountLayout` "sends a guest to sign-in…" and "opens «Favourites» signed in…" missed 3 s
  under load; alone, twice on `feat/final` without W3 and twice with it: 3/3 (finding 87's family, not a regression).
  `backup/final-pre-join-w3` at `4895884a`; ff-only → `6e96e0dd`; worktree removed.
- **U10** (sub-agent; report `scripts\lane-u10\REPORT.md`): `docs: record every screen of v1 as built`, `docs: close
  the findings v1 accepts` (22, 84, 112, 115, 187, 193 Accepted; F1's six marked "To the deployment item"),
  `refactor(web): remove the placeholder page` (`screenOf()` throws for a nav item with no screen; break red). Written
  ahead of W3 for U7/U8's lines; after W3 joined, each feature it names checked present in the code; rebased onto W3
  (no conflict); check:links 3196, typecheck 0, routes 69/69; ff-only → `acacec3f`.
- **The fold** (`backup/final-pre-fold`, `-pre-drop`, `-pre-fold2`): `git rebase -i --autosquash origin/main` folded
  the three fixups (206's fixtures into the chart commit, 210's focus rule into C0.4, C9.4's WhatsApp line) — tree
  identical; a second pass dropped `docs: record finding 206` and `… 210` (only their two files left the tree); a third
  folded **findings 130 and 165's own files** (Resolved + *Resolution*), which the lead had missed writing in C0.4 and
  C0.3 — found when the rebuilt index still listed them Open. No `fixup!` left.
- **C10.1** `docs: close the findings v1 resolves` — the index rebuilt from every finding file's status line
  (`scripts\lead\index_findings.py`): Open 8 (23, 33, 46, 64, 65, 152 + 204, 212), Accepted 10, Resolved 121; all 55 built
  findings checked Resolved; check:links 3198. **LEAD-D11:** the index commit is U10's last, not its first (it must
  follow every finding file). **Slip recorded:** while redoing the index the lead ran `git checkout --
  docs/architecture/findings/README.md` on its own uncommitted, regenerated copy — the rules forbid that command;
  nothing was lost (the file was regenerated from the findings), noted here as a breach of the rule.
- **The branch:** 124 commits on `origin/main`; every subject ≤ 50 characters; no attribution in any message.

- **The first complete verification** (`scripts\lead\final_verify.sh` on `d3fe4f91`; `scripts\lead\final\summary.txt`):
  npm ci 0 · shared build 0 · `migrate deploy` on `masaha_test` ("All migrations have been successfully applied") ·
  lint 0 · typecheck 0 · check:classes 0 (1915 files) · check:links 0 (3198) · check:conflicts 0 · unit shared 28/280,
  api 76/912, web 184/1172 · **component whole 339 files / 2006 tests, exit 0** · production build 0 · check:build 0 ·
  design check-parse 0, check-classes 0 · `#PRNUM` in 94 files, none outside documents. **Red:** `format:check` 1 —
  `apps/api/src/shared/jobs/index.ts`, the lead's merged export line of the A2 join, too long → `prettier --write`,
  folded into `fix(jobs): answer 500 when failures fill a batch` (`backup/final-pre-fold3`; head `f4dcc6dd`, 124
  commits, no `fixup!`); **`test:api` 1** — none of its 118 workers started ("Worker exited unexpectedly with exit code
  3221225794", 0xC0000142: the machine out of process resources), so no API test ran: **not a test result; to re-run.**
  First download of the head's build: **1,158,388 bytes, 7 chunks**, no leaflet / data-table / dashboard chunk
  (`scripts\firstDownload-head.txt`).
- **Stopped by the owner (2026-10-31) and handed to another agent** because of the session's limits: the remaining
  steps — `format:check` and `test:api` again, the base's first download, the real run (M1/M2 on `masaha_dev`, the
  servers, `scripts\tour.mjs`), the PR number (`scripts\prnum.sh`), the push, the PR (`scripts\pr-body.md`, drafted), CI,
  the end of this report — are written step by step in **`FINAL\HANDOFF.md`**. Leftover processes checked: none of the
  run's (a broad kill was refused by the permission classifier — the narrower listing showed nothing left); slots
  cleared.

## Memory and the grants

- **LEAD-D4 — the lead's requests go first** (17:0x): with three lanes running, free memory swung between 2.1 and
  5.5 GB and the lanes' 2-minute polls kept taking the slots while the lead's typecheck of C0.3 — the foundation, on
  the critical path of five lanes — waited 8 tries (≈ 16 minutes). `heavy.mjs` now: while the lead waits it writes
  `heavy-lead-waiting.txt` (stale after 5 minutes), the lanes take no slot while it is fresh, and the lead re-tries
  every 30 s. The memory rule (≥ 4 GB) is unchanged. *Undo:* drop the file check.

## The final verification (2026-10-31)

- `npm ci` 0 · `npm run build -w @masaha/shared` 0 · `format:check` exit=0: `All matched files use Prettier code style!`
- `lint` 0 · `typecheck` 0 · `check:classes` 0 · `check:links` 0 (3198 links) · `check:conflicts` 0
- `test:unit` shared 28 / 280 · api 76 / 912 · web 184 / 1172 — all green
- `test:component` (whole) 339 files / 2006 tests — green
- `test:api` (whole, `masaha_test`) **Test Files 120 passed (120), Tests 1374 passed (1374)** — green (ran via grant script, `scripts\lead\final\api2.txt`)
- `NODE_ENV=production npm run build` 0 · `check:build` 0 · design `check-parse` 0, `check-classes` 0
- First download of head (already measured): **1,158,388 bytes, 7 chunks**, no leaflet / data-table / dashboard chunk (`scripts\firstDownload-head.txt`)
- Step 3c (first download of `main` for comparison): **skipped** — memory short on this machine, per the handoff's option.

## The first download

Head: 1,158,388 bytes, 7 chunks (`scripts\firstDownload-head.txt`). Base not measured (step 3c skipped).

## The real run

- **M1 and M2 applied to `masaha_dev`** (2026-10-31, by the other agent: "All migrations have been successfully
  applied."); `prisma generate`. The servers (API 3320 on `masaha_dev`, web 5320) run by the lead on 2026-11-01, after
  LEAD-D12's container fix.
- **The tour** (`scripts\tour.mjs`, read-only; English in dark at 1440 and 390 — and 768 where a layout changes — Arabic
  in light at 1440; log `scripts\tour-log.txt` and `tour-log-run2.txt`; shots `FINAL\shots\tour\`, 120+ files):
  - **guest 8/8 · reception 6/6 · owner 15/15 · admin 9/10** — the one admin miss is the check's, not the page's:
    «ملخص المنصة» / "Platform summary" is the tiles section's accessible name (D5.2's `section` named so; proven by
    `AdminOverview.component.test.tsx`'s region), not visible text. The owner's sidebar groups «اليوم», «المال»,
    «المساحة», «الفريق والإعدادات» and the admin's «المساحات», «المنصة» checked; the owner's overview holds no ₪ and
    no "ILS" (D5.1's rule); reception refused finance and the audit log with the 403 inside the shell.
  - **Two tour defects found and fixed in the script, none in the app:** signing in applies the account's saved
    language (the demo accounts' is Arabic) — the tour now switches with the header toggle, as a person does; and the
    tour's full reload of every page refreshed the session each time, until the refresh's rate limit answered **429**
    (the API's log) and the session guard showed the general error («حدث خطأ غير متوقع» / "Something went wrong") —
    what the other agent's Arabic shots and the lead's first owner run (audit, settings) showed. The tour now moves
    between pages inside the app (no reload); the owner's audit and settings then rendered. The 429 on a burst of
    reloads is the limit's intended behaviour.
  - **The network:** no 5xx in any role; **no write** (GETs, the sign-ins and refreshes only).
  - **Seen by the lead** (economy agreed with the owner: the rest of the shots are for the owner): the owner's overview
    at 390 in dark English (attention rows «2 visits not collected» and «3 customers owe money», present now 0 / 40 with
    its meter, active announcements, ending this week), finance at 1440 in light Arabic (the tabs, the month select,
    the three tiles, «الدخل حسب الشهر» stacked bars reading right to left, the grouped sidebar), the admin's audit log at
    768 in dark English (the intro line, search, three filters, «Events: 256», the table with targets as links and
    «at {space}» under them).
- **Not performed** (named by the plan's §11): the write cases R1, R11, R12, R19–R24, R26, R30, R32–R35, R38 (the
  registration, the held favourite, the account edits, the desk's check-ins, write-off and undo, a subscription and a
  published-price change, payments, corrections, a report resolved, a photo, a closure, hide and show, links, lookups,
  the platform settings) — to stay within the session's limits after the handover; each behaviour is proven by its
  component and API tests (desk, finance, audit, platform-settings, space-links, lookups, users, auth). Also not seen:
  R39's build output (the verification's `check:build` stands for it), R40 (`docker compose config` — lane T's C4.4
  report), 134's measured typing with CPU throttling.
- **Data left:** none written by the run; `masaha_dev` carries M1 and M2. The servers stopped by process id (the two
  `tsx watch`, the API server, two `pino-pretty`, Vite); ports 3320 and 5320 free; `git status --short` empty.

### The lead resumes (2026-11-01), the other agent having stopped at its limit after ≈ 30 minutes

- **Found:** the other agent ran steps 3a–3b (format 0; `test:api` 120 files / 1374 tests green) and the tour, wrote the
  sections above, pushed nothing, opened no PR; the tree clean on `f4dcc6dd`; M1/M2 applied to `masaha_dev` by it.
- **Its tour results were not valid**, for two reasons the lead found: (1) signing in applies the account's saved
  language (Arabic for every demo account), so every English check of a signed-in role could only fail — the tour now
  switches language with the header's toggle after signing in, as a person would (`useLanguage`); (2) its Arabic
  dashboard shots were the root error page («حدث خطأ غير متوقع»); the lead's probe (`scripts\probe.mjs`, the owner's
  overview in Arabic) renders correctly today — attention rows, present now, ending this week — so the tour was re-run
  in full and its results replace the agent's (old log `tour-log-agent2.txt`, shots `shots\tour-agent2\`).
- **LEAD-D12 — the container's one-time recreation (EC7) not done; the old init file restored untracked for the run.**
  `masaha-postgres-1` would not start: created from `main`'s compose, it bind-mounts
  `docker/postgres/create-test-database.sql`, which C4.4 (finding 48) deletes on `feat/final`; Docker had made an empty
  directory in its place. Options: recreate the container from `feat/final`'s compose (the volume kept; the owner's
  one-time step in setup.md › *Running a second folder*), or put `main`'s file back, untracked, for the run. Chose the
  second: the container also holds worker B's databases, and recreating it is the owner's step; the empty directory
  removed, `git show origin/main:docker/postgres/create-test-database.sql` written there (untracked), the container
  started (healthy). The file is removed after the run. **For the owner, after the merge:** the next `npm run db:up`
  recreates the container once (its volume and every database kept) — until then, a container made from the old
  compose needs that file; the PR description says so. *Undo:* recreate now.

## Push, the PR, CI

- **The PR number:** the last issue/PR was #131 → **#132**. `scripts\prnum.sh 132` (adapted from PAYMENTS_STEP10's
  `prnum1.sh`; its `reset --hard` on failure removed — a failure now stops and names the backup): "PRNUM OK #132
  a12c0790 (was f4dcc6dd)"; `git grep '#PRNUM'` empty; 124 commits; tree clean; check:links 3198; the description's
  `#PRNUM` replaced too. Backup `backup/final-pre-prnum` at `f4dcc6dd`.
- `git push -u origin feat/final` (new branch); `gh pr create` → **https://github.com/Basel-Ghonaim/masaha/pull/132**
  (labels feat, area:web, area:api, area:docs; assignee the owner; title "feat: complete every screen and close the
  findings", 50 characters). The number matches the documents'.
- **Clean-up after the PR opened:** databases `masaha_a_lane_a1_test`, `masaha_a_lane_a2_test`, `masaha_a_lane_a2_dev`
  dropped (`DROP DATABASE` ×3); local branches `lane/a1`, `lane/a2`, `lane/l`, `lane/t`, `lane/w1`, `lane/w2`,
  `lane/w3`, `lane/w4`, `lane/u10` deleted; every lane worktree already removed at its join.

- **CI on `a12c0790`** (run 41288412120, the branch's head): build pass 1m20s · check:classes pass · check:conflicts
  pass · check:links pass · format:check pass · lint pass 2m11s · **test:api pass 7m18s** · **test:component pass
  8m43s** · test:unit pass · typecheck pass · CodeRabbit skipping. `mergeStateStatus` **CLEAN**. Finding 55's
  measurement (the CI run's slowest route file): the whole component lane took 8m43s with no miss; the per-file timing
  is in the run's log (not extracted here).
- **The early conflict check:** `gh pr list --state open` lists only #132 — no other open pull request to compare.

## The commits (124, oldest first)

- `fed3b46d` feat(shared): carry a refusal's details
- `9c53b8dc` feat(shared): refuse a published price changed
- `3c58a9a1` feat(web): group the dashboard's navigation
- `a55da7bb` feat(web): skip to the content in every shell
- `44df247c` feat(web): give the account its place on a phone
- `40df132f` feat(web): route the screens still to come
- `9755efe6` feat(design-system): add a meter
- `06f3c154` feat(design-system): draw bar charts and a heatmap
- `cee9736d` feat(design-system): reach a held menu item
- `c0b8e36b` feat(design-system): size a large input
- `3348faf3` feat(lists): show a list's range and its steps
- `67747ed9` feat(lists): mark the page asked while it loads
- `5d2797d5` fix(lists): keep the scroll on a page change
- `098bc4e9` refactor(lib): read Arabic-Indic digits once
- `6f5b51b7` refactor(lists): share the row menus' triggers
- `43aad599` feat(lib): build a CSV and a WhatsApp link
- `9a7dff2c` docs: record finding 204
- `5d4178a3` build(web): serve the site's parts by their entry
- `9284b98d` feat(sessions): give a replay its successor
- `b046ce99` feat(jobs): sweep expired counters and tokens
- `79aaed8d` feat(auth): say a Google sign-in made the account
- `748ce34f` feat(auth): free an expired account's address
- `14bdecc4` feat(auth): print the reset link in the email
- `958782bb` feat(users): say how an account signs in
- `6626ad4f` feat(space-links): name the owner in ALREADY_OWNER
- `a31cb3d0` feat(space-links): find an account by exact email
- `c7fe46c4` feat(space-links): one schema of space statuses
- `e620ba83` fix(staff): keep sessions held by another link
- `2fad3c23` fix(staff): refuse an admin's account by its code
- `1cf7cd7c` feat(staff): date each reception link
- `d3afe676` test(staff): pin three refusals and the expiry
- `ae1e86a8` docs(api): name the owners' type-check code
- `efb0d0d8` test(api): aim the race helper at its own wait
- `4908f217` test(spaces): find the names' own query
- `b8fceb03` refactor(users): require the names' transaction
- `7edd61a4` feat(overview): show the owner's work queue
- `0d5eb142` feat(overview): show the platform at a glance
- `b8029521` feat(finance): show a month's income
- `c4c431c9` feat(finance): show who owes and who paid
- `947629fd` feat(finance): show the space's occupancy
- `9491efeb` feat(space-settings): link the personal settings
- `8720f77c` fix(packages): say the desk sells these prices
- `f8eeac35` fix(packages): announce the terms, not the name
- `fd266d46` fix(staff): reach the held item by the keyboard
- `c56dca3c` feat(staff): show each person's month and start
- `32178078` fix(staff): word both cases and name the tokens
- `67b980a5` build(web): keep dashboard-only code acyclic
- `3d5798b4` test(web): load the lazy shells before waiting
- `bd7e9d0f` build(db): hold the test database's script inline
- `d9e81909` docs: settle the capability documents' size
- `06753d3c` feat(db): compute a subscription's due in bigint
- `0fce0315` test(db): pin Gaza's transitions in PostgreSQL
- `dab7973e` perf(subscriptions): bound check-ins by midnights
- `f0240b98` fix(jobs): answer 500 when failures fill a batch
- `3fa5ab42` feat(jobs): reclaim the files no photo holds
- `37caa0a4` fix(customers): match a phone under either code
- `347e32de` feat(visits): check a visit in for its customer
- `47ccd91d` feat(subscriptions): refuse a changed price
- `c675195f` feat(subscriptions): name who recorded and voided
- `1879e0b1` feat(visits): list a space's written-off visits
- `7e3244f0` feat(db): keep a subscription's published period
- `627eeaa6` feat(customers): carry the reminder in the file
- `9f801981` feat(desk): say more of who is there and of plans
- `1716f006` feat(data-reports): read one report by its id
- `57851f54` feat(spaces): name the retired amenities held
- `108dbff8` refactor(users): one folder per operation
- `79d8bdcd` fix(auth): keep next and the way back
- `20869f1b` feat(forms): say when a password is too long
- `7e2d442a` fix(site): announce a second retry while offline
- `95ea07af` fix(site): finish Home and About
- `1f1ce675` fix(directory): finish the map and the results
- `2048fdc4` fix(directory): draw the marks as on light tiles
- `43e69574` fix(directory): wait for near me once permitted
- `36c88ec3` fix(directory): hide area counts past the pins
- `c611a7ad` fix(directory): finish the space page
- `b8eb7ff5` fix(site): retry the route and give the 403 a way
- `167dcd70` fix(favorites): show the list's line once ready
- `974ab466` test(site): pin the footer, the areas and the pick
- `8f804bad` feat(auth): welcome a first Google sign-in
- `00017140` feat(users): edit one's own account
- `f91b34cf` feat(auth): keep a guest's action through a reset
- `06425a84` feat(audit): show a space's audit log
- `3cfaac2f` feat(audit): show the platform's audit log
- `7454f2f1` feat(platform-settings): edit the settings
- `6412e22b` feat(platform-settings): read the public contact
- `ca41fdeb` fix(space-links): name a person's front desks
- `4e010aa8` fix(space-links): word a link from a fresh read
- `cfac6125` feat(data-reports): filter by who handles them
- `9309a221` feat(space-links): land the spaces the admin keeps
- `34520e2f` fix(space-links): read the email's account exactly
- `0e83d63d` feat(space-links): link the owner a refusal names
- `fb5adcd9` fix(space-links): finish the owners and users
- `0913363b` fix(admin): reach a held user action by keyboard
- `21bfe2a5` feat(spaces): show a photo's upload as a bar
- `3f61eb7c` fix(spaces): finish the spaces list and editor
- `de0a9eb9` fix(lookups): keep switches in rows, add positions
- `e145a9e4` feat(lookups): name the retired amenities kept
- `e3b8a3ab` feat(data-reports): open a report beside its field
- `f78c1f46` fix(desk): focus the write-off's reason first
- `62b90d57` feat(desk): show a day's log beside who is here
- `2daa4143` fix(desk): order the phone's desk and its states
- `15feecfd` fix(desk): count a full space and show the rates
- `ca8bce43` feat(desk): name the file a phone adds to
- `2e572b17` fix(desk): say a refused payment recorded nothing
- `5ed2e8b2` feat(desk): say a usage subscriber's due at out
- `4a591222` fix(desk): finish the subscription sheet
- `e7d0cd63` docs(visits): name the desk's screen
- `001c2501` feat(desk): list and undo the written-off visits
- `902dd226` feat(desk): check a customer in as their visit
- `f9be0553` feat(desk): send the price the sheet showed
- `eaf2f978` feat(desk): link names and word who is here
- `3827ee48` feat(desk): renew or subscribe from the desk
- `84375a56` feat(desk): offer a customer's actions by state
- `f631ea57` feat(desk): remind a customer on WhatsApp
- `71bcb39f` feat(desk): name who recorded and voided
- `5d082659` feat(desk): correct a subscription from its card
- `c0e37ea3` feat(desk): filter customers by week and month
- `c60865c0` fix(desk): finish the customers list and file
- `5c1dabd8` docs: record finding 212
- `d41b079f` feat(payments): name the space's other owners
- `9bf66b52` docs: record every screen of v1 as built
- `0676d604` docs: close the findings v1 accepts
- `10a72981` refactor(web): remove the placeholder page
- `a12c0790` docs: close the findings v1 resolves

## Decisions taken without the owner

**None SERIOUS** in the prompt's sense (no money shown wrong, no role offered what it must not, no private data, no
key or lock rule broken, no migration beyond M1 and M2, no approved decision changed). Lane W1 marked two of its own
SERIOUS; the lead's reading (LEAD-D6) is that neither is.

- **LEAD-D1** eight lanes as §9.4, at most six at once (memory). *Undo:* none needed.
- **LEAD-D2** lane L started after C0.2, not after U0 whole (no file of U0's). *Undo:* start it after U0.
- **LEAD-D3** C4.4's container never recreated by a lane (shared with worker B); `docker compose config` only.
- **LEAD-D4** the grant script lets the lead's request go first (critical path). *Undo:* drop the file check.
- **LEAD-D5** the "first page" of the focus rule told apart per router history and a replace before any press or key,
  not a module flag (test isolation; no test-only code). *Undo:* a module flag.
- **LEAD-D6** W1's LW1-D1 (a new key so the re-activation's refusal stays true) and LW1-D2 (`?page=`, `?credit=` for
  the debts tab) accepted. *Undo:* overwrite the key; component state.
- **LEAD-D7** finding 206 (the showcase's chart fixtures matching library text) fixed in this PR, its record dropped.
- **LEAD-D8 / LEAD-D9** fresh agents took W2 and W3 over from their reports when the first agents' context ran out;
  their decisions kept.
- **LEAD-D10** finding 210 (a later hash focusing a card that takes no focus) fixed in U0's focus rule, its record
  dropped.
- **LEAD-D11** the findings index commit last in U10 (it must follow every finding file).
- **LEAD-D12** the container's one-time recreation (EC7) left to the owner; `main`'s init file kept untracked in the
  lead's folder (excluded locally in `.git/info/exclude`) so the shared container starts. *Undo:* `npm run db:up`.
- **The handover** (the owner's word, 2026-10-31): the end of the run written as `HANDOFF.md` for another agent; that
  agent ran the format and API checks and an invalid tour, then hit its limit; the lead finished (2026-11-01).
- Every lane's own decisions: `scripts\lane-<x>\REPORT.md` (LL-D1–D10, LA1-D1–D10, LA2-D1–D11, LT-D1–D11,
  LW1-D1–D9, L-W2-D1–D17, LW3-D1–D18, LW4-D1–D11, LU10-D1–D6).

## Anything that behaved unexpectedly

- Free memory swung between 1 and 7 GB; grants waited up to ≈ 30 minutes; one full `test:api` run's 118 workers could
  not start at all (0xC0000142) — re-run green.
- Finding 87's family (a cold lazy import missing a 3 s wait) kept appearing under load in files no lane touched
  (`AccountLayout`, the routes files, `App`, `router`); each green alone; lane T's warm-up cleared most; none in CI.
- The session ended twice (2026-10-29 night, 2026-10-30) and was stopped once by the owner; each time every lane was
  resumed from its own transcript, nothing lost.
- Docker Desktop was down at each resume; once, the container could not start because of this PR's own C4.4 (LEAD-D12).
- The tour: the account's saved language overrides the device's on sign-in; the refresh's rate limit (429) answers a
  burst of full reloads with the general error — both the limit's and the session's intended behaviour, not defects.
- Git Bash rewrites an argument starting with `/` into a Windows path (MSYS) — `MSYS_NO_PATHCONV=1` for the probe.
- Python heredocs turned backslashes in Windows paths into control characters in this report three times (fixed).

## Departures from the prompt

- The order of a few commits differs from §9.1 (the lanes' waiting commits came after their joins; C10.1 last).
- The real run toured every screen read-only; the plan's write cases were not performed (the handover's limits), named
  with the tests that prove them; the base's first download not rebuilt (memory).
- The lead ran `git checkout --` once on its own regenerated, uncommitted index file (a forbidden command; nothing lost).
- Two lanes and the lead ran a workspace's `tsc` directly a few times outside the grant (short, recorded in their
  reports).


## Leftovers

- **Branches:** `feat/final` (the PR). Backups, for the owner to delete after the merge: `backup/final-pre-join-l` `backup/final-pre-join-t1` `backup/final-pre-join-a1` `backup/final-pre-join-w1` `backup/final-pre-join-t` `backup/final-pre-join-a2` `backup/final-pre-join-w4` `backup/final-pre-join-w2` `backup/final-pre-join-w3` `backup/final-pre-join-u10` `backup/final-lane-*-pre-join(2)` `backup/final-a2-pre-stallfix` `backup/final-pre-fold` `backup/final-pre-drop` `backup/final-pre-fold2` `backup/final-pre-fold3` `backup/final-pre-prnum` (25 in all).
- **Worktrees:** none of the run's (every lane worktree removed at its join).
- **Databases:** the three lane databases dropped; `masaha_dev` carries M1 and M2; `masaha_test` migrated.
- **The lead's folder:** `docker/postgres/create-test-database.sql` (`main`'s copy, untracked, excluded locally) until
  the owner's `npm run db:up` after the merge (LEAD-D12).
- **Findings open:** 23, 33, 46, 64, 65, 152 (the deployment's) and 204, 212 (recorded by this run).
- **Outside the repository:** `FINAL\scripts\` (lane reports, scripts, outputs), `FINAL\shots\tour\` (the tour's
  shots for the owner), `FINAL\HANDOFF.md`.


## The reviews' fix round (2026-11-01)

Executed by worker A's fix-round executor from `7_FIX_ROUND.md` (24 items), in one conversation, no sub-agent, no
worktree. **Base:** `feat/final` clean at `origin/feat/final` `a12c0790`, `CLEAN`; `npm ci`, the shared build, the
container up; free memory 6.77 GB. **Rule kept:** every fix a new commit after `a12c0790` — no fixup, no autosquash, no
rebase of the 124, no force-push; one plain `git push` (`a12c0790..b2b0c503`).

### The fixes (25 commits; red before the fix, green after)

| # | Review | Commit | Red (before) → green |
|---|---|---|---|
| 1 | R2-F1 | `5e99323a` fix(jobs): stall only on a full batch of failures | `× one stay that always fails, alone in its batch, answers 200 … — expected 500 to be 200` → `jobs.api.test.ts` 8 passed |
| 2 | R2-F2 | `d49d30d0` fix(auth): replace only an account someone created | `× a self-registered account whose admin-issued temporary password expired is not replaced — expected 201 to be 409` → `replacement.api.test.ts` 10 passed |
| 3 | R2-F3 | `4f25d33c` test(auth): give the expiry race its race timeout | no red possible (a timeout shows only under load) → `sessionLock.api.test.ts` 9 passed |
| 4 | R2-F4 | `c15b7b78` fix(payments): sum subscription payments in bigint | `× … a subscription whose paid sum is past the integer's range — expected 500 to be 200` → customers API 12; payments/subscriptions/finance 81 |
| 5 | R3-F1 | `6e708e5a` fix(admin): hold, not disable, the owners link | `× reaches the held «Link to a space» by the keyboard — toHaveAttribute()` → space-links component 171 |
| 6 | R3-F2 | `716a953f` fix(finance): keep counted tiles in Arabic order | `× keeps the counted tiles in Arabic's own direction…`, `× keeps the stay …` → finance component 14 |
| 7 | R3-F3 | `d569bb3a` fix(desk): land the overview's #unpriced link; `7bb6d9cb` test(desk): answer the unpriced read as a page | `× lands the overview's «with no price» link … — toHaveFocus()` (still red with the id alone: the card draws after the shell's rule) → routes 70. `7bb6d9cb`: the same test's answer was typed for uncollected rows, found by the typecheck at item 12's commit; its own commit, not folded |
| 8 | R3-F4, R14-F7 | `be5c6db1` fix(web): write a formula-like CSV value as text | `× puts a quote mark before text that would open as a formula, numbers kept as numbers` → csv unit 3; finance unit 10 + component 14; finding 204 Resolved |
| 9 | R3-F5 | `95e3ddad` fix(web): land a report's field link on its notice | `× leads the owner …`/`× leads the admin …` (unit), `× lands on itself once it draws when the address's hash is #report …` → unit 2; data-reports + editor component 104 |
| 10 | R5-F1 | `a559cfea` fix(desk): keep the written-off toggle on a phone | `× keeps its header and «Written off» on a phone for the owner when empty … — not.toHaveClass("hidden")` → 13; finding 212 Resolved, out of the index's *Open* |
| 11 | R5-F2 | `fbe04292` fix(desk): hold a customer on their visit present | API `× a customer's visit names its customer, a visit by name none`; web, each half undone: `Unable to find role="link" and name "Sara Khalid"`, `Unable to find … 1 result` → occupancy API 33; desk/occupancy component 43, unit 12 |
| 12 | R5-F3 | `5a6c0d54` fix(desk): pick the oldest debt across both kinds | `× names the oldest owing item across both kinds … — expected 'Receive ₪20' to be 'Receive ₪200'` → desk component 191, openItems unit 5, desk API 159 (three exact-shape API tests take `createdAt`) |
| 13 | R5-F4 | `72e297a0` fix(desk): hold the list menu still while it reads | `× moves nothing under the pointer … — expected [ …(3) ] to deeply equal []` → desk component 192 |
| 14 | R5-F5 | `fd489782` fix(desk): name each write-off undo by its visit | four written-off tests (name not found) → 11 |
| 15 | R5-F6 | `3c3c0efd` fix(web): keep a reminder in one language | desk `× … the default text with no template`, finance `× names the space in English …`, settings `× previews the English default …` → 40 |
| 16 | R14-F1 | `b2b0c503` fix(web): dim every paged list while a page loads | `× dims the rows shown while the page asked loads …` (customers; red shown by restoring the list from HEAD: `expected null not to be null`), `× dims the cards shown …` (Directory) → seven features' component 658 |
| 17 | R14-F2 | `2409dfc5` fix(directory): bound near me's unanswered prompt | `× a prompt that never settles and no answer end as denied a minute from the press … — expected 'locating' to be 'denied'` → directory 123 |
| 18 | R14-F3, R4-F2, R4-F3 | `e870fef9` fix(web): run a held action only on its round trip | heldIntent unit `× is dropped, never run, by another tab's sign-in …`, `× is dropped on a later visit …`, `× runs once … after a password reset …`; reset page `× marks the recovery done …` (wiring removed) → unit 11; component 308 + reset page 9 |
| 19 | R14-F4 | `22baadc6` fix(directory): keep the map's filters on a phone | `× keeps «الفلاتر» on the row at 390 … — toHaveClass("min-w-0 flex-1")` → directory 122; the real run at 390 in both languages |
| 20 | R14-F5 | `34e442c6` fix(directory): focus the place filter, not main | `× «Choose your area» from the favourites focuses the place filter … — <div id=directory-filters-form> does not contain: <main id=main>` → 127 |
| 21 | R14-F6 | `11640fc7` fix(account): set a password by auth's link sent | page test `× sends the link, then draws the link sent …`, `× holds the button while a 429 runs …` → site account + users + auth 215 |
| 22 | R14-F8 | `bf316eea` docs: record finding 55's CI time; drop stale line | documents only; the figure from `gh run view 41288412120 --job 124794379554 --log`: dashboard routes 69 tests 15,009 ms, slowest 794 ms, first 512 ms; site routes slowest 407 ms; authPages slowest 342 ms |
| 23 | R14-F9 | `677fb1fd` fix(web): let a download's address go after a tick | `× … lets its address go after the click — expected "revokeObjectURL" to not be called at all` → csv/finance/payments component |
| 24 | R4-F1 | `427b6973` fix(auth): keep next through the password recovery | `× carries the return page to sign in, before and after the password is set`, `× carries the return page on to the new password`, `× drops a return page that leaves the site` → site auth 39 |

Nine subjects over 50 characters were reworded on this round's own unpushed commits (two message-only
`filter-branch` passes over `a12c0790..HEAD`, trees unchanged, the 124 untouched); the hashes above are the final ones.

### The runs on `b2b0c503` (memory free before each heavy run)

- `build -w @masaha/shared` 0 · `format:check` 0 · `lint` 0 · `typecheck` 0 · `check:classes` 0 (1917 files) ·
  `check:links` 0 (3203 links) · `check:conflicts` 0.
- `test:unit` — shared 28 / 280, api 76 / 912, web 184 / 1181: green.
- `test:component` (6.6 GB) — 340 files / 2034 tests, 455 s: green.
- `test:api` (6.91 GB) — 120 files / 1378 tests, 665 s: green.
- `NODE_ENV=production npm run build` (5.08 GB) 0 · `check:build` 0 (no showcase, no dashboard code or heavy library
  in the site's first download).
- No run killed for memory; finding 87's family missed nothing.

### The real run (`scripts\fixrun.mjs`, log `scripts\fixrun-log.txt`, shots `shots\fix\`)

Web 5320, API 3320 on `masaha_dev`, headless Chrome over CDP. **12 pass, 0 fail**; no page error.
- 19: the map at 390, Arabic and English — «الفلاتر» inside the screen, no sideways scroll.
- 24 (read-only, no reset sent): sign-in → forgot carries `?next=%2Fabout`; forgot → back to sign in carries it; an
  off-site `next` (`//evil.example`) dropped; the reset page's «Request a new link» and «Back to sign in» carry it.
- 6: finance in Arabic — the debts' amounts in `ltr`, «لا زبائن» and «زيارتان» not; the occupancy's stay not `ltr`.
- 10: the desk at 390 — «لن تُحصَّل» reachable (the demo has uncollected visits; the empty case, a write away, is the
  component test's).
- 13: the customers' «⋯» on a 2.5 s connection — one item alone, «جارٍ تحميل الإجراءات…», `aria-busy` and held; then
  «استلام ‏15 ₪», «ملف الزبون», «اشتراك جديد», «تعديل البيانات», «أرشفة…».
- 20: the favourites → `/spaces?filters=open` at 1440 — the place filter has the focus. The demo owner has no
  favourite, so near me (and its «اختر منطقتك») is not offered there; the same in-app navigation was made by the
  history (a POP, which the shell's rule takes as a link's), named in the log. The button's own path is the routes test's.
- The API's log: 36 GET, **one POST — the owner's sign-in**; no 5xx. No `/auth/` body kept. Servers stopped by
  process id (API 20424 and its `tsx watch` 6200, web 16212); ports 3320 and 5320 free.

### Push and CI

`git push origin feat/final` (plain, `a12c0790..b2b0c503`, 124 + 25 commits). CI run 41309866551 on `b2b0c503`:
build, check:classes, check:conflicts, check:links, format:check, lint, test:api, test:component, test:unit, typecheck —
all pass (CodeRabbit skipping); `mergeStateStatus` **CLEAN**. The PR description has a *Review fixes* section (each
item, its commit, the supervisor's decision) and its findings line corrected (204 and 212 resolved).

### Decisions taken on my own (met, options, chose, why, undo)

- **FR-D1 (R2-F2) the port renamed `hasActed` → `mustKeep`.** It now answers "no one else created it, or it acted";
  keeping the old name would lie. Undo: rename back, invert at the call.
- **FR-D2 (R3-F3) the card lands itself.** `id="unpriced"` alone stayed red: the card draws only once the terms
  answer, after the shell's focus rule looked. Options: a later shell retry, or the card landing on arrival (as the
  editor's `useHashLanding`). Chose the card's own landing, once per opening. Undo: drop the effect.
- **FR-D3 (R3-F5) every report link lands on `#report`.** A report decided meanwhile draws no notice, so its link then
  lands on `main`, the field's section no longer in the hash. Undo: keep `#{section}` beside a report-aware landing.
- **FR-D4 (R5-F3) `createdAt` on `SubscriptionWithMoney`** (the reviewer's option), read with the money from the same
  items row; a visit's making taken as its `checkedInAt`. An answer change, no migration. Undo: drop the field.
- **FR-D5 (R5-F4) the held item only, no prefetch on hover or focus** (the reviewer offered either): a prefetch reads a
  file for every row the pointer crosses.
- **FR-D6 (R5-F6) the second option: one language a message.** The first (always Arabic) would contradict the settings
  card's per-language default and its tests. Applied where the message is built: the desk's file, finance's debts list
  and the settings preview (the same cause). Undo: the space's Arabic catalogue instead.
- **FR-D7 (R14-F1) every paged list**, beyond the review's named ones (announcements, «غير محصّل», «لن تُحصَّل»,
  finance's who owes and who is in credit), so finding 132's "every list" holds.
- **FR-D8 (R14-F3) the reset's mark lives 10 minutes in `localStorage` (`masaha.recoveredAt`)**, removed by the next
  sign-in; the intent's own 15 minutes bound it too. Two existing tests that wrote the stored intent "as after a
  recovery" with no recovery now mark it first. Undo: a different length, or `sessionStorage` of the reset tab.
- **FR-D9 (R14-F6) composed by the page**, since a feature never imports another: `users`' card takes a slot,
  `auth` exports `SetPasswordByEmail`; `useSetPasswordLink` and `users`' `requestPasswordLink` removed (unused), the
  three words moved from `users` to `auth`. Undo: revert the commit.
- **FR-D10 (R4-F1) the reset card's «Request a new link» carries `next` too** (the same chain), and `nextSearch` carries
  only what `returnUrlOf` accepts.
- **FR-D11 the subjects reworded** on this round's own unpushed commits (message-only), not the 124.
- **FR-D12 (R14-F2) the existing prompt test reads the prompt 50 s, not 60**, to fit the 60 s bound; it still proves
  the 15 s replace it once granted.

**SERIOUS decisions:** none. **Refused commands:** none. **Left out:** nothing.

### State

`git status --short` clean on `feat/final` at `b2b0c503`. No branch or worktree made. Written outside the repository:
`FINAL\scripts\` (`fix_notes.md`, `fix_commits.txt`, `fixrun.mjs`, `fixrun-log.txt`, the run logs, the PR bodies) and
`FINAL\shots\fix\` (9 shots). **Findings open:** 23, 33, 46, 64, 65, 152 (the deployment's).
