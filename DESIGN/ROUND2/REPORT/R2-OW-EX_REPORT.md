# R2-OW-EX — The owner's management · Excess and simplification

## 1. Commits

- `HEAD` = `18ab1705149773bd05f2f7349ef341e33d175ca3`
- `origin/main` = `eff0a3d1e332a0161fde267a9a100f889184f550`
- They differ; `git diff --quiet HEAD origin/main -- docs/design` exited **0**: **design unchanged**, review continued.

## 2. Verdict

O3 holds (no amount anywhere on the overview, in any variant). The excess sits in Finance, where one month control and three stat cards repeat what the sections below them already say, and in labels that repeat the tab or the action they sit in.

## 3. The five most important points

1. Finance: the «الشهر» select changes one card per tab. «اليوم», «منذ البداية», every debt figure and every chart ignore it (001).
2. Finance › الديون carries «دفعوا في <الشهر>» twice (a card and a list), and that is the Payments ledger's job (002).
3. Finance repeats itself card-to-section: «أرصدة للزبائن» repeats «لهم رصيد» (003), and «ساعة الذروة» repeats the heatmap (004).
4. Each staff member's monthly collections appear on two pages (Staff's «مقبوضاته هذا الشهر» and Finance's «التحصيل حسب الموظف»), so money also shows on a page about access (005).
5. Ended announcements' «عرض» opens the full «تعديل الإعلان» sheet with «حفظ». That action is on rows that should not take it (009).

## 4. Issues

