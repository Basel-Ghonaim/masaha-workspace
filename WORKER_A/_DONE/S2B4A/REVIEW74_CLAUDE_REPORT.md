# Review — PR #74 (S2b-4a: the admin's space editor, first half — web)

**Head reviewed:** `b5406c0c26536463d84fe997ec02d0944f318f11` (checked again at the end: unchanged).
**Base:** `3c3dc47b` (`git merge-base origin/main <head>`). Read from commit objects only; nothing run.

**Verdict:** not ready to merge. There is one plausible blocker: the section navigation's jumps can be undone by React Router's scroll restoration. There are also six code should-fixes and a set of test and document gaps. All are small to fix.

---

## Findings, most severe first

### 1. Blocker (plausible): a click on a section chip or a checklist line can scroll back where it was

**Where:**
- `apps/web/src/features/spaces/components/editor/SectionNav.tsx:37-41` (`<a href="#id">`)
- `components/editor/MissingChecklist.tsx:45-50` (the same plain anchor)

**Why.** I read this in react-router 8.4.0's source (`lib/router/history.js:137-147`, `lib/router/router.js:1267-1274`, `lib/dom/lib.js:1061-1130`):
- A plain fragment link is a browser POP whose `history.state` is `null`, so React Router gives the location the key `"default"`.
- The tab's first entry also has the key `"default"`, because the initial `replaceState` sets only `idx`. Its scroll position is saved under `"default"` as soon as the admin navigates away from it, and is kept in sessionStorage.
- On the hash POP, `restoreScrollPosition` is therefore a number. `ScrollRestoration`'s layout effect then calls `window.scrollTo(0, saved)` and returns before its `location.hash` → `scrollIntoView` branch. That effect runs after the browser has already jumped to the fragment.

**Scenario:**
1. Open `/dashboard/admin/spaces` fresh, at scrollY 0.
2. Click a space's name to open its editor.
3. Click «التواصل». The page jumps to the section, then back to 0.
4. Click another chip. The page "restores" the position saved just before the click, so it hardly moves.

The admin can reach a section only by scrolling. The test "never asks for a move within the page, to a section" uses `router.navigate('/spaces/7#profile')`, which is a PUSH with a fresh key, and jsdom does not scroll. The plan's own *Review Focus* named this risk ("hash navigation through React Router (popstate) and `ScrollRestoration`"), and the report shows no click-through of the chips.

**Why plausible:** the mechanism is read from the source; I did not reproduce it in a browser.

**Fix:**
- Use `<Link to={{ hash: id }}>`, through `Button asChild`, in both places. That is a PUSH with a real key: the blocker still lets it through (same pathname), and ScrollRestoration takes its hash branch (`scrollIntoView`, with `scroll-mt-*` respected).
- Prove it with a test that clicks the chip itself and expects the hash location, with no dialog.
- Check it in a real browser.

### 2. Should-fix: a 404 on a save or confirm leaves a deleted space editable

**Where:**
- `apps/web/src/features/spaces/hooks/editor/useSpaceEditor.ts:38-40`
- `hooks/editor/useSpaceAnswer.ts:20-24`

**Scenario:**
1. Space 5 is deleted elsewhere.
2. The admin saves a section of space 5. The answer is 404, so `refused` invalidates the space, and the GET 404s again.
3. TanStack Query keeps the previous `data` on a failed refetch, so `space !== undefined` and the editor stays `ready`.
4. The section says «حُذفت المساحة في الأثناء», but every section stays editable and dirty. Every later save or confirm 404s, and leaving asks about changes that can never be saved.

The same happens after a delete from the list followed by Back to the cached editor. This contradicts S4 in `docs/features/spaces.md:157` ("the page then shows the space as it is").

**Fix:** in `useSpaceEditor`, return `notFound` when `query.error?.status === 404`, before the `space === undefined` branch. Alternatively, `removeQueries` on a 404 instead of invalidating. Add a test: a 404 on a save shows the 404.

### 3. Should-fix: a dirty profile can undo another admin's change, contrary to S1

**Where:**
- `hooks/profile/useProfileSection.ts:52`: `profileChanges(request, space)` diffs against the current `space`
- the follow-effect at `useProfileSection.ts:72-75` resets only a clean form

