# WOMEN_EVENING — the report (2026-11-12)

> Phase 1: the build of the decisions (2026-11-12 to 11-14). Phase 2, the rebase on the merged identity, the carried
> review fixes and the card's marks, is its own section at the end.

## Branch and head

- Branch **`feat/women-evening`**, local only (never pushed, no PR), cut from `main` `f58c12a8`.
- Head: **`9b7759229f0bb4aeb5f049dc48f9f63a632f26ce`**.
- A local backup branch, `backup/women-evening-pre-fold` (`e5d6125c`), keeps the head from before one fold (below);
  delete it when convenient.

## Commits (4; 93 files, +1041 −159)

| Commit | Subject | What |
|---|---|---|
| `486afe8f` | feat(db): add the evening switch and women's hall | `spaces.works_evenings`; the migration (column, E8 switch-on, W3 row); the seed's ninth amenity; the `venus` icon key, glyph (`VenusIcon`, `GlyphIcon`) and names; T1–T3, T19, T20 |
| `e0f7f676` | feat(spaces): the evening switch in the hours group | shared `SpaceHours.worksEvenings` and the required request field; the hours save, read and audit; the profile's box, line and hint (one rule, `eveningEndsEarly`); the shifts' Sheet sends the switch as read; spaces.md, data-model, contract, glossary; T4–T7, T12–T15 |
| `74718daa` | feat(directory): filter the evening by the switch | `evening=true` by `s.works_evenings` only; the card's `worksEvenings`; the public page's «دوام مسائي»; directory.md (decision 8 marked revised), contract, data-model; T8, T10 (evening), T18 |
| `9b775922` | feat(directory): the women's hall filter | `womensHall=true` by the amenity's key (`WOMENS_HALL_KEY`, resolved by `lookups`, active only); the card's `womensHall`; the admin's rule (409 `AMENITY_IN_FILTER`); the panel's «قاعة للنساء» and `women=1`; lookups.md, directory.md, contract, data-model, conventions, glossary, overview; T9, T10 (hall), T11, T16, T17 |

Each commit passed `lint` and `typecheck` before it was made. `#PRNUM` stands where a PR number belongs.

## The migration and the databases

