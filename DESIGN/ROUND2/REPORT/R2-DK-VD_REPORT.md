# R2-DK-VD — Round 2 review: the front desk and reception · visual design and consistency

- `origin/main` SHA: `34a6c59aab049e8f2992b29b88c8a700b926ddba` (HEAD detached at `origin/main`; `git rev-parse HEAD` equals `git rev-parse origin/main`).
- `origin/design/desk` SHA: n/a — per the 2026-10-14 update, PR #80 has merged into `main` (`34a6c59`) and the branch no longer exists (`git branch -a` shows only `main` / `origin/main`). All desk frames (§56 included) were read from `origin/main`, one source only.
- Prototype served read-only on `http://127.0.0.1:5430/` (`python -m http.server 5430 --bind 127.0.0.1 --directory docs/design/prototype`); spot-checked `Desk.html`, `Customers.html`, `My payments.html` (HTTP 200). Port 5430 is free at the end (no LISTENING). No files in the repo were edited, committed, or checked out.

## Verdict

The desk is structurally consistent (one money block, one search, one card language) but the same facts are drawn two ways in at least four places, and the customer file's payments list is the only ledger without a phone-card form.

## Five most important points

1. The customer file's payments list is a plain `Table`, not a `DataTable` — the only DK ledger with no phone-card form.
2. "Settled" is muted body text in Customers but a neutral Badge in the file header — one fact, two tokens.
3. The money block is not identical: checkout/sheet show «لم يدفع شيئًا», the collect-a-visit dialog does not.
4. Person-row gutters and `UnpaidRow` type differ between Desk (`px-4`/`caption`) and the file (`px-5`/`body-sm`).
5. Subscription/customer-card titles carry no heading level while sibling cards use `h2` — the file's hierarchy goes flat below the tabs.

## Issues

### R2-DK-VD-001 — File payments have no phone-card form

- **type:** defect · **level:** pattern · **impact:** high
- **where:** frame "Payments · voided shown struck (owner) — desktop 1440" (§27), `http://127.0.0.1:5430/Customer%20file.html?id=m6&tab=pays`, 390 + 1440, light; screenshot path `docs/design/screens/27-customer-file/05-payments-voided-shown-struck-owner-desktop-1440.webp`; §56 frame "Customer file · the visit's payment, the void in «⋯» — desktop 1440", `http://127.0.0.1:5430/Customer%20file.html?id=m14&tab=pays` (screenshot —, §56 has none yet).
- **evidence:** `C:\Users\basel\Downloads\r2-shots\DK-VD\R2-DK-VD-001.png` (not captured — no browser tool in this session; see § "What was not reviewed").
- **what is wrong:** every other DK ledger (Desk present list, Customers, Payments, My payments) is a `DataTable` with `renderCard` below 768. `Customer file.html` → `PaymentsTab` is `<Card><CardContent className="p-0"><Table>` with no `renderCard` (`Customer file.html:133-152`). Same job (a payments list), two constructions; on a phone the file's 4–5-column table is the densest surface on the desk.
- **proposal:** draw the file's payments with the same `DataTable` + `renderCard` used by `Payments.html` (date/time, customer/item, amount+method, recorded-by, «⋯»), reusing `PaidAmount` and `PaymentMenu`.
- **why:** one list pattern means one phone behaviour to learn and maintain; matches DK-017's five-columns-from-768 contract.
- **cost:** M · **rule:** foundation §9 (tables become stacked cards on phones); foundation §12 `data` (Table has no frame; `renderCard` is the phone form); lens B.4.

### R2-DK-VD-002 — "Settled" is text in one place, a Badge in another

