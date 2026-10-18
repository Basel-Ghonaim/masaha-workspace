# DELETED — the deleted spaces in the admin's list, one table of error statuses, and the parallel-work rule (API) — Plan

Worker B · worktree `C:\Users\basel\masaha-b` · branch `feat/admin-deleted-spaces`, cut with
`git switch --no-track -c feat/admin-deleted-spaces origin/main` after `git fetch --prune origin`, once
the plan is approved · databases `masaha_b_dev` / `masaha_b_test` · API 3321, web 5321. Base:
`068efc6` (#61 and #62 merged), checked equal to `origin/main` after `git fetch origin`, tree clean.
No PR is open on GitHub at the time of planning.

## 1. Summary

Three units, one PR, four commits.
- **D1, alone and first:** workflow §9's "one layer each / never in the same layer" becomes a rule by
  files: four conditions, in §9 only; `v1-mvp` › *Ordering notes*, workflow §2 and the `write-plan`
  skill link it instead of restating it.
- **D3 (finding 24):** the HTTP status of each error type, and its reverse lookup, live once in
  `@masaha/shared/core`; the API's `AppError` and error handler and the web's `toAppError` read them.
  Finding 24 resolved.
- **D2 (A3; serves findings 44 and 50):** `GET /admin/spaces?status=deleted` lists the soft-deleted
  spaces only, with every other filter, the order and the paging; each row carries its state as facts
  apart (`isVerified`, `isHidden`, `deletedAt`) instead of one `state`, and a deleted row still names
  its owners. The web looks and behaves exactly as today: three status choices, `?status=deleted`
  in the address falls back to "all", the badge still "hidden first".

## 2. The contract

**Scope**
- Workflow §9 rewritten by files (D1); §2's two mentions, `v1-mvp` › *Ordering notes* and
  `write-plan` step 1.7 link it.
- `ERROR_STATUSES` and `errorTypeOfStatus` in `packages/shared/src/core/errors.ts`; the API's
  `ERROR_DEFINITIONS` keeps only its developer messages; the web's `TYPE_BY_STATUS` goes.
- `SPACE_STATES` → `SPACE_STATUSES` (`'verified' | 'unverified' | 'hidden' | 'deleted'`), the
  filter's vocabulary only; `AdminSpaceRow.state` → `isVerified`, `isHidden`, `deletedAt`.
- `spaces`' listing takes `deleted: true` (only the soft-deleted spaces); without it, none, as today.
- The web, under §9's licence: only what the shared changes break (§7 below).
- Documents: workflow, v1-mvp, the skill, the contract (§3 line, `GET /admin/spaces`, `DELETE`),
  `space-links.md`, `spaces.md`, finding 24 + index, overview's *Built*.

**Acceptance criteria**
- [ ] §9 holds the four conditions once; `grep` finds no other document or skill restating them.
- [ ] `status=deleted` lists only soft-deleted spaces, hidden or not, verified or not, with search,
      governorate/area and stale applied before the page is cut; by English name.
- [ ] Every other status, and none, still leaves soft-deleted spaces out.
- [ ] Each row says `isVerified`, `isHidden`, `deletedAt` (ISO, `null` for a live space); a deleted
      row names its active owners.
- [ ] Restoring a listed deleted space returns it to its own state (real requests).
- [ ] Each error type's status is written once, in `packages/shared`; the API's statuses unchanged
      (API lane), the web types an envelope-less answer by the shared table (unit lane).
- [ ] The web's admin list unchanged: three status choices, `?status=deleted` reads as "all", same
      badges; no new screen, copy line or action.
- [ ] Finding 24 resolved; findings 44 and 50 untouched.

**Out of scope**
- A3's screen (two badges, a fourth filter choice, muted rows, «استرجاع») — worker A, later.
- Any change to findings 44 and 50's status or evidence.
- Any schema change, dependency, or file of the amenities worker or worker A (but see owner decision 2).

## 3. Reading done

CLAUDE.md; workflow (§2 *Phases*, *Reading before work*, §3, §4, §6–§9, *Conflicts*); the map; the
findings index (open titles) and findings 24, 44, 50, 18 in full; `features/space-links.md` and
`features/spaces.md` (whole: both are short enough that the linked sections are most of them);
`plans/v1-mvp.md` › *Ordering notes*; api-contract §3, §4, §5 › *Spaces (the admin)* (`GET`, `DELETE`,
`restore`, `AdminSpace`); conventions §4, §5, §9 › *Composed reads*; `shared-package.md`;
frontend architecture's normaliser paragraph; testing §1–§4; setup › *Running a second folder*;
`DECISIONS_ADMIN.md` › A3; the `write-plan` and `start-work-item` skills; `grep` for every restatement
of the layer rule (docs, skills, CLAUDE.md, README).

Code: `space-links/admin-spaces/` (service, mapper, `listingQuery` and their tests, the API test),
`space-links.repository.ts` (`findOwnerLinks`, `findVerifiedSpaceIds`), `spaces/listing/`,
`packages/shared/src/space-links/`, `packages/shared/src/core/errors.ts`,
`apps/api/src/shared/errors/` (`appError.ts`, `errorHandler.ts`, its API test), the web's
`shared/errors/toAppError.ts` and its test, `features/space-links/` (`filtersOf`, `rowView`,
`useAdminSpacesList`, `useAdminSpacesFilters`, the types, the tests), `features/spaces/` (`SpaceRef`,
`useSpaceActionsMenu`, its test), `pages/dashboard/admin/SpacesPage.tsx` and
`pages/dashboard/routes.component.test.tsx`.

## 4. The settled decisions, as they will be built

### D1 — the rule by files (commit 1, alone)

Workflow §9, its one home:
- Intro: "two AI workers" → "several AI workers".
- **Workers** (was "Two workers, one layer each"): worker A in the main folder, on the web by default;
  worker B in `masaha-b`, on the API by default, with the schema, the migrations and the seed. The
  split is the default, not a limit: a task worker, in a worktree of its own, is added where the rule
  below allows. One Work Item, one fresh conversation (kept).
- The licence and "the contract is the API worker's" bullets: unchanged.
- **Items in parallel** (replaces "Two items in flight never work in the same layer"): items run in
  parallel in any layer when (1) at most one item in flight changes the schema; (2) at most one adds a
  dependency; (3) no two open items edit the same code file — each plan lists its files and each
  prompt names the other open items'; shared documents and append-only lists (the contract, the
  overview's *Built* line, the findings index, a capability document's *Decisions* and *History*,
  catalogue lines) may be shared, each side in its own section, and a conflict there takes the fast
  path (*Conflicts*); (4) every item that runs the API has its own databases and ports. A plan that
  needs another open item's file stops and says so.
