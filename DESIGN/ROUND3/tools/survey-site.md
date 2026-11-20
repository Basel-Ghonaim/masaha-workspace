# Survey — public site, account area, auth (focus) pages

Read from `C:\dev\masaha\app-design\apps\web\src` and the DB copy `masaha_dr_dev`, 2026-11-13.
14 routes: `/`, `/spaces` (list + map), `/spaces/:slug`, `/about`, `/privacy`, `*` (404), `/me/favorites`,
`/me/reports`, `/me`, `/login`, `/register`, `/forgot-password`, `/reset-password`, `/change-password`.

## Conventions for the script

- **Base**: the web dev server; this worktree's `apps/web/.env` has `WEB_PORT=5323`, API proxied to `3323` (repo defaults 5320/3320). API prefix `/api/v1` (axios baseURL), same origin.
- **Language**: `localStorage['masaha.language']` = `ar` | `en`, read before paint. Absent → `navigator.languages` → `ar`. So **headless Chrome with an en-US locale renders English unless the key is set**. **Theme**: `localStorage['masaha.theme']` = `light` | `dark` (absent → `prefers-color-scheme`). `<html lang dir data-theme>` reflect both. **A sign-in sets the language to the account's** (demo-user's is `ar`): set the key again after signing in, then reload.
- **Strings**: «ar» / «en» copied from the catalogue, key = `copy.<file>.<path>` (file = `shared/copy/{arabic,english}/<file>.ts`). A string that itself contains « » is given in `backticks`. `[[x]]` = value wrapped in U+2068…U+2069 (names); `⟦x⟧` = value wrapped in U+2066…U+2069 (emails, clocks, km). **Strip U+2066–U+2069 from innerText/aria-label before comparing.** `{x}` = plain inserted value.
- **Roles**: ToggleGroup (single) and SegmentedControl items are `role=radio`; Select trigger `role=combobox`, options `role=option`; DropdownMenu items `role=menuitem`; Sheet and Dialog are `role=dialog` named by their title. No AlertDialog on these pages.
- **Stable selectors**: every design-system part has `data-slot` — `[data-slot=sheet-content]`, `[data-slot=dialog-content]`, `[data-slot=dropdown-menu-content]`, `[data-slot=select-content]`, `[data-slot=combobox-content]`, `[data-slot=skeleton]`, `[data-slot=empty-state]`, `[data-slot=alert]`, `[data-slot=pagination]`, `[data-slot=sheet-close]`. Also `main#main`, `a[href="#main"]` (skip link), `[data-card-action] button` (the heart on a card), `aside#directory-filters`, `#directory-filters-form`, map marks `.map-mark[role=button]` (Leaflet marker icons), toasts `[data-sonner-toast]`.
- **Session**: sign in through `/login` or `POST /api/v1/auth/login` `{email,password}` → cookies `masaha_refresh` (path `/api/v1/auth`) and `masaha_session` (hint, path `/`). With the hint cookie, **every page load first sends `POST /api/v1/auth/refresh`** (answer `{success:true,data:{user,accessToken}}`). Demo user: `demo-user@example.com`, id 5, name «سلمى الأغا», role USER, language `ar`, has a password, no Google, no space link (so no «لوحة التحكم» / «Dashboard» item). Its password is the seed's `SEED_DEMO_PASSWORD` (not in the repo).
- **Mock envelope**: success `{"success":true,"data":…,"meta":{…}}` (lists: `meta:{currentPage,limit,totalPages, totalRecords,hasNextPage,hasPreviousPage}`); error `{"success":false,"error":{"type":"server","message":"x", "requestId":"00000000-0000-4000-8000-000000000000"}}`. 500 → `type:"server"`; 429 → `type:"rate_limit"` plus header `Retry-After: 30` (a countdown `⟦0:30⟧` shows and the retry/submit is disabled while it counts; without the header, a plain line); 404 → `not_found`; 401 → `unauthorized`; 409 → `conflict`; 422 → `validation` with `errors:{field:[code]}`. A failed request body's `requestId` shows as «رقم المرجع: {id}» / «Reference: {id}».
- **Transport rules**: timeout 15 s. A **GET** (or a request with `Idempotency-Key`) answered **5xx or with no answer is retried twice** (after 1 s, then 2 s): answer all 3 attempts with 500, and the error state appears ≈3 s later. A 4xx (429 included) is never retried. To show a skeleton, hold the request < 15 s (longer times out and is retried). Queries are not retried by TanStack (`retry:false`).
- **Writes**: favourite save/remove, report, profile, language, passwords, forgot-password are real writes on the DB copy: answer them from the script (204 / a mocked body) unless a real change is wanted.
- **Outside requests**: map tiles `https://tile.openstreetmap.org/{z}/{x}/{y}.png` (directory map, space page location); Google's button `https://accounts.google.com/gsi/client` (sign-in, register; a client id is set in this worktree, so the button and the «أو» / «or» divider show). Photos: `GET /api/v1/files/…` — keep them out of a blanket `/api/v1/**` failure route.
- **Widths**: phone < 768 (`md`), tablet 768–1023, desktop ≥ 1024 (`lg`).
- **Time**: "now" is Gaza time (UTC+2 in November). `space_hours.day_of_week` 0 = Sunday … 5 = Friday … 6 = Saturday. Staleness as of 2026-11-13: prices stale after 30 days, other groups after 60 days; an unverified space's stale prices are hidden, a verified one's shown with «قد يكون تغيّر» / «May have changed».
- **DB facts**: 37 listed spaces (id 1 `masaha-demo` is deleted; none hidden). Verified (has an OWNER): 2–9, 14, 16, 18, 22, 23, 26–31. Unverified: 10–13, 15, 17, 19–21, 24, 25, 32–38. No `space_occupancy` override and no open check-in exists, so a verified space with capacity and hours is «متاح» while open and «مغلق الآن» outside its hours; **FULL needs a mock**. Running announcements: `shati-sea-view` CLOSURE (since 2026-11-01, no end), `pal-hub` OFFER (until 2026-11-27).

---

## Home — `/`   (role: both)
- example URLs: `/`
- params: none read. (Its links write `/spaces?q=…`, `/spaces?open=1`, `/spaces?area=<id>`, `/spaces?view=map`.)
- states by URL:
  - default: `/` — h1 «اعثر على مساحة عمل في قطاع غزة» / «Find a workspace in the Gaza Strip» (copy.site.home.title); h2 «مفتوحة الآن» / «Open now» (copy.directory.home.openNow) with ≤ 6 cards; h2 «تصفّح حسب المنطقة» / «Browse by area» (copy.site.home.areas.title) — one card per area with spaces, then «كل المناطق» / «All areas»; owners' card «هل تدير مساحة عمل؟» / «Do you run a coworking space?».
  - spaces loading: hold `GET /api/v1/spaces?limit=6&openNow=true` → 6 card skeletons.
  - areas loading: hold `GET /api/v1/map/spaces` (or `GET /api/v1/lookups`) → 3 skeletons under «تصفّح حسب المنطقة».
  - spaces failed: 500 on `GET /api/v1/spaces?limit=6&openNow=true` → alert «تعذّر تحميل المساحات» / «We couldn’t load the spaces» (copy.directory.loadFailed) + reference + button «إعادة المحاولة» / «Try again» (copy.status.retry); 429 → line «محاولات كثيرة. انتظر قليلًا ثم حاول مرة أخرى.» / «Too many attempts. Please wait a moment and try again.» (copy.errors.rate_limit), or with `Retry-After` «محاولات كثيرة، حاول بعد ⟦0:30⟧» / «Too many attempts. Try again in ⟦0:30⟧.» (copy.forms.failure.retryIn).
  - none open: answer that GET with `data:[]` (or visit when every space is closed) → empty state «لا توجد مساحات مفتوحة الآن» / «No spaces open right now» + link «تصفّح كل المساحات» / «Browse all spaces» (copy.directory.home.empty).
  - areas failed: 500 on `GET /api/v1/map/spaces` or `GET /api/v1/lookups` → alert «تعذّر تحميل المناطق» / «We couldn’t load the areas» (copy.site.home.areas.failed) + «إعادة المحاولة».
