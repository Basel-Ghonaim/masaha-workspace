# Design fix 2a — the admin's space editor and its creation form

Worker: the design-fix worker · worktree `C:\Users\basel\masaha-design` (detached at `origin/main`
`d7d800e`, tree clean) · branch `design/admin-editor`, not cut yet · prototype on **5346** (free) ·
images in `C:\Users\basel\Downloads\design-fix-admin-editor\` · subagents used: 1 of 2.

**Approved 2026-10-11** (`PROMPT\FIX_ADMIN_EDITOR_PLAN_REPLY.md`): §13.1 yes (and `Admin owners.html`
only if one expression), §13.2 yes (noted in `CHANGES.md` as waiting on 2b), S1–S10 as recommended,
DI-12/13/14 fold, DI-15 only in the prototype's own code (never `_ds/`), DI-16 not in this item.

**Override, stated:** the plan is written straight to this file, without plan mode, because the
owner's prompt for this session says "plan only: save the plan where the prompt says, then stop"
(CLAUDE.md › *Decision precedence*, 1).

## 1. Summary

Batch 2 is built in two items; this is **2a, the space editor**, which worker A builds next
(S2b-4), and the form that creates a space. The editor stops being seven cards that the API cannot
save and becomes the contract's **five fact groups and a gallery**: one «المساحة» section, then
hours, prices, amenities and contacts, then photos, each with an `h2`, a date or «لم تُضف بعد», and
a section navigation that works below `lg`. «إضافة مساحة» leads to **a creation form as #57 built
it**, which hands the admin to the new space's editor under a «ما زال ناقصًا» checklist. Hours,
prices and contacts take AD-007/008/009/006; the gallery acts at once (O7); the verified space's
page stops being a dead end (AD-012). The owner's Space profile shares the editor and inherits all
of it (O1). The two check scripts fix 1 ran by hand are committed (E8).

## 2. Contract

**Scope.** E1–E8 of the prompt, as amended in `DECISIONS_ADMIN.md` (2026-10-11), inside
`docs/design/`; the archive's documents (`CHANGES.md` *Batch 2a*, `INDEX.md`, `SCREENS.md`,
`README.md`, the board's two «Add space» frames).

**Acceptance criteria.**
- The admin's editor shows six sections — المساحة · ساعات العمل · الأسعار · المرافق · التواصل ·
  الصور — each titled by an `h2`, with one name in the card and in the navigation; no capacity.
- «المساحة» holds «الأساسيات» and «الموقع» as two `Separator`-ed blocks with one footer, one date
  and one «المعلومات ما زالت صحيحة».
- A group never saved says «لم تُضف بعد» and offers «حفظ» only; saving it gives it a date and the
  confirm.
- Below `lg` the navigation is a scrolling row of chips; at every width the section in view is
  marked (`aria-current`).
- «إضافة مساحة» opens a creation form matching #57 (two cards, the grouped area field, «اختياري»
  on every optional field, both landmarks, the pin with no place until given one and its
  coordinates field, one submit). Submitting leads to the new space's editor, headed by the
  checklist; the checklist also heads any space with a missing group.
- Hours, prices and contacts as §4 E4; the gallery as E6; the verified page as E5.
- `Owner space profile.html` shows the shared editor's changes and keeps its own content (the
  prices link row, capacity, its intro line).
- No shift row, price row or contact row overflows the viewport at 390 (measured, AD-007).
- Fix 1's F1 holds: 20 px between a card's last field and its footer.
- Every page touched opens in both languages without a blank render or a console error; every
  `INDEX.md` URL that touched a changed page still resolves.
- `node docs/design/scripts/check-parse.mjs` and `check-classes.mjs` pass; `format:check` and
  `check:links` pass.
- A before/after pair per decision in the images folder, not committed.

**Out of scope.** Batch 2b (the lists, owners, users, overview, reports, lookups, audit,
settings): none of those pages' own content. Batch 5's owner-only differences (prices as a link
row, capacity moving to Settings, no hide/delete): left as they are. The design-system items
(AD-030, SH-017's `CardTitle` level) — worker A. `apps/`, `packages/`, any other folder. The
`screens/` images (regenerated at the end of the phase). Prettier, ESLint or CI wiring for the
scripts. Anything on *Not in v1* (photos stay storage-key photos; no booking, no claiming).

## 3. Reading done

CLAUDE.md · workflow.md · docs/README.md (deferred documents: only the per-endpoint contract
sections, not triggered) · the open findings' titles (44 and 46 opened via `spaces.md`) ·
`DECISIONS_ADMIN.md` with its *Amended* note · `DECISIONS_SHARED.md` (P1 amended, P8, P9, P10) ·
`DECISIONS_OWNER.md` (O1, O7) · `REVIEW_ADMIN_REPORT.md` (AD-001…012 in full, the rest read) ·
`FIX_SHARED_PLAN.md` and `FIX_SHARED_REPORT.md` (F1, F2, the prebuilt-CSS constraint, the scripts) ·
`docs/features/spaces.md` (*Adding a space on the web*, *Web decisions*) · `lookups.md` (*The
area field*, its decisions) · `docs/design/README.md`, `CHANGES.md`, `INDEX.md` (§43, the parameters
table), `SCREENS.md` · foundation §5, §7–§10, §12 · glossary · api-contract *Spaces (the admin)* ·
data-model *Conventions* and *Spaces* · the prototype's `Admin space edit.html`, `Admin spaces.html`,
`Owner space profile.html`, `profile-a.jsx`, `profile-b.jsx`, `admin.jsx`, `shared.jsx`, `map.jsx`,
`admin-data.js`, `data.js`, `details-data.js`, `masaha.css`, and the vendored bundle's exports. The
built creation form (`AddSpacePage`, `AddSpaceForm`, `BasicsFields`, `LocationFields`, `AreaSelect`,
`PointPicker`, its copy) was surveyed by one subagent, read-only.

**What shapes the build** (from fix 1, re-verified): `_ds_bundle.css` is prebuilt, so a new utility
class can be silently dead — layout-only rules go to `masaha.css`. The bundle has `Separator`,
`SelectGroup`/`SelectLabel`, `Table` and its parts, `ToggleGroup`, `Combobox`, `Spinner`; it has
**no** `Progress` and no upload, image, trash or copy icon. `CardTitle` renders a `div`, so a section
title is `<CardTitle><h2>…</h2></CardTitle>`, as #57 does. `TimeInput` caps the hour at 23.

## 4. The decisions, as they will be built

### E1 — the editor: five fact groups and a gallery (A1)
- **One editor, in `profile-a.jsx`/`profile-b.jsx`**, used by both pages: a `SectionNav` (the
  side list from `lg`, the chips below it) and the sections. Each page hands it its sections, its
  groups' dates and missing groups; the admin's come from `admin-data.js` (`upd`, `last`, and
  `missing` read through the five groups — `pin` and `photos` are not groups), the owner's keep the
  strings it has today. **No sample data changes**, so 2b's lists show what they show now.
- **«المساحة»** (`id="profile"`): `CardTitle` `h2`, one date line, then the «الأساسيات» block and
  the «الموقع» block, each with an `h3` in `text-label`, a `Separator` between them; one footer.
  The blocks keep the anchors **`#basics` and `#location`**, so `Admin reports.html`'s «تعديل
  الحقل», the owner's Data reports links and `INDEX.md` still land.
