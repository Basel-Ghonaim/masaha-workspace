# SUBSCRIPTIONS PR 3 — `feat/subscription-check-ins` — the executor's report

Executor: Claude Code (Opus 5.5), 2026-10-22, in `C:\dev\masaha\app-b`.

## Read
As the exec prompt §0 lists: the plan's named parts, `0_CARRIED_FROM_106.md`, the review's findings 1–9,
`4_REPORT_PR2.md`'s departures and hand-over. `start-work-item` not run (the owner's instruction).

## §1 Preconditions — all held
- `gh pr view 106` → `MERGED` (merge `ab0dadbd`); `gh pr view 107` → `MERGED`.
- `C:\dev\masaha\app-b` detached at `5e8379af` = `origin/main`, clean.
- `gh pr list --state open` → none.

## §12.1 Before the branch
- `git diff --name-status d0acc06b origin/main` (PR 2's head → main): only `apps/web` (directory, map,
  platform-settings, the space page) and `docs` (findings 130–136, 40, 46, the index, setup, directory,
  spaces, frontend architecture, design-system foundation, overview). **No API or shared code file changed**:
  nothing this PR names changed.
- Findings index on main: 111 open; 120–123 this item's; 130–136 worker A's. 124–129 free (this PR: 124, 125
  carried; new ones 126 on).
- `git switch --no-track -c feat/subscription-check-ins origin/main` ✔.
- `docker start masaha-postgres-1` ✔; `apps/api/.env` names `masaha_b_dev`, `masaha_b_test`, `PORT=3321`
  (by pattern, not printed).
- `npm run build -w @masaha/shared` → exit 0.
- `prisma migrate status` → `24 migrations found` · `Database schema is up to date!`.

## C0 — Carried from #106 (each code fix red first, then green)
| # | Commit | Subject (chars) | Red before the code | Green after |
|---|---|---|---|---|
| 1 | `99919f9a` | `fix(desk): refuse a key that subscribed another` (47) | `subscribe.api.test.ts` › "a key that subscribed another customer is a conflict under this one's path, writing nothing": `AssertionError: expected 201 to be 409` | `Tests 10 passed (10)` |
| 3 | `fbe5a521` | `fix(customers): keep the phone's suffix match` (45) | unit `customerSearch.unit.test.ts` › "a whole number … or its national digits at the end of one" × (`1 failed \| 2 passed`); API `desk/customers.api.test.ts` (T22): `expected [ 'Dana' ] to deeply equal [ 'Dana', 'Huda' ]` | unit `3 passed (3)`; API (+ `customers/customers.api.test.ts`) `19 passed (19)` |
| 4 | `51f78000` | `fix(desk): warn only on older debts` (35) | `renewal.api.test.ts` › "a retry after its own renewal, still unpaid, warns of no debt": `expected { warnings: [ 'CUSTOMER_HAS_DEBT' ] } to be undefined` | (+ subscribe) `20 passed (20)` |
| 5 | `20d704c0` | `fix(desk): read a check-in's minutes in SQL` (43) | **not red — departure, stated:** the new test ("each check-in's minutes are counted as the attendance is: their sum is progress.minutesUsed", stays of 30 min 59.999 s and 44 min 40 s) passes before the change, because the TypeScript and SQL rules agree today; the item removes the second copy. Its proof is break **I5** (the SQL's `floor` → `round`): `AssertionError: expected [ 31, 45 ] to deeply equal [ 30, 44 ]`, restored sha256 same, green again | `4 passed (4)` |
| 2, 6, 7, 8 | `e91c5228` | `docs(subscriptions): record #106's review` (41) | — (documents) | `check:links` exit 0 |

- Item 1: 409 `conflict`, no code, message "This idempotency key made another subscription", checked right after the key lookup; the contract's errors line gains it (`#PRNUM`).
- Item 3: a whole number answers `{ phone, phoneDigits: '0' + national }`; the repository matches `phone = $1 OR <digits> LIKE '%' || $2`. Contract `q` line and `customers.md` history (`#PRNUM`).
- Item 4: only the items before the subscription in `itemBalances`' order (the allocation's) count; the contract already said "older".
- Item 5: `subscriptions.repository.checkInsOf` is raw SQL with `subscription_usage`'s minutes expression; `SubscriptionCheckIn` gains `minutes`; the desk no longer computes them. `subscriptions.md` says so.
- Item 2: `subscriptions.md`'s *Authority* names the module's routes and the desk's. Item 6: the contract's archived-file line dated 2026-10-21. Item 7: `payments.md` decision line past the 49th debt. Item 8: findings **124** and **125**, files and index lines.
- The docs commit's first subject was 52 characters; amended before anything else to 41.
- lint and typecheck after each commit: exit 0 each (items 1, 3, 4, 5). For 3 and 4 they ran on a tree that already held the next item's uncommitted edits; the `rebase -x "npm run lint && npm run typecheck"` before the push checks every commit alone.

