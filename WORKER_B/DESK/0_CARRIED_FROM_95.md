# Carried from #95 (DESK PR 2, `feat/desk-visits`) into DESK PR 3 (`feat/auto-checkout`)

**The owner's review rule (2026-10-20):** a serious or large review fix reopens its PR; small ones are
deferred to the **next PR as a dedicated commit at its start**, named in that PR's description ("Carried
from #95"). #95's review (`6_REVIEW_PR2_CLAUDE_CODE.md`, head `b225d1fa`) found no blocker; it merged at `f77d2012` (2026-10-20); the supervisor
confirmed items 1 and 2 in the code. They are **DESK PR 3's first commit**, before the plan's C1, with its
own red-then-green tests and breaks, recorded in `4_REPORT_PR3.md`.

Suggested subject: `fix(desk): refuse a check-out before its check-in` (recount, ≤ 50).

1. **A check-out time earlier than the check-in answers 500.** `desk.service.ts`'s quote bound (≈ line 69)
   checks the quote's age against the request only; a `checkedOutAt` before the visit's `checkedInAt` reaches
   the database's own rule (a visit closes after it opens), and the error translation table has no line for
   it. Fix: refuse it before the write with 422 `out_of_range` on `checkedOutAt`; a test, and a break
   (the comparison removed → the 500 comes back).
2. **`docs/backend/security.md`'s carried sentence is already out of date:** it names the override as the
   staff's only writes, and the next sentence adds the desk's writes, also the staff's. Fix the sentence
   (each write by its own `can()` action, owner-only or the staff's).
3. **`visits.md` says the desk decides who may type a price;** the visit-terms read asks `can()` itself.
   Fix the line to match the code.
4. **The review's other small nits** (its report, "nits"), each as the review says, where they are small
   and in PR 3's files or documents; any the executor judges not small → stop and ask.

**Taken by the owner (2026-10-20), with #95's merge at `f77d2012`, as the supervisor recommended:**

5. **A check-out that loses a race drops the second desk's payment and answers 200** (`payment: null`), as the
   plan's T20 specified: cash taken at the second desk would be in no ledger. *Recommended:* when the visit
   is already closed by another key **and the request carries a payment**, refuse it with 409 (a code of its
   own or `VISIT_ALREADY_CLOSED`, its Arabic line for the owner's approval), so the desk knows the cash is
   not recorded; a request without a payment keeps today's answer. Built in this same carried commit, before
   the desk's screen is built against it; the contract, `desk.md` and T20 say so.
6. **An unpaid check-out moves the visit to the phone's customer even when the visit already has one** —
   unreachable until step 8 checks a customer in as a visit. Record it as **finding 100** (reserved for
   worker B; worker A's next ones start at 101) in this commit.
