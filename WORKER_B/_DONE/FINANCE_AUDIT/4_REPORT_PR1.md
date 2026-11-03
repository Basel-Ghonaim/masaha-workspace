# FINANCE_AUDIT — PR 1 report (`feat/audit-log`)

Executor: worker B's executor of PR 1, 2026-10-27, under the owner's autonomy rule
(`_SHARED\AUTONOMY_2026-10-25.md`). Long outputs in `scripts\`.

## Read

- `3_EXEC_PROMPT_PR1.md`, `_SHARED\AUTONOMY_2026-10-25.md`, `0_CARRIED_FROM_123.md` whole;
  `_DONE\ANNOUNCEMENTS\6_REVIEW_PR4_CLAUDE_CODE.md` (findings 1–4; the rest of the file was on screen in the same read).
- `2_PLAN.md`: the approval note, the header, §1, §2, §3, §4 (owner's decisions, D1–D6, D14, D15), §5, §6, §7, §9
  (PR 1, *Not tested*), §10, §11, §12, §13, Appendix A. D7 opened on screen with D6 (not used).
- Repository: as each step needed (listed under each commit).

## Preconditions (§12.1)

- `git fetch origin`; worktree detached at `39ef0504` = `origin/main` (#124's merge), clean.
- #123: `gh pr view 123` → `MERGED e6737da5`; `e6737da5^{tree}` = `ff8743c8^{tree}` = `3905beba…` (the plan's read).
- Base diff `3855e37f..origin/main`: 110 paths (`scripts\base-diff.txt`). #123's paths as the plan read them;
  #124 (`e6737da5..39ef0504`) outside `apps/web`: documents only — findings 101, 125 and the index (101, 125 moved to
  *Resolved*), `customers.md`, `desk.md`, `packages.md`, `spaces.md`, `subscriptions.md` (*Who uses it*: the sheet,
  #124), `foundation.md`, `overview.md` (*Customers*: the dashboard's sheet). **No code file of §7 changed**; no
  difference the plan does not cover. Each shared document re-read on `main` before its edit.
- Open PRs: none (`gh pr list --state open` empty).
- `0_CARRIED_FROM_*.md`: only `0_CARRIED_FROM_123.md` (PR 1's C0).
- Docker: `masaha-postgres-1 Up (healthy)`. `apps/api/.env`: `PORT=3321`, `masaha_b_dev`, `masaha_b_test`
  (matched by pattern, credentials masked).
- `npx prisma migrate status` on `masaha_b_dev` and `masaha_b_test`: "Database schema is up to date!" (29 migrations,
  the last `20261026114022_closure_extension_key`) — nothing to deploy.
- `npm run build -w @masaha/shared` → exit 0.
- Branch: `git switch --no-track -c feat/audit-log origin/main`.

## Commits

### C0a `46ebbead` fix(subscriptions): move unstarted renewals too (47)

- Read: `closures.repository.ts`, `closures.service.ts`, `extension.api.test.ts` whole; `schema.prisma` *Subscription*
  (the renewal FK through `(renewal_of_id, customer_id)`: a renewal is always its customer's space's);
  `test/{factories,locks,spaces}.ts` (signatures); the contract's *Announcements (managed)* extension routes; data
  model *ClosureExtension*, *Checked by the service*; `subscriptions.md` whole; the findings index and finding 124/150
  (form).
- Tests (in `extension.api.test.ts`, new `describe('the renewal chain (finding 151)')`): T-C1 (the review's
  scenario: S ends 12-03, R 12-04 → 2027-01-02, two links, `renewalIds`), T-C2 (a renewal's renewal moves; a renewal
  started today, one ended early, another space's never), T-C3 (preview 4 = 2 covered + 2 renewals; after apply the
  preview's and the list's `extension.subscriptions` 4), T-C4 (`whileHeld`: R inserted while the extension waits on
  the space's lock → moved). The existing audit expectation gains `renewalIds: []`.
- Red (`scripts\c0a-red.txt`): `Tests  5 failed | 10 passed (15)` — e.g. `expected '2026-12-01 → 2026-12-30' to be
  '2026-12-03 → 2027-01-01'`; T-C3 `subscriptions: 2` vs 4.
- Green (`scripts\c0a-green.txt`): `Tests  15 passed (15)`.
- **§12.2 PR 1 check 3:** PostgreSQL accepts `FOR UPDATE` on the outer `SELECT` over the recursive CTE (T-C1, T-C4
  green) — one statement, as planned.
- Code: `movedCount`, `lockMoved` (one statement, `ORDER BY "id" FOR UPDATE`), `moveRenewals` replace
  `coveredCount`/`lockCovered`; the covered fragment unchanged; `today = gazaClockOf(at).date`.
- Docs: finding 151 (new, *Resolved*, its *Resolution* with `#PRNUM`), its index line under *Resolved*; contract
  (`ExtensionPreview.subscriptions`, a bullet *Their renewals not started*, the preview's 200, the 201 with
  `renewalIds`, the lock order); data model (*ClosureExtension*, *Checked by the service*); `subscriptions.md`
  (*What it does*, *Behaviour*, a new *API decisions* line, the lock line, a `#PRNUM` history line).
  `announcements.md` states no covered rule (only "the subscriptions it covered", still true): unchanged.