**Scenario:**
1. Admin A edits `nameEn`, so the section is dirty.
2. Admin B saves `addressAr: "X"`.
3. A's window regains focus. `refetchOnWindowFocus` refetches the space; it is already invalidated by `keep()`'s `['admin']` invalidation (finding 14). `space.addressAr` is now "X", but A's form still holds the old address.
4. A saves. `profileChanges` sees `addressAr` differ and sends `{ nameEn, addressAr: <old> }`, silently reverting B's change.

`spaces.md:155` (S1) states the opposite: "nor is a field another admin changed meanwhile sent back".

**Fix:** diff against the values the form was last reset from (keep them in a ref, updated at each `reset`), or send only `formState.dirtyFields`. Keep comparing to `space` only for the "nothing changed" note.

### 4. Should-fix: a 429 on «المعلومات ما زالت صحيحة» counts down but never disables the button

**Where:**
- `hooks/editor/useSectionFrame.ts:46-54` takes only `.view` from `useRefusalView` and drops `.blocked`.
- `frame.confirm` (lines 93-102) has no blocked flag.
- `components/editor/SectionCard.tsx:58-66` never disables the button.

**Scenario:** a confirm answers 429 with `Retry-After: 30`. The countdown shows, but the button stays clickable and calls the server again. Save, by contrast, is disabled during its own 429 (foundation §10's "a disabled control says why"; spaces.md D5 "a 429 counts down").

**Fix:** carry `confirmFailure.blocked` into `frame.confirm.blocked` → `disabled`. The limit is the user's, not the section's, so Save should arguably be blocked too while the confirm's wait runs.

### 5. Should-fix: the editor's hooks are proven only through one component test (testing §3)

**Where:** `components/editor/SpaceEditor.component.test.tsx` (707 lines) carries:
- every request body
- the "unchanged" rule
- the dirty tracking and the leave guard
- the refusals
- the section in view

No new hook has a `renderHook` test:
- `hooks/editor/*`
- `hooks/profile|amenities|contacts|confirm/*`
- lookups' `useAmenityChecklist`, `useAreaName`, `useAmenityNames`

`docs/development/testing.md:41-46` puts a hook's logic in its own `renderHook` test, and leaves the path and body to the repository's test. The same feature follows this elsewhere (`useAddSpaceForm`, `useSetSpaceHidden`, `useDeleteSpace`, `useAreaOptions`). The editor test also re-checks method and URL that `spacesRepository.unit.test.ts` owns: lines 294, 321, 496, 663.

**Fix:** move the logic tests to hook tests, keeping in the component test what rendering decides, and drop the method/URL checks there. Otherwise the owner accepts the deviation explicitly.

### 6. Should-fix: behaviours the PR claims that no test would catch breaking (mutation check)

Each mutation below passes every test at the head:

- **(a) The other sections' edits survive a save.** Remove `if (!formState.isDirty)` in `useProfileSection.ts:74`, `useAmenitiesSection.ts:96` or `useContactsSection.ts:90`. Saving one section would then wipe another's unsaved edits (data loss). Claimed at `spaces.md:59-60`.
- **(b) The guard clears after Save or Discard.** Drop the `beforeunload` cleanup (`useLeaveGuard.ts:28-30`), or make `onDirtyChange` ignore `false` (`useSpaceEditor.ts:23-31`):
  - test :266 discards but never tries to leave afterwards;
  - test :420 covers only a page never dirtied;
  - test :429 checks only before typing and after typing.
- **(c) A section that goes away clears its dirty flag.** Remove the unmount cleanup at `useSectionFrame.ts:60-65`. Test :343 (403 → read-only) never tries to leave afterwards, so a guard that kept asking about «المساحة» on a read-only page would pass.
- **(d) A confirm goes to its own group's path.** Hard-code `'profile'` in `useConfirmGroup(space.id, group)` (`useSectionFrame.ts:45`). Only the profile is dated in the fixture, so only test :313 confirms anything.
- **(e) "Nothing changed" for amenities and contacts.** Make `sameAmenities` always false, drop its `byId` sort, or break the contacts' `JSON.stringify` comparison (`useContactsSection.ts:68`). `services/amenitiesForm.ts` is pure and has no unit test.
- **(f) A ticked amenity retired meanwhile.** The decision at `spaces.md:160` relies on `FIELDS` holding `'amenityIds'` only and on `failureLines.validation` (`useAmenitiesSection.ts:33-36, 86`). Adding `amenityIds.N` to `FIELDS` would hide the refusal silently.

**Fix:**
- for (a), (b) and (c), one test each, as described above;
- for (d), a confirm of a dated amenities or contacts group, checking the URL and the toast's section;
- for (e), a unit test of `amenitiesForm.ts`, and a "nothing changed" test per group;
- for (f), a 422 `{'amenityIds.0':['invalid_choice']}` expecting «لم يعد أحد المرافق…».

### 7. Should-fix: `spaces.md` *Web decisions* — labels collide, and older decisions no longer hold as written

**(a) Label collision.** #74 reuses the labels D2, D4, D5 and D6, which #57's decisions already carry. `docs/features/spaces.md:142` says "*Superseded 2026-10-13 by D6 below (#74)*", but #57's own D6 (the pin, :146) is also "below".
- **Fix:** point to it by name ("by #74's «Once added, the page opens the new space's editor»"), or drop the item labels from #74's lines.

**(b) Decisions stated as they no longer hold** (documentation.md: a decision is recorded as it holds today).
- `:140` "**No Edit or owners' items yet**" is now false for Edit; only a trailing clause says otherwise.
- `:133` ("An admin's write on a space fetches the whole admin scope again, and stays pending until it has arrived") is stated generally, as is the opening of `:36` ("a write fetches the whole admin scope again"). S3 (:156) now makes the editor's writes only mark the scope out of date.
- `:69` still says "until then every row's **items** wait", while :68 was changed to say Edit never waits.
- **Fix:** reword :140 to "No owners' items yet…", scope :133 and :36 to the row actions, and change "items" to "actions" at :69.

**(c) Plausible: D5 overstates the reuse.** `spaces.md:152` (D5) says "nothing in them is the admin's". Yet every section writes through `createSpacesRepository()`, hard-wired to `/admin/spaces/…`:
- `useProfileSection.ts:20`
- `useAmenitiesSection.ts:24`
- `useContactsSection.ts:20`
- `useConfirmGroup.ts:9`
- `useSpaceQuery.ts:7`

The query key is `['admin','spaces','space',id]`. It is plausible rather than certain, because D5 may mean the interface only.
- **Fix:** say the sections hold no admin-only interface but call the admin's endpoints until the owner's exist, or record it as a finding.

### 8. Nit: changing a contact's type leaves a contradictory error

**Where:** `hooks/contacts/useContactsSection.ts:137-139` sets the type without revalidating, and `errorOf` (111-120) words the old code by the new type.

**Scenario:** a WHATSAPP row holds `name@example.com`. Save shows "invalid number". Switching the type to EMAIL makes the helper read "Stored as name@example.com", while the error reads «بريد غير صالح» until the next keystroke.

**Fix:** pass `shouldValidate: formState.isSubmitted`, as `useProfileFields` does for the pin.

### 9. Nit: a save landing while the leave dialog is open cancels the navigation the admin asked for

**Where:** `hooks/editor/useLeaveGuard.ts:33-36`.

**Scenario:**
1. Save is pending.
2. The admin clicks a sidebar item, and the dialog opens.
3. The save lands, the dirty flag clears, `blocker.reset()` runs, the dialog vanishes, and the admin stays.

While the save is in flight, the dialog also says the changes "will be lost", which is untrue.

**Fix:** `proceed()` there, since nothing is left to lose, or disable the sidebar question while a save is pending. The owner's call.

### 10. Nit: the section in view stops following the scroll after a 403 turns the page read-only

**Where:** `hooks/editor/useSectionInView.ts:18-42`.

**Scenario:** the `ReadOnlyCard`s mount with the same ids, so `key` is unchanged and the effect does not re-run. The observer keeps watching the detached `SectionCard`s, so the wide list's `aria-current` no longer moves.

**Fix:** add `readOnly` to the effect's dependencies, or register the sections by callback refs.

### 11. Nit (latent): the editor's state is not reset when `spaceId` changes

**Where:** `pages/dashboard/admin/SpaceEditPage.tsx:36`.

**Scenario:** the same element is reused for `/spaces/1` → `/spaces/2`. With space 2 cached, a dirty form is never reset (the follow-effect runs only on a clean one), so "Leave" would show space 1's edits as space 2's, and Save would send them there.

No UI path leads from one editor straight to another today. D5's owner reuse (with its space switcher) would open one.

**Fix:** `<SpaceEdit key={spaceId} spaceId={spaceId} />`.

### 12. Nit (plausible): the old space's name can paint for a frame on the next page's top bar

**Where:** `shared/routing/title/useRecordTitle.ts:15-21` uses `useEffect`. Route changes commit in a transition, so the list's `PageHeader` can paint with the record title still set before the cleanup clears it. `document.title` is not affected.

**Fix:** `useLayoutEffect`.

### 13. Nit: stale lines after Discard or confirm

**Where:** `hooks/editor/useSectionFrame.ts:75, 103`.

**Scenarios:**
- `unchanged` is never cleared: "nothing changed" → edit → Discard brings the note back, though nothing was saved.
- `form.failure ?? confirmFailure.view` keeps a save's section-level failure (such as no connection) after Discard and after a successful confirm.

**Fix:** clear both on discard and on a confirm's success.

### 14. Nit: each write marks the answer it has just stored as out of date

**Where:** `hooks/editor/useSpaceAnswer.ts:17-18`. `setQueryData` runs, then `invalidateQueries(['admin'], refetchType 'none')`, which also matches `['admin','spaces','space',id]`. The next focus refetches the fresh answer. It also feeds finding 3.

**Fix:** invalidate first, then set the data, or exclude the space's key with a predicate.

### 15. Nit: adding a space now also waits on refetching every cached editor query

**Where:** `hooks/add/useCreateSpace.ts:22, 27`, via `useRefreshAdmin({ includeInactive: true })`. Its `refetchType: 'all'` on `['admin']` now covers each `['admin','spaces','space',id]` still in the cache (5 min `gcTime`), so "Add" stays pending on N extra GETs.

**Fix:** a predicate that skips the space keys.

### 16. Nit: Remove stays enabled while a save is pending

**Where:** `components/amenities/AmenitiesSection.tsx:61-69` and `components/contacts/ContactsSection.tsx:69-77`. The inputs, the Select and Add are disabled while a save is pending; Remove is not. A row removed mid-save comes back silently with `reset(answer)`.

**Fix:** disable Remove with `form.isPending`.

### 17. Nit: duplicate React key in the read-only amenities

**Where:** `components/amenities/ReadOnlyAmenities.tsx:30` uses `key={name.text}`. In English, two own amenities may share an `nameEn`, since only `nameAr` is unique.

**Fix:** key by `nameAr` or by index.

### 18. Nit: a mixed 422 on the amenities loses the `amenityIds` error, and the line names no amenity

**Where:** `shared/forms/services/applyServerError.ts:22` returns `null` once any field was placed. A 422 carrying both `ownAmenities.N.nameAr` and `amenityIds.M` drops the second. When it is alone, «لم يعد أحد المرافق…» does not say which amenity, and the checklist still shows it as active (the lookups list is not refetched).

**Fix:** on this 422, refetch the admin amenities list so the retired one shows its «غير نشط» badge.

### 19. Nit: `beforeunload` calls only `preventDefault()`

**Where:** `hooks/editor/useLeaveGuard.ts:24-26`. Chrome before 119 needs `event.returnValue = ''` as well.

**Fix:** set both.

### 20. Nit: test titles and test data

- `services/updatedAgo.unit.test.ts:17`: `'says %s was %s: %s'` reads "says 2026-10-02T06:00:00Z was ar: قبل 11 يومًا" (rule 6). **Fix:** `'%s in %s is %s'`.
- `SpaceEditor.component.test.tsx:266`: "…discards them, while a confirmation waits" never checks that the confirmation returns after Discard.
- `pages/dashboard/routes.component.test.tsx:562-568`: the add-flow test answers `GET /admin/spaces/7` with `ok([])`. It passes only because the 30 s `staleTime` prevents a refetch. **Fix:** assert that no `GET /admin/spaces/7` was sent; that proves the seeded space.
- `AmenityNames.component.test.tsx:29`: an unused `data-testid`.

### 21. Nit: document details

- `spaces.md:59` "Save stays enabled": except while a 429 counts down (`SectionCard.tsx:50`).
- `spaces.md:150`: a stray blank line splits the *Web decisions* list in two.
- `lookups.md:97-98`: #74's decisions sit between #57's lines.
- `spaces.md:173`: the code map names a file (`hooks/useProfileFields.ts`), against documentation.md's "folders and entry points only". It also lists `confirm/` as a folder in `components/`, where none exists.
- `lookups.md:97`: "the owner's page will set a field over the catalogue" states unbuilt intent in a Description-class document.
- The retired-amenity rule is stated at `lookups.md:63` and `:97`, and restated at `spaces.md:160`. The last one could link to it instead.

---

## Checked and fine

- **Scope:** only `apps/web` and `docs` changed (106 files). Nothing in `apps/api` or `packages/shared`; no dependency.
- **Commits:** six, with subjects of 46, 45, 48, 38, 46 and 47 characters (counted). #70 is in its own commit. No tool attribution.
- **Requests match the contract:**
  - `GET` and `PATCH /admin/spaces/:id`
  - `PUT …/amenities` with `{ amenityIds, ownAmenities }` (`nameEn` blank → `null`)
  - `PUT …/contacts` with `{ contacts }`
  - `POST …/{group}/confirm` with no body
  - PATCH sends only the changed fields, a cleared optional as `null`, and never an unchanged area.
- **Contacts:** the stored form and the validation come from `@masaha/shared/spaces` (`normaliseContact`, `updateSpaceContactsSchema`), with no copy in the web. `carrierOf` reads E.164 `+97059` / `+97056`. A repeat is refused on the later row.
- **Server field errors:** `contacts.N.value`, `ownAmenities.N.nameAr|nameEn` and the profile's fields land on their fields, and the first takes the focus.
- **403 on a write:** refetches the space and turns the page read-only. The sections unmount, so no dirty flag is left behind.
- **Sections stay independent:** each has its own form, mutation and failure. A clean section follows the server's data (each `savedKey` holds only its own group); a dirty one keeps its edits.
- **The leave guard:**
  - `useBlocker` is used with the documented `{ currentLocation, nextLocation }` function and is removed on unmount.
  - A same-path move is never blocked.
  - Escape counts as Stay, and «البقاء» holds the focus.
  - The add page's landing has no blocker in its way.
  - `beforeunload` is added only while dirty and removed on cleanup.
- **The record title:**
  - `RecordTitleProvider` in `RootLayout` is its one owner, read by both `PageHeader` and `DocumentTitle` through `usePageTitle`.
  - The route's title shows while the space loads.
  - It is marked `lang`/`dir` only when the name's language differs from the interface's.
  - It follows a language switch and is cleared on unmount.
  - `PageHeader` falls back to the wordmark, so no empty `h1` (#70).
- **The verified space:** the Alert reads «يعدّلها مالكها» with no owner name (finding 59, the owner's Q1 (b)), with «عرض في الموقع». No unlink, as Q1 (b) defers it to the owners item. There is no form and no Save.
- **Checklist and sections:** «ما زال ناقصًا» lists the five groups, links only drawn sections, and is gone once nothing is missing. Hours, prices and photos are absent, not "coming soon". Each section's date, «قديمة», «لم تُضف بعد» with Save only, and «تغييرات غير محفوظة» behave as decided.
- **Entry points:** «تعديل» is first in the row menu and never waits on a 429. The 429 route test's narrowing to Hide/Delete is the design (`spaces.md:68, :164`), and Edit's not waiting is proven in `SpaceActionsMenu.component.test.tsx`. The space's name links to the editor. The add page lands on the seeded editor, recorded as D6 superseding #57's D2, with its date and reason.
- **Design system and localisation:**
  - semantic tokens only, no physical direction classes, no arbitrary values;
  - matching Arabic and English keys for every new string;
  - contacts, coordinates and stored forms are `dir="ltr"` / isolated, and own amenities' names carry `lang`/`dir`;
  - `updatedAgo` counts in Gaza's days with Western digits.
- **Documents:**
  - the code-map paths exist;
  - findings 59 and 60 follow the format, are indexed once under Open, and 60 matches the code (the Select gets an id with no item, so it shows nothing);
  - architecture §2's *Titles* matches the code;
  - the overview's *Built* line does not overclaim;
  - no `#PRNUM` is left.
