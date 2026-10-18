# F-5a · PR #25: second independent review

**Reviewed:** commit `e56664f` (branch `feat/auth-api`) against its base, `origin/main` `c427112`: 10 commits, 92 files. Read-only: nothing was run. 2026-10-02.

**How:** I read the project's documents at `e56664f`, the approved plan with its owner amendments, and the decisions approved during the work, and then the code. Nine reviewer subagents covered the eleven axes in parallel. Their 81 raw findings are merged here into 34 items. I verified the three blockers myself in the code. The adversarial verification pass was stopped at the owner's request, so every item states its status:

- **VERIFIED**: I confirmed it myself in the snapshot of `e56664f`. The three blockers were confirmed today; the other items during my own reading of the code and documents.
- **PARTLY VERIFIED**: I confirmed the code facts myself. The parts marked as *reported* come from a reviewer, and I did not re-check them.
- **UNVERIFIED**: a reviewer reported it with a `file:line` quote, and I did not re-check it. None of the stopped verification pass's partial results is used.

Line numbers are at `e56664f`. "L" means a line in a document.

---

## 1. Verdict

- **Not merge-ready.** There are three blockers in the security core:
  - one concurrent burst bypasses the sign-in brute-force limits (B1);
  - a reset or password change does not reliably end a session opened at the same moment, so an attacker who knows the old password survives the victim's reset (B2);
  - four anonymous requests an hour keep any account's reset links dead (B3).
- **One owner decision is needed before merge.** Automatic Google linking adopts an account an attacker pre-registered, and the attacker's password keeps working (Q1).
- **The rest is sound or fixable here.** The module structure, the reset-token core, the refresh families, the request id and the redaction are sound. Every other item can be fixed in this PR.

---

## 2. Findings by severity

| Id | Severity | Status | Finding |
|---|---|---|---|
| B1 | BLOCKER | VERIFIED | Sign-in failure limits are check-then-act: one concurrent burst bypasses them |
| B2 | BLOCKER | VERIFIED | A reset or password change does not reliably end a session opened at the same moment |
| B3 | BLOCKER | VERIFIED | Forgot deletes the delivered reset link before the caps decide |
| S1 | SHOULD-FIX | VERIFIED | Production protections hang on `NODE_ENV`, whose default fails open |
| S2 | SHOULD-FIX | VERIFIED | The environment-to-ports mapping lives in `server.ts`, not in the composition root |
| S3 | SHOULD-FIX | VERIFIED | `auth.forgotPassword` re-implements users' "may sign in" rule |
| S4 | SHOULD-FIX | VERIFIED | Every unique violation becomes `EMAIL_TAKEN`, so a double first Google sign-in answers an undocumented 409 |
| S5 | SHOULD-FIX | VERIFIED | Seven new repository functions take no `tx` |
| S6 | SHOULD-FIX | VERIFIED | `refresh_tokens` keeps a row per refresh of every live session; finding 17 misstates it |
| S7 | SHOULD-FIX | PARTLY VERIFIED | Bare catches turn infrastructure failures into client outcomes |
| S8 | SHOULD-FIX | VERIFIED | `textSchema` says "one line" but accepts line breaks and control characters |
| S9 | SHOULD-FIX | PARTLY VERIFIED | No service is unit-tested with fakes (R8 and the plan dropped silently) |
| S10 | SHOULD-FIX | UNVERIFIED | Specific test gaps and vacuous cases |
| S11 | SHOULD-FIX | PARTLY VERIFIED | The ESLint level rule lets modules and `shared/` import the composition root, and CI cannot see it regress |
| S12 | SHOULD-FIX | VERIFIED | Documents claim more than is built or true |
| S13 | SHOULD-FIX | VERIFIED | api-contract §5 omits answers the endpoints give; §3 does not cover the new 503 |
| S14 | SHOULD-FIX | VERIFIED | Owning documents not updated for the structure this PR built |
| N1 | NIT | PARTLY VERIFIED | Two timing claims are untrue as written |
| N2 | NIT | UNVERIFIED | The password policy counts characters; bcrypt keeps 72 bytes |
| N3 | NIT | PARTLY VERIFIED | A cross-site form post to logout or refresh clears the session cookies |
| N4 | NIT | UNVERIFIED | Dead outputs and unused exports |
| N5 | NIT | VERIFIED | Second owners for facts that already have one |
| N6 | NIT | VERIFIED | Names and comments that say something else |
| N7 | NIT | VERIFIED | Commit history breaks workflow §3, and the PR says otherwise |
| N8 | NIT | PARTLY VERIFIED | `sessions` (L0) hard-codes the auth router's URL as the cookie Path |
| N9 | NIT | VERIFIED | Controllers cast `req.body` with no link to their route's schema |
| N10 | NIT | VERIFIED | A pending reset link survives a password change |
| Q1–Q7 | QUESTION | see §3 | Decisions for the owner |

### BLOCKER

#### B1: Sign-in failure limits are check-then-act, so one concurrent burst bypasses them
- **Axis:** Security (brute force) · **Severity:** BLOCKER · **Status:** VERIFIED
- **Where:**
  - `apps/api/src/modules/auth/auth.service.ts:97-104`
  - `apps/api/src/shared/rate-limit/limiter.ts:33-40`
  - `apps/api/src/shared/rate-limit/counter.ts:42-46`
  - the general guest limit, `apps/api/src/app.ts:44-48`
  - the only limit test is sequential, `apps/api/src/modules/auth/auth.api.test.ts:223`

  ```ts
  // auth.service.ts:97-104
  await limiter.check(SIGN_IN_ADDRESS, address);
  if (email !== undefined) await limiter.check(SIGN_IN_ACCOUNT, address, email);
  try {
    return await attempt();
  } catch (error) {
    if (error instanceof AppError && error.status < 500) {
      await limiter.recordFailure(SIGN_IN_ADDRESS, address);
      if (email !== undefined) await limiter.recordFailure(SIGN_IN_ACCOUNT, address, email);
  // counter.ts:43-44, what check() runs
  SELECT hits, reset_at FROM rate_limits WHERE key = ${key} AND reset_at > now()
  ```
- **Problem.**
  - `check` is a plain `SELECT`. The failure is written only after the attempt: a cost-12 bcrypt compare for login, or a cost-12 hash for register.
  - Nothing reserves a slot. Every request whose check runs before the first failures are written goes through.
  - So the documented limits (10 failures per address + email, 50 per address, per 15 min) hold only for a client that waits for each answer. The only atomic bound left is the general guest limit: 1,200 per address per 15 min.
  - Owner amendment 1 approved `skipSuccessfulRequests` semantics: count every attempt, give the successes back. That has no such race. What was built is different, and security.md L88 now documents the racy version.
- **Failure scenario.**
  - The attacker has one IP and the victim's email. They send about 1,200 `POST /auth/login` at once, each with a different password.
  - Each request's two `SELECT`s finish in milliseconds. bcrypt runs four at a time, about 0.25 s each. So every check passes before ten failures exist.
  - All 1,200 passwords are tried, and the account locks only afterwards.
  - Repeated every window, that is about 115,000 guesses a day from one address, instead of 960.
  - The same burst spread over 1,200 emails sprays 1,200 accounts instead of 50.
  - On serverless, parallel instances widen the gap further.
  - Register (`EMAIL_TAKEN`) and Google share `limitFailures`, so they have the same gap.
- **Rule.**
  - security.md › Rate limits: L76-77 (10 and 50 failures per 15 min) and L87 ("Every count is one atomic statement on its key").
  - The plan's owner amendment 1 (L9, `skipSuccessfulRequests`).
  - ADR 0015 decision 5, and › Alternatives L44: "a check before the write races … so only the database's check holds".
- **Fix.** Reserve, then refund, with every write before the answer (ADR 0014).
  - In `limitFailures`, replace both `check` calls with `limiter.count`, the atomic upsert that refuses once over the limit. Count the address first, then the account. If the account key refuses, give back the address slot.
  - When the attempt succeeds, or fails with a 5xx, give both slots back before returning, one statement per key: `UPDATE rate_limits SET hits = hits - 1 WHERE key = $1 AND reset_at = $2 AND hits > 0`. Here `$2` is the `reset_at` the hit returned, so a refund never lands in the next window.
  - A 4xx keeps its slot as the failure.
  - Remove `check` and `peek`.
  - Rewrite security.md L88: "a failures-only limit reserves each attempt and returns it on success, before answering".
  - API tests:
    - `Promise.all` of 20 wrong-password logins for one account gives exactly ten 401s and ten 429s;
    - 20 parallel correct logins all answer 200 and leave no count.

#### B2: A reset or password change does not reliably end a session opened at the same moment
- **Axis:** Security, database concurrency (READ COMMITTED) · **Severity:** BLOCKER · **Status:** VERIFIED
- **Where:**
  - **Login** reads the hash outside any transaction, then runs bcrypt: `apps/api/src/modules/users/users.service.ts:77-78`. It then inserts a new family in autocommit statements: `apps/api/src/modules/auth/auth.service.ts:84` → `apps/api/src/modules/sessions/sessions.service.ts:50-55`.
  - **Revocations** are single `DELETE`s, by family or by user: `apps/api/src/modules/sessions/sessions.repository.ts:58-64`. They run in the reset (`auth.service.ts:196-201`) and the password change (`users.service.ts:168-172`).
  - **Rotation** reads its token without a lock, and ignores whether `markRotated` matched: `sessions.service.ts:66`, `:74`, `:77`.
  - **Logout** finds, then deletes, in two autocommit statements: `sessions.service.ts:82-85`.
  - **The password change** checks outside its transaction (`users.service.ts:155-165`), then writes unconditionally (`:169` → `apps/api/src/modules/users/users.repository.ts:75-81`).
