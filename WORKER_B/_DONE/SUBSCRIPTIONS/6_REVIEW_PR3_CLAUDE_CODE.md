# Review after the merge — SUBSCRIPTIONS PR 3 (#109), second reviewer

## 1. Range

- **Reviewed:** `7dfe360c^1..e262298e` (nine commits: `7db54e68`, `ff9348f6`, `e0699168`, `488a4c70`, `e91c5228`,
  `6056e92d` C1, `bcb328ce` C2, `ea3135f6` C3, `e262298e` C4), read from commit objects only.
- **`origin/main`:** `dec7bd37` at the start, `dec7bd37` at the end. Between `e262298e` and `dec7bd37` no file
  under `apps/api` or `packages` changed (only `apps/web` and `docs/features/directory.md`), so every API line
  cited below is the same on the PR's head and on `origin/main`.

## 2. Verdict

**One critical finding: a fix branch is needed** (finding 1). The other findings are small or to record.

## 3. Findings

### 1. critical: a subscriber's check-out records the stay up to now, past its due time, into the next day → fix branch now

- **Where:** `apps/api/src/modules/desk/desk.service.ts:487-494` (`checkOutSubscriber`: `at = now()`, then
  `subscriptions.checkOut(…, at, tx)`); `subscriptions.service.ts` `checkOut` → `repository.closeManual(id, at)`
  (`subscriptions.repository.ts:340-346`).
- **Seen in the code:** the visit's check-out caps the stay at its due time (`desk.service.ts:545`,
  `visits.stayEndAt` → `stayEnd(…)`). The subscriber's check-out reads no week, no settings and no
  `autoCheckoutDue`, and writes `checked_out_at = now`. `docs/architecture/data-model.md:83` (*Auto check-out*)
  says that open **visits and check-ins** are due by 23:59 of the check-in's Gaza day at the latest, and that "a stay the desk
  checks out after its due time — the job not yet run, or not running — is closed at that due time … so no path
  charges a stay into the next day" (#102, finding 116). This PR adds a path that does what finding 116 fixed for visits.
- **Failing scenario:** a space with closing-time check-out on and hours until 22:00. A subscriber on a `PER_HOUR`
  subscription (₪6/h) checks in at 20:00. The auto check-out job does not run overnight (cron down, the API
  restarted, or a batch past `AUTO_CHECKOUT_BATCH`). At 09:00 the next morning the subscriber comes back. The
  check-in is refused `MEMBER_ALREADY_CHECKED_IN` because the stale check-in is still open, so the desk checks
  the old one out. Stored result: `checked_out_at` = 09:00 the next day, 780 minutes instead of 120.
  `subscription_usage` then stores and answers `minutes_used` +660, `due_agorot` +₪66 (the check-out's own
  `balanceAgorot` shows it). A `totalHours` subscription can turn `EXPIRED` early. All 780 minutes count on the
  check-in's day (`minutes_today` of that day). The same overcount happens, smaller, whenever the desk closes a
  stay a few minutes after its due time and before the job's next tick, and it ignores `maxStayMinutes`.
  Attendance and money are stored wrong. Nothing reverses it: the check-out is audited, and no correction route
  exists for a check-in's times.