- **`ProfileSection`** gains the group's state: «آخر تحديث قبل …» or **«لم تُضف بعد»**; the footer
  is «حفظ», plus «تجاهل التغييرات» while dirty, plus «المعلومات ما زالت صحيحة» only when the group
  has a date and is clean. Saving a missing group dates it «الآن». P10's always-enabled save and
  its «تغييرات غير محفوظة» badge stay; F1's form layout stays.
- **Titles `h2`** on every card, the photos' and the owner's prices link and capacity cards
  included, so the outline is one level everywhere.
- **`SectionNav`:** from `lg`, today's sticky list; below it, a horizontally scrolling row of
  chips (`Button size="sm"` links), sticky under the top bar. Both mark the section in view with
  `aria-current="location"` and the selected look, driven by one `IntersectionObserver`. Names are
  the cards' own: المساحة · ساعات العمل · الأسعار · المرافق · التواصل · الصور (the old «الأسعار
  المعلنة» goes).
- **The admin has no capacity section** (already true; kept).

### E2 — the creation form (AD-002, #57)
- **A page of its own, `Admin space add.html`** (stronger decision S1), the shape #57 built:
  `AdminShell` titled «إضافة مساحة», a `Breadcrumb` back to «المساحات», then one form: a card
  «الأساسيات» (`h2`; the names and descriptions, `md:grid-cols-2`), a card «الموقع» (`h2`; the area
  in the grid's first column, the addresses and the two landmarks, the map, the coordinates in the
  first column), a failure `Alert` slot, then one start-aligned «إضافة مساحة».