- **Files** bullet: folded into condition (3) (it said the same of two workers).
- **Dependencies:** keeps the declaration (§6) and the lockfile rule; "never both at once" is now
  condition (2), so it links it instead of saying it again.
- **Databases:** "two workers never share" → "two items never share"; A's and B's names kept; "any
  other worktree whose item changes the schema" → "any other folder that runs the API: its own
  `masaha_<item>_dev` / `_test` and ports ([setup › Running a second folder])".

Elsewhere, links only:
- `v1-mvp` › *Ordering notes*: "The API may run one step ahead of the screens; what runs in parallel
  is [workflow §9](…)'s." No condition restated.
- Workflow §2 phase 1 "the boundaries with the other worker (§9)" → "the other open items' files
  (§9)"; phase 2 "the files, the other layer's included (§9)" → "the files it edits, the other layer's
  included (§9)".
- `write-plan` 1.7: "the files it edits: the other layer's under the licence the plan declares, and
  any shared with another open item, with the section each side owns (§9)".
- Checked and left: `documentation.md` §5 ("so the two workers append in different places" — the
  reason for the layered parts, still true of the default split) and the findings index's number
  ranges; CLAUDE.md, README, setup and the other skills say nothing of the rule.

Commit: `docs(workflow): run items in parallel by files`, body: the old rule blocked three parallel
items on 2026-10-12 whose only overlap was documents; the owner replaces it with a rule by files.
Checks: `format:check`, `check:links`.

