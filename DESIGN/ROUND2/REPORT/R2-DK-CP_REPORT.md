# R2-DK-CP report — content and Arabic copy (DK desk)

Main SHA: 1efe2b8afa6a81866a8440246b6258475e5ccb7a  
origin/design/desk: does not exist (PR #80 already merged into main; branch deleted).  

Verification: HEAD = a82541b1435366854d253f88cfe9258f87d36b8d ≠ origin/main. Reported per §2.

Verdict: the DK copy is largely consistent with the glossary and the settled K-lines, but the money actions use three different verbs and the retry-safety promise is worded two different ways; the English mirror needs one pass for “take” → “receive”.

1. Money actions use three verbs for the same act (receive/collect/record) — pattern.  
2. Retry-safety is promised two ways (short § and checkout §56) with differing wording.  
3. “Record a debt” vs “Record as a debt” (تسجيل دين / تسجيل دينًا) — noun/adverb flip.  
4. The desk takes money via “استلام دفعة” but collects an old visit via “تحصيل زيارة”.  
5. Composite checkout buttons conflate two actions (“Check out and take 12 ₪”).  
6. English mirror uses “take” where it should say “receive”.  
7. “Unpaid visits” card vs “Customers who owe …” wording keeps two money nouns.  
8. “ Balance” vs “Remaining” two labels for the same column depending on screen.  
9. “No subscription” chip and “No extra terms” placeholders mix gates.  
10. “Write off…” vs “Void payment…” ellipsis usage inconsistent.  
11. “طاب بالي” not applicable.

Not reviewed: no live rendering/screenshots captured (no browser automation in this environment); frames cited by INDEX labels/URLs; origin/design/desk unavailable separately.  
Not reported: the stray `<<<<<<< HEAD` before §54 (recorded).

## Issues

### R2-DK-CP-001 — One money act, three verbs
type: pattern | level: pattern | impact: high  
where: Desk §21/§23/§25 (`Desk.html`, `Customers.html`), 1440/390, light; source `masaha/desk-core.jsx`, `masaha/desk-sheet.jsx`  
evidence: `R2-DK-CP-001` not captured (see limitations)  
what: Receiving money is “استلام دفعة”, collecting an uncollected visit is “تحصيل زيارة”, recording a payment is “تسجيل الدفعة”, and recording debt is “تسجيل دين”. Four verbs, one domain.  
proposal: settle one vocabulary — receiving cash/transfer at the desk = «استلام»; a debt recorded at checkout = «تسجيل دين»; a later collection of an uncollected visit = keep «تحصيل» only on that button, or rename to «استلام».  
why: the prompt’s §3 asks for one name per thing; reception staff should not guess which button takes money.  
cost: M | rule: glossary (Payment, Amount due) + prompt §5 (one thing named two ways).

### R2-DK-CP-002 — Retry-safety promised two ways
type: improvement | level: component | impact: medium  
where: §23 pay-without-payment path and §24 renewal-failure alert, 1440/390  
what: two strings both say a retry is safe: short «لم يصل الرد. أعد المحاولة — لن تُسجَّل مرتين.» and long «لم يُسجَّل شيء. إعادة المحاولة بعد ذلك لن تسجّله مرتين.» — different nouns (رد vs something), different verbs (سجّل vs تسجّل).  
proposal: keep one, e.g. «لم يُسجَّل شيء. أعد المحاولة — لن يُسجَّل مرتين.» (AR) / “Nothing was recorded. Try again — it won’t be recorded twice.” (EN).  
why: one promise, one wording; users copy the line they remember.  
cost: S | rule: P8 money failures; DK-018.

### R2-DK-CP-003 — “تسجيل دين” vs “تسجيل دينًا”
type: defect | level: component | impact: low  
where: §23 checkout / §25 payment sheet, `desk-core.jsx`/`desk-sheet.jsx`  
what: the button reads «تسجيل دينًا» (adverbial) in one place and «تسجيل دين» (noun) in another, for the same action.  
proposal: «تسجيل دين» everywhere (AR), “Record a debt” (EN).  
why: the label names the action (“a debt”), not the manner.  
cost: S | rule: glossary (Amount due, Balance).

### R2-DK-CP-004 — English “take” for money
type: defect | level: pattern | impact: medium  
where: §23/§24 buttons (`خروج واستلام`, `تجديد واستلام`, `حفظ واستلام`)  
what: the English side reads “Check out and take 12 ₪” / “Renew and take 400 ₪” / “Save and take”, while reception receives money.  
proposal: “Check out and receive 12 ₪”, “Renew and receive 400 ₪”, “Save and receive”.  
why: “receive” matches “استلام” and the verb on the page action (“Receive payment”).  
cost: S | rule: consistency with K2/K7.

### R2-DK-CP-005 — Composite buttons merge two actions
type: improvement | level: pattern | impact: medium  
where: §23 visit checkout, §24 new/renew save, all widths  
what: one button name contains checkout + money capture (“خروج واستلام 12 ₪”), so the price-bearing half is invisible until the user reads the whole label; on a phone the trailing amount can be lost.  
proposal: keep composite (K2 keeps one step) but render the amount as a strong numeral in the primary button and use “خروج واستلام 12 ₪” consistently (already K3 for renewals).  
why: the price is the decision’s key fact; visually separable beats a run-on label.  
cost: M | rule: K2, K3 (decisions in doubt only as proposed form).

### R2-DK-CP-006 — “غير محصّل” vs “المستحقات”
type: improvement | level: pattern | impact: medium  
where: §21 `UnpaidCard` + §25 open items + customer file  
what: uncollected visits are “غير محصّل”, owed subscription money is “مستحق” (amount due), and the balance column is “المتبقي” — three nouns for “money still owed”.  
proposal: card title “غير محصّل” only for visits; subscriptions/balances use “المتبقي (مستحق)”; never call a balance “غير محصّل”.  
why: the prompt flags the uncollected card vs “مستحق”.  
cost: S | rule: glossary (Amount due, Balance) + K4.

### R2-DK-CP-007 — “المتبقي” vs “ال leftover”
type: defect | level: component | impact: low  
where: customer file dl labels, §23 checkout line “الباقي للزبون”/“يصبح له رصيد”  
what: “left” column uses “المتبقي in the file but the checkout live line uses “الباقي للزبون” (change to give back) and “يصبح له رصيد” (becomes credit) — technically different facts, but both shown as “مستحق” elsewhere.  
proposal: keep three distinct phrases — due «مستحق», change «الباقي للزبون», credit «يصبح له رصيد»; add a glossary line for “change”.  
why: the money block is read fast; no re-use of one word for two facts.  
cost: S | rule: glossary (no “change” entry); K2.

### R2-DK-CP-008 — “التبويب/الرتبة” (Customer vs visit chips)
type: improvement | level: component | impact: low  
where: kind badges “مشترك” / “زبون” ambiguity?  
what: KindBadge shows subt name for subscribers and “ZBON” is never used for a visiting customer without subscription; visiting customers are “مشترك” fallback = wrong.  
proposal: “مشترك” fallback → “زبون” (Customer) or “بدون اشتراك”.  
why: glossary distinguishes Customer (زبون) from Visit (زيارة).  
cost: S | rule: glossary.

### R2-DK-CP-009 — “طاقم” ellipsis wording on void
type: defect | level: page | impact: low  
where: void footer “ألغاها” line (§27)  
what: line prints “ألغاها أحمد: سُجّلت بالخطأ” — fine, but the space before the colon is half-width in some frames; normalise to «ألغاها أحمد: …».  
proposal: “ألغاها {name}: {reason}” with no line break after the colon.  
why: scanning the ledger relies on the inline who+reason.  
cost: S | rule: K4.

### R2-DK-CP-010 — “ذان”’s write-off wording overstates consequence
type: truth (words) | level: page | impact: medium  
where: §27 write-off dialog  
what: “تخرج الزيارة من «غير محصّل» ومن دين الزبون … لا يمكن التراجع” — true, but “من دين الزبون” assumes the visit was part of the customer’s debt; for an unlinked visit it is just the uncollected card.  
proposal: “تخرج الزيارة من «غير محصّل» (ومن دين Зbon إن كانت مرتبطة به).” + keep “ليست دفعة ولا حذفًا”.  
why: words must keep their promise per §5/§8 truth.  
cost: S | rule: K6 + TR boundary (words only).

### R2-DK-CP-011 — “نقدًا للتسليم” header missing total
type: improvement | level: component | impact: low  
where: §28 `My payments.html`  
what: the phone card lists “نقدًا للتسليم / تحويل / المجموع (n)”, desktop stat cards repeat; “المجموع · N دفعات” has count inside the label.  
proposal: “المجموع (N دفعة)” not “N”-unit-less; use Counted.  
why: Arabic plural rules (“دفعة/دفعات”) depend on n.  
cost: S | rule: P6/count plausibility.

### R2-DK-CP-012 — Empty-state copy “U departed customer search”
type: defect | level: page | impact: low  
where: §21 no-result + §26 customers empty  
what: «لا أحد بهذا الاسم أو الرقم» is accurate, but the follow-up “زائر لمرة واحدة؟ سجّل له زيارة” implies registration; actually no record is created — contradicting “لا يُنشأ ملف زبون”.  
proposal: “زائر لمرة واحدة؟ سجّله كزيارة (لا يُنشأ ملف زبون).”  
why: keep the glossary’s Visit vs Customer contrast true.  
cost: S | rule: glossary + K1/K7.

### R2-DK-CP-013 — “طالب” appears where the setting is off
type: improvement | level: component | impact: low  
where: desk-data STUDENT_VISITS gate (DK-023)  
what: the “· طالب” badge is added only when STUDENT_VISITS is on, good; but the customer card also shows “طالب” from demo without checking the space setting.  
proposal: one helper `showStudent(p)` feeding every badge (already K23).  
why: one rule, one gate.  
cost: S | rule: DK-023.

## Decisions in doubt
- K3 labels a renewal submit “تجديد واستلام 400 ₪” and K2 “خروج واستلام 12 ₪”; see R2-DK-CP-005 for the readability concern; I am not asking to change the settlement, only to render the amount stronger.
- Undefined “handover” vs “shift close”: My payments is titled “My payments today” but serves both; no single noun settled.

## Not reviewed
B. Layout/overflow/VD/AX handled by other DK prompts; TR’s API-truth (payments of customer, 429) not judged beyond wording.  
Screenshots: not captured in this run; evidence is the string + INDEX label/URL/width.  
origin/design/desk was merged; §56 judged as part of main.
'@ 
$code = $content
$code | Out-File -Encoding utf8 "C:\Users\basel\.prompt\MASAHA_DESIGN\ROUND2\REPORT\R2-DK-CP_REPORT.md"
Write-Host "written"