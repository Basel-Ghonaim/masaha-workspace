# Review — PR #60, at `ca3d42b`

**Verdict:** No blocker. The temporary password, the guard, the lock order and the revocation hold. Four commit subjects break the project's 50-character rule. Three documented behaviours have no test that would fail if their code broke.

Pinned: `gh pr view 60` gives head `ca3d42b98167fbbced18e976bfbbc15a92033b66` and base `b66ddfe`. CI is green and GitHub shows CLEAN. I read only commit objects (`git show`, `git diff b66ddfe...ca3d42b`). I ran the review from `masaha-b`, not the main folder. Both folders share one object store, so the content read is the same.

## Findings

### 1. should-fix — four commit subjects are over 50 characters
- **Where:** the commit subjects:
  - `af24445` "feat(space-links): add an owner with a temporary password" is **57** characters.
  - `ca3d42b` "refactor(api): read the signed-in claims from shared/auth" is **57**.
  - `d84f500` "feat(space-links): link and unlink the admin's owners" is **53**.
  - `49bdb41` "feat(users): record a temporary password's handover" is **51**.
  - `3e28cce` and `2c0b1b6` are 47 each, within the limit.
- **Scenario:** the project rule caps a subject at 50 characters.
- **Fix:** reword the four subjects, for example:
  - "feat(space-links): add an owner, temp password" (46)
  - "refactor(api): use shared/auth's signedIn" (41)
  - "feat(space-links): link and unlink owners" (41)
  - "feat(users): record a password handover" (39)

  Then force-push with lease.

### 2. should-fix — the users list's total under a filter is never asserted
- **Where:** `apps/api/src/modules/users/users.repository.ts:98` (`db.user.count({ where })`). The tests are `apps/api/src/modules/space-links/admin-users/adminUsers.api.test.ts:165-207`.
- **Scenario:** change the count to `db.user.count()`, without `where`. Every test still passes:
  - the paging test checks `totalRecords: 21` with no filter;
  - the filter tests check only `names(rows)`, never `meta`.

  `GET /admin/users?role=owner` would then report every account's total and the wrong `totalPages`. The contract says "every filter applies before the page is cut".
- **Fix:** in the filter test, also assert `meta.totalRecords`, at least for `?role=user&state=active`.

### 3. should-fix — the documented order of the add refusals is untested without `upgradeExisting`
- **Where:** `apps/api/src/modules/space-links/admin-owners/adminOwners.service.ts:120-127`. The tests are `adminOwners.api.test.ts:505-533`.
- **Scenario:** the contract (§5, `POST /admin/owners`) gives an order: `ACCOUNT_IS_ADMIN` → `ACCOUNT_SUSPENDED` → `ALREADY_OWNER` → `EMAIL_HAS_ACCOUNT` → `RECEPTION_LINK_ACTIVE`. Every refusal test sends `upgradeExisting: true`.
  - If the `!upgradeExisting` check moves above `assertMayOwn`, all tests still pass. An admin's, a suspended account's or an owner's email sent without the flag would then answer `EMAIL_HAS_ACCOUNT`.
  - In that case the admin's dialog would offer an upgrade that can only be refused next.
- **Fix:** run the same three cases without the flag and expect the same codes. Also add one case: the space's active reception without the flag answers `EMAIL_HAS_ACCOUNT`.

### 4. should-fix — the concurrent-creation branch has no test
- **Where:** `adminOwners.service.ts:154-157` (`if (!account) throw … EMAIL_HAS_ACCOUNT`).
- **Scenario:** delete the branch. `account.id` then throws a `TypeError`, and the API answers 500. No test fails. The contract documents this case ("also when another creation took the email meanwhile").
- **Fix:** interleave it the way the lock tests do:
  1. A test transaction inserts `nour@example.com`, uncommitted.
  2. Start `add(NEW)` and wait (`aWhile`). Its `findByEmail` sees nothing, and its insert waits on the unique index.
  3. Commit. Expect 409 `EMAIL_HAS_ACCOUNT`, no link and no audit entry.

### 5. nit — the log test would pass without the new redaction entry
- **Where:** `apps/api/src/shared/http/requestLogging.ts:20` (`'temporaryPassword'`). The test is `adminOwners.api.test.ts:442-464`.
- **Scenario:** remove `'temporaryPassword'` from `SECRET_FIELDS`, and the test still passes. pino-http logs no request or response body, so nothing ever carries the field. The test shows that nothing logs the password today. It does not show that the redaction works. That is fine as defence in depth, but `security.md` names the redaction as a guarantee.
- **Fix:** either add a unit test that logs `{ temporaryPassword: 'x' }` through `createLogger` and expects `[Redacted]`, or retitle the API test as what it proves.

