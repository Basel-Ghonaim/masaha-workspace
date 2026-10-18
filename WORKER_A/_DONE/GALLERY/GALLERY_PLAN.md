# GALLERY (S2b-4c) — the editor's photos: shrink, upload, order, cover, remove

> **Regenerated 2026-10-16 against `origin/main` @ `93f152fe` (PR #84, ADMINLIST merged; PR #82,
> OWNERSREAD merged).** One pre-approved decision is carried over verbatim from the plan this
> replaces and is **binding** on the executor:
>
> > **The per-tile progress is shown without a new design-system component and without a
> > dependency.** A tile's pending state is the layer's existing `Spinner` (never a hand-drawn bar),
> > with the percentage as text beside it — «جارٍ الرفع 45٪» / "Uploading 45%", Western digits as the
> > app's numbers — read from the upload's progress events. **Do not add shadcn's `Progress`** (it
> > brings `@radix-ui/react-progress`, a dependency) and **do not hand-roll a `role="progressbar"`
> > bar** (the prototype drew one; that is finding 73). Everything else follows this plan as written.
>
> **This plan must stand alone.** A fresh conversation — possibly Copilot or Codex — executes it
> after both ADMINLIST and OWNERSREAD are in `origin/main`, from the latest `origin/main`; a third
> conversation reviews. No step depends on any Claude skill.

> ## The owner's approval — 2026-10-17 (binding; it wins over anything below that disagrees)
>
> **Approved as written:** S1, S3–S12; §8 design issues 2 and 3 (no preview while uploading, no
> visible position number); findings 73–74 if they still hold. **Amended (already written into the
> sections below — this list is only the summary):**
>
> 1. **S2 changed:** the file input carries `accept="image/*"` (a phone opens its gallery and camera;
>    a HEIC still reaches its tile, and iOS often converts it to JPEG itself). Not the three-type list.
> 2. **`shrinkImage` takes no options:** `shrinkImage(file: File): Promise<File>`, always
>    `SHRINK_DEFAULTS`. A parameter only a test passes is forbidden in this project.
> 3. **Orientation:** the decode is `createImageBitmap(file, { imageOrientation: 'from-image' })`.
>    The re-encode drops EXIF, and the server's `autoOrient` (`apps/api/src/shared/images/encodeImage.ts`)
>    can then no longer turn a phone's portrait photo; the browser must turn it first.
> 4. **The PR number in the documents:** every new decision and history line ends `2026-10-DD, #85`
>    (§12.5 step 12b checks the number before the push).
> 5. **Fixes before the push fold into their own commit** (`git commit --fixup <sha>` then
>    `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash origin/main`); no "fix lint" commit in the history.
> 6. **The real run starts the database with `docker start masaha-postgres-1`** (Docker Desktop
>    first) — never `npm run db:up`; never `npm ci` in this folder (use `npm install` only if a
>    dependency is missing, and none should be).
> 7. **This PR also carries the post-merge review of #84** (`REVIEW84_OPENCODE_REPORT.md`): one more
>    commit, **commit 0, first in the history** — §14. It is in scope by the owner's decision, so
>    `features/space-links` and the admin list's files are licensed for §14's changes only. The
>    total stays under 70 files; if it does not, stop and ask.
>
> **The executor is OpenCode.** Work commit by commit (0, 1, 2, 3), run each commit's checks before
> starting the next, and write the report in parts.

---

## 1. Summary

The admin space editor gains its last section, **«الصور» / Photos**, on the photos API already built
by PR #77. The web first adds a **domain-free upload layer in `shared/`** — shrinking an image in the
browser and sending a multipart body through the app's one HTTP client with per-file progress —
which knows nothing of spaces, so an avatar or another file kind can use it later. Then the
**gallery**: the photos in the server's order with the cover marked, «اجعلها الغلاف», moving a photo
before and after, removing one through an `AlertDialog`, the empty state, and finally **uploading**:
choose files, each tile its own progress and its own failure with «إعادة المحاولة», the ten-photo
limit, and the leave guard while an upload runs.

One Work Item, three commits, **web only**. Nothing in `apps/api` or `packages/shared` changes: the
contract already supplies `GET|POST /admin/spaces/:spaceId/photos`, `DELETE …/photos/:photoId`,
`PUT …/photos/order`, `SpacePhoto { id, urls: { card, page } }`, the first being the cover, 4 MiB,
JPEG/PNG/WebP, at most 10 (a 409 for the eleventh), 413, 415, 30 uploads per 15 minutes, and `can()`'s
refusal of a verified space with 403.

---

## 2. The contract

### Scope

- A reusable browser image shrinker: decode a `File`, bound its longest side to 1600 px, re-encode at
  quality 0.85, hand back a multipart-ready `File`. A file the browser cannot decode is refused with
  a typed error. **No new dependency, no new design-system component.**
- A reusable multipart upload through the existing `shared/api` client, one request per file, with a
  progress callback. It knows a URL, a field name, a file and a transport progress event — nothing
  about spaces or gallery policy.
- The `spaces` repository, query key, query hook and mutations for: list, upload, remove, order.
- `PhotosSection` in the editor and `ReadOnlyPhotos` for a verified space, each built from a shared
  card frame and a shared tile.
- The gallery's copy in both catalogues, and its states.
- Focused unit and component tests for every behaviour, each in its owning lane.
- The documentation the change makes true: `docs/features/spaces.md`, one line in
  `docs/frontend/architecture.md`, the *Built* line in `docs/project/overview.md`, and the two new
  findings the prompt reserves.

### Acceptance criteria

1. `«الصور» / Photos` is the sixth item of the editor's sections navigation, after `«التواصل»`, and
   the editor draws it last. The *«ما زال ناقصًا»* checklist still lists **five** groups — photos are
   no fact group and are never «تمّت / لم تُضف بعد».
2. The section is a card with an `h2` and its intro line, and **no date, no staleness badge, no Save,
   no Discard, no “still correct”**. It is not wrapped in `SectionCard`, which is a fact group's frame.
3. An unverified space reads `GET /admin/spaces/:spaceId/photos` under
   `spacesKeys.photos(spaceId)` = `['admin','spaces','photos', spaceId]`, and renders the photos in
   the server's order. The first tile carries a `Badge variant="primary"` reading «الغلاف» / "Cover".
4. A verified space reads the same gallery and renders it read-only: no upload, remove, reorder or
   cover control is rendered at all. The server's `can()` stays the authority; the web's part is
   `useSpaceEditor`'s existing `readOnly`.
5. A non-cover tile offers «اجعلها الغلاف» / "Make it the cover"; the first tile has no such control.
   Reordering is two icon buttons — `ArrowUpIcon` («قبل»), `ArrowDownIcon` («بعد») — named for the
   photo they move, `aria-disabled` at the boundary, and each sends the **complete** id list to
   `PUT …/photos/order`. The first id is the cover. Nothing moves on screen before the server has
   accepted (no optimistic update).
6. Removing opens an `AlertDialog` whose title names the photo, acts only on confirm, then a toast
   names what was deleted. A `403` or a `404` on any gallery write says so on the tile and fetches
   the space again, so a verified space turns read-only and a deleted one shows the 404.
7. With no photos the section shows `EmptyState` — «لا توجد صور بعد» / "No photos yet" and «الصورة
   الأولى تصبح الغلاف» / "The first photo becomes the cover" — and no list.
8. «إضافة صور» / "Add photos" opens a file picker for many files at once. Files are uploaded
   **one at a time**, in the order chosen; the next starts only after the previous has been answered.
9. Each file has its own tile with its own state: being prepared, uploading with its own percentage,
   failed with its own line and «إعادة المحاولة» / "Try again". A tile that failed keeps the file.
10. A file the browser cannot decode (HEIC) is refused **on its own tile** with
    «صيغة غير مدعومة، اختر JPEG أو PNG أو WebP» / "Unsupported format; choose JPEG, PNG or WebP", and
    no request is sent. A refusal the server has already judged (413, 415, 400, 422) shows no retry,
    because a re-send of the same bytes cannot succeed; it offers only «أخرجها من القائمة».
11. Choosing more files than the gallery has room for uploads what fits and says
    «رُفعت 3 من 5؛ الحد 10 صور» / "Uploaded 3 of 5; the limit is 10 photos" with the real counts.
    At ten photos «إضافة صور» is disabled with «الحد 10 صور — احذف صورة لتضيف غيرها» beside it.
12. While any file is being prepared or uploaded, the editor's leave guard asks on a navigation to
    another page and through the browser's own prompt on reload; a move to a section's anchor never
    asks; once the queue has ended the navigation goes on by itself. The dialog's title and its line
    name the unfinished upload, and name no section that has nothing unsaved.
13. Every visible and assistive string is in both catalogues. No hardcoded text, no new dependency,
    no new design-system component, no new colour/font/CSS outside the layer, no physical direction
    class, no arbitrary-value class, no change to `apps/api` or `packages/shared`.
14. The gallery is legible and operable in Arabic and English, RTL and LTR, light and dark, at 360,
    768 and 1440 px, from the keyboard alone, and adds no width pressure to the prices table at
    768 px (finding 67 stays open and untouched).

### Out of scope

- Anything in `apps/api`, `packages/shared`, Prisma, the schema, the storage adapter, the image
  core, the rate limits, `can()` or the API error codes. If the gallery needs one of these, **stop
  and say so**.
- Drag and drop, captions, per-photo metadata, bulk delete, bulk reorder, a Save/Confirm/date on the
  section, an undo for a removal, editing a photo's file, cropping, rotating, reordering the public
  page's gallery, and anything on the public site or the owner/reception web screen.
- A new design-system component, a new dependency, a new error code, a new catalogue line under
  `errors` (every type this section can meet already has one).
- The editor's route, the page that mounts `SpaceEditor`, the space switcher, the admin's spaces list
  and `features/space-links` — the gallery is reached through the editor that already exists.
  **Exception:** §14's corrections of #84, in commit 0 only.
- Changing `docs/api/api-contract.md`, and changing the frozen design archive under `docs/design/`
  (its divergence is recorded as finding 74 instead).

---

## 3. Reading done

Read from `origin/main`'s commit objects (`git show origin/main:<path>`), never from a working tree:

