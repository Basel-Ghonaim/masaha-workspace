# Review of #143 (PR-C) — Claude Code, Opus 5.5
Head: 29a25054cca12d714bb2ede8e83dbf47dd13be07 · commits 5 · files 217 · checks: green (10 pass, CodeRabbit skipped) · head moved: no (still 29a25054, CLEAN, at the end of the review)
Verdict: mergeable after a fix round

Read-only. Every line number below is at the head. "main" means `origin/main`, the base.

## Findings (verified defects only, most severe first)

### F1 — blocker · A Sheet unmounted by a 403/404 leaves the editor holding an "open, changed" Sheet: on the 404 page every in-app navigation is silently blocked
- **Where:** `apps/web/src/features/spaces/hooks/editor/useSheetFrame.ts:44-46` (it reports `dirty` but has no unmount cleanup); `hooks/editor/useSpaceEditor.ts:32-43` (the guard is built from the editor's `sheet` + `dirty`, which nothing resets once the Sheet is gone), `:89` (`returnFocus` returns early while `sheet !== null`), `:106` (the not-found state still carries the armed `guard`); `components/editor/SpaceEditor.tsx:71` (not-found returns `<NotFoundState />` without `LeaveDialog`, which only the ready branch draws, `:93`); every section mounts its Sheet only while `host.editable` (e.g. `components/about/AboutSection.tsx:15`, `shifts/ShiftsSection.tsx:30`).
- **Seen in the code:** main's `useSectionFrame.ts:67-72` had exactly this cleanup (`return () => onDirtyChange(group, false)` on unmount). The rewrite dropped it. `useSpaceAnswer.ts:28-30` refetches the space on a 403/404, which unmounts the Sheet without `close()` ever running.
- **Scenario (admin, 404):** the admin opens «عن المساحة», types, presses «حفظ»; the space was deleted meanwhile → 404 → the space is read again → 404 → `SpaceEditor` shows the not-found state. `sheet` is still `'about'` and `dirty` still `true`, so `useBlocker` keeps blocking. The breadcrumb, the sidebar and Back all do nothing, because no dialog is drawn to answer the blocker. Only a reload gets out, and that asks through the browser's prompt. (The owner's 404, a link ended meanwhile, takes the same path unless the shell's space guard replaces the page first. I did not trace that guard, so the owner's case is plausible only.)
- **Scenario (admin, 403):** the space was verified meanwhile. The page turns read-only and the Sheet vanishes, and the 403's words go with it, since they were the Sheet's failure. Leaving the page still asks «تغادر بتغييرات غير محفوظة؟ … عن المساحة», and so does closing the tab. Focus lands on `body`, because `returnFocus` sees `sheet !== null` (plausible; I read Radix's unmount auto-focus but did not run it).
- **Test gap:** `EditSheet.component.test.tsx:158-177` only checks that «تعديل» and the dialog are gone. Its title claims "says … in the admin's words", but it asserts no words, and the words are unmounted anyway. No test covers a Sheet's 404, or the guard after either refusal.
- **Fix:** add the cleanup in `useSheetFrame` (`useEffect(() => () => reportDirty(false), [reportDirty])`, or report through a stable callback). In `useSpaceEditor`, drop the open Sheet when its section can no longer be edited (`!editable` or not-found). Draw `LeaveDialog` in every state, or reset the guard when not ready. Add tests: (a) a 404 on a changed Sheet's save, after which a link to `/elsewhere` lands; (b) a 403 after which leaving does not ask. · **Belongs:** fix round on #143, folded into `f7a3414b` (C2).

### F2 — should-fix · «عن المساحة» / «الموقع» compare with the space read at save time, so a refetch while the Sheet is open sends back the other half's (and others') stale values
- **Where:** `apps/web/src/features/spaces/hooks/profile/useProfileSheet.ts:56-62`. The form holds every profile field, both halves. On submit it computes `profileChanges(request, profileOf(space))` against the space as read now. The form is filled only on opening (`:75-77`). The query client refetches on window focus after 30 s (`shared/api/query/queryClient.ts:16,19`).
- **Seen in the code:** main's `useProfileSection` compared with `filledFrom.current`, "so a field another admin changed meanwhile is never sent back". The new docstring (`useProfileSheet.ts:28-30`) still promises that, and `docs/features/spaces.md:73-74` says each "sends only its own changed fields".
- **Scenario:** owner A opens «عن المساحة» and edits the description. Co-owner B (or A in another tab) saves a new Arabic address in «الموقع». A's tab regains focus after more than 30 s and the space is read again. A presses «حفظ». `request.addressAr` (as A's Sheet opened) differs from `space.addressAr` (B's), so the PATCH carries `addressAr: <old>` and B's address is silently reverted, under the toast «حُفظ «عن المساحة»». The same happens to B's `nameAr` when A never touched it.
- **Fix:** compare with the values the Sheet opened on (a ref set inside `useResetOnOpen`'s reset, as main's `filledFrom`). Better still, also limit the request to the part's own fields (about: names and descriptions; location: area, addresses, landmarks, pin). Add a T33 variant: open, the space read again with another field changed, save, and the body holds the typed field only. *Related, accepted:* the hours and shifts Sheets send the other half as read at opening (`useHoursSheet.ts:74`, `useShiftsSheet.ts:77`), which is the whole-group last-write-wins already in Review Focus. Taking that half from the latest read at submit would narrow it cheaply; it is the owner's call. · **Belongs:** fix round, folded into `f7a3414b` (C2).

### F3 — should-fix · The owner's header and «الموقع» name no area for a space whose area the admin hid (finding 60's defect, back in the view)
- **Where:** `apps/web/src/pages/dashboard/space/ProfilePage.tsx:20` (`AreaLine source="public"`); `features/lookups/hooks/area/useAreaName.ts:33` returns `''` when the public catalogue lacks the area, which hidden areas always do; `features/spaces/components/editor/ProfileHeader.tsx:57-58` then draws an empty span and the `·`; `components/location/LocationView.tsx:17` draws an empty line.
- **Scenario:** the admin hides «الرمال». Its spaces keep it (lookups.md:53). The owner of such a space opens «ملف المساحة»: the header reads «· موثّقة» and «الموقع» starts with an empty line. Only the Sheet's `AreaCombobox` keeps «المنطقة الحالية — لم تعد متاحة للاختيار». On main, the owner's page showed that same line in its area field.
- **Fix:** `AreaLine` on the public source, once the catalogue has loaded and holds no such area, writes the kept wording (the one `useAreaOptions` gives `kept`). The header drops the `·` when the line is empty. Add a test: a hidden area on the public source. · **Belongs:** fix round, `549c1918` (C1) for `AreaLine`, `f7a3414b` (C2) for the header.

### F4 — should-fix · The admin's amenities Sheet refuses an own amenity named like a retired platform amenity, which the checklist does not offer to tick
- **Where:** `apps/web/src/features/spaces/hooks/amenities/useAmenitiesSheet.ts:78,146` checks the clash against the whole catalogue. On the admin's page that catalogue includes retired amenities (`features/lookups/hooks/amenities/useAmenityCatalogue.ts:25-32`). The checklist offers a retired amenity only while the space holds it (`useAmenityChecklist.ts:46`).
- **Scenario:** the platform retires «مولّد». On an unverified space that does not hold it, the admin adds «مولّد» under «مرافق أخرى». The Sheet answers «هذا المرفق موجود في القائمة، اختره من فوق», yet nothing above offers it: the row can neither be ticked nor saved.
- **Also:** the `isActive` that `useAmenityCatalogue` carries (`:12,31,39`; `spaces/types/AmenityCatalogue.ts:14`) has no production reader. Only `useAmenityCatalogue.component.test.tsx:52-53` reads it. The fix below gives it its reader.
- **Fix:** check the clash against what the checklist offers: `entry.isActive || space.amenityIds.includes(entry.id)`. Add the retired case to `amenitiesForm.unit.test.ts` (or to the Sheet's test). · **Belongs:** fix round, `f7a3414b` (C2).

### F5 — should-fix · DI-3 built as a constant `unsaved: false` with no written reason; `space-links.md` now false; the link's hold is reached only by its test
- **Where:** `apps/web/src/features/spaces/components/editor/SpaceEditor.tsx:144` (`unsaved: false`); `types/OwnersSlot.ts:5-6,15` still says "whether the editor has unsaved changes"; `features/space-links/hooks/space-owners/useSpaceOwnersActions.ts:44-48`, whose hold now only `SpaceOwnersActions.component.test.tsx:181` reaches; `docs/features/space-links.md:104` ("in its notice… an unverified one's warning offers «ربط مالك»… which waits while the editor has unsaved changes") and `:201`.
- **Seen in the code:** DI-3 (approved) says "told whether a Sheet has unsaved changes as today". Constant false is functionally right, because a Sheet is modal and the header is out of reach while one is open. But neither the report nor `spaces.md` says so, X3 removed the "warning", and the document was not updated.
- **Fix (owner chooses):** (a) drop `unsaved` from `OwnedSpace` and the hold from `space-links` (its hook, its `unsavedReason` lines, its test, `space-links.md:104/201`). This is a narrow licence into another capability. (b) Keep the contract, write the reason in `spaces.md › Decisions`, and correct `space-links.md:104`. I recommend (a): by testing §3 rule 2's letter the hold is now code only a test reaches. I grade it should-fix rather than blocker because it was not written for the test and costs nothing at run time. · **Belongs:** fix round, `f7a3414b` (C2).

### F6 — should-fix · T43's DI-1 half is missing: no test opens the hours' Sheet from the shifts' no-hours action, and the test claiming it does not exercise it
- **Where:** `apps/web/src/features/spaces/components/hours/HoursSheet.component.test.tsx:318-329` is titled "… leads to the hours first without them (DI-1)" but reads a space with hours and never clicks that action. `SpaceEditor.component.test.tsx:100` checks only that the button exists. Untested: `hooks/shifts/useShiftsSection.ts:58` (action → `'hours'`) and `hooks/prices/usePricesSheet.ts:250` (`space.hours === null ? 'hours' : 'shifts'`).
- **Scenario (the break no test catches):** change `action(words.noHours.action, 'hours')` to `'shifts'`. The click then opens nothing (no `ShiftsSheet` is mounted without hours), and every lane stays green.
- **Fix:** with `NEW_SPACE`, click «الورديات»'s «أضف ساعات العمل» and expect the dialog «تعديل ساعات العمل». Do the same from the prices Sheet's «أضف وردية». Correct the misleading title. · **Belongs:** fix round, `f7a3414b` (C2).

### F7 — nit · Test titles that claim what they do not prove, and an assertion that cannot fail (testing §3 rule 6)
- `EditSheet.component.test.tsx:191`: "… or where the place may not edit". Only `?sheet=photos` is tested.
- `EditSheet.component.test.tsx:230`: `expect(bodyOf(undefined)).toBeUndefined()` is always true. The test's real proof is `:229`.
- `SpaceEditor.component.test.tsx:228-234`: the title's second half ("a complete, fresh profile says so") is the next test's; there is also a stray `restoreTransport()` mid-test.
- `SpaceEditor.component.test.tsx:285`: "shows the letter tile" is not asserted.
- `SpaceEditor.component.test.tsx:397-408`: the 403 and the 404 tests each assert only that an `h1` exists, so swapping `ForbiddenState` and `NotFoundState` passes both. Assert each state's own title.
- · **Belongs:** folded into `f7a3414b` with the fix round.

### F8 — nit · A landmark shown in the other language is inserted unisolated, with no `lang`
- **Where:** `hooks/location/useLocationSection.ts:34-36,42` and `components/location/LocationView.tsx:30`. With only `landmarkAr` in the English interface, "Landmark: قرب …" carries the Arabic run with no `lang="ar"` and no isolation; the addresses beside it get both. · **Belongs:** fold into `f7a3414b`.

### F9 — nit · A failed read shows a loading skeleton for good
- `useSpaceEditor.ts:122-123` with `ProfileHeader.tsx:95-96`: a failed gallery read leaves «اكتمال الملف» as a skeleton and the index without dots, while «الصور» shows its own failure and retry.
- `useAmenitiesSection.ts:43`: a failed catalogue read leaves «المرافق» as a skeleton.
- DI-4 asks the bar to wait, not to stay a skeleton after a failure. · **Belongs:** fold, or a finding (next free: 219, which the report offered for the toast timer; so 220).

### F10 — nit · Small wording and code mismatches
- `components/editor/SpaceEditorActions.tsx:70,76`: the phone menu's items are `disabled` while waiting. Its docstring (`:18-19`) and `spaces.md:80` say "marked, never disabled".
- `pages/dashboard/fieldSections.ts:35` ("above the field's section") and the notice paragraph of `docs/features/data-reports.md` ("the field's section just below it"): the notice is now inside the section.
- · **Belongs:** fold into `29a25054` (C5) and `f719d2c5` (C4).

## The test matrix rows of this PR (present / missing / weaker · would it fail on its break?)
- **T21** completeness — present, unit · yes (X2 as the name fails `:42-47`).
- **T22** hoursSheet — present · yes (Sunday-first index, `:57-70`).
- **T23** timeOptions — present · yes.
- **T24** nextPrice — present (`pricesForm.unit.test.ts:105-132`) · yes.
- **T25** labelled price — present · yes.
- **T26** shiftsOutside — present · yes.
- **T30** view first — present (`SpaceEditor` `:43-114`) · yes.
- **T31** hours save — present (`HoursSheet` `:69-94`, toast, focus) · yes.
- **T32** shifts save with X1 — present · yes.
- **T33** own fields only — present (`ProfileSheets` `:42-56,111-127`) · **weaker:** no read of the space between opening and saving; F2's break passes.
- **T34** discard, unchanged save, template — present (`EditSheet`, `HoursSheet:204`, `PricesSheet:54`) · yes.
- **T35** header — present · yes, but the letter tile is not asserted (F7).
- **T36** index — present · yes.
- **T37** stale pair and confirm — present · yes.
- **T38** photo keyboard, SD2, hold, Escape — present (`PhotosSection` `:202-290`) · yes.
- **T39** photo delete — present · yes.
- **T40** limit at 10 — present · yes.
- **T41** contacts, «وسيلة أخرى», keyboard order — present · yes.
- **T42** prices Sheet — present · yes, except the no-hours branch of «أضف وردية» (F6).
- **T43** shifts in use and 409 — present · **weaker:** DI-1 is missing (F6).
- **T44** hours custom mode, «إلى», last edited, DI-2 — present · yes.
- **T45** admin badges, X3, DI-3, verified view, top bar — present (`SpaceEditor` `:361-395`, `SpaceEditorActions`) · yes.
- **T46** Packages read-only, `?sheet=` once — present (`SpacePricesCard`, `EditSheet:181-189`) · yes.
- **T47** links and notices by section — present (`fieldSections.unit`, `noticeSection.unit`, `SpaceSettingsCards`) · yes.
- **T48** both languages and axe (view, each Sheet, photo edit) — present · yes.
- **T49** geolocation — present · yes.
- **T50** leave guard — present · **weaker:** no case of a Sheet unmounted by a refusal (F1).
- **T51** amenities — present · **weaker:** no retired-name clash (F4).
- **T52** lookups — present · **weaker:** `AreaLine` has no hidden-area case (F3).
- **T53** parity — existing · yes.
- "Seen failing first": the report attests it only for T48's Arabic half. The first session's per-test account was never written. I judged the tests by reading them, not by their history.

## Decisions, ODs, DIs and SDs of this PR (built / departed, judged)
- **G1** built (view, then a Sheet per section). **G2** built (order tested). **G3** built: date, stale with «ما زالت صحيحة» only when stale, empty actions, notices inside, index from 1024 px. **G4** built (no checklist, no page alert, no «كل قسم يُحفظ وحده»). **G5** built.
- **H1** built. **H2** built with X2. **H3/M2** built (64 px tile, full-width buttons and bar). **H4** built (badges; top bar).
- **P1/M1** built. **P2** built. **P3** built (the limit line replaces the button). **P4** built (Sortable; one whole-order PUT). **P5** built («حذف»/«رجوع»). **P6** built. **P7** built.
- **R1** built (Packages read-only; links re-aimed). **R2** kept. **R5** built. **R6–R9** built (labelled rows kept and shown).
- **W1–W5** built.
- **S1–S5** built. **X1** built.
- **A1–A2** built, except F4.
- **B1–B2** built (DI-6 counter). **X2** built.
- **L1–L2** built, except F3 for the owner.
- **C1–C2/M3–M4** built (tiles, «اسم الوسيلة», keyboard order).
- **X3** built. **A3**: nothing built or reserved (checked).
- **OD2** built. **OD3** built (`?sheet=` read once, `replace`, hash kept). **OD4** built. **OD5/DI-8** built (date kept on an empty-saved group). **OD7** nothing to do.
- **DI-1** built, but untested (F6). **DI-2** built and tested; nothing is sent, because the shared schema refuses it in the browser. **DI-3** departed silently: constant `unsaved: false` (F5). **DI-4** built (F9 on failure). **DI-5**, **DI-6**, **DI-7** built.
- **SD2** built and tested. **SD5** built: the owner's page reads the packages' shifts; the admin relies on the 409; finding 216 written. **SD6** built (`AreaCombobox`; `AreaSelect` kept for the add page). **SD7** built and tested. SD1, SD3 and SD4 are PR-A's and PR-B's.
- **D7:** no package data reaches the admin. `usePackageShiftIds` is called only by the owner's `ProfilePage`, and the admin's page sends no `/manage` or packages request.

## The report's deviations, judged
1. Context restart, verification redone — **acceptable.** Rule 5 ("seen failing") stays unattested for most new tests (see the matrix).
2. #143 instead of #142 — **sound.**
3. Subjects shortened to 50 characters — **sound** (workflow §3).
4. The `sortable` chunk joins in C3 — **sound** (the first page that draws it).
5. Finding 216 in C2 — **sound** (where the limit is built).
6. `weekRows` moved to `shared/lib/time` — **sound** (second user; directory.md updated). Beyond §8, but in scope.
7. Names that differ from §8:
   - `useSheetFrame` + `useResetOnOpen`, `SectionEmpty`, badges inside `ProfileHeader`, `noticeSection` — **acceptable.**
   - `profileChanges` kept and one `useProfileSheet` for both halves — **wrong in one respect:** the merge kept the whole-profile form but dropped main's `filledFrom` guard (F2).
8. `DataReportsPage.tsx` and `SpaceSettingsCards.tsx` added in C5 — **sound** (a changed signature and the link's words).
9. CI component job re-run once; 219 offered, not recorded — **acceptable** (the prompt's rule; the cause is outside this PR).
10. Not in the report — DI-3's constant `unsaved: false` and the untouched `space-links.md` — **wrong** (F5).
11. The amenities' tests living in `ContactsSheet.component.test.tsx` — **acceptable**, though the file name misleads.

## Documents
- `docs/features/spaces.md`: rewritten, with superseded decisions dated and the code map current. No removed file is named anywhere in docs or code (checked). Two problems:
  - "It sends only its own changed fields" (`:73-74`) holds only without a refetch (F2).
  - `OwnersSlot` / decision `:241` still speak of unsaved changes that are now always false (F5).
- `docs/features/space-links.md:104` (and `:201`): **false** since X3/DI-3 (F5); not touched by the PR.
- `docs/features/data-reports.md`: correct except "just below it" (F10).
- `packages.md`, `overview.md`, `space-settings.md`, `lookups.md`, `directory.md`, `glossary.md` (EC9: «الأسعار المعلنة», «سعر»), `foundation.md` (Sortable now drawn), `frontend/architecture.md` (the `sortable` chunk): accurate.
- `lookups.md:57` "show nothing while they load" is true, but for a hidden area on the public source it shows nothing for good (F3).
- Finding 216 and the index line: accurate. Findings 217 and 218 came with #140 (`19c03996`); the owner's Arabic-Indic record is written (217).
- No deferred-document trigger met (no endpoint). No tool attribution in any commit. No `#PRNUM` left.

## Scope and commits
- Five commits in plan order: C1 `549c1918` (17 files), C2 `f7a3414b` (180), C3 `1ba8748c` (16), C4 `f719d2c5` (9), C5 `29a25054` (15). All Conventional, subjects of 50 characters or fewer, no fixups.
- Web and docs only. No API, shared or schema change, as planned.
- No hardcoded text found: a grep of the new components and pages for literal text or literal `aria-label`/`placeholder`/`alt` found none. Copy is in both catalogues (parity is CI's).
- No colour or class outside tokens beyond what `check:classes` enforces.
- dnd-kit is imported only through `@shared/design-system/sortable`, from two dashboard-only components.
- Nothing toward A3.
- `useSetSpaceHidden` now also refreshes the admin editor's space (C4). It is shared with the spaces list, and the change is harmless there.

## Not checked, and why
- Nothing was run (rule: read-only). There were no lanes, no browser and no axe of my own, so dark mode, 390/768/1440 layout and a real drag rest on the report's run and screenshots.
- The design-system `Sortable`, dnd-kit's behaviour and `check:build`'s rule are PR-B's, already reviewed. I read only how PR-C calls them.
- The shell's owner space guard: whether it replaces the page before F1's owner-side 404 reaches the blocker (F1 marks the owner's case plausible).
- Radix's focus on an unmounted Dialog (F1's focus clause): read, not run.
- The API side of 409/422/403 (unchanged by this PR; T16–T20 are #140's).
- I read the remaining test files (`useSpaceEditor`, `useLeaveGuard`, `SpacePricesCard`, `PricesSheet`, the unit files) by their titles and the parts each finding needed, not line by line.
