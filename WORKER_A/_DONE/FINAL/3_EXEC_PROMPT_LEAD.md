# FINAL — the whole plan in one run: worker A as the lead of sub-agents, one PR

You are **worker A's lead executor** in `C:\dev\masaha\app` (web on **5320**, API on **3320**, `masaha_dev` /
`masaha_test`). You build **the whole approved plan** `C:\dev\masaha\workspace\WORKER_A\FINAL\2_PLAN.md` — every screen
of Masaha v1 complete, every open finding closed (web, API, shared and documents together, as the owner allowed) — by
running **sub-agents in parallel**, each on its own lane, then you join their work into **one branch and one PR**, with
the plan's atomic commits and the same quality as if each part had run alone. **The owner is away and has left the
machine to you; worker B is idle.** Do not run the `start-work-item` skill. This file binds where it differs from the
plan (§9.4 and §10.5 above all).

## 0. The rule for this run — you never stop until the whole task is done

- **No stop, no question, for any reason**, until the PR is open, CI is green on its head, it is `CLEAN`, the report
  is written and the final reply is sent. Read `C:\dev\masaha\workspace\_SHARED\AUTONOMY_2026-10-25.md` whole; this rule
  is stricter: **even a serious problem does not stop you** — decide, act, record, continue (§6).
- **Every decision** you or a sub-agent takes on its own is recorded under *Decisions taken without the owner*: met,
  options, chose, why, undo. One marked **SERIOUS** (§6) is listed first in the report and the reply.
- **The hard limits hold, always:** never merge; never push to `main`; never force-push a branch other than your PR
  branch; never create an Issue; **no migration but M1 and M2** (a need for another is SERIOUS: find the way without
  it, or leave that part out per §6); nothing on the *Not in v1* list (`docs/project/overview.md`); never change data
  through the app, the API or the database beyond the real run's named writes (§7), never reseed `masaha_dev`; never
  touch worker B's worktree (`C:\dev\masaha\app-b`), its databases (`masaha_b_*`) or port 3321; never skip, `.skip`,
  weaken or delete a test, a check, a lane or a config to make it pass; never print a secret or keep an `/auth/` body;
  no tool attribution; never `git checkout -- <file>`, `stash` or `reset --hard` (restore from a backup copy); no
  `git add -A` / `.`; **never stop for the file count** (≈ 420 expected).
- **A refused command** (the permission classifier): carry on with everything that does not need it; write the exact
  command in the report and the reply.

## 1. Read first (closed list; search before reading more)