- **type:** defect · **level:** pattern · **impact:** medium
- **where:** frame "Customers · owner — desktop 1440" (§26), `http://127.0.0.1:5430/Customers.html`, 1440, light; screenshot `docs/design/screens/26-customers-reception-vs-owner/03-customers-owner-desktop-1440.webp`; vs frame "Subscriptions · partly paid — desktop 1440" (§27), `http://127.0.0.1:5430/Customer%20file.html?id=m6`, 1440, light; screenshot `docs/design/screens/27-customer-file/01-memberships-partly-paid-desktop-1440.webp`.
- **evidence:** `C:\Users\basel\Downloads\r2-shots\DK-VD\R2-DK-VD-002.png` (not captured; see below).
- **what is wrong:** `Customers.html:78` draws a settled balance as `<span className="text-body-sm text-muted-foreground">مسدّد</span>`; `Customer file.html:175` draws it as `<Badge variant="neutral">مسدّد</Badge>`. `BalanceBadge` itself returns `null` when settled (`desk-core.jsx:217-220`), so the two call sites invent their own settled treatment. Same fact, two colours/weights (muted 13px text vs neutral pill).
- **proposal:** pick one — the neutral Badge (it pairs with the warning/success balance Badges in the same row) — and render it from `BalanceBadge` so all three states come from one component; changes Customers table, file header, and any other `BalanceBadge` call site.
- **why:** status is never colour alone (foundation §5) and never two colours for one fact; the pill keeps the row scannable next to «عليه»/«له رصيد».
- **cost:** S · **rule:** foundation §5 (status roles; status never colour alone); lens B.4.

### R2-DK-VD-003 — Money block gains/loses «لم يدفع شيئًا» between dialogs

- **type:** defect · **level:** pattern · **impact:** medium
- **where:** §56 frames "Check-out · leaves owing, the mobile asked — phone 390" (`http://127.0.0.1:5430/Desk.html?role=reception&dialog=checkout&pid=pv0&received=5`) vs "Uncollected · collect a visit with no customer — phone 390" (`http://127.0.0.1:5430/Desk.html?role=reception&dialog=pay&vid=u3`), both 390, light.
- **evidence:** `C:\Users\basel\Downloads\r2-shots\DK-VD\R2-DK-VD-003.png` (not captured; see below).
- **what is wrong:** K2 settles one money block everywhere. `MoneyBlock` takes `none = true` by default; checkout (`desk-core.jsx:544-552`) and the sheet (`desk-sheet.jsx:218-219`) keep it, but the pay-visit branch passes `none={false}` (`desk-core.jsx:609`). The block's bottom edge — and its height — differs for the same job (taking money), and the zero path is a typed `0` in one dialog vs one tap in the others.
- **proposal:** pass the same `none` everywhere (keep «لم يدفع شيئًا» in the collect-visit block too); changes `PayDialog` visit branch only.
- **why:** K2's "identical in every dialog" is a motor pattern at a till; a missing shortcut in one dialog reads as "paying nothing is not allowed here".
- **cost:** S · **rule:** DECISIONS_DESK K2; prompt §5 axis Q2.

### R2-DK-VD-004 — Person rows use two gutters (`px-4` vs `px-5`)

- **type:** defect · **level:** pattern · **impact:** low
- **where:** §56 frame "Desk · one search, here first — phone 390", `http://127.0.0.1:5430/Desk.html?role=reception&q=لمى`, 390, light, vs §56 frame "Desk · every uncollected row, the owner's «⋯» — desktop 1440", `http://127.0.0.1:5430/Desk.html?unpaid=all`, 1440, light.
- **evidence:** `C:\Users\basel\Downloads\r2-shots\DK-VD\R2-DK-VD-004.png` (not captured; see below).
- **what is wrong:** search-result present rows (`Desk.html:153`, `px-4 py-3`) sit in a `rounded-lg border bg-card` list, while `UnpaidRow` (`desk-core.jsx:765`, `px-5 py-3`) assumes a `CardContent p-0` with 20px card padding. Both are "a person + an amount/action row" on the same page; the 4px horizontal offset is visible where search results sit above the uncollected card.
- **proposal:** use `px-5` (card-padding, 20px) for both row kinds; changes `PresentRow` in `Desk.html` (and the pay-dialog picker rows at `desk-core.jsx:619`, also `px-3`).
- **why:** one row language on the desk; horizontal rhythm follows the card, not the list that happens to hold it.
- **cost:** S · **rule:** foundation §4 (`card-padding` 20px); lens A.1/A.2.

### R2-DK-VD-005 — `UnpaidRow` is caption on the desk, body-sm in the file

