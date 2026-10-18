# SESSIONS — a session ends when it should (findings 51, 20, 16, 39 · API)

> **Approved 2026-10-13** with the owner's reply (SESSIONS_PLAN_REPLY.md) folded in: O1 (a) — the `app.ts` lines in commit 4 only; O2 — SMTP keys present, `EMAIL_MODE=smtp` only while measuring, then removed, about 8 sends to the seeded admin's or a demo account's address; **S1 rejected** — the "account pending, token not" 401 stays (defence in depth), its unit test stays, security.md names both checks; S2–S7 approved; commit 2's subject shortened; the bounds measured locally, said in security.md, and **finding 65** recorded; development's reverse tell named in security.md.

Worker B · `masaha-b` · branch `feat/session-ends` (cut after approval, from `origin/main` `3c3dc47`) · DBs `masaha_b_dev`/`masaha_b_test` · API 3321, web 5321. This item carries the one schema change in flight.

## 1. Summary

- **51:** every access token carries the account's **session version**. The version goes up by one each time all of the account's sessions end. `requireAuth`, which already reads the account on each request, refuses a token whose version is not the account's: 401, as for an expired token.
- **20:** a session lives **at most 30 days from its sign-in**. Each refresh-token row carries its family's deadline: set at sign-in, copied on each rotation. A refresh past the deadline is refused and the family is deleted.
- **16:** when a forgotten-password request or a resend **sends no email**, its answer **waits a jittered time drawn from the measured length of a real send**. The timer is a port, so the tests never wait real seconds.
- **39:** `createUsersService` loses its `passwords` parameter. The unit tests that needed it move to a pure helper or are already proven in the API lane.

## 2. Contract

**Scope.** The four findings above, the migration (both columns), and the one-line schema comment for the media worker (D6). Also the documents: security.md, ADR 0003, the data model, conventions (§2, R5, §11, §12), the contract, users.md, auth.md, findings 51/20/16/39 and the index.

**Acceptance criteria**
- [ ] An access token signed before a password change (on another session), a reset, a suspension, a role change (the admin's, or one that follows owner links), the admin's temporary password, or a Google link answers 401 on its next request.
- [ ] A token signed before a suspension is still refused after the account is restored.
- [ ] The device that changed its password keeps working with the token it got back. Other tabs in the same browser refresh silently through the new cookie.
- [ ] Signing out ends only that session. The account's other sessions keep working, and no version is bumped.
- [ ] A token without the version claim (signed before the deploy) answers 401 once. The web refreshes and replays the request.
- [ ] A refresh at or past 30 days from sign-in answers 401, clears the cookies and deletes the family, even for a session that refreshed every few days. A refresh just before the deadline works.
- [ ] Families that exist at the migration get a deadline (S6).
- [ ] `forgot` and `resend` wait a drawn time within the documented bounds whenever no email was delivered: no account, a suspended account, a cap refusal, a failed send. A delivered email adds no wait. The waits vary between requests.
- [ ] `createUsersService` has no `passwords` parameter, and the `Passwords` type is gone.
- [ ] All lanes, lint, typecheck, format and links pass. Real requests against 3321 are listed in the report.

**Out of scope:** finding 17 (sweeping), apart from S3's sweep on the existing path. Finding 21 (replays within the grace window). Finding 23. The repository parameter of the older services (finding 31's follow-up). Anything in `apps/web` or `packages/shared`.

## 3. Reading done

CLAUDE.md, workflow, the map, and the open findings' titles. Then users.md and auth.md first. Findings 51, 20, 16, 39 and 31 whole, and 17, 21 and 23 opened. security.md (Tokens and cookies, Passwords, Authorization, Rate limits). ADRs 0003, 0013, 0014, 0015, 0017. Conventions §2, §8, §11, §12, §13. The data model › Users and sessions. Contract §1–§3, Session, the forgotten password, Me, Users (the admin). Testing §1–§4.

The code: `shared/auth/{accessToken,requireAuth,signedIn}.ts`, `modules/sessions/*`, `modules/users/{users.service,users.repository,password,users.controller}.ts` and their unit tests, `modules/auth/auth.service.ts` and `email/*`, `app.ts` (the wiring), `test/{app,locks}.ts`, and the identity API tests' titles. On the web, `refreshOn401.unit.test.ts`.

## 4. Settled decisions, as they will be built

**Every path that ends all sessions, from the code** (each calls `sessions.revokeAll` today):

