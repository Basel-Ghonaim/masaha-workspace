# Lane O — the owner's and the admin's overviews (C8–C11)

- **Worktree:** `C:\dev\masaha\app-b-lane-o` · **branch:** `lane/o` (checked out) · **base:** `b0cd0ae4` (the lead's
  C1–C4 on `origin/main` `d40d20f5`) · **test database:** `masaha_b_lane_o_test` (set in the worktree's
  `apps/api/.env`, migrated) · **scripts folder:** `C:\dev\masaha\workspace\WORKER_B\BACKEND_FINAL\scripts\lane-o\`
  (create it) · **grant tag:** `lane-o` · **finding numbers:** 158, 159 (more: 194, 195, and say so).
- The rules: `LANE_COMMON.md` (beside this file) — read it first, whole.

## What you build — four commits, in this order

| # | Subject (exact) | Holds (the plan's §8.1) |
|---|---|---|
| C8 | `feat(api): count what the owner's overview shows` | `spaces.freshnessOf` + `staleDays`, `dataReports.openCountOf`, `visits.unpricedCount`, `subscriptions.endingSoon`, `announcements.runningTypes`, `occupancy.glance`; U-O1; T-M1–T-M6; the *Behaviour* lines of `spaces.md`, `data-reports.md`, `visits.md`, `subscriptions.md`, `announcements.md`, `occupancy.md` |
| C9 | `feat(overview): read the owner's overview` | shared `overview` (owner part); the module, its manage route; `space.overview.read`; T-O1–T-O6; contract *Overview* (owner); conventions §9 *`overview`*; security; `overview.md` (first); foundation §13's screen-12 line (OV8) |
| C10 | `feat(api): count what the admin's overview shows` | `ListingService.count`, `adminSpaces.counts`, `staleEditable`, `dataReports.openCounts`, `users.countCreatedSince`, `lastDaysSince` (+ `auditPeriod.ts`); **OD3 (a): `GET /admin/spaces` gains `status=editable`** (unverified, hidden included; with `stale=true` it is «اكتمال البيانات»'s «عرض الكل»; the card's total equals that list's); U-O2; T-M7–T-M10; `space-links.md`, `data-reports.md`, `users.md` lines |
| C11 | `feat(overview): read the admin's overview` | shared `overview` (admin part); the admin route; T-O7–T-O11; contract; `overview.md`; **OD4: `can()`'s unused `platform.stats.read` removed** (and its unit-test line) |

**Read in the plan:** the approval note (OD1 (a) with the first five names; OD2 (a); OD3 (a) in C10; OD4); §2.3–§2.4
(the owner's overview decisions OV1–OV8, O3, A8 — binding); §3.2 (AC-O1–AC-O7); §4.2; §5.1 (the overview routes,
mounts, placement and levels); §5.2 D16 (the shared shapes); §5.4 D20–D24 (every figure, its owning module, the new
set-based function, its query); §5.6 S20–S26; §5.7 A10–A13 (not taken); §7 *Units U3, U4*; §8.1–§8.3; §9.4–§9.5
(every test and break: U-O1, U-O2, T-M1–T-M10, T-O1–T-O11, B-O1–B-O10, B-M1–B-M10); §9.7–§9.8; §11.1 items 1, 3–6;
§13 EC5, EC8, EC9, EC11, EC14.

## What the lead's C4 already gives you (on your base)

`payments.service.ts`: `balanceTotals(spaceId, at, tx?)` → `{ owed: { agorot, customers }, credit: {…} }` and
`uncollectedTotals(spaceId, tx?)` → `{ visits, owedAgorot, unpriced }`. The owner's overview reads
`balanceTotals(…).owed.customers` and `uncollectedTotals(…).visits` and **drops every amount** (D10, OV1–OV2).

## Specifics the lead fixes for you

- **T-O2's debtors' comparison:** the finance route (`…/finance/debts`) is lane F's and does not exist on your base.
  In T-O2, compare `customersOwing` with the **payments service's** `balanceTotals(spaceId, at).owed.customers` (an
  archived debtor included — B-O3), and mark the spot with the comment `// The lead adds finance/debts' total at the
  join.` The lead folds the route comparison into C9 after joining lane F.
