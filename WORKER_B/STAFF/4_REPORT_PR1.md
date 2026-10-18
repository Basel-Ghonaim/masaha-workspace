# STAFF — execution report, PR 1

Executor: Claude Code, 2026-10-18. Plan: `2_PLAN.md` (approved). Worktree `C:\Users\basel\masaha-b`.

## §0 Sync with #87

- `gh pr view 87` → `"state":"MERGED"`, `mergedAt 2026-10-18T09:06:41Z`, merge commit `10d1e854`.
- Folder clean, detached at `10d1e854` (= `origin/main`). `git log --oneline -3 origin/main` shows
  `10d1e854 Merge pull request #87 from Basel-Ghonaim/feat/space-packages`.
- `git diff --name-status 5e8c979d origin/main`: #87's files only (packages module, `app.ts`,
  `foreignKeyViolation.ts`, the contract, security, conventions, findings 77–81 + index, features, plans,
  overview, `packages/shared/src/packages/*`). No change to `shared/auth/*`, `shared/rate-limit/*`,
  `sessions/*`, `apps/api/test/*`, `schema.prisma`, `packages/shared/src/{core,users,space-links}/*`.
- `app.ts` on main: the packages service (`createPackagesService({ runInTransaction, audit: writeAudit, spaces })`)
  and `manage.use('/packages', …)` after photos — as the plan assumes. `packages/shared/package.json` unchanged.
- Open PRs: #88 (worker A, `feat/admin-owners`) — web files and documents only (`docs/features/space-links.md`,
  `spaces.md`, `overview.md`, `glossary.md`, `frontend/architecture.md`, finding 50); no code file of §7.
  Note: #88 adds web types around the admin's users rows (`userRowView.ts`); C7's additive `receptionSpaces`
  may need a fixture line there — checked at C7 against #88's head.
- Branch `feat/space-staff` cut `--no-track` from `origin/main` (`10d1e854`).
- `docker start masaha-postgres-1` → `masaha-postgres-1`. `npm run build -w @masaha/shared` → `tsc -p tsconfig.build.json` (no error).
- `apps/api/.env`: `PORT=3321`, `masaha_b_dev`, `masaha_b_test` (credentials not printed).
- `npm run db:migrate` → "Already in sync, no schema change or pending migration was found."

## §12.2 First checks (made before any code)

- **3, the resend window:** the resend tests use an injected clock (`createTestApp({ clock: () => new Date(now) })`,
  `now += 60_000`, `password.api.test.ts:229–256`). T2 can use it. ✔
- **5, `ONE_HOUR`:** `shared/rate-limit` exports `FIFTEEN_MINUTES` only; the auth limits write
  `windowMs: 60 * 60_000` inline (`auth.limits.ts:26`). Would follow that (inline, no new constant). ✔
- **7, `AdminUserRow` in the web:** `git grep -n AdminUserRow apps/web` on `origin/main` → nothing. ✔ on main —
  **but open PR #88 (worker A) builds `AdminUserRow` literals** in `OwnersList.component.test.tsx:16,29` and
  `useOwnersList.component.test.tsx:14`. C7's required `receptionSpaces` would break #88's typecheck once both
  are merged (no textual conflict: `git merge-tree` would not show it). See *Stopped*, point 3.
- **8, `LoadedSpace.linksUnder`:** present (`apps/api/src/shared/auth/spaceLinks.ts:16`). ✔
- **Findings 85–86 (documentation rule):** `docs/architecture/documentation.md` and the findings index ask a
  finding for a recorded divergence/problem; nothing asks a problem the item fixes to be recorded as
  *Resolved*. So 85–86 not needed, as the plan says. ✔
- **2, the `CHECK` and the helper — checked by reading, before the migration: FAILS.** See *Stopped*.

## STOPPED — the plan proves false against the code (before any code; nothing edited in the repo)

Branch `feat/space-staff` exists, at `origin/main` (`10d1e854`), no commit, tree clean. No migration created.

1. **The `CHECK` (S4) is broken by two test fixtures outside `createAccount`'s reach** (plan §14: "a `CHECK`
   failure appears outside the helper's reach" → stop and ask). Both write `must_change_password = true`
   with no expiry, so the database will refuse them after C1's migration:
   - `apps/api/src/shared/auth/requireAuth.api.test.ts:81–84` — `prisma.user.update({ data: { passwordHash:
     'temporary-hash', mustChangePassword: true } })` ("refuses a token signed before a temporary password").
   - `apps/api/src/modules/users/handover.api.test.ts:23–32` — `account(pending = true)` creates with
     `prisma.user.create({ data: { …, mustChangePassword: pending } })`.
   (Checked also: `test/admin.ts:46` and `users.api.test.ts:171` put `mustChangePassword` only in a signed
   token, not the row — unaffected.)
   **Offered fix (not chosen):** in C1, add `temporaryPasswordExpiresAt: pending ? <now + 7 d> : null` to the
   handover fixture and `temporaryPasswordExpiresAt: <now + 7 d>` to the requireAuth update — two more test
   files in §7 (about 52 files). No behaviour of either test changes.
