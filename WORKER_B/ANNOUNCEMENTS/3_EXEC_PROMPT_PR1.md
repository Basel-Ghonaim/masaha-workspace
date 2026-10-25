# ANNOUNCEMENTS — execute PR 1 only (`feat/announcements`)

You are the **executor** of the first of step 10's four pull requests, in a fresh conversation. You did not
plan it and you will not review it. **The plan is approved; do not re-decide anything in it.** You build it
whole: the migration, the code, the tests, the breaks, the real run, the PR, CI.

## 0. What to read — and only this (the owner's instruction)

The owner's instruction overrides the bootstrap's session checklist for this task, stated here: **do not run
the `start-work-item` skill** and do not read `docs/development/workflow.md` whole. `CLAUDE.md` is already in
your context. Read only:

1. `C:\dev\masaha\workspace\WORKER_B\ANNOUNCEMENTS\2_PLAN.md` — **these parts only:** its header and the owner's
   approval note at its top (lines 1–55, binding, it wins where the plan differs); §1; §2 *Scope*, *Acceptance
   criteria* and *Out of scope* as they touch PR 1; §3 *Assumptions* (A1–A11); §4's owner's decisions, D1–D7,
   D12 and D13 as they name PR 1, D14, D15's PR 1 part; §5 S1, S4, S5, S10, S12, *Rules the item touches*; §6;
   §7 as it names PR 1; §9 *PR 1* and *Not tested, and said*; §10; §11 *PR 1* (C1–C5); §12 (12.1–12.9 for PR 1,
   the stop rule, *Stop and ask*); §13; Appendix A *PR 1*. Nothing of PRs 2–4 unless a step needs it.
2. In the repository: the code and documents a step touches, when that step needs them — search first
   (`git grep`), then read the section, not the whole file. The `add-error-code` skill applies to each new
   error code and the `open-pr` skill may help at the end; no other skill is needed.

Read each file once. If a step proves to need a document not named here, read the part it needs and say so in
the report.

## 1. Then begin

1. **Preconditions:** SUBSCRIPTIONS PRs 1–3 (#102, #106, #109), DEMO_SEED (#104) and the fix #110 merged
   (`main` at `8fc5939e` or later). `C:\dev\masaha\app-b` detached at the latest `origin/main` and clean. If any
   fails, stop. **No `0_CARRIED_FROM_*.md` in this folder:** nothing is carried into this PR.
2. Work in `C:\dev\masaha\app-b` only — never in `C:\dev\masaha\app` (worker A) or `C:\dev\masaha\app-design`.
3. **12.1 first:** the base diff from `befd96f9` to `origin/main`, read against §3's assumptions A1–A11. **Since
   the plan was written, also merged:** SUBSCRIPTIONS' check-ins (#109: `occupancy/present.ts`,
   `occupancy.checkInWarnings`, the desk's subscriber check-in and check-out) and #110 (a subscriber's
   check-out now closes at `spaces.stayEnd`, the due time; the check-in maps its open-check-in index to
   `MEMBER_ALREADY_CHECKED_IN`). Check A5 against what merged: the subscriber check-in calls
   `occupancy.checkInWarnings`, so C5's `CLOSURE_IN_FORCE` reaches both check-ins. **A difference the plan does
   not cover → stop and ask**; any other change to a code file this PR names → stop and ask.
4. **Open PRs:** worker A's PUBLIC PR 4 (`feat/home-about`, web only) may be open. It touches no
   `packages/shared` and no `errors.ts`, but may touch web test fixtures or files under
   `apps/web/src/features/directory`. **The owner's Q10:** you edit only the fixture lines the `PublicSpace` type
   change breaks; if a worker-A PR touching those same files is open when yours is ready, yours merges after it
   and rebases — say so in the report and the description. Shared documents (`directory.md`, `overview.md`,
   `docs/README.md`, the findings index): re-read them on the merged tree before editing, each side keeps its
   own lines.
5. **Then build PR 1 only** — the plan's C1–C5, following §12 in order for PR 1: the branch
   `feat/announcements` from the latest `origin/main` (`--no-track`); `npm run build -w @masaha/shared`; 12.2's
   first checks; the commits (12.3, per commit `npm run lint` and `npm run typecheck`, and the test files the
   commit touches, in their lanes); **the migration `announcement_key`** (C1) — the plan's SQL, `migrate dev
   --create-only` **once**, then `ls` the folder (a second run applies it to `masaha_b_dev`); read the SQL
   before applying; the head's verification (12.4); every break of 12.5 for PR 1; the real run on 3321 (12.6's
   *PR 1* cases, on the demo data); `#PRNUM`; push; the PR (12.7, titled
   `feat(announcements): tell users what changes`; labels `feat`, `area:api`, `area:docs`, and `area:web` only
   if `apps/web` changes); CI green and `CLEAN`; the conflict check (12.8); the description (12.9). Stop at the
   plan's *Stop and ask*.
6. **Size:** the plan says ≈ 50 files; **stop and ask only past 65 files**.
7. `docker start masaha-postgres-1` (never `db:up`, never `npm ci`; if Docker Desktop is not running, stop and
   ask the owner to start it); `masaha_b_dev` / `masaha_b_test` at #106's migration (`prisma migrate status`
   first; anything else pending → stop and ask). No new dependency. **Finding numbers:** a new one takes
   **150** and on, in order.
