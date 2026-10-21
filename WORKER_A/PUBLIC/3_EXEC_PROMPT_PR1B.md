# PUBLIC — execute PR 1b only (`feat/directory-filters`, the Directory's filters and near me)

You are the **executor**, in a fresh conversation. You did not plan this item and you will not review it.
**The plan is approved; do not re-decide anything in it.** You build **PR 1b only**, the second of five.

## 1. Read, then begin

1. **Precondition:** PR 1a (#101, `feat/directory-list`) is merged — `gh pr view 101 --json state` → `MERGED`
   (at `befd96f9`, 2026-10-21); if not, stop.
2. Work in `C:\dev\masaha\app` only — never in `C:\dev\masaha\app-b` (worker B) or `C:\dev\masaha\app-design`
   (reviews and planners read there). Read `CLAUDE.md` at the repository's root.
3. Read the plan **whole**: `C:\dev\masaha\workspace\WORKER_A\PUBLIC\2_PLAN.md` — **the owner's approval note at
   its top binds and wins where the plan differs**: **this PR is the plan's PR 1 commits 6–7** (filter by place,
   price and state; sort the spaces nearest first), ≈ 34 files, titled with commit 6's subject. Read PR 1a's
   report `4_REPORT_PR1A.md` whole: **its split of commit 5 moved here** what only near me or the filters reach
   — the `Masaha-Near` argument and header, `hasNear`, `distanceText` and the card's distance, the distance
   word, the `placeFilter` slot — with tests 17, 31–43 and the privacy half of test 14; and **S6's
   `useMediaQuery` export** (plan §7/§9: commit 6). PR 1's acceptance criteria and real-run cases that 1a did
   not cover are this PR's.
