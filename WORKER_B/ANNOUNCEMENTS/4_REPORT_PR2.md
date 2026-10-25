# ANNOUNCEMENTS PR 2 — `feat/data-reports` — the executor's report

Written as the work goes. Scripts and outputs: `C:\dev\masaha\workspace\WORKER_B\ANNOUNCEMENTS\scripts\` (`pr2-*`, `c0-*`, `p2c*-*`).

## Preconditions and §12.1

- `C:\dev\masaha\app-b` detached at `origin/main` = `7f724dd5` (Merge #118), clean. ✔
- PR 1 (#112), PAYMENTS (#114), DESK_API (#118) merged. ✔
- `git diff --name-status befd96f9 origin/main` (551 entries) read against PR 2's code files: `schema.prisma`,
  `app.ts`, `packages/shared/src/core/errors.ts`, the two web `errors.ts`, `spaces.service.ts` changed only by
  the merged items the exec prompt names (SUBSCRIPTIONS, PR 1, #114, #117/#118: `standardPrice`, `stayEnd` added
  to `spaces.service.ts`); `spaces.repository.ts`, `data-reports/` untouched. Nothing contradicts the plan. ✔
- Open PRs: **none** (`gh pr list --state open` empty) — worker A's DESK_SCREENS PR 2 not open. ✔
- `0_CARRIED_FROM_118.md` present → C0 (items 1–5).
- Branch `feat/data-reports` from `origin/main` (`--no-track`). `docker start masaha-postgres-1` ✔.
  `apps/api/.env` names `masaha_b_dev`, `masaha_b_test`, `PORT=3321` (by pattern) ✔.
- `npm run build -w @masaha/shared` exit 0. `prisma migrate status` (masaha_b_dev): "Database schema is up to
  date!" (27 migrations); `masaha_b_test`'s last migration `20261025081716_session_activity` ✔.
  `data_reports` on `masaha_b_dev`: 0 rows (A10 holds).

## §12.2 first checks (PR 2)

- 2. `users.lockAccount(id: number, tx: Tx): Promise<Account | null>` — the session lock, then the account ✔.
- 3. `publicListing.upTo(filter, ceiling)`: `verifiedIds` only **marks** (prices shown, `verifiedOnly`); with
  `verifiedIds: []` and no price filter it filters nothing; `onlyIds` filters ✔ (proven by T8).
- 1. and 4.: below, when their code exists.

## C0 — carried from #118

- Item 1 (`idle.api.test.ts`, "renews nothing on a refresh…"): green on the code `7 passed (7)`; **break C0-1**
  (`issueInFamily` writes `lastActivityAt = at`): red — `AssertionError: expected '2026-10-21T07:10:00.000Z' to be
  '2026-10-21T07:00:00.000Z'`, `1 failed | 6 passed (7)`; restored (sha256 same), `7 passed (7)`.
- Item 4 (`test/app.ts` `signAccess` `lastActivityAt: FAR_AHEAD`): no test of its own (a helper); the idle file
  green with it.
- Item 2 (`subscribe.api.test.ts`, "a shift's published price is the one of that shift…"): green `15 passed (15)`;
  **break C0-2** (`findStandard` drops `shiftId` from its `where`): red — `AssertionError: expected { id: 2, … } to
  match object { priceAgorot: 25000, shiftId: null }` (the price with no shift answered the shift's row; with the
  break `findFirst` took the shift's row for both keys), `1 failed | 14 passed (15)`; restored (sha256 same), green.
- Item 3: ADR 0003's 2026-10-25 line → "the guard refuses an idle one (401 `SESSION_IDLE`) and the refresh ends it";
  `security.md`'s *Idle (reception)* row: "(a soft-deleted space's links count, as for `OWNER`)"; its *Last Updated*
  2026-10-25.
- Item 5: findings **170** and **171** (files + index lines under *Open*). `check:links` exit 0.

| sha | subject (chars) |
|---|---|
| `8b40f4b3` | `test(auth): prove a refresh renews no idle clock` (48) — items 1, 4 |
| `045f09eb` | `test(desk): copy a shift's published price` (42) — item 2 (the suggested subject was 52: shortened) |
| `b52bbc1f` | `docs: say the guard refuses an idle session` (43) — items 3, 5 |

