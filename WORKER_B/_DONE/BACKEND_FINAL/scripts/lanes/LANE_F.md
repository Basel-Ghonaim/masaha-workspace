# Lane F — the space's finance (C5–C7)

- **Worktree:** `C:\dev\masaha\app-b-lane-f` · **branch:** `lane/f` (checked out) · **base:** `b0cd0ae4` (the lead's
  C1–C4 on `origin/main` `d40d20f5`) · **test database:** `masaha_b_lane_f_test` (set in the worktree's
  `apps/api/.env`, migrated) · **scripts folder:** `C:\dev\masaha\workspace\WORKER_B\BACKEND_FINAL\scripts\lane-f\`
  (create it) · **grant tag:** `lane-f` · **finding number:** 157 (more: 192, 193, and say so).
- The rules: `LANE_COMMON.md` (beside this file) — read it first, whole.

## What you build — three commits, in this order

| # | Subject (exact) | Holds (the plan's §8.1) |
|---|---|---|
| C5 | `feat(finance): read a space's income` | `monthOf`, `addMonths`; shared `finance`; `windows.ts`; `payments`' `incomeIn`, `firstReceivedAt`, `collectionsIn`; the module, its income route; U-F1, U-F2, U-F4, T-F1 (income), T-F2–T-F6; contract *Finance* (income); data model (*Income*, *Collections*); conventions §7's `finance` row; security; `finance.md` (first) |
| C6 | `feat(finance): read who owes and who paid` | `customers.contactsOf`'s `archived`; the debts and payers routes; T-F1 (both), T-F7–T-F11; contract; `finance.md`; `payments.md` |
| C7 | `feat(finance): read a space's occupancy` | `occupancyGrid.ts`, the occupancy reads and route; U-F3, T-F1 (occupancy), T-F12–T-F14; contract; data model (*Occupancy statistics*); `finance.md` |

**Read in the plan:** the approval note; §2.1, §2.2 (the owner's finance decisions — binding); §3.1 (AC-F1–AC-F5);
§4.1 (R1–R15, re-verified facts); §5.1 (the finance routes, mounts, placement and levels); §5.2 D8 (the shared
shapes); §5.3 D9–D12 (windows, the ledger's aggregates, occupancy, the service); §5.4 D23–D24 (snapshots, bounds);
§5.6 S1–S3; §5.7 A1, A2 (not taken); §7 *Unit U2*; §8.1–§8.3; §9.3 (every test and break: U-F1–U-F4, T-F1–T-F14,
B-F1–B-F21); §9.7–§9.8; §11.1 items 1–5; §13 EC2, EC3, EC6.

## What the lead's C4 already gives you (on your base)

`payments.repository.ts` / `payments.service.ts`: `balancesPage(spaceId, state, at, { page, limit }, tx?)` →
`{ rows: { customerId, amountAgorot, oldest: { kind, id, createdAt } | null }[], total }`; `balanceTotals(spaceId, at,
tx?)` → `{ owed: { agorot, customers }, credit: { agorot, customers } }`; `uncollectedTotals(spaceId, tx?)` →
`{ visits, owedAgorot, unpriced }`; the uncollected `FROM` is `uncollectedOf(spaceId)`. Their test is
`payments/totals.api.test.ts`. The debts' route reads exactly these (D12) — do not write a second balance query.
`payments.md` and conventions §9 *Composed reads* already describe them; your `payments.md` lines add the income
aggregates (C5) and the finance link (`finance.md`) where C4 wrote "the `finance` module".

## Specifics the lead fixes for you

- **EC4 (the cost on a generated year) is the lead's**, run once after the joins: do not build `year.sql`. Write your
  SQL so each statement can be measured (one statement per function, as D10/D11 say).
- **Shared files — your lines only:**
  - `apps/api/src/app.ts`: **only** the `finance` construction (its `createReadSnapshot()` as `desk`'s, R9) placed
    directly after the `payments` service's construction, and **one** line `manage.use('/finance',
    createFinanceManageRouter(financeController));` beside the other manage mounts. Nothing else.
  - `packages/shared/src/core/gazaTime.ts` and its unit test: `monthOf`, `addMonths` **appended at the file's end**
    (lane O appends `lastDaysSince` there too; the lead joins them, yours first).
  - `payments.repository.ts` / `payments.service.ts` / `payments/index.ts`: your functions **below** C4's (after
    `uncollectedTotals`), nothing of C4's changed. EC3: `balancesOf` unchanged.
  - `docs/api/api-contract.md`: your own new section **Finance** after *Front desk (managed)* (and in the contract's
    section list, if it has one, in the same place). Nothing in other sections.
  - `docs/backend/conventions.md`: only §7's table row for `finance` (*Holds*: the four reads). **Not** the header's
    *Built* line (C16, the lead's) and not §9.
  - `docs/backend/security.md`: one bullet under *Authorization* (the four routes `requireCan('finance.read')`).
  - `docs/architecture/data-model.md`: *Derived values* — *Income*, *Collections* (C5), *Occupancy statistics* (C7).
  - `docs/features/payments.md`: the income aggregates and the link to `finance.md`.
- **Never touch:** `can.ts` (`finance.read` exists, R7), `overview`, `docs/plans/v1-mvp.md`,
  `docs/project/overview.md`, `docs/README.md`, `foundation.md` (C16 and lane O write those). Tell the lead in your
  reply what C16 must write for finance (v1-mvp's finance row and step 11 *Built*, `overview.md`'s *Built* line,
  `docs/README.md`'s map line for `finance.md`, conventions' *Built*).
- **The month:** `month` invalid → `validation` 422 `invalid_format` (the shared schema); out of the 24 months →
  `validation` 422 `out_of_range` on `month` — use the platform's existing way of answering a field code from a
  service (look at how another module answers `out_of_range` for a query field, e.g. the payments list's range in
  `paymentsWindow.ts`), never a new error code.
- **Clock:** every "now" through the service's injected `now` (tests `createTestApp({ clock })`), never `new Date()`.
- **Money in the API is agorot integers** end to end; never a float of money. Averages of presence and attendance
  are the one-decimal numbers D11 defines (not money).
- **The occupancy's month figures** read the month's window up to now (D11's last bullet); `byDay` 14 Gaza days
  ending today, `byHour` the 28 days before today.
- `docs/features/finance.md` follows `docs/architecture/documentation.md` §5's capability template (API parts only;
  *Who uses it* names the owner's Finance screen (19) to come, worker A's).

## Tell the lead in your reply (beside LANE_COMMON's list)

- The exact `app.ts` lines you added and where; the `gazaTime.ts` functions appended; every function added to
  `payments` (signature).
- EC2's result (does `unnest(…) WITH ORDINALITY` bind through `Prisma.sql`), EC3, EC6.
- For the real run: the four routes' exact paths and query parameters, and the SQL that cross-checks R2 (the month's
  income, the debtors' count **archived included**, the 14 days' closed visits by Gaza check-in day).
