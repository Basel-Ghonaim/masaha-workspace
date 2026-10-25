## Summary

Step 8, PR 1 of 3 (customers). The API's customers: created (idempotent), edited, archived and restored; the list, paged, searched and filtered by subscription and payment state, with debts and the payment filter computed in the database; the customer's file; subscription status and progress, on attendance counted by one database function. Finding 113 folded (the uncollected visits paged in SQL).

**Carried from #100** (its review; the owner's decisions of 2026-10-21), the first four commits:
1. The jobs endpoint answers 200 with a `failed` count when only stays failed, and 500 only when a job itself threw; the runbook reads `stay not closed` in the logs (finding 114, resolved).
2. A desk check-out charges a stay up to the earlier of the quote's time and its due time (23:59 of its check-in's day at the latest), and records that time as `checkedOutAt`; the quote and the charges so far stop there too (finding 116, resolved).
3. A write-off and its undo carry no key: accepted for v1, provided the desk's screen never retries these two routes by itself (finding 115, Open).
4. `payments.md`, `visits.md` and conventions §13 say what #100 built.
5. Nit 7: the undo's refusals tested. Nits 6 and 8: no change (the review judged both acceptable).

## Fix round (review of #102)

1. **The balance query** (review finding 1, folded into `feat(payments): compute debts in the database`): each item sums its own non-voided payments through a `LEFT JOIN LATERAL` on the payments' `visit_id` and `subscription_id` indexes, instead of an aggregate of every payment of the space joined back by an `OR` of two columns (a nested loop of items × paid items). A page and a file pass the customers they ask for: `= ANY` on the subscriptions, which PostgreSQL pushes inside the inlined `subscription_usage` (index scan, checked with `EXPLAIN`); `unnest` on the visits. At 40,000 paid visits and 2,000 paid subscriptions (`EXPLAIN (ANALYZE, BUFFERS)`, on the test database): the payment filter **6,844.7 ms → 22.1 ms** (83,998,000 join-filter rows → none); a page of 20 **108.3 ms → 8.9 ms**; one customer's items **8.3 ms**. A new test answers the list, the payment filter and a file with a payment on every item (1,000 subscriptions, 2,000 paid visits: the largest seed the 5 s budget fits, the ledger's trigger costing ~0.65 ms a payment). With the `OR` join restored that test stays green at its size: **the plan proved it**. B32–B37 re-run red then green; a voided subscription payment added to T18 (B34s, a gap the new branch opened, red).
2. **The ids' bound** (review finding 2, folded into `feat(desk): list customers and read their file`): `customers.page` with 70,000 ids that do not exist answers an empty page; B43 (one parameter per id) red in the lane. T26's 20,000-row seed is dropped: a revert to `= ANY` stays fast with statistics present, so it caught nothing more. The first round's "`= ANY` is quadratic" is withdrawn (comment and commit body).

**Deferred to PR 2** (`0_CARRIED_FROM_102.md`): review items 3, 4, 7, 9; findings 5, 6, 8 to record.

**Review Focus:** a page's visits branch still filters the space's closed visits (no index on `visits.customer_id` for closed visits: a schema change for the owner).

## Scope

1. Migration `customer_key`: `customers.request_id` (UUID, nullable), unique within the space.
2. Migration `subscription_usage`: the database function counting each subscription's days used, days this week, minutes used and today's, and its amount due.
3. `@masaha/shared/customers` (new), `@masaha/shared/subscriptions` (new); `core` gains `addDays`, `weekStartOf` (Saturday) and `dateSchema`.
4. `POST /manage/spaces/:spaceId/customers` (🧾, `Idempotency-Key`), `PATCH …/customers/:customerId` (🧾).
5. `POST …/customers/:customerId/archive` and `…/restore` (🏢).
6. `GET …/customers` (🧾: `q`, `status`, `kind`, `packageId`, `payment`, paged) and `GET …/customers/:customerId` (🧾: the file).
7. `subscriptions`: the pure status and current-subscription rules, the states read, the list's filters as ids.
8. `payments`: customers' debt and credit, the payment filter's ids and a customer's items, in one SQL query; visits' payments with their voids.
9. `can()`: `customers.archive` (owner); ADR 0009 gains two rows.
10. Error code `CUSTOMER_ARCHIVED`; `PHONE_TAKEN` and `MEMBER_ALREADY_CHECKED_IN` used for the first time.
11. Finding 120 recorded; finding 113 resolved.

## Acceptance criteria

- [x] A customer is created with a name and an optional phone, audited; a retry with the same key answers the first customer, 201; a phone another customer of the space holds (not archived) is refused 409 `PHONE_TAKEN` with `errors.phone = ["not_unique"]`, writing nothing.
- [x] Owner and reception edit a customer's name and phone; an archived one is refused `CUSTOMER_ARCHIVED`; an edit that changes nothing writes nothing; every change audited with before and after.
- [x] Only the owner archives and restores (reception 403 before anything is read); a present customer is not archived (`MEMBER_ALREADY_CHECKED_IN`); an owing customer is; a restore whose phone another customer now holds is refused `PHONE_TAKEN`; a repeat answers as it is.
- [x] The list pages the space's customers, archived ones only for `status=ARCHIVED` (the owner's; reception 403); `q` matches a name (Arabic folded as the directory's search) or, digits only (two or more), a phone's last digits; `status`, `kind`/`packageId` and `payment` filter before the page is cut: every page full, the total right.
- [x] Debt, credit and the payment filter are computed by one SQL query of `payments`; no request reads every payment, visit or check-in into memory; a voided payment counts for nothing; a written-off visit is no debt; credit is only a usage-based subscription's.
- [x] The file answers the customer, the debt, the credit, each subscription with status, progress, due, paid and balance, the unpaid visits with their payments (voided ones marked), and who is present.
- [x] Status and progress follow the data model (Gaza dates, Saturday-to-Friday weeks), every branch a unit test.

## Out of scope

The screens 14–16 and the desk's subscriber parts (worker A's later items); every web change but the catalogue lines; any export of customers or phones, for anyone; voids, the payments list, collections and finance (steps 9 and 11); merging customers; subscriptions' writes, payments and statement (PR 2); subscription check-ins and *present* defined once (PR 3).

