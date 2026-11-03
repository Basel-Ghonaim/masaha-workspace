## Summary

The rest of PAYMENTS_STEP10's approved plan, built by worker A's lead with three sub-agents in parallel and joined
into one PR: the former **PR 2** (announcements, screen 18, with the closure extension), **PR 3** (the owner's and the
admin's data reports, screens 23 and 28, and finding 8's `FilterTag`), **PR 4a** (the report of wrong information and
«بلاغاتي», screen 11) and **PR 4b** (the favourite heart, «المفضّلة», screen 10, and the space page's announcements), on
a foundation that resolves findings **169** and **173**. Web and documents only: no `apps/api`, `packages/shared`,
schema, seed, dependency or `errors.ts` change.

**Decisions taken without the owner:** none SERIOUS; listed at the end, every one in the report with its undo.

## Lane 0 — the foundation (findings 169, 173)

- `perf(design-system): serve the calendar on its own` — `Calendar` and `DatePicker` move to an entry of their own,
  `@shared/design-system/calendar` (lint allows it as it allows the data entry); react-day-picker and date-fns are a
  `calendar` chunk that `check:build` refuses in the site's first download. **Finding 169 resolved:** the first
  download 1,140,210 → 1,064,781 bytes on that commit (1,094,709 on the head, all screens in).
- `fix(design-system): start a range on each click` — the range `Calendar` sets `resetOnSelect` (a caller may still):
  the first click leaves `to` empty. **Finding 173 resolved.**
- `test(web): pre-bundle the calendar for jsdom` — react-day-picker's first import cost a test file ≈ 3.3 s in the
  component lane (date-fns read module by module), so a page drawing the calendar, loaded cold, missed its waits (the
  routes test's 403 on the owner's payments missed locally on `main` since #127; the space page's tests once it set
  the announcements). Vitest's dependency optimizer pre-bundles it for that lane only: ≈ 8 ms. The build is untouched.

## PR 2 — announcements (screen 18)

- [x] `/dashboard/spaces/:id/announcements` (owner and reception): the tabs «نشطة», «مجدولة», «منتهية» with the
  summary's counts, the tab and the page in the address; each card its type (a `warning` badge for an outage or a
  closure), its period on Gaza's clock, its text in the interface's language (the Arabic, marked, when no English); no
  status badge. — tests 25–30, 44; the real run's shots for both roles.
- [x] «إعلان جديد» / «تعديل» open the sheet (type and hint, Arabic text, English text, «يبدأ: الآن · في موعد», «ينتهي: في
  موعد · بلا موعد», date and time on Gaza's clock, a closure's line, the preview); one `Idempotency-Key` per opening,
  kept across a retry and a double press; the server's period refusals on their fields; `CLOSURE_EXTENDED` worded. —
  tests 31–35; **the real run's offline post: three failed sends and the success, one key, one announcement.**
- [x] «إنهاء الآن» with «تراجع» (not for an extended closure), «ابدأ الآن», «حذف…» naming the announcement and its true
  consequence; each sent once with no key; each toast names its tab. — tests 36–39; the real run.
- [x] The owner's «تمديد الاشتراكات» on a started closure: the preview's days, the count, the days typed (1–365), one key
  per opening, a failure kept in the dialog, `CLOSURE_ALREADY_EXTENDED`, none covered → no extension; reception's
  line; an extended closure's line. **#128 adapted:** the count is the server's — those the closure covered and their
  renewals not started («يشمل التمديد {n} اشتراكات.» and its line). — tests 40–43; **the real run applied 1 day: the
  preview said 4, 4 moved.**
- [x] Loading, failure with its reference and retry, empty per tab. — test 29.

## PR 3 — data reports (screens 23, 28)

- [x] `FilterTag` in the layer (display), its showcase, foundation §12; **finding 8 resolved.** — test 45; 44 px on
  touch in the real run.
- [x] `/dashboard/spaces/:id/reports` (owner): 20 a page, «الكل · جديدة · تمت المراجعة» in the address; the field, the
  report, the day (no time), the status; the reporter always «زائر»; the decision sheet («تعديل الحقل», the reply,
  «تم التصحيح» / «لم يُعتمد» with the reply required and focused); sent once; `REPORT_ALREADY_DECIDED`, 403, 404 worded;
  a decided report read-only. — tests 46–53, 58; the real run.
