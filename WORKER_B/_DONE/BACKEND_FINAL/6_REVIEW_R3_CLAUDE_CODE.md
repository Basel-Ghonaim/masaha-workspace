# Review of #131 — R3: the overviews and the closing documents — Claude Code
Head: c41a5397 · range 53c6a7e3..c41a5397 (5 commits) · checks: green (build, check:classes, check:conflicts, check:links, format:check, lint, typecheck, test:unit, test:api, test:component pass; CodeRabbit skipping) · head moved during the review: no (`headRefOid` c41a5397 at the start and the end; `CLEAN`, `OPEN`)
Verdict for my range: mergeable after a fix round (no blocker; one should-fix in a document, two nits)

Every read pinned to `c41a5397` (the head is the range's last commit, so every file of the range is read at the head). Commit objects only, via `git -C C:\dev\masaha\app-design show/grep/diff`. No edits, no runs.

## Findings (verified defects only, most severe first)

### R3-F1 — should-fix · `announcements.md` says `runningTypes` is "one `DISTINCT` query"; Prisma issues no DISTINCT
- Where: docs/features/announcements.md:62 at c41a5397 (code: apps/api/src/modules/announcements/announcements.repository.ts:157–163)
- Seen in the code: `runningTypes` is `prisma.announcement.findMany({ where: …RUNNING…, distinct: ['type'], select: { type: true } })`. `schema.prisma`'s generator has `previewFeatures = ["partialIndexes"]` only, with no `nativeDistinct`. Without that flag, Prisma removes the duplicates in memory. EC4's statement log (`scripts\ec4-durations.log`:35–37, a report artifact, but it is the SQL that actually ran) confirms it: `SELECT "announcements"."id", "announcements"."type"::text FROM "announcements" WHERE (space_id … deleted_at IS NULL … starts_at <= $2 AND (ends_at IS NULL OR ends_at > $3)) OFFSET $4`, with no DISTINCT. The plan's D20 cost line ("`SELECT DISTINCT type …`") assumed SQL that was never built.
- Scenario: a reader of the capability document, or a later cost review, takes the read to be one deduplicated row per type. In fact every running announcement's row is fetched and deduplicated in Node. Today's cost is negligible (a space has few running announcements), so the behaviour is right and only the document is false (*a false document*).
- Fix: reword the line to "one query of the running ones on the list's own `RUNNING` condition, each type kept once" and leave the code as it is. The other choice is to enable `nativeDistinct`, but that is a Prisma configuration change outside this PR's scope, so do not. · Belongs: a fix round on #131 (folded into 447be920)

### R3-F2 — nit · conventions §9 still says the owner's overview "will read" `closures.summary`
- Where: docs/backend/conventions.md:293 at c41a5397
- Seen in the code: the *Composed reads* bullet from #112 ends "The owner's overview will read `closures.summary`. 2026-10-24, #112." `ownerOverview.ts:61` now calls `closures.summary(space.id, at)`, and the same document's §9 *`overview`* (line 264) says so in the present tense.
- Scenario: one document states the same fact twice, once as future and once as built. C9 updated §9 *`overview`* but not this line.
- Fix: "The owner's overview reads `closures.summary` (2026-10-29, #131)." Or drop the sentence, since §9 *`overview`* owns the fact. · Belongs: a fix round on #131 (folded into a12f928e)

### R3-F3 — nit · `occupancy.glance`'s default `at = clock()` is used only by its test
- Where: apps/api/src/modules/occupancy/occupancy.service.ts:223 at c41a5397
- Seen in the code: `async glance(space: LoadedSpace, at: Date = clock())`. Its one production caller, `ownerOverview.ts:63`, passes `at`. The default is reached only by `glance.api.test.ts:122` (`occupancy.glance(await loaded())`). The plan's D20 signature was `glance(space)`; the lane recorded "`glance(space, at?)`" as its decision.
- Scenario: a code path that no production caller takes, kept for a test (the project's no-test-only-production-code practice). The overview's single-instant rule (S21) then depends on every future caller remembering to pass `at`.
- Fix: make `at` required; the test passes its `NOW`. · Belongs: a fix round on #131 (folded into 447be920)

## The plan's tests and breaks for my range (one line each: present / missing / weaker; would it fail?)
- U-O1 `staleDays` Gaza days (staleness.unit.test.ts) — present. B-O1 (UTC days): 23:30 on the 1st and 00:30 on the 3rd in Gaza give 1 UTC day against 2 Gaza days, so it fails.
- T-M1 `freshnessOf` (spaces/listing/freshness.api.test.ts) — present. B-M1 (60/30 constant): after `saveStaleness(90/45)` the groups stay stale, so it fails.
- T-M2 `openCountOf` (spaceReports.api.test.ts) — present, with a hand count of 2 against resolved, dismissed and other-space reports. B-M2 fails.
- T-M3 `unpricedCount` (unpriced.api.test.ts) — present, hand count 2 with an open visit present. B-M3 (`checked_out_at` dropped from the shared const) gives 3 and fails.
- T-M4 `endingSoon` (subscriptions/endingSoon.api.test.ts) — present, including an hours pack with no end (sorted last), Bilal's superseded subscription, an archived customer and another space, plus a comparison with `GET …/customers?status=ENDING_SOON`. B-M4 gives 7 against 6 and fails.
- T-M5 `runningTypes` (announcements.api.test.ts) — present. B-M5 (`deletedAt` dropped) brings EVENT in, so it fails.
- T-M6 `glance` (occupancy/glance.api.test.ts) — present, also compared with `GET …/occupancy`. B-M6 fails.
- U-O2 `lastDaysSince` across DST (gazaTime.unit.test.ts) — present. B-O2 (`now − 30 × 24 h`) gives 2026-10-11T08:00Z against 21:00Z and fails. `auditPeriod.ts` now calls it, with `LAST_DAYS = 30` the same rule (29 days back).
- T-M7 `counts` (adminSpaces.api.test.ts) — present, with hand counts and the four list totals, deleted spaces included. B-M7 (`isHidden:false` dropped) gives unverified 3 against 2 by the hand count and fails, even though the list shares `listingQueryOf`.
- T-M8 `staleEditable` — present, with hand rows plus the `?status=editable&stale=true` total and names. B-M8 fails.
- T-M9 `openCounts` (openCounts.api.test.ts) — present. B-M9 gives open 4 against 3 and fails.
- T-M10 `countCreatedSince` — present, with an account exactly at `since`. B-M10 (`gt`) fails.
- T-O1 the owner's work queue — present, hand counts including an archived debtor (Rami) and an AUTO unpriced visit counted in both lists. B-O3 gives customersOwing 1 and fails.
- T-O2 each count equals its list (uncollected, unpriced, reports OPEN, announcements RUNNING, customers ENDING_SOON, finance/debts `owed.customers`) — present. Weaker than the plan said in one respect: B-M3 and B-M5 cannot turn it red, because count and list share one const and the running count is `closures.summary`'s, not `runningTypes`. The lane said so, and T-M3 and T-M5's hand counts catch both breaks. Acceptable.
- T-O3 no `agorot` in the body (case-insensitive) — present. B-O4 (`balanceTotals` passed whole) fails.
- T-O4 present now, FULL at capacity, and the override — present. B-O5 fails.
- T-O5 first five sorted, running types — present, built out of order. B-O6 fails.
- T-O6 reception 403; stranger, other owner and admin 404 — present. B-O7 (`requireCan` removed) and B-O8 (mounted outside `manage`) fail.
- T-O7 admin tiles, with the new-users window edges (23:30 on the 11th out, 00:30 on the 12th in, across DST) — present. B-O9 fails.
- T-O8 tiles equal the admin lists, including `?status=editable&stale=true` and the handledBy split — present.
- T-O9 completeness, hidden included, verified, deleted and fresh excluded — present.
- T-O10 a saved threshold changes both overviews — present (AC-O5).
- T-O11 `REFUSED_CALLERS` (guest 401, USER 403, OWNER 403, pending admin 403 `PASSWORD_CHANGE_REQUIRED`) plus a body search for `present|customer|capacity|visit|subscription|payment|agorot` — present. B-O10 fails.
- `can.unit.test.ts`: `space.overview.read` is `OWNER_ONLY`, and `platform.stats.read` is removed from both the table and the expectations.
- The break lines themselves I only read in the lane report (`scripts\lane-o\REPORT.md`). I judged that each break would fail by reading the test against the code, not by running it.

## Decisions taken without the owner in my range, judged
- Lane O (1), OD3's `editable` in a second shared schema (`adminSpacesListQuerySchema`) plus finding 158: acceptable. OD3 (a) is met on the API. Widening the one schema would have forced an `apps/web` type and a copy change outside the PR's scope. Finding 158 records the merge back into one schema and the web's fallback.
- Lane O (2), `endingSoon` counted through `customers.page` (EC8): sound. The count is the list's own rule, archived customers left out, and T-M4 compares it with the route.
- Lane O, EC9 failed and `hasPhotos` dropped: sound. It is the plan's own fallback, and OV4 does not ask for it. A design note goes to worker A.
- Lane O (3), `glance(space, at?)` and `present.countsIn`: `countsIn` is sound (two counts, no names). The optional `at` is a nit (R3-F3).
- Lane O (4), `ListedSpace.stale` with a pure `freshness()`: acceptable. One rule serves the owner's groups and the admin's rows. The admin list's mapper (`adminSpaces.mapper.ts`) does not pass it on, so no answer changed.
- Lane O (6), `openCounts` as three counts in parallel: acceptable (cheap, on `(status)`).
- Lane O (7), `listingQueryOf(Partial<…>)`: acceptable. The counts pass only the filter fields.
- Lane O (8), T-O3 case-insensitive: sound (stricter than the plan).
- Lane O (9), nine sources, not ten: sound. `closures.summary` gives both the awaiting count and the running count.
- LEAD-D4, EC4 run once on the joined code: sound. The owner's overview measured 103 ms and the admin's 63 ms. I only read this in the report.
- LEAD-D5 and LEAD-D6, T-O2's debtors compared with `GET …/finance/debts`, and the test's space given its settings row: sound. The overview itself reads no settings row (`ownerOverview.ts` calls no settings read). The 500 was the debts route's `reminderTemplate` on a factory space that the API would never create without a settings row.

## Outside my range
- None found while reading. (Finance's own handling of a space with no settings row, LEAD-D6's 500, belongs to R2.)

## Checked and fine
- **No amount (OV1, OV2, O3).** `OwnerOverview` (packages/shared/src/overview/responses.ts) has no amount field at any depth. `ownerOverview.ts:67–81` builds every field by name: of `uncollectedTotals` only `.visits`, of `balanceTotals` only `.owed.customers`. `endingSoon` maps `{ id, name }` and `{ id, name, endsOn }` explicitly (subscriptions.service.ts:348–351). `glance.present` is built `{ visits, members, total }`. No spread carries a source object through. There is no debug field.
- **Who reads what (OV3, OD4).** The manage route is `requireCan('space.overview.read')` (owner only, can.ts) inside `manage`, behind `requireSpaceAccess` (app.ts:630–631). The admin route sits inside `/admin`'s guard (app.ts:667). `platform.stats.read` is gone from `can.ts` and its unit test. `git grep` finds it only in the three documents that record its removal, and nothing in apps or packages depends on it.
- **No logic in `overview` (OV7).** No repository. One `Promise.all` per screen (nine reads for the owner, four for the admin). It imports `payments`, never `finance`. Its only expressions are `capacity !== null` and `unverifiedNoOwner = unverified` (OD2).
- **Each count against its list, filter by filter.** `openCountOf` uses `statusWhere('OPEN')`, as `pageOfSpace` does. `unpricedCount` and the list share `unpricedWhere`. Uncollected comes from `uncollectedOf`, the same `FROM` as `uncollectedPage`. The running count is `counts()`'s SQL, the same condition as `STATE_WHERE.RUNNING`, and T-O2 checks it. `endingSoon` is `currentByCustomer(statesOf)` filtered `ENDING_SOON`, as `customerIdsBy` filters, then `customers.page(archived:false)` (OD1). Verified, unverified, hidden and stale use `listingQueryOf` through `listing.count`, which uses `whereOf`, the same as `findPage`. Completeness uses `status=editable` (`ids notIn verified`, hidden included, deleted excluded by `whereOf`) with `staleOnly` (OD3), matching OD2's tile. `openCounts` uses `space.deletedAt: null` plus OPEN, as `pageAll`, and `handledByWhere`, the helper `pageAll` uses. The spread is safe here because `where` names `space`, not `spaceId`. New users come from `lastDaysSince(at, 30)`, 29 days back from Gaza midnight, with `gte` (OV5).
- **Stale by the saved thresholds (OV6).** `freshnessOf`, `listing.page` and `listing.count` read `platformSettings.stalenessThresholds()` on each call, and no constant appears in the overview. T-O10 and T-M1 prove it.
- **«اكتمال البيانات» (A8).** First five by `nameEn`, then id. Unverified with hidden included, missing and stale both counted (the `staleBefore` OR keeps the null groups). Each row has `hidden`, `missing` and `stale` with days. The total equals `?status=editable&stale=true`.
- **Cost, no N+1.** Owner: about 19 statements in parallel, all set-based or by key. The heaviest are `balanceTotals` and `statesOf` over the space, the same reads the customers list's filters already do. Admin: `findVerifiedSpaceIds` three times (in `counts`, `staleEditable` and `openCounts`; the plan said twice), four `spaces` counts, one page, three `data_reports` counts and one `users` count. Observations only, not defects: `freshnessOf` runs `findPage`'s unused count for its single row, and the verified ids are read once more than planned. Both are microseconds on small tables.
- **Documents (C16 and C8–C11).** v1-mvp: step 11 *Built* (finance), step 12 *Built* (both overviews), the `/me`, `…/visits`, `…/overview` and finance rows, `/admin/stats` replaced by `/admin/overview`, and *Settles* corrected to "no export route". `docs/project/overview.md` *Built*: Finance and Overview lines, API only. `docs/README.md` map: `finance.md` and `overview.md`. Conventions §9 *Composed reads*: "`overview` (how many owe, a count — never an amount, the owner's O3)" (R11). Foundation §13 screen 12 (line 461) matches OV8 and §11.1 item 6 word for word. The findings index lists 158 under Open and 97, 153, 161, 167, 170 under Resolved, matching each file's status line. `overview.md` follows the §5 template (no web parts and no *Open findings*, correctly, since none exists), matches the code, and dates each decision 2026-10-29, #131. Contract *Overview*: the shapes equal `responses.ts`, and the errors are worded as the sibling `audit-log` and `finance` routes. `security.md` has two bullets. Every touched document's *Last Updated* is 2026-10-29. `#131` appears where `#PRNUM` was. No document claims a screen is built: "Screens 12 and 25 remain planned".

## Not checked, and why
- That each break turns red, by running it: the review rules forbid runs. I judged each by reading (above), and the red lines are only in `scripts\lane-o\REPORT.md`.
- EC4's timings (103 ms and 63 ms, no statement over 150 ms): only in the lead's report and its log, which I did not re-run. I read the log only for R3-F1's SQL.
- The R1 and R2 ranges' code that my range reads (`payments`' `uncollectedTotals` and `balanceTotals`, C4): I read them only as far as the overview's use of them (the fragment shared with the list, the fields picked). Their correctness is R1's and R2's.
- The web's handling of `?status=editable`: `apps/web` is out of scope. Finding 158 states the gap.
