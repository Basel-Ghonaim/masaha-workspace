# Review — PR #77 (MEDIA: a space's photos — the storage port, Cloudinary, the image core, the admin's gallery API, the public photos; Issue #69's leftovers)

You are an **independent reviewer** of PR #77 in the Masaha repository (Basel-Ghonaim/masaha). If two
reviewers run, they work apart; do not read the other's report.
Write your report to `C:\Users\basel\.prompt\MASAHA_MEDIA\REPORT\REVIEW77_<YOU>_REPORT.md`, where
`<YOU>` is your tool's name in capitals (`OPENCODE`, `COPILOT`).

## Rules

- **Run from `C:\Users\basel\masaha-media`** and **read only commit objects.** No edits, commits,
  checkouts, switches, installs, npm or test runs, servers, database, Docker or network calls to
  Cloudinary, no GitHub comments. **Do not run the tests:** CI ran every lane on this head and passed;
  your job is to read. `git fetch origin`, then pin to **the PR's current head**
  (`gh pr view 77 --json headRefOid` — expected `9bc0b70`; write it at the top of your report and check
  it again at the end). Base: `git merge-base origin/main <head>`. Use
  `git diff <base>...<head> -- <paths>` and `git show <head>:<file>`.
- **Never open or print** `apps/api/.env` or anything holding `CLOUDINARY_URL`'s value.
- **Report concrete problems only,** each verified in the code: file and line, the failing scenario,
  the severity (**blocker / should-fix / nit**) and the fix. No praise, no summary. If unsure, say
  "plausible" and why. A web search is allowed for a fact about sharp, multer, Cloudinary's API or
  Vercel's limits; cite it.
- **No tool attribution** in what you write.

## What the PR must be (the owner's decisions)

API, `packages/shared` (additions only) and documents; **two dependencies** (`sharp`, `multer`, with
`@types/multer`); **no migration, `schema.prisma` untouched**; nothing in `apps/web`. The prompt is
`C:\Users\basel\.prompt\MASAHA_MEDIA\PROMPT\MEDIA_PROMPT.md`; the approved plan `PLAN\MEDIA_PLAN.md`
with its reply `PROMPT\MEDIA_PLAN_REPLY.md` (**the owner's principle — build for the abstraction,
don't build it — and its three changes**), `PROMPT\MEDIA_BUILD.md` (Issue #69 added) and
`PROMPT\MEDIA_ADDITION.md`; the worker's report `REPORT\MEDIA_REPORT.md` (read its departures).
- **The storage port** (`apps/api/src/shared/storage/`): bytes by key, any content type; a local
  adapter (development and tests, serving its own files at `/api/v1/files/…`, never mounted in
  production) and a **Cloudinary adapter as a plain store** (signed `fetch`, no SDK, no
  transformation, images only today with any other type refused, a folder per environment, the URL
  built from the key at read time, never stored). Production refuses the local adapter.
- **The image core** (`apps/api/src/shared/images/`), domain-free: decoding is the content check
  (JPEG, PNG, WebP; else 415), over 50 MP refused (413) before decoding, EXIF orientation applied,
  WebP written with **no metadata**; the sizes come from the caller (`card` 640×360, `page` ≤ 1600).
- **`receiveFile`** takes its field and byte limit from its caller (4 MiB for photos).
- **The admin's gallery** (`/admin/spaces/:spaceId/photos…`): list, upload one, remove one, reorder
  (exact or 409); at most 10 (the 11th 409, no code); `can()` and the count decided again **under the
  space's lock**; the files stored before the transaction and removed whenever it refuses or fails;
  removal's files deleted before the answer, a failure logged `[storage:orphan]`; 30 uploads per 15
  minutes per user; audited with ids only; **no fact group dated** (photos left freshness).
- **Public:** `cover` on a directory card and a pin, `photos` on a space's page, publicly listed
  spaces only.
- **Issue #69** (#73's five review leftovers), its own commit, `Closes #69`.

## Look at these, in this order

1. **Security and privacy of an upload.** Can anything but a re-encoded image reach the store (a
   polyglot file, SVG, an animated or a huge image, a decompression bomb, a truncated file)? Is any
   metadata (EXIF GPS, XMP, ICC) left? Are the client's file name and MIME type truly ignored? Is the
   key random and unguessable, and can a key escape the local root (`..`, absolute paths, backslashes
   on Windows)? Is `CLOUDINARY_URL` or its secret ever logged, echoed in an error, or sent in a
   request body? Is the signature computed as Cloudinary documents it? Is the local files handler
   safe (no directory listing, no dotfiles, no path traversal) and truly absent in production?
2. **The transaction and the store.** Upload: pre-check, encode, store, then the locked transaction;
   every refusal and failure path removes both stored files before answering; nothing runs after the
   response (ADR 0014). Remove: row and order closed up in the transaction, files after, failure
   logged. Reorder: exact set under the lock. The two race tests really race (the lock held, the
   other write made meanwhile) and would fail if the decision moved outside the lock.
3. **The owner's principle.** Adding an avatar (a `users` consumer), video or another file type, or
   replacing Cloudinary: what would each need to change? Anything in `shared/` that knows a space or
   a photo? Anything in `spaces/photos/` that should be the core's? Is the extension sentence in
   conventions true to the code?
4. **Limits and memory.** multer's memory storage with its limits; sharp's `limitInputPixels`, cache
   off; the 4 MiB limit against Vercel's 4.5 MB (the contract's line on a 413 without an envelope);
   the 8 s Cloudinary timeout against the function's time limit.
5. **Issue #69.** Each of the five truly fixed: the tie-break tests fail without `, id` (the break);
   `no-store` on a refused request carrying `Masaha-Near`; "verified" and the facts read under one lock
   (no deadlock with other lock orders); the `q` code and the contract agree; security.md's sentence.
6. **The public side.** `cover` and `photos` set-based (no N+1), only for publicly listed spaces, the
   cache rules unchanged; `packages/shared` changes additive only, so nothing in `apps/web` breaks.
7. **The tests.** Each would fail if its code broke; the privacy test proves its input carried GPS
   first; expectations by hand; the Cloudinary adapter tested through the platform's `fetch`, never a
   mocked module.
8. **The documents.** The contract, `spaces.md`, `directory.md`, conventions (§1, R5, §12, the
   extension sentence), security.md (the real limit, re-encoding, no metadata, the secret, the
   upload limit), the data model (photos out of freshness; the key), setup.md, ADR 0014's *Revised*
   line, v1-mvp, findings 63 and 64 and the index, the overview's *Built* line — each true to the
   code, one home per fact.
9. **The commits:** five; count each subject's characters yourself (≤ 50, no exception).

## Your output

One file (the path above): a one-line verdict; the findings, most severe first (severity, file:line,
scenario, fix); a short "Checked and fine" list; then stop.
