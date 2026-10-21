# Carried from #101 (PUBLIC PR 1a, `feat/directory-list`) into PUBLIC PR 1b (`feat/directory-filters`)

**The owner's review rule:** a serious or large review fix reopens its PR; small ones are deferred to the
**next PR as dedicated commits at its start**, named in that PR's description ("Carried from #101"). #101's
review (`C:\dev\masaha\workspace\WORKER_A\PUBLIC\6_REVIEW_PR1A_CLAUDE_CODE.md`, head `e50d9222`) found no
blocker; #101 merged at `befd96f9` (2026-10-21). These are **PR 1b's first commit(s)**, before the plan's
commit 6, each code fix with its own test seen red before the fix and green after, recorded in
`4_REPORT_PR1B.md`. Read the review for each item's file, line and scenario.

Suggested subjects (recount, ≤ 50): `refactor(lists): share the page-in-range rule` (item 6);
`fix(directory): keep the focus while searching` (items 1, 8); `fix(directory): offer a retry after a limit`
(items 2, 10); `fix(directory): drop a budget below its minimum` (item 3); `fix(site): focus the page after
signing in` (item 5); `fix(directory): read a card's details` (item 7); `fix(directory): say no count of
zero` (item 11). Group them differently if a smaller set of atomic commits reads better; say so.

**Decided by the owner (2026-10-21), as the supervisor recommended:**

1. **The focus moves to the results only for a page the visitor chose** (review 1): a page change reached by a
   push (the pages are links), never by a replace (a search, an order, a page past the last). Test: on page 2,
   type a search — the field keeps the focus; and a pasted `?page=5` replaced by the last page moves nothing.
2. **After a rate-limit refusal the failure stays with its retry** once the countdown ends (review 2), as the
   admin's spaces list does. Test: a 429 with `Retry-After: 1`, the clock advanced, «إعادة المحاولة» offered
   and asking again.
3. **A hand-edited budget with its maximum below its minimum never reaches the server** (review 3): the
   maximum is dropped, the same rule as commit 6's `priceBounds`; test 10 gains `min=50&max=10`. If commit 6
   replaces `filtersOf`'s price reading, the rule and its test move with it — the case stays proven.
4. **`lookups.md`'s lines 18 and 104** (review 4): **no separate change** — commit 6 wires `AreaFilter` into
   the Directory, which makes them true. Check them against commit 6's code and say so in the report.
5. **The site's focus after signing in** (review 5): a `SiteLayout` mounted by a client-side navigation (from
   the focus shell) moves the focus to `main`; a first load or a reload does not. Test: sign in from the focus
   shell → the site's `main` has the focus. The focus shell's own lack goes into **finding 130**'s text (a line,
   with `{date}` and `#PRNUM`).
6. **`usePageInRange` moves to `shared/lists`** (review 6) by `git mv`, exported from its barrel; its two
   `space-links` importers and `useDirectoryList` use it; the inline copy goes. No behaviour change.
7. **A card's details are read after its name** (review 7): the link keeps the name as its name and gains
   `aria-describedby` pointing at the area and details block; test 27 asserts the description too.
8. **The count is announced only from a real answer** (review 8): while the shown answer is a placeholder, the
   live region keeps its last line.
9. **No visible loading sign on the next page** (review 9): **recorded, not built** — a new finding (the next
   free number from 132; say it), naming every paged list (the admin's lists behave alike), for the design.
10. **The untested states** (review 10): `refreshFailure` (a failed refetch over shown cards) gains its test;
    the `blocked` path is item 2's.
11. **A count of zero draws no line** (review 11): the empty directory and no match show only their
    `EmptyState`; the count line's zero forms leave both catalogues if nothing else uses them.

Every item is done in PR 1b; one you would leave → **stop and ask**, never silently.
