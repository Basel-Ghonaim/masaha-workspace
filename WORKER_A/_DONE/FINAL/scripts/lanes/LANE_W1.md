# Lane W1 — U5: the owner's screens — the two overviews, finance, and the owner's gaps

Read `LANE_COMMON.md` and `LANE_W_COMMON.md` (same folder) first and follow them; this file adds your lane's facts.

- **Worktree** `C:\dev\masaha\app-lane-w1`, **branch** `lane/w1`, **base** `56e639c6` (U0 + the lanes joined: lane L (U3, all ten commits and finding 204)).
- **Scripts folder:** `C:\dev\masaha\workspace\WORKER_A\FINAL\scripts\lane-w1\`. **Finding numbers:** 208–209.
- **The plan's parts for you** (`2_PLAN.md` lines): §5.5 **987–1253** (D5.1–D5.11); §8 U5 **2093–2100**; §9.1 U5
  **2225–2236** (C5.1–C5.11); §10.4 T110–T146 (**2507–2548**); §12.1 U5 **2799–2801**; §4.1's rows 12, 19, 21, 22,
  24, 25 (**311–352**); §7's rows for 102, 105 (with lane L), 106 (web half), 73's meter use (**1947–2018**); DI2, DI3,
  DI5–DI9, DI15, DI16, DI26, DI28, DI29 (**1874–1943**); EC16, EC17 (2871–2929). The API answers you read are on
  `main` already (#131: `GET …/overview`, `GET /admin/overview`, `GET …/finance/{income,debts,payers,occupancy}`) —
  read `docs/api/api-contract.md` › *Overview*, *Finance*, and `docs/features/{overview,finance}.md` first.
- **Your files** (§8 U5): `features/overview/**`, `features/finance/**` (new), the stub pages
  `pages/dashboard/space/{overview,finance}/…Page.tsx` and `pages/dashboard/admin/overview/OverviewPage.tsx` (replace
  their bodies), `features/staff/**`, `pages/dashboard/space/{StaffPage,SettingsPage,PackagesPage}.tsx`,
  `features/packages/components/{list/PackageRow,sheet/PackageSheet}.tsx`,
  `features/space-settings/components/reminder/ReminderCard.tsx`, copy `{overview,finance,staff,packages,spaceSettings}.ts`
  (both languages), `docs/features/{overview,finance,space-links,space-settings,packages}.md`.
- **What each commit needs from other lanes** (build those whose needs are in your base first):
  - C5.1 — lane L's C3.1 (`Meter`). C5.2 — none beyond U0 (`editable` in the spaces list's address is lane A1's C1.9
    and W2's D6.4: the link is just an address — write it). C5.3 — L's C3.2 (`BarChart`), C3.5 (range), C3.10 (csv).
    C5.4 — L's C3.5, C3.10 (`fillReminder`, `whatsappLink`, csv). C5.5 — L's C3.2 (`Heatmap`), C3.10.
    C5.6 — A1's C1.12 (`StaffMember.addedAt`). C5.7, C5.8, C5.9 — none. C5.10 — A1's C1.11 (`ACCOUNT_IS_ADMIN` on the
    re-issue). C5.11 — L's C3.3 (`held`), C3.9 (`useRowTriggers`).
- **Finding 105** closes when both C5.11 and lane W2's C6.17 are made: write its *Resolution* only if your lane file's
  base already holds C6.17; else say so in your reply (the lead writes it at the join).
- Reply DONE when all 11 commits are made and the lane-wide checks are green.