- The fields are the **same `BasicsFields` and `LocationFields`** the editor's «المساحة» uses
  (#57's D3: made for the edit screen to reuse), so the catch-up below reaches both:
  - **the grouped area field** (AD-005): a `Select` with one `SelectGroup` per governorate,
    `SelectLabel` its name, the active areas under it, placeholder «اختر المنطقة», no helper. It
    reads `admin-data.js`'s full catalogue (active only) where the page loads it, else `data.js`'s;
  - **«اختياري»** at the end of every optional label, none on a required one (AD-010): Arabic name,
    the descriptions, the English address, both landmarks optional; English name, Arabic address,
    area and coordinates required;
  - **two landmarks**, «علامة مميزة بالعربية» and «… بالإنجليزية»;
  - **the pin**: no pin on the creation map until a tap places one; the editor's starts at the
    space's location. Under it **«الإحداثيات»**, one `dir="ltr"` field, one value with the pin
    (a tap writes `lat, lng` to five places; typing or pasting moves the pin; Arabic digits and the
    Arabic comma read), helper «خط العرض ثم خط الطول، كما تنسخهما الخريطة: 31.52, 34.45».
- **Checked on submit** with #57's lines (أدخل الاسم بالإنجليزية · أدخل العنوان بالعربية · اختر
  المنطقة · ضع الدبوس على الخريطة أو أدخل إحداثياته · خط العرض ثم خط الطول · هذه النقطة خارج قطاع
  غزة), focus to the first invalid field. `?fail=add` shows «تعذّرت إضافة المساحة» in the slot.
- **On success**, the button's `loading`, then a hand-off toast «أُضيفت {name}» and the new space's
  editor (E3). The profile typed is carried in `sessionStorage`; opened directly, the page shows a
  sample new space.
- **URLs:** `Admin spaces.html`'s «إضافة مساحة» (the only change to that page's content) and the
  board's two «Add space» frames point at the new page; `Admin space edit.html?new=1` **redirects**
  there (`location.replace`, the other parameters carried), so every old link keeps working;
  `INDEX.md` rows 644–645 take the new URL; `SCREENS.md` row 26 names the page.

### E3 — after a creation, the checklist (A2)
- `Admin space edit.html?id=new&created=1`: the new space's editor, its profile from the form, its
  four other groups missing, headed by **«ما زال ناقصًا»**: a `Card` listing the five groups, each a
  link to its section with a `Badge` — «تمّت» (`success`) or «لم تُضف بعد» (`warning`, as A8 sets
  for missing). It updates as each section is saved, and goes once nothing is missing.
- The same checklist heads **any space with a missing group**: `?id=white` (hours missing) and
  `?id=palm` (prices) show it from the existing data. `?id=golden` has none and shows none.