- **Why it slipped through:** the plan's D11 says "`checkedOutAt = now`". The plan was written on `abc28e73`
  (#97), before #102 put the due-time cap on the desk's path. Neither the executor's §12.1 check nor the Codex
  review compared C3 with data-model line 83.
- **Fix:** in `checkOutSubscriber`, close at `min(now, autoCheckoutDue({ checkedInAt, week, autoCheckoutAtClosing,
  maxStayMinutes }))`, from the space's week and settings read under the lock. This is the visit's rule.
  Ideally share one helper with `visits.stayEnd` (one rule) and keep the request's time in the audit as the
  visit does (`requestedAt`). Test: an open `PER_HOUR` check-in from yesterday 20:00, checked out at 09:00, gets
  `checkedOutAt` = its due time, and its minutes and due stop there. Break: `at` passed back in. Documents: the
  contract's check-out line ("the check-in closed now") gains the due-time clause, as the visit's check-out has
  it. `desk.md` gets a decision line.

### 2. small: the partial unique index answers a 500, not `MEMBER_ALREADY_CHECKED_IN` → next API Work Item, via `0_CARRIED_FROM_109.md`

- **Where:** `subscriptions.repository.ts:402-410` (`createCheckIn`, a plain `tx.checkIn.create`, no P2002
  mapping).
- **Seen in the code:** the contract (`api-contract.md`, the check-in's errors) and D11 call the index
  `check_ins_customer_id_key` the "backstop" behind `MEMBER_ALREADY_CHECKED_IN`. Under the space's lock the index
  never fires today. If it ever fired, the unmapped unique violation would answer 500.
- **Scenario:** a write path added later (another module's check-in, a seed or repair script running while the
  desk writes) inserts an open check-in for the customer without the space's lock. The desk's check-in then
  passes `isPresent` and hits the index: 500, with no code.
- **Fix:** map the violation of that index to `AppError.conflict('MEMBER_ALREADY_CHECKED_IN')` in the repository
  (the pattern `create`'s `isForeignKeyViolation` already uses). Or reword the contract so it does not promise
  the code from the index. Plausible rather than reachable today: it needs a writer outside the lock.

### 3. small: the contract's *Front desk* introduction still says every check-out sends a key → next API Work Item

- **Where:** `docs/api/api-contract.md:508`: "The check-in, the check-out and the payment send an
  `Idempotency-Key` (§1) … a retry with the same key answers the first result." Line 577 (the subscriber's
  check-out) says "No body and no key".
- **Fix:** "The check-ins, a visit's check-out and the payment send …". One line.

### 4. record: the phone fix (carried item 3) only works because `+970` ends in 0

- **Where:** `apps/api/src/modules/customers/customerSearch.ts:24` (`phoneDigits: '0' + phone.slice(4)`),
  `customers.repository.ts` `endsWith`.
- **Seen:** the decided case works. `0521234567` normalises to `+972521234567`, and the stored `+970521234567` has
  the digits `970521234567`, which end in `0521234567`. That holds only because the country code `970` ends in
  `0`. The opposite case fails: a phone stored as `+972591234567` and typed `0591234567` (normalised to
  `+970591234567`, digits `0591234567`) is not found, because `972591234567` does not end in `0591234567`. Item
  3 asked only for the first case, so this is not a defect against the decision.
- **Record:** a finding that the whole-number search is asymmetric between the two codes. If it is ever needed,
  the fix is to match on the national digits without the trunk (`phone.slice(4)`, at least 9 digits).

### 5. record: the dated list filters on an expression, not on the `(space_id, checked_in_at)` index

- **Where:** `subscriptions.repository.ts:369`: `(checked_in_at AT TIME ZONE 'Asia/Gaza')::date BETWEEN …`.
- **Seen:** the expression has no index, so each page and its count read all of the space's check-ins. At a
  coworking space's volume this is cheap for years. The bounds stay correct (T16 proves both edges).
- **Record:** a finding with the fix: bound `checked_in_at` by the two Gaza midnights as instants. That fix runs
  into finding 120 (two zone databases), so decide it together with that finding.

### 6. record: a check-in's retry can add `SPACE_FULL` that its first answer did not have

- **Where:** `desk.service.ts:451-453`. The retry calls `occupancy.checkInWarnings` with the check-in already
  present.
- **Seen:** with capacity 4 and 3 present, the first request answers no warning and the retry answers
  `SPACE_FULL`. The contract states this ("the visit or the check-in counted present"), as the visit's retry
  already does. D11 step 2 says "so the same warnings answer twice", which holds for the limits only. This is a
  stated departure, so no change is needed. It is listed because T5 says "the same warnings" and tests a case
  with no capacity.

## 4. Where the Codex review was wrong or thin

- **Check-out, "a closed row is returned unchanged" and "fine":** it never compared C3 with data-model line 83
  or finding 116, and missed finding 1, the one critical defect.
- **"Documents … reviewed against the code":** the data model's *Auto check-out* line is now false for check-ins
  (finding 1), and the contract's *Front desk* introduction is wrong about the key (finding 3).
- **"The database's one-open-check-in constraint remains the backstop":** if it ever fired, it would answer a
  500, not the documented code (finding 2).
- **The carried items 1–8:** it judged only item 5, and only as "acceptable" from the report. It did not check
  items 1–4, 6–8 in the code, and missed the `+970` dependence of item 3 (finding 4).
- **"Warnings and dates: … fine":** it never looked at a stay across midnight, which the brief named as an
  attack.
- **Tests:** it did not say that T12–T14 have no overdue or cross-midnight case. This is the gap that let
  finding 1 through.

## 5. Checked and fine (seen in the code)

- **Authorization:** all three routes are under `requireSpaceAccess`. The check-in and check-out use
  `requireCan('attendance.record')` at the route and `can()` again on `linksUnder(tx)` after the space's lock
  (`lockAtDesk`). The list is the staff's boundary only, as for the other staff reads (#86). There is no
  owner-only action on these routes.
- **Nothing of another space is reachable by id:** `lockIn` (`s.space_id`), `lockCheckInIn` (`space_id`),
  `findCheckInByKey` (`(space_id, request_id)`), `contactsOf` and `statesIn` (`space_id`), and both list queries
  (`space_id`) all filter on the space. The composite foreign keys `(customer_id, space_id)` and
  `(subscription_id, customer_id)` also tie a check-in to its space's customer and subscription.
- **Check-in order (D11):** lock, key, subscription `FOR UPDATE`, archived, present, warnings, insert, audit. A
  key reused for another subscription answers 409 with no code. The archive and the correction or end of a
  subscription read under the same lock (T9, T10).
- **Lock order:** space, then subscription (the check-in) or check-in (the check-out). This matches D14 and the
  other desk writes. The auto check-out takes only a check-in's row, `WHERE checked_out_at IS NULL FOR UPDATE`,
  so a desk check-out that waits on it re-reads the closed row and answers it as it is. No two lock orders cross.
- **Limits:** the warning order is `UPCOMING`, `EXPIRED`, days, hours. `DAYS_PER_WEEK_USED` warns only when today
  is not counted yet. `>=` warns at the bound. Today and the week's start come from `calendarOf(at)`, the Gaza
  date. A retry's `progressWithout` removes only its own day, unless another check-in shares that day, and only
  its own minutes, including after a check-out.
- **Present once (C1):** `present.ts` is the only reader of the two sources. The occupancy read, the warnings,
  `liveStatusFor`, `isPresent` (check-in and archive) and the customer file all go through it. The directory's
  sum is unchanged for spaces with no check-ins.
- **List (C4):** `open=true` reads every open check-in, earliest first, and is not paged. A range requires both
  dates, `to` no earlier than `from` and at most `from + 92`, and is paged with a count. `open` together with a
  range answers `invalid_choice`. Both Gaza-date edges are tested.
- **Money on the check-out:** `withMoney` reads `itemBalances` after the close in the same transaction, so the
  due is `subscription_usage`'s (one rule) and paid and balance are the ledger's.
- **Carried items:** item 1 (`desk.service.ts:751-753`, plus the contract line); item 4 (`:248-252`, older by
  `itemBalances`' order); item 5 (`STAY_MINUTES` is the function's expression, character for character); items
  2, 6, 7 and 8 (the *Authority* line, the 2026-10-21 date, the 49-debt decision line, findings 124 and 125 with
  their index lines). All present on `main`.
- **Read only in the executor's report, not seen:** the red-before-green runs, breaks B1–B18, I5 and B7k, the
  database check of the partial index, the real run, and the CI results.
