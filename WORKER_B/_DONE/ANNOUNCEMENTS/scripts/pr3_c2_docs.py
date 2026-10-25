def edit(path, pairs):
    t = open(path, encoding='utf-8', newline='').read()
    for old, new in pairs:
        assert t.count(old) == 1, (path, old[:70], t.count(old))
        t = t.replace(old, new)
    open(path, 'w', encoding='utf-8', newline='').write(t)


edit('docs/api/api-contract.md', [
    ("""- a space's announcements on its page (`GET /spaces/:slug`), its running and upcoming ones, at most 20: a space posts tens at most, and the page shows them together (§5, *Directory (public)*; 2026-10-24, #112).
""", """- a space's announcements on its page (`GET /spaces/:slug`), its running and upcoming ones, at most 20: a space posts tens at most, and the page shows them together (§5, *Directory (public)*; 2026-10-24, #112);
- a user's favourites (`GET /me/favorites`), at most 200: the screen shows them together, near me included (§5, *Favourites*; #PRNUM).
"""),
    ("""A signed-in user keeps the listed spaces they want to find again, at most 200 (`FAVORITES_MAX`, `@masaha/shared/favorites`). A favourite is the user's own choice: it is not audited. Built #PRNUM.
""", """A signed-in user keeps the listed spaces they want to find again, at most 200 (`FAVORITES_MAX`, `@masaha/shared/favorites`), and reads them as the directory's cards. A favourite is the user's own choice: it is not audited. Built #PRNUM.

```ts
FavoriteSpace =                    // @masaha/shared/directory
  | { listed: true, savedAt: string, space: DirectorySpace }    // the directory's card, its live status included
  | { listed: false, savedAt: string,                            // hidden, deleted, or in an area not listed
      space: { id: number, nameEn: string, nameAr: string | null } }
```

#### `GET /me/favorites` · 👤
- **Query:** `sort` (`distance`, or absent; `invalid_choice` otherwise), with the device's point in the `Masaha-Near` header by the list's rules (*Directory (public)*): three decimals at most (`invalid_format`), inside the Strip (`out_of_range`); `distance` without the header is `required` on `near`, the header without `distance` `invalid_choice` on `near`.
- **200:** `FavoriteSpace[]`, the caller's own only, whole (§4's exception), no `meta`. Without `sort`, the newest saved first, then by space id. With `sort=distance`, the listed ones nearest first, each with its `distanceMeters`, then those that left the directory, newest saved first. No card carries a capacity or a count (ADR 0008).
- **Caching:** every answer to a request that carries the header, a refusal included, `Cache-Control: no-store`.
- **Errors:** `unauthorized` (401) without a signed-in user; `validation` (422) on the query.
"""),
])

edit('docs/backend/conventions.md', [
    ("""| `directory` | L5 | — | public | The public directory and profile, and the favourites' cards (§9) |""",
     """| `directory` | L5 | — | public, me (the favourites, at `/me/favorites`) | The public directory and profile, and the favourites' cards (§9) |"""),
    ("""- **The favourites' cards** (live status and prices) → `directory`, from the ids that `favorites` records. `favorites` never reads live status.""",
     """- **The favourites' cards** (live status and prices) → `directory`, from the ids that `favorites` records, newest saved first: the public listing lists those still listed as its cards, from the point nearest first; `spaces` names the rest, soft-deleted ones included, `listed: false`. `favorites` never reads live status. #PRNUM."""),
])

edit('docs/backend/security.md', [
    ("""- **It is sent in a header, only to sort by distance.** The `Masaha-Near: lat,lng` request header, never the query:""",
     """- **It is sent in a header, only to sort by distance:** the directory's list, and a user's favourites (`GET /me/favorites`, #PRNUM). The `Masaha-Near: lat,lng` request header, never the query:"""),
    ("""- **No cache keeps an answer to a request that carries it:** every such answer, a refusal or a failure included, is `Cache-Control: no-store`.""",
     """- **No cache keeps an answer to a request that carries it:** every such answer, a refusal or a failure included, is `Cache-Control: no-store`; on the favourites it is set before the sign-in guard, so the guard's refusal too (#PRNUM)."""),
])

edit('docs/features/directory.md', [
    ("""- Carries each card's and pin's live status, and answers a space's live status alone.
""", """- Carries each card's and pin's live status, and answers a space's live status alone.
- Answers a signed-in user's favourites whole, as its cards, newest saved first or nearest first from the device's location; one that left the directory by its name, `listed: false` ([favorites](favorites.md)).
"""),
    ("""The reports and the favourites' cards are not built; the page's announcements""",
     """The favourites' screen and the space page's heart are not built; the page's announcements"""),
    ("""- **Anyone,** signed in or not, through the API, and on the site: «المساحات», the directory's list and map, and a space's page; on Home, its spaces and the areas' counts.
""", """- **Anyone,** signed in or not, through the API, and on the site: «المساحات», the directory's list and map, and a space's page; on Home, its spaces and the areas' counts.
- **A signed-in user,** through the API: `GET /me/favorites`.
"""),
    ("""- **Leaves** which announcements the public sees, and their order, to [`announcements`](announcements.md).
""", """- **Leaves** which announcements the public sees, and their order, to [`announcements`](announcements.md).
- **Leaves** which spaces a user saved, and when, to [`favorites`](favorites.md); the names of those that left the directory to [`spaces`](spaces.md) (`namesWithDeleted`).
"""),
    ("""- Its public router is mounted at the API's root, unguarded, behind the general rate limit ([security › Rate limits](../backend/security.md#rate-limits-fixed-window)).
""", """- Its public router is mounted at the API's root, unguarded, behind the general rate limit ([security › Rate limits](../backend/security.md#rate-limits-fixed-window)).
- Its me router, at the API's root too, answers `GET /me/favorites`: `no-store` when the point is sent, then `requireAuth`, then the query with its header, by the list's rule (one function reads both).
"""),
    ("""- **API:** `apps/api/src/modules/directory/`, entry `index.ts`: the public router, its controller""",
     """- **API:** `apps/api/src/modules/directory/`, entry `index.ts`: the public router and the me router (the favourites, their order in `favoritesOrder.ts`), their controller"""),
    ("""- #112 — a space's running and upcoming announcements on its page.
""", """- #112 — a space's running and upcoming announcements on its page.
- #PRNUM — a signed-in user's favourites, whole, as its cards, newest saved first or nearest first.
"""),
    ("**Last Updated:** 2026-10-24", "**Last Updated:** 2026-10-25"),
])

