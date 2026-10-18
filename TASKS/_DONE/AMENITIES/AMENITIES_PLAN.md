# AMENITIES — no amenity filter, and a space's own amenities

> **Approved 2026-10-12** (`AMENITIES_PLAN_REPLY.md`).
> - **Base:** `main` is now `4ce6310`, with #62 merged, so the branch is cut from it. The shared documents carry #62's lines: build on them. There is no fast-path conflict left, and the only other open PR is #61 (`docs/design/` only).
> - **The owner's answers (§13):** names approved; caps 20 × 1–60 approved; S1–S6 approved; the glossary's Arabic for an *own amenity* is **«مرفق إضافي»**, not «مرفق خاص»; design issue 1 (remove the card's line) approved; the Combobox comment approved.
> - **Addition 1:** the contract's line for `PUT …/amenities` says that the audit's shape changed (`{ amenityIds }` → `{ amenityIds, ownAmenities }`) and that older entries keep the old shape.
> - **Addition 2:** a third commit, `chore(users): name both locks in changeRole`. The doc comment of `changeRole` in `apps/api/src/modules/users/users.service.ts` names both `lockAccount` and `lockForAdminChange`, and nothing else in `users` changes. The PR description says it is #62's leftover and carries `Closes #63`.
> - **The report** says that the design archive still draws an amenity filter.

Worker: the amenities task worker · worktree `C:\Users\basel\masaha-amenities` · branch `feat/space-own-amenities` (cut after approval) · DBs `masaha_amenities_dev` / `_test` · API 3322, web 5322.

## 1. Summary

The owner reopened the amenities on 2026-10-12. Every space claims fast internet and stable power, and nobody looks for a space by its hot drinks, so **amenities stop being a filter**. The flag `amenities.is_filterable` is removed from the database, the API, `@masaha/shared/lookups`, the seed, the admin's lookups screen and the documents, and the directory's planned `amenities` filter is removed from the scope and the plan.

The item also adds **a space's own amenities**. Beside the platform's common list, which stays the admin's, a space keeps its own amenities as short bilingual texts. They are part of the amenities fact group: saved whole with the platform ids on the one save path, then dated, audited and confirmed as the group is today.

## 2. Contract

**Scope**
- D1: the filter flag goes everywhere. One migration drops the column. The flag leaves the shared requests and responses, the admin's amenity endpoints, the public catalogue, the mappers and repositories, and the seed. On the web's amenities tab, the «In filters» switch, its badge, its hook, its copy (both catalogues) and its tests go. The documents follow.
- D2: a new table holds a space's own amenities: Arabic name required, English optional, an order, and a cascade from the space. `PUT /admin/spaces/:spaceId/amenities` takes `{ amenityIds, ownAmenities }`, both replaced whole. `AdminSpace` answers `ownAmenities` in order. The audit entry and the no-op rule cover the whole group.

**Acceptance criteria**
- [ ] `GET /lookups`, `GET/POST/PATCH /admin/amenities` neither answer nor store a filter flag; the column is gone (migration applied clean on an empty DB).
- [ ] The amenities tab shows no «In filters» switch, badge or sheet switch; the Active switch, names, icon and order work as before.
- [ ] An amenities save stores the platform set and the own amenities in their order, dates the group, audits `space.amenitiesEdited` with `{ amenityIds, ownAmenities }` before and after.
- [ ] A save that changes nothing writes nothing (no date, no audit), unless the group is missing; a changed order of own amenities is a change.
- [ ] An Arabic name repeated is `422`, `not_unique` on `ownAmenities.<i>.nameAr`, in both apps' shared rule, and refused by the database's key.
- [ ] Caps: at most 20 own amenities, each name 1–60 characters, under the user-text rule (`textSchema`).
- [ ] Confirm, the 403 on a verified space, the 404 on a soft-deleted space behave as for every group.
- [ ] Documents updated (§7 below); every lane and check green locally and in CI.

**Out of scope:** any screen (the editor, the space page); the public directory API (step 3); the owner's endpoints (step 5, D4); photos; the design archive (`docs/design/`).

## 3. Reading done

CLAUDE.md, workflow, the map, the findings index. `features/lookups.md` (all) and `features/spaces.md` (*Behaviour*, *Decisions*). Data model › *Conventions*, *Lookups*, *Spaces*. API contract §1–§4, *Lookups (public)*, *Lookups (the admin)*, *Spaces (the admin)*, §6. Conventions §2–§8 and §13. Testing §1–§4. `shared-package.md`. The overview. The plan's `GET /spaces` and `PUT /manage/spaces/:spaceId/:group` rows. The glossary.

Code read:
- the API: the schema; `lookups/amenities`, `catalogue/` and `lookupChange.ts`; `spaces/amenities`, `facts/` (`groupEdit.ts`, `facts.ts`), `contacts/` (the replace-whole pattern), `confirm/`, `space/` (the mapper, the view, the space test's group table and its lock tests); the seed and its test;
- `packages/shared`: `lookups/` and `spaces/requests.ts` / `responses.ts`;
- the web: `features/lookups` (the amenity row, form, section, `RowControls`, mutation keys, failure hooks and tests), both copy catalogues, and `pages/dashboard/routes.component.test.tsx`;
- the open PRs' file lists, #61 and #62.

## 4. Settled decisions, as built

**D1 — no amenity filter.**
- **The database:** migration `…_no_amenity_filter` runs `ALTER TABLE "amenities" DROP COLUMN "is_filterable"`, and the field leaves `Amenity`. The old migration that added it stays as history.
- **Shared:** `isFilterable` leaves `createAmenitySchema`, `updateAmenitySchema`, `AdminAmenity` and `CatalogueAmenity`. A request that still sends it is parsed with the key stripped, which is Zod's default.
- **The API:**
  - the amenities repository's select and `NewAmenity` lose the field, and so do both mappers and the catalogue repository's select;
  - the audit (`lookupChange`) is generic and needs no change.
- **The seed:** `isFilterable` leaves `AmenitySeed` and its two entries, the comment goes, and the seed test that counted the unfiltered amenities is removed.
- **The web (`features/lookups`):**
  - delete `hooks/filter/useSetAmenityFilter.ts`;
  - `mutationKeys.ts` loses the `'amenityFilter'` kind;
  - `useAmenityRow` loses `setFilter`, `notFiltered`, `notFilteredLabel` and `switches`;
  - `AmenityRow` loses the badge;
  - `useAmenityForm` and `AmenityFormView` lose `isFilterable` and `filter`, so `toggle` serves `isActive` only;
  - `AmenityForm` loses the switch's `Field`;
  - `useAddAmenityForm` and `useEditAmenityForm` lose the default;
  - the comments in `useAmenityRowFailure` and `useAmenityListFailure` say "its switch".
- **Copy (en and ar):** `amenities.description`, `row.notFiltered`, `row.inFilters`, `row.inFiltersName`, `sheet.inFilters` and `sheet.inFiltersHint` go. `sheet.amenityActiveHint` becomes "Inactive: not offered in forms; spaces that have it keep it." / «غير نشط: لا يظهر في النماذج، وتحتفظ به المساحات التي لديها.».

**D2 — a space's own amenities.**
- **Schema:**

  ```prisma
  model SpaceOwnAmenity {          // @@map("space_own_amenities")
    id, spaceId, nameAr String, nameEn String?, sortOrder Int @default(0), createdAt, updatedAt
    space Space @relation(..., onDelete: Cascade)
    @@unique([spaceId, nameAr])    // its prefix serves the list; as SpaceShift
  }
  ```

  `Space` gains `ownAmenities SpaceOwnAmenity[]`. Migration `…_space_own_amenities`.
- **Shared (`spaces/requests.ts`):**
  - `MAX_OWN_AMENITIES = 20` and `OWN_AMENITY_NAME_MAX_LENGTH = 60`, the length of a platform amenity's name;
  - `ownAmenity = { nameAr: textSchema(1,60), nameEn: optional(textSchema(1,60)) }`;
  - `updateSpaceAmenitiesSchema = { amenityIds (as today), ownAmenities: z.array(ownAmenity).max(20) }`, with `refuseRepeats(ctx, 'ownAmenities', …, () => 'nameAr', (o) => o.nameAr)` beside the id repeat.

  `textSchema` is the user-text rule both apps run: NFC, trimmed, no bidi or control characters.
- **Shared (`responses.ts`):** `OwnAmenity { nameAr: string; nameEn: string | null }`, and `AdminSpace.ownAmenities: OwnAmenity[]` in order, after `amenityIds`. It carries no id, as prices and contacts carry none, because nothing refers to it.
- **The API:**
  - a new `spaces/amenities/ownAmenities.repository.ts`, beside `amenities.repository.ts` as `shifts.repository.ts` sits in `hours/`. It has `listFor(spaceId, tx)`, by `sortOrder` then `id`, and `replace(spaceId, list, tx)`, which runs `deleteMany` then one `create` at a time (finding 11), as contacts do;
  - `facts.ts`: `SpaceFacts` and `NO_FACTS` gain `ownAmenities`, read in sequence under the caller's `tx`, so the space's share-locked read covers them;
  - `space.mapper.ts` answers `ownAmenities`.
- **`amenities.service.ts`:**
  - it reads the platform set and the own list under the lock;
  - when the group is dated, the set is unchanged and the own list is deep-equal in order (with `nameEn` set to `null`), it answers `null`, so nothing is written;
  - otherwise the retired-amenity check runs as today, the platform links are diffed as today, and the own list is replaced only when it differs;
  - the audit's `before` and `after` are `{ amenityIds (by id), ownAmenities: [{ nameAr, nameEn }] }`, the whole group, and a missing group's `before` is `{ amenityIds: [], ownAmenities: [] }`.
- **Unchanged:** `groupEdit` (the lock, `can()` from the links under the lock, the date, the audit), `confirm`, the routes and `app.ts`.

**D3:** the platform's list stays the admin's; only the flag goes. **D4:** no owner endpoint; the save path above is the one `PUT /manage/...` will reuse.

## 5. Stronger decisions

- **S1. `ownAmenities` is required in the body, never defaulted to `[]`.**
  - *Why:* the group is saved whole. A client that does not know the field, such as a later screen or a script sending `{ amenityIds }` alone, would silently erase the space's own amenities. Answering 422 `required` says so.
  - *Cost:* none, since no client calls the endpoint yet.
  - **Recommend: yes.**
- **S2. The database refuses a repeated Arabic name too (`@@unique([spaceId, nameAr])`), not only the shared rule.**
  - *Why:* the same guarantee as the shifts. The key's prefix also serves the list, so no other index is needed.
  - *Cost:* none.
  - **Recommend: yes.**
- **S3. Remove the `switches` slot from `RowControlsView` and `RowControls`.**
  - *Why:* the filter switch was its only user. An empty extension point is code nothing uses.
  - *Cost:* two files in `features/lookups`, with the comment trimmed.
  - **Recommend: yes.**
- **S4. Should an own amenity whose Arabic name equals a platform amenity's be refused ("tick it instead")?**
  - *Why it would help:* it steers owners to the common list.
  - *Why not:* an exact match catches little (spelling varies), and `spaces` would read names from `lookups` inside the save. The later editor shows both lists side by side, so a repeat is seen where it is made, the reasoning of finding 30.
  - **Recommend: no.**
- **S5. Two migrations, one per commit, rather than one.**
  - *Why:* each commit is one working unit with its own schema change.
  - *Cost:* the create-only step runs twice, once per migration, each followed by an `ls`.
  - **Recommend: yes.**
- **S6. The glossary gains *Amenity* (مرفق).**
  - *Why:* the glossary owns the vocabulary, and the code now names a new concept, `ownAmenities`.
  - *What it says:* a feature a space offers, either one of the platform's common amenities (a lookup), ticked, or one of the space's own, typed by it (*own amenity*, «مرفق إضافي», the owner's answer).
  - **Recommend: yes.** The Arabic wording is the owner's (Q4).
- **No ADR:** `lookups.md` and `spaces.md` naturally own these decisions (documentation §7).
- **Nothing in the documents is weakened.** The decision of #16 is superseded by the owner's decision, which is recorded as it now holds.

## 6. Related findings

No open finding touches the amenities, the lookups or the facts:
- 44, 46, 49 and 50 concern other spaces and owners matters;
- 30 (accepted) informs S4 and the rule that a repeated English name is allowed.

Nothing is folded. Finding numbers 53 and 54 are reserved; none is planned. The design archive still draws an amenity filter, but it is a frozen record kept by the design fixer, so it goes in the report and not in a finding.

## 7. Files

**The API layer, mine:**
- `apps/api/prisma/schema.prisma` and two new migrations;
- `modules/lookups/amenities/{repository,mapper}.ts` with `amenities.api.test.ts`;
- `catalogue/{repository,mapper}.ts` with `catalogue.api.test.ts`;
- `lookupChange.unit.test.ts`, test data only;
- `modules/spaces/amenities/{service.ts, ownAmenities.repository.ts (new), amenities.api.test.ts}`;
- `facts/facts.ts` and `space/space.mapper.ts`;
- `space/space.api.test.ts`: only the group table's amenities body and the read's `toEqual`. #62 edits the same file near line 443, which is no overlap;
- `space/create.api.test.ts`;
- `db/seed/lookups.ts` and `seed.api.test.ts`.

**Shared:**
- `packages/shared/src/lookups/{requests,responses,requests.unit.test}.ts`;
- `spaces/{requests,responses,requests.unit.test}.ts`.

**The web, under workflow §9's licence for what a shared type breaks:**
- `apps/web/src/features/lookups/…`, the files listed under D1 and S3, and their tests: `AmenitiesSection`, `AmenitySheet`, `useAddAmenityForm`, `useEditAmenityForm`, `useAmenitiesSection`, `useAmenityRow` and `lookupsRepository`;
- `shared/copy/{english,arabic}/lookups.ts`;
- `pages/dashboard/routes.component.test.tsx`: the fixture's flag only.

**Outside `features/lookups`, declared for approval:**
- `shared/design-system/components/fields/Combobox/Combobox.tsx`: a comment only. "such as the area or amenity filters" becomes "such as the area filter". It belongs to worker A's layer: one line, with low conflict risk.

**Documents:**
- `docs/api/api-contract.md`, shared with #62, my sections only:
  - *Lookups (public)* and *Lookups (the admin)*: the flag goes;
  - *Spaces (the admin)*: `AdminSpace`, `OwnAmenity` and `PUT …/amenities`, with its body, caps, audit and errors.
- `docs/architecture/data-model.md`:
  - the Amenity entry loses the flag;
  - a new **SpaceOwnAmenity** entry;
  - the cascade list in *Soft delete* gains own amenities.
- `docs/features/lookups.md`:
  - *Behaviour* and the switches;
  - *Responsibility boundary*;
  - *API decisions*: #16's line is replaced by "No amenity is a filter", 2026-10-12, with the owner's reason and #16 named as superseded;
  - *Web decisions*: the two-switches line;
  - both histories.
- `docs/features/spaces.md`:
  - *What it does*, *Owns*, and *Behaviour* › *Amenities*;
  - the API decisions on own amenities (S1, S2, caps, the no-op, the audit);
  - the code map and the API history.
- `docs/backend/conventions.md` §7, the modules table: `spaces` owns `space_own_amenities`. #62 edits §13 only.
- `docs/project/overview.md`, shared with #62:
  - the *Directory* line drops "the amenities that tell spaces apart";
  - the *Spaces* line in *Built* names the own amenities. #62 edits the *Users* line three lines above, a likely conflict that the fast path resolves.
- `docs/plans/v1-mvp.md`: the `GET /spaces` row drops `amenities`. It is shared with #62; my row only.
- `docs/frontend/design-system/foundation.md`:
  - §11's Select/Combobox row drops "amenity filter";
  - §13's *Directory* filters line drops the amenities.
- `docs/project/glossary.md` (S6).
- The root `README.md`, line 49: the scope as designed drops "the amenities that tell spaces apart".

**Boundaries:**
- nothing in `shared/auth`, `users`, `space-links`, `core/errors.ts`, the catalogues' `errors.ts`, `app.ts`, `test/*.ts` or `docs/design/`;
- no dependency.

## 8. Design issues (the lookups screen changes)

1. **The amenities card's line under its title only explained «In filters».** Remove it, so the card is its title and «Add amenity», as the governorates' card is.
   - *Alternative:* a new line, "The common amenities a space ticks; a space adds its own beside them". It would describe an editor that does not exist yet.
   - **Recommend: remove.**
2. **The row keeps one switch, Active, with its words beside it.** No other change; the layout already wraps.

## 9. Tests, each seen failing first, with the break it catches

**Unit (`packages/shared`)**

| # | Test | Break |
|---|---|---|
| U1 | `updateSpaceAmenitiesSchema` takes `amenityIds` and `ownAmenities` in order, the English optional (absent or `null`) | `ownAmenities` dropped, or `nameEn` required |
| U2 | Refuses an Arabic name repeated, at its repeat: `ownAmenities.2.nameAr: not_unique` | the `refuseRepeats` call removed |
| U3 | 21 → `ownAmenities: too_long`; a 61-character name → `too_long`; empty → `too_short`; a bidi control → `invalid_format` | caps changed, or `z.string()` used instead of `textSchema` |
| U4 | A body without `ownAmenities` → `required` (S1) | `.default([])` or `.optional()` |
| U5 | `createAmenitySchema` parses to `{ nameAr, nameEn, icon }` only; the old `isFilterable: ['required']` test is removed | the flag kept in the schema |

`lookupChange.unit.test` changes its sample fields only; it is unchanged in kind.

**API integration**

| # | Test | Break |
|---|---|---|
| A1 | `POST /admin/amenities` answers and audits without the flag; `PATCH` edits names and icon without it (exact `toEqual`) | the mapper or select keeps the field |
| A2 | `GET /lookups` amenities are exactly `{ id, key, nameAr, nameEn, icon }` | catalogue mapper |
| A3 | Amenities save: the platform set plus two own amenities, in order; dated now, other groups' dates untouched; answered in order | `sortOrder` not written or not read in order |
| A4 | `GET /admin/spaces/:id` answers `ownAmenities` in order | the facts reader omits them |
| A5 | The audit's before and after hold `{ amenityIds, ownAmenities }`, the whole group | the audit records ids only |
| A6 | Saved again unchanged: no date, no audit. Reordered own amenities: written and audited | compared as a set, or always written |
| A7 | A repeated Arabic name: 422 on `ownAmenities.1.nameAr`, nothing written | the route validates another schema |
| A8 | Only the own list changes, the platform set kept: written | the no-op test looks at the ids only |
| A9 | The existing tests (first save with none, 403 when verified, 404, retired kept) carry `ownAmenities: []`; the 403 test also asserts no own amenity stored | — |
| A10 | `space.api.test` group table: the amenities body includes an own amenity, so a refused caller's "nothing changed" can fail; the read and create answers expect `ownAmenities: []` | — |
| A11 | Seed test: the filter test is removed | — |

**The lock and the date, proven as for every other group.** They are `groupEdit`'s, already proven:
- the lock by the hours test for finding 43 and by the read test;
- the date per group by each group's test, where A3 and A6 cover the amenities.

**Make the break (rule 7):**
- `ownAmenities.replace` run outside `tx` (with `prisma`), seen failing on the 403 test (A9), then restored;
- the no-op reading set equality, seen failing on A6, then restored.

**Component (web), each test edited to the new expectation first, seen failing, then the code**

| # | Test | Break |
|---|---|---|
| W1 | `AmenitiesSection`: a row's text is names plus the Inactive badge only ('InternetإنترنتInactive…', and in Arabic); the only switch is «Active: Internet» | badge or switch left in place |
| W2 | "Turns a switch by its words" and "keeps the keyboard on a switch that waits" are retargeted to the Active switch | — |
| W3 | `AmenitySheet`: no «In filters» switch; the add form sends `{ nameAr, nameEn, icon }` (`useAddAmenityForm`) and the edit form sends no flag (`useEditAmenityForm`) | the form keeps the flag |
| W4 | `useAmenityRow`: the controls have no `switches`; `useAmenitiesSection` has no description | — |
| W5 | `lookupsRepository.unit`: the `editAmenity` body test uses `{ icon }` | — |

## 10. Review Focus (no planned test exercises these)

- A PATCH or POST that still sends `isFilterable`: it is stripped by Zod and changes nothing. Not tested.
- The cascade of `space_own_amenities` when a space row is hard-deleted: never done by the app; the schema relation only.
- The database key on `(space_id, name_ar)` is unreachable through the API, since the shared rule refuses first.
- Arabic names that differ only by spacing or diacritics count as different names, because `textSchema` trims and NFC-normalises but does not fold diacritics.
- The migration on a database whose amenities have filter flags set: the data is dropped by design.

## 11. Commits

1. `feat(lookups): drop the amenity filter`: migration 1, schema, shared lookups, the lookups API, the seed, the web's lookups feature and copy, the Combobox comment, all their tests, and the documents of D1: `lookups.md`, the contract's lookups sections, the data model's Amenity, the overview's *Directory*, the plan's `GET /spaces`, `foundation.md` and `README.md`.
2. `feat(spaces): keep a space's own amenities`: migration 2, schema, shared spaces, the spaces API (repository, service, facts, mapper), its tests, and the documents of D2: the contract's spaces sections, the data model, `spaces.md`, conventions §7, the glossary and the overview's *Built*.

Lint and typecheck run on each commit. Review fixes are folded later by fixup.

## 12. Verification (phase 4)

- **Migrations:**
  - `npx prisma migrate dev --create-only --name no_amenity_filter`, once, then `ls`; then the second migration the same way;
  - `migrate deploy` to `masaha_amenities_dev` and `_test`;
  - a clean run on a scratch database `masaha_amenities_scratch`, created in `masaha-postgres-1` with `createdb`, then `migrate deploy`, then `dropdb`. Never `db:up`.
- **Then:** `npm run build -w @masaha/shared`.
- **One at a time on the head:** `test:unit`, `test:component`, `test:api`; `NODE_ENV=production npm run build`, `check:build`, `lint`, `typecheck`, `check:classes`, `format:check`, `check:links`.
- **Real requests on 3322**, each in the report:
  - `GET /lookups` without the flag;
  - `POST` and `PATCH /admin/amenities` without it;
  - a space's amenities saved with two own amenities, read back in order, confirmed, and saved again unchanged (the audit count unchanged);
  - a repeated name refused.
- **The web on 5322:** the amenities tab at 390 and 1440, in RTL and LTR, light and dark. Screenshots go to `C:\Users\basel\Downloads\amenities-shots\`, never committed.
- **Afterwards:** stop the servers by PID and check that ports 3322 and 5322 are free.
- **Not run:** E2E, which is end of project.

## 13. Decisions needed from the owner

1. **Names:** `ownAmenities` / `OwnAmenity` / `SpaceOwnAmenity` / `space_own_amenities`.
2. **Caps:** at most 20 own amenities, each name 1–60 characters.
3. **S1–S6 as recommended:** `ownAmenities` required, a database key, the `switches` slot removed, no refusal of a platform amenity's name, two migrations, and a glossary row.
4. **The glossary's Arabic for an own amenity:** «مرفق خاص»?
5. **Design issue 1:** remove the amenities card's line.
6. **The licence for the one-line Combobox comment** in `shared/design-system`, worker A's layer.
