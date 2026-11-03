# BACKEND_FINAL — the rest of Masaha v1's API: finance, the two overviews, and every API item left — the plan

> **Approved by the owner, 2026-10-29 — binding on every executor of this plan** (it wins where the plan below
> differs): **§12 OD1–OD11 as recommended** —
> - **OD1** (a): "ending this week" = the one `ENDING_SOON` rule, each customer's current subscription, equal to
>   `GET …/customers?status=ENDING_SOON`, **with the first five names**.
> - **OD2** (a): one figure — the tile = unverified and not hidden, the spaces tile's «غير موثّقة» the same.
> - **OD3** (a): `GET /admin/spaces` gains `status=editable` (unverified, hidden included) with `stale=true`, in C10;
>   the card's total equals the list's.
> - **OD4**: `GET /admin/overview` replaces v1-mvp's planned `/admin/stats`; `platform.stats.read` **removed**.
> - **OD5**: finding 170 **in** (C12). **OD6**: `GET`/`PATCH /me` **in**. **OD7**: `GET …/visits` **in**, (a) the
>   owner any range (≤ the payments list's bound), reception today only. **OD8**: finding 167 **in** — **#129 is
>   merged** (`d40d20f5`, 2026-10-29), its condition met.
> - **OD9** (a): finding 152 decided after the first deployment's measurement; it stays Open. **OD10**: finding 171
>   **out** (a later desk item, option (a) recommended there). **OD11**: one PR (≈ 95 files).
> - S1–S… and D1–D… as planned; the design issues DI1–DI9 handed to worker A's screens; the executor checks EC1–EC15
>   run as written; the *Proposed alternatives* are **not** taken unless the execution prompt says so.
> - **The base moved:** `main` = `d40d20f5` (#129 merged: `apps/web`, documents — shared documents
>   `overview.md`, `architecture.md`, `docs/README.md`, the findings index (findings 180, 184, 187 added, 8, 131,
>   169, 173 resolved): re-read each on `main` before editing it). No API file changed since `e3b2f97b`.
> - **The execution rules** (lanes, joins, tests, memory, stops) come in the execution prompt, which wins over §8.4.
>
> Edit any item by its number (§, `D…`, `S…`, `T…`/`U…`, `B…`, `DI…`, `OD…`, `EC…`). The owner's decisions are in §2
> and this note, binding.

---

## 1. Header

- **Base:** `origin/main` = **`e3b2f97b`** (Merge #130, `feat/platform-settings`, 2026-10-28). #128 (the audit reader)
  and #130 (the platform settings) merged. **#129** (worker A: announcements, data reports and favourites screens;
  `apps/web` and `docs`) is **open** at `819e1eea` — it touches no API file; shared documents only
  (`docs/project/overview.md`, `docs/frontend/architecture.md`, the findings index, `docs/README.md`) and it adds
  findings 167, 168, 180, 184, 187.
- **Worker:** B, in `C:\dev\masaha\app-b`. **Folder:** `C:\dev\masaha\workspace\WORKER_B\BACKEND_FINAL\` (this plan
  `2_PLAN.md`; the executor's scripts in `scripts\`, never committed).
- **One PR**, executed by a lead with sub-agents (the execution rules come with the execution prompt): branch
  **`feat/backend-final`**, title **`feat(api): finance, the overviews and the rest`** (47 chars).
- **Size:** ≈ **95 files** (≈ 60 code and tests, ≈ 35 documents), **16 commits** (§8; 12 if every pending OD says out), **no migration, no new error
  code, no dependency, no web file** (unless the owner chooses otherwise in §12).
- **Finding numbers:** this plan's own start at **154** (worker A's run uses 174–189). Planned: none new; any finding an
  executor records takes 154, 155, … in order.
- **Read** (commit objects and the detached worktree at `e3b2f97b`; `gh` read-only): `CLAUDE.md`; conventions §6–§9
  (the module table, R7, *`overview`*, *Composed reads*), §13; `api-contract.md` (the section list, *Platform settings*
  whole, the routes each overview figure comes from); `v1-mvp.md` (steps 11–12, *Planned API surface*); `docs/README.md`
  (*Deferred documents*); `docs/project/overview.md` (*Built*, *Dashboard*, *Admin*); foundation §13 (screens 12, 25);
  `SCREENS.md` (12, 25); the prototypes `Owner overview.html`, `Admin overview.html` and the data files they load; the
  findings index and findings 97, 152, 153, 167 (at #129's head), 170, 171, 187 (at #129's head); the code of `payments`
  (repository whole, service), `customers` (`namesOf`, `contactsOf`), `occupancy`, `subscriptions` (`calendar.ts`,
  `subscriptionStatus.ts`, `customerIdsBy`, `closures.summary`), `announcements` (`counts`), `spaces` (`staleness.ts`,
  `listing`), `space-links` (`adminSpaces`, `listingQuery.ts`, `verifiedSpaceIds`), `data-reports` (`ofSpace`, `all`),
  `users` (`page`, `namesFor`), `sessions` (finding 170's lines), `desk` (`customerFile`'s snapshot, `subscribe`),
  `platform-settings` (whole), `db/transaction.ts`, `shared/auth/can.ts`, `shared/audit/writeAudit.ts`,
  `packages/shared/src/core/gazaTime.ts`, `eslint.config.js` (the level map), `app.ts` (construction and mounts),
  `schema.prisma` (indexes), the seed (`run.ts`, `seed.ts`). Workspace sources (copied here, never pointed to):
  `WORKER_B\FINANCE_AUDIT\1_PLAN_PROMPT.md` §2, `2_PLAN.md` (the PR 3 parts), `6_REVIEW_PR2_CLAUDE_CODE.md` (F1–F4),
  `DESIGN\DECISIONS\DECISIONS_OWNER.md` (O3 and its amendment), `DECISIONS_ADMIN.md` (A8), `_SHARED\OPEN_DECISIONS.md`.
- **Could not prove by reading** → executor checks §13: EC1–EC15 (the SQL binding of `unnest … WITH ORDINALITY`, the
  cost on a generated year, where a `spaces` freshness read fits, the seed test's shape, the demo data, #129's merge
  state, and more).

---

## 2. The owner's decisions — binding (verbatim)

### 2.1 The finance (the owner, 2026-10-26)
1. ~~Three PRs, in this order~~ — **superseded by the owner, 2026-10-29: one PR** (this plan).
2. **Income is cash collected:** payments received, **voided ones excluded**; a written-off visit is not income; the
   debts are their own figures. (Finance.html says it: «الدخل = المبالغ المقبوضة فعليًا، بدون الدفعات الملغاة».)
3. **Periods as the design settled (OW-015):** one month chosen (Gaza's calendar month), and fixed windows for the
   charts — the last 12 months, the last 30 days, the last 14 days, the last 4 weeks — all on Gaza time. **No free
   date range.**
4. **The server aggregates:** each chart's series and each figure computed by the API (a read model, conventions R7),
   never raw rows for the web to sum; answers bounded (ADR 0014's response size).
5. **CSV export is the web's:** built in the browser from the JSON the API answers; **no export route**. (The debts'
   CSV holds phones: the owner's alone, as the finance route is.)
6. **Finance is the owner's alone** (`finance.read`); reception reads nothing of it (it keeps «دفعاتي اليوم», #114).
7. **Occupancy statistics from closed stays**, those closed by the auto check-out included; open ones excluded.
8. (audit, built by #128.) 9. (audit, built by #128.) 10. **Audit entries are kept for ever in v1** (no retention
   job). 11. (platform settings, built by #130.) 12. (finding 151, built by #128.)

### 2.2 The finance's open questions, approved as recommended (2026-10-27) — the finance part
- **Q1 — the routes and shapes:** four routes, one per tab's need: `income?month`, `debts?state&page` (with the
  totals, the uncollected visits and the reminder template), `payers?month&page`, `occupancy?month`.
- **Q2 — what the debts count:** a written-off visit, a voided payment and an unpriced visit owe nothing; **an archived
  customer's debt is kept, marked `archived`** (it is still owed, and the desk collects it); a walk-in's uncollected
  visit is not a customer's debt but a figure of its own (`uncollected`).
- **Q3 — the occupancy figures:** a member counted once a day; the average present per hour = the stays overlapping
  that hour ÷ 4, over the 28 days before today; the peak hour = the month's hour of most presence; daily attendance =
  visits + members, averaged over the days with any; the average stay in whole minutes.
- **Q4 — the month's bounds:** the current Gaza month and 23 before it; «اليوم» and «منذ البداية» kept beside the month.
- **Q5 — no new index:** each read measured on a generated year; **a read over 150 ms is recorded, not indexed** — no
  migration without the owner; the executor continues and the owner decides at the review (the approval note's rule).
- **Q10 — decision 10 kept**, finding 152 recorded (done by #128).
- **Q12 — the documents this proves wrong are changed in the PR as written** (v1-mvp's finance row "CSV export" → no
  export route).
- (Q6–Q9, Q11: the audit, the settings and finding 151 — built.)
- **The autonomy rule** (the approval note): no stop until ready for review; each "stop and ask" of this plan becomes
  decide, record under *Decisions taken without the owner*, continue — within the rule's hard limits; no stop for the
  file count; fix rounds run only the touched test files, CI judges the rest.

### 2.3 The overviews (the owner, 2026-10-29)
- **OV1 — the owner's overview (screen 12) is a work queue with no amount anywhere** (the owner's O3, amended
  2026-10-12: income and the debts' total are sensitive and the overview is often open at the desk, in view of
  customers and staff; they live in Finance only). Its order: **«يحتاج انتباهك»** first — the space's groups missing
  or stale, new data reports, the uncollected visits (a count), a started closure without its extension, capacity not
  set; then **«الحاضرون الآن»** — present now, capacity and the live status; then **the subscriptions ending this
  week** and **the announcements running**. Each item a count and a link to where it is acted on; confirm only beside
  what it confirms.
- **OV2 — debts on the owner's overview:** «عملاء عليهم ديون» as a **count of customers** only, linking to Finance ›
  debts; no amount.
- **OV3 — the overview is the owner's only.** Reception has none (it lands on the desk, as today).
- **OV4 — the admin's overview (screen 25) is a work queue** (the owner's A8): the tiles — spaces verified,
  unverified, **unverified with no owner**, open data reports, new users; **«اكتمال البيانات»** — the first five
  spaces with a group missing or stale that the admin can act on, with «عرض الكل»; missing is a warning, stale counts
  too (the tile and the card count stale **and** missing).
- **OV5 — "new users" = the last 30 days on Gaza's calendar.**
- **OV6 — "stale" uses the staleness thresholds the admin saves in the platform settings (#130)**, on both screens;
  never a constant in code.
- **OV7 — one aggregate endpoint per screen** (conventions §9, *overview*: the users' connection is weak), every
  figure from its owning module (no logic in `overview`; it never imports `finance` — the figures both show come from
  `payments`; fetched in parallel); no polling — the web refreshes on return to the page.
- **OV8 — the foundation's screen 12 line** (`docs/frontend/design-system/foundation.md` §13: "income today and this
  month, total debt") is corrected to OV1 by this plan, as O3 ordered.

### 2.4 The design decisions these rest on (copied)
- **O3** (2026-10-11): «يحتاج انتباهك» first (missing or stale groups, new reports, uncollected visits, a started
  closure without its extension, capacity not set), then money and «الحاضرون الآن», then the ending subscriptions;
  confirm only beside what it confirms; no bottom bar on the overview. **Amended 2026-10-12: no money on the
  overview** … «3 زيارات لم تُحصَّل» → the desk; «عملاء عليهم ديون» → Finance › الديون. Rule to change: foundation §13
  screen 12 drops "income today and this month, total debt". *Deferred, not v1:* a code the owner enters to open
  Finance.
- **A8** (AD-023, AD-022, AD-012): the fourth tile «مساحات غير موثّقة بلا مالك»; «اكتمال البيانات» lists only what the
  admin can act on, the first five, with «عرض الكل»; missing is `warning` (photos `neutral`), never `destructive`; the
  tile and the card count stale **and** missing.
- **OPEN_DECISIONS point 1** (#97): «يحتاج انتباهك» counts `GET …/unpriced-visits` and `GET …/uncollected-visits`.
- **OPEN_DECISIONS point 2** (#112): the owner learns of a closure through the summary's `closuresAwaitingExtension`,
  which the overview reads through `subscriptions`' `closures.summary`.

---

## 3. Scope, acceptance criteria, out of scope

### 3.1 Part one — the finance (build map step 11's last part)
**Scope:** `@masaha/shared/finance` (L5); `core/gazaTime.ts` gains `monthOf`, `addMonths`; the `finance` module (L5,
R7): `GET /manage/spaces/:spaceId/finance/{income|debts|payers|occupancy}` (🏢 `requireCan('finance.read')`);
`payments` gains the ledger's aggregates (D10); `customers.contactsOf` answers `archived`; `docs/features/finance.md`.

**Acceptance criteria**
- [ ] **AC-F1** Income for a month (`YYYY-MM`, the current Gaza month by default, at most 23 months back, never ahead):
  its total by subscriptions and visits, the month before, today and all time (with its first day), the last 12
  months and the visits' last 30 days by Gaza day, each staff member's collections by method — every figure the
  payments not voided, counted on the Gaza day received.
- [ ] **AC-F2** Who owes: each customer's debt (the balance rule of `payments`), largest first, paged, with the phone,
  whether archived, and the oldest item still owing with its day; who is in credit (`state=CREDIT`), largest first;
  the totals (owed, in credit, the uncollected visits apart) and the space's reminder template, all from one snapshot.
- [ ] **AC-F3** Who paid in the month: each customer with what they paid then, the latest paid first, paged.
- [ ] **AC-F4** Occupancy from closed stays (the auto check-out's included): visits and members per day over the last
  14 days (a member once a day); the average present per Gaza weekday and hour over the 28 days before today; the
  month's average stay (all, members, visits), peak hour and average daily attendance.
- [ ] **AC-F5** Only the owner reads them: reception 403 before the query is read; a stranger, another space's owner
  and the admin `not_found`; another space's money never counted.

### 3.2 Part two — the overviews (build map step 12)
**Scope:** `@masaha/shared/overview` (L5); the `overview` module (L5, R7, no logic): `GET
/manage/spaces/:spaceId/overview` (🏢 `requireCan('space.overview.read')`, a new `owner` action) and `GET
/admin/overview` (🛡); one set-based function added in each owning module that has none (D20); `docs/features/overview.md`.

**Acceptance criteria**
- [ ] **AC-O1** The owner reads, in one answer, **no amount anywhere**: the fact groups missing and stale (by the
  saved thresholds), the open data reports (count), the uncollected visits and the unpriced visits (counts), the
  started closures awaiting their extension (count), whether capacity is set, the customers who owe (count), the
  present now (visits, members, total), the capacity and the live status, the subscriptions ending soon (count and the
  first five), the announcements running (count and their types).
- [ ] **AC-O2** Each count equals the total of the list it links to, read at the same instant (the desk's
  uncollected and unpriced lists, the owner's reports `status=OPEN`, the announcements `state=RUNNING`, the customers
  `status=ENDING_SOON`), and the debtors' count equals Finance › debts' `meta.totals.owed.customers`.
- [ ] **AC-O3** Reception is 403; a stranger, another space's owner and the admin `not_found`; the answer serialised
  holds no `Agorot` field (a test searches the body).
- [ ] **AC-O4** The admin reads, in one answer: spaces verified, unverified and hidden (each equal to `GET
  /admin/spaces?status=…`'s total), unverified with no owner, stale or missing (equal to `?stale=true`'s total), the
  open data reports (and how many await the admin and how many the owners), the users created in the last 30 Gaza
  days, and «اكتمال البيانات»: the first five spaces the admin can act on (unverified, hidden included) with a group
  missing or stale, each with its missing and stale groups, and their total.
- [ ] **AC-O5** A saved threshold changes both overviews at once (OV6).
- [ ] **AC-O6** A guest 401, a user and an owner 403, an admin with a pending password 403
  `PASSWORD_CHANGE_REQUIRED` on the admin's route; the admin's answer holds nothing of a space's operations (no
  customer, visit, subscription, payment, capacity or presence).
- [ ] **AC-O7** No route writes; no polling route (`markPassive` not applied).

### 3.3 Part three — the API items left (§4.3; each "in" pending §12 where marked)
- [ ] **AC-L1** (F1) A contact stored in another form (`+972…`, mixed-case email) is answered as stored, and the next
  save stores its one form, audited with exactly that `before`/`after`; the contract says it in one sentence.
- [ ] **AC-L2** (153, F2) The seed checks and stores the contact through `emailSchema` and `phoneSchema`: a seeded
  `+97259…` is stored `+97059…`, an email lowercased, a foreign number refused at seeding; finding 153 resolved, its
  wording corrected first (F2).
- [ ] **AC-L3** (F3, F4) `platform-settings.md` drops "in the browser too"; "a save that changes nothing writes nothing"
  becomes "changes no value" in the contract and the document.
- [ ] **AC-L4** (97) Finding 97 moved to *Resolved* (#130 built its fix).
- [ ] **AC-L5** (170, if §12 OD5 = in) The idle check reads the family's latest activity; a request's renewal racing a
  rotation never ends a session early (a race test).
- [ ] **AC-L6** (`/me`, if OD6 = in) `GET /me` and `PATCH /me` (name, language) for any signed-in user.
- [ ] **AC-L7** (`GET …/visits`, finding 161, if OD7 = in) a space's closed and open visits of a range of Gaza days,
  paged.
- [ ] **AC-L8** (167, if #129 has merged and OD8 = in) `GET /admin/data-reports?handledBy=ADMIN|OWNER`.

### 3.4 Out of scope
- Every screen (19, 12, 25, and the rest): worker A's, once this API merges. **No `apps/web` file.**
- An export route (decision 5); a free date range on finance (decision 3); expenses, profit, consolidated finance
  (*Not in v1*); a debt reminder sent by Masaha (a WhatsApp link only); a code to open Finance (O3, *not v1*).
- Booking, online payment, QR, claiming, reviews (*Not in v1*).
- An audit retention job (decision 10; finding 152 stays open — §12 OD9 only asks when).
- Polling of either overview (OV7); the admin's stats beyond OV4.
- The out-items of §4.3.

---

## 4. The reading done — what `main` shows that the finance plan did not know

### 4.1 Finance claims re-verified (each correction marked)
- **R1** (re-verified 2026-10-29: **no aggregate exists**) `payments.repository.ts` holds `balancesOf` (lines 112–138),
  `DEBT`/`CREDIT` (144–145), `customerBalances`, `customerIdsByPayment`, `itemBalances`, `uncollectedPage`
  (299–324), `totals`, `page`, `count`. None of `incomeIn`, `firstReceivedAt`, `collectionsIn`, `balancesPage`,
  `balanceTotals`, `uncollectedTotals`: all six are new (D10).
- **R2** (re-verified: `uncollectedPage` and `customerIdsByPayment` read `prisma`, **no `tx`**) — the new
  `uncollectedTotals` and `balancesPage`/`balanceTotals` take `tx` (the debts' snapshot); the uncollected fragment is
  extracted to one `const` both `uncollectedPage` and `uncollectedTotals` use (no second copy of the rule).
- **R3** (re-verified: unchanged) `balancesOf(spaceId, customerIds | null, { today, weekStart })` is reused as a
  fragment with no change to its text; `Now` comes from `subscriptions/calendar.ts` `calendarOf(at)`.
- **R4** (re-verified: `contactsOf` answers `{ id, name, phone }`, **no `archived`**; its one other caller is
  `subscriptions.service.ts:172`) — it gains `archived: boolean` (`archivedAt !== null`); the other caller ignores it.
- **R5** (re-verified: **`monthOf`/`addMonths` do not exist**) `core/gazaTime.ts` exports `GAZA_TIME_ZONE`,
  `GazaClock`, `gazaClockOf`, `gazaInstant`, `addDays`, `daysFrom`, `weekStartOf`. **`gazaClockOf` answers `{ date,
  dayOfWeek, minute }`** — the finance plan's check 3 is settled: the hour slot's weekday is `dayOfWeek` (0 = Sunday),
  its hour `Math.floor(minute / 60)`.
- **R6** (re-verified) the audit writer's `entityId` is `number | null` (#130); finance writes no audit — no effect.
- **R7** (re-verified) `can()` lives in `apps/api/src/shared/auth/can.ts` (not `packages/shared`): `'finance.read':
  'owner'` (line 84), its unit test `OWNER_ONLY` (`can.unit.test.ts:93`). No `overview` action exists;
  `'platform.stats.read': 'admin'` (line 101) exists and nothing uses it.
- **R8** (re-verified) the level map (`eslint.config.js:12–17`): L5 `desk`, `directory`, `finance`, `overview`, `audit`.
  `finance` and `overview` may import L0–L4, never each other.
- **R9** (re-verified) `readSnapshot` (`db/transaction.ts:22`, read-only `REPEATABLE READ`) is injected only into
  `desk` (`app.ts:431`); `finance` gets its own `createReadSnapshot()` the same way.
- **R10** (re-verified 2026-10-29: **a correction to the finance plan's real run**) `GET …/customers?payment=OWES`'s
  `total` leaves **archived** customers out (`customers.page`), while Finance › debts keeps them (Q2). The cross-check
  is against SQL over every customer (§10), and T-F10 proves the archived debtor counted.
- **R11** (re-verified: a document contradiction) conventions §9 *Composed reads* says "`overview` (total owed)": O3
  forbids an amount — corrected to "`overview` (how many owe)" (D27).
- **R12** (re-verified) `users.namesFor(ids, tx?)` exists (`users.service.ts:485`; finding 79's optional `tx`).
- **R13** (re-verified) indexes: `payments (space_id, received_at)`, `(visit_id)`, `(subscription_id)`; `visits` and
  `check_ins` `(space_id, checked_in_at)` and `(space_id, checked_out_at)`; `subscriptions (space_id, ends_on)`;
  `data_reports (space_id, status)`, `(status)`; `audit_logs (space_id, created_at)`, `(created_at)`; `users` has **no
  index on `created_at`**.
- **R14** (re-verified) the space's reminder template is `spaceSettings.read(spaceId, tx).reminderTemplate`.
- **R15** (re-verified) the finance plan's executor rule "three PRs from `main` in sequence" is gone: one PR; the
  finance plan's §12.1 base check (`3855e37f`) is replaced by §13 EC1.

### 4.2 What the overviews' reading found
- **No `overview` module, shared folder or `can()` action exists**; only the level map and conventions §7/§9 name it.
- **Almost no figure has a count function** (the sweep, file:line in D20): most are pages read for their `total`, or id
  sets. The overview may not compute (OV7), so each owning module gains a set-based count — the conventions' "add one
  where none exists".
- **Verified ⇔ an active `OWNER` link** (`can.ts:192`, ADR 0009): there is no column. So **"unverified" and "unverified
  with no owner" are the same set of links**; the prototype's «بلا مالك» tile is `unverified && !hidden` — exactly `GET
  /admin/spaces?status=unverified` (`listingQuery.ts:30` forces `isHidden: false`). See OD2.
- **«اكتمال البيانات»'s set** (unverified, hidden included, stale or missing) **has no list today**: `status=unverified`
  leaves hidden out, `stale=true` alone includes the verified. See OD3.
- **"Ending this week" has no query.** The one rule is `subscriptionStatus`'s `ENDING_SOON` (≤ 7 days to its end, or
  ≤ 20 % of its days or hours left — `subscriptionStatus.ts:36`), read only through `GET …/customers?status=ENDING_SOON`
  (each customer's **current** subscription). See OD1.
- **"New" data reports** can only be `OPEN` (`DataReportStatus { OPEN, RESOLVED, DISMISSED }`; no seen flag).
- **The prototype's admin overview has no new-users tile** (OV4 adds it) and splits the open reports by who handles
  them (A8 / admin-data.js); the owner's prototype counts «زيارة لم تُحصَّل **اليوم**» (OV1 says the uncollected visits,
  a count: the desk's list has no day) and shows «اليوم: …» (present + left today) — DI1, DI2.
- **Foundation §13 line 459** still lists "income today and this month, total debt" (OV8); **line 474** lists the
  admin's figures with "new users" (kept).

### 4.3 The API items left (swept; recommendation each)

| # | Item | Where | The fix | Size | Recommendation |
|---|---|---|---|---|---|
| L1 | **F1** (#130's review, should-fix, copied in full in D30) — a contact stored in another form answered as stored, rewritten by the next save | `platform-settings` tests; contract | a test pair (T-L1, T-L2) and one contract sentence | 3 files | **In** (owner's rule: review fixes ride the next PR's first commit) |
| L2 | **F2** — finding 153's wording ("a change no one made" → "a change of form the admin did not ask for") and its foreign-number case (`+20…` read, then the card unsavable without retyping) | finding 153 | two lines | 1 | **In**, then 153 resolved (L3) |
| L3 | **Finding 153** — the seed accepts any E.164 contact | `db/seed/run.ts:26–27`, `seed.ts:40–41` | the seed's contact through `emailSchema`/`phoneSchema` | 2–3 | **In** (small; makes F1's case impossible from the seed, and F2's) |
| L4 | **F3** — `platform-settings.md:29` "in the browser too" | doc | drop it | 1 | **In** |
| L5 | **F4** — "changes nothing writes nothing" untrue for an unset contact (rows of JSON `null` inserted) | contract, `platform-settings.md:11, 51` | "changes no value" | 2 | **In** |
| L6 | **Finding 97** — the rounding rule written twice | — (#130 moved `newSpaceDefaultsSchema` to `space-settings` with `roundingPair`) | move to *Resolved*, its *Resolution* line naming #130 | 2 | **In** (docs only) |
| L7 | **Finding 170** — a renewal racing a rotation can end a session early | `sessions.repository.ts:100–118`, `sessions.service.ts:92` | `familyActivity` reads `max(last_activity_at)`; the rotation copies that maximum; a race test | 3 | **In, recommended** (OD5) |
| L8 | **`GET`/`PATCH /me`** (v1-mvp *Planned API surface*: name, language) — not built | `users` | read and edit one's own name and language | ≈ 8 | **Owner (OD6)**, recommended in |
| L9 | **`GET /manage/spaces/:spaceId/visits`** (planned, date range; finding 161) — not built | `visits` | a paged read by a range of Gaza days | ≈ 8 | **Owner (OD7)**, recommended in |
| L10 | **Finding 167** (on #129 only) — the admin's reports not filterable by who handles them | `data-reports` | `handledBy=ADMIN|OWNER` on `GET /admin/data-reports` | 4 | **In if #129 merged first** (OD8); shares D24's rule |
| L11 | **Finding 152** — the audit kept for ever meets 0.5 GB | data model; a job | the owner decides a rule | — | **Out** of this PR; OD9 offers the options and when |
| L12 | **Finding 171** — a published price changed between read and subscribe | `desk`, a new code | the owner's options | 5 + a code | **Out**: the owner's (it said "with DESK_SCREENS PR 4"); needs a new error code; OD10 |
| L13 | **Finding 187** (on #129) — a favourite just removed cannot be saved again | `favorites` + migration | a removal window | ≈ 6 + migration | **Out**: the owner chose DI-58 (a), no undo |
| L14 | Findings 160, 162, 164, 166, 99, 83, 32 (an API read or field a screen would use) | various | each its own | — | **Out**: each waits on the owner's choice in its finding ("or the owner accepts") and a screen |
| L15 | Findings 17, 63 (sweeping jobs), 21, 23, 65, 92, 91, 84 | sessions, storage, auth, staff | jobs, measurements, owner decisions | — | **Out**: deployment measurements or owner decisions first |
| L16 | Findings 69, 77, 78, 79, 93, 106, 112, 115, 120, 121, 122, 126, 127 (small API or test fixes) | various | each named in its file | 1–4 each | **Out**: unrelated to finance and the overviews; one "findings sweep" item later is proposed (A9); 115 needs only the owner's move to *Accepted* |
| L17 | `docs/README.md` *Deferred documents* | — | its one row (*Endpoints* in the contract, each as built) | — | **Met**: this PR writes each new endpoint into the contract (§11) |
| L18 | `OPEN_DECISIONS.md` | workspace | — | — | Point 3 (finance's) and point 1/2 (the overview reads them): the report writes the lines of §11.3 |

---

## 5. Decisions as built

### 5.1 Routes and answers

**Finance (part one)**

| # | Route | Access | Query | 2xx | Module |
|---|---|---|---|---|---|
| D1a | `GET /manage/spaces/:spaceId/finance/income` | 🏢 `requireCan('finance.read')` | `financeMonthQuery` | **200** `IncomeReport` | `finance` |
| D1b | `GET …/finance/debts` | 🏢 `requireCan('finance.read')` | `debtsQuerySchema` (`state`, `page`, `limit`) | **200** `BalanceRow[]`, `meta: DebtsMeta` | `finance` |
| D1c | `GET …/finance/payers` | 🏢 `requireCan('finance.read')` | `payersQuerySchema` (`month`, `page`, `limit`) | **200** `Payer[]`, `meta: PaginationMeta` | `finance` |
| D1d | `GET …/finance/occupancy` | 🏢 `requireCan('finance.read')` | `financeMonthQuery` | **200** `OccupancyReport` | `finance` |

**The overviews (part two)**

| # | Route | Access | Query | 2xx | Module |
|---|---|---|---|---|---|
| D2a | `GET /manage/spaces/:spaceId/overview` | 🏢 `requireCan('space.overview.read')` (new, `owner`) | — | **200** `OwnerOverview` | `overview` |
| D2b | `GET /admin/overview` | 🛡 (`/admin`'s guard) | — | **200** `AdminOverview` | `overview` |

**Left items (part three, each if in)**

| # | Route | Access | Body / query | 2xx | Module |
|---|---|---|---|---|---|
| D3a | `GET /me` | 👤 | — | **200** `MyAccount` | `users` |
| D3b | `PATCH /me` | 👤 | `updateMeSchema` (`name?`, `language?`) | **200** `MyAccount` | `users` |
| D3c | `GET /manage/spaces/:spaceId/visits` | 🧾 | `visitsQuerySchema` (`from`, `to`, `page`, `limit`) | **200** `DeskVisit[]`, `meta` | `visits` |
| D3d | `GET /admin/data-reports?handledBy=` | 🛡 | `adminReportsQuerySchema` + `handledBy` | **200** as today | `data-reports` |

- **Mounts** (`app.ts`): `manage.use('/finance', createFinanceManageRouter(financeController))`;
  `manage.use('/overview', createOverviewManageRouter(overviewController))`; `admin.use('/overview',
  createOverviewAdminRouter(overviewController))`; `/me` in `users`' existing router (EC12); `visits` in its existing
  manage router. `/admin` keeps its one guard (`requireAuth()`, `requireRole('ADMIN')`, `app.ts:643`); the manage
  routers sit inside `requireSpaceAccess` (`app.ts:596–601`).
- **Placement and levels:** `finance` (L5) imports `payments` (L4), `subscriptions` (L3), `customers` (L2), `users`
  (L1), `space-settings` (L0), and reads `visits`, `check_ins` and the payers' items in its own repository (R7:
  occupancy statistics are `finance`'s, conventions §7's table). `overview` (L5) imports `spaces` (L1), `space-links`
  (L2), `announcements` (L2) through `subscriptions`' `closures`, `data-reports` (L3), `visits` (L3), `subscriptions`
  (L3), `payments` (L4), `occupancy` (L4), `users` (L1), and **has no repository** (S20).

### 5.2 Shared shapes

**D8 — `@masaha/shared/finance`** (L5; the finance plan's D8, re-verified)
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
`core/gazaTime.ts` gains `monthOf(date: string): string` (`'2026-10-29'` → `'2026-10'`) and `addMonths(month: string,
months: number): string` (pure, calendar only), which the web's month select uses too (conventions §11).

**D16 — `@masaha/shared/overview`** (L5; imports types from `spaces`, `announcements`, `occupancy` — lower levels)
```ts
OwnerOverview = {
  attention: {
    groups: { missing: FactGroup[], stale: { group: FactGroup, days: number }[] },   // days since its date, Gaza days
    openReports: number,                     // the space's data reports OPEN
    uncollectedVisits: number,               // = GET …/uncollected-visits' total
    unpricedVisits: number,                  // = GET …/unpriced-visits' total
    closuresAwaitingExtension: number,       // = closures.summary's
    capacitySet: boolean,
    customersOwing: number,                  // OV2: a count; = finance/debts' meta.totals.owed.customers
  },
  presentNow: { visits: number, members: number, total: number,
                capacity: number | null, status: LiveStatus | null },   // status as the public sees it
  endingSoon: { total: number,                                          // customers whose current subscription is ENDING_SOON
                first: { customer: { id, name }, subscription: { id, name: string, endsOn: string | null } }[] },   // ≤ 5, the soonest first
  announcements: { running: number, types: AnnouncementType[] },       // the running ones' types, each once, in ANNOUNCEMENT_TYPES' order
  at: string                                                            // the instant read (ISO), for «آخر تحديث»
}
AdminOverview = {
  spaces: { verified: number, unverified: number, hidden: number,      // each = GET /admin/spaces?status=…'s total
            unverifiedNoOwner: number,                                  // OD2
            staleOrMissing: number },                                   // = ?stale=true's total
  reports: { open: number, awaitingAdmin: number, awaitingOwners: number },
  newUsers: number,                                                     // created since the Gaza midnight 29 days before today
  completeness: { total: number,
                  first: { id: number, nameEn: string, nameAr: string | null, hidden: boolean,
                           missing: FactGroup[], stale: { group: FactGroup, days: number }[], hasPhotos: boolean }[] },   // ≤ 5
  at: string
}
```
- **No `Agorot` field in either** (OV1, OV2; T-O3 searches the body).
- `days` per stale group: `daysFrom(gazaClockOf(date).date, gazaClockOf(now).date)` — computed **in `spaces`**
  (`staleness.ts` gains `staleDays`, pure), never in `overview`.

### 5.3 The finance — windows, aggregates, occupancy, service (copied, re-verified)

**D9 — the windows** (`finance/windows.ts`, pure)
- `monthWindow(month, now)` → `{ from, to }`: `gazaInstant(\`${month}-01\`, 0)` to the next month's; **`monthError(month,
  now)`** → `'out_of_range'` when after the current Gaza month or before `addMonths(current, -23)` (422 on `month`),
  else `null`.
- `todayWindow(now)`; `monthsEnding(current, 12)`; `daysEnding(today, n)` (30, 14); `allTime` = `{ from: null, to: now }`.
- `fourWeeks(now)`: the 28 Gaza days before today (today left out, so each weekday counts exactly 4 times);
  `hourSlots(days)` → `{ from, to, weekday, hour }[]`: every hour from each day's Gaza midnight, labelled by
  `gazaClockOf(from)` — `weekday = dayOfWeek`, `hour = Math.floor(minute / 60)` (R5) — so a daylight-saving night's
  hours are as Gaza counts them.
- Every window is a pair of instants; the SQL takes them as two arrays and buckets with `unnest(…) WITH ORDINALITY`
  (S2).

**D10 — the ledger's aggregates** (`payments`; reused by the overview)

| Function (service, `at: Date` where a `Now` is needed, `calendarOf(at)`) | Answers | Query |
|---|---|---|
| `incomeIn(spaceId, windows, tx?)` | per window `IncomeSplit`, in order | `unnest(${froms}::timestamptz[], ${tos}::timestamptz[]) WITH ORDINALITY w(f, t, i) LEFT JOIN payments p ON p.space_id = ${spaceId} AND p.voided_at IS NULL AND p.received_at >= w.f AND p.received_at < w.t`; `sum(…) FILTER (WHERE p.subscription_id IS NOT NULL)` and `… visit_id …`; `GROUP BY w.i ORDER BY w.i` (a `null` start: `'-infinity'`) |
| `firstReceivedAt(spaceId, tx?)` | `Date \| null` | `min(received_at)` not voided |
| `collectionsIn(spaceId, window, tx?)` | `{ recordedById, count, totalAgorot, cashAgorot, transferAgorot }[]` | `GROUP BY recorded_by_id`, not voided, by total desc then id |
| `balancesPage(spaceId, state, at, page, tx?)` | `{ rows: { customerId, amountAgorot, oldest }[], total }` | `WITH balances AS (balancesOf(spaceId, null, now))`: per customer `DEBT` or `CREDIT` (the existing sums), `HAVING > 0`, `ORDER BY amount DESC, customer_id`, `count(*) OVER ()`, `LIMIT/OFFSET`; `oldest` (OWES): the item with `due − paid > 0` of the least `created_at`, then visit first, then id (`DISTINCT ON (customer_id)`) |
| `balanceTotals(spaceId, at, tx?)` | `{ owed: { agorot, customers }, credit: { agorot, customers } }` | the same `balances`, per customer, then summed |
| `uncollectedTotals(spaceId, tx?)` | `{ visits, owedAgorot, unpriced }` | the `uncollectedPage` fragment (R2: one `const`), `count(*)`, `sum(charge − paid)`, `count(*) FILTER (WHERE charge IS NULL)` |

- **One balance rule:** `balancesPage` and `balanceTotals` read `balancesOf` (the owner's decision 6), so a written-off
  visit, a voided payment and an unpriced visit count as the customers list and file count them; an archived
  customer's debt is kept (Q2).
- **The overview** calls `payments.balanceTotals(…).owed.customers` and `payments.uncollectedTotals(…).visits` —
  never `finance` (conventions §9). No amount leaves `overview` (it drops `agorot` before answering).

**D11 — occupancy** (`finance/finance.repository.ts`, R7)
- **Closed stays:** `SELECT checked_in_at, checked_out_at, NULL AS customer_id, 'VISIT' AS kind FROM visits WHERE
  space_id = ${spaceId} AND checked_out_at IS NOT NULL AND checked_in_at >= ${from} AND checked_in_at < ${to} UNION ALL
  SELECT checked_in_at, checked_out_at, customer_id, 'MEMBER' FROM check_ins WHERE …` — the auto check-out's included;
  open ones out (decision 7); bounded by the check-in on the `(space_id, checked_in_at)` indexes (a stay never crosses
  midnight, data model › Auto check-out).
- `perDay(spaceId, days)` → per window `{ visits, members }`: `count(*) FILTER (WHERE kind = 'VISIT')`,
  `count(DISTINCT customer_id) FILTER (WHERE kind = 'MEMBER')` (a member once a day).
- `presenceBySlot(spaceId, slots)` → per slot the stays overlapping it (`checked_in_at < slot.to AND checked_out_at >
  slot.from`), the slots one pair of arrays; the stays read once for the range.
- `stayMinutes(spaceId, window)` → `{ all, members, visits }`: `round(avg(extract(epoch FROM checked_out_at −
  checked_in_at) / 60))`, `null` without stays.
- **Pure** (`finance/occupancyGrid.ts`): `averagePerHour(slots, counts, weeks = 4)` → `byHour` (sum per weekday and
  hour ÷ 4, one decimal, half up); `peakHour(slots, counts)` → the hour of the day with the most presence over the
  month, ties the earliest, `null` when none; `averageDailyAttendance(perDay)` → the mean of `visits + members` over the
  month's days with any, one decimal, `null` when none.
- **The month's figures** use the month's window up to now (the current month so far).

**D12 — the finance service** (`finance/finance.service.ts`; deps `{ readSnapshot, payments, customers,
subscriptions, users, spaceSettings, now }`)
- `income(spaceId, month?)`: `monthError` → 422; in one snapshot: `payments.incomeIn` over [month, previous, today,
  all time, the 12 months, the 30 days] (one call, 45 windows), `firstReceivedAt`, `collectionsIn(month)`; then
  `users.namesFor` (outside the snapshot, a name being no figure). Answer `IncomeReport`.
- `debts(spaceId, query)`: in one snapshot: `payments.balancesPage`, `balanceTotals`, `uncollectedTotals`,
  `customers.contactsOf(spaceId, ids, tx)` (with `archived`), `subscriptions.namesOf(spaceId, oldestSubIds, tx)`, the
  oldest visits' names through `visits.deskVisitsOf(spaceId, ids, tx)` (a visit's `visitorName`, else its customer's,
  EC6), `spaceSettings.read(spaceId, tx).reminderTemplate`. Answer `BalanceRow[]` and `DebtsMeta`.
- `payers(spaceId, query)`: `monthError`; `repository.payersIn(spaceId, window, page)` — the customers of the month's
  payments not voided (`coalesce(v.customer_id, s.customer_id)`, a walk-in's payment naming no one, left out), `sum`,
  `max(received_at)`, latest paid first, then customer id, with `count(*) OVER ()`; names by `customers.namesOf`.
- `occupancy(spaceId, month?)`: `monthError`; D11's reads in parallel (no snapshot: each figure stands alone).
- `finance.manage.routes.ts`: four `GET`s, each `requireCan('finance.read')` → `validate(<query>, 'query')` →
  controller; the controller answers `sendSuccess` with `meta` where D1 asks it.

### 5.4 The overviews — services, the functions they call, costs

**D20 — each figure, its owning module and the set-based function** (new ones marked **+**)

| Figure | Module | Function (service) | Today (file:line) | Query and cost on a busy space |
|---|---|---|---|---|
| groups missing / stale | `spaces` (L1) | **+** `spaces.freshnessOf(spaceId, at): Promise<{ missing: FactGroup[]; stale: { group, days }[] }>` | the pure rule `spaces/staleness.ts` (`groupDatesOf` 29, `staleCutoffs` 40, `staleGroups` 53, `missingGroups` 61); thresholds `platformSettings.stalenessThresholds` (`platform-settings.service.ts:134`) | one row by primary key (five date columns) + one settings read; the pure rule (OV6) |
| open reports | `data-reports` (L3) | **+** `dataReports.openCountOf(spaceId)` | `ofSpace` page (`data-reports.service.ts:164`), `pageOfSpace` (`repository:117–131`) | `count(*) WHERE space_id AND status = 'OPEN'` on `(space_id, status)` |
| uncollected visits | `payments` (L4) | D10 `uncollectedTotals(spaceId).visits` | `uncollectedPage` (`payments.repository.ts:299`) | the uncollected fragment, counted (on `(space_id, checked_out_at)`) |
| unpriced visits | `visits` (L3) | **+** `visits.unpricedCount(spaceId)` | `unpricedIn` page (`visits.service.ts:488`; repository 206–221) | `count(*) WHERE space_id AND checked_out_at IS NOT NULL AND charge_agorot IS NULL` (same `where` as the list, one `const`) |
| closures awaiting | `subscriptions` (L3) | `closures.summary(spaceId, at).closuresAwaitingExtension` | `closures.service.ts:200` | three small queries (built) |
| capacity set; present now; live status | `occupancy` (L4) | **+** `occupancy.glance(space: LoadedSpace): Promise<{ capacity; status; present: { visits; members; total } }>` | `now(space)` (`occupancy.service.ts:182`) reads people's names too; `presentIn` (299); `liveStatus` pure | `now`'s reads without the names: the state row, the open visits and check-ins **counted**, the closures now, the week; the pure `liveStatus` |
| customers owing | `payments` (L4) | D10 `balanceTotals(spaceId, at).owed.customers` | `customerIdsByPayment` (`payments.service.ts:333`) | `balancesOf` over the space (as the customers list's filter today) |
| ending soon | `subscriptions` (L3) | **+** `subscriptions.endingSoon(spaceId, at, take = 5): Promise<{ total; first: … }>` | `customerIdsBy({ status: 'ENDING_SOON' })` (`subscriptions.service.ts:283`) over `statesOf` | `statesIn` over the space (`subscription_usage`), each customer's current subscription by the one rule (`subscriptionStatus`); the first five by `endsOn`, then id; names by `customers.namesOf` (EC8: equal to the customers list's `status=ENDING_SOON` total) |
| announcements running | `announcements` (L2), through `closures.summary`'s `running` + **+** `announcements.runningTypes(spaceId, at): Promise<AnnouncementType[]>` | `counts` (`announcements.repository.ts:139–154`) | `SELECT DISTINCT type … WHERE space_id AND deleted_at IS NULL AND starts_at <= now AND (ends_at IS NULL OR ends_at > now)` on `(space_id)` |
| spaces by status | `space-links` (L2) | **+** `adminSpaces.counts(): Promise<{ verified; unverified; hidden; staleOrMissing }>` | `adminSpaces.list` (`adminSpaces.service.ts:42`) through `listingQueryOf` (`listingQuery.ts:20–37`) and `listing.page` (`listing.service.ts:71`) | `verifiedSpaceIds` once, then four `listing.count(query)` (**+** `ListingService.count`, the `findPage` `where` without the page) in parallel; the spaces table is small (no index needed) |
| unverified, no owner | `space-links` | in `counts()`: = `unverified` (OD2) | — | — |
| completeness | `space-links` (L2) | **+** `adminSpaces.staleEditable(take = 5): Promise<{ total; first: … }>` | none (§4.2) | `listing.page({ ids: { notIn: verifiedIds }, staleOnly: true }, { page: 1, limit: 5 })` — hidden included, deleted out; its rows' `staleGroups`/`missingGroups` (+ `days`, D16) and `photoCount > 0` (EC9) |
| open reports split | `data-reports` (L3) | **+** `dataReports.openCounts(): Promise<{ open; awaitingAdmin; awaitingOwners }>` | `all` (`data-reports.service.ts:195`) | `verifiedSpaceIds` (through `space-links`, as `asAdminReports` does), then `count(*) FILTER (WHERE space_id = ANY(verified))` over `status = 'OPEN'` of live spaces, on `(status)` |
| new users | `users` (L1) | **+** `users.countCreatedSince(since: Date)` | none (`users.page`'s filter has no date, `users.service.ts:463`) | `count(*) WHERE created_at >= since` — no index (R13): a seq scan of `users` (≈ thousands: fine; EC10 measures) |

**D21 — `OverviewService`** (`overview/overview.service.ts`; one file per screen as the conventions say:
`overview/ownerOverview.ts`, `overview/adminOverview.ts`, the service joining them; deps `{ spaces, dataReports, visits,
subscriptions (with closures), announcements, payments, occupancy, spaceLinks (adminSpaces), users, now }`)
- `owner(space: LoadedSpace)`: `const at = now()`; **one `Promise.all`** of the ten calls of D20's owner rows; then the
  answer assembled field by field (no arithmetic beyond picking fields; `agorot` dropped). `since` none.
- `admin()`: `const at = now(); const since = lastDaysSince(at, 30)` = `gazaInstant(addDays(gazaClockOf(at).date,
  -29), 0)` — **the same rule as the audit's `LAST_30_DAYS`** (`audit/auditPeriod.ts`, #128). `overview` cannot import
  `audit` (both L5), so the rule moves to `@masaha/shared/core` as `lastDaysSince(now, days)` (S23), which
  `audit/auditPeriod.ts` then calls (no behaviour change; its unit test unchanged and green).
  One `Promise.all`: `adminSpaces.counts()`, `adminSpaces.staleEditable(5)`, `dataReports.openCounts()`,
  `users.countCreatedSince(since)`.
- `overview.manage.routes.ts`: `GET /` → `requireCan('space.overview.read')` → controller. `overview.admin.routes.ts`:
  `GET /` → controller. No query, so no `validate`.

**D22 — `can()`:** `'space.overview.read': 'owner'` beside `finance.read` (`can.ts`, the owner's own block), its unit
test `OWNER_ONLY`. *Why a new action, not `finance.read`:* the owner's overview is not finance (O3); a later change of
who reads it (a reception overview, OV3 undone) touches one line. The admin's route stays on `/admin`'s role guard as
every admin route (`platform.stats.read` stays unused; OD4 offers its removal or use).

**D23 — locks and snapshots** (D14's style)
- **Reads take no lock.** The income report, and the debts' page with its totals, read one `REPEATABLE READ` snapshot
  (S3). The audit-style lists (payers' page and its count) are read apart, as every list.
- **Neither overview reads a snapshot** (S21): each figure is a count standing alone, each equals its list at the same
  instant only to within a write between two statements, as two separate reads would; a snapshot would serialise the
  ten reads on one connection (Prisma runs a transaction's queries one after another), costing the parallelism OV7
  asks for.
- **No write anywhere** in part one or two (R7); the left items' writes: `PATCH /me` (one row, the user's own,
  audited — the action per EC12) and finding 170's session renewal (unchanged lock order: the session row only).

| Race | What decides | Test |
|---|---|---|
| A payment recorded during the income report | the snapshot: the month equals its bar | Not tested (no lock to wait on), said |
| A payment recorded between the debts' page and its totals | the snapshot | T-F10 (agreement), the race not tested, said |
| A request's renewal racing a rotation (170) | the newest row reads the family's max | T-L5 (`whileHeld` on the old row) |

**D24 — bounds and cost** (ADR 0014: 4.5 MB)

| Answer | Bound | Reads on one space's year (≈ 10 k payments, 9 k visits, 3 k check-ins, 500 subscriptions, 2 k customers) |
|---|---|---|
| `IncomeReport` | 12 + 30 + the staff (≤ tens) | 45 index range scans of `payments (space_id, received_at)` in one statement; one `GROUP BY` of the month |
| `BalanceRow[]` | a page (≤ 50); totals | `balancesOf` over the space, twice (page, totals) + the uncollected count |
| `Payer[]` | a page | one month's payments joined to their items by primary key |
| `OccupancyReport` | 14 + 168 cells | a month's stays (≈ 1 k) against ≤ 744 slots, and 28 days against 672 slots |
| `OwnerOverview` | ≈ 1 KB | ten small reads; the heaviest `balancesOf` (as the customers list's filter) and `statesIn` (500 subscriptions) |
| `AdminOverview` | ≈ 2 KB | `verifiedSpaceIds` (twice: S22), four counts and one page of `spaces`, two counts of `data_reports`, one of `users` |

**No new index** (Q5); EC4 measures every statement on a generated year; one over 150 ms is **recorded, not
indexed**, and the owner decides at the review.

### 5.5 The left items (each if in)

**D30 — F1–F4 and 153** (copied from #130's review)
- **F1** (should-fix): *where* `settingKeys.ts:24–30` (the read regex), `platform-settings.service.ts:103–121` (the save
  compares the normalised body with the stored form); no test stores a contact in another form. *Scenario 1:* someone
  tightens `contactWhatsapp`'s read to the phone rule; a database seeded with `+97259…` answers `GET /settings/public`
  with a 500 on About, and every test stays green. *Scenario 2:* the admin's `GET …/contact` answers `+97259…`; a `PUT`
  of the same body writes `+97059…` and audits `before {whatsapp:'+97259…'}` / `after {whatsapp:'+97059…'}` — right
  behaviour, unpinned and unwritten. *Fix:* **T-L1** — stored `'+972591234567'` and `'Hello@Masaha.PS'` → `GET
  /settings/public` and `GET /admin/settings/contact` 200, answered as stored; **T-L2** — the `PUT` of those values →
  stored `+970591234567` / `hello@masaha.ps`, one `contactEdited` with exactly those `before`/`after`. The contract's
  contact bullet gains: "A value stored in another form (a seed's) is answered as stored, and the next save stores its
  one form, audited."
- **F2:** finding 153's *Evidence* says "a change of form the admin did not ask for" (not "a change no one made"), and
  adds the case `SEED_CONTACT_WHATSAPP=+201001234567`: read and answered, but a `PUT` of the card changing only the
  email is 422 on `whatsapp`. Then 153 is **resolved** by D31.
- **F3:** `platform-settings.md:29` drops "in the browser too" (no web schema import exists; screen 32 will make it
  true and may say so).
- **F4:** the contract's *A save* bullet and `platform-settings.md` (*What it does*, line 11; decision line 51): "a save
  that changes no value writes no value and no entry" (an unset contact's first save may insert its rows as JSON
  `null`, which reads as unset).

**D31 — finding 153's fix:** `seed/run.ts` reads `SEED_CONTACT_EMAIL` and `SEED_CONTACT_WHATSAPP` through
`emailSchema` and `phoneSchema` (`@masaha/shared/core`), so the seed stores the normalised form, and a foreign number
fails the seed's environment check with its variable named (as every other seed variable). T-L3 in the seed's lane
(EC7: `seed.api.test.ts`'s shape). 153 → *Resolved*, *Resolution* "2026-10-29, #PRNUM".

**D32 — finding 170** (if in): `sessions.repository.ts` `familyActivity` answers `max(last_activity_at)` over the
family (`aggregate`), and `sessions.service.ts` `rotate` copies that maximum into the new row (line 92's `family?.lastActivityAt`
already reads it — the source changes). T-L5: `whileHeld` on the old row (a refresh's transaction), a request's
renewal waits and commits on the old row; then the idle check at the new row sees the renewal → not idle. B-L5:
`familyActivity` back to the newest row.

**D33 — `/me`** (if in; OD6): `GET /me` → `MyAccount = { id, name, email, language: 'ar' | 'en', role }` (the fields
`users.signedInAccount` already reads — EC12); `PATCH /me` `updateMeSchema = { name?: nameSchema, language?:
z.enum(LANGUAGES) }`, at least one (`required`), one row updated, audited `user.profileEdited` with only what changed
(a no-change `PATCH` writes nothing). `can()`'s `profile.update` (`self`) exists. `user.profileEdited` names no
space, so it would reach the admin's log only if added to `PLATFORM_ACCOUNT_ACTIONS`; it is **not** added (a user's
own name is no platform event), and the default deny keeps it off — stated.

**D34 — `GET …/visits`** (if in; OD7): `visitsQuerySchema = paginationQuerySchema.extend({ from?, to? })` Gaza dates,
the range by the payments list's rule (`paymentsWindow`, both or neither, ≤ the payments list's bound — EC13), today
without one; the owner every day in range, **reception today only** (a range from reception `forbidden`, as the
payments list — `payments.readOwn` style; OD7 confirms); the space's visits checked in within the window, open and
closed, newest first, then id, answered as `DeskVisit` (`visits.deskVisitsOf`); on `(space_id, checked_in_at)`.
Finding 161 resolved.

**D35 — finding 167** (if #129 merged and in): `adminReportsQuerySchema` gains `handledBy: z.enum(['ADMIN',
'OWNER']).optional()`; `data-reports` resolves it to `spaceId IN / NOT IN verifiedSpaceIds` (the same split as D20's
`openCounts` — one helper `handledByWhere(verifiedIds, handledBy)` both use).

### 5.6 Stronger decisions (S…)

- **S1 — every finance bucket a window computed in Node** (finance S2, kept): months, days and hours are instants
  from `gazaInstant`/`gazaClockOf`, passed as arrays; no `AT TIME ZONE` in finance. *Why:* one zone source (finding
  120); the indexes serve each window (finding 127's cost avoided). *Undo:* SQL `AT TIME ZONE` buckets.
- **S2 — the income and the debts read one snapshot** (finance S3): `readSnapshot` around each. *Why:* the month's
  total must equal its bar, and the page's rows its totals (finding 124). *Undo:* drop the wrapper.
- **S3 — the aggregates in `payments`, not `finance`**: *why:* "voided left out" and the balance rule keep one home,
  and the overview may reuse them (it may not import `finance`). *Undo:* A2.
- **S20 — `overview` has no repository**: every figure through its owner's service. *Why:* OV7 "no logic"; R7 would
  allow aggregate reads, but a second count of a rule (uncollected, ending soon) would drift. *Undo:* a repository
  for the admin's counts (A11).
- **S21 — no snapshot on the overviews** (D23). *Undo:* wrap in `readSnapshot`, losing the parallel reads.
- **S22 — each tile equals the list it links to**: the space counts reuse `listingQueryOf` and the listing's `where`;
  the overview's counts reuse each list's `where` (one `const` per rule). *Why:* a tile that says 7 and a list that
  shows 6 is a defect the owner sees at once. *Undo:* none needed.
- **S23 — OV5's window shared with the audit's** (`lastDaysSince` in `core`): the same Gaza-midnight rule in one
  place. *Undo:* a copy in `overview`.
- **S24 — the unpriced visits counted beside the uncollected** (OPEN_DECISIONS point 1, #97). *Undo:* drop the field.
- **S25 — stale days answered** (`days` per stale group): the prototype shows «قبل {n} يوم» / «{group} · {n} يومًا»;
  computed in `spaces`. *Undo:* groups only.
- **S26 — `space.overview.read`** (D22). *Undo:* `finance.read`.

### 5.7 Proposed alternatives (argued, not applied)
- **A1 — one finance route** (every tab in one request): one request on a weak line, but the debts and payers pages
  ride with it and every tab pays for the others. *Not recommended.*
- **A2 — every finance aggregate in `finance`'s repository:** fewer cross-module functions; two homes for the voided
  and balance rules, and the overview could not reuse them. *Not recommended.*
- **A10 — the overview reads a snapshot** (S21 undone): figures agree exactly; but ten reads run in series on one
  connection, so the server's time is the sum of ten reads instead of the slowest one. *Not recommended.*
- **A11 — the admin's counts in one SQL statement in `overview`** (R7 allows it): one round trip instead of ≈ 8; but the
  "verified" and "stale" rules would be written a second time. *Not recommended.*
- **A12 — the owner's overview without the ending-soon names** (OV1 read literally: "each item a count and a link"):
  smaller answer, no customer names on a desk-visible screen; the prototype lists five with «تجديد». See OD1.
- **A13 — a short server cache of `AdminOverview`** (60 s): the admin reloads often; the counts are cheap (D24) and a
  cache would show a hidden space as still unhidden. *Not recommended.*
- **A9 — one later "API findings sweep" item** for L16's small fixes (69, 77, 78, 79, 93, 120, 121, 126, 127), outside
  this PR. *Recommended* as a follow-up, the owner's call.

---

## 6. Related findings

| Finding | Folded? | How |
|---|---|---|
| 153 | **Yes** — resolved (D31), wording fixed first (F2) | C2 |
| 97 | **Yes** — moved to *Resolved* (code by #130) | C3 |
| 170 | **If OD5** — resolved (D32) | C13 |
| 161 | **If OD7** — resolved (D34) | C15 |
| 167 | **If #129 merged and OD8** — resolved (D35) | C14 |
| 152 | No — OD9 asks when the retention rule is decided | — |
| 124 | No (resolved) — its snapshot pattern reused (S2) | — |
| 120, 127 | No — finance avoids them (S1) | — |
| 79 | No — `namesFor` called outside the snapshots, as today | — |
| 14 | No — the owner's audit screen is worker A's | — |
| 98 | No — two new capability documents follow the template's size | — |
| 171, 187, and L14–L16 | No — §4.3 | — |
| **New** | none planned; any recorded takes 154, 155, … | — |

---

## 7. The files (A = added, M = modified)

**Unit U0 — carried review fixes** (C1–C3)
- M `apps/api/src/modules/platform-settings/publicContact.api.test.ts` (T-L1), M `adminSettings.api.test.ts` (T-L2)
- M `apps/api/src/db/seed/run.ts` (D31), M `apps/api/src/db/seed/seed.api.test.ts` (T-L3; EC7)
- M `docs/api/api-contract.md` (F1 sentence, F4), M `docs/features/platform-settings.md` (F3, F4)
- M `docs/architecture/findings/153-…md` (F2, then *Resolved*), M `97-…md` (*Resolved*), M `findings/README.md`

**Unit U1 — the ledger's balance aggregates** (C4)
- M `apps/api/src/modules/payments/payments.repository.ts` (`balancesPage`, `balanceTotals`, `uncollectedTotals`, the
  uncollected `const`), M `payments.service.ts` (the three, `at` → `calendarOf`)
- A `apps/api/src/modules/payments/totals.api.test.ts` (T-P1–T-P3)
- M `docs/features/payments.md`, M `docs/backend/conventions.md` (§9 *Composed reads*, R11)

**Unit U2 — finance** (C5–C7)
- M `packages/shared/src/core/gazaTime.ts`, M `gazaTime.unit.test.ts` (`monthOf`, `addMonths`)
- A `packages/shared/src/finance/{requests,responses,index}.ts`, A `finance/requests.unit.test.ts`
- M `payments.repository.ts`, M `payments.service.ts` (`incomeIn`, `firstReceivedAt`, `collectionsIn`)
- M `apps/api/src/modules/customers/customers.{repository,service}.ts` (`contactsOf` + `archived`)
- A `apps/api/src/modules/finance/{index,finance.service,finance.repository,finance.controller,finance.manage.routes,finance.mapper,windows,occupancyGrid}.ts`
- A `finance/{windows,occupancyGrid}.unit.test.ts`; A `finance/{access,income,debts,payers,occupancy}.api.test.ts`
- M `apps/api/src/app.ts` (`finance` built with `createReadSnapshot()`; `manage.use('/finance', …)`)
- Docs: contract *Finance*; data model *Derived values*; conventions header, §7, §9; security *Authorization*; A
  `docs/features/finance.md`; `payments.md`

**Unit U3 — the owners' functions for the overviews** (C8, C10)
- M `apps/api/src/modules/spaces/staleness.ts` (+ `staleDays`), M its unit test; M the `spaces` service file that holds
  a one-space read (EC5) (+ `freshnessOf`)
- M `apps/api/src/modules/spaces/listing/{listing.service,listing.repository}.ts` (+ `count`)
- M `apps/api/src/modules/data-reports/{data-reports.service,data-reports.repository}.ts` (+ `openCountOf`, `openCounts`)
- M `apps/api/src/modules/visits/{visits.service,visits.repository}.ts` (+ `unpricedCount`)
- M `apps/api/src/modules/subscriptions/subscriptions.service.ts` (+ `endingSoon`)
- M `apps/api/src/modules/announcements/{announcements.service,announcements.repository}.ts` (+ `runningTypes`)
- M `apps/api/src/modules/occupancy/occupancy.service.ts` (+ `glance`)
- M `apps/api/src/modules/space-links/admin-spaces/adminSpaces.service.ts` (+ `counts`, `staleEditable`)
- M `apps/api/src/modules/users/{users.service,users.repository}.ts` (+ `countCreatedSince`)
- M `packages/shared/src/core/gazaTime.ts` (+ `lastDaysSince`), M `apps/api/src/modules/audit/auditPeriod.ts` (calls it)
- M `apps/api/src/app.ts` (the listing service kept in a variable, `app.ts:345`, so `adminSpaces` and nothing else
  change; EC11)

**Unit U4 — the overviews** (C9, C11)
- A `packages/shared/src/overview/{responses,index}.ts`
- A `apps/api/src/modules/overview/{index,overview.service,ownerOverview,adminOverview,overview.controller,overview.manage.routes,overview.admin.routes}.ts`
- A `overview/{ownerOverview,adminOverview}.api.test.ts`
- M `apps/api/src/shared/auth/can.ts`, M `can.unit.test.ts` (`space.overview.read`)
- M `apps/api/src/app.ts` (the service; the two mounts)
- Docs: contract *Overview* (new section); conventions header, §7 table row, §9 *`overview`*; security; A
  `docs/features/overview.md`; foundation §13 line 459 (OV8); `v1-mvp.md` step 12 *Built*, `/admin/stats` row (OD4)

**Unit U5 — left items** (C12–C15, each if in): `sessions.{repository,service}.ts` + `sessions` race test; `users`
routes/service/repository + `packages/shared/src/users/requests.ts` + `me.api.test.ts`; `visits` routes/service/
repository + `packages/shared/src/visits/requests.ts` + `visitsList.api.test.ts`; `data-reports` + shared
`data-reports/requests.ts` + its admin test; their contract sections, feature documents and findings.

**Unit U6 — closing documents** (C16): `docs/plans/v1-mvp.md` (finance row, step 11 and 12 *Built*, the `/me`,
`visits` and `/admin/stats` rows); `docs/project/overview.md` (*Built*: Finance, Overview); `docs/README.md` (the map's
`finance.md`, `overview.md`); `docs/architecture/findings/README.md` (the index moves).

---

## 8. Units, commits and lanes

### 8.1 The commits (subject ≤ 50; each with its tests and documents)

| # | Unit | Subject | Chars | Holds |
|---|---|---|---|---|
| C1 | U0 | `test(platform-settings): pin a stored contact form` | 49 | F1: T-L1, T-L2, the contract sentence; F3; F4 (contract, `platform-settings.md`) |
| C2 | U0 | `fix(seed): store the contact in its one form` | 43 | F2's two lines; D31; T-L3; finding 153 *Resolved* + index |
| C3 | U0 | `docs: resolve finding 97` | 24 | 97 *Resolved* (#130), index |
| C4 | U1 | `feat(payments): total a space's balances` | 40 | `balancesPage`, `balanceTotals`, `uncollectedTotals`; T-P1–T-P3; `payments.md`; conventions §9 (R11) |
| C5 | U2 | `feat(finance): read a space's income` | 36 | `monthOf`, `addMonths`; shared `finance`; `windows.ts`; `incomeIn`, `firstReceivedAt`, `collectionsIn`; the module, its income route; U-F1, U-F2, U-F4, T-F1 (income), T-F2–T-F6; contract *Finance* (income); data model (*Income*, *Collections*); conventions header, §7; security; `finance.md` (first) |
| C6 | U2 | `feat(finance): read who owes and who paid` | 41 | `contactsOf`'s `archived`; the debts and payers routes; T-F1 (both), T-F7–T-F11; contract; `finance.md` |
| C7 | U2 | `feat(finance): read a space's occupancy` | 39 | `occupancyGrid.ts`, the occupancy reads and route; U-F3, T-F1 (occupancy), T-F12–T-F14; contract; data model (*Occupancy statistics*); `finance.md` |
| C8 | U3 | `feat(api): count what the owner's overview shows` | 48 | `freshnessOf` + `staleDays`, `openCountOf`, `unpricedCount`, `endingSoon`, `runningTypes`, `glance`; U-O1; T-M1–T-M6; the feature documents' *Behaviour* lines (`spaces`, `data-reports`, `visits`, `subscriptions`, `announcements`, `occupancy`) |
| C9 | U4 | `feat(overview): read the owner's overview` | 41 | shared `overview` (owner part); the module, its manage route; `space.overview.read`; T-O1–T-O6; contract *Overview* (owner); conventions §9 *`overview`*; security; `overview.md` (first); foundation §13 line 459 (OV8) |
| C10 | U3 | `feat(api): count what the admin's overview shows` | 48 | `ListingService.count`, `adminSpaces.counts`, `staleEditable`, `openCounts`, `countCreatedSince`, `lastDaysSince` (+ `auditPeriod.ts`); U-O2; T-M7–T-M10; `space-links.md`, `data-reports.md`, `users.md` lines |
| C11 | U4 | `feat(overview): read the admin's overview` | 41 | shared `overview` (admin part); the admin route; T-O7–T-O11; contract; `overview.md` |
| C12 | U5 | `fix(sessions): read a family's latest activity` | 47 | D32 (if OD5); T-L5; finding 170 *Resolved* |
| C13 | U5 | `feat(users): read and edit one's own account` | 44 | D33 (if OD6); T-L6–T-L8; contract *Me*; `users.md` |
| C14 | U5 | `feat(data-reports): filter by who handles them` | 46 | D35 (if #129 merged, OD8); T-L9; finding 167 *Resolved* |
| C15 | U5 | `feat(visits): list a space's visits by day` | 42 | D34 (if OD7); T-L10–T-L12; contract; `visits.md`; finding 161 *Resolved* |
| C16 | U6 | `docs: record the API of v1 as built` | 35 | v1-mvp (rows, steps 11–12 *Built*), `overview.md` *Built*, `docs/README.md` map, the findings index's final moves |

(C12–C15 renumber if an OD drops one; C16 stays last.)

### 8.2 Dependencies

```
C1 → C2 → C3                        (U0; one lane, first — the owner's rule: review fixes open the PR)
C4                                  (U1; needs nothing; FIRST — both U2 and U4 read it)
C5 → C6 → C7                        (U2; needs C4)
C8 → C9                             (U3 owner part, then U4 owner part; C9 needs C4 and C8)
C10 → C11                           (U3 admin part, then U4 admin part; needs C9 only for the shared `overview` folder and app.ts)
C12, C13, C14, C15                  (U5; independent of everything above and of each other)
C16                                 (last; needs every other)
```
- **Must come first:** C4 (the aggregates both parts read), and the shared folders' first files (C5 creates
  `packages/shared/src/finance`, C9 `…/overview`).
- **Can run in parallel after C4:** lane F (C5–C7), lane O (C8–C11), lane L (C12–C15).

### 8.3 Shared files and how lanes add to them without colliding
| File | Lanes | Rule |
|---|---|---|
| `apps/api/src/app.ts` | F, O, L | each lane adds **only** its own block: F the `finance` construction after `payments` and one `manage.use('/finance', …)` line; O the `overview` construction after `auditLog` and two mount lines; L none (existing routers). The lead joins in the order F, O. |
| `packages/shared/src/core/gazaTime.ts` (+ unit) | F (`monthOf`, `addMonths`), O (`lastDaysSince`) | append at the file's end, F's first; O rebases its append |
| `payments.repository.ts`, `payments.service.ts` | U1 (C4), F (C5) | C4 lands before F starts; F appends below C4's functions |
| `apps/api/src/shared/auth/can.ts` | O | O only |
| `docs/api/api-contract.md` | all | each lane writes **its own new section** (F: *Finance* after *Front desk (managed)*; O: one *Overview* section after *Audit log*, both routes; L: in *Me*, *Front desk*, *Data reports*); U0's two sentences are C1's |
| `docs/backend/conventions.md` | U1, F, O | header *Built* line: **written once by C16** from the lanes' notes; §7 table: F the `finance` row, O the `overview` row; §9: U1 the *Composed reads* bullet, O the *`overview`* section |
| `docs/architecture/data-model.md` | F | F only |
| `docs/backend/security.md` | F, O | each its own bullet under *Authorization* |
| `docs/plans/v1-mvp.md`, `docs/project/overview.md`, `docs/README.md` | — | **C16 only** (the lead), so no lane touches them |
| `docs/architecture/findings/README.md` | U0, L | U0's moves in C2–C3; L's in each of its commits; C16 checks |
| feature documents | each its owner | `payments.md`: C4 then C5/C6 (lane F after C4); every other: one lane |

### 8.4 Lanes proposed — **3 lanes + the lead** (the execution prompt decides)
1. **The lead:** C1–C4 first (≈ the first hour), then opens the lanes; joins F and O into the branch, runs C16, the
   whole verification, the real run, the PR.
2. **Lane F** (finance): C5–C7.
3. **Lane O** (overviews): C8–C11.
4. **Lane L** (left items): C12–C15, each only if its OD says in; may start before C4 (no dependency).
Join order: L's commits first if done (independent), then F, then O (O's `app.ts` block placed after F's).

---

## 9. Tests

Every test seen failing first in its own lane; expectations written by hand; a fixed clock through
`createTestApp({ clock })`; instants with their offset; Gaza dates as strings. Roles in each API file (testing §4): the
**owner**, **reception**, a **stranger** (signed in, no link), **another space's owner**, the **admin**; anonymous where
public. Each `B…` is a deliberate break: back up, make the one edit, run the named file, record the red, restore from
the backup, green again.

### 9.1 U0
- **T-L1** `publicContact.api.test.ts`: `a contact stored in another form is answered as stored` (`'+972591234567'`,
  `'Hello@Masaha.PS'`) — **B-L1**: the read through `phoneSchema` (500).
- **T-L2** `adminSettings.api.test.ts`: `saving a contact stored in another form stores its one form, audited from the
  stored to the saved` — **B-L2**: the comparison on normalised forms (no write, no entry).
- **T-L3** `seed.api.test.ts`: `the seed stores the contact normalised; a foreign WhatsApp fails the seed naming its
  variable` — **B-L3**: `run.ts` back to the E.164 regex.

### 9.2 U1 (`payments/totals.api.test.ts`)
- **T-P1** `the balances' page: largest debt first, paged, the total right; the oldest owing item of each` — **B-P1**:
  ordered by customer id.
- **T-P2** `the totals: owed and credit, customers and agorot; an archived customer's debt kept; a credit never offsets
  another item's debt` — **B-P2**: `sum(due − paid)` netted per customer.
- **T-P3** `the uncollected totals count the desk's list, its unpriced apart` (equal to `GET …/uncollected-visits`'
  total) — **B-P3**: `written_off_at IS NULL` dropped from the fragment.

### 9.3 U2 — finance (copied, re-verified)
**Unit**
- **U-F1** `packages/shared core/gazaTime.unit.test.ts`: `monthOf and addMonths across a year, back and ahead` —
  **B-F1**: `addMonths` off by one in December.
- **U-F2** `finance/windows.unit.test.ts`: `a month from its Gaza midnight to the next; 23 months back the earliest,
  the next month out of range; the 12 months and the 30 and 14 days ending today; the 28 days before today; hours
  labelled by Gaza weekday and hour across a daylight-saving night` — **B-F2**: windows from UTC midnights; **B-F3**:
  the 28 days ending today.
- **U-F3** `finance/occupancyGrid.unit.test.ts`: `the average per weekday and hour over 4 weeks, one decimal; the peak
  hour, ties the earliest, none without stays; the daily attendance over the days with any` — **B-F4**: ÷ 7; **B-F5**:
  attendance over every day of the month.
- **U-F4** `packages/shared finance/requests.unit.test.ts`: `a month YYYY-MM; a state OWES or CREDIT, OWES by default`.

**API**
- **T-F1** `finance/access.api.test.ts`: `reception is 403 on the four routes before the query is read (an invalid
  month still 403); a stranger, another space's owner and the admin not_found` — **B-F6**: `requireCan` removed from
  `income`; **B-F7**: from `debts` (the phones); **B-F7a**: the router mounted outside `manage`.
- **T-F2** `income.api.test.ts`: `the month's income by subscriptions and visits, the month before, today and all time
  with its first day: voided payments left out; a written-off visit's payment counted as received` — **B-F8**:
  `voided_at IS NULL` dropped.
- **T-F3** `the 12 months and the visits' 30 days by Gaza day: a payment at 23:30 on a month's last day counts in that
  month and that day` (23:30 Gaza = 21:30 UTC in winter, 20:30 in summer) — **B-F9**: windows by UTC days.
- **T-F4** `each staff member's collections for the month by method, named, an ex-reception's included` — **B-F10**:
  the method split from all payments.
- **T-F5** `another space's payments never counted` — **B-F11**: the space filter dropped from `incomeIn`.
- **T-F6** `a month ahead, or 24 months back, is 422 out_of_range on month; 23 back answers` — **B-F12**: `monthError`
  skipped.
- **T-F7** `debts.api.test.ts`: `who owes, largest first, paged, the total right: the phone, an archived customer kept
  and marked, the oldest item still owing and its day` — (B-P1 covers the order) **B-F13**: `archived` always false.
- **T-F8** `who is in credit, largest first` — **B-F14**: `state` ignored.
- **T-F9** `a written-off visit, a voided payment and an unpriced visit owe nothing; a walk-in's uncollected visit
  counts apart, its unpriced too` — (B-P3).
- **T-F10** `the totals agree with every page's rows, and the reminder template is the space's, null by default` —
  **B-F16**: the template not read.
- **T-F11** `payers.api.test.ts`: `the customers who paid in the month, the latest first, each with what they paid then;
  a walk-in's payment names no one; a voided payment leaves its customer out` — **B-F17**: voided counted.
- **T-F12** `occupancy.api.test.ts`: `visits and members per day over the 14 days: closed stays only, a member twice in
  a day once` — **B-F18**: open stays counted; **B-F19**: members per check-in.
- **T-F13** `the average present per hour over the 28 days before today, by Gaza weekday and hour; an auto-closed stay
  counted; today's left out` — **B-F20**: overlap by the check-in's hour only.
- **T-F14** `the month's average stay, members and visits apart, its peak hour and daily attendance; none: nulls` —
  **B-F21**: the average stay over visits only.

### 9.4 U3 — the owners' functions (each in its module's existing API test file, or a new one, EC14)
- **U-O1** `spaces/staleness.unit.test.ts` (gaining): `a stale group's days are Gaza days since its date` — **B-O1**: UTC days.
- **T-M1** `spaces`: `freshnessOf: missing and stale by the saved thresholds; a threshold saved applies at once` —
  **B-M1**: the thresholds a constant (60/30) — OV6.
- **T-M2** `data-reports`: `openCountOf counts the space's OPEN reports only` — **B-M2**: the status filter dropped.
- **T-M3** `visits`: `unpricedCount equals the unpriced list's total` — **B-M3**: `checked_out_at` condition dropped.
- **T-M4** `subscriptions`: `endingSoon counts the customers whose current subscription is ending soon, equal to the
  customers list's status=ENDING_SOON total; the first five by end date` — **B-M4**: every subscription counted (not
  the current one).
- **T-M5** `announcements`: `runningTypes: each running type once; an ended, upcoming or deleted one never` — **B-M5**:
  `deleted_at IS NULL` dropped.
- **T-M6** `occupancy`: `glance answers the present visits and members, the capacity and the status, no names` —
  **B-M6**: members counted from visits.
- **U-O2** `core/gazaTime.unit.test.ts`: `lastDaysSince: the Gaza midnight 29 days before today, across a
  daylight-saving change` (and `auditPeriod.unit.test.ts` stays green unchanged) — **B-O2**: `now − 30 × 24 h`.
- **T-M7** `space-links` admin spaces: `counts equal the list's totals for verified, unverified, hidden and stale; a
  deleted space never counted` — **B-M7**: `isHidden: false` dropped from `unverified`.
- **T-M8** `staleEditable: unverified spaces, hidden included, with a group stale or missing; the verified never; the
  first five by name, and the total` — **B-M8**: the verified ids not excluded.
- **T-M9** `data-reports`: `openCounts splits the open reports by who handles them; a deleted space's left out` —
  **B-M9**: `space.deletedAt` filter dropped.
- **T-M10** `users`: `countCreatedSince counts the accounts created from that instant` — **B-M10**: `gt` for `gte`
  (an account created at the instant missed).

### 9.5 U4 — the overviews
**`overview/ownerOverview.api.test.ts`**
- **T-O1** `the owner reads the work queue: groups missing and stale with their days, open reports, uncollected and
  unpriced visits, closures awaiting, capacity unset, customers owing` (each fixture made through the factories; hand
  counts) — **B-O3**: `customersOwing` from `customerIdsByPayment` on unarchived only (an archived debtor missed).
- **T-O2** `each count equals the list it links to` (the same app: `GET …/uncollected-visits`, `…/unpriced-visits`,
  `…/data-reports?status=OPEN`, `…/announcements?state=RUNNING`, `…/customers?status=ENDING_SOON`, `…/finance/debts`)
  — breaks B-M2–B-M5 each turn it red too.
- **T-O3** `no amount anywhere: the body holds no Agorot key` (the body serialised and searched) — **B-O4**: the answer
  passes `balanceTotals` whole.
- **T-O4** `present now: visits, members, capacity and the live status; full at capacity` — **B-O5**: `status` from the
  override ignored (`glance` without the override).
- **T-O5** `the ending-soon first five and the running announcements' types` — **B-O6**: the first five unsorted.
- **T-O6** `reception is 403; a stranger, another space's owner and the admin not_found` — **B-O7**: `requireCan`
  removed; **B-O8**: the router mounted outside `manage`.

**`overview/adminOverview.api.test.ts`**
- **T-O7** `the admin reads the tiles: verified, unverified, hidden, no owner, stale or missing, open reports split,
  new users of the last 30 Gaza days` — **B-O9**: `since` = `now − 30 days` (an account at 00:30 Gaza 29 days back
  missed).
- **T-O8** `the tiles equal the admin's lists` (`GET /admin/spaces?status=…`, `?stale=true`, `GET /admin/data-reports`)
  — B-M7 turns it red.
- **T-O9** `completeness: the first five unverified spaces with a group stale or missing, hidden ones included, each
  with its groups and days; the total` — B-M8.
- **T-O10** `a saved threshold changes both overviews at once` (`PUT /admin/settings/staleness`) — B-M1.
- **T-O11** `a guest is 401, a user and an owner 403, an admin with a pending password 403 PASSWORD_CHANGE_REQUIRED;
  nothing of a space's operations in the body` (`REFUSED_CALLERS`; the body searched for `present`, `customer`,
  `capacity`) — **B-O10**: the router mounted outside `/admin`.

### 9.6 U5 (each if in)
- **T-L5** `sessions` race: `a request's renewal racing a rotation leaves the new session active` — **B-L5** (D32).
- **T-L6** `me.api.test.ts`: `a user reads their own account` — **B-L6**: another user's id read from a query.
- **T-L7** `a user edits their name and language; only what changed is audited; no change writes nothing` — **B-L7**:
  the no-change branch removed.
- **T-L8** `a guest is 401; a suspended account 403` (the guard's own) — **B-L8**: `requireAuth` removed.
- **T-L9** `data-reports` admin: `handledBy=ADMIN keeps the unverified spaces' reports, OWNER the verified's` —
  **B-L9**: the two branches swapped.
- **T-L10** `visitsList.api.test.ts`: `the owner reads the visits checked in on a range of Gaza days, open and closed,
  newest first, paged` — **B-L10**: the range by UTC days.
- **T-L11** `reception reads today's only; a range from reception is forbidden` — **B-L11**: the range check removed.
- **T-L12** `another space's visits never; a stranger and the admin not_found` — **B-L12**: the space filter dropped.

### 9.7 Not tested, and said
- The snapshot's agreement under a concurrent payment (D23): no lock to wait on; `readSnapshot`'s own test is #118's.
- A real year's cost: measured (EC4), not tested.
- The overviews' figures agreeing **at one instant** under concurrent writes: not promised (S21).

### 9.8 Review Focus — inputs no test exercises
- A payment received at exactly a window's edge (`received_at = to`): the next window.
- A month with daylight saving's change: 23 or 25 hourly slots that day; the average is per slot.
- `month` = the current month on its first day before 08:00: empty figures, never an error.
- A customer who owes on one subscription and holds credit on another: in both lists.
- The debts' CSV across pages while a payment lands: two pages from two snapshots.
- A space with no fact dates but the profile (`profileUpdatedAt` is never null): never «missing» for the profile.
- A space with 0 capacity set vs `null`: `capacitySet` is `capacity !== null`.
- An admin who is also a space's owner: impossible (`ACCOUNT_IS_ADMIN`), so no mixed overview.
- `endingSoon` for an hours pack with no end date (`endsOn: null`): ending soon by its hours left; sorted last.
- The admin's completeness when more than five tie on name: by `nameEn`, then id (the listing's order).

---

## 10. The real run (API on 3321, `masaha_b_dev`)

Start `npm run dev -w @masaha/api` in the background (log in `scripts\server.log`, deleted after); `curl.exe -s
http://localhost:3321/health` → `db: up`. Sign in as `demo-owner@example.com`, `demo-reception@example.com`,
`demo-directory-owner@example.com` and the seed's admin (passwords read from `apps/api/.env` into variables, never
printed). A self-judging script `scripts\realrun.mjs` (`PASS`/`FAIL` per case, `ALL PASS` last), **never keeping an
`/auth/` response's body**. A case the demo data cannot show → **not performed**, with why and its test; **never change
data through the app to get past it.**