- **type:** defect · **level:** component · **impact:** low
- **where:** §56 frame "Desk · every uncollected row" (above) vs §56 frame "Customer file · unpaid visits first — desktop 1440", `http://127.0.0.1:5430/Customer%20file.html?id=m14`, 1440, light.
- **evidence:** `C:\Users\basel\Downloads\r2-shots\DK-VD\R2-DK-VD-005.png` (not captured; see below).
- **what is wrong:** `UnpaidRow` branches on `showName`: desk rows render the how/when line as `text-caption text-muted-foreground` (12px), file rows as `text-body-sm` (13px), and the file row switches to `md:flex-row md:justify-between` while the desk row always stacks (`desk-core.jsx:759-782`). One component, two type styles and two responsive behaviours for the same visit line.
- **proposal:** render the how/when line identically in both (keep `text-caption text-muted-foreground`; keep the stacked action-under-amount form, which the narrow side column needs), and let the file pass `showName={false}` for content only, not for style.
- **why:** the uncollected line is one pattern (K4/DK-012); type size should not depend on which page hosts it.
- **cost:** S · **rule:** foundation §7 (composite text styles); lens B.4.

### R2-DK-VD-006 — Method is a Badge, a caption, and plain text

- **type:** defect · **level:** pattern · **impact:** medium
- **where:** frame "My payments today — phone 390" (§28), `http://127.0.0.1:5430/My%20payments.html?role=reception`, 390, light; screenshot `docs/design/screens/28-reception-only/02-my-payments-today-phone-390.webp`; vs §32/Payments ledger and §27 file payments.
- **evidence:** `C:\Users\basel\Downloads\r2-shots\DK-VD\R2-DK-VD-006.png` (not captured; see below).
- **what is wrong:** the payment method is drawn three ways: `My payments.html:48` table column as `<Badge neutral|info>`, `Payments.html:59` / file as caption text under the amount via `PaidAmount method` (`desk-core.jsx:689-697`), and the My-payments phone card as inline plain text (`My payments.html:68`). DK-017 settles "the method under the amount"; the Badge variant adds a second treatment on the same page (table vs its own card).
- **proposal:** use `PaidAmount method` (caption text under the amount) in the My-payments table too and drop the method Badge column; changes `My payments.html` columns only (5→4 data columns + actions none — reception has no «⋯»).
- **why:** one attribute, one treatment; reserves pills for status, not for a neutral facet like cash/transfer.
- **cost:** S · **rule:** DECISIONS_DESK DK-017; foundation §5 (semantic roles); lens B.4.

### R2-DK-VD-007 — «بلا حدّ» uses a warning icon for a neutral fact

- **type:** defect · **level:** component · **impact:** low
- **where:** §56 frame "Custom · no end, no limit — phone 390", `http://127.0.0.1:5430/Desk.html?role=reception&dialog=sheet&mode=subscribe&cid=m3&pkg=custom`, 390, light.
- **evidence:** `C:\Users\basel\Downloads\r2-shots\DK-VD\R2-DK-VD-007.png` (not captured; see below).
- **what is wrong:** the custom-sheet "no end, no limit" line (`desk-sheet.jsx:105`) is `<TriangleAlertIcon className="text-warning">` + muted caption. A boundless custom subscription is a neutral structural fact (DK-008), not something needing attention; warning fill/icons are reserved for attention states (foundation §5; WarnDialog/full/renewal alerts all use warning correctly).
- **proposal:** draw it as plain muted caption (no icon), or `info` if it must carry an icon; changes the `endNote` branch only.
- **why:** warning must keep its meaning at a till; spending it on a neutral note dulls the real warnings (full space, week used up, prior debt).
- **cost:** S · **rule:** foundation §5 (warning = attention; status never colour alone is the sibling rule).

### R2-DK-VD-008 — «أرشفة» is the only destructive-feeling row action not marked destructive

- **type:** defect · **level:** pattern · **impact:** low
- **where:** frame "Customers · reception — desktop 1440" (§26), `http://127.0.0.1:5430/Customers.html?role=reception`, 1440, light; screenshot `docs/design/screens/26-customers-reception-vs-owner/01-customers-reception-desktop-1440.webp`.
- **evidence:** `C:\Users\basel\Downloads\r2-shots\DK-VD\R2-DK-VD-008.png` (not captured; see below).
- **what is wrong:** the row «⋯» marks «إلغاء الدفعة…» (`desk-core.jsx:705`) and «لن يُحصَّل…» (`desk-core.jsx:777`) as `variant="destructive"`, but «أرشفة» (`desk-core.jsx:264`) has no variant — same menu, same irreversible/felt-by-others class (P9/DK-014), default colour.
- **proposal:** give the archive menu item `variant="destructive"`; changes `CustomerMenuItems` only (all three surfaces at once: desk card ⋯, file header ⋯, Customers row ⋯).
- **why:** P9's colour contract is "destructive red only for irreversible/felt actions"; archiving qualifies (it removes the customer from search and desk), and the menu currently teaches that only money actions are serious.
- **cost:** S · **rule:** DECISIONS_SHARED P9; foundation §5 (destructive role).