- states by click:
  - heart, guest → sign-in prompt: [click `[data-card-action] button` = role=button name «حفظ [[name]] في المفضّلة» / «Save [[name]] to favourites» (copy.favorites.save)] → Dialog title «سجّل الدخول لحفظ المساحات في المفضّلة» / «Sign in to save spaces to your favourites» (copy.site.signInPrompt.favorite.title), links «إنشاء حساب» / «Create account» → `/register?next=%2F`, «تسجيل الدخول» / «Sign in» → `/login?next=%2F` (next = the current path + query), X button «إغلاق» / «Close» (copy.site.signInPrompt.close); all widths.
  - heart, signed-in → toggles: [same button; `aria-pressed` true when saved] → `POST|DELETE /api/v1/me/favorites/:id` (204) and a toast «أُضيفت إلى المفضّلة» / «Added to favourites» or «أُزيلت من المفضّلة» / «Removed from favourites» with «تراجع» / «Undo»; failure toast «تعذّر حفظ [[name]] في المفضّلة» / «We couldn’t save [[name]] to your favourites». Mock the write.
  - near me, granted: grant geolocation, set it inside the Strip (e.g. 31.515, 34.45, accuracy 50) [click role=button «الأقرب إليّ» / «Nearest to me» (copy.directory.near.button)] → heading «المساحات الأقرب إليك» / «Spaces nearest you», button pressed, line «مرتبة حسب المسافة من موقعك.» / «Sorted by distance from your location.» + «المسافات تقريبية بخط مستقيم.» + privacy line, link-buttons «إيقاف الترتيب حسب المسافة» / «Stop sorting by distance» and «مسح موقعي» / «Clear my location»; cards add «على بعد ⟦km⟧ كم» / «⟦km⟧ km away». Request `GET /api/v1/spaces?limit=6&sort=distance` with header `Masaha-Near: 31.515,34.45`.
  - near me, locating: [same click with the geolocation answer pending] → line «جارٍ تحديد موقعك…» / «Finding your location…» + «يُرسَل موقعك مقرَّبًا لترتيب المساحات حسب المسافة فقط، ولا يُحفظ.» / «Your location is sent rounded, only to sort spaces by distance, and is never stored.».
  - near me, denied: [deny geolocation, click «الأقرب إليّ»] → warning «تعذّر تحديد موقعك» / «We couldn’t find your location» + buttons «اختر منطقتك» / «Choose your area» (scrolls/focuses «تصفّح حسب المنطقة») and «حدّد موقعي على الخريطة» / «Set my location on the map» (→ `/spaces?view=map` in pick mode).
  - near me, imprecise: [geolocation outside 31.18–31.64 N × 34.17–34.62 E, or accuracy > 2000 m] → warning «تعذّر تحديد موقعك بدقة» / «We couldn’t find your location precisely» + the same two buttons.
  - hero search: [type in role=searchbox «ابحث عن مساحة» / «Search for a space» (placeholder «اسم المساحة أو المنطقة» / «Space name or area»), click role=button «بحث» / «Search» (copy.site.home.search)] → `/spaces?q=…`.
- requests on load: `GET /api/v1/spaces?limit=6&openNow=true`; `GET /api/v1/map/spaces` (no query: area counts); `GET /api/v1/lookups`. Signed-in also `POST /api/v1/auth/refresh`, `GET /api/v1/me/favorites`.
- empty/other notes: «عرض الكل» / «View all» → `/spaces?open=1` (→ `/spaces` while near me sorts). Area card = one link, h3 area name + line «[[governorate]] · {count}» (e.g. «الرمال», «[[غزة]] · 6 مساحات» / «Al-Rimal», «[[Gaza City]] · 6 spaces»); «كل المناطق» → `/spaces`. Owners' card link «تواصل معنا» / «Contact us» → `/about#owners`. Signed-in: hearts pressed on its 5 saved spaces (noor-hub, pal-hub, branch-hub, focus-hub, masahat) when shown.

## Directory, list view — `/spaces`   (role: both)
- example URLs: `/spaces`, `/spaces?page=2`, `/spaces?verified=1`, `/spaces?q=zzzz`.
- params (`features/directory/services/filtersOf.ts`; invalid values fall back to the default and are dropped):
  - `q=<text>` search on both names and the area; the field writes it 400 ms after typing stops. `q=هاب` / `q=hub` (several), `q=zzzz` (none).
  - `area=<id>[,<id>…]` (≤ 50): `2` الرمال/Al-Rimal (6 spaces), `14` النصيرات/Nuseirat (4), `9` الدرج/Al-Daraj (3), `6` الشيخ عجلين/Sheikh Ijlin (0 → no match). Area trigger shows the one name, else a count: 2 → «منطقتان محددتان» / «2 areas chosen», 3 → «3 مناطق محددة» / «3 areas chosen».
  - `period=HOUR|DAY|WEEK|MONTH` (the subscription; cards add «{price} / شهر» / «{price} / month»); `min`, `max` whole shekels, only with `period` (max < min drops max). Sent as `priceMin`/`priceMax` in agorot.
  - flags `=1`: `open` «مفتوحة الآن», `evening` «مفتوحة مساءً», `friday` «مفتوحة يوم الجمعة», `verified` «المساحات الموثّقة فقط», `students` «أسعار للطلاب». (`available` is ignored.)
  - `sort=updated` (default without q) | `name` (adds `lang`) | `relevance` (default with q; only with q) | `priceAsc` | `priceDesc` (only with a period).
  - `page=N` (18 a page; 37 spaces → 3 pages, page 3 has 1 card; a page past the last shows the last).
  - `view=map` → the map view (next section).
  - `filters=open` → on arrival opens the filters bottom sheet (< 1024) or focuses the sidebar's area filter (≥ 1024); then removed from the URL.
