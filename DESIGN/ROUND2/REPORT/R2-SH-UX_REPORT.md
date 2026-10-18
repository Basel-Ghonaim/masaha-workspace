# R2-SH-UX — The shared layer · Experience and flow

- `git rev-parse HEAD`: `34a6c59aab049e8f2992b29b88c8a700b926ddba`
- `git rev-parse origin/main`: `34a6c59aab049e8f2992b29b88c8a700b926ddba`
- Match: yes — review ran on `origin/main` (after `git fetch origin`).
- Server: `python -m http.server 5436 --bind 127.0.0.1 --directory docs/design/prototype` from `C:\Users\basel\masaha-design`.

## Verdict

The shared patterns hold together across the three shells, but seven pattern-level UX gaps remain — the phone sheets first.

## Five most important points

1. All eight add/edit/reply sheets open as side drawers on phones instead of bottom sheets.
2. Two visitor-facing one-tap actions («إنهاء الآن», hide/show) skip the P9 confirmation.
3. Payments and Finance debts have no search, breaking P5's always-visible search.
4. Owner Customers shows five status chips where P5 allows four.
5. The 768 rail is icons without names, so touch users cannot find pages there.

## Issues

### R2-SH-UX-001 — Add/edit sheets are side drawers on phones, not bottom sheets

- **type:** defect · **level:** pattern · **impact:** high · **cost:** M
- **where:** INDEX §41 frame "New announcement sheet — phone 390", prototype URL `http://127.0.0.1:5436/Announcements.html?sheet=new&type=event`, phone layout (<768, Arabic light; capture at 700px viewport, see §6 note), board screenshot `docs/design/screens/38-announcements-owner-reception/12-new-announcement-sheet-phone-390.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\SH-UX\R2-SH-UX-001.png`
- **What is wrong:** every add/edit/reply flow uses `SheetContent side="end"` at every width, so on a phone the form slides in from the side as a narrow drawer (capture: the new-announcement sheet covering the left ~60% at a 700px viewport; narrower still at 390). The shared layer already settled the opposite idiom for phones: `FilterSheet` uses `side="bottom"` below its breakpoint, and the Directory's map sheet is `side="bottom"` too. A receptionist adding a customer or subscription — an all-day phone money flow — gets the cramped drawer while filters get the thumb-friendly bottom sheet. Same job, two gestures.
- **Proposal:** make all eight sheets responsive: `side="bottom"` below 768, `side="end"` from 768 up. Pages changed: `Desk.html` (subscription / new-customer sheet in `masaha/desk-sheet.jsx`), `Staff.html`, `Announcements.html`, `Packages.html`, `Admin owners.html`, `Admin lookups.html`, `Admin reports.html`, `Data reports.html`.
- **Why it is better:** one sheet gesture per width across the product; bottom sheets on phones put the form, its errors and its submit inside thumb reach instead of a side strip.
- **rule:** REVIEW_LENS §3 B.4 (same job, same way); precedent: P5 `FilterSheet` (`masaha/shared.jsx`, `side="bottom"`) and `Directory.html` map sheet.

### R2-SH-UX-002 — «إنهاء الآن» and hide/show act at once, though visitors feel them

- **type:** defect · **level:** pattern · **impact:** medium · **cost:** S
- **where:** INDEX §38 frame "Active · owner — phone 390", prototype URL `http://127.0.0.1:5436/Announcements.html`, phone layout (<768, Arabic light), board screenshot `docs/design/screens/38-announcements-owner-reception/02-active-owner-phone-390.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\SH-UX\R2-SH-UX-002.png`
- **What is wrong:** `Announcements.html` «إنهاء الآن» ends a closure/active announcement at once with an undo toast (`endNow`), and `Admin spaces.html` hide/show (`toggleHide`) does the same. Both change what visitors see — a closure ends and the public state flips back to automatic; a space leaves or rejoins the site. P9 sends exactly this class ("felt by others") to an `AlertDialog` with no undo after, even when technically reversible (cf. the settled space-delete exception). The capture shows «إنهاء الآن» sitting next to «تعديل» as an equal-weight button, although one rewrites the public page and the other opens a form.
- **Proposal:** confirm both with an `AlertDialog` naming the true consequence («سيتوقف الزوار عن رؤية الإغلاق وتعود الحالة تلقائية» / «ستختفي المساحة من الموقع»), action `variant="destructive"` repeating the verb, dismiss «رجوع», success toast without undo. Pages changed: `Announcements.html`, `Admin spaces.html`.
- **Why it is better:** a one-tap slip no longer rewrites the public listing; the ten-second undo window stops being the only protection for visitors and subscribers.
- **rule:** DECISIONS_SHARED P9 (confirm-or-undo classification).

### R2-SH-UX-003 — Payments and Finance debts have no search

