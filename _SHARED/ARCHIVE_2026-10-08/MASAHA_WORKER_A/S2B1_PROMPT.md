# S2b-1 — The admin's spaces API: create, list, edit the profile, hide and delete

**Worker A** · main folder `C:\Users\basel\masaha` · branch `feat/admin-spaces-api`, cut from the
latest `origin/main` (the folder is on `main`, clean). Databases `masaha_dev` / `masaha_test`; API on
3320.

**Size cap:** at most 4 subagents in total, and **no self-review subagent** (an independent review
gate follows the PR). Do not run any workflow. Read the documents and sections named here; don't
sweep the repository.

## 1. How to work

- **Start with the `start-work-item` skill.** Plan in plan mode before writing code.
- **The owning documents, by section:**
  - `docs/backend/conventions.md`: §3–§6 (validation, errors, pagination and "filter before
    paginating", audit), §7 (levels, routers, the modules table: `spaces`, `space-links`,
    `platform-settings`, `space-settings`, `lookups`), §8 (R1–R8, *Transactions*, *Space access*,
    *Growth*), §9 (*New-space defaults*, *Composed reads*);
  - `docs/backend/security.md` › *Authorization* and *Rate limits*;
  - `docs/architecture/data-model.md`: *Conventions* (bilingual content, soft delete, freshness),
    *Spaces*, *Lookups*, *Derived values* (verified, publicly listed);
  - `docs/api/api-contract.md` §1–§5 (the *Lookups (the admin)* subsection is the pattern to follow);
  - `docs/architecture/shared-package.md`; `docs/development/testing.md` §1–§4;
  - `docs/plans/v1-mvp.md` step 2 and *Planned API surface* (Public directory › `GET /lookups`;
    Admin › spaces);
  - ADR 0007 (soft delete), ADR 0009 (space-scoped roles), ADR 0016 (dashboard URLs);
  - findings 11 (nested writes) and 18 (a link to a deleted space).
- **The designs** (for what the API must serve, not to build): SCREENS.md row 26;
  `docs/design/screens/43-admin-spaces/` frames 01–04 (the list, its filters, "stale only"), 09–10
  (soft delete), 11–16 (edit while unverified, verified read-only, add a space).
- **When finished, follow the `open-pr` skill.**
- **The owner's rules:**
  - honest test titles;
  - **no parameter, option or callback that only tests pass or that nothing uses** — this holds for
    the API too: a service creates its own repository; only real dependencies (the transaction
    runner, the audit writer, lower modules' services) are passed in by the composition root
    (finding 31); logic worth unit-testing lives in pure helpers;
  - **one responsibility per file**; one service / repository / controller per resource (*Growth*);
  - **checks:** lint and typecheck on each commit; the full lanes (`check:classes`, unit,
    component, api, build + `check:build`) once on the head, one at a time; don't re-run a lane that
    already passed on unchanged code;
  - commit subjects of 50 characters or fewer; report only once CI is green on the pushed head;
  - review fixes fold into their commits, with ONE "Review fixes" comment;
  - **rebase only on a real conflict:** if GitHub shows the PR `CLEAN`, don't rebase on `main`;
  - a migration is created once with `--create-only` and checked before it is applied;
  - no tool or AI attribution anywhere.

## 2. What this item delivers

Build step 2's admin spaces, **first of four items** (the owner approved the split):
- **S2b-1 (this item, API):** create an unverified space, the admin's list, one space for the admin,
  edit its profile (basics and location) while unverified, hide and unhide, soft delete; the public
  `GET /lookups`.
- S2b-2 (API): the facts — hours and shifts, prices, amenities, contacts — and confirming each group
  unchanged, designed once for the admin now and the owner in step 5.
- S2b-3 (web): the list and "Add a space" with the map pin. S2b-4 (web): the edit screen.
- **Not in step 2:** photos (step 5 settles them, with the storage port) and linking owners (step 4).

**What exists:** the tables (`spaces`, `space_settings`, `settings` with the seeded
`newSpaceDefaults` and staleness thresholds, the lookups); `spaces` with one call (`summariesFor`,
which already hides soft-deleted spaces); `space-links` (`activeLinksFor`, `mySpaces`); the `/admin`
guard (`requireAuth` + `requireRole('ADMIN')`, mounted once), the audit writer, `parseId`,
`signedIn`, `isUniqueViolation`; the lookups module with its admin router.

**It builds:**
- `POST /admin/spaces`: an unverified space from its basics and location; in **one transaction**, its
  settings row copied from `newSpaceDefaults` (`spaces` reads `platform-settings` and writes through
  `space-settings`, both built minimally here, §9); audited.
- `GET /admin/spaces`: the admin's list, **composed by `space-links`** (§9): the verified filter
  resolves to ids there first, then `spaces` applies the hidden, stale, area and search filters and
  paginates (§5). Each row: the space, its area, its state (verified / unverified / hidden), its
  owner, its stale groups, its last update.
- `GET /admin/spaces/:spaceId`: one space for the admin, with what the edit screen needs.
- Editing the profile (names, descriptions, area, addresses, landmark, location) **only while the
  space is unverified**: `can('space.profile.update')`, fed by the links loader that §8 mounts on the
  admin's space routes **without the refusal** (built here; the refusing `/manage` version comes with
  its first `/manage` space route, not now). Sets `profileUpdatedAt`; audited.
