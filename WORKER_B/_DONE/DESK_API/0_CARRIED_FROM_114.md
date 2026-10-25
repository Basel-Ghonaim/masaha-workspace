# Carried from #114 (PAYMENTS, `feat/payments`) into DESK_API (worker B's next API PR)

**The owner's review rule:** a serious or large review fix reopens its PR; small ones go to the **next PR as
dedicated commits at its start**, named in that PR's description ("Carried from #114"). #114's review
(`C:\dev\masaha\workspace\WORKER_B\PAYMENTS\6_REVIEW_CLAUDE_CODE.md`, head `8ae243f0`) found no blocker and no
should-fix. These are **DESK_API's first commits**, each code fix with its own test seen red before the fix and
green after. Read the review for each item's file, line and scenario. The supervisor confirmed item 1 in the
code (`payments.manage.routes.ts:15`: the query is validated before the service's 403).

**Decided by the owner (2026-10-24: every fix deferred to worker B's next PR, as the supervisor recommended):**

1. **Reception's refusal, said exactly** (review N1, documents only): the contract's `GET …/payments` (*Who
   reads what*, *Errors*), `security.md`'s payments-list bullet and `payments.md` (S6) say "the query is
   validated first (422); a valid `from`, `to` or `recordedById` from reception is then `forbidden` (403), never
   ignored".
2. **One meaning for the two lists' 92 days** (review N2) — **align**: the check-ins list's dated
   range becomes 92 days with both ends counted, as the payments list (`to > addDays(from,
   CHECK_IN_RANGE_MAX_DAYS - 1)` in `packages/shared/src/subscriptions/requests.ts`), its unit test's edge, and
   the contract's check-ins line; no screen reads it yet, so nothing on the web changes. *Alternative:* leave
   both and record finding 170.
3. **No PR number inside a migration** (review N3) — **write the rule, own commit**: one line in
   `docs/backend/conventions.md` (the migrations' rules): "a migration's SQL comments carry a date, never a PR
   number: the `#PRNUM` rewrite would change an applied migration's checksum". `payment_void_guard`'s file is
   **not** edited (its checksum is applied everywhere). *Alternative:* leave it unwritten (the supervisor keeps
   it out of plans).
4. **Cosmetics in `payments.repository.ts`** (review N4): the `uncollectedPage` JSDoc rewrapped within 100
   columns; `paymentsOfSubscription` and `paymentsOfVisits` select `ITEM_PAYMENT`. No behaviour change; the
   existing tests stay green.

Every item is done in that PR; one you would leave, or one that proves larger than this file says → **stop and
ask**, never silently. A new finding takes **170** and on.
