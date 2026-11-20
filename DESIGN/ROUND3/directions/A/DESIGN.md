# Direction A — «اللوحة» · The live board

> **The idea:** Masaha is a live board of where you can work in Gaza right now — the state first, in rows, the way a
> departures board or Google Maps' list answers "can I go now?" before anything else.
>
> **Point of view:** a utility, proud of being one. Density, alignment and big numerals instead of cards and
> pictures. The spark finally does its job: it marks what is open *now*. The memorable thing is **the board** — an ink
> panel with the time in Gaza and the spaces as rows, on Home, at the top of a space's page, and beside the forms.
>
> **Learns from:** Google Maps' place list (state and closing time first, photo as a thumbnail), Citymapper and
> transit/airport departure boards (time and state as large tabular numerals, colour only for live state), Linear's
> density and alignment discipline, Talabat's phone-first list density.
>
> **Keeps the typeface** (IBM Plex Sans Arabic) — this direction proves that the timidity was the system, not the font.

## Type

One family: **IBM Plex Sans Arabic** (Google Fonts), 400 / 500 / 600, for Arabic and Latin. Numerals
`font-variant-numeric: tabular-nums` everywhere a time, price or distance appears (columns must align).

| Style | Desktop | Phone | Line height (ar / en) | Weight | Use |
|---|---|---|---|---|---|
| `board-time` | 56 px | 40 px | 1.1 | 500 | The time in Gaza on the board; today's hours on a space's board |
| `display` | 48 px | 32 px | 1.25 / 1.15 | 600 | Home's h1, a space's name |
| `h1` | 36 px | 28 px | 1.3 / 1.2 | 600 | Page titles |
| `h2` | 22 px | 20 px | 1.45 / 1.3 | 600 | Section titles |
| `row-title` | 18 px | 17 px | 1.4 / 1.3 | 600 | A space's name in a row |
| `body` | 16 px | 16 px | 1.75 / 1.55 | 400 | Running text, values |
| `secondary` | 14 px | 14 px | 1.6 / 1.45 | 400 / 500 | A row's facts, labels |
| `meta` | 12 px | 12 px | 1.5 / 1.4 | 400 | Freshness, captions, legal — **never a row's main facts** |

Hierarchy by size and position, not by more weights. No all-caps, no eyebrows above headings, no tracked labels.

## Grid and spacing

- **Spacing:** a 4 px base; steps 4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96. Inside a component 4–16; between groups
  24–32; between page sections 64 (phone 48).
- **Grid:** content max 1200 px at 1440 (gutters 32; phone 16; 768: 24), 12 columns, 24 px gaps.
- **The row grid** (the core layout): a space row is a CSS grid with named columns, in reading order —
  `state-bar (4px) · plate (64px; phone 56) · name+area (1fr) · today (minmax(140px,auto)) · price (minmax(110px,auto)) ·
  save (44px)`. At ≤ 767 px it folds to two lines: plate · name+area · save on the first, state word · today · price under
  the name. Rows are 80 px tall desktop, ~96 px phone — **six spaces fit one phone screen and a half**.
- Prose measure: 68ch max.

## Surfaces and elevation

- **Ground** n-50 (dark n-950). **The board:** an ink panel — light theme **n-900** with n-50 text and n-400/n-300
  secondary text (verify ≥ 4.5:1), dark theme **n-900** on the n-950 ground with an n-800 edge. The board holds a
  header line (the time in Gaza, the count of spaces open now) and rows of its own (row separators n-800).
- **Lists outside the board:** one white (dark n-900) container, radius 12, 1 px n-200 (dark n-800) border, rows
  separated by 1 px n-200 hairlines — **no card per row, no shadow per row**.
- Shadows only for floating things (menus, the filter sheet, the map's selected sheet): `0 12px 32px rgb(13 18 23 / .14)`;
  dark: none, an n-700 edge instead.
- **Radius:** containers 12, controls 8, plates 8, the state dot 999. Nothing else rounded.

## The spark

The spark's one job here: **"open now / available now"**. A 4 px vertical **state bar** at the row's inline start
(spark for متاح and for an unverified «مفتوحة الآن»; amber `a-500` fill with its bar *and* the word ممتلئ; n-300
hollow for closed; dashed n-400 for no live state), and the 8 px dot before the state word. Today's row in a week of
hours: a spark bar at its start, never a full tint. The selected filter option: `s-100` tint plus a spark edge. The
spark never sits on a button, link or text.

## Imagery

- **Posters are signs, so they become plates:** in rows, a 64 px (phone 56) square plate, `object-fit: cover`
  centred, radius 8, 1 px n-200 inner edge. A logo-poster reads as the space's sign — which is what it is.
- **On a space's page:** a filmstrip under the board — photos at 4:3, 280 px tall desktop (phone: a horizontal
  scroll-snap strip, 220 px), the cover first, «عرض كل الصور (3)» opens a simple lightbox. A real interior photo
  (Coma, Branch 2–3) gets the first, larger slot (2× width) when it exists.
