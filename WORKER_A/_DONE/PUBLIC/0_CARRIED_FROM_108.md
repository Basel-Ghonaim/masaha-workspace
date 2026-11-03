# Carried from #108 (PUBLIC PR 3b, `feat/space-photos-status`, merged at `dec7bd37`) into PUBLIC PR 4 (Home, About, errors)

**The owner's review rule:** a serious or large review fix reopens its PR; small ones go to the **next PR as
dedicated commits at its start**, named in that PR's description ("Carried from #108"). #108 was merged by the
owner on a Codex review that called it not mergeable
(`C:\dev\masaha\workspace\WORKER_A\PUBLIC\6_REVIEW_PR3B_CODEX.md`, head `88caa228`); every finding comes here.
The supervisor confirmed items 1, 2, 3 and 6 in the code on `origin/main` `dec7bd37`. These are **PR 4's first
commits**, before the plan's PR 4 commit 1, each code fix with its own test seen **red** before the fix and
green after, recorded in `4_REPORT_PR4.md`. Read the review for each item's file, line and scenario.

Suggested subjects (recount, ≤ 50): `fix(directory): keep the last status on a failed read` (item 1);
`fix(directory): count every photo in the viewer` (item 2); `fix(directory): show one tile on a phone`
(item 3); `test(directory): drive the refresh by browser events` (item 4); `fix(site): reserve the bar's room
only with a bar` (item 6); `test(map): prove the place map lets a phone scroll` (item 7); `docs: …` (item 5).

1. **A failed refresh keeps the last known status** (review 1): `useSpacePage.ts` ≈ 93–100 checks `isError`
   before `data`; with data present, show it (the plan's "a failed read after one keeps the last state"). Test:
   a first read `AVAILABLE`, the next poll rejects → `AVAILABLE` still shown. Break: the old order → red.
2. **The viewer's total is the photo count** (review 2): `Gallery.tsx` ≈ 59–60 prints `tiles.length`; it must be
   the photos' total (`useGallery`'s `total`). Test: seven photos, the viewer at the 6th reads «6 / 7», and the
   wrap from 7 to 1. Break: `tiles.length` back → red.
3. **On a phone the first tile alone** (review 3; the plan's PR 3 commit 5: "five tiles at most from 768 px, the
   first alone on a phone"): today `useGallery` maps up to five and `layout` is `grid-cols-2` below `md` for 3+.
   Below 768 only the first tile shows (literal classes, e.g. the others `hidden md:block`), and «عرض كل
   الصور (n)» stays on it. Test of the classes by count; a real-run shot at 390 and 768 with 3+ photos.
4. **Test 77 drives the refresh by the browser's events** (review 4): `useLiveStatusQuery.component.test.tsx`
   ≈ 39–45 calls `focusManager.setFocused` directly; dispatch `visibilitychange` (with `visibilityState`) and
   the window's `focus` instead, fake timers kept: hidden → no poll at 60 s; visible / focus → a read. Break:
   `refetchOnWindowFocus` removed (or `refetchIntervalInBackground: true`) → red, recorded.
5. **Finding 131's sentence** (review 5; #107's carried item 9, left undone in #108):
   `docs/architecture/findings/131-…md` line 5 reads "the cards' and pins' live status (and the page's, since
   #108)"; its index line if it repeats the words.
6. **The footer's room only when the bar shows** (review, nit): `SiteFooter.tsx` ≈ 8–14 pads every
   `/spaces/:slug` below `md`; tie it to the bar actually drawn (the page has a phone or WhatsApp), e.g. the
   space page sets it through the site layout rather than the pathname. Test: a space with no phone or
   WhatsApp → no `pb-24`; with one → `pb-24`. Break: the pathname rule back → red.
7. **The place map's props have a test** (#107's carried item 2, left without its test): `LeafletPlaceMap.tsx`
   ≈ 52–60 `dragging={false}`, `touchZoom={false}`, the zoom buttons kept. Break: `dragging` on → red.
8. **#108's real-run gaps, done in PR 4's real run** (screenshots in `shots\pr4\carried\`): the status kept
   while the tab is hidden then refreshed on return; a finger scroll over the place map at 390 moves the page;
   the page's bottom at 390 with the bar (footer not covered) and without a bar (no blank band); the gallery at
   390, 768 and 1440 in Arabic light and English dark; after Escape closes the viewer, the focus is back on the
   tile that opened it (if it is not, that is a fix here, with a test).

**Checked, not carried:** #107's carried item 10 — the API refuses a price naming an unknown shift
(`prices.service.ts` 59–68, `prices.api.test.ts` 128–136); no change.

Every item is done in PR 4; one you would leave, or one that proves larger than this file says → **stop and
ask**, never silently. A new finding takes **137** and on.
