# Review — PR #62, head `50fdcea`

Pinned: `gh pr view 62 --json headRefOid` = `50fdcea5b336349ed7588822fe93375a2e958680`; base `d7d800e`. Read from commit objects in `C:\Users\basel\masaha`. Note: the reviewer is the same tool as the PR's author.

**Verdict:** mergeable after two should-fix items. No blocker: authorization, the admin-set lock and the revocations hold.

## Findings

### 1. should-fix — a temporary password issued after a token leaves the person's open tab stuck on 403 for up to 15 minutes

- **Where:** `apps/api/src/shared/auth/requireAuth.ts` (the pending check, `claims.mustChangePassword || account.mustChangePassword` → 403 `PASSWORD_CHANGE_REQUIRED`); the web: `apps/web/src/shared/routing/guards/PasswordChangeGate.tsx:19` and `RequirePasswordChange.tsx:19` gate on the in-memory session's `user.mustChangePassword`; `apps/web/src/shared/api/interceptors/refreshOn401.ts:24` refreshes only on 401.
- **Scenario:** the person is signed in on the web. The admin issues a temporary password (D6), which ends their sessions and sets the account's flag. On their tab, every next request answers 403 `PASSWORD_CHANGE_REQUIRED`. Nothing on the web reacts to it: the session in memory still says `mustChangePassword: false`, so the gate never sends them to the change page, and no refresh runs. Even if they reach `/me/password`, the change is not forced (`tokenPendingChange` is false), so it asks for a current password they no longer know. The tab shows errors until the access token expires (≤ 15 min); then the 401 → refresh → 401 chain signs them out.
- **Why 401 is the right answer:** a token whose claim says no change is pending while the account says one is was signed before the temporary password. Only D6 (which ends every session) and an admin-created account (whose first token already carries the claim) set the flag. So that token's session has always ended. That is S3's own reason for answering a suspended account with 401.
- **Fix:** in `requireAuth`, answer 401 (no code) when the account says a change is pending and the token does not. Keep 403 `PASSWORD_CHANGE_REQUIRED` when the token says so. Then the web's existing 401 chain signs the tab out, and the person signs in with the temporary password and is forced to change.
- **Tests to change:** the unit case "…when only the account says a change is pending" (→ 401), and `requireAuth.api.test.ts` "holds a temporary password set after the token: only the change is reachable". That second test also passes only because it sets the flag without replacing the hash, which D6 never does.
- **Documents:** security.md › *Passwords*, and the contract's §1 auth line.

### 2. should-fix — the governorate tests' audit trigger can be left behind for good

- **Where:** `apps/api/src/modules/lookups/governorates/governorates.api.test.ts:25-38` (`whileAuditRefused`).
- **Scenario:** `CREATE FUNCTION` and `CREATE TRIGGER` run outside the `try`, and nothing uses `OR REPLACE` or `IF EXISTS`. The trigger would survive in the test database if:
  - the run is killed between the create and the `finally` (Ctrl-C, a worker crash, a hard timeout);
  - or `CREATE TRIGGER` itself fails, which leaves the function behind.

  `resetDatabase` only truncates (`test/reset-database.ts:19`), so a surviving trigger stays in `masaha_test`. Every later test that writes an audit entry then fails with "audit refused", in every file, on every later run. This file's next run also fails at `CREATE FUNCTION` ("already exists").
- **Fix:**
  - start with `DROP TRIGGER IF EXISTS refuse_audit ON audit_logs` and `CREATE OR REPLACE FUNCTION`;
  - use `IF EXISTS` in the `finally`;
  - put both creates inside the `try`;
  - better still, drop a leftover in `resetDatabase` or the lane's global setup, so one aborted run cannot poison the next.

### 3. nit — finding 51 and security.md say a suspension "reaches the token at once", but a restore revives it

- **Where:** `docs/architecture/findings/51-an-access-token-outlives-the-end-of-its-session.md:5`; `docs/backend/security.md:10` (the access-token row: "only a suspension, a role change and a pending change reach it at once").
- **Scenario:** an account is suspended at T and restored at T+5 min. An access token signed before T, a stolen one included, is accepted again from T+5 until its expiry. The guard reads only `suspendedAt`, and the restore ends nothing.

  Similarly, after a role change, the old token is not ended: it acts with the new role.
- **Fix:** in finding 51's evidence and security.md's row, say that a suspension holds while it lasts, and that a token signed before it works again after a restore until it expires. The same *Resolves when* (a sessions-ended time compared with `iat`) covers it.

### 4. nit — conventions §13 says a link change takes the person's row "never an admin's"

- **Where:** `docs/backend/conventions.md:343`.
- **What is wrong:** `adminOwners.service.ts:119,170,183` lock the person (`users.lockAccount`) before `assertMayOwn` refuses an admin. A link aimed at an admin therefore takes an admin's row, under the space's lock.
- **Why no deadlock follows:** the admin-set lock takes no space row, so no cycle forms. Only the parenthesis is untrue.
- **Fix:** drop "(never an admin's)", or say that the admin-set lock takes no space's row, so no two orders cross.