edit('docs/features/favorites.md', [
    ("""- Answers a save of a space already saved, and a removal of one not saved, as done, writing nothing.
""", """- Answers a save of a space already saved, and a removal of one not saved, as done, writing nothing.
- Records which spaces a user saved, and when, for the directory, which answers them as its cards (`GET /me/favorites`, [directory](directory.md)).
"""),
    ("""- **A signed-in user,** through the API: `POST` and `DELETE /me/favorites/:spaceId`. The space page's heart and the account's favourites are not built.""",
     """- **A signed-in user,** through the API: `POST` and `DELETE /me/favorites/:spaceId`; the list, `GET /me/favorites`, is the [directory](directory.md)'s. The space page's heart and the account's favourites are not built."""),
    ("""- **Leaves** whether a space is publicly listed""",
     """- **Leaves** the list's cards, their order from a point and the names of the spaces that left to [`directory`](directory.md) ([conventions › Composed reads](../backend/conventions.md#composed-reads)).
- **Leaves** whether a space is publicly listed"""),
    ("""**Remove.** The caller's row of that space deleted, if there is one, 204 either way: a space that left the directory is removed all the same.
""", """**Remove.** The caller's row of that space deleted, if there is one, 204 either way: a space that left the directory is removed all the same.

**The list** (`directory`). The user's rows, newest saved first, then by space id (at most 200); the public listing's cards of those it lists, with their live statuses, nearest first when the point is sent; the rest named by `spaces`, soft-deleted ones included, `listed: false`, after the listed ones when ordered by distance. A space restored or shown again is listed again: the row is kept.
"""),
    ("""- **Not audited.** *Why:* a person's own choice, no one else's record. #PRNUM.
""", """- **Not audited.** *Why:* a person's own choice, no one else's record. #PRNUM.
- **The list is answered whole, with distance from the `Masaha-Near` header** (AC-014, Q9). *Why:* the screen shows every favourite at once, near me included, by the directory's privacy rules; a space that left stays, `listed: false`, so the user can remove it (C7). #PRNUM.
"""),
    ("""- #PRNUM — a signed-in user's favourites saved and removed, idempotent, at most 200.""",
     """- #PRNUM — a signed-in user's favourites saved and removed, idempotent, at most 200; read whole as the directory's cards, newest saved first or nearest first."""),
])

edit('docs/README.md', [
    ("""- [data-reports.md](features/data-reports.md) — a space's data reports""",
     """- [favorites.md](features/favorites.md) — a user's favourites: saved and removed, idempotent, at most 200, read whole as the directory's cards, newest saved first or nearest first (API only).
- [data-reports.md](features/data-reports.md) — a space's data reports"""),
])

edit('docs/plans/v1-mvp.md', [
    ("""`GET /me/reports`, the user's own reports with the replies (#120, [api-contract › Data reports](../api/api-contract.md#data-reports)).
""", """`GET /me/reports`, the user's own reports with the replies (#120, [api-contract › Data reports](../api/api-contract.md#data-reports)); the favourites, `GET /me/favorites` and `POST` / `DELETE /me/favorites/:spaceId` (#PRNUM, [api-contract › Favourites](../api/api-contract.md#favourites)).
"""),
    ("""| GET | `/me/favorites` · POST / DELETE `/me/favorites/:spaceId` | 👤 |""",
     """| GET | `/me/favorites` · POST / DELETE `/me/favorites/:spaceId` | 👤 at most 200, whole, near me by the header (built, #PRNUM) |"""),
    ("""the reporter anonymous to the owner (#120, [api-contract › Data reports](../api/api-contract.md#data-reports)). The screens remain planned.""",
     """the reporter anonymous to the owner (#120, [api-contract › Data reports](../api/api-contract.md#data-reports)); favourites, on the API: saved and removed, idempotent, at most 200, read whole as the directory's cards, newest saved first or nearest first (#PRNUM, [api-contract › Favourites](../api/api-contract.md#favourites)). The screens remain planned."""),
])

edit('docs/project/overview.md', [
    ("""- [Data reports](../features/data-reports.md): on the API,""",
     """- [Favourites](../features/favorites.md): on the API, a signed-in user's favourite spaces, saved and removed, at most 200, read whole as the directory's cards, nearest first when the device's location is sent.
- [Data reports](../features/data-reports.md): on the API,"""),
])
