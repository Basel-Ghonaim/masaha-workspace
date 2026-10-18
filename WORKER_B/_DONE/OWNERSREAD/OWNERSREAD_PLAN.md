> **Approved by the owner, 2026-10-15, as written** (the analyst's check: D1's injected reader is a genuine upward need under conventions R5 and keeps the read in one locked transaction; D2's web licence touches only `routes.component.test.tsx` and `SpaceEditor.component.test.tsx`, none of worker A's files; worker A runs in parallel on the spaces list).

# Plan: include active owners in the admin's single-space read

## Contract

### Scope

Change `GET /api/v1/admin/spaces/:spaceId` so its `AdminSpace` payload includes:

```ts
owners: { id: number; name: string }[]
```

The array contains only active `OWNER` links for that space, in link creation order
(oldest first, with user id as the deterministic tie-breaker already used by the list
composition). A `RECEPTION` link, a deactivated owner link, and an owner link to no
longer-existing user are not included. An unverified space returns `owners: []`.

The owner lookup is composed above `spaces`, from `space-links`; `spaces` must not import
`space-links`. The space facts, verification state, and owners are read under the same
space share lock and transaction. All existing `AdminSpace` responses produced by create,
profile/fact saves, and confirmations also carry the field so the shared response type
does not become inconsistent after a write.

### Acceptance criteria

- `AdminSpace` in `packages/shared` has the required `owners` field.
- `GET /admin/spaces/:spaceId` returns active owners in oldest-first order and excludes
  reception and deactivated links.
- An unverified read returns an empty owners array.
- A soft-deleted or unknown space still returns the existing `not_found` response.
- Owner data and `isVerified` are read consistently under the existing `FOR SHARE` lock;
  no stale verified flag can be paired with a fresh owner list.
- Existing authorization behavior remains unchanged.
- API integration tests prove the payload, ordering/filtering, empty case, and lock-consistent
  read; the tests are seen failing before the implementation.
- The API contract and the affected capability documentation describe the new read.
- Only the two web fixtures that are required by the now-required shared field are updated;
  no web screen or owner dialog is built in this Work Item.

### Out of scope

- Worker A's verified-space editor notice, owner names, or unlink dialog.
- A new `/admin/spaces/:spaceId/owners` endpoint.
- Changes to owner-link mutation behavior, roles, authorization, schema, migrations, or
  database indexes.
- Any reception/staff feature.
- Marking finding 59 resolved: this API slice alone does not satisfy its web resolution.

## Stronger decisions

### D1 — compose through an injected owner reader, not an L1 import

Use the existing `space-links` admin-space composition to expose a set-based
`ownersFor(spaceId, tx?)` reader. Inject that callback into the `spaces` space-view/read
path from the composition root. The callback returns `{ id, name }[]` and uses
`findOwnerLinks` plus `users.namesFor`, preserving repository order while mapping names.
Build a `Map` from the returned user names and use `flatMap` (not a fallback string) so
an owner link whose user lookup has no matching row is omitted from the response.

Reason: `spaces` is L1 and must never import the L2 `space-links`; the composition root is
the existing dependency-injection boundary and keeps the endpoint on its current
`spaces` route/controller. This is safer than adding a second owners endpoint or moving the
whole space read into an L2 route, and it preserves one implementation of the existing
locked space read.

### D2 — owners is a required `AdminSpace` field

Add `owners` to `AdminSpace`, rather than introducing a second read. The web already imports
`AdminSpace`, and the editor's eventual owner notice needs the same response that supplies
the space facts.

Narrow licence for the parallel web layer: update only these fixtures that construct a full
`AdminSpace` object:

- `apps/web/src/pages/dashboard/routes.component.test.tsx`
- `apps/web/src/features/spaces/components/editor/SpaceEditor.component.test.tsx`

Partial picks, casts, repositories, and behavior are not changed. The field is populated on
all API `AdminSpace` responses, so no consumer receives a shape that silently loses owners
after a mutation.

### D3 — preserve the existing share-lock consistency guarantee

The owner reader is called inside the same transaction after `space.repository.lockShared`
and the links are read with `linksUnder(tx)`. The owner lookup receives the same `tx`.

Reason: the existing finding-43 guarantee says a read cannot combine facts and links from
different committed states. Reading owners after the transaction would allow a link commit
between the verified calculation and the owner query.

