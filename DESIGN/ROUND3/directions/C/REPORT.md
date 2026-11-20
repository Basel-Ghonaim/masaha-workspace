# Direction C — «الدليل» · The guide: the builder's report

## What I built
Eight static pages in `directions\C\`, working from `file://` (classic scripts, data embedded, Lucide nodes inlined):
`home.html`, `spaces.html` (list; `?filters=open` = the refine panel open with شهر chosen, a full sheet on the phone;
`?view=map` = the printed map), `space.html?slug=…` (all 13 render), `login.html` (and `?register=1`), `about.html`,
`account.html`, `favorites.html`, `404.html`. Shared: `css/guide.css` (tokens for both themes, every component),
`js/core.js` (prefs, Gaza clock, the state rules, the composed sentence, shell, entry, dialogs), `js/map.js` (the SVG
map, now on the lead's `strip-outline.json`), `js/copy.js` (both languages; NEW words marked), `js/data.js` and
`js/icons.js` (generated from `_shared` and lucide-react). Every page: skip link, one h1, header (logo home, nav,
language, theme, sign in or the user's menu), footer, review panel (collapsed, out of the tab order, «حالات تجريبية»).

The memorable thing is the type: Markazi Text for the display, the names and **each space's sentence composed from
its data only** («مفتوحة الآن حتى 18:00، في الرمال، ويبدأ سعرها من 30 ₪ لليوم.»), Plex for facts. The ink fact box is
the one heavy surface. The directory is grouped into chapters by governorate (sticky headings ≥ 1024); the active
filters read back as a sentence («4 مساحات مطابقة — بسعر شهري.»). The filters, sort, search and «الأقرب إليّ»
(simulated point in الرمال) really filter the 13 spaces. The map turns to fit its frame, clusters close pins, zooms.

## How I checked
Capture tool through the grant script (lane design-c). Final full run: 10 page states × 390/768/1440 × ar/en ×
light/dark, `--full` = 120 frames, report **clean on all 120** (no overflow, contrast, sub-12 px, focus, broken image
or console error). A second batch: all 13 space pages + demo states (`?demo=1` on Branch, the directory, the map,
Home) at 390/1440 — 32 frames clean. After the last small fixes (balanced headings, map-label collision, footer
contact) a 768 ar/en batch — 8 frames clean. I read the frames, not just the report. Fixed along the way: the map's
sea and land were indistinguishable (sea → i-100, land → n-200); posters cropped/over-tall in the spread (big plate
takes the photo's ratio); the other-language name aligned to the wrong side; favourites' names underlined and the
remove button glued to the name; a pin focus ring the tool couldn't see; list entries too tall (caption dropped in
lists, plate 216 px); spark squares inside links moved outside (never on an action); the 768 h1 orphan; the
filter panel's segmented control stretching; overlapping governorate labels on small maps.
One check batch was stopped once by the session for low machine memory (not by the run); its processes finished on
their own and released the slot; no stray Chrome left.

## Weak or unfinished
- Markazi's Arabic is a restrained Naskh; at 80 px it reads authored, but it is less calligraphic than the DESIGN's
  words suggest — the owner should judge it on screen.
- The map at desktop starts below the page head (the strip view is right, the fold is not); the Gaza City cluster
  needs a click to open (by design, but it is one more step).
- Not built: privacy page (the footer omits its link), «بلاغاتي» (opens the 404), the report form, forgot/reset pages
  (a dialog stands in), Google's real button.
- The «الأقرب إليّ» location is simulated; «اتصال» never shows (no phone contacts in today's data).

## Decisions overturned (as in DESIGN.md)
foundation §7/§15 #2 (one font) → Markazi + Plex · U12 (cover photo leading a card) → plates, no card, no frame
without a photo · the filter sidebar from lg → a refine panel under the bar + the sentence · the default order shown
grouped by governorate · foundation §13 screen 1 → cover, open now, chapters · U8 order → name, sentence, fact box
first · OSM tiles → a printed map bounded to the Strip. No chips (DIRECTORY_FILTERS kept). Builder's additions are in
DESIGN.md › Builder's notes (two spark marks: filled = live, outline = by hours; verified-without-live follows the live
site; posters mounted, photos full-bleed; the map rotates to fit).

## New copy proposed
DESIGN.md › New copy (proposed), plus the list added while building: «بتوقيت غزة», «تفتح قريبًا», «{n} مفتوحة الآن»,
«الحالة حسب ساعات العمل», «تنقيح القائمة», «كل المساحات», «القطاع كاملًا», the cluster label, «لم تُضف مرافق بعد»,
«لم تُضف وسائل تواصل بعد», About's by-hours row and its group labels, «تصفّح الدليل من فصوله», «واتساب وبريد فريق
مساحة», the sentence's live patterns, the filter-sentence patterns — all in both languages, in `js/copy.js` (NEW).

## Could not do
Nothing in scope was impossible. Truth kept: no ratings, counts of people, invented photos or prices; demo states are
off by default and the Branch announcement is marked illustrative.

## Round 2 — what changed (the lead's improvement round)

1. **The Arabic display face is real now.** The Arabic h1s, names and sentences had been rendering in the Plex
   fallback (Markazi's Arabic never loaded in headless Chrome; my earlier "restrained Naskh" note was judging the
   fallback — withdrawn). Arabic display → **Amiri** (Google serves its Arabic), via `:root[lang="ar"]`; English keeps
   **Markazi Text**. Retuned: Amiri 400 for display/h1, 700 for h2 and names; generous Arabic line heights (1.5–1.85)
   so descenders clear. Recorded as an overturn in DESIGN.md › Builder's notes › Round 2.
2. **The map is north-up**: scale-and-centre fit, sea and Strip only (no grey land). At ≥ 1024 the extra width is an
   aside with the selected entry, «تصفّح حسب المنطقة» (the whole Strip / each governorate zooms the map) and the legend;
   on the phone the panel overlays the map's foot. Fixed frame height (680 / 520 px).
3. **The directory is denser**: plate 144 px at 1440, 16 px entry padding, the state line beside the name, chapters
   56 px apart with a rule — ~6 entries per 1440 screen once scrolled (was ~2).
4. **Re-captured** `home, spaces, spaces?view=map, space?slug=branch-hub, about, 404` × 390/768/1440 × ar/en ×
   light/dark, `--full`, into `shots\` — 72 frames, report clean on all. The map got a last fix (fixed height, so the
   full-page capture no longer stretches it) and its 12 frames were captured again (`shots-map\`, clean; copied into
   `shots\`). I read the frames: Amiri renders on every Arabic page, the Strip is north-up and whole, the list holds
   ~6 entries per desktop screen.
