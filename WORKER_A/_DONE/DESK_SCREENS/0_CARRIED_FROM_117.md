# Carried from #117 (DESK_SCREENS PR 1b, `feat/desk-uncollected`) into DESK_SCREENS PR 2 (`feat/desk-subscribers`)

**The owner's review rule:** a serious or large review fix reopens its PR; small ones go to the **next PR as
dedicated commits at its start**, named in that PR's description ("Carried from #117"). #117's review
(`C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\6_REVIEW_PR1B_OPENCODE.md`, head `a1193e77`) found one
should-fix, small; the supervisor confirmed it in the code. It is **PR 2's first commit**, the fix with its own
test seen red before it and green after.

Suggested subject (recount, ≤ 50): `fix(desk): show the last uncollected page in range`.

1. **A page of the uncollected visits past the last** (review F1): `useUncollectedCard.ts` keeps the page in
   the address (`uncollectedPage`) but never uses `usePageInRange` (`apps/web/src/shared/lists`), so when the
   visits of the last page are collected or written off — or a stale address names a page past the last — the
   card's `items` is empty and its state is `empty` («لا شيء لتحصيله»), hiding the rows of the pages before it
   and the pagination. **Fix:** use `usePageInRange` as the other paged lists do (the last page shown in place of
   one past it, the address replaced, not pushed), and let `state` read `empty` only when the list's total is 0.
   **Test:** a list answering page 3 empty with `totalPages: 2` → the card shows page 2's rows and its
   pagination, never the empty line; break: `usePageInRange` removed → red.

**Recorded, not carried:** the review accepted «بدون سعر» showing its first page only (pricing a visit
refetches the list, so the next unpriced visit moves into the first page). And `routes.component.test.tsx` ›
"lists reception's four pages" missed its 3 s locally the same way as finding 87's family — it joins
`WORKER_A\PUBLIC\0_CARRIED_FROM_111.md` item 11's list.

Every item is done in PR 2; one you would leave, or one that proves larger than this file says → **stop and
ask**, never silently.
