# Design fix 3 — the public site, in the prototype (plan)

> **Approved 2026-10-12** (`PROMPT\FIX_PUBLIC_PLAN_REPLY.md`), with the owner's change and answers,
> folded in below:
> - **The card shows no prices** (Home, the Directory, Favourites): no cells, no student line; prices
>   live on the space page only (U9 there as planned). The cover photo leads at the top of the card;
>   below it the display name, the area, the live state (or «لا تتوفر حالة مباشرة»), today's hours,
>   the distance when in use; the heart over the photo for a signed-in visitor. The card is shown
>   first in the report (before/after at 390, 768, 1440).
> - **The sort is «الأحدث تحديثًا · حسب الاسم»** («الأقل سعرًا» goes), with «الأقرب إليّ» as U2. The
>   price filter stays, with S1's period.
> - **SH-021's display-only line leaves the lists' header line**; it stays once in the space page's
>   prices.
> - **§13:** S1–S6 approved; design issues **1, 2, 4 built** (2 weighed again for a card with no
>   prices), **3** recorded for worker A, **5** only if the combobox clips in the phone's sheet; the
>   cover at the top.
> - **Corrections:** finding 10 is resolved (#49); the one neutral amenity mark stays, its reason in
>   `CHANGES.md` being that the vendored bundle has no amenity icons. Before removing or retyping
>   data (`lastReview`, `statusUpdated`, `jawwal`/`ooredoo`, ZM Hub's `nameAr`, `nameAr`'s move),
>   grep every reader in the whole prototype; the report names them and that none broke; the other
>   worker's files are never edited to fix one (stop and say so).

Worker: the public design fixer · worktree `C:\Users\basel\masaha-design-public` · branch
`design/public` (cut after approval: `git fetch --prune origin`, then
`git switch --no-track -c design/public origin/main`; checked now: tree clean, detached at
`origin/main` = `068efc6`) · prototype served on **5347** · nothing installed.

## 1. Summary

Batch 3 of the design review (`DECISIONS_PUBLIC.md`, as amended 2026-10-12) is applied to the
living prototype's public site: Home, the Directory (list and map), the space page, About and the
error page, plus the shared parts they use (`shared.jsx`, `space-parts.jsx`, `map.jsx`,
`location.jsx`, `data.js`, `details-data.js`, `masaha.css`). In short: one place filter over the
whole Strip, no amenity filter, a price filter; one «الأقرب إليّ» control and one state line; one
name per space; one freshness rule; the map readable on a phone and by shape, a pin placeable from
the keyboard; a cover photo (or the space's mark) on every space card, the four price cells kept;
the space page in one order with prices per audience; a space's own amenities in the one amenity
list; the report saying who reads it; About and the errors corrected. Only items marked
**prototype** are built; the design-system, API, docs and web items are not this worker's.

## 2. Contract

**Scope** — the prototype items of `DECISIONS_PUBLIC.md` (U1–U12, the smaller items, the amended
note) and the prompt's H1–H5; the archive's records of them (`CHANGES.md` *Batch 3*, `INDEX.md`
rows, the board's frames for the public pages).

**Acceptance criteria**
- [ ] **U1** the Directory's default set is every listed space («6 مساحات في قطاع غزة»); place is one
  `Combobox` (`type="multiple"`) of the areas grouped by governorate, nothing preselected, `?area=`
  a list; a governorate with no active area has no group; Home's «تصفّح حسب المنطقة» shows the
  areas that have spaces, each with its governorate, «كل المناطق» last.
- [ ] **H3** no amenity filter anywhere on the public pages (sidebar, sheet, URL).
- [ ] **U5** a «السعر» `Field` (period `ToggleGroup` ساعة · يوم · أسبوع · شهر, min/max `dir="ltr"` ₪)
  driving `period`, `priceMin`, `priceMax` (S1); the sort is «الأحدث تحديثًا · حسب الاسم», its
  trigger reading «الترتيب: …»; «متاحة الآن فقط» beside «المساحات الموثّقة فقط» under «المساحات»
  with its note.
- [ ] **U2** one `NearMeButton` (`aria-pressed`) beside the result count on Home and both Directory
  views; distance gone from the sort list; one `LocationStatus` in four states (locating, in use,
  denied, imprecise), the same two fallbacks and the privacy line everywhere; Home's «اختر منطقتك»
  moves focus to its own area section; turning off reads «إيقاف الترتيب حسب المسافة».
- [ ] **U3** one display name (`spaceName`) on the card, pin, compact card/sheet, breadcrumb,
  `document.title`, favourites, report dialog, gallery dialog; the other name only under the h1; the
  search matches both names and the area (both languages); an English-only space (ZM Hub) renders
  everywhere, marked `lang="en"` inside Arabic.
- [ ] **U4** the live status shows its state alone with «الحالة مباشرة الآن» / «الحالة المباشرة تظهر
  للمساحات الموثّقة فقط»; each fact section carries its own relative «آخر تحديث …» and «قد يكون
  تغيّر» only when stale; the unverified notice reads «… · آخر تحديث للمعلومات قبل 4 أشهر» from the
  profile's date, its contact link the Alert's `AlertAction`; «للعرض فقط · الدفع في المساحة» once,
  in the prices.
- [ ] **U6** below `md` the selected space is a small non-modal bottom `Sheet`, the map re-centring
  the pin above it; the legend above the map, always in view; pins are dots with a 44 × 44 touch
  hit area, the name on the selected one and on hover/focus; four state **shapes**, the same in the
  legend; selected = `primary` ring + raised shadow.
- [ ] **U7** picking shows a fixed centre crosshair and a primary «ثبّت الموقع هنا»; arrow keys move
  the map under it; tapping still works; «رجوع» restores the previous location; only «مسح موقعي»
  clears; «موقعي» hidden while picking.
- [ ] **Smaller (directory)** the view switch is a `ToggleGroup type="single"` in a `Field`
  «طريقة العرض» (label `sr-only`); three result columns at `xl`; the P5 exception verified (sidebar
  from `lg`, `FilterSheet` below with its footer — already built in batch 1).
- [ ] **U12 / H2 (the owner's change)** every space card (Home, Directory, Favourites) is led by a
  fixed-ratio cover frame: the first photo (lazy, a small thumbnail), or the space's mark (first
  letter of its display name, as SH-006) in the same frame; under it the display name, the area,
  the live state, today's hours and the distance in use; **no prices**; the heart over the photo
  for a signed-in visitor; the skeleton has the same frame, so nothing moves when the photo or the
  data arrives; striking at 390, 768 and 1440 in both themes. SH-021's line leaves the lists.
- [ ] **U8** one order at every width: status → announcements → prices → hours → amenities → about →
  location → (phone: «التواصل») → report; closure Alert on top.
- [ ] **U9** one `PriceGrid` per audience («الأسعار», «للطلاب»), each the periods it publishes, a
  custom label replacing the period's name (the space page only; the card has no prices).
- [ ] **H4** a space's own amenities in the same list, same style, after the common ones, with the
  list's neutral check mark; sample: Focus and Branch bilingual, Number One **Arabic only** (shown in
  Arabic, `lang="ar"`, in the English interface).
- [ ] **H5** no price of 0 and no «مجانًا» in any price on a public frame (checked: none today); the
  price filter's bounds accept whole numbers above zero only.
- [ ] **U10** the report dialog names its reader by verification, and its toast says where it went;
  its dismiss is «رجوع» (P9, settled, not yet applied here).
- [ ] **Smaller (space page)** every contact shows its value, truncated; the carrier derived from the
  prefix (`phone` type, «اتصال — جوال/أوريدو», «اتصال» otherwise); display-only line and
  «الاتجاهات» once each; phone: «الحالة» card + one «التواصل» block, bottom bar WhatsApp + Call only,
  from below `md` (not `lg`); the heart beside the name, and on Home's and the Directory's cards for
  a signed-in visitor (the sign-in dialog otherwise, P9 toast); below `md` only «العودة إلى
  المساحات», the breadcrumb from `md`; no gallery without photos, a caption instead; the space's own
  pin `role="img"`; the shifts once, under the hours.
- [ ] **U11** About: the university line gone; «متاح» and the verified card say the state is
  automatic with a short manual override; a «تواصل معنا» section (`#contact`) before
  «لأصحاب المساحات» (`#owners`); every «تواصل معنا» points at `#contact`, Home's owner card at
  `#owners`; the title `text-heading-1`.
- [ ] **Errors** offline and error add a secondary «الرئيسية»; the retry shows `loading` and, when it
  fails, «ما زال الاتصال مفقودًا»; offline has its own icon.
- [ ] Records: `CHANGES.md` *Batch 3* (one line per applied decision), `INDEX.md` rows for every new
  parameter, the board's new frames; `check-parse` and `check-classes` green at every commit; every
  changed page looked at 390 / 768 / 1440 × AR / EN × light / dark; before/after pairs in
  `Downloads\design-fix-public\`.

**Out of scope** — the design-system item PU-019 (the Switch's hit area: worker A); the docs rule
changes (foundation §12 / §15, the glossary's *Price period*); the API (`area` list, price filters,
the cover thumbnail, dropping `amenities`); the editor's own-amenities fields and the admin
lookups' «يظهر في الفلاتر» switch (other files; see §7); any page outside the public site except the
one-line link/name fixes named in §5.

## 3. Reading done

CLAUDE.md; workflow (§2 phases and reading, §3, §8, §9, §10); the prompt; `DECISIONS_PUBLIC.md`
(amended note first, then all); `DECISIONS_SHARED.md`; `REVIEW_PUBLIC_REPORT.md` (PU-001…029,
patterns, rules in doubt, not reviewed); `docs/design/CHANGES.md`, `README.md` (check scripts),
`INDEX.md` (structure, the fix-phase parameter table, the public rows); the board's public frames;
data-model › *Conventions* (a space's name: English required, Arabic optional), *Lookups*,
*Spaces*, *Derived values* (live status, stale); `features/spaces.md` › *Behaviour*;
`features/lookups.md` › *Behaviour*; api-contract › *Lookups (public)*; v1-mvp › the `GET /spaces`
row; the amenities plan (own amenities: Arabic required, English optional; glossary «مرفق إضافي»);
foundation headings, §13 public screens; overview › *Not in v1*; the findings index (open titles).
Source read: `Home.html`, `Directory.html`, `Space details.html`, `About.html`, `Error.html`,
`masaha/shared.jsx`, `space-parts.jsx`, `location.jsx`, `map.jsx`, `data.js`, `details-data.js`,
`masaha.css`, `i18n.js`; the vendored `Combobox` (multiple, `ComboboxGroup`), `Sheet` (Radix root,
so `modal={false}` drops the overlay), the icon list (no wifi-off icon), the bundle's utility
classes (`aspect-video`, `object-cover`, `truncate`, `xl:grid-cols-3` present; no `ring-*`,
`border-dashed`); every other user of the shared parts (`SpaceMap` in `profile-a.jsx`;
`FilterSheet` on nine dashboard lists; `SpaceCard` on Favourites).

## 4. The settled decisions, as they will be built

**Data (`data.js`, `details-data.js`).**
- `nameAr` moves from `details-data.js` into `data.js`, so the Directory, Home and Favourites have it
  (the search needs it). **ZM Hub loses its Arabic name** — the model's English-only case.
- Active areas are added to two more governorates (الوسطى: «دير البلح», «النصيرات»; خان يونس:
  «وسط خان يونس», «المواصي»), with no spaces; North keeps none and Rafah stays hidden, so neither
  has a group. The spaces stay where they are.
- Each space gains `photos` in `data.js` (the cover needs it on the lists; today it is
  `details-data.js` only) and the fact-group dates the page shows: `profileUpdated`,
  `amenitiesUpdated`, `contactsUpdated` (with `hoursUpdated` and the prices' `updated` already
  there), each with a days count so «قد يكون تغيّر» follows the thresholds (30 prices / 60 others).
  `lastReview` and `statusUpdated` go.
- Prices on the page become rows `{ period, audience, shift?, label?, amount }`; `prices` (the
  card's four general cells) stays. Number One: a student day and month; Focus: one labelled price
  (a week labelled «أسبوع الامتحانات»); Branch keeps its per-shift rows. Every amount above zero.
- Contacts' `jawwal` / `ooredoo` types become `phone`; the carrier is derived from `+97059` /
  `+97056` (as batch 2a's E4 did in the editor).
- `ownAmenities: [{ ar, en? }]`: Focus «زاوية مكالمات / Call corner», Branch «خزائن شخصية /
  Personal lockers», Number One «مكتبة كتب تقنية» (Arabic only).

**U3 — one name.** `shared.jsx` gains `spaceName(s)` (Arabic UI: `nameAr` else `name`; English UI:
`name`) and `<SpaceName>` (wraps it in `lang="en"`/`lang="ar"` when its script differs from the
page's). Used by `SpaceCard`, the pin label and `aria-label`, the selected card/sheet, the
breadcrumb, `document.title`, the gallery dialog, the report dialog, the favourites' remove label;
the h1 uses it and the other name (when it exists) sits under it. Search: lower-cased match on
`name`, `nameAr`, and the area's name in both languages. «حسب الاسم» sorts by the display name in
the page's locale.

**U1 / H3 / U5 — the Directory's filters** (`FiltersForm`, `applyFilters`, `syncUrl`).
- «المنطقة»: `Combobox type="multiple"`, a `ComboboxGroup` per governorate that has active areas,
  trigger «كل المناطق» (empty) / the one area's name / «2 مناطق محددة»; search in the content.
  `gov` is dropped (an old `?gov=` is ignored); `?area=nasr,rimal` works across governorates.
- The amenity group, `amenities` state and `?am=` go.
- «المساحات»: a `text-label` heading over the two `Switch` fields, «متاحة الآن فقط» first, a caption
  «"متاحة الآن" تشمل المساحات الموثّقة فقط».
- «السعر»: a `ToggleGroup` (`single`, the `short` period names) labelled «الفترة», then «من» / «إلى»
  `Input`s (`dir="ltr"`, `inputMode="numeric"`, ₪ as end adornment), a helper «النطاق على سعر
  الفترة المختارة»; a bound that is not a whole number above zero, or a max below the min, is an
  error on its field and is not applied. Period behaviour: see S1.
- Unverified spaces with stale prices are left out of the price filter (data model).
- The sort `Select`: «الأحدث تحديثًا · حسب الاسم» (the owner: «الأقل سعرًا» goes with the card's
  prices), its value read as «الترتيب: …».
- The count line: «6 مساحات في قطاع غزة» (or «في {المنطقة}» for one area), with no display-only
  note (SH-021's line leaves the lists).
- «أخرى» keeps «أسعار للطلاب» and «مفتوحة يوم الجمعة».

**U2 — near me** (`location.jsx`, Home, Directory).
- `NearMeButton` sits beside `ResultCount` on Home (the section's header) and in both Directory
  views; it is pressed while a location is in use, and pressing it again turns it off.
- While on, the list is sorted by distance and the sort trigger reads «الترتيب: حسب المسافة» with no
  item chosen; choosing a sort from the list turns «الأقرب إليّ» off.
- `LocationStatus` renders all four states, each with the privacy line: *locating* («جارٍ تحديد
  موقعك…», polite); *in use* (as today, its off link «إيقاف الترتيب حسب المسافة», or «تغيير
  الموقع» · «مسح موقعي» for a manual pin); *denied* (title «تعذّر تحديد موقعك», description «اختر
  منطقتك أو حدّد موقعك على الخريطة لنرتّب المساحات حسب المسافة»); *imprecise* (as today); the
  two fallbacks in both failures.
- Home's «اختر منطقتك» scrolls to and focuses its area section's heading; Home's «حدّد موقعي على
  الخريطة» still opens the Directory's map in picking.

**U6 — the map** (`map.jsx`, `masaha.css`, Directory).
- A pin is a `button` holding a 14 px state mark; its box is 24 px and 44 × 44 under
  `pointer: coarse`. The name shows as a label on the selected pin and on hover / `:focus-visible`.
- Marks (`masaha.css`, token colours only): متاح a filled `success` dot; ممتلئ a filled `warning`
  dot with a `card`-coloured bar across; مغلق الآن a hollow dot (`muted-foreground` ring);
  لا تتوفر حالة مباشرة a dashed hollow dot. `MapLegend` draws the same marks.
- Selected: a 2 px `primary` ring and `shadow-raised` on the pin, never a fill.
- The legend moves **above** the map (one wrapping row), in view at every width.
- Below `md`: the selected space opens a `Sheet side="bottom" modal={false}` (no overlay; outside
  taps don't close it, so another pin re-selects) with the display name, area, state, today's
  hours, distance and «عرض التفاصيل»; the map's inner layer shifts so the pin sits in the upper
  third. From `md` the overlay card stays as today.
- `SpaceMap` gains `static` (markers `role="img"` with their label, no button), used by the space
  page (PU-026).

**U7 — placing a pin by hand.** Opt-in props on `SpaceMap` (`pickAtCentre`, `onConfirmCentre`), so
the editor's pin map (`profile-a.jsx`, tap-to-place) is unchanged. In the Directory's picking: a
fixed crosshair at the centre; the instruction card says «حرّك الخريطة حتى تقع العلامة على مكانك،
أو اضغط عليه» with a primary «ثبّت الموقع هنا» and a ghost «رجوع»; the map region is focusable and
the arrow keys move the layer under the crosshair; a tap places the pin where tapped. `useNearMe`
keeps the location from before picking; «رجوع» restores it (or idle if there was none). «موقعي» is
hidden while picking.

**U12 / H2 — a striking space card** (`SpaceCard`, `SpaceCardSkeleton`, `masaha.css`; the owner's
change: no prices on any card).
- The photo leads: a fixed-ratio frame at the top of the card, edge to edge (`bg-muted`), its box
  reserved before anything loads; 16:9 from `md`, a shorter ratio below it (design issue 2, weighed
  by eye once the prices are gone).
- Under it, in order of what makes someone open it: the display name (`text-heading-3`), the area
  line (muted), then one row with the live state (`LiveStatus` badge, or «لا تتوفر حالة مباشرة») and
  «موثّقة», then today's hours and the distance in use (`text-body-sm`, muted); the «آخر تحديث» and
  stale badge leave the card with the prices (freshness belongs to the page's groups, U4). Tokens and
  layer components only (`Card`, `Badge`, the type scale, spacing tokens).
- With photos: the stand-in for the first photo (the archive has no real images; `PhotoTile`'s
  look), `loading="lazy"` noted on the element, decorative (`aria-hidden`; the title names the card).
- With none: the space's mark — the first letter of its display name in the switcher's style
  (`bg-primary text-primary-foreground`, rounded square), centred in the same frame.
- `?photos=loading` shows every frame waiting (the muted frame with a `Skeleton`), and
  `?photos=failed` the mark in place of a photo that did not load, so the weak-connection states are
  frames. The card skeleton gets the same frame.
- No price cells and no student line; `SpacePrices` and `PriceMeta` leave the card, and the lists
  lose `DISPLAY_ONLY`.
- The heart (U12 with PU-014): on Home and the Directory, for a signed-in visitor, the overlaid
  heart (as Favourites' `reserveEnd`), over the frame's top-end corner; signed out it opens the
  sign-in dialog. Toggling toasts with «تراجع» (P9).

**U8 and the smaller items — the space page** (`Space details.html`, `space-parts.jsx`).
- Order: closure Alert → gallery (or nothing) → name block with the heart beside the h1 → unverified
  notice → phone «الحالة» card → announcements → prices → hours → amenities → about → location →
  phone «التواصل» block → report. Desktop: the aside's «الحالة والتواصل» card, sticky as today.
- `StatusLine`: the badge and «الحالة مباشرة الآن», nothing dated.
- Sections' `meta`: «آخر تحديث للأسعار قبل يومين», «… لساعات العمل …», «… للمرافق …», «… للتواصل …»
  (the contacts' line in the «التواصل» block and the aside), each with «قد يكون تغيّر» when stale.
- Prices keep the stale `Alert` for a verified space's stale prices; the display-only line once,
  in the prices' meta. The card's «الدفع والاشتراك» line goes.
- «الاتجاهات» only in «الموقع». The bottom bar shows below `md` (`md:hidden`), WhatsApp and Call.
- `ContactButton` shows every value, truncated (`truncate`, `dir="ltr"`), the label «اتصال — جوال»
  / «اتصال — أوريدو» / «اتصال» from the prefix.
- Below `md`: «العودة إلى المساحات» alone; from `md`: the breadcrumb alone.
- `Gallery` with no photos renders nothing; the name block gets the caption «لا توجد صور بعد».
- `HoursSection`: the shifts once under the table («الورديات: صباحي 08:00–16:00 · مسائي …»).

**U9 — prices per audience.** `PriceGrid` takes the rows of one audience and shows one cell per row
(label in place of the period name when set). `PricesSection` renders «الأسعار» then, when any,
«للطلاب»; with shifts, the existing `Tabs` (a real tab set) holds the same per-audience grids per
shift. The card shows no prices (the owner's change).

**H4 — own amenities.** `AmenitiesSection` lists the common ones in catalogue order, then the
space's own in their order, the same chip and the same `CheckIcon` (the list's neutral mark, for
every amenity alike: the vendored bundle has no amenity icons; the code draws them since #49). An own amenity's name: in the English
interface `en` when present, else `ar` with `lang="ar" dir="rtl"`; in Arabic, `ar`.

**U10 — the report dialog.** Description: verified «يصل البلاغ إلى إدارة المساحة، وتجد ردّها في
«بلاغاتي»»; unverified «يراجع فريق مساحة البلاغ، وتجد الردّ في «بلاغاتي»». Toast: «أرسلنا البلاغ
إلى إدارة المساحة» / «أرسلنا البلاغ إلى فريق مساحة». Dismiss «رجوع».

**U11 — About.** The university line removed. «متاح»: «فيها مكان الآن، وتُحدَّث الحالة تلقائيًا من
حركة الحضور في المساحة». Verified card: «تحدّث إدارة المساحة ساعاتها وأسعارها وإعلاناتها، وتظهر
حالتها المباشرة تلقائيًا، ويمكنها ضبطها يدويًا لفترة قصيرة». A «تواصل معنا» section `id="contact"`
before owners: one line on what to write about, WhatsApp (primary) and email. The owners' card
keeps its steps and buttons. The freshness paragraph's "next to old prices" becomes "next to the
information that may have changed" (U4). h1 `text-heading-1`. Footer «تواصل معنا» →
`About.html#contact`; Home's owner card → `About.html#owners`; `Error.html`'s 403 → `#contact`.

**Errors (`Error.html`).** offline/error: primary «إعادة المحاولة», secondary outline «الرئيسية». The
retry is `useActionRun`-style: `loading` for the action time, then reload — or, with
`?fail=retry` (or `navigator.onLine === false` on offline), a polite line under the buttons «ما زال
الاتصال مفقودًا» (offline) / «ما زال الخطأ قائمًا، حاول بعد قليل» (error). Offline's icon: an inline
wifi-off SVG (the layer has none; recorded for the web).

## 5. Stronger decisions

- **S1. The price period qualifies the range; it is not a filter on its own.** Today the period
  chips filter "spaces that publish this period", which PU-002 calls the wrong question. *What:* the
  period `ToggleGroup` always holds a value, «يوم» by default; it counts as active and is sent only
  with a bound; the range applies to that period. *Why:* a range with no period
  mixes a 3 ₪ hour with a 300 ₪ month and means nothing; a bare period filter answers nothing a
  visitor asks. *Cost:* the API's `period` is required with a bound (worker B's step 3; a line in
  CHANGES' notes for the web). **Recommend: yes.**
- **S2. `SpaceMap`'s new behaviour is opt-in** (`static`, `pickAtCentre`), so the editor's pin map in
  `profile-a.jsx` keeps tap-to-place and its coordinates field. Only the pins' look (dots, ring) reaches
  it, which is the same marker everywhere. *Cost:* two props. **Recommend: yes.**
- **S3. `RouteState`'s offline (the dashboard's) takes the same wifi-off icon** as `Error.html`, so
  one state has one icon. *Cost:* one line in `shared.jsx`. **Recommend: yes.**
- **S4. U3 and U11 reach two account pages by one line each:** `Reports.html` («بلاغاتي») names the
  space with `spaceName`, and `Settings.html`'s «تواصل معنا» (to change the email) points at
  `#contact`. Neither is the other worker's file. *Why:* U3 is "one name everywhere", PU-016 "every
  «تواصل معنا»". *Cost:* two lines; batch 6's fixer would otherwise inherit them. **Recommend: yes.**
- **S5. The weak-connection states of the cover are frames** (`?photos=loading|failed`), not only a
  promise in CHANGES. *Cost:* one parameter. **Recommend: yes.**
- **S6. The map's arrow-key pan while picking** gives the crosshair a real keyboard path in the
  prototype, as Leaflet's keyboard pan will in code. *Cost:* small (the U6 re-centring uses the same
  transform). **Recommend: yes.**