- **One migration**, `20261112121413_women_evening`, created with `migrate dev --create-only` **once**, then read and
  written by hand (`ls` showed it; `masaha_we_dev`'s history still had 32 rows, so nothing was applied by the create):
  1. `ALTER TABLE "spaces" ADD COLUMN IF NOT EXISTS "works_evenings" BOOLEAN NOT NULL DEFAULT false;`
  2. E8: `UPDATE "spaces" SET "works_evenings" = true WHERE EXISTS (an open day with closes_minute >= 1200)`;
  3. W3: `INSERT INTO "amenities" (key, name_ar, name_en, icon, sort_order, is_active, updated_at) SELECT
     'womens_hall', 'قاعة للنساء', 'Women''s hall', 'venus', COALESCE(MAX(sort_order), 0) + 1, true,
     CURRENT_TIMESTAMP FROM "amenities" HAVING count(*) > 0 ON CONFLICT ("key") DO NOTHING;`
  Comments carry the date, never a PR number. No data lost; no other row touched. `IF NOT EXISTS` lets the API test
  run the file as written. No data-loss refusal met; `migrate reset` never used.
- **Applied** to `masaha_we_dev` with `migrate deploy`: **21 of its 38 spaces** switched on (the same 21 the old rule
  passed, counted before the apply), `womens_hall` added **9th**, active, after the eight.
- **Databases** (shared container, port 5433): `masaha_we_dev`, a **copy of `masaha_dev`** made with `pg_dump -Fc`
  and `pg_restore --no-owner` inside the container (no template copy; restore exit 0: 38 spaces, 8 amenities,
  32 migrations); `masaha_we_test`, empty, migrated by the lane's setup. `masaha_dev`, `masaha_test` and
  `masaha_design_*` were never touched; `db:seed` was never run.
- **`apps/api/.env`** backed up to `apps/api/.env.bak-we` (git-ignored), then `DATABASE_URL` → `masaha_we_dev` and
  `TEST_DATABASE_URL` → `masaha_we_test` (only those two values rewritten; the file never printed). **It is left
  pointing at `masaha_we_*`** for the work after the identity merge; restore it with
  `cp apps/api/.env.bak-we apps/api/.env` to go back to `masaha_dev`/`masaha_test`.

## Tests seen failing (each break made, seen failing, restored from a `cp` backup and checked with `cmp`)

| Test(s) | Lane | Break that failed it |
|---|---|---|
| T1 migration: evening switched on at ≥ 20:00 | API | `>= 1200` → `> 1200` |
| T2 migration: `womens_hall` added last, once | API | `MAX+1` → `1`; then `ON CONFLICT` dropped (second run fails) |
| T3 migration: none into an empty catalogue; a key held left alone | API | `HAVING count(*) > 0` dropped; `ON CONFLICT` dropped |
| T20 seed: nine amenities, `womens_hall` last | API | the seed's `womens_hall` entry removed |
| T19 `GlyphIcon` draws `venus` | component | `venus` taken out of `GLYPHS` |
| T4 schema: `worksEvenings` required, boolean | unit (shared) | `.optional()` |
| T5 the switch alone: written, dated, audited, week and shifts kept | API | the unchanged check made blind to the switch; separately, the switch's write removed |
| T6 unchanged week + switch writes nothing; T7 admin read carries it | API | the switch's write removed |
| T7 public page carries it | API | the facts reader answering `worksEvenings: false` |
| T12 `eveningEndsEarly` (18:00 included) / `sheetOf` reads the saved switch | unit | `<=` → `<`; `sheetOf` always `false` |
| T13 the box: sends the switch alone; opens ticked; the hint (en, ar, axe) | component | the Sheet sending `false`; `sheetOf` always `false`; `<=` → `<` |
| T14 the view's line and hint (en, ar, axe) | component | the line's text removed (`{null}`) |
| T15 the shifts' Sheet sends the switch as read | unit + component | `shiftsInput` sending `false` |
| T8 `evening` by the switch only, alone and with every filter | API | the old 20:00 `EXISTS` rule restored |
| T10 the card's `worksEvenings` (and the keys test) | API | the field dropped from `toDirectorySpace` |
| T18 the public page's «دوام مسائي» | component | the page view's `evening: null` |
| T9 `womensHall` by the key, list and map, combined | API | the hall's id hard-coded as `1` (11 tests failed) |
| T9 a retired hall passes none | API | the `isActive: true` dropped from the id-by-key lookup |
| T10 the card's `womensHall` | API | the field dropped from `toDirectorySpace` |
| T11 retiring the hall is 409 `AMENITY_IN_FILTER`, nothing written | API | the refusal removed |
| T11 rename, icon, order still open; another retires | API | the refusal made unconditional on the key |
| T16 `women=1` read, written, round trip; the request's `womensHall` | unit | `womensHall: false` in `filtersOf`; the request's line removed |
| T17 the panel's box, its address, the count (8), the clear (6 boxes) | component | the box removed; the count's line removed |

## Verification (phase 1, on the head `9b775922`)

Every heavy run went through `heavy.mjs we` (the identity's lead first). The machine was short of memory throughout
(often 3–4 GB free), so several runs waited long for a grant.

| Check | Result |
|---|---|
| `lint`, `typecheck` | clean on every commit, before it was made (the fold into commit 1 touched two test files and one copy string; the head's typecheck ran after it) |
| `format:check` | clean for every tracked file; it warns on `.claude/launch.json`, an untracked, git-ignored local file that is not mine (CI never sees it) |
| `check:classes`, `check:links` (3,272 links), `check:conflicts` | clean (2026-11-13) |
| `NODE_ENV=production npm run build` + `check:build` | clean: no showcase code in 76 build files, no dashboard code or heavy library in the site's first download (2026-11-13) |
| `test:unit` | **green**: api 324, shared 921, web 1,260 (2026-11-13, on the head) |
| `test:component` | 2026-11-12, on the head after the fold: **2,107 passed**. 2026-11-13, on the same head, in two shards (a whole run had been stopped for memory; the owner's rule: retry once): shard 1, 1,089 passed and **4 timed out** (`HoursSheet` ×2 at 15 s, `IncomeTab`, `PaymentsLedger` at 5 s); shard 2, 1,013 passed and **1 timed out** (`CorrectSheet`, 5 s). No assertion failed. Those four files, run alone, **all pass** (35 + 6 tests); the slowest `HoursSheet` test takes 6.9 s alone against 17.7 s in the shard: load, not the change. No timeout was raised. CI judges again before the PR |
| `test:api` | **green: 1,446** (2026-11-12 whole, after one run stopped for memory and retried; 2026-11-13 again in two shards, 689 + 757) |
| The migration's data steps | the API lane (`womenEveningMigration.api.test.ts`), and applied to `masaha_we_dev` (21 of 38 switched on, `womens_hall` 9th) |

## The real run (2026-11-13, API 3320 / web 5320 on `masaha_we_dev`)

Headless Chrome over CDP (no new dependency), signed in as the directory demo owner (space 2, `noor-hub`) and as the
admin; `nasr-coworking` (space 12, no owner, switch off) for the admin's editor. Over HTTP first:
`GET /spaces?evening=true` gave 20 listed spaces, every card `worksEvenings: true`; `womensHall=true` gave 0 until a
space ticked it. 25 checks, all **PASS** (`Downloads\women-evening-shots\results.txt`):

- **The owner's profile:** «دوام مسائي» under the hours after E8, no hint (a day closes at 22:00); the Sheet's box opens
  ticked; unticked and saved alone, the line goes; ticked again and saved, it is back.
- **The admin:** the women's hall's switch on the lookups page is refused, its row saying «لم يُحفظ التغيير — لا يمكن
  إيقاف هذا المرفق: دليل المساحات يصفّي به. يمكنك تغيير اسمه وأيقونته وترتيبه.»; in the editor of `nasr-coworking`,
  «قاعة للنساء» ticked and saved; the hours' box ticked, the hint shown live (its week ends at 17:00), saved.
- **The directory (guest):** the box «قاعة للنساء» writes `?women=1` and lists `nasr-coworking` alone; with «مفتوحة
  مساءً», `?evening=1&women=1`; a reload keeps both boxes ticked (the address round trip); at 390 in English and dark,
  the sheet shows «Women’s hall» ticked in «Other», the button counting 3, «No results» (the one hall space is
  unverified and «Verified spaces only» is on).
- **The public page:** «دوام مسائي» under the hours, «قاعة للنساء» among the amenities with the ♀ icon, never «مختلطة».

**Screenshots** (curated, never committed), `C:\Users\basel\Downloads\women-evening-shots\`: 01 the owner's hours
(ar, 1440, light) · 02–03 the hours' Sheet, the box ticked, and with the hint · 04 the owner's hours at 390, dark, in English, and its
Arabic twin (retaken 2026-11-14: the first take missed the hours card; the retake's first try came out in Arabic, a
sign-in switching the language, hence the `FAIL` line in `results.txt`, kept as `04-…-ar-390-dark`) ·
05 the admin's refusal · 06 the amenities' Sheet with «قاعة للنساء» · 07 the hours' Sheet with the hint · 08 the
editor's hours with «دوام مسائي» · 09–10 the directory with `?women=1` and `?evening=1&women=1` · 11 the filters' sheet
(en, 390, dark) · 12 the public page's hours and amenities (ar, 390, light) · 14 the same (en, 1440, dark).

## Problems met, and anything unexpected

- **Runs stopped for memory.** Claude Code stopped background runs while the session was idle and memory was
  critical: the API lane (once), the component lane (once) and one break script. Each lane was retried once (the
  owner's rule), in the foreground or in shards so it would not idle; all ended green but for the load timeouts
  above.
- **A "stopped" shell lived on.** The break script stopped for memory kept running: its shell resumed editing files
  while I ran the next break, so one result was invalid. I stopped its processes by PID, restored the three files from
  their `cp` backups (`cmp`-checked) and redid those breaks one at a time; every result in the table above comes from
  the clean runs.
- **Stale grant slots.** Two of my stopped runs left `heavy-slot-*` behind with no holder (2026-11-12 14:05, and
  2026-11-13 13:56); I freed each, with a `NOTE` line in `heavy-grants.log`. The lead freed one other (13:36).
- **The machine's restart (2026-11-13/14)** cleared my scratch folder (the run scripts and lane logs); the results
  were already in this report. The servers and Chrome died with it.
- **A fold.** The full component lane found two tests that list the icon grid's eight options (now nine), and the
  English icon name used a straight apostrophe where the catalogue uses ’; both fixed and folded into commit 1
  (`fixup` + `autosquash`), the earlier head kept as `backup/women-evening-pre-fold`.
- **The heredoc and Python escape traps** of this shell (a `\U` in a Windows path broke one script): edits went through
  files in the scratch folder.
- **Data in `masaha_we_dev` the real run changed:** `noor-hub`'s switch off and on again (its hours dated 2026-11-13),
  and `nasr-coworking` given the women's hall and the evening switch (dated too). `masaha_dev` untouched.
- **`masaha-demo` (space 1) is soft-deleted in this copy**, so the owner's run used the directory demo owner instead.
- **A sign-in switches the interface to the account's language**, so screenshots meant in English were retaken after
  setting it again (04).
- **A vite on 5320 was already running when I resumed on 2026-11-14,** started at 09:16 from this folder, not by me; I
  used it and left it running. I stopped only what I started.
- **Servers:** the API on 3320 that I started each time was stopped by PID (`tsx watch`, the server and `pino-pretty`)
  and the port checked free (2026-11-13 by the restart; 2026-11-14 by me).

## Decisions taken without the owner

Each is recorded in its capability document's *Decisions* too. The Arabic of `AMENITY_IN_FILTER`, of the hint and of
the box's help line needs the owner's approval.

- **X1 — The switch's name: `worksEvenings` / `works_evenings`.** Options: `evening`, `opensEvenings`,
  `worksEvenings`. Why: the owner's words («المساحة تعمل مساءً»); `evening` stays the filter's name.
- **X2 — Where it travels: inside `SpaceHours` and the hours request.** Options: a field of the space read apart; part
  of the hours. Why: E6 puts it in the hours group — one save path, one date, one staleness, one audit entry.
- **X3 — Required in the body.** Options: optional with a default of false; required. Why: the group is saved whole;
  a client that left it out would turn it off unseen (the own amenities' S1 precedent). The shifts' Sheet sends it
  as last read.
- **X4 — The hint's rule: on while the switch is on and no open day closes after 18:00** (an 18:00 close hints).
  Options: after 18:00 (E9's words); at or after 20:00 (the old rule). Why: E9's words; E1 places most closings at
  16:00–18:00.
- **X5 — The hint's place: the view and, live, the Sheet, from one pure rule (`eveningEndsEarly`).** Options: the view
  only; both. Why: the Sheet is where the owner decides; the view where it is read again; one rule cannot drift. The
  view shows it only where the space can be edited (not to the admin on a verified space).
- **X6 — The hint's wording:** «شغّلت الدوام المسائي، لكن ساعات العمل تنتهي مبكرًا: لا يُغلق أي يوم بعد 18:00.» /
  "Evening hours are on, but the opening hours end early: no day closes after 18:00." Options: the owner's sketch
  «… ساعات عملك تنتهي مبكرًا». Why: «ساعات العمل», not «ساعات عملك», since the admin's editor shows it too; the
  added clause says what "early" means. The box's help: «يظهر للزوار «دوام مسائي»، وتقول ساعات العمل حتى متى تبقى
  مفتوحة.» / "Visitors see “Evening hours”; the opening hours say until when."
- **X7 — The icon: Lucide's `venus` (♀), installed in lucide-react 1.48.** Options: `venus`, `door-closed`,
  `user-round`, `armchair`. Why: the common sign of a women's place, and distinct from `users`, the meeting room's.
  Named «رمز المرأة» / "Women’s sign" in the icon grid.
- **X8 — The admin's rule on the amenity: rename, change its icon and move it, never retire it** — refused on the
  server, 409 `AMENITY_IN_FILTER`, nothing written (the rest of the body included), its text in the row. Options:
  allow everything (the filter would then keep spaces whose page shows no hall, since a retired amenity leaves the
  page); refuse retiring; hide the row's switch (UI only, never authorization). Delete does not exist in the lookups
  (nothing is ever deleted), so there is nothing to refuse there. A `womens_hall` already retired before the
  migration (hand-made) is left retired by it, can be restored, and passes no space while retired.
- **X9 — The amenity row on a fresh database:** the migration inserts only into a catalogue that has rows; the seed
  adds `womens_hall` ninth. Options: always insert. Why: on a fresh database the migration would insert it at order
  1, and the seed's eight (1–8) would tie it with «إنترنت»; "every environment" is met — every seeded one gets it from
  the migration, a new one from the seed.
- **X10 — The filter's names: API `womensHall=true`, address `women=1`.** Options: `amenity=womens_hall`. Why: one
  fixed filter, never a filter over the catalogue (R2 stands); named like `openFriday` / `friday`. The server finds
  the amenity by its key (`WOMENS_HALL_KEY`, `lookups.activeAmenityIdOf`), never an id.
- **X11 — No fields on the map's pin.** Why: E6/W4 name the directory's card; the map's chosen card is another
  component, unchanged.
- **X12 — The favourites' cards carry both fields** — they are `DirectorySpace`, for free.
- **X13 — No ADR.** Why: one column and one filter on existing patterns, reversible, each in one capability; the
  documents that own them (spaces, directory, lookups, data model, contract) record them.
- **X14 — No plan mode, no stop after the plan** — the owner's instruction for this task (stated in the plan).
- **X15 — The lookups' «No amenity is a filter» decision is marked revised**, not removed: the general amenities
  filter stays dropped (R2); only the women's hall is a filter.
- **X16 — The commits:** four units, each with its API, web, tests and documents together (the workflow forbids
  per-layer commits); the plan's five became four by merging the profile's web into the switch's commit.

## Waiting for the identity merge

> **Done in phase 2** (`69850267`, below): the marks, `VenusIcon` in the barrel and the showcase. Kept as written
> on 2026-11-12, the plan the build followed.

Each is a short step once `feat/ink-berry-identity` has merged; none touches a file of that branch today.

### 1. The card's two marks (E6, W4) — `features/directory/components/card/SpaceCard.tsx`

The API already answers both (`DirectorySpace.worksEvenings`, `DirectorySpace.womensHall`); the favourites' cards
are the same cards and get them for free. The exact design:

- **`services/cardView.ts`** (not identity's; left untouched now, since nothing would read it): add
  `evening: space.worksEvenings ? words.card.evening : null` and
  `womensHall: space.womensHall ? words.card.womensHall : null`, beside `verified`.
- **Copy** (`copy.directory.card`): `evening: 'دوام مسائي'` / `'Evening hours'`, `womensHall: 'قاعة للنساء'` /
  `'Women’s hall'` (the same words as the page's line and the filter's box).
- **`SpaceCard.tsx`**: in the row that holds `LiveStatusBadge` and «موثّقة», after «موثّقة», two marks drawn as
  «موثّقة» is (`<span id=… className="flex items-center gap-1 text-body-sm text-muted-foreground">` — muted, not
  `text-primary`: they describe the space, they do not certify it), with `MoonIcon` and `VenusIcon`
  (`aria-hidden`, `size-4`). Each gets its id (`${ids}-evening`, `${ids}-women`) and joins the link's
  `aria-describedby` right after `verifiedId`, so a screen reader hears name, area, status, verified, evening,
  women's hall, today, distance, price. Only a mark that holds is drawn (W6: never «مختلطة», nothing for a space
  without the hall).
- **`VenusIcon`** must be exported from `shared/design-system/index.ts` (identity's file): it is declared in
  `icons/iconSet.tsx` and exported from `icons/index.ts` now, but not yet from the layer's root barrel.
- **Tests:** `cardView.unit.test.ts` (each mark on/off), `SpaceCard.component.test.tsx` (both marks, the
  description order, none when off, axe ar/en).
- **Docs:** directory.md's card paragraph («… «موثّقة»، «دوام مسائي»، «قاعة للنساء» …») and the sentence that says
  the web's card does not draw them yet.

### 2. `foundation.md`

No line is needed today: §the icons names `GlyphIcon`'s closed set without listing its glyphs. Re-read it once the
identity has merged, in case its new text lists them.

### 3. The showcase's icons

`pages/showcase/sections/icons/IconsSection.tsx` lists the layer's icons from the root barrel; `VenusIcon` joins it
with the barrel export above (its registry and fixtures are identity's files).

## Phase 2 — on the merged identity (2026-11-14)

The supervisor's message (relayed by the owner): #144 merged (`main` = `88c5eb3f`), so the no-conflict rule is over.
Still no push and no PR.

### Branch and head

- **`feat/women-evening`**, local only, rebased on `origin/main` `88c5eb3f`.
- **Head: `698502673e25ca016fcc9ca3666f3088873d67d2`.**
- Backups (local branches, delete when convenient): `backup/women-evening-pre-rebase` (`9b775922`, phase 1's head),
  `backup/women-evening-pre-reorder` (the fixes commit before it was moved first), and phase 1's
  `backup/women-evening-pre-fold`.
- **The rebase was clean:** no file changed on both sides (`git diff --name-only f58c12a8 origin/main` against mine:
  none in common); no migration on `main` since `f58c12a8`.

### Commits (6 on `origin/main`; 115 files, +1286 −180)

| Commit | Subject | Files |
|---|---|---|
| `8501d64e` | fix(design-system): identity review follow-ups | 17 (+145 −15) |
| `e1beddc1` | feat(db): add the evening switch and women's hall | 15 |
| `6f6a59ab` | feat(spaces): the evening switch in the hours group | 32 |
| `ba163cab` | feat(directory): filter the evening by the switch | 29 |
| `9a1b6b63` | feat(directory): the women's hall filter | 47 |
| `69850267` | feat(directory): the card's evening and hall marks | 10 (+103 −9) |

The four of phase 1 are unchanged by the rebase but for their new parents. The fixes commit was made on top and moved
first by a scripted rebase (`git diff` between the head before and after the move: empty).

### The review fixes carried from #144 (`8501d64e`, first on the branch)

From `0_CARRIED_FROM_144.md`, each read against the reviews' *Where*, *Scenario* and *Fix*:

| Item | Change | Test, and the break that failed it |
|---|---|---|
| R1-F1 | `ContactsView.tsx`: the anchor `group`, the caption `group-hover:text-foreground` | `ContactsSheet.component.test.tsx` «turns a tile’s caption to the foreground…»: failed before the fix (no `group`). Foundation §5's wash sentence holds as written |
| R1-F2 | `AccountLayout.tsx`, `SectionIndex.tsx`: the current entry `variant={null}` + `bg-accent text-accent-foreground`, no ghost hover; `NearMeButton.tsx`: pressed takes the chip's selected look, `border-spark bg-accent text-accent-foreground`, kept under the pointer | `AccountLayout.component.test.tsx`, `SpaceEditor.component.test.tsx` (the index), `LocationStatus.component.test.tsx` (pressed): each failed before the fix (`bg-secondary`). **The sweep** (`git grep -nE "\? ?'secondary'"`): those three, and `LiveStatusControl.tsx:48`, left as it is — its `secondary` is the neutral tone of the live state's trigger, not a selected or pressed entry |
| R1-F3 | `checkClasses.ts`: `data-[state=open]` → `data-open`, `aria-[expanded=true]` → `aria-expanded`, `data-[highlighted]` and `=true` → `data-highlighted` before the lookup; `active` added; never `aria-selected`. Foundation §3 (e) says so | `checkClasses.unit.test.ts`: 8 new cases failed before the fix (plus `aria-selected:` and `data-[state=closed]:` not flagged). `check:classes` on the tree: clean |
| R1-F5 | — | `semantic.unit.test.ts`: `painted('dark', 'accent')` is `#471f46`. Passed on the code (right today); **break:** `OKLAB_TO_LMS[0][1]` `0.3963…` → `0.4963…`, failed |
| R1-F4 | **Recorded only:** [finding 226](../../../app/docs/architecture/findings/226-a-ghost-control-inside-a-hovered-table-row-has-no-hover-of-its-own.md) (the next free number; index row added), naming `Table.tsx`, `Button.tsx` and the three menus | — |
| R2-F1 | — | `browserIcons.unit.test.ts`: every shape outside `<defs>` names its class (two `use` ink, one `path` spark). **Break:** `class="ink"` dropped from one `<use>`, failed |
| R2-F2 | — | `routes.component.test.tsx`: T19 asserts the full form's `viewBox` `263 45 2473 903` at 1280, and a new case the mark's `190 17 778 778` at 800 (one logo only). **Break:** AdminLayout's `mark` and `logo` swapped, both failed |
| R2-F3 | `docs/design/prototype/Reset email.html`: the tab icon is `masaha/logo/masaha-mark-berry.svg` | the prototype's checks: `check-parse` 52/52, `check-classes` 0 new |
| R2-F4 | **No code:** for the PR description, under *Review fixes carried from #144*: #144's first download grew by **+15,681 B (+8,073 compressed)**; its description's 15,672 / 8,079 was the `design-system` chunk's growth | — |
| R2-F5 | Foundation §16: «the full logo and the mark, light and dark, and the app icon» | `check:links` |

### The items that waited for the identity (`69850267`)

- **The card's two marks (E6, W4):** `cardViewOf` gives `evening` and `womensHall` (a pin has neither field, so its
  chosen card shows none); `SpaceCard` draws «دوام مسائي» with `MoonIcon` and «قاعة للنساء» with `VenusIcon` after
  «موثّقة», muted (`text-muted-foreground`), and its link's description reads them right after «موثّقة»; nothing for a
  space without them (W6). Copy in both catalogues. directory.md: the card paragraph, the decision, the history.
  Tests: `cardView.unit.test.ts` (each mark on and off) and `SpaceCard.component.test.tsx` (both marks and the
  description's order; one without the other; Arabic with axe) — all four **failed before** the build.
- **`VenusIcon`** exported from the layer's barrel (`shared/design-system/index.ts`) and listed in the showcase's icons.
- **`foundation.md`:** no line was needed for the icon (it names `GlyphIcon`'s closed set without listing it); its
  two lines changed are the carried R1-F3 and R2-F5.

### Verification (phase 2, on the head `69850267`)

All heavy runs through `heavy.mjs we`.

| Check | Result |
|---|---|
| `lint`, `typecheck` | clean before each of the two new commits, and after the reorder |
| `format:check` | clean for every tracked file (the same untracked `.claude/launch.json` warning) |
| `check:classes`, `check:links` (3,299 links), `check:conflicts`; the prototype's `check-parse`, `check-classes` | clean |
| `NODE_ENV=production npm run build` + `check:build` | clean (no showcase code in 77 build files; the site's first download free of dashboard code and heavy libraries) |
| `test:unit` | **green:** api 324, shared 924, web 1,401 |
| `test:component` | **green:** 2,135 (two shards, 1,108 + 1,027), no timeout this time |
| `test:api` | **green:** 1,446 (two shards, 689 + 757) |

### The real run (phase 2, API 3320 / web 5320 on `masaha_we_dev`)

10 checks, all **PASS** (appended to `results.txt`):
- the directory's card of `nasr-coworking` (ar): described «النصر · غزة | مفتوحة الآن | دوام مسائي | قاعة للنساء | اليوم
  09:00–17:00»; `?evening=1` (en, 390, dark): all 18 cards marked «Evening hours», none says mixed;
- «الأقرب إليّ» pressed (location emulated in the Strip): the chip's selected look, the spark's edge `rgb(210, 126, 208)`;
- signed in as the directory demo owner: «Favourites», the current entry, selected with no ghost hover; the profile's
  index, the section in view selected; a contact tile hovered: its caption turns from `rgb(159, 166, 173)` to the
  label's `rgb(247, 251, 255)` (dark).

Screenshots, `C:\Users\basel\Downloads\women-evening-shots\`: `p2-01` the card's marks (ar, 1440, light) · `p2-02` the
evening's cards (en, 390, dark) · `p2-03` near me pressed (ar, 1440, dark) · `p2-04` the account's current entry (en,
1440, dark) · `p2-05` a contact tile hovered (en, 1440, dark). The API I started was stopped by PID and 3320 checked
free; no headless Chrome left. The vite on 5320 (not mine, started 2026-11-14 09:16) was used and left running.

### Problems and anything unexpected (phase 2)

- **The scratch folder had been cleared by the restart,** so the run scripts were written again (a small CDP driver
  and a steps file per run).
- **A vite on 5320 was already running** from this folder when I resumed; my own `vite` then failed to bind (`Port 5320
  is already in use`). I used the running one.
- **The phase-2 component lane had no timeouts** (memory was easier: ~4.7–5 GB free), unlike phase 1's.
- **`#PRNUM`** stands in the documents of all six commits where a PR number belongs.

### For the PR description (when the owner gives the word)

- *Review fixes carried from #144*: the ten items above (R1-F1, F2, F3, F5; R1-F4 as finding 226; R2-F1 … F5), with
  #144's first-download growth corrected (+15,681 B, +8,073 compressed).
- The new domain code `AMENITY_IN_FILTER`, its English and Arabic text, the Arabic marked for the owner's approval;
  the hint's and the box's Arabic too (X6).

## PR (2026-11-14)

The supervisor's message (relayed by the owner): the owner approved new wordings for X6's three texts, waived a
re-run for that text change, and gave the word to push and open the PR. Never merge.

### The pull request and its head

- **#145** — https://github.com/Basel-Ghonaim/masaha/pull/145 — "feat(db): add the evening switch and women's hall",
  assigned to the owner, labels `feat`, `area:web`, `area:api`, `area:design-system`, `area:docs`.
- **Head: `8f511d5a18f26e5cd3fc79828a0d878892b8fb4a`** (on `main` `88c5eb3f`).
- **CI on that head: green**, run 43584602551 (`headSha` = the head): build, check:classes, check:conflicts,
  check:links, format:check, lint, test:api, test:component, test:unit, typecheck — all pass; CodeRabbit skipped.
  GitHub: **`CLEAN`**, open.

### The commits (6; 115 files, +1286 −180)

| Commit | Subject |
|---|---|
| `8501d64e` | fix(design-system): identity review follow-ups |
| `e1beddc1` | feat(db): add the evening switch and women's hall |
| `2c73d610` | feat(spaces): the evening switch in the hours group (51-character subject, waived by the owner) |
| `fae90db1` | feat(directory): filter the evening by the switch |
| `07691835` | feat(directory): the women's hall filter |
| `8f511d5a` | feat(directory): the card's evening and hall marks |

The PR's title is the first feature commit's subject: it is the one that names both halves.

### What changed since phase 2

- **The owner's texts (X6),** each folded into the commit that introduced it (`--fixup` + `autosquash`; backup
  `backup/women-evening-pre-wording`):
  - the box's help — «يظهر للزوار «دوام مسائي»، وساعات العمل أعلاه تحدّد حتى متى تبقى المساحة مفتوحة.» / "Visitors see
    “Evening hours”; the opening hours above set until when the space stays open.";
  - the hint — «شغّلت الدوام المسائي، لكن ساعات العمل لا تمتد بعد 18:00 في أي يوم.» / "Evening hours are on, but the
    opening hours don’t go past 18:00 on any day.";
  - `AMENITY_IN_FILTER` — «لا يمكن إيقاف هذا المرفق، فدليل المساحات يعتمد عليه في فلتر «قاعة للنساء». يمكنك تغيير اسمه
    وأيقونته وترتيبه.» / "This amenity can’t be retired: the directory relies on it for the “Women’s hall” filter. You
    can still rename it, change its icon or move it."

  Into `2c73d610`: both catalogues' `spaces` copy, `HoursSheet.component.test.tsx` (its five quotes; its "no hint"
  query now `/past 18:00/`) and `spaces.md`; into `07691835`: both catalogues' `errors` and `lookups.md`. The diff
  against the backup: 7 files, 14 lines each way, nothing else. The quotes in this report's earlier sections keep the
  words as they were then.
- **`#PRNUM` → `#145`** in every commit, by `git filter-branch --tree-filter` over `origin/main..HEAD` (backup
  `backup/women-evening-pre-prnum`), the next number checked first (#144 the last); 36 lines in six documents, nothing
  else, line endings kept. No `#PRNUM` left.

### What was run, and what was not

- **Locally, phase 2 (on `69850267`, the same code but for the three texts):** everything, all green — see *Phase 2 ›
  Verification* (unit 324 / 924 / 1,401; component 2,135; api 1,446; build and every check) and its real run.
- **NOT run locally — the owner's word:** no test and no local check for the three texts' change; CI on the pushed head
  checked it (all ten jobs green). `prettier --write` was applied to the five changed code files (formatting, not a
  check). Said in the PR's *Evidence* too.

### The breaks made, and the tests seen failing first

As in phase 1's and phase 2's tables; none was added by the text change (it changes no behaviour, only the words the
existing tests quote).

### Problems met, and anything unexpected

None in this step: the fixups applied cleanly, the rewrite touched only `#PRNUM`, and CI passed at the first run.

### The early conflict check

`gh pr list --state open`: **#145 is the only open pull request**; there is no other head to check with
`git merge-tree`.

### Departures from the prompt

- **The commits:** the prompt's plan named five; the build made four (each unit's API, web, tests and documents
  together, workflow §3), then the carried fixes and the card's marks made six.
- **The title** is a commit subject, as workflow §3 asks, chosen as the one naming both halves of the task.
- **No local run for the text change** — the owner's word (above).
- **`apps/api/.env`** still points at `masaha_we_dev` / `masaha_we_test` (restore with
  `cp apps/api/.env.bak-we apps/api/.env`); the local `backup/women-evening-*` branches are kept for the owner to
  delete.

Stopped here: no merge, no Issue.

## Fix round (#145's review, 2026-11-14)

The supervisor's message (relayed by the owner): `9_FIX_ROUND.md`, after `7_REVIEW.md` (read whole). The owner's word:
fix F1, F3, F4, F5 and N1 before the merge; F2 → finding 227 and a rollback step in the PR; run only the tests the
round touches.

### The pull request and its head

- **#145**, **head `6c9a5e01dd14e22a2f7e0f90c938dec175f3ca5a`** (on `main` `88c5eb3f`, unmoved), pushed with
  `--force-with-lease` over `8f511d5a`.
- **CI on that head: green**, run 43587390161 (`headSha` = the head): all ten jobs pass, CodeRabbit skipped.
  GitHub: **`CLEAN`**, open.
- Backup: `backup/women-evening-pre-fix` at `8f511d5a`.

### The commits (6; each fix folded into the commit named, `--fixup` + `autosquash`, no fix commits)

| Commit | Subject | Folded in |
|---|---|---|
| `3b5d9e89` | fix(design-system): identity review follow-ups | F3 |
| `155cbaab` | feat(db): add the evening switch and women's hall | F1, F2 (finding 227) |
| `b9a277c1` | feat(spaces): the evening switch in the hours group | F5 |
| `0856c357` | feat(directory): filter the evening by the switch | N1 |
| `3496f77f` | feat(directory): the women's hall filter | F4 |
| `6c9a5e01` | feat(directory): the card's evening and hall marks | — |

The round's diff against `8f511d5a`: 10 files, +86 −12, nothing else.

### The fixes

- **F1** — `migration.sql`: `ADD COLUMN "works_evenings" …` without `IF NOT EXISTS`, and its comment line gone.
  `womenEveningMigration.api.test.ts` runs only the file's data steps (the `UPDATE` and the `INSERT`, exactly as
  written), its `ALTER TABLE` statement filtered out; its header says so and that the lane's `migrate deploy` proves
  the DDL. **The local databases:** `masaha_we_test` took the edited file without complaint (`migrate deploy` does not
  re-check an applied migration; the test passed); `masaha_we_dev` already applied the old text, so a `migrate dev`
  there would report the migration as modified — I ran none, and reset nothing. If it matters, it is the owner's call
  (CI's databases are fresh).
- **F2** — no code. **Finding 227** (the index's next number; row added): the web crashes on an icon key it does not
  know (`GlyphIcon` / `AmenityIcon`; only retired amenities go through `iconOf`), so a migration adding a key breaks the
  code before it, against setup's rule; a fallback like `iconOf`'s would make the next key safe. **The PR's migration
  section** gains the rollback step: before a Vercel rollback past #145, `UPDATE amenities SET icon = 'users' WHERE
  key = 'womens_hall';`, and `'venus'` again once the new code is back.
- **F3** — the three `not.toHaveClass('bg-secondary', 'hover:bg-hover')` split into two assertions each
  (AccountLayout, SpaceEditor's index, LocationStatus).
- **F4** — `favorites.api.test.ts`: «a favourite’s card says whether it has the women’s hall, found by its key (X12)»:
  `internet` first, so the hall's id is 2; the favourite with the hall reads `womensHall: true`, the one without `false`.
- **F5** — `HoursSheet.component.test.tsx`: «says «دوام مسائي» but no hint on the admin’s page of a verified space,
  which it cannot edit (X5)» — no «Edit Opening hours», «Evening hours» shown, nothing matching `/past 18:00/`.
- **N1** — `SpaceDetails.component.test.tsx`: «says «Evening hours» in the hours in English, with no detectable
  accessibility violations» — axe on the hours section.

### What was run, and what was not

- **The owner's word for this round:** only the test files the round touched, each alone, through the grant script —
  `womenEveningMigration.api.test.ts` 4 passed, `favorites.api.test.ts` 5, `AccountLayout.component.test.tsx` 4,
  `SpaceEditor.component.test.tsx` 31, `LocationStatus.component.test.tsx` 5, `HoursSheet.component.test.tsx` 27,
  `SpaceDetails.component.test.tsx` 22. All green; none was stopped for memory.
- **NOT run locally:** the full lanes, `lint`, `typecheck`, `check:*` — the owner's word; CI on the head ran them all,
  green. Prettier was applied to the touched files. Said in the PR's *Evidence*.

### The breaks made (each made once, seen failing, restored from a `cp` backup and checked with `cmp`)

| Test | Break | Result |
|---|---|---|
| F3, all three | `variant="ghost"` on the current entry (AccountLayout, SectionIndex), `variant="outline"` on the pressed NearMeButton | each fails at `not.toHaveClass('hover:bg-hover')` |
| F4 | the favourites' `womensHallId` dropped from their `publicListing.page` call | fails |
| F5 | `host.editable &&` dropped from the view's hint | fails |
| N1 | the page's `evening` line set to `null` | fails |

F1's test is unchanged in what it asserts (only which statements it runs); it passes on the edited file.

### Problems, and anything unexpected

None. The fixups applied and squashed cleanly; CI passed at the first run.

### The early conflict check

`gh pr list --state open`: #145 alone; nothing to check with `git merge-tree`.

### Departures from the prompt

N1's break was not named in the message; I made one anyway (the page's line never set), as "each new or changed
assertion" asks.

Stopped here: no merge, no Issue.
