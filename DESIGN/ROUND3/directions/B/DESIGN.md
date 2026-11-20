# Direction B — «القطاع» · The Strip

> **The idea:** Masaha is the map of where to work along the Strip. Place comes first, and the Strip's long shape —
> forty kilometres of coast from Beit Hanoun to Rafah — becomes the identity's second mark, beside the logo.
>
> **Point of view:** spatial and warm. People choose a place to work by *where it is* and *what it looks like*; the
> site shows both at once. Large, calm photography where it is real; the map always one glance away; a geometric
> Arabic display face whose angles answer the logo's kufi-like letters. The memorable thing is **the Strip** — drawn as
> a tall silhouette with the spaces on it, on Home, beside the directory, on a space's page and at sign-in.
>
> **Learns from:** Airbnb's search (list and map side by side, a strict photo ratio, the card as photo + one line of
> facts with no box), Apple Maps' place cards and Guides (a calm place sheet, the map as the ground), Google Travel's
> split views, and Arabic-first apps that use a strong display face (Careem, Thmanyah's confidence with Arabic type).

## Type

- **Display: Alexandria** (Google Fonts; Arabic + Latin; geometric, by Mohamed Gaber) at 600 for headings and space
  names — its squared bowls and flat terminals answer the logo's drawing.
- **Text and UI: IBM Plex Sans Arabic** 400 / 500 (and 600 for small emphasis) — kept from today.
- Two clearly different voices: Alexandria for names and titles only; Plex for everything that is read or used.

| Style | Desktop | Phone | Line height (ar / en) | Family / weight | Use |
|---|---|---|---|---|---|
| `display` | 64 px | 36 px | 1.2 / 1.1 | Alexandria 600 | Home's h1 |
| `h1` | 44 px | 30 px | 1.25 / 1.15 | Alexandria 600 | Page titles, a space's name |
| `h2` | 28 px | 22 px | 1.35 / 1.25 | Alexandria 600 | Section titles |
| `title` | 20 px | 18 px | 1.4 / 1.3 | Alexandria 500 | A card's name |
| `body` | 16 px | 16 px | 1.75 / 1.55 | Plex 400 | Text |
| `secondary` | 14 px | 14 px | 1.6 / 1.45 | Plex 400 / 500 | Facts, labels |
| `meta` | 12 px | 12 px | 1.5 / 1.4 | Plex 400 | Freshness, captions |

Alexandria's Latin is wide: in English set `display` at 56 px and `h1` at 40 px; letter-spacing −0.01em from 28 px.

## Grid and spacing

- 8 px base; steps 4 · 8 · 12 · 16 · 24 · 32 · 48 · 72 · 112. Section spacing 112 desktop / 72 phone — **the
  rhythm changes**: wide gaps between the big sections, tight inside a card.
- Content max 1280 at 1440 (gutter 40; 768: 24; phone 16). 12 columns, 24 gap.
- **The split** (the directory ≥ 1024): list 7/12 (two card columns ≥ 1280, one below) and the map 5/12, the map
  sticky at full viewport height under the header. 768–1023 and phone: list **or** map, the toggle.
- Prose measure 66ch.

## Surfaces and elevation

- Ground n-50 / n-950. **No card boxes around space cards**: the photo is the frame (radius 16), the text sits on the
  ground under it. Panels that hold controls (filters, the place sheet, forms): white / n-900, radius 20, 1 px n-200 /
  n-800, and one soft shadow `0 1px 2px rgb(13 18 23/.05), 0 8px 24px rgb(13 18 23/.08)` (dark: no shadow, the edge).
- **The map ground** is the second surface family: land n-100, sea `i-50` (dark: land n-900, sea `i-950`), the
  governorates as bands separated by 1 px n-300 (dark n-700) lines.
- **Radius:** photos 16, panels 20, controls 12, pins and status dot 999.

## The spark

Pins of spaces **open now** (by live state or by hours) are spark-filled; the selected governorate band on Home's
Strip gets a spark edge; the selected card's photo gets a 3 px spark outline while its pin is selected on the map
(and vice versa — the list and the map are tied by the spark). Today in a week of hours: a spark dot. Never text,
never a button.

## Imagery and art direction

- **The photo ratio is 4:3 everywhere a space is a card,** radius 16. Posters fill it with `object-fit: cover` —
  acceptable because the card shows the whole space's sign; a real photo looks better and is shown larger.
- **A space's page leads with its photos when it has more than one or a real photo**: a 2-up (desktop: one large 8/12
  + a stacked pair 4/12; phone: a swipeable strip with a count «1 / 3»). With one poster only, the poster sits at 4:3 in
  the end column beside the title, not as a giant banner.
