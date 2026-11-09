# Review of #139 — Claude Code, Opus 5.5
Head: e1838447d6d113b3f48f043d8654a933748620cc · commits 5 · files 107 · checks: green (10 pass, CodeRabbit skipped) · head moved during the review: no (`gh pr view 139` at the end: `e1838447…`, `CLEAN`)
Verdict: mergeable after a fix round

All reads are pinned to `e1838447` (`git show`, `git diff origin/main...`, `git grep`); merge base `40cb481d` = `origin/main`. No blocker found: the SQL, the binding of SQL and TypeScript, the hidden-price rule and the leave-one-out hold. Library behaviour was checked in `node_modules` where a finding rests on it (Radix radio group 1.4.7, TanStack query-core 5.104.1).

## Findings (verified defects only, most severe first)

### F1 — should-fix · Switching subscription puts the old period's prices under the new period's word
- Where: `apps/web/src/features/directory/hooks/list/useDirectoryList.ts:143-144` (`cardViewOf(space, { …, period })` over `answer?.data`), with `hooks/list/useDirectoryQuery.ts:23` (`placeholderData: keepPreviousData`), at `e1838447`.
- Seen in the code: the cards are built from `query.data`, but `period` comes from the address's current filters. While a new key loads, `keepPreviousData` gives back the previous answer as `data` with `isPlaceholderData: true` (query-core 5.104.1 `queryObserver.js:314-323`). Nothing ties the price's word to the period that answer was asked with. `period === undefined` hides the price («الكل»), but a change from one period to another does not.
- Scenario: the list is filtered by «يوم» and a card reads «20 ₪ / يوم». The visitor picks «شهر». Until the monthly page arrives (seconds on a weak connection), the same dimmed cards read «20 ₪ / شهر», including spaces with no monthly price at all. A screen reader reads the same false price. No test covers a switch between two periods: `useDirectoryList.component.test.tsx` › «shows each card's price…» only goes from DAY to «الكل».
- Fix: word the price by the period of the answer on screen, not the address's. Home already does this for its title (`useHomeSpaces`' `shownNearest`, set once a real answer arrives). Simpler: show no price while `query.isPlaceholderData`, unless the period is unchanged. Add a hook test: DAY answered, then MONTH held pending → no card says «/ شهر» over a DAY price. · Belongs: a fix round on #139, folded into `d93fc646`.

