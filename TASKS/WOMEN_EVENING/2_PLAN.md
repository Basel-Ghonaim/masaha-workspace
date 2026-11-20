# WOMEN_EVENING — the plan (2026-11-12)

Worker: a task worker in `C:\dev\masaha\app`, branch `feat/women-evening` from `main` `f58c12a8`, **local only**
(no push, no PR). Decisions binding: `0_OWNER_DECISIONS.md` E1–E9, W1–W6.

**Override, stated:** `start-work-item`/`write-plan` say "plan in plan mode, save, stop for approval". The owner's
prompt says plan briefly, save, and build at once (precedence 1, the owner's instruction). No plan mode; no stop.

## 1. Summary

One switch on the space, `worksEvenings`, part of the hours group (date, staleness, audit): «المساحة تعمل مساءً» in
«ساعات العمل»'s Sheet, «دوام مسائي» in the view and on the public page, a gentle hint when it is on and no open day
closes after 18:00. The directory's «مفتوحة مساءً» reads the switch only (decision 8's 20:00 rule goes). One catalogue
amenity, `womens_hall` («قاعة للنساء» / "Women's hall", icon `venus`), added by the migration; one fixed filter
«قاعة للنساء» in «أخرى», by the amenity's key; the admin may rename, re-icon and reorder it, never retire it
(`AMENITY_IN_FILTER`). The card's two marks wait for the identity merge; their API fields are built now.

## 2. Contract

**Scope / acceptance**
- [ ] `spaces.works_evenings` (default false); E8's switch-on and W3's amenity row in the same migration.
- [ ] `PUT …/hours` takes `worksEvenings` (required); a save of the switch alone writes it, dates and audits the group,
      the week and shifts untouched; an unchanged save writes nothing.
- [ ] `AdminSpace.hours` and `PublicSpace.hours` carry `worksEvenings`.
- [ ] `evening=true` passes by the switch only; `womensHall=true` passes a space linked to the active `womens_hall`.
- [ ] `DirectorySpace` carries `worksEvenings` and `womensHall` (the card's future marks; the favourites' cards too).
- [ ] The admin's `PATCH /admin/amenities/:id` refuses `isActive: false` on `womens_hall` (409 `AMENITY_IN_FILTER`);
      rename, icon and order stay open.
- [ ] Web: the Sheet's box, the view's line, the hint (view and Sheet), the admin's editor the same (one component);
      the public page's «دوام مسائي»; the panel's «قاعة للنساء», address `women=1`, counted and cleared.
- [ ] The icon `venus` in the shared keys, the design system's set and `GlyphIcon`; its names in both catalogues.
- [ ] Documents: directory, spaces, lookups, api-contract, data-model, glossary, overview.

**Out of scope:** the card's marks (identity's `SpaceCard.tsx`), any `foundation.md` line, evening prices or a section
(E4/E5), past midnight (E3), «مختلطة» (W6), a general amenities filter (R2), the map's pin fields.

## 3. Reading done

