# SESSIONS — a session ends when it should: findings 51, 20, 16 and 39 (API)

**Worker B** · worktree `C:\Users\basel\masaha-b`, detached at `origin/main` (`3c3dc47`; migrated,
client generated, shared `dist` built) · branch `feat/session-ends`, cut with
`git switch --no-track -c feat/session-ends origin/main` after `git fetch --prune origin`.
Databases `masaha_b_dev` / `masaha_b_test`; API on 3321, web on 5321.

**Model:** Opus 5.5, effort high. **Size cap:** at most 3 subagents, no self-review subagent, no workflow.
**Plan:** `C:\Users\basel\.prompt\MASAHA_WORKER_B\PLAN\SESSIONS_PLAN.md` (`write-plan`; save, then stop).
**Report:** `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\SESSIONS_REPORT.md` (`final-report`).
Follow the skills from start to end: `start-work-item`, `write-plan`, `add-error-code` (for any new
code), `open-pr`, `final-report`.

## 1. The task in brief

Four open findings of the identity layer, in one item (the owner, 2026-10-13):
- **51 — an access token outlives the end of its session:** after a password change, a reset, a
  suspension, a role change or a temporary password, a token already handed out keeps working until
  it expires (15 minutes), and a token signed before a suspension works again once the account is
  restored. Close it.
- **20 — a session has no absolute lifetime:** a session refreshed weekly never ends. Give it one.
- **16 — the forgotten password's timing tells whether an account exists.** Narrow it.
- **39 — the users service takes a parameter only its unit test passes.** Remove it.

This item is **the one schema change in flight**.

## 2. Read first

In the order workflow §2 *Reading before work* gives.
- **The capability documents first:** `docs/features/users.md`, `docs/features/auth.md`.
- The four findings (51, 20, 16, 39) whole; finding 31 for 39's background.
- `docs/backend/security.md` (*Tokens and cookies*, *Passwords*, *Rate limits*, *Authorization*);
  ADR 0003 (the session model, revised by #62), 0013 (identity modules), 0014 (no work after the
  response), 0015 (locks, read committed), 0017 (the recovery session);
  `docs/backend/conventions.md` §2, §8, §11 (the clock), §12, §13 (the session lock);
  `docs/architecture/data-model.md` › *Users and sessions*; `docs/api/api-contract.md` §1–§3 and
  *Session*, *Me*, *Users (the admin)*; `docs/development/testing.md` §1–§4 (rule 3: a port is the one
  seam; rule 7: make the break for a security property).
- The code: `shared/auth/` (`accessToken.ts`, `requireAuth.ts`), `modules/sessions/`,
  `modules/users/`, `modules/auth/` (refresh, the forgotten password, its email port).

## 3. The settled decisions (review them in "Stronger decisions")

- **D1 — finding 51: a session version on the account, carried by the access token.** A number on
  `User` that grows by one each time the account's sessions are all ended; every access token carries
  the version it was signed under; `requireAuth`, which already reads the account on every request,
  refuses a token whose version is not the account's (401, as an expired token). *Why over the
  finding's timestamp:* exact (no same-second window between a token's `iat` and the end), and no clock
  shared between function instances. Name the column and the claim; a token without the claim
  (signed before this deploy) is refused once, and the web refreshes. **ADR 0003** gains a dated
  *Revised* line.
- **D2 — what ends every session (and bumps the version):** a password change (the session that made
  it gets a token under the new version and stays signed in, as today), a reset by email, a
  suspension, a role change, the admin's temporary password. **A sign-out ends only its own session**
  and bumps nothing; the web drops its token. Each bump happens in the same transaction, under the
  same session lock, as the refresh tokens' deletion it accompanies.
- **D3 — finding 20: a session lives at most 30 days from its sign-in.** The family carries its
  absolute deadline (a column on the session's rows, set at sign-in and copied on each rotation);
  a refresh past it is refused as any ended session is, and the family's tokens are removed. The web
  changes nothing: a refused refresh already ends the session. Say what happens to the families that
  exist at the migration (recommended: their deadline counted from their first token's creation, or
  from the migration, whichever is later — weigh it).
- **D4 — finding 16: the owner's decision.** An answer for an email that sends nothing (no account, a
  suspended one, or any other case that sends no link) **waits about as long as a real send takes on a
  good connection**, so a probe on a fast network cannot tell them apart. Measure a real send through
  the SMTP relay locally (several runs, with `EMAIL_MODE=smtp` in this folder's `apps/api/.env`; if
  its SMTP keys are absent, ask the owner to add them — never read another folder's `.env`, **read
  keys only, never print a value**; if you cannot send, say so and use a documented estimate), choose the wait with **jitter** (a fixed delay is itself a tell), and put the
  wait in the module's own rule, the clock and the timer being the platform's (a test must not wait
  real seconds: a port the test can drive, never a parameter only tests pass — testing §3 rule 2). A
  slow relay's outliers stay distinguishable: security.md records that residual as accepted, and the
  finding is resolved with that line.
