# DESK — execute PR 1 only (`feat/live-status`)

You are the **executor** of the first of three (later four) pull requests of one Work Item, in a fresh
conversation. You did not plan it and you will not review it. **The plan is approved; do not re-decide
anything in it.**

## 1. Read, then begin

1. Work in `C:\dev\masaha\app-b` only — never in `C:\dev\masaha\app` (worker A builds USERS there) or
   `C:\dev\masaha\app-design`. Read `CLAUDE.md` at the repository's root.
2. Read the plan **whole**: `C:\dev\masaha\workspace\WORKER_B\DESK\2_PLAN.md` — **the owner's approval note
   at its top binds** (§13's answers; the quote's age 5 minutes; A1 moves the unpriced close to PR 2; PR 4
   and the sweep later).
3. **Build PR 1 only** — presence and live status: §4's *The code, PR by PR* for PR 1, §9 *PR 1*, §11 *PR 1*,
   §12 for PR 1, Appendix A *PR 1*. Nothing of PR 2 or PR 3 (no check-in, no check-out, no payment, no job).
4. Follow §12 in order: the checks before the branch (12.1), the branch `feat/live-status` from the latest
   `origin/main` (`--no-track`), the first checks (12.2 — the dependency check above all: `@date-fns/tz`
   resolving to the lockfile's version with no other lockfile change; else stop), the commits (12.3, per
   commit `lint` and `typecheck`), the head's verification (12.4), **every break of 12.5 for PR 1 made and
   seen red**, the real run on 3321 (12.6), `#PRNUM`, push, the PR (12.7), CI green and `CLEAN`, the
   conflict check (12.8), the PR description (12.9). Stop at §14's points.
5. `masaha_b_dev` / `masaha_b_test`; `docker start masaha-postgres-1` (never `db:up`). Installing the one
   approved dependency is the only `npm install` allowed — as §12.2 says; never `npm ci`.
6. If you are Claude Code, the project's skills may help (the plan's Appendix B is only a map). Write
   nothing outside the repository except this folder's `4_REPORT_PR1.md`.

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
not choose it yourself. **A break that stays green:** stop — unless it is plainly your own test's defect, or
the plan's break cannot change the outcome (a bound already excluded by another rule); then make the break
that can, see it red, and state it as a departure.

**Never claim a result you did not see:** a command passed only if you saw its own output say so; copy that
line (read it by its exit code, not the tail). A break counts only when you saw it red.

## 3. Limits, and not losing work

- Write `4_REPORT_PR1.md` **as you go**: after the first checks, after each commit (sha, subject with its
  length, the red line before the code, the green line after), after each break, after the real run, after
  the push. If you stop for any reason, the report already says where the work stands.
- **One full test run at a time on this machine:** before each full lane, check no `vitest` runs under
  `C:\dev\masaha\app\`; if one does, wait. Focused runs of one or two files are fine.
- Each full lane **once, on the head**; re-run only if a file it covers changed after it passed.
- If memory runs low and a command is killed, stop and report — do not narrow it.

## 4. Discipline

Stage by path (never `-A` or `.`); each commit message written to a UTF-8 file **without a BOM, LF line
endings**, with a body saying why, and `git commit -F <file>`; subjects counted ≤ 50; **no tool
attribution**; a fix before the push folds into its commit (`--fixup` + `GIT_SEQUENCE_EDITOR=:`
autosquash); never print a secret; never merge, create an Issue, or comment on another PR. `git status
--short` clean at the end; stop the API by process id; port 3321 free.

## 5. Your final reply — this shape, finished or stopped

```
Status: DONE | STOPPED
PR: #<n> <url> · head <sha> · CI <green/red/pending> · <CLEAN/not CLEAN>   (or "no PR")
Commits: <sha> <subject> (<chars>) — one line each
Dependency: @date-fns/tz <version> · lockfile changed only for it <yes/no>
Ran and passed: <each command, with the result line you saw>
Ran and failed: <each, what failed, what you did>   (or "none")
COULD NOT RUN: <each test, lane, break or real-run case not run, the exact command, the exact error,
               why>   (or "none" — only if every planned run happened)
Breaks: <each: red seen / NOT red (why)>
First checks: <each of §12.2, ✔ or what it found>
Real run: <each case and its answer, or NOT RUN (why)>
Departures from the plan: <each, with its reason>   (or "none")
Stopped at (if STOPPED): <the step, and what the owner must decide or fix>
Report: C:\dev\masaha\workspace\WORKER_B\DESK\4_REPORT_PR1.md
```
