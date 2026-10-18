# USERS — The admin's actions on accounts: suspension, role, temporary password (API)

**Worker B** · worktree `C:\Users\basel\masaha-b`, detached at `d7d800e` (#60 merged; the shared
package's `dist` rebuilt): `git fetch --prune origin`, then check `HEAD` is `origin/main`. Branch
`feat/admin-users`, cut with
`git switch --no-track -c feat/admin-users origin/main`. Databases `masaha_b_dev` / `masaha_b_test`;
API on 3321, web on 5321.

**Size cap:** at most 3 subagents, no self-review subagent, no workflow.
**Plan:** `C:\Users\basel\.prompt\MASAHA_WORKER_B\PLAN\USERS_PLAN.md` (`write-plan`; save, then stop).
**Report:** `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\USERS_REPORT.md` (`final-report`).
Follow the skills from start to end: `start-work-item`, `write-plan`, `add-error-code` (for each new
code), `open-pr`, `final-report`.

## 1. The task in brief

The second half of build step 4 (`docs/plans/v1-mvp.md` › *4. Owners and users*), on the API only;
#60 built the first half (owners, links, the users list, the handover).
- **Suspend** an account and **restore** it.
- **Change the role** between `USER` and `ADMIN`; `OWNER` keeps following the owner links.
- **The admin's temporary password:** recovery for a person who lost their email; its handover is
  recorded through #60's handover route. It also lets the admin issue a new temporary password when
  the first was lost (finding 49).
- **The access guard reads the account's current state** on every signed-in request, so a suspension
  or a demotion takes effect at once (D5).

## 2. Read first

In the order workflow §2 *Reading before work* gives.

**The capability documents first:** `docs/features/users.md` (all), `space-links.md` (*Behaviour*,
the role that follows the links, and *API decisions*), `auth.md` (*Refresh*, where a suspended account
is refused).

**Then:**
- ADR 0003 (the session model: D5 revises it), ADR 0009 (with its *Revised* line), ADR 0013, ADR 0015;
- `docs/backend/security.md` › *Tokens and cookies* (revocation), *Passwords* (accounts created by
  someone else, the temporary password, *Recovery without the email*), *Authorization*;
- `docs/backend/conventions.md` §6 (audit), §7 (`users` L1, `space-links` L2), §13 *Concurrency*;
- `docs/api/api-contract.md` §1–§4, §5 › *Users (the admin)* and *Owners (the admin)*, §6;
- `docs/architecture/data-model.md` › *Users and sessions*;
- `docs/development/testing.md` §1–§4;
- `C:\Users\basel\.prompt\MASAHA_DESIGN\DECISIONS_ADMIN.md` › **A5** (the role change, the password
  dialog) and **AD-021**;
- the design, for what the web will need (no screen is built here): `docs/design/screens/46-admin-users/`;
- the code: `apps/api/src/shared/auth/` (`requireAuth`, `requireRole`, the access token), the `users`
  module, `space-links`' `ownerRole.ts` and admin-owners service (the lock order and the temporary
  password #60 built).

## 3. The settled decisions (review them in "Stronger decisions")

- **D1 — one state route per action,** in the style of `PUT /admin/spaces/:spaceId/hidden`:
  `PUT /admin/users/:userId/suspended` `{ suspended }` and `PUT /admin/users/:userId/role` `{ role:
  USER | ADMIN }`; each idempotent (the same state again writes nothing and ends no session), each
  audited. Replace the plan's single `PATCH /admin/users/:userId` row.
- **D2 — the platform never loses its admins.** An admin cannot suspend or demote themselves; and no
  change may leave the platform with **no active admin** (two admins demoting or suspending each
  other at once must not both succeed: settle the lock in the plan, in the lock order of
  conventions §13). Each refusal its own 409 code.
- **D3 — promoting to `ADMIN` is refused while the person holds any active link** (owner or
  reception): 409, the links are unlinked first. An admin is never linked (#60's
  `ACCOUNT_IS_ADMIN`); no silent change at a space. Demoting an admin gives `USER` (an admin has no
  links).
- **D4 — suspension keeps the links.** A suspended owner's space stays verified, the person's
  sessions end, and restoring brings everything back. Write the consequence into the documents: while
  the owner is suspended, the admin edits the space only after unlinking them.
- **D5 — the guard reads the account's current state (revises ADR 0003).** `requireAuth` reads the
  account by its id on every signed-in request: a suspended account is refused at once, and the role
  that `requireRole` and `can()` use is the stored one, not the token's. One lookup by primary key per
  request. Settle in the plan: what the token's claims still carry and why, how the pending password
  change is read, the answer for a suspended account (401 or its code), and that a deleted
  or unknown id is refused. Record ADR 0003's *Revised* line and security.md's *Tokens and cookies*.
- **D6 — the admin's temporary password:** `POST /admin/users/:userId/temporary-password`, answered
  once (`no-store`), as #60's add-an-owner answers it (reuse its generator); sets
  `mustChangePassword`, ends every session and pending reset link, as a reset does. Refused: oneself;
  a suspended account (restore it first); a Google-only account (AD-021: no password to recover,
  their way in is Google); its handover through #60's route. Issuing it again replaces the pending
  one: this resolves finding 49.
- **Every route** sits behind `/admin`'s one guard; every action audited in its own transaction,
  with names in the contract's style; the temporary password never in a log, an audit entry or an
  error.

- **D7 — a workflow rule, in a commit of its own (the owner's decision, outside the item's scope on
  purpose).** Workflow §9 *Merging* leaves a PR ready only when it is clean and its CI ran after
  `main`'s last change; it does not say what happens when another PR merges meanwhile without touching
  this one (#60's case, after #59). Add the rule: **a merge into `main` that deletes or renames no
  file, and changes none of the PR's files, does not call for a rebase or a new CI run; the PR stays
  ready.** Check `git diff --name-status <old main> <new main>` for that. Say it in §9's *Merging*
  list, and align `open-pr`'s step 3 if it needs a word; nothing else. Commit it alone, first, as
  `docs(workflow): a merge apart needs no new CI run` (≤ 50), with the reason in its body: the
  rule decides how every worker treats its open PR. It takes `format:check` and `check:links` only.

**Not in this item:** A3's `status=deleted` filter (finding 44) is a separate small item; the screens
(27 Space owners, 29 Users) are worker A's, later.

## 4. Findings

- **Folded:** 49 (D6).
- **Look at in *Related findings*:** 39 (the users service takes its hashing as a parameter only its
  unit test passes) — this item changes that service; propose folding it, with its cost.
- Your new findings number **51–52** (50 is taken by #60's fixes).

## 5. Sensitive points (an independent review follows: auth, security, transactions)

- **D5 changes every signed-in request.** Prove it per role and per state (active, suspended,
  demoted, pending password change) in the API lane; mind every route that reads `req.auth`, the
  links loader, and the refresh. Measure nothing you cannot prove; state the cost in the plan.
- **Races, each proven with its lock removed once:** two admins demoting or suspending each other;
  a suspension racing a refresh or a sign-in (no session may survive it); a role change racing a link
  (#60's lock order: the space, then the person); a temporary password racing a password change.
- **Revocation:** suspension, a role change and the temporary password each end the person's
  sessions in the same transaction; an idempotent repeat ends none.
- **The temporary password:** the same guarantees and tests as #60's (its generator, `no-store`, the
  log redaction's unit test, no audit or error holds it).

## 6. Boundaries with worker A

- Worker A works on the web meanwhile. **You touch nothing in `apps/web` except the catalogue lines of
  the error codes you add** (`shared/copy/{english,arabic}/errors.ts`, under workflow §9's licence),
  declared in the plan. A keeps out of those two files while your PR is open.
- If D5 changes the session's shape the web reads (a claim, the refresh's answer), stop and say so in
  the plan: that is a contract change worker A must know of.
- No new dependency.

## 7. Checks, the pull request and the report

- **Locally, once each on the head, one at a time:** `test:unit`, `test:api`; `lint`, `typecheck`,
  `format:check`, `check:links`. `test:component` and the build only if the web's catalogue lines
  changed (they did, if you added codes): then also `test:component`, `NODE_ENV=production npm run
  build` and `check:build`.
- **Real requests** against your API (3321), each said in the report: suspend an owner (their next
  request is refused at once, their space stays verified), restore them; demote an admin with a
  second admin present; the last admin refused; promote a linked user refused; issue a temporary
  password, record its handover, sign in with it (the change is forced).
- **PR:** title `feat(users): suspend, role and temporary password` (≤ 50, or what your plan
  settles), labels `feat`, `area:api`, `area:docs` (and `area:web` for the catalogue lines), assigned
  to the owner. An independent review follows. Don't merge.
- **The documents in this PR:** workflow §9 (D7, its own commit); `api-contract.md` (the routes, payloads and codes); the plan's API
  table (D1); `users.md` (*API decisions*, *API history*, the code map, what is not built);
  `space-links.md` if D3 or D4 change what it says; `security.md` (revocation, the guard, the admin's
  recovery, its *Built* line); ADR 0003's *Revised* line (D5); `data-model.md` if a rule changes;
  finding 49 resolved; `overview.md`'s *Built* line.
- Stop every background shell you start; `jq` is not installed — use `gh … --jq`.