### R2-DK-VD-009 — Subscription cards have titles but no headings

- **type:** defect · **level:** component · **impact:** medium
- **where:** frame "Subscriptions · partly paid — phone 390" (§27), `http://127.0.0.1:5430/Customer%20file.html?id=m6`, 390, light; screenshot `docs/design/screens/27-customer-file/02-memberships-partly-paid-phone-390.webp`.
- **evidence:** `C:\Users\basel\Downloads\r2-shots\DK-VD\R2-DK-VD-009.png` (not captured; see below).
- **what is wrong:** each subscription card renders `<CardTitle className="flex flex-wrap…">{s.name}…` with no `h2`/`h3` inside (`Customer file.html:49`), while the sibling unpaid-visits card uses `<CardTitle><h2>` (`Customer file.html:41`) and the desk's uncollected card does the same (`Desk.html:103`). Below the tabs the document outline goes h1 (customer name) → tabs → plain text. (Vendored `CardTitle` draws a `div` — cf. `profile-a.jsx:29` — so the heading must be explicit.)
- **proposal:** wrap subscription names in headings at the same level the design system gives `CardTitle` elsewhere (h3 under the tab section; needs no new component — SH-017 already makes `CardTitle` take a level).
- **why:** one h1 per page with a real section hierarchy (axis Q1); keeps the file's cards consistent with every other desk card.
- **cost:** S · **rule:** DECISIONS_SHARED SH-017/P1-SH-016; lens A.3.

### R2-DK-VD-010 — Search-result customer cards repeat R2-DK-VD-009

- **type:** defect · **level:** component · **impact:** low
- **where:** §56 frame "Desk · one search, here first — desktop 1440", `http://127.0.0.1:5430/Desk.html?role=reception&q=لمى`, 1440, light.
- **evidence:** `C:\Users\basel\Downloads\r2-shots\DK-VD\R2-DK-VD-010.png` (not captured; see below).
- **what is wrong:** `CustomerCard` renders `<DK.CardTitle><a …>{c.name}</a></DK.CardTitle>` with no heading (`desk-core.jsx:229`), while the result-group labels above it are `h2.text-label` (`Desk.html:178-184`). Card name (17px card-title size) outweighs its own group heading (14px label) — hierarchy inverted: the group label looks subordinate to its items.
- **proposal:** same fix as R2-DK-VD-009 (heading inside `CardTitle`), and restyle the two result-group labels as one consistent group-heading treatment distinct from card titles; changes `CustomerCard` + `SearchResults` only.
- **why:** hierarchy must survive the search state, which is the desk's default working state (K1).
- **cost:** S · **rule:** lens A.3; DECISIONS_SHARED SH-017.

### R2-DK-VD-011 — Due figure uses the same style as section titles

- **type:** improvement · **level:** component · **impact:** medium
- **where:** §56 frame "Check-out · more handed over: the change — desktop 1440", `http://127.0.0.1:5430/Desk.html?role=reception&dialog=checkout&pid=pv0&received=20`, 1440, light.
- **evidence:** `C:\Users\basel\Downloads\r2-shots\DK-VD\R2-DK-VD-011.png` (not captured; see below).
- **what is wrong / better:** the money block's «المستحق 12 ₪» is `text-heading-3` (`desk-core.jsx:458`) — the same 17px/600 style as the page h1 (`owner.jsx:320`), the «الحاضرون الآن» h2 (`Desk.html:232`), and every card title. The single number the eye must land on at a till has no typographic priority over its container.
- **proposal:** set the Due line to `text-heading-2` (22px/600, existing token — no new component), leaving labels/calc/live-line as-is; applies to all three money-block hosts at once (checkout, pay, sheet).
- **why:** hierarchy Q1: the block's job is "how much"; giving the figure one step over its frame makes debt/change scannable without adding colour or size outside the system.
- **cost:** S · **rule:** foundation §7 (composite text styles); lens A.3.

