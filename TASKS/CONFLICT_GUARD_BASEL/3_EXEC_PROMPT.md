# CONFLICT_GUARD — a CI check against merge-conflict markers, and two small document fixes

You are a worker on the Masaha repository, in a fresh session. This file is self-contained: every file to read
and every command is named. **Two phases:** first you write a short plan and **stop**; the owner reads it and
writes "approved" (or changes) at its top; then you build, test, push and open one pull request. Run commands
**in PowerShell**; read each exit code with `$LASTEXITCODE` right after the command (passed only if 0).

- **Your worktree:** `C:\dev\masaha\app-design` (the design worker's; prepared on `origin/main`, dependencies
  installed, shared built). Work only there. Never touch `C:\dev\masaha\app` or `app-b` (workers A and B use
  them). **When you finish** (the PR open and green, or stopped), leave `app-design` detached at `origin/main`
  and clean: `git switch --detach origin/main` — reviewers read there. This is the first of two tasks for this
  worktree; the second (`TASKS\DEMO_DAILY_BASEL`) starts after this PR is open.
- **Your folder:** `C:\dev\masaha\workspace\TASKS\CONFLICT_GUARD_BASEL\` (below: `TASK\`). Outside the worktree
  write only there: `2_PLAN.md`, `4_REPORT.md`, `scripts\`.
- No database, no server, no browser is needed.

## The goal (the owner's, 2026-10-22)

1. **`docs/design/INDEX.md` line 868** holds a stray `<<<<<<< HEAD` line left by an old merge (before
   `## 54 · Batch 4 — the account`). Remove that one line; check nothing else of a conflict is left there.
2. **A new check, `npm run check:conflicts`**, that fails when any file tracked by git holds a merge-conflict
   marker: a line starting with `<<<<<<< ` or `>>>>>>> `, or a line that is exactly `=======` **between** such
   markers. It must **not** flag a Markdown setext heading underline (`=======` under a title, with no
   `<<<<<<<` before it) nor these strings inside a code example that is not at the start of a line. It reads
   the file list from `git ls-files`, skips binary files (images, fonts, `.ico`, `.pdf`), and prints each hit as
   `<file>:<line>` with the marker, then a one-line total. Model it on the existing links check:
   `apps/api/scripts/checkLinks.ts` (run by `node scripts/checkLinks.ts`, script `check:links` in
   `apps/api/package.json`, root script `check:links` in `package.json`) and its test
   `apps/api/scripts/checkLinks.unit.test.ts` — same place, same style, same kind of unit test (the pure
   function that finds markers in a text tested on cases: a real conflict, a setext heading, a marker in the
   middle of a line, a clean file).
3. **Wire it:** the root `package.json` script `check:conflicts`; the `matrix.task` list in
   `.github/workflows/ci.yml` gains `'check:conflicts'`; `docs/development/setup.md` — its commands table (a
   row beside `check:links`, line ≈ 60) and its CI sentence (line ≈ 178); `CLAUDE.md`'s *Commands* list (one
   line beside `check:links`).
4. **Issue #71** (`gh issue view 71`): reword the "merge apart" rule in `docs/development/workflow.md` §9 as
   the issue's *Goal* says — a merge that deletes or renames no file **the PR refers to**, and changes none of
   the PR's files, needs no rebase and no new CI run. Only that sentence; nothing else in the file.

Out of scope: any other file, any refactor, any other check. Do not write a PR number into any document.

## What to read

1. `C:\dev\masaha\app-design\CLAUDE.md` — the project's rules (they bind you): task scope, atomic Conventional
   Commits, **no tool attribution anywhere** (no `Co-Authored-By`, no "generated with", no tool name), stage by
   path, decisions are the owner's.
2. The files named in *The goal*, and `docs/architecture/documentation.md` §8 if you need the links rule.

## Phase 1 — the plan, then stop

Write `TASK\2_PLAN.md` (one page): the commits (subjects ≤ 50 characters, counted), the files each touches, the
marker-finding rule and its unit-test cases, the exact new lines for `setup.md`, `CLAUDE.md` and the CI file,
and the new sentence for `workflow.md` §9 next to the old one. Then **stop** and reply only: `PLAN READY:
TASK\2_PLAN.md`. Do not edit the repository before the owner's approval note is at the plan's top.

## Phase 2 — after the owner's approval

1. Preconditions: `cd C:\dev\masaha\app-design; git fetch origin; git status --short` (nothing); `git
   rev-parse --short HEAD` equals `git rev-parse --short origin/main` (if `main` moved, `git switch --detach
   origin/main` first). Then `git switch --no-track -c chore/conflict-guard origin/main`.
