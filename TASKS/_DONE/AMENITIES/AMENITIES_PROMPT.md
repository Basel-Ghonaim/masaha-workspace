# AMENITIES — no amenity filter, and a space's own amenities (API, with the web's lookups screen)

**The amenities worker** (one-off, named after its task) · worktree `C:\Users\basel\masaha-amenities`,
detached at `origin/main` (`d7d800e`), its own `node_modules`, `.env` files ready (never print them).
Branch `feat/space-own-amenities`, cut with `git fetch --prune origin`, then
`git switch --no-track -c feat/space-own-amenities origin/main`; first push `git push -u origin
feat/space-own-amenities`. **Databases** `masaha_amenities_dev` / `masaha_amenities_test` in the
shared container (migrated and seeded); **API on 3322, web on 5322**. The container is shared: never
`npm run db:up` from this folder (finding 48); if Docker stopped, `docker start masaha-postgres-1`.

**Model:** Opus 5.5, effort high. **Size cap:** at most 3 subagents, no self-review subagent, no workflow.
**Plan:** `C:\Users\basel\.prompt\MASAHA_AMENITIES\PLAN\AMENITIES_PLAN.md` (`write-plan`; save, then stop).
**Report:** `C:\Users\basel\.prompt\MASAHA_AMENITIES\REPORT\AMENITIES_REPORT.md` (`final-report`).
Follow the skills from start to end: `start-work-item` (you are a task worker; your folder is the one
above, detached like worker B's), `write-plan`, `open-pr`, `final-report`.

**The owner's override, stated:** workflow §9 keeps two items out of one layer at once. Worker B's PR
#62 (users) is open in the API layer meanwhile; the owner runs this item in parallel on purpose: #62
changes no schema and touches none of this item's code, only three shared documents (below).

## 1. The task in brief

The owner reopened the amenities (2026-10-12): every space claims fast internet and stable power, and
nobody looks for a space by its hot drinks, so **amenities stop being a filter**. And an owner must be
able to say what their space offers beyond the platform's list. Two changes, one PR:
- **No amenity filter anywhere:** the amenity's filter flag goes from the database, the API, the
  shared package, the seed, the admin's lookups screen and the documents; the directory's planned
  `amenities` filter goes from the scope and the plan.
- **A space's own amenities:** beside the platform's list (common amenities, with their icon and both
  names, ticked in one click), a space keeps its own amenities as short texts, part of the amenities
  fact group.

## 2. Read first

In the order workflow §2 *Reading before work* gives.
- **The capability documents first:** `docs/features/lookups.md` (all: the amenities, their decisions)
  and `docs/features/spaces.md` (*Behaviour* › *Amenities* and *Save a group*, *Confirm*, *API
  decisions*).
- `docs/architecture/data-model.md` › *Conventions* (bilingual content, freshness) and *Spaces*
  (Amenity, SpaceAmenity); `docs/api/api-contract.md` §1–§4, §5 › *Lookups (public)*, *Lookups (the
  admin)*, *Spaces (the admin)* (the amenities group, confirm), §6; `docs/backend/conventions.md` §6
  (audit), §7 (`lookups` L0, `spaces` L1), §13 (the space's lock); `docs/development/testing.md`
  §1–§4; `docs/architecture/shared-package.md`;
- `docs/project/overview.md` (the *Directory* scope line and *Built*); `docs/plans/v1-mvp.md` (the
  planned `GET /spaces` row and the owner's `PUT /manage/spaces/:spaceId/:group`);
- the code: `apps/api/prisma/schema.prisma`, the `lookups` module's `amenities/` and `catalogue/`,
  the `spaces` module's `amenities/` and `facts/` (the one save path), the seed's lookups;
  `packages/shared/src/lookups/` and `spaces/`; the web's `features/lookups/` (the amenities' screen,
  its hooks and copy).

## 3. The settled decisions (review them in "Stronger decisions")

- **D1 — no amenity filter.** Drop `amenities.is_filterable` (one migration); remove the flag from
  `@masaha/shared/lookups`, the admin's `POST`/`PATCH /admin/amenities` and their answer, the public
  catalogue, the mappers and repositories, and the seed. On the web's lookups screen remove the
  «In filters» switch, its badge, its hook and its copy lines (both catalogues), and their tests; the
  rest of the screen (names, icon, active, order) stays. In the documents: lookups.md's decisions
  (#16's "Internet and stable power are not filters" is superseded, dated, with the owner's reason),
  the data model's Amenity, the contract, the overview's *Directory* line (no "amenities that tell
  spaces apart"), and the plan's `GET /spaces` row (no `amenities` filter).
- **D2 — a space's own amenities, in the amenities group.** A new table of a space's own amenities
  (its Arabic name required, its English optional, its order), cascading from the space. The amenities
  group is saved whole on the one save path, under the space's lock, with `can()`, its date and its
  audit entry, and confirmed as today: `PUT /admin/spaces/:spaceId/amenities` takes the platform's
  amenity ids **and** the space's own, replaced whole in their order. Settle in the plan: the field
  names, the caps (count and length, in the contract's style), a repeat refused `not_unique` on its
  field as the other groups do, the user-text rule both apps run, how `AdminSpace` and the audit
  entry show them, and that a save that changes nothing writes nothing.
- **D3 — the platform's list stays the admin's** (lookups): common amenities with an icon and both
  names, retired and restored as today; an owner never adds to it. Only the filter flag goes.
- **D4 — the owner's endpoints (step 5) reuse this save path;** build none of them here.

**Not in this item:** any screen (the editor and the space page are the design batches' and the web's
later); the public directory API (step 3, worker B's next item); photos.

## 4. Findings

Read the open findings' titles; open any that may touch amenities, the lookups or the facts. Your new
findings number **53–54**.

## 5. Risks

- **The migration:** create it once with `migrate dev --create-only`, then `ls` it — a second
  `--create-only` applies it to the dev database. Apply it to `masaha_amenities_dev` and run the API
  lane on `masaha_amenities_test`; check it runs clean on an empty database (a scratch one, not
  `migrate reset`).
- **The shared package:** rebuild its `dist` (`npm run build -w @masaha/shared`) before the API's and
  the web's checks; a stale `dist` once hid a CI failure.
- **Every behaviour proven in its lane,** each new test seen failing first (testing §3 rules 5–7);
  the amenities group's lock and its date proven as the other groups' are.

## 6. Boundaries with the other workers

- **Worker B (PR #62, users)** works in `masaha-b`: you touch nothing in `shared/auth`, `users`,
  `space-links`, `core/errors.ts` or the catalogues' `errors.ts`. Three documents are shared:
  `api-contract.md`, `v1-mvp.md` and `overview.md` — keep to your own sections; the *Built* line of
  the overview will likely conflict: whichever PR merges second resolves it by the fast path
  (workflow §9 *Conflicts*: keep both sides, `format:check` and `check:links`, one push).
- **Worker A** works in the main folder on the web, outside `features/lookups/` (yours, under
  workflow §9's licence: what breaks in the web when a shared type changes) and the two `errors.ts`.
- **The design fixer** works in `docs/design/` only.
- No new dependency.

## 7. Checks, the pull request and the report

- **Locally, once each on the head, one at a time:** `test:unit`, `test:component`, `test:api`;
  `NODE_ENV=production npm run build` and `check:build`; `lint`, `typecheck`, `check:classes`,
  `format:check`, `check:links`.
- **Real requests** against your API (3322), each in the report: the public catalogue without the
  flag; an amenity added and edited without it; a space's amenities saved with two of its own, read
  back in order, confirmed, saved again unchanged (nothing written), a repeat refused. And the web on
  5322: the lookups screen's amenities tab without the switch, at 390 and 1440 (screenshots in
  `C:\Users\basel\Downloads\amenities-shots\`, never committed). Stop the servers by PID and check
  ports 3322 and 5322 free.
- **PR:** title `feat(spaces): own amenities, no amenity filter` (≤ 50), labels `feat`, `area:api`,
  `area:web`, `area:docs`, assigned to the owner. An independent review follows (schema). Don't merge.
- **The documents in this PR:** the contract; the data model; `lookups.md` and `spaces.md` (decisions
  and history by layer, the code maps); the overview (*Directory* scope line, *Built*); the plan's
  `GET /spaces` row; any document that still promises an amenity filter.
- At the report, `git merge-tree --write-tree` against every open PR (#61, #62, and worker A's).
  Stop every background shell you start; `jq` is not installed — use `gh … --jq`.
