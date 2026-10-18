# Review — PR #38 (F-5b3c1) at `a4e1685` vs `origin/main`

**Verdict:** No blockers. There are two should-fix items: an account-existence oracle in the reset, and one commit subject over 50 characters. Fix those and the PR is ready to merge.

## Findings (most severe first)

### 1. should-fix: the owner's reset tells an attacker the address has an account
- **Where:** `apps/api/src/modules/auth/auth.service.ts:360` (`sessions.endRecoveries(owner, tx)`) → `sessions.service.ts:280` → `sessions.repository.ts:191` (`deleteMany({ where: { userId } })`).
- **Why it happens:** a forgot request for a known address that may sign in stores `userId` on the recovery (`auth.service.ts:268`). An unknown address stores `null`. A successful reset deletes every recovery with that `userId`, including an unbound one an attacker opened in their own browser.
- **Scenario:**
  1. The attacker sends forgot for `victim@x` in browser A.
  2. The victim resets within the hour.
  3. The attacker's `GET /auth/password/recovery` changes from `sent` to `request`, and resend changes from 202 to `RECOVERY_INVALID`.
  4. For an unknown address, the recovery stays `sent` for the full hour.

  This breaks Q1 ("reveals nothing about the account") and `security.md:57` ("names its account … never discloses it").
- **`endRecoveries` adds nothing needed:**
  - `endResetTokens` (line 359) already deletes the user's links.
  - The `reset_token_id` foreign key's ON DELETE CASCADE already ends every bound recovery, including the resetting browser's.
  - The only rows `endRecoveries` removes beyond those are the unbound ones, and those are exactly what makes the oracle.
- **Fix:** take one of these:
  - Drop `endRecoveries` and `deleteUserRecoveries`, which have no other caller, and let the cascade end the bound recoveries.
  - Or limit the delete to `resetTokenId: { not: null }`.

  Then reword `security.md:61` ("ends every session and every recovery of the user"). Proposed wording: "…every recovery bound to a link of the user". That wording is the owner's call.
- **Test:** add an API test where a second, unbound recovery for the same known address still reads `sent` after the owner's reset.

### 2. should-fix: one commit subject is 51 characters
- **Where:** `a737b64` `feat(routing): gate every route on a pending change` (51; the limit is 50).
- **Fix:** reword it to `feat(routing): gate all routes on a pending change` (50) and force-push. Do not add a new commit.

### 3. nit (uncertain): a race in the check can return 500 instead of `RESET_TOKEN_INVALID`
- **Where:** `sessions.repository.ts:200–220` (`bindRecovery`).
- **Why it happens:** `keepOnlyResetToken` and `withdrawResetToken` delete links outside the user lock. If a newer delivered link deletes the old one between `findValidResetToken` and the upsert, the upsert hits a foreign-key violation (P2003). The mapping of that error on this path is unconfirmed, so it is probably a 500. It is rare and discloses nothing.
- **Fix:** catch P2003 in `bindRecovery` and answer invalid. Or take the user lock in the keep and withdraw steps.

### 4. nit: a gate test asserts less than its title says
- **Where:** `apps/web/src/shared/routing/guards/passwordChange.component.test.tsx:~101–106`, "lets a guest and a user without a pending change through".
- **Why it happens:** after `signIn()`, `findByText('The directory')` passes at once on the guest render's leftover text. A gate that redirects every signed-in user would still pass this test.
- **Fix:** sign in before rendering, or `await waitFor(() => expect(where(router)).toBe('/spaces'))`.

### 5. nit (uncertain): `passwordChanged` checks that a user is signed in, not which user
- **Where:** `apps/web/src/shared/session/store.ts:88–97`.
- **Scenario:** A submits the change, signs out, and B signs in, all before A's `/me/password` answer arrives. B's session then takes A's access token. The documented promise ("a sign-out answered first stays signed out") still holds.
- **Fix:** compare the user id captured when the mutation started, or record it as a finding.

### 6. nit: exports nothing outside the module uses
- `positionOf`, `auth.service.ts:49`: make it module-private.
- `changePasswordPath`, `shared/routing/index.ts:~13–19`: no consumer outside `shared/routing`. `signInPath` has the same pattern on main. Drop the export only if the owner applies the rule to exports.

### 7. nit: API test gaps (the code is correct; nothing proves it)
- No test resends from a checked recovery, or from one a check opened. Removing the `linkChecked` / `resetTokenId: null` guard in `recordResend` would pass.
- No concurrent-resend test at the bound of 3. The single conditional `updateMany` is atomic.
- The cascade on a real `/me/password` change is only simulated (`endLinksMeanwhile` in `sessionLock.api.test.ts`).

## Verified OK
- **Disclosure:** forgot gives the same status, body and cookie (Max-Age is the full TTL) for known, suspended and unknown addresses; the equality is tested. Resend records the ask before reading the account. `GET /auth/password/recovery` always answers 200, never 404. Timing is unchanged apart from finding 16, which stays open.
- **Token:** it never appears in a response or a log. The check binds in a transaction after `lockAccount` and re-reads the link inside it. `reset_token_id` is unique, so one recovery per link.
- **Single use:** one `UPDATE … WHERE used_at IS NULL` under the user lock, with a concurrent-reset test.
- **Resend:** one conditional `updateMany` (fewer than 3 resends, at least 60 s since the last link, unbound, unexpired), so a race cannot pass the bound. It shares forgot's `PASSWORD_ADDRESS` and `PASSWORD_EMAIL` budget, with no second counter, and the sharing is tested.
- **Strict schemas:** the reset body and the resend body are both `strictObject`. A token in the reset body gets 422; that is tested.
- **Cookie and cross-site:**
  - The cookie is `HttpOnly`, `SameSite=Strict`, `Secure` outside development, `Path=/api/v1/auth/password`, set from one shared options object, and cleared on success.
  - `sameSiteOnly` is on all five routes (forgot, resend, recovery, check, reset), each with a 403 test.
- **Storage:** no address is stored, only a SHA-256 digest and the masked form. The migration adds one table with CASCADE foreign keys and touches no other table.
- **Unchanged:** the token stays in the URL fragment; the per-recipient, requester and ceiling caps; B3's delivery-dependent replacement; the email is sent before the answer (ADR 0014).
- **Web:**
  - **M1:** the gate is mounted once at `RootLayout` and covers the site, the dashboard and `*`. The only exemption is exactly `/change-password`. There is no loop, guests and a restoring session pass, and `next` is safe through `landingPath` / `returnUrlOf`.
  - **M2:** the form uses `useServerForm`, `PasswordRules` and `FormFailure`, and its components only render.
  - **M3:** `passwordChanged` does nothing for a signed-out session.
  - **M6:** landing is owned by `RequirePasswordChange`. There is no `onSuccess` and no navigating callback.
  - **Sign-out:** extracted into `useSignOutAction` and reused; no copy remains.
  - **Tests:** no test-only parameters, and the tests are laid out per layer.
- **Copy and docs:**
  - Both catalogues are complete, and the Arabic is listed for approval in the PR body.
  - ADR 0017 is short and decision-level. The API contract matches the shared schemas and the routes.
  - Nothing claims the web recovery screens are built; they are split to c2.
- **Commits** are atomic and Conventional, with no tool attribution.

## Tokens
Subagent 1: about 97,000. Subagent 2: about 124,000. This conversation: about 75,000. **Total: about 296,000**, under the 800,000 budget.
