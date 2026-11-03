## Summary

PUBLIC PR 4, the item's last: **Home**, **About** and the site's **offline and error states**, after the fixes
carried from #108.

- **Home** (screen 1): the hero «اعثر على مساحة عمل في قطاع غزة» with its search, which opens the Directory with
  `q`; six spaces — «متاحة الآن», or, while near me sorts by distance, «المساحات الأقرب إليك» from the rounded
  point sent in `Masaha-Near` only — with near me's own button and state line and «عرض الكل» keeping the order;
  «تصفّح حسب المنطقة», the areas that hold spaces with their governorate and count, then «كل المناطق»; the
  owners' card to `/about#owners`.
- **About** (screen 4, U11): what Masaha is and for whom; where the information comes from; what each live
  status means (the cards' own badges); «تواصل معنا» (`#contact`) then «لأصحاب المساحات» (`#owners`), each with
  the configured contact, their text alone with none; no university line. The footer offers «تصفّح المساحات»
  first.
- **The offline and error states** (PU-024): the site's boundaries offer «الرئيسية» after «إعادة المحاولة»; a
  retry while the browser still reports no connection says «ما زال الاتصال مفقودًا.» instead of reloading;
  offline has its own icon, the layer's new `WifiOffIcon`; the general error's line is «المشكلة عندنا، لا
  عندك. حاول مرة أخرى بعد قليل.»

### Carried from #108

From `0_CARRIED_FROM_108.md` (the Codex review of #108), each a commit at the start, each code fix red first:

1. A failed refresh keeps the last live status (`fix(directory): keep the status on a failed read`).
2. The viewer's position counts every photo, past the five tiles (`fix(directory): count every photo in the viewer`).
3. A phone shows the first tile alone; up to five from 768 px (`fix(directory): show one tile on a phone`).
4. Test 77 drives the refresh by the page's visibility and its event, and fails with each of its breaks
   (`test(directory): drive the refresh by page events`).
5. Finding 131 names whose live status stands for a closure (`docs: say which live status stands for a closure`).
6. The footer keeps the contact bar's room only when the page draws the bar, through the site's layout
   (`fix(site): reserve the bar's room only with a bar`).
7. The place map's no-drag, no-pinch props have their test (`test(map): prove the place map lets a phone scroll`).
8. #108's real-run gaps, done in this PR's real run; it found the focus not returning to the photo tile after
   Escape — fixed with a test (`fix(directory): return the focus to the photo tile`).

## Scope

- `shared/routing`: `RetryState` and `RouteErrorState` take the caller's other ways on and say a failed retry;
  `shared/design-system`: `WifiOffIcon` (and the showcase's icon list).
- `features/directory`: `HomeSpaces`, `useAreaCounts`, `LiveStatusBadge` and `statusViewOf` exported for About;
  `useSpaceContactBar` (carried item 6); the gallery and live-status fixes.
- `features/lookups`: `usePublicAreas`.
- `pages/site`: Home (`public/home/`), About (`public/about/`), `SiteRouteError` on the site's boundaries, the
  footer's first link and its bar room, `navigation.ts` (`OWNERS_ANCHOR`, `SITE_PATHS.owners`).
- Copy: `site.home`, `site.about`, `status`, `directory.home`, both languages.
- Docs: `directory.md`, `lookups.md`, `architecture.md` §2, `overview.md`, `docs/README.md`, finding 131.

## Acceptance criteria

- [x] Home: the hero's search opens the Directory with `q`; «متاحة الآن» (six at most) or, with a location,
  «المساحات الأقرب إليك» (six at most); «تصفّح حسب المنطقة» lists the areas that have spaces with their
  governorate and count, then «كل المناطق»; the owners' card leads to `/about#owners`.
- [x] About: no university line; «تواصل معنا» (`#contact`) before «لأصحاب المساحات» (`#owners`), each with the
  configured contact.
- [x] The site's offline and error states offer «الرئيسية» besides «إعادة المحاولة»; a retry while still
  offline says «ما زال الاتصال مفقودًا.» without a reload; the offline state has its own icon.
- [x] The same checks and CI.

## Out of scope

No `apps/api`, `packages/shared`, schema, migration, seed or dependency change. The report button, the
favourite heart and the closure's notice (step 10; finding 131). The platform's settings screen (step 11).

## Change type

Feature (web) · docs · design system (one icon).

## Evidence

Run locally on the head, each exit 0:
- `npm run test:unit -w @masaha/web` — `Test Files 115 passed (115)`, `Tests 918 passed (918)`.
- `npm run test:component -w @masaha/web -- src/shared/routing src/shared/map src/shared/design-system
  src/features/directory src/features/lookups src/pages/site` — `Test Files 98 passed (98)`, `Tests 603 passed
  (603)` (a first run failed two tests of the site shell's test, which expected the old placeholder heading;
  fixed in commit 4).
- `npm run lint` · `npm run typecheck` · the production build · `npm run check:build` (no dashboard code, no
  data table, no Leaflet in the site's first download: 1,002,500 B → 1,010,782 B) · `npm run check:classes` ·
  `npm run format:check` · `npm run check:links`.
- Tests 80–86 each seen red (before the code, or by the plan's break), and each break restored.
- The real run in local headless Chrome, Arabic light and English dark at 390, 768 and 1440: Home's search,
  available now, near me (the point only in `Masaha-Near`, three decimals), «عرض الكل», the areas, the owners'
  card and both About anchors, the legend, the contact with the email alone and with none, the offline state and
  its retry; and #108's gaps: the status not polled while the tab is hidden and read at once on return, a finger
  over the place map scrolling the page, the page's foot with and without the bar, the gallery at each width,
  the focus back on the tile after Escape.

Not run locally (CI judges): the full `test:component` lane, `test:unit` of `apps/api` and `packages/shared`,
`test:api` (no API change).

Not performed, by design: the general error (needs a code change; its tests prove it), Home's empty state (the
data has spaces available; test 83), `FULL` (no space holds it).

## Screenshots

Attached by the owner.

## Definition of Done

- [x] Scope as the plan's PR 4, with the carried items first; atomic commits, each with its reason.
- [x] Every user-facing word through the catalogue, in both languages; Arabic plural forms for the counts.
- [x] Design-system change only `WifiOffIcon`, in the layer; semantic tokens only.
- [x] Docs updated where the behaviour lives; `#111` in their history.
- [x] Lint, typecheck, tests, build and checks green locally; CI green on the pushed head.
