# Design fix 2b: the rest of the admin's dashboard

Worker: the design-fix worker (the third). Worktree `C:\Users\basel\masaha-design`, detached at `origin/main`
`068efc6` (#61 and #62 merged), tree clean, fetched and pruned. Branch `design/admin-rest`, not cut yet.
Prototype on **5346**. Images go to `C:\Users\basel\Downloads\design-fix-admin-rest\`. Subagents used: 0 of 2.

**Approved 2026-10-12** (`PROMPT\FIX_ADMIN_REST_PLAN_REPLY.md`):
- S1–S15 as recommended. S10's icons are the prototype's own, noted as lucide's (ISC).
- DI-21, DI-22 and DI-25 are folded. DI-22 means **«ناقصة» is `warning` everywhere** for the admin;
  `CHANGES.md` says the built list's `neutral` (#50) follows when worker A builds that screen.
- DI-23 and DI-24 are recorded in the report only. The analyst routes DI-23 to worker A and DI-24 to step 6.
- **AD-028 amended by the owner:** the log's red follows P9. `destructive` covers `space_deleted`,
  `user_suspended` and `owner_unlinked`; hiding becomes `neutral`, like every other action. §4 and §8 below
  are read with this change.
- At the report, run `git merge-tree --write-tree` against every open PR.

## 1. Summary

This is the second item of batch 2. It covers every admin page except the editor, built in #61. It applies the
rest of `DECISIONS_ADMIN.md` with its three *Amended* notes, plus two decisions taken since.

- **Own amenities (G1).** A space has «مرافق إضافية» of its own, in the shared editor. Both editors inherit them.
- **No amenity filter (G2).**
- **A space's state is two facts (G3).** A deleted space can be restored from the list.
- **Linking owners and changing people (G4).** There is one way to link an owner. Each act on another person
  says its consequence first. The role, suspension and the temporary password do only what #60 and #62 let the
  API do.
- **The lists, overview, reports, lookups, audit and settings (G5).** The lists follow A7's column priority and
  filters. The overview becomes a work queue (A8). A report is resolved from inside the editor. The lookups say
  what moved (AD-024…027). The audit log leads somewhere (AD-028). The settings get one width and one name
  (AD-029, as narrowed).

## 2. Contract

**Scope.** G1–G5 of the prompt, inside `docs/design/` only: the eight admin pages, `masaha/admin.jsx`,
`admin-data.js`, `profile-b.jsx` (G1), `Admin space edit.html`, `Flows - states.html`, `CHANGES.md` (a *Batch 2b*
section) and `INDEX.md`.

**Acceptance criteria.**
- **G1, the shared editor.** Its amenities section shows the common list, then «مرافق إضافية»:
  - rows of an Arabic name and an English name marked «اختياري»;
  - adding stops at 20, with «الحد 20 مرفقًا إضافيًا»;
  - each row can be removed;
  - an empty, over-long or repeated Arabic name is refused on its own field;
  - everything is saved, dated and confirmed with the section.

  The admin's editor keeps «إدارة قائمة المرافق» under the common list. `Owner space profile.html` shows the
  same section. #61's fixes hold: F1's 20 px gap, the shift ids, the day errors, the gallery's count.
- **G2.** No «في الفلاتر» switch, badge, helper or line is left on any admin page, in the admin data or on the
  board's lookups label. The Directory's filter is left as it is.
- **G3.**
  - The verification badge always shows on a space, with «مخفية» beside it when hidden.
  - The state filter offers «محذوفة» as a fourth choice. Its rows are muted and offer «استرجاع», which works at
    once.
  - «كل الحالات» never lists a deleted space.
  - The delete dialog's wording is true.
- **G4, linking.**
  - From a space, the admin picks one person in a `Combobox`. Admins and suspended accounts are not offered.
  - From a person, the admin picks one space in a `Combobox`, which shows each space's state and owner.
  - Both say the consequence before the link is made.
  - Unlinking offers one item per owner, naming them.
  - `Admin owners.html?unlink=<user>&space=<id>` opens that owner and that space.
- **G4, adding an owner.**
  - The sheet takes one space and says what will happen. Its submit reads «إنشاء حساب وربط».
  - `EMAIL_HAS_ACCOUNT` is answered after the submit and leads to «سيُرقّى حسابه» with «ترقية وربط».
  - `ALREADY_OWNER`, `ACCOUNT_IS_ADMIN` and `ACCOUNT_SUSPENDED` show on the email field.
- **G4, the one-time password dialog.**
  - It has no X, and Escape or a click outside does not close it.
  - «تم» stays disabled, with its reason shown, until «نسخ».
  - It asks how the password was handed over.
- **G4, the role.**
  - The only roles offered are «مستخدم» and «أدمن», through an `AlertDialog` that names the consequence.
  - On an owner's row, «تغيير الدور» is disabled, with «دوره يتبع روابطه — فُكّ ربطه أولًا» and the unlink link.
  - The admin's own row reads «أنت» and has no actions.
  - An owner whose spaces are all deleted shows «كل مساحاته محذوفة — استرجع المساحة لفك ربطه».
- **G4, suspension.** An `AlertDialog` gives the real consequence, including the owner's line. Restoring
  happens at once.
- **G4, the temporary password.** It is disabled, with its reason shown, for a Google-only account and for a
  suspended one.
- **G5, the lists.**
  - From 768 to 1023, Spaces, Users and Data reports show as cards.
  - Owners and the Audit log stay tables at those widths: the email goes under the name, and the details under
    the target.
  - Owners gain search and a state filter.
  - Data reports gain a space filter and a field filter, and read `?space=`.
  - The Audit log gains a target search.
  - «بيانات قديمة فقط» becomes a `ToggleGroup` chip beside the count.
- **G5, the overview and reports.** The overview is A8's work queue. A report's «تعديل الحقل» opens the editor,
  where «تم التصحيح» sits in place. «لم يُعتمد» requires a reply.
- **G5, the rest.** The lookups, audit log and settings are as §4 G5 describes.
- Every page I change opens at 390, 768 and 1440, in Arabic and English, light and dark, with no blank render,
  no console error and no horizontal overflow. Every changed `INDEX.md` URL resolves.
- `check-parse.mjs`, `check-classes.mjs`, `format:check` and `check:links` all pass.
- There is a before/after pair per decision, not committed.

**Out of scope.**
- The editor's own parts from 2a: hours, prices, contacts, the gallery, the creation form.
- The public pages: the Directory's amenity filter, and own amenities on the space page (batch 4).
- The owner's own differences (batch 5).
- The design-system items: AD-030's 44 px hit area, and DI-23 below.
- Everything outside `docs/design/`: `apps/`, `packages/`, `docs/features/`, the findings.
- The `screens/` images.
- Anything on *Not in v1*.

## 3. Reading done

- **Bootstrap:** CLAUDE.md; workflow §2 (Phases, Reading before work), §3 (Commits), §4; the open findings'
  titles.
- **The decisions:** `DECISIONS_ADMIN.md` (all three *Amended* notes, then Spaces/owners/users and Lists…) and
  `DECISIONS_SHARED.md` (P1 as amended, P5–P10, SH-007).
- **Fix 2a:** `FIX_ADMIN_EDITOR_PLAN.md` and `FIX_ADMIN_EDITOR_REPORT.md` (DI-18…20, the checks run).
- **The review:** `REVIEW_ADMIN_REPORT.md` P2–P6 and AD-013…AD-030, plus its rules in doubt.
- **The features:** `docs/features/users.md` and `space-links.md` (*What it does*, *Behaviour*, *API* and
  *Web decisions*).
- **The contract:** `api-contract.md` › *Spaces*, *Owners*, *Users (the admin)* and §6.
- **Amenities:** `AMENITIES_PLAN.md` (D1, D2, S1, S6, design issue 1, the caps; «مرفق إضافي»).
- **Foundation:** §5 status roles and §10, chiefly line 305: submits stay enabled, and a disabled action
  shows its reason.
- **Glossary:** Owner, verified. *Amenity* is not in it yet; the amenities item adds it.
- **The archive:** `CHANGES.md` (batch 1 and 2a), `INDEX.md` (the parameters table, §42–49) and the board's
  admin URLs.
- **The prototype:** all eight pages, `admin.jsx`, `admin-data.js`, `profile-a.jsx` (`useSection`,
  `ProfileSection`, `LimitNote`), `profile-b.jsx` (`AmenitiesSection`, `ContactsSection`), and `shared.jsx`
  (`FilterSheet`, `ResultCount`, `usePaged`, `ActionButton`/`ActionAlert`).
- **`finance.jsx`:** `RangePicker`.
- **The vendored bundle:** `DataTable`, `Combobox`, `DialogContent` and the icon exports.

**What shapes the build:**
- The vendored `DataTable` chooses cards or a table by one media query at 768 and has no prop to change it.
  "Cards at 768" therefore needs a prototype wrapper (§4 G5, DI-23).
- `Combobox` is in the bundle (single, searchable, with `keywords`). No page has used it yet.
- `DialogContent` with no `closeLabel` draws no X, and Radix's `onEscapeKeyDown` and `onInteractOutside` pass
  through.
- Of the platform's eight amenity icons, the bundle has only `SunIcon` and `UsersIcon` (S10).
- `max-w-3xl` and `max-w-4xl` exist in the prebuilt CSS.
- **Untrue sample data, now fixed:**
  - the audit's temporary password went «عبر واتساب» to Nour, who is Google-only;
  - `?temp=1` opens a temporary password for that Google-only user;
  - the owners page lists Rima «بدون مساحة», which ADR 0009 rule 2 says cannot persist.

## 4. The decisions, as they will be built

### G1: «مرافق إضافية» in the shared editor (`profile-b.jsx`)
- **The section's value.** `AmenitiesSection`'s value becomes `{ list, own }`, so the one save, its date, its
  dirty badge and its confirm cover both. `own` comes from `space.ownAmenities || []`, or `[]` while the group
  is missing.
- **Order inside the card:**
  1. the common checkboxes;
  2. on the admin's editor only, «لإضافة مرفق إلى قائمة كل المساحات: إدارة قائمة المرافق». The line is
     reworded because «مرفق ليس في القائمة؟» now has two answers;
  3. a `Separator`;
  4. an `h3` «مرافق إضافية» with «مرافق ليست في القائمة تخصّ هذه المساحة»;
  5. the rows: «الاسم بالعربية» and «الاسم بالإنجليزية» `labelEnd` «اختياري», side by side from `md` and
     stacked below, with an icon remove button named «حذف المرفق الإضافي 2»;
  6. «إضافة مرفق إضافي», disabled at 20 with `LimitNote` «الحد 20 مرفقًا إضافيًا». This copies the contacts'
     pattern.
- **Checks on save** run through `ProfileSection`'s `validate`, which focuses the first error:
  - an empty Arabic name: «أدخل الاسم بالعربية أو احذف هذا المرفق»;
  - over 60 characters: «60 حرفًا على الأكثر», on either field;
  - a repeated Arabic name, after trimming: «مرفق مكرّر», on the repeat's field, as the server's `not_unique`
    does.
- **Sample:** Golden Hub gets two own amenities in `admin-data.js` (`own`), passed through by
  `Admin space edit.html`. `?demo=ownlimit` fills 20.
- **The verified read-only page** gets an «مرافق إضافية» row after «المتوفر».
- **The owner's page** inherits the section with no own amenities and no page change. I open it after each
  change (risk §5).

### G2: no amenity filter
- **`Admin lookups.html`:**
  - The amenity row loses its «في الفلاتر» switch and its «ليس في الفلاتر» badge.
  - The sheet loses «يظهر في الفلاتر».
  - The amenities card loses its line about filters, so it is its title plus «إضافة مرفق», as the amenities
    plan's design issue 1 has it.
  - The amenities panel's own line takes the plan's hint: «غير النشط لا يظهر في النماذج، وتحتفظ به المساحات
    التي لديها.»
- **`admin-data.js`:** the `filter` flag goes, and the audit line «لا يظهر في الفلاتر» becomes a real amenity
  change.
- **`Flows - states.html`:** the lookups section's label stops naming «يظهر في الفلاتر».
- **The Directory** is left as it is (batch 4).

### G3: A3, a space's state (`Admin spaces.html`, `admin-data.js`)
- **The data.** A space keeps `status: 'verified' | 'unverified'`, which the editor reads, and gains
  `hidden: true`. Palm becomes unverified and hidden.
- **A deleted space.** A new deleted space, `olive` (Olive Desk, Deir al-Balah, `deleted: '2026-08-14'`), is
  Rima's only space (S13).
- **The row** shows `SpaceStatus` (verification) plus «مخفية» (`warning`) beside it.
- **The state filter:** «كل الحالات» · موثّقة · غير موثّقة · مخفية · محذوفة, read from `?status=`.
  - Verified and unverified leave hidden spaces out, as the contract's filter does.
  - «كل الحالات» never shows a deleted space.
- **Deleted rows** are muted (`text-muted-foreground`, «محذوفة في …»). They have no menu, only «استرجاع»
  (`Button size="sm" variant="outline"`). Restoring is immediate: the toast says «استُرجعت Olive Desk — عادت
  كما كانت» and the row returns to its state (S1).
- **The delete dialog** says «تختفي من الموقع ومن القائمة، وتجدها في «محذوفة» لاسترجاعها.» Its toast keeps
  «تراجع».
- **Hiding** keeps its toast and «تراجع». The verification badge stays.

### G4: one way to link, and saying what an act does (A4, A5, A6, AD-021)
**One `LinkOwnerDialog` in `admin.jsx`, used by both pages** (S2):
- **From a space** (`Admin spaces.html?link=golden`):
  - a `Combobox` «الشخص» of the owners and the users, searchable by name or email (`keywords`), each option
    giving the name, the email, and «مالك · Focus Hub» or «مستخدم»;
  - admins and suspended accounts are not offered, and nothing is preselected.
- **From a person** (`Admin owners.html?link=o1`):
  - a `Combobox` «المساحة» of the spaces that are not deleted, each option carrying its state badges and its
    owner («بلا مالك»);
  - the person's own spaces appear disabled, marked «مربوطة».
- **The consequence line** sits above «ربط» and changes with the choice:
  - an unverified space: «تصبح موثّقة ويعدّلها مالكها، ولا يعدّلها فريق مساحة بعد الآن»;
  - an already verified space: «يصبح مالكًا ثانيًا؛ تبقى موثّقة»;
  - a person who is a user so far: «يصبح حسابه حساب مالك، ويُطلب منه الدخول من جديد».
- **Submitting** with nothing chosen gives «اختر شخصًا» or «اختر مساحة» on the field. `?fail=link` shows the
  contract's `RECEPTION_LINK_ACTIVE` line inside the dialog, which stays open (DI-24).

**Unlinking:**
- The spaces menu has one item per owner, «فك ربط أحمد».
- `Admin spaces.html?unlink=<space>&owner=<id>` (the owner defaults to the first).
- `Admin owners.html?unlink=<user>&space=<id>` (the space defaults to that owner's first). This replaces the
  hard-coded `?unlink=1`; `INDEX.md` and the board take `?unlink=o3`.
- The verified page's «فك ربط المالك» becomes «فك ربط أحمد», one per owner.
- The dialog keeps its true consequence: the last owner → «تصبح غير موثّقة وتختفي حالتها المباشرة».

**The owners page is a view of the users** (A6). `admin-data.js` puts the four owners into `users` with ids
`o1…o4`, so `?link=o1` keeps working, and adds `spaces`. The page reads `users.filter(role === 'owner')` and
gains:
- search by name or email (`?q=`) and the state filter;
- the row's links: one chip per space that is not deleted, or for Rima «كل مساحاته محذوفة — استرجع المساحة
  لفك ربطه», with its link to `Admin spaces.html?status=deleted`;
- for a suspended owner, «ربط بمساحة» disabled with «الحساب موقوف — استرجعه أولًا». Unlinking stays.

**Adding an owner (A5):**
- **The sheet:** «الاسم», «البريد الإلكتروني», and **one** «المساحة» (`Combobox`, the same list as above).
  Above the submit: «سيُنشأ حساب ويظهر رمز مرور مؤقت مرة واحدة — جهّز طريقة تسليمه». The submit reads «إنشاء
  حساب وربط».
- **The server's answers come after the submit** (S3):
  - `EMAIL_HAS_ACCOUNT` shows an `info` `Alert`: «لهذا البريد حساب: سيُرقّى حسابه إلى مالك ويُربط بالمساحة،
    ويحتفظ باسمه وطريقة دخوله، ولا تظهر كلمة مرور». The submit becomes «ترقية وربط».
  - On the email field (S4): `ALREADY_OWNER` gives «مالك مسبقًا — اربطه بالمساحة», a link that opens the link
    dialog for them; `ACCOUNT_IS_ADMIN` gives «حساب أدمن، لا يُربط بمساحة»; `ACCOUNT_SUSPENDED` gives «الحساب
    موقوف — استرجعه أولًا».
  - `?email=nour@example.com` opens the sheet in the post-refusal state.

**The one-time password dialog** (`TempPassDialog`, `admin.jsx`, A5, S5):
- No `closeLabel`, so no X. `onEscapeKeyDown` and `onInteractOutside` are prevented.
- «نسخ» turns into «نُسخت».
- «تم» is disabled until then, with «انسخها أولًا — لن تظهر مرة أخرى» beside it (foundation §10).
- «طريقة التسليم» is a `RadioGroup`: واتساب · شفهيًا · أخرى. It is checked when «تم» is pressed («اختر طريقة
  التسليم»), because a submit stays enabled. The toast says «سُجّلت طريقة التسليم».

**The users page** (`Admin users.html`):
- **Role** (amended A5, S6). On a user's or another admin's row, «تغيير الدور» opens an `AlertDialog` naming
  the one possible change:
  - «جعل سارة أحمد أدمن؟ يحصل على كل صلاحيات الإدارة، وتنتهي جلساته فيدخل من جديد.», action «جعله أدمن»;
  - «إعادة منى مستخدمًا؟ يفقد لوحة الإدارة فورًا، وتنتهي جلساته.», action «إعادته مستخدمًا»
    (`destructive`).
  - The sample gains a second admin, منى (S14).
- **Disabled items** (`DropdownMenuItem disabled`, with the reason as a caption line inside it):
  - an owner's row: «تغيير الدور» disabled with «دوره يتبع روابطه — فُكّ ربطه أولًا», followed by the item «فك
    روابطه» → `Admin owners.html?q=<email>`;
  - Rima's row: «كل مساحاته محذوفة — استرجع المساحة لفك ربطه», followed by «المساحات المحذوفة»;
  - the admin's own row: «أنت», no menu.
- **Suspension:** an `AlertDialog` reading «تنتهي كل جلساته فورًا ولا يدخل حتى تسترجع حسابه.», plus, for an
  owner, «تبقى مساحته موثّقة، ولا تُعدَّل إلا بعد فك ربطه.» Its action is «إيقاف» (`destructive`).
  «استرجاع الحساب» acts at once with a toast.
- **The temporary password** is disabled with its reason: «حساب Google — يستعيده من Google» (AD-021), or
  «الحساب موقوف — استرجعه أولًا».
- **Sample fixes:** `?temp=1` now takes the first active account with a password (Omar). The audit's line
  names Omar.
- **`?q=`** is read into the search, for the audit's links.

### G5: the lists, the overview, reports, lookups, audit, settings
**A7, the column priority at 768:**
- **`AdminList` in `admin.jsx`.** It takes the `DataTable` props plus `cards="lg"`. Below 1024 it draws the
  toolbar, a list of cards and the pagination, with the same markup and classes as the `DataTable`'s own card
  branch. From 1024 it draws the `DataTable`. Spaces, Users and Data reports use it. The `.lg-col` columns that
  only waited for 1024 then show inside the table.
- **Owners** (columns: name, email, linked spaces, state, actions) and **the Audit log** (time, actor, action,
  target, details) stay `DataTable`. From 768 to 1023, the email goes under the name and the details under the
  target, as a caption; from 1024 they have their own column (S8).
- **Filters:**
  - Owners: search and state.
  - Data reports: the status chips, plus «المساحة» (`Combobox`, `?space=`) and «الحقل» (`Select`, `?field=`),
    all in `FilterSheet`. The «بلاغات <space>» link from #61 now filters.
  - Audit: «بحث في الهدف».
  - Spaces: «بيانات قديمة فقط» becomes a single `ToggleGroupItem` chip beside the count (`?stale=1`).
- **The lookups never page.** A comment says so, citing contract §4.

**A8, the overview as a work queue (`Admin overview.html`):**
- **The four tiles:**
  1. Spaces;
  2. open reports;
  3. «بيانات قديمة أو ناقصة», counting stale **and** missing → `?stale=1`;
  4. «مساحات غير موثّقة بلا مالك» → `?status=unverified`.
- **«اكتمال البيانات»** lists only the spaces the admin edits (not verified, hidden ones included), the first
  five, with «عرض الكل» → `Admin spaces.html?stale=1`.
- **Badges:** missing is `warning` and photos `neutral`, never `destructive`. «بدون دبوس» goes (DI-21).

**Reports:**
- In the sheet, «لم يُعتمد» requires the reply: «اكتب السبب؛ هو ما سيقرؤه صاحب البلاغ», focused. It stays
  optional for «تم التصحيح».
- «تعديل الحقل» → `Admin space edit.html?id=<space>&report=<id>#<section>`.
- **In the editor** (S7), an `info` `Alert` sits right above the reported section. It holds:
  - «بلاغ مفتوح على الأسعار», with the message, the reporter and the date;
  - «تم التصحيح», which marks the report, says so in the alert with a link back to the reports, and raises a
    toast;
  - «فتح البلاغ» for a reply.

**Lookups (AD-024…027, the P8 exception):**
- Each list sits in its `TabsContent`.
- The switches live only in the row. The sheet keeps the names and, for an amenity, the icon.
- **The icon** is a required grid of the platform's eight (`wifi · zap · sun · plug-zap · coffee · users ·
  presentation · graduation-cap`), each named as the code names it («واي فاي» …), with none preselected. The six
  the bundle lacks are drawn as inline SVG copied exactly from `node_modules/lucide-react`, noted as lucide's,
  ISC (S10). The sample rows get their right icons.
- **Arrows** are named «تحريك «الشجاعية» لأعلى — 11 من 11». The focus stays on the moved row's arrow, and a
  polite live region says «الشجاعية: 10 من 11».
- A list of more than ten rows (Gaza City's eleven areas) offers «الترتيب» in the row's sheet, as a number
  from 1 to N.
- **Toasts:** a switch or a move raises none (P8's exception). The sheet's save still raises one.
- **Reading width:** `max-w-4xl` (AD-029, as narrowed). The intro line moves into each panel, so the areas
  keep "filters and forms" and the amenities say "forms".

**The audit log (AD-028):**
- Each target is a link: a space → its editor; a person → `Admin users.html?q=`; a link → `Admin
  owners.html?q=`; a lookup → `Admin lookups.html` (`?tab=amenities`); a setting → `Admin settings.html`.
- Badges are `neutral`, and `destructive` only for `space_deleted`, `user_suspended` and `owner_unlinked`
  (AD-028 as amended: P9's destructive confirmations). `space_hidden` is `neutral`.
- «الفترة» is a `Select` of آخر 30 يومًا (the default) · كل الفترة · فترة محدّدة. Only the last shows the
  `RangePicker`, which stays untouched in `finance.jsx` (S9).
- «المنفّذ» shows only when the log has more than one actor. The sample has one, so it is hidden.
- With DI-25: delete, restore, unlink and unsuspend become actions and get sample lines.

**Settings (AD-029, as narrowed):**
- One `max-w-3xl` column.
- The sidebar item becomes «إعدادات المنصة», matching the page.
- Each card keeps its own errors (three error states, not one).

## 5. Stronger decisions (proposed alternatives)

| | What | Why | Cost | Recommend |
|---|---|---|---|---|
| **S1** | **Restore** happens at once, with a toast and no «تراجع» | It brings a space back exactly as it was; undoing it would be a delete, which keeps its confirmation | none | **yes** |
| **S2** | **One `LinkOwnerDialog`** for both pages; the person-side flow moves from a `Sheet` to the same `Dialog` | "One way to link" (A4): one component, one wording and one consequence line | small | **yes** |
| **S3** | **`EMAIL_HAS_ACCOUNT` is shown after the submit**, as the server answers it, not while typing | No endpoint looks up an email before the submit, so the old live hint promised what the web cannot do | none | **yes** |
| **S4** | `ALREADY_OWNER`, `ACCOUNT_IS_ADMIN`, `ACCOUNT_SUSPENDED` on the email field, each with its way on («اربطه بالمساحة» opens the link dialog) | Truth to the contract's refusals; a refusal names the next step | small | **yes** |
| **S5** | The handover is a **`RadioGroup`** (three visible choices), checked when «تم» is pressed; «تم» disabled only until «نسخ», with that reason shown | It reconciles A5's "«تم» after «نسخ»" with foundation §10 (a submit stays enabled and checks on submit), and the audit gets a channel every time | small | **yes** |
| **S6** | **«تغيير الدور» opens the `AlertDialog` directly**, naming the one change possible (user ↔ admin), with no radio step | With two roles there is nothing to choose: a radio dialog followed by a confirmation would be two dialogs for one act | none | **yes** |
| **S7** | **«تم التصحيح» sits in an `Alert` above the reported section**, carried by `?report=`, not sticky | "In place" means where the field is edited; on a phone the chips row is already sticky, and a second sticky bar would eat the screen | small | **yes** |
| **S8** | Owners' email and the Audit log's details go **under** the name or target only from 768 to 1023; they keep their own column from 1024 | A7 says it for 768; SH-007's pattern hides columns only below `lg` | none | **yes** |
| **S9** | The audit period is a **`Select` (آخر 30 يومًا · كل الفترة · فترة محدّدة)**, with the range picker only for the third | `RangePicker` is shared with the owner's finance pages, and its trigger can only print dates | small | **yes** |
| **S10** | **The six missing icons as inline SVG**, copied from `lucide-react` in `node_modules` (ISC, noted) | AD-027's grid has to show the platform's eight pictures, and the bundle draws two; the alternative is names with a placeholder mark | small | **yes** |
| **S11** | `?fail=link` and `?fail=role` show the contract's `RECEPTION_LINK_ACTIVE` and `ACCOUNT_HAS_LINKS` lines in their dialogs | The admin's list cannot know about reception links (DI-24), so the screen has to show the refusal | small | **yes** |
| **S12** | Tile 4 → `?status=unverified`; «عرض الكل» → `?stale=1` | "Unverified" already means no owner; the full list is where the rest of the work is | none | **yes** |
| **S13** | **Rima becomes a suspended owner whose only space (`olive`) is deleted**, replacing an "owner with no space" | ADR 0009 rule 2 forbids the old state; the new one is finding 50's real case and shows G4's message, G3's deleted row and the link flow's exclusion of suspended accounts | small | **yes** |
| **S14** | **A second admin (منى)** in the sample | Without one, the change *from* admin, the other half of A5's dialog, cannot be shown; she has no audit lines, so the actor filter stays hidden as AD-028 wants | none | **yes** |
| **S15** | `?q=` read by Users and Owners | The audit log's targets and the users page's «فك روابطه» have to land on the person | small | **yes** |

No rule of the documents is contradicted. Foundation §10 is the reason for S5.

## 6. Related findings

| Finding | Fold? | Why |
|---|---|---|
| **44**, no screen restores a deleted space | No | G3 draws the answer; the finding closes when the API (`status=deleted`) and the web build it, outside `docs/design/` |
| **50**, an owner whose only spaces are deleted | No | G4 shows the owner's chosen message; the finding is the API's, and stays as it is |
| **40**, the platform's contact settings | No | Settings' wording is not touched; the finding is the web's catalogue |
| **14**, the owner's audit screen | No | Batch 5 |

## 7. Files

Everything is inside `docs/design/`. Workers A and B never touch it, so no licence is needed.

- **Modules (3):** `prototype/masaha/admin.jsx`, `admin-data.js`, `profile-b.jsx`. `masaha.css` only if a
  needed class is missing from the prebuilt CSS.
- **Pages (10):** the eight admin pages; `Admin space edit.html` (G1's read-only row and demo, the report
  alert, unlink naming the owner); `Flows - states.html` (two `?unlink=` URLs, the lookups label).
- **Archive documents (2):** `CHANGES.md` (*Batch 2b*) and `INDEX.md` (the parameters table and the two
  `?unlink=` rows).
- **Not touched:**
  - `profile-a.jsx`; the report alert goes in the page;
  - `Owner space profile.html`; it inherits through the module;
  - `data.js`, `details-data.js`, `finance.jsx`, `shared.jsx`;
  - `README.md` and `SCREENS.md` (no page added or renamed).

## 8. Design issues

These were found while planning. **None is built unless the reply approves it.**

| | Issue | Better | Level | Recommend |
|---|---|---|---|---|
| **DI-21** | The overview flags «بدون دبوس على الخريطة», but the contract requires the pin when a space is created, so no space can lack one | Drop the badge, and `pin` from the sample's `missing` | prototype | fold |
| **DI-22** | "Missing" is `warning` on the overview (A8) and in 2a's checklist, but `neutral` on the built spaces list (space-links › *Web decisions*); the prototype list shows none at all | The list's freshness shows missing groups too, in **one** colour for the admin: `warning`, as A8 says. The web's choice goes to the analyst | prototype (web note) | fold the prototype; the web's choice is yours |
| **DI-23** | The layer's `DataTable` has no card breakpoint, so A7's "cards at 768" cannot be built with it | A `cards` prop (`md` by default, `lg` for these three lists) on the layer's `DataTable`; the prototype imitates it with `AdminList` | design system | record for worker A, not built here |
| **DI-24** | `AdminUserRow` carries only owner links, so a person's reception link is invisible: a role change or a link to them can only be refused afterwards | The row gains the reception links (or a `hasLinks`), so the item is disabled first with its reason; until then the dialogs show the refusal (S11) | API + prototype | prototype as S11; the API part to the analyst |
| **DI-25** | The log's seven action types miss what 2b's screens now do (delete, restore, unlink, unsuspend), so those acts would not appear | Add those four actions and sample lines; `destructive` for delete, suspend and unlink (AD-028 as amended) | prototype | fold |

## 9. Lanes and what proves each behaviour

**No test lane covers `docs/design/`.** The proof is:

| Check | The break it catches |
|---|---|
| `check-parse.mjs` | a syntax error that blanks a page |
| `check-classes.mjs` | a class the prebuilt CSS lacks, silently dead (the `AdminList` copy, `max-w-3xl`, the icon grid) |
| **A scripted browser pass** in the scratchpad: every changed page × 390/768/1440 × ar/en × light/dark | blank renders, console errors, horizontal overflow, a control cut off at the edge |
| Per-target assertions in the same pass | **G1:** 20 rows → «إضافة مرفق إضافي» disabled with its reason; a repeated Arabic name → its field `aria-invalid`; F1's 20 px gap; the owner's page has the section. **G2:** no «الفلاتر» text on the lookups. **G3:** `?status=deleted` → one muted row with «استرجاع», and «كل الحالات» without it. **G4:** the password dialog has no close button, Escape leaves it open, «تم» is disabled before «نسخ»; an owner's «تغيير الدور» is `aria-disabled`; the Google-only temporary password is disabled; the link Combobox offers no admin or suspended account; `?unlink=o3&space=numberone` names Yousef. **G5:** at 768 Spaces, Users and Reports draw cards while Owners and Audit draw a `table`; `?space=focus` lists Focus Hub's reports only; `?report=r1` draws the alert above `#prices`; an arrow's name ends «من N»; the live region changes after a move; the sidebar reads «إعدادات المنصة» |
| **My own eyes** on every changed page at 390, **768** and 1440 | gaps, misplaced blocks, anything no assertion names (#59's F2 and #61's eleven fixes were found this way) |

Each assertion is seen failing once against a broken copy before it is trusted.

## 10. Review Focus: what no check exercises

- A screen reader on the Combobox options, the disabled items' reasons, the arrows' live region and the
  password dialog's trapped focus. Real keyboard focus (`:focus-visible`).
- Touch on the Combobox inside a `Dialog` on a phone (scroll and the on-screen keyboard).
- The inline SVG icons against the web's `GlyphIcon`, by eye.
- The handover's own failure after «تم» (`TEMPORARY_PASSWORD_NOT_PENDING`): not drawn.
- Whether «محذوفة» rows read as muted enough in dark mode.

## 11. Commits

All use `docs(design)`, each subject ≤ 50 characters, counted again before each commit. A decision's
`CHANGES.md` line goes in its commit, and `INDEX.md` and the board go in the commit that changes their URL.
There are ten commits, against the usual 3–6, because the prompt asks for commits grouped by decision and G5
holds five separate decisions.

| # | Subject (chars) | Holds |
|---|---|---|
| 1 | `docs(design): a space's own amenities` (37) | G1, `?demo=ownlimit`, the *Batch 2b* heading |
| 2 | `docs(design): amenities are no filter` (37) | G2, the board label |
| 3 | `docs(design): a space's state is two facts` (42) | G3, `olive`, `?status=` |
| 4 | `docs(design): one way to link an owner` (38) | A4, A6, `LinkOwnerDialog`, `?unlink=` both pages, `?q=` on owners, INDEX/board |
| 5 | `docs(design): say what an act does, before it` (45) | A5, AD-021, the password dialog, role, suspension, `?fail=link/role`, `?q=` on users, منى |
| 6 | `docs(design): the admin's lists at 768` (38) | A7, `AdminList`, the filters, the stale chip, `?space=`, `?field=` |
| 7 | `docs(design): the overview is a work queue` (42) | A8, the reply requirement, `?report=` in the editor, DI-21/22 if approved |
| 8 | `docs(design): the lookups say what moved` (40) | AD-024…027, P8's exception, the icons |
| 9 | `docs(design): the audit log leads somewhere` (43) | AD-028, DI-25 if approved |
| 10 | `docs(design): settings: one width, one name` (43) | AD-029 |

PR title: `design: the rest of the admin's dashboard`. Labels `docs` and `area:docs`, assigned to the owner. The
analyst reviews it. Not merged.

## 12. Verification (phase 4)

There is no product code, so the workflow's exception applies: **`npm run format:check`** and **`npm run
check:links`** on the head. Reported honestly: `.prettierignore` excludes `docs/design/` and `*.md`. Then:

- the two scripts at every commit;
- the §9 browser pass on **5346** (`npx serve -l 5346` from `docs/design/prototype`), covering all eight admin
  pages and their parameters, `Admin space edit.html` (`?id=golden`, `?id=focus`, `?report=r1`,
  `?demo=ownlimit`) and `Owner space profile.html`, at 390, 768 and 1440, Arabic and English, light and dark.

No test lanes, no build: there is no code.

**Images:** every "before" is captured from the clean tree before the first edit. Pairs are named after the
decision (`G4-users-768-before.png` / `-after.png`) and never committed. The server and Chrome are stopped at
the end, 5346 is checked free, and every background shell is stopped.

## 13. Decisions needed from the owner

1. **S1–S15:** approve as recommended, or name the ones to drop. S5 (handover required), S6 (no radio step)
   and S10 (inline lucide SVGs) matter most.
2. **DI-21, DI-25:** fold, as recommended.
3. **DI-22:** one colour for "missing" in the prototype (`warning`, as A8). Folding it changes nothing in the
   web. Fold it, or leave the list without missing groups.
4. **DI-23, DI-24:** record only. They go to worker A (the `DataTable` prop) and to the analyst (the users
   row).
