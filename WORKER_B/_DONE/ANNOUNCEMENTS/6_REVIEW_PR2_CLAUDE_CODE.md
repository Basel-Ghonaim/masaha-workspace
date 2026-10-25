# Review — ANNOUNCEMENTS PR 2, #120 `feat/data-reports` (independent reviewer)

- **Head reviewed:** `36718fde7e19973f422e327c51ecab14e8599c65` (as expected). Base `origin/main` `b2f13a47`.
- **CI:** every check green (`build`, `check:classes`, `check:conflicts`, `check:links`, `format:check`, `lint`,
  `test:api`, `test:component`, `test:unit`, `typecheck`, CodeRabbit). `mergeStateStatus` CLEAN.
- **Head at the end:** `36718fde`, unchanged.
- I read everything from commit objects pinned to the head sha. I ran no tests or servers and did no checkout.

**Verdict: mergeable.** No blocker and no should-fix in the code. There are four small document or naming nits for
PR 3's first commit, and one design point to record as a finding.

---

## Findings, most severe first

### 1. finding to record (150, plausible) — the owner sees a report's exact time, which can point to the reporter
- **Where:** `data-reports.mapper.ts` `toSpaceReport` (`createdAt: row.createdAt.toISOString()`). The owner's list
  is ordered newest first by `createdAt`, then id. The shape `SpaceReport.createdAt` comes from plan D2.
- **Seen in the code:** no reporter field reaches the owner, by any path (see *Checked and fine*). But the owner
  gets the report's millisecond timestamp. The same owner reads the desk's check-ins and visits, with names and
  times.
