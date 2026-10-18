# AMENITIES — report

## 1. The pull request

- **PR:** [#64](https://github.com/Basel-Ghonaim/masaha/pull/64) `feat(spaces): own amenities, no amenity filter`.
- **Labels:** `feat`, `area:api`, `area:web`, `area:docs`; assigned to the owner.
- **Head:** `b7397dc`. CI passed on that head (all ten checks, run on `b7397dc`), and GitHub shows `CLEAN`.
- **Branch:** `feat/space-own-amenities`, cut from `origin/main` at `068efc6` (see §8). Not merged.

## 2. The commits

1. `eac5157 feat(lookups): drop the amenity filter`
   - migration `20261012122739_no_amenity_filter` and the schema;
   - `@masaha/shared/lookups`, the lookups API (amenities, catalogue) and the seed;
   - the web's amenities tab, with its switch, badge, hook, copy and card line, and the unused `switches` slot (S3);
   - the Combobox comment;
   - D1's documents: `lookups.md` (#16's decision superseded), the contract's lookups sections, the data model's Amenity, the overview's *Directory*, the plan's `GET /spaces`, `foundation.md` and `README.md`.
2. `b5b2991 feat(spaces): keep a space's own amenities`
   - migration `20261012123800_space_own_amenities` and `SpaceOwnAmenity`;
   - `@masaha/shared/spaces`, the new `ownAmenities.repository.ts`, the service, the facts reader and the mapper;
   - the tests;
   - D2's documents: the contract (with the audit-shape note), the data model, `spaces.md`, `lookups.md`'s boundary, conventions §7, the glossary (*Amenity*, *own amenity* «مرفق إضافي») and the overview's *Built*.
