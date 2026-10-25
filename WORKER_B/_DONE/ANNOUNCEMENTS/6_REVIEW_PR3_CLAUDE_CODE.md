# Review — ANNOUNCEMENTS PR 3 (#121, `feat/favorites`)

- **Head:** `91d9b27f` (`91d9b27fc5422dd7bc602228d53be37c516557a9`), as expected; `mergeStateStatus: CLEAN`.
- **CI:** every check passed on that head (`build`, `check:classes`, `check:conflicts`, `check:links`,
  `format:check`, `lint`, `test:api`, `test:component`, `test:unit`, `typecheck`, CodeRabbit).
- **Did the head move?** No. It was `91d9b27f` at the start and still `91d9b27f` at the end.
- **How I read it:** only from commit objects (`git show 91d9b27f:<path>`, `git diff origin/main...91d9b27f`). I
  ran nothing, checked nothing out and edited nothing. What I only read in the executor's report is marked
  *(report)*.

## Verdict

**Mergeable.** I found no blocker. There is one should-fix, small enough for worker B's next PR, and four nits.

## Findings, most severe first

### 1. should-fix — the save's "is it listed" read runs on a second connection while the transaction holds the user's lock

- **Where:** `apps/api/src/modules/favorites/favorites.service.ts` lines 555–561 (`isListed`) and line 574 (its
  call inside `runInTransaction`).
