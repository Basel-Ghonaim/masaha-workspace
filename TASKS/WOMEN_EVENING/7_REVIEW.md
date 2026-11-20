# Review of #145 (WOMEN_EVENING) — Claude Code, Opus 5.5
Head: 8f511d5a18f26e5cd3fc79828a0d878892b8fb4a · commits 6 · files 115 (+1286 −180) · checks: green (10 pass, CodeRabbit skipped), `CLEAN` · head moved: no (re-read at the end: same sha, `CLEAN`)
Verdict: **mergeable after a fix round** — F1 (blocker under the owner's rubric, inert at runtime) and F3–F5 are small test and migration-file fixes; F2 needs a finding and a line in the PR, no code.

## Findings (verified defects only, most severe first)

### F1 — blocker · The migration's `IF NOT EXISTS` exists only for its test
- **Where:** `apps/api/prisma/migrations/20261112121413_women_evening/migration.sql:2–3`; its user,
  `apps/api/src/db/womenEveningMigration.api.test.ts` (`STATEMENTS`, `runMigration`).
- **Seen in the code:** the file's own comment: "`IF NOT EXISTS` lets the API lane run this file as written against its
  fixtures". In every real environment the column cannot exist before this migration, so the clause does nothing. It
  takes effect only when the API lane runs the file again on a database that `migrate deploy` has already migrated,
  and twice in the hall test. This is testing §3 rule 2 ("No production code exists only to serve a test"). Rule 4
  does not save it: production gains nothing. If anything it loses a little: a hand-made `works_evenings` of another
  shape (nullable, no default) would be kept silently, and the Prisma client would then disagree with the column. The
  plan and the PR say this openly, but the plan was built without a stop. The clause is not on the review's
  *Known and accepted* list, and no project migration has this precedent (the other `IF [NOT] EXISTS` are Prisma's
  `CREATE SCHEMA`/`EXTENSION` and trigger bodies).
- **Scenario:** none at runtime. The defect is the rubric's "production code only a test uses".
- **Fix:** remove `IF NOT EXISTS` from line 3. The test then runs only the file's data steps: the `UPDATE` and the
  `INSERT`, exactly as written, with the `ALTER TABLE` statement filtered out. The lane's `migrate deploy` already
  applies the whole file to its empty database, and that proves the DDL. Its header comment already calls them "the
  data steps". The alternative: each run does `DROP COLUMN` and then the whole file, inside one interactive
  transaction, so a failure leaves the column in place. **Belongs:** fix round, folded into `e1beddc1`. Plausible side
  effect: `masaha_we_dev` already applied the old text, so `migrate dev` there will report the migration as modified.
  That is local only, because CI's databases are fresh.

### F2 — should-fix · The new row breaks the code before it: a rollback, or a tab still on the old bundle
- **Where:** `migration.sql:15–19` (`icon = 'venus'`). The rule it breaks is `docs/development/setup.md:197`: "Every
  migration must work with the code before it: a rollback on Vercel brings the old code back, never the old
  database".
- **Seen in the code** (`origin/main`, the code before this PR): `GlyphIcon`'s `GLYPHS` has no `venus`, and `const Glyph
  = GLYPHS[name]; return <Glyph …/>` renders `undefined`, which React refuses. Two pre-PR paths draw an active
  catalogue amenity's `icon` as-is:
  - `features/lookups/components/list/AmenityRow.tsx:26` → `AmenityIcon.tsx:9`, on the admin's lookups page;
  - `features/lookups/components/amenities/AmenityChecklist.tsx:63`, on the owner's and the admin's «المرافق» Sheet.
    `useAmenityChecklist` maps only *retired* amenities through `iconOf`. Active ones keep `amenity.icon`.

  The old API passes `icon` through unvalidated ("Written only from AMENITY_ICON_KEYS"), and the web repository
  parses nothing.
- **Scenario:** #145 deploys and `migrate deploy` inserts the hall. Then either:
  - **a rollback:** a Vercel rollback to the pre-#145 deployment keeps the row. The admin opens Lookups › amenities, or
    any owner opens «المرافق»'s Sheet, and the page fails to render;
  - **an old tab:** a tab still running the pre-#145 bundle refetches the catalogue and fails the same way. Plausible:
    it depends on Vercel's skew protection, which the repository cannot show.
- **Fix:** no change to this PR's code can protect the old code.
  - **A rollback step in the PR's migration section:** before rolling back past #145, run `UPDATE amenities SET icon =
    'users' WHERE key = 'womens_hall'`, and restore `venus` once the new code is back.
  - **A finding:** the web crashes on an icon key it does not know (`GlyphIcon` / `AmenityIcon`), so every migration
    that adds an icon key breaks the code before it. A fallback, like the one `iconOf` already gives retired amenities,
    would make the next key safe.

  **Belongs:** finding **227** (the next free number: the index ends at 226), and the PR description. If the owner
  wants the fallback now, it is its own small item; it does not fix this deploy.

### F3 — should-fix · R1-F2's "no ghost hover on the selected entry" assertions cannot fail
- **Where:** `apps/web/src/pages/site/account/AccountLayout.component.test.tsx:117`,
  `apps/web/src/features/spaces/components/editor/SpaceEditor.component.test.tsx:343`,
  `apps/web/src/features/directory/components/near/LocationStatus.component.test.tsx:118–121`. All three are
  `not.toHaveClass('bg-secondary', 'hover:bg-hover')`.
- **Seen in the code:** jest-dom's `toHaveClass(a, b)` passes only when **all** of the classes are present
  (`isSubset$1(expected, received)`, `node_modules/@testing-library/jest-dom/dist/matchers-*.mjs:952–1003`). Negated, it
  fails only when both are present. No `Button` variant carries both: `secondary` has `bg-secondary` and a `color-mix`
  hover, while `ghost` and `outline` have `hover:bg-hover` and no `bg-secondary`.
- **Scenario:** the break is `variant={current ? null : 'ghost'}` → `variant="ghost"` in `AccountLayout.tsx` or
  `SectionIndex.tsx` (the `className` with `bg-accent text-accent-foreground` kept), or `null` → `'outline'` in
  `NearMeButton.tsx`. The selected entry then turns to the neutral `hover` fill under the pointer, which is exactly
  what the comments ("kept under the pointer", "no ghost hover") say it never does. All three tests still pass.
  `check:classes` does not catch it either, because `hover:bg-hover` is not the tint. Each test still fails on the
  old `secondary`, through its positive `toHaveClass('bg-accent', …)` half, which is why the "seen failing" in the
  report is true of the test but not of this half.
- **Fix:** split each line in two: `not.toHaveClass('bg-secondary')` and `not.toHaveClass('hover:bg-hover')`. Make the
  break above once and watch it fail. **Belongs:** fix round, folded into `8501d64e`.

### F4 — should-fix · The favourites' `womensHall` is unproven
- **Where:** `apps/api/src/modules/directory/directory.service.ts:224–227`. The favourites pass `womensHallId` to their
  own `publicListing.page` call, apart from `filterOf`.
- **Seen in the code:** no API test sets the hall on a favourite. `womensHall`/`worksEvenings` appear only in
  `list.api`, `liveStatus.api` (the keys), `filters.api` and `page.api`. The PR states X12, "the favourites' cards carry
  both fields", and the Definition of Done asks that every claim name its proof.
- **Scenario:** dropping `womensHallId` at line 227 makes `womensHallOf` answer `false` for every favourite. The account's
  favourites lose «قاعة للنساء» on every card, and no test fails.
- **Fix:** in `directory/favorites.api.test.ts`, add a favourite linked to an active `womens_hall` (not the first
  amenity id) that reads `womensHall: true`, and one without it that reads `false`. **Belongs:** fix round, folded into
  `07691835`.

### F5 — should-fix · The hint hidden where the space is read-only is unproven
- **Where:** `apps/web/src/features/spaces/hooks/hours/useHoursSection.ts:39` (`host.editable && eveningEndsEarly(…)`).
- **Seen in the code:** every view case in `HoursSheet.component.test.tsx` renders an editable profile. X5 ("the view
  shows it only where the space can be edited") is stated in `spaces.md` (the hours text and the web decision) and in
  the PR.
- **Scenario:** dropping `host.editable &&` would show «شغّلت الدوام المسائي…» to the admin on a verified space they
  cannot edit, and no test fails.
- **Fix:** add one component case: the admin's page of a verified space, with the switch on and every day closing by
  18:00, shows «دوام مسائي» and no hint. **Belongs:** fix round, folded into `2c73d610`.

### N1 — nit · T18 checks the public page's «دوام مسائي» in Arabic only, with no axe
- **Where:** `apps/web/src/features/directory/components/page/SpaceDetails.component.test.tsx` (the new case after
  line 198).
- **Scenario:** the page's English line `copy.directory.page.hours.evening` ("Evening hours") is never rendered by a test.
  Catalogue parity proves only that the key exists. The review prompt asks for both languages and axe on the public
  page's line.
- **Fix:** add one English render of the same case, with axe on the hours section. **Belongs:** fold into `fae90db1`.

## The test matrix rows (present / missing / weaker · would it fail on its break?)

- **T1** present (API) · yes. `>= 1200` → `> 1200` fails, because «At Eight» closes at exactly 1200. A widened
  boundary fails too («Half Seven», 1170). The plan's second break (drop `NOT is_closed`) cannot be built:
  `space_hours_range_check` forces a closed day's minutes to `NULL`, so the clause is redundant. That is not a gap.
- **T2** present · yes. `MAX+1` → `1` fails (6 is expected over a retired 5). With `ON CONFLICT` dropped, the second run
  raises a unique violation.
- **T3** present · yes. With `HAVING` dropped, an empty catalogue gets a row. A key already held is left as it is.
- **T4** present (shared unit) · yes. With `.optional()`, `undefined` passes and the `required` expectation fails.
  `invalid_format` for a non-boolean is checked too.
- **T5** present (API) · yes. Both breaks fail it: an unchanged check blind to the switch, and a missing write. The
  date, the audit `before`/`after` and the kept week and shifts are all asserted.
- **T6** present · yes, when the read and the request disagree on the switch.
- **T7** present: the admin read in `hours.api`, the public page in `page.api`.
- **T8** present, in `filters.api.test.ts` (planned in `hours.api`) · yes. With the 20:00 rule restored, «Switch Off
  Late» passes and «Switch On Early» fails. It is combined with every filter, list and map, through `it.each(ALL)`
  and the map-parity case.
- **T9** present · yes. A hard-coded id 1 fails, because the hall is id 2 behind «internet». With the active check
  dropped, a retired hall passes. Missing, list, map and combined cases are all present.
- **T10** present for the list (`worksEvenings` both ways; `womensHall` false in `list.api`, true in `filters.api`).
  **Missing for the favourites** (F4).
- **T11** present · yes, whether the refusal is removed or made unconditional. Nothing is written, the other fields in
  the body included, and the audit stays empty.
- **T12** present (unit) · yes: `<=` → `<` at 1080.
- **T13** present (en, ar, axe) · yes. It fails if the Sheet sends `false`, if `sheetOf` is always `false`, or if `<`
  replaces `<=`. "The switch alone is a change" is proven by the saved toast and the write.
- **T14** present, in `HoursSheet.component.test.tsx` (planned as a new file) · yes when the line is dropped. **The
  read-only branch is missing** (F5).
- **T15** present (unit `shiftsForm` + component) · yes.
- **T16** present (`filtersOf`, `paramsOf`, `requestOf`; `women=true` and `womensHall=1` read as false) · yes.
- **T17** present (`FiltersSheet`: the box, the address and the count of 8; `useFiltersPanel`: the clear of six boxes)
  · yes.
- **T18** present, **weaker**: Arabic only, no axe (N1).
- **T19, T20** present · yes.
- **The card's marks** (phase 2): `cardView.unit` (on and off) and `SpaceCard.component` (the description's order, one
  mark without the other, Arabic with axe) · yes, whether a mark is removed or reordered in `details`.
- **The carried tests:** R1-F1 (the class pair), R1-F3 (8 new cases and 2 negatives), R1-F5 (a hand-written
  `#471f46`), R2-F1, R2-F2 · each can fail. R1-F2: the positive halves can fail; **the negative halves cannot** (F3).
- **`AMENITY_IN_FILTER`:** all four steps of backend conventions §4 are met (shared code, both catalogues, contract §6,
  T11 provokes it).

## Decisions E1–E9, W1–W6 and X1–X16 (built / departed, judged)

**The evening**
- **E1** built: the glossary, spaces.md and directory.md say it is the time most spaces have closed, never a shift.
- **E2** unchanged: still one range a day.
- **E3** not built, as decided.
- **E4** built: one column, no evening prices, no evening section.
- **E5** built: nothing new is public but the line.
- **E6** built: the box under the hours in the Sheet, in both of its views; «دوام مسائي» in the view, on the public
  page and on the card. The admin's editor is the same component.
- **E7** built: `if (filter.evening) conditions.push(sql\`s.works_evenings\`)`. The 20:00 rule is removed.
- **E8** built: the backfill is the removed predicate verbatim (below).
- **E9** built: never blocking (T13 saves through the hint), in the owner's approved words.

**The women's hall**
- **W1** built: the glossary.
- **W2** built.
- **W3** built, by the key `womens_hall` in the migration, with X9's departure (below). It is ticked in «المرافق» like
  any amenity, and shown on the public page with its icon.
- **W4** built: the card's mark.
- **W5** built: the third box of «أخرى».
- **W6** built: no «مختلطة» or "mixed" anywhere in either catalogue, and nothing is drawn without the hall.
- R2 stands: no filter over the catalogue.

**The decisions taken without the owner**
- **X1** `worksEvenings` / `works_evenings` — sound.
- **X2** the switch inside `SpaceHours` and the hours request — sound (E6).
- **X3** required in the body — sound: a client that leaves it out is refused, never silently turns it off.
- **X4** the hint while no open day closes after 18:00 — sound (E9's words). The 18:00 boundary is tested.
- **X5** the hint in the view and the Sheet from one rule, in the view only where editable — acceptable. The read-only
  branch is unproven (F5).
- **X6** superseded by the owner's texts, which are built exactly. Checked byte for byte in both copy catalogues,
  `HoursSheet.component.test.tsx` (the two quotes of the hint), `spaces.md`, `lookups.md` and the PR description. The
  English carries the same meaning.
- **X7** `venus` — sound: installed, and distinct from `users`.
- **X8** retiring refused on the server (409) — sound. The check sits under the row lock, before any write, so nothing
  is written. A hand-retired hall stays retired and can be restored, and passes no space meanwhile (tested).
- **X9** the row only into a seeded catalogue, the seed adding it ninth — acceptable. It departs from the letter of W3
  ("by the migration in every environment"), for a sound reason: a tie at order 1. Production is seeded, so it gets
  the row from the migration.
- **X10** API `womensHall`, address `women` — sound.
- **X11** no fields on the pin — acceptable: the map's chosen card is `SelectedCard`/`SpaceSummary`, not `SpaceCard`.
  The owner may want the marks there later.
- **X12** the favourites carry both fields — sound in code, unproven (F4).
- **X13** no ADR — sound.
- **X14** no plan stop — the owner's instruction.
- **X15** «No amenity is a filter» marked revised — sound.
- **X16** each unit's API, web, tests and docs in one commit — sound (workflow §3).

## The report's deviations, judged
- **Five planned commits → four → six:** acceptable. Each is a complete unit; the carried fixes come first, as the owner
  asked.
- **Built without a plan stop:** the owner's instruction, stated in the plan.
- **PR title = the db commit's subject:** acceptable. Workflow §3 says "the main commit"; this one names both halves.
- **No local run for the last text change:** known and accepted. CI is green on this head.
- **T8 and T14 in other files than planned:** acceptable.
- **Phase 1's five component timeouts:** resolved. Phase 2's lane had none, and CI is green.
- **`IF NOT EXISTS`:** declared, but a departure from testing §3 rule 2 that was never approved → F1.
- **`apps/api/.env` and the `backup/women-evening-*` branches left in place:** local, acceptable, the owner's to clean.
- **The report's earlier sections quote the superseded X6 wordings:** it says so. Acceptable.
- **"Every new test seen failing first":** true of each test as a whole. F3's halves could never fail.

## The migration, read line by line
- **1–3, the column:** `ADD COLUMN IF NOT EXISTS "works_evenings" BOOLEAN NOT NULL DEFAULT false` matches
  `worksEvenings Boolean @default(false) @map("works_evenings")`, so there is no drift and no index is needed. A
  constant default is metadata-only on PostgreSQL ≥ 11, and existing rows read `false`. `IF NOT EXISTS` → F1.
- **5–10, E8:** `UPDATE … WHERE EXISTS (… NOT h.is_closed AND h.closes_minute >= 1200)` is the predicate removed from
  `publicListing.repository.ts` (`EVENING_FROM_MINUTE = 20 * 60`) verbatim. On the day it runs, «مفتوحة مساءً»
  therefore keeps exactly the same spaces; deleted and hidden spaces are switched on too, which is harmless. Closed
  days are excluded twice: by `NOT is_closed`, and by the CHECK, which keeps their minutes `NULL`. The statement writes
  only `works_evenings`. `spaces.updated_at` is Prisma's `@updatedAt`, not a trigger, so it is not touched;
  `hours_updated_at` is not touched either, which is right, because no owner saved anything. On a re-run: Prisma never
  re-applies an applied migration. Only the test re-runs it, and there a re-run would switch an owner's "off" back on,
  which does not concern production.
- **12–19, W3:** `INSERT … SELECT … FROM "amenities" HAVING count(*) > 0 ON CONFLICT ("key") DO NOTHING`.
  - An aggregate with no `GROUP BY` yields one row, or none on an empty catalogue (T3).
  - `MAX(sort_order)` spans active and retired rows, so the hall is last.
  - `updated_at` is supplied, as it must be: it has no database default.
  - `created_at` takes its default, and the id comes from the sequence; a conflict burns one value, which is harmless.
  - `amenities_key_key` backs the `ON CONFLICT`.

  X9's seed path: the seed upserts by key with `update: {}` and `sortOrder: index + 1`. A database seeded before keeps
  the migration's row; a fresh one gets the hall ninth (T20). The data's `'Women''s hall'` uses a straight
  apostrophe, as the seed's other names do (`Al-Shuja'iyya`), while the copy uses ’. Data and copy already differed
  that way.
- **What production sees:** one `ADD COLUMN`, one `UPDATE` over `spaces` (a small table) and one `INSERT`, in one
  migration. It is compatible with the code before it, except for the icon key (F2).

## Documents
- **api-contract:** the hours body (`worksEvenings` required, `required`/`invalid_format`), the audit shape, `SpaceHours`,
  the filters (`evening` revised, `womensHall` new, both for the map through "the filters"), `DirectorySpace`'s two
  fields, the list query, `PATCH /admin/amenities/:id` 409 and the §6 code list. All true to the code.
- **data-model:** Space, Amenity (one fixed filter, never retired), freshness and «Open in the evening» (marked stored,
  beside the rule it replaced). True.
- **directory.md:** decision 8 marked revised by E7, plus the new decisions (`womensHall`, the card's field, the marks,
  the address `women`, the count of eight, the page's line) and the history. True. "The map's chosen card is another,
  unchanged" is true.
- **spaces.md:** the hours text with the approved Arabic quoted exactly, the API and web decisions, the history. True.
- **lookups.md:** the fixed amenity, the row's refusal (the approved text), X8, X9, nine icons, and «No amenity is a
  filter» marked revised. True.
- **The rest:** conventions (the composed read), the glossary (two terms), overview (the v1 line per the owner's W5,
  and the Built line), foundation §3 (e) and §16. True.
- **finding 226:** names files that exist, and `Table.tsx:64`'s classes as quoted. The prototype's new icon path
  resolves.
- **Missing:** F2's rollback step and its finding. No `#PRNUM` is left. No ADR is needed.

## Scope and commits
- **Size:** six commits, 115 files. The subjects are Conventional and ≤ 50 characters, except `2c73d610`'s 51 (waived).
- **Content:** each commit holds its unit's API, web, tests and documents. There are no tool-attribution trailers.
- **No extras:** no new dependency (`Venus` comes from the installed lucide-react), no second migration, and nothing
  from the *Not in v1* list. Nothing outside the task besides the ten carried items; R1-F4 is record-only.
- **Authorization unchanged:**
  - the hours `PUT`s keep `can()` and their role tests (bodies updated with the switch);
  - the amenities `PATCH` stays ADMIN-only;
  - the new filter is public, like the others.
- **The carried fixes' neighbours:**
  - the account navigation: the non-current links keep the ghost hover (asserted);
  - the profile's index: the current entry has `aria-current` and the tint;
  - NearMe: `variant={null}` drops cva's default (null ≠ undefined), and the base `border border-transparent` lets
    `border-spark` show;
  - `check:classes`: the spellings map is applied after the `group-`/`peer-` and `/name` strip. `active` matches only
    the bare variant (not `data-active` or `not-data-active`), and CI's `check:classes` is green on the tree.
- **The `? 'secondary'` sweep:** only `LiveStatusControl.tsx:48` remains (a tone, rightly left).

## Not checked, and why
- **Nothing was run:** this is a read-only review (no tests, checks, servers or database). CI's green run on this head
  stands for lint, typecheck, the three lanes, build and the `check:*` scripts.
- **The migration's effect on real data** (21 of 38 spaces switched on, the hall ninth) is the report's own count; I
  did not apply it anywhere.
- **The screens:** RTL/LTR, light/dark, 390/1440, the ♀ glyph's look and the muted marks' contrast on a hovered card
  were not seen. The screenshots are local to the worker, so I judged from the code only. The marks reuse the card's
  existing `text-muted-foreground` lines on the same `hover:bg-hover`.
- **The worker's `results.txt`** (35 real-run checks) was not read.
- **Vercel's skew protection** is not visible from the repository, so F2's old-tab case is plausible; its rollback case
  is not.
- **Prisma reporting an edited applied migration in `masaha_we_dev`** (F1's note) is from Prisma's documented
  `migrate dev` behaviour, not observed.
