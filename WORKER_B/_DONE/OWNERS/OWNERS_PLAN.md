# OWNERS — the admin's owner accounts and their links to spaces (API)

Worker B · `masaha-b` · branch `feat/admin-owners` from `origin/main` (`b66ddfe`) · DBs `masaha_b_dev` / `masaha_b_test` · API 3321.

## 1. Summary

The first half of build-map step 4, on the API only. The admin:
- **adds an owner**: a new account with a temporary password, shown once, or an existing account upgraded on purpose. Either way it is linked to one space, which becomes verified, all in one transaction;
- **links** more spaces, one per call, and **unlinks**. Unlinking deactivates the link;
- **reads the users list** (`GET /admin/users`); the owners page is `role=owner`;
- **records how a temporary password was handed over**.

The global `OWNER` role follows the active owner links. Each change of it ends the person's sessions.

Finding 43 is folded:
- every link change takes the space's lock;
- a fact save re-reads the links under that lock;
- the space's read is consistent.

No schema change and no new dependency.

## 2. Contract

**Scope.** These endpoints, with their payloads and errors:
- `POST /admin/owners`;
- `POST /admin/spaces/:spaceId/owners`;
- `DELETE /admin/spaces/:spaceId/owners/:userId`;
- `GET /admin/users`;
- `POST /admin/users/:userId/temporary-password/handover`.

It also covers:
- the role rule and its revocation;
- finding 43;
- the new domain codes, each with its two catalogue lines;
- the documents of §7 of the prompt.

**Acceptance criteria.** Each one is proven by a test in §9.
- [ ] Adding a new email creates an `OWNER` with `mustChangePassword`, links it, and verifies the space. It answers the temporary password once, under `Cache-Control: no-store`.
- [ ] The temporary password is in no audit entry, no log line and no error.
- [ ] An email that already has an account is refused with `EMAIL_HAS_ACCOUNT`. With `upgradeExisting: true` it is upgraded instead: its name and password are kept, there is no temporary password, and its sessions end.
- [ ] The add and link refusals of D5 each have their own answer, and nothing is written.
- [ ] Linking a `USER` makes them an `OWNER` and ends their sessions. Linking an owner to one more space changes no role and ends no session.
- [ ] Unlinking deactivates the link. Unlinking the last link leaves the space unverified, and the person a `USER` with their sessions ended. Unlinking one of two links changes neither.
- [ ] `GET /admin/users` is paged (20), with `q`, `role` and `state`. Each row carries its active owner links, and a soft-deleted space is left out.
- [ ] The handover is audited, and only while a temporary password is pending.
- [ ] Finding 43 is resolved by both of its halves, each race proven with its lock removed once.
- [ ] Every new endpoint is tested as guest, USER, OWNER, ADMIN with a pending change, and ADMIN.

**Out of scope:**
- suspension, `PATCH /admin/users` (the role change) and the admin's temporary password (`POST /admin/users/:userId/temporary-password`): the users item;
- reception links (step 6);
- `status=deleted` on `GET /admin/spaces` (finding 44);
- any web screen.

## 3. Reading done