- [x] `/dashboard/admin/reports` (admin): status chips, a searched space combobox, the field, all in the address and
  in force as removable tags with «مسح الفلاتر»; the reporter named; «يعالجه»; cards until 1024 px; an unverified
  space's report decided, a verified one read-only with a link to the space. — tests 54–58; the real run. Finding
  167 recorded (no handled-by filter).

## PR 4a — the report and «بلاغاتي» (screen 11)

- [x] A space's page: «الإبلاغ عن معلومة غير صحيحة» at the end of its sections opens the dialog (the field, details
  required for «أخرى» only, U10's line by verification); a refusal keeps the input (429 counted down); the toast says
  where the reply lands with «عرض بلاغاتي»; a repeat says one is open. — tests 59, 65–69; the real run (201, then
  200).
- [x] `/me/reports`: 20 a page, the chips, the space (a link while listed, else its name with C7's line), the field
  and the day, the status, the message (a toggle when long), the reply by who replied; the account's layout and
  navigation; the account menu's links on the site. — tests 60–64. Finding 168 recorded (a guest's intent and a
  password recovery).

## PR 4b — favourites and the space page's announcements (screen 10)

- [x] The heart on the Directory's and Home's cards and beside the page's name: pressed at once, «تراجع» naming the
  space; a failure puts it back with «إعادة المحاولة»; `FAVORITES_LIMIT_REACHED` worded; a guest gets the sign-in
  dialog with the reason and the action runs on the return. — tests 71–79; the real run (each, with the guest's).
- [x] `/me/favorites`: the cards newest first or nearest first with «الأقرب إليّ»; the spaces that left with «إزالة» and
  «تراجع». — tests 80, 81; the real run (near me; a removal with «تراجع»).
- [x] A space's page shows its running closure's notice at the top and its other announcements after the status (U8);
  **finding 131 resolved.** — tests 82–84; the real run (the notice at every width).
- [x] `check:build`: no favourites', reports' or announcements' dashboard code in the site's first download.

## The lanes and how they were joined

Three sub-agents, each in its own worktree and branch from Lane 0's head, each test red before its code and each
§10 break seen red and restored from a copy, then lint, typecheck and both full web lanes on its branch (heavy runs
granted by the lead: two at once at most, ≥ 4 GB free). Lane A (announcements) fast-forwarded; lane B (data reports)
rebased, its conflicts in the routes test's imports and architecture §2 kept both sides; lane C (the user's side)
built on lane B's commit 2 and rebased, its conflicts in the data-reports repository, keys, entry, copy, fixture and
documents kept both sides (the admin's, then the user's) — checked by a script that every changed file was one both
lanes touched. The space page's announcements (the last commit) were built by the lead on the joined branch.

## Evidence — run locally on the head

- `npm run build -w @masaha/shared` · `npm run lint` · `npm run typecheck` — exit 0.
- `npm run test:unit` — shared 25 files / 263 tests, api 71 / 879, web 157 / 1071, all passed.
- `npm run test:component` — 300 files, all passed but finding 87's family's timing misses, each green alone (named
  in the report).
- `npm run test:api` — 97 files / 1246 tests passed.
- `NODE_ENV=production npm run build` · `npm run check:build` — "No dashboard code in the site's first download.",
  "No data-table or leaflet or calendar, nor Leaflet's stylesheet, in the site's first download."
- `check:classes`, `check:links`, `check:conflicts`, `format:check` — passed.
- **The first download:** `origin/main` 1,140,210 → head 1,094,709 bytes.
- **Check 5.k:** the space page's chunk reaches `data-table` and `calendar`, «بلاغاتي»'s `data-table`, through the
  features' one entry — not the first download: **finding 180** recorded.