### 5. nit — a demoted admin's open dashboard keeps its admin view, with 403s, until the token expires

- **Where:** `requireRole.ts` (403); the web keeps `Session.user.role` in memory and refreshes only on 401.
- **Scenario:** after a demotion, the server refuses correctly. The demoted admin's tab still shows the admin's pages, each request failing with 403, until the access token expires and the 401 chain signs them out.
- **Fix:** none needed on the API for safety. Record it with finding 51 (the guard cannot tell that the session ended), or leave it for the web's users screen to handle a 403 on `/admin` by refreshing the session.

### 6. nit — the races are timed, not observed

- **Where:** `apps/api/test/locks.ts:11` (`WAIT_MS = 2_000`).
- **Scenario:** each race assumes the request reaches its lock within 2 s.
  - Under a loaded CI, the request may start only after the test transaction commits. For the promotion-waiting-on-a-link race, it then answers `ACCOUNT_HAS_LINKS` without any interleaving: a pass that proves nothing that run.
  - In the `LAST_ADMIN` races it would instead fail: 401 at the guard, since the actor is suspended or demoted by then.

  This is the same pattern as `sessionLock.api.test.ts`.
- **Fix:** before `meanwhile`, wait until `pg_stat_activity` shows a backend with `wait_event_type = 'Lock'`, and fail if none does. Optional.

## Checked and fine

- **No path reads the role from the token.** `AccessClaims` has no role. `requireRole`, `can()` (through the spaces controllers' `signedIn(req).role`) and the request log read the stored role. The general rate limit reads only `sub`, before the guard. The links loader runs after the guard. Refresh and logout act on the cookie and check the suspension under the session lock.
- **The guard's order** is token → account → suspended (401, no code) → pending (403). `/me/password` keeps `allowPendingPasswordChange`, and the forced change still needs the token's claim. The web's interceptor refreshes on any non-`/auth/` 401, and `refresh.ts` ends the session on that refresh's 401. So S3's chain holds, and the real run shows it.
- **The admin-set statement** `WHERE id = $1 OR (role='ADMIN' AND suspended_at IS NULL) ORDER BY id FOR NO KEY UPDATE`:
  - rows lock in sort order;
  - a row demoted or suspended meanwhile is re-checked and drops out;
  - a promotion committed meanwhile is missed, which only errs toward refusing;
  - the target is always in the set.
- **No deadlock:**
  - sign-in, refresh, logout, password change, reset, handover and the temporary password take one user row;
  - a link change takes the space, then one person;
  - facts saves take the space only;
  - audit and token inserts take `KEY SHARE`, which `NO KEY UPDATE` does not block.
- **`LAST_ADMIN`** is reachable only in the race, as documented. **`OWN_ACCOUNT`** comes before any lock and before the bcrypt of the temporary password.
- **Revocation:**
  - suspension writes, then revokes sessions and reset links (S5);
  - a role change ends sessions through `users.changeRole`;
  - the temporary password writes, then ends sessions and reset links;
  - each in its own transaction; an idempotent repeat and a restore end nothing.
  - The two tests the worker reports as not failing to the lock's removal alone still prove what their titles claim (no session survives). The suspension's lock is proven by its `LAST_ADMIN` race, and the temporary password's by "an account suspended while the issue waited".
- **S4:** the password change locks and checks the suspension before its compare-and-set.
- **The temporary password:**
  - #60's generator, hashed before the transaction;
  - only the hash reaches Prisma;
  - the audit `after` is `{ mustChangePassword: true }`;
  - `no-store`, and a key the logger redacts;
  - Google-only means no hash, so an account with Google and a password gets one;
  - issued again, it replaces the pending one.
- **Authorization:** every new route is inside `/admin`'s guard and tested against `REFUSED_CALLERS`. `ACCOUNT_HAS_LINKS` counts active links of either role, a soft-deleted space's included, a superset of the owner links the global role counts, as D3 asks.
- **Levels:** `users` imports nothing above L1; `shared/auth` imports no module (the reader is wired in `app.ts`); `admin-roles` imports `users` only through its `index.ts`.
- **Tests:** expectations are written by hand. The two helpers live under `test/` (`locks.ts`, `admin.ts`). The web changes are the four codes' lines in the two catalogues only.
- **Documents:**
  - ADR 0003 and ADR 0002 *Revised*;
  - the contract (the three routes, the auth line, `/me/password`, §6);
  - users.md, space-links.md;
  - the plan's table (both rows moved to *Built*);
  - overview's *Built*;
  - findings 49 (Resolved, moved in the index) and 51 (Open, indexed);
  - workflow §9 and `open-pr` step 3.

  Each matches the code, except items 3 and 4.
- **Commits:** five, subjects 49, 50, 43, 41 and 39 characters.
