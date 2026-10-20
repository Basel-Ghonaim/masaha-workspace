# SETTINGS — the executor's report (PR 1)

> Executor: Claude Code, in `C:\dev\masaha\app-b`, 2026-10-19. Written as the work goes.

## 12.1 Before the branch

- `git fetch origin`; HEAD detached at `18ab1705` = `origin/main` (Merge #90); working tree clean.
- `gh pr list --state open` → `[]` (no open PR).
- `git diff --name-status 18ab1705 origin/main` → empty (main unchanged since the plan).
- Findings index on `origin/main`: last is 93 → **94 is free**.
- Branch: `git switch --no-track -c feat/space-settings origin/main` → `Switched to a new branch 'feat/space-settings'`.
- `docker start masaha-postgres-1` first failed: Docker Desktop was not running
  (`failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine`). Started Docker
  Desktop, then `docker start masaha-postgres-1` → `masaha-postgres-1 Up 8 seconds (healthy)`.
- `npm run build -w @masaha/shared` → `tsc -p tsconfig.build.json`, no error.
- `apps/api/.env` (names only, checked with `Select-String`): `PORT=3321`, `DATABASE_URL` → `masaha_b_dev`,
  `TEST_DATABASE_URL` → `masaha_b_test`.

## 12.2 First checks (1, 2)

1. **The migration**, created once: `npm exec -w @masaha/api -- prisma migrate dev --create-only --name reception_typed_prices`
   (exit 0), then the folder: `20261019092820_reception_typed_prices`. Prisma's SQL differed from D4's
   only in spacing (`ADD COLUMN     "reception_may_type_prices" BOOLEAN NOT NULL DEFAULT false`); replaced
   with D4's text (the two comment lines and the same statement). `npm run db:migrate` → `Applying migration
   20261019092820_reception_typed_prices … Your database is now in sync with your schema.` (exit 0). The
   generated client did not name the field after it (`grep -c` → 0), so `prisma generate` → `✔ Generated
   Prisma Client (7.10.0)`; then `SpaceSettings.ts` names `receptionMayTypePrices` (33 lines).
2. **The backfill** on `masaha_b_dev`: `SELECT count(*), count(*) FILTER (WHERE reception_may_type_prices)
   FROM space_settings` → `13 | 0`. ✔

Note: `prisma format --check` reports the schema unformatted — on `origin/main` too (checked on main's own
schema), so it is not a project check; the new line is aligned by hand, the rest untouched.

## Commits

### C1 `69851c7c` feat(space-settings): gate hand-typed prices (44)
- Red before the code: `npx vitest run --project api src/db/schema.api.test.ts -t "hand-typed"` →
  `Tests  1 failed | 24 skipped (25)`: the row had no `receptionMayTypePrices`.
- Green after: the whole file → `Tests  25 passed (25)` (exit 0).
- Documents: data model (*SpaceSettings* line, the *Hand-typed prices* bullet, *Visit charge*'s link), ADR
  0009 (a third *Revised* line, rule 5's row).
- `npm run lint` exit 0 · `npm run typecheck` exit 0.

### C2 `b4bf75c3` feat(space-settings): edit a space's settings (45)
- **U1–U3**, red against a stub schema (`z.object({}).partial()`): `npx vitest run src/space-settings/requests.unit.test.ts`
  → `Tests  3 failed (3)` (`expected null to deeply equal { maxStayMinutes: [ 'out_of_range' ] }`, …). Green
  after the schema: `Tests  3 passed (3)`.
- **First check 12.2.3 (Zod's refinement order):** probed with node on the source: `{maxStayMinutes: 90,
  visitRounding: 'UP_AFTER_MINUTES'}` → `{"maxStayMinutes":["out_of_range"],"visitRoundingMinutes":["required"]}`;
  `{maxStayMinutes: 90, visitRoundingMinutes: 15}` → `{…,"visitRounding":["required"]}`; with `PER_MINUTE, 15`
  → `{…,"visitRoundingMinutes":["invalid_format"]}`. Both codes appear, each on its own path; no crash. ✔
- **U7–U8**, red against a stub `settingsChange` (always empty): `Tests  1 failed | 1 passed (2)` — U7 red
  (`expected { data: {}, before: {}, after: {} } to deeply equal { data: { …(2) }, …(2) }`); U8 passes against
  the empty stub by its nature (it asserts emptiness). Green after: `Tests  2 passed (2)`.
- **T1–T9**, red before the routes existed: `npx vitest run --project api src/modules/space-settings/space-settings.api.test.ts`
  → `Tests  8 failed | 1 passed (9)` (`expected 404 to be 200`, `expected 404 to be 403`, `expected 404 to be 422`,
  T8/T9 `1 request(s) never waited on a lock`). T2 (the 404s) passes before the routes by its nature; B18
  proves it. Green after the module and `app.ts`: `Tests  9 passed (9)`.
- **First check 12.2.4:** `npm run lint` exit 0 with `space-settings` importing only `db`, `shared/*`,
  `@masaha/shared/{core,space-settings}`. ✔
- **First check 12.2.5:** the mapper returns `SpaceSettings` and the controller's `satisfies SpaceSettings`
  compiles against Prisma's `VisitRounding` (`npm run typecheck` exit 0), no cast. ✔
- Prettier reformatted two test files before the commit (`prettier --write`).
- `npm run check:links` → `2241 links in 137 documents and 1267 source files all resolve.`
- After the commit: `npm run lint` exit 0 · `npm run typecheck` exit 0.

### C3 `68ac15d1` feat(space-settings): add reminder placeholders (47)
- **U4–U5**, red against a stub (`placeholdersIn` answering `[]`, the template a bare paragraph):
  `Tests  2 failed (2)` (`expected [] to deeply equal [ '{الاسم}', '{المساحة}', '{المبلغ}' ]`, `expected null to
  deeply equal { Object (reminderTemplate) }`).
- **T6's template cases**, red: `-t "refuses a bound"` → `Tests  1 failed | 8 skipped (9)` (`expected 200 to be 422`).
- First green attempt: U5 failed — `''` answered `[too_short, invalid_format]`: Zod 4 runs the amount's
  refinement after the paragraph's `min` fails. Fixed in the rule, not the test: the amount's refinement
  skips an empty text (`text === '' || …`), so an empty reminder is only `too_short`, as U5 states. Then
  `npx vitest run src/space-settings` → `Tests  5 passed (5)`; the API file → `Tests  9 passed (9)`.
- `REMINDER_TEMPLATE_MAX_LENGTH` moved from `requests.ts` (C2) to `reminderTemplate.ts`, as D1b places it.
- After the commit: `npm run lint` exit 0 · `npm run typecheck` exit 0.

### C4 `337dcbcf` feat(occupancy): set a space's capacity (39)
- **U6**, red against a stub (`z.object({})`): `Tests  1 failed (1)` (`expected null to deeply equal { capacity:
  [ 'out_of_range' ] }`). Green after: `Tests  1 passed (1)`.
- **T11–T19**, red before the module: `Tests  8 failed | 1 passed (9)` (`expected 404 to be 200`, `… 403`,
  `… 422`, T18/T19 `1 request(s) never waited on a lock`); T12 (the 404s) passes before the routes by its
  nature — B27 proves it. Green after the module and `app.ts`: `Tests  9 passed (9)`.
- **First check 12.2.4:** `npm run lint` exit 0 with `occupancy` importing `spaces` and
  `@masaha/shared/{core,occupancy}`. ✔
- **First check 12.2.6:** the upsert is a top-level `upsert` (no nested relation write); the occupancy file
  run printed no `DeprecationWarning` (`grep -c` → 0). Kept as planned. ✔
- Two links in the new `occupancy.md` fixed before the commit (ADR 0008's file is `0008-live-status-not-counts.md`;
  `SpaceOccupancy` sits under the data model's *Spaces*). `npm run check:links` → `2275 links in 139 documents
  and 1279 source files all resolve.`
- After the commit: `npm run lint` exit 0 · `npm run typecheck` exit 0. 42 files changed against `origin/main`.

## 12.4 Verification on the head (`337dcbcf`)

No `vitest` under `C:\dev\masaha\app\` before each full lane (the process query printed nothing).
- `npm run lint` → exit 0.
- `npm run typecheck` → exit 0.
- `npm run test:unit` → exit 0: shared `Test Files  16 passed (16)` / `Tests  222 passed (222)`; api
  `Test Files  46 passed (46)` / `Tests  745 passed (745)`; web `Test Files  80 passed (80)` / `Tests  829 passed (829)`.
- `npm run test:api` → exit 0: `Test Files  52 passed (52)` / `Tests  878 passed (878)`.
- `npm run format:check` → exit 0, `All matched files use Prettier code style!`
- `npm run check:links` → `2275 links in 139 documents and 1279 source files all resolve.`
- `npm run build -w @masaha/shared` → exit 0.
- `git grep -n "#PRNUM"` → documents only (data-model 3, ADR 0009 1, finding 94 1, occupancy.md 7,
  space-settings.md 14, v1-mvp 2).
- `git diff --stat origin/main -- apps/web package.json package-lock.json` → empty.
- **Not run, by the plan:** `test:component`, the web's `build`, `check:build`, `check:classes` — no
  `apps/web` file changes and no type it imports; CI runs them on the pushed head.

## 12.5 The breaks (each: backup to `%TEMP%\settings-breaks\`, one edit, the named file run, restored from the backup)

Run by `breaks.py` (scratchpad); the full red lines are in `%TEMP%\settings-breaks\breaks.log`.

| # | Test | Result | Red line |
|---|---|---|---|
| B1 | U1 | red | `Tests  1 failed \| 2 passed (3)` — `expected null to deeply equal { maxStayMinutes: [ 'out_of_range' ] }` |
| **B2** | U1 | **NOT red** | `Tests  3 passed (3)` — see below |
| B3 | U1 | red | `Tests  1 failed \| 2 passed (3)` — `expected null to deeply equal { maxStayMinutes: [ 'out_of_range' ] }` |
| B4 | U2 | red | `Tests  1 failed \| 2 passed (3)` — `expected null to deeply equal { Object (visitRoundingMinutes) }` |
| B5 | U2 | red | `Tests  1 failed \| 2 passed (3)` — same |
| B6 | U2 | red | `Tests  1 failed \| 2 passed (3)` — same |
| B7 | U3 | red | `Tests  1 failed \| 2 passed (3)` — `expected null to deeply equal { Object (receptionMayTypePrices) }` |
| B8 | U5 | red | `Tests  1 failed \| 1 passed (2)` — `expected null to deeply equal { Object (reminderTemplate) }` |
| B9 | U5 | red | `Tests  1 failed \| 1 passed (2)` — same |
| B10 | U5 | red | `Tests  1 failed \| 1 passed (2)` — `expected null to deeply equal { reminderTemplate: [ 'too_long' ] }` |
| B11 | U5 | red | `Tests  1 failed \| 1 passed (2)` — `expected null to deeply equal { reminderTemplate: [ 'too_short' ] }` |
| B12 | U6 | red | `Tests  1 failed (1)` — `expected null to deeply equal { capacity: [ 'out_of_range' ] }` |
| B13 | U6 | red | `Tests  1 failed (1)` — same |
| B14 | U6 | red | `Tests  1 failed (1)` — `expected null to deeply equal { capacity: [ 'required' ] }` |
| B15 | U7 | red | `Tests  2 failed (2)` — `expected { data: { …(3) }, …(2) } to deeply equal { data: { …(2) }, …(2) }` (U8 red too) |

After the run, `git status --short` → empty: every file restored.

### STOP — B2 stays green, and no test can turn it red

B2 (the stay limit's `min` lowered from 60 to 1) is an **equivalent change**: the field is also
`.int().multipleOf(60)`, and no whole number from 1 to 59 is a multiple of 60, so `min(1)` and `min(60)` accept
exactly the same values (0 is refused by both). U1's 59 is refused by `multipleOf` either way. This is not a
defect of the test: the planned break cannot be seen red by any test. Per the prompt (§2, a break that stays
green; a plan that proves false against the code), the work stopped here, B16–B34 not yet run, nothing pushed.

**Offered fixes (the owner chooses):**
1. **Replace B2 by `min 0`** (`.min(0)`), and add `maxStayMinutes: 0 → ['out_of_range']` to U1: with `min(0)`, 0
   passes `multipleOf(60)` and the minimum, so U1 goes red. This proves the minimum matters (it is what refuses 0).
2. **Drop B2**, recording that `min(60)` is implied by `multipleOf(60)` with `min(1)`; keep U1 as it is.
3. Keep the code and the break as planned, and accept B2 as "not red, equivalent" in the report.

**The owner's answer (2026-10-19): option 1.** U1 gained `maxStayMinutes: 0 → ['out_of_range']` (green on the
code: `Tests  3 passed (3)`); B2 became `.min(0)` → **red**: `Tests  1 failed | 2 passed (3)` — `expected null
to deeply equal { maxStayMinutes: [ 'out_of_range' ] }`. The test change folded into C2 (`git commit --fixup`,
autosquash), then `git rebase -x "npm run lint && npm run typecheck"` over the four commits → exit 0 (each
commit ran both). New shas: C1 `69851c7c`, C2 `03785987`, C3 `ab3d7e8b`, C4 `1cc1fadc`.

| B16 | T20 | first **NOT red**, then red | see below |

### B16 — first green: the test's own defect, strengthened (a departure)

`ALTER TABLE space_settings ALTER COLUMN reception_may_type_prices SET DEFAULT true` on `masaha_b_test` → T20
still `Tests  1 passed | 24 skipped (25)`. Cause: T20 wrote the row through Prisma, which sends the schema's
`@default(false)` in its own `INSERT`, so the database's default was never read. The global setup's
`migrate deploy` does not touch it (checked: the default read back `true` while broken, `false` after). T20 now
writes the row by raw SQL (the four required columns, as the neighbouring test does) and reads it back. Green
on the code (`Tests  1 passed | 24 skipped (25)`); B16 → **red**: `Tests  1 failed | 24 skipped (25)` —
`AssertionError: expected { spaceId: 1, …(10) } to match object { receptionMayTypePrices: false }` (`+
"receptionMayTypePrices": true`); restored with `SET DEFAULT false` → the file `Tests  25 passed (25)`;
`column_default` reads `false`. Folded into C1 (fixup + autosquash); `rebase -x "npm run lint && npm run
typecheck"` → exit 0, four `Executing` lines. Shas now: C1 `e9805067`, C2 `4811e61b`, C3 `75c0735f`, C4
`52fc8c80`.

| B17 | T1 | red | `Tests  4 failed \| 5 passed (9)`: T1 (and T4, T5, T7, which read the row back) — the read answered the other space's row |
| B18 | T2 | red | `Tests  1 failed \| 8 passed (9)` — `expected 403 to be 404` |
| B19 | T3 | red | `Tests  1 failed \| 8 passed (9)` — `expected 200 to be 403` |
| B20 | T3 | red | `Tests  1 failed \| 8 passed (9)` — `expected 422 to be 403` |
| B21 | T3 | red | `Tests  1 failed \| 8 passed (9)` — `expected 422 to be 403` |
| B22 | T4 | red | `Tests  1 failed \| 8 passed (9)` — `expected [ { actorId: 1, …(6) } ] to deeply equal [ { actorId: 1, …(6) } ]` |
| B23 | T6 | red | `Tests  1 failed \| 8 passed (9)` — `expected 200 to be 422` |
| B24 | T7 | red | `Tests  1 failed \| 8 passed (9)` — `expected [ { actorId: 1, …(6) }, …(1) ] to deeply equal []` |
| B25 | T8 | red | `Tests  1 failed \| 8 passed (9)` — `expected 200 to be 403` |
| B26 | T9 | red | `Tests  1 failed \| 8 passed (9)` — `expected 403 to be 404` (a deleted space's links read empty, so can() refused) |
| B27 | T12 | red | `Tests  1 failed \| 8 passed (9)` — `expected 403 to be 404` |
| B28 | T13 | red | `Tests  1 failed \| 8 passed (9)` — `expected 200 to be 403` |
| B29 | T13 | red | `Tests  1 failed \| 8 passed (9)` — `expected 422 to be 403` |
| B30 | T15 | red | `Tests  1 failed \| 8 passed (9)` — `expected { capacity: 50, …(3) } to deeply equal { capacity: 50, …(3) }` |
| B31 | T16 | red | `Tests  1 failed \| 8 passed (9)` — `expected { capacity: null, …(3) } to be null` |
| B32 | T17 | red | `Tests  1 failed \| 8 passed (9)` — `expected 500 to be 422` |
| B33 | T18 | red | `Tests  1 failed \| 8 passed (9)` — `expected 200 to be 403` |
| B34 | T19 | red | `Tests  1 failed \| 8 passed (9)` — `expected 403 to be 404` |

Each restored from its backup (a byte copy); `git status --short` after the runs → empty.

**The lanes again on the new head `52fc8c80`** (U1 and T20 changed after the first run): no `vitest` under
`C:\dev\masaha\app\`; `npm run test:unit` → exit 0 (shared `Tests  222 passed (222)`, api `Tests  745 passed (745)`,
web `Tests  829 passed (829)`); `npm run test:api` → exit 0, `Test Files  52 passed (52)` / `Tests  878 passed
(878)`; `npm run format:check` → exit 0.

## 12.6 The real run (API on 3321, `masaha_b_dev`)

`npm run dev -w @masaha/api` in the background; `GET /health` → `{"status":"ok","db":"up",…}`. Signed in through
`POST /api/v1/auth/login` as the demo owner and the demo reception (`SEED_DEMO_PASSWORD`) and as the seeded
admin (`SEED_ADMIN_*`), each read from `apps/api/.env` into a variable, never printed. Space 1 (the demo's).

| Case | Answer |
|---|---|
| owner `GET …/settings` | 200, the eight settings, `receptionMayTypePrices: false` |
| owner `PATCH { maxStayMinutes: 240, receptionMayTypePrices: true }` | 200, `maxStayMinutes: 240`, `receptionMayTypePrices: true` |
| owner `PATCH { maxStayMinutes: 90 }` | 422, `maxStayMinutes: ["out_of_range"]` |
| owner `PATCH { reminderTemplate: "مرحبًا {الاسم}" }` | 422, `reminderTemplate: ["invalid_format"]` |
| owner `PATCH { visitRounding: "PER_MINUTE", visitRoundingMinutes: null }` | 200, `PER_MINUTE`, `null` |
| owner `GET …/capacity` | 200, `{ capacity: 40 }` (the demo's) |
| owner `PUT { capacity: 35 }` | 200, `{ capacity: 35 }` |
| owner `PUT { capacity: 0 }` | 422, `capacity: ["out_of_range"]` |
| reception `GET …/settings` | 403 `forbidden` |
| reception `PUT …/capacity { capacity: 35 }` | 403 `forbidden` |
| admin `GET …/settings` | 404 `not_found` |

`SELECT action, before, after FROM audit_logs ORDER BY id DESC LIMIT 4` → `space.capacityEdited` `{"capacity": 40}`
→ `{"capacity": 35}`; `space.settingsEdited` `{"visitRounding": "UP_AFTER_MINUTES", "visitRoundingMinutes": 15}` →
`{"visitRounding": "PER_MINUTE", "visitRoundingMinutes": null}`; `space.settingsEdited` `{"maxStayMinutes": null,
"receptionMayTypePrices": false}` → `{"maxStayMinutes": 240, "receptionMayTypePrices": true}`; then an older
entry. ✔

A note: the script first crashed printing an Arabic label on the console's code page, after the reminder's request
had gone out (a refusal, writing nothing). The rest ran from that case on, in UTF-8 mode; the reminder's 422 was
sent twice; no edit ran twice.

Stopped by process id: `tsx watch` (22416), the server (15008), `pino-pretty` (13952). `Get-NetTCPConnection
-LocalPort 3321` → only `TimeWait` entries owned by process 0, no listener.

## Before the push (the `open-pr` skill's truth check, the fetch)

- **A roadmap note** in a test comment (`reminderTemplate.unit.test.ts`: "the copy catalogue will hold it") →
  removed, folded into C3.
- `git fetch origin`: `origin/main` still `18ab1705`. **An open PR appeared: #91** (worker A, `feat/admin-owner-links`,
  head `db1fc6f0`): web files and documents only, no code file of this item. It **takes findings 94 and 95**, so
  this item's finding is **renumbered 96** (the owner's note: "renumber if taken"): the file, its heading, the
  index line and `occupancy.md`'s two links; folded into C4. `check:links` → all resolve.
- `git merge-tree --write-tree HEAD db1fc6f0` → conflicts in **`docs/architecture/findings/README.md`** and
  **`docs/project/overview.md`** only (both expected, §7); `docs/features/spaces.md` merges clean. Whichever
  PR merges second resolves them by the fast path.
- `rebase -x "npm run lint && npm run typecheck"` → exit 0 on each of the four commits. Shas: C1 `e9805067`, C2
  `4811e61b`, C3 `5473a1de`, C4 `b64fe2d1`.
- A test file changed after the unit lane passed, so `npm run test:unit` ran again → exit 0 (`222`, `745`, `829`
  passed); `format:check` → exit 0. The API lane covers no changed file (documents and a unit test only).

## 12.7 The PR number, the push, the PR

- The next number: `gh api …/issues?state=all&per_page=1…` → 91, so **#92**. `git filter-branch` replaced `#PRNUM`
  with `#92` in each commit (`git diff --stat` old head → new head: 6 documents, 28 lines, the number only);
  `refs/original` removed; `git grep -n '#PRNUM'` → nothing.
- Commits pushed: C1 `a6ef522b` feat(space-settings): gate hand-typed prices (44) · C2 `7b708ccf`
  feat(space-settings): edit a space's settings (45) · C3 `ba415cec` feat(space-settings): add reminder
  placeholders (47) · C4 `2aec1e91` feat(occupancy): set a space's capacity (39).
- `git push -u origin feat/space-settings` → `[new branch]`. Labels `feat`, `area:api`, `area:docs` existed.
  `gh pr create --assignee @me …` → **https://github.com/Basel-Ghonaim/masaha/pull/92**: GitHub's number equals
  the one in the documents.

## `OPEN_DECISIONS.md` point 1 — the text to write (not written by the executor)

The plan's §12.8 asks for `C:\dev\masaha\workspace\_SHARED\OPEN_DECISIONS.md` point 1 to be updated; the exec
prompt (§1.5) allows no write outside the repository but this report. So the file is untouched, and this is the
replacement text for point 1, ready to paste:

> 1. **A price typed by hand at the desk** (a custom subscription's price, a visit's charge) — **settled
>    (#92, 2026-10-19):** the space setting «السماح للاستقبال بالأسعار اليدوية» is stored
>    (`receptionMayTypePrices`, **off by default**, every existing space included); the owner always may; **every
>    hand-typed price, the owner's included, carries a required reason**, recorded with who typed it (data model
>    › *Front desk and money*, ADR 0009 revised). *Enforced in: step 7 (visits) and step 8 (subscriptions).*
>    **Carried to step 7 (Q4, the owner's answer):** with the switch off and no rate at all, reception closes the
>    visit **unpriced**; it appears in the owner's «يحتاج انتباهك» for the owner to price it — never closed free.

## 12.8 CI, the conflict, CLEAN

- First CI run, on `2aec1e91`: every check **pass** (build, check:classes, check:links, format:check, lint,
  test:api 4m9s, test:component 6m9s, test:unit, typecheck; CodeRabbit skipped). But GitHub showed
  `DIRTY CONFLICTING`: **#91 had merged** into `main` (`a8c39bda`).
- **The fast path** (workflow §9, *Conflicts*; documents only): `git rebase origin/main` — C1–C3 applied clean;
  C4 conflicted in the two expected files:
  - `docs/architecture/findings/README.md`: both sides kept — main's 94 and 95, then this item's 96;
  - `docs/project/overview.md`: main's *Spaces* line (it adds "naming its owners") with this item's change
    ("The owner/reception web screen remains planned.").
  `docs/features/spaces.md` merged by itself ("and capacity" gone from both its sentences). `npm run format:check`
  → exit 0; `npm run check:links` → `2287 links in 141 documents and 1302 source files all resolve.`; no `#PRNUM`.
- New shas: C1 `840e982f`, C2 `aa7db054`, C3 `7c47efdc`, C4 `af5a05a6`. `git push --force-with-lease`.

- Second CI run, on `af5a05a6`: every check **pass** (build 26s, check:classes, check:links, format:check, lint,
  test:api 3m55s, test:component 4m55s, test:unit, typecheck); `gh pr view 92 --json headRefOid,mergeStateStatus`
  → `af5a05a6aea5b0a5f4472d218db40c60ccb12591 CLEAN` (the branch's head). The PR description updated to the final
  state (the finding's number, the rebase onto #91).
- `git status --short` → empty; port 3321 has no listener.

---

# The final report

## 1. The pull request
**#92** https://github.com/Basel-Ghonaim/masaha/pull/92 — `feat(space-settings): edit a space's settings` · head
`af5a05a6aea5b0a5f4472d218db40c60ccb12591` · CI green on it · `CLEAN`. Labels `feat`, `area:api`, `area:docs`;
assigned to the owner. Not merged.

## 2. The commits (on `a8c39bda`, main after #91)
- `840e982f` feat(space-settings): gate hand-typed prices (44)
- `aa7db054` feat(space-settings): edit a space's settings (45)
- `7c47efdc` feat(space-settings): add reminder placeholders (47)
- `af5a05a6` feat(occupancy): set a space's capacity (39)

Migration `20261019092820_reception_typed_prices`: applied to `masaha_b_dev` (13 rows, 0 true) and to
`masaha_b_test` (the API lane's `migrate deploy`).

## 3. Run, and not run
- Each commit: `npm run lint` and `npm run typecheck` exit 0 (after each commit, and again by `rebase -x` after
  each fold).
- On the head: `test:unit` (shared 222 · api 745 · web 829 passed), `test:api` (52 files, 878 passed),
  `format:check`, `check:links`, `build -w @masaha/shared` — all exit 0. After the rebase onto #91 (documents
  only): `format:check`, `check:links` locally; every lane by CI, green.
- Not run locally: `test:component`, the web's `build`, `check:build`, `check:classes` — no web change; CI ran
  `test:component`, `build` and `check:classes` green.

## 4. Breaks and red-first
Every planned test seen failing first (§ Commits above). B1–B34 all seen red, each restored from its backup
(table above). B2 changed on the owner's decision; B16 after strengthening T20 (below).

## 5. Problems and their solutions
- Docker Desktop was not running → started it; the container came up healthy.
- A heredoc Python script did not parse in Git Bash → written as a scratchpad file.
- U5: an empty reminder answered two codes (Zod 4 runs the amount's refinement after `min` fails) → the
  amount's rule skips an empty text.
- B2 equivalent to the code → stopped and asked; the owner chose `min 0` + U1's `0` case.
- B16 green: T20 went through Prisma, which sends the schema default → T20 inserts with raw SQL.
- The real-run script crashed printing Arabic on the console's code page (after a refusal had gone out) → re-run
  from that case in UTF-8 mode; no edit ran twice.
- #91 opened, then merged, during the work → finding renumbered 96; the two expected document conflicts resolved
  by the fast path.

## 6. Unexpected, even unsolved
- `prisma format --check` fails on `origin/main`'s own schema (not a project check; untouched).
- Zod 4 runs object and string refinements even when another check of the same value failed (the pair rule
  appears beside other fields' codes — acceptable, Review Focus 2; the empty reminder — handled).
- `npx vitest` printed `npm warn allow-scripts .npmrc allow-scripts setting is being ignored…` once; no effect.

## 7. The early conflict check
`gh pr list --state open` → only #92. No other open PR to check (#91 merged; its conflicts resolved above).

## 8. Departures from the prompt and the plan
1. **B2** replaced by `min 0`, and U1 gained `maxStayMinutes: 0 → out_of_range` — the owner's decision (the
   planned break was equivalent to the code).
2. **T20** writes the row by raw SQL instead of `createSettings` — the planned form could not see the database's
   default (B16 stayed green); strengthened, B16 then red.
3. **The finding is 96, not 94** — #91 took 94 and 95 (the owner's "renumber if taken").
4. **The reminder's amount rule skips an empty text** (`text === '' || …`) — beyond the plan's sketch, so U5's
   `'' → ['too_short']` holds under Zod 4.
5. **`OPEN_DECISIONS.md` not written** — the exec prompt allows no write outside the repository but this
   report; its point 1 text is above, ready to paste.
6. Two links in the new `occupancy.md` pointed at the ADR 0008's file and the entity's section as the plan named
   them; corrected to the real ones (`0008-live-status-not-counts.md`, data model › *Spaces*).

---

# Fix round 1 (review `6_REVIEW_CLAUDE_CODE.md`, prompt `7_FIXES_PROMPT.md`)

Start: head `af5a05a6`, `origin/main` `a8c39bda` (unchanged), only #92 open. The findings index on `origin/main`
ends at 95; this PR holds 96, so the new finding is **97**.

## The fixes (documents only; no code)
1. **ADR 0009 (review 2)**, in C1: the row now reads «New customer; subscription from a package, or a custom one
   (its price typed by hand: the row below)», so it agrees with the hand-typed price row under it.
2. **`security.md`'s *Built* header (review 3):** C2 adds "its settings routes" and C4 makes it "its settings and
   capacity routes", as the body says.
3. **C4's message (review 4):** "finding 94" → "finding 96"; the subject and the rest of the body unchanged.
4. **Finding 97 (review 5)**, in C2 (the commit that adds the second home): `97-the-visit-rounding-rule-is-written-twice.md`
   and its index line (Open). 97 is the next free number: `origin/main`'s index ends at 95, and this PR holds 96.
5. **The nits:**
   - DI-41 glossed in place, as «the owner's design decision DI-41» (data model, `space-settings.md`), in C2;
   - the build map's step 5 no longer cites §9 occupancy (capacity), in C4;
   - the conventions' *Built* header lists only the modules without a feature document (`sessions`,
     `platform-settings`); `space-settings` dropped in C2, and C4 no longer adds `occupancy`;
   - the data model's sentence: "the closing-time check-out and the stay limit apply at once, to the stays
     already open too; the capacity at the next check-in and in the live status", in C4.

`OPEN_DECISIONS.md` point 1: done by the supervisor (not touched).

## How they were folded (a departure in method)
These fixes change lines that both C2 and C4 change (the two *Built* headers, the findings index). A fixup
made on the head would not apply right after C2, so `--fixup` with autosquash would have stopped on its own
diffs. The same result was made by a non-interactive rebase: `GIT_SEQUENCE_EDITOR` marked C1, C2 and C4 `edit`,
and each stop got `git commit --amend --no-edit` with its own changes. C4 conflicted, as expected, in
`findings/README.md` (resolved 94, 95, 96, 97) and `conventions.md` (C2's fixed header kept). C4 was then
committed with its reworded message (`git commit -F`). Bodies kept. Checks:
- `git diff --stat af5a05a6 HEAD` → 8 documents, `15 insertions(+), 7 deletions(-)`; no code file;
- per commit: only C1, C2 and C4 changed, each with its own files; C3's tree and message are as before;
  only C4's message changed.

## Run
- `npm run check:links` → `2287 links in 142 documents and 1302 source files all resolve.` (exit 0).
- `npm run format:check` → exit 0.
- `git grep "#PRNUM\|finding 94" -- docs` → nothing.
- Not run (as the prompt says, documents only): lint, typecheck, the lanes. CI runs them.

## Commits after the round
C1 `1548d239` feat(space-settings): gate hand-typed prices (44) · C2 `2eecc64a` feat(space-settings): edit a
space's settings (45) · C3 `46c66150` feat(space-settings): add reminder placeholders (47) · C4 `a9dca5cb`
feat(occupancy): set a space's capacity (39). `git push --force-with-lease` → `af5a05a6...a9dca5cb (forced update)`.

## CI, CLEAN, conflicts
- CI on `a9dca5cb`: every check **pass** (build, check:classes, check:links, format:check, lint, test:api 4m13s,
  test:component 6m20s, test:unit, typecheck); `gh pr view 92` → `a9dca5cb4334ae86aa5b10eef45dde271e63f01b CLEAN`.
- `origin/main` still `a8c39bda`; `gh pr list --state open` → only #92: nothing to check for conflicts.
- The PR description updated to the final state (findings 96 and 97, a *Fix round 1* section).
- `git status --short` → empty.

## Unexpected
- Nothing new beyond the method note above (the fixups' shared lines).