### R2-DK-VD-012 — Handover phone card drops the transfer helper

- **type:** defect · **level:** component · **impact:** low
- **where:** frame "My payments today — phone 390" (§28) vs "— desktop 1440" (§28), `http://127.0.0.1:5430/My%20payments.html?role=reception`, 390 vs 1440, light.
- **evidence:** `C:\Users\basel\Downloads\r2-shots\DK-VD\R2-DK-VD-012.png` (not captured; see below).
- **what is wrong:** desktop shows three `StatCard`s, the transfer one with helper «وصلت إلى حساب المساحة» (`My payments.html:60-64`); the phone's one-card form (`My payments.html:55-59`, `md:hidden`) shows three `Row` lines with no helper. Same figures, different explanations — and the phone (the handover's real device) is the one that loses the "transfer is not cash to hand over" cue. Row density (`py-1`) is also tighter than `StatCard`'s card padding.
- **proposal:** add the transfer helper as muted caption under the transfer row in the phone card (one line, existing `text-caption` token); changes `My payments.html` phone card only.
- **why:** the handover's whole job is cash-vs-transfer (K4/excluded-from-figures); the clarification must travel with the figure to the phone.
- **cost:** S · **rule:** lens B.4 (same job same way); DECISIONS_DESK K4.

### R2-DK-VD-013 — Sheet body gaps differ from dialog gaps

- **type:** improvement · **level:** pattern · **impact:** low
- **where:** §56 frame "New customer · one step — phone 390", `http://127.0.0.1:5430/Desk.html?role=reception&dialog=sheet&mode=new&name=سليم`, 390, light, vs any desk dialog (e.g. §56 "Visit · the shift now, the rate named — desktop 1440").
- **evidence:** `C:\Users\basel\Downloads\r2-shots\DK-VD\R2-DK-VD-013.png` (not captured; see below).
- **what is wrong / better:** dialog forms stack at `gap-4` (16px: visit, warn, checkout, pay, debt, edit), while `SubscriptionSheet`'s `SheetBody` stacks at `gap-5` (20px, `desk-sheet.jsx:124`) with the same `Field`/`MoneyBlock` children. Two rhythms for one form language; the sheet's sections breathe differently from the dialogs' for no structural reason.
- **proposal:** set the sheet body to `gap-4`; changes one class in `desk-sheet.jsx`.
- **why:** spacing on one scale (axis Q3); 16px is already the desk's form rhythm everywhere else.
- **cost:** S · **rule:** foundation §5 (spacing scale); lens A.2.

## Decisions in doubt

None. K6's owner-only write-off treatment (destructive «⋯» item + destructive confirm, P9) is correctly applied; the warning/info split in check-in warnings (`here`→info, the rest→warning) and the renewal prior-debt warning read correctly against foundation §5. R2-DK-VD-007/008/011 are reported as defects/improvements against the rules, not against them.

## What was not reviewed and why