| # | Case | Role | Expect | Writes |
|---|---|---|---|---|
| R1 | `GET …/finance/income`, `…/debts`, `…/payers`, `…/occupancy` | owner | 200 each | none |
| R2 | cross-check by SQL (`docker exec masaha-postgres-1 psql`, `masaha_b_dev`): the month's `income.totalAgorot` = `sum(amount_agorot)` not voided from the month's Gaza midnight; `meta.totals.owed.customers` = the count of customers with a debt **archived included** (R10: not `?payment=OWES`'s total); the 14 days' visits = closed visits by check-in day | — | equal | none |
| R3 | the four finance routes | reception | 403 | none |
| R4 | the four finance routes | admin, directory owner | 404 | none |
| R5 | `GET …/overview` | owner | 200; no `Agorot` key; each count equals its list read just after (uncollected, unpriced, reports, announcements running, ending soon) and `customersOwing` = R1's debts total | none |
| R6 | `GET …/overview` | reception | 403 | none |
| R7 | `GET …/overview` | admin, directory owner | 404 | none |
| R8 | `GET /admin/overview` | admin | 200; the tiles equal `GET /admin/spaces?status=verified|unverified|hidden`, `?stale=true` totals and `GET /admin/data-reports?status=OPEN`'s total; `newUsers` = SQL count since the Gaza midnight 29 days back | none |
| R9 | `GET /admin/overview` | owner, reception | 403 | none |
| R10 | OV6 at once: `GET /admin/settings/staleness` (read A); `PUT` with `stalenessDays` = 1 → both overviews show more stale groups; **`PUT` A back** | admin, owner | changed, then as before | **two `platformSettings.stalenessEdited` entries** (named) |
| R11 | `GET /settings/public` | anonymous | the stored contact as stored (F1) | none |
| R12 | `/me` (if in): `GET`; `PATCH` the demo owner's `language` to the other, then back | owner | 200; restored | **two `user.profileEdited` entries** (named) |
| R13 | `GET …/visits?from=…&to=…` (if in) | owner; reception with a range | 200; 403 | none |
| R14 | the seed (153) | — | **not performed**: the dev database is seeded already; re-seeding is a database command outside the run (T-L3 proves it) | — |
| R15 | finding 170 | — | **not performed**: a race (T-L5 proves it) | — |

Stop the server by its process ids (the `tsx watch` child, the server, `pino-pretty`); `Get-NetTCPConnection
-LocalPort 3321` prints nothing.

---

## 11. Documents

Every new decision and history line ends with `2026-10-29, #PRNUM` (or the day it is written); *Last Updated* on each
document changed; one home per fact. New capability documents follow `docs/architecture/documentation.md` §5 (API
parts only; *Who uses it* names the web feature to come).

### 11.1 By unit (commit in brackets)
1. **`api-contract.md`** — *Platform settings*: F1's sentence, F4's wording [C1]; new section **Finance** after *Front
   desk (managed)*: the four routes, `month` and its bounds, the shapes, what each figure counts and leaves out
   (voided, written off, archived kept), the snapshot, the bounds [C5–C7]; new section **Overview** after *Audit log*:
   the two routes, the shapes, "no amount" (O3), each count = its list, no polling [C9, C11]; *Me* [C13]; *Front desk*
   the visits list [C15]; *Data reports* `handledBy` [C14].
2. **`data-model.md`** — *Derived values*: *Income* (windows, Gaza days), *Collections* (by method), *Occupancy
   statistics* (D11's definitions) [C5, C7].
3. **`conventions.md`** — §9 *Composed reads*: "`overview` (total owed)" → "`overview` (how many owe, a count — O3)"
   (R11), finance's debts through `payments`' balances [C4]; §7's `finance` row (*Holds*: the four reads) [C5]; §9
   *`overview`*: the figures' owners (D20), no repository, no snapshot, the admin's counts through `space-links`
   [C9, C11]; the header's *Built* [C16].
4. **`security.md`** — *Authorization*: finance's four routes `requireCan('finance.read')` [C5]; the owner's overview
   `space.overview.read`, the admin's behind `/admin` [C9, C11].
5. **Feature documents** — A `finance.md` [C5–C7]; A `overview.md` [C9, C11]; `payments.md` (the aggregates; *Who
   uses it*: finance, overview) [C4–C6]; `platform-settings.md` (F3, F4) [C1]; one *Behaviour* line each in
   `spaces.md`, `data-reports.md`, `visits.md`, `subscriptions.md`, `announcements.md`, `occupancy.md` [C8],
   `space-links.md`, `users.md` [C10]; `users.md` (`/me`) [C13]; `visits.md` (the list) [C15].
6. **Foundation §13 line 459** → `12. **Overview** (O) — needs attention (missing or stale groups, new reports,
   uncollected visits, a closure awaiting its extension, capacity not set, customers who owe — counts, no amounts,
   O3), present now / capacity and the live status, subscriptions ending this week, active announcements` [C9].
7. **Findings** — 153 (F2 + *Resolved*) [C2]; 97 *Resolved* [C3]; 170, 167, 161 *Resolved* if in [C12, C14, C15]; the
   index [each, checked in C16].
8. **`v1-mvp.md`** — the finance row: its four routes, "CSV export" → "no export route; the web builds the CSV"
   (decision 5); `/admin/stats` → `GET /admin/overview` (OD4); a `GET …/overview` row; `/me` and `…/visits` rows
   *built* if in; step 11 *Built* (finance) and step 12 *Built* [C16].
9. **`docs/project/overview.md`** — *Built*: a *Finance* line and an *Overview* line (API only) [C16].
10. **`docs/README.md`** — the map's `finance.md` and `overview.md` lines [C16]. *Deferred documents*: its one row is
    met per endpoint (L17).

### 11.2 `#PRNUM`
Written in the documents only; replaced per commit tree just before the push by the self-checking script (the model:
the workspace's `prnum` scripts), checked against the number `gh pr create` answers.

### 11.3 What the report writes in `_SHARED\OPEN_DECISIONS.md`
- Point 3: "the owner's debts with their phones are read on `GET …/finance/debts` (#n, date), the CSV built in the
  browser; no export route."
- Point 1: "«يحتاج انتباهك» counts the uncollected and the unpriced visits on `GET …/overview` (#n)."
- Point 2: "the owner's overview reads `closuresAwaitingExtension` (#n)."
- Point 4: "each staff member's collections are on `GET …/finance/income` (#n)."

---

## 12. Decisions needed from the owner

1. **OD1 — "the subscriptions ending this week":** (a) **the one rule `ENDING_SOON`** (≤ 7 days to the end, or ≤ 20 %
   left), each customer's current subscription — equal to `GET …/customers?status=ENDING_SOON`, the list the link
   opens; (b) the end date within the Gaza week (Saturday–Friday); (c) the end within 7 days only. And **with the first
   five names** (the prototype, «تجديد») or a count only (A12). *Recommended:* (a), with the first five.
2. **OD2 — "unverified with no owner":** verified means an active owner link, so "unverified" and "with no owner" are
   one set. (a) **the tile = unverified and not hidden** (`?status=unverified`, the prototype's), and «غير موثّقة»
   in the spaces tile's helper the same figure; (b) "with no owner" = never linked to any owner (a link of any state),
   a new query. *Recommended:* (a).
3. **OD3 — «اكتمال البيانات»'s «عرض الكل»:** its set (unverified, hidden included, stale or missing) has no list.
   (a) **`GET /admin/spaces` accepts `status=unverified&stale=true` with hidden included through a new
   `status=editable`** (one value, ≈ 3 files, the card's total = the list's); (b) the link opens `?stale=true` (verified
   included; totals differ); (c) the card excludes hidden spaces (the list exists; A8 says "and the hidden ones").
   *Recommended:* (a), in C10.
4. **OD4 — the admin's route:** `GET /admin/overview` (the `overview` module, conventions §7) replacing v1-mvp's
   planned `GET /admin/stats`; `can()`'s unused `platform.stats.read` (a) **removed** or (b) kept. *Recommended:*
   `/admin/overview`, (a) removed (an action nothing checks is a false promise).
5. **OD5 — finding 170** in this PR (C12, 3 files, its race test). *Recommended:* in.
6. **OD6 — `GET`/`PATCH /me`** (planned, not built; ≈ 8 files; the web's account screen needs it?). *Recommended:* in,
   if worker A's account screen reads it; else out and the v1-mvp row says so.
7. **OD7 — `GET …/visits`** (planned; finding 161; ≈ 8 files): who reads it — (a) **the owner any range (≤ the
   payments list's bound), reception today only**; (b) both any range. *Recommended:* in, (a).
8. **OD8 — finding 167** (on #129): in **only if #129 has merged** when lane L starts. *Recommended:* in then.
9. **OD9 — finding 152 (the audit's retention), when:** (a) **decide after the first deployment's measurement** (a
   size check of `audit_logs` monthly, the owner's); (b) a rule now: the desk's entries (visits, check-ins, payments)
   older than two years dropped, the platform's and the money's decisions kept — a job on the scheduler port (≈ 5
   files, out of this PR); (c) raise the database limit when near, cost accepted. *Recommended:* (a); 152 stays open.
10. **OD10 — finding 171:** out of this PR (it needs a new error code and a desk screen change). Options as the
    finding: (a) an optional `published.amountAgorot` compared, 409 when it differs; (b) the screen re-reads the price;
    (c) accepted. *Recommended:* (a) in a later desk item.
11. **OD11 — one PR of ≈ 95 files:** as the owner ordered; the review gets the units in order (U0 → U6).
    *Recommended:* as is.

### Design issues (for worker A's screens; not findings)
- **DI1** The owner's prototype says «زيارة لم تُحصَّل اليوم»; the desk's list (and this count) has no day: the label
  drops «اليوم».
- **DI2** The prototype's «اليوم: {present + left today}» has no field (OV1 names present now only).
- **DI3** «إعلانات نشطة»'s helper lists the running types: `announcements.types` answers them.
- **DI4** The admin's prototype has no «مستخدمون جدد» tile; OV4 adds it (`newUsers`), linking to `GET /admin/users`
  (newest first; no date filter: the link shows the list, not the 30 days).
- **DI5** The prototypes' thresholds are constants (`LIMIT = { prices: 30, other: 60 }`); the screens read the stale
  groups and days from the answers (OV6).
- **DI6** «بلاغات مفتوحة»'s helper «بانتظار الإدارة · بانتظار المالكين» is `reports.awaitingAdmin` /
  `awaitingOwners`.
- **DI7** The debts' CSV needs every debtor: the web reads the pages (≤ 50 each) before it builds the file.
- **DI8** «متوسط مدة الجلوس»: the API answers whole minutes; the web formats `4:12`.
- **DI9** «دفعوا في الشهر»'s "current subscription" line has no field; «ساعة الذروة»'s helper «الأحد والاثنين الأعلى»
  has none (the heatmap shows it).

---

## 13. Executor checks (each when its code exists; what to do if it fails)

- **EC1 — the base:** `git fetch origin`; `main` = `e3b2f97b` or later; `git diff --name-status e3b2f97b origin/main`
  shows no code file of §7 changed by others; `gh pr view 129 --json state` (merged → re-read the shared documents and
  the findings index on `main` before editing; L10 possible). *Fails:* a §7 code file changed → record, re-read it,
  adapt within the plan's decisions, and say so (autonomy rule).
- **EC2 — `unnest(${froms}::timestamptz[], ${tos}::timestamptz[]) WITH ORDINALITY`** binds through `Prisma.sql` and
  answers in order (T-F3). *Fails:* one `VALUES` list built with `Prisma.join`; say so.
- **EC3 — `balancesOf` reused without change** by `balancesPage`/`balanceTotals`. *Fails:* a change to its text is a
  change to the customers list's rule — record it, make it, run `balances.api.test.ts` and the customers tests, and
  name it in the report.
- **EC4 — the cost on a year** (`scripts\year.sql`, on `masaha_b_test` only, through `docker exec masaha-postgres-1
  psql`): one space with 500 subscriptions, 2 000 customers, 9 000 visits, 3 000 check-ins, 10 000 payments over 365
  days (5 % voided, 2 % written-off visits), 10 other spaces alike, 300 spaces in all, 5 000 users; `EXPLAIN (ANALYZE,
  BUFFERS)` of each D10, D11 statement, the payers', and each D20 count. *Over 150 ms:* **recorded, not indexed** (Q5);
  continue; the owner decides at the review. Truncate the tables after.
- **EC5 — `spaces.freshnessOf`'s home:** the `spaces` module has sub-services (`space/`, `listing/`, `facts/`); put it
  where a one-space read of the freshness columns already lives (`space.service.ts`'s read, or the listing's
  `page({ ids: { in: [spaceId] } })` reused). *Fails* (neither fits without a lock or the facts): a new repository
  function in `space/` selecting the five columns by id; say so.
- **EC6 — the oldest visit's name** for `BalanceRow.oldestItem`: `visits.deskVisitsOf(spaceId, ids, tx)` takes a
  `tx`. *Fails:* read the names outside the snapshot (a name is no figure, as `namesFor`); say so.
- **EC7 — the seed's test:** `seed.api.test.ts` can run the seed's environment check with a given contact. *Fails:* a
  unit test of the environment schema extracted as a pure function in `run.ts` (`seedEnvSchema`), and say so.
- **EC8 — `endingSoon` equals the customers list:** `customerIdsBy({ status: 'ENDING_SOON' })` minus archived
  customers (the list leaves archived out) — check whether `customers.page` drops archived for this filter; make the
  count match the list exactly (T-O2). *Fails to match:* the count follows the list; say so.
- **EC9 — `hasPhotos`:** the listing row carries a photo count or cover. *Fails:* drop `hasPhotos` (A8's «بدون صور»
  is `neutral` and not in OV4), and say so.
- **EC10 — `users.created_at` without an index:** measured in EC4 with 5 000 users. *Over 150 ms:* recorded (Q5).
- **EC11 — the listing service in a variable:** `app.ts:345` builds it inline for `adminSpaces`; keeping it in a
  `const` changes no behaviour (the same instance). *Fails:* `adminSpaces` gains `count` on its own listing; say so.
- **EC12 — `/me`'s fields and audit:** `users.signedInAccount` answers the fields D33 names; a name change is audited
  today by an existing action (`git grep "action: 'user\."`)? Use it if one exists; else `user.profileEdited` added
  to `AUDIT_ACTIONS` (shared `audit/actions.ts`) and **not** to the admin's allowlist; the router is `users.routes.ts`
  (`POST /password` today). *Fails:* stop lane L's C13 and record (autonomy rule: decide — skip C13, say so).
- **EC13 — the visits list's bound:** the payments list's range bound (its schema in `@masaha/shared/payments`); reuse
  it. *Fails* (none): 31 days, stated.
- **EC14 — the test files:** each module's existing API test file for its new function, or a new `<function>.api.test.ts`
  beside it; the lane choice recorded.
- **EC15 — the demo data for the real run:** payments this month, a debtor, a customer in credit, closed stays in the
  14 days, an open data report, a running announcement, a subscription ending soon, an unverified space with a stale
  group (SQL reads). A missing one → that case **not performed**, with why and its test.

---

## Appendix — the plan's numbers at a glance
- Routes: finance 4 (D1a–D1d), overviews 2 (D2a–D2b), left items up to 4 (D3a–D3d).
- Finance corrections re-verified: R1–R15 (11 change the finance plan's text: R1, R2, R4, R5, R7, R9, R10, R11, R13,
  R15, and the real run's cross-check).
- Left items: in 6 sure (F1, F2, F3, F4, 153, 97) + 4 pending OD (170, `/me`, visits, 167); out 7 groups (152, 171,
  187, L14, L15, L16, and the `/admin/stats` name).