4. **Carried items — this PR's first commit(s):** `C:\dev\masaha\workspace\WORKER_A\PUBLIC\0_CARRIED_FROM_101.md`
   (items 1–11, the owner's decisions of 2026-10-21) with #101's review `6_REVIEW_PR1A_CLAUDE_CODE.md`. Each
   code fix with its own test seen red before the fix and green after; item 4 is a check, not a change; item 9
   is a finding only. The PR's description names them under "Carried from #101".
5. Follow the plan's §13 for this PR, with three changes the owner made (§3 below): the first checks against
   the merged `origin/main` (`git diff --name-status e50d9222 origin/main` — PR 1a's reported head; a code file
   this PR names changed in a way the plan does not cover → stop and ask); the checks a–f that concern commits
   6–7, each with its fallback; the branch `feat/directory-filters` from the latest `origin/main`
   (`--no-track`); per commit `lint` and `typecheck`; the head's checks; the real run; `#PRNUM`; push; the PR
   (`--label feat --label area:web --label area:docs --label area:design-system`, the layer's barrel gains
   `useMediaQuery`); CI green and `CLEAN`; the conflict check against any open PR (worker B's SUBSCRIPTIONS PR 1
   may be open: shared documents only). Stop at the plan's *Stop and ask*.
6. **Finding numbers:** this item's are 130 and on; 130 is on `main`, 131 is reserved by the plan (the
   closure's notice); a new one takes the next free number (132 and on), said in the report.
7. `docker start masaha-postgres-1` (never `db:up`; never `npm ci`; if Docker Desktop is not running, stop and
   ask the owner to start it); in `apps/api` `npx prisma migrate status` — pending → `npx prisma migrate
   deploy`, then `npx prisma generate`; API on 3320, web on 5320, worker A's `masaha_dev`.
8. **The demo data (the approval note's (3)):** this PR's real run needs worker B's DEMO_SEED (≈ 24 directory
   spaces) merged and seeded into `masaha_dev` **by the supervisor** — not by you. Build everything first
   (carried commits, commits 6–7, the head's checks); **then** run §13's data inventory (read-only `GET`s, a
   script in `scripts\`). If DEMO_SEED is not merged, or the inventory lacks a case this PR's real run needs
   (two areas with spaces, prices in a day budget of 10–30 ₪, a verified and an unverified space, an available
   space, student prices, a Friday opening, coordinates for near me), **stop before the push** — commits kept
   local, the report saying where the work stands — and reply `Status: STOPPED` naming what is missing. **Never
   add or change data through the app, the API, the database or the seed.**
9. **The real run** with real screenshots (the `playwright` MCP tools if present, else local headless Chrome
   over CDP; say which): plan §13's PR 1 cases that 1a did not perform — the place filter (two areas, the
   summary), the budget (day, 10–30 ₪; an inverted range's line), each switch, «أخرى», the filters' sheet at
   390 and 768 (its count, its button) and the sidebar at 1440, near me granted, denied, imprecise and out of
   the Strip, and **the privacy proof in the network log** (no coordinate in any URL; the header only on
   `sort=distance` requests, three decimals at most; none after «مسح موقعي»); plus the carried items 1, 2 and 5
   where a browser shows them (typing a search on page 2 keeps the focus; after sign-in the focus is on
   `main`). Widths as §3.4 below. Screenshots to `C:\dev\masaha\workspace\WORKER_A\PUBLIC\shots\pr1b\`.
10. If you are Claude Code, the project's skills may help (the plan's appendix is only a map). Write nothing
    outside the repository except this folder's `4_REPORT_PR1B.md`, `shots\` and `scripts\`.

## 2. A test you cannot run stops the work

A test **failing** because its code is not written yet is the plan's red step — normal. A test, lane or
command you **cannot run** is not: it errors before any test runs (the database unreachable, Docker down, a
port taken, a module or `dist` missing, a migration pending, `No test files found`, a Vitest or TypeScript
startup error, the whole run timing out, a crash with no result); a break you could not make or run; a
real-run case you could not perform (other than those §1.8 and the plan's *Not performed, by design* allow).
**Then stop at once** — never skip, `.skip` or delete a test, never change a config, a timeout, `.env`, a
script or a lane, never mock what the plan does not, never run a narrower command and call it the lane, never
call it "flaky" and move on. Write the command, its exact error and where you were into the report, and reply
with §6's shape, `Status: STOPPED`.

**The owner's standing exceptions:**
- `routes.component.test.tsx` › "lists the owner's eleven pages" (finding 87) may miss its 3 s locally when the
  machine is loaded. If **only that test** fails and it passes alone, record both runs (times, free memory) and
  go on; **CI's `test:component` is the judge** — if it fails there, stop.
- A run **killed for low memory** is re-run **once** when the machine is quieter (no `vitest` of
  `C:\dev\masaha\app-b\` running, the free memory recorded); killed again → record it, carry on, and CI's run
  of that lane on the pushed head is the judge — red there → stop.

**A plan that proves false against the code:** stop too, say exactly what and why, and offer the fix — do
not choose it yourself. **A break that stays green:** stop — unless it is plainly your own test's defect, or
the plan's break cannot change the outcome (as a bound already excluded by another); then make the break
that can, see it red, and state it as a departure. **A design issue or a review point you would leave
undone: stop and ask** — never silently.

**Never claim a result you did not see:** a command passed only if you saw its own output say so; copy that
line (read it by its exit code). A break counts only when you saw it red.

## 3. What runs where (the owner's rule, 2026-10-21: no run that only repeats another)

1. **A test seen red before its code is its own break.** Record that red line once. Make a **separate** break
   only where the plan's break targets a guard the red step did not prove — a privacy rule (the header, the
   rounding, no coordinate in a URL), a bound, a fallback to a default, a width — and record its red output.
2. **Locally, on the head:** `npm run test:unit -w @masaha/web` (worker A changes the web only; CI runs every
   workspace) · `npm run test:component -w @masaha/web -- src/features/directory src/features/lookups
   src/features/space-links src/pages/site src/shared/lists src/shared/design-system` (the folders this PR
   touches; add any other folder whose files it changes, and say so) · `$env:NODE_ENV='production'; npm run build; Remove-Item
   Env:NODE_ENV` · `npm run check:build` (and the first download's record from the manifest, as §13 says) ·
   `npm run check:classes` · `npm run format:check` · `npm run check:links`. Before each test run: no `vitest`
   of `C:\dev\masaha\app-b\` running, the free memory recorded.
3. **Not run locally, by the owner's rule — CI's run on the pushed head is the judge:** the full
   `test:component` lane, `test:unit` of `apps/api` and `packages/shared`, and `test:api` (no API change).
   Report them under "Not run locally (CI judges)", not under COULD NOT RUN. A red CI lane → fix it, fold the
   fix, push again; red on finding 87's test alone → the exception above.
4. **The real run's widths:** the layouts that change with width — the filters' sheet (390, 768) against the
   sidebar (1440), and the results' grid — in Arabic light and English dark at 390, 768 and 1440; every other
   case once in Arabic light at 390 and once in English dark at 1440.

## 4. Limits and not losing work

- Write `4_REPORT_PR1B.md` **as you go**: after the first checks, after each commit (sha, subject with its
  length, the red line before the code, the green line after), after each break, after the real run, after
  the push. If you stop for any reason, the report already says where the work stands.
- Each run **once, on the head**; re-run only if a file it covers changed after it passed.
- Keep the scripts you write for the real run in this folder's `scripts\`, never committed.

## 5. Discipline

Stage by path (never `-A` or `.`); each commit message written to a UTF-8 file **without a BOM, LF line
endings**, with a body saying why, and `git commit -F <file>`; subjects counted ≤ 50; **no tool
attribution**; a fix before the push folds into its commit (`--fixup` + `GIT_SEQUENCE_EDITOR=:`
autosquash); never print a secret or a password; never merge, create an Issue, or comment on another PR.
`git status --short` clean at the end; stop both servers by process id; ports 3320 and 5320 free.

## 6. Your final reply — this shape, finished or stopped

```
Status: DONE | STOPPED
PR: #<n> <url> · head <sha> · CI <green/red/pending> · <CLEAN/not CLEAN>   (or "no PR")
Commits: <sha> <subject> (<chars>) — one line each
Carried from #101: <each item 1–11: done in <sha> / checked (item 4) / recorded as finding <n> (item 9)>
Ran and passed: <each command, with the result line you saw>
Ran and failed: <each, what failed, what you did>   (or "none")
Not run locally (CI judges): <each lane, and CI's result on the head once seen>
COULD NOT RUN: <each test, lane, break or real-run case not run, the exact command, the exact error,
               why>   (or "none" — only if every planned run happened)
Breaks: <each: red seen (in the red step or as its own break) / NOT red (why)>
Real run: <each case and its screenshot, or NOT PERFORMED (by design) with the test that proves it>
Data left in masaha_dev: <what the run changed>   (expected: nothing)
Departures from the plan: <each, with its reason>   (or "none")
Stopped at (if STOPPED): <the step, and what the owner must decide or fix>
Report: C:\dev\masaha\workspace\WORKER_A\PUBLIC\4_REPORT_PR1B.md
```
