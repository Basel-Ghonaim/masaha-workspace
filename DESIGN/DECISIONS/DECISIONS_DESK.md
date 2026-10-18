# Design decisions — batch 6, the front desk (approved by the owner, 2026-10-11)

From `REPORT\REVIEW_DESK_REPORT.md` (DK-001 … DK-024, patterns §2.1–§2.5). **Settled**, as the report
proposes unless said otherwise. Where each is done: **prototype**, **design system** (worker A),
**API** (worker B, steps 7–9), **docs**.

## Decisions
- **K1 — one desk search** (§2.1, DK-001, DK-002): present people first (with «خروج»), then
  customers (with «حضور»), then «تسجيل زيارة باسم «X»» (primary when nothing matches) and «زبون جديد
  باسم «X»», the typed name carried into the dialog; the present list keeps no second search.
  *(prototype)*
- **K2 — one money block** (§2.2, DK-004, DK-006): «المستحق», «المستلم الآن» filled with what is due,
  «الطريقة», a live line (the debt that remains — phone required — or the change to give back), the
  submit naming the amount, and «لم يدفع شيئًا»; one step for a new customer's sheet. *(prototype)*
- **K3 — a renewal with a debt is paid oldest first** (DK-005): the block filled with the old balance
  plus the new price, one payment per item, the Alert a warning only, «تجديد واستلام 400 ₪».
  *(prototype; API: step 8)*
- **K4 — no hidden money** (DK-011, DK-015, §2.3): the customer file lists unpaid visits and their
  payments through the visit's customer; «دفعاتي اليوم» shows a voided payment struck through with
  who and why, excluded from the cards; the toasts name amount, item and method. *(prototype)*
- **K5 — the weekday warning uses the count** (DK-009): «استنفد أيامه هذا الأسبوع · 3 من 3»; no
  weekdays in the model. *(prototype)*
- **K6 — an uncollected visit can be written off** (rule in doubt 2): an owner-only «لن يُحصَّل» with
  a required reason, recorded and audited, removing the visit from the uncollected list and the debt;
  never a payment, never a deletion. *(prototype; API and data model: step 7)*
- **K7 — the desk keeps its success toasts** (§2.5): P8's row exception does not apply at the desk
  (the changed row is often off screen on a phone): check-in and check-out keep a toast, and every
  money action one with its amount. *(prototype)*
- **K8 — «الحاضرون الآن» is answered whole** (DK-019): one composed read bounded by the people present
  (kind, name, since, today's usage, the visit's charge so far), an exception in api-contract §4; the
  log a paged read by day. *(API: step 7; docs)*
- **Smaller (as proposed):** DK-003 the phone order search → uncollected → present (once with its
  tabs); DK-007 a renewal shows the current package in one line; DK-008 a custom subscription states
  its real terms; DK-010 a fixed-price subscriber checks out in one tap; DK-012 an uncollected visit
  without a customer collects on the visit item; DK-013 customer actions by state (§2.4); DK-014
  editing a customer, «مؤرشف» in the filter with «استرجاع», a settled customer archived at once with
  undo and an owing one through an `AlertDialog`; DK-016 the void inside the row's «⋯»; DK-017 five
  columns at 768 for Customers and Payments; DK-018 money failures say a retry is safe, or what was
  saved; DK-020 «تسجيل كزيارة» as the customer; DK-021 the rounding line from the settings; DK-022 one
  place for «بدون اشتراك», status chips; DK-023 «طالب» and «الوردية» only when the space uses them.
  *(prototype; API: DK-018's keys, step 8)*

## Design system
- **DK-024 (with OW-010):** `Sheet side="end"` full width below `md`. *(design system)*

## Rules changed
- **api-contract §4:** «الحاضرون الآن» answered whole (K8); a space's packages answered whole (O-batch).
  *(docs)*
- **ADR 0009's table:** editing a customer, both roles; archiving and restoring, the owner. *(docs —
  a *Revised* line)*
- **data-model:** an uncollected visit's write-off (K6). *(docs, with step 7)*
