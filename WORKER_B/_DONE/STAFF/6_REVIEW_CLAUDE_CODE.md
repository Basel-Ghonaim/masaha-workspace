# Review — PR #90 (`feat/space-staff`), independent

**Head reviewed:** `ea56e225159fceae5c9370dbbfc7fbda128e1449` (unchanged from the prompt). Base `02b1067a` (= `origin/main`).
`gh pr view 90` → `mergeStateStatus: CLEAN`; `gh pr checks 90` → all nine lanes **pass** on this head (build,
check:classes, check:links, format:check, lint, test:api, test:component, test:unit, typecheck).
Read only through commit objects (`git diff 02b1067a...ea56e225`, `git show ea56e225:<file>`, `git show <commit>`); nothing run.

**Verdict:** ready after a fix round. There are no blockers. One should-fix is a security gap: S5 does not close
the path it was written for. The other should-fixes are a planned closure (S3) with no test, a code/doc disagreement
on "the first" temporary password, and one error message that now gives a wrong instruction.

**What I saw and what I only read:** every finding below was checked in the code at `ea56e225`. The executor's
red-first outputs, the 24 breaks, the real run and the local lane results are **in the executor's report only**:
I did not run them. CI green is the only test evidence I saw myself.

## The five most important findings

### 1. should-fix (close to a blocker) — S5 does not stop an owner taking an account the admin made an owner elsewhere
- **Where:** `apps/api/src/modules/space-links/staff/staff.service.ts:195-200` (the S5 check guards only a *new*
  issue); `apps/api/src/modules/space-links/admin-owners/adminOwners.service.ts:50-55, 86-104, 111-129`
  (`assertMayOwn`, `linkLocked` and `upgrade` accept an account whose temporary password is pending);
  `docs/features/space-links.md:117` ("a pending receptionist the admin made an owner elsewhere must not be taken
  by this space's owner").
- **Scenario:** owner O of space S creates receptionist R (B1). O gets R's temporary password. R has not
  changed it yet (it is live for 7 days). The admin then upgrades R to owner of S2, either with
  `POST /admin/owners` and `upgradeExisting` or by linking R. `changeRole` ends R's sessions but keeps the
  password and `mustChangePassword`. O signs in as R with the password O already holds. O then does the forced
  change, and with A2 can also correct R's email to an address O controls. **O now owns S2.**
  S5 refuses only a re-issue after the upgrade, but O does not need one. The plan's S5 rationale named this case;
  the code closes only half of it.
- **Before this PR:** no owner could hold another account's temporary password, so B1 creates this path.
- **Fix (in this PR's fix round; the owner decides the rule):** the admin's `linkLocked` (both the upgrade and the
  link) refuses an account whose temporary password is pending. The person changes it first, then the admin links
  them. This needs a code: reuse one, or add one through conventions §4. A test is needed:
  "the admin cannot make a pending account an owner". Alternative: the upgrade ends the pending temporary password
  and issues a fresh one to the admin. That is heavier and changes `AddedOwner`.

### 2. should-fix — S3 (the re-issue counts under the 10/hour limit) has no test
- **Where:** `apps/api/src/modules/space-links/space-links.manage.routes.ts:32`;
  `apps/api/src/modules/space-links/staff/staff.api.test.ts`. The only `staff-account` assertions are T17
  (`:85`, reception writes no row) and T20 (`:156-166`, `POST /` only).
- **Scenario:** delete `counted` from `router.post('/:userId/temporary-password', …)`. Every test stays green, and an
  owner can re-issue without limit. Each re-issue costs a bcrypt hash and ends the person's sessions.
- **Fix (this PR):** one test. Ten re-issues, or a mix of creations and re-issues, then the next re-issue answers
  429. The break: `counted` removed from the re-issue route.

### 3. should-fix — the owner may re-issue "while the first is pending", but the code allows any pending password, including the admin's recovery
- **Where:** `staff.service.ts:186` checks `account.mustChangePassword` only. The docs say "first" in three places:
  `docs/api/api-contract.md:282` ("only while the person's first is still pending (lost, or expired)"),
  `docs/backend/security.md:74` ("while its first is still pending") and `docs/features/space-links.md:117`.
- **Scenario:** R changes the first password, so the account is R's. R later loses their email, and the admin
  issues R a recovery password (pending again). O can now re-issue it (B4: active reception link, `USER`, no other
  link). O then signs in and, with A2, corrects R's email to O's. R loses an account they had settled. The impact
  is limited because S5 keeps the account to S's desk, but the docs promise this cannot happen
  ("once changed the account is the person's").
- **Fix (this PR):** choose one. Either the code refuses a re-issue once the account was ever settled (a re-issue
  only while the creator's own issue is pending), or the three documents drop "first" and say that an admin's
  recovery reopens the owner's re-issue. This is the owner's decision. Recommended: the docs follow the code, and
  `space-links.md:117`'s *Why* drops "once changed the account is the person's".

### 4. should-fix — the `GOOGLE_LINK_NOT_ALLOWED` message now gives a dead-end instruction
- **Where:** `apps/web/src/shared/copy/english/errors.ts:49` ("Sign in with its password, or reset the password, to
  continue.") and the Arabic line at `apps/web/src/shared/copy/arabic/errors.ts:41`. Code: `users.service.ts:154-157`.
- **Scenario:** S1 now sends this code for an account whose temporary password is pending. A1 makes "reset the
  password" send nothing for that account, so a person who follows the message waits for an email that never
  comes. The plan (S1, *Cost*) read only the first half of the line ("sign in with the password").
- **Fix:** one sentence in both catalogues, e.g. "…Sign in with its password to continue." Belongs to this PR's
  fix round if the owner extends the catalogue licence to it. Otherwise record it as a finding for the web item.

### 5. nit (record) — the reused error codes carry the admin's messages into the owner's staff screen
- **Where:** `apps/web/src/shared/copy/english/errors.ts:37` `ACCOUNT_IS_ADMIN` ("…can't be a space's owner"),
  `:40` `EMAIL_HAS_ACCOUNT` ("Upgrade it to an owner to link it."), `:59-60` `ACCOUNT_HAS_LINKS` ("…their role
  follows those links. Unlink them first."), and `TEMPORARY_PASSWORD_NOT_PENDING` ("…so there is no handover to
  record", now also answered by B4's re-issue). The Arabic lines match.
- **Scenario:** the staff screen (a later web item) shows the code's general message. An owner who adds an email
  that has an account is told to upgrade it, which owners cannot do. An owner who re-issues for an account that
  holds other links is told to unlink it. No screen exists yet, so nothing is wrong today.
- **Fix:** a finding to record, or a line in the staff web item's prompt. That item gives these refusals messages
  for the field or the screen. The API is fine as built.

## The other findings

### 6. nit (plausible; a finding to record) — an owner can block any free email address indefinitely
- **Where:** `staff.service.ts:85-120` (B1 creates an account for any free address); `users.service.ts:146`
  (`mayRecoverByEmail`), `:154` (`assertMayLinkGoogle`) and `temporaryPassword.ts:19-25`. An expired temporary
  password stays pending; nothing settles or frees the account.
- **Scenario:** an owner creates up to 10 reception accounts an hour under addresses that are not theirs. Each
  account stays pending for good. The real holder of the address cannot register (`EMAIL_TAKEN`), cannot reset
  (pending), and cannot sign in with Google (`GOOGLE_LINK_NOT_ALLOWED`) until the admin steps in by issuing a
  temporary password to the right person. Before this PR, an address someone else registered could be taken back
  by its holder (reset, or the Google link). The same applies by design to the holder of an admin's mistyped
  address. That is intended, but nowhere is it said to be permanent.
- **Fix:** record a finding: "an address held by a pending account is locked out until the admin acts". It
  resolves when the owner decides whether an expired pending account frees its address, or the admin gets a way
  to free it. Do not change it in this PR.

### 7. nit — `space-links.md` says the handover is recorded "under the same refusals"; it is not
- **Where:** `docs/features/space-links.md:117`; code `staff.service.ts:207-217`.
- **What:** the handover refuses only without an active reception link (404) and once nothing is pending (409).
  It does not check suspended or "holds anything else" (S5). The contract's handover errors
  (`api-contract.md`, handover section) match the code, so only the feature line is wrong.
- **Fix (this PR's fix round):** "the handover is recorded only for an active reception link here, while a
  temporary password is pending". Or add the refusals to the code. That choice is the owner's; the handover writes
  only an audit row, so the doc fix is enough.

### 8. nit (plausible; a finding to record) — the deactivation toggle can sign out an owner of another space as often as wanted
- **Where:** `staff.service.ts:150-153` (every deactivation ends every session); `space-links.manage.routes.ts:31`
  (PATCH is not counted).
- **Scenario:** after the admin makes S's receptionist the owner of S2 (still allowed once the person has settled,
  even after finding 1's fix), S's owner can deactivate and re-activate in a loop. Each deactivation ends all of the
  person's sessions, as owner of S2 too. Only the same-state check holds it back, and the loop never sends the
  same state twice.
- **Fix:** record it with finding 84 (a person holding links at two spaces). One possible rule is that a
  deactivation ends every session only when the person holds no other active link; that is the owner's call.

### 9. nit — tests that do not exist for clauses that do
- `staff.service.ts:196`, the `role !== 'USER'` half of S5: T26 (`staff.api.test.ts:391-405`) uses a `USER` with an
  OWNER link, so deleting only the role clause stays green. That clause is defensive today: an admin's role
  change refuses an account with links, and `OWNER` follows a link the count already sees.
- `staff.service.ts:46`, the 404 for a **deactivated** reception link on the re-issue and the handover: no test
  deactivates before either. T27 tests only another space's receptionist.
- `staff.service.ts:148`, `ACCOUNT_IS_ADMIN` on re-activation: not tested (the plan's T23 named only the suspension).
- The expiry check in `confirm`, under the lock (`users.service.ts:340`): the plan lists it as not tested. B10
  removed it together with the sign-in's check, so the second check alone has no proof. This was accepted by the plan.
- **Fix:** add the first two in the fix round if they are cheap. The others are fine to leave, as the plan said.

## The cross-PR trap (commit 7 and PR #89)
- On `main`, all five `AdminUserRow` literals got `receptionSpaces: []`: `OwnersList.component.test.tsx` (2),
  `useOwnersList.component.test.tsx`, `spaceLinksRepository.unit.test.ts` and `userRowView.unit.test.ts`. CI's
  typecheck is green on the head.
- **PR #89 at its current head `8548308e`** adds no `AdminUserRow` literal. Its uses are type positions only:
  `useAdminUsersQuery.ts`, `spaceLinksRepository.ts`, `services/userRowView.ts`, `types/UserRowView.ts`. Its
  `pages/showcase/fixtures.json` holds no users row. Its fix round is still to come, so on the second merge:
  - run `npm run typecheck` on the merged tree. Any new `AdminUserRow` object (a test of `userRowView`,
    `OwnersPage`, `useAdminUsersQuery`) gets `receptionSpaces: []`;
  - a users row added to the showcase's JSON fixtures is **not** caught by typecheck. Read it by eye;
  - text conflicts are expected in `docs/architecture/findings/README.md` (84 here; 82, 83 and 87 there) and
    `docs/features/space-links.md`. `docs/features/users.md` is edited by both too: check it even if Git merges it.

## The executor's departures
1. **T2 / B4: sound.** The rewritten T2 (`password.api.test.ts:323-337`) is the race the guard exists for: the
   account is settled at the request and made pending before the resend. The first email is expected and no second
   one. The guard is reachable in production: an issue deletes the reset tokens only
   (`sessions.service.ts:191-193`), and an unbound recovery keeps its `userId`, so without the guard a resend after
   an issue would email a new link. Removing the resend's check, or reverting it to `maySignIn`, sends a second
   email: red. On procedure, the plan said "stop and ask", and the owner accepted the departure afterwards. That is
   recorded in the report.
2. **The `v1-mvp.md` row rewritten, not removed: sound.** It matches the packages row #87 kept
   (`docs/plans/v1-mvp.md:229-230`), and step 6 says "Built: its API… the screen remains planned" (`:88`).
3. **`STAFF_ACCOUNT`'s window written inline (`60 * 60_000`): sound.** It follows the auth limits; there is no
   shared `ONE_HOUR`.
4. **B16 made as a lookup before the insert: sound.** The plan's literal break ("on `null`, link") cannot run: the
   unique violation has already aborted the transaction (`staff.service.ts:99`). It would answer 500 and turn T19
   red for the wrong reason. A lookup-then-link is the drift P5 names. T19 (`staff.api.test.ts:137-154`) catches
   it: 409, no `space_managers` row, no audit, and the account unchanged.
5. **`seedSettings` in the PATCH tests: sound.** It is test-only, scoped to that `describe`
   (`staff.api.test.ts:264`), and needed because the space's read needs the platform's settings.

## Checked and fine
- **A1:** `forgotPassword` and `resendResetLink` use `mayRecoverByEmail` (`auth.service.ts:283, 313`). A pending
  account opens a recovery with no `userId` and waits as for a send (T1 compares the full text and the cookie).
  `checkResetToken` and `resetPassword` re-check under the session lock, the reset **before**
  `consumeRecoveryLink`, so a refusal writes nothing (`:345, :380`; T3, T4).
- **S1:** `accountForGoogle` refuses a pending account before the authority check, after the "already linked to
  this subject" return. `linkGoogle` re-checks under the lock (`users.service.ts:370, 408`). An account already
  linked to Google opens as before (P4). The rewrite of `google.api.test.ts:94` is the approved one.
- **A2:** `email` outside the forced change gives 422 before the limiter (`users.service.ts:631`). The change sets
  the email inside the transaction only after `setPasswordIf` matched `mustChangePassword: true`, so the forced
  state is re-proven under the lock. `setEmail` is the last statement before the throw. `EMAIL_TAKEN` (409) counts
  under `PASSWORD_CHANGE` (`limiter.ts:78`: any `AppError` below 500 keeps its slot). Reset links end after a
  correction. Case is handled by `emailSchema` (T15).
- **A3:** the expiry is checked after the suspension, only once the password matched, at sign-in and in `confirm`
  (`users.service.ts:328, 340`). Every write that makes a password pending sets an expiry
  (`createWithTemporaryPassword`, `setTemporaryPassword` via `replaceWithTemporaryPassword`). Every write that
  settles one clears it (`setPassword`, `setPasswordIf`, `linkGoogleIfUnlinked`). No other source file writes
  `mustChangePassword` (`git grep`). Test fixtures outside the helper were fixed (`requireAuth`, `handover`);
  `test/admin.ts:46` puts the flag in a token only.
- **The migration:** column, then the backfill (`WHERE must_change_password`), then the `CHECK`, in that order.
  The column matches the schema (`DateTime? @db.Timestamptz(3)`). The `CHECK` lives in SQL only, which Prisma
  neither models nor drops; the schema's `///` line names it. There is no down migration, as everywhere in the
  repository. Existing pending rows get 7 days from the migration, as planned.
- **Part B authorization:** the router is mounted inside `/manage/spaces/:spaceId` behind `requireAuth` and
  `requireSpaceAccess` (`app.ts:373-379`), so a user, another owner or the admin gets 404 (T16 covers all five
  routes and all three callers). `requireCan('staff.manage')` (`can.ts:80`, owner) comes first on every route,
  before `counted` and `validate` (T17, with no rate-limit row). Every write re-asks `can()` under the space's lock
  (`staff.service.ts:32-37`), then takes the person's lock: the order the admin's owners use.
- **B1:** the insert has no lookup, the 409 writes nothing, and the account is `USER`, pending, with an expiry
  (T18, T19).
- **B3:** reads by `role: 'RECEPTION'`, so a co-owner gets 404 (T24). The same state writes nothing. Deactivation
  bumps the version and deletes refresh tokens, so the old token gets 401 and the refresh 401 (T22). Re-activation
  refuses suspended accounts and admins.
- **B4:** refusal order 404 → `TEMPORARY_PASSWORD_NOT_PENDING` → `ACCOUNT_SUSPENDED` → `ACCOUNT_HAS_LINKS`, all
  under both locks. `countOtherActiveLinks` counts both roles, soft-deleted spaces included (the safe side). The
  writes go through the shared `replaceWithTemporaryPassword`, so the expiry is renewed and sessions and reset links
  end. The admin's issue and handover behave as before.
- **Routes' order:** distinct method and path pairs, nothing shadowed. A non-numeric `:userId` reaches
  `parseId` only after `mayManage`.
- **B6:** `findActiveLinksOf` reads both roles in one query. Soft-deleted spaces drop out through `summariesFor`.
  T28 covers a deactivated link and a deleted space.
- **Section 10 (review focus):** a concurrent creation of one email ends in the loser's 409 with its transaction
  rolled back, so no link or audit is left. An issue between bcrypt and `confirm` fails `confirm`'s hash
  comparison. A forgot that races an issue may email a link that opens nothing. `setEmail` racing a registration
  hits the unique key and rolls back the whole change. A deactivation racing a refresh is ordered by the session
  lock, and the version kills the winner's token. An upgraded ex-receptionist's row becomes `OWNER`, so PATCH
  answers 404.
- **Error codes:** `TEMPORARY_PASSWORD_EXPIRED` is in `packages/shared/src/core/errors.ts`, in both catalogues
  (the owner's approved wording, word for word) and in contract §6. Every other code used already existed.
- **Documents:** ADR 0009 has a *Revised* line and rule 4's bullet replaced. Finding 84 has its index line, and
  85–86 are not needed. Security's *Built* and *Not yet built* lines, the contract's sections (*Session*, *Google*,
  *forgotten password*, *Me*, *Staff (managed)*, *AdminUserRow*, the §4 exception), `users.md`, `auth.md`,
  `conventions.md` §6, `data-model.md` and `overview.md` are true to the code, apart from findings 3 and 7. The
  facts live in security and the contract; the features summarize and link.
- **Commits:** seven, subjects 39 to 50 characters, Conventional Commits, each body saying why. No tool
  attribution. `apps/web` holds only the two catalogue lines and the five `receptionSpaces: []` lines.

**Head checked again at the end:** `ea56e225`, `CLEAN`. It did not move during the review.