3. `b7397dc chore(users): name both locks in changeRole` — a comment only (#62's leftover). The PR says so and carries `Closes #63`.

## 3. What was run

**Locally, once each and one at a time.** The lanes ran on `fd2414e`, which differs from `b7397dc` only by one comment (`lookups/responses.ts`) and one sentence (`spaces.md`), folded in after self-review.

| Check | Result |
|---|---|
| `test:unit` | shared 162, web 660, API 724, all passed |
| `test:component` | 785 passed (123 files) |
| `test:api` | 667 passed (40 files) |
| `NODE_ENV=production npm run build` and `check:build` | clean: no showcase, no dashboard code and no heavy library in the first download |
| `lint`, `typecheck` | 0 errors on the head, and on commits 1 and 2 separately (each with its own Prisma client and shared `dist`) |
| `check:classes`, `format:check`, `check:links` | clean (1925 links) |

**Migrations:**
- both migrations were applied to `masaha_amenities_dev`, and the API lane applies them to `masaha_amenities_test`;
- on a scratch database `masaha_amenities_scratch` (`createdb`, then `migrate deploy`), all 14 migrations ran clean from empty;
- `prisma migrate diff --exit-code` against the schema came back empty, `is_filterable` was absent and `space_own_amenities` present;
- the scratch database was then dropped.

**Real requests on 3322:**

| Request | Result |
|---|---|
| `GET /lookups` | 200; the amenities are `{ id, key, nameAr, nameEn, icon }`, and no item has `isFilterable` |
| `POST /admin/amenities` `{ nameAr: 'طابعة ليزر', nameEn: 'Laser printer', icon: 'presentation', isFilterable: false }` | 201 `{ id: 9, key: 'laser_printer', …, isActive: true }`: the old flag is not taken |
| `PATCH /admin/amenities/9` `{ nameEn: 'Printer', icon: 'zap', isFilterable: true }` | 200, without the flag; audit `amenity.edited` before `{ icon, nameEn }`, after `{ icon: 'zap', nameEn: 'Printer' }` |
| `POST /admin/spaces` (space 2) | 201, with `missingGroups` `['hours','prices','amenities','contacts']` |
| `PUT /admin/spaces/2/amenities` `{ amenityIds: [1, 9], ownAmenities: [{ مصلى, Prayer room }, { خزائن }] }` | 200; `amenityIds: [1, 9]`; `ownAmenities` `[{ مصلى, Prayer room }, { خزائن, null }]`; dated `13:18:41.129Z` |
| `GET /admin/spaces/2` | the same, in order |
| `POST /admin/spaces/2/amenities/confirm` | 200, dated `13:18:41.294Z`, own amenities unchanged |
| `PUT` the same group again (ids in another order, `nameEn: null`) | 200; the date stays the confirm's `13:18:41.294Z`, so nothing was written |
| `PUT` with `[{ مصلى }, { مصلى, Prayer }]` | 422, `errors: { "ownAmenities.1.nameAr": ["not_unique"] }` |
| `PUT` with `{ amenityIds: [] }` alone | 422, `errors: { "ownAmenities": ["required"] }` |

The audit log for space 2 holds `space.created`, then `space.amenitiesEdited` (after `{ amenityIds: [1, 9], ownAmenities: [...] }`), then `space.amenitiesConfirmed`. The unchanged save wrote nothing.

**The web on 5322.** Screenshots of the amenities tab and its edit sheet are in `C:\Users\basel\Downloads\amenities-shots\`, not committed:
- `amenities-ar-light-390`, `amenities-ar-dark-390`, `amenities-en-dark-390`;
- `amenities-ar-light-1440`, `amenities-en-light-1440`, `amenities-en-dark-1440`;
- `edit-sheet-ar-light-390`, `edit-sheet-en-dark-1440`.

They show no «In filters» switch, no badge and no line under the card's title; the sheet holds the names, the icon and Active, with the new hint.

**Afterwards:** both servers were stopped by PID (the `tsx watch` and its server, and Vite with esbuild), then checked: ports 3322 and 5322 are free, no node process of this worktree is left, and no headless Chrome is left. The background shells have ended.

**Not run:** E2E, which is for the end of the project.

## 4. The breaks made, and the tests seen failing first

**Seen failing first:**
- **The shared lookups tests:** 3 failed (the flag still parsed or required).
- **The lookups API:** 8 failed (POSTs without the flag got 422; the answers held the flag).
- **The web's lookups tests:** 10 failed: the row, the badge, the switches, the sheet, the forms and the section's description.
- **The shared spaces tests:** 5 failed.
- **The spaces API:** every amenities test failed, and the refused-caller table did too (`spaceOwnAmenity` absent).

**Two tests could not be seen failing:**
- `useEditAmenityForm`'s save-body test passed before the code changed. Its fixture had already lost the flag, so the body never carried it. The typecheck holds that case (`AdminAmenity` no longer has the field).
- `lookupChange.unit.test` changed its sample fields only, and still passes. It is generic over the fields.

**Breaks (rule 7), each made once, seen failing, and restored:**
- the no-op compared the own amenities as a set (sorted by name): "writes nothing when saved again unchanged, but a new order… is a change" failed;
- `ownAmenities.listFor` ordered by `nameAr` instead of `sortOrder`: 3 tests failed (the save in order, the read back, the reorder).

## 5. Problems met, and how each was solved

- **`prisma migrate dev --create-only` refused to create the drop-column migration in a non-interactive shell.** Its data-loss warning ("8 non-null values") needs a prompt. I generated the SQL with `prisma migrate diff --from-config-datasource --to-schema` against the dev database, which was up to date and to which nothing was applied. I wrote it by hand into `20261012122739_no_amenity_filter/migration.sql`, with Prisma's warning comment, then ran `ls`. The second migration was made with `--create-only` once, then listed.
- **`prisma format` realigned the `Amenity` model,** which belongs to commit 1. I staged that hunk alone with `git apply --cached` as a fixup of commit 1, and squashed it in.
- **A heredoc holding a Python edit script failed to parse.** I wrote the scripts to the scratchpad with the Write tool instead, as my notes advise.
- **The Edit tool turned the test's `'\u202E'` escape into a literal RLO character.** I found it with `cat -A` and put the escape back with Python before the test ran.
- **The self-review found two sentences to correct.** Both were folded into their commits before the push:
  - S4's reason in `spaces.md` said "the editor shows both lists", but no editor exists and the merged design doesn't show own amenities; it is reworded;
  - the catalogue's comment had been changed to "place filter" needlessly, and is restored to "the directory's filters".

## 6. Anything that behaved unexpectedly

- **Locally, `test:component` took over 10 minutes,** past the 600 s tool limit, so it finished in the background. It passed, and in CI the same lane took 2m42s.
- **The plan's first rule-7 break could not catch what it claimed.** It was "`ownAmenities.replace` run outside `tx`, seen failing on the 403 test", but the 403 refuses before the step runs, and no failure can happen after the write. A write outside the transaction is caught by no test, as with the contacts. It is a *Review Focus* item: the reviewer checks that every write in `ownAmenities.repository.ts` takes `tx`, whose `replace` signature has no default.
- **The lookups page's shared hint** ("Hidden: not shown in filters and forms…") still shows above the amenities tab. It stays true, because it speaks of hidden governorates and areas, which the area filter leaves out, and a retired amenity is in no filter. I left it unchanged; the analyst may want it worded per tab.
- **Rows from the real run are left in `masaha_amenities_dev`:** the amenity "Laser printer" (id 9, key `laser_printer`, now named "Printer") and the space "Amenities Check Hub" (id 2) with its amenities. They are in this worktree's dev database only.
- **The design archive still draws an amenity filter:** the directory prototype and the admin lookups prototype. It is left for the analyst to route to the design batches, as the reply asks.

## 7. The early conflict check

`gh pr list --state open` lists only #64:
- #61 merged (`068efc6`) and #62 merged (`4ce6310`) before the branch was cut;
- no PR of worker A's is open.

There was no other head to run `git merge-tree --write-tree` against. Against `main`, GitHub shows `CLEAN`.

## 8. Departures from the prompt and the plan

- **The base:** the reply named `main` at `4ce6310`, but `git fetch` showed `068efc6`, because #61 (design documents only) had merged since. Following workflow §3 (cut from the latest `main`), the branch was cut from `068efc6`. #61 changes no code, schema or dependency.
- **The first migration was written by hand** from `prisma migrate diff` (§5), not by `--create-only`.
- **The rule-7 break on the transaction** was replaced by the two breaks above (§4, §6).
- **Two fixups were folded before the first push:** the `Amenity` alignment, and the two self-review sentences. No fix commits remain.
- **The PR number #64** was cited in the documents before the PR was opened (the next free number), and was confirmed when it opened.

---

# Round 2 — the owner's addition: no free price

The independent review (OpenCode, on `b7397dc`) found no problem. The addition (`AMENITIES_ADDITION.md`) is built in a fourth commit of its own.

## 1. The pull request

- **PR:** [#64](https://github.com/Basel-Ghonaim/masaha/pull/64).
- **Head:** `ec2139d`. CI passed on that head (all ten checks, run `38263123353`), and GitHub shows `CLEAN`.
- **The description** names the addition: a paragraph in *Summary*, an acceptance criterion and its own *Evidence*.
- Pushed with a plain push (a new commit, no force). Not merged.

## 2. The commit

`ec2139d feat(spaces): refuse a price of zero`
- `packages/shared/src/spaces/requests.ts`: `amountAgorot` now runs from `min(1)` to `PRICE_MAX_AGOROT`, and the price's comment says that no price is free and that a free event is an announcement.
- The shared unit test and the API prices test.
- `api-contract.md`: the prices body line now reads "an integer from 1 to 10,000,000 (`out_of_range` otherwise: no price is free)".
- `spaces.md`: the *API decisions* line "Every price is above zero; a free event goes in the announcements", the owner's decision, 2026-10-12, #64. The API history line for #64 adds "no price of zero".

## 3. What was run

Run on `ec2139d`, once each, after rebuilding the shared `dist`:

| Check | Result |
|---|---|
| `test:unit` | shared 162, web 660, API 724, all passed |
| `test:api` | 668 passed (40 files): one more than round 1, the new test |
| `lint`, `typecheck` | 0 errors |
| `format:check`, `check:links` | clean (1925 links) |

**Not rerun:**
- `test:component` and the build: the commit changes no web code (the web has no price form yet, and imports no price rule), so neither can change. CI ran both on the head: `test:component` passed (4m40s) and `build` passed.
- No real requests: the API test sends the request end to end on the real database.

**Fixtures:** `grep` over the seed (`demo.ts`: 400–35,000), every API test and the shared tests found no price of 0. The only 0 was the shared test's own case, which said 0 was accepted, and it is now the refusal.

## 4. Tests seen failing first

- Shared, "wants whole agorot from 1 to 10,000,000: no price is free" failed: 0 was accepted.
- API, "refuses a price of zero on its amount, writing nothing" failed with `expected 200 to be 422`.

Both pass with the rule. No other break was needed: the rule is a bound in the shared schema, and the two tests are its own.

## 5. Problems met

None.

## 6. Anything that behaved unexpectedly

- **The database still accepts a price of 0.** `space_prices_amount_check` (the init migration) reads `amount_agorot >= 0`, so only the shared rule refuses 0. The addition named the rule's home as `requests.ts`, and a schema change is the owner's, so I made none.
  - Today every write goes through the shared schema, so the database is not reached with 0 through the API.
  - Raising the check to `> 0`, as the payments' check already is, would take one migration with no data risk: no price of 0 exists in the seed. It is offered for the owner to decide, not done.
- **The data model** says only "location and amounts in range" for the checks, which stays true.

## 7. The early conflict check

`gh pr list --state open` lists only #64, and `main` is still `068efc6`. There was no other head for `git merge-tree`.

## 8. Departures from the addition

- **The refusal's code is `out_of_range`, not `too_small`.** The addition said `too_small`, "the shared vocabulary", but the contract's field-error codes (§3) have no `too_small`. `toFieldErrors` maps Zod's `too_small` on a number to `out_of_range`, the code a negative price and one above the cap already answer. The tests, the contract and the PR say `out_of_range`.

---

# Round 3 — the database refuses a price of zero too

Built from `AMENITIES_ADDITION2.md`, the owner's decision on round 2's second point. The fourth commit was approved as built, with `out_of_range`.

## 1. The pull request

- **PR:** [#64](https://github.com/Basel-Ghonaim/masaha/pull/64).
- **Head:** `2e4aa4d`. CI passed on that head (all ten checks, run `38267613191`), and GitHub shows `CLEAN`.
- **The description** names the fifth commit beside the fourth: in *Summary*, in an acceptance criterion and in its own *Evidence*.
- Pushed with a plain push. Not merged.

## 2. The commit

`2e4aa4d feat(db): refuse a zero price in the database`
- **The migration:** `apps/api/prisma/migrations/20261012144622_space_price_above_zero/migration.sql`, written by hand, since Prisma does not model check constraints. It has one comment line, `-- No price is free: a free event is an announcement (docs/features/spaces.md › Decisions).`, then drops `space_prices_amount_check` and adds it again as `CHECK ("amount_agorot" > 0)`. No other table changes.
- **The test:** in `apps/api/src/db/schema.api.test.ts` › *a price*, "is never negative" became `it.each([0, -1])` "is above zero: %i is refused, past the API". It is a raw `prisma.spacePrice.create`, which must throw `space_prices_amount_check` and leave no row. A new case, "takes the smallest price, one agora", accepts 1.
- **The document:** `data-model.md` › *Conventions* › *Prices* now reads "Amounts are integers in agorot, above zero (a free event is an announcement), with a `currency` (`ILS`)". The contract already says 1 to 10,000,000.

## 3. What was run

On `2e4aa4d`, once each:

| Check | Result |
|---|---|
| `test:api` | 670 passed (40 files): round 2 plus the new 0 and one-agora cases |
| `lint`, `typecheck` | 0 errors |
| `format:check`, `check:links` | clean (1926 links) |

**The migration:**
- **Dev:** `migrate deploy` on `masaha_amenities_dev` applied it, and `migrate status` says "Database schema is up to date!". It went through because no price of 0 exists there.
- **Test:** the API lane applied it to `masaha_amenities_test`.
- **Scratch:** on `masaha_amenities_scratch`, `createdb` then `migrate deploy` applied all 15 migrations clean, and `pg_get_constraintdef` reads `CHECK ((amount_agorot > 0))`. `migrate diff --from-config-datasource --to-schema --exit-code` returned 0 (no drift); the database was then dropped.

**Not rerun:**
- The unit and component lanes and the build: the commit holds only the migration, a test of the API lane and a document line, with no code in `packages/`, `apps/web` or `apps/api/src` outside the test. CI ran all three on the head, and they passed.

## 4. Tests seen failing first

Against the old constraint (`>= 0`), "is above zero: 0 is refused, past the API" failed: the insert succeeded. The cases -1 and 1 passed before and after, as they should. With the migration applied, all pass.

## 5. Problems met

- **The addition's drift check, `prisma migrate diff --from-migrations prisma/migrations --to-schema`, cannot run here.** Prisma 7 needs `datasource.shadowDatabaseUrl` in `prisma.config.ts` to diff a migrations folder, and this project sets none. Its equivalent ran instead: the scratch database built from every migration, diffed against the schema, shows no drift. I added no shadow database to the config, since that is outside this item.
- **The machine twice failed to resolve `github.com`** (a fetch after the push, and a fetch of #66). The push had landed ("Everything up-to-date"; `gh` shows the head `2e4aa4d`), and the fetch of #66 went through on retry.

## 6. Anything that behaved unexpectedly

`test:api` took over 10 minutes locally, past the tool's limit, so it finished in the background. In round 2 the same lane ran in the foreground, and in CI it takes about 4 minutes. It passed.

## 7. The early conflict check

Two PRs have opened since round 2, both from the design fixer.

| PR | Head | `git merge-tree --write-tree` with `2e4aa4d` |
|---|---|---|
| #65 `design/public` | `51685d0` | clean; it touches `docs/design/` only |
| #66 `design/admin-rest` | `15039cb` | clean; it touches `docs/design/` only |

`main` is still `068efc6`.

## 8. Departures from the addition

The drift check ran on the scratch database, not with `--from-migrations` (§5). Otherwise none.
