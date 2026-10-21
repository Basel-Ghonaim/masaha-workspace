# Review — OWNER_SETUP PR 3 (#99, `feat/owner-staff-settings`)

**Head:** `20531c2c36cf7eb0b11d47b102a5828e988efdf9` · base `origin/main` `cf3190a4` · `CLEAN` · `gh pr checks 99`:
every lane `pass` (build, check:classes, check:links, format:check, lint, test:api, test:component,
test:unit, typecheck; CodeRabbit rate limited, `pass`). The head and the checks were the same at the end of
the review.

**Verdict:** no blocker. Mergeable as it stands. The fixes below are small, so they belong in **PUBLIC PR 1's
first commit**; five are findings to record.

What I saw myself: the commit objects (`git show` of each of the nine commits, files at the head), the
shared schemas (`space-settings`, `reminderTemplate`, `occupancy`), the API's staff service, `shared/forms`
(`useServerForm`, `useFormFailure`, `useRefusalView`, `applyServerError`), `DataTable`, `Skeleton`, the admin's
`MenuActionItem`, the PR's description and the CI checks. What I only read in `4_REPORT_PR3.md` and did not
check: the local lanes and their times, each red-first run and each break, finding 87's local miss, the real
run, its screenshots and network logs, the demo accounts, and the data left in `masaha_dev`. I did not
open Radix's source (see finding 11).

## The five most important

1. **should-fix: the attendance card's partial line is lost on a network failure, a timeout or a 429.**
   `apps/web/src/pages/dashboard/space/settings/useAttendanceForm.ts:98,106`. The card sets `partial` and
   uses `lines.partial` as the form's `failureTitle`. But `useFormFailure` (`shared/forms/hooks/useFormFailure.ts:26`)
   gives a network or timeout failure its own title, «offlineTitle», and ignores `title`. A 429 view
   (`useRefusalView.ts:39-42`) has no title at all. A refusal placed on a field has no failure view
   (`applyServerError` returns `null`).
   - *Scenario:* the owner changes the capacity 40 → 35 and the stay limit, then saves. `PUT …/capacity`
     succeeds. The connection drops before `PATCH …/settings` answers. The card says only "no connection,
     try again". Nothing says the capacity was saved, which is the point of finding 96. The retry
     works: it sends only the settings, because the capacity is already the baseline.
   - *Also:* a 403 on the second request reads «حُفظت السعة، ولم تُحفظ إعدادات الخروج التلقائي» followed by
     the settings' forbidden line «…؛ لم يُحفظ شيء.», which contradicts the title. It is reachable only in a
     race.
   - The documents say the partial line shows when "the settings are refused after the capacity"
     (`space-settings.md` *Behaviour*, finding 96's resolution). A 429 is a refusal, so for a 429 that is
     not true. Test 36 checks only a 500.
   - *Fix:* show the partial fact apart from the failure view, for example as the card's note «حُفظت
     السعة» while `partial` holds, so it shows beside any failure. Use a forbidden line without «لم يُحفظ
     شيء» on the partial path. Add a test with a network failure on the second request (break: the
     note dropped).
   - **Where:** PUBLIC PR 1's first commit. The code change is small. The owner may still prefer a fix
     round here, because finding 96 is resolved on this behaviour.

2. **should-fix: a 404 on the staff, settings and capacity routes does not refresh `['me']`, unlike the
   packages' routes since this PR's carried item 7** (the executor's own note, which I confirm).
   - The 404 handling is in `staff`'s list, add, row writes and re-issue, in `space-settings`' read and
     save, and in `occupancy`'s read and save.
   - None of them invalidates `['me']`. Only `features/packages/hooks/useLinkEnded.ts` does, and
     `architecture.md:310` names only the packages.
   - *Scenario:* the owner's link ends while «الموظفون» or «الإعدادات» is open. The list or the settings say
     they could not be read (a generic «لم نجد ما تبحث عنه.» with a reference), or a save says «لم تعد هذه
     المساحة متاحة لك.». The switcher and `RequireSpaceRole` keep offering the space until `['me','spaces']`
     is fetched again.
   - The owner made carried item 7 a fix, not a finding, so the two new pages should follow it.
   - *Fix:* the same call on these routes' 404s, with a §7 line naming them. A third copy of `useLinkEnded`
     makes it a shared hook's case (it invalidates `['me']`, `space-links`' scope). Whether it moves to
     `shared/` is the owner's call. Add one test per page (break: the call dropped).
   - **Where:** PUBLIC PR 1's first commit, or a finding to record if the owner wants the shared hook
     decided first.

3. **should-fix, plausible: an account created whose answer was lost leaves the owner without a way to the
   re-issue.** `apps/web/src/features/staff/hooks/add/useAddStaffForm.ts:39`.
   - The add's `POST` has no idempotency key, so it is not retried. If its answer is lost (a network
     failure after the server committed), the sheet shows the offline view.
   - The owner retries, and the server answers `EMAIL_HAS_ACCOUNT`: «…وإن كان موظفًا سابقًا هنا فأعد
     وصوله من قائمته.»
   - The list is not read again on any failure, so the new row, active and pending, is not drawn until a
     refetch.
   - The way out the API built for exactly this, the re-issue ("a lost answer, or one that expired",
     `staff.service.ts`), sits on a row the owner cannot see. The line also points to «إعادة وصوله», which
     an active row does not offer.
   - I traced this in the code and did not run it.
   - *Fix:* on any add failure, invalidate `staffKeys.list(spaceId)`, so a row the server holds shows with
     its pending badge and its «كلمة مرور مؤقتة جديدة». Add a test: a network failure, then the list read
     again (break: no invalidation).
   - **Where:** PUBLIC PR 1's first commit.

