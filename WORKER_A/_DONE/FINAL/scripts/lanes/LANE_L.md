# Lane L — U3: the layer and the web's shared modules

Read `LANE_COMMON.md` (same folder) first and follow it; this file adds your lane's facts.

- **Worktree** `C:\dev\masaha\app-lane-l`, **branch** `lane/l`, **base** `37a84e65` (= `origin/main` `ce671b37` + the
  lead's C0.1 and C0.2, which touch the error envelope and the errors catalogue only). The lead builds the rest of the
  foundation (U0: the dashboard's navigation and shells, the skip link, the account menu, the route stubs, the copy's
  three new sections) on `feat/final` meanwhile; **none of your files is U0's**, and the lead rebases your branch at
  the join. Do not touch U0's files: `pages/dashboard/{routes.tsx,navigation.ts,shell/*}`,
  `pages/site/{routes.tsx,navigation.ts,shell/*}`, `shared/routing/*`, the copy's `index.ts`/`shape.ts`,
  `copy/*/{dashboard,users,site,errors}.ts`, `features/users/*`.
- **Scripts folder:** `C:\dev\masaha\workspace\WORKER_A\FINAL\scripts\lane-l\`. **Finding numbers:** 204–205.
- **The plan's parts for you** (`2_PLAN.md` lines): §5.3 **860–934** (D3.1–D3.11); §8 U3 **2073–2085**; §9.1 U3
  **2205–2215** (C3.1–C3.10, in that order); §10.4 T79–T95 (**2485–2501**); §12.1 U3 **2793–2795**; §7's rows for
  73, 103, 104, 105, 132 (**1947–2018**; write a *Resolution* only where your commit finishes the finding — 103, 104,
  132; 73 and 105 close with lanes W1/W2's consumers: leave their files and say so); DI4 (1885); EC4 (2881). The
  foundation's §12 (`docs/frontend/design-system/foundation.md`) rows your components add are yours.
- **Your lane's order matters to the others:** lanes W1 (overview, finance), W3 (desk) and W4 (site) build on your
  components. Build in the plan's order; every commit whole and green on its own.
- **C3.9** moves `pages/dashboard/admin/useRowTriggers.ts` to `shared/lists/hooks/useRowTriggers.ts` and deletes
  `features/staff/hooks/menu/useMenuTriggers.ts`: you update their consumers' imports (the users page, the staff list)
  in the same commit — the only change you make in those files.
- **C3.10** changes `packages/shared/src/space-settings/reminderTemplate.ts` (`fillReminder`, §9.3's one exception)
  and `features/space-settings/services/reminderPreview.ts`.
- **Done:** all 10 commits; then lint, typecheck, `test:unit -w @masaha/web`, `test:unit -w @masaha/shared` (if you
  touched it), `test:component -w @masaha/web` (whole), `npm run check:classes`. Reply DONE (§9).
