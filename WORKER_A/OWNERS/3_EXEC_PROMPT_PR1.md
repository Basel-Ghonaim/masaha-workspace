# OWNERS — execute PR 1 only (`feat/admin-owners`)

You are the **executor** of the first of three pull requests of one Work Item, in a fresh conversation. You
did not plan it and you will not review it. **The plan is approved; do not re-decide anything in it.**

## 1. Read, then begin

1. Work in `C:\dev\masaha\app` only — never in `C:\dev\masaha\app-b` (worker B builds PACKAGES
   there) or a design worktree. Read `CLAUDE.md` at the repository's root.
2. Read the plan **whole**: `C:\dev\masaha\workspace\WORKER_A\OWNERS\2_PLAN.md` — **the owner's approval at its
   top binds** (the words «مالك» / «صاحب المساحة» and the glossary line in commit 3; the report names).
3. **Build PR 1 only** — its three commits (§7 *PR 1*, §9 *PR 1 · commits 1–3*, §10 *PR 1*). Nothing of PR 2
   or PR 3: no `Combobox` change, no `lineParts` move, no dialog, no linking.
4. Follow §13: the first checks (`git diff --name-status 5e8c979d origin/main` — worker B's PACKAGES may have
   merged: re-read the shared documents; stop on a §7 code file the plan does not cover; if
   `packages/shared` changed, `npm run build -w @masaha/shared` before any web check), the branch
   `feat/admin-owners` from the latest `origin/main`, per commit `lint` and `typecheck`, on the head once
   each lane, the real run (`docker start masaha-postgres-1`, never `db:up`; never `npm ci` here), the
   `#PRNUM` step, push, the PR, CI and `CLEAN`, the conflict check against any open PR.
5. Do not use the project's skills unless you are Claude Code; the plan is enough. Write nothing outside
   the repository except this folder's `4_REPORT_PR1.md` and `shots\pr1\`.

## 2. A test you cannot run stops the work

A test **failing** because its code is not written yet is the plan's red step — normal. A test, lane or
command you **cannot run** is not: it errors before any test runs (the database unreachable, Docker down, a
port taken, a module or `dist` missing, a migration pending, `No test files found`, a Vitest or TypeScript
startup error, the whole run timing out, a crash with no result); a break you could not make or run; a
real-run case you could not perform (including: no `playwright` MCP tools). **Then stop at once** — never
skip, `.skip` or delete a test, never change a config, a timeout, `.env`, a script or a lane, never mock
what the plan does not, never run a narrower command and call it the lane, never call it "flaky" and move
on. Write the command, its exact error and where you were into the report, and reply with §5's shape,
`Status: STOPPED`.

**A plan that proves false against the code** (as a planned expectation the shared code cannot produce):
stop too, say exactly what and why, and offer the fix — do not choose it yourself.

**Never claim a result you did not see:** a command passed only if you saw its own output say so; copy
that line. No "all tests pass".

## 3. Limits, and not losing work

- Write `4_REPORT_PR1.md` **as you go**: after the first checks, after each commit (sha, subject with its
  length, the red line before the code, the green line after), after each break, after the real run, after
  the push. If you stop for any reason, the report already says where the work stands.
- **One full test run at a time on this machine:** before each full lane, check no `vitest` runs under
  `C:\dev\masaha\app-b\`; if one does, wait. Focused runs of one or two files are fine.
- Each full lane **once, on the head**; re-run only if a file it covers changed after it passed.

## 4. Discipline

Stage by path (never `-A` or `.`); each commit message written to a UTF-8 file **without a BOM** and
`git commit -F <file>` (real line breaks, no literal `\n`); subjects counted ≤ 50; **no tool attribution**;
a fix before the push folds into its commit; never print a secret; never merge, create an Issue, or comment
on another PR. The real run's screenshots go to `C:\dev\masaha\workspace\WORKER_A\OWNERS\shots\pr1\` (moved
there if the tool saved them in the repository); `git status --short` clean at the end; stop both servers
by process id; ports 3320 and 5320 free.

## 5. Your final reply — this shape, finished or stopped

```
Status: DONE | STOPPED
PR: #<n> <url> · head <sha> · CI <green/red/pending> · <CLEAN/not CLEAN>   (or "no PR")
Commits: <sha> <subject> (<chars>) — one line each
Ran and passed: <each command, with the result line you saw>
Ran and failed: <each, what failed, what you did>   (or "none")
COULD NOT RUN: <each test, lane, break or real-run case not run, the exact command, the exact error,
               why>   (or "none" — only if every planned run happened)
Breaks: <each: red seen / NOT RUN (why)>
Real run: <each case and its screenshot, or NOT RUN (why)>
Departures from the plan: <each, with its reason>   (or "none")
Stopped at (if STOPPED): <the step, and what the owner must decide or fix>
Report: C:\dev\masaha\workspace\WORKER_A\OWNERS\4_REPORT_PR1.md
```
