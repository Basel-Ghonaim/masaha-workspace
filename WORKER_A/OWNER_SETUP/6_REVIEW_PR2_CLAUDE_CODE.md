# Review — OWNER_SETUP PR 2 (#98, `feat/owner-packages`)

**Head:** `8c429ff46225c9408eda9298ba1bd76ce6bb6244` · base `origin/main` `abc28e73` · `CLEAN` · `gh pr checks 98`:
every lane `pass` (build, check:classes, check:links, format:check, lint, test:api, test:component,
test:unit, typecheck; CodeRabbit skipped). The head was the same at the end of the review.

**Verdict:** no blocker. Mergeable as it stands. The fixes below are small, so they belong in **PR 3's first
commit**; two are findings to record.

What I saw myself: the commit objects (`git diff origin/main...8c429ff4`, `git show` of each commit and of
the files at the head), the shared packages schemas, the API's packages service, `toFieldErrors`,
`useRefusalView`/`RefusalText`, the editor's keys and toasts, and the CI checks. What I only read in
`4_REPORT_PR2.md` and did not check: the local lanes and their times, each break seen red, finding 87's
local miss, the real run, its screenshots and network logs, the demo passwords working, and the data left
in `masaha_dev`.

## The five most important

1. **should-fix: the row toasts break the approval note's refusal lines.**
   `apps/web/src/features/packages/components/toast/packageToasts.tsx:9-13` (used by
   `hooks/list/useRowWrite.ts:203-211`).
   - The switch and «إزالة الوردية» are `PATCH /manage/spaces/:spaceId/packages/:id`, a package's route.
     Their failure toast reads the refusal through `RefusalText`. `RefusalText` passes no `lines` to
     `useRefusalView` (`shared/forms/components/RefusalText.tsx:9`), so it uses the generic `errors`
     catalogue.
   - *Scenario:* the owner's link ends, then they press a package's switch. The server answers 404, and
     the toast says «تعذّر تغيير إتاحة {name}» / «لم نجد ما تبحث عنه.». On a 403 it says «ليست لديك صلاحية
     للقيام بهذا.».
   - The note asks for «لم تعد هذه الباقة موجودة، أو لم تعد المساحة متاحة لك.» on a package's 404, and for
     the owner's no-cause line on a 403. Only the sheet uses those lines (`words.refusals`, through
     `useServerForm`'s `failureLines`). Test 18 checks only a 500, and only the toast's title.
   - *Fix:* give `RefusalText` an optional `lines` prop, pass it on to `useRefusalView`, and have
     `toastRowFailed` pass `copy.packages.refusals`. Add a 404 case to test 18 (break: drop the lines).
   - **Where:** PR 3's first commit. It is small, and it touches one shared component.

2. **should-fix: the retired-amenity refusal still tells the user to "untick" an amenity that is not drawn**
   (carried item 1, followed through).
   - Copy: `apps/web/src/shared/copy/english/spaces.ts:277`, `unavailable: 'An amenity you ticked is no
     longer offered. Untick it, or reload the page.'`, and the Arabic line beside it.
   - The fix in `useAmenityChecklist.ts:72-80` is correct. The count is now `value ∩ linked` minus what is
     offered, on both lists. The amenity that causes this 422 is one ticked but not linked. On either list
     it is now neither offered nor drawn, and it leaves the value only at the *next* tick or untick of
     another amenity.
   - *Scenario:* the owner (or the admin) ticks X, X is retired, and they save. The 422 says "Untick it",
     but nothing is there to untick. Saving again is refused again. Their only ways out are to tick and
     untick an unrelated amenity, or to discard.
   - *Fix, either one:*
     - the section drops ids that are neither offered nor linked from the form's value when this 422
       lands, and the line says «أزلنا من اختيارك مرفقًا لم يعد متاحًا؛ احفظ مرة أخرى.»;
     - or, at the least, the line names the ways out that really exist.
     Add a test for the save after the 422.
   - **Where:** PR 3's first commit.

