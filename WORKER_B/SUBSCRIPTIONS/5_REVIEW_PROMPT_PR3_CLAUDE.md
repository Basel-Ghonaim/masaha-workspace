# Review after the merge — SUBSCRIPTIONS PR 3 (#109), one independent reviewer (Claude Code)

You are the **independent reviewer** of a pull request in the Masaha repository (GitHub
`Basel-Ghonaim/masaha`): worker B's SUBSCRIPTIONS PR 3 — subscribers checked in and out at a coworking space's
front desk, on the API. It is **already merged** (merge commit `7dfe360c`, PR head `e262298e`) on one Codex
review that found nothing. The owner judged that review weak: this is a **second, deeper review of money- and
attendance-adjacent code**. You did not write it. **Trust nothing you have not seen in the code.** This file is
self-contained. This is not a Work Item: no project skills, no branch, plan, commit, PR or issue.

**The PR holds:** first, commits carried from #106's review (a subscribe retry with another customer's key
refused; `subscriptions.md`'s *Authority* line; the phone search keeping its suffix match; the debt warning
counting older items only; a check-in's minutes read from SQL; a contract date; the 49-debt decision line;
findings 124 and 125 recorded); then the plan's four commits: C1 *present* defined once (`occupancy`), C2 check
a subscriber in (with warnings), C3 check a subscriber out, C4 list check-ins.

## Rules

- **Read only.** Work from `C:\dev\masaha\app-design`. Git commit objects only: `git fetch origin`; the PR's
  range is `7dfe360c^1..e262298e` (`git log`, `git diff 7dfe360c^1 e262298e`, `git show <commit>`, `git show
  <sha>:<path>`). Read the code as it stands on `origin/main` too, to confirm a finding still holds there.
  **No** edits to the repository, no checkout or switch, no installs, no npm or test runs, no servers, no
  database commands, no comments on GitHub. No subagents. The only file you write is the report below.
- Report **concrete problems only**, each verified in the code: the file and line (on `origin/main`), the
  failing scenario (inputs → wrong result), the severity, and the fix. Mark "plausible" when you are not sure,
  with why. **Say what you saw in the code and what you only read in a report.** No praise. No tool
  attribution anywhere.
- **Severity, under the owner's rule for this merged PR:**
  - **critical** — wrong money or attendance data stored, an authorization hole (another space's data or an
    owner's action reachable), a race that breaks an invariant, data loss → **a fix branch opened at once**;
  - **small** — a real defect with no such effect, a missing test or break, a document wrong → **the first
    commit of the next Work Item touching the API**, through `0_CARRIED_FROM_109.md`;
  - **record** — a finding to record, no code change now.
- Think like: an attacker on every route (a reception account of another space, a guessed id, a reception
  account reaching an owner's action); two desks on a weak connection checking the same member in at once and
  retrying; a check-out across midnight Gaza time; an owner reading a member's usage and debts a month later.

## What to read

1. The project's rules: `git show origin/main:CLAUDE.md`.
2. The approved plan: `C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\2_PLAN.md` — **only these parts:** the
   owner's approval note at its top (lines 1–39; it binds); §4 D11 (check-ins), D12 (*present* once), D14
   (idempotency, locks, order and races); §9 *PR 3* (the tests and the break each must catch); §11 *PR 3*
   (C1–C4); §13 (the owner's answers); Appendix A *PR 3* (the documents).
3. The carried items: `0_CARRIED_FROM_106.md` (same folder; items 1–8, the owner's decisions) and, for each
   item's file and scenario, the findings it cites in `6_REVIEW_PR2_CLAUDE_CODE.md`.
4. The executor's report `4_REPORT_PR3.md` and the Codex review `6_REVIEW_PR3_CODEX.md` (same folder). Do not
   repeat Codex's "checked and fine" on trust: **re-check each of its claims in the code**, and say where it
   was wrong.

## Look hardest at

- **Authorization:** each check-in route under the space-access check and `attendance.record`; nothing of
  another space reachable by id (a customer, a subscription, a check-in, the idempotency key); reception never
  reaching an owner-only action; the list's boundary.
- **Check-in rules (D11):** refused for a subscription not usable today (Gaza's date), ended, of an archived
  customer, or of another customer; a member already present refused; the warnings raised in the plan's order
  and never blocking; days-per-week and hours-per-day counted correctly (week start, Gaza day, open check-ins).
- **Races and retries (D14):** two check-ins of one member at once → one row (lock and constraint); a retry
  with the same key answers the same row, including after a check-out; a key reused for another subscription
  or customer refused; lock order consistent with the other desk actions (no deadlock).
- **Check-out:** only an open check-in of this space; the minutes and any balance match `subscription_usage`
  (one rule); across midnight; a second check-out; a check-out of a visit's id.
- ***Present* once (D12, C1):** every count of present people goes through the one function; visits and
  check-ins both counted; nothing double-counted; the live status unchanged for spaces with no subscribers.
- **The list (C4):** paged, bounded dates, one space, the `open=true` exception; Gaza-day bounds at the edges.
- **The carried items 1–8:** each done as decided, each code fix with its test and a break that would fail it.
- **Tests:** a behaviour the plan's §9 names with no test, or a test that would pass with the bug.
- **The documents:** the API contract, data model, conventions, security, feature documents — true to the
  code, only what this PR built.

## Your output

Write one file: `C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\6_REVIEW_PR3_CLAUDE_CODE.md`. It holds:

1. The range reviewed and `origin/main`'s head at the start and the end.
2. **A one-line verdict:** no critical finding / critical findings — a fix branch needed.
3. **The findings**, most severe first, each tagged **critical / small / record** with where its fix belongs.
4. Where the Codex review was wrong or thin, each item in one line.
5. A short "Checked and fine" list.

Then stop.
