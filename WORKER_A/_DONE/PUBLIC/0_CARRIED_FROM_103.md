# Carried from #103 (PUBLIC PR 1b, `feat/directory-filters`) into PUBLIC PR 2 (`feat/directory-map`)

**The owner's review rule:** a serious or large review fix reopens its PR; small ones are deferred to the
**next PR as dedicated commits at its start**, named in that PR's description ("Carried from #103"). #103's
review (`C:\dev\masaha\workspace\WORKER_A\PUBLIC\6_REVIEW_PR1B_CLAUDE_CODE.md`, head `52b7a2b0`) found no
blocker; #103 merged at `c3391d0e` (2026-10-21). These are **PR 2's first commit(s)**, before the plan's PR 2
commit 1, each code fix with its own test seen red before the fix and green after (the red step is its break;
a separate break only for a guard it did not prove), recorded in `4_REPORT_PR2.md`. Read the review for each
item's file, line and scenario.

Suggested subjects (recount, ≤ 50): `fix(directory): keep near me's focus and status` (items 1, 5);
`fix(directory): stop locating when no answer comes` (item 2); `fix(directory): clear what found nothing`
(item 3); `test(directory): prove near me's privacy gates` (item 4); `fix(directory): reset the price on
clearing` (item 6); `fix(directory): close the sheet when it widens` (item 7); the documents folded into the
commit they belong with. Group them differently if a smaller set of atomic commits reads better; say so.

**Decided by the owner (2026-10-21), as the supervisor recommended:**

1. **Near me keeps the focus and is heard** (review 1): one always-mounted `role="status"` wrapper around
   `LocationStatus`, whose content changes; after «إيقاف الترتيب حسب المسافة» or «مسح موقعي» the focus moves to
   «الأقرب إليّ»; while locating the button is `aria-busy`, not `disabled`, if the layer's `Button` allows it
   without a layer change (else keep `disabled` and say so). Tests: stop, then clear, by keyboard — the focus on
   «الأقرب إليّ» each time; the granted line is inside the live region.
2. **Locating ends when no answer comes** (review 2): a watchdog in `useNearMe` — no callback within ≈ 15 s →
   the denied state with «اختر منطقتك»; a late callback after it is ignored. Test with `fakeGeolocation` and the
   fake clock.
3. **«مسح الفلاتر» in the no-match state** (review 3, the owner's choice): it clears **the filters only** when a
   filter is in force (the search and the order kept, as the sheet's and the sidebar's do); it clears **the
   search only** when the search alone narrows the list to nothing. `directory.md:53` says both. Test: a search
   and a filter together → the search kept; a search alone → the search cleared.
4. **Near me's two privacy gates proven** (review 4, the owner's §3 rule): test 42 gains a stop step (no
   privacy line, the button not pressed, no header on the next request); the header's sorting gate
   (`useDirectoryList.ts:37`) broken once (`const point = near.state.point`) and test 41 seen red.
5. **No distance after the distance order stops** (review 5): a card words its distance only while the shown
   answer was asked by distance (e.g. `cardViewOf` drops it when the request had no point). Test with a held
   answer.
6. **Clearing resets the price filter's own state** (review 6): the two clear actions reset the typed texts and
   the chosen period to the address's and cancel the pending pause. Test: «abc» in «إلى», then «مسح الفلاتر».
7. **The sheet closes when the width reaches the sidebar** (review 7): `open` set to false when `wide` turns
   true. Test with the media query faked.
8. **Back to the site from the focus shell** (review 8): **recorded, not built** — a dated line in finding 130
   (a `Pop` arrival treated as a load, and a guard's `replace` on a first load), with `#PRNUM`.
9. **Finding 130's *Resolves when*** (review 9) names `FocusLayout` beside `DashboardLayout`.
10. **The place filter's cap** (review 10): **recorded, not built** — a new finding (the next free number from
    133), naming `DIRECTORY_AREAS_MAX` and `AreaFilter`.
11. **The unwrapped comment** at `components/DirectoryList.tsx:16` (review 11) re-wrapped.
12. **The stopped state's bare «مسح موقعي»** (the review's departures, the owner's word): **kept as it is** —
    no line added.

Every item is done in PR 2; one you would leave → **stop and ask**, never silently.
