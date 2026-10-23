# Review — SUBSCRIPTIONS PR 3 (`feat/subscription-check-ins`, #109), one independent reviewer (Codex)

You are the **independent reviewer** of a pull request in the Masaha repository (GitHub
`Basel-Ghonaim/masaha`): worker B's SUBSCRIPTIONS PR 3 — subscribers checked in and out at a coworking space's
front desk, on the API. You did not write it; another agent did, in another session. **Trust nothing you have
not seen in the code.** This file is self-contained.

**The PR holds:** first, commits carried from #106's review (a subscribe retry with another customer's key
refused; `subscriptions.md`'s *Authority* line; the phone search keeping its suffix match; the debt warning
counting older items only; a check-in's minutes read from SQL; a contract date; the 49-debt decision line;
findings 124 and 125 recorded); then the plan's four commits: C1 *present* defined once (`occupancy`), C2 check
a subscriber in (with four warnings), C3 check a subscriber out, C4 list check-ins.

## Rules

- **Read only.** Work from `C:\dev\masaha\app-design`. Use git commit objects only: `git fetch origin` and `git
  fetch origin pull/109/head`; base = `origin/main`; `git diff origin/main...FETCH_HEAD`, `git show <commit>`,
  `git show <sha>:<path>`. **No** edits to the repository, no checkout or switch (another worker may hold a
  branch in that worktree), no installs, no npm or test runs, no servers, no database commands, no comments on
  GitHub. The only file you write is the report below.
- First: `gh pr checks 109` — if any check is red or pending, say so in the report and stop. At the end, `gh pr
  view 109 --json headRefOid` again: say whether the head moved while you reviewed.
- Report **concrete problems only**, each verified in the code: the file and line, the failing scenario
  (inputs → wrong result), the severity (**blocker / should-fix / nit**), and the fix. Mark "plausible" when
  you are not sure, with why. **Say what you saw in the code and what you only read in the executor's
  report.** No praise. No tool attribution anywhere.
- Think like: an attacker on every route (a reception account of another space, a guessed id, a reception
  account reaching an owner's action); two desks on a weak connection checking the same member in at once and
  retrying; an owner reading a member's usage a month later.

## What to read

1. The project's rules: `git show origin/main:CLAUDE.md`.
2. The approved plan: `C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\2_PLAN.md` — **only these parts:** the
   owner's approval note at its top (lines 1–39; it binds); §4 D11 (check-ins), D12 (*present* once), D14
   (idempotency, locks, order and races); §9 *PR 3* (the tests and the break each must catch); §11 *PR 3*
   (C1–C4); §13 (the owner's answers); Appendix A *PR 3* (the documents).
3. The carried items: `C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\0_CARRIED_FROM_106.md` (items 1–8, the
   owner's decisions) and, for each item's file and scenario, the findings it cites in
   `6_REVIEW_PR2_CLAUDE_CODE.md` (same folder).
4. The executor's prompt `3_EXEC_PROMPT_PR3.md` and report `4_REPORT_PR3.md` (same folder): judge **every
   departure** it lists, every test it says it saw only green, and every break.

## Look hardest at

- **Authorization:** each check-in route under the space-access check and `attendance.record`; nothing of
  another space reachable by id (a customer, a subscription, a check-in); reception never reaching an
  owner-only action.
- **Check-in rules (D11):** refused for a subscription that is not active today (Gaza's date), ended, expired,
  of an archived customer, or of another customer; a member already present refused
  (`MEMBER_ALREADY_CHECKED_IN`); the four warnings (days per week used, outside the subscription's hours,
  outside its shift, the space full) raised in the plan's order and **never blocking**; usage-based limits.
- **Races and retries (D14):** two check-ins of one member at the same time → one row, under the space's lock
  and a database constraint; a retry with the same idempotency key answers the same row; a key used for
  another subscription or customer refused (as carried item 1 now does for subscribe).
- **Check-out:** only an open check-in of this space; the minutes and the balance answered match what
  `subscription_usage` computes (one rule — carried item 5); a second check-out refused or idempotent as the
  plan says.
- ***Present* once (D12, C1):** the occupancy read, the warnings and the public directory all count present
  people through the same function; visits and subscription check-ins both counted; the live status unchanged
  for spaces with no subscribers.
- **The list of check-ins (C4):** paged, bounded dates, one space only, the plan's §4 exception for `open=true`.
- **The carried items:** each of 1–8 done as decided, each code fix with its test.
- **The documents:** the API contract (routes, warnings, codes), the data model, conventions, security,
  `occupancy.md`, `desk.md`, `subscriptions.md`, `payments.md`, `v1-mvp.md`, `overview.md`, findings 111, 124,
  125 and the findings index — true to the code, one home per fact, only what this PR built, `#109` where the
  number goes, no `#PRNUM` left.
- **Scope:** `apps/api`, `packages/shared`, `docs`, and at most the web's two error catalogues; **no
  migration** (the plan says none). Commit subjects ≤ 50 characters, each with a body.

## Your output

Write one file: `C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\6_REVIEW_PR3_CODEX.md` (if you cannot write
there, put the whole report in your reply instead). It holds:

1. The head you reviewed, CI's state, and whether the head moved.
2. **A one-line verdict:** mergeable / mergeable after a fix round / not mergeable.
3. **The five most important findings**, most severe first, then the rest. Each with **where its fix
   belongs** under the owner's rule: **a serious or large fix → a fix round on this PR; a small one → worker
   B's next PR's first commit (through `0_CARRIED_FROM_109.md`); or a finding to record.**
4. The executor's departures, each judged.
5. A short "Checked and fine" list.

Then stop.
