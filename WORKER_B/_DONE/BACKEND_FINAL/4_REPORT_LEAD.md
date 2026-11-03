# BACKEND_FINAL — the lead's run (finance, the overviews, the API items left — one PR) — the report

> Written as the run goes (3_EXEC_PROMPT_LEAD.md §9). Worker B's lead, in `C:\dev\masaha\app-b`; API on 3321,
> `masaha_b_dev` / `masaha_b_test`.

**Status: READY FOR REVIEW** — PR #131, head `c41a5397`, CI green on every lane, `CLEAN`. SERIOUS decisions: none.
Left out of the PR: nothing.

## Start (2026-10-29)

- `git fetch origin`: `origin/main` = `d40d20f5` (Merge #129). `git diff --name-status e3b2f97b origin/main -- apps/api
  packages` empty (EC1: no API or shared file changed since the plan's base).
- `app-b` was detached at `e3b2f97b`, clean; `git switch --no-track -c feat/backend-final origin/main`.
- `npx prisma migrate status` on `masaha_b_dev` and `masaha_b_test`: 29 migrations, "Database schema is up to date!" both.
- `npm run build -w @masaha/shared`: 0. Docker `masaha-postgres-1` up (healthy). Free memory at start: 7,900,372 KB.

## Lane 0 — the foundation (by the lead)

### C1 — `23f50a4f test(platform-settings): pin a stored contact form` (49)
- T-L1 `publicContact.api.test.ts` › "a contact stored in another form is answered as stored, to anyone and to the
  admin"; T-L2 `adminSettings.api.test.ts` › "saving a contact stored in another form stores its one form, audited from
  the stored to the saved". They pin built behaviour (no code change), so no red before code: each is proven by its break.
  Green: `platform-settings/` "Test Files 2 passed (2) · Tests 15 passed (15)".
- **B-L1** (`settingKeys.ts` the contact's WhatsApp read through `phoneSchema`): red — "× a contact stored in another form
  is answered as stored…" (and the 500 test: "expected 200 to be 500"); restored by copy.
- **B-L2** (the save compares on normalised forms): red — "× saving a contact stored in another form…: expected {
  email: 'Hello@Masaha.PS', …} to deeply equal { email: 'hello@masaha.ps', …}" (and two other tests); restored.
- Documents: contract *Platform settings* — F1's sentence on the contact bullet; F4 "a save that changes no value
  writes no value and no entry (an unset contact's first save may still insert its rows, `null`…)";
  `platform-settings.md` F3 ("in the browser too" dropped), F4 (twice).

### C2 — `5656a9eb fix(seed): store the contact in its one form` (43)
- **LEAD-D1 (EC7 failed):** `seed.api.test.ts` tests `seed()`, not `run.ts`'s environment check, and `run.ts` seeds on
  import, so it cannot be imported by a test. Options: (a) a unit test of the environment schema moved to its own file;
  (b) a test spawning `run.ts` (it would write to a database). Chose (a), as EC7's fallback says, but in a new file
  `apps/api/src/db/seed/seedEnv.ts` (not inside `run.ts`, which runs on import), with `seedEnv.unit.test.ts`. Undo: the
  schema back into `run.ts`, the unit test dropped.
- The schema moved first unchanged (no behaviour change), then T-L3's three tests: red — "× stores the contact
  normalised…: ZodError" and "× a foreign WhatsApp fails the seed, naming its variable: expected true to be false";
  green after `emailSchema` / `phoneSchema`: "Tests 3 passed (3)".
- **B-L3** (`run`'s WhatsApp back to the E.164 regex): red — "expected '+972591234567' to be '+970591234567'" and the
  foreign case; restored.
- The development `.env`'s `SEED_CONTACT_WHATSAPP` passes `phoneSchema` and changes form (checked without printing it):
  `masaha_b_dev` likely holds the `+972` form — R11 shows it answered as stored.
- Finding 153: F2's wording ("a change of form the admin did not ask for") and the foreign-number case; *Resolved*,
  its *Resolution* line; the index moved.

### C3 — `a2f0d8ed docs: resolve finding 97` (24)
- 97 *Resolved* (`newSpaceDefaultsSchema` in `@masaha/shared/space-settings`, built from `VISIT_ROUNDINGS`,
  `ROUNDING_MINUTES`, `roundingPair` — verified in `packages/shared/src/space-settings/requests.ts:54–66`), naming #130.

## The lanes

- **LEAD-D2 — three lanes (F, O, L), as the plan's §8.4.** O does not split cleanly (C10–C11 need C9's shared
  `overview` folder and its `app.ts` block); L's four items could split, but every extra lane adds a full `test:api`
  (≈ 10 min, ≥ 4 GB) to a two-at-once budget, so a fourth lane would wait rather than gain. Undo: none needed.
- **LEAD-D3 — the data-reports helper written identically by two lanes.** D35 says one helper `handledByWhere` serves
  both lane L's `handledBy` filter (C14) and lane O's `openCounts` (C10); the lanes run in parallel. The lead fixed its
  exact text and place in both lanes' briefs, so the join meets two identical insertions. Undo: one lane writes it,
  the other adapts at the join.
- Finding numbers: the lead 154–155, L 156, F 157, O 158–159 (154–159 free; 160+ taken or worker A's).
- Lane prompts: `scripts\lanes\LANE_COMMON.md`, `LANE_L.md`, `LANE_F.md`, `LANE_O.md`. Grant script
  `scripts\heavy.mjs` (worker A's, copied; its log `scripts\heavy-grants.log`); break helper `scripts\break.py`.

### Lane L
- Worktree `C:\dev\masaha\app-b-lane-l`, branch `lane/l` at `a2f0d8ed`; `.env` copied (only `TEST_DATABASE_URL`
  changed, to `masaha_b_lane_l_test`); `npm ci` 0; shared build 0; database `masaha_b_lane_l_test` created and migrated
  ("All migrations have been successfully applied"). Launched after C3.

### C4 — `b0cd0ae4 feat(payments): total a space's balances` (40)
- `payments.repository.ts`: `uncollectedOf(spaceId)` — the uncollected list's `FROM`, one function `uncollectedPage`
  and `uncollectedTotals` both read (R2); `balancesPage` (one statement: `balancesOf` unchanged (EC3), per customer
  `DEBT`/`CREDIT` `HAVING > 0`, `ORDER BY amount DESC, customer_id`, `count(*) OVER ()`, the oldest owing item by
  `DISTINCT ON`, a count apart only past the last page), `balanceTotals`, `uncollectedTotals`, each `tx` optional;
  the service's three (`at` → `calendarOf`); `index.ts` exports the row types.
- T-P1–T-P3 in `payments/totals.api.test.ts` (5 tests): red — "TypeError: repository.balancesPage is not a function"
  (×5, "Tests 5 failed (5)"); green "Tests 5 passed (5)".
- **B-P1** (ordered by customer id): red — "expected [ { customerId: 1, … } ] to deeply equal [ { customerId: 2, … } ]"
  (2 tests); **B-P2** (`sum(due − paid)` netted): red — "expected { owed: { agorot: 4700 … } } to deeply equal { owed:
  { agorot: 5700 … } }"; **B-P3** (`written_off_at IS NULL` dropped): red — "expected { visits: 4, owedAgorot: 7500 }
  to deeply equal { visits: 3, owedAgorot: 4500 }". Each restored by copy.
