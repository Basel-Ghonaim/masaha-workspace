# SUBSCRIPTIONS PR 1 (`feat/customers`) — the executor's report

Written as the work goes. Executor: Claude Code, in `C:\dev\masaha\app-b`.

## 12.1 Before the branch (2026-10-21)

- `gh pr view 100 --json state` → `MERGED`, merge commit `5d42a527`. ✔
- `git status --short --branch` → clean, detached at `5d42a527` (= `origin/main`). ✔
- `git diff --name-status abc28e73 origin/main`: DESK PR 4's files (its carried commits `495623c7`, `6172ac5b`
  and C1–C4), worker A's #98 (`apps/web` packages, spaces, copy; docs). No other change to a code file of §7. ✔
- Open PRs: #99 `feat/owner-staff-settings` (worker A) — `apps/web/src/pages/dashboard/**` and
  `apps/web/src/features/**` only; no shared document, no `errors.ts`. ✔
- `0_CARRIED_FROM_100.md` read whole, and the review it cites (`DESK\6_REVIEW_PR4_CLAUDE_CODE.md`).
- **DESK PR 4's merged payment route re-read against the plan:** `receivePaymentSchema` (`visitId` required, `phone`,
  `customerName`), `ReceivedPayment { visit, payment, paidAgorot, balanceAgorot }`, `lockAtDesk(actor, space, tx,
  action = 'attendance.record')`, `payments.balanceOfVisit(spaceId, { id, chargeAgorot }, tx)` and
  `repository.paidFor(spaceId, ids, tx = prisma)`, `customerFor`, `visits.writtenOffAt` and `autoClosedIn` /
  `autoClosedPage` filtering `writtenOffAt: null`; findings index: 110–113 under *Open*, 111–113 at the plan's
  expected numbers. No difference the plan does not cover. ✔
- `apps/api/.env`: `PORT=3321`, `masaha_b_dev`, `masaha_b_test` (by pattern, credentials masked). ✔

## Branch

- `git switch --no-track -c feat/customers origin/main` → done.
- `docker start masaha-postgres-1` → **failed**: `failed to connect to the docker API at
  npipe:////./pipe/dockerDesktopLinuxEngine … The system cannot find the file specified.` Docker Desktop is not
  running. **Stopped here, asking the owner to start Docker Desktop** (exec prompt §1.8).
- **Resumed 2026-10-21** after the owner started Docker Desktop: `docker start masaha-postgres-1` ✔;
  `npm run build -w @masaha/shared` → exit 0; `prisma generate` → `✔ Generated Prisma Client (7.10.0)`;
  `prisma migrate status` → `21 migrations found … Database schema is up to date!` (`masaha_b_dev`).

## Carried from #100

