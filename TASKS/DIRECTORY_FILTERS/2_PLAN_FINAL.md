# DIRECTORY_FILTERS — final round: the plan

Branch `refactor/directory-filters`, 5 commits + the approved uncommitted price filter and 1024–1279 column.
Backups: branch `backup/directory-filters-3`, files in `backup-3\`. Nothing is committed this round.

## Files
- `prototype/Directory.html` — panel order and groups, open-now / evening logic, sort labels, caption, dead code.
- `prototype/masaha/data.js` — `eveningShift: true` on Number One (verified, closes 18:00); `others` tolerates no hours.
- `prototype/masaha/shared.jsx` — `resultsLabel` plurals; `TodayHours` copes with `hours: null`.
- `prototype/Flows - states.html`, `INDEX.md`, `CHANGES.md` — records.
- `masaha.css` — no change expected (the 1024–1279 rule stays as is).

## Order
1. `Directory.html`: state `open` (bool) + `others` (evening, friday, students, verified); `?verified=1` read on
   load into `others`, written back as `other=…verified`. Groups «المنطقة» → «السعر» → «الدوام» → «أخرى», Checkbox rows
   in `Field`; Switch and «المساحات» heading gone. Active count = areas + sub + open + others.
2. Open now: Gaza's clock through `Intl.DateTimeFormat('en-GB', { timeZone: 'Asia/Gaza' })` (weekday, hour, minute),
   today's range contains the minute, no closure. Every space; FULL stays; no hours → never.
3. Evening: any open day closing ≥ 20:00, or `eveningShift`. Replaces `openEvening`.
4. Sort labels («الأرخص شهريًا» …, "Monthly price: low to high" …; «الأرخص» / «الأغلى» under «الكل»), the caption
   «بالشيكل، على السعر الشهري.», dead imports (`SelectGroup`, `SelectLabel`, `Switch`) and the duplicate `DAY_KEYS`.
5. `shared.jsx`: plurals; `TodayHours` shows «ساعات العمل غير متوفرة» when a space has no hours.
6. Records; then the two checks; then the browser pass and the screenshots.

## What I cannot build as written, and what I do instead
- **Closures.** They exist, but in `details-data.js` (Number One's «مغلقة مؤقتًا حتى الخميس»), which the
  Directory does not load. I load `masaha/details-data.js` in `Directory.html` (as Favorites and Space details do),
  so open-now honours `s.closure`. Side effect: the Directory's map shows Number One's pin as closed, as on the
  other pages. `details-data.js` itself is not edited.
- **`hours: null` in `data.js`.** Space details reads it through `masaha/space-parts.jsx` (`TodayLine`,
  `HoursSection`, `groupDays`), which is outside the allowed files and would throw. So the null is **not** added
  to `data.js`. Instead `Directory.html?demo=nohours` drops ZM Hub's hours on the Directory only, so the card's
  «ساعات العمل غير متوفرة» and «never passes open-now / evening» can be seen. The space page's text is owed to
  the step that may touch `space-parts.jsx` (recorded in the report).
- **The board.** The earlier «Directory — Refactor 1» section (top 9984) overlaps «Space details — variants»
  (top 10054). I move it to the end of the board (after the last section) instead of shifting 500 frames, and
  INDEX gets it as a new last section, «57 · Refactor 1 — the directory's filters»; its old rows in §03 and the
  duplicated ones in §53 go. Batch 3's board frame with the gone `?period=day` points at `?sub=day&priceMax=20`.
- `TodayHours` reads the browser's day, not Gaza's; it is not this round's — recorded, not fixed.
