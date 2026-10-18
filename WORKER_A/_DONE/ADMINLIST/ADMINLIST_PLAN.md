> **Approved by the owner, 2026-10-15, with one change (the analyst's check):** workflow §3 puts a unit's documents in the **same** commit as its code, never a separate docs commit. Fold commit 3 (`docs(admin): document deleted space restore`) into the two code commits — each commit carries the document lines it makes true — so the item has **two** commits. Everything else as written.

# ADMINLIST — implementation plan

## 1. Summary

Update the admin dashboard spaces list to implement the already-built API contract and approved
admin design for deleted spaces. The list will expose `deleted` as a fourth address-backed status,
show verification and hidden state as separate facts, render deleted rows muted with their Gaza-local
deletion date and owners, and give deleted rows only a restore action. The stale-data control will
be a `ToggleGroup` chip by the result count, and missing groups will use the `warning` badge.

The implementation remains web-only. The API and `packages/shared` already provide the required
query status, row facts, `deletedAt`, owners, and restore endpoint.

## 2. Contract

### Scope

- `apps/web/src/features/space-links`: address parsing, request/query wiring, row view, desktop table,
  phone cards, toolbar, copy, and component/unit tests.
- `apps/web/src/features/spaces`: pass deleted-row facts into the action seam and make
  `SpaceActionsMenu` render the restore-only action for deleted rows; reuse the existing
  `useRestoreSpace` mutation, hold handling, refresh, and named success/failure toasts.
- Directly related dashboard composition tests and fixtures, if the changed action interface requires
  them.
- Capability documentation and the findings/overview records listed in §7.

### Acceptance criteria

1. `?status=deleted` is accepted, sent to `GET /admin/spaces`, and survives page/filter links.
   Invalid or absent status still falls back to the live-list default.
2. The status filter offers **All plus the four statuses**: verified, unverified, hidden, and
   deleted.
3. Live rows show a verification badge (`موثّقة`/`Verified` or `غير موثّقة`/`Unverified`) always,
   plus `مخفية`/`Hidden` when `isHidden`; hidden no longer replaces verification.
4. Deleted rows are included only for `status=deleted`, are muted, show `محذوفة`/`Deleted` and
   `حُذفت في …`/`Deleted on …` using the existing `Asia/Gaza`, Western-digit, Gregorian list-date
   rule, name their owners, and retain the same search/place/stale/page behavior.
5. A deleted row's only action is `استرجاع`/`Restore`; it has no edit, hide/show, delete, or
   owner action. Restore is pending on that row, observes the shared 429 hold, refreshes the admin
   scope, and then shows a named success toast. Failures show a named failure toast and request
   reference through the existing error presentation.
6. Desktop and phone render the same facts and restore-only action.
7. The stale-only control is a `ToggleGroup` chip beside the result count, not a switch field.
   Its meaning remains stale-or-missing as the API contract defines it.
8. Missing freshness badges use `warning`; stale badges remain `warning`; up-to-date remains
   `success`.
9. The implementation contains no hardcoded user-facing strings and keeps Arabic/English catalogue
   parity.
10. Findings 44 and 50 are resolved in the owning records, the capability document removes the
    obsolete web-status exception and records the new web behavior, and the overview Built line
    truthfully includes the restored deleted-space screen behavior.

### Out of scope

- Any change under `apps/api` or `packages/shared`; if the web cannot satisfy the contract with the
  existing API/shared shapes, stop and escalate rather than widening scope.
- API behavior, authorization, migrations, database work, or new error codes.
- New design-system components, tokens, dependencies, routes, or architectural decisions.
- Owner-link UI, the users/owners pages, or changing the established unlink path. The repository has
  no web unlink UI: this item resolves finding 50 only under the finding's explicit third option,
  which the prompt says the owner accepted—document the existing restore → unlink → delete path
  where the admin will find it. It must not claim that this PR adds an unlink screen or makes the
  API's deleted-space unlink endpoint work; the underlying API behavior remains unchanged.
- Changing the existing delete Undo flow except where the shared restore action interface must
  accommodate deleted rows.
- E2E automation; the required real browser run is manual evidence for this screen.

## 3. Reading done

Read in the required order and used as authoritative sources:

- `CLAUDE.md`
- `docs/development/workflow.md`
- `docs/README.md`
- `docs/architecture/findings/README.md`, plus findings 44 and 50
- `docs/features/space-links.md` (whole)
- `docs/features/spaces.md` (whole/relevant web row-action sections)
- `docs/api/api-contract.md` (admin spaces and restore contract)
- `docs/frontend/architecture.md` (capability boundaries, state, query keys)
- `docs/frontend/design-system/foundation.md` (badges, ToggleGroup, responsive/data rules)
- `docs/frontend/localisation.md` (catalogues and Gaza date formatting)
- `docs/development/testing.md`
- `C:\Users\basel\.prompt\MASAHA_DESIGN\DECISIONS_ADMIN.md`
- `docs/design/INDEX.md`
- `docs/design/prototype/Admin spaces.html`
- `docs/project/overview.md`
- GitHub issues `Basel-Ghonaim/masaha#69` and `Basel-Ghonaim/masaha#70`, because the prompt names
  them as new findings to account for; both are already closed and their fixes are verified in the
  current tree.
- Current implementation and tests in `features/space-links`, `features/spaces`, the dashboard
  spaces page, shared response/request types, repositories, and both copy catalogues.

The API contract confirms:

- `GET /admin/spaces?status=deleted` returns deleted rows only, with owners and `deletedAt`.
- `POST /admin/spaces/:spaceId/restore` is idempotent for a non-deleted space and restores its
  prior hidden/owner-link state.
- `AdminSpaceRow` already includes `isVerified`, `isHidden`, `deletedAt`, owners, freshness, and
  `lastUpdatedAt`.

## 4. Settled decisions to build

- **D1 — web only:** do not touch API or shared contract code because the endpoint and payload are
  already present.
- **A3:** state is two facts. A live row always shows verification; hidden is an additional badge.
  Deleted is a separate filter/list state, not a replacement state badge.
- **Deleted list:** `deleted` is the fourth status filter and is sent to the server. Deleted rows
  are excluded from every other status, retain search/place/stale/pagination, show owners and
  deletion date, and are muted.
- **D2:** restore uses the existing mutation pattern: row-level pending state, global 429 hold,
  refresh of the admin scope, success toast naming the space, and failure toast naming the space.
  The existing API error/reference presentation remains the source of refusal details.
- **D3:** deleted rows offer only restore. No edit, hide/show, delete, or owner actions are exposed.
- **D4:** phone cards show the same facts and the same one action as desktop rows.
- **A7:** stale data becomes a `ToggleGroup` chip next to the result count. It continues to filter
  stale or missing groups.
- **A8:** missing freshness is `warning`, not `neutral`.
- **Date rule:** use the existing `updatedOn` convention (`Asia/Gaza`, `ar-u-nu-latn`/`en-GB`,
  Gregorian calendar, year only when different) for the deleted date.
- **State location:** address filters/page remain in `useAdminSpacesFilters`; server state remains
  in TanStack Query under the existing admin space-links key; restore remains a spaces mutation
  that invalidates the admin scope through `useRefreshAdmin`.
- **Finding 50 resolution boundary:** because no web unlink UI exists, the PR documents rather than
  implements unlinking. The finding can be marked resolved only as the owner-accepted documented
  way out specified in its own “Resolves when” line; the resolution must explicitly say this is
  documentation/screen guidance, not a new unlink capability.

### User-facing strings and catalogue keys

Add or adjust both catalogues under `spaceLinks.adminList`:

| Key | Arabic | English |
|---|---|---|
| `states.deleted` | `محذوفة` | `Deleted` |
| `deletedOn` | `حُذفت في {date}` | `Deleted on {date}` |
| `restore` | `استرجاع` | `Restore` |
| `restoreNamed` | `استرجاع {name}` | `Restore {name}` |
| `verification`/state rendering | `موثّقة` / `غير موثّقة` | `Verified` / `Unverified` |
| `hidden` state rendering | `مخفية` | `Hidden` |
| stale chip | `بيانات قديمة أو ناقصة` | `Stale or missing` |

Reuse existing `spaces.toasts.restored` and `spaces.failures.restore` for mutation feedback; do
not duplicate those lines in `spaceLinks`.

The exact catalogue shape and naming may follow the current catalogue organization if a more
specific existing line is found during implementation, but every new visible or assistive line
must have the same typed key and parameters in Arabic and English.

### Interfaces

- `LIST_STATUSES` changes from `verified | unverified | hidden` to all four contract statuses;
  `ListStatus` therefore includes `deleted`.
- `AdminSpaceRowView` will expose separate verification/hidden/deleted presentation data rather than
  one collapsed `state`, for example `state: BadgeView[]`, `deletedOn: string | null`, and the
  existing row/name/owner/freshness fields. The executor should preserve the smallest clear shape
  and update all consumers together.
- `SpaceRef` will include `deletedAt` (and any name field already needed) so the menu can decide
  whether its only action is restore.
- `useSpaceActionsMenu` will return either the normal live action set or a deleted-row restore
  action with `pending`, `run`, and the existing named feedback behavior. `SpaceActionsMenu` will
  render the corresponding branch and keep the trigger accessible/focusable.
- `AdminSpacesList` continues receiving `actions`, `placeField`, and `spaceLink` from the page; it
  remains agnostic about the spaces capability's action implementation.

## 5. Stronger decisions

No new architecture or ADR decision is required. The following implementation choices strengthen
existing rules without changing product behavior:

1. **Represent state facts as an array of `BadgeView`s at the row-view seam.**
   - Why: prevents the desktop table and phone card from independently re-deriving A3 and makes
     “verification always, hidden additionally” one decision.
   - Cost: changes the current `state` consumer and its focused unit/component expectations.
   - Recommendation: do it; it is smaller and safer than duplicating conditional rendering.
2. **Keep deletion-date formatting beside the existing list date formatter.**
   - Why: it guarantees the deleted row and last-update date use one Gaza/date rule without creating
     a generic formatter prematurely.
   - Cost: one focused helper/test adjustment.
   - Recommendation: do it; the capability document already owns this list-specific rule.
3. **Reuse `useRestoreSpace` for both Undo and deleted-list restore.**
   - Why: it already owns the endpoint, admin refresh, hold recording, success/failure copy, and
     mutation lifetime after a row disappears.
   - Cost: its comments/types must be generalized from “just deleted” to “deleted row or Undo”.
   - Recommendation: do it; a second restore mutation would risk divergent feedback.
4. **Use row-level conditional composition rather than making the list know action labels.**
   - Why: the `spaces` feature owns space life/actions and the page already fills the list slot.
   - Cost: `SpaceRef` and menu tests change.
   - Recommendation: do it; it preserves the no-sibling-import boundary.

No document rule is contradicted or weakened. In particular, server authorization remains the
authority, no physical direction classes or raw colors are added, and all query state stays in the
address/TanStack Query locations already defined.

## 6. Related findings

- **Finding 44 — folded and resolved.** The deleted status screen lists deleted spaces and the
  restore action remains available after the Undo toast disappears. Cost: deleted-row presentation,
  restore-only action, component tests, and status/document updates.
- **Finding 50 — folded and resolved for the screen portion.** A deleted row names its owners and
  offers restore, while the capability documentation explicitly states the existing way back to a
  `USER`: restore → unlink → delete again. The repository has no web unlink UI, so this is resolved
  only by the owner-accepted documentation alternative in finding 50; the PR must not imply that
  unlinking a deleted space is now available on the web. The API's link behavior is unchanged.
  Cost: update the finding's evidence/resolution, index, and feature/overview wording; no backend
  or unlink-screen work.
- **Findings/issues 69 and 70 — not folded; already closed and verified, with no required changes
  for this item.**
  - `Basel-Ghonaim/masaha#69` is API-contract documentation about distinguishing
    `invalid_format` from `out_of_range` for non-integer price amounts. Its required files when
    addressed are `docs/api/api-contract.md` (and, only if the contract/API implementation were
    changed, the corresponding API/shared files and tests). This item is web-only, does not touch
    that endpoint or contract, and must not edit those files.
  - `Basel-Ghonaim/masaha#70` is a dashboard-shell safeguard against an empty `PageHeader` heading.
    Its required files when addressed are `apps/web/src/pages/dashboard/shell/PageHeader.tsx` and
    `apps/web/src/pages/dashboard/shell/PageHeader.component.test.tsx`; the current code and test
    already contain the wordmark fallback and its proof. This item does not change the shell, so
    those files remain out of scope.
- All other open findings are unrelated and are not touched.

## 7. Files to edit

### Web implementation and tests

- `apps/web/src/features/space-links/services/filtersOf.ts`
- `apps/web/src/features/space-links/services/filtersOf.unit.test.ts`
- `apps/web/src/features/space-links/services/rowView.ts`
- `apps/web/src/features/space-links/services/rowView.unit.test.ts`
- `apps/web/src/features/space-links/services/updatedOn.ts` (only if the shared formatter is
  extended/reused for deletion wording)
- `apps/web/src/features/space-links/services/updatedOn.unit.test.ts`
- `apps/web/src/features/space-links/types/AdminSpaceRowView.ts`
- `apps/web/src/features/space-links/hooks/admin-list/useAdminSpacesFilters.ts`
- `apps/web/src/features/space-links/hooks/admin-list/useAdminSpacesList.ts`
- `apps/web/src/features/space-links/hooks/admin-list/useAdminSpacesList.component.test.tsx`
- `apps/web/src/features/space-links/components/admin-list/AdminSpacesList.tsx`
- `apps/web/src/features/space-links/components/admin-list/AdminSpaceCard.tsx`
- `apps/web/src/features/space-links/components/admin-list/AdminSpacesList.component.test.tsx`
- `apps/web/src/features/spaces/types/SpaceRef.ts`
- `apps/web/src/features/spaces/hooks/menu/useSpaceActionsMenu.ts`
- `apps/web/src/features/spaces/hooks/delete/useRestoreSpace.ts` (comments/types only unless
  behavior coverage reveals a defect)
- `apps/web/src/features/spaces/components/menu/SpaceActionsMenu.tsx`
- `apps/web/src/features/spaces/components/menu/SpaceActionsMenu.component.test.tsx`
- `apps/web/src/pages/dashboard/admin/SpacesPage.tsx` only if the slot's type needs an explicit
  deleted-row-compatible prop; otherwise leave it unchanged.
- `apps/web/src/shared/copy/english/spaceLinks.ts`
- `apps/web/src/shared/copy/arabic/spaceLinks.ts`

Existing fixtures in the focused tests will be extended with a deleted row (`deletedAt`, owners,
and both verification/hidden combinations). No API/shared file is included under the D1 licence.

### Shared documents and findings

- `docs/features/space-links.md`: web behavior, A3 two-fact row state, deleted status/list,
  restore-only action, deleted-date/owners behavior; remove the obsolete “contract but `deleted`”
  web decision; add the screen history and finding resolution links.
- `docs/features/spaces.md`: web row-actions behavior, restore action for deleted rows, and the
  shared restore feedback/429 hold wording.
- `docs/architecture/findings/44-no-screen-restores-a-deleted-space-once-its-toast-has-gone.md`:
  status `Resolved` and resolution.
- `docs/architecture/findings/50-an-owner-whose-only-spaces-are-deleted-stays-an-owner.md`:
  status `Resolved` for the owner-accepted documented path and resolution stating that the
  repository has no web unlink UI: restore → unlink → delete remains the operational way out.
- `docs/architecture/findings/README.md`: move 44 and 50 from Open to Resolved.
- `docs/project/overview.md`: extend the Space links and Spaces Built lines to state that the
  dashboard lists deleted spaces and restores them, without claiming unrelated work.

The API worker's concurrent files are under `apps/api`; this plan has no shared code-file overlap.
Shared documents are edited only in the web-owned sections/history and finding-resolution lines.
Findings/issues 69–70 require no file changes in this PR: #69 belongs to a future API-contract
touch, and #70 is already implemented in the dashboard shell. Do not edit `docs/api/api-contract.md`
or `apps/web/src/pages/dashboard/shell/PageHeader*`.

## 8. Design issues

No unresolved design issue was found. The prototype already reflects the approved A3/A7/A8
direction, including `status=deleted`, separate verification/hidden facts, muted deleted rows,
restore-only deleted actions, and the stale-or-missing chip. The implementation will use existing
design-system `Badge`, `BadgeList`, `ToggleGroup`, `Button`, `DataTable`, and responsive card
composition with semantic tokens only. No design issue is proposed for owner approval.

## 9. Tests and the break each catches

Every new test must be seen failing before the implementation change, then restored and committed
green. Tests remain in the lane of the unit that decides the behavior.

### Unit lane

- `filtersOf.unit.test.ts`: `status=deleted` parses, serializes, and requests as `deleted`; an
  invalid status is omitted. Break caught: the address can display or send the deleted list under
  the wrong status, or silently fall back when it should preserve `deleted`.
- `rowView.unit.test.ts`: live verified/hidden rows produce verification plus optional hidden
  badges; live unverified rows remain unverified; deleted rows produce deletion label/date and
  owner wording; missing freshness is `warning`. Break caught: A3 is collapsed again, deleted
  metadata is lost, or A8 regresses to neutral.
- `updatedOn.unit.test.ts` (if the helper is changed): deleted dates use the same Gaza day, language,
  Western digits, and year rule. Break caught: deletion dates differ from the list's established
  date rule.

### Component lane

- `AdminSpacesList.component.test.tsx` desktop: status select has All plus four status choices; a deleted request
  is sent with `status=deleted`; table cells show both live facts and a muted deleted row with
  owners/date and only its restore action. Break caught: filter wiring, table state rendering,
  deletion metadata, or action slot behavior regresses.
- `AdminSpacesList.component.test.tsx` phone: deleted card shows the same facts/date/owners and
  only restore; stale control is a ToggleGroup chip by the count, not a switch. Break caught:
  responsive rendering diverges or A7 is implemented as a field.
- `useAdminSpacesList.component.test.tsx`: the view exposes deleted option/labels, preserves
  filters/page request, and keeps previous rows busy during a status transition. Break caught:
  hook-level list wiring can disagree with the toolbar or query.
- `SpaceActionsMenu.component.test.tsx`: a deleted row exposes only Restore, keeps its trigger
  pending/focused while restoring, succeeds after the admin list refresh, and shows a named failure
  on refusal; live rows retain Edit/Hide-or-Show/Delete. Break caught: a deleted row could still
  edit, hide, delete, or expose an owner action, or restore feedback bypasses the established
  mutation/hold behavior.
- Existing accessibility assertions are updated and retained for desktop and phone. Break caught:
  the new badges, chip, muted row, or restore action introduces an accessible-name/structure defect.

### Manual browser verification

Manual visual review is not the only proof of behavior; it verifies the Definition of Done visual
matrix: RTL/LTR, light/dark, phone/desktop, deleted/live rows, filter chip, pending/error toasts,
and focus. Screenshots go to `C:\Users\basel\Downloads\adminlist-shots\`.

No API integration test is added because the endpoint and authorization behavior are unchanged and
the requested change is explicitly web-only.

## 10. Review Focus

Inputs not fully exercised by the planned automated tests:

- Search/place/stale combinations specifically while `status=deleted`, including an empty result and
  a page past the last deleted page.
- A deleted row with no owners and an English-only name in Arabic.
- A deleted row that was hidden and verified before deletion; restore must preserve both facts as
  supplied by the subsequent list response.
- A restore 429 that starts on one page and remains held after changing status/page/filter.
- A restore failure after the row leaves the current page, including request-reference wording.
- Keyboard focus after a restored row disappears and after a failed restore.
- Dark theme contrast and muted-row readability at all four required visual combinations.
- Gaza date boundary around midnight/year change for an actual `deletedAt`.
- Browser back/reload/deep-link behavior for `?status=deleted`.

## 11. Commits

Three atomic commits, each complete and Conventional Commit formatted (subjects are under 50
characters):

1. `feat(space-links): show deleted space facts`
   - status/address/row-view changes, copy, list/table/card, ToggleGroup/missing warning, and their
     unit/component tests.
2. `feat(spaces): restore deleted space rows`
   - deleted-row action seam, restore-only menu, pending/failure behavior, and menu tests.
3. `docs(admin): document deleted space restore`
   - capability documents, overview Built lines, and findings 44/50/index resolutions.

After each commit: `git status --short`, `npm run lint`, and `npm run typecheck`. Stage paths
explicitly; never use `git add -A` or `git add .`.

## 12. Execution and verification procedure

The executor must not depend on a Claude skill:

1. Confirm the owner approved this plan. Run `git fetch origin`, verify a clean worker-A tree and
   `HEAD` at `origin/main`; cut `feat/admin-deleted-spaces` with
   `git switch -c feat/admin-deleted-spaces origin/main`.
2. Implement commit 1 using the existing feature seams. For each new test, run its focused Vitest
   file before implementation to record the intended failure, implement, then run it green.
   Stage only the listed paths and commit.
3. Run `git status --short`, `npm run lint`, and `npm run typecheck`; fix root causes before moving
   on. Implement and commit 2, then repeat those checks. Implement and commit 3, then repeat them.
4. Before push, run the full local web verification one lane at a time:
   - `npm run lint`
   - `npm run typecheck`
   - `npm run test:unit`
   - `npm run test:component`
   - `npm run build`
   - `npm run check:build`
   - `npm run check:classes`
   - `npm run check:links`
   - `npm run format:check`
   No API lane is run because no API/shared code or behavior changes; this must be stated in the
   report.
5. Run the real web verification. Start the API and web using the repository setup instructions
   (`npm run dev -w @masaha/api` and `npm run dev`) only if their environment is configured; use
   the existing seeded admin data or a controlled deleted-space fixture. Check the screen at
   `/dashboard/admin/spaces?status=deleted`, restore a deleted space, verify the list refetch and
   toast, and inspect live/deleted rows. Capture screenshots for RTL/LTR, light/dark, phone/desktop
   at `C:\Users\basel\Downloads\adminlist-shots\`. Stop every server started and verify ports 3320
   and 5320 are free. If real data/setup blocks this, record the exact reason and do not claim the
   run succeeded.
6. Check scope and diff, then push:
   `git push -u origin feat/admin-deleted-spaces`.
7. Open the PR with:
   `gh pr create --assignee @me --label feat --label area:web --label area:docs --title "feat(space-links): show deleted space facts" --body-file <prepared-description>`
   The description must be:

   ```
   ## Summary
   Add the admin's deleted-spaces view and restore path to the dashboard.

   ## Scope / Acceptance criteria / Out of scope
   - Add the fourth `deleted` status filter backed by `GET /admin/spaces?status=deleted`.
   - Show verification and hidden state as separate facts, and show deleted dates and owners.
   - Make deleted rows muted and restore-only on desktop and phone.
   - Render stale-or-missing as a ToggleGroup chip and missing as warning.
   - Out of scope: API, shared contract, database, owner-link behavior, and new design-system work.

   ## Change type
   Feature, web and documentation.

   ## Evidence
   Ran: lint, typecheck, unit tests, component tests, build, check:build, check:classes,
   check:links, format:check, and the real browser run.
   Not run: API integration tests, because no API/shared code or behavior changed.

   ## Screenshots
   RTL/LTR, light/dark, phone/desktop screenshots are in the local verification set at
   `C:\Users\basel\Downloads\adminlist-shots\`.

   ## Definition of Done checklist
   - [x] Acceptance criteria met and scope kept.
   - [x] Lint, typecheck, build and checks pass.
   - [x] Unit and component tests pass.
   - [x] Arabic and English catalogues updated.
   - [x] RTL/LTR, light/dark, phone/desktop checked.
   - [x] API authorization remains server-owned; no API change.
   - [x] Capability docs, overview and findings updated.
   - [x] Atomic history and explicit path staging.
   ```

8. Wait for CI, run `gh pr checks <number>`, and require GitHub state `CLEAN` before the report.
   Never merge.
9. At report time, run the early conflict check against every other open PR head:
   `git merge-tree --write-tree <other-head> <pushed-head>` (using the repository's documented
   command shape and recording the result). Save the final report to
   `C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\ADMINLIST_REPORT.md` only after CI is green and
   the PR is clean.

## 13. Stop and ask

Stop and escalate instead of deciding silently if:

- `origin/main` is not clean/current, the worker tree is dirty with conflicting changes, or the
  requested branch already exists with unrelated work.
- The API/shared response does not actually contain the fields or endpoint promised by the prompt.
- A required behavior needs an API/shared/schema change, a new dependency, a new design-system
  component/token, or an architectural decision.
- The design prototype and settled decisions conflict in a way that changes the screen beyond this
  plan.
- No existing test lane can own a required behavior, or a test fails for an unexplained cause after
  three root-cause-driven fixes.
- The real run cannot create or reach a deleted row without altering production/API scope.
- CI fails in unrelated code and its root cause cannot be isolated to this branch.
- The PR conflicts with worker B's API branch in a shared file or the conflict cannot keep both
  sides.

## Appendix — skill map only

This is a map, not an execution dependency:

- `start-work-item`: preflight, authoritative reading, plan/branch lifecycle.
- `write-plan`: save this approved plan before edits.
- `open-pr`: scope check, atomic commits, push, PR preparation, CI/CLEAN and conflict handling.
- `final-report`: save the report after CI/CLEAN and after any review-fix round.
- `test-driven-development`: optional lens for seeing each new test fail before implementation.
- `systematic-debugging`: root-cause process for any failed check.
- `verification-before-completion`: evidence discipline for each completion claim.
