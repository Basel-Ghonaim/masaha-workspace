# Direction C — «الدليل» · The guide

> **The idea:** Masaha as a well-made guide to the Strip's workspaces — the governorates are its chapters, each space
> an entry written from its facts, set in type that reads as if someone set it by hand.
>
> **Point of view:** editorial and typographic. Masaha's value is *trustworthy information* (where it comes from, how
> fresh it is); a guide is the form people already trust for that. Calm, generous, asymmetric pages; a Naskh display
> face with real Arabic calligraphic character beside a clean sans for facts; an ink fact box on every entry. The
> memorable thing is **the type**: big Naskh headlines and each space's one-sentence summary composed from its real
> data.
>
> **Learns from:** Thmanyah (ثمانية) — a confident Arabic editorial identity; Monocle's and Wallpaper*'s city guides —
> entries with a standfirst and a fact box; Atlas Obscura's place entries; the Financial Times' fact panels; Apple's
> Guides in Maps.

## Type

- **Display: Markazi Text** (Google Fonts; Arabic Naskh + Latin serif, by Borna Izadpanah) 500 / 600 for the h1,
  the section titles, the space names and the standfirst.
- **Text and UI: IBM Plex Sans Arabic** 400 / 500 for facts, controls, labels, tables, navigation (kept from today).
- The contrast between the two is the system: Markazi says, Plex informs.

| Style | Desktop | Phone | Line height (ar / en) | Family / weight | Use |
|---|---|---|---|---|---|
| `display` | 80 px | 44 px | 1.25 / 1.05 | Markazi 600 | Home's h1 |
| `h1` | 56 px | 36 px | 1.3 / 1.1 | Markazi 600 | Page titles, a space's name |
| `standfirst` | 26 px | 21 px | 1.6 / 1.35 | Markazi 500 | A page's or entry's lead sentence |
| `h2` | 34 px | 26 px | 1.35 / 1.2 | Markazi 600 | Chapters (governorates), sections |
| `entry` | 24 px | 21 px | 1.35 / 1.2 | Markazi 600 | A space's name in a list |
| `body` | 17 px | 16 px | 1.8 / 1.6 | Plex 400 | Running text |
| `fact` | 15 px | 15 px | 1.6 / 1.45 | Plex 400 / 500 | Facts, tables, labels |
| `meta` | 13 px | 13 px | 1.5 | Plex 400 | Freshness, captions |

Markazi's Arabic sits small on its body — set it ~10% larger than a sans at the same role (the values above already
are). English uses Markazi's Latin (a text serif) for the same roles. Numerals in facts: Plex, tabular.

## Grid and spacing

- **An asymmetric 12-column grid**, content max 1240 at 1440 (gutter 48; 768: 32; phone 20). Chapter and section
  headings sit in a **start column (3/12)**; their content in the remaining 9/12 — the guide's margin. On phone the
  heading sits above.
- Spacing: 8 px base; 8 · 16 · 24 · 32 · 48 · 80 · 128. Chapters 128 apart (phone 80) — the page breathes between
  chapters and is compact inside an entry.
- Prose measure: 62ch for body, 30ch for the standfirst.

## Surfaces and elevation

- Ground n-50 / n-950 (the identity's cool paper — **not** cream). **No cards.** Entries are type on the ground,
  separated by space and, in a list, by a 1 px n-200 rule *between entries only* (not boxes, not every element).
- **The fact box:** an ink panel (n-900 in both themes; in dark with an n-700 edge), radius 10, n-50 text, holding a
  space's decision facts. It is the one heavy surface — every entry has exactly one.
- Panels for controls (the refine panel, menus, forms): white / n-900, radius 10, 1 px border, no shadow except
  floating menus (`0 12px 32px rgb(13 18 23/.12)`).
- **Radius:** 10 on panels and photos, 8 on controls, 999 status dot. No pills.

## The spark

A small spark **square** (8 px, the ة's dots' shape from the logo) marks what matters now: before «مفتوحة الآن» /
«متاح» in a fact box and an entry line, before today in the week, at the start of the current chapter in the chapter
index, and as the 3 px start edge of a running announcement. Never text, never an action.

## Imagery and art direction

- Photos are **plates in the entry**, never banners: 3:2 at the entry's start column width in lists (≈ 280 px at
  1440), radius 10, with a 13 px caption under the photo — the space's name and «صورة من المساحة» / "Photo from the
  space" (they are the space's own material; the caption says whose).
