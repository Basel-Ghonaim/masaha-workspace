# Design fix 5: the owner's management, in the prototype

Planner: Claude Code (Opus 5.5). Planned in `C:\Users\basel\masaha-design-b`, detached at `origin/main`
`e30a86c`, tree clean, fetched. **The build runs in `C:\Users\basel\masaha-design`** (the worktree the prompt
names, at the same commit), on branch `design/owner`, prototype served on **5346**. Subagents used: 1 of 2
(a read-only search of the API's documents). No branch cut, no file of the repository edited.

**Departure, stated:** this plan was written from the `masaha-design-b` worktree, which the account batch's
prompt gives to the other design worker. Nothing was edited there. The executor builds in `masaha-design`.

**How to read this plan.** It is an execution script. Every Arabic string is followed by its English, as
`«عربي» / "English"`; write each as `tr('عربي', 'English')`. Where a block says *quote*, the lines are the
current code, to find the place. Line numbers are those of `e30a86c`; find by the quoted text, not the
number. Nothing here is "as appropriate": where a choice existed, it is taken, and §4 says why.

---

## 1. Summary and contract

### Summary
Batch 5 of the design review (the owner's management) is applied to the prototype, as the owner amended it:
- **The phone's top bar** keeps the menu, the title, P2's state control and P1's «⋯»; the account moves
  to the head of the drawer (DI-10, decided 2026-10-13).
- **No money on the overview** (O3 amended): the overview is a work queue of counts and links.
- **One editor** (O1): the owner's Space profile is the A1 editor, with prices as a link row; capacity
  and the stay limit move to Settings (O2).
- **Packages & prices** (O6, O8): the AD-008 table with its own date and confirm, and the private
  packages as rows; the package sheet holds what the model holds, and **a package's price is above zero**.
- **Announcements** (O9–O11, OW-014): the model's fields only; end now, delete, start now, no end; the
  closure extension is its own destructive action once the closure has started.
- **Staff** (O4, OW-017–019), **data reports** (O12), **finance** (OW-015, OW-016), **settings**
  (OW-021) and a new **owner's audit log** (O13).
- **Arabic plurals** (O5) through one helper.

**The editor boundary holds:** nothing the admin's editor (`Admin space edit.html`) shows changes. Three
small, default-preserving props are added to shared editor parts for the owner's pages only (§3.3), and
the dead `CapacitySection` leaves `profile-b.jsx`. Every defect found in the shared editor is recorded in
§4, not built.

### Scope
Inside `docs/design/` only:
- the owner's pages: `Owner overview.html`, `Owner space profile.html`, `Packages.html`, `Announcements.html`,
  `Staff.html`, `Finance.html`, `Owner settings.html`, `Data reports.html`, and a **new** `Owner audit.html`;
- `prototype/masaha/owner.jsx`, `owner-data.js`; `profile-a.jsx` / `profile-b.jsx` only as §3.3 says;
- `Flows - states.html` (one new section, eight relabelled frames), `CHANGES.md` (a *Batch 5* section),
  `INDEX.md` (a parameters table, one new section, eight relabelled rows), `README.md` (counts),
  `SCREENS.md` (board sections, the audit page).

### Acceptance criteria (the reviewer ticks each)
- [ ] **AC1 · DI-10.** Below 768 the owner's and reception's top bar holds only the menu button, the
      title (truncated), «⋯» when the page has actions, and P2's state control; no avatar. The drawer opens
      with an account row (avatar, name · role, email) at its head, opening the one account menu without
      the theme and language items (the drawer's foot has them). From 768 the bar is unchanged.
- [ ] **AC2 · O5.** No owner page shows «1 أيام», «2 أيام», «1 زيارات», «( 2 )» or a count glued to one
      form: the ending subscriptions read «ينتهي اليوم / غدًا / بعد يومين / بعد 3 أيام / بعد 11 يومًا»;
      the announcements' tab counts are `Badge`s.
- [ ] **AC3 · O3 amended.** `Owner overview.html` shows **no amount of money anywhere** (no ₪). Its first
      card «يحتاج انتباهك» lists, as counts and links: stale or missing groups (prices → `Packages.html#prices`),
      new reports, uncollected visits today, customers who owe, a started closure without its extension,
      capacity not set; each row's action leads there; no «المعلومات ما زالت صحيحة» on the overview.
      `?demo=clear` shows «كل شيء على ما يرام». No bottom bar and no top-bar desk shortcut.
- [ ] **AC4 · O1.** `Owner space profile.html` shows A1's sections with dates from the sample, A2's
      checklist when a group is missing (`?demo=missing`), prices as a link row to `Packages.html#prices`,
      the gallery, and no capacity, hide or delete. `Admin space edit.html?id=golden` and `?id=focus` look
      exactly as on `main` (compare the before/after images).
- [ ] **AC5 · O2 + OW-021.** `Owner settings.html#attendance` lands on one card «الحضور والحالة المباشرة»
      (capacity, auto check-out at closing, auto check-out after N hours). Rounding's first choice reads
      «تقريب لأعلى بعد [15] دقيقة» with a live example; student prices for visits start on; `max-w-3xl`.
- [ ] **AC6 · O6, O8.** `Packages.html` has two h2 sections, «الأسعار المعلنة» (the AD-008 table, dated
      «قبل 34 يومًا», «قديمة», «حفظ» and «المعلومات ما زالت صحيحة») and «الباقات الخاصة» (rows: name, terms,
      price, «متاحة في المكتب» switch, «تعديل»; a paused row muted). `Packages.html#prices` lands on the table.
      Every «الأسعار» link of the owner's pages goes to `Packages.html#prices`.
- [ ] **AC7 · O8 + price above zero.** The package sheet: name; validity (required); «الحدود» as a
      four-chip `ToggleGroup type="multiple"`, each chip revealing its field; days a week 1–7; one billing
      choice «سعر ثابت · بالساعة · باليوم» with its labelled amount, refused at 0; «لمن» and the space's own
      shifts (`?demo=noshifts`: the reason and the link); «اسم مستخدم لباقة أخرى» on a repeated name.
- [ ] **AC8 · O9, OW-014.** The announcement sheet has «نص الإعلان بالعربية» (required) and «نص الإعلان
      بالإنجليزية» (optional), the type as a `RadioGroup` with hints, and no title field; no card says
      «أنشأه». Type badges are `neutral`, `warning` for outage and closure.
- [ ] **AC9 · O10.** An active card offers «إنهاء الآن» (at once, toast with «تراجع»); a scheduled card
      «حذف» (`AlertDialog`, destructive); the sheet's «يبدأ: الآن · في موعد» and «ينتهي: في موعد · بلا
      موعد»; a closure's sheet says the space shows «مغلق الآن» for the period.
- [ ] **AC10 · O11.** The sheet has one primary. A started, unextended closure's card offers the owner
      «تمديد الاشتراكات», opening a destructive `AlertDialog` with «عدد الأيام» (≥ 1), the count and the
      days in words, «لا يمكن التراجع»; reception reads «يمدّد المالك الاشتراكات بعد الإغلاق»; a
      scheduled closure offers no extension.
- [ ] **AC11 · O4, OW-017–019.** Staff columns: name (email under it), status, «أُضيف في», «مقبوضاته
      هذا الشهر», actions; a `warning` «لم يغيّر كلمة المرور المؤقتة بعد»; «إيقاف الوصول» with its true
      consequence; «إعادة الوصول» at once; adding staff in one submit «إضافة إلى الاستقبال», both outcomes
      said first; the password dialog under A5's rules (no X, Escape and outside do nothing, «تم» after
      «نسخ», the handover asked).
- [ ] **AC12 · O12 + A8.** The owner never sees a reporter's name (list, sheet, in-place notice): «زائر»
      and the date. «لم يُعتمد» requires the reply. «تعديل الحقل» lands on the field with the report above
      it and «تم التصحيح» in place.
- [ ] **AC13 · OW-015, OW-016.** Finance has no date range; one «الشهر» `Select` (12 months) drives the
      month-based blocks, each naming its month; charts name their windows; CSV labels say what they export;
      «عليهم مبالغ» pages; «دفعوا في …» shows five and «عرض الكل».
- [ ] **AC14 · O13.** «سجل التدقيق» is in «الفريق والإعدادات» and opens `Owner audit.html`: the admin's
      audit page scoped to Focus Hub, targets as links, `neutral` badges and `destructive` only for the
      acts whose confirmation is destructive, «آخر 30 يومًا», the actor filter (three actors).
- [ ] **AC15 · states.** Every changed page opens under `?state=loading` (lists), `error`, `offline`,
      `403`, `404`, `ratelimit` (settings and sheets), and each new action's `?fail=<key>` (§3) as P7/P8 say.
- [ ] **AC16 · the matrix.** Every changed page and every new frame opens at 390, 768 and 1440, Arabic and
      English, light and dark, with no blank render, no console error, no horizontal overflow; the
      executor looked at each at 390, 768 and 1440 (§7).
- [ ] **AC17 · checks.** `check-parse.mjs` and `check-classes.mjs` pass at every commit; `format:check`
      and `check:links` pass on the head; every new or changed `INDEX.md` URL resolves.
- [ ] **AC18 · the archive.** `CHANGES.md` has a *Batch 5* section, one line per decision, true to what
      was built; `INDEX.md`, the board, `README.md` and `SCREENS.md` agree on the new frames and page.
- [ ] **AC19 · boundaries.** The diff touches none of: `Admin space edit.html`, `shared.jsx`, `auth.jsx`,
      `account.jsx`, the auth and account pages, `Desk.html`, `Customers.html`, `Customer file.html`,
      `Payments.html`, `My payments.html`, `desk-core.jsx`, `desk-sheet.jsx`, `desk-data.js`, `finance.jsx`,
      `admin.jsx`, `admin-data.js`, `_ds/`, `_vendor/`, `screens/`; nothing outside `docs/design/`.

### Out of scope
- The design-system items (OW-010's full-width `Sheet`; worker A) and the rule changes (api-contract §4,
  overview.md, glossary, foundation §13: docs and worker A).
- The API (OW-017's re-access, O12's owner read, the package price's database rule).
- The desk batch's files (listed in AC19), `Admin space edit.html` (Issue #72 waits), the account batch's
  files.
- The shared editor's defects (§4, DI-30–DI-33): recorded only.
- The `screens/` images; anything on *Not in v1* (no code to open Finance — deferred, not v1).

---

## 2. Reading done

- **Bootstrap:** `CLAUDE.md`; the `start-work-item` and `write-plan` skills; `docs/design/README.md`
  (check scripts, the shared-scope rule), `SCREENS.md`, `CHANGES.md` (batches 1, 2a, 2b, 3, whole),
  `INDEX.md` (parameter tables, §29–40, §53), the board's structure and last section.
- **Decisions:** `DECISIONS_OWNER.md` (the *Decided* 2026-10-13 note, the *Amended* O3 note, the *Added*
  DI-10 note, O1–O13, the smaller items, design system, rules changed); `DECISIONS_SHARED.md` (P1–P10 as
  amended, SH-005/006/007).
- **The review:** `REVIEW_OWNER_REPORT.md`, OW-001…OW-022, its tables and *Rules in doubt*.
- **Earlier fix plans and replies:** `FIX_ADMIN_REST_PLAN.md`, its reply and its review fixes (the
  punctuation through `tr()`, `?space=` read only from offered values, the queue counting what the list
  counts).
- **The prompt for the parallel account batch**, for the shared files and numbering.
- **The API's truth** (a subagent's read of `schema.prisma`, the migrations, `data-model.md`,
  `api-contract.md`, `v1-mvp.md`, `features/spaces.md`, `space-links.md`, `users.md`, ADRs 0008–0010,
  `security.md`, `conventions.md`, the glossary, `overview.md`). What shapes the build:
  - `Package`: `validityDays` not null and > 0; `daysPerWeek` 1–7; `hoursPerDay` 1–24; `totalDays`,
    `totalHours` > 0; `billing FIXED | PER_HOUR | PER_DAY` with one `priceAgorot`; `@@unique([spaceId,
    name])`; `isActive`; no DELETE. The database allows a price of 0; the owner decided above zero.
  - `Announcement`: `type GENERAL|OUTAGE|CLOSURE|OFFER|EVENT`, `textAr` required, `textEn` optional,
    `startsAt` required, `endsAt` null = until removed, `endsAt > startsAt`; soft-deleted; **no author**.
    Endpoints are owner **or reception**; the extension is owner only.
  - `ClosureExtension`: once per closure, `days > 0`, owner only, extends the space's active subscriptions.
  - `SpaceManager`: `deactivatedAt`, `createdAt`; re-adding the same person reactivates the link;
    deactivating revokes sessions; `User.mustChangePassword`.
  - `SpaceSettings`: `autoCheckoutAtClosing`, `maxStayMinutes` (null = at closing only, > 0),
    `visitRounding UP_AFTER_MINUTES|NEAREST_HALF_HOUR|PER_MINUTE` with `visitRoundingMinutes` 1–59 (new-space
    default 15), `visitCapAtDayPrice`, `visitStudentPrices` default **true**. Capacity is
    `SpaceOccupancy.capacity` (nullable, > 0), set through `PATCH /manage/spaces/:spaceId`.
  - Photos: 5 MB, JPEG/PNG/**WebP**, 413/415; **no maximum count is documented** (DI-32).
  - Data reports: `OPEN|RESOLVED|DISMISSED`, `resolutionNote` (shown to the reporter), no capacity field.
  - Audit log: `actorId` null = the system (auto check-out); the owner sees the space's entries, customers
    and payments included.
  - Paging: no manage list is an exception yet; packages answered whole is a decided rule change (docs).
- **The prototype:** `owner.jsx`, `owner-data.js`, `profile-a.jsx`, `profile-b.jsx`, `finance.jsx`, the
  eight owner pages, `Admin space edit.html`, `Admin audit.html`, `Admin reports.html` (A8's reply),
  `admin.jsx` (`TempPassDialog`), `shared.jsx` (`AccountMenuContent`, `PageActions`, `useActionRun`,
  `ActionButton`, `ActionAlert`, `RateLimitNote`, `LoadError`, `FilterSheet`, `usePaged`, `DateField`,
  `TimeInput`, `without`), `desk-data.js` (`PRICES`, `SHIFTS`, `PACKAGES`, `unpaid`, `MONTHS`, `monthly`,
  `staffMonth`), the vendored `SidebarProvider` (a phone drawer is a `Sheet`, its open state internal).
- **The prebuilt CSS**, checked class by class for what this plan uses. **Dead (not in
  `_ds_bundle.css`), never to be used:** `md:max-w-32`, `md:w-56`, `md:w-72`, `md:max-w-40`,
  `opacity-60`, `md:self-auto`, `hover:opacity-90`. Present: `max-w-3xl`, `max-w-4xl`, `w-16`, `w-20`,
  `w-24`, `md:w-40`, `md:w-48`, `md:grid-cols-2/3/4`, `lg:grid-cols-3/4`, `xl:grid-cols-3/4`,
  `lg:col-span-2`, `md:flex-row`, `md:items-center`, `md:justify-between`, `md:hidden`, `md:flex`,
  `lg:flex-row`, `gap-0.5`, `line-clamp-2/3`, `border-t`, `section-anchor`, `text-destructive`,
  `hover:bg-muted`, `rounded-xl`, `h-full`.
- **The vendored icons** are only: Arrow{Down,End,Start,Up}, Calendar, Check, Chevron{Down,End,Start,Up},
  ChevronsUpDown, CircleAlert, CircleCheck, Close, Ellipsis, EllipsisVertical, Error, Eye, EyeOff, Info,
  Languages, Loader, LogIn, LogOut, Menu, Moon, Search, SearchX, Select, Sort, Success, Sun, TriangleAlert,
  Users, Variant, Warning (each `…Icon`).
- **Free global names** (checked across every module and page): `AR_PLURAL`, `countText`, `Counted`,
  `DrawerAccount`, `useHashLanding`, `OwnerReportNotice`, `annPeriod`, `annStatus`, `closureDays`,
  `StaffPassDialog`, `ExtendDialog`, `monthLabel`, `MONTH_OPTS`. Use these names exactly.

---

## 3. The decisions, as they will be built

### 3.0 Shared helpers first (in `owner.jsx` and `owner-data.js`)

**`owner-data.js`** — inside the IIFE, before its `return`, add (and add each name to the returned object):
```js
  // The fix phase's sample states: ?demo=missing,nocapacity,clear,noshifts (a comma list).
  const DEMO = (new URLSearchParams(location.search).get('demo') || '').split(',');
  const demo = (k) => DEMO.includes(k);
  const NOW_ISO = '2026-09-29T12:40';
  // A1: each fact group's age in days. Prices are out of date after 30 days, the rest after 60.
  // ?demo=missing takes the amenities back to never saved (A2); ?demo=clear makes every group fresh.
  const groups = demo('clear') ? { profile: 3, hours: 3, prices: 3, amenities: 3, contacts: 3 } : { profile: 14, hours: 12, prices: 34, amenities: 20, contacts: 75 };
  const LIMIT = { prices: 30, other: 60 };
  const missing = demo('missing') ? ['amenities'] : [];
```
`announcements`, `reports` and `audit` are added by §3.6, §3.10 and §3.12. Change the existing
`return { capacity: 40, …` to `capacity: demo('nocapacity') ? null : 40` and add
`demo, NOW_ISO, groups, LIMIT, missing` to it.

**`owner.jsx`** — after the `Num` line (`const Num = ({ children }) => …`), add:
```js
// O5: a counted noun takes the form its number asks for — Arabic has six (Intl.PluralRules('ar'):
// zero, one, two, few, many, other). `ar` gives the forms, {n} where the number goes, `other` the
// fallback; `en` is [one, other]. `Counted` isolates the number as `Num` does.
const AR_PLURAL = new Intl.PluralRules('ar');
const countForm = (n, ar, en) => (LANG === 'en' ? en[n === 1 ? 0 : 1] : ar[AR_PLURAL.select(n)] || ar.other);
const countText = (n, ar, en) => countForm(n, ar, en).replace('{n}', String(n));
function Counted({ n, ar, en }) {
  const parts = countForm(n, ar, en).split('{n}');
  return parts.length < 2 ? parts[0] : <>{parts[0]}<Num>{n}</Num>{parts[1]}</>;
}
```
Rename nothing else. Extend the `Object.assign(window, { … })` at the end of `owner.jsx` with
`AR_PLURAL, countText, Counted` (and, as later blocks add them, `useHashLanding, OwnerReportNotice,
annPeriod, annStatus, closureDays`). `countForm` is internal (do not export it; it is not a generic
name either — leave it top-level).

**The forms used** (one constant per noun, written where first used; each object exactly as here):
| Constant | `ar` | `en` |
|---|---|---|
| `F_DAYS_AGO` | `{ one: 'قبل يوم واحد', two: 'قبل يومين', few: 'قبل {n} أيام', many: 'قبل {n} يومًا', other: 'قبل {n} يوم' }` | `['{n} day ago', '{n} days ago']` |
| `F_DAYS_IN` | `{ two: 'بعد يومين', few: 'بعد {n} أيام', many: 'بعد {n} يومًا', other: 'بعد {n} يوم' }` (0 and 1 handled before) | `['in {n} day', 'in {n} days']` |
| `F_DAYS_ACC` | `{ one: 'يومًا واحدًا', two: 'يومين', few: '{n} أيام', many: '{n} يومًا', other: '{n} يوم' }` | `['{n} day', '{n} days']` |
| `F_SUBS` | `{ zero: 'لا اشتراكات', one: 'اشتراك واحد', two: 'اشتراكان', few: '{n} اشتراكات', many: '{n} اشتراكًا', other: '{n} اشتراك' }` | `['{n} subscription', '{n} subscriptions']` |
| `F_SUBS_ACTIVE_ACC` | `{ one: 'اشتراك واحد نشط', two: 'اشتراكين نشطين', few: '{n} اشتراكات نشطة', many: '{n} اشتراكًا نشطًا', other: '{n} اشتراك نشط' }` | `['{n} active subscription', '{n} active subscriptions']` |
| `F_EXTEND_VERB` | `{ one: 'مدّد اشتراكًا واحدًا', two: 'مدّد اشتراكين', few: 'مدّد {n} اشتراكات', many: 'مدّد {n} اشتراكًا', other: 'مدّد {n} اشتراك' }` | `['Extend {n} subscription', 'Extend {n} subscriptions']` |
| `F_EXTENDED` | `{ one: 'مُدِّد اشتراك واحد', two: 'مُدِّد اشتراكان', few: 'مُدِّد {n} اشتراكات', many: 'مُدِّد {n} اشتراكًا', other: 'مُدِّد {n} اشتراك' }` | `['{n} subscription extended', '{n} subscriptions extended']` |
| `F_VISITS` | `{ zero: 'لا زيارات', one: 'زيارة واحدة', two: 'زيارتان', few: '{n} زيارات', many: '{n} زيارة', other: '{n} زيارة' }` | `['{n} visit', '{n} visits']` |
| `F_UNPAID` | `{ one: 'زيارة واحدة لم تُحصَّل اليوم', two: 'زيارتان لم تُحصَّلا اليوم', few: '{n} زيارات لم تُحصَّل اليوم', many: '{n} زيارة لم تُحصَّل اليوم', other: '{n} زيارة لم تُحصَّل اليوم' }` | `['{n} visit not collected today', '{n} visits not collected today']` |
| `F_SUBSCRIBERS` | `{ zero: 'لا مشتركين', one: 'مشترك واحد', two: 'مشتركان', few: '{n} مشتركين', many: '{n} مشتركًا', other: '{n} مشترك' }` | `['{n} subscriber', '{n} subscribers']` |
| `F_NEW_REPORTS` | `{ one: 'بلاغ جديد', two: 'بلاغان جديدان', few: '{n} بلاغات جديدة', many: '{n} بلاغًا جديدًا', other: '{n} بلاغ جديد' }` | `['{n} new report', '{n} new reports']` |
| `F_OWE` | `{ one: 'زبون واحد عليه مبلغ', two: 'زبونان عليهما مبالغ', few: '{n} زبائن عليهم مبالغ', many: '{n} زبونًا عليهم مبالغ', other: '{n} زبون عليهم مبالغ' }` | `['{n} customer owes money', '{n} customers owe money']` |
| `F_CUSTOMERS` | `{ zero: 'لا زبائن', one: 'زبون واحد', two: 'زبونان', few: '{n} زبائن', many: '{n} زبونًا', other: '{n} زبون' }` | `['{n} customer', '{n} customers']` |
| `F_SECTIONS_IN` | `{ one: 'قسم واحد', two: 'قسمين', few: '{n} أقسام', many: '{n} قسمًا', other: '{n} قسم' }` | `['{n} section', '{n} sections']` |
| `F_MINUTES` | `{ one: 'دقيقة', two: 'دقيقتين', few: '{n} دقائق', many: '{n} دقيقة', other: '{n} دقيقة' }` | `['{n} min', '{n} min']` |
| `F_VALID` | `{ one: 'صالحة يومًا واحدًا', two: 'صالحة يومين', few: 'صالحة {n} أيام', many: 'صالحة {n} يومًا', other: 'صالحة {n} يوم' }` | `['valid {n} day', 'valid {n} days']` |
| `F_DAYS_N` | `{ one: 'يوم واحد', two: 'يومان', few: '{n} أيام', many: '{n} يومًا', other: '{n} يوم' }` | `['{n} day', '{n} days']` |
Put `F_DAYS_AGO`, `F_DAYS_IN`, `F_DAYS_ACC`, `F_SUBS`, `F_SUBS_ACTIVE_ACC`, `F_EXTEND_VERB`, `F_EXTENDED`,
`F_VISITS`, `F_UNPAID`, `F_SUBSCRIBERS`, `F_NEW_REPORTS`, `F_OWE`, `F_CUSTOMERS`, `F_SECTIONS_IN`,
`F_MINUTES`, `F_VALID`, `F_DAYS_N` in `owner.jsx` right after `Counted`, as `const F_… = { ar: {…}, en: […] };`
— i.e. each constant is `{ ar, en }`, used as `countText(n, F_X.ar, F_X.en)` / `<Counted n={n} ar={F_X.ar}
en={F_X.en} />`. Export them all in the `Object.assign`. (`F_` names are checked free.)

**`useHashLanding`** (owner.jsx, before `OwnerShell`): the page renders after the browser looked for the
anchor, so a page opened at `#prices`, `#attendance` or `#report` brings that element into view:
```js
// The page renders after the browser looked for `#…`, so the anchor brings itself into view (as the
// admin's report notice does).
function useHashLanding() {
  React.useEffect(() => {
    const id = decodeURIComponent(location.hash.slice(1));
    if (!id) return undefined;
    const t = setTimeout(() => { const el = document.getElementById(id); if (el) el.scrollIntoView({ block: 'start' }); }, 120);
    return () => clearTimeout(t);
  }, []);
}
```
Call `useHashLanding();` as the first line of `OwnerShell`'s body (before `const ov = useOverride();`).

### 3.1 DI-10 — the phone's top bar (owner.jsx; commit 1)
- **The bar.** In `OwnerShell`, *quote*:
  `<div className="ms-auto flex items-center gap-1">` → replace with
  `<div className="ms-auto hidden items-center gap-1 md:flex">`. The language and theme toggles inside it
  keep their own `hidden md:inline-flex`; `OwnerUserMenu` is now shown from 768 only. Nothing else in the
  header changes; its order stays: `SidebarTrigger`, `h1` (`min-w-0 flex-1 truncate`), `PageActions`,
  `PublicStateControl`.
- **The drawer's head.** Add, before `function OwnerShell`:
```js
// DI-10 (decided 2026-10-13): on a phone the bar has no room for the account, so it heads the drawer,
// whose foot already holds the theme and the language — so the menu opened here leaves them out.
function DrawerAccount() {
  const u = STAFF;
  return (
    <ODropdown dir={DIR}>
      <ODropdownTrigger asChild>
        <button type="button" className="flex w-full items-center gap-3 rounded-md p-2 text-start hover:bg-sidebar-accent focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring" aria-label={tr('قائمة الحساب', 'Account menu') + ' — ' + u.name}>
          <OAvatar size="sm" aria-hidden="true"><OAvatarFallback>{u.name[0]}</OAvatarFallback></OAvatar>
          <span className="flex min-w-0 flex-1 flex-col">
            <span className="truncate text-label">{u.name} · {u.role}</span>
            <span dir="ltr" className="truncate text-caption text-muted-foreground">{u.email}</span>
          </span>
          <ChevronsUpDownIcon className="size-4 text-muted-foreground" aria-hidden="true" />
        </button>
      </ODropdownTrigger>
      <AccountMenuContent user={u} area="dashboard" onSignOut={() => { location.href = carryParams('Home.html?auth=0'); }} />
    </ODropdown>
  );
}
```
  (`AccountMenuContent` adds the theme and language items only when `setTheme` is passed; it is not.)
- In `OwnerShell`, add `const phone = !useIsTablet();` on the line after `const rail = …`; then *quote*
  `<div className="sidebar-stick">` and insert as its first child
  `{phone && <div className="border-b border-sidebar-border p-2"><DrawerAccount /></div>}`.
  (Check `border-sidebar-border` with `check-classes.mjs`; if it is reported dead, use `border-border`.)
- **A frame for it:** `?drawer=open` opens the drawer on a phone. In `OwnerShell`, after `const phone = …`:
```js
  // ?drawer=open: the phone's drawer, open, for the board (its open state is the layer's own).
  React.useEffect(() => { if (phone && pageParams.get('drawer') === 'open') { const b = document.querySelector('[data-slot=sidebar-inset] > header button'); if (b) b.click(); } }, []);
```
- **Applies to every page on `OwnerShell`**, the desk's pages included (they are not edited; they are
  looked at, §7). Strings: none new besides those quoted.

### 3.2 O5 — Arabic plurals (commit 2)
Uses §3.0's helper (it lands in this commit, with the `F_` constants).
- `Owner overview.html` *quote*
  `{sub.name} · {d === 0 ? tr('ينتهي اليوم', 'Ends today') : tr(`ينتهي بعد ${d} أيام`, `Ends in ${d} days`)}` →
  `{sub.name} · {d === 0 ? tr('ينتهي اليوم', 'Ends today') : d === 1 ? tr('ينتهي غدًا', 'Ends tomorrow') : <>{tr('ينتهي ', 'Ends ')}<Counted n={d} ar={F_DAYS_IN.ar} en={F_DAYS_IN.en} /></>}`;
  and `<CardDescription><Num>{ending.length}</Num> {tr('اشتراكات', 'subscriptions')}</CardDescription>` →
  `<CardDescription><Counted n={ending.length} ar={F_SUBS.ar} en={F_SUBS.en} /></CardDescription>`.
  (`MoneyRow` goes in commit 11; leave it here.)
- `Announcements.html` *quote* the three `TabsTrigger`s, e.g.
  `<TabsTrigger value="active">{tr('نشطة', 'Active')} (<Num>{count('active')}</Num>)</TabsTrigger>` →
  `<TabsTrigger value="active">{tr('نشطة', 'Active')}<Badge variant="neutral"><Num>{count('active')}</Num></Badge></TabsTrigger>`
  (same for `scheduled` «مجدولة» and `ended` «منتهية»).
- `Finance.html` `DebtsTab` *quote* `helper={<><Num>{debtors.length}</Num> {tr('زبائن', 'customers')}</>}` →
  `helper={<Counted n={debtors.length} ar={F_CUSTOMERS.ar} en={F_CUSTOMERS.en} />}`; *quote*
  `helper={<><Num>{credits.length}</Num> {tr('زبون دفع مقدمًا', 'prepaid')}</>}` →
  `helper={<><Counted n={credits.length} ar={F_CUSTOMERS.ar} en={F_CUSTOMERS.en} />{tr(' دفعوا مقدمًا', ' paid in advance')}</>}`;
  the «دفعوا هذا الشهر» tile's helper `tr('زبائن', 'customers')` → drop the helper; its value becomes
  `<Counted n={paidThisMonth.length} ar={F_CUSTOMERS.ar} en={F_CUSTOMERS.en} />`.
- `Owner space profile.html` *quote* the unsaved alert
  `tr(`لديك تغييرات غير محفوظة في ${dirty} ${dirty === 1 ? 'قسم' : 'أقسام'}. ستُفقد إذا غادرت الصفحة.`, …)` →
  `<>{tr('لديك تغييرات غير محفوظة في ', 'You have unsaved changes in ')}<Counted n={dirty} ar={F_SECTIONS_IN.ar} en={F_SECTIONS_IN.en} />{tr('. ستُفقد إذا غادرت الصفحة.', '. They’ll be lost if you leave the page.')}</>`.
- Every count added by later commits uses these constants; none glues a number to one form.

### 3.3 O1 + O6 — one editor; prices on their page (commit 3)
**Shared parts — default-preserving props only (the admin's editor passes none, so it is unchanged):**
- `profile-b.jsx`, `PricesSection`: *quote* `function PricesSection({ space, meta = {} }) {` →
  `function PricesSection({ space, meta = {}, title, description, hoursHref = '#hours' }) {`. In its
  `ProfileSection`, *quote* `title={tr('الأسعار', 'Prices')}` → `title={title || tr('الأسعار', 'Prices')}` and
  `description={tr('للعرض فقط · الدفع في المساحة', 'Display only · Pay at the space')}` →
  `description={description || tr('للعرض فقط · الدفع في المساحة', 'Display only · Pay at the space')}`; in the
  no-shifts line *quote* `<a href="#hours">` → `<a href={hoursHref}>`. Add above the function:
  `// The owner's Packages & prices page names the table «الأسعار المعلنة» beside its private packages,
  and its hours live on another page; the admin's editor passes none of these.`
- Nothing else in `profile-a.jsx` / `profile-b.jsx` changes in this commit.

**`owner-data.js`:** §3.0's `demo`, `NOW_ISO`, `groups`, `LIMIT`, `missing` (if not already added).

**`Owner space profile.html`:**
- Scripts: unchanged (`profile-a.jsx`, `profile-b.jsx` are loaded). The capacity section stays in this
  commit; commit 4 removes it.
- Add after `const SECTIONS …` (`O` is already the global `window.OWNER` from `owner.jsx`; **do not
  redeclare it**):
```js
// A1: each group's date from the sample; a group never saved is `missing` (A2).
const groupMeta = (g) => (O.missing.includes(g) ? { missing: true } : { updated: ago(O.groups[g]), stale: O.groups[g] > (g === 'prices' ? O.LIMIT.prices : O.LIMIT.other) });
```
- In `ProfileScreen`, between the dirty `Alert` and `<SpaceSection …/>`, add
  `<MissingChecklist names={Object.fromEntries(SECTIONS())} missing={O.missing} />`.
- Pass meta: `<SpaceSection space={space} meta={groupMeta('profile')} />`,
  `<HoursSection meta={groupMeta('hours')} />`, `<AmenitiesSection space={space} meta={groupMeta('amenities')} />`,
  `<ContactsSection space={space} meta={groupMeta('contacts')} />`.
- **The prices link row** replaces the stub card (*quote* the whole `<Card id="prices" …>…</Card>` with
  «انتقلت الأسعار المعلنة…»):
```jsx
          {/* O1/O6: the prices group lives on Packages & prices, where its table is saved and confirmed;
              here it is one row, with its date, so the profile still lists all five groups. */}
          <Card id="prices" className="section-anchor">
            <CardHeader>
              <SectionTitle>{tr('الأسعار', 'Prices')}</SectionTitle>
              <CardDescription className="flex flex-wrap items-center gap-x-2 gap-y-1">
                <span>{tr('تُعدَّل وتُؤكَّد في الباقات والأسعار ·', 'Edited and confirmed in Packages & prices ·')}</span>
                {groupMeta('prices').missing ? <span>{tr('لم تُضف بعد', 'Not added yet')}</span> : <span>{tr('آخر تحديث', 'Updated')} {groupMeta('prices').updated}</span>}
                {groupMeta('prices').stale && <Badge variant="warning">{tr('قديمة', 'Out of date')}</Badge>}
              </CardDescription>
              <CardAction><Button variant="outline" size="sm" asChild><a href="Packages.html#prices">{tr('الباقات والأسعار', 'Packages & prices')}<ArrowEndIcon /></a></Button></CardAction>
            </CardHeader>
          </Card>
```
  Add `Badge` to the page's destructuring from `window.MasahaDesignSystem`.
- The intro line stays: «كل قسم يُحفظ وحده، ويظهر للزوار فور الحفظ.» + «عرض الصفحة العامة» (O1's head).
- Owner-only by construction: no «إدارة قائمة المرافق» (no `manage` prop), no hide, delete or owners.

**`Packages.html` (section 1 here; section 2 is commit 5):**
- At the top of the page script, after `const space = …`: `publish('shifts', SAMPLE_SHIFTS());` with the
  comment `// The space's saved shifts, which the price table and the package sheet offer; on the profile
  the hours section publishes them, and it is not on this page.` (`?demo=noshifts` is commit 5's.)
- *Quote* the first `<section className="flex flex-col gap-3" aria-labelledby="pub">…</section>` → replace with:
```jsx
      <p className="text-body-sm text-muted-foreground">{tr('أسعار الأسبوع والشهر تُختار أيضًا في المكتب عند إنشاء اشتراك.', 'Week and month prices are also chosen at the desk when creating a subscription.')}</p>
      <PricesSection space={space} title={tr('الأسعار المعلنة', 'Published prices')} description={tr('تظهر في صفحة المساحة · للعرض فقط · الدفع في المساحة', 'Shown on the space page · Display only · Pay at the space')} meta={{ updated: ago(O.groups.prices), stale: O.groups.prices > O.LIMIT.prices }} hoursHref="Owner space profile.html#hours" />
```
  (`PricesSection`'s card has `id="prices"` and an h2 title; the page's own h2 «الأسعار المعلنة» goes —
  the doubled heading of OW-008.) Drop the `confirmable` prop (it did nothing).
- `OwnerShell` lands `#prices` through `useHashLanding` (§3.0) — add `useHashLanding` in this commit.

**Every «الأسعار» link of the owner's pages** goes to `Packages.html#prices`: `Data reports.html`'s
`FIELDS().prices[1]` `'Packages.html'` → `'Packages.html#prices'` (this commit); the overview's queue
(commit 11); the profile's link row (above).

**Not built (the boundary):** O6's «الفترة» and «لمن: الجميع · الطلاب» inside the table (DI-30); the
group-naming save toast (DI-31). See §4.

### 3.4 O2 + OW-021 — capacity and the stay limit in Settings (commit 4)
**`Owner space profile.html`:** drop `['capacity', …]` from `SECTIONS` and `<CapacitySection />` from the page.
**`profile-b.jsx`:** delete `function CapacitySection() {…}` entirely and `CapacitySection` from its
`Object.assign(window, {…})`, with no other change (the admin's editor never rendered it).

**`Owner settings.html`:**
- `SettingsCard`: *quote* `function SettingsCard({ title, description, card, children, onSave }) {` →
  `function SettingsCard({ id, title, description, card, children, onSave }) {` and `<Card>` →
  `<Card id={id} className={id ? 'section-anchor' : undefined}>`.
- The width: *quote* `<div className="flex max-w-2xl flex-col gap-6">` → `max-w-3xl`.
- State: *quote* `const att = useCard({ autoOut: true });` →
  `const att = useCard({ capacity: O.capacity == null ? '' : String(O.capacity), autoOut: true, maxStay: '4' });`
  and add `const [attErr, setAttErr] = React.useState({});`.
- **The card «الحضور والحالة المباشرة»** / "Attendance and the live state" replaces the «الحضور» card
  (*quote* `<SettingsCard title={tr('الحضور', 'Attendance')} card={att}>…</SettingsCard>`):
```jsx
        <SettingsCard id="attendance" title={tr('الحضور والحالة المباشرة', 'Attendance and the live state')} card={att} onSave={saveAtt}>
          <Field label={tr('السعة', 'Capacity')} labelEnd={<span className="text-caption text-muted-foreground">{tr('اختياري', 'Optional')}</span>} error={attErr.capacity}
            helper={tr('لا تظهر للزوار. بها تُحسب الحالة «ممتلئ»؛ بدونها لا تظهر حالة مباشرة.', 'Never shown to visitors. It decides when the space shows «Full»; without it there is no live status.')}>
            <Input inputMode="numeric" dir="ltr" className="w-24" value={att.v.capacity} onChange={(e) => att.set({ capacity: e.target.value.replace(/[^\d]/g, '') })} />
          </Field>
          <Field label={tr('خروج تلقائي عند الإغلاق', 'Automatic check-out at closing')} helper={<>{tr('يُسجَّل خروج الجميع الساعة', 'Everyone is checked out at')} <Num>{DESK.CLOSE}</Num>. {tr('الزيارات غير المدفوعة تظهر في «غير محصّل».', 'Unpaid visits show in «Not collected».')}</>} orientation="horizontal"><Switch checked={att.v.autoOut} onCheckedChange={(b) => att.set({ autoOut: b })} /></Field>
          <Field label={tr('خروج تلقائي بعد (ساعات)', 'Automatic check-out after (hours)')} labelEnd={<span className="text-caption text-muted-foreground">{tr('اختياري', 'Optional')}</span>} error={attErr.maxStay}
            helper={tr('يُسجَّل خروج من يبقى أكثر من هذه المدة، قبل الإغلاق. اتركه فارغًا ليكون الخروج عند الإغلاق فقط.', 'Whoever stays longer is checked out, before closing. Leave it empty to check out at closing only.')}>
            <Input inputMode="numeric" dir="ltr" className="w-20" value={att.v.maxStay} onChange={(e) => att.set({ maxStay: e.target.value.replace(/[^\d]/g, '') })} />
          </Field>
        </SettingsCard>
```
  with, before `return`:
```js
  // O2: capacity (SpaceOccupancy, PATCH /manage/spaces/:id) and the stay limit (SpaceSettings) sit
  // together, since both shape the live state and the check-out; one save sends both.
  const saveAtt = () => {
    const e = {};
    if (att.v.capacity !== '' && !(Number(att.v.capacity) > 0)) e.capacity = tr('عدد صحيح أكبر من صفر', 'A whole number above zero');
    if (att.v.maxStay !== '' && !(Number(att.v.maxStay) >= 1 && Number(att.v.maxStay) <= 23)) e.maxStay = tr('من 1 إلى 23 ساعة', 'From 1 to 23 hours');
    setAttErr(e);
    if (!Object.keys(e).length) att.save();
  };
```
  Add `Input` to the page's destructuring. The card is first, before «تسعير الزيارات».
- **Rounding (OW-021).** *Quote* `const pr = useCard({ rounding: 'up10', cap: true, student: false });` →
  `const pr = useCard({ rounding: 'up', minutes: '15', cap: true, student: true });` and add
  `const [prErr, setPrErr] = React.useState();`. Replace the `RO` constant and the `RadioGroup` (*quote*
  `const RO = [['up10', …]];` and `<Field label={tr('التقريب', 'Rounding')}>…</Field>`) with:
```jsx
  // OW-021: the model stores N (1–59) for «round up after N minutes»; the example follows it.
  const N = Number(pr.v.minutes) || 0;
  const twoH = (m) => (m <= 0 ? tr('ساعتان', '2 h') : <>{tr('ساعتان و', '2 h ')}<Counted n={m} ar={F_MINUTES.ar} en={F_MINUTES.en} /></>);
  const upExample = N >= 1 && N <= 59 ? <>{twoH(N - 1)}{tr(' = ساعتان · ', ' = 2 h · ')}{twoH(N + 1)}{tr(' = 3 ساعات', ' = 3 h')}</> : null;
```
```jsx
          <Field label={tr('التقريب', 'Rounding')} error={prErr}>
            <RadioGroup value={pr.v.rounding} onValueChange={(r) => { pr.set({ rounding: r }); setPrErr(); }}>
              <div className="flex flex-col gap-1">
                <div className="flex flex-wrap items-center gap-2">
                  <RadioGroupItem value="up" id="round-up" />
                  <label htmlFor="round-up" className="text-body">{tr('تقريب لأعلى بعد', 'Round up after')}</label>
                  <Input inputMode="numeric" dir="ltr" className="w-16" aria-label={tr('دقائق التقريب', 'Rounding minutes')} disabled={pr.v.rounding !== 'up'} value={pr.v.minutes} onChange={(e) => pr.set({ minutes: e.target.value.replace(/[^\d]/g, '').slice(0, 2) })} />
                  <span className="text-body">{tr(N >= 3 && N <= 10 ? 'دقائق' : 'دقيقة', 'minutes')}</span>
                </div>
                {upExample && <span className="ps-8 text-caption text-muted-foreground">{upExample}</span>}
              </div>
              <Field orientation="horizontal" label={<span className="flex flex-col"><span>{tr('لأقرب نصف ساعة', 'To the nearest half hour')}</span><span className="text-caption text-muted-foreground">{tr('ساعتان و20 دقيقة = ساعتان ونصف', '2 h 20 min = 2.5 h')}</span></span>}><RadioGroupItem value="half" /></Field>
              <Field orientation="horizontal" label={<span className="flex flex-col"><span>{tr('بالدقيقة', 'By the minute')}</span><span className="text-caption text-muted-foreground">{tr('ساعتان و20 دقيقة = 7 ₪', '2 h 20 min = ₪7')}</span></span>}><RadioGroupItem value="minute" /></Field>
            </RadioGroup>
          </Field>
```
  (Check `ps-8` and `w-16` with `check-classes.mjs`; if `ps-8` is dead, use `ps-6`, and if both are, drop
  the class.) The minutes word: 3–10 take «دقائق», every other N «دقيقة» (Arabic counting: 11–59 and 1
  take the singular after the number; 2 reads «دقيقتين» but the box shows the digit, so «دقيقة» is the
  label). The card's save validates (pass `onSave={savePr}` to its `SettingsCard`):
```js
  const savePr = () => { if (pr.v.rounding === 'up' && !(N >= 1 && N <= 59)) { setPrErr(tr('من 1 إلى 59 دقيقة', 'From 1 to 59 minutes')); return; } setPrErr(); pr.save(); };
```
  Add `Input` (once) to the destructuring. Student prices for visits starts **on** (`student: true`).
- The three cards keep sharing `?fail=save` (each shows `ActionAlert for="save"`): out of scope (§4 DI-38).

**Frames that change:** `INDEX.md` §36 rows «Capacity section — desktop 1440 / phone 390»
(`Owner space profile.html#capacity`) → label «Capacity → Settings «الحضور والحالة المباشرة» — desktop 1440»
(and «— phone 390»), URL `Owner settings.html#attendance`; the board's two frames (lines with
`Owner%20space%20profile.html#capacity`) likewise: `src="Owner%20settings.html#attendance"`, the `<p>` and
`title` set to the new label.

### 3.5 O8 + OW-009 + «price above zero» — packages (commit 5)
**`Packages.html`.**
- **Sample** (*quote* `const INIT = [ … ];`) → replace:
```js
// O8 (OW-009): a package as the model holds it — the validity always, the limits only when set,
// one billing choice (FIXED · PER_HOUR · PER_DAY) and one amount, above zero (the owner, 2026-10-13).
const LIMITS = () => [['totalDays', tr('عدد الأيام', 'Number of days')], ['daysPerWeek', tr('أيام بالأسبوع', 'Days a week')], ['hoursPerDay', tr('ساعات باليوم', 'Hours a day')], ['totalHours', tr('مجموع الساعات', 'Total hours')]];
const INIT = [
  { id: 'p1', name: tr('10 أيام', '10 days'), validity: '45', totalDays: '10', daysPerWeek: '', hoursPerDay: '', totalHours: '', billing: 'fixed', amount: '130', audience: 'all', shift: '', active: true },
  { id: 'p2', name: tr('20 ساعة', '20 hours'), validity: '30', totalDays: '', daysPerWeek: '', hoursPerDay: '', totalHours: '20', billing: 'fixed', amount: '50', audience: 'all', shift: '', active: true },
  { id: 'p3', name: tr('شهر يوم بعد يوم', 'Month, every other day'), validity: '30', totalDays: '', daysPerWeek: '3', hoursPerDay: '', totalHours: '', billing: 'fixed', amount: '180', audience: 'all', shift: '', active: true },
  { id: 'p4', name: tr('صباحي للطلاب', 'Student mornings'), validity: '30', totalDays: '', daysPerWeek: '', hoursPerDay: '5', totalHours: '', billing: 'day', amount: '10', audience: 'students', shift: 'am', active: false }
];
// ?demo=noshifts: a space with no shifts saved, so the sheet says why it offers none.
const SHIFTS_NOW = () => (O.demo('noshifts') ? [] : SAMPLE_SHIFTS());
```
  and change commit 3's `publish('shifts', SAMPLE_SHIFTS());` to `publish('shifts', SHIFTS_NOW());`.
- **`summary(p)`** (*quote* the whole function) → replace (the price is no longer part of the terms):
```js
const priceText = (p) => (p.billing === 'fixed' ? $(p.amount) : p.billing === 'hour' ? tr(`${$(p.amount)} للساعة`, `${$(p.amount)} an hour`) : tr(`${$(p.amount)} لليوم`, `${$(p.amount)} a day`));
function summary(p) {
  const parts = [];
  if (n(p.validity)) parts.push(countText(n(p.validity), F_VALID.ar, F_VALID.en));
  if (n(p.totalDays)) parts.push(countText(n(p.totalDays), F_DAYS_N.ar, F_DAYS_N.en));
  if (n(p.daysPerWeek)) parts.push(countText(n(p.daysPerWeek), F_DAYS_N.ar, F_DAYS_N.en) + tr(' بالأسبوع', ' a week'));
  if (n(p.hoursPerDay)) parts.push(tr(`${p.hoursPerDay} س باليوم`, `${p.hoursPerDay} h a day`));
  if (n(p.totalHours)) parts.push(tr(`رصيد ${p.totalHours} س`, `${p.totalHours} h balance`));
  if (p.audience === 'students') parts.push(tr('للطلاب', 'students'));
  const sh = SHIFTS_NOW().find((x) => x.id === p.shift);
  if (sh) parts.push(tr(sh.ar, sh.en || sh.ar));
  return parts.join(' · ');
}
```
  Delete `Opt` and `NumF` (no longer used).
- **`PackageSheet`** — replace the whole function with this structure (props `{ pkg, list, onClose, onSave }`):
  - State: `blank = { name: '', validity: '30', totalDays: '', daysPerWeek: '', hoursPerDay: '', totalHours: '', billing: 'fixed', amount: '', audience: 'all', shift: '', active: true }`;
    `[v, setV]`, `[err, setErr]`, `[on, setOn]` (the limits turned on), `form = React.useRef(null)`,
    `const { busy, run } = useActionRun('save');`. On open (`useEffect` on `pkg`): `setV({ ...blank, ...pkg })`,
    `setErr({})`, `setOn(LIMITS().map(([k]) => k).filter((k) => pkg && pkg[k]))`.
  - `toggleLimits(next)`: `setOn(next)`; for each key in `LIMITS()` not in `next`, `set({ [k]: '' })`.
  - `submit(e)`: `e.preventDefault()`; build `x`:
    - name empty → `x.name = tr('أدخل اسم الباقة', 'Enter the package name')`; else if
      `list.some((p) => p.id !== v.id && p.name.trim() === v.name.trim())` → `x.name = tr('اسم مستخدم لباقة أخرى', 'Another package has this name')`;
    - validity empty → `x.validity = tr('أدخل الصلاحية بالأيام', 'Enter the validity in days')`; else
      `!(n(v.validity) > 0)` → `tr('عدد صحيح أكبر من صفر', 'A whole number above zero')`;
    - for each `k` in `on`: empty → `x[k] = tr('أدخل العدد أو أطفئ هذا الحد', 'Enter the number, or turn this limit off')`;
      `daysPerWeek` outside 1–7 → `tr('من 1 إلى 7', 'From 1 to 7')`; `hoursPerDay` outside 1–24 →
      `tr('من 1 إلى 24', 'From 1 to 24')`; `totalDays`/`totalHours` not > 0 → `tr('عدد صحيح أكبر من صفر', 'A whole number above zero')`;
    - amount empty → `x.amount = tr('أدخل السعر', 'Enter the price')`; else `!(n(v.amount) > 0)` →
      `tr('أدخل مبلغًا أكبر من صفر', 'Enter an amount above zero')`;
    - `setErr(x)`; if any, `setTimeout(() => { const bad = form.current && form.current.querySelector('[aria-invalid="true"]'); if (bad) bad.focus(); })` and return;
    - else `run(() => onSave({ ...v, name: v.name.trim() }))` (the page's `save` raises the toast).
  - Number inputs sanitise with `latinDigits(e.target.value).replace(/[^\d]/g, '')`.
  - **Markup, in order**, inside `<SheetContent side="end" closeLabel={tr('إغلاق', 'Close')}>`:
    `SheetHeader` (title «تعديل الباقة» / "Edit package" or «باقة جديدة» / "New package"; description
    «باقة خاصة — لا تظهر للزوار، وتُختار في مكتب الاستقبال.» / "Private — never shown to visitors; chosen at the front desk."),
    then `<form ref={form} onSubmit={submit} noValidate className="flex min-h-0 flex-1 flex-col">`,
    `<SheetBody className="flex min-w-0 flex-col gap-5 py-2">` holding:
    1. `<RateLimitNote />` and `<ActionAlert for="save" />`;
    2. `<Field label={tr('اسم الباقة', 'Package name')} error={err.name}><Input value={v.name} onChange={(e) => set({ name: e.target.value })} /></Field>`;
    3. `<Field label={tr('الصلاحية (أيام)', 'Validity (days)')} error={err.validity} helper={tr('ينتهي الاشتراك بعد هذه المدة من بدايته.', 'A subscription ends this long after it starts.')}><Input inputMode="numeric" dir="ltr" className="w-24" value={v.validity} onChange={…validity} /></Field>`;
    4. `<Field label={tr('الحدود', 'Limits')} labelEnd={<Optional />} helper={tr('اختر ما ينطبق؛ يظهر لكل حد حقله.', 'Choose what applies; each limit shows its field.')}>`
       `<ToggleGroup type="multiple" value={on} onValueChange={toggleLimits} className="flex-wrap">{LIMITS().map(([k, l]) => <ToggleGroupItem key={k} value={k}>{l}</ToggleGroupItem>)}</ToggleGroup></Field>`,
       then, for each `[k, l]` of `LIMITS()` with `on.includes(k)`, in that order:
       `<Field key={k} label={l} error={err[k]}><Input inputMode="numeric" dir="ltr" className="w-24" value={v[k]} onChange={(e) => set({ [k]: latinDigits(e.target.value).replace(/[^\d]/g, '') })} /></Field>`
       (`Optional` is `profile-a.jsx`'s global);
    5. `<Field label={tr('طريقة الحساب', 'Billing')}><ToggleGroup type="single" value={v.billing} onValueChange={(b) => b && set({ billing: b })}>` with items
       `fixed` «سعر ثابت» / "Fixed price", `hour` «بالساعة» / "Per hour", `day` «باليوم» / "Per day"`</ToggleGroup></Field>`,
       then `<Field label={v.billing === 'fixed' ? tr('السعر الكلي (₪)', 'Total price (₪)') : v.billing === 'hour' ? tr('سعر الساعة (₪)', 'Price per hour (₪)') : tr('سعر اليوم (₪)', 'Price per day (₪)')} error={err.amount}><Input inputMode="numeric" dir="ltr" className="w-24" value={v.amount} onChange={…amount} /></Field>`;
    6. `<Field label={tr('لمن', 'For')}><ToggleGroup type="single" value={v.audience} onValueChange={(a) => a && set({ audience: a })}>` items
       `all` «الجميع» / "Everyone", `students` «الطلاب» / "Students"`</ToggleGroup></Field>`;
    7. the shift: `const shifts = SHIFTS_NOW();` →
       `<Field label={tr('الوردية', 'Shift')} labelEnd={<Optional />}>{shifts.length ? <ToggleGroup type="single" value={v.shift} onValueChange={(s) => set({ shift: s || '' })}>{shifts.map((x) => <ToggleGroupItem key={x.id} value={x.id}>{tr(x.ar, x.en || x.ar)}</ToggleGroupItem>)}</ToggleGroup> : <p className="text-caption text-muted-foreground">{tr('لا ورديات محفوظة بعد. ', 'No shifts are saved yet. ')}<a href="Owner space profile.html#hours">{tr('أضف ورديات في ساعات العمل أولًا', 'Add shifts in the opening hours first')}</a></p>}</Field>`;
    8. the summary box (kept): `<div className="flex flex-col gap-1 rounded-lg bg-muted p-4" aria-live="polite">` with
       «الملخّص» / "Summary", the name or «باقة بدون اسم» / "Unnamed package", `summary(v)`, and the price line
       `<span className="text-label">{n(v.amount) > 0 ? priceText(v) : tr('بدون سعر بعد', 'No price yet')}</span>`.
    `</SheetBody>`, `<SheetFooter><Button type="submit" className="w-full" loading={busy}>{tr('حفظ الباقة', 'Save package')}</Button></SheetFooter>`.
    (Delete the old «كل الشروط اختيارية ويمكن جمعها.» line.)
- **Section 2 «الباقات الخاصة» as rows** (OW-008). *Quote* the second `<section … aria-labelledby="priv">`
  → keep its heading block (h2 «الباقات الخاصة», line changed to «لا تظهر للزوار · تُختار في المكتب عند
  إنشاء اشتراك» / "Never shown to visitors · chosen at the desk when creating a subscription"; the «باقة
  جديدة» button stays at the row's end, P1). Replace the cards grid with:
```jsx
          <Card>
            <CardContent className="p-0">
              <ul className="divide-y">
                {list.map((p) => (
                  <li key={p.id} className={'flex flex-col gap-3 px-5 py-3 md:flex-row md:items-center md:justify-between ' + (p.active ? '' : 'bg-muted')}>
                    <div className="flex min-w-0 flex-col gap-1">
                      <span className="flex flex-wrap items-center gap-2"><span className="text-label">{p.name}</span>{!p.active && <Badge variant="neutral">{tr('موقوفة', 'Paused')}</Badge>}</span>
                      <span className="text-body-sm text-muted-foreground">{summary(p)}</span>
                    </div>
                    <div className="flex flex-wrap items-center gap-4">
                      <span className="text-label">{priceText(p)}</span>
                      <Field label={tr('متاحة في المكتب', 'Available at the desk')} orientation="horizontal"><Switch checked={p.active} onCheckedChange={(on) => toggle(p, on)} /></Field>
                      <Button size="sm" variant="outline" onClick={() => setEdit(p)} aria-label={tr('تعديل ', 'Edit ') + p.name}>{tr('تعديل', 'Edit')}</Button>
                    </div>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
```
  The empty state (`?state=empty`) stays as it is.
- **Toggle** (O4: pause/resume acts at once, no toast — the row changes): *quote* `const toggle = (p, on) => { … toast(…) … };`
  → `const toggle = (p, on) => setList((l) => l.map((x) => (x.id === p.id ? { ...x, active: on } : x)));`
- `save` keeps its toast «حُفظت الباقة» + the name. Pass `list={list}` to `PackageSheet`.
- The page's `?sheet=new`, `?edit=p4` keep working; new: `?demo=noshifts`, `?fail=save` (in the sheet).

### 3.6 O9, O10, OW-014 — announcements (commit 6)
**`owner-data.js`** — add the sample (moved from the page; the overview reads it in commit 11):
```js
  // O9: an announcement as the model holds it — a type, an Arabic text, an optional English one, a
  // start and an end (null: until it is ended). No title and no author.
  const announcements = [
    { id: 'a1', type: 'closure', textAr: 'مغلقة مؤقتًا من الخميس حتى السبت لصيانة المولّد. نعود يوم الأحد.', textEn: 'Closed Thursday to Saturday for generator maintenance. We reopen on Sunday.', from: '2026-10-01T08:00', to: '2026-10-03T18:00' },
    { id: 'a2', type: 'event', textAr: 'ورشة مجانية عن أدوات العمل عن بُعد يوم الأحد الساعة 11:00 في قاعة الاجتماعات.', textEn: 'A free workshop on remote-work tools on Sunday at 11:00 in the meeting room.', from: '2026-09-27T08:00', to: '2026-10-04T13:00' },
    { id: 'a3', type: 'offer', textAr: 'شهري الطلاب 250 ₪ — أحضر بطاقتك الجامعية إلى الاستقبال.', textEn: 'Student month ₪250 — bring your student card to the front desk.', from: '2026-09-15T08:00', to: null },
    { id: 'a6', type: 'closure', textAr: 'مغلقة بسبب انقطاع الكهرباء في المنطقة.', textEn: 'Closed because of a power cut in the area.', from: '2026-09-24T08:00', to: '2026-09-25T18:00' },
    { id: 'a5', type: 'outage', textAr: 'الإنترنت بطيء هذا الصباح، ونعمل على إصلاحه.', textEn: '', from: '2026-09-22T08:00', to: '2026-09-22T12:00' },
    { id: 'a4', type: 'closure', textAr: 'مغلقة لصيانة المولّد.', textEn: 'Closed for generator maintenance.', from: '2026-09-14T08:00', to: '2026-09-16T18:00', extended: { count: 19, days: 3, by: T('أحمد', 'Ahmad'), on: '2026-09-17' } }
  ];
```
  Return `announcements`. (`?demo=clear` leaves them; the overview's queue ignores them under `clear`.)

**`owner.jsx`** — add (and export) after `useHashLanding`:
```js
// O10: an announcement is active from its start until its end, scheduled before, ended after.
const annStatus = (a) => (a.to && a.to <= O.NOW_ISO ? 'ended' : a.from > O.NOW_ISO ? 'scheduled' : 'active');
// Its period, in dates and times; with no end, «بلا موعد انتهاء».
const annPeriod = (a) => {
  const D = window.DESK; const d = (iso) => D.fmtDate(iso.slice(0, 10)); const t = (iso) => iso.slice(11, 16);
  if (!a.to) return d(a.from) + ' ' + t(a.from) + tr(' · بلا موعد انتهاء', ' · no end');
  return a.from.slice(0, 10) === a.to.slice(0, 10) ? d(a.from) + ' ' + t(a.from) + '–' + t(a.to) : d(a.from) + ' ' + t(a.from) + ' – ' + d(a.to) + ' ' + t(a.to);
};
// O11: the closure's days so far — all of them once it has ended.
const closureDays = (a) => { const D = window.DESK; const end = a.to && a.to <= O.NOW_ISO ? a.to.slice(0, 10) : D.TODAY; return D.daysBetween(a.from.slice(0, 10), end) + 1; };
```
**`Announcements.html`:**
- Delete `const A = DESK.AHMAD, S = DESK.SAMI;`, `INIT`, `statusOf`, `period`, `titleOf`, `daysOf`,
  `ExtendCard`. Keep `affected`. Use `O.announcements`, `annStatus`, `annPeriod`, `closureDays`.
- **Types** (*quote* `const TYPES = () => ({ … });`) → with hints and OW-014's colours:
```js
// OW-014: one quiet colour; attention (warning) only for an outage and a closure. Each type says what it does.
const TYPES = () => ({
  general: [tr('عام', 'General'), 'neutral', tr('خبر أو تنبيه للزوار', 'News or a note for visitors')],
  outage: [tr('انقطاع كهرباء أو إنترنت', 'Power or internet outage'), 'warning', tr('يبقى المكان مفتوحًا، ويُنبَّه الزوار', 'The space stays open; visitors are warned')],
  closure: [tr('إغلاق مؤقت', 'Temporary closure'), 'warning', tr('تظهر المساحة «مغلق الآن» طوال الفترة', 'The space shows «Closed now» for the whole period')],
  offer: [tr('عرض', 'Offer'), 'neutral', tr('سعر أو خدمة لفترة محدودة', 'A price or a service for a limited time')],
  event: [tr('فعالية', 'Event'), 'neutral', tr('ورشة أو لقاء في المساحة', 'A workshop or a meetup at the space')]
});
const textOf = (a) => (LANG === 'en' && a.textEn ? a.textEn : a.textAr);
```
  `STAT` keeps its words; its colours stay (`success`, `info`, `neutral`).
- **`Preview({ a })`**: replace `titleOf(a)`/`t` with `textOf(a) || tr('نص الإعلان', 'Announcement text')`;
  the closure's `Alert` `variant="destructive"` → `variant="warning"`, its `AlertTitle` is the text and
  no `AlertDescription`; the other branch shows the type `Badge` and the text (`text-body-sm`), then
  `annPeriod(a)`; the closure's caption reads `tr('تظهر الحالة «مغلق الآن» خلال', 'The state shows «Closed now» during')} {annPeriod(a)}.`
  When the text is Arabic in an English page, wrap it `<span lang="ar" dir="rtl">` (when `LANG === 'en' && !a.textEn`).
- **The card** (*quote* the `<Card key={a.id}>…</Card>` in `paged.rows.map`) → replace with:
```jsx
            <Card key={a.id}>
              <CardHeader>
                <CardTitle className="flex flex-wrap items-center gap-2"><Badge variant={tv}>{tl}</Badge><span className="text-body-sm text-muted-foreground">{annPeriod(a)}</span></CardTitle>
                <CardAction><Badge variant={sv}>{sl}</Badge></CardAction>
              </CardHeader>
              <CardContent className="flex flex-col gap-2">
                <p className="text-body" lang={LANG === 'en' && !a.textEn ? 'ar' : undefined} dir={LANG === 'en' && !a.textEn ? 'rtl' : undefined}>{textOf(a)}</p>
                {a.type === 'closure' && <ClosureLine a={a} />}
              </CardContent>
              <CardFooter className="flex flex-wrap gap-2">
                <Button size="sm" variant="outline" onClick={() => setEdit(a)}>{st === 'ended' ? tr('عرض', 'View') : tr('تعديل', 'Edit')}</Button>
                {st === 'active' && <Button size="sm" variant="outline" onClick={() => endNow(a)}>{tr('إنهاء الآن', 'End now')}</Button>}
                {st === 'scheduled' && <Button size="sm" variant="outline" onClick={() => setRemoving(a)}>{tr('حذف', 'Delete')}</Button>}
                {extendable(a) && <Button size="sm" variant="outline" onClick={() => setExtending(a)}>{tr('تمديد الاشتراكات', 'Extend subscriptions')}</Button>}
              </CardFooter>
            </Card>
```
  where `st = annStatus(a)`, `[tl, tv] = TYPES()[a.type]`, `[sl, sv] = STAT()[st]`. (`ClosureLine`,
  `extendable`, `setExtending` are commit 7's: in this commit omit the two lines that use them, and the
  closure shows no line.) No «أنشأه».
- **End now** (O10, P9 — reversible, public): in `AnnInner`:
```js
  const { busy: ending, run: runEnd } = useActionRun('end');
  // O10: «إنهاء الآن» sets the end to now and acts at once; «تراجع» puts the old end back.
  const endNow = (a) => runEnd(() => {
    const was = a.to;
    setList((l) => l.map((x) => (x.id === a.id ? { ...x, to: O.NOW_ISO } : x)));
    toast.success(a.type === 'closure' ? tr('انتهى الإغلاق · عادت الحالة تلقائية', 'The closure has ended · the state is automatic again') : tr('انتهى الإعلان', 'The announcement has ended'),
      { action: { label: tr('تراجع', 'Undo'), onClick: () => setList((l) => l.map((x) => (x.id === a.id ? { ...x, to: was } : x))) } });
  });
```
  The «إنهاء الآن» button takes `loading={ending}`. `?fail=end` → `useActionRun`'s failure toast.
- **Delete a scheduled one** (O10, P9 — no restore endpoint): `const [removing, setRemoving] = React.useState(null);` and:
```jsx
      <AlertDialog open={!!removing} onOpenChange={(o) => !o && setRemoving(null)}>
        <AlertDialogContent>
          <AlertDialogHeader><AlertDialogTitle>{tr('حذف الإعلان؟', 'Delete the announcement?')}</AlertDialogTitle><AlertDialogDescription>{tr('يُحذف قبل أن يظهر للزوار، ولا يمكن استرجاعه.', 'It is deleted before visitors see it, and cannot be brought back.')}</AlertDialogDescription></AlertDialogHeader>
          <AlertDialogFooter><AlertDialogCancel>{tr('رجوع', 'Back')}</AlertDialogCancel><AlertDialogAction variant="destructive" onClick={() => { setList((l) => l.filter((x) => x.id !== removing.id)); toast.success(tr('حُذف الإعلان', 'Announcement deleted')); }}>{tr('حذف', 'Delete')}</AlertDialogAction></AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
```
  `?delete=a1` opens it (frame): initial state `pageParams.get('delete') ? O.announcements.find((x) => x.id === pageParams.get('delete')) : null`.
- **List state:** `const [list, setList] = React.useState(pageParams.get('state') === 'empty' ? [] : O.announcements.map((a) => ({ ...a })));`;
  `shown = list.filter((a) => annStatus(a) === tab)`; `count = (s) => list.filter((a) => annStatus(a) === s).length`.
  The `edit` initial state reads `O.announcements`; `?sheet=new&type=<t>` opens a new one of that type.
  `save(v)`: new → `[{ ...v, id: 'a' + Date.now() }, ...l]`; toast «نُشر الإعلان» / "Announcement published"
  or «حُفظ الإعلان» / "Announcement saved". Reception may create, edit, end and delete (the API's
  «owner or reception»).
- **The sheet `AnnSheet({ item, onClose, onSave })`** — replace the body (no `onExtend`):
  - State `v`: `{ type, textAr, textEn, startMode, startDate, startTime, endMode, endDate, endTime }`. For a
    new one: `{ type: item.type || 'general', textAr: '', textEn: '', startMode: 'now', startDate: DESK.TODAY, startTime: DESK.NOW, endMode: 'at', endDate: DESK.TODAY, endTime: DESK.CLOSE }`.
    For an existing one: `startMode: 'at'`, dates and times split from `from`/`to`, `endMode: a.to ? 'at' : 'none'`.
    `const { busy, run } = useActionRun('save');` and `form` ref.
  - `submit`: errors — `textAr` empty → `tr('أدخل نص الإعلان بالعربية', 'Enter the Arabic text')`;
    `endMode === 'at'` and the end (`endDate + 'T' + endTime`) not after the start (`startMode === 'now' ? O.NOW_ISO : startDate + 'T' + startTime`)
    → `x.endTime = tr('النهاية بعد البداية', 'The end comes after the start')`. Focus the first invalid
    (as §3.5). Else `run(() => onSave({ ...(item.id ? { id: item.id, extended: item.extended } : {}), type: v.type, textAr: v.textAr.trim(), textEn: v.textEn.trim(), from: start, to: v.endMode === 'none' ? null : end }))`.
  - Body, in order (`<SheetBody className="flex min-w-0 flex-col gap-5 py-2">`):
    1. `<RateLimitNote />`, `<ActionAlert for="save" />`;
    2. `<Field label={tr('النوع', 'Type')}><RadioGroup value={v.type} onValueChange={(t) => set({ type: t })}>{Object.entries(TYPES()).map(([k, [l, , h]]) => <Field key={k} orientation="horizontal" label={<span className="flex flex-col"><span>{l}</span><span className="text-caption text-muted-foreground">{h}</span></span>}><RadioGroupItem value={k} /></Field>)}</RadioGroup></Field>`
       — careful: `[l, , h]` is array destructuring with a hole, **not** object rest; allowed;
    3. `<Field label={tr('نص الإعلان بالعربية', 'Text in Arabic')} error={err.textAr} helper={tr('جملة أو جملتان يقرؤها الزائر في صفحة المساحة.', 'A sentence or two that visitors read on the space page.')}><Textarea lang="ar" dir="rtl" rows={3} value={v.textAr} onChange={…} /></Field>`;
    4. `<Field label={tr('نص الإعلان بالإنجليزية', 'Text in English')} labelEnd={<span className="text-caption text-muted-foreground">{tr('اختياري', 'Optional')}</span>} helper={tr('يظهر في الواجهة الإنجليزية؛ بدونه يظهر النص العربي.', 'Shown in the English interface; without it the Arabic text shows.')}><Textarea lang="en" dir="ltr" rows={3} value={v.textEn} onChange={…} /></Field>`;
    5. `<Field label={tr('يبدأ', 'Starts')}><ToggleGroup type="single" value={v.startMode} onValueChange={(m) => m && set({ startMode: m })}>` items `now` «الآن» / "Now", `at` «في موعد» / "At a time" `</ToggleGroup></Field>`;
       when `at`: `<div className="grid grid-cols-2 gap-3"><DateField label={tr('التاريخ', 'Date')} value={v.startDate} onChange={(x) => set({ startDate: x })} /><Field label={tr('الساعة', 'Time')}><TimeInput value={v.startTime} onChange={(x) => set({ startTime: x })} /></Field></div>`;
    6. `<Field label={tr('ينتهي', 'Ends')} helper={v.endMode === 'none' ? tr('يبقى حتى تنهيه.', 'It stays until you end it.') : undefined}><ToggleGroup type="single" value={v.endMode} onValueChange={(m) => m && set({ endMode: m })}>` items `at` «في موعد» / "At a time", `none` «بلا موعد» / "No end" `</ToggleGroup></Field>`;
       when `at`: the same pair, with `error={err.endTime}` on the time `Field`;
    7. for a closure, `<Alert variant="warning"><AlertDescription>{tr('تظهر المساحة «مغلق الآن» للزوار طوال هذه الفترة.', 'Visitors see the space as «Closed now» for this whole period.')}</AlertDescription></Alert>`;
    8. `<Preview a={{ type: v.type, textAr: v.textAr, textEn: v.textEn, from: start, to: v.endMode === 'none' ? null : end }} />`.
  - Footer: one primary, `<Button type="submit" className="w-full" loading={busy}>{item && item.id ? tr('حفظ', 'Save') : tr('نشر الإعلان', 'Publish')}</Button>`.
  - Delete the old «بعد الحفظ يمكنك تمديد…» lines.
- **Phone width:** every field is one column inside the sheet (the two-column date/time pair is
  `grid-cols-2` of a `DatePicker` trigger and a 5-character time box; look at 390 — if it overflows,
  stack it: `grid gap-3 md:grid-cols-2`).
- **Frames that change** (`INDEX.md` §38 and the board): `Announcements.html?tab=scheduled&edit=a1`
  «Scheduled closure · extend (owner)» → label «Scheduled closure · edit (owner)»; the reception pair
  (`?role=reception&tab=scheduled&edit=a1`) «Closure · reception sees note» → «Scheduled closure · edit
  (reception)»; `Announcements.html?tab=ended&edit=a4` «Ended closure · extension done» → URL
  `Announcements.html?tab=ended`, label «Ended · one closure extended, one to extend». `README.md`'s known
  limit «One older frame renders with an error: `Announcements.html?tab=ended&edit=a4`…» — delete that
  bullet once `?tab=ended&edit=a4` opens with no console error (check it; if it still errors, keep the
  bullet and record it in the report).

### 3.7 O11 — the closure extension, its own action (commit 7)
**`Announcements.html`:**
- Helpers (page level):
```js
// O11: once a closure has started, the owner may extend the active subscriptions by its days — once.
const extendable = (a) => IS_OWNER && a.type === 'closure' && annStatus(a) !== 'scheduled' && !a.extended;
```
- `ClosureLine({ a })`:
  - extended → `<span className="flex items-center gap-2 text-caption text-muted-foreground"><CircleCheckIcon className="size-4" aria-hidden="true" /><Counted n={a.extended.count} ar={F_EXTENDED.ar} en={F_EXTENDED.en} />{' '}<Counted n={a.extended.days} ar={F_DAYS_ACC.ar} en={F_DAYS_ACC.en} /> · {a.extended.by} · {DESK.fmtDate(a.extended.on, true)}</span>`;
  - scheduled → caption `tr('يمكن تمديد الاشتراكات بعد أن يبدأ الإغلاق.', 'Subscriptions can be extended once the closure has started.')}` (owner) /
    `tr('يمدّد المالك الاشتراكات بعد الإغلاق.', 'The owner extends subscriptions after the closure.')` (reception);
  - started, not extended → owner: nothing (the footer's button says it); reception: the same reception caption.
- Add the two lines §3.6 left out of the card (`ClosureLine`, the «تمديد الاشتراكات» button).
- **`ExtendDialog({ a, onClose, onDone })`**:
```jsx
function ExtendDialog({ a, onClose, onDone }) {
  const [days, setDays] = React.useState('');
  const [err, setErr] = React.useState(null);
  const { run } = useActionRun('extend');
  React.useEffect(() => { if (a) { setDays(String(closureDays(a))); setErr(null); } }, [a]);
  const d = Number(days) || 0;
  const go = (e) => {
    if (!(d >= 1)) { e.preventDefault(); setErr(tr('يومًا واحدًا على الأقل', 'At least one day')); return; }
    run(() => onDone(a, { count: affected, days: d, by: tr('أحمد', 'Ahmad'), on: DESK.TODAY }), countText(affected, F_EXTENDED.ar, F_EXTENDED.en) + ' ' + countText(d, F_DAYS_ACC.ar, F_DAYS_ACC.en));
  };
  return (
    <AlertDialog open={!!a} onOpenChange={(o) => !o && onClose()}>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>{tr('تمديد اشتراكات المشتركين النشطين بأيام الإغلاق؟', 'Extend active subscribers’ subscriptions by the closure’s days?')}</AlertDialogTitle>
          <AlertDialogDescription>
            {tr('تتأخر نهاية ', 'The end of ')}<Counted n={affected} ar={F_SUBS_ACTIVE_ACC.ar} en={F_SUBS_ACTIVE_ACC.en} />{' '}
            {LANG === 'en' ? <>{'moves '}<Counted n={d} ar={F_DAYS_ACC.ar} en={F_DAYS_ACC.en} />{' later. '}</> : <><Counted n={d} ar={F_DAYS_ACC.ar} en={F_DAYS_ACC.en} />{'. '}</>}
            {tr('لا يمكن التراجع، ولا تطبيقه مرة ثانية لهذا الإغلاق.', 'It cannot be undone, nor applied again for this closure.')}
          </AlertDialogDescription>
        </AlertDialogHeader>
        {a && <Field label={tr('عدد الأيام', 'Number of days')} error={err} helper={<>{tr('أيام الإغلاق: ', 'The closure’s days: ')}<Num>{closureDays(a)}</Num></>}>
          <Input inputMode="numeric" dir="ltr" className="w-20" value={days} onChange={(e) => { setDays(e.target.value.replace(/[^\d]/g, '')); setErr(null); }} />
        </Field>}
        <AlertDialogFooter>
          <AlertDialogCancel>{tr('رجوع', 'Back')}</AlertDialogCancel>
          <AlertDialogAction variant="destructive" onClick={go}><Counted n={affected} ar={F_EXTEND_VERB.ar} en={F_EXTEND_VERB.en} /></AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}
```
  (The `AlertDialogAction` cannot show `loading` — CHANGES' *Notes for the web worker*; `?fail=extend`
  shows `useActionRun`'s failure toast with «إعادة المحاولة».)
- In `AnnInner`: `const [extending, setExtending] = React.useState(() => { const a = O.announcements.find((x) => x.id === pageParams.get('extend')); return a && extendable(a) ? a : null; });`
  and `<ExtendDialog a={extending} onClose={() => setExtending(null)} onDone={(a, ext) => setList((l) => l.map((x) => (x.id === a.id ? { ...x, extended: ext } : x)))} />`.
  Add `Field`, `Input` to the destructuring if missing (they are imported already; check).
- The sheet has no extension any more (commit 6 removed `ExtendCard`): **one primary** in the sheet.

### 3.8 O3 (amended) — the owner's overview is a work queue (commit 11)
**`owner.jsx`:** the state for no capacity (rule 4: no live state without capacity). *Quote*
`const publicState = (present, cap, closed) => (closed ? 'closed' : present >= cap ? 'full' : 'open');` →
`const publicState = (present, cap, closed) => (closed ? 'closed' : !cap ? 'none' : present >= cap ? 'full' : 'open');`;
in `STATE_WORD` add `none: ['neutral', tr('بلا حالة مباشرة', 'No live status')]`; in `STATE_SKIN` add
`none: 'border-border bg-secondary text-secondary-foreground'`. `PublicStateControl`'s choices stay
open · full · closed (an override works without capacity, rule 3).

**`Owner overview.html`** — rewrite the page script below the destructuring (keep the head, scripts and
`ReactDOM` line). Destructure `{ DirectionProvider, Button, Badge, Card, CardHeader, CardTitle,
CardDescription, CardAction, CardContent, StatCard, CircleCheckIcon }`. Delete `GROUPS`, `ago`,
`FreshnessCard`, `MoneyTile`, `MoneyRow`. Keep `Meter`. Add:
```js
const GROUP_NAME = () => ({ profile: tr('المساحة', 'The space'), hours: tr('ساعات العمل', 'Opening hours'), prices: tr('الأسعار', 'Prices'), amenities: tr('المرافق', 'Amenities'), contacts: tr('التواصل', 'Contacts') });
const groupHref = (g) => (g === 'prices' ? 'Packages.html#prices' : 'Owner space profile.html#' + g);
// O3 (amended 2026-10-12): what needs the owner, as counts and links — no amounts, since the overview
// is often open at the desk in view of customers and staff. Confirm lives beside what it confirms.
function queueRows() {
  if (O.demo('clear')) return [];
  const rows = [];
  ['profile', 'hours', 'prices', 'amenities', 'contacts'].forEach((g) => {
    const missing = O.missing.includes(g);
    const stale = !missing && O.groups[g] > (g === 'prices' ? O.LIMIT.prices : O.LIMIT.other);
    if (missing) rows.push({ key: g, title: GROUP_NAME()[g], badge: tr('لم تُضف بعد', 'Not added yet'), caption: tr('لم يُحفظ هذا القسم بعد، فلا يراه الزوار.', 'This section was never saved, so visitors don’t see it.'), action: tr('مراجعة', 'Review'), href: groupHref(g) });
    else if (stale) rows.push({ key: g, title: GROUP_NAME()[g], badge: tr('قديمة', 'Out of date'), caption: <>{tr('آخر تحديث ', 'Updated ')}<Counted n={O.groups[g]} ar={F_DAYS_AGO.ar} en={F_DAYS_AGO.en} /></>, action: tr('مراجعة', 'Review'), href: groupHref(g) });
  });
  const reports = O.reports.filter((r) => r.status === 'new').length;
  if (reports) rows.push({ key: 'reports', title: <Counted n={reports} ar={F_NEW_REPORTS.ar} en={F_NEW_REPORTS.en} />, caption: tr('من زوار، عن معلومات في صفحة المساحة', 'From visitors, about facts on the space page'), action: tr('مراجعة', 'Review'), href: 'Data reports.html?status=new' });
  const unpaid = DESK.unpaid.filter((u) => u.date === DESK.TODAY).length;
  if (unpaid) rows.push({ key: 'unpaid', title: <Counted n={unpaid} ar={F_UNPAID.ar} en={F_UNPAID.en} />, caption: tr('خرجت بلا دفع، أو سُجّل خروجها تلقائيًا', 'Left without paying, or checked out automatically'), action: tr('فتح المكتب', 'Open the desk'), href: 'Desk.html' });
  const owe = DESK.customers.filter((c) => DESK.balance(c) > 0).length;
  if (owe) rows.push({ key: 'owe', title: <Counted n={owe} ar={F_OWE.ar} en={F_OWE.en} />, caption: tr('المبالغ في المالية › الديون', 'The amounts are in Finance › Debts'), action: tr('عرض', 'View'), href: 'Finance.html?tab=debts' });
  O.announcements.filter((a) => a.type === 'closure' && annStatus(a) !== 'scheduled' && !a.extended).forEach((a) => rows.push({ key: a.id, title: tr('إغلاق لم تُمدَّد اشتراكاته', 'A closure whose subscriptions are not extended'), caption: annPeriod(a), action: tr('مراجعة', 'Review'), href: 'Announcements.html?tab=' + annStatus(a) + '&extend=' + a.id }));
  if (!O.capacity) rows.push({ key: 'capacity', title: tr('لم تُحدَّد السعة', 'Capacity is not set'), caption: tr('بدونها لا تظهر حالة مباشرة للزوار.', 'Without it visitors see no live status.'), action: tr('تحديد السعة', 'Set the capacity'), href: 'Owner settings.html#attendance' });
  return rows;
}
function QueueCard() {
  const rows = queueRows();
  return (
    <Card>
      <CardHeader><CardTitle><h2>{tr('يحتاج انتباهك', 'Needs your attention')}</h2></CardTitle></CardHeader>
      <CardContent className={rows.length ? 'p-0' : undefined}>
        {rows.length ? <ul className="divide-y">{rows.map((r) => (
          <li key={r.key} className="flex flex-col gap-2 px-5 py-3 md:flex-row md:items-center md:justify-between">
            <div className="flex min-w-0 flex-col gap-1">
              <span className="flex flex-wrap items-center gap-2"><span className="text-label">{r.title}</span>{r.badge && <Badge variant="warning">{r.badge}</Badge>}</span>
              <span className="text-caption text-muted-foreground">{r.caption}</span>
            </div>
            <div className="shrink-0"><Button variant="outline" size="sm" asChild><a href={r.href}>{r.action}</a></Button></div>
          </li>
        ))}</ul> : <p className="flex items-center gap-2 text-body-sm text-muted-foreground"><CircleCheckIcon className="size-4" aria-hidden="true" />{tr('كل شيء على ما يرام', 'All is in order')}</p>}
      </CardContent>
    </Card>
  );
}
// Every tile is a link, or none is (OW-003): the one tile left links.
function LinkTile(props) { return <a href={props.href} className="block rounded-xl text-foreground focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring"><StatCard className="h-full" label={props.label} value={props.value} helper={props.helper} /></a>; }
```
  (No object rest anywhere: `LinkTile` reads its props by name.) In `queueRows`, under `?demo=clear`
  the desk sample's unpaid, debtors and closures are ignored too — the `return []` at the top does it.
- **`OverviewScreen`** — no `actions` prop (no desk shortcut, no bottom bar); body:
```jsx
  const [theme, setTheme] = useTheme();
  const n = DESK.present.length;
  const subs = DESK.present.filter((p) => p.kind === 'sub').length;
  const state = publicState(n, O.capacity);
  const active = O.announcements.filter((a) => annStatus(a) === 'active');
  const ending = …; // unchanged
  return (
    <OwnerShell current="overview" title={tr('نظرة عامة', 'Overview')} state={state} theme={theme} setTheme={setTheme}>
      <QueueCard />
      <div className="grid gap-4 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardDescription>{tr('الحاضرون الآن', 'Present now')}</CardDescription>
            <CardTitle className="text-display"><Num>{O.capacity ? `${n} / ${O.capacity}` : n}</Num></CardTitle>
            <CardAction><Button variant="outline" size="sm" asChild><a href="Desk.html">{tr('عرض الحاضرين', 'View who’s here')}</a></Button></CardAction>
          </CardHeader>
          <CardContent className="flex flex-col gap-3">
            {O.capacity ? <Meter value={n} max={O.capacity} /> : null}
            <p className="text-body-sm text-muted-foreground">{tr('اليوم: ', 'Today: ')}<Num>{n + DESK.leftToday}</Num>{tr(' · الآن: ', ' · now: ')}<Counted n={subs} ar={F_SUBSCRIBERS.ar} en={F_SUBSCRIBERS.en} />{tr(' و', ' and ')}<Counted n={n - subs} ar={F_VISITS.ar} en={F_VISITS.en} /></p>
            <div className="flex flex-wrap items-center gap-2 text-body-sm text-muted-foreground">
              <PublicStateBadge state={state} />
              <span>{!O.capacity ? tr('حدّد السعة في الإعدادات لتظهر حالة مباشرة.', 'Set the capacity in Settings for a live status.') : state === 'full' ? tr('وصلت إلى السعة، فتظهر المساحة «ممتلئ».', 'At capacity, so the space shows «Full».') : tr('السعة لا تظهر للزوار، فقط الحالة.', 'Visitors never see capacity, only the state.')}</span>
            </div>
          </CardContent>
        </Card>
        <LinkTile href="Announcements.html" label={tr('إعلانات نشطة', 'Active announcements')} value={<Num>{active.length}</Num>} helper={active.map((a) => TYPE_WORD()[a.type]).join(tr('، ', ', '))} />
      </div>
      {/* the «اشتراكات تنتهي هذا الأسبوع» card, unchanged from commit 2, full width (drop its lg grid wrapper and the «بلاغات جديدة» StatCard) */}
    </OwnerShell>
  );
```
  with `const TYPE_WORD = () => ({ general: tr('عام', 'General'), outage: tr('انقطاع', 'Outage'), closure: tr('إغلاق مؤقت', 'Temporary closure'), offer: tr('عرض', 'Offer'), event: tr('فعالية', 'Event') });`.
  `?demo=nocapacity` shows the queue's capacity row, «27» alone, no meter, «بلا حالة مباشرة» on the badge
  and in the bar; `?demo=missing` adds «المرافق · لم تُضف بعد»; `?demo=clear` the empty line.
- **No money:** after this commit, `grep -n "Money\|₪\|money" "Owner overview.html"` prints nothing.

### 3.9 O4 + OW-017–019 — staff (commit 8)
**`Staff.html`.**
- **Sample** (*quote* `const INIT = [ … ];`) → replace:
```js
// OW-018: what the model holds — the link's date (SpaceManager.createdAt), whether access was removed
// (deactivatedAt) and the temporary password not changed yet (User.mustChangePassword).
const INIT = [
  { id: 'st1', name: tr('سامي', 'Sami'), key: DESK.SAMI, email: 'sami@example.com', status: 'active', added: '2026-03-02', pending: false, month: 1380 },
  { id: 'st3', name: tr('ليلى', 'Laila'), key: 'ليلى', email: 'laila@example.com', status: 'active', added: '2026-09-28', pending: true, month: 0 },
  { id: 'st2', name: tr('هالة', 'Hala'), key: 'هالة', email: 'hala@example.com', status: 'removed', added: '2026-05-10', pending: false, month: 0 }
];
```
- **Columns** (*quote* `const columns = [ … ];`) → five:
  - `name` «الاسم» / "Name": `<span className="flex min-w-0 flex-col"><span className="text-label">{name}</span><Ltr>{email}</Ltr></span>` (the email in `text-caption text-muted-foreground`: wrap `<span className="text-caption text-muted-foreground"><Ltr>…</Ltr></span>`);
  - `status` «الحالة» / "Status": `<StatusB s={…} />`;
  - `added` «أُضيف في» / "Added": `DESK.fmtDate(added, true)`;
  - `month` «مقبوضاته هذا الشهر» / "Collected this month": `<MonthLink s={…} />`;
  - `act`: unchanged.
  No `.lg-col`; at 768 the table shows all five (SH-007: ≤ 5 columns stay a table).
- `StatusB` → `<span className="flex flex-col items-start gap-1"><Badge variant={s.status === 'active' ? 'success' : 'neutral'}>{s.status === 'active' ? tr('نشط', 'Active') : tr('بلا وصول', 'No access')}</Badge>{s.status === 'active' && s.pending && <Badge variant="warning">{tr('لم يغيّر كلمة المرور المؤقتة بعد', 'Hasn’t changed the temporary password yet')}</Badge>}</span>`.
- The card (`renderCard`): name, the email (`Ltr`, caption), `«أُضيف في» {date}`, `StatusB`, «هذا الشهر» `MonthLink`; drop «الاستقبال · آخر دخول».
- **Menu** (*quote* the `DropdownMenuContent` items): keep «عرض مقبوضاته»; active → `<DropdownMenuItem onSelect={() => setConfirm(s)}>{tr('إيقاف الوصول', 'Remove access')}</DropdownMenuItem>`;
  removed → `<DropdownMenuItem onSelect={() => setStatus(s, 'active')}>{tr('إعادة الوصول', 'Give access back')}</DropdownMenuItem>`.
- `setStatus` (*quote*) → `const setStatus = (s, status) => setList((l) => l.map((x) => (x.id === s.id ? { ...x, status } : x)));` — no toast (P8: the row changes; O4).
- **Remove access** (OW-017, P9): *quote* the `AlertDialog` → title `{tr('إيقاف وصول ', 'Remove ')}{confirm && confirm.name}{tr('؟', '’s access?')}`;
  description `{confirm && tr(`تنتهي كل جلسات ${confirm.name} على كل الأجهزة الآن، ويتوقف الوصول إلى Focus Hub. يبقى الاسم على الدفعات وفي السجل، ويمكنك إعادة الوصول لاحقًا.`, `${confirm.name} is signed out on every device now and can no longer reach Focus Hub. The name stays on the payments and in the log, and you can give the access back later.`)}`;
  action `<AlertDialogAction variant="destructive" onClick={() => setStatus(confirm, 'removed')}>{tr('إيقاف الوصول', 'Remove access')}</AlertDialogAction>`, cancel «رجوع».
- **Add staff in one submit** (OW-019). The sheet: title «إضافة موظف» / "Add a staff member", description
  «الدور: الاستقبال» / "Role: reception"; body: `<RateLimitNote />`, `<ActionAlert for="add" />`, «الاسم»,
  «البريد الإلكتروني», then
  `<p className="text-body-sm text-muted-foreground">{tr('إن كان للبريد حساب في مساحة يُربط به ويدخل بكلمة مروره؛ وإلا يُنشأ حساب برمز مرور مؤقت يظهر لك مرة واحدة.', 'If the email has a Masaha account, it is linked and signs in with its own password; otherwise an account is created with a temporary password shown to you once.')}</p>`;
  footer `<Button type="submit" className="w-full" loading={busy}>{tr('إضافة إلى الاستقبال', 'Add to reception')}</Button>` with `const { busy, run } = useActionRun('add');`.
  Delete `link`, `setLink`, `doLink` and the info `Alert`. `submit`: the same checks (name, email format,
  `list.some((s) => s.email === e2 && s.status === 'active')` → «هذا الموظف مضاف مسبقًا» / "This staff member is already added"),
  then `run(() => { … })` deciding:
  - a removed row with that email → it becomes `active`; close the sheet; toast `tr(`عاد وصول ${row.name} إلى Focus Hub`, `${row.name} has access to Focus Hub again`)`;
  - `EXISTING.includes(e2)` → add `{ id: 's' + Date.now(), name, key: name, email: e2, status: 'active', added: DESK.TODAY, pending: false, month: 0 }`; close; toast `tr(`رُبط حساب ${e2} بـ Focus Hub`, `${e2}’s account is linked to Focus Hub`)`;
  - otherwise → add with `pending: true`; close; open the password dialog with `{ name, email: e2, pw: tempPass() }`.
  `?email=nour@example.com` keeps prefilling Nour (submitting links her).
- **The password dialog, A5's rules** — replace the `Dialog` with `<StaffPassDialog info={pass} onClose={() => setPass(null)} />`, defined page-level:
  a copy of `admin.jsx`'s `TempPassDialog` (*quote* `function TempPassDialog({ info, onClose, line }) {` …
  `}` at `admin.jsx:96-129`) renamed `StaffPassDialog({ info, onClose })`, with its `line` replaced by the two
  existing lines `«سلّمها للموظف؛ سيُطلب منه تغييرها عند أول دخول.»` / "Hand it to the staff member;
  they’ll be asked to change it at first sign-in." and `«لن تظهر مرة أخرى بعد إغلاق هذه النافذة.»` / "It
  won’t be shown again after you close this window." Keep everything else identical: no `closeLabel`
  (no X), `onEscapeKeyDown`/`onInteractOutside` prevented, «نسخ» → «نُسخت», «تم» disabled until copied
  with «انسخها أولًا — لن تظهر مرة أخرى», «طريقة التسليم» (واتساب · شفهيًا · أخرى) checked on «تم» with
  «اختر طريقة التسليم», toast «سُجّلت طريقة التسليم». Add `RadioGroup`, `RadioGroupItem` to the page's
  destructuring. (Copying is the boundary's price: `admin.jsx` is not this batch's; DI-37.)
- `?pass=1` (Laila), `?stop=1` (Sami), `?sheet=add`, `?state=empty|loading` keep working; new `?fail=add`.
- **Frames that change** (`INDEX.md` §37 and the board): «Email already has an account → «ربط» — desktop
  1440 / phone 390» → «Email with an account → linked on submit — …» (same URL); «Suspend (confirm) — …» →
  «Remove access (confirm) — …» (same URL `Staff.html?stop=1`).

### 3.10 O12 + A8 — data reports (commit 9)
**`owner-data.js`** — the sample, without the reporter (the owner never receives the name):
```js
  // O12: the reporter is anonymous to the owner — no name is sent; the admin keeps it.
  const reports = [
    { id: 'd1', field: 'hours', date: '2026-09-29', status: 'new', msg: T('صارت المساحة تفتح 09:00 بدل 08:00 منذ بداية الأسبوع.', 'The space opens at 09:00 instead of 08:00 since the start of the week.') },
    { id: 'd2', field: 'prices', date: '2026-09-27', status: 'new', msg: T('سعر الأسبوع عند الاستقبال 100 ₪ وليس 90 ₪.', 'The weekly price at the desk is ₪100, not ₪90.') },
    { id: 'd3', field: 'amenities', date: '2026-09-20', status: 'fixed', msg: T('أضافوا قاعة اجتماعات جديدة في الطابق نفسه.', 'They added a new meeting room on the same floor.'), reply: T('شكرًا، أضفنا القاعة إلى المرافق.', 'Thanks, we added the room to the amenities.') },
    { id: 'd4', field: 'contacts', date: '2026-09-12', status: 'rejected', msg: T('رقم الواتساب لا يرد.', 'The WhatsApp number doesn’t answer.'), reply: T('الرقم صحيح، نرد خلال ساعات العمل.', 'The number is correct; we reply during opening hours.') }
  ];
```
  (`?demo=clear` → `reports` all non-new: write `const reports = demo('clear') ? [] : [ … ];`.) Return it.
  `owner.jsx`'s nav badge as §3.8 says.
**`owner.jsx`** — `OwnerReportNotice` (the admin's `ReportNotice`, for the owner, with no name):
```jsx
// O12 + A8: `?report=<id>` from «تعديل الحقل»: the open report sits above its section, where the field
// is corrected, and «تم التصحيح» resolves it there. The owner sees the date, never who reported it.
const REPORT_FIELD = () => ({ hours: tr('ساعات العمل', 'Opening hours'), prices: tr('الأسعار', 'Prices'), contacts: tr('التواصل', 'Contacts'), location: tr('الموقع', 'Location'), amenities: tr('المرافق', 'Amenities'), other: tr('أخرى', 'Other') });
const reportSection = (r) => ({ location: 'profile', other: 'profile' }[r.field] || r.field);
function OwnerReportNotice({ at }) {
  const { Alert, AlertTitle, AlertDescription, Button: B } = window.MasahaDesignSystem;
  const r = O.reports.find((x) => x.id === pageParams.get('report') && x.status === 'new');
  const [done, setDone] = React.useState(false);
  const { busy, run } = useActionRun('fix');
  if (!r || reportSection(r) !== at) return null;
  if (done) return <Alert id="report" variant="info" className="section-anchor"><AlertTitle>{tr('عُلّم «تم التصحيح»', 'Marked «Corrected»')}</AlertTitle><AlertDescription><a href="Data reports.html?status=new">{tr('العودة إلى البلاغات', 'Back to the reports')}</a></AlertDescription></Alert>;
  return (
    <Alert id="report" variant="info" className="section-anchor">
      <AlertTitle>{tr('بلاغ مفتوح على ', 'An open report on ')}{REPORT_FIELD()[r.field]}</AlertTitle>
      <AlertDescription>
        <p>{tr('«', '“')}{r.msg}{tr('»', '”')}{tr(' — زائر، ', ' — a visitor, ')}{O.fmtDate(r.date)}</p>
        <p className="flex flex-wrap items-center gap-x-4 gap-y-2 pt-2">
          <B size="sm" loading={busy} onClick={() => run(() => setDone(true), tr('عُلّم «تم التصحيح»', 'Marked «Corrected»'))}>{tr('تم التصحيح', 'Corrected')}</B>
          <a href={'Data reports.html?open=' + r.id}>{tr('فتح البلاغ للرد', 'Open the report to reply')}</a>
        </p>
      </AlertDescription>
    </Alert>
  );
}
```
  The date uses `O.fmtDate` (owner-data's own, already exported), since the profile page does not load
  `desk-data.js`. Export `OwnerReportNotice`, `REPORT_FIELD`, `reportSection`. (`B` is a local alias
  inside the function, not top-level.)
- **`owner.jsx`, the nav badge** (this commit): `OWNER_NAV`'s data-reports `badge: 2` →
  `badge: O.reports.filter((r) => r.status === 'new').length || undefined`.
- **`Owner space profile.html`**: insert `<OwnerReportNotice at="profile" />` before `<SpaceSection …/>`,
  `<OwnerReportNotice at="hours" />` before `<HoursSection …/>`, `at="amenities"` before the amenities,
  `at="contacts"` before the contacts. **`Packages.html`**: `<OwnerReportNotice at="prices" />` before
  `<PricesSection …/>`. The hash `#report` lands through `useHashLanding`.
**`Data reports.html`:**
- Delete `INIT`; `list` starts from `O.reports.map((r) => ({ ...r }))` (or `[]` under `?state=empty`);
  `open` from `O.reports`.
- `FIELDS()`'s second values become the «تعديل الحقل» targets: `prices: 'Packages.html?report=ID#report'`,
  the others `'Owner space profile.html?report=ID#report'` — build them in the sheet as
  `(r.field === 'prices' ? 'Packages.html' : 'Owner space profile.html') + '?report=' + r.id + '#report'`.
- **Columns:** delete `who`; `date` loses `meta: { className: 'hidden lg-col' }` (five columns, a table at 768).
- Sheet description `{r.who} · …` → `{tr('زائر', 'A visitor')} · {DESK.fmtDate(r.date, true)} · <Badge …>`;
  the card's line `{r.who} · {DESK.fmtDate(r.date)}` → `{tr('زائر', 'A visitor')} · {DESK.fmtDate(r.date)}`.
- **A8's reply** (as `Admin reports.html:41-42, 93`): `const [replyErr, setReplyErr] = React.useState(null);`
  (reset on open); the reply `Field`: label «ردّ إدارة المساحة» / "Reply from the space", **no** «اختياري»,
  `helper={tr('يظهر لصاحب البلاغ. مطلوب لـ«لم يُعتمد»، واختياري لـ«تم التصحيح».', 'Shown to the person who reported it. Required to mark «Not accepted», optional for «Corrected».')}`,
  `error={replyErr}`; «لم يُعتمد» with an empty reply → `setReplyErr(tr('اكتب السبب؛ هو ما سيقرؤه صاحب البلاغ', 'Write the reason; it’s what the reporter will read'))`
  and focus `document.querySelector('[role=dialog] textarea')`, nothing decided.
- `?open=d1`, `?status=new`, `?state=empty|loading` keep working.

### 3.11 OW-015 + OW-016 — finance (commit 10)
**`Finance.html`** (only; `finance.jsx` is untouched — `RangePicker` is the audit pages' too):
- Add:
```js
// OW-015: one month for the blocks that count by month; the charts keep their fixed windows, named.
const MONTH_OPTS = DESK.MONTHS.slice().reverse();
const monthLabel = (ym) => new Date(ym + '-15T12:00:00').toLocaleDateString(tr('ar-EG', 'en-GB'), { month: 'long', year: 'numeric', numberingSystem: 'latn' });
const monthTotal = (ym) => { const [v, s] = DESK.monthly[DESK.MONTHS.indexOf(ym)]; return v + s; };
const ratioOf = (ym) => monthTotal(ym) / monthTotal(DESK.MONTHS[DESK.MONTHS.length - 1]);
// The sample holds this month's collections; an earlier month's are this month's, scaled to its income.
const staffFor = (ym) => DESK.staffMonth.map(([who, n, total, cash, tf]) => { if (ym === DESK.MONTHS[DESK.MONTHS.length - 1]) return [who, n, total, cash, tf]; const k = ratioOf(ym); const t = Math.round((total * k) / 5) * 5; const c = Math.round((cash * k) / 5) * 5; return [who, Math.round(n * k), t, Math.min(c, t), t - Math.min(c, t)]; });
```
- `FinanceInner`: delete `range`; `const [month, setMonth] = React.useState(MONTH_OPTS.includes(pageParams.get('month')) ? pageParams.get('month') : MONTH_OPTS[0]);`.
  *Quote* `<FilterSheet active={1} …>…</FilterSheet>` → 
  `<Field label={tr('الشهر', 'Month')}><Select value={month} onValueChange={setMonth}><SelectTrigger className="md:w-48"><SelectValue /></SelectTrigger><SelectContent>{MONTH_OPTS.map((m) => <SelectItem key={m} value={m}>{monthLabel(m)}</SelectItem>)}</SelectContent></Select></Field>`
  (inline at every width). Add `Field, Select, SelectTrigger, SelectValue, SelectContent, SelectItem` to the destructuring.
  Pass `month` to the three tabs.
- **CSV** (P1: it stays in the bar, in «⋯» on a phone): the action's label by tab —
  income «تصدير الدخل (CSV)» / "Export income (CSV)", debts «تصدير الديون (CSV)» / "Export debts (CSV)",
  occupancy «تصدير الإشغال (CSV)» / "Export occupancy (CSV)". The files are unchanged.
- **`IncomeTab({ month })`:** `i = DESK.MONTHS.indexOf(month)`; the second tile: `label={monthLabel(month)}`,
  `value={<Money n={monthTotal(month)} />}`, helper only when `i > 0`:
  `<>{pct >= 0 ? '+' : ''}<Num>{pct + '%'}</Num>{tr(' عن ', ' vs ')}{monthLabel(DESK.MONTHS[i - 1])}</>` with
  `pct = Math.round(((monthTotal(month) - monthTotal(DESK.MONTHS[i - 1])) / monthTotal(DESK.MONTHS[i - 1])) * 100)`.
  «اليوم» and «منذ البداية» are unchanged. The collections card: `CardDescription` = `monthLabel(month)`,
  rows from `staffFor(month)`. The two charts keep their descriptions («آخر 12 شهرًا», «آخر 30 يومًا ·
  الجمعة مغلق»).
- **`DebtsTab({ month })`:** «مجموع الديون» and «لهم رصيد» are today's (unchanged). `paidThisMonth` filters
  `r.date.startsWith(month)`; its tile label «دفعوا في {monthLabel(month)}» → `tr('دفعوا في ', 'Paid in ') + monthLabel(month)`;
  the card «دفعوا هذا الشهر» → the same title, its list `slice(0, 5)`, and, when more than five,
  `<CardAction><Button variant="link" size="sm" asChild><a href="Payments.html">{tr('عرض الكل', 'View all')}</a></Button></CardAction>`
  (unfiltered: `Payments.html` reads no month; DI-36). Delete the «و … آخرين» line.
  **«عليهم مبالغ» pages** (P6): `const paged = usePaged(debtors);` render `paged.rows`, and under the
  `<ul>`, inside `CardContent`, `<div className="flex flex-wrap items-center justify-between gap-3 border-t px-5 py-3"><ResultCount>{paged.summary}</ResultCount>{paged.nav}</div>`;
  the description stays «الأكبر أولًا».
- **`OccupancyTab({ month })`:** the three tiles' helpers name the month: «متوسط مدة الجلوس» helper
  `tr('المشتركون 5:05 · الزيارات 2:40 · ', 'Members 5:05 · visits 2:40 · ') + monthLabel(month)`;
  «ساعة الذروة» helper `tr('الأحد والاثنين الأعلى · ', 'Sunday and Monday are busiest · ') + monthLabel(month)`;
  «متوسط الحضور اليومي» value `<Num>{Math.round(26 * ratioOf(month))}</Num>`, helper `monthLabel(month)`.
  The heatmap's description names its window: «متوسط الحاضرين لكل ساعة · آخر 4 أسابيع · الجمعة مغلق» /
  "Average people present per hour · last 4 weeks · closed on Fridays"; the per-day chart keeps «آخر 14 يومًا».
- New: `?month=2026-08`.

### 3.12 O13 — the owner's audit log (commit 12)
**`owner-data.js`** — the space's log (`[date, time, actor, action, target, details]`; `actor` null = the system):
```js
  // O13: the space's own log — saves and confirms, packages, announcements, the extension, payments,
  // staff and settings. An automatic check-out has no actor: the system did it.
  const AH = T('أحمد', 'Ahmad'), SA = T('سامي', 'Sami');
  const audit = [
    ['2026-09-29', '12:10', SA, 'payment_recorded', T('يوسف أبو شعبان', 'Yousef Abu Shaaban'), T('50 ₪ · تحويل', '₪50 · transfer')],
    ['2026-09-29', '09:15', SA, 'payment_recorded', T('نور الهدى سالم', 'Nour Al-Huda Salem'), T('30 ₪ · نقدًا', '₪30 · cash')],
    ['2026-09-28', '18:00', null, 'auto_checkout', T('مالك صيام', 'Malek Siam'), T('خروج تلقائي عند الإغلاق · زيارة غير محصّلة', 'Checked out at closing · visit not collected')],
    ['2026-09-28', '16:40', AH, 'staff_added', T('ليلى', 'Laila'), T('حساب جديد · كلمة مرور مؤقتة سُلّمت شفهيًا', 'New account · temporary password handed over in person')],
    ['2026-09-27', '11:20', AH, 'announcement_published', T('فعالية · ورشة تعريفية', 'Event · intro workshop'), T('من 27 سبتمبر', 'From 27 September')],
    ['2026-09-26', '13:05', AH, 'group_saved', T('ساعات العمل', 'Opening hours'), T('الجمعة: مغلقة', 'Friday: closed')],
    ['2026-09-25', '10:30', AH, 'payment_voided', T('رهف قديح', 'Rahaf Qudaih'), T('50 ₪ · سُجّلت مرتين بالخطأ', '₪50 · recorded twice by mistake')],
    ['2026-09-24', '08:05', AH, 'announcement_published', T('إغلاق مؤقت · انقطاع الكهرباء', 'Temporary closure · power cut'), T('24–25 سبتمبر', '24–25 September')],
    ['2026-09-22', '12:00', SA, 'announcement_ended', T('انقطاع · الإنترنت بطيء', 'Outage · slow internet'), T('أُنهي الآن', 'Ended now')],
    ['2026-09-20', '09:30', AH, 'package_paused', T('صباحي للطلاب', 'Student mornings'), T('لم تعد متاحة في المكتب', 'No longer offered at the desk')],
    ['2026-09-17', '10:00', AH, 'subscriptions_extended', T('إغلاق 14–16 سبتمبر', 'Closure 14–16 September'), T('19 اشتراكًا · 3 أيام', '19 subscriptions · 3 days')],
    ['2026-09-15', '17:45', AH, 'staff_deactivated', T('هالة', 'Hala'), T('انتهت جلساتها', 'Sessions ended')],
    ['2026-09-12', '15:10', AH, 'report_dismissed', T('بلاغ عن التواصل', 'Report on the contacts'), T('لم يُعتمد · بردّ', 'Not accepted · with a reply')],
    ['2026-09-10', '11:00', AH, 'group_confirmed', T('الأسعار', 'Prices'), T('ما زالت صحيحة', 'Still correct')],
    ['2026-09-05', '14:20', AH, 'settings_changed', T('تسعير الزيارات', 'Visit pricing'), T('التقريب: لأعلى بعد 15 دقيقة', 'Rounding: up after 15 minutes')],
    ['2026-09-01', '09:00', AH, 'photo_removed', T('صورة 6', 'Photo 6'), '']
  ];
  // P6: enough lines to page — one desk day after another, deterministic.
  const FILL = [[SA, 'payment_recorded', T('زيارة', 'Visit'), T('15 ₪ · نقدًا', '₪15 · cash')], [AH, 'payment_recorded', T('اشتراك شهري', 'Monthly subscription'), T('300 ₪ · تحويل', '₪300 · transfer')], [null, 'auto_checkout', T('زيارة', 'Visit'), T('خروج تلقائي عند الإغلاق', 'Checked out at closing')], [SA, 'customer_created', T('زبون جديد', 'A new customer'), '']];
  for (let i = 0; audit.length < 64; i++) { const d = new Date('2026-09-29T12:00:00'); d.setDate(d.getDate() - 2 - Math.floor(i / 3)); const [a, act, t, x] = FILL[i % FILL.length]; audit.push([d.toISOString().slice(0, 10), String(9 + (i % 8)).padStart(2, '0') + ':' + String((i * 17) % 60).padStart(2, '0'), a, act, t, x]); }
```
  Return `audit`. (Array destructuring `const [a, act, t, x] = …` is allowed; no object rest.)
**`owner.jsx`:** in `OWNER_NAV`'s «الفريق والإعدادات» group, between `staff` and `settings`:
`{ id: 'audit', label: tr('سجل التدقيق', 'Audit log'), href: 'Owner audit.html', icon: <OSearch /> }`
(the icon is a placeholder, as every nav icon is — README's known limits).
**New page `Owner audit.html`** — copy `Packages.html` lines 1–24 (the `<head>`, with
`<title>سجل التدقيق — مساحة</title>` in place of its title, then `<body …>`, `<div id="ds-root"></div>`,
`shared.jsx`, `owner.jsx`), then exactly `<script src="masaha/desk-data.js"></script>` and
`<script type="text/babel" src="masaha/finance.jsx"></script>`, then the inline
`<script type="text/babel">…</script>`, `</body>`, `</html>`. No `desk-core.jsx`, no profile modules
(the page renders no `DeskProvider`). The page script is
`Admin audit.html`'s (lines 28–93) with these differences, and nothing else:
- `AD.audit` → `O.audit`; `AD.TODAY` → `DESK.TODAY`; `AD.fmt(x)` → `DESK.fmtDate(x, true)`;
  `AdminShell current="audit"` → `OwnerShell current="audit" state={publicState(DESK.present.length, O.capacity)}`.
- `actor` shows `r.actor || tr('النظام', 'The system')` (the cell, the card, and the actor filter's options;
  filter with a key `r.actor || 'system'`).
- The actions and their words:
```js
const ACTION = () => ({ payment_recorded: tr('تسجيل دفعة', 'Payment recorded'), payment_voided: tr('إلغاء دفعة', 'Payment voided'), auto_checkout: tr('خروج تلقائي', 'Automatic check-out'), customer_created: tr('زبون جديد', 'New customer'), staff_added: tr('إضافة موظف', 'Staff added'), staff_deactivated: tr('إيقاف وصول', 'Access removed'), announcement_published: tr('نشر إعلان', 'Announcement published'), announcement_ended: tr('إنهاء إعلان', 'Announcement ended'), subscriptions_extended: tr('تمديد الاشتراكات', 'Subscriptions extended'), package_paused: tr('إيقاف باقة', 'Package paused'), group_saved: tr('حفظ قسم', 'Section saved'), group_confirmed: tr('تأكيد قسم', 'Section confirmed'), report_dismissed: tr('بلاغ لم يُعتمد', 'Report not accepted'), settings_changed: tr('تغيير الإعدادات', 'Settings changed'), photo_removed: tr('حذف صورة', 'Photo deleted') });
// AD-028 as amended: red follows P9 — only the acts whose confirmation is destructive.
const RED = ['payment_voided', 'staff_deactivated', 'subscriptions_extended', 'photo_removed'];
```
- `targetHref(r)`: `payment_*` → `'Payments.html'`; `auto_checkout`, `customer_created` → `'Customers.html'`;
  `staff_*` → `'Staff.html'`; `announcement_*` → `'Announcements.html?tab=ended'` for `announcement_ended`, else `'Announcements.html'`;
  `subscriptions_extended` → `'Announcements.html?tab=ended'`; `package_paused` → `'Packages.html'`;
  `group_saved`/`group_confirmed` → `r.target === tr('الأسعار', 'Prices') ? 'Packages.html#prices' : 'Owner space profile.html'`;
  `report_dismissed` → `'Data reports.html?status=rejected'`; `settings_changed` → `'Owner settings.html'`;
  `photo_removed` → `'Owner space profile.html#photos'`.
- The intro line: «كل ما جرى في Focus Hub: مَن فعل ماذا، ومتى.» / "Everything done at Focus Hub: who did
  what, and when."
- The period `Select` (آخر 30 يومًا default · كل الفترة · فترة محدّدة with `RangePicker`), «بحث في
  الهدف», «المنفّذ» (shown: three actors), «نوع الإجراء», the A7 details-under-target until 1024, paging,
  `?state=loading` — all as the admin's.
- `person`, `DAY`, `since` as the admin's (`DAY` and `person` are page-level names on a page without
  `admin.jsx`; checked free on this page's modules).
**`SCREENS.md`** — under *Also in the archive* add:
`- \`Owner audit.html\`: the owner's audit log (O13), the admin's audit page scoped to the space. It is not
yet one of foundation §13's screens ([finding 14](../architecture/findings/14-the-owners-audit-screen-has-no-design.md)); board section 55.`
**`README.md`** — *What is here*: «40 pages» → «41 pages».

### 3.13 The board and the index (commit 13)
See §6, commit 13, for the exact rows and frames.

---

## 4. Stronger decisions and design issues (the owner answers before the build)

### Stronger decisions (proposed; built as recommended unless the reply says otherwise)
| | What | Why | Cost | Recommend |
|---|---|---|---|---|
| **S1** | `PricesSection` takes three **default-preserving** props (`title`, `description`, `hoursHref`); the admin's editor passes none | The boundary allows a page-level prop; without it Packages keeps OW-008's doubled heading and a dead `#hours` link | none | **yes** |
| **S2** | **`CapacitySection` is deleted** from `profile-b.jsx` | After O2 nothing renders it; left in, worker A may read it as part of the editor. The admin's editor never showed it | none | **yes** |
| **S3** | The announcements, reports and audit samples **move to `owner-data.js`** | The overview's queue must count the same reports and closures the pages list (the 2b lesson: the queue counts what the list counts) | small | **yes** |
| **S4** | A sample **ended closure without its extension** (a6, 24–25 Sep) | Shows OW-013's action and the queue's row with no demo flag and without making the space «مغلق الآن» on every page | none | **yes** |
| **S5** | Staff's verb is **«إيقاف الوصول» / «إعادة الوصول»**, the dialog's body gender-neutral | OW-017's «إيقاف وصوله» is masculine; the sample's pending staff member is Laila. The meaning is the decided one | none | **yes** |
| **S6** | The queue's debt row says **«زبائن عليهم مبالغ»**, not «عملاء عليهم ديون» | «زبون» is the glossary's word and Finance's own «عليهم مبالغ» | none | **yes** |
| **S7** | The overview **drops the top bar's «مكتب الاستقبال»** | OW-003/P1 amended: "Overview: none; the desk is in the navigation" | none | **yes** |
| **S8** | A **«بلا حالة مباشرة» state** in the shell's control (`?demo=nocapacity`) | Rule 4: without capacity there is no live state; the queue's capacity row needs a true frame | small | **yes** |
| **S9** | The stay limit in **whole hours, 1–23** (stored as minutes) | `maxStayMinutes` is minutes; owners think in hours; > 23 h is never shorter than closing | none | **yes** |
| **S10** | **Finance's month drives only month-based blocks; each names its month**; earlier months' collections are this month's scaled (sample) | OW-015 lists the blocks; naming the month on each says which blocks it moved | small | **yes** |
| **S11** | The extension's **«عدد الأيام» is checked on the action** (the button stays enabled) | Foundation §10 (submits stay enabled) | none | **yes** |
| **S12** | The owner's audit names **«النظام»** for automatic check-outs | `actorId` null is the system; the actor filter then has three actors and shows (AD-028) | none | **yes** |
| **S13** | The password dialog is **copied** into `Staff.html` as `StaffPassDialog` | `admin.jsx` is not this batch's file; the two must be one component in code (DI-37) | small | **yes** |
| **S14** | `?demo=` is **a comma list** on the owner's pages (`missing`, `nocapacity`, `clear`, `noshifts`) | One parameter, combinable for one frame (`?demo=missing,nocapacity`) | none | **yes** |

### Design issues (recorded; none is built unless the reply says so)
| | Issue | Better | Level | Recommend |
|---|---|---|---|---|
| **DI-30** | O6's words in the **shared** price table: the period is «المدة» and the audience «الفئة: عام · طلاب»; O6 decides «الفترة» and «لمن: الجميع · الطلاب». The table is the admin's editor's too, which worker A is building (S2b-4) | Change both editors at once: `profile-b.jsx` `col.period` «الفترة» / "Period", `col.audience` «لمن» / "For", `AUDIENCE()` «الجميع» / "Everyone", «الطلاب» / "Students" | prototype + worker A | **Route to worker A's S2b-4 now (the analyst tells them); the prototype's shared table follows in a small item after S2b-4 merges.** If you prefer it built here: one commit «docs(design): the price table's words» changing the four strings, both editors looked at |
| **DI-31** | O4's save toast names the group («حُفظت ساعات العمل»); the shared `useSection` says «حُفظ القسم» on both editors | `useSection(id, …)` takes the group's name and says «حُفظت ساعات العمل» / "Opening hours saved" | prototype + worker A | Same routing as DI-30 |
| **DI-32** | The shared gallery caps photos at **10** and refuses **WebP**; `security.md` allows JPEG/PNG/WebP at 5 MB and **no document sets a count** | Either the contract sets a cap (10) or the gallery drops it; WebP accepted in both | docs/API + prototype | **The analyst asks worker B** whether 10 is the cap; the prototype follows the answer later |
| **DI-33** | OW-007's empty gallery is an `EmptyState` «لا توجد صور بعد · الصورة الأولى تصبح الغلاف»; the shared gallery shows a line «لا صور بعد.» | `EmptyState` in `PhotosSection` | prototype + worker A | Same routing as DI-30 |
| **DI-34** | The **admin's** phone bar has the same crowding DI-10 resolved for the owner | The same move in `AdminShell` | prototype (`admin.jsx`) | Record for the next admin item |
| **DI-35** | The desk's uncollected card has no anchor: the queue's «زيارة واحدة لم تُحصَّل اليوم» lands on the desk's top | `id="unpaid"` on that card; the link becomes `Desk.html#unpaid` | desk batch (6) | Record for batch 6 |
| **DI-36** | `Payments.html` reads no month, so Finance's «عرض الكل» lands unfiltered | `?month=YYYY-MM` on Payments; Finance's link carries it | desk batch (6) | Record for batch 6 |
| **DI-37** | The staff password dialog is a copy of `TempPassDialog` | One component (code: the layer or a shared feature part) | web | Record for the web worker |
| **DI-38** | Owner settings: the three cards share one `?fail=save`, so one failure shows in all three (2b fixed this for the admin) | One action key per card (`save-attendance`, `save-pricing`, `save-message`) | prototype | **Fold** — small, the page is this batch's: `SettingsCard` takes an `actionKey` prop that its `ActionButton actionKey` and `ActionAlert for` both use; the three cards pass `save-attendance`, `save-pricing`, `save-message`; `INDEX.md` parameters row names them (commit 4) |
| **DI-39** | The vendored `Sheet side="end"` is ¾ wide at 390 (OW-010, worker A's); the prototype's forms stay in it until the bundle re-syncs | — | design system | Record only; this batch keeps the sheets' fields single-column at 390 so nothing overflows |
| **DI-40** | foundation §13's screen 12 still lists the overview's money, and no screen holds the owner's audit log | The rule change O3 names, and a screen row for the audit (finding 14) | docs / worker A | Record; `SCREENS.md` lists the page under *Also in the archive* |

**Under each answer:** "approve S1–S14 and the routing" → build as written. "Build DI-30/31/33 here" → add
one commit after commit 3, `docs(design): the shared editor's words` (38), changing only the named strings
and `PhotosSection`'s empty branch, and re-shoot `Admin space edit.html?id=golden` (the boundary's
exception, stated in the PR). "Drop S7" → keep the overview's `actions` prop as on `main`. "Drop S5" →
use «إيقاف وصوله» / «إعادة وصوله» and the masculine body for every name. DI-38 not folded → leave the
three keys as they are.

---

## 5. The files, their owners and the boundaries

| File | Owner this round | This batch's change |
|---|---|---|
| `prototype/Owner overview.html`, `Owner space profile.html`, `Packages.html`, `Announcements.html`, `Staff.html`, `Finance.html`, `Owner settings.html`, `Data reports.html` | this batch | §3 |
| `prototype/Owner audit.html` | this batch (new) | §3.12 |
| `prototype/masaha/owner.jsx`, `owner-data.js` | this batch | §3.0, 3.1, 3.6, 3.8, 3.10, 3.12 |
| `prototype/masaha/profile-b.jsx` | shared editor; **worker A builds from it** | only S1's three default props and S2's deletion; nothing the admin's editor shows |
| `prototype/masaha/profile-a.jsx` | shared editor | **no change** |
| `prototype/Flows - states.html` | shared by both design batches | one new section at the end (its own coordinates) and eight relabelled owner frames |
| `CHANGES.md` | shared | a new `## Batch 5 …` section, appended after *Batch 2b* (the file's last section) |
| `INDEX.md` | shared | a `### Batch 5 — the owner's management` parameters table after *Batch 3*'s; `## 55 · Batch 5 …` at the end; eight relabelled rows |
| `README.md` | shared | the page count (41) and frame count (§6, commit 13); one known-limit bullet (§3.6) |
| `SCREENS.md` | shared | the board section 55 on rows 12, 18–24; the audit page line |
| **Never edited** | | `Admin space edit.html` (Issue #72), `shared.jsx`, `auth.jsx`, `account.jsx` and the auth/account pages (the account batch), `Desk.html`, `Customers.html`, `Customer file.html`, `Payments.html`, `My payments.html`, `desk-core.jsx`, `desk-sheet.jsx`, `desk-data.js` (batch 6), `finance.jsx`, `admin.jsx`, `admin-data.js`, `_ds/`, `_vendor/`, `screens/`, everything outside `docs/design/` |

**Numbering with the account batch:** it is batch 4 and appends its own `CHANGES.md` section, `INDEX.md`
section and board section. This batch numbers its index section **55** and its board section starts at
**top 150000**, leaving 54 and the space after 145730 to batch 4, so neither overlaps whatever order they
merge in. Whichever PR merges second rebases and keeps both sides (the fast path); then `README.md`'s counts
add both batches' frames and sections.

---

## 6. The commits, in order

All `docs(design): …`; counted (≤ 50). Each commit's `CHANGES.md` line goes in it; the first creates the
section heading and intro. Stage by path only.

**The section heading (commit 1 adds it, after the last line of *Batch 2b*'s table):**
```
## Batch 5 — the owner's management (2026-10-13)

Reviewed as OW-001…OW-022; decided in `DECISIONS_OWNER.md` with the owner's amendments of 2026-10-12
(no money on the overview) and 2026-10-13 (the phone's top bar, a package's price above zero, and the
editor boundary: nothing the admin's editor shows changes while worker A builds it). The design-system
item (OW-010) and the rule changes are the web's and the docs'.

| Decision | What changed | Where |
|---|---|---|
```

| # | Subject (chars) | Files | `CHANGES.md` line |
|---|---|---|---|
| 1 | `docs(design): the owner's bar on a phone` (40) | `masaha/owner.jsx`, `CHANGES.md` | `\| **DI-10** \| On a phone the owner's and reception's top bar holds four things — the menu, the page's title (truncated if it must), P1's «⋯» and P2's state control — and the account leaves it: it heads the drawer, a row with the avatar, the name and role and the email that opens the one account menu, without the theme and language items the drawer's foot already holds. From 768 the bar is unchanged. \`?drawer=open\` opens the drawer for the board. The desk's pages share the shell, so they change with it \| \`masaha/owner.jsx\` \|` |
| 2 | `docs(design): counted words in Arabic` (37) | `owner.jsx`, `Owner overview.html`, `Announcements.html`, `Finance.html`, `Owner space profile.html`, `CHANGES.md` | `\| **O5** \| Every counted noun goes through Arabic's plural forms, one helper for the owner's pages (\`Intl.PluralRules('ar')\`, the number isolated): «ينتهي غدًا», «ينتهي بعد يومين», «بعد 3 أيام», «بعد 11 يومًا», «زيارة واحدة», «زبونان»; no more «بعد 1 أيام» or «1 زيارات». The announcements' tab counts are \`Badge\`s, not a number between parentheses \| \`masaha/owner.jsx\` (\`countText\`, \`Counted\`), \`Owner overview.html\`, \`Announcements.html\`, \`Finance.html\`, \`Owner space profile.html\` \|` |
| 3 | `docs(design): one editor; prices on their page` (46) | `owner.jsx`, `owner-data.js`, `profile-b.jsx`, `Owner space profile.html`, `Packages.html`, `Data reports.html`, `CHANGES.md` | `\| **O1, O6** \| The owner's Space profile is the A1 editor with the owner's differences only: each group dated from the sample, A2's «ما زال ناقصًا» when one was never saved (\`?demo=missing\`), and **prices as one row** — its date, «قديمة» when it is, and «الباقات والأسعار» — since the price table lives on **Packages & prices**, where it is saved and confirmed. There it is the AD-008 table titled «الأسعار المعلنة», dated «قبل 34 يومًا», «قديمة», with «حفظ» and «المعلومات ما زالت صحيحة»; the page's own doubled heading is gone, and the line «أسعار الأسبوع والشهر تُختار أيضًا في المكتب» stays. Every owner's «الأسعار» link lands on \`Packages.html#prices\`, and an owner's page opened at an anchor brings it into view. The table's shared parts take three props the admin's editor never passes (S1), so the admin's editor is unchanged; O6's «الفترة» and «لمن» inside the table wait for worker A's editor (DI-30) \| \`Owner space profile.html\`, \`Packages.html\`, \`Data reports.html\`, \`masaha/owner.jsx\`, \`owner-data.js\`, \`profile-b.jsx\` (\`PricesSection\`) \|` |
| 4 | `docs(design): capacity and stay move to Settings` (48) | `profile-b.jsx`, `Owner space profile.html`, `Owner settings.html`, `INDEX.md`, `Flows - states.html`, `CHANGES.md` | `\| **O2, OW-021** \| The profile keeps only what visitors see: capacity and the stay limit leave it for Settings' first card, **«الحضور والحالة المباشرة»** (\`#attendance\`) — the capacity, «لا تظهر للزوار. بها تُحسب الحالة «ممتلئ»؛ بدونها لا تظهر حالة مباشرة»; the automatic check-out at closing; and «خروج تلقائي بعد (ساعات)», optional, whole hours from 1 to 23 (S9). The untrue «يظهر في قواعد المساحة» is gone, and so is \`CapacitySection\` (S2). Rounding's first choice is the model's: «تقريب لأعلى بعد [15] دقيقة», the minutes typed (1–59) with their live example; student prices for visits start on, as the model's default does; the page is \`max-w-3xl\`. **DI-38:** each card fails on its own (\`?fail=save-attendance\`, \`save-pricing\`, \`save-message\`). The board's two capacity frames now open \`Owner settings.html#attendance\` \| \`Owner settings.html\`, \`Owner space profile.html\`, \`profile-b.jsx\`, \`INDEX.md\`, \`Flows - states.html\` \|` (drop the DI-38 sentence if the reply does not fold it) |
| 5 | `docs(design): packages: the form the model holds` (48) | `Packages.html`, `CHANGES.md` | `\| **O8, OW-009** \| The private packages are **rows** — the name, the terms, the price in \`label\` weight, «متاحة في المكتب» and «تعديل», a paused row muted with «موقوفة»; pausing raises no toast (the row says it). The sheet asks what the model holds, required first: the name («اسم مستخدم لباقة أخرى» on a repeat), **the validity, required** («ينتهي الاشتراك بعد هذه المدة من بدايته»), then **«الحدود» on demand** — four chips, each showing its field, days a week 1–7 — then **one billing choice**, «سعر ثابت · بالساعة · باليوم», with one amount labelled for it (\`FIXED · PER_HOUR · PER_DAY\`), **above zero** (the owner, 2026-10-13: «أدخل مبلغًا أكبر من صفر»), «لمن: الجميع · الطلاب», and the space's own shifts — none saved: the reason and the way to add them (\`?demo=noshifts\`). The summary stays; a failure stays in the sheet (\`?fail=save\`) \| \`Packages.html\` \|` |
| 6 | `docs(design): announcements follow the model` (44) | `owner.jsx`, `owner-data.js`, `Announcements.html`, `INDEX.md`, `Flows - states.html`, `README.md`, `CHANGES.md` | `\| **O9, O10, OW-014** \| An announcement is what the model holds: **an Arabic text, required, an English one, optional**, a type and a period — no title and no «أنشأه». Its card leads with the type and the period, then the text. **It can end now** («إنهاء الآن», at once, «تراجع» in the toast; a closure's says the state is automatic again), **be deleted while scheduled** (\`AlertDialog\`, destructive), **start now** and **have no end** («بلا موعد · يبقى حتى تنهيه»); a closure's sheet says the space shows «مغلق الآن» for the period. The type is a \`RadioGroup\` whose rows say what each does; type badges are \`neutral\`, \`warning\` for an outage and a closure. Reception may do all of it, as the API lets it. The sample moved to \`owner-data.js\` (S3) with an ended closure still to extend (S4) \| \`Announcements.html\`, \`masaha/owner.jsx\`, \`owner-data.js\`, \`INDEX.md\`, \`Flows - states.html\` \|` |
| 7 | `docs(design): the closure extension stands alone` (48) | `Announcements.html`, `CHANGES.md` | `\| **O11** \| The closure extension left the edit sheet, which keeps one primary. Once a closure has started, its card offers the owner «تمديد الاشتراكات», an \`AlertDialog\`: «تمديد اشتراكات المشتركين النشطين بأيام الإغلاق؟», «عدد الأيام» (the closure's days so far, at least one), «تتأخر نهاية 25 اشتراكًا نشطًا يومين. لا يمكن التراجع، ولا تطبيقه مرة ثانية لهذا الإغلاق.», and the destructive «مدّد 25 اشتراكًا». Afterwards the card says «مُدِّد 19 اشتراكًا 3 أيام · أحمد · 17 سبتمبر». A scheduled closure offers nothing yet; reception reads «يمدّد المالك الاشتراكات بعد الإغلاق». \`?extend=a6\` opens it \| \`Announcements.html\` \|` |
| 8 | `docs(design): staff: say what reaches people` (44) | `Staff.html`, `INDEX.md`, `Flows - states.html`, `CHANGES.md` | `\| **O4, OW-017–019** \| The staff table has the columns the model fills — the name with the email under it, the state, «أُضيف في», «مقبوضاته هذا الشهر» — and a \`warning\` «لم يغيّر كلمة المرور المؤقتة بعد» while the handover is pending; «الدور» and «آخر دخول» are gone. The owner **removes access** to a space, not an account: «إيقاف الوصول», whose dialog says the sessions end on every device, the person no longer reaches the space, the name stays on the payments and in the log, and access can come back; «إعادة الوصول» acts at once (S5). **Adding staff is one submit**, «إضافة إلى الاستقبال», with both outcomes said before it; the server's answer decides: a linked account's toast, access given back to someone removed, or the temporary password — under A5's rules: no X, Escape and a click outside do nothing, «تم» waits for «نسخ», and the handover is asked \| \`Staff.html\`, \`INDEX.md\`, \`Flows - states.html\` \|` |
| 9 | `docs(design): reports: the reporter is a visitor` (48) | `owner.jsx`, `owner-data.js`, `Data reports.html`, `Owner space profile.html`, `Packages.html`, `CHANGES.md` | `\| **O12, A8** \| The owner never sees who reported: «زائر» and the date, in the list, the sheet and the notice; the admin keeps the name. «لم يُعتمد» requires the reply, the only thing the reporter reads. «تعديل الحقل» carries the report to the field it is about, on the profile or on Packages & prices, where an \`Alert\` holds its words, its date, «تم التصحيح» and «فتح البلاغ للرد» (\`?report=d1#report\`). The sidebar's badge counts the new reports \| \`Data reports.html\`, \`Owner space profile.html\`, \`Packages.html\`, \`masaha/owner.jsx\` (\`OwnerReportNotice\`), \`owner-data.js\` \|` |
| 10 | `docs(design): finance: one month, lists that page` (49) | `Finance.html`, `CHANGES.md` | `\| **OW-015, OW-016** \| The date range that changed nothing is gone. **One «الشهر» \`Select\`** (the last 12 months) drives what counts by month — the month's income tile, the collections by staff, «دفعوا في …» and the occupancy figures — and each names its month; the charts keep their fixed windows, now named (the heatmap's «آخر 4 أسابيع»). The export says what it exports, «تصدير الدخل (CSV)». «عليهم مبالغ» pages, largest first; «دفعوا في …» shows five and «عرض الكل». \`?month=2026-08\` opens a month \| \`Finance.html\` \|` |
| 11 | `docs(design): the owner's overview is a work queue` (50) | `owner.jsx`, `Owner overview.html`, `CHANGES.md` | `\| **O3 (amended)** \| **No money on the overview** (the owner, 2026-10-12): it is often open at the desk, in view of customers and staff, so income and debt live in «المالية والتقارير» only. It opens on **«يحتاج انتباهك»**, counts and links: a group missing or out of date (prices to \`Packages.html#prices\`), new reports, visits not collected today, customers who owe, a closure that started without its extension, and capacity not set — each with «مراجعة» or its own way there, none with a confirm (it lives beside what it confirms). Nothing to do reads «كل شيء على ما يرام». Then «الحاضرون الآن» with today's attendance, and «إعلانات نشطة», now a link; then the subscriptions ending this week. No bottom bar and no desk shortcut in the bar (S7). Without capacity the shell's control says «بلا حالة مباشرة» (S8). \`?demo=missing\`, \`nocapacity\` and \`clear\` show those states \| \`Owner overview.html\`, \`masaha/owner.jsx\` \|` |
| 12 | `docs(design): the owner's audit log` (35) | `Owner audit.html` (new), `owner.jsx`, `owner-data.js`, `SCREENS.md`, `README.md`, `CHANGES.md` | `\| **O13** \| **«سجل التدقيق»** joins «الفريق والإعدادات»: the admin's audit page (AD-028) scoped to the space — payments recorded and voided, check-outs, customers, staff, announcements, the extension, packages, saves and confirms, settings — each target a link to its page, \`neutral\` badges with red only for the acts whose confirmation is destructive, «آخر 30 يومًا», and «المنفّذ», since the space has three: أحمد، سامي، and «النظام» for automatic check-outs (S12). 64 sample lines, so it pages \| new \`Owner audit.html\`, \`masaha/owner.jsx\`, \`owner-data.js\`, \`SCREENS.md\`, \`README.md\` \|` |
| 13 | `docs(design): the board's owner frames` (38) | `Flows - states.html`, `INDEX.md`, `README.md`, `SCREENS.md`, `CHANGES.md` | `\| **Board** \| A new section, «Batch 5 — the owner's management», with 22 frames of the states above, listed in \`INDEX.md\` §55; the board's eight owner frames whose state moved are relabelled \| \`Flows - states.html\`, \`INDEX.md\`, \`README.md\`, \`SCREENS.md\` \|` |

In the `CHANGES.md` table each line is written **without** the escaping backslashes shown above (they are
there only because this plan's table holds them).

### `INDEX.md` rows each commit adds
**The parameters table** — commit 1 adds, after the *Batch 3* table:
```
### Batch 5 — the owner's management

| Parameter | Where | What it shows |
|---|---|---|
| `?drawer=open` | the owner's and reception's pages, on a phone | the drawer, open, with the account at its head (DI-10) |
```
and later commits append rows to it:
- c3: `| \`?demo=missing\` | \`Owner space profile.html\`, \`Owner overview.html\` | the amenities never saved: A2's checklist on the profile, «لم تُضف بعد» in the overview's queue |`
  and `| \`Packages.html#prices\` | Packages & prices | the published prices' table, where every «الأسعار» link lands (O6) |`
- c4: `| \`Owner settings.html#attendance\` | Settings | «الحضور والحالة المباشرة»: capacity and the check-out rules (O2) |`
  and (if DI-38 folds) `| \`?fail=save-attendance\` · \`save-pricing\` · \`save-message\` | \`Owner settings.html\` | one card's save failing, in that card only |`
- c5: `| \`Packages.html?demo=noshifts\` | the package sheet | no shift saved: the reason and the link to the hours |`
  and `| \`?fail=save\` | the package sheet | the save failing inside the sheet |`
- c6: `| \`Announcements.html?delete=a1\` | announcements | deleting a scheduled announcement: the confirmation |`
  and `| \`?fail=end\` | announcements | «إنهاء الآن» failing: the toast with «إعادة المحاولة» |`
- c7: `| \`Announcements.html?tab=ended&extend=a6\` | announcements (owner) | the closure extension's confirmation for a closure that has ended (O11) |`
  and `| \`?fail=extend\` | the same | the extension failing |`
- c8: `| \`?fail=add\` | \`Staff.html\` | adding a staff member failing inside the sheet |`
- c9: `| \`Owner space profile.html?report=d1#report\` · \`Packages.html?report=d2#report\` | the owner's editor | the report «تعديل الحقل» carried there, above its section, with «تم التصحيح» (O12, A8) |`
- c10: `| \`Finance.html?month=2026-08\` | Finance | the month chosen (OW-015) |`
- c11: `| \`Owner overview.html?demo=nocapacity\` · \`?demo=clear\` | the overview | no capacity set (the queue's row, «بلا حالة مباشرة»), or nothing to do («كل شيء على ما يرام») |`
- c12: `| \`Owner audit.html\` | the owner's audit log | the space's log (O13); \`?state=loading\` its skeleton |`

**Relabelled rows** (c4: §36's two; c6: §38's six; c9: §37's four) as §3.4, §3.6, §3.9 say.

**Commit 13 — section 55** (append at the end of `INDEX.md`):
```
## 55 · Batch 5 — the owner's management

Added by the owner's fix (`CHANGES.md` › *Batch 5*). No screenshot yet: `screens/` is regenerated once, at the end of the fix phase.

| Frame | Prototype URL | Viewport | Screenshot |
|---|---|---|---|
```
then one row per frame, in this (board) order, `| <label> | \`<url>\` | <WxH> | — |`:
| # | Label | URL | Size | Board left, top |
|---|---|---|---|---|
| 1 | Overview · a work queue, no money — desktop 1440 | `Owner overview.html` | 1440×1000 | 40, 150090 |
| 2 | Overview · a work queue — phone 390 | `Owner overview.html` | 390×844 | 1512, 150090 |
| 3 | Overview · nothing needs you — phone 390 | `Owner overview.html?demo=clear` | 390×844 | 1982, 150090 |
| 4 | Phone bar · the account heads the drawer — phone 390 | `Owner overview.html?drawer=open` | 390×844 | 2452, 150090 |
| 5 | Overview · no capacity, a group never saved — desktop 1440 | `Owner overview.html?demo=missing,nocapacity` | 1440×1000 | 40, 151170 |
| 6 | Space profile · a report on its section — phone 390 | `Owner space profile.html?report=d1#report` | 390×844 | 1512, 151170 |
| 7 | New package · limits on demand — phone 390 | `Packages.html?sheet=new` | 390×844 | 1982, 151170 |
| 8 | New announcement · the model's fields — phone 390 | `Announcements.html?sheet=new&type=closure` | 390×844 | 2452, 151170 |
| 9 | Space profile · the editor, prices as a row — desktop 1440 | `Owner space profile.html` | 1440×1000 | 40, 152250 |
| 10 | Packages & prices · two sections — desktop 1440 | `Packages.html` | 1440×1000 | 1512, 152250 |
| 11 | Edit package · per day, no shifts saved — desktop 1440 | `Packages.html?edit=p4&demo=noshifts` | 1440×1000 | 40, 153330 |
| 12 | Announcements · end now, no end, quiet types — desktop 1440 | `Announcements.html` | 1440×1000 | 1512, 153330 |
| 13 | Closure extension · the confirmation — desktop 1440 | `Announcements.html?tab=ended&extend=a6` | 1440×1000 | 40, 154410 |
| 14 | Closure extension · reception's line — phone 390 | `Announcements.html?role=reception&tab=ended` | 390×844 | 1512, 154410 |
| 15 | Staff · the password, shown once — phone 390 | `Staff.html?pass=1` | 390×844 | 1982, 154410 |
| 16 | Finance · debts that page — phone 390 | `Finance.html?tab=debts` | 390×844 | 2452, 154410 |
| 17 | Audit log · the space's — phone 390 | `Owner audit.html` | 390×844 | 2922, 154410 |
| 18 | Staff · real columns, a pending password — desktop 1440 | `Staff.html` | 1440×1000 | 40, 155490 |
| 19 | Data reports · the reporter is a visitor — desktop 1440 | `Data reports.html?open=d1` | 1440×1000 | 1512, 155490 |
| 20 | Finance · one month — desktop 1440 | `Finance.html?month=2026-08` | 1440×1000 | 40, 156570 |
| 21 | Settings · attendance and the live state — desktop 1440 | `Owner settings.html#attendance` | 1440×1000 | 1512, 156570 |
| 22 | Audit log · the space's — desktop 1440 | `Owner audit.html` | 1440×1000 | 40, 157650 |

**The board** — before `</body>` of `Flows - states.html`, append:
`<div class="section" style="left:40px;top:150000px"><h2>Batch 5 — the owner's management</h2><p>A work queue with no money · one editor, prices on their page · packages the model holds · announcements that end · the extension on its own · staff told the truth · one month · the space's audit log</p></div>`
then one line per frame, exactly in the form of section 53's lines:
`<div class="frame" style="left:<L>px;top:<T>px"><p><label></p><iframe loading="lazy" src="<url>" width="<W>" height="<H>" title="<label>"></iframe></div>`
with the URL's spaces as `%20` and every `&` as `&amp;`.

**`README.md`** — *What is here*: «Every frame of the design board (493 frames in 53 sections)» → «(515 frames in 54 sections)».
If batch 4 merged first, add its frames and section too (rebase rule).
**`SCREENS.md`** — append `, 55` to the *Board sections* of rows 12, 18, 19, 20, 21, 22, 23, 24.

---

## 7. The executor's procedure

0. **Before anything:** read this plan whole; read `DECISIONS_OWNER.md`. Do not start before the owner's
   reply to §4 is in `C:\Users\basel\.prompt\MASAHA_DESIGN\PROMPT\FIX_OWNER_PLAN_REPLY.md`; apply its answers.
1. **Branch** (Git Bash, in `C:\Users\basel\masaha-design`):
   ```bash
   git fetch origin --prune && git status --short   # must print nothing
   git rev-parse HEAD origin/main                   # note both; main may have moved
   git switch --no-track -c design/owner origin/main
   ```
   If `origin/main` is no longer `e30a86c`, read `git log --oneline e30a86c..origin/main -- docs/design`;
   if a commit touched a file of §5, stop and report before building.
2. **Server** (background shell; note its PID):
   ```bash
   cd "/c/Users/basel/masaha-design/docs/design/prototype" && python -m http.server 5346 --bind 127.0.0.1
   ```
3. **The browser pass script** — save (outside the repo) as
   `C:\Users\basel\Downloads\design-fix-owner\tools\pass.mjs`:
   ```js
   // node pass.mjs <base> <urls.txt> <outdir> [--all] [--shots]
   import { spawn } from 'node:child_process';
   import { readFileSync, mkdirSync, writeFileSync } from 'node:fs';
   import { join } from 'node:path';
   const [base, list, out] = process.argv.slice(2);
   const all = process.argv.includes('--all'), shots = process.argv.includes('--shots');
   const CHROME = process.env.CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
   mkdirSync(out, { recursive: true });
   const chrome = spawn(CHROME, ['--headless=new', '--remote-debugging-port=9333', '--user-data-dir=' + join(out, '.profile'), '--hide-scrollbars', 'about:blank'], { stdio: 'ignore' });
   const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
   let ws;
   for (let i = 0; i < 50 && !ws; i++) { try { const t = await (await fetch('http://127.0.0.1:9333/json/list')).json(); const p = t.find((x) => x.type === 'page'); if (p) ws = p.webSocketDebuggerUrl; } catch {} if (!ws) await sleep(200); }
   const sock = new WebSocket(ws); await new Promise((r) => sock.addEventListener('open', r, { once: true }));
   let id = 0; const wait = new Map(); const errors = [];
   sock.addEventListener('message', (e) => { const m = JSON.parse(e.data); if (m.id && wait.has(m.id)) { wait.get(m.id)(m); wait.delete(m.id); } if (m.method === 'Runtime.exceptionThrown') errors.push(m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text); if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') errors.push(m.params.args.map((a) => a.value ?? a.description).join(' ')); });
   const send = (method, params = {}) => new Promise((r) => { const n = ++id; wait.set(n, r); sock.send(JSON.stringify({ id: n, method, params })); });
   await send('Runtime.enable'); await send('Page.enable');
   const withQ = (u, q) => { if (!q) return u; const [p, h] = u.split('#'); return p + (p.includes('?') ? '&' : '?') + q + (h ? '#' + h : ''); };
   const variants = all ? ['', 'lang=en', 'theme=dark', 'lang=en&theme=dark'] : ['', 'lang=en&theme=dark'];
   const rows = ['url\twidth\tblank\toverflow\terrors'];
   for (const u0 of readFileSync(list, 'utf8').split(/\r?\n/).map((s) => s.trim()).filter(Boolean)) {
     for (const q of variants) { const url = withQ(u0, q);
       for (const width of [390, 768, 1440]) {
         errors.length = 0;
         await send('Emulation.setDeviceMetricsOverride', { width, height: width === 390 ? 844 : 1000, deviceScaleFactor: 1, mobile: width === 390 });
         await send('Page.navigate', { url: base + url });
         await sleep(3500);
         const r = await send('Runtime.evaluate', { expression: "JSON.stringify({ blank: !document.getElementById('ds-root') || !document.getElementById('ds-root').children.length, overflow: document.documentElement.scrollWidth > window.innerWidth + 1 })", returnByValue: true });
         const v = JSON.parse(r.result.result.value);
         rows.push([url, width, v.blank, v.overflow, errors.join(' | ')].join('\t'));
         if (shots) { const s = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false }); writeFileSync(join(out, url.replace(/[^\w]+/g, '_').slice(0, 90) + '-' + width + '.png'), Buffer.from(s.result.data, 'base64')); }
       } }
   }
   writeFileSync(join(out, 'pass.tsv'), rows.join('\n')); console.log(rows.join('\n'));
   sock.close(); chrome.kill();
   ```
   Run it as `node "C:/Users/basel/Downloads/design-fix-owner/tools/pass.mjs" http://127.0.0.1:5346/ urls-<n>.txt "C:/Users/basel/Downloads/design-fix-owner/pass-<n>" --shots`
   (from the `tools` folder; never from inside the repo's `node_modules`). A row with `true` in *blank* or
   *overflow*, or any *errors*, is a failure to fix before committing. **Before trusting it**, break a
   page on purpose once (a stray `}` in a scratch copy is not needed — run it once against
   `Owner overview.html?state=404`: *blank* must be `false`; then against a URL of a page that does not
   exist, `Nope.html`: *blank* must be `true`), so you have seen it catch a blank page.
4. **Before images** (from the clean branch, before the first edit): a `urls-before.txt` with
   `Owner%20overview.html`, `Owner%20space%20profile.html`, `Owner%20space%20profile.html#capacity`,
   `Packages.html`, `Packages.html?sheet=new`, `Packages.html?edit=p4`, `Announcements.html`,
   `Announcements.html?sheet=new&type=event`, `Announcements.html?tab=scheduled&edit=a1`, `Staff.html`,
   `Staff.html?pass=1`, `Staff.html?stop=1`, `Staff.html?sheet=add&email=nour@example.com`,
   `Data%20reports.html?open=d1`, `Finance.html`, `Finance.html?tab=debts`, `Owner%20settings.html`,
   `Admin%20space%20edit.html?id=golden`, `Admin%20space%20edit.html?id=focus`, `Desk.html`; run the
   script with `--shots` into `C:\Users\basel\Downloads\design-fix-owner\before\`. Never commit images.
5. **At every commit**, in this order:
   ```bash
   node docs/design/scripts/check-parse.mjs && node docs/design/scripts/check-classes.mjs
   git diff --stat            # only the commit's files (§6)
   git add <each file by path> && git commit -m "<subject>"
   ```
   then the pass script on the commit's frames (the table below), **and look at the PNGs yourself** at 390,
   768 and 1440. A commit is not done until both are clean.

   | After commit | URLs to pass (and look at) | Look for |
   |---|---|---|
   | 1 | `Owner%20overview.html`, `Owner%20overview.html?drawer=open`, `Finance.html`, `Desk.html`, `Desk.html?role=reception`, `Announcements.html?role=reception` | 390: one row, no avatar, the title not cut to a stub, «⋯» and the state control visible; the drawer: the account row first, its menu without theme/language; 768/1440: the bar exactly as before |
   | 2 | `Owner%20overview.html`, `Announcements.html`, `Finance.html?tab=debts`, `Owner%20space%20profile.html` (type in a field to show the alert) | the ending lines' words; the tab badges' spacing in Arabic and English; no «( 2 )» |
   | 3 | `Owner%20space%20profile.html`, `Owner%20space%20profile.html?demo=missing`, `Owner%20space%20profile.html#prices`, `Packages.html`, `Packages.html#prices`, `Admin%20space%20edit.html?id=golden`, `Admin%20space%20edit.html?id=focus`, `Admin%20space%20edit.html?id=new` | the profile's dates and «قديمة» on prices and contacts; the checklist only with `demo=missing`; the prices row's button at 390 (it moves into the content? — `CardAction` stays in the header: check it does not squeeze the title; if it does, move the button into a `CardContent` below 768 like `ProfileSection` does); Packages: one h2 for the prices; `#prices` lands on the table; **the admin's three pages identical to their before images** |
   | 4 | `Owner%20settings.html`, `Owner%20settings.html#attendance`, `Owner%20settings.html?fail=save-attendance`, `Owner%20space%20profile.html` | the card first; the minutes box inline with its words at 390 (wraps cleanly), the example under it; no capacity on the profile |
   | 5 | `Packages.html`, `Packages.html?sheet=new`, `Packages.html?edit=p4`, `Packages.html?edit=p4&demo=noshifts`, `Packages.html?sheet=new&fail=save` | the rows at 390 (price, switch, edit wrap under the name); the paused row muted; the chips wrap inside the ¾ sheet at 390 with no field cut at its edge; submit empty → the errors and the focus; 0 → «أدخل مبلغًا أكبر من صفر» |
   | 6 | `Announcements.html`, `Announcements.html?tab=scheduled`, `Announcements.html?tab=ended`, `Announcements.html?tab=ended&edit=a4`, `Announcements.html?sheet=new&type=closure`, `Announcements.html?tab=scheduled&edit=a1`, `Announcements.html?delete=a1`, `Announcements.html?role=reception` | no «أنشأه», no title field; the radio rows' hints; «يبدأ/ينتهي» toggles and the date/time pair at 390; the closure note; «إنهاء الآن» then «تراجع» brings it back; the a3 card «بلا موعد انتهاء»; English shows a5's Arabic text right-to-left |
   | 7 | `Announcements.html?tab=ended`, `Announcements.html?tab=ended&extend=a6`, `Announcements.html?role=reception&tab=ended`, `Announcements.html?tab=scheduled` | the dialog's words in both languages (plural forms), the field, the destructive action; the a4 line; no extension on the scheduled closure; the sheet has one primary |
   | 8 | `Staff.html`, `Staff.html?pass=1`, `Staff.html?stop=1`, `Staff.html?sheet=add`, `Staff.html?sheet=add&email=nour@example.com`, `Staff.html?sheet=add&fail=add`, `Staff.html?state=empty` | five columns at 768 (a table) and 1440; the warning badge's wrap; Escape on the password dialog does nothing (press it in a real browser once) |
   | 9 | `Data%20reports.html`, `Data%20reports.html?open=d1`, `Owner%20space%20profile.html?report=d1#report`, `Packages.html?report=d2#report`, `Owner%20space%20profile.html?report=d3` | no reporter's name anywhere; «لم يُعتمد» empty → the error, focused; the notice above its section, brought into view; `d3` (not new) shows nothing |
   | 10 | `Finance.html`, `Finance.html?month=2026-08`, `Finance.html?tab=debts`, `Finance.html?tab=occupancy&month=2026-03` | the Select's width at 390 and beside the tabs at 1440; month names on the blocks; the debtors' paging footer; «عرض الكل» only with more than five |
   | 11 | `Owner%20overview.html`, `Owner%20overview.html?demo=clear`, `Owner%20overview.html?demo=missing,nocapacity` | **no ₪ anywhere**; the queue first at every width; each action's target opens; «كل شيء على ما يرام»; «بلا حالة مباشرة» in the bar and the card |
   | 12 | `Owner%20audit.html`, `Owner%20audit.html?state=loading`, `Owner%20settings.html` (the nav item) | the nav item in its group, active on the page; three actors; red only on void, remove access, extension, photo; targets open |
   | 13 | every frame of §6's table, with `--all` (the full matrix: 2 languages × 2 themes × 3 widths) | the board loads its new section (open `Flows%20-%20states.html`, scroll to the bottom) |
6. **After images:** run the commit-4..12 URL lists plus the before list with `--shots` into
   `C:\Users\basel\Downloads\design-fix-owner\after\`; name pairs by decision when copying the ones for the
   PR (`O3-overview-390-before.png` / `-after.png`, one pair per decision: DI-10, O1, O2, O3, O5, O6, O8,
   O9, O10, O11, O12, O13, OW-015, OW-017). Never commit them.
7. **The head's checks** (from the repo root): `npm ci` if `node_modules` is missing, then
   `npm run format:check` and `npm run check:links`. Both must pass. Report honestly that
   `.prettierignore` excludes `docs/design/` and `*.md`, so `format:check` sees none of this batch's files;
   `check:links` does check `CHANGES.md`, `INDEX.md`, `README.md`, `SCREENS.md` (the finding link).
8. **Push and the PR:**
   ```bash
   git push -u origin design/owner
   gh pr create --assignee @me --title "design: the owner's management" --label docs --label area:docs --body-file "C:/Users/basel/Downloads/design-fix-owner/PR_BODY.md"
   ```
   **The PR description** (write it to `PR_BODY.md`, filling the bracketed results with what was run):
   ```markdown
   ## Summary
   Batch 5 of the design review — the owner's management — applied to the prototype, as the owner amended it:
   no money on the overview (O3), the phone's top bar (DI-10), a package's price above zero, and the editor
   boundary (nothing the admin's editor shows changes). Decisions: `DECISIONS_OWNER.md`; record:
   `docs/design/CHANGES.md` › *Batch 5*.

   ## Scope
   `docs/design/` only: the eight owner pages, a new `Owner audit.html`, `masaha/owner.jsx`, `owner-data.js`,
   `profile-b.jsx` (three default props and the dead `CapacitySection`, nothing the admin's editor shows),
   the board, `CHANGES.md`, `INDEX.md`, `README.md`, `SCREENS.md`.

   ## Acceptance criteria
   - [x] DI-10: the phone bar holds the menu, the title, «⋯» and the state; the account heads the drawer
   - [x] O5: counted words through Arabic's plural forms; tab counts as badges
   - [x] O3: the overview is a work queue of counts and links, with no amount of money
   - [x] O1/O6: the profile is the A1 editor with prices as a link row; prices live on Packages & prices
   - [x] O2/OW-021: capacity and the stay limit in Settings; rounding's minutes; student prices on
   - [x] O8: the package sheet holds what the model holds; the price is above zero
   - [x] O9/O10/OW-014: announcements' model fields; end now, delete, start now, no end; quiet type colours
   - [x] O11: the closure extension is its own destructive action once the closure has started
   - [x] O4/OW-017–019: staff columns, removing access, one submit, the password under A5's rules
   - [x] O12/A8: the reporter is a visitor to the owner; «لم يُعتمد» needs its reply; the report in place
   - [x] OW-015/016: one month; lists that page
   - [x] O13: the owner's audit log
   - [x] No changed page blanks, errors or overflows at 390/768/1440, ar/en, light/dark
   - [x] The admin's editor (`Admin space edit.html?id=golden|focus|new`) is unchanged

   ## Out of scope
   The design-system item (OW-010), the rule changes (api-contract §4, overview.md, glossary, foundation §13),
   the API (OW-017's re-access, O12's owner read), the desk batch's and the account batch's files,
   `Admin space edit.html` (#72), and the shared editor's defects recorded as DI-30–DI-33.

   ## Change type
   docs (design archive)

   ## Evidence
   - `node docs/design/scripts/check-parse.mjs` — [result] at each of the 13 commits
   - `node docs/design/scripts/check-classes.mjs` — [result] at each commit
   - The browser pass (`pass.mjs`): [N] URLs × 4 variants × 3 widths on the head — [0 blank, 0 overflow, 0 console errors]
   - Each changed page looked at, at 390, 768 and 1440
   - `npm run format:check` — [result] (`docs/design/` and Markdown are excluded by `.prettierignore`)
   - `npm run check:links` — [result]

   ## Screenshots
   Before/after pairs per decision were taken locally and are not committed. [Attach the 14 pairs here by drag and drop, or list them.]

   ## Definition of Done
   - [x] Scope verified: only `docs/design/` files of the batch; none of the other batches' files
   - [x] Atomic commits, Conventional Commits, subjects ≤ 50 characters
   - [x] `CHANGES.md` says only what is built
   - [x] `INDEX.md`, the board, `README.md` and `SCREENS.md` agree
   - [x] No object rest, no generic top-level name; no class missing from the prebuilt CSS
   - [x] CI green and the PR `CLEAN`
   ```
9. **CI and CLEAN** — no `jq`; poll with a bound:
   ```bash
   for i in $(seq 1 30); do gh pr checks <n> && break; sleep 30; done
   gh pr view <n> --json mergeStateStatus --jq .mergeStateStatus     # expect CLEAN
   ```
   If not `CLEAN` because `main` moved and conflicts, rebase onto `origin/main` keeping both sides of
   `CHANGES.md`, `INDEX.md`, the board, `README.md` (counts summed) — then push `--force-with-lease`.
10. **The conflict check** against every open PR:
    ```bash
    gh pr list --state open --json number,headRefName --jq '.[] | "\(.number) \(.headRefName)"'
    # for each: git fetch origin <head> && git merge-tree --write-tree --name-only HEAD FETCH_HEAD; echo "exit $?"
    ```
    Expected: conflicts only with the account batch, in the four shared files (the fast path).
11. **The report** — `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\FIX_OWNER_REPORT.md`, sections: the PR
    (number, URL) and its head SHA; the commits (SHA, subject); what was run and its results (each
    command, the pass's totals); problems met and how they were solved; anything unexpected; the conflict
    check per open PR; departures from this plan, each with why; DI-30–DI-40 restated with their routing.
12. **Stop everything:** the server (by its PID; `taskkill //PID <pid> //F` if needed), every Chrome the
    script started (`tasklist | grep -i chrome` — kill only those whose command line has
    `--remote-debugging-port=9333`), every background shell; then `netstat -ano | grep 5346` and
    `netstat -ano | grep 9333` print nothing. **Never merge.**

---

## 8. The reviewer's checklist

For each item: open the file, verify, open the frames (at 390, 768, 1440; ar and en; light and dark).
| Item | File(s) and what to verify | Frames |
|---|---|---|
| AC1 DI-10 | `owner.jsx`: the account `div` is `hidden … md:flex`; `DrawerAccount` passes no `setTheme`; `?drawer=open` effect | `Owner overview.html?drawer=open` 390; `Desk.html` 390 |
| AC2 O5 | `owner.jsx` `AR_PLURAL`, `countText`, `Counted`, the `F_` table as §3.0; grep the owner pages for `أيام\`` and `} أيام` (none glued) | overview, announcements, finance debts |
| AC3 O3 | `Owner overview.html`: no `Money`/`₪`; `queueRows` order and hrefs as §3.8; no `actions` prop | the three overview frames |
| AC4 O1 | profile page: `groupMeta`, `MissingChecklist`, the prices row; `profile-b.jsx` diff = three props + deletion only | profile; **`Admin space edit.html?id=golden`, `?id=focus`, `?id=new` against the before images** |
| AC5 O2 | settings: the card's fields, `saveAtt`, the rounding block, `student: true`, `max-w-3xl` | `Owner settings.html#attendance` |
| AC6 O6/O8 | Packages: one prices h2 (the card's), `hoursHref`, `meta`, rows markup, no toggle toast | `Packages.html`, `#prices` |
| AC7 O8 | `PackageSheet`: field order, each error string, amount > 0, `LIMITS`, `SHIFTS_NOW` | `?sheet=new`, `?edit=p4&demo=noshifts` |
| AC8–10 O9–O11 | announcements: `TYPES` colours, the sheet's fields, `endNow` undo, the delete dialog, `ExtendDialog`'s strings and `extendable` | §6 frames 8, 12, 13, 14; `?delete=a1` |
| AC11 staff | columns, `StatusB`, the dialog body, `StaffPassDialog` = `TempPassDialog` minus `line` | `Staff.html`, `?pass=1`, `?stop=1`, `?sheet=add` |
| AC12 reports | `owner-data.js` reports have no `who`; `OwnerReportNotice` uses `O.fmtDate`; A8's reply rule | `Data reports.html?open=d1`, `Owner space profile.html?report=d1#report` |
| AC13 finance | no `FilterSheet`/`RangePicker` on the page; `MONTH_OPTS`; `usePaged(debtors)`; CSV labels | `Finance.html?month=2026-08`, `?tab=debts` |
| AC14 audit | `Owner audit.html` = the admin's page with §3.12's differences; `RED`; nav item | `Owner audit.html` |
| AC15 states | `?state=loading` on staff, reports, audit; `?state=error|offline|403|404` on each page; each `?fail=` key of §6 | as listed |
| AC17–19 | run the two scripts; `git diff --stat origin/main` lists only §5's files; the board's section at top 150000 with 22 frames; `INDEX.md` §55 has 22 rows; `README.md` 515/54/41 | — |
| Hazards | below — grep for `...` inside `{ }` destructuring in the changed files; for top-level `name`; for classes in §2's dead list | — |

## 9. The hazards

- **Babel's shared globals.** Every page's modules and inline scripts share one global scope. **No object
  rest destructuring** (`const { a, ...rest } = props` or `function X({ a, ...p })`) anywhere — its
  `_excluded` helper is page-wide (`README.md`, DI-27). `Owner overview.html`'s old `MoneyTile({ href, ...p })`
  is deleted, not copied. Array destructuring with holes (`[l, , h]`) and spreads into objects (`{ ...x }`)
  are fine. **No top-level `name`** or other generic top-level names (`title`, `status`, `open`, `type`,
  `data`, `list`, `rows`): new top-level names are the ones §2 lists as checked free, plus page-local
  constants already shown in §3 (`LIMITS`, `SHIFTS_NOW`, `priceText`, `textOf`, `extendable`, `ACTION`,
  `RED`, `GROUP_NAME`, `groupHref`, `TYPE_WORD`, `staffFor`, `ratioOf`, `monthTotal`); before adding any
  other, grep it across `masaha/*.jsx` and the page.
- **`O` is already global** (`owner.jsx`: `const O = window.OWNER;`). Never redeclare `const O` in a page
  that loads `owner.jsx` (every owner page does).
- **The prebuilt CSS.** A utility class not in `_ds_bundle.css` is silently dead. Use only classes §2
  lists as present or that already appear in the file you edit; layout-only rules go to `masaha.css` with
  tokens only (none is planned). `check-classes.mjs` must pass — but it does not see classes built in
  conditions or `cn()`, so §2's dead list is checked by eye in those (`'… ' + (p.active ? '' : 'bg-muted')`).
- **The vendored bundle** (`prototype/_ds/`, `_vendor/`) is never edited. `AlertDialogAction` cannot show
  `loading`; the sidebar's drawer has no open prop (hence `?drawer=open`'s click).
- **The editor boundary.** `profile-a.jsx` is not touched; `profile-b.jsx` gets only §3.3's three
  default-preserving props and §3.4's deletion. After commits 3 and 4, `Admin space edit.html?id=golden`,
  `?id=focus` and `?id=new` must match their before images exactly.
- **Truth to the API and the data model.** Nothing on screen the API cannot do: no reporter's name to the
  owner; no title or author on an announcement; a package has one amount and one billing; the extension
  is the owner's only, once, ≥ 1 day; reception may end and delete announcements; capacity may be empty;
  the stay limit is optional. **Live status is a state, never a count**: the overview shows «27 / 40» to
  the owner only (private), and the state words, never a number, as what visitors see.
- **No money on the overview** — not in a tile, a helper, a caption or a toast.
- **Look with your eyes.** The scripts and the pass see blanks, errors and overflow, not layout: #59's F2
  and #61's eleven fixes were found by eyes. Every changed page at 390, 768 and 1440 is looked at.
- **Never commit images; never merge; stop every server, Chrome and shell you start.**

---

## 10. Decisions needed from the owner

1. **S1–S14:** approve as recommended, or name the ones to drop. S2 (deleting `CapacitySection` from the
   shared file), S5 (the gender-neutral verb) and S7 (no desk shortcut on the overview) matter most.
2. **DI-30, DI-31, DI-33** (the shared editor's words, toast and empty gallery): route to worker A's
   S2b-4 and follow later (recommended), or build here as one extra commit.
3. **DI-32** (photo count and WebP): the analyst asks worker B.
4. **DI-38:** fold (recommended) or leave.
5. **DI-34–DI-37, DI-39, DI-40:** record only (admin's bar; batch 6's anchor and month filter; the web's
   one dialog; the layer's sheet; foundation §13).
