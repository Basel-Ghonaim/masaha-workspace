# Review — the PR of ADMINLIST (an independent reviewer)

You are the **independent reviewer** of the pull request from branch `feat/admin-deleted-spaces` in the Masaha
repository (Basel-Ghonaim/masaha). Write your report to `C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\REVIEW_ADMINLIST_<YOU>_REPORT.md`
(`<YOU>` = your tool's name in capitals).

## Rules
- Find the PR: `gh pr list --head feat/admin-deleted-spaces --json number,headRefOid`. Write its number and head at
  the top of your report; check at the end that the head has not moved.
- **Run from `C:\Users\basel\masaha` and read only commit objects:** `git fetch origin`; base =
  `git merge-base origin/main <head>`; use `git diff <base>...<head>` and `git show <head>:<file>`. No
  edits, checkouts, installs, npm or test runs, servers, database commands, no GitHub comments. **Do not
  run the tests:** CI ran every lane on this head.
- Report **concrete problems only**, each verified: file and line, the failing scenario, the severity
  (**blocker / should-fix / nit**), the fix. "Plausible" when unsure, with why. No praise. No tool
  attribution. **Do not use any project skill.**

## What the PR must be
The approved plan `C:\Users\basel\.prompt\MASAHA_WORKER_A\PLAN\ADMINLIST_PLAN.md` (its contract, decisions, tests and their breaks, commits) and the
executor's report `C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\ADMINLIST_REPORT.md` (judge each departure). Scope: apps/web and docs only; nothing in apps/api or packages/shared.

## Look at these, in this order
1. The deleted list: `GET /admin/spaces?status=deleted` read as the contract says; rows muted, dated on Gaza's calendar, owners named; «استرجاع» their only action; after a restore the list fetched again and a toast names the space.
2. A3: the verification badge always, «مخفية» beside it; A7's «بيانات قديمة فقط» chip; A8's «ناقصة» as warning.
3. The address rules (`?status=deleted` now valid), the 429 hold, the focus when a restored row leaves the list.
4. Findings 44 and 50 resolved truthfully in their files and the index.
5. The tests: each would fail with its planned break; expectations by hand.
6. The documents true to the code, one home per fact.
7. The commits: count each subject's characters yourself (≤ 50).

## Your output
One file: a one-line verdict; the findings, most severe first; a short "Checked and fine" list; one line
judging the trial: did the plan leave the executor anything to guess? Then stop.
