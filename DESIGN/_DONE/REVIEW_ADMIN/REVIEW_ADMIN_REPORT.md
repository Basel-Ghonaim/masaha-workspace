# Design review 2 — the admin's dashboard

Reviewer: design-review-admin · 2026-10-10 · read-only
Source: `git archive origin/main docs/design` (49cd088), served on `http://127.0.0.1:5341/`.
Evidence: `C:\Users\basel\Downloads\design-review-admin\AD-0nn.png` (one per issue; a cropped card where
the issue is one section). Captured with headless Chrome at 390 (touch), 768 and 1440, Arabic and
English, light and dark; the layout numbers below (overflow, table widths, hit targets, headings,
tab panels) were measured in the DOM, not read off the pictures.
Scope: screens 25–32, board sections 42–49 and the admin frames of 50–52. Settled decisions
(`DECISIONS_SHARED.md`, P1–P10 and SH-005…SH-022) are applied, not re-reported; where a page needs a
choice in applying one, or where a built screen already disagrees with one, it is said so.

## 1. Summary

1. **The space edit screen is divided into seven sections that the API cannot save.** Basics and
   Location are one fact group (`profile`) with one date and one confirm; Photos is no fact group at
   all. The screen gives each its own Save, its own «آخر تحديث» and its own «المعلومات ما زالت
   صحيحة» — which the server answers 409 on any group never saved (AD-001, AD-004). This is the next
   screen to be built, so it matters most.
