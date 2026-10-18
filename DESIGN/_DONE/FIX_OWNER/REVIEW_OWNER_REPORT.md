# Design review 5 — the owner's management (Overview, Announcements, Finance, Space profile, Prices & packages, Staff, Data reports, Settings)

Reviewer: design-review-owner · 2026-10-11 · read-only
Source: `git archive origin/main docs/design` (b66ddfe), served on `http://127.0.0.1:5344/`.
Evidence: `C:\Users\basel\Downloads\design-review-owner\OW-0nn.png` (one per issue). Captured with
headless Chrome at 390 (touch emulated), 768 and 1440, in Arabic and English, light and dark. Also a
keyboard and naming pass on each page (focusable controls, their names, the heading outline). Sources
read: `owner.jsx`, `owner-data.js`, `profile-a.jsx`, `profile-b.jsx`, `finance.jsx`, the eight owner
pages, and `Admin space edit.html` for the comparison. I checked against: the API contract and the
plan's *Managed spaces* rows, `schema.prisma`, `data-model.md`, ADRs 0008/0009/0010,
`features/spaces.md`, foundation §5/§7–§13, the glossary and `overview.md`.

## 1. Summary

1. **The owner's Space profile is a second editor for the same facts, and it disagrees with the
   first.** It has eight cards with eight confirms. «الأساسيات» and «الموقع» are confirmed apart, yet
   they are one group in the API. Photos and capacity carry a «آخر تحديث» and «ما زالت صحيحة» that no
   endpoint serves. Prices are a stub that points away. The fix is to build it as **the admin's A1
   editor**, with the differences that verification brings named once (OW-001, OW-006).
2. **Private operating values sit on the page that promises "everything here shows to visitors."**
   Capacity (ADR 0008: private) and the stay limit sit under «السعة ومدة الجلوس» on the profile. The
   stay limit's helper even says «يظهر في قواعد المساحة», a public "space rules" page that does not
   exist (it is the auto check-out limit). Both belong in Settings, beside the auto check-out (OW-002,
   OW-021).
3. **The Prices & packages page needs one structure and an honest package form.** The page has two
   jobs (public prices with freshness, private templates for the desk). It shows a doubled title and
   names the price period «المدة». The package sheet marks the required validity "optional", caps
   days a week at 6 (the model allows 7), splits billing into two nested toggles where the model has
   one three-way choice, and overflows at 390 (OW-008, OW-009, OW-010).
4. **Announcements cannot be served as drawn, and cannot be ended.** The model has a bilingual text
   and no title and no author, while the sheet has two titles, one text and «أنشأه». No action ends
   or removes an announcement. A sudden closure that ends early keeps the space «مغلق الآن» publicly
   until its end date. The closure extension, irreversible and felt by every subscriber, is a second
   primary button inside the edit sheet, and it is offered before the closure has even started
   (OW-011, OW-012, OW-013).
5. **The overview buries what needs the owner.** Four money tiles lead, and «حداثة البيانات» sits
   last. Missing groups and the profile group are absent. A blind «ما زالت صحيحة» confirms prices the
   owner cannot see, its «تعديل» lands on the prices stub, and the phone's bottom bar repeats the
   desk link that P1 now reserves for «تسجيل زيارة». The proposal is a work queue first, as A8 did
   for the admin (OW-003).

Counts — **22 issues**:
- **By level:** 5 pattern · 1 design system · 3 component · 13 page.
- **By impact:** **7 high**, **13 medium**, **2 low**.
- **By type:** 15 defects · 7 improvements.

## 2. Patterns (proposals that change more than one page)

All of these are built from foundation §12 components. None needs a new design-system component.

### OW-001 · One space editor, two permissions
- **type:** defect · **level:** pattern · **impact:** high
- **where:**
  - Frame: *30 · Space profile — desktop 1440* and *36 · Space profile*.
  - Page: `http://127.0.0.1:5344/Owner%20space%20profile.html`.
  - Screenshot: `docs/design/screens/30-owner-space-profile-kept/01-space-profile-desktop-1440.webp`.
  - Compared with `Admin space edit.html?id=golden`.
- **evidence:** `OW-001.png`
- **what is wrong:** The owner's profile is drawn as its own editor, and it contradicts the settled
  admin editor (A1, AD-001…011) and the contract:
  - **8 cards, each with a date and a confirm:**
    - basics and location are confirmed separately, but the API's `profile` group is one date and
      one confirm;
    - photos and capacity show «آخر تحديث» and «المعلومات ما زالت صحيحة», but neither is a
      `FactGroup`, and `/confirm` exists only for the five groups.
  - **Names:** both names are required («أدخل الاسم بالعربية والإنجليزية»). The data model's name
    exception is English required, Arabic optional.
  - **Landmark:** one field. The contract has `landmarkAr` / `landmarkEn`.
  - **Area:** a `Select` of one governorate's areas.
  - **Pin:** placed by tap only, with no coordinates field. The built `AddSpaceForm` already has one,
    and it is the keyboard's way in.
  - **Settled admin decisions missing:** AD-006 (contact types «جوال»/«أوريدو»), AD-007 (hours
    fields) and AD-008 (the price table) all reappear as already decided, because the owner's page is
    a second copy.
- **proposal:** The owner's Space profile *is* the A1 editor, with A1's five groups, its gallery, its
  chips below `lg`, its «لم تُضف بعد» and its checklist (A2). It differs only where verification
  decides who edits:

  | | Admin (unverified space) | Owner (verified space) |
  |---|---|---|
  | Head | the unverified state, «عرض في الموقع» | «يظهر للزوار فور الحفظ» + «عرض الصفحة العامة» |
  | Groups | the five, each saved and confirmed | the same five, same rules |
  | Prices | a section of the page | a link row to *Packages & prices*, where the same price table lives (OW-006) |
  | Photos | — (the plan gives photos to the owner, 🏢) | the gallery, immediate actions (OW-007) |
  | Capacity, stay limit | never (ADR 0008: the admin never sees capacity) | not on this page: Settings (OW-002) |
  | Hide, delete, owners | the admin's | none |
  | Read-only | a verified space (AD-012) | never (a space they own is verified by definition) |

