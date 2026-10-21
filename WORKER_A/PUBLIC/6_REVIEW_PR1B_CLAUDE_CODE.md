# Review — PUBLIC PR 1b (#103, `feat/directory-filters`)

**Head:** `52b7a2b04739eb90ae9e7d49c583d3b28c5108f4` (unchanged at the end of the review) · base `origin/main`
`befd96f9` (#101's merge, also the merge base) · `gh pr checks 103`: all ten green on this head (build,
check:classes, check:links, format:check, lint, test:api, test:component 15m31s, test:unit, typecheck; CodeRabbit).
I confirmed the run's `headSha` is this head · `mergeStateStatus: CLEAN`.

**Verdict: mergeable — no blocker.** The position's privacy holds in the code. Four findings are should-fix,
all small. Under the owner's rule they go into **PUBLIC PR 2's first commit**, through `0_CARRIED_FROM_103.md`.
The owner may prefer a fix round for 1 and 2, since both touch what near me tells the visitor. The rest are
nits or findings to record.

**What I saw and what I only read.** I read the code, the tests, the documents and the commit messages
through commit objects only. I ran no test, build or server. Two things I looked at myself:
- the screenshot `1b-near-stopped-ar-light-390.png`;
- the network log `1b-near-granted-ar-light-390-log.txt`: one request carries `Masaha-Near`, it is on
  `sort=distance`, and the value is `31.502,34.467`.

These come **from the executor's report only**:
- every break being red, and every red step;
- the local lane counts;
- the first download's sizes;
- the other screenshots and widths;
- the claim that the real run left `masaha_dev` unchanged.

---

## The five most important findings

### 1. Near me drops the keyboard focus and announces nothing — should-fix
- **Where:**
  - `components/near/LocationStatus.tsx:26` (the stop button is drawn only while `view.stop !== null`), `:31`
    (clear), `:14` (the only live region);
  - `components/near/NearMeButton.tsx:11` (`loading`);
  - the design system's `Button` sets `disabled={… || loading}`.
- **Scenario (seen in the code):**
  - A keyboard or screen-reader visitor presses «إيقاف الترتيب حسب المسافة». `sorting` turns false, so
    `stop` becomes `null` and the focused button is unmounted.
  - «مسح موقعي» does the same: the state goes to `idle` and `LocationStatus` returns `null`.
  - In both cases the focus falls to `body`. The visitor is back at the top of the document, far from the
    list.
  - Pressing «الأقرب إليّ» sets `loading`, which disables the focused button. Chrome's focus fix-up then
    moves the focus to `body` (browser behaviour; I did not run it).
  - When the answer comes, the `role="status"` paragraph is replaced:
    - when the location is granted, by a plain `<p>` with no live role, so «مرتبة حسب المسافة من موقعك…» is
      never announced;
    - when it is refused, by a newly inserted warning `Alert` (`role="status"`). A live region inserted
      already filled is often not announced (plausible, not tried with a screen reader).
  - On a weak phone with a screen reader, the visitor presses the button, hears nothing, and loses their
    place.
- **Fix:**
  - Keep one always-mounted `role="status"` wrapper around `LocationStatus`, whose content changes.
  - After stop or clear, move the focus to «الأقرب إليّ».
  - Optionally, use `aria-busy` without `disabled` while locating.
  - Test: press stop, then clear, by keyboard, and each time assert the focus is on «الأقرب إليّ».
- **Where the fix belongs:** small → **PUBLIC PR 2's first commit**.

### 2. A dismissed permission prompt can leave near me "locating" for good — should-fix, plausible
- **Where:** `hooks/near/useNearMe.ts:29` (a press while `locating` returns) and `:45` (`getCurrentPosition`
  with `timeout: 8000`).
- **Scenario:**
  - **Seen in the code:**
    - The only ways out of `locating` are the two callbacks.
    - The button is disabled while locating, and `press` ignores it anyway.
    - The store is module-level, so the state lasts until a reload.
    - Meanwhile the line reads «جارٍ تحديد موقعك… يُرسَل موقعك مقرَّبًا…», which tells the visitor a
      location is being sent.
  - **Not observed:**
    - In Firefox, closing the permission panel without choosing calls neither callback. The geolocation
      `timeout` only counts once the permission is granted, so it never fires.
    - The visitor is then stuck with a spinning, disabled button and a privacy line that is not true.
    - This is the known Firefox behaviour; I did not run it.