- states by URL:
  - all: `/spaces` → h1 «مساحات العمل» / «Workspaces», count «37 مساحة في قطاع غزة» / «37 spaces in the Gaza Strip».
  - filter on: `/spaces?verified=1` (count «N مساحة مطابقة» / «N matching spaces»), `/spaces?area=2`, `/spaces?period=MONTH&min=100&max=300&sort=priceAsc` (prices on cards; sort «الترتيب: الأرخص شهريًا» / «Sort: Monthly price: low to high»), `/spaces?students=1&friday=1`, `/spaces?open=1` (time-dependent).
  - search: `/spaces?q=هاب`, `/spaces?q=hub&sort=name`.
  - no results: `/spaces?q=zzzz` → empty state «لا توجد مساحات تطابق ما اخترت» / «No spaces match your choice» + «جرّب إزالة بعض الفلاتر أو البحث باسم آخر.» + button «مسح الفلاتر» / «Clear filters» (clears the search here); `/spaces?area=6` → same, the button clears the filters.
  - page 2: `/spaces?page=2`; last page: `/spaces?page=3`; past last: `/spaces?page=9` (shows page 3).
  - filters sheet open on arrival: `/spaces?filters=open` at < 1024.
  - loading: hold `GET /api/v1/spaces?limit=18…` → 6 card skeletons.
  - failed: 500/429 on that GET → alert «تعذّر تحميل المساحات» / «We couldn’t load the spaces» + «إعادة المحاولة».
  - empty directory: answer `GET /api/v1/spaces?limit=18` (no filter) with `data:[]`, `totalRecords:0`, `totalPages:0` → «لا توجد مساحات في الدليل بعد» / «No spaces in the directory yet» (copy.directory.empty).
  - refresh failed (cards kept): after a good load, make a same-key refetch fail (window refocus) → alert «تعذّر تحديث القائمة» / «We couldn’t refresh the list» above the cards.
- states by click:
  - filters sheet (< 1024 only in the list view): [click role=button whose name starts «الفلاتر» / «Filters» (copy.directory.filters.title; with filters on the name adds e.g. «فلتر واحد مطبّق» / «1 filter applied» and a visible count badge)] → bottom Sheet, dialog «الفلاتر» / «Filters», description «تُطبَّق فورًا على النتائج» / «Applied to the results right away»; body: area, price, «الدوام» / «Hours», «أخرى» / «Other»; footer primary «عرض {N} نتيجة» … (copy.directory.filters.show; «لا توجد نتائج» / «No results» at 0; «عرض النتائج» / «Show results» while unknown) which closes it, ghost «مسح الفلاتر» / «Clear filters» (disabled with none), X «إغلاق» / «Close».
  - filters sidebar (≥ 1024, always open): `aside#directory-filters` (role=complementary «الفلاتر» / «Filters»), button «مسح» / «Clear» (copy.directory.filters.clear).
  - area filter: [≥ 1024 in the sidebar; < 1024 open the sheet first; click role=button «المنطقة» / «Area» (copy.lookups.areaFilter.label; its text «كل المناطق» / «All areas»)] → popover `[data-slot=combobox-content]`: search «ابحث عن منطقة» / «Search for an area» (placeholder «اسم المنطقة» / «Area name»), list «المناطق» / «Areas» grouped by governorate; items e.g. «الرمال» / «Al-Rimal». Typing a non-matching name → «لا توجد منطقة بهذا الاسم» / «No area by that name».
  - price: [click role=radio «شهر» / «Month» in radiogroup «نوع الاشتراك» / «Subscription»; options «الكل»,«ساعة», «يوم»,«أسبوع»,«شهر» / «All»,«Hour»,«Day»,«Week»,«Month»] → fields «من» / «From» and «إلى» / «To» appear. Errors by typing: `0` → «اكتب مبلغًا بالشيكل أكبر من صفر» / «Enter an amount in shekels, above zero»; `200000` → «اكتب مبلغًا حتى 100,000 ₪» / «Enter an amount up to ₪100,000»; To < From → `«إلى» أقل من «من».` / «“To” is below “From”.».
  - checkboxes: role=checkbox «مفتوحة الآن», «مفتوحة مساءً», «مفتوحة يوم الجمعة», «المساحات الموثّقة فقط», «أسعار للطلاب» / «Open now», «Open in the evening», «Open on Friday», «Verified spaces only», «Student prices».
  - sort menu (all widths): [click role=combobox «الترتيب» / «Sort» (text «الترتيب: الأحدث تحديثًا» / «Sort: Latest updates»)] → `[data-slot=select-content]` options «الأحدث تحديثًا», «حسب الاسم» / «Latest updates», «By name»; + «الأفضل تطابقًا» / «Best match» with q; + «الأرخص شهريًا», «الأغلى شهريًا» / «Monthly price: low to high», «Monthly price: high to low» with period=MONTH; + «حسب المسافة» / «By distance» while near me sorts.
  - view switch: [click role=radio «خريطة» / «Map» (copy.directory.view.map); «قائمة» / «List»] → `?view=map`.
  - search refused: [type only tatweel or diacritics, e.g. `ـــ`, in searchbox «ابحث عن مساحة» / «Search for a space»] → field error «اكتب حرفًا من اسم المساحة أو منطقتها» / «Type a letter of the space’s or its area’s name».
  - near me: [button «الأقرب إليّ» / «Nearest to me» beside the count] → as Home (granted/locating/denied/imprecise); granted sorts the list (`sort=distance` + `Masaha-Near`) and the sort shows «الترتيب: حسب المسافة» / «Sort: By distance»; denied «اختر منطقتك» opens the filters sheet (< 1024) or focuses the area filter (≥ 1024); «حدّد موقعي على الخريطة» → map pick mode.
  - heart, guest → sign-in prompt (as Home); signed-in toggles (as Home).
  - pagination: nav «صفحات المساحات» / «Pages of the spaces»: links «الصفحة 2» / «Page 2» (aria-label), «التالي» / «Next», «السابق» / «Previous» (disabled on the first page).
- requests on load: `GET /api/v1/spaces?limit=18[&q=…][&area=2,3][&period=MONTH&priceMin=10000&priceMax=30000] [&openNow=true][&evening=true][&openFriday=true][&verified=true][&studentPrices=true][&sort=…][&lang=ar|en] [&page=N]`; `GET /api/v1/price-ranges`; `GET /api/v1/lookups`. Signed-in: `GET /api/v1/me/favorites`.
- empty/other notes: a card is one link named by the space (`h3`); the heart is outside the link in `[data-card-action]`. Card status: verified → «متاح» / «Available», «ممتلئ» / «Full», «مغلق الآن» / «Closed now»; unverified → «مفتوحة الآن» / «Open now» or «مغلقة الآن» / «Closed now»; none → «لا تتوفر حالة مباشرة» / «No live status». Today line: «اليوم ⟦08:00–22:00⟧», «مغلقة اليوم», «مفتوحة اليوم على مدار الساعة», «ساعات العمل غير متوفرة».

## Directory, map view — `/spaces?view=map`   (role: both)
- example URLs: `/spaces?view=map`, `/spaces?view=map&verified=1`, `/spaces?view=map&q=zzzz`.
- params: the list's, except `sort`, `page`, `filters` (ignored here).
- states by URL:
  - all pins: `/spaces?view=map` → count line, «الأقرب إليّ», the map (role=application «خريطة المساحات» / «Map of spaces», in a section «الخريطة» / «Map»), legend list «دليل الخريطة» / «Map legend»: «متاح», «ممتلئ», «مغلق الآن», «لا تتوفر حالة مباشرة».
  - filtered: `/spaces?view=map&verified=1`, `/spaces?view=map&area=14`.
  - no match: `/spaces?view=map&q=zzzz` → card over the map «لا توجد مساحات تطابق ما اخترت» + «مسح الفلاتر».
  - loading: hold `GET /api/v1/map/spaces…` → notice «جارٍ تحميل المساحات…» / «Loading spaces…» over the map (map chunk skeleton first).
  - failed: 500/429 on it → alert «تعذّر تحميل المساحات» above the map + «إعادة المحاولة».
  - empty: answer it with `{"pins":[],"truncated":false}` and no filter → card «لا توجد مساحات في الدليل بعد».
  - truncated: answer with `"truncated":true` → «تظهر أول ⟦1,000⟧ مساحة؛ قرّب الخريطة لترى ما بقي.» / «Showing the first ⟦1,000⟧ spaces; zoom in to see the rest.» (count line hidden).
  - tiles failed: block `tile.openstreetmap.org` → «لم تُحمَّل الخريطة. تصفّح المساحات في القائمة.» / «The map didn’t load. Browse the spaces in the list.».
