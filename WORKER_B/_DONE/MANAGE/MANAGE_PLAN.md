> **Approved by the owner, 2026-10-15, with one change (the analyst's check):** workflow §3 puts a unit's documents in the same commit as its code — fold `docs(spaces): document managed space API` into the code commit (or split the code into two commits, each carrying its documents). Build **only after OWNERSREAD is in `origin/main`**, in `C:\Users\basel\masaha-b`, never in a design worktree. `MANAGE-copilot-draft.patch` beside this plan is an **unreviewed** draft the planning session wrote by mistake, before OWNERSREAD merged: the executor builds from this plan, and may read the draft only as a hint. Everything else as written.

# Plan: add the owner's managed-space API

**Work Item:** MANAGE, v1 MVP step 5a  
**Worker:** B  
**Base:** latest `origin/main`, after OWNERSREAD has merged  
**Branch:** `feat/owner-space-api` in `C:\Users\basel\masaha-b`  
**Mode:** API/shared contract and documentation only; no web screen

## Contract

### Scope

Add the owner/reception API under `/api/v1/manage/spaces/:spaceId`:

| Method | Path | Access | Behaviour |
|---|---|---|---|
| `GET` | `/manage/spaces/:spaceId` | active owner or reception | Read the profile and all facts, using the existing `AdminSpace` shape. |
| `PATCH` | `/manage/spaces/:spaceId` | active owner | Update the profile through the existing profile service. |
| `PUT` | `/manage/spaces/:spaceId/hours` | active owner | Save hours and shifts through the existing hours service. |
| `PUT` | `/manage/spaces/:spaceId/prices` | active owner | Save prices through the existing prices service. |
| `PUT` | `/manage/spaces/:spaceId/amenities` | active owner | Save amenities through the existing amenities service. |
| `PUT` | `/manage/spaces/:spaceId/contacts` | active owner | Save contacts through the existing contacts service. |
| `POST` | `/manage/spaces/:spaceId/:group/confirm` | active owner | Confirm one fact group through the existing confirm service. |
| `GET` | `/manage/spaces/:spaceId/photos` | active owner or reception | List photos through the existing photos service. |
| `POST` | `/manage/spaces/:spaceId/photos` | active owner | Upload a photo through the existing photos service, limits and storage included. |
| `DELETE` | `/manage/spaces/:spaceId/photos/:photoId` | active owner | Remove a photo through the existing photos service. |
| `PUT` | `/manage/spaces/:spaceId/photos/order` | active owner | Reorder photos through the existing photos service. |

Mount `requireSpaceAccess` exactly once on `/manage/spaces/:spaceId`, before every
manage router. The middleware loads the space links with the existing `space-links`
service, refuses callers without an active link, and places `LoadedSpace` on the
request. Because the security documents do not assign a status to that refusal, use
`404 not_found` so an unrelated caller cannot learn that the space exists. An unknown
or soft-deleted space is also `404`; a hidden live space remains manageable by its
owner and readable by its reception staff.

The manage routes reuse the admin services, controllers, validation schemas, photo
limits and audit action names. No service or authorization rule is copied. The
owner's write permission remains `can(..., 'space.profile.update' | 'space.facts.update' |
'space.photos.manage')`; the read permission is a new `space.read` staff action so
the reception role is explicit in the permission table. The admin remains on
`/admin`: ADR 0009 makes `ADMIN` platform-only, and `/manage` requires an active
space link, so an admin without such a link is not admitted.

No packages, capacity, stay limit, settings, staff, web screen, schema migration or
new dependency is included.

### Acceptance criteria

- `requireSpaceAccess` is implemented in `shared/auth`, accepts the existing links
  loader seam, and is mounted once at the managed-space prefix.
- Reception can read the complete space response and photos, but every mutation is
  refused by `can()`; the owner can read and mutate their verified space.
- A stranger, a signed-in user with no link, an owner of another space and an admin
  without a space link receive the no-hint refusal; an unknown or deleted space
  returns the existing `not_found` envelope.
- A hidden space remains available to its active owner/reception link.
- The four fact writes, profile patch, fact confirmations and four photo operations
  reach the same services and produce the same audit action names as `/admin`.
- Photo upload is rate-limited before the file is read and uses the same size,
  decoding, storage cleanup, lock and concurrency behaviour as the admin route.
- `/admin` behaviour is unchanged, including its unverified-space admin rules.
- API contract, spaces capability documentation, space-links documentation and the
  backend security/conventions built-status text are updated in the same PR.
- API integration tests cover every protected endpoint and the required role/space
  matrix; unit tests cover any new pure authorization rule or middleware decision.

### Out of scope

- Step 5b packages and prices/packages management.
- Capacity, occupancy, live status, stay limit and space settings.
- Staff management, customers, subscriptions, payments, announcements, reports,
  finance or audit-log reads.
- Any `apps/web` production file or screen.
- Changes to Prisma schema, migrations, shared request schemas, storage providers or
  rate-limit policy.
- Finding 17, 21, 23, 52 or 59 resolution beyond behaviour directly required here.

## Decisions

| Decision | Reason | Cost |
|---|---|---|
| Use one `requireSpaceAccess` middleware at `/manage/spaces/:spaceId`. | This is the convention's single access boundary and prevents one module router from omitting the link check. | The composition root must expose all manage routers beneath the same mount. |
| Return `404` for no active link. | Security.md requires an active link but is silent on status; hiding existence is the safer settled D2 choice. | The client cannot distinguish an unknown space from an unauthorized one. |
| Keep `/manage` owner/reception-only; do not admit `ADMIN`. | ADR 0009 says the global admin role is platform-only and space permissions come only from an active link. | An admin uses the existing `/admin` routes, even for a verified space. |
| Add `space.read` as a `staff` permission. | D3 requires reception reads and owner writes, and `can()` must decide every protected action rather than a controller role check. | `can` tests and API matrices gain one action; the shared action table remains the single rule source. |
| Reuse `AdminSpace` for the managed read. | The editor needs the same profile/fact payload and no new web contract is required. | The endpoint documentation must state that the shape is shared by admin and manage reads. |
| Keep the existing `AdminSpace` write responses. | Services already return the complete response after edits/confirmation; changing the response shape would duplicate logic. | The API contract must document the same response for both route families. |
| Use separate manage router files per module where the existing module boundaries require it, but share controllers/services. | The convention names one router per audience and the prompt requires the common middleware before every module manage router. | The composition root has a few additional router mounts. |

## Related findings

- **17 — Expired rate-limit counters and abandoned sessions are never swept:** do
  not fold; this item uses the existing photo-upload limiter and does not add a
  scheduler.
- **21 — A token replayed within the grace window starts its own branch:** do not
  fold; authentication token rotation is unrelated.
- **23 — No per-address ceiling for signed-in requests:** do not fold; the existing
  general signed-in limit remains the platform policy.
- **52 — The race tests wait a fixed time:** do not fold; use the existing photo
  race tests and do not alter the shared race harness in this API item.
- **59 — The verified space's editor cannot name its owner:** do not fold; this item
  adds no owner-name payload or web editor.
- **75–76:** no files or titles for these numbers exist in the inspected
  `origin/main` findings index/tree. Do not invent resolutions. If their supplied
  descriptions become available before execution and change authorization, locking,
  the endpoint contract or file ownership, stop and ask before editing.

## Files and interfaces

### Shared authorization and composition

- `apps/api/src/shared/auth/spaceAccess.ts` (new)
  - `requireSpaceAccess(loader: LinksLoader): RequestHandler`.
  - Parse `:spaceId`, load links and the space existence through the existing
    `linksAt` path, and throw `AppError.notFound()` when no active link exists.
  - Attach `LoadedSpace` with `links` and `linksUnder(tx)`, preserving the
    existing lock-consistent service seam.
- `apps/api/src/shared/auth/can.ts`
  - Add `'space.read': 'staff'` to the permission table and its inferred
    `SpaceAction` type.
- `apps/api/src/shared/auth/index.ts`
  - Export the middleware.
- `apps/api/src/app.ts`
  - Build the manage routers after the existing services are composed.
  - Mount `requireAuth()` and then `'/manage/spaces/:spaceId'`,
    `requireSpaceAccess((id, tx) => spaceLinks.linksAt(id, tx))`, followed by
    every manage router.
  - Keep the existing `/manage/spaces` `mySpaces` route before the parameter route.
  - Keep `/admin`'s non-refusing `loadSpaceLinks` and all existing guards unchanged.

### Controllers and routers

- `apps/api/src/modules/spaces/spaces.manage.routes.ts` (new)
  - `createSpacesManageRouter({ space, profile, hours, prices, amenities, contacts, confirm }): Router`.
  - Mount `GET`, `PATCH`, the four fact `PUT`s and the dynamic fact-group confirms
    without duplicating validation or service logic.
- `apps/api/src/modules/spaces/photos.manage.routes.ts` (new, or the equivalent
  photos-owned manage router if the existing module layout keeps photos nested)
  - `createPhotosManageRouter({ photos, limiter }): Router`.
  - Mount photo list/upload/order/remove with the exact admin schemas, upload limiter,
    `receiveFile` and `PHOTO_MAX_BYTES`.
- `apps/api/src/modules/spaces/index.ts`
  - Export the manage routers.
- Existing controllers under `apps/api/src/modules/spaces/`:
  - Extend the shared read handler only if needed to call `can(actor, 'space.read', space)`.
  - Do not add route-specific role checks or duplicate handlers.

### Tests

- `apps/api/src/shared/auth/can.unit.test.ts`
  - Add the `space.read` owner/reception/other-space/stranger/admin cases.
- `apps/api/src/shared/auth/spaceAccess.api.test.ts` (new)
  - Prove active-link acceptance, no-link `404`, deleted/unknown `404`, and
    `linksUnder(tx)` preservation through the real request path.
- `apps/api/src/modules/spaces/manage.api.test.ts` (new, or the existing API test
  file if the repository's test grouping requires one)
  - Exercise the complete managed route matrix and response persistence.
- `apps/api/src/modules/spaces/photos/photos.api.test.ts` and
  `photosRace.api.test.ts`
  - Extend only if the manage path needs a route-specific assertion; retain one
    proof for the shared service behaviour and do not duplicate every admin case.

### Documentation

- `docs/api/api-contract.md`: add the managed-space endpoint rows, access matrix,
  response/error semantics and explicit reuse of the admin shapes.
- `docs/features/spaces.md`: add the managed API behaviour and code-map entries,
  including reception read/owner write and photo reuse.
- `docs/features/space-links.md`: document that the managed route's access comes
  from active `OWNER`/`RECEPTION` links and deleted spaces are excluded.
- `docs/backend/conventions.md`: mark `requireSpaceAccess` as built and describe
  its 404 refusal and one-prefix mounting.
- `docs/backend/security.md`: record the active-link authorization boundary and
  no-hint response if the contract's current wording does not already cover it.
- `docs/plans/v1-mvp.md`: change only the planned managed rows that this item
  actually builds, leaving later rows clearly planned.
- `docs/project/overview.md`: add the managed API to the existing Spaces built
  line only if the documentation's current “Built” claim is still incomplete after
  the implementation; do not claim a web screen is built.

No `packages/shared` file is expected to change. If the existing `AdminSpace` or
request schemas cannot represent the managed response without a contract change,
stop, list the required shared files, and obtain approval before widening scope.

## Tests and deliberate breaks

All endpoint tests are `*.api.test.ts` and use real PostgreSQL; pure permission
logic is `*.unit.test.ts`. Every new test is written and run red before the
implementation. Authorization and ordering/lock properties follow testing §3 rule 7:
make the break once, observe the test fail, then restore the production code before
commit.

1. **`requireSpaceAccess` accepts an active owner and reception link.**  
   Break caught: rejecting reception or loading the wrong space resource. Deliberate
   break: temporarily remove the active-link branch and observe the API test fail.
2. **A stranger, unrelated owner, unlinked user and admin receive `404`.**  
   Break caught: global-role admission, a link to another space, or a `403`/success
   hint. Deliberate break: temporarily bypass the no-link refusal and observe red.
3. **Unknown and soft-deleted spaces receive `not_found`.**  
   Break caught: treating a deleted link as active or allowing a deleted space through.
4. **Reception can `GET` the complete space and photos.**  
   Break caught: using an owner-only permission for reads or mounting a route without
   the middleware.
5. **Reception cannot profile/fact edit, confirm, upload, delete or reorder.**  
   Break caught: any controller-side omission or accidental `staff` write permission.
   Deliberate break: temporarily change one write permission to `staff` and observe red.
6. **The owner can profile/fact edit and confirm.**  
   Break caught: failing to pass `signedIn` actor and `spaceOf(req)` to the shared
   service or mounting validation on the wrong request source.
7. **The owner can list/upload/delete/reorder photos; reception is read-only.**  
   Break caught: route wiring that bypasses the common photo service, limiter,
   `receiveFile`, or `can`.
8. **Photo upload is limited before the file is read.**  
   Break caught: placing `receiveFile` before `limitRequests`, which permits expensive
   decoding for refused uploads.
9. **A hidden linked space remains manageable; a deleted linked space does not.**  
   Break caught: access being tied to public visibility rather than link and deletion
   semantics.
10. **Admin routes retain their current unverified/verified behavior.**  
    Break caught: replacing the admin's non-refusing loader or mounting manage guards
    too broadly.
11. **A fact write and confirmation preserve audit action names and response shape.**  
    Break caught: copying a service and drifting from the admin implementation.
12. **A link change racing a managed write is decided under the space lock.**  
    Break caught: a new middleware/service path using request-time links instead of
    `linksUnder(tx)`. Deliberately break the lock-aware path once and observe red.
13. **An owner of another space cannot mutate this space.**  
    Break caught: checking only global `OWNER` or accepting a client-supplied link.

### Review Focus

- Is `requireSpaceAccess` mounted once, before every manage router, with no module
  importing `space-links` to decide access?
- Does the middleware distinguish active links from deactivated links and deleted
  spaces, and use the settled no-hint `404`?
- Does every protected write call the existing service so `can()` and the space lock
  remain authoritative?
- Is reception read-only across every write route, including photos and confirmation?
- Is the admin still admitted only by `/admin` and `requireRole('ADMIN')`?
- Is photo limiting before file parsing and is the same service/transaction/audit path
  used by both audiences?
- Are docs honest about API-only completion, with no web or package claim?
- Are findings 17, 21, 23, 52, 59 and unavailable 75–76 left open unless directly
  resolved by evidence?

## Commits

Two atomic commits, each complete and working:

1. `feat(spaces): add managed space access and routes`  
   Authorization middleware, `space.read`, manage routers, composition-root wiring,
   API/unit tests and the directly related backend contract text.
2. `docs(spaces): document managed space API`  
   API contract, capability documentation, MVP built/planned rows and overview
   update, only if the implementation triggers those documentation changes.

If the documentation and implementation are inseparable in the final diff, use one
commit instead; never exceed 50 characters, never stage by wildcard, and include no
tool-attribution trailer or generated-with footer.

## Executor procedure

This handoff is standalone and does not depend on a Claude skill.

1. In `C:\Users\basel\masaha-b`, confirm OWNERSREAD is merged into `origin/main` and
   this worktree has no edits:

   ```powershell
   git fetch origin
   git log --oneline --decorate -5 origin/main
   git status --short --branch
   git merge-base --is-ancestor <OWNERSREAD_HEAD> origin/main
   git switch --no-track -c feat/owner-space-api origin/main
   ```

   If OWNERSREAD is not in `origin/main`, or the branch already exists, stop. Re-read
   the current files because the OWNERSREAD composition-root changes are prerequisites.
2. Check open PR heads and Worker A's named branch before editing. Ensure no open item
   owns a planned API file, shared document section or shared type. If files overlap,
   stop and ask; do not resolve a parallel-work conflict silently.
3. Add the tests first and run the focused unit/API files. Record the expected red
   failures before writing production code:

   ```powershell
   Set-Location C:\Users\basel\masaha-b
   npm run test:unit -- --run apps/api/src/shared/auth/can.unit.test.ts
   npm run test:api -w @masaha/api -- src/modules/spaces/manage.api.test.ts src/shared/auth/spaceAccess.api.test.ts
   ```

4. Implement the middleware, permission, manage routers and composition wiring.
   Preserve the existing controller/service interfaces wherever possible; add only
   the new router factories and middleware interface named in this plan.
5. Run targeted checks after each implementation commit:

   ```powershell
   npm run lint
   npm run typecheck
   npm run test:unit
   npm run test:api -w @masaha/api -- src/modules/spaces/manage.api.test.ts src/shared/auth/spaceAccess.api.test.ts
   npm run format:check
   npm run check:links
   ```

   Run one API lane at a time using the worker-B database; do not recreate the shared
   container from this worktree.
6. Review the diff, run `git diff --check`, and stage explicit paths. Commit the
   implementation and documentation atomically according to the final commit split.
   Run lint and typecheck again after each commit; do not amend.
7. Start only the API on port 3321 with the worker-B environment. Verify
   `GET http://localhost:3321/health`, then make real authenticated requests as:
   an owner (read/write), reception (read and refused write), a stranger (404), and
   the admin (use `/admin`, with `/manage` refused). Verify photo upload refusal
   happens before file processing. Stop the server and verify port 3321 is free.
