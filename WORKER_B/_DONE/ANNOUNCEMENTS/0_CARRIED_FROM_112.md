# Carried from #112 (ANNOUNCEMENTS PR 1, `feat/announcements`) into PAYMENTS PR 1 (step 9, worker B's next API PR)

**The owner's review rule:** a serious or large review fix reopens its PR; small ones go to the **next PR as
dedicated commits at its start**, named in that PR's description ("Carried from #112"). #112's review
(`C:\dev\masaha\workspace\WORKER_B\ANNOUNCEMENTS\6_REVIEW_PR1_CLAUDE_CODE.md`, head `fdae748b`) found no blocker
and asked for no fix round. **Worker B's next PR is step 9's first** (the owner put step 9 next, 2026-10-24);
these are its first commits, each code fix with its own test seen red before the fix and green after. Read the
review for each item's file, line and scenario. The supervisor confirmed item 1 in the code.

Suggested subjects (recount, ≤ 50): `fix(announcements): hold the period on start now`
(item 4); `docs(announcements): state the public read and fixes` (items 1–3, 5, 6).

**Decided by the owner (2026-10-24), as the supervisor recommended:**

1. **Conventions §9 *Composed reads*** (review F1): the announcements bullet moves below the customers list's
   last sub-bullet, at the level of the other composed reads, so the customers list keeps its sub-bullets.
2. **`announcements.md` states the public read** (review F2): a *What it does* line (a space's running and
   upcoming announcements, not deleted, by start then id, up to the count the caller gives, for its public
   page); `directory` in *Who uses it*; the read in *Behaviour and flows*; the #112 history line names it.
3. **"will read"** (review F3): the contract's `GET …/announcements/summary` line — "the owner's overview will
   read the same count".
4. **Start now holds S5's 365-day bound** (review F4) — **fix**: `start()` refuses with 422
   `endsAt: out_of_range` when the end would fall more than 365 days after now (the edit's rule); a test (red
   first). *Alternative:* leave the code, record finding 150, and the contract says the bound applies to the
   post and the edit only.
5. **A retry after a delete** (review F5) — **say it, no code**: the contract's POST line adds "a
   retry of a deleted announcement answers it as it was, deleted from every read". *Alternative:* a 404 on such
   a retry (a code change, against ADR 0015 rule 3's "never a conflict").
6. **History lines in order** (review F6): `#112` last in `desk.md` and `subscriptions.md`'s histories.

**Done by the supervisor once #112 merges, not carried:** `_SHARED\OPEN_DECISIONS.md` point 2's settled line
(the report's §9), with "will read" for the overview.

Every item is done in that PR; one you would leave, or one that proves larger than this file says → **stop and
ask**, never silently. A new finding takes **150** and on.