- **Problem.**
  - Under READ COMMITTED, a `DELETE` removes only rows committed before its statement began.
  - Nothing makes a writer of new refresh tokens wait for a revocation, or re-check after it.
  - A login verifies the password against a hash it read before bcrypt, then inserts a new family.
  - A later refresh re-checks only suspension (`auth.service.ts:147-149`), so that family lives on.
- **Failure scenario.**
  - **(a) Login racing a reset.**
    - The attacker knows the victim's password P (phished, reused, or read over a shoulder in a coworking space). They loop `POST /auth/login {victim, P}`.
    - The sign-in limits never count successful logins. Only the guest limit does, at about 1.3 requests per second per address.
    - Each login spends about 0.25–0.5 s in bcrypt between its read and its `INSERT`. With one or two addresses, a login is almost always in flight.
    - The victim resets by email. One transaction consumes the token, updates `users`, deletes `refresh_tokens WHERE user_id`, and commits. The API answers 204, "every session of the user ended".
    - A login that read hash(P) before that commit inserts its family after it.
    - The attacker then rotates 7-day tokens indefinitely, past the reset meant to evict them.
  - **(b) Logout racing a refresh.**
    - Tab B inserts the successor. Tab A's `DELETE` took its snapshot before B's commit, so it misses the successor.
    - B's 200 sets `masaha_refresh` again, after A's 204 cleared it.
    - On a shared coworking computer, the next person opens Masaha signed in.
  - **(c) Password change racing a reset.**
    - A caller with the old password and a live access token calls `/me/password`. It reads the hash, spends about 0.5 s in bcrypt, then overwrites the password.
    - A reset that committed in between is undone.
- **Rule.**
  - security.md › Tokens and cookies:
    - L13: logout ends the family;
    - L15: reuse deletes the family;
    - L18: a password change or reset deletes all the user's refresh tokens.
  - api-contract §5 L121.
  - ADR 0015 decisions 5-6 (L22-23) and conventions §13 L330-331: constraints and row locks, taken in one fixed order, are the guarantee.
  - No test runs a sign-in, refresh or logout concurrently with a revocation.
- **Fix.** Every transaction that writes a user's refresh tokens takes one per-user lock first, in one fixed order: the `users` row, then the tokens.
  - **Locking read.** Give `users`, which owns the row (R1), a locking read: `SELECT password_hash, suspended_at FROM users WHERE id = $1 FOR NO KEY UPDATE`.
  - **Login.** bcrypt stays outside the transaction. Then, in `runInTransaction`:
    1. lock the row;
    2. check that the stored hash still equals the one bcrypt matched (equality only), and that the account is not suspended;
    3. `sessions.issue(…, tx)`.
  - **Register and Google.** Issue under the same lock.
  - **Refresh.** Lock the token's user first, then rotate. A revocation that committed first is then seen as "invalid". Assert `markRotated`'s result.
  - **Logout, and the suspended-refresh `revokeAll`.** Run them in a transaction behind the same lock.
  - **Reset and `/me/password`.** They already lock the row through their `UPDATE users`. Make `/me/password`'s write a compare-and-set: `… WHERE id = $1 AND password_hash IS NOT DISTINCT FROM $checked AND must_change_password = $checkedFlag`. When no row matches, answer `CURRENT_PASSWORD_INCORRECT`.
  - **Dependency.** This needs S5.
  - **Tests.** Prove each interleaving with API tests that hold the user row in a test transaction while the login, refresh or logout runs.
  - **Alternative without locks.** A per-user session epoch: read with the hash, stored on each token, checked at refresh. It needs a migration and owner approval.
  - **Documentation.** Record the mechanism in conventions §13.

#### B3: Forgot deletes the delivered reset link before the caps decide, so anyone can switch off a user's recovery
- **Axis:** Security (reset-token lifecycle, email abuse) · **Severity:** BLOCKER · **Status:** VERIFIED
- **Where:**
  - `apps/api/src/modules/auth/auth.service.ts:171-174`: issue, then send; the result is discarded.
  - `apps/api/src/modules/sessions/sessions.repository.ts:74-77`: delete the unused links, then insert, in two autocommit statements.
  - `apps/api/src/modules/auth/email/cappedEmailSender.ts:37-41`: the recipient cap refuses, with no log line.
  - The cap test only counts emails: `apps/api/src/modules/auth/password.api.test.ts:98-104`.

  ```ts
  // auth.service.ts:171-174
  const token = await sessions.issueResetToken(account.id);
  await email.send(
    resetEmail({ to: account.email, name: account.name, link: resetLink(webOrigin, token) }),
  );
  // sessions.repository.ts:75-76
  await db.passwordResetToken.deleteMany({ where: { userId, usedAt: null } });
  await db.passwordResetToken.create({ data: { userId, tokenHash, expiresAt } });
  ```
- **Problem.**
  - The live link is replaced before anything decides whether the new one will be sent.
  - When the per-inbox cap (3 an hour), the daily ceiling (100) or SMTP refuses, the link already in the inbox is gone and the new one never leaves. Forgot still answers 202.
  - Separately, two concurrent forgots both delete and both insert, which leaves two live links.
- **Failure scenario.**
  - **An attacker.**
    - Anyone who knows victim@x sends 4 forgots within a few seconds. Five per 15 min per address + email are allowed.
    - Three emails go out, each ending the previous link. The 4th ends link 3 and is capped.
    - Every link in the inbox now answers `RESET_TOKEN_INVALID`, and the victim's own forgot is capped for the rest of the hour.
    - Repeated hourly, self-service recovery is off for that account indefinitely, and silently.
  - **No attacker at all.** A user who taps "send again" a 4th time while Gmail is slow loses every link, for up to an hour.
  - **The ceiling.** Once the daily ceiling trips (Q4), every user's forgot deletes their delivered link.
- **Rule.**
  - security.md › Passwords:
    - L45: the reset follows the OWASP Forgot Password Cheat Sheet;
    - L46: "Asking again ends the earlier link: one live link per account". Here the earlier link ends although nothing replaces it;
    - L56: the caps protect people. Here they deny them recovery.
  - A reviewer quotes OWASP: "Do not make a change to the account until a valid token is presented". I did not re-check the wording.
  - **On severity:** the reviewers split, five SHOULD-FIX and one BLOCKER. I rate it BLOCKER because it needs no account, no credential and only four requests an hour, and the fix is small.
- **Fix.** Make the replacement depend on delivery, all before the 202 (ADR 0014).
  - `sessions.issueResetToken` only inserts, and returns the token and its id.
  - `forgotPassword` reads the `EmailResult`:
    - on `sent: true`, end the user's other unused links in one statement: `DELETE … WHERE user_id = $1 AND used_at IS NULL AND id < $new`. This also makes concurrent forgots converge on one live link;
    - on `sent: false`, delete the new token, so the delivered link stays live.
  - Log every refusal once, with a fixed reason and no address (S7).
  - Reword security.md L46: "a delivered link ends the earlier one".
  - Tests:
    - after a 4th forgot within the hour, the 3rd link still checks 200 and resets;
    - two concurrent forgots leave one live link.

### SHOULD-FIX

#### S1: Production protections hang on `NODE_ENV`, whose default fails open
- **Axis:** Security, environment · **Status:** VERIFIED
- **Where:**
  - `apps/api/src/config/env.ts:11`: `NODE_ENV … .default('development')`
  - `:34`: `EMAIL_MODE … .default('log')`
  - `:48-54`: Google is required only in production
  - `:57-63`: log mode is refused unless in development
  - `:25-28`: `TRUST_PROXY` defaults to `'loopback'` everywhere
  - `apps/api/src/server.ts:45`: `secureCookies: env.NODE_ENV === 'production'`
- **Problem.**
  - This PR makes `NODE_ENV` decide three things: whether log mode is allowed, whether Google is required, and whether cookies are Secure.
  - A missing `NODE_ENV` silently becomes `development`, which switches off all three protections.
  - `TRUST_PROXY` is not required in production.
- **Failure scenario.**
  - **Missing `NODE_ENV`.** F-7's Vercel project sets the secrets and `SMTP_*`, but not `EMAIL_MODE`, and `NODE_ENV` does not reach the function.
    - The API boots as development.
    - Every forgot writes a live one-hour reset link into the runtime log, delivers nothing, and still answers 202.
    - Cookies lack Secure.
  - **`TRUST_PROXY` wrong.**
    - If it stays `'loopback'` behind Vercel's proxy, every client shares one address. Anyone's 50 failures then lock every sign-in, platform-wide.
    - If it is set too trusting, `X-Forwarded-For` forges any address past every per-IP limit.
- **Rule.**
  - security.md › Passwords L55: "Production refuses to start unless the mode can deliver".
  - The approved email decision.
  - security.md L16: Secure in production.
  - conventions §1: config fails fast.
- **Fix.** Fail closed.
  - Drop `NODE_ENV`'s default; `.env.example` and Vitest already set it.
  - Make cookies Secure unless `NODE_ENV === 'development'`.
  - Require `TRUST_PROXY` when `NODE_ENV=production`.
  - Add an env unit test for each refusal.

#### S2: The environment-to-ports mapping lives in `server.ts`, not in the one composition root
- **Axis:** Architecture (composition root) · **Status:** VERIFIED
- **Where:**
  - `apps/api/src/server.ts:43-63`
  - `apps/api/src/app.ts:96-121`: `ApiOptions` takes finished adapters
  - `apps/api/src/config/env.ts:64-74` with `server.ts:53-58`: the `?? ''` fallbacks
