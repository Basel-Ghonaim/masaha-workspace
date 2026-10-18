# DELETED — the deleted spaces in the admin's list, one table of error statuses, and the parallel-work rule (API)

**Worker B** · worktree `C:\Users\basel\masaha-b`, detached at `origin/main` (`068efc6`; #62 and #61
merged; shared `dist` rebuilt) · branch `feat/admin-deleted-spaces`, cut with
`git switch --no-track -c feat/admin-deleted-spaces origin/main` after `git fetch --prune origin`.
Databases `masaha_b_dev` / `masaha_b_test`; API on 3321, web on 5321.

**Size cap:** at most 2 subagents, no self-review subagent, no workflow.
**Plan:** `C:\Users\basel\.prompt\MASAHA_WORKER_B\PLAN\DELETED_PLAN.md` (`write-plan`; save, then stop).
**Report:** `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\DELETED_REPORT.md` (`final-report`).
Follow the skills from start to end: `start-work-item`, `write-plan`, `open-pr`, `final-report`.

## 1. The task in brief

Three units, one PR:
- **The parallel-work rule (first commit, alone; the owner's decision).** Workflow §9's "two items
  in flight never work in the same layer" blocked three parallel items on 2026-10-12 whose only
  overlap was documents. The owner replaces it with a rule by files.
- **The deleted spaces in the admin's list** (design decision A3; it serves findings 44 and 50): the
  admin's list can show the soft-deleted spaces, so a screen can restore one after its toast has gone.
- **Finding 24:** the HTTP status of each error type lives once, in `packages/shared`.

## 2. Read first

In the order workflow §2 *Reading before work* gives.
- **The capability documents first:** `docs/features/space-links.md` (*The admin's list*, *API
  decisions* — note "a link to a deleted space counts for nothing" as narrowed by #60's R6) and
  `docs/features/spaces.md` (*Hide, delete, restore*, *API decisions*).
- `docs/development/workflow.md` §9 (all) and `docs/plans/v1-mvp.md` › *Ordering notes* (for D1);
- `docs/api/api-contract.md` §3 (error types), §4, §5 › `GET /admin/spaces`, `DELETE` and
  `POST …/restore`; `docs/backend/conventions.md` §4 (errors), §5 (pagination), §9 *Composed reads*;
  `docs/architecture/shared-package.md`; `docs/frontend/architecture.md` › the errors' normaliser (for
  finding 24's web side); `docs/development/testing.md` §1–§4;
- findings 24, 44 and 50 in full, and the open findings' titles;
- `C:\Users\basel\.prompt\MASAHA_DESIGN\DECISIONS_ADMIN.md` › **A3** (what the screen will show);
- the code: `space-links/admin-spaces/` (the composed list, `listingQuery`), `spaces/listing/`,
  `packages/shared/src/space-links/` (`SPACE_STATES`, `AdminSpaceRow`), `apps/api/src/shared/errors/`
  (`appError.ts`), the web's `shared/errors/toAppError.ts` and `features/space-links/` (what reads
  `SPACE_STATES` and `state`).

## 3. The settled decisions (review them in "Stronger decisions")

- **D1 — the rule, in workflow §9, its one home.** Replace the "one layer each" and "two items in
  flight never work in the same layer" items with: **items run in parallel in any layer when (1) at
  most one item in flight changes the schema, (2) at most one adds a dependency (already there), (3)
  no two open items edit the same code file — each plan lists its files and each prompt names the
  other open items'; shared documents and append-only lists (the contract, the overview's *Built*
  line, the findings index, a capability document's *Decisions* and *History*, catalogue lines) may be
  shared and are resolved by the fast path — and (4) every item that runs the API has its own
  databases and ports.** Worker A on the web and worker B on the API stay the default split, not a
  limit; task workers are added where the rule allows. **The owner's condition: no other document
  restates it.** `v1-mvp.md` › *Ordering notes* says "the two workers, one per layer, never work in
  the same layer at once": reword it to link §9 without restating any condition; check every other
  document and skill (`grep`) and make each link, not repeat. Commit it alone, first:
  `docs(workflow): run items in parallel by files` (≤ 50), its body the reason above. Checks for that
  commit: `format:check`, `check:links`.
- **D2 — the deleted spaces in `GET /admin/spaces`:** `status=deleted` lists the soft-deleted spaces
  only (hidden or not, verified or not), with the same search, place, stale filters, order and
  paging; every other status, and none, keeps leaving them out, as today. `POST …/restore` (built)
  brings one back. Settle in the plan:
  - **the row's state, as A3 decides it** ("a space's state is two facts": its verification always,
    hidden beside it, and now deleted): either `state` gains `"deleted"`, or the row carries the facts
    apart (for example `isVerified`, `isHidden`, `deletedAt`). Weigh what the screen needs and what the
    web already reads; recommend one;
  - a deleted row's **owners**: its owner links still exist (a delete writes nothing in them) but
    count for nothing in the lists; the screen's way out for finding 50 (restore, then unlink) needs
    the admin to see whose space it was. Recommend whether the row names them;
  - the composed read stays one query per module, every filter before the page.
