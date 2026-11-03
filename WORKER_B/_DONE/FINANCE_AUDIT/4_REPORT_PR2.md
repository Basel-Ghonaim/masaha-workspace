# FINANCE_AUDIT — PR 2 report (`feat/platform-settings`)

Executor: worker B's executor of PR 2, 2026-10-28, under the run's rule (`3_EXEC_PROMPT_PR2.md` §0: no stop until
ready for review) and `_SHARED\AUTONOMY_2026-10-25.md`. Long outputs in `scripts\`.

## Read

- `3_EXEC_PROMPT_PR2.md` whole; `_SHARED\AUTONOMY_2026-10-25.md` whole.
- `2_PLAN.md`: the approval note and header; §1; §2 (Scope, Acceptance criteria, Out of scope); §3; §4 (the owner's
  decisions, D1, D3, D4, D7, D13, D14, D15); §5 S8–S11 and *Rules the item touches*; §6; §7; §8; §9 PR 2 and *Not
  tested*; §10 (no settings line in it); §11; §12 whole (12.1–12.9, the PR 2 parts used); §13; Appendix A PR 2.
- `4_REPORT_PR1.md` whole; `6_REVIEW_PR1_CLAUDE_CODE.md` whole (F1–F3; their lessons: test the real writers through
  the routes, keep the capability document true to the code, date every rewritten decision line).
- Repository: as each step needed (listed under each commit).

## Preconditions (§12.1)

- `git fetch origin`; worktree detached at `76661f7c` = `origin/main` (Merge #128), clean.
- PR 1 (#128) merged as built: `audit/platformEvents.ts` holds `PLATFORM_ACTIONS` and `PLATFORM_ACCOUNT_ACTIONS`;
  the target joins are one `LEFT JOIN` per type (`audit.repository.ts`): a `platformSettings` entry joins none, so it
  reads `name: null, nameAr: null, deleted: false` with no change to the joins.
- Base diff `3855e37f..origin/main` on PR 2's code files (§7): none changed outside the item's PRs but `app.ts`
  (#123's and #128's wiring, which PR 2 builds on). No difference the plan does not cover.
- Open PRs: **#129** `feat/step10-screens` (worker A, head `fcf46637`), files `apps/web` only by `gh pr view 129
  --json files` at the start.
- `0_CARRIED_FROM_*.md`: only `0_CARRIED_FROM_123.md` (PR 1's) — PR 2 has no C0.
- Docker: `masaha-postgres-1 Up (healthy)`. `apps/api/.env`: `PORT=3321`, `masaha_b_dev`, `masaha_b_test` (matched by
  pattern, credentials masked).
- `npx prisma migrate status` on `masaha_b_dev` and on `masaha_b_test`: "Database schema is up to date!" (29
  migrations) — nothing to deploy.
- `npm run build -w @masaha/shared` → exit 0.
- Branch: `git switch --no-track -c feat/platform-settings origin/main`.
- Memory 16:13: 4,828,180 KB free.

## §12.2 PR 2 first checks

- **Check 2:** `\d settings` on `masaha_b_dev`: `updated_at` has **no default** (`created_at` has `CURRENT_TIMESTAMP`), so
  `ensure` passes `now()` itself.
- **Check 4:** the dev rows each pass their read schema: `stalenessDays` 60, `priceStalenessDays` 30, `newSpaceDefaults`
  the seeded object; `contactEmail` a string that is an email, `contactWhatsapp` a string in E.164 form (checked by
  SQL pattern; the values not printed).
- **Check 1:** `Prisma.JsonNull` writes a JSON `null` into the `Json` column (T2's clear: `contactEmail` reads back
  `null`, green).
- **Check 3:** `@masaha/shared/space-settings` exports `newSpaceDefaultsSchema`; the API's `platform-settings/index.ts`
  re-exports it, so `demo.ts` and `demoDirectory.ts` are untouched; shared build 0, typecheck 0; the seed's API tests
  (`src/db/seed`) green. The minutes' two codes (`required`, `invalid_format`) come from the space settings' own
  `roundingPair`, reused as the schema's `superRefine` (U1's defaults lines).

## Commits

### C1 `28258564` feat(platform-settings): read and save its cards (48)

- Read: `platform-settings/*` whole, `shared/audit/{writeAudit,index}.ts`, `audit/{platformEvents,audit.repository}.ts`
  (the joins), `@masaha/shared/{space-settings,audit,core}` (`roundingPair`, `emailSchema`, `phoneSchema`,
  `toFieldErrors`), `space-settings` module (the model for the change rule and the controller), `test/{admin,
  locks,spaces,factories}.ts`, `spaces/space/{create,space}.api.test.ts` (the setup), `app.ts`, `eslint.config.js`
  (L0), `directory/cache.ts`; docs: the contract's *Settings (managed)*, *Audit log*, *Users (the admin)*; conventions
  header, §6, §7, §9, §13; data model *Conventions*, *Setting*; finding 40 and the index; `space-settings.md`,
  `audit.md`, `favorites.md` (form).
- **Red first, each** (`scripts\pr2-c1-*-red.txt`):
  - U1 (shared `platform-settings/requests.unit.test.ts` and the defaults' lines in `space-settings/requests.unit.test.ts`)
    before the schemas: `Error: Cannot find module './requests.ts'` and `TypeError: Cannot read properties of undefined
    (reading 'safeParse')` — `× takes the four defaults whole, …`.
  - PR 1's U1 gains `the platform's settings are the platform's`: `AssertionError: platformSettings.newSpaceDefaultsEdited:
    expected false to be true` — `Tests 1 failed | 1 passed (2)`.
  - U2 (`settingsChange.unit.test.ts`) against a stub answering every field (backup in `scripts\stubs\`, restored,
    SHA-256 `922fddfb…` both): `AssertionError: expected { before: { …(3) }, after: { …(3) } } to deeply equal { …(2) }`.
  - T1–T8 (`adminSettings.api.test.ts`) with the service built but the router not mounted: `Tests 7 failed | 4 passed
    (11)` — `expected 404 to be 200` (T1–T3), `expected [ 'prices' ] to deeply equal [ 'amenities', … ]` (T4), `Error: 1
    request(s) never waited on a lock` (T5, T6), `staleness: expected 404 to be 422` (T8). **T7's four refused callers
    passed before the router existed** (the `/admin` guard answers first, as PR 1's T14): B9 is its break.
  - T11 (`platformAuditLog.api.test.ts`, through the real routes: the three saves, then the admin's log) with the three
    actions removed from the list (backup, restored, SHA-256 same): `AssertionError: expected [] to deeply equal [ { …(4) },
    { …(4) }, { …(4) } ]`.
- Green: U1 `Tests 7 passed (7)`; U2/PR 1 U1 `Tests 4 passed (4)` (the api unit files of `platform-settings` and
  `audit`); T1–T8 `Tests 11 passed (11)` on the first run with the router; T11's file `Tests 10 passed (10)`; with
  `create.api.test.ts` and `src/db/seed`: `Test Files 6 passed (6) · Tests 64 passed (64)`.
- lint: first run 3 errors in my tests (two `!`, one unused `_left`) — fixed before the commit; then exit 0. typecheck:
  first run failed (`AuditValue` not exported from `shared/audit`'s index; the cards' interfaces not assignable to an
  index signature) — fixed (the type exported; `settingsChange` over `object`); then exit 0. Shared build 0. Prettier
  clean. `check:links` "2957 links in 200 documents and 2117 source files all resolve."
- Docs: contract *Platform settings* (new, after *Users (the admin)*: the six routes, bodies, bounds, audit names, the
  lock) and *Audit log* (`platformSettings` target with `id: null`, the admin's list); data model (*Conventions ›
  Settings*, *Setting*); conventions (header *Built*, §6 the writer's no-id entry and the allowlist, §7 the module
  linked, §9 *Settings* without finding 40's sentence, §13 the settings' rows); finding 40 *Resolved* with its
  *Resolution*, the index line moved under *Resolved* (between 39 and 41); `features/platform-settings.md` (new);
  `space-settings.md` (code map, history); `audit.md` (a decision line, history).
- Memory before the first API file: 3,600,516 KB (a single test file, not a lane; ran); before typecheck 4,092,232 KB;
  before lint 4,350,156 KB.

### C2 `7d5bb489` feat(platform-settings): answer the public contact (50)

- Test first: T9–T10 (`publicContact.api.test.ts`) before the router: `Tests 2 failed (2)` — `expected 404 to be 200`,
  `expected 404 to be 500` (`scripts\pr2-c2-t-red.txt`).
- Code: `platform-settings.public.routes.ts` (`GET /public`), the controller's `publicContact` (`Cache-Control: public,
  max-age=300`), mounted `api.use('/settings', …)` beside the lookups; one controller for both routers.
- Green: both files of `platform-settings/` `Test Files 2 passed (2) · Tests 13 passed (13)`.
- typecheck 0; lint 0 (memory 5,106,952 KB before); Prettier clean; `check:links` "2962 links in 200 documents and 2119
  source files all resolve."
- Docs: contract (the public route, its cache and its 500; the section's access line); conventions header (the public
  contact); `platform-settings.md` (what, who, composes, flows, a decision, code map, history); v1-mvp (step 11
  *Built*, the public directory's *Built*, the two rows, the ordering note); overview (*Built*: *Platform settings*);
  `docs/README.md` (the map's line).
- Subjects: C1 48, C2 50 characters.

## The breaks (§9 PR 2, B1–B12) — each red, restored from its backup, SHA-256 same, green

`python -I -u scripts\brk.py scripts\pr2-breaks.json B1 … B12` (`scripts\pr2-breaks.out`, definitions in
`make_pr2_breaks.py`); memory before 5,125,272 KB. Tree clean after (`git status --short` empty).

| B | The edit | Red line | Restored |
|---|---|---|---|
| B1 | shared `stalenessSchema`: `.max(STALENESS_DAYS_MAX)` removed | `expected { stalenessDays: [ 'out_of_range' ] } to deeply equal { …(2) }` | `Tests 3 passed (3)` |
| B2 | the defaults' `.superRefine(roundingPair)` removed | `expected null to deeply equal { Object (visitRoundingMinutes) }` | `1 passed | 3 skipped` |
| B3 | `settingsChange` counts every field | `expected { before: { …(3) }, after: { …(3) } } to deeply equal { …(2) }` | `1 passed (1)` |
| B4 | an optional key's missing row throws (read as required) | `expected 500 to be 200` (T1) | `1 passed | 10 skipped` |
| B5 | the no-change branch removed | `expected [ { actorId: 1, …(6) }, …(5) ] to have a length of 3 but got 6` (T2) | same |
| B6 | the defaults' `write` skipped | `expected { autoCheckoutAtClosing: true, …(3) } to deeply equal { autoCheckoutAtClosing: false, …(3) }` (T3) | same |
| B7 | `lock`'s `FOR UPDATE` removed | `expected [ { actorId: 1, …(6) } ] to match object [ { …(3) } ]` (T5: `before` 60, not the first's 50) | same |
| B8 | `ensure` removed | `Error: 1 request(s) never waited on a lock` (T6) | same |
| B9 | the admin router mounted at `/admin/settings` on `api`, before the guard | `get /settings/new-space-defaults: expected 200 to be 401` and `… expected 200 to be 403` — the four callers (T7) | `4 passed | 7 skipped` |
| B10 | the `Cache-Control` header removed | `expected undefined to be 'public, max-age=300'` (T9) | `1 passed | 1 skipped` |
| B11 | the read without its parse | `expected 200 to be 500` (T10) | same |
| B12 | the three actions off the admin's list | `expected [] to deeply equal [ { …(4) }, { …(4) }, { …(4) } ]` (T11) | `1 passed | 9 skipped` |

- None stayed green. B8 is red by the lock wait rather than the plan's "unique violation, 500": without `ensure` the
  second save never waits, so the test's own guard (finding 52's `waitingOnLock`) fails first; the unique-violation
  path is not reachable because `write` updates (it never inserts). Either way the race's guard is proven.
- T7 passed before the router existed (the guard answers first): B9 is its proof.

## Verification on the head (`7d5bb489`; `scripts\head-verify.sh`, outputs `scripts\head2-*.txt`)

Each preceded by a free-memory reading (≥ 4,000,000 KB to run, else a 2-minute wait, 45 at most):
- build: first 3,798,724 KB → waited 2 min → 5,229,836; `npm run build -w @masaha/shared` exit 0.
- `npm run lint` (5,233,416) exit 0 · `npm run typecheck` (5,044,340) exit 0.
- `npm run test:unit` (5,942,548) exit 0: `Tests 267 passed (267)` · `Tests 881 passed (881)` · `Tests 1004 passed (1004)`.
- `npm run format:check` "All matched files use Prettier code style!" · `npm run check:links` "2962 links in 200
  documents and 2119 source files all resolve." · `npm run check:conflicts` "No conflict markers found."
- `npm run test:api` (5,467,500; no command timeout) exit 0: `Test Files 99 passed (99)` · `Tests 1260 passed (1260)` ·
  `Duration 731.69s`.
- `npm run test:component`: waited 18 × 2 min for memory (worker A busy; 2.6–3.9 GB free), then at 4,403,924 KB exit 0:
  `Test Files 264 passed (264)` · `Tests 1564 passed (1564)` · `Duration 671.86s`.
- `git grep -l '#PRNUM'`: documents only (9). `git diff --stat origin/main -- apps/web package.json package-lock.json`:
  empty.

After the head-verify, finding 153 folded into C1 (documents only: `git diff --stat 7d5bb489 HEAD` = the finding, its
index line, `platform-settings.md`'s *Open findings*); `check:links` re-run: "2966 links in 201 documents and 2119
source files all resolve." Commits now `2d4deef5` (C1), `099946a3` (C2).

## The real run (API on 3321, `masaha_b_dev`; `scripts\realrun2.mjs`)

**First run (`scripts\realrun2-first.out`) — stopped by its own guard:** the reads PASS; `PUT new-space-defaults` and
`PUT staleness` with the same values wrote nothing (PASS); **`PUT contact` with the same values wrote**: entry **56**
`platformSettings.contactEdited`, `after` keys `whatsapp` only. By SQL (values never printed): the seeded number was
`+972…`, the save stored `+970…`, the same nine national digits — a Palestinian mobile, which the project's phone
rule always puts on `+970`; the email was already lowercase. The script stopped before any other write ("the originals
did not round-trip: no write performed"). See decision 5 (SERIOUS) and finding 153.

**Second run (`scripts\realrun2.out`) — `ALL PASS`**, from the state after entry 56:
```
PASS health db up · audit entries before: 56
PASS admin reads the new-space defaults 200 · the thresholds ({"stalenessDays":60,"priceStalenessDays":30}) 200 · the contact (email set, whatsapp set) 200
PASS PUT new-space-defaults / staleness / contact with the same values writes nothing 200 (×3)
PASS admin saves the contact: normalised, answered as saved 200
PASS …audited on the admin's log, no entity id, only what changed 200
PASS GET /settings/public (anonymous) answers the saved contact, cached 5 minutes 200
PASS admin puts the contact back 200
PASS the admin's log shows platformSettings.contactEdited (3 in all) 200
PASS a threshold applies at once: stale groups [] → ["profile","hours","prices","amenities","contacts"] 200
PASS …audited platformSettings.stalenessEdited, only what changed 200
PASS admin puts the thresholds back; the stale groups as before 200
PASS admin saves the defaults; audited with only the switch 200 · admin puts the defaults back 200
NOT PERFORMED a new space after a default changed: §12.6 names no space creation; proven by T3 (B6 red).
PASS a guest 401, a user (the reception account, role USER) 403, an owner 403 — GET and PUT of each of the three cards (18)
     settings after = settings before (md5 of each value); audit entries after: 62 (+6)
ALL PASS
```
- **The run's writes:** entry 56 (the first run's same-values contact save, the WhatsApp normalised, not put back —
  decision 5); then contact → test → original (57, 58), staleness → 1/1 → 60/30 (59, 60), defaults → auto check-out
  flipped → original (61, 62). Every setting after the second run equals its value before it (fingerprints equal); the
  contact's WhatsApp is the normalised form of the seeded number.
- Server stopped by process id (server 528, `tsx watch` 748, `pino-pretty` 18096); port 3321: no listener;
  `server.log` deleted.

## Decisions taken without the owner (as they were met)

1. **`audit.md` touched in C1, not on §7's PR 2 list.** *Met:* the admin's list gained the three settings actions, and
   the target of a `platformSettings` entry has no id. *Options:* leave the capability document silent; one decision and
   one history line. *Chose* the two lines: the document stays true to the code (PR 1's review F2 lesson). *Undo:* drop
   them.
2. **`shared/audit/index.ts` exports `AuditValue`** (not in D15). *Met:* `settingsChange` types its values with the
   writer's `AuditValue`. *Chose* to export the existing type rather than restate it. *Undo:* inline the type.
3. **The save's actor is passed as an id** (`saveX(actorId, value)`, D7 wrote `actor`). *Why:* the `/admin` guard
   already decided; only the id is audited. *Undo:* pass `Actor`.
4. **T11 through the real routes** (the three `PUT`s, then the admin's log), not inserted entries. *Why:* PR 1's F1
   showed inserted entries cannot see a writer's slip. *Undo:* n/a.
5. **SERIOUS — the dev contact's WhatsApp left in its normalised form (`+970…`), not restored to the seeded `+972…`.**
   *Met:* the real run's first case ("the same values write nothing") saved the contact read from the card; the seeded
   number, a Palestinian mobile given with `+972`, is normalised by the save to `+970` (the project's one phone form),
   so the save wrote and audited it (entry 56). *Options:* restore the raw value by SQL (a database write the run may
   not make: hard limit); restore it through the app (impossible: the save normalises); leave it. *Chose* leave it,
   and record finding 153: the same number, in the form the app stores, written by the route under test; nothing else
   changed (the run's guard stopped before any other write). *Undo:* the owner restores the seed's value by SQL
   (`UPDATE settings SET value = '"<the seeded number>"' WHERE key = 'contactWhatsapp'` on `masaha_b_dev`) or re-runs
   the seed's contact; entry 56 stays (append-only).
6. **Finding 153 recorded and folded into C1** (the seed takes any E.164 contact number and stores it as given, while
   the phone rule stores one form). *Why:* met in the real run; the code is the seed's (`run.ts`), outside this PR's
   scope, so recorded, not fixed. *Undo:* delete the finding and its two lines.
7. **The real run saved each card and put it back** (the exec prompt §5: "saves each card … so the run can put them
   back"; §12.6 named only the contact). The thresholds' save also proves "a threshold applied at once" on the demo
   space. *Why:* the owner's prompt names the cases; each put back, proven by the values' fingerprints. A new space
   was not created (§12.6 names no such write): T3 proves it. *Undo:* n/a.
8. **"A user" refused = the demo reception account** (global role `USER`): the demo has no plain user account.
9. **B8's red is the lock wait, not a 500** (see *The breaks*). *Undo:* n/a.

## The PR number, push, PR

- `gh api …/issues?state=all&per_page=1` → 129 (worker A's #129), so 130. `scripts\prnum-pr2.sh 130` → `PRNUM OK #130
  299d8abd (was 099946a3)`; backup `backup/platform-settings-pre-prnum`; no `#PRNUM` left; only the number changed.
  `check:links` "2966 links … resolve", `format:check` clean; the number re-read: still 130.
- `git push -u origin feat/platform-settings`; `gh pr create --assignee @me --label feat --label area:api --label
  area:docs --title "feat(platform-settings): edit defaults and contact"` → **#130** = the commits' number (no redo).
- Commits: `052f0e11` feat(platform-settings): read and save its cards (48) · `299d8abd` feat(platform-settings):
  answer the public contact (50). Files against `origin/main`: **36** (the plan said ≈ 32: + finding 153, `audit.md`,
  `shared/audit/index.ts`, `publicContact`'s and the public router's own).

## CI and the state at the end

- My bounded `gh pr checks 130 --watch` was rejected in the session (the user interrupted the tool call); checked
  again after: on head `299d8abd` (= `git rev-parse HEAD`) build (39s), check:classes (33s), check:conflicts (28s),
  check:links (30s), format:check (36s), lint (1m44s), test:api (7m9s), test:component (7m30s), test:unit (1m29s),
  typecheck (49s) — **all pass**; CodeRabbit skipping. `mergeStateStatus` **CLEAN**.
- Conflicts: `git merge-tree --write-tree HEAD fcf46637` (worker A's #129) exit 0, clean; #129's files are all under
  `apps/web` (no shared document). `origin/main` still `76661f7c`: no rebase needed.
- `git status --short` clean; no rebase in progress. Branch left: `backup/platform-settings-pre-prnum` (`099946a3`).
- COULD NOT RUN / refused: none (the CI watch call was interrupted by the user, then read directly).
