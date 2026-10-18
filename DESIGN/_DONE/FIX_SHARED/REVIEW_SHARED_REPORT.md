# Design review 1 — the shared layer (shells, navigation, page-level patterns)

Reviewer: design-review-shared · 2026-10-10 · read-only
Source: `git archive origin/main docs/design` (bcb2e04), served on `http://127.0.0.1:5340/`.
Evidence: `C:\Users\basel\Downloads\design-review-shared\SH-0nn.png` (one per issue; composite where a
pattern spans pages). Captured with headless Chrome at 390 (touch), 768 and 1440, Arabic and English,
light and dark.

## 1. Summary

1. **There is no single page-header pattern.** The page's action sits on its own row on desktop and in
   five different places on a phone. Sub-pages make a generic 17 px h1 and a bigger heading that is
   not the h1 (SH-001, SH-016).
2. **The dashboard says nothing when something fails.** The prototype has 0 error toasts, no pending
   button on any dashboard action, no error, offline or 403/404 state inside the dashboard, and no
   pagination on any list, against API contract §4 (SH-009, SH-010, SH-011). Weak connections are
   the product's main condition, so this matters most.
3. **There is no way between the site and the dashboard.** The site's account menu has no
   dashboard entry. The dashboard's menu holds only sign-out, so reception has no path to its own
   password or name (SH-004). The code's `AccountMenuContent` already has half of this.
4. **The shell takes room the daily work needs.** On a phone the public state and «ضبط الحالة» add
   one or two rows to the sticky top bar on every owner and reception page. The owner's sidebar is
   eleven ungrouped items. At 768 the rail hides which space you are in (SH-002, SH-003, SH-006).
5. **The same job is done in different ways.** Filters come in five forms. Confirm and undo follow
   no rule, and destructive confirmations are drawn as primary. «إلغاء» means Cancel, Void and Stop
   at once (SH-008, SH-013, SH-014). The tablet width was never on the board, and it is where tables
   break (SH-007).

## 2. Patterns (proposals that change many pages)

Each proposal is built from foundation §12 components. None needs a new design-system component,
except where stated.

### P1 · Page header: one place for the title, the way back and the actions (SH-001, SH-016)
- **Desktop and tablet:** the top bar holds `[title] [page actions: secondary…, primary last]` in
  `PageHeader`, as the code already places the title (architecture §2), then the shell's controls.
  The separate «actions» row in `main` goes.
- **Phone:** the page's primary action lives in the shell's fixed bottom bar (`bottomAction`, today
  on the desk and the overview only), at full width, on every page that has one. Secondary page
  actions (CSV export, for example) go in a «⋯» `DropdownMenu` in the top bar. The per-page
  `md:hidden` copies go.
- **Sub-pages** (customer file, space edit, and later any record): the h1 is the record's name, with
  a back link (`Breadcrumb`, its parent only) above it in the page. The generic title («ملف الزبون»,
  «تعديل مساحة») goes.
- **Pages:** Admin spaces, owners, users, space edit; Customers, Customer file, Staff, Announcements,
  Payments, Packages, Desk, Owner overview; `OwnerShell`, `AdminShell`.

### P2 · The space's public state is one control (SH-002)
`PublicStateBadge` and `StatusControl` merge into one button whose label is what visitors see
(«يظهر للزوار: ممتلئ يدويًا · 1:24»), drawn in the state's badge colour, with a chevron. It opens
the current popover, which also holds «العودة للحالة التلقائية» in place of the separate «إلغاء»
button. On a phone it shows the short form («ممتلئ · 1:24») inside the single top-bar row. All 12
owner and reception pages; `OwnerShell`.

### P3 · Navigation grouped by what people do (SH-003)
`SidebarGroup` with `SidebarGroupLabel`, which the layer already has:
- **Owner:** نظرة عامة · **اليوم:** مكتب الاستقبال، الزبائن، الدفعات · **المال:** المالية والتقارير،
  الباقات والأسعار · **المساحة:** ملف المساحة، الإعلانات، بلاغات البيانات · **الفريق والإعدادات:**
  الموظفون، الإعدادات.