### D4 — keep finding 59 open

Do not change finding 59's status in this API-only Work Item. Its evidence and resolution
include the web notice and unlink dialog, which Worker A owns. Record in the PR that the API
portion is supplied while the finding remains Open until the web slice lands.

## Related findings

- **59 — The verified space's editor cannot name its owner:** fold the API portion into this
  Work Item by adding owners to the single-space response; leave the finding Open because the
  web resolution is explicitly out of scope.
- **71–72:** the prompt identifies these as new related findings, but no corresponding files
  or titles are present in this checkout. Do not invent resolutions or edit the index. During
  execution, inspect the owner's supplied descriptions if available; stop and ask only if
  either finding changes the endpoint contract, locking rule, or file ownership stated here.

## Files and interfaces

### Shared contract

- `packages/shared/src/spaces/responses.ts`
  - Add required `AdminSpace.owners: { id: number; name: string }[]`, documented as active
    owner links in oldest-first order.

### API composition and read

- `apps/api/src/modules/space-links/admin-spaces/adminSpaces.service.ts`
  - Add `ownersFor(spaceId: number, tx?: Tx): Promise<{ id: number; name: string }[]>`.
  - Read active owner links for one space, fetch all names in one `users.namesFor` call,
    map by user id, preserve the repository's oldest-first order, and omit any link whose
    user id is absent from the name map; never return `{ id, name: '' }`.
  - Reuse `createSpaceLinksRepository.findOwnerLinks`; do not query Prisma from the service.

- `apps/api/src/modules/spaces/space/space.service.ts`
  - Add an injected owner-reader dependency:
    `ownersFor(spaceId: number, tx?: Tx) => Promise<AdminSpace['owners']>`.
  - In `get`, call it with the transaction after the share-locked space and links are read.
  - In `create`, supply the empty result for the new unverified space (or call the reader
    after the transaction if the implementation keeps the view path uniform).

- `apps/api/src/modules/spaces/space/spaceView.ts`
  - Accept owners as view input and pass them to the mapper.

- `apps/api/src/modules/spaces/space/space.mapper.ts`
  - Map the supplied owners without recomputing or sorting them.

- `apps/api/src/modules/spaces/facts/groupEdit.ts`
  - Carry the same injected owner reader in `GroupEditDependencies`.
  - Read owners with the current transaction for both changed and unchanged group answers.

- `apps/api/src/app.ts`
  - Construct the admin-spaces composition before the space service/fact dependencies need
    its owner reader, or otherwise retain equivalent dependency ordering.
  - Pass `adminSpaces.ownersFor` to `createSpaceService` and the shared `facts` dependency
    object used by profile, hours, prices, amenities, contacts, and confirm.
  - Do not introduce a direct `space-links` import into any `spaces` module.

- `apps/api/src/modules/spaces/space/space.api.test.ts`
  - Extend the single-space read tests with owners, ordering/filtering, empty unverified
    behavior, and the existing lock-consistency scenario.

- `apps/api/src/modules/space-links/admin-spaces/adminSpaces.mapper.unit.test.ts`
  - No behavior change is expected; update only if a shared type or helper signature makes
    a focused mapper fixture require the field. Do not add duplicate proof here unless the
    mapper changes.

### API contract and capability documentation

- `docs/api/api-contract.md`
  - Add `owners` to the authoritative `AdminSpace` shape and state active/oldest-first
    semantics for `GET /admin/spaces/:spaceId`.

- `docs/features/spaces.md`
  - Update the API read description/code map decision text to link the owners composition
    to `space-links`; do not describe the future web owner notice as built.

- `docs/features/space-links.md`
  - Record that its admin composition supplies active owner names to the single-space admin
    read, while its existing list composition remains unchanged.

### Narrow parallel web licence

- `apps/web/src/pages/dashboard/routes.component.test.tsx`
  - Add `owners: []` to the `ADDED` `AdminSpace` fixture.

- `apps/web/src/features/spaces/components/editor/SpaceEditor.component.test.tsx`
  - Add `owners: []` to the `SPACE` `AdminSpace` fixture.

No web production file is in scope.

## Tests

All new API tests are `*.api.test.ts` and belong to the API integration lane with the real
PostgreSQL database. New tests must be written and run red before the production change.