- `npm run lint` exit 0; `npm run typecheck` exit 0; `check:links` "2868 links … all resolve".

### C0b `aa360aa8` fix(subscriptions): refuse a key of another space (49)

- Test: T5 gains space B's owner on B's URL with A's closure id and A's key → 409 `conflict`, no code, no `data`.
- Red (`scripts\c0b-red.txt`): `AssertionError: expected 201 to be 409` — `Tests  1 failed | 14 skipped (15)`.
- Code: `EXTENSION` selects `announcement.spaceId`, `ExtensionRow.spaceId` (as D2); the retry answers `conflict`
  when `recorded.spaceId !== space.id || recorded.announcementId !== announcementId`. The extension's own answer
  passes `spaceId: space.id` to the mapper (the type now needs it).
- Green: `closures/` both files `Tests  19 passed (19)`; lint 0; typecheck 0 (first typecheck failed on the mapper's
  argument missing `spaceId`: fixed before the commit); links 0.
- Docs: contract's extension errors; `subscriptions.md` (*Behaviour*, the key decision's line, the history line).

### C0c `d71498fa` docs: correct the extension's key and history (45)

- `data-model.md:23`: the extension's key unique on its own (no space column), linking *Constraints worth stating*;
  `subscriptions.md`: `#123` moved below `#118`. lint 0, typecheck 0, links 0.

### C1 `0f4e8543` feat(audit): read a space's audit log (37)

