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
its first half, **the owners**, on the API only.
- **Adding an owner:** the admin creates an owner account (a temporary password, shown once) or
  upgrades an existing user, and links it to a space, which becomes **verified**.
- **Linking and unlinking:** the admin links more spaces, one at a time. Unlinking leaves a space with
  no active owner unverified again.
- **Reading:** the admin reads the users list, which the owners page shows filtered to owners.
- **Finding 43 is folded:** the linking takes the space's lock, and a space's read is consistent.

The second half, **the users** (suspend, the role change, the admin's temporary password), is a later
item: build none of its actions.

## 2. Read first

In the order workflow §2 *Reading before work* gives.

**The capability documents first:**
- `docs/features/space-links.md`: the links, "verified", the admin's list;
- `docs/features/users.md`: the forced change, and what is not built;
- `spaces.md` › *Decisions*: what "verified" locks;
- `auth.md`, where the session's links are built.

**The design decisions, which this item applies:** the owner approved them on 2026-10-10, in
`C:\Users\basel\.prompt\MASAHA_DESIGN\DECISIONS_ADMIN.md`. Read **A4, A5 and A6**, and the *Rules
changed* line on `PATCH /admin/users`. The decisions in §3 below already follow them.

**Then:**
- ADR 0002 (rules 1–4, as revised) and ADR 0009 (roles at a space, verified, linking by email);
  ADR 0013 (identity modules); ADR 0015 (concurrency);
- `docs/backend/security.md` › *Tokens and cookies* (revocation), *Passwords* (accounts created by
  someone else), *Authorization*;
- `docs/backend/conventions.md`:
  - §5 (pagination), §6 (audit), §7 (modules and levels: `users` L1, `space-links` L2);
  - *Space access* and *Composed reads*;
  - §11–§13;
- `docs/api/api-contract.md` §1–§4, §5 › *Spaces (the admin)* and *Managed spaces*, §6 (domain codes);
- `docs/architecture/data-model.md` › *Spaces* (`SpaceManager`, "verified") and *Users and sessions*;
- `docs/development/testing.md` §1–§4 (every authorization rule tested per role);
- finding 43 in full, and the open findings' titles;
- the code:
  - `apps/api/src/modules/spaces/facts/groupEdit.ts` (the space's lock and `can()`);
  - `apps/api/src/modules/spaces/space/space.service.ts` (the read);
  - the `space-links` module;
  - the `users` module (hashing, `mustChangePassword`);
- `docs/plans/v1-mvp.md` › *Planned API surface*;
- the design, for the shape of what the web will need (no screen is built here):
  - `docs/design/screens/44-admin-owners/`, 12 frames: the list, add owner, upgrade and link, the
    temporary password shown once, unlink the last owner, link to more spaces;
  - `docs/design/prototype/Admin owners.html`.

  Where a frame differs from the design decisions, **the decisions win**.

## 3. The settled decisions (review them in "Stronger decisions")

**Adding an owner**
- **D1: one space at a time.** Adding an owner creates the account or upgrades an existing one, and
  links it to **one** space, in one transaction: all or nothing. The design's submit is «إنشاء حساب وربط».
  Linking more spaces is a separate call, one space each time.
- **D2: an email that already has a user account is refused first, then upgraded on purpose.**
  - Adding answers 409 with a new code (such as `EMAIL_HAS_ACCOUNT`), and the web shows the design's
    notice («سيُرقّى حسابه»). The admin then sends again with an explicit flag (such as
    `upgradeExisting: true`).
  - An upgraded account keeps its own name and password: no temporary password.
- **D3: the temporary password's handover is recorded** (A5). The one-time password dialog asks how it
  was handed over (WhatsApp, in person, other), after the password is shown. A small follow-up call
  writes the chosen channel to the audit, tied to the creation it follows. Settle its path and payload
  in the plan: the users item will reuse it for the admin's temporary password.

**Linking and unlinking**
- **D4: linking from a space may choose any person** (A4), an owner or a user, by name or email.
  Linking a user makes them an owner. The web says what will happen before it is done (A5), so the
  link call needs no extra flag.
- **D5: refused, each with a clear answer:**
  - adding an email that is already an owner (409, its own code: the admin links them instead);
  - an admin (409);
  - a suspended account (409, until the users item lifts it);
  - a soft-deleted or unknown space (404);
  - a person who holds an active reception link at that same space (409, its own code). The
    reception link is the owner's to deactivate first; no silent change of role at a space.
- **D6: unlinking deactivates the link** (`deactivatedAt`), never deletes it. Linking again
  reactivates that same row (the table's key is `(spaceId, userId)`). One rule for every link, owner
  or reception. Unlinking the last active owner is allowed: the space is unverified again (the web
  confirms it first).
- **Suggested paths, to settle in the plan:**
  - `POST /admin/owners` (add);
  - `POST /admin/spaces/:spaceId/owners` (link);
  - `DELETE /admin/spaces/:spaceId/owners/:userId` (unlink).

  The admin links owners only; reception links are the owner's, step 6. Update the plan's API table:
  its `/managers` and `/admin/owners` rows are outdated by this item.

**The global role**
- **D7: the global role `OWNER` follows the links** (A5, ADR 0009).
  - A user becomes `OWNER` with their first active owner link, and is `USER` again when their last
    one ends.
  - Both are role changes, so security.md's revocation applies: the person's sessions end.
  - An unlink that leaves the person other owner links changes no role and ends no session: the links
    loader reads the links on every request, so access to that space ends at once. Write this into
    security.md's revocation line, beside the reception rule.
  - Record the rule as ADR 0009's *Revised* line, and in the plan's `PATCH /admin/users` row: the role
    offered there is `USER` or `ADMIN`, and `OWNER` follows the links.

**Reading**
- **D8: the owners page is a view of the users list** (A6). Build the read side of
  `GET /admin/users`:
  - paged (20, the contract's default), composed as the spaces list is (conventions ›
    *Composed reads*);
  - `?q=` on the name or the email, a role filter (`role=owner` gives the owners page), and a state
    filter (active or suspended);
  - each row: the account's id, name, email, role, whether it is suspended, and its active owner links
    (each space's id and both names; a soft-deleted space's link counts for nothing, as space-links
    decides).

  Build no `GET /admin/owners`. The users item adds the actions only.

**Finding 43 (folded)**
- **D9: both halves.**
  - Every link change takes the space's row lock, so `can()` decides on the links as they are under it.
  - The space's read (`space.service.ts`) is consistent: one snapshot or one statement, your choice in
    the plan.
  - Resolve finding 43.

**Not in this item:** A3's `status=deleted` filter on `GET /admin/spaces` (finding 44) waits for a
later item.

## 4. Sensitive points (an independent review follows: auth, security and transactions)

- **The temporary password** comes from Node's `crypto` and meets the password policy. It is returned
  once, in the creation's answer only. **It never reaches a log, an audit entry or an error**: check
  the request logger's redaction and the audit's `after`.
- **Authorization:** every endpoint is the admin's (`/admin`'s one guard). Test it as USER, OWNER and
  ADMIN, and with a temporary password pending (`PASSWORD_CHANGE_REQUIRED`).
- **Concurrency:** the lock order is the space's row, then the user's row where the role changes. It
  must not deadlock with a facts save or a session refresh (conventions §13). Prove each race you can
  name in the API lane; make the break once (the lock removed) and see the test fail.
- **Audit:** every creation, upgrade, link, unlink and handover is audited in its own transaction
  (conventions §6), with names in the contract's style.
- **New domain codes:** each through `add-error-code`, with its line in both of the web's catalogues.

## 5. Findings

- **Folded:** 43 (D9).
- Your new findings number **49–50**.

## 6. Boundaries with worker A

- Worker A works on the web meanwhile. **You touch nothing in `apps/web` except the catalogue lines of
  the error codes you add** (`shared/copy/{english,arabic}/errors.ts`, under workflow §9's licence).
  Declare them in the plan. A is told to keep out of those two files while your PR is open.
- **No new dependency** (none is needed).
- The screens (27 Space owners, 29 Users) are A's, later, on this API.

## 7. Checks, the pull request and the report

- **Locally, once each on the head, one at a time:**
  - `test:unit`, `test:component`, `test:api`;
  - `NODE_ENV=production npm run build` and `check:build`;
  - `lint`, `typecheck`, `check:classes`, `format:check` and `check:links`.
- **Real requests** against your API (3321), each said in the report:
  - add a new owner with a space: the space is verified and the temporary password shown once; then
    record its handover;
  - the email-has-an-account refusal, then the upgrade;
  - link a plain user from a space: they become an owner;
  - link to one more space, unlink one of two: the role stays;
  - unlink the last one: the role and the space's verification go;
  - `GET /admin/users?role=owner&q=`.
- **PR:** title `feat(space-links): add the admin's owners` (≤ 50, or the scope your plan settles),
  labels `feat`, `area:api`, `area:docs` (and `area:web` for the catalogue lines), assigned to the
  owner. An independent review follows. Don't merge.
- **The documents in this PR:**
  - `api-contract.md`: the endpoints, their payloads and errors;
  - the plan's API table;
  - `space-links.md` and `users.md`: *API decisions* and *API history*, and the code maps;
  - security.md: revocation (D7), and the temporary password of an owner created by the admin;
  - ADR 0009's *Revised* line (D7);
  - `data-model.md`, if the link's rules change;
  - finding 43 resolved;
  - `overview.md`'s *Built* line.