- **D3 — finding 24:** the table of each error type's HTTP status moves into `packages/shared`; the
  API's `appError.ts` and the web's `toAppError.ts` both read it. Resolve finding 24.
- **The web, under workflow §9's licence (what breaks when a shared type changes):** only what D2's
  and D3's shared changes break. **The web shows nothing new:** the admin's list keeps its three
  status choices and its look until worker A builds A3's screen; if `SPACE_STATES` grows, the web's
  filter must not start offering "deleted" (keep its own list, or split the API's). No new screen,
  copy line or action.
- **Findings 44 and 50 stay Open:** each resolves with a *screen* (worker A, later). Do not change
  their status or evidence (documentation §1: a record changes only by its status and resolution).

## 4. Findings

- **Folded:** 24 (D3).
- **Served, not resolved:** 44, 50 (D2).
- Your new findings number **57–58** (51–56 are taken).

## 5. Risks

- **The parallel work, under the new rule itself:**
  - **The amenities worker** (`masaha-amenities`, PR soon, **the one schema change in flight**) edits
    `spaces/amenities/`, `spaces/facts/facts.ts`, `spaces/space/space.mapper.ts`,
    `space/space.api.test.ts`, `space/create.api.test.ts`, the lookups module, the seed,
    `packages/shared/src/{lookups,spaces}/`, the web's `features/lookups/` and `lookups.ts` catalogues,
    and `pages/dashboard/routes.component.test.tsx` (one fixture line). **You change no schema and
    edit none of these files.** Shared documents (contract, `spaces.md`, overview, plan) are allowed.
  - **Worker A** (main folder) edits `shared/storage/`, `shared/preferences/`, `shared/routing/`,
    `app/`, `pages/`, `features/auth` and `features/users` tests, `src/test/`, the `site` catalogues,
    `index.html`, `eslint.config.js`. **None of those.** If the web's licence needs one, stop and say so
    in the plan.
  - **The design fixer** works in `docs/design/` only.
- **Finding 24 crosses both apps:** prove the web's normaliser reads the shared table (its unit test),
  and the API's statuses unchanged (the API lane).
- No new dependency.

## 6. Checks, the pull request and the report

- **Locally, once each on the head, one at a time:** `test:unit`, `test:component` (the web's
  normaliser and list read shared types), `test:api`; `NODE_ENV=production npm run build` and
  `check:build`; `lint`, `typecheck`, `check:classes`, `format:check`, `check:links`. Rebuild the
  shared `dist` first.
- **Real requests** against your API (3321), each in the report: delete a space, list
  `status=deleted` (it is there, with the search and a place filter), the other statuses (it is not),
  restore it (it is back in its own state).
- **PR:** title `feat(space-links): list the deleted spaces` (≤ 50), labels `feat`, `area:api`,
  `area:web`, `area:docs`, assigned to the owner. The analyst reviews it. Don't merge.
- **The documents in this PR:** workflow §9 and the plan's *Ordering notes* (D1, its own commit); the
  contract (`GET /admin/spaces`, §3 if the table's home is named there); `space-links.md`;
  `shared-package.md` if the table's place is its business; finding 24 resolved with the index;
  overview's *Built*.
- At the report, `git merge-tree --write-tree` against every open PR (the amenities worker's,
  worker A's, the design fixer's). Stop every background shell you start; `jq` is not installed —
  use `gh … --jq`.
