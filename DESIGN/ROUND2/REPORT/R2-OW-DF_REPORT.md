# R2-OW-DF — The owner's management · Design defects

## 1. Commits

- `HEAD` (worktree `C:\dev\masaha\app-design`): `18ab1705149773bd05f2f7349ef341e33d175ca3`
- `origin/main` (after `git fetch origin`): `eff0a3d1e332a0161fde267a9a100f889184f550`
- They differ; `git diff --quiet HEAD origin/main -- docs/design` exits 0: **design unchanged**, review continued on `HEAD`.

## 2. Verdict

No console errors and no blank frames in 1,536 loads (10 pages × 64 states × 390/768/1440 × ar/en × light/dark). But the owner's pages still break at 768 (a Finance card, the Staff table, the top bar) and on the phone's announcement sheet, and several failure and loading states either spread beyond the action that failed or contradict themselves.

## 3. The five most important points

1. At 390 the announcement sheet's date and time row is 29 px wider than the sheet, so the body scrolls sideways and the fields are cut off (R2-OW-DF-001).
2. At 768 the Staff table pushes its row actions out of view behind a horizontal scroll, and its dates wrap onto three lines (R2-OW-DF-002).
3. If extending a closure's subscriptions fails, the confirmation closes and only a toast is left. P8 says a failure stays inside its dialog (R2-OW-DF-003).
4. `?fail=save` lights up failures that did not happen: on all four profile groups at once, and on the published prices card behind the package sheet (R2-OW-DF-004, -005).
5. At 768 the Finance peak-hour figure is clipped at its card's edge, and the top bar cuts the page title down («المالية و…», "Pay…") or wraps onto two rows (R2-OW-DF-006, -007).

## 4. Issues