- **type:** defect · **level:** pattern · **impact:** medium · **cost:** S
- **where:** INDEX §32 frame "Ledger · this month — phone 390", prototype URL `http://127.0.0.1:5436/Payments.html`, phone layout (<768, Arabic light), board screenshot `docs/design/screens/32-payments-owner/02-ledger-this-month-phone-390.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\SH-UX\R2-SH-UX-003.png`
- **What is wrong:** P5's filter bar starts with "search always visible", and every other list has it (Customers by name/mobile digits, Admin spaces/users/owners, Admin audit, Directory). The Payments ledger toolbar is only `FilterSheet` (range/staff/method/type) plus the voided chip — no way to find one customer's payments without paging. Finance debts is the same: a paged debtor list with no search. The capture shows the Payments phone toolbar going straight from «الفلاتر» to the totals row.
- **Proposal:** add the one search, always visible, to both toolbars — Payments by customer/item, Finance debts by customer name (the desk's name-or-mobile-digits rule where a mobile exists) — leaving the rest of the filters in the sheet. Pages changed: `Payments.html`, `Finance.html` (debts tab).
- **Why it is better:** the two money-chasing lists become findable the same way as every other list; an owner with months of ledger stops paging to answer "did X pay?".
- **rule:** DECISIONS_SHARED P5 (one filter bar).

### R2-SH-UX-004 — Owner Customers shows five status chips; P5 allows four

- **type:** defect · **level:** pattern · **impact:** medium · **cost:** S
- **where:** INDEX §56 frame "Customers · five columns, status chips — tablet 768" (and §26 "Customers · owner — phone 390"), prototype URL `http://127.0.0.1:5436/Customers.html`, phone layout (<768, Arabic light; also seen at 768 and 1440), board screenshots `docs/design/screens/26-customers-reception-vs-owner/04-customers-owner-phone-390.webp` (phone; the 768 frame has no board screenshot yet)
- **evidence:** `C:\Users\basel\Downloads\r2-shots\SH-UX\R2-SH-UX-004.png`
- **What is wrong:** P5 allows a status filter as `ToggleGroup` chips only for "four or fewer choices". Reception sees four (الكل/نشط/ينتهي قريبًا/منتهي); the owner gets a fifth, «مؤرشف», in the same chip group — mixing a live lifecycle status with a separate archived view. On phones five chips wrap into two rows and push the count/add row down; conceptually «مؤرشف» is not a fifth status but a different drawer (it even swaps the row action to «استرجاع»).
- **Proposal:** keep four lifecycle chips and move «مؤرشف» out of the group into a standalone chip by the count — the Admin spaces «قديمة أو ناقصة» precedent (a `ToggleGroup type="multiple"` beside `ResultCount`). Pages changed: `Customers.html`.
- **Why it is better:** the chip row stays within the settled four, and the archived view reads as what it is: a separate list with its own row action, not a fifth customer state.
- **rule:** DECISIONS_SHARED P5 (status chips ≤4); precedent: `Admin spaces.html` stale chip (A7).

### R2-SH-UX-005 — The 768 rail is icons without names

- **type:** improvement · **level:** pattern · **impact:** low · **cost:** M
- **where:** INDEX §29 frame "Overview — desktop 1440" (`Owner overview.html`; the board has no 768 frame — REVIEW_LENS §2c notes this), prototype URL `http://127.0.0.1:5436/Owner%20overview.html`, 768×1024, Arabic light, board screenshot `docs/design/screens/29-owner-overview-kept/01-overview-desktop-1440.webp` (desktop; no 768 board shot exists)
- **evidence:** `C:\Users\basel\Downloads\r2-shots\SH-UX\R2-SH-UX-005.png`
- **What is wrong:** at 768–1023 both dashboard shells collapse to an icon-only rail: group labels vanish and the twelve owner items (four reception, eight admin) show as bare glyphs whose only names are hover tooltips. Foundation §13 requires shells to work at 768, and this prompt judges daily-task findability on the rail — but 768 tablets are touch-first: no hover, so a receptionist or owner must tap through unknown icons to find a page (the h1 confirms only *after* arriving). The switcher marks (space initial / «م») are the only named rail items, per SH-006; the pages themselves are not.
- **Proposal:** give the rail icon-over-caption buttons (short label under each icon, rail slightly wider) with dividers where the group labels were, tooltips kept for pointer users. Pages changed: all dashboard pages via the two shells (`masaha/owner.jsx` `OwnerShell`, `masaha/admin.jsx` `AdminShell`).
- **Why it is better:** each role keeps finding its daily tasks first at 768 without tap-and-hope; the P3 grouping survives the collapse instead of flattening into twelve equal glyphs.
- **rule:** DECISIONS_SHARED P3 (navigation grouped by task, judged on the 768 rail per this prompt §5.1); `docs/frontend/design-system/foundation.md` §9/§13 (responsive, 768 checked); REVIEW_LENS §3 B.7.

### R2-SH-UX-006 — Breadcrumb current page repeats the h1 record name

- **type:** improvement · **level:** pattern · **impact:** low · **cost:** S
- **where:** INDEX §27 frame "Subscriptions · partly paid — phone 390", prototype URL `http://127.0.0.1:5436/Customer%20file.html?id=m6`, phone layout (<768, Arabic light), board screenshot `docs/design/screens/27-customer-file/02-memberships-partly-paid-phone-390.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\SH-UX\R2-SH-UX-006.png`
- **What is wrong:** SH-016/P1 settle "sub-page h1 as the record's name with a Breadcrumb back", but all three dashboard sub-pages render the name twice stacked: breadcrumb «الزبائن › رهف قديح» and then h1 «رهف قديح» (capture). The breadcrumb's current-page crumb carries no information the h1 does not already carry, while costing a full row on phones.
- **Proposal:** breadcrumb carries the parent link only (the way back: «الزبائن» / «المساحات»); the h1 keeps the record's name alone. Pages changed: `Customer file.html`, `Admin space edit.html`, `Admin space add.html`.
- **Why it is better:** one name, one row: the back way stays, the repetition goes, and phone sub-pages start one row higher.
- **rule:** DECISIONS_SHARED P1/SH-016.

### R2-SH-UX-007 — Search is a labelled field on admin lists, unlabelled elsewhere

- **type:** improvement · **level:** pattern · **impact:** low · **cost:** S
- **where:** INDEX §43 frame "Spaces — phone 390", prototype URL `http://127.0.0.1:5436/Admin%20spaces.html`, phone layout (<768, Arabic light), board screenshot `docs/design/screens/43-admin-spaces/02-spaces-phone-390.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\SH-UX\R2-SH-UX-007.png`
- **What is wrong:** the same job — the one list search — is drawn two ways: admin lists (`Admin spaces/users/owners/audit`, `Owner audit`) wrap it in a visible `Field label=«بحث»` (capture: «بحث» label above the input, costing a row on phones), while `Customers.html` and `Directory.html` use an unlabelled input with magnifier, placeholder and `aria-label`. Both are accessibly named, so this is pure pattern inconsistency (B.4): five lists spend a phone row on a label two lists prove unnecessary.
- **Proposal:** one search shape everywhere: the Customers/Directory unlabelled search (icon + placeholder + `aria-label`), dropping the redundant «بحث» `Field` labels. Pages changed: `Admin spaces.html`, `Admin owners.html`, `Admin users.html`, `Admin audit.html`, `Owner audit.html`.
- **Why it is better:** every list toolbar starts the same way and phone lists gain back one row; the magnifier-plus-placeholder carries a search box without a label, as the site lists already show.
- **rule:** REVIEW_LENS §3 B.4 (patterns across pages); DECISIONS_SHARED P5 (one filter bar).

## Decisions in doubt

None. P1–P10 held everywhere they were applied; the issues above are misapplications or unhandled cases, not rules I judge wrong.

## What was not reviewed and why

- **Match statement:** `HEAD` equals `origin/main` (`34a6c59…ddba`), so no stop was needed. The known stray `<<<<<<< HEAD` line before INDEX.md §54 was seen during reading and, per the prompt note, is not reported.
- **Out of axis (left to the other prompts/parts):** visual polish and tokens (VD), anything broken/overflowing/mis-mirrored (DF), wording and translation quality (CP), focus order/names/contrast/targets/reader order (AX), API/model/v1 truth and permissions (TR/parts), and all page-level issues (the parts). Pattern-level only, per §5.
- **Verified without defect, not filed:** P1 page header + ⋯ + desk-only bottom bar (Desk/Customers/Finance/Admin spaces at 390/768/1440); P2 public-state control; P3 grouping on desktop rail/drawer (owner/admin/reception); P4 account menu both ways + site phone avatar + owner drawer-head account (DI-10); P6 pagination (numbers hidden on phones, shown from 768, «عرض 1–20 من N»); P7 route states (offline/403/404 in-shell, load error with retry); P8 toasts above the desk bottom bar (captured live), in-dialog failures kept with input (`?fail=checkout`), desk K7 exception; P10 enabled saves; SH-005/SH-006/SH-016/SH-018 applied. English LTR (`Admin spaces.html?lang=en`) and dark (`Desk.html?role=reception&theme=dark`) spot-checks showed the same patterns; no separate dark/EN issue.
- **Methodology note:** phone evidence was captured at a 700px viewport, which renders the identical <768 phone breakpoint (cards, filter button + bottom sheet, ⋯ menus, bottom bars). True-390 headless captures of the dashboard shells clip the right edge identically on every page (a headless-viewport artifact of the closed off-canvas drawer), so they cannot serve as crops; every URL/parameter in §4 reproduces the finding at true 390 in a real browser.
- **Not reached:** `?state=ratelimit` inside desk money dialogs and the 768 rail tooltip behaviour on real touch hardware (hover-only by code inspection); no interaction beyond loading URLs with parameters was performed (read-only review, no edits).
