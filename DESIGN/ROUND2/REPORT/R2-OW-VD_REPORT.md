# R2-OW-VD — Round 2 review: owner's management · visual design and consistency

1. Commits: `HEAD` = `origin/main` = `34a6c59aab049e8f2992b29b88c8a700b926ddba` (fetch-then-compare matched; no stop condition).

2. Verdict: visually consistent and token-disciplined, but the page title types smaller than section headings and status filtering is three different components for one job.

3. Five most important points:
   - The page `h1` renders at `heading-3`, the same size as every card title, flattening page hierarchy on all ten OW pages.
   - Status filtering is `Tabs`+`Badge` (Announcements), `ToggleGroup` chips (Data reports), and `Select`s in a sheet (Audit) for the same job.
   - Finance's three tabs carry no counts while Announcements' tabs do, against settled O5.
   - The Packages «الباقات الخاصة» `h2` (`heading-2`) outweighs its own page `h1` (`heading-3`).
   - Preview/quote boxes use three different surfaces for the same job across Packages, Settings, Announcements, and Data reports.

4. Issues (most important first):

## R2-OW-VD-001 — Page h1 is card-title size
- **type:** defect | **level:** pattern | **impact:** medium
- **where:** all OW frames; representative: Overview — desktop 1440, `Owner overview.html` on `http://127.0.0.1:5423/Owner%20overview.html` (served 200), AR light; board shot `docs/design/screens/29-owner-overview-kept/01-overview-desktop-1440.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\OW-VD\R2-OW-VD-001.png` — not captured (no browser/screenshot tooling in this review environment); verified in source: `docs/design/prototype/masaha/owner.jsx:320` (`<h1 … className="… text-heading-3">`) vs DS `CardTitle` (`_ds_bundle.js`: `cn("text-heading-3", …)`) and `SectionTitle` (`profile-a.jsx:30`).
- **wrong:** foundation §7 assigns page titles `heading-1` (30px / 24px phone); the shell's `h1` is `heading-3` (17px) — identical to every `CardTitle` and every editor section `h2`. The page title never leads the page typographically.
- **proposal:** render the `OwnerShell` `h1` at `text-heading-2`, keeping `truncate` and the bar layout; only `OwnerShell` changes, so only the ten OW pages change.
- **why:** restores title > section > card order with one class, within the phone bar's truncation rule (DI-10).
- **cost:** S | **rule:** foundation §7 (Typography).

## R2-OW-VD-002 — One status-filter job, three components
- **type:** improvement | **level:** pattern | **impact:** medium
- **where:** Announcements active/scheduled/ended (`Announcements.html`, `http://127.0.0.1:5423/Announcements.html`, 1440, AR light; `docs/design/screens/38-announcements-owner-reception/01-active-owner-desktop-1440.webp`) vs Data reports all/new/fixed/rejected (`Data reports.html`, `http://127.0.0.1:5423/Data%20reports.html`, same width/mode; `docs/design/screens/39-data-reports-owner/01-list-desktop-1440.webp`) vs Audit action-type `Select` in the sheet (`Owner audit.html`, `http://127.0.0.1:5423/Owner%20audit.html`; no board shot for the sheet state).
- **evidence:** `C:\Users\basel\Downloads\r2-shots\OW-VD\R2-OW-VD-002.png` — not captured (same reason); source: `Announcements.html:198-204` (`Tabs` + `Badge` counts) vs `Data reports.html:95-98` (`ToggleGroup` chips, no counts) vs `Owner audit.html:80-87` (`Select` in `FilterSheet`).
- **wrong:** partitioning one list by status is `Tabs` with `Badge` counts on Announcements, chipless `ToggleGroup` chips with a separate `ResultCount` on Data reports, and a dropdown inside the filter sheet on Audit. Same job, three looks; only Announcements shows counts at the choice point.
- **proposal:** use Announcements' pattern — `Tabs` with `Badge` counts — on Data reports (4 statuses fit); keep sheet `Select`s only where filters are multi-dimensional (Payments, Audit period/actor). Changes Announcements (no-op) and Data reports.
- **why:** one learned control for "slice this list"; counts move from below the toolbar to the choice itself (O5).
- **cost:** M | **rule:** applies P5 (filter bar) and O5 (counts in tabs as `Badge`s).

