# Carried from #96 (OWNER_SETUP PR 1, `feat/owner-space-profile`) into OWNER_SETUP PR 2 (`feat/owner-packages`)

**The owner's review rule (2026-10-20):** a serious or large review fix reopens its PR; small ones are
deferred to the **next PR as a dedicated commit at its start**, named in that PR's description ("Carried
from #96"). #96's review (`6_REVIEW_PR1_CLAUDE_CODE.md`, head `9fae4e00`) found no blocker; the supervisor
confirmed item 1 in the code. These are **PR 2's first commit(s)**, before the plan's commit 6, each code
fix with its own red-then-green test and break, recorded in `4_REPORT_PR2.md`. Read the review for each
item's file, line and fix.

Suggested subjects (recount, ≤ 50): `fix(lookups): count only linked retired amenities` for items 1 and 10;
`docs(spaces): bring the owner's profile docs up to date` for items 2–4 and 8 (or fold the documents into the
first commit if they are few — say which).

1. **The owner's retired-amenity line counts ticks, not links** (review 1; `useAmenityChecklist.ts:37-40`):
   count `value ∩ linked` missing from the catalogue; on a toggle, drop an unseen id that is not in `linked`;
   a test with a ticked, unlinked id missing from the catalogue (red first), and its break.
2. **`docs/frontend/architecture.md` §7** allows only two cross-capability invalidations; add the owner's
   `['me']` and the editor's lookups scope (`['admin']` or `['public']`), as the review words it.
3. **Stale headers:** `spaces.md` *Authority* ("API-only" managed routes), `lookups.md` *Scope* ("for the
   admin").
4. **`overview.md`:** the profile's prices "a link to Packages & prices, not built yet" — PR 2 then rewrites
   the line as it builds the page.
5. **`PricesLinkCard`'s separator** `aria-hidden`, as the code's precedent.
6. **`pricesLink.missing`** dropped (a field only a test reads); the test asserts «لم تُضف بعد».
7. **Stale or broken comments** (review 8): the admin's reasons in the owner's hooks, the bad wrapping.
8. **An owner's 404 refreshes the switcher** (review 9, plausible): on the owner's place, a 404 also marks
   `scope.answered` out of date — if you confirm the switcher keeps the space otherwise; else record it in
   the report as not reproduced, no code.
9. **The admin's checklist has the same trap** (review 10, pre-existing): an amenity the admin ticked and
   that is retired before the save vanishes but stays in the value. Fix it beside item 1 (the same hook), and
   correct `spaces.md` and `useAmenitiesSection`'s JSDoc ("so the checklist marks it"). If it proves larger
   than item 1's fix, stop and ask instead.

**Finding numbers:** worker A's next free ones start at **101** (98 and 100 are worker B's, 99 is #96's).
**The demo-password point (review 5)** is the owner's to decide; see the supervisor's note in the execution
prompt.
