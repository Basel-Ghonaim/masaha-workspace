# SUBSCRIPTIONS — execute PR 3 only (`feat/subscription-check-ins`)

You are the **executor** of the last of step 8's three pull requests, in a fresh conversation. You did not
plan it and you will not review it. **The plan is approved; do not re-decide anything in it.** You build it
whole: the code, the tests, the breaks, the real run, the PR, CI.

## 0. What to read — and only this (the owner's instruction, 2026-10-22)

The owner's instruction overrides the bootstrap's session checklist for this task, stated here: **do not run
the `start-work-item` skill** and do not read `docs/development/workflow.md` whole. `CLAUDE.md` is already in
your context. Read only:

1. `C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\2_PLAN.md` — **these parts only:** the owner's approval note
   at its top (lines 1–39, binding); §1; §2 *Scope* and *Acceptance criteria* for PR 3; §4's owner's decisions,
   D11, D12, D14 and D15's PR 3 part; §5 as it names PR 3 or *present*; §6; §7; §9 *PR 3* and *Not tested, and
   said*; §10; §11 *PR 3* (C1–C4); §12 (12.1–12.9 for PR 3, the stop rule, *Stop and ask*); §13; Appendix A
   *PR 3*. Nothing of PR 1 or PR 2 unless a step needs it.
2. `0_CARRIED_FROM_106.md` whole, and in `6_REVIEW_PR2_CLAUDE_CODE.md` **only the findings it cites**.
3. `4_REPORT_PR2.md` — only its departures (search `Departures`) and *Hand-over to phase 2*.
4. In the repository: the code and documents a step touches, when that step needs them — search first
   (`git grep`), then read the section, not the whole file. The `add-error-code` skill applies to a new error
   code and the `open-pr` skill may help at the end; no other skill is needed.

Read each file once. If a step proves to need a document not named here, read the part it needs and say so in
the report.

## 1. Then begin

1. **Preconditions:** `gh pr view 106 --json state` → `MERGED` (at `ab0dadbd`) and `gh pr view 107 --json
   state` → `MERGED` (`main` at `5e8379af` or later). `C:\dev\masaha\app-b` detached at the latest
   `origin/main` and clean. If any fails, stop.
2. Work in `C:\dev\masaha\app-b` only — never in `C:\dev\masaha\app` (worker A) or `C:\dev\masaha\app-design`.
3. **Carried from #106 — this PR's first commit(s), before the plan's C1:** every item of
   `0_CARRIED_FROM_106.md` (1–8: the subscribe retry refused for another customer's key; `subscriptions.md`'s
   *Authority*; the phone's suffix match kept; the debt warning on older items only; a check-in's minutes from
   SQL; the archived file's date; the 49-debt decision line; findings 124 and 125). Each code fix red first,
   then green. The PR's description names them under "Carried from #106". If an item proves larger than the
   file says, **stop and ask**.
4. **Then build PR 3 only** — the plan's C1–C4 (*present* defined once; check a subscriber in, with the four
   warnings; check out; list check-ins), following §12 in order for PR 3: 12.1 (the base diff from `d0acc06b`
   — PR 2's head — with #107's merged files read in: a code file this PR names changed in a way the plan does
   not cover → stop and ask); the branch `feat/subscription-check-ins` from the latest `origin/main`
   (`--no-track`); `npm run build -w @masaha/shared`; 12.2's first checks; the commits (12.3, per commit `npm
   run lint` and `npm run typecheck`, and the test files the commit touches, in their lanes); **no migration**
   (the plan says none: if one proves needed, stop and ask); the head's verification (12.4); the breaks of 12.5
   for PR 3; the real run on 3321 (12.6's *PR 3* cases, on the demo data); `#PRNUM`; push; the PR (12.7,
   titled `feat(desk): check subscribers in and out`; labels `feat`, `area:api`, `area:docs`, and `area:web`
   only if `apps/web` changes); CI green and `CLEAN`; the conflict check (12.8: any open PR — shared documents
   only); the description (12.9). Stop at the plan's *Stop and ask*.
5. **Size:** the plan says ≈ 38 files; with the carried items ≈ 50 is expected and accepted; **stop and ask
   only past 65 files**.