- A space's page shows its photos as a **spread**: one large (6/9 of the content) and the others stacked beside it,
  captioned; with one poster, the poster sits in the start column under the fact box.
- **No photo:** no frame at all — the entry simply has no plate and its text takes the width. A guide doesn't print
  empty frames.

## Iconography

Lucide, stroke 1.5, 18 px, sparing: search, sliders, map / list, locate, heart, WhatsApp-message, phone, instagram,
mail, navigation, chevrons, x. **No icons in the amenities** — they are set as a two-column list of words (the guide's
way). No icon on headings or the 404.

## Motion

One moment: on a space's page, the **standfirst sentence** fades in (opacity, 300 ms) after the name. Everything else
instant; the refine panel opens 200 ms ease-out (transform + opacity). Reduced motion: none.

## Density

Generous on reading pages (Home, a space, About, privacy); the directory's list is tighter: entries 160–180 px tall
desktop with the photo plate at the start, ~ 6 per 1440 screen with the chapter headings.

## Components

- **Buttons:** primary ink, 44 px, radius 8, Plex 500 15 px; secondary 1 px n-400; quiet = underlined text. In the fact
  box the primary inverts (n-50 fill, n-900 text).
- **Fields:** 44 px, radius 8, 1 px n-500, label above in `fact` 500.
- **The composed summary** (the entry's one sentence, from real data only, both languages): e.g. «مفتوحة الآن حتى
  18:00، في الرمال، ويبدأ سعرها من 30 ₪ لليوم.» — "Open now until 18:00, in Al-Rimal, from ₪30 a day." Built from:
  the state by the rules (live / by hours / «لا تتوفر حالة مباشرة»), today's closing time, the area, the lowest general
  price and its period (omitted if none). **Never** an adjective or claim not in the data.
- **The refine bar** (the directory): under the h1, one line — the search field (wide), «تنقيح» / "Refine" (opens the
  refine panel), the sort as a quiet select, «الأقرب إليّ», «قائمة | خريطة». **The refine panel** opens *under the bar,
  pushing the list down*, the four groups in four columns (desktop) — المنطقة · السعر · الدوام · أخرى — with «عرض N
  نتيجة» and «مسح الفلاتر» on its last line; phone: a full sheet. When closed, the active filters show as a sentence
  under the bar: «في الرمال والدرج، مفتوحة الآن، بسعر شهري بين 250 و400 ₪» with «مسح» — the guide's voice, not chips.
- **The chapter index:** in the directory's default order (and on Home), the spaces are grouped by governorate (north
  to south: شمال غزة · غزة · الوسطى · خان يونس · رفح, only those with spaces), each chapter's `h2` in the start column,
  sticky while its entries scroll (≥ 1024). When a sort other than the default is chosen, the chapters dissolve into
  one list.
- **Header:** 72 px, the logo 40 px at the start, the nav in Plex 15 px with the current page underlined in ink, the
  language and theme as quiet text buttons.
- **Footer:** the tagline set in Markazi `standfirst` («مساحة — دليل مساحات العمل المشتركة في قطاع غزة»), the links,
  the contact.
- **Map pins:** an 8 px spark square = open now / متاح; an amber square with the ممتلئ word in the legend; a hollow n-500
  square = closed; dashed = no live state; selected: 16 px with an ink ring and the name in a Markazi label. The map
  ground in a "printed map" style: land white / n-900, sea `i-50` / `i-950`, governorate
  names set along the Strip in Markazi. Production: a custom MapLibre style in these colours, bounded to the Strip.

