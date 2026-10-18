# R2-PU-VD — The public site · Visual design and consistency

- `HEAD`: `34a6c59aab049e8f2992b29b88c8a700b926ddba`
- `origin/main`: `34a6c59aab049e8f2992b29b88c8a700b926ddba` (equal — review ran on `origin/main`)
- Served `docs/design/prototype` on `http://127.0.0.1:5409` (headless Chromium); phone evidence captured at 500 px (see §6: identical phone breakpoint).

## Verdict

The public site is visually coherent — hierarchy, grid, tokens, dark resolution and all shared patterns hold; four small consistency defects remain.

## Five most important points

1. `PriceGrid` leaves orphan cells whenever a count is not a multiple of four (Focus Hub's month price sits alone).
2. Galleries with 2–3 photos offer no explicit photo-viewer affordance; the «view all photos» pill appears only at four or more.
3. The price filter's four period chips wrap 3+1 in the sidebar and the sheet.
4. About teaches the four live states with badges while the map speaks in dots — the two keys are never paired.
5. Everything else on this axis verified: one h1 per page, card order, U8 section order, `xl` three-column grids, in-map legend, below-`lg` asides, U4 freshness lines, U9 grids, U2 location states, dark theme.

## Issues

### R2-PU-VD-001 — Price grid leaves an orphan cell on an incomplete last row

- **type:** improvement · **level:** pattern · **impact:** low
- **where:** §04 «Focus Hub · verified, متاح, fresh, 5 photos, location allowed — desktop 1440», `http://127.0.0.1:5409/Space details.html?id=focus&loc=granted`, 1440 light AR, `docs/design/screens/04-space-details-variants/01-focus-hub-verified-fresh-5-photos-location-allowed-desktop-1.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\PU-VD\R2-PU-VD-001.png` (same orphan in dark: `e3-space-dark-1440.png`)
- **what is wrong:** `PriceGrid` is `grid-cols-2 md:grid-cols-4`. Focus Hub publishes five general prices, so the month cell sits alone on a second row at one-quarter width. The same happens for every non-multiple count: ZM Hub's three prices (3+gap on desktop, 2+1 on a phone), Number One's two student prices (half-empty row on desktop). Prices are the page's key comparison content; the lone cell reads as unfinished and gives that period less visual weight for no reason.
- **proposal:** keep one grid per audience (U9), but let the cells of an incomplete last row share the row's full width (each spans an equal share of the remaining columns). Applies to `PriceGrid` wherever it renders: the general and student grids and the per-shift tab panels on every `Space details` variant.
- **why it is better:** every published price keeps equal prominence and the grid stays calm at every count, with no per-space special case. Built from the existing grid and tokens; no new component.
- **cost:** S
- **rule:** foundation §5 (spacing scale rhythm); U9 applied (grid per audience kept).

### R2-PU-VD-002 — Price period chips wrap 3+1 in the sidebar and the sheet

- **type:** improvement · **level:** component (`PriceField` in `Directory.html`) · **impact:** low
- **where:** §03 «List — desktop 1440», `http://127.0.0.1:5409/Directory.html?loc=none` (also `?loc=none&area=nasr,rimal&period=day&priceMax=20`, §53 place-and-price frame), 1440 light AR, `docs/design/screens/03-directory-views-states/01-list-desktop-1440.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\PU-VD\R2-PU-VD-002.png`
- **what is wrong:** the four period chips (ساعة · يوم · أسبوع · شهر) flow as a wrapping row, so the ~300 px sidebar (and the phone sheet) shows three chips plus a lone «شهر» on a second row. The wrap orphan reads as a broken row rather than one four-way control.
- **proposal:** lay the four chips out as an even 2×2 block (`grid-cols-2`) inside `PriceField`, so sidebar and filter sheet show the same intentional block. One fix covers both places (same component).
- **why it is better:** an even block scans as a single control with four equal choices; nothing changes about what the filter does (U5 untouched).
- **cost:** S
- **rule:** foundation §5; U5 applied.

### R2-PU-VD-003 — About's status legend never pairs badges with the map's pin marks

- **type:** improvement · **level:** page (`About.html`) · **impact:** low
- **where:** §10 «About «عن مساحة» — desktop 1440», `http://127.0.0.1:5409/About.html`, 1440 light AR, `docs/design/screens/10-about-error-pages/01-about-desktop-1440.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\PU-VD\R2-PU-VD-003.png` (map key for comparison: `c1-map-selected-1440.png`)
- **what is wrong:** About's «ماذا تعني الحالة؟» teaches the four states with `Badge` pills (success / warning / neutral / muted text), while the Directory map speaks only in pin dots (filled / filled-with-bar / hollow / dashed hollow). The encoding matches (same four states, same colours) but a visitor who learns the badges gets no help recognising the dots, and vice versa — the same job (reading a live state) learned twice.
- **proposal:** prefix each About legend term with its pin mark, reusing the same `PinMark` component the map legend uses; keep the badge beside it. About is the only page that changes.
- **why it is better:** one learned key transfers to the map — recognition instead of recall — while each surface keeps the treatment its size needs (badges in text, dots on the map).
- **cost:** S
- **rule:** U6 applied (shape *and* colour, identical in the legend — extended to the page that explains them); U11 applied.

### R2-PU-VD-004 — Galleries below four photos have no explicit viewer affordance

- **type:** improvement · **level:** component (`Gallery` in `space-parts.jsx`) · **impact:** low
- **where:** §04 «Number One Hub · closure banner, مغلق الآن, 2 photos — desktop 1440», `http://127.0.0.1:5409/Space details.html?id=numberone&loc=none&lang=en`, 1440 light EN, `docs/design/screens/04-space-details-variants/09-number-one-hub-closure-banner-2-photos-desktop-1440.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\PU-VD\R2-PU-VD-004.png` (the pill present at five photos: `a4-space-focus-1440.png`)
- **what is wrong:** the «عرض كل الصور (n)» pill renders only when four or more photos are shown, so 2–3-photo galleries (Number One, Branch) are plain tiles with no explicit sign they open the lightbox, while 5-photo galleries get a clear entry point. Same action, different affordance by photo count.
- **proposal:** render the same pill on the first tile whenever a space has more than one photo, at the same position and in the same style; single-photo galleries stay as they are (nothing further to open).
- **why it is better:** the viewer is equally discoverable on every space page; the established pill, position and lightbox are reused unchanged.
- **cost:** S
- **rule:** REVIEW_LENS §3 B.4 (the same job done the same way everywhere).

## Decisions in doubt

None. The settled decisions hold up on this axis: the priceless striking card (covers lead, order photo → name → area → state → hours → distance exact on every card), the per-audience price grids, the shape-and-colour pins identical in the legend, and the dark theme as a full resolution (map, cover art, pins, badges and price cells all resolve in dark rather than invert).

## What was not reviewed and why

- True 390 px renders: this reviewer's headless Chromium has a 500 px layout floor, so phone evidence was captured at 500 px. By code the phone layout is identical at 390 and 500 (no rule below the `md` breakpoint touches a PU page; the only sub-768 rule in `masaha.css` is the charts' tick rule), and the 2:1 cover ratio was verified there.
- Map at 768: same `isTablet` branch as the verified 1440 overlay (floating card, in-map legend); the phone sheet branch was verified at 500.
- Home dark, EN dark, About/Error phone and desktop mirrors: dark was verified on the hardest surfaces (map illustration, gallery cover art, price cells, pins, badges); EN was verified on the space page; About/Error share one centred column whose responsive button and legend rules were verified on the captured pages.
- Full `?state=loading` / `?state=error` skeletons beyond `?photos=loading`: the skeleton cards mirror `SpaceCard` slot for slot (verified in code and in the loading-covers capture).
- Anything outside the VD axis (UX flow and feedback, DF breakage/overflow/mirroring/console, EX removals, CP wording/translation, AX focus/names/contrast/targets/order, TR API/counts/privacy) — left to the sibling PU prompts.
- The stray `<<<<<<< HEAD` line before `INDEX.md` §54 — recorded by the analyst, not reported.
- Server stopped after the review; port 5409 answers nothing.
