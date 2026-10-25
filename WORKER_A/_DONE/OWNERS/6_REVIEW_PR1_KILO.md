# Review — PR #88 (`feat/admin-owners`), independent review

## Head

`e4e13e9eed93d0223c791388d9d38ebb40916ecd`, fetched as local ref `pr88` from `refs/pull/88/head`; base `5e8c979d` (= `origin/main`). Three commits: `ef57ac7c fix(spaces): title the gallery's failed writes`, `b8e47338 refactor(space-links): share the list's paging`, `e4e13e9e feat(space-links): add the admin's owners page`. Scope is `apps/web` and `docs` only — no `apps/api`, no `packages/shared`, no dependency changes, matching plan §7.

## Verdict

Pass — no blockers. PR 1 matches plan §7, §9 and §10, and CI on the head `e4e13e9e` is green in every lane with `mergeStateStatus CLEAN` (read in the executor's report `4_REPORT_PR1.md`; per the review rules I ran no lanes, builds or tests myself). Four nits below, all "a finding to record", none blocking PR 1 or deferring PR 2.

## Findings (most severe first)

**1. Nit — test budget, a finding to record.**

The route test `routes.component.test.tsx › lists the owner's eleven pages` (an owner's shell) cold-loads in ~2.4–2.5 s against the 3 s `asyncUtilTimeout` (`src/test/componentSetup.ts:10`); main is ~2.3 s, and the lane failed twice locally under load. CI's component lane passed (5 m 47 s).

Cause, confirmed in code: `apps/web/src/pages/dashboard/shell/SpaceLayout.tsx:1` imports `SpaceSwitcher` from `@features/space-links`, and the index (`apps/web/src/features/space-links/index.ts:2`, commit `e4e13e9e`) now also exports `OwnersList`, pulling in `hooks/users-list/`, `hooks/owners-list/useOwnersList.ts`, `services/usersFiltersOf.ts` and `services/userRowView.ts`. So the owners-list module graph loads in the owner's dashboard shell too, not only the admin's.

Not a behaviour defect: nothing admin-only reaches the site's first download (`check:build` passed, read in the report) and the boundary stays dashboard-only (O2; space-links imports only `@shared/*`, `@masaha/shared/*`, react-router, TanStack Query — no cross-feature import). The cost is test budget consumed on the owner shell. Fix belongs: a finding to record; no PR-1 fix, and worth watching if PR 2/PR 3 grow the space-links index further. The timings and CI result are read in the executor's report (`4_REPORT_PR1.md` §On the head); I verified only the import graph in code.

**2. Nit — departure 5, a finding to record.**

`apps/web/src/features/space-links/services/userRowView.ts:23` signs `userRowView(row, { lines, english })`; plan §9 commit 3 wrote `(row, { english })`.

The catalogue words are genuinely needed for the state labels (`lines.states.active` → `success`, `lines.states.suspended` → `neutral`), so the plan's signature was imprecise and the code is correct; no behavioural effect and no test breaks. Fix belongs: a finding to record (plan text, not code). Verified in code.

**3. Nit — departure 2, a finding to record.**

The axe test on `OwnersList.component.test.tsx`: the planned break (a chip group with no name) still passes axe — vitest-axe does not require a radiogroup to be named. The name is proven by the sibling test "filters by state from the chips" (`getByRole('radiogroup', { name: 'Status' })`), and the axe test itself was seen red by the finding-50 link without accessible text.

Fix belongs: a finding to record; the substitute is acceptable, no change. The red break outputs are read in the executor's report (`4_REPORT_PR1.md` §Commit 3); I ran no tests.

**4. Nit — departure 4, a finding to record.**

`apps/web/src/features/space-links/types/OwnersListView.ts` was added although plan §7's commit-3 list does not name it. It is a one-line `ReturnType<typeof useOwnersList>` alias used by `OwnersToolbar`; harmless. Fix belongs: a finding to record.

Documented departures with no code effect (read in the report only, not re-verified): the real run used a headless-CDP script instead of the playwright MCP tools/Chrome extension (departure 1), and the local component lane stays red on one untouched timing test with CI as the verdict (departure 3).

## Checked and fine

- Commit 1 (`ef57ac7c`): `usePhotoGallery.ts` titles refusals by action — `words.orderFailed` for the move, `words.removeFailed` for removal; both new lines added to `shared/copy/english/spaces.ts` and `shared/copy/arabic/spaces.ts`; `sendMultipart.onProgress: UploadProgress` required (`sendMultipart.ts:14`), `sendMultipart` always sets `onUploadProgress` (`sendMultipart.ts:45`), `SpacesRepository.uploadPhoto(spaceId, file, onProgress, signal?)` passes it straight (`spacesRepository.ts:42-49`); every caller passes it — `usePhotoUploads.tsx:107`, `spacesRepository.ts`, the unit tests; the "no callback" test deleted; one history line in `docs/features/spaces.md`.
- Commit 2 (`b8e47338`): old → new line by line, no behaviour change — `AdminSpacesPagination` → `ListPagination` (same `PaginationView` shape), `AdminSpacesState` → `ListState`, focus keeper / page-in-range / paused search extracted unchanged into `useFocusKeeper.ts`, `usePageInRange.ts`, `usePausedSearch.ts`, and the pagination block into `services/paginationView.ts`; `useAdminSpacesList` at head computes status and pagination identically to before; `git grep` at head shows no importer of the old paths; the spaces-list tests are untouched.
- Commit 3 (`e4e13e9e`): `useOwnersList.ts:47` fixes `role: 'owner'` on `GET /admin/users`; `?q=&state=&page=` kept in the address (`useUsersFilters.ts`), state choice `replace`s the address (Back leaves the page), defaults left out, invalid values dropped by `adminUsersQuerySchema` (`usersFiltersOf.ts`); empty / no-match / error / 429-blocked-with-retry states; focus keeper on the list; finding-50 line exactly when `row.role === 'OWNER' && row.spaces.length === 0` (`userRowView.ts:34`), the whole line a link to `deletedSpacesLink` = `/dashboard/admin/spaces?status=deleted` (`OwnerSpaces.tsx:18-28`); email under the name until 1024 px (`lg:hidden`), its own column from 1024 (`hidden lg:table-cell`, `dir="ltr"`); cards at 390 px; `dir="auto"` on names, `lang="en" dir="ltr"` on English-only names; `ToggleGroup` named "Status" (`OwnersToolbar.tsx:53`); both copy catalogues complete (`arabic/english/spaceLinks.ts`, `ownersList`); dashboard-only (`check:build` passed — read in the report); docs true to the code (glossary Owner row appended, findings/50 dated line, `space-links.md` behaviour/decisions, `architecture.md` §2, `overview.md`, `spaces.md` history line); commit subjects 46 characters each (≤ 50), bodies say why.
- Tests: every planned break seen red in its own lane (red outputs listed in `4_REPORT_PR1.md` §Commit 3); CI green on all lanes, CLEAN on `e4e13e9e` (read in the report).

## Head check

`e4e13e9e` still resolves; `git fetch` added only the `pr88` ref, nothing moved; working tree untouched (detached at `93f152fe`).
