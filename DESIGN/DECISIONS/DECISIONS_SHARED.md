# Design decisions — batch 1, the shared layer (approved by the owner, 2026-10-10)

From `REPORT\REVIEW_SHARED_REPORT.md` (issues SH-001 … SH-022). **Settled:** later reviews build on
them and do not report them again; the fixer applies them. Each says where it is done:
**prototype** (the design fixer, in `docs/design/prototype/`), **design system** (worker A, in
`apps/web/src/shared/design-system/`, shown at `/__showcase`), **docs** (the owning document).

> **Amended 2026-10-10** by the owner, after reviews 2 and 3 (`DECISIONS_ADMIN.md`,
> `DECISIONS_PUBLIC.md`): **P1** — the phone's bottom bar is only for the action that is the page's
> purpose and used all day (the desk's «تسجيل زيارة»); a list's "add" sits in a row above the list,
> at its end, at every width; secondary actions in the top bar's «⋯». **P5** — the Directory keeps its
> filter sidebar from `lg` and the sheet below it, taking the rest of P5. **P8** — an action whose
> result shows in the row it changed raises no success toast; only its failure is announced.
>
> **Amended 2026-10-11**, after reviews 4–6: **P1** — the owner's overview has **no** bottom bar
> (the desk is in the navigation; O3). **P8** — the exception does **not** apply at the front desk:
> check-in and check-out keep their success toast, and every money action one with its amount (K7).
> **P9** — archiving a customer is two cases: a settled customer is archived at once with «تراجع»; a
> customer who owes gets an `AlertDialog` naming the debt (DK-014).

## Patterns
- **P1 — one page header.** Desktop and tablet: the title and the page's actions together in the top
  bar (`PageHeader`), secondary actions first, the primary last; no separate actions row. Phone: the
  page's primary action in the shell's fixed bottom bar, full width; secondary actions in a «⋯»
  `DropdownMenu` in the top bar. A sub-page's h1 is the record's own name, with a back link to its
  parent above it. *(prototype; then worker A's shell item in code)*
- **P2 — the space's public state is one control:** one button that reads what visitors see
  («يظهر للزوار: ممتلئ يدويًا · 1:24»), in the state's colour, opening the popover that also holds
  «العودة للحالة التلقائية»; a short form on a phone, inside the one top-bar row. *(prototype)*
- **P3 — navigation grouped by task** (`SidebarGroup`): owner — نظرة عامة · اليوم (مكتب الاستقبال،
  الزبائن، الدفعات) · المال (المالية والتقارير، الباقات والأسعار) · المساحة (ملف المساحة، الإعلانات،
  بلاغات البيانات) · الفريق والإعدادات (الموظفون، الإعدادات); admin — نظرة عامة · المساحات (المساحات،
  أصحاب المساحات، بلاغات البيانات) · المنصة (المستخدمون، القوائم، سجل التدقيق، الإعدادات); reception
  ungrouped. *(prototype)*
- **P4 — one account menu in every shell:** the name and role, the email; «لوحة التحكم» on the site
  for a user with a dashboard, «الموقع العام» in the dashboard; «إعدادات حسابي»; on the site, the
  favourites and «بلاغاتي»; in the dashboard on a phone, the theme and the language; sign-out. On a
  phone the site header shows the avatar. *(prototype)*
- **P5 — one filter bar:** search always visible; every other filter a labelled `Field`, inline from
  768, in the `FilterSheet` bottom sheet below it with an active-count badge; the sheet's footer a
  primary «عرض N نتيجة» and a ghost «مسح الفلاتر»; a single status filter of four or fewer choices as
  `ToggleGroup` chips; the result count by the toolbar. *(prototype)*
- **P6 — every list pages:** 20 per page, `Pagination` in the table's footer with «1–20 من 312»,
  Previous/Next around the summary on a phone. *(prototype)*
- **P7 — one set of states** on every page that loads data: loading (`Skeleton` / `DataTable
  loading`), a load error (destructive `Alert` with «إعادة المحاولة»), offline, 403 and 404 inside the
  dashboard shell too (`EmptyState`). *(prototype)*
- **P8 — every action says it is working, it worked, or it failed:** the button's `loading`; a success
  toast saying what changed; a failure inside its dialog or sheet (which stays open and keeps the
  input), or a toast with «إعادة المحاولة» on a page; the 429 warning everywhere; toasts above the
  bottom bar. *(prototype)*
- **P9 — one rule for confirm and undo:** reversible and affecting no one else → act at once, then a
  toast with «تراجع», no dialog; irreversible or felt by others → an `AlertDialog`, action
  `variant="destructive"` repeating the verb, body saying the true consequence, no undo after.
  **Exception: deleting a space keeps its destructive confirmation** (its restore lasts only the
  toast's ten seconds; finding 44). Every dismiss button says **«رجوع»**; «إلغاء» is only the verb of
  voiding a payment. *(prototype)*
- **P10 — save stays enabled** (foundation §10); a section with unsaved changes says
  «تغييرات غير محفوظة» beside it. *(prototype)*

## Issues not covered by a pattern
- **SH-005** phone: the language in the header, the theme in the drawer and the account menu; in the
  dashboard both in the drawer's foot. *(prototype)*
- **SH-006** the tablet rail shows the space's mark as the switcher, named, with a tooltip.
  *(prototype)*
- **SH-007** below `lg`, a table of more than five columns becomes cards, or names a column priority;
  every `dir="ltr"` value in a cell is `nowrap`. *(prototype)*
- **SH-016** a sub-page's h1 is the record's name (P1). *(prototype)*
- **SH-018** a «تخطَّ إلى المحتوى» link first in every shell. *(prototype)*
- **SH-019** English «membership» → «subscription» everywhere (57). *(prototype)*
- **SH-020** account-menu items all in the menu's colour. *(prototype)*
- **SH-021** «للعرض فقط · الدفع في المساحة» once, in the list's header line; an empty price cell with
  no border and muted text. *(prototype)*
- **SH-012** the `Toaster` clears the bottom bar. *(design system)*
- **SH-017** `CardTitle` takes a heading level; the auth card's title is the page's h1.
  *(design system)*
- **SH-022** `Skeleton` one step stronger on a card (a component token). *(design system)*

## Rules changed
- **foundation §5:** Full is `warning`, Closed is `neutral` (not `destructive`). *(docs, with worker
  A's design-system item)*
- **foundation §9:** a table of more than five columns becomes cards below `lg`. *(docs, same)*
- **foundation §13 / the fix phase:** the shells and every list page are checked at **768** too.
