# ANNOUNCEMENTS — PR 1 (`feat/announcements`) — the executor's report

Written as the work goes (2026-10-24).

## 1. Preconditions and §12.1

- `origin/main` at `8fc5939e` (Merge #110); `C:\dev\masaha\app-b` detached at it, `git status --short` clean. ✔
- Merged: #102 `feat/customers`, #104 `chore/directory-demo-set`, #106 `feat/subscriptions`, #109
  `feat/subscription-check-ins`, #110 `fix/subscriber-checkout-due`. ✔
- No `0_CARRIED_FROM_*.md` in this folder: nothing carried. ✔
- Open PRs: **none** (`gh pr list --state open` empty).
- Base diff `befd96f9..origin/main`, the code files PR 1 names: `app.ts`, `subscriptions/index.ts`,
  `occupancy/occupancy.service.ts`, `occupancy/present.api.test.ts`, shared `core/errors.ts`,
  `desk/responses.ts` changed — all SUBSCRIPTIONS' / DEMO_SEED's work the plan builds on; `apps/web/src/test/publicSpace.ts`
  (new, worker A's #107) is a `PublicSpace` fixture, check 5's case.

### A1–A11
- A1 ✔ `subscriptions.mapper.ts`/`repository.ts` read dates by `toISOString().slice(0, 10)`.
- A2 ✔ the end writes `endsOn`, `endedAt`, `endedById` (`subscriptions.repository.ts:262`).
- A3 ✔ every subscription write goes through `lockAtDesk` / `lockSubscription`, `spaces.lock` first.
- A4 ✔ `statesOf` in `subscriptions.service.ts`.
- A5 ✔ `occupancy.checkInWarnings(spaceId, now, tx)`; `desk.service.ts` calls it in the visit check-in
  (`checkInVisit`) and the subscriber check-in (`subscriberWarnings`, the space's warnings first): C5's
  `CLOSURE_IN_FORCE` reaches both.
- A6 ✔ `gazaClockOf`, `addDays`, `weekStartOf` in `core/gazaTime.ts`.
- A7 ✔ `\d subscriptions` on `masaha_b_test`: `subscriptions_dates_check` (`starts_on IS NULL OR ends_on IS NULL OR ends_on >= starts_on`).
- A8 ✔ `@@index([spaceId, endsOn])` on `Subscription`.
- A9 — `subscriptions/` is still flat (no use-case folder yet); PR 1 adds `subscriptions/closures/` as planned
  (conventions §8 *Growth*). No effect on the plan.
- A10 — **a difference, covered by §12.2 check 3:** the directory demo set seeds an active closure
  (`demoDirectory.ts:675`, `closed: true`) — "no announcement" is not true. Its `announcement.create` gains a key
  like the tests'; the migration backfills the dev rows. Accounts as assumed (`demo-directory-owner@example.com`, unverified spaces present).
- A11 ✔ the four scenario subscriptions in `demo.ts`, dated around today (e.g. `-6 … +14`).

## 2. Setup
- `docker start masaha-postgres-1` ✔; `apps/api/.env` names `masaha_b_dev`, `masaha_b_test`, `PORT=3321` ✔.
- `prisma migrate status` → "Database schema is up to date!" (24 migrations); both databases at
  `20261022071444_subscription_terms`.
- `git switch --no-track -c feat/announcements origin/main` ✔; `npm run build -w @masaha/shared` exit 0.

## 3. §12.2 first checks
- **Check 1 — the migration, created once:** `prisma migrate dev --create-only --name announcement_key` run **once** →
  refused, nothing created: `Error: Prisma Migrate has detected that the environment is non-interactive, which is not
  supported.` (`ls` unchanged). The fallback SUBSCRIPTIONS used: `prisma migrate diff --from-config-datasource
  --to-schema prisma/schema.prisma --script` (read-only) → Prisma's `ADD COLUMN "request_id" UUID NOT NULL` and the unique
  index; written by hand into `20261024095504_announcement_key/migration.sql` (UTC), edited to D12's SQL (nullable
  column, backfill, `SET NOT NULL`, then the index). SQL read before applying. `npm run db:migrate` → "Your database is
  now in sync with your schema." on `masaha_b_dev`; `prisma migrate status` → up to date (25). `masaha_b_test`: the
  API lane's global setup applied it ("Applying migration `20261024095504_announcement_key`", c1 red run).
  `prisma generate`: `models/Announcement.ts` names `idempotencyKey`.
  - `prisma format` was tried once and **reverted**: it realigns unrelated models (`User`, `SpaceSettings`, …, 69
    lines); the `Announcement` model is aligned by hand instead.
- **Check 3 — the inserts:** `git grep "announcement.create"` → the four test files of §7 **and the directory demo
  seed** (`db/seed/demoDirectory.ts`, A10's difference); each gains `idempotencyKey: randomUUID()` only.

## 4. Commits

### C1 `b60907ac` feat(announcements): post and edit announcements (48)
- U4 (shared `requests.unit.test.ts`) red before its code: `Error: Cannot find module './requests.ts'` → green
  `Tests  4 passed (4)`.
- U1–U3 red before their code: `Cannot find module './announcementState.ts'` / `'./period.ts'` /
  `'./announcementChange.ts'`, `Test Files  3 failed (3)` → green `Tests  7 passed (7)`.
- T1–T7 (`announcements.api.test.ts`) red with the router unmounted (backup, edit, restore; SHA-256 same before and
  after, `c16d2a58…`): `× ` 8 of 9 failing (the not_found test passes unmounted — B12 proves it) → green with the
  touched files: `Test Files  5 passed (5)  Tests  61 passed (61)` (announcements, `db/schema`, `liveStatus`,
  `override`, `present`); the seed's lane files `Tests  20 passed (20)`. D1 is proven by its break B6.
- `npm run lint` exit 0; `npm run typecheck` exit 0; `check:links` "2655 links … all resolve" (after fixing my own
  link to data-model `#live-status`, no such heading → `#derived-values-computed-not-stored`); a lint error in
  `announcementChange.ts` (an unneeded assertion) fixed before the commit.

### C2 `443b0705` feat(announcements): end, start or delete one (45)
- T8–T11 (`lifecycle.api.test.ts`) red before the code: `Tests  3 failed | 1 passed (4)` (T8, T9, T10 `×`; T11
  passes while the routes are missing — B17 proves it) → green with the module's API files: `Test Files  2 passed (2)
  Tests  13 passed (13)` (T6 now covers the three new routes too).
- `ANNOUNCEMENT_NOT_STARTED` by the `add-error-code` steps: shared `core/errors.ts`, both catalogues (Q1's Arabic
  «لم يبدأ هذا الإعلان بعد.», English "This announcement has not started yet."), api-contract §6, T8.
- `npm run build -w @masaha/shared` exit 0; `npm run lint` exit 0; `npm run typecheck` exit 0; shared
  `errors.unit.test.ts` `Tests  13 passed (13)`.

### C3 `ddb23d81` feat(subscriptions): list notices with extensions (49)
- T12–T15 (`subscriptions/closures/list.api.test.ts`) red before the code: `Tests  4 failed (4)` → green with the
  announcements files: `Test Files  3 passed (3)  Tests  17 passed (17)`. T10 gained "then it leaves the list"
  (`Tests  4 passed (4)`).
- **§12.2 check 4 ✔:** both routers at `manage.use('/announcements', …)`: `GET` reaches `closures`' (T12), `POST`
  `announcements'` (T1); no 404.
- **§12.2 check 2 ✔:** `npm run lint` exit 0 with `subscriptions/closures/` importing `announcements` (L2) and `users`
  (L1) through their `index.ts`.
- Q6 as built: `closuresAwaitingExtension` counts only closures started within the last 30 days; T14 proves one
  started 31 days ago is not counted.
- Interface detail: `announcements.page/counts/startedClosureIds` take the instant (`at`) from the caller, and
  `startedClosureIds` a `since` (the 30-day window is `closures.summary`'s, Q6), so one summary reads one instant.
- `npm run typecheck` exit 0; `check:links` "2667 links … all resolve".

### C4 `a95d9894` feat(directory): show a space's announcements (45)
- T16–T17 (`directory/page.api.test.ts`) red before the code: `Tests  3 failed | 8 passed (11)` (T16, T17, and the
  whole-page test that now expects `announcements: []`) → green `Tests  11 passed (11)`; the directory folder `Test
  Files  5 passed (5)  Tests  58 passed (58)` after `liveStatus.api.test.ts`'s list of the page's keys gained
  `announcements` (found by running the folder; a file C1 already touched). T10 gained "the public page" (the
  lifecycle file's `beforeEach` seeds the platform's settings, which the page reads): `Tests  4 passed (4)`.
- **§12.2 check 5 ✔:** `git grep PublicSpace apps/web/src` → one object literal typed by it, `apps/web/src/test/publicSpace.ts`;
  it gains `announcements: []`, nothing else. `npm run typecheck` exit 0. No worker-A PR is open (Q10: nothing to
  merge after).
- `PUBLIC_ANNOUNCEMENTS_MAX` lives in `@masaha/shared/directory` (D2); `announcements.publicOf(spaceId, take)` takes it
  from `directory` (L5), since `announcements` (L2) cannot import the directory's shared folder.
- `npm run lint` exit 0; `npm run typecheck` exit 0; `check:links` "2668 links … all resolve".

### C5 `5df1cefa` feat(occupancy): warn of a closure at check-in (46)
- T18 (`desk/checkIn.api.test.ts`) red before the code: `Tests  1 failed | 10 passed (11)` (the answer carried no
  `meta`) → green `Tests  11 passed (11)`. T18 also checks a subscriber's check-in (`POST …/check-ins`) answers
  `['SPACE_FULL', 'CLOSURE_IN_FORCE']`: the AC's "the subscription check-in reads the same warnings", proven in the
  same file (A5).
- `CLOSURE_IN_FORCE` by the `add-error-code` steps: shared `core/errors.ts` and `DESK_WARNINGS` (after
  `OUTSIDE_OPENING_HOURS`), both catalogues (Q1's Arabic «المساحة معلَنة مغلقة الآن، وسُجّل الحضور رغم ذلك.», English
  "The space is announced closed now; the check-in was recorded anyway."), api-contract §6 and the warnings' order.
- Documents: contract, data model (*Full warning*), conventions (the desk's check-in), `occupancy.md` (its
  `announcements` line now links the new document), `desk.md`, v1-mvp (step 10 *Built*, the rows, the managed
  *Built* sentence; its *Last Updated*), overview *Built*, `docs/README.md`'s map.
- `npm run lint` exit 0; `npm run typecheck` exit 0; `check:links` "2673 links … all resolve".

## 5. The head's verification (12.4), on `5df1cefa`, each once
- Free memory before the full lanes: 3,439,316 KB; no `vitest`/`tsc` of worker A running.
- `npm run lint` exit 0 · `npm run typecheck` exit 0 (after C5, on the same tree).
- `npm run test:unit` exit 0: shared `Test Files  22 passed (22)  Tests  253 passed (253)`; api `Test Files  64 passed
  (64)  Tests  864 passed (864)`; web `Test Files  115 passed (115)  Tests  918 passed (918)`.
- `npm run test:api` exit 0: `Test Files  82 passed (82)  Tests  1131 passed (1131)`.
- `npm run format:check` exit 0 "All matched files use Prettier code style!" · `npm run check:links` exit 0 "2673
  links in 179 documents and 1769 source files all resolve." · `npm run build -w @masaha/shared` exit 0.
- `git grep "#PRNUM"`: documents only (10 files). `git diff --stat origin/main -- apps/web`: the two `errors.ts` and
  `test/publicSpace.ts` only. `package.json`/`package-lock.json`: no diff. 55 files in all.
- **Not run locally (CI judges):** `test:component`, the web's `build`, `check:build`, `check:classes` (the web change
  is catalogue strings and one typed fixture line).

## 6. The breaks (12.5) — each: backup, one edit, the named test in its lane, restore from the backup (SHA-256 same), green
Script `scripts\brk.py` with `scripts\pr1-breaks.json`; outputs `breaks-unit.out`, `breaks-api.out`, `breaks-b18.out`.
- B1 `startsAt >= now` → U1 `AssertionError: expected 'UPCOMING' to be 'RUNNING'` · restored `Tests 1 passed`.
- B2 end-after-now dropped → U2 `Tests 2 failed | 2 passed (4)`, `expected null to deeply equal { endsAt: [ 'out_of_range' ] }` · restored 4 passed.
- B3 an edit checks an unchanged end → U2 `expected { endsAt: [ 'out_of_range' ] } to be null` · restored.
- B4 every sent field counted → U3 `expected { …(3) } to deeply equal { data: { …(2) }, …(2) }` · restored.
- B5 the create's refinement removed → U4 `expected null to deeply equal { endsAt: [ 'out_of_range' ] }` · restored.
- B6 (database, `masaha_b_test`) `DROP INDEX announcements_space_id_request_id_key` → D1 `promise resolved "{ id: 2, …}"
  instead of rejecting` · restore by the migration's `CREATE UNIQUE INDEX` first **refused**: the broken run left its two
  rows with one key (`Key (space_id, request_id)=(1, …) is duplicated`); `TRUNCATE "announcements" CASCADE` on
  `masaha_b_test` (every test resets it), then the index → `pg_indexes` shows the migration's definition;
  `db/schema.api.test.ts` `Tests 26 passed (26)`.
- B7 the create's audit removed → T1 `expected [] to deeply equal [ { actorId: 2, …} ]`.
- B8 `findByKey`'s answer skipped → T2 `expected [ 201, 500 ] to deeply equal [ 201, 201 ]`.
- B9 the space's lock removed → T2 `Error: 2 request(s) never waited on a lock`.
- B10 `requireIdempotencyKey` removed → T3 `expected { type: [ 'invalid_choice' ], …} to deeply equal { idempotencyKey: [ 'required' ] }`.
- B11 `can()` on `space.links` (not under the lock) → T5 `expected 201 to be 403`.
- B12 the router mounted outside `manage` (before the boundary) → T6 `expected 401 to be 404`.
- B13 the no-change branch removed → T7 `expected [ …(2) ] to deeply equal [ …(1) ]` (an audit line appears).
- B14 the upcoming check removed → T8 `expected 500 to be 409` (the dates `CHECK`).
- B15 the "started" branch removed → T9 `expected undefined to match object { … }`.
- B16 a hard `delete` → T10 `PrismaClientKnownRequestError` (the row gone).
- B17 `lockIn` without the space → T11 `expected 200 to be 404`.
- B18 the ended tab ordered by start → **stayed green first** (`Tests 1 passed`): my own test's defect — T12's two
  ended rows ordered the same by start ascending as by end descending. Fixed the data (the one that ended last
  started last), folded into C3 (`--fixup` + autosquash); B18 again → `AssertionError: expected [ 6, 7 ] to deeply
  equal [ 7, 6 ]` · restored `Tests 1 passed`. After the fold: `list.api.test.ts` `Tests 4 passed (4)`, `npm run
  lint` exit 0, `npm run typecheck` exit 0 (the fix touched that test file only; the head's lanes not re-run).
- B19 the count taken from the days → T13 `expected [ { id: 1, type: 'CLOSURE', …} ] to deeply equal [ ObjectContaining{…} ]`.
- B20 an upcoming closure counted as awaiting → T14 `expected { running: 2, upcoming: 1, …} to deeply equal {…}`.
- B21 the closures router outside `manage` → T15 `expected 404 to be 200`.
- B22 the public `endsAt` filter dropped → T16 `expected [ Array(5) ] to deeply equal [ Array(4) ]`.
- B23 the `take` removed → T17 `expected [ …(21) ] to have a length of 20 but got 21`.
- B24 `closedAt` for any running announcement (its `type: 'CLOSURE'` dropped) → T18 `expected { success: true, …} to not have property "meta"` (the outage warned).
- Every break: `restored: sha256 same`, the restored run exit 0. `git status --short` clean after (the fold aside).
- Heads after the fold: C3 `9c6a384c`, C4 `12b1d4ea`, C5 `05a6e42d` (C1 `b60907ac`, C2 `443b0705` unchanged).

## 7. The real run (12.6, PR 1) — API on 3321, `masaha_b_dev`, the demo space
- `curl.exe -s http://localhost:3321/health` → `{"status":"ok","db":"up",…}`.
- Read first with GETs (`scripts\precheck1.mjs`): the three demo accounts sign in; reception's space `1:masaha-demo`;
  public occupancy `AVAILABLE`; no announcement in any state; the page carries none.
- `node scripts\realrun1.mjs` exit 0, **ALL PASS** (output `scripts\realrun1.out`):
  precondition 200 · reception posts a `CLOSURE` starting now → 201 `RUNNING` · the same key → 201, the same id ·
  `GET ?state=RUNNING` → it, `extension: null` · anonymous `GET /spaces/masaha-demo` → it in `announcements` (no
  `state` field) · `GET /spaces/masaha-demo/occupancy` → `CLOSED` · reception checks a visitor in → 201, warnings
  `["CLOSURE_IN_FORCE"]` · its check-out → 200: **reception paid its quote's charge, 8 agorot, in cash** (the visit
  had a rate) · `PATCH` the text → 200 · `POST …/end` → 200 `ENDED` · the page no longer shows it · the live status
  not `CLOSED` · an upcoming `GENERAL` tomorrow → 201 `UPCOMING` · `POST …/start` → 200 `RUNNING` · `DELETE` → 204
  · again → 204 · `GET …/summary` → 200 `{"running":0,"upcoming":0,"ended":1,"closuresAwaitingExtension":1}` · the
  directory owner lists the demo space's announcements → 404 · posts there → 404.
- Audit (latest first): announcement.deleted, announcement.started, announcement.created, announcement.ended,
  announcement.edited, payment.recorded, visit.checkedOut, visit.checkedIn, announcement.created, checkIn.checkedOut.
- **Data the run wrote** (`masaha_b_dev`, demo space): the closure (ended now, its text edited) — it stays in the
  summary's `closuresAwaitingExtension` for 30 days; the general announcement (started, then deleted); the visit
  «زائر الإعلانات», checked in and out, and its 8-agorot cash payment; their audit lines.
- The API stopped by process id (tsx watch 23684, the server 26776, pino-pretty 18888); port 3321 free;
  `server.log` deleted.

## 8. The number, the push, the PR (12.7)
- Next number: `gh pr list --state all --limit 1` → 111; the issues API → 111; so **#112**.
  `scripts\prnum-pr1.sh 112` → `PRNUM OK #112 fdae748b (was 05a6e42d)` (backup branch `backup/announcements-pre-prnum`,
  local only); the rewrite changed only the number (10 documents, 40 lines). `git grep "#PRNUM"` empty.
- After the rewrite: `check:links` exit 0 (2673 links), `format:check` exit 0.
- Commits after the rewrite: `e06ab057` C1 · `4ec423b1` C2 · `e11312dc` C3 · `92aa1b86` C4 · `fdae748b` C5.
- `git push -u origin feat/announcements` ✔; `gh pr create` → https://github.com/Basel-Ghonaim/masaha/pull/112 (the
  number matches), labels `feat`, `area:api`, `area:docs`, `area:web` (all existed); body `scripts\pr1-body.md`.
- **Open PRs:** worker A's #111 `feat/home-about` (opened during this work; head `03633534`, CLEAN). Shared files:
  documents only — `docs/README.md`, `docs/features/directory.md`, `docs/project/overview.md`; no code, no
  `PublicSpace` fixture (Q10's case does not arise). `git merge-tree --write-tree HEAD 03633534` → clean. Either may
  merge first.

## 9. `OPEN_DECISIONS.md` point 2 — not written (a departure, for the owner)
The plan (§12.8) has PR 1's report update `C:\dev\masaha\workspace\_SHARED\OPEN_DECISIONS.md` point 2; the exec
prompt (§1.10) allows writing nothing outside this folder's report and `scripts\`. The exec prompt is the newer
instruction, so the file is **unchanged**. The line to append to point 2, as the plan words it:

> **settled (#112, 2026-10-24):** reception posts a closure; the owner learns of it in the app only — the managed
> list's extension state per closure and the summary's `closuresAwaitingExtension`, which the overview (step 12)
> reads through `subscriptions`' `closures.summary`; no email.

## 10. CI, CLEAN, conflicts (12.8)
- `gh pr checks 112 --watch` exit 0 on the pushed head `fdae748b` (= `git rev-parse HEAD`): build, check:classes,
  check:links, format:check, lint, test:api, test:component, test:unit, typecheck — all `pass`; CodeRabbit `pass`
  ("Review rate limited", so no review from it).
- `gh pr view 112` → `mergeStateStatus: CLEAN`, 55 files.
- While CI ran, worker A's #111 merged (`main` at `2a7bd25b`). `git merge-tree --write-tree HEAD origin/main` → clean,
  and GitHub still says CLEAN: not rebased (a CLEAN PR is never rebased). No other open PR.
- `git status --short` clean; port 3321 free; the API stopped.

## 11. Departures and notes
1. **The migration's file was made by `migrate diff`, not `migrate dev --create-only`:** the one `--create-only` run
   was refused as non-interactive (SUBSCRIPTIONS hit the same); Prisma's diff was hand-edited into D12's SQL.
2. **The demo seed's closure** (`demoDirectory.ts`) gained a key: A10 said the seed holds no announcement; check 3's
   rule (add the extra inserts and say so) covered it.
3. **`liveStatus.api.test.ts`'s list of the page's keys** gained `announcements` (C4): a test the plan did not name,
   in a file C1 already touched.
4. **T10 asserts the public page and the list too** (C3, C4), and the lifecycle file seeds the platform's settings
   the page reads.
5. **T18 also checks a subscriber's check-in** (the AC's "the subscription check-in reads the same warnings"), in the
   same file.
6. **B18 stayed green first**: my own test's data; fixed and folded into C3, then red (§6).
7. **B6's restore needed the test table cleared** first (the broken run's duplicate rows), on `masaha_b_test` only.
8. **`OPEN_DECISIONS.md` not written** (§9): the exec prompt's write limit wins over the plan's §12.8.
9. **Interfaces:** `announcements.page/counts/startedClosureIds` take the instant from their caller and
   `startedClosureIds` a `since` (Q6's 30-day window is `closures.summary`'s); `announcements.publicOf(spaceId, take)`
   takes the 20 from `directory`, where `PUBLIC_ANNOUNCEMENTS_MAX` lives (D2).
- No new finding (none numbered 150).