- **No photo:** the plate shows the first letter of the shown name, `row-title` size, n-700 on n-100 (dark n-200 on
  n-800) — small, so it reads as an initial, not a broken image.

## Iconography

Lucide, stroke 1.75, 20 px in rows and controls, 16 px inline. Only functional: search, filters, map/list, location
(near me), heart, WhatsApp-message/phone/instagram/mail, navigation (directions), chevron in a row's end on touch,
external link. **No icon on headings, area links, amenities lists, or empty states.** Amenities: a two-column list of
words, each with its Lucide icon at 16 px in n-600 — the one place a small icon helps scanning.

## Motion

Instant by default. One moment: **the board's minute tick** — when Gaza's minute changes, the time's digits
cross-fade (150 ms, opacity only) and any row whose state changed swaps its bar (150 ms). Menus and the filter sheet:
200 ms ease-out in, 150 ms ease-in out, transform + opacity only. `prefers-reduced-motion`: no transitions.

## Density

Comfortable controls (44 px on touch, 40 px mouse), dense lists (rows 80 / 96 px). A filter panel is a compact form:
group labels in `secondary` 500, options 40 px rows.

## Components

- **Buttons:** primary = ink fill (n-900 / dark n-50), 44 px, radius 8, label 15 px 500; secondary = 1 px n-300 border
  on transparent; quiet = text with underline on hover. On the board (ink ground) the primary inverts: n-50 fill with
  n-900 text. Focus: 2 px ring in `ring` + 2 px offset (on the board: n-50 ring).
- **Fields:** 44 px, 1 px n-500 border, radius 8, label above in `secondary` 500; search field with the magnifier.
- **Segmented control** (subscription; language and theme in settings): one bordered track, the chosen segment
  white/n-900 with a 2 px spark edge at its block end — selected = tint + edge, never hover's n-200.
- **Checkbox rows** for الدوام / أخرى, 40 px rows, the whole row the target.
- **The state badge** (outside the bar): dot + word, `secondary` 500, no pill.
- **Header:** 64 px, white/n-950 with a bottom hairline; logo 40 px; nav as text links with a 2 px ink underline for
  the current page; the language switch and theme switch as quiet icon+text buttons; «تسجيل الدخول» secondary.
- **Footer:** an ink band (n-900, both themes) — the tagline, the links, the platform contact as a line.
- **Filter panel:** desktop ≥ 1024: a sticky rail at the inline *start* (right in RTL), 300 px, no card around it, a hairline separating it from the list. Phone: a bottom sheet with the
  count button «عرض 13 نتيجة».
- **Map pins:** a 12 px dot with a 2 px white ring, the state's shape as in U6 (filled spark = متاح/open now, filled
  amber with a bar = ممتلئ, hollow n-400 = closed, dashed = no live state); the selected pin grows to 20 px with an ink
  ring and its name label (a small ink tag). The map ground: land n-100 / sea blue-50 (dark: land n-900, sea
  blue-950), governorate borders n-300 hairlines, area names in `meta`. Production equivalent: a muted vector tile
  style in these colours (MapLibre with a custom style), fitted to the Strip.

## Every page's division

- **Home** — (1) **the board**, full width under the header: «الآن في غزة 13:42» (`board-time`, live), the h1
  «اعثر على مساحة عمل في قطاع غزة» (`display`) and the lead, the search field (inverted on ink), then the rows of the
  spaces open now (state by hours or live), «الأقرب إليّ» on the board's header line, «عرض الكل» at its end. (2) **By
  area** — not tiles: a compact two-level index, each governorate a heading with its areas as a list of links with
  their counts (`secondary`), in 3 columns desktop, 1 on phone. (3) **For owners** — one line with the action, on the
  ground, not a tinted box. Footer.
- **The directory (list)** — title «مساحات العمل» + the count line; a sticky toolbar: search, «الفلاتر» (phone),
  sort, «الأقرب إليّ», «قائمة | خريطة»; the filter rail (≥ 1024) and the rows container; pagination as «1–13 من 13».
  `?filters=open` at 1440 shows the rail with a subscription chosen (شهر) and the range visible.
