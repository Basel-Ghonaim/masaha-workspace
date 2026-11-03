# Lane C — report (saved by the lead from the sub-agent's reply; the harness refused the sub-agent's own Write)

## Phase 1 (2026-10-28) — HAND-OVER: waiting for lane B's commit 2

- Branch `lane/c` head `f837a282` — `feat(design-system): add the heart icon` (39).
- Red: `Icon.component.test.tsx` "TypeError: Cannot read properties of undefined (reading 'name')" (`HeartIcon` not
  exported), "Test Files 1 failed (1)" (`c3-red.txt`); an earlier failure (an apostrophe in a title broke the
  transform) not counted. Green: `src/shared/design-system/icons` "Test Files 2 passed (2) · Tests 55 passed (55)".
- Break #71 (`mirror` on `HeartIcon`, backup `bak-c3-iconSet.tsx`, restored by copy): RED "× never mirrors HeartIcon",
  "× draws the heart, filled by the class it is given, never mirrored" — "Tests 2 failed | 45 passed (47)".
- Heavy: `npm run lint` exit 0 (grant 09:45:51–09:47:39); `npm run typecheck` exit 0 (09:47:44–09:48:18). Prettier
  on the 5 files clean; `check:classes` "No physical direction or arbitrary-value classes in 1487 files."
- Shared: the layer's `index.ts` (`HeartIcon`, one line); `pages/showcase/sections/icons/IconsSection.tsx` (2 lines).
- Checks: 3 (site code as the plan read it); 5.j `fill-current` allowed; 5.m `unwrap` + `response.status` for
  201/200, `RequireAuth` → `/login?next=`, register keeps `next`; 5.n near-me store enough (note: `useNearMe().clear`
  does not drop `['me','favorites',{near}]`); 5.o `pageTitles.unit.test.ts` walks the routes (no change).
- Gaps for phase 2: `SpacePageView.header` has no `id` and its `verified` is a word — the view will carry both.
- Decisions: LC-D1 `HeartIcon` added to the showcase's icon list (undo: drop the 2 lines); LC-D2 no document in
  commit 3 (foundation has no icon list); LC-D3 the report returned as text (harness refusal), saved here by the lead.

## Phase 2 — DONE (2026-10-28 ≈ 11:50)