## Every page's division

- **Home** — (1) **The cover:** the `display` h1 «اعثر على مساحة عمل في قطاع غزة» over the full width, the lead as a
  `standfirst`, the search field, and one live line «مفتوحة الآن: 6 من 13 مساحة» (computed by the rule; links to the
  directory filtered by «مفتوحة الآن»). (2) **«مفتوحة الآن»** — four entries (photo plate, name, composed sentence) in a
  two-column layout ≥ 1024. (3) **The chapters** — «تصفّح حسب المنطقة» as the guide's contents: each governorate a row
  (`h2` in the start column, its areas as links with counts in the content column), a spark square on the chapter
  with a space open now. (4) **For owners** — a short typeset paragraph with «تواصل معنا». Footer.
- **The directory** — the h1 «مساحات العمل» and a standfirst-sized count line («13 مساحة في قطاع غزة»); the refine
  bar; the chapters with entries (default order) or one list (other orders); pagination as text. `?filters=open`
  shows the refine panel open with شهر chosen.
- **The map** — the refine bar stays; the map below at full width and height, governorate names along the Strip; the
  selected entry as a panel at the map's bottom with the composed sentence.
- **A space's page** — an entry spread: (1) the breadcrumb (≥ 768), the name (`h1`, Markazi) with the other name in
  `fact` under it, the heart; the **composed sentence** as the standfirst; (2) ≥ 1024 the **fact box** in the start
  column (3/12, sticky): the state, today, the week's hours (seven lines), the lowest prices, WhatsApp and call,
  «الاتجاهات»; the content (9/12): the photo spread, the unverified notice (a quiet bordered paragraph, not a blue
  banner), announcements, «الأسعار» (a typeset table per audience with «للعرض فقط · الدفع في المساحة»), «المرافق» (two
  columns of words), «عن المساحة» (the space's own words in Markazi `standfirst` size, marked «بكلمات المساحة» /
  "In the space's words"), «الموقع» (the map plate and the address), the report link. Each section's «آخر تحديث …» in
  `meta` under its heading. Phone: name, sentence, fact box, then the rest; a bottom bar with WhatsApp and Call.
- **About** — an essay: the h1, the intro as a standfirst, the sections «من أين تأتي المعلومات؟» / «ماذا تعني
  الحالة؟» / «تواصل معنا» / «لأصحاب المساحات» with their headings in the start column; the states as a typeset
  definition list with the spark/amber/hollow/dashed squares; the owners' steps numbered (a real sequence).
- **Sign in** — the h1 «تسجيل الدخول» in Markazi at `h1`, the guide's tagline as a standfirst at the start column (≥
  1024), the form in the content column (max 440 px); no floating card — the form sits on the page.
- **Account** — the h1, the account nav as a start-column list (≥ 1024; a row on phone), the settings as a typeset
  form: each setting's label in the start column and its control beside it, rules between.
- **Favourites** — «المفضّلة» with a standfirst «المساحات التي حفظتها، بحالتها الآن.» (real copy), the entries list
  (same component as the directory), «الأقرب إليّ»; the left space as a muted entry with the line.
- **404** — the `display` «الصفحة غير موجودة», the sentence as a standfirst, then the chapter index (the five
  governorates with their counts) as the way back.

## Decisions this direction overturns

- **foundation §7 and §15 #2** (one font, Plex, settled) → Markazi Text for display, Plex for text (a proposal).
- **DECISIONS_PUBLIC U12** (the cover photo leading a striking card) → entries with a photo plate at the start, no
  card; no frame at all without a photo.
- **The Directory's filter sidebar from `lg`** (DECISIONS_SHARED P5's exception, DECISIONS_PUBLIC) → a refine panel
  that opens under the bar, and the active filters read back as a sentence.
- **The directory's default order** (the latest update first) **is shown grouped by governorate** (chapters) — the
  order within a chapter stays the latest update; a proposal for the owner (the API already returns the area and its
  governorate).
