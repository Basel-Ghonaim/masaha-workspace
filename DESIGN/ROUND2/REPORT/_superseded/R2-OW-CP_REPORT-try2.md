# R2-OW-CP — Round 2 review: The owner's management · Content and Arabic copy

## 1. Commit SHAs
- HEAD: `02b1067a136d3c86378b3da60937c5f51124dc5b`
- origin/main: `60a78063590e8660c937629bf633b18aa2f9a4f1`
- Design unchanged (git diff --quiet HEAD origin/main -- docs/design exits 0)

## 2. Verdict
The owner's management pages are functionally complete but contain several copy defects: Arabic leaks into the English mirror, key terms drift from the glossary, action labels don't match what happens, and plural/gender handling is inconsistent.

## 3. Five most important points
1. **English mirror leaks Arabic**: `Announcements.html?tab=ended` shows "الإنترنت بطيء هذا الصباح، ونعمل على إصلاحه" untranslated (a5.outage has empty `textEn` in owner-data.js).
2. **"عرض الكل" (View all) buttons promise navigation but go nowhere** — on Overview (subscriptions ending this week), Finance debts (credit/paid lists), and Announcements active tab (each row's "عرض").
3. **Void payment copy uses past-tense "ألغاها أحمد" in the ledger but the dialog action is "إلغاء الدفعة"** — inconsistent verb form; the ledger should use a void noun phrase per glossary "إلغاء دفعة".
4. **Closure extension dialog states "40 اشتراكًا" but the ended list shows "مُدِّد 19 اشتراكًا 3 أيام" for a4** — the numbers don't reconcile; the dialog must show the true count that will move.
5. **Staff password delivery methods are "واتساب / شفهيًا / أخرى"** — "شفهيًا" (verbally) is not a delivery method the system can track; it should be "بشخصه" (in person) to match the audit log "سُلّمت شفهيًا".

---

## 4. Issues

### R2-OW-CP-001 — English mirror leaks Arabic in Announcements ended tab
**Type:** defect | **Level:** page | **Impact:** high  
**Where:** Frame "Ended · one closure extended, one to extend — desktop 1440", `Announcements.html?lang=en&tab=ended`, 1440×1000, light  
**Evidence:** `docs/design/screens/R2-OW-CP-001.png`

**What is wrong:** The English page shows the Arabic text "الإنترنت بطيء هذا الصباح، ونعمل على إصلاحه" for announcement a5 (outage type). In `owner-data.js` line 57, a5 has `textEn: ''` (empty string), so the prototype falls back to `textAr`.

**Proposal:**
- AR (unchanged): الإنترنت بطيء هذا الصباح، ونعمل على إصلاحه.
- EN (add to owner-data.js): "The internet is slow this morning; we're working on it."

**Why better:** The English mirror must never show Arabic. Every announcement needs `textEn` or a clear "[No English text]" placeholder.

**Cost:** S (data fix in owner-data.js; prototype already falls back correctly)

**Rule:** REVIEW_LENS.md §3.A.10 (words), DECISIONS_OWNER.md O9 (announcements follow the model — includes optional English text)

---

### R2-OW-CP-002 — "عرض الكل" buttons are dead links
**Type:** defect | **Level:** pattern | **Impact:** high  
**Where:** 
- Frame "Overview — desktop 1440", `Owner overview.html`, 1440×1000, light — "عرض الكل" under "اشتراكات تنتهي هذا الأسبوع" (8 اشتراكات)
- Frame "الدخل — desktop 1440", `Finance.html?tab=debts`, 1440×1000, light — "عرض الكل" under "لهم رصيد" and "دفعوا في سبتمبر 2026"
- Frame "Active · owner — desktop 1440", `Announcements.html`, 1440×1000, light — "عرض" button on each active announcement row  
**Evidence:** `docs/design/screens/R2-OW-CP-003.png`, `docs/design/screens/R2-OW-CP-010.png`, `docs/design/screens/R2-OW-CP-014.png`

**What is wrong:** Three "view all" controls exist but none navigate:
1. Overview → "عرض الكل" beside "8 اشتراكات" — no `href`, no click handler visible.
2. Finance debts → two "عرض الكل" links (credit list, paid-this-month list) — no navigation target.
3. Announcements active → each row has "عرض" — opens nothing; the row is already fully shown.

**Proposal:**
- Overview: change "عرض الكل" → link to `Customers.html?pay=ending-soon` (or a filtered subscriptions list).
- Finance debts: "عرض الكل" under credit → `Finance.html?tab=debts&filter=credit`; under paid → `Finance.html?tab=debts&filter=paid-this-month`.
- Announcements active: remove "عرض" button — the row already shows the full text; or make it "تعديل" (edit) for owner, hidden for reception.

**Why better:** "عرض الكل" and "عرض" promise navigation. If they don't go anywhere, they mislead the user.

**Cost:** M (needs routing targets in prototype; API endpoints exist for filtered lists)

**Rule:** REVIEW_LENS.md §3.A.10 (labels that do not say what happens), DECISIONS_SHARED.md P5 (filter bar "عرض N نتيجة" is the settled pattern for filtered views)

---

### R2-OW-CP-003 — Void payment: ledger says "ألغاها أحمد" but dialog action is "إلغاء الدفعة"
**Type:** defect | **Level:** component | **Impact:** medium  
**Where:** Frame "Voided shown (struck + who) — desktop 1440", `Payments.html?voided=1`, 1440×1000, light; Frame "Void a payment · reason required — desktop 1440", `Payments.html?void=1`, 1440×1000, light  
**Evidence:** `docs/design/screens/R2-OW-CP-004.png`

**What is wrong:** 
- Ledger row shows: "ألغاها أحمد: سُجّلت بالخطأ" (Ahmed cancelled it: recorded by mistake) — past-tense verb "ألغاها".
- Dialog title: "إلغاء الدفعة؟" (Void the payment?), primary button: "إلغاء الدفعة" (Void payment).
- Glossary term: "Void a payment" = "إلغاء دفعة" (masdar/noun), not a past-tense verb.

**Proposal:**
- Ledger: change to "ملغاة · أحمد: سُجّلت بالخطأ" (Voided · Ahmed: recorded by mistake) — use the participle/adjective "ملغاة" matching glossary "إلغاء دفعة".
- Dialog: keep "إلغاء الدفعة؟" / "إلغاء الدفعة" (matches glossary).

**Why better:** Consistent terminology. "ملغاة" is the state; "إلغاء" is the action. The past-tense verb "ألغاها" reads as narration, not a status label.

**Cost:** S (copy change in prototype)

**Rule:** glossary "Void a payment / إلغاء دفعة", DECISIONS_SHARED.md P9 ("إلغاء is only the verb of voiding a payment")

---

### R2-OW-CP-004 — Closure extension dialog shows "40 اشتراكًا" but a4 shows "مُدِّد 19 اشتراكًا 3 أيام"
**Type:** defect | **Level:** component | **Impact:** high  
**Where:** Frame "Closure extension · the confirmation — desktop 1440", `Announcements.html?tab=ended&extend=a6`, 1440×1000, light  
**Evidence:** `docs/design/screens/R2-OW-CP-002.png`

**What is wrong:** The extension dialog for a6 (power-cut closure, 24–25 Sept, 2 days) says:
- "تتأخر نهاية 40 اشتراكًا نشطًا يومين" (The end of 40 active subscriptions moves 2 days later)
- "أيام الإغلاق: 2" (Closure days: 2)
- Primary button: "مدّد 40 اشتراكًا" (Extend 40 subscriptions)

But the ended list shows a4 (14–16 Sept, 3 days) with "مُدِّد 19 اشتراكًا 3 أيام · أحمد · 17 سبتمبر 2026". The numbers 40 vs 19, 2 vs 3 days, don't match any single closure. The dialog must reflect the actual active subscriptions affected by *this* closure (a6).

**Proposal:**
- Dialog body: "تتأخر نهاية **X** اشتراكًا نشطًا **Y** أيام" where X = count of active subscriptions on the closure start date, Y = closure duration in days.
- Button: "مدّد **X** اشتراكًا".
- For a6: compute from data (likely ~19–20, not 40).

**Why better:** The confirmation must state the true consequence (P9/O11). "40" appears to be a stale placeholder.

**Cost:** M (prototype data wiring; the real count comes from the API)

**Rule:** DECISIONS_OWNER.md O11 (extension dialog names how many active subscriptions move and by how many days), REVIEW_LENS.md §3.A.11 (truth to the product)

---

### R2-OW-CP-005 — Staff password delivery method "شفهيًا" is not trackable
**Type:** improvement | **Level:** component | **Impact:** medium  
**Where:** Frame "Temporary password (shown once) — desktop 1440", `Staff.html?pass=1`, 1440×1000, light  
**Evidence:** `docs/design/screens/R2-OW-CP-005.png`

**What is wrong:** Delivery method options: "واتساب" (WhatsApp), "شفهيًا" (verbally), "أخرى" (Other). The audit log (owner-data.js line 74) records "كلمة مرور مؤقتة سُلّمت شفهيًا" — but "شفهيًا" means "orally", not "in person". The owner cannot prove delivery.

**Proposal:**
- Change "شفهيًا" → "بشخصه" (in person) — matches the audit log intent and is verifiable.
- Keep "واتساب", "أخرى".

**Why better:** "بشخصه" is a concrete delivery method; "شفهيًا" describes speech, not handoff.

**Cost:** S (copy change)

**Rule:** DECISIONS_OWNER.md O19 (staff password shown once and its delivery method), owner-data.js audit log line 74

---

### R2-OW-CP-006 — Overview queue rows: "كل شيء على ما يرام" is not a queue item
**Type:** improvement | **Level:** component | **Impact:** low  
**Where:** Frame "Overview · nothing needs you — phone 390", `Owner overview.html?demo=clear`, 390×844, light  
**Evidence:** `docs/design/screens/R2-OW-CP-012.png`

**What is wrong:** When nothing needs attention, the "يحتاج انتباهك" section shows a single row "كل شيء على ما يرام" with no action. This is a static sentence, not a queue item. The settled pattern (O3) says the overview is a work queue — empty state should say "لا يوجد ما يحتاج انتباهك" and offer a link to the relevant page.

**Proposal:**
- Replace "كل شيء على ما يرام" with "لا يوجد ما يحتاج انتباهك" (Nothing needs your attention).
- Add a ghost link "عرض النظرة العامة كاملة" or remove the section entirely when empty.

**Why better:** An empty queue should state emptiness clearly, not display a comforting sentence that looks like a row.

**Cost:** S

**Rule:** DECISIONS_OWNER.md O3 (overview is a work queue), REVIEW_LENS.md §3.A.8 (empty state says something useful)

---

### R2-OW-CP-007 — "بلا حالة مباشرة" shown when capacity not set — but the control says "تحديد السعة"
**Type:** defect | **Level:** component | **Impact:** medium  
**Where:** Frame "Overview · no capacity, a group never saved — desktop 1440", `Owner overview.html?demo=missing,nocapacity`, 1440×1000, light  
**Evidence:** `docs/design/screens/R2-OW-CP-008.png`

**What is wrong:** Two different wordings for the same state:
- Top bar status: "يظهر للزوار: بلا حالة مباشرة" (Visitors see: No live status)
- Queue item: "لم تُحدَّد السعة · بدورها لا تظهر حالة مباشرة للزوار · **تحديد السعة**" (Capacity not set · without it no live status for visitors · **Set capacity**)

The status badge says "بلا حالة مباشرة" (no live status) but the action says "تحديد السعة" (set capacity). The user must connect the two.

**Proposal:**
- Status badge: "يظهر للزوار: بلا حالة مباشرة — السعة غير محددة" (Visitors see: No live status — capacity not set).
- Queue action: keep "تحديد السعة" (primary).
- Or unify: status badge "السعة غير محددة" with "تحديد السعة" action.

**Why better:** The status and the action should use the same noun ("السعة") so the user sees the direct link.

**Cost:** S

**Rule:** REVIEW_LENS.md §3.A.3 (hierarchy), O2 (capacity moves to Settings)

---

### R2-OW-CP-008 — Data reports: reporter shown as "زائر" but the open view says "زائر · 29 سبتمبر 2026"
**Type:** defect | **Level:** component | **Impact:** low  
**Where:** Frame "Open report — desktop 1440", `Data reports.html?open=d1`, 1440×1000, light  
**Evidence:** `docs/design/screens/R2-OW-CP-006.png`

**What is wrong:** The open report header shows "زائر · 29 سبتمبر 2026 · جديد" (Visitor · 29 Sept 2026 · New). Per O12, the reporter is anonymous to the owner — "زائر" is correct. But the date format "29 سبتمبر 2026" uses the Arabic month name; the English mirror should show "29 Sept 2026".

**Proposal:** Ensure the date in the report header uses the locale's month format (already done in English mirror check — it shows "29 Sept 2026"). No change needed for Arabic.

**Why better:** Confirms O12 is implemented correctly in Arabic; English mirror is correct.

**Cost:** — (verified, no change)

**Rule:** DECISIONS_OWNER.md O12 (reporter is anonymous to the owner)

---

### R2-OW-CP-009 — Settings attendance: "التقريب لأعلى بعد دقيقة" — "دقيقة" singular for a number input
**Type:** defect | **Level:** component | **Impact:** low  
**Where:** Frame "Owner settings — desktop 1440", `Owner settings.html#attendance`, 1440×1000, light  
**Evidence:** `docs/design/screens/R2-OW-CP-007.png`

**What is wrong:** The rounding select shows:
- "تقريب لأعلى بعد **دقيقة**" (Round up after **minute** — singular)
- Options: "ساعتان و14 دقيقة = ساعتان · ساعتان و16 دقيقة = 3 ساعات"

The label uses singular "دقيقة" but the input accepts a number (minutes). Should be plural "دقائق" or "دقيقة/دقائق" per O5.

**Proposal:**
- Label: "تقريب لأعلى بعد **دقائق**" (Round up after **minutes**).
- Or use the counted form: "بعد {n} دقيقة" with the plural rules.

**Why better:** O5 requires counted nouns through plural forms. A number input's unit label must be plural/generic.

**Cost:** S

**Rule:** DECISIONS_OWNER.md O5 (Arabic plurals through plural forms), REVIEW_LENS.md §3.A.10 (plurals and gender)

---

### R2-OW-CP-010 — Finance tab names: "الدخل / الديون / الإشغال" — "الإشغال" means occupancy, not "reports"
**Type:** improvement | **Level:** page | **Impact:** low  
**Where:** Frame "الدخل — desktop 1440", `Finance.html`, 1440×1000, light  
**Evidence:** `docs/design/screens/R2-OW-CP-010.png` (debts tab), `docs/design/screens/R2-OW-CP-015.png` (audit log)

**What is wrong:** The three tabs are "الدخل" (Income), "الديون" (Debts), "الإشغال" (Occupancy). Glossary: "Occupancy / الإشغال" = "Open check-ins and visits relative to capacity". This tab shows charts of daily subscribers/visits and heatmaps — it *is* occupancy. But the tab label "الإشغال" sits under "المالية والتقارير" (Finance & reports), implying financial reports. The third tab is statistics, not finance.

**Proposal:**
- Rename tab to "الإحصائيات" (Statistics) or "التقارير" (Reports) and move occupancy charts there, OR rename the parent section from "المالية والتقارير" to "المالية والإحصائيات".
- Keep "الإشغال" as a sub-section label inside the statistics tab.

**Why better:** "المالية" = money; "الإشغال" = occupancy. Mixing them under "المالية والتقارير" is a category error.

**Cost:** M (navigation label change across prototype)

**Rule:** glossary "Occupancy / الإشغال", DECISIONS_OWNER.md O15 (Finance's range replaced by one "الشهر" select, the charts' windows named)

---

### R2-OW-CP-011 — Packages: "اسم الباقة" repeated in summary as "باقة بدون اسم"
**Type:** defect | **Level:** component | **Impact:** medium  
**Where:** Frame "New package sheet · live summary — desktop 1440", `Packages.html?sheet=new`, 1440×1000, light  
**Evidence:** `docs/design/screens/R2-OW-CP-011.png`

**What is wrong:** The sheet has a field "اسم الباقة" (Package name). The live summary below shows "الملخّص: باقة بدون اسم" (Summary: Unnamed package). When the user types a name, the summary should update live. The static "باقة بدون اسم" reads as a placeholder, not a live reflection.

**Proposal:**
- Summary line: "الملخّص: **{اسم الباقة أو 'باقة بدون اسم'}**" — update on input.
- If empty, show "باقة بدون اسم" in muted text.

**Why better:** Live summary is a settled pattern (O8: "the space's own shifts; a repeated name on its field"). The name must reflect instantly.

**Cost:** S (prototype JS wiring)

**Rule:** DECISIONS_OWNER.md O8 (package sheet: repeated name on its field)

---

### R2-OW-CP-012 — Announcements active tab: "إنهاء الآن" vs "تمديد الاشتراكات" — verb inconsistency
**Type:** improvement | **Level:** pattern | **Impact:** medium  
**Where:** Frame "Active · owner — desktop 1440", `Announcements.html`, 1440×1000, light  
**Evidence:** `docs/design/screens/R2-OW-CP-014.png`

**What is wrong:** 
- Active announcements (event, offer): action button "إنهاء الآن" (End now) — imperative verb.
- Ended closures (a6): action button "تمديد الاشتراكات" (Extend subscriptions) — masdar/noun phrase.
- O10 says "an announcement can end now" — the action is "إنهاء الآن".
- O11 says "the closure extension is its own action" — the action is "تمديد".

The verb forms differ: imperative verb vs. masdar. P9/O4 says destructive actions repeat the verb. "إنهاء" is the verb; "تمديد" is the masdar. For consistency, both should be imperative: "أنهِ الآن" / "مدّد الاشتراكات" — or both masdar: "إنهاء الآن" / "تمديد الاشتراكات".

**Proposal:** Use imperative for both destructive actions per P9:
- "أنهِ الآن" (End now — imperative)
- "مدّد الاشتراكات" (Extend subscriptions — imperative)

**Why better:** P9: "action variant='destructive' repeating the verb". Imperative is the verb form for actions.

**Cost:** S (copy change)

**Rule:** DECISIONS_SHARED.md P9 (destructive action repeats the verb), DECISIONS_OWNER.md O10/O11

---

### R2-OW-CP-013 — Space profile prices link says "الباقات والأسعار" but the page is "Packages & prices"
**Type:** defect | **Level:** component | **Impact:** low  
**Where:** Frame "Space profile · link to prices — desktop 1440", `Owner space profile.html#prices`, 1440×1000, light  
**Evidence:** `docs/design/screens/R2-OW-CP-013.png`

**What is wrong:** Space profile shows "الأسعار · تُعدَّل وتُؤكَّد في **الباقات والأسعار** · آخر تحديث قبل 34 يومًا · قديمة · **الباقات والأسعار**" (link). The page title is "الباقات والأسعار". English mirror: "Published prices · Shown on the space page · Display only · Pay at the space · Updated 34 days ago · Out of date · **Packages & prices**". The Arabic link text matches the page title — correct. But the English page title is "Packages & prices" while the link says "Packages & prices" — correct. No issue in Arabic.

**Wait** — the English mirror of Space profile shows "Prices · Edited and confirmed in **Packages & prices** · Updated 34 days ago · Out of date · **Packages & prices**" — this is consistent.

**Proposal:** No change needed. Verified consistent.

**Cost:** —

**Rule:** DECISIONS_OWNER.md O6 (prices' home is Packages & prices)

---

### R2-OW-CP-014 — Overview "الحاضرون الآن 27 / 40" — "40" is capacity but capacity is private per glossary
**Type:** defect | **Level:** component | **Impact:** medium  
**Where:** Frame "Overview — desktop 1440", `Owner overview.html`, 1440×1000, light  
**Evidence:** `docs/design/screens/R2-OW-CP-003.png`

**What is wrong:** The overview shows "الحاضرون الآن 27 / 40" (Present now 27 / 40). Glossary: "Capacity / السعة" = "Private from the public: only the space's staff (owner and reception) see it". The owner *is* staff, so seeing capacity is allowed. But the format "27 / 40" implies a fraction shown to the owner — this is correct for staff. However, the public state badge says "يظهر للزوار: متاح" (Visitors see: Available) — visitors never see the number. This is correct.

**Proposal:** Keep as is. The owner sees capacity; visitors don't. The format "27 / 40" is clear for staff.

**Cost:** — (verified correct)

**Rule:** glossary "Capacity / السعة", "Live status / الحالة المباشرة"

---

### R2-OW-CP-015 — Audit log: "الوقت / المنفّذ / الإجراء / الهدف / التفاصيل" — "المنفّذ" shows "النظام" for auto check-out
**Type:** improvement | **Level:** component | **Impact:** low  
**Where:** Frame "Audit log · the space's — desktop 1440", `Owner audit.html`, 1440×1000, light  
**Evidence:** `docs/design/screens/R2-OW-CP-015.png`

**What is wrong:** The "المنفّذ" (Actor) column shows "النظام" (The system) for automatic check-outs. This is correct per owner-data.js line 73 ("النظام"). But the English mirror shows "The system" — consistent. No issue.

**Proposal:** No change.

**Cost:** —

**Rule:** DECISIONS_OWNER.md O13 (audit log scoped to the space)

---

### R2-OW-CP-016 — Announcements new sheet: type "إغلاق مؤقت" preview shows "مغلق الآن" but the type label is "إغلاق مؤقت"
**Type:** defect | **Level:** component | **Impact:** low  
**Where:** Frame "New announcement · the model's fields — phone 390", `Announcements.html?sheet=new&type=closure`, 390×844, light  
**Evidence:** (captured in review, see text from earlier navigation)

**What is wrong:** When creating a closure announcement, the type selector shows "إغلاق مؤقت" (Temporary closure). The preview shows "Focus Hub / مغلق الآن" (Closed now). The public state during the closure is "مغلق الآن" (Closed now) — but the announcement type is "إغلاق مؤقت". The preview should clarify: "خلال الفترة ستظهر المساحة بـ «مغلق الآن»" (During the period the space will show as «Closed now»).

**Proposal:** Preview text: add a line "خلال الفترة ستظهر الحالة للزوار: **مغلق الآن**".

**Why better:** The owner must understand that "إغلاق مؤقت" → public state "مغلق الآن". The current preview shows "مغلق الآن" without explanation.

**Cost:** S

**Rule:** DECISIONS_OWNER.md O10 (closure's line saying the space shows «مغلق الآن»)

---

### R2-OW-CP-017 — "مؤرشف / محذوف / مخفية" not confused — verified
**Type:** — | **Level:** — | **Impact:** —  
**Where:** All pages reviewed  
**Evidence:** N/A

**What is wrong:** The prompt asks to check "مؤرشف/محذوف/مخفية nowhere confused". In the owner's pages:
- Announcements tabs: "نشطة / مجدولة / منتهية" (Active / Scheduled / Ended) — no "مؤرشف".
- Staff: "نشط / بلا وصول" (Active / No access) — no "محذوف".
- Packages: "موقوفة" (Paused) for private packages — not "مؤرشف".
- Spaces (admin): "محذوفة" (soft-deleted) with "استرجاع" — separate from owner's view.

**Proposal:** No confusion found. Terms are distinct.

**Cost:** —

**Rule:** REVIEW_LENS.md §3.A.3 (same thing named two ways)

---

### R2-OW-CP-018 — "اليوم: 34 · الآن: 19 مشتركًا و8 زيارات" — "34" and "19/8" need clarification
**Type:** improvement | **Level:** component | **Impact:** low  
**Where:** Frame "Overview — desktop 1440", `Owner overview.html`, 1440×1000, light  
**Evidence:** `docs/design/screens/R2-OW-CP-003.png`

**What is wrong:** The line "اليوم: 34 · الآن: 19 مشتركًا و8 زيارات" (Today: 34 · Now: 19 subscribers and 8 visits). "34" likely = total check-ins today (19 subscribers + 8 visits = 27 present now + 7 checked out?). But "34" ≠ 27. The numbers don't add up visibly.

**Proposal:** Add a tooltip or expand: "اليوم: 34 تسجيل حضور (19 مشتركًا + 8 زيارات + 7 خرجوا)" — or change to "إجمالي اليوم: 34 · الحاضرون الآن: 27 (19 مشتركًا، 8 زيارات)".

**Why better:** The two numbers (34 and 27/19/8) must relate obviously.

**Cost:** S

**Rule:** REVIEW_LENS.md §3.A.6 (numbers and dates)

---

### R2-OW-CP-019 — English mirror of Settings: reminder message preview shows Arabic placeholders
**Type:** defect | **Level:** page | **Impact:** medium  
**Where:** Frame "Owner settings — desktop 1440", `Owner settings.html?lang=en`, 1440×1000, light  
**Evidence:** (captured in review — English Settings page shows Arabic in preview)

**What is wrong:** The reminder message preview shows:
```
مرحبًا Rahaf، تذكير من Focus Hub: عليك ₪150. يمكنك الدفع في المساحة. شكرًا.
```
The placeholders `{الاسم}`, `{المبلغ}`, `{المساحة}` are Arabic in the "Insert" list, and the preview mixes Arabic/English.

**Proposal:**
- English mirror: placeholders → `{name}`, `{amount}`, `{space}`.
- Preview: "Hello Rahaf, reminder from Focus Hub: you owe ₪150. You can pay at the space. Thanks."

**Why better:** English page must be fully English.

**Cost:** S

**Rule:** REVIEW_LENS.md §3.A.7 (English mirror: same meaning, no leftover Arabic)

---

### R2-OW-CP-020 — Packages published prices: "للعرض فقط · الدفع في المساحة" — "عرض" vs "دفع" mismatch
**Type:** improvement | **Level:** component | **Impact:** low  
**Where:** Frame "Packages & prices — desktop 1440", `Packages.html`, 1440×1000, light  
**Evidence:** (captured in review)

**What is wrong:** The published prices section header says: "تظهر في صفحة المساحة · **للعرض فقط** · **الدفع في المساحة**". "للعرض فقط" (for display only) and "الدفع في المساحة" (pay at the space) — one says "display", the other says "pay". The glossary: "Payment / دفعة" = "Money received... recorded by hand (cash or transfer)". The prices are *published* (displayed), payments are *collected* at the space.

**Proposal:** Change to: "تظهر في صفحة المساحة · **أسعار معلنة** · **التحصيل في المساحة**" (Shown on space page · Published prices · Collection at the space). Or keep "للعرض فقط" but change "الدفع" to "السداد" (settlement) to distinguish from "دفعة" (payment record).

**Why better:** "الدفع" implies the payment action; "التحصيل" or "السداد" is the collection event. The glossary distinguishes "Payment / دفعة" (the recorded event) from prices.

**Cost:** S

**Rule:** glossary "Payment / دفعة", "Package / باقة"

---

### R2-OW-CP-021 — Overview "إغلاق لم تُمدَّد اشتراكاته" — passive participle, should be actionable
**Type:** improvement | **Level:** component | **Impact:** medium  
**Where:** Frame "Overview — desktop 1440", `Owner overview.html`, 1440×1000, light  
**Evidence:** `docs/design/screens/R2-OW-CP-003.png`

**What is wrong:** The queue item says: "إغلاق لم تُمدَّد اشتراكاته · 24 سبتمبر 08:00 – 25 سبتمبر 18:00 · مراجعة" (Closure whose subscriptions were not extended · 24 Sept 08:00 – 25 Sept 18:00 · Review). "لم تُمدَّد" is passive. The action is "مراجعة" (Review) which opens the ended tab. Better: "إغلاق ينتظر تمديد الاشتراكات" (Closure awaiting subscription extension) with action "تمديد" (Extend).

**Proposal:**
- Text: "إغلاق ينتظر تمديد الاشتراكات" (Closure awaiting subscription extension).
- Action button: "تمديد" (Extend) — opens `Announcements.html?tab=ended&extend=a6`.

**Why better:** Active voice + direct action verb. Matches O11 "closure extension is its own action".

**Cost:** S

**Rule:** REVIEW_LENS.md §3.A.10 (label says what happens), DECISIONS_OWNER.md O11

---

### R2-OW-CP-022 — Finance debts: "مجموع الديون 293 ₪ · 5 زبائن" — "زبائن" plural correct for 5, but "أرصدة للزبائن 18 ₪ · زبون واحد" — "زبون" singular correct
**Type:** — | **Level:** — | **Impact:** —  
**Where:** Frame "الدخل — desktop 1440", `Finance.html?tab=debts`, 1440×1000, light  
**Evidence:** `docs/design/screens/R2-OW-CP-010.png`

**What is wrong:** Verified plurals:
- "5 زبائن" (5 customers) — correct (3–10 → plural).
- "زبون واحد" (one customer) — correct (singular).
- "45 زبونًا" (45 customers) — correct (11–99 → plural with alif).
- "لهم رصيد" (they have credit) — plural pronoun correct.

**Proposal:** No change. O5 plurals working correctly.

**Cost:** —

**Rule:** DECISIONS_OWNER.md O5 (Arabic plurals through plural forms)

---

### R2-OW-CP-023 — Payments void dialog: "تبقى ظاهرة مشطوبة مع السبب واسمك" — "مشطوبة" (struck through) is visual, not semantic
**Type:** improvement | **Level:** component | **Impact:** low  
**Where:** Frame "Void a payment · reason required — desktop 1440", `Payments.html?void=1`, 1440×1000, light  
**Evidence:** `docs/design/screens/R2-OW-CP-004.png`

**What is wrong:** Dialog body: "تبقى ظاهرة مشطوبة مع السبب واسمك، ولا تُحسب في الدخل ولا في التسليم" (Remains visible struck through with reason and your name, and not counted in income nor in handover). "مشطوبة" describes the visual style (strikethrough). The semantic state is "ملغاة" (voided).

**Proposal:** "تبقى ظاهرة كـ **ملغاة** مع السبب واسمك، ولا تُحسب في الدخل ولا في التسليم" (Remains visible as **voided** with reason and your name...).

**Why better:** Uses the glossary term "إلغاء دفعة" → "ملغاة". Visual description ("مشطوبة") belongs in VD, not copy.

**Cost:** S

**Rule:** glossary "Void a payment / إلغاء دفعة"

---

### R2-OW-CP-024 — Announcements ended tab: "مُدِّد 19 اشتراكًا 3 أيام" — "مُدِّد" is passive participle, should be active
**Type:** improvement | **Level:** component | **Impact:** low  
**Where:** Frame "Ended · one closure extended, one to extend — desktop 1440", `Announcements.html?tab=ended`, 1440×1000, light  
**Evidence:** `docs/design/screens/R2-OW-CP-009.png`

**What is wrong:** The ended closure a4 shows "مُدِّد 19 اشتراكًا 3 أيام · أحمد · 17 سبتمبر 2026" (Extended 19 subscriptions 3 days · Ahmed · 17 Sept 2026). "مُدِّد" is the passive participle (was extended). The actor is "أحمد" — so active "مدّد أحمد 19 اشتراكًا 3 أيام" (Ahmed extended 19 subscriptions 3 days) is clearer.

**Proposal:** "مدّد أحمد 19 اشتراكًا 3 أيام · 17 سبتمبر 2026" (Ahmed extended 19 subscriptions 3 days · 17 Sept 2026).

**Why better:** Active voice names the actor; matches audit log "subscriptions_extended" by AH.

**Cost:** S

**Rule:** REVIEW_LENS.md §3.A.10 (active voice for actions)

---

### R2-OW-CP-025 — Staff list: "مقبوضاته هذا الشهر" — "مقبوضات" (collections) vs glossary "Payment / دفعة"
**Type:** defect | **Level:** component | **Impact:** low  
**Where:** Frame "Staff list — desktop 1440", `Staff.html`, 1440×1000, light  
**Evidence:** (captured in review)

**What is wrong:** Staff table column: "مقبوضاته هذا الشهر" (His collections this month). Glossary: "Payment / دفعة" = recorded money. "مقبوضات" is a valid synonym for "collections" but the glossary uses "دفعة" / "دفعات". The column shows amounts (1380 ₪, 0 ₪) — these are payments collected by that receptionist.

**Proposal:** Change header to "دفعاته هذا الشهر" (His payments this month) to match glossary "دفعة". Or keep "مقبوضاته" but add tooltip "دفعات تم تحصيلها".

**Why better:** Consistency with glossary term "دفعة".

**Cost:** S

**Rule:** glossary "Payment / دفعة"

---

## 5. Decisions in doubt
None. All settled decisions (DECISIONS_SHARED.md, DECISIONS_OWNER.md) are applied correctly or reported as misapplications above.

## 6. What was not reviewed and why
- **Dark mode**: Prompt says "light is enough unless a string differs in dark". No string differences found in light mode review.
- **768px viewport**: Prompt requires 390, 1440, and English 1440 (390 for dialogs). 768px is a DF/VD concern (layout breakage), not CP.
- **Front desk (Desk.html) pages**: Out of scope (Batch 6).
- **Admin pages**: Out of scope (Batch 4).
- **Public site pages**: Out of scope (Batch 3).
- **Authentication flow**: Out of scope (Batch 4).
- **API contract compliance**: TR axis, not CP.
- **Visual design (spacing, alignment, type)**: VD axis, not CP.
- **Accessibility (focus, contrast, names)**: AX axis, not CP.
- **Flow/steps (UX)**: UX axis, not CP.

---

*End of report*