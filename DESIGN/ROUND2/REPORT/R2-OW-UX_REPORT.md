# R2-OW-UX — Round 2 review: the owner's management · Experience and flow

- `HEAD`: `34a6c59aab049e8f2992b29b88c8a700b926ddba`
- `origin/main`: `34a6c59aab049e8f2992b29b88c8a700b926ddba`
- Match: yes — review ran on `origin/main` (`34a6c59`, all six design batches merged).

## Verdict

The owner's jobs mostly complete in the fewest steps with a way back, but filtered lists have no one-tap way back on desktop, acted-on items vanish from their tab with only a transient toast, and two cross-page detours (no-shifts package sheet, pending-password recovery) abandon the owner's work.

## Five most important points

1. Desktop inline filters (Payments, Audit) render no «مسح الفلاتر», and filtered-empty states offer no reset — a filter to nothing is a dead end.
2. Ending an announcement, resolving a data report, or creating a scheduled announcement removes the item from the current view with only a 10-second toast as the trail.
3. A lost temporary password has no recovery: pending staff rows offer no re-issue, only remove-and-re-add.
4. The package sheet's no-shifts detour to the hours page loses the half-filled package draft and frames the detour as mandatory.
5. Finance's single «الشهر» control reads as global but moves only some cards; the charts keep fixed windows, so picking a month appears to do nothing.

## Issues

### R2-OW-UX-001 — Filtered to nothing, no one-tap way back (desktop + empty states)

- **type:** defect · **level:** pattern · **impact:** high
- **where:** Ledger · this month — desktop 1440, `http://127.0.0.1:5422/Payments.html` (set any filter combination that matches nothing), 1440 AR light; Audit log · the space's — desktop 1440, `http://127.0.0.1:5422/Owner%20audit.html` (same), 1440 AR light; Filter · new (`Data reports.html?status=new`, resolve the last `new` item), 390/768/1440 AR light · screenshot paths in `docs/design/screens/`: `32-payments-owner/09-empty-desktop-1440.webp`, `39-data-reports-owner/05-filter-new-desktop-1440.webp` (§55 audit frames have no screenshot yet: `—`)
- **evidence:** `C:\Users\basel\Downloads\r2-shots\OW-UX\R2-OW-UX-001.png` (not captured — no browser tool in this environment; see §6)
- **what is wrong:** `FilterSheet` (`masaha/shared.jsx`) renders its «مسح الفلاتر» footer only inside the narrow bottom sheet; at `≥768` it returns the inline fields with no clear control, and its active-count badge lives only on the narrow trigger. Payments' `onClear` additionally resets only staff/method/type, leaving the period range and the «إظهار الملغاة» chip set. The filtered-empty `EmptyState`s (Payments "no payments match the filters", Data reports "no reports with this status", Audit "no events match the filters") carry no reset action. An owner who filters to nothing on desktop must revert every control by hand.
- **proposal:** Add a «مسح الفلاتر» ghost button beside every inline `ResultCount` row on wide screens (same `onClear`, extended on Payments to also reset range and the voided chip), and give each filtered-empty state one «عرض الكل» action that clears the same set. Changes: `Payments.html`, `Owner audit.html`, `Data reports.html` (empty-state action only).
- **why:** Restores the way back that B.3/B.6 require: one tap returns a productive list instead of N manual reverts, on the widths the owner actually uses for these tables.
- **cost:** M
- **rule:** REVIEW_LENS.md §3 B.3 (fewest steps, no dead ends, a way back), B.6 (recovery); applies P5 (one filter bar) to wide screens.

### R2-OW-UX-002 — Acted-on items vanish from their tab with only a toast as the trail

