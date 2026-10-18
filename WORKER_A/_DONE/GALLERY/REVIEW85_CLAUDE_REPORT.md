# Review of PR #85 (GALLERY), by Claude

**Head reviewed:** `b40a69b83c2bae4c20a0e0921c48823f93c00bf8` (`feat/space-gallery`, base `93f152fe`). It had not moved when I finished (`gh pr view 85`: same `headRefOid`, CLEAN, CI green). Read-only, from commit objects. I ran no tests, builds or servers. Claims about runtime behaviour below come from reading the code. Where I did not see the behaviour happen, I say "plausible".

**Verdict: not ready to merge. Fix round on this PR first.** There are no blockers in the strict sense: nothing corrupts data, and the contract, scope and shared layer are sound. But five should-fix defects sit in the gallery's core flows (removal, reorder, upload on a weak link, the summary line, leaving mid-upload). Tests and the real run reach none of them, so CI being green says nothing about them.

---

## Part 1: the five most important findings

### 1. [should-fix, high] A failed removal is invisible: the dialog closes on Delete
`PhotoRemoveDialog.tsx:21-26,35` and `usePhotoRemove.ts:43-51`.

`AlertDialogAction` is Radix's `Dialog.Close`, so clicking it runs `onClick={dialog.confirm}` and then `onOpenChange(false)`, which calls `dialog.cancel()` and sets `target` to `null`. The dialog therefore closes at the click.

The failure line lives inside the dialog (`failure: removalFailure.view`) and the mutation's error is shown nowhere else. Scenario: the connection drops, or the server answers 500, when the admin presses Delete. The dialog closes, no toast fires, the tile stays, and nothing says why.

The claim in `usePhotoRemove`'s JSDoc ("A refusal keeps the dialog open with its reason") is false in the UI.

The hook test "keeps the dialog open and says why (403)" calls `confirm()` directly and asserts on `target`. It never goes through the dialog, so it proves a property the UI does not have. The real run only opened the dialog and pressed Back, so Delete was never exercised in a browser.

**Fix** (fix round): make the confirm button not close the dialog, with `onClick={(e) => { e.preventDefault(); dialog.confirm(); }}` and the dialog closing in `onSuccess`. Or keep it closing and show the failure on the tile or as a toast. Add a component test that clicks Delete against a refused transport and sees the line. Also add one against a success that sees the toast and the tile gone.

### 2. [should-fix, high] A second move or cover click acts on a stale list; the arrows also break AC 5
`usePhotoOrder.ts:44,58-64,67-101`, `PhotoTile.tsx:37-58`.

`onSuccess` calls `void client.invalidateQueries(...)`, so the mutation resolves before the refetch finishes. In that gap `isPending` is false, but `photos` is still the old order. `busy` only sets `aria-busy`, and nothing blocks the click.

Scenario: the admin presses "Before: Photo 3" and then, quickly or by keyboard repeat, "Before: Photo 2" (or double-clicks one button). The second `PUT` is computed from the old list, so it undoes or garbles the first. The server accepts any full permutation, so the wrong order is saved silently.

The plan says "no optimistic move"; this is the opposite problem, a move computed from a list the server has already changed.

AC 5 says the arrows are "`aria-disabled` at the boundary". The code uses the `disabled` attribute, and the test asserts `toBeDisabled()`. This breaks the AC and the documented project rule in `spaces.md` ("waits marked, not disabled… a disabled button leaves the focus order"). In practice: press "Before" on the second photo, it becomes first, its Before button turns `disabled`, and keyboard focus is lost.

**Fix** (fix round):
- `return client.invalidateQueries(...)` from `onSuccess` so the mutation stays pending until the refetch ends.
- Make every move, cover and remove control ignore clicks while `busy`, using `aria-disabled` plus a guard in `run`.
- Use `aria-disabled` at the edges.
- Add a test for two quick clicks, expecting one `PUT` with the right ids.

### 3. [should-fix, high] An upload has a 15-second ceiling that nothing raises
`sendMultipart.ts:34`, `client.ts` (`timeout: 15_000`).

`apiClient` has a 15 s timeout, and the client's own JSDoc says "A request may set its own `timeout`". `sendMultipart` sets none. In a browser (XHR) the timeout covers the whole request, upload included.

D1's whole premise is a weak connection. A shrunk photo is a few hundred KB, and at about 30 KB/s that is 15 s or more. The tile then fails with `timeout`, the retry offers the same 15 s, and the admin on exactly the connection the design targets can never add the photo.

No test or real run could show this: the local run was instant and the fake transport has no clock.