- **foundation §13, screen 1** → the cover, the open-now entries, the chapters.
- **The space page's order** (U8: status & contact first) → the name, the composed sentence and the fact box (which
  holds status and contact) first; the rest in U8's order.
- **The map's OSM default tiles** → a custom "printed" style bounded to the Strip.

## New copy (proposed)

The composed sentence's patterns, both languages (e.g. «مفتوحة الآن حتى {time}، في {area}، ويبدأ سعرها من {price}
{per}.» / "Open now until {time}, in {area}, from {price} {per}."; «مغلقة الآن، وتفتح {day} {time}.» / "Closed now; opens
{day} at {time}."; «ساعات عملها غير متوفرة.» / "Its hours aren't available.") · «مفتوحة الآن: {n} من {m} مساحة» / "Open
now: {n} of {m} spaces" · «تنقيح» / "Refine" · the active-filter sentence's patterns · «بكلمات المساحة» / "In the
space's words" · «صورة من المساحة» / "Photo from the space".

## Builder's notes

Decided while building, in the direction's spirit; none crosses COMMON.md's fixed points.

- **Two spark marks, not one.** A live «متاح» is a *filled* spark square; an unverified space that is open *by its
  hours* gets a spark *outline* square — still "what matters now", visibly weaker than a live state. Closed: hollow
  n-500; ممتلئ: amber; no live state: dashed n-500. The word is always beside the mark (sentence, fact box, pin label,
  legend). About's legend adds the by-hours row (new copy below).
- **A verified space with no live status** (Elevate Hub today) follows the live product: «لا تتوفر حالة مباشرة ·
  موثّقة»; its sentence states today's hours («تعمل اليوم 08:00–18:00، …») instead of a state. It still counts in
  «مفتوحة الآن» (the filter and the Home count go by the hours, as the live site does). A live state outside the
  opening hours reads «مغلق الآن».
- **The sentence's price** is the general price of the shortest period the space lists (its way in: «3 ₪ للساعة»);
  under a price filter, the filter's period.
- **Plates.** Posters are *mounted* on a mat (contain, never cropped — their logos stay whole); the space's own
  interior photos (coma-io-1, branch-hub-2/3) run full-bleed. Captions («برانش هاب · صورة من المساحة») stay on a
  space's page; in lists they are dropped and the plate is 216 px (home pairs 168 px), to hold entries near 180 px —
  the density the list asks for. The big plate of a spread takes the photo's own ratio (between 4:3 and 21:9).
- **The map turns to fit its frame**: the Strip lies along a wide frame (north-east to the right) and stands in a tall
  one; a north arrow and a km bar say so. Spaces closer than ~30 px gather in an ink square with their count (a spark
  corner if one is open); pressing it zooms to them. Zoom ± and «القطاع كاملًا», drag to pan. Sea is `i-100` (i-50 was
  indistinguishable from the land); the land beyond is n-200, unlabelled; رفح is labelled as geography although it has
  no spaces. The space page's location is the same drawing as a small locator plate.
- **Home when nothing is open:** the catalogue's empty-state words, then «تفتح قريبًا» — the four that open next,
  each with its sentence («مغلقة الآن، وتفتح غدًا 08:00، …»).
- **The dateline** (the day · the time «بتوقيت غزة» · «مفتوحة الآن: 6 من 13 مساحة») opens Home's cover and sits in the
  start column of sign-in and the 404 — the guide's "edition", always on Gaza's clock.
- **The refine panel's content:** a subscription alone keeps the spaces that have a general price of that period (as
  the API does); المنطقة lists only the areas that hold spaces, with their counts, grouped by governorate; the price
  sorts appear once a subscription is chosen; «الأقرب إليّ» sorts by distance (a simulated point in الرمال) and dissolves
  the chapters. Chapter headings are sticky from 1024.