Server: `http://127.0.0.1:5424/`. Captures: `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\OW-DF\`. Every measured value below was read with in-page JavaScript on the rendered page, in a local headless Chrome.

### R2-OW-DF-001 — The announcement sheet scrolls sideways on the phone; date and time fields are cut
- **type:** defect · **level:** component · **impact:** high
- **where:** "New announcement · the model's fields — phone 390" and "Scheduled closure · edit (owner) — phone 390" (§38, §55); `Announcements.html?lang=en&tab=scheduled&edit=a1` and `?sheet=new&type=closure`, at 390, in ar and en, light and dark; screenshot `screens/38-announcements-owner-reception/06-scheduled-closure-extend-owner-phone-390.webp` (§55's frame has none yet)
- **evidence:** `R2-OW-DF-001.png`
- **what is wrong:** The sheet is 293 px wide on a 390 px screen. Its scrolling body measures `scrollWidth 321 > clientWidth 292`. The start and end Date/Time fields overflow it: the date button spans x 99→404 and the time field 112→391, both past the sheet's right edge at 390. The body scrolls sideways, the start padding is lost, and the field edges are cut off. The overflow is the same in ar and en.
- **proposal:** Inside the sheet, stack Date over Time below `sm`, and give the sheet body `min-w-0`, so that no row can be wider than the sheet. The settled OW-010 fix (`Sheet side="end"` full width below `md`) does not appear in the archive's bundle yet; when it lands, recheck this sheet together with the package and staff sheets, which are also 293 px wide today.
- **why:** The period is what a closure is about. On a phone the owner has to see both dates whole, without scrolling sideways.
- **cost:** S
- **rule:** DECISIONS_OWNER OW-010; foundation §9

### R2-OW-DF-002 — The Staff table hides its row actions at 768
- **type:** defect · **level:** page · **impact:** high
- **where:** "Staff list" / "Staff · real columns, a pending password" (§37, §55); `Staff.html?lang=en` at 768, light and dark; screenshot `screens/37-staff-owner/01-staff-list-desktop-1440.webp` (no 768 frame)
- **evidence:** `R2-OW-DF-002.png`
- **what is wrong:** The table box is 638 px wide, but `scrollWidth` is 685. The «Actions» column header sits at x 710→782, past the box's right edge at 735, so each row's «⋯» (reissue the password, stop access) can only be reached by scrolling sideways. The «Added» column is 59 px wide, so "2 Mar 2026" and "28 Sept 2026" break onto three lines. Arabic fits (scrollWidth 638 = clientWidth 638); English does not.
- **proposal:** Below `lg`, use the phone's card form, as Payments does (SH-007). If the table stays, merge «Added» under the name as a caption, keep the actions column pinned, and make the dates `nowrap`.
- **why:** Stopping a staff member's access is the action an owner comes to this page for. It cannot sit off-screen.
- **cost:** S
- **rule:** DECISIONS_SHARED SH-007; foundation §9

### R2-OW-DF-003 — A failed closure extension closes its dialog and leaves only a toast
- **type:** defect · **level:** page · **impact:** high
- **where:** "Closure extension · the confirmation" (§55); `Announcements.html?tab=ended&extend=a6&fail=extend`, then a real click on «مدّد 40 اشتراكًا», at 390 (same at 1440)
- **evidence:** `R2-OW-DF-003.png`
- **what is wrong:** Read after the click: `dialogs: []` and `toasts: ["تعذّر إتمام العملية | إعادة المحاولة"]`. The `AlertDialog` closes, and the days the owner typed (2) and the count it named (40 subscriptions) are gone. Only a page toast is left, under the ended list. Every other dialog or sheet failure on these pages stays inside it: the package sheet, the staff sheet, the announcement sheet and the void dialog.
- **proposal:** Keep the dialog open on failure, with `ActionAlert for="extend"` above its footer, as the void dialog does.
- **why:** The extension moves 40 customers' end dates. The owner needs to know nothing moved, and to retry with the same number, without starting over.
- **cost:** S
- **rule:** DECISIONS_SHARED P8 ("a failure inside its dialog or sheet, which stays open and keeps the input"); DECISIONS_OWNER O11

### R2-OW-DF-004 — `?fail=save` on the space profile fails all four groups at once
- **type:** defect · **level:** page · **impact:** medium
- **where:** "Space profile · the editor, prices as a row" (§55); `Owner space profile.html?fail=save` at 1440 (also 390 and 768, ar/en, light/dark); screenshot `screens/30-owner-space-profile-kept/01-space-profile-desktop-1440.webp`
- **evidence:** `R2-OW-DF-004.png` (the whole page, at 0.4 scale)
- **what is wrong:** On load, four destructive alerts «تعذّر إتمام العملية» show at once, one in each of «المساحة», «ساعات العمل», «المرافق» and «التواصل» (page y 221, 1502, 3123, 3826). This is before any save. After a real click on one group's «حفظ», a page toast «تعذّر إتمام العملية | إعادة المحاولة» joins them. The owner's settings page shows what this state should look like: each card has its own key (`save-attendance`, `save-pricing`, `save-message`), and only that card fails.
- **proposal:** Give each group its own failure key (`save-profile`, `save-hours`, `save-amenities`, `save-contacts`), as Owner settings does. Show the alert only in the group whose save failed, and only after that save. Do not add a toast on top of the inline alert. The editor is shared with the admin's (S2b-4 freeze), so the owner's page sets its own keys and the shared editor is only recorded.
- **why:** A section-by-section editor must say which section did not save. Four red alerts tell the owner that everything failed.
- **cost:** S
- **rule:** DECISIONS_SHARED P8; DECISIONS_OWNER (2026-10-13 note on the shared editor)

### R2-OW-DF-005 — The package sheet's failure also shows on the published prices card behind it
- **type:** defect · **level:** page · **impact:** medium
- **where:** "New package · limits on demand" (§55); `Packages.html?sheet=new&fail=save` at 1440, ar (also 390, en, dark); screenshot `screens/34-packages-prices-owner/03-new-package-sheet-live-summary-desktop-1440.webp`
- **evidence:** `R2-OW-DF-005.png`
- **what is wrong:** Read alerts: `«تعذّر إتمام العملية» @ «الأسعار المعلنة»` and `@ «باقة جديدة»`. The published prices card shows a save failure, though nobody saved it, under the sheet that did fail. `Packages.html?fail=save` without the sheet shows the same alert on the prices card alone, so one key stands for two different actions.
- **proposal:** Split the keys: `save-prices` for the published prices table and `save-package` for the sheet. Each alert then shows only where its action ran.
- **why:** After a failed package save, the owner should not also be told that the public prices failed and start re-checking them.
- **cost:** S
- **rule:** DECISIONS_SHARED P8; DECISIONS_OWNER O6, O8

### R2-OW-DF-006 — Finance › Occupancy: at 768 the peak-hour figure is clipped by its card
- **type:** defect · **level:** page · **impact:** medium
- **where:** "Finance · الإشغال" (§33/§35); `Finance.html?tab=occupancy` at 768, ar and en, light and dark (also `&month=2026-08`); screenshot `screens/33-finance-reports-owner/05-desktop-1440.webp` (no 768 frame)
- **evidence:** `R2-OW-DF-006.png`
- **what is wrong:** «ساعة الذروة» "11:00–13:00" is 180 px wide in a card 197 px wide with `overflow: hidden`. In ar the value runs from x 242 while the card starts at 246, so the first "1" is cut. In en the value ends at 511 while the card ends at 507. The value fills the card's padding on both sides. The card's caption «الأحد والاثنين الأعلى · سبتمبر 2026» also overflows its box.
- **proposal:** Below `lg`, lay out the three summary cards in one column, as on the phone, or set the value one type step smaller (`text-heading-2`) in the three-up row. The range stays `nowrap`.
- **why:** The peak hour is this tab's answer; it has to read whole.
- **cost:** S
- **rule:** foundation §9; lens §2c (768)

### R2-OW-DF-007 — At 768 the top bar cuts the page title or wraps onto two rows when a page has a secondary action
- **type:** defect · **level:** pattern · **impact:** medium
- **where:** shell top bar (P1). `Payments.html?lang=en` and `Finance.html` (ar) at 768: title truncated. `Finance.html?lang=en` at 768: the bar wraps. Every theme; screenshots `screens/32-payments-owner/01-ledger-this-month-desktop-1440.webp`, `screens/33-finance-reports-owner/01-desktop-1440.webp` (no 768 frames)
- **evidence:** `R2-OW-DF-007.png` (Payments, en), `R2-OW-DF-007b.png` (Finance, en)
- **what is wrong:** The h1 measures: Payments en `scrollWidth 78 > clientWidth 56`, shown as "Pay…". Finance ar `99 > 79`, shown as «المالية و…». Finance en does not truncate, but the header grows to 97 px with the language, theme and account pushed onto a second row; on every other page the header is 57 px. All three pages carry a secondary action («تصدير CSV», «تصدير الدخل (CSV)»). The pages without one fit on one row at 768.
- **proposal:** From `md` to `lg`, move the secondary action into P1's «⋯» `DropdownMenu`, as the phone does. The bar then keeps the title, P2's control, the language, the theme and the account on one row. This applies to Payments, Finance and any page with a secondary action in the bar.
- **why:** The h1 is how the owner knows where they are. Truncating it to "Pay…" or doubling the bar's height breaks the one-page-header pattern at the width where it matters most.
- **cost:** S
- **rule:** DECISIONS_SHARED P1, DI-10 note in DECISIONS_OWNER; foundation §9

### R2-OW-DF-008 — Payments opened from Finance's «عرض الكل» does not show its month on the phone
- **type:** defect · **level:** page · **impact:** medium
- **where:** `Payments.html?month=2026-08` (the link Finance › الديون › «دفعوا في أغسطس 2026» › «عرض الكل» opens, read as `Payments.html?month=2026-08`) at 390, ar and en, light and dark; screenshot `screens/32-payments-owner/02-ledger-this-month-phone-390.webp`
- **evidence:** `R2-OW-DF-008.png`
- **what is wrong:** At 390 the range picker is inside the collapsed filter sheet (`rangePickerVisible: false`). The trigger reads «الفلاتر» with no active-count badge, because the count only includes staff, method and type. The totals line «المجموع 3740 ₪ · نقدًا 2255 ₪ · تحويل 1485 ₪ · 33 دفعة» names no period. The month only shows indirectly, in each row's date («31 أغسطس», with no year). At 768 the same URL shows «1 أغسطس – 31 أغسطس 2026» in the open filter bar.
- **proposal:** Count a range other than the default as an active filter on the «الفلاتر» trigger, and put the period at the start of the totals line («أغسطس 2026 · المجموع 3740 ₪»). These are P5's own badge and P5's result-count line, so no new component is needed.
- **why:** The owner jumped here to see one month's payments. Without the month on screen, the totals read like this month's.
- **cost:** S
- **rule:** DECISIONS_SHARED P5 (active-count badge); INDEX `Payments.html?month=` (DI-36)

### R2-OW-DF-009 — While the list loads, its totals and counts are already shown
- **type:** defect · **level:** pattern · **impact:** medium
- **where:** `Payments.html?state=loading` at 390 (and every width and mode); the same on `Staff.html`, `Data reports.html` and `Owner audit.html` with `?state=loading`; screenshot `screens/32-payments-owner/12-loading-phone-390.webp`
- **evidence:** `R2-OW-DF-009.png`
- **what is wrong:** The rows are skeletons (10 skeleton blocks at 390), but the page shows «المجموع 11783 ₪ · نقدًا 6500 ₪ · تحويل 5283 ₪ · 277 دفعة» and «صفحة 1 من 14». The other lists do the same: «عدد الموظفين: 3», «عدد البلاغات: 4», «الأحداث: 64». The frame is drawn in a state it cannot be in: the totals come from the same response as the rows.
- **proposal:** While `loading`, render the result count and the totals as `Skeleton` text lines, and hide the pagination summary. Do this once in the list toolbar, so it applies to Payments, Staff, Data reports and the owner's audit log.
- **why:** A money total shown before the data has arrived can be read as real, at the desk or in a report.
- **cost:** S
- **rule:** DECISIONS_SHARED P7

### R2-OW-DF-010 — Announcements and Packages have no loading state
- **type:** defect · **level:** page · **impact:** medium
- **where:** `Announcements.html?state=loading` and `Packages.html?state=loading` at every width and mode; screenshots `screens/38-announcements-owner-reception/02-active-owner-phone-390.webp`, `screens/34-packages-prices-owner/02-packages-prices-phone-390.webp`
- **evidence:** `R2-OW-DF-010.png` (Announcements, 390, ar)
- **what is wrong:** Read: `skeletons: 0` on both pages. They render their full data (two active announcements; the five-row prices table and the private packages) as if loaded. Payments, Staff, Data reports and the audit log draw 25 skeleton blocks at 1440 for the same parameter. INDEX lists `?state=loading` for "every list page"; both pages are lists (O6 makes the private packages "a list of rows").
- **proposal:** Announcements: three `Skeleton` cards in place of the list, with the tab counts as skeletons. Packages: skeleton rows in the prices table and in the private packages list, the same shape `DataTable loading` uses.
- **why:** On a weak connection, the owner should see that the list is still coming, not an empty or stale page.
- **cost:** S
- **rule:** DECISIONS_SHARED P7; INDEX › URL parameters (`?state=loading`)

### R2-OW-DF-011 — The public-state popover opens with «ممتلئ» checked while the space shows «متاح»
- **type:** defect · **level:** component · **impact:** medium
- **where:** `Owner overview.html?publicstate=open` at 390 (ar), and on every owner page with `?publicstate=open` (Finance at 1440 checked too), in ar and en; screenshot `screens/29-owner-overview-kept/02-overview-phone-390.webp`
- **evidence:** `R2-OW-DF-011.png`
- **what is wrong:** Read: `trigger: "متاح"` (en "Visitors see: Available"), `popoverSelected: ["ممتلئ"]` (en "Full"), and no duration chosen. The popover's choice contradicts the state its trigger reports. The control is drawn in a state it cannot be in: «ممتلئ» is checked, but nothing has been applied and there is no button to apply it.
- **proposal:** Open the popover with the current state checked («متاح»). Picking «ممتلئ» or «مغلق الآن» then reveals «لمدة». If the board needs the override flow, show it as its own frame (`?publicstate=open&pick=full`).
- **why:** The owner opens this control to see and change what visitors see. A checked «ممتلئ» on an available space misreports it.
- **cost:** S
- **rule:** DECISIONS_SHARED P2

### R2-OW-DF-012 — The delete confirmation opens over the wrong tab and does not name the announcement
- **type:** defect · **level:** page · **impact:** medium
- **where:** `Announcements.html?delete=a1` (INDEX: "deleting a scheduled announcement") at 390, ar (all widths and modes)
- **evidence:** `R2-OW-DF-012.png`
- **what is wrong:** Read: `selectedTab: "نشطة 2"`. Visible cards: the active event and the active offer. Dialog text: «حذف الإعلان؟ — يُحذف قبل أن يظهر للزوار، ولا يمكن استرجاعه.» a1 is the scheduled closure (1–3 Oct), which is only on «مجدولة». The dialog sits over two announcements that visitors already see. It names neither the announcement nor its dates, and its body ("before visitors see it") is false for anything visible behind it.
- **proposal:** Open the confirmation on the tab of the announcement it deletes (`?delete=` sets the tab), and name it in the title: «حذف إعلان «إغلاق مؤقت · 1–3 أكتوبر»؟».
- **why:** A delete that cannot be undone must leave no doubt about what is deleted.
- **cost:** S
- **rule:** DECISIONS_SHARED P9 ("body saying the true consequence"); DECISIONS_OWNER O10

### R2-OW-DF-013 — The announcement sheet cuts the end date at 1440 in English
- **type:** defect · **level:** page · **impact:** low
- **where:** "New announcement sheet" (§38); `Announcements.html?lang=en&sheet=new&type=event` at 1440, light and dark; screenshot `screens/38-announcements-owner-reception/11-new-announcement-sheet-desktop-1440.webp`
- **evidence:** `R2-OW-DF-013.png`
- **what is wrong:** The «Ends» date button is 162 px wide. Its text "29 September 2026" needs 136 px but gets 112 (`text-overflow: ellipsis`), so it shows as "29 September …" and the year is lost. The Time field beside it has room to spare.
- **proposal:** Give the date the wider share of the row (`grid-cols-[3fr_2fr]`), or use the short month ("29 Sept 2026"), as the announcement cards already do.
- **why:** The end date decides when the public notice disappears. The owner should read it whole before publishing.
- **cost:** S
- **rule:** foundation §9

### R2-OW-DF-014 — At 1440 «إعلان جديد» sits 232 px outside the list it adds to
- **type:** defect · **level:** page · **impact:** low
- **where:** "Announcements · end now, no end, quiet types — desktop 1440" (§55); `Announcements.html` at 1440, ar and en, light and dark; screenshot `screens/38-announcements-owner-reception/01-active-owner-desktop-1440.webp`
- **evidence:** `R2-OW-DF-014.png`
- **what is wrong:** In ar the list column spans x 264→1160 (max-width), but «إعلان جديد» sits at x 32→126, at the far end of `main` (0→1192). In en the list spans 280→1176 and the button 1246→1408. The add action is in the tabs' row, but off the list's column. At 768 the list fills `main` and the button lines up with its end (32 = 32).
- **proposal:** Put the tabs and the button in a row with the list's own max-width, so the button ends where the cards end. This is P1's amended "add in a row above the list, at its end".
- **why:** The add belongs to the list. At 1440 it reads as a page action floating in empty space.
- **cost:** S
- **rule:** DECISIONS_SHARED P1 (amended 2026-10-10); lens A.1

### R2-OW-DF-015 — The phone drawer slices the last group's heading under its fixed foot
- **type:** defect · **level:** component · **impact:** low
- **where:** "Phone bar · the account heads the drawer — phone 390" (§55); `Owner overview.html?drawer=open` at 390×844, ar and en, light and dark (the same shell on every owner page)
- **evidence:** `R2-OW-DF-015.png`
- **what is wrong:** The drawer's scrolling nav ends at y 732 (`clientHeight 571 < scrollHeight 729`). The heading «الفريق والإعدادات» spans y 719→738, so its lower half is cut by the fixed foot («عرض الصفحة العامة», language, theme). The group's three links (الموظفون 742, سجل التدقيق 790, الإعدادات 838→882) are hidden below, with no sign that the list goes on. Settings and Staff look as if they were missing from the menu.
- **proposal:** Let the drawer scroll as one column, with the foot after the last group, or give the scroll area a fade or shadow at its foot edge so the cut reads as "more below".
- **why:** On the phone, the drawer is the only way to reach Staff, the audit log and Settings.
- **cost:** S
- **rule:** DECISIONS_OWNER DI-10 (2026-10-13); foundation §9

## 5. Decisions in doubt

None. OW-010 (sheets full width below `md`) is settled but does not appear in the archive yet. At 390 every owner sheet (package, staff, announcement, data report) is 293 px wide, three quarters of the screen. R2-OW-DF-001 is the defect this produces today.

## 6. What was not reviewed, and why

- **Coverage:** an automated pass loaded all 64 parameter sets of the ten pages at 390, 768 and 1440, in ar/en and light/dark: 1,536 loads. It measured console errors (none), horizontal page overflow (none), clipped and truncated text, sideways-scrolling boxes, and body text length (no blank frames: the shortest bodies are the 404/offline/error route states, 53–78 characters, by design). The visual review covered every page at all three widths in at least one ar and one en mode, plus every hot spot the prompt names. Not every one of the 1,536 frames was inspected by eye; where the probe found nothing, a defect visible only to the eye could remain.
- **Actions driven by real clicks:** «إنهاء الآن» (`fail=end`), the extension (`fail=extend`), package, staff and announcement saves (`fail=save` / `fail=add`), a settings card save, the void (`fail=void`), a profile group save, and a photo upload through the file input (`fail=upload`: «لم تُرفع: انقطع الاتصال» with «إعادة المحاولة» on its tile; an SVG gives «JPG أو PNG فقط»). The other actions on these pages were not clicked: reorder, cover, «تم التصحيح», renew, reissuing a password.
- **Upload 413:** not reachable without a file over 5 MB; not tried.
- **`Payments.html?staff=`:** loaded only with `staff=sami`, which may not be a valid key; the staff filter's other values were not checked.
- **Screenshots in `docs/design/screens/`:** not compared with the live prototype; §55's frames have none yet.
- **Out of this axis** (left to the other OW prompts): focus, keyboard, accessible names, contrast, touch targets (AX); wording (CP); flow (UX); visual consistency (VD); scope and API truth (TR).
- **The board's `Flows - states.html`:** not opened; the pages were reviewed through their own URLs.