## R2-OW-VD-003 — Finance tabs have no counts
- **type:** defect | **level:** page (Finance) | **impact:** low
- **where:** Finance الدخل/الديون/الإشغال, `Finance.html`, `http://127.0.0.1:5423/Finance.html`, 1440, AR light; `docs/design/screens/33-finance-reports-owner/01-desktop-1440.webp` (also `?tab=debts`, `http://127.0.0.1:5423/Finance.html?tab=debts`).
- **evidence:** `C:\Users\basel\Downloads\r2-shots\OW-VD\R2-OW-VD-003.png` — not captured (same reason); source: `Finance.html:163-169` (`TabsTrigger`s with bare labels) vs `Announcements.html:200-202` (each trigger carries `<Badge><Num>{count}</Num></Badge>`).
- **wrong:** O5 settles counts in tabs as `Badge`s and Announcements applies it; Finance's tabs — at minimum «الديون» (debtor count, already computed for the cards at `Finance.html:82-83`) — show none.
- **proposal:** add a `Badge` count to the «الديون» tab (debtors); leave الدخل/الإشغال uncounted (not list partitions) or count their cards if the owner wants symmetry.
- **why:** the debts count is the triage signal; Announcements proves the pattern.
- **cost:** S | **rule:** O5 (counts in tabs as `Badge`s).

## R2-OW-VD-004 — Packages section h2 outweighs the page h1
- **type:** defect | **level:** page (Packages) | **impact:** low
- **where:** Packages & prices — desktop 1440, `Packages.html`, `http://127.0.0.1:5423/Packages.html`, AR light; `docs/design/screens/34-packages-prices-owner/01-packages-prices-desktop-1440.webp`.
- **evidence:** `C:\Users\basel\Downloads\r2-shots\OW-VD\R2-OW-VD-004.png` — not captured (same reason); source: `Packages.html:151` (`<h2 … className="text-heading-2">`, 22px) vs page `h1` at `text-heading-3` (17px, R2-OW-VD-001).
- **wrong:** «الباقات الخاصة» is the only section heading in OW set above card-title size, so it outranks its own page title; every editor `h2` (`SectionTitle`) sits at card-title size.
- **proposal:** set the heading at card-title scale (reuse `SectionTitle`) unless R2-OW-VD-001 lands first, in which case keep `heading-2` under a larger `h1`.
- **why:** one section-heading rank across the editor and Packages; no new component, one class.
- **cost:** S | **rule:** foundation §7.

## R2-OW-VD-005 — Preview/quote boxes use three surfaces
- **type:** improvement | **level:** pattern | **impact:** low
- **where:** New package sheet summary (`Packages.html?sheet=new`, `http://127.0.0.1:5423/Packages.html?sheet=new`, 390; `docs/design/screens/34-packages-prices-owner/04-new-package-sheet-live-summary-phone-390.webp`) vs Reminder-message preview (`Owner settings.html`, `http://127.0.0.1:5423/Owner%20settings.html`; `docs/design/screens/40-settings-owner/01-owner-settings-desktop-1440.webp`) vs Announcement sheet preview (`Announcements.html?sheet=new&type=closure`, `http://127.0.0.1:5423/Announcements.html?sheet=new&type=closure`; `docs/design/screens/38-announcements-owner-reception/11-new-announcement-sheet-desktop-1440.webp`) vs Report sheet boxes (`Data reports.html?open=d1`, `http://127.0.0.1:5423/Data%20reports.html?open=d1`; `docs/design/screens/39-data-reports-owner/03-open-report-desktop-1440.webp`).
- **evidence:** `C:\Users\basel\Downloads\r2-shots\OW-VD\R2-OW-VD-005.png` — not captured (same reason); source: `Packages.html:124` (`rounded-lg bg-muted p-4`) vs `Owner settings.html:112` (`rounded-lg bg-muted p-3`) vs `Announcements.html:86` (`rounded-lg border … bg-background p-4`) vs `Data reports.html:57-58` (bordered `p-3` beside muted `p-3`).
- **wrong:** the same job — "read-only quoted/computed content inside a form" — is muted `p-4`, muted `p-3`, bordered `p-4`, and a bordered+muted pair side by side. Changes Packages, Settings, Announcements, Data reports if unified.
- **proposal:** one treatment for quoted/computed boxes: `rounded-lg bg-muted p-3` (the majority), keeping the report sheet's two boxes on the same surface with their caption labels (`البلاغ` / `القيمة الحالية`) carrying the distinction. No new component.
- **why:** equal content stops competing on surface; captions already name the roles.
- **cost:** S | **rule:** foundation §5 (semantic roles — one role, one surface).