CLAUDE.md; workflow, engineering-principles, testing; the decisions; directory.md, spaces.md, lookups.md, packages.md;
api-contract (directory, lookups' amenities, spaces' hours, §6); data-model; backend conventions §4, §8, §9;
frontend architecture (skimmed by need); the Prisma schema and migrations; the findings index (identity takes 220–221;
mine would start at 222, but the index is identity's file — see §11).

## 4. The settled decisions as built

- **E4/E6** the switch on `spaces` (`works_evenings`), inside the hours group: `SpaceHours = { days, shifts,
  worksEvenings }`; the request `{ days, shifts, worksEvenings }`. The shifts' Sheet sends the switch as last read.
- **E7** `evening=true` → `s.works_evenings`. `EVENING_FROM_MINUTE` goes. A space without hours can hold no `true`
  (only an hours save sets it), so it still never passes.
- **E8** `UPDATE spaces SET works_evenings = true WHERE EXISTS (open day, closes_minute >= 1200)`.
- **E9** hint: switch on and every open day closes at or before 18:00 (1080) → in the view and live in the Sheet.
- **W3** `INSERT INTO amenities (key, name_ar, name_en, icon, sort_order, is_active, updated_at) SELECT 'womens_hall',
  'قاعة للنساء', 'Women''s hall', 'venus', COALESCE(MAX(sort_order),0)+1, true, now() FROM amenities HAVING
  count(*) > 0 ON CONFLICT (key) DO NOTHING`; the seed's list gains it ninth (fresh environments).
- **W5** the panel's «أخرى»: «المساحات الموثّقة فقط», «أسعار للطلاب», «قاعة للنساء».
- **W6** nothing is said of a space without it.

## 5. The migration's SQL (in full; the file is read after `--create-only`)

```sql
-- AlterTable: the owner declares the space works in the evening (WOMEN_EVENING E4, 2026-11-12).
ALTER TABLE "spaces" ADD COLUMN IF NOT EXISTS "works_evenings" BOOLEAN NOT NULL DEFAULT false;

-- E8, once: every space whose week already closes at 20:00 or later on an open day keeps «مفتوحة مساءً».
UPDATE "spaces" SET "works_evenings" = true
WHERE EXISTS (
  SELECT 1 FROM "space_hours" h
  WHERE h."space_id" = "spaces"."id" AND NOT h."is_closed" AND h."closes_minute" >= 1200);

-- W3: the women's hall, last in the catalogue, by its fixed key; a catalogue not yet seeded gets it from the
-- seed, and a key already taken is left as it is.
INSERT INTO "amenities" ("key", "name_ar", "name_en", "icon", "sort_order", "is_active", "updated_at")
SELECT 'womens_hall', 'قاعة للنساء', 'Women''s hall', 'venus', COALESCE(MAX("sort_order"), 0) + 1, true,
  CURRENT_TIMESTAMP
FROM "amenities" HAVING count(*) > 0
ON CONFLICT ("key") DO NOTHING;
```

`IF NOT EXISTS` lets the API test run the file as written against fixtures (T1–T3).

## 6. API

- `PUT /admin/spaces/:spaceId/hours`, `PUT /manage/spaces/:spaceId/hours`: body `{ days, shifts, worksEvenings }`,
  `worksEvenings` boolean, required (`required` / `invalid_type` as zod's codes map). Audit `space.hoursEdited`
  `before`/`after` gain `worksEvenings`. Unchanged = days, shifts and switch equal.
- `GET /spaces`, `GET /map/spaces`: `evening=true` the switch; `womensHall=true` new (same boolean rule).
- `DirectorySpace`: `worksEvenings: boolean`, `womensHall: boolean`.
- `PATCH /admin/amenities/:id`: `conflict` (409) `AMENITY_IN_FILTER` for `isActive: false` on `womens_hall`.
- Composition: `directory` asks `lookups.activeAmenityIdOf(WOMENS_HALL_KEY)` (one query) for every list and pins
  read, passes the id to `spaces`' filter (`womensHall: { amenityId, only }`); `spaces` reads `space_amenities`.

## 7. `packages/shared`

`spaces`: `SpaceHours.worksEvenings`, the schema's field. `lookups`: `'venus'` in `AMENITY_ICON_KEYS`,
`WOMENS_HALL_KEY`. `directory`: `womensHall` filter, the card's fields, the `evening` comment. `core`: the code.

## 8. Web

- `spaces`: `services/hoursSheet.ts` (`worksEvenings` in the values; `eveningEndsEarly(days, on)`, the hint's one
  rule), `hooks/hours/useHoursSheet.ts`, `components/hours/HoursSheet.tsx` (a `Checkbox` Field under the hours, its
  help, the hint as a `warning-subtle` note while it holds), `hooks/hours/useHoursSection.ts` + `HoursView.tsx` (the
  line with `MoonIcon`, the hint), `hooks/shifts/useShiftsSheet.ts` + `services/shiftsForm.ts` (the switch as read).
- `directory`: `types/DirectoryFilters.ts`, `types/DirectoryRequest.ts`, `services/filtersOf.ts`,
  `services/requestOf.ts`, `hooks/list/useDirectoryFilters.ts` (count, clear), `hooks/filters/useFiltersPanel.ts`,
  `hooks/page/useSpacePage.ts`, `types/SpacePageView.ts`, `components/page/HoursSection.tsx` (the line).
- `lookups`: nothing but copy (the grid draws the ninth icon from the keys).
- Design system: `icons/iconSet.tsx` (`VenusIcon`), `icons/GlyphIcon.tsx` (`venus`).
- Copy: `spaces`, `directory`, `lookups` (icon name), `errors` — both catalogues.

**Identity check:** none of these is in `git diff --name-only origin/main...feat/ink-berry-identity` today (checked;
re-checked before each commit).

## 9. Documents

`directory.md` (behaviour, decision 8 marked revised by E7, new decisions, history), `spaces.md` (hours, decisions,
history), `lookups.md` («No amenity is a filter» revised, the admin rule, the ninth icon), `api-contract.md`,
`data-model.md` (Open in the evening, Amenity), `glossary.md` (two terms), `overview.md` (scope line and Built line).
**No ADR:** a column and a filter on the existing patterns, reversible, one capability each — under the threshold.

## 10. Test matrix

| # | Behaviour | Break that fails it | Lane / file |
|---|---|---|---|
| T1 | The migration switches on a space closing ≥ 20:00 on an open day, not one closing 19:30, not a closed day's 22:00, not a space without hours | `>= 1200` → `> 1200`; drop `NOT is_closed` | API `db/womenEveningMigration.api.test.ts` |
| T2 | It adds `womens_hall` once, both names, `venus`, last; a second run adds nothing | drop `ON CONFLICT`; `MAX+1` → `1` | same |
| T3 | An empty catalogue gets no row from it | drop `HAVING count(*) > 0` | same |
| T4 | Schema: `worksEvenings` required, boolean | make it `.optional()` | unit `shared/spaces/requests.unit.test.ts` |
| T5 | Hours save of the switch alone: written, dated, audited, days and shifts kept | leave the switch out of the unchanged check / the write | API `spaces/hours/hours.api.test.ts` |
| T6 | Saving the same week with the switch unchanged writes nothing | — (existing, extended to carry the switch) | same |
| T7 | Reads carry it: admin read, public page | drop it from the reader | API hours + `directory/page.api.test.ts` |
| T8 | `evening=true` passes by the switch only (a 23:00 space with it off fails; an 18:00 space with it on passes); with `openNow`, `verified`, `womensHall` | restore the 20:00 rule | API `directory/hours.api.test.ts` |
| T9 | `womensHall=true` passes a linked space only; by the key (the amenity's id is not 1); a retired one passes none; combined with `evening`, `area`, `verified`; the map too | filter by a hard id; drop the active check | API `directory/filters.api.test.ts` |
| T10 | The card carries `worksEvenings`, `womensHall` | drop either | API `directory/list.api.test.ts` |
| T11 | Retiring `womens_hall` is 409 `AMENITY_IN_FILTER`, nothing written; rename, icon, reorder pass; another amenity retires | remove the refusal | API `lookups/amenities/amenities.api.test.ts` |
| T12 | `eveningEndsEarly`: on + all ≤ 18:00 → true; one 18:30 → false; off → false; closed days ignored | `<=` → `<` | unit `spaces/services/hoursSheet.unit.test.ts` |
| T13 | The Sheet's box: opens on the saved value, sends it, the switch alone is a change; the hint while ticked and early; axe; ar and en | send `false` always | component `HoursSheet.component.test.tsx` |
| T14 | The view's line «دوام مسائي» and the hint; none when off; ar and en; axe | drop the line | component `spaces/.../HoursView` (new `HoursSection.component.test.tsx`) |
| T15 | The shifts' Sheet sends the switch as read | send `false` | component `ShiftsSheet` test (existing file if any, else the hours one) |
| T16 | The address: `women=1` ↔ `womensHall`, round trip; request `womensHall: true` | drop the key | unit `filtersOf.unit.test.ts`, `requestOf.unit.test.ts` |
| T17 | The panel shows «قاعة للنساء» in «أخرى», applies it, counts it, clears it | leave it out of the count | component `useFiltersPanel` / directory list test |
| T18 | The public page's «دوام مسائي» | drop it | component `SpaceDetails.component.test.tsx` |
| T19 | `GlyphIcon` draws `venus` | — | component `GlyphIcon.component.test.tsx` (row added) |
| T20 | Seed: nine amenities, `womens_hall` last | — | API `seed.api.test.ts` (count updated) |

Every new test is seen failing first (the break made, then restored from a `cp` backup).

**Review Focus:** a `womens_hall` added by hand before the migration and retired (kept retired; the filter passes
none until restored); two spaces' order of the amenities after the seed on a fresh database; the hint at exactly
18:00; `worksEvenings: true` with hours never saved (unreachable through the API).

## 11. Commits

1. `feat(db): add the evening switch and women's hall` — schema, migration, seed's ninth, T1–T3, T20.
2. `feat(spaces): the evening switch in the hours group` — shared schema/types, hours service/repository/reads,
   contract (hours), spaces.md (API), data-model, T4–T7.
3. `feat(directory): filter the evening and women's hall` — shared filters/card, lookups' id by key, listing, service,
   the admin rule + `AMENITY_IN_FILTER`, contract, directory.md/lookups.md (API), T8–T11.
4. `feat(spaces): the evening box, line and hint` — the profile web, copy, spaces.md (web), glossary, T12–T15.
5. `feat(directory): the women's hall filter and the evening` — panel, address, page line, icon, copy, directory.md and
   lookups.md (web), overview, T16–T19.

Lint and typecheck on each; `#PRNUM` where a PR number belongs. Findings: none planned; one found would be written as
a new file `222-…` without its index row (identity's file), listed as waiting.

## 12. Verification

Through `heavy.mjs we …`: lint, typecheck (each commit), format:check, check:classes, check:links, check:conflicts,
build (NODE_ENV=production) + check:build, test:unit, test:component, test:api, one at a time. Real run on 3320/5320
against `masaha_we_dev`; screenshots to `Downloads\women-evening-shots\`.

## 13. Decisions taken without the owner

| # | Decision | Options | Chosen, why |
|---|---|---|---|
| X1 | The switch's name | `evening`, `opensEvenings`, `worksEvenings` | `worksEvenings` / `works_evenings`: the owner's words («تعمل مساءً»); `evening` stays the filter's name |
| X2 | Where it travels | a field of the space; inside `SpaceHours` | inside `SpaceHours` and the hours request: it is the hours group's (E6), one date, one save path |
| X3 | Required in the body | optional default false; required | required: the group is saved whole, so a client that leaves it out would clear it unseen (spaces S1's precedent) |
| X4 | The hint's rule | none closes after 18:00; none at or after 20:00 | E9's words: no open day closes after 18:00 (an 18:00 close hints) |
| X5 | The hint's place | the view only; view and Sheet | both, one pure rule: the Sheet is where the owner decides, the view where it is read again |
| X6 | The hint's wording | the owner's sketch «… ساعات عملك …» | «شغّلت الدوام المسائي، لكن ساعات العمل تنتهي مبكرًا: لا يُغلق أي يوم بعد 18:00.» / "Evening hours are on, but the opening hours end early: no day closes after 18:00." — neutral «ساعات العمل» since the admin's editor shows it too |
| X7 | The icon | `venus` ♀, `door-closed`, `user-round`, `armchair` | `venus`: the common sign of a women's place, distinct from `users` (meeting room); installed in lucide-react 1.48 |
| X8 | The admin's rule | allow all; refuse retire; hide the switch | refuse retiring on the server, 409 `AMENITY_IN_FILTER`, its text in the row; rename, icon, order allowed; delete does not exist (lookups never deletes). A retired one would leave the filter passing spaces whose page does not show it |
| X9 | The amenity row on a fresh database | always insert; only into a seeded catalogue + the seed's ninth | only when the catalogue has rows; the seed adds it ninth: otherwise the fresh seed's 1–8 would tie it with «إنترنت» at 1 |
| X10 | The filter's names | API `womensHall`, address `women`; `amenity=womens_hall` | `womensHall` / `women=1`: one fixed filter (R2 stands), named like `openFriday`/`friday`; the server resolves it by the key |
| X11 | The pin | add the fields to `MapPin`; not | not: E6/W4 name the directory's card; the map's chosen card is another component, unchanged |
| X12 | The marks' fields on favourites | — | they are `DirectorySpace`, so the favourites' cards carry them too, for free |
| X13 | No ADR | ADR; none | none: below the threshold (one column, one filter, existing patterns) |
| X14 | No plan mode, no stop | — | the owner's instruction (§1 override) |

## 14. Waiting for the identity merge

- **The card's two marks** (`features/directory/components/card/SpaceCard.tsx`): exact design in the report.
- `foundation.md`: no line needed today (it names `GlyphIcon`'s closed set without listing it) — re-read at merge.
- The findings index row, should a finding be written.

## 15. Decisions needed from the owner

None blocking; X1–X14 for review. The Arabic of `AMENITY_IN_FILTER` and the hint need the owner's approval.
