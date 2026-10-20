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
