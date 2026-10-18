# Design review 3 — the public site (Home, Directory, Space details, About, errors)

Reviewer: design-review-public · 2026-10-10 · read-only
Source: `git archive origin/main docs/design` (49cd088), served on `http://127.0.0.1:5342/`.
Evidence: `C:\Users\basel\Downloads\design-review-public\PU-0nn.png` (one per issue). Captured with
headless Chrome at 390 (touch emulated: `pointer: coarse`), 768 and 1440, Arabic and English, light
and dark. Sources read: `shared.jsx`, `space-parts.jsx`, `map.jsx`, `location.jsx`, `data.js`,
`details-data.js`, `Home.html`, `Directory.html`, `Space details.html`, `About.html`, `Error.html`.

## 1. Summary

1. **The directory cannot show the Gaza Strip.** The governorate is a single mandatory choice that
   defaults to Gaza City, so every other governorate reads «لا توجد مساحات تطابق الفلاتر», and the
   planned `GET /spaces` has no governorate filter at all (PU-001).
2. **The filter bar is missing the price and mislabels what it has.** There is no price range
   (foundation §13, `priceMin`/`priceMax`), and the period chips sit under «مدة الاشتراك» — a
   subscription term for a public price, on a site where «يومي» is a visit, never a subscription
   (PU-002).
3. **A space has two names.** The list, the map pins, the breadcrumb and the page title use the
   English name; the page's h1 uses the Arabic one. The Arabic name is also not searchable, and an
   English-only space would render an empty h1 (PU-003).
4. **Near me breaks exactly where it is needed.** Placing a pin by hand is pointer-only — no
   keyboard path — and its «إلغاء» wipes a location the visitor already had. On a phone the
   selected card covers half the map and the legend falls below the fold (PU-004, PU-005).
5. **Three statements on the public pages are not true to the product.** The live status carries an
   «آخر تحديث» the data model has no field for, the unverified notice invents «آخر مراجعة», and
   About explains the live status as something the space updates by hand (PU-008, PU-009, PU-015).
   Separately, the About page names the university on a public page (PU-006).

Counts — **29 issues**: by level, 1 design system · 1 pattern · 1 component · 26 page. By impact,
**6 high**, **13 medium**, **10 low**. By type, 20 defects · 9 improvements.

## 2. Patterns (proposals that change more than one page)

Each is built from foundation §12 components. None needs a new design-system component.

### P-A · Place is one filter, and the directory covers the Strip (PU-001, PU-018)
- The directory's default set is **every publicly listed space in the Gaza Strip**; the count line
  reads «6 مساحات في قطاع غزة».
- **Governorate and area are one control**, not two: a `Combobox` (`multiple`) whose options are the
  areas, grouped by governorate, with the governorate's name as the group label. Its trigger
  summarises («المنطقة: 2 محددة»). Choosing a whole governorate is choosing its areas. Nothing is
  selected by default, and the sent filter is the `area` list the API already plans.
- A governorate with no active areas simply has no group, instead of an empty page.
- Home's «تصفّح حسب المنطقة» stops showing one governorate's areas: it shows the areas that have
  spaces, each with its governorate underneath, and «كل المناطق» as the last card.
- **Pages:** Directory (list and map), Home.

### P-B · One «الأقرب إليّ» control, one state line (PU-004, PU-005, PU-018)
- The control is a `Button` labelled «الأقرب إليّ», `aria-pressed`, in the **same place on every
  public page that uses a location**: beside the results count on Home and on the Directory (both
  views). It leaves the sort list, which keeps only «الأحدث تحديثًا · الأقل سعرًا · حسب الاسم»;
  turning the location on sets the sort to distance and says so.
- Under it, one `LocationStatus` line in all four states (locating, in use, denied, imprecise), with
  the same two fallbacks everywhere — «حدّد موقعي على الخريطة» and «اختر منطقتك» — and the privacy
  line. On Home «اختر منطقتك» opens Home's own area section, not another page's sheet.
- Turning it off says what goes: «إيقاف الترتيب حسب المسافة».
- **Pages:** Home, Directory list, Directory map, Space details (the distance line).

### P-C · One name for a space, everywhere (PU-003)
The space's **display name is the Arabic name when it exists, otherwise the English one**, in the
page's language, with the other name beneath it only on the space page. The card, the map pin, the
breadcrumb, the document title, the favourites list and the report dialog all use the display name.
The directory's search matches **both** names and the area name.
**Pages:** Directory (cards, pins, selected card), Home (cards), Space details, Favourites.

### P-D · One freshness rule (PU-008, PU-009, PU-020)
- **Freshness belongs to a fact group**, never to the live status: each section (hours, prices)
  carries its own «آخر تحديث …», relative («قبل 3 أيام»), and the `warning` «قد يكون تغيّر» badge
  only where the group is stale. The live status shows the state alone.
- An **unverified** space shows the same relative form in its notice («آخر تحديث للمعلومات قبل 4
  أشهر»), from the profile group's date — not an absolute «آخر مراجعة: 2 يونيو 2026».
