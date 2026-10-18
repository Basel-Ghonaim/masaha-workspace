# S2a-1 — The lookups API (the admin's governorates, areas and amenities)

**Worker B** · worktree `C:\Users\basel\masaha-b` · branch `feat/admin-lookups-api`, cut with
`git switch --no-track -c feat/admin-lookups-api origin/main` after `git fetch --prune origin`.
PR #39 is merged; if the worktree is still on `feat/dashboard-shell`, switch to detached `origin/main`
first (leave the local branch: deleting it is the owner's).

**Size cap:** at most 4 subagents in total, and no self-review subagent (an independent review gate
follows the PR). Do not run any workflow. Keep the session focused: this prompt names the documents
and sections to read; don't sweep the repository.

## 1. How to work

- **Start with the `start-work-item` skill.** Plan in plan mode before writing code.
- **The owning documents, by section:**
  - `docs/backend/conventions.md`: §3 (validation and text), §4 (errors), §6 (audit), §7 (levels,
    routers, the modules table), §8 (R1–R8, transactions, space access as the model for a guard
    mounted once), *Growth*;
  - `docs/backend/security.md`: the access token's claims, `requireRole`, rate limits;
  - `docs/api/api-contract.md`: §1–§5, and §6 for how codes are added;
  - `docs/architecture/data-model.md`: *Conventions* (bilingual content, two-level areas, active
    flags) and *Lookups*, *Publicly listed*;
  - `docs/architecture/shared-package.md` (capabilities, subpath imports, levels);
  - `docs/development/testing.md`: §1–§4 (every authorization rule per role);
  - `docs/plans/v1-mvp.md`: step 2, and *Planned API surface* › Admin;
  - ADR 0007 (soft delete) and ADR 0015 (who carries an idempotency key).
- **The designs** (for what the API must serve, not to build): SCREENS.md row 30, and
  `docs/design/screens/47-admin-lookups/` (governorates with their areas, hidden ones dimmed, reorder
  arrows, active switches, an edit sheet; amenities with the filter switch).
- **When finished, follow the `open-pr` skill.**
- **The owner's rules:**
  - honest test titles;
  - **no parameter, option or callback that only tests pass or that nothing uses**; tests stub the
    platform's seams;
  - **one responsibility per file** (architecture.md §3 holds it for the web; apply the same to the
    API: one service, repository or controller per resource once a module holds several);
  - **checks:** each commit passes lint and typecheck on its own; the full lanes (`check:classes`,
    unit, component, api, build + `check:build`) run on the head, one at a time;
  - commit subjects of 50 characters or fewer; report only once CI is green on the pushed head;
  - review fixes fold into the commits they correct (fixup + autosquash, `--force-with-lease`), with
    ONE "Review fixes" comment on the PR;
  - no tool or AI attribution anywhere.

## 2. What this item delivers

The first admin API: the bilingual lookup lists the admin keeps, guarded by role and audited. It is
the first of three items for build step 2's lookups: this one is **API only**; the web's
governorates-and-areas tab (S2a-2) and amenities tab (S2a-3) follow and consume it.

**What exists:** the tables `governorates`, `areas`, `amenities` (with seed data), no migration
needed; the `lookups` module (L0) with one service call (`areaNamesFor`) and **no router**;
`packages/shared/lookups` with `AMENITY_ICON_KEYS`; `requireAuth` and `can()` in `shared/auth`;
`textSchema` in `@masaha/shared/core`.

**It builds:**
- **`requireRole(...roles)`** in `shared/auth`: reads the role from the access token's claims;
  403 `forbidden` otherwise (security.md).
- **The audit writer `shared/audit`**, the project's first: append-only, the only writer of the
  audit table, takes the caller's `tx` so an entry commits or rolls back with its change, knows no
  domain (the calling service names the action and the entity) — conventions §6.
- **The `lookups` admin router**, under `/admin`:
  - `GET /admin/governorates`: every governorate with its areas, hidden ones included, in order;
  - `POST /admin/governorates`, `PATCH /admin/governorates/:id`;
  - `POST /admin/areas` (in a governorate), `PATCH /admin/areas/:id`;
  - `GET /admin/amenities`, `POST /admin/amenities`, `PATCH /admin/amenities/:id`;
  - the three order endpoints (decision L3).
- **Every write and its audit entry in one transaction.** Audited: added, edited, hidden, restored.
- **The contract in code:** request and response schemas in `packages/shared/lookups`, built on
  `textSchema`.
- **The documents:** api-contract.md §5 (the endpoints) and §4 (the exception, L2); the status lines
  of conventions.md (`requireRole`, the audit writer, the `lookups` admin router) and security.md
  (`requireRole`).

## 3. The owner's decisions

Approved after analysis. **You may challenge any of them:** if your reading of the code or the
documents shows a stronger alternative, put it in your plan with its trade-off and your
recommendation. The owner and the analyst weigh it; **don't build an alternative until it is
approved.**

- **L1 — the guard is mounted once:** `requireAuth` and `requireRole('ADMIN')` on the `/admin`
  prefix in the composition root, as `requireSpaceAccess` is mounted once on `/manage` (conventions
  §8). Each module's admin router stays unguarded inside it, so a new admin router can't forget it.
- **L2 — no pagination on the admin's lookup lists:** a bounded catalogue of tens of rows that the
  screen shows whole, grouped. Record it as an exception in api-contract.md §4, beside the planned
  exception for `GET /spaces`.
- **L3 — ordering is a full list per scope, in one transaction:**
  `PUT /admin/governorates/order`, `PUT /admin/governorates/:id/areas/order`,
  `PUT /admin/amenities/order`, body `{ ids: number[] }`. The ids must be exactly the scope's current
  set (no missing, extra or repeated id); otherwise 409 `conflict`. Safe to repeat.
- **L4 — hide and restore are `isActive` in the same `PATCH`** as the names. The service derives the
  audited action from the change: hidden, restored or edited (a `PATCH` changing both writes the
  entries your plan defines).
- **L5 — no new domain codes:** a duplicate name answers 409 `conflict` with
  `errors.<field> = ["not_unique"]` (as `EMAIL_TAKEN` does, without a code); a stale order list
  answers 409 `conflict` with no code. `core` and the copy catalogues are untouched.
- **L6 — an amenity's key is derived** from `nameEn` in snake_case when it is created, and never
  changes afterwards. A key that collides (a retired amenity's included) answers 409 with
  `errors.nameEn = ["not_unique"]`; a name that yields an empty key is a validation error.
- **L7 — a new row is placed last** in its list (`max(sortOrder) + 1`).

**Fixed by the documents** (still valid; flag it if you find otherwise):
- no delete: hiding and restoring with `isActive` (data-model, the plan; relations restrict);
- both names required (data-model);
- hiding a governorate changes none of its areas' flags: public listing already requires both to be
  active (data-model › *Publicly listed*);
- `lookups` is L0 and owns its three tables, with a public and an admin router (conventions §7);
- no idempotency key: ADR 0015 limits it to the front desk's creates, so the transport won't retry
  these `POST`s;
- an amenity's icon is one of `AMENITY_ICON_KEYS`; it has `isFilterable`;
- an area's governorate is set at creation and is not editable (the design's edit sheet has no such
  field).

## 4. Your plan decides

- the module's files per resource (*Growth*), the controller and routes shape, and the mappers;
- the audit actions' names and the `before` / `after` shape: **stable names**, because the audit
  reader will list them later;
- the names' length limits, within `textSchema`;
- how a unique violation becomes the 409 (reuse whatever the code already does for `EMAIL_TAKEN`);
- whether the lint level rule needs `shared/audit` declared;
- the commits (a sketch: the role guard; the audit writer with its first consumer, so no unit lands
  unused; governorates and areas; amenities).

## 5. Tests

Per testing.md, one behaviour in one lane:
- **unit** (`packages/shared`): the schemas: both names, `textSchema`'s rules, the icon list, the
  order body;
- **unit** (`apps/api`): `requireRole` (an allowed role passes, any other is 403); the services with
  plain-object fakes: the key's derivation, the audited action derived from a change, the order
  list's validation;
- **api** (real database):
  - **every endpoint as a guest (401), a USER (403), an OWNER (403) and the ADMIN**, and an admin with
    a pending password change (403 `PASSWORD_CHANGE_REQUIRED`);
  - 422 for invalid input, 409 with `not_unique` for duplicates, 404 for an unknown id;
  - hiding and restoring; the order: applied atomically, a stale or partial list refused with 409;
  - **an audit entry is written with each audited change, and rolls back with it** when the
    transaction fails; reordering writes none;
- no web test: this item has no UI.

## 6. Out of scope

- **Any web file**: the feature, the page and the copy come with S2a-2 and S2a-3.
- **`GET /lookups`** (the public read): deferred to its first consumer, the admin's space form (S2b).
- The audit reader (the `audit` module) and its screens; `optionalAuth`; the space middleware.
- Delete; moving an area to another governorate; any schema change or migration; the seed.
- New domain error codes; the copy catalogues.
- `overview.md` › *Built* (S2a-3 writes it); findings 10 and 11 (S2a-3 and S2b close them).
- **New dependencies.** If you think one is needed, stop and ask.

If the plan finds the documents missing something this item needs, or a decision that can't hold,
stop and report: record it, don't absorb it.

## 7. Parallel work

**Worker A** works in `C:\Users\basel\masaha`: PR #40 (the recovery pages, web only) now, then
F-5b3b (Google sign-in on the web), which may touch the `auth` module, `app.ts`, api-contract.md §5
(*Session* and auth), security.md, `packages/shared` (`auth`, `core`), the copy catalogues and
`package-lock.json`.
- **Declare your shared files in the plan:** `apps/api/src/app.ts`, api-contract.md (§4 and your own
  §5 subsection), the status lines of conventions.md and security.md.
- Edit them minimally, each side in its own section. **Whoever merges second** rebases and keeps
  both sides.
- Your databases are `masaha_b_dev` and `masaha_b_test`; your API runs on 3321.

## 8. Pull request

- **Title:** `feat(lookups): add the admin's lookups API` (or the main commit's subject).
- **Labels:** `feat`, `area:api`, `area:docs`. Assigned to the owner.
- **The description:** scope, acceptance criteria and out of scope; the decisions L1–L7 and any you
  challenged; evidence per lane; what was not run.
- **Review:** the independent review gate, after you report.
- After CI is green on the pushed head, stop and report: the head, the commits, the counts per lane,
  your tokens. Don't merge. Don't create an Issue.
