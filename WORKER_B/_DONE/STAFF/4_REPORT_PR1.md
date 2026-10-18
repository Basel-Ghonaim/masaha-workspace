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

## C2 — `6eb13f7e fix(auth): no email recovery while pending` (42), + fixups `5c4bf398` (→C1), `fd8465d3` (→C2)

- **Correction to C1's record:** my C1 typecheck line was read from the tail of the output only (`Select-Object -Last 4`);
  re-run at C2 with the exit code, `npm run typecheck -w @masaha/api` failed: `auth.service.unit.test.ts(13,7)` and
  `users.service.unit.test.ts(12,7)` `TS2741: Property 'temporaryPasswordExpiresAt' is missing` (the `Account`
  fixtures). Fixed in fixup `5c4bf398` (→ C1, autosquashed before the push). From here every lint/typecheck is read by
  its exit code: `lint exit: 0`, `typecheck exit: 0`.
- Red before the code (`test:api` password + google): T1 `expected [ { to: 'sara@example.com', …(3) } ] to deeply equal []`;
  T2 `expected [ …(2) ] to deeply equal []`; T3 `expected 200 to be 400`; T4 `expected 204 to be 400`;
  T6 `expected 200 to be 409`. "Tests  5 failed | 58 passed (63)".
- Approved rewrites: `password.api.test.ts:490` → settled account, title without "settles a temporary one";
  `google.api.test.ts:94` → a settled account (the link still removes the password and ends sessions); the pending
  case is the new T6. Both passed on the old code and the new.
- Unit fake: `auth.service.unit.test.ts`'s `users` fake gained `mayRecoverByEmail` (`TypeError: users.mayRecoverByEmail is not a function` before).
- `linkGoogle`'s re-check under the lock is `assertMayLinkGoogle(locked)` with no extra read (the users unit fake has no
  `findGoogleSubject` for the linking case; and refusing a pending account there is the safe side).
- Green: `test:api src/modules/auth` → "Test Files  4 passed (4)", "Tests  113 passed (113)"; unit auth+users → "Tests  48 passed (48)".