2. **Commits, in this order** (each: `npm run lint` and `npm run typecheck`, exit 0, before committing):
   1. `fix(docs): drop a stray conflict marker` — the `INDEX.md` line.
   2. `chore(ci): fail on merge-conflict markers` — the script, its unit test, the scripts, the CI matrix,
      `setup.md`, `CLAUDE.md`. **Test first:** write the unit test, run `npm run test:unit -w @masaha/api --
      scripts/checkConflicts.unit.test.ts`, see it fail (the module missing), copy the line; then the script;
      run it again, see it pass. Then run `npm run check:conflicts` on the tree: exit 0. Then **the break:** add
      a `<<<<<<< HEAD` line to `docs/design/INDEX.md` without committing (the check reads tracked files), run `npm run
      check:conflicts`, see it fail with that file and line, then `git restore docs/design/INDEX.md` and run
      it again: exit 0. Record both outputs.
   3. `docs(workflow): say what a merge apart guards` — the §9 sentence.
   Each commit message: a file `TASK\scripts\msg-<n>.txt` written with your editor — UTF-8 **without BOM**, LF
   line endings: the subject, a blank line, a body of 2–5 lines saying **why**. `git add <path> …` (never `-A`
   or `.`), then `git commit -F <file>`.
3. **On the head, once each:** `npm run test:unit -w @masaha/api`; `npm run check:conflicts`; `npm run
   check:links`; `npm run format:check`; `npm run lint`; `npm run typecheck`. Each exit 0; copy each result line
   into the report. Before a test run, if `Get-CimInstance Win32_Process -Filter "Name='node.exe'" |
   Where-Object { $_.CommandLine -match 'vitest' }` lists anything, wait until it is empty (check every 2 min,
   at most 30 min); never stop it.
4. **Description:** `TASK\scripts\pr-body.md` with: *Summary* (the four goals); *Changes* (per commit);
   *Evidence* (each command and its result line; the unit test's red then green; the break's failing output
   and the clean run); a line `Closes #71`. No tool attribution.
5. **Push and the PR:**
```powershell
cd C:\dev\masaha\app-design
git push -u origin chore/conflict-guard; "push exit $LASTEXITCODE"
gh pr create --assignee "@me" --label chore --label area:ci --label area:docs --title "chore(ci): fail on merge-conflict markers" --body-file C:\dev\masaha\workspace\TASKS\CONFLICT_GUARD_BASEL\scripts\pr-body.md
gh pr view --json number,url --jq '.number, .url'
```
6. **CI:** `gh pr checks <n> --watch --interval 60` (stop waiting after 30 minutes: report "pending"). The new
   `check:conflicts` check must appear and pass. Then `gh pr view <n> --json headRefOid,mergeStateStatus --jq
   '.headRefOid, .mergeStateStatus'` and `git rev-parse HEAD`: the same sha and `CLEAN`. A red check → read
   `gh run view <run id> --log-failed`, fix it in the right commit (`git commit --fixup <sha>`, then
   `$env:GIT_SEQUENCE_EDITOR=':'; git rebase -i --autosquash origin/main; Remove-Item Env:GIT_SEQUENCE_EDITOR`),
   `git push --force-with-lease`; red twice → stop. Never merge.
7. **Conflicts:** for each other open PR (`gh pr list --state open --json number,headRefOid`): `git merge-tree
   --write-tree HEAD <its headRefOid>` → clean, or the conflicted paths (report them; do not fix).

## Rules that stop you

A command you **cannot run** (an error before any test runs, a missing module, a timeout) → stop at once and
report the command and its exact output. Never skip or delete a test, never change a config, a lint rule, a
timeout or another check to get past a failure, never call a failure "flaky". If the goal proves wrong against
the code (for example the marker is not on line 868, or `workflow.md` §9 has no "merge apart" sentence), stop
and report. **Never claim a result you did not see**: copy the line that says it. Write `TASK\4_REPORT.md` as
you go (after the plan's approval, each commit with its sha and subject length, the test's red and green, the
break, the head's checks, the push, CI).

## Your final reply — this shape

```
Status: PLAN READY | DONE | STOPPED
PR: #<n> <url> · head <sha> · CI <green/red/pending> · <CLEAN/not CLEAN>   (or "no PR")
Commits: <sha> <subject> (<chars>) — one line each
Ran and passed: <each command, with its result line>
Ran and failed: <each, and what you did>   (or "none")
Break: <the failing output of check:conflicts with the marker, then the clean run>
Conflicts with open PRs: <each: clean / paths>
Stopped at (if STOPPED): <the step, the exact command and output>
Report: C:\dev\masaha\workspace\TASKS\CONFLICT_GUARD_BASEL\4_REPORT.md
```
