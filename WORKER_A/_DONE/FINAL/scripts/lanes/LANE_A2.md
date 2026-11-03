# Lane A2 — U2: the API of the desk, the money, the data reports and the spaces (with M1, M2)

Read `LANE_COMMON.md` (same folder) first and follow it; this file adds your lane's facts.

- **Worktree** `C:\dev\masaha\app-lane-a2`, **branch** `lane/a2`, **base** `37a84e65` (= `origin/main` `ce671b37` +
  the lead's C0.1 `75c6bc04` — the envelope's `details` — and C0.2 `37a84e65` — the domain code
  `PUBLISHED_PRICE_CHANGED` in `@masaha/shared/core` and both catalogues; your C2.8 uses it).
- **Databases:** test `masaha_a_lane_a2_test` (`TEST_DATABASE_URL`) and **dev `masaha_a_lane_a2_dev`**
  (`DATABASE_URL`), both yours and migrated to the base. Make each migration with **one** `npx prisma migrate dev
  --create-only --name <name>` run from `apps/api` against `masaha_a_lane_a2_dev` (then `ls` the folder: a second run
  would apply it; if the command refuses non-interactively or on a data-loss warning, use `npx prisma migrate diff
  --script` into the folder you make), then edit the SQL as §5.2.M gives it; then `npx prisma migrate deploy` and
  `npx prisma generate` on your dev database. Check how `apps/api`'s test set-up migrates its database (if it does not,
  `migrate deploy` with `DATABASE_URL` set to your test database for that command only). **No PR number in any SQL.
  No migration but M1 and M2.** Never `masaha_dev` or `masaha_test`.
- **Scripts folder:** `C:\dev\masaha\workspace\WORKER_A\FINAL\scripts\lane-a2\`. **Finding numbers:** 202–203.
- **The plan's parts for you** (`2_PLAN.md` lines): §5.2 **694–858** (D2.1–D2.15, §5.2.M); §8 U2 **2056–2071**;
  §9.1 U2 **2188–2203** (C2.1–C2.15, in that order); §10.3 **2449–2482** (T50–T77); §12.1 U2 **2787–2792**; §7's
  rows for 63, 120, 121, 122, 126, 127, and the API halves of 99, 160, 162, 164, 171 (**1947–2018**; write a
  finding's *Resolution* only when your commit finishes it — 63, 120, 121, 122, 126, 127; the others close in the web
  lanes, say so); OD7, OD11 (2830–2867); EC10, EC11, EC12 (the Gaza-midnight helper), EC13, EC24, EC25 (2871–2929).
- **EC10** (`GET /manage/spaces/:spaceId` answers the active `owners` to the owner): check it and say the answer in
  your reply (lane W3 builds 166 on it); if it does not, add the route as EC10 says, recorded.
- **EC13:** you may edit `apps/api/src/db/seed/demo.ts` so the demo's published subscriptions carry their period; you
  never run the seed.
- **Shared files:** `apps/api/src/app.ts` — the reclaim job in its own block (lane A1 adds two sweep jobs; the lead
  joins). `docs/api/api-contract.md` — only your routes' sections (*Front desk*, *Subscriptions*, *Customers*,
  *Occupancy*, *Data reports*, *Spaces (the admin)* › `retiredAmenities`, *Internal*'s stall and reclaim lines).
  `packages/shared/src/{visits,subscriptions,payments,desk,customers,occupancy,data-reports,spaces}/*` are yours;
  never `core/*`, never `space-settings/reminderTemplate.ts` (lane L's), never `auth`, `users`, `audit`,
  `space-links` (lane A1's). `docs/architecture/data-model.md` is shared with A1 (theirs *Operations*; yours
  *Derived values* and *Front desk and money*).
- **Done:** all 15 commits; then lint, typecheck, `test:unit` of `@masaha/shared`, `@masaha/api` and `@masaha/web`,
  and the whole `test:api` on `masaha_a_lane_a2_test`. Reply DONE (§9), with M1's and M2's folder names and SQL.