1. **`GET /admin/spaces/:spaceId` returns active owner names oldest first.**
   - Arrange two active owners with deliberately ordered `createdAt` values, plus an active
     reception link and a deactivated owner link.
   - Break caught: an implementation that includes every link, filters by the wrong role,
     loses link order, or returns user-query order rather than link order.
   - Expected payload includes only the two owner `{ id, name }` objects in oldest-first order.

2. **An unverified space returns `owners: []`.**
   - Read a space with no active owner link, then add only reception/deactivated links as the
     filtering case.
   - Break caught: an implementation that treats any manager as an owner or emits `null`/
     omitted owners for unverified spaces.

3. **The owner reader omits links with no matching user name.**
   - Exercise the owner-to-name mapping through its pure helper if one is extracted, with one
       owner link omitted from the supplied names; otherwise use the service seam already
       available to the API test harness.
   - Break caught: using `nameById.get(userId) ?? ''`, which exposes a fabricated empty-name
       owner instead of filtering the link out.

4. **All `AdminSpace` write responses retain owners.**
   - Extend the existing endpoint matrix or one focused case so a verified space's profile/fact
     response still includes its active owners after a write/confirm.
   - Break caught: injecting owners only into `GET`, which would make the shared response shape
     inconsistent and make a later editor mutation erase owner data in client state.

5. **The read's owners and verification state remain lock-consistent (finding 43).**
   - Extend the existing lock test in `space.api.test.ts` so the transaction that holds the
     space lock writes the owner link before the GET can proceed, and assert both
     `isVerified: true` and the matching owner name in the returned payload.
   - If the test setup can deterministically expose a post-read owner query, add that case:
     hold/read the share-locked transaction, attempt a blocked owner-link change, and assert
     the response cannot show a stale verification flag beside fresh owners.
   - Break caught: moving the owner query outside the read transaction or using the default
     Prisma client instead of the supplied `tx`. This is a transaction/ordering property, so
     deliberately break the lock/transaction path once, observe red, then restore it before
     commit (testing §3 rule 7).

6. **Existing authorization and not-found matrix stays green.**
   - The current `space.api.test.ts` matrix remains the proof for guest, USER, another-space
     owner, this-space owner, pending-password admin, soft-deleted, and unknown cases.
   - Break caught: moving the route or composition in a way that bypasses admin guards or
     changes visibility semantics.

Unit tests are not required for the owner reader because its behavior depends on real repository,
user, transaction, and ordering data; the API lane owns it under testing §1. If a pure mapping
helper is extracted, test only that pure helper in a unit file and do not duplicate endpoint proof.

## Review Focus

- Does any `spaces` module import `space-links` or read `space_managers` directly?
- Does every `AdminSpace` response, not only GET, include owners?
- Is the owner query passed the active transaction and executed after the share lock?
- Are active OWNER links ordered by link creation, with a deterministic tie-breaker?
- Are deactivated owners, reception links, and missing names excluded rather than represented by
  empty-name placeholders?
- Did the web licence remain limited to the two fixtures, with no overlap with Worker A's
  production files?
- Are findings 59 and 71–72 left honest, with no claim that the web resolution is complete?

## Commits

One atomic commit, because the shared contract, composition, API implementation, tests, docs, and
the two licensed fixtures form one complete response-shape change:

1. `feat(spaces): include owners in admin space reads`

Stage paths explicitly; never use `git add -A` or `git add .`. No tool-attribution trailer or
generated-with footer is permitted.

## Executor procedure

This plan is standalone; no step depends on a Claude skill.

1. Confirm the worker folder is still detached at the expected `origin/main`, the worktree has
   no conflicting edits, and Worker A is not editing either licensed web fixture:

   ```powershell
   git status --short --branch
   git log -1 --oneline
   git switch --no-track -c feat/space-owners-read origin/main
   ```

   If the branch already exists, stop rather than deleting or reusing it silently. Re-read this
   plan and the current files before editing if the base moved.

2. Ensure Worker A's open files do not overlap the file map. If the shared API contract or a
   capability document is concurrently edited, use the documented fast path and keep changes in
   separate sections.

3. Write the API test cases first. The API package script is `vitest run --project api`, so
   from the API package directory run only this file, using its workspace-relative path and no
   Jest-only `--runInBand` option. Record the expected red failure before implementing:

   ```powershell
   Set-Location C:\Users\basel\masaha-b\apps\api
   npm run test:api -- src/modules/spaces/space/space.api.test.ts
   ```

   The equivalent root invocation is
   `npm run test:api -w @masaha/api -- src/modules/spaces/space/space.api.test.ts`.
   Do not weaken assertions to obtain green.

