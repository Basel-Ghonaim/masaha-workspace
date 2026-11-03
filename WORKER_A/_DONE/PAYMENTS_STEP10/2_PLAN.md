# PAYMENTS_STEP10 — payments, announcements, data reports and favourites on the web (build map steps 9 and 10: screens 17, 18, 23, 28, 10, 11 and the space page's parts) — the plan

> **Approved by the owner, 2026-10-27 — binding on every executor of this plan** (it wins where the plan below
> differs): **§14 points 1–11 as recommended** — S1–S16 as planned; **A1 taken: PR 4 is PR 4a
> (`feat/report-wrong-info`) then PR 4b (`feat/favorites`)**, so five PRs in sequence; finding 8's `FilterTag` built
> in PR 3; P3's grouped navigation recorded as **finding 165** for an item of its own (A4 not taken); S10 (the void
> in a subscription's statement too) taken; **DI-1 … DI-61 approved as written**; the Arabic copy of §9 approved as
> written; the documents of point 8 changed in their PRs as written (foundation §13 screen 11's «ردّ فريقنا», screen
> 18's extension line); the real runs' writes of §13 allowed, **the extension applied with 1 day** on `masaha-demo`'s
> covered seed subscriptions; the ledger opens on **today**; the reviews: Claude for PRs 1–2, a free model for PRs
> 3, 4a, 4b.
> - **The base:** `main` = `39ef0504` — **#124 merged** (the head `5682764b` this plan read). PR 1 may start.
> - **Every execution runs under the owner's autonomy rule** (`C:\dev\masaha\workspace\_SHARED\AUTONOMY_2026-10-25.md`):
>   no stop until ready for review; no stop for the file count; fix rounds run only the touched test files, CI judges.
> - **Moved folders:** the finished task folders are under `_DONE` now — read `WORKER_A\DESK_SCREENS\…` as
>   `WORKER_A\_DONE\DESK_SCREENS\…` (its `scripts\run3.mjs`, `cdp3.mjs`, `prnum4.sh` among them); the plan's paths are
>   already rewritten where found.
> - **Worker B runs beside it:** FINANCE_AUDIT PR 1 (`feat/audit-log`: `apps/api`, `packages/shared`, documents; no
>   `apps/web`). Shared documents only (`api-contract.md`, `v1-mvp.md`, `overview.md`, the findings index — B
>   records 151 and 152, A 165): each keeps its own lines; whichever merges second rebases.
> - **Tracking:** the owner's Issue for this plan lists each PR's acceptance criteria; the supervisor ticks each PR's
>   box once it merges.

> Written 2026-10-26 from `origin/main` **`e6737da5`** (#123 merged: the closure extension's API —
> `GET`/`POST …/announcements/:id/extend-subscriptions`, `CLOSURE_EXTENDED`, `CLOSURE_ALREADY_EXTENDED` — is
> **on the base**). **#124** (`feat/subscription-sheet`, head `5682764b`, open, in its fix round) is read as
> merged: the desk's pages, `features/desk` (the sheet, `OpenSheet`, `useSheetOpener`, `SubscriptionSheetSlot`),
> `Sheet side="end"` full width below 768 px (finding 101) are this plan's starting point. **PR 1 starts only
> after #124 has merged** (§13 check 2). Worker A, folder `C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\`.
> Four PRs in sequence (the owner's decision 2), each cut from the latest `origin/main` once the one before has
> merged, each with its own execution prompt and review. **A1 (recommended, §14.2) splits PR 4 in two.**
> - **PR 1** `feat/payments` — payments (step 9): four commits, ≈ 83 files.
>   Title: `feat(payments): list the space's payments` (commit 3's subject).
> - **PR 2** `feat/announcements` — announcements with the closure extension: four commits, ≈ 73 files.
>   Title: `feat(announcements): list a space's announcements` (commit 1's subject).
> - **PR 3** `feat/data-reports` — the owner's and the admin's data reports: three commits, ≈ 59 files.
>   Title: `feat(data-reports): decide a space's reports` (commit 2's subject). `area:design-system` (commit 1).
> - **PR 4** — the user's side, ≈ 105 files. **With A1:** **PR 4a** `feat/report-wrong-info` — commits 1–2
>   (≈ 41 files), title `feat(data-reports): report wrong information` (commit 2's); **PR 4b** `feat/favorites`
>   — commits 3–6 (≈ 64 files), title `feat(favorites): save a space from its card` (commit 4's),
>   `area:design-system` (commit 3), cut from `main` once 4a merges. Without A1, one PR, titled by commit 2's.
>
> The executor may be any capable coding agent: no step depends on a Claude skill. Finding numbers are this
> item's range, **165 and on**, in the order first recorded (160–164 and 170–171 are taken; 151 is worker B's).
> `#PRNUM` stands for the PR's number until the push (§13). `{date}` is the day the line is committed
> (`YYYY-MM-DD`). Words are written Arabic first, then English. Design issues are **DI-n** (§7), stronger
> decisions **S-n** (§5), alternatives **A-n** (§5). Paths under `apps/web/src/` unless they start with
> `docs/`, `apps/` or `packages/`. Each PR runs under the owner's autonomy rule (decision 6, §13): no stop until
> ready for review.

## 1. Summary

The screens of build map steps 9 and 10 on the web, over an API that is built (#114, #112, #120, #121, #123).
Today the dashboard shows a placeholder for «الدفعات», «دفعاتي اليوم», «الإعلانات» and «بلاغات البيانات»
(the owner's and the admin's); the site has no account pages, no report button, no favourite heart and no
announcement on a space's page.

- **PR 1 — payments (step 9).** The owner's «الدفعات»: the space's payments, 20 a page, by a range of Gaza days
  (today by default, at most 92), staff member, method, kind and «إظهار الملغاة», every filter in the address;
  the totals of the whole filter from the server; each payment's «⋯» with the owner's «إلغاء الدفعة…» and its
  reason. Reception's «دفعاتي اليوم»: its own payments of today, the cash to hand over first, a voided one
  struck through with who voided it and why. The void is the desk module's route, so it stays `desk`'s and the
  payments page sets it in the list's row slot; a subscription's statement offers it too (S10).
- **PR 2 — announcements (screen 18).** The owner's and reception's «الإعلانات»: the running, upcoming and
  ended tabs with their counts; a new announcement and its edit (type, Arabic text, English text, start now or
  at a time, end at a time or none) with a preview of how the space's page shows it; «إنهاء الآن» with
  «تراجع», «ابدأ الآن», «حذف…»; after a closure has started, the owner's «تمديد الاشتراكات»: the preview's days
  and covered subscriptions, the days typed, once.
- **PR 3 — data reports (screens 23, 28).** The owner's «بلاغات البيانات» (the reporter anonymous: «زائر») and
  the admin's (every space, the reporter named, by status, space and field; the admin decides an unverified
  space's, a verified space's read-only); one decision sheet: «تم التصحيح» with an optional reply, «لم يُعتمد»
  with a required one. Finding 8's removable filter tag, built first.
- **PR 4 — the user's side (screens 10, 11 and the space page).** The report button on a space's page and its
  dialog (who reads it, by the space's verification, U10), «بلاغاتي» with the replies, the account's layout and
  its links in the account menu (P4); the favourite heart on the Directory's and Home's cards and beside the
  page's name, «المفضّلة» with «الأقرب إليّ» and the spaces that left; the space page's announcements and a
  running closure's notice at the top (finding 131). A guest's heart or report asks them to sign in, with the
  reason, and the action runs on their return (C4).

No `apps/api`, `packages/shared`, schema, migration, seed, dependency or `shared/copy/*/errors.ts` change: every
route and code this item needs is built.

## 2. The contract

### Scope

**PR 1 — payments**
- `shared/lib`: `dayText`, `dayWord` moved from `features/desk/services` (their second user, S7).
- `features/desk`: the owner's void of a payment — `VoidPaymentAction` (the «⋯» and its dialog), exported; a
  statement's payment row offers it to the owner (S10).
- `features/payments` (new, dashboard-only): the owner's ledger (`PaymentsLedger`) and reception's «دفعاتي
  اليوم» (`MyPaymentsToday`).
- `features/staff`: `useStaffPeople(spaceId)`, exported (the ledger's staff filter).
- `pages/dashboard/space/payments/`: `PaymentsPage` (owner), `MyPaymentsPage` (reception); `routes.tsx`.
- Copy: `payments` (new), `desk.void`. Docs: `payments.md`, `desk.md`, `space-links.md` (staff, one line),
  `architecture.md` §2, `overview.md`, findings 165, 166, 162 (evidence).

**PR 2 — announcements**
- `features/announcements` (new, any page group): the managed list and its summary, the sheet (post and edit),
  end now (with «تراجع»), start now, delete, the closure extension (preview and apply); the public pieces the
  sheet's preview draws (`AnnouncementItem`, `ClosureNotice`), not exported yet.
- `pages/dashboard/space/announcements/AnnouncementsPage.tsx`; `routes.tsx`.
- Copy: `announcements` (new). Docs: `announcements.md`, `subscriptions.md` (one line), `architecture.md` §2,
  §3 (S2's line), §7 (S12's line), `overview.md`.

**PR 3 — data reports**
- `shared/design-system`: `FilterTag` (display), its showcase section, foundation §12's row (finding 8).
- `features/data-reports` (new, any page group): the owner's list and the decision sheet; the admin's list, its
  filters and tags, the same sheet read-only for a verified space.
- `features/space-links`: `AdminSpaceFilter` (one space, searched on the server), exported.
- `pages/dashboard/space/reports/DataReportsPage.tsx`, `pages/dashboard/admin/DataReportsPage.tsx`; `routes.tsx`.
- Copy: `dataReports` (new), `spaceLinks.choices` (one line). Docs: `data-reports.md`, `space-links.md` (one
  line), `foundation.md` §12, `architecture.md` §2, `overview.md`, findings 8 (resolved), 150 (evidence), 167.

**PR 4 — the user's side** (with A1: 4a = commits 1–2, 4b = commits 3–6)
- `features/data-reports`: `ReportAction` (the button, the dialog, the guest's intent), `MyReportsList`.
- `pages/site`: `public/SignInPrompt.tsx` (a guest's sign-in with its reason), `account/AccountLayout.tsx`,
  `account/MyReportsPage.tsx`, `account/FavoritesPage.tsx`; `routes.tsx`, `navigation.ts`; the space page,
  Directory and Home pages set the new slots; `SiteLayout` mounts the favourite's resume; the header and the
  phone menu pass the account's links.
- `features/users`: the account menu's links (P4).
- `shared/design-system`: `HeartIcon` (4b commit 3).
- `features/favorites` (new, any page group): `FavoriteButton`, `RemoveFavorite`, `ResumeFavorite`.
- `features/directory`: the saved ids for the hearts (`GET /me/favorites`, its route), the card's and the
  page's action slots, `FavoritesView` (the account's list, near me, the spaces that left), the page's report
  and announcements slots.
- `features/announcements`: `SpaceAnnouncements`, `ClosureNotice`, exported.
- Copy: `dataReports.report`, `dataReports.mine`, `favorites` (new), `site.signInPrompt`, `site.account`,
  `users.account.links`, `announcements.public`. Docs: `data-reports.md`, `favorites.md`, `directory.md`,
  `announcements.md`, `users.md`, `architecture.md` §2, §7, `overview.md`, findings 131 (resolved), 168.

### Acceptance criteria

**PR 1**
- [ ] `/dashboard/spaces/:id/payments` (owner only) lists the space's payments 20 a page, the latest received
  first: the day and time (Gaza), the customer (a link to their file) or the visitor, the item, the amount with
  its method under it, who recorded it; five columns from 768 px, a card each below it.
- [ ] Filters: the range (one or two Gaza dates, at most 92 days, today by default), the staff member (the owner
  and the space's reception accounts, deactivated ones included), the method, the kind, «إظهار الملغاة»
  (hidden by default); every filter and the page in the address; inline from 768 px, in a bottom sheet below it
  with how many apply (the range counted when set); «مسح الفلاتر» at every width resets all of them.
- [ ] The totals line names its period and says what the server's `meta.totals` says: received in all, by
  cash, by transfer, how many, and the voided ones apart — never a sum of the browser's.
- [ ] A voided payment, when shown, is struck through with a visible «ملغاة» badge and «ألغاها {name}:
  {reason}»; never counted as received.
- [ ] The owner's «⋯» on a payment not voided: «إلغاء الدفعة…» (destructive) opens a dialog naming the amount,
  the customer, the day and the method, with the true consequence and a required reason; sent once with no key;
  a lost answer says a retry is safe; `VISIT_WRITTEN_OFF`, a 404 and a 403 each worded; the focus returns to the
  «⋯», or, the row gone, to the next row's «⋯», else the totals line.
- [ ] A subscription's statement (the customer's file) offers the owner the same «⋯» on a payment not voided
  (S10); reception sees none.
- [ ] `/dashboard/spaces/:id/my-payments` (reception only): «دفعاتي اليوم» — the cash to hand over, the
  transfers (with «وصلت إلى حساب المساحة»), the total and the count, from the server's totals (one card below
  768 px, three cards from it); its own payments of today, a voided one struck with who and why.
- [ ] Lint, typecheck, `test:unit`, the scoped `test:component`, the production build, `check:build` (no
  `payments` or `desk` code, no `data-table`, in the site's first download), `check:classes`, `format:check`,
  `check:links`, `check:conflicts`; CI green; `CLEAN`.

**PR 2**
- [ ] `/dashboard/spaces/:id/announcements` (owner and reception): the tabs «نشطة», «مجدولة», «منتهية», each
  with the summary's count, the tab and the page in the address; each announcement a card — its type (a
  `warning` badge for an outage or a closure, `neutral` otherwise), its period on Gaza's clock, its text in the
  interface's language (the Arabic, marked, when an English one is missing); no status badge (the tab says it).
- [ ] «إعلان جديد» (at the end of the tabs' row) and «تعديل» (not on an ended one) open the sheet: the type with
  its hint, the Arabic text (required), the English text (optional), «يبدأ: الآن · في موعد», «ينتهي: في موعد ·
  بلا موعد», the date and the time on Gaza's clock, a closure's line, the preview of the space's page; the post
  carries one `Idempotency-Key` per opening, kept across a retry and a double press; the server's period
  refusals land on their fields; `CLOSURE_EXTENDED` worded.
- [ ] «إنهاء الآن» (running) acts at once with «تراجع» in its toast (not for an extended closure); «ابدأ الآن»
  (upcoming); «حذف…» (any state, not an extended closure) asks first, naming the announcement and its true
  consequence; each sent once with no key; each toast names the tab where it went.
- [ ] The owner, on a closure that has started and is not extended: «تمديد الاشتراكات» opens the preview — the
  closure's Gaza days, the days proposed, how many subscriptions it covered — the days typed (1–365), one key per
  opening; a failure stays in the dialog with the days kept; `CLOSURE_ALREADY_EXTENDED` worded and the card then
  shows the extension; a closure that covered none says so and offers no extension. Reception reads «يمدّد
  المالك الاشتراكات بعد بدء الإغلاق.»; an extended closure reads how many, how many days, by whom, when.
- [ ] Loading (three skeleton cards), failure with its reference and a retry, empty per tab; the same checks
  and CI.

**PR 3**
- [ ] `FilterTag` in the layer (display), its showcase, foundation §12's row; finding 8 resolved.
- [ ] `/dashboard/spaces/:id/reports` (owner only): the space's reports, 20 a page, «الكل · جديدة · تمت
  المراجعة» (the address); the field, the report (two lines), the day (no time), the status; the reporter
  never named («زائر»). The sheet: the report, «تعديل الحقل» (to Packages & prices or the space's profile), the
  reply, «تم التصحيح» (reply optional) and «لم يُعتمد» (reply required, focused when missing); sent once;
  `REPORT_ALREADY_DECIDED`, a 403 and a 404 worded; a decided report read-only with its reply.
- [ ] `/dashboard/admin/reports` (admin): every space's reports by status (chips), space (a searched combobox)
  and field, every filter in the address and shown in force as removable tags with «مسح الفلاتر»; the
  reporter named; «يعالجه: الإدارة · المالك»; cards until 1024 px; an unverified space's report decided in the
  sheet (with «تعديل الحقل» to the admin's editor), a verified space's read-only with «يعالجه المالك» and a
  link to the space.
- [ ] The same checks and CI.

**PR 4**
- [ ] A space's page: «الإبلاغ عن معلومة غير صحيحة» at the end of its sections opens the dialog (the field,
  the details — required for «أخرى» only — and U10's line by the space's verification); a refusal stays in it
  with the input kept (429 counted down); the toast says where the reply lands, with «عرض بلاغاتي»; a repeat
  says one is already open.
- [ ] `/me/reports` (signed in): «بلاغاتي» 20 a page, «الكل · قيد المراجعة · تمت المراجعة»; each the space
  (a link while listed; its name as text with «لم تعد هذه المساحة معروضة في الدليل» once gone), the field and
  the day, the status, the message (a toggle when long), the reply with who replied. The account's layout and
  its navigation; the account menu (desktop and phone) links «المفضّلة» and «بلاغاتي» on the site.
- [ ] The heart on the Directory's and Home's cards and beside the page's name, for a signed-in visitor: pressed
  at once, a toast with «تراجع» naming the space; a failure puts it back and says so with «إعادة المحاولة»;
  `FAVORITES_LIMIT_REACHED` worded. A guest pressing the heart or the report gets the sign-in dialog with the
  reason; back signed in, the favourite is saved (and said) or the report dialog opens.
- [ ] `/me/favorites` (signed in): every favourite as the directory's card with its heart, newest saved first or
  nearest first with «الأقرب إليّ»; the spaces that left by their names with «إزالة» and «تراجع».
- [ ] A space's page shows its running and upcoming announcements after the status (U8) and a running closure's
  notice at the top; finding 131 resolved.
- [ ] The same checks and CI; `check:build` (no favourites', reports' or announcements' dashboard code in the
  site's first download).

### Out of scope
- Any API, `packages/shared`, schema, seed, dependency or `errors.ts` change.
- The payments CSV export (Finance's, step 11: OW-015's «تصدير الدخل (CSV)»; a page's rows are not the ledger),
  collections per staff member as a table, debts and credit screens (Finance, step 11).
- The owner's overview's queue («بلاغات جديدة», «إغلاق لم تُمدَّد اشتراكاته»), the sidebar's counts (step 12).
- A handled-by filter on the admin's reports (no API parameter, finding 167); the admin's editor's «بلاغات
  <المساحة>» link (AD-012) and its carried report (AD-UX-011): the admin's space editor (`spaces`).
- The report's «القيمة الحالية» block (DI-33, A10); restoring a deleted announcement (no route).
- The dashboard's grouped navigation (P3): not built in the shell, finding 165 (A4).
- «إعدادات حسابي» (screen 9): its page is not built; the account's navigation lists the built pages only.
- Not in v1: online payment, QR check-in, in-app space claiming, booking, reviews.

## 3. The reading done

`CLAUDE.md`; `workflow.md` (whole); `testing.md` (whole); `architecture.md` (whole); `foundation.md` §9, §10,
§12, §13, §15; `localisation.md` (catalogues and plurals, by its use in `shared/copy/plural.ts`);
`documentation.md` §5; `docs/features/payments.md`, `announcements.md`, `data-reports.md`, `favorites.md`,
`directory.md`, `desk.md` (#124's), `subscriptions.md`, `auth.md`; `api-contract.md` §1–4, *Front desk
(managed)* (the payments list, the void), *Announcements (managed)* (the extension), *Data reports*,
*Favourites*, *Directory (public)*, §6; ADR 0009 (its table); `v1-mvp.md` steps 9–10 and the ordering notes;
`overview.md` › *Built*, *Not in v1*; `docs/README.md` › deferred documents; `SCREENS.md`; the findings index
and findings 8, 87, 105, 131, 132, 138, 150, 162, 171. The prototype: `Payments.html`, `My payments.html`,
`Announcements.html`, `Data reports.html`, `Admin reports.html`, `Favorites.html`, `Reports.html`, `Space
details.html`; `desk-core.jsx` (`PaidAmount`, `PaymentMenu`, `VoidDialog`), `finance.jsx` (`RangePicker`),
`shared.jsx` (`FilterSheet`, `usePaged`, `SpaceCard`, `HeartButton`, `useFavourites`, `PageToaster`),
`account.jsx`, `space-parts.jsx` (`AnnouncementsSection`). `DECISIONS_DESK.md`, `DECISIONS_OWNER.md`,
`DECISIONS_ADMIN.md`, `DECISIONS_ACCOUNT.md`, `DECISIONS_PUBLIC.md`, `DECISIONS_SHARED.md`; the round-2 issues
on these screens: `R2-OW-AX` 001, 003, 009, 010; `R2-OW-DF` 001, 003, 008, 010, 012, 013; `R2-OW-EX` 007,
008, 009; `R2-OW-UX` 001, 002, 006, 008; `R2-OW-VD` 001, 002, 005; `R2-AD-UX` 002, 003, 005, 011; `R2-AD-DF`
018; `R2-AD-VD` 003; `R2-AU-AX` 002, 005, 006, 007; `R2-AU-CP` 005; `R2-AU-EX` 002, 003, 004; `R2-AU-UX` 001,
007; `R2-AU-VD` 005, 006; `R2-PU-CP` 010, 011, 019; `R2-PU-UX` 002, 003, 004, 006; `R2-DK-AX` 010, 016, 017;
`R2-DK-CP` 009; `R2-DK-EX` 005; `R2-DK-VD` 001, 012. `_SHARED\OPEN_DECISIONS.md`, `_SHARED\AUTONOMY_2026-10-25.md`;
`WORKER_A\PUBLIC\0_CARRIED_FROM_111.md`; `WORKER_A\_DONE\DESK_SCREENS\2_PLAN.md` (the model), `3_EXEC_PROMPT_PR4.md`
§2–§5, `4_REPORT_PR4.md` (its decisions and fix round). The code (at `origin/main`, the desk at #124's head):
`pages/dashboard` (`routes.tsx`, `navigation.ts`, `placeOf.ts`, the shell's `DashboardNavigation`,
`SpaceLayout`, `PageHeader`, `DeskPage`, `CustomersPage`, `StaffPage`), `pages/site` (`routes.tsx`,
`navigation.ts`, `SignInPage`, `nextSearch.ts`, `SiteHeader`, `SpacePage`), `features/desk` (its tree, keys,
`useDeskWrite`, the write-off's hook and dialog, the statement's hook and component, the customers list's
filters and list), `features/directory` (its tree, `SpaceDetails`, `SpaceHeader`, `SpaceCard`, `SpaceCardView`,
`DirectorySlots`, `DirectoryView`, `HomeSpaces`), `features/space-links` (`SpaceCombobox`,
`useSpaceChoices`), `features/staff` (its repository, hooks), `features/users` (`AccountMenu`,
`AccountMenuContent`, `AccountMenuSection`); `shared/api` (`request.ts`, `useIntentKey`, exports),
`shared/lists`, `shared/forms`, `shared/lib`, `shared/routing` (exports, `returnUrl.ts`), `shared/copy`
(`plural.ts`, the English index, `dashboard.ts`, `errors.ts`' codes), the design system's barrel and icon set,
`src/test/`; `packages/shared`'s `payments`, `announcements`, `data-reports`, `favorites`, `directory`
(`FavoriteSpace`), `core` (`gazaTime.ts`, `idempotencyKey.ts`), `space-links` (`StaffMember`);
`apps/web/scripts/dashboardOnly.ts`, `libraryChunks.ts`; the seeds `demo.ts`, `demoDirectory.ts` (accounts,
the voided payment, the closure).

**What the reading changed.**
- **#123 merged during the reading;** the base is `e6737da5`. #124 is still open (`5682764b`).
- **The void is the desk module's route** (`POST …/payments/:paymentId/void`, contract *Front desk*; payments.md
  "the void is a desk orchestration"), the list is the payments module's (`GET …/payments`): by architecture §3's
  rule the void is `desk`'s on the web, the list `payments`' (S1). A statement's payments carry their `id`
  (`ItemPayment`), so the file can void too (S10).
- **The managed announcements list, its summary and the extension are `subscriptions`' routes** (its `closures`
  router, mounted at `/announcements`); only the writes are `announcements`'. One screen, one audience, the
  contract's one section: S2 keeps them in one web feature, an exception to architecture §3's naming rule.
- **`GET /me/favorites` is the directory's route** (its cards); only the save and the removal are
  `favorites`'. The hearts' state and the account's list are `directory`'s; the heart's write is `favorites'`
  (S1, S13).
- **No route says whether a space is a user's favourite** except the whole list (`GET /me/favorites`, at most
  200, the directory's cards): the hearts read it once per signed-in visit (S13).
- **The admin's reports cannot be filtered by who handles them** (`AdminReport.space.verified` per row only):
  AD-UX-003's chips cannot be built (finding 167, A8).
- **The owner's and the admin's status filter is `OPEN | DECIDED`**, not the prototype's three statuses: the
  chips are «الكل · جديدة · تمت المراجعة» (DI-32).
- **A report's details are required only for «أخرى»** (`createReportSchema`); the prototype required them always
  (DI-44, A11).
- **A repeated report answers 200 with the open one**: telling it apart needs the status, which `api.post`
  drops; the repository reads it through `apiClient` (S15).
- **An announcement's end must be after now** (contract): an ended announcement cannot be posted; «تراجع» of «إنهاء
  الآن» restores the old end by `PATCH`, refused for an extended closure (`CLOSURE_EXTENDED` — a later end), so
  that undo is not offered there (DI-17).
- **The extension covers subscriptions running on any of the closure's days** (decision 4, #123), not "the active
  subscriptions" of O11's wording (DI-20); with none covered the API would still mark the closure extended —
  the screen offers nothing to extend (S11).
- **The payments list names who recorded and who voided each payment** (`PaymentRow`), to reception too (its
  own payments): «دفعاتي اليوم» shows «ألغاها {name}» — part of finding 162 holds no more for that list (§6).
- **The dashboard's navigation is flat** (`DashboardNavigation`: one `SidebarGroup`); P3's groups were never
  built. The four pages already have their places and placeholders (finding 165, A4).
- **No account page exists** (`AccountLayout` "not built yet"; `/me` is screen 9, not this item): PR 4 builds the
  layout with its first two pages.
- **The layer has no heart icon** (its icon set) and no removable tag (finding 8): two small layer commits.
- **`dayText` and `dayWord` live in `features/desk/services`** "until a second user": payments, announcements and
  data reports are three (S7).
- **No data reports and no favourites are seeded;** the demo accounts are `demo-owner`, `demo-reception`
  (global `USER`, reception at `masaha-demo`), `demo-directory-owner`, the admin. PR 3's real run needs reports
  before PR 4 builds the dialog (§14.9).

## 4. The owner's decisions, as they will be built

1. **One item, four PRs** (steps 9 and 10 together) — as the header; A1 splits PR 4 (its ≈ 105 files).
2. **The cut and the order:** PR 1 payments; PR 2 announcements with the extension; PR 3 data reports (the
   owner's and the admin's); PR 4 the user's side. Each cut from `main` once the one before merged. A better
   cut is weighed in A1 (PR 4 split, recommended) and A2 (the reporter's side moved into PR 3, not recommended).
3. **PR 4 and the public site's fix PR** (`WORKER_A\PUBLIC\0_CARRIED_FROM_111.md` + the owner's list): PR 4 comes
   last; either order works. The files both may touch are named in §8 (*Shared with the other items*); PR 4's
   first check is `git diff --name-status <PR 3's merge> origin/main -- apps/web/src/pages/site
   apps/web/src/features/directory apps/web/src/shared/copy docs` — whatever the fix PR changed there is read
   before an edit, and PR 4's slots are added to the code as it then stands (§13 check 3).
4. **Finding 8** (the removable filter tag): **confirmed for PR 3**, its first commit. The settled prototypes
   draw no tag anywhere (P5 replaced the stress test's tag row with the sheet's active count), but the admin's
   reports are the one list whose filters arrive from outside the page (a link with `?space=`) and hide in the
   sheet on a phone: the tags show the space and the field in force at every width (DI-40). The owner may instead
   close finding 8 as superseded by P5 (§14.3).
5. **Reviews:** a Claude review for PR 1 (money) and PR 2 (the extension moves subscriptions' ends); a free
   model's for PR 3 and PR 4 (4a and 4b with A1). §11 writes each PR's focus so either reviewer can follow it.
6. **Execution under the autonomy rule** (`_SHARED\AUTONOMY_2026-10-25.md`): no stop until ready for review;
   §13 lists what the executor decides alone and the limits it never crosses.
7. **The features** → S1. **8. The cache** → S3. **9. Idempotency** → S4. **10. Roles** → S5. **11. The
   navigation** → S6. **12. Widths, states, accessibility** → S8, S9 and each commit in §9. **13. Design issues**
   → §7. **14. Documents this proves wrong** → §14.8.

## 5. Stronger decisions

**S1 — the features, what each owns, and the rule between them.**
| Feature | Group | Owns on the web | Calls |
|---|---|---|---|
| `payments` (new) | dashboard only (listed) | the owner's ledger, reception's «دفعاتي اليوم» | `GET …/payments` |
| `desk` (exists) | dashboard only | + the owner's void of a payment, its «⋯» and dialog (S10: also in a statement) | `POST …/payments/:paymentId/void` (the desk module's) |
| `announcements` (new) | any page group | screen 18 whole; the public pieces (a space's announcements, a closure's notice) the site sets in `directory`'s slots | the announcements module's writes; `subscriptions`' list, summary and extension at the same path (S2) |
| `data-reports` (new) | any page group | the report action and dialog, «بلاغاتي», the owner's list, the admin's list, the decision sheet | its module's three routers |
| `favorites` (new) | any page group | the heart's save and removal (optimistic, «تراجع»), «إزالة» of a space that left, the guest's intent | `POST`/`DELETE /me/favorites/:spaceId` |
| `directory` (exists) | any page group | + the saved ids for the hearts, the account's favourites list (cards, near me, the spaces that left), the card's and the page's slots | `GET /me/favorites` (its route) |
| `staff` (exists) | dashboard only | + `useStaffPeople` (the reception accounts' names) | its list, one cache |
| `space-links` (exists) | dashboard only | + `AdminSpaceFilter` (one space, searched) | `GET /admin/spaces` (its choices) |
- **What stays in the pages:** the routes, titles and guards; each page composes — `PaymentsPage` sets `desk`'s
  `VoidPaymentAction` in the ledger's row slot and passes the people (the session's user and `staff`'s) and the
  customer's link; `CustomerPage` passes the void ability; the admin's `DataReportsPage` sets `space-links`'
  `AdminSpaceFilter` in the list's slot and the editor's link; the site's pages set `favorites`' heart,
  `data-reports`' report action and `announcements`' public pieces in `directory`'s slots, and hold the sign-in
  prompt (`SignInPrompt`, the site's own: it names the site's routes).
- **The rule:** `app → pages → features → shared`; no feature imports another (lint). Features know no routes:
  every link is a prop. Keys meet only through a scope: `desk`'s void and every announcements write invalidate
  `['space', spaceId]` (S3), which refetches `payments`' and `desk`'s lists; `favorites`' writes invalidate
  `['me']`, which refetches `directory`'s favourites.
- *Why:* each capability's web feature calls its own module's routes (architecture §3), and the exceptions are
  named: S2 for the closures router, and `desk`'s existing exception (S1 of DESK_SCREENS) covers the void. A
  `payments` feature holding the void would call the desk module's route; a `favorites` feature reading `GET
  /me/favorites` would call the directory's and draw its cards (A3). *Cost:* three slots on `directory`'s card and
  page, one on `payments`' row. *Recommend:* take it.

**S2 — `announcements` on the web holds screen 18, an exception to "names match the backend."** It calls the
announcements module's writes and the routes `subscriptions` composes at the same path — the managed list, its
summary and a closure's extension (`closures/`). *Why:* the contract has them in one section, one audience (the
staff) works them on one screen, and a `subscriptions` feature for one dialog would put a cross-feature dialog in
the page. *Cost:* architecture §3 gains, after `desk`'s exception: «**`announcements`** holds screen 18: the
announcements module's writes and the managed list, its summary and a closure's extension that `subscriptions`
composes at the same path, the contract's one section (S2, {date}, #PRNUM).» *Recommend:* take it.

**S3 — the cache: keys, refreshes, invalidations.**
| Read | Key | Refreshes |
|---|---|---|
| The ledger's page | `['space', id, 'payments', 'list', query]` | arrival; app defaults (focus once stale); `keepPreviousData` |
| «دفعاتي اليوم»'s page | `['space', id, 'payments', 'mine', page]` | arrival; defaults (focus once stale: the handover is read at the shift's end) |
| The staff's names | `staff`'s own list key (one cache with «الموظفون») | arrival; defaults |
| The announcements' page | `['space', id, 'announcements', 'list', state, page]` | arrival; defaults; `keepPreviousData` |
| The summary (the tabs' counts) | `['space', id, 'announcements', 'summary']` | arrival; defaults |
| A closure's preview | `['space', id, 'announcements', 'preview', announcementId]` | each opening of the dialog (`refetchOnMount: 'always'`): the covered count moves with the subscriptions |
| The owner's reports | `['space', id, 'dataReports', query]` | arrival; defaults; `keepPreviousData` |
| The admin's reports | `['admin', 'dataReports', query]` | the same |
| «بلاغاتي» | `['me', 'reports', query]` | the same |
| The saved ids / the account's favourites | `['me', 'favorites', request]` (`directory`'s; `{}` for the ids, `{ near }` for a sorted list) | arrival while signed in; defaults; the ids query `enabled` only with a session |
**After each write** (never awaited, the toast speaks from the answer at once — DESK_SCREENS S2):
- the void (`desk`) → `['space', spaceId]` (the ledger, «دفعاتي اليوم», the file and its statement);
- every announcements write and the extension → `['space', spaceId]` (S12);
- the owner's decision → `['space', spaceId, 'dataReports']`; the admin's → `['admin', 'dataReports']`; a report
  → `['me', 'reports']`;
- a favourite saved or removed → `['me']` (S13);
- a 404 or a 403 with no code on a dashboard write → `['me']` too (the switcher and the navigation follow), as
  `useDeskWrite`'s `linkEnded` does; `REPORT_ALREADY_DECIDED`, `CLOSURE_ALREADY_EXTENDED`, `CLOSURE_EXTENDED`,
  `ANNOUNCEMENT_NOT_STARTED` and a 404 refetch the list they came from, so the screen shows the truth.
*Recommend:* take it.

**S4 — idempotency in the web: one key per intent where the API reads one.**
| Write | Key | Retry | A lost answer |
|---|---|---|---|
| An announcement's post | one per opening of the sheet (`useIntentKey`, `renew` on open; each opening mounts a new sheet) — kept across the transport's re-sends, a double press (the submit `aria-disabled` while pending), «إعادة المحاولة» and an edit of the form | the transport's (keyed) | «لم يصل الرد. أعد المحاولة — لن يُنشر مرتين.» |
| A closure's extension | one per opening of the dialog | the transport's | «لم يصل الرد. أعد المحاولة — لن تُمدَّد مرتين.» |
| The void | none (a second void answers the first) | never re-sent by itself | «لم يصل الرد. أعد المحاولة — إلغاؤها مرة ثانية لا يغيّر شيئًا.» |
| An announcement's edit, end, start, delete | none (idempotent by design) | never re-sent by itself | `errors.network` / `errors.timeout` with the retry |
| A report | none (the open one answers a repeat, 200) | never re-sent by itself | «لم يصل الرد. أعد المحاولة — لن يُرسَل البلاغ مرتين.» |
| A decision | none (the same decision answers it as it is) | never re-sent by itself | «لم يصل الرد. أعد المحاولة — القرار نفسه لا يُسجَّل مرتين.» |
| A favourite's save or removal | none (204 either way) | never re-sent by itself | the error toast with «إعادة المحاولة» |
- **A new opening after a lost answer is a new intent:** if the first landed, the server says so —
  `CLOSURE_ALREADY_EXTENDED` («مُدّدت اشتراكات هذا الإغلاق من قبل.», the card then shows its extension); a second
  post makes a second announcement (the sheet's lost line tells the user to retry from the same sheet, not a new
  one).
- **Each 409:** `CLOSURE_ALREADY_EXTENDED` (above); `CLOSURE_EXTENDED` (an extended closure's later end, new start,
  new type or delete: `errors.CLOSURE_EXTENDED`, the list refetched); `ANNOUNCEMENT_NOT_STARTED` (end now of one
  another desk moved later, or an extension of one not started: `errors.ANNOUNCEMENT_NOT_STARTED`, refetched);
  `REPORT_ALREADY_DECIDED` (`errors.…`, refetched, the sheet then read-only with the decision);
  `FAVORITES_LIMIT_REACHED` (`errors.…` in an error toast with «إدارة المفضّلة»); the void's `VISIT_WRITTEN_OFF`
  («لا تُلغى دفعة زيارة شُطب مبلغها.» — the write-off's undo lives only in its toast, finding 164); a 409 with no
  code (`errors.conflict`).
- *Why:* ADR 0015 rule 1 where the API reads a key; idempotent-by-design writes are sent once (DESK_SCREENS S3,
  finding 115's pattern). *Recommend:* take it. **No test-only parameter:** tests read the header the fake
  adapter received.

**S5 — roles: what each sees and may press; the server decides every one.**
| Control | Owner | Reception | Admin | Signed-in user | Guest | Server's guard |
|---|---|---|---|---|---|---|
| «الدفعات» (the ledger, its filters) | ✓ | — (no route, no item) | — | — | — | `can()` (403 on a range or `recordedById` from reception) |
| «دفعاتي اليوم» | — | ✓ | — | — | — | `can()` (reception's own of today) |
| «إلغاء الدفعة…» (ledger, statement) | ✓ | — | — | — | — | `payments.void` (403) |
| «الإعلانات»: post, edit, end, start, delete | ✓ | ✓ | — | — | — | `announcements.manage` (403) |
| «تمديد الاشتراكات» | ✓ | — (a line instead) | — | — | — | `subscriptions.extendAfterClosure` (403) |
| The space's «بلاغات البيانات», its decision | ✓ | — | — | — | — | `space.dataReports.read`, `dataReports.resolve` (403) |
| The admin's reports; deciding an unverified space's | — | — | ✓ (a verified one read-only) | — | — | `requireRole('ADMIN')`; `can()` with "verified" (403) |
| The report button | ✓ | ✓ | ✓ | ✓ | the sign-in prompt | `requireAuth` (401) |
| The heart | ✓ | ✓ | ✓ | ✓ | the sign-in prompt | `requireAuth` (401) |
| «بلاغاتي», «المفضّلة» | ✓ | ✓ | ✓ | ✓ | `RequireAuth` → sign-in | `requireAuth` |
The page reads the role **at the space in the URL** from the session's link (ADR 0009, never the global role)
and passes `owner: boolean`. Every refusal is handled: a 403 with no code says «لم يعد هذا متاحًا لك في هذه
المساحة.» (`desk.refusals.forbidden`, reused) and invalidates `['me']`; the admin's 403 on a verified space's
report says «هذه المساحة موثّقة: يقرّر مالكها هذا البلاغ.» and refetches. A test per hidden control proves the
server's refusal is still worded when it is shown by mistake. *Recommend:* take it.

**S6 — the navigation.** The four dashboard pages keep the places `navigation.ts` already gives them (owner:
`payments`, `announcements`, `dataReports` at `reports`; reception: `myPayments` at `my-payments`,
`announcements`; admin: `dataReports` at `reports`): each replaces its placeholder in `SPACE_PAGES` /
`ADMIN_PAGES`; no new sidebar item. P3's groups are not built (A4, finding 165). The site gains `SITE_PATHS.account
= '/me'` (not a route yet), `myFavorites = '/me/favorites'`, `myReports = '/me/reports'`, both under
`AccountLayout` inside `SiteLayout`, each wrapped by `RequireAuth` on its own route; the account menu (desktop and
phone, `users`) gains «المفضّلة» and «بلاغاتي» on the site only (P4); the dashboard's account menu is unchanged.
*Recommend:* take it.

**S7 — `dayText` and `dayWord` move to `shared/lib`** (PR 1 commit 1): their second, third and fourth users
arrive (payments, announcements, data reports); the DESK_SCREENS rule was "in the feature until a second one".
Moved with their tests (`git mv`), `shared/lib/index.ts` exports them, `desk`'s imports follow; no behaviour
changes. *Cost:* ≈ 14 files in a refactor commit. *Recommend:* take it.

**S8 — the lists' addresses** (DESK_SCREENS S11's pattern: a value the server would refuse falls back; a change
replaces the address and returns to page 1; no default written):
- the ledger: `from`, `to` (Gaza dates, both or neither, `to` ≥ `from`, at most 92 days — else both dropped),
  `staff` (`recordedById`), `method`, `kind`, `voided=1`, `page`;
- «دفعاتي اليوم»: `page`;
- announcements: `state` (`upcoming` | `ended`; running not written), `page`;
- the owner's reports: `status` (`open` | `decided`), `page`;
- the admin's reports: `status`, `field`, `space`, `page`;
- «بلاغاتي»: `status`, `page`.
Favourites: none (near me is in memory, the directory's rule). *Recommend:* take it.

**S9 — Gaza's clock for every instant and day.** The sheet's date and time are Gaza's wall clock, sent as
`gazaInstant(date, minute).toISOString()` (`@masaha/shared/core`); a loaded instant is shown by `gazaClockOf`;
the ledger's range is Gaza dates (`YYYY-MM-DD`), «اليوم» by `gazaClockOf(new Date()).date`; every day said by
`dayText`/`dayWord` (S7). Never the browser's zone. *Recommend:* take it.

**S10 — the void in a subscription's statement too** (DK-016 "the void inside the row's «⋯»"; the prototype's
file had it on its payments tab, which DI-43 folded into the statements). The statement's payment rows carry
their `id`; the owner gets the same `VoidPaymentAction` there. *Why:* a payment recorded on the wrong
subscription is found in its file first. *Cost:* the statement's hook takes the ability, three desk files and
the customer page. *Recommend:* take it (§14.5); otherwise the void is the ledger's only.

**S11 — an extension that covers nothing is not offered.** The preview's `subscriptions` 0 → the dialog says
«لم يشمل هذا الإغلاق أي اشتراك، فلا شيء يُمدَّد.» with «رجوع» only. *Why:* the API would mark the closure
extended for nothing, and the closure could then never be extended once subscriptions are corrected. *Cost:*
none. *Recommend:* take it.

**S12 — every announcements write invalidates the whole space** (`['space', spaceId]`). *Why:* a closure written,
ended, started or deleted changes the space's state now (`occupancy`'s, the desk's top bar), and an extension
moves subscriptions' ends (`desk`'s file, statement and lists): the same reason `desk`'s writes do (architecture
§7). *Cost:* §7 gains «`announcements`' writes too (a closure changes the state now and an extension the
subscriptions) ({date}, #PRNUM)». *Recommend:* take it.

**S13 — the hearts read the saved ids from the directory's favourites; the writes are `favorites'`, which
invalidate `['me']`.** The heart flips at once (optimistic, architecture §7: "only for favourites"), held by the
heart's hook while the write is pending, then the `['me']` refetch is the truth; a failure flips it back. *Why:*
the only read that knows a favourite is `GET /me/favorites`, the directory's; a whole-scope invalidation is
§7's existing exception for a write whose screen shows another capability's view. *Cost:* one extra request
per signed-in visit to a page with cards (≤ 200 cards), none for a guest; §7 gains the favourites' line.
*Recommend:* take it.

**S14 — the guest's intent lives in memory, never in the address.** The heart and the report, pressed by a
guest, hold `{ spaceId, name }` / `{ slug }` in their feature's module store (as `directory`'s near-me store),
then open the sign-in prompt; the site's navigation to sign-in, register or Google keeps the page alive, and
once a session is established the held action runs once and is cleared: the favourite is saved and said
(«حُفظت {name} في المفضّلة»), the report dialog opens. *Why:* a link carrying `?save=1` would let a crafted link
write for a signed-in user; memory lets nothing outside the app start an action. *Cost:* a reload or a password
recovery by email loses the intent (AU-UX-001; finding 168): the user presses again. *Recommend:* take it.

**S15 — the report's repository reads the answer's status** (`apiClient.post` + `unwrap`, the "rare call"
architecture §7 allows): 201 a new report, 200 the open one answering a repeat, so the toast says which.
*Recommend:* take it.

**S16 — the capability documents:** `payments.md`, `announcements.md`, `data-reports.md`, `favorites.md` each gain
their *Web* parts (scope, *Who uses it*, *Behaviour* on the web, *Web decisions*, code map *Web*, *Web history*)
— each written at its first PR's stable core; `directory.md` gains the favourites list, the slots and the page's
announcements; `desk.md` the void; `subscriptions.md`, `space-links.md`, `users.md` one *Who uses it* line each;
architecture §2 (*Built so far*), §3 (S2), §7 (S12, S13); `overview.md`'s *Built* lines; foundation §12
(`FilterTag`), the findings. Finding 98 (size) watched: `directory.md` grows ≈ 300 words. *Recommend:* take it.

**No rule is weakened** except architecture §3's naming rule, extended by S2 with its reason (owner's approval).

### Proposed alternatives (none applied)

- **A1 — PR 4 split in two (recommended, §14.2):** PR 4 counts ≈ 105 files (two new account pages and their
  layout, the account menu, two features new or grown on the site, the directory's slots in four components,
  a layer icon). **PR 4a** = commits 1–2 («بلاغاتي» and the report, ≈ 41); **PR 4b** = commits 3–6 (the heart,
  «المفضّلة», the page's announcements, ≈ 64), cut from `main` once 4a merges. *Cost:* a fifth PR, its CI and its
  review. PR 1 (≈ 83) and PR 2 (≈ 73) stay whole: each is one capability (a split of PR 1 would leave «دفعاتي اليوم»
  without its void's struck rows to show).
- **A2 — the reporter's side in PR 3** (the dialog and «بلاغاتي» with the owner's and the admin's lists): PR 3's
  real run would then make its reports through the app. Not taken: PR 3 would touch `pages/site` (the public fix
  PR's ground, decision 3) and reach ≈ 90 files; §14.9 makes PR 3's reports by a named script instead.
- **A3 — `favorites` reads `GET /me/favorites` itself** (the ids and the account's list), drawing the
  directory's cards through a slot. Not taken: it calls the directory's route (S1).
- **A4 — P3's grouped navigation in PR 1** (one shell commit: `SPACE_NAV` and `ADMIN_NAV` gain their group, the
  sidebar draws `SidebarGroup`s with their labels, hidden on the rail): it touches every dashboard page's shell
  and finding 87's slow test. Not taken here; finding 165 records it for an item of its own.
- **A5 — the ledger opens on this month** (the prototype's sample range) rather than today. Not taken: today is
  the API's default and the owner's daily question; a month is two taps on the range.
- **A6 — the reports' status as `Tabs` with counts** (R2-OW-VD-002): no route counts reports by status. Not taken.
- **A7 — «المفضّلة» without near me** (R2-AU-EX-002): changes AC-014, settled. Not taken.
- **A8 — a handled-by filter on the admin's reports** (R2-AD-UX-003): needs `verified` on `GET
  /admin/data-reports` (worker B, S). Not taken here; finding 167.
- **A9 — undo of an announcement's delete:** needs a restore route. Not taken; the delete asks first (P9).
- **A10 — the report sheet's «القيمة الحالية في صفحة المساحة»:** a second formatter of each fact group (prices,
  hours, contacts, location, amenities) beside the directory's and the editor's. Not taken; «تعديل الحقل» leads
  to the field (DI-33).
- **A11 — a report's details always required** (the prototype): the contract requires them for «أخرى» only, one
  owner of the rule. Not taken (DI-44).
- **A12 — the void in `payments`** (the list and its action in one feature): the void route is the desk
  module's (S1). Not taken.

## 6. Related findings

| Finding | Folded? | Why · cost |
|---|---|---|
| 8 the applied-filter tag has no component | **Yes, PR 3 commit 1** (decision 4) | `FilterTag`, used by the admin's reports (DI-40); resolved there. S |
| 131 the space page cannot show a closure's notice | **Yes, PR 4** (4b commit 6) | the API carries the announcements since #112; resolved there. S |
| 162 no route names a space's staff to reception | Evidence line, PR 1 | «دفعاتي اليوم» names who voided reception's own payment (`PaymentRow.voided.by`); the statement still names neither; stays Open |
| 150 the owner sees a report's exact time | Evidence line, PR 3 (stays Accepted) | the owner's screen shows the day only, never the time (DI-34) |
| 164 a written-off visit is listed nowhere | Evidence line, PR 1 | the void of its payment is refused until the write-off is undone, whose undo is only in its toast (S4's line) |
| 171 a published price changed between the read and the subscribe | No | the desk's; untouched |
| 105 a held menu item may be unreachable | No (avoided) | no menu here holds a disabled item: an unavailable action is left out and its reason is said on the card (DI-16) |
| 132 a paged list shows no sign of the next page | No | the lists keep `keepPreviousData` and `aria-busy`, as every list |
| 87 the owner's shell cold-loads `space-links` | No | the known exception (§13); PR 3 adds `AdminSpaceFilter` to `space-links`' index: its routes test time recorded |
| 101 the end sheet is not full width on a phone | Resolved by #124 | the announcement and decision sheets are full width below 768 px |
| 98 the capability documents outgrow their guide | No | watched (S16) |
| 138 a failed refresh keeps a live status | No | the public fix PR's |
| **New 165** the dashboard's navigation is not grouped by task (P3) | Recorded, PR 1 | A4 |
| **New 166** the ledger's staff filter cannot name a space's other owners | Recorded, PR 1 | no route names a space's owners to an owner; their payments show their name in the rows |
| **New 167** the admin's reports cannot be filtered by who handles them | Recorded, PR 3 | A8 |
| **New 168** a guest's intent does not survive a password recovery | Recorded, PR 4 (commit 2; the heart's line added in commit 4) | S14's cost (AU-UX-001) |
| *(conditional)* the next free number | Recorded only if §13 check 5.k finds `data-table` in a site page's chunk | the space page or «بلاغاتي» downloading the table's library |

## 7. Design issues (built only once the reply approves them)

Each: the mistake, where it is proven, the fix from the layer's components and tokens. **⟨report · issue⟩** marks
a point a round-2 report proves, which the web must not copy.

### PR 1 — payments
1. **«تصدير CSV» on Payments** exports the page's rows, not the ledger, and CSV is Finance's (OW-015, step 11's
   "charts and CSV exports"). *Fix:* not built; no dead control.
2. **The period is invisible on a phone** ⟨R2-OW-DF · DF-008⟩: the range hides in the sheet, the count skips it,
   the totals name no period. *Fix:* the sheet's count counts a range when one is set; the totals line starts with
   the period («اليوم · …», «21 أكتوبر · …», «1 – 21 أكتوبر 2026 · …»).
3. **Filtered to nothing, no way back on wide screens** ⟨R2-OW-UX · UX-001⟩, and the prototype's clear left the
   range and the voided chip. *Fix:* «مسح الفلاتر» (`Button variant="link"`) beside the chip row at every width
   while any filter applies, resetting the range, staff, method, kind and the chip; the no-match empty state
   offers the same.
4. **The staff filter's options are hard-coded** ⟨R2-OW-UX · UX-006⟩. *Fix:* the owner («{name} (أنت)») and the
   space's reception accounts from `staff`, a deactivated one marked «· موقوف»; a space's other owners cannot
   be named (finding 166).
5. **The list's state is lost on reload** ⟨R2-OW-UX · UX-008⟩. *Fix:* every filter and the page in the address
   (S8).
6. **A voided amount is told by a strike alone** ⟨R2-DK-AX · AX-017⟩. *Fix:* struck through, a visible «ملغاة»
   `Badge neutral`, and «ألغاها {name}: {reason}» on one line (CP-009); hidden by default behind «إظهار الملغاة»
   (the prototype's), never counted as received; the totals say the voided ones apart.
7. **The void's dialog** (P9, DK-016): *Fix:* an `AlertDialog`, the action `destructive` «إلغاء الدفعة»,
   «رجوع»; the title «إلغاء الدفعة؟»; the body names the amount, who, the day and the method and the true
   consequence «تبقى ظاهرة مشطوبة مع السبب واسمك، ولا تُحسب في الدخل ولا في التسليم. لا يمكن التراجع.»; the
   reason required (1–200), focused first; a failure inside it, the reason kept.
8. **The focus is lost after the void** ⟨R2-DK-AX · AX-010⟩, and the row may leave the list (voided ones hidden).
   *Fix:* the focus returns to the row's «⋯»; once the row leaves, to the next row's «⋯», else the totals line
   (`tabIndex={-1}`).
9. **The «⋯» says whose** ⟨R2-DK-AX · AX-016⟩. *Fix:* «إجراءات الدفعة: {amount} · {who}» on the trigger; the item
   «إلغاء الدفعة…» destructive, its consequence said in the dialog it opens.
10. **«دفعاتي اليوم»'s phone card drops the transfer's helper** ⟨R2-DK-VD · VD-012⟩. *Fix:* «وصلت إلى حساب
    المساحة» under the transfer row too.
11. **The handover's figures summed in the browser** (the prototype's `sum`) would be false past one page. *Fix:*
    every figure from `meta.totals` (DESK_SCREENS S7 kept: agorot end to end, every figure the server's); the cash
    first («نقدًا للتسليم»).
12. **A voided payment of a written-off visit** cannot be voided until the write-off is undone (the ledger's
    fourth rule), whose undo lives only in its toast (finding 164). *Fix:* the refusal says so: «لا تُلغى دفعة
    زيارة شُطب مبلغها.»
13. **The customer's name in a row** links to the file (the prototype). *Fix:* a `Link` to
    `spaceCustomerPath` (the page's prop) when the payment has a customer; a visit with none shows the
    visitor's name as text, «زائر» with none.
14. **A statement's payment has no void** (the prototype's file had one). *Fix:* S10.

### PR 2 — announcements
15. **Every row repeats the tab as a status badge** ⟨R2-OW-EX · EX-008⟩. *Fix:* no status badge; the type badge
    only (`warning` for an outage or a closure, `neutral` otherwise, OW-014).
16. **Ended announcements open an editable sheet from «عرض»** ⟨R2-OW-EX · EX-009⟩. *Fix:* no «عرض»/«تعديل» on an
    ended one; the card is the view. An action that cannot apply is left out, its reason said on the card (no
    disabled menu item, finding 105).
17. **The actions by state** (O10: end now, delete, start now, no end; the prototype lacks «ابدأ الآن»).
    *Fix:* running — «تعديل», «إنهاء الآن» (with «تراجع» in its toast, restoring the old end; not for an
    extended closure, whose end may only come earlier), «⋯» «حذف…»; upcoming — «تعديل», «ابدأ الآن», «⋯» «حذف…»;
    ended — «⋯» «حذف…». An extended closure has no «حذف…»: its line says «مُدّدت اشتراكاته، فلا يُحذف ولا تُؤخَّر
    نهايته.»
18. **The delete names nothing and says a false consequence** ⟨R2-OW-DF · DF-012⟩. *Fix:* «حذف إعلان «{type} ·
    {period}»؟» and the consequence by state: running closure «يختفي من صفحة المساحة، وتعود حالتها تلقائية
    فورًا.»; running other «يختفي من صفحة المساحة فورًا.»; upcoming «لن يظهر للزوار.»; ended «يُحذف من القائمة.»
    — each «لا يمكن استرجاعه.»; destructive «حذف».
19. **A failed extension closes its dialog** ⟨R2-OW-DF · DF-003⟩. *Fix:* the failure inside it
    (`FormFailure`), the days kept, the same key on retry.
20. **O11's «المشتركين النشطين»** is not what moves: the extension covers every subscription running on any of
    the closure's days (decision 4, #123). *Fix:* «تمديد الاشتراكات التي شملها الإغلاق؟» / «شمل الإغلاق
    {count}.»; the count and the days from the preview; the days field prefilled with `proposedDays`, its
    helper «أيام الإغلاق: {proposed} ({first} – {last})».
21. **The sheet opens with an invisible focus** ⟨R2-OW-AX · AX-009⟩. *Fix:* the sheet's first focus is the checked
    type's radio (Radix's roving focus on the checked item), with the layer's ring.
22. **The date and time overflow the phone's sheet** ⟨R2-OW-DF · DF-001⟩ and the date is cut at 1440 ⟨DF-013⟩.
    *Fix:* date over time below 640 px (`grid gap-3 sm:grid-cols-2`); the date's trigger with the short month and
    the year («29 سبتمبر 2026» → `month: 'short'`).
23. **No loading state** ⟨R2-OW-DF · DF-010; R2-OW-AX · AX-001⟩. *Fix:* three `Skeleton` cards, the tabs' counts
    as skeletons, the list `aria-busy`.
24. **Acted-on items vanish from the tab** ⟨R2-OW-UX · UX-002⟩. *Fix:* each toast names the tab it went to
    («في «منتهية»») with an action «عرض» that opens that tab (the end now's toast keeps «تراجع» as its action and
    names the tab in its description).
25. **The preview's surface** ⟨R2-OW-VD · VD-005⟩. *Fix:* `rounded-lg bg-muted p-3`, drawing the public page's own
    item and notice (the same components PR 4 sets on the page).
26. **One pagination row on one page** ⟨R2-OW-EX · EX-007⟩. *Fix:* the pages show only past one page (the tab
    already counts).
27. **An English text missing in English:** the Arabic text shows, marked `lang="ar" dir="rtl"`.
28. **Reception and the extension:** a started closure, not extended, reads «يمدّد المالك الاشتراكات بعد بدء
    الإغلاق.» for reception; an upcoming one «يمكن تمديد الاشتراكات بعد أن يبدأ الإغلاق.» for the owner.
29. **A closure's consequence in the sheet:** «تظهر المساحة «مغلق الآن» للزوار طوال هذه الفترة، ويُنبَّه
    الاستقبال عند تسجيل الحضور.» (`Alert variant="warning"`), true since #112's warning.
30. **A start in the past** (a closure posted late) is allowed up to 30 days: the server's `out_of_range` on
    `startsAt` says «البداية بين 30 يومًا مضت و365 يومًا قادمة.»; on `endsAt` «النهاية بعد الآن، وخلال 365 يومًا
    من البداية.»

### PR 3 — data reports
31. **The status chips promise three statuses the API cannot filter** (the owner's «جديد · تم التصحيح · لم
    يُعتمد»): `OPEN | DECIDED`. *Fix:* «الكل · جديدة · تمت المراجعة»; each row's badge says which decision
    (`info` «جديد», `success` «تم التصحيح», `neutral` «لم يُعتمد»).
32. **The admin's chips** the same (A7's chips kept), with the space and the field as fields (P5).
33. **«القيمة الحالية في صفحة المساحة»** has no source on the owner's or the admin's report reads; it would be a
    second formatter of five fact groups (A10). *Fix:* not built; «تعديل الحقل» (outline, `ArrowEndIcon`) leads to
    the field's page: the owner's prices → «الباقات والأسعار», the rest → «ملف المساحة»; the admin's → the space's
    editor.
34. **The owner sees when a report was made** (finding 150, accepted). *Fix:* the day only («21 أكتوبر»), never the
    time; the reporter «زائر» (O12).
35. **A report with no details** (any field but «أخرى»). *Fix:* «لم يكتب المُبلِّغ تفاصيل.» in muted text.
36. **«لم يُعتمد»'s reply is required only on submit** ⟨R2-AD-DF · DF-018⟩. *Fix:* the reply's helper says it
    first: «يظهر لصاحب البلاغ. مطلوب لـ«لم يُعتمد»، واختياري لـ«تم التصحيح».»; a missing one focuses the field
    with «اكتب السبب؛ هو ما سيقرؤه صاحب البلاغ.»
37. **A decided report reopened shows its buttons again.** *Fix:* read-only: its decision badge, «الردّ: …» or
    «بلا ردّ», no buttons.
38. **A verified space's report is a dead end for the admin** ⟨R2-AD-UX · UX-002⟩. *Fix:* `Alert variant="info"`
    «مساحة موثّقة — يقرّر مالكها هذا البلاغ. للاطلاع فقط.» and «عرض المساحة» (outline link to the admin's
    editor of that space).
39. **«يعالجه»** per row (the prototype's) from `space.verified`: `info` «الإدارة» / `neutral` «المالك». No filter
    (finding 167).
40. **Filters in force are invisible** (a `?space=` link, the phone's sheet) ⟨R2-PU-UX · UX-006's pattern; finding
    8⟩. *Fix:* the admin's space and field in force as `FilterTag`s under the toolbar at every width («المساحة:
    {name}», «الحقل: {field}», each «إزالة فلتر …»), beside «مسح الفلاتر».
41. **The decided report vanishes from «جديدة»** ⟨R2-OW-UX · UX-002⟩. *Fix:* the toast «عُلّم «تم التصحيح»» /
    «عُلّم «لم يُعتمد»» says «في «تمت المراجعة»» with «عرض»; «أُرسل الردّ لصاحب البلاغ.» when a reply was written.
42. **Filtered to nothing** ⟨R2-AD-UX · UX-005⟩. *Fix:* «لا توجد بلاغات تطابق الفلاتر» with «عرض الكل».
43. **Admin's lists switch to cards at 768** (A7). *Fix:* the admin's table `cardsBelow="lg"` (eight columns); the
    owner's five columns from 768 px.

### PR 4 — the user's side
44. **The details are required always** (the prototype) though the contract requires them for «أخرى» only. *Fix:*
    «التفاصيل» marked «اختياري» except for «أخرى», whose missing message says «اكتب ما الخطأ في «أخرى».»
45. **The dialog opens with a fragment** ⟨R2-PU-CP · CP-010⟩. *Fix:* verified «بلاغك عن {name} يصل إلى إدارة
    المساحة، وتجد ردّها في «بلاغاتي».»; unverified «بلاغك عن {name} يراجعه فريقنا، وتجد الردّ في «بلاغاتي».»
    («فريقنا», as the page's notice, directory DI-26).
46. **The submit assumes success** ⟨R2-PU-UX · UX-002⟩. *Fix:* the dialog stays on a refusal or no answer, the input
    kept, its failure an `Alert` with `role="alert"`; 429 counts down.
47. **The toast drops where the reply lands** ⟨R2-PU-CP · CP-011; R2-PU-UX · UX-003⟩. *Fix:* «أرسلنا بلاغك إلى
    إدارة المساحة. ستجد ردّها في «بلاغاتي».» / «… إلى فريقنا. ستجد الردّ في «بلاغاتي».» with «عرض بلاغاتي».
48. **A repeat files nothing** (200, the open one). *Fix:* «أرسلت بلاغًا عن هذا من قبل، وما زال قيد المراجعة.»
    with «عرض بلاغاتي».
49. **The page's heart skips the undo** ⟨R2-PU-UX · UX-004⟩ **and assumes success** ⟨UX-002⟩. *Fix:* one hook for
    every heart: the toast «أُضيفت إلى المفضّلة» / «أُزيلت من المفضّلة» naming the space, with «تراجع»; a failure
    flips it back with «تعذّر حفظ {name} في المفضّلة» / «تعذّرت إزالة …» and «إعادة المحاولة».
50. **«المفضلة» / «المفضّلة»** ⟨R2-PU-CP · CP-019⟩. *Fix:* «المفضّلة» everywhere.
51. **The heart under 44 px on touch** ⟨R2-AU-AX · AX-002⟩. *Fix:* `Button size="icon"` (the layer's 44 × 44 hit
    area on a coarse pointer, AD-030), checked in the real run.
52. **The unlisted rows' rhythm and focus** ⟨R2-AU-VD · VD-005; R2-AU-AX · AX-007⟩. *Fix:* `gap-4` throughout;
    after «إزالة», the focus goes to the next row's «إزالة», else the next card's heart, else the count line.
53. **«بلاغاتي»'s two empty lines** ⟨R2-AU-CP · CP-005⟩ **and the error icon** ⟨R2-AU-VD · VD-006⟩. *Fix:* «لم ترسل أي
    بلاغ بعد» (+ «إذا رأيت معلومة خاطئة في صفحة مساحة، أبلغنا منها.» and «تصفّح المساحات») with no filter;
    «لا توجد بلاغات هنا» with one; `FlagIcon`.
54. **The message's toggle appears only after measuring** ⟨R2-AU-AX · AX-005⟩. *Fix:* a message over 160 characters
    is clamped to two lines with «عرض المزيد» / «عرض أقل» (`aria-expanded`, `aria-controls`), decided from its
    length, never measured.
55. **The report tabs keep the old page** ⟨R2-AU-UX · UX-007⟩. *Fix:* a filter change returns to page 1 (S8).
56. **The reply's label:** `repliedBy` `SPACE` «ردّ إدارة المساحة», `MASAHA` «ردّ فريقنا» (foundation §13 screen 11
    says «ردّ فريق مساحة», which reads as the space's team — PU-CP-005; §14.8 proposes its line).
57. **The account's navigation is not announced** ⟨R2-AU-AX · AX-006⟩. *Fix:* `nav` named «حسابي» (visible from
    1024 px, visually hidden below it, never `display: none`), its links `aria-current="page"`.
58. **A space that left** (C7). *Fix:* «بلاغاتي»: its name as text and «لم تعد هذه المساحة معروضة في الدليل»;
    «المفضّلة»: a muted card with the same line and «إزالة» (with «تراجع»).
59. **A running closure repeated** in the notice and the section. *Fix:* the notice at the top (U8: «the closure
    Alert stays at the top»), `Alert variant="warning"`, its text and «إعلان من إدارة المساحة · {period}»; the
    section lists the others (upcoming ones, a closure among them).
60. **The guest's prompt** (C4): *Fix:* a `Dialog` — the heart: «سجّل الدخول لحفظ المساحات في المفضّلة» / «تجد
    المساحات التي تحفظها في حسابك على أي جهاز.»; the report: «سجّل الدخول للإبلاغ عن معلومة» / «لتجد الردّ على
    بلاغك في «بلاغاتي».»; «إنشاء حساب» (outline) and «تسجيل الدخول» (primary), each carrying the page as `next`.
61. **The intent on return** (C4): the favourite saved and said «حُفظت {name} في المفضّلة» (a failure says so with
    «إعادة المحاولة»); the report dialog open.

**Not built, the reports' own improvements:** A5 (the month), A6 (VD-002), A7 (AU-EX-002), A8 (AD-UX-003), A10,
A11; AU-EX-003 (the badge and the chips both kept: a chip filters, a badge reads), AU-EX-004 (one card for a space
that left: C7 keeps its own form). **Not applicable here:** R2-OW-VD-001 (the shell's title size — the shell's
item), R2-AD-UX-011 (the editor), R2-OW-EX-005 (Staff's column), R2-DK-EX-005 (the handover recap: our figures
are the server's), R2-DK-VD-001 (the file's payments are the statement's since DI-43).

## 8. The files

A: added · M: modified · R: moved. Every test sits beside its file. The counts are estimates; `git diff --stat`
decides (no stop for the count: it is reported).

### PR 1 — `feat/payments`
- **Commit 1** `shared/lib/time/` — R `features/desk/services/dayText.ts` → `shared/lib/time/dayText.ts`, R
  `dayWord.ts` the same, each with its unit test; M `shared/lib/index.ts`; M every `features/desk` file that
  imports them (`git grep -l "services/day\(Text\|Word\)" apps/web/src/features/desk` — about eight). Docs:
  `desk.md` code map (a row's day and a date leave its services). (≈ 14)
- **Commit 2** `features/desk/` — M `repository/deskRepository.ts` (+ its unit test); A `types/VoidTarget.ts`;
  A `hooks/void/useVoidPayment.ts`, `hooks/void/useVoidDialog.ts` (+ test); A `components/void/VoidDialog.tsx`
  (+ test), `components/void/VoidPaymentAction.tsx` (+ test); M `types/DeskAbilities.ts` (`void`), M
  `hooks/statement/useStatement.ts` (+ its test), `components/statement/Statement.tsx` (+ its test), M
  `components/file/SubscriptionCard.tsx`, `components/file/CustomerFile.tsx`, M `components/toast/deskToasts.tsx`,
  M `index.ts`. `pages/dashboard/space/customers/CustomerPage.tsx` M (the owner's `void`). Copy
  `{english,arabic}/desk.ts` M. Docs `desk.md`, `payments.md` (*Who uses it*). (≈ 22)
- **Commit 3** `features/payments/` (new) — A `index.ts`; `repository/paymentsRepository.ts` (+ unit);
  `hooks/queryKeys.ts`; `hooks/ledger/useLedgerFilters.ts` (+ test), `hooks/ledger/useLedger.ts` (+ test),
  `hooks/useFocusAfterLeave.ts` (+ test); `services/ledgerQueryOf.ts` (+ unit), `services/periodText.ts` (+ unit),
  `services/paymentRowView.ts` (+ unit); `types/PaymentRowView.ts`, `types/LedgerPerson.ts`;
  `components/ledger/PaymentsLedger.tsx` (+ test), `components/ledger/LedgerFilters.tsx`,
  `components/ledger/LedgerTotals.tsx`, `components/PaymentAmount.tsx`. `features/staff/` — A
  `hooks/people/useStaffPeople.ts` (+ test); M `index.ts`. `pages/dashboard/` — A
  `space/payments/PaymentsPage.tsx`; M `routes.tsx`, `routes.component.test.tsx`. Copy
  `{english,arabic}/payments.ts` A, `index.ts` M ×2. Docs `payments.md`, `space-links.md` (staff: one line),
  `architecture.md` §2, `overview.md`; findings 165, 166 A, findings `README.md` M. (≈ 34)
- **Commit 4** `features/payments/` — A `hooks/mine/useMyPaymentsToday.ts` (+ test);
  `components/mine/MyPaymentsToday.tsx` (+ test), `components/mine/HandoverFigures.tsx`; M
  `repository/paymentsRepository.ts` (+ unit, no change of call: the same list) only if its type widens, M
  `hooks/queryKeys.ts`, `index.ts`. `pages/dashboard/space/payments/MyPaymentsPage.tsx` A; M `routes.tsx`,
  routes test. Copy ×2. Docs `payments.md`; finding 162 M (evidence). (≈ 13)

### PR 2 — `feat/announcements`
- **Commit 1** `features/announcements/` (new) — A `index.ts`; `repository/announcementsRepository.ts`
  (+ unit); `hooks/queryKeys.ts`; `hooks/list/useAnnouncementsFilters.ts` (+ test), `hooks/list/useAnnouncementsList.ts`
  (+ test); `services/periodText.ts` (+ unit), `services/typeView.ts` (+ unit), `services/textOf.ts` (+ unit),
  `services/announcementsQueryOf.ts` (+ unit); `types/AnnouncementCardView.ts`; `components/list/AnnouncementsList.tsx`
  (+ test), `components/list/AnnouncementCard.tsx`, `components/list/ClosureLine.tsx`. `pages/dashboard/` — A
  `space/announcements/AnnouncementsPage.tsx`; M `routes.tsx`, routes test. Copy `{english,arabic}/announcements.ts`
  A, `index.ts` ×2. Docs `announcements.md`, `subscriptions.md` (one line), `architecture.md` §2, §3 (S2),
  `overview.md`. (≈ 28)
- **Commit 2** `features/announcements/` — M repository (+ unit); A `hooks/sheet/useAnnouncementSheet.ts`
  (+ test), `hooks/sheet/useCreateAnnouncement.ts`, `hooks/sheet/useEditAnnouncement.ts`;
  `services/sheetRequest.ts` (+ unit); `types/SheetValues.ts`; `components/sheet/AnnouncementSheet.tsx` (+ test),
  `components/sheet/PeriodFields.tsx`, `components/sheet/TypeChoice.tsx`; `components/public/AnnouncementItem.tsx`,
  `components/public/ClosureNotice.tsx`; M `AnnouncementsList.tsx`, `AnnouncementCard.tsx`,
  `useAnnouncementsList.ts`; A `hooks/useAnnouncementsWrite.ts` (the shared invalidation, S12). Copy ×2. Docs
  `announcements.md`, `architecture.md` §7 (S12). (≈ 18)
- **Commit 3** `features/announcements/` — M repository (+ unit); A `hooks/actions/useEndNow.ts`,
  `useStartNow.ts`, `useDeleteAnnouncement.ts`, `useAnnouncementActions.ts` (+ test), `useDeleteDialog.ts` (+ test);
  `components/actions/AnnouncementMenu.tsx` (+ test), `components/actions/DeleteDialog.tsx`;
  `components/toast/announcementToasts.tsx`; M `AnnouncementCard.tsx`, `useAnnouncementsList.ts` (the focus after
  a card leaves). Copy ×2. Docs `announcements.md`. (≈ 14)
- **Commit 4** `features/announcements/` — M repository (+ unit); A `hooks/extension/useExtensionPreviewQuery.ts`,
  `useExtendSubscriptions.ts`, `useExtensionDialog.ts` (+ test); `components/extension/ExtensionDialog.tsx`
  (+ test); M `AnnouncementCard.tsx`, `ClosureLine.tsx`, `useAnnouncementsList.ts` (+ test). Copy ×2. Docs
  `announcements.md`, `subscriptions.md` (*Who uses it*: the screen's extension), `foundation.md` §13 screen 18's
  line (§14.8). (≈ 13)

### PR 3 — `feat/data-reports`
- **Commit 1** `shared/design-system/` — A `components/display/FilterTag/FilterTag.tsx`, `index.ts`,
  `FilterTag.component.test.tsx`; M the layer's `index.ts`; `pages/showcase/sections/display/FilterTagSection.tsx`
  A, `pages/showcase/registry.tsx` M; `pages/showcase/fixtures.json` M only if the section reads its words there.
  Docs `foundation.md` §12; finding 8 → Resolved, findings `README.md` M. (≈ 9)
- **Commit 2** `features/data-reports/` (new) — A `index.ts`; `repository/dataReportsRepository.ts` (+ unit);
  `hooks/queryKeys.ts`; `hooks/space/useSpaceReportsFilters.ts` (+ test), `hooks/space/useSpaceReports.ts` (+ test);
  `hooks/decide/useDecideSheet.ts` (+ test), `hooks/decide/useDecideReport.ts`; `services/reportView.ts` (+ unit),
  `services/reportsQueryOf.ts` (+ unit); `types/ReportRowView.ts`, `types/DecideTarget.ts`;
  `components/space/SpaceReportsList.tsx` (+ test), `components/decide/DecideSheet.tsx` (+ test),
  `components/StatusChips.tsx`. `pages/dashboard/` — A `space/reports/DataReportsPage.tsx`; M `routes.tsx`,
  routes test. Copy `{english,arabic}/dataReports.ts` A, `index.ts` ×2. Docs `data-reports.md`,
  `architecture.md` §2, `overview.md`; finding 150 M (evidence). (≈ 30)
- **Commit 3** `features/data-reports/` — M repository (+ unit), keys; A `hooks/admin/useAdminReportsFilters.ts`
  (+ test), `hooks/admin/useAdminReports.ts` (+ test); `services/adminReportsQueryOf.ts` (+ unit);
  `components/admin/AdminReportsList.tsx` (+ test), `components/admin/AdminReportFilters.tsx`,
  `components/admin/FilterTags.tsx`; M `DecideSheet.tsx`, `useDecideSheet.ts` (+ test: the admin's), `index.ts`.
  `features/space-links/` — A `components/admin-filter/AdminSpaceFilter.tsx` (+ test); M `index.ts`.
  `pages/dashboard/` — A `admin/DataReportsPage.tsx`; M `routes.tsx`, routes test. Copy ×2 (`dataReports`,
  `spaceLinks`). Docs `data-reports.md`, `space-links.md` (*Who uses it*: one line); finding 167 A, `README.md`.
  (≈ 20)

### PR 4 — with A1: 4a `feat/report-wrong-info` = commits 1–2; 4b `feat/favorites` = commits 3–6
- **Commit 1** `features/data-reports/` — M repository (+ unit), keys; A `hooks/mine/useMyReports.ts` (+ test),
  `hooks/mine/useMyReportsFilters.ts`; `components/mine/MyReportsList.tsx` (+ test), `components/mine/MyReportCard.tsx`;
  M `index.ts`. `pages/site/` — A `account/AccountLayout.tsx` (+ test), `account/MyReportsPage.tsx`; M
  `routes.tsx`, `navigation.ts`, `shell/SiteHeader.tsx`, `shell/SiteMenu.tsx`. `features/users/` — M
  `components/AccountMenuContent.tsx`, `components/AccountMenuSection.tsx`, `components/AccountMenu.tsx`,
  `hooks/useAccount.ts` (+ their tests). `app/pageTitles.unit.test.ts` (its list of pages) M if it enumerates
  routes by hand. Copy ×2 (`dataReports`, `site`, `users`). Docs `data-reports.md`, `users.md`, `architecture.md`
  §2 (*AccountLayout* built), `overview.md`, `foundation.md` §13 screen 11's line (§14.8). (≈ 21)
- **Commit 2** `features/data-reports/` — M repository (+ unit: the report's 201 and 200); A
  `hooks/intent/reportIntent.ts` (+ unit), `hooks/report/useReport.ts`, `hooks/report/useReportDialog.ts` (+ test),
  `hooks/report/useReportAction.ts` (+ test); `components/report/ReportAction.tsx` (+ test),
  `components/report/ReportDialog.tsx`; M `index.ts`. `features/directory/` — M `components/page/SpaceDetails.tsx`
  (the `report` slot), `types/SpacePageView.ts` if the slot's space needs a field it lacks. `pages/site/` — A
  `public/SignInPrompt.tsx` (+ test), M `public/space/SpacePage.tsx` (+ its routes test or a new
  `SpacePage.component.test.tsx`). Copy ×2 (`dataReports`, `site`). Docs `data-reports.md`, `directory.md`
  (decision 4's line revised); finding 168 A, `README.md`. (≈ 20)
- **Commit 3** `shared/design-system/icons/` — M `iconSet.tsx`, `index.ts`, `Icon.component.test.tsx`; the
  layer's `index.ts` if it re-exports icons by name. Docs `foundation.md` (only if §12 or the icon list names
  them). (≈ 4)
- **Commit 4** `features/favorites/` (new) — A `index.ts`; `repository/favoritesRepository.ts` (+ unit);
  `hooks/intent/favoriteIntent.ts` (+ unit), `hooks/toggle/useFavoriteToggle.ts` (+ test),
  `hooks/resume/useResumeFavorite.ts` (+ test); `components/FavoriteButton.tsx` (+ test),
  `components/ResumeFavorite.tsx`; `components/toast/favoriteToasts.tsx`. `features/directory/` — M
  `repository/directoryRepository.ts` (+ unit), `hooks/queryKeys.ts`; A `hooks/favorites/useFavoriteIds.ts` (+ test);
  M `types/DirectorySlots.ts`, `components/card/SpaceCard.tsx` (+ its test), `components/list/DirectoryResults.tsx`,
  `components/DirectoryList.tsx`, `components/home/HomeSpaces.tsx`, `components/page/SpaceHeader.tsx`,
  `components/page/SpaceDetails.tsx`, `index.ts`. `pages/site/` — M `public/directory/DirectoryPage.tsx`,
  `public/home/HomePage.tsx`, `public/space/SpacePage.tsx`, `shell/SiteLayout.tsx`. Copy ×2 (`favorites` A,
  `index.ts` ×2). Docs `favorites.md`, `directory.md`, `architecture.md` §7 (S13). (≈ 34)
- **Commit 5** `features/directory/` — A `hooks/favorites/useFavoritesView.ts` (+ test),
  `components/favorites/FavoritesView.tsx` (+ test), `components/favorites/UnlistedFavorite.tsx`; M `index.ts`.
  `features/favorites/` — A `components/RemoveFavorite.tsx` (+ test); M `index.ts`. `pages/site/` — A
  `account/FavoritesPage.tsx`; M `routes.tsx`, `navigation.ts`, `account/AccountLayout.tsx`; the account menu's
  links gain «المفضّلة» (`SiteHeader`, `SiteMenu`). Copy ×2. Docs `directory.md`, `favorites.md`,
  `architecture.md` §2, `overview.md`. (≈ 14)
- **Commit 6** `features/announcements/` — A `components/public/SpaceAnnouncements.tsx` (+ test),
  `services/runningClosure.ts` (+ unit); M `components/public/ClosureNotice.tsx` (+ test), `index.ts`.
  `features/directory/` — M `components/page/SpaceDetails.tsx`, `hooks/page/useSpacePage.ts`,
  `types/SpacePageView.ts` (the page's announcements). `pages/site/public/space/SpacePage.tsx` M. Copy ×2. Docs
  `announcements.md`, `directory.md`, `overview.md`; finding 131 → Resolved, `README.md`. (≈ 12)

### Shared with the other items (workflow §9)
- **#124** (DESK_SCREENS PR 4): PR 1 starts after it merges; PR 1 then edits `features/desk` files #124 wrote
  (`Statement.tsx`, `useStatement.ts`, `CustomerFile.tsx`, `SubscriptionCard.tsx`, `deskToasts.tsx`, `index.ts`,
  `deskRepository.ts`) — read as #124 left them.
- **The public site's fix PR** (`0_CARRIED_FROM_111.md` + the owner's list): it touches `pages/site/public/home/*`,
  `public/about/*`, `public/space/SpacePage.tsx` (maybe), `shell/SiteLayout.tsx`, `shell/SiteFooter.tsx`,
  `features/directory` (`components/list/DirectoryResults.tsx` — the scroll after a page —, `components/page/Gallery.tsx`,
  `StatusPanel.tsx`, `hooks/home/useHomeSpaces.ts`, `components/home/HomeSpaces.tsx`, `components/search/DirectorySearch.tsx`),
  `shared/lists/components/ListPagination.tsx`, `shared/copy/*/site.ts`, `directory.ts`, and the documents
  `directory.md`, `overview.md`, `architecture.md`, the findings index and finding 87. **PR 4 touches** of these:
  `DirectoryResults.tsx`, `HomeSpaces.tsx`, `SpacePage.tsx`, `SiteLayout.tsx`, `SpaceDetails.tsx`, copy `site.ts`,
  `directory.ts`, and the same documents. Either order: a text conflict keeps both sides (the fix's change of a
  line, PR 4's added slot or prop); PR 1–3 touch none of its code files.
- **Worker B's FINANCE_AUDIT** (step 11's API: `apps/api`, `packages/shared`, the web's two `errors.ts`,
  documents): **no code file is shared** — this item touches no `apps/api`, no `packages/shared`, no
  `errors.ts`. Shared documents, each side its own part: `payments.md`, `subscriptions.md` (finding 151's fix,
  *API* parts), `announcements.md`, `overview.md` (*Built* lines), `architecture.md` (only if B adds a web
  line), the findings index (B's numbers apart), `api-contract.md` (not touched here). **If B's PR changes a type
  this item reads** (`PaymentRow`, `PaymentsMeta`, `PaymentsQuery`, `ManagedAnnouncement`, `ExtensionPreview`,
  `SpaceReport`, `AdminReport`, `MyReport`, `FavoriteSpace`) before a PR here is pushed → the executor adapts to
  it and records the decision (§13).

## 9. What is built — interfaces, words, states

Words: Arabic, then English. A counted line gives `arabicPlural` all six forms and `englishPlural` `one`/`other`
(`shared/copy/plural.ts`); every Arabic section `satisfies Catalogue['<section>']`. A value in a sentence is
isolated (`isolate`); a person's or a space's name may differ from the interface's language (`lineParts`, or the
`SpaceNameView`'s `lang`/`dir`). Amounts (`priceText`, LTR), times (`clockOf`, `HH:MM`, LTR) and dates on Gaza's
clock (S9). Lines already in the catalogue are reused by key, never copied: `errors.<code>` (every refusal code
named here has its line, `CLOSURE_EXTENDED`, `CLOSURE_ALREADY_EXTENDED`, `ANNOUNCEMENT_NOT_STARTED`,
`REPORT_ALREADY_DECIDED`, `FAVORITES_LIMIT_REACHED` included), `status.retry`, `desk.money.methods`,
`desk.refusals.forbidden`, `terms.liveStatuses`. **The owner approves every Arabic line below** (§14.7).

**Every dialog's and sheet's states** (DESK_SCREENS §10's, kept): open → its first field focused; sending → the
submit `loading` and `aria-disabled`, the fields `disabled`, Escape and the outside click held; refused → it
stays, every value kept, the failure (`FormFailure`, an `Alert` with `role="alert"`) above the footer, a field's
refusal on its field (the first focused); no answer (`network`, `timeout`) → its lost line (S4) and «إعادة
المحاولة»; 429 → the countdown (`useRefusalView`), the submit blocked until it ends; a 403 → S5's line; done →
closed, the toast from the answer. **Every list's states:** loading (skeletons: `DataTable loading`, three
`Skeleton` cards), failed (destructive `Alert` with the reference and «إعادة المحاولة»), failed again over shown
rows (a muted line «تعذّر التحديث؛ تظهر آخر قائمة.», reused from `occupancy.present.refreshFailed`, the rows
kept), empty and no match (each its own `EmptyState`), offline (`errors.network`, the same retry), the next page
loading (rows kept, `aria-busy`). **A dialog opened from a menu item** returns the focus to the menu's trigger
(kept by a ref, `onCloseAutoFocus` prevented — #122's and #124's lesson), else, the row gone, to the list's next
row or its heading.

### PR 1 · Commit 1 — `refactor(lib): share the day's words`
- `shared/lib/time/dayText.ts` (`dayText(date, language)`) and `shared/lib/time/dayWord.ts` (`dayWord(instant, now,
  language, words)`) — the same code, moved with their unit tests; `shared/lib/index.ts` exports both; every
  `features/desk` import of `../../services/dayText` / `dayWord` becomes `@shared/lib`. No words. Docs: `desk.md`'s
  code map (its services no longer hold "a row's day, a date"); nothing else (architecture §1 already names
  `shared/lib`'s date helpers).

### PR 1 · Commit 2 — `feat(desk): void a payment`
- **Repository:** `voidPayment(spaceId: number, paymentId: number, body: VoidPaymentRequest): Promise<PaymentRow>`
  — `api.post` to `/manage/spaces/{spaceId}/payments/{paymentId}/void`, no key (S4).
- **`types/VoidTarget.ts`:** `{ id: number; amountAgorot: number; method: 'CASH' | 'TRANSFER'; receivedAt: string;
  who: string }` — the payment a page or a statement offers; `who` already worded by the caller.
- **`useVoidPayment(spaceId, paymentId)`** — `useMutation<PaymentRow, AppError, VoidPaymentRequest>`; `onSuccess`
  → `settle(spaceId)`; `onError` → `linkEnded` (`useDeskWrite`).
- **`useVoidDialog({ spaceId, payment, onDone })`** → `{ title; text; reason: { label; field; error }; back;
  submit: { label; run; busy; blocked }; failure: FormFailureView | null }` — `useServerForm` over
  `voidPaymentSchema` (a blank reason is `required`); sent once; done → `toastVoided(payment)` and `onDone`;
  refused → `deskFailure(refusal, form.failure, { title: void.failed, lost: void.lost, nothing: void.nothing, … })`
  with `failureLines`: `VISIT_WRITTEN_OFF` → `void.refusals.VISIT_WRITTEN_OFF`, `not_found` → `void.refusals.not_found`
  (and `settle`), `forbidden` → `desk.refusals.forbidden` (and `['me']`).
- **`VoidDialog({ spaceId, payment, onClose, returnFocus })`** — an `AlertDialog` as `WriteOffDialog` (DI-7):
  the reason `Textarea` focused first, «رجوع» `AlertDialogCancel`, the submit `destructive`.
- **`VoidPaymentAction({ spaceId, payment, onGone })`** (exported) — a ghost `Button size="icon"` with
  `EllipsisVerticalIcon`, `aria-label` `void.menu({ amount, who })` (DI-9); a `DropdownMenu` whose content is
  labelled the same, its one item `variant="destructive"` «إلغاء الدفعة…»; the item opens `VoidDialog`; closed,
  the focus goes to the trigger while it is connected, else `onGone()` (DI-8).
- **`DeskAbilities`** gains `void: boolean` (the owner's). **The statement (S10):** `useStatement(spaceId,
  subscriptionId, { void: boolean })` — each payment row gains `void: VoidTarget | null` (the owner's, a payment
  not voided; `who` the statement's customer's name); `Statement` draws `VoidPaymentAction` at the row's end,
  `onGone` focusing the payments' `h4` (`tabIndex={-1}`); `SubscriptionCard`, `CustomerFile` pass the ability;
  `CustomerPage` sets `void: owner`.
- **`toastVoided`** (`deskToasts.tsx`): `toast.success(void.done({ amount, who }), { description: void.doneText })`,
  worded with `currentCopy()` when it lands.
- **Words** (`desk.void`):

| key | ar | en |
|---|---|---|
| `void.menu({amount, who})` / `.action` | إجراءات الدفعة: {amount} · {who} / إلغاء الدفعة… | Payment actions: {amount} · {who} / Void payment… |
| `void.title` / `.text({amount, who, day, method})` | إلغاء الدفعة؟ / {amount} · {who} · {day} · {method}. تبقى ظاهرة مشطوبة مع السبب واسمك، ولا تُحسب في الدخل ولا في التسليم. لا يمكن التراجع. | Void this payment? / {amount} · {who} · {day} · {method}. It stays visible, struck through, with the reason and your name, and counts in neither income nor the handover. It can’t be undone. |
| `void.reason` / `.reasonRequired` / `.confirm` / `.back` | السبب / اكتب سبب الإلغاء / إلغاء الدفعة / رجوع | Reason / Write why it is voided / Void payment / Back |
| `void.done({amount, who})` / `.doneText` | أُلغيت دفعة {amount} · {who} / لا تُحسب في الدخل ولا في التسليم. | {amount} from {who} voided / It counts in neither income nor the handover. |
| `void.failed` / `.nothing` / `.lost` | تعذّر إلغاء الدفعة / لم تُلغَ الدفعة. / لم يصل الرد. أعد المحاولة — إلغاؤها مرة ثانية لا يغيّر شيئًا. | We couldn’t void the payment / The payment wasn’t voided. / No answer came back. Try again — voiding it twice changes nothing. |
| `void.refusals.VISIT_WRITTEN_OFF` / `.not_found` | لا تُلغى دفعة زيارة شُطب مبلغها. / لم تعد هذه الدفعة موجودة. | A payment of a written-off visit can’t be voided. / This payment no longer exists. |

- **Docs:** `desk.md` — *What it does* (the web: the owner voids a payment from the ledger or a statement);
  *Behaviour* «**A payment's void on the web**» (DI-7, DI-8, DI-9, S10); *Web decisions*: «The void is the desk's
  on the web, set by the payments page in its rows (S1)», S10, DI-12 — each «{date}, #PRNUM»; code map; *Web
  history*. `payments.md` *Who uses it*: «On the web, the owner voids a payment from «الدفعات» and from a
  statement ([desk](desk.md))».

### PR 1 · Commit 3 — `feat(payments): list the space's payments`
- **Repository** (`createPaymentsRepository()`): `list(spaceId: number, query: PaymentsQuery): Promise<Page<PaymentRow[],
  PaymentsMeta>>` — `api.getPage<PaymentRow[], PaymentsMeta>('/manage/spaces/{id}/payments', { params: query })`
  (the desk's customers call's way of passing params, §13 check 5.b).
- **Keys** (`paymentsKeys`): `all(id) = ['space', id, 'payments']`, `list(id, query)`, `mine(id, page)` (commit 4).
- **`services/ledgerQueryOf.ts`** (pure, S8): `ledgerQueryOf(params: URLSearchParams): { filters: LedgerFilters;
  query: PaymentsQuery }`, `paramsOf(filters): URLSearchParams`; `LedgerFilters = { from?: string; to?: string;
  staff?: number; method?: 'CASH' | 'TRANSFER'; kind?: 'VISIT' | 'SUBSCRIPTION'; voided: boolean; page: number }`;
  each parameter read by the contract's rule for it (`dateSchema`, `PAYMENT_METHODS`, `PAYMENT_KINDS`, a positive
  id, the page); `from`/`to` kept only together, `to ≥ from`, `daysFrom(from, to) + 1 ≤ PAYMENTS_RANGE_MAX_DAYS`;
  the query `{ from?, to?, recordedById?, method?, kind?, voided: voided ? 'INCLUDE' : 'EXCLUDE', page, limit: 20 }`.
- **`services/periodText.ts`** (pure): `periodText({ from, to }, language, today, words): string` — none →
  «اليوم»; one day → «21 أكتوبر 2026»; a range → `Intl.DateTimeFormat#formatRange` (`day: 'numeric', month: 'long',
  year: 'numeric'`, `timeZone: 'UTC'` on the dates' UTC midnights) → «1 – 21 أكتوبر 2026».
- **`services/paymentRowView.ts`** (pure): `paymentRowView(row: PaymentRow, { language, now, words }):
  PaymentRowView` = `{ key: string; day: string /* dayWord */; time: string /* clockOf, Gaza */; who: string /* the
  customer's name, else the visitor's, else «زائر», isolated */; customerId: number | null; item: string /* «زيارة»
  or the subscription's name */; amount: string; method: string; recorder: string; voided: { label: string; line:
  string } | null; payment: { id; amountAgorot; method; receivedAt; who: string; voided: boolean } /* for the row's
  slot */ }`.
- **`useLedgerFilters()`** (the customers list's pattern) → `{ filters; query; choose: { range(from?: string, to?:
  string): void; staff(id?: number); method(m?); kind(k?); voided(on: boolean) }; rangeError: string | null /* over
  92 days: not written */; applied: number /* the range, staff, method, kind */; anyApplied: boolean /* + the chip
  */; clear(): void /* every one, the chip included (DI-3) */; searchOf(page): string; replacePage(page): void }`.
- **`useLedger(spaceId, { people: LedgerPerson[] })`**, `LedgerPerson = { id: number; name: string; self: boolean;
  active: boolean }` → `{ label; columns; wide: boolean /* useMediaQuery('(min-width: 768px)') */; state: 'loading'
  | 'failed' | 'emptyToday' | 'noMatch' | 'ready'; rows: PaymentRowView[]; busy; count: string; totals: { line:
  string /* period first (DI-2) */; voided: string | null } | null; toolbar: { range: { label; text; value;
  choose; error; calendar: { previous; next } }; staff: { label; value; options: { value: string; label: string
  }[]; choose }; method: { … }; kind: { … }; voided: { label; quick; on; toggle }; sheet: { title; applied: string;
  show: string /* «عرض {n} دفعة», «لا نتائج — غيّر الفلاتر» at none */; clear } ; clear: { label; run } | null };
  empty: { title; text; clear: { label; run } | null }; pagination; failure; refreshFailure; focus: { rowProps,
  totalsRef } }` — `keepPreviousData`; the totals from `meta.totals` only (S5's money rule: DESK_SCREENS S7);
  `focus` keeps the focus when the row holding it leaves (DI-8): the next row's action (`data-row-action`), else
  the totals line (`hooks/useFocusAfterLeave.ts`).
- **Components:** `PaymentsLedger({ spaceId, people, customerLink, rowAction })` (exported) — `DataTable`
  (`@shared/design-system/data`) `label` «سجل الدفعات»; columns: date (the day, the time under it, `dir="ltr"`),
  customer (a `Link` to `customerLink(id)` when a customer, the item under it), amount (`PaymentAmount`: the amount
  `text-label`, the method under it; voided: struck `line-through text-muted-foreground`, a `Badge neutral`
  «ملغاة», the line under it), recorder, actions (`rowAction(payment)`, in a `flex justify-end`); `renderCard`
  below 768 px: the name, «{day} · {time} · {item} · {method} · {recorder}», the amount block, the action; the
  toolbar: `LedgerFilters` — from 768 px a `grid gap-3 md:grid-cols-2 xl:grid-cols-4` of the range (`Field` +
  `DatePicker` + `Calendar mode="range" lang`), staff, method and kind (`Select`s); below 768 px a «الفلاتر»
  `Button variant="outline"` with a `Badge` of the count (its words read in place, the directory's DI-2), opening a
  bottom `Sheet` with the same fields, «عرض {n} دفعة» (`size="lg" w-full`) and «مسح الفلاتر» (ghost); then a row:
  the «إظهار الملغاة» `ToggleGroup type="multiple"` chip (`aria-label` «تصفية سريعة»), «مسح الفلاتر»
  (`variant="link"`) while any applies; `LedgerTotals` (`<p aria-live="polite" tabIndex={-1}>`).
- **`useStaffPeople(spaceId)`** (`features/staff`, exported) → `{ people: { id: number; name: string; active: boolean
  }[]; state: 'loading' | 'failed' | 'ready' }` on the staff list's own query (one cache); a failure leaves the
  ledger's staff options to the owner alone.
- **`PaymentsPage`** (`pages/dashboard/space/payments/`): `PageHeader` (no action: DI-1); `parseSpaceId`;
  `people` = the session's user (`self`) then `useStaffPeople`; `customerLink = (id) => spaceCustomerPath(spaceId,
  id)`; `rowAction = (payment) => payment.voided ? null : <VoidPaymentAction spaceId payment onGone={…} />`
  (`onGone` hands the focus to the ledger's keeper, which moves it); `key={spaceId}`. `SPACE_PAGES.payments`.
- **Words** (`payments`, new section):

| key | ar | en |
|---|---|---|
| `ledger.label` / `ledger.columns` | سجل الدفعات / date «التاريخ» · customer «الزبون» · amount «المبلغ» · recorder «سجّلها» · actions «إجراءات» | Payments ledger / Date · Customer · Amount · Recorded by · Actions |
| `ledger.visit` / `.noName` | زيارة / زائر | Visit / Visitor |
| `ledger.range.label` / `.choose` / `.today` / `.tooLong` | الفترة / اختر الفترة / اليوم / أطول فترة 92 يومًا؛ اختر فترة أقصر. | Period / Choose a period / Today / The longest period is 92 days; choose a shorter one. |
| `ledger.range.previous` / `.next` | الشهر السابق / الشهر التالي | Previous month / Next month |
| `ledger.staff.label` / `.all` / `.self({name})` / `.inactive({name})` | الموظف / كل الموظفين / {name} (أنت) / {name} · موقوف | Staff / All staff / {name} (you) / {name} · deactivated |
| `ledger.method.label` / `.all` | الطريقة / كل الطرق | Method / All methods |
| `ledger.kind.label` / `.all` / `.VISIT` / `.SUBSCRIPTION` | النوع / كل الأنواع / زيارات / اشتراكات | Type / All types / Visits / Subscriptions |
| `ledger.voided.chip` / `.quick` / `.badge` / `.line({name, reason})` | إظهار الملغاة / تصفية سريعة / ملغاة / ألغاها {name}: {reason} | Show voided / Quick filter / Voided / Voided by {name}: {reason} |
| `ledger.filters.title` / `.clear` / `.none` | الفلاتر / مسح الفلاتر / لا نتائج — غيّر الفلاتر | Filters / Clear filters / No results — change the filters |
| `ledger.filters.applied(n)` | zero «لا فلاتر مطبّقة» · one «فلتر واحد مطبّق» · two «فلتران مطبّقان» · few «{n} فلاتر مطبّقة» · many «{n} فلترًا مطبّقًا» · other «{n} فلتر مطبّق» | one «1 filter applied» · other «{n} filters applied» |
| `ledger.filters.show(n)` | one «عرض الدفعة» · two «عرض الدفعتين» · few «عرض {n} دفعات» · many «عرض {n} دفعة» · zero/other «عرض {n} دفعة» | one «Show 1 payment» · other «Show {n} payments» |
| `ledger.count(n)` | zero «لا دفعات» · one «دفعة واحدة» · two «دفعتان» · few «{n} دفعات» · many «{n} دفعة» · other «{n} دفعة» | one «1 payment» · other «{n} payments» |
| `ledger.totals({period, received, cash, transfer, count})` | {period} · المجموع {received} · نقدًا {cash} · تحويل {transfer} · {count} | {period} · Total {received} · Cash {cash} · Transfer {transfer} · {count} |
| `ledger.totalsVoided({count, amount})` | الملغاة: {count} · {amount} | Voided: {count} · {amount} |
| `ledger.emptyToday.title` / `.text` | لا توجد دفعات اليوم / تظهر هنا كل دفعة تُسجَّل في مكتب الاستقبال. اختر فترة لترى ما قبل اليوم. | No payments today / Every payment recorded at the front desk shows up here. Choose a period to see earlier ones. |
| `ledger.noMatch.title` / `.text` | لا توجد دفعات تطابق الفلاتر / غيّر الفترة أو الفلاتر. | No payments match the filters / Change the period or the filters. |
| `ledger.loadFailed` / `ledger.pagination` | تعذّر تحميل الدفعات / label «صفحات الدفعات» · previous «السابق» · next «التالي» · page «الصفحة {page}» · summary «صفحة {page} من {total}» · more «صفحات أخرى» | We couldn’t load the payments / Pages of payments · Previous · Next · Page {page} · Page {page} of {total} · More pages |

  (The methods are `desk.money.methods`; the refresh failure `occupancy.present.refreshFailed`.)
- **Docs:** `payments.md` — header (*Scope* «…; the web feature `features/payments`, dashboard-only: the owner's
  ledger and reception's «دفعاتي اليوم»»; *Authority*'s "no web screen yet" gone); *Who uses it* (the owner on
  «الدفعات»); *Behaviour* «**The ledger on the web**»; *Web decisions*: S1 (the list `payments`', the void
  `desk`'s), S8's ledger line, DI-1–DI-6, DI-13 — each «{date}, #PRNUM»; code map *Web*; *Web history*.
  `space-links.md` (staff, *Who uses it*): «the ledger's staff filter reads the reception accounts' names on the web
  (`useStaffPeople`)». `architecture.md` §2 *Built so far*: «…, «الدفعات», the owner's ledger of [payments](…) with
  [desk](…)'s void in each row, and «دفعاتي اليوم» (commit 4)…». `overview.md` *Built*'s Payments line: «…; on the
  dashboard, the owner's ledger with its filters and totals and the void, and reception's «دفعاتي اليوم»» (with
  commit 4). Findings 165, 166 (Open), the index.

### PR 1 · Commit 4 — `feat(payments): show reception its payments today`
- **`useMyPaymentsToday(spaceId)`** → `{ intro: string; wide: boolean; figures: { label: string; cash: { label;
  amount }; transfer: { label; amount; helper }; total: { label; amount; count } } | null; note: string; label;
  columns; state: 'loading' | 'failed' | 'empty' | 'ready'; rows: PaymentRowView[]; busy; pagination; failure;
  refreshFailure; empty: string }` — the query `{ voided: 'INCLUDE', page, limit: 20 }` (no range, no
  `recordedById`: the server answers reception's own of today), `?page=` in the address; the figures from
  `meta.totals` (cash = `byMethod.CASH`, transfer = `byMethod.TRANSFER`, total = `receivedAgorot`, count =
  `count`), never summed (DI-11).
- **`MyPaymentsToday({ spaceId })`** (exported): the intro (`text-body-sm text-muted-foreground`); below 768 px one
  `Card` with a `dl` of three rows — the cash first, the transfer with its helper under it (DI-10), the total with
  the count; from 768 px three `StatCard`s (the transfer's `helper`); the note (`text-caption`); `DataTable`
  `label` «دفعاتي اليوم»: time, name, item, method (`Badge`: cash `neutral`, transfer `info`), amount
  (`PaymentAmount`, the voided line naming who voided); `renderCard` below 768 px.
- **`MyPaymentsPage`** (reception's route `my-payments`): `PageHeader`; `MyPaymentsToday`. `SPACE_PAGES.myPayments`.
- **Words** (`payments.mine`):

| key | ar | en |
|---|---|---|
| `mine.intro({date})` | الدفعات التي سجّلتها أنت اليوم، لتسليمها في نهاية الوردية · {date} | The payments you recorded today, for the end-of-shift handover · {date} |
| `mine.figures` / `.cash` / `.transfer` / `.transferHelper` / `.total` | أرقام التسليم / نقدًا للتسليم / تحويل / وصلت إلى حساب المساحة / المجموع | Handover figures / Cash to hand over / Transfer / Received in the space’s account / Total |
| `mine.note` | خطأ في دفعة؟ يلغيها صاحب المساحة، وتظهر هنا مشطوبة. | A mistake in a payment? The space’s owner voids it, and it shows here struck through. |
| `mine.label` / `.columns` | دفعاتي اليوم / time «الوقت» · name «الاسم» · item «عن» · method «الطريقة» · amount «المبلغ» | My payments today / Time · Name · For · Method · Amount |
| `mine.empty` / `.loadFailed` | لم تسجّل أي دفعة اليوم / تعذّر تحميل دفعاتك | You haven’t recorded any payments today / We couldn’t load your payments |

- **Docs:** `payments.md` (*Who uses it*: reception's «دفعاتي اليوم»; *Behaviour*; DI-10, DI-11), finding 162's
  evidence: «#PRNUM: «دفعاتي اليوم» names who voided reception's own payment (`PaymentRow.voided.by`); the statement
  still names neither.»

### PR 2 · Commit 1 — `feat(announcements): list a space's announcements`
- **Repository** (`createAnnouncementsRepository()`): `list(spaceId, query: AnnouncementsQuery):
  Page<ManagedAnnouncement[]>` (`api.getPage`); `summary(spaceId): AnnouncementsSummary`.
- **Keys** (`announcementsKeys`): `all(id) = ['space', id, 'announcements']`, `list(id, state, page)`,
  `summary(id)`, `preview(id, announcementId)` (commit 4).
- **`services/announcementsQueryOf.ts`** (pure): `?state=upcoming|ended` (running not written), `?page=` →
  `{ state: AnnouncementState; page }`; a wrong value falls back.
- **`services/periodText.ts`** (pure): `periodText({ startsAt, endsAt }, language, now, words): string` — on Gaza's
  clock (`gazaClockOf`): the same day «1 أكتوبر 08:00–18:00», two days «1 أكتوبر 08:00 – 3 أكتوبر 18:00», no end
  «من 1 أكتوبر 08:00 · بلا نهاية»; the year when it is not `now`'s; the times isolated, LTR.
- **`services/typeView.ts`** (pure): `typeView(type, words) → { label; tone: 'warning' | 'neutral'; hint }`
  (`warning` for `OUTAGE`, `CLOSURE`, OW-014). **`services/textOf.ts`**: `textOf({ textAr, textEn }, language) →
  { text; lang?: 'ar'; dir?: 'rtl' }` (DI-27).
- **`useAnnouncementsList(spaceId, { owner })`** → `{ tabsLabel; tabs: { value: AnnouncementState; label; count:
  number | null }[]; tab; choose(tab); listLabel; state: 'loading' | 'failed' | 'empty' | 'ready'; cards:
  AnnouncementCardView[]; busy; empty: { title; text }; pagination: PaginationView | null /* past one page only,
  DI-26 */; failure; refreshFailure }` with `AnnouncementCardView = { key; id; type: { label; tone }; period:
  string; text: { text; lang?; dir? }; closureLine: string | null /* DI-28 */; edit, actions, extension: (commits
  2–4) }`.
- **`AnnouncementsList({ spaceId, owner })`** (exported): a row with the `Tabs` (`aria-label` «حالة الإعلانات»;
  each trigger its word and a `Badge` count, a `Skeleton` while the summary loads) and, at its end, «إعلان جديد»
  (commit 2); the cards `flex max-w-4xl flex-col gap-4`: `Card` — `CardHeader` with `CardTitle` (`h2`) the type's
  `Badge` and the period in `text-body-sm text-muted-foreground`, `CardContent` the text (`text-body`) and the
  closure's line (`text-caption`), `CardFooter` the actions (commits 2–4); loading three skeleton cards (DI-23),
  the list `aria-busy`; the empty state per tab (`MegaphoneIcon`) with «إعلان جديد»; `ListPagination` past one page.
- **`AnnouncementsPage`** (`pages/dashboard/space/announcements/`): `PageHeader`; `owner` from the session's link
  at the space; `AnnouncementsList`; `key={spaceId}`. `SPACE_PAGES.announcements`.
- **Words** (`announcements`, new section):

| key | ar | en |
|---|---|---|
| `tabs.label` / `.RUNNING` / `.UPCOMING` / `.ENDED` | حالة الإعلانات / نشطة / مجدولة / منتهية | Announcement status / Active / Scheduled / Ended |
| `types` | GENERAL «عام» · OUTAGE «انقطاع كهرباء أو إنترنت» · CLOSURE «إغلاق مؤقت» · OFFER «عرض» · EVENT «فعالية» | General · Power or internet outage · Temporary closure · Offer · Event |
| `hints` | GENERAL «خبر أو تنبيه للزوار» · OUTAGE «يبقى المكان مفتوحًا، ويُنبَّه الزوار» · CLOSURE «تظهر المساحة «مغلق الآن» طوال الفترة» · OFFER «سعر أو خدمة لفترة محدودة» · EVENT «ورشة أو لقاء في المساحة» | News or a note for visitors · The space stays open; visitors are warned · The space shows “Closed now” for the whole period · A price or a service for a limited time · A workshop or a meetup at the space |
| `period.sameDay({day, from, to})` / `.range({fromDay, from, toDay, to})` / `.open({day, from})` | {day} {from}–{to} / {fromDay} {from} – {toDay} {to} / من {day} {from} · بلا نهاية | {day} {from}–{to} / {fromDay} {from} – {toDay} {to} / From {day} {from} · no end |
| `closure.upcoming` / `.reception` | يمكن تمديد الاشتراكات بعد أن يبدأ الإغلاق. / يمدّد المالك الاشتراكات بعد بدء الإغلاق. | Subscriptions can be extended once the closure has started. / The owner extends subscriptions once the closure has started. |
| `empty.RUNNING` / `.UPCOMING` / `.ENDED` / `.text` | لا توجد إعلانات نشطة / لا توجد إعلانات مجدولة / لا توجد إعلانات منتهية / أعلن عن إغلاق، أو انقطاع، أو عرض، أو فعالية ليراه الزوار في صفحة المساحة. | No active announcements / No scheduled announcements / No ended announcements / Announce a closure, an outage, an offer or an event for visitors to see on the space page. |
| `list.label` / `.loadFailed` / `.pagination` | الإعلانات / تعذّر تحميل الإعلانات / label «صفحات الإعلانات» and the list's five words | Announcements / We couldn’t load the announcements / Pages of announcements … |

- **Docs:** `announcements.md` — header (*Scope* «…; the web feature `features/announcements`, any page group: screen
  18, and the public pieces a space's page sets (PR 4)»; *Authority*'s "no screen yet" gone); *Who uses it*
  (the owner and reception on «الإعلانات»); *Behaviour* «**The announcements on the web**»; *Web decisions*: S2,
  S8's line, DI-15, DI-23, DI-26, DI-27; code map *Web*; *Web history*. `subscriptions.md` *Who uses it*: «On the
  web, «الإعلانات» reads the managed list and its summary ([announcements](announcements.md))». `architecture.md` §3
  (S2's line), §2 *Built so far*. `overview.md`'s Announcements line: «…; on the dashboard, the owner's and
  reception's «الإعلانات»…» (completed by commit 4).

### PR 2 · Commit 2 — `feat(announcements): post and edit an announcement`
- **Repository:** `create(spaceId, body: CreateAnnouncementRequest, key: string): Promise<Announcement>` (`api.post`
  with `withIdempotencyKey(key)`); `edit(spaceId, id, body: EditAnnouncementRequest): Promise<Announcement>`
  (`api.patch`).
- **`hooks/useAnnouncementsWrite.ts`:** `{ settle(spaceId) /* ['space', spaceId], not awaited (S12) */; linkEnded }`
  — the desk's shape.
- **`types/SheetValues.ts`:** `{ type: AnnouncementType; textAr: string; textEn: string; startMode: 'now' | 'at';
  startDate: string; startTime: string; endMode: 'at' | 'none'; endDate: string; endTime: string }`.
- **`services/sheetRequest.ts`** (pure, S9): `minuteOf('HH:MM'): number`; `instantOf(date, time): string`
  (`gazaInstant(date, minuteOf(time)).toISOString()`); `createRequestOf(values): CreateAnnouncementRequest` (a blank
  English text left out; `now` → no `startsAt`; `none` → no `endsAt`); `editRequestOf(values, loaded: Announcement):
  EditAnnouncementRequest` (only what differs: an instant compared as an instant; a cleared English text →
  `textEn: null`; `none` with an end loaded → `endsAt: null`); `valuesOf(loaded, now): SheetValues` (Gaza's wall
  clock; a new sheet: today, now's minute, the end at the day's 18:00 or the next hour).
- **`useAnnouncementSheet({ spaceId, entry, showTab, onClose })`**, `entry: { mode: 'new'; type?: AnnouncementType } |
  { mode: 'edit'; announcement: ManagedAnnouncement }` → `{ title; description; type: { label; options: { value;
  label; hint }[]; field }; textAr: { label; helper; field; error }; textEn: { label; optional; helper; field; error
  }; start: { label; modes: { value; label }[] | null /* new only */; at: boolean; date: { label; text; value;
  choose }; time: { label; field; error } }; end: { label; modes; at: boolean; date; time; help: string | null };
  closure: string | null /* DI-29 */; preview: { label; item: PublicItemView; closure: boolean }; submit: { label;
  run; busy; blocked }; failure }` — `useServerForm<SheetValues, …>` over `createAnnouncementSchema` /
  `editAnnouncementSchema`, `prepare` the request; `fieldLines` (`textAr.required`, `startsAt.out_of_range`,
  `endsAt.out_of_range`, DI-30); `failureLines` (`CLOSURE_EXTENDED`, `not_found`, `forbidden`, and for a post
  `network`/`timeout` → `sheet.lost`); an edit that changes nothing → `sheet.nothingChanged`, nothing sent; the key
  from `useIntentKey` (each opening mounts a new sheet: the list keys it by its opening's count, as #124's
  `useSheetOpener`); done → `toastPublished` / `toastSaved` with «في «{tab}»» and «عرض» → `showTab(answer.state)`
  (DI-24), `settle`, `onClose`.
- **Components:** `AnnouncementSheet` — `Sheet` `side="end"` (full width on a phone since #124), `SheetHeader`,
  a `form` with `SheetBody className="flex min-w-0 flex-col gap-5"`: `TypeChoice` (`RadioGroup`, each a `Field
  orientation="horizontal"` with the type and its hint; the checked radio focused first, DI-21), the Arabic `Textarea`
  (`lang="ar" dir="rtl"`), the English `Textarea` (`lang="en" dir="ltr"`, «اختياري» in the label's end),
  `PeriodFields` (each of start and end: a `ToggleGroup type="single"` and, «في موعد», a `grid gap-3 sm:grid-cols-2`
  of the date (`DatePicker`, `Calendar mode="single" lang`, the trigger «29 سبتمبر 2026», DI-22) and the time
  (`Input type="time" dir="ltr"`)), the closure's `Alert variant="warning"`, the preview (`rounded-lg bg-muted p-3`,
  its caption, then `AnnouncementItem` or `ClosureNotice` — `components/public/`, drawn as the space's page will,
  DI-25); `SheetFooter` the submit `w-full`. The list's «إعلان جديد» (`Button`, at the tabs row's end, P1) and each
  running or upcoming card's «تعديل» (outline, DI-16) open it; closed, the focus returns to its opener (Radix).
- **Words** (`announcements.sheet`, `.toast`, `.public`, `.actions.new`, `.actions.edit`):

| key | ar | en |
|---|---|---|
| `actions.new` / `.edit` | إعلان جديد / تعديل | New announcement / Edit |
| `sheet.new` / `.edit` / `.description` | إعلان جديد / تعديل الإعلان / يظهر في صفحة المساحة العامة خلال الفترة. | New announcement / Edit announcement / Shown on the space’s public page during the period. |
| `sheet.type` / `.textAr` / `.textArHelper` | النوع / نص الإعلان بالعربية / جملة أو جملتان يقرؤها الزائر في صفحة المساحة. | Type / Text in Arabic / A sentence or two visitors read on the space page. |
| `sheet.textEn` / `.textEnHelper` / `.optional` | نص الإعلان بالإنجليزية / يظهر في الواجهة الإنجليزية؛ بدونه يظهر النص العربي. / اختياري | Text in English / Shown in the English interface; without it, the Arabic text shows. / Optional |
| `sheet.starts` / `.ends` / `.now` / `.at` / `.noEnd` / `.noEndHelp` | يبدأ / ينتهي / الآن / في موعد / بلا موعد / يبقى حتى تنهيه. | Starts / Ends / Now / At a time / No end / It stays until you end it. |
| `sheet.date` / `.time` / `.chooseDate` / `.previousMonth` / `.nextMonth` | التاريخ / الساعة / اختر التاريخ / الشهر السابق / الشهر التالي | Date / Time / Choose a date / Previous month / Next month |
| `sheet.closure` | تظهر المساحة «مغلق الآن» للزوار طوال هذه الفترة، ويُنبَّه الاستقبال عند تسجيل الحضور. | Visitors see the space as “Closed now” for this whole period, and the desk is warned at check-in. |
| `sheet.preview` | معاينة — صفحة المساحة العامة | Preview — the space’s public page |
| `sheet.publish` / `.save` / `.failed` / `.nothingChanged` | نشر الإعلان / حفظ / تعذّر حفظ الإعلان / لم يتغيّر شيء | Publish / Save / We couldn’t save the announcement / Nothing changed |
| `sheet.lost` | لم يصل الرد. أعد المحاولة — لن يُنشر مرتين. | No answer came back. Try again — it won’t be published twice. |
| `sheet.fields.textArRequired` / `.startRange` / `.endRange` | أدخل نص الإعلان بالعربية / البداية بين 30 يومًا مضت و365 يومًا قادمة. / النهاية بعد الآن، وبعد البداية، وخلال 365 يومًا منها. | Enter the Arabic text / The start is between 30 days ago and 365 days ahead. / The end comes after now and after the start, within 365 days of it. |
| `sheet.gone` | لم يعد هذا الإعلان موجودًا. | This announcement no longer exists. |
| `toast.published` / `.saved` / `.inTab({tab})` / `.show` | نُشر الإعلان / حُفظ الإعلان / في «{tab}» / عرض | Announcement published / Announcement saved / In “{tab}” / Show |
| `public.title` / `.notice({period})` | الإعلانات / إعلان من إدارة المساحة · {period} | Announcements / An announcement from the space · {period} |

- **Docs:** `announcements.md` (*Behaviour*: the sheet, the key per opening, Gaza's clock; *Web decisions*: S4's
  post line, S9, S12, DI-21, DI-22, DI-24, DI-25, DI-29, DI-30); `architecture.md` §7 (S12's line).

### PR 2 · Commit 3 — `feat(announcements): end, start or delete one`
- **Repository:** `end(spaceId, id): Announcement` (`POST …/end`), `start(spaceId, id): Announcement` (`POST
  …/start`), `remove(spaceId, id): undefined` (`DELETE`).
- **`useAnnouncementActions(spaceId, card, { showTab })`** → `{ end: { label; run; busy } | null /* running */;
  start: { label; run; busy } | null /* upcoming */; menu: { label /* «إجراءات أخرى: {type} · {period}» */; remove:
  { label; open } | null /* not an extended closure */ } ; lock: string | null /* DI-17's line */ }` — each sent
  once with no key; end now → `toastEnded` («انتهى الإعلان», a closure «انتهى الإغلاق · عادت الحالة تلقائية»,
  description «في «منتهية»», action «تراجع» except for an extended closure: one `edit({ endsAt: was })`, said
  «أُعيد الإعلان كما كان» or «تعذّر التراجع» with its line); start now → «بدأ الإعلان الآن», «في «نشطة»» and «عرض»;
  a failure → an error toast with its line (`ANNOUNCEMENT_NOT_STARTED`, `startTooLong` for `out_of_range` on
  `endsAt`, a 403, `errors.network`) and «إعادة المحاولة» (sent again once, idempotent by design); each settles.
- **`useDeleteDialog({ spaceId, card, onClose, returnFocus })`** → `{ title; text /* by state, DI-18 */; back;
  confirm: { label; run; busy }; failure }` — sent once; `CLOSURE_EXTENDED` → its line (and the list read again);
  done → «حُذف الإعلان».
- **The focus:** the list keeps it (DI-24): a card that leaves its tab (ended, started, deleted) hands the focus
  to the next card's first action, else the tabs' list.
- **Components:** `AnnouncementMenu` (a ghost «⋯», `aria-label` the menu's, its content labelled the same, «حذف…»
  `destructive`; the trigger kept by a ref for the dialog's return), `DeleteDialog` (`AlertDialog`, destructive
  «حذف», «رجوع»); `components/toast/announcementToasts.tsx`. The card's footer: «تعديل», then «إنهاء الآن» or «ابدأ
  الآن» (outline), then the «⋯» at the end.
- **Words** (`announcements.actions`, `.delete`, `.closure.extendedLock`):

| key | ar | en |
|---|---|---|
| `actions.end` / `.start` / `.more({type, period})` / `.delete` | إنهاء الآن / ابدأ الآن / إجراءات أخرى: {type} · {period} / حذف… | End now / Start now / More actions: {type} · {period} / Delete… |
| `actions.ended` / `.closureEnded` / `.started` | انتهى الإعلان / انتهى الإغلاق · عادت الحالة تلقائية / بدأ الإعلان الآن | The announcement has ended / The closure has ended · the status is automatic again / The announcement has started |
| `actions.undo` / `.undone` / `.undoFailed` / `.failed` / `.startTooLong` | تراجع / أُعيد الإعلان كما كان / تعذّر التراجع / تعذّر تنفيذ الإجراء / نهايته بعد أكثر من 365 يومًا من الآن؛ عدّلها أولًا. | Undo / The announcement is back as it was / We couldn’t undo it / We couldn’t do that / Its end is more than 365 days from now; edit it first. |
| `delete.title({type, period})` | حذف إعلان «{type} · {period}»؟ | Delete the announcement “{type} · {period}”? |
| `delete.runningClosure` / `.running` / `.upcoming` / `.ended` | يختفي من صفحة المساحة، وتعود حالتها تلقائية فورًا. لا يمكن استرجاعه. / يختفي من صفحة المساحة فورًا. لا يمكن استرجاعه. / لن يظهر للزوار. لا يمكن استرجاعه. / يُحذف من القائمة. لا يمكن استرجاعه. | It leaves the space’s page, and the status is automatic again at once. It can’t be brought back. / It leaves the space’s page at once. It can’t be brought back. / Visitors won’t see it. It can’t be brought back. / It leaves this list. It can’t be brought back. |
| `delete.confirm` / `.back` / `.done` / `.failed` | حذف / رجوع / حُذف الإعلان / تعذّر حذف الإعلان | Delete / Back / Announcement deleted / We couldn’t delete the announcement |
| `closure.extendedLock` | مُدّدت اشتراكاته، فلا يُحذف ولا تُؤخَّر نهايته. | Its subscriptions were extended, so it isn’t deleted and its end isn’t moved later. |

- **Docs:** `announcements.md` (*Behaviour*: end now and its undo, start now, delete; *Web decisions*: S4's lines for
  the unkeyed writes, DI-16, DI-17, DI-18).

### PR 2 · Commit 4 — `feat(announcements): extend after a closure`
- **Repository:** `preview(spaceId, id): ExtensionPreview` (`GET …/extend-subscriptions`); `extend(spaceId, id, body:
  ExtendSubscriptionsRequest, key): ClosureExtension` (`POST`, `withIdempotencyKey`).
- **`useExtensionPreviewQuery(spaceId, id)`** — `refetchOnMount: 'always'` (S3).
- **`useExtensionDialog({ spaceId, closure, onClose })`** → `{ state: 'loading' | 'failed' | 'none' | 'applied' |
  'ready'; title; covered: string /* «شمل الإغلاق {n}.» */; text; days: { label; helper; field; error }; submit: {
  label /* «مدّد {n}» */; run; busy; blocked }; back; failure; loadFailure; applied: string | null }` — `useServerForm<{
  days: string }, ExtendSubscriptionsRequest>`, `prepare` → `{ days: wholeNumberOf(text) }` (Arabic digits read);
  the days prefilled with `proposedDays` (DI-20); one key per opening (the card mounts the dialog per opening);
  `failureLines`: `CLOSURE_ALREADY_EXTENDED`, `ANNOUNCEMENT_NOT_STARTED`, `forbidden` (`desk.refusals.forbidden`),
  `conflict`, `network`/`timeout` → `extension.lost`; the failure inside the dialog (DI-19); `none` (S11) and
  `applied` (another owner meanwhile) show their line with «رجوع» only; done → «مُدّدت الاشتراكات» with «{count} ·
  {days}», `settle`.
- **The card:** the owner, a closure not upcoming and `extension === null` → «تمديد الاشتراكات» (outline);
  reception → `closure.reception`; upcoming → `closure.upcoming` (the owner); `extension` set →
  `extension.line({ count, days, name, date })`.
- **`ExtensionDialog`** — `AlertDialog`: the title, the covered line and the text; the days `Field` with an `Input
  inputMode="numeric" dir="ltr" className="w-20"` and its helper; the failure; «رجوع» and the `destructive` submit;
  a `Skeleton` while the preview loads.
- **Words** (`announcements.extension`):

| key | ar | en |
|---|---|---|
| `extension.action` / `.title` | تمديد الاشتراكات / تمديد الاشتراكات التي شملها الإغلاق؟ | Extend subscriptions / Extend the subscriptions this closure covered? |
| `extension.covered(n)` | zero «لم يشمل الإغلاق أي اشتراك.» · one «شمل الإغلاق اشتراكًا واحدًا.» · two «شمل الإغلاق اشتراكين.» · few «شمل الإغلاق {n} اشتراكات.» · many «شمل الإغلاق {n} اشتراكًا.» · other «شمل الإغلاق {n} اشتراك.» | one «The closure covered 1 subscription.» · other «The closure covered {n} subscriptions.» |
| `extension.text` | تتأخر نهاية كلٍّ منها بعدد الأيام أدناه. لا يمكن التراجع، ولا التمديد مرة ثانية لهذا الإغلاق. | Each one’s end moves by the days below. It can’t be undone, nor applied again for this closure. |
| `extension.days` / `.daysHelper({days, first, last})` / `.daysRange` | عدد الأيام / أيام الإغلاق: {days} ({first} – {last}) / بين 1 و365 يومًا | Number of days / The closure’s days: {days} ({first} – {last}) / Between 1 and 365 days |
| `extension.submit(n)` | one «مدّد اشتراكًا واحدًا» · two «مدّد اشتراكين» · few «مدّد {n} اشتراكات» · many «مدّد {n} اشتراكًا» · zero/other «مدّد {n} اشتراك» | one «Extend 1 subscription» · other «Extend {n} subscriptions» |
| `extension.count(n)` | zero «لا اشتراكات» · one «اشتراك واحد» · two «اشتراكان» · few «{n} اشتراكات» · many «{n} اشتراكًا» · other «{n} اشتراك» | one «1 subscription» · other «{n} subscriptions» |
| `extension.dayCount(n)` | zero «لا أيام» · one «يوم واحد» · two «يومان» · few «{n} أيام» · many «{n} يومًا» · other «{n} يوم» | one «1 day» · other «{n} days» |
| `extension.line({count, days, name, date})` | مُدّد {count} · {days} · {name} · {date} | Extended {count} · {days} · {name} · {date} |
| `extension.none` / `.applied({count, days})` | لم يشمل هذا الإغلاق أي اشتراك، فلا شيء يُمدَّد. / مُدّدت اشتراكات هذا الإغلاق من قبل: {count} · {days}. | This closure covered no subscription, so there is nothing to extend. / This closure’s subscriptions were already extended: {count} · {days}. |
| `extension.done` / `.doneText({count, days})` | مُدّدت الاشتراكات / {count} · {days} | Subscriptions extended / {count} · {days} |
| `extension.failed` / `.loadFailed` / `.lost` / `.back` | تعذّر التمديد / تعذّر حساب الاشتراكات المشمولة / لم يصل الرد. أعد المحاولة — لن تُمدَّد مرتين. / رجوع | We couldn’t extend them / We couldn’t work out the subscriptions covered / No answer came back. Try again — they won’t be extended twice. / Back |

- **Docs:** `announcements.md` (*Behaviour*: the extension on the web; *Web decisions*: S4's extension line, S11,
  DI-19, DI-20, DI-28); `subscriptions.md` *Who uses it*: «…and the owner extends a closure's subscriptions from it
  ([announcements](announcements.md))»; `overview.md`'s Announcements line completed. The report gives the
  supervisor `OPEN_DECISIONS.md` point 2's *Built as (web)* line: «the owner's «تمديد الاشتراكات» on a started
  closure, the preview's days and count, the days typed, one key per opening; reception reads that the owner
  extends ({date}, #PRNUM).» `foundation.md` §13 screen 18's line becomes «… the owner can then extend the
  subscriptions it covered, by the days typed, once» (§14.8).

### PR 3 · Commit 1 — `feat(design-system): add a removable filter tag`
- **`FilterTag({ children, removeLabel, onRemove, className })`** (`components/display/FilterTag/`): a `span`
  `inline-flex items-center gap-1 rounded-(--radius-pill) bg-secondary ps-3 text-body-sm text-secondary-foreground`
  (the pill radius the layer's chips use, §13 check 5.i) holding the label and a ghost `Button size="icon"` with
  `XIcon` (`aria-hidden`), named by `removeLabel` (a prop: no built-in words, foundation §11), its hit area 44 × 44
  on a coarse pointer (AD-030's rule, as `size="icon"` has it). Exported from the layer's barrel.
- **Showcase:** `FilterTagSection` — two tags («المساحة: نور هب», «الحقل: الأسعار») and «مسح الفلاتر», in both
  languages (its words in `fixtures.json`, as the other sections').
- **Docs:** `foundation.md` §12 `display`: «| FilterTag | hand-built | A filter in force: its label and a remove
  button named by a prop (finding 8) |»; finding 8 → Resolved («#PRNUM: `FilterTag`, used by the admin's data
  reports»), the index.

### PR 3 · Commit 2 — `feat(data-reports): decide a space's reports`
- **Repository** (`createDataReportsRepository()`): `spaceReports(spaceId, query: SpaceReportsQuery):
  Page<SpaceReport[]>`; `decideSpace(spaceId, reportId, body: DecideReportRequest): SpaceReport` (`PATCH`).
- **Keys** (`dataReportsKeys`): `space(id, query) = ['space', id, 'dataReports', query]`, `spaceAll(id)`,
  `admin(query) = ['admin', 'dataReports', query]`, `adminAll`, `mine(query) = ['me', 'reports', query]`, `mineAll`.
- **`services/reportView.ts`** (pure): `fieldLabel(field, words)`; `statusView(status, words, audience: 'staff' |
  'reporter') → { label; tone: 'info' | 'success' | 'neutral' }` (DI-31); `reportDay(instant, language, now)` — the
  Gaza day, the year when not `now`'s, **never the time** (DI-34); `messageView(message, words) → { text } | { none }`
  (DI-35). **`services/reportsQueryOf.ts`**: `?status=open|decided&page=` → `{ status?: 'OPEN' | 'DECIDED'; page }`.
- **`useSpaceReports(spaceId)`** → `{ label; intro; columns; chips: { label; value: 'all' | 'open' | 'decided';
  options; choose }; count: string; state: 'loading' | 'failed' | 'empty' | 'noMatch' | 'ready'; rows: ReportRowView[];
  busy; empty: { title; text: string | null; showAll: { label; run } | null }; pagination; failure; refreshFailure;
  sheet: DecideTarget | null; close() }`, `ReportRowView = { key; id; field; message: { text } | { none }; day;
  status: { label; tone }; open: { label; run } }`.
- **`useDecideSheet({ target, editLink, showDecided, onClose })`**, `DecideTarget = { audience: 'owner' | 'admin';
  report: SpaceReport | AdminReport }` → `{ title; description /* «زائر · {day}» or «{reporter} · {day}» */; status;
  facts: { label; message }; readOnly: string | null; editLink: { label; to } | null; decided: { label; reply } |
  null; reply: { label; helper; field; error } | null; resolve: { label; run; busy } | null; dismiss: { label; run;
  busy } | null; failure }` — `useServerForm<{ note: string }, DecideReportRequest>`; each button sets the
  status; «لم يُعتمد» with a blank reply → `required` on `note`, focused, its line (DI-36); sent once (S4); done →
  `toastDecided` (DI-41) with «عرض» → `showDecided()`; `REPORT_ALREADY_DECIDED` and `not_found` → their lines and
  the list read again; a 403 → S5's lines.
- **Components:** `StatusChips` (`ToggleGroup type="single"`, named); `SpaceReportsList({ spaceId, fieldLink })`
  (exported) — the intro, the chips, the count (`aria-live="polite"`), `DataTable` `label` «بلاغات البيانات»
  (field `text-label`, the report `line-clamp-2 text-body-sm` with `dir="auto"`, the day, the status `Badge`, «فتح»
  outline), `renderCard` below 768 px (the field and the badge, the report, «زائر · {day}» and «فتح»), the empty
  state (`FlagIcon`); `DecideSheet({ sheet })` — `Sheet side="end"`: its header (title, description, the badge),
  `SheetBody` — the readOnly `Alert` (admin), the facts box (`rounded-lg bg-muted p-3`, «البلاغ» caption), «تعديل
  الحقل» (outline `Link`, `ArrowEndIcon`), the decided block or the reply `Textarea` with its helper; the failure;
  `SheetFooter className="flex flex-row gap-2"` — «تم التصحيح» (primary, `flex-1`), «لم يُعتمد» (outline,
  `flex-1`).
- **`DataReportsPage`** (`pages/dashboard/space/reports/`): `fieldLink = (field) => field === 'PRICES' ?
  spacePagePath(spaceId, 'packages') : spacePagePath(spaceId, 'profile')` (plus the editor's section anchor when
  §13 check 5.l finds one); `SPACE_PAGES.dataReports`.
- **Words** (`dataReports`, new section):

| key | ar | en |
|---|---|---|
| `fields` | PRICES «الأسعار» · HOURS «ساعات العمل» · CONTACT «التواصل» · LOCATION «الموقع» · AMENITIES «المرافق» · OTHER «أخرى» | Prices · Opening hours · Contact · Location · Amenities · Other |
| `statuses.staff` / `.reporter` | OPEN «جديد» · RESOLVED «تم التصحيح» · DISMISSED «لم يُعتمد» / OPEN «قيد المراجعة» · RESOLVED «تم التصحيح» · DISMISSED «لم يُعتمد» | New · Corrected · Not accepted / In review · Corrected · Not accepted |
| `chips.label` / `.all` / `.open` / `.decided` | تصفية حسب الحالة / الكل / جديدة / تمت المراجعة | Filter by status / All / New / Reviewed |
| `space.label` / `.intro` / `.columns` | بلاغات البيانات / بلاغات الزوار عن معلومات خاطئة في صفحة المساحة. / field «الحقل» · report «البلاغ» · date «التاريخ» · status «الحالة» · actions «إجراءات» | Data reports / Visitors’ reports about wrong information on the space page. / Field · Report · Date · Status · Actions |
| `count(n)` | zero «لا بلاغات» · one «بلاغ واحد» · two «بلاغان» · few «{n} بلاغات» · many «{n} بلاغًا» · other «{n} بلاغ» | one «1 report» · other «{n} reports» |
| `open` / `view` / `visitor` / `noMessage` | فتح / عرض / زائر / لم يكتب المُبلِّغ تفاصيل. | Open / View / A visitor / The reporter wrote no details. |
| `empty.title` / `.text` / `noMatch` / `showAll` | لا توجد بلاغات / عندما يبلّغ زائر عن معلومة خاطئة تظهر هنا. / لا توجد بلاغات تطابق الفلاتر / عرض الكل | No reports / When a visitor reports wrong information, it shows up here. / No reports match the filters / Show all |
| `loadFailed` / `pagination` | تعذّر تحميل البلاغات / label «صفحات البلاغات» and the list's five words | We couldn’t load the reports / Pages of reports … |
| `sheet.title({field})` / `.report` / `.editField` | بلاغ عن {field} / البلاغ / تعديل الحقل | Report about {field} / The report / Edit the field |
| `sheet.replySpace` / `.replyTeam` / `.replyHelper` / `.replyRequired` | ردّ إدارة المساحة / ردّ فريقنا / يظهر لصاحب البلاغ. مطلوب لـ«لم يُعتمد»، واختياري لـ«تم التصحيح». / اكتب السبب؛ هو ما سيقرؤه صاحب البلاغ. | Reply from the space / Reply from our team / Shown to the person who reported it. Required for “Not accepted”, optional for “Corrected”. / Write the reason; it’s what the reporter will read. |
| `sheet.resolve` / `.dismiss` / `.failed` / `.lost` | تم التصحيح / لم يُعتمد / تعذّر حفظ القرار / لم يصل الرد. أعد المحاولة — القرار نفسه لا يُسجَّل مرتين. | Corrected / Not accepted / We couldn’t save the decision / No answer came back. Try again — the same decision isn’t recorded twice. |
| `sheet.decided` / `.reply({text})` / `.noReply` / `.gone` | القرار / الردّ: {text} / بلا ردّ / لم يعد هذا البلاغ موجودًا. | Decision / Reply: {text} / No reply / This report no longer exists. |
| `toast.resolved` / `.dismissed` / `.replied` / `.inDecided` / `.show` | عُلّم «تم التصحيح» / عُلّم «لم يُعتمد» / أُرسل الردّ لصاحب البلاغ. / في «تمت المراجعة» / عرض | Marked “Corrected” / Marked “Not accepted” / The reply is shown to the reporter. / In “Reviewed” / Show |

- **Docs:** `data-reports.md` — header (*Scope*: the web feature, any page group; "no screen yet" gone); *Who uses it*
  (the owner on «بلاغات البيانات»); *Behaviour* «**The owner's reports on the web**»; *Web decisions*: S8's line,
  DI-31, DI-33, DI-34, DI-36, DI-37, DI-41, DI-42; code map *Web*; *Web history*. `architecture.md` §2;
  `overview.md`'s Data reports line; finding 150's evidence: «#PRNUM: the owner's screen shows a report's day only.»

### PR 3 · Commit 3 — `feat(data-reports): list every space's reports`
- **Repository:** `adminReports(query: AdminReportsQuery): Page<AdminReport[]>`; `decideAdmin(reportId, body):
  AdminReport`.
- **`services/adminReportsQueryOf.ts`** (pure): `?status=&field=&space=&page=` → `{ filters: { status?; field?;
  spaceId?; page }; query }`.
- **`useAdminReports({ editorLink })`** → `{ label; intro; columns; chips; filters: { wide: boolean /* 768 */;
  space: { label; value: number | undefined; chosenName: SpaceNameView | null /* the answer's rows' space while
  filtered */; choose }; field: { label; value; options; choose }; sheet: { title; applied; show; clear } }; tags: {
  key; label; removeLabel; remove }[] /* DI-40 */; clear: { label; run } | null; count; state; rows:
  AdminReportRowView[] /* + space (name, link), reporter, handledBy: { label; tone } */; busy; empty; pagination;
  failure; refreshFailure; sheet; close }` — a verified space's row opens the sheet read-only (`audience: 'admin'`,
  DI-38), «عرض» on its button.
- **`AdminReportsList({ spaceFilter, editorLink })`** (exported) — the intro, the chips, the filters (inline from
  768 px: the `spaceFilter(value, onChange, chosenName)` slot and the field `Select`; below it in the bottom
  sheet with its count), the tags row (`FilterTag`s and «مسح الفلاتر»), the count, `DataTable cardsBelow="lg"`
  (space, field, report, reporter, date, status, «يعالجه» `Badge`, «فتح»/«عرض»), `renderCard`, `DecideSheet`.
- **`AdminSpaceFilter({ value, chosenName, onChange })`** (`features/space-links`, exported): a `Field` «المساحة»
  around `SpaceCombobox` over `useSpaceChoices({ enabled })`, its first item «كل المساحات» (clears), the trigger
  the chosen name or «مساحة محددة» before the choices load.
- **The admin's `DataReportsPage`** (`pages/dashboard/admin/`): `spaceFilter = (value, onChange, chosenName) =>
  <AdminSpaceFilter … />`, `editorLink = adminSpacePath`; `ADMIN_PAGES.dataReports`.
- **Words** (`dataReports.admin`, `spaceLinks.choices.allSpaces`):

| key | ar | en |
|---|---|---|
| `admin.label` / `.intro` | بلاغات البيانات / تقرّر الإدارة بلاغات المساحات غير الموثّقة. بلاغات المساحات الموثّقة يقرّرها مالكها، وتظهر هنا للاطلاع. | Data reports / The admin decides unverified spaces’ reports. Verified spaces’ reports are decided by their owner and shown here for reference. |
| `admin.columns` | space «المساحة» · field «الحقل» · report «البلاغ» · reporter «المُبلِّغ» · date «التاريخ» · status «الحالة» · handledBy «يعالجه» · actions «إجراءات» | Space · Field · Report · Reporter · Date · Status · Handled by · Actions |
| `admin.handledBy` | admin «الإدارة» · owner «المالك» | Admin · Owner |
| `admin.space` / `.allSpaces` / `.chosen` / `.field` / `.allFields` | المساحة / كل المساحات / مساحة محددة / الحقل / كل الحقول | Space / All spaces / A chosen space / Field / All fields |
| `admin.tags.space({name})` / `.field({field})` / `.removeSpace` / `.removeField` / `.clear` | المساحة: {name} / الحقل: {field} / إزالة فلتر المساحة / إزالة فلتر الحقل / مسح الفلاتر | Space: {name} / Field: {field} / Remove the space filter / Remove the field filter / Clear filters |
| `admin.filters.title` / `.applied(n)` / `.show(n)` / `.none` | الفلاتر / (as `payments.ledger.filters.applied`) / one «عرض البلاغ» · two «عرض البلاغين» · few «عرض {n} بلاغات» · many «عرض {n} بلاغًا» · zero/other «عرض {n} بلاغ» / لا نتائج — غيّر الفلاتر | Filters / … / one «Show 1 report» · other «Show {n} reports» / No results — change the filters |
| `admin.readOnly` / `.openSpace` / `.forbiddenVerified` | مساحة موثّقة — يقرّر مالكها هذا البلاغ. للاطلاع فقط. / عرض المساحة / هذه المساحة موثّقة: يقرّر مالكها هذا البلاغ. | Verified space — its owner decides this report. For reference only. / View the space / This space is verified: its owner decides this report. |
| `spaceLinks.choices.allSpaces` | كل المساحات | All spaces |

- **Docs:** `data-reports.md` (*Who uses it*: the admin; *Behaviour*; *Web decisions*: DI-32, DI-38, DI-39, DI-40,
  DI-43); `space-links.md` *Who uses it*: «the admin's data reports filter by one space (`AdminSpaceFilter`)»; finding
  167 (Open).

### PR 4 · Commit 1 — `feat(data-reports): show a user's own reports`
- **Repository:** `myReports(query: MyReportsQuery): Page<MyReport[]>`.
- **`useMyReports({ spaceLink })`** → `{ chips; count; state: 'loading' | 'failed' | 'empty' | 'none' | 'ready'; cards:
  MyReportCardView[]; busy; empty: { title; text: string | null; browse: boolean }; pagination; failure;
  refreshFailure }` (`?status=open|decided&page=`, a change back to page 1, DI-55), `MyReportCardView = { key; space:
  { name: SpaceNameView; link: string | null /* listed */; gone: string | null /* C7 */ }; meta: string /* «{field} ·
  أُرسل {day}» */; status: { label; tone } /* reporter's words */; message: { id; text; toggle: { label; expanded;
  run } | null /* over 160 characters, DI-54 */ } | null; reply: { label /* by repliedBy, DI-56 */; text } | null }`.
- **`MyReportsList({ spaceLink, browseLink })`** (exported): the chips; `<section aria-label="البلاغات"
  aria-busy>`; a `Card` each — `CardTitle` (`h2`) the space (a `Link` while listed, its name as muted text
  otherwise), `CardDescription` the meta (and C7's line), `CardAction` the status `Badge`; the message `dir="auto"
  text-body-sm` (`line-clamp-2` while folded, its `id` the toggle's `aria-controls`) and «عرض المزيد»/«عرض أقل»
  (`Button variant="link" size="sm"`); the reply box (`rounded-md bg-muted px-3 py-2`: its label `text-caption`, the
  text `dir="auto"`); `ListPagination`; the empty states (DI-53, `FlagIcon`).
- **`AccountLayout`** (`pages/site/account/`): `<div className="mx-auto flex w-full max-w-7xl flex-col gap-6 px-4
  py-6 md:px-8 md:py-10 lg:grid lg:grid-cols-12 lg:items-start lg:gap-8">`: `<nav aria-labelledby>` (`lg:col-span-3`)
  with its label «حسابي» (`sr-only` below 1024 px, visible from it, DI-57) and its links (`Button asChild size="sm"`,
  `variant="secondary"` and `aria-current="page"` on the current, `ghost` otherwise; a row with a border below it on
  a phone, a column from 1024 px), then `<Outlet/>` (`lg:col-span-9 min-w-0`). Each page draws its `h1`
  (`text-heading-1`) and its description.
- **`MyReportsPage`**: the `h1` «بلاغاتي», the description, `MyReportsList` (`spaceLink = publicSpacePath`,
  `browseLink = SITE_PATHS.spaces`). Routes: inside `SiteLayout`'s error boundary group, `{ lazy: AccountLayout,
  children: [{ path: SITE_PATHS.myReports, handle: title «بلاغاتي», lazy: <RequireAuth><MyReportsPage/></RequireAuth> }] }`;
  `navigation.ts`: `SITE_PATHS.myReports = '/me/reports'`, `myFavorites = '/me/favorites'`, and `ACCOUNT_LINKS`
  (the account's navigation's items, in order: favourites (from commit 5), reports).
- **The account menu (P4, `users`):** `AccountMenu`, `AccountMenuSection` gain `links?: readonly { key: 'favorites' |
  'reports'; to: string }[]`; `useAccount` words them (`users.account.links`); `AccountMenuContent` draws them after
  the label (a `DropdownMenuItem asChild` `Link`, `FlagIcon` for reports, `HeartIcon` for favourites from commit 3),
  the phone's section as ghost `Button`s; `SiteHeader` and `SiteMenu` pass the site's links; the dashboard's
  `CompactAccountMenu` passes none.
- **Words** (`dataReports.mine`, `site.account`, `users.account.links`):

| key | ar | en |
|---|---|---|
| `mine.title` / `.description` | بلاغاتي / البلاغات التي أرسلتها عن معلومات خاطئة، الأحدث أولًا. | My reports / Reports you sent about wrong information, newest first. |
| `mine.chips.label` / `.all` / `.open` / `.decided` | تصفية البلاغات / الكل / قيد المراجعة / تمت المراجعة | Filter reports / All / In review / Reviewed |
| `mine.meta({field, day})` / `.gone` | {field} · أُرسل {day} / لم تعد هذه المساحة معروضة في الدليل | {field} · Sent {day} / This space is no longer listed in the directory |
| `mine.more` / `.less` | عرض المزيد / عرض أقل | Show more / Show less |
| `mine.replySpace` / `.replyTeam` | ردّ إدارة المساحة / ردّ فريقنا | Reply from the space / Reply from our team |
| `mine.empty.title` / `.text` / `.browse` / `mine.none` | لم ترسل أي بلاغ بعد / إذا رأيت معلومة خاطئة في صفحة مساحة، أبلغنا منها. / تصفّح المساحات / لا توجد بلاغات هنا | You haven’t sent any reports yet / If you see wrong information on a space’s page, report it from there. / Browse spaces / No reports here |
| `mine.region` / `.loadFailed` / `.pagination` | البلاغات / تعذّر تحميل بلاغاتك / label «صفحات البلاغات» and the list's five words | Reports / We couldn’t load your reports / Pages of reports … |
| `site.account.navigation` / `.favorites` / `.reports` | حسابي / المفضّلة / بلاغاتي | My account / Favourites / My reports |
| `users.account.links` | favorites «المفضّلة» · reports «بلاغاتي» | Favourites · My reports |

- **Docs:** `data-reports.md` (*Who uses it*: a signed-in user's «بلاغاتي»; *Web decisions*: DI-53–DI-56);
  `users.md` (*Behaviour*: the site's account menu links the account's pages, P4); `architecture.md` §2 (the layout
  tree's `AccountLayout` built; *Built so far*: «بلاغاتي»); `overview.md`; `foundation.md` §13 screen 11's «ردّ
  فريق مساحة» → «ردّ فريقنا» (§14.8, once approved).

### PR 4 · Commit 2 — `feat(data-reports): report wrong information`
- **Repository:** `report(slug, body: CreateReportRequest): Promise<{ report: MyReport; repeated: boolean }>` —
  `apiClient.post(…)` and `unwrap` (S15): `repeated` is `status === 200`.
- **`hooks/intent/reportIntent.ts`** (a module store, as `directory`'s near-me store, S14): `holdReport(slug)`,
  `takeReport(slug): boolean` (true once).
- **`useReportAction({ slug, name, verified, signIn, openMyReports })`** → `{ trigger: { label; run }; dialog: {
  open: boolean; close(); view: ReportDialogView } }` — a guest (no user, the session not restoring): `holdReport(slug)`
  then `signIn('report')`; a user: opens; mounted with a session and `takeReport(slug)` → opens (C4, DI-61).
- **`useReportDialog({ slug, name, verified, openMyReports, onDone })`** → `{ title; description /* DI-45 */; field: {
  label; placeholder; options; value; choose; error }; message: { label; optional: string | null; helper; field;
  error }; back; submit: { label; run; busy; blocked }; failure }` — `useServerForm` over `createReportSchema`
  (`prepare`: a blank message left out); `fieldLines` (`field.required`, `message.required`); `failureLines`
  (`not_found` → `report.gone`, `network`/`timeout` → `report.lost`); 429 → the countdown; done → the toast (DI-47 or
  DI-48) with «عرض بلاغاتي» → `openMyReports`; `['me', 'reports']` invalidated.
- **`ReportAction({ slug, name, verified, signIn, openMyReports })`** (exported): «الإبلاغ عن معلومة غير صحيحة»
  (`Button variant="link" className="px-0"`) and `ReportDialog` (`Dialog`: header; a `form` with the field `Select`,
  the details `Textarea`, the failure `Alert role="alert"`, the footer «رجوع» (`DialogClose`, outline) and «إرسال»).
- **`SignInPrompt({ reason, onClose })`** (`pages/site/public/`): a `Dialog` titled and worded by `reason`
  (`'favorite' | 'report'`, DI-60); «إنشاء حساب» (outline `Link` to `SITE_PATHS.register?next=`) and «تسجيل الدخول»
  (primary `Link` to `SITE_PATHS.signIn?next=`), `next` the page's `pathname + search` (`URLSearchParams`).
- **`directory`:** `SpaceDetails` gains `report?: (space: { slug: string; name: SpaceNameView; verified: boolean }) =>
  ReactNode`, drawn last in the main column (`<div className="border-t border-border pt-6">`, U8).
- **`SpacePage`:** `const [prompt, setPrompt] = useState<'favorite' | 'report' | null>(null)`; `report={(space) =>
  <ReportAction … signIn={setPrompt} openMyReports={() => navigate(SITE_PATHS.myReports)} />}`; `<SignInPrompt
  reason={prompt} onClose={…} />`.
- **Words** (`dataReports.report`, `site.signInPrompt`):

| key | ar | en |
|---|---|---|
| `report.trigger` / `.title` | الإبلاغ عن معلومة غير صحيحة / الإبلاغ عن معلومة غير صحيحة | Report wrong information / Report wrong information |
| `report.toSpace({name})` / `.toTeam({name})` | بلاغك عن {name} يصل إلى إدارة المساحة، وتجد ردّها في «بلاغاتي». / بلاغك عن {name} يراجعه فريقنا، وتجد الردّ في «بلاغاتي». | Your report on {name} goes to the space’s management; you’ll find their reply in “My reports”. / Our team reviews your report on {name}; you’ll find the reply in “My reports”. |
| `report.field` / `.choose` / `.fieldRequired` | ما المعلومة غير الصحيحة؟ / اختر / اختر نوع المعلومة | What’s wrong? / Choose / Choose what’s wrong |
| `report.message` / `.optional` / `.helper` / `.messageRequired` | التفاصيل / اختياري / مثلًا: السعر الشهري أصبح 320 ₪ / اكتب ما الخطأ في «أخرى». | Details / Optional / For example: the monthly price is now ₪320 / Write what is wrong under “Other”. |
| `report.send` / `.back` / `.failed` / `.lost` / `.gone` | إرسال / رجوع / تعذّر إرسال البلاغ / لم يصل الرد. أعد المحاولة — لن يُرسَل البلاغ مرتين. / لم تعد هذه المساحة في الدليل. | Send / Back / We couldn’t send the report / No answer came back. Try again — the report won’t be sent twice. / This space is no longer in the directory. |
| `report.sentSpace` / `.sentTeam` / `.repeated` / `.showMine` | أرسلنا بلاغك إلى إدارة المساحة. ستجد ردّها في «بلاغاتي». / أرسلنا بلاغك إلى فريقنا. ستجد الردّ في «بلاغاتي». / أرسلت بلاغًا عن هذا من قبل، وما زال قيد المراجعة. / عرض بلاغاتي | We sent your report to the space’s management. You’ll find their reply in “My reports”. / We sent your report to our team. You’ll find the reply in “My reports”. / You already reported this, and it is still in review. / View my reports |
| `signInPrompt.favorite.title` / `.text` | سجّل الدخول لحفظ المساحات في المفضّلة / تجد المساحات التي تحفظها في حسابك على أي جهاز. | Sign in to save spaces to your favourites / The spaces you save are in your account on any device. |
| `signInPrompt.report.title` / `.text` | سجّل الدخول للإبلاغ عن معلومة / لتجد الردّ على بلاغك في «بلاغاتي». | Sign in to report information / So you’ll find the reply to your report in “My reports”. |
| `signInPrompt.register` / `.signIn` / `.close` | إنشاء حساب / تسجيل الدخول / إغلاق | Create account / Sign in / Close |

- **Docs:** `data-reports.md` (*Who uses it*: a signed-in user reports from a space's page; *Web decisions*: S14,
  S15, DI-44–DI-48, DI-60, DI-61); `directory.md` (*Web decisions*: decision 4's line revised — «the page's report
  button is `data-reports`', set by the page in its slot ({date}, #PRNUM)»); finding 168 (Open).

### PR 4 · Commit 3 — `feat(design-system): add the heart icon`
- `HeartIcon` (lucide `Heart`, not mirrored) in `icons/iconSet.tsx` and the icons' index, through the layer's `Icon`
  wrapper; a filled heart is the caller's `className="fill-current"` (§13 check 5.j). No words.

### PR 4 · Commit 4 — `feat(favorites): save a space from its card`
- **`favorites` repository:** `save(spaceId): Promise<undefined>` (`POST /me/favorites/{id}`), `remove(spaceId)`
  (`DELETE`) — no body, no key.
- **`hooks/intent/favoriteIntent.ts`** (module store): `holdFavorite({ spaceId, name })`, `takeFavorite(): { spaceId;
  name } | null`.
- **`useFavoriteToggle({ space: { id: number; name: SpaceNameView }, saved: boolean, signIn })`** → `{ pressed:
  boolean; label: string; run: () => void; busy: boolean }` — a guest → `holdFavorite` and `signIn('favorite')`;
  a user → `pressed` flips at once (held while pending, S13), the save or the removal sent once; done →
  `toast(favorites.added | .removed, { description: the name, action: «تراجع» → the inverse, sent once })`, `['me']`
  invalidated; failed → `pressed` back, `toast.error(favorites.saveFailed | .removeFailed, { action: «إعادة المحاولة»
  })`; `FAVORITES_LIMIT_REACHED` → `errors.FAVORITES_LIMIT_REACHED` with «إدارة المفضّلة» (the page's link);
  `not_found` → `favorites.gone`.
- **`useResumeFavorite()`** → with a session and a held favourite: saved once, said `favorites.savedOnReturn({
  name })` (a failure: the error toast with «إعادة المحاولة»); **`ResumeFavorite`** renders nothing and runs it;
  `SiteLayout` mounts it once.
- **`FavoriteButton({ space, saved, signIn, className })`** (exported): `Button variant="outline" size="icon"`,
  `aria-pressed`, `aria-label` «حفظ {name} في المفضّلة» / «إزالة {name} من المفضّلة», `HeartIcon` (filled,
  `text-primary`, when pressed), `bg-card shadow-floating` over a cover.
- **`directory`:** the repository's `favorites(request: { near?: NearPoint }): Promise<FavoriteSpace[]>` (`GET
  /me/favorites`; `sort=distance` and the `Masaha-Near` header with a point, as the list's); keys
  `favorites(request) = ['me', 'favorites', request]`; `useFavoriteIds(): ReadonlySet<number> | null` (null for a guest:
  the query `enabled` only with a user); `DirectorySlots.cardAction?: (space: { id: number; name: SpaceNameView; saved:
  boolean }) => ReactNode`; `SpaceCard` gains `action?: ReactNode`, drawn in a `relative` wrapper beside (never
  inside) the card's `Link`, `absolute end-3 top-3` over the cover; `DirectoryResults`, `DirectoryList`, `HomeSpaces`
  pass it; `SpaceHeader` gains `action?: ReactNode` beside the `h1` (`flex items-start gap-3`, PU-014);
  `SpaceDetails` gains `heart?: (space) => ReactNode`.
- **Pages:** `DirectoryPage`, `HomePage`, `SpacePage` set `cardAction` / `heart` with `FavoriteButton` and their
  `SignInPrompt` (one per page, its own state); `SiteLayout` mounts `ResumeFavorite`.
- **Words** (`favorites`, new section):

| key | ar | en |
|---|---|---|
| `save({name})` / `.remove({name})` | حفظ {name} في المفضّلة / إزالة {name} من المفضّلة | Save {name} to favourites / Remove {name} from favourites |
| `added` / `.removed` / `.undo` | أُضيفت إلى المفضّلة / أُزيلت من المفضّلة / تراجع | Added to favourites / Removed from favourites / Undo |
| `saveFailed({name})` / `.removeFailed({name})` / `.retry` | تعذّر حفظ {name} في المفضّلة / تعذّرت إزالة {name} من المفضّلة / إعادة المحاولة | We couldn’t save {name} to your favourites / We couldn’t remove {name} from your favourites / Try again |
| `savedOnReturn({name})` / `.gone` / `.manage` | حُفظت {name} في المفضّلة / لم تعد هذه المساحة في الدليل. / إدارة المفضّلة | {name} saved to your favourites / This space is no longer in the directory. / Manage favourites |

- **Docs:** `favorites.md` — header (*Scope*: the web feature, any page group; "not built" gone); *Who uses it*
  (the heart on the site's cards and page); *Behaviour* «**The heart on the web**»; *Web decisions*: S13, S14, DI-49,
  DI-50, DI-51, DI-61; code map *Web*; *Web history*. `directory.md` (*Behaviour*: the cards' and the page's slots,
  the saved ids; *Web decisions*: S13's read; code map). `architecture.md` §7 (S13: «`favorites`' save and removal
  invalidate the whole `['me']` scope, whose favourites list is `directory`'s ({date}, #PRNUM)»).

### PR 4 · Commit 5 — `feat(favorites): list a user's favourite spaces`
- **`directory`:** `useFavoritesView({ chooseArea, openMap })` → `{ count: string; near: { button; status } /* the
  directory's near-me views */; state: 'loading' | 'failed' | 'empty' | 'ready'; cards: SpaceCardView[] /* listed,
  saved */; unlisted: { key; id; name: SpaceNameView; line: string }[]; busy; failure; empty: { title; text; browse }
  }` — the favourites' key with the point while near me sorts; `FavoritesView({ spaceLink, areaName, cardAction,
  unlistedAction, browseLink, chooseArea, openMap })` (exported): the count (`aria-live="polite"`, `tabIndex={-1}`)
  and «الأقرب إليّ» in a row, the state line, a `grid gap-4 md:grid-cols-2 xl:grid-cols-3` of `SpaceCard`s with their
  action, then the spaces that left (`ul flex flex-col gap-4`, each a muted `Card` with the name, C7's line and
  `unlistedAction(space)`), the skeletons, the failure, the empty state (`EmptyState` with a heart and «تصفّح
  المساحات»).
- **`favorites`:** `RemoveFavorite({ space })` (exported): «إزالة» (outline) through `useFavoriteToggle` with `saved`
  true, its toast with «تراجع»; the focus after it (DI-52).
- **`FavoritesPage`** (`pages/site/account/`): the `h1` «المفضّلة» and its description; `FavoritesView` with
  `cardAction` (`FavoriteButton`), `unlistedAction` (`RemoveFavorite`), `chooseArea` → the Directory, `openMap` → the
  Directory's map (as Home's). Routes: `/me/favorites` under `AccountLayout`, `RequireAuth`; `ACCOUNT_LINKS` and the
  account menu gain «المفضّلة».
- **Words** (`favorites.list`):

| key | ar | en |
|---|---|---|
| `list.title` / `.description` | المفضّلة / المساحات التي حفظتها، بحالتها الآن. | Favourites / The spaces you saved, with their status now. |
| `list.count(n)` | zero «لا مساحات محفوظة» · one «مساحة واحدة محفوظة» · two «مساحتان محفوظتان» · few «{n} مساحات محفوظة» · many «{n} مساحة محفوظة» · other «{n} مساحة محفوظة» | one «1 saved space» · other «{n} saved spaces» |
| `list.gone` / `.remove` | لم تعد هذه المساحة معروضة في الدليل / إزالة | This space is no longer listed in the directory / Remove |
| `list.empty.title` / `.text` / `.browse` | لم تحفظ أي مساحة بعد / اضغط على القلب في صفحة أي مساحة لتجدها هنا. / تصفّح المساحات | You haven’t saved any spaces yet / Tap the heart on any space’s page to find it here. / Browse spaces |
| `list.loadFailed` / `.region` | تعذّر تحميل المفضّلة / المساحات المحفوظة | We couldn’t load your favourites / Saved spaces |

- **Docs:** `directory.md` (*What it does*: the favourites' screen built — the sentence "The favourites' screen and the
  space page's heart are not built" goes; *Behaviour* «**The favourites on the web**»); `favorites.md`;
  `architecture.md` §2; `overview.md`'s Favourites line; finding 168's *Evidence* names the heart too.

### PR 4 · Commit 6 — `feat(announcements): show a space's announcements`
- **`services/runningClosure.ts`** (pure): `runningClosure(items, now): PublicAnnouncement | null` — the first
  `CLOSURE` whose start ≤ now and whose end is none or after now.
- **`SpaceAnnouncements({ items })`** (exported): a section (`h2` «الإعلانات», the directory's `Section` look by
  classes) listing `AnnouncementItem`s by start, the running closure left out (DI-59); nothing when none is left.
  **`ClosureNotice({ items })`** (exported): the running closure as `Alert variant="warning"` — `AlertTitle` its text
  (`textOf`), `AlertDescription` `public.notice({ period })`; nothing without one.
- **`directory`:** `SpacePageView` carries `announcements: PublicAnnouncement[]`; `SpaceDetails` gains `notice?:
  (items) => ReactNode` (above the grid, U8: «the closure Alert stays at the top») and `announcements?: (items) =>
  ReactNode` (after the status card below 1024 px / the header from it, before the prices, U8).
- **`SpacePage`** sets both from `@features/announcements`.
- Words: `announcements.public` (commit 2's) — no new line.
- **Docs:** `announcements.md` (*Who uses it*: the site's space page; *Web decisions*: DI-59); `directory.md`
  (*What it does*: "the page's announcements are answered by the API, not shown on the site yet" goes; decision 4's
  line: the closure's notice built); `overview.md`; finding 131 → Resolved («#PRNUM: the space's page shows its
  running and upcoming announcements and a running closure's notice at the top»).

## 10. Tests — each with its lane, title and the break that must make it fail

Each new test is seen red first (testing §3.5), its red line recorded; that red step is its own break, and a
**separate** break is made only for a guard the red step did not prove (the owner's rule). For code that exists,
the break is made once, its red output recorded, then restored **from a backup copy** (never `git checkout`).
**Markers:** [role] a permission shown or hidden, [money] a money figure, [key] an idempotency key or a retry,
[state] loading, empty, failure, offline or a 409, [width], [a11y]. A width is proven in the component lane through
`useMediaQuery` and `stubScreenWidth` (`src/test/screenWidth.ts`); a layout drawn by classes alone is checked in
the real run with its own break (§13). Hooks are tested with `renderHook` through `fakeTransport`/`fakeAdapter`
(the platform's seam); components with Testing Library and `vitest-axe`; no `vi.mock` of a module.

### PR 1
| # | Lane · file | Title | Break |
|---|---|---|---|
| 1 | unit · `shared/lib/time/dayText.unit.test.ts`, `dayWord.unit.test.ts` (moved) | the existing cases, unchanged, from their new place | none: a move (the green run recorded) |
| 2 | unit · `deskRepository.unit.test.ts` (M) | voids a payment: its path, `{ reason }`, **no `Idempotency-Key`** [key] | a key added |
| 3 | component · `hooks/void/useVoidDialog.component.test.tsx` | **requires a reason; sends it once; the toast names the amount and who** [money] | a blank reason sent |
| 4 | same | **no answer says a retry is safe and nothing is re-sent by itself** [key] [state] | a key added (the transport re-sends: two requests) |
| 5 | same | **`VISIT_WRITTEN_OFF` and a 404 worded (the 404 reads the space again); a 403 shown by mistake says it is no longer open and reads `['me']`** [role] [state] | the 403's line left out |
| 6 | component · `components/void/VoidDialog.component.test.tsx` | **an alertdialog named by its title, the reason focused first, the action destructive, the failure an alert; axe-clean** [a11y] | `role="alert"` dropped |
| 7 | component · `components/void/VoidPaymentAction.component.test.tsx` | **the «⋯» and its menu named by the amount and who; the focus back on «⋯» after the dialog; once it is gone, `onGone`** [a11y] | `onCloseAutoFocus` left to Radix |
| 8 | component · `useStatement.component.test.tsx` (M) | **the owner gets the void on a payment not voided; reception none; a voided payment none** [role] | the void offered to reception |
| 9 | unit · `paymentsRepository.unit.test.ts` | reads a page and its totals with the query as parameters; a failure is an `AppError` | `meta` dropped |
| 10 | unit · `ledgerQueryOf.unit.test.ts` | **each filter by the contract's rule; half a range, an inverted one and 93 days dropped, 92 kept; voided `EXCLUDE` by default, `INCLUDE` on `voided=1`; no default written** | 93 days kept |
| 11 | unit · `periodText.unit.test.ts` (payments) | today; one day; a range in a month, across months, across years — Gaza dates read at UTC midnight | the browser's zone |
| 12 | unit · `paymentRowView.unit.test.ts` | **the day and the time on Gaza's clock; the customer, else the visitor, else «زائر»; a subscription's name; the amount in ₪; a voided one's badge and «ألغاها {name}: {reason}»** [money] | the voider's name left out |
| 13 | component · `useLedgerFilters.component.test.tsx` | a filter replaces the address and returns to page 1; **a range over 92 days says so and is not written**; clearing resets the range, staff, method, kind and the chip | the clear keeps the range |
| 14 | component · `useLedger.component.test.tsx` | **the totals line is `meta.totals` with its period first; a voided payment is never received** [money] | the totals summed from the rows |
| 15 | same | **loading; a failure with its reference and a retry; empty today; no match with «مسح الفلاتر»; a failed refresh keeps the rows; the rows kept and busy while the next page loads** [state] | one empty state for both |
| 16 | same | the staff options: all, the owner «(أنت)», the reception accounts, a deactivated one marked; choosing one sends `recordedById` [role] | the deactivated dropped |
| 17 | component · `PaymentsLedger.component.test.tsx` | **five columns from 768, cards at 390; the filters inline from 768, a sheet with its count at 390 (a range counted); axe-clean at 390 and 1440** [width] [a11y] | the sheet at 1440 |
| 18 | same | **when the focused row leaves, the focus goes to the next row's action, else the totals line** [a11y] | the keeper removed (focus on `body`) |
| 19 | component · `staff/hooks/people/useStaffPeople.component.test.tsx` | the reception accounts by name, a deactivated one marked, from the staff list's one request | a second request |
| 20 | component · `pages/dashboard/routes.component.test.tsx` (M) | «الدفعات» for the owner (reception the 403), «دفعاتي اليوم» for reception (the owner the 403), each titled [role] | the placeholder kept |
| 21 | component · `useMyPaymentsToday.component.test.tsx` | **the figures from `meta.totals`, the cash first, never summed; no range nor `recordedById` sent** [money] [role] | a range sent |
| 22 | same | loading, failure, empty («لم تسجّل أي دفعة اليوم»), a voided one struck with «ألغاها …» [state] | the voided one counted |
| 23 | component · `MyPaymentsToday.component.test.tsx` | **one card of three rows at 390, the transfer's helper there too; three StatCards from 768; axe-clean** [width] [a11y] | the helper dropped on a phone |
| 24 | unit · `shared/copy/catalogues.unit.test.ts` (existing) | the new sections' parity | (existing) |

### PR 2
| # | Lane · file | Title | Break |
|---|---|---|---|
| 25 | unit · `announcementsRepository.unit.test.ts` | the list (state, page), the summary; **the post with its key**; the edit's `PATCH` body; end, start, delete; the preview; **the extension with its key** [key] | the post's key dropped |
| 26 | unit · `periodText.unit.test.ts` (announcements) | the same day, two days, no end, another year; **08:00 in Gaza in summer and in winter** | `getHours()` (the browser's zone) |
| 27 | unit · `typeView`, `textOf`, `announcementsQueryOf` tests | `warning` for an outage and a closure; English falls back to Arabic, marked; `state` read, a wrong one falling back | a closure `neutral` |
| 28 | component · `useAnnouncementsList.component.test.tsx` | **the tabs' counts from the summary; the tab and the page in the address; the cards in the server's order** | the tab not in the address |
| 29 | same | **three skeletons while loading; failure; empty per tab; the pages only past one** [state] | pages always drawn |
| 30 | component · `AnnouncementsList.component.test.tsx` | **the tabs named, counts as badges, no status badge on a card, the type's tone; axe-clean at 390 and 1440** [a11y] [width] | a status badge |
| 31 | unit · `sheetRequest.unit.test.ts` | **Gaza's 08:00 to the right instant in summer and winter; «الآن» → no `startsAt`; no end → no `endsAt`; an edit sends only what changed, `textEn: null`, `endsAt: null`** | the browser's zone |
| 32 | component · `useAnnouncementSheet.component.test.tsx` | **one key for the post, the same after no answer and on a second press; a new opening a new key** [key] | `renew()` on each submit |
| 33 | same | **the server's `out_of_range` on `startsAt` and `endsAt` on their fields; `CLOSURE_EXTENDED` worded; a 403 worded; an unchanged edit sends nothing** [state] [role] | the field lines left out |
| 34 | same | **the toast names the tab it went to; «عرض» opens it** | the tab not named |
| 35 | component · `AnnouncementSheet.component.test.tsx` | **the checked type's radio focused first; the closure's line; the preview draws the public item; axe-clean** [a11y] | the focus on the group |
| 36 | component · `useAnnouncementActions.component.test.tsx` | **end now acts at once; its «تراجع» sends one `PATCH` with the old end; none for an extended closure; start now; nothing re-sent after no answer** [key] [state] | «تراجع» offered on an extended closure |
| 37 | same | **running: end; upcoming: start; ended: neither; «حذف…» never on an extended closure** [role] | delete offered on an extended closure |
| 38 | component · `useDeleteDialog.component.test.tsx` | **names the announcement and its true consequence by state; `CLOSURE_EXTENDED` worded; sent once** | one text for every state |
| 39 | component · `AnnouncementMenu.component.test.tsx` | **named by the announcement; the focus back on «⋯» after the dialog; the card gone, on the next card or the tabs** [a11y] | the focus on `body` |
| 40 | component · `useExtensionDialog.component.test.tsx` | **reads the preview on opening; the days prefilled; sends the typed days with one key, the same on a retry; a new opening a new key** [key] | the proposal sent instead of the typed days |
| 41 | same | **a failure stays in the dialog with the days kept; `CLOSURE_ALREADY_EXTENDED` worded and the list read again; none covered → no submit; applied meanwhile → its line** [state] | the dialog closed on a failure |
| 42 | same | **reception: no action, its line; a 403 (shown by mistake) worded** [role] | the action shown to reception |
| 43 | component · `ExtensionDialog.component.test.tsx` | an alertdialog named; the submit counts the subscriptions in Arabic's forms (1, 2, 3, 11, 100); axe-clean [a11y] | the count left out of the submit |
| 44 | component · `routes.component.test.tsx` (M) | «الإعلانات» for both roles, titled [role] | the placeholder kept |

### PR 3
| # | Lane · file | Title | Break |
|---|---|---|---|
| 45 | component · `FilterTag.component.test.tsx` | shows its label; the button named by `removeLabel`; a click and Enter remove; axe-clean | the name left out |
| 46 | unit · `dataReportsRepository.unit.test.ts` | the owner's list and decision, the admin's list and decision: paths, queries, bodies | the admin's path |
| 47 | unit · `reportView`, `reportsQueryOf`, `adminReportsQueryOf` tests | each field's word; the status by audience; **the day only, on Gaza's calendar**; no message's line; each filter read, a wrong one dropped | the time shown |
| 48 | component · `useSpaceReports.component.test.tsx` | **«زائر» for every report, never a name; the day only** [role] | the reporter named |
| 49 | same | loading, failure, empty, no match with «عرض الكل», the chips in the address; a decided report leaves «جديدة» and the toast says where [state] | one empty state |
| 50 | component · `useDecideSheet.component.test.tsx` | **«لم يُعتمد» with no reply focuses it with its line and sends nothing; «تم التصحيح» with none sends `{ status }` alone; sent once** | the reply required for both |
| 51 | same | **`REPORT_ALREADY_DECIDED` worded and read again; a decided report read-only; a 403 worded; the admin's verified report read-only with its link** [state] [role] | the buttons on a decided report |
| 52 | component · `DecideSheet.component.test.tsx` | the sheet named; «تعديل الحقل» a link; axe-clean at 390 and 1440 [a11y] [width] | the sheet unnamed |
| 53 | component · `SpaceReportsList.component.test.tsx` | five columns from 768, cards at 390 [width] | cards at 1440 |
| 54 | component · `useAdminReports.component.test.tsx` | **the reporter named; «يعالجه» per row; a verified space's report opens read-only; an unverified one decides** [role] | a verified one decidable |
| 55 | same | **the space and the field in force as removable tags at every width; removing one replaces the address; «مسح الفلاتر» clears both** [state] | the tags only in the sheet |
| 56 | component · `AdminReportsList.component.test.tsx` | cards until 1024, the table from it; the filters in a sheet below 768; axe-clean [width] [a11y] | `cardsBelow` dropped |
| 57 | component · `space-links/…/AdminSpaceFilter.component.test.tsx` | searches the server once typing pauses; «كل المساحات» clears; the chosen name shown | no clearing item |
| 58 | component · `routes.component.test.tsx` (M) | the space's reports (owner only), the admin's (admin only), each titled [role] | the placeholders kept |

### PR 4
| # | Lane · file | Title | Break |
|---|---|---|---|
| 59 | unit · `dataReportsRepository.unit.test.ts` (M) | «بلاغاتي»'s page; **a report's 201 is new, a 200 a repeat** | `repeated` always false |
| 60 | component · `useMyReports.component.test.tsx` | **a listed space a link; one that left, its name as text with C7's line; the reply labelled by `repliedBy`** | a gone space linked |
| 61 | same | the chips in the address, back to page 1; the first empty and the filtered one; loading, failure [state] | the page kept |
| 62 | component · `MyReportsList.component.test.tsx` | **a long message clamped with «عرض المزيد» (`aria-expanded`, `aria-controls`), a short one none; `dir="auto"`; axe-clean** [a11y] | the toggle always drawn |
| 63 | component · `pages/site/account/AccountLayout.component.test.tsx` | the navigation named «حسابي», the current link `aria-current`; a guest sent to sign-in with `next` (the route's `RequireAuth`) [a11y] [role] | `aria-current` dropped |
| 64 | component · `users`' `AccountMenu` / `AccountMenuSection` tests (M) | the site's links («بلاغاتي», «المفضّلة» from commit 5); none in the dashboard's menu | links in the dashboard's |
| 65 | unit · `reportIntent.unit.test.ts` | holds a slug; taken once; another slug not | taken twice |
| 66 | component · `useReportAction.component.test.tsx` | **a guest's press holds the intent and asks the sign-in with `report`; signed in, the dialog opens once; a link alone never opens it** [role] | the dialog opened for a guest |
| 67 | component · `useReportDialog.component.test.tsx` | **«أخرى» needs its details, the others not; `{ field, message? }` sent; 429 counted down; no answer keeps the input and says a retry is safe** [state] | the details always required |
| 68 | same | **the toast by verification with «عرض بلاغاتي»; a repeat says so** | one toast for both |
| 69 | component · `ReportAction.component.test.tsx` | the dialog named; U10's sentence; the failure an alert; the focus back on the button; axe-clean [a11y] | `role="alert"` dropped |
| 70 | component · `pages/site/public/SignInPrompt.component.test.tsx` | **its title and line by action; both links carry the page as `next`** | `next` dropped |
| 71 | component · `Icon.component.test.tsx` (M) | `HeartIcon` renders, never mirrored | mirrored |
| 72 | unit · `favoritesRepository.unit.test.ts`, `favoriteIntent.unit.test.ts` | the save's and removal's paths, no body, **no key**; the intent held and taken once [key] | a key header |
| 73 | component · `useFavoriteToggle.component.test.tsx` | **pressed at once and settled by the answer; the toast names the space with «تراجع», which sends the inverse once** | pressed only on the answer |
| 74 | same | **a failure flips it back with «إعادة المحاولة»; `FAVORITES_LIMIT_REACHED` and a 404 worded; nothing re-sent by itself** [state] [key] | the pressed state kept on failure |
| 75 | same | **a guest: the intent held, the sign-in asked with `favorite`, nothing sent** [role] | sent as a guest |
| 76 | component · `useResumeFavorite.component.test.tsx` | **once signed in, the held favourite saved once and said; a failure said with a retry; nothing without an intent** | saved twice |
| 77 | component · `FavoriteButton.component.test.tsx` | `aria-pressed`, named by the space, filled when pressed; axe-clean [a11y] | `aria-pressed` dropped |
| 78 | component · `useFavoriteIds.component.test.tsx` | read only with a session; the ids of listed and gone spaces | read for a guest |
| 79 | component · `SpaceCard.component.test.tsx` (M) | **the action stands beside the card's link, never inside it (one link, one button)** [a11y] | the action inside the link |
| 80 | component · `useFavoritesView.component.test.tsx` | newest saved first; near me sorts with the header; the gone ones after; loading, failure, empty [state] | the gone ones dropped |
| 81 | component · `FavoritesView.component.test.tsx` / `RemoveFavorite.component.test.tsx` | **«إزالة» with «تراجع»; the focus to the next row, else the next heart, else the count; axe-clean at 390 and 1440** [a11y] [width] | the focus on `body` |
| 82 | unit · `runningClosure.unit.test.ts` | a running closure; an upcoming one not; one ending at now not; none | `<=` on the end |
| 83 | component · `SpaceAnnouncements.component.test.tsx`, `ClosureNotice.component.test.tsx` | **the running closure the top notice, not repeated in the section; the others by start; English falls back to Arabic, marked; nothing with none** | the closure repeated |
| 84 | component · the space page's test (`pages/site/public/space/SpacePage.component.test.tsx`, A or M) | **U8's order: the notice first, the announcements after the status, the report last; the heart beside the `h1`** [a11y] | the report before the prices |
| 85 | unit · `catalogues.unit.test.ts` (existing) | the new sections' parity | (existing) |

### Review Focus — inputs no planned test exercises
- **PR 1:** a payment received at 23:59 in Gaza and listed «اليوم» or «أمس» after midnight; a 92-day range across
  the spring's clock change; a ledger page open while another tab voids one of its rows; an owner who is reception
  at another space (the role is the one in the URL); a renewal's allocated part voided (the other parts stay); a
  ₪100,000 amount's width at 390; reception's figures with only voided payments today (zeros, the struck rows).
- **PR 2:** a closure from 23:00 to 02:00 the next day (its Gaza days); two owners extending one closure from two tabs;
  a 500-character English text at 390; «تراجع» of an end now after another desk edited the end; deleting a running
  closure while the desk's top bar shows «مغلق الآن»; the preview's count changing between the dialog's opening and
  the apply (the preview is not a lock).
- **PR 3:** a space renamed after its report; a 500-character message; an owner linked while the admin's decision
  waits (403); the 200th report's page; the field link to a profile section that does not exist.
- **PR 4:** the 200th favourite (`FAVORITES_LIMIT_REACHED`); a saved space hidden meanwhile (its card leaves for the
  gone list); the guest flow through Google and through register; a report while a reception session ends idle; a
  heart pressed twice fast (two writes, each idempotent); the Arabic name of a space in the English interface in the
  heart's name and the toast.

## 11. Each PR's review focus (decision 5)

- **PR 1 — Claude review (money).** The void: sent once, no key, never retried by the transport; the reason
  required; the refusal lines (written-off, 404, 403); the focus after it. The ledger: every figure from `meta.totals`
  (search for a `reduce` over rows); a voided payment never in the received; the range's 92-day rule against
  `paymentsQuerySchema`; the query never sending `from`/`to`/`recordedById` for reception; the owner-only route and
  the reception-only route. The statement's void offered to the owner only. `dayText`/`dayWord` moved with no change.
- **PR 2 — Claude review (the extension moves subscriptions' ends).** The extension: the typed days sent (not the
  proposal), one key per opening, the failure kept in the dialog, `CLOSURE_ALREADY_EXTENDED` and S11's none-covered
  case, the owner only. The post's key per opening; S9's Gaza instants (summer and winter); the edit's minimal body;
  «تراجع» never offered where `CLOSURE_EXTENDED` would refuse it; S12's whole-space invalidation; the delete's texts.
- **PR 3 — a free model's review.** The reporter never named on the owner's side (types, rows, sheet); the day
  only; the decision's rules (`DISMISSED` needs a reply, a decided report read-only); the admin's verified reports
  read-only; `FilterTag`'s contract (no built-in words, logical classes, 44 px on touch); the address rules; the
  chips' mapping to `OPEN | DECIDED`.
- **PR 4 (4a, 4b) — a free model's review.** The guest's intent in memory only (nothing runs from a link); the
  heart's optimistic state and its rollback; `['me']` invalidated after a favourite; the report's 201/200; the
  account's guards; the card's action outside its link; the page's slots in U8's order; the site's first download
  (`check:build`) and, recorded, whether a site page's chunk pulls `data-table` (§13 check 5.k).

## 12. The commits

| PR | # | Subject (chars) | Body (why) |
|---|---|---|---|
| 1 | 1 | `refactor(lib): share the day's words` (36) | S7: the days' words get their second, third and fourth users |
| 1 | 2 | `feat(desk): void a payment` (26) | DK-016, ADR 0010 rules 3–5 on the web; S1's void, S10 |
| 1 | 3 | `feat(payments): list the space's payments` (41) | screen 17, the owner's ledger (S8, DI-1–DI-9) |
| 1 | 4 | `feat(payments): show reception its payments today` (49) | screen 17, «دفعاتي اليوم» (K4, DK-015) |
| 2 | 1 | `feat(announcements): list a space's announcements` (49) | screen 18's list (S2, O9) |
| 2 | 2 | `feat(announcements): post and edit an announcement` (50) | O9, O10's no end; the post's key (S4) |
| 2 | 3 | `feat(announcements): end, start or delete one` (45) | O10 (DI-16–DI-18) |
| 2 | 4 | `feat(announcements): extend after a closure` (43) | O11 on #123's API (S11, DI-19, DI-20) |
| 3 | 1 | `feat(design-system): add a removable filter tag` (47) | finding 8 (decision 4) |
| 3 | 2 | `feat(data-reports): decide a space's reports` (44) | screen 23, O12 |
| 3 | 3 | `feat(data-reports): list every space's reports` (46) | screen 28, A7, A8 |
| 4a | 1 | `feat(data-reports): show a user's own reports` (45) | screen 11, C7, P4's links |
| 4a | 2 | `feat(data-reports): report wrong information` (44) | U10, C4 (S14, S15) |
| 4b | 3 | `feat(design-system): add the heart icon` (39) | PU-014's heart |
| 4b | 4 | `feat(favorites): save a space from its card` (43) | PU-014, U12, C4 (S13, S14) |
| 4b | 5 | `feat(favorites): list a user's favourite spaces` (47) | screen 10, C7, C8, AC-014 |
| 4b | 6 | `feat(announcements): show a space's announcements` (49) | U8, finding 131 |

**PR titles:** PR 1 = commit 3's; PR 2 = commit 1's; PR 3 = commit 2's; PR 4a = commit 2's; PR 4b = commit 4's
(without A1, one PR 4 titled by commit 2's). **Recount each subject before committing (≤ 50)** — the table's counts
are the planner's; the executor's count decides. A unit's code, tests and documents in its commit. A fix before
the push folds into its commit (`git commit --fixup <sha>`, then `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash
origin/main`). No tool attribution. Stage by path; `git status` before each commit. **Carried items:** a
`C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\0_CARRIED_FROM_<n>.md` left by the previous PR's review is that
PR's first commit(s), each code fix red first, then green, with its break; the PR's description says "Carried
from #<n>". PR 1's carried file, if any, is #124's (`WORKER_A\_DONE\DESK_SCREENS\0_CARRIED_FROM_124.md`, should the
supervisor route it here).

## 13. The procedure and the verification

Work in `C:\dev\masaha\app` only — never in `C:\dev\masaha\app-b` (worker B) or `C:\dev\masaha\app-design`
(planners and reviewers read there). Each commit message is a UTF-8 file **without a BOM, LF endings**, with a body
saying why, committed with `git commit -F <file>`. Scripts in `C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\
scripts\`, never committed; screenshots in `…\PAYMENTS_STEP10\shots\pr<n>\` (`pr4a`, `pr4b` with A1), never
committed; the report `…\PAYMENTS_STEP10\4_REPORT_PR<n>.md`, written **as you go** (after the first checks, after
each commit — its sha, its subject with its length, the red line before the code, the green line after —, after each
break, each decision, the real run, the push, CI).

### First checks (before any edit), each PR
1. `git status --short` clean in `C:\dev\masaha\app`; `git fetch origin`; `git switch main`; `git pull --ff-only`.
2. **What must have merged:** PR 1: **#124** (`gh pr view 124 --json state` → `MERGED`); PR 2: PR 1; PR 3: PR 2;
   PR 4(a): PR 3; PR 4b: 4a. Not merged → under the autonomy rule this is the one thing the executor cannot decide:
   write it in the report and end (nothing can continue without its base).
3. **The base diff:** PR 1: `git diff --name-status e6737da5 origin/main`; later PRs: from the previous PR's merge.
   PR 4(a): also `git diff --name-status <PR 3's merge> origin/main -- apps/web/src/pages/site
   apps/web/src/features/directory apps/web/src/shared docs` (the public fix PR, decision 3): read every changed file
   this plan names before editing it, and add the slots to the code as it stands. Read the previous
   `4_REPORT_PR<n>.md` for its departures. `packages/shared` changed → `npm run build -w @masaha/shared` before any
   web check, and re-read `packages/shared/src/{payments,announcements,data-reports,favorites,directory,core}`
   against §9 — a difference is adapted to and recorded (§13, *Decide and record*).
4. **Open PRs:** `gh pr list --state open --json number,headRefName,files`; note each head for the conflict check;
   one that edits a code file of this PR → read its diff, keep away from its lines where possible, record it.
5. **Checks against the code, each with its fallback** (a fallback taken is a decision recorded):
   - a. PR 1: `git grep -l "services/day\(Text\|Word\)" apps/web/src` lists every importer (commit 1 moves them all).
   - b. PR 1: how the desk's repository passes a list's query to `api.getPage` (`params`); the ledger does the same.
     If `paymentsQuerySchema.shape` is not reachable on the refined schema, read each field by its own schema
     (`dateSchema`, `z.enum(PAYMENT_METHODS)`, …).
   - c. PR 1: `deskFailure` and `useDeskWrite` take what §9 gives them; `CustomerFile`/`SubscriptionCard`'s current
     props, to carry the void ability (an `abilities` object if they have one, else a `void` flag).
   - d. PR 1: the staff list's query key (`staffKeys`), so `useStaffPeople` shares its cache.
   - e. PR 1: `Calendar mode="range"` and `DatePicker` take what the ledger needs (the range's value, `lang`, the month
     buttons' names); `Intl.DateTimeFormat#formatRange` in Node 24 (jsdom's lane) — else two `dayText`s around «–».
   - f. PR 2: `gazaInstant` and `gazaClockOf` are exported from `@masaha/shared/core` (the web already imports
     `gazaClockOf`).
   - g. PR 2: `Input type="time"` in the component lane (jsdom keeps `HH:MM`); else a text input with `pattern` and
     `inputMode="numeric"`, `HH:MM` read by `minuteOf`.
   - h. PR 2: Radix's `RadioGroup` in a `Sheet` gives the first focus to the checked radio; else `onOpenAutoFocus`
     focuses it.
   - i. PR 3: the pill radius's token the `ToggleGroup` chips use (`rounded-(--radius-pill)` or the layer's class);
     `check:classes` allows it.
   - j. PR 4b: `fill-current` is a class `check:classes` allows and Tailwind emits; else the `Icon` wrapper's `fill`
     prop, if it passes SVG props.
   - k. PR 3 and PR 4: after the production build, whether the space page's chunk or «بلاغاتي»'s imports the
     `data-table` chunk (the manifest, statically). If it does → record a finding (the next free number) and go on:
     `check:build` guards the first download only.
   - l. PR 3: whether the owner's profile editor has section anchors (`#hours`, `#contact`, `#location`,
     `#amenities`); else the field links to the page alone.
   - m. PR 4: `unwrap`'s signature (the report's repository reads the status beside it); `RequireAuth` sends a guest
     to sign-in with the page as `next`; the register page carries `next` (`nextSearch`).
   - n. PR 4b: the directory's near-me store exposes what `FavoritesView` needs (the point for the header, the button
     and the line's views), as `HomeSpaces` uses it.
   - o. PR 4: `app/pageTitles.unit.test.ts` enumerates the routes it checks by hand — the new pages added there.
6. **Finding numbers:** the index's highest; this item's are 165 and on (165–168 planned, then one conditional);
   a number taken meanwhile → the next free ones, said.
7. **The data inventory (read-only, before any edit).** `docker start masaha-postgres-1` (never `npm run db:up`,
   never `npm ci`); `npx prisma migrate status` in `apps/api` — pending → `npx prisma migrate deploy` then `npx prisma
   generate` (worker A's `masaha_dev` to `main`); the API on 3320 (`npm run dev -w @masaha/api`). A script signs in
   (`POST /api/v1/auth/login`) as `demo-owner@example.com`, `demo-reception@example.com`,
   `demo-directory-owner@example.com` and the admin (their passwords from `apps/api/.env`, never printed or written),
   **and never keeps an `/auth/` request's body**, then reads with `GET`s only what this PR's real run needs: PR 1 —
   `masaha-demo`'s payments (today and the month), the seed's voided payment, a customer who owes (for the run's
   ₪1 payments) with a subscription and a visit; PR 2 — `masaha-demo`'s announcements and summary, its subscriptions
   running yesterday (the extension's preview count); PR 3 — the reports (none expected before the run's own), a
   verified space of `demo-directory-owner`'s and an unverified listed space (slugs); PR 4 — `GET /me/favorites` and
   `GET /me/reports` as `demo-reception`, the directory's spaces (one listed, verified; one unverified; the closure
   space). It records, for each case of the real run, the account and the record that holds it. Stop the API by its
   process id.
8. **Branch:** `git switch --no-track -c <branch> origin/main`.

### Per commit
`npm run lint` and `npm run typecheck`; the touched test files only (`npx vitest run --project <lane> <files>` in
`apps/web`); each new test seen red first, its red line recorded; each separate break of §10 made, its red output
recorded, then restored from a backup copy.

### On the head, once each
First: no `vitest`, `tsc` or dev server of `C:\dev\masaha\app-b\` runs —
`Get-CimInstance Win32_Process -Filter "Name='node.exe'" | Where-Object { $_.CommandLine -match 'app-b' }` empty
(else wait; never stop worker B's processes); then the free memory, recorded —
`(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory` — **before each full lane**; one full lane at a time.
Then: `npm run test:unit -w @masaha/web` · the scoped `npm run test:component -w @masaha/web -- <folders>`
(PR 1: `src/features/payments src/features/desk src/features/staff src/shared/lib src/pages/dashboard
src/shared/copy`; PR 2: `src/features/announcements src/pages/dashboard src/shared/copy`; PR 3:
`src/features/data-reports src/features/space-links src/shared/design-system src/pages/dashboard src/pages/showcase
src/shared/copy`; PR 4: `src/features/data-reports src/features/favorites src/features/directory
src/features/announcements src/features/users src/shared/design-system src/pages/site src/app src/shared/copy` — plus
any other folder whose files the PR changed, said) · `$env:NODE_ENV='production'; npm run build; Remove-Item
Env:NODE_ENV` · `npm run check:build` · `npm run check:classes` · `npm run format:check` · `npm run check:links` ·
`npm run check:conflicts`.
- **The first download, recorded** (the manifest: the entry and its static imports, bytes, base and head): no
  `features/payments` or `features/desk` module, no `data-table`, no `dashboard` chunk; PR 4: the site's first
  download's bytes before and after (the new any-group features are lazy). Check 5.k recorded.
- **Not run locally — CI judges:** the full `test:component` lane, `test:unit` of `apps/api` and `packages/shared`,
  `test:api` (no API or shared change). Reported under "Not run locally (CI judges)".
- **Finding 87's family** (`routes` › "lists the owner's eleven pages" and "lists reception's four pages", the two
  site tests opening `/spaces`, `App` › "renders the main landmark", `router` › "shows the root's general error…",
  `changePasswordPage` › "lands the user on the page they asked for…"): a local miss of only those, each passing
  alone → record both runs (times, free memory) and go on; CI judges.
- **Memory:** a run killed for low memory is re-run **once** when quieter; killed again → record it, carry on, CI's
  run of that lane on the pushed head judges.
- **Fix rounds** (after a review) run only the touched test files, `lint` and `typecheck` — never a full lane; CI
  judges (the owner's rule, 2026-10-26).

### The real run
- `docker start masaha-postgres-1`; the API on 3320; the web on 5320 (`npm run dev`), worker A's `masaha_dev`.
- **Browser:** local headless Chrome over CDP, a script in `scripts\` on the model of
  `WORKER_A\_DONE\DESK_SCREENS\scripts\run3.mjs` on `cdp3.mjs` (Enter sent with `text: '\r'`; **the script never keeps an
  `/auth/` request's body**). **Each role the PR serves; Arabic light and English dark; at 390, 768 and 1440** for
  every layout that changes with width (the ledger's table and cards and its filters' sheet, the handover's figures,
  the announcements' row and sheet, the reports' tables and cards, the admin's cards until 1024, the account's
  navigation, the favourites' grid, the space page's order). **The network log** of each case: every request's
  method, URL, status and `Idempotency-Key` (the proof that the post and the extension keep one key across a retry:
  CDP `Network.emulateNetworkConditions` offline for the first send, then online and «إعادة المحاولة» → two requests,
  one key, one record; and that the void, the reports, the decisions and the favourites carry none).
- **The writes, each named (and only these, §14.9):**
  - **PR 1:** as reception (`demo-reception`) at the desk — «استلام دفعة» ₪1 cash on a customer's subscription that
    owes, and ₪1 on a visit that owes (the inventory names both); then «دفعاتي اليوم» shows them; as the owner
    (`demo-owner`) — the ledger, its filters, its range; «إلغاء الدفعة…» of the visit's ₪1 from the ledger (reason
    «دفعة تجربة»), and of the subscription's ₪1 from its statement in the customer's file; as reception again —
    «دفعاتي اليوم» shows both struck, «ألغاها أحمد الشوا: دفعة تجربة».
  - **PR 2:** as reception on `masaha-demo` — a GENERAL «إعلان تجربة» now with no end; its English text added; «إنهاء
    الآن» then «تراجع»; «إنهاء الآن» again; «حذف…»; an OFFER «عرض تجربة» starting tomorrow 09:00, then «ابدأ الآن», then
    deleted; the post's offline retry (one key, one announcement). As the owner — a CLOSURE «إغلاق تجربة» starting
    yesterday 08:00, no end (the space reads «مغلق الآن» for the moments it runs), then «إنهاء الآن»; «تمديد
    الاشتراكات» → the preview (its days and count recorded); **the apply with 1 day** only if §14.9 allows it (it moves
    the covered seed subscriptions' ends by one day, with no undo); else the dialog shown and closed, test 40 owning it.
  - **PR 3:** **before the run, by a named script**, as `demo-reception` (a signed-in user): three reports through
    `POST /api/v1/spaces/:slug/reports` — on `masaha-demo` (HOURS, «تجربة: الساعات»), on a verified space of
    `demo-directory-owner`'s (PRICES), on an unverified listed space (OTHER, «تجربة: أخرى»); then as `demo-owner` —
    «بلاغات البيانات», «تم التصحيح» with the reply «صحّحنا الساعات»; as the admin — «بلاغات البيانات» with the space
    filter and its tag, the verified space's report read-only, the unverified one «لم يُعتمد» with a reply.
  - **PR 4a:** as `demo-reception` on the site — «بلاغاتي» (the three reports and their replies); a report from a
    space's page (AMENITIES on a verified directory space) with its toast; the same report again (the repeat line); as
    a guest — the report button → the prompt → «تسجيل الدخول» → back on the page with the dialog open, then closed
    unsent.
  - **PR 4b:** as `demo-reception` — the heart on a Directory card (saved, then «تراجع»), on Home, beside a page's name
    (saved); «المفضّلة» with «الأقرب إليّ» (a point set on the map, as the Directory's pick); «إزالة» with «تراجع»; as a
    guest — a page's heart → the prompt → sign-in → saved and said; the closure space's page shows its notice at the
    top and its other announcements after the status.
- **Width breaks in the real run** (layouts drawn by classes): PR 1 — the ledger's filters' grid's `md:grid-cols-2`
  removed once (the 768 shot shows one column), restored; PR 2 — the sheet's `sm:grid-cols-2` removed (the 768 shot
  stacks the date over the time); PR 4b — the favourites' `xl:grid-cols-3` removed. Each `break-<what>.png`.
- **Touch targets:** at 390 with touch emulation (`Emulation.setTouchEmulationEnabled`), the computed hit area of the
  ledger's «⋯», the heart, `FilterTag`'s button, the announcements' «⋯» ≥ 44 px, recorded.
- **Not performed, by design:** a 429 (the dialogs' tests own it); the extension's apply if §14.9 declines it; a
  `FAVORITES_LIMIT_REACHED` (200 saves); a lost answer on the void (its test owns it; the post's is shown live).
  Any other case the data cannot hold → decided under the autonomy rule (never by changing data through the app):
  recorded as not performed, with why.
- Screenshots `<pr>-<case>-<role>-<ar-light|en-dark>-<width>.png`. Stop the servers by process id
  (`Get-CimInstance Win32_Process -Filter "Name='node.exe'" | Where-Object { $_.CommandLine -match
  'C:\\dev\\masaha\\app\\' }`, `Stop-Process -Id …`); `Get-NetTCPConnection -LocalPort 3320,5320 -State Listen` empty;
  `git status --short` clean.

### Push and the PR
1. `git grep -n "#PRNUM" HEAD`; the next number: `gh pr list --state all --limit 1 --json number` + 1 **just before
   the push** (worker B may open first).
2. `#PRNUM` replaced per commit tree by a self-checking script in `scripts\` on the model of
   `WORKER_A\_DONE\DESK_SCREENS\scripts\prnum4.sh` (`git filter-branch -f --tree-filter …` over `origin/main..HEAD`, then
   `git update-ref -d refs/original/refs/heads/<branch>`; it fails unless `git grep -n "#PRNUM" HEAD` is empty and
   `git diff origin/main --stat` lists the same files as before). A backup branch first.
3. `git push -u origin <branch>`; `gh pr create --assignee @me --label feat --label area:web --label area:docs`
   (+ `--label area:design-system` on PR 3 and PR 4b), the title §12's; the description per workflow §3 (Summary;
   Scope / Acceptance criteria / Out of scope; Change type; Evidence — run and not run; Screenshots — attached by the
   owner from `shots\`; the Definition of Done; *Decisions taken without the owner*). **Compare the number `gh pr
   create` answered with the one in the commits;** if they differ, re-run the replacement with the right number and
   `git push --force-with-lease=<branch>:<the sha you pushed>` — the only force-push, on this branch only; recorded.
4. `gh pr checks <n>` green on the pushed head's SHA (`gh pr checks <n> --watch` bounded, or polled with `gh --jq`,
   never `jq`); `gh pr view <n> --json mergeStateStatus` → `CLEAN`. A red lane → its root cause, a fix folded into
   its commit, pushed again (`--force-with-lease` on this branch).
5. The conflict check: for each other open PR, `git fetch origin <its head ref>` and `git merge-tree --write-tree
   origin/<branch> origin/<other>`; recorded.
6. The report, written as you go, then summarised (the `final-report` skill where present). **Never merge.**

### Decide and record — the autonomy rule as it applies here
No stop until the PR is ready for review. **The executor decides alone, records each under *Decisions taken
without the owner* (what it met, the options, the choice and why, how to undo it), and continues:**
- a choice this plan leaves open, or a plan that proves false against the code (take the option that keeps the plan's
  intent, the documents' rules and v1 scope; the smaller, safer change first);
- a check of §13.5 that fails (its fallback, or the smallest equivalent);
- a break that stays green (make the break that can change the outcome — or note that the test was its own red step
  — and record it);
- a carried item larger than its file says (done, recorded);
- a `packages/shared` type changed by worker B meanwhile (adapt to it; never edit `packages/shared`);
- a real-run case the data cannot hold (not performed, with why);
- a file count past an estimate (reported, never a stop);
- a command or lane it cannot run (its root cause up to three tries; else under COULD NOT RUN with the exact error,
  the rest continues, CI judges).
**The limits it never crosses** (not decisions): merging, pushing to `main`, force-pushing another branch, creating
an Issue, deleting a remote branch; building anything on the *Not in v1* list; editing `apps/api`, `packages/shared`,
a migration, the seed, a dependency or `shared/copy/*/errors.ts`; resetting, reseeding or changing data through the
app to pass a case (the real run's writes are only §13's list); touching another worker's folder, database or ports;
skipping, `.skip`-ing or deleting a test, or weakening a config, timeout, lane or check; printing a secret, a token or
a demo phone number; tool attribution. **Never claim a result you did not see:** a command passed only if its own
output said so (its exit code); a break counts only when seen red; a scoped lane with failures is not green — name
each failing file and test.

## 14. Decisions needed from the owner

1. **The plan as written,** S1–S16 — above all **S1** (the features: the void stays `desk`'s, set by the payments page;
   the favourites' list and ids are `directory`'s, the heart `favorites`'), **S2** (architecture §3's naming rule gains
   `announcements`' exception), **S13** (the hearts read the whole favourites list once per signed-in visit) and
   **S14** (the guest's intent in memory only). *Recommend:* approve.
2. **A1 — PR 4 split in two** (4a ≈ 41 files, 4b ≈ 64). *Recommend:* take it. PR 1 (≈ 83) and PR 2 (≈ 73) stay whole (A1's reason).
3. **Finding 8:** build `FilterTag` in PR 3 (the admin's filters in force, DI-40), or close it as superseded by P5's
   sheet count (no tag, the admin's filters shown only in the toolbar and the sheet). *Recommend:* build it.
4. **P3's grouped navigation:** record finding 165 for an item of its own (recommended), or A4 — one shell commit in
   PR 1.
5. **S10 — the void in a subscription's statement too.** *Recommend:* take it.
6. **The design issues DI-1 … DI-61,** each as written (§7).
7. **The Arabic copy of §9,** every line (localisation › Catalogues).
8. **The documents this item changes or proves wrong:** architecture §2 (*Built so far*, `AccountLayout` built), §3
   (S2's line), §7 (S12's and S13's lines); foundation §12 (`FilterTag`'s row) and **§13 screen 11's «ردّ فريق
   مساحة» → «ردّ فريقنا»** (it reads as the space's team, PU-CP-005; the directory already says «فريقنا») — a line the
   owner approves before PR 4 changes it; foundation §13 screen 18's "the owner can then extend all active
   subscriptions by the closure days" → "the owner can then extend the subscriptions it covered, by the days typed,
   once" (decision 4, #123) — in PR 2; `OPEN_DECISIONS.md` point 2's *Built as (web)* line, the supervisor's (§9, PR 2
   commit 4).
9. **The real run's writes** (§13): PR 1's two ₪1 payments and their voids; PR 2's announcements and **whether the
   extension is applied with 1 day** on `masaha-demo`'s covered seed subscriptions (no undo; else not performed);
   **PR 3's three reports made by a named script** before its run (no screen makes them until PR 4; A2 is the other
   way); PR 4's report and favourites. *Recommend:* allow all, the extension included.
10. **The ledger's default period:** today (recommended, the API's default) or this month (A5).
11. **The reviews' split** (decision 5) with §11's focus lists — a Claude review for PR 1 and PR 2, a free model's for
    PR 3, 4a and 4b. *Recommend:* as written.

## Appendix — steps mapped to Claude Code skills (only a map; no step depends on them)

| Step | Skill (if present) |
|---|---|
| Before the branch | `start-work-item` (its git checks; the plan is already saved) |
| Each test red first; each break | Superpowers `test-driven-development` (with `writing-good-tests.md`), per workflow §10 |
| A failure or a flake | `systematic-debugging` |
| Claims in the report and the PR | `verification-before-completion` |
| Opening the PR, its self-review, a conflict with `main` | `open-pr` |
| After CI is green and `CLEAN` | `final-report` |
| The real run's screenshots | headless Chrome over CDP (`scripts\`), as DESK_SCREENS' |