- **why it is better:** One component, one set of decisions, one test surface. The owner and the
  admin see the same groups, dates and confirms, so a report, the overview and the checklist can
  link to the same anchors.
- **cost:** M (the prototype's owner page is rebuilt from the A1 page; the built code will share one
  `SpaceEditor`).
- **pages:** Space profile; Admin space edit (shared); Overview (anchors); Data reports (anchors).
- **rule:** api-contract §5 *Spaces* (`FactGroup`, `/confirm`); data-model › Conventions (the name
  exception); DECISIONS_ADMIN A1, A2.

### OW-002 · Public facts on the profile, private operating values in Settings
- **type:** defect · **level:** pattern · **impact:** high
- **where:**
  - Frame: *36 · Capacity section — desktop 1440*.
  - Page: `http://127.0.0.1:5344/Owner%20space%20profile.html#capacity`.
  - Screenshot: `docs/design/screens/36-space-profile/03-capacity-section-desktop-1440.webp`.
- **evidence:** `OW-002.png`
- **what is wrong:**
  - The profile's promise, «كل قسم يُحفظ وحده، ويظهر للزوار فور الحفظ», is broken by its last card,
    «السعة ومدة الجلوس»:
    - capacity is private (ADR 0008) and drives the live state;
    - «أقصى مدة جلوس» is `SpaceSettings.maxStayMinutes`, the auto check-out limit.
  - The helper «يظهر في قواعد المساحة» is untrue: no page shows "space rules".
  - Meanwhile *Settings › الحضور* holds the auto check-out at closing, the stay limit's twin, without
    it.
- **proposal:**
  - Move both into **Settings**, with one card «الحضور والحالة المباشرة»:
    1. «السعة» (helper: «لا تظهر للزوار. بها تُحسب الحالة «ممتلئ»؛ بدونها لا تظهر حالة مباشرة»);
    2. «خروج تلقائي عند الإغلاق» (`Switch`);
    3. «خروج تلقائي بعد» (optional hours, labelled «اختياري»; helper «يُسجَّل خروج من يتجاوزها قبل
       الإغلاق»).
  - The profile keeps only what visitors see.
  - Judge by the capability that owns the rule (occupancy and space-settings), not by the screen.
    The plan sends capacity through `PATCH /manage/spaces/:spaceId`, and a screen can call it from
    Settings, so no API change is needed. Whether `capacity` should move under `/settings` is B's
    choice.
- **why it is better:** The owner reads one honest promise per page. The two values that shape the
  live state and the auto check-out sit together. The data model's rule 4 (no capacity → no live
  state) is said where capacity is typed.
- **cost:** S
- **pages:** Space profile, Settings, Overview (the «27 / 40» card links to Settings when capacity is
  unset).
- **rule:** ADR 0008; data-model › Derived values (live status rule 4, auto check-out); conventions
  §9 *occupancy*, *space-settings*.

### OW-003 · The owner's overview is a work queue first
- **type:** improvement · **level:** pattern · **impact:** high
- **where:**
  - Frame: *29 · Overview — desktop 1440 / phone 390*.
  - Page: `http://127.0.0.1:5344/Owner%20overview.html`.
  - Screenshots: `docs/design/screens/29-owner-overview-kept/01-overview-desktop-1440.webp` and
    `02-overview-phone-390.webp`.
- **evidence:** `OW-003.png`
- **what is wrong:**
  - **Order:**
    - four money tiles lead;
    - «حداثة البيانات» is the last card, below the fold at every width (at 768 it is the eleventh
      block);
    - «بلاغات جديدة» and «إعلانات نشطة» are tiles that link nowhere, while the money tiles do.
  - **The freshness card:**
    - lists four groups: no `profile`, and no *missing* state (A2/A8 count missing too);
    - its «تعديل» for prices opens `Owner space profile.html#prices`, the stub;
    - its «المعلومات ما زالت صحيحة» confirms a group the owner cannot see from here, and the public
      then reads «آخر تحديث اليوم».
  - **Phone:** the bottom bar holds «مكتب الاستقبال», a navigation link. Amended P1 reserves that bar
    for the desk's «تسجيل زيارة».
- **proposal:**
  - A first card **«يحتاج انتباهك»**, one row per item that needs the owner, each a link to where it
    is done. Hidden when empty, with one line «كل شيء على ما يرام». The rows:
    - groups **missing** («لم تُضف بعد») or **stale** («قد تكون قديمة منذ 34 يومًا»), the profile
      included, prices linking to *Packages & prices*;
    - new data reports («2 بلاغات جديدة»);
    - uncollected visits today;
    - a closure that has started without its extension (OW-013);
    - capacity not set (OW-002).
  - Then the money row and «الحاضرون الآن», then «اشتراكات تنتهي هذا الأسبوع».
  - **Confirm lives beside the values it confirms** (the profile section, the price table). The
    overview's row action is «مراجعة», which opens the section.
  - Every tile is a link, or none is.
  - On a phone: no bottom bar (the desk is in the navigation), and the money tiles become a 2 × 2
    grid so «الحاضرون الآن» shows on the first screen.
- **why it is better:** The owner opens the dashboard to learn what needs doing. A confirm made
  beside the prices is a true confirm. This is the same shape as the admin's overview (A8), so the
  two roles read alike.