### F2 — should-fix · The prototype's 4/12 column (R8) breaks at 1024–1279 px
- Where: `docs/design/prototype/Directory.html:449-450` at `e1838447`, against `docs/design/prototype/masaha/masaha.css:118`.
- Seen in the code: R8's rule is `@media (1024–1279) { .dir-filters {span 4} .dir-results {span 8} }`. Commit 5 moved `lg:col-span-9` from `section.dir-results` onto a new wrapper `div`. The section is no longer a grid item, so its `span 8` sizes nothing, and the wrapper keeps `span 9`. `masaha.css` loads after `_ds_bundle.css`, so `.dir-filters` still spans 4. That makes 4 + 9 = 13 of 12 columns, and auto-placement moves the results to a row of their own under the filters. Not rendered; read from the CSS and the markup.
- Scenario: open `Directory.html` at 1100 px (list view) → the results no longer sit beside the filter column; they drop below it. Decision 13's column is broken in the prototype that decision 14's change touched.
- Fix: give the wrapper the R8 class (`dir-results` on the `div`, keeping the section's grid classes, or a new class that R8 targets). Check at 1100 and 1300 px. · Belongs: a fix round on #139, folded into `e1838447`.

### F3 — should-fix · Removing a list test lost the proof that student prices keep a verified stale space
- Where: `apps/api/src/modules/directory/list.api.test.ts` (the test «leaves out an unverified space whose prices are stale … but keeps a verified one», removed in `d93fc646`); `apps/api/src/modules/directory/price.api.test.ts:177-213` (T14) at `e1838447`.
- Seen in the code: the removed test asserted `?studentPrices=true` → exactly `['Fresh', 'Stale verified']`: a verified space with stale prices and a fresh-at-30-days one pass. T14 keeps only the negative half: `not.toContain('Stale Unverified')`. Its «Stale Verified» and «Fresh» have no student price, so the `studentPrices` answer there is empty. Neither the 30-day boundary nor the verified branch is proven for `studentPrices` anywhere: «keeps the spaces with a student price» dates its prices `NOW`, and T33's candidates are fresh. The report's deviation ("`price.api.test.ts` proves both fully") is untrue for that half.
- Scenario (the break no test catches): write `studentPrices`' condition as `s.prices_updated_at >= cutoff` (or `>`) instead of `${pricesShown}`. Every lane stays green, while a verified space with prices older than 30 days vanishes from «أسعار للطلاب».
- Fix: in T14, give «Stale Verified» and «Fresh» a student price, and assert `names('&studentPrices=true')` equals `['Fresh', 'Stale Verified']`, written by hand. · Belongs: a fix round on #139, folded into `d93fc646`.

### F4 — should-fix · ADR 0008's body is rewritten, not only revised
- Where: `docs/architecture/decisions/0008-live-status-not-counts.md:16` at `e1838447`.
- Seen in the code: besides the dated *Revised* line (which is correct), the 2026-09-28 *Decision* bullet was changed. It said "returns `{ status }` … filter selects `AVAILABLE`"; it now says "returns `{ status, hoursStatus }` … «مفتوحة الآن» filter reads the hours". `documentation.md` §1 and its table: a record changes in three ways only (a moved link, a dated *Revised* line, a finding's status). The owner's item 15 asked for "a revision line". ADR 0002's own note, "The body below is left as first written", shows the convention.
- Scenario: a reader of ADR 0008 now sees, under the 2026-09-28 decision, a field and a filter that did not exist until 2026-11-08: the record is false as of its date.
- Fix: restore line 16 as first written; the *Revised* line already carries the change. · Belongs: a fix round on #139, folded into `dbc543cc`.

### F5 — nit · A lowest price under ₪1 hints «0», a value the field refuses
- Where: `apps/web/src/features/directory/services/pricePlaceholders.ts:7`; its test `pricePlaceholders.unit.test.ts:14-17` pins `min: '0'` at `e1838447`.
- Seen in the code: `Math.floor(minAgorot / 100)` gives `0` for any lowest price of 1–99 agorot (the API allows from 1 agora). The doc comment and DI-6 promise a hint that is never a value a bound refuses, and `priceBounds` refuses `0`. The test writes the refused value by hand as the expected one.
- Scenario: one space prices an hour at 50 agorot → «من»'s hint reads «0»; typed as hinted, it is said invalid.
- Fix: `Math.max(1, Math.floor(…))`, and the test expects `'1'`. · Belongs: a fix round on #139, folded into `d93fc646`.

### F6 — nit · Exports nothing reads
- Where: `packages/shared/src/occupancy/responses.ts:19` (`HOURS_STATUSES`); `apps/web/src/features/directory/services/requestOf.ts:12` (`DIRECTORY_PAGE_SIZE`); `apps/web/src/features/directory/services/cardView.ts:35` (`cardStatusOf`) at `e1838447`.
- Seen in the code (`git grep`): `HOURS_STATUSES` is a runtime constant of the shared package's public surface, read by no app, schema or test; it only derives the type. The other two are exported but used only inside their own file.
- Scenario: none at runtime; dead public surface that a later reader takes for a contract.
- Fix: `type HoursStatus = 'OPEN' | 'CLOSED'`, or keep the constant only once something reads it; drop `export` from the two module-local names. · Belongs: a fix round on #139, folded into `dbc543cc` (shared, `cardStatusOf`) and `e1838447` (`DIRECTORY_PAGE_SIZE`).

### F7 — nit · Commit 5 adds finding 215 without saying so
- Where: `e1838447` (`docs/architecture/findings/215-…md` and its index line).
- Seen in the code: the commit's subject and body speak of 18 a page, the column and the plurals only; finding 215 (OD7 b, the prototype's Home and `TodayHours`) is a separate fact, folded in by a fixup (report §2). The workflow asks for a commit described in one sentence.
- Fix: one sentence in the body ("Records finding 215 (OD7 b)…"), or let it ride in commit 1 with finding 214. · Belongs: a fix round on #139, reworded on `e1838447`.

## The test matrix (each T… : present / missing / weaker · would it fail on its break?)

Lanes as planned. Every API file pins its clock with `createTestApp({ clock })` (filters, hours, price, priceRanges, list, pins, liveStatus, favorites); none reads the real clock. Expectations are written by hand except T31's equality, which is a binding by design and is anchored by hand at 12:00.

**Shared (U)**
- T1–T3 present, both schemas; would fail on their breaks.
- T4 present (`0`, `-100`, `10000001` → `out_of_range`; `12.5`, `abc` → `invalid_format`). `1e3` dropped: it is accepted (EC5, recorded); not a defect.
- T5 present: each refusal word is tried on one schema only (list `maybe`, map `''`). Both schemas share one `filters` object, so this is not a gap.
- T6–T8 present.

**API (A)**
- T10 present: student-only, other period, no prices and stale unverified out; stale verified and the 30-day control in. Fails on audience dropped and on the hidden rule dropped.
- T11 present, both bounds alone and together, inclusive.
- T12 present (several DAY prices: a shift and a label; a lower student price never the card's). Fails on `max()` and on bounds left out of the price.
- T13 present.
- T14 present, but **weaker** for `studentPrices` (F3).
- T15 present: absent without a period, on pins, the page and favourites. Fails on `null` sent.
- T16 present: `moveRowToEnd`, pages 1–3 whole, totals; fails on `id DESC` and on no tie-break.
- T17 present (`q=P`: equal scores, so an order by score would read P1…P5).
- T18 present.
- T19 present: hidden-price, hidden, deleted, unlisted area and student exclusions each move a min or a max; `null`; `public, max-age=30`; 304 on `If-None-Match`. No verified-stale positive case, but that rule's helper is T10's.
- T20–T22 present. T21 cannot fail on its own named break ("closed flag ignored") because a closed day's minutes are null (report §6). It does fail on a wrong day index, so it is not a test that cannot fail.
- T23 present: in force, begins now, ended at now, ended before, not begun, deleted, outage. Fails on `lte`/`lt` at either edge.
- T24 present, including OD2 (closed by hand out; override expired at `until = now` stays; FULL by hand stays).
- T25–T27 present: Gaza day boundary both ways; DST both directions, so a fixed +2 or +3 offset fails; 24:00.
- T28 present.
- T29 present: 1200/1199; one late day read on a morning when that day is closed; around the clock; all closed; no hours.
- T30 present (card and pin, verified too, live status kept).
- T31 present: four clocks (opening minute, closing minute, 23:59, into Friday), a closure space in force at three of them, the non-empty anchor at 12:00, and the verified CLOSED ⇔ CLOSED check. Fails on either rule drifting to `<=`.
- T32 present (list). The map's `availableNow` is not tried over HTTP; T6 covers the strip on both schemas.
- T33 present and sound: each candidate fails exactly one filter at Thursday 10:00. All filters together keep exactly «Focus Passes». Dropping each filter returns exactly its space. «Focus No Hours» fails only the hours filters; totals match. An OR-ed or wrong-column filter (for example, the bounds on the student price) fails it.
- T34–T36 present.
- T37 present (unit).
- T38 present (`list.api.test.ts`: 37 → 18/18/1).
- T39 present (keys + T15).

**Web unit (U)**
- T40, T41 present. T42 present (existing test). T44 present (pins F5's «0»).
- T45 present: neutral on both by-hours states, verified unchanged, price isolated in both languages.
- T46, T47 present.

**Web component (C)**
- T50 present: radiogroup named and described by its Field; click; RTL and LTR arrows held as a real key press, checking and focusing; loop; Home/End check and focus (fail without the handler: Radix 1.4.7 checks only on `ARROW_KEYS` and only while one is down, `index.mjs:220, 339-372`); one tab stop entering on the checked segment; axe in both directions.
- T51 present.
- T52 present: at hook level (`usePriceFilter`: «٢٥٠» → 25000, `0`/`12.5` said and not sent, «إلى» under «من») and component level (placeholders 12/100, the described radiogroup).
- T53 present (`useDirectoryList` + `usePriceFilter`'s three «الكل» cases).
- T54, T55 (7 with everything on; 3 with a bare subscription), T56, T57 present.
- T58 present: card, its description and price, «ساعات العمل غير متوفرة». The neutral variant is proven in the unit lane, where it is decided.
- T59 present. T60 present (0, 1, 2, 3, 10, 11, 100; en 0, 1, 12). T61 present (Home test + `useHomeSpaces`).
- T65 present (existing `rowView.unit.test.ts:135`). T66 present (`useDirectoryMap`: hours items, request `{ openNow, evening }`, pins named by the state, the dashed mark).
- T80 present: waits for the h1 «Workspaces», then `getByRole` (throws on two), then near me's button gone. Fails if the pick lands on `/spaces`.
- T81 present (no test diff on `ListPagination`).

**Missing from the matrix's intent**
- A switch between two subscriptions with the previous page kept (F1).
- The student-price positive half (F3).

## The owner's decisions and the ODs (each: built as approved / departed, judged)

- **1** built: test-only fix, `warm(…)` with 60 s, finding 214 Resolved. The root cause (two same-named search boxes) is consistent with react-router's state changing before React commits. The CI timings come **only from the report and the finding**.
- **2** built (`search`, a comment naming the rule).
- **3** built: «الكل» default, `SegmentedControl` in `foundation.md` §3/§12 and the showcase. The period alone filters (the API already did; the web gap fixed, SD-2).
- **4** built: whole shekels, Arabic-Indic digits, placeholders from `/price-ranges`, «إلى» under «من» said on «إلى», refused bound not sent. The «0» hint is F5.
- **5** built: absent under «الكل»; «الكل» or clearing → the default order (SD-7/SD-8, approved with the plan); API orders need the period and end by id ascending.
- **6** built: `priceAgorot`, «15 ₪ / يوم» isolated. F1 is a defect of its display during loading.
- **7** built: Gaza clock, closures, verified and unverified, FULL stays, no hours never; `availableNow` gone from API, shared, web and Home. Remaining matches are history or examples, per EC11, re-grepped.
- **8** built.
- **9** built: verified unchanged, unverified with hours neutral, without hours «لا تتوفر حالة مباشرة»; a field of its own.
- **10** built: card, map card, status card and hours section say «ساعات العمل غير متوفرة»; no default hours.
- **11** unchanged, proven by T24.
- **12** built: order, two `CheckGroup`s, no «المساحات»/switch, «مسح» keeps the order (a price order excepted).
- **13** built: `lg:col-span-4 xl:col-span-3`, five plural forms, Gaza's day already. The prototype's R8 is broken by F2.
- **14** built: web and prototype at 18, `CHANGES.md` R9 and a P6 note, no `INDEX.md` line (EC19, sound).
- **15** built, except F4.
- **OD1 a** built.
- **OD2 a** built, consistent with `overrideInUse`: under `openNow` the space is open by its hours with no closure, so a stored `CLOSED` override in force is the one in use.
- **OD3 a** built: `/occupancy` adds `hoursStatus`; the page's neutral badge with «حسب ساعات العمل؛ …».
- **OD4 a** built: one lateral `min()` is the filter, the card's price and the order key.
- **OD5 a** built (a `space-links.md` line).
- **OD6 a** built.
- **OD7 b** built (finding 215, Open).

## The report's deviations, judged

- **#139 not #138** — sound (taken by the parallel PR).
- **Per-commit lint not run** — acceptable: the owner's instruction after the memory stop; lint is green on the head and in CI, typecheck per commit.
- **PR title naming three commits** — acceptable: three equal main commits; a stated departure.
- **Two list tests removed** — wrong in part. The period/bounds test is fully re-proven by T10/T11. The stale-price test's `studentPrices` positive half is not (F3).
- **T10–T18 in `price.api.test.ts`** — sound (one file per concern).
- **`text-card-foreground` on `bg-card`** — sound (the verified "-foreground on its surface" pair; `--card-foreground` exists in both themes).
- **`aria-label` «نوع الاشتراك» rather than a visible Field label** — acceptable. The visible «السعر» names the enclosing group, each radio is named by its visible text, and the line describes the radiogroup (proven by `toHaveAccessibleDescription`). The component's Field naming is proven by T50.
- **`todayHours` always a string** — sound (decision 10 makes "no hours" a line, not nothing).
- **Finding 215 folded into commit 5** — acceptable as placement, but the body omits it (F7).
- **EC19, no `INDEX.md` line** — sound.
- **Report §4, «الكل» without `min/max: undefined` removed as redundant** — sound: `paramsOf` writes no bound without a period, and `filtersOf` reads none.
- **Report §6, `NOT h.is_closed` kept though redundant** — sound (kept alike in `evening` and `openFriday`); T21's named break is unfalsifiable, as said above.

## Documents

- **`directory.md`**: true to the code, with the History lines dated `#139`. Its *Decisions* restate the open-now rule, which `data-model.md` owns, as the old `availableNow` line did.
- **`api-contract.md`**: query, card, pin, `PublicOccupancy`, `HoursStatus`, `PriceRanges`, `GET /price-ranges` (30 s), and the sorts all match the code.
- **ADR 0008**: the *Revised* line is right; the body edit is F4.
- **`data-model.md`**: the state by the hours, open now, open in the evening, and the live status's filter line are true. "One test binds them at an opening minute, a closing minute, a closure and a day boundary" matches `hours.api.test.ts`, whose closure space is in force at three of the four clocks.
- **`occupancy.md`, `announcements.md`, `conventions.md` (§8/§9 lines), `spaces.md`, `space-links.md`, `overview.md`** (Built line and v1 line, nothing claimed unbuilt): true.
- **`foundation.md`**: §3, §12 row, §13 Home/Directory lines true. The §12 row does not name the chosen segment's text colour (`card-foreground`); not false.
- **Findings 214 and 215**: index lines present. 214's evidence (CI timings) is only in the finding and the report.
- **`CHANGES.md`**: R9 and the P6 note are true. The prototype itself regresses R8 (F2).
- **PR numbers**: `#139` where a number belongs. No `#PRNUM` and no stray `#138` in `docs/`, `apps/` or `packages/` (git grep).

## Scope and commits

- **Scope**: no migration or schema file. No tokens or palette, no `shared.jsx`, no `Home.html`, no space-profile file. The overlaps with the women/evening task (`requests.ts`, `publicListing.repository.ts`, `directory.service.ts`, `FiltersForm`, `useFiltersPanel`, the catalogues, `directory.md`, `api-contract.md`, `Directory.html`) are those §8 recorded. `CHANGES.md` conflicts with #138 (both append; the report's §7). Nothing on the *Not in v1* list.
- **Commits**:
  - 5, Conventional; subjects 36–48 characters; each with a body.
  - No trailers or attribution (`%(trailers:only)` empty); no `fixup!`.
  - Atomic as planned, F7 aside.

## Not checked, and why

- **Not run**: no lane, build, server or browser (the review is read-only), so the layouts (production's 4/12 column, F2's prototype at 1100 px, `SegmentedControl` at 1024 px in Arabic, the dark edge) were judged from classes and CSS only.
- **Only in the report**: the report's red-first claims, the per-commit typecheck, the three local component runs, the real `masaha_dev` run and the 34 screenshots; also the CI logs of #137 (finding 214's 156/206 ms).
- **Not traced end to end**: `hours.weeksFor` (I relied on T30/T33 proving a space without rows reads `null`). The prototype's `_ds_bundle.css` was not opened to confirm whether its utilities sit in a cascade layer; either way the unlayered `masaha.css` R8 rule wins over them, which F2 relies on.
- **Not reviewed beyond the diff**: `docs/plans/v1-mvp.md` and `localisation.md`'s remaining `availableNow` mentions, taken as history and an example (EC11).
