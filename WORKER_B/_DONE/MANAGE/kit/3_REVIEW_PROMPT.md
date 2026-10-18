# Review — the PR of MANAGE (an independent reviewer)

You are the **independent reviewer** of the pull request from branch `feat/owner-space-api` in the Masaha repository
(Basel-Ghonaim/masaha). Write your report to `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\REVIEW_MANAGE_<YOU>_REPORT.md`
(`<YOU>` = your tool's name in capitals).

## Rules
- Find the PR: `gh pr list --head feat/owner-space-api --json number,headRefOid`. Write its number and head at the top
  of your report; check at the end that the head has not moved.
- **Run from `C:\Users\basel\masaha-b` and read only commit objects:** `git fetch origin`; base =
  `git merge-base origin/main <head>`; use `git diff <base>...<head>` and `git show <head>:<file>`. No
  edits, checkouts, installs, npm or test runs, servers, database commands, no GitHub comments. **Do not
  run the tests:** CI ran every lane on this head.
- Report **concrete problems only**, each verified: file and line, the failing scenario, the severity
  (**blocker / should-fix / nit**), the fix. "Plausible" when unsure, with why. No praise. No tool
  attribution. **Do not use any project skill.**

## What the PR must be
The approved plan `C:\Users\basel\.prompt\MASAHA_WORKER_B\PLAN\MANAGE_PLAN.md` (its approval note, contract, decisions, tests and their breaks, commits)
and the executor's report `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\MANAGE_REPORT.md` (judge each departure). Scope: apps/api, packages/shared and docs; no web file unless the plan declared it.

## Look at these, in this order
1. Authorization end to end: `requireSpaceAccess` mounted once on `/manage/spaces/:spaceId`; no link gives 404; reception reads, only the owner writes (`can()`), decided again under the space's lock; the admin not admitted on `/manage` (ADR 0009); a deleted space 404, a hidden one editable by its owner.
2. One implementation: the `/manage` routers call the same services as `/admin`, no copied rule; photos on #77's service with its limit and lock.
3. Every authorization property's test made to fail by its break (testing §3 rule 7): owner, reception, stranger, admin, for each kind of route.
4. The contract's *Managed spaces* rows and security.md true to the code; the audit's actor.
5. The tests: each would fail with its planned break; expectations by hand.
6. The documents true to the code, one home per fact.
7. The commits: count each subject's characters yourself (≤ 50).

## Your output
One file: a one-line verdict; the findings, most severe first; a short "Checked and fine" list; one line
judging the trial: did the plan leave the executor anything to guess? Then stop.