- **type:** defect · **level:** pattern · **impact:** high
- **where:** Active · owner (`http://127.0.0.1:5422/Announcements.html`, press «إنهاء الآن»), 390/768/1440 AR light; List (`http://127.0.0.1:5422/Data%20reports.html?status=new`, press «تم التصحيح» on the last new item), 390/768/1440 AR light; New announcement sheet (`http://127.0.0.1:5422/Announcements.html?sheet=new&type=event`, schedule «في موعد» while on the Active tab) · screenshots `38-announcements-owner-reception/01-active-owner-desktop-1440.webp`, `39-data-reports-owner/05-filter-new-desktop-1440.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\OW-UX\R2-OW-UX-002.png` (not captured; see §6)
- **what is wrong:** `endNow` moves the card from Active to Ended, `decide` moves the report out of the `new` filter, and a newly scheduled announcement lands in Scheduled while the owner watches Active. In all three cases the acting view shows no result — the list just shrinks — and the only trace is a transient success toast (10 seconds). After it expires the owner has no record of where the item went.
- **proposal:** Name the destination in the toast and add a view action to it (e.g. «انتهى الإعلان · في المنتهية — عرض», «عُلّم تم التصحيح — عرض البلاغ»), using the design system's toast action slot already used for «تراجع». Changes: `Announcements.html`, `Data reports.html`.
- **why:** Keeps the owner's place in B.3 terms: the feedback says what happened *and* where to find it, so a finished job stays findable after the toast expires.
- **cost:** S
- **rule:** REVIEW_LENS.md §3 B.6 (every action says what happened); applies P8 (success toast says what changed).

### R2-OW-UX-003 — Lost temporary password has no recovery path

