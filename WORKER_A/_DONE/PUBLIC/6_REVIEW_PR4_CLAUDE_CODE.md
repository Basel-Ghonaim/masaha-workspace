# Review — PUBLIC PR 4 (#111, `feat/home-about`)

**Head reviewed:** `036335346cd16be9a719e9a4745d244b1549cc08` (base `dec7bd37`; `origin/main` at `8fc5939e`,
`CLEAN`). `gh pr checks 111`: build, check:classes, check:links, format:check, lint, test:api, test:component,
test:unit, typecheck all **pass** (CodeRabbit pass, rate limited). At the end the head had not moved (same sha,
`CLEAN`). Read from commit objects only (`git show`, `git diff`), from `C:\dev\masaha\app-design`; no test, build
or browser run. 13 commits, 55 files, `apps/web` and `docs` only.

**Verdict: mergeable.** No blocker. Every carried item and all five plan commits are present and do what was
decided. The findings are small: two accessibility gaps on About, one doubled phrase, and one wording question
for the owner. None of them needs a fix round on this PR. They go to the public site's fix PR after the owner's
in-person review (`0_CARRIED_FROM_111.md`), or are recorded.

## The five most important findings

1. **should-fix — arriving at `/about#owners` or `/about#contact` leaves the focus at the top of `main`, not on
   the section.** `apps/web/src/pages/site/shell/useMainFocus.ts:17-21` focuses `#main` on every path change.
   `ScrollRestoration` then scrolls to the hash. *Scenario:* an owner using a screen reader presses Home's
   «تواصل معنا» (`/about#owners`). The page scrolls to the owners' section, but the screen reader starts reading
   at «عن مساحة». The keyboard's next Tab goes to the intro's «تصفّح المساحات» at the top of the page, which
   scrolls the view away from the section. The footer's «تواصل معنا» does the same from another page. Pressed on
   About itself (only the hash changes), the focus stays in the footer, so Tab leaves the page. *Fix:* when the
   location has a hash naming an element on the page, focus that section (or its `h2`, `tabIndex={-1}`) instead
   of `main`, also when only the hash changes. Add a routes test for each. This changes S8's rule ("not when only
   the hash changes"), so the owner approves it first. *Where:* the fix PR after the in-person review. I saw this
   in the code; the real run checked only `scrollY`, never `document.activeElement`.
2. **should-fix — About's freshness note says «تواصل معنا» twice.** `site.about.source.note` (both catalogues)
   already ends «… إن وجدت معلومة خاطئة، تواصل معنا.». `AboutPage.tsx:50-55` then adds a link with the same
   words (`words.contact.title`). The page reads «… تواصل معنا. تواصل معنا», and the English reads "…contact us.
   Contact us". I saw this in the code and in the shot `shots\pr4\4-about-ar-light-1440.png`. *Fix:* make the
   sentence's own last words the link to `#contact`. Split the note so that its text stays word for word as §9
   approved it (for example `note` without its last sentence, then `wrong` «إن وجدت معلومة خاطئة،» + the link
   «تواصل معنا» + «.»). Design issue 41 asks for exactly that sentence as the link. *Where:* the fix PR.
3. **should-fix (owner's wording) — Home's owners' card does not say the status shows automatically (design
   issue 36).** `site.home.owners.text` is «تواصل معنا لإضافة مساحتك، وإدارة ساعاتها وأسعارها، وإظهار حالتها
   المباشرة.» / "…and show its live status." It matches §9 word for word, but design issue 36 says Home's
   card must say the status shows automatically from the check-ins. As written, «وإظهار حالتها المباشرة» still
   reads as something the owner does. The conflict is in the plan itself (§8 against §9), not the executor's
   doing. About's step 3 and the verified card do say «تلقائيًا». *Fix:* the owner picks the words, for example
   «…وإدارة ساعاتها وأسعارها، وتظهر حالتها المباشرة تلقائيًا من تسجيل الحضور.» in both languages. *Where:* the
   fix PR, once the owner approves the Arabic.