4. **nit, plausible: after a language switch, an unchanged default reminder is saved as the space's own
   text.** `apps/web/src/features/space-settings/hooks/reminder/useReminderCard.ts:43,63`.
   - `prepare` compares the text with `defaultText`, but the form's resolver keeps the first `prepare`
     it is given (`useServerForm.ts:84`). So the comparison always uses the default text of the language
     shown at mount.
   - `usesDefault` was made a ref for this reason, but `defaultText` was not.
   - *Scenario:* the space keeps `null`, and the page opens in Arabic. The owner switches to English. The
     clean card follows `valuesOf` and shows the English default. The owner presses the reminder's «Save».
     `prepare` compares the English text with the Arabic default, so the request carries the English
     text. `changesOf` sees a change from `null`, and `PATCH {reminderTemplate: "Hello {الاسم}, …"}` is
     sent with a "saved" toast instead of «لم يتغيّر شيء». The space then keeps English words as its own.
   - I traced this in the code and did not run it.
   - *Fix:* treat the text as the default when it equals any catalogue's `defaultText`
     (`CATALOGUES.ar`/`.en`), read at check time. Add a test that switches the language and saves
     unchanged (break: compare with the first language only).
   - **Where:** PUBLIC PR 1's first commit.

5. **nit: two documents say less, or older things, than the code.**
   - `docs/features/occupancy.md:4`: the header's *Authority* still ends "The API is built; no web screen
     yet". The same header's *Scope* now names `features/occupancy`, and *Who uses it* names the settings
     page.
   - `docs/features/users.md:3`: *Last Updated* is still 2026-10-18, although this PR changes its
     *Behaviour*, decisions, code map and history (`space-links.md` and `space-settings.md` updated theirs).
   - `docs/features/space-links.md:206`: a blank line splits the *Web decisions* list in two, before the
     staff decisions.
   - *Fix:* "…; on the web, the settings page's attendance card reads and sets the capacity.", the date,
     and the blank line removed.
   - **Where:** PUBLIC PR 1's first commit (docs).

