# Review — PR #62

Head: `18e0edcf850e513d2a022ad5e3505b402508f290`. Base: `d7d800e`. Review started on `aa08e6f10145f0a4215878c8ca23383a23e743e8`; the head moved to `18e0edc` during review and the delta `aa08e6f...18e0edc` (only `apps/api/test/global-setup.ts`) was checked against the findings below.

Verdict: PASS — no blocker; one nit below.

## Findings

### Nit

- **nit, `apps/api/src/modules/users/users.service.ts:317-319`** — the `changeRole` comment says the role is changed "under its session lock, which the caller took (`lockAccount`)". The sole caller, `createAdminRolesService.change` (`apps/api/src/modules/space-links/admin-roles/adminRoles.service.ts:31`), takes `users.lockForAdminChange`, not `lockAccount`. Scenario: a reader following the comment looks for a `lockAccount` call at the call site and misses that the held lock also covers every active admin's row for the `LAST_ADMIN` count. No behaviour change (both locks are `FOR NO KEY UPDATE` on the row). Fix: name `lockForAdminChange` in the comment.

## Checked and fine

- Guard (D5): check order (token → account → suspended → account-pending-without-token → token-pending), 401 without code vs 403 `PASSWORD_CHANGE_REQUIRED`, role from the account, reader wired by the composition root; refresh, general rate limit, request log and links loader paths as decided; the web's 401→refresh→end chain holds.
- Admin-set lock: one statement ordered by id, `OWN_ACCOUNT` before any lock, `LAST_ADMIN` reachable only via the race, lock order against sign-in, refresh, password change, link/unlink, facts save, handover and temporary password without a crossing pair.
- Revocation: suspension, role change and temporary password end sessions and reset links after the write in the same transaction; idempotent repeats write and end nothing; restore ends nothing.
- Temporary password: #60's generator, `no-store`, audit without the password, `GOOGLE_ONLY_ACCOUNT` with the Google-and-password case issued, replace-on-reissue, suspension/Google checks under the session lock.
- Authorization: the three routes behind `/admin`'s guard; guest, USER, OWNER and pending-ADMIN refusals; `ACCOUNT_HAS_LINKS` counting active links of either role with deleted spaces included and deactivated excluded.
- Module levels: `users` imports nothing above it; `shared/` imports no module; the role change uses `users` only through its index.
- Tests: race interleavings via `test/locks.ts`; the governorates audit trigger is dropped in `finally` per test and, in the current head, in `test/global-setup.ts` for killed-run leftovers; helpers live under `test/`; expectations hand-written.
- Documents: ADR 0003 and ADR 0002 revised lines, security.md (Built line, tokens, guard, revocation, recovery), conventions §13, api-contract (three routes, guard 401, `/me/password`, §6 codes), users.md, space-links.md, plan table, overview Built, findings 49 (resolved) and 51/52 (open) with the index, workflow §9 and open-pr step 3.
- Commits and scope: five commits, subjects 39–50 chars; API plus the four codes' lines in the two web catalogues only; no schema change, no dependency.
