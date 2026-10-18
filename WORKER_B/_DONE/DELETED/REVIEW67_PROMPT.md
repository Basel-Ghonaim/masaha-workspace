# Review — PR #67 (DELETED: the deleted spaces in the admin's list, one table of error statuses, the parallel-work rule)

You are an **independent reviewer** of PR #67 in the Masaha repository (Basel-Ghonaim/masaha).
Write your report to `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\REVIEW67_<YOU>_REPORT.md`, where
`<YOU>` is your tool's name in capitals (`OPENCODE`, `CODEX`, `COPILOT`, `CLAUDE`).

## Rules

- **Run from `C:\Users\basel\masaha`**, but **read only commit objects** (that folder's working tree
  is on another PR's branch). No edits, commits, checkouts, switches, installs, npm or test runs,
  database or Docker commands, no GitHub comments. `git fetch origin`, then pin to **the PR's current
  head** (`gh pr view 67 --json headRefOid`, written at the top of your report, checked again at the
  end). Base: `git merge-base origin/main <head>`. Use `git diff <base>...<head> -- <paths>` and
  `git show <head>:<file>`.
- **Report concrete problems only,** each verified in the code: file and line, the failing scenario,
  the severity (**blocker / should-fix / nit**) and the fix. No praise, no summary. If unsure, say
  "plausible" and why.
- **No tool attribution** in what you write.

## What the PR must be (the owner's decisions)

API, the web's minimal follow-up, and documents; no schema change, no dependency. The approved plan is
`C:\Users\basel\.prompt\MASAHA_WORKER_B\PLAN\DELETED_PLAN.md` with its reply
`PROMPT\DELETED_PLAN_REPLY.md`; the worker's report is `REPORT\DELETED_REPORT.md`.
- **The parallel-work rule (commit 1, alone):** workflow §9 replaces "one layer each / never in the
  same layer" with four conditions (one schema change in flight; one dependency; no two open items
  edit the same code file — shared documents and append-only lists allowed, fast path; every item
  running the API has its own databases and ports). **The owner's condition: the rule lives in §9
  only;** every other document or skill links it without restating it.
- **Finding 24:** `ERROR_STATUSES` and its reverse lookup in `@masaha/shared/core`; the API's error
  type statuses and the web's normaliser read them; the API's statuses unchanged.
- **The row's state as facts:** `AdminSpaceRow` carries `isVerified`, `isHidden` and `deletedAt`
  (string or `null`) instead of one `state`; `SPACE_STATES` → `SPACE_STATUSES`.
- **`GET /admin/spaces?status=deleted`:** only soft-deleted spaces, hidden or not, verified or not,
  with search, place, stale, order and paging applied before the page is cut; every other status, and
  none, still leaves them out; a deleted row names its owners (the narrowing of "a link to a deleted
  space counts for nothing" recorded in `space-links.md`).
- **The web shows nothing new:** the admin's list keeps its three statuses (its own list), the same
  badges (hidden first), and `?status=deleted` in the address reads as "all". The owner granted three
  fixture lines of `pages/dashboard/routes.component.test.tsx`; the worker used four (the fourth a
  direct consequence of `deletedAt` being required) — judge it.
- Findings 44 and 50 stay open (a screen resolves them).

## Look at these, in this order

1. **The listing:** `deleted` filtered before paging (the total and every page right); no other
   status leaks a deleted space; the composed read stays one query per module; `deletedAt`'s
   serialisation; the owners named on a deleted row and `isVerified` following them.
2. **The rule's single home:** `grep` the documents and skills for any other statement of the four
   conditions or of the old layer rule.
3. **Finding 24:** every status in the table matches the contract §3; the reverse lookup's unknown
   statuses; nothing else in the API or the web still holds its own copy.
4. **The web:** nothing visible changed; every consumer of the old `state` updated; the address rule
   cannot request deleted spaces; the menu reads `isHidden`.
5. **The tests:** each would fail if its code broke; the paging test really interleaves deleted and
   live spaces; expectations by hand; the web's tests retitled truly.
6. **The documents:** workflow §9, the plan's *Ordering notes*, the `write-plan` skill, the contract
   (§3 line, `GET /admin/spaces`, `DELETE`), `space-links.md`, `spaces.md`, finding 24 and the index,
   the overview — each true, one home per fact.
7. **The commits:** four; count each subject (≤ 50).

## Your output

One file (the path above): a one-line verdict; the findings, most severe first (severity, file:line,
scenario, fix); a short "Checked and fine" list; then stop.
