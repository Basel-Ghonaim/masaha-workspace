# DIRECTORY_PROD — the directory's filters in production — PLAN

> Worker: Claude Code (worker A, `C:\dev\masaha\app`), Opus 5.5, effort xhigh · Planned 2026-11-08 on `40cb481d`
> (`origin/main`, tree clean, no open PR, no finding above 213 on any branch) · Branch on approval:
> `feat/directory-filters` from the latest `origin/main` · Expected PR **#138** (checked again before the push).
> Saved, once approved, to `C:\dev\masaha\workspace\TASKS\DIRECTORY_PROD\2_PLAN.md`; report to `4_REPORT.md`.

## 1. Summary

This builds the directory's new filters in the shared package, the API and the web, as the prototype (#137) shows
them, and changes their documents:
- the price as a subscription chosen in a new design-system `SegmentedControl`, with a range under it, an order in
  the sort, and the price on the card;
- «الدوام»: «مفتوحة الآن» (on the hours, on Gaza's clock, replacing `availableNow`), «مفتوحة مساءً» and Friday;
- the by-hours state of unverified spaces, and "hours not available";
- the panel's new order, the 4/12 column, the sheet's Arabic plurals, and 18 cards a page (web and prototype);
- the fix of the flaky Home test (finding 214) and #136's two nits.

## 2. Contract

**Scope.** Items 1–15 of the owner's decisions (§4), built as §4.2 says, with the owner's answers to §15 (OD).

**Acceptance criteria**
- [ ] Finding 214 is recorded with its root cause, its test is fixed in the test only, and the full component lane passes three times in a row locally, then in CI.
- [ ] `ListPagination` reads `search` once; its comment names the rule, not a workspace folder.
- [ ] `SegmentedControl` is in the design system: a radiogroup with arrows that follow the direction, Home/End, one roving tab stop, axe-clean. It is documented in `foundation.md`, has a showcase section, and passes `check:classes`.
- [ ] The API filters by `period` alone, by `priceMin`/`priceMax` (in agorot, with the period), by `openNow` and `evening`, and orders by `priceAsc`/`priceDesc` (with the period, ties ended by the id). Every filter applies before the page is cut, and `availableNow` is gone.
- [ ] Hidden prices are never filtered, priced or ordered.
- [ ] The card carries `priceAgorot` (with a period) and `hoursStatus`; the pin carries `hoursStatus`.
- [ ] The web shows the panel «المنطقة · السعر · الدوام · أخرى». The range is whole shekels with placeholders; the price order is absent under «الكل»; «مسح» clears every filter and keeps the order; the active count counts each box once; the address round-trips; an old `available=1` opens unfiltered.
- [ ] Cards show the price and the by-hours badge (neutral); «ساعات العمل غير متوفرة» shows on the card and the page; Home lists the spaces open now.
- [ ] The column is 4/12 at 1024–1279 px; the sheet's button uses the five Arabic forms; the web asks 18 a page, and the prototype pages at 18.
- [ ] Every document §8 lists is updated; nothing claims what is not built.
- [ ] Lint, typecheck, format, classes, links, conflicts, build + `check:build`, and all three lanes are green locally and in CI; the PR is `CLEAN`.

**Out of scope** (the owner's "Not in this PR"): the owner's space-profile redesign; the visual identity and logo;
women's spaces and the owner-declared evening feature. Also out of scope: any migration, `db:seed` of `masaha_dev`,
and any merge.

## 3. Reading done

- **Workspace:** `1_PLAN_PROMPT.md` and `0_OWNER_DECISIONS.md`, both whole.
- **Bootstrap and process:** `CLAUDE.md`; `workflow.md`; `engineering-principles.md`; `testing.md`; the map (`docs/README.md`); the findings index. The open findings are 23, 65 and 152 (none touch this work); 213 is the highest number.
- **Capabilities:** `features/directory.md` (whole), `spaces.md` (lines 1–241), `occupancy.md`; `lookups.md` and `space-links.md` for the admin list; `announcements.md` (its closures).
- **Platform documents:**
  - ADR 0008;
  - `data-model.md`: conventions (hours), derived values (live status, stale prices, closures);
  - `api-contract.md`: §1–4 and *Directory (public)*;
  - `conventions.md`: §5, §8 *Pure rules*, §9 *occupancy* and *Composed reads*, §11;
  - `foundation.md`: §3, §4, §8–§12;
  - `overview.md`.
- **Prototype:**
  - `Directory.html` (whole);
  - `shared.jsx`: `gazaNow`, `openNow`, `statusWord`, `LiveStatus`, `TodayHours`, `FilterSheet`, `resultsLabel`, `usePaged`;
  - `space-parts.jsx`: `StatusLine`, `TodayLine`, `HoursSection`;
  - `CHANGES.md` Refactor 1, `INDEX.md`, and the `Home.html` section.
- **Code:**
  - `packages/shared/src/directory/*` and `core/gazaTime.ts`;
  - the API's `directory/*`, `spaces/public/*`, `spaces/hours/hours.repository.ts`, `occupancy/liveStatus.ts` and `occupancy.service.ts`, `announcements` (`closedAt`), and the `space_hours` CHECK;
  - the web's `features/directory` (filters, `filtersOf`, `requestOf`, `priceBounds`, the price hook, the panel, the list hook, the sort, `cardView`, `todayHours`, the card, Home's spaces, the page's hours and status), `ListPagination`, and the admin list's `rowView`;
  - the design system's `RadioGroup` and `ToggleGroup`, their tokens, and the Radix radio group 1.4.7 source;
  - the copy catalogues (`directory`, `spaceLinks`, `audit`), `HomePage.component.test.tsx`, `HomeSearch.tsx`, and `warmLazy.ts`;
  - the CI log of #137 (run 42384998638, both attempts).

## 4. The owner's decisions — binding (verbatim from `0_OWNER_DECISIONS.md`)

> **The owner's bar (his words, 2026-11-08):** the tests must work well and in the right direction — never bent to
> pass; the filters' tests must be very strong, with no gap.
>
> ## First commit
>
> 1. **Finding 214 — the flaky Home test.** `apps/web/src/pages/site/public/home/HomePage.component.test.tsx` ›
>    «Set my location on the map» starts the pick on the Directory's map: after the navigation to `/spaces?view=map`
>    it waits for the searchbox with `findByRole`'s default 1 s; on CI under load the lazy map view takes longer. It
>    failed twice on #137 (which changed no app code) and passes locally alone. Fix the cause in the test (wait for the
>    route's content correctly), not with a retry; record finding 214 (check the findings index first).
> 2. **#136's two nits:** `ListPagination.tsx` names a variable `here0` (read the location once as `search`, then
>    `here = searchKey(search)`); its comment cites the workspace task «QUICK_FIXES_1» — a repository comment names the
>    rule or the PR, never a workspace folder.
>
> ## The filters (as built in the prototype, #137)
>
> 3. **Price — the subscription.** A segmented choice «الكل · ساعة · يوم · أسبوع · شهر», «الكل» by default (no price
>    filter). A new design-system component `SegmentedControl` (a radiogroup: one choice, arrow keys following the
>    direction, Home/End, roving tab stop), documented in `foundation.md`. In the API, the period alone now **filters**:
>    only the spaces with that price, hidden prices excluded (today the period alone filters nothing, S1).
> 4. **Price — the range.** «من / إلى» in whole shekels, shown once a subscription is chosen; placeholders = the lowest
>    and highest price of that subscription; whole numbers above zero, Arabic-Indic digits accepted, «إلى» under «من»
>    said on «إلى»; an invalid bound is said on its field and not sent. The API keeps `priceMin`/`priceMax` in agorot,
>    which need the period.
> 5. **Price — the order.** In the sort only: «الأرخص شهريًا» / «الأغلى شهريًا» (by the chosen subscription; English
>    "Monthly price: low to high / high to low"); the two items exist only once a subscription is chosen (not
>    disabled — absent); clearing the subscription while sorting by price returns to «الأحدث تحديثًا». The API gains
>    a price order in both directions that requires the period, applies the hidden-price rule, and ends with the id.
> 6. **The card's price.** While a subscription is chosen, each card shows that price («15 ₪ / يوم», LTR-isolated): the
>    API's card carries it. Revises D4 (the card carries no price).
> 7. **«مفتوحة الآن» (`openNow`).** Open now by the space's hours on **Gaza's clock** and **no closure in force**, for
>    verified **and** unverified spaces; a FULL verified space stays (its badge says so); a space without hours never
>    passes. It **replaces** `availableNow`: Home's «المتاحة الآن» section reads it, and `availableNow` leaves the API
>    (nothing else reads it). Revises ADR 0008 (the directory's filter selected `AVAILABLE`).
> 8. **«مفتوحة مساءً» (`evening`).** The space closes at 20:00 or later on at least one of its open days (its weekly
>    schedule, not today). A space without hours never passes. (An owner-declared evening feature is a later task.)
> 9. **The card's state.** Verified spaces: the live status as today (متاح / ممتلئ / مغلق الآن). Unverified spaces
>    **with hours**: «مفتوحة الآن» / «مغلقة الآن» by their hours (and closed under a closure in force), as a
>    **neutral** badge — never the live status's colours; without hours: «لا تتوفر حالة مباشرة». The API carries this
>    by-hours state as a field of its own, apart from the live status.
> 10. **Hours are optional.** A space without hours stays in the list and every other filter; its card and its page
>     say «ساعات العمل غير متوفرة» / "Hours not available"; the admin's spaces list marks it «بدون ساعات». No default
>     hours are ever assumed.
> 11. **«ممتلئ»** stays as built (desk check-ins against the capacity, plus the staff's override) — a badge, never a
>     filter.
> 12. **The panel**, top to bottom: «المنطقة» (unchanged) · «السعر» · **«الدوام»** (checkboxes «مفتوحة الآن», «مفتوحة
>     مساءً», «مفتوحة يوم الجمعة») · **«أخرى»** (checkboxes «المساحات الموثّقة فقط», «أسعار للطلاب»). The «المساحات»
>     heading and its switch go. Each box counts once in the active count; «مسح» clears every filter (the subscription
>     and the range included), not the order.
> 13. **Small fixes:** the filter column is 4 of 12 between 1024 and 1279 (3 from 1280) so the five subscriptions fit;
>     the sheet's button in Arabic plurals (0 «لا توجد نتائج», 1 «عرض نتيجة واحدة», 2 «عرض نتيجتين», 3–10 «عرض N
>     نتائج», 11+ «عرض N نتيجة»); the card's «اليوم …» line reads Gaza's day, not the browser's.
> 14. **18 cards a page** in the directory (divisible by 1, 2 and 3 columns; lighter on weak connections) — in the web
>     and in the prototype (`docs/design/prototype/Directory.html`, its `INDEX.md`/`CHANGES.md` line). The API's
>     `limit` already allows it.
>
> ## Documents in the same PR
>
> 15. `docs/features/directory.md` (D4, U1 kept, U5, S1, the new rules), `docs/api/api-contract.md` (the directory's
>     query and card), ADR 0008 (a revision line: the directory filters by the hours; the by-hours state of unverified
>     spaces), `docs/frontend/design-system/foundation.md` (`SegmentedControl`), and any other document a change makes
>     untrue.
>
> ## Not in this PR (parallel tasks, their own branches)
>
> The owner's space profile redesign; the visual identity and the logo; **spaces for women + the owner-declared
> evening feature** (one task). The worker leaves their files alone and records any overlap it sees.

### 4.2 Each item as it will be built

The tests named here are in §10. The documents are in §8, gathered by item there. Some items are built differently from how the decisions are worded (1, 3, 9, 10, 13, and the active count); §5 and §15 explain each one.

**Item 1: finding 214.**
- **Root cause.** The CI log of #137 shows the failure is not a timeout. The test failed at **156 ms** (attempt 1) and **206 ms** (attempt 2), at line 101's `toBeInTheDocument()`, with "element could not be found in the document". `findByRole` had already returned an element, and that element was then removed from the page.
  - Home's hero search (`HomeSearch.tsx`) has the same accessible name, "Search for a space", as the Directory's.
  - The test's `waitFor` checks `router.state.location`, which changes before React has rendered the Directory in place of Home.
  - On a loaded machine, `findByRole` finds **Home's** search box in that gap. React then removes Home, so the element is detached.
  - Nothing lazy is involved: the searchbox sits outside the map's `Suspense`, and the route's module was already imported in `beforeAll`.
  - §5 SD-1 explains why this changes the owner's wording of the cause, but not the remedy.
- **Fix (test only).** After the location check:
  - wait for content that only the Directory has: `findByRole('heading', { level: 1, name: 'Workspaces' })` (Home has no such h1);
  - then assert that exactly one searchbox named "Search for a space" exists (`getByRole`, which throws on two);
  - then, as before, wait for near me's button to leave.
- **Hygiene.** The file's `beforeAll` becomes `warm(...)` with a 60 s timeout (testing §3 rule 8). This is not the cause; it is the rule the file broke.
- **Files:** `HomePage.component.test.tsx`; the new finding 214 and its index line (Resolved).
- **Tests:** T80.

**Item 2: #136's nits.**
- `ListPagination.tsx`:
  - `const search = useLocation().search;` then `const here = searchKey(search);`;
  - the comment becomes «A list of one page (or none) has nothing to move between, so it draws no bar.»;
  - no task or PR number, per engineering-principles §8, which also forbids PR numbers in comments.
- This is a pure refactor: the existing `ListPagination` tests stay as they are (T81).

**Item 3: the subscription.**
- **Shared:** no schema change for `period`.
  - The API **already** filters by the period alone (`list.api.test.ts` `?period=MONTH`).
  - It is the web that never sent the period without a bound (`requestOf`: `bounded && { period }`); §5 SD-2.
- **API:** nothing new for the period itself. The price predicate is rewritten for items 5 and 6 (one lateral `min()`), and T10 proves it.
- **Web:**
  - `DirectoryFilters.period` becomes optional: `undefined` is «الكل»; `DEFAULT_PERIOD` goes.
  - The address and the request write `period` on its own.
  - `usePriceFilter` is rewritten:
    - the subscription is `SegmentedControl` options «الكل · ساعة · يوم · أسبوع · شهر», named «نوع الاشتراك», inside the «السعر» group;
    - a choice applies at once;
    - «الكل» clears the period, both bounds (their texts too) and a price order.
- **Tests:** T1, T10, T14, T50–T52.

**Item 4: the range.**
- **API:** the bounds rules stay as they are (agorot, 1–10,000,000, `required` on `period`, `out_of_range` on `priceMax`). They are proven harder: T2–T4, T11, T13.
- **New, for the placeholders (OD1 a):** `GET /price-ranges`.
  - It answers `PriceRanges = Record<PricePeriod, { minAgorot, maxAgorot } | null>` over the general prices of the publicly listed spaces whose prices are shown.
  - It reads `spaces`' `publicListing.priceRanges(filter)`, with the listed areas and the verified ids resolved first.
  - Its answers are kept for 30 s with an `ETag`.
- **Web:**
  - The range shows only once a subscription is chosen.
  - Its placeholders are `pricePlaceholders(range)`, in whole shekels: the lowest rounded down and the highest rounded up, so a placeholder never shows a decimal (DI-6).
  - `priceBounds` stays (it already reads Arabic-Indic digits and refuses `0`, letters, decimals and anything above 100,000). Its `belowMin` words become ««إلى» أقل من «من».» (DI-5).
  - The help line under a subscription is «بالشيكل، على السعر الشهري.», and the hint under «الكل» is «اختر نوع الاشتراك لتحديد نطاق السعر أو الترتيب حسبه.».
  - A refused bound is said on its field and left out of the request, as it is today.
- **Tests:** T2–T4, T11, T13, T19, T44, T52.

**Item 5: the price order.**
- **Shared:** `DIRECTORY_SORTS` adds `priceAsc` and `priceDesc`. Either one without `period` is `invalid_choice` on `sort`, as `relevance` without `q` is.
- **API:**
  - `PublicOrder` adds `{ by: 'price', direction }`.
  - The SQL orders `price ASC, id` or `price DESC, id`. Both directions end by the id ascending, as `relevance` does.
  - The key is the card's price (item 6), so a hidden price can never enter the order: the price filter left that space out already.
- **Web:**
  - The sort lists «الأرخص {شهريًا…}» / «الأغلى …» only while a period is set; they are absent, not disabled, under «الكل».
  - The order is kept in the address as `sort=priceAsc|priceDesc`; `filtersOf` drops a price order that has no period.
  - Choosing «الكل» while ordered by price returns the order to its default (§5 SD-8).
- **Tests:** T7, T16–T18, T53, T54.

**Item 6: the card's price.**
- **Shared:** `DirectorySpace.priceAgorot?: number`, present exactly when the query has `period`. The map pin carries none.
- **API:**
  - The price is one `CROSS JOIN LATERAL (SELECT min(amount_agorot) …)` over that period's **general** prices within the bounds, set to null where the prices are hidden.
  - The filter keeps the rows where it is not null and the prices are shown.
  - The same value is the card's price, the order's key and the filter's test (OD4 a).
- **Web:**
  - `cardViewOf` gives `price`: `card.price({ price: isolated(priceText(…)), period: card.periods[p] })`, which reads «‏15 ₪ / يوم» or "₪15 / day".
  - The card draws the price after today's hours, and adds it to the link's `aria-describedby` (DI-8).
- **Tests:** T12, T14, T15, T45, T58.

**Item 7: `openNow`.**
- **Shared:**
  - `openNow` is a stringbool on the list and the map.
  - `availableNow` is removed. An old client's `availableNow=true` is then dropped, as any unknown key is (EC4), and answers unfiltered.
- **API:**
  - The directory now receives the one clock (`now`, wired in `app.ts`) and reads it once per request.
  - With `openNow`, `announcements.closedSpaceIdsAt(at)` lists every space under a closure in force. It is a new read that shares one `where` builder with `closedAt`, so the closure's rule stays in one place (EC8).
  - `spaces` then filters in SQL: `EXISTS (space_hours today, gazaClockOf(at).dayOfWeek, opens_minute <= minute < closes_minute) AND NOT s.id = ANY(closedIds)`. These are `openRangeAt`'s exact comparisons.
  - `occupancy.availableAmong` is deleted. The list's `onlyIds` stays, for the favourites.
- **Web:**
  - `filters.openNow` is kept in the address as `open=1`, sent as `openNow: true`.
  - Home's request is `{ limit: 6, openNow: true }`. Its title and empty state follow DI-4, and «عرض الكل» leads to `/spaces?open=1`.
  - An old `available=1` is read as nothing.
- **Override:** whether a verified space set «مغلق» by hand stays in the list is OD2.
- **Tests:** T5, T6, T20–T28, T31–T34, T56, T61.

**Item 8: `evening`.**
- **Shared:** `evening` is a stringbool on the list and the map.
- **API:**
  - `EXISTS (space_hours h WHERE NOT h.is_closed AND h.closes_minute >= EVENING_FROM_MINUTE)`, with `EVENING_FROM_MINUTE = 1200` a constant beside `FRIDAY` in `publicListing.repository.ts`.
  - It reads the week, never the clock. A space without hours has no rows, so it never passes.
- **Web:** `filters.evening` is kept in the address as `evening=1`, sent as `evening: true`.
- **Tests:** T5, T29, T33.

**Item 9: the by-hours state.**
- **Shared:**
  - `HoursStatus = 'OPEN' | 'CLOSED'` and `HOURS_STATUSES`, in `@masaha/shared/occupancy` beside `LiveStatus`.
  - `DirectorySpace.hoursStatus` and `MapPin.hoursStatus` are `HoursStatus | null`; `PublicOccupancy.hoursStatus` follows if OD3 (a).
- **API:**
  - A pure `hoursStatusOf({ week, closureNow, at })` in `occupancy/liveStatus.ts` (the live status's file): `null` without hours, `CLOSED` under a closure, else `openRangeAt ? 'OPEN' : 'CLOSED'`.
  - `liveStatusFor(targets)` becomes `publicStatesFor(targets, at)`. It answers `{ liveStatus, hoursStatus }` per space from the same reads (no extra query), at the directory's one instant.
  - It is set for **every** space, verified or not (§5 SD-6). The web draws it only for an unverified space.
- **Web:**
  - In `cardViewOf`, an unverified space's `status` is `{ label: «مفتوحة الآن»|«مغلقة الآن», variant: 'neutral' }` from `hoursStatus`; with `null` it falls back to `noStatus`.
  - A verified space is unchanged (`statusViewOf(liveStatus)`).
  - The map's chosen card and each pin's name follow, since they use the same view. The pin's mark stays the live status's: an unverified space's mark is dashed.
  - The page follows if OD3 (a).
- **Tests:** T30, T31, T35–T37, T45, T58, T59, T66.

**Item 10: hours are optional.**
- **API:** no rule changes. A space without hours is already listed and passes every filter except `openNow`, `evening` and `openFriday`; T33 proves it.
- **Web:**
  - `todayHours(null)` gives «ساعات العمل غير متوفرة» / "Hours not available" (it drew nothing until now). The card, the map's card and the page's status card show it.
  - The page's hours section's `none` reads the same (it was «لم تُضف ساعات العمل بعد»).
- **Admin list:** OD5. Recommended: no change, because «ناقصة: ساعات العمل» already marks such a space (§5 SD-4).
- **Tests:** T22, T29, T33, T46, T58, T59, T65.

**Item 11: «ممتلئ».** No change: a badge, never a filter. T24 proves that a FULL space stays under `openNow`.

**Item 12: the panel.**
- `FiltersForm` reads «المنطقة» (the slot), then «السعر» (`PriceFilter`), then «الدوام», then «أخرى».
- The last two each use a new `CheckGroup` component: a labelled group of `Checkbox` rows, each its own horizontal `Field`.
  - «الدوام»: «مفتوحة الآن», «مفتوحة مساءً», «مفتوحة يوم الجمعة»;
  - «أخرى»: «المساحات الموثّقة فقط», «أسعار للطلاب».
- «المساحات», its two switches and its note go. Student prices and Friday move from `ToggleGroup` chips to checkboxes.
- The active count is the place, the subscription (with or without its range), and each of the five boxes, once each: seven at most (OD6 a).
- «مسح» clears the place, the subscription with both bounds and their texts, and the five boxes. It keeps the search, the view and the order, unless the order is by price (§5 SD-7).
- **Tests:** T51, T54, T55.

**Item 13: small fixes.**
- **The column.** In `DirectoryList`, the sidebar is `lg:col-span-4 xl:col-span-3` and the results `lg:col-span-8 xl:col-span-9`. This is checked by hand at 1100 and 1300 px; layout is not a component lane's (§12 V7).
- **The sheet's button.** `filters.show` takes the plural forms: one «عرض نتيجة واحدة», two «عرض نتيجتين», few «عرض N نتائج», many and other «عرض N نتيجة». `showNone` reads «لا توجد نتائج». English: "Show 1 result" / "Show N results" / "No results". The other lists' sheets are already plural; DI-10.
- **Gaza's day.** It is **already built**: `todayHours` reads `gazaClockOf(now).dayOfWeek`, and `todayHours.unit.test.ts` proves an instant past Gaza's midnight is the next day. Only the prototype's `TodayHours` reads the browser's day (§5 SD-5, OD7).
- **Tests:** T60, T46.

**Item 14: 18 a page.**
- **Web:** `DIRECTORY_PAGE_SIZE = 18` in `requestOf.ts` replaces `DEFAULT_PAGE_SIZE` there.
- **Prototype:** `Directory.html`'s list renders `usePaged(results, 18)` with its nav under the grid.
- **Design docs:** `CHANGES.md` gets row R9 in Refactor 1 and a note on P6 that the Directory pages at 18. `INDEX.md` gets a line only where a frame describes the Directory's paging (EC19).
- **Tests:** T38, T57.

**Item 15: documents.** §8 lists them.

## 5. Stronger decisions (including the proposed alternatives)

Each entry gives what, why, its cost and a recommendation; a ⚑ marks a challenge to the owner's wording.

- **SD-1 ⚑ (decision 1: the cause).**
  - **What:** the cause is an ambiguous query, not the 1 s wait. Its wait matched Home's own search box while Home was leaving.
  - **Why:** the evidence is in §4.2, item 1. The fix the owner asked for, "wait for the route's content correctly, not a retry", is kept; only the explanation in finding 214 changes. Warming the map, or raising the wait, would leave the race in place.
  - **Cost:** none.
  - **Recommend:** as planned.
- **SD-2 ⚑ (decision 3: "today the period alone filters nothing").**
  - **What:** in the API it already filters. The gap is the web's, which held a period until a bound was typed.
  - **Why:** the code (`directory.service.ts` `price: query.period && …`) and the test at `list.api.test.ts:228`.
  - **Cost:** none. No API change is made for it, but T10 makes the proof exhaustive.
  - **Recommend:** record the corrected fact in `directory.md`.
- **SD-3 ⚑ (decision 7).**
  - **What:** a verified space whose staff set «مغلق» by hand (an override `CLOSED` in force) would stay under «مفتوحة الآن» with its own badge saying «مغلق الآن».
  - **Why:** the visitor reads a contradiction on the very card the filter kept. The staff use the override exactly when the hours are wrong today, such as a power cut.
  - **Cost:**
    - one more id set from `occupancy`: the verified spaces with a `CLOSED` override in force, which the rule uses only while open by hours and under no closure, both already true under `openNow`;
    - one more test.
  - **Recommend:** leave such a space out. OD2.
- **SD-4 ⚑ (decision 10: «بدون ساعات»).**
  - **What:** the admin's list already says «ناقصة: ساعات العمل» for a space whose hours were never saved. A space has no week exactly when its hours group is missing, because the first save writes all 7 rows.
  - **Why:** a second badge would say the same thing twice on one row.
  - **Cost:** none.
  - **Recommend:** no new badge. T65 proves the existing line; `space-links.md` says it is the mark. OD5.
- **SD-5 ⚑ (decision 13: Gaza's day).** It is already built and proven in production; only the prototype differs. There is nothing to build in the web; OD7 covers the prototype.
- **SD-6 (decision 9).**
  - **What:** `hoursStatus` is set for every space, not only the unverified ones.
  - **Why:**
    - one rule, with no "verified" branch in the API;
    - it lets T31 bind the SQL filter to the TypeScript rule for every space;
    - it lets the binding test say: for a verified space with no override, `liveStatus = CLOSED` exactly when `hoursStatus = CLOSED`.
  - **Cost:** one field the web ignores on verified cards.
  - **Recommend:** yes.
- **SD-7 (decision 12: «مسح» keeps the order).**
  - **What:** a price order cannot outlive its subscription, so «مسح» returns a price order to the default and keeps any other order.
  - **Why:** decision 5's own rule.
  - **Cost:** none.
  - **Recommend:** yes; T54 proves both.
- **SD-8 (decision 5: "returns to «الأحدث تحديثًا»").**
  - **What:** with a search in force, the default order is «الأفضل تطابقًا», so it returns to the **default**: updated without a search, relevance with one.
  - **Why:** returning to updated during a search would write `sort=updated` and drop best match unasked.
  - **Cost:** none.
  - **Recommend:** yes.
- **SD-9 (the open-now rule in two places).**
  - **What:** the filter is SQL in `spaces`, which owns the hours; the state and the live status are TypeScript in `occupancy`'s pure file (`openRangeAt`). Both are the same comparison, `opens ≤ minute < closes` on the Gaza weekday, with the same closures.
  - **The alternative:** resolve `openNow` to ids in TypeScript, which reads every listed space's week on each request; at a thousand spaces that is 7,000 rows.
  - **Cost:** the binding test T31, and a line in `data-model.md` naming one rule with its two readers.
  - **Recommend:** SQL plus T31.
- **SD-10 (one instant per answer).**
  - **What:** the directory reads the clock once and hands that instant both to the filter (and its closures) and to `publicStatesFor`.
  - **Why:** two reads at a minute boundary could keep a space under «مفتوحة الآن» whose card says «مغلقة».
  - **Cost:** a `now` dependency for the directory.
  - **Recommend:** yes.
- **SD-11 (decision 6: which price).**
  - **What:** a space can have several general prices for one period (shifts, labels). The card shows the **lowest within the bounds**, which is also the value that orders and that passed the filter.
  - **Why:** a card showing ₪10 under a ₪20–30 range would look like a bug.
  - **Recommend:** yes. OD4.
- **SD-12 (decision 4: the placeholders).**
  - **What:** they need data the web does not have, hence `GET /price-ranges` (OD1). The range covers all listed spaces, as the prototype does, and does not follow the other filters.
  - **Why:** one cached read per visit, rather than one per filter change.
  - **Recommend:** yes.
- **SD-13 (the address keys).**
  - **What:** keep production's scheme (`period`, `min`, `max`, flags `=1`), adding `open` and `evening`, rather than the prototype's `sub`, `other=` and `dir=`.
  - **Why:** old shared links (`?period=DAY&min=10`) keep working, and directory.md's S5 stays true.
  - **Cost:** none.
  - **Recommend:** yes.
- **No document rule is weakened.**
  - testing §3 rule 8 is applied to the Home file (it was not).
  - Engineering-principles §8 keeps PR numbers out of comments, which is stricter than decision 2's "or the PR".

## 6. Related findings

| Finding | Status | Folded? | Why · cost |
|---|---|---|---|
| **214** (new) the Home test's wait finds Home's own search box | Resolved here | **Yes** (item 1) | the owner's item 1 · one test, one file |
| 28, 55, 87 (lazy waits) | Resolved | No | another cause; 214 cites them as ruled out |
| 23, 65, 152 | Open | No | they touch no directory code |
| 215 (new, only if OD7 b) the prototype's Home and `TodayHours` disagree with production | — | Recorded only | not built: `docs/design` is allowed only for item 14 |

Numbers 214–215 are checked against every branch and open PR again before the push. A parallel worker may take 215; if so, the next free number is used.

## 7. The `SegmentedControl`

- **Place.** `apps/web/src/shared/design-system/components/fields/SegmentedControl/` (`SegmentedControl.tsx`, `index.ts`, `SegmentedControl.component.test.tsx`), exported from the layer's `index.ts`. Its category is `fields`, because it chooses a value.
- **API.** It is compound, like `RadioGroup` and `ToggleGroup`:
  - `SegmentedControl` takes Radix `RadioGroup.Root`'s props: `value`, `onValueChange`, an optional `aria-label` or `aria-labelledby`;
  - `SegmentedControlItem` takes `RadioGroup.Item`'s props, with its label as children.
  - It has no `disabled` or invalid styling, because no caller needs one; a filter cannot be wrong.
- **Behaviour.** It is built over Radix's radio group:
  - one choice; `role="radiogroup"` and `role="radio"` with `aria-checked`;
  - one tab stop, which enters on the checked segment;
  - the arrow keys follow `DirectionProvider`: in RTL, ArrowLeft goes to the next segment. Both axes work, and the choice loops.
  - **Home and End choose the first and the last segment.** Radix's roving focus moves the focus there but checks only on the arrow keys (`ARROW_KEYS` in `react-radio-group` 1.4.7, EC1), so the item's `onKeyDown` focuses and clicks that segment itself.
  - Inside a `Field`, it is named by the label and described by the helper (`useField`, `useFieldControl`, as in `RadioGroup`).
- **Look.** Semantic tokens only (rules 1–7 of foundation §11):
  - the track: `bg-muted`, `rounded-(--radius-control)`, `p-1`, `gap-1`, its segments sharing the width (`flex-1 min-w-0`);
  - a segment: `text-label text-muted-foreground`, hover `text-foreground`, the one focus outline;
  - the chosen segment: `bg-card text-foreground shadow-raised` with `border border-(--card-border)`, so the dark theme, which has no raised shadow, still shows its edge (DI-2);
  - 32 px segments, and `pointer-coarse:h-(--control-height)` (44 px) on touch (DI-1).
  - It needs no new token and no arbitrary value. EC2 confirms the utilities exist and the colour pairs are among §5's verified ones.
- **Showcase.** `pages/showcase/sections/fields/SegmentedControlSection.tsx`, its registry entry, and its fixtures text.
- **Documentation.** `foundation.md` §3 (the fields list) and a §12 fields row.

## 8. Files

**Licence.** This item spans both layers, as the prompt assigns: shared, API and web. It writes no migration and changes no schema; a migration, if one seemed needed, would be an OD.

- **Shared:**
  - `packages/shared/src/directory/requests.ts` and `requests.unit.test.ts`; `directory/responses.ts`;
  - `packages/shared/src/occupancy/responses.ts` (`HoursStatus`, and `PublicOccupancy` if OD3 a).
- **API:**
  - `modules/directory/`: `directory.service.ts`, `.controller.ts`, `.routes.ts`, `list.api.test.ts`, `pins.api.test.ts`, `liveStatus.api.test.ts`, `favorites.api.test.ts`; new `filters.api.test.ts`, `hours.api.test.ts`, `priceRanges.api.test.ts`;
  - `modules/spaces/public/publicListing.repository.ts`, `publicListing.service.ts`;
  - `modules/occupancy/liveStatus.ts`, `liveStatus.unit.test.ts`, `occupancy.service.ts`;
  - `modules/announcements/announcements.repository.ts`, `.service.ts`;
  - `src/app.ts` (the directory's `now`);
  - `apps/api/test/spaces.ts` (helpers if needed: a closure, a price with a shift).
- **Web, `features/directory/`:**
  - `types/` (`DirectoryFilters`, `DirectoryRequest`, `PinsRequest`, `FiltersView`, `SpaceCardView`, `HomeSpacesView`, `DirectoryListView`);
  - `services/` (`filtersOf`, `requestOf`, `priceBounds`, `cardView`, `todayHours` and their unit tests; new `pricePlaceholders.ts` and `sortOrders.ts` with unit tests);
  - `hooks/filters/` (`usePriceFilter`, `useFiltersPanel`, new `usePriceRanges.ts`, tests), `hooks/list/` (`useDirectoryFilters`, `useDirectoryList`, tests), `hooks/home/useHomeSpaces*`, `hooks/map/useDirectoryMap*`, `hooks/queryKeys.ts`, `hooks/page/useSpacePage*`;
  - `repository/directoryRepository.ts` and its unit test;
  - `components/filters/` (`FiltersForm`, `PriceFilter`, new `CheckGroup.tsx`, `FiltersSheet.component.test.tsx`), `components/DirectoryList.tsx`, `components/card/SpaceCard.tsx` and its test, `components/page/StatusPanel.tsx` and `HoursSection.tsx` (and `SpaceDetails.component.test.tsx`), `components/home/HomeSpaces.tsx`, `components/map/*` only where the card or the pin's name changes.
- **Web, elsewhere:**
  - the design system's `SegmentedControl` folder, the layer's `index.ts`, and the showcase's section, `registry.tsx` and `fixtures.json`;
  - `shared/lists/components/ListPagination.tsx`;
  - `pages/site/public/home/HomePage.tsx` and `HomePage.component.test.tsx`;
  - `shared/copy/{arabic,english}/directory.ts`.
- **Docs:**
  - `docs/features/directory.md`, `spaces.md` (the listing's filters, order, price and hidden-price rule; *History*), `occupancy.md` (`publicStatesFor`, the by-hours state, no `availableAmong`), `announcements.md` (who reads the closures), `space-links.md` (only if OD5 b, else one line saying the missing line is the mark);
  - `docs/api/api-contract.md`;
  - `docs/architecture/decisions/0008-…md`;
  - `docs/architecture/data-model.md` (the live status's filter line; derived values: open now by its hours, open in the evening, the by-hours state);
  - `docs/backend/conventions.md` (§8 *Pure rules*, §9 *occupancy*, *Composed reads*);
  - `docs/frontend/design-system/foundation.md` (§3, §12, and §13 lines 449–450);
  - `docs/project/overview.md` (the *Built* line and the v1 public-site line: "available now" becomes "open now, open in the evening"; Home's line);
  - `docs/project/glossary.md` (only if EC14 finds a term);
  - findings 214 (and 215 if OD7 b) and the index;
  - `docs/design/prototype/Directory.html`, `docs/design/CHANGES.md`, `docs/design/INDEX.md` (item 14 only).

**Overlaps with the parallel tasks (recorded, not touched):**
- **Women's spaces and the evening feature.** That task will extend this item's `evening` and add a filter, in the same files:
  - `directory/requests.ts`, `publicListing.repository.ts` and `directory.service.ts`;
  - `FiltersForm` and `useFiltersPanel`;
  - the `directory` catalogues;
  - `directory.md` and `api-contract.md`;
  - `Directory.html`.
  It should start from this PR's head, or after its merge.
- **The visual identity.** Possible contact at the prototype's `shared.jsx` (which this PR does not touch unless OD7 a), the layer's tokens (which `SegmentedControl` reads but never changes) and `foundation.md` (different sections).
- **The owner's space profile.** No shared code file.

## 9. Design issues (built only once the reply approves them)

- **DI-1.** The prototype's segments are 32 px, under the 44 px touch target (§10). They take the control height on touch.
- **DI-2.** The chosen segment differs by its raised shadow, which the dark theme sets to none (`--elevation-raised: none`), so in dark it would differ by fill alone. It carries the card's edge in both themes.
- **DI-3.** The prototype's price count («N مساحات لها سعر شهري في …») and its price "no match" titles are true only when the price is the sole filter. Production's «N مساحة مطابقة» and «لا توجد مساحات تطابق ما اخترت» stay: they are true under any combination (directory.md's design issue 3).
- **DI-4.** Home's «متاحة الآن» would list full spaces under "available".
  - The title becomes «مفتوحة الآن» / "Open now".
  - The empty state becomes «لا توجد مساحات مفتوحة الآن» and «قد تكون المساحات مغلقة في هذا الوقت. تصفّح كل المساحات لمعرفة ساعات عملها.», since full spaces are now listed.
  - «عرض الكل» leads to `?open=1`.
  - The prototype's Home is OD7.
- **DI-5.** The «إلى» error becomes ««إلى» أقل من «من».» (the prototype's wording), which names both fields; «أقل من الحد الأدنى» named neither.
- **DI-6.** The placeholders are whole shekels (the lowest rounded down, the highest rounded up), never a decimal a bound refuses.
- **DI-7.** The hint under «الكل» and the help line under a subscription describe the radiogroup (`aria-describedby`, through the `Field`), so they are read with it.
- **DI-8.** The card's price is the last line of the card and the last of the link's descriptions, after today's hours.
- **DI-9.** About's legend names the live states only. No change is recommended: the neutral by-hours badge says its own words, and the page's line explains it (OD3).
- **DI-10.** The other lists' sheets keep «لا نتائج — غيّر الفلاتر» for none; only the Directory's becomes «لا توجد نتائج» (decision 13). This is a difference left as it is, recorded here.

## 10. The test matrix

Every test is seen failing first (testing §3 rule 5). Its break is named here, and its expectations are written by hand. Lanes: **U** unit · **C** component · **A** API (real PostgreSQL, `masaha_test`, fixed clock via `createTestApp({ clock: () => now })` with `now` set per test, never the real clock).

### Shared schemas (U) — `packages/shared/src/directory/requests.unit.test.ts`

| # | Proves | Break it catches |
|---|---|---|
| T1 | `period` alone is accepted on the list and the map, each of the four; another word is `invalid_choice` | the period made to require a bound |
| T2 | `priceMin` alone, `priceMax` alone and both are accepted with a period; `min = max` passes; `min > max` is `{ priceMax: ['out_of_range'] }` | `>=` for `>`; the error on `priceMin` |
| T3 | each bound without a period, and both, is `{ period: ['required'] }` | the refinement dropped for either bound |
| T4 | `0`, `-100`, `10000001` → `out_of_range`; `12.5`, `abc`, `1e3` → the codes EC5 confirms, on that field | `min(1)` lowered; `int()` dropped |
| T5 | `openNow` and `evening` take `true`/`false` on both schemas; `''` and `maybe` are `invalid_choice` | a filter missing from the map's schema |
| T6 | `availableNow: 'true'` parses to an object with no `availableNow` | the old key kept in `filters` |
| T7 | `priceAsc`/`priceDesc` are accepted with a period, with or without `q`; without a period, `{ sort: ['invalid_choice'] }`; the default order is unchanged | the refinement missing for one direction |
| T8 | the map's schema refuses a bound without a period (kept) and takes no `sort` | — (kept) |

### API (A) — real queries through `GET /spaces` and `GET /map/spaces`

| # | Proves | Break it catches |
|---|---|---|
| T10 | `period=X` alone keeps exactly the spaces with a **general** price of X; it leaves out a student-only X price, another period only, no prices, and a stale unverified space with an X price | `audience` dropped from the predicate; the hidden rule dropped |
| T11 | the bounds are inclusive, each alone and both: `priceMin` = the price passes and price − 1 agora fails; `priceMax` = the price passes and + 1 fails | `>` for `>=`; `<` for `<=` |
| T12 | a space with several general X prices (two shifts, one label) passes when **any** is within the bounds; its card's `priceAgorot` is the lowest **within** the bounds, and without bounds the lowest overall | `max()` for `min()`; the bounds left out of the price column |
| T13 | over HTTP, 422 by field: `min > max`, a bound without a period, `0`, `-1`, `12.5` (one request each, the envelope's `errors`) | the route not using the schema |
| T14 | hidden prices, on stale unverified spaces only (a verified stale and a fresh-at-30-days space as controls): never under `period`, the bounds, `studentPrices` or a price order; their unfiltered card carries no `priceAgorot`; the verified stale space keeps its price | `pricesShown` dropped from the price column or the order |
| T15 | `priceAgorot` is present on every card exactly when `period` is in the query; absent without; absent from the pins, the favourites' cards and `/spaces/:slug` | the key always set; null sent instead of absent |
| T16 | the price order, both directions: by the card's price; equal prices end by id **ascending in both** (with `moveRowToEnd` so a scan order would differ); limit 2, pages 1–3 together give the whole order, no repeat, no gap, the total right | `id DESC` in `priceDesc`; a missing tie-break |
| T17 | `sort=priceAsc` without `period` → 422 `invalid_choice` on `sort`; with `period` and `q`, ordered by price, not by score | the API order ignoring the price |
| T18 | with bounds, the order's key is the in-bounds price (a space whose cheapest X is out of bounds sorts by its in-bounds one) | the order computed apart from the filter |
| T19 | `GET /price-ranges`: each period's lowest and highest general price over the listed spaces whose prices are shown. Left out: a hidden-price space, a hidden one, a deleted one, one in an unlisted area, and student prices. A period with none → `null`. Kept 30 s with an `ETag` | a hidden space's price in the range |
| T20 | `openNow` (fixed clock, an 08:00–18:00 space, unverified): 07:59 fails, 08:00 passes (opening minute), 17:59 passes, 18:00 fails (closing minute) | `<=` at the close; `<` at the open |
| T21 | a day closed (`fri` `null`): Friday 10:00 fails, Thursday 10:00 passes | the closed flag ignored |
| T22 | a space without hours never passes `openNow`, at any clock | a null week read as open |
| T23 | a closure in force excludes. These do not: a closure that ended (`endsAt` = now, and before), one not yet begun (`startsAt` > now), a deleted one, and an `OUTAGE` announcement | `lte` for `lt`; deleted closures counted |
| T24 | under `openNow`: a verified FULL space stays with `liveStatus: 'FULL'`; a verified AVAILABLE and an unverified open space pass; a verified space with an override `CLOSED` in force follows OD2 | the filter reading the live status |
| T25 | the Gaza day boundary (winter, UTC+2): Thursday 2026-11-05 23:30Z is Friday 01:30 in Gaza. A space open only on Friday (0–1440) passes; one open only on Thursday (08:00–24:00) fails. At 21:30Z (Thursday 23:30 in Gaza) the reverse | the UTC weekday or minute used |
| T26 | DST, an 08:00 opening: 2026-10-24 05:30Z (07:30 Gaza, after the change to +02:00) fails, 06:00Z passes; 2026-03-28 05:30Z (08:30 Gaza, +03:00) passes | a fixed offset in place of `gazaClockOf` |
| T27 | a day closing at 24:00 (1440): 23:59 passes; 00:00 of the next day, closed, fails | `closes − 1` handling at midnight |
| T28 | `openNow` is applied before the page is cut: 5 open of 9 at limit 2 gives pages of 2, 2, 1; total 5; every card open | a filter applied after paging |
| T29 | `evening`: closes 20:00 (1200) passes; 19:59 (1199) fails; one evening day among short days passes; around the clock passes; all days closed fails; no hours fails; the same answer at a morning clock | `>` for `>=`; today's day read |
| T30 | `hoursStatus` on the card and the pin, at a fixed clock: unverified open → `OPEN`, closed by hours → `CLOSED`, under a closure → `CLOSED`, no hours → `null`; verified spaces also carry it, and their `liveStatus` is unchanged (`liveStatus.api.test.ts`'s cases kept) | the closure ignored in the state |
| T31 | **binding** the SQL filter to the TypeScript rule, at four clocks (an opening minute, a closing minute, a closure, a day boundary): the ids of `openNow=true` equal the ids whose unfiltered card says `hoursStatus: 'OPEN'`; for verified spaces with no override, `liveStatus === 'CLOSED'` exactly when `hoursStatus === 'CLOSED'` | the two rules drifting (one changed to `<=`) |
| T32 | `?availableNow=true` answers 200 with every listed space (an old client gets the unfiltered list, not a 422) | the old key still read |
| T33 | **leave one out.** Nine spaces, each failing exactly one of `area`, `period`+bounds, `openNow`, `evening`, `openFriday`, `verified`, `studentPrices` and `q`, plus one passing all. All the filters together give exactly that one. Dropping each filter in turn adds exactly the space it excluded. A space without hours fails only the hours filters. The totals agree | any filter OR-ed, ignored, or applied to another column |
| T34 | `/map/spaces` with `openNow` and with `evening` keeps the same spaces as the list (ids compared); each pin carries `hoursStatus` | the map's filter not wired |
| T35 | (OD3 a) `/spaces/:slug/occupancy` answers `{ status, hoursStatus }` | the field missing on the page's read |
| T36 | the favourites' listed cards carry `hoursStatus` | — (wiring) |
| T38 | 18 a page with a filter: 37 matching spaces at `limit=18` give pages of 18, 18, 1; `totalPages` 3; no repeat | — (the API already allows it; this proves the web's ask) |
| T39 | the card's keys (`liveStatus.api.test.ts`): `hoursStatus` added; `priceAgorot` only with a period; still no capacity, count or override | a count leaking into the card |

### API unit (U) — `apps/api/src/modules/occupancy/liveStatus.unit.test.ts`

| # | Proves | Break |
|---|---|---|
| T37 | `hoursStatusOf`: no week → `null` even under a closure; a closure → `CLOSED`; the opening minute → `OPEN`; the closing minute → `CLOSED`; a closed day → `CLOSED` | the closure checked before the week |

### Web unit (U)

| # | Proves | Break |
|---|---|---|
| T40 | `filtersOf` and `paramsOf` round trip: `period` alone; `min` and `max` read only with a period; `open=1`, `evening=1`; a price order read only with a period; `available=1` and `availableNow=true` read as nothing; an old `?period=DAY&min=10` still reads; no default is written | a price order kept without a period |
| T41 | `requestOf`: `limit: 18`; `period` sent alone; shekels × 100; `openNow` and `evening` sent as `true` only when set; `sort` passed; never `availableNow` | 20 left |
| T42 | `priceBounds`: «٢٥٠» → 250; `0`, `12.5`, `abc` → `invalid`; 100,001 → `tooHigh`; `max < min` → `belowMin` on max, max left out | Arabic-Indic digits not read |
| T44 | `pricePlaceholders`: 1250 and 9950 agorot → «12» and «100»; `null` → none | rounding the wrong way |
| T45 | `cardViewOf`: an unverified space with `hoursStatus` `OPEN`/`CLOSED` gets a `neutral` «مفتوحة الآن»/«مغلقة الآن»; `null` gets `noStatus`; a verified space keeps its live view; `price` is «‏15 ₪ / يوم» isolated, only with a period and a `priceAgorot` | the success colour on a by-hours badge |
| T46 | `todayHours(null)` says «ساعات العمل غير متوفرة»; Gaza's day is kept (the existing test) | null drawn as nothing |
| T47 | `sortOrders({ searching, period })`: no price items without a period; both, worded by the period, with one | items disabled instead of absent |

### Web component (C)

| # | Proves | Break |
|---|---|---|
| T50 | `SegmentedControl`: a radiogroup named by its `Field`, its segments radios with `aria-checked`; a click chooses; in RTL ArrowLeft goes next and ArrowRight back, the reverse in LTR, each choosing; it loops at the ends; Home/End choose the first and the last; one tab stop (Tab enters on the checked segment, the next Tab leaves); axe-clean in both directions | Home/End left to Radix (focus without a check); two tab stops |
| T51 | the panel's order: the groups «المنطقة», «السعر», «الدوام», «أخرى» in that order; «الدوام»'s three checkboxes and «أخرى»'s two in order; no «المساحات» and no switch | a group misplaced |
| T52 | the price: «الكل» is checked and shows no range; «شهر» sends `period=MONTH` at once, with no bounds; the range appears with placeholders from the ranges; «٢٥٠» sends `priceMin=25000` after the pause; «0» and «12.5» are said on their field and not sent; «إلى» under «من» is said on «إلى» and «إلى» not sent; «الكل» clears the period and both texts | a bound sent while invalid |
| T53 | the sort: no price item under «الكل»; «الأرخص شهريًا» and «الأغلى شهريًا» after «شهر»; choosing one sends `sort=priceAsc` with the period; «الكل» then returns the order to «الأحدث تحديثًا» and drops `sort` (with a search, to «الأفضل تطابقًا») | the order kept without its period |
| T54 | «مسح» clears the place, the subscription, both bounds and their texts, and the five boxes; it keeps the search and a «حسب الاسم» order; a price order goes to the default | the order cleared; texts left |
| T55 | the active count: each box adds 1; the place adds 1 for several areas; the subscription adds 1 with or without its range; everything on gives 7 | the range counted apart |
| T56 | the address round trip: a render at an address shows its state; a change replaces the address; a new router at that address (a reload) shows the same; Back (a memory history of two) shows the earlier state; `?available=1` opens unfiltered, with no such control | a key not read back |
| T57 | the list asks `limit=18`; page 2 asks `page=2&limit=18`; the pages and the count come from the answer's `meta` | — |
| T58 | the card: the price line shows while a subscription is chosen and not under «الكل»; an unverified card's by-hours badge is the neutral variant; «لا تتوفر حالة مباشرة» without hours; «ساعات العمل غير متوفرة» on the card; the link's description includes the price | a by-hours badge in the live status's tone |
| T59 | the page: «ساعات العمل غير متوفرة» in the hours section and the status card; (OD3 a) an unverified page's by-hours badge with «حسب ساعات العمل؛ …» | the old «لم تُضف…» kept |
| T60 | the sheet's button: 0 «لا توجد نتائج», 1 «عرض نتيجة واحدة», 2 «عرض نتيجتين», 3 and 10 «عرض N نتائج», 11 and 100 «عرض N نتيجة»; English 1 and N | a plural form wrong |
| T61 | Home asks `openNow=true&limit=6`, is titled «مفتوحة الآن», and «عرض الكل» leads to `/spaces?open=1`; the empty words | Home still asking `availableNow` |
| T65 | the admin row of a space whose hours group is missing says «ناقصة: … ساعات العمل» (OD5 a), or the new badge (OD5 b) | — |
| T66 | the map: the sheet holds the new groups; the pins' request carries `openNow` and `evening`; an unverified chosen space's card shows its by-hours state; a pin's name uses it | — |
| T80 | finding 214: the pick opens `/spaces?view=map`, the Directory's h1 «Workspaces» is shown, exactly one «Search for a space», and no «Nearest to me» | made to fail once by sending the pick to `/spaces` (the list) |
| T81 | `ListPagination`'s existing tests, unchanged, pass | — (a pure rename) |

**Finding 214's proof.** After the fix: the full component lane (`npm run test:component`, not the file alone) runs green **three times in a row** locally, then once in CI on the pushed head. The report gives the three counts, and says if a lane was killed for memory (retried once, then CI judges).

## 11. Review Focus — the inputs no planned test exercises

- **A Gaza DST date set by a future decree.** The zone data may lag; this is a known risk in conventions §11, pinned by the shared DST test.
- **An answer kept 30 s across an opening minute.** A card or the `openNow` list can lag by up to 30 s, as the live status already does.
- **A wrong device clock** reads today's hours on the wrong day (web).
- **Hours rows fewer than 7.** The API always writes 7; only raw SQL could leave fewer.
- **Very many closures in force at once:** one id list in one parameter.
- **A price ceiling at 10,000,000 agorot in the placeholders** (₪100,000).
- **The DST hour that repeats** (01:00–02:00 on 2026-10-24) for a space open around 01:00.
- **The visual layout:** the 4/12 column, and the segments fitting at 1024 px in Arabic. Manual lane only.

## 12. Executor checks (EC)

- **EC1.** Confirm in `node_modules/@radix-ui/react-radio-group` that only arrow keys check (already read: `ARROW_KEYS`, v1.4.7), and see T50 fail with Radix alone before adding the Home/End handler.
- **EC2.** Confirm the utilities used (`bg-muted`, `bg-card`, `shadow-raised`, `border-(--card-border)`, `data-checked:`, `pointer-coarse:`) exist, and that `muted-foreground`/`muted` and `foreground`/`card` are §5's verified pairs; then run `check:classes`.
- **EC3.** `liveStatusFor` and `availableAmong` have no reader outside `directory` (grep: none); rename and delete.
- **EC4.** `directoryQuerySchema` strips an unknown `availableNow` (zod's default `strip` through `.extend`), not refuses it. T6 and T32 prove it.
- **EC5.** The exact field codes `toFieldErrors` gives for `-100`, `abc`, `12.5`, `1e3`. Write them in T4 by hand once seen; never compute them in the test.
- **EC6.** Finding 214: re-read both CI attempts' lines, then make the break (T80). Optionally reproduce the old test's detached-element failure locally under a full lane. Then three full component runs.
- **EC7.** The English h1 is `directory.title` = "Workspaces", and Home has no heading of that name.
- **EC8.** One closure predicate: `closedAt` and `closedSpaceIdsAt` share one `where` builder (and T23 runs against the filter).
- **EC9.** `useDirectoryList`'s and `useDirectoryFilters`' tests that assume 20 a page or `period=DAY` by default are updated, not bent: each expectation is re-derived from the new rule.
- **EC10.** The next PR number (expected #138) is checked just before the push; `#PRNUM` is replaced in every commit's tree, with none left.
- **EC11.** After the docs: `git grep -n -i "availableNow\|available now\|متاحة الآن\|available-now"` in `docs/` and `apps/`. Each remaining match is history or true.
- **EC12.** Overnight ranges are **forbidden**, so no overnight test is needed. They are refused in four places:
  - `data-model.md` › Conventions ("v1 does not support … closing after midnight");
  - `spaces.md` decision F4;
  - `updateSpaceHoursSchema`'s `closesAfterOpening` (`packages/shared/src/spaces/requests.ts`), proven by `requests.unit.test.ts`;
  - the CHECK `space_hours_range_check` (`opens < closes ≤ 1440`, the init migration), proven by `apps/api/src/db/schema.api.test.ts:110–117`.
  T27 covers a range that closes at midnight.
- **EC13.** `CROSS JOIN LATERAL` inside `listed()` works in `findPage`, `findFirst` and the count; `price` is selectable and orderable in the outer query.
- **EC14.** `glossary.md` has no "available now" term (its *Live status* row stays true); add «مفتوحة الآن» only if the glossary lists the filters.
- **EC15.** `HomeSpacesView.viewAll.to` changes from `'available'` to `'open'`, and `HomePage.tsx`'s link to `?open=1`.
- **EC16.** The favourites' contract tests (`favorites.api.test.ts`) still match the card's keys.
- **EC17.** `check:build`: the price-ranges hook and `SegmentedControl` add no heavy library to the site's first download.
- **EC18.** At the push, a parallel PR may have taken 215 (if OD7 b) — check the numbers first.
- **EC19.** `INDEX.md`: add a line only where it describes the Directory's paging; otherwise say so in the report.
- **EC20.** `masaha_dev` is read only: GET requests for the real run; never `db:seed` it.

## 13. Risks

- **R1.** The SQL and TypeScript open-now rules drift. T31 binds them, and `data-model.md` names the one rule.
- **R2.** A parallel worker (women's spaces and evening) edits the same filter files. §8 records it; the early conflict check (`git merge-tree`) runs at the report.
- **R3.** The size, about 90 files and above 25. Per workflow phase 7, a separate review conversation is called for; the owner decides.
- **R4.** A memory-killed lane: retry once, then CI judges, said in the report.
- **R5.** A DST zone data change in Node would fail T26 and the shared test together, which is intended.
- **R6.** Removing `availableNow` breaks a stale browser tab that still sends it. It now gets the unfiltered list, not a 422 (T32).

## 14. Commits (Conventional, atomic, 5)

1. `fix(web): wait for the directory's own search` — items 1–2: `HomePage.component.test.tsx` (the wait and `warm`), `ListPagination.tsx`'s nits, finding 214 and its index line.
2. `feat(design-system): add the segmented control` — `SegmentedControl` with its test, the layer's export, the showcase section, and `foundation.md` §3 and §12.
3. `feat(directory): filter by the hours` — items 7–12 apart from the price:
   - shared `openNow`, `evening` and `HoursStatus`;
   - the API's open-now and evening filters, `hoursStatusOf`, `publicStatesFor`, `closedSpaceIdsAt`, the directory's clock, and `availableNow` removed (with OD2 and OD3);
   - the web's «الدوام»/«أخرى» `CheckGroup`, the new keys, Home on `openNow`, the by-hours badge, «ساعات العمل غير متوفرة», and the admin line (OD5);
   - the docs: ADR 0008, `data-model.md`, `occupancy.md`, `announcements.md`, `conventions.md`, `overview.md`, `api-contract.md` (filters, card, pin, occupancy) and `directory.md`'s hours parts.
4. `feat(directory): price by subscription and order` — items 3–6:
   - shared sorts and `priceAgorot`;
   - the API's lateral price, the price orders, and `GET /price-ranges`;
   - the web's subscription on `SegmentedControl`, the range with its placeholders, the sort's price items, the card's price, and the active count's subscription;
   - the docs: `api-contract.md` and `directory.md`'s price parts, `spaces.md`, and `foundation.md` §13.
5. `feat(directory): page by 18 and fit the panel` — items 13–14: the 4/12 column, the sheet's plurals, `DIRECTORY_PAGE_SIZE = 18`, the prototype's `Directory.html` paging, the `CHANGES.md` R9 row and its `INDEX.md` line, and `directory.md`'s History (both layers).

Each commit passes lint and typecheck on its own. Its tests go in the same commit as its code, and its documents too. Staging is by path (`git status` before each commit), with no tool attribution. Review fixes later fold in with fixup and autosquash, after a `backup/*` branch.

## 15. Verification (phase 4)

- **V1.** `npm run lint` · `typecheck` · `format:check` · `check:classes` · `check:links` · `check:conflicts`.
- **V2.** `NODE_ENV=production npm run build`, then `check:build` (apps/web/.env sets development).
- **V3.** `test:unit` and `test:api` in full, `masaha_test` with the DB up. At most two lanes at once with 8–10 GB free; a third waits.
- **V4.** `test:component` in full, **three times** (finding 214), one at a time.
- **V5.** A real API run against `masaha_dev`, GET only: `/spaces` with each new filter, both price orders, `?availableNow=true`, `/price-ranges` and `/map/spaces?openNow=true`.
- **V6.** The browser (Chrome, the dev server):
  - RTL and LTR, light and dark, at 390, 1100, 1300 and 1440 px;
  - the panel, the segments by keyboard, the range, the sort, the card's price and badge, Home, a space without hours, and the sheet's count.
  - Screenshots are curated into `Downloads\wi138-shots`, never pushed.
- **V7.** By hand (the manual lane): the 4/12 column at 1100 px and 3/12 at 1300 px; the five segments fitting at 1024 px in Arabic and English.
- **V8.** The servers are stopped by PID and their ports checked free (3320, 5320).
- **V9.** Push, PR (with the template, assignee and labels: `feat`, `area:web`, `area:api`, `area:design-system`, `area:docs`), CI green on the head, `CLEAN`, then `final-report`.

Not run: E2E (the end of the project, as the PR states).

## 16. Decisions needed from the owner (OD)

- **OD1 — the range's placeholders need data the web lacks.**
  - **(a)** A new public `GET /price-ranges`: each period's lowest and highest general price over the listed spaces whose prices are shown, kept 30 s. **Recommended.**
  - (b) No placeholders: decision 4 is left in part.
  - (c) Carry the range in the list's `meta`: this breaks api-contract §4's `meta` shape.
- **OD2 — a verified space set «مغلق» by hand (an override in force) under «مفتوحة الآن».**
  - **(a)** It leaves the list, so the card the filter kept never says «مغلق الآن». **Recommended.**
  - (b) It stays, as decision 7 is worded.
- **OD3 — the space page's state for an unverified space with hours (the prototype's `StatusLine`).**
  - **(a)** `GET /spaces/:slug/occupancy` adds `hoursStatus`; the page's status card shows the neutral badge with «حسب ساعات العمل؛ الحالة المباشرة تظهر للمساحات الموثّقة فقط». **Recommended:** the card and the page agree.
  - (b) Cards only: decision 9's letter.
- **OD4 — which price a card shows when a space has several general prices for the period.**
  - **(a)** The lowest within the range (the lowest overall without a range); the same value filters and orders. **Recommended.**
  - (b) The lowest overall, even outside the range.
  - (c) (a) with «من» before it when the space has more than one.
- **OD5 — the admin list's «بدون ساعات».**
  - **(a)** No new badge: «ناقصة: ساعات العمل» already marks exactly those spaces; proven by T65, and `space-links.md` says it. **Recommended.**
  - (b) Add a separate badge «بدون ساعات» beside it.
- **OD6 — the place in the active count.**
  - **(a)** Once, whatever the number of areas, as built (directory.md's design issue 14). **Recommended.**
  - (b) Each area once (the prototype's R6).
- **OD7 — the prototype's two other disagreements.** `Home.html` still lists `verified && open` and links `?available=1`; `shared.jsx`'s `TodayHours` reads the browser's day.
  - (a) Fix both in this PR, beyond item 14's licence. `shared.jsx` may also be the visual-identity worker's.
  - **(b)** Record finding 215 and leave them to the design owner. **Recommended,** to avoid that overlap.