- **Admin:** نظرة عامة · **المساحات:** المساحات، أصحاب المساحات، بلاغات البيانات · **المنصة:**
  المستخدمون، القوائم، سجل التدقيق، الإعدادات.
- **Reception** (4 items) needs no groups.

### P4 · One account menu, in every shell (SH-004, SH-005)
`AccountMenuContent` everywhere holds the name and role, then the email, and the items below.
- «لوحة التحكم» on the site, for a user with a dashboard. In the dashboard it becomes «الموقع العام».
- «إعدادات حسابي» (`/me`). On the site, also the favourites and «بلاغاتي».
- On a phone in the dashboard, the theme and language.
- «تسجيل الخروج».

On a phone the site header shows the avatar too. The language toggle stays visible in the phone
header, and the theme moves into the drawer.

### P5 · One filter bar (SH-008)
- **Search** is always visible.
- **Every other filter** is a labelled `Field`: inline from 768, and below that in the
  `FilterSheet` bottom sheet, with an active-count badge on its button.
- **The sheet's footer** follows the Directory's: a primary «عرض N نتيجة» and a ghost «مسح
  الفلاتر».
- **A single status filter** of four or fewer choices stays `ToggleGroup` chips.
- **The result count** sits by the toolbar, not only in the table's footer.
- **Pages:** Admin spaces, users, audit, reports; Customers, Payments, Finance, Data reports,
  Directory, so `FilterSheet` and the Directory sheet become one.

### P6 · Every list pages (SH-009)
`DataTable` with `Pagination` in its footer (20 per page, API contract §4), the summary
«1–20 من 312», and on a phone Previous and Next around the summary (foundation §12). Pages: Admin
spaces, owners, users, audit, reports; Customers, Payments, My payments, Desk › السجل, Staff, Data
reports, Announcements (ended).

### P7 · One set of states for every page that loads data (SH-010)
- **Loading:** `DataTable loading` or `Skeleton` in place of the content, never a blank page.
- **Error:** a destructive `Alert` in place of the content, saying «تعذّر تحميل …» with
  «إعادة المحاولة», as the Directory does now.
- **Offline, 404 and 403** inside the dashboard shell: the `EmptyState` of `Error.html`, with no
  actions (the sidebar is the way on), as `shared/routing` already builds them.
- **Pages:** every dashboard page, plus Favourites and Reports.

### P8 · Every action says it is working, it worked, or it failed (SH-011, SH-012)
- **While it runs:** the action's `Button` shows `loading`.
- **Success:** `toast.success`, saying what changed.
- **Failure:** in a dialog or sheet, a destructive `Alert` inside it, which stays open and keeps the
  input. On a page, `toast.error` with «إعادة المحاولة».
- **429:** a warning «محاولات كثيرة، حاول بعد … دقيقة».
- **On a page with a bottom bar,** toasts sit above the bar.

### P9 · Confirm or undo: one rule (SH-013, SH-014)
- **Reversible, affecting no one else:** act at once, then a toast with «تراجع» and no dialog.
  Examples: a favourite, hiding a space, archiving a customer, deleting a space (it is soft).
- **Irreversible, or felt by others:** an `AlertDialog`, and no undo after it. Examples: voiding a
  payment, suspending a user or staff, ending a subscription, unlinking the last owner.
  - The title is the verb and its object.
  - The body says the true consequence.
  - The action button repeats the verb, `variant="destructive"`.
  - The dismiss button is always «رجوع». «إلغاء» is the glossary's verb for voiding a payment
    (*Void a payment = إلغاء دفعة*), so it never also means Cancel.

### P10 · Save stays enabled (SH-015)
A section's «حفظ» is always enabled (foundation §10). A section with unsaved changes shows a caption
«تغييرات غير محفوظة» beside it.

