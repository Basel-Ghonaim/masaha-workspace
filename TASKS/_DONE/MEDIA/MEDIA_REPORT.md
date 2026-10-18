# MEDIA — a space's photos — report

## 1. Pull request and head

- **PR #77**, `feat(spaces): a space's photos`, branch `feat/space-photos`, labels `feat`, `area:api`, `area:docs`, assigned to the owner. `Closes #69`.
- **Head:** `9bc0b705b327a40c6527165b73dad0683e732552`. CI green on that head (all ten checks), GitHub `CLEAN`.
- Not merged.

## 2. Commits

1. `31140e00` `fix(directory): close #69's review leftovers` (44) — first, alone: the five items of Issue #69.
2. `a41bffb5` `feat(api): a storage port, local and Cloudinary` (47) — `shared/storage`, the config (`STORAGE_MODE`, `CLOUDINARY_URL`), `createApi({ storage })` and the local files' handler; conventions §1, R5, §12; setup; security's secret line.
3. `9d6d9017` `feat(spaces): upload and list a space's photos` (46) — sharp and multer, `shared/images` (the core comes with its first consumer, as the reply allowed), `receiveFile`, the photos' sizes, list and upload, `space.photos.manage`, the upload limit; the contract, security's hardening and limit row, the data model (D8, the key), spaces.md; finding 63.
4. `b41eb1cf` `feat(spaces): remove and reorder a space's photos` (49).
5. `9bc0b705` `feat(directory): a space's photos in public` (43) — `cover` on the card and the pin, `photos` on the page; the contract, directory.md, ADR 0014's *Revised* line, v1-mvp, the overview's *Built*; finding 64.

`#PRNUM` placeholders were replaced by `#77` in every commit's tree (`git filter-branch --tree-filter`) just before the push; the PR got #77 (#76 was taken by another PR minutes before, so the first count, #76, was redone).

## 3. What was run

**Locally, on the head, one at a time** (each lane after checking that no other folder ran one):
- `test:unit`: shared 208, api 721, web 734 — all passed.
- `test:api`: 47 files, 776 passed.
- `lint`, `typecheck`, `format:check`, `check:links` (2,007 links), `check:classes`: clean.
- `NODE_ENV=production npm run build` and `check:build`: pass.

The head changed after the first full run only by three comments and one test title (fixups, below); lint, typecheck, format, `test:unit` and `test:api` were run again on the final head.

**CI** on the pushed head: build, check:classes, check:links, format:check, lint, test:api, test:component, test:unit, typecheck — all pass. It proves sharp's `linux-x64` binary on Ubuntu.

**Real requests against 3322** (the built API, `npm run start`; the web on 5322), with the local adapter, then with Cloudinary (`STORAGE_MODE=cloudinary` over the same `.env`, folder `masaha/development`). Both runs, every line as expected:

| Case | Local | Cloudinary |
|---|---|---|
| JPEG 3000×4000 with GPS EXIF (320 bytes of EXIF) | 201; `card` 640×360, `page` 1200×1600, no EXIF/XMP/ICC, "TestCam" absent | the same |
| Delivered bytes vs the same input encoded with the same settings | — | SHA-256 **equal** for both sizes: no transformation |
| Cache header of a file | `public, max-age=31536000, immutable` | `public, no-transform, max-age=2592000` |
| PNG, WebP | 201, 201 | 201, 201 |
| Text file named `evil.jpg` | 415 | 415 |
| 4 MiB + 1 byte | 413 | 413 |
| The 11th photo | 409, no code | 409, no code |
| Reorder reversed / stale order | 204, cover changed / 409 | the same |
| Remove one | 204; its URL 404; its folder under `.storage` gone | 204; its Cloudinary URL 404 at once |
| Upload to the verified demo space (`masaha-demo`) | 403 | 403 |
| Public list's `cover`, pin's `cover`, page's `photos` (first = cover) | right | right |
| The cover through the web on 5322 (its `/api` proxy) | 200 `image/webp` | — |

