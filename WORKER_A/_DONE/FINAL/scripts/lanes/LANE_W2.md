# Lane W2 — U6: the admin's screens, both audit logs, the platform settings, the report notice

Read `LANE_COMMON.md` and `LANE_W_COMMON.md` (same folder) first and follow them; this file adds your lane's facts.

- **Worktree** `C:\dev\masaha\app-lane-w2`, **branch** `lane/w2`, **base** `4550b5b2` (U0 + the lanes joined: lane L (U3 whole) and lane T's C4.1 (the `public.ts` entries)).
- **Scripts folder:** `C:\dev\masaha\workspace\WORKER_A\FINAL\scripts\lane-w2\`. **Finding numbers:** 210–211.
- **The plan's parts for you** (`2_PLAN.md` lines): §5.6 **1255–1492** (D6.1–D6.15); §8 U6 **2102–2117**; §9.1 U6
  **2238–2255** (C6.1–C6.17); §10.4 T150–T190 (**2549–2590**); §12.1 U6 **2802–2803**; §4.1's rows 4 (G4.1), 20, 21
  (G21.3), 23, O13, 26–32 (**311–352**); §7's rows for 14, 73 (with L), 74, 83, 89, 94, 95, 99, 104/105 (the admin
  side), 158, 184 (**1947–2018**); DI1, DI17, DI18, DI30, DI31 (**1874–1943**); EC12 (the audit's stored fields),
  EC18–EC22 (2871–2929). Read `docs/api/api-contract.md` › *Audit log*, *Platform settings*, *Data reports*,
  *Spaces (the admin)*, *Owners (the admin)*, *Users (the admin)*, and `docs/features/{audit,platform-settings}.md`.
- **Your files:** §8 U6 (2102–2117), the stub pages `pages/dashboard/{space,admin}/audit/AuditPage.tsx` and
  `pages/dashboard/admin/settings/SettingsPage.tsx` (replace their bodies), copy
  `{audit,platformSettings,spaceLinks,spaces,dataReports,lookups}.ts` (both languages; `dataReports.ts` — your own
  sub-objects only), the prototype `docs/design/prototype/Admin space edit.html` and its row in
  `docs/design/CHANGES.md` (74; then run `node docs/design/scripts/check-parse.mjs` and `check-classes.mjs`).
  `features/platform-settings/public.ts` and `features/data-reports/public.ts` exist (lane T's C4.1, in your base):
  the site's parts live there; the dashboard's in `index.ts`.
- **What each commit needs from other lanes** (build those whose needs are in your base first):
  - C6.1, C6.2, C6.3, C6.4 — lane T's C4.1 (in your base). C6.8, C6.9, C6.11, C6.12, C6.13, C6.14 — none beyond your
    base (check the fields they read exist on `main`: `AdminUserRow.receptionSpaces` for C6.8; if one does not,
    record it and tell the lead). C6.5 — A1's C1.9 (`editable` in `SPACE_STATUSES`). C6.6 — A1's C1.7 (`details`
    on `ALREADY_OWNER`; the envelope's `details` is in U0). C6.7 — A1's C1.8 (`?email=`). C6.10 — A2's C2.14 (one
    report by its id). C6.15 — A2's C2.15 (`retiredAmenities`). C6.16 — L's C3.1 (`Meter`). C6.17 — L's C3.3
    (`held`), C3.9 (`useRowTriggers`).
- Reply DONE when all 17 commits are made and the lane-wide checks are green.