## C1 — `8b5b7888` `refactor(occupancy): define present once` (40)
- `occupancy/present.ts`: `presentIn(spaceId, tx?)` → `{ visits, checkIns, count }`, `presentCountsIn(spaceIds)`,
  `isPresent(spaceId, customerId, tx?)`; `occupancy.service.ts`'s `peopleIn`, `liveStatusFor` and `checkInWarnings`
  call them, and the service exposes `presentIn` and `isPresent`. **Also, as D12's "no other count of *present*
  remains":** the desk's archive (`isPresent`) and the customer's file (`presentIn`) no longer read the two sources
  themselves.
- T2 (`present.api.test.ts` › "the read, the check-in's warning and the directory count the same people present")
  is **green before the code**, as a refactor's test is (the three counts agreed); its proof is **B4** (the
  directory's count from visits only): `AssertionError: expected 'AVAILABLE' to be 'FULL'`, restored sha256 same,
  green again.
- Green: `src/modules/occupancy` + `directory/liveStatus` + `desk/{archive,customerFile,checkIn}` →
  `Test Files 7 passed (7)`, `Tests 55 passed (55)`.
- §12.2 check 1: `grep openIn|openCheckInsIn|openCountsIn|openCheckInCountsIn` in `occupancy` and `desk` lists
  only `present.ts` ✔.
- lint first exit 1 (`@typescript-eslint/unbound-method` on `isPresent: present.isPresent`); fixed by wrapping
  both, folded into C1 (`--fixup` + autosquash, with item 3's Prettier fixup of `customerSearch.ts`); then lint 0,
  typecheck 0 on the head.
- Docs: `occupancy.md` (*Present* paragraph, who uses it, decision, code map, history), conventions §9
  *occupancy*, `desk.md` (the file and the archive read `occupancy`'s *present*), `subscriptions.md` (*Who uses
  it*), finding 111 resolved + index moved to *Resolved*.

## C2 — `0b1eebf9` `feat(desk): check a subscriber in` (33)
- Shared: four codes (`add-error-code`: `core/errors.ts`, both catalogues with §13 Q2's text, contract §6, provoked
  by T4); `checkInSubscriberSchema` and `DeskCheckIn` in `@masaha/shared/subscriptions` (L3: the list in C4 is
  `subscriptions`', which may not import `desk`'s L5 types); `DESK_WARNINGS` gains the four, in order.
- API: `subscriptions/limits.ts` (pure: `subscriptionWarnings(state, { checkedInToday })`, `progressWithout`);
  `subscriptions` service `findCheckInByKey`, `limitWarnings(spaceId, subscriptionId, at, withoutId, tx)`,
  `checkIn` (audited `checkIn.checkedIn`); repository `findCheckInByKey`, `createCheckIn`, `attendanceOf` (one
  query: another check-in today; the excluded one's day, minutes, shared day — dated in SQL as
  `subscription_usage` dates), `STAY_MINUTES` / `GAZA_DAY` fragments (the C0 item 5 query uses the first);
  `desk.checkInSubscriber`, controller, `POST /check-ins` (`requireCan('attendance.record')` → key → validate).
- **Red before the code:** U1 `limits.unit.test.ts` → `Cannot find module './limits.ts'` (`no tests`). The API
  file was written after the code, so its red was taken with the route **not mounted** (the routes file backed
  up, the route removed, restored by copy, sha256 `536bf9c4…` before and after): `9 tests | 9 failed`.
- First green run: 8/9 — my own test's defect (expected `invalid_type`; the project maps a wrong type to
  `invalid_format`); test corrected → `Tests 9 passed (9)`. U1 → `Tests 8 passed (8)`.