- The display-only sentence «للعرض فقط · الدفع في المساحة» appears **once per page**, in the prices
  section (SH-021 settled the list's copy).
- **Pages:** Space details, Directory and Home cards.

## 3. Issues

### PU-001 · The directory shows one governorate at a time, and defaults to Gaza City
- **type:** defect · **level:** page · **impact:** high
- **where:** Directory — desktop 1440 · `Directory.html?loc=none&gov=khanyounis` ·
  `screens/03-directory-views-states/19-no-results-desktop-1440.webp` (the same empty state)
- **evidence:** `PU-001.png`
- **what is wrong:** `applyFilters` requires `s.gov === f.gov`, and `initialFilters` sets
  `gov: 'gaza'`. There is no "all governorates" option, and `clearedFilters` resets to Gaza City. A
  visitor in Khan Younis, Rafah or the Middle Area is told «لا توجد مساحات تطابق الفلاتر» for a
  directory that is meant to cover the Strip, and the heading counts «6 مساحات في محافظة غزة». The
  governorate is also not a filter the planned `GET /spaces` accepts (v1-mvp › Public directory
  lists `area` only), so the screen cannot be served as drawn.
- **proposal:** P-A.
- **why it is better:** the visitor sees the whole directory first and narrows it by choice; the
  screen asks the API only for what the API offers.
- **cost:** M
- **rule:** `docs/plans/v1-mvp.md` › *Public directory*; `docs/project/overview.md` › *Public site*;
  foundation §13 (*Directory*: «filters: area…»).

### PU-002 · No price filter, and the price period is labelled «مدة الاشتراك»
- **type:** defect · **level:** page · **impact:** high
- **where:** Directory — desktop 1440 · `Directory.html?loc=none` ·
  `screens/03-directory-views-states/01-list-desktop-1440.webp`; Filters sheet — phone 390 ·
  `Directory.html?loc=none&sheet=filters`
- **evidence:** `PU-002.png` (the filter panel), `PU-002b.png` (the phone toolbar)
- **what is wrong:**
  - **No price range.** foundation §13 and the planned `GET /spaces` (`priceMin`, `priceMax`) both
    have one; the panel has none. For a student choosing between 14 ₪ and 30 ₪ a day, price is the
    first filter, and the only way to compare is to read every card.
  - **«مدة الاشتراك»** names a public price period with the glossary's word for a multi-day
    arrangement, and offers «يومي», which BRIEF.md forbids as a subscription («a same-day visit is
    a visit, never a member»). The chips also do not filter by price; they filter by *which periods
    the space publishes*.
  - **The sort has no visible name.** The trigger reads «الأحدث تحديثًا» alone, beside a button
    called «الفلاتر», so it reads as another filter (`PU-002b.png`).
  - **«متاحة الآن فقط» and «المساحات الموثّقة فقط» overlap:** an unverified space never has a live
    state, so the first switch implies the second.
- **proposal:**
  - A **«السعر»** `Field`: a period `ToggleGroup` (`single`: ساعة · يوم · أسبوع · شهر) and, under
    it, min and max `Input`s (`dir="ltr"`, ₪), sending `period` + `priceMin`/`priceMax`. Its helper
    says the period picked is the one the range applies to.
  - **«أسعار للطلاب»** stays in «أخرى» as it is.
  - The sort trigger reads «الترتيب: الأحدث تحديثًا».
  - «متاحة الآن فقط» moves next to «المساحات الموثّقة فقط» under one label «المساحات» with a note
    that available-now covers verified spaces only.
- **why it is better:** price is the question the directory exists to answer, and the words stop
  promising a subscription the public site does not sell.
- **cost:** M
- **rule:** foundation §13 (*Directory*); `docs/project/glossary.md` (*Subscription*, *Visit*);
  v1-mvp › *Public directory*.

### PU-003 · A space is named two ways, and the Arabic name cannot be searched
- **type:** defect · **level:** pattern · **impact:** high
- **where:** Space details — desktop 1440 · `Space details.html?id=focus&loc=granted` ·
  `screens/04-space-details-variants/01-focus-hub-verified-fresh-5-photos-location-allowed-desktop-1.webp`;
  Directory list (cards and pins) · `Directory.html?loc=none`
- **evidence:** `PU-003.png`
- **what is wrong:** the space page's h1 is `LANG === 'en' ? space.name : space.nameAr`
  («فوكس هاب»), while `SpaceCard`, the map pin, the compact card, the breadcrumb and
  `document.title` all use `space.name` («Focus Hub»). An Arabic visitor is shown one name in the
  list and another on the page. `nameAr` is not even loaded on the Directory and Home
  (`details-data.js` is only on the space page), so the search matches the English name alone —
  typing «فوكس» finds nothing. And since the data model makes the Arabic name **optional** (the
  English one is required), a space without `nameAr` renders an empty h1.
- **proposal:** P-C.
- **why it is better:** one name is one space. A visitor who searched for a name finds the page they
  expected, and no page can render nameless.
- **cost:** S
- **rule:** `docs/architecture/data-model.md` › *Bilingual content* (a space's name: English
  required, Arabic optional); lens A10.

### PU-004 · On a phone the selected card covers half the map, and the legend is below the fold
- **type:** improvement · **level:** page · **impact:** high
- **where:** Map · marker tapped — phone 390 · `Directory.html?view=map&selected=focus&loc=none` ·
  `screens/01-flow/03-3-directory-map-marker-tapped.webp`
- **evidence:** `PU-004.png`
- **what is wrong:** the map is `calc(100svh - 17rem)` ≈ 570 px at 390, and the selected card is
  laid over its bottom edge, taking about 250 px of it. In the capture, two of the six pins sit
  behind the card, so tapping one pin hides others — on a map whose job is to compare places. The
  legend, the only key to the pin colours, is rendered *under* the map and never appears without
  scrolling. With tens of spaces, named pins will also overlap: three labels already collide at 390.
- **proposal:**
  - The selected card becomes a **bottom `Sheet`** (`side="bottom"`, the existing component) at a
    fixed small height: name, area, state, hours, distance and «عرض التفاصيل», with the map still
    panning behind it; the map re-centres the selected pin above the sheet.
  - The **legend moves into the map** as one caption row pinned to its top-end corner (where
    «موقعي» sits), or above the map, so it is always in view.
  - Pins carry the **name only when there is room**: a dot-only marker by default, the name on the
    selected one and on hover. (The real OpenStreetMap layer handles the rest with zoom.)
- **why it is better:** the map keeps being a map while a space is selected, and the only key to its
  colours is where the colours are.
- **cost:** M
- **rule:** foundation §9 (*Directory, at every width*); foundation §12 (`Sheet` `bottom`).

### PU-005 · Placing a pin by hand is pointer-only, and cancelling it erases the location you had
- **type:** defect · **level:** page · **impact:** high
- **where:** Manual pin · picking — phone 390 · `Directory.html?view=map&loc=picking` ·
  `screens/03-directory-views-states/14-manual-pin-picking-phone-390.webp`
- **evidence:** `PU-005.png`
- **what is wrong:**
  - The pin is placed by a **click on the map layer** (`SpaceMap.pick`). In picking mode every pin
    is `tabIndex={-1}` and nothing else is focusable inside the map, so a keyboard user cannot place
    a pin at all. The manual pin is one of the two documented fallbacks when a location cannot be
    used, which leaves "choose your area" as the only keyboard path — and the instruction card never
    says so.
  - The card's dismiss calls `near.clear()`, which sets the location to `idle`. A visitor who
    already had a GPS or manual location, tapped «تغيير الموقع» and then changed their mind **loses
    the location they had** and the distance sort with it.
  - The «موقعي» button stays live while picking, so two ways of setting a location are offered at
    once.
- **proposal:**
  - Picking shows a **fixed centre crosshair** and a primary «ثبّت الموقع هنا» button in the
    instruction card: the pin is placed at the map's centre, so a keyboard, a screen reader and a
    thumb all reach it. Tapping the map still works.
  - The dismiss (named «رجوع» per P9) **returns to the previous location**, whatever it was; only
    «مسح موقعي» clears one.
  - «موقعي» is hidden while picking.
- **why it is better:** the fallback for a visitor whose location failed stops being unreachable for
  anyone who cannot tap precisely, and backing out of a change stops being destructive.
- **cost:** M
- **rule:** foundation §10 (full keyboard use, every control named); foundation §13 (*Near me*
  fallbacks); P9 (dismiss is «رجوع»).

### PU-006 · The About page names the university on a public page
- **type:** defect · **level:** page · **impact:** high
- **where:** About «عن مساحة» — desktop 1440 · `About.html` ·
  `screens/10-about-error-pages/01-about-desktop-1440.webp`
- **evidence:** `PU-006.png`
- **what is wrong:** the last line of the public About page reads «مشروع تخرّج — جامعة القدس
  المفتوحة، فرع غزة». Masaha is presented to visitors and to space owners as a product; naming the
  university (and the fact that it is a graduation project) on the page that establishes the
  product's credibility works against both, and the owner's rule is that the university is never
  named publicly.
- **proposal:** the line goes. If a line about who runs Masaha is wanted, it says it in product
  terms — «فريق مساحة — غزة» — or nothing at all.
- **why it is better:** an owner deciding whether to hand their space's data to Masaha reads this
  page.
- **cost:** S
- **rule:** the owner's rule on the project's public identity.

### PU-007 · The space page answers «كم السعر؟» last, and hides the announcements at the bottom
- **type:** improvement · **level:** page · **impact:** medium
- **where:** Space details — phone 390 · `Space details.html?id=focus&loc=granted` ·
  `screens/04-space-details-variants/02-focus-hub-verified-fresh-5-photos-location-allowed-phone-390.webp`
- **evidence:** `PU-007.png`
- **what is wrong:** the phone order is photos → name → status & contact → **عن المساحة → ساعات
  العمل** → الأسعار → المرافق → الموقع → **الإعلانات** → report. The price is about 1,100 px down,
  below a description and a weekly table; a visitor deciding between spaces scrolls past the two
  things they already know (it is a workspace; it is open) to reach the one they do not. The
  announcements — a workshop, an offer, a closure — are the most time-bound thing on the page and
  sit last, below a map, while the closure announcement alone is pulled to the very top as an Alert.
- **proposal:** one order at every width: **status & contact → الإعلانات (when there are any) →
  الأسعار → ساعات العمل → المرافق → عن المساحة → الموقع → الإبلاغ**. The closure Alert stays at the
  top (it changes whether to go at all). On desktop the aside is unchanged; the content column
  follows the same order.
- **why it is better:** the page answers "can I go now", "what is happening there", "what does it
  cost", "when is it open" in the order a person asks them.
- **cost:** S
- **rule:** lens B1, B8.

### PU-008 · The live status carries an «آخر تحديث» the data model has no field for
- **type:** defect · **level:** page · **impact:** medium
- **where:** Space details — desktop 1440 · `Space details.html?id=focus&loc=granted` ·
  `screens/04-space-details-variants/01-focus-hub-verified-fresh-5-photos-location-allowed-desktop-1.webp`
- **evidence:** `PU-008.png`
- **what is wrong:** `StatusLine` prints «متاح · آخر تحديث قبل 5 دقائق» from `statusUpdated`.
  Freshness in the data model belongs to the five **fact groups** (profile, hours, prices,
  amenities, contacts); the live status is derived at request time from the hours, the closure
  announcements, the manual override and the open check-ins, and `GET /spaces/:slug/occupancy`
  returns `{ status }` and nothing else. A timestamp beside it tells the visitor the opposite of
  the truth — that someone last touched the state five minutes ago and it may now be stale.
- **proposal:** the status shows the state alone. Where the visitor needs reassurance, the caption
  says what the state is, not when it was set: «الحالة مباشرة الآن» for a verified space, and the
  existing «الحالة المباشرة تظهر للمساحات الموثّقة فقط» for the rest (P-D).
- **why it is better:** the one fact on the page that is always current stops being dated.
- **cost:** S
- **rule:** ADR 0008 (live status is a state); data-model › *Derived values* (*Live status*),
  › *Freshness*.

### PU-009 · The unverified notice shows «آخر مراجعة», a field the model has not, in another date form
- **type:** defect · **level:** page · **impact:** medium
- **where:** Golden Hub · unverified, stale price, no photos — desktop 1440 ·
  `Space details.html?id=golden&loc=none` ·
  `screens/04-space-details-variants/07-golden-hub-unverified-stale-price-no-photos-desktop-1440.webp`
- **evidence:** `PU-009.png`
- **what is wrong:** the notice ends «آخر مراجعة: 2 يونيو 2026» from a `lastReview` field. The data
  model has no such field: an unverified space has the same five group dates as any other, and the
  admin's «المعلومات ما زالت صحيحة» resets one of them. It is also the only absolute date on a page
  where every other date is relative («قبل 4 أشهر»), so two freshness statements on one page cannot
  be compared. The notice is an `info` `Alert` with no title, and its action — «هل تدير هذه
  المساحة؟ تواصل معنا» — sits outside it as a loose link.
- **proposal:** the notice reads «جمع فريق مساحة هذه المعلومات ولم تؤكدها إدارة المساحة بعد · آخر
  تحديث للمعلومات قبل 4 أشهر», from the profile group's date, in the relative form (P-D); the
  contact link becomes the Alert's `AlertAction`.
- **why it is better:** one way of saying how old a fact is, and one block that holds the statement
  and its one action.
- **cost:** S
- **rule:** data-model › *Freshness*, *Derived values* (*Stale*, *Missing*).

### PU-010 · The report dialog promises that the Masaha team will handle it
- **type:** defect · **level:** page · **impact:** medium
- **where:** Signed in · report wrong info — phone 390 ·
  `Space details.html?id=focus&loc=none&auth=1&dialog=report` ·
  `screens/04-space-details-variants/16-signed-in-report-wrong-info-phone-390.webp`
- **evidence:** `PU-010.png`
- **what is wrong:** the dialog says «يراجع فريق مساحة البلاغ ويحدّث الصفحة» for every space. A
  report about a **verified** space goes to its owner («بلاغات البيانات» in the owner's dashboard);
  only the reports of unverified spaces are resolved by the admin. The reporter is also told the
  page will be updated, which no one can promise, and the resolution they will later read is
  labelled «ردّ إدارة المساحة» or «ردّ فريق مساحة» depending on who answered — a distinction the
  dialog erases.
- **proposal:** the description names the reader, from the space's verification:
  verified → «يصل البلاغ إلى إدارة المساحة، وتجد ردّها في «بلاغاتي»»;
  unverified → «يراجع فريق مساحة البلاغ، وتجد الردّ في «بلاغاتي»».
- **why it is better:** the reporter knows who is reading and where the answer will appear.
- **cost:** S
- **rule:** `docs/project/overview.md` › *Dashboard* (*Data reports*) and *Admin dashboard*;
  foundation §13, screen 11.

### PU-011 · A student price can only ever be a month
- **type:** defect · **level:** page · **impact:** medium
- **where:** Number One Hub · closure banner, مغلق الآن, 2 photos — desktop 1440 ·
  `Space details.html?id=numberone&loc=none` ·
  `screens/04-space-details-variants/09-number-one-hub-closure-banner-2-photos-desktop-1440.webp`
- **evidence:** `PU-011.png`
- **what is wrong:** `PriceGrid` takes one `student` number and draws one «شهر» cell under
  «للطلاب», in a four-column grid whose other three cells stay empty. The card does the same with a
  single `studentMonth`. The data model gives every price an **audience** (general or student), an
  optional **shift** and an optional **custom label**, for any of the four periods — a student day
  price, or «شهري — الوردية الصباحية», has nowhere to go, and a custom label is never shown.
- **proposal:** one `PriceGrid` component rendered once per audience: «الأسعار» then «للطلاب», each
  a grid of the periods that audience publishes; a price with a custom label shows the label in
  place of the period name. The directory card keeps its four fixed general cells and gains one
  «للطلاب» line only when a student price exists, as it does now.
- **why it is better:** the page can show the prices a space actually publishes, which is the whole
  point of the price section.
- **cost:** S–M
- **rule:** data-model › *Prices*; BRIEF.md («price may be for students or a shift»).

### PU-012 · The map says a space's state with a 10 px dot, and the selected pin loses it
- **type:** defect · **level:** page · **impact:** medium
- **where:** Directory · map — desktop 1440 · `Directory.html?view=map&selected=focus&loc=none` ·
  `screens/03-directory-views-states/03-map-marker-tapped-desktop-1440.webp`; AR dark ·
  `&theme=dark` · `screens/11-variants/10-directory-map-ar-dark-desktop-1440.webp`
- **evidence:** `PU-012.png`, `PU-012b.png` (dark)
- **what is wrong:**
  - A pin's state is a 10 px coloured dot — success, warning, muted or an outline — and so is the
    legend's key. Nothing but hue separates «متاح» from «ممتلئ», which foundation §5 forbids
    («Status is never colour alone»); only the `aria-label` carries the word.
  - The **selected** pin is filled `primary`, and its `bg-success` dot disappears against it (both
    themes). Selecting a pin removes the one thing it was telling you.
  - Pins are **29 px tall** at 390 — the only controls on the public pages under the 44 px touch
    minimum.
- **proposal:**
  - Each state gets a **shape as well as a colour**: filled dot (متاح), filled dot with a bar
    (ممتلئ), hollow dot (مغلق الآن), dashed hollow dot (لا تتوفر حالة مباشرة) — the same four marks
    in the legend, which keeps its words.
  - **Selected** is shown by a `primary` ring and a raised shadow on the pin, not by filling it, so
    the state mark survives.
  - The pin's hit area is at least 44 × 44 on touch (padding around the mark, as the layer does for
    Calendar days).
- **why it is better:** the map is readable without colour vision and keeps working when you tap it.
- **cost:** S–M
- **rule:** foundation §5 (*Status is never colour alone*), §10 (44 × 44 on touch).

### PU-013 · The list/map switch is a tab list with no tab panels
- **type:** defect · **level:** component · **impact:** medium
- **where:** Directory — phone 390 · `Directory.html?loc=none` ·
  `screens/01-flow/02-2-directory-list.webp`; all Directory frames
- **evidence:** `PU-013.png`
- **what is wrong:** the «قائمة | خريطة» switch is a `Tabs`/`TabsList`, but the list and the map are
  rendered outside it: the page has `role="tablist"` with **zero** `role="tabpanel"` (measured in
  the accessibility tree). A screen-reader user is told they are on a tab that controls nothing, and
  the arrow-key model of a tab list does not match a control that swaps the whole page and the URL
  (`?view=map`). `Tabs` is also already in use on this site for a real tab set — the per-shift
  prices on the space page — so the same component means two things.
- **proposal:** the view switch becomes a `ToggleGroup type="single"` (the layer's filter chips),
  inside a `Field` labelled «طريقة العرض» (label visually hidden), with the two options as pressed
  states. `Tabs` stays for real panels.
- **why it is better:** the control announces what it is, and one component keeps one meaning.
- **cost:** S
- **rule:** foundation §12 (`Tabs`, `ToggleGroup`), §10; lens A5.

### PU-014 · The favourite sits far from the name, and is missing from the list
- **type:** improvement · **level:** page · **impact:** medium
- **where:** Space details — desktop 1440 · `Space details.html?id=focus&loc=granted` ·
  `screens/04-space-details-variants/01-focus-hub-verified-fresh-5-photos-location-allowed-desktop-1.webp`
- **evidence:** `PU-014.png`
- **what is wrong:** the heart is pushed to the far end of the content column by
  `justify-between`, about 620 px from the title it belongs to at 1440; it reads as a stray control
  in the middle of the page. And a visitor can only save a space by **opening** it: `SpaceCard`
  already supports an overlaid heart (`reserveEnd`, used on Favourites) but neither the Directory
  nor Home passes it, so saving six candidates means six page loads on a weak connection.
- **proposal:** the heart sits beside the name (`gap-3`, right after the h1 block, not at the far
  end), and `SpaceCard` is rendered with `reserveEnd` and a heart on the Directory and Home for a
  signed-in visitor; a signed-out one gets the existing sign-in dialog. The toast follows P9
  («تراجع»).
- **why it is better:** the control is next to the thing it acts on, and shortlisting happens where
  the comparing happens.
- **cost:** S–M
- **rule:** foundation §13, screen 10; P9.

### PU-015 · About explains the live status as something the space updates by hand
- **type:** defect · **level:** page · **impact:** medium
- **where:** About «عن مساحة» — desktop 1440 · `About.html` ·
  `screens/10-about-error-pages/01-about-desktop-1440.webp`
- **evidence:** `PU-015.png`
- **what is wrong:** the page whose job is to explain the states says «متاح: فيها أماكن شاغرة الآن،
  **حسب آخر تحديث من إدارة المساحة**» and, in the verified card, «**وتغيّر** حالتها المباشرة خلال
  اليوم». For a verified space the state is derived automatically — from the opening hours, an
  active closure announcement and the people currently checked in — and the manual override is the
  exception, for a set time. As written, a visitor reads the state as a claim someone typed, which
  is exactly the doubt the feature exists to remove.
- **proposal:** «متاح» reads «فيها مكان الآن، وتُحدَّث الحالة تلقائيًا من حركة الحضور في المساحة»;
  «مغلق الآن» keeps its hours-and-closure sentence; the verified card says «تحدّث إدارة المساحة
  ساعاتها وأسعارها وإعلاناتها، وتظهر حالتها المباشرة تلقائيًا، ويمكنها ضبطها يدويًا لفترة قصيرة».
- **why it is better:** the explanation matches the rule, so the state is believable.
- **cost:** S
- **rule:** ADR 0008; data-model › *Derived values* (*Live status*).

### PU-016 · A visitor has no «تواصل معنا»; the footer link lands in the owners' section
- **type:** defect · **level:** page · **impact:** medium
- **where:** About «عن مساحة» — desktop 1440 · `About.html#owners` ·
  `screens/10-about-error-pages/01-about-desktop-1440.webp`
- **evidence:** `PU-016.png`
- **what is wrong:** screen 4 is «About / Contact — contact email and WhatsApp», but the only
  contact block on the page is inside «لأصحاب المساحات», after three steps about verifying a space.
  Every «تواصل معنا» on the site — the footer of all five public pages, and Home's card — points at
  `About.html#owners`. A visitor with a question, or a person whose report was never answered, is
  sent to a section addressed to someone else.
- **proposal:** a «تواصل معنا» section of its own before «لأصحاب المساحات», holding the platform's
  WhatsApp and email (`GET /settings/public`) and one line about what to write about; the owners'
  section keeps its three steps and its own buttons. The footer and Home point at `#contact`.
- **why it is better:** the one page that offers contact offers it to the people reading it.
- **cost:** S
- **rule:** foundation §13, screen 4; v1-mvp (`GET /settings/public`).

### PU-017 · Home's «تواصل معنا» leads nowhere
- **type:** defect · **level:** page · **impact:** medium
- **where:** Home · default — desktop 1440 · `Home.html?loc=none` ·
  `screens/02-home-states/01-default-desktop-1440.webp`
- **evidence:** `PU-017.png`
- **what is wrong:** the «هل تدير مساحة عمل؟» card's button is `<a href="#">`: it reloads the top of
  Home. It is the only call to action aimed at space owners on the site's busiest page, and the one
  that brings new verified spaces into the directory.
- **proposal:** it points at the new `About.html#owners` steps (PU-016), or opens the same
  `PlatformContactDialog` the space page uses for «هل تدير هذه المساحة؟». One of the two, used in
  both places.
- **why it is better:** the product's growth path stops being a dead link.
- **cost:** S
- **rule:** lens B3 (no dead ends).

### PU-018 · Home shows one governorate's areas, and its location fallback leaves the page
- **type:** improvement · **level:** page · **impact:** medium
- **where:** Home · location denied — phone 390 · `Home.html?loc=denied` ·
  `screens/02-home-states/06-location-imprecise-phone-390.webp` (same block, imprecise)
- **evidence:** `PU-018.png`
- **what is wrong:**
  - «تصفّح حسب المنطقة» renders `M.governorates[0].areas` — Gaza City's three areas — under the
    subtitle «محافظة غزة». Home silently narrows the Strip to one governorate, and there is no
    «عرض الكل» for the areas.
  - When a location cannot be used, «اختر منطقتك» navigates to `Directory.html?sheet=filters` —
    away from a page that is already showing area cards two sections below.
  - The alert's title «تعذّر تحديد موقعك. اختر منطقتك من الفلاتر.» carries the instruction, and the
    buttons under it repeat it; the Alert has no description.
- **proposal:** P-A for the area cards. The alert's title becomes «تعذّر تحديد موقعك»; its
  description «اختر منطقتك أو حدّد موقعك على الخريطة لنرتّب المساحات حسب المسافة»; on Home
  «اختر منطقتك» moves focus to the area section instead of leaving the page.
- **why it is better:** the fallback is answered on the page the visitor is already on, and Home
  stops implying that Masaha covers Gaza City only.
- **cost:** S–M
- **rule:** foundation §13 (*Home*, *Near me*); lens B3.

### PU-019 · A Switch inside a Field is a 36 × 20 target, and its label does not activate it
- **type:** defect · **level:** design system · **impact:** medium
- **where:** Directory — desktop 1440 and Filters sheet — phone 390 ·
  `Directory.html?loc=none&sheet=filters` ·
  `screens/03-directory-views-states/22-filters-sheet-phone-390.webp`
- **evidence:** `PU-019.png`
- **what is wrong:** measured in the page, the Switch is **36 × 20 px** on touch as on desktop,
  against foundation §10's 44 × 44 minimum — the only layer control that does not grow with
  `--control-height` (which the layer does raise to 44 px under `pointer: coarse`). `Field
  orientation="horizontal"` puts the label at the start and the switch at the far end, about 200 px
  apart at 1440, and the label is a `<label for>` pointing at a `<button role="switch">`, which the
  browser cannot activate — so the whole row looks tappable and only the small switch is. The
  accessible name itself is correct.
- **proposal:** `Switch` keeps its 36 × 20 drawing and gains a hit area of at least 44 × 44 (padding
  or a pseudo-element), and `Field` makes the whole horizontal row the switch's label by wiring
  `aria-labelledby` and a click on the label row to the control.
- **why it is better:** every on/off filter and setting in the product becomes tappable with a thumb
  and with a careless click.
- **cost:** S
- **rule:** foundation §10 (44 × 44 on touch; every control has a programmatic label); §12
  (`Field`, `Switch`).

### PU-020 · «للعرض فقط» and «الاتجاهات» each appear twice on the space page, in two wordings
- **type:** defect · **level:** page · **impact:** low
- **where:** Space details — desktop 1440 · `Space details.html?id=focus&loc=granted` ·
  `screens/04-space-details-variants/01-focus-hub-verified-fresh-5-photos-location-allowed-desktop-1.webp`
- **evidence:** `PU-020.png`
- **what is wrong:** the status & contact card ends «للعرض فقط · **الدفع والاشتراك** في المساحة» and
  the prices section ends «للعرض فقط · الدفع في المساحة · آخر تحديث قبل يومين» — the same promise,
  twice, with a different verb, one of them nowhere near a price. «الاتجاهات» is likewise a button
  in the card and again beside the «الموقع» heading. On a phone the card and the fixed bottom bar
  also both carry contact actions, so «الحالة والتواصل» holds only the *secondary* channels while
  the phone and WhatsApp live in the bar — a card whose title promises more than it shows.
- **proposal:** the display-only line appears once, in «الأسعار», in BRIEF.md's wording
  («للعرض فقط · الدفع في المساحة»). «الاتجاهات» appears once, in «الموقع». On a phone the card is
  renamed «الحالة» and keeps the status, today's hours and the distance; every contact channel sits
  in one «التواصل» block above the report link, with the bottom bar repeating only WhatsApp and
  Call.
- **why it is better:** each statement has one home, and the card's title matches its contents.
- **cost:** S
- **rule:** BRIEF.md (*Prices display only*); SH-021 (the same rule, settled for the list).

### PU-021 · The contact list shows the value for some channels only, and invents a contact type
- **type:** defect · **level:** page · **impact:** low
- **where:** Space details — desktop 1440 (the aside) · `Space details.html?id=focus&loc=granted` ·
  `screens/04-space-details-variants/01-focus-hub-verified-fresh-5-photos-location-allowed-desktop-1.webp`
- **evidence:** `PU-021.png`
- **what is wrong:** `ContactButton` prints the value only for phone and WhatsApp, so «بريد»,
  «Instagram» and «Facebook» are wide buttons that are half empty and say nothing about where they
  lead (`PU-021.png`). The channel list also has `jawwal` and `ooredoo` as **types** («اتصال —
  جوال», «اتصال — أوريدو»), which the data model does not have: a contact is `phone`, and the
  carrier is only derivable from the `+97059…` / `+97056…` prefix. Keeping the carrier is right —
  calling within one network is what decides which number a person in Gaza uses — but it has to be
  stated as derived, not stored.
- **proposal:** every channel shows its value, truncated at the end on one line
  (`focus@example.com`, `@focushub`); the carrier label is derived from the stored E.164 prefix and
  the type stays `phone`, with «اتصال» alone when the prefix is neither Jawwal nor Ooredoo.
- **why it is better:** a visitor sees which account or address they are about to open, and the page
  stops implying a field the API will not send.
- **cost:** S
- **rule:** data-model › *Contacts*; foundation §8 (always-LTR values).

### PU-022 · The breadcrumb and the back link say the same thing twice
- **type:** improvement · **level:** page · **impact:** low
- **where:** Space details — phone 390 · `Space details.html?id=focus&loc=granted` ·
  `screens/04-space-details-variants/02-focus-hub-verified-fresh-5-photos-location-allowed-phone-390.webp`
- **evidence:** `PU-022.png`
- **what is wrong:** the page opens with «الرئيسية › المساحات › Focus Hub» and, on the next line at
  390, «‹ العودة إلى المساحات». Both go to the same kept query (`masaha:dir-query`). Together they
  take about 90 px above the first photo, on the page a visitor reaches most often.
- **proposal:** keep the breadcrumb on desktop and tablet (it also shows where the page sits);
  below `md` keep only «العودة إلى المساحات», on one row with nothing else. The settled P1 already
  gives dashboard sub-pages one back link; this is the public twin of it.
- **why it is better:** one way back, and 90 px of a 844 px screen returned to the content.
- **cost:** S
- **rule:** foundation §12 (`Breadcrumb`); P1.

### PU-023 · A space with no photos gets a 320 px grey box with a Latin initial
- **type:** improvement · **level:** page · **impact:** low
- **where:** Golden Hub · unverified, no photos — desktop 1440 ·
  `Space details.html?id=golden&loc=none` ·
  `screens/04-space-details-variants/07-golden-hub-unverified-stale-price-no-photos-desktop-1440.webp`
- **evidence:** `PU-023.png`
- **what is wrong:** `Gallery` renders a 14–20 rem `muted` block with `space.name[0]` at
  `text-display` and «لا توجد صور بعد». On the Arabic page the letter is «G» while the title is
  «غولدن هاب», and the box takes the best part of the first screen to say that something is
  missing. Most unverified spaces will have no photos, so this is the first impression of a large
  part of the directory.
- **proposal:** with no photos the gallery is not rendered: the page starts with the name block, and
  «لا توجد صور بعد» becomes a caption under it. (If a visual anchor is wanted, it is one `card`-high
  strip, not a 320 px block, and the letter is the display name's first character.)
- **why it is better:** an empty box stops being the biggest element on the page.
- **cost:** S
- **rule:** lens B5; P-C (the display name).

### PU-024 · The offline and error pages offer only «إعادة المحاولة»
- **type:** improvement · **level:** page · **impact:** low
- **where:** Offline — phone 390 · `Error.html?type=offline` ·
  `screens/10-about-error-pages/08-offline-phone-390.webp`; General error ·
  `Error.html?type=error`
- **evidence:** `PU-024.png`
- **what is wrong:** both states give one button, `location.reload()`. On a weak connection — the
  product's normal condition — pressing it while still offline reloads into the same page with no
  sign that anything was tried; there is no way on to anything that might be cached, and the 404,
  which *does* offer «الرئيسية» and «تصفّح المساحات», proves the pattern exists. The two states also
  share one `CircleAlertIcon`.
- **proposal:** the primary stays «إعادة المحاولة»; a secondary «الرئيسية» is added to both. The
  retry shows the button's `loading` while it tries, and says «ما زال الاتصال مفقودًا» when it fails
  (P8). Offline takes its own icon.
- **why it is better:** a visitor who cannot reach the network is not left on a page with one button
  that appears to do nothing.
- **cost:** S
- **rule:** P7, P8 (settled); foundation §13, screen 8.

### PU-025 · The results stay two columns on a 1440 screen
- **type:** improvement · **level:** page · **impact:** low
- **where:** List — desktop 1440 · `Directory.html?loc=none` ·
  `screens/03-directory-views-states/01-list-desktop-1440.webp`
- **evidence:** `PU-025.png`
- **what is wrong:** the results grid is `md:grid-cols-2` inside `lg:col-span-9`, so at 1440 each
  card is about 440 px wide and six spaces fill two and a half screens of scrolling, while Home
  shows three columns in a narrower container. The cards' content (name, area, one meta line, four
  price cells) does not grow to fill the width.
- **proposal:** the results grid becomes `md:grid-cols-2 xl:grid-cols-3` inside the 9-column area.
  The map view is unchanged.
- **why it is better:** more of the directory is comparable without scrolling, at no cost to the
  phone.
- **cost:** S
- **rule:** foundation §9.

### PU-026 · The single pin on the space page's map is a button that does nothing
- **type:** defect · **level:** page · **impact:** low
- **where:** Space details › الموقع — desktop 1440 · `Space details.html?id=focus&loc=granted` ·
  `screens/04-space-details-variants/01-focus-hub-verified-fresh-5-photos-location-allowed-desktop-1.webp`
- **evidence:** `PU-026.png`
- **what is wrong:** `LocationSection` reuses `SpaceMap` with `onSelect={() => {}}`, so the space's
  own pin is a focusable `<button aria-pressed="true">` that cannot be unpressed and does nothing
  when clicked. A keyboard user tabs into the map and finds a control with no effect.
- **proposal:** `SpaceMap` takes a `static` mode in which markers render as `role="img"` with their
  label and no button; the space page uses it. The only control in the section stays
  «الاتجاهات».
- **why it is better:** nothing on the page offers an action it does not have.
- **cost:** S
- **rule:** foundation §10; lens A5 (a control drawn in a state it cannot be in).

### PU-027 · The hours table repeats the space's shifts in every day row
- **type:** defect · **level:** page · **impact:** low
- **where:** Branch Hub · shifts + per-shift prices — desktop 1440 ·
  `Space details.html?id=branch&loc=none` ·
  `screens/04-space-details-variants/05-branch-hub-shifts-per-shift-prices-3-photos-desktop-1440.webp`
- **evidence:** `PU-027.png` (the collapsed table; see below)
- **what is wrong:** `HoursCell` renders `ShiftsLine` — the whole space's shifts — inside **every**
  row. With the sample data the days group into two rows, so it shows once and the defect is not
  visible; a space with three or more different day ranges gets the «عرض كل الأيام» toggle, and
  then «صباحي 08:00–16:00 · مسائي 16:00–22:00» is printed seven times. Shifts belong to the space,
  not to a day (data-model: named shifts inside the one daily opening range).
- **proposal:** the shifts line is rendered once, under the table, as «الورديات: صباحي 08:00–16:00 ·
  مسائي 16:00–22:00», beside the hours' «آخر تحديث».
- **why it is better:** one fact is stated once, and the expanded table stays readable at 390.
- **cost:** S
- **rule:** data-model › *Shifts*; lens A2.

### PU-028 · About's h1 uses the `display` style, which is the Home hero's
- **type:** defect · **level:** page · **impact:** low
- **where:** About «عن مساحة» — desktop 1440 · `About.html` ·
  `screens/10-about-error-pages/01-about-desktop-1440.webp`
- **evidence:** `PU-028.png`
- **what is wrong:** the heading is `text-heading-1 md:text-display`, 44 px from 768 up. foundation
  §7 reserves `display` for the Home hero only; the Directory's and the space page's titles are
  `heading-1`, so About's title is the largest text on the public site.
- **proposal:** `text-heading-1`, as the other public pages.
- **why it is better:** one page's title stops outranking the pages that matter more.
- **cost:** S
- **rule:** foundation §7 (`display` — Home hero only).

### PU-029 · How the settled filter bar (P5) fits the Directory
- **type:** improvement · **level:** page · **impact:** low
- **where:** List — tablet 768 · `Directory.html?loc=none` (no board frame); Filters sheet — phone
  390 · `screens/03-directory-views-states/22-filters-sheet-phone-390.webp`
- **evidence:** `PU-029.png`
- **what is wrong / what is decided:** P5 puts every filter inline from 768 and in the `FilterSheet`
  below that. The Directory's filter set is a **panel**, not a bar — a place combobox, two switches,
  a price field, six amenity chips and two others — and at 768 the content column is about 700 px,
  which fits neither a row of filters nor the `lg` sidebar. This is the page where the settled
  pattern needs a stated exception.
- **proposal:** the Directory keeps **the sidebar from `lg`** and **the sheet below `lg`** (bottom
  below `md`, end side from `md`), while taking the rest of P5: the search always visible, every
  filter a labelled `Field`, the active count on the «الفلاتر» button, the footer's primary
  «عرض 6 مساحات» and ghost «مسح الفلاتر», and the result count by the toolbar — which the page
  already has. The shared `FilterSheet` gains the count badge and this footer so the two become one
  component.
- **why it is better:** one filter component for the whole product, with one documented exception
  instead of a second implementation.
- **cost:** S
- **rule:** P5 (settled); foundation §9.

## 4. Rules in doubt

1. **foundation §12, `Breadcrumb`: "Dashboard sub-pages".** The public space page uses a breadcrumb,
   and should (it is the one page a visitor reaches from a search engine with no context). Propose:
   the inventory note reads "sub-pages, in the dashboard and on the space page", and the public page
   keeps the breadcrumb from `md` (PU-022).
2. **`docs/project/glossary.md` has no term for a published price's period.** The glossary defines
   *Subscription* and *Visit* but nothing for «ساعة · يوم · أسبوع · شهر» as a public price period,
   which is why the Directory reached for «مدة الاشتراك» (PU-002). Propose: add **Price period
   («الفترة السعرية»)** — one of hour, day, week or month, for which a space publishes a price; it
   is not a subscription.
3. **foundation §15, decision 3 ("comfortable, 40 px controls") versus §10 ("44 × 44 on touch").**
   The layer already resolves this with `@media (pointer: coarse)`, so it is not a defect — but the
   two sections read as a contradiction, and the next reviewer will raise it again. Propose: §15
   says "40 px, 44 px on touch".

## 5. Not reviewed

- **Checked and sound, so not reported:** touch targets (measured at 390 with `pointer: coarse` —
  the layer raises `--control-height` to 44 px, so every button, tab, select and chip passes; the
  exceptions are the map pins and the Switch, PU-012 and PU-019); the heading outline of every
  public page; the `aria` names of the view tabs and the filter switches; `details-aside` is sticky
  from `lg`; the 5-photo gallery grid is correct from 768.
- **The settled decisions** of `DECISIONS_SHARED.md` (the site header and its phone form, the
  account menu, the filter bar's shape, states, action feedback, confirm-or-undo, «إلغاء» → «رجوع»
  in the report and pin dialogs, the Toaster above a bottom bar, `CardTitle`'s heading level, the
  Skeleton's strength) — all of them appear on these pages and the fixer will apply them here.
- **Pagination** was not raised: the public directory is answered whole by design
  (api-contract §4, v1-mvp).
- **The map's drawing** (an illustration; OpenStreetMap through `shared/map` will replace it). Only
  its behaviour and layout were judged — pins, the selected card, the legend, picking. Zoom and pan
  controls do not exist in the illustration and were not reviewed; they will need a place that does
  not collide with «موقعي» or the selected card (PU-004).
- **Visible focus** was not verified: `:focus-visible` does not fire from a scripted focus in
  headless Chrome. No screen-reader pass was made; names and roles were read from the accessibility
  tree.
- **Contrast** was not re-measured (foundation §5 records the pairs as verified); only the status
  dot on the selected map pin was judged by eye, in both themes (PU-012).
- **Photo handling** beyond the placeholder: alt text for a real photo, the lightbox's keyboard and
  swipe behaviour, and image loading on a weak connection are not decided anywhere and are not in
  this review.
- **Out of scope:** the auth screens (5–7), the account area (9–11), both dashboards, and the reset
  email.
- **The archive's known limits** (placeholder icons, illustrative sample data, the Roboto fallback,
  the three superseded frames).
