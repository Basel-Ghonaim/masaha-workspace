# STAFF — execute the approved plan

You are the **executor** of one Work Item in the Masaha repository, in a fresh conversation. You did not
plan it and you will not review it. **The plan is approved; do not re-decide anything in it.** It is a
**security** item: the reset, Google sign-in, the forced change and the temporary password all change.

## 0. The precondition — the sync with #87 (do this before anything else)

```powershell
Set-Location C:\Users\basel\masaha-b
git fetch origin
gh pr view 87 --json state,mergedAt,mergeCommit
```

- **#87 not `MERGED` → stop at once** and reply `Status: STOPPED — #87 not merged`. Do not branch, do not
  read further, do not wait in a loop.
- **#87 merged →** the folder must be clean (`git status --short` empty). If it still sits on
  `feat/space-packages`, move it off: `git switch --detach origin/main` (the branch was merged; do not delete
  anything — the analyst cleans branches). Then `git log --oneline -3 origin/main` must show #87's merge.
- **Sync the plan with the merged tree:** `git diff --name-status 5e8c979d origin/main`, and re-read on
  `origin/main` every file the plan names that #87 touched (`apps/api/src/app.ts`, `docs/api/api-contract.md`,
  `docs/backend/security.md`, `docs/backend/conventions.md`, `docs/architecture/findings/README.md`,
  `packages/shared/package.json` and its indexes). A code file that now reads differently from what the
  plan assumes → stop and ask; documents only → edit beside #87's lines.
- `npm run build -w @masaha/shared` (its `dist` must hold #87's `packages`), then
  `npx prisma migrate deploy` is **not** needed for #87 (no schema) — but confirm `masaha_b_dev` and
  `masaha_b_test` are on the latest migration before yours (`npm run db:migrate` reports nothing pending).

## 1. Then follow the plan

1. Read `CLAUDE.md`, then the plan **whole**: `D:\masahaWorkspace\WORKER_B\STAFF\2_PLAN.md` — **the owner's
   approval at its top binds** (7 days; one PR; the new code's words; the Google refusal; 422; the row's
   shape; the three extra closures).
2. §12 step by step: the branch `feat/space-staff` from the latest `origin/main`; `docker start
   masaha-postgres-1` (never `db:up`, never `npm ci`); **§12.2's first checks before any code** (the test
   helper's expiry, the documentation rule for findings 85–86, every check the plan lists); the seven
   commits in order, each test red first, **each security property's deliberate break run and recorded**;
   the migration (below); §12's verification, real run on 3321, `#PRNUM`, push, PR, CI, `CLEAN`, the
   conflict check against any open PR (worker A's OWNERS: a documents-only conflict takes the fast path).
3. **The migration:** `npx prisma migrate dev --create-only --name <the plan's name>` **once** (a second run
   applies it to `masaha_b_dev`); then check the folder; edit the SQL exactly as the plan writes it (the
   backfill of pending accounts **before** the `CHECK`); then `npm run db:migrate` for `masaha_b_dev` and the
   test database as the plan's procedure says; the client regenerated. If Prisma refuses for data loss, use
   `migrate diff --script` as the plan says — never `--force` or a reset of a database you were not told to
   reset.
4. Do not use the project's skills unless you are Claude Code (then only as the plan's appendix maps them;
   the plan wins). Write nothing outside the repository except this folder's `4_REPORT_PR1.md`.

## 2. A test you cannot run stops the work

A test **failing** because its code is not written yet is the plan's red step — normal. A test, lane,
break or real-run step you **cannot run** is not: it errors before any test runs (database unreachable,
Docker down, a port taken, a module or `dist` missing, a migration pending or failing, `No test files
found`, a Vitest or TypeScript startup error, the whole run timing out, a crash with no result). **Then stop
at once** — never skip, `.skip` or delete a test, never change a config, a timeout, `.env`, a script or a
lane, never mock what the plan does not, never run a narrower command and call it the lane, never call it
"flaky". **A plan that proves false against the code:** stop, say exactly what, offer the fix — do not choose
it. **A security break that stays green: stop.** Write the command, its exact error and where you were into
the report; reply with §5's shape, `Status: STOPPED`.

**Never claim a result you did not see:** a command passed only if you saw its own output say so; copy that
line.

## 3. Limits, and not losing work

- Write `4_REPORT_PR1.md` **as you go**: after §0's sync, after the first checks, after each commit (sha,
  subject and length, the red line before the code, the green line after), after each break, the migration,
  the real run, the push.
- **One full test run at a time on this machine:** before each full lane, check that no `vitest` runs under
  `C:\Users\basel\masaha\` (worker A); if one does, wait. Focused runs of one or two files are fine.
- Each full lane **once, on the head**; re-run only if a file it covers changed after it passed.

## 4. Discipline

Stage by path (never `-A` or `.`); each commit message written to a UTF-8 file **without a BOM and with LF line
endings (no CR — #87's messages carried CRLF)**, with **a body of one or two lines saying why**, then `git commit -F <file>`; subjects counted ≤ 50; **no tool
attribution**; a fix before the push folds into its commit (`--fixup` + autosquash); never print a secret,
`apps/api/.env`, a password or a temporary password (in the report write `<redacted>`); never merge, create
an Issue, or comment on another PR; stop the API by its process id; port 3321 free at the end.

## 5. Your final reply — this shape, finished or stopped

```
Status: DONE | STOPPED
Sync with #87: <merged at <sha> / not merged>; files re-read; <any difference from the plan>
PR: #<n> <url> · head <sha> · CI <green/red/pending> · <CLEAN/not CLEAN>   (or "no PR")
Commits: <sha> <subject> (<chars>) — one line each
Migration: <name> · backfill before CHECK <yes/no> · applied to masaha_b_dev <yes/no> · test DB <yes/no>
Ran and passed: <each command, with the result line you saw>
Ran and failed: <each, what failed, what you did>   (or "none")
COULD NOT RUN: <each test, lane, break or real-run step not run, the exact command, the exact error,
               why>   (or "none" — only if every planned run happened)
Security breaks: <each property: red seen / NOT RUN (why)>
First checks: <each: result>
Real run: <each status, or NOT RUN (why)>
Departures from the plan: <each, with its reason>   (or "none")
Stopped at (if STOPPED): <the step, and what the owner must decide or fix>
Report: D:\masahaWorkspace\WORKER_B\STAFF\4_REPORT_PR1.md
```