4. Implement the injected reader, shared field, mapper/view propagation, composition-root
   wiring, and the two fixture updates. Update the contract and capability documents in the
   same commit. Keep all database access in existing repositories and use the supplied `tx`.

5. Run checks after the implementation and before staging:

   ```powershell
   npm run lint
   npm run typecheck
   npm run test:unit
   npm run test:api -w @masaha/api -- src/modules/spaces/space/space.api.test.ts
   npm run format:check
   npm run check:links
   ```

   API tests use `masaha_b_test`. Do not run a second API lane concurrently; do not run
   `npm run db:up` from this worktree. If PostgreSQL is stopped, start the already-created
   shared container as setup requires, without recreating it.

6. Review the diff and stage only the paths in this plan:

   ```powershell
   git diff --check
   git status --short
   git add packages/shared/src/spaces/responses.ts `
     apps/api/src/modules/space-links/admin-spaces/adminSpaces.service.ts `
     apps/api/src/modules/spaces/space/space.service.ts `
     apps/api/src/modules/spaces/space/spaceView.ts `
     apps/api/src/modules/spaces/space/space.mapper.ts `
     apps/api/src/modules/spaces/facts/groupEdit.ts `
     apps/api/src/app.ts `
     apps/api/src/modules/spaces/space/space.api.test.ts `
     docs/api/api-contract.md docs/features/spaces.md docs/features/space-links.md `
     apps/web/src/pages/dashboard/routes.component.test.tsx `
     apps/web/src/features/spaces/components/editor/SpaceEditor.component.test.tsx
   git diff --cached --check
   git commit -m "feat(spaces): include owners in admin space reads"
   ```

7. Re-run `git status --short`, `npm run lint`, `npm run typecheck`, and the relevant API test
   after the commit. Do not amend the commit. If a failure is caused by this change, fix the
   root cause in a new fixup workflow and fold it before push; do not leave a red commit.

8. Prepare the worker-B local environment for port 3321 using its existing
   `apps/api/.env` and `masaha_b_dev`. Start only the API:

   ```powershell
   npm run dev -w @masaha/api
   ```

   Verify it is responsive before using it:

   ```powershell
   Invoke-RestMethod http://localhost:3321/health
   ```

   Make real authenticated requests against 3321 using the seeded worker-B admin account:
   create or identify one unverified space and one space with two active owners, then call
   `GET /api/v1/admin/spaces/:spaceId`. Verify the JSON contains `owners: []` for the
   unverified space and the expected oldest-first `{id,name}` list for the verified space.
   Stop the server and verify port 3321 is free afterward. Do not use production credentials or
   external services.

9. Run the full local verification once, one lane at a time, before pushing:

   ```powershell
   npm run lint
   npm run format:check
   npm run typecheck
   npm run test:unit
   npm run test:component
   npm run test:api
   npm run build
   npm run check:build
   npm run check:classes
   npm run check:links
   ```

   The report must name anything not run and why. Manual visual review is not needed because no
   production web screen changes.