## 3. Issues

### SH-001 · The page's action has no fixed place
- **type:** improvement · **level:** pattern · **impact:** high
- **where:**
  - Spaces — desktop 1440 · `http://127.0.0.1:5340/Admin%20spaces.html` ·
    `screens/43-admin-spaces/01-spaces-desktop-1440.webp`
  - Customers · owner — phone 390 · `Customers.html` ·
    `screens/26-customers-reception-vs-owner/04-customers-owner-phone-390.webp`
  - Staff list — phone 390 · `Staff.html` · `screens/37-staff-owner/02-staff-list-phone-390.webp`
  - Active · owner — phone 390 · `Announcements.html` ·
    `screens/38-announcements-owner-reception/02-active-owner-phone-390.webp`
  - Desk · reception — phone 390 · `Desk.html?role=reception`
- **evidence:** `SH-001.png`
- **what is wrong:** On desktop the shells render `actions` as a separate row at the far end of
  `main`. It is one button on a 56 px row, about 900 px from its title (the Announcements button
  sits far from its narrow content column). On a phone that row is hidden, and each page re-adds
  its button somewhere else:
  - Spaces: under the filters, auto width.
  - Customers: under the filters, full width.
  - Staff: under the intro text.
  - Announcements: under the tabs.
  - Owners and Staff: inside the DataTable toolbar.
  - Desk and Overview: a fixed bottom bar.

  So the main action moves on every screen.
- **proposal:** P1.
- **why it is better:** the user learns the place once. On a phone the action is in thumb reach and
  never scrolls away, and a row is saved on every page.
- **cost:** M
- **rule:** architecture §2 (`PageHeader` fills the bar); lens B2.

### SH-002 · The public state takes one to two extra rows of the sticky top bar
- **type:** improvement · **level:** pattern · **impact:** high
- **where:**
  - Override active — phone 390 · `Desk.html?override=full:84` ·
    `screens/31-batch-3a-fixes/06-override-active-1-24-phone-390.webp`
  - Desk · reception — phone 390 · `Desk.html?role=reception` ·
    `screens/21-front-desk-reception-vs-owner/02-desk-reception-phone-390.webp`
  - 768: no frame.
- **evidence:** `SH-002.png`
- **what is wrong:** Below `lg`, `OwnerShell` wraps the badge and the control onto a second row of
  the sticky header: 112 px at 390. A running override adds a third row (the «إلغاء» button): 140 px.
  With the bottom bar, about 180 px of an 844 px screen is fixed chrome. The badge and the button
  also show the same fact twice. The shell mounts `StatusControl` twice, once for wide screens and
  once for narrow ones, so `?status=open` opens two popovers.
- **proposal:** P2.
- **why it is better:** one control reads as «this is what visitors see; tap to change it». The
  reception's phone gets its list back.
- **cost:** S–M
- **rule:** BRIEF.md («top-bar public state badge + «ضبط الحالة»») becomes one element; ADR 0008
  unchanged.

### SH-003 · The owner's navigation is eleven flat items
- **type:** improvement · **level:** pattern · **impact:** medium
- **where:** Desk · owner — desktop 1440 · `Desk.html` ·
  `screens/21-front-desk-reception-vs-owner/03-desk-owner-desktop-1440.webp`; the Admin sidebar in
  any admin frame.
- **evidence:** `SH-003.png`
- **what is wrong:** Daily tasks (desk, customers, payments) sit at the same level as monthly ones
  (packages, staff, settings), in no visible order. The admin's eight items mix content with
  platform.
- **proposal:** P3.
- **why it is better:** the owner finds today's work in the first group. The labels make 11 items
  scannable, and on the rail they stay for assistive technology.
- **cost:** S
- **rule:** lens B7.