- states by click:
  - filters sheet at every width: [click role=button starting «الفلاتر» / «Filters»] → the same bottom sheet as the list.
  - chosen space, ≥ 768: [click `.map-mark[role=button]` with aria-label «{name} — {status}», e.g. «بال هاب — متاح» / «Pal Hub — Available» (copy.directory.map.pin)] → card region named by the space at the map's foot: area, status, today, link «عرض التفاصيل» / «View details», X button aria-label «إغلاق» / «Close». Escape closes.
  - chosen space, < 768: [same click] → non-modal bottom Sheet (title = name, `[data-slot=sheet-content]`), link «عرض التفاصيل», X «إغلاق»; sr-only status «{name}: التفاصيل في أسفل الصفحة» / «{name}: details at the bottom of the page».
  - pick a point: [near me denied → button «حدّد موقعي على الخريطة» / «Set my location on the map» (also reachable from Home, the list, favourites)] → region «حدّد موقعك على الخريطة» / «Set your location on the map» with buttons «ثبّت الموقع هنا» / «Set location here» and «رجوع» / «Back» (over the map ≥ 1024, under it < 1024; crosshair).
  - point placed: [click «ثبّت الموقع هنا»] → user mark (role=img «موقعي (يدوي)» / «My location (manual)»), button «مركّز على موقعي» / «Centre on my location», line «موقعك ظاهر على الخريطة. تُرتَّب القائمة حسب المسافة منه.» / «Your location is shown on the map. The list is sorted by distance from it.» + «تغيير الموقع» / «Change location», «مسح موقعي» / «Clear my location».
  - near me granted on the map: [«الأقرب إليّ» with geolocation in the Strip] → user mark «موقعك» / «Your location» + «مركّز على موقعي»; the chosen card adds «على بعد ⟦km⟧ كم».
- requests on load: `GET /api/v1/map/spaces[?q=…&area=…&period=…&priceMin=…&priceMax=…&openNow=true…]` (no limit/sort/page; `bounds=` only after zooming when truncated); `GET /api/v1/price-ranges`; `GET /api/v1/lookups`; OSM tiles. Pins body: `{pins:[{id,slug,nameEn,nameAr,areaId,location:{lat,lng},isVerified,days,cover,liveStatus, hoursStatus}],truncated}`.
- empty/other notes: FULL pin = mock a pin's `liveStatus:"FULL"`.

