# Review — PUBLIC PR 3b (#108)

## Head and CI

- Reviewed head: `88caa228c365613e0055cf14eeea244e59a6cbcb`.
- `gh pr checks 108`: every listed check passed (build, check:classes, check:links, format:check, lint, test:api, test:component, test:unit, typecheck; CodeRabbit passed but was rate limited).
- Final `gh pr view 108 --json headRefOid`: `88caa228c365613e0055cf14eeea244e59a6cbcb`; the head had not moved from the reviewed head.
- Diff scope: 22 files, only `apps/web` and `docs`.

## Verdict

**Not mergeable.** The status panel discards the last successful status on a polling error, and the viewer shows the wrong position total for spaces with more than five photos. The phone gallery also diverges from the approved layout. These require a fix round on this PR.

## Five most important findings

1. **should-fix — a failed refresh replaces a known live status with an error.** In `apps/web/src/features/directory/hooks/page/useSpacePage.ts:93-100`, `liveQuery.isError` takes precedence over `liveQuery.data`. TanStack Query retains prior data after a background refetch fails, while setting `isError`; after a successful `AVAILABLE` read and a later failed 60-second refresh, the visitor therefore sees “couldn’t read status” instead of the last known status. This directly breaks the approved “failed read after one keeps the last state” behavior. Add a test that succeeds once, rejects the next poll, and asserts the successful state remains visible; branch on existing data before the error state. **Fix belongs in a fix round on this PR.**

2. **should-fix — the viewer’s position total is the tile count, not the photo count.** In `apps/web/src/features/directory/components/page/Gallery.tsx:59-60`, the position prints `gallery.tiles.length`; `useGallery.ts:12-13` limits tiles to five but the viewer navigates across `total = photos.length` at lines 14-16 and 51-68. With 6 or 30 photos, later images can be announced “6 / 5” or “30 / 5” (and the viewer’s accessible alt uses the actual total). Pass the photo total to the viewer and test a collection over five photos, including a wrap boundary. **Fix belongs in a fix round on this PR.**

3. **should-fix — the phone layout renders every gallery tile instead of only the first.** `apps/web/src/features/directory/hooks/page/useGallery.ts:12,18-32` always maps the first five photos, and its `layout` only changes the grid columns; `Gallery.tsx:23-45` renders all of them at every width. The approved plan says the phone shows the first tile alone and up to five tiles from 768 px. At 390 px, a space with several photos gets a multi-tile grid instead of the specified single tile. Make the tile set responsive or otherwise hide the extra tiles below 768 px while preserving the view-all action. The executor report says the three-photo case was checked at 390 and 768, but does not establish compliance at 390. **Fix belongs in a fix round on this PR.**

4. **should-fix — test 77 does not exercise browser visibility or window focus integration.** In `apps/web/src/features/directory/hooks/status/useLiveStatusQuery.component.test.tsx:39-45`, the test mutates `document.visibilityState` and directly calls `focusManager.setFocused(false/true)`. It never dispatches the visibility-change or window-focus events, so it cannot catch a broken TanStack focus manager/browser event hookup as required by test 77. It also has no break proving the behavior turns red. Replace the direct focus-manager calls with the actual visibility and window events, retain fake timers, and demonstrate the specified break. **Fix belongs in a fix round on this PR** because this is the planned proof for the core polling decision.

5. **should-fix — finding 131’s evidence was not corrected.** The carried decision requires the sentence to clarify that the live status belongs to cards and pins, and to the page starting in PR 3b. `docs/architecture/findings/131-the-space-page-cannot-show-a-closures-notice.md:5` still says “the site's space page (#107) therefore draws no closure; meanwhile the live status says …”, which remains ambiguous now that the page displays live status. The report says item 9 was handled in the docs commit, but the finding file is unchanged in the PR diff. Correct the sentence and index/history references if needed. **Small documentation fix: worker A’s PUBLIC PR 4 first commit, recorded through `0_CARRIED_FROM_108.md`.**

## Other concrete findings and carried items