8. Run the full local verification once, sequentially:

   ```powershell
   npm run lint
   npm run format:check
   npm run typecheck
   npm run test:unit
   npm run test:api
   npm run build
   npm run check:build
   npm run check:classes
   npm run check:links
   ```

   Run `npm run test:component` only if an imported shared/web type changes; no such
   change is expected. State anything not run and why.
9. Check conflicts against every relevant open PR head and `origin/main` using exact
   recorded OIDs:

   ```powershell
   gh pr list --repo Basel-Ghonaim/masaha --state open --limit 100 --json number,headRefName,headRefOid,title,author
   git merge-tree --write-tree HEAD <OPEN_PR_HEAD_OID>
   git merge-tree --write-tree HEAD <WORKER_A_HEAD_OID>
   git merge-tree --write-tree HEAD origin/main
   ```

   Record every head and clean/conflict result. Do not rebase unless GitHub reports a
   conflict or the owner directs it.
10. Push and open the PR:

   ```powershell
   git push -u origin feat/owner-space-api
   gh pr create --assignee @me --label feat --label area:api --label area:docs --body-file <MANAGE_PR_BODY>
   ```

   The PR description must include Summary, Scope/Acceptance criteria/Out of scope,
   Change type, Evidence with run/not-run commands, no screenshots, and the full
   Definition of Done checklist. It must state that no web screen or packages were
   built and that no finding is resolved without its stated evidence.
