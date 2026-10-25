# SUBSCRIPTIONS — execute PR 2, phase 1 of 2 (`feat/subscriptions`) — Claude Code

You are the **executor of phase 1** of step 8's second pull request, in a fresh conversation. You did not plan
it and you will not review it. **The plan is approved; do not re-decide anything in it.**

**The owner's split (2026-10-22):** PR 2 runs in two phases. **You (phase 1)** build it: the carried commits,
the plan's commits, the migration, each test red then green, every break, and you **write** — not run — the
real-run script and the PR's description. **Phase 2 (another agent, OpenCode)** runs the full lanes on the
head, runs your real-run script, sets the PR number, pushes, opens the PR and watches CI. It judges nothing:
anything red comes back to Claude. So what you hand over must be **mechanical to run and self-judging**.

## 0. What to read — and only this (the owner's instruction, 2026-10-22)

The owner's instruction overrides the bootstrap's session checklist for this task, stated here: **do not run
the `start-work-item` skill** and do not read `docs/development/workflow.md` whole. `CLAUDE.md` is already in
your context. Read only:

1. `C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\2_PLAN.md` — **these parts only:** the owner's approval note
   at its top (lines 1–39, binding: §13 as planned; A3 taken — a subscription's name correctable by the staff, this
   PR's); §1; §2 *Scope* and *Acceptance criteria* for PR 2; §4's owner's decisions, D5–D10, D14 and D15's PR 2
   part; §5's S2, S3, S6, S7, S8 and *Rules the item touches*; §6; §7; §9 *PR 2* (and *Not tested, and said*);
   §10; §11 *PR 2*; §12 (12.1–12.6, 12.9, *Stop and ask*, the stop rule); §13; Appendix A *PR 2*. Nothing of PR 3.
2. `4_REPORT_PR1.md` — **only** *C4* and *Fix round 1* (the balance query is now a `LEFT JOIN LATERAL` per item
   with the customers asked passed in, `balancesOf`, which this PR's renewal reads **under the space's lock** —
   re-read it against D5–D7).
3. `0_CARRIED_FROM_102.md` whole, and in `6_REVIEW_PR1_CLAUDE_CODE.md` **only the findings it cites** (3, 4, 5,
   6, 7, 8, 9).
4. In the repository: the code and documents a step touches, read when that step needs them — search first
   (`git grep`), then read the section, not the whole file. The `add-error-code` skill applies to each new
   error code. No other skill is needed in this phase.

Read each file once. If a step proves to need a document not named here, read the part it needs and say so in
the report.

## 1. Then begin

1. **Preconditions:** `gh pr view 102 --json state` → `MERGED` (at `43b34cd3`) and `gh pr list --state merged
   --head chore/directory-demo-set` → #104 (at `5a0cda1a`). If either fails, stop.
2. Work in `C:\dev\masaha\app-b` only — never in `C:\dev\masaha\app` (worker A) or `C:\dev\masaha\app-design`.
3. **Carried from #102 — this PR's first commit(s), before the plan's C1:** every item of
   `0_CARRIED_FROM_102.md` — the phone search in any form, the three documents, the archived customer's file
   kept for reception (a contract line), the error's comment, findings 121–123 recorded, and **item 6: an index
   serving the balances' visits branch, in this PR's planned migration** (`EXPLAIN` before and after, in the
   report). Each code fix red first, then green. If an item proves larger than the file says, **stop and ask**.
4. **Then build PR 2 only**, following §12 in order: 12.1 (the base diff from `a86645f5` — PR 1's head after its
   fix round — with DEMO_SEED's merged files read in: a code file this PR names changed in a way the plan does
   not cover → stop and ask); the branch `feat/subscriptions` from the latest `origin/main` (`--no-track`);
   `npm run build -w @masaha/shared`; 12.2's first checks; the commits (12.3, per commit `npm run lint` and `npm
   run typecheck`, and the test files the commit touches, in their lanes); **the migration
   `subscription_terms`** (with carried item 6's index, and finding 80 folded — S8), created **once** (`migrate
   dev --create-only` once, then `ls`; in a non-TTY shell or on a data-loss refusal use `migrate diff --script`,
   as PR 1 did), then `prisma generate` and `npm run db:migrate` (`masaha_b_dev`; `masaha_b_test` as the plan
   says); the breaks of 12.5 for PR 2. Stop at the plan's *Stop and ask*.
5. `docker start masaha-postgres-1` (never `db:up`, never `npm ci`; if Docker Desktop is not running, stop and
   ask the owner to start it). No new dependency. **Finding numbers:** 121–123 are the carried file's; a new
   one takes 124 and on.
6. Write nothing outside the repository except this folder's `4_REPORT_PR2.md` and `scripts\`.

## 2. What runs where in phase 1 (the owner's rule: no run that only repeats another)

- A test seen red before its code is its own break — record that red line once. A **separate** break only for
  a guard the red step did not prove (each permission; each money rule — a price never below what was paid
  (S2), a renewal at most once (S3), the debt allocated oldest first, the hand-typed price's reason; each
  idempotency key; each race).
- **On the head, once, in phase 1:** `npm run lint`, `npm run typecheck`, and 12.4's three `git` checks
  (`#PRNUM` only in documents; `apps/web` only the two `errors.ts`; no `package.json` / lock change).
- **Not in phase 1 — phase 2 runs them:** `test:unit`, `test:api` (the full lanes), `format:check`,
  `check:links`, the real run. **CI judges:** `test:component`, the web build, `check:build`, `check:classes`.
- `#PRNUM` stays `#PRNUM` in the documents; never push; never open a PR.

## 3. The hand-over — phase 1 is done only when these exist

1. **`scripts\realrun2.mjs`** — 12.6's *PR 2* cases, each with its **expected** status and code written in the
   script; it prints one line per case `PASS|FAIL <case> <status> <code>` and exits non-zero on any `FAIL`. It
   reads `SEED_DEMO_PASSWORD` from `apps/api/.env` itself, never prints a secret or a demo phone, finds the demo
   customer, package and subscription by name, and generates its own idempotency keys. It ends with the audit
   query's ten actions printed (`docker exec masaha-postgres-1 psql …`). Check it against the code by reading,
   not by running it.
2. **`scripts\pr2-body.md`** — 12.9's description, complete (the carried items under "Carried from #102", the
   new codes' Arabic as §13 Q2 approved them, the evidence you have; phase 2 fills in the lanes' lines and CI's),
   `#PRNUM` where the number goes.
3. **A section `## Hand-over to phase 2`** at the end of `4_REPORT_PR2.md`: the branch and its head sha; the
   commits (sha, subject, length); the PR's title (§11); the labels (§12.7); and any precondition phase 2 must
   hold (for example the demo data's state the real run needs, or a migration applied to `masaha_b_dev`).

## 4. A test you cannot run stops the work

A test **failing** because its code is not written yet is the plan's red step — normal. A test, lane or
command you **cannot run** is not: it errors before any test runs (the database unreachable, Docker down, a
port taken, a module or `dist` missing, a migration pending, `No test files found`, a Vitest or TypeScript
startup error, the whole run timing out, a crash with no result); a break you could not make or run. **Then
stop at once** — never skip, `.skip` or delete a test, never change a config, a timeout, `.env`, a script or a
lane, never mock what the plan does not, never run a narrower command and call it the lane, never call it
"flaky" and move on. Write the command, its exact error and where you were into the report, and reply with §7's
shape, `Status: STOPPED`.

**The owner's standing exception — memory:** a run **killed for low memory** is re-run **once** when the
machine is quieter (no `vitest` of `C:\dev\masaha\app\` running, the free memory recorded); killed again →
record it and stop.

**A plan that proves false against the code:** stop, say exactly what and why, and offer the fix — do not
choose it yourself. **A break that stays green:** stop — unless it is plainly your own test's defect, or the
plan's break cannot change the outcome; then make the break that can, see it red, and state it as a departure.
**A carried item you judge not small, or a review nit you would leave undone: stop and ask** — never leave one
silently.

**Never claim a result you did not see:** a command passed only if you saw its own output say so; copy that
line (read it by its exit code, not the tail). A break counts only when you saw it red.

## 5. Limits and not losing work

- Write `4_REPORT_PR2.md` **as you go**: after the first checks, after each commit (sha, subject with its
  length, the red line before the code, the green line after), after each break. If you stop for any reason,
  the report already says where the work stands.
- Keep a long command's output in a file under `scripts\` and read its exit code and the lines you need, not
  the whole output.
- Keep the scripts you write for breaks and the real run in this folder's `scripts\`, never committed.

## 6. Discipline

Stage by path (never `-A` or `.`); each commit message written to a UTF-8 file **without a BOM, LF line
endings**, with a body saying why, and `git commit -F <file>`; subjects counted ≤ 50; **no tool
attribution**; a fix folds into its commit (`--fixup` + `GIT_SEQUENCE_EDITOR=:` autosquash); never print a
secret or a phone number of the demo data; never push, merge, open a PR, create an Issue, or comment on a PR.
`git status --short` clean at the end; no server left running; port 3321 free.

## 7. Your final reply — this shape, handed over or stopped

```
Status: HANDED OVER | STOPPED
Branch: feat/subscriptions · head <sha> · not pushed
Commits: <sha> <subject> (<chars>) — one line each, the carried ones first
Carried from #102: <each of items 1–6: done in <sha>, red then green / recorded as finding <n>>
Migrations: <each name> · created once <yes/no> · applied to masaha_b_dev <yes/no> · masaha_b_test <yes/no>
New error codes: <each, with its Arabic and English lines>
Ran and passed: <each command, with the result line you saw>
Ran and failed: <each, what failed, what you did>   (or "none")
Left to phase 2: test:unit, test:api, format:check, check:links, the real run, #PRNUM, push, PR, CI
COULD NOT RUN: <each test or break not run, the exact command, the exact error, why>   (or "none")
Breaks: <each: red seen (in the red step or as its own break) / NOT red (why)>
First checks: <each of §12.2 for PR 2, ✔ or what it found>
Hand-over files: scripts\realrun2.mjs · scripts\pr2-body.md · the report's "Hand-over to phase 2"
Departures from the plan: <each, with its reason>   (or "none")
Stopped at (if STOPPED): <the step, and what the owner must decide or fix>
Report: C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\4_REPORT_PR2.md
```