### SH-004 · The account menus lead nowhere: no site ↔ dashboard, no account settings in the dashboard
- **type:** defect · **level:** pattern · **impact:** high
- **where:**
  - Home · signed in — desktop 1440 · `Home.html?loc=none&auth=1` ·
    `screens/14-account-signed-in-header/01-home-signed-in-desktop-1440.webp`
  - Home · signed in — phone 390 · `Home.html?loc=none&auth=1`
  - Desk (any): the account menu.
- **evidence:** `SH-004.png`
- **what is wrong:**
  - The site's `UserMenu` lists favourites, reports, settings and sign-out, with no entry into the
    dashboard. An owner or the admin who lands on the site has no way in.
  - `OwnerUserMenu` and the admin's menu hold only sign-out. Reception has no settings page, so it
    has no path to change its password or name. The owner reaches it only through a card at the
    bottom of Owner settings.
  - The admin's sidebar has no «view the site» link.
  - On a phone, the site header gives no sign of being signed in (the avatar is `hidden md:inline-flex`).
- **proposal:** P4. The code's `AccountMenuContent` already has the dashboard entry; add the way back
  and the account settings.
- **why it is better:** every role reaches its other area and its own account from the same place.
- **cost:** S
- **rule:** architecture §2 (*the site's shell … or the account once signed in*); foundation §13 #9.

### SH-005 · Language on a phone: one level down on the site, missing in the dashboard
- **type:** defect · **level:** pattern · **impact:** medium
- **where:** Home — AR light · phone 390 · `Home.html?loc=none` · `screens/01-flow/01-1-home.webp`;
  Desk · owner — phone 390 · `Desk.html`, with the drawer open.
- **evidence:** `SH-005.png`
- **what is wrong:**
  - The dashboard's phone drawer has no language toggle at all. `OwnerShell` and `AdminShell` hide
    it below `md` and add it nowhere, so a phone user cannot switch. The code already puts it in
    the drawer's foot.
  - On the site, the phone header shows the theme but not the language. A non-Arabic reader has to
    find «القائمة» to learn there is English.
- **proposal:** phone header: menu, wordmark, language (`LanguageToggle`, short label). The theme
  moves into the drawer and the account menu (P4). In the dashboard, language and theme go in the
  drawer's foot and the account menu.
- **why it is better:** language decides whether anything else can be read; the theme does not.
- **cost:** S
- **rule:** foundation §8 (direction follows language); architecture §2 (on a phone the drawer holds
  the language).

### SH-006 · The tablet rail hides which space you are in
- **type:** defect · **level:** component · **impact:** medium
- **where:** no frame (the board has no 768 frame) · `Desk.html` and `Desk.html?lang=en` at 768.
- **evidence:** `SH-006.png`
- **what is wrong:** At 768–1023 the rail starts directly with the first page's icon. The space
  switcher's mark is gone, and so is its name. The top bar does not name the space either, so an
  owner of two spaces cannot tell or change which one they are working in.
- **proposal:** the rail shows the space's mark as the switcher's trigger, named
  «تبديل المساحة — Focus Hub», with a tooltip. It opens the same `DropdownMenu`. Use `SidebarHeader`
  with its `mark` and `SidebarText`, as the code's layer does. The admin's rail shows the «م» mark.
- **why it is better:** the space is the context of every number on the page.
- **cost:** S
- **rule:** foundation §12 Sidebar (`SidebarText` kept for assistive technology on the rail).

### SH-007 · Tables at 768 are cramped, cut and wrap always-LTR values
- **type:** defect · **level:** pattern · **impact:** medium
- **where:** no frame · `Admin spaces.html` and `Customers.html` at 768 (also `Payments.html`, the
  Desk's present table).
- **evidence:** `SH-007.png`
- **what is wrong:**
  - Seven columns beside the rail, in about 640 px.
  - Space names wrap to three lines.
  - The row menu «⋮» touches the card's edge.
  - Phone numbers break mid-number («+970 59 / 000 1001»), against foundation §8.
- **proposal:** each page names a column priority. Below `lg` a DataTable shows at most five
  columns, and the rest go into the card form or the row's detail. A table with more columns uses
  the card form below `lg`. Every `dir="ltr"` value in a cell is `nowrap`, like `Num`.
- **why it is better:** a front-desk tablet is a likely device. Today it gets the worst layout.
- **cost:** M
- **rule:** foundation §9: «Tables become stacked cards» only on phones (see *Rules in doubt*).

### SH-008 · Filters do the same job in five forms
- **type:** improvement · **level:** pattern · **impact:** medium
- **where:**
  - Spaces — phone 390 · `Admin spaces.html`
  - Customers · owner — phone 390 · `Customers.html`
  - Users — phone 390 · `Admin users.html` · `screens/46-admin-users/02-users-phone-390.webp`
  - Audit log — phone 390 · `Admin audit.html`
  - All reports — phone 390 · `Admin reports.html`
  - 2 · Directory — list · `Directory.html?loc=none`
- **evidence:** `SH-008.png`
- **what is wrong:**
  - Admin spaces puts labelled Fields in `FilterSheet`.
  - Customers puts unlabelled Selects in it (aria-label only). Once one is chosen, «شهري» no longer
    says what it filters.
  - Users and Audit always show their fields inline, so on a phone three stacked fields push the
    list about 260 px down (foundation §9: phone filters open in a bottom sheet).
  - The Directory has its own sheet, with a different footer (the count in the button, «مسح» under
    it) and a different breakpoint (`lg`, against `md`).
  - The result count sits in the table footer, after the list.
- **proposal:** P5.
- **why it is better:** one way to filter everywhere. The list starts high on a phone, and the count
  answers «did my filter work?» where the user looks.
- **cost:** M
- **rule:** foundation §9; finding 8 (the applied-filter tag) is still open.

### SH-009 · No list paginates
- **type:** defect · **level:** pattern · **impact:** high
- **where:** Ledger · this month — desktop 1440 · `Payments.html` ·
  `screens/32-payments-owner/01-ledger-this-month-desktop-1440.webp`; Audit log — desktop 1440 ·
  `Admin audit.html`.
- **evidence:** `SH-009.png`
- **what is wrong:** `Pagination` is used on no page. The payments ledger, audit log, users,
  customers and the desk's log draw every row at once. The API pages every list (`?page&limit`,
  default 20, max 50), so a design without pages cannot be built as drawn. It also loads too much on
  a weak connection.
- **proposal:** P6.
- **cost:** M
- **rule:** API contract §4; foundation §12 Pagination and DataTable.

### SH-010 · The dashboard has no error, offline, 403 or 404 states, and few loading ones
- **type:** defect · **level:** pattern · **impact:** high
- **where:**
  - Customers · loading — phone 390 · `Customers.html?state=loading`
  - Loading — phone 390 · `Directory.html?loc=none&state=loading`
  - `Directory.html?loc=none&state=error`
  - `Error.html?type=offline` (site only)
- **evidence:** `SH-010.png`
- **what is wrong:** Loading is designed on four dashboard pages (Customers, Desk, Payments, My
  payments). No dashboard page has a load-error or offline state; the public site has both. The
  route-level 404, 403 and offline states are drawn only in the site's shell. A reception phone
  that loses the connection mid-shift shows nothing useful.
- **proposal:** P7.
- **cost:** M
- **rule:** foundation §13 («States: default, loading, empty, error»); architecture §2 (status states
  inside each shell).

### SH-011 · No action shows that it is waiting or that it failed
- **type:** defect · **level:** pattern · **impact:** high
- **where:** every dashboard action, for example Desk · check-in and check-out
  (`Desk.html?dialog=checkout&pid=pv0`), Staff · add (`Staff.html?sheet=add`), Payments · void
  (`Payments.html?void=1`).
- **evidence:** `SH-011.png`
- **what is wrong:** The source has 29 `toast.success` calls, 14 plain `toast` calls and 0
  `toast.error`. `Button loading` appears only on the auth pages and account Settings. The «too many
  requests» line appears only on four auth and account pages, but every endpoint may answer 429. A
  slow check-in invites a second tap, and a double check-in follows.
- **proposal:** P8.
- **cost:** M
- **rule:** foundation §10 (a button is disabled while its request is in flight); API contract §3;
  lens A8 and B6.

### SH-012 · A phone toast covers the bottom bar's primary action
- **type:** defect · **level:** design system · **impact:** medium
- **where:** Desk · reception — phone 390 · `Desk.html?role=reception&toast=welcome`. Any success
  toast after a check-in does the same.
- **evidence:** `SH-012.png`
- **what is wrong:** `Toaster position="bottom-center"` sits on top of «تسجيل زيارة» for 5 s, exactly
  when the next visitor is waiting.
- **proposal:** the layer's `Toaster` takes an offset (or a `top-center` position on phones), and the
  shell sets it while a `bottomAction` is shown.
- **why it is better:** feedback never blocks the next action.
- **cost:** S
- **rule:** —

### SH-013 · Confirm and undo follow no rule; destructive confirmations are drawn as primary
- **type:** defect · **level:** pattern · **impact:** medium
- **where:**
  - Delete (soft) — desktop 1440 · `Admin spaces.html?del=palm` ·
    `screens/43-admin-spaces/09-delete-soft-desktop-1440.webp`
  - Void a payment — desktop 1440 · `Payments.html?void=1`
  - `Customers.html?archive=m6`
  - `Staff.html?stop=1`
  - `Admin users.html?suspend=…`
- **evidence:** `SH-013.png`
- **what is wrong:**
  - **Confirm and undo:**
    - Delete a space has both a confirmation and an undo toast; so does archive a customer.
    - Hide a space has neither.
    - Remove a favourite has undo only; suspend has a confirmation only.
  - **Destructive look:** no `AlertDialogAction` passes `variant="destructive"`, so delete,
    suspend, archive and unlink are teal primary buttons. Only the void (a plain `Dialog`) is red.
  - **Button order:** the void dialog puts its buttons the other way round (destructive first, then
    «رجوع») from every `AlertDialog` (Cancel first, then Action).
- **proposal:** P9.
- **why it is better:** the user learns that red means «this cannot be taken back», and is not asked
  twice for what can be undone.
- **cost:** S–M
- **rule:** foundation §12 (AlertDialog: confirmations); lens B6.

### SH-014 · «إلغاء» means Cancel, Void and «stop the override»
- **type:** defect · **level:** pattern · **impact:** medium
- **where:** `Payments.html?void=1`; `Admin spaces.html?del=palm`; Override active · phone 390 ·
  `Desk.html?override=full:84`.
- **evidence:** `SH-014.png`
- **what is wrong:** The glossary makes «إلغاء دفعة» the term for voiding. The same word is the
  dismiss button of seven confirmations (Admin spaces, Admin users, Staff, Customers, Settings), and «إلغاء» with an ✕ ends a manual state. In the void dialog a
  cashier sees «إلغاء الدفعة» next to what other dialogs call «إلغاء».
- **proposal:**
  - Dismiss buttons say «رجوع» everywhere, as Customer file and the void dialog already do.
  - The override ends with «العودة للحالة التلقائية», inside the P2 popover.
- **cost:** S
- **rule:** glossary (*Void a payment*); lens A10.

### SH-015 · Save buttons are disabled until something changes
- **type:** defect · **level:** pattern · **impact:** low
- **where:** Owner settings — desktop 1440 · `Owner settings.html` ·
  `screens/40-settings-owner/01-owner-settings-desktop-1440.webp`; Admin settings; the space-profile
  sections (`profile-a.jsx`, Admin space edit, Owner space profile); the Announcements extend
  dialog.
- **evidence:** `SH-015.png`
- **what is wrong:**
  - `disabled={!dirty}` draws the save button pale, with no reason shown.
  - Account Settings keeps its save button enabled, so the two settings pages disagree.
- **proposal:** P10.
- **cost:** S
- **rule:** foundation §10 (submit buttons stay enabled).

### SH-016 · Sub-pages: the h1 is generic and small, and the real title is not a heading
- **type:** improvement · **level:** pattern · **impact:** medium
- **where:** Edit unverified · banner — desktop 1440 · `Admin space edit.html?id=golden` ·
  `screens/43-admin-spaces/11-edit-unverified-banner-desktop-1440.webp`; Memberships · partly paid —
  desktop 1440 · `Customer file.html?id=m6` ·
  `screens/27-customer-file/01-memberships-partly-paid-desktop-1440.webp`.
- **evidence:** `SH-016.png`
- **what is wrong:**
  - Space edit: the h1 «تعديل مساحة» is 17 px, and the h2 «Golden Hub» under it is 30 px, so the
    visual order inverts the outline.
  - Customer file: the h1 is «ملف الزبون», and the customer's name is a 22 px `div`.
  - On both, the title is said three times: the top bar, the breadcrumb and the card.
- **proposal:** P1 › sub-pages.
- **cost:** S
- **rule:** foundation §7 (`heading-1` page titles); lens A3.

### SH-017 · The auth pages have no heading
- **type:** defect · **level:** component · **impact:** medium
- **where:** Sign in · default — phone 390 · `Sign in.html` ·
  `screens/06-sign-in/02-sign-in-default-phone-390.webp`; also Register, Forgot password, Reset
  password, Change password.
- **evidence:** `SH-017.png`
- **what is wrong:** `AuthShell` has no h1, and the page title is a `CardTitle`, which is a `div`.
  Each page has 0 h1 and 0 h2, so a screen reader finds no title.
- **proposal:** the auth card's title is the page's h1. Give the layer's `CardTitle` an `as` or
  heading-level prop (level: design system), as `EmptyState` already has (`titleAs`).
- **cost:** S
- **rule:** foundation §10.

### SH-018 · No skip link; 17 tab stops before the page in the dashboard
- **type:** defect · **level:** pattern · **impact:** medium
- **where:** `Desk.html` (all dashboard pages); every site, account and auth page.
- **evidence:** `SH-018.png`
- **what is wrong:** A keyboard user goes through the switcher, 11 menu items, the public-page link,
  the state, the language, the theme and the account before reaching the desk's search, every page
  load.
- **proposal:** a «تخطَّ إلى المحتوى» link as the first focusable element of each shell, visible
  only on focus, leading to `main`. It is a `Button variant="link"`, so no new component is needed.
- **cost:** S
- **rule:** foundation §10 («full keyboard use in dashboards»).

### SH-019 · The English copy says «membership»; the glossary says «subscription»
- **type:** defect · **level:** pattern · **impact:** low
- **where:** Customers · English · `Customers.html?lang=en` ·
  `screens/52-dashboard-variants-phone-390/08-customers-english.webp`. About 50 occurrences in
  Customers, Customer file, Announcements, Packages, Payments, Finance, Overview, `desk-core.jsx`,
  `desk-sheet.jsx` and `desk-data.js`.
- **evidence:** `SH-019.png`
- **what is wrong:** «Current membership», «New membership», «No membership», «memberships
  extended». The glossary says *Subscription — replaces Membership*. The Arabic («اشتراك») is right.
- **proposal:** replace every English «membership» with «subscription».
- **cost:** S
- **rule:** glossary.

### SH-020 · The site's account-menu items are drawn as links
- **type:** defect · **level:** component · **impact:** low
- **where:** Home · signed in — desktop 1440 · `Home.html?loc=none&auth=1`, with the menu open.
- **evidence:** `SH-020.png`
- **what is wrong:** The prototype's global `a{color:var(--primary)}` turns the three menu items
  teal, while «تسجيل الخروج», a button, stays in the text colour. One menu shows two kinds of items.
- **proposal:** menu items always take the menu's own colour. The fixer checks whether the layer's
  `DropdownMenuItem asChild` with a link keeps it.
- **cost:** S

### SH-021 · SpaceCard repeats its price note on every card, and a missing price looks louder than a price
- **type:** improvement · **level:** component · **impact:** low
- **where:** 2 · Directory — list · `Directory.html?loc=none` ·
  `screens/01-flow/02-2-directory-list.webp`; also Home and Favourites.
- **evidence:** `SH-021.png`
- **what is wrong:**
  - «للعرض فقط · الدفع في المساحة» is repeated on each of six cards, a line each.
  - An unoffered period is an outlined white box with «—», which catches the eye more than the
    `muted` boxes holding prices.
- **proposal:**
  - The note goes once in the list's header line («6 مساحات · الأسعار للعرض فقط · الدفع في
    المساحة»), and in the map's selected card.
  - Each card keeps «آخر تحديث …» and the «قد يكون تغيّر» badge.
  - The empty cell takes no border and muted text, like a filled one with no value.