11. Wait for CI and GitHub `CLEAN`:

   ```powershell
   gh pr checks <PR_NUMBER> --watch
   ```

   Do not merge. After CI is green and the PR is clean, write
   `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\MANAGE_REPORT.md` with the head,
   commits, every run/not-run command, red tests and deliberate breaks, fixes,
   unexpected behaviour, conflict results and departures from this plan.

## Stop and ask

- OWNERSREAD is not merged into `origin/main`.
- Any planned code or documentation file overlaps another open item, especially
  Worker A's web files or a concurrent shared contract section.
- Findings 75–76 become available and require a different authorization, locking,
  schema or endpoint decision.
- The existing `AdminSpace`/shared schemas cannot represent the managed response
  without a new shared contract decision.
- A requirement would admit admin, reception writes, deleted spaces, capacity or
  packages contrary to this plan.
- A test lane cannot own a required behaviour, a failure has no identified root
  cause after three fixes, or a security/transaction property cannot be made red.
- A new dependency, migration, architectural decision or scope change is needed.

## Appendix — skill map only

This appendix maps the execution procedure to the repository's skills; no step
depends on a skill.

| Procedure step | Related skill |
|---|---|
| Start-state and base verification | `start-work-item` |
| Plan handoff and saved artifact | `write-plan` |
| API implementation/testing | no project skill; follow this plan and docs |
| Self-review, staging, commit, push and PR | `open-pr` |
| CI-gated report after `CLEAN` | `final-report` |