4. **nit — for a moment, Home's heading says «المساحات الأقرب إليك» over the "available now" cards.**
   `useHomeSpaces.ts` sets `title` from `nearest` (≈ line 64), and `useDirectoryQuery` keeps the previous key's
   answer (`keepPreviousData`). *Scenario:* on a weak connection the visitor grants near me. The heading switches
   to «المساحات الأقرب إليك» at once, while the six "available now" cards stay, not in distance order and with
   no distance, until the nearest answer arrives (seconds on 3G). Only `aria-busy` marks it; nothing on screen
   does. *Fix:* keep the previous title while `query.isPlaceholderData`, or show the skeletons when the request
   changes between available and nearest. *Where:* the fix PR. I saw this in the code; I did not run it.
5. **nit — a second «إعادة المحاولة» while still offline is silent to a screen reader.**
   `shared/routing/states/RetryState.tsx` (`retry`, ≈ lines 38-41; the `role="status"` line ≈ 61-63) sets
   `stillOffline` to `true`, which it already is after the first press. The live region does not change, so
   nothing is announced again, and a blind visitor cannot tell the press was received. *Fix:* clear the line,
   then set it again on the next frame (or key it by a press count). Test 80 can press twice. *Where:* the fix
   PR.

## Other findings

6. **nit — on a phone, the gallery's only tile hides «عرض كل الصور (n)» from screen readers.**
   `Gallery.tsx:32` gives each tile `aria-label={tile.view.label}` («عرض الصورة 1»). That label replaces the
   tile's content, including the pill at lines 45-49 and the image's alt «الصورة 1 من n». Carried item 3 now
   leaves the first tile alone below 768 px, so a screen-reader user on a phone is never told there are more
   photos. *Fix:* on the first tile, when `more` is set, use `more.label` as its name or point
   `aria-describedby` at the pill. *Where:* the fix PR.
7. **nit — `statusViewOf` does not yet give the live status's word and role one home.** The report justifies the
   export as "the rule keeps one home". But `useSpacePage.ts` (≈ lines 96-124, the `live` badge) still maps
   `AVAILABLE`/`FULL`/`CLOSED` to `available`/`full`/`closedNow` and `success`/`warning`/`neutral` by hand. *Fix:*
   the page uses `statusViewOf(liveQuery.data.status, copy)`. *Where:* the fix PR.
8. **nit (tests) — three behaviours have neither a test nor a real-run case.** (a) Leaving a page that reserved
   the footer's room gives it back. The routes test covers only the two static cases, so the cleanup in
   `footerRoom.ts:15-20` could be deleted with no test turning red. (b) Home's «اختر منطقتك»: the scroll to the
   areas' heading and the focus on it. (c) Home's «حدّد موقعي على الخريطة», which starts the pick and opens
   `/spaces?view=map`. The real run checked neither (b) nor (c), going by its report. *Fix:* one routes test for
   (a), for example a space with a bar, then «الرئيسية» → no `pb-24`; one Home test each for (b) and (c).
   *Where:* the fix PR.
9. **record — `useAreaCounts` ignores `truncated`.** `useAreaCounts.ts:17-25` counts the unfiltered pins. Past
   1,000 publicly listed spaces, the pins come back truncated, and every area's count and «كل المناطق»'s total
   are silently too low. That cannot happen with today's 59 spaces, but nothing says so. *Fix:* record it as
   finding 137 (a count endpoint, or summing a server count, when the directory grows); or show no number when
   `truncated`. *Where:* a finding to record.
10. **record (plausible) — the two site tests that time out at 3 s on clean `main` look like a test defect, not
    a slowness of the app.** "shows the Directory under its title" (`routes.component.test.tsx:152`) and "marks
    the current page's link" (`SiteLayout.component.test.tsx:95`) are each the first test in their file to open
    `/spaces`. Its `lazy` import pulls the whole `directory` feature through Vitest's on-demand transform inside
    a `findBy` limited by `asyncUtilTimeout: 3_000` (`test/componentSetup.ts:10`). The cold transform counts
    against a wait meant for rendering; production serves the chunk already built. That is finding 87's family.
    The cost now grows: Home imports `@features/directory`, so every test that renders `/` pays it too. *Fix:*
    record it with finding 87 (import the lazy pages once in a `beforeAll`, or a test-only longer wait for the
    first lazy page). Plausible only: I could not run it, and CI passes both.
