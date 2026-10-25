# Carried from #106 (SUBSCRIPTIONS PR 2, `feat/subscriptions`) into SUBSCRIPTIONS PR 3 (`feat/subscription-check-ins`)

**The owner's review rule:** a serious or large review fix reopens its PR; small ones are deferred to the
**next PR as dedicated commits at its start**, named in that PR's description ("Carried from #106"). #106's
review (`C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\6_REVIEW_PR2_CLAUDE_CODE.md`, head `d0acc06b`) found
no blocker and asked for no fix round. These are **PR 3's first commit(s)**, before the plan's PR 3 commits,
each code fix with its own test seen red before the fix and green after, recorded in `4_REPORT_PR3.md`. Read
the review for each item's file, line and scenario.

Suggested subjects (recount, ≤ 50): `fix(desk): refuse a key that subscribed another` (item 1);
`fix(customers): keep the phone's suffix match` (item 3); `fix(desk): warn only on older debts` (item 4);
`fix(desk): read a check-in's minutes in SQL` (item 5); `docs(subscriptions): …` (items 2, 6, 7 and the
findings).

**Decided by the owner (2026-10-22), as the supervisor recommended:**

1. **A subscribe retry with another customer's key is refused** (review 1): when `findByKey` finds a
   subscription whose `customerId` is not the path's, answer 409 as the payment routes do (`desk.service.ts`
   :319, :416, :516) — the same code and message style they use; one test (red first) and one line in the
   contract's errors for `POST …/customers/:customerId/subscriptions`.
2. **`subscriptions.md`'s *Authority* line** (review 2): it names the module's own routes (the corrections and
   the end) and the desk's (subscribe, the statement); no web screen yet.
3. **The phone search keeps its suffix match** (review 3): when a whole number is read, match the exact
   E.164 **or** the suffix on the digits (the national digits with the trunk 0), so `+970521234567` is found by
   `0521234567`; U3 and T22 gain that case.
4. **`CUSTOMER_HAS_DEBT` counts only older items** (review 6): on a retry, an item created after the
   subscription (its own unpaid renewal) does not raise the warning; compare by the order `itemBalances`
   allocates in; a test of the retry after a renewal.
5. **A check-in's minutes from SQL** (review 7): the statement's `checkIns[].minutes` comes from the same
   expression as `subscription_usage` (one rule, S1), not from TypeScript; the test that the sum of the
   check-ins' minutes equals `progress.minutesUsed`.
6. **The archived file's date** (review 9): the contract's *Customers (managed)* line dates the owner's
   decision **2026-10-21** (the PR stays #106).
7. **The 49-debt cap as a decision line** (review 8): `payments.md`'s allocation decision says that past the
   49th debt the rest goes to the new subscription (credit on a usage-based one, refused on a fixed one), and
   why the cap is acceptable.
8. **Findings to record** (this item's block; on `main` after #106: 120–123 → **124** and on, in order):
   **124** the statement's sums and its listed payments come from different snapshots (review 4; the
   customer's file has the same shape; the fix it names: one `REPEATABLE READ` transaction; to decide with the
   statement's screen item); **125** the allocation's order is not exposed to the client (review 5; the
   subscriber desk's screen wants a preview: `createdAt` in the answer, or a quote). Each a file and an index
   line.

**Done by the supervisor, not carried:** review 10 (the PR description's checklist line) is corrected in #106's
description before the merge.

Every item is done in PR 3; one you would leave, or one that proves larger than this file says → **stop and
ask**, never silently.
