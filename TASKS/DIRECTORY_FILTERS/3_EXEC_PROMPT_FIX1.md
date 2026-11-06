# DIRECTORY_FILTERS — correction 1 (the owner's review of the first build)

The owner rejected the first build. **This file supersedes §2 of `3_EXEC_PROMPT.md`** where they differ; everything
else there (where, how, limits, checks, the prototype's traps, the stop-once loop) still holds. Read it whole.

**The rule of this round: no chips anywhere in the directory's filters or sort** — no `ToggleGroup` chips for the
place, the price, «أخرى» or anything else.

## 1. Start

- `git branch backup/directory-filters-1` (keeps the first build).
- Work on `refactor/directory-filters`. The history is local and unpushed, so you may rewrite it: end with **two
  commits** on top of `main` (no fix commits, no `fixup!` left):
  1. `feat(design): rework the directory's filters and sort` — everything in `Directory.html`, `masaha/data.js`,
     `masaha/i18n.js`, `masaha/shared.jsx`, `Flows - states.html`.
  2. `docs(design): record the directory filters' round` — `docs/design/INDEX.md`, `docs/design/CHANGES.md`.
  A body on each saying what and why. `git reset --soft main` then commit by explicit path is fine.

## 2. What to build

1. **The sort is one `Select`, no chips.** Items, grouped with `SelectGroup` + `SelectLabel`:
   - (no label) «الأحدث تحديثًا» / "Latest update", «الاسم» / "Name"
   - «الشهري» / "Monthly": «السعر الشهري: الأقل أولًا» / "Monthly price: lowest first", «السعر الشهري: الأعلى أولًا» /
     "Monthly price: highest first"
   - the same for «الأسبوعي» (weekly), «اليومي» (daily), «بالساعة» (hourly), in that order.
   The trigger shows the chosen item whole («الترتيب: السعر الشهري: الأقل أولًا» may be shortened to the item alone if
   it overflows at 390 — check it). Remove the chip rows under the sort entirely. URL stays
   `?sort=price&sub=month&dir=asc` (defaults omitted as before). «الأقرب إليّ» is unchanged.
   While a price sort is on: a space without that subscription's price, or whose prices are hidden
   (`M.priceHidden(s)`), leaves the list; the count says so («8 مساحات لها سعر شهري»); the card shows that price
   («250 ₪ / شهر», LTR-isolated). An empty result says it plainly («لا توجد مساحات لها سعر شهري») with the existing
   empty state's pattern.
2. **Remove the amenities filter completely** (the group, its state, its `?am=` param, its count, its data changes
   if they were only for it). The owner cancelled it on 2026-10-12.
3. **Remove «متاحة الآن فقط» and «مفتوحة الآن»** from the filters, and the caption under the switches. Their URL
   params (`available`, any open-now param) are no longer written; an old link still opens, unfiltered by them.
   «المساحات الموثّقة فقط» stays as a `Switch`.
4. **«أخرى»: three `Checkbox` rows**, each a `Field` with its label: «أسعار للطلاب», «مفتوحة يوم الجمعة», «مفتوحة
   مساءً» («Open in the evening»: today's closing time is 20:00 or later). URL `?other=students,friday,evening`.
5. **The place: one dropdown field «المنطقة».**
   - The trigger looks like the page's other select triggers. It reads «اختر المنطقة» / "Choose an area" when nothing
     is chosen, otherwise the choice: the area's name, or «كل {المحافظة}» / "All of {governorate}".
   - It opens a panel (the design system's `Combobox` if its content can hold collapsible group headers; otherwise a
     `Popover` holding an `Input` and a hand-built list — say which in the report). Inside, top to bottom:
     - a **search field** («ابحث عن منطقة» / "Search for an area");
     - **six collapsible rows**: the active governorates by their short names (`M.govShort`; skip a hidden one or one
       with no areas) — الشمال، غزة، الوسطى، خان يونس، رفح as the data has them — and a sixth, **«كل المناطق»** / "All
       areas", which opens every area of the Strip;
     - a row is a disclosure (a chevron at the end, `aria-expanded`), never a selected state; one row open at a time;
     - an open governorate lists «كل {المحافظة}» first, then its areas, indented; «كل المناطق» lists every area, each
       with its governorate as a second, muted line.
   - **One choice.** Picking an area, or «كل {المحافظة}», applies it and closes the panel; the chosen item shows a
     check when the panel reopens. Clearing the place: an item «كل القطاع» / "The whole Strip" at the very top of the
     list (above the six rows) and the filters' «مسح».
   - Typing in the search replaces the rows with the matching areas, flat, each with its governorate's line (search
     both languages, as the page's search already does).
   - Keyboard: the trigger opens with Enter/Space; arrows move through the visible rows; Enter on a governorate row
     opens it, on an area picks it; Escape closes and returns focus to the trigger.
   - URL: an area → `?area=<id>`; a whole governorate → `?gov=<id>`; never both. An old multi-area link
     (`?area=a,b`) still opens, filtered by those areas, but the field then reads «مناطق محددة» until changed.
   - The count line: «في {المنطقة}», «في {المحافظة}», or «في قطاع غزة».
   - The same field on a phone, inside the filter sheet (the panel opens over the sheet's content; no second sheet).
6. **The active-filter count** counts: the place, verified only, and each «أخرى» box. The price sort is a sort, not a
   filter, and is not counted. «مسح» clears the filters, not the sort.

## 3. The records (commit 2)

- `INDEX.md`: the rows match the final URL set — `?sort=price&sub=…&dir=…`, `?area=<id>`, `?gov=<id>`,
  `?other=students,friday,evening`, `?verified=1`; remove `?am=`, `?available=`, `?period=`, `?priceMin=`,
  `?priceMax=` rows (say in one line that old links still open unfiltered).
- `CHANGES.md`: rewrite the round's section to what is built now: R1 the price sort, R2 no amenities (the
  2026-10-12 decision stands), R3 live status and open-now out of the filters for now, R4 «أخرى» as checkboxes with
  the evening, R5 the place dropdown, R6 `?gov=`; it revises D4 (the card shows the price under a price sort), U1
  (the combobox and "no governorate filter"), U5 (the price range).
- `Flows - states.html`: the frames point at the final states (a price sort; the place panel open on a governorate;
  the place panel searching; the phone sheet with the place open). No frame for removed states.

## 4. Before you stop — production-grade review of your own work

Open every state in a browser at **390, 768 and 1440**, **Arabic and English**, **light and dark**, and check:

- nothing overflows or wraps badly (the sort trigger at 390, long area names, the count line);
- no block drawn twice, no leftover chip, no leftover removed filter or caption, no console error;
- RTL and LTR mirror correctly (chevrons, indentation, the price's LTR isolation);
- every text exists in both languages; no English left in Arabic or the reverse;
- the URL round-trips: reload and Back show the same state; every old param named above opens without breaking;
- both checks pass: `node docs/design/scripts/check-parse.mjs`, `node docs/design/scripts/check-classes.mjs`.

Then new screenshots into `C:\Users\basel\Downloads\directory-filters-shots\fix1\` (each item of §2, desktop and
phone, one English, one dark), and **stop once** as before: print `git log --oneline main..HEAD`, the serve command,
and a ready URL per state. In the report later, list anything the web's design system lacks for this (for example
collapsible groups in `Combobox`).
