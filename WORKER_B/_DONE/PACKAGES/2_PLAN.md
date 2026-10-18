# PACKAGES — the owner's packages API (step 5b): a space's subscription templates, private to its staff

> **Approved by the owner, 2026-10-18 — binding on the executor:**
> - **S1 approved:** the name refusal is `AppError.conflict(undefined, 'Package name taken', { name: ['not_unique'] })`
>   → **409**, `errors.name = ["not_unique"]`. So T5 and T15 expect 409, Appendix A's *If S1 is not
>   approved* lines are **not** written, and **`docs/architecture/data-model.md` is not edited** (A.5 drops).
> - **S2 approved** (no cap beyond the Int column) and **S3 approved** (the read takes no lock).
> - **The precondition is met:** PR #85 merged (`5e8c979d`). §12.1's `git diff --name-status 44b8ac7b
>   origin/main` will list #85's files — re-read the shared documents it names; stop only on a §7 code file.
> - **The frozen folders:** read `DECISIONS_OWNER.md` from `D:\masahaWorkspace\DESIGN\DECISIONS\` and
>   #86's review from `D:\masahaWorkspace\WORKER_B\_DONE\HARDEN\REVIEW86_OPENCODE_REPORT.md` (the same
>   files as the `C:\Users\basel\.prompt\…` paths in §3, which are frozen). Write nothing outside the
>   repository except this folder's `4_REPORT.md`.
> - **The PR number:** the highest issue/PR is #86 today; worker A's OWNERS may open first — §12.7 checks.
> - **Amended 2026-10-18 (the executor's stop at R6):** an absent `billing` or `audience` answers
>   **`invalid_choice`**, not `required` — the shared `toFieldErrors` maps an enum's failure, absent or not,
>   to `invalid_choice`, as the prices' `period` and `audience` already answer (api-contract, `PUT …/prices`).
>   R6 expects `invalid_choice` on those two fields (and `required` on the others); Appendix A's terms
>   lines say "from their lists (`invalid_choice`)", as the prices' line does. `fieldErrors.ts` is not touched.
>   **The same holds for R8** (a PATCH's `null` on `billing`/`audience` → `invalid_choice`) — confirmed by the
>   owner after the review, 2026-10-18.

**Work Item:** PACKAGES · **Worker:** B · **Planner:** Claude Code, 2026-10-17, from `origin/main` = `44b8ac7b`
**Runs:** only after PR #85 (GALLERY, worker A) has merged, from the latest `origin/main`
**Branch:** `feat/space-packages`, cut with `--no-track` from the latest `origin/main`, in `C:\Users\basel\masaha-b`
**Ports / databases:** API 3321, web 5321 (not used) · `masaha_b_dev`, `masaha_b_test` in `masaha-postgres-1`
**Plan:** `D:\masahaWorkspace\WORKER_B\PACKAGES\2_PLAN.md` · **Report:** `D:\masahaWorkspace\WORKER_B\PACKAGES\4_REPORT.md` (UTF-8, written in parts) · no screenshots (API only)
**Executor:** any capable coding agent. This plan stands alone: no step depends on a Claude skill (Appendix B
is only a map). The planner ran nothing; where it could not be sure something works, the step is a
**check the executor makes first, with what to do if it fails** (§12.2).

**Placeholders**, and no others: `#PRNUM` (the PR's number, replaced just before the push, §12.7),
`<today>` (the date the line is written, `YYYY-MM-DD`), and, in Appendix A.2 only, `{the name refusal}`
(its words in the contract, given there).

**The name refusal** — one term used throughout, fixed by the owner's answer to S1 (§5, §13):
- **default (S1 not approved, the prompt's D3):** `AppError.validation({ name: ['not_unique'] })` → 422,
  `type: 'validation'`, `errors: { name: ['not_unique'] }`;
- **if S1 is approved:** `AppError.conflict(undefined, 'Package name taken', { name: ['not_unique'] })` → 409,
  `type: 'conflict'`, `errors: { name: ['not_unique'] }`.

---

## 1. Summary

Builds the `packages` module (conventions §7: L2, table `packages`, router *manage*) on the existing
table: `GET /manage/spaces/:spaceId/packages` for the space's staff (every package, retired ones
included, whole), and `POST …/packages` and `PATCH …/packages/:packageId` for its owner. A new shared
capability, `@masaha/shared/packages`, holds the request schemas (a price above zero), the billings and
the response type. Writes take the space's lock through `spaces`, decide `can('packages.manage')` on the
links read under it (and first at the route, through `requireCan`), and audit `package.created` /
`package.edited`. A taken name is refused on its field by the database's key in the write's own
transaction; a shift that is not the space's is refused by the database's composite key. A new
capability document, `docs/features/packages.md`, and the contract, security, conventions, plan,
overview, map and `spaces.md` lines follow. Findings 77–79 (from #86's review) and 80 (the database
still takes a free package) are recorded. No schema change, no migration, no dependency, nothing in
`apps/web`.

## 2. The contract

### Scope
- `@masaha/shared/packages`: `createPackageSchema`, `updatePackageSchema`, `SUBSCRIPTION_BILLINGS`, the
  bounds, `SpacePackage`.
- `apps/api/src/modules/packages/`: service, repository, mapper, a pure rule file, controller, manage
  router; wired and mounted in `app.ts` under `/manage/spaces/:spaceId/packages`.
- Tests in the unit lane (shared schemas; the pure rule) and the API lane (the endpoints).
- Documents: §7 and Appendix A. Findings 77, 78, 79, 80.

### Acceptance criteria
- [ ] `GET …/packages` answers an active `OWNER` or `RECEPTION` link of the space `SpacePackage[]`: every
      package of the space, retired ones included, by place then name, with no `meta`; anyone else 404.
- [ ] `POST …/packages` (owner) creates an active package placed after the last, audited
      `package.created`; reception gets 403 before its body is validated; a price of 0, a limit out of
      range or a bad choice is a 422 on its field; a name another package of the space holds (retired
      or not) is the name refusal; a shift that is not the space's is 422 `invalid_choice` on `shiftId`.
- [ ] `PATCH …/packages/:packageId` (owner) is partial (`null` clears a limit or the shift, `isActive`
      retires or offers again), writes and audits `package.edited` with only the changed fields, writes
      nothing for a patch that changes nothing, and answers 404 for a package that is not the space's.
- [ ] Every write takes the space's lock first and decides on the links read under it: an owner
      unlinked meanwhile is refused, a space deleted meanwhile is `not_found`.
- [ ] No public route reads `packages` (D7).
- [ ] The documents of Appendix A, `docs/features/packages.md` born from the template; findings 77–80
      recorded and indexed.
- [ ] No schema, migration or dependency change; no file in `apps/web`.
- [ ] Every new test seen failing first; every break of §12.5 made, its red output in the report.
- [ ] CI green on the pushed head; GitHub `CLEAN`.

### Out of scope
Every web screen; capacity and the stay limit (O2); staff (step 6); subscriptions and the desk's picker
(steps 7–8); the database's `packages_price_check` (finding 80); a reorder route; a `DELETE`; an
idempotency key; the glossary/foundation §13 #21 wording of *Rules changed* ("week and month prices also
serve as packages at the desk") — not this item's; the fixes of findings 77–79.

## 3. The reading done

