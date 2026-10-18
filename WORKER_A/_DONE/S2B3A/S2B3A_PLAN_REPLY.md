# S2b-3a — reply to your plan

The plan is approved, with the points below. It reached us cut in a few places by the terminal (the
start of the page's composition, L5's first lines, alternative 2, commit 4); what we could read keeps
the decisions. Build in this order; no new subagents beyond the cap.

## Approved as you proposed
- **The seam:** the two slots on `AdminSpacesList` (`actions(row)`, `placeField(field)`), filled by
  the page; the exports `AdminSpacesList`, `SpaceActionsMenu`, `SpaceActionsHold`,
  `GovernorateAreaSelect`.
- **Invalidation across the seam: approved** — `spaces`' writes invalidate the whole `['admin']`
  prefix, by `desk`'s rule, and stay pending until the list has arrived. Write it as **one platform
  line in `docs/frontend/architecture.md` §7**, beside `desk`'s (an admin write whose screen shows
  another capability's list invalidates the `admin` scope), and the decision with its reason in
  `spaces.md`.
- L2–L7 as written, the "restored" toast included; the Undo's 10 s.
- **Alternative 1** (the dialog's line: "It leaves the site and this list. You can undo it right
  after."): approved — it says only what is true (finding 44).
- **Alternative 3** (the date formatter stays in the feature for now): agreed.
- **Alternative 4** (the switcher's files into `switcher/` folders, moves only, its own commit):
  approved.
- The tests, the Review Focus list, the commits and the verification as planned.

## Changes
1. **An English name inside an Arabic sentence carries `lang="en"`.** Your Review Focus says it can't;
   it can where the text is rendered as a node: the delete dialog's title (the prototype does exactly
   this: `حذف <span lang="en">…</span>؟`) and the toasts, if the design system's `Toast` takes a node
   (Sonner does). Do it in both, with a test on the dialog's title; only where a string is truly
   required (an `aria-label`) does the name stay unmarked — say where in the PR.
2. **The owner's term follows the glossary:** «صاحب المساحة» (the column) and
   «صاحب المساحة: {owners}» (the card), «بلا صاحب مساحة» read aloud — the sidebar already says
   «أصحاب المساحات». The stale badge keeps the design's «قديمة: {groups}»: it is a fact for the admin,
   not the public's hedge. *(The owner may still choose the design's «المالك»; if so, this item is
   replaced by the owner's answer.)*
3. **Alternative 2 arrived cut** ("…as changed."): it is **not approved yet**. Restate it in two
   lines at the top of your next message and build everything else meanwhile; leave its part for
   last.

## The Arabic copy
Your table reached us with the Arabic letters reversed by the terminal; the owner approves the lines
as they read here (from your table), with change 2 applied. Check the catalogue against them:
- «المساحات» · «بحث» / «اسم المساحة» · «المحافظة / المنطقة» / «كل المناطق» · «{name} (مخفية)» ·
  «جارٍ التحميل» / «تعذّر تحميل المناطق» · «الحالة» / «كل الحالات»
- «الفلاتر» / «الفلاتر، المطبّق منها: {count}» · «مسح الفلاتر»
- columns: «المساحة · المنطقة · الحالة · صاحب المساحة · الحداثة · آخر تحديث · إجراءات»
- «محدّثة» / «قديمة: {groups}» / «غير مُدخلة: {groups}»; groups «البيانات الأساسية · ساعات العمل ·
  الأسعار · المرافق · التواصل», separated by «، »
- «عدد المساحات: {count}» · «لا توجد مساحات بعد» / «تظهر المساحات هنا بعد إضافتها.» ·
  «لا توجد مساحات تطابق الفلاتر» · «تعذّر تحميل المساحات»
- pagination: «صفحات قائمة المساحات · السابق · التالي · الصفحة {page} · الصفحة {page} من {total} ·
  صفحات أخرى»
- menu: «إجراءات: {name} · إخفاء · إظهار · حذف»
- dialog: «حذف {name}؟» · «تختفي من الموقع ومن هذه القائمة، ويمكنك التراجع فور الحذف.» ·
  «إلغاء» · «حذف»
- toasts: «أُخفيت {name} من الموقع» · «أصبحت {name} ظاهرة» · «حُذفت {name}» · «تراجع» ·
  «استُرجعت {name}»
- failures: «تعذّر إخفاء {name}» · «تعذّر إظهار {name}» · «تعذّر حذف {name}» ·
  «تعذّر استرجاع {name}»

If any line in your catalogue differs from these, the list above wins; report a line you think is
wrong instead of changing it.
