# DESK — execute PR 4 only (`feat/visit-debts`)

You are the **executor** of DESK's fourth pull request, in a fresh conversation. You did not plan it and you
will not review it. **The plan is approved; do not re-decide anything in it.**

## 1. Read, then begin

1. **Precondition:** PR 3 (#97) is merged — `gh pr view 97 --json state` → `MERGED` (at `abc28e73`,
   2026-10-20); if not, stop.
2. Work in `C:\dev\masaha\app-b` only — never in `C:\dev\masaha\app` (worker A) or
   `C:\dev\masaha\app-design` (a planner may be reading there). Read `CLAUDE.md` at the repository's root.
3. Read the plan **whole**: `C:\dev\masaha\workspace\WORKER_B\DESK\2_PLAN_PR4.md` — **the owner's approval
   note at its top binds** (§13 Q1–Q7 as planned; the Arabic lines as written; the finding numbers).
4. **Carried from #97 — this PR's first two commits, before the plan's C1:** read
   `C:\dev\masaha\workspace\WORKER_B\DESK\0_CARRIED_FROM_97.md` whole and the review it cites
   (`6_REVIEW_PR3_CLAUDE_CODE.md`), and build it as it says — (1) the auto check-out keeps closing stays past a
   failing one; (2) the owner's choice (b), widened: every stay due by 23:59 of its check-in's Gaza day, with
   unit tests for the three branches; the documents (items 3–6); the findings 111, 112, 113 (item 7) — #95's
   nit 9 resolved by item 2. Each code fix red first, then green, with its break. If an item proves larger
   than the file says, stop and ask.
5. **Then build the plan's commits** — the payment after the check-out, «تسجيل دينًا», the write-off and its
   undo — as §11 lists them, and §12's procedure in order: 12.1 (the base diff from `abc28e73`); the branch
   `feat/visit-debts` from the latest `origin/main` (`--no-track`); `npm run build -w @masaha/shared`; 12.2's
   first checks; the commits (per commit `lint` and `typecheck`); the migration created **once**
   (`migrate dev --create-only` once, then `ls`; on a data-loss refusal use `migrate diff --script`), then
   `prisma generate` and `npm run db:migrate` (applies to `masaha_b_dev`); the head's verification; **every
   break made and seen red**; the real run on 3321; `#PRNUM`; push; the PR; CI green and `CLEAN`; the
   conflict check (worker A's OWNER_SETUP may be open — shared documents only); the description (the new
   codes' lines listed for the owner, "Carried from #97"). Stop at the plan's *Stop and ask* points.
6. `masaha_b_dev` / `masaha_b_test`; `docker start masaha-postgres-1` (never `db:up`). No new dependency.
7. If you are Claude Code, the project's skills may help (the plan's appendix is only a map). Write nothing
   outside the repository except this folder's `4_REPORT_PR4.md` and `scripts\`.

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

**A carried item you judge not small, or a review nit you would leave undone: stop and ask** — never leave
one silently (#97's review, finding 3).

## 3. Limits, memory, and not losing work

- Write `4_REPORT_PR4.md` **as you go**: after the first checks, after each commit (sha, subject with its
  length, the red line before the code, the green line after), after each break, after the real run, after
  the push. If you stop for any reason, the report already says where the work stands.
- **Memory:** the machine is shared and has run low. Before each full lane: no `vitest`, `tsc` or dev server
  of `C:\dev\masaha\app\` runs (worker A's — never stop its processes; wait), and the free memory written
  into the report. One full lane at a time. A lane killed for memory: stop at once, no retry.
- Each full lane **once, on the head**; re-run only if a file it covers changed after it passed.
- Keep the scripts you write for breaks and the real run in this folder's `scripts\`, never committed.

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
Commits: <sha> <subject> (<chars>) — one line each, the carried ones first
Carried from #97: <each of items 1–7: done, its test and break red seen / not done (why)>
Migration: <its name> · created once <yes/no> · applied to masaha_b_dev <yes/no>
New error codes: <each, with its Arabic and English lines>
Ran and passed: <each command, with the result line you saw>
Ran and failed: <each, what failed, what you did>   (or "none")
COULD NOT RUN: <each test, lane, break or real-run case not run, the exact command, the exact error,
               why>   (or "none" — only if every planned run happened)
Breaks: <each: red seen / NOT red (why)>
First checks: <each of §12.2, ✔ or what it found>
Real run: <each case and its answer, or NOT RUN (why)>
Departures from the plan: <each, with its reason>   (or "none")
Stopped at (if STOPPED): <the step, and what the owner must decide or fix>
Report: C:\dev\masaha\workspace\WORKER_B\DESK\4_REPORT_PR4.md
```
