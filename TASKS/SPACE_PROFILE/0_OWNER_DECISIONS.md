# SPACE_PROFILE — the owner's decisions (from 2026-11-08, section by section)

The redesign of the space profile: the owner's page (`Owner space profile.html`, `/dashboard/spaces/:spaceId/profile`
in the web) **and the admin's space editor** (added to the scope 2026-11-08). The owner, acting as a space owner, found
the current page "beginner": every section always editable, a Save button in each, an order that does not follow the
public page. Decisions are taken one section at a time; this file grows with them.

## The page

- **G1 — view first.** Each section shows its facts as a visitor sees them, with no field; editing is asked for. The
  edit surface is a **Sheet** per section (approved in principle 2026-11-05), except where a section says otherwise.
- **G2 — the order follows the public page:** the header · الصور · الأسعار · ساعات العمل والورديات · المرافق · عن
  المساحة · الموقع · التواصل.
- **G3 — a section's head:** its title, «آخر تحديث قبل N أيام» (muted), «تعديل». A stale group shows «قد تكون قديمة»
  and «ما زالت صحيحة» (confirms without editing). An empty section shows «لم تُضف بعد» and a clear action («أضف ساعات
  العمل»…). Visitors' reports about a section show inside it. Desktop: a side index of the sections with a state dot
  (complete / stale / missing); phone: no index.
- **G4 — gone from the top of the page:** «كل قسم يُحفظ وحده…», the missing-items checklist (the header replaces it),
  the page-level unsaved-changes alert (a Sheet asks before discarding).
- **G5 — the admin's space editor takes the same design** in the same task.
- **Settled later the same day:** prices are edited in the profile (R1); «عن المساحة» and «الموقع» are two sections
  (B2/L2), «الورديات» a section of its own (S1) — each pair over one API group: an executor check on partial saves.
  The final order: the header · الصور · الأسعار · ساعات العمل · الورديات · المرافق · عن المساحة · الموقع · التواصل.

## The header (approved 2026-11-08)

- **H1 — a summary, not a section:** no «تعديل»; the name is edited in «عن المساحة», the cover in «الصور».
- **H2 — content:** the cover (small, beside; without photos the space's letter tile and «أضف صورة غلاف», which goes
  to «الصور»); the name, large; «{المنطقة}، {المحافظة} · موثّقة»; «عرض الصفحة العامة» (new tab) and **«نسخ الرابط»**
  (new); **اكتمال الملف** — a progress bar «N من 7 أقسام» (الصور، الأسعار، الساعات، المرافق، عن المساحة، الموقع،
  التواصل) and one line listing only what is missing or stale, each part a link to its section; when all is complete
  and fresh: «الملف مكتمل ومحدّث».
- **H3 — phone:** the cover full width on top, then the name and its line, the two buttons full width, the bar.
- **H4 — the admin's header** adds «غير موثّقة» (no owner) and «مخفية عن الزوار» (hidden); the admin's actions (hide,
  delete) stay in the page's top bar.

## الصور (approved 2026-11-08, with the owner's changes)

- **P1 — view:** desktop, the cover large (about two thirds) beside a 2×2 grid, the last tile «+N» past five; the
  head «الصور · 6 من 10 صور» and **«إدارة الصور»**; phone, the cover full width and a row of thumbnails scrolling
  sideways; no photos: «لم تُضف صور بعد», «أول صورة تكون غلاف مساحتك في الدليل», «أضف صورًا». No date, no staleness.