- **cost:** S
- **rule:** BRIEF.md (the display-only line); foundation §5 (warning is never text alone; kept).

### SH-022 · Skeletons are barely visible on a light card
- **type:** improvement · **level:** design system · **impact:** low
- **where:** Loading — phone 390 · `Directory.html?loc=none&state=loading` ·
  `screens/03-directory-views-states/24-loading-phone-390.webp`.
- **evidence:** `SH-022.png`
- **what is wrong:** `muted` (n-100) on `card` (white) is about 1.1:1, so a loading list reads as
  empty white cards. That is the state users on a weak connection see longest.
- **proposal:** the layer's `Skeleton` uses a fill a step stronger on a card (a component token,
  from n-200 in light). Dark is fine.
- **cost:** S
- **rule:** foundation §4 (component tokens).

## 4. Rules in doubt

1. **foundation §5, Status: «`destructive` … Space full».** The prototype draws Full as `warning` and
   Closed as `neutral`, and it is right. Full is not an error, and red beside «متاح» reads as
   «forbidden» and alarms. Propose: Full = `warning`, Closed = `neutral`.
2. **foundation §9: «Tables become stacked cards» on phones only; the tablet gets the full table
   beside a rail.** At 768 the content is about 640 px, too narrow for the 6–7-column tables (SH-007).
   Propose: cards below `lg` for a table with more than five columns, or a column priority per page.