### D3 — one table of statuses (finding 24)

- `packages/shared/src/core/errors.ts`, beside `ERROR_TYPES`:
  `ERROR_STATUSES = { bad_request: 400, …, service_unavailable: 503 } as const satisfies Record<ErrorType, number>`
  (every type, no other key), and `errorTypeOfStatus(status): ErrorType | undefined`, the table read
  backwards. Both crossing apps' rule (shared R5); `core` imports nothing new (R3).
- API `appError.ts`: `ERROR_DEFINITIONS` becomes `ERROR_MESSAGES: Record<ErrorType, string>` (the
  developer English stays the API's); `status = ERROR_STATUSES[type]`; `errorTypeForStatus` removed,
  `errorHandler.ts` imports `errorTypeOfStatus` from `@masaha/shared/core`.
- Web `toAppError.ts`: `TYPE_BY_STATUS` removed; `typeOfStatus` = `errorTypeOfStatus(status) ??
  (status >= 500 ? 'server' : 'unknown')`; the comment no longer cites finding 24.
- Contract §3: one line under the table, "In code: `ERROR_STATUSES` (`@masaha/shared/core`), which
  both apps read." `shared-package.md` unchanged: its `core` line already holds "the error vocabulary".
- Finding 24: `Resolved`, with its resolution line; moved in the index.

### D2 — the deleted spaces in `GET /admin/spaces`

- **Shared** (`space-links/requests.ts`, `responses.ts`): `SPACE_STATUSES = ['verified',
  'unverified', 'hidden', 'deleted']`, `SpaceStatus`; the query's `status` reads it. `AdminSpaceRow`:
  `state` → `isVerified: boolean` (an active OWNER link), `isHidden: boolean`, `deletedAt: string |
  null` (ISO 8601; `null` for a live space);
  `owners` unchanged (its active owner links, a deleted space's included).
- **`spaces`, listing:** `ListingFilter.deleted?: true` → `deletedAt: { not: null }`, else `deletedAt:
  null` as today; `LISTED` selects `deletedAt`; `ListedSpace.deletedAt: Date | null`. Every other filter, the
  order and the paging unchanged, so the deleted spaces are filtered before the page is cut.
  (`spaces/listing/` is none of the amenities worker's files.)
- **`space-links`:** `listingQueryOf` maps `status=deleted` to `{ deleted: true }` with no `ids` and
  no `isHidden` (hidden or not, verified or not); the other statuses unchanged. The service is
  unchanged: one query per module, `findVerifiedSpaceIds` still read only for verified/unverified,
  `findOwnerLinks` already reads a deleted space's active links. `toAdminSpaceRow` writes the three
  facts: `isVerified: owners.length > 0`, `isHidden`, `deletedAt` (ISO or `null`).
- **Restore:** `POST …/restore` as built; the real run shows the space back in its own state.

## 5. Stronger decisions

1. **The row's state as facts apart, not `state: "deleted"`** (the prompt's open choice). *What:*
   `isVerified`, `isHidden`, `deletedAt` replace `state`. *Why:* A3 makes a state two facts (the
   verification badge always, "hidden" beside it); `state` hides a hidden space's verification, and a
   `"deleted"` value would hide both, so the restore screen could not say the space comes back hidden
   or verified. `AdminSpace` already speaks `isHidden` / `isVerified`: one vocabulary for the two admin
   responses. The rule "hidden first" was presentation, and moves to the web's badge until A3's screen.
   *Cost:* the web's row consumers and their fixtures change (§7), among them three fixture lines in
   `pages/dashboard/routes.component.test.tsx` — **a file of worker A's `pages/` and of the amenities
   worker** (owner decision 2). *Alternative:* `state` gains `"deleted"`: no shared test file, but the
   web must narrow a value it cannot word (`lines.states` has no "deleted" and no copy line is allowed),
   and A3's screen would reopen the shape. **Recommended: facts apart.**
2. **`SPACE_STATES` → `SPACE_STATUSES`** (the query's own name). *Why:* without `state` on the row the
   name describes nothing; the filter is `status`. *Cost:* four web imports already touched by (1).
   **Recommended.**
3. **A deleted row names its owners** (the prompt's open choice). *Why:* finding 50's way out is
   restore → unlink → delete; the admin must see whose space it was, and the links are kept as they
   are. *Rule narrowed:* "a link to a deleted space counts for nothing … in the lists" gains a second
   exception beside the global role: the admin's deleted list names them (and `isVerified` follows
   them, so the row says what a restore brings back). Recorded in `space-links` › *API decisions*, and
   the `DELETE` line of the contract. *Cost:* none in code. **Recommended.**
4. **`deletedAt: string | null`** (the owner's choice, against the plan's `isDeleted`). *Why:* the
   design fixer's approved 2b plan shows a deleted row as «محذوفة في …», muted with «استرجاع»: the
   screen needs the date now. No `isDeleted`.
5. **The reverse lookup moves with the table** (`errorTypeOfStatus`). *Why:* both apps read the table
   backwards (the API's error handler for Express's 4xx, the web for a proxy's answer): a rule both
   compute (shared R5), one implementation and one unit test. *Cost:* none. **Recommended.**
6. **The web keeps its own status list,** `ADMIN_LIST_STATUSES = ['verified', 'unverified',
   'hidden'] as const satisfies readonly SpaceStatus[]` in `services/filtersOf.ts`, read by the address
   and the filter's options. *Why:* the prompt's "keep its own list" rather than split the API's enum
   (one vocabulary on the wire); without it, `?status=deleted` typed in the address would list the
   deleted spaces under Hide/Delete menus. **Recommended.**

No rule of the documents is contradicted beyond (3), which is recorded.

## 6. Related findings

- **24 — folded** (D3). Cost: three source files and one test per side.
- **44, 50 — served, not resolved:** the API now lists what a screen needs; each resolves with worker
  A's screen. Their status and evidence untouched (documentation §1).
- **18 (resolved)** — its rule is narrowed by decision 3, recorded in `space-links.md`; the finding
  itself is a record and stays as it is.
- None other of the open titles touches this item. New findings, if any: **57–58**.

## 7. Files

**API (mine):** `packages/shared/src/core/errors.ts` (+ new `errors.unit.test.ts`),
`packages/shared/src/space-links/{requests,responses}.ts`; `apps/api/src/shared/errors/{appError,errorHandler}.ts`;
`apps/api/src/modules/spaces/listing/{listing.repository,listing.service}.ts`;
`apps/api/src/modules/space-links/admin-spaces/{adminSpaces.mapper,listingQuery}.ts` and their unit
tests, `adminSpaces.api.test.ts`.

**Web, under §9's licence (what the shared changes break; nothing shown changes):**
- `shared/errors/toAppError.ts` (D3).
- `features/space-links/`: `services/filtersOf.ts` (+ its unit test), `services/rowView.ts` (+ unit
  test), `hooks/admin-list/useAdminSpacesList.ts`, `useAdminSpacesFilters.ts`,
  `types/AdminSpacesFilters.ts`, and the fixtures of `AdminSpacesList.component.test.tsx`,
  `useAdminSpacesList.component.test.tsx`, `repository/spaceLinksRepository.unit.test.ts`.
- `features/spaces/`: `types/SpaceRef.ts` (`'state'` → `'isHidden'`), `hooks/menu/useSpaceActionsMenu.ts`
  (`space.isHidden`), `components/menu/SpaceActionsMenu.component.test.tsx` (fixtures).
- **`pages/dashboard/routes.component.test.tsx`: three fixture lines** (`PALM`'s `state: 'hidden'`,
  `FOCUS`/`WHITE`'s `state: 'verified'`, lines ~538, 626, 627, in *the admin's spaces page*). This file
  is in worker A's `pages/` and carries the amenities worker's one fixture line: **owner decision 2.**
  No production file of `pages/` changes (`SpacesPage` passes the row as `SpaceRef`).

**Documents (shared, own sections):** `docs/development/workflow.md`, `docs/plans/v1-mvp.md`,
`.claude/skills/write-plan/SKILL.md`, `docs/api/api-contract.md` (§3 line; `GET /admin/spaces`;
`DELETE`), `docs/features/space-links.md` (behaviour, *API decisions*, *Web decisions*, both
histories), `docs/features/spaces.md` (*What it does* line on the listing; *API history*),
`docs/architecture/findings/24-…md` and `README.md`, `docs/project/overview.md` (*Built*, Space links).

**Not touched:** every file of the amenities worker (`spaces/amenities/`, `facts/facts.ts`,
`space/space.mapper.ts`, the space tests, lookups, seed, `shared/{lookups,spaces}`, web lookups) and of
worker A (`shared/storage|preferences|routing`, `app/`, `pages/` — but the line above —, auth/users
tests, `src/test/`, site catalogues, `index.html`, `eslint.config.js`); `docs/design/`. No schema, no
dependency.

## 8. Design issues

None: no screen is built or changed.

## 9. Tests: lane, test, the break it catches

Every new test seen failing first; changed fixtures follow the shape.

| Lane | Test | Break it catches |
|---|---|---|
| Unit (shared) | `errorTypeOfStatus` gives each contract status's type (400…503, hand-written) and `undefined` for 418 and 502 | a wrong or missing status in the table |
| API | `errorHandler.api.test` "each type → its status" (existing, hand-written) | the API's statuses changing with the move |
| Unit (web) | `toAppError` "types a status of the contract by its status" (existing, 503) — proven by reverting the lookup once | the web no longer reading the table (503 would fall to `server`) |
| Unit (API) | `listingQueryOf`: `status=deleted` → `{ deleted: true }`, no `ids`, no `isHidden`; with `areaId`, `q`, `stale` kept | deleted ignored, or narrowed to not hidden / verified |
| Unit (API) | `toAdminSpaceRow`: a hidden space with an owner → `isHidden` and `isVerified` both true; a deleted one → its `deletedAt` as an ISO string (hand-written), a live one `null`; no owner → not verified | "hidden first" collapsing the facts again |
| API | `status=deleted` lists only the deleted spaces, a hidden verified one (with its owner named) and an unverified one, not the live ones | `deletedAt` filter missing or inverted; owners dropped on a deleted row |
| API | `status=deleted` with `q` and `areaId`, and with `stale=true`, keeps only the matching deleted spaces | a filter skipped for the deleted list |
| API | `status=deleted&limit=2`: deleted spaces interleaved by name with live ones, full pages and the right total | deleted filtered after the page is cut |
| API | it.each none / verified / unverified / hidden: a deleted (hidden, verified) space is never listed (extends "leaves a soft-deleted space out") | `deleted` leaking into another status |
| API | `?status=closed` still `invalid_choice` (existing) | — (kept) |
| Unit (web) | `filtersOf`: `status=deleted` reads as no status (added to the "unknown" it.each) | the address reading by the contract's enum and requesting deleted spaces |
| Component (web) | `useAdminSpacesList` "offers the three states as filters" (existing, retitled) | the filter offering "deleted" once `SPACE_STATUSES` grows |
| Unit (web) | `rowView`: the badge is hidden whatever the owners, else verified / unverified (existing it.each, fed facts) | the badge read wrongly from the facts |
| Component (web) | `SpaceActionsMenu`: Show for a hidden space, Hide otherwise (existing, `isHidden` fixtures) | the menu reading a field the row no longer has |

## 10. Review Focus (inputs no planned test exercises)

- `status=deleted` with `governorateId` and an `areaId` outside it through the API (the pure rule
  covers it, the API lane does not).
- A deleted space whose owner link was deactivated before the delete (no owner, unverified).
- A deleted space in a retired area (the area's name still comes from `lookups`).
- 413 and 415 without an envelope on the web (the table covers them; only 503 is tested there).
- `?status=deleted` in a real browser (unit only; the browser run below checks it once).

## 11. Commits

1. `docs(workflow): run items in parallel by files` — workflow §2 and §9, v1-mvp, `write-plan`.
2. `refactor(errors): keep each error status in shared` — D3 on both sides, the shared test, the
   contract's §3 line, finding 24 resolved with the index.
3. `feat(space-links): give a row its state as facts` — `isVerified` / `isHidden` replace `state`
   (`SPACE_STATUSES` renamed, still three), API mapper and tests, the web's consumers (the badge
   "hidden first" in `rowView`, the menu's `isHidden`), the fixtures, the contract's row, `space-links.md`.
4. `feat(space-links): list the deleted spaces` — `deleted` in `SPACE_STATUSES`, `deletedAt`, the
   listing's filter, `listingQueryOf`, the API tests, the web's own status list and its tests, the
   contract (`GET`, `DELETE`), `space-links.md` (decision 3), `spaces.md`, overview's *Built*.

Lint and typecheck on each; the lanes once on the head. PR title: `feat(space-links): list the
deleted spaces`; labels `feat`, `area:api`, `area:web`, `area:docs`; assigned to the owner.

## 12. Verification (phase 4)

- Rebuild the shared `dist` first; then, one at a time on the head: `test:unit`, `test:component`,
  `test:api`; `NODE_ENV=production npm run build`, `check:build`; `lint`, `typecheck`,
  `check:classes`, `format:check`, `check:links`. Commit 1 alone: `format:check`, `check:links`.
- **Real requests** against the API on 3321 (`masaha_b_dev`, demo seed), each in the report: delete a
  verified hidden space; `status=deleted` lists it (with `q` and an `areaId`), with its owners and its
  facts; `verified`, `unverified`, `hidden` and none do not; restore it; it is back under `hidden`,
  verified, and gone from `status=deleted`.
- **Browser, once** (web on 5321): the admin's list offers three statuses; `?status=deleted` shows
  every live space under "all"; the badges as before. No screenshots (no UI change).
- Servers stopped by PID and ports 3321/5321 checked free.
- Not run: E2E (end of project); RTL/LTR and theme review (nothing visible changes).
- At the report: `git merge-tree --write-tree` against every open PR (amenities, worker A, design fixer).

## 13. Decisions from the owner (DELETED_PLAN_REPLY.md, approved)

1. **The row's shape:** facts apart — approved (A3: a state is two facts, and the restore screen must
   say what comes back).
2. **`pages/dashboard/routes.component.test.tsx`:** option (a), granted — **the three fixture lines
   only**, in *the admin's spaces page*, as an explicit exception to the new rule's condition (3),
   said in the PR description. Whichever PR merges second resolves it keeping both sides, with lint
   and typecheck.
3. **`SPACE_STATES` → `SPACE_STATUSES`:** approved.
4. **A deleted row names its owners:** approved, with the narrowing recorded as written.
5. **`deletedAt: string | null`, not `isDeleted`** (the owner's choice): the design fixer's approved
   2b plan shows «محذوفة في …». The row carries `deletedAt` (ISO, `null` for a live space) beside
   `isVerified` and `isHidden`; no `isDeleted`. §1, §4, §5, §9 and §11 updated accordingly.
6. **The D1 wording:** approved as written.