**Fix** (fix round): `sendMultipart` passes its own generous `timeout` (for example 120 s, or none with progress-based stall detection), with a unit assertion that `config.timeout` is raised. Say so in `architecture.md` §7's multipart line.

### 4. [should-fix] The "Uploaded N of M" line is a prediction, never clears, and is not announced
`usePhotoUploads.ts:163-166`, `PhotosSection.tsx:79-81`.

- It is set at choose time from `kept.length`, so it is not "the real counts". With 9 stored and `[a.heic, b.jpg]`, the HEIC takes the one free slot, `b.jpg` is dropped, and the line says "Uploaded 1 of 2" although nothing went up. The same happens when a kept file later fails.
- `setSummary` is never called with `null`. After "Uploaded 5 of 7; the limit is 10 photos", the line stays through deletions, later successful choices and everything else, until the section unmounts.
- It is a plain `<p>`, not a live region. A screen-reader user is never told that files were dropped.

**Fix** (fix round): count uploaded files as they succeed and write the line when the batch ends, or reword it to "Added N of M; the rest did not fit". Clear it when the next choose starts or the room changes. Put it in a `role="status"`. Add a test with a mixed selection (one unsupported, one over the limit, one good).

### 5. [should-fix, plausible] "Leave" does not stop the queue, so the dialog's promise is false
`usePhotoUploads.ts:111-124,138-142`.

On unmount the hook only tells the guard `false`. `drain` keeps looping over `queue.current`, and it sends every remaining queued file, because nothing aborts the request or sets a cancelled flag. `sendMultipart` takes no signal.

The dialog says "A photo that has not finished uploading will be lost", but after the admin confirms Leave in the SPA, the in-flight photo and all queued ones still upload, invisibly. They land in the space and use up the rate limit. Returning to the editor shows photos nobody saw being added.

I did not run this. It follows from the loop and from the SPA's navigation not killing JavaScript. `SpaceEditPage` also passes no `key={spaceId}`, so a space switch mid-queue is the same story.

**Fix** (fix round, or a finding if the owner prefers the dialog reworded): stop the loop on unmount with a `cancelled` ref, and abort the in-flight request through an `AbortSignal` on `sendMultipart` (a new parameter that production code does use). Or reword the dialog to what really happens. Add a test: unmount mid-queue and expect no further POST.

---

## Part 2: the rest, most severe first

