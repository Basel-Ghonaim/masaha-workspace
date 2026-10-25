# Carried from #100 (DESK PR 4, `feat/visit-debts`) into SUBSCRIPTIONS PR 1 (`feat/customers`)

**The owner's review rule:** a serious or large review fix reopens its PR; small ones are deferred to the
**next PR as a dedicated commit at its start**, named in that PR's description ("Carried from #100"). #100's
review (`C:\dev\masaha\workspace\WORKER_B\DESK\6_REVIEW_PR4_CLAUDE_CODE.md`, head `68edd9bc`) found no blocker;
#100 merged at `5d42a527` (2026-10-21). These are **SUBSCRIPTIONS PR 1's first commit(s)**, before the plan's
C1, each code fix with its own red-then-green test and break, recorded in `4_REPORT_PR1.md`. Read the review
for each item's file, line and fix.

Suggested subjects (recount, ≤ 50): `fix(jobs): answer 200 when only stays failed` (item 1);
`fix(desk): charge a stay up to its day's end` (item 2); the documents folded into the commit they belong
with, or `docs(desk): say what the debts' PR built` (items 3–4).

**Decided by the owner (2026-10-21), as the supervisor recommended:**

1. **The jobs endpoint answers 200 with a `failed` count when every job ran and only stays failed**, logging
   each failed stay (`{ err, job, stayId }`); it answers 500 only when a job itself threw. The contract
   (*Internal*), `setup.md`'s runbook (read `stay not closed` in the logs) and the jobs' decision line say so.
   Tests: a run with one failing stay answers 200 with `failed: 1` and closes the others; a job that throws
   answers 500 — each with a break. (Review finding 1: record it as **finding 114**, resolved in the same
   commit.)
2. **A desk check-out charges a stay up to `min(the quote's time, the stay's due time)`** — the due time is
   `autoCheckoutDue` (every stay due by 23:59 of its check-in's Gaza day): the "same-day stay" holds on every
   path. The data model's *Auto check-out* and *Visit charge* and `desk.md` say so; state what `checkedOutAt`
   records (the request's time, the charge capped — or the due time; decide, recommend one, say why). Tests: a
   stay checked out the next morning is charged up to 23:59 of its day; a break each. (Review finding 4 →
   **finding 116**, resolved here.)
3. **A write-off and its undo carry no key** (review finding 3): **accepted for v1**; record it as **finding
   115** (Open), naming the desk's screen item: it must not retry these two routes automatically.
4. **The documents** (review finding 2): `payments.md` (a `#100` history line; "a check-out's or a payment's
   key"), `visits.md` (the desk's transactions: check-in, check-out, write-off and its undo, `leaveTo`),
   `conventions.md` §13 ("the ceiling locks the item's row"; name the uncharged rule or say "among them").
5. **The review's other nits** (6–8) only where they are small and in this PR's files; any you would leave →
   **stop and ask**, never silently.

Findings 114–116 are DESK's block (110–119); this item's own findings stay at 120 and on. #100's PR
description (review finding 5) stays as merged — this PR's report notes the four departures it omitted.