## A space's page — `/spaces/:slug`   (role: both)
- example URLs:
  - verified, 4 photos, running announcement: `/spaces/pal-hub` — «بال هاب» / «Pal Hub»; OFFER running (section «الإعلانات» / «Announcements»); prices by shift («الأسعار حسب الوردية») + student prices; hours Sat–Thu 08–22, Fri 12–20; live status (open → «متاح»); WhatsApp + phone (contact bar < 768); saved by demo-user.
  - running closure: `/spaces/shati-sea-view` — closure notice at the top, status closed, today «مغلقة مؤقتًا اليوم» / «Temporarily closed today»; 24 h hours.
  - unverified: `/spaces/freelancers-house` (notice + owners' dialog, prices hidden as stale, description, Facebook + WhatsApp); `/spaces/masahat` (unverified with fresh prices until 2026-11-26, 24 h, email/Instagram/WhatsApp).
  - Arabic name missing (name_ar NULL): `/spaces/hawa-tech-space` (unverified), `/spaces/zeitoun-works` (verified, no capacity → «لم تكتمل معلومات الحالة المباشرة لهذه المساحة بعد.» / «This space’s live status isn’t set up yet.»), `/spaces/mawasi-field-office` (unverified). The English name shows (lang=en) in the Arabic UI.
  - longest Arabic name (20 chars): `/spaces/radwan-study-hall` «قاعة الرضوان للدراسة» (verified; hours in 3 groups → «عرض كل الأيام» toggle; phone only → bar shows only «اتصال»); `/spaces/nuseirat-study-house` «دار النصيرات للدراسة» (unverified).
  - stale: `/spaces/sabra-lab` (verified; hours 2026-08-04 and prices 2026-09-03 → «قد يكون تغيّر» / «May have changed» badges); `/spaces/tuffah-place` (unverified, prices hidden «لا نعرض الأسعار لأنها لم تُحدَّث منذ مدة. اسأل المساحة عن السعر الحالي.» / «We don’t show the prices because they haven’t been updated in a while. Ask the space for the current price.»). All of noor-hub … khan-younis-library (ids 2–25) have stale prices.
  - no hours: `/spaces/daraj-corner` (verified) → «ساعات العمل غير متوفرة» / «Hours not available».
  - no prices: `/spaces/jreas-hub` (unverified) → «لم تُضف أسعار بعد» / «No prices added yet».
  - not found: `/spaces/masaha-demo` (deleted) or `/spaces/no-such-space` → h1 «لم نجد هذه المساحة» / «We couldn’t find this space» + «ربما أُزيلت من الدليل، أو أن الرابط غير صحيح.» + link «تصفّح المساحات» / «Browse spaces».
- params: none (slug only).
- states by URL:
  - loading: hold `GET /api/v1/spaces/pal-hub` → page skeleton (sr-only h1 «صفحة المساحة» / «Space»).
  - failed: 500/429 on it → alert «تعذّر تحميل صفحة المساحة» / «We couldn’t load this space’s page» + reference + «إعادة المحاولة».
  - FULL: answer `GET /api/v1/spaces/pal-hub/occupancy` with `{"success":true,"data":{"status":"FULL","hoursStatus": "OPEN"}}`; CLOSED: `"status":"CLOSED","hoursStatus":"CLOSED"`.
  - status read failed: 500 on the occupancy GET → «تعذّر قراءة الحالة الآن» / «We couldn’t read the status just now».
  - layout by width: ≥ 1024 status + contacts in an aside «الحالة والتواصل» / «Status & contact»; 768–1023 breadcrumb nav «مسار التنقّل» / «Breadcrumb» («الرئيسية» › «المساحات» › name); < 768 link «العودة إلى المساحات» / «Back to spaces» and the fixed region «التواصل السريع» / «Quick contact» with links «واتساب» / «WhatsApp», «اتصال» / «Call».
- states by click:
  - photo viewer: [click role=button «عرض الصورة 1» / «View photo 1» (copy.directory.page.gallery.view); tiles 2–5 exist only ≥ 768; on a phone the first tile carries the pill «عرض كل الصور (4)» / «View all photos (4)»] → Dialog «صور بال هاب» / «Photos of Pal Hub», counter «1 / 4», buttons «التالية» / «Next», «السابقة» / «Previous» (only with > 1 photo), «إغلاق» / «Close». Photos `GET /api/v1/files/…`.
  - photo viewer, next photo: [open viewer, click «التالية» / «Next»] → «2 / 4».
  - all days: [click role=button «عرض كل الأيام» / «Show all days»; only when the week groups into > 2 rows, e.g. radwan-study-hall] → one row per day, button «عرض مختصر» / «Show less» (aria-expanded=true).
  - unverified owners' dialog: [click role=button «هل تدير هذه المساحة؟ تواصل معنا» / «Do you run this space? Contact us» (copy.directory.page.unverified.contact); unverified spaces only] → Dialog «تواصل مع فريقنا» / «Contact the Masaha team», the platform's WhatsApp/email buttons («واتساب …» / «WhatsApp …», «بريد …» / «Email …»), «إغلاق» / «Close»; loads `GET /api/v1/settings/public` (failure or none → «لا توجد وسيلة تواصل متاحة الآن.» / «There’s no way to reach us set up yet.»).
  - heart beside the name, guest → sign-in prompt (favourite reason, as Home) [role=button «حفظ [[name]] في المفضّلة» / «Save [[name]] to favourites»; not in `[data-card-action]`]; signed-in → toggles + toast.
  - report, guest: [click role=button «الإبلاغ عن معلومة غير صحيحة» / «Report wrong information» (copy.dataReports.report.trigger)] → Dialog «سجّل الدخول للإبلاغ عن معلومة» / «Sign in to report information» (copy.site.signInPrompt.report.title) + «إنشاء حساب», «تسجيل الدخول», X «إغلاق».
  - report, signed-in: [same click] → Dialog «الإبلاغ عن معلومة غير صحيحة» / «Report wrong information», description «بلاغك عن [[name]] يصل إلى إدارة المساحة، وتجد ردّها في …» (verified, copy.dataReports.report.toSpace) or «… يراجعه فريقنا …» (unverified, …toTeam); combobox «ما المعلومة غير الصحيحة؟» / «What’s wrong?» (placeholder «اختر» / «Choose»), textarea «التفاصيل» / «Details» (helper «اختياري» / «Optional»), buttons «رجوع» / «Back», «إرسال» / «Send». Focus starts on the combobox.
  - report field list: [open report dialog, click the combobox] → options «الأسعار», «ساعات العمل», «التواصل», «الموقع», «المرافق», «أخرى» / «Prices», «Opening hours», «Contact», «Location», «Amenities», «Other».
  - report validation: [open report dialog, click «إرسال» empty] → «اختر نوع المعلومة» / «Choose what’s wrong»; [choose «أخرى» / «Other», click «إرسال» with empty details] → `اكتب ما الخطأ في «أخرى».` / «Write what is wrong under “Other”.».
  - report sent: [choose «الأسعار», «إرسال»] → `POST /api/v1/spaces/:slug/reports` `{field,message}`; 201 → dialog closes, toast copy.dataReports.report.sentSpace / sentTeam with action «عرض بلاغاتي» / «View my reports»; 200 → toast «أرسلت بلاغًا عن هذا من قبل، وما زال قيد المراجعة.» / «You already reported this, and it is still in review.»; 500 → in-dialog alert «تعذّر إرسال البلاغ» / «We couldn’t send the report»; 429 → warning «محاولات كثيرة، حاول بعد ⟦0:30⟧». Mock it.
- requests on load: `GET /api/v1/spaces/:slug`; `GET /api/v1/spaces/:slug/occupancy` (again every 60 s and on focus); `GET /api/v1/lookups`; photos `GET /api/v1/files/…`; OSM tiles (location map, link «الاتجاهات» / «Directions»). Signed-in: `GET /api/v1/me/favorites`.
- empty/other notes: document title = the space's name. The other-language name shows under the h1.

## About — `/about`   (role: both)
- example URLs: `/about`, `/about#contact`, `/about#owners`.
- params: none; hash `#contact` / `#owners` scrolls to and focuses that h2.
- states by URL: default (h1 «عن مساحة» / «About Masaha», button-link «تصفّح المساحات» / «Browse spaces», sections «من أين تأتي المعلومات؟», «ماذا تعني الحالة؟», «تواصل معنا», «لأصحاب المساحات»); contact buttons absent when `GET /api/v1/settings/public` fails or is held.
- states by click: none (the note's link «تواصل معنا» / «contact us» → `#contact`).
- requests on load: `GET /api/v1/settings/public`.
- empty/other notes: sections are regions named by their h2 (e.g. region «تواصل معنا» / «Contact us», «لأصحاب المساحات» / «For space owners»).

## Privacy — `/privacy`   (role: both)
- example URLs: `/privacy`.
- params: none.
- states by URL: default (h1 «سياسة الخصوصية» / «Privacy Policy», «آخر تحديث: 2026-11-05», contact email button at the end from settings).
- states by click: none.
- requests on load: `GET /api/v1/settings/public`.

## Not found (404) — any unknown path, e.g. `/no-such-page`   (role: both)
- example URLs: `/no-such-page`, `/spaces/a/b`, `/me/unknown`.
- states by URL: «الصفحة غير موجودة» / «Page not found» + «ربما تغيّر الرابط أو حُذفت الصفحة.» / «The link may have changed or the page was removed.», links «الرئيسية» / «Home», «تصفّح المساحات» / «Browse spaces». Inside the site shell.
- states by click: none.
- requests on load: none (signed-in: refresh only).

## Account layout (wraps the three account pages)   (role: user)
- nav labelled «حسابي» / «My account» (label shown ≥ 1024, a row of links over the page < 1024, a column ≥ 1024): links «المفضّلة» / «Favourites», «بلاغاتي» / «My reports», «إعدادات حسابي» / «Account settings» (copy.site.account), current one `aria-current=page`.
- guest: each page redirects to `/login?next=<path>` (e.g. `/login?next=%2Fme%2Ffavorites`).

## Favourites — `/me/favorites`   (role: user)
- example URLs: `/me/favorites`.
- params: none.
- states by URL:
  - default (demo-user): h1 «المفضّلة» / «Favourites», «المساحات التي حفظتها، بحالتها الآن.»; count «5 مساحات محفوظة» / «5 saved spaces»; 5 cards, hearts pressed.
  - loading: hold `GET /api/v1/me/favorites` → 3 card skeletons.
  - failed: 500/429 → alert «تعذّر تحميل المفضّلة» / «We couldn’t load your favourites» + «إعادة المحاولة».
  - empty: answer it with `data:[]` → card «لم تحفظ أي مساحة بعد» / «You haven’t saved any spaces yet» + «اضغط على القلب في صفحة أي مساحة لتجدها هنا.» + link «تصفّح المساحات» / «Browse spaces».
  - a space that left: append `{"listed":false,"savedAt":"2026-11-01T00:00:00.000Z","space":{"id":1,"nameEn":"Demo Space","nameAr":"مساحة تجريبية"}}` to the answer → muted card «لم تعد هذه المساحة معروضة في الدليل» / «This space is no longer listed in the directory» + button «إزالة» / «Remove» (aria-label «إزالة [[name]] من المفضّلة» / «Remove [[name]] from favourites»).
- states by click:
  - remove by heart: [click a card's heart, `aria-pressed=true`] → `DELETE /api/v1/me/favorites/:id`, toast «أُزيلت من المفضّلة» / «Removed from favourites» + «تراجع» / «Undo». Mock it.
  - remove a space that left: [click «إزالة» on the mocked row] → toast «أُزيلت [[name]] من المفضّلة. لا يمكن حفظها من جديد ما دامت خارج الدليل.».
  - near me: [«الأقرب إليّ» / «Nearest to me»] → granted: `GET /api/v1/me/favorites?sort=distance` + `Masaha-Near`, distances on cards; denied: «اختر منطقتك» → `/spaces?filters=open`, «حدّد موقعي على الخريطة» → `/spaces?view=map`.
- requests on load: `POST /api/v1/auth/refresh`, `GET /api/v1/me/favorites`, `GET /api/v1/lookups`.

## My reports — `/me/reports`   (role: user)
- example URLs: `/me/reports`, `/me/reports?status=open`, `/me/reports?status=decided`.
- params: `status=open|decided` (anything else = all), `page=N` (20 a page).
- states by URL:
  - all (demo-user, 3): al-salam-hub «ساعات العمل» «قيد المراجعة» / «In review»; palm-space «الأسعار» «تم التصحيح» / «Corrected» with a reply; beit-lahia-desk «ساعات العمل» «لم يُعتمد» / «Not accepted» with a reply, no message.
  - `?status=open` (1 card), `?status=decided` (2 cards).
  - loading: hold `GET /api/v1/me/reports…` → 3 skeletons.
  - failed: 500/429 → alert «تعذّر تحميل بلاغاتك» / «We couldn’t load your reports» + «إعادة المحاولة».
  - empty: answer with `data:[]`, no status → «لم ترسل أي بلاغ بعد» / «You haven’t sent any reports yet» + «تصفّح المساحات»; with `?status=open` → «لا توجد بلاغات هنا» / «No reports here».
  - a space that left: mock a report whose space is unlisted → name as muted text + «لم تعد هذه المساحة معروضة في الدليل».
- states by click:
  - chips: [click role=radio «قيد المراجعة» / «In review» or «تمت المراجعة» / «Reviewed» or «الكل» / «All» in group «تصفية البلاغات» / «Filter reports»] → `?status=open|decided`.
  - long message: [mock a message > 160 chars; click role=button «عرض المزيد» / «Show more»] → unfolded, «عرض أقل» / «Show less». No real report is long enough.
- requests on load: `POST /api/v1/auth/refresh`, `GET /api/v1/me/reports?page=1&limit=20[&status=OPEN|DECIDED]`.

## Account settings — `/me`   (role: user)
- example URLs: `/me` (not `/me/settings`).
- params: none.
- states by URL:
  - default: h1 «إعدادات حسابي» / «Account settings»; cards «الملف الشخصي» / «Profile» (field «الاسم» / «Name», email as text, «حفظ» / «Save»), «التفضيلات» / «Preferences» (radios «العربية» / «English»; «فاتح», «داكن», «حسب الجهاز» / «Light», «Dark», «Device setting»), «تسجيل الدخول» / «Signing in» (row «كلمة المرور» / «Password» + button «تغيير» / «Change»).
  - loading: hold `GET /api/v1/me` → 3 skeleton cards (role=status «جارٍ التحميل» / «Loading»).
  - failed: 500/429 → alert «تعذّر تحميل حسابك» / «Couldn’t load your account» + «إعادة المحاولة».
  - Google-only: answer `GET /api/v1/me` with `hasPassword:false, hasGoogle:true` → Google row with badge «مربوط» / «Linked», password «لم تُعيَّن بعد» / «Not set yet», button «أرسل رابط تعيين كلمة المرور» / «Send a link to set a password».
- states by click:
  - password form: [click role=button «تغيير» / «Change»] → form: «كلمة المرور الحالية» / «Current password», «كلمة المرور الجديدة» / «New password», rules list «شروط كلمة المرور» / «Password rules» («8 أحرف على الأقل», «حرف واحد على الأقل», «رقم واحد على الأقل» / «At least 8 characters», «At least one letter», «At least one number»), line «تغيير كلمة المرور يسجّل خروجك من كل الأجهزة الأخرى», buttons «حفظ كلمة المرور» / «Save password», «رجوع» / «Back».
  - password form errors: [open it, click «حفظ كلمة المرور» empty] → «أدخل كلمة المرور» / «Enter your password» and «كلمة المرور لا تستوفي الشروط أدناه» / «The password doesn’t meet the rules below», rules in red.
  - password rules ticking: [type `abc` in «كلمة المرور الجديدة»] → letter met, others not.
  - show password: [click role=button «إظهار كلمة المرور» / «Show password»] → «إخفاء كلمة المرور» / «Hide password».
  - profile error: [clear «الاسم», click «حفظ»] → «أدخل اسمك» / «Enter your name».
  - profile saved: [edit the name, «حفظ»] → `PATCH /api/v1/me` `{name}`; toast «حُفظت التغييرات» / «Changes saved»; 500 → «تعذّر حفظ التغييرات». Mock it.
  - language: [click role=radio «English» / «العربية»] → `PATCH /api/v1/me` `{language}` and the UI switches; failure → «تعذّر حفظ اللغة» / «Couldn’t save the language».
  - theme: [click role=radio «داكن» / «Dark»] → dark theme (no request).
  - password saved: submit → `POST /api/v1/me/password` `{currentPassword,password}`; toast «تم تغيير كلمة المرور، وسُجّل خروجك من الأجهزة الأخرى»; refusal → «تعذّر حفظ كلمة المرور» / «Couldn’t save the password». Mock it.
- requests on load: `POST /api/v1/auth/refresh`, `GET /api/v1/me`.

## Sign in — `/login`   (role: visitor; a signed-in user is redirected on)
- example URLs: `/login`, `/login?next=%2Fspaces%2Fpal-hub`, `/login?next=%2Fme%2Ffavorites`.
- params: `next=<site path>` — where to land after signing in; also changes the way back: «العودة إلى الصفحة السابقة» / «Back to the previous page», or «العودة إلى [[name]]» / «Back to [[name]]» when this tab has already read that space's page; without `next` «العودة إلى الرئيسية» / «Back to home». Carried to «نسيت كلمة المرور؟» and «إنشاء حساب».
- states by URL: default: card h1 «تسجيل الدخول» / «Sign in», description, Google button (iframe) + «أو» / «or», fields «البريد الإلكتروني» / «Email» (placeholder `name@example.com`), «كلمة المرور» / «Password», link «نسيت كلمة المرور؟» / «Forgot password?», submit, «ليس لديك حساب؟» / «No account?» + «إنشاء حساب» / «Create account».
- states by click:
  - empty submit: [click the form's role=button «تسجيل الدخول» / «Sign in» (type=submit; the h1 has the same text)] → «تحقّق من كتابة البريد الإلكتروني، مثل ⟦name@example.com⟧» / «Check the email address, for example ⟦name@example.com⟧» and «أدخل كلمة المرور» / «Enter your password».
  - wrong credentials: [fill demo-user@example.com + a wrong password, submit] → `POST /api/v1/auth/login` 401 `{type:"unauthorized",code:"INVALID_CREDENTIALS"}` → alert «تعذّر تسجيل الدخول» / «Couldn’t sign in» + «البريد الإلكتروني أو كلمة المرور غير صحيحة.» / «The email or password is incorrect.».
  - too many attempts: [submit with the POST answered 429 + `Retry-After: 30`] → warning «محاولات كثيرة، حاول بعد ⟦0:30⟧» / «Too many attempts. Try again in ⟦0:30⟧.», submit disabled.
  - server error: [POST answered 500] → alert «تعذّر تسجيل الدخول» + «حدث خطأ من جهتنا. حاول مرة أخرى.» / «Something went wrong on our side. Please try again.» + «رقم المرجع: …».
  - offline: [abort the POST] → alert «تعذّر الاتصال» / «Couldn’t connect» + «تحقّق من اتصالك بالإنترنت ثم حاول مرة أخرى.» + «إعادة المحاولة».
  - submitting: [hold the POST] → submit shows a spinner (busy).
  - show password: [click «إظهار كلمة المرور» / «Show password» inside the password field].
  - Google failed to load: [block `accounts.google.com/gsi/client`] → alert «تعذّرت المتابعة باستخدام Google» / «Couldn’t continue with Google» + «تعذّر تحميل الدخول باستخدام Google. تحقّق من اتصالك ثم أعد تحميل الصفحة.».
  - signed in: [real submit] → lands on `next` (or home for a USER), toast «أهلًا بعودتك» / «Welcome back».
- requests on load: none of the app's (GSI script from Google). On submit: `POST /api/v1/auth/login`; Google: `POST /api/v1/auth/google`.

## Register — `/register`   (role: visitor)
- example URLs: `/register`, `/register?next=%2Fspaces%2Fpal-hub`.
- params: `next` (as sign-in).
- states by URL: default: h1 «إنشاء حساب» / «Create account», Google + «أو», fields «الاسم» / «Name», «البريد الإلكتروني» / «Email», «كلمة المرور» / «Password» with the rules list, submit «إنشاء الحساب» / «Create account», «لديك حساب؟» / «Have an account?» + «تسجيل الدخول» / «Sign in», «اقرأ» + «سياسة الخصوصية» / «Read the» + «privacy policy», owners' note + «تواصل معنا», way back.
- states by click:
  - empty submit: [click role=button «إنشاء الحساب» / «Create account» (type=submit; EN equals the h1)] → «أدخل اسمك» / «Enter your name», the email error, «كلمة المرور لا تستوفي الشروط أدناه» / «The password doesn’t meet the rules below», rules in red.
  - rules ticking: [type `abc1` in «كلمة المرور»] → letter + number met, length not.
  - email taken (real, no write): [name `Test`, email `demo-user@example.com`, password `abc12345`, submit] → `POST /api/v1/auth/register` 409 `EMAIL_TAKEN` → field error «يوجد حساب بهذا البريد الإلكتروني.» / «An account with this email already exists.» + link «سجّل الدخول بهذا البريد» / «Sign in with this email».
  - 429 / 500 / offline: as sign-in, title «تعذّر إنشاء الحساب» / «Couldn’t create the account».
- requests on load: none of the app's. On submit: `POST /api/v1/auth/register` `{name,email,password,language}`.

## Forgot password — `/forgot-password`   (role: visitor)
- example URLs: `/forgot-password`, `/forgot-password?next=%2Fme`.
- params: `next` (carried to sign-in and to the reset page).
- states by URL (the step comes from `GET /api/v1/auth/password/recovery`; mock its `data`):
  - request (fresh browser, `{"step":"request"}`): h1 «نسيت كلمة المرور» / «Forgot password», field «البريد الإلكتروني», submit «أرسل رابط الاستعادة» / «Send reset link».
  - sent: `{"step":"sent","email":"d***@example.com","resendInSeconds":60,"canResend":true}` → «تفقّد بريدك الإلكتروني» / «Check your email», sentMessage, «أُرسلت إلى ⟦d***@example.com⟧» / «Sent to ⟦…⟧», disabled «أعد الإرسال بعد ⟦1:00⟧» / «Resend in ⟦1:00⟧» (then «أعد الإرسال» / «Resend»), «استخدم بريدًا آخر» / «Use another email».
  - sent, resend limit: same with `"canResend":false` → «طلبت الرابط مرات كثيرة. أدخل بريدك الإلكتروني من جديد لطلب رابط آخر.».
  - link open: `{"step":"password","email":"d***@example.com"}` → «فتحت رابط الاستعادة» / «You’ve opened a reset link», «للحساب ⟦d***@example.com⟧. عيّن كلمة المرور الجديدة، أو اطلب رابطًا جديدًا.», link «تعيين كلمة مرور جديدة» / «Set a new password», button «أدخل بريدك الإلكتروني من جديد» / «Enter your email again».
  - loading: hold the recovery GET → spinner «جارٍ التحميل».
  - unreachable: 500 on it (all 3 attempts) → «حدث خطأ غير متوقع» / «Something went wrong» + «إعادة المحاولة»; aborted → «لا يوجد اتصال بالإنترنت» / «No internet connection».
- states by click:
  - empty submit: [click role=button «أرسل رابط الاستعادة» / «Send reset link»] → the email field error.
  - link sent: [type an email, submit] → `POST /api/v1/auth/password/forgot` `{email}` → answer a `sent` position (a real submit writes a recovery and binds this browser to it).
  - another email: [on «sent», click «استخدم بريدًا آخر»] → back to the request form, field focused.
  - resend: [on «sent» with the wait over, click «أعد الإرسال» / «Resend»] → `POST /api/v1/auth/password/resend`; failure → «تعذّرت إعادة إرسال الرابط».
  - 429 / 500 on the request: alert «تعذّر إرسال الرابط» / «Couldn’t send the link» (or the rate-limit warning).
- requests on load: `GET /api/v1/auth/password/recovery`, `GET /api/v1/settings/public` (footer «تواصل معنا» opens the platform WhatsApp when set, else `/about#contact`); footer «لا يمكنك الوصول إلى بريدك؟», «العودة إلى تسجيل الدخول» / «Back to sign in».

## Reset password — `/reset-password#token=<token>`   (role: both; no guard)
- example URLs: `/reset-password#token=abc123` (bogus token), `/reset-password` (no token).
- params: the token rides in the **fragment** `#token=…` (removed from the address at once); `next` in the query.
- states by URL:
  - no token: `/reset-password` → `GET /api/v1/auth/password/recovery`; any step but `password` → «انتهت صلاحية الرابط أو استُخدم من قبل» / «The link has expired or was already used» + «روابط الاستعادة صالحة لمدة ساعة ولمرة واحدة فقط.» + link «اطلب رابطًا جديدًا» / «Request a new link».
  - bogus token: `/reset-password#token=abc123` → `POST /api/v1/auth/password/reset/check` `{token}` refused → the same «expired» screen.
  - form: answer the check (or the recovery GET) with `{"step":"password","email":"d***@example.com"}` → h1 «تعيين كلمة مرور جديدة» / «Set a new password», «للحساب ⟦d***@example.com⟧» / «For ⟦…⟧», field «كلمة المرور الجديدة» / «New password» + rules, submit «حفظ كلمة المرور» / «Save password».
  - check failed: answer the check 429 (or 500) → «تعذّر التحقّق من الرابط» / «Couldn’t check the link» + the failure + «افتح الرابط من بريدك الإلكتروني مرة أخرى.» / «Open the link in your email again.».
  - unreachable: abort the check → «لا يوجد اتصال بالإنترنت» + «إعادة المحاولة».
  - loading: hold the check → spinner «جارٍ التحميل».
- states by click:
  - empty submit (form state): [click «حفظ كلمة المرور»] → «كلمة المرور لا تستوفي الشروط أدناه», rules red.
  - done: [valid password, submit; answer `POST /api/v1/auth/password/reset` 204] → «تم تغيير كلمة المرور، وسُجّل خروجك من كل الأجهزة» / «Your password was changed, and you were signed out on all devices» + link «تسجيل الدخول» / «Sign in».
  - save failed: [POST answered 500] → «تعذّر حفظ كلمة المرور» / «Couldn’t save the password».
- requests on load: `POST /api/v1/auth/password/reset/check` (with a token) or `GET /api/v1/auth/password/recovery` (without). On submit: `POST /api/v1/auth/password/reset`.

## Forced password change — `/change-password`   (role: user with a temporary password)
- example URLs: `/change-password?next=%2Fme`.
- reach it: no such user in the DB. Sign in as demo-user, then answer `POST /api/v1/auth/refresh` (or `/auth/login`) with the real body but `data.user.mustChangePassword = true` → any page redirects to `/change-password?next=<page>`. A guest → `/login`; a user without the flag → their landing.
- params: `next` (where to go once changed).
- states by URL: focus shell whose header holds only role=button «تسجيل الخروج» / «Sign out»; card «اختر كلمة مرور جديدة» / «Choose a new password», «هذه كلمة مرور مؤقتة. اختر كلمة مرورك لتتابع.», field «كلمة المرور الجديدة» + rules, submit «حفظ والمتابعة» / «Save and continue».
- states by click:
  - empty submit: [click «حفظ والمتابعة»] → «كلمة المرور لا تستوفي الشروط أدناه», rules red.
  - save failed: [`POST /api/v1/me/password` answered 500] → «تعذّر حفظ كلمة المرور».
  - sign out: [click «تسجيل الخروج»] → `POST /api/v1/auth/logout` → `/login`.
- requests on load: `POST /api/v1/auth/refresh`. On submit: `POST /api/v1/me/password` (toast «حُفظت كلمة المرور الجديدة» / «Your new password is saved»).

---

## Shell parts

## Skip link — every shell   (role: both)
- states by click: [press Tab once after load] → `a[href="#main"]` «تخطَّ إلى المحتوى» / «Skip to content» (copy.site.skipToContent) becomes visible at the top start; Enter focuses `main#main`.

## Site header — all `/`, `/spaces*`, `/about`, `/privacy`, `/me*`, 404   (role: both)
- ≥ 768: logo link to `/` (img «مساحة» / «Masaha»); nav «التنقّل الرئيسي» / «Main navigation» with links «الرئيسية», «المساحات», «عن مساحة» / «Home», «Spaces», «About Masaha» (`aria-current=page` on the current); language toggle role=button «English» in Arabic / «العربية» in English (copy.preferences.languageName of the other language); theme toggle role=button aria-label «المظهر الداكن» / «Dark theme» in light, «المظهر الفاتح» / «Light theme» in dark (copy.preferences.switchTheme); guest: link «تسجيل الدخول» / «Sign in» → `/login`; user: the account button.
- < 768: menu button `button[aria-label="القائمة"]` / `[aria-label="Menu"]`, logo, language toggle; user: avatar-only account button. Sign-in link and theme toggle hidden (they are in the drawer).
- states by click:
  - language: [click the language toggle] → the other language, `<html dir>` flips; stored in `masaha.language`.
  - theme: [click the theme toggle (≥ 768; in the drawer < 768)] → `data-theme` flips; stored in `masaha.theme`.

## Phone menu (drawer) — < 768 only   (role: both)
- states by click:
  - open, guest: [click role=button «القائمة» / «Menu» (copy.site.menu)] → Sheet from the start side, role=dialog «القائمة» / «Menu»; logo; nav «التنقّل الرئيسي» with «الرئيسية», «المساحات», «عن مساحة» (current one tinted); link «تسجيل الدخول» / «Sign in»; footer: theme toggle; X button aria-label «إغلاق القائمة» / «Close menu» (copy.site.closeMenu). Any navigation closes it.
  - open, user: [same click, signed in] → the same nav without sign-in, then group role=group «الحساب» / «Account» (copy.users.section) with the name «سلمى الأغا», links «المفضّلة», «بلاغاتي», «إعدادات حسابي» / «Favourites», «My reports», «Account settings», button «تسجيل الخروج» / «Sign out» (an owner/admin also gets «لوحة التحكم» / «Dashboard»).
  - sign-out failure in the drawer: [open, click «تسجيل الخروج» with `POST /api/v1/auth/logout` answered 500 or aborted] → «تعذّر تسجيل الخروج» / «Couldn’t sign out» + the reason, under the button.

## Account menu — signed-in, all widths   (role: user)
- trigger: role=button aria-label «قائمة الحساب: [[سلمى الأغا]]» / «Account menu: [[سلمى الأغا]]» (copy.users.menu); shows the avatar initial «س» and, from 768, the first name «سلمى».
- states by click:
  - open: [click it] → `[data-slot=dropdown-menu-content]` (role=menu): label «سلمى الأغا» + `demo-user@example.com`; menuitems «المفضّلة», «بلاغاتي», «إعدادات حسابي», «تسجيل الخروج» / «Favourites», «My reports», «Account settings», «Sign out».
  - signing out: [open, click menuitem «تسجيل الخروج» with the logout POST held] → item disabled with a spinner, menu stays open.
  - sign-out failed: [open, click «تسجيل الخروج» with `POST /api/v1/auth/logout` 500/aborted] → alert inside the menu «تعذّر تسجيل الخروج» / «Couldn’t sign out» + «لا يوجد اتصال. تحقّق من الإنترنت وحاول مرة أخرى.» (aborted).
  - signed out: [real click] → `POST /api/v1/auth/logout` 204, back to guest header.

## Site footer — the site shell only   (role: both)
- tagline «مساحة — دليل مساحات العمل المشتركة في قطاع غزة» / «Masaha — a directory of coworking spaces in the Gaza Strip»; links «تصفّح المساحات» (/spaces), «عن مساحة» (/about), «سياسة الخصوصية» (/privacy), «تواصل معنا» (/about#contact) / «Browse spaces», «About Masaha», «Privacy Policy», «Contact us». On a space page below 768 with a contact bar, it gets bottom padding for the bar.

## Focus shell — `/login`, `/register`, `/forgot-password`, `/reset-password`, `/change-password`   (role: both)
- header: logo link to `/`, then language toggle + theme toggle at **every** width (no menu, no sign-in, no footer); the card is centred from 768. `/change-password`'s header holds only «تسجيل الخروج» / «Sign out».

## Route error boundary — inside either shell   (role: both)
- states by URL: block the page's lazy module request (dev: the `/src/pages/site/…/XPage.tsx` script request after navigating client-side) or go offline before navigating → «لا يوجد اتصال بالإنترنت» / «No internet connection» + «ستظهر البيانات عند عودة الاتصال.» + buttons «إعادة المحاولة» / «Try again», «الرئيسية» / «Home». A retry that still fails adds «ما زال الاتصال مفقودًا.» / «Still no connection.».

## Toasts — every shell   (role: both)
- region «الإشعارات» / «Notifications» (sonner, `[data-sonner-toast]`), close button «إغلاق الإشعار» / «Close notification». Document title pattern «{page} · مساحة» / «{page} · Masaha».