- **No photo:** the card's frame shows **the Strip's silhouette** (n-200 on n-100; dark n-700 on n-800) with the
  space's own position as a spark dot, and the area name in `meta` — real data, and it says "here" better than a
  letter. The same on the space's page.
- Never a gradient over a photo except the scrim behind text on it (n-900 at 70%, only for the photo count).

## Iconography

Lucide, stroke 1.5, 20 px. Functional only: search, sliders (filters), map / list, locate, heart, WhatsApp-message,
phone, instagram, mail, navigation, chevrons, external link, x. Amenities: icon + word in a 2/3-column list (the
data carries the Lucide name). No icon on headings or empty states.

## Motion

One orchestrated moment: **the Strip draws in** on Home's first view — the outline strokes from north to south over
300 ms (stroke-dashoffset is not transform/opacity — use a mask that translates: a clip rectangle moving down, or
reveal by opacity of 5 governorate bands in sequence, 100 ms apart), then the pins fade in. Hovering a card raises
its pin on the map (scale via transform, 150 ms). Sheets 200 ms ease-out. Reduced motion: everything instant.

## Density

Relaxed on Home and a space's page; the directory's cards are two-up and modest (photo 4:3 at ~300 px wide),
so the list shows 4–6 spaces per screen at 1440 beside the map.

## Components

- **Buttons:** primary ink, 48 px, radius 12, Plex 500 15 px; secondary: 1 px n-300 border; on a photo: never.
- **Fields:** 48 px, radius 12, 1 px n-500, label above.
- **The filter bar** (directory): a horizontal bar under the title — search (wide) · «المنطقة ▾» · «السعر ▾» · «الدوام ▾»
  · «أخرى ▾» · the sort · «الأقرب إليّ» — each a **popover panel** with that group's controls (desktop/768), so the
  list keeps its width beside the map; phone: one «الفلاتر» button → a full-height sheet with the four groups.
  The triggers show their value («شهر · 250–400 ₪»). (Popovers are dropdown buttons, not chips.)
