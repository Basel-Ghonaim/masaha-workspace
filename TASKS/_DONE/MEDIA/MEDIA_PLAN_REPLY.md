# MEDIA — reply to your plan

A strong plan: the port kept to bytes by key, decoding as the content check, `autoOrient()` before the
metadata goes, the pre-check that spares a refused upload its work, the privacy test that first proves
its input carries GPS, the two race tests, and the honest line on what only Vercel can prove.
**Approved**, with the owner's answers and three changes below. **Save it now** (as approved here,
with these changes folded in) to `C:\Users\basel\.prompt\MASAHA_MEDIA\PLAN\MEDIA_PLAN.md`, **then
stop. Do not cut the branch yet:** DIRECTORY (#73) is under independent review. A second message will
say it has merged, with anything its review changed in the shapes you extend (D12); build only then.

## The owner's principle, and three changes it asks for

The owner (2026-10-13): **build for the abstraction, don't build the abstraction.** Adding a user's
avatar, a video, another kind of file, or replacing Cloudinary must each be a small addition — a new
consumer or a new adapter — never a rebuild of the capability. This is engineering principles §1
("put the boundary in now; build the generalisation at the second instance") and §2 (Liskov for a
port). Nothing below builds avatars, video or other files; each change only puts a boundary where it
belongs, with parameters the one existing caller passes.

1. **The image pipeline's domain-free core moves to `apps/api/src/shared/images/`.** Decoding (the
   content check: JPEG, PNG or WebP, else 415), the pixel limit (413), `autoOrient()`, dropping the
   metadata and encoding WebP outputs — taking the outputs to make (name, size, fit, quality) from its
   caller. **`spaces/photos/` keeps** the two sizes, `PHOTO_LIMIT`, the order, the cover and who may
   act, and passes its sizes in. *Why:* `users` (L1) may not import `spaces` (L1), so an avatar would
   otherwise force a move or a copy. `sharp.cache(false)` and `limitInputPixels` live with the core.
   Its unit tests move with it; the photos' sizes are tested where they are defined.
2. **The port's content type is any MIME type, not the literal `'image/webp'`:**
   `put(key, { bytes, contentType: string })`. The Cloudinary adapter derives the resource type from
   it (`image/*` → `image`) and **refuses any other type with a clear error today** (one branch, unit
   tested), so supporting video or raw files later changes the adapter only. The delivery URL is built
   from the key's own extension, never a hard-coded `.webp`. The local adapter stores any type and
   serves it with its type.
3. **`receiveFile` takes its field name and its byte limit from its caller** (the photos' routes pass
   `'photo'` and `PHOTO_MAX_BYTES`); nothing in `shared/http` reads a constant of `spaces`.

Write the extension points once, in conventions (the storage line of §1 or §12, one or two sentences,
no list of future cases): a new kind of file is a new consumer of the port, with its own content
check; a new provider is a new adapter behind the same port. Update §7 *Files* and the commits'
contents (the core in commit 2 with its first consumer, or commit 1 if you judge it cleaner — say
which); every subject stays ≤ 50 (count them).

## The owner's decisions (§13)

1. **The 11th photo: `conflict` (409) with no code.** The gallery disables "add" at 10, so only a race
   meets it.
2. **The sizes and limits as planned:** `card` 640×360 q75 centred cover crop, `page` ≤ 1600 q80 never
   enlarged, 4 MiB per request, 50 MP.
3. **D13 (a):** the local adapter serves its files at `/api/v1/files/*`; never mounted in production.
4. **S2:** the upload limit, 30 per 15 minutes per user.
5. **ADR 0014's dated *Revised* line** and its *Files* bullet, as §5 says.
6. **The pins carry `cover`.**
7. **No avatar** (the owner): out of scope; the changes above keep it a small later addition.

Every *Stronger decision* (S1–S10) is approved as recommended.

## Reminders

- Before building: `prisma migrate status` on `masaha_media_dev` / `_test` after DIRECTORY's migration
  is applied (the analyst applies it), the shared `dist` fresh, the lockfile holding
  `@img/sharp-win32-x64` and `@img/sharp-linux-x64`, `require('sharp')` working; check that
  `autoOrient()` exists in the version you install (else `rotate()` with no arguments).
- `CLOUDINARY_URL` is a secret: never print, log or echo it; check it by its shape only.
- **One full test run at a time on this machine:** before `test:api` or `test:component`, check that
  worker A (main folder) and worker B (`masaha-b`) run none.
- An independent review follows (two dependencies, uploads, security). Don't merge. At the report,
  `git merge-tree --write-tree` against every open PR. Stop every background shell you start; `jq` is
  not installed — use `gh … --jq`.
