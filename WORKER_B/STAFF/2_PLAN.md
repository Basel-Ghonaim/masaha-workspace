# STAFF — accounts created by someone else made safe (Part A), and the owner's reception accounts (Part B, step 6)

**Work Item:** STAFF · **Worker:** B · **Planner:** Claude Code, 2026-10-18, from `origin/main` = `5e8c979d`
and PR #87's head `9567da9a` (PACKAGES, read as a diff: `git diff origin/main...9567da9a`)
**Runs:** only after PR #87 (PACKAGES) has merged, from the latest `origin/main`
**Branch:** `feat/space-staff`, cut with `--no-track` from the latest `origin/main`, in `C:\Users\basel\masaha-b`
**Ports / databases:** API 3321 · `masaha_b_dev`, `masaha_b_test` in `masaha-postgres-1`
**Plan:** `D:\masahaWorkspace\WORKER_B\STAFF\2_PLAN.md` · **Reports:** `D:\masahaWorkspace\WORKER_B\STAFF\4_REPORT_PR<n>.md`
(UTF-8, written in parts with an editor) · no screenshots (API only)
**Executor:** any capable coding agent (Claude Code or OpenCode). This plan stands alone: no step depends
on a Claude skill (Appendix B is only a map). The planner ran nothing; where it could not be sure that
something works, the step is **a check the executor makes first, with what to do if it fails** (§12.2).

**Placeholders**, and no others: `#PRNUM` (the PR's number, replaced just before the push, §12.7).

> **Approved by the owner, 2026-10-18 — binding on the executor:**
> - **§13's six decisions, as recommended:** **1** a temporary password expires after **7 days**; **2** **one
>   PR**, seven commits (report `4_REPORT_PR1.md`); **3** the new code's lines — Arabic «انتهت صلاحية كلمة
>   المرور المؤقتة. اطلب واحدة جديدة ممّن أنشأ حسابك.», English "This temporary password has expired. Ask
>   whoever created your account for a new one."; **4** Google sign-in refused while a temporary password is
>   pending (the existing test `google.api.test.ts:94` changes with it, as the plan says); **5** `email`
>   outside the forced change → 422; **6** the staff row's `temporaryPassword: { expiresAt } | null`, and
>   deactivation answers the updated row.
> - **The plan's three extra closures (Google, re-issue across spaces, the re-issue's rate) are approved.**
> - **Runs only after PR #87 has merged.** The plan was written against #87's head `9567da9a`; #87 then had
>   a review fix round, so its merged tree may differ from that head: **re-read every file the plan names
>   that #87 touched** (`app.ts`, the contract, `security.md`, `conventions.md`, the findings index, the
>   shared package's exports) on the merged tree before editing; a contradiction in code → stop and ask.
> - **Finding numbers:** 84–86 are this item's (81 is #87's, 82–83 worker A's).
> - **Amended 2026-10-18 (the executor's stop at §12.2) — the owner's answers:**
>   1. `requireAuth.api.test.ts:81–84` and `handover.api.test.ts:23–32` get an expiry 7 days ahead **in the
>      commit that adds the CHECK** (no behaviour of theirs changes).
>   2. `password.api.test.ts:490` uses a settled account and drops "settles a temporary one" from its title, in
>      C2 — A1 removed that behaviour on purpose; the plan's own A1 tests prove the new one.
>   3. **#88 (worker A's PR 1) has merged**, so `main` now holds `AdminUserRow` literals in `apps/web`
>      (`OwnersList.component.test.tsx`, `useOwnersList.component.test.tsx`, `spaceLinksRepository.unit.test.ts`,
>      `userRowView.unit.test.ts` — `git grep -n "AdminUserRow" origin/main -- apps/web` finds them all). **C7
>      adds `receptionSpaces: []` to every such literal on `main`** — a licence for those test files only, no
>      other web change; `npm run typecheck` proves none is missed. Worker A's PR 2 (open or soon) builds more:
>      **whichever PR merges second adds `receptionSpaces: []` to the literals the other added**; the conflict
>      check says nothing (no text conflict) — run `npm run typecheck` on the merged tree before saying CLEAN.
>   Re-sync first: `origin/main` moved (#88). Re-read §0's files; nothing of #88 is in `apps/api`.

---

## 1. Summary

An account that someone else created — an owner the admin adds, a receptionist an owner adds — starts
with a temporary password typed by that someone, under an email that someone typed. Today three holes
follow from a mistyped email: (b) a reset email works while the temporary password is pending, so the
holder of the mistyped mailbox takes the account; (b′) the same holder does it with Google, when the
mistyped address is a Gmail one (a Google sign-in links Google to the account, removing its password);
(c) a pending temporary password never expires. Part A closes them for every such account, platform-wide:
no email recovery and no Google link while a temporary password is pending; the person confirms or
corrects the email at the forced change; a temporary password expires 7 days after it is issued.

Part B builds the owner's staff on the API (step 6): the owner creates **new** reception accounts only (an
email with an account is refused: ADR 0009 rule 4 is revised), lists them, deactivates and re-activates
them (deactivation ends every session), issues a new temporary password while one is still pending, and
records each handover; the admin's users list gains each person's reception links.

One schema change: `users.temporary_password_expires_at`, with a `CHECK` that ties it to
`must_change_password`. One new error code: `TEMPORARY_PASSWORD_EXPIRED`. No dependency. In `apps/web`,
only that code's two catalogue lines (workflow §9's licence for B; §13 D3).

## 2. The contract

### Scope
- **Part A (`users`, `auth`):**
  - A1 — while a temporary password is pending, the forgotten password sends nothing (request and resend
    answer as for any address), a link bound before it is refused at its check and at the reset, and
    **(S1)** a Google sign-in does not link to the account (`GOOGLE_LINK_NOT_ALLOWED`).
  - A2 — `POST /me/password` takes an optional `email` during the forced change: the person confirms or
    corrects their address; a taken one is `EMAIL_TAKEN`; a correction is audited `user.emailChanged`.
  - A3 — a temporary password expires 7 days after it is issued (`users.temporary_password_expires_at`);
    a password sign-in with an expired one is refused `TEMPORARY_PASSWORD_EXPIRED` (403), only once it
    matches.
  - A4 — the handover question for the owner's staff (a managed route, on the `users` service).
- **Part B (`space-links`):**
  - B1 — `POST /manage/spaces/:spaceId/staff`: a new account, a reception link, the temporary password
    once; an email with an account is refused `EMAIL_HAS_ACCOUNT`; ADR 0009 rule 4 revised.
  - B2 — `GET /manage/spaces/:spaceId/staff`: every reception link of the space, whole, owner only.
  - B3 — `PATCH /manage/spaces/:spaceId/staff/:userId { isActive }`: deactivate (every session ends) and
    re-activate; audited.
  - B4 — `POST …/staff/:userId/temporary-password`: a new one, only while one is pending.
  - A4 — `POST …/staff/:userId/temporary-password/handover { channel }`.
  - B5 — a staff-accounts limit, 10 an hour per owner, counted after `requireCan` and before `validate`.
  - B6 — `AdminUserRow.receptionSpaces` (additive).
- The documents each change triggers (§7, Appendix A); finding 84.

### Acceptance criteria
- [ ] A pending account gets no reset email from `forgot` or `resend`; the answers (status, body, cookie,
      the no-send wait) are those of an address without an account. (T1, T2)
- [ ] A reset link bound before a temporary password became pending is refused at `reset/check`
      (`RESET_TOKEN_INVALID`) and at `reset` (`RECOVERY_INVALID`), and the password is unchanged. (T3, T4)
- [ ] Once the forced change is done, the reset email is sent again — to the corrected address when it
      was corrected. (T5)
- [ ] A Google sign-in whose verified Gmail address is a pending account's is refused
      `GOOGLE_LINK_NOT_ALLOWED`, linking nothing and keeping the password. (T6)
- [ ] Every write that makes a temporary password pending stores its expiry, 7 days after `now()`; every
      write that settles one clears it; the database refuses a pending account without an expiry, and an
      expiry without a pending change. (T7–T9, U1, U2)
- [ ] A password sign-in with an expired temporary password is refused 403 `TEMPORARY_PASSWORD_EXPIRED`;
      a wrong password on such an account is still `INVALID_CREDENTIALS`; one not yet expired signs in.
      (T10, T11)
- [ ] The forced change with `email` corrects the address (audited, `before`/`after`), keeps it when it is
      the same (nothing audited), refuses a taken one with `EMAIL_TAKEN` writing nothing, and `email`
      outside the forced change is refused 422. (T12–T15)
- [ ] Staff: every route refused for a user, an owner of another space, the admin (404), and reception of
      this space (403, before the body is read or counted); the owner of this space succeeds. (T16, T17)
- [ ] The owner creates a new reception account with a temporary password answered once (`no-store`),
      audited; an email that has an account is refused and nothing is written; no existing account is
      ever linked. (T18, T19)
- [ ] The 11th staff-account request of an owner in an hour answers 429, an invalid body counted too.
      (T20)
- [ ] The list answers every reception link of the space, whole, oldest first, inactive ones included,
      each with its pending temporary password's expiry or `null`; no owner link, no last sign-in. (T21)
- [ ] Deactivating ends the person's link and every session, audited; re-activating restores the link;
      the same state writes nothing; an owner's link (a co-owner) is never touched. (T22–T24)
- [ ] The owner issues a new temporary password only while one is pending, and only for an account that
      holds nothing else; the handover is audited only while pending. (T25–T27)
- [ ] `AdminUserRow.receptionSpaces` lists the active reception links of live spaces. (T28)
- [ ] Lint, typecheck, the unit and API lanes, `format:check`, `check:links`, the shared build: green.

### Out of scope
- Every web screen: the forced change's email field, the staff page, the admin's users page (worker A,
  and its USERS item). Only the new code's catalogue lines are written in `apps/web`.
- Reception's permissions at the desk (recorded for steps 7–9 in `_SHARED/OPEN_DECISIONS.md`).
- A person working at two spaces' front desks (finding 84); packages; capacity.
- The admin's upgrade dialog showing whose account it is (worker A's OWNERS PR 2).
- Changing an email outside the forced change (`PATCH /me`, not designed).

## 3. The reading done