- **P2 — editing happens in the same section (the owner's change):** «إدارة الصور» turns the section itself into its
  edit state — **no Sheet** for photos; «تم» returns it to view. Each change saves at once.
- **P3 — the edit state:** «اختر صورًا» (several at once; camera or gallery on a phone) with the limits «حتى 10 صور ·
  JPEG أو PNG أو WebP · حتى 4 ميجابايت للصورة»; a progress bar per upload; a refused file says why under it, the others
  go on; at 10 photos the button is replaced by «وصلت الحد الأقصى (10 صور). احذف صورة لتضيف غيرها» (never disabled
  without a reason).
- **P4 — order by dragging only (the owner's change):** no move buttons; dragging a photo to the first place makes it
  the cover. (Keyboard and screen-reader users still need a way: the drag library's keyboard mode — pick up, arrows,
  drop — without visible buttons. A drag-and-drop library is a new dependency: the owner approves it at the plan.)
  **Settled 2026-11-08:** the design must serve keyboard and screen-reader users as well as dragging (pick up, move,
  drop from the keyboard, each step announced); **a drag-and-drop dependency is approved** (the plan names the
  library and why: touch, keyboard, RTL, size).
- **P5 — delete asks first (the owner's change):** a confirmation dialog «حذف هذه الصورة؟» with **«حذف»**
  (destructive) and a dismiss button. The project's rule (P9, 2026-10-11) says every dismiss reads **«رجوع»**, «إلغاء»
  being kept for voiding a payment. **Settled 2026-11-08: the project's rule stands — «حذف» and «رجوع».**
- **P6 — the cover is always marked:** a «الغلاف» badge on the first photo, in view and edit alike, and in the edit
  state the hint «اسحب صورة إلى الأول لتصبح الغلاف».
- **P7 — the admin's editor:** the same.

## الأسعار (approved 2026-11-08 — "on condition the design is logical and comfortable")

- **R1 — edited in the profile only.** The prices are edited from the space profile's «الأسعار» section (its Sheet),
  nowhere else: «الباقات والأسعار» keeps the packages, shows the prices read-only with «تعديل الأسعار في ملف
  المساحة». One place per fact (two editors invite confusion and stale overwrites). Revises O1/O6.
- **R2 — the data model stays** (audience: everyone / students; optional shift; the public page, the «أسعار
  للطلاب» filter and the desk's subscribe-from-a-published-price keep working). The owner's idea — students and
  shifts only as packages, prices = period + amount — was weighed and **not taken**: packages are private (D7), so
  visitors would lose student prices, the directory's students filter would break, the desk's published-price
  subscriptions would change, and the prices table would need a migration.
- **R3 — the Sheet, simple by default:** four rows — «بالساعة · يومي · أسبوعي · شهري» — each one amount field in
  shekels («اترك الخانة فارغة إذا لا تقدّم هذه الفترة»). Below, two optional boxes, off by default:
  «عندي أسعار خاصة للطلاب» (adds a «للطلاب» column, «للجميع» heading the first) and «أسعاري تختلف حسب الوردية»
  (adds tabs above the grid: «كل اليوم» then each shift of the space). Turning a box off with values in it asks before
  clearing them. The custom description leaves the main screen (kept only if the plan finds data that uses it — an
  executor check). Footer: «حفظ» and «رجوع».
- **R4 — view:** a small table, period and price; a «للطلاب» column only when student prices exist; shift prices
  under the shift's name only when they exist.
- **R5 — the admin's editor:** the same.
- **Revised the same day (the owner: the four-field Sheet is comfortable but less customisable — "the earlier design
  is better"): R3 and R4 are replaced by R6–R9.**
- **R6 — rows, as today, without the custom description:** each price is one row — «الفترة» (ساعة · يوم · أسبوع ·
  شهر) · «لمن» (الجميع · الطلاب) · «الوردية» (only when the space has shifts; «بدون وردية» first) · «المبلغ» (₪) ·
  remove. Desktop: one header line for the columns, the rows under it; phone: each row a small stacked block.
- **R7 — start with one row:** an empty section says «لم تُضف أسعار بعد» with «إضافة سعر»; the Sheet opens with one
  row; «إضافة سعر» adds the next, prefilled with the first period not yet priced for «الجميع» (then the students').
  Removing a row inside the Sheet is immediate (nothing is saved until «حفظ»).
- **R8 — the word is «سعر», not «اشتراك»:** in Masaha «اشتراك» is a customer's subscription at the desk (and the
  packages it is made from); an hourly or daily rate is not one. The section is «الأسعار المعلنة»; the button
  «إضافة سعر». (The supervisor's recommendation, given to the owner 2026-11-08.)
- **R9 — rules on the rows:** the same period + audience + shift twice is said on the second row («هذا السعر مضاف
  من قبل»); an empty amount is said on its row; the footer «حفظ» and «رجوع». View: a small table — the period, the
  price, «للطلاب» and the shift only where they exist.

## ساعات العمل (approved 2026-11-08, with the owner's improvements)

- **W1 — view:** days with the same hours grouped on one line («السبت – الخميس 08:00–18:00», «الجمعة: مغلقة»), today
  marked «اليوم»; a small link «إغلاق مؤقت؟ أضف إعلان إغلاق» to the announcements (a closure affects «مفتوحة الآن»);
  without hours «ساعات العمل غير متوفرة» and «أضف ساعات العمل».
- **W2 — the Sheet serves the majority first (the owner's idea):** one line «من السبت إلى الخميس» with «من [ ] إلى
  [ ]», «الجمعة: إجازة», and «تخصيص الأيام».
- **W3 — Friday in the simple view (the owner's improvement):** a box «مفتوحة يوم الجمعة أيضًا»; checked, Friday gets
  **its own «من / إلى»** right there (prefilled with the main hours, the owner sets his own — in Gaza most spaces open
  after the Friday prayer, around 12:00–13:00; no time is imposed).
- **W4 — «تخصيص الأيام»:** the full week, seven rows prefilled from the simple view, each day «مفتوحة / إجازة» and
  its own opening and closing. Saved hours that differ from day to day (beyond the Friday case) open the Sheet in
  this mode directly; going back to the simple view with differing days asks «سيتم توحيد الساعات لكل الأيام.
  متابعة؟».
- **W5 — times are chosen, not typed:** a list every 30 minutes. A day switched on takes the hours of the last open
  day edited. «نسخ إلى كل الأيام» goes. «إلى» must follow «من», said on the row. Overnight ranges follow the data
  model (the directory worker checks it). Footer «حفظ» / «رجوع». Phone: each day a small block. Admin: the same.

## الورديات (approved 2026-11-08 — a section of its own, after the hours)

- **S1 — why apart:** an owner makes a shift to sell something (a price, a package), not to say when he opens; most
  spaces have none, so it must not burden everyone's hours screen.
- **S2 — view:** the shifts on one line («الصباحية 08:00–13:00 · المسائية 13:00–20:00») and «تعديل»; none: «لا توجد
  ورديات. الورديات اختيارية، تحتاجها إذا كانت لديك أسعار أو باقات لفترات محددة من اليوم» with «إضافة وردية».
- **S3 — the Sheet:** rows (name, «من», «إلى» from the 30-minute lists) and «إضافة وردية»; a shift inside the hours of
  at least one open day; a shift used by a price or a package cannot be removed and says why on its row («هذه الوردية
  مستخدمة في سعر أو باقة، أزلها منها أولًا»).
- **S4 — with the prices:** the prices Sheet shows «الوردية» only when shifts exist; otherwise a small link «أضف
  وردية» to this section.
- **S5 — executor check:** the API keeps hours and shifts as one group with one date — confirm the shifts can be
  saved from their own Sheet without touching the hours (as for «عن المساحة» / «الموقع»).

## المرافق (approved 2026-11-08)

- **A1 — view: only what the space offers** — each with its icon and name, a grid of three columns (two on a phone),
  as on the public page; never a "not available" list; the space's own amenities after the catalogue's, a generic
  icon; none: «لم تُضف مرافق بعد» and «أضف المرافق».
- **A2 — the Sheet:** the catalogue as checkboxes with their icons (two columns, one on a phone), the whole row
  clickable; a retired amenity the space still holds stays listed and marked until unticked (as today); below,
  «مرافق أخرى» as rows (the Arabic name, the English optional, remove) with «إضافة مرفق آخر»; a row naming a
  catalogue amenity says «هذا المرفق موجود في القائمة، اختره من فوق»; footer «حفظ» / «رجوع». Admin: the same.
## عن المساحة (approved 2026-11-08)

- **B1 — view:** two columns on a desktop, «بالعربية» and «بالإنجليزية» (stacked on a phone), each the name then the
  description in its own direction; a long description shows four lines and «عرض المزيد»; a missing language says its
  effect («الوصف بالإنجليزية لم يُضف. زوار الموقع بالإنجليزية لن يروا وصفًا لمساحتك»).
- **B2 — the Sheet:** the two names side by side, then the two descriptions; «مطلوب» on the English name, «اختياري»
  on the rest; a character counter under each description («320 / 1000»); Arabic fields RTL, English LTR; under the
  English name «تغيير الاسم لا يغيّر رابط صفحتك» (the slug never changes, spaces.md); footer «حفظ» / «رجوع». Admin:
  the same. (Executor check G-open: «عن المساحة» and «الموقع» share one API group — a save of one never clears the
  other.)

## الموقع (approved 2026-11-08)

- **L1 — view:** «{المنطقة}، {المحافظة}»; the address in the interface's language with the other muted under it; the
  landmark when set; a small read-only map with the pin and «فتح في خرائط Google» (the visitors' directions link); a
  missing English address says its effect, as in «عن المساحة».
- **L2 — the Sheet:** the area — a searchable list grouped by governorate, one choice; the address and the landmark,
  Arabic and English side by side (English «اختياري»); a large map (full width on a phone), the pin dragged or placed
  by a tap; **«استخدم موقعي الحالي»** (the owner is often at the space; the pin moves there, then can be adjusted); a pin
  outside the Strip says «الموقع خارج قطاع غزة» (the server refuses it too); no address search (OpenStreetMap is weak on
  Gaza's addresses); footer «حفظ» / «رجوع». Admin: the same.

## التواصل (approved 2026-11-08 — the last section)

- **C1 — view:** one line each — its icon, its type's name, the value (numbers and links LTR-isolated), the value a
  working link (WhatsApp opens the chat, a phone calls, an email writes), so the owner tests each as a visitor would;
  none: «لم تُضف وسائل تواصل بعد. الزوار لن يجدوا طريقة للتواصل معك» and «أضف وسيلة تواصل». Types: واتساب، هاتف،
  بريد إلكتروني، إنستغرام، فيسبوك، تيك توك، موقع إلكتروني (up to 20).
- **C2 — the Sheet:** rows (the type from a list with icons, the value, remove) and «إضافة وسيلة تواصل»; a new row
  starts as WhatsApp; a placeholder per type («0599123456», «اسم الحساب أو الرابط», «https://…»); the value is
  normalised as today (Arabic-Indic digits, long Facebook links), an invalid one says why on its row («رقم الواتساب
  غير صحيح»); **reordered by dragging, keyboard included** (as the photos; the first is shown first to visitors); a
  duplicate says «هذه الوسيلة مضافة من قبل»; footer «حفظ» / «رجوع». Admin: the same.

## After the mock-up (approved 2026-11-08 — "very pleased, approved officially", with two notes)

The owner tried `mockup\index.html` and approved it officially. Two changes, built into the mock-up:

- **M1 — photos on a phone, without crowding:** the cover 16:9 full width with «الغلاف» and «N صور», then **one row of
  small thumbnails (96×72) scrolling sideways** — no stacked full-width photos, no «+N» on a phone (desktop keeps the
  cover beside a 2×2 grid with «+N»). Replaces P1's phone line.
- **M2 — the header on a phone:** the cover becomes a small square (64 px) beside the name, since «الصور» shows the
  large cover right below (two large covers stacked were crowded). Replaces H3's "cover full width". Below the
  cover and the name, the two buttons and the completeness bar take **the card's full width** (the mock-up squeezed
  them into the name's column and they overflowed — a mock-up bug, not the design).
- **M3 — contacts shown like the amenities:** a grid of tiles (three columns, two on a phone), each tile an icon,
  the type's name and the value small under it, the whole tile a working link. Replaces C1's lines.
- **M4 — any contact the owner has:** more types — تيليجرام، X (تويتر)، لينكدإن، يوتيوب — and **«وسيلة أخرى»**: its
  own name (e.g. «ديسكورد») and its link or number. This changes `CONTACT_TYPES` in `packages/shared` and very likely
  the database (an enum and a name column): the plan names the migration for the owner to approve.

**All sections decided (2026-11-08).** Next: an HTML mock-up of the whole page with its Sheets for the owner to see
(he asked for it), then the prototype round, then production.

## Before production (2026-11-09 — the prototype round merged as #138 at 7fb73c3c)

The prototype plan's three proposed alternatives, decided one by one before the production plan:

- **X1 — a shift's English name (approved, the supervisor's recommendation):** each shift row in the Sheet has an
  optional English name beside the Arabic one, as «مرافق أخرى» does; empty, the English interface shows the Arabic
  name. The API already has `nameEn` optional: no migration. Revises S3's "one name".
- **X2 — «عن المساحة» complete (approved, the supervisor's recommendation):** the section counts as complete in
  «اكتمال الملف» only when it has an **Arabic description** (the public page's main text); the English description
  stays optional (B2) and its absence is said by the section's effect line only, never by the bar. Revises the
  prototype's "complete with the name alone".
- **X3 — the admin's unverified alert (approved, the supervisor's recommendation):** dropped; the header's «غير موثّقة»
  badge (H4) says it. In the spirit of G4.
- **A3 — deferred by the owner (2026-11-09):** where «قاعة للنساء» / «للنساء فقط» and the owner-declared «دوام مسائي»
  live in the profile is **not decided**; it is decided with the women + evening task. The production plan neither
  builds nor reserves a place for them, and assumes nothing about them.

- **A3 — later:** where «قاعة للنساء» and the owner-declared evening hours live (here, or a «مزايا المساحة» section)
  is decided with that task, not built now.
