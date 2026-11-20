# Direction B — «القطاع» · The Strip: the builder's report

## What I built

Eight static pages in `directions\B\`, working from `file://` (classic scripts, no modules, no fetch, no library):
`home.html`, `spaces.html` (list; `?filters=open`; `?view=map`), `space.html?slug=…` (all 13 render), `login.html`,
`about.html`, `account.html`, `favorites.html`, `404.html`. Shared: `css\b.css` (tokens for both themes, all
components), `js\core.js` (preferences, Gaza clock, data + Demo-states overlay, the Strip map engine, shell, dialogs,
card), `js\copy.js` (both languages), `js\data.js` (generated from `_shared\data`, incl. the lead's
`strip-outline.json`), `js\icons.js` (Lucide nodes copied from `app-dr`'s `lucide-react`), one script per page group.

- **The memorable thing — the Strip**, drawn as SVG from the real coordinates on a map ground of its own (sea i-100 /
  i-950 with offshore contour lines; the Strip white / n-800 in five governorate bands; the land outside plain and
  unlabelled). On Home it *is* the opening: a full-bleed map behind the header with the h1, search and «الأقرب إليّ» on
  it; the governorates named along the Strip's eastern edge with real counts (links to the directory); every space as
  a pin (spark = open now); a **Gaza City inset** magnifying the eight pins that would otherwise overlap. The bands
  draw in north to south, then the pins (instant under reduced motion). The same Strip is the directory's working map,
  the space page's mini-map, About's figure («13 مساحة في 4 محافظات», computed), the sign-in panel, the 404 ("this page
  isn't on the map"), the no-photo frame (the space's own position as a spark dot), Home's governorate thumbnails and
  the footer mark.
- **Home:** the opening; a live line «السبت 15:08 بتوقيت غزة · 6 مساحات مفتوحة الآن» (computed on Asia/Gaza); «مفتوحة
  الآن» as a 4:3 card row (scroll-snap, previous/next); «تصفّح حسب المنطقة» as four governorate rows north to south;
  the owners' ink band.
- **Directory:** a filter bar (search · المنطقة · السعر · الدوام · أخرى · الترتيب · الأقرب إليّ) with popovers; set
  triggers show their value in the selected tint («شهر · 250–400 ₪»); on the phone one «الفلاتر» button opens a
  full-height sheet with «عرض 3 نتائج». ≥ 1024 the split (list 7/12 — two-up from 1280, row cards 1024–1279 — map
  5/12, sticky). The map zooms (buttons, wheel, drag), clusters overlapping pins (press to zoom in) and is tied to the
  list by the spark (hover a card → its pin rises; select a pin → its card's photo gets the spark outline and the place
  sheet opens with «عرض المساحة»). `?view=map`: map 12/12 at ≥ 1024, full width with a floating «قائمة / خريطة» below.
  **The filters filter** — checked by script: open now 13→6, الرمال 4, search "branch" 1, daily price 5, + student
  prices 1; «الأقرب إليّ» sorts from a simulated point in الرمال («على بعد 0.5 كم» + the product's sentence).
- **A space's page:** photos by the imagery rule (Branch Hub: a real interior large, the pair beside, the poster last;
  phone swipe strip «1 / 3»; a single poster at 4:3 beside the name); name, other name, area, heart beside the name;
  the quiet unverified note with «هل تدير هذه المساحة؟ تواصل معنا» (dialog with the platform's WhatsApp and email);
  the Demo announcement; prices (general / students, «للعرض فقط · الدفع في المساحة»); hours grouped, today's spark dot,
  «عرض كل الأيام»; amenities icon + word; about; every group's freshness; the sticky place panel (state word + dot and
  its source sentence, today, «من 30 ₪ / يوم», WhatsApp, other contacts, mini-map, address, «الاتجاهات» by
  coordinates); the report link; on the phone the essentials under the name and a WhatsApp / Call bar. Elevate and
  Jreas render their missing facts honestly.
- **Sign in** (form start, Strip panel end; small silhouette above the h1 on the phone; blur-first errors; nothing is
  sent; a valid sign-in goes to the account page), **About**, **Account** (language and theme controls really switch;
  «تغيير» opens the password form in place with live rules), **Favourites** (five saved spaces, Masahat with its photo
  removed → the no-photo frame, «نور هب» gone with «إزالة», undo toast, «الأقرب إليّ»; row cards on the phone), **404**.
- **Shell:** skip link, one h1, logo (berry / dark-berry, 40 px) home, nav, language and theme switches in place (the
  address kept in step), sign-in or the user's menu, phone menu sheet, footer. **Review panel**: dashed, collapsed,
  bottom corner opposite the header's actions; every page and state, every space, «حالات تجريبية / Demo states».

## How I checked

Every Chrome run went through `heavy.mjs`, lane `design-b`: a smoke batch; five states × 390/768/1440; all pages at
390/1440 full-page; English dark; a scripted functional probe of the filters; **the final run: all ten states ×
390/768/1440 × Arabic/English × light/dark — 180 captures, all clean** (no overflow, no contrast failure, nothing
under 12 px, no missing focus style, no broken image, no console error; reports in `shots\report-ar-light.txt`,
`report-en-dark.txt`, `report-mixed.txt`); then favourites again after its last change (12 captures, clean,
`shots-fav\`).

Found in the images and fixed: a 47 px overflow on every phone page (the SVG maps sized themselves from their own
width attribute); focus rings that lived only on a pseudo-element (cards) or a sibling (map pins); the inset over the
header and over the Strip; the hero h1 wrapping to an orphan; the price range reading backwards in RTL; the legend
sitting on the Strip (map furniture now follows the geography); the sort trigger crowding the phone bar; the long
phone filter sheet (areas in two columns); unstyled state on the phone; stretched segmented controls; 720 px-wide
price and hours tables; favourites one card per phone screen. The lead's `strip-outline.json` replaced COMMON §3's
outline before the final check; all 13 pins fall inside it and in their own governorate's band (checked by script).

Senior pass (`ui-review`, `anti-slop`): no glass, no gradients, no pills around metadata, no icons on headings or
empty states, no decorative illustration, no card boxes around spaces; one bold element (the Strip), the rest quiet.
Hover is n-200 / a raise, never the spark; selected triggers use s-100; the spark is never text or on an action.

## Weak or unfinished

- "Open now" is live on Gaza's clock: after 18:00 (Gaza) Home's row shows its empty state and most pins go hollow —
  truthful, but a quieter Home in the evening. My captures were taken around 15:00 Gaza time.
- Gaza City pins still cluster on the directory map at whole-Strip zoom (the inset solves it on Home only); pressing
  the cluster zooms in.
- 10 of 13 photos are posters; at 4:3 `cover` some lose their edges (Elevate's wordmark is cropped).
- Not built: register, forgot password, my reports, privacy (they link to the 404); no pick-on-map, no
  location-denied state. Governorate boundaries are schematic. The review panel can cover a corner at 390.

## Decisions this direction overturns (as in DESIGN.md)

- foundation §9 / DECISIONS_PUBLIC U6 (list **or** map) → side by side from 1024.
- foundation §7, §15 #2 (one font, Plex) → Alexandria for display, Plex for text.
- foundation §15 #3 (radius soft 8, comfortable) → 16 photos / 20 panels / 12 controls, controls 48 px.
- DECISIONS_SHARED P5's exception / DECISIONS_PUBLIC (the filter sidebar from lg) → a filter bar with popovers.
- DECISIONS_PUBLIC U12 (the card) → photo-led without a box, 4:3, the Strip silhouette as the no-photo state.
- foundation §13 screen 1 (Home's hero) → the opening with the Strip.
- The map's OSM default tiles → a custom style bounded to the Strip (production: MapLibre in these colours, Arabic
  labels, bounded to the Strip).
- Chips are not brought back: the filter triggers are dropdown buttons.

## New copy proposed (both languages)

From DESIGN.md: «على الخريطة» / "On the map" · «{governorate} · {n} مساحات» (built from the product's `areas.line` +
`areas.count`) · «{n} مساحة في {m} محافظات» / "{n} spaces in {m} governorates" · «عرض المساحة» / "View space" · «هذه
الصفحة ليست على الخريطة» / "This page isn't on the map". Added while building: «{اليوم} {الساعة} بتوقيت غزة» / "{day}
{time}, Gaza time" · «{n} مساحات مفتوحة الآن» / "{n} spaces open now" (all plural forms) · «من {السعر} / {الفترة}» /
"From {price} / {period}" · «عرض القطاع كله» / "Show the whole Strip" · «{n} مساحات — تكبير» / "{n} spaces — zoom in"
(cluster label) · «رفح» / "Rafah" (geography only) · «المتابعة باستخدام Google» / "Continue with Google" (Google's own
button words) · Demo announcement «تمديد ساعات العمل حتى 22:00 طوال الأسبوع» / "Opening hours extended to 22:00 all
week" (illustrative).

## Could not do / notes

- One queued capture was stopped by Claude Code for low machine memory while it still waited for a slot (it never
  ran, left nothing behind); I retried once, smaller, per the memory-kill rule, and it passed.
- No server, no git, no repository edit, no request to the live site; written only inside `directions\B\` (plus my
  capture logs `shots-log.txt`, `shots-run.log`, `shots-fav-log.txt` there). A few early-only shots remain in `shots\`
  beside the final ones.

## Builder's notes appended to DESIGN.md

Map colours (sea i-100, the Strip white, the outside n-100 — DESIGN's n-100 / i-50 were indistinguishable); the
lead's outline; north-up, never rotated or mirrored; five bands but four product governorates (Rafah as geography
only, counts by area); the Gaza City inset and the directory's clusters; `?view=map` = map 12/12; row cards on the
phone, in the 1024–1279 split and in phone favourites; the heart beside the name; the spark's jobs as built; demo
live states only inside opening hours; Home's live line; unbuilt pages → 404; the user's name as data; Google's
button words.

## Round 2 (the lead's three points)

1. **Posters on a mat.** Real photos (`coma-io-1`, `branch-hub-2`, `branch-hub-3`) still fill the 4:3 frame; every
   poster now sits whole (`object-fit: contain`) on an n-100 / n-800 mat with 16 px even padding (8 px in row cards
   and the place sheet, 20 px in the space page's gallery), radius kept. Applied in the directory, Home's «مفتوحة
   الآن», favourites, the place sheet and on a space's page (gallery, phone strip, single poster). Elevate's wordmark
   is no longer cut; the directory grid reads calmer, with Coma's real room the one photo at full bleed. Rule recorded
   in DESIGN.md › Builder's notes.
2. **Footer tagline:** `text-wrap: balance` and a 46ch measure — one line at 1440 and 768, two balanced lines on the
   phone; the silhouette mark no longer crowds it.
3. **Re-capture:** home, spaces, spaces?view=map, space?slug=branch-hub, space?slug=elevate-hub, favorites ×
   390/768/1440 × ar/en × light/dark, full page, lane `design-b` through the grant script, into `shots\`
   (`shots\report-round2.txt`): **72 captures, all clean**, no console error. Read: the directory at 1440 (ar light),
   Branch Hub full page, Elevate at 1440 (en dark), favourites at 390 (en dark).
