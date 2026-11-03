# BACKEND_FINAL — the whole plan in one run: worker B as the lead of sub-agents, one PR

You are **worker B's lead executor** in `C:\dev\masaha\app-b` (API on **3321**, `masaha_b_dev` / `masaha_b_test`).
You build **the whole approved plan** `C:\dev\masaha\workspace\WORKER_B\BACKEND_FINAL\2_PLAN.md` — the space's finance,
the owner's and the admin's overviews, and the API items left (C1–C16) — by running **sub-agents in parallel**, each
on its own lane, then you join their work into **one branch and one PR**, with the plan's atomic commits and the same
quality as if each part had run alone. **The owner (2026-10-29) leaves the machine to you; worker A is idle.** Do not
run the `start-work-item` skill. This file binds where it differs from the plan (§8.4 above all).

## 0. The rule for this run — you never stop until the whole task is done

- **No stop, no question, for any reason**, until the PR is open, CI is green on its head, it is `CLEAN`, the report
  is written and the final reply is sent. Read `C:\dev\masaha\workspace\_SHARED\AUTONOMY_2026-10-25.md` whole; this
  rule is stricter: **even a serious problem does not stop you** — decide, act, record, continue (§6).
- **Every decision** you or a sub-agent takes on its own is recorded under *Decisions taken without the owner*: met,
  options, chose, why, undo. One marked **SERIOUS** (§6) is listed first in the report and the reply.
- **The hard limits hold, always:** never merge; never push to `main`; never force-push a branch other than your PR
  branch; never create an Issue; **no migration unless the approved plan names one** (it names none — a need for one
  is SERIOUS: record it, find the way without it, or leave that part out per §6); never change data through the app,
  the API or the database beyond the real run's named writes (§7), never reseed `masaha_b_dev`; never touch worker A's
  worktree (`C:\dev\masaha\app`), its databases (`masaha_dev`, `masaha_test`) or ports (3320, 5320); never skip,
  `.skip`, weaken or delete a test, a check, a lane or a config to make it pass; never print a secret or keep an
  `/auth/` body; no tool attribution; never `git checkout -- <file>`, `stash` or `reset --hard` (restore from a backup
  copy); no `git add -A` / `.`; **never stop for the file count** (≈ 95 expected).
- **A refused command** (the permission classifier): carry on with everything that does not need it; write the exact
  command in the report and the reply.

## 1. Read first (closed list; search before reading more)

1. This file, whole; `AUTONOMY_2026-10-25.md`, whole.
2. `2_PLAN.md`, **whole** — the owner's approval note at its top binds (OD1–OD11 as recommended; the base moved to
   `d40d20f5`, #129 merged).
3. Worker A's lead run, for its method and its slips (read only these parts):
   `C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\4_REPORT_LEAD.md` — *Lane 0 — the lanes' setup* (LEAD-D4 its own
   worktrees, LEAD-D5 the grant script, LEAD-D6 the lanes' reports as text), *The joins*, *Memory and the grants*; its
   script `C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\scripts\heavy.mjs` (copy it into your `scripts\` and adapt).

## 2. The base

`git fetch origin`; `C:\dev\masaha\app-b` detached at the latest `origin/main` (`d40d20f5` or later), clean; `npx
prisma migrate status` on `masaha_b_dev` and `masaha_b_test` (nothing pending expected); `npm run build -w
@masaha/shared`; `docker start masaha-postgres-1` if it is down (Docker Desktop not running: `Start-Process
"C:\Program Files\Docker\Docker\Docker Desktop.exe"`, wait for `docker info`). Branch: `git switch --no-track -c
feat/backend-final origin/main`. Re-read on `main` each shared document before its first edit (#129 changed
`overview.md`, `architecture.md`, `docs/README.md`, the findings index). Finding numbers: **154 and on**.

## 3. Your role, the foundation, the lanes

You are the **lead and the integrator**: you build the foundation yourself, launch and supervise the sub-agents,
grant and schedule their test runs (§5), join their work, run the complete verification and the real run, open the
PR. **You decide how many sub-agents to run** — the plan proposes three lanes (F finance C5–C7, O overviews C8–C11,
L left items C12–C15); **more than three is allowed** (the owner's word) where a lane splits cleanly by files and
dependencies (e.g. the owner's and the admin's overviews, or L's independent items) — decide by the plan's §8.2–§8.3
and record why. Launch them with the **Agent** tool in the background; continue one with **SendMessage**. Each
sub-agent's prompt is **yours to write**, self-contained: its folder, branch and database; the plan's sections,
commits and decisions it builds (`D…`, `S…`, `T…`, `B…`, `EC…`); the files it owns and the shared files it may only add
to (§8.3's rules); the tests and breaks it must run and how it asks for a heavy run (§5); the decide-and-record rule
and §0's hard limits; the reply it returns (commits, red/green lines, breaks, decisions) — **as text** (the harness
refuses a sub-agent's report file; you save it as `scripts\lane-<x>\REPORT.md`).

### The foundation — by you, first, on `feat/backend-final`

**C1–C4** as the plan's §8.1 gives them: #130's review fixes and finding 153 (U0, C1–C3), then **C4 — the `payments`
totals both finance and the owner's overview read** (U1). Each commit atomic, its tests red before its code, its
breaks run, its documents; lint and typecheck green; **C4's API tests and the `payments` module's API test files run
green** before any lane that needs C4 starts. Lane L (no dependency on C4, §8.2) may start as soon as C1–C3 are in.

### The lanes' setup

- **Worktrees:** `git worktree add -b lane/<x> C:\dev\masaha\app-b-lane-<x> <the foundation's head>` (your own
  worktrees, as worker A did); copy `apps/api/.env` (never print it); `npm ci` **one worktree at a time**; `npm run
  build -w @masaha/shared` in each.
