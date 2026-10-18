# MEDIA — a space's photos (the media worker) — plan

> **Approved 2026-10-13** with the reply (`MEDIA_PLAN_REPLY.md`), folded in below. Changes from the draft:
> - the image pipeline's domain-free core lives in `apps/api/src/shared/images/`; `spaces/photos/` passes its sizes in (change 1);
> - the port's `contentType` is any MIME type; the Cloudinary adapter refuses non-`image/*` today and builds the URL from the key's own extension (change 2);
> - `receiveFile` takes its field name and byte limit from its caller (change 3);
> - conventions say the extension points once (a new kind of file is a new consumer; a new provider a new adapter);
> - the owner's §13 answers: 409 with no code; sizes as planned; D13 (a); S2; ADR 0014 *Revised*; pins carry `cover`; no avatar. S1–S10 approved.
> - **`MEDIA_ADDITION.md`:** `schema.prisma` and worker B's files untouched; findings stay 63–64.
> - **Added by `MEDIA_BUILD.md`:** Issue #69's five review leftovers of #73, one commit of their own, first (§9, §11).

## 1. Summary

Builds the whole server side of a space's photos, on `main` once DIRECTORY has merged:
- **the storage port** in `apps/api/src/shared/storage/`: bytes by key, a **local** adapter (development, tests; it serves its own files) and a **Cloudinary** adapter (online; `fetch` + a signed request, no SDK, a plain store with no transformation);
- **the image pipeline** in `spaces/photos/`: `sharp` decodes (the content check), orients, resizes and re-encodes every upload to two WebP sizes, `card` and `page`, with no metadata;
- **the admin's gallery API** on one space: list, upload one (multipart, `multer`), remove one, reorder; `can()` decides; the count of 10 is checked under the space's lock; the files are stored before the transaction and deleted when it refuses or fails;
- **the public photos** on DIRECTORY's answers: the cover's card URL on a list item and a pin, the photos on a space's page.

Two dependencies (`sharp`, `multer`), no migration, nothing in `apps/web`.

## 2. The contract

**Scope**
- `shared/storage/`: the port, the local adapter with its file handler, the Cloudinary adapter; `STORAGE_MODE` and `CLOUDINARY_URL` in the config, production refusing to start without Cloudinary.
- `shared/images/`: the domain-free image core (decode as the content check, the pixel limit, orientation, no metadata, WebP outputs the caller names).
- `spaces/photos/`: the two sizes, the repository, the service (list, upload, remove, reorder), the controller, the routes on the admin's router; a new `can()` action; an upload rate limit.
- `GET|POST /admin/spaces/:spaceId/photos`, `DELETE /admin/spaces/:spaceId/photos/:photoId`, `PUT /admin/spaces/:spaceId/photos/order`.
- `@masaha/shared/spaces`: `PHOTO_SIZES`, `PHOTO_LIMIT`, `PHOTO_MAX_BYTES`, `photoOrderSchema`, `SpacePhoto`, `PhotoUrls` (additions only).
- DIRECTORY's shapes extended: `DirectorySpace.cover`, `MapPin.cover`, `PublicSpace.photos`.
- The documents (prompt §7) and findings 63–64.
- Issue #69's five leftovers (§9, §11), closing #69.

