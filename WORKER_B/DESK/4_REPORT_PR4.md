# DESK PR 4 — `feat/visit-debts` — the executor's report

> Written as the work goes. Worker B, `C:\dev\masaha\app-b`, 2026-10-20.

## Precondition and 12.1 Before the branch

- `gh pr view 97 --json state,mergeCommit` → `MERGED`, `abc28e73`.
- `git status --short --branch` → `## HEAD (no branch)`, clean. `origin/main` = `abc28e73`.
- `git diff --name-status e122b95d origin/main` → empty.
- Open PRs: **#98** `feat/owner-packages` (worker A, head `8c429ff4`): `apps/web` and documents only. The documents
  shared with this PR are `docs/README.md`, the findings index and `overview.md`. No code file is shared.
- `0_CARRIED_FROM_97.md` exists and was read whole, along with `6_REVIEW_PR3_CLAUDE_CODE.md`.
- `git switch --no-track -c feat/visit-debts origin/main` → switched. `docker start masaha-postgres-1` → ok.
  `npm run build -w @masaha/shared` → exit 0.
- `apps/api/.env` (checked by pattern; values masked): `PORT=3321`, `masaha_b_dev`, `masaha_b_test`.
- `prisma migrate status` → `20 migrations found` · `Database schema is up to date!`
- Free memory: 4,519,640 KB. No `vitest` or `tsc` node process was running.

## Carried from #97

### Item 1: one failing stay no longer halts the job

- **Test**, in `shared/jobs/jobs.api.test.ts`: `a stay that cannot be closed is logged, and the stays after it are
  still closed`. The earlier stay's charge overflows its `Int` column, so its own transaction fails.
- **Red first:** `Tests  1 failed | 4 passed (5)` — `AssertionError: expected [] to match object [ { level: 50, …(2) } ]`
- **Code:** in both `autoCheckOut`s (`visits`, `subscriptions`), each stay's transaction is caught, logged as
  `{ err, job, stayId }` with `'stay not closed'`, and counted. After the loop, the run throws when anything failed,
  so the job is logged as failed and the endpoint answers 500. Both services now take `logger` (wired in `app.ts`).
  - The `!rules` branch is now real: `spaceSettings.settingsFor` leaves out a space without its row, and each of
    that space's stays is logged and counted as not closed. Simply deleting the branch was not possible: lint
    forbids the `!` assertion it would need.
- **Green:** `jobs.api.test.ts` + `visits/autoCheckOut.api.test.ts` → `Test Files  2 passed (2)`, `Tests  14 passed (14)`.
- **Breaks** (`scripts\brk.py scripts\pr4\c0a.json`; each restored, SHA-256 ok):
  - C0a-1, the per-stay catch removed → `Tests  1 failed | 4 passed (5)` — `expected [] to match object [ { level: 50, …(2) } ]`
  - C0a-2, a space without settings skipped silently → `Tests  1 failed | 4 passed (5)` — `expected 200 to be 500`
- Not tested on its own: the `subscriptions` loop's catch. No check-in can be made to fail its closing: it writes
  only a time, and no check refuses that time. It is the same code as the visits' loop.