- Hide and unhide (any space), soft delete (any space); audited.
- `GET /lookups` (public): active governorates with their active areas, and active amenities, in
  order, both languages — its first consumer is the space form.
- The contract in `packages/shared` (a `spaces` capability, and the public lookups read).
- The documents: api-contract.md §5 (and §4 if anything is unpaginated), data-model.md (the name
  rule), the status lines of conventions.md and security.md, `v1-mvp.md`'s "Built" lines, findings 11
  and 18 resolved.

## 3. The proposed decisions

These came out of the analysis and the owner approved them, **but they are proposals, not orders.**
You know the code best: if you find a stronger option for any of them, put it in your plan under a
dedicated section, **"Proposed alternatives"**, with its trade-off and your recommendation. The owner
and the analyst weigh it; build an alternative only once it is approved.

- **S1 — the name rule flips: the English name is required, the Arabic optional** (most spaces are
  known by an English name). A migration on `spaces` (`name_en` not null, `name_ar` nullable);
  data-model.md's bilingual rule gains this exception for a space's name; the seed and demo data
  follow. The descriptions and addresses keep their current rules unless your plan shows a reason.
- **S2 — the slug** is derived from the English name (kebab-case, Latin letters and digits), with a
  numeric suffix on a collision (`focus-hub-2`), **soft-deleted spaces included** (a slug is never
  reused); it never changes after creation.
- **S3 — the location is required at creation:** the admin places the pin before saving. The server
  refuses a point outside the Gaza Strip's bounding box, with a sensible margin so spaces at the edges
  are not refused (422 on the location field).
- **S4 — the admin's list is paginated** as api-contract §4 says (§9 names its pagination).
- **S5 — `GET /lookups` is built now,** public, active rows only, unpaginated (a bounded catalogue;
  record it beside the admin lookups' exception in §4).
- **S6 — a link to a soft-deleted space no longer counts** (resolves finding 18): the session's links
  and the user's spaces leave out deleted spaces, through `spaces`' own `summariesFor`; deleting a
  space writes nothing in `space_managers`, so it stays reversible.
- **S7 — the admin may hide, unhide and soft-delete any space,** verified or not (the plan says
  "any space"); only the profile and facts are limited to unverified spaces.
- **S8 — "stale" is computed on the server** from the platform's thresholds (`stalenessDays`,
  `priceStalenessDays`), per fact group; the list returns each row's stale groups, and its "stale
  only" filter uses the same rule. Photos count in no group yet.
