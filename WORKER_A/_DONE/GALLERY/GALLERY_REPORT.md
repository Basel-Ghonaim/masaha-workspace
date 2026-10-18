# GALLERY — report, part 1 (the four commits)

**Facts only, as of the end of this session.** The head is `b40a69b8` on
`feat/space-gallery`, cut from `origin/main` @ `93f152fe` (PR #84 merged; PR #82 merged).
**62 files changed, 2692 insertions(+), 111 deletions(-)** — under the prompt's 70.
The push, the PR, CI/`CLEAN`, the real run on 5320/3320 and the conflict check have **not**
happened yet.

---

## 1. The four commits

| # | Subject | Length | SHA |
|---|---|---|---|
| 0 | `fix(space-links): correct the deleted spaces list` | 49 | `c4a5a730` |
| 1 | `feat(web): add a shared image upload layer` | 42 | `91524abc` |
| 2 | `feat(spaces): add the editor's gallery` | 38 | `82a1259c` |
| 3 | `feat(spaces): upload photos in the gallery` | 42 | `b40a69b8` |

The four subjects match §11's table, in the plan's order, commit 0 first.

**Commit 0 (§14).** `hooks/admin-list/useAdminSpacesFilters.ts` — `applied` counts the place and
the state only; `clearFilters` writes `{ place: null, status: undefined }`, keeping the search and
the chip; `anyApplied` counts and `clearAll` clears everything. `services/rowView.ts` — a deleted row
has `state: []` and `freshness: []`, its status one muted line from `deletedOn`. `AdminSpacesList.tsx`
— the deleted row's status cell is that line, its freshness cell a muted «—» with `aria-hidden`;
`AdminSpaceCard.tsx` — the card's one line, no badge list. Catalogues — `deletedOn` →
«Deleted · ${date}» / «محذوفة · ${date}», `staleOrMissing` → «قديمة أو ناقصة» (Arabic),
`spaces.deleteDialog.description` → the design's «وتجدها في «محذوفة» لاسترجاعها» /
"It leaves the site and the list; you'll find it under «Deleted» to restore it.".
`services/updatedOn.ts` — the comment says "a row's date". Documents — `space-links.md` (line 67
"counts the sheet's own two fields"; line 72 rewritten for the muted line and the "no screen yet"
sentence; "stale or missing" in line 102; the freshness decision's wording; the #84 PRs on the
decision and history lines; finding 50 dropped from *Open findings*; finding 69 linked in its
place), `spaces.md` (the delete-dialog decision amended, the Restore-in-Actions correction,
"stale or missing" in two places, the #85 history line), `data-model.md` (line 85), findings 44 and
50 resolutions, findings 69, the index, the two headers' dates. Files: 21 (20 listed + the folded
`useAdminSpacesFilters.component.test.tsx`).

**Commit 1.** `shared/uploads/**` — `index.ts`, `types/UnsupportedImageError.ts`,
`services/photoGeometry.ts` (`fitInside`, `SHRINK_DEFAULTS`), `services/shrinkImage.ts`,
`services/sendMultipart.ts`, `services/canRetryUpload.ts`, their three unit tests and one component
test, and `src/test/fakeCanvas.ts`. Files: 11.

**Commit 2.** The gallery: `spacesRepository.ts` + test, `queryKeys.ts` (`photos`),
`types/PhotoTileView.ts`, `types/PhotoGalleryView.ts`, `hooks/photos/{usePhotosQuery,
usePhotoOrder,usePhotoRemove,usePhotoGallery,useReadOnlyPhotos}.ts` (+ two component tests),
`components/photos/{PhotosCard,PhotoTile,PhotoRemoveDialog,PhotosSection,ReadOnlyPhotos}.tsx` +
test, `SpaceEditor.tsx` and its test, `useSpaceEditor.ts`, the two `spaces.ts` catalogues.
Files: 23.

**Commit 3.** `hooks/photos/usePhotoUploads.ts` + test, `components/photos/PhotoUploadTile.tsx`,
`types/PhotoTileView.ts` and `types/PhotoGalleryView.ts` (the pending states and `uploads`),
`usePhotoGallery.ts`, `PhotosSection.tsx` + test, `useLeaveGuard.ts` + test, `useSpaceEditor.ts`,
`SpaceEditor.tsx`, the two `spaces.ts` catalogues, `docs/features/spaces.md`,
`docs/frontend/architecture.md`, `docs/project/overview.md`, findings 73 and 74 and the index.
Files: 20.

---

## 2. The red runs, per commit

### Commit 0 — the tests were written first and each was seen failing

* `rowView.unit.test.ts` — 11 passed, 1 failed:
  * `rowView > says when a deleted space was deleted in one muted line, and shows no badge of its own`
    — `AssertionError`: `english(deleted)` received `{ deletedOn: "Deleted on 1 Oct",
    freshness: [{label:"Up to date",variant:"success"}],
    state: [{label:"Verified",variant:"success"},{label:"Deleted",variant:"neutral"}] }`
    against `toMatchObject({ state: [], freshness: [], deletedOn: "Deleted · 1 Oct" })`.
* `AdminSpacesList.component.test.tsx` — 20 passed, 3 failed:
  * the deleted row's cells: `AssertionError: expected [ 'Olive Desk', 'Deir al-Balah', …(5) ] to
    deeply equal [ … 'Deleted · 1 Oct' … ]`;
  * the card's text: `expected 'Olive DeskDeir al-Balah · Owner: ⁨Rima⁩ · 12 SeptVerifiedDeleted
    Up to dateDeleted on 1 OctRestore Olive Desk' to be 'Olive Desk…Deleted · 1 OctRestore Olive Desk'`;
  * the sheet's button: `TestingLibraryElementError: Unable to find an accessible element with the
    role "button" and name "Filters, 1 applied"`.
* `useAdminSpacesList.component.test.tsx` — 11 passed, 2 failed:
  * `offers the contract's four states and the count of filters applied for the phone's button` —
    `AssertionError: expected { text: 'Filters', …(6) } to match object { text: 'Filters', …(2) }`
    (`count: 2` → `1`, `label: 'Filters, 2 applied'` → `'Filters, 1 applied'`);
  * `keeps the rows already shown busy while another status loads` — `AssertionError: expected 'noMatch'
    to be 'empty'` (the assertion was mine; the list was right to say no-match with a filter applied.
    It was corrected to `expect(result.current.list.rows).toEqual([])`).
* `SpaceActionsMenu.component.test.tsx` — 17 passed, 1 failed:
  * `asks before deleting, opening on Cancel, its title naming the space` —
    `TestingLibraryElementError: Unable to find an element with the text: It leaves the site and the
    list; you'll find it under «Deleted» to restore it.`
* One further red after the code: `useAdminSpacesList.component.test.tsx:308` —
  `AssertionError: expected 'Deleted · 1 Oct' to be 'Deleted on 1 Oct'` (an existing assertion the
  catalogue change moved; corrected by hand).

After the fixes the three files were green (`rowView` 79 unit tests in its folder; 54 component
tests in the three files).

### Commit 1 — the tests were written first; the code did not exist

* `photoGeometry.unit.test.ts`, `canRetryUpload.unit.test.ts`, `sendMultipart.unit.test.ts` —
  three suites failed to collect: `Error: Cannot find module './photoGeometry' imported from
  …/services/photoGeometry.unit.test.ts` (and the same for `./canRetryUpload`, `./sendMultipart`);
  `Tests no tests`.
* `shrinkImage.component.test.tsx` —
  `Error: Failed to resolve import "../types/UnsupportedImageError" from
  "src/shared/uploads/services/shrinkImage.component.test.tsx". Does the file exist?`;
  `Tests no tests`.
* After the code: unit 22 passed (3 files), component 4 passed (1 file).

**The deliberate break.** With the code in place I changed `imageOrientation: 'from-image'` →
`'none'` and `maxSide: 1600` → `4096`, ran both lanes, then restored them:

| lane | result |
|---|---|
| component | 2 failed — `re-encodes a photo turned as its EXIF says, at 1600 px on its longest side, as JPEG at 0.85`; `refuses a photo the browser cannot write out` |
| unit | 22 passed — the geometry test proves `fitInside` itself with numbers written by hand, and never reads `SHRINK_DEFAULTS`, which is what §9 row 6 asks for |

### Commit 2 — the tests were **not** seen failing against absent code

The hook and component files were written before the tests were run, so there was **no red run** for
the new tests of this commit. The first run after both were in place gave 12 passed, 4 failed, and
all four failures were defects in my own test expectations, not in the code:

* `usePhotoOrder.component.test.tsx` — 3 failed:
  * `sends every photo's id in the order the admin chose…` — `AssertionError: expected [ { ids: [ 3, 5, 4 ] } ]
    to deeply equal [ { ids: [ 4, 5, 3 ] } ]` (the correct order was `[3,5,4]`);
  * `says the gallery changed and shows the server's order when it refuses the move (409)` —
    `AssertionError: expected AppError: Fake refusal { …(6) } to be null` (my assertion of `refusal`
    was wrong: a 409 is the gallery's own news, not a tile failure);
  * `fetches the space again when the write is refused as verified (403)` —
    `AssertionError: expected false to be true` (no cache entry existed for a key with no observer;
    the assertion was changed to seed the key and read `state.isInvalidated`);
* `usePhotoRemove.component.test.tsx` — 1 failed, the same `expected false to be true` on the same
  pattern.
* The first `PhotosSection.component.test.tsx` run had no failures beyond those (9 passed, 1 failed
  later on a `FileList` stub — see §4).

### Commit 3 — the tests were written first and were seen failing

* `usePhotoUploads.component.test.tsx` — 5 passed, 2 failed on the first run:
  * `uploads chosen files one at a time, in the order chosen, each with its own progress` —
    `AssertionError: expected [ 'one.jpg', 'two.jpg' ] to deeply equal [ 'one.jpg' ]` (both files had
    gone up: the first answered immediately, so the loop went on to the second; the test was changed
    to hold the *first* request open and assert the second had not been sent);
  * `uploads what fits and says how many of the selection went up` —
    `AssertionError: expected true to be false` (`canAdd` was true: the hook had received the static
    `photos` array while the query was still pending; the test was changed to read the gallery through
    `usePhotosQuery`, as the section does).
* `usePhotoUploads.component.test.tsx` — one more failure later, `tells the editor while a file is
  being prepared or sent, and once the queue has ended` —
  `AssertionError: expected false to be true` at `expect(uploading.at(-1)).toBe(true)`: the unmount
  cleanup ran on every render because the test's callback identity changed (see §4, item 8).
* `PhotosSection.component.test.tsx` — 9 passed, 1 failed:
  * the first `chooseFiles` attempt —
    `TypeError: Cannot set property length of #<FileList> which has only a getter`;
  * after that was fixed —
    `TestingLibraryElementError: Unable to find an element with the text: Preparing…` (the tile had
    already moved on to "Uploading 0%"; the assertion became
    `getByRole('status', { name: /Uploading \d+%/ })`).

After those corrections: `usePhotoUploads` 7 passed, `PhotosSection` 10 passed, the two leave-guard
and editor files green.

---

## 3. Every check and lane run, with its result

Per commit, on that commit's head:

| check | commit 0 | commit 1 | commit 2 | commit 3 |
|---|---|---|---|---|
| `npm run check:links` | 2070 links in 156 documents and 1156 source files all resolve | — | — | 4 broken links, then 2087 links in 158 documents and 1185 source files all resolve |
| `npm run lint` | clean | 5 errors, then clean | clean | 9 errors, then 6, then clean |
| `npm run typecheck` | clean | 1 error, then clean | 5 errors, then clean | 4 errors, then clean |
| `npm run format:check` | 2 files failed, then clean | 11 files failed, then clean | clean | 7 files failed, then clean |
| `npm run check:classes` | — | — | No physical direction or arbitrary-value classes in 820 files | No physical direction or arbitrary-value classes in 823 files |

On the head, after commit 3 and after the commit-0 fold:

| lane | result |
|---|---|
| `npm run test:unit` | **78 files, 818 tests passed** |
| `npm run test:component` (1st full run) | **1 file failed, 2 tests** — `useAdminSpacesFilters.component.test.tsx`; 146 files passed |
| `npm run test:component` (2nd full run) | **1 file failed, 1 test** — `src/pages/dashboard/routes.component.test.tsx`; 146 files passed |
| `npm run test:component` (3rd full run) | **147 files, 980 tests passed** |

`npm run test:component` takes about 6 minutes on this machine. `npm run test:api` was **not** run,
by §12.3 (nothing in `apps/api` or `packages/shared` changes; CI runs it).

Not yet run on the head: `NODE_ENV=production npm run build`, `npm run check:build`. Not yet done at
all: the push, the PR, CI/`CLEAN`, the conflict check, the real run.

---

## 4. The two failures under load, and each alone

**1. `src/features/space-links/hooks/admin-list/useAdminSpacesFilters.component.test.tsx` — 2
tests, in the first full component run.**

* `useAdminSpacesFilters > writes each filter chosen to the address, back on the first page` — the
  test asserted `filters.applied` was `3` for `?status=hidden&governorate=2&stale=true`; commit 0
  changed the sheet's count to its own two fields.
* `useAdminSpacesFilters > clears the filters in the phone's sheet, keeping the search` — the test
  asserted the sheet's clear left `?q=Hub`; commit 0 keeps the stale chip, so it leaves
  `?q=Hub&stale=true`.

**This was a real miss in commit 0's verification.** The plan's §14 named two test files for R84-001
(`AdminSpacesList.component.test.tsx` and `useAdminSpacesList.component.test.tsx`); the third file,
which tests the filters hook directly, was not in my list and was never run while writing commit 0.
Both tests were corrected by hand (the titles now say the sheet's own two fields, and the second
asserts `?q=Hub&stale=true`), and the change was **folded into commit 0** with
`git commit --fixup 98c87c26` + `$env:GIT_SEQUENCE_EDITOR=':'; git rebase -i --autosquash
origin/main`. The history is now four commits again, with `c4a5a730` at the bottom.
Alone afterwards: `src/features/space-links` → **6 files, 65 tests passed**.

**2. `src/pages/dashboard/routes.component.test.tsx` — 1 test, in the second full component run.**

* `the dashboard's navigation > lists the owner's eleven pages, the overview marked as the page
  shown`.

The file does not appear in this item's §7 file list; the branch touches no routes. It passed
**alone**: 36 tests passed in 23.7 s. The next full run was green (147 files, 980 tests), so it is
recorded as a flake under load (finding 28 is the project's own note on such tests). Nothing was
changed for it.

---

## 5. Every problem met, and how it was solved

1. **`git commit -F` took the file's first paragraph as the subject.** Commit 0's first attempt had
   the whole paragraph as its subject line. Amended with the subject on the first line of the file:
   49 characters.
2. **lint — `axios` is restricted to `shared/api`.** `sendMultipart.ts` and
   `sendMultipart.unit.test.ts` imported `AxiosProgressEvent` from `axios`. The production file now
   declares its own `ProgressEvent = { loaded: number; total?: number }` (a supertype Axios's event
   satisfies); the test's `serve` callback declares the full shape
   `{ loaded; total?; bytes; lengthComputable }`, which `InternalAxiosRequestConfig` accepts.
3. **lint — `require-await` on the fake canvas's stubs.** `vi.fn(async …)` became
   `vi.fn(() => Promise.resolve(…))` / `vi.fn(() => Promise.reject(new Error(…)))`.
4. **lint — `no-unnecessary-type-conversion`.** `` `encoded ${String(type ?? '')}` `` dropped the
   conversion.
5. **typecheck — the unit test's `serve` parameter was narrower than `InternalAxiosRequestConfig`.**
   Declared the progress event with `bytes` and `lengthComputable` too (see item 2).
6. **typecheck — `Property 'data' does not exist on type 'never'`.** `query.error === undefined`
   narrowed TanStack Query's union to nothing, because its success variant carries `error: null`.
   Both gallery hooks now use `query.isSuccess`.
7. **lint — `react-hooks/refs`.** `queue.current` was read during render (the tiles map and the
   `full` flag), and `guard.current = onUploadingChange` was assigned during render. The tiles and
   `full` are derived from the `items` state; the ref is assigned inside an effect, and the
   unmount-only effect reads the callback through that ref so its identity cannot fire it.
8. **A test's flapping `onUploadingChange`.** With a fresh callback identity per render the
   unmount cleanup fired `false` on every render, so the last told value was `false`. Solved by the
   ref-in-an-effect pattern above; the real app passes a `useCallback`, so this only bit the test.
9. **lint — `no-confusing-void-expression`.** `AlertDialog`'s `onOpenChange={(open) => (open ?
   undefined : dialog.cancel())}` now uses braces: `onOpenChange={(open) => { if (!open)
   dialog.cancel(); }}`.
10. **Test helper — `Object.assign` on a `FileList` prototype object.**
    `TypeError: Cannot set property length of #<FileList> which has only a getter`. Replaced with
    `Object.create(FileList.prototype)` + `Object.defineProperties` for `length`, `item` and
    `[Symbol.iterator]`.
11. **`Spinner` requires a `label` and is itself `role="status"`.** A pending tile's own
    `role="status"` wrapper was removed; the `Spinner` carries `label={waiting}` (the layer's own
    name), and the visible text beside it is `aria-hidden` so the same words are announced once.
12. **`getByLabelText('Add photos')` in the section test.** The sr-only input's `aria-label` is the
    same string as the button's text, and only the input is labelled, so the input is found — as the
    test wanted. No change needed.
13. **A 409 read as a tile failure.** `usePhotoOrder` first kept the `AppError` of a conflict, so a
    409 would have put a failure line on a tile; `refusal` is now `null` when the type is
    `conflict`, and the 409 speaks through the `orderChanged` announcement (§4.4's "A move or a cover
    landed" line).
14. **The queue's room counted failed tiles.** `PHOTO_LIMIT - photos.length -
    waitingOn(queue.current)` now counts only the items that are not `failed` — a refused file keeps
    its tile but needs no room, and a queued one still does.
15. **`check:links` — 4 broken links in the two new findings.** The relative depth from
    `docs/architecture/findings/` was wrong (`../../../design/…` → `../../design/…`,
    `../../../architecture/documentation.md` → `../documentation.md`). Corrected; the check then
    printed 2087 links in 158 documents and 1185 source files all resolve.
16. **A dense, duplicated tile build in `usePhotoGallery`.** The first draft built the removal tile's
    object inline with the label computed twice. Refactored to build the tile, then spread it into the
    actioned copy — one label, one place.
17. **The section's own load failure** showed the section title instead of the refusal's line.
    `useRefusalView`'s view now supplies `failure.message` (or the section's title when there is no
    view), which keeps the shared reader and shows the refusal's line with its reference.

---

## 6. Departures from the plan

1. **Commit 2's new tests were never seen failing against absent code.** The hooks were written
   before their tests were run. Commit 0, commit 1 and commit 3 each had a red run; commit 2 did not.
   The four failures it did produce were defects in my own expectations (§2, commit 2).
2. **`types/PhotoTileView.ts` gained an `id` field** (the plan's type keyed a tile by `photo-<id>`
   with no id field). Without it the removal would have to parse the key back into a number.
3. **The pending tile is its own view type, not one unified `PhotoTileView`.** §4.2 describes one
   type with `state`, `progress`, `fileName`, `retry` and `drop`. I kept `PhotoTileView` as committed
   in commit 2 (stored photos) and added `PhotoUploadTileView` beside it, so the stored tile's shape
   did not grow nulls. §7's commit-3 list also did not name `types/PhotoGalleryView.ts`; the
   `uploads` field and `PhotoUploadView` were added there in commit 3.
4. **`PhotoGalleryView` has no `order` field** (§4.2 lists one in the return). The order's actions
   ride on the tiles, so no component would have read it; returning it would have been dead shape.
5. **`toasts.photoRemoved`, `photos.verifiedMeanwhile` and `photos.deletedMeanwhile` are in commit 0
   and commit 2**, not in commit 3 as §11's copy list has them. Criterion 6 needs the 403/404 lines
   in commit 2 with the removal and the order, and the removal's toast is needed by `usePhotoRemove`
   there. **`photos.choose` and `photos.limitReason` are in commit 3**, which §11's list does not
   name, because the picker renders there and an unused catalogue line is not one this item should
   ship.
6. **Commit 0 also added a line to `space-links.md`'s *Open findings* for finding 69 and one Web
   history line for #85**, and changed lines 123/124's "*Superseded 2026-10-15 by the deleted-spaces
   screen, below.*" to "by #84's decisions, below." §14 named only the decision and history date
   lines; these are the same PR, named in the same place.
7. **Commit 0's third test file.** §14's R84-001 row named two tests; `useAdminSpacesFilters.component.test.tsx`
   was missed, failed in the first full component run, was corrected and folded into commit 0 (§4,
   item 1).
8. **Findings recorded: 69, 73, 74.** Finding 70 is **not** recorded: §14 asks for it only if the
   real run reproduces a verified row with no owner, and the real run has not happened. Finding 63
   and finding 64 stay open and untouched, as §6 asks.
9. **The docs' new decision lines end `2026-10-17, #85`** (the owner's amendment 4), and the #84
   corrections end `2026-10-15, #84`. The PR number was confirmed before any document named it:
   `gh api "repos/Basel-Ghonaim/masaha/issues?state=all&per_page=1" --jq '.[0].number'` printed
   `84`, and `gh pr list` printed `[]`.
10. **The plan's §12.1 step 1 said to read code in `C:\Users\basel\masaha-design`.** The executor's
    instruction says to work in `C:\Users\basel\masaha` and never in a design worktree, so every read
    was from `git show origin/main:<path>` and the working tree in `C:\Users\basel\masaha`.
11. **`usePhotoGallery(spaceId, onUploadingChange)` and `PhotosSection({ spaceId, onUploadingChange })`**
    take the editor's callback, as §4.2 describes (`onUploadingChange` on the hook), rather than the
    gallery owning the boolean. The plan's `usePhotoUploads` signature (`onUploadingChange` third)
    is unchanged.
12. **`docs/frontend/architecture.md`'s shared-module list and §7's multipart line are two additions**
    (§7 says "Two lines, no more"): one bullet in §4 for `shared/uploads` and one bullet in §7 for the
    multipart rule. The §4 bullet is one line.

---

*Part 2 of this report — the scope check, the push, the PR, CI/`CLEAN`, the conflict check and the
real run — is owed when those happen.*
## Part 2 — the resumption

**Resumed by:** OpenCode, 2026-10-17, from `b40a69b8` on `feat/space-gallery`. The required resume state was confirmed: `git rev-parse --short HEAD` returned `b40a69b8` and `git status --short` was empty. The four existing commits were not rewritten or re-tested.

### Build checks

- `$env:NODE_ENV='production'; npm run build` — passed. Vite transformed 3974 modules and produced the production bundles.
- `npm run check:build` — passed: no showcase code, dashboard code, data-table or Leaflet code in the site's first download.

### Real run

Docker Desktop was already available; `docker start masaha-postgres-1` succeeded. `npm run db:migrate` reported no pending changes, and `npm run db:seed` completed. A disposable seeded admin was used for the browser run; the API health check reported `{"status":"ok","db":"up"}` on port 3320 and the web responded on port 5320.

- **Unverified space:** created `Gallery Test Space` through Add space, reached the empty gallery, uploaded two JPEGs serially, confirmed each stored tile and the cover state, moved the cover with «Make it the cover», and observed the live announcement. The initial Arabic RTL phone screenshot and the two-photo gallery screenshot were saved.
- **HEIC:** `IMG_8901.HEIC` reached its own pending tile and ended with «Unsupported format; choose JPEG, PNG or WebP». No request was sent. Screenshot saved.
- **Renamed invalid `.jpg`:** the browser decoder rejected `gallery-invalid.jpg` before the API, so the server-side 415 path was not exercised; the tile showed the same unsupported-format refusal and no request.
- **Removal:** opened the named destructive AlertDialog, verified Back had focus, and cancelled it. Screenshot saved.
- **Verified space:** opened seeded `Demo Space` (space 7). Its gallery showed the empty state and no upload, reorder, cover or remove controls. Screenshot saved.
- **Languages, directions, themes and widths:** exercised Arabic RTL and English LTR, light and dark, at 360, 768 and 1440 widths. Screenshots are in `C:\Users\basel\Downloads\gallery-shots\`.
- **Finding 70:** not reproduced. The verified seeded row showed owner `أحمد الشوا`; no verified row with a missing owner was observed, so finding 70 was not recorded.
- **Not exercised:** sustained mid-upload disconnect and retry, filling to ten and an over-limit selection, portrait EXIF-6 phone photo, active-upload navigation/reload prompts, screen-reader output, and a server-side 415. The local uploads completed too quickly for the disconnect/leave-guard cases, no EXIF-6 phone source was available, and the invalid image was refused by the browser before the API. Production Cloudinary was not exercised; finding 64 remains open. Prices at 768 px were visually checked and showed no gallery-induced width pressure.

Both dev servers were stopped by their listening PIDs, and ports 3320 and 5320 were confirmed free. Screenshots were moved to `C:\Users\basel\Downloads\gallery-shots\`; the repository remained clean and no screenshot was staged.

### Push, PR, CI and conflicts

The branch was pushed with `git push -u origin feat/space-gallery`. Pull request **#85** was opened as `feat(spaces): add the editor's gallery` with labels `feat`, `area:web`, `area:docs`, assigned to `@me`. CI passed on the pushed head: `build`, `check:classes`, `check:links`, `format:check`, `lint`, `test:api`, `test:component`, `test:unit`, and `typecheck`. GitHub reports `mergeStateStatus: CLEAN`, `mergeable: MERGEABLE`, and the PR remains open and unmerged. There were no other open PRs, so the conflict check had no other heads to compare.

### Departure

The previously recorded departures remain unchanged: commit 2's tests were not seen failing against absent code; the report's Part 1 records the other test-first breaks, the additional `id` and pending-tile view types, the omitted dead `order` field, catalogue placement differences, and the real-run limitations above. No code defect was fixed during the resumption, and no finding 70 file was added.

## Review fixes

**Head:** `4f5bc294` on `feat/space-gallery`, CI green on it, PR CLEAN. Rebased once on `origin/main` (GitHub showed a conflict after the first push): one conflict, the *Last Updated* line of `docs/project/overview.md`, kept the later date (2026-10-17). Comment "Review fixes" posted on #85.

**Commits (subject lengths):** `c977137b` fix(web): harden the shared upload layer (40) · `1a355404` fix(space-links): hide an empty badge list (42) · `4f5bc294` fix(spaces): correct the gallery after review (45).

### Fixes and their red lines (new tests, seen failing with the production change stashed)

| # | Test | Red line |
|---|---|---|
| 1 | PhotosSection: keeps the removal dialog open and says why | no text /went wrong on our side/ |
| 2 | PhotosSection: takes a second move only after the first is answered | `expected [3 requests] to have a length of 2 but got 3` (two PUTs); the arrows test: `aria-disabled` absent |
| 3 | sendMultipart: own, longer timeout | `expected 15000 to be 120000` |
| 4 | usePhotoUploads: counts what went up when the batch ends; PhotosSection: announces… | `'Uploaded 1 of 2…' to be 'Uploaded 0 of 2…'` |
| 5 | usePhotoUploads: stops the queue when left; sendMultipart: hands the signal | `expected undefined to be true` (not aborted); `expected undefined to be AbortSignal` |
| 6 | usePhotoRemove: 404 fetches the gallery; forgets a failed removal | `expected false to be true`; `expected AppError… to be null` |
| 7 | PhotosSection: cover buttons named; upload 409 says full | no button "Make Photo 2 the cover"; no text "The space already has 10 photos…" |
| 8 | PhotosSection (verified): names each photo | no img named "Photo 1" |
| 9 | PhotosSection: refused order in view; usePhotoOrder 409 | `not.toHaveClass("sr-only")` failed; `expected undefined to be 'The photos changed…'` |
| 10 | shrinkImage: transparent photo on white | `expected null to be '#ffffff'` |
| 11 | PhotosSection: «Add photos» available while uploading | `toBeEnabled` failed |
| 12 | PhotosSection: says the upload failed | no text "We couldn’t upload this photo" |
| nit | AdminSpacesList phone card: no empty badge row | `expected <span> to be null` |

Assertions added where the fix touched a planned claim, already green before the fix: refetch after a removal, the removal toast and closed dialog. The leave-guard default is a type-level change with no test.

### Not done, and why

- **Review 6, the "That photo was already removed" line.** The review's premise is wrong: `photos.service.ts` `remove` writes nothing and answers 204 for an unknown photo (S4), and an order with a missing id is a 409. No photo-level 404 exists, so every 404 is the space and «حُذفت المساحة» is right. No line added.
- Not in the review's fix list and left alone: the mislabelled duplicate section test (13), the remaining test gaps in 13/14 that no fix touched (failed-tile rendering, 429 countdown, unmount-wiring from the section to the guard, the `SpaceEditor` section-order assertion), the removal and order failures still titled with `loadFailed` (a load sentence on a write failure), departure notes in 15, and the `onProgress` branch nit in 17.
- Unrequested but forced by 12: one new catalogue line, `uploadFailed`. Also `orderChanged` was reworded and `before`/`after` deleted, as asked.

### Run and not run

Run: the touched component and unit files focused (`src/features/spaces`, `src/features/space-links/components/admin-list`, `src/shared/uploads`, `src/shared/copy`), then `npm run lint`, `typecheck`, `check:classes`, `format:check`, `check:links` (also again after the rebase). Not run locally: full `test:unit`/`test:component`, `test:api`, `build`, `check:build`, a real browser run; CI ran all lanes green on `4f5bc294`.