The URLs opened in **headless Chrome** (CDP script): local card 640×360 and page through `http://localhost:5322`, Cloudinary card 640×360 and page 1200×1600. Screenshots: `Downloads\media-shots\` (not committed). Both API logs were checked: neither holds `CLOUDINARY_URL` nor its secret; no `[storage:orphan]` line. Servers stopped by PID; ports 3322 and 5322 checked free.

**Not run:**
- `test:component` locally: no type the web imports changes (`@masaha/shared/spaces` only gains exports, `@masaha/shared/directory` is not imported by the web, and the web's typecheck passes). CI ran it: pass.
- Vercel: nothing here proves the function's sharp binary or the platform's own 4.5 MB limit; the first online deployment with `STORAGE_MODE=cloudinary` does. Our 413 test proves our limit only.
- E2E: not part of this item.

## 4. Breaks made, and tests seen failing first

**Seen failing first** (before their code): the three Issue #69 tests (`no-store` on a 422, the page's verified under the lock, the spaces-only `q`), the storage unit tests (missing modules), the env tests (3 failing), the `can()` table (14), the shared order schema, the files handler's 404 (it answered 500, which led to a fix, §5), and the public `cover`/`photos` tests (5 failing).

**Made once and restored** (each test failed):
- `, id` removed from `orderOf` (`updated` and `distance`): the list's and the near's tie-break tests.
- The signature's `.sort()` removed.
- `encodeImage`: no `autoOrient()`; no format check; no `limitInputPixels`; no `withoutEnlargement`; `keepMetadata()` — each caught.
- Upload: `keepMetadata()` (the API privacy test); no discard after a failed store; no upload limiter.
- Race: the count checked only before the lock, and `can()` on the loader's links — both race tests failed.
- Remove: no discard; no close-up of the order. Reorder: repeated ids allowed.
- Public: the cover chosen by id rather than the gallery's order.

## 5. Problems met

- **The files handler answered 500 for a missing file.** `express.static`'s `send` passes the `fs` error (`status: 404`, `expose: false`), which the error handler treats as unknown. Fixed in the adapter: any 4xx of the static handler becomes `not_found`.
- **A heredoc'd Python edit failed to parse** in Git Bash (a quote inside the text): the long edits went into scratchpad `.py` files instead (as memory says).
- **A test name clash** (`first` declared twice in `list.api.test.ts`) made one break run look like a pass; the file failed to transform. Renamed and the break re-run: it fails as it should.
- **The PR number moved** from #76 to #77 between the count and the push (another PR was opened); the placeholders were rewritten again.
- **The Chrome extension** showed an error page for `localhost`; the headless Chrome CDP fallback (memory) opened the URLs.

## 6. Anything unexpected

- **sharp's `metadata()` already enforces `limitInputPixels`**: the 50 MP refusal happens before any decode, as wanted.
- **A spaces-only `q` answered two codes** (`too_short` and `invalid_format`): Zod's refinement runs after a failed `min`. Issue #69's item 4 is resolved by making it `too_short` alone (the refinement passes an empty string) and saying so in the contract, rather than changing the contract to two codes.
- **Cloudinary serves with `no-transform` and 30 days**, not a year; fine for keys that never change.
- **Cloudinary removed the file from delivery at once** (404 right after the destroy with `invalidate=true`).
- **Worker A started a full `test:component` run** while my second `test:api` ran (it was idle when I checked); both finished green, the API lane took ~2.5 minutes longer.
- Dev data: two test spaces (`media-local-…`, `media-cloudinary-…`) remain in `masaha_media_dev`, with their photos under `apps/api/.storage/` (git-ignored) and 9 photos (18 files) under Cloudinary's `masaha/development/` folder. Left as development data; say if they should be removed.

## 7. Early conflict check (`git merge-tree --write-tree`, this head against each open PR)

- **#74 `feat/admin-space-editor`:** conflicts in documents only — `docs/architecture/findings/README.md`, `docs/features/spaces.md`, `docs/project/overview.md` (both sides append to the open findings, spaces.md's sections and the *Built* line). The fast path: keep both sides, `format:check`, one push.
- **#75 `design/account`:** clean.
- **#76 `design/owner`:** clean.

## 8. Departures from the prompt

- **`schema.prisma` untouched** (MEDIA_ADDITION.md): D8's comment line is worker B's; the plan said this item would edit it. None of B's files touched.
- **The plan file** was saved with the reply's three changes, `MEDIA_BUILD.md`'s Issue #69 commit and the addition's schema line; the plan was saved only at the build message (the exit from plan mode was replaced by the build message), before the branch was cut.
- **ADR 0014** got its dated *Revised* line and *Files* bullet, as approved.
- **`spaces.md` decisions:** the API decisions for photos are dated `#77`; directory.md's earlier "the card carries no photo" line is kept and marked *Revised* by the new one, rather than edited.
- No other departure.

---

# Review fixes — round 1 (`MEDIA_FIXES.md`)

## 1. Pull request and head

- PR #77, new head **`7d6e0f75fb8cc79bfe4bc7d334ee85f95dfc765b`**: CI green on it (all ten checks), `CLEAN`. One "Review fixes" comment posted; the description updated to the final state. Not merged.

