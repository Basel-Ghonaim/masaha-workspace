# OWNER_SETUP — execute PR 2 (`feat/owner-packages`, Packages & prices)

You are the **executor**, in a fresh conversation. You did not plan this item and you will not review it.
**The plan is approved; do not re-decide anything in it.** You build **PR 2 only**.

## 1. Read, then begin

1. **Precondition:** PR 1 (#96, `feat/owner-space-profile`) is merged — `gh pr view 96 --json state` →
   `MERGED` (at `c91f5b42`, 2026-10-20); if not, stop.
2. Work in `C:\dev\masaha\app` only — never in `C:\dev\masaha\app-b` (worker B) or
   `C:\dev\masaha\app-design`. Read `CLAUDE.md` at the repository's root.
3. Read the plan **whole**: `C:\dev\masaha\workspace\WORKER_A\OWNER_SETUP\2_PLAN.md` — **the owner's
   approval note at its top binds and wins where the plan differs**: three PRs; **this PR is the plan's
   commits 6–7** (the prices on Packages & prices; the private packages), ≈ 40 files, titled with commit 7's
   subject; tests 13, 15–20 and test 14's Packages case; the Packages page's real-run cases. The refusal
   lines as the note corrects them (a package's 404 names both causes; a 403 names none). Nothing of PR 3
   (staff, settings, the handover).
4. **Carried from #96 — this PR's first commit(s), before the plan's commit 6:** read
   `C:\dev\masaha\workspace\WORKER_A\OWNER_SETUP\0_CARRIED_FROM_96.md` whole and the review it cites
   (`6_REVIEW_PR1_CLAUDE_CODE.md`), and build it as it says — each code fix red first, then green, with its
   break. The PR's description says "Carried from #96".
5. **Read #96's report** (`4_REPORT_PR1.md`) for what PR 1 actually built and its departures (the shapes of
   `meanwhileLines`, `listLink`, `SPACE_PAGES`, `spacePagePath`, `usePricesLink`); build on them as merged.
6. Follow the plan's §13 for PR 2 (its "PR 1" checks read for this PR): the first checks against the merged
   `origin/main` (`git diff --name-status 9fae4e00 origin/main`: worker B's DESK may have merged API and
   docs changes — a code file this PR names changed in a way not covered → stop and ask; check 5's
   `toFieldErrors` point for the empty limit; check 6's `Sheet` — if it is not full width below 768 px,
   build with it as it is and record the next free finding); the branch `feat/owner-packages` from the latest
   `origin/main` (`--no-track`); per commit `lint` and `typecheck`; on the head each lane once; the real run;
   `#PRNUM`; push; the PR; CI green and `CLEAN`; the conflict check against any open PR (worker B's DESK PR 3
   may be open: shared documents only). Stop at §13's *Stop and ask*.
7. **Finding numbers start at 101** (98 and 100 are worker B's, 99 is #96's): the first free number from
   101 on the latest index.
8. `docker start masaha-postgres-1` (never `db:up`; never `npm ci`); API on 3320, web on 5320, worker A's
   `masaha_dev` (migrated to `main`). The real run with a browser tool that takes **real screenshots** — the
   `playwright` MCP tools if present, otherwise local headless Chrome over CDP; say which. Arabic light and
   English dark, at 390, 768 and 1440: §13's Packages & prices cases (the profile's prices row now leading to
   the built page; «الأسعار المعلنة» as a table at 1440 and cards at 768/390, saved and confirmed, its leave
   guard; a package added with two limits, per day, students and a shift, edited, a repeated name refused,
   paused by its switch; «صباحي» paused → its held-shift line → «إزالة الوردية»; the network log with no
   `/admin/` request). Screenshots to `C:\dev\masaha\workspace\WORKER_A\OWNER_SETUP\shots\pr2\`.
9. **The demo accounts (the supervisor's note after #96):** if a demo account refuses `SEED_DEMO_PASSWORD`,
   **stop and report** — do not reset passwords or change data through the app to get past it; the owner
   restores the demo data. Undo what your real run changes where the app allows it (a package you add may
   stay; say what remains).
10. If you are Claude Code, the project's skills may help (the plan's appendix is only a map). Write nothing
    outside the repository except this folder's `4_REPORT_PR2.md` and `shots\`.

## 2. A test you cannot run stops the work

A test **failing** because its code is not written yet is the plan's red step — normal. A test, lane or
command you **cannot run** is not: it errors before any test runs (the database unreachable, Docker down, a
port taken, a module or `dist` missing, a migration pending, `No test files found`, a Vitest or TypeScript
startup error, the whole run timing out, a crash with no result); a break you could not make or run; a
real-run case you could not perform (other than those the plan names). **Then stop at once** — never skip,
`.skip` or delete a test, never change a config, a timeout, `.env`, a script or a lane, never mock what the
plan does not, never run a narrower command and call it the lane, never call it "flaky" and move on. Write
the command, its exact error and where you were into the report, and reply with §5's shape,
`Status: STOPPED`.

**One known exception (the owner's decision on #96):** `routes.component.test.tsx` › "lists the owner's
eleven pages" (finding 87) may miss its 3 s locally when the machine is loaded. If **only that test** fails
in the full component lane and it passes when its file runs alone, record both runs (times, free memory) in
the report and the PR's Evidence and go on; **CI's `test:component` is the judge** — if it fails there,
stop. Any other failure follows the rule above.

**A plan that proves false against the code:** stop too, say exactly what and why, and offer the fix — do
not choose it yourself. **A break that stays green:** stop — unless it is plainly your own test's defect, or
the plan's break cannot change the outcome (as a bound already excluded by another); then make the break
that can, see it red, and state it as a departure.

**Never claim a result you did not see:** a command passed only if you saw its own output say so; copy that
line (read it by its exit code). A break counts only when you saw it red.

## 3. Limits, memory, and not losing work

- Write `4_REPORT_PR2.md` **as you go**: after the first checks, after each commit (sha, subject with its
  length, the red line before the code, the green line after), after each break, after the real run, after
  the push. If you stop for any reason, the report already says where the work stands.
- **Memory:** the machine is shared and has run low. Before each full lane: no `vitest`, `tsc` or dev server
  of `C:\dev\masaha\app-b\` runs (worker B's — never stop its processes; wait), and the free memory written
  into the report. One full lane at a time. A lane killed for memory: stop at once, no retry.
- Each full lane **once, on the head**; re-run only if a file it covers changed after it passed.
- Keep the scripts you write for the real run in this task folder's `scripts\`, never committed.

## 4. Discipline

Stage by path (never `-A` or `.`); each commit message written to a UTF-8 file **without a BOM, LF line
endings**, with a body saying why, and `git commit -F <file>`; subjects counted ≤ 50; **no tool
attribution**; a fix before the push folds into its commit (`--fixup` + `GIT_SEQUENCE_EDITOR=:`
autosquash); never print a secret or a password; never merge, create an Issue, or comment on another PR.
`git status --short` clean at the end; stop both servers by process id; ports 3320 and 5320 free.

## 5. Your final reply — this shape, finished or stopped

```
Status: DONE | STOPPED
PR: #<n> <url> · head <sha> · CI <green/red/pending> · <CLEAN/not CLEAN>   (or "no PR")
Commits: <sha> <subject> (<chars>) — one line each, the carried one(s) first
Carried from #96: <each item 1–9: done, its test and break red seen / not done (why)>
Ran and passed: <each command, with the result line you saw>
Ran and failed: <each, what failed, what you did>   (or "none")
COULD NOT RUN: <each test, lane, break or real-run case not run, the exact command, the exact error,
               why>   (or "none" — only if every planned run happened)
Breaks: <each: red seen / NOT red (why)>
Real run: <each case and its screenshot, or NOT RUN (why)>
Data left in masaha_dev: <what the run changed and did not undo>
Departures from the plan: <each, with its reason>   (or "none")
Stopped at (if STOPPED): <the step, and what the owner must decide or fix>
Report: C:\dev\masaha\workspace\WORKER_A\OWNER_SETUP\4_REPORT_PR2.md
```