From `origin/main` (`5e8c979d`): `CLAUDE.md`; `docs/development/workflow.md`; `docs/development/testing.md`;
`docs/backend/security.md` (whole); `docs/backend/conventions.md` (§4 errors, §6 audit, the module table);
`docs/api/api-contract.md` (§1–§4, *Session*, *The forgotten password*, *Me*, *Managed spaces*, *Owners
(the admin)*, *Users (the admin)*, §6); `docs/architecture/data-model.md` (User, SpaceManager, *Constraints
worth stating*); ADR 0009 (whole); `docs/features/users.md`, `space-links.md` (whole); the findings
index, and findings 17, 21, 23, 49; `docs/README.md` (*Deferred documents*); `docs/plans/v1-mvp.md`
(step 6's lines); `docs/project/overview.md` (the roles and *Built* lines). Code: `auth/auth.service.ts`;
`users/users.service.ts`, `users.repository.ts`, `temporaryPassword.ts`, `users.controller.ts`, its
`me` and `admin` routes, `index.ts`; `space-links/` (`index.ts`, `space-links.service.ts` head,
`space-links.repository.ts`, `space-links.admin.routes.ts`, `admin-owners/adminOwners.service.ts`,
`admin-users/adminUsers.service.ts` and `.mapper.ts`); `shared/auth/can.ts`, `requireCan.ts`;
`spaces/photos.manage.routes.ts`, `spaces.limits.ts`; `app.ts` (the composition and the `manage`
router); `prisma/schema.prisma` (User, SpaceManager); the last two migrations; `test/app.ts`
(`createAccount`, `recordingEmailSender`) and `test/global-setup.ts`; `packages/shared/src/users/requests.ts`,
`space-links/requests.ts`, `core/fields.ts`; the web's two `errors.ts` catalogues (shape only); the uses of
`mustChangePassword: true` across the API tests.
From #87's diff: `app.ts`, the contract (*Packages (managed)*, the §4 exception), `security.md`,
`conventions.md`, the findings index (77–80), `packages.manage.routes.ts`, `packages.service.ts` (the
`lockFor` pattern with `LoadedSpace.linksUnder`), `packages.controller.ts`.
Outside the repository: `D:\masahaWorkspace\DESIGN\DECISIONS\DECISIONS_OWNER.md` (O4, OW-017–019),
`_SHARED\OPEN_DECISIONS.md` (reception's permissions, not built), `WORKER_B\PACKAGES\2_PLAN.md` (§12's
procedure) and `3_EXEC_PROMPT.md` §2 (the stop rule).
`docs/features/auth.md` and ADRs 0013 and 0017 are read by the executor at C2 (§12.3), where their lines
are edited; nothing in them is planned to change but the reset's and Google's lines named in Appendix A.

## 4. The prompt's settled decisions, as they will be built

"Pending" means `users.must_change_password = true` throughout: a temporary password the person has not
yet changed. It is set only with a temporary password, and cleared by every password write and by a
Google link (today's code: `setPassword`, `setPasswordIf`, `linkGoogleIfUnlinked`).

### A1 — no reset by email while a temporary password is pending
- `users` gains one rule, beside `maySignIn`:
  ```ts
  /** Whether the reset email may open the account: one that may sign in, with no temporary password
   *  pending (accounts created by someone else, docs/backend/security.md › Passwords). */
  mayRecoverByEmail(account: Account): boolean   // maySignIn(account) && !account.mustChangePassword
  ```
- `auth.forgotPassword`: `holder = account && users.mayRecoverByEmail(account) ? account : undefined` —
  so a pending account is treated exactly as an unknown or suspended one: the recovery opens with
  `userId` undefined, nothing is sent, `answerAsASend(false)` waits the drawn time. The answer is
  unchanged for every address (no disclosure).
- `auth.resendResetLink`: `if (users.mayRecoverByEmail(account)) delivered = await sendResetLink(…)`.
- **The race** (a link issued while the account was not pending, then a temporary password issued before
  it is used): issuing a temporary password already ends every reset link (`endResetTokens`), but a
  `forgot` that read the account before the issue committed can still insert its link after. So:
  - `checkResetToken`: inside its transaction, after `users.lockAccount(owner, tx)`, return `undefined`
    (→ `RESET_TOKEN_INVALID`) when `!users.mayRecoverByEmail(account)`.
  - `resetPassword`: inside its transaction, `const account = await users.lockAccount(owner, tx)`;
    when `!account || !users.mayRecoverByEmail(account)` → `throw invalidRecovery()` **before**
    `consumeRecoveryLink` (nothing is written; the transaction rolls back).
- Once the person changes the temporary password, `mustChangePassword` is false and every path works again.
- *Recovery meanwhile:* a new temporary password from whoever created it — the admin's existing
  `POST /admin/users/:userId/temporary-password`, or the owner's (B4).

### A2 — the person confirms or corrects their email at the forced change
- **Endpoint:** `POST /me/password`, the forced change itself (the holder of the temporary password is the
  proof). **Body:** `{ currentPassword?, password, email? }` — `email` optional, so today's web keeps
  working unchanged and worker A adds the field later; `emailSchema` (trimmed, lowercased).
  ```ts
  // packages/shared/src/users/requests.ts
  export const changePasswordSchema = z.object({
    currentPassword: z.string().min(1).max(PASSWORD_MAX_LENGTH).optional(),
    password: passwordSchema,
    /** Only in the forced change: the address confirmed, or corrected (A2). */
    email: emailSchema.optional(),
  });
  ```
  (`emailSchema` from `../core/index.ts`; executor check §12.2.6: `users` may import `core`.)
- **Rules** in `users.changePassword`:
  1. `email` present and the change **not** forced → `AppError.validation({ email: ['invalid_choice'] })`,
     before the limiter (as `currentPassword: ['required']` is) — P2.
  2. Forced, and `email` equal to the account's → nothing more than today; no audit.
  3. Forced, and `email` different → in the **same** transaction, after `setPasswordIf` succeeds and
     before `endSessions`: `repository.setEmail(userId, email, tx)`, which returns `'taken'` on the
     `users_email_key` unique violation; `'taken'` → `throw AppError.conflict('EMAIL_TAKEN', 'Email
     taken', { email: ['not_unique'] })` — the transaction rolls back, so the password is **not**
     changed either (all or nothing). Then `audit({ actorId: userId, action: 'user.emailChanged',
     entityType: 'user', entityId: userId, before: { email: old }, after: { email } }, tx)`.
  4. The refusal is thrown inside `limiter.limitFailures(PASSWORD_CHANGE)`, so each `EMAIL_TAKEN` counts
     as a failure of the change (10 / 15 min per user): probing addresses through it is bounded like
     registration. Accepted disclosure: as at registration (security › *Registering an email that has an
     account*).
- **A Postgres note:** a unique violation aborts the transaction; nothing runs after it but the throw.
  `setEmail` must therefore be the last statement before the throw, and the audit after it (§12.2.4).
- **The answer** stays `{ accessToken }`; the web reads the corrected address on its next session read
  (the refresh). Said in the contract for worker A (§13 D5).

### A3 — a temporary password expires 7 days after it is issued
- **A column** (the owner said a migration is acceptable if needed; it is — the issue time is stored
  nowhere): `User.temporaryPasswordExpiresAt DateTime? @map("temporary_password_expires_at")
  @db.Timestamptz(3)`, `null` when none is pending. *Why the expiry, not the issue time:* the rule is one
  comparison at sign-in, the staff list answers it as is, and a later change of the number changes the
  next issues only (P3).
- **The migration** `<timestamp>_temporary_password_expiry`, created once with `--create-only` (§12.3),
  then edited by hand to this (the column line as Prisma writes it):
  ```sql
  -- A temporary password expires 7 days after it is issued (docs/backend/security.md › Passwords).
  -- One pending now has no known issue: it gets 7 days from this migration.
  ALTER TABLE "users" ADD COLUMN "temporary_password_expires_at" TIMESTAMPTZ(3);
  UPDATE "users" SET "temporary_password_expires_at" = now() + interval '7 days'
    WHERE "must_change_password";
  -- A pending temporary password has an expiry, and only a pending one (S4).
  ALTER TABLE "users" ADD CONSTRAINT "users_temporary_password_expiry_check"
    CHECK ("must_change_password" = ("temporary_password_expires_at" IS NOT NULL));
  ```
- **The pure rule**, `apps/api/src/modules/users/temporaryPassword.ts`:
  ```ts
  /** A temporary password lives this long from its issue (A3, the owner's decision 2026-10-18). */
  export const TEMPORARY_PASSWORD_LIFETIME_MS = 7 * 24 * 60 * 60 * 1000;
  /** When a temporary password issued at `issuedAt` expires. */
  export function temporaryPasswordExpiry(issuedAt: Date): Date;
  /** Whether the account's temporary password is pending and has expired at `now` (at the instant: expired). */
  export function temporaryPasswordExpired(
    account: { mustChangePassword: boolean; temporaryPasswordExpiresAt: Date | null }, now: Date,
  ): boolean;   // mustChangePassword && expiresAt !== null && expiresAt.getTime() <= now.getTime()
  ```
- **Writes** (`users.repository.ts`): `ACCOUNT` selects `temporaryPasswordExpiresAt`; `NewAccount` gains
  `temporaryPasswordExpiresAt?: Date`; `setTemporaryPassword(id, hash, expiresAt, tx)`; `setPassword`,
  `setPasswordIf` and `linkGoogleIfUnlinked` also set `temporaryPasswordExpiresAt: null`.
  `users.createWithTemporaryPassword` and the issue (A4/B4's shared `replaceWithTemporaryPassword`, below)
  pass `temporaryPasswordExpiry(now())`. The `now` is the `users` service's existing clock dependency.
- **Sign-in** (`users.verifyCredentials`): after the password matches and `assertMaySignIn`, and again in
  `confirm` under the lock: `if (temporaryPasswordExpired(account, now())) throw
  AppError.forbidden('TEMPORARY_PASSWORD_EXPIRED', 'Temporary password expired')`. Order: unknown or
  wrong → `INVALID_CREDENTIALS`; then `ACCOUNT_SUSPENDED`; then `TEMPORARY_PASSWORD_EXPIRED` — so only a
  holder of the right password learns it expired. The sign-in limiter keeps the slot (a 403 is a
  refusal), as for a suspension.
- **Where it does not apply** (P4): a session opened in time keeps its forced change (the person proved
  the password before it expired; the session lives at most 30 days); a Google sign-in of an account
  already linked to that Google account opens as today (Google proves the person). Refusing the forced
  change after the expiry would trap a Google-and-password account whose admin-issued password expired:
  it could sign in with Google and do nothing else.
- **The code** `TEMPORARY_PASSWORD_EXPIRED` follows conventions §4's four steps (§13 D3).
- **The test helper** `apps/api/test/app.ts › createAccount`: when `mustChangePassword: true` is given
  without `temporaryPasswordExpiresAt`, it sets `new Date(Date.now() + 7 days)`, so every existing test
  that creates a pending account keeps passing under the `CHECK` (the uses: `auth.api.test.ts`,
  `google.api.test.ts`, `password.api.test.ts`, `space-links.api.test.ts`, `users.api.test.ts`).

### A4 — the handover question wherever a temporary password is shown
- `users` keeps one implementation, with the lock and the transaction its caller's:
  ```ts
  /** The account's handover, under its session lock, which the caller took (with `lockAccount`).
   *  Only while its temporary password is pending. `spaceId` names the space for an owner's staff. */
  recordHandoverLocked(actorId: number, account: Account, channel: HandoverChannel, tx: Tx,
                       spaceId?: number): Promise<void>
  ```
  The admin's `recordHandover(actorId, userId, channel)` becomes: its transaction, `lockAccount`, 404,
  then `recordHandoverLocked` (behaviour unchanged). The owner's route (Part B) calls the locked one under
  the space's lock. Audit as today: `user.temporaryPasswordHandedOver`, `after: { channel }`, with
  `spaceId` when given, so the owner's audit log (OW-022, later) finds it.

### B1 — the owner creates new accounts only
- **Route:** `POST /manage/spaces/:spaceId/staff` · 🏢. **Body** (`addStaffSchema`,
  `@masaha/shared/space-links`): `{ name: textSchema(1, NAME_MAX_LENGTH), email: emailSchema }`.
- **201:** `AddedStaff = { userId: number, temporaryPassword: string }`, `Cache-Control: no-store`.
- **One transaction** (`staff.service.add`): `users.issueTemporaryPassword()` before it (bcrypt outside);
  then `lockFor(actor, space, tx)` (the space's lock and `can('staff.manage')` on the links under it, as
  packages' `lockFor`); then `users.createWithTemporaryPassword({ name, email, role: 'USER' }, hash,
  actor.id, tx)`; `null` (the email has an account, now or by a creation meanwhile) →
  `AppError.conflict('EMAIL_HAS_ACCOUNT', 'The email has an account', { email: ['not_unique'] })`; then
  `repository.linkReception(spaceId, userId, tx)` (a create: a new account has no row); then
  `audit({ action: 'space.staffAdded', entityType: 'space', entityId: spaceId, spaceId, after: { userId } })`.
- **No lookup before the insert:** the unique key decides, so no read-then-link path exists to drift into
  linking (P5). An existing account is never linked by an owner, whatever its state.
- **The disclosure:** `EMAIL_HAS_ACCOUNT` tells an owner that an address has an account, as registration
  does (security.md's accepted trade-off); B5's limit bounds it to 10 an hour.
- **ADR 0009** gains a *Revised* line and rule 4's second bullet is replaced (Appendix A.6). A person at
  two spaces' desks: finding 84.

### B2 — the list
- **Route:** `GET /manage/spaces/:spaceId/staff` · 🏢 (owner only: `requireCan('staff.manage')`, so
  reception gets 403; the boundary already gave others 404).
- **200:** `StaffMember[]`, **whole** (a space has few staff; the contract's §4 exceptions list gains it,
  as the packages did): every `RECEPTION` link of the space, active or not, oldest first
  (`createdAt`, then `userId`).
  ```ts
  // @masaha/shared/space-links
  StaffMember = {
    userId: number, name: string, email: string,
    isActive: boolean,                          // false: deactivated (OW-017), re-activated through PATCH
    temporaryPassword: { expiresAt: string } | null   // pending (OW-018's badge); null once changed
  }
  ```
  An expired one is still listed with its past `expiresAt`: the web says it expired, and B4 issues another.
  No last sign-in (OW-018).
- **Composed read** (one query per module): `repository.findReceptionLinksAt(spaceId)` → `{ userId,
  deactivatedAt }[]` in order; `users.staffAccounts(ids)` → `{ id, name, email, mustChangePassword,
  temporaryPasswordExpiresAt }[]` (a new `users` read, without the hash); `toStaffMember` maps.

### B3 — deactivate and re-activate, `PATCH …/staff/:userId`
- **Route:** `PATCH /manage/spaces/:spaceId/staff/:userId` · 🏢, **body** `setStaffActiveSchema =
  { isActive: boolean }`. **200:** the `StaffMember` as it now is.
- **One transaction:** `lockFor`; `users.lockAccount(userId, tx)` (the space's lock, then the person's —
  the order every link change takes); the person's link at the space with `role = RECEPTION`, else 404
  (an unknown person, no link, **an owner's link: a co-owner is never touched here**).
  - Same state as asked → nothing written, no session ended; answers the member.
  - `isActive: false` → `deactivateReceptionLink(spaceId, userId, now(), tx)`; `users.endSessions(userId,
    tx)` (every session: the shared desk device must not stay signed in); audit `space.staffDeactivated`
    (`entityType: 'space'`, `entityId: spaceId`, `spaceId`, `before: { userId, isActive: true }`,
    `after: { userId, isActive: false }`).
  - `isActive: true` → refused for a suspended account (`conflict` `ACCOUNT_SUSPENDED`) and for an admin
    (`conflict` `ACCOUNT_IS_ADMIN`: a deactivated receptionist may have been made admin since, P6);
    else `reactivateReceptionLink`; audit `space.staffReactivated` (the mirror). No session ends.

### B4 — a new temporary password, only while one is pending
- **Route:** `POST /manage/spaces/:spaceId/staff/:userId/temporary-password` · 🏢. **200:**
  `IssuedTemporaryPassword` (`@masaha/shared/users`), `Cache-Control: no-store`.
- **One transaction**, the password hashed before it: `lockFor`; `users.lockAccount`; refusals in this
  order: 404 without an **active** reception link of the person at the space; `conflict`
  `TEMPORARY_PASSWORD_NOT_PENDING` once the person has changed it (the account is theirs; recovery is the
  email or the admin); `conflict` `ACCOUNT_SUSPENDED`; `conflict` `ACCOUNT_HAS_LINKS` when the account is
  not a `USER` or holds any other active link (S5). Then `users.replaceWithTemporaryPassword(actor.id,
  userId, hash, tx, spaceId)` — the admin's issue's writes, extracted: `setTemporaryPassword` (with the
  new expiry), `endSessions`, `endResetTokens`, audit `user.temporaryPasswordIssued` (`after:
  { mustChangePassword: true }`, `spaceId` here). The admin's `issueTemporaryPasswordFor` calls the same
  function (behaviour unchanged).
- It also resolves, for staff, what finding 49 resolved for owners: a lost answer to B1 is recovered by B4.

### A4 (Part B's route) — the owner's handover
- **Route:** `POST /manage/spaces/:spaceId/staff/:userId/temporary-password/handover` · 🏢, body
  `handoverSchema` (`@masaha/shared/users`). **204.**
- **One transaction:** `lockFor`; `users.lockAccount`; 404 without an active reception link at the space;
  `users.recordHandoverLocked(actor.id, account, channel, tx, spaceId)`, which answers
  `TEMPORARY_PASSWORD_NOT_PENDING` once nothing is pending.

### B5 — the limit, and the routes' order
- `apps/api/src/modules/space-links/space-links.limits.ts`:
  ```ts
  /** Staff accounts an owner creates or re-issues, counted before the body is read: each costs a
   *  bcrypt hash, and a creation an account row (docs/backend/security.md › Rate limits). */
  export const STAFF_ACCOUNT: RateLimitPolicy = { name: 'staff-account', limit: 10, windowMs: ONE_HOUR };
  ```
  (`ONE_HOUR`: executor check §12.2.5.) It counts the creation (B5) and the re-issue (S3), by the owner.
- `apps/api/src/modules/space-links/space-links.manage.routes.ts`, mounted at `manage.use('/staff', …)`:
  ```ts
  const mayManage = requireCan('staff.manage');
  const counted = limitRequests(limiter, (req) =>
    Promise.resolve({ policy: STAFF_ACCOUNT, by: [String(signedIn(req).userId)] }));
  router.get('/', mayManage, staff.list);
  router.post('/', mayManage, counted, validate(addStaffSchema), staff.add);
  router.patch('/:userId', mayManage, validate(setStaffActiveSchema), staff.setActive);
  router.post('/:userId/temporary-password', mayManage, counted, staff.issueTemporaryPassword);
  router.post('/:userId/temporary-password/handover', mayManage, validate(handoverSchema), staff.recordHandover);
  ```

### B6 — DI-24's API half
- `AdminUserRow` gains `receptionSpaces: { id: number, nameEn: string, nameAr: string | null }[]` — its
  active `RECEPTION` links, oldest first, none to a soft-deleted space: the same shape as `spaces`.
  Additive: no web code builds an `AdminUserRow` today (checked: `git grep AdminUserRow origin/main --
  apps/web` finds nothing; §12.2.7 checks again).
- `space-links.repository.ts`: `findOwnerLinksOf` becomes `findActiveLinksOf(userIds, tx?)` returning
  `{ spaceId, userId, role }` (both roles, same order); `adminUsers.service` reads the summaries of both
  sets in one `spaces.summariesFor` call and splits by role; `toAdminUserRow(account, owned, reception)`.

### B7 — unchanged
Reception keeps reading the owners' names on `GET /manage/spaces/:spaceId` (#86's D5); the staff list is
the owner's alone. No code changes; the existing test stays green.

### The plan's own decisions (inside the agreed item)
- **P1 — module placement:** the staff live in `space-links` (the `space_managers` table, step 6's module
  per conventions' table), in `apps/api/src/modules/space-links/staff/` (service, controller, mapper,
  API test), as `admin-owners/` is; the routes in `space-links.manage.routes.ts`. Every account write is
  a `users` function (ADR 0013).
- **P2 — `email` outside the forced change is refused**, not ignored: a silent drop would let a client
  believe an address changed. 422 `invalid_choice` (no new code; the field is not a choice there).
- **P3 — the expiry stored, not the issue time** (A3's reason).
- **P4 — the expiry applies at the password sign-in only** (A3's reason).
- **P5 — B1 inserts without a lookup;** the unique key refuses an existing email.
- **P6 — re-activation refuses an admin and a suspended account,** as linking an owner does.
- **P7 — the deactivation's answer is the member** (200), so the web updates the row without a re-read;
  the admin's `suspended` route answers 204, but it has no row shape of its own here.
- **P8 — audit actions:** `user.emailChanged`, `space.staffAdded`, `space.staffDeactivated`,
  `space.staffReactivated` (the `space.owner*` naming); `user.created`, `user.temporaryPasswordIssued`
  and `user.temporaryPasswordHandedOver` reused, with `spaceId` when an owner acts.

### The code, file by file (interfaces; the commit in brackets)
- `apps/api/prisma/schema.prisma` — `User.temporaryPasswordExpiresAt`, with a `///` line. [C1]
- `apps/api/prisma/migrations/<ts>_temporary_password_expiry/migration.sql` — above. [C1]
- `apps/api/src/modules/users/temporaryPassword.ts` (+ `.unit.test.ts`) — the lifetime, `temporaryPasswordExpiry`, `temporaryPasswordExpired`. [C1]
- `apps/api/src/modules/users/users.repository.ts` — `ACCOUNT` + expiry; `NewAccount.temporaryPasswordExpiresAt`; `setTemporaryPassword(id, hash, expiresAt, tx)`; the three clears [C1]; `setEmail(id, email, tx): Promise<'set' | 'taken'>` (`takenKey`) [C3]; `findStaffAccounts(ids, tx?)` [C4].
- `apps/api/src/modules/users/users.service.ts` — the expiry at issue and at sign-in [C1]; `mayRecoverByEmail`, the Google refusal in `accountForGoogle` and `linkGoogle` [C2]; `email` in `changePassword` [C3]; `staffAccounts` [C4]; `replaceWithTemporaryPassword`, `recordHandoverLocked` [C6].
- `apps/api/src/modules/users/index.ts` — exports as needed (`type StaffAccount`). [C4]
- `apps/api/src/modules/auth/auth.service.ts` — A1's four places. [C2]
- `packages/shared/src/core/errors.ts` — `TEMPORARY_PASSWORD_EXPIRED`. [C1]
- `apps/web/src/shared/copy/arabic/errors.ts`, `english/errors.ts` — its two lines (§13 D3). [C1]
- `packages/shared/src/users/requests.ts` — `email` in `changePasswordSchema`. [C3]
- `packages/shared/src/space-links/requests.ts` — `addStaffSchema`, `setStaffActiveSchema` (+ types). [C4, C5]
- `packages/shared/src/space-links/responses.ts` — `AddedStaff`, `StaffMember` [C4]; `AdminUserRow.receptionSpaces` [C7].
- `packages/shared/src/space-links/index.ts` — the exports (check whether it re-exports `*`). [C4]
- `apps/api/src/modules/space-links/space-links.repository.ts` — `linkReception`, `findReceptionLinksAt` [C4]; `findReceptionLink(spaceId, userId, tx)`, `deactivateReceptionLink`, `reactivateReceptionLink`, `countOtherActiveLinks(userId, spaceId, tx)` [C5, C6]; `findActiveLinksOf` [C7].
- `apps/api/src/modules/space-links/staff/staff.service.ts` — `createStaffService({ runInTransaction, audit, spaces, users, now })`: `list(spaceId)`, `add(actor, space, request)`, `setActive(actor, space, userId, isActive)` [C4, C5]; `issueTemporaryPassword(actor, space, userId)`, `recordHandover(actor, space, userId, channel)` [C6].
- `apps/api/src/modules/space-links/staff/staff.controller.ts`, `staff.mapper.ts` (`toStaffMember`). [C4…C6]
- `apps/api/src/modules/space-links/space-links.manage.routes.ts` — `createStaffManageRouter({ staff, limiter })`. [C4…C6]
- `apps/api/src/modules/space-links/space-links.limits.ts` — `STAFF_ACCOUNT`. [C4]
- `apps/api/src/modules/space-links/index.ts` — the staff exports. [C4]
- `apps/api/src/modules/space-links/admin-users/adminUsers.service.ts`, `adminUsers.mapper.ts`. [C7]
- `apps/api/src/app.ts` — `const staff = createStaffService({ runInTransaction, audit: writeAudit, spaces, users, now: clock })`; `manage.use('/staff', createStaffManageRouter({ staff: createStaffController(staff), limiter }))`, after #87's packages line. [C4]
- `apps/api/test/app.ts` — `createAccount`'s default expiry. [C1]

## 5. Stronger decisions

### S1 — no Google link while a temporary password is pending — **recommended, planned**
*What:* `users.accountForGoogle`: when the email's account has `mustChangePassword` (and no Google
account linked), throw `GOOGLE_LINK_NOT_ALLOWED`, before the authority check; `users.linkGoogle`
re-checks it under the lock (a temporary password issued meanwhile) and throws the same. *Why:* the same
hole as A1 by another door — a mistyped `@gmail.com` address's holder signs in with Google, and the link
removes the password and the pending change: the account is theirs. *Cost:* two checks and one test; a
pending person whose address really is theirs signs in with the temporary password first, then Google
links later. Uses an existing code (its copy already says "sign in with the password").

### S2 — the reset refused at its check and its success, not only at the request — **recommended, planned**
*What:* A1's race guard (above). *Why:* a link inserted after a temporary password was issued would
otherwise still reset it. *Cost:* two lines under locks already taken; one test (T3/T4).

### S3 — the owner's re-issue counts under the same limit — **recommended, planned**
*What:* `STAFF_ACCOUNT` counts B4 too. *Why:* each re-issue costs a bcrypt hash and ends a person's
sessions; B5 bounded only the creation. *Cost:* none in practice (10 an hour).

### S4 — a `CHECK` ties the expiry to the pending change — **recommended, planned**
*What:* the migration's constraint. *Why:* every write that sets or settles a pending change must also set
or clear the expiry; the database refuses one that forgets (an account pending forever was hole (c)).
*Cost:* the test helper's default; one schema test.

### S5 — the owner's re-issue refused for an account that holds anything else — **recommended, planned**
*What:* B4 refuses an account that is not a `USER`, or holds an active link other than this reception link
(`ACCOUNT_HAS_LINKS`). *Why:* a receptionist still pending could be upgraded by the admin to an owner
elsewhere (`upgradeExisting` keeps the pending change); without this, the first space's owner could issue
a password to another space's owner and take the account. *Cost:* one count under the lock; one test.

### Rules the item touches, stated
- **ADR 0009 rule 4, second bullet** ("an email that already has an account links that account") —
  replaced by the owner's B1; a *Revised* line (Appendix A.6).
- **security.md › Passwords** ("a reception account the owner creates for a new email. An email that
  already has an account is linked instead") and **› Password reset** ("settles a pending temporary one")
  — rewritten (Appendix A.2).
- **The design's OW-019** ("both outcomes said first") — now one outcome; the web item reads the
  contract. Not a repository file; said in the PR and the report.
- **`docs/features/users.md`** "the temporary passwords of the owner's reception accounts are not
  built" — now built.

## 6. Related findings

- **49** (resolved) — *a lost answer to adding an owner loses its temporary password*: B4 gives staff the
  same way out; no edit to 49 (its resolution stands); the staff decision cites it.
- **17** — *expired counters and abandoned sessions are never swept*: not folded; the new column adds
  nothing to sweep (a pending row is the account itself). Cost of folding: a scheduler, out of scope.
- **21** — *a token replayed within the grace window*: not folded; deactivation ends every session,
  branches included (`endSessions` deletes every refresh token and raises the version).
- **23** — *no per-address ceiling for signed-in requests*: not folded; B5 is per owner, as the photos'.
- **New, 84** — *a person cannot work at two spaces' front desks* (B1): Open; resolves when an in-person
  code (or another proof the person gives) lets a second owner link an existing account.
- **85, 86** — not needed. The reset-while-pending hole and the never-expiring password are **not**
  recorded as findings: workflow §4 and §8 record a finding for a problem that is *not* fixed in the item
  (unrelated work, an observation); a problem the item itself fixes by the owner's decision is carried by
  that decision and by `security.md`, and the PR names it. (The planner did not read
  `docs/architecture/documentation.md` in full; the executor checks its findings section at C4 and, if it
  asks a resolved problem to be recorded, records 85 and 86 as *Resolved* and says so.)

## 7. The files it edits

About **50 files**, one PR (§13 D2):

| Area | Files |
|---|---|
| Schema | `apps/api/prisma/schema.prisma`; `apps/api/prisma/migrations/<ts>_temporary_password_expiry/migration.sql` (new) |
| `users` | `temporaryPassword.ts`, `temporaryPassword.unit.test.ts`, `users.repository.ts`, `users.service.ts`, `index.ts` |
| `auth` | `auth.service.ts` |
| `space-links` | `space-links.repository.ts`, `index.ts`, `space-links.manage.routes.ts` (new), `space-links.limits.ts` (new), `staff/staff.service.ts`, `staff/staff.controller.ts`, `staff/staff.mapper.ts`, `staff/staff.api.test.ts` (new ×4), `admin-users/adminUsers.service.ts`, `admin-users/adminUsers.mapper.ts`, `admin-users/adminUsers.api.test.ts` |
| Root | `apps/api/src/app.ts` (shared with #87, merged first) |
| API tests | `auth/auth.api.test.ts`, `auth/password.api.test.ts`, `auth/google.api.test.ts`, `users/users.api.test.ts`, `users/issueTemporaryPassword.api.test.ts`, `db/schema.api.test.ts`, `test/app.ts` |
| Shared | `core/errors.ts`, `users/requests.ts`, `space-links/requests.ts`, `space-links/responses.ts`, `space-links/index.ts` |
| Web (licence) | `apps/web/src/shared/copy/arabic/errors.ts`, `english/errors.ts` — one line each |
| Docs | `docs/api/api-contract.md`, `docs/backend/security.md`, `docs/backend/conventions.md`, `docs/architecture/data-model.md`, `docs/architecture/decisions/0009-space-scoped-reception-role.md`, `docs/features/users.md`, `docs/features/auth.md`, `docs/features/space-links.md`, `docs/architecture/findings/84-….md` (new), `docs/architecture/findings/README.md`, `docs/project/overview.md`, `docs/plans/v1-mvp.md` |

- **Worker A's OWNERS (web, in parallel):** no code file is shared. The catalogue lines are append-only
  lines (workflow §9 item 3); the contract is B's. `POST /admin/owners` is **not changed**: its new
  account gets an expiry (invisible in the contract's shape), its email may be corrected at the first
  change, and its reset waits for the change — all behaviour, no field or code of that endpoint. Said in
  the contract's *Owners (the admin)* by one link to security.
- **#87:** this item runs after it; `app.ts`, the contract, `security.md`, `conventions.md` and the
  findings index are edited on the merged tree (§12.1).

## 8. Design issues

None: no screen is built. For the web items (said in the report, not built): OW-019's "both outcomes"
becomes one outcome — the add-staff sheet shows `EMAIL_HAS_ACCOUNT` on the email field; OW-018's badge
reads `temporaryPassword !== null`, and an expired one needs its own words and B4's action.

## 9. Tests — lane, title, the break each catches

Each test is seen failing first (testing §3 rule 5): written before its code, run red, the red line
copied into the report. A test marked ∅ passes before its code (it guards existing behaviour); its break
(§12.5) is its proof. Commands: `npm run test:unit -w @masaha/api -- <file>`,
`npm run test:api -w @masaha/api -- <file>`.

### Unit — `apps/api/src/modules/users/temporaryPassword.unit.test.ts` [C1]
- **U1** "expires a temporary password exactly 7 days after its issue" — `temporaryPasswordExpiry(new
  Date('2026-10-18T10:00:00.000Z'))` equals `2026-10-25T10:00:00.000Z` (written by hand). *Break:* 8 days.
- **U2** "counts a pending temporary password as expired from its expiry's instant, and never one not
  pending" — at `expiresAt − 1 ms` false, at `expiresAt` true, after true; `mustChangePassword: false`
  with any date false. *Break:* `<` for `<=` (B2).

### API — `apps/api/src/modules/auth/password.api.test.ts` [C2]
- **T1** "sends no reset email to an account whose temporary password is pending, and answers as for an
  unknown address" — a pending account; `POST /auth/password/forgot` → 202, the same body shape and
  cookie as for `nobody@example.com` (both asserted), `recordingEmailSender().sent` empty. *Break B3:*
  `mayRecoverByEmail` returns `maySignIn(account)` alone → one email sent.
- **T2** "the resend sends nothing for a pending account" — forgot then resend (past the 60 s window:
  executor check §12.2.3 on how the existing resend tests pass the window) → 202, nothing sent. *Break B4:*
  the resend's check reverted to `maySignIn`.
- **T3** "refuses a reset link at its check once the account's temporary password is pending" — a
  non-pending account asks a link (one email, its token read from it); then the account is made pending
  **directly in the test database** (`must_change_password = true`, an expiry) **without** ending its
  links (the race); `reset/check` → 400 `RESET_TOKEN_INVALID`. *Break B5:* the check's guard removed → 200.
- **T4** "refuses the reset itself, keeping the password, when the account became pending after the link
  was checked" — check first (200), then make pending as T3, then `reset` → 400 `RECOVERY_INVALID`; the
  hash unchanged, `must_change_password` still true. *Break B6:* the reset's guard removed → 204 and the
  password replaced.
- **T5** "once the temporary password is changed, the reset email is sent again — to the corrected
  address" [C3] — pending account; forced change with `email: 'new@example.com'`; forgot for
  `new@example.com` → one email to it; forgot for the old address → none. ∅ for the first half after C2;
  red until C3 for the address.

### API — `apps/api/src/modules/auth/google.api.test.ts` [C2]
- **T6** "refuses to link Google to an account whose temporary password is pending, linking nothing" — a
  pending `@gmail.com` account; the test's Google port (existing pattern in this file) verifies that
  address → 409 `GOOGLE_LINK_NOT_ALLOWED`; `google_subject` null, `password_hash` unchanged, no session.
  *Break B7:* the pending check removed from `accountForGoogle` → 200 `linked: true`.
  **Existing test to re-read:** `google.api.test.ts:94` creates a pending account and links it; under S1
  it now expects the refusal — the executor rewrites that test's expectation (it asserted the hole) and
  says so in the report. If the test proves something else that S1 breaks, stop and ask.

### API — `apps/api/src/db/schema.api.test.ts` [C1]
- **T7** "the database refuses a pending temporary password without an expiry, and an expiry without
  one" — `prisma.user.create` with `mustChangePassword: true` and no expiry → rejected (constraint name
  in the error); `update` of a settled account setting an expiry alone → rejected. *Break B8:* the
  constraint dropped from `masaha_b_test` (§12.5) → both succeed.

### API — `apps/api/src/modules/users/issueTemporaryPassword.api.test.ts` [C1]
- **T8** "a temporary password the admin issues expires 7 days after it, and replaces the pending one's
  expiry" — before/after timestamps around the call; stored expiry within `[before + 7 d, after + 7 d]`;
  a second issue moves it. *Break B9:* `setTemporaryPassword` keeps the old expiry (passes the first
  issue's).
- **T9** "the forced change clears the expiry" [C1] — after `/me/password`, `temporary_password_expires_at`
  is null (the `CHECK` would refuse otherwise; this names it). ∅ once C1's clears exist; break: remove the
  clear from `setPasswordIf` → the change answers 500 (recorded).

### API — `apps/api/src/modules/auth/auth.api.test.ts` [C1]
- **T10** "refuses a sign-in with an expired temporary password with TEMPORARY_PASSWORD_EXPIRED, only
  once it matches" — a pending account with `temporaryPasswordExpiresAt` 1 s in the past: the right
  password → 403 `TEMPORARY_PASSWORD_EXPIRED`, no refresh cookie; a wrong one → 401
  `INVALID_CREDENTIALS`. *Break B10:* the expiry check removed → 200.
- **T11** "a temporary password still signs in until it expires" — expiry 1 min ahead → 200 with
  `mustChangePassword: true`. ∅ (guards U2's direction at the endpoint).

### API — `apps/api/src/modules/users/users.api.test.ts` [C3]
- **T12** "the forced change corrects the email, audited with the old and the new address" — 200; the
  account's email is the new one; one `user.emailChanged` entry with `before: { email: old }`,
  `after: { email: new }`, actor the user. *Break:* `setEmail` not called → old email (red before C3).
- **T13** "the forced change refuses an email another account holds, changing nothing" — two accounts;
  → 409 `EMAIL_TAKEN`, `errors.email = ['not_unique']`; the password hash and `must_change_password`
  unchanged; no audit entry. *Break B11:* `setEmail` moved to its own transaction after the change → the
  password changed while the email was refused.
- **T14** "refuses an email outside the forced change" — a normal account, `currentPassword` right,
  `email` given → 422 `errors.email = ['invalid_choice']`, nothing changed. *Break B12:* the forced check
  removed → the email changes with the current password alone.
- **T15** "the same email confirms it: nothing audited" — `email` equal (case-insensitively, via the
  schema) → 200, no `user.emailChanged`. *Break:* audit written whenever `email` is present.

### API — `apps/api/src/modules/space-links/staff/staff.api.test.ts` [C4–C6]
Fixtures (the existing helpers: `test/spaces.ts`, `test/admin.ts`, `createAccount`, links inserted with
`prisma.spaceManager.create`): space S with owner O and reception R; space S2 with owner O2; a user U;
the admin A.
- **T16** "every staff route answers 404 to a user, another space's owner and the admin" — the five
  routes × U, O2, A → 404 (the boundary). ∅ (the boundary exists); *break B13:* the staff router mounted
  outside `/manage/spaces/:spaceId` (on `loadSpaceLinks` as #87's B3 did) → not 404.
- **T17** "reception is refused every staff route with 403, before the body is read or counted" — R posts
  an invalid body to `POST /staff` → 403 (not 422), and no `rate_limits` row for `staff-account` and R's
  id exists (the photos test's pattern); same for GET, PATCH, the issue and the handover. *Break B14:*
  `mayManage` removed from `POST /` → 422; *Break B15:* `counted` before `mayManage` → a row exists.
- **T18** "the owner creates a new reception account with a temporary password answered once" — 201,
  `Cache-Control: no-store`, `userId`, a 12-character password; the account is `USER`, pending, with an
  expiry; R's link `RECEPTION`, active; audit `user.created` and `space.staffAdded` (`after: { userId }`,
  `spaceId`); the password signs in (200, `mustChangePassword: true`).
- **T19** "refuses an email that has an account, linking nothing" — U's email → 409 `EMAIL_HAS_ACCOUNT`,
  `errors.email = ['not_unique']`; no `space_managers` row for U; no audit entry; U's password and
  sessions untouched. *Break B16:* on `null`, link the existing account instead (read it by email and
  `linkReception`) → 201 and U linked. **The security property of B1.**
- **T20** "the 11th staff-account request of an owner in an hour answers 429, an invalid body counted
  too" — 10 POSTs with an invalid body (422 each, nothing created), the 11th → 429 with `Retry-After`.
  *Break B17:* `counted` after `validate` → the 11th answers 422.
- **T21** "the list answers every reception link, whole and oldest first, with each pending password's
  expiry" — R (pending), R2 (changed), R3 (deactivated); O's own link absent; `[R, R2, R3]` in creation
  order; `isActive` true/true/false; `temporaryPassword` `{ expiresAt }` / null / per its state; no `meta`;
  no other key (the exact objects written by hand). *Break B18:* `findReceptionLinksAt` filters
  `deactivatedAt: null` → R3 missing.
- **T22** "deactivating ends the person's link and every session" [C5] — R signs in (access token and
  refresh cookie); O `PATCH { isActive: false }` → 200 `isActive: false`; R's access token on
  `GET /manage/spaces/S` → 401; R's refresh → 401; audit `space.staffDeactivated`. *Break B19:*
  `endSessions` removed → the old token answers 404 (the link check), the refresh 200: the refresh line
  fails. **The security property of B3.**
- **T23** "re-activating restores the link, ends nothing, and the same state writes nothing" [C5] — after
  T22's state: `{ isActive: true }` → 200, R signs in and reads S; a second `{ isActive: true }` → 200 and
  no second audit entry; a suspended R → 409 `ACCOUNT_SUSPENDED`. *Break:* the same-state return removed
  → two entries.
- **T24** "an owner cannot deactivate a co-owner, or anyone without a reception link here" [C5] — S gets a
  second owner O3; O `PATCH /staff/O3 { isActive: false }` → 404, O3's link active; U → 404; R2 of S2 →
  404. *Break B20:* the link read without `role: 'RECEPTION'` → O3 deactivated.
- **T25** "the owner issues a new temporary password only while one is pending" [C6] — pending R → 200
  `no-store`, the old password → 401 `INVALID_CREDENTIALS`, the new one signs in; expiry moved; audit
  `user.temporaryPasswordIssued` with `spaceId`; after R changes it → 409
  `TEMPORARY_PASSWORD_NOT_PENDING`. *Break B21:* the pending check removed → 200 on a signed-in account.
  **B4's security property.**
- **T26** "refuses a re-issue for an account that holds anything else" [C6] — pending R also linked as
  `OWNER` of S2 (inserted, role set to `OWNER`) → 409 `ACCOUNT_HAS_LINKS`, its password unchanged.
  *Break B22:* the S5 check removed → 200. **S5's property.**
- **T27** "records the owner's handover only for its own pending staff" [C6] — R pending → 204, audit
  `user.temporaryPasswordHandedOver` with `after: { channel: 'IN_PERSON' }`, `spaceId`; R after the change
  → 409 `TEMPORARY_PASSWORD_NOT_PENDING`; S2's reception → 404; `channel: 'SMS'` → 422. *Break B23:* the
  link check removed → S2's reception's handover 204.

### API — `apps/api/src/modules/space-links/admin-users/adminUsers.api.test.ts` [C7]
- **T28** "each row lists the person's active reception links, beside the spaces they own" — R active at
  S, deactivated at S2 (a second row), at a soft-deleted S3 → `receptionSpaces: [S]`, `spaces: []`; an
  owner's row `receptionSpaces: []`. *Break B24:* `findActiveLinksOf` without `deactivatedAt: null` → S2
  listed.

### Not tested, and said
- The concurrent creation of one email by two owners (one 201, one 409) — the unique key decides; Review
  Focus.
- The expiry re-checked in `confirm` under the lock (an issue between bcrypt and the lock) — Review Focus.
- B7 — the existing `GET /manage/spaces/:spaceId` reception test stays green; no new test.

## 10. Review Focus — the inputs no planned test exercises

- Two owners (or the admin and an owner) creating the same email at once: `createWithTemporaryPassword`
  returns `null` for the loser inside its own transaction; check no link or audit survives.
- A temporary password issued between `verifyCredentials`' bcrypt and its `confirm`: `confirm` re-reads
  the account under the lock and applies the expiry to the new one (a fresh issue is not expired).
- `forgot` racing a temporary password's issue (S2): the guard at check and reset is the proof; the
  link may still be emailed — acceptable, it opens nothing.
- `setEmail` racing a registration of the same address: the unique key; the change rolls back whole.
- Deactivation while the person refreshes: the session lock orders them; a refresh that won still dies at
  its next request (the version).
- A deactivated receptionist re-activated after the admin upgraded them to owner of S: the link row's
  role is then `OWNER`, so the staff PATCH answers 404 (the link read by role).
- The `email` field's case: `emailSchema` lowercases before the comparison.

## 11. The commits

Subjects counted (≤ 50):

| # | Subject | Chars | Holds |
|---|---|---|---|
| C1 | `feat(users): expire temporary passwords` | 39 | A3: schema, migration, `temporaryPassword.ts` + U1–U2, repository/service expiry, the code + catalogues, `test/app.ts`, T7–T11; docs A.1–A.4 (expiry parts) |
| C2 | `fix(auth): no email recovery while pending` | 42 | A1 + S1 + S2: `mayRecoverByEmail`, `auth.service.ts`, Google refusal; T1–T4, T6; docs (reset, Google) |
| C3 | `feat(users): correct the email at first sign-in` | 47 | A2: the schema field, `setEmail`, `changePassword`; T5, T12–T15; docs |
| C4 | `feat(space-links): add and list a space's staff` | 47 | B1, B2, B5: shared shapes, repository, `staff/`, routes, limits, `app.ts`; T16–T21; ADR 0009 revised, finding 84, docs |
| C5 | `feat(space-links): deactivate and reactivate staff` | 50 | B3: T22–T24; docs |
| C6 | `feat(space-links): reissue a staff password` | 43 | B4 + A4: `replaceWithTemporaryPassword`, `recordHandoverLocked`, two routes; T25–T27; docs |
| C7 | `feat(space-links): show reception links to admin` | 48 | B6: T28; docs |

Each commit: its code, its tests and its documents together; lint and typecheck green on each. Every new
decision and history line in a document ends with `2026-10-18, #PRNUM` (or the day it is written).
The PR's title: `feat(space-links): add the owner's staff` (40).

## 12. Verification and the procedure

### 12.1 Before the branch
```powershell
Set-Location C:\Users\basel\masaha-b
git fetch origin
git status --short --branch          # clean, detached (or on the merged feat/space-packages: then `git switch --detach origin/main`)
gh pr view 87 --json state,mergedAt  # MERGED; if not, stop: this item runs after #87
git log --oneline -5 origin/main
gh pr list --state open --json number,title,headRefName,headRefOid
git diff --name-status 5e8c979d origin/main
```
#87's files will be listed — expected. **Any other change** to a code file of §7, to `shared/auth/*`,
`shared/rate-limit/*`, `sessions/*`, `apps/api/test/*`, `schema.prisma` or `packages/shared/src/{core,users,space-links}/*`
— re-read it; **if it contradicts this plan, stop and ask.** An open PR that edits a code file of §7
(worker A's OWNERS must not): stop and ask. The shared documents: re-read on the merged tree before
editing. Then:
```powershell
git switch --no-track -c feat/space-staff origin/main
docker start masaha-postgres-1       # never npm run db:up; never npm ci
npm run build -w @masaha/shared      # the shared dist holds #87's packages before any API run
```
`apps/api/.env` must point at `masaha_b_dev` / `masaha_b_test` and `PORT=3321` (check the names; never
print the file). After #87's merge, `masaha_b_dev` needs no migration from it (it has none).

**One full test run at a time on this machine.** Before each full lane:
```powershell
Get-CimInstance Win32_Process -Filter "Name = 'node.exe'" |
  Where-Object { $_.CommandLine -match 'vitest' } | Select-Object ProcessId, CommandLine
```
A line under `C:\Users\basel\masaha\` (not `masaha-b`): wait for it to end.

### 12.2 First checks (each when its code exists)
1. **The migration, created once:**
   ```powershell
   npm exec -w @masaha/api -- prisma migrate dev --create-only --name temporary_password_expiry
   Get-ChildItem apps/api/prisma/migrations | Select-Object -Last 2
   ```
   Run it **once**, then list the folder (a second `--create-only` applies the migration to the dev
   database). Replace the generated SQL with §4 A3's (keep Prisma's column line if it differs only in
   quoting). *If Prisma refuses for data loss:* it will not here (a nullable column); if it does, use
   `prisma migrate diff --from-migrations … --to-schema-datamodel … --script` into the folder and say so.
   Then `npm run db:migrate` (applies it to `masaha_b_dev`); `masaha_b_test` is migrated by the API lane's
   global setup. `npx prisma generate` if the client is not regenerated by the migrate (check
   `apps/api/src/generated/prisma/models/User.ts` names `temporaryPasswordExpiresAt`).
2. **The `CHECK` and the helper:** after C1's migration, run `auth.api.test.ts` alone; a failure naming
   `users_temporary_password_expiry_check` from `createAccount` means the helper's default is missing.
3. **The resend window in tests** (T2): read how the existing resend tests in `password.api.test.ts`
   pass the 60 s window (an injected clock, or a database update of the recovery); use the same. None:
   stop and ask.
4. **The unique violation inside the change** (T13): if T13 answers 500, log the error's `code` and
   `meta` once (removed before the commit). `P2002` naming `users_email_key`: map it in `setEmail` with
   the repository's `takenKey`. Anything else: stop and ask.
5. **`ONE_HOUR`:** `shared/rate-limit` exports `FIFTEEN_MINUTES`; the register limit counts per hour —
   reuse its constant (`git grep -n "60 \* 60" apps/api/src/shared/rate-limit apps/api/src/modules/auth`).
   None exported: define `ONE_HOUR` in `space-links.limits.ts` locally, as the auth limits do.
6. **Imports:** `packages/shared/src/users/requests.ts` importing `emailSchema` from `../core/index.ts`
   passes lint (shared's own levels). If refused, stop and ask.
7. **`AdminUserRow` in the web:** `git grep -n "AdminUserRow" apps/web` finds nothing. If it finds a
   fixture, add `receptionSpaces: []` to it under B's licence (what breaks when a shared type changes)
   and say so.
8. **`LoadedSpace.linksUnder`:** present after #87 (`shared/auth/spaceLinks.ts`). If not, stop and ask.

### 12.3 Implement, commit by commit
Stage **by path** (`git add <path> …`; never `-A` or `.`); `git status` before each commit; after each
commit `npm run lint` and `npm run typecheck`. Inside each commit: the test first, run red (its output to
the report), then the code, then green, then its documents (Appendix A, tagged by commit). At C2, read
`docs/features/auth.md` (its reset and Google lines) and ADR 0013/0017 before editing the first. The
error code at C1 follows conventions §4 in its order: `packages/shared/src/core/errors.ts`, both
catalogues, the contract's §6 line, T10.

**A fix before the push** folds into its commit:
```powershell
git commit --fixup=<sha> -- <paths>
$env:GIT_SEQUENCE_EDITOR=':'; git rebase -i --autosquash $(git merge-base HEAD origin/main); Remove-Item Env:GIT_SEQUENCE_EDITOR
git rebase -x "npm run lint && npm run typecheck" $(git merge-base HEAD origin/main)
```

### 12.4 Verification on the head (phase 4)
One at a time: `npm run lint` · `npm run typecheck` · `npm run test:unit` · `npm run test:api` ·
`npm run format:check` · `npm run check:links` · `npm run build -w @masaha/shared`. Also:
`git grep -n "#PRNUM"` lists only documents before §12.7; `git diff --stat origin/main -- apps/web`
shows the two catalogue files only, one line each; `git diff --stat origin/main -- package.json
package-lock.json` is empty. **Not run, with why:** `test:component`, the web's `build`, `check:build`,
`check:classes` — the web's change is two catalogue strings, whose parity `test:unit` checks; CI runs the
rest on the pushed head.

### 12.5 The breaks (testing §3 rule 7), each recorded
For each: copy the file to `$env:TEMP\staff-breaks\` (a backup), make the one edit, run the named test
file, copy the red output into the report, restore **from the backup** (never `git checkout`), run it
green, then `git diff --stat` shows only the item's own work.

| # | Test | File | The edit |
|---|---|---|---|
| B1 | U1 | `temporaryPassword.ts` | 8 days |
| B2 | U2 | `temporaryPassword.ts` | `<` for `<=` |
| B3 | T1 | `users.service.ts` | `mayRecoverByEmail` = `maySignIn` |
| B4 | T2 | `auth.service.ts` | the resend checks `maySignIn` |
| B5 | T3 | `auth.service.ts` | the check's guard removed |
| B6 | T4 | `auth.service.ts` | the reset's guard removed |
| B7 | T6 | `users.service.ts` | the pending refusal removed from `accountForGoogle` (and `linkGoogle`) |
| B8 | T7 | `masaha_b_test` | `docker exec masaha-postgres-1 psql -U <user> -d masaha_b_test -c 'ALTER TABLE users DROP CONSTRAINT users_temporary_password_expiry_check'`; run T7 red; restore with the migration's own `ADD CONSTRAINT` statement through the same command; T7 green |
| B9 | T8 | `users.service.ts` | the issue passes the account's old expiry |
| B10 | T10 | `users.service.ts` | the expiry check removed (both places) |
| B11 | T13 | `users.service.ts` | `setEmail` in a second transaction after the first commits |
| B12 | T14 | `users.service.ts` | the forced-only check removed |
| B13 | T16 | `app.ts` | the staff router mounted at `/manage/spaces/:spaceId/staff` behind `requireAuth()` and `loadSpaceLinks` (no refusal) instead of inside the boundary's `manage` router |
| B14 | T17 | `space-links.manage.routes.ts` | `POST /` without `mayManage` |
| B15 | T17 | `space-links.manage.routes.ts` | `counted` before `mayManage` |
| B16 | T19 | `staff.service.ts` | on `null`, link the existing account |
| B17 | T20 | `space-links.manage.routes.ts` | `counted` after `validate` |
| B18 | T21 | `space-links.repository.ts` | `deactivatedAt: null` in `findReceptionLinksAt` |
| B19 | T22 | `staff.service.ts` | `endSessions` removed |
| B20 | T24 | `space-links.repository.ts` | `findReceptionLink` without the role |
| B21 | T25 | `staff.service.ts` | the pending check removed |
| B22 | T26 | `staff.service.ts` | the S5 check removed |
| B23 | T27 | `staff.service.ts` | the handover's link check removed |
| B24 | T28 | `space-links.repository.ts` | `findActiveLinksOf` without `deactivatedAt: null` |

A break that stays green: stop and ask.

### 12.6 The real run (API on 3321, `masaha_b_dev`)
1. `npm run dev -w @masaha/api` in the background; `curl.exe -s http://localhost:3321/health` → `db: up`.
2. As the admin (the `SEED_ADMIN_*` account; never print the password): create a space; `POST
   /api/v1/admin/owners` → the owner's temporary password; `POST /auth/password/forgot` for the owner's
   email → 202 and **no** reset email in the API's log (`EMAIL_MODE=log`: no `reset-password#token` line);
   sign in with it; `POST /me/password { password, email: <corrected> }` → 200; forgot for the corrected
   address → a reset line in the log.
3. As the owner: `POST /manage/spaces/<id>/staff { name, email }` → 201 with `no-store`; the same with
   the admin's email → 409 `EMAIL_HAS_ACCOUNT`; `GET …/staff` → the member pending; `POST
   …/staff/<id>/temporary-password/handover { channel: 'WHATSAPP' }` → 204; `POST …/temporary-password`
   → 200; the receptionist signs in with the new one → 200; set the receptionist's
   `temporary_password_expires_at` to the past in `masaha_b_dev` (`docker exec … psql … UPDATE users …`)
   → sign-in 403 `TEMPORARY_PASSWORD_EXPIRED`; re-issue → signs in; forced change; `GET
   /manage/spaces/<id>` as reception → 200; `PATCH …/staff/<id> { isActive: false }` → 200; the
   receptionist's old token → 401; `PATCH { isActive: true }` → 200; as the admin, `GET
   /admin/users?q=<email>` → `receptionSpaces` names the space.
4. Stop the server by its process id; `Get-NetTCPConnection -LocalPort 3321 -ErrorAction
   SilentlyContinue` prints nothing.

### 12.7 The PR number, push and PR
Just before the push, in Git Bash:
```bash
n=$(( $(gh api "repos/{owner}/{repo}/issues?state=all&per_page=1&sort=created&direction=desc" --jq '.[0].number') + 1 ))
base=$(git merge-base HEAD origin/main)
git filter-branch -f --tree-filter "grep -rl '#PRNUM' docs | xargs -r sed -i 's/#PRNUM/#$n/g'" $base..HEAD
git for-each-ref --format='%(refname)' refs/original/ | xargs -r -n1 git update-ref -d
git grep -n '#PRNUM' ; echo "expect nothing above; PR will be #$n"
git push -u origin feat/space-staff
```
Then `gh label list` (create `feat`, `area:api`, `area:docs` if missing, each with a description and a
colour), and at once:
```powershell
gh pr create --assignee @me --label feat --label area:api --label area:docs `
  --title "feat(space-links): add the owner's staff" --body-file <§12.9's text, saved in $env:TEMP>
```
Confirm GitHub's number equals `n`; if not, replace it in the documents (a fixup into the commits that
hold it) and `git push --force-with-lease`.

### 12.8 CI, CLEAN, conflicts, report
- `gh pr checks <n> --watch`, then `gh pr view <n> --json headRefOid,mergeStateStatus,statusCheckRollup`:
  green **on the pushed head** and `CLEAN`. Never merge; never rebase a `CLEAN` PR.
- **Conflicts, early:** for every other open PR, `git merge-tree --write-tree HEAD <its headRefOid>`;
  record clean or the conflicted paths. Documents or catalogue lines only: the fast path when its turn
  comes (keep both, `format:check`, one push). Code: stop and ask.
- **The report**, `D:\masahaWorkspace\WORKER_B\STAFF\4_REPORT_PR<n>.md`, written in parts with an editor
  (UTF-8): the head and the commits; each command run and not run; each test's red-first output; each
  break of §12.5 with its red output; §12.2's results; the real run's statuses; the owner's answers to
  §13 as built; the rewritten Google test (T6); the problems and their solutions; anything unexpected,
  even unsolved; the conflict check; every departure from this plan with its reason; the PR number.

### 12.9 The PR description (fill the evidence from the runs)
```markdown
## Summary
Accounts created by someone else made safe, platform-wide, and the owner's reception accounts (step 6), on the API.
- A temporary password pending: no reset email, no reset with an older link, no Google link (a mistyped address's holder could take the account).
- The forced change confirms or corrects the email (`POST /me/password { email? }`), audited.
- A temporary password expires 7 days after it is issued (`TEMPORARY_PASSWORD_EXPIRED`); a migration adds the expiry with a `CHECK`.
- Staff: the owner creates new reception accounts only (ADR 0009 rule 4 revised), lists them, deactivates (every session ends) and re-activates, re-issues a pending temporary password, records each handover; 10 an hour.
- The admin's users list carries each person's reception links.
- Documents: the contract, security, conventions, data model, ADR 0009, `users`, `auth` and `space-links`, the overview and the plan; finding 84.

## Scope / Acceptance criteria / Out of scope
<§2>

## Change type
feat — API code, a migration, the shared contract, tests and documents; one error code's two catalogue lines in `apps/web`. No dependency.

## New error code
`TEMPORARY_PASSWORD_EXPIRED` — en: <line>; ar: <line> (**the Arabic needs the owner's approval**).

## Evidence
- `npm run lint`, `npm run typecheck` (each commit), `test:unit`, `test:api`, `format:check`, `check:links`, `build -w @masaha/shared`: <results>.
- Seen failing first: <each test, its red line>.
- Deliberate breaks, each red then restored: <B1–B24>.
- Real run on 3321: <statuses>.
- Not run: `test:component`, the web's `build`, `check:build`, `check:classes` — two catalogue lines; CI runs them.

## Screenshots
None: API and documents only.

## Definition of Done checklist
- [x] Acceptance criteria met, scope kept.
- [x] Lint and typecheck clean; `packages/shared` builds.
- [x] Tests added in the owning lanes, each seen failing.
- [x] No hardcoded user-facing text; both catalogues updated for the new code.
- [x] Authorization enforced on the server (the boundary, `requireCan`, `can()` under the lock).
- [x] Triggered documentation updated in this PR; the contract's *Endpoints* met.
- [x] One home per fact; nothing claimed that is not built.
- [x] Every claim names its test or command.
- [x] Atomic history, pushed.
```

### The executor's stop rule — a test it cannot run stops the work
A test **failing** because the code is not written yet is the plan's red step — normal. A test or command
you **cannot run** is not. It is any of: the command errors before any test runs (the database
unreachable — `ECONNREFUSED`, `P1001` —, Docker not running, a port taken, a module or `dist` missing, a
migration pending, an environment variable absent, `No test files found`, a Vitest/TypeScript startup
error, a timeout of the whole run, a crash with no test result); a break of §12.5 you could not make or
could not run; a step of §12.6's real run you could not perform.
**When that happens: stop at once.** Do not work around it — never skip, `.skip` or delete a test, never
change a config, a timeout, `.env`, a script or a lane, never mock or stub what the plan does not, never
run a narrower command and call it the lane, never mark it "flaky" and move on. Write the exact command,
its exact error (the first lines that say why) and what you were about to do into the report, then reply
`Status: STOPPED`. The owner fixes the environment; you resume from there.
**Never claim a result you did not see.** A command counts as passed only when you saw its own output say
so; copy that line.

## 13. Decisions needed from the owner

1. **D1 — the lifetime:** 7 days (the prompt's number), in `TEMPORARY_PASSWORD_LIFETIME_MS` and the
   migration's backfill. Another number changes both lines and U1.
2. **D2 — one PR or two:** about 50 files, under the prompt's ~60, so **one PR** is planned, its seven
   commits in Part A then Part B order. Two PRs (PR 1 = C1–C3, PR 2 = C4–C7) would protect the admin's
   owners a review cycle sooner, at the cost of a second CI/review round and documents edited twice.
3. **D3 — the new code `TEMPORARY_PASSWORD_EXPIRED` (403)** (the prompt allows it for A3), and its two
   catalogue lines in `apps/web` under B's licence (workflow §9; the prompt's "nothing in `apps/web`" is
   kept otherwise). Draft copy:
   - en: `This temporary password has expired. Ask whoever created your account for a new one.`
   - ar: `انتهت صلاحية كلمة المرور المؤقتة. اطلب كلمة مرور مؤقتة جديدة ممّن أنشأ حسابك.`
4. **D4 — S1, no Google link while pending** (recommended): it changes an existing test's expectation
   (`google.api.test.ts:94`, which today links a pending Gmail account — the hole itself).
5. **D5 — A2's shape:** `email` optional on `POST /me/password`, refused 422 `invalid_choice` outside the
   forced change (P2); the answer unchanged (`{ accessToken }`), the web reading the new address at its
   next session read. Worker A builds the field.
6. **D6 — the staff list's pending field:** `temporaryPassword: { expiresAt } | null` (so the web can say
   "expired" and offer B4), and the PATCH answering the member (P7).
7. **S2–S5** — recommended and planned; say if any is not wanted.

## 14. Stop and ask

- #87 is not merged; or `origin/main` changed a code file §12.1 names in a way this plan does not cover;
  or an open PR edits a code file of §7.
- A change is needed in `apps/web` beyond the two catalogue lines (and §12.2.7's fixture), or a
  dependency.
- More than about 60 files would change.
- The migration cannot be made as §12.2.1 says, or a `CHECK` failure appears outside the helper's reach.
- The unique violation in the change is not `P2002` on `users_email_key` (§12.2.4).
- The existing Google test (T6) proves something S1 breaks besides the link itself.
- A break of §12.5 stays green.
- A failure not understood after three root-cause fixes; CI failing for a reason not reproduced locally
  after three.
- A conflict with another open PR in a code file.

---

## Appendix A — the documents, line by line (the commit in brackets)

1. **`docs/api/api-contract.md`** — *Last Updated* 2026-10-18.
   - §1 *Auth* line: unchanged.
   - §4 exceptions: `- a space's staff (GET /manage/spaces/:spaceId/staff), every reception link, active or not: a space has few, and the owner's page reads them whole (§5, *Staff (managed)*; why: [space-links › Decisions](../features/space-links.md#api-decisions)).` [C4]
   - *Session › POST /auth/login* errors: add `forbidden` (403) `TEMPORARY_PASSWORD_EXPIRED`, only once the password matches, for a temporary password past its expiry ([security.md](…#passwords)). [C1]
   - *POST /auth/google*: `conflict` (409) `GOOGLE_LINK_NOT_ALLOWED` also when the email's account has a temporary password pending. [C2]
   - *The forgotten password*: `forgot` and `resend`: "When the address has an account that may sign in **and has no temporary password pending**, the reset email is sent"; `reset/check` and `reset`: their invalid answers also cover "an account whose temporary password became pending". [C2]
   - *Me › POST /me/password*: body `{ currentPassword?, password, email? }`; `email` only during the forced change: the address confirmed, or corrected, audited `user.emailChanged`; errors add `validation` (422) `errors.email = ["invalid_choice"]` outside it, and `conflict` (409) `EMAIL_TAKEN` with `errors.email = ["not_unique"]`, nothing changed. "The answer is the same; the session's user reads the corrected address at its next refresh." [C3]
   - A new section **`### Staff (managed)`** after *Packages (managed)*: the routes of §4 B1–B4 and A4, each with body, answer, errors, audit; the `StaffMember` and `AddedStaff` shapes; the limit (one link to security). [C4–C6]
   - *Users (the admin) › AdminUserRow*: `receptionSpaces` line. [C7]
   - §6: `TEMPORARY_PASSWORD_EXPIRED` appended. [C1]
2. **`docs/backend/security.md`** — *Built* gains "the expiry of a temporary password; no email recovery and no Google link while one is pending; the email confirmed at the forced change; the temporary passwords created by an owner; the revocation when a reception link is deactivated"; *Not yet built* loses the two staff items. *Last Updated* 2026-10-18.
   - *Passwords › Accounts created by someone else*: the reception bullet becomes "a reception account the owner creates; an email that already has an account is refused, never linked ([ADR 0009](…), revised)" [C4]; a new paragraph: **A temporary password expires 7 days after it is issued**; a password sign-in with an expired one is refused (`TEMPORARY_PASSWORD_EXPIRED`), only once it matches; a session opened before keeps its forced change; a new one is issued by whoever created the account [C1]. **While one is pending, the account has no recovery by email and no Google link** — the email was typed by someone else, and only the person holding the temporary password proved anything; the forced change then confirms or corrects the address [C2, C3].
   - *Password reset › The request / Success*: "An unknown, suspended **or pending** account gets no email"; success "sets the password" (drop "settles a pending temporary one"), and the check and the success refuse a link of an account that became pending. [C2]
   - *Sign-in methods › Google*: "**where it links**" preceded by "never while a temporary password is pending (`GOOGLE_LINK_NOT_ALLOWED`)". [C2]
   - *Recovery without the email*: "an owner may also issue one to their own reception staff while its first is pending ([the contract](…#staff-managed))". [C6]
   - *Rate limits* table: `| Staff accounts | Every creation and re-issue by an owner, by the owner, counted before the body is read: each costs a bcrypt hash | 10 / hour |`. [C4]
   - *Authorization*: "The managed photo, package **and staff** routes ask `can()` first …". [C4]
3. **`docs/architecture/data-model.md`** — *User*: "and, while a temporary password is pending, when it expires ([security › Passwords](…))" [C1]; *Constraints worth stating*: "a pending temporary password has an expiry, and only a pending one (a `CHECK`)" under the later migrations' list [C1].
4. **`docs/features/users.md`** — *What it does*: the expiry; no email recovery or Google link while pending; the email corrected at the forced change; the owner's re-issue and handover through `space-links`. Remove "and the temporary passwords of the owner's reception accounts are not built". *API decisions* (each ending `2026-10-18, #PRNUM`): A3's column and P3/P4; A1 + S1 + S2 (`mayRecoverByEmail`); A2 + P2; `replaceWithTemporaryPassword` and `recordHandoverLocked` shared by the admin and the owner. *History*: `#PRNUM — the temporary password's expiry; no recovery by email or Google while pending; the email confirmed at the forced change; the owner's re-issue and handover.` [C1–C3, C6]
5. **`docs/features/auth.md`** — its reset and Google flow lines name the pending refusal (link to security); a decision line for S2's guard; *History* line. [C2]
6. **`docs/architecture/decisions/0009-space-scoped-reception-role.md`** — a second *Revised* line: `> **Revised:** 2026-10-18 — rule 4: the owner creates new accounts only; an email that already has an account is refused, never linked (a typed email can be wrong: a stranger would reach the desk). A person at two spaces' desks waits for a proof they give in person ([finding 84](../findings/84-….md)). #PRNUM`; rule 4's second bullet replaced by "an email that already has an account is refused: no existing account is linked by an owner." [C4]
7. **`docs/features/space-links.md`** — *What it does*: the owner's staff (create, list, deactivate and re-activate, re-issue, handover); the reception links in the users list. Replace "The dashboard screen and staff-management API remain planned" with "The dashboard screen remains planned". *How it composes*: the staff routes under the boundary with `requireCan('staff.manage')` and the limit; every write under the space's lock then the person's; the list composed (links here, accounts from `users`). *API decisions* (`2026-10-18, #PRNUM`): B1/P5; B2 whole; B3/P6/P7; B4/S5; B5/S3; B6; P1; P8. *Code map*: `staff/`, `space-links.manage.routes.ts`, `space-links.limits.ts`. *Open findings*: 84. *History*: `#PRNUM — the owner's staff; the reception links in the admin's users list.` [C4–C7]
8. **`docs/backend/conventions.md`** — §6 audit list: "space links: linking owners, adding, deactivating and re-activating staff"; "a person's email corrected at the first sign-in". *Built*: no change unless it names staff. *Last Updated*. [C3, C5]
9. **`docs/architecture/findings/84-a-person-cannot-work-at-two-spaces-front-desks.md`** — `# 84. A person cannot work at two spaces' front desks` · **Status:** Open · **Date:** 2026-10-18 · **Evidence:** an owner creates new accounts only (ADR 0009, revised): a receptionist who already has an account — at another space, or as a customer who registered — cannot be added; they would need a second account under another email. **Resolves when:** a second owner can link an existing account on a proof the person gives in person (a code shown on their own signed-in device), or the owner decides v1 needs none. Index line under *Open*. [C4]
10. **`docs/project/overview.md`** — the *Built* line of space links/users gains "the owner's reception accounts on the API (create, list, deactivate and re-activate, re-issue a pending temporary password)"; the owner/reception web screen stays planned. Check the exact *Built* line on the merged tree. [C4]
11. **`docs/plans/v1-mvp.md`** — step 6 (line ~87): mark its API built (`#PRNUM`), the screen remaining; remove the staff endpoints from *Planned API surface* if listed there (the contract's deferred rule). [C4]

## Appendix B — Claude Code skills, only a map

| Step | Skill (if the executor is Claude Code) |
|---|---|
| §12.1, the branch | `start-work-item` (its git part) |
| Each test red first, each break | `superpowers:test-driven-development` (workflow §10) |
| Any failure | `superpowers:systematic-debugging` |
| C1's error code | `add-error-code` |
| §12.4 before any claim | `superpowers:verification-before-completion` |
| §12.7–12.8 | `open-pr`, then `final-report` |

OpenCode follows the same steps from this plan alone.
