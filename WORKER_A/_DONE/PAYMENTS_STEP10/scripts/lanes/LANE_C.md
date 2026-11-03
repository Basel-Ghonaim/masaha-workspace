# Lane C — the user's side (the plan's PR 4a and 4b, commits 1–5)

Read `C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\scripts\lanes\LANE_COMMON.md` whole first: it binds you.
This file adds your lane's facts.

- **Worktree:** `C:\dev\masaha\app-lane-c` · **branch:** `lane/c` (from Lane 0's `cf0dcb0c`).
- **Scripts and report folder:** `C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\scripts\lane-c\`.
- **Grant name:** `lane-c`. **Your new finding numbers, if any:** 178, 179 (168 is the plan's, yours).

## What you build

The plan's **PR 4** with A1 — **4a** = commits 1–2, **4b** = commits 3–5 — in this order on your branch at the end:

| # | Subject (§12) | §9 | §8 | §10 tests |
|---|---|---|---|---|
| 1 | `feat(data-reports): show a user's own reports` | *PR 4 · Commit 1* | PR 4 commit 1 | 59 (the page), 60–64, catalogue parity |
| 2 | `feat(data-reports): report wrong information` | *PR 4 · Commit 2* | commit 2 | 59 (201/200), 65–70 |
| 3 | `feat(design-system): add the heart icon` | *PR 4 · Commit 3* | commit 3 | 71 |
| 4 | `feat(favorites): save a space from its card` | *PR 4 · Commit 4* | commit 4 | 72–79 |
| 5 | `feat(favorites): list a user's favourite spaces` | *PR 4 · Commit 5* | commit 5 | 80, 81, 64 (the «المفضّلة» link) |

**Not yours: commit 6** (`feat(announcements): show a space's announcements`, finding 131, tests 82–84): the lead
builds it on the joined branch, since it needs lane A's `features/announcements`. Leave the space page's
announcements slot and the closure notice to it; build the space page's other slots (the report, the heart) so a
later slot can be **added** beside them in U8's order (test 84's order is then the lead's to finish).

Plan line ranges: §2 PR 4 scope 115–130, AC 194–212; §6 (findings 131, 168); §7 PR 4 682–729; §8 PR 4 812–852 and
*Shared with the other items* 854–874; §9 PR 4 1356–1524 (1525–1541 is commit 6, read it to leave room for it);
§10 PR 4 1623–1653 and *Review Focus*; §11 1685–1688; §13 checks 3 (PR 4), 5.j, 5.m, 5.n, 5.o (5.k is the lead's).
**Check 3's public fix PR has not merged:** `git diff --name-status e6737da5 HEAD -- apps/web/src/pages/site
apps/web/src/features/directory` is empty — the site's code is as the plan read it.

**Your documents:** `docs/features/data-reports.md` (the user's side), `users.md`, `directory.md`, `favorites.md`
(*Web* parts, S16), `docs/frontend/architecture.md` §2 (`AccountLayout` built) and §7 (S13's line),
`docs/project/overview.md`, `docs/frontend/design-system/foundation.md` §13 screen 11's line («ردّ فريق مساحة» →
«ردّ فريقنا», approved) and the icon list if it names icons; finding 168 (new, the plan's words; the heart's line added
in commit 4) and its index line.

## The order of work (lane B's commit 2 comes first)

Your commits 1–2 extend `features/data-reports`, which **lane B creates in its commit 2** (its repository,
`hooks/queryKeys.ts`, `index.ts`, copy `dataReports.ts`). You must not create those files yourself.

1. **Phase 1 (now):** read everything of §2 above and the site's code you will change (`pages/site/**`,
   `features/directory/**`, `features/users/**`'s account menu, `shared/routing`'s `RequireAuth`, the directory's
   near-me store). Build **commit 3** (the heart icon — design-system only) on `lane/c`, with its test and break, lint
   and typecheck through the grant. Then **end your turn** with the reply marked `HAND-OVER: waiting for lane B's
   commit 2`, saying what you read and any decision already taken.
2. **Phase 2 (when the lead continues you with lane B's commit-2 sha `<B2>`):** `lane/b` is in the same repository.
   Move your branch onto it: `git rebase --onto <B2> cf0dcb0c lane/c` (your heart commit then sits on lane B's
   commit 2; it touches no file of theirs). Then build commits 1, 2, 4, 5 in that order. Before the heavy checks, put
   your commits in the plan's order — 1, 2, 3 (heart), 4, 5 — with a scripted interactive rebase
   (`GIT_SEQUENCE_EDITOR="python <your script>" git rebase -i <B2>`, the script moving the heart's `pick` line after
   commit 2's); check every subject and that each commit's tree still typechecks only if a later commit depends on
   an earlier (the heart is used from commit 4 on, so it stays before 4).
3. Lane B builds its commit 3 (the admin's list) meanwhile on its own branch: it also adds to the data-reports
   repository, keys, `index.ts` and copy. **Add your parts as separate lines/entries** (the user's reports beside the
   owner's), never reorder theirs, so the lead's join keeps both sides.

## Files

**Yours:** `features/data-reports`' user side (`ReportAction`, `ReportDialog`, `MyReportsList`, `MyReportCard`, the
`hooks/mine/*`, `hooks/report/*`, `hooks/intent/*`, and your additions to its repository, keys, `index.ts`, copy);
`features/favorites/**` (new); `features/directory/**` (the saved ids, the slots, `FavoritesView`); `features/users`'
account menu; `shared/design-system/icons/**` (the heart) and the layer's `index.ts` only if it re-exports icons by
name (your line); `pages/site/**` (`public/SignInPrompt.tsx`, `account/**`, `routes.tsx`, `navigation.ts`, the shell's
header and menu, `SiteLayout`, the Directory, Home and space pages); `app/pageTitles.unit.test.ts` if it lists routes
by hand; copy `favorites.ts` (new), `site.ts`, `users.ts`, `directory.ts` and your part of `dataReports.ts`; the
documents above.
**Shared (your own lines only):** copy `{english,arabic}/index.ts` (`favorites`, alphabetical: after `errors`),
`dataReports.ts` (lane B's file: add your sections), the data-reports repository/keys/`index.ts` (lane B's files: add
yours), `architecture.md`, `overview.md`, `foundation.md`, the findings index.
**Not yours (never edit):** `features/announcements/**` (lane A), `pages/dashboard/**`, lane B's owner/admin parts
of `features/data-reports`, `features/space-links`, `shared/design-system/components/display/FilterTag`, copy
`announcements.ts`, `spaceLinks.ts`, any `errors.ts`.

## When you end

1. After phase 1: the hand-over above.
2. After phase 2: commits 1–5 in the plan's order; the heavy checks of LANE_COMMON §4 (lint, typecheck, the two full
   web lanes) through the grant, all green; the reply marked **DONE**. If the lead later sends you fixes, fold them
   into their commits and re-run what they touched and the lane they failed in.
