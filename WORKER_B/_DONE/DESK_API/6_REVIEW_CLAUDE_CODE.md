# Review — DESK_API, #118 `feat/desk-api` (independent reviewer)

- **Head:** `12abd2643c48e87a926b55e87b18c1d5d36d7c54`, base `origin/main` (`b2f13a47`), 8 commits, 59 files.
- **CI:** every check green on that head (build, check:classes, check:conflicts, check:links, format:check, lint,
  test:api 7m11s, test:component 18m13s, test:unit, typecheck; CodeRabbit rate-limited, reported pass).
  `mergeStateStatus` CLEAN.
- **Head moved during the review:** no. Re-checked at the end: still `12abd264`, CLEAN.
- Read only, from commit objects pinned to the head (`git show <sha>:…`, `git diff origin/main...<sha>`).
  Nothing run.

**Verdict: mergeable.** No blocker. Two small should-fix test gaps and some nits go to worker B's next PR
(`0_CARRIED_FROM_118.md`). Two findings to record (170, 171).

---

## Findings, most severe first

### 1. should-fix — no test proves that the refresh renews nothing for a live reception session
- **Where:** `apps/api/src/modules/sessions/sessions.service.ts` `issueInFamily` (`lastActivityAt = family?.lastActivityAt ?? at`)
  and `rotate` (passes `stored`); `apps/api/src/modules/auth/idle.api.test.ts`.
- **Seen in the code:** the rotation copies the presented row's `lastActivityAt`. That is correct today.
  But none of the six idle tests refreshes a **live** reception session. Test 2 refreshes an idle one, which is deleted before
  any rotation. Test 4 refreshes owners and the admin, who are not bound. Test 3 never refreshes.
- **Failing scenario (a bug the suite would let through):** the rotation writes `lastActivityAt: at` (or the
  `?? at` fallback is reached). Then every refresh renews the session. The web refreshes on every page load, and
  on the 401 of an expired 15-minute access token. So a desk left open that is reloaded, or that refreshes
  ahead of time, never ends. All six idle tests stay green.
- **Fix:** one API test. Reception signs in at T, refreshes at T+10 min (200), and the new row's
  `last_activity_at` is still T. Then a request at T+15:01 with the new access token gets 401 `SESSION_IDLE`.
- **Where the fix belongs:** small — **worker B's next PR, first commit** (`0_CARRIED_FROM_118.md`).

### 2. should-fix — spec D: no test covers a published price that has a shift
- **Where:** `apps/api/src/modules/spaces/prices/prices.repository.ts` `findStandard` (`shiftId: key.shiftId ?? null`);
  `apps/api/src/modules/desk/subscribe.api.test.ts`.
- **Seen in the code:** the lookup matches the shift correctly. The tests cover a general month price, a week price, a student
  month price, a labelled price, another space's price and `shiftId: 999`. No test uses a price that has a real
  shift.
- **Failing scenario (a bug the suite would let through):** suppose `findStandard` dropped the shift from its
  `where`. Take a space with a month price of 25,000 and a morning-shift month price of 15,000. Reception asks for
  the morning one, and `findFirst` may return the 25,000 row with `shiftId: null`. The customer is charged the
  wrong price and loses the shift on the subscription. The `shiftId: 999` case would still give 422, because the
  only week price in that test has a label and is filtered out. So every spec D test stays green.
- **Fix:** add a shift and two month prices (no shift, and that shift), then subscribe with each key.
  Assert the `priceAgorot` and `shiftId` copied from each.
- **Where the fix belongs:** small — **worker B's next PR, first commit**.

### 3. nit — ADR 0003's revision says the guard ends an idle session; under O1 it does not
- **Where:** `docs/architecture/decisions/0003-session-model.md`, the 2026-10-25 *Revised* line: "the guard and
  the refresh end an idle one".
- **Seen in the code:** `requireAuth.ts` throws `SESSION_IDLE` and deletes nothing (`sessions.idleState` returns
  `'idle'` and keeps the family). Only `rotate` deletes. `security.md`, `auth.md` and the contract say this
  correctly; the ADR contradicts them.
- **Fix:** "the guard refuses an idle one (401 `SESSION_IDLE`) and the refresh ends it".
- **Where the fix belongs:** small — **next PR, first commit** (documents).

