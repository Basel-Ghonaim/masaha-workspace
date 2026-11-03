# Lane A1 — U1: the API of identity, accounts, staff and owners

Read `LANE_COMMON.md` (same folder) first and follow it; this file adds your lane's facts.

- **Worktree** `C:\dev\masaha\app-lane-a1`, **branch** `lane/a1`, **base** `37a84e65` (= `origin/main` `ce671b37` +
  the lead's C0.1 `75c6bc04 feat(shared): carry a refusal's details` — the envelope's `details`,
  `AppError.conflict(code, message, errors, details)` — and C0.2 `37a84e65 feat(shared): refuse a published price
  changed`).
- **Databases:** your test database `masaha_a_lane_a1_test` (your `apps/api/.env`'s `TEST_DATABASE_URL`; already
  migrated). `DATABASE_URL` still names `masaha_dev`: never run anything that writes through it (no dev server, no
  seed, no migrate dev).
- **Scripts folder:** `C:\dev\masaha\workspace\WORKER_A\FINAL\scripts\lane-a1\`. **Finding numbers:** 200–201.
- **The plan's parts for you** (`2_PLAN.md` lines): §5.1 **569–692** (D1.1–D1.17); §8 U1 **2042–2054**; §9.1 U1
  **2169–2186** (C1.1–C1.17, in that order); §10.2 **2408–2447** (T20–T49); §12.1 U1 **2782–2786**; §7's rows for 17,
  21, 32, 69, 77, 78, 79, 83, 89, 91, 92, 93, 106, 158 (**1947–2018**); S1, S7 (1834–1853); EC2, EC3, EC9
  (2871–2929). Finding 22 (OD1, accepted) — C1.5 writes `localisation.md`'s line naming the reset email's second
  home; its finding file is the lead's (U10). The web halves of 83, 89 (D6.5), 106 (D5.10), 158 (D6.4) are other
  lanes': write a finding's *Resolution* only when your commit finishes it (17, 21, 69, 77, 78, 79, 91, 92, 93); for
  32, 83, 89, 106, 158 leave the file to the web lane that finishes it, and say so.
- **Shared files:** `apps/api/src/app.ts` — your two sweep jobs and the successor key in their own block (lane A2 adds
  the reclaim job beside them; the lead joins both). `docs/api/api-contract.md` — only the sections of your routes
  (*Session*, *Me*, *Staff (managed)*, *Owners (the admin)*, *Users (the admin)*, *Spaces (the admin)* › `status`,
  *Internal*'s two sweep lines). `packages/shared/src/{auth,users,audit,space-links}/*` are yours (§9.3); never
  `core/*` (the lead's). `docs/backend/security.md` is yours; `docs/architecture/data-model.md` › *Operations* yours
  (lane A2 edits other parts).
- **Note on C1.9 (158):** if the web imports the second schema (`ADMIN_SPACES_STATUSES` / `adminSpacesListQuerySchema`)
  anywhere, move that import to the one schema in your commit (an import change only — say it in your reply).
- **Done:** all 17 commits; then the lane's heavy checks (§4 of the common file): lint, typecheck, `test:unit` of
  `@masaha/shared`, `@masaha/api` and `@masaha/web` (the shared types reach the web), and the whole `test:api` on
  `masaha_a_lane_a1_test`. Reply DONE (§9).