2. **"Add space" is the edit screen with seven saves for a space that does not exist yet** (AD-002).
   The code already chose one form with one submit (#57). What is still missing from the design is
   the other half: nothing leads the admin from the new space to the five fact groups it is now
   missing (AD-003).
3. **The admin's one-way doors are drawn as ordinary ones.** The one-time password can be closed
   before it is read (AD-018); a role is changed to «مالك», which ADR 0009 says the links own, with
   no confirmation and no word about the person's spaces (AD-020); a deleted space can be reached
   only through a ten-second Undo, although the API restores it forever (AD-013).
4. **The same job is done two ways.** Linking an owner to a space is a dialog with radio buttons on
   the spaces page and a sheet with checkboxes on the owners page, with different rules and
   different consequences, and neither says who already owns the space (AD-015). The lookups edit the
   same two switches in the row and again in the sheet (AD-025).
5. **The phone is the weakest width.** At 390 the shift rows are cut off the screen, invisible and
   unreachable (AD-007); the seven-section form has no section navigation below `lg` (AD-011); and
   almost every control in the admin is under the 44 px touch target the foundation sets — 95 on the
   edit screen, 128 on the lookups (AD-030).

**Counts.** 30 issues: by level — design system 1, pattern 2, page 27. By impact — high 11,
medium 16, low 3. By type — defect 19, improvement 11. Six cross-page proposals (P1–P6) carry most
of them.
**The space edit screen** carries AD-001 … AD-012 (and P1, P2 below); its proposals are gathered in
§2 P1.

## 2. Patterns (proposals that change many pages)

Built from foundation §12 components. None needs a new design-system component.

### P1 · The space edit screen is five fact groups, one profile and one gallery (AD-001, AD-004, AD-008, AD-010, AD-011)

The page's division follows the contract's `FactGroup` (`profile | hours | prices | amenities |
contacts`), because that is what can be saved, dated and confirmed:

| Section | Saves | Its date | «ما زالت صحيحة» |
|---|---|---|---|
| **المساحة** (names, descriptions, area, addresses, landmark, pin) | `PATCH /admin/spaces/:id` | the profile's | yes |
| **ساعات العمل** (the week and the shifts) | `PUT …/hours` | hours | yes |
| **الأسعار** | `PUT …/prices` | prices | yes |
| **المرافق** | `PUT …/amenities` | amenities | yes |
| **التواصل** | `PUT …/contacts` | contacts | yes |
| **الصور** | the photo endpoints | — | — |

- **One profile section, two groups of fields inside it** («الأساسيات» and «الموقع» as `Separator`-ed
  blocks under one `CardTitle`, one footer, one date). Today they are two cards with two dates
  («قبل أسبوعين» and «قبل شهر») for one server-side date.
- **A group that was never saved says so** — «لم تُضف بعد» in place of «آخر تحديث …» — and offers
  **Save only**, never Confirm (the contract answers 409). The space's `missingGroups` names them.
- **Photos keeps no freshness line and no Confirm.**
- **Each section's title is an `h2`** (SH-017), so the side navigation's anchors land on headings.
- **Below `lg` the side navigation becomes a row of chips** under the page header, scrolling
  horizontally, with the current section marked; above `lg` the sticky list marks it too.
- Pages: Admin space edit (`?id=`, `?new=1`, `?id=focus`); the owner's Space profile reuses it
  (review 3 decides the owner's copy — it has Capacity as a sixth, private section).

### P2 · A space's state is two facts, and a deleted space has a way back (AD-013, AD-014)

- The list's **state** column shows `verified | unverified` as its badge and **adds** a «مخفية»
  badge beside it, instead of replacing it. The row keeps both facts, as `AdminSpace` does
  (`isVerified`, `isHidden`), and hiding no longer erases whether an owner edits the space.
- **Freshness** shows what is stale (warning) **and what is missing** (neutral) — the built list
  already does, the prototype shows stale only.
- **Deleted** is a fourth choice of the status filter, listing the soft-deleted spaces with
  «استرجاع» on each row. It needs `status=deleted` in `GET /admin/spaces` (§5 lists none today) and
  the existing `POST …/restore`. Pages: Admin spaces; the overview's counters.

### P3 · One way to link an owner to a space (AD-015, AD-016, AD-017, AD-019)

One flow, reached from both pages, with the same words and the same consequence line:

- **From a space** (spaces list › «ربط مالك»): choose **one person** — a `Combobox` searching the
  owners and the users by name or email, not a radio list of everyone; suspended accounts are
  excluded, and each option says what it is («مالك · Focus Hub» / «مستخدم»).
- **From a person** (owners page › «ربط بمساحة»): choose **one space at a time** — a `Combobox` over
  the spaces, each option carrying its state badge and its current owner.
- **Unlinking names the link it removes**: from the space, the menu lists one item per owner
  («فك ربط أحمد»), as the owners page already does.
- Both say the consequence before the act, in the same sentence as the confirmation:
  linking an unverified space → «تصبح موثّقة ويعدّلها مالكها»; unlinking the last owner → «تصبح غير
  موثّقة وتختفي حالتها المباشرة».
- Pages: Admin spaces, Admin owners.

### P4 · Say what the action will do, before it is done (AD-017, AD-018, AD-020, AD-026)

Every admin action is felt by someone else, so P8 and P9 are not enough on their own: the screen
also says, **before** the act, what it will do to that person.

- **Adding an owner** says in the sheet, above the submit: «سيُنشأ حساب ويظهر رمز مرور مؤقت مرة
  واحدة — جهّز طريقة تسليمه» (or, for an email that already has an account, «سيُرقّى حسابه ولن تظهر
  كلمة مرور»).
- **The one-time password dialog cannot be dismissed by accident**: no close X, no Escape, no click
  outside; its only way out is «تم» — enabled once the password was copied or revealed, with
  «لن تظهر مرة أخرى» beside it. It also records how it was handed over (the audit log already
  prints «صدرت عبر واتساب», which no screen asks for): a one-choice `Select` («واتساب · شفهيًا ·
  أخرى»).
- **Changing a role** is an `AlertDialog` naming the consequence («يفقد لوحة التحكم فورًا» /
  «يحصل على كل صلاحيات الإدارة»).
- Pages: Admin owners, Admin users, Admin spaces, Admin lookups.

### P5 · One toolbar, and one column priority per list at 768 (AD-019, AD-022, AD-028)

Applying the settled P5 and SH-007 to the admin's five lists; the choice per page is the review's:

| List | Columns | At 768 | Filters |
|---|---|---|---|
| Spaces (7) | name · area · state · owner · freshness · last update | **cards** (the table is 675 px in a 638 px frame) | search, place, state, stale |
| Users (7) | name · email · role · method · joined · state | **cards** | search, role, state |
| Data reports (8) | space · field · report · reporter · date · state · handled by | **cards** | status chips **+ space + field** (missing today) |
| Owners (5) | name · email · linked spaces · state | table, email under the name | **search (missing today)**, state |
| Audit log (5) | time · actor · action · target · details | table, details under the target | range, actor, action **+ target search** |

- **The lookups do not page and have no toolbar** — the contract answers them whole (§4's
  exception), so P6 does not apply there. Say it in the fix, so a later reader does not add
  pagination.
- **A switch is not a filter field** (the «بيانات قديمة فقط» switch sits on the labels' line, out of
  step with the three fields beside it): it becomes a `ToggleGroup` chip by the result count.

### P6 · The admin's work queue, not the admin's statistics (AD-023, AD-012, AD-022)

The overview, the reports sheet and the read-only space page each end in a place with nothing to do.
One rule: **every row of the admin's work names its next step, and every page the admin lands on
leads somewhere.**

- The overview's fourth tile becomes «مساحات غير موثّقة بلا مالك» (the admin's own pipeline) in place
  of «مستخدمون جدد هذا الأسبوع», which carries no action.
- «اكتمال البيانات» lists **only what the admin can act on** (unverified and hidden spaces), the
  first five, with «عرض الكل» to `Admin spaces.html?stale=1`; the verified ones are their owners'
  work and are counted in the reports tile instead.
- A report's «تعديل الحقل» carries the report with it (`…&report=r1`): the edit screen shows a
  sticky line «بلاغ مفتوح على الأسعار» with «تم التصحيح» in it, so the admin never has to find the
  report again.
- The read-only verified space gets the three links its own Alert promises: «بلاغات هذه المساحة»,
  «فك ربط المالك», «عرض في الموقع».

## 3. Issues

### AD-001 · The edit screen's seven sections are not the API's five fact groups
- **type:** defect · **level:** page · **impact:** high
- **where:** Edit unverified · banner — desktop 1440 · `Admin space edit.html?id=golden` ·
  `screens/43-admin-spaces/11-edit-unverified-banner-desktop-1440.webp`
- **evidence:** `AD-001.png`
- **what is wrong:** «الأساسيات» and «الموقع» are two cards, each with its own Save, its own
  «آخر تحديث» («قبل أسبوعين» and «قبل شهر») and its own «المعلومات ما زالت صحيحة». Both are the one
  `profile` group: one `PATCH /admin/spaces/:id`, one date in `updatedAt.profile`, one
  `POST …/profile/confirm` (api-contract §5, *Spaces (the admin)*). Two saves would overwrite one
  another's date; two different "last updated" values for one fact group cannot both be true.
- **proposal:** P1 — one «المساحة» section holding both blocks, one footer, one date.
- **why it is better:** what the screen promises to save is what the server saves; the admin reads
  one date per fact group, the same number the public page shows.
- **cost:** M
- **rule:** api-contract §5 (`FactGroup`, `updatedAt`); spaces › *Save a group*.

### AD-002 · "Add space" is the edit screen, with seven saves for a space that does not exist
- **type:** defect · **level:** page · **impact:** high
- **where:** Add space — desktop 1440 · `Admin space edit.html?new=1` ·
  `screens/43-admin-spaces/15-add-space-desktop-1440.webp`; phone ·
  `16-add-space-phone-390.webp`
- **evidence:** `AD-002.png`, `AD-003.png`
- **what is wrong:** `?new=1` renders the same seven cards with seven «حفظ» buttons (all seven
  disabled until a field is touched). Only the profile can be created (`POST /admin/spaces` takes
  the profile alone); every fact group needs a `:spaceId` that does not exist yet. The page's h1 and
  its h2 are both «إضافة مساحة».
- **proposal:** the add page is the profile section alone — the names, the descriptions, the area,
  the addresses, the landmarks and the pin — with one «إضافة مساحة» at the end, as the code chose
  (spaces › *Web decisions*, D1); then P1's edit screen.
- **why it is better:** the form asks only for what the creation can take, and the admin is not
  offered six saves that would fail.
- **cost:** S (the design catches up with the code)
- **rule:** api-contract §5 (`POST /admin/spaces`); spaces › *Web decisions* (D1, D2) — **already
  taken better in code (#57).**

### AD-003 · Nothing leads from the new space to the facts it is missing
- **type:** improvement · **level:** page · **impact:** high
- **where:** Spaces — desktop 1440 · `Admin spaces.html` ·
  `screens/43-admin-spaces/01-spaces-desktop-1440.webp` (after an add)
- **evidence:** `AD-003.png`
- **what could be better:** a space is created with five missing fact groups; the add returns to the
  list, and the list says only «قديمة / محدّثة». The admin must remember which space it just added
  and open its menu to carry on. The design has no screen for «ما زال ناقصًا».
- **proposal:** after the creation, open the edit screen of the new space with a checklist at its
  head: the five groups, each «لم تُضف بعد» or «تمّت», each a link to its section; the list's toast
  keeps «فتح المساحة». The same checklist is the edit screen's header for any space with missing
  groups.
- **why it is better:** a space is useful to a visitor only once hours, prices and contacts exist;
  the admin is shown the remaining work instead of having to recall it.
- **cost:** M
- **rule:** api-contract §5 (`missingGroups`); spaces › *Freshness*; lens B3.

### AD-004 · A group that was never saved still offers «المعلومات ما زالت صحيحة», and Photos has a freshness line
- **type:** defect · **level:** page · **impact:** high
- **where:** Edit unverified — desktop 1440 · `Admin space edit.html?id=golden#photos` ·
  `screens/49-fixes-batch-4/04-admin-unverified-edit-24-hour.webp` (same page)
- **evidence:** `AD-004.png`
- **what is wrong:** every section shows «آخر تحديث …» and, when it is clean, «المعلومات ما زالت
  صحيحة» — Photos included. Photos is not a `FactGroup`: there is no date and no confirm path for
  it, so the button maps to nothing. For a real unverified space most groups are **missing**
  (`updatedAt[group] === null`), and `POST …/<group>/confirm` answers **409** on a missing group; the
  screen shows a date anyway and offers the button.
- **proposal:** P1 — «لم تُضف بعد» and Save only while a group is missing; Photos drops both the
  freshness line and the Confirm.
- **why it is better:** the admin is never offered an action the server refuses, and "last updated"
  stops being shown for data that was never entered.
- **cost:** S
- **rule:** api-contract §5 (`POST …/confirm`, 409 for a missing group; `updatedAt` null).

### AD-005 · The area field offers one governorate's areas
- **type:** defect · **level:** page · **impact:** high
- **where:** Edit unverified · banner — desktop 1440 · `Admin space edit.html?id=golden` (Location) ·
  `screens/43-admin-spaces/11-edit-unverified-banner-desktop-1440.webp`
- **evidence:** `AD-005.png`
- **what is wrong:** the «المنطقة» select lists Gaza City's areas only, with «محافظة غزة» as a fixed
  helper under it. A space in Khan Younis, Rafah, the Middle Area or North Gaza cannot be entered.
- **proposal:** one field over the whole catalogue, the governorates as groups with visible names and
  their active areas under them, as the code chose (lookups › *Web decisions*, D4); no helper naming
  one governorate.
- **why it is better:** every area a space may take is reachable, and the governorate is read from
  the group the chosen area sits in.
- **cost:** S — **already taken better in code (#57, design issue 4).**
- **rule:** api-contract §5 (`areaId`: an active area in an active governorate); lookups › *Web
  decisions*.

### AD-006 · Contact types the platform has not, and the one it has is missing
- **type:** defect · **level:** page · **impact:** high
- **where:** Edit unverified — desktop 1440 · `Admin space edit.html?id=golden#contacts` ·
  `screens/43-admin-spaces/11-edit-unverified-banner-desktop-1440.webp`
- **evidence:** `AD-006.png`
- **what is wrong:** the type list is واتساب · **جوال** · **أوريدو** · بريد · Instagram · Facebook ·
  TikTok · موقع. `CONTACT_TYPES` is `WHATSAPP · PHONE · EMAIL · INSTAGRAM · FACEBOOK · TIKTOK ·
  WEBSITE`: there is no carrier type, and «هاتف» is missing. The read-only view maps the same three.
  Nothing in the form says a value is normalised, although every contact is stored in one form (a
  phone in E.164, an email lowercased, a handle turned into a full `https://` address).
- **proposal:** the seven types of the contract, «هاتف» in place of «جوال» and «أوريدو»; each field's
  helper says the stored form («يُحفظ كـ +97059…», «يُحفظ كـ https://instagram.com/<اسم>»), and the
  value is shown in that form after it is typed.
- **why it is better:** the carrier is not a kind of contact, and the admin sees the value the
  visitor will see before saving.
- **cost:** S
- **rule:** `packages/shared/src/spaces/contacts.ts` (`CONTACT_TYPES`); api-contract §5 (`Contact`);
  BRIEF.md (*contacts are a list … numbers LTR*).

### AD-007 · At 390 the shift rows are cut off the screen
- **type:** defect · **level:** page · **impact:** high
- **where:** Edit unverified · banner — phone 390 · `Admin space edit.html?id=golden#hours` ·
  `screens/43-admin-spaces/12-edit-unverified-banner-phone-390.webp`
- **evidence:** `AD-007.png`
- **what is wrong:** each shift's fields measure 596 px inside a 390 px viewport (`[-256 … 340]`):
  the English name, the Arabic name and the «من – إلى» pair run past the card on both sides, the
  second time input is invisible, and the page does not scroll sideways, so the content cannot be
  reached at all. The cause is two full-width `TimeInput`s in one `flex` row with no `min-w-0`; the
  day rows escape it only because they pass `w-24`. The same row shape is used by the price rows.
- **proposal:** the time pair becomes two `Field`s («من» and «إلى»), side by side with
  `flex-1 min-w-0` from `md` and stacked below it; the day rows keep their two boxes and gain the
  same two labels (today they are an unlabelled pair with a dash).
- **why it is better:** a shift can be entered on a phone at all, and the two boxes say which is
  which without hovering.
- **cost:** S
- **rule:** foundation §9 (phone: single column); foundation §10 (every control has a label).

### AD-008 · The price rows repeat 25 labels, and the shift choice is not the space's
- **type:** improvement · **level:** page · **impact:** medium
- **where:** Edit unverified — desktop 1440 · `Admin space edit.html?id=golden#prices` ·
  `screens/43-admin-spaces/11-edit-unverified-banner-desktop-1440.webp`
- **evidence:** `AD-008.png`
- **what could be better:** five price rows each repeat five labels (المدة · الفئة · الوردية · وصف
  مخصّص · المبلغ) — 25 labels for 5 prices — and «وصف مخصّص» wraps under its own «اختياري» tag. The
  «الوردية» select offers a fixed «بدون وردية · الوردية الصباحية · الوردية المسائية», not the shifts
  the Hours section above actually holds; the contract refuses a `shiftId` that is not the space's,
  and refuses removing a shift a price still uses (409). Nothing says the limits (40 prices, 10
  shifts, 20 contacts, 100 amenities) or that a period+audience+shift+label may not repeat.
- **proposal:** the rows become a small table: the labels once in the header row from `md`, each row
  a line of controls, and on a phone one card per price with its labels. «الوردية» lists the
  section's own shifts (empty → the field is disabled with «أضف ورديات أولًا»). «إضافة سعر» is
  disabled at the limit, with the reason beside it, and a duplicate row is marked on the field that
  would tell it apart.
- **why it is better:** the eye reads five rows instead of twenty-five labels, and a price can only
  name a shift that exists.
- **cost:** M
- **rule:** api-contract §5 (`Price`, one price per period/audience/shift/label, the limits);
  foundation §10 (a disabled control shows its reason).

### AD-009 · Opening hours: the shift rule is not the contract's, and "copy to all days" hides on Saturday
- **type:** defect · **level:** page · **impact:** medium
- **where:** Admin · unverified edit · 24-hour · `Admin space edit.html?id=golden#hours` ·
  `screens/49-fixes-batch-4/04-admin-unverified-edit-24-hour.webp`
- **evidence:** `AD-009.png`
- **what is wrong:**
  - the screen refuses a shift outside the **envelope** of every open day (earliest open → latest
    close); the contract requires a shift to sit inside **the range of at least one open day**. A
    space open 08:00–18:00 on Sunday and 10:00–20:00 on Monday would accept a 08:00–20:00 shift on
    the screen and be refused by the server, and the other way round;
  - «نسخ إلى كل الأيام» appears only on the Saturday row, so the admin must know to start there;
  - a day open around the clock (`0`–`1440`) has no affordance: it is typed as 00:00–24:00 into a
    field whose own rule caps the hour at 23;
  - the shift's Arabic name is required by the contract and its English one optional; neither is
    marked, and an empty name is not caught.
- **proposal:** validate a shift against each open day, naming the day in the error («خارج ساعات
  الأحد»); move «نسخ إلى كل الأيام» into the section's header, applying the first open day; add a
  «24 ساعة» switch per day that sets 00:00–24:00 and hides the two boxes; mark the optional English
  name.
- **why it is better:** the form refuses exactly what the server refuses, and says which day is the
  problem.
- **cost:** M
- **rule:** api-contract §5 (`PUT …/hours`: a shift inside at least one open day; `0`–`1440`;
  `nameEn` optional).

### AD-010 · Required and optional are not marked, and the wrong name is required
- **type:** defect · **level:** page · **impact:** medium
- **where:** Edit unverified — desktop 1440 · `Admin space edit.html?id=golden#basics` ·
  `screens/43-admin-spaces/11-edit-unverified-banner-desktop-1440.webp`
- **evidence:** `AD-010.png`
- **what is wrong:** only «علامة مميزة» carries «اختياري». The section refuses a save without **both**
  names; the contract requires `nameEn` (the slug comes from it) and leaves `nameAr` optional, and
  requires `addressAr` while `addressEn` is optional — the screen asks neither. The landmark is one
  field where the contract has two (`landmarkAr`, `landmarkEn`).
- **proposal:** every field that may stay empty says «اختياري»; the required ones are checked in the
  browser by the contract's schema; the landmark is asked in both languages like the addresses.
- **why it is better:** the admin learns what is needed before the server says so, and an English
  landmark stops being lost.
- **cost:** S — **already taken better in code (#57, design issues 1 and 2).**
- **rule:** api-contract §5 (*The profile*); spaces › *Web decisions*.

### AD-011 · Below 1024 the seven-section form has no navigation
- **type:** improvement · **level:** page · **impact:** medium
- **where:** Edit unverified — 768 (no frame on the board) · `Admin space edit.html?id=golden`;
  phone 390 · `screens/43-admin-spaces/12-edit-unverified-banner-phone-390.webp`
- **evidence:** `AD-011.png`
- **what could be better:** the section list is `hidden lg:flex`, so from 1023 px down the page is
  about 5 400 px of continuous form with no map of itself and no way back to the top. Above `lg` the
  list is sticky but marks no current section, and its «الأسعار المعلنة» does not match the card's
  «الأسعار».
- **proposal:** P1 — a horizontally scrolling row of chips below the page header under `lg`, the
  sticky list above it, both marking the section in view; one name per section in both places.
- **why it is better:** the admin reaches the group it came to fix in one tap, which is how this
  screen is used: a report says the prices are wrong.
- **cost:** M
- **rule:** foundation §9; lens B1.

### AD-012 · The verified space's page is a dead end
- **type:** improvement · **level:** page · **impact:** medium
- **where:** Verified · read-only — desktop 1440 · `Admin space edit.html?id=focus` ·
  `screens/43-admin-spaces/13-verified-read-only-desktop-1440.webp`; English ·
  `screens/51-dashboard-variants-english-ltr-light/06-admin-space-read-only.webp`
- **evidence:** `AD-012.png`
- **what could be better:** the page has **no button at all** in `main`. Its Alert says «لتصحيح
  معلومة، راجع بلاغاتها أو فك ربط المالك» and links to neither. It also repeats the section
  navigation, whose seven anchors now scroll a short read-only list.
- **proposal:** the Alert's two paths become links in it («بلاغات Focus Hub», «فك ربط المالك»), with
  «عرض في الموقع» beside them; the owner is named in the page («يعدّلها أحمد») with a link to the
  owners page; below `lg` the section list disappears.
- **why it is better:** the page tells the admin what it may do next instead of naming it in prose.
- **cost:** S
- **rule:** lens B3 (no dead ends); glossary (*Verified space*).

### AD-013 · A deleted space cannot be found or restored once the toast has gone
- **type:** defect · **level:** pattern · **impact:** high
- **where:** Delete (soft) — desktop 1440 · `Admin spaces.html?del=palm` ·
  `screens/43-admin-spaces/09-delete-soft-desktop-1440.webp`
- **evidence:** `AD-013.png`
- **what is wrong:** the confirmation says «تبقى في قاعدة البيانات ويمكن استرجاعها», which is true of
  the database and false of the interface: the only restore is the toast's ten seconds (finding 44).
  `GET /admin/spaces` never lists a soft-deleted space, so no screen can reach `POST …/restore`.
- **proposal:** P2 — «محذوفة» as a fourth state in the status filter, the rows muted with
  «استرجاع», and the confirmation's line says what is true today until it exists («تختفي من الموقع
  ومن هذه القائمة. يمكنك التراجع مباشرة بعد الحذف.»). Needs `status=deleted` in `GET /admin/spaces`.
- **why it is better:** a soft delete the admin cannot undo is a hard delete with extra storage; and
  the words stop promising a screen that does not exist.
- **cost:** M (S for the words alone)
- **rule:** ADR 0007; api-contract §5 (`DELETE`, `POST …/restore`, `GET /admin/spaces`); spaces ›
  *Web decisions* (the Undo is the only restore).

### AD-014 · Hiding a space erases whether it is verified
- **type:** improvement · **level:** page · **impact:** medium
- **where:** Spaces — desktop 1440 · `Admin spaces.html` ·
  `screens/43-admin-spaces/01-spaces-desktop-1440.webp`; dark ·
  `screens/50-dashboard-variants-arabic-dark/13-admin-spaces-dark.webp`
- **evidence:** `AD-014.png`
- **what could be better:** the state column holds one of موثّقة · غير موثّقة · مخفية. Hidden is a
  different fact (`isHidden`) from verified (`isVerified`): a hidden space still has its owner, who
  still edits it, and the admin cannot see that from the list. «إخفاء» and «إظهار» also give no
  warning that the space leaves the public directory at once.
- **proposal:** P2 — the verification badge always, plus a «مخفية» badge; the menu's «إخفاء» keeps
  its toast («أُخفيت Palm Hub من الموقع»), which the built screen already does.
- **why it is better:** two facts, two badges; the admin knows who may edit a hidden space.
- **cost:** S
- **rule:** api-contract §5 (`AdminSpace.isHidden`, `isVerified`; `AdminSpaceRow.state`).

### AD-015 · Linking an owner is two different flows, and neither says who owns the space
- **type:** defect · **level:** pattern · **impact:** high
- **where:** Link owner — desktop 1440 · `Admin spaces.html?link=golden` ·
  `screens/43-admin-spaces/05-link-owner-desktop-1440.webp`; Link to more spaces ·
  `Admin owners.html?link=o1` · `screens/44-admin-owners/11-link-to-more-spaces-desktop-1440.webp`
- **evidence:** `AD-015.png`
- **what is wrong:**
  - from the space: a `Dialog` with a `RadioGroup` of **every** owner, unpaged and unsearchable, the
    first choice preselected — and the preselected one is **ريما**, a *suspended* owner with no
    space;
  - from the owner: a `Sheet` with a checkbox **per space**, many at once, each space's own owner not
    shown, so linking a second owner to Focus Hub looks the same as verifying Golden Hub;
  - both lists grow without bound: the dialog is a radio list of all owners, the sheet a checkbox
    list of all spaces.
- **proposal:** P3.
- **why it is better:** one flow to learn, no suspended account linked by accident, and the admin
  sees whether it is verifying a space or adding a second owner.
- **cost:** M
- **rule:** api-contract §4 (every list pages); plan › `POST /admin/spaces/:spaceId/managers`;
  ADR 0009 (*Verified means at least one OWNER link*).

### AD-016 · «فك الربط» from the spaces list picks an owner silently
- **type:** defect · **level:** page · **impact:** medium
- **where:** Unlink last owner → unverified — phone 390 · `Admin spaces.html?unlink=numberone` ·
  `screens/43-admin-spaces/08-unlink-last-owner-unverified-phone-390.webp`
- **evidence:** `AD-016.png`
- **what is wrong:** the row menu has one «فك الربط», which takes `owners[0]`. With two owners the
  admin unlinks the older one without choosing, and the confirmation names a person it never
  offered.
- **proposal:** P3 — one menu item per owner, «فك ربط أحمد», as the owners page already does.
- **why it is better:** the admin chooses the link it is breaking.
- **cost:** S
- **rule:** plan › `DELETE /admin/spaces/:spaceId/managers/:userId` (one link at a time).

### AD-017 · The add-owner sheet never says it creates an account
- **type:** defect · **level:** page · **impact:** medium
- **where:** Add owner — desktop 1440 · `Admin owners.html?sheet=add` ·
  `screens/44-admin-owners/03-add-owner-desktop-1440.webp`; existing account ·
  `screens/44-admin-owners/05-existing-account-upgrade-and-link-desktop-1440.webp`
- **evidence:** `AD-017.png`
- **what is wrong:** the sheet asks for a name, an email and any number of spaces, and its submit
  says «إضافة». What follows is an account, a one-time password and up to six links — none of it
  said before the button. The existing-account case is explained in an Alert, the new-account case
  is not. One submit also stands for several server calls (the account, then one link per space),
  and a partial failure has no story.
- **proposal:** P4's line above the submit; one space at a time (P3), so a failure names one link;
  the submit says what it does («إنشاء حساب وربط»).
- **why it is better:** the admin knows a password is about to appear once, and is ready to deliver
  it.
- **cost:** S
- **rule:** ADR 0009 (4); plan › `POST /admin/owners`; lens B6.

### AD-018 · The one-time password can be closed before it is read
- **type:** defect · **level:** page · **impact:** high
- **where:** Temporary password (once) — desktop 1440 · `Admin owners.html?pass=1` ·
  `screens/44-admin-owners/07-temporary-password-once-desktop-1440.webp`; Issue temporary password ·
  `Admin users.html?temp=1` · `screens/46-admin-users/07-issue-temporary-password-desktop-1440.webp`
- **evidence:** `AD-018.png`
- **what is wrong:** the dialog that shows the password once has a close X, closes on Escape and on a
  click outside, and its own text says «لن تظهر مرة أخرى بعد إغلاق هذه النافذة». A mis-tap locks the
  person out of the account that was just created, and the only repair is to issue another password.
  The audit log records how it was handed over («صدرت عبر واتساب»), which no screen ever asks.
- **proposal:** P4 — no X, no Escape, no outside click; «تم» is the only way out, enabled after
  «نسخ»; the channel is chosen in the dialog and written to the audit entry.
- **why it is better:** the one irreversible screen of the admin cannot be dismissed by accident,
  and the log says something the admin actually recorded.
- **cost:** S
- **rule:** security.md (temporary password, changed at first sign-in); glossary (*Audit log*);
  foundation §12 (Dialog).

### AD-019 · The owners page has no search, and its main column has no endpoint
- **type:** defect · **level:** page · **impact:** medium
- **where:** Owners — desktop 1440 · `Admin owners.html` ·
  `screens/44-admin-owners/01-owners-desktop-1440.webp`
- **evidence:** `AD-019.png`
- **what is wrong:** the table has no search, no filter and no paging, while the users list beside it
  has all three. Its «المساحات المرتبطة» column is the page's reason to exist, and no planned
  endpoint answers it: `GET /admin/users` searches users, `…/managers` writes one link. The page also
  lists an owner with no space («ريما · بدون مساحة»), which ADR 0009 rule 2 says cannot persist — the
  global `OWNER` label returns to `USER` when the last link goes.
- **proposal:** keep the page, as a view of `GET /admin/users?role=owner` with its links in the row,
  and give it the search and the state filter the users list has (P5). The endpoint grows the owners'
  links, or the page drops the column and shows the spaces in a row expansion. If the owner prefers
  one list, the alternative is to merge it into Users with a role filter and link spaces only from a
  space — the design loses nothing but the sheet.
- **why it is better:** the admin finds an owner by name among hundreds, and the screen asks the
  server something the server can answer.
- **cost:** M · **the owner's choice** between the two shapes.
- **rule:** plan › Admin (`GET /admin/users`); api-contract §4; ADR 0009 (2).

### AD-020 · «تغيير الدور» sets a role the links own, with no confirmation
- **type:** defect · **level:** page · **impact:** high
- **where:** Change role — desktop 1440 · `Admin users.html?changerole=1` ·
  `screens/46-admin-users/05-change-role-desktop-1440.webp`
- **evidence:** `AD-020.png`
- **what is wrong:** a plain `Dialog` with three radios — مستخدم · مالك · أدمن — and «حفظ». Two
  problems: ADR 0009 rule 2 makes the global `OWNER` a **label kept in sync with the links**, set
  when the first `OWNER` link is created and removed with the last, so «مالك» is not a role the admin
  can grant here (the dialog admits it: «المالك يحتاج ربطه بمساحة»); and granting «أدمن» — the whole
  platform, every space's data — is one radio and one Save, while suspending the same person is an
  `AlertDialog`. Nothing says what happens to an owner's spaces when the role is taken away.
- **proposal:** the choice is «مستخدم» or «أدمن»; «مالك» is shown as a disabled, derived state with
  «يأتي من المساحات المرتبطة به» and a link to the owners page. Changing to or from «أدمن» is an
  `AlertDialog` naming the consequence (P4).
- **why it is better:** the screen stops offering a role the system derives, and the most powerful
  grant on the platform is confirmed like the least.
- **cost:** S
- **rule:** ADR 0009 (2); P9 (*irreversible or felt by others → AlertDialog*).

### AD-021 · A Google-only user loses the recovery item with no reason
- **type:** improvement · **level:** page · **impact:** low
- **where:** Users — desktop 1440 · `Admin users.html` ·
  `screens/46-admin-users/01-users-desktop-1440.webp`
- **evidence:** `AD-021.png`
- **what could be better:** «إصدار كلمة مرور مؤقتة» is simply absent for a user whose method is
  Google. The admin, on the phone with someone locked out, finds no item and no explanation.
- **proposal:** the item stays, disabled, with its reason beside it («حساب Google — يستعيده من
  Google»), as foundation §10 requires of a disabled action.
- **why it is better:** the admin learns why it cannot help, instead of hunting for a missing item.
- **cost:** S
- **rule:** foundation §10 (a disabled control shows its reason); auth.md (Google sign-in).

### AD-022 · Resolving a report leaves the report behind
- **type:** improvement · **level:** page · **impact:** medium
- **where:** Unverified · resolve — desktop 1440 · `Admin reports.html?open=r1` ·
  `screens/45-admin-data-reports-all-spaces/03-unverified-resolve-desktop-1440.webp`; phone ·
  `04-unverified-resolve-phone-390.webp`
- **evidence:** `AD-022.png`
- **what could be better:** the sheet's «تعديل الحقل» navigates away to the edit screen; the report
  stays open, unresolved, and the admin must find it again to mark it. Nothing checks that anything
  was changed before «تم التصحيح». «لم يُعتمد» can be sent with an empty reply, so the reporter is
  told only that it was not accepted. The list filters by status alone — with every space's reports
  in one table there is no way to see one space's.
- **proposal:** P6 — the edit screen carries the report and offers «تم التصحيح» in place; «لم
  يُعتمد» asks for the reply (it is the only thing the reporter will read); the toolbar gains the
  space and the field as filters (P5).
- **why it is better:** one path, one place to finish the job, and a rejected report that says why.
- **cost:** M
- **rule:** overview.md (*Data reports … resolved with an optional note*); plan ›
  `GET/PATCH /admin/data-reports`; lens B3.

### AD-023 · The overview counts instead of queueing, and paints a missing photo red
- **type:** improvement · **level:** page · **impact:** medium
- **where:** Overview — desktop 1440 · `Admin overview.html` ·
  `screens/42-admin-overview/01-overview-desktop-1440.webp`; dark ·
  `screens/50-dashboard-variants-arabic-dark/12-admin-overview-dark.webp`
- **evidence:** `AD-023.png`
- **what could be better:**
  - «بدون صور», «بدون دبوس على الخريطة», «بدون ساعات عمل» are `destructive` badges: red for a fact
    that was never entered, beside amber for data that is out of date. Foundation §5 keeps
    `destructive` for errors and negative states;
  - «مستخدمون جدد هذا الأسبوع» leads to an unfiltered users list and asks for nothing (its «منذ
    السبت» is also a fixed date in the sample);
  - «اكتمال البيانات» is unbounded (every space with anything missing or stale) and mixes rows the
    admin can act on with rows that say «يعدّلها المالك»;
  - the stale tile counts stale only while the card below counts stale **or** missing, so the page
    shows two numbers for one idea.
- **proposal:** P6 — missing becomes `warning` (or `neutral` for photos, which block nothing),
  the fourth tile becomes «غير موثّقة بلا مالك», the card lists the admin's own five with «عرض
  الكل», and both the tile and the card count stale **and** missing.
- **why it is better:** the admin's home becomes the day's work, in the order it should be done.
- **cost:** M
- **rule:** foundation §5 (status roles); api-contract §5 (`stale=true` keeps stale **or** missing).

### AD-024 · The lookups' tabs have no panels
- **type:** defect · **level:** page · **impact:** medium
- **where:** Governorates and areas — desktop 1440 · `Admin lookups.html` ·
  `screens/47-admin-lookups/01-governorates-and-areas-desktop-1440.webp`
- **evidence:** `AD-024.png`
- **what is wrong:** `TabsList` is rendered alone and the content below it sits outside the `Tabs`
  element: the two tabs carry `aria-controls` pointing at ids that do not exist, and the page has
  **0** elements with `role="tabpanel"`. A screen-reader user is told there is a tab panel and never
  reaches one; the arrow keys move the tab but the content is not announced.
- **proposal:** each list sits in its own `TabsContent`, as the code does (lookups › *Web
  decisions*: the two sections under tabs, the tab kept in the address).
- **why it is better:** the tab contract holds, and the tab is linkable.
- **cost:** S — **already taken better in code (#49).**
- **rule:** foundation §11 (6) and §12 (Tabs); foundation §10.

### AD-025 · The lookups edit the same switch twice, and label it a third time
- **type:** improvement · **level:** page · **impact:** medium
- **where:** Amenities — desktop 1440 · `Admin lookups.html?tab=amenities` ·
  `screens/47-admin-lookups/05-amenities-desktop-1440.webp`; Edit area (hidden) ·
  `Admin lookups.html?edit=area` · `screens/47-admin-lookups/03-edit-area-hidden-desktop-1440.webp`
- **evidence:** `AD-025.png`
- **what could be better:** an amenity's row holds «في الفلاتر» and «نشط» as switches **and** repeats
  «ليس في الفلاتر» as a badge two centimetres away; the edit sheet then offers both switches again,
  so the same fact is set in two places with two different feedbacks (the row writes at once, the
  sheet writes on Save). The governorate and area rows repeat the pattern with «نشطة».
- **proposal:** the switches stay in the row, where the built screen puts them and where they are
  one click; the sheet keeps the names and the icon only. The «ليس في الفلاتر» badge goes — the
  switch beside it already says it. «مخفية» stays as a badge, because a hidden row is also greyed.
- **why it is better:** one control per fact, one feedback per control.
- **cost:** S
- **rule:** lookups › *Web decisions* (two switches in the row, each pending on its own write);
  lens B1.

### AD-026 · Reordering a lookup says nothing, and costs one click per step
- **type:** improvement · **level:** page · **impact:** medium
- **where:** Governorates and areas — desktop 1440 · `Admin lookups.html` ·
  `screens/47-admin-lookups/01-governorates-and-areas-desktop-1440.webp`
- **evidence:** `AD-026.png`
- **what could be better:** the arrows move a row with no message, no pending state and no Save, while
  the switch beside them raises a toast. Gaza City holds eleven areas, so moving the last to the top
  is ten clicks and ten whole-list writes (`PUT …/areas/order` replaces the list each time). The
  arrows carry no position, so a keyboard user hears only «تحريك لأعلى».
- **proposal:** the arrow's name carries the position («تحريك «الشجاعية» لأعلى — 11 من 11»), the row
  keeps the focus after the move and the list announces the new position in a live region; the
  arrows of a list wait together while an order is in flight (the code already holds them). A list
  of more than ten rows also offers «ترتيب» in the row's own sheet (a position field), so the last
  row reaches the top in one write.
- **why it is better:** the admin knows the move landed, and a long list is not ten round trips on a
  weak connection.
- **cost:** M
- **rule:** api-contract §5 (`PUT …/order`, the whole list); P8; lookups › *Web decisions*.

### AD-027 · The amenity icons are not the platform's, and most say the wrong thing
- **type:** defect · **level:** page · **impact:** low
- **where:** Amenities — desktop 1440 · `Admin lookups.html?tab=amenities` ·
  `screens/47-admin-lookups/05-amenities-desktop-1440.webp`
- **evidence:** `AD-027.png`
- **what is wrong:** the icon field is a `Select` of design-system component names in English
  («Info», «Search», «CircleCheck»…), nine of them, chosen freely; the eight the platform has are
  `AMENITY_ICON_KEYS` (`wifi · zap · sun · plug-zap · coffee · users · presentation ·
  graduation-cap`). The sample shows the result: «إنترنت» carries a magnifying glass, «كهرباء
  مستقرة» a tick, «مشروبات ساخنة» an information circle.
- **proposal:** a visible grid of the eight, each named, none preselected and the choice required, as
  the code chose.
- **why it is better:** the admin picks a picture, not a class name, and only pictures the directory
  can draw.
- **cost:** S — **already taken better in code (#49).**
- **rule:** `packages/shared/src/lookups/amenityIcons.ts`; lookups › *Web decisions*.

### AD-028 · The audit log leads nowhere and paints seven colours
- **type:** improvement · **level:** page · **impact:** medium
- **where:** Audit log — desktop 1440 · `Admin audit.html` ·
  `screens/48-admin-audit-log-platform-settings/01-audit-log-desktop-1440.webp`
- **evidence:** `AD-028.png`
- **what could be better:** no entry links to what it is about (a space, a user, a lookup), so
  following up means copying a name into another page's search. The action badge takes five of the
  six semantic colours — `user_suspended` is `destructive`, a red row in a log of past events — and
  a rainbow carries no ranking. The range opens on «1 سبتمبر – 29 سبتمبر» with nothing saying it is
  the default, so an older event is simply not there. The actor filter offers one actor.
- **proposal:** the target becomes a link to its page; the badge is `neutral` for every action and
  carries its word, `destructive` kept for the two that end access (`user_suspended`,
  `space_hidden`); the range's trigger reads «آخر 30 يومًا» with «كل الفترة» in it; the actor filter
  appears only once there is more than one actor.
- **why it is better:** the log becomes a way into the records it describes, and colour means
  something again.
- **cost:** M
- **rule:** foundation §5 (status roles; status is never colour alone); plan › `GET
  /admin/audit-log` (the filters the screen implies are not yet in the contract).

### AD-029 · Three page widths and two names for one page
- **type:** defect · **level:** page · **impact:** low
- **where:** Platform settings — desktop 1440 · `Admin settings.html` ·
  `screens/48-admin-audit-log-platform-settings/03-platform-settings-desktop-1440.webp`;
  Lookups · `Admin lookups.html`
- **evidence:** `AD-029.png`
- **what is wrong:** the settings page is `max-w-2xl`, the lookups `max-w-4xl`, every other admin page
  full width, so the content's start edge jumps as the admin moves between them. The sidebar item
  says «الإعدادات» and the page says «إعدادات المنصة» (SCREENS row 32 calls it *Platform settings*).
  The settings page also shares one error object between its three cards, so a failure in one can
  mark another.
- **proposal:** one content width for the admin's forms (`max-w-3xl` for a single-column form page,
  full width for a list); one name, «إعدادات المنصة», in the sidebar and the page.
- **why it is better:** the pages read as one dashboard, and the sidebar names what the page is.
- **cost:** S
- **rule:** foundation §13 (32, *Settings*); lens A1, A10.

### AD-030 · Almost every control in the admin is under the 44 px touch target
- **type:** defect · **level:** design system · **impact:** medium
- **where:** Lookups — phone 390 · `Admin lookups.html` ·
  `screens/47-admin-lookups/02-governorates-and-areas-phone-390.webp`; Spaces — phone 390 ·
  `screens/43-admin-spaces/02-spaces-phone-390.webp`
- **evidence:** `AD-030.png`
- **what is wrong:** measured at 390 with touch emulation: 128 controls under 44 × 44 on the lookups,
  95 on the space edit, 16 on the spaces list, 11 on the users list. The repeat offenders are the
  layer's own sizes: a row's icon button 40 × 40, `size="sm"` 58 × 32, a `Switch` 36 × 20, a filter
  chip 36 high, a text link inside a row 50 × 22. Foundation §10 sets 44 × 44 on touch; foundation
  §5 locks the control height at 40.
- **proposal:** the layer keeps the 40 px look and grows the **hit area** to 44 on touch (a
  pseudo-element or padding on `Button size="icon"`, `size="sm"`, `Switch` and `ToggleGroupItem`
  under a coarse-pointer media query), rather than every screen spacing its rows. See the rule in
  doubt below.
- **why it is better:** the admin's lists are usable with a thumb; nothing moves on a mouse.
- **cost:** M (one change in the layer, every screen fixed)
- **rule:** foundation §10 (44 × 44 on touch) against foundation §5 (*comfortable, 40 px controls*).

## 4. Rules in doubt

1. **foundation §10's 44 × 44 against §5's 40 px controls.** They cannot both hold for an icon
   button, a switch or a chip. Propose: the visual size stays at 40 (and 36 for a switch) and the
   layer guarantees the 44 px hit area on coarse pointers; §10 says "hit area", not "control size"
   (AD-030).
2. **P8 against the lookups' "no toasts" (lookups › Web decisions, #43/#49).** The settled pattern
   says every action raises a success toast; the built lookups deliberately raise none, because the
   row itself shows the new state and a failure stays in its card. Propose: P8 gains the exception —
   **an action whose result is visible in the row it changed says so in the row** (and only a failure
   is announced), which also covers AD-026's reordering.
3. **P1 against "Add space sits above the list, at its end, at every width" (spaces › Web
   decisions, #57).** P1 puts a page's primary action in the phone's fixed bottom bar; the built
   screen put it above the list at every width, because the top bar was full. Both were decided on
   2026-10-10. Propose: P1 holds for an action that is a page's purpose and is used constantly (the
   desk), and the list's "add" stays above the list; whichever the owner picks, one of the two
   documents changes.
4. **ADR 0009 (2) against the planned `PATCH /admin/users` role change.** If the global `OWNER` is a
   derived label, the admin's role control may offer only `USER` and `ADMIN`; the plan's line should
   say so before the endpoint is built (AD-020).
5. **Prototype only — not an authoritative rule:** the prototype's `AdminShell` has no space switcher
   and no «الموقع العام», and its account menu holds sign-out alone; P4 already settles that, and the
   admin's shell is in the shared fix, not here.

## 5. Not reviewed

- **The owner's and reception's pages**, including the owner's own space profile, which reuses the
  edit screen's sections (review 3). Where the admin's screen is fixed, the owner's copy inherits it:
  the owner's version adds Capacity, which is private (glossary) and must never reach the admin's.
- **The public side of what the admin enters** (the directory's cards, the space page's freshness
  lines): review 4.
- **Visible focus** was not verified: a focus set from a script in headless Chrome does not raise
  `:focus-visible`, so the ring needs a real keyboard pass. The tab order and the names were read
  from the DOM; no screen-reader pass was made.
- **Loading, error, offline, 403 and 404** on the admin's pages: the prototype has none, and P7
  settles them; this review did not repeat them per page.
- **Contrast of the admin's own badges in dark** was eyeballed, not measured; the layer's contrast
  test owns it.
- **The archive's known limits** (placeholder navigation icons, sample data reused between spaces,
  the Roboto fallback, the three superseded frames) are not reported. The amenity icons in AD-027 are
  **not** one of them: they are chosen in the design's own picker, from the wrong list.