- **S9 — the admin's and the owner's edits are separate endpoints** (`/admin/spaces/:spaceId…` now,
  `/manage/spaces/:spaceId…` in step 5) **over one service logic**, with `can()` deciding; this item
  builds only the admin's.

**Fixed by the documents** (flag any you find no longer holds):
- `spaces` (L1) owns its tables; `space-links` (L2) composes the admin's list; `platform-settings` and
  `space-settings` are L0; no module imports a higher level or its own level (R3);
- a space's settings row is created with the space, copied from the defaults, in the same
  transaction; changing a default never touches existing spaces; the four governed settings have no
  database default;
- verified = an active `OWNER` link; the admin edits facts only while a space is unverified, and
  `spaces` never imports `space-links` for that (the links loader puts the links on the request);
- soft delete is `deletedAt`; publicly listed requires not deleted, not hidden, and an active area and
  governorate;
- every write audited in its own transaction; no idempotency key (not a desk create);
- the first nested write (the space with its settings) is where finding 11 is resolved.

## 4. Your plan decides

- the endpoints' exact shapes within the planned paths (for example hide/unhide inside the `PATCH`
  or as their own route), the list's query parameters and row shape, the admin's one-space shape;
- the module files per resource, the minimal `platform-settings` and `space-settings` surfaces (only
  what this item uses), and how the composed read passes ids between modules;
- the slug helper and the Gaza bounds (as pure helpers, unit-tested);
- how finding 11's warning is avoided, and how the test proves it;
- the audit action names (stable) and payloads;
- the migration (checked with `--create-only` before it is applied) and its effect on the seed;
- the tests, per testing.md:
  - **every protected endpoint as a guest, a USER, an OWNER of another space, the OWNER of this
    space, and the ADMIN** (testing.md §4), and an admin with a pending password change;
  - the composed list: each filter, the verified filter before pagination (full pages, right totals),
    a deleted space absent, the stale groups;
  - creation: the defaults copied in the same transaction (and nothing written when they can't be),
    the slug and its collisions (deleted spaces included), the bounds;
  - the profile edit refused on a verified space; hide, unhide, delete; the audit entries;
  - finding 18: a link to a deleted space gone from the session and the user's spaces;
  - `GET /lookups`: active rows only, in order;
- the commits (a sketch: the name rule and the public lookups; the space's creation with its
  settings; the admin's list; the profile edit, hide and delete with the links loader).

## 5. Out of scope

- Any web file (S2b-3, S2b-4). Photos and the storage port. Linking and unlinking owners (step 4).
- The facts (hours, shifts, prices, amenities, contacts) and confirming a group (S2b-2).
- The refusing space middleware on `/manage`, `optionalAuth`, the directory.
- New dependencies. If you think one is needed, stop and ask.

If the plan finds the documents missing something this item needs, or a decision that can't hold,
stop and report: record it, don't absorb it.

## 6. Parallel work

Another worker may be working in its own worktree at the same time.
- **Declare in your plan every shared file you will edit** (for example `apps/api/src/app.ts`,
  api-contract.md, the status lines of conventions.md and security.md, data-model.md, `v1-mvp.md`,
  `findings.md`), and edit each minimally, in your own section.
- Number any new finding after the last one on `main` when you start; if a conflict appears later,
  the PR is rebased then, keeping both sides.
- **This item changes the schema:** after the merge, the migration is applied to the other worker's
  database too (the analyst does that); say in the PR what it changes.

## 7. Pull request

- **Title:** `feat(spaces): add the admin's spaces API` (or the main commit's subject).
- **Labels:** `feat`, `area:api`, `area:docs`. Assigned to the owner.
- **The description:** scope, acceptance criteria and out of scope; the decisions S1–S9 and any
  alternative approved; the migration; evidence per lane; what was not run.
- **Review:** the independent review gate, after you report.
- After CI is green on the pushed head, stop and report: the head, the commits, the counts per lane,
  your tokens. Don't merge. Don't create an Issue.
