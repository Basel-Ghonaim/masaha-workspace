# SETTINGS — independent review of PR #92 (Claude Code)

> **Head:** `af5a05a6aea5b0a5f4472d218db40c60ccb12591` (checked at the start and the end; unchanged) ·
> **Base:** `origin/main` `a8c39bda` (= the merge base) · `mergeStateStatus` **CLEAN** ·
> `gh pr checks 92`: every lane **pass** (build, check:classes, check:links, format:check, lint,
> test:api, test:component, test:unit, typecheck; CodeRabbit skipped).
> Read only commit objects in `C:\dev\masaha\app-design` (`git diff origin/main...af5a05a6`, `git show`).
> Nothing was run, checked out or installed.

## Verdict

**Ready to merge after a short documents-only fix round (or as is, with the nits recorded).** No blocker.
The server side is sound: owner-only on both routes at the route and again under the lock; validation
matches the database's `CHECK`s, so no partial patch can reach one as a 500; writes are minimal and audited.
What remains is document precision, one stale commit body and one workspace file the executor was not
allowed to write.

## The five most important findings

### 1. `OPEN_DECISIONS.md` point 1 was not updated: Q4 is not yet in the owner's queue — should-fix
- **Seen:** `C:\dev\masaha\workspace\_SHARED\OPEN_DECISIONS.md` lines 7–10 still hold the old open text
  ("…*Settle in: step 7 (visits) and step 8 (subscriptions).*"). The setting is not marked as stored by #92,
  and Q4 is not there at all (with the switch off and no rate, the visit closes **unpriced** and goes to the
  owner's «يحتاج انتباهك»).
- **Read only in the report:** the executor held back because the exec prompt allowed no write outside the
  repository; the replacement text is in `4_REPORT_PR1.md` › *`OPEN_DECISIONS.md` point 1*.
- **Scenario:** step 7's planner reads `OPEN_DECISIONS.md`, finds point 1 still open with no Q4, and decides
  the no-rate case again (or closes the visit free).
- **Fix:** paste the report's text into point 1. **Where:** outside the PR, before step 7 is planned (owner or
  orchestrator).

### 2. ADR 0009's table now contradicts itself on custom subscriptions — should-fix (documents)
- **Seen:** `docs/architecture/decisions/0009-space-scoped-reception-role.md`, rule 5's table (header
  `| Action | Reception | Owner |`): the existing row `New customer; subscription from a package or custom |
  ✓ | ✓` is unchanged, and the new row right below says reception types a custom subscription's price only
  "where the space allows it". The data model's new *Hand-typed prices* bullet says a custom subscription's
  price **is** a hand-typed price.
- **Scenario:** step 8's builder reads the first row as "reception may create a custom subscription" without
  a condition. With the switch off, either reception creates one (bypassing the gate), or the two rows are
  read as being in conflict.
- **Fix:** qualify the old row, for example `subscription from a package; custom (its price typed by hand:
  below)`, or fold "custom" into the new row. **Where:** a fix round on this PR (C1, which owns the ADR edit).

### 3. `security.md`'s *Built* header does not list the new `requireCan` routes — nit
- **Seen:** `docs/backend/security.md` line 3 (*Built*): "…and `requireCan` on its photo and package writes
  and its staff routes…" is unchanged. The body (*Authorization*) was updated: "…the staff routes, and the
  settings and capacity routes, ask `can()` first…".
- **Scenario:** the header, which is the document's summary of what is built, understates it.
- **Fix:** "…on its photo and package writes, its staff routes, and its settings and capacity routes".
  **Where:** fix round (C2/C4).

### 4. C4's commit body still says "finding 94" — nit
- **Seen:** `git show af5a05a6`, body: "…so the attendance card's single save is finding 94, for screen 24's
  plan." The finding is **96** (`docs/architecture/findings/96-…md`). The tree and the PR description are
  right, and `git grep "finding 94"` finds nothing.
- **Fix:** reword C4 if a fix round runs (the history is permanent once merged). **Where:** fix round.