3. **foundation §13 and the board: «Every screen: phone and desktop».** No 768 frame exists, and the
   tablet is where the shell (SH-006) and tables (SH-007) break. Propose: the shells and every list
   page are also checked at 768 in the fix phase.
4. **BRIEF.md: «top-bar public state badge + «ضبط الحالة»» as two elements** — see P2. (BRIEF is the
   archive's brief, not an authoritative document; listed so the change is not silent.)

## 5. Not reviewed

- **The pages' own content** (later reviews), one line each:
  - Owner overview shows the public state twice: the bar and the occupancy card.
  - Customer file has a five-button action row.
  - The Desk's «زبون جديد» is an extra full-width row on a phone.
  - The Directory filter sheet offers «يومي» as a price period.
  - The long single-page Admin space edit form has per-section saves.
  - The Announcements list column is narrow on desktop.
- **The design system's components themselves:** `/__showcase` was not opened; only their use in the
  prototype was judged.
- **Visible focus** was not verified. A focus set from a script in headless Chrome does not trigger
  `:focus-visible`, so the ring needs a real keyboard check. No screen-reader pass was made; headings
  and the tab order were read from the DOM.
- **The map**, the location flows and the email template (public and auth reviews).
- **The archive's known limits** (placeholder icons, such as two eye icons on the rail; sample data;
  the Roboto fallback; the three superseded frames) were not reported.