- **Problem.**
  - `server.ts` chooses the email adapter by `EMAIL_MODE`, with its SMTP settings. It builds the Google identity, and derives `secureCookies`, `trustProxy` and `webOrigin`.
  - `createApi` only receives finished objects.
  - The conventions give port wiring to `app.ts` and keep the entry thin. The plan said `app.ts` wires the email adapter by mode, and the verifier.
  - The PR does not list this divergence.
  - The smtp guarantee lives in `superRefine`, not in the type.
- **Failure scenario.**
  - F-7's function entry must re-create `server.ts:43-63`.
  - If it wires `createLogEmailSender`, production writes reset links into the logs, although `loadEnv` passed with `EMAIL_MODE=smtp`.
  - If it omits `trustProxy`, see S1.
  - If it omits `google`, `/auth/google` answers 503 even though `GOOGLE_CLIENT_ID` is set.
  - No test catches any of these, because `test/app.ts` is a third composition.
- **Rule.**
  - conventions §1 L12-17, and §12 L303: "One composition root … Only a thin entry differs".
  - ADR 0014 decision 2.
  - The plan: L82, L114, L121.
  - CLAUDE.md: overrides are stated, never silent.
- **Fix.**
  - Move the mapping into `app.ts`, as one function both entries call, for example `createApiFromEnv(env, logger)`.
  - Keep the injection points for tests.
  - Parse the email settings in `env.ts` as a discriminated union, `{ mode: 'log' } | { mode: 'smtp'; settings }`, so the `?? ''` fallbacks disappear.

#### S3: `auth.forgotPassword` re-implements users' "may sign in" rule
- **Axis:** Architecture (ADR 0013, module ownership) · **Status:** VERIFIED
- **Where:**
  - `apps/api/src/modules/auth/auth.service.ts:170`: `if (!account || account.suspendedAt) return;`
  - `apps/api/src/modules/users/users.service.ts:51-53`: `assertMaySignIn`
  - `apps/api/src/modules/users/index.ts:4`: exports `Account`, a Prisma payload type
- **Problem.**
  - Every other flow asks `users`, through `assertMaySignIn`.
  - Forgot reads `suspendedAt` itself, because `assertMaySignIn` throws and forgot must not.
  - The exported Prisma payload type makes the duplication easy.
- **Failure scenario.**
  - The admin slice adds a blocking state to `assertMaySignIn`.
  - Login, Google and refresh follow it.
  - Forgot keeps mailing reset links to accounts that `users` now refuses, and no test fails.
- **Rule.**
  - ADR 0013 › Consequences (L25): "The sign-in flows hold no rules of their own about accounts. A rule about who may sign in lives in users".
  - The service's own docstring, `auth.service.ts:53`.
- **Fix.**
  - Add `users.maySignIn(account): boolean`, and build `assertMaySignIn` on it.
  - Have forgot call `maySignIn`.
  - Optionally, export a domain `Account` type instead of the Prisma payload.

#### S4: Every unique violation becomes `EMAIL_TAKEN`, so a double first Google sign-in answers an undocumented 409
- **Axis:** Code quality, contract, concurrency · **Status:** VERIFIED. The code is checked; the race is reasoned from it.
- **Where:**
  - `apps/api/src/modules/users/users.repository.ts:87-96`: P2002 → `EMAIL_TAKEN`
  - `apps/api/src/modules/users/users.service.ts:113-121`: the Google create
  - `:100-111` with `users.repository.ts:64-66`: the link, a read then an unconditional update
  - `docs/api/api-contract.md:95`
- **Problem.**
  - The repository picks the domain answer for any unique violation, on the email or on `google_subject`.
  - `create` serves both register and the first Google sign-in.
  - The Google lookups and create handle no conflict.
- **Failure scenario.**
  - A new user double-taps "Sign in with Google", or the web retries on a weak connection.
  - One request answers 200. The other answers 409 `EMAIL_TAKEN` with `errors.email`, a code `/auth/google` does not document.
  - `limitFailures` counts it as a failure on the shared address.
- **Rule.**
  - conventions §2 L52: a repository never holds rules.
  - conventions §4 L67-68: P2002 → `NOT_UNIQUE`, through one constraint-name table.
  - api-contract §5 L95.
  - ADR 0015 decision 3: a retry returns the first result.
- **Fix.**
  - The repository reports which constraint failed.
  - Register maps only the email constraint to `EMAIL_TAKEN`.
  - The Google create re-reads by subject on a conflict, and signs that account in.
  - The link uses `updateMany({ where: { id, googleSubject: null } })` and re-reads when nothing changed. The same subject signs in; another subject answers `GOOGLE_TOKEN_INVALID`.
  - Add an API test with two concurrent first sign-ins.

#### S5: Seven new repository functions take no `tx`
- **Axis:** Code organization, database · **Status:** VERIFIED
- **Where:**
  - `apps/api/src/modules/users/users.repository.ts`: `:35` `findCredentials`, `:47` `findByGoogleSubject`, `:52` `findByEmail`, `:64` `linkGoogle`, `:69` `findPasswordHash`
  - `apps/api/src/modules/sessions/sessions.repository.ts`: `:74` `replaceResetToken`, `:80` `findResetTokenOwner`
- **Problem.**
  - They query `db` only, against the repository contract.
  - No orchestrator can put them in its transaction.
- **Failure scenario.**
  - The B2, B3 and S4 fixes need these functions inside a transaction.
  - For example, a Google link under B2's user-row lock would run its `UPDATE` on a second connection. That connection waits for the lock its own transaction holds, and the request hangs until Prisma's 5 s timeout, then answers 500.
- **Rule.** conventions §2 L52 ("each function accepts an optional `tx`") and §8 L179.
- **Fix.**
  - Add `tx: Tx = db` to the seven functions.
  - Thread an optional `tx` through the service methods that call them.

#### S6: `refresh_tokens` keeps a row per refresh of every live session, and finding 17 misstates it
- **Axis:** Database, operations · **Status:** VERIFIED. The code is checked; the growth figures are estimates.
- **Where:**
  - `apps/api/src/modules/sessions/sessions.service.ts:50-55`: the only caller of `deleteExpired`, which runs at a new sign-in or a password change
  - `:64-79`: rotate inserts, and never deletes
  - `apps/api/src/modules/sessions/sessions.repository.ts:75`: deletes only unused reset tokens
  - `docs/architecture/findings.md:247`
- **Problem.**
  - A session that keeps refreshing never signs in again, so every rotated row stays as long as the session lives.
  - Finding 17 blames only abandoned sessions.
  - Used reset tokens are never deleted.
- **Failure scenario.**
  - A desk tab refreshes every 15 min, plus once per page load. That is about 50 rows a day, about 15k a year, and about 5 MB per tab per year at roughly 350 B a row with its five indexes (estimate).
  - Twenty spaces with two tabs each come to about 200 MB a year, against Neon's 0.5 GB.
  - Beyond 0.5 GB, writes are blocked. The general limiter writes on every request, so the whole API then fails.
  - Logging out a year-old desk family deletes about 15k rows inside one request.
- **Rule.**
  - ADR 0014 › Deviations › Database.
  - CLAUDE.md "Claim only what is true": finding 17 was written in this PR.
- **Fix.**
  - Call `repository.deleteExpired(stored.userId, at, tx)` inside rotate. It is one `DELETE` on the `user_id` index. Expired tokens are already answered "invalid", so no answer changes.
  - Delete used reset tokens in the reset transaction.
  - Correct finding 17's evidence.
  - Add an API test that a refresh removes the user's expired tokens.

#### S7: Bare catches turn infrastructure failures into client outcomes
- **Axis:** Code quality (error handling), security · **Status:** PARTLY VERIFIED. The code is mine; the jose and nodemailer internals are reported.
- **Where:**
  - `apps/api/src/modules/auth/google.ts:50-52`: a catch-all → `undefined`
  - `apps/api/src/modules/auth/auth.service.ts:133-135` and `:102`: → 401 `GOOGLE_TOKEN_INVALID`, counted because it is below 500
  - `apps/api/src/modules/auth/email/cappedEmailSender.ts:37-41`: an error at the recipient step returns with no log line
  - `cappedEmailSender.ts:42-46`: any error at the ceiling step logs "[email:ceiling] the daily email ceiling is reached"
  - `auth.service.ts:172-174`: the `EmailResult` is discarded
  - `apps/api/src/modules/auth/email/smtpEmailSender.ts:43`: the reason is `error.message`
- **Problem.**
  - A failure to fetch Google's keys (a timeout, a network error, or a non-200, thrown inside `jwtVerify` by the remote key set) is answered as the user's bad token, and counted as a sign-in failure on the shared address.
  - The email caps cannot tell a database error from a cap.
  - An unsent email can leave no trace.
  - The SMTP reason is nodemailer's free text. Reported: it can include the recipient address, while the comment at `cappedEmailSender.ts:49` says the log keeps addresses out.
- **Failure scenario.**
  - Google's key endpoint is slow from the region for a few minutes.
  - Fifty people at one coworking space see "invalid Google token".
  - `SIGN_IN_ADDRESS` (50 per 15 min) trips, and every password sign-in from that space answers 429 for the rest of the window.
  - The logs show only 401 warnings.
- **Rule.**
  - api-contract §5 L95: `GOOGLE_TOKEN_INVALID` is "for a token that fails verification", and 503 is the answer for unavailability.
  - security.md › Rate limits: only failed attempts count.
  - security.md › Passwords L47: "a failed send is only logged".
  - conventions §4: unknown errors are logged.
- **Fix.**
  - In `google.ts`, return `undefined` only for jose's token-rejection errors (expiry, claims, signature, invalid token, algorithm, no matching key), and rethrow the rest. Auth maps those to `AppError.serviceUnavailable`, which is not counted.
  - In the decorator:
    - treat only an `AppError` of type `rate_limit` as a cap;
    - log anything else as an error;
    - log exactly one warn line per unsent email, with a fixed reason and nodemailer's `code`, `responseCode` and `command`, never its message.
  - Add unit tests with a rejecting key set and a throwing counter.

