# DESK PR 3 — `feat/auto-checkout` — the executor's report

> Written as the work goes. Worker B, `C:\dev\masaha\app-b`, 2026-10-20.

## Precondition and 12.1 Before the branch

- `gh pr view 95 --json state` → `MERGED`, merge commit `f77d2012`.
- `git status --short --branch` → `## HEAD (no branch)`, clean; `origin/main` = `f77d2012`.
- `git diff --name-status eff0a3d1 origin/main`: the code files are PR 1's and PR 2's (as the plan and A1 say: `visits`,
  `payments`, `desk`, `customers`, `subscriptions`, `announcements`, `occupancy`, `directory`, `shared/auth|errors|http`,
  `db/checkViolation.ts`, the migration, `packages/shared` core/occupancy/directory/visits/payments/desk,
  `eslint.config.js` (PR 1's `@date-fns/tz` rule), `package-lock.json`); the rest is #93's web and documents. Nothing else.
- Open PRs: **#96** `feat/owner-space-profile` (worker A, OWNER_SETUP PR 1, head `677d7822`): non-web files are documents
  only — `docs/README.md`, findings 67 and 99 and the findings index, `lookups.md`, `spaces.md`, `frontend/architecture.md`,
  `overview.md`. Shared with this PR: the findings index (finding 100), `spaces.md` (C1's code map line), `overview.md`.
- `git switch --no-track -c feat/auto-checkout origin/main` → switched. `docker start masaha-postgres-1` → ok.
  `npm run build -w @masaha/shared` → exit 0. `apps/api/.env`: `masaha_b_dev`, `masaha_b_test`, `PORT=3321` (by pattern,
  3 lines); no `JOBS_SECRET` yet. `prisma migrate status` → `Database schema is up to date!`.
- Free memory before the first focused run: 4,015,604 KB; no `vitest`/`tsc` of worker A running.

## C0 (carried from #95) — `7aee9175 fix(desk): refuse a check-out before its check-in` (49)

- Tests in `desk/checkOut.api.test.ts`: new `a check-out time before the visit's check-in is refused (422 out_of_range),
  writing nothing` (item 1); T20 becomes `… answers it closed without a payment, and refuses one with 409
  VISIT_ALREADY_CLOSED`; T21 becomes `… record one payment; the other is refused, its cash unrecorded` (item 5).
- **Red first:** `Tests  3 failed | 17 passed (20)` — `AssertionError: expected 200 to be 409`; `AssertionError: expected
  500 to be 422` (item 1's 500, as the review said); `AssertionError: expected [ 200, 200 ] to deeply equal [ 200, 409 ]`.
- Code: `desk.service.ts` — closed by another key with a `payment` → `AppError.conflict('VISIT_ALREADY_CLOSED')`; a priced
  time before `locked.checkedInAt` → 422 `out_of_range` on `checkedOutAt`. New code `VISIT_ALREADY_CLOSED` by
  `add-error-code`: `core/errors.ts`, both catalogues, api-contract §6, the tests provoke it.
  - EN "This visit was already checked out; this payment was not recorded."
  - AR "سُجّل خروج هذه الزيارة من قبل، ولم تُسجَّل هذه الدفعة." (**for the owner's approval**)
- **Green:** `Test Files  1 passed (1)`, `Tests  20 passed (20)`.
- **Breaks** (`scripts\brk.py carried.json`; backup, one edit, the file, restore, SHA-256 checked):
  - comparison with the check-in removed → `Tests  1 failed | 19 passed (20)` — `AssertionError: expected 500 to be 422`
  - the closed visit's payment refusal removed → `Tests  2 failed | 18 passed (20)` — `expected 200 to be 409`;
    `expected [ 200, 200 ] to deeply equal [ 200, 409 ]`
- Documents: item 2 `security.md` ("its own `can()` action, owner-only or the staff's"); item 3 `visits.md` (*Asks*
  `can()` for the terms; *Leaves* the decision under the lock to `desk`); item 4 = review nit 6 (the contract's
  `roundingRule` comment: "or when the charge is the day price alone"); item 5 in the contract (retry line, the errors
  line, §6), `desk.md` (flow, two decisions, history); item 6 → **finding 100** (file + index under *Open*).
- Review nits **not** taken in this commit (item 4 leaves the judgment to me): nit 7 (one `presentIn` helper) — in
  `occupancy`, which PR 3 does not touch, and a refactor of three call sites, not small; nit 8 (a key that closed a
  visit unpaid is not remembered) — a rule change, the owner's; nit 9 (charge overflow) — "record or ignore", plausible
  only, PR 3's auto check-out bounds the stay to one Gaza day; nit 10 — no fix (history).
- `npm run lint` → exit 0 · `npm run typecheck` → exit 0 · `format:check` → `All matched files use Prettier code style!`
  · `check:links` → `2402 links in 147 documents and 1392 source files all resolve.`

## C1 — `212887b9 feat(spaces): compute the auto check-out time` (45)

- U1–U8 (`spaces/autoCheckout.unit.test.ts`, 8 tests). **Red** with a stub answering `null` → `Failed Tests 7`
  (`AssertionError: expected null to deeply equal 2026-10-18T15:00:00.000Z`, …; U4 expects `null` and passed).
  **Green** → `Tests  8 passed (8)`.
- U7's daylight-saving day from Node's zone data: `2026-03-28T00:00Z → +03:00`, `2026-10-23T23:00Z → +02:00`
  (Saturday 2026-10-24 at 02:00); a check-in at 01:00 (+03:00) is due at 23:59 (+02:00).
- **B1** `max` for `min` → `Tests  2 failed | 6 passed (8)` — `expected 2026-10-18T15:00:00.000Z to deeply equal 2026-10-18T08:50:00.000Z`
- **B2** the closing read from the run's day (`gazaClockOf(new Date())` — the pure rule takes no run time, so the
  run's day is the real clock's) → `Tests  6 failed | 2 passed (8)` — `expected 2026-10-20T20:59:00.000Z to deeply equal 2026-10-18T15:00:00.000Z`
- `spaces.service.autoCheckoutDue` passes it through; the `SpacesService` fake in `space-links.service.unit.test.ts` gains it.
- Documents: data model *Auto check-out* (D-PR3-1, `#PRNUM`); `spaces.md` code map.
- `npm run lint` → exit 0 · `npm run typecheck` → exit 0.

## C2 — `3ba3b63f feat(jobs): close open stays automatically` (42)

- Tests: U9 `shared/jobs/secret.unit.test.ts`; U10 in `config/env.unit.test.ts` (the production fixtures gain
  `JOBS_SECRET`, the defaults `JOBS_SECRET: undefined`); T1–T4 `shared/jobs/jobs.api.test.ts`; T5–T13
  `visits/autoCheckOut.api.test.ts`.
- **Red first** — API (services built, the endpoint not yet mounted): `Tests  12 failed | 1 passed (13)` —
  `AssertionError: expected 404 to be 200` ×9, `expected 404 to be 401`, `expected 404 to be 500`, `Error: 1 request(s)
  never waited on a lock` (T3 expects 404 and passed). (A first attempt before the services' dependencies were wired
  crashed every test with `TypeError: Cannot destructure property 'runInTransaction'` — not counted as the red.)
  Unit (`env.ts` from `HEAD`, `matchesSecret` stubbed `true`): `Tests  2 failed | 16 passed (18)` — `expected undefined to
  be 'a-jobs-secret-of-at-least-32-characte…'`; `expected true to be false`.
- **Green:** API `Test Files  2 passed (2)`, `Tests  13 passed (13)`; unit `Tests  18 passed (18)`.
- **Breaks** (`scripts\brk.py c2.json`, each restored, SHA-256 ok):
  - **B3** `header.includes(secret)` → `Tests  1 failed (1)` — `expected true to be false`
  - **B4** production list without `JOBS_SECRET` → `Tests  1 failed | 16 passed (17)` — `expected [Function] to throw an error`
  - **B6** secret check removed → `Tests  1 failed | 3 passed (4)` — `expected 200 to be 401`
  - **B7** mounted always → `Tests  1 failed | 3 passed (4)` — `expected 401 to be 404`
  - **B8** the `try` per job removed → `Tests  1 failed | 3 passed (4)` — `expected [] to match object [ { level: 50, …(2) } ]`
  - **B9** `checkedOutAt = now` → `Tests  4 failed | 5 passed (9)` — `expected { id: 1, spaceId: 1, …(19) } to match object { …(8) }`
  - **B10** the still-open checks removed — **two edits** (the open read's `checkedOutAt: null` and the lock's
    `checked_out_at IS NULL`): the plan's single edit cannot fail T6, since the open read never returns a closed
    visit → `Tests  2 failed | 7 passed (9)` — `expected { visits: 1, remaining: +0 } to deeply equal { visits: +0, remaining: +0 }`
  - **B2 (API side)** the due read from the run's day → `Tests  6 failed | 3 passed (9)` — `expected { visits: +0, remaining: +0 } to deeply equal { visits: 2, remaining: +0 }`, …
  - **B11** — the plan's "settings read at check-in" has no code form (no setting is stored on a visit); made instead
    as **the stay limit not read at the run** (`maxStayMinutes: null`) → `Tests  1 failed | 8 passed (9)` —
    `expected { id: 1, spaceId: 1, …(19) } to match object { …(2) }`
  - **B12** subscriptions' job not registered → `Tests  1 failed | 8 passed (9)` — `expected undefined to deeply equal { …(2) }`
  - **B13** no `FOR UPDATE` → `Tests  1 failed | 8 passed (9)` — `expected { visits: 1, remaining: +0 } to deeply equal { visits: +0, remaining: +0 }`
- §12.2 check 1 (the compare): `timingSafeEqual` on the SHA-256 digests of the header and `Bearer <secret>` ✔.
  Check 3 (404 without the secret): T3 ✔. Check 4 (levels): `npm run lint` → exit 0 with `subscriptions` importing
  `spaces` and `space-settings`, `shared/jobs` importing no module ✔.
- Code beyond the plan's table: `space-settings.repository.findMany` (for `settingsFor`); the visits service takes
  `runInTransaction`; **two jobs** registered (`visits.autoCheckOut`, `subscriptions.autoCheckOut`) where the plan names
  one `autoCheckOut` — T4 needs one module's failure to leave the other's closings done.
- Documents: api-contract *Internal* (new section); conventions header (*Built* + the scheduler) and §12's row; security
  (*HTTP hardening* `JOBS_SECRET`, header); setup *Timed jobs* (the runbook line); `.env.example`; data model *Auto
  check-out*; `visits.md` (flow, three decisions, code map, history); `desk.md` (one line); overview; v1-mvp (*Built*,
  *Settles* done).
- `check:links` → `2416 links in 147 documents and 1402 source files all resolve.` · `format:check` → pass ·
  `npm run lint` → exit 0 · `npm run typecheck` → exit 0.

## C3 — `6286a667 feat(visits): price an unpriced visit` (37)

- **A1's remainder, read on #95's code:** the unpriced close (Q4's branch), `VISIT_NOT_PRICED` and T14–T17 are in
  `desk.service.ts` / `checkOut.api.test.ts` already (seen; the four tests pass in this branch). C3 keeps the reads and
  the pricing: `unpricedIn`, `price`, `GET …/unpriced-visits`, `PUT …/visits/:visitId/charge`, `VISIT_ALREADY_PRICED`,
  T18–T23. Subject changed from the plan's `feat(visits): close a visit unpriced` (that close is #95's) — a departure.
- Tests: `visits/unpriced.api.test.ts` (T18–T23, plus `refuses an invalid body with 422 before anything is written`);
  `packages/shared/src/visits/requests.unit.test.ts` + `a visit's price typed by hand … 1 to 10,000,000 whole agorot and a
  reason of 1–200 characters`.
- **Red first:** API, before the routes → `Tests  6 failed | 1 passed (7)` — `expected 404 to be 200` ×2, `expected 404 to
  be 403`, `expected 404 to be 409`, `expected 404 to be 422`, `Error: 1 request(s) never waited on a lock` (T22 expects
  404 and passed). Shared, with `priceVisitSchema = z.any()` → `Tests  1 failed | 1 passed (2)` — `expected { amountAgorot:
  1500, …(1) } to deeply equal { amountAgorot: 1500, …(1) }`.
- **Green:** `unpriced.api.test.ts` + `checkOut.api.test.ts` → `Test Files  2 passed (2)`, `Tests  27 passed (27)`;
  shared visits + desk requests → `Tests  3 passed (3)`.
- **Breaks** (`scripts\brk.py c3.json`):
  - **B16** pricing's `can()` as the staff's → `Tests  1 failed | 6 passed (7)` — `expected 200 to be 403`
  - **B17** the charge check removed → `Tests  1 failed | 6 passed (7)` — `expected 200 to be 409`
  - **B18** `can()` on `space.links` → `Tests  1 failed | 6 passed (7)` — `expected 200 to be 403`
- `VISIT_ALREADY_PRICED` by `add-error-code` (EN "This visit already has a price." / AR "لهذه الزيارة سعر بالفعل.", §13 Q2's
  lines, approved with the plan); api-contract §6; T21 provokes it.
- Departure: `priceVisitSchema` in `@masaha/shared/visits` (amount bound `PRICE_MAX_AGOROT`, 10,000,000, the same value
  as `PAYMENT_MAX_AGOROT`), and the check-out's `charge` reuses it; `CHARGE_REASON_MAX_LENGTH` moves from `desk` to
  `visits` (`desk/requests.ts` edited: one home for the typed price's rule; desk's U10 still green).
- The route asks `requireCan('attendance.record')` (the staff's): `prices.typeByHand` needs the space's switch, which
  `requireCan` cannot read; the service decides it under the lock (403 `PRICE_TYPING_NOT_ALLOWED`).
- Documents: api-contract (the two routes, §6), data model (*Unpriced visit*), security (the pricing's authorization),
  `visits.md` (what it does, boundary, flow, decision, code map, history), `desk.md` (one line).
- `lint` → exit 0 · `typecheck` → exit 0 · `check:links` → `2417 links in 147 documents and 1403 source files all resolve.` · `format:check` → pass.

## C4 — `9ff1d473 feat(payments): list uncollected visits` (39)

- Tests: U11 `payments/balance.unit.test.ts`; T24–T27 `payments/uncollected.api.test.ts`.
- **Red first:** unit, with `balanceOf` stubbed `null` → `Tests  1 failed (1)` — `expected null to be 2000`; API, before
  the route → `Tests  4 failed (4)` — `expected 404 to be 200` ×2, `TypeError: Cannot read properties of undefined
  (reading 'map')` ×2 (the 404's envelope has no data).
- **Green:** API `Tests  4 passed (4)`; unit `Tests  1 passed (1)`.
- **Breaks** (`scripts\brk.py c4.json`):
  - **B5** `paid − due` → `Tests  1 failed (1)` — `expected -2000 to be 2000`
  - **B19** the `AUTO` filter dropped (the page) → `Tests  1 failed | 3 passed (4)` — `expected [ …(5) ] to deeply equal [ …(3) ]`
  - **B20** voided payments summed → `Tests  1 failed | 3 passed (4)` — `expected [] to deeply equal [ { id: 2, paidAgorot: +0, …(1) } ]`
  - **B21** the settled ids filtered after the page → `Tests  1 failed | 3 passed (4)` — `expected { currentPage: 1, limit: 1, …(4) } to deeply equal …`
- §12.2 check 4: `payments` importing `visits` → `npm run lint` exit 0 ✔.
- `app.ts`: `payments` built once with `visits` (was inline in the desk's deps), its manage router mounted.
- Documents: api-contract (the route, `UncollectedVisit`), conventions §9's uncollected line (D-PR3-4), data model
  (*Uncollected visits*: the unpriced included), `payments.md`, `visits.md`, overview, v1-mvp (*Built*: the step's API
  built; the surface's `GET …/visits` row narrowed to its date range).
- `lint` → exit 0 · `typecheck` → exit 0 · `check:links` → `2421 links in 147 documents and 1408 source files all resolve.` · `format:check` → pass.

## 12.4 Verification on the head
- Before each lane: no `vitest`/`tsc` running anywhere (worker A's included); free memory 4,620,840 KB (unit), 3,450,752 KB (api).
- On `9ff1d473`: `npm run test:unit` → exit 0: shared `Tests  230 passed (230)`, api `Tests  783 passed (783)`, web
  `Tests  842 passed (842)`. `npm run test:api` → exit 0: `Test Files  62 passed (62)`, `Tests  961 passed (961)`.
  `format:check` → pass; `check:links` → `2422 links …`; `build -w @masaha/shared` → exit 0.
- **`origin/main` moved meanwhile:** #96 (worker A, OWNER_SETUP PR 1) merged at `c91f5b42` (web and documents only:
  `git diff --name-only f77d2012 origin/main` outside `apps/web` and `docs` → nothing). `git merge-tree` → conflicts in
  `docs/architecture/findings/README.md` (finding 99 beside 100) and `docs/features/spaces.md` (the header line next to
  *Last Updated*). **Rebased** on `c91f5b42` (the documents' fast path): kept both index lines; took #96's header line
  (mine changed only *Last Updated*, already 2026-10-20 there). `git rebase -x "lint && typecheck"` → `CHECK-OK` on each
  of the 5 commits, `Successfully rebased`. Head `9e79aee0`.
- Re-run on `9e79aee0` because files they cover changed (the web from #96, the documents): `npm run test:unit` → exit 0:
  shared `230 passed`, api `783 passed`, web `Tests  858 passed (858)`; free memory 4,921,744 KB before it.
  `format:check` → `All matched files use Prettier code style!`; `check:links` → `2433 links in 148 documents and 1426
  source files all resolve.`; `build -w @masaha/shared` → exit 0. **`test:api` not re-run:** no file it covers changed
  (#96 touched no `apps/api` or `packages/shared` file); its pass above stands for the same API and shared code.
- `git grep -n "#PRNUM"` → documents only (8 files). `git diff --stat $(merge-base) -- apps/web` → only the two
  `errors.ts` catalogues; `-- package.json package-lock.json` → empty.
- Not run, with why: `test:component`, the web's `build`, `check:build`, `check:classes` — the web change is two
  catalogue files of strings, whose parity the typecheck enforces; CI runs them.

## 12.2 check 2 — the timer leaves no handle
- `npx tsx scripts\timer-check.ts` (imports `startEvery` from the source, starts it every 5 minutes, logs its own exit)
  → `timer started`, `exited after 79 ms`: the process ends at once with the timer running, so the timer never holds
  it open (`unref`). (Stopping the dev server by process id on Windows cannot show a graceful exit.)

## 12.6 The real run — API on 3321, `masaha_b_dev` (2026-10-20, ≈ 14:35 in Gaza)
- `JOBS_SECRET` set in `apps/api/.env` to a random 43-character value (`crypto.randomBytes(32)`, base64url), never
  printed; `npm run dev -w @masaha/api` in the background (log to `scripts\server.log`).
- `scripts\realrun3.mjs` (secrets read from `.env` into variables, never printed):
  - `/health` → `{"status":"ok","db":"up",…}`.
  - **The timer's own first run**, 10 s after start: two `job ran` lines at 14:34:39 (it closed the demo's old open
    visit and check-in: `visit.autoCheckedOut`, `checkIn.autoCheckedOut` in the audit).
  - Signed in as `demo-owner` (2) and `demo-reception` (3); space 1. Settings before: `maxStayMinutes` 240,
    `receptionMayTypePrices` true. `PATCH …/settings { maxStayMinutes: 60 }` → 200.
  - Visit 10 inserted through `psql`, checked in 3 hours ago at 5 ₪ / 25 ₪.
  - `POST /internal/jobs/run` without the secret → **401** (`unauthorized`); with a wrong one → **401**; with it → **200**
    `{"ranAt":…,"jobs":[{"name":"visits.autoCheckOut","done":{"visits":1,"remaining":0}},{"name":"subscriptions.autoCheckOut","done":{"checkIns":0,"remaining":0}}]}`.
  - Visit 10: `checked_in_at 08:34:58.629Z`, `checked_out_at 09:34:58.629Z` (**check-in + 1 h**), `AUTO`, charge 500.
  - Again → 200 `visits: 0`, `checkIns: 0`.
  - `GET …/uncollected-visits` (owner) → 200, total 3, visit 10 listed `paidAgorot 0`, `balanceAgorot 500`.
  - Switch off (`PATCH …/settings { receptionMayTypePrices: false, maxStayMinutes: null }` → 200); a visit with no rate
    inserted; reception's check-out with `phone: "0599000123"` → **200**, `charge: null`, `MANUAL`, customer 6 (found).
  - `GET …/unpriced-visits` → 200, lists it. Reception's `PUT …/charge` → **403 `PRICE_TYPING_NOT_ALLOWED`**; the owner's
    → **200** (`amountAgorot 1000`, `typedById 2`, `reason "Real run"`); again → **409 `VISIT_ALREADY_PRICED`**.
  - Settings put back (`maxStayMinutes` 240, switch on) → 200.
  - Audit (newest first): `space.settingsEdited, visit.priced, visit.checkedOut, space.settingsEdited,
    visit.autoCheckedOut, space.settingsEdited, checkIn.autoCheckedOut, visit.autoCheckedOut, …`.
- Left in `masaha_b_dev` (demo data): visits 10 and 11 closed (11 priced 1,000, left to customer 6); the demo's visit 1
  and check-in 4 closed by the timer's first run.
- **The timer's next run:** `job ran` ×2 at **14:39:29**, five minutes after the start's tick (14:34:29 + 10 s first
  run at 14:34:39) — the in-process interval works.
- Stopped by process id (tsx watch 21800, the server 16032, pino-pretty 14384); `Get-NetTCPConnection -LocalPort 3321`
  → nothing: port 3321 free (the background task then reports exit 127, as before).
- **`JOBS_SECRET` removed from `apps/api/.env` afterwards** (added only for the run); the server log (which shows no
  secret) deleted with it.

## 12.7 The PR number, push and PR
- 56 files against `origin/main` (§14's "about 70" not reached). Next number from GitHub: **97**.
- `git filter-branch` replaced `#PRNUM` → `#97` in each commit's documents (8 files, 23 lines); `git grep -n '#PRNUM'` →
  nothing; `check:links` → `2433 links …`, `format:check` → pass again.
- Commits: `a750897f fix(desk): refuse a check-out before its check-in` (49) · `be220604 feat(spaces): compute the auto
  check-out time` (45) · `e1c8a2b2 feat(jobs): close open stays automatically` (42) · `47f344a0 feat(visits): price an
  unpriced visit` (37) · `e122b95d feat(payments): list uncollected visits` (39).
- `git push -u origin feat/auto-checkout` → new branch. Labels `feat`, `area:api`, `area:docs`, `area:web` exist.
- `gh pr create …` → **https://github.com/Basel-Ghonaim/masaha/pull/97** (= `n`). Its description names "Carried from #95"
  and lists the two new codes' lines for the owner's approval.

## 12.8 CI, CLEAN, conflicts
- `gh pr checks 97` → every check `pass`: lint, format:check, typecheck, test:unit, test:component, check:classes,
  check:links, build, test:api, CodeRabbit.
- `gh pr view 97 --json headRefOid,mergeStateStatus` → `e122b95d39479a3a58bfdebe6ae1a6002acc87ff` (= `git rev-parse
  HEAD`), **`CLEAN`**.
- Early conflict check: `gh pr list --state open` → only #97 itself; nothing to check. (#96 merged before the push; the
  rebase above resolved its two document conflicts.)
- `C:\dev\masaha\workspace\_SHARED\OPEN_DECISIONS.md`: point 1's *Carried to step 7* line → built (#95's unpriced close;
  #97's pricing route and the two reads «يحتاج انتباهك» counts); point 4 left open, its *Settle in* narrowed to step 9.

---

# Final report — DESK PR 3

1. **The pull request:** #97 https://github.com/Basel-Ghonaim/masaha/pull/97 — `feat(jobs): close open stays
   automatically` — head `e122b95d`, CI green on it, `CLEAN`.
2. **The commits:** `a750897f fix(desk): refuse a check-out before its check-in` (49, carried from #95) · `be220604
   feat(spaces): compute the auto check-out time` (45) · `e1c8a2b2 feat(jobs): close open stays automatically` (42) ·
   `47f344a0 feat(visits): price an unpriced visit` (37) · `e122b95d feat(payments): list uncollected visits` (39). Each
   linted and typechecked (`rebase -x`).
3. **Run:** lint, typecheck (each commit and the head); `test:unit` shared 230 / api 783 / web 858; `test:api` 62 files,
   961 tests; `format:check`; `check:links` (2,433); `build -w @masaha/shared` — all exit 0. **Not run locally:**
   `test:component`, the web's `build`, `check:build`, `check:classes` (two catalogue files of strings; CI ran
   test:component, build, check:classes green); `test:api` not re-run after the rebase on #96 (no file it covers changed).
4. **Breaks and red-first:** 22 breaks, 22 red — carried ×2; B1, B2; B3, B4, B6–B13 and B2 (API side); B16–B18;
   B5, B19–B21 (each above, with its lines); every new or changed test seen failing first (each commit's section). B14/B15 (the unpriced close) were PR 2's
   by A1 and are not repeated.
5. **Problems and their solutions:**
   - A first red run of C2 crashed (`createSubscriptionsService()` called without its new dependencies): not counted;
     the dependencies wired, then the real red (404s) seen.
   - A heredoc failed to parse on an apostrophe: the document edits written as script files in `scripts\`.
   - `origin/main` moved (#96) during the work: rebased before the push, two document conflicts kept both sides.
   - A `.env` copy taken before the real run held secrets: deleted at once (the workspace is backed up to GitHub); the
     secret line was removed afterwards by pattern instead.
6. **Unexpected, even if solved:** #96 merged mid-work; the timer's first run closed the demo's long-open visit 1 and
   check-in 4 (correct, but demo data changed); the jobs' endpoint calls also log `job ran`, so the timer's second run
   was told apart by its time (14:39:29).
7. **Early conflict check:** no other open PR.
8. **Departures:** C0 holds items 1–6 (nits 7–10 not taken, reasons in C0); `VISIT_ALREADY_CLOSED` (item 5, Arabic for
   approval); two jobs instead of one `autoCheckOut`; B2's unit break as `gazaClockOf(new Date())`; B10 made as two
   edits; B11 as "the stay limit not read at the run"; C3's subject (the close is #95's); `priceVisitSchema` in
   `visits`, reused by the check-out (`CHARGE_REASON_MAX_LENGTH` moved); the pricing route's `requireCan('attendance.record')`;
   `space-settings.repository.findMany`, `runInTransaction` for `visits`, the `SpacesService` fake's `autoCheckoutDue`;
   the `test:api` lane not re-run after the rebase; `JOBS_SECRET` removed from `.env` after the real run.
- `git status --short` clean; port 3321 free; no process of this worktree running.