- **C10's data-reports helper — write it exactly as below** (lane L writes the same text in the same place for its
  `handledBy` filter, so the join merges cleanly): in `apps/api/src/modules/data-reports/data-reports.repository.ts`,
  **directly after the `statusWhere` function** and before `const NEWEST_FIRST`:

  ```ts
  /** Who handles a report, as a condition: the admin an unverified space's, its owners a verified one's. */
  function handledByWhere(
    verifiedIds: readonly number[],
    handledBy: 'ADMIN' | 'OWNER' | undefined,
  ): Prisma.DataReportWhereInput {
    if (handledBy === 'ADMIN') return { spaceId: { notIn: [...verifiedIds] } };
    if (handledBy === 'OWNER') return { spaceId: { in: [...verifiedIds] } };
    return {};
  }
  ```

  (one blank line before and after it). `openCounts` counts the open reports of live spaces (`space: { deletedAt:
  null }`, `status: 'OPEN'`) in all, with `handledByWhere(verifiedIds, 'ADMIN')`, and with `'OWNER'` (D20; three
  counts in parallel or one `groupBy` — your choice, recorded).
- **EC4 (the cost on a generated year) is the lead's**, after the joins: do not build `year.sql`.
- **Shared files — your lines only:**
  - `apps/api/src/app.ts`: the listing service kept in a `const` (EC11, no behaviour change); the `overview`
    construction placed **directly after `auditLog`'s**; and two mount lines, `manage.use('/overview', …)` beside the
    other manage mounts and `admin.use('/overview', …)` beside the other admin mounts. Nothing else.
  - `packages/shared/src/core/gazaTime.ts` and its unit test: `lastDaysSince` **appended at the file's end** (lane F
    appends `monthOf`/`addMonths` there; the lead joins them). `audit/auditPeriod.ts` then calls it (its unit test
    unchanged and green).
  - `apps/api/src/shared/auth/can.ts` (+ unit test): `'space.overview.read': 'owner'` beside `finance.read` (C9);
    `platform.stats.read` removed (C11).
  - `docs/api/api-contract.md`: your own new section **Overview** after *Audit log* (and in the contract's section list
    if it has one); the *Admin spaces* section's `status` values gain `editable` (C10, your lines). Nothing else.
  - `docs/backend/conventions.md`: §7's table row for `overview`; §9's *`overview`* section (D20's owners, no
    repository, no snapshot). **Not** the header's *Built* line (C16) and not §9 *Composed reads* (C4 wrote it).
  - `docs/backend/security.md`: one bullet under *Authorization* (the owner's overview `space.overview.read`; the
    admin's behind `/admin`).
  - `docs/frontend/design-system/foundation.md` §13: only the screen-12 line, as the plan's §11.1 item 6 gives it.
  - the feature documents of the modules you add a function to: one *Behaviour* line each (and *Who uses it*: the
    overview); `users.md`, `data-reports.md` and `visits.md` are touched by lane L too — keep your lines separate.
- **Never touch:** `finance`, `payments` (beyond reading it), `docs/plans/v1-mvp.md`, `docs/project/overview.md`,
  `docs/README.md`, `docs/architecture/data-model.md`. Tell the lead in your reply what C16 must write for the overviews
  (v1-mvp's step 12 *Built*, the `/admin/stats` row → `GET /admin/overview` (OD4), a `GET …/overview` row; the *Built*
  lines; `docs/README.md`'s map line for `overview.md`; conventions' *Built*).
- **No amount anywhere** in `OwnerOverview` (T-O3 searches the serialised body for `Agorot`); nothing of a space's
  operations in `AdminOverview` (T-O11). **No snapshot** on either (S21); one `Promise.all` each (D21).
- **Clock:** every "now" through the injected `now` (tests `createTestApp({ clock })`), never `new Date()`.
- `docs/features/overview.md` follows `docs/architecture/documentation.md` §5's capability template (API parts only;
  *Who uses it* names screens 12 and 25 to come, worker A's).

## Tell the lead in your reply (beside LANE_COMMON's list)

- The exact `app.ts` lines you added and where; `lastDaysSince`'s text; each new set-based function (module,
  signature).
- EC5, EC8, EC9, EC11, EC14's results.
- For the real run: the two routes, and for each figure the list route it must equal (path and query).