2. **A1 breaks an existing test the plan does not name:** `apps/api/src/modules/auth/password.api.test.ts:490`
   "sets the new password once with the recovery's link, **settles a temporary one**, ends every session…"
   creates `createAccount({ mustChangePassword: true })` and resets through `forgot`. Under A1 `forgot` sends
   nothing for a pending account, so `lastToken()` throws "No reset link was sent". The plan rewrites the
   matching security line (Appendix A.2, drop "settles a pending temporary one") but not this test.
   **Offered fix (not chosen):** in C2, the test creates a settled account (`createAccount()`), its title drops
   "settles a temporary one", and its `mustChangePassword: false` assertion stays; the pending case is T1/T4's.
   This is the same kind of rewrite the owner approved for `google.api.test.ts:94` (it asserted the hole).
3. **C7 vs open PR #88 (semantic, not textual):** #88's web tests build `AdminUserRow` objects; a required
   `receptionSpaces` makes them fail typecheck whichever merges second. **Options (not chosen):** (a) whoever
   merges second adds `receptionSpaces: []` to #88's three fixtures (if STAFF merges second, under B's licence
   — "what breaks when a shared type changes" — a fixup in C7 after rebasing on main); (b) tell worker A now
   so #88 is ready for it. The plan's §12.2.7 assumed no web code builds the row; true on `main`, not in #88.

## Resumed — the owner's amendment (plan top, "Amended 2026-10-18"), all three approved

- Re-sync: `origin/main` = `02b1067a` (Merge #88). `git diff --name-status 10d1e854 origin/main` outside
  `apps/web`: documents only (finding 50, features space-links/spaces, frontend architecture, glossary,
  overview). Nothing in `apps/api` or `packages/shared`. No open PR.
- The branch had no commit (`git rev-list --count origin/main..HEAD` → 0), tree clean: moved to `02b1067a`
  with `git reset --hard origin/main`. `npm run build -w @masaha/shared` → no error.


## C1 — `f982572e feat(users): expire temporary passwords` (39)

- Migration: `npm exec -w @masaha/api -- prisma migrate dev --create-only --name temporary_password_expiry` run **once**
  → folder `20261018091812_temporary_password_expiry`; Prisma's SQL (one `ADD COLUMN`) replaced by §4 A3's exactly
  (column, backfill `UPDATE … WHERE must_change_password` **before** the `CHECK`). `npm run db:migrate` →
  "Applying migration `20261018091812_temporary_password_expiry`" … "Your database is now in sync with your schema."
  (`masaha_b_dev`). `masaha_b_test`: applied by the API lane's global setup (the first focused run). Client:
  `prisma generate` → "Generated Prisma Client (7.10.0)"; `models/User.ts` names `temporaryPasswordExpiresAt`.
- First check 2 (the CHECK and the helper): the red run showed it — `Database error. Code: 23514 … violates check
  constraint "users_temporary_password_expiry_check"` from `createAccount({ mustChangePassword: true })` before the
  helper's default; green after. The amendment's two fixtures (`requireAuth.api.test.ts`, `handover.api.test.ts`)
  got `inAWeek()` (a small exported helper in `test/app.ts`, also used by `createAccount`).
- Red before the code:
  - U1 `TypeError: temporaryPasswordExpiry is not a function`; U2 `TypeError: temporaryPasswordExpired is not a function`.
  - T10 `AssertionError: expected 200 to be 403`.
  - T8, T9 (and the existing issue tests) `AssertionError: expected 500 to be 200` — the CHECK refusing an issue without expiry.
  - T7 passed at its first run: the migration (its code) existed before the test DB was migrated. Its proof is B8.
  - T11 ∅ (guards the direction; passed before and after).
- Green: `test:unit … temporaryPassword.unit.test.ts` → "Tests  5 passed (5)"; `test:api` on auth, issueTemporaryPassword,
  schema, handover, requireAuth → "Test Files  5 passed (5)", "Tests  101 passed (101)".
- `npm run lint` → `eslint .` no error; `npm run typecheck` → no error; `prettier --check` on the touched trees → "All matched files use Prettier code style!".
- Departure (small): `ONE_HOUR` n/a here; the clock comment in `users.service.ts` names the expiry.

### Breaks (C1)
- B1 (8 days) → `expected 2026-10-26T10:00:00.000Z to deeply equal 2026-10-25T10:00:00.000Z`; restored → "5 passed".
- B2 (`<` for `<=`) → `expected false to be true`; restored → "5 passed".
- B8 (CHECK dropped in `masaha_b_test`) → T7 `promise resolved "{ id: 2, email: 'b@example.com', …}" instead of rejecting`;
  restoring with the migration's `ADD CONSTRAINT` first failed (`is violated by some row` — the red run's row);
  that row deleted (`DELETE 1`, test DB only), constraint added (`ALTER TABLE`) → T7 "1 passed".
- B9 (the issue keeps the old expiry) → T8 `expected 1792920536919 to be greater than or equal to 1792920597000`; restored → passed.
- B10 (expiry check off, both places) → T10 `expected 200 to be 403`; restored → passed.
- (An early attempt of B1 aborted on a script error before running; the file was restored from its backup, `git status` clean.)