## The rest

6. **nit: an English copy comment is on the wrong key.** `apps/web/src/shared/copy/english/spaceSettings.ts:68`.
   «A save's refusals, in the owner's words…» now sits above `reminder:`, because commit 6 inserted the
   reminder between the comment and `refusals`. *Fix:* move it back above `refusals`. **Where:** PUBLIC PR 1.

7. **nit: the attendance card's loading says nothing to a screen reader.**
   `apps/web/src/pages/dashboard/space/settings/AttendanceCard.tsx:25`. It puts `aria-label` on a
   `Skeleton`, which is `aria-hidden`, so the label is never read. `SpaceSettingsCards`' loading puts
   `aria-busy` and `aria-label` on a plain `div` with no role. *Fix:* the busy wrapper with a role (or a
   visually hidden status line), as one pattern for both. **Where:** PUBLIC PR 1.

8. **nit: a failed settings read shows two alerts.** `AttendanceCard` and `SpaceSettingsCards` read the same
   query, so a failed `GET …/settings` draws «تعذّر تحميل الإعدادات» twice, each with «إعادة المحاولة».
   *Fix:* if the settings fail, only one of them says so (for example, the attendance card's alert only
   when its own capacity read failed). **Where:** PUBLIC PR 1, or accept.

9. **Finding to record (103): the Arabic-Indic digit readers are now five.**
   - `shared/lib/numbers/wholeNumber.ts` is new, beside packages' `countOf`, `clockTime`, `shekels` and
     the coordinates' reader.
   - #98's review asked for a finding "when the next one appears", and this PR is that point.
   - The departure itself (`wholeNumberOf` in `shared/lib`, with no drive-by refactor) is accepted.

10. **Finding to record (104): `useMenuTriggers` is a copy of the admin page's `useRowTriggers`.**
    - `features/staff/hooks/menu/useMenuTriggers.ts` is a second instance, and the executor flags it.
    - A feature cannot import a page's hook, so the copy is accepted for now.
    - The shared home, `shared/` or the design system's data layer, is a later refactor.

11. **Finding to record (105), plausible: a held menu item may be unreachable by the keyboard.**
    - `StaffActionsMenu` draws a held «كلمة مرور مؤقتة جديدة» as a `disabled` `DropdownMenuItem` with its
      reason inside it. It copies the admin's `MenuActionItem`, which does the same.
    - As far as I know, Radix's menu skips disabled items in its arrow-key navigation. If so, a keyboard
      or screen-reader user never reaches the reason, and S10 holds only for the pointer.
    - I did not open Radix's source, so this is unverified. It is a project-wide pattern, not this PR's.

12. **Finding to record (106): one approved copy line is false in one case, and one is outside the label in
    name.**
    - A re-issue for an account that has become an admin is answered `ACCOUNT_HAS_LINKS`
      (`staff.service.ts`, `role !== 'USER'`). The owner then reads «صار لهذا الحساب مساحة أخرى…»
      (`arabic/staff.ts:82`).
    - The insert buttons show «{الاسم}» but are named «إدراج الاسم» / "Insert the name". The visible text
      is not inside the accessible name (WCAG 2.5.3).
    - Both follow the approved plan, so I record them rather than reword them.

13. **Accepted, worth a later word: what a `null` reminder sends is not decided on the web.** The default
    shown and previewed is the interface language's (the executor's note), so an English-interface owner
    previews English. The finance step that sends the reminder will decide which catalogue `null` means.
    Until then the preview may not be what a customer receives. Recording it in finding 106's spirit, or
    in the finance plan, is enough.

## Departures in the report, judged