- **Seen in the code:** `save` opens the transaction and locks the user's row (`users.lockAccount(actor.id, tx)`,
  which is the session lock). Then, still inside the callback, it calls `isListed(spaceId)`.
  `isListed` calls `lookups.listedAreaIds()` and `publicListing.upTo(...)`, and neither takes a `tx`.
  `upTo` (`spaces/public/publicListing.service.ts`) runs in sequence `platformSettings.stalenessThresholds()`,
  `repository.findFirst`, and then `hours.weeksFor` and `photos.coverKeysFor` in parallel. Every one of those uses
  the global `prisma`, so each needs a pool connection other than the one the transaction holds.
  - This breaks conventions §8 *Transactions*: "The orchestrator opens the transaction and passes `tx` to each
    lower module's service it calls."
  - The data-reports create (#120) asks the same "listed" question **before** its transaction
    (`data-reports.service.ts` lines 268–276: `findShown`, `isActiveArea`, then `runInTransaction` and
    `lockAccount`).
- **Failing scenario (plausible, not run):**
  - `PrismaPg` uses `pg`'s pool, 10 connections by default (`db/prisma.ts` sets no `max`). Its
    `connectionTimeoutMillis` of 2 000 ms also bounds the wait for a free connection.
  - Suppose about 10 users save at the same moment, or saves run beside other transactions. Each save holds one
    connection for its transaction and asks for one or two more. The pool can run out with every connection held
    by a transaction that is waiting for another one.
  - The inner reads then fail after 2 s. The user gets a 500 instead of 204, and the interactive transaction's 5 s
    timeout is spent.
  - More commonly, the user's session row stays locked across five extra queries. While it is locked, that user's
    refresh or sign-out waits on it.
  - T2 and T5 do not show this. Their test transaction holds the lock until both requests are queued, and two
    requests never exhaust the pool.
- **Fix:** read `isListed(spaceId)` **before** `runInTransaction`, as the data-reports create does. Keep the
  answers' order inside the transaction: lock, then `has` → return (204), then `!listed` → `not_found`, then the
  count, then the insert.
  - Moving the read changes no answer. The listed read is already outside the transaction's snapshot, so reading
    it earlier makes no race the code does not already have.
  - A space hidden between the read and the insert is saved and then shown `listed: false`, which is
    removable. That is harmless, and the same as today.
  - The cost is one listing read for a space that is already saved.
  - Optionally, add the missing test of finding 4 below with this fix.
- **Where the fix belongs:** small. It goes in **worker B's next PR's first commit** (ANNOUNCEMENTS PR 4,
  `feat/closure-extension`, through `0_CARRIED_FROM_121.md`).

### 2. nit — `favorites.md`'s decisions, and the new contract and conventions lines, carry no date

- **Where:**
  - `docs/features/favorites.md` › *API decisions*: all five bullets end in "#121." only.
  - `docs/api/api-contract.md` › *Favourites*: "Built #121."
  - The §4 exception line ("§5, *Favourites*; #121").
  - The §6 code line "(409: a new favourite past the user's 200, #121)".
  - `docs/backend/conventions.md`'s header ("`favorites` (…, #121)") and its §9 *Composed reads* line ("… #121.").
- **Why:** `documentation.md` §5's template asks for each decision "with its reason, its date and its PR". Every
  sibling line from #112 and #120 says "2026-10-2x, #1xx".
- **Fix:** add "2026-10-25, " (or the merge date) before each `#121`.
- **Where the fix belongs:** next PR's first commit.

### 3. nit — `directory.md`'s Authority still says "what anyone reads without signing in"

- **Where:** `docs/features/directory.md` line 4. Its Authority also says "Its endpoints are owned by the API
  contract (#directory-public)".
- **Why:** the document now also owns a signed-in read, `GET /me/favorites`. The body already says so (*What it
  does*, *Who uses it*, *How it composes the platform*). The endpoint's contract section is *Favourites*, not
  *Directory (public)*.
- **Fix:** "… what anyone reads without signing in, and a signed-in user's favourites as its cards", and link
  `api-contract.md#favourites` beside `#directory-public`.
- **Where the fix belongs:** next PR's first commit.

### 4. nit — two documented behaviours have no test

- **(a) A saved space that has left the directory, saved again, answers 204.** `favorites.md` says "The
  already-saved answer comes before the listing and the ceiling", and the code does it (`has` at line 573,
  before `isListed` at 574). Only the *ceiling* half is tested (T4).
  - Failing scenario: swap lines 573 and 574. Saving a hidden space you had already saved then gives 404 instead
    of 204, and every test stays green.
  - This matters for finding 1's fix, which moves the listed read.
- **(b) A favourite whose space is in an inactive area is answered `listed: false`.** The contract and
  `FavoriteSpace`'s comment both name it. T8 covers hidden and deleted only. The code path is the same
  `publicListing.page` filter (`areaIds: listedAreaIds`), so this is low risk.
- **Fix:**
  - For (a), extend T1 or T3: save, then hide the space, then save again → 204, still one row.
  - For (b), add an inactive-area favourite to T8.
- **Where the fix belongs:** next PR's first commit, together with finding 1.

### 5. nit — "then by space id" leaves out the direction

- **Where:** `api-contract.md` › `GET /me/favorites` 200, and `favorites.md` › *The list*: "the newest saved
  first, then by space id".
- **Seen in the code:** `favorites.repository.ts` line 508 orders `[{ createdAt: 'desc' }, { spaceId: 'desc' }]`,
  so the higher id comes first on a tie.
- **Fix:** "then the higher space id first".
- **Where the fix belongs:** next PR's first commit.

No finding needs recording (151 is not taken).

## `FAVORITES_LIMIT_REACHED`

409, `AppError.conflict('FAVORITES_LIMIT_REACHED', …)` (`favorites.service.ts` line 576). It is in
`packages/shared/src/core/errors.ts`, after `REPORT_ALREADY_DECIDED`, and in contract §6. Both catalogues have it.

- English (`apps/web/src/shared/copy/english/errors.ts`): «Your favourites are full; remove a space first.»
- Arabic (`apps/web/src/shared/copy/arabic/errors.ts`), exactly as in the code:
  **«امتلأت مفضّلتك؛ أزل مساحة أولًا.»** This is the line the owner approved in Q1.

## The departures, each judged

1. **`now` added to favourites' dependencies** (D15 left it out): **right.** Conventions §11 has one clock, and
   T1 asserts `createdAt` equals the test clock. data-reports does the same.
2. **`no-store` set before `requireAuth` on `GET /me/favorites`** (D15 put the guard first): **right, and
   needed.** Security › Location asks for `no-store` on every answer to a request carrying the point, "a refusal
   or a failure included". With the guard first, an anonymous request's 401 would have no header.
   - Seen: `directory.me.routes.ts` runs `keepNearPrivate`, then `requireAuth()`, then `validateFavoritesQuery`.
   - Seen: T9 asserts `no-store` on the anonymous 401, on the 422 and on the 200.
   - It is set twice (`parseWithNear` calls `keepPrivateIfNear` again). That is harmless.
3. **T7's `GET` added in C2:** **right.** The route does not exist in C1.
4. **"site" → "me" also in `data-reports.md`'s placement and code-map lines:** **right.** It is the same name, and
   leaving it would have kept the fifth router kind that item 1 removes.
   - Seen: both lines say "me".
   - *(report)*: the code-map line was folded in by a fixup.
5. **Carried item 4 left:** **right, as the carried file allows.** Seen: no file under `apps/api/test/` is in the
   diff.
6. **The `Masaha-Near` rule extracted** (shared `checkNear`, the API's `parseWithNear`): **right, and `GET /spaces`
   behaves exactly as before.** Seen:
   - `checkNear` is the two removed refinements word for word: the same paths, the same `required` and
     `invalid_choice`.
   - `directoryQuerySchema` calls it in the same place in its `superRefine`.
   - `validateListQuery` still sets `no-store` before it parses, builds the same `{ ...req.query, near }` input,
     throws the same `toValidationError`, and writes the same `res.locals.directoryQuery`.
   - `directory.routes.ts` is unchanged, and no existing directory test file is in the diff.
   - `nearPoint` is shared, not copied.
   - `favoritesQuerySchema`'s `z.literal('distance')` fails as `invalid_value`, which `fieldErrors.ts` line 46
     maps to `invalid_choice`, as the contract says.
7. **U1's red taken by moving `favoritesOrder.ts` aside:** **acceptable.** A "Cannot find module" red proves
   nothing about the order. B1 (*report*: U1 red with `[5, 3, 9, 1, 7]`) is the real proof of the guard, and the
   owner's rule allows a separate break for it.
8. **Lint and typecheck not re-run per commit after the docs-only fixup:** **acceptable.** CI ran `lint` and
   `typecheck` green on the head. A change to a document line cannot change either result for the earlier
   commits' trees. That the fixup touched one document line I only read in the report; I did not see the
   pre-fixup commit.
9. **C0's second subject shortened (53 → 43):** **right.** `docs(data-reports): state the decision race` (43), and
   its body names items 2, 3 and 5.

## Checked and fine

- **Authorization:**
  - All three routes are behind `requireAuth()` (`favorites.me.routes.ts`, `directory.me.routes.ts`).
  - The user is always `signedIn(req).userId`. The path carries only the space's id, so no route can name
    another user's favourite.
  - `remove` deletes by `{ userId, spaceId }` (B6, T6). `of` filters by `userId` (B9, T10).
  - `favorites.manage: 'self'` is unused, which is right: ownership is the actor's own id, and the plan made no
    change to `can.ts`.
  - The users' `/me` router has only `POST /password`, so it shadows neither router.
- **The save's transaction:**
  - Locking: `lockAccount` comes first (`null` → 401).
  - Answer order: already saved → return comes before the listed check and the ceiling.
  - Ceiling: the count is taken under the lock with `>=` (B5).
  - Key backstop: the composite key is the backstop. Its 500 (B2) cannot happen without the break, because the
    only writer of favourites checks `has` under the user's lock.
  - Race with hiding: a space hidden between the listed read and the insert is saved and then answered
    `listed: false`. That is harmless. Finding 1 is about where that read runs, not about this race.
- **The list:**
  - The cards: listed spaces go through the directory's own `cardsOf`, the code `list` used before, extracted
    without change. They carry live statuses from `liveStatusesOf`, and `verifiedIds` comes from `space-links`.
  - What a card leaves out: T8 compares each card with `GET /spaces`' own, and T10 checks there is no capacity
    and no count.
  - Spaces that left: `spaces.namesWithDeleted`, `listed: false`.
  - Order: `favoritesOrder` puts the listed ones first by the listing's distance order, then the unlisted ones
    newest saved first.
  - A favourite of a restored space is listed again, because the row is kept (soft delete has no cascade).
- **The point's privacy:**
  - `no-store` is on the 200, 401 and 422 (T9).
  - The header without `sort` gives `invalid_choice` on `near`.
  - The 422 body carries codes only (`toFieldErrors`), never the point.
  - The parsed point lives on `res.locals`, not the request.
  - `requestLogging.ts` redacts `req.headers["masaha-near"]` for every route, and `customProps` adds only
    `userId`, `role` and `spaceId`.
  - The answer carries only `distanceMeters`, rounded to 100 m by `publicListing`, as the directory does. Without
    the point there is no `distanceMeters` (T9's last check).
- **The carried items from #120:**
  - Item 1 is complete. File renamed, factory renamed, `index.ts`, `app.ts`, conventions §7's row and §9's line,
    `data-reports.md`. Only names changed (96 % similarity, one line).
  - Item 2 matches `decideUnder` (lines 120–127: `can()` on the links under the lock comes before `lockIn`). Both
    `data-reports.md` › **Decide** and the contract's admin line now say 403 while the owner is linked, and 409
    once the space is unverified. The owner's line already said 409.
  - Item 3: the sentence moved to the O12 bullet.
  - Item 5: finding 150 is *Accepted*, with the option not taken, and listed under *Accepted* in the index, in the
    format of finding 30.
- **Scope:**
  - 35 files: `apps/api`, `packages/shared`, `docs`, and the web's two `errors.ts` (one line each).
  - No migration, no `package*.json`.
  - Four commits with subjects of 42, 43, 44 and 43 characters, each with a body and no tool attribution.
  - No `#PRNUM` is left; `#121` is where the number goes.
- **Reception idle (#118):** the new routes use the same `requireAuth()`, so `SESSION_IDLE` applies to them
  unchanged.
