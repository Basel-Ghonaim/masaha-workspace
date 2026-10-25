# OWNERS — execute PR 3 only (`feat/admin-owner-links`)

You are the **executor** of the last of three pull requests of one Work Item, in a fresh conversation. You
did not plan it and you will not review it. **The plan is approved; do not re-decide anything in it.**

## 1. Read, then begin

1. Work in `C:\dev\masaha\app` only — never in `C:\dev\masaha\app-b` or `C:\dev\masaha\app-design`. Read
   `CLAUDE.md` at the repository's root. (Masaha moved to `C:\dev\masaha\` on 2026-10-18; any older path you
   meet in a document is history.)
2. Read the plan **whole**: `C:\dev\masaha\workspace\WORKER_A\OWNERS\2_PLAN.md` — **the owner's approval at
   its top binds**, above all its last block, *Added 2026-10-18 (PR 2's review, deferred to PR 3)*. Then read
   PR 2's review `6_REVIEW_PR2_CLAUDE_CODE.md` (the findings that block names) and `4_REPORT_PR2.md` (*Fix
   round 1* and *Fix round 2*: what PR 2 became).
3. **Build PR 3 only, in three commits:**
   1. **#89's leftovers** — the approval note's (a)–(c), with a test and its break where behaviour changes:
      `fix(space-links): finish the add-owner sheet` (44). Its (d), the missing PR 2 screenshots, is taken
      in this PR's real run.
   2. §9 *PR 3 · commit 1* — linking and unlinking: `feat(space-links): link and unlink owners` (42), the
      PR's title.
   3. §9 *PR 3 · commit 2* — the editor names its owners (finding 59 resolved):
      `feat(spaces): name a verified space's owners` (44).
   Files: §7 *PR 3*; tests: §10 *PR 3*; §14's point 1 (`owners` leaves architecture §3 and
   `dashboardOnly.ts`) and point 2 (the unlink reads the space's owners on every opening).
   **Precondition:** PR #89 is merged — `gh pr view 89 --json state`; if not, stop.
4. **What changed on `main` since the plan (check, then build on it):** #89 (PR 2) at `60a78063`, then #90
   (worker B's STAFF) at `18ab1705`. #90 matters to you:
   - The admin's **link** now refuses an account whose temporary password is pending: `409
     ACCOUNT_PASSWORD_PENDING` (its lines are in both errors catalogues). The link dialog words it like the
     plan's other refusals, and §10's `it.each` of the link dialog's refusals includes it.
   - `AdminUserRow.receptionSpaces` is required: every `AdminUserRow` literal you add carries it.
   - Findings 88–93 are taken; **the next free number is 94**.
   Run the first checks of §13 with base `60a78063`: `git diff --name-status 60a78063 origin/main`. A §7
   code file changed in a way the plan does not cover → stop and ask. `packages/shared` changed → `npm run
   build -w @masaha/shared` before any web check.
5. Follow §13: the branch `feat/admin-owner-links` from the latest `origin/main` (`--no-track`); per commit
   `lint` and `typecheck`; on the head each lane once; the real run; the `#PRNUM` step; push, the PR, CI
   green, `CLEAN`; the conflict check against any open PR.
6. The report is **`4_REPORT_PR3.md`** in this folder (not §13's name); screenshots in `shots\pr3\`. Write
   nothing else outside the repository.

## 2. A test you cannot run stops the work

A test **failing** because its code is not written yet is the plan's red step — normal. A test, lane or
command you **cannot run** is not: it errors before any test runs (the database unreachable, Docker down, a
port taken, a module or `dist` missing, a migration pending, `No test files found`, a Vitest or TypeScript
startup error, the whole run timing out, a crash with no result); a break you could not make or run; a
real-run case you could not perform. **Then stop at once** — never skip, `.skip` or delete a test, never
change a config, a timeout, `.env`, a script or a lane, never mock what the plan does not, never run a
narrower command and call it the lane, never call it "flaky" and move on. Write the command, its exact
error and where you were into the report, and reply with §5's shape, `Status: STOPPED`.

**A plan that proves false against the code:** stop too, say exactly what and why, and offer the fix — do
not choose it yourself. **A break that stays green:** stop, unless it is plainly your own test's defect —
then strengthen the test, see the break go red, and state it as a departure.

**Never claim a result you did not see:** a command passed only if you saw its own output say so; copy that
line. A break counts only when you saw it red. No "all tests pass".

## 3. Limits, and not losing work

- Write `4_REPORT_PR3.md` **as you go**: after the first checks, after each commit (sha, subject with its
  length, the red line before the code, the green line after), after each break, after the real run, after
  the push. If you stop for any reason, the report already says where the work stands.
- **One full test run at a time on this machine:** before each full lane, check no `vitest` runs under
  `C:\dev\masaha\app-b\`; if one does, wait. Focused runs of one or two files are fine.
- Each full lane **once, on the head**; re-run only if a file it covers changed after it passed.

## 4. The real run

`docker start masaha-postgres-1` (never `db:up`; never `npm ci`); API on 3320, web on 5320, worker A's
`masaha_dev` (migrated to `main`). A browser tool that takes **real screenshots** — the `playwright` MCP
tools if you have them, otherwise local headless Chrome over CDP (as PR 2 did); say which. Cases: §13's
*PR 3* list, plus the approval note's (d): the add sheet, the upgrade confirm and the password dialog in
English dark, and at 390 and 768. Also: a link refused with `ACCOUNT_PASSWORD_PENDING` (an owner just added,
password not yet changed, linked to a second space). Screenshots to
`C:\dev\masaha\workspace\WORKER_A\OWNERS\shots\pr3\` (moved there if saved elsewhere).

## 5. Discipline

Stage by path (never `-A` or `.`); each commit message written to a UTF-8 file **without a BOM, LF line
endings**, with a body saying why, and `git commit -F <file>`; subjects counted ≤ 50; **no tool
attribution**; a fix before the push folds into its commit; never print a secret; never merge, create an
Issue, or comment on another PR. `git status --short` clean at the end; stop both servers by process id;
ports 3320 and 5320 free.

## 6. Your final reply — this shape, finished or stopped

```
Status: DONE | STOPPED
PR: #<n> <url> · head <sha> · CI <green/red/pending> · <CLEAN/not CLEAN>   (or "no PR")
Commits: <sha> <subject> (<chars>) — one line each
Ran and passed: <each command, with the result line you saw>
Ran and failed: <each, what failed, what you did>   (or "none")
COULD NOT RUN: <each test, lane, break or real-run case not run, the exact command, the exact error,
               why>   (or "none" — only if every planned run happened)
Breaks: <each: red seen / NOT red (why)>
Real run: <each case and its screenshot, or NOT RUN (why)>
Departures from the plan: <each, with its reason>   (or "none")
Stopped at (if STOPPED): <the step, and what the owner must decide or fix>
Report: C:\dev\masaha\workspace\WORKER_A\OWNERS\4_REPORT_PR3.md
```