- **`RecordHandover` and `recordAdminHandover` (A3): accepted, and I checked them.**
  - The dialog's `recordHandover` is required, and `useHandover` wraps it with `gcTime: 0`. `mutationFn`
    passes the request alone, because React Query passes a second argument.
  - `OwnersPage` and `IssuePasswordDialog` pass the admin's. `staff` builds the space's in
    `useShownPassword`.
  - A 404 or `TEMPORARY_PASSWORD_NOT_PENDING` closes the dialog with «لم تُسجَّل طريقة التسليم»
    (`useTemporaryPasswordDialog.ts`).
  - Test 22 is retitled as the note asks. Test 21 is in `staffRepository.unit.test.ts`.
- **The slot's `ShownPassword` (the dialog's input plus `returnFocus`): accepted.** The page draws
  `<TemporaryPasswordDialog {...shown} />` and never touches a repository. Its `recordHandover` type
  repeats `users`' structurally, because features do not import each other.
- **Finding 90 resolved in commit 3, not commit 2: accepted.** The add words `EMAIL_HAS_ACCOUNT` in
  commit 2, and the other codes come with the actions that meet them.
- **The menu's order (the destructive item last, after a separator): accepted.** It is the users page's
  convention.
- **`wholeNumberOf` in `shared/lib`: accepted**, with finding 9.
- **`FormSchema` and `FailureLines` exported from `shared/forms`: accepted.** Both are types, and the
  page's schema and the toasts need them.
- **The attendance form hook in its own file, and test 36 rendering the card: accepted.** The real
  capacity query and its new baseline are exercised. The frame's state is written in the page, because
  `useSettingsCard` is internal to `space-settings`.
- **The reminder's default flag as a ref: accepted.** It is needed, because the resolver keeps its first
  `prepare`. The same reason applies to `defaultText`, which item 4 covers.
- **`useMenuTriggers` copying `useRowTriggers`: accepted**, with finding 10.
- **The toolbar's add only while people are listed (one «إضافة موظف» at a time): accepted.** The focus
  ref is read when the dialog closes, by which time the toolbar exists.
- **`fieldErrors.name.too_short` and the add's `not_found`: accepted.** #98 found the same `too_short`.
- **`minutes.fieldErrors.invalid_format` worded as `out_of_range`: accepted.**
- **The carried items' shapes** (`useLinkEnded`, the toast's option asserted, the amenity dropped by its
  index, `sectionName`): **accepted**, and I checked each.
- **The breaks:** I only read the report's red lines and did not rerun any. The one that first stayed
  green (`duration: Infinity`) was fixed by asserting the option, as #98's review offered.

## Checked and fine

- **Scope and commits.**
  - Only `apps/web` and `docs` change.
  - There are nine commits: three carried, then the plan's six. Every subject is 50 characters or fewer
    (the longest is `fix(packages): word a row's refusal as the owner's`, at 50), and each body says why.
  - There is no tool attribution. The title is plan commit 2's subject.
  - The description says "Carried from #98" and asks the owner to approve the amenity line.
- **The carried items 1–8 of `0_CARRIED_FROM_98.md`.**
  - Item 1: `RefusalText` takes `lines`, the row toast passes `copy.packages.refusals`, and a 404 case
    asserts `duration: Infinity`. Staff's re-activation toast uses the same prop.
  - Item 2: the 422's `amenityIds.<i>` ids leave the value, `shouldDirty` is set, the line is the review's,
    and the next save sends without them.
  - Item 3: `sectionName` names the frame, both toasts, the confirm failure and the leave guard.
  - Item 4: the chosen shift goes back to `''` once `shifts` lacks it.
  - Item 5: `spaces.md`'s line and its code map are fixed.
  - Item 6: the held shift has no empty name, a new package's 404 says `spaceGone`, and test 18 asserts
    that the toast stays.
  - Item 7: `useLinkEnded` covers the row writes, the sheet and the list's read.
  - Item 8: finding 102 is Open and indexed.