`CLAUDE.md`; `docs/development/workflow.md` (whole); `docs/development/testing.md`; `docs/README.md`
(the map, *Deferred documents*: only the contract's *Endpoints*); `docs/architecture/documentation.md`
(§5 the template); `docs/backend/conventions.md` (whole); `docs/backend/security.md`;
`docs/api/api-contract.md` (whole); `docs/architecture/data-model.md`; `docs/architecture/shared-package.md`;
`docs/development/engineering-principles.md`; `docs/development/setup.md` (second folder, the API, its
test lane); `docs/plans/v1-mvp.md` (step 5, *Planned API surface*); `docs/project/overview.md`;
`docs/features/spaces.md` and `docs/features/lookups.md` (the template in use); ADR 0009, ADR 0010;
the findings index and finding 63; `C:\Users\basel\.prompt\MASAHA_DESIGN\DECISIONS_OWNER.md` (DI-10,
O6, O8, *Rules changed*); `docs/design/prototype/Packages.html` (the sheet O8 describes);
`C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\REVIEW86_OPENCODE_REPORT.md` (findings 77–79); the
last accepted plan's procedure (`D:\masahaWorkspace\WORKER_B\_DONE\HARDEN\HARDEN_PLAN.md` §12).

Code on `origin/main`: `schema.prisma` (`Package`, the enums), migration `20260929120200_front_desk`
(the packages table, its keys and CHECKs) and `20261012144622_space_price_above_zero`; `app.ts`;
`shared/auth/` (`can.ts`, `requireCan.ts`, `spaceAccess.ts`, `spaceLinks.ts`, `index.ts`);
`shared/audit/writeAudit.ts`; `shared/errors/appError.ts`, `errorHandler.ts` (maps no Prisma code);
`shared/http/sendSuccess.ts`; `shared/validation/parseId.ts`; `db/` (`transaction.ts`,
`uniqueViolation.ts`, `foreignKeyViolation.ts`, `index.ts`); `modules/spaces/` (`index.ts`,
`spaces.service.ts`/`.repository.ts` with `lock`, the managed routers, `prices/`, `facts/groupEdit.ts`,
`hours/shifts.repository.ts`, `photos/photos.service.ts`, `profile.ts`, `space/space.service.ts`);
`modules/lookups/` (`governorates/`, `lookupChange.ts` and its test); `modules/space-links/`
(`index.ts`, routes, `linksAt`, `adminOwners` lock, `adminSpaces.ownersFor`); `modules/users/`
(`namesFor`); `packages/shared/` (`package.json`, `core/fields.ts`, `core/fieldErrors.ts`,
`spaces/requests.ts`, `responses.ts`, its unit test); `eslint.config.js` (the level map: `packages` is
L2 for the API and the shared package); `apps/api/test/` (`locks.ts`, `admin.ts`, `spaces.ts`,
`factories.ts`), `manage.api.test.ts`, `db/front-desk.api.test.ts` (a foreign shift is P2003).

## 4. The prompt's settled decisions, as they will be built

### D1 — the API only, under the managed boundary
Three routes on a new router mounted at `manage.use('/packages', …)` inside the existing
`/manage/spaces/:spaceId` mount (`requireAuth()` → `requireSpaceAccess(…)`), so every caller without an
active link at a live space gets 404 before the router. The read needs nothing more (the boundary *is*
`can('space.read')`). The writes are `can(actor, 'packages.manage', …)` (rule `'owner'`, `can.ts`),
asked twice: at the route by `requireCan('packages.manage')` before `validate` (P1), and in the service
under the space's lock (P2). No `DELETE`: `isActive: false` retires. Out: capacity, the stay limit,
staff, every screen.

### D2 — a price above zero
`priceAgorot: z.number().int().min(1).max(PRICE_MAX_AGOROT)` in the shared schema, `PRICE_MAX_AGOROT`
imported from `@masaha/shared/spaces` (10,000,000, a space's prices' bound): 0 → `out_of_range`,
12.5 → `invalid_format`. The database's `packages_price_check` stays `>= 0`; finding 80 records it.

### D3 — a repeated name
The database's key `packages_space_id_name_key` (`@@unique([spaceId, name])`) decides, in the write's own
statement and transaction: the repository catches its P2002 with `isUniqueViolation(error,
'packages_space_id_name_key')` (the lookups' pattern, `governorates.repository.ts`) and the service
throws **the name refusal**. The field code is the contract's existing `not_unique` (§3's list), no new
domain code. The key covers retired packages too. No pre-check exists, so no race can pass it; two
writes of one name at once also serialize on the space's lock (P2). See S1 for the status.

### D4 — order
The list is `orderBy: [{ sortOrder: 'asc' }, { name: 'asc' }]`. **The rule:** a new package's
`sortOrder` is the largest `sortOrder` among the space's packages, retired ones included, plus one, or
`0` for its first, read under the space's lock (so two creates never share a place). No reorder route.
Names are unique per space, so the order is total. The name only orders rows written outside the API
(the demo seed's, all at the default 0).

### D5 — the read answers every package, whole
One `findMany` of the space's packages, `isActive` in each, no `page`, no `meta`. Added to
api-contract §4's exceptions (Appendix A).

### D6 — the body
| Field | Create | Rule (code on failure) |
|---|---|---|
| `name` | required | `textSchema(1, 60)` (`PACKAGE_NAME_MAX_LENGTH`): NFC, trimmed, no bidi or control characters (`too_short`, `too_long`, `invalid_format`); one name, the model's, not a pair; exact match after trim and NFC for uniqueness |
| `validityDays` | required | whole, 1 to 2,147,483,647 (`out_of_range`, `invalid_format`) |
| `totalDays`, `totalHours` | optional, `null` = none | the same |
| `daysPerWeek` | optional | whole, 1–7 (`MAX_DAYS_PER_WEEK`) |
| `hoursPerDay` | optional | whole, 1–24 (`MAX_HOURS_PER_DAY`) |
| `billing` | required | `SUBSCRIPTION_BILLINGS` = `FIXED`, `PER_HOUR`, `PER_DAY` (`invalid_choice`) |
| `priceAgorot` | required | D2 |
| `audience` | required | `PRICE_AUDIENCES` from `@masaha/shared/spaces` (`invalid_choice`) |
| `shiftId` | optional, `null` = none | a positive Int; one of the space's own shifts, else 422 `invalid_choice` on `shiftId` (P3) |
| `isActive` | not on create (P5) | PATCH only, boolean |

The limits combine freely (data-model › *Subscription limits*: "freely combined", warnings only). The
upper bound of the counts is the Int column's, as `parseId` and the shared ids use (S2). PATCH is the
same fields plus `isActive`, each optional; a required term is never `null` (`invalid_format`).

### D7 — never public
Built as a rule, held by structure: the module exports no public router (its row in conventions §7:
*manage*); `app.ts` mounts its one router only inside the managed boundary; the directory's packages are
`spaces`' published `SpacePrice` rows. **No test proves "nothing reads it"**: a test can only pin what
today's public answers hold, and its break (adding a read) is not a change anyone can name in advance.
What is proven: the matrix (T2) refuses every non-staff caller; the real run (§12.6) reads the space's
public page and finds no package's name in it. Stated in `packages.md`'s decisions.

### D8 — audit
In the write's transaction, through the injected `audit` (`writeAudit`), entity `package`, the package's
id, the space as `spaceId`, the actor:
- `package.created`, `after`: the stored terms (`name, validityDays, totalDays, daysPerWeek,
  hoursPerDay, totalHours, billing, priceAgorot, audience, shiftId`, absent ones `null`);
- `package.edited`, `before` and `after`: only the fields that changed, `isActive` included (one entry
  per request; the lookups split their flag because hiding has a public effect, a package's has none).

The existing names are `<entity>.<verb>`, singular (`space.created`, `user.created`,
`governorate.added`); the prompt's "`<module>.<verb>`" is read as that naming: `package.`, not
`packages.`.

### D9 — subscriptions keep their snapshot
Stated in `packages.md` and the contract (ADR 0010 rule 6): an edit or a retirement changes no
subscription. No code.

### D10 — the documents
Appendix A, written out: `api-contract.md`, `security.md`, `conventions.md` (its header needs only its
date: packages joins "the capabilities documented in `docs/features/`"; §6's list and §7's row change),
`plans/v1-mvp.md`, the new `docs/features/packages.md`, `docs/README.md` (the map lists every capability
document, documentation §9), `docs/project/overview.md` (*Built*), and `docs/features/spaces.md` (its two
"packages remain planned" lines, and *Who uses it*). *Deferred documents* holds only the contract's
*Endpoints*, met here.

### The plan's own decisions (inside the agreed item)
- **P1 — the writes are refused at the route first.** `requireCan('packages.manage')` before
  `validate`, as conventions §2's chain orders it and the photo writes do: reception's write is 403
  whatever its body (the fact routes answer 422 before 403 because their admin twin shares them; these
  routes have no twin). The service still decides under the lock.
- **P2 — a write takes the space's lock** (`spaces.lock(id, tx)`, `SpacesService`, FOR NO KEY UPDATE),
  404 when the space is gone, then `can()` on `space.linksUnder(tx)` (finding 43's rule, conventions
  §8 *Space access*). Not one of §13's "changes of a space", but it decides on the links and names a
  shift, and the place after the last needs one writer at a time.
- **P3 — the shift is checked by the database's key, not a read.** The composite foreign key
  `(shift_id, space_id) → space_shifts(id, space_id)` refuses another space's shift (P2003, as
  `db/front-desk.api.test.ts` shows for a visit); under the space's lock the space's own key cannot fail,
  so any P2003 of a package write is its shift → `invalid_choice` on `shiftId`. `packages` reads no
  shift, as `spaces` reads no package (spaces F5); no `spaces` code changes. Prices check by a read
  because one save holds up to 40 rows and the key cannot say which; a package is one row.
- **P4 — the read takes no transaction and no lock.** It is one statement, never half of a change; a
  space deleted after the boundary admitted the request answers its packages once more, as any read
  that started before the delete.
- **P5 — a new package is active; `isActive` is an edit's.** The design's sheet has no switch (it sits on
  the row, «متاحة في المكتب»), and a lookup row is created active too; an `isActive` in a create body is
  stripped, as every unknown key.
- **P6 — the name** is 1–60 characters, as a price's label; uniqueness is the key's exact match.
- **P7 — `SpacePackage`** carries no `sortOrder` and no dates: a list's order is its array's.
- **P8 — the path parameter is `:packageId`**, as `:photoId`.
- **P9 — no idempotency key** (ADR 0015's scope is the desk's creates): a create retried after a lost
  answer meets its own name (the name refusal), and the list shows the package.
- **P10 — `SUBSCRIPTION_BILLINGS` lives in `@masaha/shared/packages`** (L2), which `subscriptions` (L3)
  will import; its name follows the Prisma enum `SubscriptionBilling`.

### The code, file by file (interfaces; the commit that adds each part in brackets)

**`packages/shared/src/packages/`** (new; shared-package R1–R2, L2 in `eslint.config.js`)
- `index.ts` [C2]: `export * from './requests.ts';` and `export * from './responses.ts';`
- `requests.ts`: a header comment citing `docs/api/api-contract.md` §5 *Packages (managed)*;
  [C2] `SUBSCRIPTION_BILLINGS = ['FIXED', 'PER_HOUR', 'PER_DAY'] as const`;
  [C3] `PACKAGE_NAME_MAX_LENGTH = 60`, `MAX_DAYS_PER_WEEK = 7`, `MAX_HOURS_PER_DAY = 24`; private
  `id` (positive Int ≤ 2,147,483,647), `count` (whole, 1 to 2,147,483,647), `optional(schema)` =
  `schema.nullable().optional()` (as `spaces/requests.ts`); the `terms` object of D6;
  `createPackageSchema = z.object(terms)`, `CreatePackageRequest`;
  [C4] `updatePackageSchema = z.object({ ...terms, isActive: z.boolean() }).partial()`,
  `UpdatePackageRequest`. Imports `textSchema` from `../core/index.ts`, `PRICE_AUDIENCES` and
  `PRICE_MAX_AGOROT` from `../spaces/index.ts` (R3: lower level, through its index).
- `responses.ts` [C2]: `SpacePackage { id; name; validityDays; totalDays: number | null; daysPerWeek;
  hoursPerDay; totalHours; billing: (typeof SUBSCRIPTION_BILLINGS)[number]; priceAgorot;
  audience: (typeof PRICE_AUDIENCES)[number]; shiftId: number | null; isActive: boolean }`, each field
  with a one-line comment as `spaces/responses.ts` does (type-only imports).

**`apps/api/src/modules/packages/`** (new)
- `index.ts`: `createPackagesService`, `type PackagesService`, `createPackagesController`,
  `createPackagesManageRouter` (R2: nothing else).
- `packages.repository.ts`: `PACKAGE` select (the 12 response fields) `satisfies Prisma.PackageSelect`;
  `PackageRow`; `PackageTerms = Omit<PackageRow, 'id' | 'isActive'>`; `PackageData =
  Partial<Omit<PackageRow, 'id'>>`; `PackageWrite = { package: PackageRow } | { refused: 'name' | 'shiftId' }`;
  a private `written(write)` mapping P2002 on `packages_space_id_name_key` → `{ refused: 'name' }` and
  P2003 (`isForeignKeyViolation`) → `{ refused: 'shiftId' }`, rethrowing anything else (comment: under
  the space's lock, the only key a package's write can miss is its shift's).
  `createPackagesRepository()` (no parameter, as `createPricesRepository`):
  [C2] `listFor(spaceId, tx: Tx = prisma): Promise<PackageRow[]>` (D4's order);
  [C3] `nextPlace(spaceId, tx: Tx): Promise<number>` (`aggregate _max sortOrder` where `spaceId`, `?? -1`, `+ 1`);
  [C3] `create(spaceId, terms: PackageTerms, sortOrder, tx: Tx): Promise<PackageWrite>`;
  [C4] `findIn(spaceId, id, tx: Tx = prisma): Promise<PackageRow | null>` (`findUnique` on
  `id_spaceId`); [C4] `update(spaceId, id, data: PackageData, tx: Tx): Promise<PackageWrite>`
  (`where: { id_spaceId: { id, spaceId } }`, so it can never touch another space's row).
- `packages.mapper.ts` [C2]: `toSpacePackage(row: PackageRow): SpacePackage`, field by field.
- `packageTerms.ts` (pure, like `spaces/profile.ts`): [C3] `toPackageTerms(request:
  CreatePackageRequest): PackageTerms` (absent limit or shift → `null`); [C3] `packageValues(fields):
  AuditValues`; [C4] `interface PackageChange { data: PackageData; before: AuditValues; after:
  AuditValues }` and `packageChange(current: PackageRow, edit: UpdatePackageRequest): PackageChange`:
  a field the edit sets (not `undefined`) to a value other than the current one; `null` clears; an
  edit that changes nothing has empty `data` (`profileChange`'s rule).
- `packages.service.ts`: [C2] `createPackagesService()` with `list(spaceId): Promise<SpacePackage[]>`
  (no transaction, P4). [C3] the factory takes `{ runInTransaction, audit, spaces }`
  (`spaces: SpacesService` from `../spaces/index.ts`; R4, L2 → L1); a private `lockFor(actor, space, tx)`
  (`spaces.lock` false → `AppError.notFound(undefined, 'Space not found')`; `can(actor,
  'packages.manage', { links: await space.linksUnder(tx) })` false → `AppError.forbidden()`); a private
  `packageOf(write)` (`refused: 'name'` → the name refusal; `refused: 'shiftId'` →
  `AppError.validation({ shiftId: ['invalid_choice'] })`); `create(actor, space, request)`: one
  transaction, one statement at a time — `lockFor`, `toPackageTerms`, `nextPlace`, `create`, the
  `package.created` entry, `toSpacePackage`. [C4] `update(actor, space, packageId, edit)`: `lockFor`,
  `findIn` (none → `AppError.notFound(undefined, 'Package not found')`), `packageChange` (empty `data`
  → answer the current package, write nothing), `update`, the `package.edited` entry. Its doc comment
  names the order of work, as `photos.service.ts`'s does.
- `packages.controller.ts`: [C2] `list` → `sendSuccess(res, … satisfies SpacePackage[])`; [C3] `create`
  → `signedIn(req)`, `spaceOf(req)`, `req.body as CreatePackageRequest`, `{ status: 201 }`; [C4] `update`
  → `parseId(req.params.packageId)`, `req.body as UpdatePackageRequest`.
- `packages.manage.routes.ts`: `createPackagesManageRouter(controller)`: [C2] `router.get('/',
  controller.list)`; [C3] `const mayManage = requireCan('packages.manage')`, `router.post('/',
  mayManage, validate(createPackageSchema), controller.create)`; [C4] `router.patch('/:packageId',
  mayManage, validate(updatePackageSchema), controller.update)`.

**`apps/api/src/app.ts`**: [C2] import the three factories from `./modules/packages/index.ts`;
`const packages = createPackagesService();` after `const spaces = createSpacesService();`; after the
photos' `manage.use('/photos', …)`: `manage.use('/packages',
createPackagesManageRouter(createPackagesController(packages)));`. [C3] `createPackagesService({
runInTransaction, audit: writeAudit, spaces })`.

**`apps/api/src/db/foreignKeyViolation.ts`** [C3], comment only: "…a row still referenced refused its
delete, such as a shift a price uses, or a write named a row its key cannot find, such as another
space's shift. A repository turns it into what it means; the service answers." (today's says "what is
in use; the service answers the 409", which a package's 422 would make untrue).

## 5. Stronger decisions

### S1 — a taken name answers `conflict` (409), not `validation` (422) — **recommended**
- **What:** the name refusal as `conflict` (409) with `errors.name = ["not_unique"]`.
- **Why:** the contract's §3 gives a unique violation to `conflict` (409); data-model › *Conventions*
  says "Unique violations (Prisma `P2002`) become `409 CONFLICT`"; conventions §4 says "`P2002` →
  `conflict` with `NOT_UNIQUE` field errors"; every name taken by another stored row answers 409 today
  (governorates, areas, amenities, `EMAIL_TAKEN`). The 422 `not_unique` is used only for a repeat inside
  one request's own list (the group saves), which the browser's schema finds before sending; a name
  taken by another package can only be found by the server. The owner's O8 ("a repeated name on its
  field") holds either way: both carry `errors.name`, and the web already puts a 409's `not_unique` on
  its field (`apps/web/src/features/lookups/hooks/useLookupForm.ts:48`).
- **Cost:** none in code (one line: `conflict` instead of `validation`; T5 and T15 expect 409). Keeping
  422 costs three exceptions in three documents (the contract's §3 row, data-model's line, conventions
  §4, Appendix A *If S1 is not approved*) — data-model is #85's file too — and a second meaning of a
  taken field.
- **Recommendation:** approve S1. Until the reply, the default stands.

### S2 — no domain cap on the counts, or on a space's number of packages — **considered, not recommended**
- **What:** a guard bound (say, a validity of at most ten years) or a cap per space (a 409 past it).
- **Why not:** neither is in the model, the design or the owner's decisions; the Int column's bound
  already keeps every input from a 500; a space types its packages by hand, tens at most, so the whole
  list stays small.
- **Cost if adopted:** a product rule nobody asked for, its contract line, a 409 path and its test.
- **Recommendation:** keep the Int bound only; revisit with the desk's screen.

### S3 — the read under the space's share lock — **considered, not recommended**
- **What:** read the list in a transaction under `FOR SHARE`, as the space's read and the photos' list
  do, so a space deleted after the boundary answers 404.
- **Why not:** one statement is never half of a change (P4); `spaces` exports no share lock to modules
  above it (`lockShared` is internal to `space/space.repository.ts`), so it would add a `spaces` export
  and a transaction to every desk read.
- **Recommendation:** no.

### Rules the item touches, stated
- **engineering-principles §6, "Paginate every list":** the list is whole (D5), through the contract's
  §4 exception list, its documented home.
- **conventions §4 / data-model / contract §3 on P2002 → 409:** contradicted by D3's 422 unless S1 is
  approved; Appendix A carries the exceptions for the default.
- **data-model › Constraints, "prices not negative":** still true of the database; D2's stricter rule is
  the API's, and finding 80 records the gap.
- **conventions §13, the space's lock:** a package's write takes it too (P2) — consistent, not required.
- **spaces F5, "`spaces` reads none of their tables":** kept: no `spaces` code changes (P3).
- **testing §4, every role on each protected endpoint:** USER, an owner of another space, the owner, an
  unlinked admin, and reception (T2, T7, T16).

## 6. Related findings

- **77, 78, 79 — #86's review:** **recorded here** (the owner's decision; no code), in C1. Their fixes
  are out of scope. T9 and T10 use `whileHeld`, so they share 77's caveat (Review Focus).
- **80 — new:** "The database still takes a package with a price of zero", recorded in C3 (D2).
- **43 — two races around a space's facts** (Resolved): its rule is applied (P2, T9).
- **14 — the owner's audit screen has no design:** `package.*` entries will appear there; not folded.
- **63, 17, 21, 23, 15, 59, 67:** not related. **73–74** are #85's. **81** is not used.

## 7. The files it edits

No licence in another layer. **28 files** (+1 if S1 is not approved):

| # | Path | Commit | What |
|---|---|---|---|
| 1 | `docs/architecture/findings/77-the-race-helper-counts-any-waiting-backend-and-its-reach-sits-under-vitests-timeout.md` | C1 | new |
| 2 | `docs/architecture/findings/78-the-owners-names-test-assumes-nothing-reads-users-before-them.md` | C1 | new |
| 3 | `docs/architecture/findings/79-the-users-names-reader-keeps-an-optional-transaction.md` | C1 | new |
| 4 | `docs/architecture/findings/README.md` | C1, C3 | 77–79, then 80, under *Open* — **shared** |
| 5 | `packages/shared/src/packages/index.ts` | C2 | new |
| 6 | `packages/shared/src/packages/requests.ts` | C2, C3, C4 | new |
| 7 | `packages/shared/src/packages/responses.ts` | C2 | new |
| 8 | `packages/shared/src/packages/requests.unit.test.ts` | C3, C4 | new, R1–R8 |
| 9 | `apps/api/src/modules/packages/index.ts` | C2 | new |
| 10 | `apps/api/src/modules/packages/packages.manage.routes.ts` | C2, C3, C4 | new |
| 11 | `apps/api/src/modules/packages/packages.controller.ts` | C2, C3, C4 | new |
| 12 | `apps/api/src/modules/packages/packages.service.ts` | C2, C3, C4 | new |
| 13 | `apps/api/src/modules/packages/packages.repository.ts` | C2, C3, C4 | new |
| 14 | `apps/api/src/modules/packages/packages.mapper.ts` | C2 | new |
| 15 | `apps/api/src/modules/packages/packageTerms.ts` | C3, C4 | new |
| 16 | `apps/api/src/modules/packages/packageTerms.unit.test.ts` | C3, C4 | new, U1–U5 |
| 17 | `apps/api/src/modules/packages/packages.api.test.ts` | C2, C3, C4 | new, T1–T16 |
| 18 | `apps/api/src/app.ts` | C2, C3 | wiring and mount |
| 19 | `apps/api/src/db/foreignKeyViolation.ts` | C3 | comment |
| 20 | `docs/api/api-contract.md` | C2, C3, C4 | §4, §5 *Packages (managed)* (§3 if S1 not approved) |
| 21 | `docs/features/packages.md` | C2, C3, C4 | new |
| 22 | `docs/README.md` | C2 | the map's line |
| 23 | `docs/backend/conventions.md` | C2, C3 | date, §7 row; §6 bullet (§4 if S1 not approved) |
| 24 | `docs/backend/security.md` | C3 | header, *Authorization* |
| 25 | `docs/features/spaces.md` | C3, C4 | *Who uses it*; header and lines 18–19 — **shared** |
| 26 | `docs/architecture/findings/80-the-database-still-takes-a-package-with-a-price-of-zero.md` | C3 | new |
| 27 | `docs/plans/v1-mvp.md` | C4 | date, *Built* line, the row |
| 28 | `docs/project/overview.md` | C4 | date, *Built* — **shared** |
| c | `docs/architecture/data-model.md` | C3 | only if S1 is not approved — **shared** |

**Shared with #85** (`gh pr view 85 --json files`: web and documents only, no code file of this plan):
`docs/features/spaces.md`, `docs/project/overview.md`, `docs/architecture/findings/README.md`, and
`docs/architecture/data-model.md`. #85 merges first, so each is **re-read on the merged tree before it is
edited**; this item edits only the lines Appendix A names (spaces.md: the header's last sentence and
date, the two lines on "packages remain planned", *Who uses it*; the overview: the date, the Spaces
line's last sentence, one new line; the index: four lines under *Open*). A conflict there is
documents-only: keep both sides.

## 8. Design issues

None: this item builds no screen.

## 9. Tests — lane, title, the break each catches

Every test is seen failing first (testing §3 rules 5–7): written before its code and run red; a test
that passes before its code exists (marked **∅**) is proven by its break instead. Every red run's output
— the failing title and its assertion lines — goes into the report. Expectations are written by hand.

### Unit lane — `packages/shared/src/packages/requests.unit.test.ts` (`npm run test:unit -w @masaha/shared -- src/packages/requests.unit.test.ts`)
Style of `spaces/requests.unit.test.ts`: a `VALID` body `{ name: 'Morning', validityDays: 30, billing:
'FIXED', priceAgorot: 5000, audience: 'GENERAL' }` and `errorsOf(body)` through `toFieldErrors`.
- **R1** [C3] *takes a package's required terms alone, and every limit and the shift beside them* —
  `parse(VALID)` equals `VALID`; with `totalDays: 10, daysPerWeek: 3, hoursPerDay: 5, totalHours: 40,
  shiftId: 7` equals it too; each limit `null` passes. Break: a limit required → red.
- **R2** [C3] *trims the name, and refuses one empty, longer than 60 characters, or on two lines* —
  `'  Morning  '` → `'Morning'`; `''` and `'   '` → `too_short`; `'a'.repeat(61)` → `too_long`, 60
  passes; `'Morning\nEvening'` → `invalid_format`. Break: `textSchema(1, 80)` → red.
- **R3** [C3] *wants whole agorot from 1 to 10,000,000: no package is free* — 0 → `out_of_range`; 1 and
  10_000_000 pass; 10_000_001 → `out_of_range`; 12.5 → `invalid_format`. **Break (D2):** `.min(0)` → red.
- **R4** [C3] *keeps each count in its range: the validity and the totals from 1, days a week 1 to 7,
  hours a day 1 to 24* — `validityDays` 0, `totalDays` 0, `totalHours` 0, `daysPerWeek` 0 and 8,
  `hoursPerDay` 0 and 25, `validityDays` 2_147_483_648 → `out_of_range`; `daysPerWeek` 7 and
  `hoursPerDay` 24 pass; `validityDays` 1.5 → `invalid_format`. Break: `daysPerWeek` max 8 → red.
- **R5** [C3] *refuses a billing or an audience not on its list* — `'WEEKLY'`, `'ALL'` →
  `invalid_choice`. Break: `billing: z.string()` → red.
- **R6** [C3] *requires the name, the validity, the billing, the price and the audience* — `{}` → each
  of the five `required`, nothing else. Break: `audience` optional → red.
- **R7** [C4] *takes any part of the terms and the active flag on an edit, and nothing* — `{}`,
  `{ isActive: false }`, `{ totalDays: null, shiftId: null }` pass as given. Break: no `.partial()` → red.
- **R8** [C4] *never clears a required term on an edit* — `{ name: null }`, `{ validityDays: null }`,
  `{ billing: null }`, `{ priceAgorot: null }`, `{ audience: null }`, `{ isActive: null }` → each
  `invalid_format` on its field. Break: `name` made nullable → red.

### Unit lane — `apps/api/src/modules/packages/packageTerms.unit.test.ts` (`npm run test:unit -w @masaha/api -- src/modules/packages/packageTerms.unit.test.ts`)
`CURRENT`: a `PackageRow` written by hand (`id 4, name 'Morning', validityDays 30, totalDays 10,
daysPerWeek null, hoursPerDay 5, totalHours null, billing 'FIXED', priceAgorot 5000, audience 'GENERAL',
shiftId null, isActive true`).
- **U1** [C3] *stores an absent limit or shift as none* — `toPackageTerms(VALID)` equals the ten terms
  with every limit and `shiftId` `null`. Break: `totalDays: request.totalDays` (no `?? null`) → red.
- **U2** [C4] *writes and records only the fields the edit sets to a new value* — `{ name: 'Morning',
  priceAgorot: 6000 }` → `data { priceAgorot: 6000 }`, `before { priceAgorot: 5000 }`, `after
  { priceAgorot: 6000 }`. Break: no comparison with the current value → red.
- **U3** [C4] *clears a limit with null, recording what it held* — `{ totalDays: null }` → `data
  { totalDays: null }`, `before { totalDays: 10 }`, `after { totalDays: null }`. Break: `null` treated as
  absent (`!= null` filter) → red.
- **U4** [C4] *changes nothing for an edit of the same values, or of nothing* — `{}` and `{ name:
  'Morning', isActive: true }` → `data {}`, `before {}`, `after {}`. Break: every present field written → red.
- **U5** [C4] *records a retirement as the flag's change* — `{ isActive: false }` → `data { isActive:
  false }`, `before { isActive: true }`, `after { isActive: false }`. Break: `isActive` dropped from the
  compared fields → red.

### API lane — `apps/api/src/modules/packages/packages.api.test.ts` (`npm run test:api -w @masaha/api -- src/modules/packages/packages.api.test.ts`)
Setup as `manage.api.test.ts`: `resetDatabase(prisma)`; `spaceId` from `createSpace()`; `owner =
signInOwnerOf(spaceId)`; `reception = signIn('USER', 'reception@example.com')` with a `RECEPTION`
`spaceManager` row; `stranger = signIn('USER', 'stranger@example.com')`; `otherSpaceId` from
`createSpace('other-space')`, `unrelatedOwner = signInOwnerOf(otherSpaceId)`; `admin = signIn('ADMIN')`;
`shift` = `prisma.spaceShift.create({ data: { spaceId, nameAr: 'صباحي', startsMinute: 480, endsMinute:
840 } })`, `otherShift` the same at `otherSpaceId`. A `packages(caller, method, suffix?, body?, at =
spaceId)` helper builds `/api/v1/manage/spaces/<at>/packages<suffix>`. `VALID` as above. Helpers
`dataOf`, `errorOf`, `auditEntries` (`test/admin.ts`), `whileHeld` (`test/locks.ts`).

**C2 — the read**
- **T1** *answers the owner and reception every package of the space, retired ones included, by place
  then name, whole* — seed with `prisma.package.create`, in this order: `Beta` (sortOrder 0), `Alpha`
  (sortOrder 0, `isActive: false`), `Aardvark` (sortOrder 1) — each `validityDays 30, billing 'FIXED',
  priceAgorot 5000` — and `Other` at `otherSpaceId`. Owner `GET` → 200, `dataOf` equals, by hand, the
  three `SpacePackage`s `[Alpha, Beta, Aardvark]` (every field; limits and `shiftId` `null`;
  `audience 'GENERAL'`); `response.body.meta` is `undefined`; reception's body equals the owner's.
  **Breaks:** `orderBy` by place then `id` (→ `[Beta, Alpha, Aardvark]`) → red; the `spaceId` filter
  dropped (→ `Other` listed) → red; `where: { isActive: true }` → red.
- **T2** ∅ *answers not_found to a stranger, an owner of another space and an unlinked admin on every
  packages route* — [C2] `GET` → 404 `not_found`; [C3] adds `POST VALID` → 404 and no package written;
  [C4] adds `PATCH /<a seeded package's id> { priceAgorot: 1 }` → 404 and the package unchanged.
  **Break:** mount the router behind `loadSpaceLinks((id, tx) => spaceLinks.linksAt(id, tx))` (the
  admin's loader, which refuses no one) on its own `api.use('/manage/spaces/:spaceId/packages',
  requireAuth(), …)` before the managed mount → the stranger's `GET` is 200 → red.

**C3 — add**
- **T3** *creates an active package with its terms, placed after the last, and audits
  package.created* — owner `POST { name: 'Zeta', validityDays: 30, billing: 'FIXED', priceAgorot: 5000,
  audience: 'GENERAL' }` → 201, `dataOf` equals `{ id: <number>, name: 'Zeta', validityDays: 30,
  totalDays: null, daysPerWeek: null, hoursPerDay: null, totalHours: null, billing: 'FIXED',
  priceAgorot: 5000, audience: 'GENERAL', shiftId: null, isActive: true }`; then `POST { name: 'Alpha',
  validityDays: 45, totalDays: 10, daysPerWeek: 3, hoursPerDay: 5, totalHours: 40, billing: 'PER_DAY',
  priceAgorot: 1000, audience: 'STUDENT', shiftId: shift.id }` → 201 with those terms; `GET` →
  `[Zeta, Alpha]`; `auditEntries()` equals two entries `{ actorId: owner.id, action: 'package.created',
  entityType: 'package', entityId: <each id>, spaceId, before: null, after: <its ten terms, nulls
  included> }`. **Breaks:** `nextPlace` answering 0 (→ `[Alpha, Zeta]`) → red (ordering, D4); the audit
  call dropped → red.
- **T4** *refuses a price of zero and a limit out of its range on their fields, writing nothing* —
  `POST { ...VALID, priceAgorot: 0, daysPerWeek: 8 }` → 422 `validation`, `errors` equal
  `{ priceAgorot: ['out_of_range'], daysPerWeek: ['out_of_range'] }`; `prisma.package.count()` is 0.
  **Break:** the route without `validate(createPackageSchema)` (the price 0 passes the database's
  CHECK; the 8 fails it → 500) → red.
- **T5** *refuses a name another package of the space holds, retired or not, on its field; another
  space may hold it* — owner `POST { ...VALID, name: 'Alpha' }` → 201; retire it with
  `prisma.package.update(… { isActive: false })`; `POST { ...VALID, name: 'Alpha' }` → **the name
  refusal** (status, `type`, `errors: { name: ['not_unique'] }`); this space still has one package and
  `auditEntries()` one entry; `unrelatedOwner` `POST { ...VALID, name: 'Alpha' }` at `otherSpaceId` →
  201. **Break:** the P2002 mapping dropped from `written` → 500 → red.
- **T6** *refuses a shift that is not the space's with invalid_choice on shiftId, writing nothing* —
  `POST { ...VALID, shiftId: otherShift.id }` and `{ ...VALID, shiftId: 2147483647 }` → each 422
  `validation`, `errors` equal `{ shiftId: ['invalid_choice'] }`; count 0. **Break:** the P2003 mapping
  dropped → 500 → red.
- **T7** *refuses reception's create with 403 before reading its body, and writes nothing* — reception
  `POST {}` → 403 `forbidden` (not 422); reception `POST VALID` → 403; count 0; no audit entry.
  [C4] adds reception `PATCH /<id> { priceAgorot: 0 }` → 403 (not 422) and `PATCH /<id> { priceAgorot:
  6000 }` → 403, the package unchanged. **Breaks:** `mayManage` dropped from the POST route (→ the `{}`
  body answers 422) → red; [C4] dropped from the PATCH route → red.
- **T9** *decides a write on the links under the space's lock: an owner unlinked meanwhile is refused*
  — `whileHeld((tx) => tx.$queryRaw\`SELECT id FROM spaces WHERE id = ${spaceId} FOR NO KEY UPDATE\`,
  () => packages(owner, 'post', '', VALID), (tx) => tx.spaceManager.update({ where: { spaceId_userId:
  { spaceId, userId: owner.id } }, data: { deactivatedAt: new Date() } }))` → 403 `forbidden`; count 0;
  `auditEntries()` `[]`. **Break (security, rule 7):** `can()` on `space.links` (the loader's) instead of
  `linksUnder(tx)` → 201 → red.
- **T10** *refuses a write to a space deleted while it waited for its lock* — `whileHeld(<the same
  hold>, () => packages(owner, 'post', '', VALID), (tx) => tx.space.update({ where: { id: spaceId },
  data: { deletedAt: new Date() } }))` → 404 `not_found`; count 0. **Break:** `lockFor` ignoring
  `spaces.lock`'s answer → 403 (no links under the lock) or 201 → red.

**C4 — edit**
- **T11** *edits what the patch sets, clears a limit with null, and audits package.edited with the
  fields that changed* — owner `POST { ...VALID, name: 'Alpha', totalDays: 10, hoursPerDay: 5 }`;
  `PATCH /<id> { name: 'Alpha', priceAgorot: 6000, totalDays: null }` → 200, `dataOf` equals the
  package with `priceAgorot 6000, totalDays null, hoursPerDay 5`; the last audit entry equals
  `{ actorId: owner.id, action: 'package.edited', entityType: 'package', entityId: <id>, spaceId,
  before: { priceAgorot: 5000, totalDays: 10 }, after: { priceAgorot: 6000, totalDays: null } }`.
  **Breaks:** `after` the whole edit (→ `name` recorded) → red; the update skipped → red.
- **T12** *retires a package with isActive false, keeps it in the list, and offers it again* — owner
  `POST { ...VALID, name: 'Alpha' }`; `PATCH { isActive: false }` → 200 `isActive: false`; `GET` lists it with `isActive: false`; its entry has
  `before { isActive: true }`, `after { isActive: false }`; `PATCH { isActive: true }` → `isActive:
  true`. **Break:** `isActive` left out of `updatePackageSchema` (stripped) → red.
- **T13** *writes nothing for a patch that changes nothing* — owner `POST { ...VALID, name: 'Alpha' }`
  (price 5000); `PATCH {}` and `PATCH { name: 'Alpha', priceAgorot: 5000 }` → 200 with the package as
  it was; its `updatedAt` (read with Prisma) unchanged;
  still one audit entry. **Break:** update and audit even when `data` is empty → red.
- **T14** ∅ *answers not_found for a package of another space, or an id no package has, changing
  nothing* — `Other` created with Prisma at `otherSpaceId`; owner `PATCH /<Other's id> { priceAgorot:
  1 }` → 404 and `Other` unchanged; `/999999` and `/abc` → 404. **Break (security, rule 7):** `findIn`
  by `id` alone and `update` by `id` alone → 200, `Other` changed → red.
- **T15** *refuses renaming to another package's name, and a shift that is not the space's, on their
  fields* — `Alpha` and `Beta` created; `PATCH Beta { name: 'Alpha' }` → the name refusal; `PATCH Beta
  { shiftId: otherShift.id }` → 422 `{ shiftId: ['invalid_choice'] }`; `Beta` unchanged, one entry per
  create only. **Break:** `update` not passed through `written` → 500 → red.
- **T16** = T7's [C4] half; **T8** = T2's [C3]/[C4] halves (numbers kept for the report's table).

### Not tested, and said
- **D7** (nothing public reads the table): a rule (D7); the real run checks the public page (§12.6).
- **Two creates of one name at once:** the database's key decides inside the write, with no check
  before it; a race test would pass with or without any code of this item (testing §1: T5 and the key
  prove it).
- **Two creates at once getting distinct places:** the lock serializes them; which of the two waiters
  takes the lock first is PostgreSQL's, so a test could not fix the expected order (Review Focus).

## 10. Review Focus — the inputs no planned test exercises

- Two concurrent creates: distinct `sortOrder`s rest on P2 alone (no test, §9).
- A space deleted between the boundary and a `GET`: answered once more (P4, S3).
- A create retried after a lost answer: the name refusal for its own package (P9).
- T9 and T10 wait through `whileHeld`, whose `waitingOnLock()` counts any waiting backend of the test
  database (finding 77); only one test file runs at a time, so no other request waits there.
- `PATCH` changing `billing` keeps `priceAgorot` as it was (now read as a rate): the owner sends both;
  no cross-field rule (D6).
- An `isActive` in a create body is stripped silently (P5), as any unknown key.
- Uniqueness is exact (`Morning` and `morning` are two names), as the key holds it (P6).
- `PRICE_AUDIENCES` and `PRICE_MAX_AGOROT` are `spaces`' exports: a change there changes packages too.
- The demo seed's packages sit at `sortOrder` 0, so they list by name (D4).

## 11. The commits

| Commit | Subject (chars) | Content |
|---|---|---|
| C1 | `docs(findings): record three review findings` (44) | findings 77, 78, 79; the index |
| C2 | `feat(packages): list a space's packages` (39) | shared `index.ts`, `responses.ts`, `requests.ts` (billings); the module's read (index, routes GET, controller.list, service.list, repository.listFor, mapper); `app.ts`; T1, T2; Appendix A's [C2] lines |
| C3 | `feat(packages): add the owner's packages` (40) | the create schema and R1–R6; `packageTerms.ts` with U1; nextPlace, create, `written`, `lockFor`, `packageOf`, the service's dependencies; POST with `requireCan`; `app.ts`'s dependencies; `foreignKeyViolation.ts`'s comment; T3–T7, T9, T10, T2's POST; Appendix A's [C3] lines; finding 80 and the index |
| C4 | `feat(packages): edit and retire a package` (42) | the update schema and R7, R8; `packageChange` and U2–U5; findIn, update, service.update; PATCH; T11–T15, T2's and T7's PATCH; Appendix A's [C4] lines |

The PR's title is C3's subject, its main unit. Bodies say *why* in one or two lines; no trailer, no tool
attribution. Each commit passes lint and typecheck on its own.

## 12. Verification and the procedure

### 12.1 Before the branch
```powershell
Set-Location C:\Users\basel\masaha-b
git fetch origin
git status --short --branch          # clean and detached
gh pr view 85 --json state,mergedAt  # MERGED; if not, stop: this item runs after #85
git log --oneline -5 origin/main
gh pr list --state open --json number,title,headRefName,headRefOid
git diff --name-status 44b8ac7b origin/main
```
Any change to a code file of §7 (rows 5–19), to `apps/api/src/modules/spaces/index.ts`,
`spaces.service.ts`, `shared/auth/*`, `db/uniqueViolation.ts`, `eslint.config.js`,
`packages/shared/src/spaces/*`, `packages/shared/src/core/*`, `apps/api/test/*` or `schema.prisma`, or
an existing `apps/api/src/modules/packages/` — **re-read it; if it contradicts this plan, stop and ask.**
An open PR editing any code file of §7: stop and ask. The shared documents of §7: re-read on the merged
tree before editing them. Then:
```powershell
git switch --no-track -c feat/space-packages origin/main
docker start masaha-postgres-1       # never npm run db:up
```
`apps/api/.env` must point at `masaha_b_dev` / `masaha_b_test` and `PORT=3321` (check the names; never
print the file).

**One full test run at a time on this machine.** Before each full lane:
```powershell
Get-CimInstance Win32_Process -Filter "Name = 'node.exe'" |
  Where-Object { $_.CommandLine -match 'vitest' } | Select-Object ProcessId, CommandLine
```
A line under `C:\Users\basel\masaha\` (not `masaha-b`): wait for it to end. One or two files are not a
full run.

### 12.2 First checks (each when its code exists)
1. **The level rule:** after C2's files, `npm run lint`. The module (L2) importing `../spaces/index.ts`
   and `@masaha/shared/packages`, and `packages/shared/src/packages` importing `../spaces/index.ts`,
   must pass (`packages` is L2 in `eslint.config.js`). *If lint refuses:* stop and ask.
2. **`id_spaceId`:** `npm run typecheck` accepts `findUnique`/`update` on `where: { id_spaceId: { id,
   spaceId } }`. *If not* (the compound name differs): use the name the generated client gives
   (`apps/api/src/generated/prisma/models/Package.ts`, `PackageWhereUniqueInput`), and say so in the
   report.
3. **P2002's meta** (T5): if T5 answers 500, log `error.meta` once (removed before the commit). If the
   constraint's name appears in it under another spelling, match that; if it names no constraint, stop
   and ask.
4. **P2003 on a write** (T6): if T6 answers 500, log the error's `code` once (removed). Not `P2003`: stop
   and ask (the fallback, a read of the shifts through a new `spaces` export, is the owner's to approve).
5. **Audit `before`:** `null` when not given (the lookups' tests expect it); write what the model gives.

### 12.3 Implement, commit by commit
Stage **by path** (`git add <path> …`; never `-A` or `.`); `git status` before each commit; after each
commit `npm run lint` and `npm run typecheck`. Inside each commit: the test first, run red (output to the
report), then the code, then green, then its documents (Appendix A's lines tagged with that commit).
Focused runs: the commands of §9. A **∅** test is green before its code; its break (§12.5) is its proof.

**A fix before the push** folds into its commit:
```powershell
git commit --fixup=<sha> -- <paths>
$env:GIT_SEQUENCE_EDITOR=':'; git rebase -i --autosquash $(git merge-base HEAD origin/main); Remove-Item Env:GIT_SEQUENCE_EDITOR
git rebase -x "npm run lint && npm run typecheck" $(git merge-base HEAD origin/main)
```

### 12.4 Verification on the head (phase 4)
One at a time, after §12.1's check: `npm run lint` · `npm run typecheck` · `npm run test:unit` ·
`npm run test:api` · `npm run format:check` · `npm run check:links` · `npm run build -w @masaha/shared`
(so `packages/shared/dist` holds the new folder). Also: `git grep -n "#PRNUM"` lists only the documents
before §12.7; `git diff --stat origin/main -- apps/web apps/api/prisma package.json package-lock.json`
is empty. **Not run, with why:** `test:component`, the web's `build`, `check:build`, `check:classes` —
no file in `apps/web` changes and the prompt's list leaves them to CI, which runs them on the pushed head.

### 12.5 The breaks (testing §3 rule 7), each recorded
For each: copy the file to `$env:TEMP\packages-breaks\` (a backup), make the one edit, run the named
test file, copy the red output into the report, restore **from the backup** (never `git checkout`), run
it green again, then `git diff --stat` shows only the item's own work.

| # | Test | File | The edit |
|---|---|---|---|
| B1 | T1 | `packages.repository.ts` | `listFor`'s `where` without `spaceId` |
| B2 | T1 | `packages.repository.ts` | `orderBy: [{ sortOrder: 'asc' }, { id: 'asc' }]` |
| B3 | T2 | `app.ts` | the packages router mounted behind `loadSpaceLinks` (§9, T2) |
| B4 | T3 | `packages.repository.ts` | `nextPlace` returns `0` |
| B5 | T4 | `packages.manage.routes.ts` | POST without `validate(createPackageSchema)` |
| B6 | T5 | `packages.repository.ts` | `written` without the P2002 branch |
| B7 | T6 | `packages.repository.ts` | `written` without the P2003 branch |
| B8 | T7 | `packages.manage.routes.ts` | POST without `mayManage` |
| B9 | T9 | `packages.service.ts` | `can(actor, 'packages.manage', space)` |
| B10 | T10 | `packages.service.ts` | `lockFor` ignores `spaces.lock`'s answer |
| B11 | T14 | `packages.repository.ts` | `findIn` and `update` by `{ id }` alone |
| B12 | T16 | `packages.manage.routes.ts` | PATCH without `mayManage` |
| B13 | R3 | `requests.ts` (shared) | `priceAgorot` `.min(0)` |

A break that stays green: stop and ask.

### 12.6 The real run (API on 3321, `masaha_b_dev`)
1. `npm run dev -w @masaha/api` in the background; `curl.exe -s http://localhost:3321/health` → `db: up`.
2. Data through the API (as HARDEN's run): sign in the seeded admin (`POST /api/v1/auth/login`, the
   `SEED_ADMIN_*` account; never print the password); `POST /api/v1/admin/spaces` in an active area;
   `POST /api/v1/admin/owners { name, email, spaceId }` → the temporary password; sign in with it;
   `POST /api/v1/me/password` → the owner's token. Register reception and a stranger
   (`POST /api/v1/auth/register`). Link reception in the dev database only (no staff API yet):
   `docker exec masaha-postgres-1 psql -U <user from .env's URL> -d masaha_b_dev -c "INSERT INTO space_managers (space_id, user_id, role, created_at, updated_at) VALUES (<space>, <reception>, 'RECEPTION', now(), now())"`.
   Owner `PUT /api/v1/manage/spaces/<id>/hours` with seven open days 480–1320 and one shift
   `{ nameAr: 'صباحي', startsMinute: 480, endsMinute: 840 }` → its id from the answer.
3. Each status recorded: owner `POST …/packages` (with the shift) → 201; owner `GET` → 200 `[it]`;
   reception `GET` → 200, the same body; reception `POST` → 403; reception `PATCH` → 403; owner `PATCH
   { isActive: false }` → 200; owner `POST` of the same name → the name refusal; owner `POST`
   `priceAgorot: 0` → 422; stranger and admin `GET` → 404; no token → 401; **D7:** `GET
   /api/v1/spaces/<slug>` (the space's public page) → 200, and its body does not contain the package's
   name (`Select-String` on the saved body finds nothing).
4. Stop the server by its process id (a backgrounded dev task can leave `tsx watch` on the port); then
   `Get-NetTCPConnection -LocalPort 3321 -ErrorAction SilentlyContinue` prints nothing.

### 12.7 The PR number, push and PR
Just before the push, in Git Bash:
```bash
n=$(( $(gh api "repos/{owner}/{repo}/issues?state=all&per_page=1&sort=created&direction=desc" --jq '.[0].number') + 1 ))
base=$(git merge-base HEAD origin/main)
git filter-branch -f --tree-filter "grep -rl '#PRNUM' docs | xargs -r sed -i 's/#PRNUM/#$n/g'" $base..HEAD
git for-each-ref --format='%(refname)' refs/original/ | xargs -r -n1 git update-ref -d
git grep -n '#PRNUM' ; echo "expect nothing above; PR will be #$n"
git push -u origin feat/space-packages
```
(`n` is expected to be 87 if nothing opened since #86; the command decides.) Then `gh label list`
(create `feat`, `area:api`, `area:docs` if missing, each with a description and a colour), and at once:
```powershell
gh pr create --assignee @me --label feat --label area:api --label area:docs `
  --title "feat(packages): add the owner's packages" --body-file <§12.9's text, saved as a file in $env:TEMP>
```
Confirm the number GitHub gave equals `n`; if not, replace it in the documents (a fixup into the commits
that hold it) and `git push --force-with-lease`.

### 12.8 CI, CLEAN, conflicts, report
- `gh pr checks <n> --watch`, then `gh pr view <n> --json headRefOid,mergeStateStatus,statusCheckRollup`:
  green **on the pushed head** and `CLEAN`. Never merge; never rebase a `CLEAN` PR.
- **Conflicts, early:** for every other open PR, `git merge-tree --write-tree HEAD <its headRefOid>`;
  record clean or the conflicted paths. Documents only: the fast path when its turn comes (keep both,
  `format:check`, one push). Code: stop and ask.
- **The report**, `D:\masahaWorkspace\WORKER_B\PACKAGES\4_REPORT.md`, written in parts with an editor
  (UTF-8; never a lossy shell redirect): the head and the commits; each command run and not run; each
  test's red-first output; each break of §12.5 with its red output; §12.2's results; the real run's
  statuses; the owner's answer to S1–S3 as built; the problems and their solutions; anything unexpected,
  even unsolved; the conflict check; every departure from this plan with its reason; the PR number.

### 12.9 The PR description (fill the evidence from the runs)
```markdown
## Summary
The owner's packages, on the API (step 5b): a space's subscription templates, private to its staff.
- `GET /manage/spaces/:spaceId/packages`: the space's staff read every package, retired ones included,
  whole, by place then name.
- `POST` and `PATCH …/packages[/:packageId]`: the owner adds (active, placed last) and edits (partial;
  `isActive: false` retires); refused at the route for reception, then decided again under the space's
  lock; audited `package.created` / `package.edited`.
- A price above zero (DI-10) and every limit's range in `@masaha/shared/packages`; a taken name and a
  foreign shift refused on their fields by the database's keys.
- Documents: the contract, security, conventions, the plan, the overview, the map and a new capability
  document, `docs/features/packages.md`; findings 77–79 (#86's review) and 80 recorded.

## Scope
<§2 Scope>
## Acceptance criteria
<§2's checklist, ticked>
## Out of scope
<§2 Out of scope>

## Change type
feat — API code, the shared contract, tests and documents. No schema, migration or dependency; nothing in `apps/web`.

## Evidence
- `npm run lint`, `npm run typecheck` (each commit), `npm run test:unit`, `npm run test:api`,
  `npm run format:check`, `npm run check:links`, `npm run build -w @masaha/shared`: <results>.
- Seen failing first: <each test, its red line>.
- Deliberate breaks (testing §3 rule 7), each red then restored: <B1–B13>.
- Real run on 3321: <statuses, and the public page without the package's name>.
- Not run: `test:component`, the web's `build`, `check:build`, `check:classes` — no file in `apps/web`
  changed; CI runs them.

## Screenshots
None: API and documents only.

## Definition of Done checklist
- [x] Acceptance criteria met, scope kept.
- [x] Lint and typecheck clean; `packages/shared` builds.
- [x] Tests added in the owning lanes, each seen failing.
- [x] No user-facing text added (no catalogue entry: no new error code).
- [x] Authorization enforced on the server (the boundary, `requireCan`, `can()` under the lock).
- [x] Triggered documentation updated in this PR; the capability document born; the contract's
      *Endpoints* (the only deferred document) met.
- [x] One home per fact; nothing claimed that is not built.
- [x] Every claim names its test or command.
- [x] Atomic history, pushed.
```

## 13. Decisions needed from the owner

1. **S1** — a taken name answers 409 `conflict` (recommended), or keep D3's 422 `validation` with the
   three document exceptions of Appendix A.
2. **S2** — no domain cap on the counts or on a space's packages (recommended as is).
3. **S3** — the read without the share lock (recommended as is).

Everything else is the prompt's decisions as written, or the plan's own (P1–P10) inside them.

## 14. Stop and ask

- #85 is not merged; or `origin/main` changed a code file §12.1 names in a way this plan does not cover;
  or an open PR edits a code file of §7.
- A change is needed in `apps/web`, the schema, a migration or a dependency; or a `spaces` export
  (§12.2 check 4).
- More than about 40 files would change.
- Lint's level rule refuses the new module or the shared folder (§12.2 check 1).
- P2002's meta names no constraint (check 3), or a package's foreign shift is not P2003 (check 4).
- A break of §12.5 stays green.
- A failure not understood after three root-cause fixes; CI failing for a reason not reproduced locally
  after three.
- A conflict with another open PR in a code file.
- Anything in this plan proves false against the code at execution time.

## Appendix A — the documents, written out

Each block names its commit. `<today>` is the date the line is written. A header's *Last Updated*
becomes `<today>` in the first commit that edits the document.

### A.1 `docs/architecture/findings/` — C1 (77–79) and C3 (80)

**`77-the-race-helper-counts-any-waiting-backend-and-its-reach-sits-under-vitests-timeout.md`**
```markdown
# 77. The race helper counts any waiting backend, and its reach sits under Vitest's timeout

**Status:** Open · **Date:** <today>

**Evidence:** `waitingOnLock` (`apps/api/test/locks.ts:19-41`), called without `on`, counts every backend of the test database whose `wait_event_type` is `Lock` (line 30), not the request the race started: a race whose own request never reached its lock still passes once any other backend of that database waits, as `whileHeld` calls it (line 65). Its reach, `REACH_MS` (line 10), is 4 seconds, under Vitest's default test timeout of 5 seconds (`apps/api/vitest.config.ts` sets none): on a slow machine a request that hashes a password first can take longer than the reach, and the test fails though the race is sound. Found by #86's review; one test file runs at a time against its own database, so no unrelated waiter has appeared yet.

**Resolves when:** every race names the table its request waits on (`on`), `whileHeld` included, or the helper follows the request's own backend; and the reach and the race tests' timeout are set together, the reach well under the test's own limit.
```

**`78-the-owners-names-test-assumes-nothing-reads-users-before-them.md`**
```markdown
# 78. The owners' names test assumes nothing reads `users` before them

**Status:** Open · **Date:** <today>

**Evidence:** the test "reads the owners' names on the read's own connection, inside its transaction" (`apps/api/src/modules/spaces/space/space.api.test.ts:404-449`) compares the backend that waits on the space's lock (`readWaiter`, line 419) with the one that waits on the `users` table (`namesWaiter`, line 437). It proves what its title says only because nothing the read does between the lock and the names touches `users`: `get` (`apps/api/src/modules/spaces/space/space.service.ts:92-105`) takes the share lock (line 97), then reads the links (line 99), the facts (line 101) and the owners (line 102). A read of `users` added before the owners, on the transaction's connection, would be the one found waiting, so the test would pass whichever connection then read the names. Found by #86's review.

**Resolves when:** the test identifies the names' own query (by its statement, not only its backend), or a guard fails when the read touches `users` before `ownersFor`.
```

**`79-the-users-names-reader-keeps-an-optional-transaction.md`**
```markdown
# 79. The users' names reader keeps an optional transaction

**Status:** Open · **Date:** <today>

**Evidence:** `users.namesFor(ids, tx?)` (`apps/api/src/modules/users/users.service.ts:372`) and its repository's `findNames(ids, tx = db)` (`users.repository.ts:78`) take the transaction as optional. `ownersFor(spaceId, tx)` (`apps/api/src/modules/space-links/admin-spaces/adminSpaces.service.ts:31-34`) requires its own and passes it on, so the rule that a read inside a transaction never waits on a second connection ([conventions › Transactions](../../backend/conventions.md#transactions)) is held by `ownersFor`'s callers, not by the reader: a new caller inside a transaction can leave `tx` out and still compile. Its one caller without a transaction is the admin's spaces list (`adminSpaces.service.ts:61`). Found by #86's review.

**Resolves when:** `namesFor` takes its `tx` as a required `Tx | undefined`, so each caller says which it means (the list passing `undefined`), or a check refuses a read without `tx` inside `runInTransaction`.
```

**`80-the-database-still-takes-a-package-with-a-price-of-zero.md`** (C3)
```markdown
# 80. The database still takes a package with a price of zero

**Status:** Open · **Date:** <today>

**Evidence:** a package's price is above zero (the owner's decision, 2026-10-13; [packages › Decisions](../../features/packages.md#api-decisions)), and the API refuses zero in its shared schema (`priceAgorot` from 1, `@masaha/shared/packages`). The database's `packages_price_check` (`apps/api/prisma/migrations/20260929120200_front_desk/migration.sql`) still checks `price_agorot >= 0`, so a write that does not pass through the API (the seed, a script, a later module) can store a free package. A space's prices moved to `> 0` in a migration of their own (`20261012144622_space_price_above_zero`).

**Resolves when:** a migration of the front desk's steps changes `packages_price_check` to `price_agorot > 0`, with its test in `apps/api/src/db/`, as the space prices' did.
```

**`README.md`** — under *Open*, in number order after 67 (and after #85's 73, 74 as merged); C1 adds
the first three, C3 the fourth:
```markdown
- [77. The race helper counts any waiting backend, and its reach sits under Vitest's timeout](77-the-race-helper-counts-any-waiting-backend-and-its-reach-sits-under-vitests-timeout.md)
- [78. The owners' names test assumes nothing reads `users` before them](78-the-owners-names-test-assumes-nothing-reads-users-before-them.md)
- [79. The users' names reader keeps an optional transaction](79-the-users-names-reader-keeps-an-optional-transaction.md)
- [80. The database still takes a package with a price of zero](80-the-database-still-takes-a-package-with-a-price-of-zero.md)
```

**Executor check:** re-verify each `file:line` on the tree the branch is cut from (#85 is web and
documents only, so none should move); correct any that did.

### A.2 `docs/api/api-contract.md`

**§4 *Exceptions*** (C2) — a fourth bullet:
```markdown
- a space's packages (`GET /manage/spaces/:spaceId/packages`), retired ones included: a space keeps tens at most, typed by hand, and the owner's list and the front desk's picker both read them whole (§5, *Packages (managed)*; why: [packages › Decisions](../features/packages.md#api-decisions)).
```

**§5, a new section after *Managed photos*, before *Lookups (public)*:**
````markdown
### Packages (managed)

A space's packages: the subscription templates its owner keeps, private to its staff ([data-model › Operations](../architecture/data-model.md#operations)); the public's packages are the space's published prices. The endpoints sit under `/manage/spaces/:spaceId` and answer as *Managed spaces* says: without an active `OWNER` or `RECEPTION` link at the live space, `not_found` (404). The list is the staff's (🧾); every write is the owner's (🏢), and reception's is refused with `forbidden` (403) before its body is read.        [C2: the paragraph without its last clause; C3: ", and reception's … read."]

- **The terms** (C3):
  - `name`, required, 1–60 characters, NFC-normalised and trimmed, with no bidirectional controls and no control characters or line separators (`invalid_format`): one name, in the language the owner types. Another package of the space, retired or not, may not hold it;
  - `validityDays`, required: a subscription made from the package ends this many days after it starts;
  - the limits, each optional (absent or `null`): `totalDays`, `daysPerWeek` (at most 7), `hoursPerDay` (at most 24) and `totalHours`; they combine freely;
  - every count is a whole number from 1 (`out_of_range`; `invalid_format` when not whole), at most 2,147,483,647;
  - `billing`: `FIXED`, `PER_HOUR` or `PER_DAY` (`SUBSCRIPTION_BILLINGS`, `@masaha/shared/packages`; `invalid_choice` otherwise);
  - `priceAgorot`: the whole price when `FIXED`, else the rate per hour or per day, in whole agorot from 1 to 10,000,000, as a space's prices: `out_of_range` outside it (no package is free), `invalid_format` when not whole;
  - `audience`: `GENERAL` or `STUDENT` (`PRICE_AUDIENCES`, `@masaha/shared/spaces`; `invalid_choice`);
  - `shiftId`, optional: one of the space's shifts.
- **Order** (C2): a list's order is its array's: by place, then by name. (C3 appends:) A new package is placed after the last; no endpoint reorders them.
- **Retired, never deleted** (C4): `isActive: false` retires a package, which stays listed; `true` offers it again. A subscription made from a package keeps its own copy of the terms ([ADR 0010](../architecture/decisions/0010-manual-payment-ledger.md)): an edit or a retirement changes none.
- **Audit** (C3), in the change's own transaction ([conventions §6](../backend/conventions.md#6-audit)), with the package as the entity and its space as the entry's: `package.created` (`after`: its terms). (C4 appends:) `package.edited` (`before` and `after`: only the fields that changed, `isActive` included); an edit that changes nothing writes nothing.

```ts
SpacePackage = {
  id: number,
  name: string,
  validityDays: number,
  totalDays: number | null, daysPerWeek: number | null,   // its limits; null: none
  hoursPerDay: number | null, totalHours: number | null,
  billing: "FIXED" | "PER_HOUR" | "PER_DAY",              // SUBSCRIPTION_BILLINGS
  priceAgorot: number,                                   // whole agorot: the price, or the rate per hour or day
  audience: "GENERAL" | "STUDENT",                       // PRICE_AUDIENCES
  shiftId: number | null,                                // one of the space's shifts
  isActive: boolean                                      // false: retired, no longer offered
}
```

#### `GET /manage/spaces/:spaceId/packages` · 🧾        (C2)
- **200:** `SpacePackage[]` (`@masaha/shared/packages`): every package of the space, retired ones included, in order. Not paginated (§4).
- **Errors:** `not_found` (404).

#### `POST /manage/spaces/:spaceId/packages` · 🏢        (C3)
- **Body:** `{ name, validityDays, totalDays?, daysPerWeek?, hoursPerDay?, totalHours?, billing, priceAgorot, audience, shiftId? }`.
- **201:** `SpacePackage`, active and placed last. Audited `package.created`.
- **Errors:** `validation` (422), with `invalid_choice` on `shiftId` for a shift that is not one of the space's; {the name refusal}, when another package of the space, retired or not, has the name; `forbidden` (403) for reception, before the body is read, and for an owner whose link ended meanwhile; `not_found` (404).

#### `PATCH /manage/spaces/:spaceId/packages/:packageId` · 🏢        (C4)
- **Body:** any of the terms, and `isActive`; what is absent is kept, and a limit or the shift is cleared with `null`.
- **200:** `SpacePackage`. Audited `package.edited`.
- **Errors:** as the create's; `not_found` (404) for a package that is not the space's.
````
`{the name refusal}` is written, by default (S1 not approved):
```markdown
`validation` (422), with `errors.name = ["not_unique"]`
```
and with S1 approved:
```markdown
`conflict` (409), with `errors.name = ["not_unique"]`
```
The `(C2)` … `(C4)` and `[C2]` … tags are this plan's, never the document's.

**If S1 is not approved** (C3), §3's `validation` row: "Field validation failed (`errors` present)" →
"Field validation failed (`errors` present), and a package's name another package of its space holds (§5, *Packages (managed)*)".

### A.3 `docs/backend/security.md` (C3)
- Header *Built*: "`requireSpaceAccess`, mounted once on `/manage/spaces/:spaceId`, and `requireCan` on
  its photo writes;" → "…, and `requireCan` on its photo and package writes;". *Last Updated* `<today>`.
- *Authorization*, the managed-space bullet's last sentences: "The managed photo writes ask `can()`
  first, at the route, through `requireCan(action)`: a caller who may not change the photos is refused
  (403) before the request is counted or its body read; the service still decides under the lock." →
  "The managed photo and package writes ask `can()` first, at the route, through `requireCan(action)`: a
  caller who may not change them is refused (403) before the request is counted or its body read; the
  service still decides under the lock."

### A.4 `docs/backend/conventions.md`
- (C2) §7's table: `` | `packages` | `` → `` | [`packages`](../features/packages.md) | ``. *Last Updated*
  `<today>`. The header's *Built* needs nothing more: packages joins "the capabilities documented in
  `docs/features/`".
- (C3) §6's list, after "customer create, edit and archive; subscriptions created, corrected and
  ended;": a bullet "- a space's packages created and edited, a retirement included;".
- (C3, **only if S1 is not approved**) §4: "Prisma `P2002` → `conflict` with `NOT_UNIQUE` field errors."
  → "… field errors; a package's name is the one exception, a `validation` (422) on its field
  ([packages › Decisions](../features/packages.md#api-decisions))."

### A.5 `docs/architecture/data-model.md` (C3, **only if S1 is not approved**; shared)
*Conventions*: "- **Unique violations** (Prisma `P2002`) become `409 CONFLICT`." → "… become `409
CONFLICT`, except a package's name, refused as `validation` (422) on its field ([packages ›
Decisions](../features/packages.md#api-decisions))." *Last Updated* `<today>`.

### A.6 `docs/plans/v1-mvp.md` (C4)
- *Managed spaces*' *Built* line: "…the API-only profile, facts, confirmations and photo routes below."
  → "…the API-only profile, facts, confirmations, photo and package routes below."
- The packages row becomes:
  ```markdown
  | GET / POST / PATCH | `/manage/spaces/:spaceId/packages[/:packageId]` | GET 🧾 · writes 🏢 | subscription templates, listed whole, retired ones included; never public ([api-contract › Packages (managed)](../api/api-contract.md#packages-managed)) |
  ```
- *Last Updated* `<today>`.

### A.7 `docs/README.md` (C2)
Under *features/*, after the `spaces.md` line:
```markdown
- [packages.md](features/packages.md) — a space's packages, the subscription templates its owner keeps, private to its staff: listed whole, added, edited and retired (API only).
```

### A.8 `docs/project/overview.md` (C4; shared — re-read after #85)
- The Spaces line's last sentence: "The owner/reception web screen, capacity and packages remain
  planned." → "The owner/reception web screen and capacity remain planned." (If #85 reworded that
  sentence, drop only "and packages" from it.)
- A new line after the Spaces line:
  ```markdown
  - [Packages](../features/packages.md): on the API, a space's packages, its owner's subscription templates: listed whole to its staff, retired ones included, added and edited by its owner, retired rather than deleted; never public.
  ```
- *Last Updated* `<today>`.

### A.9 `docs/features/spaces.md` (shared — re-read after #85; API parts only)
- (C3) *Who uses it*, a bullet after `space-links`':
  ```markdown
  - **[`packages`](packages.md),** whose writes take the space's lock first.
  ```
- (C4) The header's last sentence: "The owner/reception web screen, capacity and packages remain
  planned." → "The owner/reception web screen and capacity remain planned." And under *What it does*:
  "The owner/reception web screen, capacity and packages / remain planned, and photos are still
  API-only." → drop "and packages" (the line becomes "…web screen and capacity remain planned…"),
  keeping whatever #85 made of "photos are still API-only". *Last Updated* `<today>`.

### A.10 `docs/features/packages.md` (new; C2 writes it, C3 and C4 add their lines)
```markdown
# Packages

> **Status:** Active · **Class:** Description — what is built, as the code shows it · **Last Updated:** <today> · **Owner:** Basel Ghoneim
> **Authority:** The `packages` capability: a space's packages, the subscription templates its owner keeps, private to its staff. Its endpoints are owned by the [API contract](../api/api-contract.md#packages-managed); its entity by the [data model](../architecture/data-model.md#operations). The API is built; no web screen yet.
> **Scope:** the API module `packages` (L2); `@masaha/shared/packages`. No web feature yet.

## What it does

- Keeps a space's packages: a name, a validity in days, optional limits (total days, days a week, hours a day, total hours), a billing (a whole price, or a rate per hour or per day) with its price, an audience, an optional shift of the space, and whether the package is still offered.
- Answers the space's staff every package, retired ones included, in order, whole.            [C2]
- Lets the owner add a package, placed last.                                                [C3]
- Lets the owner edit any of a package's terms, and retire it; a package is never deleted.   [C4]

## Who uses it

- **The space's owner,** through the API: reads, adds and edits.            [C2: "reads"; C3 "adds"; C4 "and edits"]
- **The space's reception,** through the API: reads them, for the front desk, which will choose from them when it makes a subscription.
- No web screen reads it yet. The public never does: its packages are the space's published prices ([glossary](../project/glossary.md)).

## Responsibility boundary

- **Owns** the `packages` table, the order of a space's packages, and the rule of what an edit changes.   [C2: without "and the rule…"; C4 adds it]
- **Leaves** the space, its lock and its shifts to [`spaces`](spaces.md); who may read or write to `can()` ([security › Authorization](../backend/security.md#authorization)); the subscriptions made from a package, which copy its terms, to `subscriptions` (not built).

## How it composes the platform

- Its manage router sits below `/manage/spaces/:spaceId`, behind the one boundary that admits the space's staff ([security › Authorization](../backend/security.md#authorization), [conventions › Routers](../backend/conventions.md#routers)).
- Its list is one of the contract's exceptions to pagination ([api-contract §4](../api/api-contract.md#4-pagination)).
- Its writes ask `can()` at the route, through `requireCan`, then again under the space's lock, taken through `spaces` ([conventions › Space access](../backend/conventions.md#space-access)).   [C3]
- Each change is audited by the audit writer, in the change's own transaction ([conventions §6](../backend/conventions.md#6-audit)), with the names the [contract](../api/api-contract.md#packages-managed) gives.   [C3]
- Its requests are checked by the shared schemas ([shared-package.md](../architecture/shared-package.md)).   [C3]

## Behaviour and flows

**The list.** One query reads the space's packages, by place, then by name, retired ones included, each saying whether it is offered.   [C2]

**Add.** In one transaction: the space's lock; `can()` on the links as they are under it; the package written after the last, active; its audit entry. A name another package of the space holds, retired or not, is refused by the database's key; so is a shift that is not one of the space's. Each refusal names its field.   [C3]

**Edit.** The same lock and `can()`, then the package, found among the space's own; only the fields the edit sets to a new value are written and audited, `null` clearing a limit or the shift. An edit that changes nothing writes nothing. Retiring is the same edit, `isActive: false`; a retired package stays listed, and `true` offers it again.   [C4]

## Decisions

### API decisions

- **A package is private to the space's staff: no public route reads it** (D7). *Why:* the public's packages are the space's published prices; the module has no public router. <today>, #PRNUM.   [C2]
- **The list answers every package, retired ones included, whole** (D5). *Why:* the owner's list shows the retired ones and the desk's picker offers the active ones; a space keeps tens at most, typed by hand. <today>, #PRNUM.   [C2]
- **The order is a package's place, then its name; no route reorders them** (D4). *Why:* the design orders nothing by hand; the name orders the rows written outside the API. <today>, #PRNUM.   [C2]
- **The read is one query, with no lock.** *Why:* one statement is never half of a change; the boundary has admitted the caller. <today>, #PRNUM.   [C2]
- **A new package is active, placed after the last** (D4). *Why:* as a new lookup row; the design's switch sits on the row, not in the sheet. <today>, #PRNUM.   [C3]
- **The writes are the owner's: refused at the route before the body is read, then decided again under the space's lock, on the links read there** (D1). *Why:* reception reads packages for the desk but never changes them ([ADR 0009](../architecture/decisions/0009-space-scoped-reception-role.md)); a link ended meanwhile still decides ([finding 43](../architecture/findings/43-two-races-around-a-spaces-facts.md)). <today>, #PRNUM.   [C3]
- **A package's price is above zero,** in whole agorot up to the prices' bound (the owner's DI-10). *Why:* as a space's prices: a free offer is an announcement. The database still takes zero until the desk's migration ([finding 80](../architecture/findings/80-the-database-still-takes-a-package-with-a-price-of-zero.md)). <today>, #PRNUM.   [C3]
- **A name is the package's own within its space, retired ones included,** refused on its field by the database's key, in the write's own transaction (the owner's O8). *Why:* the desk tells packages apart by name; no check before the write can race it. <today>, #PRNUM.   [C3]
- **One name, 1–60 characters, in whatever language the owner types** (the model). *Why:* the owner's label for their own staff, as long as a price's label. <today>, #PRNUM.   [C3]
- **The shift is one of the space's own, as the database's key holds it** (D6). *Why:* the key through `(shiftId, spaceId)` refuses another space's shift; `packages` reads no shift, as `spaces` reads no package ([spaces › Decisions](spaces.md#api-decisions)). <today>, #PRNUM.   [C3]
- **The limits combine freely, each only bounded** ([data model › Front desk and money](../architecture/data-model.md#front-desk-and-money)). *Why:* they only warn at check-in. <today>, #PRNUM.   [C3]
- **Each create is audited, `package.created`, with its terms** (D8). <today>, #PRNUM.   [C3]
- **No idempotency key on a create.** *Why:* a package is the owner's setup, not a desk create ([ADR 0015](../architecture/decisions/0015-idempotency-and-concurrency.md)); a create retried after a lost answer meets its own name, and the list shows it. <today>, #PRNUM.   [C3]
- **A package is retired, never deleted:** `isActive: false`, and offered again with `true` (D1, the model). *Why:* the subscriptions made from it name it. <today>, #PRNUM.   [C4]
- **An edit writes and audits only what it changes, `package.edited`, the flag included; one that changes nothing writes nothing** (D8). *Why:* as the space profile's edit; one entry per edit, since a package's flag has no public effect. <today>, #PRNUM.   [C4]
- **Editing or retiring a package changes no subscription** (D9). *Why:* a subscription copies its terms when it is made ([ADR 0010](../architecture/decisions/0010-manual-payment-ledger.md)). <today>, #PRNUM.   [C4]

## Code map

- **API:** `apps/api/src/modules/packages/`, entry `index.ts`: the service, the repository, the mapper, the manage router, and beside them the pure rule of a package's terms and of what an edit changes (`packageTerms.ts`).   [C2 without "and beside them…"; C3 "the pure rule of a package's terms"; C4 "and of what an edit changes"]
- **Shared:** `packages/shared/src/packages/`: the requests, with the billings and the limits' bounds, and the response.

## Open findings

- None.   [C2]  →  [C3] `- [80](../architecture/findings/80-the-database-still-takes-a-package-with-a-price-of-zero.md): the database still takes a package of price zero.`

## History

### API history

- #PRNUM — a space's packages, on the API: listed whole to its staff, added and edited by its owner, retired rather than deleted.   [C2 "listed whole to its staff"; C3 adds "added"; C4 the rest]
```
The `[Cn]` tags are this plan's; they never reach the file. About 900 words at C4.

## Appendix B — skill map (a map only; no step depends on a skill)

| Step | Claude Code skill |
|---|---|
| §12.1 — the folder, the reading, the branch | `start-work-item` |
| Saving this plan | `write-plan` |
| §12.3 — red first, the breaks | `superpowers:test-driven-development` (optional, workflow §10) |
| §12.2, §14 — a failure's root cause | `superpowers:systematic-debugging` (optional) |
| §12.4–§12.7 — scope, commits, push, PR | `open-pr` |
| §12.8 — the report after CI and `CLEAN` | `final-report` |