- `CLAUDE.md` — the non-negotiables, the decision precedence, the session checklist.
- `docs/README.md` — the map, the *read it when* lines, the deferred-documents table (none is
  triggered: the *Endpoints* row is the API's, and no endpoint is built here).
- `docs/development/workflow.md` — §2 the Work Item and its seven phases, **Reading before work**,
  §3 Git lifecycle, *Commits*, *PR description*, §4 scope control, §5 Definition of Done, §6
  decision authority, §7 documentation triggers, §8 stop rules, §9 parallel work and *Conflicts*.
- `docs/features/spaces.md` — *What it does*, *Responsibility boundary*, *How it composes the
  platform*, *The space editor on the web* (every paragraph), *Photos*, the web decisions of #74 and
  #79 (S1–S9, and the patterns their reviews corrected), *Code map* › Web, *Open findings*.
- `docs/api/api-contract.md` §3 (error types) and §5 › *Spaces (the admin)* › *Photos* — the four
  endpoints, their bodies, their status codes, the audit names, the caching line.
- `docs/backend/conventions.md` — the storage line (a new file kind is a new consumer) and the layers.
- `docs/frontend/architecture.md` — §1 four zones and the dependency rule, §2 page groups and
  *Titles*, §3 capabilities, the dashboard-only rule, *Capability layout*, *Components present; hooks
  prepare*, *React Query in a feature*, *Where state lives*, *What a feature exports*, **§3 Forms**,
  §5 errors, §7 server state (keys, invalidation, retries, query defaults, and *"Optimistic updates
  never for money or presence; only for favourites"*).
- `docs/frontend/design-system/foundation.md` — §2 principles, §3 architecture and the closure rule,
  §5 semantic roles, §7 typography (*Digits: Western (0–9) in both languages*), §8 direction and
  icons, §9 responsive layout, §10 accessibility baseline, §11 the component contract, §12 the
  component inventory (there is **no `Progress`**; `Button`, `Badge`, `Card`, `AlertDialog`,
  `EmptyState`, `Spinner`, `Skeleton`, `Alert`, `ArrowUpIcon`, `ArrowDownIcon`, `XIcon` exist).
- `docs/frontend/localisation.md` — the catalogue mechanism, *Writing a line*, parity, `useCopy` /
  `currentCopy`.
- `docs/development/testing.md` — §1 the assignment rule, §2 the lanes and what each forbids, §3 the
  seven rules, *A feature, layer by layer*, §4 what must always be tested.
- `docs/development/engineering-principles.md` — §1 (put the boundary in now, build the
  generalisation at the second instance), §3 architecture rules, §7 naming, §8 comments.
- `docs/architecture/documentation.md` — §5 the capability-document template and the *Decisions* /
  *History* split by layer, §7 ADRs, §8 link integrity.
- `docs/architecture/findings/README.md` — every open title; the open files **63**, **64**, **67**;
  the resolved files **59**, **67**'s neighbour **44** and **50** for the format.
- `docs/project/overview.md` — the *Built* line for **Spaces**.
- `docs/development/setup.md` — §*The web* (ports 5320 / 3320, the `/api` proxy), §*The API first run*,
  §*Running a second folder*, §*CI* (every lane runs in CI, `test:api` as its own job).
- `packages/shared/src/spaces/photos.ts` — `PHOTO_LIMIT = 10`, `PHOTO_MAX_BYTES = 4 * 1024 * 1024`,
  `PHOTO_SIZES = ['card','page']`, `PhotoSize`; `responses.ts` — `PhotoUrls = Record<PhotoSize,string>`,
  `SpacePhoto = { id, urls }`; `index.ts` re-exports `./photos.ts`.
- `apps/web/src/shared/api/client/request.ts` — `api.get/post/put/patch/delete` **already accept
  `config?: AxiosRequestConfig`**, so `onUploadProgress` needs no transport change;
  `client/setupApiClient.ts` — the interceptor order; `interceptors/retry.ts` — **a POST without an
  `Idempotency-Key` is never re-sent**, so an upload is retried only by the user;
  `interceptors/normalise.ts` turns every failure into an `AppError` (status, code, requestId,
  retryAfterSeconds).
- `apps/web/src/features/spaces/` on `main`: `repository/spacesRepository.ts`,
  `hooks/queryKeys.ts`, `hooks/mutationKeys.ts`, `index.ts`,
  `components/editor/{SpaceEditor,SectionCard,ReadOnlyCard,SectionNav,LeaveDialog,MissingChecklist}.tsx`,
  `hooks/editor/{useSpaceEditor,useSpaceQuery,useSectionFrame,useSectionInView,useSpaceAnswer,useLeaveGuard}.ts`,
  `hooks/contacts/useContactsSection.ts` (the section-hook pattern),
  `components/amenities/AmenitiesSection.tsx` (the *disabled Add + its reason* pattern),
  `components/toast/{ActionRefusal,actionToasts}.tsx`, `services/updatedAgo.ts`,
  `types/SectionFrameView.ts`.
- `apps/web/src/shared/design-system/index.ts` (the whole public surface) and the source of
  `Spinner`, `EmptyState`, `Button`.
- `apps/web/src/shared/forms/hooks/useRefusalView.ts` (+ `types/FormFailureView.ts`) — the one reader
  of a refusal, with `lines` by `code ?? type` and the 429 countdown.
- `apps/web/src/shared/copy/english/spaces.ts` and `arabic/spaces.ts` (the `editor` object and its
  shape), `english/errors.ts` (`payload_too_large`, `unsupported_media_type`, `conflict`, `forbidden`,
  `not_found`, `rate_limit`, `network`, `timeout`, `canceled`, `unknown` all exist).
- `apps/web/src/test/` — `fakeAdapter.ts` (the unit lane's transport), `fakeTransport.ts` (the
  component lane's), `fakePlatform.ts` / `fakeStorage.ts` (the established pattern: a test stands in
  for the **browser through the global the production code reaches**, never `vi.mock`).
- `apps/web/vite.config.ts` — the unit lane is **node** (no DOM, no canvas), the component lane is
  **jsdom**; `scripts/checkClasses.ts` — physical and arbitrary-value classes outside the layer fail;
  `scripts/dashboardOnly.ts` — `shared/` is not a dashboard module, so a shared module only the
  dashboard imports never enters the site's first download.
- `docs/design/prototype/masaha/profile-b.jsx` — the prototype's `PhotosSection` in full (its grid,
  its tile, its cover badge, its arrows, its `AlertDialog`, its limit line, its live region).
- `C:\Users\basel\.prompt\MASAHA_DESIGN\DECISIONS_ADMIN.md` › **A1** (five fact groups **then الصور**
  — "no date, no confirm"; the sections are `h2`; below `lg` the navigation is a scrolling row of
  chips) and `DECISIONS_OWNER.md` › **O7** (photos are immediate actions: upload on choose, per-tile
  progress and failure with 413/415 and retry, removal by `AlertDialog`, reorder and cover at once,
  no save, no date); **DI-33** as recorded in the previous plan (the empty state).
- `C:\Users\basel\.prompt\MASAHA_WORKER_A\PLAN\ADMINLIST_PLAN.md` §*Files* — its files, and the
  binding pre-approved progress decision in the plan this replaces.

---

## 4. The settled decisions, as they will be built

Each is **D1–D6** from the prompt (owner, 2026-10-15) or settled by the design.

**D1 — shrink in the browser to the longest side 1600 px, at quality 0.85.**
`1600` is the server's own `page` bound, and the server never enlarges, so anything larger is thrown
away. Re-encoding also strips the EXIF a phone photo carries, which is half of the server's own
rationale. The result is at most 1600×1600 ≈ 2.6 MP, comfortably under the server's 50 MP guard, and
a JPEG at 0.85 there is a few hundred kilobytes — so a phone photo travels small on a weak
connection and stays under 4 MiB.

**D2 — a HEIC the browser cannot decode is refused on its tile,** with
«صيغة غير مدعومة، اختر JPEG أو PNG أو WebP» / "Unsupported format; choose JPEG, PNG or WebP".
**No new dependency**, no conversion fallback: nothing sends a request.

**D3 — one upload at a time, in the order chosen.** The order is the gallery's, a weak connection is
not shared, and a burst would meet the 30-per-15-minutes limit.

**D4 — order by arrows** «قبل» / «بعد» and «اجعلها الغلاف», as the admin's lists move rows: keyboard
and screen reader first. No drag and drop.

**D5 — more files than the gallery has room for:** upload what fits and say
«رُفعت 3 من 5؛ الحد 10 صور» / "Uploaded 3 of 5; the limit is 10 photos"; «إضافة صور» is disabled at
ten with its reason beside it.

**D6 — the leave guard asks while an upload runs.** The photos are immediate actions, so nothing is
"unsaved"; only an unfinished upload is lost, and the dialog says exactly that.

**Settled by the design:** removal through an `AlertDialog`; no date, no confirm, no save (A1); the
empty state «لا توجد صور بعد · الصورة الأولى تصبح الغلاف» (DI-33); a verified space's gallery
read-only; the section is made for the owner's editor to reuse, as #74's D5.

### 4.1 Interfaces — the shared upload layer (`shared/uploads`)

```
apps/web/src/shared/uploads/
  index.ts                        the module's only entry
  types/UnsupportedImageError.ts  the class the shrinker rejects with
  services/photoGeometry.ts       pure: the size a photo is drawn at
  services/shrinkImage.ts         the browser act: decode → draw → encode
  services/sendMultipart.ts       one multipart POST through @shared/api, with progress
  services/canRetryUpload.ts      pure: whether a re-send of these bytes could succeed
```

| Export | Signature | Returns / throws |
|---|---|---|
| `fitInside` | `(width: number, height: number, maxSide: number) => { width: number; height: number }` | The size inside `maxSide` on its **longest** side; never enlarges; neither side below 1. Pure — no DOM, so the **unit** lane proves it. |
| `SHRINK_DEFAULTS` | `{ maxSide: 1600, quality: 0.85, mimeType: 'image/jpeg' } as const` | The one place the numbers of D1 live. |
| `shrinkImage` | `(file: File) => Promise<File>` — **no options parameter**; it always uses `SHRINK_DEFAULTS` | A new `File` named `<base>.jpg` of type `image/jpeg`, at the bounded size. It decodes with `createImageBitmap(file, { imageOrientation: 'from-image' })`, so a phone's portrait photo is turned before its EXIF is dropped. Rejects with `UnsupportedImageError` when `createImageBitmap` or `canvas.getContext('2d')` is unavailable, when the decode fails, or when `toBlob` yields nothing. |
| `sendMultipart` | `<T>({ url, fieldName, file, onProgress }: { url: string; fieldName: string; file: File; onProgress?: (sent: number, total: number) => void }) => Promise<T>` | The envelope's `data` (`api.post` already unwraps). Rejects with the transport's `AppError`. Calls `onProgress(loaded, total)` from `onUploadProgress`, ignoring an event with no `total`. |
| `canRetryUpload` | `(error: Pick<AppError,'type'> \| AppError) => boolean` | `true` for `network`, `timeout`, `canceled`, `unknown`, `server`, `service_unavailable`, `rate_limit`; `false` for every 4xx the server has already judged (`bad_request`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `validation`, `payload_too_large`, `unsupported_media_type`). Pure — the **unit** lane proves it. |
| `UnsupportedImageError` | `class UnsupportedImageError extends Error` | The only error `shrinkImage` raises. |

`shared/uploads` imports `@shared/api`, `@shared/errors` and nothing else. It never names a space, a
photo or a gallery. It is a `shared/` module, so the dependency rule holds (`shared → shared`).

### 4.2 Interfaces — the spaces feature

**Repository** (`repository/spacesRepository.ts`, four methods added to `SpacesRepository` and its
factory):

```ts
listPhotos(spaceId: number): Promise<SpacePhoto[]>;
uploadPhoto(spaceId: number, file: File, onProgress?: (sent: number, total: number) => void): Promise<SpacePhoto>;
removePhoto(spaceId: number, photoId: number): Promise<undefined>;
orderPhotos(spaceId: number, ids: number[]): Promise<undefined>;
```

built on the existing `path(spaceId)`:

```
listPhotos  → api.get<SpacePhoto[]>(`${path}/photos`)
uploadPhoto → sendMultipart<SpacePhoto>({ url: `${path}/photos`, fieldName: 'photo', file, onProgress })
removePhoto → api.delete<undefined>(`${path}/photos/${photoId}`)
orderPhotos → api.put<undefined>(`${path}/photos/order`, { ids })
```

`SpacePhoto`, `PHOTO_LIMIT` and `PHOTO_MAX_BYTES` come from `@masaha/shared/spaces` — never copied.

**Query key** (`hooks/queryKeys.ts`): `photos: (spaceId: number) => ['admin','spaces','photos', spaceId]`.
The only key the gallery reads or invalidates. It never invalidates `['admin']` wholesale, never the
space's key except to refetch it on a 403/404, and never another capability's.

**Types** (`types/PhotoTileView.ts`, `types/PhotoGalleryView.ts`) — the view models a hook hands a
component; no `AppError`, no code, no mutation ever crosses into a component.

```ts
type PhotoTileState = 'done' | 'preparing' | 'uploading' | 'failed';
type PhotoActions = {
  before: { label: string; disabled: boolean; busy: boolean; run: () => void };
  after:  { label: string; disabled: boolean; busy: boolean; run: () => void };
  cover:  { label: string; run: () => void } | null;   // null on the cover itself
  remove: { label: string; run: () => void };
  retry:  { label: string; run: () => void } | null;   // null when a re-send cannot succeed
  drop:   { label: string; run: () => void } | null;   // only while the photo is not on the server
};
type PhotoTileView = {
  key: string;                  // `photo-<id>`, or `upload-<local id>` before it is stored
  position: number;             // 1-based, from the order shown
  label: string;                // «الصورة 3» / "Photo 3"
  cover: boolean;
  image: { src: string } | null;// urls.card; null while the file is being prepared or sent
  state: PhotoTileState;
  progress: number | null;      // 0–100, only in 'uploading'
  fileName: string | null;      // the chosen file's name, while it is not yet stored
  failure: FormFailureView | null;
  actions: PhotoActions | null; // null on a verified space
};
```

**Hooks** (each one responsibility; all in `hooks/photos/`):

| Hook | Reads | Returns |
|---|---|---|
| `usePhotosQuery(spaceId)` | `spacesKeys.photos(spaceId)` | TanStack Query's `useQuery<SpacePhoto[], AppError>` over `repository.listPhotos` |
| `usePhotoOrder(spaceId, photos)` | that key | `{ moveBefore(id), moveAfter(id), makeCover(id), busy, failure: FormFailureView \| null, said: string \| null, announce(line) }`. Each move computes the **whole** permutation of `photos.map(p => p.id)` and sends it; on 204 it invalidates the key, on 409 it invalidates too and says the gallery changed, on 403/404 it calls `useSpaceAnswer(spaceId).refused(error)` and invalidates the key. No optimistic move. |
| `usePhotoRemove(spaceId)` | that key | `{ target: PhotoTileView \| null, ask(tile), cancel(), confirm(), busy, failure }`. `confirm()` calls `removePhoto`, invalidates the key, closes the dialog and fires `toast.success(copy.spaces.toasts.photoRemoved({ photo }))` with `currentCopy()` read then. |
| `usePhotoUploads(spaceId, photos, onUploadingChange)` | that key | `{ choose(files: FileList \| File[]), busy, tiles: PendingTileView[], summary: string \| null, canAdd, addReason }`. Owns the queue: snapshots the room left, keeps only what fits, shrinks, sends one at a time in order, records each tile's own progress and failure, offers a retry where one can work, and calls `onUploadingChange(true/false)` while any file is being prepared or sent (and `false` once it unmounts). |
| `usePhotoGallery(spaceId, readOnly)` | that key | The section's whole view: `{ state: 'loading' \| 'failed' \| 'ready', title, intro, failure, retry, tiles, empty, said, order, remove, uploads }`. |
| `useReadOnlyPhotos(spaceId)` | that key | `{ state, failure, retry, tiles, empty, said }` — the same query and the same tiles with `actions: null`. |

`useSpaceEditor(spaceId)` gains two things: the section list becomes
`[...FACT_GROUPS, 'photos']` (a `readonly (FactGroup | 'photos')[]`; `useSectionInView` already takes
`readonly string[]`), and it holds an `uploading` boolean fed by
`onUploadingChange: (uploading: boolean) => void`, which it passes to `useLeaveGuard`. The
**checklist is untouched** — it still maps `FACT_GROUPS` only.

`useLeaveGuard(unsaved, saving, uploading)` gains a third input and returns the same view shape.
`guarding` becomes `unsaved.length > 0 || uploading`. The description is the unsaved/saving line when
sections are unsaved, then the upload line when an upload runs; the title is the existing
«Leave with unsaved changes?» while any section is unsaved, and the new «تغادر أثناء رفع صورة؟ /
"Leave while an upload is running?" when only an upload is running. Nothing about the existing wording
changes when no upload runs, so the existing tests stay true.

**Components** (all in `components/photos/`):

| Component | Props | Renders |
|---|---|---|
| `PhotosCard` | `{ id, title, description, children }` | `Card` (`id` = the navigation's anchor, `scroll-mt-28 lg:scroll-mt-20` as `SectionCard`/`ReadOnlyCard` do) with `CardHeader`/`CardTitle`/`h2`/`CardDescription` and `CardContent`. No form, no footer, no date. |
| `PhotosSection` | `{ spaceId }` | What `usePhotoGallery` returns: the `sr-only` `role="status"` announcement, the list of tiles, or the `EmptyState`, the file input, «إضافة صور» with its reason, the summary line, and `PhotoRemoveDialog`. |
| `ReadOnlyPhotos` | `{ spaceId }` | The same tiles with no actions, inside the same `PhotosCard`, no intro (the intro describes changes) and no picker. |
| `PhotoTile` | `{ tile: PhotoTileView }` | One `<li>`: the thumb (`aspect-video`, `urls.card`, `alt=""` — the tile is named by its actions), the `Badge` on the cover, the `Spinner` + percentage while pending, the failure line, and the actions. |
| `PhotoRemoveDialog` | `{ dialog: PhotoRemoveDialogView }` | The `AlertDialog` of the prototype: `AlertDialogTitle` naming the photo, `AlertDialogDescription` saying what it does, `AlertDialogCancel` «رجوع», `AlertDialogAction variant="destructive"` «حذف», its focus on Cancel. |

`features/spaces/index.ts` **does not change**: the gallery is used only inside the editor, so nothing
leaves the capability.

### 4.3 Every user-facing string, in both languages

Added to `spaces.editor.sections` and a new `spaces.editor.photos` object in
`apps/web/src/shared/copy/english/spaces.ts` and `.../arabic/spaces.ts` (the Arabic file keeps
`satisfies Catalogue['spaces']`). Position: `sections.photos` after `sections.contacts`; `photos`
after `editor.contacts`; `toasts.photoRemoved` after `toasts.restored`.

| Key | English | Arabic |
|---|---|---|
| `sections.photos` | `Photos` | `الصور` |
| `photos.intro` | `Up to 10 photos · JPEG, PNG or WebP · 4 MB each. The first is the cover, and every change is saved at once.` | `حتى 10 صور · JPEG أو PNG أو WebP · حتى 4 ميغابايت للصورة. الأولى هي الغلاف، وكل تغيير يُحفظ فورًا.` |
| `photos.loadFailed` | `We couldn’t load the photos` | `تعذّر تحميل الصور` |
| `photos.empty.title` | `No photos yet` | `لا توجد صور بعد` |
| `photos.empty.text` | `The first photo becomes the cover.` | `الصورة الأولى تصبح الغلاف.` |
| `photos.cover` | `Cover` | `الغلاف` |
| `photos.photo({position})` | `Photo ${position}` | `الصورة ${position}` |
| `photos.choose` | `Add photos` | `إضافة صور` |
| `photos.limitReason` | `Up to 10 photos — remove one to add another` | `الحد 10 صور — احذف صورة لتضيف غيرها` |
| `photos.summary({uploaded, selected})` | `Uploaded ${uploaded} of ${selected}; the limit is 10 photos` | `رُفعت ${uploaded} من ${selected}؛ الحد 10 صور` |
| `photos.before` | `Before` | `قبل` |
| `photos.beforeNamed({photo})` | `Before: ${photo}` | `قبل: ${photo}` |
| `photos.after` | `After` | `بعد` |
| `photos.afterNamed({photo})` | `After: ${photo}` | `بعد: ${photo}` |
| `photos.makeCover` | `Make it the cover` | `اجعلها الغلاف` |
| `photos.makeCoverNamed({photo})` | `Make ${photo} the cover` | `اجعل ${photo} الغلاف` |
| `photos.removeNamed({photo})` | `Remove ${photo}` | `إزالة ${photo}` |
| `photos.removeDialog.title({photo})` | `Delete ${photo}?` | `حذف ${photo}؟` |
| `photos.removeDialog.description` | `It leaves the space’s page at once and cannot be brought back.` | `تختفي من صفحة المساحة فورًا ولا يمكن استرجاعها.` |
| `photos.removeDialog.cancel` | `Back` | `رجوع` |
| `photos.removeDialog.confirm` | `Delete` | `حذف` |
| `photos.preparing` | `Preparing…` | `جارٍ التحضير…` |
| `photos.uploading({percent})` | `Uploading ${percent}%` | `جارٍ الرفع ${percent}٪` |
| `photos.unsupported` | `Unsupported format; choose JPEG, PNG or WebP` | `صيغة غير مدعومة، اختر JPEG أو PNG أو WebP` |
| `photos.tooLarge` | `Larger than 4 MB; choose a smaller photo` | `أكبر من 4 ميغابايت؛ اختر صورة أصغر` |
| `photos.rateLimitedMany` | *(none)* *(the shared `errors.rate_limit` line and the countdown are used)* | |
| `photos.retry` | `Try again` | `إعادة المحاولة` |
| `photos.drop` | `Take it off the list` | `أخرجها من القائمة` |
| `photos.moved({photo, position, total})` | `${photo} is now at position ${position} of ${total}` | `${photo} الآن في الموضع ${position} من ${total}` |
| `photos.covered({photo})` | `${photo} is the cover now` | `${photo} هي الغلاف الآن` |
| `photos.orderChanged` | `The gallery changed since this page was opened. Reload it to see the current order.` | `تغيّرت الصور منذ فتح هذه الصفحة. أعد التحميل لترى الترتيب الحالي.` |
| `photos.galleryFull` | `The space already has 10 photos. Remove one to add another.` | `للمساحة 10 صور بالفعل. احذف صورة لتضيف غيرها.` |
| `photos.verifiedMeanwhile` | `The space was verified meanwhile: its owner edits its photos now.` | `تم توثيق المساحة في هذه الأثناء؛ مالكها يعدّل صورها الآن.` |
| `photos.deletedMeanwhile` | `The space was deleted meanwhile.` | `حُذفت المساحة في هذه الأثناء.` |
| `toasts.photoRemoved({photo})` | `${photo} deleted` | `حُذفت ${photo}` |
| `editor.leave.uploadTitle` | `Leave while an upload is running?` | `تغادر أثناء رفع صورة؟` |
| `editor.leave.uploading` | `A photo that has not finished uploading will be lost.` | `ستفقد أي صورة لم يكتمل رفعها.` |

Notes that bind the writing: no line concatenates — a varying value arrives through a named
parameter (`String(position)` inside a template literal, as `spaces.editor.hours.shift` and
`prices.row` already do); no line carries markup; `٪` in Arabic and `%` in English keep the owner's
pre-approved wording and Western digits, as the foundation's *Digits* rule requires; no plural
categories are needed, because D5's line is a fixed construction and `arabicPlural` would contradict
the owner's words. **No new line is added under `errors`** — 413, 415, 409, 403, 404, 429 and the
network failures all already have one.

### 4.4 Each state, named to the design system's components

| The gallery's state | What the admin sees | Layer component used |
|---|---|---|
| The gallery is loading | one skeleton line where the list will be | `Skeleton` |
| The gallery failed | the editor's own failure shape, with "Try again" | `components/editor/EditorFailure.tsx` (reused) + `Button` |
| No photos | icon-less `EmptyState`, `titleAs="h3"` so the outline stays | `EmptyState` |
| The photos are there | a `<ul className="grid grid-cols-2 gap-3 md:grid-cols-3">` of tiles | `Card`, `Badge`, `Button` |
| A tile is the cover | a `Badge variant="primary"` over the thumb, top-start | `Badge` |
| A tile is being prepared | `Spinner` + «جارٍ التحضير…» | `Spinner` (**never** a hand-drawn bar — the binding decision) |
| A tile is uploading | `Spinner` + «جارٍ الرفع 45٪» in `text-caption text-muted-foreground` | `Spinner` |
| A tile failed | a `text-destructive` caption inside `role="status"`, then `Button variant="outline" size="sm"` «إعادة المحاولة» and `Button variant="ghost" size="sm"` «أخرجها من القائمة» | `Button` |
| The gallery is at ten | `Button variant="outline"` `disabled`, with the reason in `text-caption text-muted-foreground` beside it — the sections' limit pattern | `Button` |
| A move or a cover landed | an `sr-only` `role="status"` line naming the photo | — |
| A write is waiting | the tile's buttons `loading` / `aria-busy`, so the keyboard keeps its place | `Button` |
| A removal is asked for | a destructive `AlertDialog` opening on Cancel, focus on it | `AlertDialog` |
| A refusal with no domain code | its request reference under the line | `components/toast/ActionRefusal.tsx` (the same reader) |
| The page is left while an upload runs | the editor's own dialog, retitled | `AlertDialog` (`LeaveDialog`) |
| The whole section | a card with an `h2`, `scroll-mt-28 lg:scroll-mt-20` | `Card` (`PhotosCard`) |

---

## 5. Stronger decisions

Each is a decision inside this item's scope that the plan makes **stronger**, or a rule of the
documents it would otherwise weaken. Nothing here contradicts an authoritative document; each is
listed with what, why, its cost, and the recommendation.

**S1 — Re-encode every chosen file as `image/jpeg` at 0.85, whatever its source type.**
*Why:* all three types the server accepts are re-encoded to WebP there anyway, so the type only
decides the bytes on the wire; one output type is the one every browser can encode, keeps the code to
one branch, and drops a PNG's alpha (a space photograph has none, and nothing else in v1 draws one).
*Cost:* a transparent PNG loses its transparency on the way up.
*Alternative:* keep the source type where the browser can encode it — more branches, no user gain.
*Recommendation:* build the single type.

**S2 — `accept="image/*"` on the file input (the owner, 2026-10-17).**
*Why:* on a phone it opens the gallery and the camera instead of a file browser; it hides no image
type, so a HEIC still reaches its tile and D2's refusal (iOS often converts it to JPEG itself). The
server checks the **content** either way, and the intro line names the three types.
*Cost:* a non-image file cannot be picked at all — the right outcome.
*Not chosen:* no `accept` (a file browser on the phone), or the three-type list (hides HEIC, so D2's
refusal could never be reached).

**S3 — One serial queue in the section's own state, not in TanStack Query; the query cache holds only
`SpacePhoto[]`.**
*Why:* a `File` is a browser object and a percentage is not server state
(`architecture.md` › *Where state lives*: "One component's own state → `useState`"). A `useMutation`
per file would also make the *serial* rule (D3) an accident of timing instead of a fact.
*Cost:* the editor needs one explicit boolean (`onUploadingChange`) to reach the leave guard.
*Recommendation:* build it.

**S4 — No optimistic update on a move, a cover or a removal; the upload's 201 answer is appended.**
*Why:* `architecture.md` §7 allows optimistic updates only for favourites. A move answers 204 with no
body, so the truth is a refetch; an upload answers the whole `SpacePhoto`, which is the server's own
row in the server's own position, so appending it is keeping the answer, not predicting it.
*Cost:* on a weak connection a reorder looks like it did nothing for a moment.
*Recommendation:* build it; correctness and the contract's "the ids must be exactly the space's
photos" rule outweigh a faster animation.

**S5 — A 403 or a 404 on any gallery write goes through `useSpaceAnswer(spaceId).refused`.**
*Why:* #74's web decision S4 already established it for the sections' writes, so a verified space
turns read-only and a deleted one shows the 404 — whatever was read before. The gallery must not
invent a second rule.
*Cost:* the gallery's own `failure` line and the space's own read both speak; the space's wins,
because the page changes shape.
*Recommendation:* build it, and say so in the failure line.

**S6 — The file input is `sr-only` and `tabIndex={-1}`, and the visible `Button` opens it.**
*Why:* the design system has no file control, and this is exactly what the prototype drew; the
button carries «إضافة صور», and the browser gives the input its own platform name in browse mode, so
no control is unnamed and the focus order has one entry for it.
*Cost:* a keyboard user reaches one control, not two.
*Recommendation:* build it.

**S7 — A refused tile offers a retry only when a re-send of the same bytes could succeed.**
*Why:* 413/415/400/422 are the server's verdict on these bytes; a retry button that cannot work is a
lie. `canRetryUpload` is the whole rule, in one pure function both lanes can prove.
*Cost:* one small pure function and a branch in the tile.
*Recommendation:* build it. (After a 413 the tile's only way on is «أخرجها من القائمة» — and, since
the browser has already shrunk the file, a 413 from this screen is in practice unreachable; §*Review
Focus* says so and the report must not claim it was exercised.)

**S8 — A 429 fails its own tile and the queue carries on.**
*Why:* each tile's failure is its own by D3/O7; `useRefusalView` already renders the countdown for
`rate_limit`, so the wait stays in one place; pausing the queue would need a second, untested timer
rule and a new string.
*Cost:* during a burst each remaining tile is refused in turn and shows its own countdown.
*Recommendation:* build it; the 30-per-15-minutes limit is only met by a deliberate burst.

**S9 — Do not write the shared 429 hold key (`spacesKeys.hold`) from the gallery.**
*Why:* that key is the **admin's spaces list**'s own hold, shown by `SpaceActionsHold` above that
list; writing it from the editor would change another screen's behaviour for a refusal this screen
shows itself, and this item's contract is the editor.
*Cost:* two refusals of the same window are held in two places, each on its own screen.
*Recommendation:* do not write it. Recorded here so the omission is deliberate, not forgotten.

**S10 — No new mutation key for the gallery's writes.** `spaceWriteKey` is documented as "every write
on one space's facts, its saves and its confirmations"; photos are explicitly not a fact group, and
`uploading` is already local state reported to the guard. A new key under `['admin','spaces','photos',
…]` would sit one element away from the query key and risk a prefix collision.
*Cost:* none; `useIsMutating` is not used for the gallery.
*Recommendation:* do not add one.

**S11 — `shared/uploads`, not a `shared/api` method.**
*Why:* the owner's principle is to build for the abstraction: shrinking and sending a file is a
platform mechanism a later avatar or another file kind reuses, and `api.post` already takes the
config `onUploadProgress` needs, so **the transport is not touched at all**. `Axios` stays inside
`shared/api` either way.
*Cost:* the progress seam is documented once in `architecture.md` §7 rather than typed on the
`Api` object.
*Alternative:* an `api.upload(url, form, { onProgress })` helper beside `api.getPage`. Equally legal;
it puts one more method on a module three capabilities share, for no second consumer yet.
*Recommendation:* build `shared/uploads`.

**S12 — The gallery's failures are read through `useRefusalView`, with `photos`' own lines for the
codes it knows.** *Why:* one reader for every refusal, its `failureLines` pattern is the form's, and
the tile needs the reference and the countdown for free.
*Cost:* a hook per tile that has a failure. *Recommendation:* build it.

**No rule of the documents is weakened.** The one place a temptation exists — hand-drawing the
prototype's progress bar — is refused by the binding decision at the head of this plan and becomes
finding 73.

---

## 6. Related findings

The open titles were read in `docs/architecture/findings/README.md`; 63, 64 and 67 were opened.

| Finding | Folded? | Why, and the cost |
|---|---|---|
| **63 — A photo's files can outlive it** | **No.** | Backend storage reclamation with no job in v1; the browser cannot decide a file's ownership. Folding it means scheduler and storage work under `apps/api`, which this contract forbids. The gallery's per-tile failure is an **upload** failure and says nothing about a file left behind; nothing here resolves it. |
| **64 — The deployment's headers must let Cloudinary's photos load** | **No.** | A deployment/CSP matter. Folding it means editing the deployment headers and verifying production, outside this item, and the local run (`STORAGE_MODE=local`) cannot prove it. The gallery's `<img src={photo.urls.card}>` makes the header requirement real for the first time on a screen, so the gallery **links** finding 64 rather than resolving it. |
| **67 — The prices table cuts its shift at 768 px** | **No.** | Unrelated responsive work in another section. Acceptance criterion 14 says only that the gallery adds no width pressure to it. |
| **59 — The verified editor cannot name its owner** | **No.** | Owned by the owners item (merged as PR #82); the read-only gallery names no owner either, consistently. |
| **46 / 33 — the deployment's headers for maps and Google** | **No.** | Untouched by this item. |

### New findings this item reserves (73–74)

The prompt reserves **73** and **74**. Each is recorded **only if it is still true when the code is
written**; a finding records a problem, and an unused number is simply unused. If neither holds, say
so in the report and record none.

- **73 — the gallery's per-tile progress has no component in the layer.** The prototype draws a
  `.upload-bar` `role="progressbar"` bar in `docs/design/prototype/masaha/profile-b.jsx`, and
  `foundation.md` §12 has no progress component, while adding shadcn's `Progress` would bring
  `@radix-ui/react-progress`, a dependency the owner has ruled out. The gallery therefore shows the
  layer's `Spinner` with the percentage as text — accessible, honest, and not the designed bar.
  *Resolves when:* the layer gains a progress component (or a token pair a bar may be built from), or
  the owner accepts the spinner and the design is updated.
- **74 — the design's gallery copy states limits the contract no longer has.** The prototype says
  «حتى 10 صور · JPG أو PNG · حتى 5 ميغابايت» / "Up to 10 photos · JPG or PNG · up to 5 MB each",
  while `docs/api/api-contract.md` accepts JPEG, PNG **and WebP** and caps a photo at **4 MiB**. The
  archive under `docs/design/` is a frozen record, so the divergence is permanent and the screen
  cannot make the drawing true.
  *Resolves when:* the design archive is refreshed from the built screens.

Both files are new (`docs/architecture/findings/73-….md`, `74-….md`), in the format of finding 63 —
heading, `**Status:** Open · **Date:**`, **Evidence**, **Resolves when** — and both are added to
`docs/architecture/findings/README.md` under *Open*, each with its own line.

---

## 7. The files it edits

Every path is relative to the repository root. **Nothing in `apps/api` or `packages/shared` is
touched**, and **no licence in the other layer is needed or declared**: the gallery needs nothing
from the API worker, and nothing from `packages/shared`, because every value it reads is already
exported (`SpacePhoto`, `PHOTO_LIMIT`, `PHOTO_MAX_BYTES`, `PhotoUrls`).

### Commit 1 — the shared upload layer (new files only)

| Path | Why |
|---|---|
| `apps/web/src/shared/uploads/index.ts` | The module's only entry (architecture §1). |
| `apps/web/src/shared/uploads/types/UnsupportedImageError.ts` | The shrinker's one typed failure. |
| `apps/web/src/shared/uploads/services/photoGeometry.ts` | `fitInside` and `SHRINK_DEFAULTS`: the pure half of D1. |
| `apps/web/src/shared/uploads/services/photoGeometry.unit.test.ts` | Lane: **unit**. |
| `apps/web/src/shared/uploads/services/shrinkImage.ts` | The browser half of D1. |
| `apps/web/src/shared/uploads/services/shrinkImage.component.test.tsx` | Lane: **component**. |
| `apps/web/src/shared/uploads/services/sendMultipart.ts` | The multipart POST with progress, through `@shared/api`. |
| `apps/web/src/shared/uploads/services/sendMultipart.unit.test.ts` | Lane: **unit**. |
| `apps/web/src/shared/uploads/services/canRetryUpload.ts` | S7's rule, pure. |
| `apps/web/src/shared/uploads/services/canRetryUpload.unit.test.ts` | Lane: **unit**. |
| `apps/web/src/test/fakeCanvas.ts` | A browser stand-in for the canvas and the bitmap decode, in the same shape as `fakePlatform.ts`/`fakeStorage.ts`: a test file only, reached through the globals the production code uses, never `vi.mock`. |

### Commit 2 — the gallery

| Path | New / edited | Why |
|---|---|---|
| `apps/web/src/features/spaces/repository/spacesRepository.ts` | edited | The four calls. |
| `apps/web/src/features/spaces/repository/spacesRepository.unit.test.ts` | edited | The four calls' method, path and body. |
| `apps/web/src/features/spaces/hooks/queryKeys.ts` | edited | `photos(spaceId)`. |
| `apps/web/src/features/spaces/types/PhotoTileView.ts` | new | The tile view model. |
| `apps/web/src/features/spaces/types/PhotoGalleryView.ts` | new | The section's view model. |
| `apps/web/src/features/spaces/hooks/photos/usePhotosQuery.ts` | new | The gallery's read. |
| `apps/web/src/features/spaces/hooks/photos/usePhotoOrder.ts` | new | Before, after, cover, and the announcements. |
| `apps/web/src/features/spaces/hooks/photos/usePhotoOrder.component.test.tsx` | new | Lane: **component**. |
| `apps/web/src/features/spaces/hooks/photos/usePhotoRemove.ts` | new | The `AlertDialog`'s view and the confirmation. |
| `apps/web/src/features/spaces/hooks/photos/usePhotoRemove.component.test.tsx` | new | Lane: **component**. |
| `apps/web/src/features/spaces/hooks/photos/usePhotoGallery.ts` | new | The composition the section renders. |
| `apps/web/src/features/spaces/hooks/photos/useReadOnlyPhotos.ts` | new | The verified space's gallery. |
| `apps/web/src/features/spaces/components/photos/PhotosCard.tsx` | new | The section's frame: no date, no footer. |
| `apps/web/src/features/spaces/components/photos/PhotoTile.tsx` | new | One tile. |
| `apps/web/src/features/spaces/components/photos/PhotoRemoveDialog.tsx` | new | The `AlertDialog`. |
| `apps/web/src/features/spaces/components/photos/PhotosSection.tsx` | new | The editable gallery. |
| `apps/web/src/features/spaces/components/photos/ReadOnlyPhotos.tsx` | new | The read-only gallery. |
| `apps/web/src/features/spaces/components/photos/PhotosSection.component.test.tsx` | new | Lane: **component**. |
| `apps/web/src/features/spaces/components/editor/SpaceEditor.tsx` | edited | Draws the section in both modes. |
| `apps/web/src/features/spaces/components/editor/SpaceEditor.component.test.tsx` | edited | **Shared with worker B (merged, PR #82)** — see below. |
| `apps/web/src/features/spaces/hooks/editor/useSpaceEditor.ts` | edited | `'photos'` in the section list; `uploading` for the guard. |
| `apps/web/src/shared/copy/english/spaces.ts` | edited | Every English line of §4.3. |
| `apps/web/src/shared/copy/arabic/spaces.ts` | edited | Every Arabic line of §4.3. |

### Commit 3 — uploading in the gallery

| Path | New / edited | Why |
|---|---|---|
| `apps/web/src/features/spaces/hooks/photos/usePhotoUploads.ts` | new | The queue, the limit, the summary. |
| `apps/web/src/features/spaces/hooks/photos/usePhotoUploads.component.test.tsx` | new | Lane: **component**. |
| `apps/web/src/features/spaces/types/PhotoTileView.ts` | edited | The pending states and their fields. |
| `apps/web/src/features/spaces/components/photos/PhotosSection.tsx` | edited | The picker, «إضافة صور», the summary. |
| `apps/web/src/features/spaces/components/photos/PhotoTile.tsx` | edited | The preparing / uploading / failed tile. |
| `apps/web/src/features/spaces/components/photos/PhotosSection.component.test.tsx` | edited | The upload states. |
| `apps/web/src/features/spaces/hooks/editor/useSpaceEditor.ts` | edited | `onUploadingChange` wired to the guard. |
| `apps/web/src/features/spaces/hooks/editor/useLeaveGuard.ts` | edited | The third input (D6). |
| `apps/web/src/features/spaces/hooks/editor/useLeaveGuard.component.test.tsx` | edited | Lane: **component**. |
| `apps/web/src/features/spaces/components/editor/SpaceEditor.tsx` | edited | Passes `onUploadingChange`. |
| `apps/web/src/shared/copy/english/spaces.ts` | edited | `summary`, `preparing`, `uploading`, `unsupported`, `tooLarge`, `retry`, `drop`, `orderChanged`, `galleryFull`, `verifiedMeanwhile`, `deletedMeanwhile`, `toasts.photoRemoved`, `leave.uploadTitle`, `leave.uploading`. |
| `apps/web/src/shared/copy/arabic/spaces.ts` | edited | The same lines in Arabic. |

### Documentation (in commit 3, with the code that makes them true)

| Path | What |
|---|---|
| `docs/features/spaces.md` | **Web behaviour**: a «الصور» paragraph in *The space editor on the web* — the order, the cover, the arrows, the `AlertDialog`, the empty state, the picker, the serial queue, the per-tile progress and failure with its retry, the ten-photo limit and its line, the leave guard, a verified space's read-only gallery, the fact that photos carry no date and confirm nothing. **Web decisions**: S1, S2, S3, S4, S5, S7, S8, S9, S11, S12, each with its reason, today's date and `#85`, appended to the *Web decisions* list only. **Code map › Web**: `hooks/photos/`, `components/photos/` added by name, never as a file list. **Open findings**: 73 and 74 linked once they exist. **Web history**: one line for this item. The *API* parts are not touched. |
| `docs/frontend/architecture.md` | §1's shared-modules list gains `uploads`; §7 gains one line that a multipart upload goes through `api` with `onUploadProgress` and is re-sent only by the user. Two lines, no more. |
| `docs/project/overview.md` | The **Spaces** *Built* line gains the gallery: "and its photos, uploaded and ordered from its own section". |
| `docs/architecture/findings/73-…md`, `74-…md`, `docs/architecture/findings/README.md` | Only if §6 holds true when the code is written. |

### Files shared with another open item

- **`apps/web/src/features/spaces/components/editor/SpaceEditor.component.test.tsx`** is the one file
  worker B (OWNERSREAD, **merged** as PR #82) also edited, and it is edited here too. Both sides are
  already in `origin/main` (verified at the head of this plan), so there is nothing left to
  sequence: the change appends to the merged fixture and adds gallery assertions. Its `renderEditor`
  must answer `GET /admin/spaces/7/photos` (or the gallery's own query fails in every existing test),
  and its **existing** assertion `toEqual(['The space','Opening hours','Prices','Amenities','Contacts'])`
  in *"lists its sections in a navigation, the one in view marked"* **must become a six-item list** —
  a recorded change to an existing test, made because the behaviour changed on purpose, not a
  convenience. Its *five groups* checklist assertion is **not** changed.
- **`routes.component.test.tsx`** is touched by B and **not** by this item: the gallery adds no route
  and the editor is reached exactly as it is.
- **ADMINLIST's files** (`features/space-links/**`, `features/spaces/types/SpaceRef.ts`,
  `features/spaces/hooks/menu/**`, `features/spaces/hooks/delete/useRestoreSpace.ts`,
  `features/spaces/components/menu/**`, `pages/dashboard/admin/SpacesPage.tsx`, the `spaceLinks`
  catalogues) are **none of them needed**: the gallery reads the space id from the route, asks for
  the photos with its own key, and never shows on the admin's list.
- **Shared, append-only documents** — `docs/features/spaces.md`'s *Decisions* and *History* (the Web
  part only), `docs/project/overview.md`'s *Built* line and the findings index — may be written by
  another item at the same time. Keep to this item's own sentences and take the fast path
  (a rebase that keeps both sides, `format:check` alone, one push) if only documents conflict.

**Total: 44 files** (11 new in commit 1, 23 in commit 2, 4 new in commit 3, 6 documents), plus
**commit 0's files (§14, about 22, several shared with the gallery's)** — still under 70.

---

## 8. Design issues

Found while reading the design against the code and the decisions. **Each is built only once the
owner's reply approves this plan** (workflow §2, phase 2).

1. **The designed progress bar has no component, and the approved answer is the spinner.** The
   prototype draws `.upload-bar` with `role="progressbar"` and an inline `style={{ width }}` — a CSS
   class and a style outside the layer, which `foundation.md` §3 and `check:classes` forbid. **Built:**
   the layer's `Spinner` with the percentage as text, per the binding decision. *Recorded as finding
   73.*
2. **No preview image on a tile that has not been stored yet.** The prototype draws
   `URL.createObjectURL(file)` in the thumb. **Built:** the tile shows the file's name and the pending
   state instead, and its thumb appears from the server's `urls.card` the moment the row is written
   (the API stores the file *before* the transaction, so this is within the same request). *Why:*
   `URL.createObjectURL` needs a revoke path or it leaks, and jsdom has no implementation, so a
   preview would add a lifecycle and a test stub for a thumbnail the admin sees a moment later.
   *Cost:* the admin does not see the photo while it travels. *Alternative:* an object URL per tile,
   revoked in an effect — say the word and it is built instead.
3. **The tile carries no visible position number.** The prototype has none, and the arrows read as
   "move this one earlier/later", so the number is only needed by a screen reader, where every action
   name carries it («قبل: الصورة 3»). *Cost:* a sighted admin cannot read out a photo's number while
   telling someone else which one to move. *Alternative:* a `text-caption` position line under each
   thumb.
4. **The picker's file input is `sr-only`.** The prototype marks it `sr-only tabIndex={-1}` behind a
   button; the layer has no file control, and adding one is a new component and a new dependency,
   which this item may not do. *Cost:* a keyboard user reaches one control, not two, and no custom
   "no file chosen" text is possible. *Recorded* in the plan rather than as a finding, since the
   prototype already drew exactly this.
5. **The prototype's copy is out of date** (5 MB, JPG/PNG only). **Built:** the contract's real limits,
   as listed in `photos.intro`. The frozen drawing stays as it is — **finding 74**.

Everything else in the design agrees with the settled decisions and is built as drawn: the two-column
grid that becomes three from `md`, the cover badge over the thumb, the ghost icon buttons in one row
with the delete at the end, «اجعلها الغلاف» below them on a non-cover tile, the destructive
`AlertDialog` opening on Cancel, the disabled «رفع صور» with its limit note, and the `sr-only`
`role="status"` announcements.

---

## 9. Tests: lane, title, and the break each catches

Every new test is **seen failing in its own lane before the code that passes it**, and is written by
hand, never computed by the code under it (testing §3, rules 5–7). A red test is never committed.
The suffixes pick the lane; `apps/web/vite.config.ts` runs `unit` in node and `component` in jsdom.

### Unit lane — `npm run test:unit` (node)

| # | File · title | Break it catches |
|---|---|---|
| 1 | `photoGeometry.unit.test.ts` · *fits a photo inside the longest side it is given, and never enlarges one* | The longest side taken from the width instead of the longer of the two; enlarging a small photo; a zero or negative side after rounding. |
| 2 | `canRetryUpload.unit.test.ts` · *offers a retry only for a failure another attempt could cure* | Offering a retry on 413/415/422 (a lie); hiding one after a network failure or a 429 (the common case). |
| 3 | `sendMultipart.unit.test.ts` · *sends one part under its field name through the one client, and reports its progress* | Bypassing `api` and calling Axios directly; the wrong field name or a second part; the envelope leaking; progress never reaching the caller. |
| 4 | `sendMultipart.unit.test.ts` · *rejects a refusal with the transport’s AppError* | The raw Axios error escaping, so a component could see a transport object. |
| 5 | `spacesRepository.unit.test.ts` (edited) · *reads, uploads, removes and orders a space’s photos on the contract’s paths* | A path, a method or a body drifting from `api-contract.md §5 › Photos` (`{ ids }`, the part named `photo`). |

### Component lane — `npm run test:component` (jsdom)

| # | File · title | Break it catches |
|---|---|---|
| 6 | `shrinkImage.component.test.tsx` · *re-encodes a photo turned as its EXIF says, at 1600 px on its longest side, as JPEG at 0.85* | The longest side never bounded (a 4000×3000 fake comes out 1600×1200); a missing or wrong quality; a re-encoded file keeping the source's extension or type; an enlargement (an 800×600 fake stays 800×600); the decode called without `imageOrientation: 'from-image'` (the fake records the options it was called with). The numbers are written in the test by hand, never read from `SHRINK_DEFAULTS`. |
| 7 | `shrinkImage.component.test.tsx` · *refuses a file the browser cannot decode, and one it cannot draw* | A HEIC reaching `sendMultipart`; a canvas-less browser crashing instead of refusing. |
| 8 | `usePhotoOrder.component.test.tsx` · *sends every photo’s id in the order the admin chose, and shows the new order once the server has accepted* | A partial id list (the contract refuses it); a wrong permutation; the order changing on screen before the answer; no refetch after the 204. |
| 9 | `usePhotoOrder.component.test.tsx` · *makes a photo the cover by sending it first* | «اجعلها الغلاف» sending a list where the photo is not first; the cover badge not moving; the control showing on the cover itself. |
| 10 | `usePhotoOrder.component.test.tsx` · *says the gallery changed and shows the server’s order when it refuses the move (409)* | A 409 read as a success; the stale order left on screen. |
| 11 | `usePhotoRemove.component.test.tsx` · *asks before it removes a photo, and says what it removed* | Removing without the dialog; the dialog not naming the photo; no toast. |
| 12 | `usePhotoRemove.component.test.tsx` · *says the space was verified or deleted and fetches the space again on a 403 or a 404* | The page staying editable after the space became verified; the 404 not shown. |
| 13 | `usePhotoUploads.component.test.tsx` · *uploads chosen files one at a time, in the order chosen, each with its own progress* | Two requests in flight; one shared percentage across tiles; the queue reordered; a new queue starting a second upload. |
| 14 | `usePhotoUploads.component.test.tsx` · *keeps a failed file on its own tile with a retry where one can work, and refuses a file the browser cannot decode* | A failure with no retry; a retry on a 413; a HEIC reaching the network; one tile's failure clearing another's. |
| 15 | `usePhotoUploads.component.test.tsx` · *uploads what fits and says how many of the selection went up* | The ten-photo cap passed; a count that lies (3 of 5 said as 5 of 5, or none said). |
| 16 | `PhotosSection.component.test.tsx` · *shows the photos in order with the cover, the picker and each tile’s actions* | The cover not marked; an action unnamed or unreachable; the section's frame carrying a date or a Save. |
| 17 | `PhotosSection.component.test.tsx` · *shows the empty state, and the limit beside a disabled add at ten* | A different empty wording; a disabled control with no reason shown. |
| 18 | `PhotosSection.component.test.tsx` · *shows a verified space’s photos with no control to change them* | Any write control rendered on a verified space — the one failure the server would catch anyway. |
| 19 | `PhotosSection.component.test.tsx` · *names each move and cover in a live region* | A silent reorder: a sighted-only change with no announcement for a screen reader. |
| 20 | `useLeaveGuard.component.test.tsx` (edited) · *asks while an upload is running, names no section, and lets a move within the page through* | Leaving silently during an upload; the dialog naming a section that is not unsaved; an anchor move blocked. |
| 21 | `useLeaveGuard.component.test.tsx` (edited) · *goes on by itself once the upload has ended* | A dialog left blocked after the queue finished. |
| 22 | `SpaceEditor.component.test.tsx` (edited) · *lists Photos after Contacts and draws the section, editable or read-only* | The section or its navigation item missing; the item in the wrong place; controls drawn on a verified space. |

**Not run here:** `npm run test:api` locally — nothing in `apps/api` or `packages/shared` changes, and
the photos' endpoints are already proven by the API lane's own tests. CI runs it on the PR
regardless, and the report must say so.

**Duplication check** (testing §1): the repository's method/path/body is proven once (unit 5); the
hooks' own decisions — which ids, which queue, which failure line — are proven in the hook's
component test; the rendering — which state, which label, what is disabled — is proven in the
component test. Nothing is proven twice, and nothing is proven only by a browser.

---

## 10. Review Focus — the inputs no planned test exercises

- **A 413 from this screen.** The browser has already bounded the photo to 1600 px and re-encoded it,
  so the server's 4 MiB is unreachable in practice. The path must exist and be honest, but a run
  cannot exercise it: **the report must say it was not exercised**, not that it passed.
- **A very large source** (50 MP from a phone): the shrink bounds the result, but the decode itself
  can exhaust a weak phone's memory. Watch it in the real run; if it fails, that is a finding, not a
  bug to fix silently.
- **A 415**: a file renamed to `.jpg` that is not an image — the server's content check refuses it.
- **A mixed selection**: one HEIC, one refused as too large, one that goes up, one with a dropped
  connection. The order, the counts and the summary must all stay true.
- **Two admins in the same gallery**: one moves, the other removes; the loser's 409 and its refetch.
- **A space verified while the gallery is open**: the next write's 403, the page turning read-only
  under the admin's hands.
- **30 uploads in 15 minutes**: the 429 on a tile, its countdown, the rest of the queue, and the
  admin's retry afterwards.
- **Focus** after a move, a cover, a removal, a retry and a dialog close; and the keyboard order
  inside a tile (before, after, cover, remove).
- **360 px**: two columns of tiles with four actions each; the disabled «إضافة صور» and its reason on
  one line; long Arabic labels.
- **A broken `urls.card`** and a slow image; dark-theme contrast on the `primary` cover badge.
- **`beforeunload`**, Back/Forward and a deep link while a queue is running; then choosing Leave.
- **Production Cloudinary**: not exercised by a local run — finding 64 stays open and the report must
  not claim otherwise.
- **The design archive** (`docs/design/prototype/**`) is not edited here; finding 74 records why.

---

## 11. The commits

Four atomic commits, each a complete working unit, each with its code, its tests and the documents
it makes true **in the same commit** (workflow §3). Subjects are `<type>(<scope>): <description>`,
imperative, lowercase, no period. **A changed row state and its action change go in one commit**
(#84's review, R84-013).

| # | Subject | Length | What is in it |
|---|---|---|---|
| 0 | `fix(space-links): correct the deleted spaces list` | **49** / 50 | §14 whole: #84's review corrections — code, tests, both catalogues, the documents, findings 69–70. **First in the history.** |
| 1 | `feat(web): add a shared image upload layer` | **42** / 50 | `shared/uploads/**` — `fitInside`, `SHRINK_DEFAULTS`, `shrinkImage`, `sendMultipart`, `canRetryUpload`, `UnsupportedImageError`, the module's `index.ts` — with its three unit tests, its one component test, and `src/test/fakeCanvas.ts`. No feature, no copy, no document: nothing in the app reads it yet, and a reviewer can read the layer alone. |
| 2 | `feat(spaces): add the editor's gallery` | **38** / 50 | The four repository calls and their test, `spacesKeys.photos`, the photo types, `usePhotosQuery`, `usePhotoOrder`, `usePhotoRemove`, `usePhotoGallery`, `useReadOnlyPhotos`, `PhotosCard`, `PhotoTile`, `PhotoRemoveDialog`, `PhotosSection`, `ReadOnlyPhotos`, the editor's wiring (`SpaceEditor`, `useSpaceEditor`) and their tests, and every catalogue line commit 3 does not add. |
| 3 | `feat(spaces): upload photos in the gallery` | **42** / 50 | `usePhotoUploads` and its test, the pending states of `PhotoTileView`, `PhotoTile` and `PhotosSection` and their tests, the leave guard's third input and its two tests, the remaining catalogue lines, `docs/features/spaces.md`, the two lines in `docs/frontend/architecture.md`, the *Built* line in `docs/project/overview.md`, and findings 73–74 with the index. |

The PR title is commit 2's subject, `feat(spaces): add the editor's gallery` — the one line that
names the item.

Rules the executor follows: **stage by path**, never `git add -A` / `git add .`; `git status --short`
before each commit; `npm run lint` and `npm run typecheck` after each commit; the lanes once, on the
head; **no tool attribution** in any commit, message or document. A fix needed **before the push**
folds into the commit it belongs to (`git commit --fixup <sha>`, then
`GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash origin/main`); after the push, a review fix is
a new commit on top (the owner's exception for small review fixes). Commit messages are written to a
UTF-8 file and passed with `git commit -F <file>` — no literal `\n`, no `\u` escapes in a body.

---

## 12. Verification, and the executor's procedure

This procedure is self-contained. No step depends on any Claude skill.

### 12.1 Before the branch

1. `cd C:\Users\basel\masaha-design` and `git fetch origin`. Read the code from `origin/main` with
   `git show origin/main:<path>`, `git ls-tree -r --name-only origin/main <dir>` and
   `git grep <pattern> origin/main -- <paths>`. **Never check anything out in that folder** — it is a
   clean worktree kept for reading.
2. Confirm both preconditions are merged into `origin/main`:
   `git log --oneline origin/main -30` must show the ADMINLIST merge (PR #84) and the owners-read
   merge (PR #82). **If either is missing, stop and say so.**
3. Work in `C:\Users\basel\masaha` — worker A's folder, now that ADMINLIST has merged. Confirm it is
   clean (`git status --short` empty) and on `main`, then `git pull`.
4. Cut the branch: `git switch -c feat/space-gallery origin/main`.
5. Re-read the merged versions of the files in §7 before editing them; the merged tree, not
   `origin/main`'s shape from this plan's date, is what counts.

### 12.2 While implementing

6. For each new test, run it **once in its own lane before** the code that makes it pass, and record
   the failure. Implement. **Commit 0 first (§14)**, then commit 1 → stage its eleven paths by name
   → `git status --short` → commit → `npm run lint` → `npm run typecheck`. Then commit 2 the same
   way, then commit 3.
7. After each commit, `npm run lint` and `npm run typecheck` must be clean. A fix folds into the
   commit it belongs to (§11) — nothing has been pushed yet.

### 12.3 On the head — one lane at a time, in this order

```
npm run test:unit
npm run test:component
$env:NODE_ENV='production'; npm run build      # PowerShell; in bash: NODE_ENV=production npm run build
npm run check:build
npm run lint
npm run typecheck
npm run check:classes
npm run format:check
npm run check:links
```

`npm run test:api` is **not** run locally and the report must say so with the reason (no API or
shared-package behaviour changes; CI runs the lane on the PR).

### 12.4 The real run

8. In `C:\Users\basel\masaha`: start Docker Desktop, then `docker start masaha-postgres-1`
   (**never** `npm run db:up`, in any folder); `npm run db:migrate` (nothing new should apply); `npm run db:seed`
   (with `SEED_ADMIN_*` set; add `SEED_DEMO=true` and `SEED_DEMO_PASSWORD` for the demo space, owner
   and reception account). `STORAGE_MODE=local` is the default in `apps/api/.env`, which writes the
   files under `apps/api/.storage/` and serves them at `/api/v1/files/…` through the dev proxy.
9. Start the API (`npm run dev -w @masaha/api`, port **3320**, `GET /health` reports `"db": "up"`)
   and the web (`npm run dev`, port **5320**). Sign in as the seeded admin at
   `http://localhost:5320/dashboard/admin/spaces`.
10. Exercise, and screenshot each to `C:\Users\basel\Downloads\gallery-shots\`:
    - **An unverified space** — create one through **Add space** (the seed's demo space is verified);
      the editor opens on the new space. Check the empty state; add 2–3 photos (JPEG, PNG, WebP),
      watching each tile's own progress; choose a HEIC (a refused tile with the exact line, and **no
      request**); choose a renamed `.jpg` that is not an image (a 415 on its tile); drop the
      connection mid-upload (a failure with «إعادة المحاولة», and the retry succeeding);
      choose more files than the room left («رُفعت 3 من 5؛ الحد 10 صور»); fill the gallery to ten and
      check «إضافة صور» disabled with its reason; «اجعلها الغلاف» on a middle photo; «قبل»/«بعد» at the
      boundaries; a removal through the `AlertDialog` and its toast; the `sr-only` announcements in a
      screen reader or the accessibility tree; a navigation away **during** an upload (the dialog,
      its title and its line) and a reload during one (the browser's prompt); an anchor chip during
      an upload (no question).
    - **A verified space** — the seeded demo space: the same gallery with **no** control to change
      anything.
    - **A portrait photo taken on a phone** (EXIF orientation 6): it must stand upright in the tile
      and on the space's page.
    - **Commit 0 (§14):** the deleted list (`?status=deleted`) — one muted «محذوفة · date» line, no
      badge, «—» for freshness, «استرجاع» only; the phone sheet's badge and its clear with
      `?stale=true` on; the delete dialog's new line; the chip «قديمة أو ناقصة»; whether a verified
      space with no owner shows on the list (§14, finding 70).
    - Every case in **Arabic and English, RTL and LTR, light and dark, at 360, 768 and 1440 px**, and
      the keyboard alone (Tab through a tile; open the dialog with the keyboard; Cancel keeps the
      focus where it was).
    - Confirm the prices table at 768 px is no worse than finding 67 describes, and did not get worse
      because of this section.
11. Stop both servers by PID and **check ports 3320 and 5320 are free** (a `tsx watch` API can survive
    Ctrl+C on Windows). If any case above cannot be run, write the exact blocker in the report and
    **do not claim it passed**.

### 12.5 Scope, push, pull request

12. Re-read the diff: `git status --short` and `git diff origin/main...HEAD --stat`, and check every
    path against §7. Anything outside §7 is either reverted or raised in the report — never
    "improved" here.
12b. **The PR number.** Issues and PRs share one sequence; the highest today is #84, so this PR
    should be **#85**. Check: `gh api "repos/Basel-Ghonaim/masaha/issues?state=all&per_page=1" --jq '.[0].number'`
    must print `84`. If it prints more, use that number + 1 in every `#85` of the documents, folded
    into the commits that hold them (§11). After `gh pr create` (step 14), if the PR's number is not
    the one written, stop and ask.
13. `git push -u origin feat/space-gallery`.
14. Open the pull request with the description written out in §12.6:

```
gh pr create --assignee @me --label feat --label area:web --label area:docs `
  --title "feat(spaces): add the editor's gallery" --body-file <the file written below>
```

(`gh label create` first if `area:docs` does not exist yet.) **Never merge.**
15. `gh pr checks <number>` until CI is green on the pushed head, and GitHub shows **CLEAN**.
16. The early conflict check (workflow §9): for every other open PR,
    `git fetch origin <branch>` then `git merge-tree --write-tree origin/<other-head> HEAD` (git
    ≥ 2.38). A non-zero exit or a conflict in the output is a conflict: note it, with the order it
    implies, in the report. A conflict only in documents takes the fast path — rebase keeping both
    sides, `npm run format:check` alone, one push. A conflict in code adds `lint` and `typecheck`.
17. **Only after CI is green and the PR is CLEAN**, write the report to
    `C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\GALLERY_REPORT.md`: the head and the three commits
    with their lengths; what was run and what was not (the API lane, and any real-run case blocked);
    the breaks each new test was seen failing on; the problems met and how they were solved;
    **anything that behaved unexpectedly, even unsolved**; the conflict check's result; any departure
    from this plan with its reason; and the findings recorded, or none. Then summarise it in the
    conversation.

### 12.6 The pull request description, written out

```
## Summary

The admin space editor gains its sixth section, «الصور» / Photos, on the photos API from #77.

- A domain-free upload layer in `shared/uploads`: `fitInside` (pure), `shrinkImage` (browser
  decode → draw → encode, longest side 1600, quality 0.85, always `image/jpeg`), `sendMultipart`
  (one multipart POST through the app's one client, with `onUploadProgress`), and `canRetryUpload`
  (pure). It names no space and no photo, so a later avatar reuses it. The transport is untouched:
  `api.post` already takes an `AxiosRequestConfig`.
- The gallery: the photos in the server's order, the first marked as the cover, «اجعلها الغلاف»,
  «قبل»/«بعد» to move one, removal through an `AlertDialog` with a toast, the empty state, and a
  verified space's copy read-only with no write control at all. No date, no confirm, no save —
  photos are no fact group.
- Uploading: «إضافة صور» opens a many-file picker, files go up **one at a time** in the order
  chosen, each tile has its own preparing/uploading state with its own percentage and its own
  failure with «إعادة المحاولة» where a re-send could work; a file the browser cannot decode is
  refused on its tile with no request sent; the ten-photo limit uploads what fits and says
  «رُفعت 3 من 5؛ الحد 10 صور»; and the editor's leave guard asks while an upload runs.
- First commit — #84's post-merge review: the phone's Filters sheet counts and clears only its own
  two filters; a deleted row is one muted «محذوفة · date» line as the design draws it; the delete
  dialog says where a deleted space goes; the chip reads «قديمة أو ناقصة»; the restore's pending
  double click and the status transition are proven; the documents carry #84 and drop finding 50
  from the open list; findings 69–70 recorded.

## Scope

- Acceptance criteria: §2 of the plan, all fourteen.
- Nothing in `apps/api` or `packages/shared`. No new dependency, no new design-system component, no
  new colour, font or CSS outside the layer, no new error code, no new `errors` catalogue line.

## Out of scope

- Drag and drop, captions, bulk actions, an undo for a removal, editing a photo's file, the public
  page's gallery, and the owner/reception web screen.

## Change type

feat — a new capability section plus one new `shared/` platform module.

## Evidence

- `npm run test:unit` — <result>: <n> files, including `photoGeometry`, `canRetryUpload` and
  `sendMultipart`.
- `npm run test:component` — <result>: <n> files, including the gallery's hooks, the section, and the
  leave guard.
- `NODE_ENV=production npm run build` → <result>; `npm run check:build` → <result> (the gallery is
  dashboard-only and stays out of the site's first download).
- `npm run lint`, `npm run typecheck`, `npm run check:classes`, `npm run format:check`,
  `npm run check:links` → <results>.
- **Not run:** `npm run test:api` — no API or shared-package behaviour changes; CI runs the lane on
  this PR.
- **Not exercised by the real run:** <each case that could not be run, and why>.
- Every new test was seen failing in its own lane before the code that passes it: <the list of
  failures, one line each>.

## Screenshots

`C:\Users\basel\Downloads\gallery-shots\` — Arabic and English, RTL and LTR, light and dark, at 360,
768 and 1280/1440 px: <the list of files, by what each shows>.

## Definition of Done

- [x] Acceptance criteria met, scope kept.
- [x] Lint and typecheck clean; the production build passes; `check:build` passes.
- [x] Tests in the owning lane (`testing.md` §1), each seen failing first; no behaviour proven twice.
- [x] No hardcoded user-facing text; both catalogues updated; `catalogues.unit.test.ts` passes.
- [x] Checked in RTL and LTR, light and dark, phone and desktop.
- [x] Authorization remains the server's; a verified space's gallery is read-only in the web because
      the server's `can()` refuses every write, not instead of it.
- [x] Triggered documentation updated in this PR: `docs/features/spaces.md` (web behaviour, web
      decisions, code map, history), `docs/frontend/architecture.md` (the shared module and the
      multipart rule), `docs/project/overview.md` (Spaces — Built), and findings <73/74/none> with the
      index.
- [x] One home per fact; nothing claimed that is not built.
- [x] Every claim above names the test or the command that proves it.
- [x] Atomic history, pushed; this PR is ready for review and **not merged**.
```

---

## 13. Decisions needed from the owner

> **Taken — 2026-10-17.** See the approval at the top: every item below is approved, S2 amended.

The settled decisions (D1–D6, A1, O7, DI-33) cover the behaviour, the API contract is already built,
the file count is 44 — under the prompt's split threshold — and no decision is left to take alone.
What the owner is asked for is the **approval of this plan**, which covers:

1. **S1** — re-encode every upload as `image/jpeg` (one output type; a PNG's transparency is lost).
2. **S2** — no `accept` on the file input, so a HEIC can reach the tile and be refused with the
   owner's own words.
3. **S4** — no optimistic reorder: the order changes after the server's 204 and its refetch.
4. **S7** — no retry offered on a refusal the server has already judged (413/415/400/422).
5. **S8** — a 429 fails its own tile and the queue carries on, each tile counting down.
6. **§8 design issues 2 and 3** — no preview thumbnail on a tile still being uploaded, and no visible
   position number on a tile.
7. **§6** — findings 73 and 74, if they still hold when the code is written.

### Stop and ask

Stop, and say so, rather than deciding any of these:

- ADMINLIST (PR #84) or OWNERSREAD (PR #82) is **not** in `origin/main`, or their merged code makes
  any file of §7 read differently from this plan.
- The gallery needs any change in `apps/api`, `packages/shared`, Prisma, the storage adapter, the
  image core, a rate limit, `can()` or an API error code — **including a new error code**, which the
  `add-error-code` rules own and the API worker must write.
- `shared/api` cannot carry `onUploadProgress` through the config `api.post` already takes, and the
  transport would have to change to get a progress event.
- The per-tile progress cannot be expressed with `Spinner` + text and would need a new
  design-system component, a new token or a new dependency.
- The work would exceed about 70 files, or need a second Work Item (the *shared* upload layer split
  from the *gallery*) — propose the split, do not take it.
- No lane can own a behaviour, or a focused test still fails after three root-cause attempts.
- `SpaceEditor.component.test.tsx` cannot be edited without undoing something OWNERSREAD built.
- The local run cannot exercise the editable gallery at all (no unverified space reachable, no
  admin credentials, no database) — record the blocker; claim nothing.
- A failure's cause is not found after three attempts, or a stop rule in workflow §8 fires.

---

## 14. Commit 0 — the post-merge review of #84 (the owner, 2026-10-17)

Source: `C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\REVIEW84_OPENCODE_REPORT.md` — read each
finding there for its evidence and line numbers; **re-read the files on the merged tree** before
editing. One commit, `fix(space-links): correct the deleted spaces list` (49), **before** commit 1.
Each item: what, where, the test that proves it (seen failing first), and the document line.

| # | Review | The change | Test (lane) — its break |
|---|---|---|---|
| 0.1 | R84-001 | `hooks/admin-list/useAdminSpacesFilters.ts`: `applied` counts **`place` and `status` only**; `clearFilters` writes `{ place: null, status: undefined }` and keeps the search **and** `stale`; its JSDoc says "the place and the state". `anyApplied` / `clearAll` (the no-match state's «مسح الفلاتر») still count and clear everything. | `AdminSpacesList.component.test.tsx` (the phone sheet) and `useAdminSpacesList.component.test.tsx`: with `?status=hidden&stale=true` the button reads «Filters, 1 applied» / `count: 1`, and the sheet's clear keeps `stale=true` in the address (component) — break: count `stale` again. |
| 0.2 | R84-006 (the owner: **follow the design**) | `services/rowView.ts` + `types/AdminSpaceRowView.ts`: a **deleted** row has `state: []` and `freshness: []`; its status reads one muted line from `deletedOn`. The `deletedOn` line becomes the design's: Arabic `` `محذوفة · ${date}` ``, English `` `Deleted · ${date}` `` (the existing key, both catalogues). The table's state cell shows that line in `text-muted-foreground`; its freshness cell a muted «—» with `aria-hidden="true"`; the card shows the line and no badge list. Live rows are unchanged (A3 holds for them). | `rowView.unit.test.ts` (unit): a deleted verified row has no badge and the line «محذوفة · 14 أغسطس» / "Deleted · 14 Aug" — break: keep the verification badge. `AdminSpacesList.component.test.tsx`: the deleted row's cells on desktop and the card on the phone (component). |
| 0.3 | R84-002 | The delete dialog says where a deleted space goes — `spaces.deleteDialog.description`: Arabic «تختفي من الموقع ومن القائمة، وتجدها في «محذوفة» لاسترجاعها.», English "It leaves the site and the list; you’ll find it under «Deleted» to restore it." (the design's own words, `docs/design/prototype/Admin spaces.html:122`). | An existing dialog test that reads the description, updated by hand; if none reads it, add the assertion to the delete dialog's component test. |
| 0.4 | R84-003 | Arabic `spaceLinks.adminList.staleOrMissing` → «قديمة أو ناقصة» (DI-26). English stays "Stale or missing". | `catalogues.unit.test.ts` parity stays green; no new test (the label is asserted in English). |
| 0.5 | R84-010 | No code change. | `SpaceActionsMenu.component.test.tsx`: click «Restore», keep the answer pending (the file's `deferred` pattern), click again — one write only (component). Break: drop `restore.isPending` from `waiting` → two writes. |
| 0.6 | R84-011 | No code change. | `useAdminSpacesList.component.test.tsx`: from `/s` to `/s?status=deleted` with a deferred answer — `busy === true` and the previous rows still there (component). Break: no `placeholderData` on a status change. |
| 0.7 | R84-012 | `services/updatedOn.ts`: its comment says "a row's date" (last update or deletion). Name unchanged. | — |
| 0.8 | R84-007, 008, 009, 004, 014 | **Documents:** `docs/features/space-links.md` — line 67 (the sheet counts its two fields), drop finding 50 from *Open findings*, "stale or missing" wherever it still says "stale only" (also `docs/features/spaces.md` and `docs/architecture/data-model.md:85`, and the test title at `AdminSpacesList.component.test.tsx:325`), the freshness decision's wording ("a warning badge each"), line 72: one sentence that **the unlink step has no screen yet** (A4 brings it); a new web decision for 0.2 ("a deleted row is one muted line, as the design draws it — 2026-10-17, #85"). `docs/features/spaces.md` — the restore button sits in the row's actions (line 211); the delete-dialog decision (line 167) amended to the new line, 2026-10-17, #85. **Every #84 decision and history line** in both documents and both finding resolutions (44, 50) ends `2026-10-15, #84` instead of "the deleted-spaces screen". | `npm run check:links` |
| 0.9 | R84-005 | **Record findings** (format of finding 63; both in `docs/architecture/findings/README.md` under *Open*): **69** — "The owners endpoint answers `invalid_format` for a deleted space where the contract names `invalid_choice`" (evidence: `ADMINLIST_BROWSER_ROUND2_REPORT.md` §10, `api-contract.md:553`; resolves when the refusal is a code the contract names). **70** — "A verified space can show no owner on the admin's list" — **only if the real run reproduces it** (space 41 in `masaha_dev`, or any verified row whose owners read «—»); if not reproduced, record nothing and say so in the report. | — |

**Out of commit 0:** R84-013 (history; the rule is now in §11). Nothing in `apps/api` or
`packages/shared`.

**Files (about 22):** `features/space-links/hooks/admin-list/useAdminSpacesFilters.ts`, its two
tests named above, `services/rowView.ts` + `rowView.unit.test.ts`, `services/updatedOn.ts`,
`types/AdminSpaceRowView.ts`, `components/admin-list/AdminSpacesList.tsx` and `AdminSpaceCard.tsx`,
`features/spaces/components/menu/SpaceActionsMenu.component.test.tsx`, the delete dialog's test if one
reads the description, `shared/copy/{arabic,english}/spaceLinks.ts`, `shared/copy/{arabic,english}/spaces.ts`
(shared with commits 2–3 — commit 0 touches only `deleteDialog.description`), `docs/features/space-links.md`,
`docs/features/spaces.md`, `docs/architecture/data-model.md`, findings 44, 50, 69 (70) and the index.

**PowerShell form** of §11's fold: `$env:GIT_SEQUENCE_EDITOR=':'; git rebase -i --autosquash origin/main`.

---

## Appendix — skill map (a map only; no step depends on any of these)

| Step of this plan | The project's skill for it |
|---|---|
| §12.1 — reading, checking the folder, cutting the branch | `start-work-item` |
| Saving this plan before any branch or edit | `write-plan` |
| §12.5 — scope check, staging by path, push, the PR, CI/`CLEAN`, conflicts | `open-pr` |
| §12.5 step 17 — the report, and again after each review-fix round | `final-report` |
| §12.2 step 6 — seeing each new test fail first | `test-driven-development` |
| Any failure or flake — the root cause before the change | `systematic-debugging` |
| §12.3 — every claim names the command that proves it | `verification-before-completion` |

None of these is a dependency: the procedures above are written out in full. The project documents
(`CLAUDE.md`, `docs/development/workflow.md`, `docs/development/testing.md`, the capability's own
document) win over any of them.
