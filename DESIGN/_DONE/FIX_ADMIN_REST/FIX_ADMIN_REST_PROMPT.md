# Design fix 2b — the rest of the admin's dashboard, in the prototype

**The design-fix worker** · worktree `C:\Users\basel\masaha-design`, detached at `origin/main`
(`068efc6`, #61 merged) · branch `design/admin-rest`, cut with `git fetch --prune origin`, then
`git switch --no-track -c design/admin-rest origin/main`. Serve the prototype on **port 5346**
(`npx serve -l 5346` from `docs/design/prototype`; its `serve.json` keeps the parameters). No
`npm ci`, no database, no `.env`.

**Model:** Opus 5.5, effort high. **Size cap:** at most 2 subagents, no workflow.
**Plan:** `C:\Users\basel\.prompt\MASAHA_DESIGN\PLAN\FIX_ADMIN_REST_PLAN.md` (`write-plan`; save, then stop).
**Report:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\FIX_ADMIN_REST_REPORT.md` (`final-report`).
**Before/after images:** `C:\Users\basel\Downloads\design-fix-admin-rest\` (not committed).
Follow the skills: `start-work-item` (you are a third worker; your folder is the one above),
`write-plan`, `open-pr`, `final-report`.

## 1. The task in brief

The second item of batch 2: every admin page but the editor (#61). Apply the rest of
`DECISIONS_ADMIN.md` to the prototype, as amended — including two decisions taken since the review:
**amenities are no filter, and a space has «مرافق إضافية» of its own** (in the shared editor), and
**the role change as the API now builds it**.

## 2. Read first

1. **The decisions:** `C:\Users\basel\.prompt\MASAHA_DESIGN\DECISIONS_ADMIN.md` — its three *Amended*
   notes first, then **Spaces, owners, users** (A3–A6, AD-021) and **Lists, overview, reports,
   lookups, audit, settings** (A7, A8, Lookups, Audit log, Settings). Apply only what is marked
   **prototype**; the editor's part (A1, A2, hours, prices, contacts, the verified page) is done.
2. **Already settled:** `DECISIONS_SHARED.md` (P1 as amended, P5–P9; SH-007), and your own
   `CHANGES.md` for what 2a built and left (the «بلاغات <space>» link waits for this item's space
   filter; `Admin owners.html?unlink=` is hard-coded).
3. **The review behind them:** `C:\Users\basel\.prompt\MASAHA_DESIGN\REPORT\REVIEW_ADMIN_REPORT.md`
   (AD-013 … AD-030).
4. **What the API now does** (the screens must not promise otherwise): `docs/features/users.md` and
   `docs/features/space-links.md` (*Behaviour*, *API decisions*); `docs/api/api-contract.md` ›
   *Owners (the admin)* and *Users (the admin)*, and §6 (the codes: `EMAIL_HAS_ACCOUNT`,
   `ALREADY_OWNER`, `ACCOUNT_IS_ADMIN`, `RECEPTION_LINK_ACTIVE`, `ACCOUNT_SUSPENDED`, `OWN_ACCOUNT`,
   `LAST_ADMIN`, `ACCOUNT_HAS_LINKS`, `GOOGLE_ONLY_ACCOUNT`, `TEMPORARY_PASSWORD_NOT_PENDING`).
   For the own amenities: `C:\Users\basel\.prompt\MASAHA_AMENITIES\PLAN\AMENITIES_PLAN.md` (approved,
   being built): `ownAmenities`, Arabic name required, English optional, at most 20, each 1–60
   characters, a repeated Arabic name refused on its field; the glossary's «مرفق إضافي».
5. `docs/design/README.md`, `CHANGES.md`, `INDEX.md`; foundation §5, §7–§10, §12; the glossary.
6. The prototype's source: the eight pages (`Admin spaces/owners/users/overview/reports/lookups/
   audit/settings.html`), `masaha/admin.jsx`, `admin-data.js`, `shared.jsx`, and the shared editor
   (`profile-a.jsx`, `profile-b.jsx`) for G1.

## 3. The settled decisions (review them in "Stronger decisions")

- **G1 — «مرافق إضافية» in the shared editor's amenities section:** the common list to tick, then the
  space's own amenities: short rows, Arabic name and English name («اختياري»), added up to 20 (the
  limit with its reason), removed, a repeated Arabic name marked on its field; saved with the section,
  dated and confirmed with it. Both editors inherit it (the owner's page too — O1). Under the admin's
  list, keep «إدارة قائمة المرافق».
- **G2 — no amenity filter:** the lookups page's amenities lose the «في الفلاتر» switch, its badge and
  its line; nothing else in the archive offers an amenity as a filter on the admin's pages (the
  Directory's filter is the public batch's — leave it).
- **G3 — A3, a space's state is two facts and a deleted space has a way back:** the verification badge
  always, «مخفية» beside it; «محذوفة» a fourth choice of the state filter, its rows muted with
  «استرجاع». (The API's `status=deleted` comes later; the prototype shows it now.)
- **G4 — A4, A5, A6, AD-021, as #60 and #62 built them:** one way to link an owner, from a space (a
  `Combobox` of one person) and from a person (one space), each saying the consequence before the act;
  unlink naming the owner, one item per owner (and `Admin owners.html?unlink=` takes the row's own
  owner and space); adding an owner says what will happen, its submit «إنشاء حساب وربط», and
  `EMAIL_HAS_ACCOUNT` leads to the upgrade («سيُرقّى حسابه»); the one-time password dialog as A5 says
  (no X, no Escape, no outside click; «تم» after «نسخ»; how it was handed over). **The role (amended):**
  «مستخدم» or «أدمن» only; on an owner's row «تغيير الدور» visible, disabled, with «دوره يتبع روابطه —
  فُكّ ربطه أولًا» and the unlink link; the admin's own row «أنت», no actions; an owner whose spaces
  are all deleted says «كل مساحاته محذوفة — استرجع المساحة لفك ربطه». **Suspension** is an
  `AlertDialog` saying its true consequence for an owner («تبقى مساحته موثّقة، ولا تُعدَّل إلا بعد فك
  ربطه»); restore at once. **The admin's temporary password** disabled with its reason for a
  Google-only account (AD-021) and a suspended one («استرجع الحساب أولًا»).
- **G5 — A7, A8 and the rest, as the file says:** Spaces, Users and Data reports become cards at 768;
  Owners and the Audit log stay tables (A7's columns); Owners gain search; Data reports gain the space
  and the field as filters (the space filter is the one the editor's «بلاغات <space>» link waits for:
  make it read `?space=`); the Audit log gains a target search; «بيانات قديمة فقط» a `ToggleGroup`
  chip by the count; the overview a work queue (A8); a report's «تعديل الحقل» carries the report to
  the editor, where «تم التصحيح» is in place; the lookups' arrows, focus and live region (AD-025/026);
  the audit log (AD-028); the settings (AD-029, **as narrowed**: data tables full width, lists managed
  row by row — the lookups, the amenities — keep a reading width).

## 4. Stay alert: new design issues

Report any new defect or better design — never silently fixed or ignored: in the plan's **"Design
issues"** (`write-plan`), or, once building, in the report's **"New design issues"**, each with the
frame, what is wrong, the better solution from the design system, and its level. Build none unless
the reply approves it.

## 4b. The owner's additions

A change **inside** a decision you apply — make it. A **new** change — say it goes to the analyst
first. List every addition in the report's **"Owner's additions"**.

## 5. Risks

- **The shared editor (G1):** `profile-a.jsx`/`profile-b.jsx` serve the admin's and the owner's pages;
  #61's fixes must hold (F1's gap, R2's shift ids, R3's day errors, the gallery's counting). Open both
  pages after each change.
- **Truth to the API:** no screen offers what the API refuses (a role for a linked person, a temporary
  password for a Google-only account, a link to an admin). Where you are unsure, read the contract.
- **Your checks' limit:** the scripts and a load matrix see blanks and errors, not layout: #59's F2
  and #61's eleven fixes were found by eyes. Look at every changed page at 390, **768** and 1440.
- **The repository:** touch nothing outside `docs/design/`.

## 6. Phase 4 and the pull request

- **Checks:** your two scripts (`docs/design/scripts/`) at every commit, `format:check`,
  `npm run check:links`. No test lanes, no build.
- **Real run:** every page you changed, at 390, 768 and 1440, Arabic and English, light and dark;
  before/after pairs in the images folder, named after the decision (`G4-users-768.png`). Servers
  stopped and the port checked free. Stop every background shell you start; `jq` is not installed —
  use `gh … --jq`.
- **The archive's documents:** a *Batch 2b* section in `docs/design/CHANGES.md`, one line per applied
  decision; `INDEX.md` for every URL or parameter you add or rename.
- **PR:** title `design: the rest of the admin's dashboard` (≤ 50), labels `docs`, `area:docs`,
  assigned to the owner; commits grouped by decision (≤ 50 characters each — count them). The analyst
  reviews it. Don't merge.
