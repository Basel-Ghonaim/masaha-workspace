# OWNER_SETUP — PR 3 report (`feat/owner-staff-settings`, Staff and Settings)

Executor: Claude Code (Opus 5.5), 2026-10-20. Written as the work goes.

## 1. First checks (plan §13, "First checks, PR 2" = this PR)

1. `gh pr view 98 --json state` → `MERGED` (merge commit `cf3190a4`). `git switch main`; `git pull --ff-only` →
   `Already up to date.`; `git status --short` empty.
2. Base diff `git diff --name-status 8c429ff4 origin/main` → **empty** (only #98's merge). No code file of this PR
   changed; `packages/shared` unchanged since #98 (its `dist` present).
3. Open PRs: `gh pr list --state open` → `[]` (DESK has no open PR).
4. Check 5 — `useServerForm` (`shared/forms/hooks/useServerForm.ts`) passes `failureTitle` to `useFormFailure`
   in its body, on every render. Holds.
5. `packages/shared` read against §9: `space-settings` (`updateSpaceSettingsSchema` `.partial().superRefine(roundingPair)`,
   `MAX_STAY_MINUTES` 60–1380 step 60, `ROUNDING_MINUTES` 1–59, `VISIT_ROUNDINGS`, `SpaceSettings`'s eight fields,
   `REMINDER_PLACEHOLDERS`, `REMINDER_AMOUNT`, `placeholdersIn`, `reminderTemplateSchema` — `invalid_choice` for an
   unknown placeholder, `invalid_format` without the amount); `occupancy` (`setCapacitySchema` 1–`CAPACITY_MAX` 1000
   or `null`, `SpaceCapacity`); `space-links` staff (`addStaffSchema`, `setStaffActiveSchema`, `AddedStaff`,
   `StaffMember`); `users`' `IssuedTemporaryPassword`. As §9. The contract's staff, settings and capacity routes as §9.
6. Finding numbers: 101 is the last (#98's); **102** is the carried one, any further from **103**.
7. Branch: `git switch --no-track -c feat/owner-staff-settings origin/main`.

## 2. Commits

### Carried from #98 — commit A `25e8efd3` `fix(packages): word a row's refusal as the owner's` (50)
Items 1, 4, 6, 7 (review 8: fixed, not a finding), 8 (finding 102), 9 of `0_CARRIED_FROM_98.md`.
- `RefusalText` takes optional `lines` (passed to `useRefusalView`; `FailureLines` exported from `shared/forms`);
  `toastRowFailed(title, refusal, lines)`, `useRowWrite` passes `copy.packages.refusals`.
- `useLinkEnded` (new, `features/packages/hooks/`): a 404 invalidates `['me']`; used by `useRowWrite`'s and
  `useSavePackage`'s `onError` and, by an effect, the list's read in `usePackagesSection`.
- A new package's 404 → `packages.spaceGone` «لم تعد هذه المساحة متاحة لك.» (both catalogues).
- The held shift while `shifts` is `null` (or the shift unknown) → `packages.heldShiftUnnamed` (both catalogues).
- Review 4: `usePackageSheet` puts the shift back to `''` when `shifts` no longer holds the chosen one.
- Docs: `packages.md` *Behaviour*, two *Web decisions*, code map, open findings, *Web history*; `architecture.md` §7;
  finding **102** (Open) and its index line.
- **Red first** (the five new or extended tests, before the code): `npx vitest run --project component
  src/features/packages/hooks` → `Tests  5 failed | 9 passed (14)` — `Unable to find an element with the text: This
  package no longer exists, or the space is no longer open to you.`; `expected 'Paused, but still holds the shift
  “”;…' to be 'Paused, but still holds a shift; the …'`; `expected false to be true` (the list's 404 and `['me']`);
  `expected { name: 'Monthly', …(9) } to match object { shiftId: null }`; `expected { kind: 'refused', …(3) } to
  match object { Object (message) }`.
- **Green:** `npx vitest run --project component src/features/packages` → `Test Files  3 passed (3)` / `Tests  17
  passed (17)`.
- **Breaks** (each restored from its backup): lines dropped from the toast → `Tests  1 failed | 6 passed (7)`;
  `useLinkEnded` never matching → `Tests  3 failed | 11 passed (14)`; the held line with an empty name → `Tests  1
  failed | 6 passed (7)`; a new package's 404 as a package's → `Tests  1 failed | 6 passed (7)`; the shift not put
  back → `Tests  1 failed | 6 passed (7)`; `duration: Infinity` dropped → first **stayed green** (`Tests  7 passed
  (7)`): my own test's defect — fake timers switched on after the toast's real timer had started; the test now
  asserts the toast's option (`duration: Infinity`, as the review offered) → the break `Tests  1 failed | 6 passed
  (7)`; restored.
- `npm run lint` → exit 0; `npm run typecheck` → exit 0; Prettier on the changed files → `All matched files use
  Prettier code style!`.

### Carried from #98 — commit B `131f44e8` `fix(spaces): drop a refused retired amenity` (43)
Item 2. The API names the refused amenity by its place in the request (`amenityIds.<i>`, `amenities.service.ts`), so
`useAmenitiesSection` takes exactly those ids out of the form's value on that 422 (`setValue`, dirty), and the line
says so: «أزلنا من اختيارك مرفقًا لم يعد متاحًا؛ احفظ مرة أخرى.» / "We took an amenity no longer offered out of your
choice; save again." (the review's Arabic; the English mine — **for the owner's approval in the PR description**).
Docs: `spaces.md` *Behaviour*, the #74 decision's line, *Web history*; `lookups.md` *Behaviour*.
- A first commit subject was 54 characters: amended before anything else (`335fcd69` → `131f44e8`).
- Red: `Tests  3 failed | 8 passed (11)` — `expected [ 2, 5 ] to deeply equal [ 2 ]` and the two line assertions.
- Green: `npx vitest run --project component src/features/spaces/hooks/amenities` → `Tests  11 passed (11)`.
- Break (the value kept) → `Tests  1 failed | 10 passed (11)`; restored.

### Carried from #98 — commit C `74cd2971` `fix(spaces): name the prices card one way` (41)
Items 3 and 5. `hooks/editor/sectionName.ts` (`sectionName(place, group, copy)`: the owner's prices
`publishedTitle`, else the group's) used by `useSectionFrame` (title, confirm failure), `useSaveGroup`,
`useConfirmGroup`, `useSpacePricesEditor` (leave guard); `usePricesSection` no longer overrides the title.
`spaces.md`: "not built yet" → "where the owner edits and confirms them"; code map `useSpaceShifts`, `sectionName`;
O6's line and *Web history*.
- Red: a stub of the old behaviour → unit `expected 'Prices' to be 'Published prices'`, `Tests  1 failed (1)`; the
  toast test → `Unable to find an element with the text: Published prices saved`, `Tests  1 failed | 2 passed (3)`.
  (A first unit run with the code already written passed — not counted as red; redone with the stub.)
- Green: `npx vitest run --project unit src/features/spaces` → `Tests  87 passed (87)`; component
  `src/features/spaces` → `Test Files  23 passed (23)` / `Tests  228 passed (228)`.
- Breaks: the save toast by group → `Tests  1 failed | 2 passed (3)`; `sectionName` ignoring the place → `Tests  1
  failed (1)`; restored.
- `npm run lint` → 0; `npm run typecheck` → 0; Prettier → `All matched files use Prettier code style!`.

### Plan commit 1 — `bc38a5b4` `feat(users): record a handover at a space` (41)
A3 (replaces S4): `TemporaryPasswordDialogInput.recordHandover: RecordHandover` (required; `types/RecordHandover.ts`:
`({ userId, channel }) => Promise<unknown>`); `useHandover(recordHandover)` is the mutation (`gcTime: 0`) over it; the
outcome lines unchanged («لم تُسجَّل طريقة التسليم» on `TEMPORARY_PASSWORD_NOT_PENDING` or 404). `users` exports
`recordAdminHandover` (`repository/adminHandover.ts`, the repository's `/admin/users/:id/temporary-password/handover`)
and the `RecordHandover` type; `OwnersPage` and `IssuePasswordDialog` pass it. Design issue 15:
`users.passwordChange.description` «هذه كلمة مرور مؤقتة. اختر كلمة مرورك لتتابع.» / "This is a temporary password.
Choose your own password to continue." Docs: `users.md` *Behaviour* (the forced change's line; the handover's write),
two *Web decisions*, code map, *Web history*.
- Test 22 (`useTemporaryPasswordDialog.component.test.tsx`, "records the handover through the write its caller
  gives"): red before the code → `AssertionError: expected "vi.fn()" to be called once with arguments: [ { userId:
  12, channel: 'WHATSAPP' } ]`, `Tests  1 failed | 7 passed (8)`. With the code it stayed red the same way: React
  Query passes `mutationFn` a second argument (its context), so the caller's write got two — `mutationFn` now
  passes the request alone. Green: `npx vitest run --project component src/features/users src/pages/dashboard/admin`
  → `Test Files  17 passed (17)` / `Tests  83 passed (83)`; unit `src/features/users src/shared/copy` → `Tests  38
  passed (38)`.
- Break (the dialog ignores the caller's write, using the admin's) → `Tests  1 failed | 7 passed (8)`; restored.
- Test 21 moves to `staffRepository.unit.test.ts` (commit 2), as the approval note says.
- `npm run lint` → 0; `npm run typecheck` → 0; Prettier → clean (after `--write` on the new type); `npm run
  check:links` → `2448 links in 188 documents and 1462 source files all resolve.`

### Plan commit 2 — `8d9e147a` `feat(staff): add the owner's staff page` (39)
Built `features/staff` (dashboard-only, already in `DASHBOARD_ONLY_CAPABILITIES`): `StaffRepository` (list, add,
setActive, reissue, **handOver** — A3), keys `['space', id, 'staff']`, `useStaffQuery`, `useStaffList`, `badgesOf`,
`useAddStaff` (`gcTime: 0`, `onSuccess` returns the list's invalidation), `useAddStaffForm`, `useShownPassword`,
`StaffList` (DataTable, cards below `md`), `AddStaff` (end sheet); `StaffPage` (the role line, the list, `users`'
`TemporaryPasswordDialog`); `SPACE_PAGES.staff`; copy `staff` ×2 (with the approval note's add refusal and the zero
«لا يوجد موظفون»). Docs: `space-links.md` (header *Authority* and *Scope*, *What it does*, *Who uses it*, a *Behaviour*
paragraph «The owner's staff on the web», five *Web decisions*, code map *Web (staff)*, *Web history*);
`architecture.md` *Built so far*; `overview.md` *Built*; `docs/README.md` (space-links' line).
- **Departures (shape, within the plan's lines):**
  - The page's slot takes one object, `ShownPassword` = `TemporaryPasswordDialogInput & { returnFocus }` exactly
    (`person`, `password`, `kind`, `recordHandover`, `onDone`, `returnFocus`), so the page draws
    `<TemporaryPasswordDialog {...shown} />` and staff's handover write reaches the dialog without the page
    touching a repository; `useShownPassword` (extra file) holds it and builds the write.
  - Commit 2's table has the name and status columns; the actions column comes with the actions (commit 3).
  - «إضافة موظف» sits in the toolbar only while people are listed; the empty state carries it otherwise (one button
    of that name on the page at a time). The focus returns to the toolbar's, which exists once the list has arrived.
  - `fieldErrors.name.too_short` added (an empty name is `too_short` under `textSchema(1, …)`, as #98 found).
  - The add's `not_found` worded too, «لم تعد هذه المساحة متاحة لك.» (the space's route).
  - **Finding 90 is resolved in commit 3**, not here: this commit words only `EMAIL_HAS_ACCOUNT`; the other three
    codes come with the row's actions.
  - Test 22's file stayed `users`'; test 21 is `staffRepository.unit.test.ts`'s second test.
- Tests (new code, written with it; red shown by each break): 21 + 23 `staffRepository.unit.test.ts` (2), 24
  `staffBadges.unit.test.ts` (1) → `Tests  3 passed (3)`; 25 `useStaffList.component.test.tsx` (3), 26
  `useAddStaffForm.component.test.tsx` (4), 40's staff part (`routes.component.test.tsx`, 2) → `Tests  9 passed | 42
  skipped (51)`.
- Breaks, each red, each restored: 21 the admin's path → `Tests  1 failed | 1 passed (2)`; 23 `setActive` as `PUT` →
  `Tests  1 failed | 1 passed (2)`; 24 the expiry's comparison reversed → `Tests  1 failed (1)`; 25 the pending badge
  dropped → `Tests  1 failed | 2 passed (3)`; 26 the notice dropped → `Tests  1 failed | 3 passed (4)`; 26 the email
  worded by the generic lines (no `not_unique`) → `Tests  1 failed | 3 passed (4)`; 40 `staff` with `BOTH` → `Tests  1
  failed | 1 passed | 42 skipped (44)`.
- Checks: `npm run lint` → 0; `npm run typecheck` → 0; Prettier → clean (after `--write`); `npm run check:links` →
  `2455 links in 188 documents and 1482 source files all resolve.`; `npm run check:classes` → `No physical direction
  or arbitrary-value classes in 1006 files.`; component `src/features/staff src/features/users` → `Tests  80 passed
  (80)`; unit `src/features/staff src/shared/copy` → `Tests  36 passed (36)`.

### Plan commit 3 — `96546c27` `feat(staff): deactivate, reactivate and reissue` (47)
Built: `useSetStaffActive` (PATCH, the answer replaces the row by `setQueryData`), `useDeactivateDialog`,
`useReissue` (`gcTime: 0`, the list read again for the new expiry), `useReissueDialog`, `useStaffActions`,
`useMenuTriggers`; `StaffActionsMenu`, `DeactivateDialog`, `ReissueDialog`, `accessToasts`; the list's actions
column, its card's menu, and the dialogs held by `StaffList` above the rows (as the admin's users page holds its);
the re-issued password goes to the same slot (`kind: 'issued'`, the focus back to the row's menu). Copy `staff.menu`,
`deactivate`, `reactivate`, `reissue`, `refusals` ×2 (the approval note's 404 and 403 lines). Docs: `space-links.md`
*What it does*, *Behaviour* (the menu, the three actions, the refusals), three *Web decisions*, code map, *Web
history*; finding **90 → Resolved** (its resolution line names `staff`'s copy), moved in the index; `overview.md`.
- **Departures:** the menu puts the destructive «إيقاف وصوله» last, after a separator (the users page's menu order);
  the busy menu button keeps `aria-disabled`/`aria-busy` and stays closed (the layer's `loading` would disable it,
  leaving the focus order); `useMenuTriggers` is a copy of `pages/dashboard/admin/useRowTriggers` (a feature may not
  import a page's hook) — a second instance, noted for the review; `types/StaffDialog.ts`, `hooks/menu/`,
  `components/access/accessToasts.tsx` are extra files.
- Tests (new code, written with it): 27 `useDeactivateDialog.component.test.tsx` (3, rendering the dialog), 28
  `useStaffActions.component.test.tsx` (5), 29 `useReissueDialog.component.test.tsx` (2 + 4 cases), 30
  `StaffList.component.test.tsx` (2, axe clean) → `Test Files  6 passed (6)` / `Tests  23 passed (23)` (the staff
  folder). My own test defects fixed first: literal isolate marks written by the file tool (rewritten as escapes),
  the titles' isolates, the table's placeholder rows, the cache's collection awaited, `<main>` for axe's landmark.
- Breaks, each red, each restored: 27 closed on confirm → `Tests  3 failed (3)`; 27 the sessions line dropped →
  `Tests  1 failed | 2 passed (3)`; 28 the re-issue offered when settled → `Tests  1 failed | 4 passed (5)`; 29 the
  refetch dropped → `Tests  2 failed | 4 passed (6)`; 30 the menu unnamed → `Tests  1 failed | 1 passed (2)`.
- Checks: lint → 0; typecheck → 0 (after typing the test's items); Prettier → clean; `check:links` → `2455 links in 188
  documents and 1497 source files all resolve.`; `check:classes` → `No physical direction or arbitrary-value classes
  in 1021 files.`

### Plan commit 4 — `e1eafcee` `feat(space-settings): add the owner's settings` (46)
Built `features/space-settings` (dashboard-only, already listed): `SpaceSettingsRepository` (get, update — PATCH), keys
`['space', id, 'space-settings']`, `useSpaceSettingsQuery`, `useSaveSettings` (`onSuccess` sets the answer and toasts
«حُفظت إعدادات «{card}»»), `useSettingsCard` (+ `changesOf`: only what changed, a group sent whole), `usePricingCard`,
`useReceptionCard`, `useSpaceSettingsCards`, `roundingExample`; `SettingsCard`, `SpaceSettingsCards`, `PricingCard`,
`ReceptionCard`; `SettingsPage` (`max-w-3xl` column); `SPACE_PAGES.settings`; copy `spaceSettings` ×2. Docs:
`space-settings.md` (header, *What it does*, *Who uses it*, *How it composes*, *Behaviour* «The owner's settings on the
web», five *Web decisions*, code map *Web*, *Web history*); `architecture.md` (*Built so far*, the status line's
`shared/lib`); `overview.md`; `docs/README.md` (the line drops "(API only)").
- **Departures:** `shared/lib/numbers/wholeNumber.ts` (`wholeNumberOf`, with a unit test) — the minutes, and in
  commit 5 the attendance card's capacity and hours, read Arabic-Indic digits; the page's attendance schema cannot
  import a feature's helper, so it is `shared/lib`'s (packages' `countOf` and the other local copies are left as they
  are — no drive-by refactor). `SpaceSettingsCards` takes `spaceName` in commit 6, where it is used. Extra files:
  `types/SettingsCardView.ts`, `hooks/useSpaceSettingsCards.ts`. `useSettingsCard` sets a failure aside on discard, as
  the editor's frame does. `minutes.fieldErrors.invalid_format` worded as `out_of_range` (a non-whole number).
- Tests (new code, written with it): 31 settings' part (`spaceSettingsRepository.unit.test.ts`, 1), 32
  `roundingExample.unit.test.ts` (1), `wholeNumber.unit.test.ts` (1) → unit `Tests  8 passed (8)` (with the staff
  ones); 33 `usePricingCard.component.test.tsx` (4), 34 `useReceptionCard.component.test.tsx` (1), 39
  `SpaceSettingsCards.component.test.tsx` (2, axe clean), 40's settings part (2) → `Tests  9 passed | 44 skipped (53)`.
- Breaks, each red, each restored: 31 the edit as `PUT` → `Tests  1 failed (1)`; 32 `n − 1` → `n` → `Tests  1 failed
  (1)`; 33 the rule sent alone (no group) → `Tests  1 failed | 3 passed (4)`; 34 no toast → `Tests  1 failed (1)`; 39
  the unsaved badge dropped → `Tests  1 failed | 1 passed (2)`; 40 `settings` with `BOTH` → `Tests  1 failed | 1 passed
  | 44 skipped (46)`; `wholeNumberOf` not reading Arabic digits → `Tests  1 failed | 5 passed (6)`.
- Checks: lint → 0; typecheck → 0; Prettier → clean; `check:links` → `2459 links in 188 documents and 1522 source files
  all resolve.`; `check:classes` → `No physical direction or arbitrary-value classes in 1046 files.`; component
  `src/features/space-settings` → `Tests  7 passed (7)`; unit `src/features/space-settings src/shared` → `Tests  458
  passed (458)`.

### Plan commit 5 — `474b3add` `feat(space-settings): save the attendance card` (46)
Built `features/occupancy` (new web feature, not dashboard-only): `OccupancyRepository` (getCapacity, setCapacity —
PUT), keys `['space', id, 'occupancy', 'capacity']`, `useCapacityQuery`, `useSetCapacity`; `space-settings` exports
`SettingsCard`, `SettingsCardView`, `useSpaceSettingsQuery`, `useSaveSettings`; `pages/dashboard/space/settings/`:
`attendanceSchema` (both contracts' `safeParse`, merged), `useAttendanceCard` (the two reads' states),
`useAttendanceForm` (the form and the one save), `AttendanceCard`; `SettingsPage` places it first. Copy
`spaceSettings.attendance` ×2. Docs: `occupancy.md` (scope, *Who uses it*, a *Web decisions* line, code map *Web*, open
findings, *Web history*); `space-settings.md` (*What it does*, *Behaviour* the attendance card, a *Web decisions* line,
*Web history*); finding **96 → Resolved**, moved in the index; `architecture.md`; `overview.md`; `docs/README.md`.
- **Departures:** `FormSchema` exported from `shared/forms` (a type, for the page's schema); the card's form hook is a
  file of its own (`useAttendanceForm.ts`) beside `useAttendanceCard.ts` (one responsibility each); the frame's state
  (unsaved, discard, «لم يتغيّر شيء») is written in the page's hook, as `useSettingsCard` is internal to
  `space-settings`; the form's stay-limit field is named `maxStayMinutes` (holding hours) so a refusal lands on it, as
  #98's `priceAgorot`; only-the-capacity saves toast «حُفظت إعدادات «الحضور والحالة المباشرة»» from the page, a
  settings save by `useSaveSettings` — one toast either way; test 36 renders the card (`AttendanceCard`) rather than
  the hook, so the capacity's query and its new baseline are the real ones.
- Tests (new code, written with it): 31 occupancy's part (1), 35 `attendanceSchema.unit.test.ts` (2) → unit `Tests  3
  passed (3)`; 36 `useAttendanceCard.component.test.tsx` (4) → `Tests  4 passed (4)`.
- Breaks, each red, each restored: 31 capacity as `PATCH` → `Tests  1 failed (1)`; 35 the settings' issues dropped →
  `Tests  1 failed | 1 passed (2)`; 36 the two calls swapped → `Tests  3 failed | 1 passed (4)`; 36 the form reset on a
  partial failure → `Tests  1 failed | 3 passed (4)`; 36 the old capacity kept as the baseline → `Tests  1 failed | 3
  passed (4)`.
- Checks: lint → 0; typecheck → 0; Prettier → clean; `check:links` → `2466 links in 188 documents and 1534 source files
  all resolve.`; `check:classes` → `No physical direction or arbitrary-value classes in 1058 files.`; the settings'
  component tests with the routes' → `Test Files  5 passed (5)` / `Tests  13 passed | 44 skipped (57)`.

### Plan commit 6 — `4f8a5c2a` `feat(space-settings): edit the debt reminder` (44)
Built `useReminderCard` (the text, or the catalogue's while the space keeps none; inserts at the caret; the preview;
the restore; the refusal by code — `invalid_choice` names the first placeholder off the list, isolated;
`invalid_format` the missing amount or a character), `reminderPreview`, `ReminderCard`; `SpaceSettingsCards` takes
`spaceName`, which `SettingsPage` reads from `space-links`' `useMySpacesQuery` (the Arabic name, else the English).
Copy `spaceSettings.reminder` ×2. Docs: `space-settings.md` *What it does*, *Behaviour* the reminder, two *Web
decisions*, code map, *Web history*; `overview.md`.
- **Departures:** "uses the default" is a ref, read by the form's preparation (`useServerForm` builds its resolver
  once, with the first `prepare`), not state; the textarea's ref is created by the component and the insert takes the
  field from the click (the React lint rule `react-hooks/refs` refuses a hook-owned ref read in a handler made during
  render); the catalogue's text is per interface language, so a space that keeps none previews it in the owner's
  language.
- Tests (new code, written with it): 37 `reminderPreview.unit.test.ts` (1) → unit `Tests  3 passed (3)` (the settings
  folder); 38 `useReminderCard.component.test.tsx` (4, rendering the card) → `Tests  4 passed (4)`; the settings
  folder's component tests → `Tests  11 passed (11)`.
- Breaks, each red, each restored: 37 the first only (`replace`) → `Tests  1 failed | 1 passed (2)`; 38 the insert
  appended → `Tests  1 failed | 3 passed (4)`; 38 the default text sent as text → `Tests  2 failed | 2 passed (4)`; 38
  the token unnamed → `Tests  1 failed | 3 passed (4)` (re-run with UTF-8 output: my script's print failed on Arabic the
  first time, the file restored by its `finally`).
- Checks: lint → 0 (after one unnecessary optional chain in the test); typecheck → 0; Prettier → clean; `check:links`
  → `2466 links in 188 documents and 1539 source files all resolve.`; `check:classes` → `No physical direction or
  arbitrary-value classes in 1063 files.`

## 3. On the head (`4f8a5c2a`), once each
- 17:36: `app-b` vitest/tsc → 2 (worker B's); waited (polled every 15 s) until 0 at 17:39; free memory 4,839 MB of
  15,680 MB.
- `npm run test:unit` → exit 0: `Test Files  19 passed (19)` / `Tests  230 passed (230)`; `Test Files  52 passed (52)` /
  `Tests  783 passed (783)`; `Test Files  96 passed (96)` / `Tests  876 passed (876)`.
- 17:40: app-b → 0; free 5,286 MB. `npm run test:component -- --reporter=verbose` (foreground) → exit 0: **`Test Files
  188 passed (188)` / `Tests  1225 passed (1225)`**, `Duration  443.43s`. The `--reporter` flag did not reach Vitest
  through the workspace script (npm: `Unknown cli config "--reporter"`), so the lane printed no per-test time.
- **Finding 87's time**, the routes file alone (a diagnostic, not the lane): first run `× … lists the owner’s eleven
  pages … 3061ms`, `Tests  1 failed | 45 passed (46)` (the machine busy just after the lane); again, free memory 3,144
  MB, no vitest running: `✓ … 2227ms`, `Tests  46 passed (46)`. The full lane passed it; CI's `test:component` judges.
- `NODE_ENV=production npm run build` → exit 0, `✓ built in 1.96s`; `npm run check:build` → `No showcase code in 42 build
  files (1030 strings checked).` / `No dashboard code in the site's first download.` / `No data-table or leaflet, nor
  Leaflet's stylesheet, in the site's first download.`; `npm run check:classes` → `No physical direction or
  arbitrary-value classes in 1063 files.`; `npm run format:check` → `All matched files use Prettier code style!`; `npm
  run check:links` → `2466 links in 188 documents and 1539 source files all resolve.` Not run: `test:api` (no API or
  shared change; CI runs it).

## 4. The real run (head `4f8a5c2a`)
- **Browser:** local headless Chrome over CDP (no `playwright` MCP tools in this session). Scripts in `scripts\`:
  `cdp3.mjs`, `common3.mjs` (#98's, shots to `pr3`; the network log now carries a write's body, never a sign-in's),
  `probe3.mjs`, `pr3run1.mjs`, `pr3run2.mjs`. Shots: `shots\pr3\` (50 PNG, 4 network logs).
- **Setup:** `docker start masaha-postgres-1`; `prisma migrate status` → `Database schema is up to date!`; API `/health`
  → `{"status":"ok","db":"up",…}`; web 5320 → 200. **The demo accounts accept `SEED_DEMO_PASSWORD`** (`probe3.mjs`:
  `owner 200`, `reception 200`; no password printed; the one-time passwords masked in the script's own log).

| Case | Seen | Shots |
|---|---|---|
| The staff page | h1 «الموظفون»; the role line; «موظف واحد»; «إضافة موظف»; «ليلى النجار / demo-reception@example.com / نشط» | `ar-light-1440-staff-page` |
| Add with a new email | the sheet «إضافة موظف / الدور: الاستقبال / الاسم / البريد الإلكتروني / يُنشأ حساب جديد لهذا البريد … لا يُربط حساب موجود. / إنشاء حساب الاستقبال»; the one-time dialog (the person, «نسخ», the created line, «واتساب»), «تم» → toast «سُجّلت طريقة التسليم: موظف تجريبي · واتساب», the focus back on «إضافة موظف»; the new row «نشط / لم يغيّر كلمة المرور المؤقتة بعد» | `-staff-add-sheet`, `-staff-added-one-time-dialog`, `-staff-added-row` |
| Add with an email that has an account | the admin's email → on the email «لهذا البريد حساب في مساحة، ولا يُربط حساب موجود. استخدم بريدًا آخر؛ …» | `-staff-add-existing-refused` |
| Re-issue offered and its handover | the new row's menu «كلمة مرور مؤقتة جديدة / إيقاف وصوله»; the confirm «كلمة مرور مؤقتة جديدة لـ موظف تجريبي؟ / تحلّ محلّ …», opened on «رجوع»; «إصدار» → the dialog with the issued line → handover toast; the focus back on «إجراءات: موظف تجريبي» | `-staff-new-row-menu`, `-staff-reissue-confirm`, `-staff-reissued-one-time-dialog` |
| Re-issue held | the demo receptionist's menu: «كلمة مرور مؤقتة جديدة» held, «غيّر كلمة المرور المؤقتة؛ إن نسي كلمة مروره يستعيدها بالبريد.» under it | `-staff-reissue-held` |
| Deactivate, reactivate | «إيقاف وصول ليلى النجار؟ / تنتهي كل جلساته على كل الأجهزة فورًا، …», opened on «رجوع»; confirmed → «بلا وصول», no toast; the menu «إعادة وصوله / كلمة مرور مؤقتة جديدة / أعد وصوله أولًا.»; «إعادة وصوله» → «نشط», no toast | `-staff-deactivate-dialog`, `-staff-deactivated`, `-staff-deactivated-menu`, `-staff-reactivated` |
| The settings' cards | h1 «الإعدادات»; «الحضور والحالة المباشرة», «تسعير الزيارات» (its link «الباقات والأسعار»), «الاستقبال», «رسالة التذكير» | `ar-light-1440-settings-page` |
| The attendance card's one save | capacity 40 → 35 and the stay limit (none) → 5 in one save: `PUT …/capacity {"capacity":35}` then `PATCH …/settings {"maxStayMinutes":300}`, one toast «حُفظت إعدادات «الحضور والحالة المباشرة»»; the limit cleared → `PATCH {"maxStayMinutes":null}`; capacity 0 → «عدد صحيح من 1 إلى 1000», nothing sent; «تجاهل التغييرات» → 35; put back to 40, no limit | `-attendance-unsaved`, `-attendance-saved`, `-attendance-refused` |
| Visit pricing | up after 10: «ساعتان و9 دقائق = ساعتان · ساعتان و11 دقيقة = 3 ساعات»; half hour → the minutes disabled, `PATCH {"visitRounding":"NEAREST_HALF_HOUR","visitRoundingMinutes":null}`; up after 15 → `PATCH {"visitRounding":"UP_AFTER_MINUTES","visitRoundingMinutes":15}`, «ساعتان و14 دقيقة … ساعتان و16 دقيقة …»; left at 15 as before the run | `-pricing-up-after-10`, `-pricing-half`, `-pricing-up-after-15` |
| The reception switch | on → `PATCH {"receptionMayTypePrices":true}`, toast «حُفظت إعدادات «الاستقبال»»; put back off | `-reception-unsaved`, `-reception-saved` |
| The reminder | the default shown (none saved); each token inserted at the caret, the caret after it, the focus in the field, the preview filled («رهف», «‏150 ₪», «مساحة تجريبية»); without `{المبلغ}` → «أضف {المبلغ} ليعرف الزبون كم عليه.»; `{الاسم الكامل}` → «{الاسم الكامل} ليس من الكلمات المتاحة؛ …»; a valid text saved; «استعادة النص الافتراضي» → `PATCH {"reminderTemplate":null}` | `-reminder-inserted`, `-reminder-missing-amount`, `-reminder-unknown`, `-reminder-saved`, `-reminder-restored` |
| Reception refused | `/staff` and `/settings` → «لا تملك صلاحية الوصول إلى هذه الصفحة / هذه الصفحة غير متاحة لحسابك.»; neither in its sidebar; 0 requests to them | `ar-light-1440-reception-staff-403`, `-reception-settings-403` |
| Widths | Arabic light 768/390, English dark 1440/768/390: the staff page (a table from 768, cards at 390), a row's menu, the add sheet, the settings page; no horizontal scroll at any width | `{ar-light-{768,390},en-dark-{1440,768,390}}-{staff-page,staff-row-menu,staff-add-sheet,settings-page}` |
| Network log | **0** `/admin/` requests in every owner run (28, 20, 27 requests) | `ar-light-1440-network-log.txt`, `-staff-network-log.txt`, `ar-light-network-log.txt`, `en-dark-network-log.txt` |

- Page errors: 0 in every run. Not performed, as the plan names (component tests prove them): the attendance card's
  partial failure (test 36), a re-issue's `ACCOUNT_HAS_LINKS` (test 29), a re-activation's `ACCOUNT_IS_ADMIN` (test 28).
- My script's own defect, not the app's: the reminder's caret offsets I chose fell inside a word, so the inserted text
  reads «ع{المبلغ}ليك»; each token went exactly where the caret was.
- Seen, for the review: the reminder's preview names the space by its Arabic name in the English interface too (the
  plan's "the Arabic name when there is one").
- **Data left in `masaha_dev`:** the receptionist «موظف تجريبي» (`pr3-staff-…@example.com`), active, its temporary
  password pending (no delete exists; it can be deactivated); the demo receptionist deactivated and re-activated (two
  audit entries, its sessions ended); the space's settings and capacity as before the run (capacity 40, no stay limit,
  up after 15, reception's switch off, the reminder `null`), with their audit entries for each save.
- Servers and the CDP Chrome stopped by PID; ports 3320 and 5320 → none listening.

## 5. `#PRNUM`, the push, the PR
- Truth check before the push: `occupancy.md` still said "No web screen reads it yet" — now "No web screen reads the
  state now yet; the owner's settings page reads and sets the capacity.", folded into commit 5 (`--fixup` + autosquash
  on `origin/main`, which had not moved: `cf3190a4`).
- `git grep -n "#PRNUM" HEAD` → 31 lines; the next number → `gh api …issues… --jq '.[0].number'` → 98, so **99**.
  `git filter-branch … 's/#PRNUM/#99/g'` over `origin/main..HEAD`; `refs/original` removed; `git grep "#PRNUM" HEAD` →
  0; `git diff origin/main --stat` → `131 files changed, 4968 insertions(+), 102 deletions(-)` before and after;
  `check:links` → `2466 links in 188 documents and 1539 source files all resolve.`
- Commits now: `24626e8c` fix(packages): word a row's refusal as the owner's (50) · `93cdb2a4` fix(spaces): drop a
  refused retired amenity (43) · `132dd08b` fix(spaces): name the prices card one way (41) · `8b592880` feat(users):
  record a handover at a space (41) · `4a4ff5b3` feat(staff): add the owner's staff page (39) · `a3b36c3d` feat(staff):
  deactivate, reactivate and reissue (47) · `afc65252` feat(space-settings): add the owner's settings (46) · `b1cb1fe4`
  feat(space-settings): save the attendance card (46) · `20531c2c` feat(space-settings): edit the debt reminder (44).
- Pushed `feat/owner-staff-settings`; **PR #99** https://github.com/Basel-Ghonaim/masaha/pull/99 (assignee me; `feat`,
  `area:web`, `area:docs`; title = the plan's commit 2's subject; the description says "Carried from #98" and asks the
  owner to approve the amenity line's Arabic). The number matches. Open PRs before it: none (no conflict check owed).
- **CI on `20531c2c`** (run 39443989564): build, check:classes, check:links, format:check, lint, test:api,
  **test:component** (9m17s), test:unit, typecheck — all `pass` (CodeRabbit: rate limited, `pass`). `gh pr view 99 --json
  headRefOid,mergeStateStatus` → `20531c2c…`, **`CLEAN`**. `git status --short` → empty.

## 6. Final report (`final-report`)
1. **PR #99** https://github.com/Basel-Ghonaim/masaha/pull/99 · head **`20531c2c`** · CI green on that head (run
   39443989564) · **`CLEAN`**. Not merged.
2. **Commits:** the carried three (`24626e8c` 50, `93cdb2a4` 43, `132dd08b` 41), then the plan's 1–6 (`8b592880` 41,
   `4a4ff5b3` 39, `a3b36c3d` 47, `afc65252` 46, `b1cb1fe4` 46, `20531c2c` 44).
3. **Run:** per commit lint + typecheck (§2); on the head `test:unit` (230 / 783 / 876), `test:component` (188 files,
   1225 tests, 443 s), build, `check:build`, `check:classes` (1063), `format:check`, `check:links` (2466); the real run
   (§4); CI all green. **Not run:** `test:api` locally (no API change; CI passed it); E2E (end of project); in a browser
   the attendance card's partial failure, `ACCOUNT_HAS_LINKS`, `ACCOUNT_IS_ADMIN` (tests 36, 29, 28).
4. **Breaks / red first:** carried items 1, 2, 3, 4, 6, 7, 8, 9 and plan tests 21–40 — each seen red (§2); test 41 is the
   existing catalogue parity test, run in the unit lane.
5. **Problems and how solved:** heredocs that would not parse (files written instead); the file tool writing `\u`
   escapes as literal isolate marks (rewritten via `chr(92)`, the whole diff scanned: none left); a subject at 54
   characters (amended at once); React Query passing `mutationFn` a second argument (wrapped); the resolver keeping the
   first `prepare` (a ref); the `react-hooks/refs` lint rule (the ref read in the click); worker B's lanes running
   (waited); my break script's print on Arabic (UTF-8); `--reporter` not reaching Vitest through the workspace script
   (the routes file timed alone); a stale "no web screen" sentence (folded into commit 5).
6. **Unexpected, unsolved:** the routes file alone missed finding 87's 3 s wait once right after the full lane (3061 ms)
   though the lane passed it, then passed (2227 ms); the reminder's preview names the space in Arabic in the English
   interface (the plan's rule, worth a look); `useMenuTriggers` copies the admin page's `useRowTriggers`; packages'
   `countOf` and other local digit readers remain beside the new `shared/lib` `wholeNumberOf`; staff and settings do
   not refresh `['me']` on a 404 as packages now do (not in the plan).
7. **Early conflict check:** `gh pr list --state open` → #100 (`feat/visit-debts`, worker B, head `68edd9bc`). `git
   merge-tree --write-tree origin/feat/owner-staff-settings origin/feat/visit-debts` → conflicts in
   `docs/architecture/findings/README.md` (B adds 110–113, this PR 102, beside 100/101), `docs/features/space-settings.md`
   (the header's date; B's API line, this PR's web lines) and `docs/project/overview.md` (each its own *Built* line);
   `docs/README.md` auto-merges. No code file shared — the fast path (workflow §9) for whichever merges second.
8. **Departures:** gathered in §2–§5 — the carried items' shapes (`useLinkEnded`, the toast's option asserted, the
   amenity dropped by its index, `sectionName`); A3's shape (`RecordHandover`, `recordAdminHandover`); the staff slot as
   one `ShownPassword` object; finding 90 resolved in commit 3; the toolbar's add only with rows; the menu's order; extra
   files; `wholeNumberOf` in `shared/lib`; `FormSchema` and `FailureLines` exported; the attendance form hook in its own
   file and test 36 rendering the card; the reminder's ref; the occupancy sentence fixed before the push.

## Fix round 1 (`7_FIXES_PROMPT_PR3.md`, review `6_REVIEW_PR3_CLAUDE_CODE.md`)

### First
- `git status --short` clean on `feat/owner-staff-settings`; `git fetch origin` → `main` at `5d42a527` (#100 merged).
- `docker start masaha-postgres-1` failed: Docker Desktop not running (`failed to connect to the docker API …`); stopped
  and asked; the owner started it; the container started.
- **Rebase** `git rebase origin/main`: text conflicts only in the three foreseen documents —
  `docs/architecture/findings/README.md` (commit A: 102 kept before #100's 110–113; commit a3b36c3d: 90 into
  *Resolved* beside #100's 100; commit 5: 96 the same), `docs/features/space-settings.md` (commit 4: the header's
  *Authority* and *Scope* this PR's, its body #100's), `docs/project/overview.md` (commits 4, 5, 6: this PR's *Space
  settings* line, #100's *Front desk* line with its debts). No code file conflicted; every #100 line kept. New heads:
  `2645ebe6` … `1130642b`.
- At the supervisor's note, after the rebase: `prisma migrate status` → `20261020124728_visit_write_off` pending;
  `npx prisma migrate deploy` → `All migrations have been successfully applied.`; `npx prisma generate` → generated.
- `npm run build -w @masaha/shared` → 0; `npm run lint` → 0; `npm run typecheck` → 0.

### The fixes (each folded into its commit: `--fixup`, then `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash origin/main`)
1. **The attendance card's partial fact** (review 1) → commit 5. The fact is the card's **note** while `partial`
   holds (`SettingsCardView.note`, `role="status"`), beside whatever failure view the second request gets; the
   failure title is the card's own again; on the partial path `forbidden` is `attendance.forbiddenAfterCapacity`
   «لم يعد هذا متاحًا لك في هذه المساحة.» / "This is no longer open to you at this space." (new, both catalogues);
   discard clears it. Docs: `space-settings.md` *Behaviour* and decision, finding 96's resolution ("whatever the second
   request's failure").
   - Red (two new tests, before the code): `Tests  2 failed | 4 passed (6)` — a network failure (`ERR_NETWORK`) on the
     PATCH: `Unable to find an element with the text: The capacity was saved; …`; a 403: `Unable to find … This is no
     longer open to you at this space.` Green: `Tests  6 passed (6)`.
   - Breaks: the note dropped → `Tests  3 failed | 3 passed (6)`; the forbidden line as before → `Tests  1 failed | 5
     passed (6)`; restored.
2. **A 404 on the staff, settings and capacity routes refreshes `['me']`** (review 2). `useLinkEnded` moved
   (`git mv`) from `features/packages/hooks/` to **`shared/api/query/useLinkEnded.ts`**, exported by `@shared/api`:
   *why there* — it is the only `shared/` module on React Query (beside the one QueryClient), and §7, which defines the
   `['me']` scope it marks, is `shared/api`'s; `shared/session` has no query code. Used by packages (unchanged
   behaviour), staff (`useStaffQuery`'s read, `useAddStaff`, `useSetStaffActive`, `useReissue`), space-settings
   (`useSpaceSettingsQuery`, `useSaveSettings`) and occupancy (`useCapacityQuery`, `useSetCapacity`); the queries by an
   effect on their error. Folded: the move into commit A (packages), staff into commits 2 and 3, settings into 4,
   occupancy into 5. Docs: `architecture.md` §7 ("a 404 on the owner's packages, staff, settings and capacity routes
   … (`useLinkEnded`, `shared/api`'s …)"), `packages.md` (code map, decision), `space-links.md`, `space-settings.md`,
   `occupancy.md`.
   - Tests: "fetches the owner’s own spaces again when the list is refused 404" (`useStaffList`), and the settings'
     load failure asserting `['me','spaces']` invalidated (`SpaceSettingsCards`) — written with the code, green
     (`Tests  23 passed (23)` with packages); red by the breaks: the staff call dropped → `Tests  1 failed | 3 passed
     (4)`; the settings call dropped → `Tests  1 failed | 1 passed (2)`; the shared hook never matching → `Tests  5
     failed | 18 passed (23)`; restored.
3. **A lost add answer shows the new row** (review 3) → commit 2. `useAddStaff`'s `onError` invalidates
   `staffKeys.list(spaceId)` (and `useLinkEnded`). `EMAIL_HAS_ACCOUNT`'s line for both cases — **for the owner:**
   «لهذا البريد حساب في مساحة، ولا يُربط حساب موجود. استخدم بريدًا آخر؛ وإن كان في قائمة موظفيك فمن صفّه: أعد
   وصوله، أو أصدر له كلمة مرور مؤقتة جديدة.» / "… Use another email; if they are on your staff list, act from their
   row: give their access back, or issue them a new temporary password." Docs: `space-links.md` *Behaviour* and design
   issue 10's decision.
   - Red: `Tests  2 failed | 3 passed (5)` — `expected [ { …(19) } ] to have a length of 2 but got 1` (the network
     failure, the list not read again) and the line. Green: staff folder `Tests  25 passed (25)`. Break (no
     invalidation) → `Tests  1 failed | 4 passed (5)`; restored.
4. **The default reminder after a language switch** (review 4) → commit 6. `isDefaultText` compares with **every**
   catalogue's `defaultText` (`CATALOGUES`), read at check time. Docs: `space-settings.md` *Behaviour*.
   - Red: the new test (Arabic, `setLanguage('en')`, save unchanged) → `Unable to find an element with the text:
     Nothing changed`, `Tests  1 failed | 4 passed (5)` (after fixing my own test's lookup by the English label).
     Green: settings folder `Tests  12 passed (12)`. Break (the first language only) → `Tests  1 failed | 4 passed
     (5)`; restored.
5. **The documents** (review 5): `occupancy.md`'s *Authority* "…; on the web, the settings page's attendance card reads
   and sets the capacity." (commit 5); `users.md` *Last Updated* 2026-10-18 → 2026-10-20 (commit 1); the blank line in
   `space-links.md`'s *Web decisions* removed (commit 2).
6. **The rest** (review 6–8): the English copy's comment moved back above `refusals` (commit 6); the loading states are
   one pattern, `role="status"` with a visually hidden «جارٍ التحميل»-line (`copy.status.loading`) over the placeholders,
   in `AttendanceCard` (commit 5) and `SpaceSettingsCards` (commit 4); a failed settings read is said once — the
   attendance card shows its own alert only when its capacity read failed, and draws nothing when only the settings
   failed (commit 5).
   - Tests (written with the code): "leaves settings that cannot be read to the cards below, drawing no alert of its
     own", "says it is loading to a screen reader while its values arrive" (attendance), "says it is loading … while
     the settings arrive" (cards) → `Tests  11 passed (11)`. Breaks: two alerts again → `Tests  1 failed | 7 passed
     (8)`; the attendance's status role dropped → `Tests  1 failed | 7 passed (8)`; the cards' dropped → `Tests  1
     failed | 2 passed (3)`; restored.
7. **Findings recorded** (each a file and an index line, Open): **103** Arabic-Indic digits are read by five helpers
   (commit 4; linked from `space-settings.md`); **104** the staff menu's row triggers copy the admin page's (commit 3);
   **105** a held menu item may be unreachable by the keyboard — **unverified in Radix's source**, a project-wide
   pattern (commit 3); **104, 105** linked from `space-links.md`; **106** two approved owner lines miss a case, or the
   label in the name (`ACCOUNT_HAS_LINKS` for an admin's account; the insert buttons' names) (commit 6; linked from
   `space-links.md` and `space-settings.md`). Review 13 (what a `null` reminder sends) left to the finance step, as the
   review accepts.
- The autosquash met text conflicts in `space-links.md` (twice) and `space-settings.md` (twice), where a fixup made on
  the head carried a later commit's lines as context: each resolved by keeping the earlier commit's own lines and the
  fix, the later lines returning with their commit; the final tree checked (every sentence present once, no marker).
- Bodies: a line added where the *why* changed — commit A (the shared hook's place), commit 2 (the list read again on
  a failed add), commit 5 (the note rather than the title) — via an `exec git commit --amend -F` rebase; the tree
  unchanged (`TREE-UNCHANGED`). Commits now: `62ea2287` (50) · `498d9d6f` (43) · `a15b2f4e` (41) · `98358852` (41) ·
  `f25f3830` (39) · `ad898745` (47) · `1c5d6ce4` (46) · `9c48b95f` (46) · `3d1ed3d3` (44).
- On the squashed tree: `npm run lint` → 0; `npm run typecheck` → 0; `check:links` → `2487 links in 196 documents and
  1543 source files all resolve.`; `check:classes` → `No physical direction or arbitrary-value classes in 1063 files.`;
  `format:check` → `All matched files use Prettier code style!`

### Verify (fix round)
- Before the run: app-b vitest → 0; free memory 3,677 MB (10:49).
- The touched component files: `npx vitest run --project component src/features/packages src/features/staff
  src/features/space-settings src/pages/dashboard/space src/pages/dashboard/routes.component.test.tsx` → `Test Files  1
  failed | 14 passed (15)` / `Tests  1 failed | 108 passed (109)`: only finding 87's «lists the owner’s eleven pages»
  (3122 ms). The routes file alone (free 7,802 MB) → `✓ … 3468ms`, `Tests  46 passed (46)` — the standing exception;
  CI's `test:component` judges.
- Unit `src/features src/shared src/pages` → `Test Files  84 passed (84)` / `Tests  702 passed (702)`.
- `NODE_ENV=production npm run build` → `✓ built in 1.79s`; `npm run check:build` → no showcase code, no dashboard
  code and no data-table or leaflet in the site's first download.

### Real run (fix round; headless Chrome over CDP; shots `shots\pr3-fixes\`, 6 PNG)
- Demo accounts: `owner 200`, `reception 200` (no password printed).
- **The reminder after a language switch**, the space keeping none: Arabic light → English, at 1440 and 390: the field
  follows to "Hello {الاسم}, …"; «Save» → "Nothing changed", **0 writes**; English dark → Arabic, at 1440 and 390: the
  same, «لم يتغيّر شيء», 0 writes (`{ar-light,en-dark}-{1440,390}-reminder-after-language-switch`).
- **The add sheet's reworded line** (the admin's email): English "… if they are on your staff list, act from their row:
  give their access back, or issue them a new temporary password."; Arabic «… وإن كان في قائمة موظفيك فمن صفّه: أعد
  وصوله، أو أصدر له كلمة مرور مؤقتة جديدة.» (`ar-light-1440-…`, `en-dark-1440-staff-add-existing-line`; the run's
  language had switched by then).
- 0 `/admin/` requests, 0 page errors. **Not performed, by design:** the attendance card's partial failure (no way to
  fail only the second request without changing code or data — its tests prove it) and a lost add answer (the same).
- Data changed: none (the reminder saved nothing; the add was refused). Servers and the CDP Chrome stopped by PID;
  ports 3320 and 5320 free.

### Push and CI (fix round)
- `git grep "#PRNUM" HEAD` → 0 (`#99` already). `git push --force-with-lease` → `20531c2c...3d1ed3d3 (forced update)`.
- PR description: a "Fix round (review of #99)" section before *Scope*, with each item and the two reworded Arabic lines
  for the owner.
- **CI on `3d1ed3d3`** (run 39565398657): build, check:classes, check:links, format:check, lint, test:api,
  **test:component** (9m58s), test:unit, typecheck — all `pass`; CodeRabbit `pass` (review completed). `gh pr view 99
  --json headRefOid,mergeStateStatus` → `3d1ed3d3…`, **`CLEAN`**. Open PRs: only #99 (no conflict check owed).
  `git status --short` → empty. Not merged.
