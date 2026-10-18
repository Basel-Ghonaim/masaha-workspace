# OWNERS — The admin's owner accounts and their links to spaces (API)

**Worker B** · worktree `C:\Users\basel\masaha-b`, detached at `82cb03a`. First move it to the
latest `main` (`b66ddfe`, after #57; no schema change since): `git fetch --prune origin`, then
`git switch --detach origin/main`. Branch `feat/admin-owners`, cut with
`git switch --no-track -c feat/admin-owners origin/main`. Databases `masaha_b_dev` / `masaha_b_test`;
API on 3321, web on 5321.

**Size cap:** at most 3 subagents, no self-review subagent, no workflow.
**Plan:** `C:\Users\basel\.prompt\MASAHA_WORKER_B\PLAN\OWNERS_PLAN.md` (`write-plan`; save, then stop).
**Report:** `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\OWNERS_REPORT.md` (`final-report`).
Follow the skills from start to end: `start-work-item`, `write-plan`, `add-error-code` (for each new
code), `open-pr`, `final-report`.

## 1. The task in brief

Step 4 of the build map (`docs/plans/v1-mvp.md` › *4. Owners and users*) is split in two. This item is
its first half, **the owners**, on the API only. The admin creates an owner account (a temporary
password, shown once) or upgrades an existing user to owner, and links the owner to one or more spaces,
which become **verified**. The admin unlinks an owner (a space left with no active owner is unverified
again), and reads the owners list. **Finding 43 is folded:** the linking takes the space's lock, and a
space's read is consistent. The second half (users: search, suspend, role, the admin's temporary
password) is a later item; build nothing of it.

## 2. Read first

