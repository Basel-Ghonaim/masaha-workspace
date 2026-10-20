# SETTINGS — the space's operating settings and its capacity (the owner), DI-41 — the plan

> **Base:** `origin/main` at `18ab1705` (Merge #90, 2026-10-19). **Worker:** B, in `C:\dev\masaha\app-b`.
> **Folder:** `C:\dev\masaha\workspace\WORKER_B\SETTINGS\` — this plan `2_PLAN.md`; the report
> `4_REPORT_PR<n>.md`. **Branch:** `feat/space-settings`. **One PR**, about 43 files.
> **Read only from commit objects** (`git show origin/main:…`); nothing was run, built or checked out.
> Every point this plan could not prove by reading is an **executor check** (§12.2), with what to do if
> it fails.

> **Approved by the owner, 2026-10-19 — binding on the executor:**
> - **§13 as recommended:** **Q1** the stay limit in whole hours, 1–23; **Q2** capacity's ceiling 1,000;
>   **Q3** "applies at once" includes the stays already open (D5 as written); **Q4** for step 7 — with the
>   switch off and no rate, the visit closes **unpriced** and appears in the owner's «يحتاج انتباهك» for
>   the owner to price it (never closed free): written into `OPEN_DECISIONS.md` point 1 by the report, not
>   built here; **Q5** two routes, finding 94 recorded; **Q6** the two placeholder codes; **S1–S3** not
>   built. **One PR.**
> - Executed and reviewed by Claude Code, each in its own conversation. Findings start at **94** — check
>   the index on the latest `origin/main` first (worker A's OWNERS PR 3 runs in parallel and may take one);
>   renumber if taken. Its shared documents (`overview.md`, `spaces.md`, the findings index) are the
>   expected text conflicts — whichever PR merges second resolves them.

## 1. Summary

The front desk (step 7) will read a space's settings on every visit, and the full warning and the live
status need its capacity. The tables exist (`space_settings`, `space_occupancy`), but no route reads or
writes them. This item gives the **owner** (only) a managed read and a managed write for each owning
module, on the API:

- **`space-settings`** (L0): `GET` / `PATCH /manage/spaces/:spaceId/settings` — auto check-out at
  closing, the stay limit, the visit rounding rule and its minutes, the cap at the day price, student
  prices for visits, the WhatsApp reminder template (its placeholders validated), and a **new setting**:
  whether reception may type a price by hand (off by default) — the item's one schema change.
- **`occupancy`** (L4), created now with its first slice only: `GET` / `PUT
  /manage/spaces/:spaceId/capacity`; the row is created on its first write (conventions §9).
- Every write: the space's lock, `can()` on the links read under it, only what changes written,
  audited in the same transaction. Reception is refused (403) before a body is read; anyone else who is
  not the space's staff — the admin included — gets 404 from the boundary.
- **Documents only:** DI-41 (a missing student price falls back to the general one), the hand-typed
  price rule (reception only where the space allows; a reason on every one), and "a change applies
  from then on" — in the data model, ADR 0009 (revised) and the new feature documents. Steps 7–8 build
  them.

## 2. The contract

### Scope
1. A migration adds `space_settings.reception_may_type_prices BOOLEAN NOT NULL DEFAULT false`
   (Prisma `receptionMayTypePrices`); existing rows and every new space get `false`.
2. `@masaha/shared/space-settings`: the visit rounding rules, the bounds, `updateSpaceSettingsSchema`,
   the reminder template's rule (`reminderTemplate.ts`) and the `SpaceSettings` response.
3. `@masaha/shared/occupancy`: `setCapacitySchema`, the bound, `SpaceCapacity`.
4. `space-settings`: a manage router, controller, mapper, the pure `settingsChange.ts`; the service and
   repository gain the read and the edit; the service takes the space's lock as a function the
   composition root passes (§4, P1).
5. `occupancy`: a new module with the capacity only: routes, controller, service, repository.
6. `app.ts`: both routers mounted inside the managed boundary; `spaces` built before `spaceSettings`.
7. Tests (unit and API lanes) and documents (§7, Appendix A); finding 94.

### Acceptance criteria
- [ ] `GET /manage/spaces/:id/settings` answers the owner the space's eight settings; reception 403;
      a stranger, an owner of another space and an unlinked admin 404.
- [ ] `PATCH …/settings` writes only the fields set to a new value, `null` clearing the stay limit or
      the reminder template; the rounding rule and its minutes are sent together; each bound refused on
      its field (422); a patch that changes nothing writes and audits nothing.
- [ ] `GET` / `PUT …/capacity`: `null` before any capacity; a first `PUT` with a number creates the
      `space_occupancy` row; a change or a clear keeps the row and its override; the same value writes
      nothing; `0`, `1001` and a missing `capacity` are refused (422).
- [ ] Both writes take the space's lock and decide `can()` on the links under it: an owner unlinked
      while the request waited is refused 403; a space deleted meanwhile answers 404; nothing written.
- [ ] Reception's read and write are refused 403 before the body is read (an invalid body still 403).
- [ ] Audited in the change's transaction: `space.settingsEdited`, `space.capacityEdited`, with the
      fields that changed in `before` / `after`.
- [ ] `reception_may_type_prices` defaults to `false` (schema test); `masaha_b_dev`'s existing rows read
      `false` after the migration.
- [ ] The contract, the data model (DI-41, hand-typed prices, a change applies from then on), ADR 0009
      (revised), conventions, security, the two new feature documents, the map, the overview and the
      build map say what is built and nothing more.

### Out of scope
- Every web screen (screen 24, worker A later); no `apps/web` change at all.
- The platform's settings and its admin routes (step 11); `newSpaceDefaults` is unchanged (§4, D4).
- The desk's use of any value: the charge, the rounding, the cap, the student fallback, auto check-out,
  the full warning, the hand-typed price and its reason (steps 7–8).
- The reminder's sending and filling (finance, step 11); its default text (the web's catalogue).
- The live status, the override, `present`, `GET …/occupancy` (step 7); announcements; reception's
  open points 2–4.

## 3. The reading done

From `origin/main`: `CLAUDE.md`; `docs/development/workflow.md` (whole), `testing.md` (whole);
`docs/backend/conventions.md` (whole: §2 layers, §6 audit, §7 level map and modules, §8 R1–R8 and
*Space access*, §9 settings / new-space defaults / `space-settings` / `occupancy`, §13 the space's
lock); `docs/api/api-contract.md` §1–§5 to *Staff (managed)* and §6's place; `docs/architecture/
data-model.md` (*Conventions*, *Spaces*, *Setting*, *Derived values*, *Front desk and money*,
*Constraints*); `docs/backend/security.md` (*Authorization*, *Rate limits*); ADR 0002, 0008, 0009
(grep and the decision table), `docs/architecture/documentation.md` §5 (the capability template);
`docs/README.md` (the map, deferred documents); `docs/features/packages.md` (whole), `spaces.md`
(settings/capacity lines); `docs/project/overview.md` (*Built*, *Dashboard*); `docs/plans/v1-mvp.md`
(steps 5–7, 11, ordering notes, the planned API surface); the findings index and 31, 40, 93;
`docs/architecture/shared-package.md` (R1–R4); the design archive's `Owner settings.html` and
`CHANGES.md` (O2, OW-021, S9).
Code: `space-settings/*`, `platform-settings/*` (`settingKeys.ts`), `spaces/spaces.service.ts`,
`spaces.repository.ts`, `space/space.service.ts` (creation), `spaces.manage.routes.ts`, `packages/*`
(routes, controller, service, repository, mapper, `packageTerms.ts`, the API test), `space-links.
manage.routes.ts`, `shared/auth/{can,requireCan,spaceAccess,spaceLinks,index}.ts`,
`shared/audit/writeAudit.ts`, `shared/validation/validate.ts`, `db/index.ts`, `app.ts`,
`eslint.config.js` (the level map), `schema.prisma` (`Space`, `SpaceSettings`, `SpaceOccupancy`,
`Visit`, `AuditLog`), the two table migrations and `20261018091812`, `db/schema.api.test.ts`,
`spaces/space/create.api.test.ts`, `test/{factories,locks,spaces,admin}.ts`, `test/global-setup.ts`,
`packages/shared/src/{core/fieldErrors.ts,core/fields.ts,packages/*}`, `db/seed/demo.ts`.
Workspace: `DESIGN\DECISIONS\DECISIONS_OWNER.md` (O2, OW-021; OW-002 inside O2; OW-024 is not the
settings screen), `_SHARED\OPEN_DECISIONS.md`, `_DONE\STAFF\3_EXEC_PROMPT.md` §2, `_DONE\STAFF\2_PLAN.md`
(the shape). `gh pr list --state open`: none on 2026-10-19; the last number used is #90.

**What the reading established**
- `space-settings` exists minimally: `createFor` only, called by the space's creation. It is **L0**;
  `spaces`, which owns the space's lock, is **L1** — so `space-settings` cannot import it (R3).
- `occupancy` has **no folder**; it is in the level map (L4) and in `eslint.config.js`'s map already.
- `can.ts` has `space.settings.manage` and `space.capacity.manage`, both `owner`. No new action needed.
- The rounding minutes are 1–59 for `UP_AFTER_MINUTES` only, in the database (`space_settings_
  visit_rounding_check`) and in `newSpaceDefaultsSchema`; the stay limit and capacity are only `> 0` in
  the database.
- The design (O2, S9): the stay limit is whole hours 1–23; capacity optional, a whole number above
  zero; rounding minutes typed 1–59; three placeholders `{الاسم}`, `{المبلغ}`, `{المساحة}`, the amount
  required. Its comment names the capacity's route as `PATCH /manage/spaces/:id` — not this plan's (§6).
- `validate` strips unknown keys; `toFieldErrors` maps a refinement's `params.code`, and
  `not_multiple_of` to `out_of_range`.

## 4. The prompt's settled decisions, as they will be built

### D1 — scope: every field of `SpaceSettings`, and the capacity

**The settings** (`@masaha/shared/space-settings`, `requests.ts`):

```ts
export const VISIT_ROUNDINGS = ['UP_AFTER_MINUTES', 'NEAREST_HALF_HOUR', 'PER_MINUTE'] as const;
export const MAX_STAY_MINUTES = { min: 60, max: 1_380, step: 60 } as const;   // whole hours, 1–23
export const ROUNDING_MINUTES = { min: 1, max: 59 } as const;

export const updateSpaceSettingsSchema = z
  .object({
    autoCheckoutAtClosing: z.boolean(),
    maxStayMinutes: z.number().int().min(60).max(1_380).multipleOf(60).nullable(),
    visitRounding: z.enum(VISIT_ROUNDINGS),
    visitRoundingMinutes: z.number().int().min(1).max(59).nullable(),
    visitCapAtDayPrice: z.boolean(),
    visitStudentPrices: z.boolean(),
    receptionMayTypePrices: z.boolean(),
    reminderTemplate: reminderTemplateSchema.nullable(),
  })
  .partial()
  .superRefine(roundingPair);          // below
export type UpdateSpaceSettingsRequest = z.infer<typeof updateSpaceSettingsSchema>;
```
(Use the constants inside the schema; the literal numbers above are for the reader.)

**The bounds, each with its reason:**

| Field | Bound | Codes | Reason |
|---|---|---|---|
| `maxStayMinutes` | `null`, or 60–1,380 in steps of 60 | `out_of_range` (below, above, not a whole hour — `not_multiple_of`), `invalid_format` (not whole) | The design's S9: whole hours, 1 to 23. A visit is a same-day stay: closing time (or 23:59) already ends every stay, so 24 h or more never acts. Kept in minutes, the model's unit, so a finer step later is a validation change, not a schema one |
| `visitRoundingMinutes` | 1–59, exactly for `UP_AFTER_MINUTES`; `null` for the two others | `out_of_range`; `invalid_format` (not whole) | The database's `CHECK` and `newSpaceDefaultsSchema` already say so (OW-021): 0 would round every started minute up, 60 never |
| rounding pair | `visitRounding` and `visitRoundingMinutes` sent **together, or neither** | the missing one `required`; minutes `null` for `UP_AFTER_MINUTES` → `visitRoundingMinutes: ['required']`; a number for another rule → `visitRoundingMinutes: ['invalid_format']` | The rule and its N are one choice (the design's radio with its input); together, the patch is checked alone, never against the stored row, so no partial patch can reach the `CHECK` as a 500 |
| `reminderTemplate` | `null` (the catalogue's default text), or a paragraph of 1–500 characters with the placeholder rule (D1b) | `too_short`, `too_long`, `invalid_format`, `invalid_choice` | A reminder is a few lines (the design's default is about 80 characters); 500 keeps a `wa.me` link of Arabic text well inside every browser's URL limit |
| `capacity` | `null` (none), or 1–1,000 | `out_of_range`; `invalid_format`; `required` when absent | `> 0` is the database's. The ceiling catches a slip of the keyboard (400 for 40) that would leave a space never «ممتلئ»; Gaza's coworking spaces seat tens (the demo, 40). **The owner confirms 1,000** (§13, Q2) |
| the booleans | `true` / `false`, never `null` | `invalid_format` | A switch has two states |

`roundingPair` (a `superRefine` in `requests.ts`): adds a `custom` issue with `params: { code }` on the
right path, as the table says. *Executor check §12.2.3* — Zod 4 runs an object's refinement only when
its fields parsed; the unit tests assert the exact codes either way.

**D1b — the reminder template** (`packages/shared/src/space-settings/reminderTemplate.ts`, its own file
because the web's form and the finance step use the same rule, shared-package R2):

```ts
/** The placeholders a reminder may hold, as the owner types them, in either interface language. */
export const REMINDER_PLACEHOLDERS = ['{الاسم}', '{المبلغ}', '{المساحة}'] as const;
/** The one a reminder must hold: the customer is told what they owe. */
export const REMINDER_AMOUNT = '{المبلغ}';
export const REMINDER_TEMPLATE_MAX_LENGTH = 500;
/** Every `{…}` the text holds, in order: a pair of braces with no brace inside. */
export function placeholdersIn(text: string): string[];   // /\{[^{}]*\}/gu
/** A reminder: a paragraph, each placeholder from the list, the amount among them. */
export const reminderTemplateSchema = paragraphSchema(1, REMINDER_TEMPLATE_MAX_LENGTH)
  .refine(every placeholder is in REMINDER_PLACEHOLDERS, { params: { code: 'invalid_choice' } })
  .refine(placeholdersIn(text).includes(REMINDER_AMOUNT), { params: { code: 'invalid_format' } });
```
- `{الاسم}` the customer's name, `{المبلغ}` the amount they owe, `{المساحة}` the space's name; each any
  number of times. A lone brace is text. A placeholder not on the list (a typo, `{الأسم}`, `{name}`) is
  refused (`invalid_choice`), so a customer never receives a literal `{…}`. Without `{المبلغ}`:
  `invalid_format` (the design's «أضف {المبلغ}…»). The two codes differ, so the web can say which.
- The tokens are Arabic whatever the interface language: the design inserts them as they are
  (`<span dir="rtl">`). Line breaks kept, bidi controls refused — `paragraphSchema`'s rules.
- The contract says the placeholders and that the finance step fills them; it never fills them here.

**The response** (`responses.ts`):

```ts
export interface SpaceSettings {
  autoCheckoutAtClosing: boolean;
  maxStayMinutes: number | null;          // null: at closing only
  visitRounding: (typeof VISIT_ROUNDINGS)[number];
  visitRoundingMinutes: number | null;    // set exactly for UP_AFTER_MINUTES
  visitCapAtDayPrice: boolean;
  visitStudentPrices: boolean;
  receptionMayTypePrices: boolean;        // false for every new space
  reminderTemplate: string | null;        // null: the catalogue's default text
}
```

**The capacity** (`@masaha/shared/occupancy`, L4 — it imports `core` only):

```ts
export const CAPACITY_MAX = 1_000;
export const setCapacitySchema = z.object({
  capacity: z.number().int().min(1).max(CAPACITY_MAX).nullable(),   // null clears it
});
export type SetCapacityRequest = z.infer<typeof setCapacitySchema>;
export interface SpaceCapacity { capacity: number | null }           // null: none set
```

**The routes** (each under the managed boundary, so 404 for anyone without an active link):

| Route | Guard | Answer |
|---|---|---|
| `GET /manage/spaces/:spaceId/settings` | `requireCan('space.settings.manage')` | 200 `SpaceSettings` |
| `PATCH /manage/spaces/:spaceId/settings` | the same, then `validate(updateSpaceSettingsSchema)` | 200 `SpaceSettings` |
| `GET /manage/spaces/:spaceId/capacity` | `requireCan('space.capacity.manage')` | 200 `SpaceCapacity` |
| `PUT /manage/spaces/:spaceId/capacity` | the same, then `validate(setCapacitySchema)` | 200 `SpaceCapacity` |

- `PATCH` for the settings: eight fields, any of them; absent kept (as a package's edit). `PUT` for the
  capacity: one value set whole, idempotent, as `PUT /admin/spaces/:id/hidden` and `…/role` are.
- **Two routes, not one card's route:** the design's attendance card shows capacity beside the stay
  limit (O2), but they are two capabilities with different owners and consumers (conventions §7, "a
  screen is not a capability"); a composed write would need a module above both for one screen. The web
  sends two requests (finding 94 records what the card must decide).
- The capacity's path is its own, `…/capacity`, not `PATCH /manage/spaces/:id` (the prototype's
  comment): `spaces` does not own it.

**Who owns what** — the smallest honest home for capacity (the prompt's question): a new `occupancy`
module holding the **capacity only**: `index.ts`, `occupancy.manage.routes.ts`,
`occupancy.controller.ts`, `occupancy.service.ts`, `occupancy.repository.ts`. Why: conventions §9 gives
`space_occupancy` and its first write to `occupancy`, and R1 lets only it write the table; putting the
capacity in `space-settings` (L0) or `spaces` (L1) would break R1 and make the desk's step move it
again. Only what exists is created (§1): no mapper (the answer is one field), no pure rule yet.

### D2 — who edits: the owner only
- Both reads and both writes are `requireCan(<owner action>)` at the route, before `validate`, so
  reception is refused 403 before its body is read (as the staff routes); the service asks `can()`
  again under the space's lock, on `space.linksUnder(tx)` (finding 43).
- The **reads are owner-only too** (decision 2: reception reads nothing here; the desk's services read
  the values they need in steps 7–8). The read asks `can()` at the route only: it takes no lock (one
  query, as the packages' list).
- **The admin** never reaches them: the boundary answers 404 to an unlinked admin (ADR 0002, 0008:
  capacity is private from the admin). No admin route.
- No rate limit beyond the general one: owner-only, cheap writes, no hash, no file (security's table
  counts only costly or guessable work).

### D3 — DI-41, documents only
`data-model.md › Visit charge`: "student when chosen and the space's settings allow student prices for
visits, otherwise general" gains: **each student price the space does not publish falls back to the
general one, the hour and the day apart; the desk offers the student audience only where it changes a
rate** (DI-41, 2026-10-19). Also in `space-settings.md`'s decisions as a link. Built in step 7.

### D4 — hand-typed prices: the setting stored, the rule documented
- **Schema:** `receptionMayTypePrices Boolean @default(false) @map("reception_may_type_prices")`, its doc
  comment `/// Reception may type a price by hand at the desk; the owner always may. Off by default.`
  Migration `<ts>_reception_typed_prices`:
  ```sql
  -- Whether reception may type a price by hand at the desk (a custom subscription's price, a visit's
  -- charge): off for every space, the existing ones included (docs/architecture/data-model.md).
  ALTER TABLE "space_settings" ADD COLUMN "reception_may_type_prices" BOOLEAN NOT NULL DEFAULT false;
  ```
  No `CHECK`; nothing else changes. The creation's `createFor` is unchanged: the column's default gives
  the new space `false`.
- **Not in `newSpaceDefaults`.** Why: those four are the settings with no database default, copied so
  the platform governs a new space's *pricing behaviour*; this one is a fraud guard whose safe value is
  fixed, as `visitStudentPrices`' default is. Adding it would change the platform's key, its schema,
  the seed and its tests — step 11's ground — for a value no admin should flip platform-wide.
- **The rule, documented** (data model › *Front desk and money*, one new bullet, the one home; ADR 0009
  revised; `space-settings.md`): a price typed by hand at the desk — a custom subscription's price, or
  a visit's charge where the space has no rate — is typed by the owner always, by reception only where
  the space's settings allow it (off by default); **every hand-typed price, by anyone, carries a
  required reason**, recorded with who typed it. Steps 7 and 8 enforce it (`can()`, the reason's
  column). The *Visit charge* "neither →" line links to that bullet.
- `OPEN_DECISIONS.md` point 1 → settled: written in the report, not here (the workspace file), with the
  open question for step 7 (§13, Q4).

### D5 — a change applies from then on, documents only
`data-model.md`, a bullet after *Visit charge*: **A change to the space's settings or capacity applies
from then on**: a visit's rates (and its audience's student prices) are copied at check-in, its
rounding rule and the cap are read at its check-out, and the closing-time check-out, the stay limit and
the capacity apply at once, to the stays already open too. `space-settings.md` and `occupancy.md` link
it. Steps 7–8 build it. (*"to the stays already open too"* is this plan's reading of "apply at once" —
§13, Q3.)