## 2. Commits (after the rebase and the fold)

1. `6ea0faeb` `fix(directory): close #69's review leftovers`
2. `628baf2c` `feat(api): a storage port, local and Cloudinary` — fixes 1–3 folded in.
3. `80a8d7b0` `feat(spaces): upload and list a space's photos`
4. `bec418ee` `feat(spaces): remove and reorder a space's photos`
5. `7d6e0f75` `feat(directory): a space's photos in public`

**Rebase** on `origin/main` (#74, #75 merged): conflicts in documents only, both sides kept — `docs/features/spaces.md` (authority line, *What it does* with its closing sentence, code map, open findings; again in commits 3 and 4 on the photos bullet), the findings index (59, 60 beside 63), the overview's *Built* line (the editor beside the photos). No code conflicted; `npm install` changed nothing.

**The fixes** (each verified in the code first):
1. **`overwrite: 'false'`** (Copilot 1, true: my plan's D1 had it and the build dropped it) — signed in `put`.
2. **`asset_folder`** (Copilot 2, true, D1 again) — the key's folder under `masaha/<env>/`, signed.
3. **The local adapter's `contentType`** (Copilot 3) — **pushed back**: a key's extension names its type (conventions' storage line), the local handler serves by it as Cloudinary's URL does; a second home for the type could disagree with the first. The port's `StoredFile` comment now says the content type must agree with the key's extension.

## 3. What was run

On the head, one at a time (no lane running in `masaha-b` or the main folder at each check): `test:unit` 208 + 721 + 768; `test:api` 47 files, 776; `lint`, `typecheck`, `format:check`, `check:links` (2,027 links); the production build and `check:build`. CI: all pass.

**Real run against Cloudinary** (`STORAGE_MODE=cloudinary`; `CLOUDINARY_URL` checked by its shape only, never printed; the API log holds neither it nor its secret):
- **Through the adapter**, its answer read: `public_id` `masaha/development/spaces/review…/card`, **`asset_folder` `masaha/development/spaces/review…`** (the folder sent), and a `display_name` (`card`) — **the account uses dynamic folders**. The Admin API (`resources/by_asset_folder`) lists the file in that folder.
- **`overwrite=false`:** a second upload to the same key (a PNG) was answered `existing: true`; the delivered file was still the first, byte for byte.
- **Through the API:** one upload (201), its two files listed in `masaha/development/spaces/<key>`, then removed.

**Clean-up:** the first run's 9 photos (18 files) and this round's files were removed — the photos through the API (`DELETE`, 10 photos), the adapter's test file through the adapter. The Admin API lists **no file under `masaha/development/`**. The two test spaces stay in `masaha_media_dev`.

**Not run:** `test:component` locally (no type the web imports changed; CI ran it). Vercel, as before.

## 4. Breaks and tests seen failing first

- The adapter's upload test, with `overwrite` and `asset_folder` expected in the signed fields and the signature, was seen failing before the code.
- Fix 3 changes a comment only.

## 5. Problems met

- My real-run script searched the spaces by slug (`q=media-cloudinary`); `q` matches names, so it found nothing. Searched by `q=cloudinary` and re-ran the API part only.
- Heredoc-free edits as before (scratchpad `.py` files) for the conflict resolution.

## 6. Anything unexpected

- **The CDN kept a removed file briefly.** A file fetched just before its removal still answered 200 right after `destroy` with `invalidate=true`, then 404 a little later; a file never fetched (the first run) answered 404 at once. O7's "disappears at once" holds for the page (which stops naming it within 30 s), and within a short time for the URL itself.
- `npm install` after the rebase changed nothing (#74 and #75 added no dependency).

## 7. Early conflict check (this head against each open PR)

- **#78 `feat/session-ends`** (worker B): conflicts in **documents only** — `docs/backend/conventions.md` (the header's *Built* line, and §12, where B adds a *Timer* row to the ports table where I added the storage port's line) and `docs/architecture/findings/README.md` (63–64 beside 65–66). `app.ts`, `test/spaces.ts`, the contract and the data model merge clean. The fast path, keeping both sides.
- **#76 `design/owner`:** conflicts in `docs/design/CHANGES.md` and `INDEX.md` — with `main` itself (after #75), not with this PR, which touches nothing in `docs/design/`.

## 8. Departures

- None from `MEDIA_FIXES.md`. The removals of the test files used the API for the photos (keeping the rows and files in step) and the adapter for its own test file, as allowed.
