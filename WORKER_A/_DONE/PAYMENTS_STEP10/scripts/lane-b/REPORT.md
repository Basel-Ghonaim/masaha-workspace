# Lane B — report (saved by the lead from the sub-agent's replies; the harness refuses a sub-agent's report file)

## Hand-over after commit 2 (2026-10-28)

- `lane/b` head `a9096f31`. Commits: `0406e833 feat(design-system): add a removable filter tag` (47) ·
  `a9096f31 feat(data-reports): decide a space's reports` (44).
- c1 red (against a stub rendering only the label, `c1-red.txt`): "Unable to find an accessible element with the role
  "button" and name "Remove the space filter"" (2 failed, 1 passed). Green: FilterTag 3/3; showcase registry 9/9.
- c2 red (code moved aside to `bak-c2-red\`, restored, `cmp`-checked): "Cannot find module './dataReportsRepository'",
  "Failed to resolve import './DecideSheet'", routes test "./space/reports/DataReportsPage". Green: unit + catalogue
  parity 18/18; component 20/20; routes 57 passed, 1 failed (not the lane's — below).
- Breaks, all red (`break-<id>.txt`, restored from `bak-break-<id>.*`): #45 name left out (3 tests + axe); #46 POST for
  PATCH; #47a time shown; #47b a wrong chip kept; #48 the reporter named; #49 one empty state; #50 reply required for
  both; #51 buttons on a decided report; #52 sheet unnamed (390, 1440); #52-focus reply not first; #53 `cardsBelow="lg"`;
  #53-leave (green at first — the refetch landed before the close; the test now holds the read until released, then
  red); #58 the placeholder kept.
- Heavy: c1 lint exit 1 (two `no-confusing-void-expression` in the showcase section), fixed, exit 0; typecheck 0. c2
  lint exit 1 (`react-hooks/immutability` on a ref prop; three needless `as HTMLElement`), fixed, exit 0; typecheck 0.
  `check:links` "2946 links in 199 documents and 2139 source files all resolve"; `check:classes` clean (1517 files);
  Prettier clean.
- Shared: copy `{english,arabic}/index.ts` (`dataReports` after `dashboard`); `routes.tsx` (`SPACE_PAGES.dataReports`
  between `customers` and `desk`); routes test (import of `../../test/dataReport`, `describe("the space's data
  reports")` before "the space's customers"); architecture §2 (a clause in the *Built so far* line — conflict expected
  with lane A); overview (the Data reports line's end); foundation §3 `display` row + §12 FilterTag row; findings index
  (8 → Resolved); `src/test/dataReport.ts` (new fixture).
- Decisions: LB-D1 FilterTag's remove `size-8` + `pointer-coarse:size-(--control-height)` (32 px, 44 on touch);
  LB-D2 foundation §3's display row lists FilterTag; LB-D3 showcase fixtures worded apart from the catalogue; LB-D4
  keys/repository hold the owner's parts only; LB-D5 two words beyond §9 (`dataReports.byline`, `sheet.close`
  «إغلاق»); LB-D6 the decision's status in the form's values (`setValue`/`useWatch`); LB-D7 the sheet's first focus by
  Radix's default (lands on the reply; an `onOpenAutoFocus` handler's break stayed green, so removed; to confirm in the
  real run); LB-D8 test 49's leave/toast proven in `SpaceReportsList.component.test.tsx`, the filters through
  `useSpaceReports`; LB-D9 focus to the count when the opened row leaves (layout-effect cleanup); LB-D10 fixture file;
  LB-D11 `toastDecided` in `components/toast/`. Check 5.i `rounded-(--radius-pill)` allowed; 5.l the profile editor has
  `#hours`, `#contacts`, `#location`, `#amenities` (PRICES → Packages & prices; OTHER → the profile).
- Problem (not the lane's): routes › "refuses reception the owner's payments with the 403 inside the shell" fails
  locally — a cold lazy load past the 3 s wait (5.6 s alone); with `routes.tsx` and its test from HEAD it fails the
  same way (`c2-routes-alone-base.txt`). Finding 55/87's family; CI judges.

## DONE (2026-10-28 ≈ 10:55)

- `lane/b` head `30d41fbb`: `0406e833` (47) · `a9096f31` (44, unchanged since the hand-over) · `30d41fbb
  feat(data-reports): list every space's reports` (46).
- c3 red (new code aside, changed code back to commit 2's, restored, `cmp`-checked, `c3_red.sh`): "…adminReports is
  not a function", "…decideAdmin is not a function", `./adminReportsQueryOf` not found; the admin sheet's lines not
  found; `AdminReportsList`, `useAdminReports`, `AdminSpaceFilter`, "./admin/DataReportsPage" not found. Green: unit
  24/24; component 35/35; routes 59/60 (the known miss).
- c3 breaks, all red: #46-admin; #47c; #54a; #54b; #51-admin; #55a (1024 and 390); #55b; #55c (green at first → test
  added "takes off the space and the field together with «Clear filters», the chip kept" → red); #56; #57; #58-admin.
- Heavy (final tree): lint 0 (10:39–10:41); typecheck 0 (10:41–10:42); `test:unit -w @masaha/web` "Test Files 147
  passed (147) · Tests 1028 passed (1028)"; `test:component -w @masaha/web` "Test Files 1 failed | 271 passed (272) ·
  Tests 1 failed | 1606 passed (1607)" (391.87 s, no kill) — the one: routes › "refuses reception the owner’s payments
  with the 403 inside the shell" 5729 ms; alone 3072 ms red. `check:links` "2957 links in 200 documents and 2155 source
  files all resolve"; `check:classes` clean (1533 files). Finding 87 timing: "lists the owner's eleven pages" 2221 ms,
  "lists reception's four pages" 283 ms.
- Shared (c3): copy `spaceLinks.choices.allSpaces`; `ADMIN_PAGES.dataReports` after `lookups`; the routes test's
  "the admin's data reports" describe; `space-links/index.ts` (`AdminSpaceFilter`); new `pages/dashboard/fieldSections.ts`;
  architecture §2 (a clause in the admin's pages); findings 167 (new) + index; `space-links.md`, `data-reports.md`.
- Decisions LB-D12–D17: the admin's space filter slot (`AdminSpaceFilterSlot`; its own Combobox over
  `useSpaceChoices({ enabled: open })`, «كل المساحات» first); `ReportListParts.tsx` (moved unchanged); the field →
  anchor map in `pages/dashboard/fieldSections.ts` (admin: `adminSpacePath(id)#…`, OTHER the editor, a verified
  space's «عرض المساحة»); the admin's 403 worded as "verified meanwhile", reports re-read, `['me']` not invalidated;
  «مسح الفلاتر» keeps the chip, «عرض الكل» clears all, the toast's «عرض» sets decided; the admin's non-admin 403 test
  uses the existing heading pattern. LB-D5 extended: `dataReports.admin.allSpaces` dropped for
  `spaceLinks.choices.allSpaces`; the admin's filter count reuses `payments.ledger.filters.applied`.
