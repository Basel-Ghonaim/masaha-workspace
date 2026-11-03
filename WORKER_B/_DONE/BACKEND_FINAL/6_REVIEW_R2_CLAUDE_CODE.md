# Review of #131 — R2: the finance — Claude Code
Head: c41a5397 · range 6d563549..53c6a7e3 (3 commits: a05891e4, 71a18c1b, 53c6a7e3) · checks: green (build, check:classes, check:conflicts, check:links, format:check, lint, typecheck, test:unit, test:api, test:component pass; CodeRabbit skipping) · head moved during the review: no (`c41a5397…`, `CLEAN`, read again at the end)
Verdict for my range: mergeable after a fix round

No file of `apps/api/src/modules/finance/` changed after 53c6a7e3 (`git diff --stat 53c6a7e3..c41a5397`): every finance file below was read at the head and is the same as at the end of my range. The `payments` aggregates (`balancesPage`, `balanceTotals`, `uncollectedTotals`, `uncollectedOf`) are R1's commit 5f867d86; I read them at the head because finance's debts answer them.

## Findings (verified defects only, most severe first)

### R2-F1 — should-fix · Finance › debts' "owed" and "uncollected" overlap, but the contract says the uncollected are "counted apart"
- Where: docs/api/api-contract.md:726 at c41a5397 (also docs/features/finance.md:10, packages/shared/src/finance/responses.ts:55); the rule is apps/api/src/modules/payments/payments.repository.ts:162 (`uncollectedOf`, unchanged since before #131) against :135 (`balancesOf`'s visit branch).
- Seen in the code: `uncollectedOf` keeps every visit closed by the auto check-out (`v.checkout_method = 'AUTO' OR (v.customer_id IS NULL AND …)`), with or without a customer. `balancesOf` counts every closed visit that has a customer and is not written off in that customer's debt. «تسجيل دينًا» (`desk.service.ts:708–725` → `visits.leaveTo`) sets `customer_id` and leaves `checkout_method = 'AUTO'`. `desk/debt.api.test.ts:71` pins that such a visit "stays uncollected, with its customer". `finance.service.ts:155–158` reads both figures into one `meta.totals`.
- Scenario: a walk-in's visit is auto-closed at 4,000, unpaid. Reception records it as a debt to a phone. `GET …/finance/debts` then answers `totals.owed.agorot` including the 4,000 (and that customer in `owed.customers`) **and** `totals.uncollected` `{ visits: 1, owedAgorot: 4,000 }`. Each figure is right by its own rule. The contract says "A walk-in's uncollected visit is no customer's debt: it is counted apart", so a reader, or the coming screen 19, may add owed and uncollected. That shows the owner 8,000 still to collect where 4,000 is owed. No test has this case: T-F9 and T-F10 seed uncollected visits without a customer only.
- Fix: (a) in this fix round, correct the contract sentence, `finance.md:10` and the `DebtsMeta` comment to say what the code does: the uncollected count is the desk's list, which keeps an auto-closed visit left to a customer, so its rest is also in that customer's debt and the two figures are never added. Pin it with a test in `debts.api.test.ts` (an auto-closed visit left to a customer: in `owed` and in `uncollected`). (b) Whether finance's `uncollected` should leave out visits that have a customer is the owner's call: it would break AC-O2's "equal to the desk's list" for the overview's count, and Q2 speaks of "a walk-in's uncollected visit" only. · Belongs: a fix round on #131 (the documents and the test, folded into 71a18c1b) **and** a finding (**193**) for the owner's decision on (b).

### R2-F2 — nit · finance.md says income reads 45 windows; the code reads 46
- Where: docs/features/finance.md:33 at c41a5397 (the plan's D12 has the same miscount).
- Seen in the code: `finance.service.ts:93–100` builds the month, the month before, today, all time (4), then 12 months and 30 days: 4 + 12 + 30 = 46. `split(4 + months.length + i)` reads index 45 last.
- Scenario: a reader checking the statement's size or the indexes against the document counts one window short. The answer itself is right.
- Fix: "45" → "46". · Belongs: a fix round on #131 (folded into a05891e4; the paragraph is rewritten in 53c6a7e3, so fold the change wherever the line last changes).

### R2-F3 — nit · `todayWindow` is production code that only a test uses
- Where: apps/api/src/modules/finance/windows.ts:25 at c41a5397.
- Seen in the code: `git grep todayWindow` finds the export and `windows.unit.test.ts:12,38` only. The service builds today's window with `dayWindow(gazaClockOf(at).date)` (`finance.service.ts:90,96`).
- Scenario: dead production code that a test keeps green. The project's rule is no production code that only tests use or that nothing uses.
- Fix: either use `todayWindow(at)` in `income`, or drop the export and point its unit case at `dayWindow` (the 25-hour day is already asserted through `dayWindow`). · Belongs: a fix round on #131 (folded into a05891e4).

## The plan's tests and breaks for my range (one line each: present / missing / weaker; would it fail?)
The tests were seen in the code. The red lines of the breaks are **only in a report** (`scripts\lane-f\REPORT.md`, `break-F-*.txt`). I judged from the code whether each break would turn its test red.
- U-F1 `gazaTime.unit.test.ts` monthOf/addMonths: present. B-F1 (December off by one) would fail it (report: "expected '2026-13' to be '2027-01'").
- U-F2 `windows.unit.test.ts`: present, including the 25-hour 2026-10-24 and the 23-hour 2026-03-28. B-F2 (UTC midnights) fails the `monthWindow`/`dayWindow` instants; B-F3 (28 days ending today) fails `['2026-10-01','2026-10-28']`.
- U-F3 `occupancyGrid.unit.test.ts`: present. B-F4 (÷ 7) fails 1.3; B-F5 (attendance over every day) fails 3.7.
- U-F4 `requests.unit.test.ts`: present.
- T-F1 `access.api.test.ts`: present, every route with an invalid query: reception 403, owner 422, stranger/other owner/admin 404. B-F6, B-F7 → 422 ≠ 403; B-F7a → 404 ≠ 403. Would fail.
- T-F2 income/voided/written-off: present. B-F8 → the 5,000 voided counted. Would fail.
- T-F3 Gaza days: present. The 23:30 (+03:00) payment of 30 Sept is still 30 Sept in UTC, so on its own it does not catch B-F9. The 00:30 (+03:00) payment of 1 Oct (21:30 UTC, 30 Sept) does catch it: `2026-10` = 33,800 and `visitsByDay` 2026-10-01 = 800 would fail. Would fail.
- T-F4 collections by method, an ex-reception named: present. B-F10 would fail.
- T-F5 another space: present (income, today, all time, collections). B-F11 would fail.
- T-F6 422 month bounds, 23 back answers: present, plus `invalid_format`. B-F12 would fail.
- T-F7 debts order, phone, archived, oldest item: present, paged in 3 pages. B-F13 (`archived` false) would fail. B-P1 would fail the order.
- T-F8 credit: present. B-F14 would fail.
- T-F9 written-off/voided/unpriced owe nothing; uncollected apart, equal to the desk's list: present. B-P3 would fail. **Weaker:** no visit left to a customer (R2-F1).
- T-F10 totals = sum of every page, template: present, both states paged with limit 1. B-F16 would fail.
- T-F11 payers: present (latest first, tie by id, walk-in out, voided out, archived in, September's 23:30, other space, past last page). B-F17 would fail.
- T-F12 per day: present (open visit left out, M twice → once). B-F18, B-F19 would fail.
- T-F13 per hour: present (auto-closed member on the 11th counted, today out). B-F20 would fail `at(0,10)` / `at(2,10)`.
- T-F14 average stay, peak tie, attendance, nulls: present. B-F21 would fail (`all` 88 vs 86).
- Not tested, and said (§9.7): the snapshot under a concurrent payment, a real year's cost. Accepted.

## Decisions taken without the owner in my range, judged
- **Lane F (1): all time runs from `-infinity` to `infinity`, not "to now"** (D9 said to now). *Sound.* The month and today run to their next midnight. With "to now", a payment recorded at the request's instant, or one dated by a fixed clock, could fall in today but outside all time. Documented in `finance.md`.
- **Lane F (2): `contactsOf` gains `archived`, narrowed out of `deskCheckIns`** (`subscriptions.service.ts:183`; R4 was wrong). *Sound.* It keeps the check-ins' answer to its contract, and the check-in test caught the leak. One line, documented in `subscriptions.md`.
- **Lane F (3): `.extend` instead of the deprecated `.merge`.** *Sound.* Same schema.
- **Lane F (4): the month's bound as `AppError.validation({ month: ['out_of_range'] })`.** *Sound.* `out_of_range` is an existing validation code (announcements, desk). No new error code.
- **Lane F (5): occupancy's five reads in parallel, with no snapshot.** *Sound.* It is the plan's D12. No figure must equal another.
- **Lane F (6): `finance.md` rewritten whole in C7.** *Acceptable.* Each of the three commits carries `finance.md` (seen in `git show --stat`), so no commit links a missing document. Only C7's wording is final.
- **Lane F: the API tests' red taken with the routes unmounted** (the service was written before its tests). *Acceptable, weaker than the rule.* The 404 red proves the route, not the logic. Each logic break (B-F8–B-F21) was then run red, which is the stronger proof, and I judged above that each would fail.
- **LEAD-D4: EC4 (cost on a generated year) run once on the joined code.** *Acceptable.* One data set measured every statement. Only in a report: income 89 ms, debts 190 ms wall (statements ≤ 49 ms), none over 150 ms.
- **LEAD-D6** (the overview's test space lacked its settings row; `debts` → 500): *sound.* `spaceSettings.read` treats a missing row as a fault. Every space made through the API has one, so a client cannot cause the 500. The finance tests give their space a settings row.

## Outside my range
- `payments.repository.ts:162` (`uncollectedOf`, the desk's rule since #97/#100/#114, reused by R1's `uncollectedTotals`): an auto-closed visit left to a customer stays uncollected and is also that customer's debt. This is the root of R2-F1. Its consequence for the owner's overview (`uncollectedVisits` and `customersOwing` both count it) is R3's to weigh.

## Checked and fine
- **Income = cash collected:** every income sum is `voided_at IS NULL`, on `received_at`, with `>= from AND < to`, so a payment at a window's `to` falls in the next window (§9.8). `payments_one_item_check` (`num_nonnulls(visit_id, subscription_id) = 1`) makes the subscriptions/visits split exact and `total = subscriptions + visits` never double-counts. A subscribe allocated over old debts records one row per item, each `receivedAt: at` (`desk.service.ts:324,365`), counted once in the window it was collected. A check-out's payment is `receivedAt: requestedAt`.
- **Windows:** `monthWindow` and `dayWindow` come from `gazaInstant` (S1, no `AT TIME ZONE`). `monthError` compares `YYYY-MM` strings, which the regex keeps at fixed width. The previous month of the 23rd month back answers (no bound needed). The 12 months, 30, 14 and 28 days end with now whatever the month asked, as the contract says. On a month's first Gaza day before 08:00, the result is empty figures, not an error (`daysOfMonth` gives one day).
- **One snapshot (S2):** `income` runs `incomeIn`, `firstReceivedAt` and `collectionsIn` on `tx`. `debts` runs `balancesPage` (and its `countOwing` fallback), `balanceTotals`, `uncollectedTotals`, `spaceSettings.read`, `contactsOf`, `subscriptions.namesOf` and `visits.deskVisitsOf` all on `tx` (each repository takes `tx`, seen). No call inside either transaction uses `prisma` directly. `users.namesFor` runs after the snapshot, as planned. `readSnapshot` is `READ ONLY`, `REPEATABLE READ`.
- **Debts:** `balancesOf(spaceId, null, …)` filters no archive, so the archived are kept (Q2), and the balance rule is the one `payments` rule (`DEBT`/`CREDIT` constants). Totals = pages (T-F10). The oldest item is `due − paid > 0` (an unpriced `NULL` due is never oldest), least `created_at`, visit first, then id. The phone and `archived` come from `contactsOf`, filtered on the space. `limit` is bounded by `MAX_PAGE_SIZE`. The CSV comes from pages read in separate snapshots (accepted, §9.8).
- **Payers:** `coalesce(v.customer_id, s.customer_id)`, walk-ins out, voided out, `count(*) OVER ()` counts customers (groups), the fallback is `count(DISTINCT …)` past the last page, and the items join on the composite FK (same space). `customers.namesOf` does not filter the archived, so an archived payer cannot cause a "missing" 500.
- **Occupancy:** closed stays only (`checked_out_at IS NOT NULL`), auto-closed ones kept, bounded by check-in on `(space_id, checked_in_at)` (both tables indexed, schema :736, :795). Overlap is `in < slot.to AND out > slot.from` (a stay ending at 10:00 is not in 10:00). A member is counted once a day (`count(DISTINCT customer_id)`). Whole minutes come from `round(avg(...))::integer`. The peak hour takes the earliest of ties. Attendance divides by the days with any. ÷ 4 rounds one decimal half up, exactly. On a 25-hour day the repeated hour's two slots are summed into one weekday-hour cell (a 1 a.m. cell, negligible). This is the plan's "per slot", seen and accepted.
- **Authorization:** each of the four routes has `requireCan('finance.read')` before `validate`. `'finance.read': 'owner'` (`can.ts:84`). The router is mounted on `manage`, behind `requireSpaceAccess` (`app.ts:606` in the range, `:637` the guard), so the admin and strangers get `not_found`.
- **Cost:** income is one statement of 46 windows on `payments (space_id, received_at)`. Debts runs `balancesOf` twice (page and totals), within EC4's figures. I read the costs in the report only.
- **Documents:** the contract's *Finance* (shapes, errors, the snapshot claims), data model *Income*, *Collections*, *Occupancy statistics*, conventions §7's `finance` row, security's bullet, and `customers.md`/`payments.md`/`subscriptions.md` lines are true to the code, except R2-F1 and R2-F2.

## Not checked, and why
- Whether each break actually ran red, and the EC4 timings and plans: read only in the reports (`lane-f\REPORT.md`, `4_REPORT_LEAD.md`). The rules forbid test runs and database commands.
- `sum(...)::integer` overflow: all-time income above 2³¹ agorot (≈ 21 million ₪) would be `integer out of range`. That is not a realistic space, and it is the module's existing convention, so it is not a finding.
- The real run's R1–R4 (ALL PASS): only in the lead's report.