- **nit — footer space is reserved even when no contact bar is shown.** `apps/web/src/pages/site/shell/SiteFooter.tsx:8-14` applies `pb-24` to every `/spaces/:slug` route below `md`, based only on pathname. The bar itself only appears when the page has a phone or WhatsApp contact. Space pages without those contacts therefore get an unnecessary blank footer area. Tie the reserve to whether the bar is actually present, or accept and record this small layout cost. **PUBLIC PR 4 first commit** under the owner’s small-fix rule.
- **Missing test for carried item 2.** `LeafletPlaceMap.tsx:52-60` has the required `dragging={false}` and `touchZoom={false}`, with zoom buttons retained. However, the PR adds no test asserting those props, although the carried item explicitly required one. The executor report says the props are “covered by the implementation,” which is not a test. Add the prop test in **PUBLIC PR 4 first commit**, or record the omission there.
- **Carried item 9 is missing**, as above; it was not done by the docs commit.
- **Carried item 10: checked, no change required.** `apps/api/src/modules/spaces/prices/prices.service.ts:59-68` compares each non-null requested `shiftId` with the space’s saved shift IDs and rejects unknown IDs with `invalid_choice`. `apps/api/src/modules/spaces/prices/prices.api.test.ts:128-136` verifies a shift from another space is rejected and writes nothing. The API therefore does not allow the page to receive a price naming an unknown shift through the supported update path.
- Carried items 1, 3, 4, 5, 6, 7 and 8 appear implemented in the diff: the footer reserves room, the map disables drag/touch zoom, architecture §2 is corrected, the directory Authority line and comma are corrected, the route test covers the absent-contact line, the phone announcement is outside the busy section with language-marked name, loading/failed states get an `h1`, and the Escape comment now matches its handler. For item 2, the code is present but its required test is missing. For item 9, the docs fix is absent.

## Executor departures and evidence limits

- The executor report records the broader scoped component command as **58 passed files / 378 passed tests plus 5 timing/state failures in 3 files**. It says changed files were rerun directly and passed. That does not turn the scoped run green; CI’s component check is green on this PR head, but the report does not identify the three failing files or show whether they overlap changed code. Treat the local failures as unresolved evidence, not as an implementation defect established by this review.
- The executor report says hidden-tab pausing and touch-scroll over the place map were not independently exercised in the browser. Those cases remain unverified by the real run; test 77 also does not prove browser visibility/focus integration, as finding 4 explains.
- The plan’s visual matrix requires width-dependent layouts at 390, 768 and 1440 in both Arabic light and English dark. The report lists Arabic 390/768 and English dark 1440 for the gallery, not the full matrix. It also reports no 390 px footer-bottom screenshot and no map-touch-scroll screenshot. I read the executor’s report only; I did not inspect its screenshots.
- The report says Escape closed the viewer but does not say that focus returned to the opening tile. I did not inspect screenshots or rerun the browser.
- The report records tests 76–78 as red then green, but does not include the exact failing/passing output lines or the required break evidence for test 77. I did not rerun these tests.
- No API files are changed, as required. The live query uses a slug-specific key and `encodeURIComponent` in the repository; it sets `refetchInterval: 60_000`, omits `refetchIntervalInBackground` (default false), and sets `refetchOnWindowFocus: 'always'`. The list query code is untouched. Both copy catalogues have `directory.page.gallery` and `directory.page.liveStatus` strings.
- Commit objects contain eight commits, all with bodies; subjects are within 50 characters. No `fixup!`, `style:` or `wip` commit remains. The executor report’s formatting commit (`style: format directory changes`) is not a separate commit in the reviewed head, consistent with the final commit hygiene rule.
- Docs accurately describe gallery and polling behavior and use `#108`; however finding 131 is not updated. Architecture §6 says the place map is never dragged and the page scrolls past it, consistent with the new props.

## Checked and fine

- CI is green on the head reviewed; the fetched diff is 22 files and within the `apps/web` + `docs` scope.
- No-photo pages omit the gallery; the header’s no-photo caption remains driven by `space.photos.length === 0` in `useSpacePage.ts`.
- Gallery images use bilingual alt text; the first tile is eager and later tiles lazy. The dialog is titled with the space name, uses `dir="ltr"` for image and position, and has previous/next/close labels in both catalogues. Navigation wraps in the hook. The executor report says Escape closes; focus return was not independently verified.
- Status query is scoped to the slug, URL-encodes it, polls at 60 seconds while visible by default, refetches on window focus, and is separate from list queries.
- The phone live line is rendered outside the `aria-busy` section and the map Escape comment matches the behavior.
- The fix to the API price-shift validation makes carried item 10 unreachable through the supported API path.