- **The real run** (`masaha_dev`, headless Chrome, both roles' and the admin's screens, the guest, Arabic light and
  English dark at 390 / 768 / 1440): every write named in the report with its network line (method, URL, status,
  `Idempotency-Key`), the width breaks (the sheet's date and time, the favourites' grid) and 44 px touch targets.
  It found one defect, fixed here: a guest's favourite saved on their return showed unpressed until the next read (the
  hearts' first read joined the save's invalidation); the fix and its test are in `feat(favorites): save a space
  from its card`.

## Findings

Resolved: **8**, **131**, **169**, **173**. Recorded: **167**, **168** (the plan's), **180** (check 5.k).

## Decisions taken without the owner

None SERIOUS. Each with its options, choice and undo in the lead's report and the lanes' (`L0`, `LA-D1…15`,
`LB-D1…17`, `LC-D1…21`, `LEAD-D1…12`); the larger ones: the extension's count worded for #128 (LA-D1); the lanes' seams
and the cross-lane order (LEAD-D1, D2); the heavy runs' grant by a script (LEAD-D5); the public pieces' split
`ClosureAlert` / `ClosureNotice` (LEAD-D8); the calendar pre-bundled for the component lane (LEAD-D11); the favourite's
refetch fix (LEAD-D12).

## Left out

Nothing.


## Review fixes (2026-10-28/29)

Every finding of the three Claude reviews fixed (the owner's decision: nothing carried), each folded into the commit that made the code, each code fix with a test seen red before it and a break that turns it red again:

- **R1-F1 (blocker)** — an edit never sends a start or an end the user did not change: compared at the Gaza date and minute the sheet shows, not to the millisecond (a start posted «الآن» keeps its seconds on the server). → `feat(announcements): post and edit an announcement`.
- **R1-F2** — a 409 or a 404 stays in the extension's or the delete's dialog: the list holds the opened dialog (as it holds the sheet), so a refetch that changes the card no longer unmounts it; on close the focus goes to the opener, else the card's first action, else the next card or the tab. → `…end, start or delete one`, `…extend after a closure`.
- **R1-F3** — finding 169's resolution names the announcement sheet's period among the calendar's importers. **R1-F4** — the sheet's calendar marks Gaza's today. → `…post and edit an announcement`.
- **R1 (outside its range)** — `announcements.md`'s *Web history* line starts "#129 —". → `…show a space's announcements`.
- **R2-F1** — `data-reports.md`'s *Open findings* lists 167. → `…list every space's reports`.
- **R2-F2** — after `REPORT_ALREADY_DECIDED` the sheet shows the decision, read from page 1 of «الكل» of the same scope, and never a stale «جديد» («تمت المراجعة» until it is read); the owner's and the admin's. → `…decide a space's reports`, `…list every space's reports`.
- **R2-F3** — the focus after a filter tag or «مسح الفلاتر» leaves: the next tag's button, else «مسح الفلاتر», else the count. → `…list every space's reports`.
- **R2-F4** — recorded as **finding 184** («تعديل الحقل»'s anchor may not scroll on arrival; plausible, not run in a browser). → `…list every space's reports`.
- **R3-F1** — **the owner's decision on DI-58, option (a):** «إزالة» of a space that left offers no «تراجع» (the API answers 404 to a re-save) and says it cannot be saved again while out of the directory; **finding 187** recorded (an undo would need the API to allow it). → `feat(favorites): list a user's favourite spaces`.
- **R3-F2** — a guest's held favourite and report expire: after 15 minutes, or when the guest lands on another page of the site (the shell reports each page through `@shared/routing`, so it imports no feature). Memory only, as S14. → `feat(data-reports): report wrong information`, `feat(favorites): save a space from its card`.
- **R3-F3** — the heart keeps one name, «حفظ {name} في المفضّلة», with `aria-pressed` (a departure from §9's two names). → `…save a space from its card`.
- **R3-F4** — `overview.md` names the report from a space's page. → `…report wrong information`.

Verified locally on `819e1eea`: lint, typecheck, `test:unit -w @masaha/web` (157 files, 1075 tests), `test:component -w @masaha/web` (300 files, 1744 tests), `check:links`, `check:classes`, `check:conflicts`, `format:check`. No API or shared change in this round; CI ran every lane green on `819e1eea`, `CLEAN`.
