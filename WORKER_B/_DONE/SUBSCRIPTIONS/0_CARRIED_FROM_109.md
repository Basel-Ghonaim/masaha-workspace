# Carried from #109 (SUBSCRIPTIONS PR 3, `feat/subscription-check-ins`, merged at `7dfe360c`) into the fix PR `fix/subscriber-checkout-due`

**The owner's rule for this merged PR (2026-10-24):** a critical finding opens a fix branch at once; small ones
go to the first Work Item that touches the API. The second review
(`C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\6_REVIEW_PR3_CLAUDE_CODE.md`, range `7dfe360c^1..e262298e`)
found **one critical finding** (its 1); the supervisor confirmed it in the code on `origin/main` `dec7bd37`.
The fix PR is that first API Work Item, so the small items ride on it too. Read the review for each item's
file, line and scenario.

Suggested subjects (recount, ≤ 50): `fix(desk): close a subscriber's stay at its due` (item 1);
`fix(subscriptions): answer a duplicate check-in` (item 2); `docs(api): say which desk writes send a key`
(item 3); `docs(findings): record #109's review` (item 4).

1. **Critical — a subscriber's check-out stops at the stay's due time** (review 1). `checkOutSubscriber`
   (`desk.service.ts` ≈ 476–501) closes at `now()`; the visit's check-out caps at its due time
   (`visits.stayEndAt`, `desk.service.ts:545`), and `docs/architecture/data-model.md` *Auto check-out* says no
   path charges a stay into the next day (#102). Close the check-in at `min(now, due)`, the due computed by
   `spaces.autoCheckoutDue` from the space's week and settings read **under the space's lock** — the same
   rule the check-ins' auto check-out already uses (`subscriptions.service.ts` ≈ 580); one rule, no second
   copy (share a helper if the two would otherwise repeat it). Keep the request's time in the audit as the
   visit does (`requestedAt`). **Tests (red first):** an open `PER_HOUR` check-in from yesterday 20:00, closing
   at 22:00, checked out at 09:00 today → `checkedOutAt` = 22:00, minutes 120, `balanceAgorot` up to 22:00
   only; the same with `maxStayMinutes`; a check-out before its due → `now` unchanged. **Break:** `at` passed
   back in → red. **Documents:** the contract's subscriber check-out line ("closed now") gains the due-time
   clause as the visit's has; `docs/features/desk.md` a decision line (2026-10-24, the PR's number).
   **Not in scope:** correcting check-ins already stored past their due — the supervisor checks the demo and
   dev data separately; if the executor sees a production-shaped need, stop and ask.
2. **Small — the open-check-in index answers its code, not a 500** (review 2): in `createCheckIn`
   (`subscriptions.repository.ts` ≈ 402–410) map the unique violation of `check_ins_customer_id_key` to
   `AppError.conflict('MEMBER_ALREADY_CHECKED_IN')`, the pattern `create` uses for its foreign key. A unit or
   API test that forces the violation (red first).
3. **Small — the contract's *Front desk* introduction** (review 3): `api-contract.md` ≈ 508 says every
   check-out sends a key; the subscriber's check-out sends none (≈ 577). One line: the check-ins, a visit's
   check-out and the payment send `Idempotency-Key`.
4. **Findings to record** (SUBSCRIPTIONS' block; on `main` 120–125 → **126** and on, in order): **126** the
   whole-number phone search matches `+970` typed as `+972` but not the reverse (review 4; the fix it names:
   match the national digits without the trunk, at least 9); **127** the dated check-in list filters on a
   Gaza-date expression with no index (review 5; the fix: bound `checked_in_at` by the two Gaza midnights; to
   decide with finding 120). Each a file and an index line.

**Not carried:** review 6 (a retry may add `SPACE_FULL`) — the contract already states it; no change.

Every item is done in this PR; one you would leave, or one that proves larger than this file says → **stop
and ask**, never silently.