### 5. The visit-rounding rule now has two homes — finding to record (step 11)
- **Seen:** `apps/api/src/modules/platform-settings/settingKeys.ts:14–24` (`newSpaceDefaultsSchema`:
  `z.enum(VisitRounding)`, `visitRoundingMinutes: z.int().min(1).max(59).nullable()`, a `.refine` pairing
  rule with an English `message`). This PR adds the same rule to `packages/shared/src/space-settings/requests.ts`
  (`VISIT_ROUNDINGS`, `ROUNDING_MINUTES`, `roundingPair` with field codes). The plan kept `newSpaceDefaults`
  unchanged on purpose (D4, step 11's ground), so this is not a departure.
- **Scenario:** step 11 builds the admin's defaults editor on the older, message-based schema. The two
  definitions drift: different codes on the same rule, or different bounds after a later change to one.
- **Fix:** step 11's plan makes `newSpaceDefaultsSchema` reuse `ROUNDING_MINUTES` and the pair rule from
  `@masaha/shared/space-settings`. Both are L0, so the level rule allows the import. **Where:** a finding to record now
  (or a line in step 11's plan).

## The rest

### 6. `DI-41` is cited in the data model but defined nowhere in the repository — nit
- **Seen:** `docs/architecture/data-model.md` *Visit charge*: "(DI-41, 2026-10-19, #92)"; the same in
  `space-settings.md`. `DI-41` is not in `docs/design/` (`CHANGES.md` defines DI-38 but not DI-41); it exists
  only in the workspace. The rule stands on its own sentence, so this is provenance, not meaning.
- **Fix:** drop the ID (keep the date and #92), or accept the label as the design log's. **Where:** fix
  round, or accept.

### 7. `v1-mvp.md` step 5 still names capacity among its supports, while "Built early" sits in step 11 — nit
- **Seen:** `docs/plans/v1-mvp.md:81` (step 5, *Supported by*): "…§9 occupancy (capacity)". Line 141 (step 11)
  says "**Built early:** the space's settings and its capacity, on the API (#92…)". The attendance card that
  shows capacity is on screen 24 (step 11; finding 96), so step 5's mention is the stale one. The line comes
  from `main`, but this PR makes it misleading.
- **Fix:** drop "and §9 occupancy (capacity)" from step 5, or say there that it was built in #92. **Where:** fix
  round (C4) or the next plan edit.

### 8. `conventions.md`'s *Built* header lists two documented capabilities as if they had no document — nit
- **Seen:** `docs/backend/conventions.md` line 3: "the modules `sessions`, `platform-settings` minimally (…),
  `space-settings` (…, and its owner's read and edit), and `occupancy`'s capacity, **beside the capabilities
  documented in `docs/features/`**". This PR gives both modules a feature document, so the list now
  overlaps the "beside" clause, and the detail ("its owner's read and edit") is a second home of
  `space-settings.md`'s scope.
- **Fix:** keep only the modules that have no feature document (`sessions`, `platform-settings`). The two new
  ones are then covered by the clause. **Where:** fix round, or accept.

### 9. The capacity "applies at once, to the stays already open too" — nit (wording)
- **Seen:** `data-model.md`, the new *A change … applies from then on* bullet. The capacity has no effect on an
  open stay; it acts on the next check-in's warning and on the live status. Q3 asked about the stay limit and
  the closing check-out. The sentence is true but groups capacity with them.
- **Fix:** "…the closing-time check-out and the stay limit apply at once, to the stays already open too; the
  capacity at the next check-in and in the live status." **Where:** fix round, or accept.

### On the departures and the breaks (judged)
- **B2 → `min 0`** (the owner's word): right. `.int().multipleOf(60)` makes `min(1)` and `min(60)`
  equivalent, so the planned break could never go red. U1's new `0 → out_of_range` case is the one value that
  only `min` refuses. Seen in `requests.unit.test.ts:18`.
- **B16 / T20 by raw SQL:** right, and stronger. Prisma sends the schema's `@default(false)` itself, so the
  planned T20 could not see the database's default, which is what existing rows took. Seen in
  `schema.api.test.ts` (the raw `INSERT` with only the four required columns and `updated_at`).
- **The amount refinement skips `''`:** right. Without it, Zod 4 would add `invalid_format` beside `too_short`
  on an empty or whitespace-only text (the paragraph trims). Seen in `reminderTemplate.ts`.
- **Finding 96, not 94:** right (#91 took 94 and 95). Seen in the index, the file and `occupancy.md`'s two links.
- **The `occupancy.md` link corrections:** seen. They resolve, and CI's `check:links` passed.
- **The other breaks went red:** I saw only the report's lines (`4_REPORT_PR1.md` §12.5), not the runs. By
  reading, each assertion would fail under its break. B22: T4 sends `visitCapAtDayPrice: true` unchanged, so
  a whole-request audit differs. B24: T7's empty patch would audit. B30: T15 seeds a full override. B31: T16's
  `PUT null` with no row would create one. B26 and B34 go red as 403, not 404: with the lock's answer ignored,
  `linksUnder` reads no links for a soft-deleted space. The test still catches the change, and nothing is
  written either way.

### Commits
Seen: four commits, subjects 44, 45, 47 and 39 characters (≤ 50). Each is atomic, with its tests and documents.
The bodies give the why, with no tool attribution and no `#PRNUM` left (`git grep` empty). The only wrong body
is C4's (finding 4).

### Against #91 and `main`
Seen: the PR is based on `a8c39bda` (main after #91). The findings index keeps 94 and 95 (#91's) and adds 96.
`overview.md` keeps #91's *Spaces* wording ("naming its owners") and drops "and capacity". `spaces.md` merged
clean. No text conflict remains (CLEAN).

## Checked and fine (seen in the code)
- **Authorization.** Both routers are mounted inside `manage`, behind `requireAuth` + `requireSpaceAccess`
  (`app.ts`). A stranger, an owner of another space, an unlinked admin, a deactivated link (`roleAt` ignores
  deactivated links; proven at the boundary by `spaces/manage.api.test.ts:140`) and a soft-deleted space all
  get 404. `requireCan('space.settings.manage' | 'space.capacity.manage')` (both `'owner'` in `can.ts`) runs
  before `validate` on every route, so reception gets 403 even with an invalid body (T3, T13). Both writes take
  the lock first (false → 404), then `can()` on `space.linksUnder(tx)`. No other route writes `space_settings`
  or `space_occupancy`: no `capacity` in any spaces schema; the spaces router uses explicit paths (`/hours`,
  `/prices`, …), with no `/:group` that could shadow `/capacity` or `/settings`.
- **Validation.** The stay limit is int, 60–1,380, a multiple of 60, or null. Capacity is int 1–1,000 or null,
  and required. The rounding minutes are 1–59, and `roundingPair` means a patch carries both fields or neither,
  consistent with each other. Every accepted pair satisfies `space_settings_visit_rounding_check` on its own,
  and `settingsChange` only drops a field equal to the stored one, so the stored row stays consistent and no
  `CHECK` can fire as a 500. Booleans are never null. Strings for numbers get `invalid_format`. The reminder
  goes through `paragraphSchema` (CRLF → LF, NFC, trim, bidi and control characters refused); placeholders
  are on the list, and the amount is required. `validate` replaces the body with the parsed, stripped value.
  An object refinement cannot crash on a non-object body: Zod aborts first, and `validate` answers 400.
- **Writes.** Under the lock, the current row is read inside the transaction, so two owners serialize and the
  second compares against the first's result. Only the changed fields are written and audited. A no-change
  edit returns before `update` and `audit`. The capacity upsert's `update` is `{ capacity }` only, and
  `create` leaves the override null. Equal values (`null` with no row included) write nothing.
- **Migration.** One `ADD COLUMN … BOOLEAN NOT NULL DEFAULT false`, nothing else. `schema.prisma` has
  `@default(false) @map("reception_may_type_prices")`, and the mapper and `SpaceSettings` agree.
  `createFor` is unchanged, so a new space gets the default. Not seen: the backfill on `masaha_b_dev`
  (the report's `13 | 0`).
- **Module boundaries.** `space-settings` (L0) imports only `db`, `shared/*` and `@masaha/shared/space-settings`.
  The lock arrives as `lockSpace`, passed by `app.ts` (P1), and `spaces` is now created before it.
  `occupancy` (L4) imports `spaces` (L1) through its index. `@masaha/shared/occupancy` imports only `zod`.
  The `exports` wildcard serves both new paths, and the level map already listed both modules.
- **Documents.** The contract's two sections match the code: routes, bodies, every code, `required` on a
  missing capacity, 403 before the body and for an owner unlinked meanwhile, 404 for a space deleted meanwhile,
  and the audit names. DI-41, *Hand-typed prices* and "from then on" each live once in the data model, and the
  feature documents link to them. ADR 0009's revision line and its table columns (Reception, then Owner) are
  right. `docs/README.md`, the overview's *Built*, `spaces.md` and the planned API surface (the settings row
  removed, "capacity remains planned" removed) are updated. No document claims the desk's use is built.