### 6. [should-fix] Remove and upload failures leave the gallery stale, and say the wrong thing
- `usePhotoRemove`/`usePhotoOrder`: a 403/404 only calls `useSpaceAnswer.refused`, which invalidates the space. The plan says "and invalidates the key" (photos), and this does not.
- A `DELETE` 404 for a photo another admin already removed (the plan's "two admins" case) shows the "The space was deleted meanwhile" line (`usePhotoGallery.ts:33-35`). The space is not deleted. The removed tile also stays, since the photos are never refetched.
- `remove.reset()` is never called, so after a failed removal and Cancel, asking about another tile shows the previous failure in the new dialog (`failure` is derived from `remove.isError`).
- **Fix** (fix round): invalidate the photos key on any gallery write error with status 404/409. Reset the mutation in `ask`/`cancel`. Word the photo-404 case as "that photo is already gone".

### 7. [should-fix] Catalogue lines shipped unused; the cover buttons are unnamed
`galleryFull`, `makeCoverNamed`, `before` and `after` are defined in both catalogues and read nowhere (checked with grep over `features/`).
- The report says an unused line "is not one this item should ship". That is wrong for these four.
- `makeCoverNamed` unused means every tile's cover button reads only "Make it the cover". With several tiles, a screen-reader user hears the same name each time, while the arrows and Remove are named for their photo.
- `galleryFull` unused means an upload 409 (gallery filled elsewhere) shows the generic `errors.conflict` text and the gallery is not refetched.
- **Fix** (fix round): use `makeCoverNamed` as the cover button's accessible name. Map `conflict` to `galleryFull` on the upload tile and refetch. Delete `before` and `after`.

### 8. [should-fix] A verified space's tiles have no accessible content
`PhotoTile.tsx:20-26`, `ReadOnlyPhotos.tsx`. The image is `alt=""` and `actions` is null, so a `<li>` holds nothing but (on the first) "Cover". A screen reader hears an N-item list of empty items, and the plan's justification ("named by its actions") does not hold with no actions. No axe test covers the read-only case.
**Fix** (fix round): give read-only tiles an accessible name, with `alt` set to `label` or a visually hidden `label`.

### 9. [should-fix] The 409 message is only in an `sr-only` region
`usePhotoOrder.ts:48-51`. `orderChanged` is written to `said`, which `PhotosSection` renders in `<p role="status" className="sr-only">`. A sighted admin whose move was refused sees the list jump with no explanation. The line also says "Reload it", while the hook already refetched.
**Fix** (fix round): show it visibly, as a caption or in the tile failure, and reword it to what happened.

### 10. [should-fix, small] A transparent PNG becomes black
`shrinkImage.ts:24-31`. Canvas JPEG export composites transparency onto black. S1's cost says it "loses its transparency", but it is not lost, it turns black. No white fill is drawn first.
**Fix** (fix round): `fillStyle = '#fff'; fillRect` before `drawImage`. Extend `fakeCanvas` so the test can see it.

### 11. [nit→should-fix] "Add photos" is disabled during any upload, with no reason, and focus is lost
`usePhotoGallery.ts:112`: `disabled: !canAdd || busy`. The plan disables it only at ten. A real `disabled` button also drops keyboard focus after the picker closes. This is not among the 12 declared departures. It also makes `choose`'s "append to a running queue" path unreachable in the UI.
**Fix** (fix round, or a recorded departure): drop `|| busy`, or use `aria-disabled`, and show a reason.

### 12. [nit] Failure text on an upload tile
`PhotoUploadTile.tsx:42` falls back to `words.loadFailed` ("We couldn't load the photos"), a load message, on an upload with no `AppError`. A non-`UnsupportedImageError` thrown by `draw`/`toBlob` becomes `refusal: null`, with no retry and a wrong sentence.

### 13. Tests: judged one by one

**Commit 2 (never seen failing):**
- `spacesRepository.unit` (paths, methods, body): would go red on drift. Fine.
- `usePhotoOrder`: tests 1 and 3 (the id lists) go red on a partial or wrong permutation. The three-way claims fail:
  - "shows the new order once the server has accepted": no assertion on the refetch. Remove `invalidateQueries(photos)` and the test stays green.
  - The 409 test claims "shows the server's order": it never checks the refetch. Same break stays green.
  - The 403 test checks only the space key.
  - Nothing tests two quick moves (finding 2).
- `usePhotoRemove`: test 1 goes red without the toast or the right URL. The refetch is not asserted. The 403 test checks `target` only, which is the opposite of what the UI does (finding 1). No component test clicks Delete.
- `PhotosSection`: cover, order, disabled arrows and the live region would go red as planned. The `disabled` assertion encodes the AC 5 violation. The test titled "…and the limit beside a disabled add at ten" (line 153) only checks the empty state and duplicates the one above it. The ten-photo case is covered by the next test, so this is a mislabelled duplicate.
- `SpaceEditor` "draws the photos section last": it never asserts the order. Drawing it first would pass. The six-item navigation test does pin the nav order.

**Commit 3 (seen failing):** the uploads tests are real. Gaps: no mixed selection (the summary lie), no 403/404 on upload through `useSpaceAnswer` (S5), no unmount `false`, and nothing proves `PhotosSection` → `useSpaceEditor` → guard is wired (a dropped `onUploadingChange` prop passes every test).

**The two failures under load:**
- `useAdminSpacesFilters`: a real miss. The test asserted the old behaviour, and the executor fixed and folded it correctly.
- `routes.component.test.tsx`: a flake. The branch touches no routes, it passed alone and on the next full run, and CI is green. It is the class finding 28 describes, so no new finding is needed.

### 14. What the real run did not exercise: is a test proving it?
- Ten-photo limit: **proved** (section test, hook test).
- Over-limit selection: **partly**. The hook test proves the counts at choose time only (finding 4 shows why that is not enough).
- Leave guard during an upload: **the guard hook is proved**, including the reload prompt (`unloadAsks`). The wiring from the section to the guard and the unmount are **not proved**.
- Disconnect and retry: **the hook is proved** (`ERR_NETWORK`, then retry). **No test renders a failed tile.** The retry and drop buttons, the 429 countdown, the `tooLarge` line and the reference line are proved by nothing, and the real run showed only the unsupported-format tile.
- EXIF-6: the option is **proved passed**, with `from-image` asserted on the decode. The actual rotation is not provable in jsdom and the real run had no sample.
- Server 415: `canRetryUpload` is proved (no retry). The tile text is the generic line, and nothing proves the UI.
- **Nothing proves:** a removal's failure (finding 1), the 15 s timeout (3), the Leave-continues behaviour (5), a stale double move (2), and anything done on the commit 0 screens in a browser. Part 2 of the report lists none of §12.4's commit 0 checks (deleted list, phone sheet badge and clear with `stale=true`, dialog line, chip). Finding 70 was checked against the seeded demo space, not space 41 in `masaha_dev` as §14 names.

### 15. The 12 departures
1. Commit 2 tests not seen failing: accepted as disclosed, and now shown to matter (finding 13).
2. `id` added to the tile: fine.
3. Two tile types: fine, but `PhotoUploadTileView` lacks the plan's `drop` only-when-failed rule. Drop renders only when failed, so there is no ghost.
4. No `order` field: fine.
5. Copy placement: fine, but it claims no unused line ships (finding 7).
6. Extra lines in `space-links.md`: fine.
7. Third test file: fine.
8. Finding 70 not recorded: acceptable, but see finding 14.
9. `#85` / `#84` suffixes: fine.
10. Reading from the working tree: harmless.
11. `onUploadingChange` on the hook: fine.
12. Extra bullet in `architecture.md`: fine.
- **Undeclared:** the `busy` disable (finding 11), `disabled` instead of `aria-disabled` (2), no photos invalidation on 403/404/409 (6), and the summary semantics (4).

### 16. Frontend rules and documents
- No physical direction classes, no arbitrary values, no new colour or CSS, and design-system components only. `top-2 start-2` is logical. Strings are all in both catalogues with parity (apart from the four unused).
- `docs/features/spaces.md:19` still says "photos are still API-only". It now contradicts the new gallery paragraphs in the same file. Fix: "the owner/reception web screen is not built".
- The spaces.md paragraph says a refusal "stays on the tile" and "Nothing moves before the server has accepted" (see findings 1, 2, 9). The finding 73 text puts the percentage "inside the tile's own `role="status"`", but the tile's own status wrapper was removed and the `Spinner` is the `role="status"`. This is a nit.
- The headers: `overview.md` (Last Updated 2026-10-14) and `frontend/architecture.md` (2026-10-13) were edited without a date bump, while commit 0 bumped two others. A nit.
- The `spaces.md` history line for #85 says Restore was "placed in the Actions"; no code moved in this PR. The cell already holds the actions. It is a doc correction, so reword the line as "documented".
- The `spaces.md` decision quotes "you'll" with a straight apostrophe, while the catalogue uses `’`. A nit.
- Findings 73 and 74 are honest and the link check passes.

### 17. Commit 0 against §14 (rows 0.1 to 0.9)
Complete and self-consistent:
- Sheet count and clear: right, and tested at hook and list level. `anyApplied` and `clearAll` still include the chip.
- The deleted row is one muted line: right, in `rowView`, table and card.
- The delete dialog's line and the chip's words: right.
- Both added tests exist and would go red on their named breaks (the status-change busy test fails without `placeholderData` at its `status === 'ready'` assertion).
- `updatedOn`'s comment, the `#84` suffixes, findings 44/50 and 69, and "stale or missing" everywhere: done.
- Nits:
  - The phone card still renders an empty `BadgeList` `<span>` for a deleted row, which adds a stray flex gap.
  - The `useLeaveGuard` third parameter has a `= false` default that no caller uses.
  - `sendMultipart`'s optional `onProgress` branch is exercised only by a test (production always passes it), which skirts the "no parameter only a test uses" rule.

### 18. Commits
Subject lengths, counted: 49, 42, 38, 42. All are at most 50. No tool attribution in the messages or in the documents. Order matches the plan. Staging and scope: 62 files, nothing in `apps/api` or `packages/shared`.

---

## Where each fix belongs
- **Fix round on this PR:** 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, the `spaces.md:19` line, the test gaps in 13/14, and the nits in 12/16/17 (cheap).
- **Finding to record instead (if the owner prefers):** 5 (leave semantics) and 10 (alpha).

## Checked and fine
- The upload layer is domain-free, imports only `@shared/api` and `@shared/errors`, and goes through the one client. `fitInside`, 1600 px, 0.85 and JPEG are right, and `imageOrientation: 'from-image'` is really passed (asserted). `shrinkImage` takes no options.
- `fakeCanvas` is reached through globals, with no `vi.mock`. The progress-event typing avoids importing Axios outside `shared/api`.
- The query key, the repository paths and the multipart field name match the contract.
- Serial queue order, one request in flight, room accounting and the HEIC refusal with no request are correct and tested. A verified space draws no controls, the ten-photo limit text is right, and the guard's title and description are right (unit-tested).
- The checklist still lists five groups, and the section carries no date or Save.
- CI is green on this head, the PR is CLEAN, and the head did not move during the review.