After the three: `npm run lint` exit 0; `npm run typecheck` exit 0.

## The supervisor's autonomy message (2026-10-25)

During C1 a message from the main supervisor's session pointed to
`C:\dev\masaha\workspace\_SHARED\AUTONOMY_2026-10-25.md` (read whole): for the next hour, decisions where the
prompt says "stop and ask" are taken by the executor and recorded under **Decisions taken without the owner**;
the hard limits stay. Followed from here on.

## Decisions taken without the owner

(none yet that needed one — departures within the plan's own allowance are listed under *Departures*)

## Departures

- `spaces.namesWithDeleted` is added in **C1**, not C2: the create's answer (`MyReport`) needs the space's slug
  and names already.
- C0's second subject shortened (52 → 42 chars).
- The migration: `migrate dev --create-only` ran **once** and refused (non-interactive, exit 1, no folder made);
  the SQL is `prisma migrate diff --from-config-datasource --to-schema prisma/schema.prisma --script`
  (masaha_b_dev was up to date), the folder `20261025112542_data_report_rules` made by hand, D12's SQL appended,
  read, then `npm run db:migrate` (applied to masaha_b_dev; masaha_b_test by the API lane's setup).
- §12.2 check 1: Prisma refused `where: { status: OPEN }` (an enum literal) and accepted the plan's string form
  `where: { status: "OPEN" }`; the migration writes `WHERE ("status" = 'OPEN')` ✔.
- A `SpacesService` fake in `space-links.service.unit.test.ts` gains `namesWithDeleted` (one line): the type
  change breaks it otherwise.
- `createdAt` of a report is written from the one clock (`now` added to the service's deps; the plan's deps list
  did not name it): the first green run showed the database's time, not the test clock.

## C1 — `6dd2f295` `feat(data-reports): report a space's wrong data` (47)

- U1 red: `Error: Cannot find module './requests.ts'` (`Test Files 1 failed`); green `Tests 3 passed (3)`.
- D1–D3 (`db/dataReports.api.test.ts`): green `3 passed (3)` — the API lane's setup applied
  `20261025112542_data_report_rules` to masaha_b_test ("Applying migration … All migrations have been successfully
  applied"). Proven by the database breaks B3–B5.
- T1–T5 red: `4 failed` of 5 (`expected 404 to be 201`; the race `2 request(s) never waited on a lock`); T2 passed
  on 404 alone (proven by B7). Green after the code: `Tests 5 passed (5)`.
  (On the way: `waitingOnLock({ on: 'users' })` never matches a row-lock wait — it reads relation locks — so the
  test uses `{ count: 2 }`, as every other race test does.)
- §12.2 check 4: `vitest --project api src/modules/directory` → `Test Files 5 passed (5)`, `Tests 58 passed (58)` ✔.
- §12.2 check 2: `npm run lint` exit 0 with `data-reports` importing `spaces`, `users`, `lookups` ✔.
- `npm run lint` exit 0; `npm run typecheck` exit 0; `check:links` exit 0 ("2763 links … all resolve").

## C2 — `c7504a15` `feat(data-reports): list a user's own reports` (45)

- T6–T8 red: `Tests 3 failed (3)` (`expected 404 to be 200`). Green: `Tests 3 passed (3)` (after correcting my
  test's guess of `meta`'s keys — `currentPage`/`totalRecords`, the contract's §4).
- §12.2 check 3 proven by T8: `verifiedIds: []` with `onlyIds` lists exactly the listed spaces ✔.
- `lint` exit 0, `typecheck` exit 0, `check:links` exit 0. A Prettier-only change of its test file found later is
  a `fixup!` commit, folded into C2 before the push.

## C3 — `0418319d` `feat(data-reports): let the owner decide reports` (48)

- `REPORT_ALREADY_DECIDED` (add-error-code skill, conventions §4's order): `core/errors.ts`; Arabic «سبق البتّ في
  هذا البلاغ.», English «This report was already decided.»; api-contract §6; provoked by T12.
- U2 red: `Error: Cannot find module './decision.ts'`; green `Tests 1 passed (1)`.
- T9–T15 red: `7 tests | 6 failed` (`expected 404 to be 200`, `expected 404 to be 403`); T13 passed on 404 alone
  (proven by B19). Green: `Tests 7 passed (7)` — after fixing my test's privacy search: the reporter's id `6`
  matched inside other numbers; it now looks for the id as a JSON value (`:6,` / `:6}`).
- `lint` exit 0, `typecheck` exit 0, `check:links` exit 0.

## C4 — `b748eb3e` `feat(data-reports): let the admin decide reports` (48)

- T16–T19 red: `4 tests | 4 failed` (`expected 404 to be 200`; the races `1 request(s) never waited on a lock`).
  Green: `Tests 4 passed (4)`.
- `lint` exit 0, `typecheck` exit 0, `check:links` exit 0. Deferred documents: only *Endpoints* applies — written.

## The fixup folded before the push

`GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash` folded the C2 fixup (Prettier only). The head's tree
`b25eba81…` equals C4's tree, on which lint and typecheck had passed, so they were not run again; the plan's
`rebase -x "lint && typecheck"` per commit was not run for that Prettier-only change (stated).
Commits now: `8b40f4b3`, `045f09eb`, `b52bbc1f` (C0), `6dd2f295` (C1), `93820fb7` (C2), `029a75c3` (C3),
`7d6f9153` (C4).

## Head verification (12.4)

- Free memory before `test:unit`: 3,431,660 KB; no vitest or tsc of worker A running.
- `npm run test:unit` exit 0: `Test Files 24 passed (24)`, `Tests 259 passed (259)` (shared); `67 passed (67)`,
  `875 passed (875)`; `126 passed (126)`, `950 passed (950)`.
- `npm run test:api` (no command timeout) exit 0: `Test Files 90 passed (90)`, `Tests 1198 passed (1198)`;
  "No pending migrations to apply" on masaha_b_test.
- `npm run format:check` exit 0 ("All matched files use Prettier code style!"); `npm run check:links` exit 0 ("2786
  links in 186 documents and 1919 source files all resolve."); `npm run check:conflicts` exit 0 ("No conflict
  markers found."); `npm run build -w @masaha/shared` exit 0.
- `git grep "#PRNUM"`: documents only (7 files); `git diff --stat origin/main -- apps/web` → the two `errors.ts`,
  1 line each; `package.json`/`package-lock.json` unchanged.
- Not run locally (CI judges): `test:component`, the web build, `check:build`, `check:classes`.

## Breaks (12.5) — each red, restored from its backup (SHA-256 same), green again

Output: `scripts\pr2-breaks.out`, `pr2-b15.out`, `pr2-dbbreaks.out`; definitions `pr2-breaks.json`
(`pr2_make_breaks.py`), `pr2_b15.py`, `pr2_dbbreaks.sh`.

| Break | Red seen | Green after |
|---|---|---|
| C0-1 `issueInFamily` writes `at` | idle test: `expected '…07:10…' to be '…07:00…'` | 7/7 |
| C0-2 `findStandard` drops the shift | subscribe test: `expected { id: 2, … } to match object { priceAgorot: 25000, shiftId: null }` | 15/15 |
| B1 dismissal refinement removed | U1: `expected null to deeply equal { note: [ 'required' ] }` | 3/3 |
| B2 comparison by status only | U2: `expected 'as-is' to be 'conflict'` | 1/1 |
| B3 drop `data_reports_open_key` (db) | D1: `promise resolved … instead of rejecting` | 3/3 |
| B4 drop `data_reports_decision_check` (db) | D2: `promise resolved … instead of rejecting` | 3/3 |
| B5 drop `data_reports_dismissal_note_check` (db) | D3: `promise resolved … instead of rejecting` | 3/3 (*) |
| B6 `requireAuth()` removed | T1–T5 all: `expected 401 to be 201` (the limiter's `signedIn` refuses) | 5/5 |
| B7 `isActiveArea` skipped | T2: `expected 201 to be 404` | 5/5 |
| B8 `findOpen` skipped | T3: `expected 500 to be 200`; T4 `[ 201, 500 ]` | 5/5 |
| B9 `lockAccount` removed | T4: `expected [ 201, 500 ] to deeply equal [ 200, 201 ]` | 5/5 |
| B10 the limiter removed | T5: `expected 201 to be 429` | 5/5 |
| B11 counted by `clientAddress` | T5: `expected 429 to be 201` (the neighbour refused) | 5/5 |
| B12 user filter dropped | T6: `expected [ 4, 3, 2, 1 ] to deeply equal [ 3, 2, 1 ]` | 3/3 |
| B13 `repliedBy` from verification now | T7: `expected [ …(2) ] to match object [ … ]` | 3/3 |
| B14 `listed` from `deletedAt` only (`summariesFor`) | T8: `expected [ …(4) ] to deeply equal [ …(4) ]` | 3/3 |
| B15 `userId` in the select and the mapper | T9 and T11: `expected [ …(3) ] to deeply equal [ …(3) ]` | 7/7 (**) |
| B16 `requireCan('space.dataReports.read')` removed | T10: `expected 422 to be 403` | 7/7 |
| B17 the audit removed | T11: `expected [] to deeply equal [ { actorId: 1, … } ]`; T12 | 7/7 |
| B18 the open check removed | T12: `expected 200 to be 409` | 7/7 |
| B18 on T19 | T19: `expected 200 to be 409` | 4/4 |
| B19 `findSpaceOf` compared to nothing | T13: `expected 200 to be 404` | 7/7 |
| B20 `requireCan('dataReports.resolve')` removed | T14: `expected 422 to be 403` | 7/7 |
| B21 `can()` on the request's links | T15: `expected 200 to be 403` | 7/7 |
| B22 `field` filter ignored | T16: `expected [ 2, 1 ] to deeply equal [ 1 ]` | 4/4 |
| B23 `can()` replaced by the admin role | T17 and T18: `expected 200 to be 403` | 4/4 |
| B24 links read before `spaces.lock` | T18: `expected 200 to be 403`; T19 `expected 403 to be 409` | 4/4 |

(*) B5's restore first failed: the red run left a dismissed row with no note in masaha_b_test, which the
re-added CHECK refused. `DELETE FROM data_reports` on **masaha_b_test** (truncated before every test anyway),
then the statement again; green. The rules' definitions on masaha_b_test then compared to masaha_b_dev's:
identical.
(**) B15 first ran with `userId` in the select only and **stayed green** — plainly my break's defect (the mapper
never shows a column it is not given). Run again as the plan names it, select **and** mapper: red. Departure
stated.

## Real run (12.6, PR 2) — API on 3321, masaha_b_dev — `ALL PASS`, exit 0

`node scripts\realrun2.mjs` (output `scripts\realrun2.out`); `/health` → `{"status":"ok","db":"up",…}`.
Reporter `demo-reception` (user 3, a global USER); verified set space `noor-hub` (2, the directory owner's),
unverified `tuffah-place` (10). Signed in once; every request within a minute, so no idle sign-in again.

PASS POST verified { PRICES } 201 · the same again 200 (same id) · POST unverified { HOURS } 201 · { OTHER } no
message 422 · GET /me/reports both OPEN 200 · owner GET …/data-reports 200, no reporter (name, email, `userId`, the
id as a value) · owner PATCH { RESOLVED, note } 200 (SPACE) · owner PATCH { DISMISSED } 409 REPORT_ALREADY_DECIDED ·
admin GET /admin/data-reports 200 with the reporter's name · admin PATCH the verified space's 403 · admin PATCH {
DISMISSED } no note 422 · with a note 200 (MASAHA) · GET /me/reports?status=DECIDED SPACE and MASAHA 200 · POST
verified { CONTACT } 201 · **the 11th report request of the hour 429 with Retry-After** · one open CONTACT report.

**Requests sent to reach 429: 11** (counted: PRICES ×2, HOURS, OTHER (422), CONTACT, 5 repeats, then the 11th).
**Data changed on masaha_b_dev:** `data_reports` rows 1 (noor-hub PRICES, RESOLVED by its owner, a note),
2 (tuffah-place HOURS, DISMISSED by the admin, a note), 3 (noor-hub CONTACT, OPEN); `audit_logs`
`dataReport.resolved` (1) and `dataReport.dismissed` (2); one `rate_limits` row `data-report:<hash>` (hits 11,
resets 13:20Z); the general limiter's counters and the sessions of the three sign-ins.

The API stopped by process id (5132 the server, 32624 `tsx watch`, 13240 `pino-pretty`); port 3321 free;
`server.log` deleted.

## PR number, push, PR (12.7)

- `gh api …issues?state=all…` → last 119; `scripts\prnum-pr2.sh 120` (DESK_API's model, its branch, backup and
  body adapted; its checks kept): "PRNUM OK #120 36718fde (was 7d6f9153)". `#PRNUM` only in documents; the
  migration's SQL holds no number. `check:links` exit 0, `format:check` exit 0 after the rewrite.
- Labels `feat`, `area:api`, `area:docs`, `area:web` exist. `git push -u origin feat/data-reports`.
- `gh pr create --assignee @me …` → **#120** https://github.com/Basel-Ghonaim/masaha/pull/120 (= the expected n).
- Commits on the branch: `8b40f4b3` (48), `045f09eb` (42), `b52bbc1f` (43), `25d4001c` C1 (47), `11ce49a8` C2 (45),
  `2ab0edb2` C3 (48), `36718fde` C4 (48). No `fixup!`, no rebase in progress.
- Local branch left: `backup/data-reports-pre-prnum` (the pre-number head `7d6f9153`).

## Open PRs and conflicts (12.8)

- Worker A's **#119** `feat/desk-subscribers` (head `8d087c5e`) opened during this work. Shared files with #120:
  `docs/architecture/findings/README.md` only (a document: #119 its own lines, #120 lines 170–171); no code
  file shared. `git merge-tree --write-tree HEAD 8d087c5e` exit 0: **clean**. Whichever merges second rebases if
  GitHub asks, keeping both sides' lines.
- #120: 46 files (`git diff --name-only origin/main...HEAD`), within the 60.

## CI (12.8) — green on the pushed head, CLEAN

`gh pr checks 120`: pass lint, check:conflicts, format:check, typecheck, test:unit, test:component, check:classes,
check:links, build, test:api, CodeRabbit. `gh pr view 120 --json headRefOid,mergeStateStatus` →
`36718fde7e19973f422e327c51ecab14e8599c65`, `CLEAN` (= `git rev-parse HEAD`). (`check:build` shows no check of its
own in the list; it runs inside CI's `build` job, as before.)

## Leftovers

`git status --short` empty; no rebase in progress. Local backup branch left: `backup/data-reports-pre-prnum`.
(The `backup/desk-subscribers-*` branches in the shared repository are worker A's, not touched.) Port 3321 free.

## Decisions taken without the owner

None needed a decision under the autonomy rule: no plan point proved false against the code, no carried item
was larger than its file, no real-run case was missing from the demo data, and the one break that stayed green
(B15) was plainly my own break's defect, fixed as §12.5 allows. The departures above are the plan's own allowances.
