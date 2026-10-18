F-5a review — fixes before merge (PR #25). The owner's review gate found the issues below. Every claim was checked in the code. Fix them in THIS conversation and on this same branch and PR. Each fix comes with its test, and each commit stays atomic. Then re-run every lane and update the PR's Evidence. Don't merge.

## A. Owner decisions (as approved)

D1. Google pre-registration takeover.
  - The risk: registration has no email verification, and Google links automatically to an account with a matching email. An attacker can register victim@gmail.com with their own password. When the victim later signs in with Google, the account is linked and the attacker's password still works.
  - Decision: on an AUTOMATIC link to an account that has a password, clear that password and revoke all of the account's sessions in the same transaction. The account becomes Google-only; its owner can set a new password from /me/password, as a Google-only account already can.
  - Record the rule and its reason in security.md › Sign-in methods. Add API tests: after the link, the old password fails, and the earlier sessions are gone.
  - F-5b's "accounts linked" toast should say that the password was removed. Add that line to F-5b's drafted entry.

D2. R2 (one public entry): amend conventions §8 R2 to admit what the composition root and the seed legitimately need from a module's index:
  - controller factories;
  - port adapters;
  - `hashPassword`, for the seed.

  Remove anything nothing outside the module uses, such as the unused TTL constants.

D3. R8: the sessions rotation and the password-change rules stay proven in the API lane, because they depend on database state. Add unit tests only for pure logic that has none today (see C10). Note in testing.md or conventions R8 that DB-dependent service rules are proven in the API lane.

D4. Remove the attacker-chosen name from the reset email's greeting, for example «مرحبًا،» / "Hello,". Without email verification, the name lets anyone place text in an email our sender delivers to any address. Record the divergence from the design in the PR.

D5. Record as findings, without building now:
  - the global email ceiling can be exhausted by one actor who registers many accounts (one actor can disable resets for everyone for a day);
  - a session has no absolute lifetime (each rotation grants 7 more days);
  - the reset email's copy lives outside the web copy catalogue.

  Finding 19 stays Open until the owner accepts it; don't mark it Accepted yourself.

D6. overview.md › Built: unchanged in this PR. Authentication becomes "Built" when F-5b makes it usable.

## B. Security and correctness fixes

B1. Rotation and revocation race (sessions.service.ts rotate, end, revokeAll; sessions.repository.ts).
  - The problem: under READ COMMITTED, a concurrent rotation's uncommitted successor survives a family or user delete. A logout or a revocation can then leave a live token.
  - The fix: serialize per user. Lock the user's row (FOR UPDATE) at the start of rotate, logout, family revocation and revokeAll, all inside a transaction. In rotate, re-read the token after the lock and treat a missing row as invalid. Use markRotated's result.
  - Prove it with a concurrency API test: logout in parallel with a refresh leaves no live token in the family.

B2. Failures-only sign-in limit is check-then-act (auth.service.ts limitFailures).
  - The problem: a burst of parallel attempts all pass the check before any failure is recorded.
  - The fix: count the attempt atomically BEFORE running it (refuse if over the limit), and on success take the hit back BEFORE the response. That stays inside ADR 0014, and successes still never count.
  - Prove it: N parallel wrong logins never exceed the limit.

B3. Forgot replaces the token before the email caps apply (auth.service.ts forgotPassword; cappedEmailSender.ts).
  - The problem: when a cap stops the send, the user's earlier link is already dead and no new one arrives.
  - The fix: decide the caps BEFORE issuing the token. Issue or replace the token only when the email will actually be sent. Keep the answer 202 in every case.
  - Prove it: after the cap, the last link the user received still works.

B4. replaceResetToken: run its delete and insert in one transaction. Give every repository function the optional `tx` that conventions §2 requires (users.repository: findCredentials, findByGoogleSubject, findByEmail, linkGoogle, findPasswordHash; sessions.repository: replaceResetToken, findResetTokenOwner).

B5. SMTP deadline (smtpEmailSender.ts).
  - The problem: the comment says the attempt is bounded, but it isn't: dnsTimeout defaults to 30 s, and socketTimeout only measures inactivity.
  - The fix: wrap sendMail in one overall deadline of about 10 s that resolves `{ sent: false }`, and set dnsTimeout.
  - Log only the error code or response code, never the error message, which some relays fill with the recipient's address.

B6. /me/password:
  - delete the user's unused reset tokens in the same transaction;
  - count CURRENT_PASSWORD_INCORRECT toward the per-account failure limit, as sign-in does.

B7. P2002 mapping: move it out of users.repository into the shared constraint table (shared/errors), keyed by constraint name. The email's unique key maps to EMAIL_TAKEN; the google_subject key never maps to EMAIL_TAKEN.

B8. Production environment hardening (config/env.ts):
  - `log` email mode requires NODE_ENV=development set explicitly, not by default;
  - TRUST_PROXY is required when NODE_ENV=production; F-7 sets Vercel's value.

  Test both refusals.

B9. Access token: verify with `requiredClaims: ['exp', 'sub']`, and set and check an issuer.

B10. The module-level lint rule has a hole (eslint.config.js): the default is `allow`, and `app.ts`, `db/` and `config/` are one "assembly" element. A module or shared/ can therefore import app.ts, and db/ can import any module. The fix:
  - forbid L0–L5, platform and unplaced code from importing app.ts, server.ts or test/;
  - separate db/seed from db/ (only the seed may import modules);
  - show the violation runs in the Evidence.

B11. Composition: move the choice of port implementations (Google verifier, email log or SMTP) from server.ts into the composition root (app.ts, or a factory it owns), so F-7's function entry stays thin and has nothing to duplicate (conventions §1, §12).

## C. Tests and docs

C1. Grace-sibling family: keep both concurrent tabs' tokens and assert that each one's family equals the original family, and that both die on logout and on reuse.

C2. Add one test with createTestApp({ secureCookies: true }): both Set-Cookie headers, and both clears, carry Secure.

C3. Unit tests for packages/shared:
  - textSchema: NFC normalisation, and every bidi-control range refused;
  - emailSchema: trimmed and lowercased;
  - passwordSchema.

  Add the test script packages/shared needs, wired into test:unit.

C4. ADR 0003: add a `Revised:` line. A session is now a family of refresh tokens, with grace siblings, not one row.

C5. Stale lines:
  - frontend/architecture.md: "F-5 builds the guards" becomes F-5b;
  - conventions §1: text normalisation lives in packages/shared;
  - api-contract §3: `service_unavailable` also covers Google not configured;
  - security.md: refresh failures clear the cookies on 401/403, not on 429, matching api-contract;
  - security.md: the per-token reset bucket does not limit guessing; the per-address bucket does.

C6. Rename the `describe('the request id')` blocks in front-desk.api.test.ts and payments.api.test.ts to "the idempotency key" (conventions §13).

C7. Commits: optional. Shorten 8f1597f's title only if it can be done without an interactive rebase; otherwise leave it.

C8. Arabic copy: the three error lines and the reset email are approved as written, except the greeting change in D4.

Update the PR description: the fixes made, the decisions D1–D6, the new findings, the Evidence (all lanes), and anything not done, with the reason.