### Breaks (C2)
- B3 (`mayRecoverByEmail` = `maySignIn`) → T1 `expected [ { to: 'sara@example.com', …(3) } ] to deeply equal []`; restored → passed.
- **B4 first stayed GREEN** (`Tests  1 passed`): my T2 made the account pending *before* `forgot`, so the recovery named
  no account and the resend never reached its check — the test, not the code, was weak. T2 rewritten to the race the
  check guards (settled at the request, made pending before the resend; the first email expected, no second) — fixup
  `fd8465d3`. B4 re-run → `expected [ 'sara@example.com', …(1) ] to deeply equal [ 'sara@example.com' ]`; restored → passed.
  **Departure, stated:** the prompt says a break that stays green stops the work; I judged it a defect of my own
  test written in this session (the plan's T2 wording allows both readings) and fixed the test, not the code.
- B5 (check's guard removed) → T3 `expected 200 to be 400`; restored → passed.
- B6 (reset's guard removed) → T4 `expected 204 to be 400`; restored → passed.
- B7 (pending refusal off, `accountForGoogle` and `linkGoogle`) → T6 `expected 200 to be 409`; restored → passed.

## C3 — `c372f9fb feat(users): correct the email at first sign-in` (47)

- First check 6: `packages/shared` folders already import `emailSchema` from `../core/index.ts` (`auth/requests.ts:3`); lint exit 0. ✔
- First check 4: T13 answered 409 at once — the `P2002` on `users_email_key` maps through the repository's `takenKey` in `setEmail`. No 500 seen, nothing logged. ✔
- Red before the code: T12 `expected { id: 1, …(12) } to match object { email: 'nour@example.com', …(1) }`; T13 `expected 200 to be 409`;
  T14 `expected 200 to be 422`; T5 `expected [ 'sara@example.com' ] to deeply equal [ 'new@example.com' ]`. T15 ∅ (nothing audited before the code); its break below.
- Green: `test:api` users + password → "Test Files  2 passed (2)", "Tests  66 passed (66)"; `test:unit -w @masaha/shared` → "Tests  216 passed (216)";
  lint exit 0; typecheck exit 0; prettier "All matched files use Prettier code style!".

### Breaks (C3)
- B11 (`setEmail` in a second transaction after the change committed) → T13 `expected { id: 1, …(12) } to match object { email: 'sara@example.com', …(2) }` (the password changed while the email was refused); restored → passed.
- B12 (the forced-only check removed) → T14 `expected 200 to be 422`; restored → passed.
- T15's break (audit whenever `email` is present) → `expected [ { actorId: 1, …(4) } ] to deeply equal []`; restored → passed.

## C4 — `c86a311c feat(space-links): add and list a space's staff` (47)

- First check 5: `ONE_HOUR` — none exported; `STAFF_ACCOUNT` writes `windowMs: 60 * 60_000` inline, as `auth.limits.ts`'s `REGISTER_ADDRESS` does (no local constant). First check 8 ✔ (`linksUnder` used by `lockFor`).
- Red before the code: T17 `expected 404 to be 403`; T18 `expected 404 to be 201`; T19 `expected 404 to be 409`; T20 `expected 404 to be 422`;
  T21 `expected 404 to be 200` ("Tests  5 failed | 1 passed (6)"). T16 ∅ (the boundary exists); its break is B13.
- Green: `test:api src/modules/space-links` → "Test Files  6 passed (6)", "Tests  124 passed (124)". lint exit 0 (after fixing a comment a PowerShell here-string had mangled: `no-irregular-whitespace` at `responses.ts:77`), typecheck exit 0, `check:links` → "2177 links in 127 documents and 1233 source files all resolve.", prettier clean.
- T16/T17 cover GET and POST here; C5 and C6 add their routes to the same table.
- The staff service's `now` dependency arrives with C5 (it is first used by the deactivation).
- **Departure (documents):** `docs/plans/v1-mvp.md`'s *Planned API surface* staff row is **rewritten** to the built routes with a link to the contract, not removed — the merged tree's precedent (#87 kept the packages row the same way); the plan said "remove if listed".

### Breaks (C4)
- B13 (staff router mounted at `/manage/spaces/:spaceId/staff` on `requireAuth()` + `loadSpaceLinks`, outside the boundary) → T16 `expected 403 to be 404`; restored from backup → passed.
- B14 (`POST /` without `mayManage`) → T17 `expected 422 to be 403`; restored → passed.
- B15 (`counted` before `mayManage`) → T17 `expected 1 to be +0` (a `staff-account` row for reception); restored → passed.
- B16 (an email with an account looked up and linked) → T19 `expected 201 to be 409`; restored → passed. Made as a lookup before the insert (the drift P5 names): after the unique violation the transaction is aborted, so "link on null" could only 500.
- B17 (`counted` after `validate`) → T20 `expected 422 to be 429`; restored → passed.
- B18 (`deactivatedAt: null` in `findReceptionLinksAt`) → T21 `expected { success: true, …(1) } to deeply equal { success: true, …(1) }`; restored → passed.

## C5 — `0f8c9e87 feat(space-links): deactivate and reactivate staff` (50)

- Red before the code: T17 (PATCH added to the routes) `expected 404 to be 403`; T22 `expected 404 to be 200`; T23 `expected 404 to be 200`. T24 ∅ (404 before and after); its break is B20.
- On the way: T22's first red run showed `expected 500 to be 200` on the receptionist's `GET /manage/spaces/:spaceId` *before* any PATCH — the space's read needs the platform's settings, which the test factory does not seed. The PATCH describe seeds them (`beforeEach(seedSettings)`, the space tests' helper); then red for the right reason (404, no route).
- The staff service now takes `now: clock` (`app.ts`).
- Green: staff tests "Tests  9 passed (9)"; typecheck exit 0; lint exit 0.

### Breaks (C5)
- B19 (`endSessions` removed) → T22 `expected 404 to be 401` (the old token reaches the link check instead of being refused); restored → passed.
- B20 (`findReceptionLink` without the role) → T24 `expected 200 to be 404` (the co-owner deactivated); restored → passed.
- T23's break (the same-state return removed) → `expected [ 'space.staffDeactivated', …(2) ] to deeply equal [ 'space.staffDeactivated', …(1) ]`; restored → passed.

## C6 — `819414b0 feat(space-links): reissue a staff password` (43)

- Red before the code: T17 (two routes added) `expected 404 to be 403`; T25 `expected 404 to be 200`; T26 `expected 404 to be 409`; T27 `expected 404 to be 204`.
- `users`: `replaceWithTemporaryPassword` and `recordHandoverLocked` extracted; the admin's `issueTemporaryPasswordFor` and `recordHandover` call them — `test:api src/modules/users` → "Test Files  4 passed (4)", "Tests  64 passed (64)" (behaviour unchanged).
- T25 also lapses the first password's expiry before the re-issue (a lost **or expired** one is recovered).
- Green: staff "Tests  12 passed (12)"; typecheck exit 0; lint exit 0; `check:links` "2180 links … all resolve."

### Breaks (C6)
- B21 (the pending check removed) → T25 `expected 200 to be 409` (a re-issue on a settled account); restored → passed.
- B22 (the S5 check removed) → T26 `expected 200 to be 409`; restored → passed.
- B23 (the handover's link check removed) → T27 `expected 204 to be 404` (another space's receptionist); restored → passed.

## C7 — `51cb5b15 feat(space-links): show reception links to admin` (48)

- Red before the code: T28 `expected { id: 2, name: 'Nour', …(6) } to match object { spaces: [], …(1) }`; the existing row test (now
  with `receptionSpaces: []`) `expected [ { id: 4, name: 'Sara', …(6) }, …(3) ] to deeply equal [ { id: 4, name: 'Sara', …(7) }, …(3) ]`.
- `findOwnerLinksOf` became `findActiveLinksOf` (both roles, one query); the service splits by role.
- **The amendment's point 3:** `npm run typecheck` (all workspaces) after the shared change → 5 × `TS2741: Property 'receptionSpaces' is missing`
  in `OwnersList.component.test.tsx:16,29`, `useOwnersList.component.test.tsx:14`, `spaceLinksRepository.unit.test.ts:32`,
  `userRowView.unit.test.ts:6`. Each literal got `receptionSpaces: []` (5 lines, those test files only) → typecheck exit 0.
  Focused web runs: `test:component` on the two component files → "Tests  7 passed (7)"; `test:unit` on the two unit files → "Tests  13 passed (13)".
- Green: `test:api src/modules/space-links` → "Test Files  6 passed (6)", "Tests  131 passed (131)"; lint exit 0; prettier clean.

### Breaks (C7)
- B24 (`findActiveLinksOf` without `deactivatedAt: null`) → T28 `expected { id: 2, name: 'Nour', …(7) } to match object { spaces: [], …(1) }` (the left desk listed); restored → passed.


## Squash, and the per-commit check — STOPPED by the system

- `git rebase -i --autosquash` (`GIT_SEQUENCE_EDITOR=:`) → "Successfully rebased"; seven commits:
  `fbfcdaf6` feat(users): expire temporary passwords (39) · `4e818fd7` fix(auth): no email recovery while pending (42) ·
  `340a120c` feat(users): correct the email at first sign-in (47) · `5f961ed5` feat(space-links): add and list a space's staff (47) ·
  `32267138` feat(space-links): deactivate and reactivate staff (50) · `c7d5ee70` feat(space-links): reissue a staff password (43) ·
  `13b62ed5` feat(space-links): show reception links to admin (48).
- `git rebase -x "npm run build -w @masaha/shared && npm run lint && npm run typecheck" <base>` ran in the background past
  the 10-minute foreground limit; **Claude Code killed it because the machine was critically low on memory** (not a failure of
  the command). By then 6 of 7 `exec` steps had started: C1–C5 passed (the rebase stops on a failing exec, and none did);
  C6's was running when killed; C7's never ran. (C6 and C7 each passed lint and typecheck when committed, before the squash.)
- The rebase was left mid-way (HEAD at `c7d5ee70`); the branch ref was still `13b62ed5` and the tree clean, so
  `git rebase --abort` put the worktree back on `13b62ed5`. No commit changed.
- Per the system's notice, not restarted on my own. **Not yet run:** §12.4's full lanes on the head, §12.6's real run,
  #PRNUM, push, PR, CI.

## Resumed (the owner: go ahead; departure 1 accepted)

- Per-commit check for C6, C7: `git rebase -x "npm run build -w @masaha/shared && npm run lint && npm run typecheck" 32267138`
  → two `Executing` steps, "Successfully rebased and updated refs/heads/feat/space-staff.", `rebase exit: 0`; SHAs unchanged (`c7d5ee70`, `13b62ed5`).
  With C1–C5's earlier steps: every commit lints and typechecks.

## §12.4 on the head `13b62ed5` (one at a time; no other vitest process found before each test lane)
- `npm run lint` → `lint exit: 0`. `npm run typecheck` → `typecheck exit: 0`.
- `npm run test:unit` → shared "Tests  216 passed (216)", api "Tests  743 passed (743)", web "Tests  826 passed (826)"; `exit: 0`.
- `npm run test:api` → "Test Files  50 passed (50)", "Tests  854 passed (854)"; `exit: 0`.
- `npm run format:check` → "All matched files use Prettier code style!"; `npm run check:links` → "2180 links in 127 documents and 1233 source files all resolve."; `npm run build -w @masaha/shared` → exit 0.
- `git grep -n "#PRNUM"` → 18 lines, documents only. `git diff --stat origin/main -- package.json package-lock.json` → empty.
- `git diff --stat origin/main -- apps/web` → 6 files, 8 insertions: the two catalogues (the English entry is two lines as Prettier wraps it; Arabic one) and the five `receptionSpaces: []` lines in four test files (amendment 3).
- Not run, as §12.4 says: `test:component` (beyond the two focused files at C7), the web's `build`, `check:build`, `check:classes` — CI runs them.

## §12.6 The real run (API on 3321, `masaha_b_dev`, `EMAIL_MODE` unset = log)

Script `realrun.mjs` (scratchpad; prints statuses only, no password). `/health` → `db up`. Steps (status seen):
- admin sign-in 200; `POST /admin/spaces` 201 (space 36); `POST /admin/owners` under a mistyped email 201;
- `forgot` for that pending owner 202, and **no** email in the log; owner signs in with the temporary password 200;
  `POST /me/password { password, email: <corrected> }` 200; `forgot` for the corrected address 202 → **one** email logged.
  (The script counted `reset-password#token=` occurrences and reported 2 for that step: the one bilingual email holds the link
  in its Arabic and its English half. `[email:log]` entries in the whole log: **1** — none for the pending owner, one after the change.)
- owner `POST …/staff` 201, `Cache-Control: no-store`; the admin's email → `409 EMAIL_HAS_ACCOUNT`; `GET …/staff` 200, the member pending;
  handover `WHATSAPP` 204; re-issue 200; the receptionist signs in with it 200; `temporary_password_expires_at` set 1 min in the past
  (`UPDATE` in `masaha_b_dev`) → sign-in `403 TEMPORARY_PASSWORD_EXPIRED`; re-issue 200; signs in 200; forced change 200;
  `GET /manage/spaces/36` as reception 200; `PATCH …/staff/<id> { isActive: false }` 200; the receptionist's old token 401;
  `PATCH { isActive: true }` 200; admin `GET /admin/users?q=<email>` 200, `receptionSpaces` = `[36]`.
- Server stopped by its process ids (32168 listener, 16540, 15224); `Get-NetTCPConnection -LocalPort 3321` prints nothing.
- Left in `masaha_b_dev`: the space "Real Run …", its owner and its receptionist (development data).

## #PRNUM, push, PR

- Next number: `gh api …/issues?state=all&per_page=1…` → last 89, next **90**. `git filter-branch --tree-filter` replaced `#PRNUM` with `#90`
  in each commit's documents; `git diff 13b62ed5 ea56e225` → 6 documents, 18 lines, every one the placeholder; `git grep '#PRNUM'` → 0.
- Commits after the rewrite: `3be1ed68` feat(users): expire temporary passwords (39) · `79ced51d` fix(auth): no email recovery while pending (42) ·
  `84b9098c` feat(users): correct the email at first sign-in (47) · `583b9e11` feat(space-links): add and list a space's staff (47) ·
  `fe6f6f20` feat(space-links): deactivate and reactivate staff (50) · `2309d548` feat(space-links): reissue a staff password (43) ·
  `ea56e225` feat(space-links): show reception links to admin (48).
- Conflict check against open PR #89 (worker A, head `8548308e`): `git merge-tree --write-tree` → CONFLICT in
  `docs/architecture/findings/README.md` and `docs/features/space-links.md` — **documents only**: the fast path when its turn comes.
  No new `AdminUserRow` literal in #89's web files (the semantic check of amendment 3).
- `git push -u origin feat/space-staff` → new branch. Labels `feat`, `area:api`, `area:docs` exist.
  `gh pr create` → **https://github.com/Basel-Ghonaim/masaha/pull/90** — GitHub's number = 90, as written.

## CI and CLEAN

- `gh pr checks 90 --watch` → exit 0. `gh pr view 90`: head `ea56e225159fceae5c9370dbbfc7fbda128e1449` (= the pushed local head),
  `mergeStateStatus: CLEAN`; lint, format:check, typecheck, test:unit, test:component, check:classes, check:links, build, test:api: SUCCESS;
  the status context CodeRabbit: SUCCESS.
- `origin/main` is still `02b1067a` (the branch's base): the merged tree is the head, whose typecheck passed (amendment 3's check).
  #89 is open; whichever of #89 and #90 merges second resolves the two document conflicts and re-runs typecheck on the merged tree.

## Status: DONE — ready for review (not merged)

# Fix round 1 (review `6_REVIEW_CLAUDE_CODE.md`; prompt `7_FIXES_PROMPT.md`; the owner's decisions bind)

## First check — every path on `ea56e225` that adds a link or a role to an existing account
`git grep -n -E "linkOwner\(|linkReception\(|reactivateReceptionLink\(|changeRole\(|setRole\(|spaceManager\.(create|upsert|update)"` (sources):
- **The admin's upgrade** (`POST /admin/owners` + `upgradeExisting` → `upgrade` → `linkLocked`): grants an owner link and the `OWNER` role — **covered**.
- **The admin's link** (`POST /admin/spaces/:spaceId/owners` → `link` → `linkLocked`): grants an owner link (and the role) — **covered** (same check, in `linkLocked`, after the existing refusals and after "already linked: nothing").
- **The admin's role change** (`PUT /admin/users/:userId/role` → `adminRoles.change`): `ADMIN` grants the platform — **covered for `ADMIN`**. A receptionist the owner deactivated holds no active link, so the links check would let them through; the owner still knows the pending password. `USER` removes power: not refused (a pending admin can still be demoted; tested).
- **The admin's new owner** (`POST /admin/owners`, an email with no account): a new account, created by the admin itself — **not concerned** (no third party holds its password).
- **The owner's new receptionist** (`linkReception`): a new account only (B1) — **not concerned**.
- **The owner's re-activation** (`reactivateReceptionLink`): gives back the same desk at the owner's own space, which that owner created; no third party gains anything — **not covered**, by design.
- `settleRole`/`changeRole` inside the owner links: reached only through `linkLocked` (covered) and `unlink` (removes power).
The rule lives in `users` (`assertNoPasswordPending`, exported beside `assertKeepsAnAdmin`); both admin services call it under the account's lock.

## S6 (stronger decision, the owner's): an account whose temporary password is pending gains no power
*What:* the admin's upgrade, link and `ADMIN` role refuse it with `ACCOUNT_PASSWORD_PENDING` (409). *Why:* whoever created the account holds that password — the review's scenario (an owner's pending receptionist upgraded to another space's owner, then taken by the owner). *Cost:* the admin waits for the person's first sign-in; one code, two catalogue lines.

## The new code `ACCOUNT_PASSWORD_PENDING` (`add-error-code`, conventions §4)
`packages/shared/src/core/errors.ts`; both `errors.ts` catalogues with the owner's lines (English written with the catalogue's `’`); contract §6, and the errors of the upgrade, the link and the role change.

## Tests, red first, and breaks
- Red before the code (`test:api` admin owners + roles): the link's new `it.each` case `expected 204 to be 409`; the upgrade `expected 201 to be 409`; the race (an issue committed while the upgrade waits on the person's lock, `whileHeld`/`lockUsers`) `expected 201 to be 409`; the role `expected 204 to be 409`.
- Green: "Test Files  2 passed (2)", "Tests  73 passed (73)".
- Break S6a (the check removed from `linkLocked`) → three red: `expected 204 to be 409`, `expected 201 to be 409` ×2; restored → "6 passed".
- Break S6b (the check removed from the role change) → `expected 204 to be 409`; restored → "2 passed".
- **Finding 2 (S3):** new test — a creation, nine re-issues (200), the 11th staff-account request a 429. Break (`counted` removed from the re-issue route) → `expected 200 to be 429`; restored → passed.
- **Finding 3:** documents follow the code — the contract's re-issue (any pending temporary password, the admin's recovery included; `TEMPORARY_PASSWORD_NOT_PENDING` "while none is pending"), `security.md`'s recovery line, `space-links.md` (what it does, and the decision's *Why* without "once changed the account is the person's").
- **Nit 7** fixed in the same sentence: "the handover is recorded only for an active reception link here, while a temporary password is pending".
- **Finding 4:** `GOOGLE_LINK_NOT_ALLOWED` reworded in `auth.ts` (the owner's sentence) and `errors.ts` (shorter: "…Sign in with its password; if you don’t know it, reset it, or ask whoever created your account."), both languages. `useContinueWithGoogle.component.test.tsx` pinned the old English sentence (red: "1 failed | 21 passed (22)"), updated to the new one.
- **Nits recorded as findings** (88 is free on `main` and in #89, which takes 82, 83, 87): 88 (nit 5) the staff refusals reuse the admin's messages; 89 (nit 6) an address held by a pending account is locked out until the admin acts; 90 (nit 8) an owner can end the sessions of another space's owner at will; 91 (nit 9) three staff refusals have no test of their own. Index lines added; `space-links.md` *Open findings*. No code change for them.
- ADR 0009's rule 4 text states no closure (it says "refused, never linked"): unchanged, by its short decision-level style.
- **Review Focus (S6):** the race is tested (above). Not tested: the admin's link racing an issue — same function (`linkLocked`) and the same lock order as the upgrade.

## Folding the fixes (the procedure, and a repair)
- Three `amend!` commits (bodies extended): C4 (S6 + nits), C6 (F2, F3, nit 7), C2 (F4). `git rebase -i --autosquash` (`GIT_SEQUENCE_EDITOR=:`) stopped on **document conflicts**: C4's fix carried lines added later (C5–C7) as context. Resolved at C4 (C4's text + the S6 lines), and at C5 and C6 with a small resolver.
- **The C6 step went wrong:** the C6 fix had been committed on top of C7, so its conflict resolution carried C7's users-list decision line and the superseded re-issue line into C6. Detected by `git diff 8ca33914 HEAD` (the pre-rebase head = the intended text) and by listing each commit's decision lines. Repaired with `git commit-tree`: C6's `space-links.md` = the intended final text minus C7's own changes (from `git diff 2309d548 ea56e225`), C7's = the intended final text; messages and authorship kept; `git reset --hard` to the rebuilt head (tree clean). Final tree vs `8ca33914`: one line of `docs/features/users.md` in another order (the S6 decision before the shared-writes decision), nothing else.
- Per-commit check: two `git rebase -i` runs with an `exec` after C2–C4, then C5–C7 (`npm run build -w @masaha/shared && npm run lint && npm run typecheck`) → each "Successfully rebased", `rebase exit: 0`; SHAs unchanged.

## Commits after the round
`3be1ed68` feat(users): expire temporary passwords (39) · `3a430836` fix(auth): no email recovery while pending (42) ·
`848cd99c` feat(users): correct the email at first sign-in (47) · `50756cf4` feat(space-links): add and list a space's staff (47) ·
`da38d609` feat(space-links): deactivate and reactivate staff (50) · `6851b8ac` feat(space-links): reissue a staff password (43) ·
`cc8a7d5e` feat(space-links): show reception links to admin (48).

## Ran on the head (only what the change touches)
- `test:api` admin owners + admin roles + staff → "Test Files  3 passed (3)", "Tests  86 passed (86)".
- `test:unit -w @masaha/web` copy + auth repository → "Tests  39 passed (39)"; `test:component -w @masaha/web` the three Google files → "Tests  22 passed (22)".
- `format:check` "All matched files use Prettier code style!"; `check:links` "2196 links in 131 documents and 1233 source files all resolve."
- Real run (3321, `masaha_b_dev`): a new pending owner linked to a second space → `409 ACCOUNT_PASSWORD_PENDING`; a registered user given the admin's temporary password → upgrade `409 ACCOUNT_PASSWORD_PENDING`, role `ADMIN` `409 ACCOUNT_PASSWORD_PENDING`; 6/6. Server stopped by its process ids (12212, 27932, 21012); port 3321 free.

## CI after fix round 1
- `gh pr checks 90 --watch` → exit 0. Head `cc8a7d5eac2adbf4571302facd214b7731bb7de6` (= local), `mergeStateStatus: CLEAN`; lint, format:check, typecheck, test:unit, test:component, check:classes, check:links, build, test:api, CodeRabbit: SUCCESS.
- **Still to do, on the supervisor's word that #89 has merged:** rebase on the new `main`; resolve `docs/architecture/findings/README.md` and `docs/features/space-links.md`; `receptionSpaces: []` in #89's `AdminUserRow` literals (`git grep -n "AdminUserRow" origin/main -- apps/web`, and the showcase JSON by eye); renumber 88–91 if #89 took one; typecheck and the touched web tests on the merged tree; push; CI; CLEAN.

## Rebase on `main` after #89 (`60a78063`)
- The owner: #89 merged; `ACCOUNT_PASSWORD_PENDING`'s lines approved as written (the PR's approval marks removed).
- `git rebase -i origin/main` with a `break` after C4. C1–C3 applied cleanly (`users.md` merged by Git: both sides kept, checked by `git diff origin/main HEAD` and `git diff cc8a7d5e HEAD`).
  C4 conflicted in `docs/architecture/findings/README.md` and `docs/features/space-links.md`, as expected:
  - **renumbered** this PR's findings 88–91 → **90–93** (#89 took 88 and 89): `git mv` of the four files, their titles, the index lines and `space-links.md`'s *Open findings* links; `git grep` for the old names or "finding 88–91" → nothing.
  - the index's and *Open findings*' lists: both sides, in number order (82, 83, 84, 87, 88, 89, 90–93).
  - the code map: the API and Shared lines from C4, the Web line from `main` (#89's `AddOwner`).
  C5–C7 applied cleanly. `git diff cc8a7d5e HEAD`: `main`'s files plus the four renamed findings, nothing else.
- C7: `npm run typecheck` on the merged tree → 2 × `TS2741 … 'receptionSpaces' is missing` (`AddOwner.component.test.tsx:41`, `useAddOwnerForm.component.test.tsx:33`); `receptionSpaces: []` added to each, amended into C7 → typecheck exit 0. The showcase's `fixtures.json` read by eye: no users row.
- Commits: `66027b12` feat(users): expire temporary passwords (39) · `bf18beb0` fix(auth): no email recovery while pending (42) · `1d7a5c6b` feat(users): correct the email at first sign-in (47) · `0d09d4e3` feat(space-links): add and list a space's staff (47) · `22610843` feat(space-links): deactivate and reactivate staff (50) · `f7ea9445` feat(space-links): reissue a staff password (43) · `26ea3a1b` feat(space-links): show reception links to admin (48).
- Ran on the head: `npm run build -w @masaha/shared` exit 0; `npm run lint` exit 0; `npm run typecheck` exit 0; `test:component -w @masaha/web` AddOwner, useAddOwnerForm, OwnersList, useOwnersList → "Test Files  4 passed (4)", "Tests  21 passed (21)"; `test:api` staff + adminOwners → "Test Files  2 passed (2)", "Tests  62 passed (62)"; `check:links` "2208 links in 136 documents and 1256 source files all resolve."; `format:check` "All matched files use Prettier code style!".
- Pushed with lease (`cc8a7d5e` → `26ea3a1b`); PR description updated (findings 90–93, the rebase, the approval marks removed).
- Noted, not acted on: #89's finding 88 ("the upgrade confirm shows no front desks") may now be resolvable with `AdminUserRow.receptionSpaces` — the web's to decide.

- CI on `26ea3a1b` (= local): lint, format:check, typecheck, test:unit, test:component, check:classes, check:links, build, test:api, CodeRabbit: SUCCESS; `mergeStateStatus: CLEAN`. (The first `gh pr checks --watch` ended while two lanes were still running; a bounded wait read them once they finished.)

## Status: DONE — ready for review (not merged)

