# Review of #138 (space profile, prototype) — Claude Code, Opus 5.5
Head: 5413937904f8b9f1450f372dbb02731eeded2804 · files 14 · checks: green (11 pass, CodeRabbit skipped) · head moved: no (same head at the end, `CLEAN`, 1 commit)
Verdict: mergeable after a fix round

No blocker. Four should-fix findings (two are Sheet behaviour, one a link left on Packages, one an unguarded link) and five nits.

## Findings (most severe first)

### F1 — should-fix · Escape, meant to cancel a keyboard move in «تعديل التواصل», closes the Sheet or asks «تجاهل التغييرات؟»
- **Where:** `docs/design/prototype/masaha/profile-c.jsx:279-280` (the handle's `onKeyDown={sort.key(c.id)}`), `masaha/profile-a.jsx:326-330` (Escape in `usePfReorder`) and `profile-a.jsx:256` (`PSheetContent` has no `onEscapeKeyDown`).
- **Seen in the code:** the vendored Radix layer listens for Escape on `document` in the **capture** phase (`_ds_bundle.js:2713-2727`: `ownerDocument.addEventListener("keydown", handleKeyDown, { capture: true })`, then `onDismiss()`). So it runs before React's handler on the handle. Its `e.stopPropagation()` comes too late.
- **Scenario:** open `Owner space profile.html?sheet=contacts`, Tab to a handle, press Space (the announcement says «…أو Escape للإلغاء»), ArrowDown, then Escape. The draft is dirty, so «تجاهل التغييرات؟» opens on top of the Sheet. Pressing Escape right after lifting, with nothing else changed, closes the Sheet outright. The photos are not affected: they are not in a Sheet.
- **Fix:** in `PfSheet`, pass `onEscapeKeyDown={(e) => { const t = document.activeElement; if (t && t.closest('[data-lifted]')) e.preventDefault(); }}` to `PSheetContent`, so the reorder hook's own Escape cancels the move. Then confirm it in the browser.

### F2 — should-fix · The hours Sheet counts as "changed" as soon as it opens on a space without hours
- **Where:** `masaha/profile-b.jsx:268`: `const dirty = open && JSON.stringify(pfHoursOf(v)) !== JSON.stringify(d.hours || null);`
- **Seen in the code:** with `d.hours === null`, `pfHoursDraft` fills the default Saturday–Thursday 08:00–18:00, so `pfHoursOf(v)` is an object compared with `"null"`. That makes `dirty` true with nothing touched. The other Sheets avoid this with `usePfDraft`, which compares with the copy taken at opening (R7's comment, `profile-a.jsx:289-290`).
- **Scenario:** `Owner space profile.html?demo=nohours` (or `Admin space edit.html?id=white` / `?id=new`): «أضف ساعات العمل», then «رجوع» (or ✕, Escape, the overlay). «تجاهل التغييرات؟» appears although nothing changed. This contradicts CHANGES.md's G1 line ("A change asks…").
- **Fix:** take a base at opening (`base = JSON.stringify(pfHoursOf(pfHoursDraft(d.hours)))` in the `[open]` effect) and compare `pfHoursOf(v)` with it.

### F3 — should-fix · A link still sends the owner to Packages to change the prices
- **Where:** `docs/design/prototype/Owner settings.html:87`. The «تسعير الزيارات» card shows the hour and day prices with `<a href="Packages.html#prices">الباقات والأسعار</a>`.
- **Seen in the code:** after R1, `Packages.html#prices` is read-only. This card is where an owner sees that visits are billed from those prices, and the link now leads to a read-only table that needs a second hop. CHANGES.md's R1 line says "Every «الأسعار» link … lands on `Owner space profile.html#prices`", and this one was missed (the file is unchanged in the PR).
- **Scenario:** Settings → «الباقات والأسعار» beside the hour and day prices → Packages, read-only → «تعديل الأسعار في ملف المساحة».
- **Fix:** `href="Owner space profile.html#prices"` (or `?sheet=prices#prices`), labelled «الأسعار المعلنة». It is in `docs/design/`, so it stays in scope.

### F4 — should-fix · The admin's «إدارة قائمة المرافق» leaves an edited Sheet without asking
- **Where:** `masaha/profile-b.jsx:470`: a plain `<a href={manage}>` inside the amenities Sheet (only `Admin space edit.html` passes `manage`).
- **Scenario:** `Admin space edit.html?id=golden&sheet=amenities`, tick an amenity, then click «إدارة قائمة المرافق». The page navigates away and the change is lost, with no «تجاهل التغييرات؟». The prices Sheet's «أضف وردية» goes through `close(then)` for exactly this reason (`profile-b.jsx:169`).
- **Fix:** render the Sheet's children as a function and route the link through `close(() => { location.href = manage; })`, as the prices Sheet does.

### F5 — nit · The two pages disagree on whether the sample space has shifts
- **Where:** `Packages.html:36` (`SHIFTS_NOW` = `SAMPLE_SHIFTS()` unless `?demo=noshifts`; package p4 «صباحي للطلاب» uses `am`) against `masaha/owner-data.js` (`profile.shifts` is empty unless `?demo=shifts`).
- **Scenario:** the profile says «لا توجد ورديات…», and one click away Packages shows two shifts and a package on the morning one.
- **Fix:** have Packages read `O.profile.shifts`, with `?demo=shifts` there too (moving the default frames to `noshifts`), or note the difference in INDEX.

### F6 — nit · L2's pin drag is not built, and nothing records why
- **Where:** `masaha/profile-c.jsx:128` (`SpaceMap … picking onPick`): tap to place, tap again to move.
- **Seen in the code:** L2 says "the pin dragged or placed by a tap". The plan's workarounds cover only the map drawing Gaza City alone, and CHANGES says "placed by a tap" without a reason.
- **Fix:** add a line to CHANGES ("the prototype moves the pin by a second tap; dragging is the production map's"), or use `map.jsx`'s existing `pickAtCentre` mode.

### F7 — nit · A new space (`?id=new`) has no hide or delete in the top bar
- **Where:** `Admin space edit.html:95`: `const actions = isNew ? [] : […]`.
- **Scenario:** H4 puts the admin's actions in the top bar. A space the admin has just created can be neither hidden nor deleted there, and nothing says why.
- **Fix:** keep both actions for `id=new`, or write the reason in CHANGES.

### F8 — nit · CHANGES.md groups decisions instead of one line each
- **Where:** `docs/design/CHANGES.md`, the Refactor 2 table: rows such as «G5, H4, P7, R5», «W1–W5», «S1–S4», «C1, C2, M3, M4».
- **Seen in the code:** the prompt asked for "one line per decision, naming what it revises", and Refactor 1's table above is one decision per row. The revisions themselves are named, in the intro paragraph.
- **Fix:** split the rows, or accept the grouping knowingly.

### F9 — nit (plausible) · The custom hours rows label every time field just «من» / «إلى»
- **Where:** `masaha/profile-b.jsx:296-304`.
- **Scenario:** a screen-reader user tabbing through «تخصيص الأيام» hears «من» seven times. The day's name is a plain `span`, not the group's label (the simple view's Friday uses a `fieldset` with a `legend`).
- **Fix:** make each `li` a `fieldset` with `<legend>{n}</legend>`, or label the fields «السبت من» and so on.

Also seen, outside this PR's scope: `masaha.css:62` keeps `.section-anchor{scroll-margin-top:8.5rem}` below 1024, which was sized for the chips row this PR removes (G3). The phone anchors may now land too low. The browser pass will show it; it is plausible only.

## The decisions, one line each (built / missing / different)
- **G1** built: view first, one `PfSheet` per section, «حفظ» / «رجوع», «تجاهل التغييرات؟» on every close (but see F1, F2, F4).
- **G2** built: header · الصور · الأسعار المعلنة · ساعات العمل · الورديات · المرافق · عن المساحة · الموقع · التواصل (`SpaceProfile`).
- **G3** built: title, muted date, «تعديل»; stale badge with «ما زالت صحيحة»; empty frame with its action; report inside its section; index with dots from 1024, none on a phone.
- **G4** built: the saved-alone line, the checklist and the page-level dirty alert are gone from both pages.
- **G5** built: both pages render `SpaceProfile`.
- **H1** built: no «تعديل» on the header.
- **H2** built: cover or letter tile with «أضف صورة غلاف» (opens the photos' edit state), name, area and governorate with «موثّقة», «عرض الصفحة العامة» in a new tab, «نسخ الرابط», «N من 7 أقسام» with the bar and the missing/stale links, or «الملف مكتمل ومحدّث».
- **H3** superseded by M2.
- **H4** built: «غير موثّقة» and «مخفية عن الزوار», hide and delete in the top bar (none for `id=new`, F7).
- **M2** built in the CSS: a 4 rem square beside the name; buttons and bar span the card (`.pf-hdr`, `grid-cols-2` buttons); layout unverified without a browser.
- **P1** built (desktop ≥ 768): cover over two of three columns beside a 2×2 grid, «+N» past five; head «الصور» with «N من 10 صور» and «إدارة الصور»; empty state with its three lines; no date.
- **M1** built: 16:9 cover with «الغلاف» and «N صور», one sideways row of 6 × 4.5 rem thumbnails, no «+N».
- **P2** built: edit in place, «تم», each act saved at once.
- **P3** built: «اختر صورًا» (multiple), the limits line, a bar per upload, the reason on a refused tile, the limit sentence replacing the button.
- **P4** built: native drag plus the keyboard (Space, arrows by direction, Home/End, Space, Escape), each step announced; no move buttons. Touch is left to the library, recorded.
- **P5** built: «حذف هذه الصورة؟» with «حذف» and «رجوع».
- **P6** built: «الغلاف» in view and edit, and the drag hint.
- **P7** built: the same on the admin's page.
- **R1** built: Packages shows the prices read-only with «تعديل الأسعار في ملف المساحة» (`?sheet=prices#prices`); the overview, audit and data-report links moved, but Owner settings did not (F3).
- **R2** built: period, audience, optional shift and amount; saved labels kept.
- **R5** built: the same on the admin's page.
- **R6** built: rows with «الفترة» · «لمن» · «الوردية» (only with shifts, «بدون وردية» first) · «المبلغ (₪)» · remove; one header line from 768, a stacked block per row on a phone; no description field.
- **R7** built: empty state with «إضافة سعر»; one starting row; the next row prefilled with the first free period for everyone, then the students'; immediate removal.
- **R8** built: «الأسعار المعلنة» and «إضافة سعر».
- **R9** built: «هذا السعر مضاف من قبل» on the second row, «أدخل المبلغ» on its row; the view shows «لمن» and the shift only when present.
- **W1** built: grouped days, «اليوم», the closure link (owner only), the empty state.
- **W2** built: «من السبت إلى الخميس», «الجمعة: إجازة», «تخصيص الأيام».
- **W3** built: the Friday box with its own «من» / «إلى», prefilled.
- **W4** built: seven rows; day-varying hours open customised; «سيتم توحيد الساعات…» on the way back.
- **W5** built: 30-minute lists to 24:00; a day switched on takes the last open day edited; «نسخ إلى كل الأيام» gone; «إلى» after «من» said on its row (after «حفظ»); phone blocks. The empty-hours dirty bug is F2.
- **S1** built: its own section after the hours.
- **S2** built: one line of shifts, and the optional empty text with «إضافة وردية».
- **S3** built: rows with a name, «من» and «إلى» from the lists, «إضافة وردية»; inside at least one open day; remove disabled with its reason when a price or package uses the shift.
- **S4** built: «الوردية» only with shifts, otherwise «أضف وردية», which asks first if the Sheet changed.
- **S5** executor check, recorded in CHANGES.
- **A1** built: only what is offered, icon and name, 3 columns (2 on a phone), own amenities after with the generic icon, empty state.
- **A2** built: checkbox rows with icons in 2 columns (1 on a phone), «أُزيل من القائمة» on a held retired amenity, «مرافق أخرى» rows with «إضافة مرفق آخر», the catalogue message (see F4 for the admin's link).
- **B1** built: two columns, each in its own direction, four lines then «عرض المزيد», the missing-language effect line.
- **B2** built: names side by side, «مطلوب» on the English name, «اختياري» on the rest, the «N / 1000» counters, «تغيير الاسم لا يغيّر رابط صفحتك».
- **L1** built: area line, the address in the interface's language with the other muted, the landmark, a static map and «فتح في خرائط Google», the effect line.
- **L2** different: area `Combobox` grouped by governorate, addresses and landmarks side by side, a large map, «استخدم موقعي الحالي», «الموقع خارج قطاع غزة», no search, the coordinates field kept (with a reason); the pin is not dragged (F6).
- **C1** superseded by M3.
- **C2** built: rows with a handle, a type with its icon, the value with its placeholder and its stored form, remove; a new row is WhatsApp; invalid values and repeats said on the row; drag by the handle plus the keyboard (Escape broken, F1).
- **M3** built: tiles in 3 columns (2 on a phone), each a working link (wa.me, tel:, mailto:, https).
- **M4** built: تيليجرام، X، لينكدإن، يوتيوب and «وسيلة أخرى» with its own name; the production migration is recorded as owed.
- **A3** later, not built: correct.

## The plan's alternatives and workarounds, judged
- **Touch dragging left to the production library:** sound. The dependency is approved, and it is recorded in CHANGES.
- **«نسخ الرابط» through `navigator.clipboard` plus a toast:** sound.
- **«استخدم موقعي الحالي» simulated, with the coordinates field kept as the keyboard's way to place the pin:** sound. The extra field is justified (the map has no keyboard pin, and the outside-the-Strip line needs a way to be reached).
- **Each pair of sections over one group with one date, one staleness and one «ما زالت صحيحة»:** acceptable for the prototype. The partial save is correctly made an executor check (S5, B2).
- **Placeholder SVG icons:** sound (as F-6).
- **Times to 24:00, overnight deferred:** acceptable, as W5 says.
- **Custom description dropped; saved labels shown, not edited:** acceptable. A labelled row can't change its period and only goes by deleting it, which is fine until the executor's data check.
- **Alternative — an English name per shift:** sound and cheap (the model has it; the English UI now shows Arabic names). The owner should choose it. Built as decided, which is correct.
- **Alternative — «عن المساحة» complete only with an Arabic description:** sound. It is the public page's main text, and the effect line alone doesn't move the bar. Built as decided; owner to choose.
- **Alternative — drop the admin's unverified alert:** acceptable either way. The header badge now says the same thing; owner to choose.

## Records (INDEX, CHANGES, Flows)
- **Flows:** section «Refactor 2 — the space profile» with 26 frames. Its URLs and order match INDEX §58 one to one, and the rows don't overlap (the 768 × 1024 frame's row is followed at +1104).
- **INDEX:** the parameter rows are updated (`id=new` / `white` / `palm` / `pricelimit` / `ownlimit`, `demo=missing`, `Packages.html#prices`, `noshifts`, `report=d2` now on the profile), `shifterror` removed, a new «Refactor 2» parameter table, and §58. They match the code (`demo` keys in `owner-data.js`, `?sheet=` / `?photos=edit` in `SpaceProfile`).
- **CHANGES:** «Refactor 2 — the space profile (2026-11-08)» names what it revises: A1's editor, A2's checklist, O1/O6, G1's «مرافق إضافية», AD-006's types, the old order, and P9 kept. It lists the open production items (touch library, M4 migration, S5/B2, custom description). It is true to the code except R1's "every link" (F3) and the grouping (F8).
- **Scope:** all 14 files are under `docs/design/`. One commit, `feat(design): redesign the space profile`, Conventional, with no tool attribution.
- **Global scope:** no top-level name in `profile-a/b/c.jsx` is declared again in any other script of the three pages (`shared`, `owner` / `admin`, `map`, `desk-core`, the data files, the inline scripts) or exported by them. The inline scripts' new names (`space`, `groups`, `initial`, `notice`, `missing`, `profile`, `own`, `prices`, `PUBLISHED`…) collide with nothing and none is browser-owned. There is no object rest. The aliases (`P*`, `Q*`, `R*`) are unique. The exports this PR removed (`PricesSection`, `HoursSection`, `CONTACT_TYPES`, `dirtySet`, …) are used nowhere else. `Space details.html` uses `space-parts.jsx`'s own sections and loads no profile module. `Admin space add.html` uses only exports that were kept.

## Not checked, and why (the browser pass is the supervisor's)
- **Nothing was run** (read-only review). Everything here comes from the code at the head, including F1's ordering, which comes from reading the bundle's Radix source; F1 should be confirmed in the browser.
- **`check-parse.mjs` / `check-classes.mjs` are not in CI** (no workflow or `package.json` script runs them), and I did not run them. I spot-checked about 90 of the new classes against `_ds_bundle.css` / `masaha.css` and all exist, but a full run is the supervisor's.
- **Not looked at in a browser:** layouts at 390/768/1024/1440 (above all M2's header, M1's thumbnail row, the price and contact row grids), dark mode, English, overflow, focus trapping and return, toasts, the live-region wording as spoken, `navigator.clipboard`, and the map's pin placement.
- **Not compared:** the mock-up (`mockup\index.html`) against the pages, visually.
