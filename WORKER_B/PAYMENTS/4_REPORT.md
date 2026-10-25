# PAYMENTS — executor's report (`feat/payments`)

## Where the work stands
**Paused at §12.2 check 8 (the demo data, A1), before any commit.** The branch `feat/payments` is cut from
`origin/main` at `104d9d07` (`--no-track`); nothing edited, nothing committed.

## §12.1 — before the branch
- `C:\dev\masaha\app-b`: detached at `104d9d07` = `origin/main`, clean. ✔
- `git diff --name-status 104d9d07 origin/main`: empty — A2 holds. ✔
- `gh pr list --state open`: `[]` — no open PR (CONFLICT_GUARD not opened yet). ✔
- `0_CARRIED_FROM_*.md`: only `ANNOUNCEMENTS\0_CARRIED_FROM_112.md` (items 1–6, as the plan says); none in
  `PAYMENTS\`. ✔
- `apps/api/.env`: `masaha_b_dev`, `masaha_b_test`, `PORT=3321`. ✔ Docker `masaha-postgres-1` up (healthy).
- `npm run build -w @masaha/shared`: built. `prisma migrate status`: "25 migrations found … Database schema is
  up to date!" (masaha_b_dev, at `20261024095504_announcement_key`, #112's). ✔

## §12.2 check 8 — the demo data (A1) on `masaha_b_dev`: **does not hold**
`SELECT … FROM payments WHERE space_id = (masaha-demo) ORDER BY id` (at 2026-10-24 12:13 UTC) answers 14 rows,
not the seed's 6. Earlier items' real runs left their writes:
- **A payment received today** — id 18, visit 37 («زائر الإعلانات»), 8 agorot, CASH, 2026-10-24 11:02 UTC
  (14:02 Gaza), recorded by `demo-reception`. Case 2 ("reception's list today → `[]`, totals 0") cannot hold.
- **«رامي»'s visit (id 4) is paid in full** — id 15, 1,500 CASH, 2026-10-22, by `demo-reception`. Cases 4 and 9
  (reception pays 500 on «رامي»'s visit) are refused by the ledger's ceiling.
- **Case 1's hand-counted totals** (6 payments, 47,500 received) no longer match: ids 7, 8, 9, 11, 14, 15, 16
  are within the last 10 days too.
- Held: «هبة» (visit 2, MANUAL, no customer, 1,500, paid 1,500 by reception on 2026-10-03, id 1); the
  voided duplicate (id 4, «سُجّلت مرتين») and its live twin (id 5) on «يوم بعد يوم».

Per the exec prompt §1.8 and §12.2 check 8: stopped and reported; no data changed.

**The owner's answer (2026-10-24):** "Build; reseed before real run" — C0a–C4 and the breaks now; just before
§12.6, `db:reset` + `db:seed` (`SEED_DEMO=true`) on `masaha_b_dev` only, A1 re-checked, then the plan's cases
as written.

## Commits
- **C0a** `4a29404c` `fix(announcements): hold the period on start now` (48). Carried item 4.
  Red (T0, `npx vitest run --project api src/modules/announcements/lifecycle.api.test.ts` in `apps/api`):
  `AssertionError: expected 200 to be 422` — `Tests  1 failed | 4 passed (5)`. Green: `Tests  5 passed (5)`.
  lint exit 0, typecheck exit 0.
- **C0b** `f66794fc` `docs(announcements): state the public read` (42). Carried items 1, 2, 3, 5, 6.
  check:links "2678 links in 179 documents and 1787 source files all resolve."; lint 0; typecheck 0.
- **C1** `727059fc` `feat(db): keep a written-off visit's payments` (45).
  - Migration: `migrate dev --create-only --name payment_void_guard` run **once** → `20261024133344_payment_void_guard`
    (empty `migration.sql`, as expected); D9 written by `scripts\mkmig.py`, which copies `payments_guard_change`'s
    body byte for byte from `20260929120300_payments/migration.sql` (its only definition) and adds only D9's block.
    SQL read before applying. `masaha_b_test`: applied by the API lane's global setup ("Applying migration
    `20261024133344_payment_void_guard`"); `masaha_b_dev`: `npm run db:migrate` → "Your database is now in sync";
    `prisma migrate status` → "Database schema is up to date!". `\sf payments_guard_change` on `masaha_b_test` shows
    the new block. §12.2 check 5: `PERFORM … FOR SHARE` accepted by PostgreSQL ✔.
  - D1 red: **departure** — the lane's global setup applies pending migrations before any test, so D1 could not be
    run before the migration; its red was seen through **B4** (the old function restored on `masaha_b_test`):
    `AssertionError: promise resolved "{ id: 1, spaceId: 1, …(12) }" instead of rejecting` — `Tests  1 failed | 17
    passed (18)`. Restored (D9's statement re-run): `Tests  18 passed (18)`.
  - Catalogue lines (Q6) reworded, English and Arabic as approved. lint 0; typecheck 0; prettier clean.
- **C2** `37c33f97` `feat(payments): void a payment` (30).
  - U1 (void part) red, with `voidPaymentSchema` held back: `TypeError: Cannot read properties of undefined
    (reading 'parse')` — `Tests  1 failed (1)`; green `Tests  1 passed (1)`.
  - T1–T13 (`desk/void.api.test.ts`) red: **departure** — the code was written before the file was run, so the red
    was taken with the void's route held back (backed up, removed, restored): `Tests  12 failed | 1 passed (13)`
    (the passing one is T5, a 404 either way; its guard is B8). Green: `Tests  13 passed (13)`.
  - §12.2 check 2 (level rule): `npm run lint` exit 0 with `payments` → `users`, `customers`, `subscriptions` ✔.
    Check 3: `users` (295), `customers` (356), `subscriptions` (362) are built before `payments` (388) ✔.
    Check 7: `:paymentId` parsed by `parseId`, as `:visitId` ✔.
  - Breaks (`scripts\brk.py`, `c2-breaks.json`; each restored from its backup, sha256 "same", green after):
    - B5 audit removed → `AssertionError: expected [] to deeply equal [ { actorId: 1, …(6) } ]`
    - B6 `requireCan('payments.void')` removed → `expected 422 to be 403`
    - B7 "voided already" branch removed → `expected 500 to be 200`
    - B8 `lockIn` without the space filter → `expected 500 to be 404`
    - B9 `can()` on `space.links` → `expected 200 to be 403`
    - B10 `voided_at IS NULL` dropped (subscriptions branch) → `expected { id: 1, customerId: 1, …(25) } to match object { Object (paidAgorot, balanceAgorot) }`
    - B11 the same on the visits branch → `expected { debtAgorot: +0, …(2) } to deeply equal { debtAgorot: 2000, …(2) }`
    - B12 the void by the item (`updateMany` on `visitId`) → `expected { payments: [ …(4) ], …(2) } to deeply equal …`
      (first attempt did not compile — my break's own defect, an `await` in a non-async method — remade and run)
    - B13 `FOR UPDATE` removed → `expected 500 to be 200`
    - B14 `lockAtDesk` skipped → `Error: 1 request(s) never waited on a lock`
    - B23 `findByKey` skipped in `receivePayment` → `expected 500 to be 201`
    - B4 on T7 (old function on `masaha_b_test`) → both written-off tests `expected 200 to be 409`; restored
      (D9 re-run) → `Tests  2 passed | 11 skipped (13)`.
  - lint 0; typecheck 0; check:links "2689 links … all resolve."; prettier fixed two files, then the two test files
    re-run green.
- **C3** `13540a50` `feat(payments): show a voided visit uncollected` (47).
  - T15 red before D8: `AssertionError: expected [] to deeply equal [ { id: 1, paidAgorot: +0, …(1) } ]` —
    `Tests  1 failed | 6 passed (7)`; green `Tests  7 passed (7)`. Q1's test (a manual, unpriced, customer-less
    visit not listed) passed before the code too (nothing listed manual visits then); its guard is BQ1.
  - **Departure (an existing test's fixture):** `uncollected.api.test.ts`' first test built a manual, priced,
    customer-less, unpaid visit and asserted it is never listed. That state is unreachable (data model *Checked by
    the service*: a manual check-out's unpaid rest has a customer) and, under the approved D8, is exactly what is
    now listed. The fixture now gives it a customer (its rest a customer's debt), the title says so; the test's
    intent is kept.
  - Breaks: B15 (predicate back to `AUTO`) → `expected [] to deeply equal [ { id: 1, … } ]`; **BQ1** (Q1's
    priced-only clause dropped) → `expected [ { id: 1, paidAgorot: +0, …(1) } ] to deeply equal []`;
    **B16 stayed green** — `checked_out_at IS NOT NULL` dropped alone cannot change the outcome: an open visit has
    no charge (`visits_charge_check`) and no method (`visits_checkout_method_check`), so the approved predicate
    already leaves it out. **Departure:** the break that can, B16b (that clause and Q1's together) →
    `expected [ …(2) ] to deeply equal [ { id: 1, … } ]` (the open visit listed). All restored, sha256 "same".
  - The shared `UncollectedVisit` comment updated (one file beyond §7's C3 list, same PR).
  - lint 0; typecheck 0; check:links 0.
- **C4** `05504d53` `feat(payments): list a space's payments` (39).
  - U1 (query part) red with `paymentsQuerySchema` held back: `TypeError: Cannot read properties of undefined
    (reading 'parse')` — `Tests  1 failed | 1 passed (2)`; green `Tests  2 passed (2)`.
  - U2 red: `Error: Cannot find module './paymentsWindow.ts'` (`Tests  no tests`: the module not written yet — the
    plan's red step); green `Tests  1 passed (1)`. Its assertions are proven by B2 and B3.
  - T16–T23 (`payments/list.api.test.ts`) red with the `GET /payments` route held back: `Tests  8 failed (8)`;
    green `Tests  8 passed (8)`.
  - §12.2 check 4 ✔: `GET …/payments` reaches the payments' router (T16 green) and `POST` is still the desk's
    (`desk/payments.api.test.ts` `Tests  18 passed (18)`). Check 6 ✔: `meta` typed `PaymentsMeta` in a variable,
    assignable to the helper's `PaginationMeta`; the helper unchanged.
  - **Departure:** `createPaymentsService` gains `now` (the one clock, conventions §11) besides D10's three
    dependencies — the list's "today" needs it; `app.ts` passes `clock`.
  - Breaks (all red, restored sha256 "same", green after):
    - B1 the 92-day bound removed → `expected null to deeply equal { to: [ 'out_of_range' ] }` (U1; T22 is the
      same schema at the route)
    - B2 `to` exclusive of its own day → `expected { Object (from, to) } to deeply equal { Object (from, to) }`
    - B3 the UTC date for today → the same line
    - B17 `orderBy` id ascending → `expected [ 2, 3, 1 ] to deeply equal [ 3, 2, 1 ]`
    - B18 the window's `lt` as `lte` → `expected [ 7, 6, 3, 2, 1, 5 ] to deeply equal [ 6, 3, 2, 1, 5 ]`
    - B19 the totals from the page's rows → `expected { Object (count, receivedAgorot, ...) } to deeply equal …`
    - B20 `voidedAt: null` dropped from the received sum → the same line
    - B21 the narrowing skipped → `expected [ 5, 4, 2, 1 ] to deeply equal [ 2, 1 ]`
    - B22 reception's refusal removed → `expected 200 to be 403`
    - B24 the `spaceId` filter dropped → `TypeError: Cannot read properties of undefined (reading 'map')` (the
      request answered 500: another space's visit has no name here)
  - lint 0; typecheck 0; prettier clean; check:links "2694 links in 179 documents and 1793 source files all resolve."
- **Size:** 39 files from `104d9d07` (≤ 58).
- **`origin/main` moved meanwhile:** #113 (`chore/conflict-guard`) merged at `5c0cdcba`; its files (CI, `CLAUDE.md`,
  `package.json`, `apps/api/scripts/`, findings 137–138 and index, `docs/development/{setup,workflow}.md`,
  `docs/frontend/architecture.md`, `docs/features/lookups.md`, `docs/design/INDEX.md`) share none with this branch;
  not rebased (rebase only when dirty).

## §12.4 Verification on the head `05504d53`
- Free memory before the lanes: 5,413,016 KB; worker A's `vitest run --project component` (in `C:\dev\masaha\app`)
  was running — waited for it to end (a bounded background check), never stopped it.
- `npm run lint` → exit 0 · `npm run typecheck` → exit 0 (both on the C4 tree, identical to the head).
- `npm run test:unit` (free 5,175,924 KB) → exit 0: shared `Test Files  23 passed (23)` / `Tests  255 passed (255)`;
  api `Test Files  65 passed (65)` / `Tests  865 passed (865)`; web `Test Files  115 passed (115)` / `Tests  918
  passed (918)`.
- `npm run test:api` (free 2,594,080 KB, then 3,070,084 KB, no vitest running): **killed twice** with no result
  (`npm error code 4294967295` after "No pending migrations to apply."). First read as a memory kill; **the cause
  was my own command's 600 s timeout**: the lane takes ~9.5 minutes. The lane's own command (`vitest run --project
  api`, the api workspace's `test:api` script, run in `apps/api` with no timeout; free 4,758,896 KB) → exit 0:
  `Test Files  84 passed (84)` / `Tests  1156 passed (1156)`, `Duration  558.69s`. (Before it, the touched folders
  alone — payments, desk, db, announcements, subscriptions — `Test Files  31 passed (31)` / `Tests  298 passed
  (298)`, as evidence only.) `masaha_b_test` migrated by the lane's setup ("No pending migrations to apply.").
- `npm run format:check` → exit 0, "All matched files use Prettier code style!" · `npm run check:links` →
  "2694 links in 179 documents and 1793 source files all resolve." · `npm run build -w @masaha/shared` → exit 0.
- `git grep -n "#PRNUM"`: documents, and **the migration's comment** (D9's own text carries `#PRNUM`) — see §12.7.
- `git diff --stat 104d9d07 HEAD -- apps/web`: only the two `errors.ts`, one line each ✔ ·
  `-- package.json package-lock.json`: empty ✔.
- **Not run locally (CI judges):** `test:component`, the web's `build`, `check:build`, `check:classes`.

## §12.7 (first part) — the PR number, before the real run
- **Departure (order):** `#PRNUM` was replaced **before** the real run, not after it: D9 puts `#PRNUM` in the
  migration's comment, and rewriting the migration after it is applied changes its checksum; reseeding
  `masaha_b_dev` after the rewrite gives it the final file's checksum.
- `scripts\prnum.sh` (from `SUBSCRIPTIONS\scripts\prnum-fix109.sh`: branch `feat/payments`, backup branch
  `backup/payments-pre-prnum`, description `scripts\pr-body.md`, its checks kept). **Departure:** it rewrites
  `apps/api/prisma/migrations` as well as `docs` (the migration's one `#PRNUM`). Next number checked with
  `gh pr list --state all --limit 1` → #113, so 114. Output: `PRNUM OK #114 8ae243f0 (was 05504d53)`; `git diff
  --stat backup/payments-pre-prnum HEAD` → 9 files, 34 lines each way, the number only.
- Commits after the rewrite: `ab31e0f4` C0a · `51fdbb81` C0b · `7a9fffd8` C1 · `811aa7a4` C2 · `d15a4d05` C3 ·
  `8ae243f0` C4 (the head).
- The migration's checksum is the file's SHA-256 (the old file's `9b253eae…` = both databases' stored value). The
  comment lies outside the function body, so the function is unchanged. `masaha_b_test`: its
  `_prisma_migrations.checksum` row set to the new file's (`65deadd9…`), guarded by the old value — `UPDATE 1`.
  `masaha_b_dev`: reset (below), which applied the new file (`65deadd9…`).

## §12.6 The real run (API on 3321, `masaha_b_dev`)
- **Reseed, as the owner decided:** `prisma migrate reset --force` was refused by Prisma ("detected that it was
  invoked by Claude Code"); the owner consented explicitly ("Yes, reset masaha_b_dev"), passed as
  `PRISMA_USER_CONSENT_FOR_DANGEROUS_AI_ACTION` → "Database reset successful", 26 migrations applied; `npm run
  db:seed` → "Seeded the lookups, the admin account and the settings. Seeded the demo space. Seeded the
  directory's demo set."; `migrate status` → "Database schema is up to date!". (An earlier `db:seed` before the
  consent changed nothing: "The demo space exists; left unchanged.")
- **A1 re-read ✔:** six payments — «هبة»'s 1,500 cash by `demo-reception` 2026-10-23; 6,000; 10,000 transfer; the
  voided 20,000 («سُجّلت مرتين») and its live twin; 10,000 by the owner; none today (2026-10-24). «رامي»'s visit
  (`MANUAL`, customer 5, 1,500) unpaid.
- `curl.exe -s http://localhost:3321/health` → `{"status":"ok","db":"up",…}`. Signed in as `demo-owner@`,
  `demo-reception@`, `demo-directory-owner@example.com` (the password read from `.env`, never printed).
- `node scripts\realrun1.mjs` → exit 0, every line PASS, `ALL PASS`:
  1 owner's ten days: six newest first, totals 47,500 (cash 37,500, transfer 10,000), count 5, voided 1/20,000, the
    duplicate's reason «سُجّلت مرتين» and its voider's name · 2 reception today `[]`, totals 0 · 3 reception's range
    403 · precondition رامي owes 1,500 · 4a reception pays 500 → 201, balance 1,000 · 4b its list: that one, 500 cash ·
    5 reception's void 403 · 6a owner voids «هبة» → 200, R1 · 6b again with R2 → 200, R1, the same answer · 6c
    uncollected: «هبة», balance 1,500 · 7a/7b directory owner: list 404, void 404 · 8a owner voids case 4's → 200 ·
    8b reception's list: it, voided; received 0, voided 1/500 · 9a reception pays 500 more → 201 · 9b write-off 200 ·
    9c the void 409 `VISIT_WRITTEN_OFF` · 9d undo 200 · 9e the void 200.
- `audit_logs` (latest first): `payment.voided` 8 · `visit.writeOffUndone` 4 · `visit.writtenOff` 4 ·
  `payment.recorded` 8 · `payment.voided` 7 · `payment.voided` 1 · `payment.recorded` 7 — three voids, none for
  case 6's second call. Payments: 1 voided (R1), 4 voided (seed), 7 voided, 8 voided; 2, 3, 5, 6 live.
- **The run's writes (masaha_b_dev):** payments 7 and 8 (500 each on «رامي»'s visit, by reception), both voided by
  the owner; «هبة»'s payment 1 voided; «رامي»'s visit written off and the write-off undone.
- Server stopped by process id (4820 the server, 22476 `tsx watch`, 20876 `pino-pretty`); port 3321 free;
  `server.log` deleted.

## §12.7 Push and PR
- Before the push, on the rewritten head `8ae243f0`: `npm run check:links` → "2694 links in 179 documents and 1793
  source files all resolve."; `npm run format:check` → "All matched files use Prettier code style!"; `git grep
  "#PRNUM"` → nothing. Subjects: 48, 42, 45, 30, 47, 39; no attribution trailer.
- `git push -u origin feat/payments` → new branch. Labels `feat`, `area:api`, `area:docs`, `area:web` exist.
- `gh pr create` → **https://github.com/Basel-Ghonaim/masaha/pull/114** — the number the documents carry ✔.
  Description: `scripts\pr-body.md`.

## §12.8 Conflicts
- Open PRs: only #114. `git merge-tree --write-tree HEAD origin/main` (main at `5c0cdcba`, #113 merged) → clean.
- `git status --short` clean. Local backup branch left by the script: `backup/payments-pre-prnum` (at `05504d53`).

## Observations for the owner (not findings; nothing recorded in the repository)
- **The two ranged lists count 92 days differently.** The plan's U1 gives the payments list 92 days with both ends
  counted (`to ≤ from + 91`), built so. The check-ins list it names as the precedent allows `to ≤ from + 92`
  (`CHECK_IN_RANGE_MAX_DAYS`, `subscriptions/requests.ts`): 93 days counted. One of them may want aligning; it would
  be finding 170 if recorded.
- `checked_out_at IS NOT NULL` in D8's predicate is implied by the database once Q1's priced-only clause is in
  (B16 green): kept, as the plan writes it, as a guard should those constraints change.

## CI on the pushed head `8ae243f0`
- `gh pr checks 114`: pass — format:check, test:component, check:classes, lint, typecheck, test:unit, check:links,
  check:conflicts, build, test:api, CodeRabbit. `gh pr view 114` → head `8ae243f07cfa…` = local HEAD,
  `mergeStateStatus` **CLEAN**. (`check:build` runs inside CI's `build` job.)
- **Status: DONE** — ready for review, not merged.