Server: `http://127.0.0.1:5425/`. Shots: `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\OW-EX\`. Each removal was checked again at 768, `?lang=en&theme=dark`. It holds there unless the issue says otherwise.

### R2-OW-EX-001 — Finance's month select drives one card per tab
- **type** improvement · **level** page · **impact** high
- **where** «Finance · one month — desktop 1440» (§55); `Finance.html?month=2026-08`; 1440 Arabic light; screenshot — (§55 has none yet; nearest `screens/33-finance-reports-owner/01-desktop-1440.webp`)
- **evidence** `R2-OW-EX-001.png`
- **what is wrong** With «أغسطس 2026» chosen, only the middle card changes (9020 ₪ → «8090 ₪ · +5% عن يوليو 2026»). «اليوم 104 ₪ حتى 12:40» and «منذ البداية 101370 ₪» stay the same, and both charts keep their own windows («آخر 12 شهرًا», «آخر 30 يومًا»). On `?tab=debts&month=2026-08`, «مجموع الديون 293 ₪», «أرصدة للزبائن 18 ₪» and all five debt rows stay the same; only «دفعوا في أغسطس 2026 · 16 زبونًا» moves. At 768 in English and dark it is the same («Total owed ₪293», «Paid in August 2026 / 16 customers»). The control looks like it filters the whole page but filters almost nothing.
- **proposal** Remove the page-level «الشهر» `Field`. Put one month `Select` in the header of the income month card, the only card it drives (and in «التحصيل حسب الموظف», which is per month). The Debts tab has no month control at all (see 002).
- **why** The owner stops picking a month and wondering why nothing changed; each figure shows its own window.
- **cost** S · **rule** DECISIONS_OWNER «Smaller» OW-015 (the select's *placement* is the application; the single «الشهر» choice is kept)

### R2-OW-EX-002 — Debts tab repeats «who paid this month», which is the ledger's job
- **type** improvement · **level** page · **impact** medium
- **where** «الديون — desktop 1440» (§33); `Finance.html?tab=debts`; 1440 Arabic light; `screens/33-finance-reports-owner/03-desktop-1440.webp`
- **evidence** `R2-OW-EX-002.png`
- **what is wrong** The tab says «دفعوا في سبتمبر 2026» twice: as a stat card «45 زبونًا», and as a section of five rows with «عرض الكل». That link goes to the Payments ledger, whose «الفترة» filter already answers the question. Neither is a debt.
- **proposal** Remove both the card and the section from الديون. The tab keeps «مجموع الديون», «عليهم مبالغ» and the credit (003). Cross-page: Finance and Payments.
- **why** The debts tab answers one question, "who owes me"; the owner is not shown 45 payers in a debt view.
- **cost** S · **rule** lens §3 B.1; DECISIONS_OWNER OW-016 (the list's «عرض الكل» goes with it)

### R2-OW-EX-003 — «أرصدة للزبائن» card and «لهم رصيد» section say the same thing
- **type** improvement · **level** page · **impact** low
- **where** «الديون» (§33); `Finance.html?tab=debts`; **768** Arabic light; `screens/33-finance-reports-owner/03-desktop-1440.webp`
- **evidence** `R2-OW-EX-003.png`
- **what is wrong** The card says «18 ₪ · زبون واحد دفعوا مقدمًا». The section below says «لهم رصيد · دفعوا مقدمًا أكثر مما استخدموا» with one row, «رنا الأغا · له رصيد 18 ₪». The same fact appears twice with the same subtitle wording. At 768 it takes a full card plus a full section.
- **proposal** Keep the «لهم رصيد» section, with the total in its header line («18 ₪ · زبون واحد»), and remove the stat card. Once 002 is applied, «مجموع الديون» is the tab's only stat card.
- **why** One place for credit; the eye finds the debt total at once.
- **cost** S · **rule** —

### R2-OW-EX-004 — Occupancy's «ساعة الذروة» card repeats the heatmap below it
- **type** improvement · **level** page · **impact** low
- **where** «الإشغال — desktop 1440» (§33/§35); `Finance.html?tab=occupancy`; 1440 Arabic light; `screens/33-finance-reports-owner/05-desktop-1440.webp`
- **evidence** `R2-OW-EX-004.png`
- **what is wrong** The card says «11:00–13:00 · الأحد والاثنين الأعلى». The «ساعات الذروة» heatmap right under it shows exactly that: its darkest cells are 11–13 on Sunday and Monday. It is the same finding twice, and the windows disagree: the card says «سبتمبر 2026», the heatmap «آخر 4 أسابيع».
- **proposal** Remove the card. Put the peak in the heatmap's description line («الذروة 11:00–13:00، الأحد والاثنين»).
- **why** One answer to "when is it busiest", with one window, next to the evidence.
- **cost** S · **rule** DECISIONS_OWNER OW-015 (windows named)

### R2-OW-EX-005 — Staff collections shown on two pages
- **type** improvement · **level** pattern (Staff, Finance) · **impact** medium
- **where** «Staff · real columns, a pending password — desktop 1440» (§55); `Staff.html`; 1440 Arabic light; `screens/37-staff-owner/01-staff-list-desktop-1440.webp`
- **evidence** `R2-OW-EX-005.png`
- **what is wrong** Staff's column «مقبوضاته هذا الشهر» reads «سامي 1380 ₪». Finance › الدخل › «التحصيل حسب الموظف» reads «سامي · 58 · 1380 ₪» for the same month, with count, cash and transfer added. The figure appears on two pages; on the Staff page it is the only amount, on a page about access (status, password, deactivate). At 768 en/dark: «Collected this month ₪1380».
- **proposal** Remove the column from Staff; Finance's table is the money home. If the link is wanted, the staff row's «⋯» can offer «مقبوضاته» → `Payments.html?staff=<id>`.
- **why** Money stays in the money pages, and the Staff list is open in front of the staff it lists.
- **cost** S · **rule** DECISIONS_OWNER OW-018 (only if its "real columns" named this one; then see §5)

### R2-OW-EX-006 — Staff states its count twice
- **type** improvement · **level** page · **impact** low
- **where** «Staff list — phone 390» (§37); `Staff.html`; 390 Arabic light; `screens/37-staff-owner/02-staff-list-phone-390.webp`
- **evidence** `R2-OW-EX-006.png`
- **what is wrong** «عدد الموظفين: 3» sits beside «إضافة موظف», and the footer says «صفحة 1 من 1» (1440: «عرض 1–3 من 3»). The page has no filter bar, so P5's result count does not apply, and three cards are counted by eye.
- **proposal** Remove «عدد الموظفين». «إضافة موظف» keeps its row (P1 amended).
- **why** One less line above the list on a phone.
- **cost** S · **rule** DECISIONS_SHARED P5 (result count is for a filter bar), P6

### R2-OW-EX-007 — Pagination on lists that have one page
- **type** improvement · **level** pattern (Announcements, Staff, Data reports, Finance › الديون) · **impact** low
- **where** «Active · owner — phone 390» (§38); `Announcements.html`; 390 Arabic light; `screens/38-announcements-owner-reception/02-active-owner-phone-390.webp`
- **evidence** `R2-OW-EX-007.png`
- **what is wrong** Two announcements, then «عرض 1–2 من 2», then «السابق · صفحة 1 من 1 · التالي», both buttons `aria-disabled="true"`. The tab already says «نشطة 2». The same footer is on Staff («1–3 من 3»), Data reports («1–4 من 4»), all three announcement tabs and the debts list («1–5 من 5»). That is two dead buttons and a third count.
- **proposal** Render `Pagination` only when total > page size (20). On one page, show nothing (the tab or filter count already says how many).
- **why** The phone loses a row of disabled controls that cannot be used.
- **cost** S · **rule** DECISIONS_SHARED P6 (how pages apply it)

### R2-OW-EX-008 — Announcement status badge repeats the tab
- **type** improvement · **level** page · **impact** low
- **where** «Announcements · end now, no end, quiet types — desktop 1440» (§55); `Announcements.html`; 1440 Arabic light; screenshot — (nearest `screens/38-announcements-owner-reception/01-active-owner-desktop-1440.webp`)
- **evidence** `R2-OW-EX-008.png`
- **what is wrong** In «نشطة» every row carries «نشط»; in «مجدولة» every row «مجدول»; in «منتهية» every row «انتهى» (en: «Active», «Ended»). The badge can only ever say the tab's name.
- **proposal** Remove the status badge from rows; keep the type badge.
- **why** Each card has one badge, the one that tells rows apart (the type).
- **cost** S · **rule** —

### R2-OW-EX-009 — Ended announcements open an editable sheet from «عرض»
- **type** improvement · **level** page · **impact** medium
- **where** «Ended · one closure extended, one to extend — desktop 1440» (§38); `Announcements.html?tab=ended`, then «عرض» on the 22 Sept outage; 1440 Arabic light; `screens/38-announcements-owner-reception/09-ended-closure-extension-done-desktop-1440.webp`
- **evidence** `R2-OW-EX-009.png`
- **what is wrong** The ended row already shows its type, period and full text. «عرض» opens «تعديل الإعلان»: the type `RadioGroup`, both texts, start/end and «حفظ». It does the same for reception (`role=reception`: three «عرض» buttons) and at 768 en/dark («Edit announcement … Save»). The control duplicates the row, and it offers an edit on a record that is over.
- **proposal** Remove «عرض» from ended rows. The row is the view. Keep «تمديد الاشتراكات» where it applies (O11).
- **why** Fewer buttons per row, and no-one edits a finished announcement by accident.
- **cost** S · **rule** DECISIONS_OWNER O10 (actions on an announcement)

### R2-OW-EX-010 — The temporary-password dialog says "shown once" twice
- **type** improvement · **level** component · **impact** low
- **where** «Staff · the password, shown once — phone 390» (§55); `Staff.html?pass=1`; 390 Arabic light; `screens/37-staff-owner/06-temporary-password-shown-once-phone-390.webp`
- **evidence** `R2-OW-EX-010.png`
- **what is wrong** The body says «لن تظهر مرة أخرى بعد إغلاق هذه النافذة.», and the footer under «تم» says «انسخها أولًا — لن تظهر مرة أخرى». en: «It won’t be shown again after you close this window.» / «Copy it first — it won’t be shown again».
- **proposal** Keep only the footer line beside «تم», where the decision is made, and remove the body line.
- **why** A shorter dialog; the warning sits once, at the button that closes it.
- **cost** S · **rule** DECISIONS_OWNER O4 (A5's dialog rules; wording only, nothing removed from A5)

### R2-OW-EX-011 — The overview's live card repeats the top bar's public state
- **type** improvement · **level** page · **impact** medium
- **where** «Overview · a work queue, no money — desktop 1440» (§55); `Owner overview.html`; 1440 Arabic light; screenshot — (nearest `screens/29-owner-overview-kept/01-overview-desktop-1440.webp`)
- **evidence** `R2-OW-EX-011.png`
- **what is wrong** The top bar's P2 control reads «يظهر للزوار: متاح». The «الحاضرون الآن» card ends with a badge reading the same «يظهر للزوار: متاح», plus «السعة لا تظهر للزوار، فقط الحالة.». On a phone the bar says «متاح» and the card says it again. en/768: «Visitors see: Available / Visitors never see capacity, only the state.»
- **proposal** Remove the badge and the line from the card. The P2 control is the one place for what visitors see, and the capacity note belongs to Settings' capacity field, which already says «لا تظهر للزوار».
- **why** The card answers "how full are we"; the bar answers "what do visitors see". Neither is said twice.
- **cost** S · **rule** DECISIONS_SHARED P2

### R2-OW-EX-012 — "No capacity" is said three times on one screen
- **type** improvement · **level** page · **impact** low
- **where** «Overview · no capacity, a group never saved — desktop 1440» (§55); `Owner overview.html?demo=nocapacity`; 1440 Arabic light; screenshot —
- **evidence** `R2-OW-EX-012.png`
- **what is wrong** The top bar says «يظهر للزوار: بلا حالة مباشرة». The queue row says «لم تُحدَّد السعة · بدونها لا تظهر حالة مباشرة للزوار · تحديد السعة». The live card adds «يظهر للزوار: بلا حالة مباشرة · حدّد السعة في الإعدادات لتظهر حالة مباشرة.» en/768: «Capacity is not set / Without it visitors see no live status.» and «Visitors see: No live status / Set the capacity in Settings for a live status.»
- **proposal** The queue row is the call to action (O3); remove the card's line (with 011, the card shows only the count).
- **why** One instruction with one button; less to read when nothing has changed.
- **cost** S · **rule** DECISIONS_OWNER O3

### R2-OW-EX-013 — «إعلانات نشطة» card on the overview has no work in it
- **type** improvement · **level** page · **impact** low
- **where** «Overview · a work queue — phone 390» (§55); `Owner overview.html`; 390 Arabic light; screenshot —
- **evidence** `R2-OW-EX-013.png`
- **what is wrong** A full-width card on a phone, «إعلانات نشطة · 2 · فعالية، عرض», linking to Announcements. It is not in O3's list for the overview (queue, «الحاضرون الآن», ending subscriptions) and asks nothing of the owner. Announcement work that does need the owner, such as the closure extension, is already a queue row («إغلاق لم تُمدَّد اشتراكاته»). The card is the same at 768 en/dark («Active announcements / 2 / Event, Offer»).
- **proposal** Remove the card; Announcements stays one tap away in P3's «المساحة» group.
- **why** The ending subscriptions, which are actual work, move a whole card higher on a phone.
- **cost** S · **rule** DECISIONS_OWNER O3

### R2-OW-EX-014 — Settings' «حسابي» card repeats the account menu
- **type** improvement · **level** page · **impact** low
- **where** «Owner settings — phone 390» (§40); `Owner settings.html`; 390 Arabic light; `screens/40-settings-owner/02-owner-settings-phone-390.webp`
- **evidence** `R2-OW-EX-014.png`
- **what is wrong** The last card, «حسابي · الاسم وكلمة المرور واللغة والمظهر · الإعدادات الشخصية», links to account settings. The account menu (P4) already holds «إعدادات حسابي» (observed: «أحمد · صاحب المساحة / … / الموقع العام / إعدادات حسابي / تسجيل الخروج»). en/768: «My account / Personal settings».
- **proposal** Remove the card; Settings holds the space's settings only.
- **why** The page has one job, and personal settings have one way in.
- **cost** S · **rule** DECISIONS_SHARED P4

### R2-OW-EX-015 — "Chosen at the desk" stated three times on Packages
- **type** improvement · **level** page · **impact** low
- **where** «New package sheet · live summary — desktop 1440» (§34); `Packages.html?sheet=new`; 1440 Arabic light; `screens/34-packages-prices-owner/03-new-package-sheet-live-summary-desktop-1440.webp`
- **evidence** `R2-OW-EX-015.png`
- **what is wrong** On one screen: the page intro «أسعار الأسبوع والشهر تُختار أيضًا في المكتب عند إنشاء اشتراك.», the section line «لا تظهر للزوار · تُختار في المكتب عند إنشاء اشتراك», and the sheet's description «باقة خاصة — لا تظهر للزوار، وتُختار في مكتب الاستقبال.» All three are present in English at 768.
- **proposal** Keep the section line under «الباقات الخاصة». Put the intro's fact on «الأسعار المعلنة»'s own line (it is about those prices). The sheet's description goes; its title and the section already say it.
- **why** Each fact sits once, next to what it describes.
- **cost** S · **rule** foundation §13 #21 (as amended by DECISIONS_OWNER «Rules changed»)

### R2-OW-EX-016 — A paused package says so twice
- **type** improvement · **level** page · **impact** low
- **where** «Packages & prices · two sections — desktop 1440» (§55); `Packages.html` (scrolled); 1440 Arabic light; screenshot —
- **evidence** `R2-OW-EX-016.png`
- **what is wrong** «صباحي للطلاب» carries a «موقوفة» badge, a tinted row, and its «متاحة في المكتب» switch off. The badge restates the switch beside it (en: «Paused» + «Available at the desk» off).
- **proposal** Remove the badge; the switch is the state and its control.
- **why** One signal, which is also the way to change it.
- **cost** S · **rule** —

### R2-OW-EX-017 — «عرض الصفحة العامة» twice on the space profile
- **type** improvement · **level** page · **impact** low
- **where** «Space profile · the editor, prices as a row — desktop 1440» (§55); `Owner space profile.html`; 1440 Arabic light; screenshot —
- **evidence** `R2-OW-EX-017.png`
- **what is wrong** The intro line ends with the link «عرض الصفحة العامة», and the sidebar's foot has the same link a few hundred pixels away. At 768 the rail keeps it as an eye icon (`aria-label="View public page"`) and the intro keeps the text link.
- **proposal** Remove the intro's link from 768 up; keep it below `md`, where the sidebar is in the drawer.
- **why** One way to the public page per screen.
- **cost** S · **rule** DECISIONS_OWNER O1 (owner's page only, not the shared editor)

### R2-OW-EX-018 — Audit rows for a new customer repeat the action as the target
- **type** improvement · **level** page · **impact** low
- **where** «Audit log · the space's — desktop 1440» (§55); `Owner audit.html`; 1440 Arabic light; screenshot —
- **evidence** `R2-OW-EX-018.png`
- **what is wrong** Three rows read «سامي | زبون جديد | زبون جديد | —». The action badge and the target cell say the same words, and the details cell is empty (en: «New customer | A new customer»). Every other row names its target («ليلى», «رهف قديح», «ساعات العمل»).
- **proposal** The target is the customer's name, as on every other row. If the name cannot be shown, leave the target cell empty rather than repeating the action.
- **why** The row answers "who was added".
- **cost** S · **rule** DECISIONS_OWNER O13

## 5. Decisions in doubt

- **P5 + P6 give one filtered list two counts.** Data reports shows «عدد البلاغات: 4» (P5's result count) and «عرض 1–4 من 4» (P6's footer). The same happens on the audit log («الأحداث: 64» and «عرض 1–20 من 64») and on Payments («277 دفعة» and «عرض 1–20 من 277»). Proposal: when both are present, the footer summary is enough; P5's count could live only inside the `FilterSheet`'s «عرض N نتيجة». Pattern-level: Data reports, Owner audit, Payments, and every admin list with a filter bar.
- **OW-018's staff columns:** if «مقبوضاته هذا الشهر» was one of the settled "real columns", 005 becomes a doubt about that choice rather than an issue: money on the Staff list duplicates Finance's per-staff table.
- **O3 money check: nothing to report.** `Owner overview.html`, `?demo=missing,nocapacity`, `?demo=clear`, `?drawer=open` and `?lang=en&theme=dark` were read at 768. No line contained ₪/ILS/NIS. The queue's debt row is a count with a link («5 زبائن عليهم مبالغ · المبالغ في المالية › الديون»).

## 6. What was not reviewed, and why

- **Steps that could merge (prompt §5.5): nothing qualified as excess.** A new announcement already has «يبدأ: الآن / في موعد» in its sheet. Staff add → password is two surfaces, settled by OW-019/A5. A new package is born «متاحة في المكتب», with no separate publish step.
- **Package-sheet «الملخّص»:** it restates the fields as typed. It was not judged excess, because it is the sheet's only check of a limits combination; there is no evidence it is unused.
- **The shared editor's own hints** (for example «"نسخ إلى كل الأيام" ينسخ ساعات السبت…»): the hint names which day copies, so it was not judged pure repetition. Owner batch rule: the shared editor is not changed here.
- **Out of axis and seen in passing, not reported:** for the same September, Payments' «المجموع 11783 ₪ · 277 دفعة» differs from Finance's «9020 ₪» and from the per-staff table's 41 + 58 = 99 payments (DF/TR). Also, `captureBeyondViewport` captures in RTL drew the page shifted sideways; this is a capture-tool artefact, not a page defect, and live `scrollWidth` was 1440 = `clientWidth`.
- **Not opened state by state:** the `?fail=…`, `?state=loading|error|offline|403|404` and `?state=ratelimit` variants (states belong to DF/AX), and the admin editor's carry pages outside this scope.
- **Widths and modes covered:** every page in scope at 1440 and 390 in Arabic light. Each issue's page was checked again at 768 with `lang=en&theme=dark` (Owner overview, Space profile, Settings, Audit, Packages, Staff, Announcements and its ended tab, Finance with all three tabs). Payments and Data reports were seen at 1440 and 390 only. Their only finding is the P5/P6 count doubling, which is listed under §5 rather than raised as an issue.

---
Report: `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-OW-EX_REPORT.md` · issues: 18 · captures: 18