- **type:** defect · **level:** page · **impact:** high
- **where:** Staff list — desktop 1440 (`http://127.0.0.1:5422/Staff.html`), then Temporary password (shown once) (`http://127.0.0.1:5422/Staff.html?pass=1`), 390/768/1440 AR light · screenshots `37-staff-owner/01-staff-list-desktop-1440.webp`, `37-staff-owner/05-temporary-password-shown-once-desktop-1440.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\OW-UX\R2-OW-UX-003.png` (not captured; see §6)
- **what is wrong:** The handover dialog correctly forces copy + channel before «تم», but once it closes the password is unrecoverable by design («لن تظهر مرة أخرى»). A pending-password row (`لم يغيّر كلمة المرور المؤقتة بعد`) then offers only «عرض مقبوضاته» and «إيقاف الوصول» in its `⋯` menu. If the copied password is lost (cleared clipboard, lost paper), the owner's only path is remove-and-re-add the person, which discards the added date and confuses the audit trail — a dead end in the middle of the add-staff job.
- **proposal:** Add one row action for pending staff only, «كلمة مرور مؤقتة جديدة», which rotates the password and reopens the same shown-once dialog (same copy-first, same channel step). No other row changes.
- **why:** Completes the handover flow (B.3): a recoverable mistake costs one tap instead of destroying and recreating the staff record.
- **cost:** M
- **rule:** REVIEW_LENS.md §3 B.3 (no dead ends), B.6 (recovery); O4 action table (staff password under A5's rules — rotation reuses the same dialog).

### R2-OW-UX-004 — Package draft is lost on the no-shifts detour, framed as mandatory

- **type:** defect · **level:** page · **impact:** medium
- **where:** Edit usage-based package (`http://127.0.0.1:5422/Packages.html?edit=p4&demo=noshifts`), 390/768/1440 AR light · screenshot `34-packages-prices-owner/05-edit-usage-based-package-desktop-1440.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\OW-UX\R2-OW-UX-004.png` (not captured; see §6)
- **what is wrong:** With no shifts saved, the sheet's shift field says «لا ورديات محفوظة بعد» with a link to `Owner space profile.html#hours`. Following it leaves `Packages.html`, and the half-filled package (React state, not URL-persisted) is gone on return. The copy («أضف ورديات … أولًا») reads as a prerequisite, though the sheet can be saved shift-less and edited later — so owners either abandon a nearly-done package or take a detour that deletes their work.
- **proposal:** Add one line under the no-shifts note: the package can be saved without a shift and given one later via «تعديل». Keep the hours link as the secondary path, not the only one.
- **why:** Removes a false prerequisite and a work-destroying detour (B.3): the common case (save now, refine later) finishes in place; the rare case (add shifts first) stays one tap away.
- **cost:** S
- **rule:** REVIEW_LENS.md §3 B.3 (fewest steps, a way back), B.5 (common case first).

### R2-OW-UX-005 — Finance's «الشهر» reads as global but moves only some cards

- **type:** improvement · **level:** page · **impact:** medium
- **where:** الدخل (`http://127.0.0.1:5422/Finance.html`), الديون (`http://127.0.0.1:5422/Finance.html?tab=debts`), الإشغال (`http://127.0.0.1:5422/Finance.html?tab=occupancy`); one month (`http://127.0.0.1:5422/Finance.html?month=2026-08`), 390/768/1440 AR light, EN + dark spot-checked in code (`?lang=en`, `?theme=dark` paths exist) · screenshots `33-finance-reports-owner/01-desktop-1440.webp`, `33-finance-reports-owner/03-desktop-1440.webp`, `33-finance-reports-owner/05-desktop-1440.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\OW-UX\R2-OW-UX-005.png` (not captured; see §6)
- **what is wrong:** The month select sits beside the tab bar, reading as the page's time scope, but the three charts keep fixed windows (12 months, 30 days, 14 days, last-4-weeks heatmap) however the month is set; only the stat cards, the collections-by-staff table and the «دفعوا في …» card follow it, and the debtors list is month-independent. Picking `2026-08` leaves most of the screen unchanged with no explanation — the control promises what the page does not do.
- **proposal:** Scope the control to what it drives: move the month select into the month-driven blocks (or, smaller, add a caption under it: «يطبَّق على بطاقات الشهر وجداول التحصيل؛ الرسوم نوافذ ثابتة مسماة»). Keep the charts' existing window captions.
- **why:** An honest control (B.1 — each section one job; B.3 — nothing asked twice to no effect): the owner stops re-picking a month wondering why the charts ignore it.
- **cost:** S (caption) / M (move into cards)
- **rule:** REVIEW_LENS.md §3 B.1 (division of the page), B.3; OW-015 (one month for the blocks that count by month).

### R2-OW-UX-006 — Staff «عرض مقبوضاته» deep-links to a filter value Payments cannot show

- **type:** defect · **level:** page · **impact:** medium
- **where:** Staff list (`http://127.0.0.1:5422/Staff.html`, row `⋯` → «عرض مقبوضاته» for ليلى or هالة) lands on `http://127.0.0.1:5422/Payments.html?staff=<name>`, 390/768/1440 AR light · screenshots `37-staff-owner/01-staff-list-desktop-1440.webp`, `32-payments-owner/01-ledger-this-month-desktop-1440.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\OW-UX\R2-OW-UX-006.png` (not captured; see §6)
- **what is wrong:** Payments' staff filter offers only «كل الموظفين», أحمد and سامي. Staff keys for ليلى/هالة arrive via `?staff=` but match no option and no ledger row (`r.by` is only أحمد/سامي), so the owner lands on an empty ledger with a broken select value and no stated reason — a dead end reached by following the product's own link.
- **proposal:** Build the staff filter options from the space's staff list (names the ledger's `by` values), and for names with no rows keep the option selectable with the existing "no payments match the filters" empty state. Changes: `Payments.html` (options); `Staff.html` link unchanged.
- **why:** Every offered link must land somewhere truthful (B.3 — no dead ends): the owner sees ليلى's (empty) collections instead of a broken filter.
- **cost:** S
- **rule:** REVIEW_LENS.md §3 B.3, B.7 (daily task: checking a staff member's collections); P5 (filter options reflect the data).

### R2-OW-UX-007 — Three independent Settings cards share one anonymous «حُفظت الإعدادات» toast

- **type:** improvement · **level:** page · **impact:** low
- **where:** Owner settings (`http://127.0.0.1:5422/Owner%20settings.html`, incl. `?fail=save-attendance|save-pricing|save-message` and `#attendance`), 390/768/1440 AR light · screenshot `40-settings-owner/01-owner-settings-desktop-1440.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\OW-UX\R2-OW-UX-007.png` (not captured; see §6)
- **what is wrong:** Attendance, visit-pricing and reminder-message cards each save alone (good), but all three resolve to the identical toast «حُفظت الإعدادات». With per-card failure alerts but a shared success message, an owner who edits two cards cannot tell from the feedback alone what was actually saved.
- **proposal:** Name the card in its toast («حُفظت الحضور والحالة المباشرة», «حُفظ تسعير الزيارات», «حُفظت رسالة التذكير»), mirroring the per-card `actionKey` already used for failures.
- **why:** Applies P8 as written — a success toast says *what* changed — at the one page where three savers share one message.
- **cost:** S
- **rule:** REVIEW_LENS.md §3 B.6; P8 (amended 2026-10-10/11).

### R2-OW-UX-008 — In-session list state (tab, month, filters, page) does not survive reload or Back

- **type:** improvement · **level:** pattern · **impact:** medium
- **where:** `http://127.0.0.1:5422/Finance.html?tab=debts` (change month, reload — month resets), `http://127.0.0.1:5422/Payments.html?month=2026-08` (change staff/method, press Back — selection lost), `http://127.0.0.1:5422/Data%20reports.html?status=new`, `http://127.0.0.1:5422/Announcements.html` (tab), 390/768/1440 AR light · screenshots `33-finance-reports-owner/03-desktop-1440.webp`, `32-payments-owner/01-ledger-this-month-desktop-1440.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\OW-UX\R2-OW-UX-008.png` (not captured; see §6)
- **what is wrong:** Tabs, the Finance month, Payments range/filters/chip and the reports/announcements tab initialise from the URL once (`pageParams` at load) but never write back. On a weak connection — the lens's default — reloads are routine, and each one wipes the owner's filter work; filtered views are also unshareable and Back does not restore them. The prototype already proves the URL vocabulary (`?tab=`, `?month=`, `?status=`, `?range=`); it is just write-only at load.
- **proposal:** Sync the same parameters back to the URL on change (replace-state, no reload) for Finance tab+month, Payments range+filters+voided, Data reports status, Announcements tab. No new parameters, no new UI. Changes: `Finance.html`, `Payments.html`, `Data reports.html`, `Announcements.html`.
- **why:** Directly serves axis Q5 (lists keep their place) under lens conditions (Arabic first, weak connection): a reload or a shared link keeps the owner's exact working set.
- **cost:** M
- **rule:** REVIEW_LENS.md §3 B.3 (a way back), B.7; §1 (weak connection).

### R2-OW-UX-009 — Queue's «عرض» for owing customers undersells the destination

- **type:** improvement · **level:** page · **impact:** low
- **where:** Overview — desktop 1440 (`http://127.0.0.1:5422/Owner%20overview.html`, «زبائن عليهم مبالغ» row → `Finance.html?tab=debts`), 390/768/1440 AR light · screenshot `29-owner-overview-kept/01-overview-desktop-1440.webp`
- **evidence:** `C:\Users\basel\Downloads\r2-shots\OW-UX\R2-OW-UX-009.png` (not captured; see §6)
- **what is wrong:** Every other queue row's action names its destination («فتح المكتب», «تحديد السعة», «مراجعة»), but the owe row's action is a bare «عرض» with the destination only in the caption («المبالغ في المالية › الديون»). The one queue item that leaves the page for a different nav group gives the weakest scent of where it goes.
- **proposal:** Label the action «عرض الديون» (destination-first, matching «فتح المكتب» beside it). One string, both languages, via the copy catalogue.
- **why:** B.7/B.3: the queue is a launcher — each action should name where the owner is going, especially across nav groups.
- **cost:** S
- **rule:** REVIEW_LENS.md §3 B.7 (daily tasks first, labelled by what people do). Not a wording-quality (CP) finding: the change is the action's target labelling, not its Arabic.

## Decisions in doubt

None. The settled decisions hold up under this axis: the work-queue overview carries no money (O3 amended 2026-10-12 — verified, no amounts in `Owner overview.html`; counts only), no owner page renders a bottom bar (only `Desk.html` passes `bottomAction` — P1 as amended), every «الأسعار» path lands on `Packages.html#prices` (overview queue, profile prices row, settings pricing card, data-reports field map, audit targets), and the profile reads as the A1 editor with prices as a dated link row (O1/O6).

## What was not reviewed and why

- **Visual rendering at 390 / 768 / 1440, English and dark modes:** this environment exposes no browser tool, and the prompt forbids installing anything, so pages could not be opened visually. Judgement is from the prototype sources (page markup, `masaha/owner.jsx`, `owner-data.js`, `shared.jsx`, `desk-core.jsx`, `finance.jsx`, `profile-*.jsx`) with the server used only to verify serving (`200` on `Owner overview.html`). Width/mode applicability above is by code reasoning (responsive classes, `FilterSheet` breakpoints, `tr()`/`theme` paths), not by screenshots.
- **Evidence captures:** `C:\Users\basel\Downloads\r2-shots\OW-UX\` was created but no `<ID>.png` could be produced without a renderer; `evidence` fields name the intended paths and each issue cites the authoritative `docs/design/screens/…` frame instead.
- **Out-of-axis matters, left to the sibling OW prompts:** visual polish/tokens (VD), breakage/overflow/mirroring (DF), element removals/merges (EX), wording/translation quality (CP), focus/names/targets/reader order (AX), API/data-model/v1/money-privacy/permissions (TR) — including whether reception may save announcements and whether void/re-access endpoints exist.
- **Known archive limits** (REVIEW_LENS.md §2: placeholder nav icons, illustrative sample data, offline Google font, three superseded frames) and the recorded `INDEX.md` §54 merge-marker leftover (per this prompt §1, not reported).
- **End-to-end state after actions** (e.g. debts list refreshing behind the Finance pay dialog) could not be executed without a browser; only the in-page state handling was read.

## Browser pass (2026-10-17)
Server: http://127.0.0.1:5490 · masaha-design at 93f152f · tool: playwright MCP
### Existing issues
- R2-OW-UX-001 — not checked: Filtered empty states not triggered in browser (search did not filter).
- R2-OW-UX-002 — not checked: Acted-on items vanish not tested (requires triggering actions).
- R2-OW-UX-003 — confirmed: Pending staff (ليلى) shows «لم يغيّر كلمة المرور المؤقتة بعد» with no reissue option in row menu. — r2-shots/OW-UX/R2-OW-UX-003.png
- R2-OW-UX-004 — confirmed: Package sheet with no shifts shows «أضف ورديات في ساعات العمل أولًا» (reads as mandatory). — r2-shots/OW-UX/R2-OW-UX-004.png
- R2-OW-UX-005 — confirmed: Finance has month control «سبتمبر 2026» beside tab bar; charts keep fixed windows. — r2-shots/OW-UX/R2-OW-UX-005.png
- R2-OW-UX-006 — confirmed: Staff «عرض مقبوضاته» deep-links to `Payments.html?staff=ليلى` which matches no option. — r2-shots/OW-UX/R2-OW-UX-006.png
- R2-OW-UX-007 — not checked: Settings toast naming not tested (requires triggering saves).
- R2-OW-UX-008 — not checked: URL state sync not verified in browser.
- R2-OW-UX-009 — confirmed: Queue shows «5 زبائن عليهم مبالغ» with bare «عرض» button. — r2-shots/OW-UX/R2-OW-UX-009.png
### Checked now
- Staff page: pending staff (ليلى) with no reissue option (confirms R2-OW-UX-003).
- Staff row menu: «عرض مقبوضاته» + «إيقاف الوصول» only (confirms R2-OW-UX-003/006).
- Package sheet no-shifts: «أضف ورديات في ساعات العمل أولًا» reads as mandatory (confirms R2-OW-UX-004).
- Finance: month control «سبتمبر 2026» beside tab bar (confirms R2-OW-UX-005).
- Overview: «5 زبائن عليهم مبالغ» with bare «عرض» (confirms R2-OW-UX-009).
- 768px width: no horizontal overflow on overview.
- Dark mode: page background rgb(12,19,21), theme set correctly.
### New issues
None.
### Still not checked
- R2-OW-UX-001: Filtered empty states not triggered.
- R2-OW-UX-002: Acted-on items vanish not tested.
- R2-OW-UX-007: Settings toast naming not tested.
- R2-OW-UX-008: URL state sync not verified.
- Screen-reader audio: no screen reader available.