- **The map** — the toolbar stays; the SVG map fills the frame below it (desktop: 100vh − header − toolbar); the
  legend inside the map's top-end corner as rows; selecting a pin opens its row (the same component) as a floating
  panel at the map's bottom; phone: a bottom sheet with the row.
- **A space's page** — (1) **the space's board** (ink): breadcrumb (≥ 768), the name (`display`) and the other
  language's name under it, the area; then three columns of facts: **الحالة** (the state word with its bar + «الحالة
  مباشرة الآن» or the hours-based line), **اليوم** (today's hours in `board-time`, or «مغلقة اليوم»), **السعر** («من
  30 ₪ / يوم» — the lowest general day price, else the first period's), and the actions: WhatsApp (primary,
  inverted), call, «الاتجاهات», the heart. (2) The unverified notice as one line under the board with «هل تدير هذه
  المساحة؟ تواصل معنا». (3) The filmstrip. (4) Two columns ≥ 1024: the start column (8/12) — announcements, prices (a
  table: period · general · students), hours (the week as seven rows, today with the spark bar), amenities, about;
  the end column (4/12) — a sticky **contact & location** panel: contacts as rows with their values, the small SVG map
  with the pin, «الاتجاهات», the address. Each section's «آخر تحديث …» as `meta` beside its heading. (5) The report
  link. Phone: one column in this order; a bottom bar with WhatsApp and Call.
- **About** — the h1 and intro at 68ch; **«من أين تأتي المعلومات؟»** as a two-column comparison (verified ·
  unverified) in one container with a hairline between; **the states** as the real row component with each state's bar
  and its sentence; «تواصل معنا» and «لأصحاب المساحات» side by side (≥ 1024), the owners' steps as a numbered list (it is
  a real sequence).
- **Sign in** — two columns ≥ 1024: the form (start, 440 px) and the board (end) showing «الآن في غزة» with the open
  rows (live data, not decorative); phone: the form only under a slim ink strip with the time. h1 «تسجيل الدخول» at
  `h1` size.
- **Account (إعدادات حسابي)** — the account nav as a horizontal tab row under the h1 (المفضّلة · بلاغاتي · إعدادات حسابي),
  then one settings form in **label column (4/12) + control column (8/12)** rows separated by hairlines: الاسم,
  البريد الإلكتروني, اللغة (segmented), المظهر (segmented, «حسب الجهاز» default), كلمة المرور («تغيير»), each with
  its helper; «حفظ» only on the name row.
- **Favourites (المفضّلة)** — the same tab row; the saved spaces as board-style rows (on the ground container, not
  ink) with their states; «الأقرب إليّ»; the left space as a muted row with «لم تعد هذه المساحة معروضة في الدليل» and
  «إزالة».
- **404** — the board with one row: «الصفحة غير موجودة» with «ربما تغيّر الرابط أو حُذفت الصفحة.» and the actions,
  then the open-now rows below («مفتوحة الآن») so the way back is content, not a button pair.

## Decisions this direction overturns

- **foundation §7** — the type scale (display 44 → 48/56 board numerals; body 15 → 16; body-sm 13 for facts → 14;
  line height 1.8 → 1.75 ar / 1.55 en). The family stays.
- **foundation §4–§5** — "Layout is not tokenised" → a grid, a spacing scale and the row grid as tokens; `card-padding`
  and the one-card-for-everything surface → lists in one container with hairlines; radius used on containers and
  controls only.
- **DECISIONS_PUBLIC U12** (2026-10-11/12: "the cover photo at the top of the card … the card must be striking (the
  photo leads)") → the photo becomes a 64 px plate in a row; the striking element is the state and the board.
  Home, the directory and favourites lose the card grid.
- **foundation §13, screen 1** (Home: "hero with search, quick area filters") → the board leads; the area tiles become
  an index.
- **The hours table's today row** in the selected tint (`accent`) → a spark bar.
- **The map's OpenStreetMap default tiles** → a muted style in the identity's neutrals, fitted to the Strip.
- **DECISIONS_ACCOUNT C6** (account nav as a side list) → a tab row under the h1.

## New copy (proposed)

«الآن في غزة» / "Now in Gaza" (the board's clock) · «{n} مفتوحة الآن» / "{n} open now" (the board's count, by the real
rule) · «اليوم» / "Today" and «السعر» / "Price" as the space board's column labels · «من 30 ₪ / يوم» / "From ₪30 / day".

