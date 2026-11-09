# DIRECTORY_PROD — the owner's decisions (2026-11-08)

The production step of refactor round 1: the directory's filters as the prototype now shows them (#137, merged
2026-11-07 at `40cb481d`), built in the web and the API, with their documents. Approved by the owner on 2026-11-08.
Worker: **Claude Code** in `C:\dev\masaha\app`; plan first, then execution on the owner's approval.

**The owner's bar (his words, 2026-11-08):** the tests must work well and in the right direction — never bent to
pass; the filters' tests must be very strong, with no gap.

## First commit

1. **Finding 214 — the flaky Home test.** `apps/web/src/pages/site/public/home/HomePage.component.test.tsx` ›
   «Set my location on the map» starts the pick on the Directory's map: after the navigation to `/spaces?view=map`
   it waits for the searchbox with `findByRole`'s default 1 s; on CI under load the lazy map view takes longer. It
   failed twice on #137 (which changed no app code) and passes locally alone. Fix the cause in the test (wait for the
   route's content correctly), not with a retry; record finding 214 (check the findings index first).
2. **#136's two nits:** `ListPagination.tsx` names a variable `here0` (read the location once as `search`, then
   `here = searchKey(search)`); its comment cites the workspace task «QUICK_FIXES_1» — a repository comment names the
   rule or the PR, never a workspace folder.

## The filters (as built in the prototype, #137)

3. **Price — the subscription.** A segmented choice «الكل · ساعة · يوم · أسبوع · شهر», «الكل» by default (no price
   filter). A new design-system component `SegmentedControl` (a radiogroup: one choice, arrow keys following the
   direction, Home/End, roving tab stop), documented in `foundation.md`. In the API, the period alone now **filters**:
   only the spaces with that price, hidden prices excluded (today the period alone filters nothing, S1).
4. **Price — the range.** «من / إلى» in whole shekels, shown once a subscription is chosen; placeholders = the lowest
   and highest price of that subscription; whole numbers above zero, Arabic-Indic digits accepted, «إلى» under «من»
   said on «إلى»; an invalid bound is said on its field and not sent. The API keeps `priceMin`/`priceMax` in agorot,
   which need the period.
5. **Price — the order.** In the sort only: «الأرخص شهريًا» / «الأغلى شهريًا» (by the chosen subscription; English
   "Monthly price: low to high / high to low"); the two items exist only once a subscription is chosen (not
   disabled — absent); clearing the subscription while sorting by price returns to «الأحدث تحديثًا». The API gains
   a price order in both directions that requires the period, applies the hidden-price rule, and ends with the id.
6. **The card's price.** While a subscription is chosen, each card shows that price («15 ₪ / يوم», LTR-isolated): the
   API's card carries it. Revises D4 (the card carries no price).
7. **«مفتوحة الآن» (`openNow`).** Open now by the space's hours on **Gaza's clock** and **no closure in force**, for
   verified **and** unverified spaces; a FULL verified space stays (its badge says so); a space without hours never
   passes. It **replaces** `availableNow`: Home's «المتاحة الآن» section reads it, and `availableNow` leaves the API
   (nothing else reads it). Revises ADR 0008 (the directory's filter selected `AVAILABLE`).
8. **«مفتوحة مساءً» (`evening`).** The space closes at 20:00 or later on at least one of its open days (its weekly
   schedule, not today). A space without hours never passes. (An owner-declared evening feature is a later task.)
9. **The card's state.** Verified spaces: the live status as today (متاح / ممتلئ / مغلق الآن). Unverified spaces
   **with hours**: «مفتوحة الآن» / «مغلقة الآن» by their hours (and closed under a closure in force), as a
   **neutral** badge — never the live status's colours; without hours: «لا تتوفر حالة مباشرة». The API carries this
   by-hours state as a field of its own, apart from the live status.
10. **Hours are optional.** A space without hours stays in the list and every other filter; its card and its page
    say «ساعات العمل غير متوفرة» / "Hours not available"; the admin's spaces list marks it «بدون ساعات». No default
    hours are ever assumed.
11. **«ممتلئ»** stays as built (desk check-ins against the capacity, plus the staff's override) — a badge, never a
    filter.
12. **The panel**, top to bottom: «المنطقة» (unchanged) · «السعر» · **«الدوام»** (checkboxes «مفتوحة الآن», «مفتوحة
    مساءً», «مفتوحة يوم الجمعة») · **«أخرى»** (checkboxes «المساحات الموثّقة فقط», «أسعار للطلاب»). The «المساحات»
    heading and its switch go. Each box counts once in the active count; «مسح» clears every filter (the subscription
    and the range included), not the order.
13. **Small fixes:** the filter column is 4 of 12 between 1024 and 1279 (3 from 1280) so the five subscriptions fit;
    the sheet's button in Arabic plurals (0 «لا توجد نتائج», 1 «عرض نتيجة واحدة», 2 «عرض نتيجتين», 3–10 «عرض N
    نتائج», 11+ «عرض N نتيجة»); the card's «اليوم …» line reads Gaza's day, not the browser's.
14. **18 cards a page** in the directory (divisible by 1, 2 and 3 columns; lighter on weak connections) — in the web
    and in the prototype (`docs/design/prototype/Directory.html`, its `INDEX.md`/`CHANGES.md` line). The API's
    `limit` already allows it.

## Documents in the same PR

15. `docs/features/directory.md` (D4, U1 kept, U5, S1, the new rules), `docs/api/api-contract.md` (the directory's
    query and card), ADR 0008 (a revision line: the directory filters by the hours; the by-hours state of unverified
    spaces), `docs/frontend/design-system/foundation.md` (`SegmentedControl`), and any other document a change makes
    untrue.

## The plan's open decisions (approved 2026-11-08, as the planner recommended)

OD1 (a) a public `GET /price-ranges`, kept 30 s · OD2 (a) a verified space closed by a manual override leaves
«مفتوحة الآن» · OD3 (a) the occupancy read adds `hoursStatus`; the space page shows the neutral by-hours badge · OD4 (a)
a card shows the lowest price within the range (lowest overall without one), the same value filters and orders · OD5
(a) no new admin badge («ناقصة: ساعات العمل» already marks them) · OD6 (a) the place counts once · OD7 (b) finding 215
for the prototype's Home and `TodayHours`, not fixed here. The planner's corrections stand: finding 214's cause is the
two «Search for a space» boxes (fixed in the test); the API already filters by the period alone (the web is the gap);
the web already reads Gaza's day. **Execution by a fresh Claude Code session** (the planner does not execute).

## Not in this PR (parallel tasks, their own branches)

The owner's space profile redesign; the visual identity and the logo; **spaces for women + the owner-declared
evening feature** (one task). The worker leaves their files alone and records any overlap it sees.