- **The place sheet** (the map's selected space): a panel at the map's bottom (phone: a bottom sheet over the map)
  with the photo, name, state, today, «عرض المساحة».
- **Header:** on the ground, 72 px, logo 40 px; the nav at the start after the logo; actions at the end.
- **Footer:** the Strip's silhouette small at the start, the tagline, the links.
- **Map pins:** 14 px circles with a 2 px ground-colour ring: spark-filled = open now; amber-filled with a white bar =
  ممتلئ; hollow n-500 = closed; dashed hollow = no live state; selected = 24 px, an ink ring, the name in a white tag.
  Production: MapLibre with a custom style in these colours, Arabic labels, bounded to the Strip.

## Every page's division

- **Home** — (1) **the opening**: two columns ≥ 1024 — at the start the `display` h1, the lead, the search field and
  «الأقرب إليّ»; at the end **the Strip**, full height (≈ 640 px), with its five governorates named along it and every
  space as a pin (open now in spark). Hovering/focusing a governorate name highlights its band and shows its count
  («غزة · 9 مساحات»). Phone: the h1 and search first, then the Strip, still vertical but compact (≈ 360 px tall,
  centred) — its shape is the point. (2) **«مفتوحة الآن»** — a horizontal row of
  4:3 cards (scroll-snap on phone, 4 across at 1440). (3) **«تصفّح حسب المنطقة»** — the governorates north to south as
  five rows, each a large `h2` name with its areas as text links and counts; each row has the band of the Strip it is
  (a small silhouette crop) at its start. (4) **For owners** — a band with the text and «تواصل معنا». Footer.
- **The directory** — title + count; the filter bar; ≥ 1024 the split (list 7/12 · map 5/12, sticky); the cards
  two-up; hovering or focusing a card marks its pin. `?filters=open` at 1440 shows the «السعر» popover open with شهر
  chosen and the range. `?view=map` below 1024 shows the map full-width with the place sheet; at ≥ 1024 the map is
  always there, so `?view=map` collapses the list to a narrow column (or the map takes 12/12 with the place sheet —
  say which you chose).
- **A space's page** — (1) photos (as Imagery says). (2) A two-column body ≥ 1024: start 8/12 — the name (`h1`), the
  other name, the area; the unverified notice; announcements; prices (two small tables, general and students);
  hours (the week, today with the spark dot); amenities; about. End 4/12 — a **sticky place panel**: the state (word +
  dot), today's hours, «من 30 ₪ / يوم», WhatsApp (primary) and call, the heart, then the Strip mini-map with its pin,
  the address and «الاتجاهات». Phone: the panel's essentials right under the name, a bottom bar with WhatsApp and
  Call. The report link last.
- **About** — the h1 and intro beside the Strip silhouette with the real counts per governorate («13 مساحة في 5
  محافظات» — computed); verified / unverified as two columns; the states legend as the four pins with their words
  and sentences; contact; owners.
- **Sign in** — split ≥ 1024: the form (start) and the Strip panel (end, the map ground with the pins and the
  tagline); phone: the form with a thin Strip silhouette above the h1.
- **Account** — the h1, a side nav (≥ 1024; tabs on phone) and the settings in three titled groups without boxes,
  separated by space and a hairline; segmented controls for language and theme.
- **Favourites** — the cards grid (2–3 across) with «الأقرب إليّ»; the left space as a muted card with the silhouette
  and the line.
- **404** — the Strip silhouette, large, with «الصفحة غير موجودة», the sentence and «تصفّح المساحات» / «الرئيسية» —
  "this page is not on the map".

## Decisions this direction overturns

- **foundation §9 and DECISIONS_PUBLIC (U6, the Directory "at every width: the list or the map, never side by
  side")** → side by side from 1024. *Why:* choosing a place to work is a spatial decision; Airbnb and Google show both.
- **foundation §7 and §15 #2** (one font, Plex, "settled") → Alexandria for display, Plex for text (a proposal).
- **foundation §15 #3** (radius soft 8, comfortable) → 16 photos / 20 panels / 12 controls, controls 48 px.
- **DECISIONS_SHARED P5's exception and DECISIONS_PUBLIC "the Directory keeps its filter sidebar from lg"** → a
  filter bar with popovers above the list (the sidebar would squeeze the split).
- **DECISIONS_PUBLIC U12** (the card) → kept photo-led, but without a box, at 4:3, and with the Strip silhouette as the
  no-photo state (replacing the letter).
- **foundation §13, screen 1** (Home's hero) → the opening with the Strip.
- **The map's OSM default tiles** → a custom neutral style bounded to the Strip.

## New copy (proposed)

«على الخريطة» / "On the map" (the Strip's label for screen readers) · «{governorate} · {n} مساحات» per band (from
the real plural rules) · «{n} مساحة في {m} محافظات» / "{n} spaces in {m} governorates" (About) · «عرض المساحة» / "View
space" (the place sheet) · «هذه الصفحة ليست على الخريطة» / "This page isn't on the map" (404's sub-line; the h1 stays
«الصفحة غير موجودة»).

## Builder's notes

Decisions the builder took where this document left something open or where building it showed a problem. Each
stays inside COMMON.md's fixed points.

- **The map ground's colours.** Land n-100 next to sea i-50 are almost the same pale blue (#ECF4FC / #F1F8FE): the
  coast disappeared. Built instead: **sea i-100**, **the Strip itself white (dark: n-800)** with its governorate bands
  alternating white / n-50 (dark: n-800 / a mix of n-800 and n-900), **the land outside the Strip n-100 (dark: n-900)**
  with no labels at all, band lines n-300 (dark n-700), the Strip's edge n-500. Three faint offshore contour lines
  (i-200 / dark i-900) give the sea a cartographic texture. The Strip is the brightest thing on its map.
- **The outline** is the lead's `../_shared/data/strip-outline.json` (it replaced COMMON §3's cruder one, in which
  Masar Tech at Al-Mawasi fell in the sea); the governorate boundaries are schematic lines between the coast and the
  border, checked so that every space's pin falls in its own governorate's band.
- **North-up, never rotated or mirrored.** The silhouette is the shape people in Gaza know from every map (the
  diagonal), so it is drawn north-up everywhere — "tall" comes from its diagonal, not from rotating it. The map never
  mirrors with the reading direction; its furniture follows the geography (zoom controls over the sea, the legend on
  the land), placed with logical properties per direction.
- **Five governorates, four in the product.** The product's lookups have four governorates (North Gaza, Gaza, Deir
  al-Balah, Khan Younis); Rafah is not one of them. The Strip is drawn with its five real bands; Rafah is named as
  geography only (muted, not a link, no count). Counts are computed from each space's *area* (so Golden Hub counts in
  North Gaza although its pin, at its real coordinates, falls inside Gaza City — that is the data). About's line is
  therefore «13 مساحة في 4 محافظات», not 5.
