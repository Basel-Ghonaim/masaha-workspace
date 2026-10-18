# MEDIA — a space's photos: the storage port, Cloudinary online, the admin's gallery API and the public photos (API)

**The media worker** (one-off, named after its task) · worktree `C:\Users\basel\masaha-media`,
detached at `origin/main` (`e30a86c`), its own `node_modules`, `.env` files ready (**never print
them; print keys only**). **Databases** `masaha_media_dev` / `masaha_media_test` in the shared
container (migrated and seeded); **API on 3322, web on 5322**. The container is shared: never
`npm run db:up` from this folder (finding 48); if Docker stopped, `docker start masaha-postgres-1`.

**Model:** Opus 5.5, effort high. **Size cap:** at most 3 subagents, no self-review subagent, no workflow.
**Plan:** `C:\Users\basel\.prompt\MASAHA_MEDIA\PLAN\MEDIA_PLAN.md` (`write-plan`; save, then stop).
**Report:** `C:\Users\basel\.prompt\MASAHA_MEDIA\REPORT\MEDIA_REPORT.md` (`final-report`).
Follow the skills from start to end: `start-work-item` (you are a task worker; your folder is the one
above, detached like worker B's), `write-plan`, `add-error-code` (for any new code), `open-pr`,
`final-report`.

**When you build — read this first.** You plan now, in parallel with worker B's open item
(DIRECTORY, branch `feat/public-directory`), which edits `apps/api/src/app.ts`,
`apps/api/src/modules/spaces/index.ts` and adds the `directory` module and its migration — files this
item needs too (workflow §9, *Items in parallel*, rule 3). So: **plan against today's `main` and
DIRECTORY's plan** (`C:\Users\basel\.prompt\MASAHA_WORKER_B\PLAN\DIRECTORY_PLAN.md`, read-only), and
**cut your branch only when the reply says DIRECTORY has merged**: `git fetch --prune origin`, then
`git switch --no-track -c feat/space-photos origin/main`; first push `git push -u origin
feat/space-photos`. After that merge the analyst applies its migration to your databases and rebuilds
your shared `dist`; check it before you build.

## 1. The task in brief

A space has photos: designed (A1's gallery, O7's immediate actions, U12's cover on the card), modelled
(`SpacePhoto`, ordered, by storage key), never built. This item builds **the whole server side**:
- **the storage port** (`docs/backend/conventions.md` §1, §12; ADR 0014): byte-level, with a local
  adapter for development and tests and a **Cloudinary** adapter online;
- **the image pipeline:** every upload decoded and **re-encoded on the server** into WebP sizes, its
  metadata dropped;
- **the admin's gallery API** on one space: list, upload one, remove one, reorder (the first is the
  cover), under the space's rules;
- **the public photos**, on worker B's directory once merged: the cover's small size on a list item
  (U12) and the photos on a space's page.

The web (the editor's gallery, the browser's shrinking, the card's cover) is **not** in this item:
worker A builds it on this API later. Design what the web will need into the contract.

**Why this shape** (the owner, 2026-10-13, after reading the "quick tweets" project's media module,
`D:\quick-tweets-app\docs\backend\media.md` and `apps\api\src\modules\media\` — read them as a
reference, not a rulebook; its decisions differ from ours): that module served many features with a
media registry, a reference ledger and a garbage collector, and stored on local disk with no resizing.
Masaha has one consumer (a space's photos), deploys on Vercel's free tier, and serves people on weak
connections in Gaza. Take its port, its content checks and its clean-up on failure; leave its
registry, ledger, reclamation job and self-serving of bytes.

## 2. Read first

In the order workflow §2 *Reading before work* gives.
- **The capability document first:** `docs/features/spaces.md` (whole: the save path, the space's
  lock, `can()` and verified, the admin's router, the code map).
- `docs/backend/conventions.md` §1 (the layout: `shared/storage/`), §2, R5 and R6 (**they disagree on
  where a port lives**, D2), §6 (audit), §7 (levels), §8, §12 (environments, the ports' table, *no
  work after the response*), §13 (locks; idempotency); `docs/backend/security.md` (*HTTP hardening*:
  the 5 MB photo line against the 4.5 MB platform limit, D5; rate limits; authorization);
  `docs/architecture/decisions/0014-deployment.md` (files, free tiers), 0012, 0015;
  `docs/architecture/data-model.md` (*Conventions*: freshness lists **photos in the profile group**,
  D8; *Spaces*: `SpacePhoto`; cascades) and `apps/api/prisma/schema.prisma`'s `SpacePhoto`;
  `docs/api/api-contract.md` §1–§6 (413 and 415 are reserved), §5 › *Spaces (the admin)*;
  `docs/plans/v1-mvp.md` (step 5 "settles photos"; the planned `/manage/spaces/:spaceId/photos` row);
  `docs/development/testing.md` §1–§4 (a port is the one legitimate seam, rule 3);
  `docs/development/setup.md` (environment, CI).
- The design (what the API must serve; no screen here): `C:\Users\basel\.prompt\MASAHA_DESIGN\DECISIONS_ADMIN.md`
  › A1 (the gallery: no date, no confirm, no save), `DECISIONS_OWNER.md` › O1, O7 (upload on choose,
  per-tile progress and failure 413/415 with retry, removal by AlertDialog, reorder and cover at once),
  `DECISIONS_PUBLIC.md` › U12 (the cover on the card, a small thumbnail, lazy, a fixed ratio; no
  photo → the space's mark), U8 and PU-023 (the page's gallery; none → a caption); the prototype's
  gallery in `docs/design/prototype/` (find it; say where).
- DIRECTORY's plan (above), read-only: the list item and page shapes you will extend.

## 3. The settled decisions (review them in "Stronger decisions")

- **D1 — online storage is Cloudinary's free plan** (the owner: free, no bank card; paid plans come
  with funding). **Cloudinary is a dumb store only:** we upload the finished WebP files and serve them
  as they are, with no Cloudinary transformation (no credits spent on transformations, no original
  ever stored there, and a move to R2 or S3 later is a new adapter, not new data). The adapter talks
  to Cloudinary's REST API with `fetch` and a signed request (**no Cloudinary SDK**). Name its
  environment in the plan; recommended: `STORAGE_MODE` (`local` | `cloudinary`, as `EMAIL_MODE` is)
  and Cloudinary's own `CLOUDINARY_URL`. **Production refuses to start without it**, as it does
  without Google's id. Keep dev and production apart on the one free account (a folder per
  environment).
- **D2 — placement:** the port and its adapters in `apps/api/src/shared/storage/` (conventions §1 and
  R6: the platform, bytes by key, no domain); a space's photos in `spaces` (`photos/`), which owns
  `space_photos`, the limit, the order, the cover, the sizes and who may act. **No `media` module**
  and no change to the level map. R5's "the port lives in the module that needs it, never in
  `shared/`" contradicts §1 and R6 for storage: correct R5's sentence in this PR, in the commit that
  builds the port.
- **D3 — libraries where the work is hard and security-sensitive, hand-written where it is thin:**
  `sharp` decodes, resizes, re-encodes to WebP and drops the metadata — **decoding is the real
  content check** (a file sharp cannot decode as JPEG, PNG or WebP is 415), so no signature table is
  written by hand; `multer` (memory storage, one file, a byte limit, no other parts) parses the
  upload — streaming as quick tweets did buys nothing under a 4.5 MB request that sharp reads whole.
  The Cloudinary calls (upload, delete) are hand-written (D1). **Two dependencies, one item:** this is
  the only item adding dependencies now (workflow §9, rule 2); declare both in the plan with their
  versions and why (sharp's native binary on Vercel and on Windows; check `check:build` is unaffected —
  both are API-only).
- **D4 — the table does not change** (the owner): `SpacePhoto.path` holds **one storage key**; each
  size is derived from it by a fixed suffix (for example `<key>/card.webp`, `<key>/page.webp`); no
  provider URL is ever stored — the URL is built at read time from the key and the configuration.
  The cover is the first photo by `sortOrder`. If the plan finds a real need for a column, it says so
  as an open question: **no migration without the owner's approval.**
- **D5 — the upload goes through our API, small:** the web will shrink a photo before sending it
  (A's later item); the server accepts one image per request **below Vercel's 4.5 MB request limit
  including the multipart overhead** (settle the number, about 4 MB), refuses a larger one with 413
  and anything not a decodable JPEG, PNG or WebP with 415. security.md's "5 MB per photo" line becomes
  true to this (and to D3's re-encoding) in this PR. Settle the sizes and quality of the WebP files
  (recommended: two — a card size for U12's thumbnail and a page size — with the longest side, the
  quality and a decode-time guard against decompression bombs, sharp's `limitInputPixels`), and say
  what a portrait or panorama becomes.
- **D6 — the gallery API, the admin's first, the owner's later:** on the admin's router for one space
  (`/admin/spaces/:spaceId/photos…`): **list** (its own read, so `AdminSpace` and the web's fixtures do
  not change while worker A builds the editor on them), **upload one** (answers the new photo),
  **remove one**, **reorder** (the whole list of ids, exact or 409, as the lookups' order is). Same
  service for the owner's `/manage/spaces/:spaceId/photos` later (step 5): build nothing of `/manage`
  now, but nothing that would stop it. **Who may act is `can()`'s**, as for every fact group: the
  admin edits an unverified space's photos; a verified space's are its owner's
  (security.md › *Authorization*). Settle the answer's shape (each photo: id, order, the URLs of its
  sizes) and the paths' names.
- **D7 — at most 10 photos a space** (O7; DI-32 asks whether 10 is the cap: it is), checked **under
  the space's lock**, so two uploads at once cannot pass it; the 11th is refused (a domain code or
  `invalid_choice` — settle it; `add-error-code` if new).
- **D8 — photos carry no freshness date and no confirm** (A1, O7: "no save, no date"). The data
  model lists photos in the profile's group; **recommended:** photos leave the freshness groups, and
  a photo change dates nothing (the data model's line corrected). Weigh it in "Stronger decisions"
  if you see a reason the profile's date should move.
- **D9 — the order of work around the store** (ADR 0014: nothing runs after the response; the
  conventions: no network call inside a transaction): **upload** — decode and re-encode, store the
  files under a new random key, then one transaction under the space's lock (`can()`, the count, the
  row at the end of the order, the audit entry); a refusal or a failure there deletes the stored files
  before answering. **Remove** — the row deleted (the order closed up) and audited in its
  transaction, then the files deleted before answering; a failed delete is logged, never answered as
  a failure. **No reclamation job in v1:** a file left behind by a crash is recorded as a finding (its
  number from §4) with what would resolve it.
- **D10 — the audit:** each change is audited as a space's fact change (conventions §6): upload,
  removal, order; settle the names and what each entry holds (ids and order, never a URL or a key).
- **D11 — privacy:** no metadata survives (D3), proven by a test that uploads a JPEG carrying EXIF GPS
  and reads none back from the stored file. Storage keys are random and unguessable; nothing about the
  uploader is written to the store.
- **D12 — the public side, on the merged directory:** a list item and a pin's selected card carry the
  cover's card-size URL, or nothing (the web draws the space's mark, U12); a space's page carries its
  photos in order, page size, with the card size where the web needs it. Only a publicly listed
  space's photos are public. Settle the cache rule with DIRECTORY's (its list is cached; a URL that
  never changes for a key can be cached long by the CDN).
- **D13 — development and tests:** the local adapter writes under a git-ignored folder; the API lane
  uses it (or an in-memory one) through the port, never a mock of a module (testing §3, rule 3). How
  the web reaches a locally stored photo in development without a path that differs between
  environments (conventions §12: "no module, rule or path changes between them") is the plan's to
  settle, with options and a recommendation.

## 4. Findings

Read the open findings' titles; open those that touch storage, deployment headers (33, 46 — the
web's `img-src` must allow Cloudinary's delivery host online: a finding like 46 if no header config
exists yet), rate limits (23) and concurrency (52). Your new findings number **63–64**.

## 5. Risks

- **sharp's native binary** on Windows locally, in CI (Ubuntu) and on Vercel: prove the first two;
  say what proves the third.
- **The 4.5 MB limit** is the platform's, not Express's: a test of our limit proves our code, not
  Vercel's; say so.
- **Memory:** `multer`'s memory storage and sharp's decode of a large image (pixel limit, D5).
- **Cloudinary's signature** and its error answers: a failed store is a 5xx with nothing written;
  a store that times out after Cloudinary kept the file is the finding of D9.
- **Secrets:** the `CLOUDINARY_URL` is a secret: never print it, never log it, never in a test
  fixture; `.env.example` names it with no value. The owner adds it to this folder's `apps/api/.env`
  for the real run; if it is absent then, run against the local adapter and say what was not run.
- **The machine (the owner's rule): one full test run at a time on this machine.** Before a full lane
  (`test:api`, `test:component`), check that worker A (the main folder) and worker B (`masaha-b`) are
  not running one; if one is, wait.

## 6. Boundaries with the other open items

- **Worker B — DIRECTORY** (`masaha-b`, `feat/public-directory`): you build after it merges (above).
  Its files are then `main`'s; D12 extends them.
- **Worker A — S2b-4a, the admin's space editor** (main folder, `feat/admin-space-editor`): `apps/web`
  only. You change **nothing in `apps/web`**, and no shared type the web already imports
  (`AdminSpace`, the spaces requests): that is why D6's list is its own read. If the plan finds a
  shared type the web uses must change, it stops and says so. `spaces.md`'s *Web* parts are A's; you
  write its *API* parts and the code map's API and Shared lines (fast path on a conflict).
- **Two design fixers** work in `docs/design/` only; you touch nothing there.
- The documents you share (the contract, `spaces.md`, the overview's *Built* line, the findings
  index) take the fast path.

## 7. Checks, the pull request and the report

- **Locally, once each on the head, one at a time:** `test:unit`, `test:api`; `lint`, `typecheck`,
  `format:check`, `check:links`; the build and `check:build`; `test:component` only if a shared type
  reaches the web (say why if not run).
- **Real requests** against 3322, each in the report (with the local adapter, and with Cloudinary when
  the owner has added its key): upload a JPEG with GPS EXIF (the stored WebP has none, its sizes
  right), a PNG and a WebP; a text file renamed `.jpg` (415); an oversize file (413); the 11th photo
  (refused); reorder (the cover changes) and a stale order (409); remove one (its files gone); a
  verified space's upload by the admin (refused by `can()`); the public list's cover and the space's
  page photos; the URLs opening in a browser.
- **PR:** title ≤ 50 (for example `feat(spaces): a space's photos`), labels `feat`, `area:api`,
  `area:docs`, assigned to the owner. An independent review follows (two dependencies, uploads,
  security). Don't merge.
- **The documents:** the contract (the gallery's endpoints and payloads, the public fields, 413/415's
  lines, any new code); `spaces.md` (*What it does*, *Behaviour* › photos, *API decisions*, *API
  history*, code map); `directory.md` (the public photos); conventions (§1's storage, R5's sentence,
  §12's ports table and what is built); security.md (*HTTP hardening*: the real limit, the types,
  the re-encoding, no metadata, the secret); the data model (D8, and `SpacePhoto`'s key); setup.md
  (`STORAGE_MODE`, `CLOUDINARY_URL`, the local folder); ADR 0014 only by a dated *Revised* line if the
  plan finds it needs one; `v1-mvp.md`'s photo rows; the overview's *Built* line.
- At the report, `git merge-tree --write-tree` against every open PR. Stop every background shell
  you start; `jq` is not installed — use `gh … --jq`.