- `CHANGES.md` says the built code still returns to the list until S2b-4.

### E4 — hours, prices, contacts
**Hours** (AD-007, AD-009):
- A day row: its name, the «مفتوحة» switch, a **«24 ساعة»** switch that sets 00:00–24:00
  (`0`–`1440`) and hides the boxes, else **«من» and «إلى» as two labelled `Field`s**, side by side
  (S3).
- A shift row: «الاسم بالعربية», «الاسم بالإنجليزية» **«اختياري»**, then «من»/«إلى» as two `Field`s,
  side by side from `md` with `flex-1 min-w-0`, stacked below — the cause of AD-007 removed.
- **Each shift checked against each open day** (D4: inside the range of at least one): the error
  when it fits none, and the open days it does not fit named on it (S2). Also: an empty Arabic name,
  an end not after the start, a repeated Arabic name (`not_unique`).
- **«نسخ إلى كل الأيام»** in the card's header (`CardAction`, beside the unsaved badge), copying the
  **first open day** in the week's order, 24-hour included, to every open day; closed days stay
  closed.
- `?demo=shifterror` keeps its frame (a shift past every day's close).

**Prices** (AD-008):
- **A small table from `md`**: the bundle's `Table` with one header row — المدة · الفئة · الوردية ·
  وصف مخصّص (اختياري) · المبلغ (₪) · a remove column — each row a line of unlabelled-on-screen
  controls named by their header and row («المدة — السعر 2»). **Below `md`, one card per price**
  with its labels. One is rendered at a time (`useIsTablet`), not both hidden by CSS.
- **«الوردية»** offers «بدون وردية» and the **saved** shifts of the Hours section (S7); with none,
  the column's selects are disabled and the reason is said once above the table, «أضف ورديات في
  ساعات العمل أولًا», linking `#hours`.
- **«إضافة سعر»** disabled at **40** with «الحد 40 سعرًا» beside it; `?demo=pricelimit` fills 40
  rows to show it.
- **A repeat** is marked on the field that tells it apart — the label when it has one, else the
  shift, else the period — «يتكرر سعر بالمدة والفئة نفسيهما».
- The display-only line and the stale note stay.

**Contacts** (AD-006, PU-021):
- The contract's **seven types**: واتساب · هاتف · بريد · Instagram · Facebook · TikTok · موقع.
  The sample's `jawwal`/`ooredoo` rows load as **هاتف** (the data file is not changed: the public
  pages are batch 4's).
- **«هاتف»** shows its carrier **derived from the number** beside it — a neutral `Badge` «جوال» for
  +97059, «أوريدو» for +97056, none otherwise.
- **Each value's helper shows the stored form** as it is typed, from a small normaliser in the
  prototype that follows data-model › *Conventions*: «يُحفظ كـ +970599123456», «… https://instagram.com/name»,
  the email lowercased; a value that cannot be stored is refused on its field on save; a repeat
  once normalised is `not_unique`.

### E5 — the verified space's page (AD-012)
- The `Alert`'s two paths become **links** in it: «بلاغات Focus Hub» → `Admin reports.html?space=focus`
  and «فك ربط المالك» → `Admin spaces.html?unlink=focus` (both need the owner, §13), with
  **«عرض في الموقع»** → `Space details.html?id=focus` beside them.
- **The owner named:** «يعدّلها أحمد», linking `Admin owners.html`.
- **No section list below `lg`;** from `lg` the side list stays for the six read-only sections,
  which take the editor's names and order (المساحة with its two blocks, the hours with the shifts,
  the prices as rows, the seven contact types, the photos).

### E6 — the gallery (A1, O7)
- No date, no «المعلومات ما زالت صحيحة», no «حفظ», no footer.
- **«رفع صور»** opens the file picker; each chosen file becomes a tile at once, with its own
  progress bar (a layout-only rule; the bundle has no `Progress`) and its preview.