## R2-OW-VD-006 — Missing-checklist rows are denser than every sibling row
- **type:** improvement | **level:** pattern (shared editor component; also reaches the admin editor) | **impact:** low
- **where:** Space profile — desktop 1440, `Owner space profile.html?demo=missing`, `http://127.0.0.1:5423/Owner%20space%20profile.html?demo=missing`, AR light; `docs/design/screens/30-owner-space-profile-kept/01-space-profile-desktop-1440.webp`.
- **evidence:** `C:\Users\basel\Downloads\r2-shots\OW-VD\R2-OW-VD-006.png` — not captured (same reason); source: `profile-a.jsx:218` (`py-2`, no inline padding) vs queue rows (`Owner overview.html:59`), debts rows (`Finance.html:99`), package rows (`Packages.html:161`) — all `px-5 py-3` with `divide-y`.
- **wrong:** the checklist is the same row job (label + status badge + target) at `py-2` while every sibling list row is `px-5 py-3`; both on the spacing scale, but two densities for one pattern.
- **proposal:** set checklist rows to `px-5 py-3` to match queue/debts/package rows. Per the 2026-10-13 owner note, a shared-editor defect is recorded, not built, while worker A builds the admin editor.
- **why:** checklist lines scan like the queue they feed.
- **cost:** S | **rule:** foundation §5 (spacing scale, applied consistently).

## R2-OW-VD-007 — Linked stat tile looks exactly like static stats
- **type:** improvement | **level:** pattern (Overview + Finance) | **impact:** low
- **where:** Overview «إعلانات نشطة» tile, `Owner overview.html`, `http://127.0.0.1:5423/Owner%20overview.html`, 1440, AR light (`docs/design/screens/29-owner-overview-kept/01-overview-desktop-1440.webp`) vs Finance static `StatCard`s, `Finance.html` (same server/mode; `docs/design/screens/33-finance-reports-owner/01-desktop-1440.webp`).
- **evidence:** `C:\Users\basel\Downloads\r2-shots\OW-VD\R2-OW-VD-007.png` — not captured (same reason); source: `Owner overview.html:72` (`LinkTile`: bare `<a>` wrapping `StatCard`, focus style only, no hover treatment) vs `Finance.html:53-55,91-93` (identical `StatCard`s, not links).
- **wrong:** the same component does two jobs — navigation vs display — with zero visual distinction; nothing says the overview tile is a link until focused.
- **proposal:** give the linked tile an affordance from existing tokens (e.g. hover `bg-accent` transition on the card, or a trailing end-chevron in `muted-foreground`); no new component — `StatCard` gains no variant, the wrapper carries it.
- **why:** interactive and static numbers stop masquerading as each other; keeps the one-tile-links exception (O3) discoverable.
- **cost:** S | **rule:** lens §3 B.4 (same job the same way; here: different jobs must read differently).

5. Decisions in doubt: none.

