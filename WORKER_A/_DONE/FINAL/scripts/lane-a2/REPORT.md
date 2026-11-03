# Lane A2 — the sub-agent's report (returned as text; saved by the lead)

Lane A2 · DONE · Branch lane/a2 head c17e1b18 (base 37a84e65), clean. 111 files, ≈ +1,860 / −170. No attribution, no
`#PRNUM` in SQL.

Commits: ad4b54ff feat(db): compute a subscription's due in bigint (48) · 9254e5b6 test(db): pin Gaza's transitions in
PostgreSQL (46) · 190e5158 perf(subscriptions): bound check-ins by midnights (49) · a9cdfcd7 fix(jobs): answer 500 when
failures fill a batch (48) · 5519f558 feat(jobs): reclaim the files no photo holds (44) · 7fd9a671 fix(customers):
match a phone under either code (47) · b0ec197c feat(visits): check a visit in for its customer (47) · 6514d321
feat(subscriptions): refuse a changed price (43) · 87a620d4 feat(subscriptions): name who recorded and voided (49) ·
20cf0839 feat(visits): list a space's written-off visits (47) · 10605e65 feat(db): keep a subscription's published
period (48) · 7ce2a438 feat(customers): carry the reminder in the file (47) · 2abb2f8a feat(desk): say more of who is
there and of plans (49) · e613dfde feat(data-reports): read one report by its id (45) · c17e1b18 feat(spaces): name the
retired amenities held (45).

**Migrations.** M1 `apps/api/prisma/migrations/20261029144213_subscription_usage_bigint/migration.sql` — the plan's
§5.2.M SQL exactly (header comment; `DROP FUNCTION "subscription_usage"(integer, integer, date, date);`; `CREATE
FUNCTION … RETURNS TABLE (…, "due_agorot" bigint) LANGUAGE sql STABLE`; `CASE billing WHEN 'FIXED' THEN
price_agorot::bigint WHEN 'PER_DAY' THEN count(DISTINCT c.day) * price_agorot::bigint ELSE
round(coalesce(sum(c.minutes),0) * price_agorot::bigint / 60.0)::bigint END`; the lateral join unchanged). M2
`…/20261029154841_subscription_published_period/migration.sql`:

```sql
-- AlterTable
ALTER TABLE "subscriptions" ADD COLUMN "published_period" "PricePeriod";

-- A subscription sold from a published price keeps its period, so the customers list can filter the weekly and
-- the monthly ones (foundation §13 #14): only a week or a month, never with a package.
ALTER TABLE "subscriptions" ADD CONSTRAINT "subscriptions_published_period_check"
  CHECK ("published_period" IS NULL OR ("published_period" IN ('WEEK', 'MONTH') AND "package_id" IS NULL));
```

Schema `Subscription.publishedPeriod PricePeriod? @map("published_period")` (`prisma format` re-aligned the model).
Each folder by one `migrate dev --create-only` on `masaha_a_lane_a2_dev`, then edited; deploy + generate there; the
test set-up migrates the test database. Incident: C2.1's red run applied M1's still-empty migration to its own test
database; the row deleted from `_prisma_migrations` there and re-deployed (`lane-a2/fixtestdb.mjs`).

Red → green: C2.1 T50 "22003 integer out of range", T51 "expected 500 to be 200" · C2.2 T52 green, proof B52 · C2.3
T53 "checkInsOnDays is not a function" · C2.4 T54 "200 to be 500", T55 "{…(3)} to deeply equal {…(4)}" · C2.5 T56/T57
"storage.list(...) is not a function", T58 "undefined to deeply equal { skipped: true }" / "{ removed: 200, kept: 2 }"
· C2.6 T59 "[] to deeply equal ['Dana']" · C2.7 T61 "to match object { visitorName, customer }", 422 test, T62/T63
"201 to be 422/409" · C2.8 T64 "201 to be 409" · C2.9 T66 recordedBy / voided.by · C2.10 T67, T68 "404 to be 200/403"
· C2.11 T69 "{ publishedPeriod: 'MONTH' }", T70 unit, T71 proof B71 · C2.12 T72 "{ reminderTemplate: null }" · C2.13
T73, T74 · C2.14 T75, T76 "404 to be 200" · C2.15 T77 "{ retiredAmenities }".

Breaks (backup copy, restored): B51, B51b → 500 · B52 zone 'UTC' red ('Asia/Jerusalem' stays green: same 2026
transitions in the installed zone data) · B53, B53b · B54, B54s · B55 · B56 (4 files, not 3) · B57 (1, not 2) · B58
`{ removed: 3, kept: 2 }`, B58b · B59; B60 green with the same break (126 says the +972 direction worked), B60b red ·
B61 · B62 201 · B63 500 · B64 201 · B65 409 ×2 · B66 · B67 · B68 200 for reception · B69 · B70 · B71 (CHECK dropped on
its own test DB) "promise resolved instead of rejecting", restored (`b71.mjs`, `b71fix.mjs`) · B72 · B73 · B74 · B75
200 not 404 · B76 404 · B77.

