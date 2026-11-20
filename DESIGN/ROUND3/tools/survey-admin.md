# Survey — admin dashboard, shells, landing, 404, showcase (for the capture script)

Read-only survey of `C:\dev\masaha\app-design\apps\web\src` and DB `masaha_dr_dev`, 2026-11-13. Strings are copied from
`shared/copy/{arabic,english}/*.ts` (key in parentheses, relative to the catalogue root). «…» marks a quoted
string; the guillemets are not part of it unless the catalogue has them.

## Common (applies to every page below)
- Base `http://localhost:5320`; API under `/api/v1` (every path below omits `/api/v1`).
- Session: sign in as the ADMIN, user 1 «Basel» `baselghonaim@gmail.com`. Every page load first sends `POST /auth/refresh` (cookie) and the guards wait for it. A sign-in sets the UI language to the account's; afterwards pick language/theme by localStorage **before** load: `masaha.language` = `ar` | `en`, `masaha.theme` = `light` | `dark` (raw strings; no key = device). The dashboard's language/theme toggles only write these keys (no API call).
- Every admin page also sends `GET /admin/data-reports?status=OPEN&handledBy=ADMIN&page=1&limit=1` (the sidebar badge; `meta.totalRecords` = 7 now).
- Retries: the transport re-sends a GET on 5xx / network error / timeout **twice** (after 1 s, then 2 s) → a 500 stub must answer all 3 attempts and the error shows after ~3 s. 4xx (429 included) is never retried. Queries: `retry:false`, `staleTime` 30 s, refetch on window focus.
- Stub shapes: success `{"success":true,"data":…}` (lists add `"meta":{"currentPage":1,"limit":20,"totalPages":1,"totalRecords":0}`); error `{"success":false,"error":{"type":"server","message":"x","requestId":"r1"}}` + HTTP 500; 429: `"type":"rate_limit"` + header `Retry-After: 60` → retry buttons / row actions are held with a countdown line («محاولات كثيرة، حاول بعد …» forms.retryIn). Loading = hold the request unanswered. Offline = abort the request (network error) → offline variants.
- Accessible names that embed a person's or space's name wrap it in Unicode isolates U+2068 … U+2069 (written `⁨…⁩` below, e.g. «قائمة الحساب: ⁨Basel⁩»). Strip `[\u2066-\u2069]` before matching, or include them. Visible text never has them.
- Space names: Arabic UI shows `nameAr`, or `nameEn` (lang=en) when there is none (spaces 8, 13, 24); English UI always `nameEn`. People's names are Arabic in both UIs.
- Widths: <768 phone (sidebar = drawer), 768–1023 tablet (icon rail), ≥1024 desktop (expanded sidebar). Tables: spaces, users, reports from 1024 (cards below); owners, audit from 768.
- Lists page at 20. Pagination (`shared/lists/ListPagination`): links «السابق»/«Previous», «التالي»/«Next», page links aria-label «الصفحة 2»/«Page 2» (`*.pagination.page`). A `page=` past the last is replaced by the last page.
- Forms validate in the browser with the contract schema (`useServerForm`): an empty submit shows field errors and sends **nothing**.
- Data now (time-dependent; stale = prices > 30 days, other groups > 60 days): 38 spaces; 1 deleted (Demo Space). Verified (owner linked): 2–9, 14, 16, 18, 22, 23, 26–31 (19). Unverified: 10–13, 15, 17, 19–21, 24, 25, 32–38 (18). Hidden: none. Prices stale on 2–25; hours stale on 9; hours missing on 7 (verified); prices missing on 32. Photos: 1 each, 26 has 4, deleted 1 has 0. Shifts only on 2, 16, 26, 27, 30 (all verified). Users 50 (1 admin, 7 owners: 2, 4, 46–50; user 3 «ليلى النجار» is reception at 26). No suspended, no Google-only account. Reports 18 (9 open: 7 admin-handled, 2 owner-handled).

---

## Dashboard landing — /dashboard   (role: admin)
- example URLs: `/dashboard`
- params: none (`next` is not read here).
- states by URL: redirect: `/dashboard` → replaced by `/dashboard/admin` once the session is restored (renders nothing itself).
- states by click: none.
- requests on load: `POST /auth/refresh` only.
- empty/other notes: signed out → sign-in page with the return URL.

## Overview — /dashboard/admin   (role: admin)
- example URLs: `/dashboard/admin`
- params: none.
- states by URL:
  - ready: `/dashboard/admin` — tiles region «ملخص المنصة»/«Platform summary» (overview.admin.tiles.label): Spaces 37 («19 موثّقة · 18 غير موثّقة · 0 مخفية»), Open reports 9 («7 بانتظار الإدارة · 2 بانتظار المالكين»), Stale or missing 25, Unverified no owner 18, New users 18. Card «اكتمال البيانات»/«Data completeness» lists 5 of 12: Beit Lahia Desk (15), Bureij Work (20), Freelancers House (11), Hawa Tech Space (13), Jreas Hub (32); footer link «عرض الكل (12)»/«View all (12)».
  - loading: hold `GET /admin/overview` → two skeleton blocks (`[aria-busy]`).
  - failed: 500 → destructive alert «تعذّر تحميل النظرة العامة»/«Couldn’t load the overview» (overview.loadFailed) + button «إعادة المحاولة»/«Try again» (status.retry).
  - offline: abort → empty state «لا يوجد اتصال بالإنترنت»/«No internet connection» (status.offline.title) + «إعادة المحاولة».
  - 429: as failed, retry button disabled with countdown.
  - nothing missing: stub `completeness:{total:0,first:[]}` → «لا مساحات ينقصها شيء.»/«No space misses anything.» and «عرض الكل»/«View all».
- states by click: none (every control is a link): tiles → `a[href="/dashboard/admin/spaces"]`, `a[href="/dashboard/admin/reports?status=open"]`, `a[href="/dashboard/admin/spaces?stale=true"]`, `a[href="/dashboard/admin/spaces?status=unverified"]`, `a[href="/dashboard/admin/users"]`; each completeness row link «تعديل»/«Edit» (overview.admin.completeness.edit) → `/dashboard/admin/spaces/<id>`; «عرض الكل (12)» → `/dashboard/admin/spaces?status=editable&stale=true`.
- requests on load: `GET /admin/overview` (refetched on every mount).
- empty/other notes: tiles: 1 column <768, 2 at 768, 3 at 1024, 5 at 1280. Privacy note under the card (spaces.editor.privacy).

## Spaces list — /dashboard/admin/spaces   (role: admin)
- example URLs: `/dashboard/admin/spaces`, `/dashboard/admin/spaces?page=2`, `/dashboard/admin/spaces?status=deleted`
- params (`features/space-links/services/filtersOf.ts`):
  - `q` = 1–80 chars, searches both names (e.g. `q=hub` → many; `q=zzzz` → none).
  - `status` = `verified` (19) | `unverified` (18) | `hidden` (0 → no-match) | `deleted` (1: Demo Space) | `editable` (18, unverified incl. hidden). Anything else = all non-deleted (37).
  - `governorate` = id 1–5 (2 Gaza City → 20 rows; 5 Rafah → 0) or `area` = id (area wins): `area=2` Al-Rimal → 6, `area=6` Sheikh Ijlin → 0.
  - `stale=true` → 25 rows (2 pages); `status=editable&stale=true` → 12.
  - `page` = N (37 rows → pages 1–2; page 2 has 17).
