# Lane T — U4: the build and the tooling

Read `LANE_COMMON.md` (same folder) first and follow it; this file adds your lane's facts.

- **Worktree** `C:\dev\masaha\app-lane-t`, **branch** `lane/t`, **base** `f1bf19d9` (the foundation U0 whole on
  `feat/final`: C0.1–C0.6 — the error envelope's `details`, the new error code, the grouped navigation, the skip link,
  the account on a phone, the routes of every screen still to come).
- **Scripts folder:** `C:\dev\masaha\workspace\WORKER_A\FINAL\scripts\lane-t\`. **Finding numbers:** 206–207.
- **The plan's parts for you** (`2_PLAN.md` lines): §5.4 **936–985** (D4.1–D4.5); §8 U4 **2087–2091**; §9.1 U4
  **2217–2223** (C4.1–C4.5); §10.4 T96–T100 (**2502–2506**); §12.1 U4 **2796–2798**; §7's rows for 27, 48, 55, 87,
  98, 180 (**1947–2018**); OD4, OD8 (2830–2867); EC5, EC6, EC7, EC14, EC15 (2871–2929); the carried item 11's test
  part (lines 200–214: the slow tests finding 87 names).
- **Hand-over after C4.1.** Build **C4.1 first** (the `public.ts` entries of `data-reports`, `announcements`,
  `platform-settings`; the site's imports moved to them; the lint boundary; `check:build`'s site rule and its unit
  test), make it green (its tests, lint, typecheck through the grant), commit, and **end your turn with a HAND-OVER
  reply** (§9, "HAND-OVER: C4.1 made"). The lead joins it into `feat/final` at once (lanes W2 and W4 build on it),
  then continues you with a message; you then build C4.2–C4.5 on your branch as it is (do not rebase unless the
  lead's message says so).
- **C4.2/C4.3/C4.1's `check:build` rules** need a production build to prove (T97, T99): a build is heavy — through
  the grant, `NODE_ENV=production npm run build -w @masaha/web` (the web's `.env` sets `NODE_ENV=development`;
  production must be set for the build), then `npm run check:build`. Run it once for C4.1 and once for C4.2. Record
  the outputs. EC5's time box is two hours; if it fails, follow EC5's fallback and record it.
- **C4.4 (D4.4, finding 48) — LEAD-D3:** the database container is shared by every lane and by worker B; **never run
  `npm run db:up`, `docker compose up`, `down`, or anything that recreates or stops the container.** Prove the change
  by `docker compose config` alone (read-only) from your worktree (and compare with `C:\dev\masaha\app`'s output
  read-only, `docker compose -f C:/dev/masaha/app/docker-compose.yml config` is allowed); the recreation (EC7) is
  left to the owner, named in `setup.md` as the one-time step it is. Record it.
- **C4.3 (D4.3)** edits the six route test files' set-up only (a `beforeAll` warm-up); other lanes add tests to some of
  them — keep your change to the imports and the `beforeAll`, so the joins meet small hunks.
- **C4.5 (OD4 (b))** revises `docs/architecture/documentation.md` §5 with OD4's sentence; finding 98's file
  `Resolved` in that commit.
- **Done:** all 5 commits; then lint, typecheck, `test:unit -w @masaha/web`, `test:component -w @masaha/web` (whole),
  `npm run check:classes`, `npm run check:links`. Reply DONE (§9), with the build and `check:build` outputs.