- **A test database per lane** (the API lane migrates and truncates its database, so two lanes may never share one):
  in the shared container, `CREATE DATABASE masaha_b_lane_<x>_test` (the name must end in `_test`); the lane's
  `apps/api/.env` gets its own `TEST_DATABASE_URL` pointing at it (only that variable changed); `npx prisma migrate
  deploy` on it. You alone own `masaha_b_test` (your foundation and the final run). Drop the lane databases after the
  PR is open (`DROP DATABASE …`), and name them in the report.
- A lane touches **only its own files** plus the shared files §8.3 gives it, adding its own block; a shared file it
  must change beyond that → its own lines only, said in its reply.

## 4. Joining the lanes

- In the order §8.4 gives (L, then F, then O), or the order your lanes' readiness and dependencies make safer
  (recorded): rebase each lane's branch onto `feat/backend-final`'s head (no merge commits in the PR; atomic commits
  kept). After each join: `npm run lint`, `npm run typecheck`, the lane's own API test files; a text conflict in a
  shared file → keep both sides in the plan's order, recorded; a semantic conflict → §6.
- Subjects as §8.1 (recount, ≤ 50), each with a body; a fix found while joining is **folded into its commit**
  (`--fixup` + `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash origin/main`); no `fixup!` left; subjects checked
  after each autosquash; a `backup/backend-final-<what>` branch before each rebase or fold, all named.
- **C16** (v1-mvp, overview.md, `docs/README.md`, conventions' *Built* line) is yours, last, on the joined branch.
- Remove the lanes' worktrees once joined (`git worktree remove`); delete the local lane branches once the PR is
  open; name what you removed.

## 5. Tests and memory — about 10 GB for you; you schedule them

- **The owner frees about 10 GB before the run.** You hold the machine's test budget: **you schedule every heavy run
  of every lane and your own** through your grant script (`heavy.mjs`, adapted), logged to `scripts\heavy-grants.log`.
  A heavy run is: a full `test:api` (≈ 10 minutes, **no command timeout**), `test:unit`, `test:component`, `lint`,
  `typecheck`, a build. **Grant a run only when ≥ 4 GB is free** after it would start; with ~10 GB free, two at once is
  the expected ceiling — **decide the number by the readings, not by habit**, and distribute the runs logically: the
  short ones (lint, typecheck, a lane's own test files) between the long ones; never two `test:api` lanes started at
  the same minute; a lane whose foundation-dependent tests are ready first goes first. A wait re-checks every 2
  minutes (bounded loops only). Record each grant, wait and end.
- **During the work, every sub-agent tests its own work:** each new test **red before its code** (copy the line),
  green after; each break of the plan's §9 for its commits **from a backup copy, restored by copy** (red line
  recorded); only the test files its change touches (`npm run test:api -w @masaha/api -- <files>` on its own test
  database; `test:unit -- <files>`) — these light runs need no grant.
- **Before a lane is joined, it passes on its own branch:** lint, typecheck, `test:unit`, and **the full `test:api` on
  its own database** — each through your grant. All green.
- **A run killed for low memory:** wait for memory, re-run it once; killed again → run it in parts (by directory) until
  every file has run green once. Record each kill. Never leave a lane unrun.
- **The final, complete verification — by you, on `feat/backend-final` after C16, before the PR is opened:** `npm run
  build -w @masaha/shared`; `npm run lint`; `npm run typecheck`; `npm run test:unit`; `npm run test:api` (on
  `masaha_b_test`); `npm run test:component`; `NODE_ENV=production npm run build` then `npm run check:build`; `npm run
  check:classes`; `check:links`; `check:conflicts`; `format:check`; `git grep -l '#PRNUM'` documents only. Then **the
  real run** (§7). Web finding 87's family (slow first lazy imports) missed in a full run and passing alone: re-run
  alone, record, go on. **Only when all of this is green do you push and open the PR.**

## 6. A problem — never a stop

- **Simple** (a test, a type, a lint rule, a document line, a lane's slip, a conflict resolved by keeping both
  sides): fix, fold into its commit, re-run what it touched **and the whole lane it failed in**, go on.
- **SERIOUS** — wrong money shown or computed, a role let through (finance is the owner's alone; the overviews per
  OV3/OV4), private data shown to whom it must not, a lock or snapshot rule broken, a need for a migration, a change to
  an approved decision, a conflict between lanes that needs a redesign, a failure across lanes: **still no stop.** Find
  its cause; take the safest course that keeps the approved decisions and the hard limits — fix it inside the plan if
  you can; else **leave that part (its commits) out of the PR** on its own branch, keep the rest whole and green, name
  it. Record it SERIOUS first. Never weaken a test to pass.
- A case the demo data lacks → never change data through the app to make it: not performed, with why and the test
  that proves it.

## 7. The real run (on the joined branch, after the verification is green)

The plan's §10 on 3321 and `masaha_b_dev`: a self-judging script (`ALL PASS`; the model:
`C:\dev\masaha\workspace\WORKER_B\FINANCE_AUDIT\scripts\realrun1.mjs`, its actor check by id); **never keep an
`/auth/` body**; each case and role as §10 names (the owner's finance windows and CSV-ready answers, the debtors'
count checked against SQL **including archived customers** as the plan corrected; reception and the admin refused on
finance; the owner's overview with no amount anywhere in its body; the admin's overview, its tiles equal to the lists
they link to; `/me`, the visits list, finding 167's filter, finding 170's case as §10 says). **Every write named, and
put back where §10 says it can be**; data left named. Stop the API by process id (`tsx watch`, the server,
`pino-pretty`); port 3321 free; `git status --short` clean.