Heavy checks (grant, head c17e1b18, 2026-10-31 UTC): lint 0 (08:18:58) · typecheck 0 (08:40:18) · unit shared 27 /
274 · unit api 75 / 906 · unit web 157 / 1076 · **test:api on masaha_a_lane_a2_test: 1 failed | 116 passed (117), 1
failed | 1347 passed (1348)** — `finance/debts.api.test.ts` › "the totals agree with every page's rows, and the
reminder template is the space's, null by default" timed out (5770 ms > 5000) under load; alone twice green (1686,
1423 ms). Earlier (10-30, loaded): staff "the owner issues a new temporary password only while one is pending" 7.4 s;
desk customers' 1,000-subscriptions test ≈ 6 s (green 10-31); its own reclaim "removes at most 200 files a run" 6.3 s →
fixed in C2.5 (ten removals at once, parallel set-up; 1.5 s; B58/B58b re-made). Incidents: the 10-30 full run stopped
with TaskStop left slot-2 held (released by hand, logged); a reclaim test file run against the same DB during it.

Shared files: `app.ts` (the `photos.reclaimOrphans` job after `subscriptions.autoCheckOut`; `lookups` in `facts`) ·
contract (Front desk, Subscriptions, Customers, Occupancy, Data reports, Spaces › retiredAmenities, Internal) ·
data-model (Amount due bigint; the published period; the Subscription entity) · conventions §12 (`list`) · features
subscriptions, payments, visits, customers, occupancy, spaces, data-reports · web test fixtures (desk ×10 + deskCustomer,
occupancy ×4, spaces ×2, routes test `retiredAmenities: []`) · web copy `desk.ts` customers.kind.options WEEK «أسبوعي» /
Weekly, MONTH «شهري» / Monthly (U8's sub-object; needed for typecheck) · `space-links.service.unit.test.ts` one stub
line · packages/shared subscriptions, desk, payments, visits, occupancy, spaces.

Findings closed: 122, 120, 127, 121, 63, 126. API halves of 160, 171, 162, 164, 99 built (files for the web lanes).

ECs: EC10 yes — `GET /manage/spaces/:spaceId` answers `owners` (active OWNER links, oldest first); no route · EC11
readers: subscriptions mapper, payments `itemBalances`; DEBT/CREDIT sums and `balanceTotals` now `::bigint` + Number();
nothing depends on the function · EC12 `gazaInstant(date, 0)` + `addDays`; `GET …/visits` already filters by instants
· EC13 the demo sells nothing from a published price: seed unchanged · EC24 `PresentPerson` built in
occupancy.service `peopleIn` from `visits.openIn` (now selects `audience`) · EC25 reused `visits.writeOff`,
`space.dataReports.read`, the admin role guard.

Decisions (none SERIOUS): LA2-D1 DEBT/CREDIT and `balanceTotals` were `::integer` → `::bigint` + Number() · LA2-D2 the
written-off list lives in `payments` beside the uncollected list (visits, L3, may not import payments); type in
`@masaha/shared/visits`; same path · LA2-D3 `stalled: true` only on a stall; `JobDone` `Record<string, number |
boolean>`; `JobsRun.stalled` · LA2-D4 reclaim skips outside Gaza 03:00; ≤ 200 a run, ten at once · LA2-D5
`visit.checkedIn` audit carries `customerId` only for a customer's visit · LA2-D6 `publishedPeriod` on
`DeskSubscription`; not in the created audit · LA2-D7 the file reads `spaceSettings.read`; three test files give their
space a settings row · LA2-D8 retired amenities named through `lookups.retiredAmenitiesNamed` injected into the space
view (async, takes the tx); `lookups` added to group-edit deps · LA2-D9 the admin's single report `not_found` for a
soft-deleted space · LA2-D10 T52 compares date and minute · LA2-D11 per-commit eslint/tsc, full runs at checkpoints.

Join notes: app.ts (its job line, `lookups` in `facts`); `namesFor(ids, tx)` and once `(ids, undefined)`; no new test
uses `whileHeld`; stubs of LookupsService/Repository need `retiredAmenitiesNamed`/`findRetiredAmenitiesNamed`;
jobs.api.test's whole-list `toEqual` needs A1's two sweeps; breaking: `ItemPayment.voided.byId` → `voided.by { id, name
}` + `recordedBy`; `CUSTOM` narrowed.
