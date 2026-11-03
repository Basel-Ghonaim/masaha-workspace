# Lane T — the sub-agent's reports (returned as text; saved by the lead)

## Hand-over 1 — C4.1

Lane T · HAND-OVER: C4.1 made · Branch lane/t head a48a236a (base f1bf19d9)

Commits: a48a236a build(web): serve the site's parts by their entry (49)

Red/green:
- T98 (`scripts/checkBuild.unit.test.ts` › sitePageProblems) written against a stub returning []: red "names a site
  page that reaches a library's chunk through its static imports" (expected [] to deeply equal [ Array(1) ]) and
  "names each library a site page reaches, deeply" (expected [] to deeply equal [ …(2) ]); after the code 18/18.
- The lint entry (new `scripts/publicEntries.unit.test.ts`): red before the eslint change — "allows the site a
  capability through its public entry" (expected [ 'page → feature (public.ts)' ] to deeply equal []), "refuses the
  site a capability's index when the capability has a public entry" (expected [] to deeply equal [ 'site →
  announcements (index.ts)' ]); after: publicEntries, dashboardOnlyRule, layerEntries 15/15.
- T99 (build), first on the old imports with the new rule: build 0, check:build 1 — "src/pages/site/account/
  MyReportsPage.tsx reaches data-table's chunk", "src/pages/site/public/space/SpacePage.tsx reaches calendar's chunk"
  (two calendar chunks), "…SpacePage.tsx reaches data-table's chunk". After: build 0, check:build 0 ("No site page
  reaches data-table or leaflet or calendar through its static imports." plus the three existing passes). Outputs
  `lane-t/c41-checkbuild-red.txt`, `c41-checkbuild-green.txt`.

Breaks: B98 = the stub's red; B99 = the red build (same import graph, before the move); the lint deny rule's break =
the second red line.

Heavy checks (UTC): production build, old imports 15:53:11–15:53:19 exit 0 · lint 15:55:25–15:58:26 exit 0 ·
typecheck 15:59:33 exit 0 · production build after 16:01:02–16:01:06 exit 0 · check:build after each: 1 then 0.
Light: prettier clean; check:links 3126 resolve; check:classes clean; SpacePage.component.test 9/9; site
routes.component.test one finding-87 miss under lint's load ("shows the Directory under its title", no main), passed
with -t, then the whole file 13/13.

Shared files: `eslint.config.js` (PUBLIC_ENTRY_CAPABILITIES read from the features with a public.ts; zoneEntries allow
a feature's public.ts; one site → feature index.ts deny policy for those capabilities); `docs/frontend/architecture.md`
(header line; Last Updated; §1 dependency rule sentence; "(a capability's public.ts aside, §3)"; §3 new paragraph "A
capability's public entry" with its two checks); `docs/features/{data-reports,announcements}.md` (Web code map names
both entries).

Findings closed: 180 (status Resolved, *Resolution (2026-10-29, #PRNUM)*); index untouched.

Decisions (none SERIOUS): LT-D1 (EC14) no Leaflet allowance — every site page refused all three library chunks
(shared/map loads Leaflet only by dynamic import; the red build showed none statically) · LT-D2 lint also refuses the
site a capability's index.ts when it has a public.ts · LT-D3 `platform-settings/index.ts` is `export {};` until U6
fills it · LT-D4 two production builds for C4.1 (red and green, S9) · LT-D5 two feature code-map lines edited outside
§12.1's list (they had become false).

Notes: W2 and W4 import the site's pieces from `@features/{data-reports,announcements,platform-settings}/public`;
U6's `usePlatformContact` belongs in `platform-settings/public.ts`.

**Lead's join:** rebased onto `56e639c6` (no conflict) → `4550b5b2`; typecheck 0, lint 0; `scripts` unit 159/159;
component (space page, account, data-reports, announcements, platform-settings) 26 files / 134 tests; ff.
