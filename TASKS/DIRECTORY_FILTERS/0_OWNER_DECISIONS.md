# DIRECTORY_FILTERS — the owner's decisions (2026-11-05)

The first round of the refactor: the directory page «المساحات» (`Directory.html` in the prototype, `/spaces` in the
web). Decided with the main supervisor on 2026-11-05. This round changes the **prototype only**; the web and API
follow on the same branch later, in the PR that this round's commits will ride.

## The filters and the order

1. **The price range and the period leave the filter panel.** «من/إلى» and «الفترة» (ساعة · يوم · أسبوع · شهر) are
   removed. *Why:* typing numbers is a poor experience, and the period alone selects nothing.
2. **«السعر» joins the sort, with its subscription and its direction, as one choice.** The sort list holds «الأحدث
   تحديثًا», «الاسم» and «السعر». Choosing «السعر» shows two chip rows beside the sort (inside the sort's sheet on a
   phone): the subscription — **شهري** (default) · أسبوعي · يومي · ساعة — and the direction — **الأقل سعرًا**
   (default) · الأعلى سعرًا. *Why (the owner):* each subscription has its own audience and each space its own offer
   per subscription (5 ₪/hour with 250 ₪/month against 4 ₪/hour with 500 ₪/month), so no single price can rank
   spaces, and a direction without a subscription means nothing. It is a sort, not a filter, so the order has one
   control. «الأقرب إليّ» stays its own control.
3. **A space without a price for the chosen subscription leaves the list while the price sort is on,** and the count
   says so («8 مساحات لها سعر شهري»). A space whose prices the page hides (unverified and stale) leaves it too, as
   today. *Why:* an owner enters a price to be found by it (the owner's usage guide will say so, later).
4. **The card shows the chosen subscription's price, only while the price sort is on** («250 ₪ / شهر»). *Revises*
   D4 (2026-10-12, «the card carries no price»), for this one case. *Why:* an order by price with no price shown
   cannot be read.
5. **The place filter has two levels:** the governorates (the active ones, as chips), then a governorate's areas as
   chips under it, its first chip «كل {المحافظة}»; more than one area, across governorates, may be chosen. On a phone,
   «المنطقة» opens a screen of the governorates, a governorate opens a screen of its areas, with «رجوع». The choice
   shows as removable chips. No typing is needed; the search box still finds an area by name. *Revises* U1's
   combobox (and its "no governorate filter").
6. **New filters:** «مفتوحة الآن» by the space's hours (any space, verified or not — also the fix direction for
   Home's empty «المتاحة الآن», REFACTOR_NOTES 2026-11-02); the amenities as chips (all chosen must be offered);
   «مفتوحة مساءً». *Revises* «the amenities are no filter» (2026-10-12).
7. **«أخرى» (student prices, open on Friday) and «المساحات الموثّقة فقط» stay.** The caption under «متاحة الآن فقط» is
   reviewed once «مفتوحة الآن» exists beside it.

## Revision 1 — after the first look (2026-11-05, supersedes items 2, 5, 6 and 7)

The first build used chips everywhere and brought back the amenities; the owner rejected it. The supervisor's own
proposals caused both (chips in the spec; the amenities revived without asking although the owner had cancelled them
on 2026-10-12). **No chips anywhere in the directory's filters or sort.**

- **R1 — the price sort is one `Select`**, every option whole: «السعر الشهري: الأقل أولًا», «السعر الشهري: الأعلى
  أولًا», and the same for weekly, daily and hourly, grouped under a label per subscription, after «الأحدث تحديثًا»
  and «الاسم». The subscription and the direction are one choice, one click. Items 3 and 4 stand (a space without
  that price leaves the list; the card shows that price).
- **R2 — the amenities filter is dropped** (the owner's 2026-10-12 decision stands).
- **R3 — «متاحة الآن فقط» is dropped from the filters for now**, with its caption: a larger architectural decision
  on live status comes later. **«مفتوحة الآن» (by hours) is dropped too** (the supervisor's recommendation, approved):
  it would be confused with it; both return with that decision. «المساحات الموثّقة فقط» stays.
- **R4 — «أخرى»: «أسعار للطلاب», «مفتوحة يوم الجمعة», «مفتوحة مساءً» (today's closing time 20:00 or later),** as
  `Checkbox` rows, not chips.
- **R5 — the place: one dropdown field «المنطقة»** (option b, the owner's choice): its trigger reads «اختر المنطقة»
  (no filter) or the choice; it opens a panel with a **search field** on top, then **six collapsible rows** — الشمال،
  غزة، الوسطى، خان يونس، رفح (the active governorates, short names) and a sixth, **«كل المناطق»**, which opens every
  area of the Strip. A governorate opens its areas, the first «كل {المحافظة}». **One choice:** an area, or a whole
  governorate; picking closes the panel. Typing in the search shows the matching areas flat, each with its
  governorate. The same field on a phone, inside the filter sheet.
- **R6 — a whole governorate is its own URL value, `?gov=<id>`** (the supervisor's recommendation, approved): an area
  list would miss an area added to the governorate later, and a governorate may outgrow the API's 50-area limit. The
  API needs a `governorate` filter back in the production step.

**For the production step (the web and API PR, same branch):** the web's `Combobox` must support collapsible groups
and a group-level choice (a design-system extension); the API gains `sort=price` with the period and the direction
(the hidden-price rule applied), a `governorate` filter, `evening`, and loses `period`/`priceMin`/`priceMax`;
`availableNow` stays in the API (Home reads it) and only leaves the directory's filters; `docs/features/directory.md`,
the API contract and the decisions D4/U1/U5 are updated in that PR.

## The method (approved 2026-11-05)

- An **OpenCode** worker in `C:\dev\masaha\app`, a normal round: branch `refactor/directory-filters` from the latest
  `main`, atomic Conventional Commits, explicit staging, no tool attribution. **No PR, no push** (the branch stays
  local until the web/API work opens the PR on it).
- Files: `docs/design/` only (the prototype, `INDEX.md`, `CHANGES.md`, the board). Nothing in `apps/`, `packages/` or
  the rest of `docs/`.
- Checks: the prototype's two scripts only (`check-parse`, `check-classes`); no test lane, build or lint.
- A short plan file, the work without stopping, then **one stop** for the owner's review by eye; his notes in the same
  session, each folded into its commit (`backup/*` first, `--fixup` + autosquash); then the report.
- The web/API docs (`docs/features/directory.md`'s D4, U1 lines, the API contract) change with the production work,
  not in this round.