- **The Gaza City inset.** Eight of the thirteen pins sit within about 2 km of each other in Gaza City; at the scale
  of the whole Strip they overlap. On Home (and at sign-in) a circular **inset** magnifies Gaza City (×3.4), tied to a
  ring on the Strip by a leader line — a cartographer's device that keeps every pin legible and becomes the opening's
  memorable detail. On the directory's working map the same problem is solved the product way: **clusters** (an ink
  disc with the count, a spark ring when one of them is open now) that zoom in when pressed, plus zoom/pan and
  «عرض القطاع كله».
- **`?view=map` at ≥ 1024: the map takes 12/12** with the place sheet; «قائمة» returns to the split. Below 1024 a
  floating «خريطة / قائمة» button switches (Airbnb's pattern), the toggle in the title row is shown from 1024.
- **Cards in the split.** Two-up from 1280 (photo ≈ 350 px wide at 1440, not 300: the 7/12 column is 728 px). From
  1024 to 1279 and on the phone the card becomes a **row** (photo 4:3 at 128 px on the phone, 220 px in the split,
  facts beside it) — the density the diagnosis asked for (a phone screen now holds four to five spaces, not one).
- **The heart sits beside the name, never on the photo** (this document's "on a photo: never"), on cards and on a
  space's page.
- **The spark's jobs, as built:** open-now pins and the open-now dot (live «متاح» or by hours «مفتوحة الآن» — the word
  always says which), the cluster ring "one is open here", the selected card's 3 px outline ↔ its selected pin's
  cluster ring, today's dot in the hours, the no-photo dot "here". **Hover is never spark** (band hover is n-200,
  card hover raises the pin by scale). «ممتلئ» is amber with a bar; closed is hollow; no live state is dashed.
- **Demo states and the clock.** A verified space's demo live state applies only inside its opening hours; outside
  them it reads «مغلق الآن», as the product computes it. Everything "now" is computed live on Asia/Gaza time, so after
  18:00 (Gaza) Home's «مفتوحة الآن» row shows its empty state — by design, not a fault.
- **Home's live line** under the search: «السبت 14:15 بتوقيت غزة · 6 مساحات مفتوحة الآن» (new copy) — the product's
  strength (hours on Gaza's clock) made visible in the first screen.
- **Pages the mock-up does not build** (register, forgot password, my reports, privacy) link to `404.html`, which is
  honest about it ("this page isn't on the map"). A valid sign-in (no request is made) goes to the account page.
- **The user's name** «سلمى الأغا» is data and is shown as typed in both languages.
- **Google's button** reads «المتابعة باستخدام Google» / "Continue with Google" — Google's own button words; no
  Google mark is drawn.
- **Favourites on the phone** use the same row card as the directory (photo 128 px beside the facts), so the six
  saved spaces fit in about two screens instead of six.
- **Posters and photos are framed differently (round 2, the lead's call).** Real interior photos (`coma-io-1`,
  `branch-hub-2`, `branch-hub-3`) fill their 4:3 frame (`cover`). Every other cover is the space's own poster: it sits
  **whole** (`contain`) on a quiet mat inside the same frame (n-100 light / n-800 dark), 16 px of even padding (8 px in
  row cards and the place sheet, 20 px in the space page's gallery), radius kept — so no sign is cut and the directory
  stops reading as a wall of other brands. Applied to every card and plate that shows a cover (directory, Home's
  «مفتوحة الآن», favourites, the map's place sheet) and to the posters on a space's page (gallery, phone strip, the
  single poster beside the name).