- **Bootstrap and workflow:** CLAUDE.md, workflow, the map, and the findings index (43, 25, 39 and 20 opened).
- **Capability documents:** space-links.md, users.md, spaces.md › *Decisions* and *Read and edit*, and auth.md (the session's links).
- **The design decisions:** DECISIONS_ADMIN A4, A5 and A6, and *Rules changed*.
- **ADRs:** 0002, 0009, 0013 and 0015.
- **security.md:** Tokens and cookies, Passwords and Authorization.
- **conventions:** §2, §4–§8 (Space access, Transactions), §9 *Composed reads*, and §10–§13.
- **api-contract:** §1–§6.
- **data-model:** Spaces, Users and sessions, Derived values and Constraints.
- **Other documents:** testing §1–§4; v1-mvp step 4 and *Planned API surface*; shared-package.md; localisation › Catalogues; glossary (Owner is صاحب المساحة).
- **Code:**
  - `groupEdit.ts`, `space.service.ts` and `space.repository.ts` (its lock);
  - the whole `space-links` and `users` modules;
  - `shared/auth` (`can`, `loadSpaceLinks`, `requireAuth`, `requireRole`);
  - `shared/audit`, `db/transaction.ts`, `app.ts` and `requestLogging.ts`;
  - `test/admin.ts` and `test/app.ts`, and the lock-holding test in `prices.api.test.ts`;
  - `packages/shared` `core/errors.ts`, `space-links` and `users`.
- **Design:** frames 44/01 and 44/05, and 46/01 (the users list's columns).

## 4. Settled decisions, as they will be built

**D1/D2 — adding an owner: `POST /admin/owners`.**
- **Body:** `{ name, email, spaceId, upgradeExisting? }`. The name is 1–100 characters, as at registration; the email is normalised by `emailSchema`.
- **How it runs:** the email is read first, outside the transaction.
  - **A new email:** `users` generates the temporary password and hashes it, before any transaction. Then, in one transaction:
    1. lock the space;
    2. create the account (`OWNER`, `mustChangePassword`);
    3. link it;
    4. audit `user.created` and `space.ownerLinked`.
  - **An existing email:** each refusal below is checked in order, under the space's lock and then the user's. Then the link is made and the role follows the links (D7).
- **201:** `{ userId, temporaryPassword: string | null }`, with `null` for an upgrade, and `Cache-Control: no-store`.
- **The flag allows an upgrade but does not require one.** With `upgradeExisting: true` and a new email, the account is created.
- **A concurrent creation that took the email** answers `EMAIL_HAS_ACCOUNT`. Sending it again resolves it.
- **The refusal order for an existing email:**
  1. `ACCOUNT_IS_ADMIN`;
  2. `ACCOUNT_SUSPENDED` (an existing code, here as a 409);
  3. `ALREADY_OWNER`;
  4. without the flag, `EMAIL_HAS_ACCOUNT`;
  5. `RECEPTION_LINK_ACTIVE`.
- **The temporary password:**
  - 12 characters from Node's `crypto.randomInt`, over an alphabet without look-alikes (no `0 O 1 l I`), about 69 bits;
  - redrawn until it passes the shared policy (`passwordRules`);
  - a pure `users/temporaryPassword.ts`.

**D3 — the handover: `POST /admin/users/:userId/temporary-password/handover`.**
- **Body:** `{ channel: "WHATSAPP" | "IN_PERSON" | "OTHER" }` (`HANDOVER_CHANNELS`, `@masaha/shared/users`).
- **204:** audits `user.temporaryPasswordHandedOver` with `after: { channel }`. The entry names the same user as the creation it follows.
- **Refused:**
  - with 409 `TEMPORARY_PASSWORD_NOT_PENDING` unless the account's temporary password is still pending;
  - with 404 for an unknown user.
- **The users item reuses it as is** after `POST /admin/users/:userId/temporary-password`.

**D4 — linking: `POST /admin/spaces/:spaceId/owners`.**
- **Body:** `{ userId }`. The web finds the person through `GET /admin/users`.
- **204.** It runs in one transaction:
  1. lock the space (404 when it is unknown or soft-deleted);
  2. lock the user (422 `errors.userId = ["invalid_choice"]` when unknown);
  3. the refusals: `ACCOUNT_IS_ADMIN`, `ACCOUNT_SUSPENDED`, and `RECEPTION_LINK_ACTIVE` for an active reception link here;
  4. link, or reactivate the row (role set to `OWNER`);
  5. audit `space.ownerLinked` (`after: { userId }`);
  6. the role rule.

**D5** is as listed above.

**D6 — unlinking: `DELETE /admin/spaces/:spaceId/owners/:userId`.**
- **204.** It runs in one transaction:
  1. lock the space (404);
  2. lock the user;
  3. deactivate the active `OWNER` row;
  4. audit `space.ownerUnlinked` (`before: { userId }`);
  5. the role rule.
- **Repeats:** a repeat, or a person with no active owner link here, writes nothing. A reception link is never touched.

**D7 — the role.** Under the user's lock, the person's active `OWNER` rows are counted.
- **The rule:** `ownerRoleFor(role, count)` is a pure helper in `space-links`. It gives `OWNER` when the count is above 0, `USER` at 0, and never touches an `ADMIN`.
- **On a change,** `users.changeRole(account, role, actorId, tx)` runs under the lock the caller took. It updates the role, revokes every refresh token, and audits `user.roleChanged` (`before`/`after: { role }`).
- **Docs:** security.md's revocation line, ADR 0009's *Revised* line, and the plan's `PATCH /admin/users` row ("`USER` or `ADMIN`; `OWNER` follows the links").

**D8 — reading: `GET /admin/users`.**
- **Query:** `?q=&role=&state=&page=&limit=`:
  - `q` is 1–100 characters, part of the name or the email, whatever the case;
  - `role` is `user`, `owner` or `admin`;
  - `state` is `active` or `suspended`.
- **Order:** newest first (`createdAt desc, id desc`).
- **Composed in `space-links` (`admin-users/`)**, one query per module:
  1. `users.page()` filters and pages;
  2. the page's active owner links;
  3. `spaces.summariesFor()`, which drops a soft-deleted space.
- **Each row:** `AdminUserRow = { id, name, email, role, isSuspended, signIn: { password, google }, joinedAt, spaces: { id, nameEn, nameAr }[] }`. The `spaces` are its active owner links, oldest first. See S2 for `signIn` and `joinedAt`.

**D9 — finding 43.**
- **The links under the lock.** `LinksLoader` takes an optional `tx`. The loader puts `linksUnder(tx)` on `LoadedSpace` (`shared/auth`), and the composition root wires it with `spaceLinks.linksAt(spaceId, tx)`. `groupEdit` re-reads the links under the space's lock, and `can()` and `isVerified` decide from them. `spaces` never imports `space-links`, which conventions §8 keeps.
- **The links' writers.** Every link change takes the space's lock (`spaces.lock(spaceId, tx)`, newly exported).
- **The read.** `space.get()` runs in a transaction under the space's lock in share mode (`FOR SHARE`, see S1). It reads the space, its facts and its links (`linksUnder`) there.

**The lock order, written into conventions §13.**
- **A link change** locks the space's row, then the user's row. The user's row is the session lock, through `users.lockAccount`.
- **A facts save** takes the space's row only. A refresh or a sign-in takes the user's row and reads the links without a lock. So there is no cycle.

## 5. Stronger decisions

- **S1 — The read is consistent through the space's share lock, rather than a repeatable-read snapshot (D9).**
  - *Why:*
    - every writer of a space's facts and links takes that lock, so no save commits between the read's statements;
    - it keeps ADR 0015's "read committed, row locks", with no second isolation level;
    - only a lock can be proven in the API lane: a test holds a save open, and the read must answer its whole result. A snapshot has no deterministic test.
  - *Cost:*
    - a read waits behind a save in progress (milliseconds);
    - a future writer of the space's facts must take the lock. Conventions §13 says so.
  - *Recommend:* yes.
- **S2 — The rows add `joinedAt` and `signIn` (password and Google).**
  - *Why:* the users screen (46/01) shows both, and AD-021 disables the temporary password for a Google-only account. D8 says the users item adds actions only.
  - *Cost:* two fields. *Recommend:* yes.
- **S3 — Linking an owner already actively linked here answers 204 and writes nothing.** The unused placeholder `OWNER_ALREADY_LINKED` is removed (core, both catalogues, contract §6).
  - *Why:* a link change is idempotent by design (ADR 0015 decision 2), so a retry after a lost answer succeeds. No endpoint would ever send the placeholder.
  - *Cost:* four lines removed. *Recommend:* yes.
- **S4 — `POST /admin/owners` answers an unknown or soft-deleted `spaceId` with 422 `errors.spaceId = ["invalid_choice"]`, not 404.**
  - *Why:* the id is a body field, as `areaId` is answered when a space is created. The web shows it on its field. The path routes keep the 404.
  - *Cost:* none. *Recommend:* yes.
- **S5 — Every link change takes the user's lock, not only when the role changes.**
  - *Why:* whether the role changes is known only once the links are counted under that lock. Two unlinks of one person at once would otherwise each see the other's link, and leave an `OWNER` with no links.
  - *Cost:* an unlink waits behind that user's sign-in (milliseconds). *Recommend:* yes, as the prompt's lock order requires.
- **S6 — The role counts active `OWNER` rows whether or not their space is soft-deleted.**
  - *Why:* deleting a space writes nothing in its links and stays reversible. A role that followed deletion would end sessions on a delete and on a restore.
  - *Cost:* someone linked only to deleted spaces stays labelled `OWNER`. The label grants nothing (ADR 0009 rule 1). *Recommend:* yes, written into data-model.
- **S7 — Defences for the temporary password.**
  - The creation's answer carries `Cache-Control: no-store`.
  - `temporaryPassword` joins the logger's redacted fields, although bodies are never logged.
  - The handover is refused unless a temporary password is pending.
  - *Cost:* small. *Recommend:* yes.
- **S8 — Fold finding 25** (the signed-in helper written twice). This item edits `users.controller.ts`. Its copy and `space-links.controller.ts`' are replaced by `shared/auth`'s `signedIn`.
  - *Cost:* about 10 lines in one more file. *Recommend:* yes.

No rule of the documents is weakened. ADR 0015 decision 5 is kept by S1.

## 6. Related findings

- **43:** folded (D9), and resolved in the commit that adds linking.
- **25:** fold proposed (S8).
- **39** (the users service's test-only `passwords` parameter): not folded. Its refactor of the unit test into helpers and API tests is separate work. New users code takes no such parameter.
- **20 and 21** (session lifetime and grace): untouched.
- **New finding 49:** "A lost answer to adding an owner loses its temporary password". A retry answers `ALREADY_OWNER`, and the person cannot sign in until the admin issues a temporary password (the users item).
- **Number 50:** kept free.

## 7. Files

**API**, all of `apps/api/src`:
- `shared/auth/spaceLinks.ts`: `LinksLoader` with `tx`, and `linksUnder` on `LoadedSpace`;
- `shared/http/requestLogging.ts`: the redacted field;
- `app.ts`: wiring and routers;
- **spaces:**
  - `spaces.service.ts`: `lock`;
  - `space/space.repository.ts`: `lockShared`;
  - `space/space.service.ts`: `get` under the lock;
  - `facts/groupEdit.ts`: the re-read;
- **space-links:**
  - `space-links.service.ts` and `space-links.repository.ts`: `linksAt(spaceId, tx)`, and the link rows' reads and writes;
  - `ownerRole.ts` and `ownerRole.unit.test.ts`;
  - `admin-owners/`: the service, controller and API test (add, link, unlink);
  - `admin-users/`: the service, mapper, controller and API test;
  - `space-links.admin.routes.ts`, `index.ts` and `space-links.controller.ts` (S8);
- **users:**
  - `users.service.ts`: `issueTemporaryPassword`, `createOwnerAccount`, `changeRole`, `page`, `recordHandover`, and the `audit` dependency;
  - `users.repository.ts`, `temporaryPassword.ts` and `temporaryPassword.unit.test.ts`;
  - `users.admin.routes.ts`, `users.controller.ts`, `index.ts`, and `handover.api.test.ts`;
- the race tests in `spaces/hours/hours.api.test.ts` (the save) and `spaces/space/space.api.test.ts` (the read).

**Shared:**
- `packages/shared/src/core/errors.ts`;
- `space-links/requests.ts` and `responses.ts`: `addOwnerSchema`, `linkOwnerSchema`, `adminUsersQuerySchema`, `AddedOwner` and `AdminUserRow`;
- `users/requests.ts`: `handoverSchema` and `HANDOVER_CHANNELS`.

**Web, under the licence of workflow §9:** `apps/web/src/shared/copy/english/errors.ts` and `arabic/errors.ts`. These lines are mine while the PR is open:
- the codes added: `EMAIL_HAS_ACCOUNT`, `ALREADY_OWNER`, `ACCOUNT_IS_ADMIN`, `RECEPTION_LINK_ACTIVE` and `TEMPORARY_PASSWORD_NOT_PENDING`;
- `OWNER_ALREADY_LINKED` removed (S3).

Nothing else in `apps/web`.

**Docs:**
- `api/api-contract.md`: new *Owners (the admin)* and *Users (the admin)* sections, and §6;
- `plans/v1-mvp.md`: its API table;
- `features/space-links.md`, `features/users.md` and `features/spaces.md`;
- `backend/security.md`: status, revocation and *Passwords*;
- `backend/conventions.md`: §8 *Space access* and §13;
- ADR 0009 (*Revised*);
- `architecture/data-model.md`: SpaceManager and User;
- the findings: 43 resolved, 25 resolved (if folded), and 49 new, with the index;
- `project/overview.md`: *Built*.

## 8. Design issues

None: this item builds no screen. For worker A's later screens:
- the creation's answer is the only copy of the password, and the web must keep it in no cache (finding 34's rule);
- a link from a space sends `state=active`, and shows an admin in a page of results as disabled.

## 9. Tests: lane, proof and break

**Unit:**
- `temporaryPassword`: 12 characters, only the alphabet, every draw passing the policy. *Break:* an alphabet or a length change.
- `ownerRoleFor`: USER and 1 give OWNER; OWNER and 0 give USER; OWNER and 2 give nothing; ADMIN gives nothing. *Break:* any branch.
- Catalogue parity (the existing test) covers the new lines.

**API: `POST /admin/owners`.**
- **A new email:** 201, with a password that passes the policy and verifies against the stored hash. The role is `OWNER`, `mustChangePassword` is set, the link is active, and `GET /admin/spaces/:id` says verified. The audit entries are exactly `user.created` (`after` without the password) and `space.ownerLinked`.
- **`Cache-Control: no-store`** is on the answer.
- **The password is in no log line and no audit entry** (a captured logger stream). *Break:* log the body, or audit it.
- **`EMAIL_HAS_ACCOUNT`** writes nothing. **Then the upgrade** answers 201 with a null password, keeps the name and hash, sets the role to `OWNER`, ends the person's refresh tokens, and audits `space.ownerLinked` then `user.roleChanged`.
- **The refusals,** each writing nothing: `ACCOUNT_IS_ADMIN`, `ACCOUNT_SUSPENDED`, `ALREADY_OWNER` and `RECEPTION_LINK_ACTIVE`.
- **An unknown or deleted `spaceId`:** 422 `invalid_choice`, and no account is created (all or nothing). *Break:* create the account before checking the space.
- **Each refused caller,** and ADMIN.

**API: link.**
- A `USER` becomes `OWNER`, with their sessions ended and the space verified.
- An owner linked to a second space keeps the role, and their session token survives.
- A re-link writes nothing.
- A deactivated row is reactivated, and a deactivated reception row becomes `OWNER`.
- **The refusals:** admin, suspended, active reception, an unknown user (422), and a deleted or unknown space (404).
- **The link waits for the space's lock:** a test transaction holds it, and no row appears until it commits. *Break:* drop the lock.
- **A refresh in progress:** a test transaction holds the user's row and adds a refresh token. The link that waited ends that session too. *Break:* change the role without the user's lock.
- **Callers.**

**API: unlink.**
- Unlinking one of two links keeps the role and the session, and the space is unverified when it had no other owner.
- Unlinking the last link makes the person a `USER`, ends their sessions, and leaves the space unverified, with the audit entries in order.
- A repeat, or a reception link, writes nothing.
- A deleted or unknown space answers 404.
- **Two unlinks of one person's two links at once:** a test transaction holds the user's row until both wait, and the person ends as a `USER`. *Break:* count the links before the user's lock.
- **Callers.**

**API: `GET /admin/users`.**
- 20 per page, with its meta, newest first.
- `q` on the name and on the email, whatever the case.
- `role` and `state`.
- Each row's `spaces`: only active `OWNER` links, oldest first, without a deleted space's, a reception link or a deactivated link.
- `signIn` and `joinedAt`.
- An unknown `role` is 422 `invalid_choice`.
- **Callers.**

**API: the handover.**
- 204 and its audit entry.
- 409 `TEMPORARY_PASSWORD_NOT_PENDING`, 404 for an unknown user, and 422 for an unknown channel.
- **Callers.**

**API: finding 43.**
- **The save:** a test transaction locks the space and commits an owner link, while an admin's hours save waits behind it. The save answers 403 and writes nothing. *Break:* use the loader's links instead of `linksUnder`.
- **The read:** a test transaction holds the lock and changes both the days and the shifts. `GET /admin/spaces/:id` answers them both new once it commits. *Break:* drop the share lock, and the old state is answered.

## 10. Review Focus (no planned test)

- Two creations of the same new email at once: the database's unique key decides, and the loser answers `EMAIL_HAS_ACCOUNT`.
- Two first links of one `USER` at once: only the first changes the role, by the same lock as the unlink race.
- Deadlocks under real concurrency beyond the deterministic orders tested. The order argument is in §4.
- `%` and `_` in `q`, as Prisma's `contains` treats them (the same as the spaces list).
- A handover recorded twice: two entries, accepted.
- A role whose remaining links are all to deleted spaces (S6).

## 11. Commits

1. `fix(spaces): decide on the links under the lock`: D9's re-read and the share-locked read, with their race tests; conventions §8 and §13; spaces.md.
2. `feat(space-links): list the users for the admin`: `GET /admin/users`, `users.page`, the shared schemas, the contract, space-links.md, users.md, and the plan's table.
3. `feat(space-links): link and unlink the admin's owners`: link and unlink, `ownerRoleFor`, `users.changeRole`, `ACCOUNT_IS_ADMIN`, `RECEPTION_LINK_ACTIVE` and the S3 removal; security.md's revocation, ADR 0009, data-model, and finding 43 resolved.
4. `feat(space-links): add an owner with a temporary password`: `POST /admin/owners`, `temporaryPassword`, `EMAIL_HAS_ACCOUNT` and `ALREADY_OWNER`, the redaction, `no-store`, security *Passwords*, and finding 49.
5. `feat(users): record a temporary password's handover`: the handover, `TEMPORARY_PASSWORD_NOT_PENDING`, and overview *Built*.
6. `refactor(api): read the signed-in claims from shared/auth` (finding 25, if folded).

Each commit carries its code, tests and documents. Lint and typecheck run on each.

**PR:**
- title `feat(space-links): add the admin's owners`;
- labels `feat`, `area:api`, `area:docs` and `area:web`;
- assigned to the owner;
- the new codes listed with their English and Arabic text, the Arabic marked as needing the owner's approval.

## 12. Verification (phase 4)

**Once each on the head, one at a time:**
- `test:unit`, `test:component` and `test:api` (on `masaha_b_test`);
- `NODE_ENV=production npm run build`, then `check:build`;
- `lint`, `typecheck`, `check:classes`, `format:check` and `check:links`.

**Real requests against the API on 3321 (`masaha_b_dev`, the seeded admin),** each written into the report:
1. Add a new owner with a space: the space becomes verified, and the password is shown once. Then record its handover.
2. The `EMAIL_HAS_ACCOUNT` refusal, then the upgrade.
3. Link a plain user from a space: they become an owner.
4. Link one more space, then unlink one of the two: the role stays.
5. Unlink the last: the role and the verification go.
6. `GET /admin/users?role=owner&q=…`.

The server is stopped afterwards, and port 3321 checked free.

**Not run:**
- the web dev server, since no screen changes;
- E2E, which waits for the end of the project.

## 13. Decisions needed from the owner

1. **S1:** the share lock instead of a snapshot for the space's read.
2. **S2:** `joinedAt` and `signIn` in the users rows.
3. **S3:** an idempotent re-link, and removing `OWNER_ALREADY_LINKED`.
4. **S4:** 422 `invalid_choice` for the body's `spaceId`.
5. **S8:** fold finding 25.
6. **The new codes' names:**
   - `EMAIL_HAS_ACCOUNT`;
   - `ALREADY_OWNER`;
   - `ACCOUNT_IS_ADMIN`;
   - `RECEPTION_LINK_ACTIVE`;
   - `TEMPORARY_PASSWORD_NOT_PENDING`;
   - and `ACCOUNT_SUSPENDED` reused for the 409.

   Their Arabic text is approved in the PR.
7. **The handover's path** (`/admin/users/:userId/temporary-password/handover`), and its payload `{ channel }`.

## 14. The owner's reply (2026-10-11): approved, with one addition

- **Decisions §13:**
  - S1 (the share lock, its rule for future writers written into conventions §13), S2, S3, S4, S8 (finding 25, as its own last commit), the codes, `ACCOUNT_SUSPENDED` reused as the 409, and the handover's path and payload: all approved.
  - S5, S6 and S7 approved as written.
  - Finding 49 approved; 50 stays free.
- **Addition, to D4:** when a link reactivates a deactivated `RECEPTION` row as `OWNER`, its `space.ownerLinked` entry carries `before: { role: "RECEPTION" }`, so the space's log shows that the person's role there changed. One API test proves it, in commit 3.
- **Reminders:**
  - every new endpoint tested as guest, USER, OWNER, ADMIN with a pending change, and ADMIN;
  - each race with its lock removed once;
  - `git merge-tree --write-tree` against every other open PR at the report;
  - an independent review follows; no merge.
