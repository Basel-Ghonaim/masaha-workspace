# ANNOUNCEMENTS PR 4 — `feat/closure-extension` — the executor's report

## Preconditions and §12.1

- `C:\dev\masaha\app-b` was detached at `origin/main` = `1a89da5d` (#121), clean.
- Read: `0_CARRIED_FROM_121.md` whole; review PR 3 findings 1–5; the plan's parts named by the exec prompt;
  `4_REPORT_PR3.md`'s departures.
- Base diff `befd96f9..origin/main` on PR 4's code files: only the merged #102–#121 changes the prompt names
  (schema, `announcements/`, `subscriptions/closures/`, `constraintCodes.ts`, shared `core/` and `announcements/`).
  No other change to a PR 4 code file.
- Supervisor's checks re-read: `ClosureExtension` / `SubscriptionExtension` in `schema.prisma` (no `request_id` yet);
  `constraintCodes.ts` holds four ledger lines, no `announcements_closure_extended`.
- **`daysFrom`:** `apps/api/src/modules/subscriptions/subscriptionStatus.ts:27`, private:
  `(Date.parse(to) − Date.parse(from)) / 86 400 000` on `YYYY-MM-DD` at UTC midnight — whole calendar days from
  `from` to `to`, the plan's meaning. Decision: move it to `packages/shared/src/core/gazaTime.ts` (exported, U1),
  imported by `subscriptionStatus.ts` (C2). A departure, stated.
- **Lock reuse:** `announcements.repository.lockIn(spaceId, id, tx)` (`SELECT … FOR UPDATE`, then the row, `null`
  when not the space's or deleted). `lockClosure` will be `lockIn` plus "type is `CLOSURE`", no second lock statement.
- Open PRs: #122 `feat/customers-file` (`358765e3`) only.
- Branch `feat/closure-extension` created from `origin/main` (`--no-track`) at `1a89da5d`.
- `npm run build -w @masaha/shared` → exit 0 (`scripts\pr4-shared-build.txt`).

## First stop — Docker Desktop was not running (resolved)

- `docker start masaha-postgres-1` first failed: `failed to connect to the docker API at
  npipe:////./pipe/dockerDesktopLinuxEngine … The system cannot find the file specified.`; `prisma migrate status` →
  `P1001`. Stopped and asked; the owner started Docker; the work continued.
- `docker start masaha-postgres-1` → `masaha-postgres-1`. `prisma migrate status` → `Database schema is up to date!`
  (`scripts\pr4-migrate-status.txt`). Both `masaha_b_dev` and `masaha_b_test` at `20261025112542_data_report_rules`
  (read in `_prisma_migrations`). `apps/api/.env` names `masaha_b_dev`/`masaha_b_test` (2 matches), `PORT=3321`.

## §12.2 check 3 — the demo data ✔

The demo space `masaha-demo` (id 1; `demo-owner` OWNER, `demo-reception` RECEPTION). Gaza today `2026-10-26`; a
closure started two days ago covers `2026-10-24 … 2026-10-26`. Read-only `SELECT`s on `masaha_b_dev`:

| Subscription | starts_on | ends_on | ended early | Covered |
|---|---|---|---|---|
| 1 | 2026-10-18 | 2026-11-07 | no | ✔ |
| 2 | 2026-10-20 | 2026-11-02 | no | ✔ |
| 3 | 2026-10-14 | 2026-11-13 | no | ✔ |
| 4 | — | — (no end) | no | ✘ (no end) |
| 5 | 2026-10-25 | 2026-11-23 | no | ✔ |

Four covered (1, 2, 3, 5). The space has no announcement yet; `closure_extensions` is empty.

## The migration `closure_extension_key` (phase 1)

- Schema: `ClosureExtension` gains `idempotencyKey String @unique @map("request_id") @db.Uuid` with a doc comment
  as `Announcement`'s key.
- `npm exec -w @masaha/api -- prisma migrate dev --create-only --name closure_extension_key`, run **once** → exit 1,
  `Prisma Migrate has detected that the environment is non-interactive, which is not supported.`; `ls` showed no new
  folder (`scripts\pr4-create-only.txt`).
- Fallback, as PR 2 did: `npx prisma migrate diff --from-config-datasource --to-schema prisma/schema.prisma --script`
  (from `apps/api`; `--to-schema-datamodel` was removed in this Prisma) → exit 0 (`scripts\pr4-diff.sql`):
  `ADD COLUMN "request_id" UUID NOT NULL;` and `CREATE UNIQUE INDEX "closure_extensions_request_id_key"`. Edited into
  D12's form, the folder named by the UTC time.
- **Path:** `apps/api/prisma/migrations/20261026114022_closure_extension_key/migration.sql`. Not applied (`migrate
  status`: "Following migration have not yet been applied"), not committed. No PR number in it.

```sql
-- AlterTable
ALTER TABLE "closure_extensions" ADD COLUMN     "request_id" UUID;

-- Rows made before the key (tests, the dev data) get one of their own.
UPDATE "closure_extensions" SET "request_id" = gen_random_uuid() WHERE "request_id" IS NULL;
ALTER TABLE "closure_extensions" ALTER COLUMN "request_id" SET NOT NULL;

-- CreateIndex
CREATE UNIQUE INDEX "closure_extensions_request_id_key" ON "closure_extensions"("request_id");

-- Decision 6 (2026-10-21): once a closure's subscriptions were extended, it keeps its type and its start, is
-- never deleted, and its end only comes earlier (S3: a running closure must still be able to end). Its text
-- may change. The database owns the rule: `announcements` cannot read this table (conventions §7).
CREATE FUNCTION "announcements_guard_extended"() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF EXISTS (SELECT 1 FROM "closure_extensions" WHERE "announcement_id" = OLD."id") AND (
       NEW."type" <> OLD."type" OR NEW."starts_at" <> OLD."starts_at"
       OR NEW."deleted_at" IS DISTINCT FROM OLD."deleted_at"
       OR (NEW."ends_at" IS DISTINCT FROM OLD."ends_at"
           AND NOT (NEW."ends_at" IS NOT NULL AND (OLD."ends_at" IS NULL OR NEW."ends_at" < OLD."ends_at")))) THEN
    RAISE EXCEPTION 'announcements_closure_extended: closure % had its subscriptions extended', OLD."id"
      USING ERRCODE = 'check_violation', TABLE = 'announcements', CONSTRAINT = 'announcements_closure_extended';
  END IF;
  RETURN NEW;
END;
$$;
CREATE TRIGGER "announcements_guard_extended"
  BEFORE UPDATE OF "type", "starts_at", "ends_at", "deleted_at" ON "announcements"
  FOR EACH ROW WHEN (OLD."type" = 'CLOSURE') EXECUTE FUNCTION "announcements_guard_extended"();
```

- **Names checked against the code:** the columns (`type`, `starts_at`, `ends_at`, `deleted_at`,
  `closure_extensions.announcement_id`) and the enum value `CLOSURE` are the schema's;
  `db/checkViolation.ts` reads the message's leading `name: ` (`/^([a-z0-9_]+): /`) on SQLSTATE 23514, so
  `announcements_closure_extended:` is read as check 1 needs.
- **SQL departures from D12:** none. (The method — `migrate diff` instead of `--create-only` — is the allowed
  fallback, stated above.)

**Phase 1 ends here**, waiting for `3_EXEC_PROMPT_PR4_APPROVAL.md`.

## Phase 2

- `3_EXEC_PROMPT_PR4_APPROVAL.md` read whole; `AUTONOMY_2026-10-25.md` read. `git merge --ff-only origin/main` →
  `3855e37f` (#122), the two uncommitted paths kept.
- `npm run db:migrate` → `Applying migration 20261026114022_closure_extension_key` … `Your database is now in sync
  with your schema.` No second migration proposed. `prisma generate` → `ClosureExtension.ts` names `idempotencyKey`.
  `masaha_b_test` migrated by the API lane's setup (the first API run's refusals prove the trigger there).

### C0-1 — `de75b3d3` `fix(favorites): read the listing before the lock` (48)
- Item 1: `isListed` read before `runInTransaction`; inside: lock, already saved → 204, `!listed` → not_found,
  ceiling, insert. `favorites.md` *Save* and a history line.
- Item 4 (a): T1 extended (saved, hidden, saved again → 204, one row). Break C0a (the listed check moved ahead of
  "already saved"): `× … again 204 with one row, even once hidden` / `AssertionError: expected 404 to be 204`;
  restored sha256 same; `Tests 1 passed | 6 skipped (7)`.
- Item 4 (b): T8 (directory) gains an inactive-area favourite → `listed: false` with its name. Break C0b (the
  listing's area condition `OR TRUE`): `× the favourites, whole, … inactive-area one listed false with its name` /
  `AssertionError: expected [ … ] to deeply equal [ … ]`; restored; `Tests 1 passed | 3 skipped (4)`.
  (Both written green on the code as it was — the order already held — so the red is the break's; `scripts\pr4-c0-breaks.out`.)
- The two files: `Tests 11 passed (11)`; lint 0, typecheck 0 (after C1's test-key edits, below), check:links 0.

### C0-2 — `210d8879` `docs(favorites): date the decisions and fixes` (45)
- Items 2, 3, 5: "2026-10-25, " before `#121` on favorites.md's five decisions, the contract's Built line, §4
  exception, §6 line, conventions' header and §9 line; directory.md's Authority names the favourites and links
  `api-contract.md#favourites`; "then the higher space id first" in the contract and favorites.md. lint 0, typecheck 0,
  check:links 0.
- `0_CARRIED_FROM_120.md` item 4 (`apps/api/test/app.ts`): no commit touches that file → left, as allowed.

### C1 — `311181b0` `feat(db): guard an extended closure` (35)
- Migration as approved; schema key; `constraintCodes.ts` `announcements_closure_extended`; `CLOSURE_EXTENDED` in
  shared and both catalogues (Q1's Arabic word for word); D1–D2 in `db/closureExtensions.api.test.ts`.
- The extension inserts of `db/schema.api.test.ts` **and `subscriptions/closures/list.api.test.ts`** (not in §7's
  list: it inserts extensions too, PR 1's) gain `idempotencyKey: randomUUID()` — typecheck failed without it.
- D1–D2 written after the migration was applied to `masaha_b_test` (the lane's setup ran it before), so their red is
  B5–B6 (`scripts\pr4_dbbreaks.sh`, `pr4-dbbreaks.out`):
  - B5 drop the trigger → `× refuses a new type, start, deletion or later end …` / `AssertionError: promise resolved
    "{ id: 1, spaceId: 1, …(9) }" instead of rejecting`; restored by the migration's `CREATE TRIGGER`; `Tests 2 passed (2)`.
  - B6 drop `closure_extensions_request_id_key` → `× an extension's key is unique` / `promise resolved … instead of
    rejecting`. The restore first failed (`could not create unique index … Key (request_id)=(…) is duplicated`: the red
    run's own rows were left); the test database's extension rows deleted (each test resets them anyway), then the
    migration's `CREATE UNIQUE INDEX` → index back; `Tests 2 passed (2)`.
- The three test files: `Tests 32 passed (32)`. lint 0, typecheck 0, check:links 0, shared build 0.
- Docs: data model (Idempotency, *Constraints*: the key, the trigger), contract (PATCH/DELETE errors, §6), conventions
  (*The ledger's rules*: the trigger), announcements.md (flow, decision, history).

### C2 — `5da2c314` `feat(subscriptions): preview a closure's extension` (50)
- U1 red: `× counts calendar days across a month, a year and a leap day` / `TypeError: daysFrom is not a function`;
  green after the move: `Tests 6 passed (6)`. `daysFrom` moved (not copied) from `subscriptionStatus.ts` into
  `packages/shared/src/core/gazaTime.ts` (exported; same meaning, on `utcDay`); `subscriptionStatus.ts` imports it;
  the subscriptions unit tests `Tests 25 passed (25)`.
- U2 red: `Error: Cannot find module './closureSpan.ts'` (test before the file); green `Tests 11 passed (11)` with
  `subscriptionStatus.unit.test.ts`. B2/B3 run as their own breaks.
- T1, T7 (its read part), T8 red: `× …` three, `AssertionError: expected 404 to be 200` / `404 to be 409` /
  `404 to be 200` (`Tests 3 failed (3)`); green with `list.api.test.ts`: `Tests 7 passed (7)`.
  One fix of my own test before green: the closure ending at Tuesday's midnight covers 4, not 5 (the subscription
  starting Tuesday drops out) — the expectation was wrong, not the code.
- `closureIn` (announcements) reads the space's `CLOSURE`, not deleted (`findClosure`); the preview: applied first
  (answered with how many it moved), then upcoming → `ANNOUNCEMENT_NOT_STARTED`, then the span and `coveredCount`.
- Shared: `EXTENSION_MAX_DAYS`, `ExtensionPreview`. Docs: contract (the type, the route, the covered rule), data model
  (*Derived values*: the covered days).
- lint 0, typecheck 0, check:links 0, shared build 0.

### C3 — `721578c6` `feat(subscriptions): extend after a closure` (43)
- U3 red: `× days are whole, 1 to 365` / `TypeError: Cannot read properties of undefined (reading 'parse')`; green
  `Tests 5 passed (5)`.
- T2–T7 (POST parts), T9–T11, T12–T13 red (`scripts\pr4-c3-red.txt`): `Tests 11 failed | 2 passed (13)` —
  `expected 404 to be 201` ×5, `404 to be 403`, `404 to be 409`, `request(s) never waited on a lock` ×4 (no route yet).
  Green with the closures folder, the announcements folder and `db/closureExtensions`: `Tests 33 passed (33)`.
- **§12.2 check 1 ✔:** the trigger's error answers `409 CLOSURE_EXTENDED` (T12), never a 500.
  **Check 2 ✔:** `"ends_on" + ${days}::integer` is a date: T2's hand-counted ends (`2026-11-30` + 4 → `2026-12-04`, …).
- Code: `lockClosure` = `repository.lockIn` + the `CLOSURE` check (no second lock statement); the closures repository
  gains `lockCovered`, `moveEnds`, `findByKey`, `isExtended`, `createExtension` (with the links); the service
  `extend`; the route `requireCan('subscriptions.extendAfterClosure')` → `requireIdempotencyKey` → `validate`; `app.ts`
  gives `closures` `runInTransaction`, `audit`, `spaces`.
- `CLOSURE_ALREADY_EXTENDED` in shared and both catalogues (§13 Q1's lines); `extendSubscriptionsSchema`,
  `ClosureExtension`.
- Docs: contract (POST, the type, §6), data model (decision 4, *ClosureExtension*), conventions (§6, §7 row, §13), security,
  ADR 0009 (row + *Revised*), subscriptions.md, announcements.md, v1-mvp (step 10 *Built*, the row), overview (line 62,
  *Built*).
- lint 0, typecheck 0 (after the code), check:links `2855 links in 191 documents and 2020 source files all resolve.`

## §12.5 — the breaks (`scripts\brk.py pr4-breaks.json`, output `pr4-breaks.out`; B5–B6 above)

Each: backup, one edit, the named test red, restored from the backup (sha256 same), green again.

| B | Edit | Red line |
|---|---|---|
| B1 | `daysFrom` `+ 1` | `expected 1 to be +0` |
| B2 | dates by UTC (`toISOString().slice(0, 10)`) | `expected '2026-11-06' to be '2026-11-07'` |
| B3 | `endsAt` without `− 1 ms` | `expected { firstDay: '2026-11-05', …(2) } to deeply equal …` |
| B4 | `.max(EXTENSION_MAX_DAYS)` removed | `expected null to deeply equal { days: [ 'out_of_range' ] }` |
| B7 | `ends_on >= first` dropped | T1 `expected { … } to deeply equal { … }` |
| B8 | ends moved by the proposal (3), not the days (4) | T2 `expected '2026-12-03' to be '2026-12-04'` |
| B9 | `ended_at IS NULL` dropped | T3 `expected '2026-12-02' to be '2026-11-30'` |
| B10 | `starts_on <= last` dropped | T3 `expected '2026-12-13' to be '2026-12-11'` |
| B11 | the space filter dropped | T3 `expected '2026-12-02' to be '2026-11-30'` |
| B12 | `requireCan('subscriptions.extendAfterClosure')` removed | T4 `expected 422 to be 403` |
| B13 | `findByKey` skipped | T5 `expected 409 to be 201` |
| B14 | the space's lock removed | T6 `Error: 2 request(s) never waited on a lock` |
| B15 | the started check removed | T7 `expected 201 to be 409` |
| B16 | `applied` not read | T8 `expected { … } to deeply equal { … }` |
| B17 | the covered set locked before `spaces.lock` | T9 `expected 500 to be 201` (the request and the test's transaction deadlock: the request held the subscription's row the test then updates) |
| B18 | the closure read before the lock | T10 `expected { announcementId: 1, days: 4, …(3) } to match object { subscriptions: 4 }` |
| B19 | `can()` on `space.links` | T11 `expected 201 to be 403` |
| B20 | the translation line removed | T12 `expected 500 to be 409` |

All 18 restored: `restored: sha256 same`, each `restored run exit 0`. `git status --short` empty afterwards.

## §12.4 — the head (`721578c6`), each once

- Free memory before the lanes: 6 734 964 KB; no `vitest`/`tsc` of worker A's running.
- `npm run lint` → exit 0. `npm run typecheck` → exit 0.
- `npm run test:unit` → exit 0: `Test Files 24 passed (24) / Tests 261 passed (261)`; `Test Files 69 passed (69) /
  Tests 877 passed (877)`; `Test Files 135 passed (135) / Tests 978 passed (978)` (the three workspaces).
- `npm run format:check` → `All matched files use Prettier code style!`; `npm run check:links` → `2855 links in 191
  documents and 2020 source files all resolve.`; `npm run check:conflicts` → `No conflict markers found.`
- `git grep '#PRNUM'` → documents only (9 files, none in the migration); `git diff --stat origin/main -- apps/web` → the
  two `errors.ts` only; `-- package.json package-lock.json` → empty. **Files: 42.**
- `npm run test:api` (run 1, background, no command timeout) — **killed for low memory**: the harness stopped it
  ("the system was critically low on memory"); vitest's workers had died at start-up, `Worker exited unexpectedly with
  exit code 3221225794 during starting state` (0xC0000142), after `Test Files 5 passed (5) / Tests 255 passed (255)`;
  no test failed. Free memory afterwards 3 549 116 KB (not quieter).
- `npm run build -w @masaha/shared` → exit 0.

## §12.6 — the real run (API on 3321, `masaha_b_dev`, `scripts\realrun4.mjs`, output `realrun4.out`)

`GET /health` → `{"status":"ok","db":"up",…}`. Space 1 (`masaha-demo`), reception user 3, owner user 2. The covered set,
by the rule written by hand in SQL for `2026-10-24..2026-10-26`: subscriptions 1, 2, 3, 5 (ends 11-07, 11-02, 11-13,
11-23).

| Case | Answer |
|---|---|
| reception posts a closure started two days ago, ending in an hour | 201 `RUNNING` (closure **2**) |
| the preview (reception) | 200, `proposedDays: 3`, `2026-10-24..2026-10-26`, `subscriptions: 4`, `applied: null` |
| reception extends | 403 |
| the owner extends `{ days: 3 }` with key E | 201, `subscriptions: 4` |
| E again | 201, the same body |
| another key | 409 `CLOSURE_ALREADY_EXTENDED` |
| the ends | 1 → 2026-11-10, 2 → 2026-11-05, 3 → 2026-11-16, 5 → 2026-11-26 (each +3) |
| `PATCH { type: GENERAL }` | 409 `CLOSURE_EXTENDED` |
| `DELETE` | 409 `CLOSURE_EXTENDED` |
| `POST …/end` | 200 `ENDED` |
| `subscription_extensions` | extension **1**, rows for subscriptions 1, 2, 3, 5 |

`ALL PASS`, exit 0. Audit of closure 2: `announcement.created`, `closure.subscriptionsExtended`, `announcement.ended`.
**Data changed on `masaha_b_dev`:** announcement 2 (posted, then ended now); closure extension 1 (3 days, by the owner);
`subscription_extensions` (1, 1), (1, 2), (1, 3), (1, 5); subscriptions 1, 2, 3, 5's `ends_on` +3 days; the audit's
three entries. The server stopped by its process ids (tsx watch 30492, server 27868, pino-pretty 9924); port 3321 free.
The background task reported exit 127 — the effect of stopping it, after the run. `server.log` deleted.
- `npm run test:api` (run 2, the one re-run the memory rule allows, after worker A's component run ended; free memory
  6 428 224 KB) → exit 0: `Test Files 95 passed (95) / Tests 1224 passed (1224)`, `Duration 552.49s`
  (`scripts\pr4-head-api2.txt`). `masaha_b_test` at 29 migrations (the new one applied by the lane's setup).

## §12.7 — `#PRNUM`, push, PR

- `gh pr list --state all --limit 1` just before → `122` (no PR opened meanwhile); next **#123**.
- `scripts\prnum-pr4.sh 123` → `PRNUM OK #123 ff8743c8 (was 721578c6)`: 9 documents, 25 lines, only the number
  changed; the migration untouched (no number in it). Backup branch `backup/closure-extension-pre-prnum` (at `721578c6`).
- After the rewrite: `check:links` 0, `format:check` 0.
- `git push -u origin feat/closure-extension` → new branch; head `ff8743c89b769c7808977d2967c766ed5fe16a40`.
- `gh pr create --assignee @me`, labels `feat`, `area:api`, `area:docs`, `area:web`, title `feat(subscriptions): extend
  them after a closure` (48) → **https://github.com/Basel-Ghonaim/masaha/pull/123**; the number equals the one written.

| Commit | Subject (chars) |
|---|---|
| `454e16ba` | `fix(favorites): read the listing before the lock` (48) |
| `193797df` | `docs(favorites): date the decisions and fixes` (45) |
| `633dabcd` | `feat(db): guard an extended closure` (35) |
| `ecf5ef1e` | `feat(subscriptions): preview a closure's extension` (50) |
| `ff8743c8` | `feat(subscriptions): extend after a closure` (43) |

## §12.8 — conflicts

No other PR open (#122 merged before the branch was brought up): nothing to merge-tree against.

## §12.8 — CI and CLEAN

On the pushed head `ff8743c89b769c7808977d2967c766ed5fe16a40` (= `git rev-parse HEAD`): lint pass 1m37s · typecheck
pass 59s · test:unit pass 2m22s · test:api pass 7m48s · test:component pass 19m53s · build pass · check:classes pass ·
check:conflicts pass · check:links pass · format:check pass · CodeRabbit pass. `mergeStateStatus` **CLEAN**. Files 42.
Not merged, not rebased.

## Departures from the plan

- `daysFrom` **moved** from `subscriptionStatus.ts` (private) into `packages/shared/src/core/gazaTime.ts`, exported, and
  imported back (D10 said "gains"): one function, not a copy. Approved in the approval file.
- `lockClosure` = `repository.lockIn` + the `CLOSURE` check: no second lock statement. Approved.
- The migration made by `prisma migrate diff --from-config-datasource --to-schema --script` (the one `--create-only`
  run refused as non-interactive), as allowed. Approved.
- D11's repository names: `isExtended` for `findFor`; `createExtension` writes the extension and its links
  (`linkSubscriptions` folded in), still two statements.
- `subscriptions/closures/list.api.test.ts` gains `idempotencyKey` on its two extension inserts (not in §7's list; it
  inserts extensions since PR 1). +1 file.
- T9 inserts, while the extension waits, a subscription that **is** covered (starting on the last day) instead of a
  renewal starting after the last day, which is never covered and so proves nothing about the race; the early end of a
  covered one is as planned.
- U2's and D1–D2's red: U2 by "Cannot find module" (the test before the file); D1–D2 were written after the lane's setup
  had applied the migration to `masaha_b_test`, so their red is B5–B6 (each seen red).
- The plan's `OPEN_DECISIONS.md` line ("the extension built (#123)") is **not written**: the exec prompt (§1.6) allows
  writing only this report and `scripts\` outside the repository. The supervisor may add it.
- `apps/api/src/app.ts` (the source, not `test/app.ts`) changed for the closures service's new dependencies;
  `0_CARRIED_FROM_120.md` item 4 stays open.

## Decisions taken without the owner

1. **The preview of an applied extension** — met: D11 says "applied → `{ …span, proposedDays, subscriptions: count,
   applied }`", leaving `subscriptions` ambiguous (counted now, or moved). Options: count the covered set again now; or
   answer how many it moved. Chose **how many it moved** (the links' count), with the span and proposal recomputed at
   now, so the preview matches the list's `extension.subscriptions` and a later subscription never reads as moved. Undo:
   in `closures.service.ts` `preview`, call `coveredCount` in the applied branch too (and T8's expectation).
2. **The API lane killed for low memory** — the harness stopped run 1 (workers exited 0xC0000142 at start-up, no test
   failed). The owner's memory rule allows one re-run when quieter, which the harness's own note advised against
   doing unasked; I followed the owner's written rule: waited for worker A's component run to end (free memory 6.4 GB),
   re-ran once → green. CI's test:api on the head is green too. Undo: none needed.
3. **B6's restore** — the migration's `CREATE UNIQUE INDEX` failed on the red run's leftover duplicate rows on
   `masaha_b_test`. Deleted that test database's extension rows (every API test resets them anyway), then restored the
   index from the migration's statement. Undo: none needed (test database only).

## Leftovers

- Local branch `backup/closure-extension-pre-prnum` (at `721578c6`, before `#PRNUM` → `#123`). Kept for the owner.
- No rebase in progress (no `rebase-*` directory in the worktree's git dir). `git status --short` clean.
- API stopped by process id; port 3321 free. No new finding recorded (151+ unused; note: findings 162–163 exist on
  main since #122, so a next finding would take 164).
