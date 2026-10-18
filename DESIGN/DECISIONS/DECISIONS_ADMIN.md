# Design decisions — batch 2, the admin's dashboard (approved by the owner, 2026-10-10)

> **Amended 2026-10-11** by the owner, at PR #59's review: the batch is built as **two items** —
> **2a, the space editor** (A1, A2, hours, prices, contacts, the verified page, AD-002's creation
> form, the gallery) and **2b, the rest**. **AD-029 narrowed:** data tables full width; a list managed
> row by row with controls (the lookups, the amenities) keeps a reading width (`max-w-3xl`/`4xl`), so a
> row's name stays near its controls. From #59's review, for this batch: «بيانات قديمة فقط» as A7's
> chip (2b); «إضافة مساحة» leads to the creation form (2a); the gallery has no date, confirm or save
> (2a).
>
> **Amended 2026-10-12** by the owner, at PR #61's look: **no «24 ساعة» switch** (AD-009) — no space
> in Gaza opens around the clock; midnight is «إلى» 24:00; each day shows «مفتوحة»/«مغلقة»; the
> admin's amenities list links «إدارة قائمة المرافق». **The amenities' place (filter or not, who adds
> them) is reopened** by the owner as a larger decision.
>
> **Amended 2026-10-12** (the owner, before 2b): **amenities are no filter** anywhere; a space has
> **«مرافق إضافية»** of its own beside the common list (Arabic name required, English optional, at
> most 20, each 1–60 characters), in the amenities group — the shared editor shows them (2b). **A5's
> role change, as #62 built it:** a person with any active link keeps the role the links give, so on
> an owner's row «تغيير الدور» stays visible, disabled, with «دوره يتبع روابطه — فُكّ ربطه أولًا» and
> the unlink link; the admin's own row reads «أنت» with no actions; an owner whose spaces are all
> deleted says «كل مساحاته محذوفة — استرجع المساحة لفك ربطه» (finding 50).
>
> **Amended 2026-10-12** (the owner, at 2b's plan): **«ناقصة» is `warning` everywhere** for the admin
> (A8; the built list's `neutral`, #50, follows when worker A builds this screen). **AD-028's red
> follows P9:** `destructive` for deleting a space, suspending an account and unlinking an owner;
> hiding is `neutral`. **To route:** DI-23 (`DataTable` cards until `lg`) → worker A's design-system
> item; DI-24 (the users row lacks reception links) → step 6.

From `REPORT\REVIEW_ADMIN_REPORT.md` (AD-001 … AD-030). **Settled.** Where each is done:
**prototype** (the design fixer), **design system** (worker A, in code), **API** (worker B),
**docs** (the owning document), **web** (worker A, when it builds the screen).

## The space edit screen (S2b-4 builds on it)
- **A1 — five fact groups and a gallery** (AD-001, 004, 008, 010, 011): one «المساحة» section (the
  basics and the location as two `Separator`-ed blocks, one footer, one date, one confirm), then
  ساعات العمل, الأسعار, المرافق, التواصل, then الصور (no date, no confirm). A group never saved says
  «لم تُضف بعد» and offers **Save only**. Section titles are `h2`; below `lg` the side navigation
  becomes a scrolling row of chips, the current section marked at every width, one name per section
  in both places. *(prototype; web in S2b-4)*
- **A2 — after a creation, the new space's edit screen with a "still missing" checklist** (AD-003):
  the five groups, each «لم تُضف بعد» or «تمّت», each linking its section; the same checklist heads
  any space with missing groups. **Arrives with S2b-4** (until then the creation returns to the list,
  #57). *(prototype; web in S2b-4)*
- **Hours** (AD-007, AD-009): «من» and «إلى» as two labelled `Field`s, side by side from `md`,
  stacked below; a shift validated **against each open day**, the error naming the day; «نسخ إلى كل
  الأيام» in the section's header (from the first open day); a «24 ساعة» switch per day; the shift's
  English name marked optional. *(prototype)*
- **Prices** (AD-008): a small table, the labels once in its header from `md`, one card per price on
  a phone; «الوردية» lists the section's own shifts (none → disabled, «أضف ورديات أولًا»);
  «إضافة سعر» disabled at the limit with its reason; a duplicate marked on the field that would tell
  it apart. *(prototype)*
- **Contacts** (AD-006, with PU-021): the contract's seven types; **«هاتف»**, never «جوال» or
  «أوريدو» as a type — the carrier is **derived** from the number's prefix (+97059 جوال, +97056
  أوريدو) and shown beside it; each field's helper shows the stored form. *(prototype)*
- **The verified space's page** (AD-012): its Alert's two paths are links («بلاغات <المساحة>»,
  «فك ربط المالك»), with «عرض في الموقع»; the owner named; no section list below `lg`. *(prototype)*

## Spaces, owners, users
- **A3 — a space's state is two facts; a deleted space has a way back** (AD-013, AD-014): the
  verification badge always, plus a «مخفية» badge; «محذوفة» as a fourth choice of the status filter,
  muted rows with «استرجاع». Resolves finding 44. *(prototype; API: `status=deleted` in
  `GET /admin/spaces`; web later)*
- **A4 — one way to link an owner** (AD-015, AD-016): from a space, a `Combobox` choosing **one
  person** (owners and users by name or email, suspended accounts excluded, each option saying what
  it is); from a person, a `Combobox` choosing **one space** (its state and current owner shown);
  unlinking names the owner («فك ربط أحمد»), one item per owner; both say the consequence before the
  act («تصبح موثّقة ويعدّلها مالكها» / «تصبح غير موثّقة وتختفي حالتها المباشرة»). *(prototype; API:
  B's owner-linking item)*
- **A5 — say what an action will do to someone else, before it is done** (AD-017, AD-018, AD-020):
  adding an owner says «سيُنشأ حساب ويظهر رمز مرور مؤقت مرة واحدة» (or «سيُرقّى حسابه» for an
  existing account), its submit «إنشاء حساب وربط», one space at a time; the one-time password dialog
  has no X, no Escape, no outside click — «تم», enabled after «نسخ», is its only way out — and asks
  how it was handed over (واتساب · شفهيًا · أخرى), written to the audit entry; a role change offers
  **«مستخدم» or «أدمن»** only («مالك» shown as derived from the links, ADR 0009 rule 2), and to or
  from «أدمن» is an `AlertDialog` naming the consequence. *(prototype; API: the handover channel and
  the role rule)*
- **A6 — the owners page stays** (AD-019), as a view of `GET /admin/users?role=owner` with each
  owner's links in the row, with the users list's search and state filter. *(prototype; API: B)*
- **AD-021:** a Google-only user's «إصدار كلمة مرور مؤقتة» stays, disabled, with its reason.
  *(prototype)*

## Lists, overview, reports, lookups, audit, settings
- **A7 — column priority at 768** (AD-019, AD-022, AD-028), applying SH-007: Spaces, Users and Data
  reports become **cards** at 768; Owners and the Audit log stay tables (email under the name; details
  under the target); Owners gain search; Data reports gain the space and the field as filters; the
  Audit log gains a target search. **The lookups never page** (the contract answers them whole). A
  switch is not a filter field: «بيانات قديمة فقط» becomes a `ToggleGroup` chip by the count.
  *(prototype)*
- **A8 — the overview is a work queue** (AD-023, AD-022, AD-012): the fourth tile «مساحات غير موثّقة
  بلا مالك»; «اكتمال البيانات» lists only what the admin can act on, the first five, with «عرض
  الكل»; missing is `warning` (photos `neutral`), never `destructive`; the tile and the card count
  stale **and** missing; a report's «تعديل الحقل» carries the report to the edit screen, where
  «تم التصحيح» is in place; «لم يُعتمد» requires its reply. *(prototype)*
- **Lookups** (AD-025, AD-026): the switches only in the row (the sheet keeps the names and the icon;
  the «ليس في الفلاتر» badge goes); each arrow's name carries its position («… — 11 من 11»), the row
  keeps the focus, a live region announces the move; a list of more than ten rows offers a position
  field in its sheet. *(prototype)*
- **Audit log** (AD-028): each target links to its page; action badges `neutral`, `destructive` only
  for the two that end access; the range reads «آخر 30 يومًا» with «كل الفترة»; the actor filter only
  once there is more than one actor. *(prototype)*
- **Settings** (AD-029): one content width for a form page (`max-w-3xl`), lists full width; one
  name, «إعدادات المنصة», in the sidebar and the page; each card its own error. *(prototype)*
- **Already better in code** (AD-002, 005, 010, 024, 027): the design catches up — one creation form,
  the grouped area field, «اختياري» and the two landmarks, the tabs with panels, the eight-icon grid.
  *(prototype)*

## Design system
- **AD-030 (with PU-019):** controls keep their 40 px look; on a coarse pointer the layer guarantees a
  **44 × 44 hit area** for `Button size="icon"` and `size="sm"`, `Switch`, `ToggleGroupItem` and the
  map's pins. *(design system)*

## Amendments to the shared decisions (see `DECISIONS_SHARED.md`)
- **P1 narrowed:** the phone's fixed bottom bar is only for the action that is **the page's purpose
  and used all day** (the desk's «تسجيل زيارة»). A list's **"add" sits in a row above the list, at
  its end, at every width** (as #57 built "Add space"); secondary page actions go in the top bar's
  «⋯». Sub-pages as P1 says.
- **P8's exception:** an action whose result **shows in the row it changed** (a switch, a reorder)
  raises **no success toast**; only its failure is announced (as the built lookups do).

## Rules changed
- **foundation §10 and §15:** "40 px controls; 44 × 44 hit area on touch". *(docs, with A's
  design-system item)*
- **docs/plans/v1-mvp.md**, `PATCH /admin/users`: the role offered is `USER` or `ADMIN`; `OWNER`
  follows the links (ADR 0009). *(docs, with B's owner-linking item)*