- states by URL:
  - default (2 pages): `/dashboard/admin/spaces`
  - page 2: `/dashboard/admin/spaces?page=2`
  - search, no result: `/dashboard/admin/spaces?q=zzzz` → «لا توجد مساحات تطابق الفلاتر»/«No spaces match the filters» + button «مسح الفلاتر»/«Clear filters»
  - filter, no result: `/dashboard/admin/spaces?status=hidden`
  - filter on: `/dashboard/admin/spaces?status=verified`, `…?status=unverified`, `…?governorate=2`, `…?area=2`
  - stale chip on: `/dashboard/admin/spaces?stale=true` (page 2: `…?stale=true&page=2`)
  - overview's «عرض الكل»: `/dashboard/admin/spaces?status=editable&stale=true`
  - deleted: `/dashboard/admin/spaces?status=deleted` (muted name, «محذوفة · <date>», a Restore button instead of the menu)
  - past the last page: `/dashboard/admin/spaces?page=9` → replaced by page 2
  - loading / failed / 429: hold or 500 `GET /admin/spaces…` → skeleton rows / «تعذّر تحميل المساحات»/«We couldn’t load the spaces» + «إعادة المحاولة»
- states by click:
  - row menu: [css=`button[aria-label^="إجراءات: "]` / `button[aria-label^="Actions: "]`; name «إجراءات: ⁨نور هب⁩»/«Actions: ⁨Noor Hub⁩» (spaces.menu.actions)] → DropdownMenu: «تعديل»/«Edit» (link; on verified rows «عرض (يعدّلها المالك)»/«View (its owner edits it)» spaces.menu.view), «إخفاء»/«Hide» (spaces.menu.hide — **WRITES at once**, `PUT /admin/spaces/:id/hidden`), separator, «حذف»/«Delete» (spaces.menu.delete). All widths (last table column ≥1024, card end <1024). Opening writes nothing.
  - delete dialog: row menu → menuitem «حذف»/«Delete» → AlertDialog title «حذف نور هب؟»/«Delete Noor Hub?» (spaces.deleteDialog.title), buttons «رجوع»/«Back», «حذف»/«Delete» (confirm **WRITES** `DELETE /admin/spaces/:id`). Opening writes nothing.
  - restore (deleted row): on `?status=deleted`, button text «استرجاع»/«Restore», aria-label «استرجاع ⁨مساحة تجريبية⁩»/«Restore ⁨Demo Space⁩» (spaces.menu.restoreNamed) — **WRITES** `POST /admin/spaces/1/restore`.
  - status select (≥768 inline): role=combobox named «الحالة»/«Status» (spaceLinks.adminList.status) → listbox «كل الحالات», «موثّقة», «غير موثّقة», «مخفية», «محذوفة», «تعدّلها الإدارة» / «All statuses», «Verified», «Unverified», «Hidden», «Deleted», «Kept by the admin». Writes the URL only.
  - place select (≥768 inline): role=combobox named «المحافظة / المنطقة»/«Governorate / area» (adminList.place) → listbox «كل المناطق»/«All areas» (lookups.placeSelect.all), then each governorate and its indented areas.
  - filters sheet (<768 only): button text «الفلاتر»/«Filters», aria-label «الفلاتر»/«Filters» or «الفلاتر، المطبّق منها: 1»/«Filters, 1 applied» (adminList.filters / filtersApplied) → bottom Sheet title «الفلاتر»/«Filters», close «إغلاق»/«Close», the two selects, «عرض 37 نتيجة»/«Show 37 results» (adminList.showResults), «مسح الفلاتر»/«Clear filters» (disabled while none applies).
  - stale chip: toggle button (aria-pressed) «قديمة أو ناقصة»/«Stale or missing» in group «تصفية سريعة»/«Quick filter» → `?stale=true`. All widths.
  - search: input type=search in field «بحث»/«Search», placeholder «اسم المساحة»/«Space name»; typing writes `?q=` after a pause.
  - add space: link «إضافة مساحة»/«Add space» (dashboard.addSpace.title) → `/dashboard/admin/spaces/new`.
- requests on load: `GET /admin/spaces?page=1` (+ `q`, `status`, `governorateId`, `areaId`, `stale=true`); ≥768 also `GET /admin/governorates` (place field). Writes: `PUT /admin/spaces/:id/hidden {isHidden}`, `DELETE /admin/spaces/:id`, `POST /admin/spaces/:id/restore`.
- empty/other notes: empty (stub `data:[]`, no filter) «لا توجد مساحات بعد»/«No spaces yet» + «تظهر المساحات هنا بعد إضافتها.»; count line «عدد المساحات: 37»/«Spaces: 37». A 429 on hide/delete shows the hold line above the list and holds every row's menu. Pages: 37 rows → 2.

## Add space — /dashboard/admin/spaces/new   (role: admin)
- example URLs: `/dashboard/admin/spaces/new`
- params: none.
- states by URL:
  - empty form: `/dashboard/admin/spaces/new` (cards «الأساسيات»/«Basics» and «الموقع»/«Location»; breadcrumb nav «مسار التنقل»/«Breadcrumb»: link «المساحات»/«Spaces» › «إضافة مساحة»).
  - map failed: block `https://tile.openstreetmap.org/*` → «لم تُحمَّل الخريطة. أدخل الإحداثيات بدلًا منها.»/«The map didn’t load. Enter the coordinates instead.» (map.failed).
  - areas failed: 500 on `GET /lookups` → the area select's only option says the failure.
- states by click:
  - validation: click submit [role=button «إضافة مساحة»/«Add space» (spaces.add.submit)] on the empty form → «أدخل الاسم بالإنجليزية»/«Enter the English name», «أدخل العنوان بالعربية»/«Enter the Arabic address», «اختر المنطقة»/«Choose the area», «ضع الدبوس على الخريطة أو أدخل إحداثياته»/«Place the pin on the map, or enter its coordinates» (spaces.add.fieldErrors). No request. All widths.
  - area select: role=combobox named «المنطقة»/«Area» (spaces.add.area), placeholder «اختر المنطقة»/«Choose an area» → listbox grouped by governorate.
  - map pin: click inside the map [css=`[aria-label="خريطة قطاع غزة: اضغط لوضع دبوس المساحة"]` / `[aria-label="Map of the Gaza Strip: click to place the space’s pin"]` (spaces.add.map)] → pin + coordinates filled. Zoom buttons «تكبير»/«Zoom in», «تصغير»/«Zoom out». No write.
  - coordinates errors: field «الإحداثيات»/«Coordinates»: type `1, 1` + submit → «هذه النقطة خارج قطاع غزة»/«This point is outside the Gaza Strip»; `abc` → «أدخل الإحداثيات: خط العرض ثم خط الطول»/«Enter the coordinates as the latitude, then the longitude».