- **cost:** M
- **pages:** Overview; Space profile and Packages (anchors and confirm); Data reports, Desk,
  Announcements, Settings (link targets).
- **rule:** DECISIONS_SHARED P1 (amended); DECISIONS_ADMIN A2, A8; features/spaces.md *Confirm*
  (a missing group has nothing to confirm, 409).

### OW-004 · What reaches others is said before it happens (P9 and A5 on the owner's pages)
- **type:** improvement · **level:** pattern · **impact:** medium
- **where:**
  - Frame: *37 · Temporary password (shown once) — desktop 1440*.
  - Page: `http://127.0.0.1:5344/Staff.html?pass=1`.
  - Screenshot:
    `docs/design/screens/37-staff-owner/05-temporary-password-shown-once-desktop-1440.webp`.
- **evidence:** `OW-004.png`
- **what is wrong:** The owner's actions that reach other people are not classified, so each page
  improvises:
  - **Staff password dialog:** it can be left by X, Escape or «تم» before copying. This is the exact
    case A5 closed for the admin.
  - **Closure extension:** it says nothing of what the subscribers will see.
  - **Deactivating a staff member:** it does not say they are signed out everywhere (OW-017).
- **proposal:** This table sets each action's form, applying P9. Dismiss buttons read «رجوع»
  everywhere.

  | Action (page) | Reaches | Form |
  |---|---|---|
  | Save / confirm a group (profile, prices) | the public page | act; toast names the group («حُفظت ساعات العمل») |
  | Remove a photo (profile) | the public page; no restore endpoint | `AlertDialog` «حذف الصورة؟ تختفي من صفحة المساحة» |
  | Reorder, cover (profile) | public, reversible | act, no toast (P8 exception) |
  | Pause / resume a package | future desk choices only | act, no toast (P8 exception: the card changes) |
  | Publish / edit an announcement | the public page | act; toast |
  | End an announcement now | public, reversible | act; toast with «تراجع» (OW-012) |
  | Delete a scheduled announcement | no restore endpoint | `AlertDialog` |
  | Extend subscriptions after a closure | every active subscriber; irreversible | `AlertDialog`, `variant="destructive"`, «مدّد 25 اشتراكًا» (OW-013) |
  | Add staff (new account) | creates an account | said before submit; password dialog under A5's rules (no X, no Escape, «تم» after «نسخ», handover channel) |
  | Deactivate staff | ends their sessions | `AlertDialog` with the true consequence (OW-017) |
  | Resolve / dismiss a report | the reporter reads the reply | A8: «لم يُعتمد» requires the reply |

- **why it is better:** One rule, so the owner learns once what a confirm means. The irreversible,
  money-shaping extension stops looking like an ordinary save.
- **cost:** S (wording and dialog wiring across five pages).
- **pages:** Space profile, Packages, Announcements, Staff, Data reports.
- **rule:** DECISIONS_SHARED P8, P9; DECISIONS_ADMIN A5, A8.

### OW-005 · Counted words in Arabic, and numbers inside labels
- **type:** defect · **level:** pattern · **impact:** medium
- **where:**
  - Frame: *29 · Overview — desktop 1440*.
  - Page: `http://127.0.0.1:5344/Owner%20overview.html`.
  - Screenshot: `docs/design/screens/29-owner-overview-kept/01-overview-desktop-1440.webp`.
  - Also *38 · Active · owner* (`Announcements.html`).
- **evidence:** `OW-005.png`
- **what is wrong:**
  - **Counts are glued to one plural form:**
    - «ينتهي بعد 1 أيام», «ينتهي بعد 2 أيام» (Overview);
    - «1 زيارات» (Overview, not collected);
    - «سيتأثر 25 اشتراكًا» is right only by luck of the number.
  - **Tab counts render as «نشطة ( 2 )»:** the isolated number pushes the parentheses apart
    (Announcements).
- **proposal:**
  - Every counted noun goes through Arabic plural forms (`Intl.PluralRules('ar')`: zero, one, two,
    few, many, other): «ينتهي غدًا», «ينتهي بعد يومين», «بعد 5 أيام», «زيارة واحدة».
  - A count in a tab or chip uses the `Badge` count, not parentheses around a `<bdi>`.
- **why it is better:** Arabic that reads as written by a person, not as a template (lens A10).
- **cost:** S
- **pages:** Overview, Announcements, Finance (helpers), Staff, the extension dialog.
- **rule:** foundation §8 (mixed content); `docs/frontend/localisation.md` (plurals).

### How the owner's pages apply the other settled patterns
These are choices only. The patterns themselves are not reported again.

**Primary action and "add" (P1 amended)**
- Overview: none; the desk is in the navigation.
- Announcements «إعلان جديد», Staff «إضافة موظف», Packages «باقة جديدة»: in the row above their
  list, at its end, at every width.
- Profile, Settings: none at page level; each section saves itself.
- Finance: «تصدير CSV» in the top bar's «⋯» on a phone.

**Column priority at 768 (SH-007, A7)**
- Staff (7 columns): becomes cards. Drop «الدور»; it is always «الاستقبال» (OW-018).
- Data reports (6 columns): becomes cards, as A7 did for the admin's.
- Finance › collections (5 columns): stays a table.

**Paging (P6, contract §4)**
- These page: announcements (each tab), data reports, debtors, «دفعوا هذا الشهر» (OW-016), staff.
- Packages: proposed as a bounded list answered whole, because the desk's picker needs them all (see
  *Rules in doubt*).

**Content width (AD-029):** Settings `max-w-3xl` (today `max-w-2xl`). The profile follows A1.

## 3. Issues

