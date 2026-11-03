# Lane B — data reports (the plan's PR 3, commits 1–3)

Read `C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\scripts\lanes\LANE_COMMON.md` whole first: it binds you.
This file adds your lane's facts.

- **Worktree:** `C:\dev\masaha\app-lane-b` · **branch:** `lane/b` (from Lane 0's `cf0dcb0c`).
- **Scripts and report folder:** `C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\scripts\lane-b\`.
- **Grant name:** `lane-b`. **Your new finding numbers, if any:** 176, 177 (167 is the plan's, yours).

## What you build

The plan's **PR 3 — data reports (screens 23, 28)**, its three commits in order, each atomic:

| # | Subject (§12) | §9 | §8 | §10 tests |
|---|---|---|---|---|
| 1 | `feat(design-system): add a removable filter tag` | *PR 3 · Commit 1* | PR 3 commit 1 | 45 |
| 2 | `feat(data-reports): decide a space's reports` | *PR 3 · Commit 2* | commit 2 | 46–53, 58 (the owner's half), catalogue parity |
| 3 | `feat(data-reports): list every space's reports` | *PR 3 · Commit 3* | commit 3 | 54–57, 58 (the admin's half) |

Plan line ranges: §2 PR 3 scope 106–113, AC 180–192; §6 (findings 8, 150, 167, 87); §7 PR 3 651–681; §8 PR 3
790–810; §9 PR 3 1249–1355; §10 PR 3 1605–1622, Review Focus 1654–1669; §11 1681–1684; §13 checks 5.i, 5.l (5.k is
the lead's, after the build).

**Your documents:** `docs/frontend/design-system/foundation.md` §12 (`FilterTag`'s row; §3's category table already
names the tag's category), finding 8 → *Resolved* (with its *Resolution* line) and the findings index; finding 150
(evidence line); finding 167 (new, the plan's words) and its index line; `docs/features/data-reports.md` (*Web*
parts, S16), `space-links.md` (one *Who uses it* line), `docs/frontend/architecture.md` §2, `docs/project/overview.md`.
Finding 87: record in your report the routes test's time after `AdminSpaceFilter` joins `space-links`' index.

## The hand-over after commit 2 (lane C waits on it)

Lane C's PR 4a extends your `features/data-reports` (its repository, keys, `index.ts`, copy `dataReports.ts`), so it
cannot start its part until your commit 2 exists. **Build commit 1, then commit 2 first and quickly** (its touched
tests, red first, its breaks, lint and typecheck through the grant), **then end your turn** with the reply marked
`HAND-OVER: commit 2 ready` and its sha. Do not start commit 3 before the lead continues you. Design commit 2's
repository, query keys, `index.ts` and copy section so another commit can **add** to them (one export per line, the
admin's and the user's parts later added beside the owner's).

## Files

**Yours:** `apps/web/src/shared/design-system/components/display/FilterTag/**` (new) and the layer's `index.ts`
(your one export line, alphabetical), `apps/web/src/pages/showcase/sections/display/FilterTagSection.tsx` (new),
`pages/showcase/registry.tsx` (your entry), `pages/showcase/fixtures.json` only if the section reads words there;
`apps/web/src/features/data-reports/**` (new), `features/space-links/components/admin-filter/**` (new) and
`features/space-links/index.ts` (your export); `pages/dashboard/space/reports/**`, `pages/dashboard/admin/DataReportsPage.tsx`
(new); copy `{english,arabic}/dataReports.ts` (new), `{english,arabic}/spaceLinks.ts` (`spaceLinks.choices`, one
line); the documents above.
**Shared (your own lines only):** `pages/dashboard/routes.tsx` (`SPACE_PAGES.dataReports`, `ADMIN_PAGES.dataReports`),
`pages/dashboard/routes.component.test.tsx` (your tests in their own `it`s), copy `{english,arabic}/index.ts`
(`dataReports`, alphabetical: after `dashboard`), `architecture.md`, `overview.md`, `foundation.md`, the findings
index.
**Not yours (never edit):** `features/announcements`, `features/favorites`, `features/directory`, `features/users`,
`pages/site/**`, `shared/design-system/icons/**` (lane C's heart), copy `announcements.ts`, `favorites.ts`, `site.ts`,
`users.ts`, any `errors.ts`; and the parts of `features/data-reports` that are PR 4's (`ReportAction`,
`MyReportsList`, the report dialog, the guest's intent — lane C's).

## When you end

1. After commit 2: the hand-over above.
2. Continued by the lead: commit 3; then the heavy checks of LANE_COMMON §4 (lint, typecheck, the two full web
   lanes), all green; end with the reply marked **DONE**. If the lead later sends you fixes, fold them into their
   commits and re-run what they touched and the lane they failed in.