- No rule of the documents is weakened. ADR 0008 (a state, never a count) is strengthened by U4; the
  location still never leaves the device.

## 6. Related findings

- **8** (the applied-filter tag has no component): not folded — a design-system item; the Directory
  shows the active count on «الفلاتر» and in the sidebar's «مسح».
- **10** (amenity icons): not folded — the reason the list keeps one neutral mark (H4).
- **35** (the web sets no document title), **40** (platform contacts outside the catalogue): code
  items; the prototype already sets the title and shows the contacts. Not folded.

## 7. Files

Mine (prototype): `Home.html`, `Directory.html`, `Space details.html`, `About.html`, `Error.html`,
`masaha/shared.jsx`, `space-parts.jsx`, `location.jsx`, `map.jsx`, `data.js`, `details-data.js`,
`masaha.css`; one line each in `Favorites.html` (the remove label's name), `Reports.html`,
`Settings.html` (S4). Records: `CHANGES.md` (my *Batch 3* section, appended after 2a), `INDEX.md`
(a *Batch 3* parameter table under the fix-phase table, and my rows), `Flows - states.html` (my new
section appended at the board's end; existing public frames keep their URLs).

**The other worker's** (`design/admin-rest`): the eight admin pages, `Admin space edit.html`,
`admin.jsx`, `admin-data.js`, `profile-b.jsx` — **none edited.** Effects that reach them without an
edit, said in the PR: the pin marker's new look in the editor's map (via `map.jsx`), ZM Hub's empty
Arabic name in the admin's views (via `data.js`), and contacts typed `phone`. Not needed from them:
nothing. For them / later batches (recorded, not done): the admin lookups' «يظهر في الفلاتر» goes
(H3), and the editor needs own-amenity fields (H4, `profile-*.jsx`).

Shared sections: `CHANGES.md`, `INDEX.md`, the board — whichever PR merges second rebases keeping
both; if both appended board frames at the same height, the second shifts its own.

## 8. Design issues (not built unless approved)

1. **The map's «موقعي» duplicates «الأقرب إليّ»** in the map view (U2 puts the one control beside the
   count). *Better:* «موقعي» becomes «مركّز على موقعي» only while a location is in use (re-centres,
   `variant="outline"`), and is absent otherwise. *Level:* page · low.
2. **The cover makes a phone card about 200 px taller** (6 spaces ≈ +1,200 px). *Better:* below `md`
   a 2:1 frame instead of 16:9 (`aspect-video` → a `masaha.css` ratio rule), keeping the photo and
   the cells. *Level:* page · medium.
3. **No offline icon in the layer** (`CircleAlertIcon` is error's too). *Better:* add `WifiOffIcon`
   to the design system's icon set. *Level:* design system · low.
4. **Favourites stays two columns at `xl`** while the Directory takes three (PU-025). *Better:*
   `xl:grid-cols-3` there too, so the same card has one width. *Level:* page · low.
5. **A combobox inside the phone's bottom sheet** opens a popover over a sheet with its own scroll; if
   it clips at 390 during the run, *better:* the place field opens full-height in the sheet (the
   `Combobox`'s content `side="bottom"`, `max-h` of the sheet). To be confirmed by eye. *Level:*
   component · low.

## 9. Tests — what each look catches

No test lane covers `docs/design/`; the two scripts plus the real run stand in.
- `check-parse.mjs` → a syntax error that blanks a page. `check-classes.mjs` → a class the bundle
  lacks (every new rule in `masaha.css` with tokens).
- Frames (each at 390 / 768 / 1440, AR/EN, light/dark where it changed):
  `Directory.html?loc=none` (the Strip count, 3 columns at 1440, covers, cells) · `&sheet=filters`
  (place combobox, «المساحات», «السعر», no amenities) · `?area=nasr,rimal&period=month&priceMax=300`
  (filters apply, count line) · `?priceMin=50&priceMax=20` (the range error) · `?q=فوكس` and
  `?q=zm` (both names) · `?view=map&selected=focus&loc=none` (sheet on phone, card from 768, ring,
  marks, legend) · `?view=map&loc=picking` and `&loc=manual` then «تغيير الموقع» → «رجوع» (location
  kept) · `?loc=denied|imprecise|locating|granted` (four states) · `?photos=loading|failed`.
  `Home.html?loc=none|denied|granted` (one control, area cards across governorates, «اختر منطقتك»
  focus) · `&auth=1` (hearts). `Space details.html?id=focus|branch|numberone|golden|zm|white` (order,
  name, dates, prices per audience, labelled price, own amenities, no gallery, contacts),
  `&lang=en` on numberone (Arabic-only own amenity) and zm (English name in AR), `&auth=1&dialog=report`
  on focus and golden (two readers). `About.html`, `#contact`. `Error.html?type=offline|error`
  `&fail=retry`, `?type=403`.
- Regression looks on the shared parts' other users: `Favorites.html`, `Admin space edit.html?id=white`
  (the pin map still tap-to-place), one dashboard list with `FilterSheet` at 390.

## 10. Review focus (inputs no look exercises)

The Combobox with every area chosen; a space with photos but none loading (real network);
`sessionStorage` holding a picked location across pages while picking is cancelled; keyboard-only
tabbing through 6+ dot pins; a very long English-only name in an Arabic card; RTL arrow-key
direction while panning (arrows move the map in the visual direction).

## 11. Commits (`docs(design): …`, ≤ 50 characters, each with its CHANGES line, INDEX rows, frames)

1. `docs(design): one name for each space` (U3, data moves) — 38
2. `docs(design): place is one filter, no amenities` (U1, H3) — 48
3. `docs(design): a price filter and the sort's name` (U5) — 48
4. `docs(design): one near-me control and state line` (U2, design issue 1) — 49
5. `docs(design): the map by shape, on a phone too` (U6, PU-026) — 46
6. `docs(design): place a pin from the keyboard` (U7) — 43
7. `docs(design): a striking space card` (U12/H2, no prices, hearts, design issues 2 and 4) — 36
8. `docs(design): the space page in one order` (U8, smaller items) — 41
9. `docs(design): one freshness rule` (U4) — 32
10. `docs(design): prices per audience` (U9, H5) — 33
11. `docs(design): own amenities in the one list` (H4) — 43
12. `docs(design): the report names its reader` (U10) — 41
13. `docs(design): About and the error pages` (U11, errors, S3, S4) — 39

## 12. Verification (phase 4)

- At every commit: `node docs/design/scripts/check-parse.mjs` and `check-classes.mjs`.
- Real run: `python -m http.server 5347 --bind 127.0.0.1` from `docs/design/prototype`; Chrome (or
  the headless CDP fallback) at 390 (touch), 768, 1440, AR/EN, light/dark, on every frame of §9;
  before/after pairs in `C:\Users\basel\Downloads\design-fix-public\` named by decision
  (`H2-home-390.png`). The server and any browser stopped, port 5347 checked free; every background
  shell stopped.
- **Not run here:** `format:check` and `check:links` (no packages installed in this worktree, by the
  prompt): CI runs them; the report says so and waits for green. No lanes, no build: no code changes.
- PR `design: the public site`, labels `docs`, `area:docs`, assigned to the owner; not merged.

## 13. Decisions from the owner (answered 2026-10-12)

1. **S1–S6:** approved.
2. **Design issues:** 1, 2 and 4 built; 3 recorded for worker A's design-system item (a wifi-off
   icon); 5 only if the combobox clips in the phone's sheet.
3. **The cover's place:** at the top of the card; the card shows no prices (the owner's change).