### OW-006 · Prices: one home, and the links that point at the stub
- **type:** defect · **level:** page · **impact:** high
- **where:**
  - Frame: *34 · Space profile · link to prices — desktop 1440*.
  - Page: `http://127.0.0.1:5344/Owner%20space%20profile.html#prices`.
  - Screenshot:
    `docs/design/screens/34-packages-prices-owner/07-space-profile-link-to-prices-desktop-1440.webp`.
- **evidence:** `OW-006.png`
- **what is wrong:**
  - The profile's «الأسعار» card says the prices «انتقلت … إلى صفحة مستقلة». That is a changelog
    sentence, not a section.
  - The overview's «تعديل» for stale prices opens this stub.
  - The profile's side navigation lists «الأسعار» as if it were a section.
  - The admin edits the same prices inside the editor (A1), so the owner and the admin look for them
    in different places with no explanation.
- **proposal:**
  - Prices stay on **Packages & prices**, as P3's navigation already says (المال › الباقات
    والأسعار).
  - The editor there is the **same price table as AD-008**, with its own «آخر تحديث» and «المعلومات
    ما زالت صحيحة».
  - In the owner's profile, the prices group is one row of the A2 checklist and of the chips: «الأسعار
    ← الباقات والأسعار».
  - Every «تعديل الأسعار» link (Overview, Data reports) goes to `Packages.html#prices`.
- **why it is better:** The owner finds prices where they think about money. Every link lands on the
  editor, not on a note about a move.
- **cost:** S
- **rule:** DECISIONS_SHARED P3; DECISIONS_ADMIN AD-008.

### OW-007 · Photos are a gallery of immediate actions, not a form
- **type:** defect · **level:** component · **impact:** medium
- **where:**
  - Frame: *30 · Space profile — desktop 1440*.
  - Page: `http://127.0.0.1:5344/Owner%20space%20profile.html#photos`.
  - Screenshot: `docs/design/screens/30-owner-space-profile-kept/01-space-profile-desktop-1440.webp`.
- **evidence:** `OW-007.png`
- **what is wrong:** The photos card is drawn like a group: a list edited locally, then «حفظ», with a
  date and a confirm. The plan's API is `POST / DELETE /manage/spaces/:spaceId/photos[/:photoId]`,
  where each upload, removal and reorder is its own request. That leaves no answer for:
  - what an upload shows while it travels on a weak connection;
  - what a 413 (too large) or 415 (wrong type) shows, and on which photo;
  - whether a removed photo can come back.
- **proposal:**
  - **Choosing files uploads them at once.** Each tile shows a `Spinner` and «جارٍ الرفع». A failed
    one stays as a tile with the error in words and two actions, «إعادة المحاولة» and «إزالة»:
    - «الصورة أكبر من 5 ميغابايت»;
    - «JPG أو PNG فقط».
  - **Removing a photo** is an `AlertDialog` (OW-004).
  - **Reorder and «الغلاف»** act at once, with no toast.
  - No «حفظ», no date, no confirm (A1).
  - At the limit, «رفع صور» is disabled with its reason («10 صور كحدّ أقصى»).
  - Empty state: an `EmptyState` «لا توجد صور بعد · الصورة الأولى تصبح الغلاف».
- **why it is better:** It matches how a photo really reaches the server. The owner on a weak
  connection sees each file's fate.
- **cost:** M
- **rule:** plan › *Planned API surface* (photos); api-contract §3 (413, 415); P9.

### OW-008 · Packages & prices: two sections that say what each is for
- **type:** improvement · **level:** page · **impact:** medium
- **where:**
  - Frame: *34 · Packages & prices — desktop 1440*.
  - Page: `http://127.0.0.1:5344/Packages.html`.
  - Screenshot:
    `docs/design/screens/34-packages-prices-owner/01-packages-prices-desktop-1440.webp`.
- **evidence:** `OW-008.png`
- **what is wrong:**
  - **Doubled heading:** the h2 «الأسعار المعلنة» heads a card titled «الأسعار».
  - **The price period is labelled «المدة»:** the glossary's term is «الفترة السعرية», and «المدة»
    is a subscription's length.
  - **The audience reads «عام / طلاب»:** the public page (U9) groups by «الأسعار» and «للطلاب».
  - **The private packages are cards:**
    - the fourth wraps alone;
    - the price is buried in a summary line;
    - the desk switch sits beside «تعديل» with equal weight.
- **proposal:**
  - **Section 1 «الأسعار المعلنة»** (h2), the AD-008 table, under its own line:
    - «تظهر في صفحة المساحة · للعرض فقط · الدفع في المساحة · آخر تحديث قبل 34 يومًا»;
    - the stale note, then «حفظ» and «المعلومات ما زالت صحيحة»;
    - the price period labelled «الفترة», the audience «لمن: الجميع · الطلاب».
  - **Section 2 «الباقات الخاصة»** (h2), the line «لا تظهر للزوار · تُختار في المكتب عند إنشاء
    اشتراك», then the add row (P1) and a list:
    - one row per package: the name, the terms summary, the price in `label` weight, and the
      «متاحة في المكتب» `Switch`;
    - «تعديل» in the row;
    - a paused row muted, with its badge.
  - Keep the sentence that public week and month prices also appear at the desk.
- **why it is better:** Each section has one job and one heading. The price, the thing an owner scans
  for, is visible. The words match the public page and the glossary.
- **cost:** S
- **rule:** glossary (*Price period*, *Package*); DECISIONS_PUBLIC U9; DECISIONS_ADMIN AD-008.

### OW-009 · The package sheet: required first, limits on demand, billing as the model has it
- **type:** defect · **level:** component · **impact:** medium
- **where:**
  - Frame: *34 · New package sheet · live summary — desktop 1440*.
  - Page: `http://127.0.0.1:5344/Packages.html?sheet=new`.
  - Screenshot:
    `docs/design/screens/34-packages-prices-owner/03-new-package-sheet-live-summary-desktop-1440.webp`.
