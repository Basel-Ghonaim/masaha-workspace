# FINANCE_AUDIT — the audit reader, the platform settings and the space's finance, on the API (build map step 11) — the plan

> **Approved by the owner, 2026-10-27 — binding on every executor of this plan** (it wins where the plan below
> differs): **§13 Q1–Q12 as recommended**, S1–S12 as planned.
> - **The base, corrected:** `main` = `39ef0504` — **#123 merged** (`e6737da5`; its tree equals the head `ff8743c8`
>   this plan read) and **#124 merged** (worker A's subscription sheet: `apps/web` and documents — among them
>   `features/subscriptions.md`, `overview.md`, the findings index; re-read them on `main` before editing). §12.1's
>   base diff runs from `3855e37f`.
> - **Q10:** decision 10 kept (entries kept for ever) and **finding 152** recorded by PR 1 (a retention rule decided
>   before Neon's 0.5 GB). **Q12:** the documents this plan proves wrong are changed in their PRs as written.
> - **Q5 under the run's rule:** a read over 150 ms on the generated year is **recorded, not indexed** — no migration
>   without the owner; the executor continues and the owner decides at the review.
> - **Every execution runs under the owner's autonomy rule** (`C:\dev\masaha\workspace\_SHARED\AUTONOMY_2026-10-25.md`):
>   no stop until ready for review (PR open, CI green, `CLEAN`, report); each "stop and ask" of this plan becomes
>   decide, record under *Decisions taken without the owner*, continue — within the rule's hard limits. No stop for
>   the file count. Fix rounds run only the touched test files; CI judges the rest.
> - **Moved folders:** the finished task folders are under `_DONE` now — read `WORKER_B\ANNOUNCEMENTS\…`,
>   `WORKER_B\PAYMENTS\…`, `WORKER_B\SUBSCRIPTIONS\…`, `WORKER_B\DESK_API\…`, `WORKER_A\DESK_SCREENS\…` as
>   `WORKER_B\_DONE\…` / `WORKER_A\_DONE\…` (the plan's paths are already rewritten where found).
> - **Tracking:** the owner's Issue for this plan lists each PR's acceptance criteria; the supervisor ticks each PR's
>   box once it merges.

> **Base:** `origin/main` at `3855e37f` (Merge #122, `feat/customers-file`, 2026-10-26). **#123**
> (`feat/closure-extension`, ANNOUNCEMENTS PR 4) was **not merged** when this plan was written: it is read
> **as merged**, at its head `ff8743c8` (it only adds: a migration, the extension's routes, two codes). PR 1's
> executor starts only once #123 has merged (§12.1 checks it).
> **Worker:** B, in `C:\dev\masaha\app-b`. **Folder:** `C:\dev\masaha\workspace\WORKER_B\FINANCE_AUDIT\`: this
> plan `2_PLAN.md`; the reports `4_REPORT_PR<n>.md`; the executor's scripts in `scripts\` (never committed).
> **Three PRs in sequence**, each cut from the latest `origin/main` once the one before it has merged:
> - **PR 1** `feat/audit-log` — `feat(audit): read the owner's and admin's logs` (46) — ≈ 36 files, **no
>   migration**; opens with the four items carried from #123 (finding 151 among them).
> - **PR 2** `feat/platform-settings` — `feat(platform-settings): edit defaults and contact` (50) — ≈ 32 files, no
>   migration; resolves finding 40.
> - **PR 3** `feat/finance` — `feat(finance): read a space's money and occupancy` (49) — ≈ 36 files, no migration
>   unless §12.2's measurement asks the owner for an index.
> Each touches authorization (PR 1 privacy, PR 3 the owner's money) and transactions or locks: each gets its own
> review conversation (workflow §2, phase 7).
> **Read only from commit objects** (`git show origin/main:…`, `git show ff8743c8:…`, `git grep`, `git ls-tree`,
> `gh`). Nothing was run, built, installed or checked out. Every point reading could not prove is an **executor
> check** (§12.2), with what to do if it fails.
> **Beside it:** worker A finishes DESK_SCREENS PR 4 (#124's fix round: `apps/web`, `docs`), then the public
> site's fix PR, later the screens of steps 9–11. **This item plans no change in `apps/web`** (no new error code,
> §13 Q12). **Shared documents, each a likely text conflict:** `docs/api/api-contract.md`,
> `docs/backend/conventions.md`, `docs/architecture/data-model.md`, `docs/backend/security.md`,
> `docs/plans/v1-mvp.md`, `docs/project/overview.md`, `docs/README.md`,
> `docs/architecture/findings/README.md`, and the capability documents worker A's web parts may touch
> (`features/subscriptions.md`, `payments.md`, `space-settings.md`). **The web's two `errors.ts`** are shared only
> if an executor needs a code this plan does not name — then it stops and asks (§12.9).
> **Finding numbers:** **151** is the carried file's (written and resolved by PR 1, C0a). This item's own start at
> **152**; one is planned if the owner approves it (§13 Q10).

---

## 1. Summary

Step 11's API: the owner reads the space's money and occupancy; the owner and the admin read their audit logs;
the admin edits the platform's settings.

- **PR 1 — the audit reader.** First the carried items: an extension also moves each covered subscription's
  renewal chain that has not started (finding 151, the owner's option A), a key retried against another space's
  URL is a conflict, two document corrections. Then the `audit` module (L5, a read model, R7): the owner's log of
  the space — every entry, the admin shown as **Masaha** — and the admin's log of the platform's events only, by a
  default-deny allowlist; both paged, newest first, the last 30 days by default or all time, searched by the
  target's name, filtered by actor and action.
- **PR 2 — the platform settings.** The admin reads and saves three cards, each its own resource and save: the
  new-space defaults, the staleness thresholds, and the platform's contact, which joins the typed key catalogue
  (finding 40). Anyone reads the contact (`GET /settings/public`). Each save audited, on the admin's list.
- **PR 3 — the finance read model.** The owner alone (`finance.read`) reads four tabs' figures, each aggregated by
  the server on Gaza's calendar: income (cash collected, voided payments left out) for a chosen month against the
  month before, today, all time, the last 12 months, the visits' last 30 days and each staff member's collections
  by method; who owes (largest first, since when, the oldest item, the phone and the space's reminder text) and
  who is in credit, with the totals; who paid in the month; occupancy from closed stays (members and visits per
  day over 14 days, the average present per hour over 4 weeks, the month's average stay, peak hour and daily
  attendance). No export route: the web builds its CSV from these answers.

No booking, online payment, QR, claiming or reviews (overview *Not in v1*); no expenses, no consolidated finance
across spaces (*Not in v1*); no notification (a reminder stays a WhatsApp link a person sends).

---

## 2. The contract

### Scope

**PR 1 — `feat/audit-log`**
0. **Carried from #123** (`0_CARRIED_FROM_123.md`, decided by the owner): (1) finding 151, option A — the extension
   moves each covered subscription's not-yet-started renewal chain, start and end, by the same days, under the same
   locks, linked and audited; (2) a key that extended another space's closure is a `conflict`; (3) `data-model.md`
   line 23; (4) `subscriptions.md`'s history order.
1. `@masaha/shared/audit` (new, L5): the queries, `AuditEntry`, `AUDIT_ACTIONS`, `AUDIT_ENTITY_TYPES`.
2. The `audit` module (L5, reads `audit_logs`, writes nothing): `GET /manage/spaces/:spaceId/audit-log` (🏢
   `requireCan('space.auditLog.read')`) and `GET /admin/audit-log` (🛡).
3. The admin's allowlist (`audit/platformEvents.ts`, pure): the platform's event types, default deny.
4. `docs/features/audit.md` (new); the contract's *Audit log*; conventions §6 (the reader built), security; finding
   151 (new, resolved).

**PR 2 — `feat/platform-settings`**
1. `@masaha/shared/platform-settings` (new, L0): the thresholds' and the contact's schemas and shapes;
   `@masaha/shared/space-settings` gains `newSpaceDefaultsSchema` (moved from the API's catalogue, §5 S9).
2. The catalogue gains `contactEmail` and `contactWhatsapp` (optional keys): finding 40 resolved.
3. `GET` and `PUT /admin/settings/{new-space-defaults|staleness|contact}` (🛡), one resource per card (AD-029);
   `GET /settings/public` (🌐).
4. Audit `platformSettings.newSpaceDefaultsEdited`, `.stalenessEdited`, `.contactEdited`, on the admin's
   allowlist; the audit writer takes an entry with no entity id (a setting has none).
5. `docs/features/platform-settings.md` (new).

**PR 3 — `feat/finance`**
1. `@masaha/shared/finance` (new, L5): the queries and the four answers; `core/gazaTime.ts` gains the month's
   calendar (`monthOf`, `addMonths`).
2. The `finance` module (L5, R7): `GET /manage/spaces/:spaceId/finance/{income|debts|payers|occupancy}` (🏢
   `requireCan('finance.read')`).
3. `payments` gains the ledger's aggregates (income by windows, collections, the balances' page and totals, the
   uncollected totals); `customers.contactsOf` answers `archived` too.
4. `docs/features/finance.md` (new); `OPEN_DECISIONS.md` point 3 updated by the report.

### Acceptance criteria

**PR 1 — carried**
- [ ] An extension moves every covered subscription's end, and each renewal of one that has not started (start
      after today in Gaza, not ended early) — and that renewal's own renewal, and so on — start and end, by the same
      days; one link each; audited `after: { days, subscriptionIds, renewalIds }`. The review's scenario: S 11-01 →
      11-30, R 12-01 → 12-30, a closure 11-08 → 11-10 extended by 3 → S ends 12-03, R runs 12-04 → 01-02.
- [ ] A renewal already started, or ended early, is not moved; the preview's count is what the extension will move,
      the chain included.
- [ ] A key that extended a closure of another space is `conflict` (409, no code), answering nothing of it.

**PR 1 — the audit reader**
- [ ] The owner reads every entry of the space (its staff's, the system's, the admin's), newest first, paged
      (§4); another space's never. The admin's actor is `MASAHA` with no id or name; a staff member's is named,
      even after their link ended; the system's is `SYSTEM`.
- [ ] Each entry carries its action, time, actor, target (type, id, its current name where it has one, whether it
      is deleted), and `before` / `after` as stored.
- [ ] `period=LAST_30_DAYS` (the default: from the Gaza midnight 29 days before today) or `ALL`; `q` finds the
      entries whose target's name holds it (Arabic folded); `actor` and `actions` narrow; every filter applies
      before the page is cut, the total right; `meta.actors` lists the actors of the period, each once.
- [ ] Reception is 403 before the query is read; a stranger, another space's owner and the admin `not_found`.
- [ ] The admin reads only the platform's events, of every space and of none: spaces created, edited, confirmed,
      their photos, hidden, shown, deleted, restored; owners linked and unlinked; accounts created, suspended,
      restored, their role, temporary passwords and handovers, an email corrected — those naming no space; lookups;
      data reports decided; the platform's settings (PR 2). **Never** an entry about a space's customers,
      subscriptions, check-ins, visits, payments, packages, announcements or closure extensions, its capacity, its
      live-status override, its settings or its staff (an owner's reception account's events included).
- [ ] The admin's `q` also finds every entry of a space by the space's name; each entry carries its space.

**PR 2**
- [ ] The admin reads and saves each card on its own; a save answers the card as saved; only what changed is
      audited, an unchanged save writes nothing; a refusal 422 on its field writes nothing.
- [ ] A new default applies to the next space created, never to an existing one; a new threshold applies at once.
- [ ] The contact: an email (lowercased) and a WhatsApp number (normalised, Palestinian or Israeli), each or both
      `null` to clear; `GET /settings/public` answers both, `null` while unset, `Cache-Control: public, max-age=300`.
- [ ] Two saves of one card at once: the second's `before` is the first's `after`; two first saves of the contact
      make one row per key.
- [ ] A non-admin is 403 on every admin route, a guest 401; the admin's log shows the three settings actions.

**PR 3**
- [ ] Income for a month (`YYYY-MM`, the current Gaza month by default, at most 23 months back, never ahead): its
      total by subscriptions and visits, the month before, today and all time (with its first day), the last 12
      months and the visits' last 30 days by Gaza day, each staff member's collections by method — every figure the
      payments not voided, counted on the Gaza day received.
- [ ] Who owes: each customer's debt (the balance rule of `payments`), largest first, paged, with the phone, whether
      archived, and the oldest item still owing with its day; who is in credit (`state=CREDIT`), largest first; the
      totals (owed, in credit, the uncollected visits apart) and the space's reminder template, all from one
      snapshot.
- [ ] Who paid in the month: each customer with what they paid then, the latest paid first, paged.
- [ ] Occupancy from closed stays (the auto check-out's included): visits and members per day over the last 14
      days (a member once a day); the average present per Gaza weekday and hour over the 28 days before today;
      the month's average stay (all, members, visits), peak hour and average daily attendance.
- [ ] Only the owner reads them: reception 403 before the query is read; a stranger, another space's owner and the
      admin `not_found`; another space's money never counted.

### Out of scope
- The screens 19, 24's rest, 31 and 32: worker A's later items, once this API has merged. Any `apps/web` change.
- An export route (decision 5); a free date range on finance (decision 3) or on the audit logs (§13 Q8).
- Expenses, profit, consolidated finance (*Not in v1*); a debt reminder sent by Masaha (a WhatsApp link only).
- A retention job for the audit (decision 10); the overview (step 12) — it will reuse §4 D10's functions.
- Moving the site's contact from `VITE_CONTACT_*` to `GET /settings/public` (worker A's).
- The admin's stats (`GET /admin/stats`, step 12).

---

## 3. The reading done, and what it changed

From `origin/main` at `3855e37f` and #123's head `ff8743c8`: `CLAUDE.md`; `docs/development/workflow.md` (whole),
`testing.md` (whole); `docs/backend/conventions.md` (whole); `security.md` (the header, *Authorization*, *Rate
limits*); ADR 0002, 0009, 0010, 0014 (their rules on privacy, money, size); `docs/architecture/data-model.md`
(whole); `docs/api/api-contract.md` (§1–§4, *Settings (managed)*, *Front desk (managed)* with the payments list,
*Announcements (managed)*, *Internal*, *Lookups (public)*, the admin's sections, §6); `docs/plans/v1-mvp.md`
(steps 9–12, the ordering notes, the route tables); `docs/project/overview.md` (whole); `docs/README.md` (the map,
the deferred documents); `docs/architecture/documentation.md` §5; the findings index, findings 14, 40, 120, 127,
164; `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_OWNER.md` (the money note O3 at its top, O11–O13, OW-015,
OW-016), `DECISIONS_ADMIN.md` (A7, AD-028, AD-029), `DECISIONS_SHARED.md` (P3); the prototypes `Finance.html`,
`masaha/finance.jsx`, `Owner audit.html`, `Admin audit.html` and `masaha/admin-data.js`'s action list;
`_SHARED\OPEN_DECISIONS.md`; `0_CARRIED_FROM_123.md` and `WORKER_B\_DONE\ANNOUNCEMENTS\6_REVIEW_PR4_CLAUDE_CODE.md`;
`WORKER_B\_DONE\ANNOUNCEMENTS\2_PLAN.md` and `scripts\prnum-pr4.sh` (the models); the code of `shared/audit`,
`platform-settings` (whole), `payments` (repository whole, service's functions, `paymentsWindow.ts`), `customers`
(service's reads), `subscriptions` (index, `namesOf`, `renewal.ts`), `subscriptions/closures/` at `ff8743c8`
(repository whole, service's preview and extend), `visits` and `occupancy` and `space-settings` (their service
functions), `shared/auth/can.ts` (whole), every audit `action:` written (`git grep`), `users.service.ts`'s
temporary-password entries, `spaces/space/space.service.ts` and `spaces/facts/groupEdit.ts` (their actions), `app.ts`
(the mounts), `db/transaction.ts` (`readSnapshot`), `schema.prisma` (`AuditLog`, `Setting`, `Payment`, `Visit`,
`CheckIn`, `Subscription`, `Customer`, `SpaceSettings`, their indexes), the seed (`seed.ts`, `run.ts`, `lookups.ts`'s
`DEFAULT_SETTINGS`, `demo.ts`'s money and stays), `apps/api/test/{locks,spaces,admin,factories}.ts` (exports),
`packages/shared` (`package.json`'s exports, `core/{gazaTime,fields,index}.ts`, `space-settings/requests.ts`),
`eslint.config.js` (both level maps), `apps/web/scripts/dashboardOnly.ts`, the web's
`features/platform-settings/services/platformContact.ts`.

**What the reading changed:**
- **The audit table names its actor and entity by id only; the admin's role can change.** Decision 8's "Masaha" is
  decided by **links**, not the role: an actor with no link of any state to the space is the platform (S1).
- **An owner's staff account's events carry the space** (`user.temporaryPasswordIssued`, `…HandedOver` with
  `spaceId`, `users.service.ts`), while the admin's own carry none. The allowlist is therefore not actions alone:
  an account's event is the platform's only when it names no space (S5).
- **ADR 0002 and 0008 keep capacity private from the admin**: `space.capacityEdited`, `space.statusOverridden` and
  `…Cleared`, `space.settingsEdited` and the staff's `space.staff*` stay the space's (D3).
- **`AuditEntry.entityId` is required in the writer** while the column is nullable: a platform setting has no id,
  so PR 2 makes it `number | null` (S8).
- **Shared capabilities import only lower levels** (`eslint.config.js`): `@masaha/shared/platform-settings` (L0)
  cannot import `@masaha/shared/space-settings` (L0) for `VISIT_ROUNDINGS`. So the new-space defaults' schema moves
  to `space-settings` (a space's settings subset), and the admin's settings are **three resources**, one per card,
  each typed by its owner (S9) — AD-029's "each card its own save and error" by construction.
- **The seed writes the contact only when the environment gives it** (`run.ts`: `z.email()`, an E.164 regex), and
  nothing reads it (the site reads `VITE_CONTACT_*` since #107). The catalogue's read schemas accept exactly the
  stored form the seed writes; the admin's save writes the normalised form (S10). No data migration.
- **The balances already live in one query of `payments`** (`balancesOf`, the owner's decision 6). Who owes and who
  is in credit are pages of it, not a second rule (D10).
- **Gaza dates in SQL come from PostgreSQL's zone data** (`AT TIME ZONE`, finding 120), the rest from Node's. Every
  finance bucket is a window of instants computed in Node and passed as arrays, so one zone source decides and the
  `(space_id, received_at)` and `(space_id, checked_in_at)` indexes serve each window (S2; finding 127's shape
  avoided).
- **A stay never crosses midnight** (data model › Auto check-out): occupancy bounds stays by their check-in time.
- **The prototype's finance shows «اليوم» and «منذ البداية»** beside the month (data model › Income lists them):
  kept. Its «دفعوا في الشهر» is a figure of its own (D12). Its occupancy stat cards are the chosen month's; the
  heatmap and the 14 days are fixed windows (OW-015).
- **No new error code is needed:** every refusal is `validation`, `forbidden` or `not_found`. No web change.
- **Every `can()` action exists:** `space.auditLog.read`, `platform.auditLog.read`, `finance.read`,
  `platform.settings.manage`. No change to `can.ts`.
- **`audit` and `finance` are already on both level maps (L5) and on the web's dashboard-only list;
  `platform-settings` is not on it** (the site reads the contact): no lint or build-check change.

---

## 4. The decisions as built

### The owner's decisions (2026-10-26), as built
1. **Three PRs** (§1), each from `main` once the one before merged.
2. **Income is cash collected:** `voided_at IS NULL`, counted on the Gaza day received; a written-off visit is no
   income (its earlier payments stay income: they were received); debts are their own figures (D10–D12).
3. **Periods:** `month` (Gaza's calendar month) and fixed windows — 12 months, 30 days, 14 days, 4 weeks — on Gaza
   time; no free range (D9).
4. **The server aggregates:** every series and figure computed by the API, each answer bounded (D13).
5. **No export route:** the web builds CSV from the answers (the debts' phones: the owner's alone, as the route).
6. **Finance is the owner's alone:** `requireCan('finance.read')` on each route, before the query is read.
7. **Occupancy from closed stays**, the auto check-out's included, open ones excluded (D11).
8. **The owner's log:** every entry of the space, the admin's actor `MASAHA` (S1).
9. **The admin's log:** the allowlist (D3), `q` by target, `actor`, `period` `LAST_30_DAYS` | `ALL`, paged; each
   target an id and a type the web maps to a page.
10. **Kept for ever:** no retention job; §13 Q10 records what that costs.
11. **The platform settings:** defaults, thresholds and the contact, in the typed catalogue (finding 40), one
    resource and save per card (AD-029, S9).
12. **Finding 151, option A:** D2.

### D1 — routes and answers

| PR | Route | Access | Query / body | 2xx | Module |
|---|---|---|---|---|---|
| 1 | `GET /manage/spaces/:spaceId/audit-log` | 🏢 `requireCan('space.auditLog.read')` | `spaceAuditQuerySchema` | **200** `AuditEntry[]`, `meta: AuditMeta` | `audit` |
| 1 | `GET /admin/audit-log` | 🛡 | `platformAuditQuerySchema` | **200** `PlatformAuditEntry[]`, `meta: AuditMeta` | `audit` |
| 2 | `GET /admin/settings/new-space-defaults` | 🛡 | — | **200** `NewSpaceDefaults` | `platform-settings` |
| 2 | `PUT /admin/settings/new-space-defaults` | 🛡 | `newSpaceDefaultsSchema` | **200** `NewSpaceDefaults` | `platform-settings` |
| 2 | `GET /admin/settings/staleness` | 🛡 | — | **200** `StalenessThresholds` | `platform-settings` |
| 2 | `PUT /admin/settings/staleness` | 🛡 | `stalenessSchema` | **200** `StalenessThresholds` | `platform-settings` |
| 2 | `GET /admin/settings/contact` | 🛡 | — | **200** `PlatformContact` | `platform-settings` |
| 2 | `PUT /admin/settings/contact` | 🛡 | `platformContactSchema` | **200** `PlatformContact` | `platform-settings` |
| 2 | `GET /settings/public` | 🌐 | — | **200** `PlatformContact`, `Cache-Control: public, max-age=300` | `platform-settings` |
| 3 | `GET /manage/spaces/:spaceId/finance/income` | 🏢 `requireCan('finance.read')` | `?month=` | **200** `IncomeReport` | `finance` |
| 3 | `GET …/finance/debts` | 🏢 `requireCan('finance.read')` | `?state=&page=&limit=` | **200** `BalanceRow[]`, `meta: DebtsMeta` | `finance` |
| 3 | `GET …/finance/payers` | 🏢 `requireCan('finance.read')` | `?month=&page=&limit=` | **200** `Payer[]`, `meta` | `finance` |
| 3 | `GET …/finance/occupancy` | 🏢 `requireCan('finance.read')` | `?month=` | **200** `OccupancyReport` | `finance` |

- **Placement and levels** (conventions §7–§9, R7): `audit` (L5) reads `audit_logs` with the names of the targets
  and the actors (spaces, users, customers, subscriptions, packages, visits, check-ins, announcements, lookups,
  `space_managers`) in its own queries — a read model, writing nothing; it imports no module. `finance` (L5)
  imports `payments` (L4), `subscriptions` (L3), `customers` (L2), `users` (L1), `space-settings` (L0), and reads
  `visits`, `check_ins` and the payers' items in its own repository (R7: occupancy statistics are `finance`'s,
  conventions §9). `platform-settings` (L0) imports nothing new. §12.2 check 2 runs `lint` on each.
- **Routers and mounting** (`app.ts`): `manage.use('/audit-log', createAuditManageRouter(…))`;
  `admin.use('/audit-log', createAuditAdminRouter(…))`; `admin.use('/settings', createPlatformSettingsAdminRouter(…))`;
  `api.use('/settings', createPlatformSettingsPublicRouter(…))`; `manage.use('/finance', createFinanceManageRouter(…))`.
  `/admin` keeps its one guard (`requireAuth()`, `requireRole('ADMIN')`), so no admin router can leave it out.
- **Reads are read without a lock.** The finance reads whose figures must agree read **one snapshot**
  (`readSnapshot`, conventions › Composed reads): the income report, and the debts' page with its totals (S3).

### D2 — finding 151 and the key's space (carried, PR 1 C0a–C0b)

**The moved set** (`closures.repository.ts`, replacing `coveredCount` and `lockCovered`; the covered fragment
unchanged):
```sql
WITH RECURSIVE covered AS (
  SELECT "id" FROM "subscriptions" WHERE <covered(spaceId, span)>
), chain AS (
  SELECT s."id" FROM "subscriptions" s JOIN covered c ON s."renewal_of_id" = c."id"
  WHERE s."space_id" = ${spaceId} AND <pending(today)>
  UNION
  SELECT s."id" FROM "subscriptions" s JOIN chain c ON s."renewal_of_id" = c."id"
  WHERE s."space_id" = ${spaceId} AND <pending(today)>
)
-- pending(today): s."ended_at" IS NULL AND s."starts_on" IS NOT NULL AND s."starts_on" > ${today}::date
```
- `movedCount(spaceId, span, today): Promise<number>` → `SELECT (SELECT count(*) FROM covered) + (SELECT count(*)
  FROM chain WHERE "id" NOT IN (SELECT "id" FROM covered))` (the preview; no lock).
- `lockMoved(spaceId, span, today, tx): Promise<{ covered: number[]; renewals: number[] }>` → `SELECT "id", ("id" IN
  (SELECT "id" FROM chain) AND "id" NOT IN (SELECT "id" FROM covered)) AS "renewal" FROM "subscriptions" WHERE "id"
  IN (SELECT "id" FROM covered UNION SELECT "id" FROM chain) ORDER BY "id" FOR UPDATE` — one statement, the chain
  locked with the covered rows, by id (§12.2 PR 1 check 3).
- `moveRenewals(ids, days, at, tx)`: `UPDATE "subscriptions" SET "starts_on" = "starts_on" + ${days}::integer,
  "ends_on" = "ends_on" + ${days}::integer, "updated_at" = ${at} WHERE "id" = ANY(${ids}::integer[])` (an end of
  `NULL` stays `NULL`: an hours pack).
- **Why the chain only through renewals not started:** a renewal that started is running on its own days (the
  covered rule judges it); moving it would shift days already used. A renewal ended early has no days to move.
  A renewal with no start counts as started, as in the covered rule.
- **`today`** is `gazaClockOf(at).date`, at the extension's `now`.

**The extension** (`closures.service.ts` `extend`, same order and locks): … `const today =
gazaClockOf(at).date; const { covered, renewals } = await repository.lockMoved(space.id, closureSpan(closure,
at), today, tx); await repository.moveEnds(covered, days, at, tx); await repository.moveRenewals(renewals, days,
at, tx); await repository.createExtension({ … }, [...covered, ...renewals], tx);` audit `after: { days,
subscriptionIds: covered, renewalIds: renewals }`; the answer's `subscriptions: covered.length + renewals.length`.
**The preview** answers `movedCount` (§13 Q11: the chain counts, so the dialog's number is what moves, and the list's
`extension.subscriptions` — the links' count — says the same once applied).

**The key's space (item 2):** `findByKey(key, tx)` selects the extension's announcement's `spaceId`
(`announcement: { select: { spaceId: true } }`), so `ExtensionRow` gains `spaceId`; the retry branch answers
`conflict` (409, no code) when `recorded.spaceId !== space.id || recorded.announcementId !== announcementId`.
*Why `conflict`, not `not_found`:* it is what a key reused on another closure of the same space answers, so a
caller learns nothing more about another space; `not_found` would answer differently for a key that exists.

### D3 — the admin's allowlist (`audit/platformEvents.ts`, pure, PR 1; PR 2 adds three)
```ts
/** The platform's events, whatever space they name (public facts, existence, owners, lookups, reports). */
export const PLATFORM_ACTIONS = [
  'space.created', 'space.profileEdited', 'space.hoursEdited', 'space.pricesEdited', 'space.amenitiesEdited',
  'space.contactsEdited', 'space.profileConfirmed', 'space.hoursConfirmed', 'space.pricesConfirmed',
  'space.amenitiesConfirmed', 'space.contactsConfirmed', 'space.photoAdded', 'space.photoRemoved',
  'space.photosReordered', 'space.hidden', 'space.unhidden', 'space.deleted', 'space.restored',
  'space.ownerLinked', 'space.ownerUnlinked',
  'governorate.added', 'governorate.edited', 'governorate.hidden', 'governorate.restored',
  'area.added', 'area.edited', 'area.hidden', 'area.restored',
  'amenity.added', 'amenity.edited', 'amenity.hidden', 'amenity.restored',
  'dataReport.resolved', 'dataReport.dismissed',
  // PR 2: 'platformSettings.newSpaceDefaultsEdited', 'platformSettings.stalenessEdited', 'platformSettings.contactEdited',
] as const;
/** An account's events: the platform's only when they name no space (an owner's staff account's are the space's). */
export const PLATFORM_ACCOUNT_ACTIONS = [
  'user.created', 'user.roleChanged', 'user.suspended', 'user.unsuspended', 'user.temporaryPasswordIssued',
  'user.temporaryPasswordHandedOver', 'user.emailChanged',
] as const;
export function isPlatformEvent({ action, spaceId }: { action: string; spaceId: number | null }): boolean;
export function platformEventsSql(): Prisma.Sql;  // ("action" = ANY(<PLATFORM_ACTIONS>) OR ("action" = ANY(<ACCOUNT>) AND "space_id" IS NULL))
```
- **Default deny:** an action on neither list never reaches the admin, however it is named later.
- **Why the owner's edits of the public facts are listed:** they are public data (ADR 0002: the admin keeps every
  space's existence and moderation); the reports' decisions are the platform's work queue (A8). **Why the staff,
  the settings, the capacity and the override are not:** ADR 0002/0008/0009 keep the space's operations, capacity
  and staff from the admin; an owner's staff account is the space's.
- `platformEventsSql()` is built from the same two arrays, so the SQL and the unit-tested rule cannot drift.

### D4 — the audit answers (`@masaha/shared/audit`, PR 1)
```ts
AUDIT_PERIODS = ['LAST_30_DAYS', 'ALL'] as const
AUDIT_ACTIONS = [ …every action the API writes, each listed once, PR 2 adding its three… ] as const
AUDIT_ENTITY_TYPES = ['space', 'user', 'governorate', 'area', 'amenity', 'dataReport', 'customer', 'subscription',
  'checkIn', 'visit', 'payment', 'package', 'announcement'] as const        // PR 2 adds 'platformSettings'
AUDIT_ACTIONS_MAX = 30
auditQuery = paginationQuerySchema.extend({
  period: z.enum(AUDIT_PERIODS).default('LAST_30_DAYS'),
  q: textSchema(1, 80).optional(),
  actions: a comma-separated list of AUDIT_ACTIONS, 1–30, each once (invalid_choice / too_long),
})
spaceAuditQuerySchema = auditQuery.extend({ actor: z.union([id, z.enum(['MASAHA', 'SYSTEM'])]).optional() })
platformAuditQuerySchema = auditQuery.extend({ actor: id.optional() })
AuditActor = { kind: 'PERSON', id: number, name: string } | { kind: 'MASAHA' } | { kind: 'SYSTEM' }
AuditTarget = { type: AuditEntityType, id: number | null, name: string | null, nameAr: string | null, deleted: boolean }
AuditEntry = { id, at, action: string, actor: AuditActor, target: AuditTarget,
               before: Record<string, unknown> | null, after: Record<string, unknown> | null }
PlatformAuditEntry = AuditEntry & { space: { id, nameEn, nameAr: string | null, deleted: boolean } | null }
AuditMeta = PaginationMeta & { actors: AuditActor[] }      // the period's actors under every filter but actor and page, ≤ 50
```
- **`action` is answered as stored** (a string): a later action not yet on `AUDIT_ACTIONS` is still shown; the
  list is what `actions` accepts and what the web labels (§10).
- **The target's name** is its **current** name, by type: a space's `nameEn`/`nameAr`; a lookup's `nameEn`/`nameAr`;
  a user's, a customer's, a subscription's, a package's `name`; a visit's `visitorName`, else its customer's; a
  check-in's customer's; none for a payment, an announcement, a data report or a setting (the web words them from
  `before`/`after`). `deleted`: a soft-deleted space or announcement. *Why current:* the table stores ids; a
  name copied into every entry would duplicate data the audit writer must not know (R6).
- **`before` / `after` as stored:** the writer never stores a secret (conventions §6, security › Passwords), and the
  admin sees only D3's entries; summarising them would put display rules in the API (ADR 0006).

### D5 — the audit queries (`audit/audit.repository.ts`, PR 1)
One statement for the page and one for its count, in parallel (conventions §5), sharing one `WHERE`:
```sql
FROM "audit_logs" a
LEFT JOIN "space_managers" sm ON sm."space_id" = a."space_id" AND sm."user_id" = a."actor_id"   -- the owner's only
LEFT JOIN "users" au ON au."id" = a."actor_id"
LEFT JOIN LATERAL (                                                                              -- the target's name
  SELECT "name_en" AS name, "name_ar" AS name_ar, "deleted_at" IS NOT NULL AS deleted FROM "spaces"
    WHERE a."entity_type" = 'space' AND "id" = a."entity_id"
  UNION ALL SELECT "name", NULL, false FROM "users" WHERE a."entity_type" = 'user' AND "id" = a."entity_id"
  UNION ALL … one branch per named type of D4 …
) t ON true
WHERE <scope> AND (${since}::timestamptz IS NULL OR a."created_at" >= ${since})
  [AND <actor>] [AND a."action" = ANY(${actions}::text[])]
  [AND strpos(masaha_search_text(concat_ws(' ', t.name, t.name_ar[, the entry's space's names])), masaha_search_text(${q})) > 0]
ORDER BY a."created_at" DESC, a."id" DESC LIMIT ${take} OFFSET ${skip}
```
- **Scope:** the owner's `a."space_id" = ${spaceId}`; the admin's `platformEventsSql()` (D3), and a `LEFT JOIN
  "spaces" es ON es."id" = a."space_id"` for the entry's space and the search by its names.
- **The owner's actor:** `a."actor_id" IS NULL` → `SYSTEM`; `sm."user_id" IS NULL` → `MASAHA` (no id, no name
  selected into the answer); else `PERSON` with `au."name"`. `actor=MASAHA` → `a."actor_id" IS NOT NULL AND
  sm."user_id" IS NULL`; `SYSTEM` → `a."actor_id" IS NULL`; an id → `a."actor_id" = ${id} AND sm."user_id" IS NOT
  NULL` (an admin's id never filters the owner's log by name). The admin's actor is always `PERSON`.
- **`since`:** `LAST_30_DAYS` → `gazaInstant(addDays(gazaClockOf(now).date, -29), 0)` (`audit/auditPeriod.ts`,
  pure); `ALL` → `null`.
- **`meta.actors`:** `SELECT DISTINCT` of the actor's kind and id under the same `WHERE` without the actor filter,
  at most 50, persons by name, then `MASAHA`, then `SYSTEM`.
- **Search by name (S6):** in the same statement, before the page is cut — the rule of conventions §5 (never filter
  a page after fetching it) — through the database's `masaha_search_text` (Arabic folded, data model › Search).
- **Indexes:** the owner's on `audit_logs_space_id_created_at_idx`; the admin's on `audit_logs_created_at_idx`
  (platform events are rare among a busy desk's, so a page reads a few thousand index rows); no new index (§12.2
  PR 1 check 4 measures it).

### D6 — the audit service and its routes (PR 1)
- `createAuditService({ now })` → `spaceLog(spaceId, query): Promise<{ rows: AuditEntry[]; total; actors }>` and
  `platformLog(query): Promise<{ rows: PlatformAuditEntry[]; total; actors }>`; mapper `toAuditEntry(row)`,
  `toPlatformAuditEntry(row)`.
- `audit.manage.routes.ts`: `GET /` → `requireCan('space.auditLog.read')` → `validate(spaceAuditQuerySchema,
  'query')` → controller. `audit.admin.routes.ts`: `GET /` → `validate(platformAuditQuerySchema, 'query')`.
- The owner's route reads `req.space.id` from the boundary; no lock (a log is history).

### D7 — the platform settings (PR 2)
**The catalogue** (`settingKeys.ts`): `newSpaceDefaults: newSpaceDefaultsSchema` (now imported from
`@masaha/shared/space-settings`), `stalenessDays`, `priceStalenessDays` (`z.int().min(1).max(365)` — the stored
values 60 and 30 pass), and **optional** keys `contactEmail: z.email().nullable()`, `contactWhatsapp:
z.string().regex(/^\+[1-9][0-9]{7,14}$/).nullable()` — the stored form the seed already writes (`run.ts`), so no
row needs migrating (S10). A required key missing or invalid stays a fault (throws); an optional key's missing row
reads `null`.

**The shared shapes** (`@masaha/shared/platform-settings`, L0; `space-settings` for the defaults):
```ts
STALENESS_DAYS_MAX = 365
stalenessSchema = z.object({ stalenessDays: z.int().min(1).max(365), priceStalenessDays: z.int().min(1).max(365) })
platformContactSchema = z.object({ email: emailSchema.nullable(), whatsapp: phoneSchema.nullable() })   // both required keys; null clears
StalenessThresholds = { stalenessDays: number, priceStalenessDays: number }
PlatformContact = { email: string | null, whatsapp: string | null }
// space-settings (L0), moved from the API: what a new space's settings are copied from
newSpaceDefaultsSchema = z.object({ autoCheckoutAtClosing: z.boolean(), visitRounding: z.enum(VISIT_ROUNDINGS),
  visitRoundingMinutes: z.int().min(1).max(59).nullable(), visitCapAtDayPrice: z.boolean() })
  .refine(minutes set exactly for UP_AFTER_MINUTES, { path: ['visitRoundingMinutes'] })   // codes as the space's settings: required / invalid_format
NewSpaceDefaults = z.infer<typeof newSpaceDefaultsSchema>
```
**The service** (`platform-settings.service.ts`, deps `{ runInTransaction, audit }`): `newSpaceDefaults(tx?)`,
`stalenessThresholds(tx?)` (unchanged), `contact(): Promise<PlatformContact>`, and one save per card,
`saveNewSpaceDefaults(actor, value)`, `saveStaleness(actor, value)`, `saveContact(actor, value)`, each in one
transaction:
1. `repository.ensure(keys, tx)`: `INSERT INTO "settings" ("key", "value", "updated_at") VALUES … ON CONFLICT
   ("key") DO NOTHING` — only for the optional keys (an absent contact row), with JSON `null`;
2. `repository.lock(keys, tx)`: `SELECT "key", "value" FROM "settings" WHERE "key" = ANY(${keys}) ORDER BY "key"
   FOR UPDATE` — the card's rows, by key (one fixed order);
3. `settingsChange(current, next)` (pure, `settingsChange.ts`): only the fields that changed → `null` answers the
   card as it is, writing nothing;
4. `repository.write(key, value, tx)` per changed key (`Prisma.JsonNull` for `null`, §12.2 PR 2 check 2);
5. audit `platformSettings.<card>Edited`, `entityType: 'platformSettings'`, `entityId: null`, no space, `before` /
   `after` the changed fields.
- **Who may:** the `/admin` guard (`requireRole('ADMIN')`, the account read on every request); the platform
  settings name no space, so `can()`'s `platform.settings.manage` is the role itself (as the admin's other routes).
- **The public read** (`platform-settings.public.routes.ts`): `GET /` → `contact()` → `Cache-Control: public,
  max-age=300` (a contact changes rarely; the site reads it on About and the owner's line).
- **The writer** (`shared/audit/writeAudit.ts`): `entityId: number | null` (S8).

### D8 — the finance shapes (`@masaha/shared/finance`, PR 3)
```ts
FINANCE_MONTHS_BACK = 23                                  // the current month and 23 before it
financeMonthQuery = z.object({ month: z.string().regex(/^\d{4}-(0[1-9]|1[0-2])$/).optional() })   // invalid_format; the range: D9
DEBT_STATES = ['OWES', 'CREDIT'] as const
debtsQuerySchema = paginationQuerySchema.extend({ state: z.enum(DEBT_STATES).default('OWES') })
payersQuerySchema = paginationQuerySchema.merge(financeMonthQuery)
IncomeSplit = { subscriptionsAgorot: number, visitsAgorot: number, totalAgorot: number }
IncomeReport = {
  month: string,                                          // YYYY-MM, as asked or the current
  income: IncomeSplit, previousMonth: IncomeSplit,
  today: IncomeSplit,
  allTime: IncomeSplit & { since: string | null },        // the Gaza day of the first payment not voided
  months: { month: string, income: IncomeSplit }[],      // 12, oldest first, ending with the current month
  visitsByDay: { date: string, agorot: number }[],       // 30 Gaza days, oldest first, ending today
  collections: { recordedBy: { id, name }, count: number, totalAgorot: number,
                 byMethod: { CASH: number, TRANSFER: number } }[]   // the month, largest first, then by id
}
BalanceRow = {
  customer: { id, name, phone: string | null, archived: boolean },
  amountAgorot: number,                                   // OWES: the debt; CREDIT: the credit
  oldestItem: { kind: 'VISIT' | 'SUBSCRIPTION', id, name: string | null, since: string } | null   // OWES only; since: its Gaza day
}
DebtsMeta = PaginationMeta & {
  totals: { owed: { agorot, customers }, credit: { agorot, customers },
            uncollected: { visits: number, owedAgorot: number, unpriced: number } },
  reminderTemplate: string | null                         // the space's; null: the catalogue's default
}
Payer = { customer: { id, name }, paidAgorot: number, lastPaidAt: string }      // in the month
OccupancyReport = {
  month: string,
  averageStayMinutes: { all: number | null, members: number | null, visits: number | null },
  peakHour: number | null,                                // 0–23, the month's
  averageDailyAttendance: number | null,                  // one decimal
  byDay: { date: string, visits: number, members: number }[],          // 14 Gaza days, oldest first, ending today
  byHour: { weekday: number, hours: number[] }[]          // 7 (0 = Sunday … 6), each 24 averages, one decimal
}
```
`core/gazaTime.ts` gains `monthOf(date: string): string` and `addMonths(month: string, months: number): string`
(pure, calendar only), which the web's month select uses too (conventions §11).

### D9 — the windows (`finance/windows.ts`, pure, PR 3)
- `monthWindow(month, now)` → `{ from, to }`: `gazaInstant(`${month}-01`, 0)` to the next month's; **`monthError(month,
  now)`** → `'out_of_range'` when after the current Gaza month or before `addMonths(current, -23)` (422 on
  `month`), else `null`.
- `todayWindow(now)`; `monthsEnding(current, 12)`; `daysEnding(today, n)` (30, 14); `allTime` = `{ from: null, to:
  now }`.
- `fourWeeks(now)`: the 28 Gaza days before today (today left out, so each weekday counts exactly 4 times);
  `hourSlots(days)` → `{ from, to, weekday, hour }[]`: every hour from each day's Gaza midnight, labelled by
  `gazaClockOf(from)` (a daylight-saving night's hours as Gaza counts them, §12.2 PR 3 check 3).
- Every window is a pair of instants; the SQL takes them as two arrays and buckets with `unnest(…) WITH
  ORDINALITY` (S2).

### D10 — the ledger's aggregates (`payments`, PR 3) — reused by the overview
| Function | Answers | Query |
|---|---|---|
| `incomeIn(spaceId, windows, tx?)` | per window `IncomeSplit`, in order | `unnest(${froms}::timestamptz[], ${tos}::timestamptz[]) WITH ORDINALITY w(f, t, i) LEFT JOIN payments p ON p.space_id = ${spaceId} AND p.voided_at IS NULL AND p.received_at >= w.f AND p.received_at < w.t`, `sum(…) FILTER (WHERE p.subscription_id IS NOT NULL)` and `… visit_id …`, `GROUP BY w.i` (a `null` start: `-infinity`) |
| `firstReceivedAt(spaceId, tx?)` | `Date \| null` | `min(received_at)` not voided |
| `collectionsIn(spaceId, window, tx?)` | `{ recordedById, count, totalAgorot, cashAgorot, transferAgorot }[]` | `GROUP BY recorded_by_id`, not voided, by total desc then id |
| `balancesPage(spaceId, state, at, page, tx?)` | `{ rows: { customerId, amountAgorot, oldest }[], total }` | `WITH balances AS (balancesOf(spaceId, null, now))`: per customer `DEBT` or `CREDIT` (the existing sums), `HAVING > 0`, `ORDER BY amount DESC, customer_id`, `count(*) OVER ()`; `oldest` (OWES): the item with `due − paid > 0` of the least `created_at`, then visit first, then id (`DISTINCT ON`) |
| `balanceTotals(spaceId, at, tx?)` | `{ owed: { agorot, customers }, credit: { agorot, customers } }` | the same `balances`, summed |
| `uncollectedTotals(spaceId, tx?)` | `{ visits, owedAgorot, unpriced }` | the `uncollectedPage` fragment, counted and summed |
- **One balance rule:** `balancesPage` and `balanceTotals` read `balancesOf` (the owner's decision 6), so a
  written-off visit, a voided payment and an unpriced visit count as the customers list and file count them.
- **The overview (step 12)** will call `payments.balanceTotals` (its «عملاء عليهم ديون» count) and
  `payments.uncollectedTotals` (its «زيارات لم تُحصَّل»); never `finance` (conventions §9). No money on the owner's
  overview (O3): the counts only. Nothing else of finance is reused there.
- `payments.service.ts` exposes each (the `Now` its `balancesOf` needs, from `at`, as `customerBalances` does).

### D11 — occupancy (`finance/finance.repository.ts`, R7, PR 3)
- **Closed stays:** `SELECT checked_in_at, checked_out_at, NULL AS customer_id, 'VISIT' FROM visits WHERE
  space_id = ${spaceId} AND checked_out_at IS NOT NULL AND checked_in_at >= ${from} AND checked_in_at < ${to}
  UNION ALL SELECT …, customer_id, 'MEMBER' FROM check_ins …` — the auto check-out's included; open ones out
  (decision 7); bounded by the check-in, which the `(space_id, checked_in_at)` indexes serve (a stay never crosses
  midnight).
- `perDay(spaceId, days)` → per window `{ visits, members }`: `count(*) FILTER (WHERE kind = 'VISIT')`,
  `count(DISTINCT customer_id) FILTER (WHERE kind = 'MEMBER')` (K5: a member counted once a day).
- `presenceBySlot(spaceId, slots)` → per slot the stays overlapping it (`checked_in_at < slot.to AND checked_out_at
  > slot.from`), the slots one pair of arrays; the stays read once for the whole range.
- `stayMinutes(spaceId, window)` → `{ all, members, visits }`: `round(avg(extract(epoch FROM checked_out_at −
  checked_in_at) / 60))`, `null` without stays.
- **Pure** (`finance/occupancyGrid.ts`): `averagePerHour(slots, counts, weeks = 4)` → `byHour` (sum per weekday and
  hour ÷ 4, one decimal, half up); `peakHour(slots, counts)` → the hour of the day with the most presence over the
  month, ties the earliest, `null` when none; `averageDailyAttendance(perDay)` → the mean of `visits + members` over
  the month's days with any, one decimal, `null` when none.
- **The month's figures** use the month's window up to now (the current month so far).

### D12 — the finance service (`finance/finance.service.ts`, PR 3)
Deps `{ readSnapshot, payments, customers, subscriptions, users, spaceSettings, now }`.
- `income(spaceId, month?)`: `monthError` → 422; in one snapshot: `payments.incomeIn` over [month, previous,
  today, all time, the 12 months, the 30 days] (one call, 45 windows), `firstReceivedAt`, `collectionsIn(month)`;
  then `users.namesFor` (outside the snapshot, a name being no figure). Answer `IncomeReport`.
- `debts(spaceId, query)`: in one snapshot: `payments.balancesPage`, `balanceTotals`, `uncollectedTotals`,
  `customers.contactsOf(spaceId, ids, tx)` (now with `archived`), `subscriptions.namesOf(spaceId, oldestSubIds,
  tx)`, `spaceSettings.read(spaceId, tx).reminderTemplate`. Answer `BalanceRow[]` and `DebtsMeta`.
- `payers(spaceId, query)`: `monthError`; `repository.payersIn(spaceId, window, page)` — the customers of the
  month's payments not voided (`coalesce(v.customer_id, s.customer_id)`, a walk-in's payment naming no one), `sum`,
  `max(received_at)`, latest paid first, then customer id, with `count(*) OVER ()`; names by
  `customers.namesOf`.
- `occupancy(spaceId, month?)`: `monthError`; D11's reads in parallel (no snapshot: each figure stands alone).
- `finance.manage.routes.ts`: four `GET`s, each `requireCan('finance.read')` → `validate(<query>, 'query')` →
  controller; the controller answers `sendSuccess` with `meta` where §4 asks it.

### D13 — bounds and cost
| Answer | Bound | Its reads on one space's year (≈ 10 k payments, 9 k visits, 3 k check-ins, 500 subscriptions, 36 k audit entries) |
|---|---|---|
| `IncomeReport` | 12 + 30 + the staff who recorded (≤ tens) | 45 index range scans of `payments_space_id_received_at_idx` in one statement; one `GROUP BY` of the month |
| `BalanceRow[]` | a page (≤ 50); totals | `balancesOf` over the space (as `customerIdsByPayment` today); `subscription_usage` inlined once |
| `Payer[]` | a page | one month's payments joined to their items by primary key |
| `OccupancyReport` | 14 + 168 cells | a month's stays (≈ 1 k) against ≤ 744 slots, and 28 days against 672 slots (nested loop ≈ 10⁶ comparisons) |
| `AuditEntry[]` | a page (≤ 50); `actors` ≤ 50 | the owner's on `(space_id, created_at)`; the admin's on `(created_at)` |
Every answer stays far under ADR 0014's 4.5 MB (a page of entries with whole price lists ≈ 0.5 MB at worst). **No
new index** (data model: indexes only for queries that run, measured): §12.2 PR 1 check 4 and PR 3 check 4 measure
each on a generated year; a read over its threshold stops the item for the owner's index decision (§13 Q5).

### D14 — locks, snapshots and races
- **Reads** take no lock. The income report and the debts' page with its totals read one `REPEATABLE READ`
  snapshot (S3); the audit page and its count, the payers' page and its count, are read apart, as every list (a
  write between them shows on the next read).
- **The extension** (carried): the space's row, the closure's, then the covered **and** pending renewal rows in one
  statement by id — conventions §13's one fixed order, unchanged; every subscription write takes the space's lock
  first, so the chain is read as committed.
- **A settings save:** the card's rows by key (`FOR UPDATE`), after an `INSERT … ON CONFLICT DO NOTHING` for an
  absent optional key. No other lock order involves `settings` (a space's creation reads the defaults without one).

| Race | What decides | Test |
|---|---|---|
| A renewal sold while the extension waits | the space's lock; the chain read under it | PR1 T-C4 |
| Two admins save one card at once | the rows' `FOR UPDATE`; the second's `before` is the first's `after` | PR2 T5 |
| Two first saves of the contact at once | `ON CONFLICT DO NOTHING`, then the lock | PR2 T6 |
| A payment recorded during the income report | the snapshot: the month equals its bar | §10 (no deterministic test) |

### D15 — the code, PR by PR (interfaces; the commit in brackets)

**PR 1**
| Where | What |
|---|---|
| `subscriptions/closures/closures.repository.ts` | `coveredCount`, `lockCovered` → `movedCount(spaceId, span, today)`, `lockMoved(spaceId, span, today, tx)`; + `moveRenewals(ids, days, at, tx)`; `findByKey` selects the space; `ExtensionRow.spaceId` [C0a, C0b] |
| `subscriptions/closures/closures.service.ts` | `preview` → `movedCount`; `extend` → D2 [C0a, C0b] |
| `packages/shared/src/audit/{requests,responses,actions,index}.ts` (+ `requests.unit.test.ts`) | D4 [C1, C2] |
| `audit/{index,audit.service,audit.repository,audit.controller,audit.mapper}.ts` | D5–D6 [C1, C2] |
| `audit/audit.manage.routes.ts`, `audit/audit.admin.routes.ts` | D6 [C1, C2] |
| `audit/auditPeriod.ts` (+ unit), `audit/platformEvents.ts` (+ unit) | D5's `since`; D3 [C1, C2] |
| `app.ts` | the service; the two routers [C1, C2] |

**PR 2**
| Where | What |
|---|---|
| `packages/shared/src/space-settings/{requests,index}.ts` | + `newSpaceDefaultsSchema`, `NewSpaceDefaults` [C1] |
| `packages/shared/src/platform-settings/{requests,responses,index}.ts` (+ unit) | D7's shapes [C1] |
| `platform-settings/settingKeys.ts`, `index.ts` | the catalogue (D7); the index re-exports the moved schema from shared [C1] |
| `platform-settings/platform-settings.{repository,service}.ts`, `settingsChange.ts` (+ unit) | `ensure`, `lock`, `write`; the saves; `contact()` [C1, C2] |
| `platform-settings/platform-settings.{controller,admin.routes,public.routes}.ts` | D1's routes [C1, C2] |
| `shared/audit/writeAudit.ts` | `entityId: number \| null` [C1] |
| `audit/platformEvents.ts` (+ unit), `packages/shared/src/audit/{actions,responses}.ts` | the three actions; `'platformSettings'` [C1] |
| `app.ts` | the routers; `platformSettings` gains `runInTransaction`, `audit` [C1, C2] |

**PR 3**
| Where | What |
|---|---|
| `packages/shared/src/core/gazaTime.ts` (+ unit) | `monthOf`, `addMonths` [C1] |
| `packages/shared/src/finance/{requests,responses,index}.ts` (+ unit) | D8 [C1–C3] |
| `payments/payments.{repository,service}.ts` | D10 [C1, C2] |
| `customers/customers.{repository,service}.ts` | `contactsOf` answers `archived` [C2] |
| `finance/{index,finance.service,finance.repository,finance.controller,finance.manage.routes,finance.mapper}.ts` | D11–D12 [C1–C3] |
| `finance/windows.ts` (+ unit), `finance/occupancyGrid.ts` (+ unit) | D9, D11 [C1, C3] |
| `app.ts` | `finance` built; `manage.use('/finance', …)` [C1] |

---

## 5. Stronger decisions, and Proposed alternatives

### S1 — "Masaha" decided by links, not by the role — **recommended, planned (PR 1)**
*What:* an actor with no link of any state to the space is `MASAHA`; the answer carries neither id nor name.
*Why:* the role is read now and can change (an admin demoted, a user made admin); the links are kept for ever and
only the platform acts on a space without one (the admin is never linked: `ACCOUNT_IS_ADMIN`). *Cost:* one join.

### S2 — every bucket a window computed in Node — **recommended, planned (PR 3)**
*What:* months, days and hours are instants from `gazaInstant`/`gazaClockOf`, passed as arrays; no `AT TIME ZONE` in
finance. *Why:* one zone source (finding 120), and the indexes serve each window (finding 127's cost avoided).
*Cost:* the arrays (≤ 744 pairs) and one pure file with its tests.

### S3 — the income and the debts read one snapshot — **recommended, planned (PR 3)**
*What:* `readSnapshot` around each. *Why:* the month's total must equal its bar, and the page's rows its totals
(conventions › Composed reads, finding 124). *Cost:* none beyond the call.

### S4 — the owner's audit actor filter never names an admin — **recommended, planned (PR 1)**
`actor=<id>` matches only a linked person; the admin's entries are reached by `actor=MASAHA`. *Why:* decision 8; an
admin's id guessed into the filter would otherwise confirm who acted. *Cost:* one clause.

### S5 — the allowlist as data, with an account rule — **recommended, planned (PR 1)**
Two arrays in one pure file, the SQL built from them, unit-tested and broken at the API. *Why:* default deny must
be one list; an account's events are the platform's only with no space (§3). *Cost:* one file.

### S6 — the target search inside the page's statement — **recommended, planned (PR 1)**
`q` matches the targets' current names (and, for the admin, the entry's space) in the same SQL, through
`masaha_search_text`. *Why:* conventions §5's purpose (never filter a fetched page) holds; R7 lets a read model read
the names; the database's folding finds «احمد» for «أحمد». *Cost:* the lateral names on every scanned row (a space's
year is ≈ 36 k).

### S7 — `meta.actors` — **recommended, planned (PR 1)**
The period's actors, so the web offers the actor filter only when there are several (AD-028) without reading every
page. *Cost:* one `DISTINCT` query.

### S8 — an audit entry may name no entity id — **recommended, planned (PR 2)**
`entityId: number | null` in the writer, as the column already is. *Why:* a platform setting has no numeric id; a
fake `0` would lie. *Cost:* one type.

### S9 — three settings resources, the defaults' schema in `space-settings` — **a placement, stated (§13 Q9)**
*Why:* the shared level rule refuses an L0 capability importing another (§3); the defaults are a subset of a
space's settings; AD-029 wants each card its own save and error. *Cost:* three small `GET`s on the admin's page.

### S10 — the contact read in its stored form, written normalised — **recommended, planned (PR 2)**
*Why:* the seed already wrote the E.164 form and a valid email; a stricter read could turn an existing row into a
500 on the public About; the admin's save normalises (`emailSchema`, `phoneSchema`). *Cost:* two schemas per key.

### S11 — the staleness thresholds bounded 1–365 — **recommended, planned (PR 2)**
Today any positive integer; a typo of 6000 would mark nothing stale for years. *Cost:* one bound.

### S12 — the chain moves start and end, linked and counted — **as carried (option A), stated (§13 Q11)**
The preview counts the chain; the audit names `renewalIds` apart.

### Rules the item touches, stated
- **conventions §6** — the reader built; the allowlist's home (`audit/platformEvents.ts`) and the account rule;
  `MASAHA` by links; entries kept for ever (decision 10); remove "no design yet" (O13 designed it; finding 14 stays
  open for its screen). **§7** — `audit`'s and `finance`'s *Holds*; `platform-settings`' routers (public: the
  contact; admin: three cards). **§9** — *Settings*: the contact keys in the catalogue (finding 40 resolved);
  *Composed reads*: finance's debts through `payments`' balances, its occupancy its own (R7); *overview*: the two
  `payments` functions it will read. **§13** — the settings' row lock.
- **data-model** — *Conventions › Settings* (the contact keys no longer excepted); *Entities › Setting*,
  *AuditLog* (kept for ever, decision 10); *Derived values* — *Income*, *Collections*, *Occupancy statistics*
  refined (D9, D11); *Checked by the service* — the extension's chain (carried); line 23 (carried).
- **security.md** — *Authorization*: the owner's log and finance (`requireCan`), the admin's allowlist.
- **api-contract** — new *Audit log*, *Platform settings*, *Finance* sections; §6 unchanged (no code).
- **v1-mvp** — the finance row loses "CSV export" (decision 5) and names its four routes; `/admin/settings`
  becomes the three cards; `/settings/public` built.
- **ADR 0002** consequence "leaves out member and attendance entries" holds by D3 (no change).

### Proposed alternatives (the owner may prefer them)
- **A1 — one finance route** (`GET …/finance?month=`, every tab). One request on a weak line; but the debts page and
  the payers page would ride with it, and every tab would pay for the others. **Not recommended.**
- **A2 — every finance aggregate in `finance`'s repository** (R7), none in `payments`. Fewer cross-module functions;
  the "voided left out" and the balance rules would then have two homes, and the overview could not reuse them
  (conventions §9 forbids it to import `finance`). **Not recommended.**
- **A3 — an index for the admin's log now** (`(action, created_at)`, ≈ 30 MB a busy year). Faster "all time"
  counts; against ADR 0014's 0.5 GB and before any measurement. **Not recommended** until §12.2's measure.
- **A4 — a retention rule** (decision 10 challenged): the desk's entries (visits, check-ins, payments) older than
  two years summarised or dropped. *Why:* at twenty busy spaces the table may near Neon's 0.5 GB in about two years
  (≈ 730 k entries a year). *Cost:* a job, a decision on what the owner may still need. **For the owner** (§13 Q10).
- **A5 — the prototype's «فترة محدّدة» on the audit logs** (`from`/`to`, ≤ 92 days, as the payments list). The
  owner's decision 9 names two choices only. **Not recommended.**
- **A6 — names as they were** (copied into each entry when written). Accurate history; the writer would have to know
  each entity's name (R6). **Not recommended.**

---

## 6. Related findings

| Finding | Folded? | Why, and the cost |
|---|---|---|
| **151** A renewal sold before the extension stays put | **Yes, PR 1 C0a** (carried) | Written and resolved in the same commit (option A) |
| **40** The platform's contact settings are outside the typed catalogue | **Yes, PR 2 C1** (decision 11) | Two keys, their schemas, the admin's card; its *Resolution* line, index line |
| **14** The owner's audit screen has no design | No | O13 designed it (`Owner audit.html`); its screen is worker A's, which resolves it. PR 1 states the API built in conventions §6 |
| **120** Gaza dates are read by two zone databases | No | Finance avoids it (S2); the existing readers keep it |
| **127** The dated check-in list filters on an expression | No | Finance filters by instants; that list is `subscriptions`' |
| **124** A statement's sums and payments from different snapshots | No (resolved) | Its pattern reused (S3) |
| **164** A written-off visit is listed nowhere | No | Finance shows debts, not write-offs; a list of write-offs is its own item |
| **161** No route reads the visits of a day | No | Occupancy answers counts, not visits |
| **17** Expired counters and abandoned sessions never swept | No | The same family as A4; recorded as §13 Q10 |
| **79** The users' names reader keeps an optional transaction | No | `namesFor` called outside the snapshots, as today |
| **98** The capability documents outgrow their size guide | No | Three new documents follow the template |

**Planned new finding:** **152** — "Audit entries kept for ever meet the database's 0.5 GB" (A4), if §13 Q10
approves recording it (PR 1 C2). Any other finding an executor records takes the next number, across the three
PRs, in order.

---

## 7. The files it edits

Only `apps/api`, `packages/shared` and `docs`. **No `apps/web` file, no dependency, no migration** (unless the
owner orders an index after §12.2's measurement; then §12.2 *Every PR* check 1).

| PR | Code (new +) | Documents |
|---|---|---|
| 1 | `subscriptions/closures/{closures.repository,closures.service}.ts`, `closures/extension.api.test.ts`; shared + `audit/{requests,responses,actions,index}.ts`, + `audit/requests.unit.test.ts`; api + `audit/{index,audit.service,audit.repository,audit.controller,audit.mapper,audit.manage.routes,audit.admin.routes,auditPeriod,platformEvents}.ts`, + `audit/{auditPeriod,platformEvents}.unit.test.ts`, + `audit/{spaceAuditLog,platformAuditLog}.api.test.ts`; `app.ts` | `api-contract.md`, `data-model.md`, `conventions.md`, `security.md`, + `features/audit.md`, `features/subscriptions.md` (and `announcements.md` if it states the covered rule), + `findings/151-…md`, (+ `findings/152-…md`, Q10), `findings/README.md`, `docs/README.md`, `plans/v1-mvp.md`, `project/overview.md` — ≈ 36 |
| 2 | shared `space-settings/{requests,index}.ts` (+ its unit test's lines), + `platform-settings/{requests,responses,index}.ts`, + `platform-settings/requests.unit.test.ts`, `audit/{actions,responses}.ts`; api `platform-settings/{index,settingKeys,platform-settings.repository,platform-settings.service}.ts`, + `platform-settings/{settingsChange,platform-settings.controller,platform-settings.admin.routes,platform-settings.public.routes}.ts`, + `settingsChange.unit.test.ts`, + `platform-settings/{adminSettings,publicContact}.api.test.ts`; `shared/audit/writeAudit.ts`; `audit/platformEvents.ts`, its unit test, `audit/platformAuditLog.api.test.ts`; `app.ts` | `api-contract.md`, `data-model.md`, `conventions.md`, + `features/platform-settings.md`, `features/space-settings.md` (code map), `findings/40-…md`, `findings/README.md`, `docs/README.md`, `plans/v1-mvp.md`, `project/overview.md` — ≈ 32 |
| 3 | shared `core/gazaTime.ts`, `core/gazaTime.unit.test.ts`, + `finance/{requests,responses,index}.ts`, + `finance/requests.unit.test.ts`; api `payments/payments.{repository,service}.ts`, `customers/customers.{repository,service}.ts`, + `finance/{index,finance.service,finance.repository,finance.controller,finance.manage.routes,finance.mapper,windows,occupancyGrid}.ts`, + `finance/{windows,occupancyGrid}.unit.test.ts`, + `finance/{access,income,debts,payers,occupancy}.api.test.ts`; `app.ts` | `api-contract.md`, `data-model.md`, `conventions.md`, `security.md`, + `features/finance.md`, `features/payments.md`, `docs/README.md`, `plans/v1-mvp.md`, `project/overview.md` — ≈ 36 |

**No stop for the file count** (the owner's rule, 2026-10-26): the count is reported.

---

## 8. Design issues

No screen is built. The API follows `Finance.html`, `Owner audit.html`, `Admin audit.html`, O3, O13, OW-015,
OW-016, A7, AD-028, AD-029. Points for worker A's screens, not findings:
- **The audit pages' «فترة محدّدة»** has no API (decision 9: «آخر 30 يومًا» and «كل الفترة»): the select keeps two
  choices.
- **The audit's «نوع الإجراء»** groups actions (`lookup_changed`, `group_saved`): the web sends the group's actions
  in `actions` (≤ 30).
- **The owner's target search** finds a target by its own name: a customer's entries, not the payments of that
  customer (a payment's target is the payment). The placeholder «دفعة، شخص، إعلان…» should say «شخص، باقة، اشتراك…».
- **Finance's «دفعوا في الشهر»** lists a payer's name and what they paid in the month; the prototype's "current
  subscription" line has no field (a second composition for a line the owner did not ask for).
- **«ساعة الذروة»'s helper «الأحد والاثنين الأعلى»** has no field: the heatmap shows the busy days.
- **The debts' CSV** needs every debtor: the web reads the pages (≤ 50 each) before it builds the file.
- **«متوسط مدة الجلوس»**: the API answers whole minutes; the web formats `4:12`.

---

## 9. Tests — lane, title, the break each catches

Every test is seen failing first in its own lane; every expectation is written by hand; a fixed clock through
`createTestApp({ clock })`; instants with their offset; Gaza dates as strings. Roles in each API file (testing §4):
the **owner**, **reception**, a **stranger** (signed in, no link), **another space's owner**, the **admin**; for the
public route, **anonymous**. B-numbers are §12.5's breaks, each run once, its red lines recorded. Audit entries are
**inserted directly** (`prisma.auditLog.create`, fixed `createdAt`), so the reader is proven apart from the writers.

### PR 1 — carried (`subscriptions/closures/extension.api.test.ts`, existing, gaining) [C0a, C0b]
Clock `2026-11-12T10:00:00+02:00`; a closure `2026-11-08T00:00+02:00` → `2026-11-11T00:00+02:00` (days 11-08 to
11-10).
- T-C1 `a renewal not started moves with the subscription it renews: S ends 12-03, R runs 12-04 → 2027-01-02, one
  link each, audited with renewalIds` (S 11-01 → 11-30; R renews S, 12-01 → 12-30; extended by 3) — **B-C1**: the
  chain's move dropped (`renewals` not moved).
- T-C2 `a renewal of that renewal moves too; a renewal started (12 November) or ended early stays; another space's
  never` — **B-C2**: `starts_on > today` dropped from `pending`; **B-C3**: the recursion's second branch removed.
- T-C3 `the preview counts what the extension moves, the chain included; the list's extension says the same` —
  **B-C4**: the preview's count without the chain.
- T-C4 `a renewal sold while the extension waits on the space's lock moves too` (`whileHeld`: the test inserts R
  renewing a covered S, starting after today) — **B-C5**: `lockMoved` read before `spaces.lock`.
- T5 gains `a key that extended another space's closure is a conflict, with nothing of that extension answered`
  (space B's owner on A's closure id with A's key) — **B-C6**: the space comparison removed.

### PR 1 — the audit reader
**Unit**
- U1 `audit/platformEvents.unit.test.ts`: `the platform's list names no customer, subscription, check-in, visit,
  payment, package, announcement or closure action, nor a space's capacity, override, settings or staff; an
  account's event is the platform's only with no space` — **B1**: `'payment.recorded'` added to `PLATFORM_ACTIONS`;
  **B2**: `isPlatformEvent` ignoring `spaceId`.
- U2 `audit/auditPeriod.unit.test.ts`: `the last 30 days start at the Gaza midnight 29 days before today, across a
  daylight-saving change; all time has no start` — **B3**: `now − 30 × 24 h`.
- U3 `packages/shared audit/requests.unit.test.ts`: `the period defaults to the last 30 days; actions are known,
  each once, at most 30; q 1–80; the owner's actor an id, MASAHA or SYSTEM; the admin's an id` — **B4**: the
  actions' enum check removed.

**API — `audit/spaceAuditLog.api.test.ts`** [C1]
- T1 `the owner reads every entry of the space, newest first, paged, with before and after as stored: the staff's,
  the system's and the admin's; another space's never` — **B5**: the space filter dropped.
- T2 `the admin's actor is MASAHA with no id or name; a staff member's is named, also once their link ended; the
  system's is SYSTEM` (the body serialised and searched for the admin's id key and name) — **B6**: `PERSON` for
  every actor with an id (decision 8).
- T3 `each target has its type, id and current name: a customer, a subscription, a visit by its visitor, a space; a
  deleted announcement is marked; a payment has none` — **B7**: the lateral without its type condition on `users`.
- T4 `the last 30 days by default, from the Gaza midnight 29 days back; ALL reaches an older entry` — **B8**: the
  default `ALL`.
- T5 `q finds the entries whose target's name holds it (أحمد for احمد); actor (a person, MASAHA, SYSTEM) and actions
  narrow; each before the page is cut, the total right` — **B9**: `q` matched on `nameAr` only (a customer's name
  missed).
- T6 `actor=<the admin's id> finds nothing; actor=MASAHA finds the admin's` — **B10**: S4's link condition removed.
- T7 `meta.actors lists the period's actors once each, MASAHA and SYSTEM included` — **B11**: `DISTINCT` removed.
- T8 `reception is 403 before the query is read; a stranger, another space's owner and the admin not_found` —
  **B12**: `requireCan('space.auditLog.read')` removed; **B12a**: the router mounted on `api` outside `manage` (the
  boundary skipped: the stranger, the other owner and the admin read it).
- T9 `an unknown period or action, a q of 81, an actor of another kind: 422 on its field`.

**API — `audit/platformAuditLog.api.test.ts`** [C2]
- T10 `the admin reads the platform's events of every space and of none — a space hidden, an owner linked, an
  account suspended, an area edited, a report decided — and never a payment, a visit, a check-in, a subscription,
  a customer, a package, an announcement, an extension, a capacity, an override, a space's settings or its staff`
  (one entry of each inserted) — **B13**: `'payment.recorded'` added to the list; **B14**: `'space.capacityEdited'`
  added.
- T11 `an account's event that names a space (an owner's staff) is the space's, never the admin's; the admin's own
  are listed` — **B15**: the account rule's `"space_id" IS NULL` dropped.
- T12 `q finds a space's entries by its name, a person's by name, an area's by its Arabic name; each entry carries
  its space, a deleted one marked` — **B16**: the entry's space left out of the search.
- T13 `actor narrows to one person; meta.actors the period's persons` — **B17**: the actor filter ignored.
- T14 `a guest is 401, a user and an owner 403, an admin with a pending password 403 PASSWORD_CHANGE_REQUIRED`
  (`REFUSED_CALLERS`) — **B18**: the router mounted outside `/admin`.

### PR 2
**Unit**
- U1 `packages/shared platform-settings/requests.unit.test.ts`: `thresholds 1–365, whole; the contact's email
  lowercased, its WhatsApp normalised (Jawwal to +970), null clears; the defaults' minutes exactly with
  UP_AFTER_MINUTES` — **B1**: the thresholds' upper bound removed; **B2**: the defaults' refinement removed.
- U2 `platform-settings/settingsChange.unit.test.ts`: `only the fields that change; nothing when all equal` — **B3**:
  every field counted.
- U1 of PR 1 (`platformEvents.unit.test.ts`) gains `the platform's settings are the platform's`.

**API — `platform-settings/adminSettings.api.test.ts`** [C1]
- T1 `the admin reads each card: the defaults, the thresholds, the contact null while unset` — **B4**: the optional
  keys read as required (500).
- T2 `each card saves on its own, answered as saved; audited with only what changed, no entity id; the same values
  write nothing` — **B5**: the no-change branch removed (an entry appears).
- T3 `a saved default is copied into the next space only; an existing space keeps its own` (`POST /admin/spaces`)
  — **B6**: the save writing the default under the stored key's old value (`write` skipped).
- T4 `a threshold saved applies at once: a group 40 days old is stale under 30` (`GET /admin/spaces/:id`).
- T5 `two saves of one card at once: the second's before is the first's after` (`whileHeld` on the
  `stalenessDays` row) — **B7**: `lock`'s `FOR UPDATE` removed.
- T6 `two first saves of the contact at once make one row per key, both 200` (`waitingOnLock({ count: 1 })` on a
  held insert) — **B8**: `ensure` removed (the second's insert is a unique violation, 500).
- T7 `a guest is 401, a user and an owner 403 on the six routes` — **B9**: the router mounted outside `/admin`.
- T8 `an invalid body is 422 on its field, writing nothing` (a threshold 0, an email without @, a WhatsApp of
  another country).

**API — `platform-settings/publicContact.api.test.ts`** [C2]
- T9 `anyone reads the contact, with Cache-Control public 5 minutes; none set: both null` — **B10**: the header
  removed.
- T10 `a stored contact that fails its schema is a 500, never answered` — **B11**: the read without its parse.

**API — `audit/platformAuditLog.api.test.ts`** (PR 2 C1)
- T11 `the three settings actions are on the admin's log, the target typed platformSettings with no id` — **B12**:
  the three left off the list.

### PR 3
**Unit**
- U1 `packages/shared core/gazaTime.unit.test.ts` (gaining): `monthOf and addMonths across a year, back and ahead` —
  **B1**: `addMonths` off by one in December.
- U2 `finance/windows.unit.test.ts`: `a month from its Gaza midnight to the next; 23 months back the earliest, the
  next month out of range; the 12 months and the 30 and 14 days ending today; the 28 days before today; hours
  labelled by Gaza weekday and hour across a daylight-saving night` — **B2**: windows from UTC midnights; **B3**:
  the 28 days ending today.
- U3 `finance/occupancyGrid.unit.test.ts`: `the average per weekday and hour over 4 weeks, one decimal; the peak hour,
  ties the earliest, none without stays; the daily attendance over the days with any` — **B4**: ÷ 7 instead of ÷ 4;
  **B5**: attendance over every day of the month.
- U4 `packages/shared finance/requests.unit.test.ts`: `a month YYYY-MM; a state OWES or CREDIT, OWES by default`.

**API — `finance/access.api.test.ts`** [C1–C3]
- T1 `reception is 403 on the four routes before the query is read (an invalid month still 403); a stranger,
  another space's owner and the admin not_found` — **B6**: `requireCan('finance.read')` removed from `income`;
  **B7**: from `debts` (the debts' phones, decision 5); **B7a**: the router mounted outside `manage` (the boundary
  skipped).

**API — `finance/income.api.test.ts`** [C1]
- T2 `the month's income by subscriptions and visits, the month before, today and all time with its first day:
  voided payments left out; a written-off visit's payment counted as received` (hand sums) — **B8**: `voided_at IS
  NULL` dropped.
- T3 `the 12 months and the visits' 30 days by Gaza day: a payment at 23:30 on a month's last day counts in that
  month and that day` (23:30 Gaza = 21:30 UTC) — **B9**: windows by UTC days.
- T4 `each staff member's collections for the month by method, named, an ex-reception's included` — **B10**: the
  method split taken from all payments.
- T5 `another space's payments never counted` — **B11**: the space filter dropped from `incomeIn`.
- T6 `a month ahead, or 24 months back, is 422 out_of_range on month; 23 back answers` — **B12**: `monthError`
  skipped.

**API — `finance/debts.api.test.ts`** [C2]
- T7 `who owes, largest first, paged, the total right: the phone, an archived customer kept and marked, the oldest
  item still owing and its day` — **B13**: ordered by customer id.
- T8 `who is in credit, largest first; a credit never offsets another subscription's debt` — **B14**: the amount
  netted per customer (`sum(due − paid)`).
- T9 `a written-off visit, a voided payment and an unpriced visit owe nothing; a walk-in's uncollected visit counts
  apart, its unpriced too` — **B15**: `written_off_at IS NULL` dropped from `balancesOf` (this file only).
- T10 `the totals agree with every page's rows, and the reminder template is the space's, null by default` —
  **B16**: the template not read (always null).

**API — `finance/payers.api.test.ts`** [C2]
- T11 `the customers who paid in the month, the latest first, each with what they paid then; a walk-in's payment
  names no one; a voided payment leaves its customer out` — **B17**: voided payments counted.

**API — `finance/occupancy.api.test.ts`** [C3]
- T12 `visits and members per day over the 14 days: closed stays only, a member twice in a day once` — **B18**: open
  stays counted (decision 7); **B19**: members counted per check-in.
- T13 `the average present per hour over the 28 days before today, by Gaza weekday and hour; an auto-closed stay
  counted; today's left out` — **B20**: overlap by the check-in's hour only.
- T14 `the month's average stay, members and visits apart, its peak hour and daily attendance; none: nulls` —
  **B21**: the average stay over visits only.

### Not tested, and said
- The snapshot's agreement under a concurrent payment (D14): no lock to wait on, so no deterministic test; the
  snapshot is the existing `readSnapshot`, whose own test is #118's.
- A real year's cost: measured, not tested (§12.2 PR 1 check 4, PR 3 check 4).

---

## 10. Review Focus — inputs no planned test exercises

- An action written by a later PR and not added to `AUDIT_ACTIONS`: answered (as stored) but not filterable; and not
  on the admin's list — hidden from the admin by default, as D3 means.
- An admin who once held a link to the space (an owner made admin after their links ended): named, not `MASAHA`, in
  that space's log (S1).
- A target renamed since: the log shows the current name; a customer archived shows `deleted: false` (archive is no
  delete).
- `q` over thousands of an owner's entries in `ALL`: each scanned row joins its target's name.
- A renewal chain three deep, each not started; a covered subscription with a renewal that starts today (started).
- A month with daylight saving's change: 23 or 25 hourly slots that day; the average is per slot.
- A payment received at exactly a window's edge (`received_at = to`): the next window.
- A customer who owes on one subscription and holds credit on another: in both lists.
- Collections by an admin: none can be recorded (`payments.record` is the staff's).
- `month` of the current month on its first day before 08:00: empty figures, never an error.
- The debts' CSV across pages while a payment lands: two pages from two snapshots.

---

## 11. The commits

Conventional Commits; subjects counted (≤ 50); a body that says why; no tool attribution; staged by path. Every new
decision and history line ends with `<the day's date>, #PRNUM`. **C0** in PR 2 and PR 3, only if a
`0_CARRIED_FROM_<n>.md` naming that PR exists in this folder when its executor starts: its items as it says, in that
PR's first commit(s), each red first, with its break; the description says "Carried from #n".

### PR 1 — `feat/audit-log`, title `feat(audit): read the owner's and admin's logs` (46)
| # | Subject | Chars | Holds |
|---|---|---|---|
| C0a | `fix(subscriptions): move unstarted renewals too` | 47 | D2's chain; T-C1–T-C4; finding 151 (new, *Status:* Resolved, its *Resolution* line), its index line (Resolved); contract (the extension's preview, `201`, audit `renewalIds`); data model (*Checked by the service*, *ClosureExtension*); `subscriptions.md` (*Behaviour*, an *API decisions* line, history) |
| C0b | `fix(subscriptions): refuse a key of another space` | 49 | D2's key; T5's line; contract (the extension's errors); `subscriptions.md` (the key decision's line) |
| C0c | `docs: correct the extension's key and history` | 45 | `data-model.md:23` (unique on its own, linking line 140); `subscriptions.md`'s history: `#123` below `#118` |
| C1 | `feat(audit): read a space's audit log` | 37 | shared `audit`; the module, `auditPeriod`, the owner's route; U2, U3, T1–T9; contract *Audit log* (the owner's); conventions §6, §7; security; data model (*AuditLog*); `features/audit.md` (first) |
| C2 | `feat(audit): read the platform's audit log` | 42 | `platformEvents.ts`, the admin's route; U1, T10–T14; contract (the admin's); conventions §6 (the allowlist); security; `audit.md`; v1-mvp (the two rows, step 11 *Built*); overview (*Built*); `docs/README.md`; (finding 152, Q10) |

### PR 2 — `feat/platform-settings`, title `feat(platform-settings): edit defaults and contact` (50)
| # | Subject | Chars | Holds |
|---|---|---|---|
| C1 | `feat(platform-settings): read and save its cards` | 48 | shared `platform-settings`, the moved defaults' schema; the catalogue's contact keys; the six admin routes; the writer's `entityId`; the audit list's three actions; U1–U2, T1–T8, PR 1's T11 line; contract *Platform settings*; data model; conventions §6, §7, §9, §13; finding 40 resolved and its index line; `features/platform-settings.md` (first), `space-settings.md` |
| C2 | `feat(platform-settings): answer the public contact` | 50 | `GET /settings/public`; T9–T10; contract; conventions §7; `platform-settings.md`; v1-mvp (the rows); overview (*Built*); `docs/README.md` |

### PR 3 — `feat/finance`, title `feat(finance): read a space's money and occupancy` (49)
| # | Subject | Chars | Holds |
|---|---|---|---|
| C1 | `feat(finance): read a space's income` | 36 | `monthOf`, `addMonths`; shared `finance`; `windows.ts`; `payments.incomeIn`, `firstReceivedAt`, `collectionsIn`; the module, its income route; U1, U2, U4, T1 (income), T2–T6; contract *Finance* (income); data model (*Income*, *Collections*); conventions §7, §9; security; `features/finance.md` (first), `payments.md` |
| C2 | `feat(finance): read who owes and who paid` | 41 | `balancesPage`, `balanceTotals`, `uncollectedTotals`, `contactsOf`'s `archived`; the debts and payers routes; T1 (both), T7–T11; contract; conventions §9 (*overview* reads the two); `finance.md`, `payments.md` |
| C3 | `feat(finance): read a space's occupancy` | 39 | `occupancyGrid.ts`, the occupancy reads and route; U3, T1 (occupancy), T12–T14; contract; data model (*Occupancy statistics*); `finance.md`; v1-mvp (the row, step 11 *Built*); overview (*Built*); `docs/README.md` |

---

## 12. Verification and the procedure

**The same procedure for each PR**, with that PR's branch and checks. The executor of PR *n* reads this whole
plan and builds only PR *n*.

### 12.1 Before the branch
```powershell
Set-Location C:\dev\masaha\app-b
git fetch origin
git status --short --branch            # clean, detached at origin/main
git log --oneline -10 origin/main
git diff --name-status 3855e37f origin/main
gh pr list --state open --json number,title,headRefName,headRefOid,files
Get-ChildItem C:\dev\masaha\workspace\WORKER_B\FINANCE_AUDIT -Filter '0_CARRIED_FROM_*.md'
```
- **PR 1:** #123 merged (`gh pr view 123 --json state,mergeCommit`); else stop. Its merged files hold D2's starting
  point (`coveredCount`, `lockCovered`, `findByKey` as read at `ff8743c8`); a difference → stop and ask.
- **PRs 2–3:** the previous PR merged; its files hold what this plan says.
- **Any PR:** a change on `main` since `3855e37f` to a code file this PR names (§7), outside the item's own PRs →
  stop and ask. An open PR that edits one of them → stop and ask; one that edits a shared document: re-read it on
  the merged tree before editing (workflow §9).
- `0_CARRIED_FROM_<n>.md` naming this PR: read it whole and the review it cites; its items are C0 (§11); if they
  contradict this plan → stop and ask.

```powershell
git switch --no-track -c <feat/audit-log | feat/platform-settings | feat/finance> origin/main
docker start masaha-postgres-1         # never npm run db:up; never npm ci
npm run build -w @masaha/shared
```
- `apps/api/.env` names `masaha_b_dev` / `masaha_b_test` and `PORT=3321` (`Select-String` by pattern; never print
  the file).
- After a merged migration (#123's `closure_extension_key` before PR 1): `npm exec -w @masaha/api -- prisma
  generate`, `npm run db:migrate` (applies to `masaha_b_dev`); `prisma migrate status` → up to date. If
  `node_modules` misses a package: stop and ask (no `npm ci`).

**Memory: one full test run at a time on this machine.** Before each full lane, write the free memory into the
report and check that no `vitest` of worker A's runs:
```powershell
Get-CimInstance Win32_OperatingSystem | Select-Object FreePhysicalMemory
Get-CimInstance Win32_Process -Filter "Name = 'node.exe'" |
  Where-Object { $_.CommandLine -match 'vitest|tsc' } | Select-Object ProcessId, CommandLine
```
- A `vitest` (or `tsc`) under `C:\dev\masaha\app\`: wait for it to end; never stop it.
- **A full lane killed for low memory is re-run once, when the machine is quieter** (the free memory recorded
  again); **killed again → record it, carry on, and CI's run of that lane on the pushed head judges it** (red there
  → stop).

### 12.2 First checks (each when its code exists)

**Every PR**
1. **A schema change, only if the owner ordered one** (an index after check 4): the schema edit; `npm exec -w
   @masaha/api -- prisma migrate dev --create-only --name <name>` **once**, then `Get-ChildItem
   apps/api/prisma/migrations | Select-Object -Last 2`; **never run `--create-only` twice** (a second run applies
   the first). Non-interactive or a data-loss refusal: `npm exec -w @masaha/api -- prisma migrate diff
   --from-migrations apps/api/prisma/migrations --to-schema-datamodel apps/api/prisma/schema.prisma --script` into
   the folder, and say so. **No PR number in a migration's SQL** (a date only). `npm run db:migrate`
   (`masaha_b_dev`); `masaha_b_test` by the API lane's global setup, confirmed in its first output.
2. **The level rule:** `npm run lint` passes with D1's imports. A refusal: stop and ask.

**PR 1**
3. **`lockMoved` in one statement:** PostgreSQL accepts `FOR UPDATE` on the outer `SELECT` over the recursive CTE
   (T-C1 green). If it refuses: read the chain's ids first under the space's lock (no `FOR UPDATE`), then `SELECT
   "id" FROM "subscriptions" WHERE "id" = ANY(${all}) ORDER BY "id" FOR UPDATE`; say so (the space's lock keeps the
   set unchanged between the two).
4. **The cost on a year** (`scripts\audit-year.sql`, on `masaha_b_test` only, through `docker exec
   masaha-postgres-1 psql`): one space and its users, then `generate_series` inserting 36 000 audit entries over 365
   days (a desk's mix: 95 % visit, check-in and payment actions, 5 % platform ones) and 300 000 entries of other
   spaces; `EXPLAIN (ANALYZE, BUFFERS)` of D5's page and count, the owner's (`LAST_30_DAYS`, `ALL`, with `q`) and the
   admin's (`ALL`, with `q`). Record each plan's time. **Over 150 ms for any one → stop and report** with the plans
   (the owner decides an index, A3). The API lane empties the tables before each file; truncate them after anyway.
5. **`masaha_search_text`** exists on the test database (directory's migration) and folds «أحمد» into «احمد» (T5).
6. **The demo data for the real run** (§12.6): a covered subscription with a renewal not started in the demo space
   (SQL); if none, the carried real-run case is **not performed** (with why and its test, T-C1).

**PR 2**
1. **`Prisma.JsonNull`** writes a JSON `null` into the required `Json` column (T2's clear). If Prisma refuses: delete
   the optional row instead (`ensure` then recreates it on the next save) and say so.
2. **`INSERT … ON CONFLICT ("key") DO NOTHING`** supplies `updated_at` (the column has no database default: `@updatedAt`);
   check `\d settings` and pass `now()` if it has none.
3. **The shared move:** `@masaha/shared/space-settings` exports `newSpaceDefaultsSchema`; the API's
   `platform-settings/index.ts` re-exports it, so the seed's imports (`demo.ts`, `demoDirectory.ts`) are untouched;
   `npm run build -w @masaha/shared` and the typecheck green. The schema's error codes for the minutes are the space
   settings' (`required`, `invalid_format`); if the refinement cannot give two codes, use one `invalid_format` and say
   so.
4. **The dev data:** `SELECT key, value FROM settings` on `masaha_b_dev` — each row passes its read schema (a
   `contact*` row in another form: stop and report; no migration is planned).

**PR 3**
1. **`unnest` of two `timestamptz[]` with `WITH ORDINALITY`** binds through `Prisma.sql` (`${froms}::timestamptz[]`)
   and answers in order (T3). If not: one `VALUES` list built with `Prisma.join`, and say so.
2. **`balancesOf` reused** as a fragment by the new functions without change; if a change is needed to its text,
   stop and ask (the customers list reads it).
3. **`gazaClockOf`'s fields:** it answers the Gaza weekday (0 = Sunday) and the minute of the day; if it answers the
   date and minute only, derive the weekday with `weekStartOf` and `daysFrom` (`core/gazaTime.ts`), and say so.
4. **The cost on a year** (`scripts\finance-year.sql`, `masaha_b_test`): one space, 500 subscriptions, 9 000 visits,
   3 000 check-ins and 10 000 payments over 365 days (5 % voided, 2 % written-off visits), and 10 other spaces of the
   same size; `EXPLAIN (ANALYZE, BUFFERS)` of each D10 and D11 statement and the payers'. **Over 150 ms for any one →
   stop and report** with the plans.
5. **The demo data for the real run:** payments in the current month, a debtor, a customer in credit (the exam
   student's), closed stays in the 14 days (SQL); a figure the data cannot show → that case **not performed**, with
   why and its test.

### 12.3 Implement, commit by commit
- Stage **by path** (never `-A` or `.`), `git status --short` before each commit; after each commit `npm run lint`
  and `npm run typecheck`, and the commit's own test files in their lanes.
- Inside each commit: the test first, run red in its lane (the red output in the report); the code, then green; the
  commit's documents (Appendix A).
- **No new error code is planned.** If one proves needed: stop and ask; once approved, the `add-error-code` steps in
  order — (1) the code in `packages/shared/src/core/errors.ts`'s list; (2) its text in **both**
  `apps/web/src/shared/copy/arabic/errors.ts` and `…/english/errors.ts` (the typecheck fails while one is missing),
  the Arabic marked for the owner; (3) its line in api-contract §6; (4) the test that provokes it; and the PR gains
  `area:web` and names the two catalogues as shared with worker A.
- Each commit message in a UTF-8 file, **no BOM, LF line endings**, with a body; `git commit -F <file>`.
- **A fix before the push** folds into its commit:
  ```powershell
  git commit --fixup=<sha> -- <paths>
  $env:GIT_SEQUENCE_EDITOR=':'; git rebase -i --autosquash $(git merge-base HEAD origin/main); Remove-Item Env:GIT_SEQUENCE_EDITOR
  git rebase -x "npm run lint && npm run typecheck" $(git merge-base HEAD origin/main)
  ```
- **Fix rounds** (after a review) run **only the touched test files**, lint and typecheck — never a full lane; CI
  judges (the owner's rule, 2026-10-26).

### 12.4 Verification on the head (phase 4)
- One at a time, each **once, on the head** (re-run only if a file it covers changed after it passed): `npm run
  lint` · `npm run typecheck` · `npm run test:unit` · `npm run test:api` (no command timeout: ≈ 10 minutes) · `npm
  run format:check` · `npm run check:links` · `npm run check:conflicts` · `npm run build -w @masaha/shared` (the
  shared package changes in every PR).
- Also: `git grep -n "#PRNUM"` lists only documents (before §12.7); `git diff --stat origin/main -- apps/web
  package.json package-lock.json` is empty.
- **Not run, with why:** `test:component`, the web's `build`, `check:build`, `check:classes`: no web file changes;
  CI runs them on the pushed head.

### 12.5 The breaks — every one run, its red recorded
- For each B of §9: back up the file into `scripts\breaks\`, make the one edit, run the named test file in its lane,
  copy the red lines into the report, restore **from the backup** (never `git checkout`; SHA-256 before and after, no
  CRLF change — Python writes with `newline=""`), run it green, then `git diff --stat` shows only the item's own work.
  The scripts (`scripts\brk.py` and its JSON, as ANNOUNCEMENTS did) stay uncommitted.
- **A test seen red before its code is its own break**; a separate break only for a guard the red step did not prove
  (the owner's rule).
- **Every permission, money figure, privacy rule and race has its break:**
  - permissions — the owner, reception, the admin, another space's owner, a stranger, anonymous: PR 1 B12, B12a, B18; PR 2
    B9; PR 3 B6, B7, B7a;
  - money figures: PR 3 B8–B16, B17;
  - privacy (the admin never sees a space's customers, visits, subscriptions or payments; the admin is Masaha to the
    owner): PR 1 B1, B2, B6, B10, B13, B14, B15; PR 3 B11;
  - races: PR 1 B-C5; PR 2 B7, B8;
  - the carried items: B-C1–B-C6.
- **A break that stays green: stop**, unless it is plainly your own test's defect, or the break cannot change the
  outcome (a bound already excluded by another rule); then make the break that can, see it red, and state it as a
  departure.

### 12.6 The real run (API on 3321, `masaha_b_dev`)
Start `npm run dev -w @masaha/api` in the background (log to `scripts\server.log`, deleted afterwards);
`curl.exe -s http://localhost:3321/health` → `db: up`. Sign in as `demo-owner@example.com`,
`demo-reception@example.com`, `demo-directory-owner@example.com` and the seed's admin (`SEED_DEMO_PASSWORD` and
`SEED_ADMIN_*` read from `apps/api/.env` into variables, never printed). The script is `scripts\realrun<n>.mjs`,
**self-judging**: each case prints `PASS` or `FAIL` with its status, and the last line `ALL PASS` or the count failed;
**it never keeps an `/auth/` response's body** (only the access token, in memory). **A demo account or data that does
not hold what a case needs → that case "not performed", with why and the test that proves it; never change data
through the app to get past it.** The run's own writes are named in the report.
- **PR 1:** the owner `GET …/audit-log` → 200, its count; reception → 403; the directory owner on the demo space →
  404; the admin `GET /admin/audit-log?period=ALL` → 200, **every action on D3's lists** (the script checks each);
  **the run's writes:** the admin hides then shows the demo space and one unverified directory space (`PUT
  /admin/spaces/:id/hidden` true, false) → the admin's log shows the four with names; the owner's log shows the demo
  space's two with `actor.kind = MASAHA` and no id; `q=<the space's English name>` finds them; the carried case (check
  6): the owner previews and extends a closure posted by reception two days back covering a subscription with a
  renewal not started → the renewal's start moved (`GET …/subscriptions/:id`), or not performed.
- **PR 2:** the admin reads the three cards; `PUT …/staleness` with the same values → 200, no new audit entry
  (`SELECT count(*) FROM audit_logs` before and after); **the run's writes:** `PUT …/contact` with a test email and
  WhatsApp, then the original values back → both audited; `GET /settings/public` (anonymous) → the values and
  `Cache-Control`; the owner `GET /admin/settings/contact` → 403; the admin's log shows `platformSettings.contactEdited`
  twice.
- **PR 3:** the owner reads the four routes → 200; **cross-checks by SQL** (`docker exec … psql`, `masaha_b_dev`):
  the month's `income.totalAgorot` equals `SELECT sum(amount_agorot) FROM payments WHERE space_id = … AND voided_at
  IS NULL AND received_at >= <the month's Gaza midnight>`; the debtors' `meta.totals.owed.customers` equals `GET
  …/customers?payment=OWES`'s `totalRecords`; the 14 days' visits equal `count(*)` of closed visits by check-in day;
  reception → 403 on each; the admin and the directory owner → 404. No write.
- Stop the server by its process ids (the `tsx watch` child, the server, `pino-pretty`); `Get-NetTCPConnection
  -LocalPort 3321 -ErrorAction SilentlyContinue` prints nothing.

### 12.7 The PR number, push and PR
- **`scripts\prnum-pr<n>.sh`**, modelled on `WORKER_B\_DONE\ANNOUNCEMENTS\scripts\prnum-pr4.sh`: it checks the branch and a
  clean tree, reads the next number from `gh api …/issues?state=all&per_page=1&sort=created&direction=desc`, stops
  unless it equals the number given, backs the head up (`backup/<branch>-pre-prnum`), rewrites `#PRNUM` in `docs`
  per commit tree (`git filter-branch --tree-filter`), removes `refs/original/`, checks that no `#PRNUM` remains and
  that the rewrite changed nothing but the number, rewrites the description file, and prints `PRNUM OK #<n> <head>`
  or `PRNUM STOP: <why>`.
- Then `npm run check:links; npm run format:check`; `git push -u origin <branch>`.
- `gh label list`: `feat`, `area:api`, `area:docs` exist (create a missing one with a description and a colour).
- At once:
  ```powershell
  gh pr create --assignee @me --label feat --label area:api --label area:docs `
    --title "<the PR's title, §11>" --body-file <§12.9's text, saved in scripts\>
  ```
- **GitHub's number must equal the script's** (worker A may open a PR meanwhile): if not, fix the documents (a
  fixup into the commits that hold it, the script run again with the right number) and `git push
  --force-with-lease`.

### 12.8 CI, CLEAN, conflicts, report
- `gh pr checks <n> --watch` (bounded), then `gh pr view <n> --json headRefOid,mergeStateStatus`: green **on the
  pushed head** (= `git rev-parse HEAD`) and `CLEAN`. Never merge; never rebase a `CLEAN` PR.
- **Conflicts:** for every other open PR, `git merge-tree --write-tree HEAD <its headRefOid>`; record clean or the
  conflicted paths. Documents only: the fast path when its turn comes. Code: stop and ask.
- **The report**, `4_REPORT_PR<n>.md` in this folder, written **as the work goes**: after the first checks, after each
  commit (sha, subject with its length, red, green), after each break, after the real run, after the push. It holds
  each command run or not, §12.2's results (the measured plans' times), the owner's answers to §13 as built, problems
  and their solutions, anything unexpected, the conflict check, every departure with why, and the file count.
- **PR 1's report** appends to `C:\dev\masaha\workspace\_SHARED\OPEN_DECISIONS.md` point 2: "finding 151 resolved
  (#n, <date>): the extension moves each covered subscription's renewal chain not started". **PR 3's report** appends
  to point 3: "the owner's debts with their phones are read on `GET …/finance/debts` (#n), the CSV built in the
  browser; no export route". The supervisor commits nothing there.
- **Never leave silently:** a carried item, a review nit or a planned break undone is said, with why.

### 12.9 The PR description
```markdown
## Summary
<PR 1: the owner's audit log of the space (the admin shown as Masaha) and the admin's log of the platform's events, by a default-deny list; paged, the last 30 days or all, searched by target, filtered by actor and action.
 PR 2: the platform's settings as three cards the admin reads and saves on its own — the new-space defaults, the staleness thresholds and the contact, now in the typed catalogue (finding 40) — and the public contact.
 PR 3: the owner's finance: income (cash collected, voided payments left out) by month, day and staff member; who owes and who is in credit with the totals and the reminder's text; who paid in the month; occupancy from closed stays.>
<"Carried from #n": each item, if C0 exists (PR 1: the four of #123, finding 151 first)>

## Scope / Acceptance criteria / Out of scope
<§2, this PR's part>

## Change type
feat — API code, the shared contract, tests and documents; no migration; no web change; no dependency.

## New error codes
None.

## Evidence
- `lint`, `typecheck` (each commit), `test:unit`, `test:api`, `format:check`, `check:links`, `check:conflicts`, `build -w @masaha/shared`: <results>.
- Seen failing first: <each test, its red line>.
- Deliberate breaks, each red then restored: <the PR's B-list>.
- Measured on a generated year: <each statement's time> (PR 1, PR 3).
- Real run on 3321: <statuses, the run's own writes>.
- Not run: `test:component`, the web's `build`, `check:build`, `check:classes` — no web file changes; CI runs them.

## Screenshots
None: API and documents only.

## Definition of Done checklist
- [x] Acceptance criteria met, scope kept.
- [x] Lint and typecheck clean; `packages/shared` builds.
- [x] Tests added in the owning lanes, each seen failing.
- [x] No hardcoded user-facing text (codes and data only).
- [x] Authorization on the server (`requireCan`, the boundary, `/admin`'s guard; the admin's allowlist).
- [x] Triggered documentation updated in this PR.
- [x] One home per fact; nothing claimed that is not built.
- [x] Every claim names its test or command.
- [x] Atomic history, pushed.
```

### The executor's rules
- **A test you cannot run** (it errors before any test runs: the database unreachable, Docker down, a port taken, a
  module or `dist` missing, a migration pending, `No test files found`, a startup error, the whole run timing out):
  **record the command and its exact error, carry on with the rest, and CI judges** — never skip, `.skip` or delete
  a test, never weaken it, never change a config, a timeout, `.env`, a script or a lane, never run a narrower
  command and call it the lane. A **failing** test whose code is not written yet is the plan's red step.
- **A plan that proves false against the code:** stop, say exactly what and why, and offer the fix — do not choose it.
- **Never claim a result you did not see:** a command passed only if its own output said so (read by its exit code).
- **Never leave silently;** **no stop for the file count** (report it); the scripts stay in `scripts\`, never
  committed; never merge; no tool attribution; stage by path.

### Stop and ask
- #123 (PR 1) or the previous PR not merged, or merged in a shape §12.1 does not match; `origin/main` changed a code
  file of §7 otherwise; an open PR edits one; a carried file contradicts this plan.
- A change needed in `apps/web`, a dependency, an error code, or a schema change the owner did not order.
- A measured statement over 150 ms (§12.2 PR 1 check 4, PR 3 check 4); a dev `settings` row that fails its schema.
- The level rule refusing an import of D1; `balancesOf` needing a change.
- A break that stays green (§12.5's exception aside).
- A failure not understood after three root-cause fixes; CI failing for a reason not reproduced locally after three.
- A conflict with another open PR in a code file.
- The owner's answer to §13 changing a test or a rule beyond what it says.

---

## 13. Decisions needed from the owner

1. **Q1 — the finance routes and shapes (decision 13):** four routes, one per tab's need (D1, D8): `income?month`,
   `debts?state&page` (with the totals, the uncollected visits and the reminder template), `payers?month&page`,
   `occupancy?month`. *Recommended.* *Otherwise:* A1, one route.
2. **Q2 — what the debts count (D10, D12):** a written-off visit, a voided payment and an unpriced visit owe nothing;
   **an archived customer's debt is kept, marked `archived`** (it is still owed, and the desk collects it); a
   walk-in's uncollected visit is not a customer's debt but a figure of its own (`uncollected`). *Recommended.*
   *Otherwise:* archived customers left out.
3. **Q3 — the occupancy figures (D11):** a member counted once a day; the average present per hour = the stays
   overlapping that hour ÷ 4, over the 28 days before today; the peak hour = the month's hour of most presence; daily
   attendance = visits + members, averaged over the days with any; the average stay in whole minutes.
   *Recommended.*
4. **Q4 — the month's bounds (D9):** the current Gaza month and 23 before it (the web's select shows them); «اليوم»
   and «منذ البداية» kept beside the month (data model › Income).
5. **Q5 — no new index (D13):** each read measured on a generated year; one over 150 ms stops the item for your
   decision. *Recommended.* *Otherwise:* A3 now.
6. **Q6 — the audit entry (decision 15, D4–D5):** `before`/`after` as stored; the target's current name; `MASAHA`
   decided by links (S1), the owner's actor filter never naming an admin (S4); `meta.actors` (S7). *Recommended.*
7. **Q7 — the admin's allowlist (D3):** the list as written: the spaces' public facts and existence whoever acted,
   owners, the platform's accounts (those naming no space), lookups, the reports' decisions, the platform's settings;
   never the operations, capacity, override, settings or staff of a space. *Recommended.*
8. **Q8 — the audit filters (decision 15):** `period` `LAST_30_DAYS` | `ALL` only (the prototype's «فترة محدّدة» not
   built, A5); `q` by the target's name (and, for the admin, the space's); `actor`; `actions` (≤ 30). *Recommended.*
9. **Q9 — the platform settings' contract (decision 16, S9–S11):** three resources (`GET`/`PUT
   /admin/settings/{new-space-defaults|staleness|contact}`), the defaults' schema moved to
   `@masaha/shared/space-settings`; thresholds 1–365; the contact cleared with `null`, read in its stored form;
   `GET /settings/public` cached 5 minutes; no data migration; the site's switch from `VITE_CONTACT_*` is worker A's.
   *Recommended.*
10. **Q10 — decision 10's cost:** at about twenty busy spaces the audit table grows by ≈ 730 k entries (≈ 200 MB with
    its indexes) a year, against Neon's free 0.5 GB (ADR 0014). *Recommended:* keep decision 10, and PR 1 records
    **finding 152** so a retention rule (A4) is decided before the limit, not at it. *Otherwise:* A4 now.
11. **Q11 — the carried item 1's details (S12):** the preview counts the renewals it will move; the audit names them
    `renewalIds` beside `subscriptionIds`; item 2 answers `conflict` (D2). *Recommended.*
12. **Q12 — the PRs as cut (decision 17):** PR 1 ≈ 36 files, PR 2 ≈ 32, PR 3 ≈ 36; no migration, no error code, no
    web change. The documents this proves wrong, each changed in its PR as a proposal you approve here: v1-mvp's
    finance row ("CSV export" → no export route; decision 5), its `/admin/settings` row (→ three cards); conventions
    §6's "no design yet" (O13); data model's settings exception (finding 40).

---

## Appendix A — the documents, line by line (the commit in brackets)

Every new decision and history line ends with `<the day's date>, #PRNUM`; *Last Updated* on each document changed.
New capability documents follow `docs/architecture/documentation.md` §5 (API parts only; *Who uses it* names the
web feature where one exists).

### PR 1
1. **Finding 151** (new): title "A renewal sold before a closure's extension stays where it is"; *Status:* Resolved;
   evidence as the review's finding 1; *Resolution* (the day's date, #PRNUM): option A, D2. Index: under *Resolved*
   [C0a].
2. **`api-contract.md`** — the extension's preview ("how many it covered" → "how many it will move: those it covered
   and their renewals not started"), its `201` (the renewals' start and end moved; audit `after: { days,
   subscriptionIds, renewalIds }`) [C0a]; its errors (a key of another space's closure: `conflict`) [C0b]; new
   section *Audit log* after *Favourites*: the two routes, the query, `AuditEntry`, `PlatformAuditEntry`,
   `AuditMeta`, the actor rule, the allowlist's summary linking conventions §6 [C1, C2].
3. **`data-model.md`** — *Checked by the service*: the extension's line gains the chain [C0a]; *Entities ›
   ClosureExtension*: "moved on" includes the renewals [C0a]; line 23: the extension's key unique on its own [C0c];
   *Entities › AuditLog*: kept for ever in v1 (decision 10) [C1].
4. **`conventions.md`** — header *Built*: the audit reader; *Not yet built*: without it [C1]; §6: "Reading is a
   module" + built, the owner's log, `MASAHA` by links; the allowlist's home and the account rule; finding 14's line
   rewritten (designed by O13; the screen open) [C1, C2]; §7: `audit`'s *Holds* [C1].
5. **`security.md`** — *Authorization*: the owner's audit log (`requireCan('space.auditLog.read')`); the admin's log
   the platform's events only [C1, C2].
6. **`features/audit.md`** (new) [C1, C2]; **`features/subscriptions.md`** — *Behaviour* (the closures paragraph:
   the chain), *API decisions* (the chain; the key's space), history order and line [C0a–C0c].
7. **`v1-mvp.md`** — the two `audit-log` rows built; step 11 *Built* (the audit reader) [C2]. **`overview.md`** —
   *Built*: an *Audit* line [C2]. **`docs/README.md`** — the map's `audit.md` line [C2].

### PR 2
1. **`api-contract.md`** — new section *Platform settings*: the six admin routes, their bodies and bounds, the audit
   names; `GET /settings/public` and its cache [C1, C2].
2. **`data-model.md`** — *Conventions › Settings*: no exception left; *Entities › Setting*: the contact keys in the
   catalogue, optional [C1].
3. **`conventions.md`** — header *Built*: `platform-settings` (the cards, the public contact); §6's list: the
   platform's settings (already listed) — the allowlist line gains them; §7: its routers; §9 *Settings*: finding 40's
   sentence removed; §13: the settings' row lock [C1, C2].
4. **Finding 40** — *Status:* Resolved, its *Resolution* line; index moved [C1].
5. **`features/platform-settings.md`** (new) [C1, C2]; **`features/space-settings.md`** — code map: the defaults'
   schema in its shared folder [C1].
6. **`v1-mvp.md`** — `/admin/settings` row → the three cards (built); `/settings/public` built [C2];
   **`overview.md`** — *Built*: a *Platform settings* line [C2]; **`docs/README.md`** [C2].

### PR 3
1. **`api-contract.md`** — new section *Finance* after *Front desk (managed)*: the four routes, `month` and its
   bounds, the shapes, what each figure counts and leaves out, the snapshot, the bounds (ADR 0014) [C1–C3].
2. **`data-model.md`** — *Derived values*: *Income* (the windows, Gaza days), *Collections* (by method), *Occupancy
   statistics* (D11's definitions) [C1, C3].
3. **`conventions.md`** — header *Built*: `finance`; §9 *Composed reads*: finance's debts through `payments`'
   balances; *`overview`*: it will read `payments.balanceTotals` and `uncollectedTotals` [C1, C2].
4. **`security.md`** — *Authorization*: finance's four routes `requireCan('finance.read')` [C1].
5. **`features/finance.md`** (new) [C1–C3]; **`features/payments.md`** — *Behaviour*: the aggregates, *Who uses it*:
   finance [C1, C2].
6. **`v1-mvp.md`** — the finance row (its four routes; no export route, decision 5), step 11 *Built* [C3];
   **`overview.md`** — *Built*: a *Finance* line [C3]; **`docs/README.md`** [C3].

## Appendix B — Claude Code skills, only a map

| Step | Skill (if the executor is Claude Code) |
|---|---|
| §12.1, the branch | `start-work-item` (its git part) |
| Each test red first, each break | `superpowers:test-driven-development` (workflow §10) |
| A new error code (none planned; only after the owner's yes) | `add-error-code` |
| Any failure | `superpowers:systematic-debugging` |
| §12.4 before any claim | `superpowers:verification-before-completion` |
| §12.7–12.8 | `open-pr`, then `final-report` |

Only a map: the plan and the documents decide, and a skill that disagrees with them loses.
