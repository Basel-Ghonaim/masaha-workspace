# PACKAGES — execute the approved plan (OpenCode)

You are the **executor** of one Work Item in the Masaha repository, in a fresh conversation. You did not
plan it and you will not review it. **The plan is approved; do not re-decide anything in it.**

## 1. Read, then begin

1. Work in `C:\Users\basel\masaha-b` only — never in `C:\Users\basel\masaha` (worker A) or a design
   worktree. Read `CLAUDE.md` at the repository's root.
2. Read the plan **whole**: `D:\masahaWorkspace\WORKER_B\PACKAGES\2_PLAN.md` — **the owner's approval at
   its top binds** (S1: a taken name is **409**; S2, S3; `data-model.md` is not edited).
3. Follow its §12 step by step: §12.1 (the folder, `origin/main`, the branch `feat/space-packages`,
   `docker start masaha-postgres-1` — never `db:up`, never `npm ci`), **§12.2's first checks**, the four
   commits in order (each test red first, then the code), §12.4, §12.5's thirteen breaks, §12.6's real run
   on 3321, §12.7's PR number, push and PR, §12.8's CI, `CLEAN`, the conflict check.
4. **Do not use the project's skills** (`.claude/skills/`); the plan is enough. If OpenCode asks to write
   to `D:\masahaWorkspace\WORKER_B\PACKAGES\`, that folder is allowed; nothing else outside the repository.

## 2. The rule that matters most: a test you cannot run stops the work

A test **failing** because the code is not written yet is the plan's red step — normal. A test or command
you **cannot run** is not. It is any of:

- the command errors before any test runs: the database is unreachable (`ECONNREFUSED`, `P1001`),
  Docker is not running, a port is taken, a module or `dist` is missing, a migration is pending, an
  environment variable is absent, `No test files found`, a Vitest/TypeScript startup error, a timeout of
  the whole run, a crash with no test result;
- a break of §12.5 that you could not make or could not run;
- a step of §12.6's real run that you could not perform.

**When that happens: stop at once.** Do not work around it — never skip, `.skip` or delete a test, never
change a config, a timeout, `.env`, a script or a lane, never mock or stub what the plan does not, never
run a narrower command and call it the lane, never mark it "flaky" and move on. Write the exact command,
its exact error (the first lines that say why) and what you were about to do into `4_REPORT.md`, then
reply with §5's final reply, `Status: STOPPED`. The owner fixes the environment; you resume from there.

**Never claim a result you did not see.** A command counts as passed only when you saw its own output
say so (e.g. `Test Files  12 passed (12)`); copy that line. No "should pass", no "all tests pass" as a
summary.

## 3. Your limits, and how not to lose work

- Your model may hit a rate or daily limit mid-item. So **write `4_REPORT.md` as you go**, not at the end:
  create it after §12.1, and append after **each** first check, **each** commit (its sha, subject, the red
  line seen before the code, the green line after), **each** break, the real run and the push. If you stop
  for any reason, the report must already say exactly where the work stands.
- **One full test run at a time on this machine:** before each full lane, §12.1's process check; if a
  `vitest` runs under `C:\Users\basel\masaha\`, wait for it to end. Focused runs of one or two files are fine.
- **Run each full lane once, on the head** (§12.4). Re-run a lane only if a file it covers changed after it
  passed. Do not re-run what already passed.

## 4. The rest of the discipline

- Stage **by path** (`git add <paths>`; never `-A` or `.`). Write each commit message to a UTF-8 file and
  `git commit -F <file>` — real line breaks, no literal `\n`, no escaped characters. Count each subject
  (≤ 50). **No tool attribution** anywhere (no `Co-Authored-By`, no "generated with"). A fix before the push
  folds into its commit (§12.3). Never amend or rewrite a pushed commit unless §12.7 says so.
- Never print a secret: never print `apps/api/.env` or a password; check the variable names only.
- **§14 "Stop and ask" binds**, as does every "stop and ask" in §12.2 and §12.5 — a break that stays green
  is a stop, not a note.
- Never merge, never create an Issue, never comment on a PR other than this item's.
- Stop the API by its process id at the end; check port 3321 answers nothing.

## 5. Your final reply — exactly this shape, whether finished or stopped

```
Status: DONE | STOPPED
PR: #<n> <url> · head <sha> · CI <green / red / pending> · <CLEAN / not CLEAN>   (or "no PR")
Commits: <sha> <subject> (<chars>) — one line each
Ran and passed: <each command, with the result line you saw>
Ran and failed: <each, what failed, what you did>   (or "none")
COULD NOT RUN: <each test, lane, break or real-run step you did not run, the exact command, the exact
               error, and why>   (or "none" — say "none" only if every planned run happened)
Breaks B1–B13: <each: red seen / NOT RUN (why)>
First checks 1–5: <each: result>
Real run (§12.6): <each status, or NOT RUN (why)>
Departures from the plan: <each, with its reason>   (or "none")
Stopped at (if STOPPED): <the step, and what the owner must fix before you resume>
Report: D:\masahaWorkspace\WORKER_B\PACKAGES\4_REPORT.md
```

When the PR is green and `CLEAN` and the report is complete, give that reply and stop.
