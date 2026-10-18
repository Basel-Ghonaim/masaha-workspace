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
- `npm run test:unit` — 129 test files, 1,719 tests passed.
- `npm run test:api` — 47 test files, 795 tests passed.
- `npm run test:component` — 142 test files, 934 tests passed.
- `npm run lint` — passed.
- `npm run typecheck` — passed for shared, API and web.
- `npm run format:check` — passed.
- `npm run check:links` — 2,062 links in 117 documents and 1,151 source files resolved.
- `npm run build` — passed.
- `npm run check:build` — passed; no showcase, dashboard, data-table or Leaflet leakage in the first download.
- `npm run check:classes` — passed; no physical direction or arbitrary-value classes.
- Real authenticated requests on port 3321 — verified space `3` returned two owners in oldest-first order; unverified space `4` returned `owners: []`; health was up and the server was stopped by PID 24500, leaving port 3321 free.
- Conflict check — no open PRs were returned by `gh pr list`; Worker A's named branch `feat/admin-deleted-spaces` was not present on origin; `git merge-tree --write-tree HEAD origin/main` was clean.
- Deliberate verification break — removing the space `FOR SHARE` lock made the finding-43 API test fail (1 failed, 103 passed); the source was restored from a backup copy.
- A separate owner-reader-without-transaction break remained green because the existing test cannot expose that post-read race; it was restored immediately and is recorded in the execution report.

## Screenshots
None — no production web screen changed.

## Definition of Done checklist
- [x] Acceptance criteria met and scope kept.
- [x] API contract and capability documents updated.
- [x] Tests run in the owning API lane.
- [x] Authorization and share-lock behavior preserved.
- [x] Atomic history and explicit staging used.
- [x] CI passes on the pushed head and GitHub shows CLEAN.


