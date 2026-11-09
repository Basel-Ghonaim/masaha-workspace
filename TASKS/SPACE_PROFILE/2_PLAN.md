# SPACE_PROFILE — plan (prototype only, 2026-11-08)

Branch `design/space-profile` from `origin/main` 40cb481d, worktree `C:\dev\masaha\app-design`. Only `docs/design/`.

## Where things live today → where they go
- `masaha/profile-a.jsx`: the old frame (`useSection`, `ProfileSection` with a Save per card, `MissingChecklist`,
  `SectionNav` chips), «المساحة» (basics + location in one form), the hours with the shifts inside. **Kept** for
  `Admin space add.html`: `BasicsFields`, `LocationFields`, `AreaSelect`, coords helpers, `errorsOf`, `basicsErrors`,
  `locationErrors`, `SectionTitle`, `Optional`, `ago`, `latinDigits`, `SAMPLE_SHIFTS`, `publish`/`useStored`. The rest
  is replaced by the new frame: the page store (one object, five API groups with their dates), the section head (G3),
  the Sheet with «تجاهل التغييرات؟» (one component for all seven Sheets), the header (H1–H4, M2), the side index with
  its dots, the reorder hook (native drag + keyboard + live region), and الصور (P1–P7, M1).
- `masaha/profile-b.jsx`: prices/amenities/contacts/photos as always-open forms. **Replaced** by: الأسعار المعلنة
  (R6–R9, a view also used read-only by Packages), ساعات العمل (W1–W5), الورديات (S1–S5), المرافق (A1–A2).
- **New `masaha/profile-c.jsx`**: عن المساحة (B1–B2), الموقع (L1–L2), التواصل (C1–C2, M3, M4 — the new types and
  «وسيلة أخرى»), and `SpaceProfile`, the page body both pages render (owner / admin / admin read-only).
- `masaha/space-parts.jsx` is Space details' only; the profile pages never load it, so it stays untouched.
- Pages: `Owner space profile.html` and `Admin space edit.html` shrink to their shells + `SpaceProfile`;
  `Packages.html` shows the prices read-only with «تعديل الأسعار في ملف المساحة» (R1). Links that land on
  `Packages.html#prices` to edit (Data reports, Owner audit, Owner overview) move to `Owner space profile.html#prices`;
  `#profile` becomes `#about`.

## Order of work
1. Frame + header + index + photos (a) → 2. prices, hours, shifts, amenities (b) → 3. about, location, contacts, page
   (c) → 4. owner page → 5. admin page (badges «غير موثّقة» / «مخفية عن الزوار», hide/delete in the top bar, the verified
   space = the same view with no «تعديل») → 6. Packages → 7. links, INDEX, CHANGES, Flows frames → 8. checks + a global
   name check over each page's scripts → 9. browser pass (390/768/1024/1440 × ar/en × light/dark), screenshots.

## Sample data (URL `?demo=` comma list; `?sheet=<section>` opens a Sheet, `?photos=edit` the photos' edit state)
- Default Focus Hub: 6 photos, 4 prices with a students' month, Sat–Thu 08:00–18:00, Friday closed, no shifts, a
  «وسيلة أخرى» contact (ديسكورد), no English description (its effect line); prices (34 days) and contacts (75) stale.
- `shifts` two shifts with shift prices (the morning one used by a package → cannot be removed); `nohours` no hours;
  `photos10` ten photos (the limit line); `nophotos` no photos (letter tile, empty state); `missing` amenities never
  saved (an empty section); `empty` every group empty but the name; `clear` all fresh → «الملف مكتمل ومحدّث»;
  `custom` hours that differ by day (the Sheet opens customised); `outside` «موقعي الحالي» outside the Strip.
- Admin: `?id=golden` (unverified, stale), `?id=palm` (hidden, prices missing), `?id=new`, `?id=focus` (verified, read-only).

## What cannot be built as written, and what I do instead
- **Touch dragging** (P4/C2): native HTML5 drag works with a mouse only; keyboard mode is built (Space lift, arrows,
  Space drop, Escape cancel, announced). Touch is the production library's (the approved dependency) — in the report.
- **Copy link**: `navigator.clipboard` with the page URL, a toast; the prototype has no real public URL.
- **«استخدم موقعي الحالي»**: no geolocation prompt; the sample's position (`demoUser`), `outside` puts it in Rafah's
  sea. The map's drawing covers Gaza City only, so «الموقع خارج قطاع غزة» is reached by the coordinates field, kept
  under the map as the keyboard's way to place the pin (the map has no keyboard pin).
- **Partial saves over one API group** (S5, G-open): the prototype saves «عن المساحة»/«الموقع» and «ساعات العمل»/
  «الورديات» into one group each — one date, one staleness, «ما زالت صحيحة» confirms the pair. The executor checks the API.
- **Amenity icons**: the bundle has none; small inline SVG placeholders (currentColor), like the nav icons (F-6).
- **Overnight hours**: lists 00:00–24:00 every 30 minutes, «إلى» after «من»; overnight follows the model (later check).
- **Custom price description**: dropped from the Sheet (R6). Data that uses it: only the public sample's «أسبوع
  الامتحانات» (details-data); the real data is the executor's check. Labelled rows are kept and shown, not edited.

## Proposed alternatives (built as decided unless the owner says otherwise)
- **Shift names**: S3 gives one name; the model has an optional English name (the English UI then shows the Arabic).
  Alternative: an optional English field on the row, as «مرافق أخرى» has. Built: one name (S3).
- **Completeness = 7 sections** counts «عن المساحة» complete with only the English name. Alternative: count it
  complete with an Arabic description too (the public page's main text). Built: as decided (name only).
- **Admin's «أنت تعدّل مساحة غير موثّقة» alert**: kept, without «كل قسم يُحفظ وحده» (G4); the header badge alone may
  be enough — the owner may drop the alert.