- **Scenario (reasoned):** a small space has four visitors in the morning. One of them checks in at 10:38. At
  10:42:13.512 a `PRICES` report of that space appears in the owner's list. People usually report from inside the
  space, so the owner can narrow the reporter to one or two people. That works against O12 ("a reporter must not
  fear the space"). It is a consequence of the approved shape, not a code defect, so it is the owner's call.
- **Options for the owner:** answer the owner's `createdAt` coarsened (to the Gaza day, or the hour) and order by
  it, keeping the exact time for the reporter and the admin; or accept it.
- **Where it belongs:** **record finding 150** (B's block; 150 is free on `main`). It is not a fix round, because
  it changes an approved shape (*propose, don't decide*).

### 2. nit — the "site" router is a fifth router kind that conventions does not define
- **Where:** `docs/backend/conventions.md` › *Routers*: "A module has up to four routers, one per audience"
  (public, me, manage, admin). The PR changes §7's `data-reports` row from `me` to "site (…)", and §9 to "`site`, at
  the API's root". The code has `data-reports.site.routes.ts` and `createDataReportsSiteRouter`.
- **Seen in the code:** this router serves only signed-in users (`requireAuth()` on both routes). That is the
  **me** audience. *Routers* already says a path need not carry its module's name, so being mounted at the root
  does not make it another kind. The name comes from plan D1, so it is not the executor's departure. But this PR
  made the conventions disagree with themselves: before it, §7 and §9 said `me`.
- **Fix:** call it the `me` router: the §7 row "me (at the API's root: a report, and the reporter's own)", and §9
  likewise. Rename the file and factory to `data-reports.me.routes.ts` / `createDataReportsMeRouter`, plus
  `index.ts` and `app.ts`. The other way would be adding a *site* row to *Routers*, but that is a convention
  change and needs the owner.
- **Where it belongs:** small — **PR 3's first commit** (`0_CARRIED_FROM_120.md`). PR 3 adds `me` routers itself.

### 3. nit — the feature document and the contract over-state "the owner and the admin at once"
- **Where:** `docs/features/data-reports.md` › *Behaviour and flows* › **Decide**: "The owner and the admin at once:
  the second waits on the space's lock and finds the report decided." Also the contract's
  `PATCH /admin/data-reports/:reportId` errors: "`conflict` (409) … also when the owner decided it first". C4's
  commit body says the same.
- **Seen in the code** (`data-reports.service.ts` `decideUnder`, lines 120–130): `can()` runs on the links under
  the lock **before** the report is read. Take the common order: the owner decides and stays linked while the
  admin's decision waits. The admin then reads a verified space and gets **403 `forbidden`**, never 409. The admin
  gets 409 only if the owner was unlinked in between, which is what T19 builds by hand. The reverse order is right
  as written: the admin decides an unverified space, an owner is linked and decides, and the owner gets 409.
- **Fix:** "an owner's decision while the admin's waits makes it 403 while the owner is still linked, and
  `REPORT_ALREADY_DECIDED` once the space is unverified again; the admin's decision first makes the owner's 409."
  Make the contract's admin line the same.
- **Where it belongs:** small — **PR 3's first commit** (documents).

### 4. nit — a sentence in the feature document's *Decisions* sits under the wrong bullet
- **Where:** `docs/features/data-reports.md` › *API decisions*. The bullet "The admin decides an unverified space's
  reports only…" ends with "2026-10-25, #120. The repository's select leaves the reporter out, so no mapper can leak
  them. 2026-10-25, #120." That sentence belongs to the privacy bullet above it, "The owner never sees who reported;
  the admin does (O12)". That bullet has no date.
- **Fix:** move the sentence and its date to the O12 bullet.
- **Where it belongs:** small — **PR 3's first commit**.

### 5. nit — a comment line in the test helper runs past the wrap width
- **Where:** `apps/api/test/app.ts` line 24: "…which never ends nor goes idle. A test of the session's own rules
  signs in" is about 112 characters. The comments around it wrap at 100. Prettier does not reflow comments, so CI
  did not catch it.
- **Fix:** re-wrap the comment.
- **Where it belongs:** PR 3's first commit, with item 2. Drop it if that commit doesn't touch the file anyway.

---

## `REPORT_ALREADY_DECIDED` — the Arabic line

Seen in `apps/web/src/shared/copy/arabic/errors.ts` at the head:

> `REPORT_ALREADY_DECIDED: 'سبق البتّ في هذا البلاغ.',`

This matches the line the owner approved. English: `'This report was already decided.'`. The code is in
`packages/shared/src/core/errors.ts`, after `ANNOUNCEMENT_NOT_STARTED`, with its comment. The contract's §6 lists
it as "(409: a decided report decided again, otherwise than it was, 2026-10-25, #120)". The service throws
`AppError.conflict('REPORT_ALREADY_DECIDED')`, which is 409.

---

## The departures, each judged

1. **`spaces.namesWithDeleted` added in C1, not C2 — right.** `create` answers a `MyReport`, which needs the slug
   and names (service line 272), so C1 needs it. It is one `findMany` with no `deletedAt` filter, exported as the
   `SpaceName` type.
2. **The service's `now` dependency — right.** `createdAt: now()` (create) and `resolvedAt: now()` (decide) come
   from the one clock (conventions §11). Without it, `createdAt` would be the database's `DEFAULT now()`, which the
   tests' clock cannot pin. `app.ts` passes `clock`. The plan's deps list left it out, but the plan's own §11 rule
   requires it.
3. **The `SpacesService` fake gains a line in `space-links.service.unit.test.ts` — right.** It is a type-only
   necessity: one `namesWithDeleted: () => Promise.reject(...)`, the same as its neighbours. It is not test-only
   production code.
4. **The migration made with `migrate diff --script` — right.** This follows the project's rule: a second
   `--create-only` would apply the migration. The folder `20261025112542` sorts after the last one on `main`
   (`20261025081716`). Prisma's generated part (the enum, the column, the index) and D12's appended SQL are both
   in the file. **Prisma's partial index `where: { status: "OPEN" }`** is the plan's string form.
   `previewFeatures = ["partialIndexes"]` is in the generator, so Prisma knows the index and a later migration
   keeps it. The SQL writes `WHERE ("status" = 'OPEN')`.
5. **C0's subject shortened (52 → 42) — right.** `test(desk): copy a shift's published price` still says what the
   commit does.
6. **B15's first break stayed green and was rerun as the plan names it — right.** Adding `userId` to the select
   alone cannot leak it: `toSpaceReport` builds the answer field by field (mapper lines 101–110). The plan's break,
   select **and** mapper, is the meaningful one, and it went red. One caveat, which I read only in the report: the
   rerun's red output is in `scripts\pr2-b15.out`, which I did not open.
7. **B5's restore deleted a leftover row on `masaha_b_test` — acceptable.** The test database is truncated before
   every test, and the executor compared the constraint definitions with `masaha_b_dev`'s afterwards. Nothing
   touched `masaha_b_dev` beyond the real run's stated rows.
8. **Lint and typecheck not rerun after the Prettier-only fixup — acceptable.** CI ran both green on the pushed
   head. A Prettier-only change to one test file cannot change a type or a lint rule. The intermediate commits were
   not each re-checked (`rebase -x`), and the report says so.

---

## Checked and fine (seen in the code at the head)

**Privacy (the owner never sees the reporter)**
- `REPORT` (repository lines 14–24) names no `userId` and no `resolvedById`. `pageOfSpace`, `findOpen`, `create`
  and `decide` select only `REPORT`.
- `lockIn` adds only `resolvedById`, the decider, and `toSpaceReport` drops it.
- `WITH_PEOPLE` is used by `pageAll` and `findWithPeople` only. Both are reached only from `all` and
  `decideAsAdmin`, behind `/admin` (`requireRole('ADMIN')`).
- The owner's decision answer is `toSpaceReport(decided)`, and the as-is path is `toSpaceReport(current)`.
- The errors are `AppError.notFound(undefined, 'Report not found')`, `forbidden()` and
  `conflict('REPORT_ALREADY_DECIDED')`, with nothing of the reporter.
- The audit `after` is `{ note }`, the actor is the decider, and the report's create is not audited.
- **T9 searches the list's answer only, not the decision's.** The decision's answer is still pinned:
  T11 `toEqual`s the whole `SpaceReport` of a resolve, so any added defined key fails it, and T12 checks that the
  as-is answer equals the first. The audit line is `toEqual`ed in T11 too.

**Authorization**
- The manage routes: `GET` has `requireCan('space.dataReports.read')` (`adminOrOwner`) before
  `validate(…, 'query')`. `PATCH` has `requireCan('dataReports.resolve')` before `validate(body)`. Reception is
  refused 403 before either is read (T10 and T14 send invalid input).
- The admin, strangers and other spaces' owners get 404 from `requireSpaceAccess` (`space.read`). A soft-deleted
  space's manage routes are 404, because `linksAt` answers `[]` once `summariesFor` is empty.
- The decision: `findSpaceOf` is compared with the path's space (404). Then `spaces.lock`, which is 404 once
  deleted. Then `can(actor, 'dataReports.resolve', { links })` on the links read **under the lock**: on the manage
  path `space.linksUnder(tx)`, the same loader as `spaceLinks.linksAt`; on the admin path `spaceLinks.linksAt`.
  Then `lockIn` (`FOR UPDATE`). The lock order is the space, then the report. The create takes only the user's row
  (`users.lockAccount`, the session lock), so no two orders cross.
- `adminWhileUnverifiedElseOwner` refuses the admin on a verified space and reception everywhere.

**The create**
- The route order is `requireAuth()` → `limitRequests(DATA_REPORT, by: [userId])` → `validate` → controller, so
  repeats, invalid bodies, unknown slugs and other spaces all count.
- The count is per user, not per address: the key holds only the user id and no slug.
- `findShown` (not deleted, not hidden) plus `isActiveArea` (an active area in an active governorate) is 404
  otherwise. It is the same rule as `publicListing`'s `listed()` and `listedAreaIds`, so `create` and `mine` agree.
- The repeat is answered 200 with `findOpen` and writes nothing.
- The partial index's P2002 (500) is reachable only without the user's lock (B9 shows it), so it is a backstop.

**The decision rules**
- `decisionOf`: open → decide. Decided with the same status, the same normalised note and the same decider →
  as-is. Anything else → conflict.
- A dismissal without a note is 422 by the schema's refinement, and is also refused by the `CHECK`.
- `resolvedAs` is `'OWNER'` on the manage path and `'ADMIN'` on the admin path. The audit is
  `dataReport.resolved` / `dataReport.dismissed` in the same transaction, with the report as the entity and the
  space as the entry's space.

**The user's list**
- `repliedBy` is read from `resolved_as` only (mapper line 96).
- `listed` comes from `publicListing.upTo({ areaIds: listedAreaIds, verifiedIds: [], onlyIds }, n)`. I read
  `listed()` in `publicListing.repository.ts`: `verifiedIds` only feeds `is_verified`, `pricesShown`, and
  `verifiedOnly` when that is set. With no price or verified filter it filters nothing, which confirms the
  executor's check 3.
- Names come from `namesWithDeleted`.

**The admin's list**
- `space: { deletedAt: null }` applies in both the `findMany` and the `count`.
- The status, field and space filters are in one `where`.
- The names come from `users.namesFor` over the reporters and deciders, and `verified` from `verifiedSpaceIds()`.
  Each is one query.

**The migration**
- I read it whole. It has the enum, the nullable column, `data_reports_open_key … WHERE ("status" = 'OPEN')`, and
  the three `CHECK`s exactly as D12 writes them. There is no PR number in it.
- `schema.prisma` agrees with it: the enum, `resolvedAs`, the `@@unique(… where: { status: "OPEN" })` and the
  updated `message` comment.
- Existing rows are safe. No route, seed or script wrote `data_reports` before this PR (`git grep` over
  `apps/api/prisma` and `src`), so no decided row without `resolved_as` can exist. If one did, the `ADD CONSTRAINT`
  would fail loudly rather than pass.

**Races (T4, T15, T18, T19)**
- T4 holds the user's row and waits for two waiters. B9's red (`[201, 500]`) shows it depends on the lock.
- T15 and T18 change the links inside the holder of the space's lock, so they would pass if the links were read
  before the lock (B21, B24).
- T19 builds the owner's decision and the unlink inside the holder. Its 409 does not tell the space→report lock
  order apart from the reverse: the report row is held by the holder either way. No other path locks a report and
  then a space, so this is not a defect.

**Carried from #118**
- Item 1: the new idle test refreshes at T+10 (200), checks that the newest row's `lastActivityAt` is still T, and
  checks that `me` at T+15:01 with the new token is `SESSION_IDLE`. This matches review finding 1.
- Item 2: the shift's price is 15,000 with `shiftId` and the plain one 25,000 with `shiftId: null`. This matches
  finding 2.
- Item 3: ADR 0003's line now says "the guard refuses an idle one (401 `SESSION_IDLE`) and the refresh ends it". The
  `security.md` *Idle* row says a soft-deleted space's links count. That is true to the code:
  `space-links.repository.ts` `activeRolesOf` filters on `deactivatedAt: null` only.
- Item 4: `signAccess` has `lastActivityAt: FAR_AHEAD`.
- Item 5: findings 170 and 171 match the #118 review's points 5 and 6, including the fixes they name. Both are
  indexed under *Open*.

**Documents**
- These are true to the code, apart from items 3 and 4 above: the contract's *Data reports* section and §6,
  `data-model.md` (DataReport, *Constraints*, *Checked by the service*), `security.md` (the limit moved to
  *Built*, its *Rate limits* row, the two *Authorization* bullets), `conventions.md` *Built*, `spaces.md`,
  `v1-mvp.md` (decision 10's wording on both rows), `overview.md` lines 62 and 66 and its *Built* line, and
  `docs/README.md`.
- `#120` appears where a number goes.
- `data-reports.md` follows the capability template.

**Scope**
- 46 files, all in `apps/api`, `packages/shared` and `docs`, plus the web's two `errors.ts` (one line each).
- Seven commits. Subjects are 42–48 characters and each has a body.
- No `package.json` change.

## Read only in the executor's report (not verified here)
- Every red and green output of the breaks (C0-1, C0-2, B1–B24), the real run's `ALL PASS` and its 11 requests to
  the 429, and the local `test:unit` and `test:api` totals.
- I saw CI green, but not the per-break runs. The executor says the reds are in `scripts\pr2-*.out`, which I did not
  open.
