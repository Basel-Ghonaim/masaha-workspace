# SUBSCRIPTIONS — execute PR 2 only (`feat/subscriptions`)

You are the **executor** of the second of step 8's three pull requests, in a fresh conversation. You did not
plan it and you will not review it. **The plan is approved; do not re-decide anything in it.**

## 1. Read, then begin

1. **Preconditions:** SUBSCRIPTIONS PR 1 (#102) is merged — `gh pr view 102 --json state` → `MERGED` (at
   `43b34cd3`, 2026-10-21) — and worker B's DEMO_SEED (`chore/directory-demo-set`) is merged —
   `gh pr list --state merged --head chore/directory-demo-set`; if either is not, stop.
2. Work in `C:\dev\masaha\app-b` only — never in `C:\dev\masaha\app` (worker A) or `C:\dev\masaha\app-design`
   (reviews and planners read there). Read `CLAUDE.md` at the repository's root.
3. Read the plan **whole**: `C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\2_PLAN.md` — **the owner's approval
   note at its top binds** (§13 as planned; A3 taken: a subscription's name correctable by the staff — this
   PR's; findings from 120). Read your PR 1 report `4_REPORT_PR1.md` whole, its *Fix round 1* included: the
   balance query is now a `LEFT JOIN LATERAL` per item with the customers asked passed in (`balancesOf`), which
   this PR's renewal reads **under the space's lock** — re-read it against the plan's D5–D7.
4. **Carried from #102 — this PR's first commit(s), before the plan's C1:** read
   `C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\0_CARRIED_FROM_102.md` whole and #102's review
   `6_REVIEW_PR1_CLAUDE_CODE.md` — the phone search in any form, the three documents, the archived customer's
   file kept for reception (a contract line), the error's comment, findings 121–123 recorded, and **item 6: an
   index serving the balances' visits branch, in this PR's planned migration**. Each code fix red first, then
   green. The PR's description says "Carried from #102". If an item proves larger than the file says, **stop
   and ask**.
5. **Then build PR 2 only** — subscriptions and their money: the plan's §2 *Scope* and *Acceptance criteria*
   for PR 2, §4's decisions as they touch PR 2 (D6–D10, D14), §5's S2, S3, S6, S7, S8, §9 *PR 2*, §11 *PR 2*,
   §12 for PR 2. Nothing of PR 3.
6. Follow §12 in order for PR 2: 12.1 (the base diff from `a86645f5` — PR 1's head after its fix round — with
   DEMO_SEED's merged files read in: a code file this PR names changed in a way the plan does not cover → stop
   and ask); the branch `feat/subscriptions` from the latest `origin/main` (`--no-track`); `npm run build -w
   @masaha/shared`; 12.2's first checks; the commits (12.3, per commit `lint` and `typecheck`); **the migration
   `subscription_terms`** (with carried item 6's index, and finding 80 folded — S8), created **once** (`migrate
   dev --create-only` once, then `ls`; in a non-TTY shell or on a data-loss refusal use `migrate diff --script`,
   as PR 1 did), then `prisma generate` and `npm run db:migrate` (`masaha_b_dev`; `masaha_b_test` as the plan
   says); the head's verification (12.4, with item 9 below); the breaks of 12.5 for PR 2; the real run on 3321
   (12.6, on the demo data); `#PRNUM`; push; the PR (12.7); CI green and `CLEAN`; the conflict check (12.8:
   worker A's PUBLIC PR 2 may be open — shared documents only); the description (12.9, the new codes' Arabic as
   §13 Q2 approved them). Stop at the plan's *Stop and ask*.
7. `docker start masaha-postgres-1` (never `db:up`, never `npm ci`; if Docker Desktop is not running, stop and
   ask the owner to start it); `masaha_b_dev` / `masaha_b_test`. No new dependency. **Finding numbers:** 121–123
   are the carried file's; a new one takes 124 and on.
8. If you are Claude Code, the project's skills may help (the plan's appendix is only a map). Write nothing
   outside the repository except this folder's `4_REPORT_PR2.md` and `scripts\`.
9. **What runs where (the owner's rule, 2026-10-21: no run that only repeats another):** a test seen red before
   its code is its own break — record that red line once; a **separate** break only for a guard the red step
   did not prove (each permission; each money rule — a price never below what was paid (S2), a renewal at most
   once (S3), the debt allocated oldest first, the hand-typed price's reason; each idempotency key; each race).
   On the head once: `test:unit`, `test:api` (the full API lane stays local for this money PR),
   `format:check`, `check:links`. **Not run locally — CI judges:** `test:component`, the web build,
   `check:build`, `check:classes` (only the web's errors catalogue changes); report them under "Not run locally
   (CI judges)", not under COULD NOT RUN.

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

- Write `4_REPORT_PR2.md` **as you go**: after the first checks, after each commit (sha, subject with its
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
Carried from #102: <each of items 1–6: done in <sha>, red then green / recorded as finding <n>>
Migrations: <each name> · created once <yes/no> · applied to masaha_b_dev <yes/no>
New error codes: <each, with its Arabic and English lines>
Ran and passed: <each command, with the result line you saw>
Ran and failed: <each, what failed, what you did>   (or "none")
Not run locally (CI judges): <each lane, and CI's result on the head once seen>
COULD NOT RUN: <each test, lane, break or real-run case not run, the exact command, the exact error,
               why>   (or "none" — only if every planned run happened)
Breaks: <each: red seen (in the red step or as its own break) / NOT red (why)>
First checks: <each of §12.2 for PR 2, ✔ or what it found>
Real run: <each case and its answer, or NOT RUN (why)>
Departures from the plan: <each, with its reason>   (or "none")
Stopped at (if STOPPED): <the step, and what the owner must decide or fix>
Report: C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\4_REPORT_PR2.md
```