- lint 0, typecheck 0 (web included: catalogue parity).
- **Departure, stated (small, not in the plan):** a check-in key that checked in **another subscription** is 409
  `conflict`, no code — the rule carried item 1 set for the subscribe and the payments already follow; break B7k.
- **Retry warnings:** the space's (`SPACE_FULL`, hours) as of the retry with the check-in counted present, as the
  visit's retry already does (documented); the limits without it (D11 step 2).
- Breaks (`scripts\p3-c2.json`, `p3-c2-breaks.out`), each red, restored (sha256 same), green again:
  - B1 days `>=`→`>`: `expected [] to deeply equal [ 'DAYS_PER_WEEK_USED' ]` (3 tests ×); B1h hours `>=`→`>`:
    `expected [] to deeply equal [ 'HOURS_PER_DAY_USED' ]`; B2 "today not counted" dropped:
    `expected [ 'DAYS_PER_WEEK_USED' ] to deeply equal []`.
  - B5 audit skipped: `expected [] to deeply equal [ { actorId: 2, …(6) }, …(1) ]`.
  - B6 warnings after the create: `expected [ 201, undefined ] to deeply equal [ 201, [ 'DAYS_PER_WEEK_USED' ] ]`.
  - B7 `findCheckInByKey` skipped: `expected [ 201, 409 ] to deeply equal [ 201, 201 ]`; B7k the other
    subscription's key let through: `expected 201 to be 409`.
  - B8 the space's lock removed: `Error: 2 request(s) never waited on a lock`.
  - B9 the visit side of `isPresent` dropped: `expected 201 to be 409`.
  - B10 the archived check removed: `expected 201 to be 409`.
  - B11 `can()` on `space.links`: `expected 201 to be 403`.
  - B12 the subscription's warnings read before `lockAtDesk`: `expected undefined to deeply equal [ 'SUBSCRIPTION_EXPIRED' ]`.
  - B13 the customer read before the lock: `expected 201 to be 409`.
