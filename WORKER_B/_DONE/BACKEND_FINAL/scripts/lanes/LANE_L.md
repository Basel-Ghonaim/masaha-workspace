# Lane L — the API items left (C12–C15)

- **Worktree:** `C:\dev\masaha\app-b-lane-l` · **branch:** `lane/l` (already checked out) · **base:** `a2f0d8ed`
  (`origin/main` `d40d20f5` + the lead's C1–C3) · **test database:** `masaha_b_lane_l_test` (set in the worktree's
  `apps/api/.env`, migrated) · **scripts folder:** `C:\dev\masaha\workspace\WORKER_B\BACKEND_FINAL\scripts\lane-l\`
  (create it) · **grant tag:** `lane-l` · **finding numbers:** 156 (then ask nothing: use 190, 191 and say so).
- The rules: `LANE_COMMON.md` (beside this file) — read it first, whole.

## What you build — four commits, in this order, each with its tests, breaks and documents

The owner's approval (the plan's top note) puts **all four in**: OD5 (170) in, OD6 (`/me`) in, OD7 (a) — the owner any
range ≤ the payments list's bound, reception today only —, OD8 (167) in (#129 merged).

| # | Subject (exact) | Plan sections |
|---|---|---|
| C12 | `fix(sessions): read a family's latest activity` | §4.3 L7; D32; T-L5, B-L5; §6 (170); §11.1 item 7 |
| C13 | `feat(users): read and edit one's own account` | §4.3 L8; D33; EC12; T-L6–T-L8, B-L6–B-L8; §11.1 items 1 (*Me*), 5 (`users.md`) |
| C14 | `feat(data-reports): filter by who handles them` | §4.3 L10; D35; T-L9, B-L9; §11.1 items 1 (*Data reports*), 7 (167) |
| C15 | `feat(visits): list a space's visits by day` | §4.3 L9; D34; EC13; T-L10–T-L12, B-L10–B-L12; §11.1 items 1 (*Front desk*), 5 (`visits.md`), 7 (161) |

Read also the plan's §1 (header), §3.3 (AC-L5–AC-L8), §5.1's *Left items* table and mounts, §8.1, §8.3, §9.6, §9.7.

## Specifics the lead fixes for you

- **C14's helper — write it exactly as below** (lane O writes the same text in the same place for its `openCounts`, so
  the join merges cleanly): in `apps/api/src/modules/data-reports/data-reports.repository.ts`, **directly after the
  `statusWhere` function** and before `const NEWEST_FIRST`:

  ```ts
  /** Who handles a report, as a condition: the admin an unverified space's, its owners a verified one's. */
  function handledByWhere(
    verifiedIds: readonly number[],
    handledBy: 'ADMIN' | 'OWNER' | undefined,
  ): Prisma.DataReportWhereInput {
    if (handledBy === 'ADMIN') return { spaceId: { notIn: [...verifiedIds] } };
    if (handledBy === 'OWNER') return { spaceId: { in: [...verifiedIds] } };
    return {};
  }
  ```

  (one blank line before and after it). `pageAll` takes the verified ids and `handledBy` and spreads
  `handledByWhere(...)` into its `where`; the service reads `spaceLinks.verifiedSpaceIds()` only when `handledBy` is
  given. The shared `adminReportsQuerySchema` gains `handledBy: z.enum(['ADMIN', 'OWNER']).optional()` (export the
  values as a `const` array beside the other report constants if the shared file's style does).
- **C13:** EC12 decides the audit action. If none exists for a name/language change, add `user.profileEdited` to the
  shared `AUDIT_ACTIONS` and **not** to the admin's allowlist (`PLATFORM_ACCOUNT_ACTIONS`), as D33 says — check
  `docs/backend/conventions.md` §6 and the audit's tests for what adding an action requires. `/me` is mounted in the
  existing `users` router per EC12 (no `app.ts` change if the router is already mounted; if a new mount line in
  `app.ts` is unavoidable, it is **one line**, and say exactly which in your reply).
- **C15:** the range rule reuses the payments list's (`paymentsWindow` / its shared schema — EC13); reception with a
  range is `forbidden` as the payments list's own rule answers it. Visits answered as `DeskVisit` through
  `visits.deskVisitsOf`. No `app.ts` change (the visits manage router exists).
- **Shared files you may touch, only your own lines:** `docs/api/api-contract.md` (your sections: *Me* — create it
  where the contract's section list places account routes, and list it in the contract's section list if it has one;
  the *Front desk (managed)* visits list; *Data reports* `handledBy`); `docs/architecture/findings/README.md` (170,
  167, 161 moved to *Resolved* each in its commit, by number order); `packages/shared` (`users/requests.ts`,
  `visits/requests.ts`, `data-reports` requests, `audit/actions.ts` — your additions only).
- **Never touch:** `apps/api/src/app.ts` (beyond the one line above, if unavoidable), `payments`, `finance`,
  `overview`, `can.ts`, `gazaTime.ts`, `conventions.md`, `docs/plans/v1-mvp.md`, `docs/project/overview.md`,
  `docs/README.md` (the lead's C16 writes those from your notes).
- Each finding resolved: its status line `Resolved`, a `**Resolution (2026-10-29, #PRNUM):** …` line at its end, its
  index line moved under *Resolved* in number order.

## Tell the lead in your reply (beside LANE_COMMON's list)

- For C16: the v1-mvp rows to mark built (`/me`, `GET …/visits`), and anything else of `v1-mvp.md`,
  `docs/project/overview.md` or `docs/README.md` your commits make untrue.
- Whether the race test of C12 (T-L5) needed anything from `test/locks.ts` that it lacks.