- Read: `schema.prisma` (*AuditLog*, the name columns of the targets, *SpaceManager*), `shared/audit/writeAudit.ts`,
  every `action:` written (`git grep`, the dynamic ones in `lookupChange.ts`, `groupEdit.ts`, `space.service.ts`,
  `users.service.ts`, `staff.service.ts`), `packages/shared` (`package.json`, `core/{pagination,fields,fieldErrors,
  gazaTime}.ts`, `payments/requests.ts` and its unit test, `directory/requests.ts`' comma lists), the data-reports
  module (routers, controller, service's page) and its API test's setup, `customers.repository.ts` (`page`, the
  search), `shared/http` (`buildPaginationMeta`, `sendSuccess`), `app.ts` (mounts), `test/{admin,factories}.ts`,
  `eslint.config.js` (level map: `audit` L5), `can.ts` (`space.auditLog.read` owner, `platform.auditLog.read` admin);
  docs: contract §4–§5 (*Favourites*, *Data reports*), conventions header, §6, §7 table, §8 R7, security
  *Authorization*, data model *AuditLog* and *Search*, documentation.md §5 (template), `favorites.md`,
  `data-reports.md` (form), finding 14.
- **Red first, each:** U3 (shared `requests.unit.test.ts`) against a stub `requests.ts` (`spaceAuditQuerySchema =
  paginationQuerySchema`, the real file backed up in `scripts\stubs\` and restored, SHA-256 equal):
  `AssertionError: expected { page: 1, limit: 20 } to deeply equal { page: 1, limit: 20, …(1) }`. U2
  (`auditPeriod.unit.test.ts`) against a stub returning `null`: `expected undefined to be '2026-10-11T21:00:00.000Z'`.
  T1–T9 (`spaceAuditLog.api.test.ts`) before the module: `Tests  9 failed (9)` — `expected 404 to be 200` (and 403,
  422).
- One expectation of U3 corrected after its first green run: an actor id of `0`, `-3` or `2147483648` answers
  `out_of_range` (the union's number branch), not `invalid_format` as I first wrote; `ADMIN` and `1.5` are
  `invalid_format`. The contract says both.
- Green: U3 `Tests  1 passed (1)`; U2 `Tests  1 passed (1)`; T1–T9 `Tests  9 passed (9)` on the first run.
- **§12.2 check 5:** `masaha_search_text` exists on `masaha_b_test` and folds «أحمد» to «احمد» (T5 green: `q=احمد`
  finds the customer «أحمد سالم»).
- **§12.2 check 2:** `npm run lint` exit 0 with the module's imports (`@masaha/shared/{audit,core}`, `shared/*`).
- lint 0, typecheck 0 (after `npm run build -w @masaha/shared`, exit 0), links "2891 links … all resolve", Prettier
  clean.
- Docs: contract *Audit log* (new, after *Favourites*: the rules, the types, the owner's route); conventions header
  (*Built* / *Not yet built*), §6 (the reader, `MASAHA` by links, finding 14's line rewritten: designed by O13, screen
  not built), §7 (`audit` linked, *Holds*); security (*Authorization*: the owner's log); data model (*AuditLog*: kept
  for ever, decision 10); `features/audit.md` (new).

### C2 `e8e09fc3` feat(audit): read the platform's audit log (42)

- **Red first, each:** U1 (`platformEvents.unit.test.ts`) against a stub (empty lists, `isPlatformEvent` always
  true): `AssertionError: announcement.created: expected [ true, true ] to deeply equal [ false, false ]`. U3's new
  admin line against `platformAuditQuerySchema = spaceAuditQuerySchema` (backup/restore, SHA-256 equal): `expected null
  to deeply equal { actor: [ 'invalid_format' ] }`. T10–T13 before the route: `expected 404 to be 200` —
  `Tests  4 failed | 4 passed (8)`; **T14's four `REFUSED_CALLERS` passed before the route existed** (the `/admin`
  guard answers before routing), so B18 is its break (below).
- Green: U1 `Tests  1 passed (1)`; U3 `Tests  2 passed (2)`; both audit API files `Tests  17 passed (17)`.
- lint 0, typecheck 0, shared build 0, links "2907 links … all resolve"; `features/audit.md` 1,111 words.
- Docs: contract (the admin's route, `PlatformAuditEntry`), conventions (header *Built*, §6 the allowlist's home and
  the account rule, *kept for ever* with finding 152, §7 *Holds*), security (the admin's log), data model (finding
  152 linked), `audit.md`, v1-mvp (step 11 *Built*, the two rows), overview (*Built*: *Audit*), `docs/README.md` (the
  map's line), **finding 152** (new, Open) and its index line.

## §12.2 PR 1 check 4 — the cost on a generated year (`masaha_b_test`, truncated after each run)

Scripts: `scripts\audit-year.sql` (the plan's lateral), `audit-year-memoize.sql`, `audit-year-joins.sql`,
`audit-year-final.sql` (the shape built); outputs `*.out` beside them. Data: 1 busy space with 36,000 entries over
365 days (95 % visit, check-in, payment and customer actions; 5 % `space.profileEdited`), 300,000 entries of 10
other spaces, 1,000 platform entries naming no space (`user.created`, `area.edited`); 500 customers and 3,000 visits
for the names; 337,000 entries, 70 MB with indexes. `EXPLAIN (ANALYZE, BUFFERS)`; `since` = the Gaza midnight 29 days
back; `q` = «زبون 42» (owner) and «hub 7» (admin).

| Statement | Lateral (planned) | Joins (built) |
|---|---|---|
| O1 owner page, 30 days | 0.8 ms | 2.0 ms |
| O2 owner count, 30 days | 1.6 ms | 2.2 ms |
| O3 owner actors, 30 days | 3.0 ms | 5.1 ms |
| O4 owner page, all | 5.2 ms | 1.7 ms |
| O5 owner count, all | 5.8 ms | 11.6 ms |
| O6 owner actors, all | 22.3 ms | 56.8 ms |
| **O7 owner page, all, `q`** | **2,466 ms** | **280 ms** |
| **O8 owner count, all, `q`** | **8,429 ms** | **220 ms** |
| O9 owner page, 30 days, `q` | 24.0 ms | 72.2 ms |
| A1 admin page, all | 5.6 ms | 2.9 ms |
| A2 admin count, all | 58.4 ms | 93.9 ms |
| A3 admin actors, all | 59.1 ms | 102.1 ms |
| **A4 admin page, all, `q`** | **4,319 ms** | **1,082 ms** |
| **A5 admin count, all, `q`** | **4,727 ms** | **179 ms** |

- **Why the lateral was slow** (`audit-year-memoize.out`): PostgreSQL put a `Memoize` node over the lateral `UNION
  ALL`, keyed by `(entity_type, entity_id)`, which missed and evicted on every one of the 36,000 rows (0.19 ms a row,
  the `Append` beneath it 0.01 ms): O8 8,641 ms with it, 735 ms with `enable_memoize = off`; the lateral alone, no `q`,
  8,202 ms; the search function alone over 36,000 texts, 62 ms.
- **The joins** (one `LEFT JOIN` per target type, the type in its condition; the names by `coalesce`) read each table
  once: in a quieter run (`audit-year-joins.out`) O7 133 ms, O8 114 ms, the owner's actors with `q` 145 ms, A5 114 ms,
  A4 582 ms. The final run above was on a busier machine (every figure about twice as high).
- **Over 150 ms, recorded and not indexed** (the owner's Q5 rule): `q` over **all time** — the owner's page and count
  (280 / 220 ms), the admin's page and count (1,082 / 179 ms). Every read without `q`, and `q` over the default 30
  days, is under 150 ms. A4's plan walks `audit_logs_created_at_idx` backwards through every entry for the first 20
  platform entries that match; an index on `(action, created_at)` (A3) or a trigram index would serve it — **the
  owner's decision at the review**; no migration was made.

## Decisions taken without the owner (as they were met)

1. **The target's names by joins, not a lateral subquery** (§12.2 check 4). *Met:* D5's `LEFT JOIN LATERAL (… UNION
   ALL …)` made PostgreSQL wrap the lateral in a `Memoize` node that missed and evicted on every row: `q` over a
   year took 2.5–8.4 s for the owner and 4.3–4.7 s for the admin. *Options:* keep the lateral and only record it;
   turn Memoize off per statement (a session setting in a read); one `LEFT JOIN` per target type, its type in the
   condition, names by `coalesce`. *Chose* the joins: the same answer (T3, T5, T12 unchanged and green), no schema
   change, 10–30× faster on `q`, no slower elsewhere. Folded into C1 (an `edit` rebase; C2 replayed over it, its one
   conflict resolved to the tested file; `backup/feat-audit-log-pre-joins` kept). *Undo:* restore the lateral block
   from that backup branch's `audit.repository.ts`.
2. **Four reads over 150 ms recorded, not indexed** (the owner's Q5 rule): `q` over all time — owner's page and
   count 280 / 220 ms, admin's page and count 1,082 / 179 ms on a busy machine (133 / 114 / 582 / 114 ms when
   quieter). *Options:* an index now (A3, a migration the owner did not order); record. *Chose* record. *Undo:* n/a —
   the owner decides an index at the review.
3. **T-C2's "started" renewal on the file's own clock.** *Met:* the plan's T-C2 used a clock of 2026-11-12 and a
   closure ended 11-11; `extension.api.test.ts` runs every test at 2026-11-10 with running closures, and with a running
   closure any started renewal is also covered. *Options:* a second app with another clock in the file; an ended
   closure at the file's clock. *Chose* the ended closure (11-08 only; the renewal starting today, 11-10, is neither
   covered nor pending): one clock per file, the same rule proven (B-C2 red). *Undo:* rewrite T-C2 with a second app.
4. **`actions` repeated are counted once,** as the directory's area list (`[...new Set(…)]`), rather than refused
   (D4 says "each once" with the codes `invalid_choice` / `too_long` only). *Undo:* a `not_unique` refinement.
5. **An actor id below 1 or past the largest answers `out_of_range`** (Zod's number branch of the union), a letter
   `invalid_format`; the contract says both. *Undo:* a refinement forcing one code.
6. **`OPEN_DECISIONS.md` not appended** (§12.8 asks PR 1's report to append point 2). *Met:* the exec prompt (§2.6)
   allows writing only this report and `scripts\` outside the repository; the prompt wins. The line for the
   supervisor: "finding 151 resolved (#<n>, 2026-10-27): the extension moves each covered subscription's renewal
   chain not started". *Undo:* the supervisor appends it.
7. **The carried real-run case not performed** (§12.2 check 6): `masaha_b_dev`'s demo space has one closure (id 2),
   already extended by #123's run, and no renewal that starts after today (`SELECT … r.starts_on > today` → 0);
   creating either through the app would be a write the run may not make. Proven by T-C1–T-C4 and B-C1–B-C5.

## The breaks — stopped for low memory (2026-10-27)

- `python -I scripts\brk.py scripts\pr1-breaks.json` (all 25: B-C1–B-C6, B1–B18, B12a), started in the background
  with about 4.8 GB free (worker A running only a `tsc`). **Claude Code stopped it because the system was critically
  low on memory.** Its output was still buffered: **no red line was captured.** The backups show it had reached B9
  (B-C1 … B8 had run; B9 was applied).
- **The tree after the stop:** B9's edit was left in `audit.repository.ts`. Restored by copying
  `scripts\breaks\B9__audit.repository.ts` (equal to `HEAD`'s file by `cmp`), SHA-256 `c4cebf03…` both;
  `git status --short` clean. No other file was left changed.
- The harness says not to restart the stopped command on my own: **the breaks are awaiting the owner's go-ahead**,
  and so are the full lanes (`test:unit`, `test:api`), which use more memory than the breaks.

## The breaks — re-run on the owner's go-ahead (each red, restored from its backup, SHA-256 same, green)

Outputs: `scripts\pr1-breaks-{1,2,3}.out` (`python -I -u brk.py`, unbuffered, three foreground batches). Free memory before: 3,598,936 KB; no vitest or tsc of worker A's running. Tree clean after each batch.

```
== B-C1 (apps/api/src/modules/subscriptions/closures/closures.service.ts) broken run exit 1
AssertionError: expected '2026-12-01 → 2026-12-30' to be '2026-12-04 → 2027-01-02' // Object.is equality
   restored run exit 0: Tests  1 passed | 14 skipped (15)
== B-C2 (apps/api/src/modules/subscriptions/closures/closures.repository.ts) broken run exit 1
AssertionError: expected '2026-11-12 → 2026-12-11' to be '2026-11-10 → 2026-12-09' // Object.is equality
   restored run exit 0: Tests  1 passed | 14 skipped (15)
== B-C3 (apps/api/src/modules/subscriptions/closures/closures.repository.ts) broken run exit 1
AssertionError: expected '2026-12-31 → 2027-01-29' to be '2027-01-02 → 2027-01-31' // Object.is equality
   restored run exit 0: Tests  1 passed | 14 skipped (15)
== B-C4 (apps/api/src/modules/subscriptions/closures/closures.repository.ts) broken run exit 1
AssertionError: expected { firstDay: '2026-11-08', …(4) } to match object { subscriptions: 4, applied: null }
   restored run exit 0: Tests  1 passed | 14 skipped (15)
== B-C5 (apps/api/src/modules/subscriptions/closures/closures.service.ts) broken run exit 1
AssertionError: expected 500 to be 201 // Object.is equality
   restored run exit 0: Tests  1 passed | 14 skipped (15)
== B-C6 (apps/api/src/modules/subscriptions/closures/closures.service.ts) broken run exit 1
AssertionError: expected 201 to be 409 // Object.is equality
   restored run exit 0: Tests  1 passed | 14 skipped (15)
== B1 (apps/api/src/modules/audit/platformEvents.ts) broken run exit 1
AssertionError: payment.recorded: expected true to be false // Object.is equality
   restored run exit 0: Tests  1 passed (1)
== B2 (apps/api/src/modules/audit/platformEvents.ts) broken run exit 1
AssertionError: expected true to be false // Object.is equality
   restored run exit 0: Tests  1 passed (1)
== B3 (apps/api/src/modules/audit/auditPeriod.ts) broken run exit 1
AssertionError: expected '2026-10-11T08:00:00.000Z' to be '2026-10-11T21:00:00.000Z' // Object.is equality
   restored run exit 0: Tests  1 passed (1)
== B4 (packages/shared/src/audit/requests.ts) broken run exit 1
AssertionError: expected null to deeply equal { actions: [ 'invalid_choice' ] }
   restored run exit 0: Tests  2 passed (2)
== B5 (apps/api/src/modules/audit/audit.repository.ts) broken run exit 1
AssertionError: expected [ 5, 4 ] to deeply equal [ 4, 3 ]
   restored run exit 0: Tests  1 passed | 8 skipped (9)
== B6 (apps/api/src/modules/audit/audit.mapper.ts) broken run exit 1
AssertionError: expected { kind: 'PERSON', id: 5, name: '' } to deeply equal { kind: 'MASAHA' }
   restored run exit 0: Tests  1 passed | 8 skipped (9)
== B7 (apps/api/src/modules/audit/audit.repository.ts) broken run exit 1
AssertionError: expected [ …(8) ] to deeply equal [ …(8) ]
   restored run exit 0: Tests  1 passed | 8 skipped (9)
== B8 (packages/shared/src/audit/requests.ts) broken run exit 1
AssertionError: expected [ 1, 2 ] to deeply equal [ 1 ]
   restored run exit 0: Tests  1 passed | 8 skipped (9)
== B9 (apps/api/src/modules/audit/audit.repository.ts) broken run exit 1
AssertionError: expected [] to deeply equal [ 1 ]
   restored run exit 0: Tests  1 passed | 8 skipped (9)
== B10 (apps/api/src/modules/audit/audit.repository.ts) broken run exit 1
AssertionError: expected [ 1 ] to deeply equal []
   restored run exit 0: Tests  1 passed | 8 skipped (9)
== B11 (apps/api/src/modules/audit/audit.repository.ts) broken run exit 1
AssertionError: expected [ …(7) ] to deeply equal [ …(4) ]
   restored run exit 0: Tests  1 passed | 8 skipped (9)
== B12 (apps/api/src/modules/audit/audit.manage.routes.ts) broken run exit 1
AssertionError: expected 422 to be 403 // Object.is equality
   restored run exit 0: Tests  1 passed | 8 skipped (9)
== B12a (apps/api/src/app.ts) broken run exit 1
AssertionError: expected 404 to be 403 // Object.is equality
   restored run exit 0: Tests  1 passed | 8 skipped (9)
== B13 (apps/api/src/modules/audit/platformEvents.ts) broken run exit 1
AssertionError: expected [ 1, 2, 3, 4, 5, 6, 7 ] to deeply equal [ 1, 2, 3, 4, 5, 6 ]
   restored run exit 0: Tests  1 passed | 7 skipped (8)
== B14 (apps/api/src/modules/audit/platformEvents.ts) broken run exit 1
AssertionError: expected [ 1, 2, 3, 4, 5, 6, 15 ] to deeply equal [ 1, 2, 3, 4, 5, 6 ]
   restored run exit 0: Tests  1 passed | 7 skipped (8)
== B15 (apps/api/src/modules/audit/platformEvents.ts) broken run exit 1
AssertionError: expected [ 1, 2, 3, 4 ] to deeply equal [ 3, 4 ]
   restored run exit 0: Tests  1 passed | 7 skipped (8)
== B16 (apps/api/src/modules/audit/audit.repository.ts) broken run exit 1
AssertionError: expected [ 1 ] to deeply equal [ 1, 2 ]
   restored run exit 0: Tests  1 passed | 7 skipped (8)
== B17 (apps/api/src/modules/audit/audit.repository.ts) broken run exit 1
AssertionError: expected [ 1, 2, 3, 4 ] to deeply equal [ 2 ]
   restored run exit 0: Tests  1 passed | 7 skipped (8)
== B18 (apps/api/src/app.ts) broken run exit 1
AssertionError: expected 200 to be 401 // Object.is equality
AssertionError: expected 200 to be 403 // Object.is equality
   restored run exit 0: Tests  5 passed | 3 skipped (8)
```

- B12a answered 404 (not the plan's "the stranger reads it"): mounted on `api` before the boundary, `requireCan` found no loaded space; reception's 403 was lost, so the break is red as the guard's absence shows. B18: the four refused callers got 200.

## Verification on the head (`72a264e8`)

- Before the lanes: free memory 1,545,172 KB with worker A's `eslint .` at 3 GB (pid 12524) — waited for it to end
  (not stopped); then 4,519,632 KB, then 4,682,436 KB before `test:api`; no vitest/tsc/eslint of worker A's running.
- `npm run test:unit` exit 0: `Tests  263 passed (263)` · `Tests  879 passed (879)` · `Tests  989 passed (989)`.
- `npm run test:api` (background, no timeout) exit 0: `Test Files  97 passed (97)` · `Tests  1245 passed (1245)` ·
  `Duration  643.48s`.
- `npm run format:check` "All matched files use Prettier code style!"; `check:links` "2907 links in 194 documents and
  2066 source files all resolve."; `check:conflicts` "No conflict markers found."; `build -w @masaha/shared` exit 0;
  lint and typecheck exit 0 (after C2 and after the joins' fold).
- `git grep -l "#PRNUM"`: documents only (9). `git diff --stat origin/main -- apps/web package.json
  package-lock.json`: empty. Files changed against `origin/main`: 34.
- Not run, with why: `test:component`, the web's `build`, `check:build`, `check:classes` — no web file changes; CI.

## The real run (API on 3321, `masaha_b_dev`)

`scripts\realrun1.out`:
```
PASS health db up
PASS owner reads the space's log (13 entries, SQL 13) 200 -
PASS reception is refused 403 -
PASS the directory owner on the demo space is not_found 404 -
PASS admin reads the platform's events (17; every action on the list; off-list: none) 200 -
     the admin's rows 17, SQL by the same list 17
PASS admin sets space 1 hidden true 204 -   (and false; space 10 true, false: 204 each)
PASS the admin's log shows the four, with names 200 -
FAIL the owner's log shows the demo space's two, the actor MASAHA with no id or name 200 -
PASS q=Demo Space finds them (2 entries) 200 -
NOT PERFORMED the carried extension of a renewal chain (…) Proven by T-C1–T-C4.
1 FAILED
```
- **The FAIL was the script's own check:** it searched the body for `"id":<admin id>,"name"`; the seeded admin's id
  is 1, and the target `{"type":"space","id":1,"name":"Demo Space"}` matched it. The API's answer (read again,
  `dbg1.mjs`): entries 52 and 53 `{"kind":"MASAHA"}`. Re-judged **read-only** (`realrun1b.mjs`, no write repeated):
  `PASS … (52, 53) as MASAHA; no actor carries the admin's id 200` · `PASS q=Demo Space finds 52 and 53 (2 entries)
  200` · `ALL PASS`. `realrun1.mjs`'s check corrected to compare the actors' ids.
- **The run's writes:** `PUT /admin/spaces/1/hidden` true then false, `PUT /admin/spaces/10/hidden` true then false;
  audit entries 52–55 (`space.hidden` / `space.unhidden`, the admin the actor). Both spaces end as they began
  (shown).
- Server stopped by process id (tsx watch 10036, server 3144, pino-pretty 2100); port 3321 free; `server.log` deleted.

## The PR number, push, PR, conflicts

- `gh api …/issues?state=all&per_page=1` → 127 (worker A's #127 `feat/payments`), so 128.
  `scripts\prnum-pr1.sh 128` → `PRNUM OK #128 3f8a2184 (was 72a264e8)`; backup `backup/audit-log-pre-prnum`; no
  `#PRNUM` left; the rewrite changed nothing but the number. Then `check:links` 0, `format:check` 0, the number still
  127 + 1, `git push -u origin feat/audit-log`.
- `gh pr create … --title "feat(audit): read the owner's and admin's logs"` → **#128** (equal to the commits'
  number: no redo needed).
- Commits after the rewrite: `47b3f2bd` fix(subscriptions): move unstarted renewals too (47) · `36f03ca7`
  fix(subscriptions): refuse a key of another space (49) · `4336a34e` docs: correct the extension's key and history
  (45) · `1d43ef5b` feat(audit): read a space's audit log (37) · `3f8a2184` feat(audit): read the platform's audit log
  (42).
- **Conflicts:** `git merge-tree --write-tree HEAD 9e16098d` (#127's head) → exit 0, clean. Shared with #127:
  `docs/architecture/findings/README.md` and `docs/project/overview.md` (documents; each side kept its lines).

## CI and the state at the end

- `gh pr checks 128` (`scripts\ci.txt`) on head `3f8a2184` = `git rev-parse HEAD`: build, check:classes,
  check:conflicts, check:links, format:check, lint (1m43s), test:api (4m51s), test:component (8m40s), test:unit
  (1m22s), typecheck — **all pass**; CodeRabbit skipping. `mergeStateStatus` **CLEAN**. Files: **34** (the plan said
  ≈ 36).
- `git status --short` clean; no rebase in progress. Local branches left: `backup/feat-audit-log-pre-joins` (the head
  before the joins' fold), `backup/audit-log-pre-prnum` (the head before the PR number).
- Merge order with #127 (worker A, `feat/payments`): no shared code file; shared documents `findings/README.md` and
  `overview.md`, merge-tree clean. Whichever merges second re-checks; nothing to rebase now.
- **For the supervisor** (`_SHARED\OPEN_DECISIONS.md` point 2, not written by me — decision 6): "finding 151 resolved
  (#128, 2026-10-27): the extension moves each covered subscription's renewal chain not started".
- **The owner's decisions at review:** the four `q`-over-all-time reads over 150 ms (an index, or accept); finding
  152's retention rule (Open).

## The review's fix round (2026-10-28)

Prompt: `7_FIX_ROUND_PR1.md`; review: `6_REVIEW_PR1_CLAUDE_CODE.md` (mergeable after a fix round). The owner's decision:
F1, F2 and F3 fixed in this round; F1 may touch `users` and `space-links`.

### The base

- `git fetch origin`; `gh pr view 128` → head `3f8a2184`, `mergeStateStatus` **CLEAN**; `origin/main` `0ec43b61`;
  merge-base `39ef0504`. **Not rebased** (CLEAN). Backup `backup/audit-log-pre-review-fix` at `3f8a2184`.
- Docker Desktop was not running (`npipe … dockerDesktopLinuxEngine` not found; `test:api`'s global setup
  ECONNREFUSED): started it and `docker start masaha-postgres-1` → `Up (healthy)`. No data changed.

### F1 (blocker) — a staff account's events are the space's

- **Sweep** (`git grep` of the seven `PLATFORM_ACCOUNT_ACTIONS` in `apps/api/src`, then their callers):
  `user.temporaryPasswordIssued` / `user.temporaryPasswordHandedOver` already name the space from the owner's routes
  (the admin's own recovery names none: the admin's act); `user.roleChanged` (adminOwners, adminRoles) and
  `user.suspended` / `user.unsuspended` (the users' admin routes) are the admin's only. **Only the review's two
  concern a reception account:** `user.created` (staff `add`) and `user.emailChanged` (the forced change). No other.
- **Writers changed:** `users.createWithTemporaryPassword` takes an optional `spaceId` after `tx` (as
  `replaceWithTemporaryPassword` does); `staff.service.ts` `add` passes `space.id`; the admin's owner creation passes
  none. The forced change's `user.emailChanged` names `receptionSpaceOf(userId, tx)`: the space of the account's
  `RECEPTION` link, active or not (one desk per person), read in the change's transaction; none for an owner or a
  user. `receptionSpaceOf` is a new `space-links` service read (repository `findReceptionSpaceOf`), passed into
  `users` in `app.ts` as a closure, since `space-links` is a level above (as `lockSpace`, `ownersFor`). No schema
  change, no migration.
- **Test** (through the real routes), `platformAuditLog.api.test.ts`: "an owner's reception account's creation and
  email correction, through the routes, are the space's, never the admin's; the admin's creation of an owner is the
  admin's". The owner adds Hala (`POST /manage/spaces/:id/staff`); Hala signs in and corrects her email
  (`POST /me/password`); the admin creates an owner of a third space (`POST /admin/owners`). The admin's
  `?period=ALL` account events = the admin's `user.created` of the owner only; the owner's log = Hala's
  `user.emailChanged` (actor Hala) and the owner's `user.created` (actor Ahmad), target Hala.
  - **Red before the fix:** `× an owner's reception account's …` — `AssertionError: expected [ …(3) ] to deeply equal
    [ { action: 'user.created', …(2) } ]` (the admin's log listed Hala's `user.emailChanged` and `user.created`).
  - **Green after:** `Test Files 3 passed (3) · Tests 40 passed (40)` (the platformAuditLog, staff and users API files).
  - **Break** (`space.id` dropped from the staff call; backup copy, restored): `× … AssertionError: expected [ …(2) ]
    to deeply equal [ { action: 'user.created', …(2) } ]` — `Tests 1 failed | 8 passed (9)`; restored, diff back.
- **Tests the fix touched:** `staff.api.test.ts` (its `user.created` entry now `spaceId`; it was `spaceId: null`,
  asserting the leak); `users.service.unit.test.ts` (the new required dependency, a stub that rejects, as `audit`).
- **Documents:** `audit.md`'s *Why* of the account decision (the creation, the temporary passwords and their
  handover, the email at the forced change; 2026-10-28, #128); `api-contract.md` (the forced change's `email`, the
  staff add's `user.created` "with the space"); `users.md` (its two decisions, Last Updated). The contract's
  admin-log line and conventions §6 already said an owner's staff account's events name the space: now true,
  unchanged.
- Folded into `feat(audit): read the platform's audit log` → **`4706968a`**.

### F2 — `audit.md`'s *The target*

- Now: one left join per entity type, its type in the join's condition, so at most one matches (a visit's and a
  check-in's customer joined through them), the names by `coalesce`; joins, not a lateral subquery. A new *API
  decisions* line (the `Memoize` miss, 2.5–8.4 s; 2026-10-27, #128). `git blame 3f8a2184` → the line was
  `1d43ef5b`'s. Folded into `feat(audit): read a space's audit log` → **`762f4cb0`**.

### F3 — `subscriptions.md`'s lock line

- Appended "The renewals not started with them, 2026-10-27, #128." (`git blame` → `47b3f2bd`). Folded into
  `fix(subscriptions): move unstarted renewals too` → **`2e808f76`**. The autosquash met two conflicts on the
  adjacent key line (which `36f03ca7` changes): each resolved by keeping that commit's key line and the lock line with
  F3's sentence (scripted; the lock line asserted equal but for the sentence).

### Runs (touched files only, by the owner's rule)

- `npm run test:api -w @masaha/api -- src/modules/audit/platformAuditLog.api.test.ts
  src/modules/space-links/staff/staff.api.test.ts src/modules/users/users.api.test.ts` → `Test Files 3 passed (3) ·
  Tests 40 passed (40)`.
- `npm run test:unit -w @masaha/api -- src/modules/users/users.service.unit.test.ts` → `Tests 9 passed (9)`.
- `npx prettier --check` (the touched code files) → "All matched files use Prettier code style!"; `npm run
  typecheck` → exit 0; `npm run lint` → exit 0; `npm run check:links` → "2909 links in 194 documents and 2066 source
  files all resolve." No shared change, so no shared build.

### Commits after the folds (base `39ef0504`, unchanged)

`2e808f76` fix(subscriptions): move unstarted renewals too (47) · `7a4e1da2` fix(subscriptions): refuse a key of
another space (49) · `0379377a` docs: correct the extension's key and history (45) · `762f4cb0` feat(audit): read a
space's audit log (37) · `4706968a` feat(audit): read the platform's audit log (42). No `fixup!`; subjects unchanged;
no `#PRNUM`; `git diff backup/audit-log-pre-review-fix HEAD` = the three fixes only (12 files, +100 −14). PR files:
34 → **41** (`git diff --name-only origin/main...HEAD`).

### Push and CI

- My `git push --force-with-lease=feat/audit-log:3f8a21845c3d435b845674d950dab2f5fc3bf7cd origin feat/audit-log`
  was refused by the session's permission classifier (Claude Code auto mode), not by git; not worked around. **The
  owner pushed it**: `git fetch` → `origin/feat/audit-log` = `4706968a` = `git rev-parse HEAD`.
- `gh pr checks 128 --watch` (bounded at 25 min) exit 0, on head `4706968a`: build (39s), check:classes (25s),
  check:conflicts (22s), check:links (26s), format:check (37s), lint (1m30s), test:api (6m45s), test:component
  (11m17s), test:unit (1m16s), typecheck (45s) — **all pass**; CodeRabbit skipping. Run 40658959435.
- `gh pr view 128` → head `4706968a`, `mergeStateStatus` **CLEAN** (UNSTABLE while the checks ran).
- PR description: `gh pr edit 128 --body-file …` — a *Review fixes (2026-10-28)* section before *Change type*: F1 (the
  sweep, the two writers, the route test red/green/break), F2, F3, the runs; verified by `gh pr view 128 --json body`.

### Decisions taken without the owner (this round)

1. **The autosquash on the merge-base, not on `origin/main`.** *Met:* the prompt's `rebase -i --autosquash
   origin/main` would also move the base to `0ec43b61`, while #128 was `CLEAN` (rebase only when not). *Options:*
   `origin/main`; the merge-base `39ef0504`. *Chose:* the merge-base: the folds without a rebase onto `main`.
   *Undo:* `git rebase origin/main` (merge-tree was clean).
2. **`receptionSpaceOf` a required dependency of `users`, not an optional one.** *Met:* `users` cannot import
   `space-links` (a level above). *Options:* optional with a `null` default; required. *Chose:* required: a
   forgotten wiring would silently put the space's entry back in the admin's log; the unit test passes a stub.
   *Undo:* make it optional in `Dependencies`.
3. **A reception link of any state names the space.** *Met:* the owner may deactivate the desk before its first
   sign-in. *Options:* the active link only; any. *Chose:* any: the account is still that space's staff's and its
   email was typed by that owner; the owner's log names a person also once their link ended. *Undo:* add
   `deactivatedAt: null` to `findReceptionSpaceOf`.
4. **F1's document lines dated 2026-10-28** (the day the rule became true), beside #128's 2026-10-27. *Undo:* the
   date.

### Branches

`backup/audit-log-pre-review-fix` (`3f8a2184`, made this round); earlier: `backup/audit-log-pre-prnum`,
`backup/feat-audit-log-pre-joins`. No rebase in progress; `git status --short` clean.
