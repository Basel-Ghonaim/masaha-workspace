# SUBSCRIPTIONS — the fix PR after #109 (`fix/subscriber-checkout-due`)

You are the **executor** of one small fix pull request, in a fresh conversation. You did not write #109 and you
will not review this PR. **What to fix is decided; do not re-decide it.** You build it whole: the code, the
tests, the breaks, the PR, CI.

## 0. What to read — and only this (the owner's instruction)

The owner's instruction overrides the bootstrap's session checklist for this task, stated here: **do not run
the `start-work-item` skill**, do not write a plan file, and do not read `docs/development/workflow.md` whole.
`CLAUDE.md` is already in your context. Read only:

1. `C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\0_CARRIED_FROM_109.md` whole — it is the scope.
2. In `6_REVIEW_PR3_CLAUDE_CODE.md` (same folder) **only findings 1–5**.
3. In the repository, when a step needs it (search first with `git grep`, then read the section):
   `apps/api/src/modules/desk/desk.service.ts` (`checkOutSubscriber`, `checkOutVisit`),
   `apps/api/src/modules/visits/visits.service.ts` (`stayEndAt`), `apps/api/src/modules/spaces/autoCheckout.ts`,
   `apps/api/src/modules/subscriptions/{subscriptions.service,subscriptions.repository}.ts`, the existing
   check-out tests of the desk, `docs/architecture/data-model.md` (*Auto check-out*), `docs/api/api-contract.md`
   (*Front desk*), `docs/features/desk.md`, `docs/architecture/findings/` (the format and the index). The
   `open-pr` skill may help at the end; no other skill is needed.

Read each file once. If a step needs a document not named here, read the part it needs and say so in the report.

## 1. Then begin

1. **Preconditions:** `gh pr list --state open` — note any open PR (conflict check later). In
   `C:\dev\masaha\app-b`: `git fetch origin`, `git switch --detach origin/main`, clean. If not clean, stop.
2. Work in `C:\dev\masaha\app-b` only — never in `C:\dev\masaha\app` or `C:\dev\masaha\app-design`.
3. `docker start masaha-postgres-1` (never `db:up`, never `npm ci`; if Docker Desktop is not running, stop and
   ask the owner to start it). `npm run build -w @masaha/shared`. `masaha_b_dev` / `masaha_b_test` are at
   #106's migration; this PR has **no migration** (if one proves needed, stop and ask). No new dependency.
4. Branch `fix/subscriber-checkout-due` from `origin/main` (`--no-track`).
5. **The commits, in the file's order:** item 1 (the critical one) first, then 2, 3, 4. Each code fix: its test
   seen **red** before the code, **green** after. Per commit `npm run lint`, `npm run typecheck`, and the test
   files it touches in their lanes.
6. **Breaks** (a test seen red before its code is its own break; record that red line once): item 1 — the
   check-out's time passed back as `now` → red; the cap computed without `maxStayMinutes` → red. Item 2 — the
   mapping removed → the test answers 500 → red.
7. **On the head, once:** `npm run lint`, `npm run typecheck`, `npm run test:unit`, `npm run test:api` (the full
   API lane stays local: attendance and money), `npm run format:check`, `npm run check:links`. **Not run
   locally — CI judges:** `test:component`, the web build, `check:build`, `check:classes`.
8. **No real run** (the owner's rule: the API test proves the time; the demo data holds no overdue check-in, and
   you never change data through the app to make one). Say so in the report.
9. **Finding numbers:** 126 and 127 as the file says. `#PRNUM` where the PR's number goes, replaced in each
   commit's tree just before the push by `C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\scripts\prnum.sh`
   (adapt its branch name to `fix/subscriber-checkout-due` and its expected number to the next free number,
   which you check with `gh pr list --state all --limit 1`; keep its checks). Never in the working tree alone.
10. **The PR:** `gh pr create`, titled `fix(desk): close a subscriber's stay at its due`; labels `fix`,
    `area:api`, `area:docs`. The description says it fixes #109's review finding 1 (critical, wrong stored
    attendance and money), lists items 2–4 under "Carried from #109", and names the tests and breaks. CI green
    and `CLEAN`; the conflict check against any open PR (shared documents only).
11. **Size:** ≈ 10–14 files expected; **stop and ask past 20**.
12. Write nothing outside the repository except this folder's `4_REPORT_FIX109.md` and `scripts\`.

## 2. A test you cannot run stops the work

A test **failing** because its code is not written yet is the red step — normal. A test, lane or command you
**cannot run** is not: it errors before any test runs (the database unreachable, Docker down, a port taken, a
module or `dist` missing, a migration pending, `No test files found`, a Vitest or TypeScript startup error, a
timeout of the whole run, a crash with no result); a break you could not make or run. **Then stop at once** —
never skip, `.skip` or delete a test, never change a config, a timeout, `.env`, a script or a lane, never run a
narrower command and call it the lane, never call it "flaky". Write the command, its exact error and where you
were into the report, and reply with §5's shape, `Status: STOPPED`.

**The owner's standing exception — memory:** a full lane **killed for low memory** is re-run **once** when the
machine is quieter (no other `vitest` running, the free memory recorded); killed again → record it, carry on,
and **CI's run of that lane on the pushed head is the judge** — red there → stop. **Finding 87**'s routes test
missing its 3 s locally while it passes alone → CI judges.

**An item that proves false against the code or larger than the file says, or one you would leave undone:
stop and ask** — never silently. **A break that stays green:** stop — unless it is plainly your own test's
defect; then make the break that can, see it red, and state it as a departure. **Never claim a result you did
not see:** a command passed only if you saw its own output say so (read it by its exit code).

## 3. Not losing work

Write `4_REPORT_FIX109.md` **as you go**: after the first checks, after each commit (sha, subject with its
length, the red line, the green line), after each break, after the push. Keep a long command's output in a file
under `scripts\` and read its exit code and the lines you need. One full lane at a time.

## 4. Discipline

Stage by path (never `-A` or `.`); each commit message written to a UTF-8 file **without a BOM, LF line
endings**, with a body saying why, and `git commit -F <file>`; subjects counted ≤ 50; **no tool attribution**;
no `fixup!`, `style:` or `wip` commit left — a fix before the push folds into its commit (`--fixup` +
`GIT_SEQUENCE_EDITOR=:` autosquash); never print a secret or a demo phone number; never merge, create an Issue,
or comment on another PR. `git status --short` clean at the end; any API you started stopped by process id;
port 3321 free.

## 5. Your final reply — this shape, finished or stopped

```
Status: DONE | STOPPED
PR: #<n> <url> · head <sha> · CI <green/red/pending> · <CLEAN/not CLEAN> · files <count>   (or "no PR")
Commits: <sha> <subject> (<chars>) — one line each
Items of 0_CARRIED_FROM_109.md: <each of 1–4: done in <sha>, red then green / recorded as finding <n>>
Ran and passed: <each command, with the result line you saw>
Ran and failed: <each, what failed, what you did>   (or "none")
Not run locally (CI judges): <each lane, and CI's result on the head once seen>
COULD NOT RUN: <each test, lane or break not run, the exact command, the exact error, why>   (or "none")
Breaks: <each: red seen / NOT red (why)>
Departures: <each, with its reason>   (or "none")
Stopped at (if STOPPED): <the step, and what the owner must decide or fix>
Report: C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\4_REPORT_FIX109.md
```