- **D5 — finding 39:** `createUsersService` loses its `passwords` parameter; the service hashes and
  verifies through its own module's helpers; the logic worth a unit test lives in pure helpers; the
  rest is proven in the API lane. **Only that parameter:** the repository parameter the older services
  share stays for the planned refactor (finding 31's follow-up).
- **D6 — one migration** (both columns), created once with `migrate dev --create-only`, then `ls`;
  on data loss it refuses: `migrate diff --script`. **You also write one comment line for the media
  worker:** in `schema.prisma`, `Space.profileUpdatedAt`'s doc comment drops "and photos" (photos
  leave the freshness groups, the media item's D8), in your migration's commit — the media worker
  leaves the schema file alone so that one item edits it.

## 4. Findings

Read the open findings' titles; open those that touch sessions, tokens or the identity layer (17
expired counters and sessions never swept; 21 a replayed token's branch; 23). Resolve 51, 20, 16 and
39 with their status and a resolution line, and the index. Your new findings number **65–66**.

## 5. Risks

- **Every path that ends sessions** must bump the version, under the lock it already takes, or a
  token survives one of them: list them all in the plan from the code, not from this prompt.
- **Races:** a refresh racing a password change or a suspension (the session lock); a role change
  racing a link change. Prove each security property by making its break once (testing §3 rule 7).
- **The deploy:** every signed-in user's token is refused once after the deploy (no claim) and the web
  refreshes silently; say what proves it.
- **Secrets:** read the `.env` keys only; never print a value, an SMTP password or a token.
- **The machine (the owner's rule): one full test run at a time.** Before `test:api` or
  `test:component`, check that worker A (main folder) and the media worker (`masaha-media`) run none.

## 6. Boundaries with the other open items

- **The media worker** (`C:\Users\basel\masaha-media`, branch `feat/space-photos`, building now) edits
  `apps/api/src/app.ts`, `apps/api/src/config/env.ts`, `apps/api/src/shared/auth/can.ts` (+ its unit
  test), `apps/api/src/shared/http/` (a new `receiveFile.ts` and `index.ts`), the new
  `shared/storage/` and `shared/images/`, `modules/spaces/` (`photos/`, `spaces.admin.routes.ts`,
  `spaces.limits.ts`, `index.ts`, `public/`), `modules/directory/`, `packages/shared/src/spaces/` and
  `src/directory/`, `apps/api/test/app.ts` and a new `test/storage.ts`, `apps/api/package.json`,
  `package-lock.json`, `.env.example`, `.gitignore`. **You touch none of them.** If the plan needs
  one, it stops and says so.
- **Worker A** (main folder; PR #74 under review, then the editor's second half): `apps/web` only.
  You change nothing in `apps/web` and no shared type it imports; if one must change, stop and say so.
- Shared documents (security.md, the contract, `users.md`, `auth.md`, the data model, conventions,
  the findings index, the overview's *Built* line) take the fast path; keep to your sections.
- No new dependency.

## 7. Checks, the pull request and the report

- **Locally, once each on the head, one at a time:** `test:unit`, `test:api`; `lint`, `typecheck`,
  `format:check`, `check:links`; `test:component`, the build and `check:build` only if something the
  web imports changes (say why if not run).
- **Real requests** against 3321, each in the report: an access token refused right after a password
  change on another session, after a suspension and after the restore; the changer's own new token
  working; a refresh refused past the 30-day deadline (with a clock you can drive, or a row's deadline
  set in the database); the forgotten password's answer times for an unknown email and a real one,
  several runs each, side by side.
- **PR:** title ≤ 50 (for example `feat(sessions): end a session when it should`), labels `feat`,
  `area:api`, `area:docs`, assigned to the owner. An independent review follows (security, the
  schema). Don't merge.
- **The documents:** security.md (*Tokens and cookies*: the version and the 30 days; *Passwords*: the
  forgotten password's wait and its accepted residual); ADR 0003 (*Revised*); the data model (the two
  columns); the contract only if an answer changes; `users.md`, `auth.md` (*API decisions*, *API
  history*); the findings and the index; the overview's *Built* line if it names the session.
- At the report, `git merge-tree --write-tree` against every open PR. Stop every background shell
  you start; `jq` is not installed — use `gh … --jq`.