### 4. nit — the test helper `signAccess` dates its session by the database clock, not the test's clock
- **Where:** `apps/api/test/app.ts` `signAccess`: the family row is created without `lastActivityAt`, so the
  column's `DEFAULT CURRENT_TIMESTAMP` (real time) applies.
- **Failing scenario:** a later test uses `createTestApp({ clock })` with a clock more than 15 minutes ahead of
  real time and a reception token from `signAccess`. Its requests then get 401 `SESSION_IDLE`, which looks
  unrelated to what the test is about. No current test hits this (CI is green).
- **Fix:** set `lastActivityAt: FAR_AHEAD` in the helper, the same way as `expiresAt` and `sessionEndsAt`.
  Then `now − lastActivityAt` is always negative, the session is always live, and no renewal is written.
- **Where the fix belongs:** small — **next PR, first commit**.

### 5. nit (plausible) — a request's renewal racing a rotation can be lost on the newest row
- **Where:** `sessions.repository.ts` `familyActivity` (reads the **newest** row) and `renewActivity`
  (`updateMany` over the family); `sessions.service.ts` `rotate` (copies the presented row's value).
- **Scenario (reasoned, not run):** tab A refreshes. Inside its transaction it inserts the new row with the old
  `last_activity_at = L0` and locks the old row with `markRotated`. At the same moment tab B sends a request with a
  still-valid access token, and its `updateMany` runs. Under READ COMMITTED that UPDATE cannot see A's
  uncommitted new row. It waits on the old row's lock and then updates only the old row. The newest row keeps L0,
  and both `idleState` and the next `rotate` read L0. So the renewal is lost, and the session can end up to
  "time since L0" early if nothing else renews it within 60 s. It needs two tabs and a refresh within the same
  milliseconds, and the cost is one extra sign-in, never a session kept alive. That is why this is plausible
  and minor.
- **Fix:** read `max(last_activity_at)` over the family in `familyActivity`, and copy that maximum on
  rotation. Or take the session lock in the renewal, which costs more.
- **Where the fix belongs:** **record a finding (170)**. It is not worth a fix round.

### 6. finding to record — a published price changed between the desk's read and the subscribe is charged silently
- **Where:** `desk.service.ts` `subscribe`: `spaces.standardPrice(space.id, request.published, tx)` under
  `lockAtDesk`'s space lock. The prices save (`prices.service.ts` `update`, through `editGroup`) holds the same
  space lock.
- **Seen in the code:** the two writes are serialised, so the subscribe always reads one committed set of
  prices, never a half-replaced one. If the owner deleted the key, the answer is 422 `invalid_choice` on
  `published`. If the owner changed the amount, the customer is charged the **new** amount. The answer's
  `subscription.priceAgorot` shows it, but nothing tells the desk the amount differs from what it displayed. With
  a `payment` sized for the old amount, two things can happen. If the new price is lower, the ledger refuses the
  overpayment (`PAYMENT_EXCEEDS_DUE`) and the whole subscribe fails. If it is higher, a balance is left without
  any warning.
- **This follows the spec** ("its amount is the server's"), so it is **not a defect of this PR**. Recording it lets PR 4's
  screen, or a later change, decide. Options: an optional `published.amountAgorot` that the server compares,
  answering 409, or the screen re-reading the price before confirming.
- **Where it belongs:** **record a finding (171)**, for the owner to decide with DESK_SCREENS PR 4.

### 7. nit — unrelated whitespace in `schema.prisma`
- **Where:** `apps/api/prisma/schema.prisma`: the `User` and `SpaceSettings` columns are re-aligned (the
  formatter caught up with `temporaryPasswordExpiresAt` and `receptionMayTypePrices`). These lines change
  whitespace only and are not part of the task.
- **Fix:** none needed. Reverting would leave the file unformatted again. Noted only for the scope rule.

---

## `SESSION_IDLE` — the Arabic line (for the owner's approval)

Seen in `apps/web/src/shared/copy/arabic/errors.ts`, character for character the spec's line:

> انتهت جلستك بعد 15 دقيقة دون نشاط. سجّل الدخول من جديد.

English (`english/errors.ts`): "Your session ended after 15 minutes with no activity. Sign in again."
The code is in `DOMAIN_ERROR_CODES` (auth group) and in contract §6. Both catalogues compile, since typecheck
enforces their parity.

---

## The departures, each judged

1. **Spec B's race tests lock `visits`, not `customers` — right.** The code confirms it. In the file,
   `customers.findIn` is the **first** read, so a lock there would block before the snapshot is taken. Both
   isolation levels would then see the commit, and the test would prove nothing. `visits` is read only by the money
   reads (`itemBalances`, `customerBalances`, later `presentIn` and `deskVisitsOf`). Those are queued after
   `statesOf` and, in the statement, after the payments and check-ins lists. So the lock really does sit between
   two reads. That the tests failed on the old code and under the `ReadCommitted` break is **read in the report
   only**. The interleaving argument is mine, from the read order in the code.
2. **Spec D's `name` inside `published` — acceptable.** DESK_SCREENS' approval note says "`published: { period,
   audience, shiftId? }` plus `name`", which does not say where `name` goes. The code and the contract put it
   inside. **The supervisor should tell worker A's PR 4 to send it as `published.name`.** A top-level `name` is
   stripped by zod, and the request then fails with `published.name: required`.
3. **Two extra breaks (B5 the day count, B6 the label filter) — right**, by the owner's rule: they are guards the
   red step did not prove. Seen in the report only.
4. **The idle time passed into `sessions` from `auth` and `app.ts` (the lint level rule) — acceptable.** One
   constant (`RECEPTION_IDLE_MINUTES`, shared) is turned into milliseconds in two places (`app.ts` inline,
   `auth.service.ts` `RECEPTION_IDLE_MS`). Both read the one constant, so a single owner keeps it. `sessions` stays
   free of policy and only takes a bound.
5. **The owner's two idle hours proven in the API lane only — acceptable.** O3 allows one hand-written row.
   `idle.api.test.ts` test 4 covers the owner, an owner who is reception elsewhere, and the admin with a reception
   link (seen in the code). Break B4 is in the report only.
6. **59 files — within the approved 60.** Counted from the diff.
7. **The first `test:api` run's timeout (customers scale test, 1,000 subscriptions) — I agree it is the lane's
   load, not the snapshot.** The scale test's list and payment-filter reads are **not** wrapped (`customers()` is
   unchanged). Only its one file read is, and that read covers one customer: one connection held for a few
   queries in sequence, tens of milliseconds, as the executor measured. If the snapshot starved the pool,
   Prisma's 2 s `maxWait` would fail with P2028, not the test's 5 s timeout. The measured times are **read in the report
   only**, and CI's `test:api` on the head is green.
   One side effect to know about: the default 5 s interactive-transaction timeout now bounds the statement and the
   file. A read slower than that now fails instead of answering slowly. Both reads are bounded by one customer or
   one subscription, so this is acceptable.
8. **Idle-bound counts active links of soft-deleted spaces — acceptable.** It matches how ADR 0009 and the data
   model already define `OWNER` ("a soft-deleted space's included") and `countOwnerLinks`. The other way round is
   harmless: a reception link at a deleted space binds an account that can open nothing anyway. It is not written
   in `security.md`'s *Idle (reception)* row; half a line could go with finding 3's commit.

---

## Checked and fine (seen in the code)

- **`sid`:** signed as `sid`. `verify` refuses a token whose `sid` is missing, not a number, not a safe integer, or
  below 1 (unit test with `undefined`, `'41'`, `1.5`, `0`, `-1`). An API test proves a token without `sid` gets 401.
  Every signing path passes the family id: sign-in, login, Google link, refresh, password change.
- **`requireAuth` order:** signature and claims, then the account (missing, suspended, `sessionVersion`, pending
  password), then 403 `PASSWORD_CHANGE_REQUIRED`, then the idle check. Admin is skipped before any link query.
  Idle-bound means `RECEPTION` present and `OWNER` absent among the active links (`deactivatedAt: null`), read on
  every request. A signed-out family gets 401 with no code. A `sid` cannot name another user's family without the
  signing secret.
- **O1:** `requireAuth` answers `SESSION_IDLE` and deletes nothing (test 1 asserts the family is still there).
  `rotate` checks idleness after the expiry check and **before** the grace and reuse paths, deletes only this family,
  and returns `idle`. `auth.refresh` throws `SESSION_IDLE` after the commit, and the controller's 401 branch clears
  both cookies (test 2). `sessionVersion` is unchanged and the second device keeps working (test 2). Nothing else
  revives an idle family: the renewal runs only on `live`, and the refresh checks first.
- **The renewal:** `updateMany` with `lastActivityAt < now − 60 s`, so a burst writes once (test 5). It is skipped
  when `req.passive` is set.
- **The passive mark:** `api.get('/manage/spaces/:spaceId/occupancy', markPassive)` is mounted before the
  `/manage/spaces/:spaceId` guard. The routers mounted earlier on `/manage/spaces` (`createSpaceLinksMeRouter`) and
  `/me` guard per route (`router.get('/', requireAuth(), …)`), so no guard runs before the mark. The matcher is exact
  (`app.get`, end-anchored), so `/capacity`, `/status-override` and the other managed routes are not caught. The
  occupancy router's only `GET /occupancy` is the poll. `req.passive` is set only by that middleware; no header or
  query sets it.
- **The rotation** copies `lastActivityAt` and `sessionEndsAt` from the presented row. The family's other rows
  are updated together, and other families are untouched.
- **The migration:** one column, `TIMESTAMPTZ(3) NOT NULL DEFAULT CURRENT_TIMESTAMP`, so existing families count
  from the migration. The comment is dated with no PR number. `schema.prisma` matches it
  (`@default(now()) @db.Timestamptz(3)`).
- **Spec B:** `readSnapshot` is `$transaction` with `RepeatableRead` and `SET TRANSACTION READ ONLY` before the
  first read. Every read of `statement` and `customerFile` takes `tx`, including the three that gained it
  (`checkInsOf`, `renewedBy`, `paymentsOfSubscription`) and `withMoney`'s two. No lock is taken, and nothing slow or
  over the network runs inside the transaction. The tests assert sums equal lists (paid against listed payments,
  minutes against listed check-ins, balance = due − paid, debt = positive balances).
- **Spec D:** the schema counts to exactly one of `packageId`, `published` and `custom` (else `invalid_choice` on
  `packageId`), and allows only `WEEK` or `MONTH`. The price is looked up by space, period, audience, shift (or none)
  and `labelAr: null`; the four partial unique indexes make that one row at most. The terms are `FIXED`, its amount,
  audience and shift, no limits, `packageId` null, `priceTyped` null. The end is `startsOn + 6` or `+ 29` (tests:
  10-21 → 11-19 is 30 days, 11-20 → 11-26 is 7). `mayType` is false, so reception may subscribe even where typing is
  off (the test uses reception). Idempotency is unchanged: the same key returns the first subscription.
- **Carried from #114:** item 1 is in the contract (*Who reads what*, *Errors*), `security.md` and `payments.md`.
  Item 2 is `addDays(from, CHECK_IN_RANGE_MAX_DAYS - 1)`, with unit-test edges 07-22→10-21 accepted (92 days) and
  07-21 → `out_of_range`, and the contract line updated; the constant has no other user. Item 3 is a line in
  `data-model.md` beside the migration bullets (O4); `payment_void_guard` is untouched. Item 4 has both selects on
  `ITEM_PAYMENT` (`VISIT_PAYMENT` plus the void fields, the same set) and the JSDoc rewrapped.
- **Documents:** `security.md` (the *Idle (reception)* row, *Authorization*), the contract (§1, the refresh, the
  subscribe, check-ins, payments, §6), `auth.md`, `desk.md`, `subscriptions.md`, `payments.md`, `data-model.md`, and
  finding 124 resolved and moved in the index. They match the code, except finding 3 above. Each fact has one home
  with links, and `#118` is everywhere the number goes; no `#PRNUM` is left anywhere.
- **Scope and commits:** `apps/api`, `packages/shared`, `docs`, and the web's two `errors.ts` (one line each).
  Eight subjects, each 50 characters or fewer, each with a body. No tool attribution.

## Read only in the executor's report (not verified here)

The red-then-green lines, breaks B1–B6, the per-commit lint and typecheck, the local `test:api` runs and their
timings, and the real run (its O3 `UPDATE`, subscription 5 on `masaha_b_dev`).
