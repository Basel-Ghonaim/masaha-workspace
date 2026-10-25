# Carried from #123 (ANNOUNCEMENTS PR 4, `feat/closure-extension`) into worker B's next API PR (FINANCE_AUDIT PR 1)

**The owner's review rule:** small review fixes go to the **next PR as dedicated commits at its start**, named in
that PR's description ("Carried from #123"). #123's Claude review (`C:\dev\masaha\workspace\WORKER_B\_DONE\ANNOUNCEMENTS\
6_REVIEW_PR4_CLAUDE_CODE.md`, head `ff8743c8`) found no blocker and no should-fix in the code, one decision-level
gap and three nits. The supervisor confirmed items 1 and 2 in the code. Read the review for each item's file and
lines.

1. **Finding 151 — a renewal sold before the extension stays put** (review 1). The covered rule ignores
   `renewal_of_id`, and a renewal starts the day after the renewed one's end (`renewal.ts` `proposedStart`). So an
   extension moves the old subscription's end into its renewal's days; the two overlap, the renewal is "current",
   and the customer's days are lost. **The owner's decision (2026-10-26): option A — the extension also moves each
   covered subscription's renewal chain that has not started yet** (`starts_on` after today, not ended early), by
   the same days, start and end, in the same transaction and under the same locks (the chain's rows locked with the
   covered ones, `ORDER BY id`), each linked to the extension as the covered ones are, and audited in the same
   entry (`after.subscriptionIds` and the moved renewals). A renewal that already started is not moved (it is
   covered or not by the rule itself). Write **finding 151** (Status: Resolved by this PR, its *Resolution* line
   with the date and `#PRNUM`), its index line; the contract's extension routes, data model (*Checked by the
   service*: the covered rule and the chain), `announcements.md` / `subscriptions.md` where the rule is said.
   Tests: the review's scenario (S 11-01→11-30, its renewal R 12-01→12-30, a closure 11-08→11-10, extended by 3 →
   S ends 12-03, R runs 12-04→01-02; one row each, no overlap); a renewal already started is not moved; the
   preview's count says what it will move (decide whether the chain counts, and say it). Each red first; a break
   that drops the chain's move.
2. **A key retried against another space's URL answers that space's extension** (review 2, nit): `findByKey` is
   global (the key is unique on its own); the retry compares only `announcementId`. Make another space's
   extension under that key a `conflict` (or `not_found` — choose and say why), checked before answering; one line
   in T5. Red under a break that skips the space check.
3. **`data-model.md:23`** (review 3): the extension's key is listed under "unique within its space"; it is unique
   on its own (`closure_extensions_request_id_key`, and the same document's line 140). Say so there.
4. **`subscriptions.md`'s API history order** (review 4): the `#123` line sits above `#118`'s; move it below.

Suggested subjects (recount, ≤ 50): `fix(subscriptions): move a renewal with its extension` (item 1);
`fix(subscriptions): keep a retried key to its space` (item 2); `docs: correct the extension's key and history`
(items 3–4).

Every item is done in that PR; one that proves larger than this file says is decided under the run's rule and
recorded, never left silently.