- **The one-time password.**
  - It lives in `useShownPassword`'s state only.
  - The add's mutation is `gcTime: 0` and reset before it is handed on. The re-issue's is `gcTime: 0` and
    reset at once. The handover's variables hold only the user and the channel.
  - No URL, log or storage holds it: I searched the diff for `console.`, `navigate(`, `searchParams` and
    storage, and found none.
  - The handover goes to `/manage/spaces/:spaceId/staff/:userId/temporary-password/handover`, and the
    admin's is unchanged.
  - The focus returns to «إضافة موظف» after an add, and to the row's menu (`triggers.focusOf`) after a
    re-issue.
- **Staff.**
  - The notice is said before the submit.
  - `EMAIL_HAS_ACCOUNT` lands on the email as `not_unique`: the API sends exactly `{ email: ['not_unique'] }`.
  - A 429 counts down.
  - The deactivation is an `AlertDialog` that opens on «رجوع». Its action is a destructive `Button`, and
    Escape and «رجوع» are held while it waits. A refusal stays inside, the sessions line is there, and
    the answer replaces the row by `setQueryData` with no toast.
  - The re-activation acts at once, with no toast. Its failure toast stays and names the person in
    isolates.
  - The re-issue is offered only while a password is pending and active. Otherwise it is held with
    S10's two reasons. `TEMPORARY_PASSWORD_NOT_PENDING` and a 404 read the list again.
  - The busy menu button keeps `aria-disabled` and `aria-busy` and does not open.
  - The approval note's refusal lines are exact: the add's forbidden, the actions' forbidden, and the
    404 naming both causes. «لا يوجد موظفون» appears for zero, in the count and the empty title.
- **Settings.**
  - Each card's dirty badge, discard (a failure set aside, a wait kept) and «لم يتغيّر شيء» work.
    `changesOf` sends only what changed, so cards never overwrite each other.
  - The rounding pair is sent together whenever either changes, with `null` minutes for the other rules.
    An empty minutes field under "up after" is refused as `required` by the shared `roundingPair`.
  - The attendance card's order is capacity first. The capacity answer becomes the baseline through the
    capacity query. Every value stays, the next save sends only the settings, and an empty capacity or
    limit is sent as `null`. Hours go as minutes, Arabic digits are read, and both contracts' issues land
    on their fields.
  - The reminder inserts at the caret, then puts the caret after the token and the focus back. Its two
    refusals are told apart, and the unknown token is named in isolates. The default is saved as `null`
    and restored as `null`. The preview fills every occurrence with «رهف», 150 ₪ and the space's name.
- **Routes and authorization.**
  - `staff` and `settings` are `OWNER` in `navigation.ts`, both `staff` and `space-settings` are in
    `dashboardOnly.ts`, and `occupancy` is rightly not dashboard-only.
  - The routes test refuses reception both pages with the 403.
- **Design system, copy and accessibility.**
  - Only semantic tokens and logical classes are used (`ps-7`, `w-px` in a column's meta). The link
    classes follow the existing precedent.
  - The menus are named «إجراءات: {name}». Every counted noun has all six Arabic forms and
    `englishPlural`. The two catalogues mirror each other, with `satisfies` on the Arabic ones.
  - The forced change's line no longer names an issuer (design issue 15).
- **The documents.**
  - `space-links.md` has a staff section (S5), five plus three *Web decisions* dated `#99`, a code map,
    an updated history, and finding 90 moved out of its open list.
  - `space-settings.md` has its header, *Behaviour*, *Web decisions* for design issues 13, 14, 16 and 17,
    the code map and *Web history*.
  - `occupancy.md` has its scope, *Who uses it*, a *Web decisions* line and the code map, with finding 96
    gone from its open list. Item 5 covers the stale *Authority* line.
  - `users.md` has A3 and design issue 15.
  - `architecture.md`, `overview.md` and `docs/README.md` claim only what is built.
  - Findings 90 and 96 are Resolved with their resolution lines and moved in the index. Finding 102 is
    Open and indexed.