- Light runs: `payments/` "Test Files 4 passed · Tests 25 passed"; with desk's `debt`, `payments`, `writeOff`:
  "Test Files 7 passed (7) · Tests 64 passed (64)". Grants: lint exit 0 (174 s), typecheck exit 0 (60 s).
- Documents: `payments.md` (*What it does*, *Who uses it*, two *Behaviour* paragraphs, a decision, history `#PRNUM`);
  conventions §9 *Composed reads* — "`overview` (how many owe, a count — never an amount, the owner's O3)" (R11) and
  the aggregates' bullet. `check:links` "3026 links … all resolve". Finance's and the overview's documents are not
  linked from C4 (they do not exist yet); lane F links `finance.md`.

### Lanes F and O
- Worktrees `C:\dev\masaha\app-b-lane-f` (`lane/f`) and `C:\dev\masaha\app-b-lane-o` (`lane/o`) at `b0cd0ae4`; `.env`
  copied (only `TEST_DATABASE_URL` changed, to `masaha_b_lane_f_test` / `masaha_b_lane_o_test`); `npm ci` one at a time
  (0, 0); shared build 0 ×2; each database created and migrated. Launched after C4's lint, typecheck and tests.
- **LEAD-D4 — EC4 (the cost on a generated year) run once by the lead after the joins**, not per lane: one data set,
  every statement measured on the joined code, and no lane spends its memory on a 300-space year. Undo: each lane
  measures its own statements.
- **LEAD-D5 — T-O2's debtors' comparison** against the payments service's `balanceTotals` in lane O (the finance route
  is lane F's); the lead folds the `…/finance/debts` comparison into C9 after the join. Undo: none needed.

