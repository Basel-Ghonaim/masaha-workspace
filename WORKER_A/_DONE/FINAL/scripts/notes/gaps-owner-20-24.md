# Gaps 20–24 (agent report, verified against prototype + code by the agent)

## 20 Space profile — partial
1. Open-report notice above its section missing (O12/A8): «بلاغ مفتوح على {field}», the report's words, «زائر، {date}», «تم التصحيح», «فتح البلاغ للرد»; after: «عُلّم «تم التصحيح»» + «العودة إلى البلاغات». absent in features/spaces, ProfilePage. evidence Owner space profile.html:48,51,66,68; owner.jsx:250-268. M. Fix: page fills a notice slot in SpaceEditor per section from a data-reports component; needs one report by id (contract has only paged list) → add GET …/data-reports/:reportId or filter status=OPEN; «تم التصحيح» = existing PATCH.
2. «نسخ إلى كل الأيام» header action stays beside title on phone; design moves it to top of content below 768. SectionCard.tsx:41-46 (shared with admin editor). S.

## 21 Prices & packages — partial
1. Desk words missing (design issue 4 dropped them because desk not built; now built): page line «أسعار الأسبوع والشهر تُختار أيضًا في المكتب عند إنشاء اشتراك.», section line «… · تُختار في المكتب عند إنشاء اشتراك», switch «متاحة في المكتب», sheet's «…وتُختار في مكتب الاستقبال», empty «…لتختارها في المكتب». copy/arabic/packages.ts:6,11,14,80. Packages.html:98,145,152,168,176. S.
2. Row price wrong place/weight: design label weight in end group beside switch; code body-sm under terms. PackageRow.tsx:23. S.
3. Report notice above «الأسعار المعلنة» (?report=d2#report) missing. Packages.html:146. S once 20.1.

## 22 Staff — partial
1. «مقبوضاته هذا الشهر» column / card «هذا الشهر {₪}» missing, each links to ledger for that person. StaffList.tsx:97-110. M. Fix: compose from GET …/finance/income collections[].recordedBy.id/totalAgorot (design issue 9 deferred to payments step, built).
2. Menu item «عرض مقبوضاته» missing → link …/payments?staff={userId} (ledger reads ?staff=, ledgerQueryOf.ts:59). useStaffActions.ts:49-82. S.
3. «أُضيف في» column/card line missing; StaffMember has no date (shared space-links/responses.ts:75-86). M: add addedAt (link createdAt) across shared/API/contract/web.

## 23 Data reports — partial
1. «تعديل الحقل» doesn't carry the report (?report=<id>#report) and list can't open one from ?open=<id>. DataReportsPage.tsx:35-38; reportsQueryOf.ts:39-40. S.
2. Sidebar «بلاغات البيانات» has no count of new reports (badge, badgeLabel «بلاغات جديدة»). NavigationItem.tsx:17-30. S. Read GET …/data-reports?status=OPEN&limit=1 meta.totalRecords.

## 24 Settings — partial
1. «حسابي» card missing: «الاسم وكلمة المرور واللغة والمظهر.» + «الإعدادات الشخصية» → /me. Owner settings.html:115. S (design issue 13 in space-settings.md said /me not built).
2. Auto check-out helper lacks «الزيارات غير المدفوعة تظهر في «غير محصّل».» copy/arabic/spaceSettings.ts:61; Owner settings.html:81. S.
3. Reminder description lacks «تُفتح في واتساب برسالة جاهزة من ملف الزبون، وترسلها أنت.» spaceSettings.ts:83; Owner settings.html:106. S once customer file's WhatsApp reminder built (none on main).

Decided deviations: Profile no unsaved alert / no amenities link (DI 2,3), only hidden badge, English label always, prices table from 1024 (67), spinner per tile (73), gallery copy (74), retired amenity line (99). Packages: «بدون وردية» first (5), shekels decimals (6), held-shift line (7), 102, 103. Staff: creates only (ADR 0009 rev, DI10), held reissue (11), 92, 104/105. Data reports: three chips DI-31, no current value DI-33, day not time DI-34/150, no-details DI-35, decided read-only DI-37, toast+«عرض الكل» DI-41/42. Settings: reception card (14), «استعادة النص الافتراضي» (17), no money examples (16). All: 130.
Superseded deviations (reasons no longer hold): 21.1 (DI 4), 22.1–22.3 (DI 9), 24.1 (DI 13).
UNVERIFIED: dark contrast, 768/1440 rendering.
Total 13.