#### S8: `textSchema` says "one line" but accepts line breaks and control characters
- **Axis:** Security, validation · **Status:** VERIFIED
- **Where:**
  - `packages/shared/src/text.ts:5-16`: refuses only bidi controls; the comment at `:7` reads "One line of user text"
  - used for the account's name (`packages/shared/src/auth.ts:18`)
  - greeted in the reset email: `apps/api/src/modules/auth/email/resetEmail.ts:55`, `:75`
- **Problem.**
  - A name may contain line breaks and other control characters, which the schema's own description rules out.
  - The name then lands in the reset email's text and HTML.
- **Failure scenario.**
  - Register with the name "Sara\nYour account is locked, restore it at evil.example", then ask for a reset.
  - Masaha's genuine Gmail sends that sentence on its own line (Q4).
- **Rule.** `text.ts:7`; conventions §3 L61.
- **Fix.**
  - Also refuse Unicode control characters (category Cc, line breaks included), failing with `invalid_format`.
  - Add a unit test in `packages/shared`.

#### S9: No service is unit-tested with fakes, so R8 and the plan were dropped silently
- **Axis:** Tests · **Status:** PARTLY VERIFIED. The absence and the rules are checked; the unpinned behaviours are reported.
- **Where:**
  - There is no `*.unit.test.ts` for the sessions, users or auth services. The PR's unit tests cover env, `accessToken`, `requireAuth`, `requestLogging`, `clientAddress`, the limiter, `cappedEmailSender`, `resetEmail` and `google`.
  - `docs/backend/conventions.md:173` (R8); `docs/development/testing.md:21`; the plan, L257 ("the users service rules with fakes").
  - The PR's Definition of Done ticks "Tests in the owning lanes".
- **Problem.**
  - Every service rule is proven only through the API lane.
  - The injectable seams (sessions' `now` and repository, users' repository and sessions) are passed by nobody.
- **Failure scenario.** Reported: each of these changes passes the whole suite.
  - The in-grace test refreshes at about 0 s and reuse is tested at 31 s, so `ROTATION_GRACE_MS = 1_000`, or `>` turned into `>=`, passes.
  - Tests overwrite `expiresAt`, so a 24 h reset TTL passes.
  - No test links a suspended account by email.
  - A refactor that returns early on `!found` passes. It reopens the timing enumeration that security.md L34 says is closed.
- **Rule.** conventions §8 R8; testing.md §1-§2; the plan › Verification › Unit; workflow §5 (Definition of Done); CLAUDE.md (an override is stated, never silent).
- **Fix.** Either of:
  - Add unit tests for the sessions, users and auth services, with plain-object fakes and a fixed `now`. Cover:
    - the grace at 30,000 vs 30,001 ms, and the TTLs;
    - the credential order and the dummy compare;
    - every Google branch;
    - the current-password rule;
    - how `limitFailures` counts a 4xx, a 5xx and a success.
  - Or state the deviation in the PR and record it.

#### S10: Specific test gaps and vacuous cases
- **Axis:** Tests · **Status:** UNVERIFIED, except (b), which I verified
- **Where (reported):**
  - `apps/api/src/modules/auth/password.api.test.ts:120-128` (the expired-link check) and `:98-104` (the cap)
  - `apps/api/src/modules/auth/auth.api.test.ts:348-366` (refresh 429) and `:406-435` (redaction)
  - `apps/api/test/app.ts:37` (`secureCookies: false` everywhere)
- **Problem and failure scenario.**
  - **(a)** The check endpoint's "expired" case expires the token, then calls forgot again, which deletes it. Check then sees an unknown token. Removing `expiresAt: { gt: now }` from `findResetTokenOwner` (`sessions.repository.ts:82`) passes every test.
  - **(b)** The cap test never checks that the delivered link survives (B3).
  - **(c)** There is no 429 test for password-address (50) or general-user (300).
  - **(d)** No test refreshes an account whose password change is pending, though security.md L43 says it works.
  - **(e)** No test builds the cookies with `secure: true`.
  - **(f)** No test reads `userId` and role from a log line.
  - **(g)** No test uses a sender that throws. The decorator awaits `inner.send` unguarded (`cappedEmailSender.ts:48`), so a throwing adapter would answer 500 only for existing accounts.
  - **(h)** The refresh-429 test cannot tell a limit applied before the rotation from one applied after it.
  - **(i)** The redaction test's `PASSWORD` assertion can never fail, because bodies are never logged. Header redaction is proven three times, and the 3-an-hour cap twice.
- **Rule.** testing.md §1 (one behaviour, one lane; the deletion check); the plan › Verification ("429 per scope").
- **Fix.** Per item:
  - give the expired case its own account, and assert the expired row still exists when it is checked;
  - extend the cap test (B3);
  - add the two 429 tests and a pending-account refresh;
  - add a `secure: true` cookie unit test and a log-field assertion;
  - add a try/catch in the decorator, with a rejecting-sender test;
  - assert `rotatedAt` is still null after a refresh 429;
  - drop the redundant proofs.

#### S11: The ESLint level rule lets modules and `shared/` import the composition root, and nothing in CI proves the rule still works
- **Axis:** Architecture (level rule) · **Status:** PARTLY VERIFIED. The configuration and the two imports below are mine; the plugin's edge cases are reported.
- **Where:**
  - `eslint.config.js:127-129`: `assembly` covers `db`, `config`, `test` and everything else under `src`
  - `:136`: `default: 'allow'`
  - `:142-149`: the only `disallow` targets module elements
  - `apps/api/src/shared/validation/validate.api.test.ts:7` and `apps/api/src/modules/users/users.api.test.ts:14`: `import { createApp } from '../../app.ts'`, accepted by the PR's clean lint run
- **Problem.**
  - No policy forbids an import *to* `assembly`. Any module or `shared/` file may therefore import:
    - `app.ts`, which imports every module;
    - `test/app.ts`;
    - `db/seed`, which imports `users`.

    Each of these reaches higher levels transitively. `shared/` importing the root defeats R6.
  - The plan asked for separate root and db elements.
  - Reported: a file placed directly in `modules/` or `shared/` is classified as `assembly`, not `unplaced`.
  - The rule was proven once, with temporary files. CI has no regression test, and an import the plugin cannot resolve is allowed by the default.
- **Failure scenario.**
  - A file in `modules/sessions` (L0) imports `../../app.ts` for a helper. Lint passes. The ESM graph gains the cycle `app.ts → sessions → app.ts`, and sessions now loads auth (L3).
  - `shared/http` imports from `app.ts`. Lint passes, although conventions §7 L108 says any module import from `shared/` fails lint.
- **Rule.** conventions §7 L108, R3 and R6; engineering-principles §3 (no cycles; `index.ts` only); ADR 0012 ("enforced by tooling"); the plan › Level rule (L156-165).
- **Fix.**
  - Split `assembly` into two element types:
    - `infrastructure`: `db`, `config` and `generated`. Modules and `shared/` may import it, `db` and `config` only through `index.ts`;
    - `root`: `app.ts`, `server.ts`, `test/` and `db/seed`. Only `root` may import it.
  - Disallow modules, platform and infrastructure → root. If tests may compose the app, exempt `*.test.ts` in their own block.
  - Classify a file placed directly under `modules/` as `unplaced`.
  - Add a unit-lane test that lints in-memory probe files with ESLint's Node API: one per violation kind of the PR's evidence, plus the allowed imports.

