# Design decisions — batch 3, the public site (approved by the owner, 2026-10-10)

> **Changed 2026-10-13** by the owner (step 3's API): the directory is **paged and filtered on the
> server**, and **"near me" sorts on the server**, so the device's location reaches the API (rounded on
> the device, never stored or logged). **The privacy line «يبقى موقعك على جهازك فقط، ولا يُرسَل إلى أي
> جهة.» becomes untrue** and must be reworded in the prototype (`shared.jsx`'s `PRIVACY_LINE`) and in
> the web when it is built — route to the next design item that may touch `shared.jsx`. The list
> pages (P6's pagination); the map reads its own light pins.

> **Amended 2026-10-12** by the owner: **amenities are no filter** — the Directory's amenity filter
> goes (the API's `amenities` filter is dropped from the plan). **A space's own amenities («مرافق
> إضافية») show exactly as the common ones** on the space page and wherever amenities show: one list,
> one style, no second section; an own amenity, having no icon of its own, takes one neutral mark that
> the common ones' layout already allows. **U12, changed again by the owner (2026-10-12): the card shows
> no prices** — prices live on the space page only. The cover photo sits at the top of the card, and
> the card must be striking (the photo leads; no price cells, no student line). **The sort loses «الأقل سعرًا»** (a sort
> by a price the card does not show reads as random); the price filter stays (a budget), and
> SH-021's «للعرض فقط · الدفع في المساحة» leaves the lists for the space page's prices. **DI-16 (a price of 0):** no free price is shown or entered — every price
> is above zero; a free event goes in the space's announcements (the API's rule changes to match).

From `REPORT\REVIEW_PUBLIC_REPORT.md` (PU-001 … PU-029). **Settled.** Where each is done:
**prototype** (the design fixer), **design system** (worker A), **API** (worker B, the public
directory, build step 3), **docs** (the owning document), **web** (worker A, step 3).

## Patterns
- **U1 — the directory covers the Strip; place is one filter** (PU-001, PU-018): the default set is
  every publicly listed space in the Gaza Strip («6 مساحات في قطاع غزة»); governorate and area are
  one `Combobox` (`multiple`) of the areas grouped under their governorate, nothing preselected,
  sending the `area` list; a governorate with no active areas has no group. Home's «تصفّح حسب
المنطقة» shows the areas that have spaces, each with its governorate, and «كل المناطق» last.
  *(prototype; API: the `area` list filter)*
- **U2 — one «الأقرب إليّ» control and one state line** (PU-004, PU-005, PU-018): a `Button`
  «الأقرب إليّ» (`aria-pressed`) beside the results count on Home and the Directory (both views); it
  leaves the sort list («الأحدث تحديثًا · الأقل سعرًا · حسب الاسم»), and turning it on sorts by
  distance and says so; under it one `LocationStatus` line in its four states, with the same two
  fallbacks everywhere («حدّد موقعي على الخريطة», «اختر منطقتك») and the privacy line; on Home
  «اختر منطقتك» moves to Home's own area section; turning it off says «إيقاف الترتيب حسب المسافة».
  *(prototype)*
- **U3 — one name per space** (PU-003): in the Arabic interface the Arabic name when it exists, else
  the English one; in the English interface the English name; the other name under the title on the
  space page only. The card, the pin, the breadcrumb, the document title, the favourites and the
  report dialog use it. The search matches **both names and the area**. *(prototype; API: the search)*
- **U4 — one freshness rule** (PU-008, PU-009, PU-020): freshness belongs to a fact group, never to
  the live status (which shows its state alone, with «الحالة مباشرة الآن» or «الحالة المباشرة تظهر
  للمساحات الموثّقة فقط»); each section carries its own relative «آخر تحديث …» and «قد يكون تغيّر»
  only when stale; an unverified space's notice says «آخر تحديث للمعلومات قبل 4 أشهر» from the
  profile's date, its contact link the Alert's action; «للعرض فقط · الدفع في المساحة» once per page,
  in the prices. *(prototype)*

## The directory
- **U5 — a price filter** (PU-002): a «السعر» `Field` — a period `ToggleGroup` (ساعة · يوم · أسبوع ·
  شهر) and min / max inputs (`dir="ltr"`, ₪), sending `period`, `priceMin`, `priceMax`; the sort
  trigger reads «الترتيب: …»; «متاحة الآن فقط» beside «المساحات الموثّقة فقط» under «المساحات», with
  a note that available-now covers verified spaces only. *(prototype; API: the planned filters)*
- **U6 — the map on a phone** (PU-004, PU-012): the selected card is a small bottom `Sheet`, the map
  still panning behind it and re-centring the pin above it; the legend inside the map (top-end, by
  «موقعي») or above it; pins are dots, the name on the selected one and on hover; each state a
  **shape as well as a colour** (filled · filled with a bar · hollow · dashed hollow), the same marks
  in the legend; the selected pin a `primary` ring and a raised shadow, not a fill. *(prototype)*
- **U7 — placing a pin by hand** (PU-005): a fixed centre crosshair and a primary «ثبّت الموقع هنا»;
  tapping the map still works; «رجوع» returns to the previous location, only «مسح موقعي» clears it;
  «موقعي» hidden while picking. *(prototype)*
- **Smaller:** the view switch is a `ToggleGroup type="single"` in a `Field` «طريقة العرض» (label
  visually hidden), `Tabs` kept for real panels (PU-013); three result columns at `xl` (PU-025); the
  **P5 exception**: the Directory keeps its filter sidebar from `lg` and the sheet below `lg`, and
  takes the rest of P5 — the shared `FilterSheet` gains this footer, so the two are one component
  (PU-029). *(prototype)*
- **U12 — a cover photo on the space card** (the owner, 2026-10-11, at PR #59's review): the space's
  first photo (its cover) at the top of the card on Home, the Directory and Favourites, at a fixed
  ratio, lazy-loaded and served as a small thumbnail; a space with no photo shows its mark (the first
  letter of its name, as the switcher's, SH-006) in the same frame. No logo field (no schema change).
  *(prototype; API: a thumbnail for the cover — near the deferred storage layer, Issue #37, to plan
  with the owner; web: step 3)* — *open:* whether U9's four price cells stay once the card has a
  photo (the analyst proposes two: day and month).
  > **Superseded by the amendments at the top (2026-10-12):** U9's card part («the card keeps its four general
  > cells and one «للطلاب» line») and U12's open point (whether the cells stay) — the card shows no price;
  > U2's sort list loses «الأقل سعرًا»; the amenities are no filter. The web builds the amended rules
  > (PUBLIC, PR 1). *(Added by the supervisor with the owner's approval, 2026-10-21.)*

## The space page
- **U8 — one order at every width** (PU-007): status & contact → announcements (when any) → prices →
  hours → amenities → about → location → report; the closure Alert stays at the top. *(prototype)*
- **U9 — prices per audience** (PU-011): one `PriceGrid` per audience («الأسعار», then «للطلاب»), each
  the periods that audience publishes; a custom label replaces the period's name; the card keeps its
  four general cells and one «للطلاب» line when a student price exists. *(prototype)*
- **U10 — the report says who reads it** (PU-010): verified → «يصل البلاغ إلى إدارة المساحة، وتجد
  ردّها في «بلاغاتي»»; unverified → «يراجع فريق مساحة البلاغ، وتجد الردّ في «بلاغاتي»». *(prototype)*
- **Smaller:** contacts show their value (truncated), the carrier derived from the prefix (PU-021,
  with AD-006); the display-only line and «الاتجاهات» once each, on a phone a «الحالة» card and one
  «التواصل» block, the bottom bar repeating only WhatsApp and Call (PU-020); the heart beside the name
  and on the Directory's and Home's cards for a signed-in visitor (PU-014); below `md` only «العودة
  إلى المساحات», the breadcrumb from `md` (PU-022); no gallery when there are no photos, a caption
  instead (PU-023); the space's own pin `role="img"`, not a button (PU-026); the shifts once, under
  the hours (PU-027); the page's phone bottom bar at the shells' `md` breakpoint, not `lg` (DI-3 of
  the shared fix). *(prototype)*

## About, Home, errors
- **U11 — About** (PU-006, PU-015, PU-016, PU-017, PU-028): **the university line goes** (the owner's
  rule); «متاح» reads «فيها مكان الآن، وتُحدَّث الحالة تلقائيًا من حركة الحضور في المساحة» and the
  verified card says the state is automatic, with a short manual override; a «تواصل معنا» section of
  its own before «لأصحاب المساحات» (the platform's WhatsApp and email), which the footer and Home's
  owner card point at (`#contact` / `#owners`); the title `text-heading-1`. *(prototype)*
- **The errors** (PU-024): offline and error add a secondary «الرئيسية»; the retry shows `loading`
  and says «ما زال الاتصال مفقودًا» when it fails; offline its own icon. *(prototype)*

## Design system
- **PU-019:** a `Switch` in a `Field` gets a 44 × 44 hit area on touch, and its whole horizontal row
  activates it (`aria-labelledby` and the label row's click). *(design system)*

## Rules changed
- **foundation §12 `Breadcrumb`:** "sub-pages, in the dashboard and on the public space page". *(docs)*
- **glossary:** a new term, **Price period · الفترة السعرية** — one of hour, day, week or month for
  which a space publishes a price; not a subscription. *(docs)*
- **foundation §15:** "40 px controls, 44 px on touch" (one sentence; with AD-030). *(docs)*