## Builder's notes

Decisions the builder took where this document left something open or met a fixed point, in its spirit (2026-11-14).

- **Live vs by-hours on the same bar.** COMMON §1 asks for a *neutral* badge for an unverified space's state by its
  hours. So the spark keeps its job ("open now") but in two weights: a **filled** spark bar and dot = a live state
  (متاح); a **hollow** spark bar and ring = «مفتوحة الآن» by hours. The word is always ink, never tinted, so the badge
  stays neutral; the reader sees at a glance which "open" is live. Closed = hollow n-400; no live state = dashed
  n-400; full = amber fill. The legend (map) and About's state board show all five.
- **A state column in the row.** The row grid above has no place for the state word on desktop; the built row is
  `bar · plate · name+area · state · today · price · save`, with a quiet column-header line (المساحة · الحالة · اليوم ·
  السعر) on lists ≥ 1024 — the board's columns. Below 1024 (not only ≤ 767) the row folds to two lines: at 768 the
  seven columns did not fit.
- **The row's price.** The day's general price, else the first period's (hour → month); while a subscription is
  chosen in the filters, that period's price. No price = an en dash (the words «لم تُضف أسعار بعد» for screen
  readers), hidden on the phone's folded row.
- **A verified space's live state is closed outside its hours** (the server derives it so); the demo states apply
  within opening hours only. Elevate Hub (verified, no capacity) keeps «لا تتوفر حالة مباشرة», as live.
- **After hours the board is not empty.** With nothing open, Home, sign-in and 404 say «لا توجد مساحات مفتوحة الآن»
  (catalogue) and list the spaces by when they next open — «تفتح غدًا 08:00» — computed from the real week.
- **The spark on the ink board** is s-400 (the dark theme's spark), in both themes: the board is a dark ground.
- **Posters in the filmstrip are not cropped**: a poster sits whole (contain) in a 16:9 frame on the muted ground; a
  real interior photo fills a 4:3 frame, the first one an 8:3 (2×) slot. In 64 px plates posters are cropped square
  as this document says, with a per-space focal point so the mark stays in (Al-Salam, Masahat, Masar Tech, Branch…).
- **The map.** No governorate borders are drawn: `_shared` has no source for them and an approximate administrative
  line on a Gaza map is a truth risk; the four governorates the product lists are labelled inside the Strip
  instead. Pins closer than 22 px merge into an ink count circle (a count of spaces, real) that zooms in on press.
  Land n-50 on a blue-100 sea (light) — n-100 on blue-50 was too close to read the coast; dark: n-900 on blue-950.
- **The directory opens with an ink band** (title + Gaza's clock + the open count), so every public page that lists
  spaces starts with the board's voice; the toolbar under it is on the ground and sticky.
- **The theme switch in the header is an icon button** with its name as label and tooltip (the language switch
  keeps icon + text); in the phone menu both are written out.
- **The space's board at 768**: status and today side by side, the price on its own line under them (today's hours
  at 44 px), since three columns broke the 56 px numerals.
- **Areas index** in four columns (one per governorate the product has), two at 768, one on the phone.
- **Account.** «بلاغاتي» and «سياسة الخصوصية» / «إنشاء حساب» / «نسيت كلمة المرور؟» are outside the eight pages; their
  links show a small note instead of a dead page. The Google button stands in for Google's own rendered button
  («المتابعة باستخدام Google» is Google's text, not the catalogue's).
- **Filters' area groups** start collapsed (each governorate with its count), so price, hours and other show on one
  screen; zero-count areas stay selectable, in the muted colour.

### New copy (proposed, as built)

- «الآن في غزة» / "Now in Gaza"; «{n} مساحة مفتوحة الآن» with Arabic plural forms / "{n} spaces open now".
- «تفتح لاحقًا» / "Opening next"; «تفتح {اليوم|غدًا|السبت} {08:00}» / "Opens {today|tomorrow|Saturday} {08:00}".
- «من {30 ₪} / {يوم}» / "From {₪30} / {day}"; column labels «المساحة · الحالة · اليوم · السعر» / "Space · Status · Today ·
  Price" (اليوم and السعر exist in the catalogue).
- «{n} مساحات متقاربة، تكبير» / "{n} spaces close together, zoom in" (the map's cluster, read by screen readers).
- Illustrative (demo states only): «تمديد ساعات العمل حتى 22:00 طوال الأسبوع» / "Opening hours extended to 22:00 all
  week".