### Lane L — DONE (its report saved as `scripts\lane-l\REPORT.md`)
- `lane/l` head `9facce4f` on `a2f0d8ed`: C12 `fix(sessions): read a family's latest activity` (47), C13
  `feat(users): read and edit one's own account` (44), C14 `feat(data-reports): filter by who handles them` (46), C15
  `feat(visits): list a space's visits by day` (42). Every test red before its code (404 / 401 / wrong rows), every break
  B-L5–B-L12 red and restored. Its grants: lint 0, typecheck 0, test:unit (shared 268, api 884, web 1075 tests),
  **test:api 101 files / 1272 tests passed** on `masaha_b_lane_l_test`; no kill.
- Its decisions (recorded by the lane; the lead keeps them): rotate reads the family's max too (C12); an empty
  `PATCH /me` answers 200 writing nothing, as every partial PATCH (C13); a suspended account 401 (the guard's), not 403
  as T-L8 said (C13); `handledByWhere` joined by `AND: [...]` so `spaceId` is kept — a defect its test caught (C14);
  `REPORT_HANDLERS` exported; 167 and 161 *Resolved* with "the screen is the web's"; a visits range granted by
  `can('payments.read')` (no visits action; `can.ts` not the lane's); EC13 failed in part — `visits` (L3) cannot import
  `payments`' window (L4), so a local `daysWindow` with the same Gaza-midnight rule and `VISITS_RANGE_MAX_DAYS = 92`.
  None SERIOUS (each keeps the plan's intent; the access rule equals the payments list's).
- **Join:** `backup/backend-final-lane-l-pre-join` at `9facce4f`; `git rebase --onto b0cd0ae4 a2f0d8ed lane/l` — clean:
  `f86aa488`, `713dcce2`, `55018275`, `7a318bd8`. `backup/backend-final-pre-join-l` at `b0cd0ae4`; `git merge --ff-only
  lane/l`. On it: idle, users, data-reports, visits, payments API "Test Files 18 passed · Tests 145 passed"; sessions,
  audit unit "Tests 12 passed"; typecheck 0, lint 0 (grants). Worktree `app-b-lane-l` removed.
- For C16 (from the lane): v1-mvp `/me` and `…/visits` built; conventions §6's audited list gains
  `user.profileEdited`.

### Lane F — DONE (`scripts\lane-f\REPORT.md`)
- `lane/f` head `4bfd1054` on `b0cd0ae4`: C5 `feat(finance): read a space's income` (36), C6 `feat(finance): read who
  owes and who paid` (41), C7 `feat(finance): read a space's occupancy` (39). Unit tests red before code; the API tests'
  red taken with the route unmounted (the lane wrote the service before its API test files — said, not hidden); every
  break B-F1–B-F21 red and restored; B-P1/B-P3 first green on the debts file → cases added → red. Grants: lint 0,
  typecheck 0, test:unit all passed, **test:api 105 files / 1284 tests** on `masaha_b_lane_f_test`; no kill.
- Its decisions kept: all time `-infinity`..`infinity`; `contactsOf`'s `archived` narrowed out of `deskCheckIns`' answer
  (R4 was wrong: the other caller passed the object through — the check-in test caught it); `.extend` for `.merge`;
  `out_of_range` through `AppError.validation`; occupancy reads in parallel; `finance.md` written whole in C7. None
  SERIOUS.
- **Join:** `backup/backend-final-lane-f-pre-join` at `4bfd1054`; `git rebase --onto 7a318bd8 b0cd0ae4 lane/f` — clean:
  `8cd2bcfa`, `f7cd3a13`, `2d8c0b86`; `backup/backend-final-pre-join-f` at `7a318bd8`; `--ff-only`. On it: finance,
  payments, customers, subscriptions, desk API "Test Files 29 passed · Tests 234 passed"; finance unit 9, shared core +
  finance unit 85 passed; typecheck 0, lint 0 (grants). Worktree removed.

### Lane O — DONE (`scripts\lane-o\REPORT.md`)
- `lane/o` head `32fcd35f` on `b0cd0ae4`: C8 (48), C9 (41), C10 (48), C11 (41) — subjects as §8.1. Every test red
  before its code; every break red and restored. Grants: lint 0, typecheck 0, test:unit all passed, **test:api 107 files
  / 1292 tests** on `masaha_b_lane_o_test` (853 s); no kill.
- Its decisions kept (none SERIOUS): OD3's `editable` lives in a second shared schema for the API
  (`adminSpacesListQuerySchema`), because widening the web's status list breaks its typecheck and `apps/web` is out of
  scope — **finding 158** recorded (Open) for worker A's screen 25; `endingSoon` counted through `customers.page` (EC8:
  the list leaves archived customers out); EC9 failed — `hasPhotos` dropped (the plan's fallback); `glance(space, at?)`.
- **Join:** `backup/backend-final-lane-o-pre-join` at `32fcd35f`; `git rebase --onto 2d8c0b86 b0cd0ae4 lane/o`. C8 clean.
  Conflicts, each kept both sides (`scripts\join_o.py`, `join_o_c10.py`): C9 — `app.ts` (F's finance mount, then O's
  overview controller and mount), conventions §7 (F's `finance` row, O's `overview` row), `security.md` (F's bullet, then
  O's); C10 — `gazaTime.ts` (F's `monthOf`/`addMonths`, then O's `lastDaysSince`), its unit test (the imports' union;
  F's describe, then O's), `data-reports.repository.ts` (O's `openCounts`, then L's rewritten `pageAll` doc).
  `handledByWhere` once (the two identical insertions merged, LEAD-D3). C11 clean.
- **LEAD-D6 — the T-O2 fold, and a fixture gap it showed.** The marker replaced by `GET …/finance/debts`'
  `meta.totals.owed.customers` = `customersOwing`; it answered **500**: "The space 1 has no settings row" (the test's
  factory space has none; every space created through the API has one — not a product defect, the finance tests give
  theirs one). The test's `beforeEach` gives the space its settings row, as `debts.api.test.ts` does; the in-test
  payments service and its imports dropped. Green "Tests 6 passed (6)". Folded into C9 (`backup/backend-final-lane-o-pre-fold`;
  `--fixup` + autosquash on `2d8c0b86`; no `fixup!` left): `51f35f90`, `b1ac98a4`, `798f4708`, `d7e626d3`.
- On the joined branch (`backup/backend-final-pre-join-o` at `2d8c0b86`, `--ff-only`): overview, spaces, space-links,
  data-reports, visits, subscriptions, announcements, occupancy, users, finance API "Test Files 54 passed · Tests 611
  passed"; api unit "Tests 807 passed"; shared unit "Tests 271 passed"; typecheck 0, lint 0 (grants). Worktree removed.

## EC4 — the cost on a generated year (on the joined branch `d7e626d3`, `masaha_b_test` only)
- `scripts\year.sql` (after `ec4-truncate.sql`): 300 spaces (150 with an owner, every 17th hidden), 5 000 users, 11
  busy spaces each with 2 000 customers, 500 subscriptions, 9 000 visits (1 % auto-closed, 2 % written off), 3 000
  check-ins, ≈ 9 700 payments (5 % voided) over 365 days — in all 22 000 customers, 99 000 visits, 33 000 check-ins,
  107 120 payments; settings rows added for the reads. `ANALYZE`d.
- Method: `log_min_duration_statement = 0` set on `masaha_b_test` only; the API run against it on 3321
  (`DATABASE_URL` overridden; signed in as a generated owner and admin with a throwaway password, no `/auth/` body
  kept); each new route called once to warm, then once measured (`scripts\ec4-calls.mjs`); the measured pass's
  durations read from the container's log (`scripts\ec4-durations.log`).
- Route wall times (measured pass): income 89 ms, debts 190 ms, debts `CREDIT` 156 ms, payers 118 ms, occupancy 138 ms,
  the owner's overview 103 ms, the visits list 40 ms, the admin's overview 63 ms (with `users.created_at`, no index),
  the admin's reports `handledBy` 30 ms.
- **Statements:** 171 in the measured pass; **none over 150 ms**; the slowest 49.0 ms. No index proposed (Q5). EC10
  (`users.created_at` unindexed, 5 000 users) within that.
- Cleanup: server stopped by its process id (port 3321 free), the setting reset, the tables truncated.

## C16 — `70a4b021 docs: record the API of v1 as built` (35)
- `v1-mvp.md`: step 11 *Settles* says the server aggregates and the web builds the CSV (no export route); step 11
  *Built* finance; step 12 *Built* both overviews; *Me*, *Managed spaces* and *Admin* `Built:` lines; the `/me` and
  `…/visits` rows built; the finance row's four reads and "no export route"; a `GET …/overview` row; `/admin/stats` →
  `GET /admin/overview` (OD4). `docs/project/overview.md` *Built*: Finance, Overview. `docs/README.md` map:
  `finance.md`, `overview.md`. Conventions: the header's *Built* (finance, overview, Gaza's months and last days); §6's
  audited list names `user.profileEdited` (lane L's note). Findings index checked against every file's status
  (scripted): no mismatch. Subjects recounted: all ≤ 50 (C1 is 50, not the plan's 49).

## The final verification (on `70a4b021`, 16 commits)
- `npm run build -w @masaha/shared` 0 · `npm run lint` 0 · `npm run typecheck` 0 · `npm run test:unit` — shared "27
  passed · 271 passed", api "75 · 902", web "157 · 1075" · **`npm run test:api` (on `masaha_b_test`) "Test Files 114
  passed (114) · Tests 1319 passed (1319)"** · `npm run test:component` "Test Files 1 failed | 299 passed (300) · Tests 2
  failed | 1742 passed (1744)": site `routes.component.test.tsx` › "shows the Directory under its title" (3022 ms) and
  "shows a space's page…" (5118 ms) — finding 87's family (3 s waits, while `test:api` ran beside it); alone while
  `test:api` still ran: 1 failed (3020 ms); **alone with the machine quiet: "Tests 13 passed (13)"**. The PR changes no
  `apps/web` file (`git diff --stat origin/main -- apps/web` empty). CI judges.
- Production build: a first try through the grant failed at once ("'NODE_ENV' is not recognized" — `cmd` takes no
  prefix); re-run with `NODE_ENV=production` in the environment: exit 0; `npm run check:build` 0 ("No showcase code in
  73 build files…", "No dashboard code in the site's first download.", "No data-table or leaflet or calendar…").
- `check:classes` 0 (1659 files) · `check:links` 0 (3112 links, 209 documents) · `check:conflicts` 0 · `format:check` 0
  · `git grep -l '#PRNUM'`: 22 files, all under `docs/`.
- Grants: two slots at most (test:api with lint/typecheck/unit, then test:component). The final `test:api` and `lint`
  each **waited four 2-minute tries** (11:53–11:59 UTC, free memory 3.50–4.01 GB < 4 GB) before their grants; no kill.

## The real run (2026-10-29, `masaha_b_dev`, API on 3321; `scripts\realrun.mjs`, output `scripts\realrun.txt`)
- `npm run dev -w @masaha/api` (log `scripts\server.log`, deleted after); `/health` → `db: up`. Signed in as the demo
  owner, the demo reception, the demo directory owner and the seed's admin (passwords read from `.env`, never printed;
  no `/auth/` body kept).
- A first try stopped at R2 on the script's own SQL (an alias missing in the debtors' query, before any write); fixed,
  re-run whole: **ALL PASS**, 56 cases:
  - R1 the four finance reads 200; R2 the month's income 46 000 = SQL 46 000; debtors 3 = SQL 3 (archived included,
    R10 of the plan; the demo data has no archived debtor — T-F7/T-P2 prove it); the 14 days' closed visits by Gaza day
    equal (4 visits); R3 reception 403 on the four (with an invalid `month`: refused before the query is read); R4 the
    admin and the directory owner 404 on the four.
  - R5 the owner's overview 200, no `agorot` anywhere; uncollected 3, unpriced 0, open reports 0, running
    announcements 0, ending soon 2 — each equal to its list's total; customers owing 3 = debts' 3. (The demo space has
    no open report, no running announcement, no archived customer — EC15: those equalities hold at 0; their tests prove
    the non-zero cases.) R6 reception 403; R7 the admin and the directory owner 404.
  - R8 the admin's overview 200: verified 14, unverified 11, hidden 0, stale or missing 3, completeness 1
    (`?status=editable&stale=true`), open reports 1 (awaiting the admin 0, the owners 1, each = `?handledBy=`), new
    users 4 = SQL 4; nothing of a space's operations. R9 the owner and reception 403.
  - R10 the thresholds read (60/30); `PUT` 1/1 → the owner's stale and missing groups 0 → 5, the admin's 3 → 25; `PUT`
    60/30 back; the owner's overview as before. R11 the public contact answered as stored (compared, not printed).
  - R12 `GET /me` 200; `PATCH` language ar → en → ar. R13 the owner's visits 2026-10-23..29 (3) 200; reception with a
    range 403; reception today 200.
  - R14 (the seed, 153) and R15 (finding 170's race): **not performed**, as the plan says — re-seeding is outside the
    run; a race is not a real-run case; T-L3 and T-L5 prove them.
- **Writes, all named and put back:** audit entries 63–64 `platformSettings.stalenessEdited` (60/30 → 1/1, 1/1 →
  60/30); 65–66 `user.profileEdited` (ar → en, en → ar). The thresholds read 60/30 again; the demo owner's language
  `ar`. **Data left:** those four audit entries (the log is append-only).
- The API stopped by its process ids (8264, 10020, 14064: `tsx watch`, the server, `pino-pretty`); port 3321 free;
  `git status --short` clean.

## Push, the PR, CI
- The number: `gh api …issues?state=all&per_page=1` → 130, so **#131**; `scripts\prnum.sh 131` (the model's, adapted):
  `backup/backend-final-pre-prnum` at `70a4b021`; `#PRNUM` → `#131` in every commit's tree — "PRNUM OK #131 c41a5397";
  the rewrite changed only the number (22 files, 88/88 lines); the description's placeholder none.
- `git push -u origin feat/backend-final`; `gh pr create --assignee @me --label feat --label area:api --label
  area:docs` → **https://github.com/Basel-Ghonaim/masaha/pull/131**, title `feat(api): finance, the overviews and the
  rest` (46). The number matched: no rewrite after.
- 130 files changed.
- **CI on `c41a5397`** (`gh pr checks 131 --watch`): build pass (30 s), check:classes, check:conflicts, check:links,
  format:check pass, lint pass (1 m 20 s), typecheck pass (41 s), test:unit pass (1 m 6 s), **test:api pass (7 m 30 s)**,
  **test:component pass (7 m 6 s)**; CodeRabbit skipping. `mergeStateStatus` **CLEAN**.

## The commits (final, on the PR)
- `23f50a4f` test(platform-settings): pin a stored contact form (50)
- `62d76b81` fix(seed): store the contact in its one form (44)
- `66c7b80a` docs: resolve finding 97 (24)
- `5f867d86` feat(payments): total a space's balances (40)
- `061f7f16` fix(sessions): read a family's latest activity (46)
- `cd27ab2b` feat(users): read and edit one's own account (44)
- `40ef7b9e` feat(data-reports): filter by who handles them (46)
- `6d563549` feat(visits): list a space's visits by day (42)
- `a05891e4` feat(finance): read a space's income (36)
- `71a18c1b` feat(finance): read who owes and who paid (41)
- `53c6a7e3` feat(finance): read a space's occupancy (39)
- `447be920` feat(api): count what the owner's overview shows (48)
- `a12f928e` feat(overview): read the owner's overview (41)
- `57fa7992` feat(api): count what the admin's overview shows (48)
- `74379567` feat(overview): read the admin's overview (41)
- `c41a5397` docs: record the API of v1 as built (35)

## Memory and the grants (`scripts\heavy-grants.log`, UTC)
- 32 grants: the lead 15, lane O 9, lane L 4, lane F 4; two slots at most at once (the lanes' full `test:api` runs
  overlapped two at a time, never started in the same minute); the lowest free memory at a grant 4,653,544 KB.
- 8 waits, all the lead's (the final `test:api` and `lint`, 11:53–11:59, 3.50–4.01 GB free, after EC4's server).
- **No kill**, no exit 75, no give-up.

## Test databases
- Made: `masaha_b_lane_l_test`, `masaha_b_lane_f_test`, `masaha_b_lane_o_test` (each migrated). **Dropped** after the
  PR was opened (`DROP DATABASE`, three). `masaha_b_test` (the lead's): EC4's year generated and truncated; the final
  `test:api` ran on it.

## What `_SHARED\OPEN_DECISIONS.md` must say (for the supervisor; the plan's §11.3)
- Point 3: "the owner's debts with their phones are read on `GET …/finance/debts` (#131, 2026-10-29), the CSV built in
  the browser; no export route."
- Point 1: "«يحتاج انتباهك» counts the uncollected and the unpriced visits on `GET …/overview` (#131)."
- Point 2: "the owner's overview reads `closuresAwaitingExtension` (#131)."
- Point 4: "each staff member's collections are on `GET …/finance/income` (#131)."

## Decisions taken without the owner (none SERIOUS)
1. **LEAD-D1** (EC7 failed) — the seed's environment schema in `seedEnv.ts` with a unit test. Undo: back into `run.ts`.
2. **LEAD-D2** — three lanes, not more (each lane adds a full `test:api` to a two-slot budget). Undo: none needed.
3. **LEAD-D3** — the data-reports helper's exact text given to two lanes; merged as one. Undo: none needed.
4. **LEAD-D4** — EC4 run once by the lead on the joined code. Undo: per-lane measurements.
5. **LEAD-D5** — T-O2 compared with the payments service in lane O; the lead folded the finance route in.
6. **LEAD-D6** — the T-O2 fold's 500 traced to the test's space lacking its settings row (a fixture gap, not a product
   defect); the test gives it one, as the finance tests do. Undo: none needed.
7. Lane L: the rotation reads the family's latest activity too (170); `PATCH /me {}` 200 writing nothing; a suspended
   account 401 (the guard's); `AND: [handledByWhere(…)]` (a spread lost `spaceId`); `REPORT_HANDLERS` exported; 167 and
   161 resolved with "the screen is the web's"; the visits range by `can('payments.read')`; EC13 in part — a local
   `daysWindow` (levels forbid `payments`' window), 92 days.
8. Lane F: all time `-infinity`..`infinity`; `contactsOf`'s `archived` narrowed out of `deskCheckIns` (R4 was wrong);
   `.extend`; `out_of_range` via `AppError.validation`; occupancy reads in parallel; `finance.md` written whole in C7.
   Its API tests' red was taken with the routes unmounted (the service was written before its API test files).
9. Lane O: OD3's `editable` in a second API schema, **finding 158**; `endingSoon` through `customers.page` (EC8); EC9
   failed — `hasPhotos` dropped; `glance(space, at?)`; `ListedSpace.stale`; three parallel counts; T-O3
   case-insensitive.
10. The C1 subject is 50 characters, not the plan's 49 (recounted; within the limit).

## Leftovers
- Branches (local): `backup/backend-final-lane-l-pre-join`, `-lane-f-pre-join`, `-lane-o-pre-join`, `-lane-o-pre-fold`,
  `-pre-join-l`, `-pre-join-f`, `-pre-join-o`, `-pre-prnum`. Lane branches `lane/l`, `lane/f`, `lane/o` deleted; their
  worktrees `app-b-lane-{l,f,o}` removed.
- Databases: the three lane databases dropped. `masaha_b_dev`: the real run's four audit entries (63–66).
- Scripts and outputs: `scripts\` (lanes' prompts and reports, breaks and backups, EC4, the real run, `pr-body.md`).
- Design notes for worker A (from the lanes): no «بدون صور» on the completeness card (EC9); finding 158 for screen 25's
  `editable` filter.

## The reviews' fix round (2026-10-29)

Executor: the fix-round prompt `7_FIX_ROUND.md`; the three reviews `6_REVIEW_R{1,2,3}_CLAUDE_CODE.md` (no blocker).
Scripts and outputs: `scripts\fix-round\`.

### The base
- `git fetch origin`; local `feat/backend-final` at `c41a5397` = `origin`; `mergeStateStatus` **CLEAN** → **no rebase**.
- `backup/backend-final-pre-review-fix` at `c41a5397`. `npm run build -w @masaha/shared` ok.

### The fixes (each folded; `--fixup` + `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash origin/main`, three rounds)
- **R2-F1** — contract *Finance* › *Who owes*, `DebtsMeta`'s comment, finding **193** and its index line → `fc960282`
  (was `71a18c1b`); the new test in `debts.api.test.ts` ("an auto-closed visit left to a customer is in that
  customer's debt and in the uncollected count too…") → the same. It pins existing behaviour, so it was **green first**
  (6/6); **its red is a break**: `uncollectedOf` given `AND v.customer_id IS NULL` (backup
  `bak-FR-R2F1-payments.repository.ts`, output `break-FR-R2F1.txt`): "Tests 1 failed | 5 passed (6)", `uncollected`
  `owedAgorot` 0 ≠ 4000, `visits` 0 ≠ 1; restored from the backup copy; green again (6/6). `finance.md:10` → `3a4ba5e8`
  (was `53c6a7e3`, the line's last writer). The overview's consequence (`overview.md` and finding 193's second
  paragraph) → `d9730e58` (was `a12f928e`).
- **R2-F2** — `finance.md` "45" → "46" windows → `3a4ba5e8` (the line's last writer, as the reviewer allowed).
- **R2-F3** — `todayWindow` removed from `windows.ts`; its unit case asserts `dayWindow('2026-10-29')` → `84c2a5dc`
  (was `a05891e4`). No new behaviour: the assertion moved (6/6 green).
- **R3-F1** — `announcements.md`: one query on the `RUNNING` condition, each type kept once by Prisma's `distinct` in
  memory → `bea15c5b` (was `447be920`). Code unchanged.
- **R3-F2** — conventions §9 *Composed reads*: "reads `closures.summary` (2026-10-29, #131)" → `d9730e58`.
- **R3-F3** — `glance(space, at: Date)`, no default; `glance.api.test.ts` passes `NOW` → `bea15c5b`. Green (with debts:
  2 files, 7 tests).
- **R1-F1** — `terms`'s JSDoc back on `terms` → `f565fcaa` (was `6d563549`).
- **R1-F2** — `payments.md`: the desk's web sentences back on the front desk bullet → `113c87e3` (was `5f867d86`),
  carried through `84c2a5dc` and `fc960282`, which each rewrote the adjacent Finance bullet (three conflicts, resolved by
  `scripts\fix-round\payments_move.py`: each commit keeps its own Finance wording, minus the two sentences; checked with
  a word diff against the backup: only the two sentences moved). "will count" → "counts" → `d9730e58`.
- **R1-F3** — `.env.example`: a Palestinian or Israeli number, any typed form the phone rule reads, stored in its one
  E.164 form → `5a9a594a` (was `62d76b81`).
- Contract conflicts in round one (the *Occupancy statistics* bullet of `53c6a7e3` sits next to *Who owes*): resolved by
  `resolve_contract.py`, keeping both bullets, the fixed *Who owes*.
- After each round: every subject unchanged (diffed against the backup), no `fixup!`; `git range-diff` shows only the
  intended commits changed (`74379567` → `0e528c5a` context only); the final tree differs from the backup by the fixes
  alone (15 files, +56/−24 before R1-F2).

### The runs
- While fixing: `debts.api.test.ts` green 6/6, the break red, green again; `windows.unit.test.ts` 6/6; `debts` +
  `glance` 7/7; `lint` 0, `typecheck` 0, `check:links` "3116 → 3118 links … all resolve"; Prettier on touched code.
- Final head `ecda64c7`, free memory 5,296,216 KB before `test:api`, 5,296,912 KB before `test:unit` (≥ 4 GB):
  `lint` exit 0; `typecheck` exit 0; `test:unit` 27/271 + 75/902 + 157/1075 passed; **`test:api` 114 files, 1320 tests
  passed**; `format:check` "All matched files use Prettier code style!"; `check:links` "3118 links in 210 documents and
  2332 source files all resolve."; `check:conflicts` "No conflict markers found."
- No real run (documents, a test and two dead defaults; behaviour unchanged).

### Push and CI
- `git grep '#PRNUM'` → nothing. `git push --force-with-lease=feat/backend-final:c41a5397… origin feat/backend-final`
  → `c41a5397...ecda64c7 (forced update)`; not refused.
- CI on `ecda64c7`: build, check:classes, check:conflicts, check:links, format:check, lint (1 m 53 s), typecheck,
  test:unit (1 m 11 s), **test:api (6 m 37 s)**, **test:component (6 m 55 s)** all pass; CodeRabbit skipping.
  **CLEAN**; 132 files (130 + finding 193 + `.env.example`).
- `gh pr edit 131 --body-file scripts\fix-round\pr-body.md`: *Review fixes (2026-10-29)* added; finding 193 in
  *Findings*.

### The commits after the folds
- `23f50a4f` test(platform-settings): pin a stored contact form (50)
- `5a9a594a` fix(seed): store the contact in its one form (44)
- `6174433b` docs: resolve finding 97 (24)
- `113c87e3` feat(payments): total a space's balances (40)
- `2714af6f` fix(sessions): read a family's latest activity (46)
- `b8958212` feat(users): read and edit one's own account (44)
- `f304280d` feat(data-reports): filter by who handles them (46)
- `f565fcaa` feat(visits): list a space's visits by day (42)
- `84c2a5dc` feat(finance): read a space's income (36)
- `fc960282` feat(finance): read who owes and who paid (41)
- `3a4ba5e8` feat(finance): read a space's occupancy (39)
- `bea15c5b` feat(api): count what the owner's overview shows (48)
- `d9730e58` feat(overview): read the owner's overview (41)
- `6d92df4f` feat(api): count what the admin's overview shows (48)
- `0e528c5a` feat(overview): read the admin's overview (41)
- `ecda64c7` docs: record the API of v1 as built (35)

### Decisions taken on my own
- **FR-D1: `finance.md`'s two lines folded into the occupancy commit, not `71a18c1b`/`a05891e4`.** Met: the prompt names
  `71a18c1b` for R2-F1's documents, but `finance.md` was rewritten whole in `53c6a7e3`, the lines' last writer. Options:
  fold into the older commits (conflicts on a rewritten file, then lost by the rewrite) or into `53c6a7e3`. Chose
  `53c6a7e3` (now `3a4ba5e8`), as R2-F2's reviewer allowed. Undo: move the hunk with a fixup to the other commit.
- **FR-D2: the overview's consequence folded into the owner's-overview commit, not `71a18c1b`.** Met: at `71a18c1b` no
  overview exists, so saying it there would claim something not yet built. Chose: finding 193 born in `fc960282` with
  finance only; its overview paragraph and `overview.md`'s sentence in `d9730e58`. Undo: fold both into `fc960282`.
- **FR-D3: R2-F3 by removal** (not using `todayWindow` in `income`): `income` needs today's date itself for
  `daysEnding`, so `todayWindow` would read Gaza's clock twice. Undo: restore the export and call it in `income`.
- **FR-D4: R1-F2's "counts" and R1-F3 folded into the commits that made the old lines false** (`a12f928e`,
  `62d76b81`): both lines were written on `main` before #131 (`e122b95d`; `.env.example` untouched by #131), so no
  commit of the PR wrote them. Undo: none needed; a fixup moves either.
- **FR-D5: R3-F1 by the document**, not by enabling `nativeDistinct` (a Prisma configuration change, out of scope, as
  the reviewer said).
- **FR-D6: lint and typecheck run once on the whole working tree before round one's fixups,** not before each of the
  seven; each round's tree was re-verified at the end (final runs). Undo: n/a.

### Leftovers
- Backup branch: `backup/backend-final-pre-review-fix` (at `c41a5397`), local only.
- `git status --short` clean; no rebase in progress.