### D6 — audit
In the write's transaction, through `writeAudit`, entity `space` / the space's id, `spaceId` set:
- `space.settingsEdited` — `before` / `after`: only the fields set to a new value (as `package.edited`);
- `space.capacityEdited` — `before: { capacity }` (`null` with no row) / `after: { capacity }`.
A write that changes nothing writes nothing and audits nothing. Both names are space-private: the
admin's future audit allowlist (conventions §6) leaves them out by default.

### D7 — out (as the prompt): no web, no platform settings, no desk use, no announcements.

### The plan's own decisions (inside the agreed item)
- **P1 — the space's lock reaches `space-settings` as a parameter.** `createSpaceSettingsService({
  runInTransaction, audit, lockSpace })`, where `lockSpace: (spaceId: number, tx: Tx) => Promise<boolean>`
  is a local type, and the composition root passes `(spaceId, tx) => spaces.lock(spaceId, tx)`. Why: the
  lock is `spaces`' (L1, conventions §13) and `space-settings` is L0: R5 solves an upward need by
  passing a parameter, as `createSpaceService` already receives `ownersFor` from `space-links`. No type
  is imported from `spaces`. `app.ts` creates `spaces` before `spaceSettings` (it takes no dependency).
- **P2 — the settings row is a fact, not a choice.** Every space has one (data model › *Checked by the
  service*). A missing row on the read or the write is a fault: the repository answers `null`, the
  service throws `new Error('The space <id> has no settings row.')` (500), as `platform-settings` treats
  a missing key; no 404, no creation. No test reaches it (§10).
- **P3 — `settingsChange.ts`**, a pure helper like `packageChange`: `settingsChange(current, edit) →
  { data, before, after }`, only the fields whose value differs; the rounding pair compared field by
  field (a rule kept with new minutes writes only the minutes).
- **P4 — the reads take no lock:** one statement is never half of a change (as packages, D's "the read
  is one query").
- **P5 — the capacity's write** under the lock: read the current capacity (`null` without a row); equal
  to the request → answer it, write nothing; else `upsert` on `spaceId` with `{ capacity }` only, so the
  override's three columns are never touched (create: the override `null`, the columns' defaults).
- **P6 — mounting:** `manage.use('/settings', createSpaceSettingsManageRouter(…))` (one path, ever);
  `manage.use(createOccupancyManageRouter(…))` with `'/capacity'` inside the router, because the module
  will add `/occupancy` and `/status-override` (the planned surface) to the same router.
- **P7 — the existing repository's `db` parameter** (`createSpaceSettingsRepository(db = prisma)`) stays:
  removing it is a refactor outside the item; the new functions use `tx: Tx = db` as `create` does.

### The code, file by file (interfaces; the commit in brackets)

| File | What | Commit |
|---|---|---|
| `apps/api/prisma/schema.prisma` | `receptionMayTypePrices` (D4) | C1 |
| `apps/api/prisma/migrations/<ts>_reception_typed_prices/migration.sql` | D4's SQL | C1 |
| `apps/api/src/db/schema.api.test.ts` | T20 | C1 |
| `packages/shared/src/space-settings/{index,requests,responses}.ts` | D1 (the template as `paragraphSchema(1, 500)` in C2) | C2 |
| `packages/shared/src/space-settings/requests.unit.test.ts` | U1–U3 | C2 |
| `packages/shared/src/space-settings/reminderTemplate.ts` (+ `.unit.test.ts`) | D1b; `requests.ts` uses `reminderTemplateSchema` | C3 |
| `apps/api/src/modules/space-settings/space-settings.repository.ts` | `SETTINGS` select; `SettingsRow`; `SettingsData = Partial<SettingsRow>`; `find(spaceId, tx = db): Promise<SettingsRow \| null>`; `update(spaceId, data, tx): Promise<SettingsRow>` (by `spaceId`) | C2 |
| `…/space-settings/settingsChange.ts` (+ `.unit.test.ts`) | P3; U7–U8 | C2 |
| `…/space-settings/space-settings.mapper.ts` | `toSpaceSettings(row): SpaceSettings` | C2 |
| `…/space-settings/space-settings.service.ts` | deps P1; `createFor` unchanged; `read(spaceId): Promise<SpaceSettings>`; `update(actor: Actor, space: LoadedSpace, edit): Promise<SpaceSettings>` — one transaction: `lockSpace` (false → 404), `can(actor, 'space.settings.manage', { links: await space.linksUnder(tx) })` (false → 403), `find` (null → P2), `settingsChange`, nothing → answer current; else `update`, `audit` | C2 |
| `…/space-settings/space-settings.controller.ts` | `read`, `update` (as packages': `signedIn`, `spaceOf`, `sendSuccess`) | C2 |
| `…/space-settings/space-settings.manage.routes.ts` | `createSpaceSettingsManageRouter(controller)`: `get('/', may, read)`; `patch('/', may, validate(updateSpaceSettingsSchema), update)` | C2 |
| `…/space-settings/index.ts` | + controller factory, router, `SpaceSettingsService` deps | C2 |
| `…/space-settings/space-settings.api.test.ts` | T1–T10 | C2, C3 (T6's template cases) |
| `packages/shared/src/occupancy/{index,requests,responses}.ts` (+ `requests.unit.test.ts`) | D1; U6 | C4 |
| `apps/api/src/modules/occupancy/occupancy.repository.ts` | `capacityOf(spaceId, tx = prisma): Promise<number \| null>`; `setCapacity(spaceId, capacity: number \| null, tx): Promise<void>` (upsert, P5) | C4 |
| `…/occupancy/occupancy.service.ts` | `createOccupancyService({ runInTransaction, audit, spaces })`: `capacity(spaceId): Promise<SpaceCapacity>`; `setCapacity(actor, space, request): Promise<SpaceCapacity>` (lock → can `space.capacity.manage` under it → P5 → audit) | C4 |
| `…/occupancy/occupancy.controller.ts`, `occupancy.manage.routes.ts`, `index.ts` | `createOccupancyManageRouter(controller)`: `get('/capacity', may, …)`, `put('/capacity', may, validate(setCapacitySchema), …)` | C4 |
| `…/occupancy/occupancy.api.test.ts` | T11–T19 | C4 |
| `apps/api/src/app.ts` | C2: `spaces` moved up, `spaceSettings` with P1's deps, `manage.use('/settings', …)`; C4: `occupancy` service, `manage.use(createOccupancyManageRouter(…))` | C2, C4 |

## 5. Stronger decisions

### S1 — the database's `CHECK`s follow the API's bounds — **not recommended**
*What:* in the same migration, tighten `space_settings_max_stay_minutes_check` to `BETWEEN 60 AND
1380 AND % 60 = 0`, and `space_occupancy_capacity_check` to `BETWEEN 1 AND 1000`. *Why it is stronger:*
a row written outside the API (the seed, a script) could not hold what the API refuses. *Cost:* two
constraint changes and their schema tests; the bounds are product choices (the design's whole hours,
an estimated ceiling) that would then need a migration to change; the API is the only writer.
*Recommendation:* keep the database's invariants (`> 0`) and the bounds in the shared schema.

### S2 — placeholders stored as neutral keys (`{name}`, `{amount}`, `{space}`) — **not recommended**
*Stronger:* one stored form whatever the language. *Cost:* the web translates on load and save; the
design's plain textarea with typed tokens becomes something else. *Recommendation:* the design's Arabic
tokens, refused when unknown (D1b).

### S3 — a strict body (unknown keys refused) on the settings `PATCH` — **not recommended**
*Stronger:* a misspelt key (`maxStayMinute`) would answer 422 instead of an empty patch. *Cost:* differs
from every other managed write (they strip); the web sends typed bodies from the shared type.
*Recommendation:* strip, as the others.

### S4 — capacity's ceiling — **recommended, planned** (1,000; §13 Q2 for the number).

### Rules the item touches, stated
- **R5 (ports, rarely):** P1 passes a function, not a port; the precedent is `ownersFor`.
- **Conventions §13:** "a future writer of any of them takes [the space's lock] too" — both writes do.
- **ADR 0009 rule 5's table:** gains the hand-typed price row (D4); nothing weakened.
- None contradicted.

## 6. Related findings

| Finding | Fold? | Why, cost |
|---|---|---|
| 43 (two races around a space's facts) | Not folded; **followed** | The writes decide under the lock on `linksUnder` (T8, T18) |
| 40 (contact settings outside the catalogue) | No | Platform settings, step 11 |
| 14 (the owner's audit screen has no design) | No | Reading the audit is step 11 |
| 31 / 39 (parameters only tests pass) | No | P7 keeps an existing `db` default; nothing new takes a test-only parameter |
| 77, 52 (the race helper) | No | Used as packages use it |
| 80 (a package price of zero in the database) | No | Packages' migration, the desk's step |

**New finding (number 94, or the next free from 94 if worker A's PR 3 took it — §12.1):**
`94. The attendance card saves two capabilities in one save` — **Open**, 2026-10-19. *Evidence:* the
design's «الحضور والحالة المباشرة» card (O2) has one «حفظ» for the capacity and the stay limit, and its
comment names `PATCH /manage/spaces/:id` for the capacity; the contract has `PUT …/capacity`
(`occupancy`) and `PATCH …/settings` (`space-settings`), two requests, so one save can half succeed
(DI-38 fails a card as a whole). *Resolves when:* screen 24's plan decides the order of the two
requests and what the card says when the second fails, or the owner splits the card's save.

## 7. The files it edits

Code (§4's table): 29 files under `apps/api` and `packages/shared`. **Nothing in `apps/web`** (no shared
type the web imports changes; no error code). **No dependency.**

Documents (14): `docs/api/api-contract.md`, `docs/architecture/data-model.md`, `docs/architecture/
decisions/0009-space-scoped-reception-role.md`, `docs/backend/conventions.md`, `docs/backend/
security.md`, `docs/features/space-settings.md` (new), `docs/features/occupancy.md` (new),
`docs/README.md`, `docs/project/overview.md`, `docs/features/spaces.md`, `docs/plans/v1-mvp.md`,
`docs/architecture/findings/94-the-attendance-card-saves-two-capabilities-in-one-save.md` (new),
`docs/architecture/findings/README.md`. Total ≈ 43.

**Shared with worker A's OWNERS PR 3 — likely text conflicts** (each side keeps its own section; the
fast path, workflow §9 *Conflicts*):
- `docs/project/overview.md` — this item appends two *Built* lines (*Space settings*, *Occupancy*) and
  removes "and capacity" from the *Spaces* line's "The owner/reception web screen and capacity remain
  planned" — **the same line worker A's PR likely rewrites** (the owner's web screen). Conflict likely.
- `docs/features/spaces.md` — removes "and capacity" from the header's *Authority* sentence and from
  the paragraph under *What it does* ("The owner/reception web screen and capacity remain planned") —
  the sentences worker A likely edits. Conflict likely.
- `docs/architecture/findings/README.md` — one line under *Open* (94); worker A may append theirs.
  Conflict likely, trivial.
- Not touched here: `docs/features/space-links.md`, `docs/frontend/architecture.md`.
No code file is shared with any open item (none is open on 2026-10-19).

## 8. Design issues

None: the item builds no screen. The one design point the API exposes is finding 94.

## 9. Tests — lane, title, the break each catches

Every test is seen failing first (its red output into the report); every break of §12.5 is made once,
seen red, restored from its backup. Titles are written as below.

### Unit — `packages/shared/src/space-settings/requests.unit.test.ts` [C2]
- **U1** `takes a stay limit of whole hours from 1 to 23, or null to remove it` — 60, 1380, `null` pass;
  59, 1440 and 90 → `maxStayMinutes: ['out_of_range']`; 60.5 → `['invalid_format']`. *Breaks:* B1
  (`max` 1440), B2 (`min` 1), B3 (no `multipleOf`).
- **U2** `takes the rounding rule and its minutes together: 1 to 59 for "up after N minutes", none for
  the others` — `{UP, 15}`, `{PER_MINUTE, null}`, `{NEAREST_HALF_HOUR, null}` pass; `{UP, 0}` / `{UP, 60}`
  → `out_of_range`; `{UP, null}` → `visitRoundingMinutes: ['required']`; `{PER_MINUTE, 15}` →
  `['invalid_format']`; `{ visitRoundingMinutes: 15 }` → `visitRounding: ['required']`; `{ visitRounding:
  'UP_AFTER_MINUTES' }` → `visitRoundingMinutes: ['required']`; `'ROUND'` → `invalid_choice`. *Breaks:* B4
  (pair rule removed), B5 (`max` 60), B6 (`min` 0).
- **U3** `keeps what a patch leaves out, and refuses null for a switch` — `{}` parses to `{}`; each of
  the four booleans `null` → `['invalid_format']`. *Break:* B7 (`receptionMayTypePrices` made
  `.nullable()`).

### Unit — `packages/shared/src/space-settings/reminderTemplate.unit.test.ts` [C3]
- **U4** `takes a reminder with the amount, each placeholder any number of times, a lone brace and line
  breaks kept` — the design's default text; `{المبلغ}` twice; `"{ {المبلغ}"`; `"a\r\nb {المبلغ}"` →
  `"a\nb {المبلغ}"`; `placeholdersIn` answers `['{الاسم}','{المساحة}','{المبلغ}']` for a hand-written text.
- **U5** `refuses a reminder without the amount, with a placeholder off the list, empty or over 500
  characters` — no `{المبلغ}` → `reminderTemplate: ['invalid_format']`; `{الأسم} {المبلغ}` and `{name}
  {المبلغ}` → `['invalid_choice']`; `''` → `['too_short']`; 501 characters → `['too_long']`; `null`
  passes through `updateSpaceSettingsSchema`. *Breaks:* B8 (list check removed), B9 (amount check
  removed), B10 (`max` 5000), B11 (`min` 0).

### Unit — `packages/shared/src/occupancy/requests.unit.test.ts` [C4]
- **U6** `takes a capacity from 1 to 1,000, or null to clear it, and requires the field` — 1, 1000,
  `null` pass; 0, 1001 → `capacity: ['out_of_range']`; 1.5 and `'40'` → `['invalid_format']`; `{}` →
  `['required']`. *Breaks:* B12 (`max` 10000), B13 (`min` 0), B14 (`.optional()` added).

### Unit — `apps/api/src/modules/space-settings/settingsChange.unit.test.ts` [C2]
- **U7** `changes only the fields set to a new value, each with its value before and after` — current
  row, an edit of three fields of which one is unchanged and one `null` → `data`/`before`/`after` of the
  two. *Break:* B15 (the comparison dropped: every requested field kept).
- **U8** `changes nothing for an empty edit or an edit of the same values` — `data` `{}`.

### API — `apps/api/src/db/schema.api.test.ts` [C1]
- **T20** `turn reception's hand-typed prices off by default` — `createSettings` (no field) →
  `receptionMayTypePrices: false`. *Break:* B16 (`ALTER … SET DEFAULT true` on `masaha_b_test`).