## Change type

feat — API code, the shared contract, tests and documents; two migrations (customers' key; the attendance function); the new code's catalogue lines in `apps/web` (worker B's licence).

## New error codes (the Arabic needs the owner's approval)

| Code | Answer | English | Arabic |
|---|---|---|---|
| `CUSTOMER_ARCHIVED` | 409 | This customer is archived; the owner restores them first. | هذا الزبون مؤرشف؛ يسترجعه المالك أولًا. |

## Evidence

- `lint` and `typecheck` on each of the ten commits (`git rebase -x`, after the last rebase): all pass.
- On the head: `test:unit` exit 0 (shared 241, api 827, web 888 tests); `format:check` exit 0; `check:links` (2,562 links resolve); `build -w @masaha/shared` exit 0.
- `test:api` exit 0 — `Test Files 70 passed (70)`, `Tests 1039 passed (1039)` — on `d06897ca`, before the last rebase, which brought in only `apps/web` and `docs` from `main` (#101). After the fix round: the payments, desk and customers folders, `Test Files 11 passed (11)`, `Tests 104 passed (104)`; CI runs the whole lane.
- Seen failing first, in its own lane: the jobs tests (`expected 500 to be 200`); the overdue check-out, its quote and its charge so far; U6, U3, U1, U2, U4, U5, U7 (the modules missing or not exporting yet); T1–T9 and T10–T15 (routes absent); T16–T20 (`customerBalances is not a function`); T21–T26 (routes absent). D1–D4 and T27–T30 were red through their breaks.
- Deliberate breaks, each red then restored from a backup (SHA-256 compared): carried C0-1a/b, C0-2a–c, C0-7a–c; C1 B3, B11, B18–B24, B25b, B26; C2 B13, B27–B31 (+ B10x); C3 B1, B2, B4–B10 (+ B7h, B8b) and the database breaks B14–B17 (`CREATE OR REPLACE` on the test database); C4 B32–B35, B36b, B37; C5 B12, B38–B42 (+ B41s), B43 (in the lane since the fix round), B44–B46; C6 C6-a–c, C6-d2.
- §12.2's checks: the two migrations, each created once; `subscription_usage` answers on both databases; `masaha_search_text` exists; one array parameter above 65,535 (70,000 ids, scratch run: green; bound one each: 500); a `@db.Date` reads back as its calendar date; the level rule accepts every import.
- Real run on 3321 (`masaha_b_dev`): create 201, the same key 201 with the same id, the same phone 409 `PHONE_TAKEN`; `?payment=OWES`, `?status=ENDING_SOON`, `?q=` by digits 200; the file 200 (رامي: debt 1,500, one unpaid visit); reception's archive 403, the owner's 200; reception's `?status=ARCHIVED` 403; the owner's restore 200; audited `customer.created`, `.archived`, `.restored`.
- Not run: `test:component`, the web's `build`, `check:build`, `check:classes` — the web change is two catalogue lines, whose parity the typecheck enforces; CI runs them.

## Departures from the plan

- **Migrations without `migrate dev`:** this environment has no TTY, so `prisma migrate dev --create-only` refuses ("non-interactive"). `customer_key` was written by `prisma migrate diff --from-config-datasource --to-schema … --script` (the plan's fallback), and `subscription_usage` by hand (the plan's fallback for an empty migration); each once.
- **The list's id lists are read through `IN (SELECT unnest($array))`**, one parameter each. (The first round's claim that `= ANY` is quadratic was wrong: its 45.8 s came from rows without statistics; corrected in the fix round.)
- **The ids' bound** is proven by a test of `customers.page` with 70,000 ids that do not exist (fix round); the 20,000-row seed (T26) is dropped.
- **T16–T20 call `payments`' repository queries** against the real test database: C4 has no route, and no API test here builds a service by hand. C5's endpoint tests prove the service.
- **Breaks that could not change the outcome, replaced:** B25 (`spaceOf` itself answers 404 without a loaded space) → B25b (mounted behind `loadSpaceLinks`); B36 (a payment's foreign key keeps it with its own space's items) → B36b (the visits' space filter); C6-d (`ORDER BY id`, an extra break) → C6-d2.
- **The archive's *present* check** reads the space's open check-ins and visits (both existing reads, bounded by who is present); `desk` gains `subscriptions` in C2 (the plan: C5). PR 3's `occupancy.isPresent` will replace it.
- **The overdue check-out also caps the quote and the charges so far** (carried item 2), so the desk shows what it will charge; `checkedOutAt` records the stay's end, the audit the request's time.
- **"A job that throws answers 500" is unit-tested on `createJobs`** (whose jobs are its dependency): no job can be made to throw through the real app without test-only code.
- **Small additions:** `customerChange.ts` (the edit's change, pure); `CustomerRow.current.packageId`; `OpenCheckIn.subscriptionId`; `calendarOf` exported by `subscriptions`. `DeskSubscription` has no `renewalOfId` or `priceTyped` until PR 2's columns.
- **The PR's size:** 84 files, over the plan's "about 70"; the owner chose one PR as is.
- **#100's description** (review finding 5) stays as merged; the four departures it left out: the schema edited by hand after `prisma format` realigned unrelated blocks; D1 and D2 written after the migration, red only through B5 and B6; B12's and B18's red differing from the plan's expectation; the PR-number fix (`#99` → `#100`) by `filter-branch`.

## Screenshots

None: API and documents only.

## Definition of Done checklist

- [x] Acceptance criteria met, scope kept.
- [x] Lint and typecheck clean; `packages/shared` builds.
- [x] Tests added in the owning lanes, each seen failing.
- [x] No hardcoded user-facing text (codes only; both catalogues).
- [x] Authorization on the server (the boundary, `requireCan`, `can()` under the space's lock).
- [x] Triggered documentation updated in this PR.
- [x] One home per fact; nothing claimed that is not built.
- [x] Every claim names its test or command.
- [x] Atomic history, pushed.
