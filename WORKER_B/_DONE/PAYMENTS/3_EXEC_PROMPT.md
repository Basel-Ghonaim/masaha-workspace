# PAYMENTS — execute the one PR (`feat/payments`)

You are the **executor** of step 9's one pull request, in a fresh conversation. You did not plan it and you
will not review it. **The plan is approved; do not re-decide anything in it.** You build it whole: the carried
fixes, the migration, the code, the tests, the breaks, the real run, the PR, CI.

## 0. What to read — and only this (the owner's instruction)

The owner's instruction overrides the bootstrap's session checklist for this task, stated here: **do not run
the `start-work-item` skill** and do not read `docs/development/workflow.md` whole. `CLAUDE.md` is already in
your context. Read only:

1. `C:\dev\masaha\workspace\WORKER_B\PAYMENTS\2_PLAN.md` **whole** (≈ 1,000 lines; it is one PR) — the owner's
   approval note at its top binds and wins where the plan differs (**Q1's correction to D8 included**).
2. `C:\dev\masaha\workspace\WORKER_B\ANNOUNCEMENTS\0_CARRIED_FROM_112.md` whole, and in
   `6_REVIEW_PR1_CLAUDE_CODE.md` (same folder) **only F1–F6**.
3. In the repository: the code and documents a step touches, when that step needs them — search first
   (`git grep`), then read the section, not the whole file. The `open-pr` skill may help at the end; no other
   skill is needed (no new error code).

Read each file once. If a step proves to need a document not named here, read the part it needs and say so in
the report.

## 1. Then begin

1. **Preconditions:** `main` at `104d9d07` (#112 merged) or later. `C:\dev\masaha\app-b` detached at the latest
   `origin/main` and clean. If not, stop.
2. Work in `C:\dev\masaha\app-b` only — never in `C:\dev\masaha\app` (worker A) or `C:\dev\masaha\app-design`.
3. **§12.1 first:** the base diff from `104d9d07` to `origin/main`, read against §3's assumptions A1–A2 (the
   demo payments of A1 included). A difference the plan does not cover → **stop and ask**. Open PRs (`gh pr
   list --state open`): `chore/conflict-guard` (CI, `package.json`, `apps/api/scripts/`, the findings index,
   `lookups.md`, `docs/frontend/architecture.md`, `workflow.md`, `setup.md`, `CLAUDE.md`) may be open — no code
   file shared with this PR; a shared document → re-read on the merged tree before editing, each side keeps its
   own lines.
4. **Carried from #112 — the first commits** (the plan's C0a, C0b), before C1. Item 4's code fix red first, then
   green. The PR's description names them under "Carried from #112".
5. **Then the plan's commits C1–C4**, following §12 in order: the branch `feat/payments` from the latest
   `origin/main` (`--no-track`); `npm run build -w @masaha/shared`; §12.2's first checks; the commits (§12.3,
   per commit `npm run lint` and `npm run typecheck`, and the test files the commit touches, in their lanes);
   **the migration `payment_void_guard`** (C1) — raw SQL, `migrate dev --create-only` **once**, then `ls` the
   folder; non-interactive or refused → `migrate diff --script` as SUBSCRIPTIONS did; **copy
   `payments_guard_change`'s body from `20260929120300_payments/migration.sql`** (its only definition on `main`,
   checked by the supervisor) and add only D9's read; read the SQL before applying; both B databases migrated;
   the head's verification (§12.4); every break of §12.5 **and Q1's new one**; the real run on 3321 (§12.6, on
   the demo data); `#PRNUM`; push; the PR (§12.7, titled `feat(payments): void payments and list them`; labels
   `feat`, `area:api`, `area:docs`, `area:web` — the two catalogue lines change); CI green and `CLEAN`; the
   conflict check (§12.8); the description (§12.9). Stop at the plan's *Stop and ask*.
6. **Size:** the plan says ≈ 44 files; **stop and ask only past 58 files**.
7. `docker start masaha-postgres-1` (never `db:up`, never `npm ci`; if Docker Desktop is not running, stop and
   ask the owner to start it); `masaha_b_dev` / `masaha_b_test` at #112's migration (`prisma migrate status`
   first; anything else pending → stop and ask). No new dependency. **Finding numbers:** a new one takes
   **170** and on, in order.
8. **The demo data:** read what you need with `GET`s first (A1: «هبة», «رامي», the voided and live
   subscription payments, nothing received today). A case the data cannot show → **stop and report**; never
   change data through the app to get past it. The run's own writes (payments recorded and voided, a write-off
   and its undo) — name each in the report.
9. Write nothing outside the repository except this folder's `4_REPORT.md` and `scripts\`.

## 2. What runs where (the owner's rule: no run that only repeats another)

