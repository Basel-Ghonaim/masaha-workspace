# DESK PR 2 — `feat/desk-visits` — the executor's report

> Written as the work goes. Worker B, `C:\dev\masaha\app-b`, 2026-10-20.

## Precondition and 12.1 Before the branch

- `gh pr view 94 --json state` → `MERGED`, merge commit `eabdb919`.
- `git fetch origin`; `git status --short --branch` → `## HEAD (no branch)`, clean.
- `git log --oneline -5 origin/main` → `eabdb919 Merge pull request #94 …` over PR 1's four commits.
- `git diff --name-status eff0a3d1 origin/main` → 59 files, exactly `eff0a3d1..e07308b4` (PR 1's merged head, as
  reviewed in `6_REVIEW_PR1_CLAUDE_CODE.md`); no other change since the plan's base.
- Open PRs: **#93** `feat/admin-users` (worker A, head `4daedc94`): its non-web files are documents only
  (findings 49, 88, the findings index, `space-links.md`, `users.md`, `frontend/architecture.md`,
  `foundation.md`, `overview.md`) — no code file of this PR. Shared documents: `overview.md`, the findings index
  (finding 15 moves in C3).
- `git switch --no-track -c feat/desk-visits origin/main` → `Switched to a new branch 'feat/desk-visits'`.
- `docker start masaha-postgres-1` → first `failed to connect to the docker API` (Docker Desktop was not
  running); Docker Desktop started, then `docker start masaha-postgres-1` → `masaha-postgres-1`.
- `npm install` (once, never `npm ci`) → exit 0; `git status --short` empty after it.
- `npm run build -w @masaha/shared` → exit 0.
- `apps/api/.env` (checked by pattern, never printed): `masaha_b_dev`, `masaha_b_test`, `PORT=3321`.
- `npm exec -w @masaha/api -- prisma generate` → `✔ Generated Prisma Client (7.10.0)`;
  `npm run db:migrate` → `Already in sync, no schema change or pending migration was found.` (`masaha_b_dev`).

## The owner's answer — `SPACE_NOT_OPEN`'s line (2026-10-20)