- Not a break: "its shift" (exec prompt §2's list) — the plan has no shift warning for a check-in; nothing to break.

## C3 — `8e116480` `feat(desk): check a subscriber out` (34)
- `CheckInCheckOut` (`@masaha/shared/desk`); `subscriptions` `lockCheckInIn` (`FOR UPDATE`, the space's only),
  `checkOut` (`MANUAL`, audited `checkIn.checkedOut`); `desk.checkOutSubscriber` with `withMoney`'s paid and
  balance; `POST /check-ins/:checkInId/check-out` (`requireCan('attendance.record')`, no key).
- Red before the code (T12–T14, the route absent): `Tests 3 failed (3)`, `expected 404 to be 200`. Green:
  `Tests 3 passed (3)`. lint 0, typecheck 0.
- Breaks (`p3-c3.json`, `p3-c3-breaks.out`), each red, restored (sha256 same), green again:
  - B14 `checkoutMethod` left null: `expected 500 to be 200` (the `CHECK`).
  - B15 the closed branch removed: `expected { id: 1, …(7) } to match object { id: 1, …(4) }` (closed again, MANUAL).
  - B16 `can()` on `space.links`: `expected 200 to be 403`.
- Docs: contract (the route, `CheckInCheckOut`), `desk.md`, conventions §9, `subscriptions.md`.

## C4 — `67c553fe` `feat(subscriptions): list check-ins` (35)
- `checkInsQuerySchema` (`open=true` | `from`/`to` ≤ 92 days, `page`, `limit`) and `CHECK_IN_RANGE_MAX_DAYS` in
  `@masaha/shared/subscriptions`; `subscriptions` `checkInsIn` and `deskCheckIns` (each check-in with its
  customer — new `customers.contactsOf`, one query — and its subscription's state; the desk's check-in and
  check-out answer through it); repository `openCheckInRowsIn`, `checkInsBetween` (raw SQL, `GAZA_DAY`);
  `GET /check-ins` on the subscriptions' router (D1's placement; no `requireCan`, #86); `app.ts` builds
  `customers` before `subscriptions` and passes it.
- Red: U2 (`requests.unit.test.ts`) → `TypeError: Cannot read properties of undefined (reading 'parse')` (2 ×);
  T15–T17 → `Tests 3 failed (3)`, `expected 404 to be 200`. Green: U2 `Tests 4 passed (4)`; with C2's and C3's
  files `Test Files 3 passed (3)`, `Tests 15 passed (15)`.
- lint first exit 1 (`no-confusing-void-expression` in the schema's helper), fixed, folded into C4 (fixup +
  autosquash); `eslint` on the folder 0; typecheck 0.
- Breaks (`p3-c4.json`, `p3-c4-breaks.out`), each red, restored (sha256 same), green again:
  - B3 the 92-day bound removed: `expected null to deeply equal { to: [ 'out_of_range' ] }`.
  - B17 a `take: 20` left on the open list: `expected [ Array(20) ] to deeply equal [ Array(21) ]`.
  - B18 the range by UTC date: `expected [ 5, 4 ] to deeply equal [ 4, 3 ]`.
- Docs: contract (the route, §4's exception), `subscriptions.md`, `customers.md`, v1-mvp (step 8 *Built*, the
  route table's *Built* sentence), overview.

## §12.2 first checks (PR 3)
1. `grep openIn|openCheckInsIn|openCountsIn|openCheckInCountsIn` in `occupancy` (and `desk`) → only `present.ts` ✔.
2. The level rule: `npm run lint` exit 0 with `desk` importing `subscriptions` and `occupancy`, and `subscriptions`
   importing `customers` ✔.
3. The partial unique index: on `masaha_b_dev`, in `BEGIN … ROLLBACK`, two open check-ins by raw insert for one
   customer → `ERROR: duplicate key value violates unique constraint "check_ins_customer_id_key"` ✔ (nothing kept:
   open check-ins after it `0`, as before).

## §12.4 Verification on the head `67c553fe` (each once, one at a time; free memory 4,976,304 KB, no vitest/tsc running)
| Command | Exit | Result line |
|---|---|---|
| `npm run build -w @masaha/shared` | 0 | — |
| `npm run lint` | 0 | — |
| `npm run typecheck` | 0 | — |
| `npm run test:unit` | 0 | shared `Test Files 21 passed (21)` / `Tests 249 passed (249)`; web `61 passed (61)` / `857 passed (857)`; api `115 passed (115)` / `917 passed (917)` |
| `npm run test:api` | 0 | `Test Files 79 passed (79)`, `Tests 1107 passed (1107)` |
| `npm run format:check` | 0 | `All matched files use Prettier code style!` |
| `npm run check:links` | 0 | `2626 links in 176 documents and 1743 source files all resolve.` |
- `git grep -n "#PRNUM"` → documents only (11 files under `docs/`); `git diff --stat origin/main -- apps/web` → only
  the two `errors.ts`; `-- package.json package-lock.json` → empty. **47 files** changed.
- Not run locally (CI judges): `test:component`, the web's `build`, `check:build`, `check:classes`.
- Per commit: `git rebase -x "npm run lint && npm run typecheck" origin/main` → exit 0, `OK` for each of the nine
  commits (`99919f9a` … `67c553fe`); the head unchanged.

## §12.6 The real run (API on 3321, `masaha_b_dev`, head `67c553fe`)
- `npm run dev -w @masaha/api` in the background; `curl.exe -s http://localhost:3321/health` →
  `{"status":"ok","db":"up",…}`. `node scripts\realrun3.mjs` → **exit 2**:
```
PASS precondition: محمد not present; his split-week subscription (3 days a week) read; 0 present 200 -
     before: status EXPIRED, days this week 0, checked in today false; the limits expected: ["SUBSCRIPTION_EXPIRED"]
PASS reception checks محمد in: warnings ["SUBSCRIPTION_EXPIRED"] 201 -
PASS the same key: the same check-in and the same warnings 201 -
NOT RUN سارة present → 409: سارة is not present in the demo data (her open check-in was closed)
PASS SUBSTITUTE محمد, present by the run's check-in, another key: refused 409 MEMBER_ALREADY_CHECKED_IN
PASS the occupancy counts him: 1 present 200 -
PASS the open check-ins: 1, his among them, no meta 200 -
PASS check-out: MANUAL, paid 10000, balance 5000 200 -
PASS check-out again: answered as it is 200 -
PASS the last week's check-ins: 1, his first 200 -
audit (latest first): checkIn.checkedOut, checkIn.checkedIn, visit.autoCheckedOut, visit.autoCheckedOut
1 NOT RUN, the rest PASS
```
- **The split-week case:** the demo week holds **0** of its days and the subscription is **EXPIRED** (the seed's
  dates have passed), so the check-in warned `SUBSCRIPTION_EXPIRED`, not `DAYS_PER_WEEK_USED` (recorded, as the plan asks).
- **NOT RUN — the plan's case "the present demo subscriber (سارة) → 409":** nobody is present in `masaha_b_dev`
  (`check_ins` open: 0; the occupancy read `present: 0`): the auto check-out has closed the seed's open check-in.
  Not changed through the app. The same rule was shown on the run's own check-in (محمد, another key → 409
  `MEMBER_ALREADY_CHECKED_IN`), labelled SUBSTITUTE. Per exec prompt §1.7 / §3: **stopped here, before #PRNUM and
  the push**, to ask the owner.
- **Data changed by the run:** one check-in of «محمد عوض» on «أسبوعان، 6 أيام», checked in and checked out (MANUAL)
  today, with its two audit entries (`checkIn.checkedIn`, `checkIn.checkedOut`). Nothing else.
- The server stopped by process id (`tsx watch` 13168, the server 28000, `pino-pretty` 16540); port 3321 free;
  `scripts\server.log` deleted. Worker A's `pino-pretty` processes (under `C:\dev\masaha\app\`) untouched.
- **The owner's answer (2026-10-22):** accept the substitute and continue (#PRNUM, push, PR, CI).

## §12.7 PR number, push, PR
- An open PR appeared meanwhile: **#108** `feat/space-photos-status` (worker A, 21 files), sharing **no file** with this PR.
- `prnum3.sh 109` (prnum.sh adapted: branch `feat/subscription-check-ins`, backup `backup/check-ins-pre-prnum`,
  body `pr3-body.md`; its checks kept) → `PRNUM OK #109 e262298e (was 67c553fe)`; `git grep "#PRNUM"` empty;
  `check:links` 0 (`2626 links … all resolve.`), `format:check` 0.
- Labels exist (`feat`, `area:api`, `area:docs`, `area:web`). `git push -u origin feat/subscription-check-ins` ✔;
  `gh pr create` → **#109** https://github.com/Basel-Ghonaim/masaha/pull/109 (= the expected number).
- **Conflicts (§12.8):** `git merge-tree --write-tree HEAD 5c3122ff` (#108's head) → exit 0, clean.

## §12.8 CI and CLEAN
- `gh pr checks 109 --watch` → every check passed on head `e262298eb5efdd47ebb82fefc182080b507db0a2` (= local
  `git rev-parse HEAD`): build 32s, check:classes 37s, check:links 33s, format:check 40s, lint 1m56s, test:api 6m47s,
  test:component 10m28s, test:unit 2m20s, typecheck 56s, CodeRabbit pass ("Review rate limited").
- `gh pr view 109` → `mergeStateStatus: CLEAN`. Not merged.
- Final: `git status --short` clean; port 3321 free; 47 files.

## Departures from the plan (all)
1. Carried item 5's test was green before its code (the two rules agreed); proved by break I5.
2. C1's T2 was green before its code (a refactor); proved by B4. The desk's archive and the customer's file also use
   `occupancy`'s *present* (D12's "no other count remains").
3. A check-in key that checked in another subscription → 409, no code (carried item 1's rule); B7k.
4. `DeskCheckIn` in `@masaha/shared/subscriptions` (L3), not `desk`, since `subscriptions` lists check-ins;
   `customers.contactsOf` added for the lists; `app.ts` builds `customers` before `subscriptions`.
5. The C2 API file's red was taken with the route unmounted (the file was written after the code).
6. Real run: the plan's "present سارة" case NOT RUN (nobody present in the demo data); a substitute on the run's own
   check-in, which the owner accepted; the split-week check-in warned `SUBSCRIPTION_EXPIRED` (the demo dates have passed).
- Read beyond §0's list: the plan's D1/D2 rows for PR 3 (the routes and `DeskCheckIn`), as the shapes live there.
