## Summary

Refactor round 1 of the live site: the directory's filters, redesigned **in the design prototype only**. The panel
now reads, top to bottom, «المنطقة» · «السعر» · «الدوام» · «أخرى», and the order by price lives in the sort. The web
app and the API follow in a later PR, which decides the revised design decisions with the docs.

## Scope

- **In scope:** 8 files under `docs/design/`: `prototype/Directory.html`, `prototype/Flows - states.html`,
  `prototype/masaha/data.js`, `prototype/masaha/masaha.css`, `prototype/masaha/shared.jsx`,
  `prototype/masaha/space-parts.jsx`, `INDEX.md`, `CHANGES.md`.
- **Acceptance criteria:** the decisions below, built as listed and recorded in `CHANGES.md` › *Refactor 1* and
  `INDEX.md` (URL parameters and §57).
- **Out of scope:**
  - `apps/` and `packages/`; nothing in the product changes here.
  - The docs outside `docs/design/`. The revisions of D4, U1, U5 and ADR 0008 (the filter by `AVAILABLE`) are owed
    by the production step and are recorded in `CHANGES.md` for it.
  - Spaces for women: approved as a direction, with its own ticket.
  - The owner-declared evening shift: a future feature, simulated in the sample data only (`eveningShift`).

## The decisions built

- **The price.** A segmented choice, «الكل · ساعة · يوم · أسبوع · شهر», with «الكل» by default (a radiogroup with
  arrow keys).
  - Once a subscription is chosen: a «من / إلى» range in shekels, with placeholders from the data and the caption
    «بالشيكل، على السعر الشهري.».
  - The range is validated: whole numbers above zero, Arabic-Indic digits are read, and «إلى» below «من» is flagged
    on «إلى».
  - Only the spaces with that price are listed, and their cards show it.
  - The price order is in the sort («الأرخص شهريًا» / «الأغلى شهريًا», and the same for the other subscriptions). Its
    items are shown only once a subscription is chosen; clearing the subscription returns the order to «الأحدث
    تحديثًا».
  - URL: `sub`, `priceMin`, `priceMax`, `sort=price`, `dir=desc`.
- **«الدوام».**
  - «مفتوحة الآن»: by the hours on Gaza's clock (`Asia/Gaza`) and the closures, for verified and unverified spaces
    alike. A space without hours never passes.
  - «مفتوحة مساءً»: the space closes at 20:00 or later on one of its open days, or declares an evening shift.
  - «مفتوحة يوم الجمعة».
  - URL: `open=1`, `other=evening,friday`.
- **«أخرى».** «المساحات الموثّقة فقط» (now a checkbox; the «المساحات» heading and its switch are gone) and «أسعار
  للطلاب». URL `other=students,verified`; an old `?verified=1` still opens filtered and is then written the new way.
- **«ممتلئ» is a badge, not a filter.** A full verified space stays in «مفتوحة الآن».
- **An unverified space's state by its hours.**
  - With hours, its card and its page say «مفتوحة الآن» or «مغلقة الآن», as a neutral badge (it is no live state).
  - Without hours, they keep «لا تتوفر حالة مباشرة».
  - One rule, `openNow` in `shared.jsx`, serves both this badge and the filter.
- **Hours are optional.** ZM Hub has none. Its card and its page (the today line and the hours section) say «ساعات
  العمل غير متوفرة».
- **The sheet's button uses the Arabic plurals:** «لا توجد نتائج», «عرض نتيجة واحدة», «عرض نتيجتين», «عرض N نتائج»,
  «عرض N نتيجة». English is unchanged. The button is shared by every page's filter sheet.
- **The filter column** is 4 of 12 between 1024 and 1279, so the five subscriptions fit on one line.

## Change type

Design prototype (docs).

## Evidence

From the repository root, on the pushed head:

```
$ node docs/design/scripts/check-parse.mjs
51/51 blocks parsed, from 42 pages and the modules
$ node docs/design/scripts/check-classes.mjs
338 classes used, 5 dead uses, 0 new
$ npm run check:links
3240 links in 251 documents and 2609 source files all resolve.
$ npm run check:conflicts
No conflict markers found.
```

- **Looked at in a browser** (headless Chrome) at 390, 768, 1024 and 1440, in Arabic and English, light and dark:
  - Directory: list, map card and phone sheet, open now, price range, price sort, the sort's items, the old
    `?verified=1` link.
  - Space details for ZM Hub, Golden Hub and Number One.
  - Home's nearest list, Favorites, and the filter sheets of Customers and Admin spaces.
  - 192 loads in the final pass: no console error, no horizontal overflow, the URL the same after reload.
- **Not run:** test lanes, build, lint, typecheck. No file under `apps/` or `packages/` changed, so no application
  code is affected.

## Screenshots

Kept locally in `Downloads\directory-filters-shots\` (not pushed). Ready prototype URLs, after
`python -m http.server 5325 --directory docs/design/prototype`; each also works with `&lang=en` and `&theme=dark`:

- Open now: `http://localhost:5325/Directory.html?loc=none&open=1`
- Price range: `http://localhost:5325/Directory.html?loc=none&sub=month&priceMin=250&priceMax=400` (phone:
  add `&sheet=filters`)
- Price sort: `http://localhost:5325/Directory.html?loc=none&sub=week&sort=price&dir=desc`
- A space without hours: `http://localhost:5325/Directory.html?loc=none&q=ZM` and
  `http://localhost:5325/Space%20details.html?id=zm&loc=none`
- An unverified space with hours: `http://localhost:5325/Space%20details.html?id=golden&loc=none`
- The board: `http://localhost:5325/Flows%20-%20states.html` (its last section)

## Definition of Done checklist

- [x] Acceptance criteria met, scope kept: only the 8 files under `docs/design/`.
- [ ] N/A: Lint and typecheck clean; build passes. No application code changed; the prototype's own two checks
  pass (above).
- [ ] N/A: Tests in the owning lane. The prototype has no test lane; its checks are `check-parse` and
  `check-classes`.
- [x] No hardcoded user-facing text: every new string in the prototype is written in both languages with `tr("…", "…")`.
  The product's catalogues are untouched (no product code).
- [x] UI checked in RTL and LTR, light and dark, phone and desktop (390, 768, 1024, 1440).
- [ ] N/A: Authorization on the server. No protected action.
- [x] Triggered documentation updated in the same PR: `CHANGES.md` and `INDEX.md`. No deferred document's trigger
  is met.
- [x] Each fact has one home. Nothing is claimed as built in the product; the revisions owed by the production step
  are recorded, not applied.
- [x] Every claim in this description names the command or check that proves it (Evidence).
- [x] History pushed and PR description complete. It is **one commit** by the owner's instruction: the round is one
  unit, the prototype with the records that describe it.