Breaks tool: `scripts\brk.py` (backup into `scripts\breaks\`, edit, run the test file, restore from the backup,
SHA-256 compared, run green); entries in `scripts\c0.json`.

### Item 1 — the jobs answer 200 with a `failed` count (finding 114) — commit `3bf44d7b`
`fix(jobs): answer 200 when only stays failed` (44)
- **Red first** (`vitest run --project api src/shared/jobs/jobs.api.test.ts`, the tests edited, code not yet):
  `Tests  3 failed | 2 passed (5)` — `expected { …(2) } to deeply equal { …(2) }` (the `failed: 0` count) and
  `expected 500 to be 200` twice.
- **Green** after the code: `Tests  5 passed (5)`; `autoCheckOut.api.test.ts` (its exact `done` counts gain
  `failed: 0`, by hand) `Tests  9 passed (9)`; the new `jobs.unit.test.ts` `Tests  2 passed (2)`.
- **Breaks:** C0-1a (`visits.service.ts`: `if (failed > 0) throw` put back) → red: `Tests  2 failed | 3 passed (5)`,
  `expected 500 to be 200`; restored, sha256 same, `Tests  5 passed (5)`. C0-1b (`jobs.ts`: `failed: false`) → red:
  `Tests  1 failed | 1 passed (2)`, `a job that throws fails the run …`; restored, sha256 same, `Tests  2 passed (2)`.
- **How "a job that throws answers 500" is proven:** no job can be made to throw through the real app without
  test-only code (each job's reads are plain queries; a space without settings is now a stay's failure). So the
  unit that decides `failed` — `createJobs`, whose jobs are its injected dependency — is unit-tested (a job that
  throws → `failed: true`, logged `job failed`; a job with failed stays → `failed: false`); the router's
  `if (failed) throw AppError.server` is unchanged. The former API test "a failing job answers 500" (a space
  without settings) now proves that case answers 200 with `failed: 1` and the other job still closed its stay.
- `lint` exit 0 · `typecheck` exit 0 (the tree before a Prettier-only fix of `autoCheckOut.api.test.ts`).
- Documents: contract *Internal* (200 with `failed`; 500 only when a job threw), `setup.md`'s runbook (read
  `stay not closed`), `visits.md` (decision + history), finding 114 (Resolved) + index.

### Item 2 — a desk check-out charged up to the stay's day's end (finding 116) — commit `e50f2b93`
`fix(desk): charge a stay up to its day's end` (44)
- **Decided here (the carried file asked to recommend one): `checkedOutAt` records the stay's end — the earlier of
  the quote's time and the due time.** Why: the record's times then agree with its charge and with what the auto
  check-out would have recorded (a stay never crosses into the next day, as data); the audit's `requestedAt` keeps
  when the desk closed it.
- **Wider than the check-out alone, stated:** the quote (`GET …/visits/:visitId`) and the charges so far (the
  occupancy read's `chargeNowAgorot`) stop at the due time too, by the same helper (`visits.stayEnd`), so the desk
  shows what it will charge (#95's "the desk shows a price and charges exactly that price"). Two files' worth; not
  larger than the item, so not asked.
- **Red first:** `checkOut.api.test.ts -t "next morning"` → `expected 422 to be 200` (the uncapped charge 2,500 left
  1,000 unpaid, so a phone was required); `visits.api.test.ts` (the quote) → `expected { Object (at, chargeAgorot,
  ...) } to deeply equal …`; `present.api.test.ts` → `expected [ { id: 1, chargeNowAgorot: 2500 } ] to deeply equal
  [ { id: 1, chargeNowAgorot: 1500 } ]`.
- **Green:** `checkOut.api.test.ts` `Tests  22 passed (22)`; `visits.api.test.ts` `Tests  4 passed (4)`;
  `present.api.test.ts` `Tests  9 passed (9)`; `autoCheckOut.api.test.ts` `Tests  9 passed (9)`.
- **Breaks:** C0-2a (desk: `checkedOutAt = pricedTo`) → `expected 422 to be 200`; C0-2b (quote uncapped) →
  `Tests  1 failed | 3 passed (4)`; C0-2c (charges so far uncapped) → `chargeNowAgorot: 2500` vs `1500`. Each
  restored, sha256 same, green.
- `lint` exit 0 · `typecheck` exit 0 · Prettier clean.
- Documents: data model (*Auto check-out*, *Visit charge*), contract (check-out 200, quote, people's charge so far),
  `desk.md` (check-out paragraph, decision, history), `visits.md` (check-out, reads, history), finding 116 (Resolved)
  + index.

### Items 3 and 4 — finding 115 recorded; the documents — commit `85429d10`
`docs(desk): say what the debts' PR built` (40)
- Finding 115 (*Open*): a write-off and its undo carry no key; accepted for v1, the desk's screen item must not retry
  these two routes automatically; `desk.md`'s write-off decision links it.
- `payments.md`: "a check-out's or a payment's key"; the `#100` history line (the fourth rule, `balanceOfVisit`,
  `paidFor` in the caller's transaction, the payment after the check-out). `visits.md`: *Leaves* and *How it
  composes* name the desk's transactions (check-in, check-out, write-off and its undo, `leaveTo`). Conventions §13:
  the rules listed with the uncharged rule named, "The ceiling locks the item's row".
- `check:links` → `2462 links in 156 documents and 1462 source files all resolve.`

### Item 5 — the review's other nits — commit `2e9dee61`
`test(desk): prove the undo's refusals` (37)
- **Nit 7, done** (`writeOff.api.test.ts`, small): the undo's `not_found` for a stranger, another space's owner,
  the admin and another space's visit; 403 for an owner whose link ended while it waited (`whileHeld`). Tests of
  code that exists, so proven by breaks: C0-7a (`visits.repository.ts` `lockIn` without its space) → `expected 200
  to be 404`; C0-7b (the managed boundary admitting anyone) → `expected 403 to be 404`; C0-7c (`lockAtDesk`'s `can()`
  on `space.links`) → `expected 200 to be 403`. Each restored, sha256 same, green; the file `Tests  14 passed (14)`.
- **Nit 6 — no change:** the review judged it acceptable (the answer names the visit's own customer); it is for the
  desk's screen item's brief — noted here for the supervisor.
- **Nit 8 — no change:** the review judged it follows from the owner's choice "always"; nothing to fix.
- `lint` exit 0 · `typecheck` exit 0.
- #100's PR description (review finding 5) stays as merged; the four departures it omitted are, from #100's report:
  the schema edited by hand after `prisma format` realigned unrelated blocks; D1 and D2 written after the migration,
  so their red came only through B5 and B6; B12's and B18's red differing from the plan's expectation; the PR-number
  fix (`#99` → `#100`) by `filter-branch`.

## PR 1 — C1 `feat(customers): create and edit a customer`

### §12.2 check 1 — migration `customer_key`
- Schema: `Customer.idempotencyKey String? @map("request_id") @db.Uuid`, `@@unique([spaceId, idempotencyKey])`; the
  Customer block realigned by hand (no `prisma format`); `prisma validate` → valid.
- `prisma migrate dev --create-only --name customer_key` → **refused, nothing created**: `Error: Prisma Migrate has
  detected that the environment is non-interactive, which is not supported.` (from Git Bash and from PowerShell
  alike; this harness has no TTY: `process.stdin.isTTY` undefined). `ls` of the folder unchanged after each.
- **Departure (the plan's own fallback, §12.2 check 1):** `prisma migrate diff --from-config-datasource --to-schema
  prisma/schema.prisma --script` (read-only; `masaha_b_dev` was up to date with every migration) → exactly `ALTER TABLE
  "customers" ADD COLUMN "request_id" UUID;` and `CREATE UNIQUE INDEX "customers_space_id_request_id_key" …`, written
  into a hand-made `20261021074423_customer_key/migration.sql` (UTC timestamp). Created once.
- `npm run db:migrate` → `Your database is now in sync with your schema.` (`masaha_b_dev`); `prisma generate` →
  `✔ Generated Prisma Client (7.10.0)`; `prisma migrate status` → `Database schema is up to date!`.

### C1 committed — `5150d3df` `feat(customers): create and edit a customer` (43)
- **Red first:** U6 (`packages/shared … src/customers/requests.unit.test.ts`) → `Cannot find module './requests.ts'`
  (the code not written: the plan's red step); U3 → `Cannot find module './customerSearch.ts'`; T1–T9
  (`customers.api.test.ts`, the routes not yet mounted) → `Tests  9 failed | 1 passed (10)` (the 1: T8's not_found,
  true before the routes exist — proven by its break below).
- **Green:** U6 `Tests  3 passed (3)`; U3 `Tests  2 passed (2)`; `customers.api.test.ts` `Tests  10 passed (10)`;
  desk + occupancy files (the phone flow uses the repository) `Test Files  8 passed (8)`, `Tests  95 passed (95)`.
- **Breaks** (`scripts\c1.json`), each restored from its backup, sha256 same, green after:
  - B3 (`\d{1,}`) → `expected { phoneDigits: '5' } to deeply equal { name: '5' }`.
  - B11 (edit's phone without `.nullable()`) → `ZodError` in *null clears the phone*.
  - B18 (create's audit skipped) → `expected [] to deeply equal [ { actorId: 2, …(6) }, …(1) ]`.
  - B19 (`findByPhone` without `archivedAt: null`) → `expected 409 to be 201`.
  - B20 (the phone check skipped) → `expected 500 to be 409` (the unique index aborts the transaction).
  - B21 (`findByKey` skipped) → `expected [ 201, 409 ] to deeply equal [ 201, 201 ]`.
  - B22 (the create without the space's lock) → `Error: 2 request(s) never waited on a lock`.
  - B23 (`requireIdempotencyKey` removed) → `expected { name: [ 'too_short' ] } to deeply equal { idempotencyKey:
    [ 'required' ] }`.
  - B24 (the no-change check removed) → an extra `customer.edited` entry (`…(2)` vs `…(1)`).
  - **B25 stayed green — departure:** the router mounted outside `manage` cannot change a stranger's answer:
    `spaceOf(req)` (read by `requireCan`) itself answers `not_found` when no space is loaded. The plan's exception
    applies (the break cannot change the outcome); the break that can, **B25b**: mounted behind `loadSpaceLinks`
    (links loaded, no refusal) → `expected 403 to be 404`. Red seen.
  - B26 (`can()` on `space.links`) → `expected 201 to be 403`.
- `lint` exit 0 · `typecheck` exit 0 · Prettier clean · `check:links` → `2482 links in 157 documents and 1474 source
  files all resolve.`
- **Small additions, stated:** `customers/customerChange.ts` (pure, as `packageChange`) — not in §7's list; the
  edit's "only what changed" lives there.
- Documents: contract (§1 key line; new *Customers (managed)*: fields, `Customer`, the create and the edit, audit),
  data model (*Idempotency*, the key's constraint line), conventions §13, security (header *Built*, the boundary
  line), `customers.md` (new), `docs/README.md` (map line).

## C2 committed — `3e33f39b` `feat(customers): archive and restore a customer` (47)
- **Red first:** U8 (the `customers.archive` row added to `can.unit.test.ts`'s table) → `Tests  14 failed | 391
  passed (405)`; T10 (restore, in `customers.api.test.ts`) and T11–T15 (`desk/archive.api.test.ts`) → `Tests  7 failed
  | 10 passed (17)`.
- **Green:** `can.unit.test.ts` `Tests  405 passed (405)`; the two API files `Tests  17 passed (17)`.
- **T10 made observable, stated:** without the route's `requireCan`, the restore's service `can()` still answers 403,
  so B27 could not turn a plain 403 check red. T10's reception refusal is now asserted while the test holds the
  space's lock (answered 403 at once, before the service reads).
- **Breaks** (`scripts\c2.json`), each restored, sha256 same, green:
  - B13 (`'customers.archive': 'staff'`) → U8 `Tests  3 failed | 402 passed (405)`, `expected true to be false`; and
    in the API lane (T13, covered by B13) → `expected 404 to be 403`.
  - B27 (the restore route's `requireCan` removed) → the request waited on the lock: `Transaction API error: A
    commit cannot be executed on an expired transaction … 3000 ms`.
  - B10x (extra: the restore's phone check skipped) → `expected 500 to be 409`.
  - B28 (the archive's "already" branch removed) → a second `customer.archived` entry.
  - B29 (the present check removed) → `expected 200 to be 409`.
  - B30 (the edit's archived check removed) → `expected 200 to be 409`.
  - B31 (`lockAtDesk`'s `can()` on `space.links`) → `expected 200 to be 403`.
- `lint` exit 0 · `typecheck` exit 0 · Prettier clean · `check:links` → `2487 links … all resolve.`
- **New error code** `CUSTOMER_ARCHIVED` (409): shared, both catalogues — EN "This customer is archived; the owner
  restores them first." AR «هذا الزبون مؤرشف؛ يسترجعه المالك أولًا.» (§13 Q2 word for word) — contract §6 (+
  `PHONE_TAKEN`'s and `MEMBER_ALREADY_CHECKED_IN`'s glosses).
- **Departure, stated:** the archive's *present* check reads the space's open check-ins and open visits
  (`subscriptions.openCheckInsIn`, `visits.openIn`, both existing, bounded by who is present) instead of new
  `openCheckInOf` / `openOf` helpers; `desk` gains `subscriptions` as a dependency here (the plan: C5). PR 3's D12
  replaces it with `occupancy.isPresent`.
- Documents: ADR 0009 (two rows + *Revised*), security, contract (archive and restore routes, *Archived, never
  deleted*, audit names), `customers.md`, `desk.md`.

## C3 committed — `d2b744c7` `feat(subscriptions): derive status and progress` (47)
- **§12.2 check 1 (the function's migration):** `prisma migrate dev` cannot run here (no TTY, as for C1); the plan's
  fallback for an empty migration: the folder `20261021082345_subscription_usage` made by hand, D3's SQL under a
  raw-SQL header. `npm run db:migrate` → `Your database is now in sync with your schema.`; the first API run's global
  setup → `Applying migration 20261021082345_subscription_usage … All migrations have been successfully applied.`
  (`masaha_b_test`).
- **Check 2:** `SELECT count(*) FROM subscription_usage(1, NULL, current_date, current_date)` → `4` on `masaha_b_dev`,
  `2` on `masaha_b_test`. **Check 3:** `masaha_search_text` present on `masaha_b_test`. ✔
- **Red first:** U1/U2 → `addDays is not a function`, `weekStartOf is not a function`, `Cannot read properties of
  undefined (reading 'parse')` (`Tests  3 failed | 25 passed (28)`); U4/U5 → `Cannot find module` (not written).
  **Departure:** D1–D4 were written after the migration had been applied, so their red is the database breaks'.
- **Green:** shared core `Tests  28 passed (28)` (after a typing fix of U2, `23` in `fields`); `subscriptions` unit
  `Tests  13 passed (13)`; `db/subscriptions.api.test.ts` `Tests  14 passed (14)`.
- **Breaks:** B1 (week from Sunday) red; B2 (any `YYYY-MM-DD`; re-run after U2's fix) red; B4 (ended branch gone), B5
  (upcoming before ended), B6 (no end check), B7 (total days), B7h (total hours), B8 (no short-subscription rule),
  B8b (`<` for `≤` 7 days), B9 (`<` for `≤` 20 %), B10 (by id only) — each red, restored, sha256 same, green.
  **Database** (`scripts\dbbrk.py`, `CREATE OR REPLACE` on `masaha_b_test`, restored from the migration's text):
  B14 (`::date` without `AT TIME ZONE`) → D1 red; B15 (an open stay's minutes by `now()`) → D2 red; B16 (`floor`) →
  D3 red; B17 (no space filter) → D4 `expected [ 1, 2, 3 ] to deeply equal [ 1, 2 ]`. **Problem met and solved:** the
  first restore went through a Windows text pipe and stored the function with CRLF (md5 different, SQL the same);
  the script now sends bytes, the function was restored exactly (md5 `0fe1e5da…` = `masaha_b_dev`'s), and B14 re-run
  → red, `md5 same`.
- `lint` exit 0 · `typecheck` exit 0 · Prettier clean · `check:links` → `2506 links … all resolve.`
- **Departure, stated:** `DeskSubscription` has no `renewalOfId` and no `priceTyped` in PR 1: their columns arrive
  with PR 2's migration; nothing claims them before.
- Documents: data model (*Subscription progress*, *status*: `UPCOMING`, ended → expired, "at most 7 days"; *Amount
  due*), conventions §8, `subscriptions.md` (new), `desk.md` (link), `docs/README.md`, finding 120 + index.

## C4 committed — `feat(payments): compute debts in the database` (45)
- **How T16–T20 run, stated:** no API test in the repository builds a service by hand, and C4's queries have no
  route until C5; so `payments/balances.api.test.ts` runs `payments`' repository queries against the real test
  database (as the `db/` tests run SQL), with the calendar's days given. C5's endpoint tests then prove the service.
- **Red first:** `Tests  5 failed` — `TypeError: repository.customerBalances is not a function`.
- **Green:** `Tests  5 passed (5)`; with `db/subscriptions.api.test.ts` and `uncollected.api.test.ts` `Test Files  3
  passed (3)`, `Tests  24 passed (24)`.
- **Breaks** (`scripts\c4.json`), each restored, sha256 same, green: B32 (no `greatest`) → `debtAgorot: 19400` vs
  `21900`; B33 (no `usage_based` filter) → red (T17's fixed price lowered under what was paid, directly, since PR 2's
  price guard is not built: a fixed one still holds no credit); B34 (voided counted) → `debtAgorot: +0` vs `2000`;
  B35 (written-off counted) → `5000` vs `2000`; **B36 stayed green — departure:** the `paid` part's space filter
  cannot change the outcome, since a payment's foreign key `(item, space)` keeps it with its own space's items (the
  plan's exception); **B36b** (the visits' space filter dropped) → `expected [ 1, 4 ] to deeply equal [ 1 ]`, red;
  B37 (`ORDER BY id`) → red.
- **§12.2 check 6:** `npm run lint` exit 0 with `payments` importing `subscriptions` (`calendarOf`, `Now`).
- `lint` exit 0 · `typecheck` exit 0 · Prettier clean · `check:links` → `2509 links … all resolve.`
- **Departure:** `payments` needs no `subscriptions` service nor `now` dependency: the calendar's days come from the
  pure `calendarOf` (exported by `subscriptions`), and each method takes its instant.
- Documents: data model (*Customer debt*), conventions §9 (the balance query, R7's exception), `payments.md`.

## C5 — in progress, STOPPED (Docker Desktop not running)
- Written so far (uncommitted, in the working tree): U7 (`desk/requests.unit.test.ts`, red seen: `Cannot read
  properties of undefined (reading 'parse')`, then green `Tests  5 passed (5)`); the shared desk query and answers
  (`customersQuerySchema`, `CustomerRow`, `CustomerFile`, …) and `ItemPayment`; `customers.page` (raw SQL, each id
  list one array parameter); `subscriptions.currentOf` / `customerIdsBy`; `payments.paymentsFor`;
  `visits.deskVisitsOf`; the desk's `customers` and `customerFile` with their routes. `typecheck -w @masaha/api` clean.
- T21–T26 (`desk/customers.api.test.ts`) red seen before the code (`Tests  6 failed`; routes absent).
- **Then:** `vitest run --project api src/modules/desk/customers.api.test.ts src/modules/desk/customerFile.api.test.ts`
  → `Error: Cannot reach the test database (TEST_DATABASE_URL)… ECONNREFUSED`; `docker ps` → `failed to connect to
  the docker API at npipe:////./pipe/dockerDesktopLinuxEngine … The system cannot find the file specified.` Docker
  Desktop has stopped. **Stopped here (exec prompt §1.8 and §2): the owner must start Docker Desktop.**
- **Resumed** after the owner restarted Docker Desktop: `docker start masaha-postgres-1` ✔.

## C5 committed — `3b4c45e9` `feat(desk): list customers and read their file` (46)
- **Red first:** U7 → `Cannot read properties of undefined (reading 'parse')`; T21–T26 → `Tests  6 failed` (routes
  absent). T27–T30's file ran only after the code (it was skipped in the first red run by Vitest's file-level
  failure); their red is the breaks B44–B46's.
- **Green:** U7 `Tests  5 passed (5)`; both API files `Tests  10 passed (10)`; desk, customers, payments, occupancy
  and `db/subscriptions` together `Test Files  15 passed (15)`, `Tests  146 passed (146)`.
- **§12.2 check 7 and a fix it found:** T26 at 70,000 ids timed out. Measured: the seed alone costs ~7 s at 70,000
  (2.4 s customers, 4.5 s subscriptions), and the list's `id = ANY($array)` was quadratic (psql, 40,000 rows: 45.8 s;
  `id IN (SELECT unnest($array))`: 0.2 s). **Departure:** the page reads each list through `unnest` (still one array
  parameter). T26 then fit at 40,000 (4.5 s alone, too close to 5 s for the full lane), so it is **30,000** (3.1 s).
- **§12.2 check 4:** a scratch run (`scripts\b43.py`), T26 at 70,000 ids with a 60 s timeout, both files backed up
  and restored by SHA-256: the code as it is → **green** (one array parameter above PostgreSQL's 65,535 bound);
  **B43** (the ids bound one each, `Prisma.join`) → `expected 500 to be 200`, red. The first control attempt timed out
  at 60 s once (the next hook too); a probe of `pg_stat_activity` and a re-run did not reproduce it — recorded, cause
  not found. At 70,000 the request takes several seconds (15.5 s with the seed): **Review Focus** (S10, statistics on
  freshly inserted rows).
- **§12.2 check 5:** the file test reads `startsOn: '2026-10-01'` from `new Date('2026-10-01T00:00:00Z')`. ✔
- **§12.2 check 6:** `npm run lint` exit 0 with `desk` importing `customers`, `subscriptions`, `payments`, `visits`,
  `occupancy`. ✔
- **Breaks** (`scripts\c5.json`, multi-edit support added to `brk.py`), each restored, sha256 same, green: B12
  (refinement gone) → `expected null to deeply equal { kind: [ 'invalid_choice' ] }`; B38 (current by id only) →
  rows differ; B39 (name without `masaha_search_text`) → `expected [] to deeply equal [ 'أسامة علي' ]`; B40 (the
  payment filter applied to the page after it is fetched) → `expected { names: [ 'Lina' ], total: 5 } …`; B41 (`NONE`'s
  exclusion as an inclusion) and B41s (`SETTLED`'s) → red; B42 (`customers.manage` for `ARCHIVED`) → `expected 200 to
  be 403`; B44 (voided payments dropped) → red; B45 (no visit side) → `expected null to deeply equal { kind: 'VISIT'
  … }`; B46 (paid subtracted twice) → `expected 11000 to be 21500`.
- **Small additions, stated:** `CustomerRow.current` carries `packageId` (the row's kind); `OpenCheckIn` carries
  `subscriptionId` (the file's presence); `paymentsFor` takes visit ids only (a subscription's payments are PR 2's
  statement).
- `lint` exit 0 · `typecheck` exit 0 · Prettier clean · `check:links` → `2517 links … all resolve.`
- Documents: contract (the list and the file, the shapes, §4's exception), conventions (header *Built*, §9), `desk.md`,
  `customers.md`, `subscriptions.md` (S10 decision), `payments.md`, `v1-mvp.md` (step 8 *Built*, the routes' *Built*
  sentence), `overview.md` (*Customers*), `docs/README.md`.

## C6 committed — `9dab21dc` `fix(payments): page uncollected visits in SQL` (45)
- Finding 113 folded (§13 Q9): `payments.uncollectedPage` — one query and its count over the auto-closed visits not
  written off and their non-voided payments, the settled ones left out in SQL, the unpriced kept; `visits.deskVisitsOf`
  answers the page's visits; `autoClosedIn` / `autoClosedPage` removed.
- **Proof, as the plan says: the existing tests unchanged** — payments, `writeOff`, visits files `Test Files  6
  passed (6)`, `Tests  44 passed (44)`.
- **Breaks** (`scripts\c6.json`): C6-a (no written-off filter) → `expected [ 1, 2 ] to deeply equal [ 1 ]`; C6-b (no
  settled filter) → 2 failed; C6-c (voided counted) → red. **C6-d** (`ORDER BY v.id`, an extra break of mine) stayed
  green: in these tests a later close has a lower id, so that order is the same rows; **C6-d2** (`ORDER BY
  checked_out_at` ascending) → 3 failed, red. Each restored, sha256 same, green.
- `lint` exit 0 · `typecheck` exit 0 · Prettier clean · `check:links` → `2520 links … all resolve.`
- Documents: finding 113 (Resolved, resolution line) + index moved; `payments.md`; `visits.md`; conventions §9.

## Stop and ask — the PR's size (answered)
- PR 1 changes 84 files (22 from the carried commits, 10 of them shared with C1–C6; 72 from C1–C6), over the plan's
  "about 70". **The owner answered (2026-10-21): one PR, as is.**

## Rebase onto the new main (#99 merged, `2c4d78f9`)
- `git merge-tree --write-tree HEAD origin/main` → `CONFLICT (content): Merge conflict in docs/README.md` (documents
  only; #99 changed `apps/web` and `docs` only). Rebased (`git rebase origin/main`); one resolution in C1: main's two
  map lines (space-settings, occupancy) kept, `customers.md`'s line added after them. Subjects unchanged.
- Per commit (`git rebase -x "npm run lint && npm run typecheck" origin/main`): `OK` for all ten — `7159631a`,
  `45e39dca`, `601157af`, `0ffec309`, `5bb7445b`, `ad1e4630`, `92f87d69`, `6eae9b63`, `aec78fef`, `f41deab5` (the
  head); the rebase rewrote nothing.
- The commits after the rebase: `7159631a` fix(jobs) · `45e39dca` fix(desk) · `601157af` docs(desk) · `0ffec309`
  test(desk) · `5bb7445b` C1 · `ad1e4630` C2 · `92f87d69` C3 · `6eae9b63` C4 · `aec78fef` C5 · `f41deab5` C6.

## 12.4 Verification on the head (`f41deab5`)
- Free memory before the lanes: `FreePhysicalMemory : 4223880` (KB); no `vitest`/`tsc` of worker A running.
- `npm run build -w @masaha/shared` → exit 0 (after the rebase).
- `npm run test:unit` → exit 0: `Test Files  20 passed (20)` / `Tests  241 passed (241)` (shared), `Test Files  56
  passed (56)` / `Tests  827 passed (827)` (api), `Test Files  96 passed (96)` / `Tests  876 passed (876)` (web).
- `npm run test:api` (on `f41deab5`) → **failed**, lane exit 1: `Test Files  1 failed | 69 passed (70)`, `Tests  1
  failed | 1038 passed (1039)` — T26 `Error: Test timed out in 5000ms` (5171 ms), then `afterAll` `Hook timed out in
  10000ms` (the request still running). **Root cause found:** the lane empties every table, so the planner's
  statistics say `customers` is empty and each foreign-key check of the seed's 20,000–30,000-row subscriptions insert
  scans every customer (quadratic): an orphaned seed from the timed-out run ran ~30 s, and a psql seed beside it
  took 27.5 s; with statistics present the same seed takes 1.8 s. **Fix (the test's seed only):** `ANALYZE customers`
  after inserting them; and T26 at **20,000** ids (the plan's own fallback, check 7): 2.2 s alone (40,000: 4.5 s, too
  close to 5 s for the full lane). Folded into C5 (`--fixup` + autosquash), C5's body reworded (20,000); C5 is now
  `26a4749c`, C6 `d06897ca` (the head). `lint` exit 0, `typecheck` exit 0 on the head; the file `Tests  6 passed (6)`.
- `npm run format:check` → exit 0, `All matched files use Prettier code style!`.
- `npm run check:links` → `2552 links in 164 documents and 1569 source files all resolve.`
- `git grep -n "#PRNUM"` outside `docs/` → nothing; `git diff --stat origin/main -- apps/web` → only the two
  `errors.ts` (2 insertions); `git diff --stat origin/main -- package.json package-lock.json` → empty.
- Free memory before the re-run: `FreePhysicalMemory : 3448436`; no `vitest`/`tsc` of worker A.
- `npm run test:api` re-run on the head `d06897ca` → lane exit 0: `Test Files  70 passed (70)`, `Tests  1039 passed
  (1039)`.
- `npm run format:check` re-run (a covered file changed) → exit 0; `check:links` → `2552 links … all resolve.`
- **Not run, with why:** `test:component`, the web's `build`, `check:build`, `check:classes`: the web change is two
  catalogue lines, whose parity the typecheck enforces; CI runs them on the pushed head.

## 12.6 The real run (API on 3321, `masaha_b_dev`, `scripts\realrun1.mjs`)
- `curl http://localhost:3321/health` → `{"status":"ok","db":"up",…}`; signed in as `demo-owner@` and
  `demo-reception@` (the password read from `.env` into a variable, never printed).
- reception `POST …/customers { name, phone }` (a fresh key, a fresh number) → **201** id 9; the same key again →
  **201**, id 9 (same); another key, the same phone → **409 `PHONE_TAKEN`**, `{"phone":["not_unique"]}`.
- `GET …/customers?payment=OWES` → **200**: رامي سالم (1,500), محمد عوض (5,000, EXPIRED), سارة خالد (400, EXPIRED),
  and two customers DESK's real runs left ("Real run" 1,001, "Real run B" 1,500). The plan expected رامي and محمد;
  the others are older dev data (the seed's dates have aged since it ran, so its subscriptions' statuses differ).
- `?status=ENDING_SOON` → **200**: يوسف أبو علي (the hours pack, 16 of 20 hours) and نور حسن.
- `?q=0599000205` → **200** `["رامي سالم"]` (by digits).
- `GET …/customers/<رامي>` → **200**: debt 1,500, credit 0, no subscription, one unpaid visit (charge 1,500, paid 0,
  balance 1,500) with its customer رامي سالم.
- reception `POST …/archive` → **403**; the owner → **200** (`archivedAt` set); reception `?status=ARCHIVED` →
  **403**; the owner `POST …/restore` → **200** (`archivedAt: null`).
- `SELECT action … FROM audit_logs ORDER BY id DESC LIMIT 4` → `customer.restored`, `customer.archived`,
  `customer.created` (customer 9), then an earlier `payment.recorded`.
- Stopped by process ids (9028 `tsx watch`, 21244 the server, 19444 `pino-pretty`); port 3321 free; no API process
  left. `server.log` deleted. **The demo data changed:** one customer added, «تجربة التشغيل», with a fresh phone,
  archived and restored (three audit entries); nothing else.

## 12.7 The PR number, and a second rebase (#101 merged, `befd96f9`)
- Labels `feat`, `area:api`, `area:docs`, `area:web` exist. No other PR open. The next number: **102**.
- `git filter-branch --tree-filter "… sed 's/#PRNUM/#102/g'"` over the ten commits; `refs/original` removed;
  `git grep '#PRNUM'` → nothing.
- `git fetch` then showed `origin/main` at `befd96f9` (#101, worker A: 91 `apps/web` files, 8 documents);
  `merge-tree` → `CONFLICT (content): … docs/architecture/findings/README.md`. Rebased: two resolutions in the
  index's *Open* list (worker A's finding 130 and our 115, then our 120), kept in number order. Documents only.
- After the second rebase, per commit (`rebase -x` lint + typecheck): `OK` for all ten — `f8743c5a` fix(jobs),
  `0832e38e` fix(desk), `b0c6e36a` docs(desk), `07a70976` test(desk), `079d8c18` C1, `b444d59e` C2, `31f72494` C3,
  `b0468c7f` C4, `6108c942` C5, `900eebb4` C6 (the head).
- **On the head `900eebb4`:** `git diff d06897ca 900eebb4 -- apps/api packages/shared` → empty (the API lane's pass on
  `d06897ca` covers the same API and shared trees; not re-run). `build -w @masaha/shared` exit 0; `test:unit` exit 0
  (shared `241 passed`, api `827 passed`, web `Test Files  102 passed (102)` / `Tests  888 passed (888)` with #101's
  files); `format:check` exit 0; `check:links` → `2562 links in 165 documents and 1613 source files all resolve.`
- The number still 102 just before the push; no tool attribution in any commit message.
- `git push -u origin feat/customers` → `* [new branch] feat/customers -> feat/customers`.
- `gh pr create … --title "feat(desk): keep customers on file"` → **https://github.com/Basel-Ghonaim/masaha/pull/102**
  (= the number in the documents). Body: `scripts\pr1-body.md`.

## OPEN_DECISIONS.md point 3 — the update (for the supervisor to apply; this file is not edited here)
Replace the line's tail with: "**settled (#102, 2026-10-21):** a paged, searched list (at most 50 a page) for the
owner and reception; no export and no whole list for anyone in step 8; an export is the owner's, later, in finance."

## 12.8 CI, CLEAN, conflicts — and the final summary

1. **The pull request:** #102 https://github.com/Basel-Ghonaim/masaha/pull/102 · head `900eebb4` (= `git rev-parse HEAD`).
   `gh pr checks 102 --watch` → all pass on that head: build, check:classes, check:links, format:check, lint,
   test:api (6m3s), test:component (15m0s), test:unit, typecheck, CodeRabbit. `gh pr view 102` → `900eebb4 CLEAN
   MERGEABLE`.
2. **The commits** (carried first): `f8743c5a` fix(jobs): answer 200 when only stays failed (44) · `0832e38e`
   fix(desk): charge a stay up to its day's end (44) · `b0c6e36a` docs(desk): say what the debts' PR built (40) ·
   `07a70976` test(desk): prove the undo's refusals (37) · `079d8c18` feat(customers): create and edit a customer (43) ·
   `b444d59e` feat(customers): archive and restore a customer (47) · `31f72494` feat(subscriptions): derive status and
   progress (47) · `b0468c7f` feat(payments): compute debts in the database (45) · `6108c942` feat(desk): list
   customers and read their file (46) · `900eebb4` fix(payments): page uncollected visits in SQL (45).
3. **Run:** per commit lint + typecheck (all ten OK); `test:unit` (shared 241, api 827, web 888); `test:api` (70 files,
   1039 tests, on `d06897ca`, the same API/shared trees as the head); `format:check`; `check:links` (2562);
   `build -w @masaha/shared`; the real run on 3321. **Not run locally:** `test:component`, the web's `build`,
   `check:build`, `check:classes` (two catalogue lines) — CI ran and passed them on the head.
4. **Breaks and first failures:** each section above; every planned break red, three replaced where the planned one
   could not change the outcome (B25 → B25b, B36 → B36b, C6-d → C6-d2), plus extras (B7h, B8b, B10x, B41s, B43's
   scratch run).
5. **Problems met and solved:** Docker Desktop stopped twice (the owner restarted it); `prisma migrate dev` refuses a
   non-TTY shell (the plan's fallbacks); a Windows text pipe stored a restored function with CRLF (bytes now; restored
   exactly); `= ANY($array)` quadratic on long lists (`unnest`); T26 timed out in the full lane — stale planner
   statistics made the seed's foreign-key checks quadratic (`ANALYZE customers` in the seed; 20,000 ids); two
   documents-only rebases (#99, #101).
6. **Unexpected, unsolved:** the first B43 control (70,000 ids) timed out at 60 s once, not reproduced (the stale
   statistics are the likely cause, found later); at 70,000 ids the list request takes several seconds on freshly
   inserted rows — Review Focus (S10). The dev data holds earlier real runs' customers, so `?payment=OWES` lists more
   than the plan expected.
7. **Early conflict check:** `gh pr list --state open` → only #102; no other open PR to compare.
8. **Departures:** as listed in the PR description's *Departures from the plan* (migrations by fallback; `unnest`;
   T26 at 20,000 with `ANALYZE`; T16–T20 on the repository; the three replaced breaks; the archive's *present* read and
   `desk` → `subscriptions` in C2; the quote and charges so far capped with the check-out; the jobs' 500 unit-tested;
   small additions; `DeskSubscription` without PR 2's fields; 84 files, the owner's "one PR").
- **End state:** `git status --short` clean; port 3321 free; no API process left; `scripts\` uncommitted.

## Fix round 1 (the review of #102, findings 1 and 2; `7_FIXES_PROMPT_PR1.md`)

1. **The PR and its head:** #102, reopened; the new head after the push is in point 9. `origin/main` unmoved
   (`befd96f9`): no rebase.
2. **The commits** (C4 and C5 changed by `--fixup` + autosquash, both bodies reworded): `f8743c5a` fix(jobs) ·
   `0832e38e` fix(desk) · `b0c6e36a` docs(desk) · `07a70976` test(desk) · `079d8c18` C1 · `b444d59e` C2 · `31f72494`
   C3 · `bdc297dc` feat(payments): compute debts in the database (45) · `e6ca6606` feat(desk): list customers and read
   their file (46) · `a86645f5` fix(payments): page uncollected visits in SQL (45). The tree differs from `900eebb4`
   in five files only (`payments.repository.ts`, `balances.api.test.ts`, `customers.repository.ts`, both
   `customers.api.test.ts`).
3. **Item 1 — the balance query** (`balancesOf`, into C4):
   - **The form, recommended and built:** a `LEFT JOIN LATERAL` per branch, each item summing its own non-voided
     payments through `payments(subscription_id)` / `payments(visit_id)`. Why over two equi-joined aggregates: a
     grouped aggregate still reads every payment of the space on every call, even for one customer's file; the
     lateral reads only the items asked. `customerIdsByPayment` stays whole-space (a filter over every customer), on
     the same form.
   - **The customers asked are passed in:** `customerBalances` and `itemBalances` give their ids — on the
     subscriptions `u.customer_id = ANY($ids)`, on the visits `v.customer_id IN (SELECT unnest($ids))`, each one
     array parameter. **`EXPLAIN` on the pushdown:** PostgreSQL inlines `subscription_usage` and pushes `= ANY` inside
     (a `Bitmap Index Scan on subscriptions_customer_id_ends_on_idx` for the page's 20 customers); an
     `IN (SELECT unnest(…))` semi-join is *not* pushed there (all 2,000 subscriptions counted). So `= ANY` on that
     branch; the function's signature is unchanged.
   - **At scale** (`scripts\scale-seed.sql` + `scale-explain.sql` / `scale-explain-new.sql`, one rolled-back
     transaction on `masaha_b_test`: 2,000 customers with a fixed subscription each paid in part, 40,000 walk-in
     visits each paid; `EXPLAIN (ANALYZE, BUFFERS)`; outputs `scale-explain.out`, `scale-explain-new.out`):

     | Query | Before (the `OR` join) | After |
     |---|---|---|
     | `customerIdsByPayment` (OWES) | **6,844.7 ms** — Nested Loop Left Join, `Join Filter: … OR …`, **Rows Removed by Join Filter: 83,998,000** | **22.1 ms** — no join filter; `Index Cond: (subscription_id = …)`, `(visit_id = …)` |
     | `customerBalances` (a page of 20) | 108.3 ms — the same join filter, 839,980 rows removed | **8.9 ms** — the function's subscriptions by index for the 20 |
     | `itemBalances` (one customer) | (whole-space before, as the page) | **8.3 ms** |
   - **The lane's proof:** the review's scale cannot be seeded inside Vitest's 5 s — the ledger's insert trigger costs
     ~0.65 ms a payment (40,000 visit payments: 25.9 s alone in psql). A new test beside T26, at the largest seed that
     fits — 1,000 subscriptions each paid 1,000 of 3,000, 2,000 walk-in visits paid in full (1.4 s) — proves the list,
     `?payment=OWES` (total 1,000) and a file (debt 2,000, the subscription's paid and balance, no unpaid visit)
     answer with a payment on every item. **Break F1-or** (the `OR` join over the aggregate restored) **stayed green**
     at that scale: **the plan proved it**, not the time budget (the table above).
   - **B32–B37 re-run on the new form**, each red then green: B32 → `debtAgorot: 19400` vs `21900`; B33 → red; B34
     (visits' voided filter) → `30000` vs `32000`; B35 → `5000` vs `2000`; B36b → `[ 1, 4 ]` vs `[ 1 ]`; B37 → red.
   - **A gap found and closed:** B34s (the *subscriptions'* voided filter dropped, now a separate branch) stayed green
     — no test voided a subscription's payment. T18 (`balances.api.test.ts`) gains a voided payment on a fixed
     subscription; B34s then → `debtAgorot: 2000` vs `32000`, red.
   - **F1-whole** (an extra break: the subscriptions' customer filter dropped) stayed green: the page's answer is
     kept to the customers asked either way — a cost, not an answer; the plan above is its proof.
4. **Item 2 — the ids' bound** (into C5): a test in `customers/customers.api.test.ts` (the level rule refuses a `desk`
   test importing `customers`' repository) calls `customers.page` with **70,000 ids that do not exist**: `include` →
   `{ rows: [], total: 0 }`; `exclude` → the space's one customer (0.5 s). **B43** (`Prisma.join`, one parameter per
   id) → `PrismaClientKnownRequestError`, **red in the lane**.
5. **A claim of mine corrected:** C5's body and the repository's comment said `= ANY($array)` is quadratic (45.8 s at
   40,000 in psql). Re-measured with statistics present: `= ANY` on a bound array 8.3 ms, on a column-sourced array
   12.0 ms. The 45.8 s came from freshly inserted rows without statistics (the same cause as T26's earlier timeout).
   `unnest` stays (one parameter, harmless); the claim is removed from the comment and C5's body. **F2-any** (a revert
   to `= ANY`) stayed green against T26's 20,000-row seed, so **T26 is dropped**, as the prompt says: it no longer
   catches anything the new tests do not.
6. **Review Focus, recorded:** the visits branch for a page still filters the space's closed visits (40,001 rows
   removed, a few ms at 40,000): `visits` has no index on `customer_id` for closed visits; an index is a schema change
   for the owner.
7. **Run, and passed:** `lint` exit 0 · `typecheck` exit 0 (on the head) · Prettier clean · free memory
   `5025536` KB, no `vitest`/`tsc` of worker A · `npm run test:api -w @masaha/api -- src/modules/payments
   src/modules/desk src/modules/customers` → exit 0, `Test Files  11 passed (11)`, `Tests  104 passed (104)`. No unit
   file and no document changed, so no unit lane, `format:check` or `check:links` run (CI runs them).
8. **Real run** (3321, `masaha_b_dev`, read-only, `scripts\realrun1b.mjs`): health `db: up`; the list → 200, 9
   customers; `?payment=OWES` → 200 `Real run 1001`, `Real run B 1500`, `رامي سالم 1500`, `سارة خالد 400`,
   `محمد عوض 5000` — the same rows and sums as the first real run; رامي's file → 200, debt 1,500, credit 0, one
   unpaid visit (4, paid 0, balance 1,500) — as before. Stopped by process ids; port 3321 free; `server.log` deleted.
9. **Pushed:** `git push --force-with-lease` → `900eebb4...a86645f5 (forced update)`; `#PRNUM` absent (already #102).
   The PR description gained *Fix round (review of #102)*, the deferral note (review items 3, 4, 7, 9; findings 5, 6,
   8 → `0_CARRIED_FROM_102.md`) and the two corrected statements (`= ANY`, T26).
10. **CI on `a86645f5`:** the local `gh pr checks --watch` was stopped by Claude Code for low memory (the watcher, not
    CI), and not restarted. A one-shot read: format:check, lint, test:unit, typecheck, build, check:classes,
    check:links, CodeRabbit **pass**; **test:api and test:component pending**; merge state `UNSTABLE` while they run.
    **Not yet green on the new head** — to be read once they finish.