| Path | Where | Bumps |
|---|---|---|
| Password change | `users.changePassword` | yes; the new token is signed with the version read after the bump |
| Reset by email | `auth.resetPassword` | yes |
| Suspension | `users.setSuspended(true)` | yes (restoring bumps nothing) |
| Role change: the admin's, and one that follows owner links | `users.changeRole` (called by `adminRoles` and `adminOwners`) | yes |
| The admin's temporary password | `users.issueTemporaryPasswordFor` | yes |
| **Google link** (not in the prompt's D2 list, but the code ends sessions here) | `users.linkGoogle` | yes; the session it opens reads the account after the bump |
| A refresh refused for a suspended account | `auth.refresh` | yes (harmless: the suspension already bumped). This keeps one rule, below |
| Sign-out | `auth.logout` → `sessions.end` | **no**: it ends only its own family |

- **D1.** New column `User.sessionVersion Int @default(0)` (`session_version`). New claim `sessionVersion`, an integer, signed by `accessTokens.sign`. `verify` returns `undefined` when the claim is missing or is not a safe integer ≥ 0, so a token from before the deploy answers 401. `ACCOUNT` (users repository) selects the version. `accessClaims(account)` carries it. `SignedInAccount` gains `sessionVersion`, and `requireAuth` answers 401 ("Session ended") when it differs from the claim. ADR 0003 gets a dated *Revised* line.
- **D2.** A new users-service function, `endSessions(userId, tx)`, takes the version up with an atomic `{ increment: 1 }` in the same statement sequence as `sessions.revokeAll`, inside the caller's transaction, under the session lock the caller already holds. Every row of the table above calls it. Nothing else calls `sessions.revokeAll` (S5).
- **D3.** New column `RefreshToken.sessionEndsAt Timestamptz(3)` (`session_ends_at`, not null). `issue` sets it to `now + 30 days`, and `rotate` copies it. In `rotate`, under the lock: if `at >= sessionEndsAt`, the family is deleted and the outcome is `invalid`, so the refresh answers 401 and the cookies are cleared as for any ended session. A token's own `expiresAt` stays `at + 7 days`, not capped at the deadline: capping it would make `ownerOf` refuse the token before the lock, and the family would not be deleted. The web changes nothing.
- **D4.** A new port in the composition root, `ApiOptions.wait?: (ms) => Promise<void>`, defaulting to `node:timers/promises`' `setTimeout`, passed to `createAuthService` (see the owner decision O1).
  - The rule is the auth module's own, in a new `modules/auth/forgotPasswordWait.ts`: the bounds `NO_SEND_WAIT = { minMs, maxMs }`, taken from the measurement, and a draw with `crypto.randomInt`, uniform between the bounds.
  - `sendResetLink` returns whether the email was delivered. `forgotPassword` and `resendResetLink` call `wait(draw())` when no email was delivered.
  - A slow relay's outliers stay distinguishable. security.md records that residual as accepted, and finding 16 is resolved with that line.
- **The measurement** (O2): with `EMAIL_MODE=smtp` set in this folder's `apps/api/.env` for the measurement only, about 8 real requests for a real account and 8 for an unknown email, end to end against 3321, with no wait in place.
  - The bounds are the p10–p90 of the difference between the two series, rounded to 100 ms.
  - Without SMTP keys I say so, and use a documented estimate of 1.5–3.0 s (Gmail SMTPS: DNS, TCP, TLS, AUTH, MAIL, RCPT, DATA, about 7 round trips plus Google's processing).
  - The `.env` change is reverted afterwards. Keys are read only, and no value is printed.
- **D5.** `passwords` and `Passwords` are removed. The service calls `hashPassword` and `verifyPassword` from `./password.ts`. The repository parameter stays.
- **D6.** One migration, `<ts>_session_ends`, made once with `migrate dev --create-only`, then checked with `ls`. Its SQL is hand-edited for the backfill (S6). If it refuses on data loss, I use `migrate diff --script` instead. Same commit: `Space.profileUpdatedAt`'s doc comment loses "and photos".

## 5. Stronger decisions

- **S1. Remove `requireAuth`'s "account pending, token not" 401.** — **Owner: rejected, it stays** (defence in depth for a future path, such as the owner's reception passwords; its unit test stays; security.md names both checks). The version check now covers it: the only way a pending change appears on an existing account is the admin's temporary password, which bumps the version.
  - *Why:* one mechanism for one fact. Otherwise there are two 401 rules for the same case.
  - *Cost:* one unit test is removed and security.md is reworded. If a future path set a temporary password without `endSessions`, nothing would catch it. That path is the owner's reception passwords, not built yet, and it would have to end sessions anyway.
  - **Recommend: remove.** If you prefer, keep it as defence in depth, at no other cost.
- **S2. The Google link bumps the version** (the table above).
  - *Why:* a token from a session opened before the link may be the pre-account attacker's, which is the exact case the link guards against.
  - *Cost:* none. **Recommend: yes** (this is required by "every path from the code").
- **S3. `deleteExpired` also deletes rows past their `sessionEndsAt`.**
  - *Why:* dead families leave on the user's next sign-in or refresh, as expired rows do now. This eases finding 17.
  - *Cost:* one condition. **Recommend: yes.**
- **S4. The wait also covers `resend`.**
  - *Why:* a resend for a recovery with no account sends nothing and answers at once, the same leak as `forgot`.
  - *Cost:* one call. **Recommend: yes.**
- **S5. `endSessions` is the only path to `sessions.revokeAll`.** `auth.resetPassword` and the refused refresh call it instead of `sessions.revokeAll`.
  - *Why:* no future path can delete refresh tokens without bumping the version. The invariant sits in one function, beside the session lock.
  - *Cost:* an extra version write on a refused refresh of a suspended account. **Recommend: yes.**
- **S6. Backfill: every existing family's deadline is the migration's time + 30 days** (one `UPDATE … SET session_ends_at = now() + interval '30 days'`, then `SET NOT NULL`).
  - *Why:* the prompt's "first token's creation or the migration, whichever is later" always comes out as the migration. The family's first row is usually deleted after 7 days anyway, so its real sign-in time is not known.
  - *Cost:* a session alive at the deploy lasts up to 30 more days.
  - *Rejected alternative:* `MIN(created_at) + 30 days`, which would land 23–30 days out anyway.
  - **Recommend: migration + 30 days.**
- **S7. Wait only when nothing was delivered**, rather than padding every answer to a floor.
  - *Why:* padding a real send as well (`max(send, target)`) moves the real answers later than the padded ones, so the two distributions stop matching.
  - *Cost:* none. **Recommend: yes.**

No other documented rule is weakened. security.md's *Tokens and cookies* will say plainly that a sign-out leaves its own access token valid for at most 15 minutes, and that the web drops that token (D2, accepted).

## 6. Related findings

- **51, 20, 16, 39:** folded (the prompt).
- **17** (sweeping): not folded. It needs the scheduler. S3 only keeps the new deadline from adding to it.
- **21** (a replay within the grace window): not folded. The version does not change it, because a replayed branch is still the same family. It is unchanged.
- **23** (per-address ceiling): not related to the session's end. Not folded.
- **New finding 65** (the owner's reply): the forgotten password's wait was measured from a development machine. **66** only if the work finds something.

## 7. Files

**API, this item's:**
- `apps/api/prisma/schema.prisma` and the new migration.
- `src/shared/auth/accessToken.ts`, `requireAuth.ts`, and their unit tests. Also `requireAuth.api.test.ts`.
- `src/modules/sessions/sessions.service.ts`, `sessions.repository.ts`, and `sessions.service.unit.test.ts` (fixture: the deadline).
- `src/modules/users/users.service.ts`, `users.repository.ts`, `password.ts`, a new `password.unit.test.ts`, `users.service.unit.test.ts`, `users.api.test.ts`, `suspension.api.test.ts` and `issueTemporaryPassword.api.test.ts`.
- `src/modules/auth/auth.service.ts`, a new `forgotPasswordWait.ts` and its unit test, `auth.service.unit.test.ts` (the `Account` literal), `auth.api.test.ts`, `password.api.test.ts`, `google.api.test.ts` and `sessionLock.api.test.ts`.

**Shared with an open item:**
- **`apps/api/src/app.ts`, which the media worker edits.** D4 needs about 3 lines here: `ApiOptions.wait`, its default, and passing it to `createAuthService`. **O1 decides.**
- `test/app.ts` is not touched. `createTestApp` already spreads `Partial<ApiOptions>`, so a test file passes its own `wait`.

**Documents (the fast path, my own sections only):**
- `docs/backend/security.md` and `docs/architecture/decisions/0003-session-model.md`.
- `docs/architecture/data-model.md` (User, RefreshToken).
- `docs/backend/conventions.md`: §2's line on `passwords`, R5's port list (the timer), §11, and the §12 table row.
- `docs/api/api-contract.md`: the §1 *Auth* line, and the 401 wording in *Me*, *Users (the admin)* role and suspended. The refresh's 401 already covers the deadline.
- `docs/features/users.md` and `auth.md` (API decisions, API history, open findings, code map).
- Findings 51, 20, 16 and 39, and the index.
- The overview's *Built* line does not name the session, so it is not touched.

**Not touched:** `apps/web` and `packages/shared`. No shared type changes, because the claims are API-internal and the web never decodes the JWT. No dependency is added.

## 8. Design issues

None: no screen.

## 9. Tests: lane, test, the break it catches

Every new test is seen failing first. Each security, transaction or ordering property is broken once by hand (testing §3 rule 7).

| Behaviour | Lane · file | Break it catches |
|---|---|---|
| A token carries the version; a token without the claim, or with a non-integer or negative one, is refused | unit · `accessToken.unit.test.ts` | `verify` accepting a missing claim |
| A version mismatch answers 401 | unit · `requireAuth.unit.test.ts` | the comparison removed |
| Another session's token is refused after a password change, and the changer's new token works | API · `users.api.test.ts` | no bump; signing the new token before the bump (the changer is refused) |
| The token is refused after a reset | API · `password.api.test.ts` | the bump removed from `resetPassword` |
| The token is refused after a suspension, **and still after the restore** | API · `suspension.api.test.ts` | the bump removed from `setSuspended` |
| Role change: a promoted user's old token is now **401** (it went through before), and a demoted admin's is 401 (it was 403) | API · `requireAuth.api.test.ts` (both existing tests change) | the bump removed from `changeRole` |
| An owner link that changes the role makes the person's old token 401 | API · `requireAuth.api.test.ts`, through `PUT /admin/spaces/:id/owner` or the route `adminOwners` serves | the same bump, through the links path |
| A token from before a temporary password is refused (the existing test; both the version check and the kept pending check refuse it) | API · `requireAuth.api.test.ts` | the bump removed from `issueTemporaryPasswordFor` |
| A Google link makes the old token 401, and the new session works | API · `google.api.test.ts` | the bump removed from `linkGoogle`; the account read before the bump |
| Sign-out leaves the account's other session's token working | API · `auth.api.test.ts` | `logout` calling `endSessions` |
| **Race:** a sign-in that waited on a role change's lock gets a token that works | API · `sessionLock.api.test.ts` (`whileHeld`) | `signIn` signing with the account read before the lock |
| **Race:** a refresh that waited on a password change's lock is refused, and the access token it had answers 401 afterwards | API · `sessionLock.api.test.ts` | the bump outside the locked transaction |
| A refresh 30 days after sign-in is refused, the family deleted and the cookies cleared, through refreshes at days 6/12/18/24; a refresh at 30 days − 1 ms works | API · `auth.api.test.ts` with a mutable `clock` | the deadline not copied on rotation (renewed instead); the check removed |
| A password change's new session gets its own 30 days | API · `users.api.test.ts` | `issue` copying the old family's deadline |
| Sign-in deletes rows past their deadline (S3) | API · `auth.api.test.ts` | the condition removed |
| The draw stays within the bounds | unit · `forgotPasswordWait.unit.test.ts` (a draw at the low and high ends, through an injected `randomInt`-shaped argument of the pure helper itself, not of the service) | wrong bounds |
| `forgot` waits within the bounds for an unknown, a suspended and a capped address, and not for a delivered email; 3 unknown-address waits are not all equal | API · `password.api.test.ts` (`wait` recorder through `createTestApp`) | the wait removed for the suspended address; a fixed delay; waiting after a delivered email |
| `resend` waits for a recovery with no account, and not for a delivered email | API · `password.api.test.ts` | S4 removed |
| With no hash, `verifyPassword` still spends a cost-12 comparison | unit · new `password.unit.test.ts`: elapsed ≥ 40 ms, against about 0 ms for an early return | `if (!hash) return false` |

**D5's moved tests** (rule 3: no fake passwords):
- The unit test "spends a comparison" becomes `password.unit.test.ts`.
- "Shows a suspension only once the password matches" is already in `auth.api.test.ts:236`.
- "Confirms under the lock" is in `sessionLock.api.test.ts:97`.
- `PASSWORD_NOT_SET` is in `users.api.test.ts:127`.
- The forced skip is in `users.api.test.ts:48` and `:146`.
- A wrong current password is in `:76`.
- A change made meanwhile is in `sessionLock.api.test.ts:145`.
- The Google unit tests stay, on the fake repository. `linkGoogle`'s test expects `endSessions`' bump and `revokeAll`.

Test files whose `forgot` or `resend` sends nothing (`password.api.test.ts`, and `sessionLock.api.test.ts` if it does) build their app with a recording `wait`.

**The deploy:** after it, every token without the claim answers 401 once. The web's `refreshOn401.unit.test.ts`, "refreshes once and replays the request once, with the new token", proves the silent refresh. A real request with an old-format token shows the 401 (§12).

## 10. Review Focus (inputs no planned test exercises)

- A version bump landing between a refresh's `ownerOf` and its lock (the lock is meant to cover it; no test drives that exact gap).
- Clock skew between function instances on the 30-day deadline: each instance uses its own clock, so the skew is in milliseconds.
- A relay slower than `maxMs`: the accepted residual.
- Development with `EMAIL_MODE=log`: unknown addresses wait and known ones answer at once, the reverse tell, development only.
- The version is an Int, so overflow is unreachable in practice.
- Two ends at once (a role change and a link change on one person) both increment atomically, so no update is lost; no test drives it.
- An access token alive during the migration: it is refused once (no claim), as for any token.

## 11. Commits

1. `refactor(users): hash passwords in the module` (47) — D5. Includes the conventions §2 line, finding 39 resolved, the index and users.md.
2. `feat(sessions): end a session 30 days on` (41 characters; every subject counted before its commit) — D3 and S3, the migration with both columns (the version column is unused until commit 3, because D6 asks for one migration), the `profileUpdatedAt` comment. Includes security.md (30 days), the data model, finding 20 resolved, the index and auth.md.
3. `feat(auth): end access tokens with their session` (49) — D1, D2, S2, S5 (S1 not applied). Includes security.md, ADR 0003 *Revised*, the contract wording, users.md and auth.md, finding 51 resolved and the index.
4. `feat(auth): wait as a send would when none is made` (49) — D4, S4, S7 and the `app.ts` port (its three lines in this commit only). Includes security.md *Passwords*: its accepted residual, the bounds measured locally (one constant, `NO_SEND_WAIT`), and one sentence that `EMAIL_MODE=log`'s reverse tell is development only; **finding 65** "The forgotten password's wait was measured from a development machine" (*resolves when* the send is measured on the deployment and the bounds set from it), with the index; conventions R5/§11/§12, auth.md, finding 16 resolved and the index.

Each commit gets lint and typecheck. Staging is by path.

## 12. Verification

- Before `test:api` and `test:component`, I check that worker A and `masaha-media` are running no tests.
- Once each, one at a time, on the head: `test:unit`, `test:api`, `lint`, `typecheck`, `format:check`, `check:links`.
- **Not run:** `test:component`, `build` and `check:build`. Nothing the web imports changes (no `packages/shared` and no `apps/web` edits).
- **Real requests against 3321** (all in the report, no token or secret printed):
  1. A token refused right after a password change made on another session, and the changer's token working.
  2. A token refused after a suspension, and still refused after the restore.
  3. A token without the claim (signed with the old shape) refused once, and the refresh working.
  4. A refresh refused past the deadline, with the row's `session_ends_at` set in the past in `masaha_b_dev`.
  5. `forgot` answer times for an unknown email and a real one, 8 runs each, side by side, with SMTP if the keys exist.
- Servers are stopped by PID afterwards and the ports checked free. `.env` goes back to `EMAIL_MODE` as it was.
- At the report: `git merge-tree --write-tree` against every open PR.

## 13. Decisions needed from the owner — answered (see the note at the top)

**If the media PR merges first and this one conflicts:** rebase, keep both sides, `lint` and `typecheck` only, one `--force-with-lease` push, CI runs the lanes; no local lane for that rebase. If the conflict reaches beyond `app.ts`'s lines, stop and say so.

- **O1. `apps/api/src/app.ts` belongs to the media worker, and D4 needs about 3 lines there:** the `wait` port in `ApiOptions` and passing it to `createAuthService`. No other wiring avoids it: every port reaches the auth service through `createApi`, and an unwired default would make the tests wait real seconds.
  - **(a) Recommended:** allow the lines. Whichever PR merges second rebases and keeps both sides (lint and typecheck, the code fast path).
  - **(b)** Split finding 16 into a small follow-up after the media PR merges. This item then ships 51, 20 and 39.
- **O2. SMTP keys for the measurement:** `SMTP_HOST`, `SMTP_PORT`, `SMTP_SECURE`, `SMTP_USER`, `SMTP_PASSWORD` and `EMAIL_FROM` in `C:\Users\basel\masaha-b\apps\api\.env`. They are absent now. I set `EMAIL_MODE=smtp` only while measuring. Without the keys, I use the documented estimate of 1.5–3.0 s and say so.
- **O3. The stronger decisions S1–S7:** approve, or name the ones to drop. The recommendations are all "yes", and S1 is the only one with a real alternative.