1. This file, whole; `AUTONOMY_2026-10-25.md`, whole.
2. `2_PLAN.md`, **whole** — **the approval note at its top binds** (OD1–OD12 as recommended, DI1–DI33 as recommended,
   PA1–PA7 not taken; M1 and M2 only; §10.5's "CI judges" overridden).
3. The two lead runs before you, for their method and their slips (only these parts):
   `C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\4_REPORT_LEAD.md` — *Lane 0 — the lanes' setup* (LEAD-D4 own
   worktrees, LEAD-D5 the grant script, LEAD-D6 the lanes' reports as text), *The joins*, *The cause, found
   (LEAD-D11)*, *Memory and the grants*; `C:\dev\masaha\workspace\WORKER_B\BACKEND_FINAL\4_REPORT_LEAD.md` — its lanes'
   setup (a test database per lane) and its joins; the grant script
   `C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\scripts\heavy.mjs` (copy it into your `scripts\` and adapt).

## 2. The base

`git fetch origin`; `C:\dev\masaha\app` on `main` at the latest `origin/main` (`ce671b37` or later), clean; `npm ci`;
`npm run build -w @masaha/shared`; `npx prisma migrate status` on `masaha_dev` and `masaha_test` (nothing pending
expected); `docker start masaha-postgres-1` if down (Docker Desktop not running: `Start-Process "C:\Program
Files\Docker\Docker\Docker Desktop.exe"`, wait for `docker info`). Branch: `git switch -c feat/final origin/main`.
Re-read on `main` each shared document before its first edit. Finding numbers: **200–219 yours** (a defect found while
building that this PR does not fix); 220–239 the reviewers'.

## 3. Your role, the foundation, the lanes

You are the **lead and the integrator**: you build U0 yourself, launch and supervise the sub-agents, grant and schedule
their heavy runs (§5), join their work, build U10, run the complete verification and the real run, open the PR. **You
decide how many sub-agents to run and how many at once** — the plan proposes 8 lanes (A1, A2, L, T, W1, W2, W3, W4)
with at most 6 running; split or merge lanes where the files and §9.2's dependencies make it cleaner, and record why.
Launch them with the **Agent** tool in the background; continue one with **SendMessage**. Each sub-agent's prompt is
**yours to write**, self-contained: its folder, branch and databases; the plan's units, commits and decisions it
builds (`D…`, `S…`, `DI…`, `T…`/`B…`, `EC…`, `M…`); the files it owns and the shared files it may only add to (§9.3);
the tests and breaks it must run and how it asks for a heavy run (§5); the decide-and-record rule and §0's hard limits;
the reply it returns (commits, red/green lines, breaks, decisions) — **as text** (the harness refuses a sub-agent's
report file; you save it as `scripts\lane-<x>\REPORT.md`).

### The foundation (U0) — by you, first, on `feat/final`

U0's commits as §9.1 gives them (the routes, the navigation with its groups (165), the copy sections, the account
menu, the shells, the envelope's `details` and the new error code — C0.1, C0.2 …), each atomic, red first where a test
applies, its breaks run, lint and typecheck green. **The API lanes start as soon as C0.2 is in; the web lanes as soon
as U0 is whole** (§9.2). Merge U4's C4.1 (the `public` entries) right after U0, as §9.2 says.

### The lanes' setup

- **Worktrees:** `git worktree add -b lane/<x> C:\dev\masaha\app-lane-<x> <the foundation's head>` (your own worktrees);
  copy `apps/web/.env` and `apps/api/.env` (never print them); `npm ci` **one worktree at a time**; `npm run build -w
  @masaha/shared` in each.
- **Databases for the API lanes** (the API test lane migrates and truncates its database — two lanes never share one):
  in the shared container, `CREATE DATABASE masaha_a_lane_<x>_test` (the name must end in `_test`) for each lane that
  runs `test:api`, with its own `TEST_DATABASE_URL` in the lane's `apps/api/.env`; **lane A2 (the migrations) also gets
  `masaha_a_lane_a2_dev`** with its own `DATABASE_URL`, where it runs `npx prisma migrate dev --create-only` **once per
  migration** (then `ls` the folder; non-interactive or on a data-loss refusal → `npx prisma migrate diff --script`),
  never on `masaha_dev`; `npx prisma migrate deploy` on each lane database. No PR number in any SQL. You alone own
  `masaha_test` (the foundation and the final run) and `masaha_dev` (the real run, after `migrate deploy` of M1 and M2
  at the end). Drop the lane databases after the PR is open, and name them.
- A lane touches **only its own files** plus the shared files §9.3 gives it; a shared file it must change beyond that →
  its own lines only, said in its reply.
- **A web lane that needs an API lane's shared type** waits for that commit to be joined into `feat/final` and rebases
  onto it (§9.2); meanwhile it builds its independent commits first.

## 4. Joining the lanes

- In an order that keeps §9.2's dependencies (the API lanes and L early; W-lanes as their needs land): rebase each
  lane's branch onto `feat/final`'s head — **no merge commits in the PR**; atomic commits kept. After each join: `npm run
  lint`, `npm run typecheck`, the lane's own test files; a text conflict in a shared file → keep both sides in the
  plan's order, recorded; a semantic conflict → §6.
- Subjects as §9.1 (recount, ≤ 50), each with a body; a fix found while joining is **folded into its commit**
  (`--fixup` + `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash origin/main`); no `fixup!` left; subjects checked after
  each autosquash; a `backup/final-<what>` branch before each rebase or fold, all named.
- **U10** (the closing documents, the findings index moved once — OD9) is yours, last, on the joined branch.
- Remove the lanes' worktrees once joined; delete the local lane branches once the PR is open; name what you removed.

## 5. Tests and memory — the owner frees about 10 GB; you schedule them

- **You hold the machine's test budget:** every heavy run of every lane and your own goes through your grant script
  (`heavy.mjs`, adapted), logged to `scripts\heavy-grants.log`. A heavy run is: a full `test:api` (≈ 10 minutes, **no
  command timeout**), `test:unit`, `test:component`, `lint`, `typecheck`, a build. **Grant one only when ≥ 4 GB is
  free** after it would start; the number at once **by the readings** (about two is what fit before); never two
  `test:api` started the same minute; the short runs between the long ones. A wait re-checks every 2 minutes (bounded
  loops only). Record each grant, wait and end.
- **During the work, every sub-agent tests its own work:** each new test **red before its code** (copy the line),
  green after; each break of the plan's §10 for its commits **from a backup copy, restored by copy** (red line
  recorded); only the test files its change touches — these light runs need no grant.
- **Before a lane is joined, it passes on its own branch, through your grants:** lint, typecheck, and the full lanes
  its change reaches — `test:unit`; `test:component` for a web lane; the full `test:api` on its own database for an
  API lane. All green.
- **A run killed for low memory:** wait for memory, re-run it once; killed again → run it in parts (by directory) until
  every file has run green once. Record each kill. **Never leave a lane unrun; nothing reaches CI untested.**
- **The final, complete verification — by you, on `feat/final` after U10, before the PR is opened** (§10.5, with this
  file's memory rule): `npm ci`; `npm run build -w @masaha/shared`; `npm run format:check`; `lint`; `typecheck`;
  `check:classes`; `check:links`; `check:conflicts`; `test:unit`; `test:component` (whole); `test:api` (whole, on
  `masaha_test` after `migrate deploy`); `NODE_ENV=production npm run build` then `npm run check:build` (and the first
  download measured against `origin/main`'s); `node docs/design/scripts/check-parse.mjs` and `check-classes.mjs`;
  `git grep -l '#PRNUM'` documents only. Finding 87's family (slow first lazy imports) missed in a full run and passing
  alone: re-run alone, record, go on. Then **the real run** (§7). **Only when all of this is green do you push and open
  the PR.**

## 6. A problem — never a stop

- **Simple** (a test, a type, a lint rule, a document line, a lane's slip, a conflict resolved by keeping both sides):
  fix, fold into its commit, re-run what it touched **and the whole lane it failed in**, go on.
- **SERIOUS** — wrong money shown, sent or computed; an amount on the owner's overview; a role offered what it must
  not; private data shown to whom it must not; a key renewed on a retry or missing; a lock or snapshot rule broken; a
  need for a migration beyond M1, M2; a change to an approved decision; a conflict between lanes that needs a redesign;
  a failure across lanes: **still no stop.** Find its cause; take the safest course that keeps the approved decisions
  and the hard limits — fix it inside the plan if you can; else **leave that part (its commits) out of the PR** on its
  own branch, keep the rest whole and green, name it. Record it SERIOUS first. Never weaken a test to pass.
- A case the demo data lacks → never change data through the app to make it: not performed, with why and the test
  that proves it.

## 7. The real run (on the joined branch, after the verification is green)

`npx prisma migrate deploy` on `masaha_dev` (M1, M2) and `generate`; the plan's §11: the web on 5320 and the API on
3320, local headless Chrome over CDP (the models: `C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\scripts\run2.mjs`
on `cdp2.mjs`; Enter with `text: '\r'`; **never keep an `/auth/` body**); each screen, each role (owner, reception,
admin, user, guest), Arabic light and English dark at 390 / 768 / 1440 where layouts change; the network log (method,
URL, status, `Idempotency-Key`); **every write named, and put back where §11 says it can be**; data left named. Shots in
`C:\dev\masaha\workspace\WORKER_A\FINAL\shots\`. Stop every server by process id (`tsx watch`, the server,
`pino-pretty`, Vite); ports 3320 and 5320 free; `git status --short` clean.

## 8. Push, the PR, CI

- **The PR number:** `gh api "repos/Basel-Ghonaim/masaha/issues?state=all&per_page=1" --jq '.[0].number'` plus one, just
  before the push; replace `#PRNUM` in every commit's tree **before the first push** (the model:
  `C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\scripts\prnum1.sh`); after `gh pr create`, compare; if it differs,
  redo and `git push --force-with-lease=feat/final:<sha>` (refused → §0).
- `git push -u origin feat/final`; `gh pr create --assignee @me --label feat --label area:web --label area:api --label
  area:docs`, a title ≤ 50 (e.g. `feat: complete every screen and close the findings` — recount). The description: a
  summary; **one section per unit** (U0–U10) with its acceptance criteria and how each is met; the screens completed;
  the findings closed (built / accepted, with numbers) and those left to the deployment; the migrations (M1, M2) and
  their SQL; the lanes and how they were joined; the local verification (each command, its result); the real run; the
  decisions taken without the owner (SERIOUS first); anything left out (§6) and where.
- `gh pr checks <n> --watch` (bounded; no command timeout) → green; `CLEAN`. A red lane → fix, fold, re-run it locally
  in full, push (lease on your own head), watch again.

## 9. The report and the final reply

`C:\dev\masaha\workspace\WORKER_A\FINAL\4_REPORT_LEAD.md`, **written as you go**: the foundation; each lane (its
sub-agent, commits, red/green lines, breaks, its databases, its grants); the joins; memory (each grant, wait, kill);
the full verification; the first download; the real run (cases, network log, writes, data left); push, PR, CI;
*Decisions taken without the owner* (SERIOUS first); leftovers. Write only that report and files under
`C:\dev\masaha\workspace\WORKER_A\FINAL\scripts\` and `shots\` outside the repository. Scripts in files (heredocs can
fail to parse); Python writes with `newline=""`; never `cd` into `node_modules`; `jq` is absent — use `gh --jq`.

```
Status: READY FOR REVIEW | INCOMPLETE (only if nothing at all could continue)
SERIOUS decisions: <each, one line>   (or "none")
PR: #<n> · head <sha> · CI <green/red> · <CLEAN/not CLEAN> · files <n>
Lanes: <n sub-agents, peak at once, and why> · U0 <commits> · each lane <commits> · U10 <sha>
Left out of the PR: <part, branch, why>   (or "nothing")
Screens: <32 complete? any gap left, and why>
Findings: <built n / accepted n / deployment 6 / new 200+>
Migrations: M1 <folder>, M2 <folder> — applied to <databases>
Commits: <n> — the list in the report
Verification (local, on <sha>): <each command with its result line>
First download: base <bytes> → head <bytes>
Real run: <cases> · writes <each, put back or left> · data left <rows>
Memory: <grants, peak concurrency, waits, kills>
Databases made and dropped: <names>
CI on the head: <each lane>
Decisions taken without the owner: <count>, in the report
Refused commands: <command>   (or "none")
Leftovers: <branches, worktrees, backups, databases>
Report: C:\dev\masaha\workspace\WORKER_A\FINAL\4_REPORT_LEAD.md
```