6. `docker start masaha-postgres-1` (never `db:up`, never `npm ci`; if Docker Desktop is not running, stop and
   ask the owner to start it); `masaha_b_dev` / `masaha_b_test`, both already at #106's migration. No new
   dependency. **Finding numbers:** 124–125 are the carried file's; a new one takes **126** and on.
7. **The demo data:** `masaha_b_dev` holds the demo set as #106's real run left it (رامي's visit paid and his
   two «أسبوعي» subscriptions; see `4_REPORT_PR2.md`'s phase 2). Read what you need with `GET`s first. A case
   the data cannot show → **stop and report**; never change data through the app to get past it. What the run
   itself writes (check-ins, check-outs), say in the report.
8. Write nothing outside the repository except this folder's `4_REPORT_PR3.md` and `scripts\`.

## 2. What runs where (the owner's rule: no run that only repeats another)

- A test seen red before its code is its own break — record that red line once. A **separate** break only for
  a guard the red step did not prove (each permission — `attendance.record`; each money rule; each warning's
  rule — days per week, the subscription's hours, its shift, the space full; each idempotency key; each race —
  a member checked in twice at once).
- **On the head, once:** `npm run lint`, `npm run typecheck`, `npm run test:unit`, `npm run test:api` (the full
  API lane stays local for this PR: attendance and money), `npm run format:check`, `npm run check:links`, and
  12.4's `git` checks. **Not run locally — CI judges:** `test:component`, the web build, `check:build`,
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
**A carried item you judge not small, or a review nit you would leave undone: stop and ask** — never silently.

**Never claim a result you did not see:** a command passed only if you saw its own output say so; copy that
line (read it by its exit code, not the tail). A break counts only when you saw it red.

## 4. Limits and not losing work

- Write `4_REPORT_PR3.md` **as you go**: after the first checks, after each commit (sha, subject with its
  length, the red line before the code, the green line after), after each break, after the real run, after
  the push. If you stop for any reason, the report already says where the work stands.
- Keep a long command's output in a file under `scripts\` and read its exit code and the lines you need, not
  the whole output.
- One full lane at a time; each **once, on the head**. Keep the scripts for breaks and the real run in this
  folder's `scripts\`, never committed. The real-run script judges itself (`PASS|FAIL` per case against the
  expected status and code, `ALL PASS` and exit 0), as `realrun2.mjs` does.

## 5. Discipline

Stage by path (never `-A` or `.`); each commit message written to a UTF-8 file **without a BOM, LF line
endings**, with a body saying why, and `git commit -F <file>`; subjects counted ≤ 50; **no tool
attribution**; a fix before the push folds into its commit (`--fixup` + `GIT_SEQUENCE_EDITOR=:`
autosquash); `#PRNUM` replaced in each commit's tree just before the push (`scripts\prnum.sh` in this folder
does it and checks itself — adapt its branch name to `feat/subscription-check-ins`, keep its checks), never in
the working tree alone; the PR opened with `gh pr create`; never print a secret or a demo phone number; never
merge, create an Issue, or comment on another PR. `git status --short` clean at the end; stop the API by
process id; port 3321 free.

## 6. Your final reply — this shape, finished or stopped

```
Status: DONE | STOPPED
PR: #<n> <url> · head <sha> · CI <green/red/pending> · <CLEAN/not CLEAN> · files <count>   (or "no PR")
Commits: <sha> <subject> (<chars>) — one line each, the carried ones first
Carried from #106: <each of items 1–8: done in <sha>, red then green / recorded as finding <n>>
New error codes: <each, with its Arabic and English lines>   (or "none")
Ran and passed: <each command, with the result line you saw>
Ran and failed: <each, what failed, what you did>   (or "none")
Not run locally (CI judges): <each lane, and CI's result on the head once seen>
COULD NOT RUN: <each test, lane, break or real-run case not run, the exact command, the exact error,
               why>   (or "none" — only if every planned run happened)
Breaks: <each: red seen (in the red step or as its own break) / NOT red (why)>
First checks: <each of §12.2 for PR 3, ✔ or what it found>
Real run: <each case and its answer, or NOT RUN (why)> · data changed: <what>
Departures from the plan: <each, with its reason>   (or "none")
Stopped at (if STOPPED): <the step, and what the owner must decide or fix>
Report: C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\4_REPORT_PR3.md
```
