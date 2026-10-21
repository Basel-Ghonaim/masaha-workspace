# SUBSCRIPTIONS — execute PR 1 only (`feat/customers`)

You are the **executor** of the first of step 8's three pull requests, in a fresh conversation. You did not
plan it and you will not review it. **The plan is approved; do not re-decide anything in it.**

## 1. Read, then begin

1. **Precondition:** DESK PR 4 (#100) is merged — `gh pr view 100 --json state` → `MERGED` (at `5d42a527`,
   2026-10-21); if not, stop.
2. Work in `C:\dev\masaha\app-b` only — never in `C:\dev\masaha\app` (worker A) or `C:\dev\masaha\app-design`
   (reviews read there). Read `CLAUDE.md` at the repository's root.
3. Read the plan **whole**: `C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\2_PLAN.md` — **the owner's approval
   note at its top binds** (§13 as planned; A3 taken: a subscription's name correctable by the staff — PR 2's;
   finding 113 folded into **this PR** as C6; findings from 120).
4. **Carried from #100 — this PR's first commit(s), before the plan's C1:** read
   `C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\0_CARRIED_FROM_100.md` whole and the review it cites, and
   build it as it says — the jobs answering 200 with a `failed` count (finding 114), a desk check-out charged up
   to the stay's day's end (finding 116), finding 115 recorded, the documents. Each code fix red first, then
   green, with its break. The PR's description says "Carried from #100". If an item proves larger than the
   file says, **stop and ask**.
5. **Re-read DESK PR 4's merged payment route** (`POST …/payments`, the ledger trigger, `balanceOfVisit`)
   against the plan's assumptions (§0 of the plan, §12.1): a difference the plan does not cover → stop and ask.
6. **Then build PR 1 only** — customers: the plan's §2 *Scope* and *Acceptance criteria* for PR 1, §4's
   decisions as they touch PR 1, §9 *PR 1*, §11 *PR 1* (its commits, C6 included), §12 for PR 1. Nothing of PR 2
   or PR 3.
7. Follow §12 in order for PR 1: 12.1 (the base diff from `abc28e73`, #100's merged files read in); the branch
   `feat/customers` from the latest `origin/main` (`--no-track`); `npm run build -w @masaha/shared`; 12.2's
   first checks; the commits (12.3, per commit `lint` and `typecheck`); **the two migrations**, each created
   **once** (`migrate dev --create-only` once, then `ls`; on a data-loss refusal use `migrate diff --script`),
   then `prisma generate` and `npm run db:migrate` (applies to `masaha_b_dev`; `masaha_b_test` as the plan
   says); the head's verification (12.4); **every break of 12.5 for PR 1 made and seen red**; the real run on
   3321 (12.6); `#PRNUM`; push; the PR (12.7); CI green and `CLEAN`; the conflict check (12.8: worker A's #99
   may be open, rebased — shared documents only); the description (12.9, the new codes' Arabic for the owner);
   `OPEN_DECISIONS.md` point 3 as the plan says (in the report). Stop at the plan's *Stop and ask*.
8. `docker start masaha-postgres-1` (never `db:up`; if Docker Desktop is not running, stop and ask the owner to
   start it); `masaha_b_dev` / `masaha_b_test`. No new dependency.
9. If you are Claude Code, the project's skills may help (the plan's appendix is only a map). Write nothing
   outside the repository except this folder's `4_REPORT_PR1.md` and `scripts\`.

## 2. A test you cannot run stops the work

A test **failing** because its code is not written yet is the plan's red step — normal. A test, lane or
command you **cannot run** is not: it errors before any test runs (the database unreachable, Docker down, a
port taken, a module or `dist` missing, a migration pending, `No test files found`, a Vitest or TypeScript
startup error, the whole run timing out, a crash with no result); a break you could not make or run; a
real-run case you could not perform. **Then stop at once** — never skip, `.skip` or delete a test, never
change a config, a timeout, `.env`, a script or a lane, never mock what the plan does not, never run a
narrower command and call it the lane, never call it "flaky" and move on. Write the command, its exact
error and where you were into the report, and reply with §5's shape, `Status: STOPPED`.

**The owner's standing exception — memory:** a full lane **killed for low memory** is re-run **once** when the
machine is quieter (no `vitest` of `C:\dev\masaha\app\` running, the free memory recorded); killed again →
record it, carry on with everything else, and **CI's run of that lane on the pushed head is the judge** — red
there → stop and report.

**A plan that proves false against the code:** stop too, say exactly what and why, and offer the fix — do
not choose it yourself. **A break that stays green:** stop — unless it is plainly your own test's defect, or
the plan's break cannot change the outcome (a bound already excluded by another rule); then make the break
that can, see it red, and state it as a departure. **A carried item you judge not small, or a review nit you
would leave undone: stop and ask** — never leave one silently.

**Never claim a result you did not see:** a command passed only if you saw its own output say so; copy that
line (read it by its exit code, not the tail). A break counts only when you saw it red.

## 3. Limits and not losing work

- Write `4_REPORT_PR1.md` **as you go**: after the first checks, after each commit (sha, subject with its
  length, the red line before the code, the green line after), after each break, after the real run, after
  the push. If you stop for any reason, the report already says where the work stands.
- One full lane at a time; each **once, on the head**; re-run only if a file it covers changed after it passed.
- Keep the scripts you write for breaks and the real run in this folder's `scripts\`, never committed.

## 4. Discipline

Stage by path (never `-A` or `.`); each commit message written to a UTF-8 file **without a BOM, LF line
endings**, with a body saying why, and `git commit -F <file>`; subjects counted ≤ 50; **no tool
attribution**; a fix before the push folds into its commit (`--fixup` + `GIT_SEQUENCE_EDITOR=:`
autosquash); never print a secret or a phone number of the demo data; never merge, create an Issue, or
comment on another PR. `git status --short` clean at the end; stop the API by process id; port 3321 free.

## 5. Your final reply — this shape, finished or stopped

```
Status: DONE | STOPPED
PR: #<n> <url> · head <sha> · CI <green/red/pending> · <CLEAN/not CLEAN>   (or "no PR")
Commits: <sha> <subject> (<chars>) — one line each, the carried ones first
Carried from #100: <each of items 1–5: done, its test and break red seen / not done (why)>
Migrations: <each name> · created once <yes/no> · applied to masaha_b_dev <yes/no>
New error codes: <each, with its Arabic and English lines>
Ran and passed: <each command, with the result line you saw>
Ran and failed: <each, what failed, what you did>   (or "none")
COULD NOT RUN: <each test, lane, break or real-run case not run, the exact command, the exact error,
               why>   (or "none" — only if every planned run happened)
Breaks: <each: red seen / NOT red (why)>
First checks: <each of §12.2 for PR 1, ✔ or what it found>
Real run: <each case and its answer, or NOT RUN (why)>
Departures from the plan: <each, with its reason>   (or "none")
Stopped at (if STOPPED): <the step, and what the owner must decide or fix>
Report: C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\4_REPORT_PR1.md
```