8. **The new error codes** (the plan's §13 list and Q1's Arabic): each with the `add-error-code` skill, in
   `packages/shared` and both web catalogues' `errors.ts`, word for word as approved; list them in the reply.
9. **The demo data:** `masaha_b_dev` holds the demo set and SUBSCRIPTIONS' real runs' rows. Read what you need
   with `GET`s first. A case the data cannot show → **stop and report**; never change data through the app to
   get past it. What the run itself writes (announcements, the visit and its check-out), say in the report.
10. Write nothing outside the repository except this folder's `4_REPORT_PR1.md` and `scripts\`.

## 2. What runs where (the owner's rule: no run that only repeats another)

- A test seen red before its code is its own break — record that red line once. A **separate** break only for
  a guard the red step did not prove (each permission; each idempotency key; each state rule — not started,
  ended, deleted; the closure warning; each race §12.5 names).
- **On the head, once:** `npm run lint`, `npm run typecheck`, `npm run test:unit`, `npm run test:api` (the full
  API lane stays local: authorization and the schema), `npm run format:check`, `npm run check:links`, and
  12.4's `git` checks. **Not run locally — CI judges:** `test:component`, the web build, `check:build`,
  `check:classes`; report them under "Not run locally (CI judges)", not under COULD NOT RUN — unless
  `apps/web` changes beyond `errors.ts`: then also `npm run test:component -w @masaha/web --` the folders it
  touches, and say so.
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
machine is quieter (no `vitest` of `C:\dev\masaha\app\` running — worker A runs its web lanes in parallel —
the free memory recorded); killed again → record it, carry on, and **CI's run of that lane on the pushed head
is the judge** — red there → stop.

**A plan that proves false against the code:** stop, say exactly what and why, and offer the fix — do not
choose it yourself. **A break that stays green:** stop — unless it is plainly your own test's defect, or the
plan's break cannot change the outcome; then make the break that can, see it red, and state it as a departure.
**Anything you would leave undone: stop and ask** — never silently.

**Never claim a result you did not see:** a command passed only if you saw its own output say so; copy that
line (read it by its exit code, not the tail). A break counts only when you saw it red.

## 4. Limits and not losing work

- Write `4_REPORT_PR1.md` **as you go**: after the first checks, after each commit (sha, subject with its
  length, the red line before the code, the green line after), after each break, after the real run, after
  the push. If you stop for any reason, the report already says where the work stands.
- Keep a long command's output in a file under `scripts\` and read its exit code and the lines you need, not
  the whole output.
- One full lane at a time; each **once, on the head**. Keep the scripts for breaks and the real run in this
  folder's `scripts\`, never committed. The real-run script judges itself (`PASS|FAIL` per case against the
  expected status and code, `ALL PASS` and exit 0), as `WORKER_B\SUBSCRIPTIONS\scripts\realrun2.mjs` does.

## 5. Discipline

Stage by path (never `-A` or `.`); each commit message written to a UTF-8 file **without a BOM, LF line
endings**, with a body saying why, and `git commit -F <file>`; subjects counted ≤ 50; **no tool
attribution**; no `fixup!`, `style:` or `wip` commit left — a fix before the push folds into its commit
(`--fixup` + `GIT_SEQUENCE_EDITOR=:` autosquash); `#PRNUM` replaced in each commit's tree just before the push
(`C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\scripts\prnum-fix109.sh` is the latest model — copy it into
this folder's `scripts\`, adapt its branch to `feat/announcements` and its expected number to the next free
one, checked with `gh pr list --state all --limit 1`, keep its checks), never in the working tree alone; the PR
opened with `gh pr create`; never print a secret or a demo phone number; never merge, create an Issue, or
comment on another PR. `git status --short` clean at the end; stop the API by process id; port 3321 free.

## 6. Your final reply — this shape, finished or stopped

```
Status: DONE | STOPPED
PR: #<n> <url> · head <sha> · CI <green/red/pending> · <CLEAN/not CLEAN> · files <count>   (or "no PR")
Commits: <sha> <subject> (<chars>) — one line each
Migration: <name> · applied to masaha_b_dev and masaha_b_test · migrate status <line>
New error codes: <each, with its Arabic and English lines>   (or "none")
Ran and passed: <each command, with the result line you saw>
Ran and failed: <each, what failed, what you did>   (or "none")
Not run locally (CI judges): <each lane, and CI's result on the head once seen>
COULD NOT RUN: <each test, lane, break or real-run case not run, the exact command, the exact error,
               why>   (or "none" — only if every planned run happened)
Breaks: <each: red seen (in the red step or as its own break) / NOT red (why)>
First checks: <each of §12.1 (A1–A11) and §12.2 for PR 1, ✔ or what it found>
Real run: <each case and its answer, or NOT RUN (why)> · data changed: <what>
Open PRs and merge order: <worker A's open PR, shared files, which merges first>
Departures from the plan: <each, with its reason>   (or "none")
Stopped at (if STOPPED): <the step, and what the owner must decide or fix>
Report: C:\dev\masaha\workspace\WORKER_B\ANNOUNCEMENTS\4_REPORT_PR1.md
```
