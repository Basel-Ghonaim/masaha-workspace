# FIX PUBLIC — reply to your plan

A careful plan: S1's period that qualifies the range, the opt-in map props that leave the editor's map
alone, and the weak-connection frames are right. **Approved**, with one change of the owner's to the
card (below) and the answers to §13. **First, save it** (as approved here, with the changes below) to
`C:\Users\basel\.prompt\MASAHA_DESIGN\PLAN\FIX_PUBLIC_PLAN.md`, then cut `design/public` from
`origin/main` (check it is still the latest) and build.

## The owner's change: the card shows no prices

The owner decided (2026-10-12, recorded in `DECISIONS_PUBLIC.md`'s amended note):
- **No prices on any space card** (Home, the Directory, Favourites): no price cells, no student line.
  **Prices live on the space page only** (U9 there stays as you planned).
- **The cover photo sits at the top of the card** — your reading of U12 — and **the card must be
  striking**: the photo leads. Below it, what makes someone open the space: its display name, its
  area, its live state (verified) or «لا تتوفر حالة مباشرة», today's hours, the distance when a
  location is in use; the heart over the photo for a signed-in visitor. Build it from the design
  system's components and tokens only; give it hierarchy and rhythm worthy of the site's first
  impression, at 390, 768 and 1440, in both themes. **Show the card first in your report** (before
  and after at each width), so the owner judges it by eye.
- **The sort loses «الأقل سعرًا»:** a sort by a price the card does not show reads as random. The sort
  is «الأحدث تحديثًا · حسب الاسم», with «الأقرب إليّ» as U2 builds it. **The price filter stays**
  (a budget), with S1's period.
- **SH-021's «للعرض فقط · الدفع في المساحة»** leaves the lists' header line (no prices there now) and
  stays once in the space page's prices.
- Update §2, §4 (U5, U9's card line, U12/H2, the skeleton) and §11 accordingly; the cover commit's
  subject may become `docs(design): a striking space card` (count it).

## The owner's decisions (§13)

1. **S1–S6:** approved.
2. **Design issues:** build **1** (one location control: «موقعي» only as «مركّز على موقعي» while a
   location is in use), **2** (a shorter frame below `md`; weigh it again now that the card has no
   price cells — keep it striking, not tall), and **4** (Favourites at three columns from `xl`);
   **3** is recorded for worker A's design-system item (a wifi-off icon); **5** only if your eyes see
   the combobox clip in the phone's sheet.
3. **The cover's place:** at the top of the card, as you read it.

## Two corrections

- **H4 and finding 10:** finding 10 is **resolved** — the code draws every amenity icon (#49). What
  lacks them is the prototype's vendored bundle. Keep one neutral mark for every amenity, common and
  own, as you planned (it keeps them alike, the owner's rule), but write the true reason in
  `CHANGES.md`: the bundle has no amenity icons, not finding 10.
- **The data you remove or retype** (`lastReview`, `statusUpdated`, the contacts' `jawwal`/`ooredoo`,
  ZM Hub's `nameAr`, `nameAr` moving from `details-data.js`): before each change, `grep` every reader
  across the whole prototype (the admin's pages and the editor included) and say in the report which
  readers you found and that none broke; you may not edit the other worker's files to fix one — stop
  and say so.

## Reminders

- **Truth to the product:** live status is a state, never a count; the location never leaves the
  device.
- Your two scripts at every commit; `format:check` and `check:links` by CI (say so).
- At the report, `git merge-tree --write-tree` against every open PR (the other design worker's
  `design/admin-rest`, workers A and B, the amenities PR).
- The analyst reviews it. Don't merge. Stop every background shell you start; `jq` is not installed —
  use `gh … --jq`.
