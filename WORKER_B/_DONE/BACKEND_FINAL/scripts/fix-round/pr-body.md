## Summary

The rest of v1's API, in one PR as the owner ordered (OD11): **the space's finance** (build map step 11's last part), **the owner's and the admin's overviews** (step 12), and **the API items left** — #130's review fixes, findings 153, 97, 170, 167 and 161, `GET`/`PATCH /me` and a space's visits by day. No migration, no new error code, no dependency, no `apps/web` file. Built from the approved plan `BACKEND_FINAL/2_PLAN.md` (OD1–OD11 as recommended).

16 commits, in units: U0 #130's fixes (1–3) · U1 the ledger's totals (4) · U5 the items left (5–8) · U2 finance (9–11) · U4 the overviews (12–15) · U6 the closing documents (16).

## Part one — finance (`GET /manage/spaces/:spaceId/finance/{income|debts|payers|occupancy}`, 🏢 `finance.read`)

- [x] **AC-F1** a month's income (`YYYY-MM`, the current Gaza month by default, 23 back at most, never ahead) by subscriptions and visits, the month before, today, all time with its first day, the last 12 months and the visits' last 30 Gaza days, each staff member's collections by method — voided payments left out, counted on the Gaza day received. *Met by* `payments.incomeIn` (one statement, every window a pair of instants through `unnest … WITH ORDINALITY`), `collectionsIn`, `firstReceivedAt`; in one `REPEATABLE READ` snapshot. Tests `finance/income.api.test.ts` (T-F2–T-F6), `windows.unit.test.ts`.
- [x] **AC-F2** who owes (largest first, paged, phone, `archived`, the oldest item still owing and its day), who is in credit, the totals and the reminder template, from one snapshot. *Met by* `payments.balancesPage` / `balanceTotals` / `uncollectedTotals` (commit 4, the one balance rule) and `debts.api.test.ts` (T-F7–T-F10).
- [x] **AC-F3** who paid in the month, the latest first, paged — `payers.api.test.ts` (T-F11).
- [x] **AC-F4** occupancy from closed stays (the auto check-out's included): 14 days by day (a member once a day), the average present per Gaza weekday and hour over the 28 days before today, the month's average stay, peak hour and daily attendance — `occupancyGrid.unit.test.ts`, `occupancy.api.test.ts` (T-F12–T-F14).
- [x] **AC-F5** reception 403 before the query is read; a stranger, another space's owner and the admin `not_found`; another space's money never counted — `access.api.test.ts` (T-F1), T-F5.
- No export route: the web builds the CSV from the JSON (the owner's decision 5).

## Part two — the overviews (`GET /manage/spaces/:spaceId/overview` 🏢 `space.overview.read`; `GET /admin/overview` 🛡)

- [x] **AC-O1** the owner's work queue in one answer, **no amount anywhere**: groups missing and stale (by the saved thresholds) with their days, open reports, uncollected and unpriced visits, closures awaiting their extension, capacity set, customers who owe (a count), present now with capacity and the live status, ending soon (count and first five), running announcements and their types.
- [x] **AC-O2** each count equals the list it links to, read in the same test (`ownerOverview.api.test.ts` T-O2, including `…/finance/debts`' `meta.totals.owed.customers`).
- [x] **AC-O3** reception 403; stranger, another owner, the admin `not_found`; the serialised body searched for `agorot` (T-O3).
- [x] **AC-O4** the admin's tiles: verified, unverified (= unverified with no owner, OD2), hidden, stale or missing, open reports split by who handles them, new users of the last 30 Gaza days, «اكتمال البيانات» (first five and total, hidden included) — each equal to `GET /admin/spaces?status=…` / `?stale=true` / `?status=editable&stale=true` (OD3) / `GET /admin/data-reports` (`adminOverview.api.test.ts`).
- [x] **AC-O5** a saved threshold changes both overviews at once (T-O10).
- [x] **AC-O6** guest 401, user and owner 403, pending password 403 `PASSWORD_CHANGE_REQUIRED`; nothing of a space's operations in the admin's body (T-O11).
- [x] **AC-O7** no write, no polling route. Every figure from its owning module's new set-based function (commits 12, 14); `overview` has no repository and reads no snapshot (S20, S21). `platform.stats.read` removed (OD4).

## Part three — the items left

- [x] **AC-L1** (F1) a contact stored in another form answered as stored; the next save stores its one form, audited exactly (commit 1).
- [x] **AC-L2** (153, F2) the seed reads the contact through `emailSchema`/`phoneSchema`; a foreign number fails the seed naming its variable (commit 2; `seedEnv.unit.test.ts`).
- [x] **AC-L3** (F3, F4) "in the browser too" dropped; "changes no value" (commit 1).
- [x] **AC-L4** (97) resolved (commit 3).
- [x] **AC-L5** (170) the idle check and the rotation read the family's latest activity; a race test (commit 5).
- [x] **AC-L6** `GET`/`PATCH /me` — name and language, audited `user.profileEdited` (never on the admin's log) (commit 6).
- [x] **AC-L7** (161) `GET …/visits?from&to` — the owner any range ≤ 92 days, reception today only (commit 8).
- [x] **AC-L8** (167) `GET /admin/data-reports?handledBy=ADMIN|OWNER` (commit 7).

## Carried from #130 (review F1–F4)

F1 → commit 1 (T-L1, T-L2, the contract sentence) · F2 → commit 2 (finding 153's wording and foreign-number case, then resolved) · F3, F4 → commit 1.

## Findings

Resolved: **153**, **97**, **170**, **167**, **161**. Recorded: **193** — an auto-closed visit left to a customer is both in that customer's debt and in the uncollected count (the review's R2-F1, for the owner's decision); **158** — the admin's spaces list's `editable` status lives in a second shared schema for the API (widening the web's status list breaks its typecheck; the web's screen 25 will take it). Not taken (as the plan): 152 (OD9), 171 (OD10), 187.

## How it was built — the lanes and the joins

A lead and three sub-agents, each in its own worktree with its own test database (`masaha_b_lane_{l,f,o}_test`, dropped after): the lead built commits 1–4; lane L the items left, lane F finance, lane O the overviews; each lane passed lint, typecheck, `test:unit` and the full `test:api` on its own database before its join. Joined by rebase in the order L, F, O (no merge commit); the conflicts (`app.ts`'s mounts, `gazaTime.ts`, conventions §7, `security.md`, the data-reports repository) kept both sides. One fold at the join: T-O2 compares with the finance route (its test space given its settings row, as every space has).

## Local verification (on the head before the number was set)

| Command | Result |
|---|---|
| `npm run build -w @masaha/shared` | 0 |
| `npm run lint` · `npm run typecheck` | 0 · 0 |
| `npm run test:unit` | shared 271, api 902, web 1075 passed |
| `npm run test:api` | **114 files, 1319 tests passed** |
| `npm run test:component` | 1742 / 1744 — site `routes.component.test.tsx` 2 × 3 s waits while `test:api` ran (finding 87's family; no web file changed); alone, machine quiet: 13 / 13 |
| `NODE_ENV=production npm run build` + `npm run check:build` | 0 · 0 |
| `check:classes` · `check:links` · `check:conflicts` · `format:check` | 0 · 0 (3112 links) · 0 · 0 |

**Cost on a generated year** (300 spaces, 5 000 users, 99 000 visits, 107 120 payments): every new route 30–190 ms; 171 statements, **none over 150 ms** (the slowest 49 ms) — no index proposed (Q5).

## The real run (`masaha_b_dev`, API on 3321) — ALL PASS, 56 cases

The four finance reads 200, cross-checked by SQL (the month's income, the debtors archived included, the 14 days' closed visits by Gaza day); reception 403, the admin and the directory owner 404 on each. The owner's overview: no `agorot`, each count = its list, customers owing = debts' total; reception 403. The admin's overview: each tile = its list, new users = SQL. A threshold saved changes both overviews and is put back. The public contact answered as stored. `/me` read and the language changed and changed back. The visits by day: the owner 200, reception with a range 403. Writes (named, put back): two `platformSettings.stalenessEdited`, two `user.profileEdited` entries.

## Decisions taken without the owner (none SERIOUS)

- The seed's environment schema moved to `seedEnv.ts` with a unit test (EC7: `run.ts` seeds on import).
- 170: the rotation reads the family's latest activity too (else a refresh of the new token would still see itself idle).
- `PATCH /me {}` answers 200 writing nothing (as every partial PATCH); a suspended account is 401 (the guard's).
- `handledBy` joined by `AND: [...]` (a spread lost the `spaceId` filter — its test caught it).
- The visits range is the owner's by `can('payments.read')`; `visits` (L3) cannot import `payments`' window, so the same Gaza-midnight rule locally, bound 92 days.
- All time `-infinity`..`infinity`; `contactsOf`'s `archived` kept out of the check-ins' answer.
- OD3's `editable` in a second API schema (finding 158); `endingSoon` counted through the customers list's own query (EC8); `hasPhotos` dropped (EC9 failed: the listing has no photo count).
- EC4 measured once on the joined code rather than per lane.

## Review fixes (2026-10-29)

The three reviews (R1 the foundation and the items left, R2 finance, R3 the overviews and the documents): no blocker; every finding fixed, each folded into the commit that made its lines (subjects unchanged, no fix commit).

- **R2-F1 (should-fix) — finance's `owed` and `uncollected` overlap.** The contract (*Finance*), `finance.md` and the `DebtsMeta` comment now say what the code does: the uncollected count is the desk's list, which keeps an auto-closed visit left to a customer, so its rest is also in that customer's debt, and the two figures are never added. Pinned by a test in `debts.api.test.ts` (in `owed`, in `uncollected` and on the desk's list); red by a break that dropped visits with a customer from `uncollectedOf` (`uncollected` 0 ≠ 1), green after. `overview.md` says the overview's consequence (`uncollectedVisits` and `customersOwing` both count such a visit). **Finding 193** recorded for the owner: whether finance's `uncollected` should leave out a visit with a customer (it cannot change the shared count, which AC-O2 keeps equal to the desk's list). → `feat(finance): read who owes and who paid`; `finance.md` → `…occupancy` (its last writer); the overview's lines → `feat(overview): read the owner's overview`.
- **R2-F2** — `finance.md`: income reads 46 windows, not 45. → `feat(finance): read a space's occupancy`.
- **R2-F3** — `todayWindow`, used by a test only, removed; its unit case asserts `dayWindow` of today's date. → `feat(finance): read a space's income`.
- **R3-F1 (should-fix)** — `announcements.md`: `runningTypes` is one query of the running ones, each type kept once by Prisma's `distinct` in memory, not a SQL `DISTINCT` (the code unchanged). → `feat(api): count what the owner's overview shows`.
- **R3-F2** — conventions §9 *Composed reads*: the owner's overview *reads* `closures.summary`. → `feat(overview): read the owner's overview`.
- **R3-F3** — `occupancy.glance`'s `at` is required; its test passes its clock. → `feat(api): count what the owner's overview shows`.
- **R1-F1** — `visits.service.ts`: `terms`'s doc comment back on `terms`. → `feat(visits): list a space's visits by day`.
- **R1-F2** — `payments.md` *Who uses it*: the desk's web sentences back under the front desk bullet (→ `feat(payments): total a space's balances`, carried through the two finance commits that rewrote the Finance bullet); "will count" → "counts" (→ `feat(overview): read the owner's overview`, which built the count).
- **R1-F3** — `apps/api/.env.example`: the seed's WhatsApp is a Palestinian or Israeli number, read by the phone rule in any typed form and stored in its one E.164 form. → `fix(seed): store the contact in its one form`.

On the new head: `lint`, `typecheck`, `test:unit`, `test:api`, `format:check`, `check:links`, `check:conflicts` all pass.

## Left out

Nothing.