### API — `apps/api/src/modules/space-settings/space-settings.api.test.ts` [C2; T6's template cases C3]
Setup as `packages.api.test.ts`: the space and another, a settings row each (the four defaults, the
other space's distinct), owner, reception (a `RECEPTION` link), stranger, unrelated owner, admin.
- **T1** `answers the owner the space's settings, and only its own` — the other space created first with
  different values; the owner's read equals the row written by hand, all eight fields. *Break:* B17
  (`find` reads `findFirst` with no `where`).
- **T2** `answers not_found to a stranger, an owner of another space and an unlinked admin, on the read
  and the edit, changing nothing` — and no audit. *Break:* B18 (the router mounted outside the boundary:
  `api.use('/manage/spaces/:spaceId/settings', requireAuth(), loadSpaceLinks(…), router)`).
- **T3** `refuses reception's read and edit with 403 before reading the body, changing nothing` — the
  edit with `{ maxStayMinutes: 0 }` and with a valid body. *Breaks:* B19 (no `may` on `GET`), B20 (no
  `may` on `PATCH`), B21 (`may` after `validate`).
- **T4** `edits what the patch sets, clears with null, and audits space.settingsEdited with only the
  fields that changed` — patch `{ autoCheckoutAtClosing: false, maxStayMinutes: 240, visitCapAtDayPrice:
  <same>, receptionMayTypePrices: true, reminderTemplate: 'عليك {المبلغ}' }` → 200 with the new values;
  the row; one entry, `before`/`after` of four fields (not the cap); the other space's row unchanged;
  then `{ maxStayMinutes: null, reminderTemplate: null }` clears both, a second entry. *Break:* B22 (the
  audit records the whole request).
- **T5** `changes the rounding rule and its minutes together` — `{ PER_MINUTE, null }`, then `{ UP, 20 }`;
  each stored; the second entry's `before` `{ visitRounding: 'PER_MINUTE', visitRoundingMinutes: null }`.
- **T6** `refuses a bound on its field, writing nothing` — `maxStayMinutes: 1440`, `visitRoundingMinutes:
  60` with its rule, a rule without its minutes, and [C3] a template without `{المبلغ}` and one with
  `{name}` → 422 with each field's code; row unchanged; no audit. *Break:* B23 (`validate` removed from
  the `PATCH`).