**Acceptance criteria**
- [ ] An upload of a JPEG, a PNG or a WebP answers 201 with `{ id, urls: { card, page } }`; both stored files are WebP, `card` exactly 640×360, `page` at most 1600 on its longest side, never enlarged.
- [ ] A JPEG carrying EXIF GPS is stored with no EXIF, XMP or ICC, proven by reading the stored file back through its URL; an EXIF rotation is applied before the metadata is dropped.
- [ ] Anything sharp cannot decode as JPEG, PNG or WebP (text renamed `.jpg`, SVG, GIF, a truncated file) answers 415; a file over 4 MiB, or an image over 50 megapixels, answers 413; no file answers 422 `photo: ["required"]`; any other part answers 400. None stores anything.
- [ ] The 11th photo is refused, including when two uploads race with 9 photos (decided under the space's lock), and the refused upload's files are deleted before the answer.
- [ ] A verified space's photos are refused to the admin by `can()` (403), decided again under the lock; nothing stored stays.
- [ ] A failed store answers 503 with no row and no file left; a failed transaction deletes the stored files before answering.
- [ ] Remove deletes the row, closes up the order, then deletes both files before answering; a failed file delete is logged with `[storage:orphan]` and answered 204. Removing a photo the space does not have writes nothing (204).
- [ ] Reorder takes every id exactly once (else 409, no code); the first is the cover; the same order writes nothing.
- [ ] Each change is audited (`space.photoAdded`, `space.photoRemoved`, `space.photosReordered`) with the gallery's ids before and after, never a key or a URL; no change dates any fact group.
- [ ] Authorization per role on every endpoint: USER 403, an owner (of this or another space) 403 on the admin's router, the admin 2xx on an unverified space and 403 on a verified one for the three writes (GET stays readable).
- [ ] A public list item and pin carry `cover` (the first photo's card URL) or `null`; a space's page carries `photos` in order with both sizes; only publicly listed spaces (DIRECTORY's rule).
- [ ] Locally the URLs open in a browser through the web's `/api` proxy (`/api/v1/files/…`), with an immutable cache header; with `CLOUDINARY_URL` set, the URLs are Cloudinary's delivery URLs and open.
- [ ] `CLOUDINARY_URL` is never printed, logged or in a fixture; an invalid one is refused at startup without echoing it.
- [ ] Every lane, lint, typecheck, format, links, build and `check:build` green; the documents updated.

**Out of scope**
- Every screen: the editor's gallery, the browser's shrinking, the card's cover (worker A, later).
- `/manage/spaces/:spaceId/photos` (step 5): nothing built, nothing that stops it (the service takes the actor and the loaded space; `can()` decides).
- A reclamation job (finding 63), Cloudinary transformations, a stored original, a media registry or reference ledger.
- Demo photos in the seed.

## 3. Reading done

- **Always:** CLAUDE.md, workflow (whole), the docs map, the findings index; opened 17, 23, 33, 46, 52.
- **Capability:** `features/spaces.md` (whole).
- **Platform:** conventions §1–§13 (whole); security.md (whole); ADR 0014; data-model (whole); schema's `Space` and `SpacePhoto`; api-contract §1–§6 (whole); v1-mvp steps 3 and 5 and the planned surface; testing §1–§5; setup (whole).
- **Design:** DECISIONS_ADMIN A1, DECISIONS_OWNER O1, O7, DECISIONS_PUBLIC U12 (and its 2026-10-12 change: no prices on the card), U8, PU-023; DI-32 in `FIX_OWNER_PLAN.md:1138` (the cap of 10, WebP accepted). **The prototype's gallery:** `docs/design/prototype/masaha/profile-b.jsx:254-367` (`PhotosSection`, used by `Admin space edit.html:170` and `Owner space profile.html:56`); the card's cover `shared.jsx:410-460` (`.cover-ratio`: 2:1 on a phone, 16:9 from 768 px; the mark with no photo); the page's gallery `space-parts.jsx:8-56` (up to 5 tiles, 14/20 rem high, first tile 2×2; a lightbox at `max-w-3xl`, 18/24 rem; no gallery with no photo, a caption).
- **DIRECTORY's plan** (approved 2026-10-13): `DirectorySpace`, `MapPin`, `PublicSpace`, the 30 s cache, the page read under the share lock, `spaces/public/`.
- **Reference:** quick tweets' `docs/backend/media.md` and `modules/media/` (port shape, key rule, clean-up on failure, local adapter's root check).
- **Code:** `app.ts`, `server.ts`, `config/env.ts`, `shared/errors`, `shared/http/requestLogging.ts`, `shared/auth/can.ts` and `spaceLinks.ts`, `spaces/facts/groupEdit.ts` (the save path photos must not reuse: it dates a group), `space/space.repository.ts` (`lock`), `contacts/*`, `spaces.admin.routes.ts`, `test/app.ts`, `test/locks.ts`, `test/spaces.ts`, `vitest.config.ts`, `packages/shared/src/core/errors.ts`.
- **Registry:** `sharp@0.35.5` (2026-09-27; no install script, its platform binaries are optional `@img/*` packages without scripts), `multer@2.4.0` (2026-09-14), `@types/multer@2.3.0` (2026-09-28): each at least two weeks old today.

## 4. The settled decisions, as built

**D1 — Cloudinary, a plain store.**
- `STORAGE_MODE` = `local` (default) | `cloudinary`; `CLOUDINARY_URL` = `cloudinary://<api_key>:<api_secret>@<cloud_name>`, parsed by the config into `{ cloudName, apiKey, apiSecret }`, required with `cloudinary`. **Production refuses `local`** (as `EMAIL_MODE=log`). The refusal's message names the variable, never its value.
- **Folder per environment:** every object under `masaha/<NODE_ENV>/` (`masaha/production/…`, `masaha/development/…`), no extra variable.
- **Upload:** `POST https://api.cloudinary.com/v1_1/<cloud>/image/upload`, a `FormData` with `file` (the WebP as a `Blob`), `public_id` (`masaha/<env>/spaces/<key>/card`), `asset_folder` (the same folder, for dynamic-folder accounts), `overwrite=false`, `timestamp`, `api_key`, `signature` = SHA-1 of the sorted signed parameters + the secret. Timeout 8 s (`AbortSignal.timeout`).
- **Delete:** `POST …/image/destroy` with `public_id`, `invalidate=true`, signed; "not found" counts as deleted.
- **Resource type** from the content type: `image/*` → `image`; any other type refused with a clear `StorageError` today (one branch, unit tested), so video or raw files later change the adapter only. The `public_id` is the key without its extension.
- **URL:** `https://res.cloudinary.com/<cloud>/<resource type>/upload/<public_id>.<the key's own extension>`, the original as uploaded, no transformation. The real run compares the delivered bytes' SHA-256 with the uploaded file's.
- A non-2xx, a network failure or a timeout throws; the service turns it into `service_unavailable` (503).

**D2 — placement.**
- `apps/api/src/shared/storage/`: `storage.ts` (the port and the key rule), `localStorage.ts` (the adapter and its file handler), `cloudinaryStorage.ts` (the adapter and the signature), `index.ts`. Knows no domain: no "space", no "photo".
- `apps/api/src/modules/spaces/photos/`: sizes, the limit, the order, the cover, who may act.
- `apps/api/src/shared/images/`: `encodeImage` (D3), domain-free, so `users` (L1) could use it for an avatar without importing `spaces` (L1).
- No `media` module; the level map unchanged.
- **The extension points, once, in conventions §12's storage line:** a new kind of file is a new consumer of the port, with its own content check; a new provider is a new adapter behind the same port.
- **R5 corrected** in the port's commit: "A port that only one module needs lives in that module (auth's email and Google identity); a platform port that knows no domain lives in `shared/` (storage, the scheduler). Either is wired in the composition root."

**The port:**
```ts
interface Storage {
  /** Stores a new object; keys are never reused. Throws StorageError. */
  put(key: string, file: { bytes: Buffer; contentType: string }): Promise<void>;
  /** Deletes an object; one already absent is not an error. Throws StorageError. */
  remove(key: string): Promise<void>;
  /** Where a browser fetches it: absolute online, root-relative locally. */
  url(key: string): string;
  /** The local adapter's handler for its own files (development only, D13). */
  files?: RequestHandler;
}
```
Key rule: `/`-separated segments of `[A-Za-z0-9_-]`, the last with one `.ext`, ≤ 200 characters; anything else throws (no `..`, no absolute path); the local adapter also checks the resolved path stays under its root.

**D3 — libraries.** `sharp@^0.35.5` and `multer@^2.4.0` in `apps/api` dependencies, `@types/multer@^2.3.0` in its devDependencies. sharp: prebuilt libvips per platform through `@img/sharp-<platform>` optional packages (no install script, so no `allowScripts` row); `package-lock.json` must list `@img/sharp-win32-x64` and `@img/sharp-linux-x64` (checked after `npm install`). Both are API-only, so `check:build` (the web's dist) is unaffected.
- **multer:** memory storage, `single('photo')`, limits `{ fileSize: PHOTO_MAX_BYTES, files: 1, fields: 0, parts: 1 }`, wrapped in `shared/http/receiveFile.ts` as `receiveFile(field, maxBytes)` (the photos' routes pass `'photo'` and `PHOTO_MAX_BYTES`; nothing in `shared/http` reads a constant of `spaces`), which maps `LIMIT_FILE_SIZE` → 413 and every other multer or busboy error → 400. The client's MIME type and file name are never read.
- **sharp** (`shared/images/`, domain-free: `encodeImage(bytes, outputs)`, each output `{ name, width, height, fit: 'cover' | 'inside', quality }` from the caller; `spaces/photos/photoSizes.ts` defines `card` and `page`): `sharp(bytes, { limitInputPixels: 50_000_000 })`; `metadata().format` must be `jpeg`, `png` or `webp`, else 415; any decode error → 415; the pixel limit → 413; then `.autoOrient()` and two outputs from one input (`clone()`), `.webp()` with no `keepMetadata`/`withExif`, so EXIF, XMP and ICC are dropped (colour converted to sRGB). Animated WebP keeps its first frame. `sharp.cache(false)` at module load, so a warm function holds no image memory between requests.

**D4 — the table does not change.** `SpacePhoto.path` holds the key: 128 random bits, base64url (22 characters). Objects: `spaces/<key>/card.webp`, `spaces/<key>/page.webp` (the `spaces/` prefix is the photos service's, not the port's). The URL is built at read time by `storage.url()`. The cover is the first by `sortOrder, id`. No column needed; schema.prisma is not changed here: `profileUpdatedAt`'s doc comment (D8) is worker B's to write (`MEDIA_ADDITION.md`).

**D5 — the limit and the sizes.**
- **One image per request, at most 4 MiB (4,194,304 bytes)**: with one part's multipart overhead (≈ 300 bytes) it stays under Vercel's 4.5 MB in either reading of "MB". Larger → 413; online, a request over 4.5 MB is refused by Vercel itself with a 413 that carries no envelope (the contract says so).
- **`card`: 640×360 (16:9), cover crop, centred, WebP quality 75**, about 20–35 kB: the card's frame (16:9 from 768 px, 2:1 on a phone, `object-cover`), the page's gallery tiles (14/20 rem high) and the editor's tiles. Enlarged when the source is smaller, so it is always 640×360.
- **`page`: fit inside 1600×1600, never enlarged, WebP quality 80**, about 120–300 kB: the lightbox (`max-w-3xl`, 768 px × 2).
- **A portrait** 3000×4000 → `page` 1200×1600, `card` the middle 16:9 band. **A panorama** 8000×1000 → `page` 1600×200, `card` its centre. **Decompression bombs:** 50 MP (a 48 MP phone photo passes) → 413.

**D6 — the gallery API** (admin's router, under the links loader on `/spaces/:spaceId`):
```ts
PhotoUrls = { card: string, page: string }     // absolute online, root-relative locally; used as given
SpacePhoto = { id: number, urls: PhotoUrls }   // a list's order is its array's order; the first is the cover
```
- `GET /admin/spaces/:spaceId/photos` → 200 `SpacePhoto[]` in order; 404 for an unknown or soft-deleted space. Its own read, so `AdminSpace` does not change.
- `POST /admin/spaces/:spaceId/photos` (multipart, one part `photo`) → 201 `SpacePhoto`, placed last. Errors: 400, 403, 404, 409, 413, 415, 422, 429, 503.
- `DELETE /admin/spaces/:spaceId/photos/:photoId` → 204; a photo the space does not have → 204, nothing written (as an owner's unlink).
- `PUT /admin/spaces/:spaceId/photos/order` `{ ids }` → 204; not exactly the space's photos → 409, no code (as the lookups' order).
- Every write: 403 (no code) on a verified space; 404 on a soft-deleted one. A hidden space's photos can be changed.
- One service for both routers: `upload(actor, space, bytes)`, `remove(actor, space, photoId)`, `reorder(actor, space, ids)`, `list(spaceId)`.

**D7 — at most 10** (`PHOTO_LIMIT`), checked under the space's lock (`FOR NO KEY UPDATE`, through `space.repository.lock`). **The 11th: `conflict` (409) with no code** — the only 409 the upload answers, so it is unambiguous there, and no code means no catalogue line in `apps/web` (see decision 1 in §13).

**D8 — no freshness.** Photos leave the profile group: data-model's *Freshness* line drops "photos", `profileUpdatedAt`'s schema comment drops "and photos" (worker B's commit); the photos service never touches a date column. Reason: A1 and O7 ("no date, no confirm"); a new photo says nothing about whether the hours or the prices are still true.

**D9 — order of work.**
- **Upload:** (routes) the upload limit → `receiveFile` → (service) a cheap pre-check, no lock: `can()` on the loaded links and `count < 10` (S1) → pipeline → a new key → `put` both objects at once (if either fails, `remove` both, settled, then 503) → one transaction: lock the space, 404 if deleted, links under the lock, `can()`, count, insert at `sortOrder = count`, audit → 201. A refusal or failure of the transaction removes both objects before rethrowing.
- **Remove:** one transaction: lock, 404, `can()`, the photo of this space (none → nothing written), delete, close up the order (`sort_order - 1` above it, one statement), audit; then `remove` both objects; a failure is logged at `warn` with `[storage:orphan]` and the object keys (random, already public in URLs), and answered 204.
- **Reorder:** one transaction: lock, 404, `can()`, exact set check, same order → nothing; else one update per row (≤ 10), audit.
- No reclamation job: finding 63.

**D10 — the audit**, in the change's transaction, entity and space = the space:
- `space.photoAdded`: `before: { photoIds }`, `after: { photoIds }` (the new id last);
- `space.photoRemoved`: `before: { photoIds }`, `after: { photoIds }`;
- `space.photosReordered`: `before: { photoIds }`, `after: { photoIds }`.
The gallery is recorded whole, as ids in order, as every group is; never a key or a URL.

**D11 — privacy.** No metadata survives (D3), proven end to end (§9). Keys are random; the store receives only the WebP bytes and the key: no file name, no uploader.

**D12 — public.** `DirectorySpace.cover: string | null` and `MapPin.cover: string | null` (the first photo's card URL); `PublicSpace.photos: PhotoUrls[]` in order. `spaces` answers them set-based: `coverKeys(spaceIds)` (one `DISTINCT ON (space_id) … ORDER BY space_id, sort_order, id`) and the page's photos read inside DIRECTORY's share-locked page read. **Cache:** the answers keep DIRECTORY's 30 s; a file's URL never changes for its key and a key is never reused, so the local handler sends `Cache-Control: public, max-age=31536000, immutable`, and Cloudinary's CDN keeps its own long cache, purged on delete (`invalidate=true`). A removed photo leaves the answers within 30 s.

**D13 — development: the local adapter serves its own files.**
- Options weighed: (a) **the local adapter's handler, mounted by the composition root when the port has one, at `/api/v1/files/*`**; (b) Vite serving the API's folder (touches the web, couples the two); (c) an absolute URL to the API's port (breaks the one origin, ADR 0014); (d) Cloudinary in development too (needs the network: the demo runs offline, ADR 0014).
- **Recommended (a):** `express.static` over `apps/api/.storage/` (git-ignored), `index: false`, `dotfiles: 'deny'`, `fallthrough: false`, immutable cache, mounted before the general limit. URLs are root-relative (`/api/v1/files/spaces/<key>/card.webp`), so the web's proxy reaches them at its own origin, and the API lane reads them with Supertest. No module, rule or contract path differs: the URL is opaque to the client, and only the port's implementation differs, as conventions §12 allows. Production never mounts it (production refuses `local`).
- The API lane passes `createLocalStorage(<a temporary folder>)` through `createApi({ storage })`, the port as the seam (testing §3 rule 3), as `email` is passed today.

## 5. Stronger decisions (and proposed alternatives)

- **S1 — a pre-check before the image work**, decided again under the lock. *Why:* a verified space's upload or an 11th photo would otherwise cost a decode, two uploads to Cloudinary and two deletes before its refusal. *Cost:* one read without a lock. Recommended.
- **S2 — an upload limit: 30 uploads per 15 minutes, by the user** (`photo-upload`, counted on every upload, before the file is read), beside the general limit. *Why:* each upload costs a decode on the function and Cloudinary's free credits; 10 photos with retries fit easily. *Cost:* a row in security.md's table. Recommended.
- **S3 — a `can()` action of its own, `space.photos.manage`**, rule `adminWhileUnverifiedElseOwner`. *Why:* the table names what it decides; photos are no fact group any more (D8). *Cost:* a row and its unit case. Recommended.
- **S4 — removing an absent photo answers 204, writing nothing.** *Why:* a retried removal after a lost answer must not show a failure (O7's immediate actions); the owners' unlink set the precedent. *Cost:* a wrong id is not reported. Recommended.
- **S5 — an image over 50 MP answers 413, not 415.** *Why:* it is too large, not of the wrong type; the web's message differs. Recommended.
- **S6 — `autoOrient()` before the metadata is dropped.** *Why:* without it, every portrait taken on a phone is stored sideways once EXIF is gone. Recommended (part of D3 really).
- **S7 — the card is a centred 16:9 crop**, so the editor's tile shows exactly what the card shows. *Alternative:* sharp's `attention` crop (finds the salient part) — less predictable for the admin, more CPU. Recommended: centre.
- **S8 — `invalidate=true` on Cloudinary's delete.** *Why:* O7's dialog says the photo "disappears from the page at once"; without it the CDN keeps serving the URL. *Cost:* none on the upload API. Recommended.
- **S9 — the reorder answers 204** (the lookups' precedent) rather than the list. *Why:* the client sent the order it shows. Recommended.
- **S10 — the 413/415/503 lines of the contract say that online a body over 4.5 MB never reaches the API** (Vercel's own 413, no envelope). *Why:* the web must treat a 413 without an envelope as the same refusal. Recommended.
- **ADR 0014:** a dated *Revised* line, and its *Files* bullet: "photos go to Cloudinary's free plan through the storage port, as a plain store; resized on the client and sent through the API" (it says "or uploaded directly"). The decision is unchanged. Recommended.
- **Rules this item changes, none weakened:** security.md's "5 MB per photo" becomes 4 MiB (stricter); "or uploaded directly to storage" goes (a narrower path); R5's sentence is corrected (D2); data-model's freshness drops photos (D8).

## 6. Related findings

- **17 (counters never swept):** not folded; the upload limit adds one key per uploader, negligible. Needs the scheduler port.
- **23 (no per-address ceiling when signed in):** not folded; S2 bounds uploads per user, the per-address question is unchanged.
- **33, 46 (the deployment's headers):** not folded (no header config exists). **New 64** records Cloudinary's delivery host for `img-src`, beside them.
- **52 (race tests wait a fixed time):** not folded: it changes every race test's helper; the photos' race tests use `test/locks.ts` as it is and inherit it. Cost if folded: a helper and every race test.
- **New 63 — a photo's files can outlive it:** a crash between the store and the commit, a timeout after Cloudinary kept the file, or a failed delete leaves objects no row names (logged `[storage:orphan]` where the process survives). *Resolves when:* a timed job (the scheduler port) lists `masaha/<env>/spaces/` and deletes the objects no row names, older than an hour, or a measurement shows the loss does not matter against the free plan's storage.
- **New 64 — the deployment's headers must let Cloudinary's photos load:** `img-src https://res.cloudinary.com`, beside 33 and 46.

## 7. Files

**API (mine)**
- `apps/api/package.json`, `package-lock.json` (sharp, multer, @types/multer).
- `apps/api/src/config/env.ts` (+ `env.unit.test.ts`): `STORAGE_MODE`, `CLOUDINARY_URL`, the production refusal; `index.ts` exports `storageOf`-style settings if needed.
- `apps/api/src/shared/storage/` (new): `storage.ts`, `localStorage.ts`, `cloudinaryStorage.ts`, `index.ts`, `localStorage.unit.test.ts`, `cloudinaryStorage.unit.test.ts`, `storage.unit.test.ts` (key rule).
- `apps/api/src/shared/http/receiveFile.ts`, `index.ts`.
- `apps/api/src/shared/auth/can.ts`, `can.unit.test.ts` (S3).
- `apps/api/src/shared/images/` (new): `encodeImage.ts`, `index.ts`, `encodeImage.unit.test.ts`.
- `apps/api/src/modules/spaces/photos/` (new): `photoSizes.ts` (+ unit test), `photos.repository.ts`, `photos.service.ts`, `photos.controller.ts`, `photos.api.test.ts`, `photosRace.api.test.ts`; `apps/api/src/modules/spaces/spaces.limits.ts` (the upload policy).
- `apps/api/src/modules/spaces/spaces.admin.routes.ts`, `index.ts`.
- **After DIRECTORY's merge (its files, then `main`'s):** `spaces/public/*` (covers, the page's photos), `modules/directory/directory.service.ts` / mapper (the fields), their API tests.
- `apps/api/src/app.ts`: `storage` in `ApiOptions`, the files handler, the photos wiring, `createAppFromEnv`'s adapter choice.
- `apps/api/prisma/schema.prisma`: **untouched** (`MEDIA_ADDITION.md`): worker B writes D8's comment line in its migration's commit; none of B's files are touched (`shared/auth/accessToken.ts`, `requireAuth.ts`, `modules/sessions|users|auth/`, `apps/api/prisma/`).
- `apps/api/test/app.ts` (a default local storage in a temporary folder), `apps/api/test/storage.ts` (new: test images built with sharp, a storage that fails on a chosen call, the folder's file list).
- `apps/api/.env.example`; root `.gitignore` (`apps/api/.storage/`).

**Shared (mine, the contract)**
- `packages/shared/src/spaces/photos.ts` (+ `photos.unit.test.ts`), `spaces/index.ts`.
- `packages/shared/src/directory/responses.ts` (after the merge): `cover`, `photos`.

**Documents:** api-contract (§3's 413/415/503 lines, §5 *Spaces (the admin)* › photos, the directory's fields); `features/spaces.md` (API parts and the code map's API and Shared lines only); `features/directory.md` (public photos); conventions (header *Built*, §1 storage line, R5, §12 ports table); security.md (header, *HTTP hardening*, the upload limit row, the secret); data-model (D8, `SpacePhoto`'s key); setup.md (`STORAGE_MODE`, `CLOUDINARY_URL`, `.storage/`, sharp's binaries); ADR 0014 (*Revised*, *Files*); v1-mvp (photo rows); overview's *Built*; findings 63, 64 and the index.

**Shared with other open items:** nothing in `apps/web`; no type the web imports changes (`AdminSpace` untouched; the spaces entry only gains exports; if `@masaha/shared/directory` is imported by the web by the build, I check its fixtures and stop if one breaks). `spaces.md`, the contract, the overview's *Built* line and the findings index take the fast path. Nothing in `docs/design/`.

## 8. Design issues

No screen is built. For worker A's later item and the design fixers (recorded in the report, nothing touched in `docs/design/`): the prototype's gallery accepts JPEG and PNG only and says "up to 5 MB" (`profile-b.jsx:310, 346`); the API accepts WebP too and 4 MiB, after the browser's shrinking (DI-32).

## 9. Tests: lane, test and the break each catches

**Unit**
- `shared/storage/storage.unit.test.ts` — the key rule refuses `..`, an absolute path, a backslash, an empty segment, two extensions. *Break:* drop a clause.
- `localStorage.unit.test.ts` (a temporary folder) — `put` then the bytes on disk; `remove` twice; a key escaping the root throws; `url()` root-relative. *Break:* drop the root check.
- `cloudinaryStorage.unit.test.ts` (`fetch` stubbed with `vi.stubGlobal`, the platform's seam) — the signature against Cloudinary's documented example (a hand-written expected digest); the upload's URL and signed fields (`public_id` under `masaha/<env>/`, no secret in the body); a non-2xx and a timeout throw; destroy with `invalidate`; "not found" on destroy resolves; the delivery URL. *Breaks:* unsorted parameters, the secret sent, a 4xx swallowed.
- `config/env.unit.test.ts` — production refuses `local`; `cloudinary` without the URL refused; a malformed URL refused and the error text holds none of it. *Break:* drop the refinement.
- `shared/images/encodeImage.unit.test.ts` (images made with sharp in the test) — JPEG, PNG, WebP each give the WebP outputs asked; a `cover` output exact, an `inside` one never enlarged; EXIF orientation 6 turns the output; text, SVG, GIF and a truncated JPEG → 415; a 56 MP PNG → 413. *Breaks:* drop `autoOrient`, the format list, `limitInputPixels`, `withoutEnlargement`.
- `spaces/photos/photoSizes.unit.test.ts` — the photos' sizes through the core: `card` exactly 640×360 (also from a 300×200 source); `page` ≤ 1600; a portrait and a panorama as D5 says. *Break:* a size changed.
- `cloudinaryStorage.unit.test.ts` also: a non-`image/*` content type refused before any request; the URL takes the key's extension.
- `shared/auth/can.unit.test.ts` — `space.photos.manage`: admin on unverified, owner on verified, not admin on verified, not reception.
- `packages/shared/src/spaces/photos.unit.test.ts` — `photoOrderSchema`: ids required, positive integers, at most 10.

**API (`photos.api.test.ts`, local adapter in a temporary folder)**
- **Privacy (D11):** upload a JPEG whose EXIF carries GPS (asserted present in the input first, so the test cannot pass empty), fetch both URLs through the app: `image/webp`, immutable cache, sizes right, `metadata().exif` undefined and no `GPS`/`Exif` bytes. *Made break:* `keepExif()`.
- PNG and WebP accepted; the answer's exact shape.
- Text renamed `photo.jpg` with `image/jpeg` → 415; 4 MiB + 1 byte → 413; no file → 422 `photo: ["required"]`; two files or an extra field → 400. Each: no row, the folder empty.
- The 10th accepted, the 11th → 409, nothing stored (pre-check). 
- A failing `put` on the page size → 503, no row, the card's object removed.
- List in order; 404 for unknown and soft-deleted spaces.
- Reorder: 204, the list and the cover follow; same order writes no audit; missing, extra, repeated or another space's id → 409.
- Remove: 204, the order closed up (`sortOrder` 0…n-1), both files gone, audit exact; an absent id → 204, nothing written; a failing `remove` → 204, the row gone, a `[storage:orphan]` line in a captured log.
- **Audit:** exact entries for the three, with ids only. **Dates:** `profileUpdatedAt` and every group date unchanged after each change. *Break:* call `editGroup`.
- **Authorization:** USER 403; an owner of this space and of another 403 (the admin's router); the admin on a verified space 403 for upload (nothing stored), remove and reorder, 200 for list.
- **Upload limit:** 30 requests with no file (422 each) then the 31st → 429. *Break:* the limiter after `receiveFile`.
- The files handler: `/api/v1/files/../x` and an unknown key → 404.

**API (`photosRace.api.test.ts`, `whileHeld`)**
- 9 photos; the space's row held; an upload starts (passes the pre-check, stores, waits); meanwhile a 10th row is inserted; commit → 409 and the upload's files removed. *Made break:* count before the lock.
- An unverified space held; an upload waits; meanwhile an owner is linked; commit → 403 and the files removed. *Made break:* decide on the loader's links.

**API (DIRECTORY's tests, extended)**
- List item and pin: `cover` is the first photo's card URL after a reorder, `null` with none. Page: `photos` in order with both URLs, `[]` with none. *Breaks:* the second photo as cover; `page` in `cover`.

**Issue #69 (DIRECTORY's leftovers)**
1. `directory/list.api.test.ts` (default order) and `near.api.test.ts` (distance order): before asserting, the earliest row is updated so its physical position leaves id order. *Made break:* `, id` removed from `orderOf`; both fail.
2. `near.api.test.ts`: a request with `Masaha-Near` refused for another field (422) carries `Cache-Control: no-store`. *Break:* the header set after validation.
3. `page()` reads verified and the facts under one transaction and the share lock; `page.api.test.ts` proves it with the space's row held and an owner unlinked meanwhile. *Made break:* the links read before the transaction. If a reason appears to keep the gap, it is recorded instead and said in the report.
4. The `q` of spaces only: the code and the contract say the same code; the shared unit test pins it.
5. security.md › *Location*: the screen labels the distance approximate, not the answer (documents only).

Every new test is seen failing first; the made breaks are made once and restored.

## 10. Review Focus (inputs no planned test exercises)

- A CMYK JPEG, a 16-bit PNG, a PNG with transparency (kept in WebP), an ICC profile other than sRGB.
- An animated WebP (first frame), an APNG.
- Exactly 4 MiB; a client that disconnects mid-upload (multer aborts; nothing stored).
- Cloudinary's dynamic-folder vs fixed-folder accounts (`asset_folder`), its rate limits, a delivery before the CDN has the object.
- A remove and a reorder at once (the lock orders them; the reorder then answers 409).
- A remove racing an upload's transaction; two removes of the same photo.
- The function's 10 s limit on Vercel with a slow Cloudinary (8 s timeout, then an orphan: finding 63).
- 1,000 pins each with a cover (≈ +22 kB gzip).

## 11. Commits

0. `fix(directory): close #69's review leftovers` (45) — first, alone: the five of Issue #69, its body naming each; the PR says `Closes #69`, with an *Issue #69* section listing the five and where each is proven.
1. `feat(api): a storage port, local and Cloudinary` (47) — `shared/storage`, the config, `createApi({ storage })` and the files handler, `.env.example`, `.gitignore`, tests; conventions §1, R5, §12; setup.md; security.md's secret line.
2. `feat(spaces): upload and list a space's photos` (46) — sharp and multer, `receiveFile`, `shared/images` (the core comes with its first consumer), the photos' sizes, the service's list and upload, `can()`'s action, the upload limit, the routes, the shared photos, the tests; the contract, security.md's hardening and limit row, data-model (D8, the key), spaces.md; finding 63.
3. `feat(spaces): remove and reorder a space's photos` — the service, routes, tests; the contract; spaces.md.
4. `feat(directory): a space's photos in public` — `cover` and `photos`, `spaces`' set-based reads, the tests; the contract, directory.md, ADR 0014's *Revised*, v1-mvp, the overview's *Built*; finding 64.

PR: `feat(spaces): a space's photos`; labels `feat`, `area:api`, `area:docs`; assigned to the owner. Not merged.

## 12. Verification (phase 4)

**Before building:** the reply says DIRECTORY merged → `git fetch --prune origin`, `git switch --no-track -c feat/space-photos origin/main`; check its migration is applied to `masaha_media_dev`/`_test` (`prisma migrate status`) and the shared `dist` is fresh; after `npm install`, the lockfile holds `@img/sharp-win32-x64` and `@img/sharp-linux-x64`, and `node -e "require('sharp')"` works on Windows.

**Once each on the head, one at a time** (first checking no `vitest` runs in the main folder or `masaha-b`): `test:unit`, `test:api`, `lint`, `typecheck`, `format:check`, `check:links`, `build` (with `NODE_ENV=production`) and `check:build`. **`test:component` not run** unless a type the web imports changes (it does not: additions only); said in the report. CI proves sharp on Ubuntu.

**Real requests against 3322** (local adapter; then Cloudinary if the owner has added `CLOUDINARY_URL`, else said as not run): the JPEG with GPS (stored file read back: no EXIF, sizes right), a PNG, a WebP; a text file as `.jpg` (415); 4 MiB + 1 (413); the 11th (409); reorder (the cover changes) and a stale order (409); remove (its files gone from `.storage/` or Cloudinary's 404); a verified space's upload (403); the public list's `cover` and the page's `photos`; the URLs opened in a browser through the web on 5322 (and Cloudinary's, with the bytes' hash compared). Servers stopped by PID, ports 3322 and 5322 checked free.

**What proves Vercel:** nothing here; the first online deployment with `STORAGE_MODE=cloudinary` (sharp's `linux-x64` binary in the function, the 4.5 MB platform limit). The report says so.

**At the report:** `git merge-tree --write-tree` against every open PR; `gh pr checks` green and `CLEAN`; background shells stopped.

## 13. Decisions needed from the owner (answered 2026-10-13: 1 → 409 with no code; 2–6 as recommended; no avatar)

1. **The 11th photo:** `conflict` (409) with no code (recommended: unambiguous on the upload, no line in `apps/web`), or a new `PHOTO_LIMIT_REACHED` (clearer, but `add-error-code` adds its text to both web catalogues, a licence in `apps/web` this prompt does not give).
2. **The sizes:** `card` 640×360 q75 (cover crop, centred) and `page` ≤ 1600 q80, the 4 MiB request limit and 50 MP (D5).
3. **D13:** the local adapter serves its files at `/api/v1/files/*` (recommended (a)).
4. **S2:** the upload limit, 30 per 15 minutes per user.
5. **ADR 0014's *Revised* line** (§5).
6. **D12's pins carry `cover`** (≈ 22 kB more gzip at 1,000 pins), as the prompt asks; the alternative is a pin without it and the selected card drawing the mark.
