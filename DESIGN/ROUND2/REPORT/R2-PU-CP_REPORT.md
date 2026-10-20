# R2-PU-CP — The public site · Content and Arabic copy

## 1. Commits

- `HEAD` (C:\dev\masaha\app-design): `18ab1705149773bd05f2f7349ef341e33d175ca3`
- `origin/main` after `git fetch origin`: `eff0a3d1e332a0161fde267a9a100f889184f550`
- They differ; `git diff --quiet HEAD origin/main -- docs/design` exits **0**: **design unchanged**, review continued on `HEAD`.

## 2. Verdict

The Arabic reads as Arabic in most places, but the copy around location, counts and the brand name makes promises that are untrue or ambiguous (the privacy line in states where nothing is sent, «في قطاع غزة» under active filters, «فريق مساحة», «غير متاحة»), and the English mirror still leaks Arabic titles and turns «محافظة غزة» into "Gaza City".

## 3. The five most important points

1. The reworded privacy line «يُرسَل موقعك مقرَّبًا…» appears in the denied and imprecise states, where nothing was sent; in the imprecise state it follows «لذلك لم نستخدمه» (R2-PU-CP-001).
2. The result count says «لا توجد مساحات في قطاع غزة» / «مساحة واحدة في قطاع غزة» when filters or a search narrowed the list, so it states something false about the Strip (R2-PU-CP-003).
3. The filter sheet's button reads «عرض 6 نتيجة» and «عرض 0 نتيجة» (wrong number agreement, and a button that shows nothing), under a subtitle saying the filters already apply at once (R2-PU-CP-004).
4. «فريق مساحة» (the brand) reads as "the space's team", the opposite of what it means, in the unverified notice, About and the report toast (R2-PU-CP-005); «هذه المساحة غير متاحة» reuses the live-status word for "not found" (R2-PU-CP-006).
5. Copy for owners says they update the live status themselves («وتحدّث حالتها … بنفسك»; Home's «وتحديث … حالتها المباشرة»), which contradicts the automatic status that About's own verified card describes (R2-PU-CP-007).

> **How the pages were seen (an override, stated).** The Claude-in-Chrome extension's only connected browser is "Browser 1", a **macOS** machine, which cannot reach this Windows machine's `127.0.0.1:5412`: every prototype URL showed Chrome's error page (example.com loaded, so the extension itself worked). My tab there was closed. Instead, each page was rendered in a local headless Chrome (fresh profile, driven over CDP from a scratchpad script), at the stated viewport, and every quoted string was read from the **rendered page** with in-page JavaScript (`document.body.innerText`, `document.title`, `closest('[lang]')`) — the same reading `javascript_tool` gives — never from the source alone. Captures come from the same headless Chrome (`Page.captureScreenshot`), and each PNG was opened and checked.

## 4. Issues

Base URL: `http://127.0.0.1:5412/`. Evidence folder: `C:\dev\masaha\workspace\DESIGN\ROUND2\shots\r2-shots\PU-CP\`.

### R2-PU-CP-001 — The privacy line says the location is sent in states where nothing was sent
- **type:** defect · **level:** pattern · **impact:** high
- **where:** 03 · "Location denied — phone 390" and "Location imprecise (outside Gaza / > 2 km) — phone 390"; `Directory.html?loc=denied`, `Directory.html?loc=imprecise`, `Home.html?loc=denied`, `Home.html?loc=imprecise`; 390, light; `docs/design/screens/03-directory-views-states/10-location-denied-phone-390.webp`
- **evidence:** `R2-PU-CP-001.png` (`Directory.html?loc=denied`, 390)
- **what is wrong:** the denied state reads «اختر منطقتك أو حدّد موقعك على الخريطة لنرتّب المساحات حسب المسافة. يُرسَل موقعك مقرَّبًا لترتيب المساحات حسب المسافة فقط، ولا يُحفظ.» The browser refused the location, yet the line says it *is* sent. The imprecise state contradicts itself: «…لذلك لم نستخدمه. يُرسَل موقعك مقرَّبًا…». EN does the same: "…so we didn’t use it. Your location is sent rounded…". The Alert also says «حسب المسافة» twice.
- **proposal:** in denied/imprecise, a conditional line: «إن حدّدت موقعك، نرسله تقريبيًا لترتيب المساحات فقط، ولا نحفظه.» / "If you set your location, we send it approximately, only to sort the spaces, and never store it." Keep the present-tense line (R2-PU-CP-002) for granted and manual only.
- **why:** a privacy promise has to be literally true in the state where it appears. Here, someone who just refused permission is told their location is being sent.
- **cost:** S (one more string in `location.jsx`, used by the two failure states)
- **rule:** DECISIONS_PUBLIC "Changed 2026-10-13" (the reworded privacy line is open); lens A.11.

### R2-PU-CP-002 — «مقرَّبًا» is a calque of "rounded", and the passive hides who sends it
- **type:** improvement · **level:** pattern · **impact:** medium
- **where:** 03 · "Location allowed · sorted «الأقرب إليّ» — phone 390"; `Directory.html?loc=granted` (also Home `?loc=granted`, `Directory.html?loc=manual`, and the picking text on `?view=map&loc=picking`: «ويُرسَل مقرَّبًا ولا يُحفظ»); 390, light; `docs/design/screens/03-directory-views-states/06-location-allowed-sorted-phone-390.webp`
- **evidence:** `R2-PU-CP-002.png`
- **what is wrong:** «يُرسَل موقعك مقرَّبًا لترتيب المساحات حسب المسافة فقط، ولا يُحفظ.» An Arabic reader doesn't say «مقرَّبًا» (rounded, as of a number) for an imprecise location, and it can be read as "brought near". The passives with no agent («يُرسَل … ولا يُحفظ») read as a translation of "is sent … never stored" and never say *to whom* it is sent. The line also sits right under «مرتبة حسب المسافة من موقعك…» and repeats «حسب المسافة».
- **proposal:** «نرسل موقعًا تقريبيًا (لا موقعك الدقيق) إلى مساحة لترتيب المساحات فقط، ولا نحفظه.» / "We send an approximate location (not your exact one) to Masaha, only to sort the spaces, and we never store it." Picking text: «…نرتّب المساحات حسب المسافة منه، ونرسله تقريبيًا ولا نحفظه.» (with R2-PU-CP-005's brand marking if adopted).
- **why:** it says plainly what leaves the phone, to whom, how precise it is and what it is for, which are the four things a privacy line has to answer. It also reads as Arabic said first.
- **cost:** S (`shared.jsx` `PRIVACY_LINE`, `location.jsx` picking text)
- **rule:** DECISIONS_PUBLIC "Changed 2026-10-13"; lens A.10.

### R2-PU-CP-003 — The result count states something false about the Strip when filters or a search are active
- **type:** defect · **level:** page · **impact:** high
- **where:** 03 · "No results — phone 390"; `Directory.html?loc=none&demo=noresults` (also `?loc=none&available=1&verified=1` → «مساحة واحدة في قطاع غزة», `?loc=none&q=zm` → «مساحة واحدة في قطاع غزة»); 390, light; `docs/design/screens/03-directory-views-states/20-no-results-phone-390.webp`
- **evidence:** `R2-PU-CP-003.png`
- **what is wrong:** with one filter active, the count reads «لا توجد مساحات في قطاع غزة» above «لا توجد مساحات تطابق الفلاتر». EN: "No spaces in the Gaza Strip". With both switches on it reads "1 space in the Gaza Strip". The area filter alone switches the line to «3 مساحات في المناطق المحددة», so only the non-place filters keep the Strip wording. U1's «6 مساحات في قطاع غزة» describes the **default set**. Applied to a filtered set, it is untrue.
- **proposal:** with a filter or search active (other than place): «مساحة واحدة تطابق بحثك» · «3 مساحات تطابق الفلاتر» · none: «لا نتائج» / "1 space matches your filters" · "No results". Keep «… في قطاع غزة» only for the unfiltered set.
- **why:** the count is the first thing people read after filtering, and it must not tell a student that Gaza has one workspace, or none.
- **cost:** S
- **rule:** DECISIONS_PUBLIC U1 (misapplied); lens A.11.

### R2-PU-CP-004 — «عرض 6 نتيجة» / «عرض 0 نتيجة»: wrong agreement, and a label that doesn't say what happens
- **type:** defect · **level:** component (the shared `FilterSheet` footer) · **impact:** medium
- **where:** 03 · "Filters sheet — phone 390"; `Directory.html?loc=none&demo=noresults&sheet=filters` («عرض 0 نتيجة»), `Directory.html?loc=none&sheet=filters` («عرض 6 نتيجة»), `Directory.html?loc=none&sheet=filters&area=nasr,rimal&period=day&priceMax=20` («عرض 3 نتيجة»); 390, light; `docs/design/screens/03-directory-views-states/22-filters-sheet-phone-390.webp`
- **evidence:** `R2-PU-CP-004.png` (the 0 case)
- **what is wrong:** after 3–10, Arabic takes the plural («6 نتائج»); «نتيجة» is only right from 11 up. «عرض 0 نتيجة» invites a tap that shows an empty list. The sheet's own subtitle says «تُطبَّق فورًا على النتائج», so the button applies nothing (it only closes the sheet), yet it reads like a submit. EN "Show 0 results" has the same problem.
- **proposal:** make it follow the count: 0 → «لا نتائج — غيّر الفلاتر»; 1 → «عرض المساحة»; 2 → «عرض المساحتين»; 3–10 → «عرض 6 مساحات»; 11+ → «عرض 12 مساحة». EN "Show 6 spaces", "No results — change the filters". Counting *spaces* also matches the page's count line.
- **why:** correct Arabic number agreement, and the button says what the user is about to see.
- **cost:** S (the page already has a plural helper: «مساحتان»، «3 مساحات»)
- **rule:** DECISIONS_SHARED P5 («عرض N نتيجة»: the pattern, misapplied for N = 0–10); prompt §5.4–5.5.

### R2-PU-CP-005 — «فريق مساحة» reads as "the space's team", the opposite of what it means
- **type:** defect · **level:** pattern · **impact:** high
- **where:** 04 · "Golden Hub · unverified, stale price, no photos — phone 390"; `Space details.html?id=golden&loc=none` (also `?id=white`, `?id=zm`, About's «جمعها فريق مساحة», and the toast «أرسلنا البلاغ إلى فريق مساحة» after sending a report on `?id=golden&loc=none&auth=1&dialog=report`); 390, light; `docs/design/screens/04-space-details-variants/08-golden-hub-unverified-stale-price-no-photos-phone-390.webp`
- **evidence:** `R2-PU-CP-005.png`
- **what is wrong:** «جمع فريق مساحة هذه المعلومات ولم تؤكدها إدارة المساحة بعد». The brand «مساحة» is also the glossary's word for a space, and nothing marks it as a name, so «فريق مساحة» naturally reads as "a space's team". That happens on the very notice whose point is that the *space* has confirmed nothing. EN is unambiguous ("The Masaha team…"), so the two languages say different things. «تؤكدها» also lacks the shadda the site uses elsewhere («تأكّد»).
- **proposal:** mark the brand whenever it follows a noun: «جمع فريق منصّة «مساحة» هذه المعلومات، ولم تؤكّدها إدارة المساحة بعد». Or the shorter «جمع فريقنا هذه المعلومات…», since About already says «جمع فريقنا». Toast: «أرسلنا البلاغ إلى فريقنا». About card: «جمعها فريقنا».
- **why:** the unverified notice and the report routing exist to say *who* stands behind the data, so the brand must not be read as the space.
- **cost:** S (strings on three pages: the Space details notice, the toast, About)
- **rule:** glossary *Space* / *Unverified space*; lens A.10. U10's dialog line is under §5 (decisions in doubt).

### R2-PU-CP-006 — «هذه المساحة غير متاحة» reuses the live-status word for "not found"
- **type:** defect · **level:** page · **impact:** medium
- **where:** 04 · "Space not found / hidden — phone 390"; `Space details.html?id=focus&loc=none&state=notfound`; 390, light; `docs/design/screens/04-space-details-variants/18-space-not-found-hidden-phone-390.webp`
- **evidence:** `R2-PU-CP-006.png`
- **what is wrong:** «متاح» is the glossary's live state, "has room now" (About: «فيها مكان الآن»). So «هذه المساحة غير متاحة» also reads as "this space has no free seat", while the body says it may have been removed. EN "This space isn’t available" is just as ambiguous next to "Available".
- **proposal:** «لم نجد هذه المساحة» + «ربما أُزيلت من الدليل، أو أن الرابط غير صحيح.» / "We couldn’t find this space".
- **why:** one word should keep one meaning across the site, and "not found" must not sound like "full".
- **cost:** S
- **rule:** glossary *Live status* (Available · متاح).

### R2-PU-CP-007 — Owners are told they update the live status themselves; the status is automatic
- **type:** defect · **level:** pattern · **impact:** medium
- **where:** 10 · "About «عن مساحة» — phone 390"; `About.html` (section «لأصحاب المساحات», `#owners`), and Home's owner card on `Home.html?loc=none`; 390, light; `docs/design/screens/10-about-error-pages/02-about-phone-390.webp`
- **evidence:** `R2-PU-CP-007.png`
- **what is wrong:** About step 3: «تصبح مساحتك موثّقة، وتحدّث حالتها وأسعارها وساعاتها بنفسك.» / "…and you update its status, prices and hours yourself." Home: «تواصل معنا لإضافة مساحتك وتحديث ساعاتها وأسعارها وحالتها المباشرة.» / "…keep its hours, prices and live status up to date." The same About page says, for a verified space, «وتظهر حالتها المباشرة تلقائيًا، ويمكنها ضبطها يدويًا لفترة قصيرة», and for «متاح» «وتُحدَّث الحالة تلقائيًا من حركة الحضور». So the owners are promised the very thing visitors are told doesn't happen.
- **proposal:** About step 3: «تصبح مساحتك موثّقة: تحدّث أسعارها وساعاتها بنفسك، وتظهر حالتها المباشرة تلقائيًا من تسجيل الحضور.» / "Your space becomes verified: you keep its prices and hours yourself, and its live status shows automatically from check-ins." Home: «تواصل معنا لإضافة مساحتك، وإدارة ساعاتها وأسعارها، وإظهار حالتها المباشرة.» / "Contact us to add your space, manage its hours and prices, and show its live status."
- **why:** an owner should know the status comes from the front desk, or they will expect to set it and visitors will distrust it.
- **cost:** S (About, Home)
- **rule:** DECISIONS_PUBLIC U11 (the verified card says the state is automatic); glossary *Live status*, *Manual state override*.

### R2-PU-CP-008 — "Stale" is worded three ways; the prices section breaks U4's line
- **type:** defect · **level:** pattern · **impact:** medium
- **where:** 04 · "Focus Hub · verified + stale price (40 days) — phone 390"; `Space details.html?id=focus&loc=none&demo=stale`; 390, light; `docs/design/screens/04-space-details-variants/04-focus-hub-verified-stale-price-40-days-phone-390.webp`
- **evidence:** `R2-PU-CP-008.png`
- **what is wrong:** the stale prices read «قد تكون الأسعار تغيّرت — آخر تحديث قبل شهر», while every other stale section on the site reads «قد يكون تغيّر» (Golden Hub's hours, amenities and contacts), and About promises «فنعرض «قد يكون تغيّر» بجانب المعلومة القديمة». The glossary's term is a third form: *Stale* «قد تكون قديمة». The prices line also drops the section's own «آخر تحديث للأسعار …» form and moves the date into the warning. EN: "Prices may have changed — updated a month ago" vs "May have changed".
- **proposal:** one form everywhere: the section's usual «آخر تحديث للأسعار قبل شهر» followed by the «قد يكون تغيّر» badge, then the Alert body «تأكّد من السعر مع المساحة قبل الذهاب.» If the price warning keeps its own title, use «قد تكون الأسعار تغيّرت» in **every** section's badge instead («قد تكون الساعات تغيّرت»…), and align the glossary.
- **why:** About teaches users one marker to look for, so the page should show that marker.
- **cost:** S (`space-parts.jsx`; one glossary line if the owner prefers the longer form)
- **rule:** DECISIONS_PUBLIC U4 (misapplied); glossary *Stale*.

### R2-PU-CP-009 — An unverified space's hidden prices: «السعر غير محدّث» with no date and no word that they are hidden
- **type:** improvement · **level:** component (`PriceGrid`, unverified + stale) · **impact:** medium
- **where:** 04 · "Golden Hub · unverified, stale price, no photos — phone 390"; `Space details.html?id=golden&loc=none`; 390, light; `docs/design/screens/04-space-details-variants/08-golden-hub-unverified-stale-price-no-photos-phone-390.webp`
- **evidence:** `R2-PU-CP-009.png`
- **what is wrong:** the whole «الأسعار» section is one muted line, «السعر غير محدّث — تواصل مع المساحة» (EN "Price not up to date — contact the space"). It is singular for a set of prices, it doesn't say that prices exist but are hidden, and it is the only section on the page without its «آخر تحديث …» date, although U4 gives each section its own. The sections below it on the same page say «آخر تحديث لساعات العمل قبل شهرين» + «قد يكون تغيّر».
- **proposal:** «لا نعرض الأسعار لأنها لم تُحدَّث منذ مدة. اسأل المساحة عن السعر الحالي.» + the section's «آخر تحديث للأسعار قبل …» / "We don’t show the prices because they haven’t been updated in a while. Ask the space for the current price." + "Prices updated … ago".
- **why:** it tells the user why there is no number and how old the last one was, in the same form as every other section.
- **cost:** S
- **rule:** DECISIONS_PUBLIC U4.

### R2-PU-CP-010 — The report dialog opens with a fragment, «عن فوكس هاب.»
- **type:** improvement · **level:** component (`ReportDialog`) · **impact:** low
- **where:** 04 · "Signed in · report wrong info — phone 390"; `Space details.html?id=focus&loc=none&auth=1&dialog=report` (and `?id=golden…`: «عن غولدن هاب. يراجع فريق مساحة البلاغ…»); 390, light; `docs/design/screens/04-space-details-variants/16-signed-in-report-wrong-info-phone-390.webp`
- **evidence:** `R2-PU-CP-010.png`
- **what is wrong:** «عن فوكس هاب. يصل البلاغ إلى إدارة المساحة، وتجد ردّها في «بلاغاتي».» The first "sentence" is only a prepositional phrase, a word-for-word "About Focus Hub." It reads as a translation and makes the routing sentence start cold.
- **proposal:** keep U10's settled routing words and fold the name in: «بلاغك عن فوكس هاب يصل إلى إدارة المساحة، وتجد ردّها في «بلاغاتي».» / "Your report on Focus Hub goes to the space’s management; you’ll find their reply in “My reports”."
- **why:** one natural Arabic sentence that still names the space and says who reads it.
- **cost:** S
- **rule:** DECISIONS_PUBLIC U10 (wording around it, not its routing words).

### R2-PU-CP-011 — The report's success toast drops where the reply lands, and its EN mirror differs
- **type:** improvement · **level:** component (`ReportDialog` toast) · **impact:** low
- **where:** 04 · "Report · unverified space, read by the team — phone 390" (53); `Space details.html?id=golden&loc=none&auth=1&dialog=report`, after choosing «الأسعار», typing details and pressing «إرسال»; 390, light; screenshot — (53 has none yet)
- **evidence:** `R2-PU-CP-011.png`
- **what is wrong:** the toast reads «أرسلنا البلاغ إلى فريق مساحة» (verified: «أرسلنا البلاغ إلى إدارة المساحة»). Once the dialog closes, nothing says where the answer will appear, and U10's whole point (who reads it, where the reply lands) is gone. EN verified reads "We sent your report to the space", while the AR and the dialog say "the space’s management".
- **proposal:** «أرسلنا بلاغك إلى إدارة المساحة. ستجد ردّها في «بلاغاتي».» / "We sent your report to the space’s management. You’ll find their reply in “My reports”." Unverified: «أرسلنا بلاغك إلى فريقنا. ستجد الردّ في «بلاغاتي».» / "…to the Masaha team…".
- **why:** the confirmation is the last thing the user sees, so it should carry the promise the dialog made, the same way in both languages.
- **cost:** S
- **rule:** DECISIONS_PUBLIC U10; DECISIONS_SHARED P8 (a toast saying what changed).

### R2-PU-CP-012 — Home names one control two ways: heading «الأقرب إليك», button «الأقرب إليّ»
- **type:** defect · **level:** page · **impact:** low
- **where:** 02 · "Location allowed · «الأقرب إليك» — phone 390"; `Home.html?loc=granted`; 390, light; `docs/design/screens/02-home-states/04-location-allowed-phone-390.webp`
- **evidence:** `R2-PU-CP-012.png`
- **what is wrong:** the section heading «الأقرب إليك» sits right beside the pressed button «الأقرب إليّ» (EN "Nearest to you" / "Nearest to me"), so the same idea switches person within one row. The Directory uses only «الأقرب إليّ».
- **proposal:** heading «المساحات الأقرب إليك» / "Spaces nearest you", so it names the list rather than echoing the button. Or keep «الأقرب إليّ» on the button only and title the section «بالقرب منك».
- **why:** a heading and a control that differ by one letter look like a typo, and the heading should say what the list is.
- **cost:** S
- **rule:** lens A.10 (named two ways); DECISIONS_PUBLIC U2 (the control's name).

### R2-PU-CP-013 — The mirror changes the place: «محافظة غزة» becomes "Gaza City"
- **type:** defect · **level:** pattern · **impact:** medium
- **where:** 02 · "Default · «متاحة الآن» — phone 390", English mirror; `Home.html?loc=none&lang=en` (also every card's area line on Home and the Directory: AR «النصر، غزة», EN "An-Nasr, Gaza City"); 390 and 1440, light; `docs/design/screens/01-flow/01-1-home.webp`
- **evidence:** `R2-PU-CP-013.png`
- **what is wrong:** Home's area cards read «الرمال · محافظة غزة · 3 مساحات» in Arabic but "Al-Rimal · Gaza City · 3 spaces" in English, so one language names the governorate and the other a city. The cards read «النصر، غزة», where «غزة» could be either. The hero «اعثر على مساحة عمل في غزة» / "Find a workspace in Gaza" and the title «مساحات العمل في غزة» use a third, vaguer «غزة», while the count says «قطاع غزة» (U1: the directory covers the Strip).
- **proposal:** cards: «النصر، محافظة غزة» or, shorter, «النصر · غزة» with EN "An-Nasr · Gaza Governorate" (or "Gaza (gov.)" if it must be short). Area cards: EN "Gaza Governorate · 3 spaces". Hero: «اعثر على مساحة عمل في قطاع غزة» / "Find a workspace in the Gaza Strip".
- **why:** a user in Khan Younis must be able to tell that "Gaza" means the Strip in the hero and the governorate on the card, and both languages must name the same place.
- **cost:** S–M (Home, Directory cards, the space page's area line; the lookup's EN governorate name)
- **rule:** glossary *Governorate*, *Area*; DECISIONS_PUBLIC U1; prompt §5.7.

### R2-PU-CP-014 — The English mirror keeps Arabic document titles on Home, the Directory and About
- **type:** defect · **level:** pattern · **impact:** medium
- **where:** 03 · "List — desktop 1440", English mirror; `Directory.html?loc=none&lang=en` (also `Home.html?loc=none&lang=en`, `About.html?lang=en`); 390 and 1440, light; `docs/design/screens/03-directory-views-states/01-list-desktop-1440.webp`
- **evidence:** `R2-PU-CP-014.png`. The tab title isn't drawn in a screenshot, so the capture adds a yellow strip at its foot, written by the capture script, with `document.title` as read from the page. The page itself is unaltered.
- **what is wrong:** with `<html lang="en">`, `document.title` is «المساحات — مساحة» (Directory), «مساحة — مساحات العمل في غزة» (Home) and «عن مساحة — مساحة» (About). Space details and Error switch to English ("Focus Hub — Masaha", "Page not found — Masaha"). The tab, the history, a bookmark and a shared link's preview all show Arabic to an English reader.
- **proposal:** "Workspaces — Masaha", "Masaha — Coworking spaces in the Gaza Strip", "About Masaha — Masaha" (or simply "About — Masaha").
- **why:** the title is the page's name everywhere outside the page, so the mirror isn't complete without it.
- **cost:** S (three pages)
- **rule:** prompt §5.7 (no leftover Arabic); DECISIONS_PUBLIC U3 (the document title uses the interface's name).

### R2-PU-CP-015 — The imprecise state says the accuracy is "less than 2 km", which is backwards
- **type:** defect · **level:** component (`LocationStatus`) · **impact:** medium
- **where:** 03 · "Location imprecise (outside Gaza / > 2 km) — phone 390"; `Directory.html?loc=imprecise` (and `Home.html?loc=imprecise`); 390, light; `docs/design/screens/03-directory-views-states/12-location-imprecise-outside-gaza-2-km-phone-390.webp`
- **evidence:** `R2-PU-CP-015.png`
- **what is wrong:** «يبدو أن الموقع خارج قطاع غزة أو أن دقته أقل من 2 كم، لذلك لم نستخدمه.» Accuracy isn't measured in km. The case in question is an error margin *larger* than 2 km, but «دقته أقل من 2 كم» literally says the precision is within 2 km, which is the good case. EN "less accurate than 2 km" has the same muddle.
- **proposal:** «يبدو أن موقعك خارج قطاع غزة، أو أن هامش الخطأ فيه أكبر من 2 كم، فلم نستخدمه.» / "Your position seems to be outside the Gaza Strip, or off by more than 2 km, so we didn’t use it."
- **why:** it states the real condition, so a user knows that moving outdoors or turning on GPS may help.
- **cost:** S
- **rule:** prompt §5.6 (numbers and distances).

### R2-PU-CP-016 — The price filter's help line reads as a translation
- **type:** improvement · **level:** page · **impact:** low
- **where:** 03 · "Filters sheet — phone 390"; `Directory.html?loc=none&sheet=filters`; 390, light (and the sidebar at 1440 EN: "The range reads the chosen period’s price."); `docs/design/screens/03-directory-views-states/22-filters-sheet-phone-390.webp`
- **evidence:** `R2-PU-CP-016.png`
- **what is wrong:** «النطاق على سعر الفترة المختارة.» is a word-for-word rendering ("the range on the price of the chosen period") with no verb. EN "The range reads the chosen period’s price." is unidiomatic too.
- **proposal:** «يُطبَّق «من» و«إلى» على سعر اليوم» (the chosen period's name filled in: «سعر الساعة / اليوم / الأسبوع / الشهر») / "From and To apply to the day price".
- **why:** it names the period actually chosen, so the user doesn't have to connect the chips to the fields themselves.
- **cost:** S
- **rule:** DECISIONS_PUBLIC U5; lens A.10.

### R2-PU-CP-017 — A shift is named two ways on one page, and neither matches the glossary
- **type:** defect · **level:** page · **impact:** medium
- **where:** 04 · "Branch Hub · ممتلئ, shifts + per-shift prices, 3 photos — phone 390"; `Space details.html?id=branch&loc=none`; 390, light; `docs/design/screens/04-space-details-variants/06-branch-hub-shifts-per-shift-prices-3-photos-phone-390.webp`
- **evidence:** `R2-PU-CP-017.png`
- **what is wrong:** the price chips read «اليوم الكامل · الدوام الصباحي · الدوام المسائي», and the hours, a few lines below, read «الورديات: صباحي 08:00–16:00 · مسائي 16:00–22:00». The same two parts of the day are «دوام» in one place and «وردية» in the other, and the glossary's term is *Shift* · **وردية**. EN is consistent ("Morning shift" / "Shifts: Morning…"), so only the Arabic splits.
- **proposal:** chips «اليوم كاملًا · الوردية الصباحية · الوردية المسائية»; hours «الورديات: الصباحية 08:00–16:00 · المسائية 16:00–22:00».
- **why:** a visitor matching a price to its hours must see the same word in both places.
- **cost:** S
- **rule:** glossary *Shift*; lens A.10.

### R2-PU-CP-018 — Distances: "approximately" said twice, and «1.0 كم»
- **type:** improvement · **level:** component (`SpaceCard` distance) · **impact:** low
- **where:** 03 · "Location allowed · sorted «الأقرب إليّ» — phone 390"; `Directory.html?loc=granted` (and Home `?loc=granted`, the space page with `loc=granted`); 390, light; `docs/design/screens/03-directory-views-states/06-location-allowed-sorted-phone-390.webp`
- **evidence:** `R2-PU-CP-018.png`
- **what is wrong:** under «مرتبة حسب المسافة من موقعك. المسافات تقريبية بخط مستقيم.», every card again says «على بعد 0.7 كم تقريبًا», «على بعد 1.0 كم تقريبًا». The ".0" is noise in Arabic or English ("About 1.0 km away").
- **proposal:** cards «على بعد 0.7 كم» · «على بعد 1 كم» / "0.7 km away" · "1 km away", leaving the approximation to the status line once. For a single card out of context (the space page), keep «نحو 0.7 كم».
- **why:** less repetition on every card of a phone list, and numbers written the way people say them.
- **cost:** S (`fmtKm`)
- **rule:** prompt §5.6.

### R2-PU-CP-019 — «المفضلة» and «المفضّلة»: one word, two spellings
- **type:** defect · **level:** pattern · **impact:** low
- **where:** 04 · "Signed out · heart → sign-in dialog — phone 390"; `Space details.html?id=focus&loc=none&dialog=signin` («سجّل الدخول لحفظ المساحات في المفضلة»); the heart's toast on `?id=focus&loc=none&auth=1` («أُضيفت إلى المفضلة»); against «تعذّر حفظ فوكس هاب في المفضّلة» (`&fav=1&fail=fav`) and «حُفظت فوكس هاب في المفضّلة» (`&toast=welcomefav`); 390, light; `docs/design/screens/04-space-details-variants/14-signed-out-heart-sign-in-dialog-phone-390.webp`
- **evidence:** `R2-PU-CP-019.png`
- **what is wrong:** the page's own strings spell the favourites list both with and without the shadda, so the same word changes form between the dialog and the toast that follows it.
- **proposal:** «المفضّلة» everywhere (the account menu and «المفضّلة» page already use it): «سجّل الدخول لحفظ المساحات في المفضّلة», «أُضيفت إلى المفضّلة», «أُزيلت من المفضّلة».
- **why:** one written form per term, as the rest of the site does with «موثّقة».
- **cost:** S
- **rule:** lens A.10 (named two ways).

### R2-PU-CP-020 — Contact labels mix Arabic and Latin in the Arabic interface
- **type:** improvement · **level:** component (contacts list) · **impact:** low
- **where:** 04 · "Focus Hub · verified, متاح, fresh, 5 photos, location allowed — phone 390"; `Space details.html?id=focus&loc=none` (also `?id=branch`: «TikTok»; `?id=numberone`: «Instagram»); 390, light; `docs/design/screens/04-space-details-variants/02-focus-hub-verified-fresh-5-photos-location-allowed-phone-390.webp`
- **evidence:** `R2-PU-CP-020.png`
- **what is wrong:** the list reads «واتساب · اتصال — جوال · بريد · Instagram · Facebook». WhatsApp is written in Arabic, but the other three services aren't, so one list follows two rules.
- **proposal:** «إنستغرام · فيسبوك · تيك توك» in Arabic, keeping the handle values in Latin (`@focushub.example`).
- **why:** the labels match each other, and an Arabic screen reader says the words naturally.
- **cost:** S
- **rule:** prompt §5.7.

### R2-PU-CP-021 — «خطأ في الموقع» on About: «الموقع» is also the site's word for location
- **type:** improvement · **level:** page · **impact:** low
- **where:** 53 · "About · contact for everyone — desktop 1440", seen at 390; `About.html` («تواصل معنا», `#contact`); 390, light; screenshot — (53 has none yet)
- **evidence:** `R2-PU-CP-021.png`
- **what is wrong:** «اكتب لنا بسؤال، أو عن بلاغ لم يصلك ردّه، أو عن خطأ في الموقع.» Across the public site «الموقع» means *location* («مسح موقعي», «الموقع» section, «الموقع» in the report's choices), so «خطأ في الموقع» can be read as "a mistake in a space's location". «اكتب لنا بسؤال» is also a calque of "write to us with a question".
- **proposal:** «راسلنا إن كان لديك سؤال، أو بلاغ لم يصلك ردّه، أو مشكلة في الموقع الإلكتروني.» / "Message us with a question, a report that got no reply, or a problem with the website."
- **why:** it removes a misreading the page's own vocabulary creates, and reads as Arabic.
- **cost:** S
- **rule:** DECISIONS_PUBLIC U11 (the contact section); lens A.10.

### R2-PU-CP-022 — The sort control shows a value its menu does not offer
- **type:** improvement · **level:** page · **impact:** low
- **where:** 03 · "Location allowed · sorted «الأقرب إليّ» — phone 390"; `Directory.html?loc=granted`, the sort menu opened; 390, light; `docs/design/screens/03-directory-views-states/06-location-allowed-sorted-phone-390.webp`
- **evidence:** `R2-PU-CP-022.png` (the menu open over the trigger; R2-PU-CP-018's frame shows the closed trigger)
- **what is wrong:** the trigger reads «الترتيب: حسب المسافة» (EN "Sort: By distance"), but opening it lists only «الأحدث تحديثًا · حسب الاسم» (EN "Recently updated · By name"). The words promise a choice that the list doesn't contain. Picking either option silently ends distance sorting, which only «إيقاف الترتيب حسب المسافة» says out loud.
- **proposal:** while near-me is on, add a checked, read-only first item «حسب المسافة (الأقرب إليّ)» / "By distance (nearest to me)", so the open list matches its trigger. Or let the trigger read «الترتيب: الأقرب إليّ» to point at the control that owns it.
- **why:** a select whose label isn't among its options reads as a fault, and the user can't tell how to return to it.
- **cost:** S
- **rule:** DECISIONS_PUBLIC U2 (distance left the sort list; the trigger still names it).

### R2-PU-CP-023 — «لم يكن الخطأ منك.» reads as a translation of "It wasn’t your fault"
- **type:** improvement · **level:** page · **impact:** low
- **where:** 10 · "General error — phone 390"; `Error.html?type=error` (and `&fail=retry`: «ما زال الخطأ قائمًا. حاول بعد قليل.»); 390, light; `docs/design/screens/10-about-error-pages/06-general-error-phone-390.webp`
- **evidence:** `R2-PU-CP-023.png`
- **what is wrong:** «حدث خطأ غير متوقع» + «لم يكن الخطأ منك. حاول مرة أخرى بعد قليل.» The reassurance is a calque. «الخطأ» also repeats the title's word in a different sense (fault vs. error), and the failed-retry line repeats «حاول بعد قليل».
- **proposal:** «المشكلة عندنا، لا عندك. حاول مرة أخرى بعد قليل.» / "The problem is on our side, not yours. Try again in a moment." Failed retry: «ما زالت المشكلة قائمة. نعمل على حلّها.» / "It’s still not working. We’re on it." (only if that's true; otherwise «ما زالت المشكلة قائمة. جرّب بعد دقائق.»).
- **why:** it reads as Arabic said first, and the two lines no longer echo each other.
- **cost:** S
- **rule:** DECISIONS_PUBLIC "The errors" (PU-024); lens A.10.

### R2-PU-CP-024 — "Sort: Recently updated" is cut to "Recently update" at 1440
- **type:** defect · **level:** page · **impact:** low
- **where:** 03 · "List — desktop 1440", English mirror; `Directory.html?loc=none&lang=en`; 1440, light; `docs/design/screens/03-directory-views-states/01-list-desktop-1440.webp`
- **evidence:** `R2-PU-CP-024.png`
- **what is wrong:** the trigger's text is "Sort: Recently updated" (read from the page), but it renders as «Sort: Recently update»: the text needs 154 px and the box gives 146 px, so the final "d" is clipped and the visible word is wrong.
- **proposal:** a shorter label that fits the fixed control in both languages: "Sort: Latest updates" / «الترتيب: آخر تحديث», or "Sort: Newest" if the owner wants it shorter.
- **why:** a clipped label that still looks like a whole word reads as a typo in the product.
- **cost:** S
- **rule:** prompt §5 (a string too long for its control, reported as copy).

## 5. Decisions in doubt

- **U10's «يراجع فريق مساحة البلاغ» (settled dialog line).** It carries the ambiguity of R2-PU-CP-005: «فريق مساحة» reads as "the space's team", in the one sentence meant to say the *space* is **not** who reads it. Proposal: «يراجع فريقنا البلاغ، وتجد الردّ في «بلاغاتي».» / unchanged EN. Cost S.
- **The live states are masculine; everything around them is feminine.** The glossary fixes «متاح · ممتلئ · مغلق الآن». On the same card they stand beside «موثّقة», on the space page beside «مغلقة مؤقتًا اليوم», and in About «ممتلئ» is explained as «مفتوحة، لكن لا أماكن شاغرة الآن». A reader agrees these with «المساحة» (feminine) and sees the gender flip. Not a defect while the glossary stands, but «متاحة · ممتلئة · مغلقة الآن» would read as one voice with the rest. The cost is M: glossary, foundation's state names, every page and the dashboard's public-state control. It is the owner's call.
- **P5's «عرض N نتيجة» as a fixed string.** Settled as a pattern, but Arabic needs the count's agreement (R2-PU-CP-004). The pattern should be stated as "a count-aware label", not one string.

## 6. What was not reviewed, and why

- **The Chrome extension's view.** The only connected browser is a macOS Chrome that can't reach this machine's `127.0.0.1:5412`, so every page was read and captured in a local headless Chrome instead (see the note under §3). Nothing was judged from source alone.
- **Dark mode.** Not opened page by page. The public pages' strings are chosen by language only (`tr(ar, en)`), and none of the reviewed strings depends on the theme, so no dark-only copy was expected. Not observed, so not claimed.
- **Arabic at 1440 and every page at 768.** Out of this prompt's widths (Arabic 390; English 390 and 1440). EN 1440-only strings were read ("Clear", "2 areas chosen", "Below the minimum", "Status & contact").
- **States with no URL and no capture:** the geolocation prompt and the live switch from «الأقرب إليّ» off to on (headless Chrome has no location to grant); the map's hover names on pins; the toast after «إيقاف الترتيب حسب المسافة» or «مسح موقعي», if any; the search field's typing. The report dialog's send, the favourite toggle, the sort menu and the failed retries were driven by script and are reported.
- **The account pages a public flow lands on** (Sign in, Register, Favourites, My reports): another part's scope.
- **Repository state at the end.** The http.server (PID 20172) was stopped and port 5412 answers nothing. `git status --short` in `C:\dev\masaha\app-design` is **not empty**: it lists `?? R2-DK-DF-test.png` and `?? R2-DK-DF-test2.png`. I didn't write them (the names belong to the DK-DF review), and earlier in this run it listed `?? r2-shots-tmp/`, also not mine and now gone. I left them untouched. This review saved nothing inside `app-design`: captures are in `…\ROUND2\shots\r2-shots\PU-CP\` and scripts in the session scratchpad.