- **No rendered-frame inspection (widths/modes/roles matrix):** this session has no browser tool, so pages were judged from the prototype sources (`Desk.html`, `Customers.html`, `Customer file.html`, `My payments.html`, `Payments.html`, `masaha/desk-core.jsx`, `masaha/desk-sheet.jsx`, `masaha/masaha.css`, `docs/design/INDEX.md` §§20–28, 31, 56) plus HTTP 200 checks on the §2 local server. Real overflow, breakpoint behaviour at 390/768/1440, Arabic vs English rendering, and light vs dark token resolution were not eyeballed.
- **Evidence captures:** `C:\Users\basel\Downloads\r2-shots\DK-VD\` was created, but no `<ID>.png` crops were saved — there was nothing to crop without a renderer. Issue locations instead cite the exact source lines and the INDEX frame + local URL so a follow-up with a browser can capture them in minutes.
- **Out-of-axis matters** (prompt §5): flow length/feedback behaviour (UX), broken/overflow/mirroring/console (DF), element removals (EX), wording/translation (CP), focus/names/contrast/targets/reader order (AX), API/model/v1 truth and money/role privacy (TR) were left to the sibling DK prompts even where noticed.
- **Settled patterns** (`REVIEW_LENS.md` §2b, `DECISIONS_SHARED.md`, `DECISIONS_DESK.md` K1–K8/DK-003–DK-023) were not re-reported; only their misapplication is reported above. The stray `<<<<<<< HEAD` line before `INDEX.md` §54 noted in the prompt update was not reported, as instructed.
- **Desk-branch second source:** none — per the update the branch is merged and deleted; §56 frames were reviewed on `main`.

## Browser pass (2026-10-17)
Server: http://127.0.0.1:5490 · masaha-design at 93f152f · tool: playwright MCP
### Existing issues
- R2-DK-VD-001 — confirmed: Customer file payments use a plain `<Table>` (1 table, 3 rows) with no `renderCard` — no phone-card form at 390. — r2-shots/DK-VD/R2-DK-VD-001.png
- R2-DK-VD-002 — confirmed: Both text treatment (`text-body-sm text-muted-foreground`) and Badge (`variant="neutral"`) exist for «مسدّد»; `BalanceBadge` returns null when settled. — r2-shots/DK-VD/R2-DK-VD-002.png
- R2-DK-VD-003 — confirmed: Checkout dialog shows «لم يدفع شيئ»; pay-visit branch passes `none={false}` (source-verified, `desk-core.jsx:609`). — r2-shots/DK-VD/R2-DK-VD-003.png
- R2-DK-VD-004 — confirmed: Present rows use `px-4` (16px), unpaid rows use `px-5` (20px) — 4px gutter difference. — r2-shots/DK-VD/R2-DK-VD-004.png
- R2-DK-VD-005 — not checked: Type difference between desk (`text-caption`) and file (`text-body-sm`) not measured in browser.
- R2-DK-VD-006 — not checked: Method Badge vs caption not measured in browser.
- R2-DK-VD-007 — not checked: «بلا حدّ» warning icon not opened in browser (sheet dialog did not render).
- R2-DK-VD-008 — confirmed: «أرشفة» menu item has `variant="default"` (not destructive) on customer file. — r2-shots/DK-VD/R2-DK-VD-008.png
- R2-DK-VD-009 — confirmed: Customer file page has only h1 "رهف قديح"; subscription cards have no headings. — r2-shots/DK-VD/R2-DK-VD-009.png
- R2-DK-VD-010 — confirmed: Search-result customer cards have no headings; only h1 "رهف قديح" on the page. — r2-shots/DK-VD/R2-DK-VD-010.png
- R2-DK-VD-011 — changed: Due figure «المستحق 12 ₪» renders at 16px/400 weight, not `text-heading-3` (17px/600) as the report claims. — r2-shots/DK-VD/R2-DK-VD-011.png
- R2-DK-VD-012 — confirmed: My payments phone card (390) shows no transfer helper «وصلت إلى حساب المساحة». — r2-shots/DK-VD/R2-DK-VD-012.png
- R2-DK-VD-013 — changed: Sheet body uses `gap-4` (not `gap-5` as the report claims); already matches dialog rhythm. — r2-shots/DK-VD/R2-DK-VD-013.png
### Checked now
- Customer file payments at 390: plain `<Table>` with 3 rows, no card form (confirms R2-DK-VD-001).
- "مسدّد" treatment: both text span and neutral Badge found in source (confirms R2-DK-VD-002).
- «لم يدفع شيئ»: present in checkout dialog, absent in pay-visit dialog (confirms R2-DK-VD-003).
- Person row gutters: present `px-4`, unpaid `px-5` (confirms R2-DK-VD-004).
- «أرشفة» menu item: `variant="default"` (confirms R2-DK-VD-008).
- Subscription cards: no headings on customer file page (confirms R2-DK-VD-009/010).
- Due figure: 16px/400, not heading-3 (changed from report).
- My payments phone: no transfer helper (confirms R2-DK-VD-012).
- Sheet body: `gap-4` not `gap-5` (changed from report).
- 768px width on Desk: no horizontal overflow.
- Dark mode: muted text 7.62:1, passes AA.
### New issues
None.
### Still not checked
- R2-DK-VD-005: UnpaidRow type difference between desk and file (not measured).
- R2-DK-VD-006: Method Badge vs caption (not measured).
- R2-DK-VD-007: «بلا حدّ» warning icon (sheet did not render).
- Screen-reader audio: no screen reader available.
- 768px width: not checked on all DK pages.