3. **nit: the prices' toasts and confirm failure call the card «الأسعار», but it is titled «الأسعار المعلنة»**
   (the executor's note, which I confirm).
   - `useSaveGroup.ts:28` and `useConfirmGroup.ts:23` name the section `words.sections[group]`.
     `useSectionFrame.ts:50` builds `confirmFailureTitle` from the same value.
   - Only the frame's title (`usePricesSection.ts:220`) and the leave guard (`useSpacePricesEditor.ts:26`)
     use `publishedTitle`. So one card names itself two ways: «حُفظ قسم «الأسعار»» and
     ««الأسعار»: المعلومات ما زالت صحيحة» under a heading «الأسعار المعلنة».
   - *Fix:* resolve the section's name once by place. For example, a `sectionName(place, group)` used by
     the frame, the two toasts and the confirm failure. On the owner's place, prices gives `publishedTitle`.
   - **Where:** PR 3's first commit.

4. **nit, plausible: a new package can get stuck on a removed last shift.**
   `PackageSheet.tsx:73-100` and `usePackageSheet.ts:200-228`.
   - The shift's error (`form.errors.shiftId`) is drawn only in the chips branch.
   - *Scenario:* the owner opens «باقة جديدة» and picks the space's only shift. The shift is removed in
     another tab, and the owner saves. The server answers 422 `shiftId`, the `['space', id]` scope is
     fetched again, and `shifts` becomes `[]`. The sheet now shows «لا ورديات محفوظة بعد.» but no error.
     The value still holds the removed id, and no «بدون وردية» chip is left to clear it. Each later save is
     refused the same way, silently, until the sheet is closed and opened again.
   - I traced this in the code and did not run it. An edit cannot reach this state, because a held shift
     cannot be removed (finding 81).
   - *Fix:* when `shifts` no longer holds the chosen id, the shift goes back to `''`. Or draw the error in
     the "none" branch too.
   - **Where:** PR 3's first commit, or a finding to record.

5. **nit: `spaces.md` still says Packages & prices is not built.**
   - `docs/features/spaces.md:19` (the lines under *What it does*) ends "its prices lead to Packages &
     prices, not built yet". Commit 6 built the page, and the same document's *Behaviour* now describes it.
   - In the same document, the code map's *Web* entry (line 262) lists the index's exports without
     `useSpaceShifts`, which `index.ts` now exports for the packages page.
   - *Fix:* "…its prices lead to Packages & prices, where the owner edits and confirms them", and add
     `useSpaceShifts` to the list.
   - **Where:** PR 3's first commit (docs).

## The rest

6. **nit: the held-shift line can name an empty shift.** `usePackagesSection.ts:119-121`.
   - When `shifts` is `null` (the space still loading, or its read failed), `shift` is `undefined`, and the
     line reads «موقوفة وما زالت تحجز وردية «»؛ …». If the space's read fails, the line stays that way.
   - *Fix:* while `shifts` is `null`, draw the line without the name, or hold the line back (the clear does
     not need the name).
   - **Where:** PR 3's first commit.

7. **nit: a 404 on a new package says "This package no longer exists".**
   - `usePackageSheet.ts:107` passes `words.refusals` whatever `editing` is. A `POST` can only be refused
     404 for the space, and the package never existed.
   - *Fix:* when `editing === null`, use `not_found` «لم تعد هذه المساحة متاحة لك.» (the editor's line).
   - **Where:** PR 3's first commit.

8. **Finding to record (consistency with carried item 8): the packages' 404 does not refresh `['me']`.**
   - #98 makes an owner's 404 in the editor invalidate `['me']` (`useSpaceAnswer.ts:31-34`), so the
     switcher stops offering a space whose link ended.
   - The packages' writes (`useRowWrite`, `useSavePackage`) and the list's `GET` do not. On a 404 there, the
     switcher and `RequireSpaceRole` keep the space until `['me','spaces']` is fetched again.
   - The page's prices editor does invalidate it on its own writes' 404, but not on a read.
   - *Record:* a finding, or the same small hook in `packages` (an owner-place 404 → `['me']`, with a
     §7 line).

9. **nit: test 18 does not prove "a failure's toast stays".**
   `usePackagesSection.component.test.tsx:347-358` checks the toast's title only. `duration: Infinity`
   (`packageToasts.tsx:12`) has no assertion and no break. *Fix:* with item 1's test, check that the toast
   is still there after the default duration (fake timers), or assert the option.
   **Where:** PR 3's first commit.

10. **nit, plausible: the sheet's summary is announced on every keystroke.**
    - `PackageSheet.tsx:101` puts `aria-live="polite"` on the whole box, which includes the name.
    - Typing the name in a screen reader re-reads the name, the terms and the price at each pause. The
      plan asked for `aria-live` on the summary, so this follows the plan.
    - *Fix, if wanted:* `aria-live` on the terms and price only, or `aria-atomic` with a debounce.
    - **A finding to record** at most.

## Departures in the report, judged

- **The edit is checked with `createPackageSchema`: accepted, and I checked it.**
  - `updatePackageSchema` is `z.object({ ...terms, isActive }).partial()` (`requests.ts:54`). Each field's
    rule is the create schema's own, so the two schemas can differ only on an absent field.
  - The sheet always sends every term (`packageInput`), so the create schema refuses nothing the server
    would accept.
  - The other way round, the update schema would have let a blank validity through as absent, and the
    server would have kept the old one. That is a silent loss.
  - One corner: a stored row that the create rules refuse would block every edit of it. It is not
    reachable, because the API validates every write with the same rules, and finding 80 is about price 0
    in the database only.
- **`useRowWrite` (one hook for the switch and the clear) and `useSavePackage`: accepted.** It is the same
  `PATCH` and the same answer handling, with the title chosen by the change. `pending` is read across every
  pending write of the space's rows (`useMutationState`), and both the switch and the clear are guarded by
  it.
- **The sheet's open state lives in the section, and the form is mounted only while the sheet is open:
  accepted.** Each opening starts from the package as it stands now.
- **The field named `priceAgorot` holds shekels text: accepted.** It is the precedent of
  `pricesForm.ts:15` (`amountAgorot: string`), and a refusal lands on its field by the request's name.
- **The empty-limit line: accepted.** `toFieldErrors` gives `invalid_format` for a `''` count. The line is
  chosen only when the field is empty, so a non-whole count keeps «عدد صحيح من 1 فأكثر». Test 19 covers
  `totalHours` on and empty.
- **`too_short` added to `fieldErrors.name`: accepted.** `textSchema(1, 60)` refuses an empty name as
  `too_small` on a length, which `toFieldErrors` maps to `too_short` (`fieldErrors.ts:40-41`).
- **`useSpaceShifts` moved to commit 7: accepted.** There is no export without a caller.
- **Four extra files: accepted.** `useRowWrite`, `useSavePackage`, `ChipsField` and `packageToasts` each
  have one job and stay inside `features/packages`.
- **«باقة جديدة» has no icon: accepted.** No icon would mean a design-system change.
- **Finding 101: accepted, and true to the code as the report quotes it.** I did not open `Sheet.tsx`
  myself. The package sheet does give its own `SheetBody` `min-w-0` (`PackageSheet.tsx:56`).
- **A local Arabic-Indic digit reader: accepted** under "no drive-by refactor". With `clockTime`, `shekels`
  and `coordinates`, that makes a fourth copy, so it is worth a finding when the next one appears.
- **Finding 87's local miss under the owner's rule: accepted.** I only read about it. CI's
  `test:component` passed on this head.
- **The component lane run in the foreground after the memory kill, at the owner's word, and the rebase on
  #97: accepted.** The findings index kept 100 and 101 in order, as I saw at the head.

## Checked and fine

- **Scope and commits.**
  - Only `apps/web` and `docs` change.
  - Five commits: the three carried, then the plan's 6 and 7. Every subject is 50 characters or fewer:
    the first and the last are 49 and 47 by my count, and the other three look well under. Each body says
    why.
  - There is no tool attribution. The PR title is commit 7's subject.
- **Carried items 1–9.** Each is in the code or the docs as `0_CARRIED_FROM_96.md` says:
  - 1 and 9: the count is `value ∩ linked`, and a toggle keeps only what is offered or linked, on both
    sources, with two tests;
  - 2: §7 now names the owner's `['me']` and the lookups scope, and later the 422's `['space', id]`;
  - 3: both headers are corrected;
  - 4: the overview says "not built yet", which commit 6 then rewrites;
  - 5: the dot is `aria-hidden`, with an assertion;
  - 6: `missing` is dropped;
  - 7: the comments are reworded and rewrapped;
  - 8: an owner's 404 invalidates `scope.answered`, with a test.
  - What remains is only items 2 and 8 above.
- **The prices page.**
  - `SpacePricesEditor` is the editor's `PricesSection` on the owner's place, read from
    `/manage/spaces/:id`.
  - It has its own loading, failure, 404 and `ForbiddenState`.
  - Its own leave guard names «الأسعار المعلنة»; I saw the test and its break only in the report.
  - The confirm and the date are the section's own.
  - The no-shift note links `${spacePagePath(id,'profile')}#hours`, and the admin's editor passes `null`.
  - `key={spaceId}` is set on the page.
- **Packages: the calls and the keys.**
  - Every call is on `/manage/spaces/:spaceId/packages`, and there is no `/admin/` call. The routes test
    asserts it.
  - The keys are under `['space', id, 'packages']`. The row writes' key does not overlap the editor's
    `writeKey`, so a switch never holds the prices' leave guard.
  - The page is `OWNER` only in `navigation.ts`, and `packages` is in `dashboardOnly.ts`.
- **The sheet against the contract.**
  - Arabic-Indic digits are read.
  - A limit off is sent as `null`, and one on and empty as `''`, so it is refused on its field.
  - The amount goes through `agorotOf`, and its label follows the billing.
  - The audience is chips. The shift chips put «بدون وردية» first and are always on one.
  - The edit sends the terms whole (S11). A 409 `{ name: ['not_unique'] }` lands on the name: the API sends
    exactly that (`packages.service.ts:188`).
  - A 422 `{ shiftId: ['invalid_choice'] }` invalidates `['space', id]`.
  - A save waits for the list's refetch (`onSuccess` returns the invalidation), then closes and toasts.
- **The switch and the held shift.**
  - The switch is `aria-disabled` while pending, and a press is ignored.
  - The list is replaced from the answer by `setQueryData`, with no refetch.
  - `heldShift` appears only for `!isActive && shiftId !== null`, and the clear sends `PATCH {shiftId:
    null}`.
- **Money and words.**
  - Amounts go through `shared/lib` (`agorotOf`, `shekelsOf`, `priceText`), and a rate's amount is
    isolated.
  - Every counted noun has all six Arabic forms and `englishPlural`.
  - Both catalogues match the plan's table and the approval note's refusal lines. The Arabic one
    `satisfies Catalogue['packages']`.
  - The summary is joined by « · ».
- **Accessibility and the design system.**
  - The switch is named «{name}: متاحة», so the visible «متاحة» is in its name, and the edit is named
    «تعديل {name}», each name isolated.
  - The summary has `aria-live="polite"`.
  - Only semantic tokens (`bg-muted`, `text-muted-foreground`, `divide-border`) and logical classes are
    used, with no arbitrary values.
  - The footer's submit is full width. Test 20 checks axe.
- **The documents.**
  - `packages.md`: the header, *What it does*, *Who uses it*, *How it composes*, *Behaviour*, eight *Web
    decisions* each dated "2026-10-20, #98", the code map, the open findings and *Web history*.
  - Finding 81 is Resolved, with its resolution line, and moved in the index. Finding 101 is Open and
    indexed.
  - `architecture.md`'s *Built so far* and §7, `overview.md`'s packages line and `docs/README.md`'s line
    are true.
  - Staff and settings are not claimed: `space-settings.md` is still "(API only)". No deferred-document
    trigger is met.