- **A failure stays on its tile:** a file over 5 MB (413) or not JPG/PNG (415) says why, with
  «إزالة»; a network failure (`?fail=upload`) says so with «إعادة المحاولة» (S5).
- **Removal** by an `AlertDialog`: «حذف الصورة؟ تختفي من صفحة المساحة فورًا.», destructive «حذف»,
  «رجوع»; then a toast «حُذفت الصورة».
- **Reorder and «اجعلها الغلاف» apply at once**, with no toast (P8's exception), the new position
  said in a polite live region (S10); the 10-photo limit disables the button with its reason.

### E7 — the owner's page shares the editor (O1)
`Owner space profile.html` changes only where the shared editor forces it: its own navigation
becomes `SectionNav`, its Basics and Location become «المساحة». Its own content stays: the intro
line, the unsaved-sections alert, the prices card linking Packages & prices, the capacity section
with its confirm. The report lists what it inherited.

### E8 — the check scripts, committed
- `docs/design/scripts/check-parse.mjs`: every `.jsx` and every page's inline Babel script through
  the vendored `_vendor/babel.min.js` (loaded with `createRequire`), paths relative to the script.
- `docs/design/scripts/check-classes.mjs`: every class in the pages and modules against
  `_ds_bundle.css`, `styles.css` and `masaha.css`; it **fails on a new dead class** and reports the
  six known ones (DI-9) as a baseline listed in the script.
- Node's own modules only; no dependency, no CI wiring. A paragraph in `docs/design/README.md` says
  how to run them and **what they cannot see**: a layout drawn twice, a gap, a misplaced block (fix
  1's F2), or an error that only happens at runtime — those need the browser.

## 5. Stronger decisions

| | What | Why | Cost | Recommend |
|---|---|---|---|---|
| **S1** | The creation form is **its own page**, `Admin space add.html`, and `?new=1` redirects to it | It is the code's shape (its own route); a "new" state inside the editor's file is what the decision forbids in spirit, and the redirect keeps every old URL | one page, one redirect line | **yes** |
| **S2** | A shift's **error** when it fits no open day; the open days it does **not** fit named on it as its helper («لا تنطبق يوم الخميس 08:00–14:00») | The contract accepts a shift inside one day, so naming every other day as an *error* would refuse what the server takes; the helper still says which day is the problem | small | **yes** — the decision's "the error naming the day" read this way |
| **S3** | **Day rows keep «من»/«إلى» side by side at every width;** only the shift rows stack below `md` | Two `w-24` boxes fit at 390 (192 px); stacking seven days doubles the section | none | **yes**, measured at 390 |
| **S4** | The limit-with-reason pattern also for **shifts (10)** and **contacts (20)** | Same contract limits as the prices', same foundation §10 rule | small | **yes** |
| **S5** | A 413/415 tile offers **«إزالة»**, not retry; a network failure offers **«إعادة المحاولة»** | Retrying a file that is too large or of the wrong type fails again | none | **yes** |
| **S6** | The chips row is **sticky** under the top bar (its offset measured from the bar) | AD-011's complaint is also "no way back to the top" of a 5 400 px page | one `masaha.css` rule | **yes** |
| **S7** | «الوردية» offers only **saved** shifts, and says so | The contract's `shiftId` names a saved shift of the space; a new unsaved one has no id | none | **yes** |
| **S8** | `#basics` and `#location` kept as block anchors inside `#profile` | Four pages and `INDEX.md` link them | none | **yes** |
| **S9** | Group dates from the sample data, not hard-coded strings, on the admin's page | The checklist, «لم تُضف بعد» and the dates must agree for one space | small | **yes** |
| **S10** | Photo reorder announced in a polite live region | P8's exception drops the toast, so nothing else tells a screen reader the move landed (as AD-026 for the lookups) | small | **yes** |

No rule of the documents is contradicted. The foundation §7 title-size tension fix 1 recorded
still stands and is not touched.

## 6. Related findings

| Finding | Fold? | Why |
|---|---|---|
| **44** — no screen restores a deleted space | No | A3 (2b) answers it on the spaces list; the editor has no delete |
| **46** — the deployment's headers must let the map's tiles load | No | Deployment, not design; the prototype's map is an illustration |
| **8**, **14** | No | Not this batch's pages |

## 7. Files

All inside `docs/design/`; workers A and B are in `apps/` and never touch it, so no licence.

- **New (3):** `prototype/Admin space add.html`, `scripts/check-parse.mjs`, `scripts/check-classes.mjs`
- **Modules (3):** `prototype/masaha/profile-a.jsx`, `profile-b.jsx`, `masaha.css`
- **Pages (4):** `Admin space edit.html`; `Owner space profile.html` (E7, forced by the shared
  editor); `Admin spaces.html` (the «إضافة مساحة» link — and the `?unlink=` line only if §13.1 says
  so); `Flows - states.html` (the two «Add space» frames' URL)
- **Archive documents (4):** `README.md`, `CHANGES.md`, `INDEX.md`, `SCREENS.md`
- **Not touched:** `admin-data.js`, `data.js`, `details-data.js` (2b's and batch 4's pages read
  them), `Admin reports.html`, `Admin owners.html`, every 2b page.

## 8. Design issues

Found while planning. **None is built unless the reply approves it.**

| | Issue | Better | Level | Recommend |
|---|---|---|---|---|
| **DI-12** | A price's custom label is one field; the contract has `labelAr` and `labelEn`, the English only with the Arabic | The label cell holds the Arabic; an English field («اختياري») follows it in the row (a card line on a phone) | prototype | fold |
| **DI-13** | Removing a shift a saved price uses is refused by the server (409), and the form gives no warning | The shift's remove button disabled with «يستخدمها سعر — غيّره أولًا» beside it (foundation §10) | prototype | fold |
| **DI-14** | Only the prices section says it is stale; Golden Hub's hours, amenities and contacts are 70 days old and their sections say nothing, while visitors see «قد تكون قديمة» | A stale group's date line carries a `warning` Badge «قديمة», its confirm beside it; the prices' paragraph becomes that badge | prototype | fold |
| **DI-15** | `TimeInput` caps the hour at 23, so a day closing at midnight (16:00–24:00, `closesMinute` 1440) cannot be entered without «24 ساعة» | «إلى» accepts 24:00 as the day's end | prototype (and a note for the web's time field) | fold |
| **DI-16** | The editor refuses a price of 0 while the contract takes 0–10,000,000 agorot | Leave as is unless the owner wants a free price shown; a note for the web | prototype | **do not fold** — ask |
| **DI-17** | `?unlink=` on Admin spaces and on Admin owners is hard-coded to Number One Hub's Yousef, so any link to it names the wrong owner | Take the space's (or the person's) first owner; A4 (2b) rewrites unlinking anyway | prototype | see §13.1 |

## 9. Lanes and what proves each behaviour

**No test lane owns `docs/design/`** (excluded from ESLint and Prettier). The proof is:

| Check | The break it catches |
|---|---|
| `check-parse.mjs` | a syntax error that blanks a page |
| `check-classes.mjs` | a new class the prebuilt CSS does not define, silently dead |
| **A scripted browser pass** (scratchpad, not committed): every page touched × 390/768/1440 × ar/en × light/dark, asserting no blank render, no console error, **no horizontal overflow** (`scrollWidth ≤ innerWidth`, AD-007's break), **each section title drawn once** and **one «إضافة مساحة» submit** (F2's class of break), chips count = sections count, F1's 20 px footer gap | blanks, runtime errors, overflow, a part drawn twice |
| **My own eyes** on every changed section at 390, 768 and 1440 | gaps, misplaced blocks, anything the assertions do not name |

Each assertion is seen failing once against a deliberately broken copy before it is trusted.

## 10. Review Focus — what no check exercises

- A screen reader on the chips' `aria-current`, the checklist's links and the photo live region;
  real keyboard focus (`:focus-visible` does not fire under scripted focus).
- The `IntersectionObserver`'s marking at a section boundary, and touch scrolling of the chips.
- Real uploads of large and wrong-type files; previews of real photos.
- The prototype's contact normaliser against `@masaha/shared`'s real rules — it approximates them
  for the helper's wording, and the web uses the shared rules, not this.
- The owner's page as a whole: batch 5 decides its own differences.

## 11. Commits

`docs(design)`, each subject ≤ 50 characters (counted). `CHANGES.md`'s line goes in the commit of
its decision; `INDEX.md`, `SCREENS.md` and the board in the commit that changes the URL.

| # | Subject (chars) | Holds |
|---|---|---|
| 1 | `docs(design): add the prototype's check scripts` (47) | E8, the README paragraph, the *Batch 2a* heading |
| 2 | `docs(design): the profile fields as the code built` (50) | AD-005/010 catch-up: `BasicsFields`, `LocationFields`, grouped area, «اختياري», two landmarks, coordinates |
| 3 | `docs(design): five fact groups and a section nav` (48) | E1, E7's inherited structure |
| 4 | `docs(design): a creation form for a new space` (45) | E2, the redirect, INDEX rows, board, SCREENS |
| 5 | `docs(design): a checklist of what is missing` (44) | E3, `?created=1` in INDEX |
| 6 | `docs(design): hours, prices and contacts` (40) | E4, `?demo=pricelimit`, approved DIs |
| 7 | `docs(design): the gallery acts at once` (38) | E6, `?fail=upload` |
| 8 | `docs(design): the verified space leads somewhere` (48) | E5 (and DI-17 if approved) |

PR title, as the prompt sets: `design: the admin's space editor`; labels `docs`, `area:docs`;
assigned to the owner; not merged.

## 12. Verification (phase 4)

No product code, so workflow phase 4's exception: **`npm run format:check`** and **`npm run
check:links`** on the head (`node_modules` exists in the worktree, so no `npm ci`). Reported, not
claimed: `.prettierignore` excludes `docs/design/` and `*.md`, so `format:check` cannot see this
item; `check:links` covers the Markdown, not the prototype's HTML. Then the two scripts, and the
browser pass of §9 on **5346**: `Admin space edit.html` (`?id=golden`, `white`, `focus`,
`new&created=1`, `?new=1`'s redirect, `?demo=shifterror`, `?demo=pricelimit`, `?fail=upload`),
`Admin space add.html`, `Owner space profile.html`, `Admin spaces.html`, at 390, 768 and 1440,
Arabic and English, light and dark.

**Before/after images:** every "before" captured first, from the clean tree, before the first
edit; pairs named after the decision (`E1-editor-768-before.png`, `…-after.png`), in
`C:\Users\basel\Downloads\design-fix-admin-editor\`, never committed. The server and Chrome are
stopped at the end and 5346 checked free; every background shell stopped.

## 13. Decisions needed from the owner

1. **E5's «فك ربط المالك» link.** `Admin spaces.html?unlink=` always names Yousef (DI-17). Allow
   one expression in `Admin spaces.html` so it takes the space's first owner (outside «إضافة
   مساحة», which the prompt limits me to) — **recommended** — or link the list without opening the
   dialog.
2. **E5's «بلاغات Focus Hub» link** goes to `Admin reports.html?space=focus`, a filter 2b adds
   (A7); until then it opens the whole list. Accept, or hold the link for 2b.
3. **S1–S10:** approve as recommended, or say which to drop (S2 especially: it is my reading of
   "the error naming the day").
4. **DI-12 … DI-16:** fold DI-12, 13, 14, 15; leave DI-16 — or your choice.