## 8. Push, the PR, CI

- **The PR number:** `gh api "repos/Basel-Ghonaim/masaha/issues?state=all&per_page=1" --jq '.[0].number'` plus one,
  just before the push; replace `#PRNUM` in every commit's tree **before the first push** (the model:
  `C:\dev\masaha\workspace\WORKER_B\FINANCE_AUDIT\scripts\prnum-pr1.sh`); after `gh pr create`, compare; if it
  differs, redo and `git push --force-with-lease=feat/backend-final:<sha>` (refused → §0).
- `git push -u origin feat/backend-final`; `gh pr create --assignee @me --label feat --label area:api --label
  area:docs`, a title ≤ 50 (e.g. `feat(api): finance, the overviews and the rest` — recount). The description: a
  summary; **one section per part** (finance, overviews, left items) with its acceptance criteria and how each is met;
  *Carried from #130* (F1–F4); the findings resolved and recorded; the lanes and how they were joined; the local
  verification (each command, its result); the real run; the decisions taken without the owner (SERIOUS first);
  anything left out (§6) and where.
- `gh pr checks <n> --watch` (bounded; no command timeout) → green; `CLEAN`. A red lane → fix, fold, re-run it
  locally in full, push (lease on your own head), watch again.

## 9. The report and the final reply

`C:\dev\masaha\workspace\WORKER_B\BACKEND_FINAL\4_REPORT_LEAD.md`, **written as you go**: the foundation; each lane
(its sub-agent, commits, red/green lines, breaks, its test database, its grants); the joins; memory (each grant, wait,
kill); the full verification; the real run (cases, network log, writes, data left); push, PR, CI; what
`_SHARED\OPEN_DECISIONS.md` must say (the plan's §11.3 — write the lines in the report for the supervisor);
*Decisions taken without the owner* (SERIOUS first); leftovers. Write only that report and files under
`C:\dev\masaha\workspace\WORKER_B\BACKEND_FINAL\scripts\` outside the repository. Scripts in files (heredocs can fail
to parse); Python writes with `newline=""`; never `cd` into `node_modules`; `jq` is absent — use `gh --jq`.

```
Status: READY FOR REVIEW | INCOMPLETE (only if nothing at all could continue)
SERIOUS decisions: <each, one line>   (or "none")
PR: #<n> · head <sha> · CI <green/red> · <CLEAN/not CLEAN> · files <n>
Lanes: <n sub-agents, and why that many> · foundation <commits> · each lane <commits> · C16 <sha>
Left out of the PR: <part, branch, why>   (or "nothing")
Commits: <sha> <subject> (<chars>) — all, in order
Verification (local, on <sha>): <each command with its result line>
Real run: <cases> · writes <each, put back or left> · data left <rows>
Memory: <grants, peak concurrency, waits, kills>
Test databases: <made and dropped>
CI on the head: <each lane>
Findings: <resolved / recorded / new (154+)>
OPEN_DECISIONS lines for the supervisor: <in the report>
Decisions taken without the owner: <count>, in the report
Refused commands: <command>   (or "none")
Leftovers: <branches, worktrees, backups, databases>
Report: C:\dev\masaha\workspace\WORKER_B\BACKEND_FINAL\4_REPORT_LEAD.md
```