11. **nit (docs).** (a) `docs/features/directory.md:4`'s Authority line ("On the web, the directory's list, its
    filters and near me, its map, and a space's page are built") does not name Home's spaces and the areas'
    counts, or About's legend. (b) `docs/features/lookups.md:5`'s Scope line still ends at "the site's
    Directory", without Home. (c) The new *status states* bullet in `architecture.md` §2 (≈ line 104) carries no
    "(2026-10-24, #111)", unlike its neighbours. (d) `overview.md`'s Directory line ends "About, with the
    statuses' legend and the platform's contact": the contact is `platform-settings`', not `directory`'s (one
    home per fact). (e) The JSDoc at `SiteFooter.tsx:6` runs past the 100-character line. *Where:* the fix PR.
12. **nit — `HomeSearch` hard-codes `maxLength={80}`,** copying `DirectorySearch.tsx:14`. The server's rule is
    `SPACE_NAME_MAX_LENGTH` (80, `@masaha/shared/spaces`, used by `directoryQuerySchema`'s `q`), and two literal
    copies drift. *Fix:* both read the shared constant. *Where:* the fix PR, or record it.
13. **record — a failed poll keeps a status that still says «الحالة مباشرة الآن».** Carried item 1 does what was
    decided (`useSpacePage.ts:94-97`: the failure line only when nothing was ever read). But after many failed
    60-second refreshes, the badge still shows the last status as live, with no sign that it is old. A product
    point for the owner, not a defect. *Where:* record it, or decide it at the in-person review.
14. **nit (the report only) — the report says Home listed "the 21 areas that hold spaces".** The run's own
    output (`scripts\run4-layouts.txt`, line 2) shows 17 area cards and then «كل المناطق · قطاع غزة · 59
    مساحة», which matches the inventory's 17 areas with pins. "21" is area 2's count. The code is right; only the
    report's sentence is wrong.

## The departures, judged

- **All three site boundaries on `SiteRouteError`** (the plan said two): right. `FocusLayout` has two route
  groups (sign-in, the forced password change), each with its own boundary (`routes.tsx`), and both deserve
  «الرئيسية». Fine.
- **`useHomeSpaces({ chooseArea, openMap })`**: interface only. The state line needs both actions, and
  `HomeSpaces` still takes the plan's props. Fine.
- **`OWNERS_ANCHOR` / `SITE_PATHS.owners` in commit 4**: commit 4's owners' card links there, so the commit
  stays whole. Fine.
- **`statusViewOf` exported beside `LiveStatusBadge`**: fine as an export; see finding 7 for the copy that
  remains.
- **Two tests outside the plan's list** (`SiteLayout.component.test.tsx`, `App.component.test.tsx`): both
  expected the placeholder heading «Home». Changing them was needed and limited to the heading. Fine.
- **The carried history line in commit 3's `directory.md`**: the line about the carried fixes rides in a feature
  commit. Not ideal for atomic commits, but the stated reason (a conflict beside commit 3's own line) holds.
  Acceptable.
- **The offline case's order**: going online first fires `online`, and `RetryState` reloads by design (its effect
  at lines 25-36). Pressing «الرئيسية» while still offline was the only way to see it. Fine.
- **The touch scroll by `Input.dispatchTouchEvent`**: the report's control (no scroll even over plain text) shows
  that `synthesizeScrollGesture` does nothing here. I read this in the report only. Fine.
- **A ninth carried commit (the focus fix)**: the carried file asked for exactly this ("if it is not, that is a fix
  here, with a test"). `Gallery.tsx`'s `onCloseAutoFocus` and the opener index are right, and the test closes
  with Escape after moving to the next photo, then checks that tile 2 has the focus. Fine.
- **Test 77's first rewrite left its breaks green**: the final test (`useLiveStatusQuery.component.test.tsx`)
  would fail under both breaks. With `refetchIntervalInBackground: true`, the tick at 60 s while hidden sends a
  third request, and `advanceTimersByTimeAsync` lets it go out before `toHaveLength(2)`. With
  `refetchOnWindowFocus` removed, the first return still refetches (the data is 60 s old, past the 30 s
  `staleTime`), but the second, immediate return finds it fresh, so the fourth request never comes and the
  `waitFor` fails. The events are dispatched as the browser sends them: `visibilitychange` bubbling from
  `document` to `window`, where TanStack v5's focus manager listens; no `focusManager` call is left. I reasoned
  this from the code; I did not run the breaks.

## Checked and fine

- **Carried 1–8:** 1 checks `data === undefined` (a first-ever failure still says «تعذّر قراءة الحالة الآن»; the
  new test fails on the old order). 2 prints `viewer.total`, with a test of 1/7 → 6/7 → 7/7 → 1/7. 3 hides
  tiles 2–5 below `md` and uses `grid-cols-1`; the pill stays on tile 1 (`Gallery.tsx:45-49`); hidden lazy
  images are never fetched. 4: see above. 5: finding 131's line 5 names the cards', the pins' and the page's
  status; its index line holds only the title. 6: `useFooterRoom` goes through the outlet's context (the
  pathless boundary route renders no `<Outlet>` of its own, so the context reaches `SpacePage`), the rule
  matches the bar's (`WHATSAPP` or `PHONE`), and its test fails under the pathname rule. 7: Leaflet's own
  classes (`leaflet-grab`, `leaflet-touch-drag`, `leaflet-touch-zoom`) and both zoom buttons. 8: the hidden tab,
  touch, bottom and gallery shots I read in the report only.
- **Home:** the search trims and encodes `q` (test 85: `?q=Hub%20%26%20Co`). `limit: 6` with `availableNow`, or
  `sort: 'distance'` with the point only in `Masaha-Near`; the params hold no coordinate (test 83). The nearest
  answer lives under the list key, which `hasNear` drops on «مسح موقعي». «عرض الكل» → `/spaces?available=1`, or
  `/spaces`, whose default order with a point is distance (the real run reports the same first six). Area cards
  only for counts > 0, in the catalogue's order, the governorate isolated, «كل المناطق» with the total, one
  retry for both reads (test 84). The empty state offers «تصفّح كل المساحات».
- **About:** `#contact` before `#owners` (test 85), each with `PlatformContact layout="row"`, and their text alone
  with none (test 86; `PlatformContact` returns `none` = `null`). No hard-coded contact, no university line. The
  legend is a `dl` with `LiveStatusBadge` and «لا تتوفر حالة مباشرة». Its words match §9.
- **Errors and offline:** «الرئيسية» after «إعادة المحاولة» inside the site's shell (routes test). The retry does
  not call `onRetry` while `navigator.onLine` is false (test 80, its break red per the report). `online` still
  reloads. `WifiOffIcon` is built on the layer's `Icon` without the mirror flag, exported from `icons/index.ts`
  and the layer's barrel, and shown in the showcase. The general error's line matches design issue 39 in both
  languages, shared by every shell. The session's `RetryState` unmounts on retry (`restoring`), so its new
  `trying` state cannot stick.
- **Structure:** one `h1` per page; `h2` sections, `h3` in the cards (`CardTitle` is a `div`); sections named by
  their headings; logical classes (`ps-6`, `end-3`, `self-start`); semantic tokens only; every string in both
  catalogues, Arabic `satisfies Catalogue['site']`, the count through `arabicPlural`'s six forms.
- **Weight:** Home and About stay `lazy` routes; `SiteRouteError` (static) imports only `Button`, `Link` and the
  copy. The first-download sizes and `check:build` I read in the report only.
- **Foundation §12** lists components, not icons, so it was rightly left unedited (check 5l).
- **Docs:** `#111` in the histories of `directory.md` and `lookups.md` and in architecture's *Built* line; the
  README's directory line; `overview.md`'s *Built* lines. Commit subjects are ≤ 50 characters, each with a body;
  no tool attribution, no trailers; the PR description says "Carried from #108".
