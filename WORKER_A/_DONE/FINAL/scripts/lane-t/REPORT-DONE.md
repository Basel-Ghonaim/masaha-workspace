# Lane T — the final report (returned as text; saved by the lead)

Lane T · DONE · Branch lane/t head 5957dd65 (C4.1 rebased by the lead onto 56e639c6 → 4550b5b2).

**FIRST (blocks CI, not lane T's):** a fresh production build of the joined branch fails check:build's
showcase-strings rule: lane L's chart fixtures (`a5747df7`) hold single words the build's libraries also write — the
month ticks يوليو, أغسطس, سبتمبر, Jul, Aug, Oct (date-fns, in the calendar chunk) and ILS (the priceText chunk):
"7 showcase string(s) in the build", exit 1. Every lane-T rule passes on that build. Recorded as finding 206.

Commits: 4550b5b2 build(web): serve the site's parts by their entry (49) · afaa7466 build(web): keep dashboard-only
code acyclic (44) · 50b9aa5c test(web): load the lazy shells before waiting (46) · 07427eaa build(db): hold the test
database's script inline (49) · 111d5a04 docs: settle the capability documents' size (43) · 5957dd65 docs: record
finding 206 (24).

Red/green: C4.1 as in the hand-over (`REPORT.md`). C4.2 — T96 red against stubs, 4 failed (dashboardCycleProblems ›
"refuses a chunk the dashboard imports that imports it back", "refuses a cycle closed deeper down": expected [] to
deeply equal [Array(1)]; isDashboardShared › "takes a module only dashboard code imports…", "holds a cycle of such
modules…": expected false to be true) + "names the chunk of what only the dashboard imports when the first download
imports it" red; green scripts/ 9 files / 169. T97 red before the group: check:build exit 1 ("…AnnouncementsPage.tsx
imports the dashboard chunk (_dashboard-DH2j8ltA.js), which imports it.", same for SettingsPage.tsx); green after: "No
dashboard code in the site's first download, and no chunk the dashboard imports imports it back." (a dashboard-shared
chunk of 77.8 kB). C4.3 — T100 red against a warm() that does not await ("awaits every loader once" [false,false] ≠
[true,true]; "fails when a loader fails" resolved instead of rejecting); routeLoaders red against a stub; green 5/5;
the six route files 6 / 111. **Measured: SiteLayout's first test 369 ms (3,814 cold before); App's "renders the main
landmark" 624 ms.** C4.4 — no test; `docker compose config` from lane-t and from an unrelated `--project-directory`
identical, no folder path; vs C:\dev\masaha\app's, only the bind of `docker/postgres/create-test-database.sql`
replaced by the inline config (`lane-t/c44-config-*.txt`); never `db:up`/`up`/`down`. C4.5 docs only.

Breaks: B96, B100 = the stubs' reds; B97 = the red check:build without the group; B98, B99 = C4.1's reds.

Heavy checks (grant log): unit web 2026-10-30 14:11:42–14:12:26 exit 0, 164 files / 1113 · component whole 2026-10-31
07:53:53–08:06:46 exit 1, 5 files failed | 303 passed, 6 tests failed | 1780 passed (≈ 30 min memory wait first) —
5 "Test timed out in 5000ms" under load (LocationStatus, SpaceEditor › leaving the editor, UsersPage › link dialog,
dashboard routes › add-space, authPages › RequireGuest landing) and dashboard routes › "moves to another space from
the switcher" (read the nav before it updated); the 5 files re-run together and alone: 5 / 129 green
(`final-rerun.txt`) · lint 08:06:49–08:11:53 exit 0 · typecheck 08:11:54–08:13:20 exit 0 · production builds all exit
0 (C4.1 red 10-29 15:53, green 16:01; C4.2 10-30 13:04; its check:build `lane-t/c42-checkbuild.txt` exit 1 only on 206)
· check:classes 1710 files clean · check:links 3134.

Shared files: eslint.config.js (C4.1) · vite.config.ts (the dashboard-shared group, last, a `name` function with
getModuleInfo via isDashboardShared) · checkBuild.ts (sitePageProblems, dashboardCycleProblems, dashboard-shared
counted as dashboard code in the first-download rule) · dashboardOnly.ts (isDashboardShared, ModuleGraph,
DASHBOARD_SHARED_CHUNK) · architecture.md (header, §1 sentence, §3 build bullet, §3 public entry paragraph) ·
setup.md (check:build row, *Database*, *Running a second folder* with the one-time recreation EC7, Last Updated) ·
testing.md §3 rule 8 (the warm-up) · documentation.md §5 (OD4's text) · data-reports.md, announcements.md code maps ·
the six route test files (imports and one top-level beforeAll each).

Findings closed: 180 (C4.1), 27 (C4.2), 55, 87 (C4.3), 48 (C4.4), 98 (C4.5). Opened: 206 (Open).

Decisions (none SERIOUS): LT-D1–D5 as in the hand-over · LT-D6 (EC5) the dashboard-shared group takes any module that
is not dashboard code, has no lazy importer, and whose every chain of static importers ends in dashboard code
(Rolldown's getModuleInfo), placed last — the plan's named modules already had chunks; the real cycle ran through
@masaha/shared's space-settings schemas and announcements' dashboard parts · LT-D7 check:build refuses the
dashboard-shared chunk in the first download too · LT-D8 `apps/web/src/test/warmLazy.ts` (beside the test helpers) +
`routeLoaders(routes, path)` (lint refuses app/ a page's file) · LT-D9 the dashboard routes file warms all 28 lazy
modules; the site files their shells and the pages they open; each beforeAll 60 s; no test timeout raised · LT-D10 the
warm-up note in testing.md §3 (setup.md has no *Tests* section) · LT-D11 documents dated 2026-10-29.

Notes: EC7 is the owner's one-time step (setup.md › *Running a second folder*: the next `db:up` recreates the
container once; the volume stays); 55's resolution: the CI run's slowest route file goes in the PR's report (the
lead's).