### 6. nit (plausible gap) — an owner whose only link is to a deleted space can't be demoted
- **Where:** `space-links.repository.ts:81` counts a soft-deleted space's links, by decision. `adminOwners.service.ts:181` (`lockSpace`) answers 404 for a deleted space. `adminUsers.service.ts:44` leaves the deleted space out of the row.
- **Scenario:**
  1. Owner A's only link is to space S, and the admin deletes S.
  2. A stays `OWNER`, and `GET /admin/users?role=owner` lists A with `spaces: []`.
  3. `DELETE /admin/spaces/S/owners/A` answers 404, and the role change offers only USER or ADMIN (ADR 0009 *Revised*).

  The only way to make A a user is to restore S, unlink A, then delete S again. The decision is recorded in space-links.md and data-model.md, but this consequence and the way out are written nowhere.
- **Fix:** add one sentence to the space-links decision or the contract naming the way out. Alternatively, record a finding for the owner to decide.

### 7. nit — documents the PR left stale
- `docs/features/space-links.md:4` (*Authority*) still lists the uses as "the session, the caller's own list, the space switcher, the admin's spaces list and the links loader". It is missing the users list and the owners.
- `docs/features/space-links.md:107` (*Shared* code map) says "the caller's spaces, the admin's list query and its rows". It is missing:
  - the users query;
  - `addOwnerSchema` and `linkOwnerSchema`;
  - `AddedOwner` and `AdminUserRow`.
- `docs/features/users.md:72` (*Shared* code map) doesn't name `handoverSchema` or `HANDOVER_CHANNELS`.
- `docs/backend/conventions.md:3` (*Built* status) still lists only "the idempotency key's name and the session lock" for §13. The space's lock, now built (§13, line 342), is missing.
- `docs/backend/conventions.md:343` says "A link change always takes the person's row". A new account's add does not take it: it inserts the row. That is harmless, but the sentence is not literally true. Fix: "…every link change of an existing person".

## Checked and fine
- **The temporary password:**
  - It is drawn with `crypto.randomInt`, which has no modulo bias, from 56 symbols × 12 (about 69 bits). It is drawn again until a digit and a letter are present.
  - It is hashed before the transaction and appears in no audit entry (`after` holds name, email, role and `mustChangePassword`), no `AppError` message and no Prisma argument (only the hash is passed).
  - It is answered only on the 201, with `no-store`. An upgrade answers `null`. A replay answers `ALREADY_OWNER`, never the password (finding 49 states this truly).
- **The guard:**
  - Every new route sits under `api.use('/admin', requireAuth(), requireRole('ADMIN'), admin)`. `requireAuth()` refuses a pending change.
  - The four refused callers are tested on all four endpoints and the list.
  - An admin is refused on link and upgrade, and `ownerRoleFor` never changes an admin. A suspended account is refused on both.
- **Locks:**
  - Every link change takes the space (`FOR NO KEY UPDATE`), then the user (`FOR NO KEY UPDATE`), then the tokens.
  - A facts save, hide, delete and restore take only the space. Sign-in, refresh, the password change, the Google link and the handover take only the user. No path takes the user before the space, so I found no deadlock.
  - The foreign-key `FOR KEY SHARE` taken by inserts into `space_managers`, the audit and the sessions does not conflict with `FOR NO KEY UPDATE`.
- **Races:**
  - Two unlinks of one person's last two links: each counts after the other committed, under READ COMMITTED behind the user lock, so the person ends a `USER`.
  - A link against an unlink of the same person: serialized by the user lock.
  - A sign-in or refresh against a role change: both read the role under the user lock, and a session committed first is revoked. The test at `adminOwners.api.test.ts:253` really interleaves.
  - A save against a link, and a read against a save: the tests hold the lock, and each would fail without its lock or its second read.
- **Revocation:** `changeRole` writes the role, then `revokeAll`, then the audit, in the caller's transaction. It is called only when `ownerRoleFor` returns a new role, and a link or unlink that leaves the role as it is ends no session (tested).
- **The users list:**
  - It makes three queries in `users`, one for the links and one for the spaces, with no N+1.
  - Deactivated, reception and deleted-space links are left out (tested). An unknown `role` or `state` answers 422 `invalid_choice` (tested).
- **Finding 25:** no controller keeps a local `signedIn`, and `req.auth` is read only by `signedIn`, `requireRole` and `requireAuth`.
- **The loader:** `linksAt(spaceId, tx)` is passed `tx` by `groupEdit` and `space.get`, through `linksUnder`.
- **History:**
  - There is no CR byte in any blob changed by any of the six commits.
  - "#59" appears in no file and no commit message; the only hits are the colour `#593700` and a binary.
  - No conflict markers. `spaceLinks.ts` is whole: `loadSpaceLinks`, `spaceOf` and the types are present, with no duplicate.
- **Module rules:** `users` (L1) imports nothing above it. The repositories are created inside the services, not injected, and there is no `vi.mock`.
- **Docs:**
  - The contract §5 and §6 match the code's codes and statuses.
  - ADR 0009's *Revised* line, findings 43, 25 and 49 and the index sections, data-model and the plan's admin table are as the code does.
  - `OWNER_ALREADY_LINKED` is gone everywhere except its recorded removal.