- `lane/c` head `b8f70b7d` on lane B's `a9096f31`: `15dae1d1 feat(data-reports): show a user's own reports` (45) ·
  `022723db feat(data-reports): report wrong information` (44) · `76deaeef feat(design-system): add the heart icon`
  (39) · `87e94de4 feat(favorites): save a space from its card` (43) · `b8f70b7d feat(favorites): list a user's
  favourite spaces` (47). 113 files against `a9096f31`. The reorder (scripted `rebase -i --autosquash`, a fixup folded
  into c1, LC-18) met two conflicts in architecture §2's line, resolved by hand; the final tree identical to the
  pre-rebase backup.
- Red per commit (implementation moved aside, `red.py`, `red-c<n>.json`): c1 "createDataReportsRepository(...).myReports
  is not a function", ./useMyReports, ./MyReportsList unresolved, the menu's links, "Unable to find role=navigation 'My
  account'", "expected '/me/reports' to be '/login'" → unit 46/46, component 23 files/106; c2 "repository.report is not
  a function", "Cannot find module './reportIntent'", ./ReportAction, ./useReportAction, ./ReportDialog, ./SignInPrompt,
  the page's report button → unit 50, component 14/65 (+16 after LC-D8); c3 → 55/55; c4 "repository.favorites is not a
  function", './favoritesRepository', './favoriteIntent', FavoriteButton, useFavoriteToggle, useFavoriteIds, SpaceCard
  "Unable to find button 'Save Masaha Hub'", the page's heart → unit 76, component 31/167; c5 ./FavoritesView,
  ./useFavoritesView, ./RemoveFavorite, the menu's links → unit 76, component 50/254.
- Breaks, all red: #59 `repeated: false`; #60 a gone space linked; #61 page kept ("expected '?status=decided&page=2'
  to be '?status=decided'"); #62 toggle always; #63 `aria-current` dropped; #64 links in the dashboard's menu; #65/#65b
  taken twice; #66 dialog for a guest; #67 details always required; #68 one toast; #69 `role="alert"` dropped; #70
  `next` dropped; c2-drop (the held report not cancelled on close); #71; #72 a key header ("expected 'k' to be
  undefined"); #73 pressed only on the answer; #74 pressed kept on failure; #75 sent as a guest; #76 saved twice (green
  at first → the resume mounted in StrictMode after the session → red "Found multiple elements…"); #77 `aria-pressed`
  dropped; #78 read for a guest; #79 action inside the link; #80 gone ones dropped; #81 focus keeper removed; c5-clear
  (clearing near me keeps the favourites' near answer).
- Heavy on `b8f70b7d`: lint 0 (11:39–11:41); typecheck 0 (11:41); `test:unit -w @masaha/web` "Test Files 149 passed
  (149) · Tests 1032 passed (1032)"; `test:component -w @masaha/web` "Test Files 1 failed | 284 passed (285) · Tests 1
  failed | 1650 passed (1651)" (11:42–11:48) — the known routes 403 miss; alone red too; lane C touches nothing under
  `pages/dashboard`. Per commit: Prettier, `check:classes` (1573 files), `check:links` ("2960 links … all resolve"),
  `check:conflicts` clean. Mid-commit, `src/pages/site` missed SiteAccount "shows sign-in to a guest" and SiteLayout
  "renders the header…" on a cold import; alone 14/14 (finding 87's family); the full lane passed them.
- Shared: copy index ×2 (`favorites` after `errors`); `dataReports.ts` ×2 (`mine`, `report`); data-reports repository
  (`myReports`, `report`), keys (`mineAll`, `mine`), `index.ts` (`MyReportsList`, `ReportAction`); `src/test/dataReport.ts`
  (`myReport()`); the layer's `index.ts` (`HeartIcon`); `IconsSection.tsx`; `pages/site/routes.component.test.tsx` (its
  error-boundary helper wraps a QueryClient); architecture §2, §7; overview; foundation screen 11; findings index 168.
- Decisions (none SERIOUS): LC-D4 «بلاغاتي» reuses `useSpaceReportsFilters` (no `useMyReportsFilters`); LC-D5 copy reused
  by key (`sheet.replySpace`/`replyTeam`, `dataReports.pagination`, `site.browseSpaces`, `status.retry`); LC-D6
  `SITE_PATHS.account` not added (nothing uses it), `myFavorites` in c4; LC-D7 `signIn(reason, cancel)` — closing the
  prompt lets the held intent go; `useSignInPrompt`, `useHeart` in `pages/site/public/`; LC-D8 the held report a zustand
  store (`useStore`), "once" = until the dialog is closed; LC-D9 `SpacePageView.space: { id, slug, name, verified }`;
  LC-D10 `useReportDialog`'s tests render `ReportDialog`; LC-D11 `invalid_choice` → «اختر نوع المعلومة»; LC-D12 favourite
  writes through `writeFavorite` outside the component («تراجع» works after the heart leaves); LC-D13 `RemoveFavorite`
  held with `aria-disabled`; LC-D14 DI-52's focus order (next «إزالة», else the first card's heart, else the count);
  LC-D15 `useNearMe().clear` drops the favourites' near answers; LC-16 the site routes test's QueryClient; LC-17
  `SpacePage.component.test.tsx` loads the lazy shell once in `beforeAll`; LC-18 architecture's "`account/` not built"
  corrected to the account's settings (screen 9); LC-19 `DirectoryList` unchanged; LC-20 a press while the session
  restores is ignored; LC-21 the account links before the dashboard in the menu (`accountLinkIcons.ts`).
- Left: commit 6 (the lead's); check 5.k (the lead's build) — `@features/data-reports`' index exports
  `SpaceReportsList`, which imports `@shared/design-system/data`; 178, 179 unused.