- **evidence:** `OW-009.png`
- **what is wrong:**
  - **Validity is required but marked «اختياري»:** «الصلاحية (أيام)» is `Package.validityDays`, not
    null, yet the sheet says «كل الشروط اختيارية».
  - **Days a week:** the sheet caps them at 6; the model's CHECK allows 7.
  - **Billing:** the model has one three-way choice (`FIXED · PER_HOUR · PER_DAY`), but the sheet
    nests «الوحدة» inside «حسب الاستخدام». In Arabic both amounts are labelled «السعر (₪)».
  - **Wall of fields:** five numeric fields stand in a grid at equal weight, though most packages use
    one or two.
  - **Missing states:**
    - a name already used (`@@unique([spaceId, name])`);
    - the shift choice when the space has no shifts.
- **proposal:**
  1. «اسم الباقة».
  2. «الصلاحية» (required, days; helper «ينتهي الاشتراك بعد هذه المدة من بدايته»).
  3. «الحدود» (اختيارية): a `ToggleGroup type="multiple"` of the four limits («عدد الأيام · أيام
     بالأسبوع · ساعات باليوم · مجموع الساعات»). Each chip turned on reveals its field; days a week
     1–7.
  4. «طريقة الحساب»: one `ToggleGroup type="single"` «سعر ثابت · بالساعة · باليوم», then one amount
     labelled for the choice: «السعر الكلي (₪)», «سعر الساعة (₪)» or «سعر اليوم (₪)».
  5. «لمن»: the audience, and «الوردية» listing the space's own shifts. With none, it is disabled with
     «أضف ورديات في ساعات العمل أولًا», as AD-008 does.
  6. The summary (kept, it is good).

  A repeated name shows «اسم مستخدم لباقة أخرى» on the name.
- **why it is better:** The common case is three fields. The form says only what is true. Billing
  maps one-to-one to what is stored.
- **cost:** M
- **rule:** `schema.prisma` *Package* (validity, limits CHECK, unique name); foundation §10
  (disabled only with a reason shown).

### OW-010 · An end-side `Sheet` on a phone is three-quarters wide, and its form overflows
- **type:** defect · **level:** design system · **impact:** medium
- **where:**
  - Frame: *34 · Edit usage-based package — phone 390*.
  - Page: `http://127.0.0.1:5344/Packages.html?edit=p4`.
  - Screenshot:
    `docs/design/screens/34-packages-prices-owner/06-edit-usage-based-package-phone-390.webp`.
