# DESK_API — specs B, C and D on the API (`feat/desk-api`) — the plan

> **Approved by the supervisor for the owner, 2026-10-25 — binding; continue with phase 2.** Every open point as
> the plan recommends:
> - **O1 — taken:** `requireAuth` answers 401 `SESSION_IDLE` **without deleting**; the refresh, for an idle
>   family, deletes it, clears the cookies and answers 401 `SESSION_IDLE` — so the web's refresh sees the code
>   (DESK_SCREENS PR 3 shows its line from the refresh's answer). A test: an idle reception's request → 401
>   `SESSION_IDLE`, the family still there; then the refresh → 401 `SESSION_IDLE`, the family gone; a second
>   device untouched.
> - **O2 — taken:** spec D names the price by its unique key, `published: { period, audience, shiftId? }` plus
>   the subscription's `name`, never a `priceId` (the price rows are re-created on every save,
>   `prices.repository.ts:31`). The supervisor recorded the changed request shape for worker A's PR 4.
> - **O3 — taken:** in the real run, after reception signs in, one SQL `UPDATE` moves **only that session's**
>   `last_activity_at` back 16 minutes on `masaha_b_dev`; name it in the report. Nothing else is written by
>   hand.
> - **O4 — `docs/architecture/data-model.md`**, beside its migration bullets (the partial indexes and the
>   `CHECK`s): "a migration's SQL comments carry a date, never a PR number: the `#PRNUM` rewrite would change an
>   applied migration's checksum".
> - **Size — ≈ 52 files approved** (commit 6's test helpers); **stop and ask past 60**.
> - **The per-request link query and the passive mark in `app.ts`:** accepted as stated, with their costs.
> - **The owner's standing rules:** each code fix red before green; a separate break only for a guard the red
>   step did not prove; `test:api` run with no command timeout; no PR number in the migration; no reset or
>   reseed of `masaha_b_dev` without the owner's word; no `fixup!` commit or rebase left in progress.

> Written 2026-10-25 from `origin/main` **`b7fe343e`** (#114 and #115 merged), read only. The contract: DESK_SCREENS
> `2_PLAN.md` §6 specs **B**, **C**, **D** (spec A not built) and its approval note (§14.4: the month 30 days, the
> week 7, the first day counted); `0_CARRIED_FROM_114.md` items 1–4. Findings from **170**; none planned.
> **Four points below need the supervisor's word before phase 2** (§5: O1, O2, O3 and the size).

## 1. The commits, in order (subjects counted)

| # | Subject (chars) | What |
|---|---|---|
| 1 | `docs(payments): say reception's refusal exactly` (47) | carried 1 — documents only |
| 2 | `fix(subscriptions): count 92 days with both ends` (48) | carried 2 — test red first |
| 3 | `docs(conventions): no PR number in a migration` (46) | carried 3 — one line (see O4) |
| 4 | `refactor(payments): reuse the item payment select` (49) | carried 4 — no behaviour change |
| 5 | `feat(desk): read a statement from one snapshot` (46) | spec B (statement and file) |
| 6 | `feat(auth): name the session in the access token` (48) | spec C, part 1: the `sid` claim |
| 7 | `feat(auth): end reception's session when idle` (45) | spec C, part 2: the column, the rule — **PR title** |
| 8 | `feat(desk): subscribe from a published price` (44) | spec D |

Spec C takes two commits: the `sid` claim alone touches every helper that signs a test token (≈ 9 files), and
reviewing it apart from the idle rule keeps commit 7 to the rule.

## 2. The carried items (commits 1–4)

1. **Docs:** `api-contract.md` › `GET …/payments` (*Who reads what*, *Errors*), `security.md`'s payments-list
   bullet, `payments.md` (S6, *Behaviour*): "the query is validated first (422); a valid `from`, `to` or
   `recordedById` from reception is then `forbidden` (403), never ignored".
2. **Test first:** `packages/shared/src/subscriptions/requests.unit.test.ts`: `to = from + 91` accepted, `to = from
   + 92` → `out_of_range` on `to` (red today: 92 is accepted). **Code:** `requests.ts:71` → `addDays(from,
   CHECK_IN_RANGE_MAX_DAYS - 1)`. Contract line 586: "at most 92 days with both counted", as the payments line.
3. One line (O4 for where): "a migration's SQL comments carry a date, never a PR number: the `#PRNUM` rewrite
   would change an applied migration's checksum". `payment_void_guard` untouched.
4. `payments.repository.ts`: the `uncollectedPage` JSDoc rewrapped ≤ 100 columns; `paymentsOfSubscription` and
   `paymentsOfVisits` select `ITEM_PAYMENT`. Green: `payments` and `desk` API files unchanged.

## 3. Spec B — one snapshot (commit 5)

- **The port:** `db/transaction.ts` gains `createReadSnapshot(db)` → `ReadSnapshot = <T>(work: (tx) => Promise<T>)
  => Promise<T>`: `db.$transaction(async (tx) => { await tx.$executeRaw\`SET TRANSACTION READ ONLY\`; return
  work(tx); }, { isolationLevel: 'RepeatableRead' })`. Exported from `db/index.ts`, injected into `createDeskService`
  (`readSnapshot`) by `app.ts`, as `runInTransaction` is. `RunInTransaction` is not widened.
- **Wrapped:** `statement` and `customerFile`, whole (their first read included, so the snapshot starts with it).
- **`tx` to each read:** those that take one already get it (`statesOf`, `itemBalances`, `customerBalances`,
  `customers.findIn`, `occupancy.presentIn`, `visits.deskVisitsOf`, `payments.paymentsFor`). Three gain an optional
  last `tx: Tx = prisma`, repository and service wrapper: `subscriptions.checkInsOf`, `subscriptions.renewedBy`,
  `payments.paymentsOfSubscription`. `Promise.all` stays (Prisma serialises a transaction's queries).
- **The race test** (`statement.api.test.ts`; then the same in `customerFile.api.test.ts`): through `locks.ts`, a
  test transaction takes `LOCK TABLE customers IN ACCESS EXCLUSIVE MODE` (the statement's second query,
  `customers.findIn`, reads it; its first, `statesOf`, does not — the executor confirms the order once with
  Prisma's query log and names the table it locks), starts the request, `waitingOnLock({ on: 'customers' })`,
  inserts a closed check-in and a payment on the subscription, commits. Asserted: `paidAgorot` = the sum of the
  listed payments not voided; `progress.minutesUsed` = the sum of the listed check-ins' minutes. Under
  `ReadCommitted`, `statesOf`'s progress predates the commit and `checkInsOf` follows it → unequal. The file's test:
  the balances (`customerBalances`) against the unpaid visits' sums, the lock again on the read between them.
- **Break:** `isolationLevel: 'ReadCommitted'` → both red. If the order gives no read on each side of a lock: say
  so, prove by the break alone (the spec's own fallback), a departure.
- **Docs:** conventions §9 › *Composed reads* (the rule line); `desk.md` (*API decisions*, *API history*); finding
  124 resolved.

## 4. Spec C — reception's idle session (commits 6, 7)

**Commit 6 — `sid`.** `AccessClaims` gains `sessionId: number`, signed as the JWT claim `sid`; `verify` refuses a
token without a safe positive integer `sid` (as one without `sessionVersion`) → `requireAuth`'s 401 → the web's
refresh replaces it. `sessions.issue` and `rotate` return `familyId` with the token; `users.accessClaims(account,
sessionId)`; `auth.service.sessionFor(account, familyId)` and `users.service` (the password change) pass it.
`SignedIn` gains `sessionId`. **Cost:** every access token alive at deploy is refused once, and refreshed silently.
Test helpers that sign tokens (`test/admin.ts`, `test/spaces.ts`, three API test files, the two `requireAuth`
tests, `accessToken.unit.test.ts`) get one helper in `test/app.ts`, `signAccess(user, { pending? })`, which inserts
a real family row and signs its id. Tests: a token without `sid` → 401; `verify` drops a bad `sid`.

**Commit 7 — the rule.**
- **Column:** `RefreshToken.lastActivityAt DateTime @default(now()) @map("last_activity_at") @db.Timestamptz(3)`.
  Set from the clock at sign-in (`issueInFamily`), copied on rotation from the rotated row (as `sessionEndsAt`).
  **Migration** `<ts>_session_activity`, `--create-only` once: `ALTER TABLE "refresh_tokens" ADD COLUMN
  "last_activity_at" TIMESTAMPTZ(3) NOT NULL DEFAULT CURRENT_TIMESTAMP;` — families alive at the migration start
  their 15 minutes from it (as `session_ends_at` did, #78). A comment line, dated, no PR number.
- **Idle-bound:** an account whose role is not `ADMIN` and whose **active** links include `RECEPTION` and no
  `OWNER`. No link is on the request when `requireAuth` runs (the boundary loads one space's, after it, and the
  rule is account-wide), so this is **one indexed query** on `space_managers(user_id)` per signed-in non-admin
  request: `spaceLinks.activeRolesOf(userId)` (distinct roles), wired into `requireAuth` by `app.ts` as the
  account reader is. Admins skip it. For an idle-bound account, **one more read** (the family's newest row, by
  `family_id`), and at most **one write a minute**.
- **`requireAuth`**, after every existing check (the 403 `PASSWORD_CHANGE_REQUIRED` included), through an injected
  `IdleSessions` port (`sessions` service, its clock): family missing → 401 (`Session ended`: a sign-out ends this
  device's access at once); `now − lastActivityAt > 15 min` → **401 `SESSION_IDLE`**; otherwise, unless the request
  is passive, `updateMany({ familyId, lastActivityAt < now − 60 s }, { lastActivityAt: now })` — every row of the
  family, so whichever token rotates next copies it (an idle-bound family lives one working stretch: tens of rows).
  The family is **not** deleted here (O1).
- **Passive:** `markPassive` (shared/auth) sets `req.passive`; `app.ts` mounts `api.get('/manage/spaces/:spaceId/
  occupancy', markPassive)` just before the boundary, the only passive route. A per-route mark inside the occupancy
  router cannot work: the boundary's `requireAuth` runs before the route is matched.
- **The refresh:** in its transaction, after `maySignIn`, `sessions.rotate(token, tx, { idleBound })`: after the
  expiry check, idle-bound and past 15 min → `deleteFamily` (this device; `sessionVersion` untouched), outcome
  `idle`; after the commit `auth.refresh` throws **401 `SESSION_IDLE`**, and the controller's existing 401 branch
  clears the cookies. The refresh renews nothing.
- **Constants:** `RECEPTION_IDLE_MINUTES = 15` in `@masaha/shared/auth`; `SESSION_IDLE` in `DOMAIN_ERROR_CODES`
  (status 401), its lines (`add-error-code` skill) «انتهت جلستك بعد 15 دقيقة دون نشاط. سجّل الدخول من جديد.» /
  "Your session ended after 15 minutes with no activity. Sign in again.", contract §6.
- **Tests** (`apps/api/src/modules/auth/idle.api.test.ts`, `createTestApp({ clock })`, sign-in through the API so
  the family carries the clock's time; the JWT's own 15 minutes run on real time, untouched):
  1. reception active at 14:59 → 200 and `last_activity_at` = then; 15:01 after it → 401 `SESSION_IDLE`;
  2. then the refresh → 401 `SESSION_IDLE`, `Set-Cookie` clearing, the family's rows 0; a second device (its own
     sign-in, active) → 200, its family and `session_version` unchanged;
  3. the occupancy polled every 30 s: 200 to 15:00, then 401 `SESSION_IDLE` on the next request;
  4. idle 2 h → 200 for an owner, an owner who is reception elsewhere, and an admin with a reception link;
  5. renewal throttle: requests at +10 s and +30 s leave `last_activity_at` at the sign-in; +61 s moves it;
  6. a token without `sid` → 401 (commit 6); a reception token whose family was signed out → 401.
  **Breaks:** the `markPassive` mount removed → 3 red; the refresh's idle path ending every session
  (`endSessions`) → 2 red (second device); the `OWNER` exclusion removed → 4 red.
- **Docs:** `security.md` › *Tokens and cookies* (row *Idle (reception)*), *Authorization* (`requireAuth`'s check);
  ADR 0003 *Revised: 2026-10-25*; api-contract §1 and §6; `auth.md` (*API decisions*, *API history*);
  `data-model.md` (the session's column). `OPEN_DECISIONS.md` stays the supervisor's.

## 5. Spec D — a published price (commit 8)

- **Code against the spec:** a published price has **no id** in any answer (`Price`, `@masaha/shared/spaces`), and
  every prices save **deletes and re-creates** the rows (`prices.repository.replace`), so an id the desk read dies
  at the owner's next save. See O2.
- **As recommended (O2 (b)):** `subscribeSchema` gains `published: { period: 'WEEK' | 'MONTH', audience, shiftId?,
  name: textSchema(1, PACKAGE_NAME_MAX_LENGTH) }`; exactly one of `packageId`, `published`, `custom` (refine on the
  count; else `invalid_choice` on `packageId`). The server finds the space's standard row (no label) by its key —
  unique by the three partial indexes — through `spaces.publishedPrice(spaceId, key, tx)` (prices repository); none
  → `invalid_choice` on `published`. Terms: `FIXED`, `priceAgorot` its amount, its audience and shift, no limits,
  `packageId` null, `priceTyped` null, `endsOn = addDays(startsOn, 6)` (WEEK) or `29` (MONTH). Under
  `subscriptions.manage` (reception may); no `mayType` check.
- **Tests** (`subscribe.api.test.ts`; `requests.unit.test.ts`): reception from the month price → 201, terms copied,
  `endsOn` = start + 29, `priceTyped` null; the week → + 6; a later prices save leaves it as it was; with
  `packageId` → 422; `HOUR` → 422 (schema); a key the space has not → 422 `invalid_choice` on `published`; the
  student month price picked by `audience`.
- **Docs:** api-contract (*Subscriptions*); `desk.md`, `subscriptions.md` (*API decisions*); data model › Package.

## 6. What the specs leave open — each with my recommendation

- **O1 (spec C vs worker A's plan) — where the idle family is deleted.** The spec deletes it in `requireAuth`. But
  the web's interceptor answers any 401 with a refresh, which would then find no token and answer a plain 401, and
  DESK_SCREENS PR 3 commit 5 shows the idle message only when **the refresh** says `SESSION_IDLE`. **Recommend:**
  `requireAuth` refuses `SESSION_IDLE` without deleting; the refresh deletes and says `SESSION_IDLE`. Safety is the
  same: nothing renews an idle family (the renewal runs only past the check; the refresh checks first). A browser
  closed meanwhile leaves the family until its 7 days (`deleteExpired` sweeps it). *Alternative:* delete in both,
  and the web shows no idle message.
- **O2 (spec D) — how a price is named.** **(b) recommended:** by its key (`period`, `audience`, `shiftId`), as a
  visit already picks its rates; no answer or web type changes; worker A's PR 4 sends `published: {…}` instead of
  `{ priceId, name }`. *(a):* `priceId` as written — the managed and admin space reads gain each price's `id`
  (`AdminSpace.prices`), the prices save's comparison drops it, web fixtures that build an `AdminSpace` change
  (≈ 4 more files), and an id goes stale at every owner save (the desk then answers 422, which is the safe side).
- **O3 (real run) — the idle case "with the clock".** The dev server on 3321 has no clock setting. **Recommend:**
  reception signs in, then the script moves **its own family's** `last_activity_at` back 16 minutes with one SQL
  statement on `masaha_b_dev` (session data, no domain row), then a request → 401 `SESSION_IDLE`, the refresh →
  401 and the family gone. The real 15 minutes not waited. *Alternative:* skip the case live; the API lane's clock
  proves it.
- **O4 (carried 3) — `conventions.md` has no migrations section** (`grep -i migration`: none). **Recommend:** the
  line in conventions §8 *Module rules* beside the schema's rule if one fits, else `data-model.md` › its
  migrations bullets (lines 143–146, where "a change to one is a new raw-SQL migration" lives); the subject then
  `docs(data-model): …`.
- **Also decided here, no question:** an owner who is reception elsewhere is never idle-bound (spec); a link change
  takes effect on the next request, and an owner demoted to reception whose family was not renewed while unbound
  ends at that request (signs in once — accepted, written in `auth.md`); a session that predates the column counts
  from the migration; today the web, on a `SESSION_IDLE` 401, refreshes, is refused, and lands on sign-in with no
  message until worker A's PR 3 commit 5.

## 7. Files, size, procedure

- **≈ 52 files** (docs 10: contract, security, payments.md, conventions or data-model, desk.md, auth.md,
  subscriptions.md, data-model, ADR 0003, finding 124; shared 6; web 2 catalogues; API source ≈ 20 incl. schema
  and migration; tests ≈ 14). **Past 45 — I ask approval now**; the excess is commit 6's token helpers. O2 (a) adds ≈ 4.
- **Migration:** `<UTC ts>_session_activity` (commit 7), `--create-only` once, `ls`, SQL read, `db:migrate`;
  `masaha_b_test` by the lane's setup; `migrate status` up to date.
- **Procedure:** PAYMENTS §12 adapted — §12.1 (`git diff --name-status b7fe343e origin/main`; open PRs; a shared code
  file → stop), the branch `--no-track`, `build -w @masaha/shared`, per commit lint/typecheck/its test files red
  then green; on the head once lint, typecheck, `test:unit`, `test:api` (no command timeout), format:check,
  check:links, check:conflicts; `git grep "#PRNUM"` documents only, none in the migration; `apps/web` diff = the two
  catalogues. CI judges `test:component`, the web build, `check:build`, `check:classes`. Breaks from backups
  (`scripts\breaks\`, SHA-256 before/after).
- **Real run** (`scripts\realrun.mjs`, 3321, `masaha_b_dev`, `PASS|FAIL`, `ALL PASS`): owner reads a demo
  statement and a file (sums agree); reception idle (O3); reception subscribes a demo customer from the demo
  space's published month price (201, start + 29) — **its one write**; the owner's session after its family is set
  back 2 h → 200 (the owner never idle-ended). A demo case missing → stop and report.
- **Stop rules** (the prompt's §3): a lane or test I cannot run, a spec false against the code, a break that stays
  green (its exception aside), an item left undone, past the approved size, a shared code file with an open PR →
  stop and report, `Status: STOPPED`.
