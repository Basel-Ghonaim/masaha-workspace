# Design decisions — batch 5, the owner's management (approved by the owner, 2026-10-11)

> **Decided 2026-10-13** by the owner: **DI-10, the phone's top bar:** the account avatar leaves the
> bar on a phone and heads the drawer (which already holds the theme and the language); the bar keeps
> the menu button, the title (truncated if it must), P2's state control and P1's «⋯». **A package's
> price is above zero**, as a space's prices are (a free event is an announcement); the database's
> rule follows with the desk's steps. **While worker A builds the admin's editor (S2b-4), this batch
> changes nothing in the shared editor that the admin's editor shows:** the owner's differences are
> the owner's page's only; a defect in the shared editor is recorded, not built.

> **Added 2026-10-11** (from fix 1, DI-10): the phone top bar is full; its precedence (title, P1's «⋯», P2's state control, the account) is settled **with this batch**, before anything more is added to it.
>
> **Amended 2026-10-12** by the owner (O3): **no money on the overview.** Income (today, this month,
> since the start) and the debts' total are sensitive and the overview is often open at the desk, in
> view of customers and staff; they live in «المالية والتقارير» only. The overview keeps its work
> queue as counts and links, no amounts («3 زيارات لم تُحصَّل» → the desk; «عملاء عليهم ديون» → Finance
> › الديون). **Rule to change:** foundation §13, screen 12 (Overview, O) drops "income today and this
> month, total debt" (with worker A's design-system item). **Deferred, not v1:** a code the owner
> enters to open Finance and reports.

From `REPORT\REVIEW_OWNER_REPORT.md` (OW-001 … OW-022). **Settled**, as the report proposes unless
said otherwise. Where each is done: **prototype**, **design system** (worker A), **API** (worker B),
**docs**.

## Decisions
- **O1 — one space editor, two permissions** (OW-001): the owner's Space profile *is* the A1 editor
  (five groups, gallery, chips, «لم تُضف بعد», the A2 checklist), differing only as the report's table
  says (head line, prices as a link row to Packages & prices, photos, no capacity, no hide/delete).
  *(prototype; web in step 5)*
- **O2 — capacity and the stay limit move to Settings** (OW-002, OW-021): one card «الحضور والحالة
  المباشرة» (capacity, auto check-out at closing, auto check-out after N hours); the profile keeps
  only what visitors see. *(prototype)*
- **O3 — the overview is a work queue** (OW-003): «يحتاج انتباهك» first (missing or stale groups,
  new reports, uncollected visits, a started closure without its extension, capacity not set), then
  money and «الحاضرون الآن», then the ending subscriptions; confirm only beside what it confirms;
  **no bottom bar on the overview** (P1 amended). *(prototype)*
- **O4 — the owner's actions classified** (OW-004): the report's table applies P9 and A5 (the staff
  password dialog under A5's rules, the extension destructive, deactivating staff with its true
  consequence). *(prototype)*
- **O5 — Arabic plurals** (OW-005): every counted noun through the plural forms («ينتهي غدًا»,
  «بعد يومين», «زيارة واحدة»); counts in tabs as `Badge`s. *(prototype; web: the copy catalogue's
  plurals)*
- **O6 — prices' home is Packages & prices** (OW-006, OW-008): the AD-008 table with its own date and
  confirm there; every «تعديل الأسعار» link goes to it; «الفترة» and «لمن: الجميع · الطلاب»; the
  private packages a list of rows. *(prototype)*
- **O7 — photos are immediate actions** (OW-007): upload on choose, per-tile progress and failure
  (413, 415) with retry, removal by `AlertDialog`, reorder and cover at once, no save, no date.
  *(prototype)*
- **O8 — the package sheet** (OW-009): validity required; limits on demand (a `ToggleGroup` of four);
  days a week 1–7; billing one choice «سعر ثابت · بالساعة · باليوم» with its labelled amount; the
  space's own shifts; a repeated name on its field. *(prototype)*
- **O9 — announcements follow the model** (OW-011): Arabic text (required) and English text
  (optional), the type and the period; **no title and no «أنشأه»; no schema change.** *(prototype)*
- **O10 — an announcement can end now, be deleted, start now, or have no end** (OW-012), the
  closure's line saying the space shows «مغلق الآن». *(prototype)*
- **O11 — the closure extension is its own action, once the closure has started** (OW-013): an
  `AlertDialog`, destructive, naming how many active subscriptions move and by how many days.
  *(prototype)*
- **O12 — the reporter is anonymous to the owner** (OW-020): the owner sees «زائر» and the date; the
  admin keeps the name. *(prototype; API: the owner's reports read; docs: `features/` when built)*
- **O13 — the owner's audit log** (OW-022): «سجل التدقيق» in P3's «الفريق والإعدادات» group, the
  admin's audit page (AD-028) scoped to the space. *(prototype)*
- **Smaller (as proposed):** OW-014 type badges `neutral` (`warning` for outage and closure), the type
  a `RadioGroup` with hints; OW-015 Finance's range replaced by one «الشهر» select, the charts' windows
  named, «تصدير الدخل (CSV)»; OW-016 the finance lists page or link «عرض الكل»; OW-017 «إيقاف وصوله»
  with its true consequence (re-access through the same `PATCH`); OW-018 real staff columns (no last
  sign-in) and a «لم يغيّر كلمة المرور المؤقتة بعد» badge; OW-019 adding staff in one submit, both
  outcomes said first; OW-021 the rounding minutes settable, student visit prices on by default.
  *(prototype; API: OW-017's re-access)*

## Design system
- **OW-010 (with DK-024):** `Sheet side="end"` full width below `md`, its body `min-w-0`.
  *(design system)*

## Rules changed
- **api-contract §4:** a space's packages answered whole (the desk's picker needs them). *(docs)*
- **overview.md › Dashboard:** the space profile's names follow the data model (English required,
  Arabic optional). *(docs)*
- **glossary *Package* / foundation §13 #21:** "the published week and month prices also serve as
  packages at the desk; private packages are never shown publicly". *(docs)*
