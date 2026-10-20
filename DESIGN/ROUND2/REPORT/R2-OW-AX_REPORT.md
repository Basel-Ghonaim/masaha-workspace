# R2-OW-AX — The owner's management · Accessibility and resilience

## 1. Commits

- `HEAD` (worktree `C:\dev\masaha\app-design`): `18ab1705149773bd05f2f7349ef341e33d175ca3`
- `origin/main`: `eff0a3d1e332a0161fde267a9a100f889184f550`
- They differ; `git diff --quiet HEAD origin/main -- docs/design` exits 0: **design unchanged**, review continued.

## 2. Verdict

Names, keyboard traps, contrast and the 44 px controls hold almost everywhere. The gaps are in the states a weak connection meets (no skeleton on six pages; a sheet's failure toast that cannot be reached), the page structure a screen reader relies on (Arabic titles in English, card titles that are not headings, two h1s on the route states), and a set of text links under 44 px on touch.

## 3. The five most important points

1. `?state=loading` shows no skeleton on six of the ten pages (Overview, Space profile, Settings, Packages, Announcements, Finance); they render their full data (R2-OW-AX-001).
2. The `<title>` stays Arabic («نظرة عامة — مساحة») when the interface is English, on all ten pages (R2-OW-AX-002).
3. When a sheet's save fails, a toast with «إعادة المحاولة» appears that no pointer or key can reach, and focus drops onto the sheet container (R2-OW-AX-003).
4. The Settings, Overview and Finance card titles are `DIV`s, so heading navigation skips every card, including Settings' three «حفظ» cards (R2-OW-AX-004).
5. Name and target links in rows and cards are 18–22 px tall on touch (Audit log, Overview, Payments at 768, Staff), and the Staff money links are named only «0 ₪» (R2-OW-AX-005, -006).

## 4. Issues

Local server: `http://127.0.0.1:5427/`. Captures: `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\OW-AX\`. Touch measurements use `Emulation.setTouchEmulationEnabled` plus `pointer: coarse`.

### R2-OW-AX-001 — No loading skeleton on six of the ten pages
- **type:** defect · **level:** pattern · **impact:** high
- **where:** Finance & reports «الدخل» — phone 390 (INDEX §33), `Finance.html?state=loading`, 390, Arabic light; `screens/33-finance-reports-owner/02-phone-390.webp`. Also `Owner overview.html`, `Owner space profile.html`, `Owner settings.html`, `Packages.html`, `Announcements.html` with `?state=loading`.
- **evidence:** `R2-OW-AX-001.png`
- **what is wrong:** with `?state=loading`, each of these six pages has 0 `Skeleton` elements and renders its full data («9020 ₪», the queue, every field). Staff, Payments, Data reports and Audit log show 25 skeleton elements. P7's loading state can't be reached on these six pages, so on a slow connection the owner sees either nothing or stale-looking figures, and a screen reader gets no busy state.
- **proposal:** give each page its `Skeleton` frame shaped like its content: StatCards on Finance and the Overview, card outlines with field rows on Settings and the Space profile, the price table and the package rows on Packages, and announcement cards on Announcements. Mark the loading region `aria-busy="true"`.
- **why:** the same weak-connection state on every page tells people "loading", not "empty" or "zero income".
- **cost:** M
- **rule:** DECISIONS_SHARED P7 (settled state unreachable); foundation §10.

### R2-OW-AX-002 — The document title stays Arabic in English, on every page
- **type:** defect · **level:** pattern · **impact:** medium
- **where:** Overview · a work queue, no money — desktop 1440 (INDEX §55), `Owner overview.html?lang=en&theme=dark`, 1440, English dark; no screenshot yet (§55). Same on all ten OW pages, in both themes and at every width.
- **evidence:** `R2-OW-AX-002.png`
- **what is wrong:** the page has `<html lang="en">` and its h1 reads "Overview", but `document.title` is «نظرة عامة — مساحة». The tab title and the first thing a screen reader announces are in the other language, and they are read with the English voice. The Arabic form also uses «—» where the rule asks for "{page} · Masaha".
- **proposal:** set the title from the copy catalogue on each language switch, as "{page} · Masaha" or «{page} · مساحة» (the shells' `PageHeader` already holds the page name).
- **why:** with several dashboard tabs open, the owner and a screen-reader user find the right one by its title.
- **cost:** S
- **rule:** foundation §10 (document title in the interface's language, WCAG 2.4.2).

### R2-OW-AX-003 — A sheet's failed save raises a toast that can't be reached, and focus is lost
- **type:** defect · **level:** pattern · **impact:** high
- **where:** Add staff sheet — desktop 1440 (INDEX §37), `Staff.html?sheet=add&fail=add`, 1440, Arabic light; `screens/37-staff-owner/03-add-staff-sheet-desktop-1440.webp`. The same `useActionRun` runs in the package sheet (`?fail=save`) and the announcement sheet (`?fail=save`).
- **evidence:** `R2-OW-AX-003.png`
- **what is wrong:** I filled both fields and pressed Enter on «إضافة إلى الاستقبال». Focus then lands on `DIV[role=dialog]` (the sheet itself, with no ring). A toast «تعذّر إتمام العملية · إعادة المحاولة» opens outside the modal sheet. Its button has `pointer-events: none` (body `pointer-events: none`), and eight Tab presses only cycle الاسم → البريد → submit → إغلاق, never reaching it. The toast is announced, but its offered action can't be used.
- **proposal:** when the action runs inside a sheet or dialog, raise no toast. Show the failure only in the sheet's `ActionAlert`, announced when it appears, and return focus to the submit button. Keep the toast with «إعادة المحاولة» for page-level actions only.
- **why:** one failure message with one working retry, and the keyboard user keeps their place.
- **cost:** S
- **rule:** DECISIONS_SHARED P8 (failure inside the sheet, which stays open); foundation §10 (full keyboard use).

### R2-OW-AX-004 — Card titles are not headings on Settings, Overview and Finance
- **type:** defect · **level:** pattern · **impact:** medium
- **where:** Owner settings — desktop 1440 (INDEX §40), `Owner settings.html`, 1440, Arabic light; `screens/40-settings-owner/01-owner-settings-desktop-1440.webp`. Also `Owner overview.html` and `Finance.html`.
- **evidence:** `R2-OW-AX-004.png`
- **what is wrong:** Settings has one heading, «الإعدادات» (h1). Its four card titles («الحضور والحالة المباشرة», «تسعير الزيارات», «رسالة التذكير», «حسابي») are `DIV`s, and three buttons are named only «حفظ». On the Overview the only h2 is «يحتاج انتباهك»: «الحاضرون الآن», «إعلانات نشطة» and «اشتراكات تنتهي هذا الأسبوع» are not headings. Finance has only its h1, with chart titles that are not headings. A screen-reader user can't jump to a card, and can't tell which card a «حفظ» saves. The Space profile and Packages do have h2 and h3, so the pages are inconsistent.
- **proposal:** pass each page's `CardTitle` its heading level (h2 for the cards, h3 inside), as SH-017 decided, on Settings, the Overview and Finance.
- **why:** heading navigation is how a screen-reader user scans a dashboard, and each «حفظ» is then read inside its card's heading.
- **cost:** S
- **rule:** DECISIONS_SHARED SH-017 (`CardTitle` takes a heading level); foundation §10.

### R2-OW-AX-005 — Name and target links in rows and cards are 21 px tall on touch
- **type:** defect · **level:** pattern · **impact:** medium
- **where:** Audit log · the space's — phone 390 (INDEX §55), `Owner audit.html?theme=dark`, 390, Arabic dark; no screenshot yet. Also Overview «اشتراكات تنتهي هذا الأسبوع» names (`Owner overview.html`, 390 and 768: 21 px) and Payments customer names (`Payments.html`, 768: 22 px).
- **evidence:** `R2-OW-AX-005.png`
- **what is wrong:** with touch emulation, the audit log's 20 target links (a person, «زيارة», «اشتراك شهري», …) are 332×21 px. On the Overview the customer names are 113×21 px beside a «تجديد» of 59×44. On Payments at 768 the names are 152–194×22 px.
- **proposal:** on a coarse pointer, give these row links a 44 px block. Either make the whole card or row the link, keeping the row's own buttons separate, or pad the link to `min-h-11` with `py`. Pages: Overview, Payments, Audit log.
- **why:** on a phone at the desk a 21 px target is often missed, or hits the line below.
- **cost:** S
- **rule:** foundation §10 (44×44 on touch).

### R2-OW-AX-006 — The Staff "this month" money links are 19×18 px and named only by the amount
- **type:** defect · **level:** page · **impact:** medium
- **where:** Staff · real columns, a pending password (INDEX §55) / Staff list — phone 390 (INDEX §37), `Staff.html`, 390, Arabic light; `screens/37-staff-owner/02-staff-list-phone-390.webp`. Also at 768 (21×19) and 1440 (18–44×19).
- **evidence:** `R2-OW-AX-006.png`
- **what is wrong:** each card's «هذا الشهر» link to `Payments.html?staff=…` is 41×18, 19×18 and 19×18 px on touch. Their names are only «1380 ₪», «0 ₪» and «0 ₪», which give neither the person nor the destination, so two links read identically in a links list.
- **proposal:** make it a `Button variant="link"` (or ghost) of at least 44 px, reading «دفعات ليلى هذا الشهر: 0 ₪».
- **why:** it becomes tappable, and the link says where it leads and whose money it is.
- **cost:** S
- **rule:** foundation §10 (44×44 on touch; a programmatic label for every control).

### R2-OW-AX-007 — Route states (offline, 403, 404) carry two h1s, the first naming the missing page
- **type:** defect · **level:** pattern · **impact:** low
- **where:** INDEX's URL parameters (`?state=offline · 403 · 404`), `Payments.html?state=404`, 1440, Arabic light; no screenshot. Same on all ten OW pages for offline, 403 and 404.
- **evidence:** `R2-OW-AX-007.png`
- **what is wrong:** the page has 2 h1s, «الدفعات» then «الصفحة غير موجودة». A screen reader announces the page as «الدفعات» and then says it does not exist. On Payments the header also keeps «تصدير CSV», although INDEX says these states have no actions.
- **proposal:** in a route state, have `PageHeader` show the state as the page's only h1 («الصفحة غير موجودة»), with the `EmptyState` title one level down, and no page actions.
- **why:** one h1 that matches what the user is actually looking at.
- **cost:** S
- **rule:** DECISIONS_SHARED P7; foundation §10.

### R2-OW-AX-008 — Text links show the browser's focus outline, not the design system ring
- **type:** defect · **level:** design system · **impact:** low
- **where:** Ledger · this month — desktop 1440 (INDEX §32), `Payments.html?theme=dark`, 1440, Arabic dark; `screens/32-payments-owner/01-ledger-this-month-desktop-1440.webp`. The same links on the Overview, Audit log, Staff, Settings («الباقات والأسعار») and Space profile («عرض الصفحة العامة»).
- **evidence:** `R2-OW-AX-008.png`
- **what is wrong:** after real Tab presses, the customer link «يوسف أبو شعبان» has `outline-style: auto` (the user-agent ring, near-white in dark mode). Every button, tab and nav link shows the 2 px teal `ring`. It is visible, but it is a second focus style.
- **proposal:** give the design system's text-link style (`Button variant="link"` / the link class) the same `focus-visible:outline-2 outline-ring outline-offset-2` as the controls.
- **why:** one ring means one thing to look for on every page.
- **cost:** S
- **rule:** foundation §10 ("One visible focus ring (`ring`) on every interactive element").

### R2-OW-AX-009 — The announcement sheet opens with focus on the type group, and no control shows it
- **type:** defect · **level:** page · **impact:** low
- **where:** New announcement · the model's fields — phone 390 (INDEX §55), `Announcements.html?sheet=new&type=closure`, 390, Arabic light; no screenshot yet. The same on `?tab=scheduled&edit=a1`, for owner and reception.
- **evidence:** `R2-OW-AX-009.png`
- **what is wrong:** on open, `document.activeElement` is `DIV[role=radiogroup]` (tabindex 0, `:focus-visible` false, no outline, no shadow). Nothing on screen shows focus. The first ArrowDown then lands on «عام», not on the checked «إغلاق مؤقت». The package and staff sheets open on their first field instead.
- **proposal:** open the sheet with focus on the checked type radio (or the Arabic text), and drop the group's own tabindex so the roving focus starts on the checked item.
- **why:** a keyboard user sees where they are as soon as the sheet opens, the same as in the other two sheets.
- **cost:** S
- **rule:** foundation §10 (visible focus; full keyboard use).

### R2-OW-AX-010 — The calendar popover is an unnamed dialog
- **type:** defect · **level:** design system · **impact:** low
- **where:** Ledger · this month — desktop 1440 (INDEX §32), `Payments.html`, 1440, Arabic light, «الفترة» opened with Enter; `screens/32-payments-owner/01-ledger-this-month-desktop-1440.webp`. The same popover on the announcement sheet's date fields (INDEX §41).
- **evidence:** `R2-OW-AX-010.png`
- **what is wrong:** Enter on «الفترة» moves focus into a `role=dialog` with `aria-label` and `aria-labelledby` both null, so it is announced as "dialog" with no purpose. Focus lands on «الشهر السابق». Its day buttons are named well («الثلاثاء، 1 سبتمبر 2026», 44×44 on touch).
- **proposal:** in the design system's date picker, label the popover with its field («الفترة», «يبدأ»/«ينتهي») through `aria-labelledby`, or use the month caption.
- **why:** a screen-reader user hears which date they are choosing.
- **cost:** S
- **rule:** foundation §10 (a programmatic label for every control); lens A.9.

### R2-OW-AX-011 — The "no shifts" link in the package sheet is 150×18 px on touch
- **type:** defect · **level:** page · **impact:** low
- **where:** Edit package · per day, no shifts saved (INDEX §55), `Packages.html?edit=p4&demo=noshifts`, 390, Arabic light; no screenshot yet.
- **evidence:** `R2-OW-AX-011.png`
- **what is wrong:** «أضف ورديات في ساعات العمل أولًا», the sheet's only way to the hours, measures 150×18 px with touch emulation.
- **proposal:** make it a `Button variant="outline" size="sm"` (44 px on touch) under the «الوردية» reason line.
- **why:** this is the step the owner has to take next, so it should be easy to tap.
- **cost:** S
- **rule:** foundation §10 (44×44 on touch).

### R2-OW-AX-012 — "View public page" in the space profile is 100×19 px on touch
- **type:** defect · **level:** page · **impact:** low
- **where:** Space profile — phone 390 (INDEX §36), `Owner space profile.html`, 390, Arabic light; `screens/30-owner-space-profile-kept/02-space-profile-phone-390.webp`. Also 768 and 1440 (99–109×19).
- **evidence:** `R2-OW-AX-012.png`
- **what is wrong:** the link under the section chips measures 100×19 px with touch emulation. The chips above it are 44 px tall.
- **proposal:** give it the size of the chips: an outline `Button` with the external icon, or a 44 px `min-h` on coarse pointers.
- **why:** after saving a section, checking the public page is the owner's natural next step.
- **cost:** S
- **rule:** foundation §10.

### R2-OW-AX-013 — The «تقريب لأعلى بعد» rounding choice has a 27 px tap area
- **type:** defect · **level:** page · **impact:** low
- **where:** Owner settings — phone 390 (INDEX §40), `Owner settings.html`, 390, Arabic light, card «تسعير الزيارات»; `screens/40-settings-owner/02-owner-settings-phone-390.webp`.
- **evidence:** `R2-OW-AX-013.png`
- **what is wrong:** with touch emulation the radio is 18×18 px and its label 90×27 px. The other two choices' labels are 163×44 and 116×44 px. The minutes input sitting inline keeps this one row short.
- **proposal:** give the row the same 44 px `min-h` as its siblings (the minutes input can stay inline).
- **why:** all three choices are equally easy to tap.
- **cost:** S
- **rule:** foundation §10.

### R2-OW-AX-014 — The tablet rail's last item is 39 px wide
- **type:** defect · **level:** pattern · **impact:** low
- **where:** the shell at 768 (no board frame); `Finance.html`, 768, Arabic light. The same rail on all ten OW pages.
- **evidence:** `R2-OW-AX-014.png`
- **what is wrong:** with touch emulation «عرض الصفحة العامة» measures 39×44 px. Every other rail item is 47×44 px.
- **proposal:** use the rail's item size (`SidebarMenuButton`) for the footer link too.
- **why:** the same target everywhere in the rail.
- **cost:** S
- **rule:** foundation §10; lens §2c (768).

### R2-OW-AX-015 — "Copied" in the temporary-password dialog is never announced
- **type:** improvement · **level:** page · **impact:** low
- **where:** Staff · the password, shown once — phone 390 (INDEX §55) / Temporary password (INDEX §37), `Staff.html?pass=1`, 390, Arabic light; `screens/37-staff-owner/06-temporary-password-shown-once-phone-390.webp`.
- **evidence:** `R2-OW-AX-015.png`
- **what is wrong:** the dialog opens with focus on «نسخ», and Enter changes its text to «نُسخت». The dialog holds no live region and no toast is raised. The only live region on the page («عدد الموظفين: 3») is outside the dialog, so a screen reader on the focused button is not told the copy worked. That matters for a password shown only once.
- **proposal:** put a polite `role="status"` inside the dialog that reads «نُسخت كلمة المرور» after the copy (or «تعذّر النسخ — انسخها يدويًا» on failure).
- **why:** the owner can close the dialog knowing the password was actually copied.
- **cost:** S
- **rule:** DECISIONS_SHARED P8 (every action says it worked); foundation §10.

## 5. Decisions in doubt

None.

## 6. What was not reviewed, and why

- **A real screen reader** (NVDA, VoiceOver, TalkBack) was not run; none is driveable from this headless setup. Reading order, names, roles, `aria-current`, live regions and dialog names were read from the rendered DOM with in-page JavaScript, and focus order was checked with real `Input.dispatchKeyEvent` Tab, Arrow, Enter and Escape presses.
- **How the toasts are actually spoken.** The Sonner region is `aria-live="polite"` («الإشعارات») and receives the toasts, but whether a given reader speaks them was not heard.
- **Live failures.** `?fail=` and `?state=ratelimit` are static frames: the in-sheet `ActionAlert`, the per-card Settings alerts (`?fail=save-attendance|save-pricing|save-message`) and the three 429 alerts on Settings render on load, so I could not observe whether they are announced *when* a request fails.
- **Clipboard.** The copy in the password dialog could not be checked in headless Chrome; only the button's change to «نُسخت» was observed.
- **Contrast.** Computed text contrast on all ten pages at 390, 768 and 1440, Arabic and English, light and dark (120 renders), found no text under WCAG AA, including the badges, helpers and the struck voided amount with «ألغاها أحمد: …». The only low values were the `aria-disabled` pagination buttons (3.25:1), which are exempt. Inputs, radios and borders measured 3.97–6.69:1 against their background. The off-state of a switch was not seen (every switch on these pages is on).
- **Checked with no finding:** names on every row «⋯» menu («إجراءات الدفعة: 50 ₪ · …», «إجراءات سامي»), the month and filter selects (via `label[for]`), the tabs and every radiogroup and toolbar; editor chips with `aria-current="location"` at 44 px; the void dialog (`alertdialog`, named, validation moves focus to «السبب» with `aria-invalid` and `aria-describedby`); the drawer on a phone (opens on the account, 44 px items, Escape returns focus to «القائمة»); focus traps in all sheets and dialogs; voided rows (struck *and* «ألغاها …» text); queue badges («قديمة», «لم تُضف بعد») with text; no horizontal scroll at any width.