- requests on load: `GET /lookups`; map tiles. On submit: `POST /admin/spaces` (**WRITES**, then navigates to the new space's editor).
- empty/other notes: optional fields marked «اختياري»/«Optional».

## Space editor — /dashboard/admin/spaces/:spaceId   (role: admin)
- example URLs:
  - unverified, editable, a section missing (A2 / «اكتمال الملف» line): `/dashboard/admin/spaces/32` (Jreas Hub: prices missing → «6 من 7 أقسام», issue link «الأسعار المعلنة: لم تُضف بعد»/«Published prices: not added yet»).
  - unverified, several issues: `/dashboard/admin/spaces/24` (Mawasi Field Office: no Arabic name, about missing, prices stale, no English address); `/dashboard/admin/spaces/10` (Tuffah Place: about missing, prices stale 91 days).
  - unverified, complete: `/dashboard/admin/spaces/34` (Al-Salam Hub → «الملف مكتمل ومحدّث»/«The profile is complete and up to date»).
  - verified = read-only for the admin (no Edit buttons, no «ما زالت صحيحة», no photo management; hide/delete stay): `/dashboard/admin/spaces/2` (Noor Hub, owner سامي الحلو), `/dashboard/admin/spaces/26` (Pal Hub, owner أحمد الشوا, 4 photos, 2 shifts), `/dashboard/admin/spaces/7` (hours missing, read-only empty «ساعات العمل غير متوفرة.»).
  - deleted: `/dashboard/admin/spaces/1` → API 404 → 404 state inside the shell; top-bar actions absent.
  - unknown: `/dashboard/admin/spaces/9999` (API 404); `/dashboard/admin/spaces/abc`, `/dashboard/admin/spaces/0` (404 without a request).
- params:
  - `sheet` = `prices` | `hours` | `shifts` | `amenities` | `about` | `location` | `contacts` → that Sheet opens once the page draws (only when editable, i.e. unverified); the param is then removed (replace).
  - `report` = an OPEN report id of this space → its notice inside the field's section; add `#report` to land on it.
  - hash = `#photos` | `#prices` | `#hours` | `#shifts` | `#amenities` | `#about` | `#location` | `#contacts` → scrolls to and focuses that section's heading (`#<id>-title`).
- states by URL:
  - prices sheet open: `/dashboard/admin/spaces/32?sheet=prices` (empty, one starting row) or `/dashboard/admin/spaces/10?sheet=prices`
  - hours sheet: `/dashboard/admin/spaces/10?sheet=hours`; shifts sheet: `/dashboard/admin/spaces/10?sheet=shifts`; amenities: `…/10?sheet=amenities`; about: `…/24?sheet=about`; location: `…/24?sheet=location`; contacts: `…/10?sheet=contacts`
  - report notice: `/dashboard/admin/spaces/32?report=4#report` (prices), `/dashboard/admin/spaces/34?report=11#report` (hours) → notice «بلاغ مفتوح على الأسعار»/«An open report on Prices» (dataReports.notice.title)
  - section landing: `/dashboard/admin/spaces/10#contacts`
  - stale section: `/dashboard/admin/spaces/10#prices` → badge «قد تكون قديمة»/«May be out of date» + line + button «ما زالت صحيحة»/«Still correct»
  - loading: hold `GET /admin/spaces/:id` → skeleton (label «جارٍ التحميل»/«Loading»)
  - failed: 500 on `GET /admin/spaces/:id` → «تعذّر تحميل المساحة»/«We couldn’t load the space» + «إعادة المحاولة»
  - photos failed: 500 on `GET /admin/spaces/:id/photos` → header «تعذّر حساب اكتمال الملف: لم تُحمَّل الصور»/«We couldn’t count the profile: the photos didn’t load» + «إعادة المحاولة»; photos card «تعذّر تحميل الصور»/«We couldn’t load the photos»
  - photos empty: stub `GET /admin/spaces/:id/photos` → `data:[]` → «لم تُضف صور بعد.»/«No photos yet.» + «أضف صورًا»/«Add photos» and header link «أضف صورة غلاف»/«Add a cover photo» (editable spaces only)
- states by click (all on an unverified space unless said; Sheets slide from the end side, full width <768, max 2xl from 768; footer «حفظ»/«Save» + «رجوع»/«Back»; close X aria-label «رجوع»/«Back»; opening writes nothing):
  - page actions ≥768: buttons «إخفاء عن الزوار»/«Hide from visitors» (spaces.editor.actions.hide — **WRITES at once**; «إظهار للزوار»/«Show to visitors» when hidden) and «حذف المساحة»/«Delete the space» (spaces.editor.actions.delete) → the delete AlertDialog «حذف جريس هاب؟»/«Delete Jreas Hub?» («رجوع»/«حذف»; confirm **WRITES**, then `/dashboard/admin/spaces?status=deleted`). Verified spaces too.
  - page actions menu <768: icon button aria-label «إجراءات الصفحة»/«Page actions» (spaces.editor.actions.menu) → DropdownMenu «إخفاء عن الزوار», «حذف المساحة».
  - copy link: button «نسخ الرابط»/«Copy link» (spaces.editor.header.copyLink) → toast «نُسخ رابط الصفحة العامة»/«Public page link copied» (or «تعذّر نسخ الرابط. انسخه من هنا:» when the clipboard is refused). No write.
  - link an owner (unverified only): header button «ربط مالك»/«Link an owner» (spaceLinks.spaceOwners.link) → Dialog «ربط مالك بـ جريس هاب»/«Link an owner to Jreas Hub», «ليس لها مالك اليوم.»/«It has no owner today.», close «إغلاق»/«Close», field «الشخص»/«Person» (combobox, «اختر شخصًا»/«Choose a person»), link «مالك جديد بلا حساب؟ أضفه من صفحة أصحاب المساحات.» → `/dashboard/admin/owners?sheet=add`, submit «ربط»/«Link» (**WRITES** `POST /admin/spaces/:id/owners`). On open: `GET /admin/users?state=active&limit=50`, `GET /admin/spaces/:id`.
  - link dialog validation: in that dialog click «ربط»/«Link» with no person → field error «اختر شخصًا»/«Choose a person». No request.
  - person picker: click role=combobox «الشخص»/«Person» → popover: search «بحث»/«Search» (placeholder «الاسم أو البريد»/«Name or email»), list «الأشخاص»/«People»; typing `zzzz` → «لا نتائج»/«No results» (`GET /admin/users?q=zzzz&state=active&limit=50`); choosing a person shows the consequence lines («تصبح جريس هاب موثّقة …»).
  - unlink an owner (verified only, e.g. `/2`): in the info notice «يعدّلها ⁨سامي الحلو⁩»/«Edited by ⁨سامي الحلو⁩», button «فك ربط ⁨سامي الحلو⁩»/«Unlink ⁨سامي الحلو⁩» (spaceLinks.spaceOwners.unlink) → AlertDialog «فك ربط سامي الحلو من نور هب؟»/«Unlink سامي الحلو from Noor Hub?» (line is a skeleton while `GET /admin/spaces/:id` runs), «رجوع»/«Back», «فك الربط»/«Unlink» (**WRITES** `DELETE /admin/spaces/:id/owners/:userId`).
  - prices sheet: button text «تعديل»/«Edit», aria-label «تعديل الأسعار المعلنة»/«Edit Published prices» (spaces.editor.section.editNamed + sectionNames.prices) → Sheet «تعديل الأسعار المعلنة»/«Edit the published prices». On /32 the card's empty action «إضافة سعر»/«Add a price» opens it instead.
  - prices rows: in the sheet «إضافة سعر»/«Add a price» adds a row; remove icon aria-label «حذف السعر 1»/«Remove price 1»; link «أضف وردية»/«Add a shift» opens the shifts sheet.
  - prices validation: add a row, leave «المبلغ (₪)»/«Amount (₪)» empty, «حفظ» → «أدخل المبلغ»/«Enter the amount». No request.
  - hours sheet: aria-label «تعديل ساعات العمل»/«Edit Opening hours» → Sheet «تعديل ساعات العمل»/«Edit the opening hours» (simple view: «من السبت إلى الخميس», «من»/«إلى» selects, checkbox «مفتوحة يوم الجمعة أيضًا»/«Also open on Friday»).
  - hours customise: in the hours sheet button «تخصيص الأيام»/«Set each day» → 7 day blocks, switches aria-label «مفتوحة يوم السبت»/«Open on Saturday» … «مفتوحة يوم الجمعة»/«Open on Friday» (hours.openOn), button «رجوع إلى الشكل البسيط»/«Back to the simple view».
  - hours unify dialog: customise → switch off «مفتوحة يوم الأحد»/«Open on Sunday» → «رجوع إلى الشكل البسيط» → AlertDialog «سيتم توحيد الساعات لكل الأيام. متابعة؟»/«Every day will take the same hours. Continue?», «رجوع»/«Back», «متابعة»/«Continue». No write.
  - hours none open: customise → switch all 7 off → «حفظ» → alert «افتح يومًا واحدًا على الأقل.»/«Open at least one day.». No request.
  - shifts sheet: the shifts card (no unverified space has shifts) empty action «إضافة وردية»/«Add a shift» (shifts.empty.action) → Sheet «تعديل الورديات»/«Edit the shifts» with row «الوردية 1»; empty Arabic name + «حفظ» → «اكتب اسم الوردية»/«Enter the shift’s name». (`?sheet=shifts` also works.)
  - amenities sheet: aria-label «تعديل المرافق»/«Edit Amenities» → Sheet «تعديل المرافق»/«Edit the amenities»: checkboxes named by amenity («إنترنت»/«Internet» …), «إضافة مرفق آخر»/«Add another amenity», link «إدارة قائمة المرافق»/«Manage the amenities list» (→ `/dashboard/admin/lookups?tab=amenities`). Empty own row + «حفظ» → «اكتب اسم المرفق بالعربية أو احذف هذا الصف».
  - about sheet: aria-label «تعديل عن المساحة»/«Edit About the space» → Sheet «تعديل: عن المساحة»/«Edit: about the space»; clear «الاسم بالإنجليزية»/«Name in English» + «حفظ» → «أدخل الاسم بالإنجليزية»/«Enter the English name».
  - location sheet: aria-label «تعديل الموقع»/«Edit Location» → Sheet «تعديل الموقع»/«Edit the location»: area combobox «المنطقة»/«Area», map aria-label «خريطة قطاع غزة: اضغط لوضع دبوس المساحة»/«Map of the Gaza Strip: tap to place the space’s pin», button «استخدم موقعي الحالي»/«Use my current location» (geolocation: granted → «نُقل الدبوس إلى موقعك الحالي. عدّله إن لزم.»; denied → «تعذّر معرفة موقعك. …»); clear «العنوان بالعربية» + «حفظ» → «أدخل العنوان بالعربية»/«Enter the Arabic address». On open: `GET /lookups`.
  - contacts sheet: aria-label «تعديل التواصل»/«Edit Contacts» → Sheet «تعديل التواصل»/«Edit the contacts»: «إضافة وسيلة تواصل»/«Add a contact», type select «النوع»/«Type», drag handle «ترتيب …»/«Reorder …», remove «حذف …»/«Remove …»; new empty row + «حفظ» → «املأ القيمة أو احذف هذه الوسيلة»/«Fill in the value, or remove this contact».
  - save unchanged: open any sheet, click «حفظ»/«Save» → toast «لم يتغيّر شيء»/«Nothing changed», sheet closes. No request.
  - discard dialog: open a sheet, change any field, click «رجوع»/«Back» (or Esc) → AlertDialog «تجاهل التغييرات؟»/«Discard the changes?», «رجوع»/«Back», «تجاهل التغييرات»/«Discard changes». No write.
  - leave dialog: open a sheet, change a field, then `history.back()` → AlertDialog «مغادرة الصفحة مع تغييرات غير محفوظة؟»/«Leave with unsaved changes?», «البقاء»/«Stay», «المغادرة»/«Leave». No write.
  - photos manage: button «إدارة الصور»/«Manage photos» (spaces.editor.photos.manage) → edit mode: «اختر صورًا»/«Choose photos» (file input), limits line, sortable tiles, per tile remove aria-label «حذف الصورة 1»/«Delete Photo 1»; the button becomes «تم»/«Done». No write until a file is chosen / removed / moved.
  - photo remove dialog: manage → «حذف الصورة 1»/«Delete Photo 1» → AlertDialog «حذف هذه الصورة؟»/«Delete this photo?», «رجوع»/«Back», «حذف»/«Delete» (**WRITES** `DELETE /admin/spaces/:id/photos/:photoId`). Spaces 10–25, 32–38 have one photo, so the line «الصورة التالية تصبح الغلاف.»/«The next photo becomes the cover.» never shows there.
  - stale confirm: on `/10#prices` button «ما زالت صحيحة»/«Still correct» — **WRITES** `POST /admin/spaces/10/prices/confirm`.
  - report notice actions (`/32?report=4#report`): button «تم التصحيح»/«Corrected» (**WRITES** `PATCH /admin/data-reports/4`); links «فتح البلاغ للرد»/«Open the report to reply», «العودة إلى البلاغات»/«Back to the reports».
- requests on load: `GET /admin/spaces/:id`, `GET /admin/spaces/:id/photos`, `GET /admin/amenities`, `GET /admin/governorates` (+ `GET /admin/data-reports/:reportId` with `?report=`). On submit: `PUT /admin/spaces/:id/prices`, `PUT …/hours` (hours and shifts), `PUT …/amenities`, `PUT …/contacts`, `PATCH /admin/spaces/:id` (about, location); photos `POST …/photos` (multipart `photo`), `DELETE …/photos/:photoId`, `PUT …/photos/order`; confirm `POST …/{profile|hours|prices|amenities|contacts}/confirm`.
- empty/other notes: top bar h1 = the space's name once loaded («تعديل مساحة»/«Edit space» before); breadcrumb «المساحات» › name. Section index (≥1024 only): nav «أقسام الملف»/«Profile sections». Header badges «غير موثّقة»/«Unverified» or «موثّقة»/«Verified»; meter «اكتمال الملف»/«Profile completeness»; issues nav «ما بقي»/«Still to do». Verified notice links «عرض في الموقع»/«View on the site» and «بلاغات ⁨نور هب⁩»/«⁨Noor Hub⁩’s reports» (→ `/dashboard/admin/reports?space=2`).

## Space owners — /dashboard/admin/owners   (role: admin)
- example URLs: `/dashboard/admin/owners`, `/dashboard/admin/owners?sheet=add`
- params: `q` (name or email, 1–80), `state` = `active` | `suspended`, `page`, `sheet=add` (opens the add sheet; removed when it closes). `role` is ignored (fixed to owner).
- states by URL:
  - list (7 rows, 1 page, newest first: رنا الخطيب, دعاء السقا, يوسف حمدان, خالد البطش, محمد أبو شعبان, سامي الحلو (12 spaces), أحمد الشوا): `/dashboard/admin/owners`
  - add sheet open: `/dashboard/admin/owners?sheet=add`
  - search, no result: `/dashboard/admin/owners?q=zzzz` → «لا يوجد أصحاب مساحات يطابقون البحث»/«No space owners match» + «مسح الفلاتر»/«Clear filters»
  - filter, no result: `/dashboard/admin/owners?state=suspended`
  - one owner: `/dashboard/admin/owners?q=demo-directory-owner%40example.com` (the users page's «فك روابطه» lead lands like this)
- states by click:
  - add owner sheet: button «إضافة مالك»/«Add owner» (spaceLinks.addOwner.open) → Sheet «إضافة مالك»/«Add owner», close «إغلاق»/«Close», fields «الاسم»/«Name», «البريد الإلكتروني»/«Email address», «المساحة»/«Space» (combobox «اختر المساحة»/«Choose the space»), notice «سيُنشأ حساب ويظهر رمز مرور مؤقت مرة واحدة — جهّز طريقة تسليمه.», submit «إنشاء حساب وربط»/«Create account and link». On open: `GET /admin/spaces?limit=50`. All widths.
  - add owner validation: submit the empty sheet → «أدخل الاسم»/«Enter the name», «أدخل البريد الإلكتروني»/«Enter the email», «اختر المساحة»/«Choose the space»; email `abc` → «أدخل بريدًا صحيحًا، مثل name@example.com». No request.
  - email has an account: name any, email `demo-user@example.com`, choose a space, submit → `POST /admin/owners` refused 409 `EMAIL_HAS_ACCOUNT` (**sends a POST; the server writes nothing**) → `GET /admin/users?email=demo-user%40example.com` → box «لهذا البريد حساب»/«This email has an account» + «تأكّد أنه الشخص المقصود: سيصبح مالكًا لهذه المساحة», submit becomes «ترقية وربط»/«Upgrade and link» (that one **WRITES**).
  - already an owner: email `garden.owner@example.com` → refused `ALREADY_OWNER` (no write) → `GET /admin/users?email=garden.owner%40example.com` → email field error «هذا البريد لمالك مسبقًا.»/«This email is already an owner’s.» + link-button «اربطه بالمساحة»/«Link them to the space» → closes the sheet, opens the link dialog «ربط ⁨رنا الخطيب⁩ بمساحة».
  - admin email: `baselghonaim@gmail.com` → refused `ACCOUNT_IS_ADMIN` (no write) → «هذا البريد لحساب أدمن، ولا يُربط أدمن بمساحة.».
  - temporary password dialog: only after a successful `POST /admin/owners` (**WRITES**: creates an account). To show it without writing, answer that POST with 201 `{"success":true,"data":{"userId":999,"temporaryPassword":"Tmp-4Kq9-x7Lm"}}` → Dialog «كلمة المرور المؤقتة»/«Temporary password» (no close button; Esc/outside ignored), «نسخ»/«Copy», radio group «طريقة التسليم»/«How it was handed over»: «واتساب»/«WhatsApp», «شفهيًا»/«In person», «أخرى»/«Other»; «تم»/«Done» held with «انسخها أولًا — لن تظهر مرة أخرى»/«Copy it first — it won’t be shown again»; «تم» sends `POST /admin/users/999/temporary-password/handover` (stub too).
  - row menu: icon button aria-label «إجراءات: ⁨رنا الخطيب⁩»/«Actions: ⁨رنا الخطيب⁩» (spaceLinks.ownerActions.menu) → items «ربط بمساحة»/«Link to a space», separator, one destructive «فك الربط من جاردن سبييس»/«Unlink from Garden Space» per space (ownerActions.unlinkFrom; سامي الحلو has 12). Table ≥768, card <768.
  - link from person: row menu → «ربط بمساحة» → Dialog «ربط ⁨رنا الخطيب⁩ بمساحة»/«Link ⁨رنا الخطيب⁩ to a space», «مساحة واحدة في كل مرة.»/«One space at a time.», field «المساحة»/«Space» (combobox «اختر مساحة»/«Choose a space»), submit «ربط»/«Link» (**WRITES**); empty submit → «اختر مساحة»/«Choose a space». On open: `GET /admin/spaces?limit=50`.
  - unlink from menu: row menu → «فك الربط من جاردن سبييس» → AlertDialog «فك ربط رنا الخطيب من جاردن سبييس؟»/«Unlink رنا الخطيب from Garden Space?», «رجوع»/«Back», «فك الربط»/«Unlink» (**WRITES**).
  - state chips: radio group «الحالة»/«Status»: «الكل», «نشط», «موقوف» / «All», «Active», «Suspended».
  - search: field «بحث»/«Search», placeholder «الاسم أو البريد»/«Name or email».
- requests on load: `GET /admin/users?role=owner&page=1` (+ `q`, `state`). On submit: `POST /admin/owners {name,email,spaceId[,upgradeExisting]}`.
- empty/other notes: intro line (spaceLinks.ownersList.intro); count «عدد أصحاب المساحات: 7»/«Space owners: 7». Empty (stub `data:[]`): «لا يوجد أصحاب مساحات بعد»/«No space owners yet» + link-button «إضافة مالك» (`?sheet=add`). Failure «تعذّر تحميل أصحاب المساحات»/«We couldn’t load the space owners». Repeated refused POSTs may meet the rate limit (429).

## Users — /dashboard/admin/users   (role: admin)
- example URLs: `/dashboard/admin/users`, `/dashboard/admin/users?page=2`
- params: `q` (name or email), `role` = `user` (42) | `owner` (7) | `admin` (1), `state` = `active` | `suspended` (0), `page` (50 rows → 3 pages; `role=user` → 3 pages).
- states by URL:
  - page 1 (newest first: Basel = you, then عز الدين ضاهر, يحيى الخضري, …; owners 50, 49, 48, 47, 46 are on page 1): `/dashboard/admin/users`
  - pages 2/3: `/dashboard/admin/users?page=2`, `/dashboard/admin/users?page=3`
  - search, no result: `/dashboard/admin/users?q=zzzz` → «لا يوجد مستخدمون يطابقون البحث»/«No users match» + «مسح الفلاتر»
  - filter, no result: `/dashboard/admin/users?state=suspended`
  - role filter: `/dashboard/admin/users?role=owner`, `…?role=admin` (only your row)
  - reception person: `/dashboard/admin/users?q=demo-reception%40example.com` (ليلى النجار)
  - owner: `/dashboard/admin/users?q=garden.owner%40example.com` (رنا الخطيب)
- states by click:
  - row menu (plain user, e.g. عز الدين ضاهر on page 1): icon button aria-label «إجراءات: ⁨عز الدين ضاهر⁩»/«Actions: ⁨عز الدين ضاهر⁩» (spaceLinks.userActions.menu) → items «تغيير الدور»/«Change role», «ربط بمساحة»/«Link to a space», «إصدار كلمة مرور مؤقتة»/«Issue a temporary password», separator, «إيقاف»/«Suspend» (destructive). Your own row has no menu, only «أنت»/«You». Table ≥1024, cards below.
  - owner row menu (رنا الخطيب): «تغيير الدور» held, reason under it «دوره يتبع روابطه — فُكّ ربطه أولًا»/«Their role follows their links — unlink them first», then item-link «فك روابطه»/«Unlink them» → `/dashboard/admin/owners?q=garden.owner%40example.com`.
  - reception row menu (`?q=demo-reception%40example.com`): «تغيير الدور» held «يعمل في مكتب استقبال — يفكّه مالك المساحة أولًا»/«They work a front desk — its space’s owner ends that first».
  - role dialog: plain user → «تغيير الدور» → AlertDialog «جعل ⁨عز الدين ضاهر⁩ أدمن؟»/«Make ⁨عز الدين ضاهر⁩ an admin?», «رجوع»/«Back», «جعله أدمن»/«Make them an admin» (**WRITES** `PUT /admin/users/:id/role`). The «إعادة … مستخدمًا؟» variant needs a second admin (**WRITES** first).
  - link dialog from person: «ربط بمساحة» → Dialog «ربط ⁨عز الدين ضاهر⁩ بمساحة» (as on the owners page; submit **WRITES**).
  - issue password confirm: «إصدار كلمة مرور مؤقتة» → AlertDialog «إصدار كلمة مرور مؤقتة لـ ⁨عز الدين ضاهر⁩؟»/«Issue a temporary password for ⁨عز الدين ضاهر⁩?», «رجوع»/«Back», «إصدار»/«Issue» (**WRITES** `POST /admin/users/:id/temporary-password`: revokes their password and sessions).
  - one-time password dialog (issued): **WRITES** — only after «إصدار»; or answer that POST with 200 `{"success":true,"data":{"temporaryPassword":"Tmp-4Kq9-x7Lm"}}` → «كلمة المرور المؤقتة» with «سلّمها له بعد التأكد من هويته؛ سيُطلب منه تغييرها عند الدخول التالي.» (same controls as on the owners page).
  - suspend dialog: «إيقاف» → AlertDialog «إيقاف ⁨عز الدين ضاهر⁩؟»/«Suspend ⁨عز الدين ضاهر⁩?» (an owner adds «تبقى مساحاته موثّقة…», reception adds «يبقى رابطه بمكتب الاستقبال…»), «رجوع»/«Back», «إيقاف»/«Suspend» (**WRITES** `PUT /admin/users/:id/suspended`). «استرجاع الحساب» needs a suspended account (**WRITES** first).
  - role chips: radio group «الدور»/«Role»: «الكل», «مستخدم», «مالك», «أدمن» / «All», «User», «Owner», «Admin».
  - state chips: radio group «الحالة»/«Status»: «الكل», «نشط», «موقوف» / «All», «Active», «Suspended».
- requests on load: `GET /admin/users?page=1` (+ `q`, `role`, `state`).
- empty/other notes: count «عدد المستخدمين: 50»/«Users: 50». Empty (stub) «لا يوجد مستخدمون بعد»/«No users yet»; failure «تعذّر تحميل المستخدمين»/«We couldn’t load the users».

## Data reports — /dashboard/admin/reports   (role: admin)
- example URLs: `/dashboard/admin/reports`, `/dashboard/admin/reports?open=4`
- params: `status` = `open` (9) | `decided` (9) (else all 18); `field` = `PRICES` | `HOURS` | `CONTACT` | `LOCATION` | `AMENITIES` | `OTHER` (uppercase; `OTHER` → 2); `space` = id (`26` → 3); `handledBy` = `admin` (11) | `owner` (7); `page`; `open` = report id (opens its sheet).
- states by URL:
  - all (18, one page, no page 2): `/dashboard/admin/reports`
  - open / decided chips: `…/reports?status=open`, `…/reports?status=decided`
  - filters on (tags shown): `…/reports?field=OTHER`, `…/reports?space=26`, `…/reports?handledBy=admin`
  - no match: `/dashboard/admin/reports?field=PRICES&space=38` → «لا توجد بلاغات تطابق الفلاتر»/«No reports match the filters» + «عرض الكل»/«Show all»
  - report to decide (unverified): `/dashboard/admin/reports?open=4` (Jreas Hub · Prices), `…?open=11` (Al-Salam Hub · Opening hours)
  - read-only (verified space): `/dashboard/admin/reports?open=1` (Pal Hub · Opening hours)
  - decided: `…?open=9` (Corrected), `…?open=13` (Not accepted)
- states by click:
  - open a report: row button text «فتح»/«Open» (unverified) or «عرض»/«View» (verified), no aria-label — scope it to the row/card (e.g. the row containing «جريس هاب»/«Jreas Hub») → Sheet title «جريس هاب · الأسعار»/«Jreas Hub · Prices» (dataReports.sheet.adminTitle) + badge «جديد»/«New», link «تعديل الحقل»/«Edit the field» (→ `/dashboard/admin/spaces/32?report=4#report`), textarea field «ردّ فريقنا»/«Reply from our team», buttons «تم التصحيح»/«Corrected», «لم يُعتمد»/«Not accepted» (**WRITE** `PATCH /admin/data-reports/:id`), close «إغلاق»/«Close». Opening writes nothing. All widths.
  - dismiss validation: in the sheet click «لم يُعتمد»/«Not accepted» with an empty reply → «اكتب السبب؛ هو ما سيقرؤه صاحب البلاغ.»/«Write the reason; it’s what the reporter will read.». No request.
  - read-only sheet: «عرض»/«View» on a verified space's row (or `?open=1`) → alert «مساحة موثّقة — يقرّر مالكها هذا البلاغ. للاطلاع فقط.»/«Verified space — its owner decides this report. For reference only.» + link «عرض المساحة»/«View the space»; no decision buttons.
  - status chips: radio group «تصفية حسب الحالة»/«Filter by status»: «الكل», «جديدة», «تمت المراجعة» / «All», «New», «Reviewed».
  - space filter (≥768 inline): role=combobox named «المساحة»/«Space», showing «كل المساحات»/«All spaces» → popover search (`GET /admin/spaces?limit=50` on open; `q=` as you type).
  - field select (≥768 inline): role=combobox «الحقل»/«Field» → «كل الحقول»/«All fields», «الأسعار», «ساعات العمل», «التواصل», «الموقع», «المرافق», «أخرى» / «Prices», «Opening hours», «Contact», «Location», «Amenities», «Other».
  - handled-by chips (≥768 inline): radio group «يعالجه»/«Handled by»: «الكل», «الإدارة», «المالك» / «All», «The admin», «The owner».
  - filter tags (any filter on, all widths): remove buttons aria-label «إزالة فلتر المساحة»/«Remove the space filter», «إزالة فلتر الحقل»/«Remove the field filter», «إزالة فلتر «يعالجه»»/«Remove the handled-by filter»; button «مسح الفلاتر»/«Clear filters».
  - filters sheet (<768 only): button text «الفلاتر»/«Filters», aria-label «الفلاتر» or «فلتر واحد مطبّق»/«1 filter applied» (payments.ledger.filters.applied) → bottom Sheet «الفلاتر»: space, field, handled-by, «عرض 18 بلاغًا»/«Show 18 reports», «مسح الفلاتر», close «إغلاق».
- requests on load: `GET /admin/data-reports?page=1&limit=20` (+ `status=OPEN|DECIDED`, `field`, `spaceId`, `handledBy=ADMIN|OWNER`); `?open=` for a report not on the page → `GET /admin/data-reports/:id`. On decide: `PATCH /admin/data-reports/:id {status, note?}`.
- empty/other notes: intro (dataReports.admin.intro); count «18 بلاغًا»/«18 reports». Empty (stub) «لا توجد بلاغات»/«No reports»; failure «تعذّر تحميل البلاغات»/«We couldn’t load the reports». Table ≥1024, cards below.

## Lookups — /dashboard/admin/lookups   (role: admin)
- example URLs: `/dashboard/admin/lookups`, `/dashboard/admin/lookups?tab=amenities`
- params: `tab` = `amenities` (anything else = governorates; choosing governorates removes the param).
- states by URL:
  - governorates tab: `/dashboard/admin/lookups` — 5 cards: North Gaza (1 area), Gaza City (11, Al-Shuja'iyya hidden), Deir al-Balah (Middle Area) (5), Khan Younis (6, 4 hidden), Rafah (hidden badge «مخفية»/«Hidden», 2 hidden areas).
  - amenities tab: `/dashboard/admin/lookups?tab=amenities` — 8 amenities, all active.
  - loading / failed: hold or 500 `GET /admin/governorates` → «تعذّر تحميل المحافظات»/«We couldn’t load the governorates» + «إعادة المحاولة»; amenities: «تعذّر تحميل المرافق»/«We couldn’t load the amenities».
  - empty: stub `data:[]` → «لا محافظات بعد»/«No governorates yet» + «أضف أول محافظة، ثم مناطقها.»; «لا مرافق بعد»/«No amenities yet» + «أضف أول مرفق.».
- states by click:
  - tabs: tablist aria-label «القوائم»/«Lookups»; tabs «المحافظات والمناطق»/«Governorates and areas», «المرافق»/«Amenities» (writes `?tab=`).
  - add governorate sheet: button «إضافة محافظة»/«Add governorate» (lookups.governorates.add, foot of the list) → Sheet «إضافة محافظة»/«Add governorate», fields «الاسم بالعربية»/«Name in Arabic», «الاسم بالإنجليزية»/«Name in English», «حفظ»/«Save», close «إغلاق»/«Close».
  - add governorate validation: «حفظ» on the empty sheet → «أدخل الاسم بالعربية»/«Enter the Arabic name», «أدخل الاسم بالإنجليزية»/«Enter the English name». No request.
  - edit governorate: ghost button text «تعديل»/«Edit», aria-label «تعديل: ⁨غزة⁩»/«Edit: ⁨Gaza City⁩» (lookups.row.editName) → Sheet «تعديل محافظة»/«Edit governorate» (+ field «الترتيب»/«Position», helper «من 1 إلى 5»/«From 1 to 5»).
  - add area: button «إضافة منطقة»/«Add area» in each card (Gaza City card: the second) → Sheet «إضافة منطقة»/«Add area», description = the governorate's English name («Gaza City»).
  - edit area: aria-label «تعديل: ⁨الرمال⁩»/«Edit: ⁨Al-Rimal⁩» → Sheet «تعديل منطقة»/«Edit area».
  - reorder arrows: icon buttons «تحريك لأعلى: ⁨غزة⁩ — 2 من 5»/«Move up: ⁨Gaza City⁩ — 2 of 5», «تحريك لأسفل: ⁨غزة⁩ — 2 من 5»/«Move down: ⁨Gaza City⁩ — 2 of 5» (lookups.row.moveUp/moveDown; areas likewise within their card; first's up and last's down disabled) — **WRITES** `PUT /admin/governorates/order` / `PUT /admin/governorates/:id/areas/order`.
  - shown switch: aria-label «ظاهرة: ⁨غزة⁩»/«Shown: ⁨Gaza City⁩» (lookups.row.shown) — **WRITES** `PATCH /admin/governorates/:id` / `PATCH /admin/areas/:id`.
  - add amenity sheet (amenities tab): «إضافة مرفق»/«Add amenity» → Sheet «إضافة مرفق»/«Add amenity»: radio group «الأيقونة»/«Icon» («واي فاي»/«Wi-Fi», «برق»/«Lightning», «شمس»/«Sun», «قابس كهرباء»/«Power plug», «فنجان قهوة»/«Coffee cup», «أشخاص»/«People», «لوح عرض»/«Presentation board», «قبعة تخرّج»/«Graduation cap»), names; empty «حفظ» → «اختر أيقونة»/«Choose an icon» + name errors. No request.
  - edit amenity: aria-label «تعديل: ⁨إنترنت⁩»/«Edit: ⁨Internet⁩» → Sheet «تعديل مرفق»/«Edit amenity».
  - amenity arrows / active switch: «تحريك لأعلى: ⁨كهرباء مستقرة⁩ — 2 من 8»/«Move up: ⁨Stable power⁩ — 2 of 8»; switch «نشط: ⁨إنترنت⁩»/«Active: ⁨Internet⁩» (lookups.amenities.row.activeName) — **WRITES** (`PUT /admin/amenities/order`, `PATCH /admin/amenities/:id`).
- requests on load: governorates tab `GET /admin/governorates`; amenities tab `GET /admin/amenities` (only the active tab mounts). On submit: `POST /admin/governorates`, `PATCH /admin/governorates/:id`, `POST /admin/areas`, `PATCH /admin/areas/:id`, `POST /admin/amenities`, `PATCH /admin/amenities/:id`.
- empty/other notes: hint line under the tabs (lookups.governorates.hint / lookups.amenities.hint). Names in aria-labels follow the UI language.

## Audit log — /dashboard/admin/audit   (role: admin)
- example URLs: `/dashboard/admin/audit`, `/dashboard/admin/audit?page=2`
- params: `q` (1–80, the target), `period=all` (else last 30 days), `actor` = user id (e.g. `1`), `type` = `spaces` | `owners` | `accounts` | `lookups` | `reports` | `platformSettings`, `page`.
- states by URL:
  - last 30 days (153 events → 8 pages): `/dashboard/admin/audit`; page 2: `…/audit?page=2`
  - all time (161 → 9 pages): `/dashboard/admin/audit?period=all`
  - actor: `/dashboard/admin/audit?actor=1`; type: `…/audit?type=spaces`, `…/audit?type=reports`
  - no match: `/dashboard/admin/audit?type=lookups` (or `type=platformSettings`, `q=zzzz`) → «لا توجد أحداث تطابق الفلاتر»/«No events match the filters»
  - failed: 500 → «تعذّر تحميل سجل التدقيق»/«Couldn’t load the audit log» + «إعادة المحاولة»
- states by click:
  - period select (≥768 inline): role=combobox «الفترة»/«Period» → «آخر 30 يومًا»/«Last 30 days», «كل الفترة»/«All time».
  - actor select (≥768 inline; shown with ≥2 actors, 8 now): role=combobox «المنفّذ»/«Actor» → «الكل»/«All» + people.
  - type select (≥768 inline): role=combobox «نوع الإجراء»/«Action type» → «كل الإجراءات»/«All actions», «المساحات»/«Spaces», «أصحاب المساحات»/«Space owners», «الحسابات»/«Accounts», «القوائم»/«Lookups», «بلاغات البيانات»/«Data reports», «إعدادات المنصة»/«Platform settings».
  - filters sheet (<768 only): button text «الفلاتر»/«Filters», aria-label «الفلاتر» or «فلتر واحد مطبّق»/«1 filter applied» (audit.filters.applied) → bottom Sheet «الفلاتر»: the three selects, «عرض 153 نتيجة»/«Show 153 results», «مسح الفلاتر», close «إغلاق».
  - search: field «بحث في الهدف»/«Search the target», placeholder «مساحة، شخص، قائمة…»/«A space, a person, a lookup…».
- requests on load: `GET /admin/audit-log?period=LAST_30_DAYS&page=1&limit=20` (+ `period=ALL`, `q`, `actor`, `actions=<comma list>` for `type`).
- empty/other notes: intro (audit.intro.platform); count «الأحداث: 153»/«Events: 153». Empty (stub, no filter) «لا أحداث بعد»/«No events yet». Target links: a space → its editor, a person → `/dashboard/admin/users?q=<name>`, a report → `/dashboard/admin/reports?open=<id>`. Table ≥768, cards below.

## Platform settings — /dashboard/admin/settings   (role: admin)
- example URLs: `/dashboard/admin/settings`, `/dashboard/admin/settings#staleness`
- params: none; card anchors `#contact`, `#staleness`, `#defaults`.
- states by URL:
  - ready: three cards «التواصل مع المنصة»/«Platform contact» (email baselghonaim17@gmail.com, WhatsApp +970597063545), «حداثة البيانات»/«Data freshness» (30 / 60), «الإعدادات الافتراضية للمساحات الجديدة»/«Defaults for new spaces».
  - one card loading / failed: hold or 500 one of the three GETs → that card's skeleton / alert «تعذّر تحميل «التواصل مع المنصة»»/«Couldn’t load “Platform contact”» + «إعادة المحاولة»; the other cards stay.
- states by click:
  - unsaved: change any field → badge «تغييرات غير محفوظة»/«Unsaved changes» + button «تجاهل التغييرات»/«Discard changes» in that card. No write.
  - staleness validation: clear «الأسعار (أيام)»/«Prices (days)» → card «حفظ»/«Save» → «أدخل عدد الأيام»/«Enter the number of days»; `999` → «من 1 إلى 365 يومًا»/«From 1 to 365 days». No request.
  - contact validation: email `abc` → «أدخل بريدًا صحيحًا»/«Enter a valid email»; WhatsApp `12` → «رقم غير صالح، مثل +970 59 000 0000»/«Not a valid number, e.g. +970 59 000 0000». No request.
  - defaults: switch «تسجيل خروج تلقائي عند الإغلاق»/«Automatic check-out at closing», radio group «تقريب الزيارات»/«Visit rounding» («تقريب لأعلى بعد عدد من الدقائق», «لأقرب نصف ساعة», «بالدقيقة» / «Round up after a number of minutes», «To the nearest half hour», «By the minute»; minutes field «بعد (دقائق)»/«After (minutes)» under the first), switch «لا يتجاوز سعر اليوم»/«Never more than the day price». No write until «حفظ».
- requests on load: `GET /admin/settings/contact`, `GET /admin/settings/staleness`, `GET /admin/settings/new-space-defaults`. On submit (per card, **WRITES**): `PUT` the same path.
- empty/other notes: one column, max 3xl.

## 404 inside the dashboard — /dashboard/admin/*   (role: admin)
- example URLs: `/dashboard/admin/nope`, `/dashboard/admin/spaces/new/x`, `/dashboard/admin/spaces/abc`, `/dashboard/admin/spaces/1` (deleted → API 404), `/dashboard/admin/spaces/9999`
- params: none.
- states by URL: not found: any above → inside the shell, empty state h1 «الصفحة غير موجودة»/«Page not found» + «ربما تغيّر الرابط أو حُذفت الصفحة.»/«The link may have changed or the page was removed.» (status.notFound); no buttons. For `/spaces/1` and `/spaces/9999` the top bar still says «تعديل مساحة»/«Edit space» with the breadcrumb; for `/nope` and `/spaces/abc` the top bar title is empty.
- states by click: none.
- requests on load: none (or `GET /admin/spaces/:id` → 404).
- empty/other notes: route error: abort the page's lazy module (dev: e.g. `GET /src/pages/dashboard/admin/SpacesPage.tsx…`) before navigating → «لا يوجد اتصال بالإنترنت»/«No internet connection» + «إعادة المحاولة»/«Try again» inside the shell; a thrown non-chunk error → «حدث خطأ غير متوقع»/«Something went wrong». A non-admin on `/dashboard/admin` gets the bare 403 «لا تملك صلاحية الوصول إلى هذه الصفحة».

---

## Dashboard shells (AdminLayout → DashboardLayout)   (role: admin)
- Skip link: first Tab stop, `a[href="#main"]` «تخطَّ إلى المحتوى»/«Skip to content» (site.skipToContent); visible only while focused. `main#main` takes the focus on each navigation.
- Sidebar: `nav[data-slot="sidebar"]` aria-label «لوحة إدارة المنصة»/«Platform admin» (dashboard.adminNavigation); `data-mode` = `desktop` (≥1024, expanded, 248 px) | `tablet` (768–1023, 64 px icon rail) | `phone` (drawer).
- Header: full logo (expanded and drawer) or the mark alone (rail); sr-only «مساحة»/«Masaha» (site.wordmark); caption «إدارة المنصة»/«Platform admin» (dashboard.platformAdmin; sr-only on the rail).
- Groups and items (`a[data-slot="sidebar-menu-button"]`, current one `aria-current="page"` / `data-active="true"`): «نظرة عامة»/«Overview» (no group); group «المساحات»/«Spaces»: «المساحات»/«Spaces», «أصحاب المساحات»/«Space owners», «بلاغات البيانات»/«Data reports» (badge `[data-slot="sidebar-menu-badge"]` = 7, described «7 بلاغات بانتظار الإدارة»/«7 reports waiting for the admin» — dashboard.badges.reportsForAdmin); group «المنصة»/«The platform»: «المستخدمون»/«Users», «القوائم»/«Lookups», «سجل التدقيق»/«Audit log», «إعدادات المنصة»/«Platform settings». The Spaces item stays current on `/spaces/new` and `/spaces/:id`.
- Top bar (`header`, sticky): <768 the drawer trigger; the page's h1 (and the editor's actions); from 768 the language toggle, theme toggle and account button.
- states by click:
  - drawer (<768): button [css=`[data-slot="sidebar-trigger"]`; aria-label «القائمة»/«Menu» (dashboard.menu)] → Sheet from the start side (role=dialog, sr-only title «لوحة إدارة المنصة»/«Platform admin»), no close button (Esc / overlay / choosing a link closes it). Head: account row button (aria-label «قائمة الحساب: ⁨Basel⁩»/«Account menu: ⁨Basel⁩», shows «Basel · أدمن»/«Basel · Admin» and the email); then logo, groups; foot: language and theme toggles.
  - drawer account menu (<768): drawer → account row → the account menu below.
  - account menu (≥768): avatar button aria-label «قائمة الحساب: ⁨Basel⁩»/«Account menu: ⁨Basel⁩» (users.menu; shows «B») → role=menu: label «Basel · أدمن»/«Basel · Admin» (users.nameWithRole) + `baselghonaim@gmail.com`; items «الموقع العام»/«Public site» (→ `/`), «إعدادات حسابي»/«Account settings» (→ `/me`), «تسجيل الخروج»/«Sign out» (**WRITES** `POST /auth/logout`, ends the session — avoid; a 500 stub shows «تعذّر تسجيل الخروج»/«Couldn’t sign out» inside the menu).
  - rail tooltip (768–1023): hover or focus a rail item → Tooltip with its name (e.g. «المساحات»), on the page's side; group names sr-only, groups divided by lines.
  - theme toggle: icon button aria-label «المظهر الداكن»/«Dark theme» while light, «المظهر الفاتح»/«Light theme» while dark (preferences.switchTheme) — localStorage only. ≥768 in the top bar, <768 in the drawer's foot.
  - language toggle: button whose text is the other language: «English» in the Arabic UI, «العربية» in the English UI (preferences.languageName of the other catalogue; `bdi[lang]`) — localStorage only. Same places as the theme toggle.
- requests on load: `POST /auth/refresh`, `GET /admin/data-reports?status=OPEN&handledBy=ADMIN&page=1&limit=1`.
- other notes: toasts region aria-label «الإشعارات»/«Notifications», close «إغلاق الإشعار»/«Close notification» (status.toasts). The phone action bar (`[data-slot="page-action-bar"]`) is never filled on admin pages.

---

## Showcase — /__showcase (development only)
- URL scheme: `/__showcase` (every section) · `/__showcase/<category>` · `/__showcase/<category>/<slug>`. Unknown category/slug → redirect to `/__showcase` keeping the query.
- Page params: `theme` = `light` | `dark` (default: what `<html>` shows), `lang` = `ar` | `en` (sets direction; default `<html lang>`), `width` = `360` | `768` | `1280` (iframe width; default 1280). E.g. `/__showcase/overlays/dialog?theme=dark&lang=en&width=360`.
- The page shows the view in an iframe: `/__showcase/preview[/<category>[/<slug>]]?theme=…&lang=…` — capture the preview URL directly at the viewport you want (it ignores `width`).
- Toolbar (English only, `fixtures.json` toolbar): native selects labelled «Preview theme», «Preview direction», «Preview width»; heading «Masaha design system showcase»; nav aria-label «Showcase sections» with «Every section, in build order»; <768 the nav is a drawer opened by «Open the list of showcase sections» (close «Close the list of showcase sections»).
- Categories and slugs (44 entries):
  - icons: `icons`
  - actions: `button`, `toggles`, `dropdown-menu`
  - fields: `field`, `input`, `textarea`, `select`, `checkbox`, `radio-group`, `switch`, `toggle-group`, `segmented-control`, `combobox`, `calendar`, `date-picker`, `sortable`
  - display: `badge`, `card`, `separator`, `avatar`, `stat-card`, `filter-tag`, `meter`, `logo`
  - data: `table`, `data-table`, `bar-chart`, `heatmap`
  - feedback: `skeleton`, `spinner`, `alert`, `toast`, `empty-state`, `refreshing`
  - overlays: `tooltip`, `dialog`, `alert-dialog`, `sheet`, `popover`
  - navigation: `tabs`, `breadcrumb`, `pagination`, `sidebar`
- states by click (inside the preview; strings from `fixtures.json` samples.ar / samples.en):
  - dialog (`overlays/dialog`): button «تغيير اسم المساحة»/«Rename the space».
  - alert dialog (`overlays/alert-dialog`): button «إيقاف عضوية سارة الحلو»/«Deactivate Sara Helou».
  - sheets (`overlays/sheet`): «فتح درج التنقل»/«Open the navigation drawer», «فتح لوح التفاصيل»/«Open the details panel», «فتح لوح الفلاتر»/«Open the filter panel».
  - popover (`overlays/popover`): «عرض ساعات العمل»/«Show the opening hours».
  - tooltip (`overlays/tooltip`): hover icon buttons «البحث في المشتركين»/«Search the members list», «تسجيل الخروج من الحساب»/«Sign out of your account» (one tooltip is always open: «نسخ رابط المساحة»/«Copy the space link»).
  - dropdown menu (`actions/dropdown-menu`): icon button «إجراءات البلاغ عن مساحة الريادة»/«Actions for the report about Riyada Space»; button «خيارات عرض الجدول»/«Table view options» (submenu «تصدير الجدول»/«Export the table»).
  - toasts (`feedback/toast`): «إشعار عادي», «نجاح», «معلومة», «تنبيه», «خطأ», «مع إجراء» / «Plain toast», «Success toast», «Information toast», «Warning toast», «Error toast», «Toast with an action».
- requests: none (fixtures only).