- **Documents in this commit** (carried items 3, 4, 5 and 7):
  - item 3: `visits.md`'s *Leaves* now says "the check-out's transaction, the space's lock and the check-out's
    typed-price decision". *How it composes* now says that `visits` runs its own transactions for the auto
    check-out and the pricing.
  - item 4: conventions §12's *Scheduler* row has the 5-minute / 10-second detail in the *Locally* cell only.
    `.env.example`'s comment now reads "The API's own server runs the jobs every 5 minutes either way; without
    it, the endpoint is not mounted."
  - item 5: setup's runbook says the header must be written exactly (`Bearer`, one space, the secret).
  - item 1's own documents: the contract's *Internal* `Errors` line; a line in `visits.md`'s decision; a line in
    `space-settings.md`'s P2 (`settingsFor` leaves a space without its row out).
  - item 7: findings **111** (#95's nit 7, *present* counted twice), **112** (#95's nit 8, a key that closed a
    visit with no payment is not remembered) and **113** (#97's review 7, the uncollected read grows), each a
    file plus its index line under *Open*.
- `npm run lint` → exit 0 · `npm run typecheck` → exit 0 · `check:links` → `2437 links in 151 documents and 1426
  source files all resolve.`
- **Commit:** `31bcea72 fix(jobs): keep closing stays past a failing one` (48)

### Item 2: every stay closes by its day's end (the owner's choice (b), widened)

- **Tests**, in `spaces/autoCheckout.unit.test.ts`:
  - `is due at 23:59 of its check-in's day when the closing check-out is off and there is no stay limit`
    (replaces the old "is never due…" test);
  - `a stay limit never carries a stay into the next day` (23 h from 20:00).
- **Red first:** `Tests  2 failed | 7 passed (9)` — `AssertionError: expected null to deeply equal
  2026-10-18T20:59:00.000Z`; `expected 2026-10-19T16:00:00.000Z to deeply equal 2026-10-18T20:59:00.000Z`
- **Code:** `autoCheckoutDue` takes one `Math.min` over 23:59 of the check-in's Gaza day (always), the closing
  (when on) and the stay limit (when set). It returns `Date` and is never `null`; the callers' `dueAt &&` is gone.
  The `LAST_MINUTE` comment is corrected.
- **Green:** unit `Tests  9 passed (9)`. The API files `visits/autoCheckOut` + `jobs` → `Tests  14 passed (14)`.
- **Breaks, one per branch** (`scripts\pr4\c0b.json`; each restored, SHA ok):
  - C0b-1, the 23:59 bound dropped → `Tests  2 failed | 7 passed (9)` — `expected Invalid Date to deeply equal …20:59…`
  - C0b-2, the closing dropped → `Tests  2 failed | 7 passed (9)` — `expected …20:59… to deeply equal …15:00…`
  - C0b-3, the stay limit dropped → `Tests  2 failed | 7 passed (9)` — `expected …15:00… to deeply equal …08:50…`
- **Documents:** data model *Auto check-out* (the bound, `#PRNUM`); the contract's `maxStayMinutes` line and its
  comment ("at closing, or 23:59").
- **#95's nit 9 is resolved:** a charge is now bounded by one day's stay (24 h × `PRICE_MAX_AGOROT` < 2³¹). The
  commit body says so.
- `npm run lint` → exit 0 · `npm run typecheck` → exit 0
- **Commit:** `d40e857d fix(visits): close every stay by its day's end` (46)
- Item 6 (`v1-mvp.md` step 7 *Built*) is reworded by the plan's C2–C4, as the item says ("as it lands").

## C1 — `dd5b6004 feat(visits): store a visit's write-off` (39)

- **Schema:** `Visit.writtenOffAt`, `writtenOffById` (`VisitWrittenOffBy` → `User`, `Restrict`), `writeOffReason`, each with
  a `///` line; `User.visitsWrittenOff`. `prisma format` was run once but also realigned the unrelated `User` and
  `SpaceSettings` blocks (main is not formatted), so the schema was rewritten from `HEAD` and edited by hand. The
  diff is `Visit` plus one `User` line; `prisma validate` → valid.
- **§12.2 check 1, the migration, created once:** `prisma migrate dev --create-only --name visit_write_off` run
  **once** → `20261020124728_visit_write_off` (listed). Prisma's `ADD COLUMN` ×3 and `AddForeignKey` were kept. Then
  appended: the raw-SQL header, D2's `visits_write_off_check`, and `CREATE OR REPLACE FUNCTION
  "payments_guard_insert"()` copied whole from `desk_visit_charge`. A `diff` against that function shows only the
  three planned changes: `written_off boolean;`, the `SELECT … "written_off_at" IS NOT NULL INTO due, written_off`
  (split over two lines), and the `IF written_off THEN RAISE … payments_visit_written_off` block with its comment.
  No data-loss refusal happened.
  - `npm run db:migrate` → `Your database is now in sync with your schema.` (`masaha_b_dev`). It did **not**
    regenerate the client (`Visit.ts` named `writtenOffAt` 0 times), so `npx prisma generate` was run after it →
    `Generated Prisma Client (7.10.0)`; `Visit.ts` then names it 66 times.
  - The function on both databases: `prosrc LIKE '%payments_visit_written_off%'` → `t` on `masaha_b_dev` and `t` on
    `masaha_b_test` (migrated by the API lane's global setup).
- **D1** (`db/front-desk.api.test.ts`) and **D2** (`db/payments.api.test.ts`) were written after the migration was
  applied (check 1 comes right after the schema edit), so they passed at once: `Tests  38 passed (38)`. **Their
  red is the database breaks** (a departure, stated):
  - **B5** (`scripts\pr4\dbbreak.sh`: `DROP CONSTRAINT visits_write_off_check` on `masaha_b_test`) → `Tests  1
    failed | 21 passed (22)` — `AssertionError: promise resolved "{ id: 1, spaceId: 1, …(22) }" instead of
    rejecting`. Restored with D2's `ADD CONSTRAINT` → `Tests  22 passed (22)`; the constraint count is 1.
  - **B6** (`desk_visit_charge`'s function on `masaha_b_test`) → `Tests  1 failed | 15 passed (16)` — `promise
    resolved "{ id: 1, spaceId: 1, …(12) }" instead of rejecting`. Restored with the new function → `Tests  16
    passed (16)`; `prosrc LIKE …` → `t`. (B6 on T22 is run at C3.)
- **§12.2 check 4, the exact-key tests:** after `DeskVisit.writeOff` and the mapper, the `desk`, `visits`,
  `payments` and `db/seed` API files ran red with `Tests  5 failed | 62 passed (67)`. The five whole-visit
  `toEqual`s are in `checkIn` (the check-in's answer), `checkOut` (the paid check-out), `uncollected` (the listed
  visit), `unpriced` (the listed visit) and `visits` (the quoted visit). Each gained `writeOff: null` by hand and
  nothing else → `Tests  67 passed (67)`. Each `toMatchObject` was left as it was.
- **Documents:** the data model (*Visit*, *Constraints*: the `CHECK` and the ledger's bullet), conventions §13 ("four
  rules"), the contract's `DeskVisit`, `payments.md` (*Owns*, the S1 decision), `visits.md` (*Owns*, *API
  history*).
- `npm run lint` → exit 0 · `npm run typecheck` → exit 0
- Free memory before the focused runs: 4,734,208 KB; none of worker A's `vitest`/`tsc` running.

## C2 — `e0377cc8 feat(desk): write a visit off, and undo it` (42)

- **Tests:** U1 (`can.unit.test.ts`, `'visits.writeOff': OWNER_ONLY`); U2 (`visits/requests.unit.test.ts`); T1–T12
  (`desk/writeOff.api.test.ts`, new); T34 (`payments/uncollected.api.test.ts`).
- **Red first:**
  - U1 → `Tests  14 failed | 378 passed (392)` — `expected undefined to be true`, `expected undefined to be false`, and
    the actions list one short.
  - U2 → `Tests  1 failed | 2 passed (3)` — `TypeError: Cannot read properties of undefined (reading 'parse')`.
  - T1–T12 + T34 → `Tests  13 failed | 4 passed (17)`: `expected 404 to be 200` and similar ×11; `Error: 1 request(s)
    never waited on a lock` ×2 (T5, T9: no route yet); T34 `expected [ 1, 2 ] to deeply equal [ 1 ]`.
- **Code:** `writeOffVisitSchema` (`WRITE_OFF_REASON_MAX_LENGTH = 200`); `VISIT_ALREADY_PAID` (via `add-error-code`:
  `core/errors.ts`, both catalogues, contract §6, T6 provokes it); `VISIT_NOT_PRICED`'s two lines revised as approved;
  `'visits.writeOff': 'owner'`; `visits.repository` `writeOff` / `undoWriteOff`, and `writtenOffAt: null` in
  `autoClosedIn` and `autoClosedPage` (D6); `visits.service` `writeOff` / `undoWriteOff` (audited); `paidFor` takes
  `tx = prisma` (check 8); `payments.balanceOfVisit`; `desk` `lockAtDesk(…, action)`, `lockClosed`,
  `writeOffVisit`, `undoWriteOff`; the controller and the two routes.
- **Green:** U1 `Tests  392 passed (392)`; U2 `Tests  3 passed (3)`; API `Test Files  2 passed (2)`, `Tests  17 passed (17)`.
- **Breaks** (`scripts\pr4\c2.json`, output `c2.out`; each restored, SHA ok), every one RED:
  - B1 `'staff'` → `Tests  3 failed | 389 passed (392)` — `expected true to be false` (×3)
  - B2 `z.string()` → `Tests  1 failed | 2 passed (3)` — `expected { reason: '  Left without paying ' } to deeply equal …`
  - B7 `writtenOffAt` dropped from `autoClosedPage` → `Tests  2 failed | 15 passed (17)` — T1 `expected [ 1 ] to deeply
    equal []`; T34 `expected [ 1, 2 ] to deeply equal [ 1 ]`
  - B8 the balance taken as the charge → `Tests  3 failed | 9 passed (12)` — T2's and T9's audited amount; T6 `expected
    200 to be 409`
  - B9 refused unless `AUTO` → `Tests  1 failed | 11 passed (12)` — `expected 409 to be 200`
  - B10 the route's `requireCan` removed → `Tests  1 failed | 11 passed (12)` — `expected 422 to be 403`
  - B11 `can()` on `space.links` → `Tests  1 failed | 11 passed (12)` — `expected 200 to be 403`
  - B12 the no-charge check removed → `Tests  1 failed | 11 passed (12)` — `expected 'VISIT_ALREADY_PAID' to be
    'VISIT_NOT_PRICED'` (the plan expected a 500 from the `CHECK`; here the null balance reaches the "nothing owed"
    refusal first, and the test is red either way)
  - B13 the balance check removed → `Tests  2 failed | 10 passed (12)` — `expected 200 to be 409` ×2
  - B14 the already-written-off branch removed → `Tests  1 failed | 11 passed (12)` — T7 `… to match object { Object
    (writeOff) }`
  - B15 `validate` removed → `Tests  1 failed | 11 passed (12)` — `expected 500 to be 422`
  - B16 the balance read before the space's lock → `Tests  2 failed | 10 passed (12)` — T9 `expected 500 to be 409` and
    the partial write-off's amount
  - B17 the undo audits but does not clear → `Tests  1 failed | 11 passed (12)` — `… to match object { id: 1, writeOff:
    null }`
  - B18 the not-written-off branch removed → `Tests  1 failed | 11 passed (12)` — `expected 500 to be 200` (the plan
    expected "an audit is written"; without the branch the undo reads a null write-off and fails, red either way)
  - T12 has no break of its own; B1 covers it, as the plan says.
- **Documents:** the contract (intro, the two routes, `UncollectedVisit`'s line, §6); the data model (*Written-off visit*,
  *Uncollected visits*, *Customer debt*); conventions §9; security's *Authorization*; ADR 0009's row and *Revised* line;
  `desk.md` (what it does, the device line moved to "the desk's screen item", the flow, three decisions, history);
  `payments.md`; `visits.md`; **finding 110** (file + index under *Open*). `check:links` → `2441 links in 152
  documents and 1428 source files all resolve.`
- `npm run lint` → exit 0 · `npm run typecheck` → exit 0
- **Departures:**
  - The plan's `balancesOf(space.id, [{ id, chargeAgorot }], tx)` is built as `balanceOfVisit(space.id, { id,
    chargeAgorot }, tx)` → `{ paidAgorot, balanceAgorot }`. Each caller has one visit, and reading one entry back
    from a map would need a `!`, which lint forbids. It is built in C2, not C3, because the write-off needs it first.
  - `v1-mvp.md` (Appendix A item 9) and `overview.md` are edited once, in C4, when all three routes exist.

## C3 — `feat(desk): receive a payment for a visit` (41)

- **Tests:** U3 (`desk/requests.unit.test.ts`); T13–T25 (`desk/payments.api.test.ts`, new); T26 (`desk/checkOut.api.test.ts`).
- **Red first:**
  - U3 → `Tests  1 failed | 1 passed (2)` — `TypeError: Cannot read properties of undefined (reading 'parse')`.
  - API → `Tests  14 failed | 20 passed (34)`: T26 `expected 200 to be 409`; T13–T19, T24, T25 `expected 404 to be …`
    (no route yet); T20 `Error: 2 request(s) never waited on a lock`; T21–T23 `Error: 1 request(s) never waited on a
    lock`.
- **Code:** `receivePaymentSchema` (its own local `id`, as each shared module writes it: check 5); `ReceivedPayment`;
  `VISIT_WRITTEN_OFF` and `VISIT_HAS_CUSTOMER` (via `add-error-code`); the `CONSTRAINT_CODES` line; `visits.leaveTo`
  (audited `visit.leftToCustomer`); `desk` `customerFor` (finding 100, used by the check-out and the payment),
  `receivePayment`, its controller and its route (`requireCan('payments.record')`, `requireIdempotencyKey`,
  `validate`).
- **Green:** the `desk` API files → `Test Files  4 passed (4)`, `Tests  56 passed (56)`; shared desk → `Tests  2 passed (2)`.
- **§12.2 checks 2 and 3:** T17 answers `VISIT_WRITTEN_OFF` through `checkViolationOf` (no 500). T13 and T22 pass
  with the service's `lockIn` and the trigger's `FOR UPDATE` in one transaction (no wait, no deadlock).
- **Departure:** `customerFor` does not look the phone up for a visit that has a customer. It compares the phone
  with that customer's own (`visit.customer.phone`, stored in E.164 as `phoneSchema` normalises). This gives the
  same answer as the plan's lookup, except when the visit's customer was archived and the same number was reused:
  the plan's lookup would refuse, while this keeps the visit's own customer. It needs no new read in `customers`,
  a module outside §7's file list.
- **Breaks** (`scripts\pr4\c3.json`, output `c3.out`; each restored, SHA ok), every one RED:
  - B3 `visitId` optional → `Tests  1 failed | 1 passed (2)` — `expected null to deeply equal { visitId: [ 'required' ] }`
  - B19 `balanceAgorot` read before the insert → `Tests  7 failed | 6 passed (13)` — T13 `expected 422 to be 201` and others
  - B20 the phone rule skipped → `Tests  2 failed | 11 passed (13)` — `expected 201 to be 422`; `expected 201 to be 409`
  - B21 the phone's customer written over the visit's → `Tests  2 failed | 32 passed (34)` — T26 `expected 200 to
    be 409`; T16 `expected 201 to be 409`
  - B22 the phone rule before the insert → `Tests  7 failed | 6 passed (13)` — T17 `expected 422 to be 409`, …
  - B23 the `CONSTRAINT_CODES` line removed → `Tests  2 failed | 11 passed (13)` — T17 and T22 `expected 500 to be 409`
  - B24 the open check removed → `Tests  1 failed | 12 passed (13)` — `expected 'VISIT_NOT_PRICED' to be undefined`
  - B25 `findByKey` removed → `Tests  2 failed | 11 passed (13)` — `expected 500 to be 201`; `expected [ 500, 201 ] to
    deeply equal [ 201, 201 ]`
  - B26 the space's lock removed for this route → `Tests  4 failed | 9 passed (13)` — `Error: 2 request(s) never
    waited on a lock` (T20), and T21–T23 the same with 1
  - B27 the balance read before the lock → `Tests  2 failed | 11 passed (13)` — T21 `expected 422 to be 201`; T22
    `expected 500 to be 409`
  - B28 `can()` on `space.links` → `Tests  1 failed | 12 passed (13)` — `expected 201 to be 403`
  - B29 `requireCan('visits.writeOff')` on the route → `Tests  12 failed | 1 passed (13)` — `expected 403 to be 201`, …
  - B30 `requireIdempotencyKey` removed → `Tests  12 failed | 1 passed (13)` — `expected 500 to be 422`, …
  - B31 the check-out's own `findOrCreateByPhone` restored → `Tests  1 failed | 20 passed (21)` — T26 `expected 200 to
    be 409`
  - **B6 on T22** (`dbbreak.sh`, `desk_visit_charge`'s function on `masaha_b_test`) → `Tests  2 failed | 11 passed
    (13)` — T22 `expected 201 to be 409`; T17 `expected 422 to be 409`. Restored → `Tests  13 passed (13)`; `prosrc
    LIKE …` → `t`.
- **Documents:** the contract (§1's *Built for*, the intro, the check-out's unpaid rule and errors, `POST …/payments`
  with `ReceivedPayment`, §6); the data model (*Unpaid visit*, *Checked by the service*); conventions (header, §9);
  security; `desk.md` (what it does, the unpaid-part rule, the payment's flow and lock order, four decisions, code
  map, history); `payments.md`; **finding 100 resolved** (status, resolution line, its index line moved to
  *Resolved*); `docs/README.md`'s map lines for `desk.md` and `payments.md` (check 9: they list what is built).
- **Lint and typecheck of the commit:** the first run after committing gave `lint=1 typecheck=2`, because the working
  tree already held C4's tests (`debt.api.test.ts`, U4), which name code not yet written. With those set aside, the
  committed tree gives `npm run lint` → exit 0 and `npm run typecheck` → exit 0. Both files were then put back.
- **Commit:** `44d2dbe7 feat(desk): receive a payment for a visit` (41)

## C4 — `d48accf5 feat(desk): leave a visit's debt to a customer` (46)

- **Tests:** U4 (`desk/requests.unit.test.ts`); T27–T33 (`desk/debt.api.test.ts`, new).
- **Red first:** U4 → `Tests  1 failed | 2 passed (3)` — `TypeError: Cannot read properties of undefined (reading
  'parse')`. API → `Tests  7 failed (7)`: `expected 404 to be 200` and similar ×6; `Error: 1 request(s) never waited on
  a lock` (T33).
- **Code:** `leaveToCustomerSchema`; `desk.leaveToCustomer` (D4's order, through `lockClosed`, `balanceOf` and
  `customerFor`); its controller and route (`requireCan('payments.record')`, `validate`).
- **Green:** the `desk` API files → `Tests  63 passed (63)`; shared desk → `Tests  3 passed (3)`.
- **Breaks** (`scripts\pr4\c4.json`, `c4.out`; each restored, SHA ok), every one RED:
  - B4 `phone` optional → `Tests  1 failed | 2 passed (3)` — `expected null to deeply equal { phone: [ 'required' ] }`
  - B32 `visits.leaveTo` not called → `Tests  3 failed | 4 passed (7)` — `… to match object { id: 1, customer: … }`
  - B33 a no-charge refusal added → `Tests  1 failed | 6 passed (7)` — T28 `expected 409 to be 200`
  - B34 the same-customer branch removed → `Tests  1 failed | 6 passed (7)` — T29: a second audit entry
  - B35 the written-off check removed → `Tests  1 failed | 6 passed (7)` — `expected 200 to be 409`
  - B36 the balance check removed → `Tests  1 failed | 6 passed (7)` — `expected 200 to be 409`
  - B37 `validate` removed → `Tests  2 failed | 5 passed (7)` — `expected 500 to be 422`
  - B38 `can()` on `space.links` → `Tests  1 failed | 6 passed (7)` — `expected 200 to be 403`
  - B39 the visit read without its lock, before the space's → `Tests  3 failed | 4 passed (7)` — T33 `expected 200 to
    be 409`, …
- **Documents:** the contract (`PUT …/customer`, §6's glosses); the data model (*Unpaid visit*); conventions §9;
  security; `desk.md`; `visits.md`; `docs/README.md`; `v1-mvp.md` (step 7's *Goal* and *Built*, which is carried item 6;
  step 9's *Goal*; the route table's payments row; the managed *Built* sentence and its access line); `overview.md`.
- `npm run lint` → exit 0
- **Commit:** `d48accf5 feat(desk): leave a visit's debt to a customer` (46)
