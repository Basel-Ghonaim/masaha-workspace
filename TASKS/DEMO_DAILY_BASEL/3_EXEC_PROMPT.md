# DEMO_DAILY — the directory's demo set renews its day-bound states on every seed run

You are a worker on the Masaha repository, in a fresh session. This file is self-contained: every file to read
and every command is named. **Two phases:** first you read and write a short plan and **stop**; the owner reads
it and writes "approved" (or changes) at its top; then you build, test, push and open one pull request. Run
commands **in PowerShell**; read each exit code with `$LASTEXITCODE` right after the command (passed only if 0).

- **Your worktree:** `C:\dev\masaha\app-design` (the design worker's; prepared: dependencies installed, shared
  built, its own databases). `TASKS\CONFLICT_GUARD_BASEL` merged (#113, 2026-10-24): the worktree is free and
  `npm run check:conflicts` now runs in CI. Others read in this worktree (a reviewer or a planner, commit objects
  only): if a `git` command fails on a `.lock` file, wait 30 s and retry once; failed again → stop and report;
  never delete a `.lock` file. Never touch `C:\dev\masaha\app` or `app-b` (workers A and B use them).
  **When you finish** (the PR open and green, or stopped), leave `app-design` detached at `origin/main` and
  clean: `git switch --detach origin/main` — reviewers read there.
- **Your databases:** `masaha_design_dev` and `masaha_design_test` in the Docker container `masaha-postgres-1`
  (port 5433); `app-design\apps\api\.env` already points at them, and the API there runs on **port 3323**.
  Never touch `masaha_dev`, `masaha_test`, `masaha_b_dev` or `masaha_b_test`.
- **Your folder:** `C:\dev\masaha\workspace\TASKS\DEMO_DAILY_BASEL\` (below: `TASK\`). Outside the worktree
  write only there: `2_PLAN.md`, `4_REPORT.md`, `scripts\`.

## The problem and the goal (the owner's, 2026-10-22)

The development-only demo set of the public directory (`apps/api/src/db/seed/demoDirectory.ts`, run by `npm
run db:seed` with `SEED_DEMO=true`) has two cases bound to the day it was seeded:
- **FULL** — `noor-hub`'s sibling spaces with `present` visitors; the one at line ≈ 132 (`capacity: 4,
  present: 4`) is full. Its visitors are checked in "within today", so the next day they no longer count and
  the space is no longer full.
- **Closed today** — the space at line ≈ 167 (`hours: { open: ['09:00', '17:00'], closedToday: true }`)
  closes **the weekday it was seeded on** (line ≈ 702). The next day another weekday is today, so it is open.

And `seedDemoDirectory` returns at once when the set exists (line ≈ 534, the marker `noor-hub`), so running
the seed again changes nothing. Real runs on any later day have recorded both cases as "not performed".

**The goal:** when the set already exists, `npm run db:seed` with `SEED_DEMO=true` **renews these day-bound
states for today** (Gaza's day), so after any run on any day: the full space is full now, and the closed-today
space is closed today. Rules:
1. Only the set's own spaces (the slugs in this file's set) — never the demo space of `demo.ts`, never any
   other space, user or table row.
2. **Idempotent within a day:** a second run the same day changes nothing (the same counts, no new rows).
3. Nothing else of the set changes on a renewal: names, prices, photos, contacts, dates of "last updated"
   stay as they are (or say in the plan exactly what moves and why).
4. Every space with `present` visitors gets exactly `present` visitors present today, not only the full one
   (the live states of the others — available, busy — must also hold today).
5. It still refuses to run in production (the existing `nodeEnv` guard).
6. Old visits from earlier days: decide in the plan what happens to them (left as they are if the API's
   *present* already ignores them; closed or removed only if they would distort today's state), and why.
   The set's visits are demo data in a development database only.

**What changed since 2026-10-22 (read it on `origin/main`, line numbers may have moved):**
- **#109** — *present* is defined once, in `apps/api/src/modules/occupancy/present.ts`: open visits **and**
  subscription check-ins. The set's present people are visits; renew them as visits and check `present.ts`'s
  rule (what makes a visit count as present today) before deciding rule 6.
- **#112** — the set now inserts a closure announcement with an `idempotencyKey` (`demoDirectory.ts` ≈ 682).
  Leave it as it is; a renewal never adds a second one.
- **The auto check-out (#97)** closes every open visit at its due time (the space's closing time, or 23:59 —
  `spaces/autoCheckout.ts`), run every 5 minutes in development. A seed run after a space's closing time would
  leave visits the job closes at once. Say in the plan how the renewal behaves then (for example: the visits'
  check-in at the start of today's opening, and a run after closing renews nothing for that space and says so),
  and test it with a fixed clock.

Out of scope: the demo space of `demo.ts`, any API route, the schema (no migration), the web, any other seed.

## What to read

1. `C:\dev\masaha\app-design\CLAUDE.md` — the project's rules (they bind you): task scope, atomic Conventional
   Commits, **no tool attribution anywhere** (no `Co-Authored-By`, no "generated with", no tool name), stage by
   path, decisions are the owner's.
2. `apps/api/src/db/seed/demoDirectory.ts` (whole), `apps/api/src/db/seed/demoDirectory.api.test.ts` (whole —
   it already checks each case through the public reads, with `now`), `apps/api/src/db/seed/run.ts`.
3. How *present* is counted: search `git grep -n "present" -- apps/api/src/modules/occupancy` and read the
   function the live status uses. **Note:** worker B is changing *present*'s definition in another branch
   right now (`refactor(occupancy): define present once`); rely on the public reads in your tests, not on
   that file's internals.
4. `docs/development/setup.md` — the line about the demo set (`SEED_DEMO`).

## Phase 1 — the plan, then stop

Write `TASK\2_PLAN.md` (one page): how a renewal finds the set and what it writes (rows, by table), the rule for
old visits (goal 6), why it is idempotent, the commits (subjects ≤ 50 characters, counted), the files, the
tests (below) and the one new sentence for `setup.md`. Then **stop** and reply only: `PLAN READY:
TASK\2_PLAN.md`. Do not edit the repository before the owner's approval note is at the plan's top.

## Phase 2 — after the owner's approval

1. **Preconditions:**
```powershell
cd C:\dev\masaha\app-design
git fetch origin; git status --short                       # expect: nothing
git switch --detach origin/main
docker ps --format '{{.Names}} {{.Status}}'                # expect: masaha-postgres-1 Up …
npm run build -w @masaha/shared; "shared exit $LASTEXITCODE"
cd apps\api; npx prisma generate; npx prisma migrate deploy; npx prisma migrate status; cd ..\..   # expect: up to date
git switch --no-track -c chore/demo-daily origin/main
```
2. **Test first.** In `demoDirectory.api.test.ts` add a test (its file's style; it already passes `now`): seed
   with `now` = day 1, then seed again with `now` = day 2 (another weekday) → on day 2 the full space reads
   full and the closed-today space reads closed today, through the same public reads the file uses; and a
   third run on day 2 → the same rows (counts of the set's visits and of everything else unchanged). Run
   **that file only**:
   `npm run test:api -w @masaha/api -- src/db/seed/demoDirectory.api.test.ts` → see it **fail** (the second
   run renews nothing); copy the failing line into the report. Then the code; run it again → pass; copy the
   line. Then **the break:** comment out the renewal's call once, run the file, see the new test fail, restore
   it exactly (`git diff` shows only your work), run it, pass. Record both.
3. **Commits** (each: `npm run lint` and `npm run typecheck`, exit 0, before committing). One feature commit,
   e.g. `chore(seed): renew the demo's day each run` (count it ≤ 50), with the test and `setup.md`'s sentence.
   The message in a file `TASK\scripts\msg-1.txt` written with your editor — UTF-8 **without BOM**, LF line
   endings: the subject, a blank line, 2–5 lines saying **why**. `git add <path> …` (never `-A` or `.`), then
   `git commit -F <file>`.
4. **On the head, once each:** `npm run test:unit -w @masaha/api`; `npm run test:api -w @masaha/api`; `npm run
   lint`; `npm run typecheck`; `npm run format:check`; `npm run check:links`. Each exit 0; copy each result line
   into the report. Before a test run, if `Get-CimInstance Win32_Process -Filter "Name='node.exe'" |
   Where-Object { $_.CommandLine -match 'vitest' }` lists anything, wait until it is empty (check every 2 min,
   at most 30 min); never stop it. A lane killed for low memory → once more when it is quieter; killed again →
   record it, CI judges.
5. **The real run** (on `masaha_design_dev` only):
```powershell
cd C:\dev\masaha\app-design
$env:SEED_DEMO='true'; npm run db:seed; "seed exit $LASTEXITCODE"; npm run db:seed; "seed again exit $LASTEXITCODE"; Remove-Item Env:SEED_DEMO
$S = 'C:\dev\masaha\workspace\TASKS\DEMO_DAILY_BASEL\scripts'
Start-Process -WindowStyle Hidden -WorkingDirectory 'C:\dev\masaha\app-design' -FilePath npm.cmd -ArgumentList 'run','dev','-w','@masaha/api' -RedirectStandardOutput "$S\api.log" -RedirectStandardError "$S\api.err.log"
```
   Wait (≤ 60 s) until `curl.exe -s http://localhost:3323/health` contains `"db":"up"`. Then read, with
   `curl.exe -s`, the public list `http://localhost:3323/api/v1/spaces?limit=50` (and the next page if the set's spaces are not all on it) and save it to
   `$S\after.json`; report the full space's and the closed-today space's live state as the API answers them
   (search the JSON for their slugs). Then stop the API:
```powershell
Get-NetTCPConnection -LocalPort 3323 -State Listen -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }
Get-CimInstance Win32_Process -Filter "Name='node.exe'" | Where-Object { $_.CommandLine -match 'masaha\\app-design\\' -and $_.CommandLine -match 'tsx|pino' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
Get-NetTCPConnection -LocalPort 3323 -State Listen -ErrorAction SilentlyContinue   # expect: nothing
git status --short                                                                 # expect: nothing
```
   If the seed writes photo files under `apps/api/.storage`, that folder is ignored by git; say so.
6. **Description:** `TASK\scripts\pr-body.md`: *Summary* (the problem and the goal); *Changes*; *Evidence*
   (each command and its result line; the test's red then green; the break; the real run's two states); *Out
   of scope*. No tool attribution. Do not write a PR number into any document.
7. **Push and the PR:**
```powershell
cd C:\dev\masaha\app-design
git push -u origin chore/demo-daily; "push exit $LASTEXITCODE"
gh pr create --assignee "@me" --label chore --label area:api --label area:docs --title "chore(seed): renew the demo's day each run" --body-file C:\dev\masaha\workspace\TASKS\DEMO_DAILY_BASEL\scripts\pr-body.md
gh pr view --json number,url --jq '.number, .url'
```
8. **CI:** `gh pr checks <n> --watch --interval 60` (stop waiting after 40 minutes: report "pending"); then
   `gh pr view <n> --json headRefOid,mergeStateStatus --jq '.headRefOid, .mergeStateStatus'` and `git rev-parse
   HEAD`: the same sha and `CLEAN`. A red check → read `gh run view <run id> --log-failed`, fix it in the
   commit (`git commit --fixup <sha>`, then `$env:GIT_SEQUENCE_EDITOR=':'; git rebase -i --autosquash
   origin/main; Remove-Item Env:GIT_SEQUENCE_EDITOR`), `git push --force-with-lease`; red twice → stop. Never
   merge.
9. **Conflicts:** for each other open PR (`gh pr list --state open --json number,headRefOid`): `git merge-tree
   --write-tree HEAD <its headRefOid>` → clean, or the conflicted paths (report them; do not fix).
10. `git switch --detach origin/main` — `app-design` left clean.

## Rules that stop you

A command you **cannot run** (an error before any test runs, the database unreachable, a missing module, a
timeout) → stop at once and report the command and its exact output. Never skip or delete a test, never change
a config, `.env`, a timeout or a lane to get past a failure, never call a failure "flaky". Never touch another
worker's database or worktree. If the goal proves wrong against the code (for example the set's lines are not
where this file says, or *present* already counts earlier days), stop and report. **Never claim a result you
did not see**: copy the line that says it. Write `TASK\4_REPORT.md` as you go.

## Your final reply — this shape

```
Status: PLAN READY | DONE | STOPPED
PR: #<n> <url> · head <sha> · CI <green/red/pending> · <CLEAN/not CLEAN>   (or "no PR")
Commits: <sha> <subject> (<chars>)
Test: <its red line, then its green line> · Break: <red, then green>
Ran and passed: <each command, with its result line>
Ran and failed: <each, and what you did>   (or "none")
Real run: full space <slug>: <state> · closed-today space <slug>: <state> · second seed run: <what changed>
Conflicts with open PRs: <each: clean / paths>
app-design left at origin/main and clean: <yes/no>
Stopped at (if STOPPED): <the step, the exact command and output>
Report: C:\dev\masaha\workspace\TASKS\DEMO_DAILY_BASEL\4_REPORT.md
```