- **evidence:** `OW-010.png`
- **what is wrong:**
  - At 390 the sheet takes about 290 px.
  - The rate field runs off its start edge (its value is cut at the screen's edge).
  - Labels wrap beside their «اختياري».
  - The page behind shows a sliver of unusable content.
  - The same sheet carries the announcement, staff, report and package forms.
- **proposal:** In the layer, `Sheet side="end"` becomes full width below `md` (and keeps
  `max-w-sm` above). Its body's content is `min-w-0`, so a field never exceeds it.
- **why it is better:** A form on a phone gets the whole width. No field is cut.
- **cost:** S
- **rule:** foundation §9 (phone), §12 `Sheet`.

### OW-011 · Announcements: the fields the model has, and not the ones it lacks
- **type:** defect · **level:** page · **impact:** high
- **where:**
  - Frame: *38 · New announcement sheet — desktop 1440*.
  - Page: `http://127.0.0.1:5344/Announcements.html?sheet=new&type=event`.
  - Screenshot:
    `docs/design/screens/38-announcements-owner-reception/11-new-announcement-sheet-desktop-1440.webp`.
- **evidence:** `OW-011.png`
- **what is wrong:** The model's `Announcement` is `type`, `textAr` (required), `textEn` (optional),
  `startsAt` and `endsAt` (null = until removed). The design does not match it:
  - **Titles:** the sheet asks for «العنوان بالعربية», «العنوان بالإنجليزية» and one «النص»
    (single-language, optional). Two of those fields have no column, and the text has no English
    side.
  - **Author:** each card says «أنشأه أحمد». Announcement has no author (only the audit entry knows).
- **proposal:**
  - Follow the model:
    - «نص الإعلان بالعربية» (required, `Textarea`, with a short-length helper);
    - «نص الإعلان بالإنجليزية» (اختياري);
    - the type and the period.
  - The card's headline is the type `Badge` + the period, and the text below it.
  - Drop «أنشأه».
  - If the owner wants a title or an author, that is a schema change and their decision (a
    `createdById` is cheap and useful for the desk). Until decided, draw what exists.
- **why it is better:** The screen can be built without a hidden migration. The English text exists
  for the English interface.
- **cost:** S (design), or M with the schema change.
- **rule:** `schema.prisma` *Announcement*; lens §2c (a field the data model has not).

### OW-012 · An announcement can be ended now, removed, started now, or left open
- **type:** defect · **level:** page · **impact:** high
- **where:**
  - Frame: *38 · Active · owner — desktop 1440*.
  - Page: `http://127.0.0.1:5344/Announcements.html?tab=scheduled`.
  - Screenshot:
    `docs/design/screens/38-announcements-owner-reception/01-active-owner-desktop-1440.webp`.
- **evidence:** `OW-012.png`
- **what is wrong:**
  - **No way to end or remove:** the only action is «تعديل».
    - A power cut announced as a closure until Thursday that ends on Tuesday keeps the space
      «مغلق الآن» on the public page (live-status rule 2) until someone edits the date.
    - The plan has `DELETE` and `PATCH`.
  - **Dates only:** «من» and «إلى» are dates. The model stores times, has `endsAt = null` («حتى
    أُزيله»), and the commonest Gaza closure starts *now*.
- **proposal:**
  - **On an active card:** «إنهاء الآن» (`outline`). It sets the end to now and acts at once, with a
    toast «انتهى الإعلان · عادت الحالة تلقائية» and «تراجع» (OW-004).
  - **On a scheduled card:** «حذف», an `AlertDialog`.
  - **In the sheet:**
    - «يبدأ»: `ToggleGroup` «الآن · في موعد» (date + time);
    - «ينتهي»: «في موعد · بلا موعد» (helper «يبقى حتى تنهيه»).
  - For a closure, the sheet says «تظهر المساحة «مغلق الآن» طوال هذه الفترة».
- **why it is better:** The live state stays true when life changes faster than the plan, the
  everyday case for a space in Gaza.
- **cost:** M
- **rule:** data-model › Derived values (live status rule 2); `schema.prisma` *Announcement*
  (`endsAt` null); plan (`PATCH / DELETE announcements`).

### OW-013 · The closure extension is its own action, after the closure starts
- **type:** improvement · **level:** component · **impact:** high
- **where:**
  - Frame: *38 · Scheduled closure · extend (owner) — desktop 1440 / phone 390*.
  - Page: `http://127.0.0.1:5344/Announcements.html?tab=scheduled&edit=a1`.
  - Screenshot:
    `docs/design/screens/38-announcements-owner-reception/05-scheduled-closure-extend-owner-desktop-1440.webp`.
- **evidence:** `OW-013.png`
- **what is wrong:**
  - **Inside the edit form:** the extension, irreversible ("once per closure"), money-shaping and
    felt by 25 subscribers, is a card inside the edit sheet, with its own primary «تمديد» above the
    sheet's primary «حفظ». That makes two primaries in one form.
  - **Too early:** it is offered on a **scheduled** closure (1–3 Oct, today 29 Sep), before the
    closure has happened and while its dates can still change.
  - **Unclear count:** «سيتأثر 25 اشتراكًا» does not say which subscriptions (active today, or active
    during the closure).
- **proposal:**
  - The closure's **card** carries, for the owner only and once the closure has started, «تمديد
    الاشتراكات» (`outline`).
  - It opens an `AlertDialog`:
    - **title:** «تمديد اشتراكات المشتركين النشطين بأيام الإغلاق؟»;
    - **field:** «عدد الأيام», defaulting to the closure's days so far (or all of them once ended),
      at least 1;
    - **body:** «تتأخر نهاية 25 اشتراكًا نشطًا 3 أيام. لا يمكن التراجع، ولا تطبيقه مرة ثانية لهذا
      الإغلاق.»;
    - **action:** `variant="destructive"`, «مدّد 25 اشتراكًا».
  - After it: the card's line «مُدِّد 25 اشتراكًا 3 أيام · أحمد · 4 أكتوبر».
  - Reception's card says «يمدّد المالك الاشتراكات بعد الإغلاق».
  - The overview queue lists a closure started without its extension (OW-003).
  - The edit sheet keeps one primary.
- **why it is better:** The most consequential button on these pages is never confused with saving a
  text, and it is offered when its number of days is known.
- **cost:** M
- **rule:** ADR 0009 (owner only); `schema.prisma` *ClosureExtension* (once, ≥ 1 day); P9.

### OW-014 · Announcement types: one quiet colour, and the choice visible
- **type:** defect · **level:** page · **impact:** low
- **where:**
  - Frame: *38 · Active · owner — desktop 1440*.
  - Page: `http://127.0.0.1:5344/Announcements.html?tab=ended`.
  - Screenshot:
    `docs/design/screens/38-announcements-owner-reception/01-active-owner-desktop-1440.webp`.
- **evidence:** `OW-014.png`
- **what is wrong:**
  - **Colours:** the five types use five semantic roles.
    - «عرض» is `success`, a positive *state*.
    - «إغلاق مؤقت» is `destructive`, while foundation §5 now makes Closed `neutral`.
    - «فعالية» is `info`.
  - **Picker:** the type is a `Select` that hides five choices which change the form (closure).
- **proposal:**
  - **Colours:** type badges `neutral`, except «انقطاع» and «إغلاق مؤقت», which are `warning`
    (attention). The closure's public Alert follows U8.
  - **Picker:** the type becomes a `RadioGroup` (five short rows, each with a one-line hint, e.g.
    «إغلاق مؤقت — تظهر المساحة «مغلق الآن»»).
- **why it is better:** Colour keeps its meaning across the product, and the owner sees what each
  type does before choosing.
- **cost:** S
- **rule:** foundation §5 (status roles, Closed neutral); lens A5.

### OW-015 · Finance's period control changes nothing on the page
- **type:** defect · **level:** page · **impact:** medium
- **where:**
  - Frame: *33 · الدخل — desktop 1440*.
  - Page: `http://127.0.0.1:5344/Finance.html`.
  - Screenshot: `docs/design/screens/33-finance-reports-owner/01-desktop-1440.webp`.
- **evidence:** `OW-015.png`
- **what is wrong:** «الفترة 1 سبتمبر – 29 سبتمبر» heads every tab, but no block on the page follows
  it:
  - «اليوم»;
  - «هذا الشهر»;
  - «منذ البداية»;
  - «آخر 12 شهرًا»;
  - «آخر 30 يومًا»;
  - collections «هذا الشهر»;
  - occupancy «آخر 14 يومًا».

  On a phone it is a one-filter sheet.
- **proposal:**
  - Remove the range.
  - The charts keep their fixed windows, named in their descriptions.
  - The period-based blocks take one **«الشهر»** `Select` in the toolbar, last 12 months, default the
    current one: the month tile, collections by staff, «دفعوا هذا الشهر», and the occupancy figures.
  - CSV says what it exports: «تصدير الدخل (CSV)».
- **why it is better:** A control that is shown must do something. Owners count by month (ADR 0010,
  cash basis).
- **cost:** M
- **rule:** plan › finance endpoints; ADR 0010 rule 5.

### OW-016 · Finance's lists end in "and 17 more"
- **type:** improvement · **level:** page · **impact:** low
- **where:**
  - Frame: *33 · الديون — desktop 1440*.
  - Page: `http://127.0.0.1:5344/Finance.html?tab=debts`.
  - Screenshot: `docs/design/screens/33-finance-reports-owner/03-desktop-1440.webp`.
- **evidence:** `OW-016.png`
- **what is wrong:**
  - «دفعوا هذا الشهر» shows eight names and «و 17 آخرين», with nothing to open.
  - «عليهم مبالغ» lists every debtor on one page.
- **proposal:**
  - Both lists page (P6). «عليهم مبالغ» keeps the largest first.
  - «دفعوا هذا الشهر» shows the first five and «عرض الكل» to `Payments.html` filtered by the chosen
    month.
- **why it is better:** There are no dead ends, and the debtor list stays fast as it grows.
- **cost:** S
- **rule:** api-contract §4; DECISIONS_SHARED P6.

### OW-017 · Deactivating staff: the right verb and the true consequence
- **type:** defect · **level:** page · **impact:** medium
- **where:**
  - Frame: *37 · Suspend (confirm) — desktop 1440*.
  - Page: `http://127.0.0.1:5344/Staff.html?stop=1`.
  - Screenshot: `docs/design/screens/37-staff-owner/09-suspend-confirm-desktop-1440.webp`.
- **evidence:** `OW-017.png`
- **what is wrong:**
  - **The verb:** «إيقاف / Suspend» is the admin's word for ending a whole *account*
    (`User.suspendedAt`). The owner deactivates a *link* to one space (ADR 0009 rule 4). A linked
    person keeps their own account and other spaces.
  - **The body:** «ينتهي دخوله فورًا» omits that every session of theirs is revoked (security.md
    › Revocation), that this concerns this space only, and that it can be undone.
  - **Reactivation:** «إعادة تفعيل» is drawn, but the plan only says "deactivate".
- **proposal:**
  - **Verb:** «إيقاف وصوله» / "Remove access".
  - **Body:** «يخرج سامي من حسابه على كل الأجهزة الآن، ولا يصل إلى Focus Hub. يبقى اسمه على دفعاته
    وفي السجل، ويمكنك إعادة وصوله لاحقًا.»
  - **Action:** `variant="destructive"`.
  - The row badge reads «بلا وصول».
  - Ask B to serve «إعادة الوصول» as the same `PATCH`. Re-adding the same email reaches it anyway.
- **why it is better:** The owner knows exactly what the person loses, and nothing is said that is not
  true.
- **cost:** S
- **rule:** ADR 0009 rule 4; security.md › Revocation; glossary.

### OW-018 · Staff columns the model cannot fill, and the one state worth showing
- **type:** defect · **level:** page · **impact:** medium
- **where:**
  - Frame: *37 · Staff list — desktop 1440* (shown at 768, no board frame).
  - Page: `http://127.0.0.1:5344/Staff.html`.
  - Screenshot: `docs/design/screens/37-staff-owner/01-staff-list-desktop-1440.webp`.
- **evidence:** `OW-018.png`
- **what is wrong:**
  - **«آخر دخول»** («اليوم 07:52», «لم يدخل بعد»): no field holds a last sign-in.
  - **«الدور»:** always «الاستقبال».
  - **At 768:** the `DataTable` toolbar is an empty band (its only content is phone-only).
  - **Missing state:** a new account whose temporary password was never changed (`mustChangePassword`)
    looks exactly like an active one. The handover failing is the thing the owner needs to see.
- **proposal:**
  - Columns: «الاسم» (email under it), «الحالة», «أُضيف في» (the link's date), «مقبوضاته هذا الشهر»,
    actions.
  - A `warning` badge «لم يغيّر كلمة المرور المؤقتة بعد» while it is pending.
  - No toolbar when it holds nothing.
- **why it is better:** Every cell is real. The one failure in adding staff becomes visible.
- **cost:** S
- **rule:** `schema.prisma` *User* (`mustChangePassword`), *SpaceManager* (`createdAt`); lens A11.

### OW-019 · Adding staff: one submit, both outcomes said first
- **type:** defect · **level:** page · **impact:** medium
- **where:**
  - Frame: *37 · Email already has an account → «ربط» — phone 390*.
  - Page: `http://127.0.0.1:5344/Staff.html?sheet=add&email=nour@example.com`.
  - Screenshot:
    `docs/design/screens/37-staff-owner/08-email-already-has-an-account-phone-390.webp`.
- **evidence:** `OW-019.png`
- **what is wrong:**
  - **Two steps:** «إضافة» first, then, if the email has an account, an Alert and a second button
    «ربط».
  - **No endpoint for the first step:** the plan has one `POST /staff` that decides, and no account
    lookup.
  - **Privacy:** the first step tells an owner whether any email has a Masaha account before they
    commit to anything.
- **proposal:**
  - The sheet says both outcomes before the submit: «إن كان للبريد حساب في مساحة يُربط به ويدخل
    بكلمة مروره؛ وإلا يُنشأ حساب برمز مرور مؤقت يظهر لك مرة واحدة.»
  - The submit is «إضافة إلى الاستقبال».
  - The answer decides what follows:
    - the password dialog (A5's rules); or
    - a toast «رُبط حساب nour@example.com بـ Focus Hub».
  - A failure stays in the sheet (P8).
- **why it is better:** It takes one step, it is servable by the planned endpoint, and nothing is
  revealed before the act.
- **cost:** S
- **rule:** ADR 0009 rule 4; plan (`POST /manage/spaces/:spaceId/staff`); DECISIONS_ADMIN A5.

### OW-020 · Should the owner see who reported? (the owner's choice)
- **type:** improvement · **level:** page · **impact:** medium
- **where:**
  - Frame: *39 · Open report — desktop 1440*.
  - Page: `http://127.0.0.1:5344/Data%20reports.html?open=d1`.
  - Screenshot: `docs/design/screens/39-data-reports-owner/03-open-report-desktop-1440.webp`.
- **evidence:** `OW-020.png`
- **what is wrong:** The owner's list and sheet name the reporter («سارة · 29 سبتمبر»). No document
  says whether a space's owner sees a reporter's identity. In a small community a report about a
  space, read by that space, can invite pressure. And the name does nothing to help correct a fact.
- **proposal:** The owner sees «زائر» and the date. The admin keeps the name. Everything else stays
  as A8 settles it: «لم يُعتمد» needs its reply, and «تعديل الحقل» carries the report and offers
  «تم التصحيح» in place, applied to the owner. The alternative, showing the first name only, is the
  owner's call.
- **why it is better:** Reporting stays safe, so people keep reporting, and that is what keeps the
  facts true.
- **cost:** S
- **rule:** none yet (to be recorded in `features/` when data reports are built).

### OW-021 · Settings: the rounding minutes and the defaults the model holds
- **type:** defect · **level:** page · **impact:** medium
- **where:**
  - Frame: *40 · Owner settings — desktop 1440*.
  - Page: `http://127.0.0.1:5344/Owner%20settings.html`.
  - Screenshot: `docs/design/screens/40-settings-owner/01-owner-settings-desktop-1440.webp`.
- **evidence:** `OW-021.png`
- **what is wrong:**
  - **Rounding:** «تقريب لأعلى بعد 10 دقائق» is a fixed choice. The model stores the N (1–59;
    platform default 15).
  - **Student prices for visits:** drawn off; the model's default is on.
  - **Stay limit:** it is missing here (it sits on the profile, OW-002).
  - **Save:** disabled until a change (P10).
- **proposal:**
  - The first rounding option reads «تقريب لأعلى بعد [ 15 ] دقيقة», with a small numeric `Input`
    inside the option, enabled when the option is chosen, plus its live example.
  - Student prices for visits starts on.
  - The attendance card as OW-002 sets it.
- **why it is better:** The owner can set the rule the desk actually applies, and what the page shows
  matches what is stored.
- **cost:** S
- **rule:** `schema.prisma` *SpaceSettings*; conventions §9 *New-space defaults*.

### OW-022 · The owner's audit log has no place
- **type:** improvement · **level:** page · **impact:** medium
- **where:**
  - Frame: *40 · Owner settings — desktop 1440* (the navigation).
  - Page: `http://127.0.0.1:5344/Owner%20settings.html`.
  - Screenshot: `docs/design/screens/40-settings-owner/01-owner-settings-desktop-1440.webp`.
- **evidence:** `OW-022.png`
- **what is wrong:**
  - `overview.md` lists the owner's «Audit log».
  - ADR 0009 gives it to the owner.
  - The plan builds it in step 11 (finding 14).
  - Yet no owner frame or navigation item exists.
- **proposal:**
  - Add «سجل التدقيق» to P3's «الفريق والإعدادات» group.
  - It is the admin's audit page (AD-028: target links, neutral badges, «آخر 30 يومًا», the actor
    filter once there is more than one actor), scoped to the space.
  - The actions are the space's (saves, confirms, voids, staff, extensions).
- **why it is better:** The owner can answer "who changed the price?" and "who voided this?". It
  reuses a settled page.
- **cost:** S (design), M (build).
- **rule:** ADR 0009 rule 5; finding 14; DECISIONS_SHARED P3 (an added item, the owner's decision).

## 4. Rules in doubt

- **api-contract §4, "every list pages":** a space's **packages** are a short, bounded list that the
  desk's subscription picker needs whole, like the lookups. Propose adding them to §4's exceptions;
  staff could follow. B's decision, with the owner.
- **overview.md › Dashboard, "Space profile (owner; Arabic required, English optional)":** this
  misleads. The name is the data model's exception (English required, Arabic optional), and the
  prototype followed the overview into requiring both. The fix is one clause in the overview (a
  document, not the design). Record as a finding if not fixed in scope.
- **glossary *Package* and foundation §13 #21, "the published prices are the public packages":** the
  phrase makes "student" a period («hour, day, week, month, student»). Since U9, the student price is
  an *audience*, and only week and month prices act as packages at the desk. Propose: «the published
  week and month prices also serve as packages at the desk; private packages are never shown
  publicly».

## 5. Not reviewed

- **Out of scope (review 6):** the front desk, customers, the subscription sheet, payments, and the
  receive-payment sheet that Finance › Debts opens.
- **Settled, not re-reported:** the shell's top bar and public-state control (P2), the navigation
  (P3), the account menu (P4), and the contact types, hours and price-table forms (AD-006/007/008).
  The owner's page inherits them through OW-001.
- **Known limits:**
  - `Owner overview.html?override=120` and `Announcements.html?tab=ended&edit=a4` are superseded
    frames;
  - placeholder navigation icons;
  - illustrative data.
- **The charts' design** (finance) is settled in build step 11. I noted only that the bars carry
  their values in a `title`, which a keyboard user cannot reach. The screen-reader table covers it.
- **The map pin** was looked at only as far as OW-001; its behaviour is the built `AddSpaceForm`'s.
