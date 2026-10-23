# Carried from #107 (PUBLIC PR 3a, `feat/space-page`) into PUBLIC PR 3b (the photos and the live status)

**The owner's review rule:** a serious or large review fix reopens its PR; small ones are deferred to the
**next PR as dedicated commits at its start**, named in that PR's description ("Carried from #107"). #107's
review (`C:\dev\masaha\workspace\WORKER_A\PUBLIC\6_REVIEW_PR3A_CLAUDE_CODE.md`, head `a85151b9`) found no
blocker and asked for no fix round. These are **PR 3b's first commit(s)**, before the plan's PR 3 commit 5,
each code fix with its own test seen red before the fix and green after, recorded in `4_REPORT_PR3B.md`. Read
the review for each item's file, line and scenario.

Suggested subjects (recount, ≤ 50): `fix(site): keep the footer above the contact bar` (item 1);
`fix(map): let a phone scroll past the place map` (item 2); `fix(directory): name the page while it loads`
(item 7); `test(site): prove the dialog's none line` (item 5); `docs: …` (items 3, 4, 8, 9).

**Decided by the owner (2026-10-22), as the supervisor recommended:**

1. **The contact bar never covers the footer** (review 1): the room for the fixed bar is left after the site's
   footer, not inside the details (a spacer or the site layout's padding while the bar shows); a width test, and
   a real-run shot at the bottom of the page at 390.
2. **The place map lets a phone scroll** (review 2): `dragging={false}` and `touchZoom={false}` on the place map
   (the zoom buttons kept), so a finger on it scrolls the page; `architecture.md` §6's sentence says what the
   code does. A test of the props, and the real run's scroll over the map at 390.
3. **`architecture.md` §2** (review 3): the last sentence no longer says the space page is not built; the
   file's *Last Updated* bumped.
4. **`directory.md`'s *Authority* line** (review 4): names the map and the space's page; the stray double comma
   removed.
5. **Test 75 proves the page's wiring** (review 5): in `routes.component.test.tsx`, an unverified space with no
   contact configured opens the dialog and finds the `none` line; with an email stubbed, the `mailto:` link.
   Break: drop `none` in `SpacePage.tsx` → red.
6. **The phone's live line** (review 6): the words stay «{name}: التفاصيل في أسفل الصفحة» / "{name}: details at
   the bottom of the page"; the name carries its language mark (`lang`/`dir` as the pins' names do); the live
   line moves outside the section that turns `aria-busy`.
7. **The space page's loading and failed states have a heading** (review 8): a visually hidden `h1` with
   `site.links.space` while loading or failed; a test.
8. **Escape's comment** (review 7): says what the code does (Escape on the map closes the card wherever the
   focus is inside the map).
9. **Finding 131's evidence** (review 9): "the cards' and pins' live status (and the page's, from PUBLIC PR
   3b)".
10. **Prices that all name an unknown shift** (review 10, plausible): first check in the API (validation of a
    price's `shiftId` against the space's saved shifts) whether it can answer such a price. If it can, the page
    shows «لم تُضف أسعار بعد» instead of an empty section (a unit test of `priceGroups`); if it cannot, say so
    in the report with the file and line that prevents it, and change nothing.

Every item is done in PR 3b; one you would leave, or one that proves larger than this file says → **stop and
ask**, never silently. A new finding takes **137** and on.
