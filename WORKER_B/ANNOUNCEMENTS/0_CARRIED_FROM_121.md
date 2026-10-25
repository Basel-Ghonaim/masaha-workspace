# Carried from #121 (ANNOUNCEMENTS PR 3, `feat/favorites`) into worker B's next API PR (ANNOUNCEMENTS PR 4, `feat/closure-extension`)

**The owner's review rule:** a serious or large review fix reopens its PR; small ones go to the **next PR as
dedicated commits at its start**, named in that PR's description ("Carried from #121"). #121's review
(`C:\dev\masaha\workspace\WORKER_B\ANNOUNCEMENTS\6_REVIEW_PR3_CLAUDE_CODE.md`, head `91d9b27f`) found no
blocker, one should-fix (small) and four nits; the owner merged #121 (`1a89da5d`) with them carried. The
supervisor confirmed item 1 in the code (`favorites.service.ts`: `isListed` inside `runInTransaction`, through
`lookups.listedAreaIds()` and `publicListing.upTo`, neither given `tx`; `db/prisma.ts` sets no pool `max`). Read
the review for each item's file and lines.

Suggested subjects (recount, ≤ 50): `fix(favorites): read the listing before the lock` (items 1 and 4);
`docs(favorites): date the decisions and fixes` (items 2, 3, 5).

1. **The save's listed read runs on other connections while it holds the user's lock** (review 1,
   should-fix): read `isListed(spaceId)` **before** `runInTransaction`, as the data-reports create does
   (conventions §8 *Transactions*). Keep the answers' order inside the transaction: the user's lock, then
   already saved → 204 (writing nothing), then not listed → `not_found`, then the ceiling, then the insert. No
   answer changes; a space hidden between the read and the insert is saved and shown `listed: false` (as today).
   **Its test is item 4 (a):** red against a break that moves the listed check ahead of "already saved", green
   after.
2. **Dates on #121's lines** (review 2): add `2026-10-25, ` before `#121` on `favorites.md`'s *API decisions*
   bullets, the contract's *Favourites* "Built" line, its §4 exception line and its §6 code line, and
   `conventions.md`'s header and §9 *Composed reads* lines — as every #112 and #120 line reads.
3. **`directory.md`'s *Authority*** (review 3): "… what anyone reads without signing in, and a signed-in user's
   favourites as its cards", with `api-contract.md#favourites` linked beside `#directory-public`.
4. **Two documented behaviours with no test** (review 4): **(a)** save a space, hide it, save it again → 204,
   still one row (extend T1 or T3); **(b)** a favourite whose space's area is made inactive is answered
   `listed: false` with its name (add it to T8). Each seen red under its break, then green.
5. **The tie's direction** (review 5): the contract's `GET /me/favorites` 200 and `favorites.md` › *The list*:
   "the newest saved first, then the higher space id first" (`favorites.repository.ts` orders `spaceId: 'desc'`).

**Left from #120, still open:** `0_CARRIED_FROM_120.md` item 4 (the 112-character comment line in
`apps/api/test/app.ts`) — re-wrap it only if a commit of PR 4 touches that file; otherwise leave it and say so.
No finding is recorded by this file; a new finding takes **151** and on.

Every item is done in that PR; one you would leave, or one that proves larger than this file says → **stop and
ask**, never silently.