- **Fix:**
  - Add a watchdog in `useNearMe`: no answer within about 15 s → `refused('denied')`.
  - Ignore a late callback after that.
  - Or let a press while locating cancel it.
  - Test with `fakeGeolocation` and the fake clock: no callback, advance the clock, and the state is
    `denied` with «اختر منطقتك».
- **Where the fix belongs:** small → **PUBLIC PR 2's first commit**.

### 3. «مسح الفلاتر» does two different things, and `directory.md` states only one — should-fix
- **Where:**
  - `hooks/list/useDirectoryList.ts:184`: no match's «مسح الفلاتر» runs `filters.clearAll`, which also clears
    the search and the order.
  - The sheet's «مسح الفلاتر» and the sidebar's «مسح» run `clearFilters`, which keeps them
    (`useFiltersPanel.ts`, via `useDirectoryList`'s `clear: filters.clearFilters`).
  - `docs/features/directory.md:53`: «Clearing the filters keeps the search and the order.»
- **Scenario (seen in the code):**
  - A visitor searches «Hub» and turns on «متاحة الآن فقط», and nothing matches.
  - «مسح الفلاتر» in the sheet keeps «Hub».
  - The button with the same label in the no-match state erases «Hub» and the chosen order too.
  - One label carries two meanings, which is design issue 6's principle broken in another place. The
    document's sentence is false for the no-match button.
- **Fix (the owner's call on behaviour):**
  - Either no match runs `clearFilters` when a filter is in force, and `clearAll` only when the search alone
    narrows the list;
  - or the document says what each button does.
  - Either way, add a test of the no-match button with a search and a filter together.
- **Where the fix belongs:** small → **PUBLIC PR 2's first commit**.

### 4. Two privacy guards have no break of their own, and one has no test — should-fix (the owner's §3 rule)
- **Where:**
  - `hooks/list/useDirectoryList.ts:37`: `const point = near.state.sorting ? near.state.point : null`, the gate
    that keeps the header off every request but those that order by distance;
  - `hooks/near/useLocationStatus.ts`: `privacy: sorting ? words.privacy : null`, for the granted state that is
    not sorting.
- **Scenario (seen in the tests):**
  - Test 41 was written after its code. Its recorded break is "sort=distance left out", which proves the
    request's order, not this gate. No break removes the gate.
    - Test 41's later assertions (`button.on` false, no header on the last request) would probably fail if
      the gate were removed. That is my reading; no red run of it is recorded.
  - The "stopped" state (point kept, nothing sent) has **no component test** at all. Test 42 goes from
    granted straight to «مسح موقعي». Test 40 checks the store only.
    - So a regression showing «يُرسَل موقعك مقرَّبًا…» while nothing is sent (design issue 5) would stay
      green.
    - The real run shows it correctly: «مسح موقعي» alone in `1b-near-stopped-ar-light-390.png`, which I
      viewed.
- **Fix:**
  - Add a stop step to test 42: press «إيقاف الترتيب حسب المسافة», then assert there is no privacy line and
    the button is not pressed.
  - Break the gate once (`const point = near.state.point`), see test 41 red, and record it.
- **Where the fix belongs:** small → **PUBLIC PR 2's first commit**.

### 5. Cards keep «على بعد … كم» after the distance order stops, until the next answer — nit, plausible
- **Where:** `hooks/list/useDirectoryList.ts:123` (cards from `answer`, which may be the placeholder) with
  `useDirectoryQuery`'s `keepPreviousData`.
- **Scenario:**
  - **Seen in the code:**
    - Stopping or clearing switches the key to one without a point.
    - If that key is not cached (the visitor changed a filter or the page while sorting), the shown answer is
      the distance-ordered placeholder.
    - So every card still says «على بعد 0.7 كم», while the button is off and the state line is empty or
      gone.
    - The point itself is not kept: only the answer's `distanceMeters` are.
  - **Not observed:** how long it lasts. On a weak connection, seconds.
- **Fix:** word the distance only while the shown answer was asked by distance. For example, `cardViewOf` drops
  `distance` when `point === null`; or the hook keeps the previous data only between keys of the same kind.
- **Where the fix belongs:** **PUBLIC PR 2's first commit**, with finding 1.

---

## The rest

### 6. The price filter's own state survives «مسح الفلاتر» — nit
- **Where:**
  - `hooks/filters/usePriceFilter.ts:42`: `texts` is reset only when the address's `min`/`max` change;
  - `:79`: `chosen` is reset only when the address's `period` changes.
- **Scenario (seen in the code):**
  - Type «abc» in «إلى». The address loses `max`, and the field keeps «abc» with its red line. Then
    «مسح الفلاتر» (or «مسح»): `min`/`max` were already absent, so nothing resets. «abc» and «اكتب مبلغًا
    بالشيكل أكبر من صفر» stay after clearing.
  - The same happens to a period chosen with no bound: «شهر» stays pressed, and the help line keeps naming
    the month. In both cases the clear action is disabled when nothing else applies, so the visitor cannot
    reset them.
  - Typing a bound and pressing «مسح» within the 400 ms pause brings the bound back when the pause ends.
- **Fix:** give the price hook a reset that the two clear actions call (texts to the address's, `chosen` to the
  default), and cancel the pending pause.
- **Where:** **PUBLIC PR 2's first commit**.

### 7. The sheet reopens by itself after a width change — nit
- **Where:** `hooks/filters/useFiltersPanel.ts:33` (`open` outlives `wide`).
- **Scenario (seen in the code):** a visitor opens the sheet at 768 px and turns a tablet to landscape
  (≥ 1024 px). The sheet unmounts and the sidebar shows, but `open` stays `true`. Turning back below 1024 px
  opens the sheet unasked, with its focus trap.
- **Fix:** set `open` to false when `wide` turns true.
- **Where:** **PUBLIC PR 2's first commit**.

### 8. Returning to the site by Back leaves the focus nowhere — nit, plausible
- **Where:** `pages/site/shell/useMainFocus.ts:15`. A `Pop` arrival is treated as a load.
- **Scenario:**
  - From `/spaces`, a visitor opens «تسجيل الدخول» (the focus shell) and presses the browser's Back. That is
    a `Pop`, which mounts a fresh `SiteLayout`, so `placed` is the path and no focus moves. The form that
    held the focus is gone.
  - The opposite also happens: a first load that a guard redirects with `replace` before the site shell
    mounts (such as `/login` loaded while signed in) moves the focus on what is, for the visitor, a first
    load.
  - Commit `b82d213b`'s body names a pop as "the first load, a reload" only.
- **Fix:** record it with finding 130's focus-shell line (the owner decided "a first load or a reload does
  not"), or tell a load from Back with the history index.
- **Where:** **a finding to record** (a line in 130).

### 9. Finding 130's *Resolves when* names only the dashboard — nit
- **Where:** `docs/architecture/findings/130-the-dashboards-shells-have-no-skip-link.md:9`. The new dated line
  adds the focus shell (`FocusLayout`), but *Resolves when* still reads "a dashboard item adds … to
  `DashboardLayout`". A dashboard item could close the finding while the focus shell still lacks both.
- **Fix:** add `FocusLayout` to *Resolves when*.
- **Where:** **PUBLIC PR 2's first commit** (one line).

### 10. The place filter has no cap of 50 — finding to record
- **Where:** `useFiltersPanel.ts:42` (`apply({ areas: ids })`) with `filtersOf`'s all-or-nothing `area` (more than
  `DIRECTORY_AREAS_MAX = 50` falls back to none).
- **Scenario:** if the catalogue grows past 50 areas, choosing the 51st writes 51 ids. The address is then read
  as no area at all, and the whole place filter clears silently. Today's seed (`apps/api/src/db/seed/lookups.ts`)
  holds well under 50 areas, so it cannot happen yet. This is plan §11's Review Focus case.
- **Where:** **record a finding** (or cap the choice in `AreaFilter` when the catalogue grows).

### 11. A doc comment left unwrapped — nit
- `components/DirectoryList.tsx:16` is about 135 characters, a sentence inserted without re-wrapping. Prettier
  does not wrap comments.
- **Where:** **PUBLIC PR 2's first commit**.

---

## The executor's departures, judged
- **DEMO_SEED waived:** the owner's decision. The report's inventory (read only) lists every case the run
  needed.
- **Tests 32–35, 41–43 and design issue 14's count written after their code:** allowed under §3 only with a
  break each. A break is recorded for each (from the report only). Exception: the gates in finding 4.
- **Guards the red step did not prove:**
  - own breaks are recorded for:
    - privacy: rounding, the accuracy check, the point in the query, ask on mount, the point in
      `localStorage`, the raw point kept on imprecise, `removeQueries` left out;
    - a bound: accept 0;
    - widths: both drawn, the sheet opened at every width, and the real run's sidebar grid;
    - the distance format: `toFixed`.
  - Missing: the header's sorting gate and the stopped-state privacy line (finding 4).
- **`useFiltersPanel` returning the whole view:** fine. One hook, called once by `useDirectoryList`, with no
  duplicate state. Its local `open` causes finding 7.
- **«₪» as a catalogue word:** right. No text is hard-coded, and both catalogues have it.
- **A period kept in the hook before any bound, and one 400 ms pause for both bounds:** follows S5 (a period is
  written only with a bound). The pause is right: a minimum changed under a typed maximum is applied with it.
  The local state's reset is finding 6.
- **No `distances.*` words:** **the plan's line is wrong for the list, and the departure is right.**
  - `packages/shared/src/directory/requests.ts:132` refuses `near` without `sort=distance`, so a card can carry
    a distance only while sorted. «المسافات من موقعك.» in the stopped state would be false.
  - Nothing true is left unsaid by the list: no card shows a distance once stopped. The exception is
    finding 5's placeholder.
  - The stopped state shows a bare «مسح موقعي» with no line saying a point is kept (seen in the screenshot).
    It is understandable; a short line is the owner's option, not a defect.
  - The words fit PR 3's client-side distance, if anywhere.
- **«الأقرب إليّ» returning to page 1:** right as a change of order. It uses `replacePage`, so the focus is not
  moved (item 1's rule). Small cost: a press that ends denied has already left page 3.
- **Item 11's zero form:** acceptable. `ArabicPlural` needs six forms, and `count` returns `''` before calling
  it for none (`useDirectoryList`), so the form is never drawn.
- **The shared `src/test/fakeGeolocation.ts`:** fine. A test helper beside the others, stubbing the platform's
  seam (`navigator.geolocation`), used by three files. No production code exists only for tests.
- **The button's alignment fix folded into commit 6:** right under the fold rule (`items-end`).
- **The areas' comma as `%2C`:** cosmetic. `URLSearchParams` writes it, a pasted `2,3` reads the same, and a
  shared link works. No change needed.
- **Carried items 2 and 5 not shown in the browser:** acceptable. The first needs 1,200 guest requests; the
  second would write a refresh token. Each has a component test.

## The carried items (`0_CARRIED_FROM_101.md`), each seen in the code
1. **Done** in `50fe2c75`. `DirectoryResults` moves the focus only on a `Push`. The tests type on page 2 and
   paste `?page=5` (the focus ends on `body`).
   - The rule also holds for the filters (`apply` replaces) and near me (`replacePage(1)`), by code.
   - There is no test of those two specifically. The mechanism is the same as the search's.
2. **Done** in `3c837b30`. Once the count has ended, the line is `errors.rate_limit` and the retry is offered.
   The test uses `Retry-After: 1`, advances the clock, sees the retry, and asks again.
3. **Done** in `21de283d`. `filtersOf` drops `max < min`, and test 10 gains `min=50&max=10` and `10&10`.
   `priceBounds` applies the same rule in the fields.
4. **Checked, true.** `lookups.md:18` and `:104` hold now that `DirectoryPage` sets `AreaFilter` in
   `placeFilter`.
5. **Done** in `b82d213b`. The test signs in from the focus shell and the site's `main` takes the focus.
   Finding 130 gained its line. Gaps: findings 8 and 9.
6. **Done** in `dafc816c`. A 100 % rename to `shared/lists`, exported from the barrel; the two `space-links`
   importers and `useDirectoryList` read it there; the inline copy is gone.
7. **Done** in `52e31433`. `aria-describedby` points at one id per detail; test 27 asserts «الرمال · غزة متاح
   موثّقة». The distance joins the list in commit 7.
8. **Done** in `50fe2c75`. The count is set from a non-placeholder answer only; tested with a held answer.
9. **Recorded** as finding 132 (`2fe598c5`). Its claim holds: the owners list is the users list with a fixed
   role (`useOwnersList`).
10. **Done** in `3c837b30`. `refreshFailure` has its test (its break from the report only).
11. **Done** in `ec0f4709`. A total of 0 gives `''`, and both zero lines left the Arabic catalogue.

## Checked and fine
- **The position's privacy:**
  - It is asked only in `press`.
  - `judgePosition` gets `coords` and returns only the rounded point or `imprecise`. The raw position goes no
    further.
  - `Math.round(x·10³)/10³` with `String()` gives at most three decimals, as the shared header regex demands.
  - The point lives in a module-level Zustand store with no `persist`.
  - It goes into the header only through `repository.list(request, near)`, and only while `sorting`, always
    with `requestOf(…, { byDistance: true })`.
  - It is never in `params`, `paramsOf`, the page links or `sort`. `filtersOf` drops `sort=distance`, so a
    pasted link cannot ask for distance without the header.
  - «مسح موقعي» clears the store and removes every list key holding a point (`hasNear`).
  - Nothing in `apps/web` logs a query key, an `AppError` carries no request config, and no query persister
    exists.
  - The privacy line shows in `locating` and in granted-while-sorting only. Denied, unavailable or timeout,
    imprecise and out of the Strip each say their own line.
- **The filters:**
  - Each lives in the address: `area`, `period` only with a bound, `min`/`max` whole shekels 1–100,000,
    `available`, `verified`, `students`, `friday`.
  - Every write replaces the address and returns to page 1; `clearFilters` keeps `q` and `sort`.
  - Invalid text never reaches the address. An inverted budget shows «أقل من الحد الأدنى» and drops the
    maximum, so there is no 422.
  - The period's single `ToggleGroup` ignores an empty value.
  - The badge counts the six filters in force, not values.
  - The place filter goes through the page's `placeFilter` slot, and `features/directory` imports no other
    feature.
- **The sheet and the sidebar:**
  - They are drawn once per width through `useMediaQuery('(min-width: 1024px)')`. `FILTERS_FORM_ID` is
    therefore unique.
  - The trigger is `SheetTrigger asChild` (`aria-expanded`). The badge is `aria-hidden`, and its words are
    read in its place («الفلاتر 3 فلاتر مطبّقة»).
  - The sheet is a dialog named «الفلاتر». Its primary button closes it and counts the spaces in Arabic
    agreement, says «لا نتائج — غيّر الفلاتر» for none, and says «عرض النتائج» while the count is unknown.
  - The close button comes after the body, so the place filter takes the focus on opening. Radix returns the
    focus to the trigger on closing (by code; not asserted by a test).
  - The sidebar is an `aside` named «الفلاتر», with an `h2` and «مسح». «اختر منطقتك» focuses the place filter
    at 1440 px and opens the sheet at 390 px (tested).
- **Design system, copy and accessibility:**
  - Semantic tokens and layout classes only, with logical properties and nothing outside the layer.
  - `useMediaQuery` is exported in one barrel line, and foundation §3's tree and *Width* rule are true. Its
    px query matches the layer's own `Sidebar` and `DataTable`.
  - Every new string is in both catalogues, and the Arabic `satisfies Catalogue['directory']`.
  - `applied` and `show` have all six Arabic forms.
  - Decision 8's privacy line and design issues 4, 9, 11 and 12 match §9 word for word.
  - The switches are named by their `Field`, and the two groups are named «المساحات» and «السعر».
- **The documents:**
  - `directory.md`: the header, what it does, how it composes, the filters, near me, the eleven new
    web decisions, the code map and the history. Exception: finding 3's sentence.
  - `architecture.md`: §1 `lists`, §2 the shell, §3 *Where state lives*.
  - foundation §3; `overview.md`'s Directory line; finding 132 and its index line.
  - All true to the code and saying only what #103 built. `docs/README.md` needed no change.
- **Scope and commits:**
  - `apps/web` and `docs` only; no API or `packages/shared` change.
  - Ten atomic commits, the carried ones first. Subjects are 36–49 characters, and each body says why.
  - No `#PRNUM` is left, and there is no tool attribution.
