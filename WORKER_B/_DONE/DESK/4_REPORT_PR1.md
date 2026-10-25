# DESK PR 1 — `feat/live-status` — the executor's report

> Written as the work goes. Worker B, `C:\dev\masaha\app-b`, 2026-10-19.

## 12.1 Before the branch

- `git fetch origin`; `git status --short --branch` → `## HEAD (no branch)`, clean.
- `git log --oneline -5 origin/main` → head `eff0a3d1 Merge pull request #92 …` (the plan's base).
- `gh pr list --state open` → no open PR.
- `git diff --name-status eff0a3d1 origin/main` → empty: nothing changed since the plan's base.
- `git switch --no-track -c feat/live-status origin/main` → `Switched to a new branch 'feat/live-status'`.
- `docker start masaha-postgres-1` → `masaha-postgres-1`. `npm run build -w @masaha/shared` → exit 0.
- `apps/api/.env` (checked by pattern, never printed): names `masaha_b_dev` and `masaha_b_test`; `PORT=3321`.

## 12.2 First checks (PR 1)

1. **The dependency** — `npm install -w @masaha/api -w @masaha/shared @date-fns/tz@^1.5.0` → exit 0.
   `git diff --stat` → `apps/api/package.json | 1 +`, `package-lock.json | 2 ++`, `packages/shared/package.json | 1 +`.
   The lockfile diff is only the two workspaces' `"@date-fns/tz": "^1.5.0"` lines; `node_modules/@date-fns/tz`
   stays at `1.5.0` (no entry added or changed). ✔ (the `TZDate` typecheck: see C1).
2. **A Gaza daylight-saving transition** — Node's zone data:
   ```
   2025-01-01T00:00:00.000Z GMT+02:00
   2025-04-12T00:00:00.000Z GMT+03:00
   2025-10-24T23:00:00.000Z GMT+02:00
   2026-01-01T00:00:00.000Z GMT+02:00
   2026-03-28T00:00:00.000Z GMT+03:00
   2026-10-23T23:00:00.000Z GMT+02:00
   ```
   Pinned in U2: 2026-03-28 (02:00 local +02 → 03:00 +03) and 2026-10-24 (02:00 +03 → 01:00 +02).

## C1 `feat(core): read the time in Gaza` (33) — NOT COMMITTED: STOPPED

- U1–U3 written by hand in `packages/shared/src/core/gazaTime.unit.test.ts` (the transitions above).
- **Red first:** with a stub that throws, `npx vitest run src/core/gazaTime.unit.test.ts` (shared, unit) →
  `Tests  3 failed (3)` (`Error: not built yet` in each).
- **Green:** `gazaTime.ts` through `TZDate`, exported from `core/index.ts` → `Tests  3 passed (3)`.
- `npm run typecheck` → exit 0 (shared, api, web): `import { TZDate } from '@date-fns/tz'` typechecks.
- Conventions header and §11 edited (Gaza time built; `@date-fns/tz` alone; `core/gazaTime.ts`).
- **`npm run lint` → exit 1:**
  ```
  packages/shared/src/core/gazaTime.ts
     1:24  error  core → @date-fns/tz is not allowed. Core imports nothing but zod (docs/architecture/shared-package.md, R3)  boundaries/dependencies
    25:14  error  Invalid type "number" of template literal expression  @typescript-eslint/restrict-template-expressions
  ```
  The second is my own code's defect, fixed (`String(…)`); `npx eslint packages/shared/src/core/gazaTime.ts`
  now reports only the first.

## STOPPED — the plan proves false against the code

**What:** the plan (§4 PR 1 table, §2 Scope 1, §12.2 check 1) puts `gazaTime.ts` in
`packages/shared/src/core/` importing `TZDate` from `@date-fns/tz`. `docs/architecture/shared-package.md`
**R3** — "`core` imports nothing but zod … Lint enforces it" — and its lint policy in `eslint.config.js`
(`sharedDependencies`, "Core imports no package but zod: no Node module either, since the web runs it too")
refuse it. The plan's §12.2 check 3 looked at the API's level rule only; this is the shared package's rule.
§14 ("the level rule refuses an import this plan names") and the exec prompt ("a plan that proves false
against the code") say stop and ask. Conventions §11 (the dependency "of `packages/shared`", the calendar
rules "pure functions in `packages/shared`") and shared-package R3 disagree; the plan followed §11.

**The fixes, the owner's to choose (none taken):**
1. **Admit `@date-fns/tz` in core** *(recommended — smallest, and what conventions §11 already intends)*:
   R3 becomes "`core` imports nothing but zod and `@date-fns/tz` (Gaza time, conventions §11)"; one allow
   line beside zod's in `eslint.config.js`'s core policy; `shared-package.md`'s *Last Updated*. +2 files in C1,
   no other change to the plan. An architecture rule's change: the owner's approval, stated in C1's body.
2. **A2 for core only:** `gazaTime.ts` through `Intl` (≈ 20 lines of offset arithmetic), no dependency;
   §13 Q1 reversed, conventions §11's library line changes instead.
3. **Gaza time in the API** (`apps/api/src/shared/time/`): no rule change, but against conventions §11's
   "the calendar rules are shared … so the web and the API agree" — not recommended.

**Where the work stands:** branch `feat/live-status` (local, not pushed, no commit), cut from
`origin/main` `eff0a3d1`. Uncommitted in the worktree, kept for the resumption: the dependency
(`apps/api/package.json`, `packages/shared/package.json`, `package-lock.json`), `core/gazaTime.ts`,
`core/gazaTime.unit.test.ts`, `core/index.ts`, `docs/backend/conventions.md`. `git status --short` is
therefore not clean (by the stop, deliberately: nothing to discard before the owner decides). No API was
started; port 3321 free; no full lane run; no break made yet (they belong after the commits).

## RESUMED — the owner's answer (2026-10-19): option 1

"Allow `@date-fns/tz` in shared core": R3 in `docs/architecture/shared-package.md` amended ("`core` imports
nothing but zod and `@date-fns/tz`, Gaza's calendar"), a dated *Revised* line ending `#PRNUM`, *Last
Updated* 2026-10-19; `eslint.config.js`'s core policy allows `@date-fns/tz` beside zod — that one package
only (probe: a temporary `core/zzProbe.ts` importing `date-fns` → `core → date-fns is not allowed. Core
imports nothing but zod and @date-fns/tz …`; file removed).
- `npm run lint` → exit 0. `npm run typecheck` → exit 0.

### C1 committed — `f967c822 feat(core): read the time in Gaza` (33)
- Red: `Tests  3 failed (3)` (stub). Green: `Tests  3 passed (3)`.
- Files: the dependency (3), `core/gazaTime.ts` (+ test), `core/index.ts`, conventions header + §11,
  `shared-package.md` R3, `eslint.config.js`.

### C2 committed — `a9f60c7b feat(occupancy): derive the live status` (39)
- U4–U12 (`liveStatus.unit.test.ts`, 10 tests). **Red** (stub answering `'AVAILABLE'`):
  `Tests  7 failed | 3 passed (10)` (e.g. `AssertionError: expected 'AVAILABLE' to be null`). **Green:** `Tests  10 passed (10)`.
- T1–T6 (`present.api.test.ts`, api lane). **Red:** the read's code was written before this API test, so its red was
  seen with the route removed (backup → `sed` delete of `router.get('/occupancy', …)` → run → restored from the backup):
  `Tests  5 failed | 1 passed (6)` (`expected 404 to be 200`; T2 expects 404 and passed). **Green:** `Tests  6 passed (6)`.
- §12.2 check 3 (C2 part): `npm run lint` → exit 0 with `occupancy` importing `visits`, `subscriptions`, `customers`,
  `announcements` and `spaces` ✔. `npm run typecheck` → exit 0.
- Documents: api-contract (§4's exception; *Occupancy (managed)* with the read; *Capacity*'s line), `occupancy.md`,
  conventions header, the map line, overview, v1-mvp (step 7 *Built*, the managed sentence, the `…/occupancy` row removed).
- Departures: `space-links.service.unit.test.ts` gains `weekOf` in its `SpacesService` fake (the type requires it; not in
  §7's list). `visits.openCountsIn`, `subscriptions.openCheckInCountsIn`, `spaces.weeksFor`, `occupancy.statesFor`,
  `liveStatusFor`, `availableAmong` are built in C4, where the directory first uses them, not C2 (no code nothing uses).
  The data model is not edited in C2 (Appendix A gives it no C2 line).

### C3 committed — `4bce0d7f feat(occupancy): override the live status` (41)
- U13 (`overrideUntil.unit.test.ts`): **red** (stub answering `now`) `Tests  2 failed (2)` (`expected 2026-10-18T07:00:00.000Z to deeply equal 2026-10-18T07:30:00.000Z`); **green** `Tests  2 passed (2)`.
- U14 (shared `occupancy/requests.unit.test.ts`): **red** with `state: z.string()` (B8's form) `Tests  1 failed | 1 passed (2)` (`expected null to deeply equal { state: [ 'invalid_choice' ] }`); **green** `Tests  2 passed (2)`.
  My first expectation for an absent field was `required`; the project's rule (`toFieldErrors`, as the packages' and prices' tests say) answers an absent choice `invalid_choice` — my test's defect, corrected.
- T7–T15 (`override.api.test.ts`): **red** before the routes `Tests  8 failed | 1 passed (9)` (`expected 404 to be 200`, … T15 `1 request(s) never waited on a lock`; T12 expects 404 and passed); **green** `Tests  9 passed (9)`.
- T16 (`occupancy.api.test.ts`, through the routes: override, then capacity, then the read): written after the override code, `Tests  10 passed (10)`; its red is B24 (12.5).
- `SPACE_NOT_OPEN` by `add-error-code`: `core/errors.ts`, both catalogues (§13 Q2's lines), api-contract §6, T10 provokes it. Shared `errors.unit.test.ts` → `Tests  13 passed (13)`.
- `npm run lint` → exit 0; `npm run typecheck` → exit 0; Prettier clean.
- Documents: contract (*Occupancy (managed)*'s override, `PUT`/`DELETE`), security (header + *Authorization*), data model *Live status* 3, `occupancy.md`, map line, overview, v1-mvp (the `status-override` row removed into *Built*).

### C4 committed — `69b334d9 feat(directory): show the live status` (37)
- U15 (shared `directory/requests.unit.test.ts`): **red** `Tests  1 failed | 31 passed (32)` (`expected { Object (page, limit, ...) } to match object { availableNow: true }`); **green** `Tests  32 passed (32)`.
  `availableNow` parses as `openFriday` does (`z.stringbool()`): `true`/`false`, anything else `invalid_choice`; `false` filters nothing.
- T17–T21 (`directory/liveStatus.api.test.ts`): **red** before the code `Tests  5 failed (5)` (e.g. `expected { 'Second Open': undefined, …(5) } to deeply equal { 'Open Room': 'AVAILABLE', …(5) }`; `/occupancy` `expected 404 to be 200`); **green** with the whole directory folder `Tests  55 passed` after the two shape updates below.
- §12.2 check 3 (C4 part): lint exit 0 with `directory` importing `occupancy` and `@masaha/shared/occupancy` ✔. Check 4: `onlyIds` applied in `listed()`'s raw SQL exactly as `verifiedIds` (`s.id = ANY(…::int[])` among the conditions, before the order and the page) ✔; `publicListing.service.ts` needed no change (`PublicListingFilter` is `PublicFilter` without the cut-off). Check 5: `groupBy` with `_count: { _all: true }` compiles, one query each; T17/T19 prove the counts (a closed visit in *Open Room*) ✔.
- `npm run lint` → exit 0; `npm run typecheck` → exit 0.
- Documents: contract *Directory (public)* (the intro line, `availableNow`, `liveStatus` on both shapes, `PublicOccupancy`, `GET /spaces/:slug/occupancy`), `directory.md`, `occupancy.md` (the directory's read), v1-mvp (*Built*, the ordering note, the surface's two rows into the *Built* sentence), overview.
- Departures: `list.api.test.ts` and `pins.api.test.ts` (not in §7) gain `liveStatus: null` in their exact-shape expectations; the list test's title drops "or live status". `space-links.service.unit.test.ts`'s fake gains `weeksFor`. `GET /spaces/:slug/occupancy` answers any listed space (`{ status: null }` for an unverified one), as §4's C4 line says ("not listed → 404, as `page`"); v1-mvp's old surface row said "verified spaces only" — the row is removed.

## 12.4 Verification on the head (`69b334d9`), one at a time
- `npm run lint` → exit 0 · `npm run typecheck` → exit 0 (after C4, the head).
- `npm run test:unit` → exit 0: shared `Tests  227 passed (227)`, api `Tests  757 passed (757)`, web `Tests  833 passed (833)`.
- `npm run test:api` → exit 0: `Test Files  55 passed (55)`, `Tests  899 passed (899)` (no vitest under `C:\dev\masaha\app\` before it).
- `npm run format:check` → exit 0, `All matched files use Prettier code style!`
- `npm run check:links` → exit 0, `2316 links in 142 documents and 1323 source files all resolve.`
- `npm run build -w @masaha/shared` → exit 0.
- `git grep -n "#PRNUM"` → documents only (api-contract 2, data-model 1, shared-package 1, conventions 1, directory.md 3, occupancy.md 9, v1-mvp 2).
- `git diff --stat origin/main -- apps/web` → only the two `errors.ts` catalogues (1 line each).
- Not run, with why: `test:component`, the web's `build`, `check:build`, `check:classes` — the web change is two catalogue files of strings, whose parity the unit lane checks; CI runs them.

## 12.5 The breaks — each red, each restored from its backup (hash-checked), on the head `1a80fed6`

Harness: the file copied to `%TEMP%\desk-breaks\`, one edit, the named test file run in its lane, the file restored from the copy and checked byte for byte by SHA-256; never `git checkout`. `git status --short` empty afterwards.

- **U1 zone UTC** (`packages/shared/src/core/gazaTime.ts`) — **red**: `Test Files  1 failed (1) · Tests  3 failed (3)` — reads a winter and a summer instant as Gaza's date, weekday and minute 29ms; turns a Gaza date and minute into the instant, on both sides of a daylight-saving change 1ms — `AssertionError: expected { date: '2026-01-15', …(2) } to deeply equal { date: '2026-01-15', …(2) }`
- **U2 fixed +02:00** (`packages/shared/src/core/gazaTime.ts`) — **red**: `Test Files  1 failed (1) · Tests  1 failed | 2 passed (3)` — turns a Gaza date and minute into the instant, on both sides of a daylight-saving change 6ms — `AssertionError: expected 2026-07-01T08:00:00.000Z to deeply equal 2026-07-01T07:00:00.000Z`
- **U3 minute % 1440** (`packages/shared/src/core/gazaTime.ts`) — **red**: `Test Files  1 failed (1) · Tests  1 failed | 2 passed (3)` — reads minute 1440 as the next day's midnight 7ms — `AssertionError: expected 2026-01-14T22:00:00.000Z to deeply equal 2026-01-15T22:00:00.000Z`
- **B1 unverified branch removed** (`apps/api/src/modules/occupancy/liveStatus.ts`) — **red**: `Test Files  1 failed (1) · Tests  1 failed | 9 passed (10)` — an unverified space has no live state, even under a closure or an override 5ms — `AssertionError: expected 'AVAILABLE' to be null`
- **B2 closure branch removed** (`apps/api/src/modules/occupancy/liveStatus.ts`) — **red**: `Test Files  1 failed (1) · Tests  1 failed | 9 passed (10)` — an active closure makes it CLOSED, over an override and within its hours 7ms — `AssertionError: expected 'AVAILABLE' to be 'CLOSED' // Object.is equality`
- **B3 outside-hours branch removed** (`apps/api/src/modules/occupancy/liveStatus.ts`) — **red**: `Test Files  1 failed (1) · Tests  1 failed | 9 passed (10)` — outside today's hours it is CLOSED: before opening, at the closing minute, on a closed day 7ms — `AssertionError: expected 'AVAILABLE' to be 'CLOSED' // Object.is equality`
- **B4 override branch removed** (`apps/api/src/modules/occupancy/liveStatus.ts`) — **red**: `Test Files  1 failed (1) · Tests  1 failed | 9 passed (10)` — an override in force gives its state while open, even without a capacity 8ms — `AssertionError: expected 'AVAILABLE' to be 'FULL' // Object.is equality`
- **B5 no-hours/no-capacity branch removed** (`apps/api/src/modules/occupancy/liveStatus.ts`) — **red**: `Test Files  1 failed (1) · Tests  2 failed | 8 passed (10)` — without any hours there is no live state, an override included 5ms; open without a capacity has no live state 1ms — `AssertionError: expected 'AVAILABLE' to be null`
- **B6 override swapped before the closure** (`apps/api/src/modules/occupancy/liveStatus.ts`) — **red**: `Test Files  1 failed (1) · Tests  1 failed | 9 passed (10)` — an active closure makes it CLOSED, over an override and within its hours 7ms — `AssertionError: expected 'AVAILABLE' to be 'CLOSED' // Object.is equality`
- **B10 requireCan(space.capacity.manage) on GET /occupancy** (`apps/api/src/modules/occupancy/occupancy.manage.routes.ts`) — **red**: `Test Files  1 failed (1) · Tests  2 failed | 4 passed (6)` — answers the owner and reception the status, the capacity, the count and the people present 421ms; lists the people present oldest first, a check-in by its customer's name 250ms — `AssertionError: expected 403 to be 200 // Object.is equality`
- **B11 router mounted outside manage** (`apps/api/src/app.ts`) — **red**: `Test Files  1 failed (1) · Tests  5 failed | 1 passed (6)` — answers the owner and reception the status, the capacity, the count and the people present 464ms; counts open visits and open subscription check-ins, never closed ones or another space's 403ms — `AssertionError: expected 404 to be 200 // Object.is equality`
- **B12a checkedOutAt dropped in visits.openIn** (`apps/api/src/modules/visits/visits.repository.ts`) — **red**: `Test Files  1 failed (1) · Tests  1 failed | 5 passed (6)` — counts open visits and open subscription check-ins, never closed ones or another space's 262ms — `AssertionError: expected 3 to be 2 // Object.is equality`
- **B12b checkedOutAt dropped in visits.openCountsIn** (`apps/api/src/modules/visits/visits.repository.ts`) — **red**: `Test Files  1 failed (1) · Tests  4 failed | 1 passed (5)` — every card and pin carries its live status; an unverified space's is null 510ms; no public answer carries a capacity, a count or an override 540ms — `AssertionError: expected { 'Second Open': 'AVAILABLE', …(5) } to deeply equal { 'Open Room': 'AVAILABLE', …(5) }`
- **B13a checkedOutAt dropped in subscriptions.openCheckInsIn** (`apps/api/src/modules/subscriptions/subscriptions.repository.ts`) — **red**: `Test Files  1 failed (1) · Tests  1 failed | 5 passed (6)` — counts open visits and open subscription check-ins, never closed ones or another space's 257ms — `AssertionError: expected 3 to be 2 // Object.is equality`
- **B13b checkedOutAt dropped in subscriptions.openCheckInCountsIn** (`apps/api/src/modules/subscriptions/subscriptions.repository.ts`) — **red**: `Test Files  1 failed (1) · Tests  4 failed | 1 passed (5)` — every card and pin carries its live status; an unverified space's is null 531ms; no public answer carries a capacity, a count or an override 459ms — `AssertionError: expected { 'Second Open': 'AVAILABLE', …(5) } to deeply equal { 'Open Room': 'AVAILABLE', …(5) }`
- **B14 people by id desc** (`apps/api/src/modules/occupancy/occupancy.service.ts`) — **red**: `Test Files  1 failed (1) · Tests  1 failed | 5 passed (6)` — lists the people present oldest first, a check-in by its customer's name 245ms — `AssertionError: expected [ Array(4) ] to deeply equal [ Array(4) ]`
- **B15 present passed as 0** (`apps/api/src/modules/occupancy/occupancy.service.ts`) — **red**: `Test Files  1 failed (1) · Tests  1 failed | 5 passed (6)` — reads the status from the hours, the capacity and the override 254ms — `AssertionError: expected { status: 'AVAILABLE', …(4) } to match object { status: 'FULL', present: 2 }`
- **B16 deletedAt dropped in closedAt** (`apps/api/src/modules/announcements/announcements.repository.ts`) — **red**: `Test Files  1 failed (1) · Tests  1 failed | 5 passed (6)` — a CLOSURE announcement in force closes it; a deleted, ended or other-type one does not 237ms — `AssertionError: expected { status: 'CLOSED', capacity: 5, …(3) } to match object { status: 'AVAILABLE' }`
- **B17 type dropped in closedAt** (`apps/api/src/modules/announcements/announcements.repository.ts`) — **red**: `Test Files  1 failed (1) · Tests  1 failed | 5 passed (6)` — a CLOSURE announcement in force closes it; a deleted, ended or other-type one does not 257ms — `AssertionError: expected { status: 'CLOSED', capacity: 5, …(3) } to match object { status: 'AVAILABLE' }`
- **B7 overrideUntil without min** (`apps/api/src/modules/occupancy/overrideUntil.ts`) — **red**: `Test Files  1 failed (1) · Tests  1 failed | 1 passed (2)` — each duration ends after its time, or at closing when closing comes first 8ms — `AssertionError: expected 2026-10-18T08:00:00.000Z to deeply equal 2026-10-18T07:45:00.000Z`
- **B8 state as z.string()** (`packages/shared/src/occupancy/requests.ts`) — **red**: `Test Files  1 failed (1) · Tests  1 failed | 1 passed (2)` — an override takes one of the three states and one of the four durations 6ms — `AssertionError: expected null to deeply equal { state: [ 'invalid_choice' ] }`
- **B18 until from the database now()** (`apps/api/src/modules/occupancy/occupancy.service.ts`) — **red**: `Test Files  1 failed (1) · Tests  5 failed | 4 passed (9)` — the owner and reception set an override for 30 minutes, ending at now + 30 min, audited 405ms; an override asked for 2 hours ends at today's closing when closing is sooner 251ms — `AssertionError: expected { Object (status, capacity, ...) } to deeply equal { Object (status, capacity, ...) }`
- **B19 open check removed** (`apps/api/src/modules/occupancy/occupancy.service.ts`) — **red**: `Test Files  1 failed (1) · Tests  1 failed | 8 passed (9)` — refuses an override while the space is not open by its hours, or has none: 409 SPACE_NOT_OPEN, writing nothing 217ms — `AssertionError: expected 200 to be 409 // Object.is equality`
- **B20 in-force check removed on clear** (`apps/api/src/modules/occupancy/occupancy.service.ts`) — **red**: `Test Files  1 failed (1) · Tests  1 failed | 8 passed (9)` — clears the override in force, audited space.statusOverrideCleared; clearing none writes nothing 325ms — `AssertionError: expected { capacity: 10, …(3) } to deeply equal { capacity: 10, …(3) }`
- **B21 validate removed** (`apps/api/src/modules/occupancy/occupancy.manage.routes.ts`) — **red**: `Test Files  1 failed (1) · Tests  1 failed | 8 passed (9)` — refuses an invalid body with 422 before anything is written 213ms — `AssertionError: expected 500 to be 422 // Object.is equality`
- **B22 setOverride upsert nulls capacity on update** (`apps/api/src/modules/occupancy/occupancy.repository.ts`) — **red**: `Test Files  1 failed (1) · Tests  2 failed | 7 passed (9)` — clears the override in force, audited space.statusOverrideCleared; clearing none writes nothing 253ms; the first override creates the occupancy row with no capacity; it never touches a capacity 266ms — `AssertionError: expected { status: null, capacity: null, …(3) } to match object { status: 'AVAILABLE', …(2) }`
- **B23 can() on space.links** (`apps/api/src/modules/occupancy/occupancy.service.ts`) — **red**: `Test Files  1 failed (1) · Tests  1 failed | 8 passed (9)` — a reception link deactivated while the override waits on the space's lock refuses it with 403 232ms — `AssertionError: expected 200 to be 403 // Object.is equality`
- **B24 capacity upsert nulls the override** (`apps/api/src/modules/occupancy/occupancy.repository.ts`) — **red**: `Test Files  1 failed (1) · Tests  2 failed | 8 passed (10)` — changes and clears a capacity, keeping the row and its override 203ms; setting the capacity keeps an override in force 317ms — `AssertionError: expected { capacity: 50, …(3) } to deeply equal { capacity: 50, …(3) }`
- **B9 availableNow as z.coerce.boolean()** (`packages/shared/src/directory/requests.ts`) — **red**: `Test Files  1 failed (1) · Tests  1 failed | 31 passed (32)` — availableNow takes true only 9ms — `AssertionError: expected { page: 1, limit: 20, …(3) } to match object { availableNow: false }`
- **B25 liveStatus null for all** (`apps/api/src/modules/directory/directory.service.ts`) — **red**: `Test Files  1 failed (1) · Tests  2 failed | 3 passed (5)` — every card and pin carries its live status; an unverified space's is null 485ms; availableNow keeps only AVAILABLE spaces, before the page is cut: every page full, the total right 320ms — `AssertionError: expected { 'Second Open': null, …(5) } to deeply equal { 'Open Room': 'AVAILABLE', …(5) }`
- **B26 present added to the public answer** (`apps/api/src/modules/directory/directory.service.ts`) — **red**: `Test Files  1 failed (1) · Tests  2 failed | 3 passed (5)` — no public answer carries a capacity, a count or an override 421ms; GET /spaces/:slug/occupancy answers { status } for a listed space, with the public cache; 404 for a hidden, deleted or unknown one 288ms — `AssertionError: expected { success: true, data: { …(2) } } to deeply equal { success: true, …(1) }`
- **B27 availableNow applied after the page** (`apps/api/src/modules/directory/directory.service.ts`) — **red**: `Test Files  1 failed (1) · Tests  2 failed | 3 passed (5)` — availableNow keeps only AVAILABLE spaces, before the page is cut: every page full, the total right 330ms; availableNow on the map keeps the same spaces 294ms — `AssertionError: expected { currentPage: 1, limit: 1, …(4) } to match object { totalRecords: 2, totalPages: 2 }`
- **B28 listed check removed on /occupancy** (`apps/api/src/modules/directory/directory.service.ts`) — **red**: `Test Files  1 failed (1) · Tests  1 failed | 4 passed (5)` — GET /spaces/:slug/occupancy answers { status } for a listed space, with the public cache; 404 for a hidden, deleted or unknown one 344ms — `AssertionError: expected 200 to be 404 // Object.is equality`

Beyond §9's list: B12b and B13b (the counts' filters, the directory's path) — B13b needed a closed check-in in T17–T21's setup, added before the breaks and folded into C4 (`--fixup` + autosquash). B6 is the closure and the override swapped (the override then wins over a closure).

## After the fixup — the head `1a80fed6`
- `git rebase -x "npm run lint && npm run typecheck"` from the base: `CHECK-OK` on each of the 4 commits, `Successfully rebased` (shas unchanged: f967c822, a9f60c7b, 4bce0d7f, 1a80fed6).
- `npm run test:api` re-run (its directory file changed after the first run): exit 0, `Test Files  55 passed (55)`, `Tests  899 passed (899)`. `format:check` exit 0. The unit lane's files did not change since it passed.

## 12.6 The real run — API on 3321, `masaha_b_dev` (2026-10-19, about 17:44 in Gaza, a Monday)
`npm run dev -w @masaha/api` in the background; `prisma migrate status` → `Database schema is up to date!`;
`curl.exe -s http://localhost:3321/health` → `{"status":"ok","db":"up",…}`. Signed in as `demo-owner@example.com`,
`demo-reception@example.com` (`SEED_DEMO_PASSWORD` read from `.env` into the script, never printed) and the `SEED_ADMIN_*` admin.
The demo space (`masaha-demo`, id 1) is open on Mondays 08:00–22:00 and already had one open visit and one open check-in (demo data),
so *present* is 3 with the inserted visit, not the plan's 1.
- `PUT …/hours` (the week as it is, open now, shifts kept) → 200. `PUT …/capacity { capacity: 1 }` → 200 `{"capacity": 1}`.
- `INSERT INTO visits … 'Real run' …` through `psql` → visit 5.
- `GET …/occupancy` as reception → 200, `status FULL`, `capacity 1`, `present 3`, `override null`, *Real run* listed as a `VISIT`.
- `PUT …/status-override { state: "AVAILABLE", duration: "MINUTES_30" }` as reception → 200, `status AVAILABLE`, `override.until 2026-10-19T15:14:34.264Z` (30 min ahead).
- `GET /api/v1/spaces?availableNow=true` → 200, `masaha-demo` listed with `liveStatus: AVAILABLE`.
- `GET /api/v1/spaces/masaha-demo/occupancy` → 200 `{"success": true, "data": {"status": "AVAILABLE"}}` only, `Cache-Control: public, max-age=30`.
- `DELETE …/status-override` as the owner → 200, `status FULL`, `override null`.
- `GET …/occupancy` as the admin → 404 `not_found`.
- `SELECT action FROM audit_logs ORDER BY id DESC LIMIT 3` → `space.statusOverrideCleared, space.statusOverridden, space.capacityEdited`.
- Tidied: the inserted visit closed through `psql` (`UPDATE 1`); the capacity put back to 35 → 200 (the demo's own; an extra `space.capacityEdited`).
- Stopped by process id (tsx watch 10632, the server 14676, pino-pretty 15064); `Get-NetTCPConnection -LocalPort 3321` → nothing: port 3321 free.

## 12.7 The PR number, push and PR
- Next number from GitHub: **94**. `git filter-branch` replaced `#PRNUM` → `#94` in each commit's documents (7 files, 19 lines); `git grep -n '#PRNUM'` → nothing. Commits now:
  `e7def25d feat(core): read the time in Gaza` (33) · `2c9bac4c feat(occupancy): derive the live status` (39) · `21a9f88e feat(occupancy): override the live status` (41) · `e07308b4 feat(directory): show the live status` (37).
- `npm run check:links` → `2316 links … all resolve.` `git diff --stat origin/main` → 59 files.
- `git push -u origin feat/live-status` → new branch. Labels `feat`, `area:api`, `area:docs`, `area:web` exist.
- `gh pr create --assignee @me …` → **https://github.com/Basel-Ghonaim/masaha/pull/94** — the number equals `n`.

## 12.8 CI, CLEAN, conflicts
- `gh pr checks 94 --watch` → exit 0; every check `pass`: lint, format:check, typecheck, test:unit, test:component, check:classes, check:links, build, test:api (CodeRabbit skipped for manual review).
- `gh pr view 94 --json headRefOid,mergeStateStatus,statusCheckRollup` → head `e07308b4e6099283572ff9c4dbf9a4c1cb5673b3` (= `git rev-parse HEAD`), `CLEAN`, all `SUCCESS`.
- Early conflict check: the open PRs are #94 (this) and **#93** `feat/admin-users` (worker A, head `4daedc94`). `git merge-tree --write-tree HEAD 4daedc94` → exit 0, tree `2267d1c0`, **clean**. The two PRs' own changes (each from its merge base; #93 is based on #91) share one file, `docs/project/overview.md` (*Built*, each its own line), merged cleanly by Git. Not merged, not rebased.

---

# Final report — DESK PR 1

1. **The pull request:** #94 https://github.com/Basel-Ghonaim/masaha/pull/94 — `feat(occupancy): derive the live status` — head `e07308b4`, CI green on it, `CLEAN`.
2. **The commits:** `e7def25d feat(core): read the time in Gaza` (33) · `2c9bac4c feat(occupancy): derive the live status` (39) · `21a9f88e feat(occupancy): override the live status` (41) · `e07308b4 feat(directory): show the live status` (37). Each linted and typechecked (`rebase -x`).
3. **Run:** lint, typecheck (each commit and the head); `test:unit` shared 227 / api 757 / web 833; `test:api` 55 files, 899 tests (twice, the second after the fixup); `format:check`; `check:links` (2316); `build -w @masaha/shared` — all exit 0. **Not run locally:** `test:component`, the web's `build`, `check:build`, `check:classes` (two catalogue lines of strings; CI ran test:component, build and check:classes green).
4. **Breaks and red-first:** 33 breaks, 33 red (12.5, each with its lines); every new test file seen failing first (C1–C4 sections).
5. **Problems and their solutions:**
   - Lint refused `core → @date-fns/tz` (shared-package R3): **stopped**; the owner chose option 1 (R3 and its lint policy admit `@date-fns/tz` in core, that one package only); resumed.
   - My template-literal number (`restrict-template-expressions`): `String(…)`.
   - An absent enum answers `invalid_choice`, not `required`, by the project's `toFieldErrors`: my U14 expectation corrected (as the packages' test says).
   - The audit writer takes no `null` for `before`/`after`: absent instead (stored as none).
   - The `SpacesService` fake in `space-links.service.unit.test.ts` needed `weekOf` and `weeksFor` to typecheck.
   - The list's and the pins' exact-shape tests needed the new `liveStatus` field.
   - Heredoc-embedded Python failed to parse twice: the scripts moved to scratchpad files.
   - My break results were first appended to this report in the console's code page (cp1252, CRLF): re-encoded to UTF-8 with LF.
6. **Unexpected, even if solved:**
   - The plan's §12.2 check 3 looked only at the API's level map; the shared package's own core rule (R3) was the one that refused.
   - The demo space already had one open visit and one open check-in, so the real run's *present* was 3, not the plan's 1 (`FULL` at capacity 1 either way).
   - Worker A's #93 is based on #91, before #92: a plain `git diff origin/main 4daedc94` shows #92's occupancy files as if #93 touched them; from each merge base, only `overview.md` is shared.
   - Stopping the dev API: the background task reports exit 127 once its processes are stopped by id (expected; the port is free).
7. **Early conflict check:** #93 — clean (12.8).
8. **Departures from the prompt and the plan, each with its reason:**
   - **R3 amended** (`docs/architecture/shared-package.md`, `eslint.config.js`), by the owner's decision of 2026-10-19 after the stop — not in the plan's files.
   - `space-links.service.unit.test.ts`, `directory/list.api.test.ts`, `directory/pins.api.test.ts` edited (not in §7): the types and the exact shapes required it.
   - `openCountsIn`, `openCheckInCountsIn`, `weeksFor`, `statesFor`, `liveStatusFor`, `availableAmong` built in C4 (where the directory first uses them), not C2; `publicListing.service.ts` needed no change.
   - T1–T6's red was seen with the route removed (the read's code was written before that API test); T16 (written after the override code) has its red in B24.
   - T16 added as a new test through the routes, beside the existing capacity test that already kept the override.
   - A closed check-in added to T17–T21's setup (folded into C4) so B13b, beyond §9's list, could go red; B12b and B13b added to the breaks.
   - `GET /spaces/:slug/occupancy` answers any listed space (`{ status: null }` when unverified), per §4's C4 line; v1-mvp's removed row had said "verified spaces only".
   - The real run re-saved the demo's hours as they were (already open now) and put the demo's capacity back to 35 afterwards; the inserted visit closed as planned.
   - The PR body is in the scratchpad (`pr-body.md`), not `$env:TEMP` directly; nothing else written outside the repository but this report.
