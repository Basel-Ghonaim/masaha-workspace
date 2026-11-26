# WI-B2: the auth forms' main action, and the audit. The report

> Prompt: `11_FOLLOWUP_PROMPT.md`. Plan: `12_PLAN.md`. Resumed once after the supervisor session closed on
> 2026-11-25 (§5). **Not merged.**

## 1. The pull request

**[#159](https://github.com/Basel-Ghonaim/masaha/pull/159)**, `feat/auth-main-action` → `main`.

| | |
|---|---|
| Head | `75a1c2c4bdc78dc30523b674a52e720c3068f806` |
| CI | Green on that head (run 45776846378, `test:api` included) |
| Merge state | `CLEAN` |
| Labels | `feat`, `area:web` |
| Assignee | the owner |

14 files, all web: 7 source files and 7 test files.

## 2. The commits

On `origin/main` = `95c33fe9`:

1. `75a1c2c4`, `feat(auth): draw the forms' main action`:
   - `variant="main"` on the submit of `SignInForm`, `RegisterForm`, `ForgotPasswordForm` and `ResetPasswordForm`.
     That also covers the reset page's sign-in (#157) and the views of the sign-in over a page.
   - `ResetPasswordPage`: «Request a new link», and the signed-in «Sign in».
   - `ForgotPasswordPage` and `in-place/ForgotView`: the open link's «Set a new password».
   - The tests.

No deviation commit: the audit found nothing that clearly breaks the rule (§3). No document commit: no document points
to this follow-up (`directory.md`, foundation and `auth.md` checked), and none states anything the change alters.
`#PRNUM` was not needed.

## 3. What was run, and what was not

**Locally, on the head, through `heavy.mjs b2`:**

| Check | Result |
|---|---|
| `format:check` | pass, after a Prettier fix to 5 of my files, amended into the commit |
| `check:links` | pass, 2830 links |
| `check:conflicts` | pass |
| `check:classes` | pass, 2021 files |
| `lint` · `typecheck` | pass. Run just before the Prettier-only amend; CI ran both on the head: pass |
| `test:unit` | 1477 (web) + 924 (api) + 384 (shared) passed |
| `test:component` | 2273 passed, 1 timed out (5 s): `CorrectSheet` "sends only the changed fields…", untouched here. Alone: 6/6 passed. CI: pass |
| production build (`NODE_ENV=production`) · `check:build` | pass |

**Not run locally:** `test:api`, because nothing in the API changed. CI ran it: pass.

### The audit, by the code

**Screens** (`pages/site/routes.tsx` and `pages/dashboard/routes.tsx`): 43 `variant="main"` call sites on `main` before
this PR, plus 8 here. Each screen the §4.3 table names has exactly one main action. The rest have none: settings
cards, states, the directory, the overview pages, the lists the table does not name.

**Overlays:** 54 files hold a Dialog, AlertDialog, Sheet or AdaptiveDialog.
- **One `main` each, on the confirm:**
  - announcement sheet, report, decide, visit, check-out, collect, correct, debt, edit customer, pay, subscription,
    pre-check-in («as a visit»), price, usage-out;
  - package, `AddStaff`, reissue, `AddOwner`'s form, link owner, `EditSheet`, `HoursSheet`, issue password, temporary
    password;
  - every phone filter sheet: directory, customers, ledger, audit, admin reports, admin spaces.
- **Two call sites in one file, one per view:**
  - `AddOwner`: the page's trigger, and the sheet's submit.
  - `CustomersFilters`: the toolbar's «زبون جديد» from 768 px, and the filter sheet's «عرض…».
- **None, as the rule says:**
  - the destructive confirms (delete, end, archive, void, write-off, unlink, role, suspend, deactivate, discard, leave,
    photo remove, delete space, extension);
  - the gallery viewer, the unverified notice, the map's `SelectedSheet` (the directory leads with live status);
  - `LookupSheet` (a trigger wrapper: its forms, `AmenityForm` and `LookupForm`, hold the `main`);
  - the site menu, and the showcase.
- **`SignInPrompt`:** its forms are the auth forms above.

### The audit, in Chrome

Headless Chrome over CDP, with the API on 3320 and the web on 5320. Script: `scripts\audit.mjs`. Outputs:
`out-audit-full.json` and `out-audit-recheck.json`; the table is built by `table.mjs`.
- **Light theme.** Routes in Arabic, overlays in English.
- **Roles and widths:** as a guest, the demo owner and the admin, at 1440 and 390.
- **Coverage:** 78 route views and 26 overlay openings that write no data.
- **Dark:** five screens at both widths.
- **axe:** 0 violations on `/login`, `/register`, `/forgot-password`, `/reset-password` and the sign-in over a page,
  at both widths.
- **Refresh limiter:** each role signed in once and moved inside the app, so there were 8 refreshes and no 429.
- **Page errors and overflow:** none.

**Verdict:** every row is ok (§9).
- Where a page's `main` stays under an overlay's scrim, the overlay still holds exactly one. That is D2, accepted.
- Eight overlay triggers were not matched by the script (§5). Those overlays are covered by the code audit above.

**Shots:** `C:\Users\basel\Downloads\berry-audit-shots\`, 12 curated (the auth pages, the sign-in over a page, the desk,
the customers' filter sheet, Owners and its sheet, dark sign-in and desk). Every capture is in `raw\`.

## 4. Tests seen failing first, and breaks

Run before the change, all nine assertions failed (7 files). After it, all 218 tests in `features/auth` and
`pages/site/auth` passed.
- `SignInForm`: "draws its submit as the main action" (new).
- `RegisterForm`: "draws its submit as the main action" (new).
- `ForgotPasswordCard`: "shows the email form without a recovery" (+1 assertion).
- `ResetPasswordCard`: "shows the new password…" (+1 assertion).
- `resetPasswordPage`, three cases:
  - "links to a new link when this one can no longer be used";
  - "offers the sign-in on the card once the password is set…";
  - "keeps the link to sign in when a session is still held…".
- `forgotPasswordPage`: "links on to the new password…" («Set a new password» is `main`, «Enter your email again» is
  not).
- `inPlaceSignIn`: "draws one main action in each view" (new). It walks sign-in, register and forgot, where the link is
  open. Each view holds exactly one `main`.

No breaks beyond these: no deviation was fixed, so no deviation test exists. No test was weakened. The two existing
`toHaveAttribute` expressions were only split, to add the class assertion.

## 5. Problems met, and how each was solved

- **The session closed during audit run 2** (the supervisor's session ended). On resume:
  - Docker Desktop was down, so the API failed with Prisma `ECONNREFUSED`. I started Docker, ran `db:up`, waited for
    healthy, and restarted the API.
  - The audit was rerun once (run 3). Run 1 had used auto-found dashboard links, which missed the sidebar's pages.
    Run 3 has explicit lists of every owner and admin page.
- **The Owners page counted 0 `main`** although `AddOwner`'s trigger is `main` and is painted berry (shot
  `admin-1440-dashboard-admin-owners.png`).
  - **Cause:** the script counted `[data-slot="button"]`. Radix's `SheetTrigger asChild` replaces that slot.
  - **Fix:** the selector became every `button, a`, and I re-measured Owners and the five dark screens.
    Owners: 1 `main`. Dark: no berry, the same as run 3.
  - **Scope of the gap:** a grep shows `AddOwner` is the only `main` inside a `*Trigger asChild`.
- **`heavy.mjs` runs through `cmd`,** which reads `|` in a filter argument as a pipe. The script now also reads its
  filter from `AUDIT_ONLY`.
- **Eight overlay triggers were not matched,** so those overlays were not opened. Their labels differ in case («Edit
  Contacts», «Edit Opening hours»), or sit behind a menu (users' «Actions») or another tab (amenities). They are covered
  by the code audit. I did not spend another run on them, to save usage.
- **The first PowerShell check loop** wrote logs to paths with a colon, so four checks did not run. I reran them in
  Bash.
- **The servers** were stopped by PID afterwards (process trees), and ports 3320 and 5320 checked free.

## 6. Anything that behaved unexpectedly

- **The `CorrectSheet` timeout under the full component lane** (5 s). It passed alone, and CI passed. It may be a flaky
  test under load. Recorded, not changed.
- **The script's pattern `subscription`** matched «End subscription» on the customer's file. That opened the end
  dialog, which shows no `main`, as the destructive rule says. Escape closed it, and no data was written.
- **The ledger filter sheet's `main`** reads «No results — change the filters». That is its count label while the demo
  filters match nothing. It is still the sheet's one confirm.

## 7. Early conflict check

`gh pr list --state open`: only #159. No other pull request to check.

## 8. Departures, and points for the owner

- **For the owner, unchanged: screens the §4.3 table does not name, with no main action today.**
  - Owner: the overview, payments, finance, reports, audit.
  - Admin: the overview, reports, users, audit.
  - Site: privacy, and the account's favourites and reports.

  None is a clear break: the rule gives a main action only where a screen exists for one action. Whether any should
  get one is the owner's call.
- **Judgement taken: the open link's «Set a new password» is `main`.** I read it as "a done state's one link". Its
  outline «Enter your email again» is the alternative.
- **Judgement taken: the reset page's signed-in «Sign in» is `main`,** as the done state's one link.
- **Overlays in English and routes in Arabic,** rather than both languages each. This kept to one run, given the usage
  limit. The colours do not depend on the language; #158's pass covered both.
- **The verification ran mostly before the PR,** on the same tree: lint and typecheck ran before a formatting-only
  amend. CI then ran every check on the head.

## 9. The audit table

| Screen | Role | Width | Expected | Found (painted `main`) | Verdict |
|---|---|---|---|---|---|
| / | guest | 1440 | 1 «بحث» | بحث | ok |
| /spaces | guest | 1440 | none (directory) | 0 | ok |
| /spaces/pal-hub | guest | 1440 | 1 WhatsApp | واتساب +970599000010 | ok |
| /about | guest | 1440 | 1 «تصفّح المساحات» | تصفّح المساحات | ok |
| /privacy | guest | 1440 | none (not named) | 0 | ok |
| /login | guest | 1440 | 1 submit | تسجيل الدخول | ok |
| /register | guest | 1440 | 1 submit | إنشاء الحساب | ok |
| /forgot-password | guest | 1440 | 1 submit | أرسل رابط الاستعادة | ok |
| /reset-password | guest | 1440 | 1 (the state's link) | اطلب رابطًا جديدًا | ok |
| /no-such-page | guest | 1440 | none (state) | 0 | ok |
| / | guest | 390 | 1 «بحث» | بحث | ok |
| /spaces | guest | 390 | none (directory) | 0 | ok |
| /spaces/pal-hub | guest | 390 | 1 WhatsApp | واتساب | ok |
| /about | guest | 390 | 1 «تصفّح المساحات» | تصفّح المساحات | ok |
| /privacy | guest | 390 | none (not named) | 0 | ok |
| /login | guest | 390 | 1 submit | تسجيل الدخول | ok |
| /register | guest | 390 | 1 submit | إنشاء الحساب | ok |
| /forgot-password | guest | 390 | 1 submit | أرسل رابط الاستعادة | ok |
| /reset-password | guest | 390 | 1 (the state's link) | اطلب رابطًا جديدًا | ok |
| /no-such-page | guest | 390 | none (state) | 0 | ok |
| /dashboard/spaces/26 | owner | 1440 | none (not named) | 0 | ok |
| /dashboard/spaces/26/desk | owner | 1440 | 1 top bar / action bar; rows ink | تسجيل زيارة | ok |
| /dashboard/spaces/26/customers | owner | 1440 | 1 toolbar | زبون جديد | ok |
| /dashboard/spaces/26/payments | owner | 1440 | none (not named) | 0 | ok |
| /dashboard/spaces/26/finance | owner | 1440 | none (not named) | 0 | ok |
| /dashboard/spaces/26/packages | owner | 1440 | 1 header | باقة جديدة | ok |
| /dashboard/spaces/26/profile | owner | 1440 | none (editor page) | 0 | ok |
| /dashboard/spaces/26/announcements | owner | 1440 | 1 header | إعلان جديد | ok |
| /dashboard/spaces/26/reports | owner | 1440 | none (not named) | 0 | ok |
| /dashboard/spaces/26/staff | owner | 1440 | 1 toolbar | إضافة موظف | ok |
| /dashboard/spaces/26/audit | owner | 1440 | none (not named) | 0 | ok |
| /dashboard/spaces/26/settings | owner | 1440 | none (cards) | 0 | ok |
| /dashboard/spaces/26/customers/17 | owner | 1440 | 1 first state action | حضور ⁨آية مطر⁩ | ok |
| /me/favorites | owner | 1440 | none (state/list) | 0 | ok |
| /me/reports | owner | 1440 | none (list) | 0 | ok |
| /me/settings | owner | 1440 | none (cards) | 0 | ok |
| /dashboard/spaces/26 | owner | 390 | none (not named) | 0 | ok |
| /dashboard/spaces/26/desk | owner | 390 | 1 top bar / action bar; rows ink | تسجيل زيارة | ok |
| /dashboard/spaces/26/customers | owner | 390 | 1 toolbar | زبون جديد | ok |
| /dashboard/spaces/26/payments | owner | 390 | none (not named) | 0 | ok |
| /dashboard/spaces/26/finance | owner | 390 | none (not named) | 0 | ok |
| /dashboard/spaces/26/packages | owner | 390 | 1 header | باقة جديدة (below the fold) | ok |
| /dashboard/spaces/26/profile | owner | 390 | none (editor page) | 0 | ok |
| /dashboard/spaces/26/announcements | owner | 390 | 1 header | إعلان جديد | ok |
| /dashboard/spaces/26/reports | owner | 390 | none (not named) | 0 | ok |
| /dashboard/spaces/26/staff | owner | 390 | 1 toolbar | إضافة موظف | ok |
| /dashboard/spaces/26/audit | owner | 390 | none (not named) | 0 | ok |
| /dashboard/spaces/26/settings | owner | 390 | none (cards) | 0 | ok |
| /dashboard/spaces/26/customers/17 | owner | 390 | 1 first state action | حضور ⁨آية مطر⁩ | ok |
| /me/favorites | owner | 390 | none (state/list) | 0 | ok |
| /me/reports | owner | 390 | none (list) | 0 | ok |
| /me/settings | owner | 390 | none (cards) | 0 | ok |
| /dashboard/admin | admin | 1440 | none (not named) | 0 | ok |
| /dashboard/admin/spaces | admin | 1440 | 1 «إضافة مساحة» | إضافة مساحة | ok |
| /dashboard/admin/spaces/new | admin | 1440 | 1 submit | إضافة مساحة (below the fold) | ok |
| /dashboard/admin/owners | admin | 1440 | 1 AddOwner | إضافة مالك | ok |
| /dashboard/admin/reports | admin | 1440 | none (not named) | 0 | ok |
| /dashboard/admin/users | admin | 1440 | none (not named) | 0 | ok |
| /dashboard/admin/lookups | admin | 1440 | none (cards) | 0 | ok |
| /dashboard/admin/audit | admin | 1440 | none (not named) | 0 | ok |
| /dashboard/admin/settings | admin | 1440 | none (cards) | 0 | ok |
| /dashboard/admin/spaces/34 | admin | 1440 | none (editor page) | 0 | ok |
| /me/favorites | admin | 1440 | none (state/list) | 0 | ok |
| /me/reports | admin | 1440 | none (list) | 0 | ok |
| /me/settings | admin | 1440 | none (cards) | 0 | ok |
| /dashboard/admin | admin | 390 | none (not named) | 0 | ok |
| /dashboard/admin/spaces | admin | 390 | 1 «إضافة مساحة» | إضافة مساحة | ok |
| /dashboard/admin/spaces/new | admin | 390 | 1 submit | إضافة مساحة (below the fold) | ok |
| /dashboard/admin/owners | admin | 390 | 1 AddOwner | إضافة مالك | ok |
| /dashboard/admin/reports | admin | 390 | none (not named) | 0 | ok |
| /dashboard/admin/users | admin | 390 | none (not named) | 0 | ok |
| /dashboard/admin/lookups | admin | 390 | none (cards) | 0 | ok |
| /dashboard/admin/audit | admin | 390 | none (not named) | 0 | ok |
| /dashboard/admin/settings | admin | 390 | none (cards) | 0 | ok |
| /dashboard/admin/spaces/34 | admin | 390 | none (editor page) | 0 | ok |
| /me/favorites | admin | 390 | none (state/list) | 0 | ok |
| /me/reports | admin | 390 | none (list) | 0 | ok |
| /me/settings | admin | 390 | none (cards) | 0 | ok |

| Overlay | Role | Width | Expected | Found | Verdict |
|---|---|---|---|---|---|
| signin-prompt (Sign in to report information) | guest | 1440 | 1 confirm | Sign in · behind the scrim: WhatsApp +970599000010 | ok |
| directory-filters (Filters) | guest | 390 | 1 confirm | Show 37 results | ok |
| signin-prompt (Sign in to report information) | guest | 390 | 1 confirm | Sign in · behind the scrim: WhatsApp | ok |
| site-menu (Menu) | guest | 390 | none (navigation) | 0 · behind the scrim: WhatsApp | ok |
| desk-visit (Check in a visit) | owner | 1440 | 1 confirm | Check in · behind the scrim: Check in a visit | ok |
| customers-new (New customer) | owner | 1440 | 1 confirm | Save without payment · behind the scrim: New customer | ok |
| customer-subscription (End the subscription today?) | owner | 1440 | none (destructive: «End subscription» opened) | 0 · behind the scrim: Check in ⁨آية مطر⁩ | ok |
| customer-edit | owner | 1440 | 1 confirm | not opened (trigger «^Edit» not matched) | by code |
| staff-add (Add staff member) | owner | 1440 | 1 confirm | Create the reception account · behind the scrim: Add staff member | ok |
| announcement-new (New announcement) | owner | 1440 | 1 confirm | Publish · behind the scrim: New announcement | ok |
| package-new (New package) | owner | 1440 | 1 confirm | Save package · behind the scrim: New package | ok |
| profile-edit | owner | 1440 | 1 confirm | not opened (trigger «^Edit the contacts» not matched) | by code |
| profile-hours | owner | 1440 | 1 confirm | not opened (trigger «opening hours» not matched) | by code |
| desk-visit (Check in a visit) | owner | 390 | 1 confirm | Check in · behind the scrim: Check in a visit | ok |
| customers-new (New customer) | owner | 390 | 1 confirm | Save and receive ⁨₪25⁩ · behind the scrim: New customer | ok |
| customers-filters (Filters) | owner | 390 | 1 confirm | Show 27 customers · behind the scrim: New customer | ok |
| customer-subscription (End the subscription today?) | owner | 390 | none (destructive: «End subscription» opened) | 0 · behind the scrim: Check in ⁨آية مطر⁩ | ok |
| customer-edit | owner | 390 | 1 confirm | not opened (trigger «^Edit» not matched) | by code |
| staff-add (Add staff member) | owner | 390 | 1 confirm | Create the reception account · behind the scrim: Add staff member | ok |
| announcement-new (New announcement) | owner | 390 | 1 confirm | Publish · behind the scrim: New announcement | ok |
| package-new (New package) | owner | 390 | 1 confirm | Save package · behind the scrim: New package | ok |
| profile-edit | owner | 390 | 1 confirm | not opened (trigger «^Edit the contacts» not matched) | by code |
| profile-hours | owner | 390 | 1 confirm | not opened (trigger «opening hours» not matched) | by code |
| ledger-filters (Filters) | owner | 390 | 1 confirm | No results — change the filters | ok |
| audit-filters (Filters) | owner | 390 | 1 confirm | Show 274 results | ok |
| space-link-owner (Link an owner to Al-Salam Hub) | admin | 1440 | 1 confirm | Link | ok |
| owners-add (Add owner) | admin | 1440 | 1 confirm | Create account and link · behind the scrim: Add owner | ok |
| users-temporary | admin | 1440 | 1 confirm | not opened (trigger «temporary password» not matched) | by code |
| lookups-amenity | admin | 1440 | 1 confirm | not opened (trigger «^Add amenity» not matched) | by code |
| lookups-governorate (Add governorate) | admin | 1440 | 1 confirm | Save | ok |
| spaces-filters (Filters) | admin | 390 | 1 confirm | Show 37 results · behind the scrim: Add space | ok |
| space-link-owner (Link an owner to Al-Salam Hub) | admin | 390 | 1 confirm | Link | ok |
| owners-add (Add owner) | admin | 390 | 1 confirm | Create account and link · behind the scrim: Add owner | ok |
| users-temporary | admin | 390 | 1 confirm | not opened (trigger «temporary password» not matched) | by code |
| lookups-amenity | admin | 390 | 1 confirm | not opened (trigger «^Add amenity» not matched) | by code |
| lookups-governorate (Add governorate) | admin | 390 | 1 confirm | Save | ok |
| reports-filters (Filters) | admin | 390 | 1 confirm | Show 18 reports | ok |
| audit-filters (Filters) | admin | 390 | 1 confirm | Show 88 results | ok |

| Dark screen | Role | Width | Expected | Found | Verdict |
|---|---|---|---|---|---|
| / | guest | 1440 | no berry | berry 0, main-slot 1 (rgb(247, 251, 255)) | ok |
| /spaces/pal-hub | guest | 1440 | no berry | berry 0, main-slot 1 (rgb(247, 251, 255)) | ok |
| /login | guest | 1440 | no berry | berry 0, main-slot 1 (rgb(247, 251, 255)) | ok |
| /dashboard/spaces/26/desk | owner | 1440 | no berry | berry 0, main-slot 1 (rgb(247, 251, 255)) | ok |
| /dashboard/admin/spaces | admin | 1440 | no berry | berry 0, main-slot 1 (rgb(247, 251, 255)) | ok |
| / | guest | 390 | no berry | berry 0, main-slot 1 (rgb(247, 251, 255)) | ok |
| /spaces/pal-hub | guest | 390 | no berry | berry 0, main-slot 1 (rgb(247, 251, 255)) | ok |
| /login | guest | 390 | no berry | berry 0, main-slot 1 (rgb(247, 251, 255)) | ok |
| /dashboard/spaces/26/desk | owner | 390 | no berry | berry 0, main-slot 1 (rgb(247, 251, 255)) | ok |
| /dashboard/admin/spaces | admin | 390 | no berry | berry 0, main-slot 1 (rgb(247, 251, 255)) | ok |
