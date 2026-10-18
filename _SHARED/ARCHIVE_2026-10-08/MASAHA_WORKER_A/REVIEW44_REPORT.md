# Review — PR #44 at `92d04ba` (base `c9db4d8`)

**Verdict:** ready to merge after five should-fix items: one connection-use bug and four test or document gaps. There are no blockers.

## Findings

1. **should-fix: profile edit reads the thresholds on a second connection inside its transaction.** `apps/api/src/modules/spaces/profile/profile.service.ts:49` and `:67`
   - **Problem:** `view(...)` runs inside `runInTransaction`. `spaceView.ts` calls `platformSettings.stalenessThresholds()` with no `tx`, so each edit holds its transaction's connection while it takes a second one from the pool.
   - **Scenario:** enough concurrent profile edits use up the pool. Each one then waits for a second connection until the interactive-transaction timeout fails it.
   - **Inconsistency:** `create()` avoids this on purpose: `space.service.ts:180` calls `view` after the transaction.
   - **Fix:** return `current` or `updated` from the transaction and call `view` after it, as `create()` does.

2. **should-fix: finding 11's guard can never fail, and the rule it closes has no lasting home.** `apps/api/src/modules/spaces/space/create.api.test.ts:237-256` and `docs/architecture/findings.md` (finding 11)
   - **Problem:** pg 8.23 emits this warning through `nodeUtils.deprecate` (`pg/lib/client.js`), which warns only once per process. The listener is attached only in the file's last `describe`. The creations in `POST /admin/spaces` (from line 76) run first.
   - **Scenario:** nested writes come back. The first creation uses up the single warning while nothing listens, and the guard still passes.
   - **What follows:** the resolution's claim, "`create.api.test.ts` checks that the creation emits no such warning", is not true in practice. The rule ("write one statement at a time"; "no pg major upgrade without checking") now lives only in a resolved finding, and S2b-2's facts are the next nested-write candidate.
   - **Fix:**
     - Attach the listener at file level (a top-level `beforeAll`), or move the guard to its own file.
     - Put the rule in `conventions.md` (§2 or §13), or keep the finding Open.
     - Correct the resolution's wording.

3. **should-fix: the slug race retry (S2) is untested, and its 409 is not in the contract.** `space.service.ts:154-186`; `docs/api/api-contract.md:297`
   - **Untested:** nothing runs creations at once, so removing the retry fails no test.
   - **Undocumented:** the contract lists only `validation` (422) for `POST /admin/spaces`. The `conflict` (409) after three lost races is missing.
   - **Fix:** add an api test that sends several creations with the same `nameEn` together (`Promise.all`) and expects distinct slugs. Document the 409.

4. **should-fix: no test proves "deleting writes nothing in `space_managers`" (S6).** `apps/api/src/modules/spaces/space/space.api.test.ts:259`
   - **Problem:** the test counts link rows. A DELETE that set `deactivatedAt` on the links would still pass. The restore test (`:274-312`) sets `deletedAt` in the database rather than through `DELETE`.
   - **Fix:** after `DELETE`, assert the link is unchanged (`deactivatedAt: null`). Or run DELETE, then restore, through the API and check the user's spaces.

5. **should-fix: "nothing written when the defaults are invalid" is untested.** `create.api.test.ts:178-185`
   - **Problem:** only a missing `newSpaceDefaults` row is covered. The invalid branch (`SETTING_KEYS[key].parse`) is not.
   - **Fix:** store a value that fails its schema, then assert a 500 and `{ spaces: 0, settings: 0, audit: 0 }`.

6. **nit: a 500 after the creation commits.** `space.service.ts:180`
   - **Problem:** `view()` reads the staleness thresholds after the commit.
   - **Scenario:** an unreadable `stalenessDays` gives a 500 for a space that exists. A retry then creates `focus-hub-2`.
   - **Fix:** read the thresholds inside the transaction, with `tx`, before the insert. Keep the reads sequential.

