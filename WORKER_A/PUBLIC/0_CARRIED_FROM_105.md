# Carried from #105 (PUBLIC PR 2, `feat/directory-map`) into PUBLIC PR 3 (the space page)

**The owner's review rule:** a serious or large review fix reopens its PR; small ones are deferred to the
**next PR as dedicated commits at its start**, named in that PR's description ("Carried from #105"). #105's
review (`C:\dev\masaha\workspace\WORKER_A\PUBLIC\6_REVIEW_PR2_CLAUDE_CODE.md`, head `f0fc8a73`; merged head
`644908a8`, the same code) found no blocker. **All its findings are PR 3's first commit(s)**, before the plan's
first PR 3 commit, each code fix with its own test seen red before the fix and green after, recorded in
`4_REPORT_PR3A.md` (PR 3 is split: these open **PR 3a**). Read the review for each item's file, line and scenario.

Suggested subjects (recount, ≤ 50): `fix(directory): end the pick with the map` (items 1, 6–8);
`fix(directory): reach the chosen space first` (item 2); `fix(directory): keep the pick's centre rounded`
(item 3); `fix(directory): say what the map does with me` (item 4); `fix(directory): show the pins loading`
(item 5); `docs: …` for items 9–13 and the findings. Fewer, larger commits are fine if each body says which
items it holds.

**Decided by the owner (2026-10-22), as the supervisor recommended:**

1. **The pick ends with the map** (review 1): when the map's view unmounts while picking, `cancelPick` runs
   (an unmount effect in `MapView` or `useDirectoryMap`), so the location from before comes back. Test: start
   a pick from a held pin's line, switch to «قائمة», see the pin's line and the distance order again; open
   «خريطة» again, no crosshair.
2. **The chosen space is reached first** (review 2, the owner's choice of the two ways): the map's overlay
   (the card, the legend, «مركّز على موقعي») comes **before** the map's panes in the DOM, with its own stacking
   above them, so it precedes the pins in the tab order; below 768 px, when the sheet opens, one polite live
   line in `DirectoryMap` says where the details are (new words in both catalogues, e.g. «{name}: التفاصيل في
   أسفل الصفحة» — the executor proposes the exact words in the report, the reviewer of PR 3 checks them). The
   focus still stays on the pin (U6 unchanged). Tests of the order and of the line.
3. **The pick's centre never leaves unrounded** (review 3): no `onViewChange` while picking (the pick needs no
   pins), and `boundsText` rounds the box **outward** to two decimals. Unit tests of both.
4. **The map's own near-me line** (review 4, the owner's words): on the map, a granted or placed location
   shows **«موقعك ظاهر على الخريطة. تُرتَّب القائمة حسب المسافة منه.»** (English: "Your location is shown on
   the map. The list is sorted by distance from it."), **with no privacy sentence and no stop button**; the
   list keeps its own line. `directory.md`'s line on when the privacy line shows becomes true on both views.
5. **The pins' first load is shown** (review 5): the map's section `aria-busy` while the whole set is pending,
   and a muted line over the map's foot (the `MapNotice` look), «جارٍ تحميل المساحات…» / "Loading spaces…".
   Test with a held answer.
6. **The picking card goes under the map below `lg`** (review 6): the `under` slot's breakpoint moves from 768
   to 1024 px (the map's own height breakpoint); the test's width moves with it.
7. **Escape closes the card from 768 px** (review 7): the same `close` as «إغلاق», the focus back on the pin.
8. **The sheet's «إغلاق» and Escape return the focus to the pin** (review 8): a test of each.
9. **The ceiling in the copy** (review 11): `directory.map.truncated` takes `{count}` from
   `MAP_PINS_CEILING`, formatted per language.
10. **The catalogue's comment on `map.pin`** (review 12): says the name is not isolated, as the code does.
11. **The Sheet's non-modal use** (review 13): one clause in `overlays/Sheet/Sheet.tsx`'s comment and in
    foundation's Sheet row (non-modal on request: no scrim, no trap). This PR then carries `area:design-system`.
12. **The overview's build line** (review 14): `docs/project/overview.md` names the site's map (with PR 3's own
    overview edit if it has one).
13. **`role="application"` named** (review 16): kept, and `frontend/architecture.md` §6 says why and what it
    costs a screen reader (browse mode off inside the map).
14. **Findings to record** (this item's block; the index holds 130, 132, 133, 131 reserved → **134** and on, in
    order): **134** each render of the map rebuilds every marker (review 9; the fix it names: memoised marks
    and stable handlers); **135** dark theme: the marks on the always-light tiles disagree with the legend
    (review 10; a design call — the light tokens inside `.leaflet-container`; for the owner's public-site
    review after PR 4); **136** the 15 s watchdog counts the time at the permission prompt (review 15; the
    owner's ≈ 15 s kept). Each a file and an index line.

Every item is done in PR 3; one you would leave, or one that proves larger than this file says → **stop and
ask**, never silently.

**After #105 merges:** the local backup branches `backup/directory-map-pre-squash` and
`backup/directory-map-pre-prnum` in `C:\dev\masaha\app` are deleted with the branch (the supervisor).
