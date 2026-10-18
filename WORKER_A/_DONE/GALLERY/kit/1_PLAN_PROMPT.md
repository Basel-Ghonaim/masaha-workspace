# GALLERY (S2b-4c) — the editor's photos: shrink, upload, order, cover, remove (web) — PLAN ONLY

**Worker A, a planning conversation** (the owner's trial: plan → execute → review). **You write the
plan only:** no branch, no edit, no commit, no server.
**Plan:** `C:\Users\basel\.prompt\MASAHA_WORKER_A\PLAN\GALLERY_PLAN.md` — save it, then stop.
If you are Claude Code: use `write-plan` for its discipline; otherwise follow §0.

**Where you read — important.** Worker A is **executing another plan right now** (ADMINLIST, branch
`feat/admin-deleted-spaces`) in the main folder `C:\Users\basel\masaha`: its working tree is changing.
**Do not work in that folder.** Work in `C:\Users\basel\masaha-design` (a clean worktree; never check
out anything there): run `git fetch origin`, then read the code **only from `origin/main`'s commit
objects** — `git show origin/main:<path>`, `git ls-tree -r --name-only origin/main <dir>`,
`git grep <pattern> origin/main -- <paths>`. Read ADMINLIST's plan
(`C:\Users\basel\.prompt\MASAHA_WORKER_A\PLAN\ADMINLIST_PLAN.md`) to know which files it changes.

## 0. The plan must stand alone

A fresh conversation executes it — **possibly Copilot or Codex** — **after ADMINLIST has merged**, from
the latest `origin/main`; a third conversation reviews. So: every decision taken with its one-line
reason; the files and, for each new hook, component or service, its interface (name, inputs, what it
returns or renders, the query keys it reads or invalidates); every user-facing string in Arabic and
English with its catalogue key; each state named to the design system's components; each test with
its lane, title and the break that must make it fail (`docs/development/testing.md` §3); the commits,
subjects counted (≤ 50); the executor's procedure with its commands (check ADMINLIST is in
`origin/main`; branch `feat/space-gallery` from the latest `origin/main`; checks after each commit;
`test:unit`, `test:component`, `NODE_ENV=production npm run build`, `check:build`, `lint`,
`typecheck`, `check:classes`, `format:check`, `check:links`; a real run on 5320 with the API on 3320
and `STORAGE_MODE=local`, screenshots to `C:\Users\basel\Downloads\gallery-shots\`; push;
`gh pr create --assignee @me --label feat --label area:web --label area:docs` with the description
written out; `gh pr checks` and `CLEAN`; the report to
`C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\GALLERY_REPORT.md`; the conflict check with
`git merge-tree --write-tree`); a **"Stop and ask"** list; an appendix mapping steps to Claude's skills,
"only a map". No step may depend on a Claude skill. Never merge; no tool attribution; stage by path.

## 1. The task

The admin's space editor gains its last section, **«الصور»**, on the photos API of PR #77
(`GET|POST /admin/spaces/:spaceId/photos`, `DELETE …/photos/:photoId`, `PUT …/photos/order`;
`SpacePhoto { id, urls: { card, page } }`, the first is the cover; 4 MiB; JPEG, PNG, WebP; 10 photos;
409 for the 11th; 413; 415; 30 uploads per 15 minutes; a verified space refused by `can()` with 403).
**One Work Item, three commits** (the owner):
1. **A domain-free upload layer in `shared/`:** shrinking an image in the browser, and a multipart
   upload through the one HTTP client with per-file progress — knowing nothing of spaces, so an avatar
   or another file kind can use it later (the owner's principle: build for the abstraction, don't build
   it).
2. **The gallery:** the photos in order with the cover marked, «اجعلها الغلاف», moving a photo before
   and after, removing one through an `AlertDialog`, the empty state.
3. **Uploading in the gallery:** choose files, each tile its own progress and its own failure with
   «إعادة المحاولة», the limit, the leave guard while an upload runs.
**If the plan finds more than about 70 files, or a decision the owner must take about the shared
layer, propose splitting into two Work Items in "Decisions needed" — do not decide it alone.**

## 2. Read first (from `origin/main`)

`CLAUDE.md`; `docs/development/workflow.md`; `docs/features/spaces.md` (the photos' API decisions of
#77; the editor's web decisions of #74 and #79 — the patterns to copy, as their reviews corrected
them); `docs/api/api-contract.md` › the photos' endpoints; `docs/backend/conventions.md`'s storage
line (a new file kind is a new consumer); `docs/frontend/architecture.md` (§3, §7, the transport,
*Forms*); `docs/frontend/design-system/foundation.md` §5, §9, §10, §12; `docs/frontend/localisation.md`;
the design: `C:\Users\basel\.prompt\MASAHA_DESIGN\DECISIONS_ADMIN.md` › A1 (the gallery: no date, no
confirm, no save), `DECISIONS_OWNER.md` › O7 (upload on choose, per-tile progress and failure 413/415
with retry, removal by `AlertDialog`, reorder and cover at once), DI-33 (the empty state); the
prototype's `PhotosSection` in `docs/design/prototype/masaha/profile-b.jsx`.

## 3. Settled decisions (the owner, 2026-10-15)

- **D1 — shrink in the browser to the longest side 1600 px** (the server's `page` size; nothing larger
  is ever kept), re-encoded at quality 0.85, so a phone photo travels small on a weak connection and
  stays under 4 MiB.
- **D2 — HEIC the browser cannot decode:** refused on its tile, «صيغة غير مدعومة، اختر JPEG أو PNG أو
  WebP» (write the English). **No new dependency.**
- **D3 — one upload at a time,** in the order chosen (the order is the gallery's; a weak connection is
  not shared; the 30-per-15-minutes limit is not hit by a burst).
- **D4 — order by arrows** «قبل» / «بعد» and «اجعلها الغلاف», as the admin's lists move rows (keyboard
  and screen reader); no drag and drop now.
- **D5 — choosing more photos than the 10 allow:** upload what fits, and say so: «رُفعت 3 من 5؛ الحد
  10 صور» (write the English); «إضافة صور» disabled at 10 with its reason.
- **D6 — the leave guard asks while an upload runs** (the photos are immediate actions; only an
  unfinished upload is lost).
- **Settled by the design:** removal through an `AlertDialog`; no date, no confirm, no save (A1); the
  empty state «لا توجد صور بعد · الصورة الأولى تصبح الغلاف» (DI-33); a verified space's gallery
  read-only; the section made for the owner's editor to reuse, as #74's D5.

## 4. Findings

Read the open findings' titles; open those that touch the editor or uploads (63, 64, 67). New findings:
**73–74**.

## 5. Boundaries

ADMINLIST changes `features/space-links` (the admin list), `features/spaces/components/menu/`,
`features/spaces/hooks/delete/useRestoreSpace.ts`, `features/spaces/hooks/menu/`,
`features/spaces/types/SpaceRef.ts`, `pages/dashboard/admin/SpacesPage.tsx`, the `spaceLinks` copy
files: your plan builds after it merges, so list any of those you also need and say why. Worker B
(OWNERSREAD) adds `owners` to `AdminSpace` and touches `routes.component.test.tsx` and
`SpaceEditor.component.test.tsx`: if your plan needs those, it builds after B merges too — say so.
Nothing in `apps/api` or `packages/shared` (the API is built); if the gallery needs a change there,
stop and say so.
