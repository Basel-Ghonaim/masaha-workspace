## The real run (2026-10-28, `masaha_dev`; scripts `run2.mjs`, `run2-ann.mjs`, `run2-breaks.mjs` on `cdp2.mjs`; shots `shots\lead\`)

- The API on 3320 and the web on 5320 (`npm run dev`), started for the run; `masaha-postgres-1` up. Headless Chrome over
  CDP; Enter sent with its text; no `/auth/` body kept; no phone printed. Every line below is from
  `scripts\run2-log.txt` and the cases' output.
- **PR 3 — before the run, the named script** (`reports3.mjs`, as `demo-reception`, `POST /api/v1/spaces/:slug/reports`):
  `masaha-demo` HOURS «تجربة: الساعات» → 201 id 1; `noor-hub` (verified, `demo-directory-owner`'s) PRICES → 201 id 2;
  `tuffah-place` (unverified, listed) OTHER «تجربة: أخرى» → 201 id 3.
- **PR 3, the owner** (ar 1440): «بلاغات البيانات» — "بلاغ واحد", the report «زائر · 28 أكتوبر», the day only; «فتح» → the
  sheet «بلاغ عن ساعات العمل», **its first focus on the reply's textarea** (LB-D7 confirmed in a browser); the reply
  «صحّحنا الساعات», «تم التصحيح» → toast «عُلّم «تم التصحيح» | في «تمت المراجعة» | أُرسل الردّ لصاحب البلاغ. | عرض»; the
  focus back on «فتح»; `PATCH /api/v1/manage/spaces/7/data-reports/1 200 Idempotency-Key: none body:
  {"status":"RESOLVED","note":"صحّحنا الساعات"}`. Shots `3-owner-*` (ar light / en dark × 390, 768, 1440).
- **PR 3, the admin** (ar 1440): the intro, the chips, «المساحة» / «كل المساحات», «الحقل»; 3 rows, the reporter named
  (ليلى النجار) and «يعالجه» (الإدارة / المالك); the space combobox searched «نور» → «كل المساحات | نور هب» → the address
  `?space=48` and the tag «إزالة فلتر المساحة» (shots at 1440, 390, 768); the verified space's report «عرض» → read-only
  «مساحة موثّقة — يقرّر مالكها هذا البلاغ. للاطلاع فقط. | عرض المساحة»; «مسح الفلاتر» → the address empty; tuffah-place's
  «فتح» → «ردّ فريقنا», the reply «تجربة: لا يلزم تعديل», «لم يُعتمد» → `PATCH /api/v1/admin/data-reports/3 200
  Idempotency-Key: none body: {"status":"DISMISSED","note":"تجربة: لا يلزم تعديل"}`. English dark at 390, 768, 1024 (the
  table from 1024, cards below), 1440.
- **PR 4a** (reception): «بلاغاتي» — 3 reports, «ردّ فريقنا» / «ردّ إدارة المساحة» with the replies, the chips, the
  account's navigation «حسابي» (ar/en × 390, 768, 1440). From `noor-hub`'s page: «الإبلاغ عن معلومة غير صحيحة» → the
  dialog «بلاغك عن نور هب يصل إلى إدارة المساحة، وتجد ردّها في «بلاغاتي».», its first focus on the field's select;
  «المرافق», «إرسال» → toast «أرسلنا بلاغك إلى إدارة المساحة. ستجد ردّها في «بلاغاتي». | عرض بلاغاتي»; the focus back on
  the button; `POST /api/v1/spaces/noor-hub/reports 201 Idempotency-Key: none body: {"field":"AMENITIES"}`. **The same
  again** → info toast «أرسلت بلاغًا عن هذا من قبل، وما زال قيد المراجعة.»; `POST … 200` (the open one, S15). **As a
  guest** (en): the button → «Sign in to report information», «Create account → /register?next=%2Fspaces%2Fnoor-hub |
  Sign in → /login?next=%2Fspaces%2Fnoor-hub» → signed in → back on `/spaces/noor-hub` with the report's dialog open →
  closed, **0 writes**.
- **PR 4b** (reception): a Directory card's heart «Save Radwan Study Hall to favourites», **pressed at once** (`true`
  before the answer), toast «Added to favourites | Radwan Study Hall | Undo» → «Undo» → not pressed; `POST
  /api/v1/me/favorites/51 204 Idempotency-Key: none`, `DELETE /api/v1/me/favorites/51 204 Idempotency-Key: none`. Home's
  first card (ar) → «أُضيفت إلى المفضّلة | قاعة الرضوان للدراسة | تراجع», `POST …/51 204`. `noor-hub`'s page at 390: the
  heart in the name's block → saved, `POST …/48 204`. **The guest's heart** on `sada-space` → «Sign in to save spaces to
  your favourites» → signed in → toast «حُفظت Sada Space في المفضّلة», `POST …/49 204`, and the heart unpressed:
  **LEAD-D12's defect, fixed** (above). «المفضّلة»: «3 مساحات محفوظة», the cards with their status; «الأقرب إليّ» (the
  device's point by CDP geolocation, the permission granted) → «مرتبة حسب المسافة من موقعك…», 0.3 / 1.5 / 2.5 km, `GET
  /api/v1/me/favorites?sort=distance 200`; a card's heart → «أُزيلت من المفضّلة | نور هب | تراجع» → «تراجع»; `DELETE …/48
  204`, `POST …/48 204` (no key). Shots ar/en × 390, 768, 1440.
- **PR 2, reception** (en 1440): «New announcement» → the sheet, its first focus on the checked type's radio; General,
  «إعلان تجربة», «No end»; **the post offline** (CDP) → the sheet's lost line «No answer came back. Try again — it won’t be
  published twice.» with «Try again» → online, «Try again» → toast «Announcement published | In “Active” | Show». **The
  network log: four `POST /api/v1/manage/spaces/7/announcements`, all `Idempotency-Key:
  1cc56cf9-aa48-4979-9be2-7eb3265e90f8` — three `failed (net::ERR_INTERNET_DISCONNECTED)` (the transport's re-sends), then
  201; one announcement** («Active 1»). The first script then stopped at the «Ended» tab (Radix's tabs change on a mouse
  press, not a click), so the next writes' network lines were not kept; **the audit log** of space 7, read after as the
  owner (`auditcheck.out.txt`), gives them in order: `announcement.edited` 13:29:21 (its English text; «Announcement
  saved»), `announcement.ended` 13:29:24 («The announcement has ended | In “Ended” | Undo»), `announcement.edited`
  13:29:26 («Undo» → «The announcement is back as it was»), `announcement.ended` 13:29:28 (the focus on the «Active» tab
  once the card left). Continued (`annReception2`): «Ended» → «⋯» → «Delete…» → «Delete the announcement “General · 28
  October 15:29–15:29”? | It leaves this list. It can’t be brought back.» → `DELETE …/announcements/2 204` (no key); an
  Offer «عرض تجربة» from **29 October 09:00** (the calendar and the time) → `POST …/announcements 201 Idempotency-Key:
  9b2acc81-… body: {"type":"OFFER","textAr":"عرض تجربة","startsAt":"2026-10-29T07:00:00.000Z"}` (Gaza's 09:00 that day) →
  «Scheduled» → «Start now» → `POST …/announcements/3/start 200` (no key) → «Delete…» («It leaves the space’s page at
  once…») → `DELETE …/3 204`.
- **PR 2, the owner**: a Temporary closure «إغلاق تجربة» from **27 October 08:00** (yesterday), no end, its line «Visitors
  see the space as “Closed now”…», the preview the closure's notice → `POST …/announcements 201 Idempotency-Key:
  2f246030-… body: {"type":"CLOSURE","textAr":"إغلاق تجربة","startsAt":"2026-10-27T06:00:00.000Z"}`; reception's card reads
  «يمدّد المالك الاشتراكات بعد بدء الإغلاق.», the owner's offers «تمديد الاشتراكات» (shots `2-active-*`, both roles, ar/en
  × 390, 768, 1440). **While it ran, the space page as a guest** (ar/en × 390, 768, 1440): the notice «إغلاق تجربة |
  إعلان من إدارة المساحة · من 27 أكتوبر 08:00 · بلا نهاية» above the name at every width, the status «مغلق الآن»; no
  announcements section (the running closure was the only one, DI-59). Then «End now» → «The closure has ended · the
  status is automatic again | In “Ended” | Undo», `POST …/4/end 200`; «Extend subscriptions» → `GET
  …/4/extend-subscriptions 200`, the dialog «The extension moves 4 subscriptions. | Those the closure covered, and their
  renewals not started yet… | The closure’s days: 2 days (27 October – 28 October)», its first focus on the days; **1
  typed** → «Extend 4 subscriptions» → `POST …/4/extend-subscriptions 201 Idempotency-Key: dcb8f9db-… body: {"days":1}`;
  toast «Subscriptions extended | 4 subscriptions · 1 day»; the card «Extended 4 subscriptions · 1 day · أحمد الشوا · 28
  October | Its subscriptions were extended, so it isn’t deleted and its end isn’t moved later.» **The preview's count
  4; the subscriptions moved: 4** (#128's count: those the closure covered and their renewals not started). Shots
  `2-ended-*` (both roles, ar/en × 390, 768, 1440).
- **Width breaks** (from backup copies, restored by copy, "restored true"): the sheet's date and time at 768 `162px
  162px`, with `sm:grid-cols-2` removed `336px` (one column, `break-sheet-period-reception-ar-light-768.png`); at 390
  one column (357px) in both languages. The favourites' grid at 1440 `290.656px 290.672px 290.656px`, with
  `xl:grid-cols-3` removed `444px 444px` (`break-favorites-grid-reception-ar-light-1440.png`; a first try replaced only
  the first of the file's two grids, the gone spaces', and stayed three: redone on both).
- **Touch targets** at 390 with touch emulation: the announcements' «⋯» 44×44; the page's heart 44×44; a card's heart
  44×44; `FilterTag`'s remove button 44×44.
- **The refresh limit:** after ≈ 40 sign-ins the API answered `POST /auth/refresh` 429 (30 per 15 minutes): the last
  two sessions came up as a guest (a card's heart then read «حفظ»; its size stands). The account menu's case waited for
  the window.
- **Not performed, by design:** a 429 on a dialog (their tests own it); `FAVORITES_LIMIT_REACHED` (200 saves); «إزالة» of
  a space that left the directory (no favourite of reception's has left, and the data is never changed to make one —
  test 81 owns it); a second guest save to show LEAD-D12's fix in a browser (a write beyond §13; the new test owns it);
  the announcements section beside a running closure (no other announcement ran then; tests 83, 84).
