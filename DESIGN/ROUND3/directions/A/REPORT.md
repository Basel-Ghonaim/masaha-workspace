# Direction A — «اللوحة» · The live board: the builder's report

> Saved by the lead from the builder's final message (the harness refused the builder's own write of this file).

## Built
The eight pages (`home`, `spaces`, `space`, `login`, `about`, `account`, `favorites`, `404`) in `directions\A\`,
static, from `file://`, no library: `css\a.css` (tokens for both themes, components), `js\core.js` (the words in both
languages verbatim from the catalogue, Gaza's clock and the status rules, header, footer, row, plate, review panel,
each page's script), `js\data.js` (the 13 live spaces, generated from `_shared\data`), `js\icons.js` (Lucide nodes
from app-dr's `lucide-react`, stroke 1.75).

- **Home:** the ink board leads — Gaza's time at 56 px (live, cross-fading each minute) with the day, the open-now
  count with a spark dot, «الأقرب إليّ»; the h1, the lead and an inverted search; the open spaces as board rows under
  column labels (المساحة · الحالة · اليوم · السعر). After hours the board lists spaces by when they next open
  («تفتح غدًا 08:00»), from the real week. Then the areas as a 4-column index with counts, and a one-line owners' section.
- **Directory:** an ink band (title, clock, open count), a sticky toolbar (search, «الفلاتر» below 1024, «الأقرب
  إليّ», قائمة | خريطة); the filter rail from 1024 (areas grouped by governorate, collapsed, with counts; the
  subscription segmented control, «من/إلى» once chosen; الدوام; أخرى); the results line with the sort; the rows in one
  container; «عرض 1–13 من 13». The filters filter (area, period and range, open now, evening, Friday, verified,
  students, women's hall, search in both languages); sorts: latest update, name, cheapest/dearest by period, distance;
  «الأقرب إليّ» simulates a point in الرمال with «على بعد x كم»; state in the address. `?filters=open`: rail with شهر
  and the range (4 results) / the bottom sheet «عرض 4 نتائج». `?view=map`: SVG Strip from the given outline, real
  coordinates, pins by state, nearby pins merged into count circles that zoom in, zoom buttons, wheel and drag, the
  legend top-end, the chosen pin's row as a floating panel (sheet on phone), labels only inside the Strip.
- **Space page:** all 13 slugs. The space's board: breadcrumb, the sign as a plate, the name at 48 px and the other
  name, three facts (الحالة, اليوم at 56 px, السعر «من 30 ₪ / يوم»), WhatsApp (inverted primary), Call only with a
  phone, الاتجاهات, the heart. Then the unverified line with a dialog, a filmstrip with a lightbox, the announcement,
  the prices table, the week with a spark bar on today, amenities, about (each with «آخر تحديث»), a sticky contact and
  location panel with a mini SVG map, the report link; phone bottom bar WhatsApp/Call. Elevate and Jreas show their gaps plainly.
- **Sign in:** Google, email, password with show/hide, blur and submit validation; the live board beside the form
  from 1024; a slim ink strip with the time on the phone.
- **About:** the intro at 68ch, verified vs unverified in one container, the five states on an ink board, contact and
  the owners' three steps side by side.
- **Account:** a tab row; label (4/12) / control (8/12) rows; name with «حفظ», email read-only, language and theme
  segmented (theme with حسب الجهاز), applied at once; password opens an inline change form with live rules.
- **Favourites:** the five saved spaces with their state now (Masahat's photo removed on purpose for the initial
  plate), «نور هب» as a muted row with «إزالة», removing by the heart with a toast and «تراجع».
- **404:** a board row with a dashed (no-state) bar for «الصفحة غير موجودة» and its actions, then the open-now rows.
- **Every page:** skip link, one h1, labels, «{page} · مساحة», `?lang=`/`?theme=` then stored then Arabic + device;
  switches work in place. The review panel: dashed, bottom inline-start, out of the tab order until opened, every page
  and state, «حالات تجريبية / Demo states» off by default.

## Checked
All runs through `heavy.mjs`, lane `design-a`: iterative runs, demo-state and filter cases (`demo=1` home and Branch,
`area=2&open=1` one result, the demo map, `filters=open`). Final full run: 10 pages × 390/768/1440 × ar/en ×
light/dark with `--full` — all 120 frames "clean" (no overflow, contrast, sub-12 px, focus, broken image or console
error); images read. Fixed along the way: map labels under 12 px (pixel coordinates), the lightbox's empty image, row
name links' focus ring, the row grid at 768 (rows fold below 1024), the space board's numerals at 768 (2 + 1), the
directory head given the ink band, phone touch targets to 44 px, the review toggle moved below sheets and bars, plate
focal points, a template "→" removed. The last tweaks (768 space board, Pal/Elevate focal points) were checked in a
targeted 768 run (clean); the `shots\` frames predate them.

## Weak or unfinished
The map has no governorate borders; Gaza City's pins cluster at the default zoom. «بلاغاتي», Privacy, Register and
Forgot are outside the eight pages (their links show a note). The Google button is a stand-in. Captures are from
Saturday ~14:20 Gaza time: the after-hours board («تفتح لاحقًا») is coded but not seen. The dashed "no live status"
bar is quiet by design, but 7 of 13 rows carry it today.

## Overturned (as in DESIGN.md)
foundation §7 type scale (family kept) · §4–§5 layout tokens, lists in one container, radius on containers and
controls only · DECISIONS_PUBLIC U12 (photo → 64 px plate, no card grid) · §13 Home (the board leads, areas an index)
· the hours table's today tint → a spark bar · OSM default tiles → a muted style fitted to the Strip ·
DECISIONS_ACCOUNT C6 (side nav → tab row). Not overturned: the filters stay a form, not chips.

## Builder's decisions (DESIGN.md › Builder's notes)
The spark has two weights: filled = a live «متاح», hollow = «مفتوحة الآن» by hours, the word always ink · a state
column; rows fold below 1024 · the row's price: the day's, else the first period's, else the chosen period's; an en
dash when none · verified spaces read closed outside their hours · boards after hours show when each space next opens
· the spark on ink is s-400 in both themes · posters never cropped in the filmstrip; real photos fill 4:3 or 8:3 · no
governorate borders (no source; a truth risk) — labels and clusters; land n-50 on a blue-100 sea · the directory's ink
band · the header's theme switch an icon button · the areas index in 4 columns · the space board at 768 is 2 + 1 ·
filter groups start collapsed.

## New copy (proposed)
«الآن في غزة» / "Now in Gaza" · «{n} مساحة مفتوحة الآن» (plurals) / "{n} spaces open now" · «تفتح لاحقًا» / "Opening
next" · «تفتح {اليوم|غدًا|day} {time}» / "Opens …" · «من {price} / {period}» / "From …" · «المساحة» / «الحالة» column
labels · the map cluster «{n} مساحات متقاربة، تكبير» · illustrative: «تمديد ساعات العمل حتى 22:00 طوال الأسبوع».

## Could not do
`REPORT.md` itself (the harness blocked the builder's write; the lead saved it). A shell `rm` of `A\shots\*` was
refused mid-session; the shots were overwritten instead.

## Improvement round (the lead's review, 2026-11-14)
1. **Map outline:** the directory map, the space page's mini-map and their data now use `_shared\data\strip-outline.json`
   (embedded in `js\data.js`); all 13 spaces and the governorate label points checked inside; Masar Tech now on land.
2. **Location panel:** the whole Strip in a 340×220 frame, the space as an ink pin with a white ring and halo and an ink
   tag with its area name; label «موقع {name} على الخريطة — {area}»; the frame keeps its proportion (tag text ≥ 12 px).
3. **Phone quick bar:** hidden (and out of the tab order) until the board's own actions scroll out of view, hidden again
   on the way back; the bottom padding reserved, so nothing shifts. (The frames show the top only, so the bar's entry is not captured.)
4. **Re-capture** (lane `design-a`): home, the map, Branch and Jreas at 390/768/1440 × ar/en × light/dark, `--full`:
   48/48 clean, no console errors; frames read.
