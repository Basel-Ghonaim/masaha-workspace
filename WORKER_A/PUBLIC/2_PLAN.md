# PUBLIC — the public site on the web: Directory, map, Space details, Home, About (build map step 3, screens 1–4) — the plan

> Written 2026-10-20 from `origin/main` **`cf3190a4`** (#98 merged: OWNER_SETUP PR 2). **The executor of PR 1
> starts only after OWNER_SETUP PR 3 (`feat/owner-staff-settings`) has merged**; its first step is
> `git diff --name-status cf3190a4 origin/main` (§13). Four PRs in sequence (the owner's decision 2), each cut
> from the latest `origin/main` once the one before it has merged, each with its own execution prompt and its
> own review (all four are over 25 files):
> - **PR 1** `feat/directory-list` — the Directory's list: seven commits, ≈ 95 files (A13 proposes two PRs).
> - **PR 2** `feat/directory-map` — the map: three commits, ≈ 40 files.
> - **PR 3** `feat/space-page` — the Space details page: six commits, ≈ 75 files.
> - **PR 4** `feat/home-about` — Home, About and the error states: five commits, ≈ 38 files.
>
> The executor may be any capable coding agent: no step depends on a Claude skill (the appendix is only a
> map). Finding numbers are this item's range, **130 and on**, in the order they are first recorded.
> `#PRNUM` stands for the PR's number until the push (§13). `{date}` is the day the line is committed
> (`YYYY-MM-DD`). Words are written Arabic first, then English.

> **Approved by the owner, 2026-10-21 — binding on every executor of this plan** (it wins where the plan
> below differs):
> - **§14 as the supervisor recommended:** (1) the plan with S1–S15 (A1–A12 not taken); (2) the closure's notice
>   waits for step 10 (finding 131); (3) **a small worker-B seed item** (`SEED_DEMO`'s directory set, ≈ 24
>   spaces, the cases §14.3 lists, photos through the local storage port) runs **before PR 1b's real run** —
>   PR 1a's real run uses what `masaha_dev` holds and stops only at a case its own list needs (§13's check);
>   (5) design issues 1–44 as written; (6) the Arabic copy of §9 as written; (7) `area:design-system` on the
>   PRs whose layers change; (8) foundation §5's status roles (PR 1) and architecture §6's sentence (PR 2)
>   corrected — the supervisor added decision 7's line to `DECISIONS_PUBLIC.md` (2026-10-21); (10) finding 27
>   resolved in PR 1's documents commit if its build's manifest shows the chunks no longer import each other.
> - **(4) The platform's contact:** the variables `VITE_CONTACT_EMAIL` and `VITE_CONTACT_WHATSAPP` (S11). **The
>   email is a placeholder for now: `masahagaza@gmail.com`**; no WhatsApp yet (hidden). The executor **may add
>   `VITE_CONTACT_EMAIL=masahagaza@gmail.com` to `apps/web/.env`** (local, never committed) — the one `.env`
>   change this item allows — and documents both variables in `apps/web/.env.example` (the email with this
>   placeholder, the WhatsApp empty) and the setup document; Vercel's value is the owner's.
> - **(9) A13 taken — five PRs, not four:** **PR 1a** `feat/directory-list` — commits 1–5 (≈ 63 files), title =
>   commit 5's subject; **PR 1b** `feat/directory-filters` — commits 6–7 (≈ 34 files), title = commit 6's
>   subject, cut from `main` once 1a merges; then PR 2 (map), PR 3 (space page), PR 4 (Home, About, errors),
>   each with its own execution prompt and review. Each PR's documents say only what it built.
> - **The owner's standing rules:** a small fix a review defers is the next PR's first commit
>   (`0_CARRIED_FROM_<n>.md`); a full lane killed for memory is re-run once, then CI judges; finding 87's routes
>   test missing its 3 s locally while passing alone → CI judges.

## 1. Summary

Step 3 of the build map on the web: anyone finds a space, in the list or on the map, near them or by filter,
sees its page and how to reach Masaha. The API is built (#73, #77, #94); the four public pages are placeholders.

- **PR 1 — the Directory's list.** A new web feature, `directory` (any page group, architecture §3), lists the
  publicly listed spaces a page at a time from `GET /spaces`: the striking card (the cover or the space's mark,
  no price, the live status by word, today's hours, the distance), the search (both names and the area), the
  place filter (`lookups`' public areas, one multiple `Combobox`), the price filter (a period and a budget in
  shekels), «متاحة الآن فقط» and «المساحات الموثّقة فقط», «أخرى» (student prices, open on Friday), the sort,
  the pages (P6), and «الأقرب إليّ» with its one state line and the privacy line. Every filter, the sort and
  the page live in the URL; the device's rounded location lives in memory only. The filters are a sidebar
  from 1024 px and a bottom sheet below it. The site's shell gains its skip link and moves the focus to the
  page on navigation. Two refactors first: the list's pages (`ListPagination` and its helpers) and the name and
  clock rules move from dashboard-only features to `shared/`, so the site can use them.
- **PR 2 — the map.** `shared/map` gains a map of many marks (Leaflet stays there) and the directory draws its
  pins on it: each live state a shape as well as a colour, the legend in the map, the selected space as a
  bottom sheet on a phone and a card from 768 px, re-asking within the viewport past 1,000 pins, and placing
  one's location by hand at a centre crosshair. Leaflet still loads only with the map.
- **PR 3 — the Space details page** at `/spaces/:slug`: one order at every width (U8), prices per audience
  (U9), the hours with the shifts once, the amenities as one list, the gallery or its caption, the location on
  a static map with «الاتجاهات», the contacts with their values and carriers, each fact group's freshness
  (U4), the live status refreshed every 60 s while the page is visible, the unverified notice with the
  platform's contact, the breadcrumb from 768 px and the phone's WhatsApp/Call bar below it. A new web feature,
  `platform-settings`, reads the platform's contact from two `VITE_` variables (decision 5).
- **PR 4 — Home, About and the error states.** Home (the hero search, «متاحة الآن» or the nearest, «تصفّح
  حسب المنطقة», the owners' card), About (U11, its `#contact` and `#owners`), and the site's offline and error
  states with a second way on and a retry that says it is trying (PU-024).

No API, `packages/shared`, schema, migration, seed or dependency change. The report button and the favourite
heart are not built (decision 4).

## 2. The contract

### Scope

**PR 1 — the Directory's list**
- `shared/lists` (new module): `ListPagination`, `paginationView`, `PaginationView`, `pageItems`,
  `usePausedSearch`, moved from `features/space-links` (S2).
- `shared/lib`: `spaceNameOf` and `SpaceNameView` (`names/`), `clockOf` (`time/`), moved from
  `features/spaces` (S3).
- `shared/design-system`: `useMediaQuery` exported from the layer's barrel (S6) — no visual change.
- `pages/site/shell`: the skip link, `<main id="main">`, the focus moved to it on navigation (S8).
- `features/lookups`: `AreaFilter` (new export); `AreaName` takes `source` (S7).
- `features/directory` (new, any page group): the list, its URL state, the card, the filters, the sort, the
  pages, near me.
- `pages/site/public/directory/DirectoryPage.tsx`: composes the list with `lookups`' two slots.
- Copy: `site` (the skip link), `lookups` (the area filter), a new `directory` section.
- Docs: `docs/features/directory.md` (its web parts), `lookups.md`, `docs/frontend/architecture.md`,
  `docs/frontend/design-system/foundation.md` (§3 the layer's hook export; §5 the status roles, if §14.8 is
  approved), `docs/project/overview.md`, `docs/README.md`; finding 130 recorded.

**PR 2 — the map**
- `shared/map`: `MarkerMap` (many marks, a selected one, the user's point, a centre to pick, the viewport
  handed back), its lazy Leaflet part, the `MapMark` type; `shared/design-system/leaflet.css`: the four mark
  shapes and the crosshair (S12).
- `features/directory`: the pins' read and its viewport re-ask, the view switch («قائمة | خريطة»), the map
  view, the legend, the selected card and sheet, picking a point by hand; the near-me fallback «حدّد موقعي
  على الخريطة».
- Copy: `directory.view`, `directory.map`, `directory.pick`; `directory.near` (the map fallback).
- Docs: `directory.md`, `architecture.md` §6, `foundation.md` §3 (`leaflet.css`'s marks).

**PR 3 — the Space details page**
- `shared/lib`: `carrierOf` (`phone/`) and `updatedAgo` (`time/`), moved from `features/spaces` (S3).
- `shared/map`: `PlaceMap` (one place, its pin `role="img"`).
- `features/platform-settings` (new, any page group): the platform's contact from `VITE_CONTACT_EMAIL` and
  `VITE_CONTACT_WHATSAPP` (S11).
- `features/directory`: the page's read and its states, the live status's read and refresh, the sections,
  the gallery, the bottom bar, the near-me distance.
- `pages/site`: the route `/spaces/:slug` and `public/space/SpacePage.tsx`; `navigation.ts` (`spacePath`).
- Copy: `directory.page`, `platformSettings`, `site.links.space` (the route's title).
- Docs: `directory.md`, `architecture.md` (§2 the route built, §3 `platform-settings`, §7 the live status's
  refresh), `docs/development/setup.md` (the two variables), `apps/web/.env.example`, `overview.md`,
  `docs/README.md`; finding 40's evidence line; finding 131.

**PR 4 — Home, About and the error states**
- `shared/routing`: `RetryState` and `RouteErrorState` take the site's second way on and say a failed retry
  (PU-024); `shared/design-system`: `WifiOffIcon`.
- `features/directory`: `HomeSpaces` (available now or the nearest), `useAreaCounts`.
- `features/lookups`: `usePublicAreas`.
- `pages/site`: `public/home/` (the page, the area cards), `public/about/AboutPage.tsx`, the site's error
  boundary, the footer's third link.
- Copy: `site.home`, `site.about`, `status`, `directory.home`.
- Docs: `directory.md`, `lookups.md`, `architecture.md` §2, `foundation.md` §12 (the icon), `overview.md`,
  `docs/README.md`.

### Acceptance criteria

**PR 1**
- [ ] `/spaces` lists the publicly listed spaces 20 a page from `GET /spaces`, each card a link (to
  `/spaces/:slug`, the site's 404 until PR 3) with its cover or mark, its name (U3), its area with its
  governorate, its live status by word (or «لا تتوفر حالة مباشرة»), «موثّقة», today's hours on Gaza's
  calendar, and no price.
- [ ] The search (paused typing), the place filter, the price filter, the two switches, «أخرى», the sort and
  the page are in the URL: a reload, Back and a shared link show the same list; a value the server would
  refuse falls back to its default and never reaches the request.
- [ ] Below 1024 px the filters open in a bottom sheet from a button that says whether it is open and how many
  filters apply; its primary button counts the spaces (Arabic agreement); from 1024 px they are a sidebar.
- [ ] «الأقرب إليّ» asks for the location only when pressed; the point is rounded to three decimals before
  anything keeps it, kept in memory only, sent only in `Masaha-Near` with `sort=distance`; «إيقاف الترتيب حسب
  المسافة» keeps it, «مسح موقعي» drops it and every answer ordered by distance; a denied, unavailable,
  imprecise or out-of-Strip location says so and offers «اختر منطقتك»; the privacy line shows only where a
  location is being sent.
- [ ] Loading (skeleton cards), a failure (with its reference and «إعادة المحاولة»), offline, an empty
  directory, no match (with «مسح الفلاتر») and a page past the last are each their own state.
- [ ] The skip link reaches `#main`; a new page takes the focus to it; a new page of results takes the focus
  to the results' heading.
- [ ] Every counted line through the catalogue's plural forms.
- [ ] Lint, typecheck, `test:unit`, `test:component`, the production build, `check:build` (no dashboard code,
  no Leaflet, no data table in the site's first download), `check:classes`, `format:check`, `check:links`
  green; CI green; `CLEAN`.

**PR 2**
- [ ] «قائمة | خريطة» switches the view (`?view=map`) at every width; the map shows every space that passes
  the filters as a pin whose state is a shape as well as a colour, the legend in the map; past 1,000 pins it
  says so and asks again within the viewport.
- [ ] A pin is a named, focusable button; choosing one shows its card (a non-modal bottom sheet on a phone,
  a card in the map from 768 px), «عرض التفاصيل» leading to its page.
- [ ] «حدّد موقعي على الخريطة» (from the state line) shows a centre crosshair; «ثبّت الموقع هنا» places the
  rounded point and sorts by distance; «رجوع» returns to the location before; the arrow keys pan.
- [ ] Leaflet and its stylesheet stay out of the site's first download (`check:build`) and arrive only with
  the map.
- [ ] The same checks and CI as PR 1.

**PR 3**
- [ ] `/spaces/:slug` shows the space's page, titled by its name, in U8's order at every width; a hidden,
  deleted or unknown space shows «لم نجد هذه المساحة» with «تصفّح المساحات».
- [ ] Its live status is read from `GET /spaces/:slug/occupancy` on arrival, every 60 s while the page is
  visible, and on returning to it; never while hidden.
- [ ] Prices per audience; hidden prices explained with their date; each fact group's date and «قد يكون
  تغيّر» when stale; hours with today and the shifts once; the amenities one list; contacts with their values
  and a phone's carrier; the gallery or «لا توجد صور بعد»; the static map's pin `role="img"`; the breadcrumb
  from 768 px, «العودة إلى المساحات» below it; the WhatsApp/Call bar below 768 px.
- [ ] An unverified space's notice offers the platform's contact: the configured email only until a WhatsApp
  number is configured; neither drawn when neither is set.
- [ ] The same checks and CI.

**PR 4**
- [ ] Home: the hero's search opens the Directory with `q`; «متاحة الآن» (six at most) or, with a location,
  «المساحات الأقرب إليك» (six at most); «تصفّح حسب المنطقة» lists the areas that have spaces with their
  governorate and count, then «كل المناطق»; the owners' card leads to `/about#owners`.
- [ ] About: no university line; «تواصل معنا» (`#contact`) before «لأصحاب المساحات» (`#owners`), each with
  the configured contact.
- [ ] The site's offline and error states offer «الرئيسية» besides «إعادة المحاولة»; a retry while still
  offline says «ما زال الاتصال مفقودًا.» without a reload; the offline state has its own icon.
- [ ] The same checks and CI.

### Out of scope

- Any API, `packages/shared`, schema, migration, seed or dependency change (§14 if one seems needed).
- The report button, the favourite heart, «بلاغاتي», the space page's announcements and the closure's notice
  (step 10; decision 4; §14.2).
- The account area (`/me`) and the dashboard's shells (finding 130 records their missing skip link).
- The removable filter tag (finding 8, step 10) and an applied-filters row (A3).
- The platform's settings screen and `GET /settings/public` (step 11; A9).
- Round 2's open design decisions: built from the settled ones (decision 6); the defects its reports prove are
  not copied (§8).

## 3. The reading done

`CLAUDE.md`; `docs/development/workflow.md`; `testing.md`; `engineering-principles.md` §1;
`docs/frontend/architecture.md` (whole: §1 the zones, §2 the site's shell and titles, §3 the features and their
exports, §6 the map, §7 the cache and polling); `design-system/foundation.md` (§3, §5, §8, §9, §10, §12, §13
screens 1–4 and near me, §15); `localisation.md`; `documentation.md` §5; `docs/features/directory.md`,
`occupancy.md`, `lookups.md` (the public catalogue, `AreaName`, `source`), `spaces.md` (the editor's read-only
views, its code map); `docs/api/api-contract.md` §1–4, *Lookups (public)*, *Directory (public)*;
`docs/backend/security.md` › *Location*; ADR 0002, 0004 (polling), 0008; `docs/plans/v1-mvp.md` step 3, the
ordering notes and the planned `GET /settings/public`; `docs/design/SCREENS.md`; `docs/project/overview.md`;
`docs/README.md`; `docs/development/setup.md` › *The web*; the findings index and findings 8, 27, 40, 46, 55,
64, 98. The prototype: `Home.html`, `Directory.html`, `Space details.html`, `About.html`, `Error.html`,
`masaha/shared.jsx`, `location.jsx`, `map.jsx`, `space-parts.jsx`, and `data.js`/`details-data.js` for the
periods, the «أخرى» group and the channels. `DECISIONS_PUBLIC.md`, `DECISIONS_SHARED.md`; the four round-2
reports `R2-PU-AX`, `R2-PU-CP`, `R2-PU-UX`, `R2-PU-VD`. The code: `pages/site` (`routes.tsx`, `navigation.ts`,
`index.ts`, the shell, the four placeholders), `shared/map` (whole), `shared/routing` (the index, the states,
`publicSpacePath`), `shared/copy` (`site`, `status`, `map`, `terms`, `plural.ts`, the index), `shared/lib`,
`shared/storage`, `shared/api` (the calls, the query client's defaults), `shared/forms` (`isolated`, `clock`),
`shared/localisation`'s exports, the design system's barrel (`Combobox`, `Pagination`, `Badge`), `leaflet.css`'s
head; `features/lookups` (the index, the catalogue's query, the keys, `AreaName`, `AmenityIcon`, the
repository); `features/spaces` (the read-only hooks of hours, prices, contacts, amenities; `carrierOf`,
`clockTime`, `updatedAgo`, `spaceName`); `features/space-links` (the admin list's URL filters, `usePausedSearch`,
`ListPagination`, `paginationView`, `pageItems`); `packages/shared` (`directory`, `lookups`, `occupancy`,
`spaces` responses, `core/gazaTime`); `apps/web/scripts/` (`checkBuild.ts`, `dashboardOnly.ts`,
`libraryChunks.ts`), `vite.config.ts`, the eslint boundaries, `apps/web/.env.example`, `app/RootLayout.tsx`,
`src/test/` (the helpers' names); the demo seed's space. OWNER_SETUP's `2_PLAN.md` and `3_EXEC_PROMPT_PR3.md`
for the shape and the procedure.

**What the reading changed.**
- **The site cannot import what it needs from `spaces` or `space-links`** (dashboard-only, architecture §3):
  the list's pages (`ListPagination`, `paginationView`, `pageItems`, `usePausedSearch`) and the name, clock,
  carrier and date rules have a second user now. They move to `shared/` (S2, S3), as the money helpers did.
- **`directory` cannot import `lookups`** (no sibling imports): the area filter and the governorate's name are
  `lookups`' exports set in the directory's slots by the page (S7) — the card's area line included, since
  `DirectorySpace.area` carries no governorate ("its governorate: the catalogue's").
- **Leaflet stays in `shared/map`** (lint), while architecture §6 gives "space markers and popups" to
  `directory`: the map of many marks is a generic `shared/map` component; the directory decides what each
  mark means (S12).
- **The public page carries no announcements** (`PublicSpace`): the closure's Alert the owner lists in PR 3
  has no data until step 10 (§14.2, finding 131).
- **`PublicSpace` carries no live status;** the page always reads `GET /spaces/:slug/occupancy` (decision 3).
- **The prototype keeps the location in `sessionStorage`** and its privacy line in every state; here it lives
  in memory only (S4) and the line shows only where a location is sent (design issue 5, R2-PU-CP-001).
- **The demo seed holds one space** (verified, no photo): the real runs' pages, an unverified space with
  hidden prices, photos and a space with no hours need data `masaha_dev` may not hold (§13's inventory, §14.3).
- **Foundation §5 still says "Space full" is `destructive`;** DECISIONS_SHARED settled Full as `warning` and
  Closed as `neutral` (2026-10-10) without the document following (§14.8).
- **Architecture §3 gives the public contact to `platform-settings`, and v1-mvp plans `GET /settings/public`;**
  decision 5 puts it in the web's configuration for now (S11, A9, §14.4).

## 4. The owner's decisions, as they will be built

1. **Worker A builds it after OWNER_SETUP** (no third worker).
2. **Four PRs in sequence,** as above, each from the latest `main` once the one before has merged. A better cut
   is proposed only (A11).
3. **The live status's delivery.** The space page reads `GET /spaces/:slug/occupancy` on arrival, **every 60 s
   while the page is visible** (`refetchInterval: 60_000`; TanStack Query pauses an interval while the document
   is hidden, `refetchIntervalInBackground` staying `false`) and **on returning to it**
   (`refetchOnWindowFocus: 'always'`). The Directory's and Home's lists keep the app's defaults: no interval;
   fetched again on returning to the window once their 30 s have passed, and on a new visit. Recorded in
   architecture §7 › *Polling*, which owns polling: PR 1 the lists' line, PR 3 the page's.
4. **No report button, no favourite heart:** not drawn at all; the space page's title row and its last section
   end where they would have stood, with no gap (design issue 34).
5. **The platform's contact** comes from two `VITE_` variables read in one module of a new
   `features/platform-settings` (S11): `VITE_CONTACT_EMAIL` and `VITE_CONTACT_WHATSAPP`. Each shows only when
   set and valid. **The owner fills them** in `apps/web/.env` (local) and, online, in the Vercel project's
   *Settings › Environment Variables* (Production and Preview), then redeploys (Vite reads them at build time).
   Until the owner supplies the WhatsApp number, only `VITE_CONTACT_EMAIL` is set; `.env.example` lists both,
   empty, with one comment line each.
6. **Design round 2:** built from the settled decisions; every defect the four reports prove is listed in §8
   with its fix; what would change a settled decision is a Proposed alternative (§5).
7. **The decisions file's amendments win:** no price on the card, no «الأقل سعرًا», no amenities filter. The
   line that corrects `DECISIONS_PUBLIC.md`, for the supervisor to add under U12 (PR 1's documents step names
   it in the PR's description; the executor does not edit the file):
   > **Superseded by the amendments at the top (2026-10-12):** U9's card part («the card keeps its four general
   > cells and one «للطلاب» line») and U12's open point (whether the cells stay) — the card shows no price;
   > U2's sort list loses «الأقل سعرًا»; the amenities are no filter. The web builds the amended rules
   > (PUBLIC, PR 1).
8. **The privacy line** under «الأقرب إليّ» is the prototype's corrected one, word for word: «يُرسَل موقعك
   مقرَّبًا لترتيب المساحات حسب المسافة فقط، ولا يُحفظ.» / "Your location is sent rounded, only to sort spaces
   by distance, and is never stored."

## 5. Stronger decisions

**S1 — one `directory` web feature holds the list, the map and the space's public page.** Architecture §3 names
`directory` "(the directory and the public profile)", any page group; its API module and `directory.md` own the
public page. `spaces` stays dashboard-only, its editor untouched. *What stays in `pages/site`:* the routes, the
titles, the shell, the paths (`SITE_PATHS`, `spacePath`), and the composition of `directory` with `lookups` and
`platform-settings`. *Cost:* one large feature (≈ 110 files by PR 4), a folder per operation. *Recommend:* take
it.

**S2 — the list's pages move to a new `shared/lists`** (`ListPagination`, `paginationView`, `PaginationView`,
`pageItems`, `usePausedSearch`), with their tests, unchanged. *Why:* the Directory is their second user, and
`space-links` is dashboard-only; engineering principles §1 (the second instance). A new `shared/` module is named
in architecture §1's zone table (eslint's `apps/web/src/shared/*` element already admits it). *Cost:* one
refactor commit, six importers. *Recommend:* take it.

**S3 — the name, clock, carrier and date rules move to `shared/lib`:** `spaceNameOf`/`SpaceNameView` and
`clockOf` in PR 1, `carrierOf`/`Carrier` and `updatedAgo` in PR 3, each with its tests. `clockTime.ts` keeps
`minuteOf` and `settledClock` and imports `clockOf`. *Why:* the card and the page need them; a copy would drift
(OWNER_SETUP did the same for money). *Cost:* two refactor commits. *Recommend:* take it.

**S4 — the device's location lives in memory only:** a store in `features/directory` (Zustand, as the session
and the preferences are; never persisted) holds the **rounded** point (three decimals, `NEAR_DECIMALS`), where it
came from (`device` or `pin`), its state (`idle`, `locating`, `denied`, `imprecise`, `picking`) and whether the
lists sort by distance. The raw position never leaves the geolocation callback. Never in the URL, never in
browser storage, never logged; «مسح موقعي» also removes every answer ordered by distance from the cache.
*Why:* security › Location ("never stored"); a URL is logged by hosts and shared by people; a reload asks again
with one tap, the permission being the browser's. It survives moving between Home, the Directory and a space's
page (one app). *Cost:* a reload loses it (A8 keeps it for the tab). Architecture §3 › *Where state lives* gets
its line. *Recommend:* take it.

**S5 — the Directory's URL** (`/spaces?…`), every key optional, a default never written:
`q` (the search as typed, trimmed), `area` (comma list of area ids, each once, at most 50), `period`
(`HOUR`|`DAY`|`WEEK`|`MONTH`, default `DAY`, written only with a bound), `min`, `max` (whole shekels, 1–100,000),
`available=1`, `verified=1`, `students=1`, `friday=1`, `sort` (`updated`|`name`|`relevance`; `relevance` only
with `q`; the default — `relevance` with `q`, else `updated` — unwritten), `page` (written from 2), `view=map`
(PR 2). The budget is in **shekels** in the URL and named `min`/`max`, the API's `priceMin`/`priceMax` being
agorot (one name, one unit). A value the server would refuse falls back to its default; a filter change
replaces the address and returns to page 1, as the admin's lists do. The distance order is **not** in the URL
(S4). *Recommend:* take it.

**S6 — the layer exports `useMediaQuery`** (`shared/design-system/lib/useMediaQuery.ts`, internal today).
*Why:* the filters are drawn once per width — the sidebar from 1024 px, the sheet below — never twice with
duplicate ids, and the component lane can prove the switch with `stubScreenWidth`. *Cost:* one line in the
layer's barrel and foundation §3's public surface. *Recommend:* take it (else: both drawn, hidden by classes,
and the width rule proven only in the real run).

**S7 — `lookups` offers the site two exports, set by the page in the directory's slots:** `AreaFilter` (new: the
public catalogue's areas, grouped under their governorates, a multiple `Combobox`) and `AreaName` with a
required `source: LookupsSource` (`public` reads `GET /lookups`; the two admin callers pass `admin`). *Why:* no
sibling imports; the governorate's name is the catalogue's. *Cost:* the existing callers of `AreaName` add
`source="admin"`. *Recommend:* take it.

**S8 — the site's shell gets SH-018's skip link and focus management:** its first focusable element, «تخطَّ
إلى المحتوى» → `#main`; `<main id="main" tabIndex={-1}>`; on a change of **path** (not of search or hash, not
the first load) the focus moves to `#main` without scrolling (`ScrollRestoration` scrolls). *Why:* R2-PU-AX-001
(a skip link to nothing) and a client-side navigation that leaves the focus on a removed link. *Cost:* the
shell and its test. The dashboard's shells are out of scope (finding 130). *Recommend:* take it.

**S9 — «أخرى» (student prices, open on Friday) is built in PR 1,** though the prompt's PR 1 list omits it.
*Why:* foundation §13 and the overview's scope list both; the API has both filters; the prototype draws them.
*Cost:* one `ToggleGroup`, two URL keys. *Recommend:* take it.

**S10 — the sort offers «الأفضل تطابقًا» while a search is typed,** the server's default then; «حسب المسافة»
appears, chosen, only while sorting by distance. *Why:* the server orders by relevance with `q`, and a trigger
must never show a value its list lacks (R2-PU-CP-022). *Recommend:* take it.

**S11 — the platform's contact is `features/platform-settings`,** any page group (architecture §3 already names
it "the public contact"): `services/platformContact.ts` reads `import.meta.env.VITE_CONTACT_EMAIL` and
`VITE_CONTACT_WHATSAPP` through a pure `contactOf({ email, whatsapp })` that keeps an email only if the shared
`emailSchema` takes it and a WhatsApp number only if `normalisePhone` (`@masaha/shared/core`) gives one;
`PlatformContact` (exported UI) renders the configured channels as buttons. *Why:* one seam, which step 11
replaces with `GET /settings/public` without touching a page; never the copy catalogue (decision 5); a
constants file would put the owner's number in the repository. *Cost:* a feature with no repository yet.
*Recommend:* take it.

**S12 — `shared/map` gains `MarkerMap` (PR 2) and `PlaceMap` (PR 3); Leaflet stays there.** A mark is a shape
and a tone the caller chooses (`MapMark = { shape: 'filled' | 'bar' | 'hollow' | 'dashed'; tone: 'success' |
'warning' | 'neutral' | 'muted' }`), drawn by `leaflet.css` from the tokens; the directory maps a live state to
a mark. *Why:* lint keeps Leaflet in `shared/map`; the layer's admission test (a mark survives outside Masaha).
Architecture §6's sentence is corrected: the markers' *meaning* is the directory's, their drawing
`shared/map`'s. *Recommend:* take it.

**S13 — the list keeps the previous page on screen while the next arrives** (`placeholderData:
keepPreviousData`), the results marked `aria-busy`. *Why:* on a weak connection the list never blanks between
two filters. *Recommend:* take it.

**S14 — the live status's words are `terms.liveStatuses`, and its roles DECISIONS_SHARED's:** `AVAILABLE` →
`success`, `FULL` → `warning`, `CLOSED` → `neutral`; none → muted text. *Why:* one home per word; foundation §5's
table still names `destructive` for "Space full" (§14.8). *Recommend:* take it, and correct foundation §5 in
PR 1.

**S15 — a `q` the server would refuse never leaves the browser:** the search's text is read with the
`directoryQuerySchema`'s rule (`@masaha/shared/directory`); a text of tashkeel or tatweel only stays in the
field with its line, «اكتب حرفًا من اسم المساحة أو منطقتها», and the request goes without it. *Why:* the server
answers 422, which would replace the list by a failure. *Recommend:* take it.

**No rule is weakened.** Authorization is not involved (public reads); the design system gains only S6's
export, `leaflet.css`'s marks (PR 2) and one icon (PR 4), each in the layer.

### Proposed alternatives (the owner may prefer them; none is applied)

- **A1 — the privacy line's wording** (R2-PU-CP-002): «نرسل موقعًا تقريبيًا (لا موقعك الدقيق) إلى مساحة
  لترتيب المساحات فقط، ولا نحفظه.», and R2-PU-CP-001's conditional line for the failed states («إن حدّدت
  موقعك، نرسله تقريبيًا لترتيب المساحات فقط، ولا نحفظه.»). Not taken: decision 8 fixes the line. *If taken:*
  `directory.near.privacy` changes and one line is added.
- **A2 — feminine live states** («متاحة · ممتلئة · مغلقة الآن», R2-PU-CP's doubt). Cost M: the glossary,
  `terms`, the dashboard. Not taken.
- **A3 — an applied-filters row on a phone** (R2-PU-UX-006): it needs finding 8's removable tag in the layer
  before step 10. Cost M. Not taken.
- **A4 — «تبديل الحدّين»** on an inverted price range (R2-PU-UX-007). Cost S. Not taken.
- **A5 — «الاتجاهات» in the phone's bottom bar** (R2-PU-UX D1). Changes PU-020. Not taken.
- **A6 — the budget said in the count line** (R2-PU-UX D2), e.g. «… · سعر اليوم حتى 20 ₪». Not taken.
- **A7 — the map's marks beside About's legend** (R2-PU-VD-003): About would need `leaflet.css`'s marks outside
  the map. Not taken.
- **A8 — the rounded location kept for the tab** in `sessionStorage`, through `shared/storage`'s first session
  key, so a reload keeps it. Not taken (S4).
- **A9 — `GET /settings/public` by worker B now** (the plan's planned endpoint), so the contact has one home (the
  platform's settings, finding 40) and the admin edits it at step 11; `platform-settings` would read it instead
  of the variables. Cost: an API item before PR 3. Not taken (decision 5).
- **A10 — a numeric first-download budget in `check:build`** (bytes of the entry and its static imports). A
  change of a build check (a review trigger). Not taken: the structural rules hold; each report records the
  sizes.
- **A11 — another cut:** near me (the store, the state line, the privacy line) moves from PR 1 to PR 2, which
  owns its map fallback; PR 1 ≈ 48 files, PR 2 ≈ 52. Not taken: the owner's cut ships near me with the list,
  «اختر منطقتك» its only fallback until PR 2.
- **A12 — the space page in `spaces`' public part.** Not taken (S1).

## 6. Related findings

| Finding | Folded? | Why · cost |
|---|---|---|
| 8 the applied-filter tag has no component | No | The owner placed it at step 10; the Directory shows the count badge and «مسح الفلاتر» (A3). |
| 27 two dashboard chunks import each other | No, re-checked | PR 1 makes the site use `useQuery` and `publicSpacePath`, the two imports that tie the chunks: §13 › *On the head* reads the manifest after the build and records whether the cycle is gone; resolving it is the owner's call on that evidence (§14.10). |
| 40 the platform's contact settings are outside the typed catalogue | Evidence line, PR 3 | The site reads its contact from the web's variables (S11); the seeded rows stay unread. Its *Resolves when* is unchanged (step 11, or A9). |
| 46 the map's tiles and a future CSP | No | PR 2 adds the Directory's map to its evidence (one line, same commit as the map). |
| 64 Cloudinary's photos and a future CSP | No | Its evidence already names every card's cover and the gallery. |
| 55 a lazy shell's first wait | No | The site's routes test gains a page; its time is recorded (§13). |
| 98 the capability documents outgrow their size guide | No | `directory.md` grows by its web parts (≈ +900 words by PR 4); each line kept to a decision's sentence. The owner's decision on finding 98 applies after. |
| **New 130** the dashboard's shells have no skip link | Recorded, PR 1 | SH-018 is built on the site only; the dashboard's two shells are another item. |
| **New 131** the space page cannot show a closure's notice | Recorded, PR 3 | `PublicSpace` carries no announcement (step 10); the live status says «مغلق الآن» meanwhile (§14.2). |

## 7. The files

A: added · M: modified · D: deleted · R: moved (`git mv`, then edited). Paths under `apps/web/src/` unless they
start with `docs/`, `apps/` or `packages/`. Every test sits beside its file.

**The counts the reading gives** (the owner estimated ≈ 60, 40, 55, 35): **PR 1 ≈ 95**, PR 2 ≈ 40, **PR 3 ≈ 75**,
PR 4 ≈ 38 — the two refactors of PR 1 (≈ 26 files, mostly one-line imports) and of PR 3 (≈ 12) make the
difference. A13 (§5's list continues below) proposes splitting PR 1.

- **A13 — split PR 1 in two** (as OWNER_SETUP's A4, which the owner took): **PR 1a** `feat/directory-list` —
  commits 1–5 (the two refactors, the shell, `lookups`, the list with its search, sort and pages; ≈ 63 files),
  title = commit 5's subject; **PR 1b** `feat/directory-filters` — commits 6–7 (the filters and near me; ≈ 34
  files), title = commit 6's subject, cut from `main` once 1a merges. *Why:* two reviews of a readable size; 1a
  ships a working list. *Cost:* a fifth PR and its CI. **Recommended.** PR 3 could split the same way (its
  commits 1–4 and 5–6); not recommended (≈ 75 files, two of its commits one-line imports).

### PR 1
- `shared/lists/` (A, new module): `index.ts`; R `features/space-links/components/ListPagination.tsx` →
  `components/ListPagination.tsx`; R `services/pageItems.ts` (+ `pageItems.unit.test.ts`); R
  `services/paginationView.ts`; R `types/PaginationView.ts`; R `hooks/usePausedSearch.ts`.
- `features/space-links/` — M `components/admin-list/AdminSpacesList.tsx`, `owners-list/OwnersList.tsx`,
  `users-list/UsersList.tsx`, `hooks/admin-list/useAdminSpacesFilters.ts`, `useAdminSpacesList.ts`,
  `hooks/users-list/useAdminUsersList.ts`, `useUsersFilters.ts` (imports only; plus any other importer
  `git grep` finds).
- `shared/lib/` — R `features/spaces/services/spaceName.ts` → `names/spaceName.ts` (+ its unit test), R
  `features/spaces/types/SpaceNameView.ts` → `names/SpaceNameView.ts`; A `time/clockOf.ts`, A
  `time/clockOf.unit.test.ts` (the `clockOf` cases moved from `clockTime.unit.test.ts`); M `index.ts`.
- `features/spaces/` — M `services/clockTime.ts` (imports `clockOf`), M `services/clockTime.unit.test.ts`
  (loses the moved cases), M every importer of `spaceNameOf`/`SpaceNameView`
  (`hooks/add/useCreateSpace.ts`, `hooks/editor/useSpaceEditor.ts`, `hooks/editor/useSpaceName.ts`,
  `hooks/menu/useSpaceActionsMenu.ts`, `components/toast/actionToasts.tsx`, `types/NamedLineView.ts`,
  `types/OwnersSlot.ts`, `types/SpaceAction.ts`, and any `git grep` adds). `space-links`' own
  `SpaceNameView` (in `AdminSpaceRowView.ts`) is left as it is (no drive-by; Review Focus).
- `shared/design-system/index.ts` — M (`useMediaQuery` exported, S6).
- `pages/site/shell/` — M `SiteLayout.tsx`, A `SkipLink.tsx`, A `useMainFocus.ts`, M
  `SiteLayout.component.test.tsx`.
- `features/lookups/` — A `components/area/AreaFilter.tsx` (+ component test), A
  `hooks/area/useAreaFilter.ts` (+ component test); M `components/area/AreaName.tsx`,
  `hooks/area/useAreaName.ts` and their tests (`source`); M `index.ts`.
- `pages/dashboard/admin/SpaceEditPage.tsx` — M (`AreaName source="admin"`), and any other caller.
- `features/directory/` (A, new):
  - `index.ts`;
  - `repository/directoryRepository.ts` (+ unit test);
  - `hooks/queryKeys.ts`;
  - `hooks/list/useDirectoryFilters.ts` (+ component test), `useDirectoryQuery.ts`, `useDirectoryList.ts`
    (+ component test);
  - `hooks/filters/usePriceFilter.ts` (+ component test), `useFiltersPanel.ts`;
  - `hooks/near/nearMeStore.ts`, `useNearMe.ts` (+ component test), `useLocationStatus.ts`;
  - `services/filtersOf.ts` (+ unit test), `requestOf.ts` (+ unit test), `cardView.ts` (+ unit test),
    `todayHours.ts` (+ unit test), `distanceText.ts` (+ unit test), `nearPoint.ts` (+ unit test),
    `priceBounds.ts` (+ unit test);
  - `types/DirectoryFilters.ts`, `SpaceCardView.ts`, `NearState.ts`, `DirectorySlots.ts`;
  - `components/DirectoryList.tsx` (+ component test); `components/card/SpaceCard.tsx`, `SpaceCover.tsx`,
    `LiveStatusBadge.tsx`, `SpaceCardSkeleton.tsx`; `components/list/DirectoryResults.tsx`,
    `ResultsState.tsx`; `components/search/DirectorySearch.tsx`; `components/sort/SortSelect.tsx`;
    `components/filters/FiltersForm.tsx`, `PriceFilter.tsx`, `FiltersSidebar.tsx`, `FiltersSheet.tsx`
    (+ component test); `components/near/NearMeButton.tsx`, `LocationStatus.tsx` (+ component test).
- `pages/site/public/directory/DirectoryPage.tsx` — M; `pages/site/routes.component.test.tsx` — M (the
  Directory's case).
- `shared/copy/{english,arabic}/` — M `site.ts`, `lookups.ts`; A `directory.ts`; M `index.ts` ×2.
- Docs — M `docs/features/directory.md`, `lookups.md`, `docs/frontend/architecture.md`,
  `docs/frontend/design-system/foundation.md`, `docs/project/overview.md`, `docs/README.md`; A
  `docs/architecture/findings/130-the-dashboards-shells-have-no-skip-link.md`; M
  `docs/architecture/findings/README.md`.

### PR 2
- `shared/map/` — A `components/MarkerMap.tsx` (the lazy wrapper, + component test),
  `components/LeafletMarkerMap.tsx`, `components/MapMarkSample.tsx`, `hooks/usePickCentre.ts`,
  `services/markClass.ts` (+ unit test), `types/MapMark.ts`, `types/MarkerMapProps.ts`; M `index.ts`,
  `components/MapFailed.tsx` (its line from a prop).
- `shared/design-system/leaflet.css` — M (the marks, the selected ring, the crosshair, the user's point).
- `features/directory/` — M `repository/directoryRepository.ts` (+ test: `pins`), M `hooks/queryKeys.ts`; A
  `hooks/map/usePinsQuery.ts`, `useDirectoryMap.ts` (+ component test), `useSelectedPin.ts`; M
  `hooks/near/nearMeStore.ts`, `useNearMe.ts` (+ test: picking); A `services/pinMark.ts` (+ unit test),
  `services/boundsText.ts` (+ unit test); A `components/DirectoryView.tsx`, `components/view/ViewSwitch.tsx`,
  `components/map/DirectoryMap.tsx` (+ component test), `MapLegend.tsx`, `SelectedCard.tsx`,
  `SelectedSheet.tsx`, `PickCard.tsx`, `MapNotice.tsx`; M `components/near/LocationStatus.tsx` (+ test), M
  `services/filtersOf.ts` (+ test: `view`), M `index.ts`.
- `pages/site/public/directory/DirectoryPage.tsx` — M.
- `shared/copy/{english,arabic}/directory.ts`, `map.ts` — M.
- Docs — M `directory.md`, `architecture.md` (§6), `foundation.md` (§3 `leaflet.css`), finding
  `46-…md` (evidence).

### PR 3
- `shared/lib/` — R `features/spaces/services/carrierOf.ts` → `phone/carrierOf.ts` (+ unit test), R
  `features/spaces/services/updatedAgo.ts` → `time/updatedAgo.ts` (+ unit test); M `index.ts`;
  `features/spaces/` — M `hooks/contacts/useContactsSection.ts`, `useReadOnlyContacts.ts`,
  `hooks/editor/usePricesLink.ts`, `useSectionFrame.ts` (imports).
- `shared/map/` — A `components/PlaceMap.tsx` (+ component test), `components/LeafletPlaceMap.tsx`; M
  `index.ts`.
- `features/platform-settings/` (A, new): `index.ts`; `services/platformContact.ts` (+ unit test);
  `components/PlatformContact.tsx` (+ component test); `types/PlatformChannel.ts`.
- `vite-env.d.ts` — M (the two variables); `apps/web/.env.example` — M.
- `features/directory/` — M `repository/directoryRepository.ts` (+ test: `space`, `status`), M
  `hooks/queryKeys.ts`; A `hooks/page/useSpacePageQuery.ts`, `useSpacePage.ts` (+ component test),
  `useGallery.ts` (+ component test); A `hooks/status/useLiveStatusQuery.ts` (+ component test); A
  `services/weekRows.ts` (+ unit test), `priceGroups.ts` (+ unit test), `freshness.ts` (+ unit test),
  `contactLinks.ts` (+ unit test), `localText.ts` (+ unit test), `straightLine.ts` (+ unit test); A
  `types/SpacePageView.ts`,
  `PriceGroupView.ts`; A `components/page/SpaceDetails.tsx` (+ component test), `SpaceHeader.tsx`,
  `StatusPanel.tsx`, `Section.tsx`, `PricesSection.tsx`, `HoursSection.tsx`, `AmenitiesSection.tsx`,
  `AboutSection.tsx`, `LocationSection.tsx`, `ContactList.tsx`, `UnverifiedNotice.tsx`, `ContactBar.tsx`,
  `Gallery.tsx`, `PageSkeleton.tsx`; M `index.ts`.
- `pages/site/` — M `routes.tsx` (the space's route), `navigation.ts` (`spacePath`), A
  `public/space/SpacePage.tsx`, M `routes.component.test.tsx`; M `public/directory/DirectoryPage.tsx`
  (`spaceLink` from `spacePath`).
- `shared/copy/{english,arabic}/` — M `directory.ts`, `site.ts`; A `platformSettings.ts`; M `index.ts` ×2.
- Docs — M `directory.md`, `architecture.md`, `docs/development/setup.md`, `overview.md`, `docs/README.md`,
  finding `40-…md` (evidence line); A `131-the-space-page-cannot-show-a-closures-notice.md`; M findings
  `README.md`.

### PR 4
- `shared/design-system/` — M `icons/iconSet.tsx` (`WifiOffIcon`), `icons/index.ts`, `index.ts`; the showcase's
  icon section if it lists the set (`pages/showcase/sections/icons/IconsSection.tsx`).
- `shared/routing/` — M `states/RetryState.tsx`, `states/RouteErrorState.tsx`; A
  `states/RetryState.component.test.tsx` (or M the existing test that covers it).
- `features/directory/` — A `hooks/home/useHomeSpaces.ts` (+ component test), `hooks/home/useAreaCounts.ts`
  (+ component test), `components/home/HomeSpaces.tsx`; M `index.ts`.
- `features/lookups/` — A `hooks/area/usePublicAreas.ts` (+ component test); M `index.ts`.
- `pages/site/` — M `public/home/HomePage.tsx`; A `public/home/HomeSearch.tsx`, `public/home/AreaCards.tsx`,
  `public/home/useAreaCards.ts` (+ component test), `public/home/OwnersCard.tsx`; M
  `public/about/AboutPage.tsx`; A `public/about/StatusLegend.tsx`; A `shell/SiteRouteError.tsx`; M
  `routes.tsx` (the site's boundary), `shell/SiteFooter.tsx`, `navigation.ts` (`OWNERS_ANCHOR`,
  `SITE_PATHS.owners`), `routes.component.test.tsx`.
- `shared/copy/{english,arabic}/` — M `site.ts`, `status.ts`, `directory.ts`, `lookups.ts`.
- Docs — M `directory.md`, `lookups.md`, `architecture.md`, `foundation.md` (§12, the icon), `overview.md`,
  `docs/README.md`.

### Shared with the other open items

- **OWNER_SETUP PR 3** (worker A, merged before PR 1 starts): it edits `shared/copy/*/index.ts`,
  `docs/frontend/architecture.md`, `docs/project/overview.md`, `docs/README.md` and the findings index. It merges
  first, so these are **text conflicts only if it is still open** — §13 check 3 reads the base diff; each side
  keeps its own lines (the catalogue's section list, the *Built* lines, the map's lines).
- **Worker B's DESK PR 4 and step 8 (API)**, in parallel: **no code file is shared** (this item touches no
  `apps/api`, `packages/shared`, or `shared/copy/*/errors.ts`). Shared documents, each side in its own part
  (workflow §9, the fast path): `docs/project/overview.md` (*Built* lines), `docs/plans/v1-mvp.md` (not edited
  here unless §14.2's line is approved), the findings index (B appends its own numbers). If DESK or step 8
  changes `packages/shared/src/directory`, `lookups`, `occupancy` or `spaces`' responses, or the public
  endpoints, before a PR of this item is pushed — **stop and ask** (§13).

## 8. Design issues (built only once the reply approves them)

Each: the mistake, where it is proven, the fix from the layer's components and tokens. **Points the round-2
reports prove, which the web must not copy, are marked ⟨report · issue⟩.**

### PR 1 — the Directory's list
1. **The skip link leads nowhere** ⟨R2-PU-AX · AX-001⟩: SH-018's link targets `#main`, which no page defines.
   *Fix:* S8 — `<main id="main" tabIndex={-1}>` in the site's shell, the link first in the header.
2. **The filters' button hides whether the sheet is open** ⟨R2-PU-AX · AX-002⟩. *Fix:* the button is the
   `Sheet`'s own trigger (`SheetTrigger asChild`), so Radix sets `aria-expanded` and `aria-controls`; its
   count badge has its words for assistive technology («فلتران مطبّقان»).
3. **The count states something false under a filter** ⟨R2-PU-CP · CP-003⟩: «مساحة واحدة في قطاع غزة» when a
   switch narrowed the list. *Fix:* «… في قطاع غزة» only when nothing narrows the list; with any filter or a
   search, «{n} مساحات مطابقة» (one counted line each, §9).
4. **«عرض 6 نتيجة» / «عرض 0 نتيجة»** ⟨R2-PU-CP · CP-004, and its doubt on P5⟩. *Fix:* the sheet's primary
   counts spaces with Arabic agreement («عرض المساحتين», «عرض 6 مساحات», «عرض 12 مساحة»); with none,
   «لا نتائج — غيّر الفلاتر»; while the count is unknown, «عرض النتائج».
5. **The privacy line where nothing was sent** ⟨R2-PU-CP · CP-001⟩: the denied and imprecise states repeat
   «يُرسَل موقعك…». *Fix:* the line (decision 8's words) shows while locating, while a location is in use, and
   in the map's picking card (PR 2); never in the denied, unavailable or imprecise states.
6. **«الأقرب إليّ» off means two things** ⟨R2-PU-UX · UX-001⟩: Home's clears the location, the Directory's keeps
   it. *Fix:* one meaning everywhere (S4's store, shared by Home): pressing it again, or «إيقاف الترتيب حسب
   المسافة», stops the distance order and keeps the location; «مسح موقعي» alone drops it.
7. **The sort shows a value its list lacks** ⟨R2-PU-CP · CP-022⟩, and the design has no order for a search.
   *Fix:* S10.
8. **«Sort: Recently updated» is clipped** ⟨R2-PU-CP · CP-024⟩. *Fix:* the trigger is `w-full md:w-60`, and
   the order is «الأحدث تحديثًا» / "Latest updates".
9. **Distances: "approximately" on every card, and «1.0 كم»** ⟨R2-PU-CP · CP-018⟩. *Fix:* the card says «على
   بعد 0.7 كم», «على بعد 1 كم», «على بعد 12 كم»; the approximation is said once, in the state line.
10. **The period chips wrap 3 + 1** ⟨R2-PU-VD · VD-002⟩. *Fix:* the four chips are a 2 × 2 grid
    (`grid grid-cols-2`) in the sidebar and the sheet alike.
11. **The price filter's help line reads as a translation** ⟨R2-PU-CP · CP-016⟩. *Fix:* «يُطبَّق «من» و«إلى»
    على سعر {اليوم}», the chosen period named.
12. **The imprecise line says the opposite** ⟨R2-PU-CP · CP-015⟩ («دقته أقل من 2 كم»). *Fix:* «يبدو أن موقعك
    خارج قطاع غزة، أو أن هامش الخطأ فيه أكبر من 2 كم، فلم نستخدمه.»
13. **A cover that fails to load** has no state in the design (only `?photos=failed` in a demo). *Fix:* the
    image's `error` swaps it for the space's mark in the same frame; nothing moves (the frame's ratio is fixed:
    `aspect-2/1` on a phone, `md:aspect-video`).
14. **The filters' count badge counts values** (the prototype adds each area). *Fix:* it counts filters in
    force: the place, the price, «متاحة الآن», «موثّقة», student prices, Friday — six at most.
15. **A search of diacritics only** has no line; the server refuses it. *Fix:* S15.
16. **A verified space with no live status** (no hours, or no capacity) reads as an unverified one. *Fix:*
    the card shows «لا تتوفر حالة مباشرة» for both (true for both); the page says which (PR 3, issue 24).
17. **The card's area names a city in English and a governorate in Arabic** ⟨R2-PU-CP · CP-013⟩. *Fix:* the
    card's area line is `lookups`' `AreaName` from the public catalogue, «{area} · {governorate}» in both
    languages, the governorate's own name (the admin's data) — never a short form.
18. **The Directory's empty directory** has no state in the design (no space at all, nothing narrowing).
    *Fix:* `EmptyState` «لا توجد مساحات في الدليل بعد» with «نضيف المساحات تباعًا؛ عد قريبًا.», no action.

### PR 2 — the map
19. **The map's failure line** is the point picker's («enter the coordinates»), wrong here. *Fix:* `MarkerMap`
    takes its line from the caller: «لم تُحمَّل الخريطة. تصفّح المساحات في القائمة.» with the list a click
    away (the view switch).
20. **Past 1,000 pins** the design says nothing. *Fix:* a muted line over the map's foot, «تظهر أول 1000
    مساحة؛ قرّب الخريطة لترى ما بقي.», while the answer is `truncated`; the viewport's answer replaces it.
21. **The legend's fourth mark** («لا تتوفر حالة مباشرة») covers an unverified space and a verified one with no
    status; the dashed hollow mark is used for both (issue 16).
22. **The phone's selected sheet** must not trap the map (U6). *Fix:* the layer's `Sheet` with `modal={false}`
    if its root passes `modal` through (§13 check 7); if it does not, a bottom `Card` fixed over the map's
    foot, `role="region"` named by the space — and finding 13x records the sheet's missing mode (no
    design-system change in this item).

### PR 3 — the Space details page
23. **The closure's Alert has no data** until step 10 (`PublicSpace` has no announcement). *Fix:* not built;
    the live status says «مغلق الآن» under a closure (the rule's); finding 131; §14.2.
24. **A verified space with no live status** has no line in the design. *Fix:* «لا تتوفر حالة مباشرة» with
    «لم تكتمل معلومات الحالة المباشرة لهذه المساحة بعد.»
25. **«هذه المساحة غير متاحة» for a page not found** ⟨R2-PU-CP · CP-006⟩. *Fix:* «لم نجد هذه المساحة» /
    «ربما أُزيلت من الدليل، أو أن الرابط غير صحيح.»
26. **«فريق مساحة» reads as "the space's team"** ⟨R2-PU-CP · CP-005⟩. *Fix:* «فريقنا» in the unverified notice
    and the contact dialog (and About, PR 4).
27. **«Stale» worded three ways** ⟨R2-PU-CP · CP-008⟩. *Fix:* every section, the prices included: its
    «آخر تحديث لـ… {ago}» then the `warning` badge «قد يكون تغيّر»; the prices add one `warning` Alert
    without a title, «تأكّد من السعر مع المساحة قبل الذهاب.»
28. **Hidden prices: «السعر غير محدّث» with no date** ⟨R2-PU-CP · CP-009⟩. *Fix:* «لا نعرض الأسعار لأنها لم
    تُحدَّث منذ مدة. اسأل المساحة عن السعر الحالي.» on `bg-muted`, with the section's «آخر تحديث للأسعار …».
29. **A shift is «دوام» and «وردية» on one page** ⟨R2-PU-CP · CP-017⟩. *Fix:* the tabs read «اليوم كاملًا» and
    each shift's own name; the hours' line reads «الورديات:»; no «دوام».
30. **Contact labels mix Arabic and Latin** ⟨R2-PU-CP · CP-020⟩. *Fix:* «إنستغرام · فيسبوك · تيك توك» in
    Arabic; the values stay as stored, left to right.
31. **The price grid's orphan cell** ⟨R2-PU-VD · VD-001⟩. *Fix:* the cells of an incomplete last row share
    the row: a two-column grid (`grid-cols-2 md:grid-cols-4`) whose last cell spans what is left
    (`col-span-2` on a phone's odd last; from `md`, `md:col-span-{n}` by the count's remainder — the classes
    listed in `priceGroups`, never computed into a class string).
32. **The gallery's "view all" only from four photos** ⟨R2-PU-VD · VD-004⟩. *Fix:* «عرض كل الصور (n)» on the
    first tile whenever there is more than one photo, at every width.
33. **A group never saved** on the public page: no design. *Fix:* hours `null` → «لم تُضف ساعات العمل بعد»;
    no price → «لم تُضف أسعار بعد»; no amenity, no contact, no description → the section is not drawn (the
    prototype's rule); the status card then has no contacts and the phone no bottom bar.
34. **The heart and the report** (decision 4): the title row holds the name alone; the page ends with its last
    section, no border line or empty row where «الإبلاغ عن معلومة غير صحيحة» stood.
35. **«قواعد المساحة»** in the prototype's About section: the API has no such field. *Fix:* not drawn.

### PR 4 — Home, About, errors
36. **Owners are told they set the live status** ⟨R2-PU-CP · CP-007⟩. *Fix:* Home's owners' card and About's
    step 3 say the status shows automatically from the check-ins (§9 words).
37. **Home names one control two ways** ⟨R2-PU-CP · CP-012⟩. *Fix:* the heading «المساحات الأقرب إليك».
38. **«خطأ في الموقع» on About** ⟨R2-PU-CP · CP-021⟩, and it promises a reply to a report (none in v1 yet).
    *Fix:* «راسلنا إن كان لديك سؤال، أو مشكلة في الموقع الإلكتروني.»
39. **«لم يكن الخطأ منك.»** ⟨R2-PU-CP · CP-023⟩. *Fix:* «المشكلة عندنا، لا عندك. حاول مرة أخرى بعد قليل.»
    (both shells read `status.error`).
40. **The hero's «غزة»** ⟨R2-PU-CP · CP-013⟩. *Fix:* «اعثر على مساحة عمل في قطاع غزة».
41. **About's legend teaches «report from the space's page»**, a button v1 does not draw yet (decision 4).
    *Fix:* «إن وجدت معلومة خاطئة، تواصل معنا.» linking `#contact`.
42. **The footer has no way back to browsing** ⟨R2-PU-UX · UX-008⟩. *Fix:* «تصفّح المساحات» first among the
    footer's links.
43. **The offline state's icon** is the error's (PU-024 settled; the layer has none). *Fix:* the layer's icon
    set gains `WifiOffIcon` (Lucide's `WifiOff`, not mirrored), used by `RetryState` for offline.
44. **The contact's WhatsApp** is unknown until the owner gives it (decision 5). *Fix:* About's two sections
    and the space page's dialog draw each configured channel and nothing else; with none, the dialog says «لا
    توجد وسيلة تواصل متاحة الآن.», and About's sections keep their text without buttons.

**Not built, the reports' own improvements** (each a Proposed alternative, §5): R2-PU-CP-002 (A1), the feminine
states (A2), UX-006 (A3), UX-007 (A4), UX D1 (A5), UX D2 (A6), VD-003 (A7). Not applicable to v1's web:
R2-PU-UX-002, UX-003, UX-004, R2-PU-CP-010, CP-011, CP-019 (the heart and the report, decision 4).
R2-PU-UX-005 (Home's search dropping `lang`/`theme`) cannot occur: the language and the theme are not in the
URL (localisation › resolution), and the search navigates within the app.

## 9. What is built — interfaces, words, states

Words: Arabic first, then English. A counted line gives `arabicPlural` all six forms and `englishPlural`
`one`/`other` (`shared/copy/plural.ts`); every line is in both catalogues; each Arabic section `satisfies
Catalogue['<section>']`. A value set in a sentence is isolated (`isolate` from `shared/localisation`; a name with
`lineParts` where its language may differ). A time range, a price, a distance's number and a count of pages are
left to right. **The owner approves every Arabic line below** (localisation › Catalogues; §14.6).

### PR 1 · Commit 1 — `refactor(space-links): share the list's pages`
- `shared/lists/index.ts`: `export { ListPagination } from './components/ListPagination'; export {
  paginationView } from './services/paginationView'; export type { PaginationView } from
  './types/PaginationView'; export { usePausedSearch } from './hooks/usePausedSearch';` — each moved as it is
  (`pageItems` stays internal; its unit test moves with it). The seven `space-links` importers read
  `@shared/lists`.
- No behaviour change: every `space-links` test passes unchanged but for its imports.
- Docs: `architecture.md` §1's zone table (`shared/` gains `lists`) and the status line («`shared/lists`' list
  pages and paused search (§1)» among the built modules).

### PR 1 · Commit 2 — `refactor(spaces): share the name and clock rules`
- `shared/lib/names/spaceName.ts`: `spaceNameOf(space: { nameEn: string; nameAr: string | null }, english:
  boolean): SpaceNameView`; `shared/lib/names/SpaceNameView.ts`: `SpaceNameView = { text: string; lang?: 'en';
  dir?: 'ltr' }`; `shared/lib/time/clockOf.ts`: `clockOf(minute: number): string` (`510` → `08:30`, `1440` →
  `24:00`). `shared/lib/index.ts` exports the three. `features/spaces/services/clockTime.ts` imports `clockOf`
  and keeps `minuteOf` and `settledClock`.
- No behaviour change. Docs: `architecture.md`'s status line («`shared/lib`'s money, name and clock helpers»).

### PR 1 · Commit 3 — `feat(site): add a skip link and focus each page`
- `pages/site/shell/SkipLink.tsx`: `<a href="#main">` with `copy.site.skipToContent`, hidden until focused:
  `sr-only focus-visible:not-sr-only focus-visible:fixed focus-visible:start-4 focus-visible:top-2
  focus-visible:z-sticky focus-visible:rounded-md focus-visible:bg-background focus-visible:px-4
  focus-visible:py-2 focus-visible:text-primary focus-visible:outline-2 focus-visible:outline-ring` (layout and
  semantic roles only).
- `SiteLayout`: `<SkipLink />` first, then the header; `<main id="main" tabIndex={-1} className="flex flex-1
  flex-col outline-none">`; `useMainFocus()`.
- `pages/site/shell/useMainFocus.ts`: `useMainFocus(): void` — on a change of `useLocation().pathname`, never
  the first render, `document.getElementById('main')?.focus({ preventScroll: true })`.
- Words (`site`): `skipToContent` «تخطَّ إلى المحتوى» / "Skip to content".
- Docs: `architecture.md` §2 › *The site's shell* («the skip link to the page's `main`, first; a new page moves
  the focus to `main` ({date}, #PRNUM)»); finding 130 (Open): the dashboard's two shells lack SH-018's link;
  *Resolves when* a dashboard item adds it to `DashboardLayout`.

### PR 1 · Commit 4 — `feat(lookups): offer the public areas to the site`
- `AreaName({ areaId, source }: { areaId: number; source: LookupsSource })`, `useAreaName(areaId, source)`:
  `public` reads `useCatalogueQuery()` only (the admin's lists never enabled); `admin` as today. The line is
  today's `lookups.areaName({ area, governorate })`; empty while loading or failed. `SpaceEditPage` (and any
  caller `git grep` finds) passes `source="admin"`.
- `AreaFilter({ value, onValueChange }: { value: readonly number[]; onValueChange: (ids: number[]) => void })`:
  a `Field` labelled `areaFilter.label` holding `Combobox type="multiple"` (values as strings, handed back as
  numbers); `ComboboxTrigger empty={value.length === 0}` showing the summary; `ComboboxContent` with
  `searchLabel`, `searchPlaceholder`, `listLabel`, `emptyText`, `loading`; one `ComboboxGroup` per governorate
  that has an area, its heading the governorate's name, each `ComboboxItem value={String(id)}
  keywords={[nameAr, nameEn]}` named in the interface's language.
- `useAreaFilter({ value })` → `{ label, summary, groups: { key: number; heading: string; items: { value:
  string; text: string; keywords: string[] }[] }[], loading: string | null, failure: { line: string; retry: {
  label: string; run: () => void } } | null }`. The summary: none → `all`; one → that area's name (an id the
  catalogue does not hold → `chosen(1)`); more → `chosen(n)`. The failure's line and «إعادة المحاولة» stand in
  the list's empty text.
- Words (`lookups.areaFilter`):

| key | ar | en |
|---|---|---|
| `label` | المنطقة | Area |
| `all` | كل المناطق | All areas |
| `chosen(n)` | one «منطقة واحدة محددة» · two «منطقتان محددتان» · few «{n} مناطق محددة» · many «{n} منطقة محددة» · zero/other «{n} منطقة محددة» | one «1 area chosen» · other «{n} areas chosen» |
| `search` / `searchPlaceholder` | ابحث عن منطقة / اسم المنطقة | Search for an area / Area name |
| `list` / `none` | المناطق / لا توجد منطقة بهذا الاسم | Areas / No area by that name |
| `loading` / `failed` | جارٍ تحميل المناطق… / تعذّر تحميل المناطق | Loading the areas… / We couldn’t load the areas |

  («إعادة المحاولة» is `status.retry`.)
- Docs: `lookups.md` — *Who uses it* (anyone, on the site's Directory, through the page); *Behaviour* «**The area
  filter**» (grouped, multiple, both names searched, its states) and `AreaName`'s source; *Web decisions*
  («**The site's Directory filters by `lookups`' `AreaFilter` and names a card's area with `AreaName` on the
  public source, both set by the page** (S7). *Why:* no feature imports another; the governorate is the
  catalogue's. {date}, #PRNUM.»); code map (`AreaFilter`).

### PR 1 · Commit 5 — `feat(directory): list the spaces page by page`
- **Repository** `DirectoryRepository` (`createDirectoryRepository()`, made once per hook module):
  `list(request: DirectoryRequest, near: NearPoint | null): Promise<Page<DirectorySpace[]>>` →
  `api.getPage<DirectorySpace[]>('/spaces', { params: request, headers: near === null ? undefined : {
  [NEAR_HEADER]: nearHeader(near) } })`. (`near` is always `null` until commit 7.)
- **Keys** (`hooks/queryKeys.ts`): `directoryKeys.all = ['public', 'directory']`; `directoryKeys.list(request,
  near) = ['public', 'directory', 'list', request, near]`; `hasNear(key)` — whether a list key holds a point
  (`key[4] !== null`), for commit 7.
- **`types/DirectoryFilters.ts`**: `{ q: string | undefined; areas: number[]; period: PricePeriod; min: number |
  undefined; max: number | undefined; availableNow: boolean; verified: boolean; studentPrices: boolean;
  openFriday: boolean; sort: 'updated' | 'name' | 'relevance' | undefined; page: number }` (`view` in PR 2).
- **`services/filtersOf.ts`**: `filtersOf(params: URLSearchParams): DirectoryFilters` — S5's keys; a value the
  server would refuse falls back: `area` kept only if every part is a positive whole number and there are at
  most 50 (else `[]`), duplicates dropped; `period` one of `PRICE_PERIODS` (else `DAY`); `min`/`max` whole
  numbers 1–100,000 (else none); a flag only `'1'`; `sort` one of the three, `relevance` only with `q`; `page`
  a whole number ≥ 1 (else 1); `q` through `searchOf`. `paramsOf(filters): URLSearchParams` writes no default
  (`period` only with a bound, `page` from 2, `sort` only when it differs from the default for `q`).
  `searchOf(text): { q: string | undefined; refused: boolean }` — trimmed empty → none; else
  `directoryQuerySchema.safeParse({ q: text })`: its `q`, or `refused: true` and none (S15).
- **`services/requestOf.ts`**: `requestOf(filters, language): DirectoryRequest` (the type beside it: the API's
  query, `limit: 20`): `area` the ids joined by commas; `period`, `priceMin = min × 100`, `priceMax = max × 100`
  only with a bound; `studentPrices`, `openFriday`, `verified`, `availableNow` only when `true`; `q`; `sort` only
  when chosen; `lang` only with `sort: 'name'`; `page` from 2.
- **`hooks/list/useDirectoryFilters.ts`** (as `useAdminSpacesFilters`, on `useSearchParams`): `{ filters, search:
  { text, change, refused }, apply(change: Partial<DirectoryFilters>), clearAll(), searchOf(page): string,
  replacePage(page), applied: number, anyApplied: boolean }` — a change replaces the address (`replace: true`)
  and returns to page 1; the search reaches the address once typing pauses (`usePausedSearch`); `applied`
  counts the place, the price, «متاحة الآن», «موثّقة», student prices, Friday (design issue 14);
  `anyApplied` adds the search.
- **`hooks/list/useDirectoryQuery.ts`**: `useQuery<Page<DirectorySpace[]>, AppError>({ queryKey, queryFn,
  placeholderData: keepPreviousData })` (S13); the app's defaults otherwise (decision 3).
- **`hooks/list/useDirectoryList.ts`** → the list's view:
  ```ts
  type DirectoryListView = {
    search: { label: string; placeholder: string; text: string; change: (text: string) => void; error: string | null };
    sort: { label: string; valueText: string; value: string; options: { value: string; label: string }[]; choose: (value: string) => void };
    count: string;                       // '' until the first answer
    results: {
      heading: string; busy: boolean;    // busy: a fetch in flight over shown cards
      state: 'loading' | 'failed' | 'empty' | 'noMatch' | 'ready';
      cards: SpaceCardView[];
      failure: { title: string; line: string; reference: string | null; retry: { label: string; run: () => void } } | null;
      refreshFailure: … same shape | null;   // a refetch failed over shown cards
      empty: { title: string; text: string };
      noMatch: { title: string; text: string; clear: { label: string; run: () => void } };
    };
    page: number;
    pagination: PaginationView | null;   // paginationView(…, words: directory.pagination)
  };
  ```
  The failure's line is read as every refusal is (`useRefusalView`, `shared/forms`): no connection or no answer
  says so, any other with its reference. `empty` when nothing narrows the list and none comes back; `noMatch`
  when something does. A page past the last (the answer's `totalPages` below `page`, at least one page) is
  replaced by the last (`replacePage`). The count: `count.all(total)` when nothing narrows the list,
  `count.matching(total)` otherwise (design issue 3).
- **`services/cardView.ts`**: `cardViewOf(space: DirectorySpace, { english, now, words }): SpaceCardView`:
  ```ts
  type SpaceCardView = {
    key: number; slug: string; name: SpaceNameView; mark: string;   // mark: the shown name's first character
    areaId: number; cover: string | null;            // the area named by the page's slot
    status: { label: string; variant: 'success' | 'warning' | 'neutral' } | null;  // null → `noStatus`
    noStatus: string; verified: string | null; today: string | null; distance: string | null;
  };
  ```
  `status` from `terms.liveStatuses` (S14); `today` from `todayHours`; `distance` from `distanceText` when the
  answer has `distanceMeters`.
- **`services/todayHours.ts`**: `todayHours(days: (OpeningRange | null)[] | null, now: Date, words):
  string | null` — the weekday of `gazaClockOf(now)` (Sunday 0, as `days`); a closed day → `card.closedToday`;
  0–1440 → `card.openAllDay`; else `card.today({ range })`, the range `clockOf` both ends joined by «–»,
  isolated; `null` days → `null` (nothing drawn).
- **`services/distanceText.ts`**: `distanceText(meters: number, language): string` — kilometres, one decimal
  under 10 and whole from 10, no trailing «.0» (`Intl.NumberFormat`, `ar-u-nu-latn` for Arabic,
  `maximumFractionDigits` 1 or 0) → `card.distance({ km })` (design issue 9).
- **Components:**
  - `DirectoryList(slots: DirectorySlots)` — exported. `DirectorySlots = { spaceLink: (slug: string) =>
    string; areaName: (areaId: number) => ReactNode; placeFilter: (value: number[], onChange: (ids:
    number[]) => void) => ReactNode }` (the last used from commit 6; `areaName` takes an id, since a map's pin
    carries only its area's id). The toolbar (search, then the sort; one
    row from 768 px), the count row, the results, the pages.
  - `DirectorySearch` — a `Field` with a visually hidden label holding `Input type="search"` (`maxLength` 80,
    `SearchIcon` at the start), its error under it.
  - `SortSelect` — `Select` whose trigger is named `sort.label` and shows `sort.value({ sort })`; `w-full
    md:w-60` (design issue 8).
  - `DirectoryResults` — `<section aria-labelledby>` with a visually hidden `h2` (`results`) that takes
    `tabIndex={-1}`; `aria-busy` while fetching; `grid gap-4 md:grid-cols-2 xl:grid-cols-3`. **When the page
    changes** (not on the first render), it focuses that heading and scrolls the section's start into view.
  - `ResultsState` — six `SpaceCardSkeleton`s (`aria-hidden`), the failure (`Alert variant="destructive"`, its
    title, line, reference, `AlertAction` with «إعادة المحاولة»), `EmptyState` for empty and no match.
  - `SpaceCard({ card, href, areaName })` — the whole card one link (React Router `Link`), named by the
    space's name: `block h-full rounded-lg text-foreground focus-visible:outline-2 focus-visible:outline-offset-2
    focus-visible:outline-ring`; inside, `Card` (`h-full overflow-hidden pt-0 hover:bg-accent`):
    `SpaceCover`; the header's title (`h3`, the name with its `lang`/`dir`) and description (the area slot);
    the content: `LiveStatusBadge`, then «موثّقة» (`CircleCheckIcon`, `text-primary`); today's hours and the
    distance (`text-body-sm text-muted-foreground`). No price.
  - `SpaceCover({ cover, mark })` — a frame of fixed ratio (`relative aspect-2/1 w-full overflow-hidden
    bg-muted md:aspect-video`): the cover `<img alt="" loading="lazy" decoding="async" class="size-full
    object-cover">`, which its `error` replaces by the mark (design issue 13); with no cover, the mark (`size-16
    rounded-xl bg-primary text-heading-1 text-primary-foreground`, centred).
  - `LiveStatusBadge({ status, none })` — `Badge` by variant, or `text-body-sm text-muted-foreground` with
    `none`.
- **`DirectoryPage`** (`pages/site/public/directory/`): its `h1` `directory.title`, then `<DirectoryList
  spaceLink={publicSpacePath} areaName={areaName} placeFilter={placeFilter} />`, the two slots made once at
  module level: `(areaId) => <AreaName areaId={areaId} source="public" />`, `(value, onChange) => <AreaFilter
  value={value} onValueChange={onChange} />`. Container `mx-auto flex w-full max-w-7xl flex-col gap-4 px-4 py-6
  md:px-8`.
- **Words** (`directory`, new section):

| key | ar | en |
|---|---|---|
| `title` | مساحات العمل | Workspaces |
| `search.label` / `.placeholder` | ابحث عن مساحة / اسم المساحة أو المنطقة | Search for a space / Space name or area |
| `search.refused` | اكتب حرفًا من اسم المساحة أو منطقتها | Type a letter of the space’s or its area’s name |
| `sort.label` / `sort.value({sort})` | الترتيب / الترتيب: {sort} | Sort / Sort: {sort} |
| `sort.options` | updated «الأحدث تحديثًا» · name «حسب الاسم» · relevance «الأفضل تطابقًا» · distance «حسب المسافة» | Latest updates · By name · Best match · By distance |
| `count.all(n)` | zero «لا توجد مساحات في قطاع غزة بعد» · one «مساحة واحدة في قطاع غزة» · two «مساحتان في قطاع غزة» · few «{n} مساحات في قطاع غزة» · many/other «{n} مساحة في قطاع غزة» | one «1 space in the Gaza Strip» · other «{n} spaces in the Gaza Strip» |
| `count.matching(n)` | zero «لا توجد مساحات مطابقة» · one «مساحة واحدة مطابقة» · two «مساحتان مطابقتان» · few «{n} مساحات مطابقة» · many/other «{n} مساحة مطابقة» | one «1 matching space» · other «{n} matching spaces» |
| `results` | النتائج | Results |
| `loadFailed` / `refreshFailed` | تعذّر تحميل المساحات / تعذّر تحديث القائمة | We couldn’t load the spaces / We couldn’t refresh the list |
| `empty.title` / `empty.text` | لا توجد مساحات في الدليل بعد / نضيف المساحات تباعًا؛ عد قريبًا. | No spaces in the directory yet / We add spaces as we go; come back soon. |
| `noMatch.title` / `noMatch.text` | لا توجد مساحات تطابق ما اخترت / جرّب إزالة بعض الفلاتر أو البحث باسم آخر. | No spaces match your choice / Try removing some filters, or searching for another name. |
| `clearFilters` | مسح الفلاتر | Clear filters |
| `pagination` | label «صفحات المساحات» · previous «السابق» · next «التالي» · page «الصفحة {page}» · summary «صفحة {page} من {total}» · more «صفحات أخرى» | Pages of the spaces · Previous · Next · Page {page} · Page {page} of {total} · More pages |
| `card.verified` | موثّقة | Verified |
| `card.today({range})` / `card.closedToday` / `card.openAllDay` | اليوم {range} / مغلقة اليوم / مفتوحة اليوم على مدار الساعة | Today {range} / Closed today / Open around the clock today |
| `card.distance({km})` | على بعد {km} كم | {km} km away |
| `status.none` | لا تتوفر حالة مباشرة | No live status |

  (The live states are `terms.liveStatuses`: «متاح» · «ممتلئ» · «مغلق الآن».)
- **Docs:** `directory.md` — the header (*Authority*: "…; on the web, the directory's list"; *Scope* adds the
  web feature `features/directory`, any page group); *What it does* (the web's list); *Who uses it* (anyone, on
  the site's «المساحات»); *How it composes* (the page sets `lookups`' area filter and area name in the list's
  slots; the pages from `shared/lists`; the TanStack Query defaults); *Behaviour* «**The directory's list on the
  web**» (the card, the search, the sort, the pages, the states); *Web decisions*: S1, S5, S7's slots, S10,
  S13, S14, S15, decision 7 («the card shows no price»), design issues 3, 7, 9, 13, 16, 17, 18 — each «{date},
  #PRNUM.»; code map *Web*; *Web history*. `architecture.md` — §2 *Built so far* (the site's Directory page,
  composing `directory` with `lookups`), §7 › *Polling* («the directory's lists are never polled: they are
  fetched again on returning to the window once stale, and on a new visit ({date}, #PRNUM)»).
  `overview.md` *Built* (Directory: «on the site, the directory's list: search, sort and pages»).
  `docs/README.md` (directory's line loses "(API only)"). `foundation.md` §5 (S14, if §14.8 approves).

### PR 1 · Commit 6 — `feat(directory): filter by place, price and state`
- **`services/priceBounds.ts`**: `priceBounds(minText: string, maxText: string): { min?: number; max?:
  number; minError?: PriceError; maxError?: PriceError }` with `PriceError = 'invalid' | 'tooHigh' |
  'belowMin'` — Arabic-Indic digits read; blank → none; a whole number of shekels 1–100,000 (else `invalid`,
  or `tooHigh` above); `max < min` → `belowMin` on the maximum, which is then left out.
- **`hooks/filters/usePriceFilter.ts`** (`filters`, `apply`) → `{ label, period: { label, value, options: {
  value, label }[], choose }, min: { label, text, change, error }, max: { … }, help }` — the period applies at
  once; the texts reach the address once typing pauses (400 ms, as the search), only their valid bounds; an
  address changed elsewhere (Back, «مسح») sets the texts again.
- **`hooks/filters/useFiltersPanel.ts`** → `{ wide: boolean; sheet: { open, setOpen, title, description,
  applied: string, count: number, show: string, clear: { label, disabled, run } }; sidebar: { title, clear } }`
  — `wide = useMediaQuery('(min-width: 1024px)')` (S6); `count` = `applied`; `show`: `filters.showLoading` while
  the total is unknown, `filters.showNone` at 0, else `filters.show(total)`.
- **Components:** `FiltersForm({ place, price, spaces, others })` — the place slot; «المساحات», a group named
  by its label (`role="group"`, `aria-labelledby`) with two horizontal `Field`s holding `Switch`es and its note;
  `PriceFilter` (a group «السعر»: the period's `ToggleGroup type="single"` laid out `grid grid-cols-2`, design
  issue 10; «من» and «إلى» side by side, `Input dir="ltr" inputMode="numeric"` with «₪» at the start, each
  its error; the help line); «أخرى», a `Field` holding `ToggleGroup type="multiple"`. `FiltersSidebar` —
  from 1024 px, `<aside id="directory-filters" aria-label>` (`lg:col-span-3`), a `Card` with its title and a
  ghost «مسح» (disabled when nothing applies). `FiltersSheet` — below 1024 px, the `Sheet`'s trigger
  (`SheetTrigger asChild`, an outline `Button` «الفلاتر» with a `primary` `Badge` of the count, hidden from
  assistive technology, and the `applied` words visually hidden — design issue 2); `SheetContent side="bottom"`
  with its title, description, the form, and a footer: the primary `show` (`size="lg" w-full`, closes) and the
  ghost «مسح الفلاتر» (`w-full`, disabled when nothing applies). The list's layout from 1024 px: `lg:grid
  lg:grid-cols-12 lg:items-start`, the results `lg:col-span-9`.
- **Words** (`directory.filters`):

| key | ar | en |
|---|---|---|
| `title` / `description` | الفلاتر / تُطبَّق فورًا على النتائج | Filters / Applied to the results right away |
| `applied(n)` | zero «لا فلاتر مطبّقة» · one «فلتر واحد مطبّق» · two «فلتران مطبّقان» · few «{n} فلاتر مطبّقة» · many «{n} فلترًا مطبّقًا» · other «{n} فلتر مطبّق» | one «1 filter applied» · other «{n} filters applied» |
| `show(n)` / `showNone` / `showLoading` | one «عرض المساحة» · two «عرض المساحتين» · few «عرض {n} مساحات» · many/zero/other «عرض {n} مساحة» / لا نتائج — غيّر الفلاتر / عرض النتائج | one «Show 1 space» · other «Show {n} spaces» / No results — change the filters / Show results |
| `clear` / `close` | مسح / إغلاق | Clear / Close |
| `spaces` / `availableNow` / `verified` | المساحات / متاحة الآن فقط / المساحات الموثّقة فقط | Spaces / Available now only / Verified spaces only |
| `availableNote` | تشمل «متاحة الآن» المساحات الموثّقة فقط. | “Available now” covers verified spaces only. |
| `price` / `period` / `from` / `to` | السعر / الفترة / من / إلى | Price / Period / From / To |
| `periods` | HOUR «ساعة» · DAY «يوم» · WEEK «أسبوع» · MONTH «شهر» | Hour · Day · Week · Month |
| `rangeHelp({period})` + `periodPrices` | يُطبَّق «من» و«إلى» على سعر {period} — HOUR «الساعة» · DAY «اليوم» · WEEK «الأسبوع» · MONTH «الشهر» | From and To apply to the {period} price — hour · day · week · month |
| `priceErrors` | invalid «اكتب مبلغًا بالشيكل أكبر من صفر» · tooHigh «اكتب مبلغًا حتى 100,000 ₪» · belowMin «أقل من الحد الأدنى» | Enter an amount in shekels, above zero · Enter an amount up to ₪100,000 · Below the minimum |
| `other` / `studentPrices` / `openFriday` | أخرى / أسعار للطلاب / مفتوحة يوم الجمعة | Other / Student prices / Open on Friday |

- **Docs:** `directory.md` *Behaviour* (the filters: the place, the price as a budget, the two switches,
  «أخرى»; the sidebar from 1024 px, the sheet below), *Web decisions* (S6, S9, design issues 2, 4, 10, 11, 14;
  «**The budget is whole shekels in the address (`min`, `max`), sent as agorot**» — S5), *Web history*;
  `foundation.md` §3 (the layer's public surface adds `useMediaQuery`).

### PR 1 · Commit 7 — `feat(directory): sort the spaces nearest first`
- **`types/NearState.ts`**: `NearPoint = { lat: number; lng: number }` (rounded); `NearState = { status: 'idle' |
  'locating' | 'granted' | 'denied' | 'imprecise'; point: NearPoint | null; source: 'device' | 'pin' | null;
  sorting: boolean }` (PR 2 adds `picking` and the point before it).
- **`hooks/near/nearMeStore.ts`**: a Zustand store at module level, internal to the feature, never persisted:
  `locating()`, `granted(point, source)` (sorting on), `refused(status)`, `stopSorting()`, `sortAgain()`,
  `clear()` (back to `idle`, no point). It holds only `NearState` (S4).
- **`services/nearPoint.ts`**: `MAX_ACCURACY_METRES = 2000`; `roundedPoint({ latitude, longitude }): NearPoint`
  (each to `NEAR_DECIMALS` decimals: `Math.round(x × 10³) / 10³`); `judgePosition(coords: { latitude: number;
  longitude: number; accuracy: number }): { status: 'granted'; point: NearPoint } | { status: 'imprecise' }` —
  imprecise when `accuracy` is above 2,000 m, or the rounded point is outside `isInGazaStrip`;
  `nearHeader(point): string` (`"31.521,34.452"`).
- **`hooks/near/useNearMe.ts`** → `{ state: NearState; press(): void; stop(): void; clear(): void }`. `press`:
  sorting → `stopSorting`; a point → `sortAgain`; else, with no `navigator.geolocation` → `refused('denied')`,
  otherwise `locating()` and `getCurrentPosition(success, failure, { enableHighAccuracy: true, timeout: 8000,
  maximumAge: 300000 })`: the success hands `position.coords` to `judgePosition` and keeps only its answer; any
  failure → `refused('denied')`. **The location is asked only on `press`, never on load.** `clear()`: the
  store's `clear`, then `queryClient.removeQueries({ queryKey: directoryKeys.all, predicate: (query) =>
  hasNear(query.queryKey) })`.
- **`hooks/near/useLocationStatus.ts`** (`{ chooseArea }`) → `{ kind: 'none' } | { kind: 'locating'; line;
  privacy } | { kind: 'granted'; line; approximate; privacy; stop: { label; run } | null; clear: { label; run }
  } | { kind: 'denied' | 'imprecise'; title; text; fallbacks: { label; run }[] }` — the privacy line only in
  `locating` and `granted` (design issue 5); `granted`'s line by the source and whether it sorts; `stop` only
  while sorting.
- **The list:** while `sorting` and a point is held, the request is sent with `sort: 'distance'` (no `lang`)
  and the point in `Masaha-Near`; the sort's options gain `distance`, chosen; choosing another order calls
  `stop()` and writes that order (S10). Each card's distance from `distanceMeters`.
- **Components:** `NearMeButton({ on, locating, label, press })` — `Button size="sm" variant={on ? 'secondary'
  : 'outline'} aria-pressed={on} loading={locating}`. `LocationStatus({ view })` — `locating`: a `role="status"`
  caption line with the privacy line; `granted`: a caption line («مرتبة حسب المسافة من موقعك.» + «المسافات
  تقريبية بخط مستقيم.» + the privacy line) and `link`-variant buttons «إيقاف الترتيب حسب المسافة», «مسح
  موقعي»; `denied`/`imprecise`: `Alert variant="warning"` with its title, text and the fallbacks as outline
  small buttons in `AlertAction`. The count row: the count (`aria-live="polite"`) at the start, `NearMeButton`
  at the end; `LocationStatus` under it.
- **«اختر منطقتك»** (`chooseArea`): from 1024 px, scrolls `#directory-filters` into view and focuses its first
  control (the place filter); below it, opens the filters' sheet.
- **Words** (`directory.near`):

| key | ar | en |
|---|---|---|
| `button` / `locating` | الأقرب إليّ / جارٍ تحديد موقعك… | Nearest to me / Finding your location… |
| `privacy` | يُرسَل موقعك مقرَّبًا لترتيب المساحات حسب المسافة فقط، ولا يُحفظ. | Your location is sent rounded, only to sort spaces by distance, and is never stored. |
| `sorted.device` / `sorted.pin` | مرتبة حسب المسافة من موقعك. / مرتبة حسب المسافة من الموقع الذي حدّدته على الخريطة. | Sorted by distance from your location. / Sorted by distance from the point you set on the map. |
| `distances.device` / `distances.pin` | المسافات من موقعك. / المسافات من الموقع الذي حدّدته على الخريطة. | Distances from your location. / Distances from the point you set on the map. |
| `approximate` | المسافات تقريبية بخط مستقيم. | Distances are approximate, in a straight line. |
| `stop` / `clear` | إيقاف الترتيب حسب المسافة / مسح موقعي | Stop sorting by distance / Clear my location |
| `denied.title` / `denied.text` | تعذّر تحديد موقعك / اختر منطقتك لتصفّح مساحاتها. | We couldn’t find your location / Choose your area to browse its spaces. |
| `imprecise.title` / `imprecise.text` | تعذّر تحديد موقعك بدقة / يبدو أن موقعك خارج قطاع غزة، أو أن هامش الخطأ فيه أكبر من 2 كم، فلم نستخدمه. | We couldn’t find your location precisely / Your position seems to be outside the Gaza Strip, or off by more than 2 km, so we didn’t use it. |
| `chooseArea` | اختر منطقتك | Choose your area |

  (`sorted.pin` and `distances.pin` are used from PR 2.)
- **Docs:** `directory.md` *Behaviour* «**Near me on the web**» (asked on press only; rounded before it is kept;
  memory only; the header with the distance order only; stop and clear; the states and the privacy line),
  *Web decisions* (S4, decision 8, design issues 5, 6, 12), *Web history*; `architecture.md` §3 › *Where state
  lives* («the device's location for near me → memory only, the rounded point, in `directory`'s store; never
  the URL or the browser's storage ({date}, #PRNUM)»); `overview.md`'s Directory line adds «near me».

### PR 2 · Commit 1 — `feat(map): show many marks and pick a centre`
- **`types/MapMark.ts`**: `MapMark = { shape: 'filled' | 'bar' | 'hollow' | 'dashed'; tone: 'success' |
  'warning' | 'neutral' | 'muted' }`.
- **`types/MarkerMapProps.ts`**:
  ```ts
  type MapMarker = { id: number; point: MapPoint; mark: MapMark; label: string;   // label: the button's name
                     name: { text: string; lang?: 'ar' | 'en' } };                // shown on the selected one and on hover
  type MarkerMapProps = {
    markers: MapMarker[]; selectedId: number | null; onSelect: (id: number) => void;
    bounds: MapBounds;                                   // where it opens, fitted
    user: { point: MapPoint; label: string } | null;     // the visitor's point, a picture named by `label`
    focus: { point: MapPoint; place: 'centre' | 'upper' } | null;  // brought into view; `upper` above a bottom sheet
    pick: { onPick: (point: MapPoint) => void; keys: string } | null;  // a crosshair at the centre; a tap places too
    onViewChange: ((bounds: MapBounds) => void) | null;  // after each move, the box in view
    label: string; failed: string;                       // the map's name; its line when it cannot load
    overlay: (map: { centre: () => MapPoint; showUser: () => void }) => ReactNode;  // drawn over the map
  };
  ```
- **`services/markClass.ts`**: `markClass(mark: MapMark, selected: boolean): string` → `map-mark
  map-mark-{shape} map-tone-{tone}` and ` map-mark-selected`.
- **`MarkerMap(props)`** (exported): `Suspense` with a `Skeleton` of the map's size (`h-120 w-full rounded-xl
  lg:h-160`) around the lazy `LeafletMarkerMap`; its code failing to arrive → `MapFailed` with `failed`.
  **`LeafletMarkerMap`**: `dir="ltr"` box; `MapContainer` fitted to `bounds`, held within it at a quarter's
  margin, the zoom at the start and the attribution at the end in either language (as the picker); Leaflet's
  keyboard on (the container pans with the arrows); each marker a `divIcon` (`html: '<span></span>'`, its
  classes `markClass`), `keyboard: true`, its element given `role="button"`, `aria-label={label}` and
  `aria-pressed={selected}` once mounted (as the picker names its pin), a click or Enter → `onSelect`; a
  `Tooltip` with the name, `permanent` on the selected marker, `aria-hidden`; the user's point a `divIcon`
  `map-user`, `role="img"`, `aria-label`; `pick` → `.map-crosshair` over the centre, a click places, the
  markers out of the tab order; `onViewChange` on `moveend`; `focus` → `panTo` (for `upper`, the point is put a
  quarter of the box above the centre); `useTileStatus` → `MapFailed` with `failed`.
- **`MapMarkSample({ mark })`** (exported): a `span` of the mark's classes, `aria-hidden` — the legend's marks,
  drawn inside the map's overlay, where `leaflet.css` has arrived.
- **`MapFailed`** takes its line (`line: string`); `PointPicker` passes `copy.map.failed` (no change for it).
- **`leaflet.css`**: `.map-mark` (a 16 px dot, a 2 px border on `card`), `-filled` (filled with its tone),
  `-bar` (filled, with a `card` bar across its middle), `-hollow` (`card` fill, a 2 px border of its tone),
  `-dashed` (`card` fill, a dashed border); tones `success`, `warning`, `muted-foreground` (`neutral` and
  `muted`); `.map-mark-selected` (a 3 px `primary` outline and `--elevation-floating`, never a fill; U6);
  `.map-user` (a `primary` dot ringed `card`); `.map-crosshair` (a centred cross on `foreground` with a `card`
  halo); the tooltip on `card`/`card-foreground`, `--elevation-floating`. Every colour a semantic token.
- Docs: `architecture.md` §6 (*Built:* `MarkerMap`; "space markers and popups belong to `directory`" becomes
  «what a mark means belongs to `directory`; `shared/map` draws marks the caller names by shape and tone»
  — S12, {date}, #PRNUM); `foundation.md` §3's `leaflet.css` line (the marks, the crosshair).

### PR 2 · Commit 2 — `feat(directory): show the spaces on a map`
- **Repository** `pins(request: PinsRequest): Promise<MapPins>` → `api.get<MapPins>('/map/spaces', { params:
  request })`; `PinsRequest` = the list's filters (no sort, page, language or limit) and `bounds?: string`
  (`boundsText(bounds)` → `"south,west,north,east"`). Keys: `directoryKeys.pins(request) = ['public',
  'directory', 'pins', request]`.
- `DirectoryFilters.view: 'list' | 'map'` (`view=map`, else the list); `filtersOf`/`paramsOf` read and write it;
  a change of view keeps every filter.
- **`services/pinMark.ts`**: `pinMark(status: LiveStatus | null): MapMark` — `AVAILABLE` filled success;
  `FULL` bar warning; `CLOSED` hollow neutral; none dashed muted (U6; design issue 21).
- **`cardViewOf`** takes a `DirectorySpace` or a `MapPin` (the area's id from `area.id` or `areaId`).
- **`hooks/map/usePinsQuery.ts`** (`keepPreviousData`); **`useSelectedPin()`** — the selected pin's id, local
  state, cleared when the filters change; **`useDirectoryMap({ filters, request })`** → `{ map: MarkerMapProps'
  data (markers, selectedId, onSelect, bounds = GAZA_STRIP_BOUNDS, user, focus, onViewChange, label, failed),
  state: 'loading' | 'failed' | 'noMatch' | 'ready', failure, noMatch, truncated: string | null, selected: {
  card: SpaceCardView; close: () => void } | null, phone: boolean }` — `onViewChange` is given only while the
  whole set came back `truncated`; then, after a 400 ms pause, the pins are asked again within the box in view
  (`bounds`), and that answer replaces the marks; `phone = !useMediaQuery('(min-width: 768px)')`; `focus` the
  selected pin, `upper` on a phone.
- **Components:** `ViewSwitch` (exported) — a `Field` whose label is visually hidden («طريقة العرض») holding
  `ToggleGroup type="single"` «قائمة» · «خريطة» (PU-013); `DirectoryView(slots)` (exported, replaces
  `DirectoryList` as the page's export, which becomes internal) — the toolbar, then the list (PR 1) or the map;
  on the map the filters are the sheet at every width and there is no sort (the prototype's). `DirectoryMap` —
  `<section aria-label>` holding `MarkerMap` with, in its overlay: the legend (top-end), «مركّز على موقعي»
  (outline small, while a point is held), the selected card from 768 px, the no-match card, the truncated line;
  below 768 px the selected space is `SelectedSheet`. `MapLegend` — a `ul` named «دليل الخريطة», each item
  `MapMarkSample` and its word. `SelectedCard` — `Card shadow-overlay`, the name (`CardTitle`), the area slot,
  a ghost icon «إغلاق», `LiveStatusBadge`, today and the distance, «عرض التفاصيل» (`Button asChild` → the
  space's link, `w-full`). `SelectedSheet` — the same in `Sheet side="bottom" modal={false}` that never takes
  the focus on open and is not closed by a tap on the map (design issue 22; §13 check 7). `MapNotice` — the
  truncated line.
- **`DirectoryPage`**: a row with the `h1` and `ViewSwitch` (`flex flex-wrap items-end justify-between gap-4`),
  then `DirectoryView`.
- **Words** (`directory.view`, `directory.map`):

| key | ar | en |
|---|---|---|
| `view.label` / `view.list` / `view.map` | طريقة العرض / قائمة / خريطة | View / List / Map |
| `map.label` / `map.region` | خريطة المساحات / الخريطة | Map of spaces / Map |
| `map.pin({name, status})` | {name} — {status} | {name} — {status} |
| `map.legend` | دليل الخريطة | Map legend |
| `map.centre` / `map.you` | مركّز على موقعي / موقعك | Centre on my location / Your location |
| `map.details` / `map.close` | عرض التفاصيل / إغلاق | View details / Close |
| `map.failed` | لم تُحمَّل الخريطة. تصفّح المساحات في القائمة. | The map didn’t load. Browse the spaces in the list. |
| `map.truncated` | تظهر أول 1000 مساحة؛ قرّب الخريطة لترى ما بقي. | Showing the first 1,000 spaces; zoom in to see the rest. |

- **Docs:** `directory.md` *Behaviour* «**The map on the web**» (the pins by state, the legend, the selected
  card and sheet, the viewport's re-ask), *Web decisions* (S12's meaning; U6; design issues 19–22), *Web
  history*; finding 46's evidence (the Directory's map loads the same tiles).

### PR 2 · Commit 3 — `feat(directory): set my location on the map`
- **The store:** `status: 'picking'` and `before: { point; source; sorting } | null`; `startPick()` (keeps what
  was there), `cancelPick()` (restores it, or `idle`), `placePin(point)` (rounded by `roundedPoint`; `granted`,
  source `pin`, sorting on). **`useNearMe`** adds `pickOnMap()` (the map view, then `startPick`), `cancelPick`,
  `placePin(point)`.
- **The map while picking:** the crosshair; the markers out of the tab order and not selectable; «مركّز على
  موقعي», the near-me button and the state line hidden (U7); `PickCard` in the overlay — its title, its text
  with the privacy promise, the keys' line (visually hidden, the map's `aria-describedby`), «ثبّت الموقع هنا»
  (primary, `flex-1`, places `centre()`), «رجوع» (ghost, `cancelPick`). A tap on the map places the point too.
- **The state line:** «حدّد موقعي على الخريطة» joins «اختر منطقتك» in the denied and imprecise states;
  «تغيير الموقع» (a link) beside a pin's line; `denied.text` becomes the prototype's.
- **Words** (`directory.pick`, `directory.near`):

| key | ar | en |
|---|---|---|
| `pick.title` | حدّد موقعك على الخريطة | Set your location on the map |
| `pick.text` | حرّك الخريطة حتى تقع العلامة على مكانك التقريبي، أو اضغط عليه. نرتّب المساحات حسب المسافة منه، ويُرسَل مقرَّبًا ولا يُحفظ. | Move the map until the mark is on your approximate location, or tap it. We sort the spaces by distance from it; it is sent rounded and never stored. |
| `pick.keys` | الأسهم تحرّك الخريطة تحت العلامة في الوسط. | The arrow keys move the map under the mark in the centre. |
| `pick.confirm` / `pick.back` | ثبّت الموقع هنا / رجوع | Set location here / Back |
| `near.pickOnMap` / `near.change` | حدّد موقعي على الخريطة / تغيير الموقع | Set my location on the map / Change location |
| `near.denied.text` (changed) | اختر منطقتك أو حدّد موقعك على الخريطة لنرتّب المساحات حسب المسافة. | Choose your area or set your location on the map to sort the spaces by distance. |
| `map.yourPin` | موقعي (يدوي) | My location (manual) |

- **Docs:** `directory.md` *Behaviour* (placing a point by hand: rounded, kept as the device's is), *Web
  decisions* (U7 as built), *Web history*.

### PR 3 · Commit 1 — `refactor(spaces): share the carrier and date rules`
- `shared/lib/phone/carrierOf.ts` (`Carrier`, `carrierOf(phone)`), `shared/lib/time/updatedAgo.ts`
  (`updatedAgo(iso, language, now)`), moved as they are, exported from `shared/lib`; the four `spaces` importers
  read `@shared/lib`. No behaviour change. Docs: `architecture.md`'s status line (the carrier and date helpers).

### PR 3 · Commit 2 — `feat(platform-settings): read the public contact`
- **`types/PlatformChannel.ts`**: `{ kind: 'whatsapp' | 'email'; value: string; href: string }`.
- **`services/platformContact.ts`**: `contactOf({ email, whatsapp }: { email?: string; whatsapp?: string }):
  PlatformChannel[]` — WhatsApp first: `normalisePhone(whatsapp)` gives the number in its one stored form or it
  is left out; `href` `https://wa.me/{digits}`; then the email, if `emailSchema` takes it, `href`
  `mailto:{email}`. `platformContact(): PlatformChannel[]` reads `import.meta.env.VITE_CONTACT_EMAIL` and
  `VITE_CONTACT_WHATSAPP` on each call (tests set them with `vi.stubEnv`, the platform's seam, as Google's id).
- **`PlatformContact({ layout, none })`** (exported): `layout: 'row' | 'column'` (About's row from 768 px, the
  dialog's column); each channel a `Button asChild` link, the first `primary`, the rest `outline`: its word, then
  its value `dir="ltr"` (muted on outline); WhatsApp opens a new tab (`rel="noopener"`), the email does not;
  with no channel, `none` (or nothing).
- `vite-env.d.ts`: `readonly VITE_CONTACT_EMAIL?: string; readonly VITE_CONTACT_WHATSAPP?: string;`.
  `apps/web/.env.example`: «# The platform's contact, shown on About and to an unverified space's owner: an
  email and a WhatsApp number. Each empty one is not shown.» then `VITE_CONTACT_EMAIL=` and
  `VITE_CONTACT_WHATSAPP=`.
- **Words** (`platformSettings`, new): `contact.whatsapp` «واتساب» / "WhatsApp"; `contact.email` «بريد» /
  "Email".
- **Docs:** `setup.md` › *The web* (a bullet: the two variables, where they show, empty → not shown; online,
  the Vercel project's environment variables, then a redeploy); `architecture.md` §3 (`platform-settings` built:
  the public contact, read from the web's configuration until step 11 — S11, {date}, #PRNUM); finding 40's
  evidence («Since #PRNUM the site reads its contact from `VITE_CONTACT_EMAIL` and `VITE_CONTACT_WHATSAPP`; the
  seeded rows stay unread.»). No capability document yet (no API slice of `platform-settings` is built on the
  web's side; documentation §5's stable core) — the decision lives in `architecture.md` §3.

### PR 3 · Commit 3 — `feat(map): show one place on a map`
- **`PlaceMap({ point, label, failed })`** (exported; lazy as the others): a map centred on `point` (zoom 16),
  the layer's pin (`.map-pin`) on it, **`role="img"`** and `aria-label={label}`, not draggable and not a button
  (PU-026); the zoom and the attribution as the picker's; its failure line `failed`.
- Docs: `architecture.md` §6 (*Built:* `PlaceMap`).

### PR 3 · Commit 4 — `feat(directory): show a space's public page`
- **Repository** `space(slug): Promise<PublicSpace>` → `api.get('/spaces/' + encodeURIComponent(slug))`; keys
  `directoryKeys.space(slug) = ['public', 'directory', 'space', slug]`.
- **`services/localText.ts`**: `localText(ar: string | null, en: string | null, english: boolean): { text:
  string; lang?: 'ar' | 'en'; dir?: 'rtl' | 'ltr' } | null` — the interface's language when there is one, else
  the other, marked.
- **`services/weekRows.ts`**: `weekRows(days, now, words, all: boolean): { rows: { key; label; value; today:
  boolean; closed: boolean }[]; canExpand: boolean }` — Saturday first (indexes 6, 0, 1, …, 5), consecutive days
  with the same range grouped (a pair «{first}، {second}», a run «{first} – {last}»), each its range («08:00–22:00»
  isolated), «مغلقة» or «على مدار الساعة»; `all` lists each day; `canExpand` when the groups are more than two;
  today from `gazaClockOf(now)`.
- **`services/priceGroups.ts`**: `priceGroups(prices, shifts, words, language): { tabs: { key; label; range:
  string | null; audiences: PriceGroupView[] }[] | null; audiences: PriceGroupView[] }` — with any price naming a
  saved shift, tabs: «اليوم كاملًا» (no shift) then each shift with prices, its range; else one set. A
  `PriceGroupView` is `{ title: string | null /* «للطلاب» */; cells: { key; label; value; span: string }[] }`:
  general first, then students; each cell its label in the interface's language (else the other, marked) or its
  period's name, and `priceText(amountAgorot, language)`; `span` from `cellSpan(index, count)` — a fixed table
  of literal classes so an incomplete last row shares its width (design issue 31): phone (`grid-cols-2`) an odd
  count's last cell `col-span-2`; from 768 px (`md:grid-cols-4`) by the count's remainder — 1: the last
  `md:col-span-4`; 2: the last two `md:col-span-2`; 3: the last `md:col-span-2`; other cells `md:col-span-1`
  where a phone span must be undone.
- **`services/freshness.ts`**: `freshnessOf(updatedAt: string | null, stale: boolean, group, now, language,
  words): { line: string | null; stale: string | null }` — `page.updated.{group}({ ago: updatedAgo(…) })`, and
  `page.stale` when the group is in `staleGroups`.
- **`services/contactLinks.ts`**: `contactLinkOf(contact, words): { key; label; value; href; external: boolean }`
  — WhatsApp `https://wa.me/{digits}`, phone `tel:{value}` with its carrier in the label («اتصال — جوال»),
  email `mailto:`, the others their stored `https://` address (`external`).
- **`hooks/page/useSpacePageQuery.ts`**; **`useSpacePage(slug)`** → `SpacePageView`: `{ state: 'loading' |
  'failed' | 'notFound' | 'ready'; failure; notFound: { title; text }; header: { name: SpaceNameView; other: {
  text; lang; dir } | null; areaId; verified: string | null; noPhotos: string | null }; unverified: { text;
  contact: string; dialog: { title; text; close; none } } | null; panel: { today: string | null; distance: string
  | null }; prices: { title; meta (freshness + «للعرض فقط · الدفع في المساحة»); state: 'shown' | 'hidden' |
  'none'; hidden; none; check: string | null /* stale */; groups }; hours: { title; meta; none: string | null;
  rows; canExpand; toggle: { label; expanded; run } }; amenities: { title; meta; items: { key; text; lang?; icon:
  AmenityIconKey | null }[] } | null; about: { title; text } | null; location: { title; meta: null; point;
  mapLabel; failed; address; landmark; directions: { label; href } }; contacts: { title; meta; items } | null;
  bar: { label; whatsapp: { label; href } | null; call: { label; href } | null } | null }` — `notFound` on a 404;
  the profile's date in the unverified line; the distance («نحو 0.7 كم») from the store's point by the straight
  line to `location` (`straightLine`, in `services/`, rounded as the server's to 100 m) when a point is held;
  `bar` only when a WhatsApp or a phone contact exists; `wide = useMediaQuery('(min-width: 1024px)')` (the aside,
  or the status and contacts inline) and `phone = !useMediaQuery('(min-width: 768px)')` (the bar), as S6. **`useSpacePageTitle(slug): PageTitle |
  undefined`** (exported) — the name for the page's title, from the same query.
- **Components:** `SpaceDetails({ slug, areaName, browseLink, ownerContact })` (exported; `ownerContact:
  ReactNode`, the page's `PlatformContact`): its states (`PageSkeleton`; the failure `Alert` with «إعادة
  المحاولة»; `notFound` as an `EmptyState` with «تصفّح المساحات» → `browseLink`); then U8's order: the
  gallery's place (commit 5), `SpaceHeader` (the `h1` name with its `lang`/`dir`, the other name under it, the
  area slot, «موثّقة», «لا توجد صور بعد»), `UnverifiedNotice` (`Alert variant="info"`, its text, `AlertAction`
  an outline small button that opens a `Dialog` with `ownerContact` or its `none` line), below 1024 px
  `StatusPanel` (status only); `PricesSection`, `HoursSection` (a `Card` holding a `Table` with a visually hidden
  caption, «الأيام» / «الساعات» headers, today's row `bg-accent` with a `primary` badge «اليوم» and
  `aria-current="date"`, «عرض كل الأيام» as a link button with `aria-expanded`; the shifts' line under it),
  `AmenitiesSection` (a `ul` of pills: the platform's `GlyphIcon` by its key, the space's own `CheckIcon`, one
  list), `AboutSection`, `LocationSection` (`PlaceMap`, the address and the landmark, «الاتجاهات» an outline
  small link to `https://www.google.com/maps/search/?api=1&query={lat},{lng}` in a new tab), below 1024 px
  `ContactList` as a section; from 1024 px (`wide`) `<aside aria-label>` (`lg:col-span-4`) holding `StatusPanel`
  with the contacts. `Section` — `<section aria-labelledby>` with its `h2` (`text-heading-2`), its body, its meta
  (`text-caption text-muted-foreground`, the stale badge `warning`). `ContactBar` — drawn only below 768 px (`phone`), `fixed inset-x-0
  bottom-0 z-sticky border-t border-border bg-background px-4 py-3`, a named region with «واتساب» (primary) and
  «اتصال» (outline), each `flex-1`; the page then pads its foot (`pb-24 md:pb-0`). Layout: `flex flex-col gap-10
  lg:grid lg:grid-cols-12 lg:items-start lg:gap-8`, the main column `min-w-0 lg:col-span-8`.
- **`pages/site`:** `routes.tsx` — `{ path: SITE_PATHS.space, handle: { title: (copy) => copy.site.links.space
  }, lazy: … SpacePage }` before `*`; `SITE_PATHS.space = '/spaces/:slug'`; `publicSpacePath` stays the one way
  to build its link (`shared/routing`; its comment loses "the site has no page at it yet").
  **`SpacePage`**: `slug` from `useParams()`; `useRecordTitle(useSpacePageTitle(slug))`; from 768 px a
  `Breadcrumb` (named) «الرئيسية» › «المساحات» (with the Directory's last search, `useDirectoryReturn()`) ›
  the name (`BreadcrumbPage`); below 768 px «العودة إلى المساحات» (a link button with `ChevronStartIcon`); then
  `<SpaceDetails slug areaName browseLink={SITE_PATHS.spaces} ownerContact={<PlatformContact layout="column"
  none={…} />} />`. **`useDirectoryReturn(): string`** (exported by `directory`): the Directory's last search
  (`?…`), which `useDirectoryFilters` keeps in the feature's memory on each write (never storage).
- **Words** (`directory.page`, `site.links.space`):

| key | ar | en |
|---|---|---|
| `site.links.space` | صفحة المساحة | Space |
| `page.breadcrumb` / `page.back` | مسار التنقّل / العودة إلى المساحات | Breadcrumb / Back to spaces |
| `page.loadFailed` | تعذّر تحميل صفحة المساحة | We couldn’t load this space’s page |
| `page.notFound.title` / `.text` | لم نجد هذه المساحة / ربما أُزيلت من الدليل، أو أن الرابط غير صحيح. | We couldn’t find this space / It may have been removed from the directory, or the link is wrong. |
| `page.noPhotos` | لا توجد صور بعد | No photos yet |
| `page.unverified.text({ago})` | جمع فريقنا هذه المعلومات، ولم تؤكّدها إدارة المساحة بعد · آخر تحديث للمعلومات {ago} | Our team collected this information; the space hasn’t confirmed it yet · Information updated {ago} |
| `page.unverified.contact` | هل تدير هذه المساحة؟ تواصل معنا | Do you run this space? Contact us |
| `page.dialog.title` / `.text` | تواصل مع فريقنا / أخبرنا أنك تدير هذه المساحة، وسنتواصل معك لتأكيد معلوماتها. | Contact the Masaha team / Tell us you run this space, and we’ll get in touch to confirm its information. |
| `page.dialog.close` / `.none` | إغلاق / لا توجد وسيلة تواصل متاحة الآن. | Close / There’s no way to reach us set up yet. |
| `page.status.title` / `page.statusContact.title` | الحالة / الحالة والتواصل | Status / Status & contact |
| `page.distance({km})` | نحو {km} كم | About {km} km away |
| `page.sections` | prices «الأسعار» · hours «ساعات العمل» · amenities «المرافق» · about «عن المساحة» · location «الموقع» · contacts «التواصل» | Prices · Opening hours · Amenities · About the space · Location · Contact |
| `page.updated.{group}({ago})` | profile «آخر تحديث للمعلومات {ago}» · prices «آخر تحديث للأسعار {ago}» · hours «آخر تحديث لساعات العمل {ago}» · amenities «آخر تحديث للمرافق {ago}» · contacts «آخر تحديث للتواصل {ago}» | Information updated {ago} · Prices updated {ago} · Hours updated {ago} · Amenities updated {ago} · Contacts updated {ago} |
| `page.stale` | قد يكون تغيّر | May have changed |
| `page.prices.displayOnly` / `.students` | للعرض فقط · الدفع في المساحة / للطلاب | Display only · Pay at the space / For students |
| `page.prices.byShift` / `.wholeDay` | الأسعار حسب الوردية / اليوم كاملًا | Prices by shift / Whole day |
| `page.prices.periods` | HOUR «ساعة» · DAY «يوم» · WEEK «أسبوع» · MONTH «شهر» | Hour · Day · Week · Month |
| `page.prices.hidden` | لا نعرض الأسعار لأنها لم تُحدَّث منذ مدة. اسأل المساحة عن السعر الحالي. | We don’t show the prices because they haven’t been updated in a while. Ask the space for the current price. |
| `page.prices.none` / `.check` | لم تُضف أسعار بعد / تأكّد من السعر مع المساحة قبل الذهاب. | No prices added yet / Check the price with the space before you go. |
| `page.hours.caption` / `.days` / `.hours` | ساعات العمل الأسبوعية / الأيام / الساعات | Weekly opening hours / Days / Hours |
| `page.hours.today` / `.closed` / `.allDay` | اليوم / مغلقة / على مدار الساعة | Today / Closed / Around the clock |
| `page.hours.showAll` / `.showLess` | عرض كل الأيام / عرض مختصر | Show all days / Show less |
| `page.hours.dayNames` | sat «السبت» · sun «الأحد» · mon «الاثنين» · tue «الثلاثاء» · wed «الأربعاء» · thu «الخميس» · fri «الجمعة» | Saturday … Friday |
| `page.hours.pair({first,second})` / `.run({first,last})` | {first}، {second} / {first} – {last} | {first}, {second} / {first} – {last} |
| `page.hours.shifts({list})` | الورديات: {list} | Shifts: {list} |
| `page.hours.none` | لم تُضف ساعات العمل بعد | Opening hours not added yet |
| `page.location.directions` / `.map({name})` / `.failed` | الاتجاهات / موقع {name} على الخريطة / لم تُحمَّل الخريطة. | Directions / {name} on the map / The map didn’t load. |
| `page.contacts.types` | WHATSAPP «واتساب» · PHONE «اتصال» · EMAIL «بريد» · INSTAGRAM «إنستغرام» · FACEBOOK «فيسبوك» · TIKTOK «تيك توك» · WEBSITE «الموقع الإلكتروني» | WhatsApp · Call · Email · Instagram · Facebook · TikTok · Website |
| `page.contacts.withCarrier({type,carrier})` / `.carriers` | {type} — {carrier} / jawwal «جوال» · ooredoo «أوريدو» | {type} — {carrier} / Jawwal · Ooredoo |
| `page.bar.label` / `.whatsapp` / `.call` | التواصل السريع / واتساب / اتصال | Quick contact / WhatsApp / Call |

- **Docs:** `directory.md` *Who uses it* (the site's space page), *How it composes* (the page sets the area name
  and the platform's contact; `PlaceMap`), *Behaviour* «**A space's page on the web**» (the order, each section,
  the states, the freshness, the bar), *Web decisions* (U8, U9 as built, U4, design issues 23–35, decision 4),
  code map, *Web history*; `architecture.md` §2 (the space details page built; `publicSpacePath`'s page exists);
  finding 131 (Open: the public page carries no announcement; *Resolves when* step 10 adds them to `GET
  /spaces/:slug` and the page shows a closure's notice); `overview.md`; `docs/README.md`.

### PR 3 · Commit 5 — `feat(directory): show the space's photos`
- **`useGallery(photos, name)`** → `{ tiles: { key; src /* card */; alt; className; view: { label; run } }[];
  layout: string; more: { label; run } | null; viewer: { open; setOpen; title; position; src /* page */; alt;
  previous: { label; run } | null; next: { label; run } | null; close } }` — five tiles at most from 768 px, the
  first alone on a phone; `layout` and each `className` from a fixed table by the count (the prototype's: 1 → one
  column; 2 → two; 3–5 → the first `md:col-span-2 md:row-span-2`), literal classes; `more` whenever there is
  more than one photo (design issue 32); the viewer moves round the photos.
- **`Gallery`** — `null` with no photo (the header's caption says so, PU-023); else the grid of buttons, each
  holding its `<img alt="الصورة {n} من {name}" loading={n === 1 ? 'eager' : 'lazy'}>`; the «عرض كل الصور (n)»
  outline pill on the first tile; a `Dialog` (`sm:max-w-3xl`) titled «صور {name}», its position `dir="ltr"`, the
  page-size image, «السابقة» / «التالية» (`ChevronStartIcon` / `ChevronEndIcon`).
- **Words** (`directory.page.gallery`): `label({name})` «صور {name}» / "Photos of {name}"; `view({n})` «عرض الصورة
  {n}» / "View photo {n}"; `all({count})` «عرض كل الصور ({count})» / "View all photos ({count})"; `photo({n,
  total, name})` «الصورة {n} من {total} — {name}» / "Photo {n} of {total} — {name}"; `previous` «السابقة» /
  "Previous"; `next` «التالية» / "Next"; `close` «إغلاق» / "Close".
- **Docs:** `directory.md` *Behaviour* (the gallery), *Web decisions* (design issue 32), *Web history*.

### PR 3 · Commit 6 — `feat(directory): refresh a space's live status`
- **Repository** `status(slug): Promise<PublicOccupancy>` → `api.get('/spaces/' + encodeURIComponent(slug) +
  '/occupancy')`; keys `directoryKeys.status(slug) = ['public', 'directory', 'status', slug]`.
- **`hooks/status/useLiveStatusQuery(slug)`**: `useQuery({ …, refetchInterval: 60_000, refetchOnWindowFocus:
  'always' })` (decision 3).
- **`StatusPanel`** — verified with a status: `LiveStatusBadge` and «الحالة مباشرة الآن»; verified without:
  «لا تتوفر حالة مباشرة» and `status.unset`; unverified: «لا تتوفر حالة مباشرة» and `status.unverified`; while
  the first read loads, a `Skeleton` the badge's size; a failed read with none before: `status.failed`, the next
  interval trying again; a failed read after one: the last state kept. Today and the distance under it.
- **Words** (`directory.page.status`): `live` «الحالة مباشرة الآن» / "Live right now"; `unverified` «الحالة
  المباشرة تظهر للمساحات الموثّقة فقط» / "Live status is shown for verified spaces only"; `unset` «لم تكتمل
  معلومات الحالة المباشرة لهذه المساحة بعد.» / "This space’s live status isn’t set up yet."; `failed` «تعذّر
  قراءة الحالة الآن» / "We couldn’t read the status just now".
- **Docs:** `architecture.md` §7 › *Polling*: «the live status every 60 s» becomes «a space's page reads its
  live status every 60 s while the page is visible, and on returning to it; the lists are never polled
  (decision 3, {date}, #PRNUM)»; `directory.md` *Web decisions* (decision 3), *Web history*.

### PR 4 · Commit 1 — `feat(routing): offer home and say a failed retry`
- **`RetryState({ kind, onRetry, children })`**: `children` are the caller's other ways on, after «إعادة
  المحاولة» (the site's «الرئيسية»; the dashboard gives none). The retry shows `loading`; offline, while
  `navigator.onLine` is still false, it does not reload: `status.stillOffline` shows under the buttons
  (`role="status"`) and the button is available again. The offline state's icon is `WifiOffIcon`.
  **`RouteErrorState({ children })`** passes them on.
- **`pages/site/shell/SiteRouteError.tsx`**: `<RouteErrorState><Button asChild variant="outline"><Link
  to={SITE_PATHS.home}>{copy.site.links.home}</Link></Button></RouteErrorState>`; the site's two boundaries
  (`SiteLayout`'s and `FocusLayout`'s) use it.
- **The layer:** `WifiOffIcon` in `icons/iconSet.tsx` (Lucide's `WifiOff`, not mirrored), exported; the
  showcase's icon section shows it.
- **Words** (`status`): `error.description` (changed) «المشكلة عندنا، لا عندك. حاول مرة أخرى بعد قليل.» / "The
  problem is on our side, not yours. Try again in a moment."; `stillOffline` «ما زال الاتصال مفقودًا.» / "Still
  no connection."
- **Docs:** `architecture.md` §2 › *status states* (the site's second way on, the retry that stays offline,
  PU-024); `foundation.md` §12 (no change unless the icon list is named there — §13 check).

### PR 4 · Commit 2 — `feat(lookups): list the public areas for home`
- **`usePublicAreas()`** (exported) → `{ areas: { id: number; name: string; governorate: string }[]; state:
  'loading' | 'failed' | 'ready'; retry: () => void }` — the public catalogue's areas, governorate by
  governorate, in its order, named in the interface's language.
- Docs: `lookups.md` (*Who uses it*: Home; the export).

### PR 4 · Commit 3 — `feat(directory): offer home its spaces and counts`
- **`useHomeSpaces()`** → `{ title; near: { button; status }; viewAll: { label; to: 'list' | 'available' };
  state; cards; failure; empty: { title; text; action } }` — while sorting by distance with a point: `GET /spaces`
  `sort=distance`, `limit=6`, the point in its header, titled «المساحات الأقرب إليك» (design issue 37); else
  `availableNow=true`, `limit=6`, «متاحة الآن». Near me as the Directory's (one store, one meaning, design
  issue 6); «حدّد موقعي على الخريطة» starts the pick and opens the Directory's map.
- **`HomeSpaces({ spaceLink, areaName, links: { list: string; available: string; map: string }, chooseArea })`**
  (exported): the section (`aria-labelledby` its `h2`), the button and «عرض الكل» at the row's end, the state
  line, the cards (`grid gap-4 md:grid-cols-2 lg:grid-cols-3`), skeletons, the failure, the empty state with
  «تصفّح كل المساحات».
- **`useAreaCounts()`** (exported) → `{ counts: ReadonlyMap<number, number>; total: number; state; retry }` —
  from `GET /map/spaces` with no filter (the pins' key), counted by `areaId`.
- **Words** (`directory.home`): `available` «متاحة الآن» / "Available now"; `nearest` «المساحات الأقرب إليك» /
  "Spaces nearest you"; `viewAll` «عرض الكل» / "View all"; `empty.title` «لا توجد مساحات متاحة الآن» / "No
  spaces available right now"; `empty.text` «قد تكون المساحات ممتلئة أو مغلقة في هذا الوقت. تصفّح كل المساحات
  لمعرفة ساعات عملها.» / "Spaces may be full or closed at this time. Browse all spaces to see their hours.";
  `empty.action` «تصفّح كل المساحات» / "Browse all spaces".
- Docs: `directory.md` (*Who uses it*: Home; *Behaviour* «Home's spaces»; *Web history*).

### PR 4 · Commit 4 — `feat(site): build the home page`
- **`HomePage`**: the hero (`h1` `text-heading-1 md:text-display`, its lead), `HomeSearch` (a `form
  role="search"`: `Input type="search"` named, «بحث»; on submit, `navigate('/spaces' + (q ? '?q=' +
  encodeURIComponent(q) : ''))`); `HomeSpaces` (`links`: `/spaces`, `/spaces?available=1`, `/spaces?view=map`;
  `chooseArea` scrolls to and focuses the areas' heading, `tabIndex={-1}`); `AreaCards`; `OwnersCard`.
- **`useAreaCards()`** (`pages/site/public/home/`) composes `usePublicAreas` and `useAreaCounts`: the areas with
  at least one space, in the catalogue's order, each `{ key, title, line: «{governorate} · {count}», to:
  '/spaces?area={id}' }`, then «كل المناطق» «قطاع غزة · {total}» → `/spaces`; loading skeletons; a failure of
  either with one «إعادة المحاولة» retrying both.
- **`AreaCards`** — `grid gap-4 md:grid-cols-3`, each a link holding a `Card` (`hover:bg-accent`), `ArrowEndIcon`
  in `CardAction`. **`OwnersCard`** — `Card bg-muted`, its title, text and an outline «تواصل معنا» →
  `/about#owners`.
- **Words** (`site.home`):

| key | ar | en |
|---|---|---|
| `title` / `lead` | اعثر على مساحة عمل في قطاع غزة / ساعات العمل والأسعار والحالة المباشرة لمساحات العمل المشتركة، في مكان واحد. | Find a workspace in the Gaza Strip / Opening hours, prices and live status of coworking spaces, in one place. |
| `search.label` / `.placeholder` / `.submit` | ابحث عن مساحة / اسم المساحة أو المنطقة / بحث | Search for a space / Space name or area / Search |
| `areas.title` / `areas.all` / `areas.strip` | تصفّح حسب المنطقة / كل المناطق / قطاع غزة | Browse by area / All areas / The Gaza Strip |
| `areas.count(n)` | one «مساحة واحدة» · two «مساحتان» · few «{n} مساحات» · many/zero/other «{n} مساحة» | one «1 space» · other «{n} spaces» |
| `areas.line({place, count})` / `areas.failed` | {place} · {count} / تعذّر تحميل المناطق | {place} · {count} / We couldn’t load the areas |
| `owners.title` / `owners.text` / `owners.action` | هل تدير مساحة عمل؟ / تواصل معنا لإضافة مساحتك، وإدارة ساعاتها وأسعارها، وإظهار حالتها المباشرة. / تواصل معنا | Do you run a coworking space? / Contact us to add your space, manage its hours and prices, and show its live status. / Contact us |

- Docs: `architecture.md` §2 (Home built); `overview.md`.

### PR 4 · Commit 5 — `feat(site): build the about page`
- **`AboutPage`** (`max-w-3xl` column, U11): the intro (`h1` `text-heading-1`, two paragraphs, «تصفّح المساحات»);
  «من أين تأتي المعلومات؟» (two cards and the note, design issue 41); «ماذا تعني الحالة؟» (`StatusLegend`: a
  `dl` in a `Card`, each term `LiveStatusBadge` — exported by `directory` now — or «لا تتوفر حالة مباشرة»);
  `#contact` «تواصل معنا» (its text, `PlatformContact layout="row"`); `#owners` «لأصحاب المساحات» (three steps
  in an `ol`, `PlatformContact layout="row"`). No university line (U11).
- **`navigation.ts`**: `OWNERS_ANCHOR = 'owners'`, `SITE_PATHS.owners = '/about#owners'`. **`SiteFooter`**:
  «تصفّح المساحات» first (design issue 42).
- **Words** (`site.about`):

| key | ar | en |
|---|---|---|
| `intro` | مساحة دليل لمساحات العمل المشتركة في قطاع غزة. نجمع في مكان واحد ساعات عمل كل مساحة وأسعارها ومرافقها وطرق التواصل معها، ونعرض حالتها المباشرة إن كانت موثّقة، لتعرف قبل أن تخرج إن كانت مفتوحة وفيها مكان. | Masaha is a directory of coworking spaces in the Gaza Strip. It brings together each space’s hours, prices, amenities and contacts, and shows its live status if it’s verified, so you know before you leave whether it’s open and has room. |
| `audience` | لمن يعمل عن بعد، وللطلاب، ولكل من يحتاج مكانًا فيه كهرباء وإنترنت ليعمل أو يدرس. | For remote workers, students, and anyone who needs a place with power and internet to work or study. |
| `source.title` | من أين تأتي المعلومات؟ | Where does the information come from? |
| `verified.title` / `.subtitle` / `.text` | مساحة موثّقة / تديرها المساحة نفسها / تحدّث إدارة المساحة ساعاتها وأسعارها وإعلاناتها، وتظهر حالتها المباشرة تلقائيًا، ويمكنها ضبطها يدويًا لفترة قصيرة. | Verified space / Managed by the space itself / The space updates its hours, prices and announcements; its live status shows automatically, and the space can set it by hand for a short time. |
| `unverified.title` / `.subtitle` / `.text` | مساحة غير موثّقة / جمعها فريقنا / جمع فريقنا معلوماتها من المساحة ومن صفحاتها العامة، ونراجعها دوريًا. لا تظهر لها حالة مباشرة. | Unverified space / Collected by our team / Our team collected its information from the space and its public pages, and reviews it periodically. It has no live status. |
| `source.note` | «آخر تحديث» هو آخر مرة تأكّدنا فيها من المعلومة أو حدّثتها المساحة. كلما طالت المدة زاد احتمال أن تكون قد تغيّرت، فنعرض «قد يكون تغيّر» بجانب المعلومة القديمة. إن وجدت معلومة خاطئة، تواصل معنا. | “Updated” is the last time we confirmed the information or the space updated it. The longer ago, the more likely it has changed, so we show “May have changed” next to old information. If you find wrong information, contact us. |
| `status.title` | ماذا تعني الحالة؟ | What does the status mean? |
| `status.available` / `.full` / `.closed` / `.none` | فيها مكان الآن، وتُحدَّث الحالة تلقائيًا من حركة الحضور في المساحة. / مفتوحة، لكن لا أماكن شاغرة الآن. / خارج ساعات العمل، أو مغلقة مؤقتًا بإعلان من المساحة. / المساحة غير موثّقة، أو لم تكتمل معلومات حالتها، فلا تظهر لها حالة لحظة بلحظة. راجع ساعات العمل أو تواصل معها. | Has room now; the status updates itself from who comes and goes at the space. / Open, but no free places right now. / Outside opening hours, or temporarily closed by an announcement from the space. / The space isn’t verified, or its status isn’t set up, so it shows no live status. Check its hours or contact it. |
| `contact.title` / `contact.text` | تواصل معنا / راسلنا إن كان لديك سؤال، أو مشكلة في الموقع الإلكتروني. | Contact us / Message us with a question, or a problem with the website. |
| `owners.title` | لأصحاب المساحات | For space owners |
| `owners.steps` | 1 «تواصل معنا وأخبرنا باسم مساحتك وموقعها.» · 2 «نتأكّد معك من المعلومات وننشئ حساب إدارة المساحة.» · 3 «تصبح مساحتك موثّقة: تحدّث أسعارها وساعاتها بنفسك، وتظهر حالتها المباشرة تلقائيًا من تسجيل الحضور.» | Contact us with your space’s name and location. · We confirm the information with you and create the space’s management account. · Your space becomes verified: you keep its prices and hours yourself, and its live status shows automatically from check-ins. |

- Docs: `architecture.md` §2 (About built, its anchors); `overview.md` (*Built*: the public site's four pages);
  `directory.md` (`LiveStatusBadge` exported).

## 10. Tests — each with its lane, title and the break that must make it fail

Each new test is seen red first (testing §3.5), its red line recorded; for code that exists, the break is made
once, its red output recorded, then restored (§3.7). **Every accessibility rule, state, width and privacy rule
has its break** — marked **[a11y]**, **[state]**, **[width]**, **[privacy]**. A width is proven in the
component lane through `useMediaQuery` and `stubScreenWidth` (S6); a layout drawn by classes alone is checked
in the real run's screenshots, and its break is listed there (§13).

### PR 1
| # | Lane · file | Title | Break |
|---|---|---|---|
| 1 | unit · `shared/lists/services/pageItems.unit.test.ts` (moved) | its titles, unchanged | (moved: green before and after) |
| 2 | unit · `shared/lib/names/spaceName.unit.test.ts`, `shared/lib/time/clockOf.unit.test.ts` (moved) | their titles, unchanged | (moved) |
| 3 | component · `pages/site/shell/SiteLayout.component.test.tsx` | **offers «تخطَّ إلى المحتوى» first, leading to the page's main content** [a11y] | the link's `href="#content"` |
| 4 | same | **moves the focus to the main content when another page opens, not on the first load nor when only the search changes** [a11y] | the effect keyed on `location.key` |
| 5 | component · `lookups/hooks/area/useAreaFilter.component.test.tsx` | offers the public catalogue's areas under their governorates, none chosen, a governorate with no area left out, never asking for the admin's lists | keep a governorate with no area |
| 6 | same | sums up the choice: all areas, one area by its name, then counted in Arabic (2, 3, 11) | `chosen(1)` for one area |
| 7 | same | **says the catalogue failed inside the list and tries again** [state] | the retry left out |
| 8 | component · `lookups/components/area/AreaFilter.component.test.tsx` | is named by its label, finds an area by its English name in the Arabic interface, and is axe-clean [a11y] | `keywords` left out |
| 9 | component · `useAreaName.component.test.tsx` (M) | names an area from the public catalogue for the public source, never asking for the admin's lists | `source` ignored |
| 10 | unit · `directory/services/filtersOf.unit.test.ts` | reads each filter from the address; falls back to the default for each value the server would refuse (51 areas, `area=3,x`, `period=YEAR`, `min=0`, `max=abc`, `max=100001`, `sort=relevance` without `q`, `page=0`) | accept `relevance` without `q` |
| 11 | same | writes no default into the address | write `page=1` |
| 12 | same | **keeps a search of diacritics only off the request, and says so** [state] | `searchOf` hands the text back |
| 13 | unit · `requestOf.unit.test.ts` | asks in agorot, the period only with a bound, only the true flags, and the language only to order by name | send the shekels |
| 14 | unit · `directoryRepository.unit.test.ts` | asks for a page of spaces with its query; **sends the location only in `Masaha-Near`, never in the query** [privacy]; a failure arrives as an `AppError` | the point added to `params` |
| 15 | unit · `cardView.unit.test.ts` | **shows a live state by its word and its role: available success, full warning, closed neutral, none in words** [a11y] | `FULL` → `destructive` |
| 16 | unit · `todayHours.unit.test.ts` | reads today on Gaza's calendar (an instant just past Gaza's midnight is already its next day); a closed day; all day; never saved draws nothing | `now.getUTCDay()` |
| 17 | unit · `distanceText.unit.test.ts` | 0.7 km, 1 km (no «.0»), 12 km from 10, Western digits in Arabic | `toFixed(1)` |
| 18 | component · `useDirectoryFilters.component.test.tsx` | a filter replaces the address and returns to the first page | keep the page |
| 19 | same | the search reaches the address only once typing has paused | write on each key |
| 20 | component · `useDirectoryList.component.test.tsx` | **shows skeletons while the first page loads, then the cards** [state] | `ready` while pending |
| 21 | same | **a failure says so with its reference, and «إعادة المحاولة» asks again** [state] | the retry does not refetch |
| 22 | same | **no connection says so, not a server's failure** [state: offline] | the line of `errors.server` for every failure |
| 23 | same | **tells an empty directory from no match; only no match offers clearing the filters** [state: empty] | one state for both |
| 24 | same | keeps the cards while the next page loads, marked busy | no `placeholderData` |
| 25 | same | a page past the last shows the last | `replacePage` left out |
| 26 | same | counts the Strip's spaces, or the matching ones once a filter or a search narrows them | `count.all` always |
| 27 | component · `DirectoryList.component.test.tsx` | **names the search, the sort, the results and the pages; each card is one link named by its space; axe-clean at 390 and 1440** [a11y] [width] | the results' heading left out |
| 28 | same | **moves the focus to the results when the page changes, and only then** [a11y] | the effect runs on the first render too |
| 29 | same | a cover that fails to load shows the space's mark in its place | no `error` handler |
| 30 | same | offers «الأفضل تطابقًا» only while a search is typed | offered always |
| 31 | unit · `priceBounds.unit.test.ts` | reads whole shekels in Arabic digits; refuses 0, letters and above 100,000; a maximum under the minimum is refused on the maximum | accept 0 |
| 32 | component · `usePriceFilter.component.test.tsx` | writes a valid budget to the address after the pause (agorot in the request) and leaves an invalid bound out, with its line | apply an invalid bound |
| 33 | component · `FiltersSheet.component.test.tsx` | **below 1024 px the filters open from a button that says whether the sheet is open and how many filters apply** [a11y] [width] | a plain `Button` with `onClick` |
| 34 | same | its primary button counts the spaces in Arabic agreement and closes the sheet; with none, says so | «عرض {n} نتيجة» |
| 35 | same | **from 1024 px the filters are a sidebar named «الفلاتر», with no Filters button** [width] | both drawn |
| 36 | unit · `nearPoint.unit.test.ts` | **rounds a point to three decimals** [privacy]; refuses a position less precise than 2 km or outside the Strip | no rounding; the accuracy check left out |
| 37 | component · `useNearMe.component.test.tsx` (the browser's `navigator.geolocation` stubbed, the platform's seam) | **asks for the location only when the button is pressed** [privacy] | ask on mount |
| 38 | same | **keeps only the rounded point, in memory: nothing in the address, nor in local or session storage** [privacy] | the store persisted to `localStorage` |
| 39 | same | **a refusal or an imprecise position says so and keeps nothing** [state] | keep the raw point on imprecise |
| 40 | same | **stopping keeps the point; clearing drops it and every answer ordered by distance** [privacy] | `removeQueries` left out |
| 41 | component · `useDirectoryList.component.test.tsx` | sorts nearest first through the header while the button is pressed, and words each card's distance | `sort=distance` left out |
| 42 | component · `LocationStatus.component.test.tsx` | **shows the privacy line while locating and in use, never once the location was refused or imprecise** [privacy] | the line in `denied` |
| 43 | same | the refused states offer «اختر منطقتك», which focuses the place filter from 1024 px and opens the sheet below it [width] | the fallback left out |
| 44 | component · `pages/site/routes.component.test.tsx` (M) | shows the Directory under its title | the route's title left out |
| 45 | unit · `shared/copy/catalogues.unit.test.ts` (existing) | parity of the new sections | (existing; runs in the lane) |

### PR 2
| # | Lane · file | Title | Break |
|---|---|---|---|
| 46 | unit · `shared/map/services/markClass.unit.test.ts` | names a mark's shape and tone, and the selected one by a ring | the selected as a fill class |
| 47 | component · `shared/map/components/MarkerMap.component.test.tsx` | **names each mark as a button with its label and pressed state, and selects it on a click and on Enter** [a11y] | no `role` |
| 48 | same | **while picking, the marks leave the tab order and a tap places the point** [a11y] | marks kept tabbable |
| 49 | same | **its line shows when its tiles fail** [state] | the line left out |
| 50 | unit · `directory/services/pinMark.unit.test.ts` | **each live state is a shape as well as a colour** [a11y] | `FULL` drawn `filled` |
| 51 | unit · `boundsText.unit.test.ts` | writes `south,west,north,east` | `north` first |
| 52 | component · `useDirectoryMap.component.test.tsx` | asks for the pins with the list's filters; a change of filter clears the selection | selection kept |
| 53 | same | **past 1,000 pins says so and asks again within the box in view, after a pause** [state] | no re-ask |
| 54 | component · `DirectoryMap.component.test.tsx` | **a chosen pin shows its card from 768 px, and below it a sheet that leaves the focus on the map** [width] [a11y] | a modal sheet |
| 55 | same | the legend names each state beside its mark; «عرض التفاصيل» leads to the space's page; axe-clean | a mark without its word |
| 56 | same | **with no match, says so over the map and offers clearing the filters**; **a failure says so and tries again** [state] | the no-match card left out |
| 57 | component · `ViewSwitch` (in `DirectoryMap.component.test.tsx`) | switches the view in the address, keeping every filter | the filters reset |
| 58 | unit · `filtersOf.unit.test.ts` (M) | reads and writes `view=map` | `view` dropped |
| 59 | component · `useNearMe.component.test.tsx` (M) | **a point placed by hand is kept rounded, from a pin, and sorts by distance; «رجوع» restores the location before** [privacy] | the pin not rounded; cancel clears |
| 60 | component · `LocationStatus.component.test.tsx` (M) | the refused states offer setting the location on the map; a pin's line offers «تغيير الموقع» | the map fallback left out |

### PR 3
| # | Lane · file | Title | Break |
|---|---|---|---|
| 61 | unit · `shared/lib/phone/carrierOf.unit.test.ts`, `time/updatedAgo.unit.test.ts` (moved) | their titles | (moved) |
| 62 | unit · `platform-settings/services/platformContact.unit.test.ts` | keeps a WhatsApp number in its stored form and a valid email, WhatsApp first; leaves out an empty or an invalid one | keep an invalid email |
| 63 | component · `PlatformContact.component.test.tsx` (`vi.stubEnv`) | **with only the email set, offers the email alone; with none, shows its `none`** [state] | a WhatsApp button drawn regardless |
| 64 | component · `shared/map/components/PlaceMap.component.test.tsx` | **the place's pin is a picture named by its label, not a button** [a11y] | `role="button"` |
| 65 | unit · `directory/services/weekRows.unit.test.ts` | Saturday first; equal days grouped (a pair, a run); today on Gaza's calendar; every day on demand | Sunday first |
| 66 | unit · `priceGroups.unit.test.ts` | general prices, then students; a label stands for its period; shift tabs only when a price names a saved shift; an incomplete last row shares its width (counts 1–7) | the span table off by one |
| 67 | unit · `freshness.unit.test.ts` | dates a group, marks it stale, says nothing while missing | the stale mark ignored |
| 68 | unit · `contactLinks.unit.test.ts` | each contact its link (`wa.me` digits, `tel:`, `mailto:`, the stored address); a phone's carrier in its label | `wa.me/+970…` |
| 69 | unit · `localText.unit.test.ts`, `straightLine.unit.test.ts` | the interface's language else the other, marked; the straight-line distance of a known pair | the mark left out; degrees as radians |
| 70 | component · `useSpacePage.component.test.tsx` | **a 404 is «لم نجد هذه المساحة»; a failure says so with its reference and tries again; no connection says so** [state] | 404 shown as a failure |
| 71 | same | **hidden prices say why, with their date; prices never saved say so** [state: empty] | the hidden line without its date |
| 72 | same | the unverified notice dates the profile; the bar exists only with a WhatsApp or a phone contact | the bar always |
| 73 | component · `SpaceDetails.component.test.tsx` | **one `h1`; the sections in U8's order, each named by its heading; axe-clean at 390 and 1440** [a11y] [width] | prices after hours |
| 74 | same | **from 1024 px the status and the contacts are a named aside; below it a status card first and a contact section last; the bar only below 768 px** [width] | the aside drawn at 390 |
| 75 | same | the owner's dialog shows the page's contact, or its `none` line | `none` never shown |
| 76 | component · `Gallery` (in `SpaceDetails.component.test.tsx`) | **with more than one photo, «عرض كل الصور (n)» at every width; the viewer moves round; each photo named; none → no gallery and the caption** [a11y] [state] | the pill from four photos only |
| 77 | component · `useLiveStatusQuery.component.test.tsx` (fake timers; `document.visibilityState` and the window's `focus`) | **reads the status again every 60 s while the page is visible, never while it is hidden, and at once on returning** | `refetchIntervalInBackground: true`; `refetchOnWindowFocus: false` |
| 78 | component · `StatusPanel` (in `SpaceDetails.component.test.tsx`) | **a verified space with no status says it is not set up; an unverified one, that it shows for verified spaces only; a failed first read says so** [state] | one line for all three |
| 79 | component · `pages/site/routes.component.test.tsx` (M) | **shows a space's page titled by its name; from 768 px a breadcrumb back to the Directory with its last search, below it a back link** [width] | the last search dropped |

### PR 4
| # | Lane · file | Title | Break |
|---|---|---|---|
| 80 | component · `shared/routing/states/RetryState.component.test.tsx` | **offers the caller's way on beside «إعادة المحاولة»; a retry while still offline says so and does not reload** [state: offline] | reload anyway |
| 81 | component · `lookups/hooks/area/usePublicAreas.component.test.tsx` | lists the catalogue's areas in order, each with its governorate | the governorate left out |
| 82 | component · `directory/hooks/home/useAreaCounts.component.test.tsx` | counts the pins by area, and their total | count areas, not pins |
| 83 | component · `useHomeSpaces.component.test.tsx` | available now, six at most; with a point, nearest through the header, titled «المساحات الأقرب إليك»; **the empty state offers browsing all** [state] | `limit` left out |
| 84 | component · `pages/site/public/home/useAreaCards.component.test.tsx` | **only the areas with spaces, in order, then «كل المناطق» with the total; a failure retries both reads** [state] | areas with no space kept |
| 85 | component · `pages/site/routes.component.test.tsx` (M) | Home's search opens the Directory with its `q`; About has `#contact` before `#owners`, each with the configured contact, and no university line; the footer offers «تصفّح المساحات» first; axe-clean | `q` not encoded |
| 86 | component · same | **with no contact configured, About's sections keep their text without buttons** [state] | a hard-coded email |

## 11. Review Focus — inputs no planned test exercises

- A space whose English name only is set, in the Arabic interface, on a card, a pin's name, the page's `h1`,
  the breadcrumb and the document's title (U3, `lang="en"`).
- 50 areas chosen at once; an `area` id in the URL that the catalogue does not hold (hidden since): the summary
  counts it, the server narrows to nothing.
- Typing fast across the 400 ms pause in the search and both price fields, then Back.
- A list answer that arrives after the filters changed again (`keepPreviousData` with a stale key).
- Near me granted at 2.0 km accuracy exactly, and at the Strip box's edge (the rounded point outside it).
- A location granted on Home, then the Directory's map pick, «رجوع», then Home again.
- `distanceMeters` 0 and 99,900.
- The map with one pin; with 1,000 pins and `truncated`; zooming out after a viewport re-ask.
- A space at 24:00 closing, a day 0–1440, and a week with every day closed.
- 40 prices across three shifts and both audiences; a shift named only in Arabic in the English interface.
- Twenty contacts; an Instagram address 200 characters long at 390 px (truncated, never overflowing).
- Ten photos; a photo URL that 404s in the viewer.
- The live status's 60 s refetch across a midnight in Gaza; a tab hidden for an hour, then shown.
- The page opened on a hidden space's slug from a stale card (the card's 30 s cache).
- `VITE_CONTACT_WHATSAPP` in the local form «0599 000 099» (normalised or left out).
- `space-links`' own `SpaceNameView` (a copy of the moved type), left as it is: a later item may merge it.

## 12. The commits

| PR | # | Subject (chars) | Body (why) |
|---|---|---|---|
| 1 | 1 | `refactor(space-links): share the list's pages` (45) | the site's Directory pages its list too; `space-links` is dashboard-only (S2) |
| 1 | 2 | `refactor(spaces): share the name and clock rules` (48) | the site's cards name a space and its hours (S3) |
| 1 | 3 | `feat(site): add a skip link and focus each page` (47) | SH-018; R2-PU-AX-001 (S8); finding 130 |
| 1 | 4 | `feat(lookups): offer the public areas to the site` (49) | the Directory's place filter and area names (S7) |
| 1 | 5 | `feat(directory): list the spaces page by page` (45) | screen 2's list, search, sort and pages; the URL (S5) |
| 1 | 6 | `feat(directory): filter by place, price and state` (49) | U1, U5, «أخرى» (S9); the P5 exception (S6) |
| 1 | 7 | `feat(directory): sort the spaces nearest first` (46) | U2 and the privacy line (decision 8); memory only (S4) |
| 2 | 1 | `feat(map): show many marks and pick a centre` (44) | the map of many places stays in `shared/map` (S12) |
| 2 | 2 | `feat(directory): show the spaces on a map` (41) | U6; the viewport past 1,000 pins |
| 2 | 3 | `feat(directory): set my location on the map` (43) | U7 |
| 3 | 1 | `refactor(spaces): share the carrier and date rules` (50) | the space page shows carriers and dates (S3) |
| 3 | 2 | `feat(platform-settings): read the public contact` (48) | decision 5 (S11) |
| 3 | 3 | `feat(map): show one place on a map` (34) | PU-026 |
| 3 | 4 | `feat(directory): show a space's public page` (43) | screen 3, U8, U9, U4; finding 131 |
| 3 | 5 | `feat(directory): show the space's photos` (40) | the gallery or its caption (PU-023) |
| 3 | 6 | `feat(directory): refresh a space's live status` (46) | decision 3 |
| 4 | 1 | `feat(routing): offer home and say a failed retry` (48) | PU-024 |
| 4 | 2 | `feat(lookups): list the public areas for home` (45) | U1's «تصفّح حسب المنطقة» |
| 4 | 3 | `feat(directory): offer home its spaces and counts` (49) | screen 1's spaces and the areas' counts |
| 4 | 4 | `feat(site): build the home page` (31) | screen 1 |
| 4 | 5 | `feat(site): build the about page` (32) | screen 4, U11 |

PR titles: PR 1 = commit 5's subject (with A13: 1a commit 5's, 1b commit 6's); PR 2 = commit 2's; PR 3 =
commit 4's; PR 4 = commit 4's. **Recount each subject before committing (≤ 50).** A unit's code, tests and docs
in its commit. A fix before the push folds into its commit (`git commit --fixup <sha>`, then
`GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash origin/main`). No tool attribution. Stage by path; `git
status` before each commit. **Carried items:** if the supervisor leaves `C:\dev\masaha\workspace\WORKER_A\
PUBLIC\0_CARRIED_FROM_<n>.md` (from the review of the PR before, OWNER_SETUP PR 3's for PR 1), its items are
that PR's first commit(s), each code fix red first, then green, with its break; the PR's description says
"Carried from #<n>".

## 13. The procedure and the verification

Work in `C:\dev\masaha\app` only — never in `C:\dev\masaha\app-b` (worker B) or `C:\dev\masaha\app-design`
(reviews and planners read there). Each commit message is written to a UTF-8 file **without a BOM, LF line
endings**, with a body saying why, and committed with `git commit -F <file>`. The executor's scripts live in
`C:\dev\masaha\workspace\WORKER_A\PUBLIC\scripts\`, never committed; screenshots in
`C:\dev\masaha\workspace\WORKER_A\PUBLIC\shots\pr<n>\` (moved there if saved elsewhere), never committed; the
report `C:\dev\masaha\workspace\WORKER_A\PUBLIC\4_REPORT_PR<n>.md`, written **as you go**.

### First checks (before any edit), each PR
1. `git status --short` clean in `C:\dev\masaha\app`; `git fetch origin`; `git switch main`; `git pull --ff-only`.
2. **The PR before has merged.** PR 1: `gh pr list --state merged --head feat/owner-staff-settings --json
   number,mergeCommit` (OWNER_SETUP PR 3); PRs 2–4: the previous branch of §1 (with A13, PR 1b after 1a). Empty →
   **stop**.
3. **The base diff.** PR 1: `git diff --name-status cf3190a4 origin/main`; PRs 2–4: `git diff --name-status
   <the previous PR's reported head> origin/main`. Read the previous PR's `4_REPORT_PR<n>.md` (OWNER_SETUP's for
   PR 1) for its departures. A code file this plan names that changed in a way the plan does not cover → **stop
   and ask**. `packages/shared` changed → `npm run build -w @masaha/shared` before any web check, and re-read
   `packages/shared/src/directory`, `lookups`, `occupancy`, `spaces` (the responses) and `core/gazaTime` against
   §9; a difference → **stop**.
4. **Open PRs:** `gh pr list --state open --json number,headRefName,files`; one that edits a code file of this
   PR → **stop and ask**. Note the others' heads for the conflict check (worker B's: shared documents only).
5. **Checks against the code, each with its fallback:**
   - a. `useMediaQuery(query: string): boolean` in `shared/design-system/lib/` (S6). Else **stop**.
   - b. `CardTitle` takes a heading level (SH-017): the card's title is an `h3`. If it renders a `div`, the
     `h3` goes inside it; a departure.
   - c. `useRefusalView` (`shared/forms`) gives a line for `network` and `timeout`. Else the list's hook words
     those two with `status.offline`; a departure.
   - d. `ComboboxItem` takes `keywords`. Else the area filter's search matches the shown name only; record
     finding 13x (no design-system change).
   - e. eslint lets `features/` import `zustand` (S4). Else **stop and ask**.
   - f. `useGovernoratesQuery` takes `{ enabled }` (PR 1's `AreaName` source). Else it gains it, in commit 4,
     as `useCatalogueQuery` has it.
   - g. PR 2: the layer's `Sheet` passes `modal` to its root. Else design issue 22's fallback (a bottom `Card`)
     and finding 13x.
   - h. PR 2: Leaflet renders in the component lane (the point picker's test proves it). If the marks' names
     cannot be read there, prove them through `MarkerMap` as that test does; still not → **stop and ask**.
   - i. PR 3: `normalisePhone`'s signature (`@masaha/shared/core`) and that `emailSchema` is exported. Else
     **stop**.
   - j. PR 3: the layer's `Alert` renders with a description and no title. Else the stale prices' Alert takes
     `page.stale` as its title; a departure.
   - k. PR 4: React Router's `ScrollRestoration` scrolls to `#owners` and `#contact` arriving from another page.
     Else `AboutPage` scrolls to the hash once rendered (a two-line effect); a departure.
   - l. PR 4: `foundation.md` §12 names the icon set's members. If not, it is not edited.
6. **Finding numbers:** the index's highest; this item's are 130 and on. If 130 is taken, the next free ones,
   said in the report.
7. **The data inventory (read-only, before any edit).** `docker start masaha-postgres-1` (never `npm run db:up`;
   never `npm ci`); `npx prisma migrate status` in `apps/api` — a migration pending → `npx prisma migrate deploy`
   then `npx prisma generate` (worker A's `masaha_dev` to `main`); the API on 3320 (`npm run dev -w
   @masaha/api`). A script in `scripts\` reads, with plain `GET`s and no write: `GET /api/v1/spaces?limit=50`
   (every page), `GET /api/v1/map/spaces`, and `GET /api/v1/spaces/:slug` for each listed space. It records the
   count of listed spaces and, for each case of this PR's real run (below), a space that holds it. **A case the
   data does not hold → stop and report** (§14.3) — never change data through the app, the API or the seed to
   get past it. Stop the API by its process id.
8. **Branch:** `git switch --no-track -c <branch> origin/main` (§1's names).

### Per commit
`npm run lint` and `npm run typecheck`; focused runs of the touched test files while working; each new test seen
red first, its red line recorded; each break of §10 made, its red output recorded, then restored.

### On the head, once each
First: no `vitest`, `tsc` or dev server of `C:\dev\masaha\app-b\` runs —
`Get-CimInstance Win32_Process -Filter "Name='node.exe'" | Where-Object { $_.CommandLine -match 'app-b' }`
empty (else wait; never stop worker B's processes); then the free memory, recorded —
`(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory` — **before each full lane**; one full lane at a
time on this machine. Then: `npm run test:unit` · `npm run test:component` (record the time of
`pages/dashboard/routes.component.test.tsx` › "lists the owner's eleven pages", finding 87, and of the site's
routes test, finding 55) · `$env:NODE_ENV='production'; npm run build; Remove-Item Env:NODE_ENV` · `npm run
check:build` · `npm run check:classes` · `npm run format:check` · `npm run check:links`.
- **The first download, recorded:** from `apps/web/dist/.vite/manifest.json`, the entry and every chunk it
  imports statically, with their bytes, before (the base) and after (the head); no public page's chunk in it,
  no `leaflet`, no `data-table`, no `dashboard` (A10 is not taken: a record, not a gate).
- **Finding 27, re-checked (PR 1):** in the same manifest, whether the space shell's chunk and the `dashboard`
  chunk still import each other; the answer recorded, the finding left to the owner.
- **Not run:** `test:api` (no API or shared change; CI runs it).

### The real run
- `docker start masaha-postgres-1`; the API on 3320 (`npm run dev -w @masaha/api`, worker A's `masaha_dev`); the
  web on 5320 (`npm run dev`). PR 3 and 4: `apps/web/.env` holds `VITE_CONTACT_EMAIL` with a test value such as
  `hello@example.com` for the run (the owner's real value only if the owner gave it), and no
  `VITE_CONTACT_WHATSAPP`; one case with both (a test number), then back to the email alone. `.env` is never
  committed.
- **Browser:** the `playwright` MCP tools if present, else local headless Chrome over CDP (a script in
  `scripts\`); say which. **Arabic light and English dark, at 390, 768 and 1440.** Near me through CDP:
  `Browser.grantPermissions` (`geolocation`, origin `http://localhost:5320`) and
  `Emulation.setGeolocationOverride` (a point in Gaza City at 30 m; then one at 5,000 m for imprecise; then one
  in Cairo for out of the Strip); denied with `Browser.resetPermissions` and no grant. **The network log** of
  each case: every request URL, and the `Masaha-Near` header's value.
- **PR 1 cases:** the list (cards, the cover or the mark, the status words, today's hours, «موثّقة»); a search by
  an English name in Arabic; a search of diacritics only (its line, no 422 in the log); the place filter (two
  areas, the summary), the budget (day, 10–30 ₪; an inverted range's line), each switch, «أخرى»; the sort (by
  name, a search's «الأفضل تطابقًا»); page 2 (focus on the results; Back returns to page 1); a reload and a
  copied URL show the same list; no match and «مسح الفلاتر»; the filters' sheet at 390 and 768 (its count, its
  button), the sidebar at 1440; near me granted (sorted, distances, the privacy line, «إيقاف…», «مسح موقعي»),
  denied, imprecise, out of the Strip (no privacy line in those); the skip link (Tab from the page's top) and
  the focus after a header link. **The privacy proof in the log:** no request URL holds a coordinate; the
  header only on `sort=distance` requests; its value has three decimals at most; after «مسح موقعي», no header.
- **PR 2 cases:** «خريطة» (the pins by state, the legend); choose a pin (its card at 768 and 1440, its sheet at
  390 with the map still panning); «عرض التفاصيل»; a filter on the map; «حدّد موقعي على الخريطة» from the
  denied state → the crosshair → the arrows pan → «ثبّت الموقع هنا» (sorted, «تغيير الموقع»), then «رجوع»
  from a second pick; «مركّز على موقعي»; the network log: Leaflet's chunk and stylesheet only after «خريطة».
- **PR 3 cases:** a verified space (the order at each width, the status, today, the prices per audience and by
  shift, the hours with today and «عرض كل الأيام», the amenities, the map's pin, «الاتجاهات», the contacts and
  the carrier, the breadcrumb from 768, the back link and the bar at 390); an unverified space with hidden
  prices (the notice, its dialog with the email alone, then both channels, then none); a space with photos (the
  viewer) and one without (the caption); a stale group's badge; an unknown slug (`/spaces/no-such-space`); the
  status refetched after 60 s (the log), not while the tab is hidden (CDP `Page.setWebLifecycleState`
  `frozen`/`active` or `Emulation.setFocusEmulationEnabled`), and at once on returning.
- **PR 4 cases:** Home (the hero's search → the Directory; «متاحة الآن» or its empty state; near me → «المساحات
  الأقرب إليك» and «عرض الكل» keeping the order; «تصفّح حسب المنطقة»; the owners' card → About's `#owners`);
  About (both anchors from the footer and Home, the legend, the contact with the email alone); the offline
  state (CDP `Network.emulateNetworkConditions` offline, then a lazy page: «إعادة المحاولة» while still
  offline says «ما زال الاتصال مفقودًا.», «الرئيسية» back online); the general error is not producible without
  a code change — not performed (test 80 owns it).
- **Width breaks in the real run** (a layout drawn by classes, §10's note): PR 1 — the results' columns (`md:`,
  `xl:`) removed once, the 1440 screenshot showing one column, restored; PR 3 — the main column's `lg:col-span-8`
  removed once, the 1440 screenshot showing it full width, restored. Each break's screenshot named
  `break-<what>.png`.
- **Not performed, by design:** `FULL` (it needs people checked in: never through the app) unless the data
  shows one; a truncated map (1,000 spaces); a photo that fails to load; the general error state — their
  component tests prove them. Any other case not performed → the stop rule.
- Screenshots `<pr>-<case>-<ar-light|en-dark>-<width>.png`. Stop the servers by process id
  (`Get-CimInstance Win32_Process -Filter "Name='node.exe'" | Where-Object { $_.CommandLine -match
  'C:\\dev\\masaha\\app\\' }`, `Stop-Process -Id …`); `Get-NetTCPConnection -LocalPort 3320,5320 -State Listen`
  empty; `git status --short` clean.

### Push and the PR
1. `git grep -n "#PRNUM" HEAD`; the next number: `gh api "repos/{owner}/{repo}/issues?state=all&per_page=1&sort=created&direction=desc" --jq '.[0].number'`
   + 1 (worker B may take it first: check at that moment).
2. In Git Bash: `git filter-branch -f --tree-filter "grep -rl '#PRNUM' docs | xargs -r sed -i 's/#PRNUM/#<n>/g'" origin/main..HEAD`,
   then `git update-ref -d refs/original/refs/heads/<branch>`; `git grep -n "#PRNUM" HEAD` empty; `git diff
   origin/main --stat` the same files as before.
3. `git push -u origin <branch>`; `gh pr create --assignee @me --label feat --label area:web --label area:docs`
   (with `--label area:design-system` on PRs 1, 2 and 4 if §14.7 approves), the title §12's; the description per
   workflow §3 (Summary; Scope / Acceptance criteria / Out of scope; Change type; Evidence — run and not run;
   Screenshots — attached by the owner; the Definition of Done), and, for PR 1, the line for
   `DECISIONS_PUBLIC.md` (decision 7) for the supervisor. Confirm the number matches.
4. `gh pr checks <n>` green on the pushed head's SHA; `gh pr view <n> --json mergeStateStatus` → `CLEAN`.
5. The conflict check: for each other open PR, `git fetch origin <its head ref>` and `git merge-tree
   --write-tree origin/<branch> origin/<other>`; recorded.
6. The report, written as you go (after the first checks, after each commit with its sha, subject length, red
   line and green line, after each break with its red output, after the real run, after the push). **Never
   merge.** Each PR is reviewed in a separate conversation.

### The stop rule (as `OWNER_SETUP\3_EXEC_PROMPT_PR3.md` §2)

**A test you cannot run stops the work.** A test **failing** because its code is not written yet is the plan's
red step — normal. A test, lane or command you **cannot run** is not: it errors before any test runs (the
database unreachable, Docker down, a port taken, a module or `dist` missing, a migration pending, `No test files
found`, a Vitest or TypeScript startup error, the whole run timing out, a crash with no result); a break you
could not make or run; a real-run case you could not perform (other than those the plan names). **Then stop at
once** — never skip, `.skip` or delete a test, never change a config, a timeout, `.env`, a script or a lane,
never mock what the plan does not, never run a narrower command and call it the lane, never call it "flaky" and
move on. Write the command, its exact error and where you were into the report, and reply with `Status:
STOPPED`.

**Known exceptions (the owner's decisions on #96 and #98):**
- `routes.component.test.tsx` › "lists the owner's eleven pages" (finding 87) may miss its 3 s locally when the
  machine is loaded. If **only that test** fails and it passes alone, record both runs (times, free memory) and
  go on; **CI's `test:component` is the judge** — if it fails there, stop.
- If the full component lane is **killed for memory**, re-run it once when the machine is quieter; killed
  again → record it, carry on, and CI's `test:component` is the judge on the pushed head.

**A plan that proves false against the code:** stop too, say exactly what and why, and offer the fix — do not
choose it yourself. **A break that stays green:** stop — unless it is plainly your own test's defect, or the
plan's break cannot change the outcome (as a bound already excluded by another); then make the break that can,
see it red, and state it as a departure.

**Never claim a result you did not see:** a command passed only if you saw its own output say so; copy that line
(read it by its exit code). A break counts only when you saw it red.

**A demo account or demo data that does not hold what a real-run case needs → stop and report;** never change
data through the app (or the API, or the seed) to get past it.

### Stop and ask
- The PR before has not merged; a base diff changes a code file this plan names in a way it does not cover; an
  open PR edits one of this PR's code files.
- Anything would need `apps/api`, `packages/shared`, the schema, a migration, the seed, a dependency,
  `shared/copy/*/errors.ts`, or a design-system change beyond S6's export, `leaflet.css`'s marks and crosshair,
  and `WifiOffIcon`.
- `packages/shared`'s `directory`, `lookups`, `occupancy` or `spaces` responses differ from §9's use.
- Check 5's a, e, h or i fails; the data inventory lacks a case (check 7).
- `check:build` fails because a module of this item reaches the site's first download.
- An existing `spaces`, `space-links` or `lookups` test fails after a refactor commit and the cause is not the
  move's own mistake.
- A routes test times out beyond the known exception.
- Three fixes of one failure have failed; a decision this plan does not settle.

## 14. Decisions needed from the owner

1. **The plan as written,** with S1–S15 as recommended — S4's memory-only location (not A8), S6's layer export,
   S11's variables (not A9), S12's generic map.
2. **The closure's notice on the space page** (design issue 23, finding 131): accept that it waits for step 10
   (the live status says «مغلق الآن» meanwhile), or ask worker B for the closures in force on `GET
   /spaces/:slug` before PR 3 (an API item).
3. **The real runs' data.** `masaha_dev` may hold only the demo space (verified, no photo, one area). The cases
   need: 21+ listed spaces (pages), two areas or more, an unverified space with hidden (stale) prices, a space
   with photos and one without, a space with no hours, shift prices, student prices, a Friday-open space, a
   phone contact. *Recommend:* a small worker-B seed item (`SEED_DEMO`'s directory set: ≈ 24 spaces across
   areas, unverified ones, one whose prices' date is 60 days back, photos through the local storage port) before
   PR 1's real run; otherwise the owner adds what the admin's pages can (spaces, photos — not a stale date), and
   the executor stops at each case still missing.
4. **The platform's contact (S11):** the variables' names, and **the email's value** for `apps/web/.env` and
   Vercel (the WhatsApp number when the owner has it). The documents stay true: architecture §3 already gives
   the public contact to `platform-settings`; `GET /settings/public` stays planned for step 11 (v1-mvp); finding
   40 gets its evidence line.
5. **The design issues 1–44,** each as written.
6. **The Arabic copy of §9,** every line (localisation › Catalogues).
7. **`area:design-system`** on PRs 1, 2 and 4, whose layers change (S6, the marks, the icon), beside the
   prompt's labels.
8. **The documents the decisions prove wrong:** foundation §5's status roles corrected in PR 1 (Full `warning`,
   Closed `neutral` — DECISIONS_SHARED, 2026-10-10; S14); architecture §6's "space markers … belong to the
   `directory` feature" corrected in PR 2 (S12); and the supervisor adds decision 7's line to
   `DECISIONS_PUBLIC.md`.
9. **A13 — PR 1 split in two** (≈ 63 and ≈ 34 files). *Recommended.*
10. **Finding 27:** if PR 1's manifest shows the chunks no longer import each other, resolve it in PR 1's
    documents commit, or leave it for the owner to judge.

## Appendix — steps mapped to Claude Code skills (only a map; no step depends on them)

| Step | Skill (if present) |
|---|---|
| Before the branch | `start-work-item` (its git checks; the plan is already saved) |
| Each test red first; each break | Superpowers `test-driven-development` (with `writing-good-tests.md`), per workflow §10 |
| A failure or a flake | `systematic-debugging` |
| Claims in the report and the PR | `verification-before-completion` |
| Opening the PR, its self-review, a conflict with `main` | `open-pr` |
| After CI is green and `CLEAN` | `final-report` |
| The real run's screenshots | `run`, or the Chrome tools; else headless Chrome over CDP |
