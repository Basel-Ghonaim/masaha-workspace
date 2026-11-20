# Round 3 — the diagnosis: why Masaha reads as AI-made

> The design lead, 2026-11-14. Seen on the **live site** (https://masaha-omega.vercel.app, read only, paced) for every
> public page, and on **app-dr** (`18b03798`, ports 5336/3336, the demo user) for the signed-in pages. 134 captures in
> `before\` (390 and 1440; Arabic, and English for Home, the directory, a space, sign-in and the account; light and dark;
> viewport and full page), each with a JSON of measured facts beside it. Lenses run: `ui-review`, `web-review`,
> `design-critique`, `anti-slop`, `ui-compare` (no UXKIN: the comparisons are from named real products I know, not
> from a library), plus `frontend-design`, `typography`, `spacing`, `surfaces`, `page-patterns`, `viewports`, `motion`.
> This is my judgement, not their checklists.

## The verdict in one paragraph

Masaha is **correct, accessible and honest — and has no point of view.** It is shadcn/ui's default kit with the
brand's two colours dropped in: every surface is the same white rounded card with a 1 px border and a soft shadow;
one typeface at one weight (600) carries every heading; most of what a person actually reads is set at 13 px; every
section of every page has the same weight; the spark, the identity's one memorable colour, appears almost only as a
pink "selected" tint. Nothing on any page could only belong to *a directory of places to work in Gaza today*. Take the
logo off and Home is any SaaS template's "Find X in Y" page. That sameness — not any single defect — is what people
with design experience read as "made by AI". The product's real strengths (truthful live state, hours on Gaza's clock,
the electricity and internet facts, WhatsApp as the way in) are present in the data and almost invisible in the design.

## The tells, named

Each is concrete and measured on the captures (frames named as `before\<page>-<width>-<lang>-<theme>`).

1. **One card for everything.** 678 rounded corners on the measured light Arabic frames, all 6 or 8 px (`radius-md` /
   `radius-lg`), plus 89 pills. The space card, the area tile, the owners' banner, the settings sections, the sign-in
   form, the prices, the "status & contact" panel and the About explainer are the same object: white, bordered,
   rounded, padded 20 px. Hierarchy is impossible when the frame never changes (`home-1440-ar-light.full`,
   `account-1440-ar-light.full`, `about-1440-ar-light.full`).
2. **A timid, flat type scale.** Measured on the light Arabic frames: **13 px is the most used size (522 text
   elements)**, then 14/500 (309), 17/600 (169), 12 px (145); the 15 px body only 136. The card's area line, its
   hours, the freshness notes, the helper texts — the facts people come for — are 12–13 px grey. Every heading is
   weight 600; there is no display voice. The sign-in, register, forgot, reset, forced-change and 404 pages have an
   **h1 of 17 px** (a card title promoted to h1). Body line height is 1.8 — airy for running Arabic, but on the short
   UI lines that dominate the site it adds height without rhythm.
3. **The hero cliché.** Home opens with a left/right-aligned headline, a grey sub-line and a search box with a button
   («اعثر على مساحة عمل في قطاع غزة» · «بحث»), on a blank ground — the "Find X in Y" hero every template ships. No
   image, no place, no live moment. The one thing that could open the page — *what is open right now, near you* —
   is the second section, drawn exactly like everything else (`home-1440-ar-light.full`).
4. **Every section the same weight.** Home is: hero → six identical cards → eight identical area tiles, each with the
   same arrow icon → a tinted call-to-action box. The directory is: title → toolbar → identical cards. The space page
   is: gallery → name → a blue info banner → prices in three bordered boxes → a table → pills → paragraph → map →
   link. Nothing is allowed to be bigger, darker, denser or quieter than its neighbour. No rhythm, no density change.
5. **The spark has no job you can see.** ADR 0019 gives the berry "what matters now". On the live pages it is the logo's
   two dots, a pink selected pill («قائمة» / «خريطة»), the sidebar's current item and the hours table's **today row,
   filled pink across its full width** (`space-1440-ar-light.full`). Open now — the thing that matters now — is a grey
   12 px pill («مفتوحة الآن») indistinguishable from «لا تتوفر حالة مباشرة».
6. **Other people's posters are the art direction.** 10 of the 13 live covers are the spaces' social-media posters —
   logos, slogans, phone numbers, English and Arabic display fonts — and only Coma's and two of Branch's photos are
   real interiors. Dropped at full card width, edge to edge, they make the directory a wall of thirteen competing
   brands; Masaha's own identity disappears under them (`spaces-1440-ar-light.full`, `home-1440-en-dark`). There is no
   imagery rule: the same crop takes a logo or a room.
7. **The map opens on the wrong place.** The directory's map starts at a regional zoom: the Strip is a sliver on the
   left, the pins are tiny dashed rings, and most of the frame is the sea and **Hebrew place names** of the default
   OpenStreetMap tiles (`map-1440-ar-light`). For a Gaza product this reads unfinished, and worse. The tiles are the
   default OSM style on both themes — no colour, no Arabic-first labelling, no relation to ink and berry.
8. **Icons as decoration.** An arrow on every area tile, a magnifier-in-a-circle on the 404, an icon on every amenity
   pill, checks inside selected pills. They add count, not meaning (`anti-slop`: "decoration, not structure").
9. **Template empty states and auth.** The 404 is the stock "icon in a tinted circle + title + two buttons" in the
   middle of an empty page (`404-390-ar-light`). All five auth pages are a 448 px card floating in an empty viewport,
   the same as every shadcn starter (`login-1440-ar-light`). Nothing says Masaha or Gaza.
10. **The phone is a long scroll of screens.** Home at 390 is 3,890 px for six spaces and eight areas — each card
    nearly a full screen (`home-390-ar-light.full`); the directory is 5,133 px for 13 spaces. A person on a phone
    (most of the audience, often on a weak connection) scrolls a screen per space to compare three facts.
11. **No photo, no character.** A space without a photo becomes a centred letter on a grey slab
    (`favorites-1440-ar-dark`): five of them in a row look like a loading state.
12. **Settings as stacked cards of equal weight** (`account-1440-ar-light.full`): profile, preferences, sign-in methods,
    each the same box; the save button in the first box only; language and theme as pink pills. The account area's
    side nav repeats «حسابي» as a header and the four items as plain links.

What is **not** a tell: the copy. It is specific, plain and true («ساعات العمل والأسعار والحالة المباشرة لمساحات
العمل المشتركة، في مكان واحد.», «جمع فريقنا هذه المعلومات، ولم تؤكّدها إدارة المساحة بعد»). Keep its voice; the
design under it is the problem. Also not a problem: accessibility basics (no page overflows at 390 or 1440, focus
rings exist, contrast is held by the token tests), and the truth rules (no counts, no ratings).

## Page by page — what it is for, what the user needs first, what it does instead

| Page | For | Needs first | Does instead |
|---|---|---|---|
| **Home** | Get a person from "I need a place to work" to a space they can go to now | What's open now near me, and how to see all | A generic hero + search; the open spaces as six full cards; eight look-alike area tiles; an owners' box |
| **Directory — list** | Compare spaces on the few facts that decide: open now, where, today's hours, price, power/internet | A scannable list: state, name, area, today, price, at a glance | A grid of poster cards, 3 columns; the facts as 13 px grey under a large image; the filters in a bordered sidebar card |
| **Directory — filters** | Narrow by place, budget, hours | Few, clear choices, the result count | A correct but plain stack (segmented control, checkboxes); on the phone a sheet whose rows are 112 px apart — the panel is longer than its content warrants (`spaces-filters-390-ar-light`) |
| **Directory — map** | Where are they, which is near me | The Strip, filling the frame; states legible as pins | The region, Hebrew labels, dashed specks |
| **A space's page** | Decide to go: open now? today's hours? price? power/internet? how to reach them? | One block with state + today + price + WhatsApp, then the rest | Gallery first, name under it, a heavy blue notice, three price boxes, a table, pills, a map; the decision facts split between a short side card and the long main column (the side card ends a third down, leaving the column empty) |
| **About** | Trust: where the data comes from, what the states mean, how owners join | The verified/unverified idea, the states, the contact | A centred text column with two cards and a legend box; the contact buttons repeated twice |
| **Privacy** | Read a policy | Readable long text | Fine as text; same plain column, nothing to navigate it by |
| **Sign in / register / forgot / reset / forced change** | Get in quickly | The form, trust that it is Masaha | A starter-kit card; h1 at 17 px; nothing of the brand beyond the header logo |
| **Account (إعدادات حسابي)** | Change name, language, theme, password | Each setting where expected | Three equal cards; pills for settings |
| **Favourites (المفضّلة)** | Return to my spaces, see their state now | State and today's hours of my saved spaces | The directory's card grid again; letter slabs where photos are missing |
| **404** | Recover | A way back to the spaces | The stock empty state |

## The design system — what it lacks to carry a strong product

`docs/frontend/design-system/foundation.md` is careful about colour, contrast, RTL and accessibility — and almost
silent about everything that makes a design *look like someone*:

- **Type.** One family (IBM Plex Sans Arabic 400/500/600) for Arabic and Latin, composite styles from *Sea*: display
  44 (phone 30, but Home's phone h1 measures 24), h1 30, h2 22, h3 17, body 15/1.8, body-sm 13, caption 12. The steps
  from 13 to 17 are small and many; there is no display voice and no contrast between reading text and UI text. Plex
  Sans Arabic is a good text face, but neutral by design — alone, it guarantees a neutral site. Latin at 1.8 line
  height (English mode) is loose; foundation §7 anticipated tightening it, which never happened.
- **Spacing and grid.** "Layout is not tokenised" (§4): a gutter, two gaps, a section spacing and a hero padding as
  guidance. No column grid, no measure for prose, no rule for density changes, no vertical rhythm. So every page
  invents the same 24/56 rhythm.
- **Surfaces and elevation.** One `card` surface, one `card-border`, three shadows. No second surface family (a band,
  an inset, an ink panel), so the only way to group is another card.
- **Radius.** A single soft scale (4/6/8/12) applied to everything — the "SaaS-card kit" signature.
- **Imagery.** No rule at all: no ratio by context, no treatment of posters vs photos, no no-photo state with
  character, no map style. The map tiles are outside the system entirely.
- **Iconography.** Lucide, used everywhere as a prefix. No rule for when an icon carries meaning.
- **Motion.** Two durations and an easing; nothing designed. Fine as restraint, but there is no single moment.
- **Density.** One density (comfortable, 40/44 px controls) for a site whose core job — comparing places — wants a
  denser mode.
- **The spark.** Specified as a role with careful rules, but no component gives it its job ("what matters now") — so it
  ends up as the selected tint, which is the one place users notice it least.

## Compared with real products (`ui-compare`, without UXKIN)

From my own knowledge of these products' public pages; no page was fetched for this round.

| Product | What it does that Masaha does not |
|---|---|
| **Google Maps** (place lists, place sheet) | The list row leads with the *state*: "Open · Closes 6 PM" in colour, then the distance; the place sheet's first block is name → state → the four action buttons (directions, call, website, save). Dense, scannable, the photo a supporting thumbnail. |
| **Airbnb** (search) | Photo-led cards with a strict ratio and one line of facts; at desktop the **list and the map side by side**, the map pins carrying the one number that matters (price). A strong, single display voice (Cereal) across UI. |
| **Citymapper / transit boards** | Time and state as large numerals, everything else small; colour reserved for live state. The board metaphor: rows, not cards. |
| **Workfrom / Croissant / Deskpass** (coworking discovery) | The amenities that decide work (Wi-Fi speed, outlets) promoted to the card; the space page's first screen answers "can I work here today". |
| **Talabat / Careem** (Arabic-first apps) | Arabic display type with weight and size contrast; phone-first density — cards of 120–160 px height in a list, not full-screen tiles; sticky filter bars. |
| **Thmanyah (ثمانية)** (Arabic editorial) | A typographic identity: a custom Arabic display face, large confident headlines, generous measure, and a clear editorial rhythm. Proves an Arabic site can feel authored, not assembled. |
| **Almosafer / Booking.com** | A filter rail that is a real tool (counts per option, collapsible groups), a sort bar that reads as a sentence, a results header that says what you are looking at. |

**What most of them share:** a **single strong idea of what the user needs first** (state, price, photo or time),
pushed to the top of every card and every page; **density** on lists; **one display voice**; colour **reserved for
one meaning**. Masaha has the data for all four and uses none.

## What follows

Three directions (`directions\A`, `B`, `C`), each a different answer to *what does this person need first, and how
should it feel*: **A — the live board** (state-first utility, rows not cards), **B — the Strip** (place- and
map-led, the Strip's shape as the identity's second mark), **C — the guide** (editorial and typographic, the
spaces as entries of a guide by governorate). All three keep ink + berry, the logo, Arabic first, v1 and the truth
rules (R3-14).