In the order workflow §2 *Reading before work* gives. **The capability documents first:**
`docs/features/space-links.md` (the links, "verified", the admin's list) and `docs/features/users.md`
(the forced change; what is not built), then `spaces.md` › *Decisions* (what "verified" locks) and
`auth.md` where the session's links are built. Then:
- ADR 0002 (rules 1–4, as revised) and ADR 0009 (roles at a space, verified, linking by email);
  ADR 0013 (identity modules); ADR 0015 (concurrency);
- `docs/backend/security.md` › *Tokens and cookies* (revocation), *Passwords* (accounts created by
  someone else), *Authorization*;
- `docs/backend/conventions.md` §5 (pagination), §6 (audit), §7 (modules and levels: `users` L1,
  `space-links` L2), *Space access*, *Composed reads*, §11–§13;
- `docs/api/api-contract.md` §1–§4, §5 › *Spaces (the admin)* and *Managed spaces*, §6 (domain codes);
- `docs/architecture/data-model.md` › *Spaces* (`SpaceManager`, "verified"), *Users*;
- `docs/development/testing.md` §1–§4 (every authorization rule tested per role);
- finding 43 in full, and the open findings' titles;
- `apps/api/src/modules/spaces/facts/groupEdit.ts` (the space's lock and `can()`),
  `apps/api/src/modules/spaces/space/space.service.ts` (the read), the `space-links` module, the
  `users` module (hashing, `mustChangePassword`), and `docs/plans/v1-mvp.md` › *Planned API surface*;
- the design, for the shape of what the web will need (no screen is built here):
  `docs/design/screens/44-admin-owners/` (12 frames: the list, add owner, upgrade and link, the
  temporary password shown once, unlink the last owner, link to more spaces) and
  `docs/design/prototype/Admin owners.html`.

## 3. The settled decisions (review them in "Stronger decisions")

**Creating and linking**
- **D1 — one call creates or upgrades an owner and links them**, to the spaces chosen (none, one or
  several), in one transaction: all or nothing. Separate calls link one owner to one more space and
  unlink. Suggested shape, to settle in the plan: `GET /admin/owners`, `POST /admin/owners`,
  `POST /admin/spaces/:spaceId/owners`, `DELETE /admin/spaces/:spaceId/owners/:userId` (the admin links
  owners only; reception links are the owner's, step 6). The planned surface's `/managers` rows are
  outdated by this: update the plan's table.
- **D2 — an email that already has a user account is refused first, then upgraded on purpose.**
  `POST /admin/owners` answers 409 with a new code (such as `EMAIL_HAS_ACCOUNT`); the web shows the
  design's notice, and the admin sends again with an explicit flag (such as `upgradeExisting: true`).
  An upgraded account keeps its own name and password: no temporary password. The upgrade is a role
  change, so security.md's revocation rule applies as written: the user's sessions end.
- **D5 — the edges, each refused with a clear answer:** an email that is already an owner (409, its own
  code: the admin links the owner to more spaces instead); an admin's email (409); a suspended account
  (409, until the users item lifts it); a soft-deleted or unknown space (404, or `invalid_choice` on
  `spaceIds` in the creation's body).
- **D6 — linking a user who holds an active reception link at that space is refused** (409, its own
  code); the reception link is the owner's to deactivate first. No silent change of role at a space.

**Unlinking**
- **D3 — unlinking deactivates the link** (`deactivatedAt`), never deletes it; linking again reactivates
  that same row (the table's key is `(spaceId, userId)`). One rule for every link, owner or reception.
- **D4 — unlinking an owner does not end their sessions.** The links loader reads the links on every
  request, so the access ends at once, and the owner keeps their other spaces. Write this into
  security.md's revocation line, beside the reception rule it differs from.
- Unlinking the last active owner is allowed: the space is unverified again (the web confirms it first,
  per the design).

**Reading**
- **D7 — the owners list is paged** (20, the contract's default), with `?q=` on the name or the email,
  composed as the spaces list is (conventions › *Composed reads*). Each row: the account's id, name,
  email, whether it is suspended, and its active linked spaces (id and both names; a soft-deleted
  space's link counts for nothing, as space-links decides).
- **The global role `OWNER`** puts an account in the owners list and grants nothing at a space
  (ADR 0009: `can()` reads only the link). It stays when the last link goes: the design lists an owner
  "with no space". Record this as a dated *Revised* line in ADR 0009, linked from security.md.

**Finding 43 (folded)**
- **D8 — both halves.** Every link change takes the space's row lock, so `can()` decides on the links
  as they are under it. A creation that links several spaces locks them in ascending id order. And the
  space's read (`space.service.ts`) is consistent: one snapshot or one statement, your choice in the
  plan. Resolve finding 43.

## 4. Sensitive points (an independent review follows: auth, security and transactions)

- **The temporary password** comes from Node's `crypto` and meets the password policy. It is returned
  once, in the creation's answer only. **It never reaches a log, an audit entry or an error**: check
  the request logger's redaction and the audit's `after`.
- **Authorization:** every endpoint is the admin's (`/admin`'s one guard). Test it as USER, OWNER and
  ADMIN, and with a temporary password pending (`PASSWORD_CHANGE_REQUIRED`).
- **Concurrency:** the lock order (spaces by id, then the user's row where a role changes) must not
  deadlock with a facts save or a session refresh (conventions §13). Prove each race you can name in
  the API lane; make the break once (the lock removed) and see the test fail.
- **Audit:** every creation, upgrade, link and unlink is audited in its own transaction
  (conventions §6), names in the contract's style.
- **New domain codes:** each through `add-error-code`, with its line in both of the web's catalogues.

## 5. Findings

- **Folded:** 43 (D8).
- Your new findings number **49–50**.

## 6. Boundaries with worker A

- Worker A works on the web meanwhile. **You touch nothing in `apps/web` except the catalogue lines of
  the error codes you add** (`shared/copy/{english,arabic}/errors.ts`, workflow §9's licence); declare
  them in the plan. A has been told to keep out of those two files while your PR is open.
- **No new dependency** (none is needed).
- The screens (27 Space owners) are A's, later, on this API.

## 7. Checks, the pull request and the report

- **Locally, once each on the head, one at a time:**
  - `test:unit`, `test:component`, `test:api`;
  - `NODE_ENV=production npm run build` and `check:build`;
  - `lint`, `typecheck`, `check:classes`, `format:check` and `check:links`.
- **Real requests** against your API (3321), each said in the report:
  - create a new owner with two spaces, and see the spaces verified;
  - the email-has-an-account refusal, then the upgrade;
  - link to one more space, and unlink;
  - unlink the last owner, and see the space unverified again;
  - the owners list with `?q=`.
- **PR:** title `feat(space-links): add the admin's owners` (≤ 50, or the scope your plan settles), labels
  `feat`, `area:api`, `area:docs` (and `area:web` for the catalogue lines), assigned to the owner. An
  independent review follows. Don't merge.
- **The documents in this PR:**
  - `api-contract.md`: the endpoints, their payloads and errors;
  - the plan's API table;
  - `space-links.md` and `users.md`: *API decisions* and *API history*, and the code maps;
  - security.md: revocation (D4), and the temporary password of an owner created by the admin;
  - ADR 0009's *Revised* line (the global role);
  - `data-model.md`, if the link's rules change;
  - finding 43 resolved;
  - `overview.md`'s *Built* line.
