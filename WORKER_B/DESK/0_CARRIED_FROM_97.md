# Carried from #97 (DESK PR 3, `feat/auto-checkout`) into DESK PR 4 (`feat/visit-debts`)

**The owner's review rule (2026-10-20):** a serious or large review fix reopens its PR; small ones are
deferred to the **next PR as a dedicated commit at its start**, named in that PR's description ("Carried
from #97"). #97's review (`6_REVIEW_PR3_CLAUDE_CODE.md`, head `e122b95d`) found no blocker; the supervisor
confirmed item 1 in the code (`visits.service.ts` `autoCheckOut`: no per-stay catch; the `!rules` branch).
These are **DESK PR 4's first commit**, before the plan's first commit, each code fix with its own
red-then-green test and break, recorded in `4_REPORT_PR4.md`. Read the review for each item's file, line and
fix.

Suggested subject: `fix(jobs): keep closing stays past a failing one` (recount, ≤ 50); a second carried
commit for item 2 if its code change is taken.

1. **One failing stay halts the job everywhere** (review 1): catch per stay in both `autoCheckOut`s (log
   `{ err, job, stayId }`, count `failed`, go on; the run answers 500 when `failed > 0`); make the `!rules`
   branch real (`settingsFor` skips an absent row) or delete it; one test with two stays, the first made to
   fail, and its break.
2. **"A stay never crosses into the next day" is not what the code does** (review 2) — **the owner chose (b),
   widened (below): a second carried commit, `fix(visits): close every stay by its day's end`.**
3. **`visits.md`'s boundary** (review 4): *Leaves* and *Owns*/*How it composes* as the review words them.
4. **The scheduler's local fact in two homes; `.env.example`'s comment** (review 5): as the review says.
5. **The runbook names the header exactly** (review 6: `Bearer`, case and all) — one line in setup's runbook.
6. **`v1-mvp.md` step 7 *Built*** (review 8): PR 4 rewords it as it lands (collecting and writing off).
7. **Findings to record** (numbers from 110, worker B's PR 4 block): #95's nit 7 (one helper for *present*);
   #95's nit 8 (a key that closed a visit with no payment is not remembered); review 7 (the uncollected read
   grows with every auto-closed visit). #95's nit 9 (the charge overflowing `Int`) resolves with item 2 (b),
   else it is recorded too with its true reason.

**Item 2 — decided by the owner (2026-10-20): (b), widened, as recommended; #97 merged at `abc28e73`.** the data model calls a visit
"a same-day stay", and the stay limit's schema says so too; the code lets the stay-limit branch cross
midnight (23 h from a 20:00 check-in) and, with the closing check-out off and no limit, never closes a stay.
*Recommended (b), widened:* the code follows the documentation — a stay's due time is the earliest of the
closing (when on), the stay limit (when set) and **23:59 of its check-in's Gaza day, always**; one `Math.min`,
unit tests for the three branches, a break each; the comment corrected; #95's nit 9 resolved (a charge is
then bounded by one day). *Alternative (a):* the documentation follows the code (the limit may cross
midnight; with both off, no auto check-out), and nit 9 is recorded.
