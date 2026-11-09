# SPACE_PROFILE — the space profile in production — PLAN (2_PLAN_PROD)

> Planner: Claude Code (Opus 5.5), 2026-11-09, on `main` at `7fb73c3c` (clean, = `origin/main`).
> Executed later by a fresh Claude Code session. Every number below (§, SD, DI, EC, T, OD, R) is
> referenced by the others; the executor follows them in order and escalates rather than deviates.

## 1. Summary

The owner's «ملف المساحة» (`/dashboard/spaces/:spaceId/profile`) and the admin's space editor
(`/dashboard/admin/spaces/:spaceId`) become one **view-first** page, as the prototype (#138) shows:
a header that summarises the space (cover, name, place, verified, «عرض الصفحة العامة», «نسخ الرابط»,
«اكتمال الملف» N of 7), a side index from 1024 px, and eight sections in the public page's order —
الصور · الأسعار المعلنة · ساعات العمل · الورديات · المرافق · عن المساحة · الموقع · التواصل — each shown
as a visitor sees it and edited in its own **Sheet** (the photos in place). Prices move into the
profile (Packages & prices shows them read-only). Photos and contacts are ordered by **dragging**,
the keyboard included, through an approved dependency (**dnd-kit**). Contacts gain **Telegram, X,
LinkedIn, YouTube** and **«وسيلة أخرى»** with its own name — the one approved **migration**.

Three PRs (OD1): **#140** contacts of any kind (shared + API + migration + the web's minimum),
**#141** the design system's sortable list (the dependency), **#142** the profile itself (web).

## 2. The contract

### Scope
- **PR-A (#140):** `CONTACT_TYPES` + the four networks' and «وسيلة أخرى»'s rules in `@masaha/shared`;
  `Contact.label`; the migration (enum values, `label` column, its `CHECK`); the API storing,
  auditing and answering the label (admin, managed and public reads); the contact and map links
  moved to `shared/lib` (one rule for the public page and the profile); the web's catalogues and
  the public page for the new types; the current editor offers the four networks (not «وسيلة أخرى»
  yet, which needs its name field: PR-C).
- **PR-B (#141):** `@dnd-kit/core` + `@dnd-kit/sortable` + `@dnd-kit/utilities` wrapped once in the
  design system as `Sortable` (a fourth entry, `@shared/design-system/sortable`), with a keyboard mode
  of its own (SD3), its own chunk held out of the site's first download, the ESLint restriction,
  the showcase section, `foundation.md`.
- **PR-C (#142):** the new page for both places; every section's view and Sheet; photos' edit state
  with drag; contacts' Sheet with drag and «وسيلة أخرى»; prices edited in the profile only and shown
  read-only on Packages & prices; every link that edits prices or a section re-aimed; reports'
  notices inside their sections; the admin's hide/delete in the top bar (H4); documents.

### Acceptance criteria (each proven by a test of §9 or a check of §12)
1. G1–G5, H1–H4 (with M2), P1–P7 (with M1), R1, R2, R5–R9, W1–W5, S1–S5 (with X1), A1–A2, B1–B2
   (with X2), L1–L2, C1–C2 (with M3–M4), X3 are built as §4 states them.
2. A Sheet's save sends only its section's part: «عن المساحة» and «الموقع» each a `PATCH` of their own
   changed fields; «ساعات العمل» the new week with the saved shifts unchanged; «الورديات» the saved week
   unchanged with the new shifts (T31–T33).
3. «وسيلة أخرى» is stored with its name; the four networks in their one form; existing contacts
   untouched (T1–T13, EC5).
4. Packages & prices shows the prices read-only; every edit link lands on the profile's «الأسعار
   المعلنة» (T46–T47).
5. Keyboard and screen reader: pick up / move / drop / cancel, each announced, for photos and
   contacts; axe-clean in view, Sheet and edit states, both languages (T28, T38, T41, T48).
6. `check:build` holds dnd-kit out of the site's first download (§12).
7. Every lane green locally and in CI; the report saved.

### Out of scope
- Anything on *Not in v1* (no booking, reviews, QR, payment, in-app claiming).
- **A3:** «قاعة للنساء» / «للنساء فقط» and the owner-declared «دوام مسائي»: nothing built, nothing
  reserved (no empty section, no flag, no copy line).
- The add-space page (keeps `AreaSelect` and its form, #57), the admin's spaces list, the directory's
  own screens beyond the contact links (PR-A), packages' own editor, the desk.
- Any API change beyond contacts (none is needed: §5 settles S5/B2/L2 by reading).
- An address search on the map (L2), a shift's place in hours (S1).

## 3. Reading done

`CLAUDE.md`; `docs/development/workflow.md`, `engineering-principles.md`, `testing.md`; `docs/README.md`;
`docs/features/spaces.md` (whole); `docs/architecture/data-model.md` (conventions, contacts, times,
CHECKs); `docs/api/api-contract.md` (§ spaces the admin: shapes, PATCH, hours, prices, contacts,
confirm, photos; managed routes); `docs/frontend/design-system/foundation.md` (§3, §9–§13); the findings
index (open: 23, 65, 152, 215; next free **216**); `docs/design/README.md`, `CHANGES.md` › Refactor 2,
`INDEX.md` §58; the prototype: `Owner space profile.html`, `Admin space edit.html`, `Packages.html`,
`Owner settings.html` (pricing link), `masaha/profile-a.jsx`, `profile-b.jsx`, `profile-c.jsx`,
`owner-data.js`, `masaha.css` (`.pf-*`), `shared.jsx` (`PageActions`); `0_OWNER_DECISIONS.md` whole.
Code: `features/spaces/**` (editor, sections, hooks, services, repository, index), the three pages
(`admin/SpaceEditPage`, `space/ProfilePage`, `space/PackagesPage`), `pages/dashboard/fieldSections.ts`,
`OverviewPage`, `AuditPage`, `SettingsPage`/`PricingCard`, `features/data-reports` notice
(`noticeGroup.ts`, `ReportNoticeView`), `features/lookups` (exports, `AreaSelect`, `AmenityChecklist`,
`AmenityIcon`), `features/directory/services/contactLinks.ts` and `useSpacePage.ts`, `features/packages`
exports, `shared/map` (PointPicker drags, PlaceMap), `shared/lib`, the design system (components,
icons, `GlyphIcon`, Sheet), `apps/web/scripts/checkBuild.ts` + `libraryChunks.ts`, `package.json`;
`packages/shared/src/spaces/{contacts,requests,responses}.ts`, `core/fields.ts`;
`apps/api/src/modules/spaces/{facts/groupEdit,facts/facts,contacts/*,hours/hours.service}.ts`, the
Prisma `ContactType` and `SpaceContact`, the migrations' CHECK precedent. The test helpers
(`fakeGeolocation`, `screenWidth`, `fakeIntersectionObserver`, `findToast`, `fakeAdapter`).
**Not read** (the executor reads them where its commit needs them): `frontend/architecture.md` §7 and
*Forms* (to follow `useServerForm`), `backend/conventions.md` §6 (audit), `localisation.md`
(formatting, isolation), `packages.md`, `data-reports.md`, `overview.md`, `space-settings.md`,
`lookups.md`, `directory.md`, the glossary.

## 4. The owner's decisions — binding (word for word from `0_OWNER_DECISIONS.md`)

> ## The page
>
> - **G1 — view first.** Each section shows its facts as a visitor sees them, with no field; editing is asked for. The
>   edit surface is a **Sheet** per section (approved in principle 2026-11-05), except where a section says otherwise.
> - **G2 — the order follows the public page:** the header · الصور · الأسعار · ساعات العمل والورديات · المرافق · عن
>   المساحة · الموقع · التواصل.
> - **G3 — a section's head:** its title, «آخر تحديث قبل N أيام» (muted), «تعديل». A stale group shows «قد تكون قديمة»
>   and «ما زالت صحيحة» (confirms without editing). An empty section shows «لم تُضف بعد» and a clear action («أضف ساعات
>   العمل»…). Visitors' reports about a section show inside it. Desktop: a side index of the sections with a state dot
>   (complete / stale / missing); phone: no index.
> - **G4 — gone from the top of the page:** «كل قسم يُحفظ وحده…», the missing-items checklist (the header replaces it),
>   the page-level unsaved-changes alert (a Sheet asks before discarding).
> - **G5 — the admin's space editor takes the same design** in the same task.
> - **Settled later the same day:** prices are edited in the profile (R1); «عن المساحة» and «الموقع» are two sections
>   (B2/L2), «الورديات» a section of its own (S1) — each pair over one API group: an executor check on partial saves.
>   The final order: the header · الصور · الأسعار · ساعات العمل · الورديات · المرافق · عن المساحة · الموقع · التواصل.
>
> ## The header (approved 2026-11-08)
>
> - **H1 — a summary, not a section:** no «تعديل»; the name is edited in «عن المساحة», the cover in «الصور».
> - **H2 — content:** the cover (small, beside; without photos the space's letter tile and «أضف صورة غلاف», which goes
>   to «الصور»); the name, large; «{المنطقة}، {المحافظة} · موثّقة»; «عرض الصفحة العامة» (new tab) and **«نسخ الرابط»**
>   (new); **اكتمال الملف** — a progress bar «N من 7 أقسام» (الصور، الأسعار، الساعات، المرافق، عن المساحة، الموقع،
>   التواصل) and one line listing only what is missing or stale, each part a link to its section; when all is complete
>   and fresh: «الملف مكتمل ومحدّث».
> - **H3 — phone:** the cover full width on top, then the name and its line, the two buttons full width, the bar.
> - **H4 — the admin's header** adds «غير موثّقة» (no owner) and «مخفية عن الزوار» (hidden); the admin's actions (hide,
>   delete) stay in the page's top bar.
>
> ## الصور (approved 2026-11-08, with the owner's changes)
>
> - **P1 — view:** desktop, the cover large (about two thirds) beside a 2×2 grid, the last tile «+N» past five; the
>   head «الصور · 6 من 10 صور» and **«إدارة الصور»**; phone, the cover full width and a row of thumbnails scrolling
>   sideways; no photos: «لم تُضف صور بعد», «أول صورة تكون غلاف مساحتك في الدليل», «أضف صورًا». No date, no staleness.
> - **P2 — editing happens in the same section (the owner's change):** «إدارة الصور» turns the section itself into its
>   edit state — **no Sheet** for photos; «تم» returns it to view. Each change saves at once.
> - **P3 — the edit state:** «اختر صورًا» (several at once; camera or gallery on a phone) with the limits «حتى 10 صور ·
>   JPEG أو PNG أو WebP · حتى 4 ميجابايت للصورة»; a progress bar per upload; a refused file says why under it, the others
>   go on; at 10 photos the button is replaced by «وصلت الحد الأقصى (10 صور). احذف صورة لتضيف غيرها» (never disabled
>   without a reason).
> - **P4 — order by dragging only (the owner's change):** no move buttons; dragging a photo to the first place makes it
>   the cover. (Keyboard and screen-reader users still need a way: the drag library's keyboard mode — pick up, arrows,
>   drop — without visible buttons. A drag-and-drop library is a new dependency: the owner approves it at the plan.)
>   **Settled 2026-11-08:** the design must serve keyboard and screen-reader users as well as dragging (pick up, move,
>   drop from the keyboard, each step announced); **a drag-and-drop dependency is approved** (the plan names the
>   library and why: touch, keyboard, RTL, size).
> - **P5 — delete asks first (the owner's change):** a confirmation dialog «حذف هذه الصورة؟» with **«حذف»**
>   (destructive) and a dismiss button. The project's rule (P9, 2026-10-11) says every dismiss reads **«رجوع»**, «إلغاء»
>   being kept for voiding a payment. **Settled 2026-11-08: the project's rule stands — «حذف» and «رجوع».**
> - **P6 — the cover is always marked:** a «الغلاف» badge on the first photo, in view and edit alike, and in the edit
>   state the hint «اسحب صورة إلى الأول لتصبح الغلاف».
> - **P7 — the admin's editor:** the same.
>
> ## الأسعار (approved 2026-11-08 — "on condition the design is logical and comfortable")
>
> - **R1 — edited in the profile only.** The prices are edited from the space profile's «الأسعار» section (its Sheet),
>   nowhere else: «الباقات والأسعار» keeps the packages, shows the prices read-only with «تعديل الأسعار في ملف
>   المساحة». One place per fact (two editors invite confusion and stale overwrites). Revises O1/O6.
> - **R2 — the data model stays** (audience: everyone / students; optional shift; the public page, the «أسعار
>   للطلاب» filter and the desk's subscribe-from-a-published-price keep working). The owner's idea — students and
>   shifts only as packages, prices = period + amount — was weighed and **not taken**: packages are private (D7), so
>   visitors would lose student prices, the directory's students filter would break, the desk's published-price
>   subscriptions would change, and the prices table would need a migration.
> - **R3 — the Sheet, simple by default:** four rows — «بالساعة · يومي · أسبوعي · شهري» — each one amount field in
>   shekels («اترك الخانة فارغة إذا لا تقدّم هذه الفترة»). Below, two optional boxes, off by default:
>   «عندي أسعار خاصة للطلاب» (adds a «للطلاب» column, «للجميع» heading the first) and «أسعاري تختلف حسب الوردية»
>   (adds tabs above the grid: «كل اليوم» then each shift of the space). Turning a box off with values in it asks before
>   clearing them. The custom description leaves the main screen (kept only if the plan finds data that uses it — an
>   executor check). Footer: «حفظ» and «رجوع».
> - **R4 — view:** a small table, period and price; a «للطلاب» column only when student prices exist; shift prices
>   under the shift's name only when they exist.
> - **R5 — the admin's editor:** the same.
> - **Revised the same day (the owner: the four-field Sheet is comfortable but less customisable — "the earlier design
>   is better"): R3 and R4 are replaced by R6–R9.**
> - **R6 — rows, as today, without the custom description:** each price is one row — «الفترة» (ساعة · يوم · أسبوع ·
>   شهر) · «لمن» (الجميع · الطلاب) · «الوردية» (only when the space has shifts; «بدون وردية» first) · «المبلغ» (₪) ·
>   remove. Desktop: one header line for the columns, the rows under it; phone: each row a small stacked block.
> - **R7 — start with one row:** an empty section says «لم تُضف أسعار بعد» with «إضافة سعر»; the Sheet opens with one
>   row; «إضافة سعر» adds the next, prefilled with the first period not yet priced for «الجميع» (then the students').
>   Removing a row inside the Sheet is immediate (nothing is saved until «حفظ»).
> - **R8 — the word is «سعر», not «اشتراك»:** in Masaha «اشتراك» is a customer's subscription at the desk (and the
>   packages it is made from); an hourly or daily rate is not one. The section is «الأسعار المعلنة»; the button
>   «إضافة سعر». (The supervisor's recommendation, given to the owner 2026-11-08.)
> - **R9 — rules on the rows:** the same period + audience + shift twice is said on the second row («هذا السعر مضاف
>   من قبل»); an empty amount is said on its row; the footer «حفظ» and «رجوع». View: a small table — the period, the
>   price, «للطلاب» and the shift only where they exist.
>
> ## ساعات العمل (approved 2026-11-08, with the owner's improvements)
>
> - **W1 — view:** days with the same hours grouped on one line («السبت – الخميس 08:00–18:00», «الجمعة: مغلقة»), today
>   marked «اليوم»; a small link «إغلاق مؤقت؟ أضف إعلان إغلاق» to the announcements (a closure affects «مفتوحة الآن»);
>   without hours «ساعات العمل غير متوفرة» and «أضف ساعات العمل».
> - **W2 — the Sheet serves the majority first (the owner's idea):** one line «من السبت إلى الخميس» with «من [ ] إلى
>   [ ]», «الجمعة: إجازة», and «تخصيص الأيام».
> - **W3 — Friday in the simple view (the owner's improvement):** a box «مفتوحة يوم الجمعة أيضًا»; checked, Friday gets
>   **its own «من / إلى»** right there (prefilled with the main hours, the owner sets his own — in Gaza most spaces open
>   after the Friday prayer, around 12:00–13:00; no time is imposed).
> - **W4 — «تخصيص الأيام»:** the full week, seven rows prefilled from the simple view, each day «مفتوحة / إجازة» and
>   its own opening and closing. Saved hours that differ from day to day (beyond the Friday case) open the Sheet in
>   this mode directly; going back to the simple view with differing days asks «سيتم توحيد الساعات لكل الأيام.
>   متابعة؟».
> - **W5 — times are chosen, not typed:** a list every 30 minutes. A day switched on takes the hours of the last open
>   day edited. «نسخ إلى كل الأيام» goes. «إلى» must follow «من», said on the row. Overnight ranges follow the data
>   model (the directory worker checks it). Footer «حفظ» / «رجوع». Phone: each day a small block. Admin: the same.
>
> ## الورديات (approved 2026-11-08 — a section of its own, after the hours)
>
> - **S1 — why apart:** an owner makes a shift to sell something (a price, a package), not to say when he opens; most
>   spaces have none, so it must not burden everyone's hours screen.
> - **S2 — view:** the shifts on one line («الصباحية 08:00–13:00 · المسائية 13:00–20:00») and «تعديل»; none: «لا توجد
>   ورديات. الورديات اختيارية، تحتاجها إذا كانت لديك أسعار أو باقات لفترات محددة من اليوم» with «إضافة وردية».
> - **S3 — the Sheet:** rows (name, «من», «إلى» from the 30-minute lists) and «إضافة وردية»; a shift inside the hours of
>   at least one open day; a shift used by a price or a package cannot be removed and says why on its row («هذه الوردية
>   مستخدمة في سعر أو باقة، أزلها منها أولًا»).
> - **S4 — with the prices:** the prices Sheet shows «الوردية» only when shifts exist; otherwise a small link «أضف
>   وردية» to this section.
> - **S5 — executor check:** the API keeps hours and shifts as one group with one date — confirm the shifts can be
>   saved from their own Sheet without touching the hours (as for «عن المساحة» / «الموقع»).
>
> ## المرافق (approved 2026-11-08)
>
> - **A1 — view: only what the space offers** — each with its icon and name, a grid of three columns (two on a phone),
>   as on the public page; never a "not available" list; the space's own amenities after the catalogue's, a generic
>   icon; none: «لم تُضف مرافق بعد» and «أضف المرافق».
> - **A2 — the Sheet:** the catalogue as checkboxes with their icons (two columns, one on a phone), the whole row
>   clickable; a retired amenity the space still holds stays listed and marked until unticked (as today); below,
>   «مرافق أخرى» as rows (the Arabic name, the English optional, remove) with «إضافة مرفق آخر»; a row naming a
>   catalogue amenity says «هذا المرفق موجود في القائمة، اختره من فوق»; footer «حفظ» / «رجوع». Admin: the same.
> ## عن المساحة (approved 2026-11-08)
>
> - **B1 — view:** two columns on a desktop, «بالعربية» and «بالإنجليزية» (stacked on a phone), each the name then the
>   description in its own direction; a long description shows four lines and «عرض المزيد»; a missing language says its
>   effect («الوصف بالإنجليزية لم يُضف. زوار الموقع بالإنجليزية لن يروا وصفًا لمساحتك»).
> - **B2 — the Sheet:** the two names side by side, then the two descriptions; «مطلوب» on the English name, «اختياري»
>   on the rest; a character counter under each description («320 / 1000»); Arabic fields RTL, English LTR; under the
>   English name «تغيير الاسم لا يغيّر رابط صفحتك» (the slug never changes, spaces.md); footer «حفظ» / «رجوع». Admin:
>   the same. (Executor check G-open: «عن المساحة» and «الموقع» share one API group — a save of one never clears the
>   other.)
>
> ## الموقع (approved 2026-11-08)
>
> - **L1 — view:** «{المنطقة}، {المحافظة}»; the address in the interface's language with the other muted under it; the
>   landmark when set; a small read-only map with the pin and «فتح في خرائط Google» (the visitors' directions link); a
>   missing English address says its effect, as in «عن المساحة».
> - **L2 — the Sheet:** the area — a searchable list grouped by governorate, one choice; the address and the landmark,
>   Arabic and English side by side (English «اختياري»); a large map (full width on a phone), the pin dragged or placed
>   by a tap; **«استخدم موقعي الحالي»** (the owner is often at the space; the pin moves there, then can be adjusted); a pin
>   outside the Strip says «الموقع خارج قطاع غزة» (the server refuses it too); no address search (OpenStreetMap is weak on
>   Gaza's addresses); footer «حفظ» / «رجوع». Admin: the same.
>
> ## التواصل (approved 2026-11-08 — the last section)
>
> - **C1 — view:** one line each — its icon, its type's name, the value (numbers and links LTR-isolated), the value a
>   working link (WhatsApp opens the chat, a phone calls, an email writes), so the owner tests each as a visitor would;
>   none: «لم تُضف وسائل تواصل بعد. الزوار لن يجدوا طريقة للتواصل معك» and «أضف وسيلة تواصل». Types: واتساب، هاتف،
>   بريد إلكتروني، إنستغرام، فيسبوك، تيك توك، موقع إلكتروني (up to 20).
> - **C2 — the Sheet:** rows (the type from a list with icons, the value, remove) and «إضافة وسيلة تواصل»; a new row
>   starts as WhatsApp; a placeholder per type («0599123456», «اسم الحساب أو الرابط», «https://…»); the value is
>   normalised as today (Arabic-Indic digits, long Facebook links), an invalid one says why on its row («رقم الواتساب
>   غير صحيح»); **reordered by dragging, keyboard included** (as the photos; the first is shown first to visitors); a
>   duplicate says «هذه الوسيلة مضافة من قبل»; footer «حفظ» / «رجوع». Admin: the same.
>
> ## After the mock-up (approved 2026-11-08 — "very pleased, approved officially", with two notes)
>
> The owner tried `mockup\index.html` and approved it officially. Two changes, built into the mock-up:
>
> - **M1 — photos on a phone, without crowding:** the cover 16:9 full width with «الغلاف» and «N صور», then **one row of
>   small thumbnails (96×72) scrolling sideways** — no stacked full-width photos, no «+N» on a phone (desktop keeps the
>   cover beside a 2×2 grid with «+N»). Replaces P1's phone line.
> - **M2 — the header on a phone:** the cover becomes a small square (64 px) beside the name, since «الصور» shows the
>   large cover right below (two large covers stacked were crowded). Replaces H3's "cover full width". Below the
>   cover and the name, the two buttons and the completeness bar take **the card's full width** (the mock-up squeezed
>   them into the name's column and they overflowed — a mock-up bug, not the design).
> - **M3 — contacts shown like the amenities:** a grid of tiles (three columns, two on a phone), each tile an icon,
>   the type's name and the value small under it, the whole tile a working link. Replaces C1's lines.
> - **M4 — any contact the owner has:** more types — تيليجرام، X (تويتر)، لينكدإن، يوتيوب — and **«وسيلة أخرى»**: its
>   own name (e.g. «ديسكورد») and its link or number. This changes `CONTACT_TYPES` in `packages/shared` and very likely
>   the database (an enum and a name column): the plan names the migration for the owner to approve.
>
> **All sections decided (2026-11-08).** Next: an HTML mock-up of the whole page with its Sheets for the owner to see
> (he asked for it), then the prototype round, then production.
>
> ## Before production (2026-11-09 — the prototype round merged as #138 at 7fb73c3c)
>
> The prototype plan's three proposed alternatives, decided one by one before the production plan:
>
> - **X1 — a shift's English name (approved, the supervisor's recommendation):** each shift row in the Sheet has an
>   optional English name beside the Arabic one, as «مرافق أخرى» does; empty, the English interface shows the Arabic
>   name. The API already has `nameEn` optional: no migration. Revises S3's "one name".
> - **X2 — «عن المساحة» complete (approved, the supervisor's recommendation):** the section counts as complete in
>   «اكتمال الملف» only when it has an **Arabic description** (the public page's main text); the English description
>   stays optional (B2) and its absence is said by the section's effect line only, never by the bar. Revises the
>   prototype's "complete with the name alone".
> - **X3 — the admin's unverified alert (approved, the supervisor's recommendation):** dropped; the header's «غير موثّقة»
>   badge (H4) says it. In the spirit of G4.
> - **A3 — deferred by the owner (2026-11-09):** where «قاعة للنساء» / «للنساء فقط» and the owner-declared «دوام مسائي»
>   live in the profile is **not decided**; it is decided with the women + evening task. The production plan neither
>   builds nor reserves a place for them, and assumes nothing about them.
>
> - **A3 — later:** where «قاعة للنساء» and the owner-declared evening hours live (here, or a «مزايا المساحة» section)
>   is decided with that task, not built now.

**Two approvals already given (the prompt):** a drag-and-drop dependency (§6 names it), and the
contacts' new types with «وسيلة أخرى» need a migration (§7 shows its SQL).

**Precedence inside the list (stated, not silent):** M1 overrides P1's phone line; M2 overrides H3;
M3 overrides C1's lines; M4 extends C1's types to twelve; R6–R9 replace R3–R4; X1 revises S3's one
name; X2 revises the prototype's completeness of «عن المساحة»; X3 removes the admin's unverified alert
(the prototype still draws it — the decision wins).

### 4.1 How each decision is built (the executor's reading of them)

- **Sections and ids** (anchors, index, `?sheet=`): `photos`, `prices`, `hours`, `shifts`, `amenities`,
  `about`, `location`, `contacts`. Section → API group: about/location → `profile`; hours/shifts →
  `hours`; others their own; photos none.
- **Date, staleness, confirm (G3, S5, B2):** one date per group (the API's model, `DATE_COLUMNS`), so
  both sections of a pair show the same «آخر تحديث قبل N أيام» (Gaza days, `updatedAgo`) and the same
  «قد تكون قديمة»; «ما زالت صحيحة» appears only on a stale group's warning line (prototype), posts
  `…/{group}/confirm`, and clears the line on both sections of the pair. No confirm on a fresh section
  (a change from today's editor, recorded in spaces.md).
- **Completeness (H2, X2):** content-based, computed on the web from the space read and the gallery:
  الصور ≥ 1 photo; الأسعار ≥ 1 price; الساعات saved (`hours !== null`); المرافق ≥ 1 (platform or own);
  عن المساحة `descriptionAr` present (X2); الموقع always (its fields are required) unless stale;
  التواصل ≥ 1. Each part is `ok` / `stale` (its group stale) / `missing` (no content). The shifts are
  never counted; their index dot is «اختياري» when none. Until the gallery has loaded, the bar waits
  (a skeleton line), so it never says «6 من 7» then «7 من 7».
- **Empty state per section** (G3): shown when the section has no content (as the bar's `missing`),
  with its action opening its Sheet (photos: the edit state). A group saved empty (D2) is shown empty
  too; its date is not shown (prototype), the server's own missing/fresh model is unchanged.
- **A Sheet (G1):** end side, full width below 768 px (the layer's Sheet); its footer «حفظ» and «رجوع»;
  with changes, any close — «رجوع», the close button (named «رجوع»), Escape, the overlay, a link out of
  the Sheet — asks «تجاهل التغييرات؟» («تجاهل التغييرات» destructive, «رجوع» back to the Sheet with the
  focus on «حفظ»). It compares with what it opened on, so one opened on a default (the template week,
  one empty price row, one empty shift, one WhatsApp row) is not changed. Focus returns to the «تعديل»
  that opened it, or, when that button is gone (an empty section's action, after a first save), to the
  section's heading. An unchanged Sheet's «حفظ» on a saved group closes and sends nothing, with the toast
  «لم يتغيّر شيء» (D3: nothing is written); on a missing group it sends (D2 dates it, even empty).
  Saved: the toast names the section («حُفظ «ساعات العمل»، ويظهر للزوار الآن»); the Sheet closes; the
  section holds the server's answer. Refusals stay in the Sheet: field errors on their rows, the first
  focused; a 429 counts down on «حفظ»; a 403/404 says the place's words (#96) and the space is fetched
  again (a verified one turns read-only for the admin and the Sheet unmounts; a deleted one shows 404).
- **`?sheet=<section>`** opens that Sheet once the page has drawn (the prototype's deep link, used by
  R1's links), then the parameter is removed with `replace`, so Back and a reload never reopen it.
- **The leave guard:** no page-level alert (G4). The router's guard stays for an upload still running
  (its words, #85) and for a Sheet with changes when the route changes by Back or a link outside it:
  it asks with the Sheet's own words naming the section. Closing or reloading asks through the browser.
- **The header (H1, H2, M2, H4):** cover (`card` size) or the letter tile (the English name's first
  letter, `lang="en"`), «أضف صورة غلاف» (opens the photos' edit state and moves the focus to «اختر
  صورًا»), the name (`spaceNameOf`), «{area}، {governorate}» (lookups, by place's source) with
  «موثّقة» (owner always; admin «موثّقة» or «غير موثّقة») and «مخفية عن الزوار» when hidden; «عرض الصفحة
  العامة» (new tab) and «نسخ الرابط» (absolute URL, `location.origin + publicSpacePath(slug)`, on the
  clipboard; toast «نُسخ رابط الصفحة العامة»; when the clipboard refuses, an error toast that shows the
  link to copy by hand); «اكتمال الملف», the layer's `Meter` (`kind="meter"`, `valueText` «N من 7
  أقسام»), and one line of links «{section}: لم تُضف بعد» / «… قد تكون قديمة» or «الملف مكتمل ومحدّث».
  Phone (M2): a 64 px square cover beside the name, its link under the name, the two buttons and the
  bar at the card's full width.
- **Side index (G3):** from 1024 px only, a `nav` «أقسام الملف» of the eight sections, each with its
  dot (`success` complete · `warning` stale · `destructive` missing · `border` optional) and the state
  said to a screen reader; the section in view marked `aria-current="location"` (`useSectionInView`).
  No chips row on a phone (revises #74's S7).
- **Admin (G5, H4, X3):** the same page. A verified space: same view with no «تعديل», «ما زالت صحيحة»,
  «إدارة الصور» or empty-state actions; the notice «يعدّلها {names}» with the reports link and an unlink
  per owner (kept, #91, #132). An unverified space: **no alert** (X3); its «ربط مالك» moves to the header
  (DI-3). Top bar (H4): «إخفاء عن الزوار» / «إظهار للزوار» (immediate, toast with «تراجع») and «حذف
  المساحة» (asks; «حذف» / «رجوع»; then the spaces list `?status=deleted` with the Undo toast), as buttons
  from 768 px and a «إجراءات الصفحة» menu below (the prototype's `PageActions`); the privacy note last.
- **Photos (P1–P7, M1):** view: from 768 px the cover two thirds wide beside a 2×2 grid, «+N» on the
  fourth tile past five; below 768 px the cover 16:9 with «الغلاف» and «N صور», then one row of 96×72
  thumbnails scrolling sideways. Head: «N من 10 صور», «إدارة الصور» / «تم». Edit state: «اختر صورًا»
  (many, `accept="image/*"` — DI-7) with the limits line; uploads as today (#85, one at a time, a `Meter`
  per tile, refusals on their tile, retry only where it can work); at 10 the button gives way to the
  limit line; the grid is the layer's `Sortable` (grid): drag (mouse, touch) or keyboard; the first is
  «الغلاف»; the hint «اسحب صورة إلى الأول لتصبح الغلاف» with the keyboard's way; each drop sends the
  whole order once (`PUT …/photos/order`), the dropped order kept on screen while it is sent (SD2), a
  second move held until the gallery is fetched again; a delete button per tile → «حذف هذه الصورة؟»
  («حذف» destructive / «رجوع»), adding «الصورة التالية تصبح الغلاف» for the cover.
- **Prices (R1, R2, R6–R9, S4):** view: a small table, period · «لمن» (only with student prices) ·
  «الوردية» (only with shift prices) · price, a labelled row showing its label (kept, never edited),
  sorted as the prototype (no shift first, by period, everyone first); «للعرض فقط · الدفع في المساحة» and,
  for the owner, «تظهر في «الباقات والأسعار» للقراءة». Sheet «تعديل الأسعار المعلنة»: rows «الفترة» ·
  «لمن» · «الوردية» (only with saved shifts, «بدون وردية» first) · «المبلغ (₪)» · remove; one header line
  from 768 px, a stacked block per row below; one row to start; «إضافة سعر» prefilled (R7); a repeat
  said on the later row «هذا السعر مضاف من قبل»; an empty amount «أدخل المبلغ»; amounts as today (shekels,
  two decimals, Arabic digits read, sent as agorot); up to 40; no shifts → «تريد سعرًا لفترة من اليوم؟
  أضف وردية» (asks first if the prices changed, then opens the shifts' Sheet); none left → the line
  «لا أسعار. احفظ هكذا ليقول الدليل إن الأسعار غير متوفرة.»
- **Hours (W1–W5):** view: days grouped by equal ranges, Saturday first, «اليوم» on today's group (Gaza's
  weekday), «مغلقة»; the owner's «إغلاق مؤقت؟ أضف إعلان إغلاق» → the announcements page (DI-5). Sheet:
  simple mode (Sat–Thu one range, Friday box with its own range prefilled from the main hours) or
  «تخصيص الأيام» (seven blocks, switch + two times); saved hours not simple open in the custom mode;
  back to simple with differing days asks «سيتم توحيد الساعات لكل الأيام. متابعة؟»; times from 30-minute
  lists (ends to 24:00; a saved time off the grid kept in its list); a day switched on takes the last
  open day edited; «إلى» after «من» said on its row; no day open said once; a saved shift that the new
  week no longer holds is said before sending (DI-2). The request: the new week + the saved shifts as
  read (ids, names, times).
- **Shifts (S1–S5, X1):** view: one line «الصباحية 08:00–13:00 · المسائية 13:00–20:00» (each name in the
  interface's language, the Arabic when no English); none: the S2 lines and «إضافة وردية» (outline);
  without saved hours, the empty state says to add the hours first and its action opens the hours'
  Sheet (DI-1). Sheet «تعديل الورديات»: rows — Arabic name, English name (optional, X1), «من», «إلى» (the
  30-minute lists), remove — up to 10; the D4 rule (inside one open day; a helper naming the days it
  does not apply on); a repeated Arabic name; in use → remove disabled with S3's line, from the saved
  prices and, for the owner, the packages' shifts (SD5); a 409 (a subscription, a visit or a package the
  page cannot see) said in the Sheet, the space fetched again. The request: the saved week as read +
  the new shifts.
- **Amenities (A1–A2):** view: the offered ones only, the catalogue's (icon + name, platform order) then
  the own (a generic check icon), three columns, two on a phone. Sheet: the catalogue as checkbox rows
  with icons, two columns from 768 px, whole row clickable, a held retired one listed «أُزيل من القائمة»;
  «مرافق أخرى» rows (Arabic, English optional, remove), «إضافة مرفق آخر», up to 20; a row naming a
  catalogue amenity (either language, trimmed, case-insensitive) «هذا المرفق موجود في القائمة، اختره من
  فوق», checked in the browser only (the server's S4 stands); the admin's «إدارة قائمة المرافق» link
  (asks first when changed).
- **About (B1–B2, X2):** view: «بالعربية» / «بالإنجليزية» columns (stacked below 768 px), each the name
  then the description in its own `lang`/`dir`, four lines then «عرض المزيد» / «عرض أقل»
  (`aria-expanded`); a missing description says its effect; no Arabic name: «لم يُضف الاسم بالعربية.»
  Sheet: names side by side («مطلوب» on the English with «تغيير الاسم لا يغيّر رابط صفحتك»; «اختياري» on
  the rest), descriptions with a live counter «320 / 1000» (DI-6). Sends a `PATCH` of its changed fields.
- **Location (L1–L2):** view: «{area}، {governorate}», the address in the interface's language with the
  other muted (each in its `lang`/`dir`), the landmark, a missing English address's effect line, a
  small read-only map (`PlaceMap`) and «فتح في خرائط Google» (the shared maps link, PR-A). Sheet: the
  area as a searchable `Combobox` grouped by governorate (a new lookups field, SD6), addresses and
  landmarks side by side, a large `PointPicker` (tap places, drag moves — it already does), «استخدم
  موقعي الحالي» (§4.2), the coordinates field (#57), «الموقع خارج قطاع غزة» on it. Sends a `PATCH` of its
  changed fields.
- **Contacts (C1–C2, M3–M4):** view: tiles (three columns, two on a phone) — icon, type name («وسيلة
  أخرى»'s own name), the value small, LTR-isolated — each tile the shared contact link (WhatsApp chat,
  call, mail, the page in a new tab). Sheet «تعديل التواصل», «الأولى تظهر أولًا للزوار.»: rows — a drag
  handle (the keyboard's grip), the type (a `Select` with icons, twelve types), «اسم الوسيلة» for «وسيلة
  أخرى» («مثلًا: ديسكورد»), the value (a placeholder per type; «يُحفظ كـ …» as today; a phone's carrier),
  remove; a new row WhatsApp; per-type refusals (§11 copy list); a duplicate; up to 20; the order of the
  rows is the order saved on «حفظ».

### 4.2 What the prototype simulates, done for real

- **Touch drag:** dnd-kit's `TouchSensor` (press 250 ms, 5 px tolerance, so a phone still scrolls) and
  `PointerSensor` for a mouse (6 px before a drag starts, so a click on a tile's delete button stays a
  click); auto-scroll near the edges is dnd-kit's.
- **Keyboard drag:** the layer's own keyboard mode (SD3): Space or Enter lifts the focused item, the
  arrows move it (in a grid ArrowLeft/ArrowRight follow the reading direction, ArrowUp/Down by one; in a
  list only up/down), Home/End to the ends, Space/Enter drops, Escape puts it back; each step said in the
  layer's live region with the words the feature gives; Tab while lifted drops it where it is.
- **Geolocation:** `navigator.geolocation.getCurrentPosition` (`enableHighAccuracy`, a 10 s timeout); a
  point inside the Strip moves the pin and the coordinates and toasts «نُقل الدبوس إلى موقعك الحالي.
  عدّله إن لزم.»; outside, the coordinates field shows «الموقع خارج قطاع غزة» and the pin stays; refused,
  unavailable or timed out: «تعذّر معرفة موقعك. اسمح للمتصفح بمعرفة موقعك، أو ضع الدبوس على الخريطة.»;
  no `navigator.geolocation`: the button is not drawn. The seam is the browser's global, as `useNearMe`
  and `test/fakeGeolocation.ts` already use.
- **Clipboard:** `navigator.clipboard.writeText` (absent or refused → the error toast with the link).
- **The pin's drag:** `PointPicker` already places on a tap and moves on a drag.

## 5. The checks the decisions name — settled by reading, or planned

- **S5 / B2 / L2 — settled.** The profile is a `PATCH` of any part (`updateSpaceProfileSchema =
  createSpaceSchema.partial()`, `requests.ts:54–56`; what is absent is kept, contract § PATCH), and the
  web already sends only the fields that changed (`useProfileSection` + `profileChanges`), so «عن
  المساحة» and «الموقع» each send their own changed fields and never clear the other's. The hours are
  one `PUT` of the week with the shifts (`hours.service.ts`), so «ساعات العمل» sends the new week with the
  shifts exactly as read (ids kept: `shiftChanges` updates in place), and «الورديات» the week exactly as
  read with the new shifts; an unchanged half is rewritten identically. One date per group
  (`DATE_COLUMNS`): what the view shows is in §4.1. Proven by T31–T33 (web) and T16–T17 (API).
- **R3/R6 the custom label — EC1** (Docker is not running at planning; read-only, never seeded).
  Whatever it finds, labelled rows are kept and shown, never edited (R2/R6); the result goes in the
  report. Production data cannot be read by the executor: OD7.
- **W5 overnight — settled.** A day is one range with `opensMinute < closesMinute`, 0–1440
  (`requests.ts:71–82`, decision F4, data-model › *Times of day*, and the init migration's CHECK). The
  Sheet's «إلى» lists end at 24:00, and «إلى» not after «من» is refused on its row (the schema's
  `out_of_range` on `closesMinute`).
- **P4 / C2 order — settled.** Photos: `PUT …/photos/order` with every id once, first = cover, 204, 409
  when the ids are not exactly the gallery (contract § photos order; `usePhotoOrder`) → **one request
  per drop**, the whole order. Contacts: saved whole in their order on «حفظ» (`contacts.repository.replace`
  writes `sortOrder` by index) → a drag changes the Sheet's draft only.
- **M4 readers — settled.** `CONTACT_TYPES` (`shared/spaces/contacts.ts`; `requests.ts` enum); web:
  `features/spaces/hooks/contacts/useContactsSection.ts`, `useReadOnlyContacts.ts`, copy
  `shared/copy/{arabic,english}/spaces.ts` (`types`, `examples`, `fieldErrors`) and `directory.ts`
  (`page.contacts.types`), `features/directory/services/contactLinks.ts` (an exhaustive `switch`),
  `features/directory/hooks/page/useSpacePage.ts` (the WhatsApp/phone bar: unchanged); API: Prisma enum,
  `contacts.repository.ts` (`select { type, value }`), `contacts.service.ts` (compare + audit),
  `facts/facts.ts` (via the repository, so the admin's, managed and public reads all carry what it
  selects), seeds `demo.ts` / `demoDirectory.ts` (only existing types: unchanged, still typed by
  `ContactType`); tests `contacts.unit.test.ts`, `requests.unit.test.ts`, `contacts.api.test.ts`,
  `directory/page.api.test.ts`. «وسيلة أخرى» shows its own name wherever a type's name is shown: the
  public page's contacts (label in the type's place, `dir="auto"`, isolated), the profile's tiles, the
  admin's same view.
- **R1 — settled.** The links that edit prices: `OverviewPage` (`prices` → packages`#prices`),
  `fieldSections.ownerFieldLink` (`PRICES` → packages), `SettingsPage` → `PricingCard` (`pricesLink`),
  `ProfilePage` (`pricesLink` place), `PackagesPage` (`SpacePricesEditor`, `hoursLink`), `packages`'
  sheet line (`hoursLink`). Each is re-aimed in PR-C (§8, commit C5).

## 6. The dependency

- **Name:** `@dnd-kit/core`, `@dnd-kit/sortable`, `@dnd-kit/utilities` (the stable line; versions at
  EC2 — at planning, 6.3.x / 10.0.x / 3.2.x, all over two weeks old), `dependencies` of `apps/web`,
  caret ranges as the repository writes them.
- **Why this one:** touch and mouse dragging through one pointer model with activation constraints (a
  phone keeps scrolling); grid sorting (`rectSortingStrategy`, the photos) and lists
  (`verticalListSortingStrategy`, the contacts) in one API; auto-scroll; React 19 peer range
  (`>=16.8`); unopinionated rendering, so the layer keeps its own tokens, focus ring and words (no
  built-in English: every announcement and instruction is a prop, §11 of foundation); RTL-safe because
  the pointer works in screen coordinates and the keyboard mode is the layer's (SD3); headless, so no
  CSS file enters. Weighed: **pragmatic-drag-and-drop** (no keyboard mode — its guidance is buttons,
  which P4 rules out), **react-movable** (lists only, no grid), **SortableJS** (imperative, ~45 KB, its
  own DOM moves fight React), **react-aria's DnD** (much larger), **@dnd-kit/react 0.x** (pre-1.0 API,
  more churn), the **native HTML5 drag** (no touch on many phones — the prototype's limit).
- **Size:** about 18 KB min+gzip for the three (EC2 measures the built chunk and reports it). Its own
  chunk `sortable` in `LIBRARY_CHUNKS`, reached only from the dashboard's profile pages; `check:build`
  refuses it in the site's first download (the rule it already applies to the table, Leaflet and the
  calendar).
- **Maintenance:** the classic packages are in maintenance by their author (no breaking changes since
  2023, millions of weekly downloads); wrapped once in the layer, so a later move (to `@dnd-kit/react`
  or another) changes one component. Lint (b) forbids `@dnd-kit/*` outside the layer.

## 7. The migration (approved in principle; SQL for the owner)

Name: `apps/api/prisma/migrations/<timestamp>_contact_types_and_other/migration.sql`. Prisma schema:
`enum ContactType { … TELEGRAM X LINKEDIN YOUTUBE OTHER }` (appended), `SpaceContact.label String?`.
Generated with `migrate dev --create-only` **once**, read, then the `CHECK` appended by hand (Prisma
compares no CHECK, data-model § constraints). Expected file:

```sql
-- AlterEnum: the contact networks the owner asked for, and «وسيلة أخرى» (M4).
ALTER TYPE "ContactType" ADD VALUE 'TELEGRAM';
ALTER TYPE "ContactType" ADD VALUE 'X';
ALTER TYPE "ContactType" ADD VALUE 'LINKEDIN';
ALTER TYPE "ContactType" ADD VALUE 'YOUTUBE';
ALTER TYPE "ContactType" ADD VALUE 'OTHER';

-- AlterTable: «وسيلة أخرى»'s own name; every existing row keeps NULL.
ALTER TABLE "space_contacts" ADD COLUMN "label" TEXT;

-- An «other» contact has its own name, never blank, and no other type has one
-- (docs/features/spaces.md › Decisions). The type is compared as text: a value added above
-- cannot be used as an enum literal in the same transaction.
ALTER TABLE "space_contacts" ADD CONSTRAINT "space_contacts_label_check"
  CHECK (("type"::text = 'OTHER') = ("label" IS NOT NULL)
         AND ("label" IS NULL OR btrim("label") <> ''));
```

Existing rows: no `UPDATE`, no default; every existing row is of an old type with `label` NULL, so the
CHECK holds as it is added. Unique key `(space_id, type, value)` unchanged (two «other» contacts with one
value are one contact). Rollback is not automatic (Postgres drops no enum value): a revert would be a new
migration dropping the column and the CHECK, the enum values staying unused — said in the PR.

## 8. The PR split and the files

**OD1 recommends three PRs**, merged in order A → B → C (A and B are independent; C needs both).

### PR-A (#140) — `feat(spaces): contacts of any kind`
- `packages/shared/src/spaces/contacts.ts` (+ unit test): the twelve types in the C1/M4 order
  (`WHATSAPP, PHONE, EMAIL, INSTAGRAM, FACEBOOK, TELEGRAM, TIKTOK, X, LINKEDIN, YOUTUBE, WEBSITE,
  OTHER`); networks: TELEGRAM (`t.me`, `telegram.me` → `https://t.me/<h>`), X (`x.com`, `twitter.com`,
  `mobile.twitter.com` → `https://x.com/<h>`), LINKEDIN (`linkedin.com` links only, path kept → `https://
  www.linkedin.com/…`; a bare name refused), YOUTUBE (`youtube.com`, `m.youtube.com` → `https://www.youtube.
  com/@<h>` or the path; `youtu.be` refused: a video is no channel); `handlePath` optional on `Network`;
  OTHER: a number by `normalisePhone` (the platform's rule, D6), else a web link by the website rule,
  else null. `CONTACT_LABEL_MAX_LENGTH = 40`.
- `packages/shared/src/spaces/requests.ts` (+ unit test): `contact` adds `label: optional(textSchema(1, 40))`;
  OTHER without one → `required` on `contacts.<i>.label`; another type with one → `invalid_format`
  there; output `label` trimmed or `null`. `responses.ts`: `Contact.label: string | null`.
- `apps/api/prisma/schema.prisma`, the migration (§7); `modules/spaces/contacts/contacts.repository.ts`
  (select and write `label`), `contacts.service.ts` (compare and audit with it), `contacts.api.test.ts`;
  `modules/directory/page.api.test.ts` (the label on the public page).
- Web: `shared/lib/contacts/contactLink.ts` (moved from `features/directory/services/contactLinks.ts`,
  with its words as a parameter of the shape both catalogues give; the new types and OTHER: `tel:` for a
  number, else its link; OTHER's label as its name) + unit test moved and extended;
  `shared/lib/map/mapsLink.ts` (the Google Maps link from `useSpacePage.ts`) + unit test;
  `shared/lib/index.ts`; `features/directory/hooks/page/useSpacePage.ts`, `components/page/…` (only the
  imports and the label's isolation); `features/spaces/hooks/contacts/useContactsSection.ts` (offers
  `CONTACT_TYPES` without OTHER until PR-C; sends `label: null`) + its test; copy
  `shared/copy/{arabic,english}/{spaces,directory}.ts` (types, examples, refusals for the new types).
- Docs: `api-contract.md` (`Contact`, the contacts body and codes), `data-model.md` (Contacts
  convention: twelve types, the label; the CHECK in *later migrations*), `features/spaces.md` (API
  decisions + history), `features/directory.md` (the shared link, the label), glossary (EC9).

### PR-B (#141) — `feat(design-system): a sortable list`
- `apps/web/package.json`, `package-lock.json` (root): the three packages.
- `apps/web/src/shared/design-system/components/fields/Sortable/{Sortable.tsx,index.ts,
  Sortable.component.test.tsx}` and `sortable.ts` (the fourth entry); `lib/sortableKeys.ts` (the pure
  keyboard step: index, key, layout, direction → next index) + unit test.
- `apps/web/scripts/libraryChunks.ts` + `libraryChunks.unit.test.ts` (the `sortable` chunk),
  `layerEntries.unit.test.ts` (and whatever list of the layer's entries it reads: the fourth entry);
  `vite.config.ts` needs no change (it maps `LIBRARY_CHUNKS`, line 45); root `eslint.config.js`
  (restriction (b) for `@dnd-kit/*`, the `sortable` entry allowed); the showcase
  `pages/showcase/sections/fields/…` + `registry.tsx` + `fixtures.json`.
- Docs: `foundation.md` §3 (the entry, the category row), §12 (`fields` row: Sortable).
- **Component API (for PR-C):** `Sortable<Id>({ items: Id[], layout: 'grid' | 'list', onMove(next: Id[],
  moved: Id), disabled?, label, words: { lifted, moved, dropped, cancelled, instructions, held? },
  renderItem(id, { itemProps, handleProps, lifted, dragging }) })` — `handleProps` when a row drags by a
  handle (contacts), `itemProps` on the whole tile otherwise (photos); words are functions of
  `{ name, position, count }` given by the feature, `nameOf(id)` too.

### PR-C (#142) — `feat(spaces): the space profile, view first`
Web, `apps/web/src/`:
- **`features/spaces/`** — rewritten under the existing folders:
  - `components/editor/`: `SpaceEditor.tsx` (rewritten: the header, the index, the eight sections, the
    Sheets), `ProfileHeader.tsx`, `SectionIndex.tsx` (replaces `SectionNav.tsx`), `SectionCard.tsx`
    (rewritten: title h2, meta, «تعديل», stale line, empty state, notice slot), `EditSheet.tsx` +
    `DiscardDialog.tsx`, `SpaceStatusBadges.tsx`, `VerifiedNotice.tsx` (kept), `PrivacyNote.tsx` (kept),
    `LeaveDialog.tsx` (words), `EditorLoading/Failure` (kept); **removed:** `MissingChecklist`,
    `OwnerHead`, `PricesLinkCard`, `ReadOnlyCard`, `ReadOnlyRows`, `SectionNav`.
  - `components/{photos,prices,hours,shifts,amenities,about,location,contacts}/`: a `…View.tsx` and a
    `…Sheet.tsx` each (photos: `PhotosView`, `PhotosEdit`, `PhotoTile`, `PhotoUploadTile`,
    `PhotoRemoveDialog`); **removed:** every `ReadOnly*.tsx`, `ProfileSection`, `HoursSection`,
    `PricesSection`, `AmenitiesSection`, `ContactsSection`, `PhotosSection`, `PhotosCard`,
    `SpacePricesEditor` (→ `prices/SpacePricesCard.tsx`, read-only).
  - `hooks/editor/`: `useSpaceEditor.ts` (rewritten), `useProfileHeader.ts`, `useSectionFrame.ts`
    (rewritten for view-first), `useEditSheet.ts` (draft, dirty, ask, focus return, `?sheet=`),
    `useSaveGroup.ts` (toast by section name), `useLeaveGuard.ts`, `useSectionInView.ts`,
    `useHashLanding.ts`, `sectionName.ts` (+ test), `editorScope.ts`; **removed:** `usePricesLink.ts`.
  - `hooks/{about,location,hours,shifts,prices,amenities,contacts,photos}/use…Sheet.ts` (+ component
    tests); `hooks/location/useCurrentPosition.ts`; `hooks/photos/usePhotoOrder.ts` (pending order,
    SD2), `usePhotoUploads.ts`, `usePhotoRemove.ts` (kept, words); `hooks/prices/useSpacePricesCard.ts`;
    **removed:** `useReadOnly*.ts`, `usePricesSection`, `useHoursSection`, `useProfileSection`,
    `useSpacePricesEditor`.
  - `services/`: `completeness.ts` (+ unit), `hoursSheet.ts` (+ unit; replaces `hoursForm.ts`),
    `timeOptions.ts` (+ unit), `pricesForm.ts` (+ R7's `nextPrice`, unit), `pricesView.ts` (sort, columns;
    unit), `shiftsForm.ts` (+ unit), `amenitiesForm.ts` (+ the catalogue-name check; unit),
    `aboutChanges.ts` / `locationChanges.ts` (from `profileChanges.ts`; unit), `contactsForm.ts` (unit);
    **removed:** `clockTime.ts` (+ test) once unused.
  - `types/`: `EditorPlace.ts` (admin: `areaName`/`amenityNames` leave it — both places now pass the
    area line and the catalogue as editor props; owner: + `closureLink`, `packageShifts`, − `pricesLink`;
    the top bar's actions are the page's, not the place's), `SectionId.ts`, `SectionFrameView.ts`, `AmenitiesField.ts` (+ icons),
    `AreaField.ts`, new `AmenityCatalogue.ts`, `AreaLine.ts`; `index.ts` (exports: `SpaceEditor`,
    `SpacePricesCard`, `SectionId`, drop `SpacePricesEditor`).
- **`features/lookups/`:** `components/area/AreaCombobox.tsx` (+ test; over `useAreaOptions`, grouped,
  searchable, a hidden own area kept first as `AreaSelect` does), `components/area/AreaLine.tsx` (area،
  governorate; + test), `hooks/amenities/useAmenityCatalogue.ts` (the catalogue by source: id, names,
  icon key; + test), `components/amenities/AmenityChecklist.tsx` (icons, two columns, «أُزيل من
  القائمة»; test updated), `index.ts`.
- **`features/data-reports/`:** `services/noticeGroup.ts` → sections (`LOCATION → location`,
  `OTHER → about`), `types/ReportNoticeView.ts` (`section`), `useReportNotice.ts`, its test.
- **`features/packages/`:** `hooks/shifts/usePackageShiftIds.ts` (every package's shift, retired ones
  included, from the list query; + test), `index.ts`.
- **`features/space-settings/`:** `PricingCard.tsx` (only the link's words if they say Packages).
- **`shared/design-system/icons/iconSet.tsx`** (+ `index.ts`): the contact glyphs (MessageCircle, Phone,
  Mail, Camera, ThumbsUp, Send, Music, AtSign, Briefcase, Play, Globe, Link) and GripVertical,
  LocateFixed, Copy — Lucide has no brand marks (checked: none in the installed version).
- **`pages/dashboard/`:** `space/ProfilePage.tsx` (place: closure link, package shifts, catalogue, area
  line, combobox), `admin/SpaceEditPage.tsx` (the same, the top bar's hide/delete — reusing
  `useSetSpaceHidden`/`useDeleteSpace` through a new `SpaceEditorActions` export of `spaces`),
  `space/PackagesPage.tsx` (`SpacePricesCard`, no notice, shifts link → `profile?sheet=shifts#shifts`),
  `space/overview/OverviewPage.tsx` (prices → `profile#prices`, profile → `#about`),
  `fieldSections.ts` (PRICES → profile), `space/SettingsPage.tsx` (pricing → `profile?sheet=prices#prices`),
  their component tests.
- **Copy:** `shared/copy/{arabic,english}/spaces.ts` (+ `packages.ts`, `dataReports.ts` where lines move).
- **Docs:** `features/spaces.md` (web behaviour rewritten, decisions superseded with dates, code map,
  history), `packages.md`, `data-reports.md`, `overview.md`, `space-settings.md`, `lookups.md`;
  `foundation.md` §12 icons line if it lists glyphs; findings 216 (+ index).

**Files shared with other open items (workflow §9):** the palette lab (`app-b`) changes prototype files
and maybe later the tokens — PR-B/PR-C touch no token file; if the lab lands token renames first, PR-C
follows them. The women + evening task (schema, directory, profile): **PR-A is this item's one schema
change** — that task's migration waits for PR-A's merge; it shares `features/directory/*` (PR-A only)
and the whole profile (PR-C) — it should start after PR-C merges, or its plan names these files. Recorded
in the report's conflict check.

## 9. Stronger decisions (SD) — each with why, cost, recommendation

- **SD1 — The contact and map links move to `shared/lib`** (PR-A). *Why:* the profile's tiles must link
  as the public page does (C1, M3: "so the owner tests each as a visitor would"); the second instance
  (engineering principles §1). *Cost:* two moved helpers, the directory's imports. **Recommend.**
- **SD2 — A dropped photo stays where it was dropped while its order is sent** (revises #85's "nothing
  moves before the server has accepted"). *Why:* with dragging, a tile snapping back then jumping is a
  false signal; the dropped order is the user's act, kept as the section's own state (like the upload
  queue), not a prediction written into the cache; on a refusal it returns to the server's order with
  the reason, and a 409 fetches the gallery again (as today). *Cost:* one local state in
  `usePhotoOrder`. **Recommend.**
- **SD3 — The keyboard mode is the layer's own, by index, not dnd-kit's `KeyboardSensor`.** *Why:*
  dnd-kit's keyboard moves by measured geometry, which jsdom cannot measure (the component lane could
  not prove P4's keyboard path without stubbing layout), and its spoken positions are its own; an
  index step is deterministic, follows the reading direction in a grid and only up/down in a list (the
  prototype's rule), and its words are the catalogue's. The pointer and touch stay dnd-kit's. *Cost:*
  one pure step function and a small state machine in the component. **Recommend.**
- **SD4 — «وسيلة أخرى»'s number follows the platform's phone rule (Palestinian / Israeli, E.164)**,
  else it must be a web link. *Why:* one number, one form in the database (D6); a foreign messenger is
  reached by its link. *Cost:* an owner with a foreign number writes it as a link (`wa.me/…`).
  **Recommend.**
- **SD5 — A shift a package uses is known only to the owner's page.** *Why:* packages are private to the
  space's staff (D7); the admin cannot read them, so the admin's Sheet relies on the server's 409, said
  in the Sheet. *Cost:* one packages hook passed by the owner's page; a recorded, accepted limit
  (finding 216). **Recommend.**
- **SD6 — The area field of «الموقع» is a new lookups `AreaCombobox`, `AreaSelect` kept for the add
  page.** *Why:* L2 asks a searchable list; the add page is out of scope and keeps its field (#57).
  *Cost:* one component over the same options hook. **Recommend.**
- **SD7 — Confirm only on a stale group** (G3), never on a fresh one. *Why:* the design; the API and
  the overview are unchanged. *Cost:* an owner can no longer renew a fresh date by hand. **Recommend**
  (it is the decision; stated because it revises #74's A1).

Documents' rules this item would weaken: none, once spaces.md records the superseded web decisions
(#74 A1/S7/S8, #79 typed times and «نسخ إلى كل الأيام», #85 the arrows and "nothing moves before",
#96/#98 the owner's head, the prices row and Packages' editor, O6).

## 10. Related findings

- 23, 65, 152, 215 (open): none touches the profile; **not folded**. (152, the audit's growth: the
  contacts' audit adds a short label, negligible.)
- **New 216 — "The admin's shifts Sheet cannot mark a shift a package uses"** (Accepted: D7 keeps
  packages from the admin; the server's 409 is the guard), written in PR-C. Next free after it: 217.

## 11. Design issues (DI) — each built only once the reply approves it

- **DI-1 — Shifts before hours.** A shift must lie inside an open day, and the shifts' save resends the
  week; with no hours saved there is no week to resend. The shifts' empty state, while the hours are
  missing, says «أضف ساعات العمل أولًا، ثم الورديات.» and its action opens the hours' Sheet.
- **DI-2 — A new week that drops a saved shift.** The hours' Sheet cannot show the shifts, yet the
  server refuses a week that leaves a saved shift outside every open day. Before sending, the Sheet says
  «الوردية «{name}» خارج الساعات الجديدة. عدّل الورديات أولًا أو اختر ساعات تشملها.» with a link to the
  shifts' Sheet (asking first, as S4's link does).
- **DI-3 — «ربط مالك» without the alert.** X3 drops the unverified alert, which held the owners' slot's
  link (#91). It moves to the admin's header, beside «غير موثّقة», as an outline button (the slot's own),
  told whether a Sheet has unsaved changes as today.
- **DI-4 — The completeness bar waits for the gallery** (a skeleton line), so it never counts down a
  photo it has not read.
- **DI-5 — The closure link** leads to the announcements page (it has no deep link to a new closure;
  adding one would touch `announcements`): the words «إغلاق مؤقت؟ أضف إعلان إغلاق من الإعلانات».
- **DI-6 — The description's limit is said, never cut:** the counter turns `destructive` past 1000 and
  the save is refused `too_long` on the field, instead of the prototype's `maxLength`, which drops pasted
  text silently.
- **DI-7 — The photo picker keeps `accept="image/*"`** (#85: a HEIC reaches its tile and is refused in the
  owner's words), not the prototype's three types.
- **DI-8 — An empty-saved group shows its empty state but keeps its date line** («آخر تحديث …») so an
  owner who saved "no prices" sees it was a choice; the bar still counts it missing. (The prototype hides
  the date; this is the safer reading of D2 — OD5.)

## 12. Tests — the matrix (lanes per testing.md; every new test seen failing first)

Rule for every row: expectations written by hand; the break named; for security/transaction/ordering
properties the break is made once and restored **from a `cp` backup, never `git checkout`**.

### Shared (unit, `packages/shared`)
- **T1** TELEGRAM: `@masaha_ps`, `masaha_ps`, `t.me/masaha_ps`, `https://telegram.me/masaha_ps?x=1` →
  `https://t.me/masaha_ps`; `example.com/masaha` → null. *Break:* a wrong base or host list.
- **T2** X: a handle and a `twitter.com` link → `https://x.com/<h>`, query dropped. *Break:* twitter kept.
- **T3** LINKEDIN: `linkedin.com/company/masaha` → `https://www.linkedin.com/company/masaha`; `masaha`
  (a bare name) → null. *Break:* a handle accepted.
- **T4** YOUTUBE: `@masaha` → `https://www.youtube.com/@masaha`; `youtube.com/channel/UC…` kept;
  `youtu.be/abc` → null. *Break:* youtu.be accepted.
- **T5** OTHER: `discord.gg/focushub` → `https://discord.gg/focushub`; `0599123456` and `٠٥٩٩١٢٣٤٥٦` →
  `+970599123456`; `+44 20 7946 0000` → null; `two words` → null. *Break:* any text accepted.
- **T6** The existing types' rules unchanged (the existing tests pass untouched).
- **T7** `updateSpaceContactsSchema`: OTHER without label → `required` at `contacts.0.label`; blank label
  → `too_short`; 41 characters → `too_long`; a bidi control → `invalid_format`; WHATSAPP with a label →
  `invalid_format` at `contacts.0.label`; OTHER's label trimmed in the output, another type's `null`;
  `TWITTER` → `invalid_choice`; two OTHERs with one value → `not_unique` on the second's value.
  *Break:* the label rule left out.

### API (`test:api`, real database)
- **T9** `PUT /admin/spaces/:id/contacts` with TELEGRAM, X, LINKEDIN, YOUTUBE and an OTHER with
  «ديسكورد»: 200, stored forms and labels, `GET` in the same order; audit `space.contactsEdited` `after`
  holds the label. *Break:* the label not selected.
- **T10** OTHER without a label → 422 `errors["contacts.0.label"] = ["required"]`, WHATSAPP with one →
  `["invalid_format"]`; nothing written, the date unchanged.
- **T11** Changing only an OTHER's label is a change (written, dated, audited). *Break:* the compare
  ignores the label.
- **T12** The CHECK: a raw insert of OTHER with NULL label, WHATSAPP with a label, OTHER with `'  '`
  are each refused by the database. *Make the break:* the constraint dropped in the test DB once.
- **T13** The public page (`directory/page.api.test.ts`) carries OTHER's label and `null` for the others.
- **T14** The managed route (`manage.api.test.ts`): an owner saves an OTHER; reception is refused 403 (the
  existing per-role rows extended by one body, no new endpoint).
- **T16** Hours: a `PUT` with the week exactly as saved and the shifts changed keeps every day row,
  updates the shifts (ids kept), dates the group, audits `before.days == after.days`. *(EC8: exists?)*
- **T17** Profile: a `PATCH` of the about fields alone leaves the location fields; of the location
  alone leaves the names and descriptions. *(EC8)*
- **T18** Confirm `hours` and `profile` date their group only. *(EC8)*
- **T19** A shift used by a price, and one used by a package, refused on removal (409), the week taken
  back. *(EC8: the package case added if missing)*
- **T20** Photos: an order makes its first the cover in the directory's covers read; a stale order 409.
  *(EC8)*
- **T15** Existing rows untouched: EC5 on `masaha_dev` (counts by type before/after, `label` all NULL).

### Design system (PR-B)
- **T28** `sortableKeys` (unit): grid RTL ArrowLeft → +1, ArrowRight → −1; LTR the reverse; list
  ArrowLeft/Right → no move; ArrowUp/Down ±1 in both (grid: by one); Home/End; clamped at the ends.
  *Break:* the direction ignored.
- **T28b** `Sortable` (component): Space lifts and announces the feature's words with position «2 من
  3»; ArrowDown moves and announces; Space drops and calls `onMove` once with the new order; Escape
  restores and calls nothing; Tab while lifted drops; `disabled` holds a lift and says `held`; no
  English built-in string in the DOM (every live text from props); axe clean lifted and at rest.

### Web (PR-A and PR-C)
- **T27** `contactLink` (unit, moved + new): wa.me digits, `tel:` with carrier label, `mailto:`, a
  network's https link external, OTHER number `tel:`, OTHER link external with its label as name.
- **T21** `completeness` (unit): seven parts; about `missing` with both names and an English description
  but no Arabic description (**X2**), `ok` with it; a stale group → `stale` on both of its sections;
  prices saved empty → `missing`; shifts never counted; «N» = the ok-or-stale count. *Break:* X2 read as
  the name.
- **T22** `hoursSheet` (unit): saved Sat–Thu equal + Friday any → simple; differing → custom; `null` →
  the template (not dirty); simple → `days` by the contract's Sunday-first index (Friday = 5, Saturday =
  6); custom → seven; to simple takes the first open of Sat–Thu, Friday kept. *Break:* an index off by one.
- **T23** `timeOptions` (unit): 48 starts, ends 00:30…24:00, a saved 08:15 kept in its list, in order.
- **T24** `nextPrice` (unit, R7): first unpriced period for everyone without shift or label, then the
  students', then a day for everyone.
- **T25** `pricesForm` (unit): a labelled saved row keeps both labels in the request; agorot.
- **T26** `shiftsOutside(week, shifts)` (unit, DI-2).
- **T30** View first (component, owner and admin): each section shows its facts with no input; each
  «تعديل» named «تعديل {section}»; each empty state's words and action (the eight).
- **T31** Hours Sheet: simple save → `PUT …/hours` with the new week and the saved shifts unchanged; the
  Sheet closes, toast names «ساعات العمل», focus on its «تعديل».
- **T32** Shifts Sheet: save → the saved week unchanged, the shifts with ids and English names (X1).
- **T33** About Sheet → `PATCH` of its changed fields only; Location Sheet → its own only (B2/L2).
- **T34** Discard: «رجوع» / close / Escape with changes ask «تجاهل التغييرات؟»; its «رجوع» returns to
  «حفظ»; «تجاهل التغييرات» closes and sends nothing; unchanged closes at once; the template week and the
  first empty price row are not changes; unchanged «حفظ» on a saved group sends nothing, toasts «لم
  يتغيّر شيء».
- **T35** Header: «N من 7 أقسام» on the `Meter`, the line's links to missing/stale sections, X2's case,
  «الملف مكتمل ومحدّث»; «نسخ الرابط» puts the absolute URL on the clipboard (user-event's stub) and
  toasts; the letter tile and «أضف صورة غلاف» opening the edit state.
- **T36** Index: drawn from 1024 px (`test/screenWidth.ts`), none below; dots' states said; current
  section `aria-current`.
- **T37** Stale: «قد تكون قديمة» and «ما زالت صحيحة» on both sections of the pair; confirm posts the
  group's path once; both lines go.
- **T38** Photos keyboard drag: «إدارة الصور», focus photo 2, Space → announced lift, ArrowLeft (RTL) →
  position 3 announced, Space → one `PUT …/photos/order` with the new ids; the order shown while pending;
  a second lift held until the gallery is read again; Escape sends nothing.
- **T39** Photo delete asks «حذف هذه الصورة؟» («حذف» / «رجوع»); «رجوع» sends nothing; «حذف» sends
  `DELETE`; the cover's line.
- **T40** At 10 photos the limit line replaces «اختر صورًا» (no disabled button).
- **T41** Contacts Sheet: OTHER shows «اسم الوسيلة», refused «اكتب اسم الوسيلة» on its row; per-type
  refusal words; duplicate «هذه الوسيلة مضافة من قبل»; a new row is WhatsApp; a keyboard move of a
  handle changes the order sent on «حفظ»; tiles' hrefs per type and OTHER's name.
- **T42** Prices Sheet: one row on an empty section; «إضافة سعر» prefilled; a repeat on the second row;
  «أدخل المبلغ»; «الوردية» only with shifts; «أضف وردية» asks when dirty then opens the shifts' Sheet; a
  labelled row read-only and kept in the request.
- **T43** Shifts: in use by a saved price and by a package (owner page) → remove disabled with S3's line;
  the admin's 409 said in the Sheet and the space fetched again; no hours → DI-1.
- **T44** Hours Sheet: differing saved days open in custom mode; back to simple asks «سيتم توحيد…»; «إلى»
  before «من» said on its row; a day switched on takes the last edited open day's hours; DI-2's line.
- **T45** Admin: «غير موثّقة» / «مخفية عن الزوار» badges, no unverified alert (X3), «ربط مالك» in the
  header (DI-3); verified → same view, no «تعديل» / «ما زالت صحيحة» / «إدارة الصور», «يعدّلها …»; the top
  bar's hide (toast «تراجع») and delete (asks «حذف» / «رجوع», then the deleted list with Undo).
- **T46** Packages & prices: the prices read-only (no input), date and stale badge, «تعديل الأسعار في ملف
  المساحة» → `…/profile?sheet=prices#prices`; on the profile `?sheet=prices` opens that Sheet once and
  leaves the address without it.
- **T47** Links: overview prices → `profile#prices`, profile → `#about`; a PRICES report's «تعديل الحقل»
  → profile; settings' pricing link → profile; a LOCATION report's notice inside «الموقع», OTHER inside
  «عن المساحة» (data-reports' test too).
- **T48** Both languages: English renders a Sheet's labels and each text field's `lang`/`dir`; axe clean
  in view, with each Sheet open, and in the photos' edit state (vitest-axe), Arabic and English.
- **T49** «استخدم موقعي الحالي» (`test/fakeGeolocation.ts`): inside → coordinates and toast; outside →
  «الموقع خارج قطاع غزة»; refused → its line; no geolocation → no button.
- **T50** Leave guard: Back with a dirty Sheet asks, naming the section; an upload in flight asks (#85).
- **T51** Amenities Sheet: a held retired amenity marked; an own row naming a catalogue amenity refused
  in the browser; the view lists the offered ones only, own after the catalogue's.
- **T52** Lookups: `AreaCombobox` (search, groups, a hidden own area first), `AreaLine`,
  `useAmenityCatalogue`; packages `usePackageShiftIds` (retired included).
- **T53** Catalogue parity (existing test, new keys).
- **Time seam:** `vi.setSystemTime` as the web's tests do (today's «اليوم», Gaza days); the width seam
  `test/screenWidth.ts`; the geolocation seam `test/fakeGeolocation.ts`; the clipboard user-event's;
  the network `fakeAdapter`. No parameter, option or module exists only for a test.

## 13. Review Focus (inputs no planned test exercises)

- A real touch drag on a phone (activation delay vs scroll; the strip and the grid), EC4.
- A screen reader's actual speech (NVDA/VoiceOver) of the lift/move/drop words.
- Leaflet's drag of the pin inside a Sheet at 390 px; the Sheet's scroll with a 300-px map.
- Two sessions saving the hours and the shifts of one space at once (whole-group `PUT`s: the later wins,
  as since #48).
- A YouTube `/c/` or `/user/` link (kept by the path rule), LinkedIn `/school/`.
- A space with forty prices, ten shifts, twenty contacts in the Sheets at 390 px.

## 14. Commits (Conventional, atomic; lint + typecheck on each; lanes once on each PR's head)

- **PR-A:** A1 `refactor(lib): share the contact and map links` · A2 `feat(spaces): contacts of any kind`
  (shared + migration + API + the web's minimum + docs + tests).
- **PR-B:** B1 `feat(design-system): add a sortable list` (dependency, component, keyboard step, entry,
  chunk, lint, showcase, foundation).
- **PR-C:** C1 `feat(lookups): an area combobox and the amenity catalogue` · C2 `feat(spaces): the
  space profile, view first` (frame, header, index, Sheets, the eight sections without reordering, the
  admin's same page, copy, spaces.md) · C3 `feat(spaces): order photos and contacts by dragging` · C4
  `feat(spaces): the admin's hide and delete in the top bar` · C5 `feat(spaces): prices edited in the
  profile only` (Packages read-only, every link re-aimed, notices by section, packages/data-reports/
  overview/space-settings docs, finding 216).

## 15. Executor checks (EC)

- **EC1** `npm run db:up`, then read-only: `SELECT count(*) FROM space_prices WHERE label_ar IS NOT NULL
  OR label_en IS NOT NULL;` on `masaha_dev` (names per the schema's `@map`). Report the count. Never
  `db:seed`.
- **EC2** `npm view @dnd-kit/core version time peerDependencies` (and sortable, utilities): the latest
  stable, ≥ 2 weeks old, React 19 in range; install; after `build`, the `sortable` chunk's gzip size
  reported (`vite.config.ts` already builds every `LIBRARY_CHUNKS` group).
- **EC3** dnd-kit's `DndContext` `accessibility` props: our announcements and instructions replace its
  English ones; no `aria-roledescription="sortable"` left in English (set from props).
- **EC4** Touch: Chrome DevTools touch emulation at 390 px — a press-and-hold drags, a swipe scrolls; a
  delete tap is a click.
- **EC5** The migration: `migrate dev --create-only` **once**, `ls` the folder, compare with §7, append
  the CHECK, `migrate dev` to apply to `masaha_dev`; before and after: `SELECT type, count(*),
  count(label) FROM space_contacts GROUP BY type;` — equal counts, zero labels. The test DB through the
  lane's own reset. A refusal for "unsafe use of new value" means the CHECK lost its `::text`.
- **EC6** The blank label's code is `too_short` (textSchema's `min(1)` after trim): T7 asserts the code
  the schema yields, and the contract says it.
- **EC7** Lucide names in the installed version (seen at planning: message-circle, phone, mail, camera,
  thumbs-up, send, music, at-sign, briefcase, play, globe, link, grip-vertical, locate-fixed).
- **EC8** For T16–T20, find the existing test by name; add only the missing ones, each proven by
  reverting its code once.
- **EC9** The glossary's words for the new types, «الأسعار المعلنة», «سعر»; add what is missing.
- **EC10** `migrate deploy` online is the deploy's (setup.md runbook): PR-A's description says the merge
  applies one migration to production.

## 16. Verification (phase 4, each PR, before any push)

`npm run lint`, `typecheck`, `format:check`, `check:classes`, `check:links`, `check:conflicts`; `NODE_ENV=
production npm run build` then `check:build`; `test:unit`, `test:component`, `test:api` **in full**, two
at a time at most with 8–10 GB free, a third waiting; **a lane killed for memory: retried once; killed
again, CI judges** — said in the PR and the report. A real run: PR-A, real requests (`curl` on the
managed and public routes with an OTHER contact) and the public page in the browser; PR-B, the
showcase at 360/768/1280, RTL/LTR, light/dark, keyboard; PR-C, the owner's and the admin's pages
in the browser at 390/768/1440, RTL/LTR, light/dark, every Sheet, a mouse drag, a keyboard drag, touch
emulation, «نسخ الرابط», «استخدم موقعي الحالي» (DevTools sensors, inside and outside the Strip).
Servers stopped by PID, ports checked free. Screenshots to `Downloads\wi<n>-shots`, curated, never
pushed. Report only once `gh pr checks` is green on the pushed head and GitHub shows `CLEAN`.

## 17. Limits (written for the executor)

- No migration beyond §7; **never `db:seed` `masaha_dev`**; `migrate dev --create-only` once (a second
  run applies it); `migrate reset` needs the owner.
- Stage by path; never `git add -A` / `.`; no tool attribution; `#PRNUM` replaced just before each push
  (next numbers checked then: expected #140, #141, #142); no push to `main`, no merge, no force-push of
  another branch, no secret printed. Executors never stop on file count; they report it. Review fixes
  fold into their commits (`backup/*` first). Branches from the latest `main`: `feat/contact-types`,
  `feat/sortable-list`, `feat/space-profile`.
- **What changes on each merge day (every merge deploys):** **#140** — visitors: nothing until a space
  adds a new contact; then its Telegram/X/LinkedIn/YouTube shows as a link on its page. Owners and the
  admin: the current editor's type list offers the four networks. One migration runs online. **#141** —
  nothing visible (the showcase is development-only; no production page uses the list yet). **#142** —
  owners and the admin see the new profile (view first, Sheets, drag, completeness, «نسخ الرابط»);
  Packages & prices shows the prices read-only; the overview's, settings' and reports' links land on the
  profile; «وسيلة أخرى» becomes available. Visitors: nothing changes on the public pages.

## 18. Risks

- **R-1** PR-C is large (~100 files): one review conversation; commits C2–C5 keep it readable.
- **R-2** jsdom and dnd-kit's pointer path: the component lane proves the keyboard path only; the pointer
  and touch are the browser run's (EC4) — stated in the PR.
- **R-3** The enum migration is not reversible by `migrate` (§7).
- **R-4** Old bookmarks to `#profile` / `#basics` land on no section (the page still opens); the link
  builders are all re-aimed.
- **R-5** The women + evening task: schema (waits for PR-A), directory (PR-A) and profile (PR-C) overlap.

## 19. Proposed alternatives (challenges — none built without the owner)

- **PA-1 — Keep a manual «ما زالت صحيحة» on fresh sections too** (the old editor had it): owners who just
  checked would renew the date without waiting to go stale. The design shows it on stale only; I do not
  recommend changing it.
- **PA-2 — A shifts endpoint of its own (`PUT …/shifts`)** so a shifts save never resends the week. Not
  needed (§5), and it would split F3's one group; not recommended.

## 20. Open points for the owner (OD)

- **OD1 — The PR split.** (a) **three PRs: contacts (API+shared+migration) → sortable (dependency) →
  profile (web)** — *recommended*: the schema and the dependency each reviewed alone and early; (b) two
  PRs (contacts; profile with the dependency); (c) one PR.
- **OD2 — H4's hide/delete in the editor's top bar** (production has them only in the list's row menu):
  (a) **build them in C4** — *recommended*, H4 is binding; (b) leave them to the list and record it.
- **OD3 — `?sheet=` opens a Sheet from a link** (R1's «تعديل الأسعار في ملف المساحة», settings, the
  packages' shift line): (a) **open the Sheet** — *recommended*, the prototype's; (b) land on the section.
- **OD4 — The closure link (DI-5):** (a) **the announcements page** — *recommended*; (b) a deep link that
  opens a new closure there (touches `announcements`).
- **OD5 — An empty-saved group's date (DI-8):** (a) **shown** — *recommended*; (b) hidden, as the prototype.
- **OD6 — Approve DI-1…DI-8 and SD1–SD7** as written (or name the ones to drop).
- **OD7 — Production's labelled prices:** the executor cannot read production; (a) **nothing to do** —
  *recommended*: labelled rows are kept and shown either way; (b) the owner runs EC1's query on Neon.