10. Before pushing, compare the proposed branch head with every relevant open PR head, not
    only `origin/main`. The check is read-only after the heads have been identified. From the
    repository root, enumerate the current open PR heads and record the result:

    ```powershell
    Set-Location C:\Users\basel\masaha-b
    gh pr list --repo Basel-Ghonaim/masaha --state open --limit 100 `
      --json number,headRefName,headRefOid,title,author
    git branch -r --no-color
    ```

    The required heads to check are:

    - every `headRefOid` returned by `gh pr list` for an open PR whose files can overlap this
      Work Item, especially Worker A's PR/head when its `headRefName` or author identifies it;
    - Worker A's remote branch even if it has no PR, when the owner has named that branch:
      resolve it read-only with
      `git ls-remote --heads origin <WORKER_A_BRANCH>` and use the returned commit id;
    - `origin/main` as the base sanity check, although it is not a substitute for the open
      PR/Worker A comparisons.

    For each recorded commit id, run the exact three-way-tree check separately:

    ```powershell
    git merge-tree --write-tree HEAD <OPEN_PR_HEAD_OID>
    git merge-tree --write-tree HEAD <WORKER_A_HEAD_OID>
    git merge-tree --write-tree HEAD origin/main
    ```

    Substitute only the actual OIDs that were recorded; do not pass a branch name that may
    move during the check. If no open PRs exist, record `gh pr list` as empty, still check
    Worker A's named branch if one exists, and check `origin/main`. The report must list every
    PR number/title/head OID checked, Worker A's branch/OID (or that no such branch was
    supplied or found), each command's clean/conflict result, and any file overlap. Do not
    merge or rebase unless the owner directs it or GitHub reports a conflict.

11. Write the exact PR description below to the concrete session artifact
    `C:\Users\basel\.prompt\MASAHA_WORKER_B\files\OWNERSREAD_PR_BODY.md`, then push and open
    the PR with its title, labels, assignee, and body file:

    ```powershell
    Set-Location C:\Users\basel\masaha-b
    git push -u origin feat/space-owners-read
    gh pr create `
      --title "feat(spaces): include owners in admin space reads" `
      --assignee @me `
      --label feat `
      --label area:api `
      --label area:docs `
      --body-file "C:\Users\basel\.prompt\MASAHA_WORKER_B\files\OWNERSREAD_PR_BODY.md"
    ```

    Use this description verbatim in that body file, filling in command results only where
    marked:

    ```markdown
    ## Summary
    Add active owner names to `AdminSpace` and `GET /admin/spaces/:spaceId`, composed from
    `space-links` under the existing space share lock.

    ## Scope / Acceptance criteria / Out of scope
    - `AdminSpace.owners` is required, active OWNER links only, oldest first.
    - Unverified spaces return an empty owners array.
    - All AdminSpace responses retain the field.
    - API tests prove filtering, ordering, empty state, authorization, not-found behavior and
      lock-consistent verification/owners.
    - Out of scope: the web owner notice and unlink dialog; finding 59 remains Open.

    ## Change type
    Feature — API/shared contract and documentation.

    ## Evidence — what was run
    List the passing lint, format, typecheck, unit, component, API, build, check:build,
    check:classes, check:links, real 3321 request, and conflict-check commands. State anything
    not run.

    ## Screenshots
    None — no production web screen changed.

    ## Definition of Done checklist
    - [x] Acceptance criteria met and scope kept.
    - [x] API contract and capability documents updated.
    - [x] Tests run in the owning API lane.
    - [x] Authorization and share-lock behavior preserved.
    - [x] Atomic history and explicit staging used.
    - [ ] CI passes on the pushed head and GitHub shows CLEAN.
    ```

12. Wait for CI, then run:

    ```powershell
    gh pr checks <PR_NUMBER> --watch
    ```

    Proceed only when all required checks pass and GitHub reports `CLEAN`. No merge is performed.

13. After CI and `CLEAN`, write the report to
    `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\OWNERSREAD_REPORT.md`, including the head,
    commit, every command run/not run, the red tests and breaks made, problems and fixes,
    unexpected behavior, the conflict result, and any departure from this plan. Do not claim
    finding 59 is resolved.

## Stop and ask

- Worker A's production changes overlap any API/shared file in this plan, or either licensed web
  fixture is being changed for another reason.
- The actual 71–72 finding descriptions require a different endpoint, a schema change, or a
  locking/ownership decision not settled by this plan.
- A required API response cannot carry owners without changing a public contract beyond the
  owner's settled D2 decision.
- The owner reader would require `spaces` to import `space-links`, a new dependency, a migration,
  or a new authorization rule.
- No existing test lane can deterministically prove the lock-consistency requirement.
- A test or build failure remains unexplained after three root-cause fixes.
- GitHub reports a conflict or CI failure in unrelated code; do not silently rebase or repair it.

## Appendix: Claude skill map (map only)

No step depends on a Claude skill. If the executor is Claude, the project skills correspond as
follows:

- Start/worktree and bootstrap reading: `start-work-item`.
- Plan persistence: `write-plan`.
- Test-first execution and proving deliberate transaction breaks: the workflow's testing rules
  and optional `test-driven-development`.
- Root-cause diagnosis of failures: optional `systematic-debugging`.
- Verification claims: optional `verification-before-completion`.
- PR opening and later review rounds: `open-pr`.
- Post-CI report: `final-report`.
