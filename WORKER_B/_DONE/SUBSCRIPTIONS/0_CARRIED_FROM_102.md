# Carried from #102 (SUBSCRIPTIONS PR 1, `feat/customers`) into SUBSCRIPTIONS PR 2 (`feat/subscriptions`)

**The owner's review rule:** a serious or large review fix reopens its PR; small ones are deferred to the
**next PR as dedicated commits at its start**, named in that PR's description ("Carried from #102"). #102's
review (`C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\6_REVIEW_PR1_CLAUDE_CODE.md`, head `900eebb4`) found
one serious fix (the balance query) and the ids' bound beside it — both done in #102's fix round
(`7_FIXES_PROMPT_PR1.md`). These are the rest: **PR 2's first commit(s)**, before the plan's C1, each code fix
with its own test seen red before the fix and green after, recorded in `4_REPORT_PR2.md`. Read the review for
each item's file, line and scenario.

Suggested subjects (recount, ≤ 50): `fix(customers): find a phone in any form` (item 1);
`docs(customers): say what the customers' PR built` (items 2–4); findings folded into the documents commit.

**Decided by the owner (2026-10-21), as the supervisor recommended:**

1. **The phone search finds a number typed in any form** (review 3 with 9's separators): when
   `normalisePhone(q)` answers a number, match that phone exactly; otherwise the suffix match on the digits,
   with the same separators dropped as `core/phone.ts` (`-`, `.`, `(`, `)`, spaces, `+`). T22 and U3 gain a
   `+972` local form (`0521234567`), a `00970…` form and a hyphenated one.
2. **The three documents made untrue by #102** (review 4): `occupancy.md:25` (only `announcements` lacks a
   capability document; link `customers.md` and `subscriptions.md`); ADR 0015's line on keys — its *Revised*
   line (Q10) lands in this PR as planned, saying customers carry the key since #102 and subscriptions since
   this PR; `payments.md`'s uncollected visits' decision head reworded to what is built (paged in SQL).
3. **Reception reads an archived customer's file** (review 7, the owner's word): **kept** — an archived
   customer's debts are collected at the desk; the contract's *Customers (managed)* says so in one line.
4. **`CUSTOMER_ARCHIVED`'s comment** (review 9) says "edited", as the contract's gloss does (checking in is
   PR 3's).
5. **Findings to record** (this item's block, 121 and on, in order): **121** the auto check-out can stall
   silently behind a batch of stays that always fail (review 5, plausible — name the fixes it lists);
   **122** `subscription_usage` overflows `integer` on extreme usage-based prices and fails the whole space's
   reads (review 6); **123** a delayed retry of a customer edit can revert another desk's edit (review 8),
   naming the customers' screen item, with finding 115. Each a file and an index line, in the documents
   commit.

6. **An index on the visits' customer** (#102's fix round, its *Review Focus*; the owner's choice, 2026-10-21):
   PR 2's planned migration also creates an index serving `balancesOf`'s visits branch (the space's closed
   visits of the customers asked — say which columns and why, from `EXPLAIN`), so a page's visits cost what the
   page holds. Record the plan before and after in the report.

Every item is done in PR 2; one you would leave → **stop and ask**, never silently. The cosmetic comment width
in `customers.repository.ts` (review 9) is fixed only if that file is touched anyway.
