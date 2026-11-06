# DIRECTORY_FILTERS — plan (Refactor 1, prototype only)

## 0. Branch / files
- Branch: `refactor/directory-filters` (already cut from latest main)
- Files: `docs/design/prototype/Directory.html`, `docs/design/prototype/masaha/data.js`,
  `docs/design/INDEX.md`, `docs/design/CHANGES.md`, `docs/design/prototype/Flows - states.html`
- No `shared.jsx` change expected; SpaceCard price line passed as optional prop if needed,
  else rendered inside Directory.html wrapper.

## 1. Commit 1 — feat(design): sort the directory by a subscription's price (§2.1-4)
- Remove PriceField/priceRange/inRange/toLatin; delete period/priceMin/priceMax URL sync;
  activeCount drops price term; clearedFilters drops period fields.
- SORTS(): add price: السعر. Select adds item value="price".
- Sort state: [sort, setSort] + sub/dir state (sub default 'month', dir default 'asc',
  read from ?sub=/?dir= on load, written by syncUrl — extend syncUrl to take sort extras).
- PriceSortControls component: two ToggleGroup single rows — subscription from M.periods
  ordered month/week/day/hour by filter label; direction asc/desc. Shown beside/under sort
  Select in toolbar (desktop) and phone (below select, same surface).
- applyFilters: add 'price' sorter; ties then by id. priceHidden filtered out when price sort on.
- Count line: when price sort on, `<n> مساحات لها سعر شهري` via countLabel pattern + period filter name.
- Card price: Directory.html list renders price line when sort==='price' (pass via SpaceCard
  wrapper or new prop). Home/Favorites untouched.
- Checks: check-parse, check-classes both pass.

## 2. Commit 2 — feat(design): choose the directory's place by governorate (§2.5)
- Replace PlaceField combobox with two-level: governorates chips (M.governorates, skip hidden /
  no areas); tapping opens areas chips below, first «كل X» selects all; multi-select; one open at
  a time; count badge on chosen governorate; removable area chips under المنطقة.
- Phone FilterSheet: المنطقة row shows choice; tap -> governorate list in sheet; tap gov -> areas
  with «كل …» + «رجوع» back; internal view swap, not second sheet. Needs local govView state.
- Keep ?area= URL, placeLine, placeSummary. Remove Combobox usage in Directory.html only.

## 3. Commit 3 — feat(design): add open-now, evening and amenity filters (§2.6-7)
- Open-now Switch above «متاحة الآن فقط» (any space, hours vs now); caption rewrite split.
- Evening chip into others (M.others add {id:'evening'}), check today close >= 20:00; ?other= carries it.
- Amenities group: chips multi-select, all chosen must match; >6 show 6 + «عرض الكل» toggle; ?am=.
- activeCount each once; clear() clears all; FiltersForm ordering updated.
- data.js: tweak hours/prices/amenities so filters are visible (week price gaps, 22:00 close,
  varied amenities); keep all ?demo= params.

## 4. Commit 4 — docs(design): record the directory filters' round (§3)
- INDEX.md: replace ?period/priceMin row, update ?area row, add ?sort=price&sub&dir, ?am=, other=evening.
- CHANGES.md: new section «Refactor 1 — the directory's filters (2026-11-05)», one line per decision,
  naming D4, U1 combobox, U5 price range, amenities-no-filter (2026-10-12).
- Flows - states.html: price-sort frames (1440, 390) + place-open frames (desktop, phone), existing pattern.

## 5. Browser / shots / stop
- Serve: cd docs/design/prototype && npx serve .
- Look at 390/768/1440 AR+EN light/dark before each commit.
- Screenshots -> C:\Users\basel\Downloads\directory-filters-shots\ (never repo):
  price-sort list (1440, 390, AR; EN; dark), place-open (desktop, phone sheet 2 screens),
  new filters on, card with price.
- Stop once: print branch, git log --oneline main..HEAD, serve cmd, ready-to-open URLs per decision.
- Deviations: none expected; phone price controls placed directly under Select (no sort sheet exists).