- **The fact box** shows the week Saturday → Friday (Gaza's week), the today row marked; WhatsApp with its number;
  «اتصال» only when the space has a phone contact (none in today's data); other channels as text links.
- **Mock-up stand-ins:** the Google button is drawn (production renders Google's own); sign-in / Google set a local
  "signed in" flag and open the account (nothing is sent); `login.html?register=1` is the create-account form; «بلاغاتي»
  and the footer's privacy link are out of this round (the first opens the 404, the second is omitted).

### New copy (proposed) — added while building

«بتوقيت غزة» / "Gaza time" · «تفتح قريبًا» / "Opening next" · «{n} مفتوحة الآن» / "{n} open now" (a chapter's line) ·
«الحالة حسب ساعات العمل» / "Status by opening hours" · «تنقيح القائمة» / "Refine the list" · «كل المساحات» / "All
spaces" (the one list) · «القطاع كاملًا» / "The whole Strip" · «{n} مساحات هنا، اضغط للتقريب» / "{n} spaces here, press
to zoom in" · «لم تُضف مرافق بعد» / "No amenities added yet" · «لم تُضف وسائل تواصل بعد» / "No contacts added yet" ·
About: «للمساحات الموثّقة» / «لغير الموثّقة», and «مفتوحة الآن · مغلقة الآن — مساحة غير موثّقة نعرف ساعات عملها: نحسب من
ساعاتها إن كانت مفتوحة الآن بتوقيت غزة، دون أن نعرف إن كان فيها مكان.» · 404: «تصفّح الدليل من فصوله» / "Find your way
from the guide's chapters" · footer: «واتساب وبريد فريق مساحة» · the sentence's live patterns: «فيها مكان الآن، ومفتوحة
حتى {time}» / "Has room now, open until {time}", «ممتلئة الآن، ومفتوحة حتى {time}» / "Full right now, open until
{time}", «تعمل اليوم {range}» / "Open today {range}" · the filter sentence: «{n} مساحات مطابقة — في الرمال والدرج، مفتوحة
الآن، بسعر شهري بين 250 و400 ₪.» · the illustrative demo announcement «تمديد ساعات العمل حتى 22:00 طوال الأسبوع».

### Round 2 (the lead's improvement round)

- **The Arabic display face is Amiri, not Markazi.** In the captures the Arabic headlines, names and sentences were
  rendering in the Plex fallback: Markazi's Arabic did not reach headless Chrome through the css2 link (its Latin
  faces did), so the direction's memorable thing was not real. I switched the Arabic display to **Amiri** (Google
  serves its Arabic subset; a classic book Naskh with real calligraphic contrast) via `:root[lang="ar"]`, and kept
  **Markazi Text for the English display** (its Latin rendered correctly). This overturns this document's single
  display face: Markazi still says it in English, Amiri says it in Arabic; Plex informs in both. Retuned for Amiri:
  display and h1 at weight 400 (Amiri's regular is the elegant cut at size), h2/names at 700 (the browser's match for
  600), Arabic line heights display 1.5 · h1 1.55 · h2/entry 1.6 · standfirst 1.85 · sentence 1.7–1.8 so the
  descenders and the dots clear the next line.
- **The map is north-up**, always: fitted by scale and centring, the sea and the Strip only (no grey land beyond — it
  read as other territory). The extra width at ≥ 1024 holds an aside: the selected entry's panel, «تصفّح حسب المنطقة»
  (the whole Strip and each governorate, which zoom the map to their spaces) and the legend. On the phone the panel
  overlays the map's foot and the aside follows below. The map frame has a fixed height (680 / 520 px) so it never
  depends on the viewport. This supersedes the "map turns to fit its frame" note above.
- **The directory is denser:** the plate is 144 px at 1440 (132 at 768, 96 on the phone), the entry's padding 16 px,
  the state line («الحالة حسب ساعات العمل») sits beside the name instead of under the sentence, and chapters are 56 px
  apart with a rule — about six entries per 1440 screen once the page head has scrolled.
