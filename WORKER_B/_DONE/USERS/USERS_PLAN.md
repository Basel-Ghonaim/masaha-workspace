# USERS — the admin's actions on accounts: suspension, role, temporary password (API) — Plan

Worker B · worktree `C:\Users\basel\masaha-b` · branch `feat/admin-users`, cut with
`git switch --no-track -c feat/admin-users origin/main` once the plan is approved · databases
`masaha_b_dev` / `masaha_b_test` · API 3321, web 5321. Base: `d7d800e` (#60 merged), checked equal to
`origin/main` after `git fetch --prune origin`, tree clean.

## 1. Summary

The second half of build step 4, on the API only. The admin suspends and restores an account
(`PUT /admin/users/:userId/suspended`), changes a person's role between `USER` and `ADMIN`
(`PUT /admin/users/:userId/role`), and issues a temporary password
(`POST /admin/users/:userId/temporary-password`), whose handover goes through #60's route. The platform
never loses its last active admin, under one lock. `requireAuth` reads the account on every signed-in
request, so a suspension, a demotion, a promotion or a pending password change takes effect on the
next request (ADR 0003 revised). Four new 409 codes, with their catalogue lines in the web. First, in a
commit of its own, the workflow rule D7.

## 2. The contract

**Scope**
- D7: workflow §9 *Merging* gains the "merge apart" rule; `open-pr` step 3 a few words.
- D5: `requireAuth` reads the account by id on every signed-in request; the token stops carrying the
  role.
- D1, D2, D4: suspension and restore, idempotent, audited, ending sessions, under the admin-set lock.
- D1, D2, D3: the role change, `USER` ↔ `ADMIN`, idempotent, audited, ending sessions.
- D6: the admin's temporary password, answered once, ending sessions and reset links; finding 49.
- The documents the prompt lists (§7 below), the four codes' catalogue lines.

**Acceptance criteria**
- [ ] A suspended account's unexpired access token is refused (401) on its next request, `/me/password` included; its refresh tokens are gone; its links and its space's verified state are kept.
- [ ] A demoted admin's next `/admin` request is refused (403); a promoted user's next one passes, with the old token.
- [ ] A temporary password issued after a token was signed makes that token answer `PASSWORD_CHANGE_REQUIRED` everywhere but `/me/password`.
- [ ] An unknown id in a valid token is 401.
- [ ] Suspending, restoring, promoting, demoting: the same state again writes nothing and ends no session.
- [ ] An admin cannot suspend, change the role of, or issue a temporary password to themselves (`OWN_ACCOUNT`).
- [ ] Two admins demoting or suspending each other at once: one succeeds, the other answers `LAST_ADMIN`; at least one active admin remains (proven with the lock removed).
- [ ] Promoting a person with any active link (owner or reception, a deleted space's included) is refused (`ACCOUNT_HAS_LINKS`); so is setting `USER` on an `OWNER`.
- [ ] A role change racing a link: never an admin with a link (both directions, proven with the lock removed).
- [ ] A suspension racing a sign-in, a refresh or a password change: no session survives (proven with the lock removed).
- [ ] The temporary password: 200 `{ temporaryPassword }`, `no-store`, `mustChangePassword`, every session and reset link ended, audited without it, in no log line; again replaces the pending one; refused for oneself, a suspended account (`ACCOUNT_SUSPENDED`), a Google-only account (`GOOGLE_ONLY_ACCOUNT`); its handover recorded through #60's route; a sign-in with it is forced to change.
- [ ] Every new route refuses guest, USER, OWNER and a pending ADMIN as `/admin` does.
- [ ] The documents of §7 updated; finding 49 resolved; finding 51 recorded.

**Out of scope**
- A3's `status=deleted` filter (finding 44); the screens 27 and 29 (worker A, later); `GET`/`PATCH /me`;
  reception accounts and the owner's temporary passwords (step 6); any schema change; finding 39 (§6).

## 3. Reading done

CLAUDE.md; workflow (all); the map; the findings index, and the files of 39, 49 (and 50, 20, 21, 23 by
title). `users.md` (all), `space-links.md` (all), `auth.md` (all). ADR 0003, 0009, 0013, 0015.
`security.md` (all). Conventions §4, §6, §7, §8, §13. Contract §1–§4, §5 (Session, Me, Spaces (the
admin) for the `hidden` route's style, Owners, Users), §6. Data model › *Users and sessions*. Testing
§1–§5. `shared-package.md`. `DECISIONS_ADMIN.md` › A3–A7, AD-021. Screens `46-admin-users/` 03, 05, 07.
Plan v1-mvp › step 4 and the admin API table; overview › *Built*. The code: `shared/auth/*`,
`app.ts` (composition), `shared/http/requestLogging.ts`, the `users` module (service, repository,
routes, controller, mapper, temporary password, unit and API tests), `space-links`' `ownerRole.ts`,
`admin-owners/`, admin routes, `auth.service.ts` (sign-in, refresh, reset), `sessions.service.ts`,
`sessionLock.api.test.ts`, `test/admin.ts`, `test/app.ts`, the web's `refreshOn401.ts` and
`refresh.ts`, the web's error catalogue, `.github/workflows/ci.yml`.

## 4. The settled decisions, as they will be built

### D7 — the workflow rule (commit 1, alone)
- Workflow §9 *Merging* gains one item: *a merge into `main` that deletes or renames no file and
  changes none of the PR's files needs no rebase and no new CI run: the PR stays ready. Checked with
  `git diff --name-status <old main> <new main>`.* The existing item ("whose CI ran after main's last
  change") gains "or after a merge apart (above)".
- `open-pr` step 3: "… when GitHub shows a conflict; a merge apart needs no new run ([§9](…))".
- `docs(workflow): a merge apart needs no new CI run`, body: the rule decides how every worker treats
  an open PR when another merges meanwhile (#60 after #59). Checks: `format:check`, `check:links`.

### D5 — the guard reads the account (revises ADR 0003)
- **`requireAuth` takes an account reader**, as `loadSpaceLinks` takes a links loader: `shared/`
  imports no module (R6), so the composition root wires `users.signedInAccount` into
  `createRequireAuth(tokens, readAccount)`. The reader is one `findUnique` by primary key with the
  account's small select: `{ role, mustChangePassword, suspended }`, or nothing.
- **The guard, in order:** no valid token → 401; no account for its id (deleted, unknown, another
  environment's token) → 401; a suspended account → **401, no code**; a pending change → 403
  `PASSWORD_CHANGE_REQUIRED` unless the route allows it. Pending means **the token's claim or the
  account** says so (S1).
- **What the token still carries:** `sub` and `mustChangePassword`. The `role` claim goes (S2): the
  server reads the role from the account, and the web never decodes the token (checked: no decoding
  in `apps/web`). `mustChangePassword` stays because it is the half of the forced change's double
  check that a token alone carries: it says this session was opened with the temporary password. A
  temporary password issued after the token (D6) is in the account only, so the old token is refused
  everywhere but `/me/password`, and there the current password is required.
- **`req.auth` becomes `SignedIn`**: `{ userId, role, tokenPendingChange }` — `role` the account's now,
  `tokenPendingChange` the token's claim (renamed so no reader mistakes it for the account's flag).
  `signedIn(req)` returns it; `requireRole` and `can()` (through the spaces controllers' `role`) read
  the stored role; the request log's `role` too; `changePassword` passes `tokenPendingChange`.
- **The answer for a suspended account: 401.** The web's transport refreshes on any 401; the refresh
  fails (the suspension deleted every refresh token) and the session ends at once. A 403
  `ACCOUNT_SUSPENDED` here would leave the web signed in with a failing page until the token expired.
  The reason shows at the next sign-in (`ACCOUNT_SUSPENDED`, 403, as today). **No contract change the
  web must follow:** `Session` and the refresh's answer are unchanged; the token is opaque to the web.
- **Cost:** one primary-key read per signed-in request (the links loader already makes one more on the
  space routes). Locally sub-millisecond; online one round trip to Neon of the size the request
  already makes. Not measured: no test can prove a latency.
- **What stays on the token alone:** the general rate limit, which reads only the token's `sub`
  (before the guard), unchanged.
- **ADR 0003** gains `> **Revised:** 2026-10-11 — the guard reads the account by id on every signed-in
  request, so a suspension or a role change takes effect at once; the access token carries who, and
  whether a temporary password was pending.` **security.md › Tokens and cookies** states the claims and
  the guard; *Authorization* states the reading.

### D1, D2, D4 — suspension and restore (`users`, L1)
- `PUT /admin/users/:userId/suspended`, body `{ isSuspended: boolean }` (S6), 204. In the `users`
  admin router, beside the handover.
- **In order:** the actor's own id → 409 `OWN_ACCOUNT` (before any lock); then one transaction: the
  admin-set lock (below); an unknown id → 404; the same state → nothing; suspending an active admin
  with no other active admin → 409 `LAST_ADMIN`; then the write.
- **Suspend:** `suspendedAt = now`, every session ended, every pending reset link ended (S5), audited
  `user.suspended` (`before: { isSuspended: false }`, `after: { isSuspended: true }`), the person as the
  entity. **Restore:** `suspendedAt = null`, audited `user.unsuspended` (the reverse); it ends nothing.
- **D4:** the links are untouched: a suspended owner's space stays verified, so the admin edits it only
  after unlinking them. Written in security.md › *Authorization* and space-links.md › *Behaviour*.
- **A password change racing a suspension (S4):** `changePassword` now takes the session lock and
  checks `maySignIn` inside its transaction, before its compare-and-set; today a change whose access
  token passed the guard before a suspension committed could open a new session for the suspended
  account.

### D2 — the admin-set lock (settled)
- **One statement in `users`' repository, `lockWithActiveAdmins(id, tx)`:**
  `SELECT id, role, suspended_at FROM users WHERE id = $id OR (role = 'ADMIN' AND suspended_at IS NULL)
  ORDER BY id FOR NO KEY UPDATE`. It takes the target's session lock and every active admin's row, by
  id (conventions §13: one fixed order). Under read committed, a row a concurrent change demoted or
  suspended is re-checked when its lock is granted and drops out of the set, so the count of the
  *other* active admins is the committed one.
- `users.lockForAdminChange(id, tx)` answers `{ account, otherActiveAdmins }` or nothing; suspension
  and the role change both take it first. A temporary password locks the target alone
  (`lockAccount`): it removes no admin.
- **Lock order** (conventions §13, extended): the person's row (with the active admins', by id), then
  their tokens. A role change takes no space lock; a link change takes the space, then the person
  (never an admin), so no two orders cross.
- **A consequence to know:** with the self-refusal, the actor is an active admin other than the target
  when the request starts, so `LAST_ADMIN` is reached only when the actor was demoted or suspended
  meanwhile: the race. In a real run, the last admin trying to demote or suspend is refused
  `OWN_ACCOUNT`. `LAST_ADMIN` is proven in the API lane by the race test.

### D1, D2, D3 — the role change (`space-links`, L2, orchestrator)
- `PUT /admin/users/:userId/role`, body `{ role: "USER" | "ADMIN" }`, 204. It lives in `space-links`,
  because D3 reads the person's links, which `users` (L1) cannot; `users.changeRole` (#60) writes the
  role, ends the sessions and audits `user.roleChanged`. New folder `space-links/admin-roles/`.
- **In order:** own id → 409 `OWN_ACCOUNT`, whatever the role asked; then one transaction:
  `users.lockForAdminChange`; unknown → 404; the same role → nothing; any active link of the person
  (owner or reception, a soft-deleted space's included, as the global role counts it) → 409
  `ACCOUNT_HAS_LINKS` — this refuses promoting a linked user or owner (D3) and setting `USER` on an
  `OWNER`, whose role follows the links (ADR 0009); demoting an active admin with no other active admin
  → 409 `LAST_ADMIN`; then `users.changeRole`. Demoting an admin gives `USER` (an admin has no links).
- A suspended account's role may change: the role and the suspension are independent (Review Focus).

### D6 — the admin's temporary password (`users`)
- `POST /admin/users/:userId/temporary-password`, no body, **200** `IssuedTemporaryPassword =
  { temporaryPassword: string }` (`@masaha/shared/users`), `Cache-Control: no-store`, as #60's add
  answers it.
- **In order:** own id → 409 `OWN_ACCOUNT`; the password generated and hashed before the transaction
  (`users.issueTemporaryPassword`, #60's generator); then one transaction: `lockAccount`; unknown → 404;
  suspended → 409 `ACCOUNT_SUSPENDED` (restore first); no password (Google only, AD-021) → 409
  `GOOGLE_ONLY_ACCOUNT`; then the hash set with `mustChangePassword = true`, every session ended, every
  reset link ended (its recoveries with it, as a reset does), audited `user.temporaryPasswordIssued`
  (`after: { mustChangePassword: true }`), never the password.
- **Again** replaces the pending one (finding 49 resolved). An account with Google and a password gets
  one. Another admin gets one (an admin who lost their email).
- The answer's field is `temporaryPassword`, a key the logger already redacts (#60's unit test,
  `requestLogging.unit.test.ts`); no error or audit entry holds it.

### The four new codes (each through `add-error-code`), all 409 `conflict`
| Code | English | Arabic (needs the owner's approval) |
|---|---|---|
| `OWN_ACCOUNT` | You can’t do this to your own account. | لا يمكنك تنفيذ هذا الإجراء على حسابك. |
| `LAST_ADMIN` | The platform must keep at least one active admin. | يجب أن يبقى على المنصة أدمن نشط واحد على الأقل. |
| `ACCOUNT_HAS_LINKS` | This person is linked to a space, and their role follows those links. Unlink them first. | هذا الشخص مرتبط بمساحة، ودوره يتبع روابطه. فُكّ ربطه أولًا. |
| `GOOGLE_ONLY_ACCOUNT` | This account signs in with Google only, so it has no password to replace. | هذا الحساب يسجّل الدخول باستخدام Google فقط، وليست له كلمة مرور لاستبدالها. |

`ACCOUNT_SUSPENDED` is reused (its text, "This account is suspended.", fits the admin).
`PASSWORD_NOT_SET` is not: its text speaks to the account's holder.

## 5. Stronger decisions

- **S1 — a pending change is refused when the token *or* the account says so.** *Why:* the account
  catches a temporary password issued after the token (D6); the claim keeps today's refusal of a
  token issued while a change was pending. *Cost:* none. **Recommend.**
- **S2 — the access token drops its `role` claim** (D5 asks what the claims carry). *Why:* a claim the
  server no longer reads is an authority that would go stale if anyone read it again. *Cost:* the
  15 test sites that sign tokens drop one field; tokens signed before deploy still verify (an extra
  claim is ignored). **Recommend.**
- **S3 — a suspended account's request answers 401, no code** (D5 asks). *Why:* the web's existing
  401 → refresh → 401 path ends the session at once, with no web change; a 403 would not. *Cost:* the
  reason is not in that answer, only at the next sign-in. **Recommend.**
- **S4 — a password change checks the suspension under the session lock.** *Why:* the only path that
  opens a session without that check (sign-in, Google, refresh already check under it). *Cost:* one
  lock and one check in `changePassword`; one test. **Recommend.**
- **S5 — a suspension also ends the pending reset links** (and the recoveries bound to them). *Why:* a
  suspension ends every way back in; a link sent before it should not outlive it, and after a restore
  the person asks for a new one. *Cost:* one call, one assertion. **Recommend.**
- **S6 — the body is `{ isSuspended }`, not `{ suspended }`.** *Why:* the same name as the users row's
  `isSuspended` and the `hidden` route's `{ isHidden }`. *Cost:* none. **Recommend.**
- **S7 — the self-refusal is one code for the three actions, and refuses any role asked of oneself,**
  `ADMIN` included. *Why:* one rule, as the design shows the admin's own row with no actions ("أنت").
  **Recommend.**
- **Weighed, not recommended:**
  - *Re-checking, under the admin-set lock, that the actor is still an active admin:* it would answer the
    race with 403 rather than `LAST_ADMIN`, but the invariant would then rest on two rules instead of
    being checked where it is broken, and every other admin route reads the role once, at the guard.
  - *A token version* (a stored "sessions ended at" the guard compares with the token's `iat`), so a
    password change or a reset also ends the other devices' access tokens at once: a schema change,
    outside this item. Recorded as **finding 51** (below).
  - *D7 and conflicts across files:* a merge apart can still break the PR through a file it does not
    touch (a renamed export). CI runs on every push to `main`, so it shows there. Keep the owner's
    rule as written.

## 6. Related findings

- **49 — folded** (D6): resolved in commit 5, status and resolution line, index moved.
- **39 — not folded; recommend leaving it to a small item of its own.** This item adds no new use of
  the `passwords` parameter (the temporary password reuses `issueTemporaryPassword`). Folding it means
  removing the parameter and reworking the 11 cases of `users.service.unit.test.ts`, which fakes the
  repository and the sessions too (finding 31's pattern); and the case *"spends a comparison on an
  unknown email"* is proven only through that fake: without it, that sign-in timing property needs a
  new proof (a pure helper choosing the hash to compare, in the sign-in path). Cost: about a
  half-day's change in the sign-in's code, inside a PR already under a security review. The owner
  decides.
- **50 — not folded,** touched: a person whose only owner links are to deleted spaces holds active
  links, so `ACCOUNT_HAS_LINKS` refuses promoting them; the way out stays finding 50's.
- **20, 21, 23 — not folded:** session lifetime and grace (sessions), and the per-address ceiling;
  D5 changes none of them.
- **New: 51 — "An access token outlives the end of its session"** (Open). After a password change or a
  reset, another device's access token works until it expires (15 min): the guard now reads the
  role, the suspension and the pending change, but nothing tells it the sessions ended. *Resolves
  when:* the guard refuses a token issued before the account's sessions last ended (a stored
  timestamp), or the owner accepts it. Recorded in commit 2. Number 52 stays free.

## 7. Files

**API (worker B's layer)**
- `apps/api/src/shared/auth/`: `accessToken.ts` (claims: `userId`, `mustChangePassword`),
  `requireAuth.ts` (reader, `SignedIn`, the order), `signedIn.ts`, `requireRole.ts` (type only),
  `index.ts`; tests `accessToken.unit.test.ts`, `requireAuth.unit.test.ts`, `requireRole.unit.test.ts`;
  new `requireAuth.api.test.ts`.
- `apps/api/src/app.ts`: wire `users.signedInAccount`; mount nothing new (routes live in the routers).
- `apps/api/src/shared/http/requestLogging.ts`: only if the type of `auth` needs it.
- `apps/api/src/modules/users/`: `users.service.ts` (`signedInAccount`, `lockForAdminChange`,
  `setSuspended`, `setTemporaryPassword`, `accessClaims` without the role, `changePassword`'s lock),
  `users.repository.ts` (`lockWithActiveAdmins`, `setSuspendedAt`, `setTemporaryPassword`),
  `users.controller.ts`, `users.admin.routes.ts`, `index.ts`; tests `users.api.test.ts` (the suspended
  case → 401; token signing), `users.service.unit.test.ts` (claims), new `suspension.api.test.ts`,
  new `issueTemporaryPassword.api.test.ts`.
- `apps/api/src/modules/space-links/`: new `admin-roles/adminRoles.service.ts`,
  `adminRoles.controller.ts`, `adminRoles.api.test.ts`; `space-links.repository.ts`
  (`countActiveLinks`); `space-links.admin.routes.ts`; `index.ts`.
- Token-signing test sites (drop `role`): `space-links.api.test.ts`, `spaces/space/space.api.test.ts`,
  `test/admin.ts`, `test/spaces.ts`.
- `packages/shared/src/`: `core/errors.ts` (four codes, in a users group); `users/requests.ts`
  (`setSuspendedSchema`), `users/responses.ts` (`IssuedTemporaryPassword`); `space-links/requests.ts`
  (`changeRoleSchema`, `{ role: z.enum(['USER', 'ADMIN']) }`).

**The web, under workflow §9's licence (declared):** `apps/web/src/shared/copy/english/errors.ts` and
`apps/web/src/shared/copy/arabic/errors.ts`, the four codes' lines only. Worker A keeps out of these two
files while the PR is open. Nothing else in `apps/web`.

**Documents:** `docs/development/workflow.md` §9 and `.claude/skills/open-pr/SKILL.md` (commit 1);
`docs/api/api-contract.md` (the three routes, `/me/password`'s suspended answer, the guard's 401 for a
suspended account in *Session*'s preamble, §6); `docs/plans/v1-mvp.md` (the two rows become built: the
*Built* line); `docs/features/users.md`; `docs/features/space-links.md` (the role change, D3, D4);
`docs/backend/security.md` (Built line, Tokens and cookies, Revocation, Authorization, Passwords ›
*Recovery without the email*); `docs/backend/conventions.md` §13 (the admin-set lock and its order);
`docs/architecture/decisions/0003-session-model.md` (*Revised*); findings 49 and new 51, the index;
`docs/project/overview.md` (*Built*). `data-model.md`: no rule changes (suspension and the role are
already described) — left as is.

## 8. Design issues

None: no screen is built. For the web later (worker A): the change-role dialog (05) shows «مالك» as a
choice; the API takes `USER` or `ADMIN` only (A5), so «مالك» is derived and shown, never chosen. The
temporary-password dialog (07) asks for no reason; the handover follows the shown password (A5).

## 9. Tests: lane, test, the break it catches

All new tests seen failing first; each lock test made to fail once with its lock removed (rule 7).

**Unit**
- `requireAuth.unit.test.ts` (the decision, given a token and a reader's answer): each malformed header
  → 401 without reading (break: read before parsing); no account → 401; suspended → 401 (break: drop
  the check); pending by claim only, and by account only → `PASSWORD_CHANGE_REQUIRED`, both let through
  when allowed (break: `&&` for `||`); `req.auth.role` is the account's, not anything from the token
  (break: role from claims).
- `accessToken.unit.test.ts`: a token carries `sub` and `mustChangePassword`; a token without a valid
  `sub` or flag is refused (updated cases).

**API**
- `requireAuth.api.test.ts` — the account now, per state, through real routes: a suspended account's
  token is 401 on `/manage/spaces`, `/me/password` and `/admin/users` (break: guard without the reader);
  a USER made ADMIN in the database reaches `/admin/users` with the token signed before (break: role
  from the token); an ADMIN made USER is 403 there; a pending change set after the token → 403
  `PASSWORD_CHANGE_REQUIRED`, `/me/password` still reachable; an id with no account → 401.
- `suspension.api.test.ts`: suspends: 204, `suspendedAt` set, refresh tokens and reset links gone,
  `user.suspended` entry; the next request is 401; an owner's link kept and the space verified (D4);
  restores: `user.unsuspended`, sign-in works again; the same state twice writes no entry and ends no
  session (break: no idempotency); `OWN_ACCOUNT`; 404 unknown; 422 bad body; the refused callers.
  **Races:** two admins suspending each other — the test transaction suspends B and holds B's row while
  B's request suspends A → `LAST_ADMIN`, A active (break: lock the target only); a suspension waiting
  on a sign-in — the test holds the row and inserts a refresh token → none survives (break: revoke
  before taking the lock); a password change waiting on a suspension — the test holds the row and
  suspends → the change answers `ACCOUNT_SUSPENDED` and no token exists (break: S4's check removed).
- `adminRoles.api.test.ts`: promotes: role `ADMIN`, sessions ended, `user.roleChanged`; demotes with a
  second admin present; the same role writes nothing (USER, ADMIN, a reception's USER); `OWN_ACCOUNT`
  for any role asked; `ACCOUNT_HAS_LINKS` for an owner link, a reception link, a deleted space's owner
  link, and `USER` on an `OWNER`; a deactivated link does not count (break: count without
  `deactivatedAt`); 422 `invalid_choice` for `OWNER`; 404; the refused callers. **Races:** two admins
  demoting each other → `LAST_ADMIN` (break: lock the target only); a promotion waiting on a link —
  the test locks the person, links them and commits → `ACCOUNT_HAS_LINKS` (break: count the links
  before the lock); a link waiting on a promotion — the test holds the person and makes them ADMIN →
  the link answers `ACCOUNT_IS_ADMIN` (break: #60's person lock removed).
- `issueTemporaryPassword.api.test.ts`: 200, `no-store`, 12 characters of the alphabet, the account's
  hash matches it, `mustChangePassword`, sessions and reset links ended, `user.temporaryPasswordIssued`
  without it; a sign-in with it answers `mustChangePassword: true`; the handover then records; again →
  the first no longer signs in, the second does (finding 49); no log line or audit entry holds it (as
  #60's test); `OWN_ACCOUNT`, `ACCOUNT_SUSPENDED`, `GOOGLE_ONLY_ACCOUNT`; an account with Google and a
  password gets one; 404; the refused callers. **Race:** an issue waiting on a password change — the
  test holds the row, sets a new hash and inserts a token → the temporary password wins and no token
  survives (break: revoke before the lock).
- Updated: `users.api.test.ts` "refuses a suspended account whose access token has not expired yet" →
  401 by the guard.

## 10. Review Focus (inputs no planned test exercises)

- Two concurrent role changes or suspensions of *non-admin* targets that lock overlapping admin sets:
  ordered by id, so no deadlock, but no test runs two at once.
- A role change for a suspended account (allowed, untested beyond the code's order).
- Tokens signed before the deploy (with a `role` claim): verify ignores the extra claim; not tested.
- The guard's extra read under load online (Neon): not measured.
- A promotion racing a *reception* link change: reception links are not built yet (step 6); the
  conventions require that writer to take the person's lock.

## 11. Commits

1. `docs(workflow): a merge apart needs no new CI run` — workflow §9, `open-pr` step 3.
2. `feat(api): read the account on each signed-in call` — D5 (`shared/auth`, `app.ts`,
   `users.signedInAccount`, claims, `SignedIn`, the token-signing test sites), the guard's tests,
   ADR 0003, security.md (claims, guard), the contract's preamble and `/me/password`, finding 51.
3. `feat(users): suspend and restore an account` — the admin-set lock, the route, `OWN_ACCOUNT`,
   `LAST_ADMIN`, S4, S5, their catalogue lines, tests, conventions §13, the contract, users.md,
   space-links.md (D4), security.md, the plan's table.
4. `feat(space-links): change a person's role` — `admin-roles/`, `countActiveLinks`,
   `ACCOUNT_HAS_LINKS`, tests, the contract, space-links.md, users.md, the plan's table.
5. `feat(users): issue a temporary password` — the route, `GOOGLE_ONLY_ACCOUNT`, tests, the contract,
   users.md, security.md (recovery, Built line), finding 49 resolved, overview's *Built*, the plan's
   *Built* line.

PR: `feat(users): suspend, role and temporary password`; labels `feat`, `area:api`, `area:docs`,
`area:web`; assigned to the owner; not merged.

## 12. Verification (phase 4)

- `npm run build -w @masaha/shared` first (the API reads the shared `dist`).
- Once each, on the head, one at a time: `test:unit`, `test:api` (on `masaha_b_test`), `lint`,
  `typecheck`, `format:check`, `check:links`; since the catalogue lines change: `test:component`,
  `NODE_ENV=production npm run build`, `check:build`. Commit 1 alone: `format:check`, `check:links`.
- **Real requests** against the API on 3321 (`masaha_b_dev`, seeded with demo data): suspend an owner
  (their next request 401, their space still verified), restore them; demote an admin with a second
  admin present; the last admin refused (`OWN_ACCOUNT` in a real run: `LAST_ADMIN` is the race's, proven
  in the API lane); promote a linked user refused; issue a temporary password, record its handover,
  sign in with it (`mustChangePassword: true`, the next request `PASSWORD_CHANGE_REQUIRED`). The server
  stopped and port 3321 checked free afterwards.
- Not run: the E2E lane (end of project); no screenshots (no UI).

## 13. Decisions from the owner (USERS_PLAN_REPLY.md, approved)

1. S1–S7: approved as recommended.
2. Finding 39: not folded; it stays for a small item of its own.
3. The four codes: names approved; Arabic approved for `OWN_ACCOUNT`, `LAST_ADMIN`,
   `ACCOUNT_HAS_LINKS`; `GOOGLE_ONLY_ACCOUNT` reworded (in the table above) to match the catalogue's
   "باستخدام Google".
4. Finding 51: recorded as Open, with its *Resolves when* as written. 52 stays free.

Reminders from the reply: the whole API lane runs; the report names every test whose expectation
changed, with why; the real run shows the web-facing chain once (the suspended account's next request
401, then its refresh refused); each race broken once, a break that does not fail as planned reported;
`git merge-tree --write-tree` against every open PR at the report.