- A test seen red before its code is its own break — record that red line once. A **separate** break only for
  a guard the red step did not prove (each permission — the owner's void, reception's narrowing and its refused
  filters; each money rule — a voided payment counting nowhere, the totals; the trigger's written-off rule; the
  two races of D6; Q1's priced-only clause).
- **On the head, once:** `npm run lint`, `npm run typecheck`, `npm run test:unit`, `npm run test:api` (the full
  API lane stays local: money, authorization and the schema), `npm run format:check`, `npm run check:links`, and
  §12.4's `git` checks. **Not run locally — CI judges:** `test:component`, the web build, `check:build`,
  `check:classes`; report them under "Not run locally (CI judges)", not under COULD NOT RUN.
- **A fix after a lane passed** re-runs only the test files it touches, plus `typecheck` and `lint`; say so.

## 3. A test you cannot run stops the work

A test **failing** because its code is not written yet is the plan's red step — normal. A test, lane or
command you **cannot run** is not: it errors before any test runs (the database unreachable, Docker down, a
port taken, a module or `dist` missing, a migration pending, `No test files found`, a Vitest or TypeScript
startup error, the whole run timing out, a crash with no result); a break you could not make or run; a
real-run case you could not perform. **Then stop at once** — never skip, `.skip` or delete a test, never
change a config, a timeout, `.env`, a script or a lane, never mock what the plan does not, never run a
narrower command and call it the lane, never call it "flaky" and move on. Write the command, its exact error
and where you were into the report, and reply with §6's shape, `Status: STOPPED`.

**The owner's standing exception — memory:** a full lane **killed for low memory** is re-run **once** when the
machine is quieter (no `vitest` of `C:\dev\masaha\app\` running, the free memory recorded); killed again →
record it, carry on, and **CI's run of that lane on the pushed head is the judge** — red there → stop.

**A plan that proves false against the code:** stop, say exactly what and why, and offer the fix — do not
choose it yourself. **A break that stays green:** stop — unless it is plainly your own test's defect, or the
plan's break cannot change the outcome; then make the break that can, see it red, and state it as a departure.
**A carried item or anything you would leave undone: stop and ask** — never silently.

**Never claim a result you did not see:** a command passed only if you saw its own output say so; copy that
line (read it by its exit code, not the tail). A break counts only when you saw it red.

## 4. Limits and not losing work

- Write `4_REPORT.md` **as you go**: after the first checks, after each commit (sha, subject with its length,
  the red line before the code, the green line after), after each break, after the real run, after the push.
  If you stop for any reason, the report already says where the work stands.
- Keep a long command's output in a file under `scripts\` and read its exit code and the lines you need.
- One full lane at a time; each **once, on the head**. The real-run script judges itself (`PASS|FAIL` per case
  against the expected status and code, `ALL PASS` and exit 0), as
  `WORKER_B\SUBSCRIPTIONS\scripts\realrun2.mjs` does.

## 5. Discipline

Stage by path (never `-A` or `.`); each commit message written to a UTF-8 file **without a BOM, LF line
endings**, with a body saying why, and `git commit -F <file>`; subjects counted ≤ 50; **no tool
attribution**; no `fixup!`, `style:` or `wip` commit left — a fix before the push folds into its commit
(`--fixup` + `GIT_SEQUENCE_EDITOR=:` autosquash); `#PRNUM` replaced in each commit's tree just before the push
(copy `WORKER_B\SUBSCRIPTIONS\scripts\prnum-fix109.sh` into this folder's `scripts\`, adapt its branch to
`feat/payments` and its expected number to the next free one, checked with `gh pr list --state all --limit 1`,
keep its checks), never in the working tree alone; the PR opened with `gh pr create`; never print a secret or
a demo phone number; never merge, create an Issue, or comment on another PR. `git status --short` clean at the
end; stop the API by process id; port 3321 free. The local `backup/*` branch the script leaves: say its name.

## 6. Your final reply — this shape, finished or stopped

```
Status: DONE | STOPPED
PR: #<n> <url> · head <sha> · CI <green/red/pending> · <CLEAN/not CLEAN> · files <count>   (or "no PR")
Commits: <sha> <subject> (<chars>) — one line each, the carried ones first
Carried from #112: <each of items 1–6: done in <sha>, red then green / docs>
Migration: <name> · applied to masaha_b_dev and masaha_b_test · migrate status <line>
Ran and passed: <each command, with the result line you saw>
Ran and failed: <each, what failed, what you did>   (or "none")
Not run locally (CI judges): <each lane, and CI's result on the head once seen>
COULD NOT RUN: <each test, lane, break or real-run case not run, the exact command, the exact error,
               why>   (or "none" — only if every planned run happened)
Breaks: <each: red seen (in the red step or as its own break) / NOT red (why)>
First checks: <each of §12.1 (A1–A2) and §12.2, ✔ or what it found>
Real run: <each case and its answer, or NOT RUN (why)> · data changed: <what>
Open PRs and merge order: <each open PR, shared files, which merges first>
Departures from the plan: <each, with its reason>   (or "none")
Stopped at (if STOPPED): <the step, and what the owner must decide or fix>
Report: C:\dev\masaha\workspace\WORKER_B\PAYMENTS\4_REPORT.md
```