6. What was not reviewed and why:
- Pixel rendering at 390 / 768 / 1440, dark theme, and EN LTR: no browser or screenshot tooling exists in this review environment, so no `<ID>.png` captures were taken (the shots folder holds none); widths/modes/languages were reviewed in source (responsive classes, `tr()` strings, semantic tokens) and every key state URL served 200 on port 5423 (21 URLs checked, incl. `?demo=clear`, `?sheet=new`, `?edit=p4&demo=noshifts`, `?tab=ended&extend=a6`, `?pass=1`, `?void=1`, `?voided=1`, `?month=2026-08`, `?report=d1`, `?fail=save-attendance`, `?role=reception…`, `?lang=en&theme=dark`).
- Anything out of the VD axis per the prompt (§5: UX flow/feedback, DF breakage/overflow/mirroring/console, EX removals, CP wording, AX focus/names/contrast/targets/order, TR truth/permissions) — left to the sibling OW prompts.
- Settled patterns (P1–P10, SH-*, O1–O13, OW-014–OW-021, DI-10/DI-36, AD-008/K4/P9 colour applications) were checked for consistent application only; verified consistent: queue-first overview with no amounts (O3), one `h1` per page, AD-008 table with date+confirm on Packages (O6), package live summary (O8), per-card Settings saves, voided struck with who/why (K4), destructive red only on void/staff-removal/extension (O4/P9), «عرض الكل» carrying the month (DI-36).
- The stray `<<<<<<< HEAD` line before INDEX §54, flagged in the prompt header, was not reported per instruction.
- Server on port 5423 was stopped after the review and the port verified free.

## Browser pass (2026-10-17)
Server: http://127.0.0.1:5490 · masaha-design at 93f152f · tool: playwright MCP
### Existing issues
- R2-OW-VD-001 — confirmed: h1 uses `text-heading-3` (17px, 600 weight) on Owner overview. — r2-shots/OW-VD/R2-OW-VD-001.png
- R2-OW-VD-002 — confirmed: Announcements uses Tabs with counts («نشطة2», «مجدولة1», «منتهية3»); Data reports uses ToggleGroup with 4 chips (الكل, جديد, تم التصحيح, لم يُعتمد); different components for the same job. — r2-shots/OW-VD/R2-OW-VD-002.png
- R2-OW-VD-003 — confirmed: Finance tabs (الدخل, الديون, الإشغال) have no Badge counts. — r2-shots/OW-VD/R2-OW-VD-003.png
- R2-OW-VD-004 — confirmed: Packages h2 «الباقات الخاصة» is 22px (heading-2), h1 is 17px (heading-3) — h2 outweighs h1. — r2-shots/OW-VD/R2-OW-VD-004.png
- R2-OW-VD-005 — confirmed: Package sheet preview box uses `rounded-lg bg-muted p-4`; Settings uses `p-3` for similar preview. — r2-shots/OW-VD/R2-OW-VD-005.png
- R2-OW-VD-006 — confirmed: Checklist rows use `py-2` (8px) while sibling queue/debts/package rows use `py-3` (12px). — r2-shots/OW-VD/R2-OW-VD-006.png
- R2-OW-VD-007 — not checked: Linked stat tile («إعلانات نشطة») not found as a distinct link element in the rendered page.
### Checked now
- h1 styling: `text-heading-3` at 17px/600 (confirms R2-OW-VD-001).
- Packages h1/h2: h1 17px, «الباقات الخاصة» h2 22px (confirms R2-OW-VD-004).
- Announcements: 3 tabs with counts in text; Data reports: 4 chips in ToggleGroup (confirms R2-OW-VD-002).
- Finance: 3 tabs, no Badge counts (confirms R2-OW-VD-003).
- Preview boxes: package sheet `p-4`, settings `p-3` (confirms R2-OW-VD-005).
- Checklist rows: `py-2` vs sibling rows `py-3` (confirms R2-OW-VD-006).
- 768px width: no horizontal overflow on overview.
- Dark mode: muted text passes AA.
### New issues
None.
### Still not checked
- R2-OW-VD-007: Linked stat tile not found as a distinct element in the rendered page.
- Dark mode: not fully checked for all OW pages.
- 768px width: not checked on all OW pages.
- English/LTR: not checked for OW pages.