- **T7** `writes nothing for a patch that changes nothing` — `{}` and the stored values → 200 the
  settings; no entry; `updatedAt` unchanged. *Break:* B24 (the empty-change return removed).
- **T8** `decides an edit on the links under the space's lock: an owner unlinked meanwhile is refused` —
  `whileHeld` as packages'. *Break:* B25 (`can()` on `space.links`).
- **T9** `refuses an edit to a space deleted while it waited for its lock, and writes nothing`. *Break:*
  B26 (`lockSpace`'s answer ignored).

### API — `apps/api/src/modules/occupancy/occupancy.api.test.ts` [C4]
Same callers; `createSpace` makes no occupancy row.
- **T11** `answers the owner no capacity before one is set, and the capacity once it is` — `{ capacity:
  null }`; a row (30) by hand → 30; another space's row (99) never answered.
- **T12** `answers not_found to a stranger, an owner of another space and an unlinked admin, on the read
  and the write, writing nothing` — no row, no audit. *Break:* B27 (router outside the boundary).
- **T13** `refuses reception's read and write with 403 before reading the body, writing nothing` — `{
  capacity: 0 }` and `{ capacity: 30 }`. *Breaks:* B28 (no `may` on `GET`), B29 (no `may` on `PUT`).
- **T14** `sets a first capacity, creating the space's occupancy row, and audits space.capacityEdited` —
  `PUT { capacity: 40 }` → 200 `{ capacity: 40 }`; the row with the override `null`; `before: { capacity:
  null }`, `after: { capacity: 40 }`.
- **T15** `changes and clears a capacity, keeping the row and its override` — a row with capacity 30 and
  an override (state, until, by); `PUT 50`, then `PUT null`; the override's three columns unchanged; two
  entries. *Break:* B30 (the upsert's `update` also writes the override's columns `null`).
- **T16** `writes nothing for the capacity it already has, a null with no row included` — `PUT null`
  with no row → no row, no entry; `PUT 30` on 30 → no entry. *Break:* B31 (the equality check removed).
- **T17** `refuses a capacity out of range or missing, on its field, writing nothing` — 0, 1001, `{}` →
  422; no row. *Break:* B32 (`validate` removed from the `PUT`).
- **T18** `decides a write on the links under the space's lock: an owner unlinked meanwhile is refused`.
  *Break:* B33 (`can()` on `space.links`).
- **T19** `refuses a write to a space deleted while it waited for its lock, writing nothing`. *Break:* B34
  (`spaces.lock`'s answer ignored).

### Not tested, and said
- P2's fault (a space without its settings row) — unreachable through the API; a deleted row would only
  prove the `throw`. Review Focus.
- DI-41, the hand-typed rule and "from then on" — documents only; steps 7–8 test them.
- `masaha_b_dev`'s backfill — checked once in the real run (§12.6), not a test: a migration's
  `ADD COLUMN … DEFAULT` is PostgreSQL's.

## 10. Review Focus — the inputs no planned test exercises
1. A space whose settings row is missing (P2: 500, by design).
2. A `PATCH` with several invalid fields at once: whether Zod 4 still runs `roundingPair` (§12.2.3) —
   the codes of the other fields are right either way; the pair's may be absent until they are fixed.
3. Placeholders in other Unicode forms (an `{المبلغ}` typed with a decomposed letter): NFC first, then
   the exact match; not tested beyond NFC's own guarantee.
4. A template of exactly 500 characters with placeholders: the length counts the tokens as typed.
5. Two owners editing the settings at once: serialized by the space's lock; the second sees the first's
   row (no test: the lock's order is proven by T8/T9's shape).
6. A capacity `PUT` racing the step-7 override write (not built): the upsert writes `capacity` only.
7. `lockSpace` passed as a lambda (P1): `app.ts` order — a wrong order fails at the first request only.

## 11. The commits

| # | Subject | Chars | Holds |
|---|---|---|---|
| C1 | `feat(space-settings): gate hand-typed prices` | 44 | D4: schema, migration, T20; data-model (*SpaceSettings* entity line, the *Hand-typed prices* bullet, *Visit charge*'s link), ADR 0009 revised |
| C2 | `feat(space-settings): edit a space's settings` | 45 | D1 (settings), D2, D3, D5 (settings half), D6 (settings), P1–P4, P6–P7: shared `space-settings` (template as a paragraph), the module's files, `app.ts`; U1–U3, U7–U8, T1–T9; docs: contract *Settings (managed)*, `space-settings.md`, the map, conventions, security, data-model (DI-41, from then on), overview, v1-mvp (settings) |
| C3 | `feat(space-settings): add reminder placeholders` | 47 | D1b: `reminderTemplate.ts`, U4–U5, T6's template cases; contract's placeholder lines; `space-settings.md` decision |
| C4 | `feat(occupancy): set a space's capacity` | 39 | D1 (capacity), D2, D6 (capacity), P5–P6: shared `occupancy`, the module, `app.ts`; U6, T11–T19; docs: contract *Capacity (managed)*, `occupancy.md`, the map, conventions, security, overview, `spaces.md`, v1-mvp (capacity), finding 94 and its index line |

Each commit holds its code, tests and documents; lint and typecheck green on each. Every new decision
and history line ends with `2026-10-19, #PRNUM`. **The PR's title:** `feat(space-settings): edit a
space's settings` (45).

## 12. Verification and the procedure

### 12.1 Before the branch
```powershell
Set-Location C:\dev\masaha\app-b
git fetch origin
git status --short --branch            # clean, detached at origin/main
git log --oneline -5 origin/main
gh pr list --state open --json number,title,headRefName,headRefOid,files
git diff --name-status 18ab1705 origin/main
```
**A change since `18ab1705`** to a code file of §4's table, to `shared/auth/*`, `shared/audit/*`,
`shared/validation/*`, `spaces/spaces.service.ts`, `spaces/space/space.service.ts`, `apps/api/test/*`,
`schema.prisma`, `eslint.config.js` or `packages/shared/src/core/*`: re-read it; **if it contradicts this
plan, stop and ask.** A new migration on `main`: it is fine; this item's migration is created after it.
An open PR (worker A's) that edits a code file of §4: stop and ask. Its documents: re-read the shared
ones on the merged tree before editing. **The finding's number:** `git show
origin/main:docs/architecture/findings/README.md | Select-String '\[9[4-9]\.'` — the first free number from
94 is this item's (and its file name). Then:
```powershell
git switch --no-track -c feat/space-settings origin/main
docker start masaha-postgres-1         # never npm run db:up; never npm ci
npm run build -w @masaha/shared
```
`apps/api/.env` must name `masaha_b_dev` / `masaha_b_test` and `PORT=3321` (check the names with
`Select-String`; never print the file).

**One full test run at a time on this machine.** Before each full lane:
```powershell
Get-CimInstance Win32_Process -Filter "Name = 'node.exe'" |
  Where-Object { $_.CommandLine -match 'vitest' } | Select-Object ProcessId, CommandLine
```
A line under `C:\dev\masaha\app\` (worker A): wait for it to end.

### 12.2 First checks (each when its code exists)
1. **The migration, created once** (after the schema edit):
   ```powershell
   npm exec -w @masaha/api -- prisma migrate dev --create-only --name reception_typed_prices
   Get-ChildItem apps/api/prisma/migrations | Select-Object -Last 2
   ```
   Run it **once**, then list the folder (a second `--create-only` applies the first to the dev
   database). Replace the generated SQL with D4's (keep Prisma's own line if it differs only in
   quoting). *On a data-loss refusal* (not expected: a column with a default): `prisma migrate diff
   --from-migrations apps/api/prisma/migrations --to-schema-datamodel apps/api/prisma/schema.prisma
   --script` into the folder, and say so. Then `npm run db:migrate` (applies it to `masaha_b_dev`;
   regenerates the client — check `apps/api/src/generated/prisma/models/SpaceSettings.ts` names
   `receptionMayTypePrices`, else `npm exec -w @masaha/api -- prisma generate`). `masaha_b_test` is
   migrated by the API lane's global setup (`migrate deploy`).
2. **The backfill** on `masaha_b_dev`: `docker exec masaha-postgres-1 psql -U <the .env user> -d
   masaha_b_dev -c "SELECT count(*), count(*) FILTER (WHERE reception_may_type_prices) FROM
   space_settings"` → `n | 0`; into the report.
3. **Zod's refinement order:** after U2 is written, run it once with a body that fails `maxStayMinutes`
   and the pair at once; record whether both codes appear. Either is acceptable (Review Focus 2); a
   **crash** or a code on the wrong path: stop and ask.
4. **The level rule:** `npm run lint` after C2 passes with `space-settings` importing only `db`,
   `shared/*`, `@masaha/shared/{core,space-settings}`, and after C4 with `occupancy` importing `spaces`
   and `@masaha/shared/{core,occupancy}`. A refusal: stop and ask (it means P1 or the level map is wrong).
5. **`AuditValues` and the rounding enum:** the mapper's `satisfies SpaceSettings` compiles against
   Prisma's `VisitRounding`; if not, map through `VISIT_ROUNDINGS` — never a cast.
6. **Upsert's statement** (P5): no nested write; if Prisma warns about a nested write in an interactive
   transaction (finding 11), use `findUnique` + `create` / `update` under the lock instead, and say so.

### 12.3 Implement, commit by commit
Stage **by path** (`git add <path> …`; never `-A` or `.`); `git status` before each commit; after each
commit `npm run lint` and `npm run typecheck`. Inside each commit: the test first, run red in its lane
(the output into the report), then the code, then green, then its documents (Appendix A, tagged by
commit). No error code is added (the refusals use the field-error codes and the existing types).

**A fix before the push** folds into its commit:
```powershell
git commit --fixup=<sha> -- <paths>
$env:GIT_SEQUENCE_EDITOR=':'; git rebase -i --autosquash $(git merge-base HEAD origin/main); Remove-Item Env:GIT_SEQUENCE_EDITOR
git rebase -x "npm run lint && npm run typecheck" $(git merge-base HEAD origin/main)
```

### 12.4 Verification on the head (phase 4)
One at a time: `npm run lint` · `npm run typecheck` · `npm run test:unit` · `npm run test:api` ·
`npm run format:check` · `npm run check:links` · `npm run build -w @masaha/shared`. Also:
`git grep -n "#PRNUM"` lists only documents (before §12.7); `git diff --stat origin/main -- apps/web
package.json package-lock.json` is empty. **Not run, with why:** `test:component`, the web's `build`,
`check:build`, `check:classes` — no `apps/web` file changes and no type it imports; CI runs them on the
pushed head.

### 12.5 The breaks (testing §3 rule 7), each recorded
For each: copy the file to `$env:TEMP\settings-breaks\` (a backup), make the one edit, run the named
test file in its lane, copy the red lines into the report, restore **from the backup** (never `git
checkout`; keep `newline=""` / no CRLF change if a script copies), run it green, then `git diff --stat`
shows only the item's own work.

| # | Test | File | The edit |
|---|---|---|---|
| B1 | U1 | shared `space-settings/requests.ts` | stay `max` 1440 |
| B2 | U1 | same | stay `min` 1 |
| B3 | U1 | same | `multipleOf(60)` removed |
| B4 | U2 | same | `roundingPair` removed |
| B5 | U2 | same | minutes `max` 60 |
| B6 | U2 | same | minutes `min` 0 |
| B7 | U3 | same | `receptionMayTypePrices` `.nullable()` |
| B8 | U5 | `reminderTemplate.ts` | the list refinement removed |
| B9 | U5 | same | the amount refinement removed |
| B10 | U5 | same | `max` 5000 |
| B11 | U5 | same | `min` 0 |
| B12 | U6 | shared `occupancy/requests.ts` | `max` 10000 |
| B13 | U6 | same | `min` 0 |
| B14 | U6 | same | `.optional()` added |
| B15 | U7 | `settingsChange.ts` | the value comparison removed |
| B16 | T20 | `masaha_b_test` | `docker exec masaha-postgres-1 psql -U <user> -d masaha_b_test -c "ALTER TABLE space_settings ALTER COLUMN reception_may_type_prices SET DEFAULT true"`; T20 red; restore with `SET DEFAULT false` by the same command; T20 green |
| B17 | T1 | `space-settings.repository.ts` | `find` as `findFirst({ select })`, no `where` |
| B18 | T2 | `app.ts` | the settings router mounted outside `manage` (`api.use('/manage/spaces/:spaceId/settings', requireAuth(), loadSpaceLinks(…), router)`) |
| B19 | T3 | `space-settings.manage.routes.ts` | `GET` without `may` |
| B20 | T3 | same | `PATCH` without `may` |
| B21 | T3 | same | `may` after `validate` |
| B22 | T4 | `space-settings.service.ts` | `before`/`after` from the whole request |
| B23 | T6 | `space-settings.manage.routes.ts` | `validate` removed |
| B24 | T7 | `space-settings.service.ts` | the empty-change return removed |
| B25 | T8 | same | `can()` on `space.links` |
| B26 | T9 | same | `lockSpace`'s answer ignored |
| B27 | T12 | `app.ts` | the occupancy router mounted outside `manage`, as B18 |
| B28 | T13 | `occupancy.manage.routes.ts` | `GET` without `may` |
| B29 | T13 | same | `PUT` without `may` |
| B30 | T15 | `occupancy.repository.ts` | the upsert's `update` also writes the override's three columns `null` |
| B31 | T16 | `occupancy.service.ts` | the equality check removed |
| B32 | T17 | `occupancy.manage.routes.ts` | `validate` removed |
| B33 | T18 | `occupancy.service.ts` | `can()` on `space.links` |
| B34 | T19 | same | `spaces.lock`'s answer ignored |

**A break that stays green: stop and ask.**

### 12.6 The real run (API on 3321, `masaha_b_dev`)
1. `npm run dev -w @masaha/api` in the background; `curl.exe -s http://localhost:3321/health` →
   `db: up`.
2. **The owner:** if `masaha_b_dev` has the demo space (`demo-owner@example.com`), sign in with
   `SEED_DEMO_PASSWORD` read from `apps/api/.env` into a variable, never printed; else, as the
   `SEED_ADMIN_*` admin, create a space and an owner (`POST /api/v1/admin/owners`), and make the forced
   change. Reception: the demo's, or one the owner adds (`POST …/staff`).
3. As the owner: `GET …/settings` → 200, `receptionMayTypePrices: false`; `PATCH { maxStayMinutes: 240,
   receptionMayTypePrices: true }` → 200; `PATCH { maxStayMinutes: 90 }` → 422 `out_of_range`; `PATCH {
   reminderTemplate: "مرحبًا {الاسم}" }` → 422 `invalid_format`; `PATCH { visitRounding: "PER_MINUTE",
   visitRoundingMinutes: null }` → 200; `GET …/capacity` → the demo's 40 (or `null`); `PUT { capacity: 35 }`
   → 200; `PUT { capacity: 0 }` → 422. As reception: `GET …/settings` and `PUT …/capacity` → 403. As
   the admin: `GET …/settings` → 404. The audit rows (`SELECT action, before, after FROM audit_logs
   ORDER BY id DESC LIMIT 4` through `psql`) → `space.settingsEdited` ×2, `space.capacityEdited`.
4. Stop the server by its process id (the `tsx watch` child and the server, memory *stop dev server*);
   `Get-NetTCPConnection -LocalPort 3321 -ErrorAction SilentlyContinue` prints nothing.

### 12.7 The PR number, push and PR
Just before the push, in Git Bash:
```bash
n=$(( $(gh api "repos/{owner}/{repo}/issues?state=all&per_page=1&sort=created&direction=desc" --jq '.[0].number') + 1 ))
base=$(git merge-base HEAD origin/main)
git filter-branch -f --tree-filter "grep -rl '#PRNUM' docs | xargs -r sed -i 's/#PRNUM/#$n/g'" $base..HEAD
git for-each-ref --format='%(refname)' refs/original/ | xargs -r -n1 git update-ref -d
git grep -n '#PRNUM' ; echo "expect nothing above; PR will be #$n"
git push -u origin feat/space-settings
```
Then `gh label list` (create `feat`, `area:api`, `area:docs` if missing, each with a description and a
colour), and at once:
```powershell
gh pr create --assignee @me --label feat --label area:api --label area:docs `
  --title "feat(space-settings): edit a space's settings" --body-file <§12.9's text, saved in $env:TEMP>
```
GitHub's number must equal `n`; if not, replace it in the documents (a fixup into the commits that hold
it) and `git push --force-with-lease`.

### 12.8 CI, CLEAN, conflicts, report
- `gh pr checks <n> --watch`, then `gh pr view <n> --json headRefOid,mergeStateStatus,statusCheckRollup`:
  green **on the pushed head** and `CLEAN`. Never merge; never rebase a `CLEAN` PR.
- **Conflicts, early:** for every other open PR, `git merge-tree --write-tree HEAD <its headRefOid>`;
  record clean or the conflicted paths. Documents only (§7's three expected): the fast path when its
  turn comes (keep both sides, `format:check`, one push). Code: stop and ask.
- **The report**, `C:\dev\masaha\workspace\WORKER_B\SETTINGS\4_REPORT_PR<n>.md`, written in parts
  (UTF-8): the head and the commits; each command run and not run; each test's red-first output; each
  break with its red lines; §12.2's results; the real run's statuses; the owner's answers to §13 as
  built; the problems and their solutions; anything unexpected, even unsolved; the conflict check;
  every departure from this plan with its reason; and **the update of
  `C:\dev\masaha\workspace\_SHARED\OPEN_DECISIONS.md` point 1**, written there as settled: «السماح
  للاستقبال بالأسعار اليدوية» stored (#n, off by default); the owner always may; a reason on every
  hand-typed price; enforced by steps 7 (visits) and 8 (subscriptions) — with §13 Q4 carried to step 7.

### 12.9 The PR description (fill the evidence from the runs)
```markdown
## Summary
The owner's settings and capacity, on the API, ahead of the front desk (step 7).
- `GET` / `PATCH /manage/spaces/:id/settings` (`space-settings`): auto check-out, the stay limit (whole hours 1–23), the rounding rule with its minutes (1–59, sent together), the day-price cap, student prices for visits, the WhatsApp reminder (placeholders checked), and a new switch: reception may type prices by hand (off by default; a migration).
- `GET` / `PUT /manage/spaces/:id/capacity` (`occupancy`, its first slice): 1–1,000 or none; the row created on its first write.
- Owner only: reception 403 before the body is read; everyone else 404; every write under the space's lock, audited.
- Documents: DI-41 (the student fallback), the hand-typed price rule (ADR 0009 revised), "a change applies from then on"; two new feature documents; finding 94.

## Scope / Acceptance criteria / Out of scope
<§2>

## Change type
feat — API code, a migration, the shared contract, tests and documents. No `apps/web` change, no dependency, no error code.

## Evidence
- `npm run lint`, `npm run typecheck` (each commit), `test:unit`, `test:api`, `format:check`, `check:links`, `build -w @masaha/shared`: <results>.
- Seen failing first: <each test, its red line>.
- Deliberate breaks, each red then restored: <B1–B34>.
- Real run on 3321: <statuses>.
- Not run: `test:component`, the web's `build`, `check:build`, `check:classes` — no web change; CI runs them.

## Screenshots
None: API and documents only.

## Definition of Done checklist
- [x] Acceptance criteria met, scope kept.
- [x] Lint and typecheck clean; `packages/shared` builds.
- [x] Tests added in the owning lanes, each seen failing.
- [x] No hardcoded user-facing text (no web change; the API sends codes only).
- [x] Authorization enforced on the server (the boundary, `requireCan`, `can()` under the lock).
- [x] Triggered documentation updated in this PR; the contract's *Endpoints* met.
- [x] One home per fact; nothing claimed that is not built.
- [x] Every claim names its test or command.
- [x] Atomic history, pushed.
```

### The executor's stop rule — a test you cannot run stops the work
A test **failing** because its code is not written yet is the plan's red step — normal. A test, lane,
break or real-run step you **cannot run** is not: it errors before any test runs (database unreachable,
Docker down, a port taken, a module or `dist` missing, a migration pending or failing, `No test files
found`, a Vitest or TypeScript startup error, the whole run timing out, a crash with no result). **Then stop
at once** — never skip, `.skip` or delete a test, never change a config, a timeout, `.env`, a script or a
lane, never mock what the plan does not, never run a narrower command and call it the lane, never call it
"flaky". **A plan that proves false against the code:** stop, say exactly what, offer the fix — do not choose
it. **A security break that stays green: stop.** Write the command, its exact error and where you were into
the report; reply `Status: STOPPED`.

**Never claim a result you did not see:** a command passed only if you saw its own output say so; copy that
line.

## 13. Decisions needed from the owner

1. **Q1 — the stay limit's bound:** whole hours 1–23 (60–1,380 minutes in steps of 60), as the design's
   S9. A finer limit (any minute from 15 to 1,439) changes U1's lines and the contract only.
2. **Q2 — capacity's ceiling, 1,000** (S4). Another number changes `CAPACITY_MAX`, U6 and the contract;
   no ceiling at all drops B12.
3. **Q3 — "apply at once" includes the stays already open** (D5): a lower stay limit, or the closing
   check-out turned on, acts on visitors already in. The other reading (only stays that start after the
   change) is step 7's to build; it changes D5's one line.
4. **Q4 — for step 7, not built here:** with the switch off, what reception does with a visit whose
   space has no rate at all (the charge must be typed): leave it for the owner, or close it uncharged.
   Carried into `OPEN_DECISIONS.md` point 1 (§12.8).
5. **Q5 — two routes for the attendance card** (D1): capacity and the settings stay two capabilities;
   the card's half-failure is finding 94, for screen 24's plan. One composed write is the alternative (a
   module above both for one screen), not recommended.
6. **Q6 — the placeholder codes** (D1b): `invalid_format` without `{المبلغ}`, `invalid_choice` for one
   off the list. Say if the web would rather have one code.
7. **S1–S3** — not recommended, not planned; say if any is wanted.
8. **The size:** about 43 files — one PR.

## 14. Stop and ask

- `origin/main` changed a code file §12.1 names in a way this plan does not cover; or an open PR edits
  a code file of §4.
- A change is needed in `apps/web`, a dependency, a new error code, or a second schema change.
- More than about 60 files would change.
- The migration cannot be made as §12.2.1 says.
- The level rule refuses P1's wiring or `occupancy`'s imports (§12.2.4).
- Zod's refinement crashes or puts a code on the wrong path (§12.2.3).
- A break of §12.5 stays green.
- A failure not understood after three root-cause fixes; CI failing for a reason not reproduced locally
  after three.
- A conflict with another open PR in a code file.

---

## Appendix A — the documents, line by line (the commit in brackets)

Every new decision and history line ends with `2026-10-19, #PRNUM`; *Last Updated* 2026-10-19 on each
document changed.

1. **`docs/architecture/data-model.md`**
   - *SpaceSettings* entity line: "…student prices for visits (on by default), **whether reception may
     type a price by hand (off by default),** and the WhatsApp reminder template…" [C1]
   - *Front desk and money*, a new bullet after *Visit charge*: **Hand-typed prices** — D4's rule, in
     two sentences; *Visit charge*'s "neither → the desk types the amount, recorded as a desk-set price
     with who set it" gains "under the rule of [hand-typed prices](#front-desk-and-money)". [C1]
   - *Visit charge*: D3's sentence (DI-41). [C2]
   - A bullet after *Hand-typed prices*: D5's sentence. [C2]
2. **`docs/architecture/decisions/0009-space-scoped-reception-role.md`** — a third *Revised* line: `>
   **Revised:** 2026-10-19 — rule 5: reception types a price by hand only where the space's settings
   allow it, off by default; every hand-typed price, the owner's included, carries a reason. #PRNUM`;
   rule 5's table gains the row `| Type a price by hand (a custom subscription's, or a visit's charge
   with no rate), with a reason | where the space allows it | ✓ |` after "New customer; subscription…".
   [C1]
3. **`docs/api/api-contract.md`** — *Last Updated*.
   - A new section **`### Settings (managed)`** after *Staff (managed)*: the opening paragraph (under the
     boundary, every route the owner's 🏢, reception 403 before a body is read, the admin never); the
     settings with their bounds and codes (D1's table, as sentences); the rounding pair; `null` for the
     stay limit and the reminder; the audit `space.settingsEdited`; "a change applies from then on" as a
     link to the data model; the `SpaceSettings` shape; `#### GET …/settings · 🏢` (200, errors 403
     reception, 404) and `#### PATCH …/settings · 🏢` (body: any of the eight; 200; errors 422 with the
     codes, 403 reception before the body is read and an owner unlinked meanwhile, 404 also for a space
     deleted meanwhile). [C2] The reminder's placeholders, their meanings, the two codes, "the debt
     reminder (not built) fills them". [C3]
   - A new section **`### Capacity (managed)`** after it: private from the public and the admin (ADR
     0008), the owner's; `SpaceCapacity`; `#### GET …/capacity · 🏢` (`null` before one is set) and
     `#### PUT …/capacity · 🏢` (body `{ capacity }`, 1–1,000 or `null`; the row on the first write; the
     same value writes nothing; audited `space.capacityEdited`; errors as the settings'). [C4]
4. **`docs/backend/conventions.md`** — header *Built*: "`platform-settings` and `space-settings`
   minimally (…)" becomes "`platform-settings` minimally (the new-space defaults and the staleness
   thresholds), `space-settings` (a space's settings row, created with it, and its owner's read and
   edit)" [C2], and "…, and `occupancy`'s capacity" [C4]; §6 audit list: "settings changes, for spaces
   and the platform" gains "a space's capacity" [C4]; §9 `space-settings`: "The modules that apply them
   read them: …" gains "visits and subscriptions (whether reception may type a price by hand)" [C2].
5. **`docs/backend/security.md`** — *Authorization*: "The managed photo and package writes, and the
   staff routes, ask `can()` first" → "…, the staff routes, and the settings [C2] and capacity [C4]
   routes, ask `can()` first".
6. **`docs/features/space-settings.md`** (new, the template of documentation §5, about 600 words) [C2;
   C3's decision line]: header (Active, Description, 2026-10-19; authority: the `space-settings`
   capability, a space's settings; endpoints owned by the contract's *Settings (managed)*, the entity by
   the data model; the API is built, no web screen); *What it does*; *Who uses it* (the owner through the
   API; the desk's modules will read it, steps 7–8; the finance step, the reminder); *Responsibility
   boundary* (owns `space_settings` and what an edit changes; leaves the lock to `spaces`, the defaults to
   `platform-settings`, capacity to `occupancy`, the charge to `visits`); *How it composes the platform*
   (links: the boundary, `requireCan`, the lock passed by the composition root, the audit, the new-space
   defaults); *Behaviour and flows* (the read; the edit; the creation's row); *Decisions › API decisions*
   (D1's bounds with reasons, the pair, D1b [C3], D2, D4 incl. not in `newSpaceDefaults`, D6, P1, P2, P4,
   DI-41 and "from then on" as links); *Code map*; *Open findings* (none); *History › API history*
   (`#PRNUM — a space's settings, read and edited by its owner on the API; reception's hand-typed prices
   switch`).
7. **`docs/features/occupancy.md`** (new, about 400 words) [C4]: the same template for the capacity only;
   *Responsibility boundary* names what it will own (present, the live status, the override — conventions
   §9, link) without claiming it; decisions: the bound, two routes (finding 94), P5, owner-only and
   private from the admin; *Open findings*: 94; *History*.
8. **`docs/README.md`** — two lines under *features/*: `- [space-settings.md](features/space-settings.md)
   — a space's settings, read and edited by its owner (API only).` [C2] and `-
   [occupancy.md](features/occupancy.md) — a space's state now; so far its private capacity, set by its
   owner (API only).` [C4]
9. **`docs/project/overview.md`** — *Built* gains `- [Space settings](../features/space-settings.md): on
   the API, a space's settings read and edited by its owner, reception's hand-typed prices off by
   default.` [C2] and `- [Occupancy](../features/occupancy.md): on the API, a space's private capacity,
   set by its owner.` [C4]; the *Spaces* line's "The owner/reception web screen and capacity remain
   planned" → "The owner/reception web screen remains planned" [C4]. **Likely conflict with worker A.**
10. **`docs/features/spaces.md`** — the header's "The owner/reception web screen and capacity remain
    planned" and *What it does*' "The owner/reception web screen and capacity remain planned" → drop
    "and capacity" (and "remain" → "remains"), linking [occupancy](occupancy.md) once in the
    *Responsibility boundary*'s *Leaves* line ("…a space's settings to `space-settings`, its capacity to
    [`occupancy`](occupancy.md)…"). [C4] **Likely conflict with worker A.**
11. **`docs/plans/v1-mvp.md`** — step 11: a line **"Built early:** the space's settings and its capacity,
    on the API (#PRNUM, [api-contract › Settings (managed)](../api/api-contract.md#settings-managed)),
    ahead of the front desk; screen 24 remains here.**"** [C2, capacity named at C4]; *Ordering notes*:
    "Until step 11, a space runs on the new-space defaults copied at its creation, and the platform on its
    seeded settings" → "A space runs on the new-space defaults copied at its creation until its owner
    edits its settings (on the API since #PRNUM; screen 24 in step 11); the platform runs on its seeded
    settings until step 11." [C2]; *Planned API surface › Managed spaces*: the *Built* sentence names the
    settings [C2] and capacity [C4] routes; the `GET / PATCH …/settings` row removed [C2]; the
    `…/:spaceId` row's "; capacity remains planned" removed [C4].
12. **`docs/architecture/findings/94-the-attendance-card-saves-two-capabilities-in-one-save.md`** (or the
    next free number) — §6's text; the index line under *Open*. [C4]

## Appendix B — Claude Code skills, only a map

| Step | Skill (if the executor is Claude Code) |
|---|---|
| §12.1, the branch | `start-work-item` (its git part) |
| Each test red first, each break | `superpowers:test-driven-development` (workflow §10) |
| Any failure | `superpowers:systematic-debugging` |
| §12.4 before any claim | `superpowers:verification-before-completion` |
| §12.7–12.8 | `open-pr`, then `final-report` |

No error code, so `add-error-code` is not used. OpenCode follows the same steps from this plan alone.