`0_CARRIED_FROM_94.md` item 4: "its catalogue line re-read: if it names only the hours, stop and ask". The line named
only the hours (EN "The status can be set only while the space is open by its hours." / AR "لا تُضبط الحالة إلا
والمساحة مفتوحة حسب ساعات عملها."). Asked; the owner chose **name all three**:
- EN "The status can't be set now: the space is closed, outside its hours, or has no active owner."
- AR "لا يمكن ضبط الحالة الآن: المساحة مغلقة أو خارج ساعات عملها أو بلا مالك فعّال."
Both catalogues change in the second carried commit.

## Carried 1 — `e7011bf8 fix(occupancy): prove the directory's live inputs` (49)

- Item 1: a new test in `directory/liveStatus.api.test.ts` — `a closure in force closes a space and an override in
  force gives its state, on the card, the pin and /occupancy` (a *Closure Room* with a `CLOSURE` in force, an
  *Override Room* with a `FULL` override in force, both otherwise `AVAILABLE`). The code it proves already existed,
  so its red is its two breaks (harness: backup, one exact edit, the file's run, restore checked by SHA-256):
  - **`closureNow: false`** in `liveStatusFor` → `Tests  1 failed | 5 passed (6)` — `AssertionError: expected { 'Override Room': 'FULL', …(7) } to match object { 'Closure Room': 'CLOSED', …(1) }`
  - **`override: null`** in `liveStatusFor` → `Tests  1 failed | 5 passed (6)` — `AssertionError: expected { 'Override Room': 'AVAILABLE', …(7) } to match object { 'Closure Room': 'CLOSED', …(1) }`
  - Green: `Test Files  1 passed (1)`, `Tests  6 passed (6)`.
- Item 2: `docs/plans/v1-mvp.md` — "reception is read-only" → "reception reads, and sets and clears the live
  status's override". Item 3: `docs/backend/security.md` — "its own `can()` action (owner-only, or the staff's for
  the override)". *Last Updated* 2026-10-20 on both.
- My own lint defect (a tuple's `string | undefined` in a template) fixed with `as const` before the commit.
- `npm run lint` → exit 0 · `npm run typecheck` → exit 0.

## Carried 2 — `a9bb4b08 fix(occupancy): refuse an ignored override` (42)

- Item 4 test (`override.api.test.ts`): `refuses an override under a closure in force or on an unverified space: 409
  SPACE_NOT_OPEN, writing nothing` (owner and reception under a closure; reception once the owner's link is ended).
- Item 5 test (`present.api.test.ts`): `answers the override only while the rule uses it: a closure announced after
  it, or no active owner, hides it`.
- **Red first** (both files): `Tests  2 failed | 15 passed (17)` — `AssertionError: expected 200 to be 409` and
  `AssertionError: expected { status: 'CLOSED', capacity: 5, …(3) } to match object { status: 'CLOSED', override: null }`.
- Code: `liveStatus.ts` + `overrideInUse(input)` (verified, no closure, open by its hours, in force), which `liveStatus`
  itself calls (one rule); `occupancy.now` answers `overrideInUse`; `setOverride` refuses `SPACE_NOT_OPEN` when not open,
  under a closure read in the transaction (`announcements.closedAt` gains an optional `tx`), or unverified by the links
  read under the lock (`lockForOverride` answers them).
- **Green:** `Tests  17 passed (17)`; occupancy unit `Tests  12 passed (12)`.
- **Breaks**, each red, restored (SHA-256):
  - closure check removed → `Tests  1 failed | 9 passed (10)` — `AssertionError: expected 200 to be 409`
  - verified check removed → `Tests  1 failed | 9 passed (10)` — `AssertionError: expected 200 to be 409`
  - item 5: the read's override unfiltered (`state.override && until > now`) → `Tests  1 failed | 6 passed (7)` —
    `AssertionError: expected { status: 'CLOSED', capacity: 5, …(3) } to match object { status: 'CLOSED', override: null }`
- Documents: `occupancy.md` (*Behaviour*: the read and the override; *API decisions*: a new line «2026-10-20, #PRNUM.»),
  api-contract (`SpaceOccupancyNow.override`'s comment, the `PUT` refusal, §6's line). Both catalogues: the owner's line.
  The data model's *Live status* 3 ("only while the space is open by its hours") is left as it is: still true, and
  the refusal's cases are an API decision the contract owns.
- `npm run lint` → exit 0 · `npm run typecheck` → exit 0.

## C1 — `a616656e feat(db): record why a charge was typed` (39)

- T1 (`db/front-desk.api.test.ts`): `a typed charge's reason comes with who typed it, and is never blank`; the existing
  `names who typed a charge…` test gains a reason in its two cases (the new CHECK, checked first by name, would
  otherwise answer instead of `visits_charge_set_by_check`). T2 (`db/payments.api.test.ts`, changed): `a visit is paid
  only once its charge is set: payments_visit_uncharged`.
- **Red first** (both files, before the schema): `Tests  3 failed | 33 passed (36)` — the reason column unknown to the
  client; `expected [Function] to throw error matching /payments_visit_uncharged/ but got '…prisma.payment.create()…'`.
- **§12.2 check 1 (the migration, once):** `prisma migrate dev --create-only --name desk_visit_charge` run once →
  `20261020074552_desk_visit_charge`, holding Prisma's `ALTER TABLE "visits" ADD COLUMN "charge_reason" TEXT;`. Appended
  under a raw-SQL header: `visits_charge_reason_check` as the plan writes it; `CREATE OR REPLACE FUNCTION
  "payments_guard_insert"`, copied by script from `20260929120300_payments` — `diff` of the two functions shows only the
  `CREATE OR REPLACE` and the one RAISE (`payments_visit_uncharged`). No data-loss refusal.
  `npm run db:migrate` → `Applying migration 20261020074552_desk_visit_charge` … `in sync` (`masaha_b_dev`);
  `prisma generate` → `Generated`; `models/Visit.ts` names `chargeReason` (58 mentions); `psql … prosrc LIKE
  '%payments_visit_uncharged%'` on `masaha_b_dev` → `t`.
- A slip, undone before the commit: `prisma format` re-aligned two unrelated models (`User`, `SpaceSettings`); the schema
  was restored from `HEAD` and only the two new lines re-added (`git diff --stat` → `2 ++`).
- **Green:** `Tests  36 passed (36)` (the lane's setup applied the migration to `masaha_b_test`).
- **B1** (`ALTER TABLE visits DROP CONSTRAINT visits_charge_reason_check` on `masaha_b_test`) → `Tests  1 failed | 20
  passed (21)` — `AssertionError: promise resolved "{ id: 1, spaceId: 1, …(19) }" instead of rejecting`; restored with the
  migration's `ADD CONSTRAINT` → `Tests  21 passed (21)`.
- **B2** (the payments migration's function `CREATE OR REPLACE`d on `masaha_b_test`) → `Tests  1 failed | 14 passed (15)`
  — `expected [Function] to throw error matching /payments_visit_uncharged/ but got '…'`; restored with the new
  migration's function → `Tests  15 passed (15)`.
- Data model: *Visit* ("who typed it and why"), the later migrations' `CHECK` list (the reason), the ledger bullet
  (`payments_visit_uncharged`); *Last Updated* 2026-10-20.
- `npm run lint` → exit 0 · `npm run typecheck` → exit 0.

## Fixups into carried 2 (folded before the push)
- The English `SPACE_NOT_OPEN` line now uses the catalogue's typographic apostrophe (`can’t`), like every other line.
- `occupancy.md` *API history* gains this PR's line (oldest first, after #94).

## C2 — `b7eb6038 feat(desk): check a visitor in` (30)

- U9 (`packages/shared/src/visits/requests.unit.test.ts`): **red** with a stub `z.any()` → `Tests  1 failed (1)` —
  `AssertionError: expected { visitorName: '  Omar  ' } to deeply equal { visitorName: 'Omar', …(1) }`; **green** `Tests  1 passed (1)`.
- U1–U3 (`visits/visitCharge.unit.test.ts`, `ratesFor`) — **moved into C2** (see departures): **red** with a stub
  answering no rates → `Tests  3 failed` (`expected { hourAgorot: null, dayAgorot: null } to deeply equal { hourAgorot: 500, dayAgorot: 2500 }`); **green** `Tests  3 passed (3)`.
- T3–T12 (`desk/checkIn.api.test.ts`, 10 tests): **red** before the route → `Tests  9 failed | 1 passed (10)`
  (`expected 404 to be 201`, `expected 404 to be 422`, `Error: 2 request(s) never waited on a lock`, …; T4 expects 404
  and passed); **green** → `Test Files  1 passed (1)`, `Tests  10 passed (10)`.
- `SPACE_FULL` by `add-error-code`: `core/errors.ts` (under occupancy), both catalogues (§13 Q2's lines), api-contract §6,
  T10 provokes it.
- §12.2 check 3 (`res.locals` for the key): `idempotencyKeyOf(res)` as `listQueryOf(res)` ✔. Check 5 (`sendSuccess`'s meta
  widened to `PaginationMeta | WarningsMeta`): `npm run typecheck` (shared, api, web) → exit 0 ✔.
- Typecheck needed `pricesOf` in `space-links.service.unit.test.ts`'s `SpacesService` fake (as PR 1's `weekOf`).
- Documents: api-contract (§1's key built; *Capacity*'s line; new *Front desk (managed)* with `DeskVisit`, `VisitCharge`,
  the check-in; §6 `SPACE_FULL`), data model (*Visit charge*: standard prices only; the shift fallback, Q4),
  conventions (header; §13 S1's sentence), `visits.md` and `desk.md` (new), `occupancy.md` (the warnings), map lines,
  v1-mvp (step 7 *Built*, the managed sentence, the surface row reduced to its `GET`).
- `npm run check:links` → `2356 links in 144 documents and 1340 source files all resolve.`; `format:check` exit 0.
- `npm run lint` → exit 0 · `npm run typecheck` → exit 0 (after the commit).

## C3 — `737521de feat(desk): check a visit out and take payment` (46)

- U11 (`shared/auth/can.unit.test.ts`, `prices.typeByHand`, six actors with the switch off and on, and deactivated links):
  **red** → `Failed Tests 8` (`AssertionError: expected undefined to be false`, the action not in the table); **green**
  `Tests  379 passed (379)`.
- U4–U8 (`visits/visitCharge.unit.test.ts`, `chargeOf`): **red** with a stub answering `{ amountAgorot: 0 }` →
  `Failed Tests 5` (`expected { amountAgorot: +0 } to deeply equal { amountAgorot: 1500, …(4) }`, …); **green** `Tests  8 passed (8)`.
- U10 (`packages/shared/src/desk/requests.unit.test.ts`): **red** with a stub `z.any()` → `Tests  1 failed (1)`
  (`expected { …(5) } to deeply equal { …(5) }`); **green** `Tests  1 passed (1)`.
- T13–T27 and, by A1, PR 3's T14–T17 (the unpriced close) in `desk/checkOut.api.test.ts` (19 tests): **red** before the
  route → `Tests  18 failed | 1 passed (19)` (T26 expects 404 and passed); after the code without the translation
  table → `Tests  2 failed | 17 passed (19)`, both `AssertionError: expected 500 to be 409` (T18, A1's T17); **green**
  → `Test Files  1 passed (1)`, `Tests  19 passed (19)`.
- **§12.2 check 2 — the trigger's error as Prisma throws it** (logged once through a temporary line in the error handler,
  then the file restored from its copy; `git diff --stat` empty for it):
  `PrismaClientKnownRequestError`, code **`P2039`**, `meta` = `{"modelName":"Payment","driverAdapterError":{"name":
  "DriverAdapterError","cause":{"originalCode":"23514","originalMessage":"payments_within_due: 1501 agorot would exceed
  the 1500 due (0 paid)","kind":"postgres","code":"23514",…}}}` — and the same with `payments_visit_uncharged: a visit is
  paid once its charge is set`. No constraint field: `checkViolationOf` reads `meta.driverAdapterError.cause` when its
  `originalCode` is `23514`, and takes the message's leading `name:` (a trigger's), else PostgreSQL's
  `violates check constraint "…"`.
- §12.2 check 4: the space's lock, then the visit's row `FOR UPDATE`, then the trigger's own `FOR UPDATE` in one
  transaction — T13 and T21 green, no deadlock, no wait ✔.
- Codes by `add-error-code`: `PRICE_TYPING_NOT_ALLOWED`, `PAYMENT_EXCEEDS_DUE`, and (A1) `VISIT_NOT_PRICED`: `core/errors.ts`,
  both catalogues (§13 Q2's lines; the English with the catalogue's typographic apostrophe), api-contract §6; T24, T18 and
  A1's T17 provoke them.
- Regression run of the neighbouring files: api lane `src/modules/desk src/modules/occupancy src/shared/errors src/db` →
  `Test Files  13 passed (13)`, `Tests  165 passed (165)`; unit lane `src/modules src/shared` → `Tests  689 passed (689)`.
- Documents: api-contract (§1; *Front desk*: the check-out's body, charge, unpaid rest, retry, audit names,
  `VisitPayment`, `VisitCheckOut`, the endpoint; §6's three codes), data model (*Visit charge*: P7's rounding, the
  unpriced close; *Unpaid visit*), conventions (header; §4: the table built), security (header; `requireCan` on the desk's
  writes; `prices.typeByHand`), `payments.md` (new), `visits.md`, `desk.md`, finding 15 Resolved + its resolution line +
  index moved (Open → Resolved, in number order), map line, overview *Front desk*, v1-mvp (step 7 *Built*, *Closes* done,
  the managed sentence, the check-out row removed). `check:links` → `2385 links in 145 documents and 1352 source files
  all resolve.`; `format:check` exit 0.
- `npm run lint` → exit 0 · `npm run typecheck` → exit 0 (after the commit).

## C4 — `aad8063f feat(visits): read a visit's terms and charge` (45) — sha before the autosquash; see the final list

- T28–T30 (`visits/visits.api.test.ts`) and T31 (`occupancy/present.api.test.ts`, which gains a settings row in its setup,
  as every real space has one, and `chargeNowAgorot: null` in T1's exact people): **red** before the code →
  `Tests  4 failed | 7 passed (11)` (`expected 404 to be 200` ×2; `expected { status: 'AVAILABLE', …(4) } to deeply equal …`
  (T1's new field); `expected [ Array(3) ] to deeply equal [ Array(3) ]` (T31)); T30 expects 404 and passed.
- **Green** → with occupancy, desk and directory: `Test Files  11 passed (11)`, `Tests  116 passed (116)`.
- `spaces.shiftsOf` added for the terms' rates per shift (the plan's table names no shift read); the `SpacesService`
  fake in `space-links.service.unit.test.ts` gains it.
- Documents: api-contract (`PresentPerson.chargeNowAgorot`; `VisitQuote`, `QuotedVisit`, `Rates`, `VisitTerms`; the two
  `GET`s), `occupancy.md` (the charge so far), `visits.md` (the reads), v1-mvp (*Built*). `check:links` → `2387 links in
  145 documents and 1355 source files all resolve.`; `format:check` exit 0.
- Observed, not recorded: `occupancy.md` was already over documentation §5's ~1,200 words on `origin/main` (1,478); this PR
  brings it to 1,700. Left for the owner (no finding recorded: the plan's §6 plans none; it is the document's size, not
  a divergence in the code).
- `npm run lint` → exit 0 · `npm run typecheck` → exit 0 (after the commit).

## After the autosquash — the head `36fa5d29`
- The two fixups folded into the carried commit 2 (`GIT_SEQUENCE_EDITOR=:` autosquash) → `Successfully rebased`.
- `git rebase -x "npm run lint && npm run typecheck"` from the base → `CHECK-OK` on each of the 6 commits, `Successfully rebased`.
- Commits now: `e7011bf8 fix(occupancy): prove the directory's live inputs` (49) · `0bd902d1 fix(occupancy): refuse an
  ignored override` (42) · `5e5103aa feat(db): record why a charge was typed` (39) · `97211655 feat(desk): check a visitor
  in` (30) · `5fce9750 feat(desk): check a visit out and take payment` (46) · `36fa5d29 feat(visits): read a visit's terms
  and charge` (45).

## 12.4 Verification on the head — STOPPED
- No `vitest` under `C:\dev\masaha\app\` before the lanes.
- `npm run test:unit` → exit 0: shared `Tests  229 passed (229)`, api `Tests  772 passed (772)`, web `Tests  833 passed (833)`.
- `npm run test:api` (run in the background) → **killed by Claude Code because the system was critically low on memory**
  (its notice: "stopped because the system is running low on memory … Do not start it again on your own"). The log
  holds only the global setup's `No pending migrations to apply.`: no test result. Two leftover `vitest` processes of
  this worktree (23532, 30648) were stopped by process id; none remains.
- **STOPPED here**, by the exec prompt §3 ("If memory runs low and a command is killed, stop and report — do not narrow
  it") and §2 (a lane that cannot run). Not yet done: `test:api` on the head, `format:check`/`check:links`/`build -w
  @masaha/shared` on the head (both passed after C4 before the autosquash, which changed only the folded fixups), the
  breaks of 12.5 (B3–B39 and A1's three; B1, B2 and the five carried breaks are done and red), the real run (12.6; its
  script is ready in the scratchpad, `realrun.mjs`), `#PRNUM`, the push and the PR.
- Worktree: branch `feat/desk-visits`, local only, not pushed; `git status --short` empty; port 3321 not used.
- The breaks' spec is ready: scratchpad `breaks.txt` (41 blocks) run by `brks.py` (backup, one edit, the file's run,
  restore checked by SHA-256).

## Departures so far
- **Carried item 4's catalogue line:** asked the owner (the line named only the hours); answer "name all three".
- `ratesFor` and U1–U3 built in C2 (the check-in first uses them), not C3; `chargeOf` and U4–U8 in C3 as planned.
- `ratesFor` takes `{ audience, shiftId }` only, not `studentPrices`: a student visit where the switch is off is refused
  before (T5), so the parameter would be read by nothing.
- `visits` audits its own entries (`visit.checkedIn`, `visit.checkedOut`): its deps gain `audit` (the plan's list had
  none for visits or desk). `customers`' service now takes `{ audit }`.
- `announcements.closedAt` gains an optional `tx` (carried item 4 reads the closure in the override's transaction).
- `liveStatus.ts` gains `overrideInUse` (item 5's one rule, which `liveStatus` itself calls).
- `spaces.shiftsOf` (C4, the terms' shifts) — not in the plan's table; the `SpacesService` fake gains `pricesOf`, `shiftsOf`.
- `present.api.test.ts` gains a settings row in its setup (the charge so far reads the settings, as every real space has
  them) and `chargeNowAgorot` in T1's exact shape.
- By A1, PR 3's T14–T17 (`VISIT_NOT_PRICED` and the unpriced close) are in C3; PR 2's T24 tests a typed price only.
- B25 (planned "the rounding read at check-in") cannot exist as written — no rounding is stored at check-in; its spec
  instead fixes the rounding and cap regardless of the settings at check-out. B31's spec makes both of the plan's edits
  (no `FOR UPDATE`, no space lock) in one break.
- The data model's *Live status* 3 left unchanged by carried item 4 (still true; the refusal's cases are the contract's).

# RESUMED — `3c_RESUME_PR2.md` (2026-10-20)

- Memory first: no `node.exe` running at all (worker A's included); `FreePhysicalMemory` = 5,254,628 KB.
- **Rebased on `origin/main` `7d48c9c3` (after #93):** `git rebase origin/main` → `Successfully rebased`, **no conflicts**.
  `npm run build -w @masaha/shared` → exit 0; `npm run lint` → exit 0; `npm run typecheck` → exit 0 (shared, api, web).
- **Finding 98** recorded (the number reserved): `docs/architecture/findings/98-the-capability-documents-outgrow-their-size-guide.md`
  and its index line under *Open*, after 97 — the guide (documentation §5), the sizes on `main` at `7d48c9c3` by `wc -w`
  (spaces 11,026; space-links 8,962; users 3,594; lookups 2,870; directory 1,728; auth 1,627; occupancy 1,478 → 1,700 by
  this PR), why it matters, the choice left to the owner. `occupancy.md` not trimmed. Folded (`--fixup` + autosquash) into
  the commit that grows `occupancy.md` most — the carried `fix(occupancy): refuse an ignored override` (+126 words; C2
  +67, C4 +29). `check:links` → `2400 links in 146 documents and 1392 source files all resolve.`
- Commits now: `ef3993b5` (carried 1) · `0dfb178a` (carried 2, with finding 98) · `bd35a6a2` C1 · `8ffd6e38` C2 · `3b89a83a`
  C3 · `a7561f47` C4.

## 12.4 Verification on the rebased head `a7561f47`, one lane at a time
- `npm run lint` → exit 0 · `npm run typecheck` → exit 0.
- Before `test:unit`: no `node.exe` at all; free 5,356,724 KB. `npm run test:unit` → exit 0: shared `Tests  229 passed (229)`,
  api `Tests  772 passed (772)`, web `Tests  842 passed (842)`.
- Before `test:api`: worker A's focused `vitest` runs (`C:\dev\masaha\app\`, component lane) came and went; waited (never
  stopped them) until no `vitest`/`tsx`/`tsc` for three checks 5 s apart; free 5,116,856 KB. `npm run test:api` → exit 0:
  `Test Files  58 passed (58)`, `Tests  936 passed (936)`.
- `npm run format:check` → `All matched files use Prettier code style!` · `npm run check:links` → `2400 links in 146
  documents and 1392 source files all resolve.` · `npm run build -w @masaha/shared` → exit 0.
- `git grep -n "#PRNUM"` → documents only (11 files). `git diff --stat origin/main -- apps/web` → only the two `errors.ts`
  catalogues. `git diff --stat origin/main -- package.json package-lock.json` → empty.
- Not run, with why: `test:component`, the web's `build`, `check:build`, `check:classes` — the web change is two catalogue
  files of strings, whose parity the typecheck enforces; CI runs them.

## 12.5 The breaks owed — each red, each restored from its backup (SHA-256 checked), on the head `a7561f47`
Harness: scratchpad `brks.py` + `breaks.txt` (backup to `%TEMP%\desk-breaks\`, one exact edit, the named file in its
lane, restore, hash). B11–B13's first attempt ran `--project unit` in `packages/shared`, which has no such project
(`Error: No projects matched the filter "unit".`) — my harness's defect, not counted; rerun without `--project`.
- **B3** student fallback by the pair (`visitCharge.ts`) — `Tests  1 failed | 7 passed (8)` — `expected { hourAgorot: 400, dayAgorot: null } to deeply equal { hourAgorot: 400, dayAgorot: 2500 }`
- **B4** no shift fallback — `Tests  1 failed | 7 passed (8)` — `expected { hourAgorot: 300, dayAgorot: null } to deeply equal { hourAgorot: 300, dayAgorot: 2500 }`
- **B5** `>=` — `Tests  1 failed | 7 passed (8)` — `expected 1000 to be 500`
- **B6** no minimum — `Tests  1 failed | 7 passed (8)` — `expected { amountAgorot: +0, …(4) } to match object { amountAgorot: 500, billedMinutes: 1 }`
- **B7** `Math.floor` (half hours) — `Tests  1 failed | 7 passed (8)` — `expected { amountAgorot: 250, …(4) } to deeply equal { amountAgorot: 500, …(4) }`
- **B8** `Math.floor` (per minute) — `Tests  1 failed | 7 passed (8)` — `expected 25 to be 26`
- **B9** cap ignored — `Tests  1 failed | 7 passed (8)` — `expected { amountAgorot: 4000, …(4) } to match object { Object (amountAgorot, capApplied) }`
- **B10** `0` instead of `null` — `Tests  1 failed | 7 passed (8)` — `expected { amountAgorot: +0, …(4) } to be null`
- **B11** `max(60)` removed (shared) — `Tests  1 failed (1)` — `expected null to deeply equal { visitorName: [ 'too_long' ] }`
- **B12** `min(1)` removed (shared payments) — `Tests  1 failed (1)` — `expected null to deeply equal { Object (payment.amountAgorot) }`
- **B13** `reason` optional (shared desk) — `Tests  1 failed (1)` — `expected null to deeply equal { 'charge.reason': [ 'required' ] }`
- **B14** `prices.typeByHand` as staff (`can.ts`) — `Tests  1 failed | 378 passed (379)` — `expected true to be false`
- **B15** rates from the request — `Tests  3 failed | 7 passed (10)` — `expected { id: 1, visitorName: 'Omar', …(9) } to deeply equal …`
- **B16** student setting not read — `Tests  1 failed | 9 passed (10)` — `expected 201 to be 422`
- **B17** retry pre-check removed — `Tests  2 failed | 8 passed (10)` — `expected 500 to be 201`; `expected [ 500, 201 ] to deeply equal [ 201, 201 ]`
- **B18** space lock removed (check-in) — `Tests  2 failed | 8 passed (10)` — `Error: 2 request(s) never waited on a lock`
- **B19** key middleware after `validate` — `Tests  1 failed | 9 passed (10)` — `expected { visitorName: [ 'required' ] } to deeply equal { idempotencyKey: [ 'required' ] }`
- **B20** `isFull` with `>` — `Tests  1 failed | 9 passed (10)` — `expected { success: true, …(1) } to match object { Object (meta) }`
- **B21** check-in `can()` on `space.links` — `Tests  1 failed | 9 passed (10)` — `expected 201 to be 403`
- **B22** `checkedInAt` from the column default — `Tests  2 failed | 8 passed (10)` — `… to match object { Object (checkedInAt) }`
- **B23** charged to the database's `now()` — `Tests  7 failed | 12 passed (19)` — `expected 422 to be 200` (the charge, to the real now, exceeds the payment: a phone asked)
- **B24** rates re-read at check-out — `Tests  1 failed | 18 passed (19)` — `expected 422 to be 200` (charge 2,100 > the 1,167 paid)
- **B25** rounding and cap fixed (not the settings at check-out; the plan's "read at check-in" has no code form) — `Tests  1 failed | 18 passed (19)` — `expected 422 to be 200`
- **B26** phone check removed — `Tests  2 failed | 17 passed (19)` — `expected 200 to be 422` (×2, A1's T15 included)
- **B27** a customer always created — `Tests  1 failed | 18 passed (19)` — `expected 500 to be 200`
- **B28** `payments_within_due` line removed — `Tests  1 failed | 18 passed (19)` — `expected 500 to be 409`
- **B29** payment key not looked up — `Tests  1 failed | 18 passed (19)` — `expected { visit: { id: 1, …(10) }, …(1) } to deeply equal …`
- **B30** closed check removed — `Tests  3 failed | 16 passed (19)` — `expected 500 to be 200`; `expected 409 to be 200`
- **B31** no `FOR UPDATE` and no space lock (two files, one break) — `Tests  2 failed | 17 passed (19)` — `Error: 2 request(s) never waited on a lock`
- **B32** quote bound removed — `Tests  1 failed | 18 passed (19)` — `expected 200 to be 422`
- **B33** `chargeSetById` not written — `Tests  2 failed | 17 passed (19)` — `expected 500 to be 200` (the reason's `CHECK` refuses it)
- **B34** typed price as staff — `Tests  4 failed | 15 passed (19)` — `expected 200 to be 403`; `expected 422 to be 200`
- **B35** rate check removed — `Tests  1 failed | 18 passed (19)` — `expected 200 to be 422`
- **B36** `lockIn` without `spaceId` — `Tests  1 failed | 18 passed (19)` — `expected 422 to be 404`
- **B37** check-out `can()` on `space.links` — `Tests  1 failed | 18 passed (19)` — `expected 200 to be 403`
- **A1a** unpriced close charged 0 — `Tests  3 failed | 16 passed (19)` — `expected { visit: { id: 1, …(10) }, …(1) } to match object { visit: { …(4) }, payment: null }`
- **A1b** whoever may type not made to — `Tests  1 failed | 18 passed (19)` — `expected 200 to be 422`
- **A1c** `payments_visit_uncharged` line removed — `Tests  1 failed | 18 passed (19)` — `expected 500 to be 409`
- **B38** student rates always answered — `Tests  1 failed | 2 passed (3)` — `expected { rounding: { …(2) }, …(3) } to deeply equal …`
- **B39** charge so far at the check-in time — `Tests  1 failed | 7 passed (8)` — `expected [ Array(3) ] to deeply equal [ Array(3) ]`
- `git status --short` empty afterwards.

## 12.6 The real run — API on 3321, `masaha_b_dev` (2026-10-20, ≈ 12:38 in Gaza)
`npm run dev -w @masaha/api` in the background; `curl -s http://localhost:3321/health` → `{"status":"ok","db":"up",…}`;
`prisma migrate status` → `Database schema is up to date!`. Signed in as `demo-owner@example.com` (id 2) and
`demo-reception@example.com` (id 3), `SEED_DEMO_PASSWORD` read from `.env` into the script, never printed. Space 1
(`masaha-demo`): it already has a standard hour (5 ₪) and day (25 ₪) price; its settings round `PER_MINUTE`, and its
reception switch is **on**.

**First pass** (`realrun.mjs`), with two assumptions of my script that the demo's data proved wrong:
- `GET …/visit-terms` (owner) → 200: `PER_MINUTE`, cap on, `mayTypePrice: true`, rates for no shift and shifts 1 and 2 (5/25 ₪, student 4/20 ₪).
- `POST …/visits` (fresh key) → 201, visit 6, rates 500/2,500, no `meta` (the demo's capacity not reached); the same request again → 201, the same id 6.
- `GET …/visits/6` → 200, quote `{ at, chargeAgorot: 8, billedMinutes: 1, capApplied: false }` (one minute, per minute).
- The check-out "part paid" sent `charge − 100` = −92 → 422 `payment.amountAgorot: out_of_range` (my script's defect: it
  assumed a charge above 1 ₪); the next two calls followed from it (422).
- The prices removed (`PUT …/prices []` → 200); visit 7: reception's typed price → **200** (the demo's switch is on, so
  reception may type: correct behaviour, not the case the plan wanted); the owner's then → 200, the visit already closed,
  answered as it is. Visit 8 (reception, untyped) → 422 `required` on `charge` (reception may type there, so it must:
  correct). The prices put back → 200.

**Second pass** (`realrun2.mjs`): the switch turned off for the run (`PATCH …/settings { receptionMayTypePrices: false }`
→ 200), then put back.
- `GET …/visits/6` → quote `chargeAgorot: 8`. **Check-out, part paid (7), no phone → 422 `{ phone: ['required'] }`.**
- **With `phone: "0599000123"` → 200**: charge 8 (`PER_MINUTE`, cap not applied), customer `{ id: 6, name: "Real run",
  phone: "+970599000123" }` created, payment 7 `CASH` by reception. **The same check-out again (same key) → 200, the
  same body (`same body: true`).**
- The prices removed; visit 9: **reception's typed price → 403 `PRICE_TYPING_NOT_ALLOWED`**; **the owner's → 200**,
  charge 1,000 typed by 2 with its reason, payment 1,000.
- Visit 8 (no rate), **reception, untyped, with the phone → 200, closed unpriced** (`charge: null`), left to customer 6
  (found by the phone).
- The demo's prices put back → 200; the switch put back → 200 `true`.
- `GET …/occupancy` (reception) → 200: the demo's own visit 1 with `chargeNowAgorot: 2500` (open since 2026-10-04,
  capped at the day price) and its check-in 4; the real run's visits all closed.
- `SELECT action FROM audit_logs ORDER BY id DESC LIMIT 14` → `space.settingsEdited, space.pricesEdited,
  visit.checkedOut, payment.recorded, visit.checkedOut, visit.checkedIn, space.pricesEdited, payment.recorded,
  visit.checkedOut, customer.created, space.settingsEdited, space.pricesEdited, visit.checkedIn, payment.recorded`.
- Left in `masaha_b_dev` by the run (demo data): visits 6–9 closed, customer 6 (+970599000123), payments 7, 1,000 and
  1,000 (visit 7's by reception in the first pass, visit 9's by the owner).
- Stopped by process id (tsx watch 12648, the server 25080, pino-pretty 11204); `Get-NetTCPConnection -LocalPort 3321` →
  nothing: port 3321 free. (The background task then reports exit 127, as in PR 1.)

## 12.7 The PR number, push and PR
- Next number from GitHub: **95** (the latest, #94). Before the push, plan §14's size point: **78 files** (over "about
  70") — asked the owner; answer: **push as one PR** (the excess is the carried commits and finding 98).
- `git filter-branch` replaced `#PRNUM` → `#95` in each commit's documents (11 files, 38 lines; `git diff` against the
  pre-filter head shows only those lines); `git grep -n '#PRNUM'` → nothing; `check:links` and `format:check` again → pass.
- Commits: `ef3993b5 fix(occupancy): prove the directory's live inputs` (49) · `ec37ae95 fix(occupancy): refuse an
  ignored override` (42) · `7b868292 feat(db): record why a charge was typed` (39) · `4ff745ab feat(desk): check a
  visitor in` (30) · `80de13a4 feat(desk): check a visit out and take payment` (46) · `b225d1fa feat(visits): read a
  visit's terms and charge` (45).
- `git push -u origin feat/desk-visits` → new branch. Labels `feat`, `area:api`, `area:docs`, `area:web` exist.
- `gh pr create …` → **https://github.com/Basel-Ghonaim/masaha/pull/95** — the number equals `n`. Its description names
  "Carried from #94" with both carried commits, and the new codes' lines for the owner's approval.

## 12.8 CI, CLEAN, conflicts
- `gh pr checks 95 --watch` — the first watch dropped on a network error (`wsarecv: An existing connection was forcibly
  closed by the remote host`) with test:api and test:component pending; re-watched → every check `pass`: lint,
  format:check, typecheck, test:unit, test:component (5m28s), check:classes, check:links, build, test:api (4m26s);
  CodeRabbit skipped (manual review).
- `gh pr view 95 --json headRefOid,mergeStateStatus,statusCheckRollup` → head `b225d1fa8fc3f6baa23985c1ebfea6c262639ef9`
  (= `git rev-parse HEAD`; the run's head SHA the same, `success`), **`CLEAN`**, `SUCCESS` ×10.
- Early conflict check: the only open PR is #95 itself (#93 merged before the rebase) → nothing to check.

---

# Final report — DESK PR 2

1. **The pull request:** #95 https://github.com/Basel-Ghonaim/masaha/pull/95 — `feat(desk): check a visit out and take
   payment` — head `b225d1fa`, CI green on it, `CLEAN`.
2. **The commits:** `ef3993b5 fix(occupancy): prove the directory's live inputs` (49) · `ec37ae95 fix(occupancy): refuse
   an ignored override` (42, with finding 98) · `7b868292 feat(db): record why a charge was typed` (39) · `4ff745ab
   feat(desk): check a visitor in` (30) · `80de13a4 feat(desk): check a visit out and take payment` (46) · `b225d1fa
   feat(visits): read a visit's terms and charge` (45). Each linted and typechecked (`rebase -x`).
3. **Run:** lint, typecheck (each commit and the head); `test:unit` shared 229 / api 772 / web 842; `test:api` 58 files,
   936 tests; `format:check`; `check:links` (2,400); `build -w @masaha/shared` — all exit 0, on the rebased head.
   **Not run locally:** `test:component`, the web's `build`, `check:build`, `check:classes` (two catalogue files of
   strings; CI ran test:component, build and check:classes green). The first `test:api` (before the resume) was killed
   for low memory and is not counted.
4. **Breaks and red-first:** 48 breaks, 48 red — the five carried, B1–B2 (database), B3–B39 and A1's three (12.5, each with
   its lines); every new test file seen failing first (each commit's section).
5. **Problems and their solutions:**
   - `SPACE_NOT_OPEN`'s line named only the hours: asked; the owner chose "name all three".
   - The first `test:api` killed for low memory: stopped and reported; resumed by `3c_RESUME_PR2.md` with the memory check
     before each lane and worker A's runs waited out.
   - `prisma format` re-aligned unrelated models: the schema restored from `HEAD`, only the two lines re-added.
   - Prisma reports the trigger's violation as `P2039` with no constraint field: `checkViolationOf` reads the database's
     message (12.2 check 2).
   - A heredoc failed to parse on an apostrophe, and escapes turned into literal newlines: scripts written with the Write
     tool instead.
   - B11–B13 first ran with a project the shared package lacks: rerun without it.
   - The real run's first pass assumed a charge above 1 ₪ and the reception switch off; the demo rounds per minute and has
     it on: a second pass turned the switch off for the run, paid `charge − 1`, and put both back.
   - The plan's §14 size point (78 files): asked; the owner chose one PR.
6. **Unexpected, even if solved:** worker A's focused vitest runs kept starting while I waited for a quiet machine; the
   demo space had its reception switch on and per-minute rounding; the first CI watch dropped on a network error.
7. **Early conflict check:** no other open PR.
8. **Departures** (each with its reason, above in *Departures so far*): the `SPACE_NOT_OPEN` line (the owner's answer);
   `ratesFor` and U1–U3 in C2; `ratesFor` without `studentPrices`; `visits` and `customers` audit their own entries;
   `announcements.closedAt(…, tx)`; `overrideInUse`; `spaces.shiftsOf`; `present.api.test.ts`'s settings row; A1's tests in
   C3; B25 reworded and B31 made as one break; the data model's *Live status* 3 unchanged; finding 98 folded into the
   carried commit 2 (by `3c_RESUME_PR2.md`); 78 files in one PR (the owner's answer); the real run in two passes, the
   demo's switch turned off for the run and put back, the run's visits, customer 6 and three payments left in
   `masaha_b_dev`.
- `git status --short` clean; port 3321 free; no process of this worktree running.