#### S12: Documents claim more than is built or true
- **Axis:** Documentation · **Status:** VERIFIED
- **Where:**
  - `docs/backend/security.md`: `:3` (the status line), `:15` (the Reuse row), `:18` (the Revocation row), `:58` (the admin's recovery), `:64` (`requireRole`)
  - `docs/architecture/data-model.md:36`
  - `docs/architecture/findings.md`: `:247` (17), `:255` (18), `:263` (19)
  - `apps/api/src/modules/auth/email/resetEmail.ts:15-16`: the font stacks
- **Problem.**
  - **(1) The status line.** security.md's status line, written in this PR, lists as unbuilt only suspension and role changes, the upload limits and the data-report limit. So these read as built, and none exists:
    - `requireRole` (no `requireRole` anywhere in `apps/api/src`);
    - the temporary passwords created by the owner or the admin;
    - the admin's recovery and its audit;
    - the revocation when a reception link is deactivated (`space-links` has only `findActiveLinks`).
  - **(2) Rate-limit keys.** data-model.md:36 says a rate-limit key "names no one". An unsalted SHA-256 of an IPv4 address is reversed by hashing all 2^32 addresses.
  - **(3) Finding 17** misses the main growth source (S6).
  - **(4) Finding 18** cites R1 for "reads only its own table". R1 limits writes. The reading restriction is the repository's (§2), and `space-links` (L2) may call `spaces` (L1).
  - **(5) Finding 19** is "Accepted" for seven colours. But the email also hard-codes two font stacks and all its inline CSS. CLAUDE.md forbids "colours, fonts or CSS" outside the design system, and accepting a deviation is the owner's call.
  - **(6) The Reuse row.** security.md:15's "Ending only the family still cuts a stolen chain" does not hold within the grace (Q5).
- **Failure scenario.** The author of the admin or staff slice reads the status line, assumes `requireRole` and the temporary-password flow exist, and builds against them.
- **Rule.** CLAUDE.md "Claim only what is true"; the rules of docs/README.md; CLAUDE.md "Decisions are gated".
- **Fix.**
  - Split the status line into built and not built.
  - Say the table stores digests, not anonymous data, or salt the digest with a server secret.
  - Correct findings 17 and 18.
  - Widen finding 19 to colours, fonts and inline styles, and leave it Open until the owner accepts it.
  - Correct the Reuse sentence (Q5).

#### S13: api-contract §5 omits answers the endpoints give, and §3 does not cover the new 503
- **Axis:** Documentation (API contract) · **Status:** VERIFIED
- **Where:**
  - `docs/api/api-contract.md`: `:90` (login), `:95` (google), `:117` (check), `:47` (§3: 503 = "Database unreachable")
  - `apps/api/src/modules/auth/auth.routes.ts:21`, `:22`, `:26`: `validate` on login, google and check
  - `apps/api/src/modules/auth/auth.service.ts:131`: 503 without a client id
- **Problem.**
  - Login, google and check validate their bodies and can answer validation 422, which their entries omit.
  - `/auth/google` can answer 409 `EMAIL_TAKEN` today (S4).
  - §3 defines 503 as "Database unreachable", while `/auth/google` answers 503 when no client id is configured.
  - For check and reset, the section's intro ("These three share the password limits") implies 429, but only forgot lists it.
- **Failure scenario.**
  - F-5b builds its error states from §5.
  - An empty `#token=` fragment gets 422 from `/reset/check`, where the contract promises only 400.
- **Rule.** workflow §7: an endpoint, payload or error code goes into api-contract in the same PR. The plan's list of documents: "§5: every endpoint, with request, response, cookies and errors".
- **Fix.**
  - List 422 on login, google and check, and 429 on check and reset. Or state once per section that every endpoint may answer them.
  - Fix S4 rather than documenting a 409.
  - Widen §3's 503 row to "a dependency (the database, Google sign-in) is unavailable or not configured".

#### S14: Owning documents not updated for the structure this PR built
- **Axis:** Documentation, plan conformance · **Status:** VERIFIED
- **Where:**
  - `docs/backend/conventions.md:166` (R5): lists the ports as storage, email, clock and scheduler. The approved Google identity port is missing, as it is from §1 L12-14 and §12's ports table L306-311.
  - `conventions.md:170` (R6): `shared/auth` = route guards and `can()`. It now also signs and verifies access tokens.
  - `conventions.md:49` (§2): puts the rate limiter in the route chain, while every auth limit is applied in the service.
  - `conventions.md:162` (R2): `index.ts` exports the service factory, the routers and the public types. But:
    - `auth/index.ts` also exports the controller factory and three email adapters;
    - `sessions/index.ts` exports the cookie helper;
    - `users/index.ts` exports the controller factory and `hashPassword`.
  - `conventions.md:3`: the status line says "Of the sections from §10 on, only the logging of §10 is built", yet §12's email port, the PostgreSQL rate limits and §13's rename are built.
  - `docs/architecture/decisions/0003-session-model.md:10`: "one database row per session".
  - `docs/architecture/data-model.md:8` (the IDs convention) vs `apps/api/prisma/schema.prisma:845` (`key String @id`). The plan had `{ id, key @unique }`, and the divergence is not stated.
  - `docs/README.md:72`: "eleven Work Items"; there are now twelve.
- **Problem.** The code is the source of truth, and the owning documents now contradict it in nine places.
- **Failure scenario.**
  - The next slice adds a storage port, and a reviewer applying R5 asks to remove the Google port.
  - Or a module follows §2 and counts a failures-only limit in the route chain, where it cannot see the outcome.
- **Rule.** workflow §7: the owning document changes in the same PR, and ADRs are revised in place with a "Revised" line. CLAUDE.md "Code is the source of truth … fix the document". The engineering-principles header: a deviation is recorded, never silent.
- **Fix.** One documentation pass:
  - R5, §1 and §12: add the Google identity port (and a Revised line on ADR 0012, if the owner wants the ADR to list it);
  - R6 and §1: add the token codec;
  - §2: state where failures-only or service-keyed limits are applied;
  - R2: cover what the root wires;
  - §1: list `<module>.limits.ts` and the `email/` adapters;
  - fix both status lines and §10;
  - revise ADR 0003 in place;
  - add a key-as-primary-key exception to data-model's IDs convention, and list the divergence in the PR;
  - README: "twelve Work Items".

### NIT

#### N1: Two timing claims are untrue as written
- **Axis:** Security, documentation · **Status:** PARTLY VERIFIED
- **Where:**
  - `apps/api/src/modules/users/password.ts:12`, `:17`: `unmatchableHash ??= hashPassword(...)`
  - `docs/backend/security.md:34`
  - `apps/api/src/modules/auth/email/smtpEmailSender.ts:16-18`, `:32-34`
- **Problem.**
  - The dummy hash is built lazily. So the first unknown-email or Google-only sign-in per process pays a hash plus a compare, on every serverless cold instance.
  - "The whole attempt is bounded" is untrue. The three nodemailer timeouts are per phase, and `socketTimeout` measures inactivity. Reported: `dnsTimeout` keeps a 30 s default.
- **Failure scenario.**
  - A probe for an unknown email on a fresh instance answers about 0.25 s slower than for an existing one.
  - A slow relay holds forgot open for tens of seconds, for existing accounts only. Finding 16 understates that tail.
- **Rule.** security.md › Passwords L34; CLAUDE.md "Claim only what is true".
- **Fix.**
  - Use a precomputed cost-12 hash literal.
  - Set `dnsTimeout`, and reword the comment: each phase is bounded, and the worst case is their sum.
  - Update finding 16.

#### N2: The password policy counts characters, but bcrypt keeps 72 bytes
- **Axis:** Security · **Status:** UNVERIFIED
- **Where (reported):** `packages/shared/src/password.ts:3-4`, `:12`
- **Problem.**
  - `.max(72)` counts UTF-16 units, but bcrypt keeps 72 UTF-8 bytes.
  - So an Arabic passphrase keeps only its first ~36 letters.
  - The policy predates this PR, but this PR's endpoints are the first to hash user-chosen passwords.
- **Failure scenario.** A 45-letter Arabic phrase followed by "٢٠٢٦": any password that starts with the same 36 letters signs in.
- **Rule.** The file's own comment ("The upper bound is bcrypt's"); security.md L35.
- **Fix.**
  - Refine on `new TextEncoder().encode(p).length <= 72`, failing with `too_long`.
  - State the byte bound in security.md.

#### N3: A cross-site form post to logout or refresh clears the session cookies
- **Axis:** Security (CSRF) · **Status:** PARTLY VERIFIED. The code is mine; the browser behaviour (RFC 6265bis) is the reviewer's reading.
- **Where:**
  - `apps/api/src/modules/auth/auth.controller.ts:69-74`: logout always clears the cookies
  - `:42-52`: refresh clears them on 401 or 403
  - `apps/api/src/modules/auth/auth.routes.ts:23-24`: no body and no origin check
- **Problem and failure scenario.**
  - A page the receptionist opens auto-submits a form to `/api/v1/auth/logout`.
  - No SameSite=Strict cookie is sent, so nothing is revoked. But the answer deletes both cookies, and the desk is signed out within 15 minutes.
  - This can be repeated at will.
- **Rule.** ADR 0003; security.md L16 (SameSite=Strict instead of a CSRF token).
- **Fix.** On the two cookie routes, answer 403 before touching cookies when either:
  - `Sec-Fetch-Site` is present and is neither `same-origin` nor `none`; or
  - `Origin` differs from `CORS_ORIGIN`.

#### N4: Dead outputs and unused exports
- **Axis:** Code organization · **Status:** UNVERIFIED
- **Where (reported):**
  - `apps/api/src/modules/sessions/index.ts:4-6`: the three sessions constants
  - `apps/api/src/shared/auth/index.ts:13`: `ACCESS_TOKEN_TTL_SECONDS`
  - `apps/api/src/shared/http/index.ts:3`: `REDACTED_PATHS`
  - `sessions.service.ts:19`: `Rotation`'s unread `userId`
  - `:15`: `IssuedToken.expiresAt`
  - `sessions.repository.ts:55`: `markRotated`'s boolean, ignored at `sessions.service.ts:77`
  - `limiter.ts:45-47`: the unused synchronous branch
- **Problem and failure scenario.**
  - Another module can start depending on an exported constant, which turns a change to the grace window into a cross-module change.
  - A later change may trust a value nothing has ever read.
- **Rule.** conventions R2; engineering-principles §1-§2.
- **Fix.**
  - Keep these file-local, or drop them.
  - `markRotated`'s boolean becomes useful once B2 asserts it.

#### N5: Second owners for facts that already have one
- **Axis:** Engineering principles · **Status:** VERIFIED
- **Where:**
  - The email is normalised by hand in `apps/api/src/modules/auth/google.ts:47`, instead of by `emailSchema` (`packages/shared/src/auth.ts:13`).
  - The recipient is digested in `cappedEmailSender.ts:36`, and again by `keyOf` (`limiter.ts:24-25`).
  - The access-token claims are derived twice: `auth.service.ts:74-78` and `users.service.ts:173-177`.
  - `FIFTEEN_MINUTES` is declared twice: `app.ts:34` and `auth.limits.ts:4`.
- **Failure scenario.**
  - `emailSchema`'s normalisation changes, but Google-created accounts keep the old form.
  - Their owners can then no longer sign in by password, or get a reset email.
- **Rule.** ADR 0012 › Consequences ("Each rule has one owner"); engineering-principles §4.
- **Fix.**
  - Use `emailSchema.safeParse` in `google.ts`.
  - Let `keyOf` be the one digest.
  - Add one `toAccessClaims(account)` in `users`.
  - Keep one window constant.

#### N6: Names and comments that say something else
- **Axis:** Code quality · **Status:** VERIFIED
- **Where:**
  - In `auth.service.ts`, "address" is the IP in sign-in (`:93`, `:111`) but the email in forgot (`:165`), where the IP is called `from`.
  - `:143`: `refreshToken && (await …)` yields `'' | number | undefined`.
  - `apps/api/src/db/payments.api.test.ts:227` and `front-desk.api.test.ts:229`: `describe('the request id')` wraps idempotency-key tests.
  - `migration.sql:1`: "-- F-5a: …", a roadmap note.
  - `sessions.service.ts:31`: the header lists only refresh-token operations.
- **Failure scenario.** Someone adds `limiter.count(PASSWORD_ADDRESS, address)` in forgot, and silently keys a per-IP ceiling by email.
- **Rule.** engineering-principles §1, §7, §8 ("no roadmap notes in code or test names"); conventions §13 ("Two ids, never confused").
- **Fix.**
  - Use `clientAddress` and `email` throughout.
  - Write two plain guards in refresh.
  - Rename the describe blocks to "the idempotency key".
  - Complete the sessions header.
  - Optionally, describe the change in the migration's header before merge. Its checksum changes, so the owner's development database would need a reset.

#### N7: Commit history breaks workflow §3, and the PR says otherwise
- **Axis:** Workflow · **Status:** VERIFIED
- **Where:**
  - Commit `e56664f` "docs(findings): record the f-5a findings" holds findings 16–19, which describe `d173c58`, `7eb2179` and `dbd0ae7`.
  - The subject of `8f1597f` is 52 characters long.
  - The PR ticks "Documents updated in the same commits: … findings 16–19".
- **Problem and failure scenario.**
  - Reverting `d173c58` (the reset email) leaves findings 16 and 19 describing code that is gone.
  - The PR's claim is false.
- **Rule.** workflow §3 L42 (at most 50 characters) and L67 (code, tests and documents in the same commit); the plan L199.
- **Fix.** Either:
  - fold each finding into its commit (fixup and autosquash, with an owner-approved force-push), and shorten `8f1597f`'s subject; or
  - correct the PR's claim and state both deviations.

#### N8: `sessions` (L0) hard-codes the auth router's URL as the cookie Path
- **Axis:** Abstraction · **Status:** PARTLY VERIFIED
- **Where:**
  - `apps/api/src/modules/sessions/sessionCookies.ts:19`: `path: '/api/v1/auth'`
  - vs `app.ts:89` and `:153`, the mounts
- **Problem and failure scenario.**
  - The contract moves the auth router.
  - Reported: the tests still pass, because they set the Cookie header by hand.
  - Browsers stop sending the cookie to refresh, and every session ends after 15 minutes.
- **Rule.** conventions §7 › Routers: the composition root mounts each router where the contract puts it.
- **Fix.** Either:
  - pass the path from `app.ts`; or
  - add one test with a supertest agent (cookie jar) that signs in and refreshes.

#### N9: Controllers cast `req.body`, so nothing ties a route's schema to its controller's type
- **Axis:** Types · **Status:** VERIFIED
- **Where:**
  - `apps/api/src/modules/auth/auth.controller.ts:26` and the other handlers
  - `apps/api/src/modules/users/users.controller.ts:20`
  - `apps/api/src/shared/validation/validate.ts:16`: `validate(schema: z.ZodType, …): RequestHandler`
- **Problem and failure scenario.**
  - `validate(resetCheckSchema)`, pasted onto the reset route, compiles.
  - Then `password` is stripped, and `hashPassword(undefined)` rejects with a 500, after the limit has already counted the request.
  - These are the first controllers, so they set the pattern.
- **Rule.** engineering-principles §5.
- **Fix.** Either:
  - add a typed helper of about 15 lines, `validated(schema, handler)`, in `shared/validation`; or
  - write the pairing rule into conventions §3.

#### N10: A pending reset link survives a password change
- **Axis:** Security · **Status:** VERIFIED (code)
- **Where:**
  - `apps/api/src/modules/users/users.service.ts:168-172`: the change's transaction touches no reset token
  - `apps/api/src/modules/auth/auth.service.ts:196-201`: a reset consumes one token and leaves the others
- **Problem and failure scenario.**
  - A user asks for a link, then remembers the password and changes it in settings.
  - The link can still reset the password for up to an hour.
- **Rule.** security.md › Passwords L46 (one live link). A reviewer cites the OWASP cheat sheet; I did not re-check it.
- **Fix.** Delete the user's unused reset tokens inside the `/me/password` and reset transactions.

---

## 3. Questions for the owner

#### Q1: Automatic Google linking adopts an account whose email was never proven. Recommend deciding before merge.
- **Axis:** Security · **Status:** VERIFIED (code). Google's guidance on `hd` and on authoritative domains is reported.
- **Where:**
  - `apps/api/src/modules/auth/auth.service.ts:111-115`: register opens a session, and nothing proves the inbox
  - `apps/api/src/modules/users/users.service.ts:100-111`: the link by email
  - `apps/api/src/modules/users/users.repository.ts:64-66`: sets `googleSubject` only; the password hash and every refresh family stay
  - `apps/api/src/modules/auth/google.ts:44`: `email_verified` is accepted for any domain
- **Problem.** The approved automatic link has a consequence the owner most likely did not foresee: the pre-account takeover known as the classic-federated merge (Sudhodanan & Paverd, USENIX Security 2022, cited by the reviewers).
- **Failure scenario.**
  - The attacker registers victim@gmail.com with password P, and keeps that session.
  - Later, the victim taps "Sign in with Google". No account has their `sub`, but the email matches, so `linkGoogle` runs.
  - The victim now uses the account (the `linked: true` toast), while P and the attacker's refresh family keep working.
  - The victim cannot remove P, because `/me/password` asks for the current one.
  - When an owner later adds the victim's email as reception, ADR 0009 links this existing account. The attacker then has the desk: customers' names and phones, and payments.
- **Rule.**
  - security.md › Sign-in methods L25 (approved).
  - security.md › Tokens and cookies L18: a link is not a revocation event, while a reset, the other proof of the inbox, ends every session.
  - ADR 0009 decision 4.
- **Options.**
  - **(A) Accept.** Write the consequence into security.md, and make the staff slice prove the email itself.
  - **(B) A safe automatic link.**
    - Link only when Google is authoritative for the address: gmail.com, or an `hd` claim.
    - In one transaction, set `googleSubject` where it is still null, end every session, and clear the existing password. The person adds a password later through the reset email.
    - Cost: someone who registered with their own password has to set it again.
  - **(C) No automatic link onto an account that has a password.**
    - The person signs in with the password, or resets it, and links Google from the account's settings.
    - Simplest logic, but it drops `linked` and needs a link endpoint (F-6).
- **Recommendation:** B, in this PR. ADR 0009's reception link will rest on "an account with this email is this person".

#### Q2: `/me/password` turns a 15-minute access token into a lasting credential
- **Axis:** Security · **Status:** VERIFIED (code)
- **Where:**
  - `apps/api/src/modules/users/users.service.ts:155-165`, `:168-172`
  - `apps/api/src/modules/users/users.routes.ts:14`
  - `apps/api/src/app.ts:39-43`: the general 300 per 15 min per user is its only limit
- **Problem.**
  - **(1)** A Google-only account sets its first password with nothing but a valid access token. The change ends every other session and hands the caller a fresh refresh cookie.
  - **(2)** No failure limit counts `CURRENT_PASSWORD_INCORRECT`.
  - **(3)** Skipping the current password follows the database flag, not the token's `mustChangePassword` claim.
- **Failure scenario.**
  - **A Google-only user.** A stored XSS on the single origin runs in their tab.
    - It sends `POST /api/v1/auth/refresh` (same-origin, so the cookie is sent) and gets an access token.
    - It then sends `POST /api/v1/me/password {password: "attacker1"}` and gets 200.
    - The attacker now has a password forever, and the victim's sessions have ended. The victim signs back in with Google and sees nothing.
  - **An owner.** The same script tries 300 current passwords per 15 min, about 28,800 a day against 960 at login. On a hit, it takes the account.
- **Rule.** security.md › Passwords L44 (approved); › Rate limits; ADR 0003 (the short-lived, in-memory token is what bounds theft).
- **Options.**
  - **(A) Accept,** and write it into security.md.
  - **(B) Close all three paths:**
    - count `CURRENT_PASSWORD_INCORRECT` under a per-user failures limit, with B1's reserve and refund;
    - skip the current password only when both the claim and the flag say a change is pending;
    - send a Google-only account's first password through the reset email.
  - **(C) As B,** but require a fresh Google ID token for the first password. That makes it an auth endpoint, because the Google port lives in auth (L3).
- **Recommendation:** B.

#### Q3: Amendment 1's keys leave successful registrations unbounded, and let 50 junk Google tokens lock a whole coworking address out of sign-in
- **Axis:** Security, operations · **Status:** VERIFIED (code). The platform quotas are reported, from Vercel's and Neon's public pages.
- **Where:**
  - `apps/api/src/modules/auth/auth.service.ts:111-121`: register and login count only failures
  - `:132`: a Google failure counts on the address only
  - `:97`: every sign-in flow checks `SIGN_IN_ADDRESS` first
  - `:195`: reset hashes before it checks the token
  - `apps/api/src/app.ts:145-152`: a request with a valid bearer counts by user
- **Problem.**
  - **(a) Registrations.** Successful registrations are bounded only by the guest limit, 1,200 per 15 min per address. Each costs a cost-12 hash, a users row that is never deleted, and a refresh row. Each created account's token also moves its holder into a fresh 300-request bucket.
  - **(b) Junk Google tokens.** A junk token fails in microseconds, and counts only on the per-address key that every flow checks first.
- **Failure scenario.**
  - **(a)** One script registers about 1,200 accounts per 15 min per IP, which is about 300 s of bcrypt CPU per window.
    - Reported: Vercel Hobby's monthly Active CPU (4 h) is then gone in about 12 h. Under ADR 0014's usage terms, the feature then pauses for the rest of a 30-day period.
    - Meanwhile, the rows push toward Neon's 0.5 GB.
  - **(b)** Anyone on a space's Wi-Fi sends 50 `POST /auth/google {idToken: "x"}`.
    - Every password sign-in, Google sign-in and registration from that address answers 429 for 15 minutes, repeatably.
    - This is exactly the lockout that security.md L72 says keying by address would cause.
- **Rule.** security.md › Rate limits L72-77 (the approved keys); ADR 0014 › Deviations (Database; Usage terms).
- **Options.**
  - **(1) Accept,** and record both risks in security.md and ADR 0014.
  - **(2) Bound both, in this PR:**
    - count every registration per address before hashing, for example 20 an hour, which is enough for a space's newcomers;
    - give failed Google tokens their own per-address policy, which refuses only `/auth/google`;
    - check the reset token (read-only) before hashing.
  - **(3) Also** keep a per-address ceiling for signed-in requests, sized in F-7.
- **Recommendation:** (2) in this PR, and (3) at F-7.

#### Q4: Anyone can make Masaha's Gmail send attacker-worded mail to any address, and trip the shared ceiling
- **Axis:** Security (email abuse) · **Status:** VERIFIED (code)
- **Where:**
  - `apps/api/src/modules/auth/email/resetEmail.ts:55`, `:75`: the greeting uses the account's name
  - `apps/api/src/modules/auth/email/cappedEmailSender.ts:16-19`, `:43`: one 100-a-day ceiling, keyed `'all'`
  - S8: the name accepts line breaks
- **Problem.**
  - Registration proves no inbox, and the name is free text. The reset email greets by that name.
  - Every user shares one ceiling.
- **Failure scenario.**
  - The attacker registers 34 third-party addresses with a name like "فريق مساحة: حسابك موقوف، فعّله عبر evil.example".
  - They then send 3 forgots for each, about 45 min from one IP under 50 per 15 min.
  - That is 102 emails from Masaha's Gmail, all passing DMARC, carrying the phishing line.
  - The ceiling trips. For the rest of the 24-hour window, no user receives a reset email. While B3 is unfixed, each user's forgot also deletes their delivered link.
  - Spam reports can get the Gmail sender throttled.
- **Rule.** security.md › Passwords L54-56 (the caps protect "the sender's reputation"); ADR 0014 › Email (a single sender).
- **Options.**
  - **(a)** Greet without the name, or only with a name Google vouched for. This is a design deviation to record.
  - **(b)** Also count delivered reset emails per requesting address per day, for example 10.
  - **(c)** Add an hourly ceiling beside the daily one, so a trip lasts an hour, not a day.
  - **(d)** Accept and record.
- **Recommendation:** (a) + (b), with S8.

#### Q5: Within the 30 s grace, each presentation of a rotated token mints an independent branch that reuse detection never sees
- **Axis:** Security · **Status:** VERIFIED (code)
- **Where:**
  - `apps/api/src/modules/sessions/sessions.service.ts:69-78`
  - `docs/backend/security.md:14-15`
- **Problem.**
  - Within the grace, rotate issues a brand-new token on each presentation, as security.md L14 says.
  - But a copy presented within 30 s of a rotation becomes its own chain.
  - Each holder rotates their own chain and never presents a token rotated more than 30 s ago, so the reuse rule never fires.
- **Failure scenario.**
  - An infostealer replays the refresh cookie at once.
  - If the victim's next refresh falls within 30 s of the replay, which is likely while they are active, thief and victim each hold a live branch.
  - The thief refreshes every 15 minutes, undetected, until a logout, a password change or a reset.
- **Rule.** security.md L15 ("Ending only the family still cuts a stolen chain"); CLAUDE.md "Claim only what is true".
- **Options.**
  - **(A) Accept,** and correct L15.
  - **(B) Return the same successor** for every presentation within the grace. Derive it deterministically, for example `base64url(HMAC-SHA256(serverKey, presentedToken))`, store its hash at the first rotation, and return it while its row exists.
  - **(C) Cap** the grace re-issues per token.
- **Recommendation:** A now; B if the owner wants reuse detection to hold inside the grace.

#### Q6: The first slice whose rules read the time wires no clock
- **Axis:** Architecture · **Status:** PARTLY VERIFIED. The code and documents are mine; the test-flake scenario is reported.
- **Where:**
  - `apps/api/src/modules/sessions/sessions.service.ts:36` and `apps/api/src/shared/rate-limit/limiter.ts:23`: `now = () => new Date()` defaults
  - `apps/api/src/shared/rate-limit/counter.ts:29-33`: PostgreSQL's `now()`
  - `apps/api/src/shared/rate-limit/policy.ts:26`: Retry-After = the database's `reset_at` − Node's now
  - `apps/api/src/app.ts:122`, `:129`: no clock passed
  - `docs/backend/conventions.md:291`, `:296`
  - the plan, L82 ("clock-free")
- **Problem.**
  - §11 says the clock is a port injected at assembly, and that it applies "from the first slice that reads the time".
  - F-5a reads the time (the grace, the expiries, the windows, Retry-After) from four sources, and the documents were not amended.
  - Retry-After mixes the database's clock with the API's, and online they are different hosts.
  - Reported: the rate-limit API tests also mix both clocks, with 1 s margins, so they can flake locally when Docker's VM clock drifts.
- **Options.**
  - **(a)** Wire one clock in `createApi`, where the seams already exist, and pass its time into the counter's SQL.
  - **(b)** Stay clock-free: amend §11 and §12, and record a finding for the skew.
- **Recommendation:** (a).

#### Q7: The request's log line is written after the response
- **Axis:** Operations · **Status:** UNVERIFIED
- **Where (reported):**
  - `apps/api/src/shared/http/requestLogging.ts:28-31`: pino's default, asynchronous destination
  - `:38-57`: pino-http, which logs on the response's `finish` event
- **Problem.**
  - For every 2xx and 4xx request, the only log line (request id, status, duration, user) is written after the response, through an asynchronous stream.
  - ADR 0014 and conventions §12 forbid work after the response, because a function may be frozen.
- **Failure scenario.**
  - Online, a user reports the request id of a 429.
  - The function froze before the line reached stdout, so no log line carries that id.
  - Matching a report to the log is the very purpose conventions §10 gives the id.
- **Rule.** conventions §12 L312; ADR 0014 › Consequences; conventions §10 L285.
- **Options.**
  - **(a)** Use a synchronous stdout destination, and state in §10 and §12 that the line is best effort online.
  - **(b)** Write the access line before the response: wrap `res.end`, with pino-http's `autoLogging` off.
  - **(c)** Accept and record.
- **Recommendation:** (a).

**The PR's own "Decisions and divergences to review" (#1–#7):** this review raises nothing on #1–#3 and #5–#7; #4 is S12.

---

## 4. What is solid

A future change must not break these:

1. **Reset tokens.**
   - 256 bits, SHA-256 at rest, one hour.
   - Consumed by one conditional `UPDATE … WHERE used_at IS NULL AND expires_at > now RETURNING`, inside the transaction that sets the password and ends every session.
   - Never split it into a read and then an update. A concurrent-reset test guards it: `password.api.test.ts:178`.
2. **`counter.hit`.** One `INSERT … ON CONFLICT DO UPDATE`, with the window rollover in its `CASE`. Every count-based limit (general, refresh, password, email caps) is atomic and written before the answer, and the keys are the policy's name plus a SHA-256 digest.
3. **The reuse rule.** `rotate` returns `{ outcome: 'reused' }` instead of throwing inside `runInTransaction`, so the family's deletion commits before the 401. Throwing there would roll the revocation back.
4. **bcrypt.** It runs outside every transaction (reset, `/me/password`). Keep it that way in the B2 fix.
5. **Access tokens.** HS256 is pinned on sign and on verify, and the claims are shape-checked. Every token is minted from the database row, so a refresh or a Google sign-in cannot drop the forced-change claim.
6. **Credential checks.**
   - An unknown email or a Google-only account still spends a bcrypt compare, and answers `INVALID_CREDENTIALS`.
   - `ACCOUNT_SUSPENDED` shows only after a matching password.
   - The Google verifier pins RS256, the issuer, the audience, the expiry and `email_verified`. It looks the `sub` up before the email, and never relinks another subject.
7. **Cookies and bodies.**
   - The refresh cookie is HttpOnly, SameSite=Strict, `Path=/api/v1/auth`, set and cleared from one options object.
   - Only `application/json` bodies are parsed, and CORS allows one origin.
8. **The reset link.** Its origin comes from configuration, never the Host header. The token rides in the fragment, and the name and link are HTML-escaped.
9. **The request id and redaction.**
   - The request id is a server UUID, generated first in the chain; client ids are ignored. It is in the header and in every error envelope.
   - The `cookie`, `authorization` and `set-cookie` headers are redacted, and bodies are never serialized.
10. **Module boundaries.**
    - Services import neither Express nor Prisma.
    - Every cross-module import in production code goes downward, through `index.ts`.
    - The lint map mirrors conventions §7.

---

## 5. Comparison with the first review

*Written after sections 1–4 were final. I read `F5A_REVIEW_FIXES.md` only then, and the sections above are unchanged.*

### 5.1 Each finding of this review against the first review

| This review | Against the first review | Note |
|---|---|---|
| B1 | **SAME** as B2 | Same fix: count first, give back on success, before answering. Two additions: refund only within the same window (`reset_at = $2`), and return the address slot when the account key refuses. |
| B2 | **DISAGREES** with B1 (scope) | B1 sees only rotation, logout and revocation. Its lock never covers *issue*, so the most exploitable case survives its fix: a login that verified the old password before a reset still inserts its family after it. The lock must also cover login, register and Google, with the hash re-checked under it, and `/me/password` needs a compare-and-set. Prefer `FOR NO KEY UPDATE`: B1's `FOR UPDATE` also blocks, for the lock's duration, the foreign-key checks of concurrent inserts that reference the user (payments, audit entries). |
| B3 | **SAME** problem as B3; **DISAGREES** with its fix | Deciding the caps before issuing still kills the delivered link when SMTP fails after the caps pass. And with B4's transaction, two concurrent forgots still leave two live links: under READ COMMITTED, both `DELETE`s see nothing to delete. Replace only after a delivered send (retire the older ids), and delete the new token when it is not sent. |
| S1 | **SAME** as B8, extended | Secure cookies and the Google requirement also hang on `NODE_ENV`. Making `NODE_ENV` required fixes all three at once. |
| S2 | **SAME** as B11 | Also: a discriminated email setting, so the `?? ''` fallbacks go. |
| S3 | **NEW** | |
| S4 | **SAME** as B7; partly **DISAGREES** | B7 alone still answers `EMAIL_TAKEN` to a double first Google sign-in whenever the email key is the one that fires. `signInWithGoogle` must re-read by subject on a conflict, and the link must be conditional. |
| S5 | **SAME** as B4 (its second half) | |
| S6 | **NEW** | D5's "no absolute session lifetime" is related, but a different issue. |
| S7 | Partly **SAME** as B5 (log codes, never the message) | **NEW:** the Google key-fetch failure answered as 401 and counted on the NAT address, and the cap catches that hide database errors. |
| S8 | **NEW** | D4 removes the name from the email, but the schema still accepts line breaks in every other use. C3 tests NFC and bidi only. |
| S9 | Relates to D3; partly **DISAGREES** with D3's premise | D3, an owner decision, is acceptable as the recorded deviation my fix allows. But these depend on inputs only (testing.md §1), and stay unpinned unless the API tests are extended to the boundary values: the grace boundary, the TTLs, the dummy-compare order, the Google branches and how `limitFailures` counts. D3 also points to a "C10" that the list does not contain. |
| S10 | (b) **SAME** as B3's test; (e) **SAME** as C2; the rest **NEW** | |
| S11 | **SAME** as B10, extended | B10's rule as worded would fail existing tests, which import `test/app.ts` and `app.ts` (`users.api.test.ts:12`, `:14`; `validate.api.test.ts:7`), unless `*.test.ts` are exempted. Also: a CI test through ESLint's API, rather than evidence runs only; and files placed directly under `modules/` classified as unplaced. |
| S12 | Partly **SAME** as D5 (finding 19 stays Open) | **NEW:** the status line's claims of what is built, "names no one", and findings 17 and 18. |
| S13 | Partly **SAME** as C5 (§3's 503) | **NEW:** the missing 422 and 429. |
| S14 | Partly **SAME** as D2 (R2) and C4 (ADR 0003) | **NEW:** R5, R6, §2, the status lines, the IDs convention and the README's count. |
| N1 | **SAME** as B5 for the SMTP part | **NEW:** the lazy dummy hash. On B5's fix, see 5.2. |
| N2 | **NEW** | |
| N3 | **NEW** | |
| N4 | **SAME** as D2 (unused exports) | |
| N5 | **NEW** | |
| N6 | Partly **SAME** as C6 | |
| N7 | Partly **SAME** as C7 | C7 leaves out the separate findings commit and the PR's false "same commits" claim. |
| N8 | **NEW** | |
| N9 | **NEW** | |
| N10 | **SAME** as B6 (its first bullet) | |
| Q1 | **SAME** as D1 (already decided); partly **DISAGREES** | See 5.2. |
| Q2 | Partly **SAME** as B6 (its second bullet) | **NEW:** a first password with no proof, and the skip decided by the flag instead of the claim. On B6, see 5.2. |
| Q3 | Partly **SAME** as D5 (the ceiling exhaustion, recorded) | **NEW:** unbounded registrations (CPU, storage, the free-tier pause), the lockout of a whole NAT address by 50 junk Google tokens, and reset hashing before it checks the token. |
| Q4 | **SAME** as D4 and D5 | Extra: my option (b), a daily count per requesting address. |
| Q5 | **NEW** | |
| Q6 | **NEW** | |
| Q7 | **NEW** | |

### 5.2 First-review items I believe are wrong, incomplete or unnecessary

1. **D1 is risky as specified.**
   - It keeps trusting `email_verified` for every domain. Google is authoritative only for gmail.com, or when the token carries an `hd` claim.
   - Take a non-Gmail address whose Google account belongs to a former holder, for example a space's shared mailbox created as a Google account by an ex-employee. D1 now clears the real owner's password and revokes their sessions on that person's first Google sign-in: a takeover, with a lockout.
   - D1 also sends people to `/me/password`'s first-password path, which needs no proof (Q2).
   - **Fix:** link automatically only when Google is authoritative. Otherwise refuse, and ask for a password sign-in or a reset. Set a first password through the reset email.
2. **B1 is incomplete** (see B2 in the table). The issue paths are not locked, the hash is not re-checked under the lock, and `FOR NO KEY UPDATE` is preferable to `FOR UPDATE`.
3. **B3 and B4 together are incomplete.** They still lose the delivered link on an SMTP failure, and they do not stop two live links under concurrency. B4's transaction fixes only a partial failure between the delete and the insert.
4. **B5's fix, as worded, breaks ADR 0014.** "An overall deadline … that resolves `{ sent: false }`":
   - if the SMTP exchange keeps running after the deadline, the 202 goes out with work still in flight;
   - the email can then arrive with a link that the B3 fix has just invalidated.

   The deadline must abort the connection (close the transport or socket) before it resolves.
5. **B6's second bullet has the wrong key and the old race.** It says "the per-account failure limit, as sign-in does", but that limit is keyed by address + email. For `/me/password`, key it by the user id, because a token thief can change address. And use B2's race-free reservation, or the same burst bypass applies: the bcrypt compare is the slow step here too.
6. **B7 alone does not fix the Google race** (S4).
7. **B9 is unnecessary.** It is harmless defence in depth at best:
   - `accessToken.ts:40-42` already refuses a token without a numeric `sub` (`Number(undefined)` is `NaN`);
   - only this server can mint a token, with `JWT_SECRET`, and it always sets `exp`;
   - an issuer adds nothing while one secret signs one kind of token.
8. **B10, as worded, fails existing tests.** It needs an exemption for `*.test.ts` (see S11).
9. **D3's premise is only partly accurate** (see S9), and it refers to a "C10" that does not exist.
10. **C5's fourth bullet is unnecessary.** At `e56664f`, security.md has no line about refresh failures clearing the cookies; only L16 mentions clearing, from one options object. api-contract L100 already owns that fact, and adding it to security.md would give it a second owner.

### 5.3 First-review items this review missed, which I agree with

- **C5's first bullet.** `docs/frontend/architecture.md:49` still says "F-5 builds the guards"; it should be F-5b.
- **C5's second bullet.** conventions §1 L32 still places text normalisation in the API's `shared/validation`, but it lives in `packages/shared`.
- **C5's last bullet.** The per-token reset bucket does not limit guessing; only the per-address one does.
- **D5.** Record that a session has no absolute lifetime, because each rotation grants 7 more days. Record that the reset email's copy lives outside the web catalogue.
- **C1.** A test for grace siblings: both belong to the original family, and both die on logout and on reuse.
- **C3.** Unit tests for `emailSchema` and `passwordSchema`, and a test script for `packages/shared`.
- **D6 and C8** agree with this review.

---

## 6. What I could not check, and why

- **Nothing was executed (read-only).**
  - I ran no tests, lint, typecheck, build, database or Prisma command.
  - So the PR's evidence is unverified: the test counts, the lint-violation runs, the empty `migrate diff` and the manual log-mode run.
  - The races in B1–B3 are established by reading the code and PostgreSQL's documented READ COMMITTED behaviour, not reproduced. API tests that send `Promise.all` bursts, or hold a lock in a test transaction, would confirm them deterministically.
- **The adversarial verification pass was stopped** at the owner's request, before it finished, and none of its partial results is used.
  - Items marked UNVERIFIED, and the *reported* parts of the PARTLY VERIFIED ones, come from reviewer subagents (each with a `file:line` quote). I did not re-check them.
- **Library internals.** Reviewer subagents read these in `node_modules`, after checking the versions against `package-lock.json` at `e56664f`; I did not re-read them:
  - jose's key-set errors;
  - nodemailer's timeouts and error messages;
  - when pino-http writes its line;
  - eslint-plugin-boundaries' classification;
  - bcrypt's 72-byte cut;
  - Express 5's `clearCookie`.
- **Two procedural slips, with no effect on the findings:**
  - one subagent ran `node -e` once to parse the lockfile (read-only);
  - another read one line of `CLAUDE.md` from the working tree by mistake, then confirmed the same text in the snapshot.

  No finding relies on either.
- **Platform facts** come from public pages that reviewers read on 2026-10-02:
  - Vercel Hobby's CPU allowance and its 30-day pause;
  - `NODE_ENV` at runtime;
  - no IPv6 ingress;
  - Neon's storage limit.

  They are not checked against the F-7 deployment, which does not exist yet. `TRUST_PROXY`'s right value online is unknown until then.
- **Estimates, not measurements:** about 350 B per refresh row, about 0.25 s per cost-12 bcrypt, about 15 compares a second.
- **Not exercised:** Google's live behaviour (the `hd` claim, the keys endpoint), and real Gmail SMTP delivery and rejections.
- **Not checked:**
  - the PR's CI status (I used only `gh pr view`);
  - the wording of the Arabic copy;
  - the OWASP Forgot Password Cheat Sheet's exact wording, quoted in B3 and N10.