7. **nit: the links loader returns a deleted space's links.** `space-links.service.ts:50` and `space-links.repository.ts:29`
   - **Today:** harmless, because every admin handler answers 404 for a deleted space.
   - **Risk:** when the owner guard on `/manage/spaces/:spaceId` reuses this loader, managers of a deleted space would pass it.
   - **Fix:** return `[]` for a deleted space, or record this as a condition on the guard's slice.

8. **nit: tests duplicated across lanes (testing.md §1).**
   - `adminSpaces.api.test.ts:164-177` repeats `adminSpaces.mapper.unit.test.ts:34-40`.
   - `requests.unit.test.ts:69-73` repeats `:42-46`: the same `location` schema via `.partial()`.
   - **Fix:** drop the copies.

9. **nit: an extra query when no listed space has an owner.** `adminSpaces.service.ts:41`
   - **Problem:** `users.namesFor([])` still runs.
   - **Fix:** skip the call when `links` is empty.

10. **nit: finding 18 is marked resolved one commit before restore exists.** The resolution in `8c2ee31` says "a restored space has its links again", but restore lands in `92d04ba`. It is true at the PR head.

11. **nit: the contract's slug length is ambiguous.** It says "at most 60 characters", but 60 is the base before the suffix (`slug.ts:6`). Say "the base, at most 60 characters, then the suffix".

## Verified OK

**Security, data and correctness (subagent 1):**
- **Mounting:** every `/admin/spaces*` route sits under `api.use('/admin', requireAuth(), requireRole('ADMIN'), admin)`. The non-refusing loader is mounted only at `/admin/spaces/:spaceId`, and a non-numeric id gets 404.
- **Profile edit:** order is lock, then 404 if deleted, then `can('space.profile.update')` (403 if verified). Hide, delete and restore work on any space. `spaces` never imports `space-links`.
- **`GET /lookups`:** active rows only, in order; no `isActive` or `sortOrder` in the response.
- **Migration:** fills missing `name_en` from the slug before `NOT NULL`; `name_ar` nullable; two nullable landmark columns; nothing else in the schema changed.
- **Creation:**
  - One transaction with flat, sequential writes.
  - Missing defaults throw before any write.
  - The slug is counted over every row, deleted spaces included.
  - The retry catches only `SlugTaken` (P2002 on `spaces_slug_key`), reruns the whole transaction, and stops at 3.
  - The area must be active, in an active governorate.
  - The Gaza box is a pure shared helper (`out_of_range`).
- **Admin list:** filters apply before skip/take and the count; the verified ids are resolved first; verified and unverified exclude hidden spaces; one cut-off serves both the row and the filter; one query per module; search is `contains`, case-insensitive, and safe with a null `name_ar`.
- **Finding 18:** the session's links and `mySpaces` drop deleted spaces, and `space_managers` is untouched.
- **Idempotency and audit:** hide, delete and restore are idempotent under a row lock and audited in the same transaction, with the right actor and `spaceId` and no secrets.
- **`paragraphSchema`:** relaxes only `\n`.
- **Levels and dependencies:** R3 respected; each service creates its own repository; no test-only parameters.

**Tests, contract, documents and commits (subagent 2):**
- **Actor coverage (testing.md §4):** all six actors on the five per-space endpoints and on `GET /admin/spaces`. `POST` covers all but "owner of this space", which cannot apply to a creation. `/lookups` is tested as a guest and as a USER.
- **Decisions:** S1, S3, S4, S5, S7 and S8 each have a test that would fail if broken, and so do restore, `paragraphSchema`, `lastUpdate` and finding 36. S2's derivation and suffix are covered; its race is not (finding 3).
- **Contract:** paths, bodies, statuses, shapes, error codes and the §4 exception match the code, apart from findings 3 and 11.
- **Documents:** the data-model name rule, the localisation rule, the status lines, v1-mvp's Built lines and finding 36 claim nothing beyond what is built.
- **Web change:** minimal. `choiceOf` falls back to `nameEn` with `lang="en" dir="ltr"`.
- **Commits:** six, Conventional, subjects 42–46 characters, no tool attribution, each a complete unit.

**Tokens:** about 360,000 in total. Subagent 1 used about 142,000, subagent 2 about 160,000, and this conversation about 60,000.
