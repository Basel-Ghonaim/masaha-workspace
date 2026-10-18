# Review — the PR of OWNERSREAD (an independent reviewer)

You are the **independent reviewer** of the pull request from branch `feat/space-owners-read` in the Masaha
repository (Basel-Ghonaim/masaha). Write your report to `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\REVIEW_OWNERSREAD_<YOU>_REPORT.md`
(`<YOU>` = your tool's name in capitals).

## Rules
- Find the PR: `gh pr list --head feat/space-owners-read --json number,headRefOid`. Write its number and head at
  the top of your report; check at the end that the head has not moved.
- **Run from `C:\Users\basel\masaha-b` and read only commit objects:** `git fetch origin`; base =
  `git merge-base origin/main <head>`; use `git diff <base>...<head>` and `git show <head>:<file>`. No
  edits, checkouts, installs, npm or test runs, servers, database commands, no GitHub comments. **Do not
  run the tests:** CI ran every lane on this head.
- Report **concrete problems only**, each verified: file and line, the failing scenario, the severity
  (**blocker / should-fix / nit**), the fix. "Plausible" when unsure, with why. No praise. No tool
  attribution. **Do not use any project skill.**

## What the PR must be
The approved plan `C:\Users\basel\.prompt\MASAHA_WORKER_B\PLAN\OWNERSREAD_PLAN.md` (its contract, decisions, tests and their breaks, commits) and the
executor's report `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\OWNERSREAD_REPORT.md` (judge each departure). Scope: apps/api, packages/shared and docs; web files only if the plan declared them.

## Look at these, in this order
1. The levels: `spaces` (L1) never imports `space-links` (L2); the composition sits where conventions §9 puts it.
2. The owners: active owner links only, oldest first, names from `users`; none for an unverified space; read under the same share lock as the space's facts.
3. The contract and `@masaha/shared`: the new field or read documented; if `AdminSpace` changed, every web file touched is a fixture or type the plan declared.
4. Finding 59's status and resolution line true to what was built.
5. The tests: each would fail with its planned break; expectations by hand.
6. The documents true to the code, one home per fact.
7. The commits: count each subject's characters yourself (≤ 50).

## Your output
One file: a one-line verdict; the findings, most severe first; a short "Checked and fine" list; one line
judging the trial: did the plan leave the executor anything to guess? Then stop.
