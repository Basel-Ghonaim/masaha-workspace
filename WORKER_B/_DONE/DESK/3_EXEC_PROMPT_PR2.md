# DESK — execute PR 2 only (`feat/desk-visits`)

You are the **executor** of the second of DESK's pull requests, in a fresh conversation. You did not plan it
and you will not review it. **The plan is approved; do not re-decide anything in it.**

## 1. Read, then begin

1. **Precondition:** PR 1 (#94, `feat/live-status`) is merged — `gh pr view 94 --json state` → `MERGED`
   (merged at `eabdb919`, 2026-10-20); if not, stop.
2. Work in `C:\dev\masaha\app-b` only — never in `C:\dev\masaha\app` (worker A) or
   `C:\dev\masaha\app-design`. Read `CLAUDE.md` at the repository's root.
3. Read the plan **whole**: `C:\dev\masaha\workspace\WORKER_B\DESK\2_PLAN.md` — **the owner's approval note
   at its top binds**: the quote's age at most **5 minutes**, the check-out's audit entry recording both the
   quote time used and the request's own time; **A1 taken — the unpriced close (`VISIT_NOT_PRICED` and its
   tests) is built in this PR's check-out**, not PR 3; PR 4 and the sweep later.
4. **Carried from #94 — this PR's first two commits, before the plan's C1:** read
   `C:\dev\masaha\workspace\WORKER_B\DESK\0_CARRIED_FROM_94.md` whole and build it as it says —
   `fix(occupancy): prove the directory's live inputs` (items 1–3: the directory's closure and override
   tests with their two breaks; `v1-mvp.md`; `security.md`), then `fix(occupancy): refuse an ignored
   override` (items 4–5, the owner's decision: refused during a closure in force and on an unverified
   space, `SPACE_NOT_OPEN`; the staff's answer carries the override only while the rule uses it; a test and
   a break each). Each red first, then green. The PR's description says "Carried from #94" with both.
5. **Then build PR 2 only** — the check-in, the check-out and payment: §4's *The code, PR by PR* for PR 2,
   §9 *PR 2*, §11 *PR 2* (C1–C4, as amended by A1), §12 for PR 2, Appendix A *PR 2*. Nothing of PR 3 (no
   job, no auto check-out, no uncollected list).
6. Follow §12 in order for PR 2: 12.1 (the base diff from `eff0a3d1`: PR 1's files must match what the plan
   says they hold); the branch `feat/desk-visits` from the latest `origin/main` (`--no-track`);
   **after PR 1's merge: `npm install` once in the worktree (never `npm ci`)**, `npm run build -w
   @masaha/shared`; 12.2's first checks for PR 2; the commits (12.3, per commit `lint` and `typecheck`); C1's
   migration created **once** (`migrate dev --create-only` once, then `ls`; on a data-loss refusal use
   `migrate diff --script`), then `prisma generate` and `npm run db:migrate` (applies to `masaha_b_dev`); the
   head's verification (12.4); **every break of 12.5 for PR 2 made and seen red**; the real run on 3321
   (12.6); `#PRNUM`; push; the PR (12.7); CI green and `CLEAN`; the conflict check (12.8: worker A's #93 or
   OWNER_SETUP may be open — shared documents only); the description (12.9). Stop at §14's points.
7. `masaha_b_dev` / `masaha_b_test`; `docker start masaha-postgres-1` (never `db:up`). No new dependency.
8. If you are Claude Code, the project's skills may help (the plan's Appendix B is only a map). Write
   nothing outside the repository except this folder's `4_REPORT_PR2.md`.

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

- Write `4_REPORT_PR2.md` **as you go**: after the first checks, after each commit (sha, subject with its
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
Commits: <sha> <subject> (<chars>) — one line each, the two carried ones first
Carried from #94: <each of items 1–5: done, its test and break red seen / not done (why)>
Migration: <its name> · created once <yes/no> · applied to masaha_b_dev <yes/no>
Ran and passed: <each command, with the result line you saw>
Ran and failed: <each, what failed, what you did>   (or "none")
COULD NOT RUN: <each test, lane, break or real-run case not run, the exact command, the exact error,
               why>   (or "none" — only if every planned run happened)
Breaks: <each: red seen / NOT red (why)>
First checks: <each of §12.2 for PR 2, ✔ or what it found>
Real run: <each case and its answer, or NOT RUN (why)>
Departures from the plan: <each, with its reason>   (or "none")
Stopped at (if STOPPED): <the step, and what the owner must decide or fix>
Report: C:\dev\masaha\workspace\WORKER_B\DESK\4_REPORT_PR2.md
```
