# Review of #132 — R2: the whole API (identity, accounts, staff, owners, jobs, migrations, desk money) — Claude Code, Opus 5.5 (claude-opus-5-5)
Head: a12c0790 · commits 35 · checks: green (every check on a12c0790; CodeRabbit skipping) · head moved during the review: no (a12c0790 at start and end, CLEAN)
Verdict for my range: mergeable after a fix round

Read only from commit objects (`git show <sha>`, `git show a12c0790:<path>`, `git grep … a12c0790`). Nothing run: no tests, breaks, npm, database or servers. Whatever I say about a test's red or a break comes **only from the lanes' reports** unless I say I read the assertion.

## Findings (verified defects only, most severe first)

### R2-F1 — should-fix · A single stay that always fails makes most runs answer 500 again (finding 114 reopened)
- Where: `apps/api/src/modules/visits/visits.service.ts:522` and `apps/api/src/modules/subscriptions/subscriptions.service.ts:700` at a12c0790 (`stalled = batch.length > 0 && closed === 0 && failed - failedBefore === batch.length`). The contract states the opposite: `docs/api/api-contract.md:1136` ("one bad stay never turns every call red"). So does the router's JSDoc (`shared/jobs/jobs.routes.ts`).
- Seen in the code: `batch` is `due.slice(0, AUTO_CHECKOUT_BATCH)`, so it holds whatever is due now, often only one stay. A run counts as "stalled" when every stay in that batch failed, whatever the batch's size. `jobs.routes.ts` then throws `server` for the whole run.
- Scenario: one visit can never be closed. T54 builds exactly this case: its `hourRateAgorot` makes the charge overflow the column. Most cron runs have no other stay due, especially at night: the batch is `[that visit]`, nothing closes, and the run answers **500**. That repeats every 5 minutes until someone fixes the data. A run where other stays fall due answers 200, because they close. This is finding 114's failure, which #102 resolved: a free cron service may switch the endpoint off after a series of red calls. That would stop every space's auto check-out, plus the new sweeps and the reclaim, which share the endpoint. Finding 121 asked for a 500 only when the failures *filled the batch* (500 stays). The plan's D2.4 wrote "the batch they took", and the code and T54 follow that wording, so the departure comes from the plan.
- Fix: stalled only when the batch was full: `batch.length === AUTO_CHECKOUT_BATCH && closed === 0 && failed - failedBefore === batch.length`, in both services. T54 and its subscriptions twin then need a full batch of failing stays: one `INSERT … generate_series(1, 500)` of failing visits, plus one check-in, to cover both jobs. Add a test that one failing stay alone answers 200 with `failed: 1`, which is 114's guarantee. Correct the contract line and finding 121's *Resolution* to say "its batch full". · Belongs: a fix round on #132 (folded into `f0240b98`).

### R2-F2 — should-fix · A stranger can retire a self-registered account that was really used (S1 does not hold "one recovered after use")
- Where: `apps/api/src/modules/auth/auth.service.ts:180-189` (`freeAddress`), `apps/api/src/modules/users/users.service.ts:69` (`replaceableHolder`) and `apps/api/src/modules/audit/audit.repository.ts` (`hasActed`) at a12c0790. The document making the false claim is `docs/backend/security.md:53` ("keeps a real account (an owner whose admin-issued password expired, **or one used before**) from being taken").
- Seen in the code: an account is replaceable when four things hold:
  - it has no Google subject;
  - it has `mustChangePassword` with an expired `temporaryPasswordExpiresAt`;
  - it holds no active OWNER link;
  - `hasActed` is false, meaning no audit entry with it as actor, no favourite and no data report.

  Self-registration writes no audit entry; `AUDIT_ACTIONS` has no `user.registered` and no password-change action. The admin can issue a temporary password to any account that has a password (`POST /admin/users/:userId/temporary-password` → `issueTemporaryPasswordFor`, valid 7 days).
- Scenario:
  1. Sara registers `sara@example.com` herself and uses the site for months without saving a favourite, reporting or editing her profile.
  2. She loses access to her inbox and asks the platform (the forgot page's «لا يمكنك الوصول إلى بريدك؟» → WhatsApp). The admin issues her a temporary password, which she doesn't use within 7 days.
  3. Anyone who registers `sara@example.com` gets 201: Sara's account is suspended, its sessions end, its address becomes `replaced-{id}@replaced.invalid`, and the stranger holds an account at her address.

  The plan says this must not happen: S1's own *Why* (§5.11) and D1.4's *Why* narrow the owner's 91 (a) "so a real account (an owner, **or one recovered after use**) is never taken by a stranger". The criteria S1 lists don't deliver that intent for an account whose use left no footprint. The tests (T29's four footprints) don't cover the case. (The damage is limited: her inbox can later reset the stranger's account, and her old one held nothing but its name. It is still the "used account retired by a stranger" this review was asked to look for.)
- Fix: treat as replaceable only an account **someone else created**, one with a `user.created` audit entry as its entity. The owner's staff add and the admin's owner add both write that entry (`users.createWithTemporaryPassword`, their only caller pair); registration and Google write none. It is one more `EXISTS` in the same read as `hasActed` (inverted), with no migration. Add a T29 case: a self-registered account with an expired, admin-issued temporary password → `EMAIL_TAKEN`. Make security.md say the rule. · Belongs: a fix round on #132 (folded into `748ce34f`). It narrows the approved S1 towards its own stated *Why*, so the owner approves it first; if the owner declines, a finding (224) and security.md's "or one used before" corrected.

### R2-F3 — nit · One new race test runs under Vitest's 5 s default, below the helper's 8 s reach
- Where: `apps/api/src/modules/auth/sessionLock.api.test.ts:95-109` at a12c0790 ("a temporary password that expires between the check and the lock is refused at confirm", T44, added by `d3afe676`).
- Seen in the code: the test races through `whileLocked` → `whileHeld('users', …)`, and the request it waits for hashes a password first. It passes no timeout, so it gets Vitest's 5,000 ms default (`apps/api/vitest.config.ts` sets none). Every other race in the file passes `20_000` or `RACE_TIMEOUT_MS`, and `REACH_MS` is 8,000. `efb0d0d8` (C1.15), the next commit but one, set every race's timeout and missed this one.
- Scenario: on a loaded machine where the request takes 5–8 s to reach the lock, the test fails at its 5 s limit although the race is sound. That is exactly finding 77's defect, and 77's *Resolution* ("the reach (8 s) sits well under the race tests' 20 s") is false for this test.
- Fix: pass `RACE_TIMEOUT_MS` as the third argument. · Belongs: a fix round on #132 (folded into `d3afe676`).

### R2-F4 — nit · An overflow survives M1: a subscription's paid sum is still cast to `integer`
- Where: `apps/api/src/modules/payments/payments.repository.ts:124` at a12c0790 (`SELECT sum(amount_agorot)::integer AS paid FROM payments WHERE subscription_id = …` inside `balancesOf`).
- Seen in the code: M1 made `due` a `bigint`, and `DEBT`, `CREDIT` and `balanceTotals` are `bigint` + `Number()`. A subscription's own paid sum is still `::integer`. A payment is at most 10,000,000 agorot (`PAYMENT_MAX_AGOROT`), and a usage-based subscription may be paid beyond its due (credit).
- Scenario: T51's own subscription: per day at the price bound, 215 days, a due of 2,150,000,000 agorot. Paid in full, it takes 215 payments, and the paid sum passes 2³¹ − 1. Every `balancesOf` read that includes it then raises 22003: the customers list and its `OWES`/`CREDIT` filters, the customer's file, and the space's `balanceTotals`. Each answers 500 for the whole space, which is finding 122's failure on the payments side. The amounts are as unrealistic as 122's own.
- Fix: `sum(amount_agorot)::bigint` there, with `Number()` where `itemBalances` maps `paid` (exact within the bound). · Belongs: a fix round on #132 (folded into `06753d3c`).

## The checklist (lines 1–7, each answered)

**1. Every commit of my range read** (each with `git show <sha>`, the full source diff; the head read where a later commit touched the file):

U1:
- `9284b98d` sessions: successor = HMAC-SHA256 under an HKDF key from `JWT_SECRET`; the grace path answers the stored successor.
- `b046ce99` the sweeps of refresh/reset tokens, recoveries and rate-limit counters (5,000 a table), as two jobs.
- `79aaed8d` `GoogleSession.created`.
- `748ce34f` finding 91: replacement of an expired pending account (S1), `user.replaced`, `space.staffDeactivated` by no one.
- `14bdecc4` the reset email prints its link in both parts and both languages; localisation.md's second home (OD1).
- `958782bb` `MyAccount.hasPassword` and `hasGoogle`, read as counts.
- `6626ad4f` `ALREADY_OWNER` with `details.userId`.
- `a31cb3d0` `GET /admin/users?email=`, exact match.
- `c7fe46c4` one `SPACE_STATUSES` with `editable`; the second schema removed.
- `e620ba83` a deactivation ends sessions only with no other active link.
- `2fad3c23` the re-issue refuses an admin with `ACCOUNT_IS_ADMIN`.
- `1cf7cd7c` `StaffMember.addedAt`.
- `d3afe676` tests T41–T44.
- `ae1e86a8` the contract names `invalid_format` and `invalid_choice` on `spaceId`; T45.
- `efb0d0d8` `waitingOnLock({ on })`, `REACH_MS` 8 s, `RACE_TIMEOUT_MS` 20 s, 41 race files.
- `4908f217` the owners' names test finds its statement.
- `b8fceb03` `namesFor(ids, tx: Tx | undefined)`.

U2 (and lane T's two, and W4's move):
- `bd7e9d0f` the test database's init script inline in Compose (`configs.content`); the SQL file removed.
- `d9e81909` documentation §5's size rule revised (OD4 (b)).
- `06753d3c` **M1** `subscription_usage` due in `bigint`; DEBT, CREDIT and totals `bigint` + `Number()`.
- `0fce0315` T52: PostgreSQL's and Node's Gaza date and minute around 2026's transitions.
- `dab7973e` dated check-ins bounded by two Gaza midnights; T53's `EXPLAIN`.
- `f0240b98` `stalled` and the 500 (R2-F1).
- `3fa5ab42` `storage.list` (local walk, Cloudinary Admin API) and `photos.reclaimOrphans`.
- `37caa0a4` phone matched by national digits without the trunk 0.
- `347e32de` a visit's check-in takes `customerId`.
- `47ccd91d` `published.amountAgorot` and `PUBLISHED_PRICE_CHANGED`.
- `c675195f` `ItemPayment.recordedBy` and `voided.by` with names.
- `1879e0b1` `GET …/written-off-visits`.
- `7e3244f0` **M2** `published_period` with its CHECK; the kind filter's `WEEK`/`MONTH`; `CUSTOM` narrowed.
- `627eeaa6` `CustomerFile.reminderTemplate`.
- `9f801981` `PresentPerson.audience`; `CustomerRow.current` limits and progress.
- `1716f006` one report by id (owner and admin).
- `57851f54` `AdminSpace.retiredAmenities`.
- `108dbff8` web `features/users`: one folder per operation (moves only, the entry's names unchanged).

**2. The plan's decisions for U1 and U2, built as approved:**
- D1.1–D1.17: built. Two adaptations are judged below: LA1-D3, the rate-limit sweep ordered by `reset_at, key` since the table has no id; and LA1-D8, the swept rows documented under *Users and sessions*.
- D1.4 is built exactly to S1's criteria (OD6 (a)). S1's stated purpose is not met for a self-registered account (R2-F2).
- D2.1–D2.15 and M1/M2: built as written. D2.4's rule is the plan's own wording, and it reopens finding 114 (R2-F1).
- M1: I compared the SQL line by line with the original migration `20261021082345_subscription_usage`. The only differences are the return column `due_agorot bigint` and the `::bigint` casts in the `CASE`. FIXED gives `price::bigint`, the same value; PER_DAY multiplies `count(DISTINCT day)`, already `bigint`, by `price::bigint`, the same value; PER_HOUR gives `round(bigint × bigint / 60.0)::bigint`. The numeric rounds half away from zero as before, so normal values are unchanged. The `DROP … (integer, integer, date, date)` signature matches the original. `git grep` finds the function only in these two migrations and no view or function depending on it. Its callers are `subscriptions.repository.ts:570` (`due_agorot: bigint` → `Number()` in the mapper) and `payments.repository.ts:119` (in the `UNION ALL`, `bigint` with a visit's `integer` charge resolves to `bigint`). One cast is left: R2-F4.
- M2: `ADD COLUMN "published_period" "PricePeriod"` is nullable, so existing rows stay `NULL` and the CHECK holds for them. The CHECK reads `IS NULL OR (IN ('WEEK','MONTH') AND package_id IS NULL)`. Only the published branch of the subscribe sets the column (`desk.service.ts`: `published.period`); the package and custom branches set `null`. Nothing else writes it: corrections, renewals (a new subscribe) and closure extensions don't touch it.
- The Prisma schema adds `publishedPeriod PricePeriod? @map("published_period")`. Prisma models neither CHECKs nor functions, so there is no drift; `migrate deploy` ran green in CI's `test:api`.
- No PR number and no `#PRNUM` in either SQL file (`git grep`).

**3. Money, roles, privacy, keys and locks:**
- Money:
  - 171 (a): the compare happens under the space's lock (`lockAtDesk` first), after the idempotency replay. The price is read through `tx`, and the comparison is integer agorot (`shown !== price.amountAgorot`). It answers 409 `PUBLISHED_PRICE_CHANGED`, writing nothing (T64 asserts no subscription, payment or audit). The prices save takes the same lock. The code is in `core/errors.ts`, in both web catalogues and in contract §6.
  - The written-off amount is `charge − paid`, voids left out.
  - M1: R2-F4.
- Roles:
  - `written-off-visits` sits behind `requireCan('visits.writeOff')` (owner only), placed before `validate` and the read.
  - The manage single report sits behind `requireCan('space.dataReports.read')` (admin or owner). Its `findInSpace` is scoped to the space, and the owner's list has no other filter, so the two agree.
  - The admin's report is on the admin router.
  - `ALREADY_OWNER` is raised only on `POST /admin/owners`, so only the admin gets the id.
  - The re-issue now checks `ACCOUNT_IS_ADMIN` before `ACCOUNT_HAS_LINKS`.
- Privacy:
  - `hasPassword`/`hasGoogle` appear only on `/me`, as counts; no hash is read.
  - The space's report never names its reporter (the `REPORT` select).
  - `recordedBy`/`voided.by` names go to staff (162, approved).
  - The reminder template goes to staff (D2.12, approved).
  - The successor key is passed only to `createSessionsService` and is never logged. `JWT_SECRET` is at least 32 characters (`config/env.ts:21`) and the key is 32 bytes.
  - The reset email's link reaches a log only through the development-only `logEmailSender`, which predates this PR.
- Keys:
  - The visit check-in's replay still answers the visit made before any customer check.
  - The subscribe's replay comes before the price compare.
  - No new keyed write.
- Locks and transactions:
  - Finding 91: space lock, then account lock, then a re-check under the lock (`lockReplaceable`). Every read goes through `tx`: `findByEmail`, `findGoogleSubject`, `countOwnerLinks`, `hasActed`, the link, `endSessions`, `setSuspendedAt`, `setEmail`, the audit.
  - 160: under the space's lock, `customers.findIn`, `occupancy.isPresent` and `ratesAt` all go through `tx`; the archive takes the same lock.
  - 92: `countOtherActiveLinks` runs under the space's lock and the person's lock.
  - 99: `retiredAmenitiesNamed` runs in the read's or the save's `tx` (`groupEdit`, `space.service`).
  - The file's `spaceSettings.read` is in its snapshot `tx`.
  - The written-off list and the single reports are lock-free reads, as the contract says.

**4. Planned tests and breaks (T20–T77, B20–B77).** All are present at the head. I read each assertion; every break result comes only from the lanes' reports.
- Weaker or wrong:
  - T54 (and its subscriptions twin) pins the defect of R2-F1: one failing stay → 500.
  - T44 has no race timeout (R2-F3).
  - T29 has no case for a self-registered account (R2-F2).
  - T51 covers an unpaid due only (R2-F4).
  - T60 cannot be turned red by its planned B60, since the old trunk-0 rule already found `+970…` from `+972…`. The lane proved it with B60b; it stays a valid regression guard.
  - T20 proves one successor and no extra row (family count 2) on a sequential replay. The concurrent "two tabs" test doesn't assert that the two successors are the same, but the session lock serialises them, so T20 stands for both.
- Would fail if the behaviour regressed, by my reading:
  - identity, staff and owners: T20–T43, T45–T49;
  - migrations, desk and money: T50, T52, T53, T56–T59, T61–T77.

**5. Screens:** none in my range. These are API commits; `108dbff8` only moves files, and the web fixtures only gain typed fields (`addedAt`, `retiredAmenities`, the desk's).

**6. Findings my range closes**, each against its *Resolves when*:
- Built as it says: 17, 21, 48, 63, 69, 78, 79, 82, 92, 93, 98 (OD4 (b)), 120, 126, 127.
- 77: built, except for one test (R2-F3).
- 91: built to S1, but S1's purpose has a gap (R2-F2).
- 121: built as D2.4 worded it, but it reopens 114 (R2-F1).
- 122: built; one cast left (R2-F4).
- API halves built as their decisions say: 32 (D1.3), 83 (D1.7), 89 (D1.8), 99 (D2.15), 106 (D1.10), 158 (D1.17), 160 (D2.7), 162 (D2.9), 164 (D2.10), 171 (D2.8). Their web halves belong to the other reviewers.

**7. Documents my range changes:**
- Read and true to the code: contract (*Session/register/google*, *Me*, *Staff*, *Owners*, *Users*, *Spaces › status/retiredAmenities*, *Customers*, *Subscriptions*, *Front desk*, *Data reports*, *Internal*, §6), security.md *Tokens and cookies* and *Rate limits*, data-model.md (*Amount due* `bigint`, the published period, the swept rows), conventions §12 (`list`), the features' lines for auth, users, space-links, audit, visits, payments, subscriptions, spaces, data-reports, localisation.md (OD1), setup.md (*Database*, *Running a second folder*), documentation.md §5, and each closed finding's *Resolution*.
- Not true: security.md:53's "or one used before" (R2-F2); contract:1136 "one bad stay never turns every call red" and finding 121's *Resolution* (R2-F1); finding 77's *Resolution* for one test (R2-F3).
- One home per fact is kept: the replacement rule lives in security.md *Passwords*, with users.md and auth.md linking to it.
- `#132` is in every dated line; no `#PRNUM` anywhere (`git grep` empty).

## Decisions taken without the owner in my range, judged
- **LA1-D1** (light checks per commit, whole ones at intervals): acceptable. CI and the lead's final run are green.
- **LA1-D2** (`successorKeyOf` in `tokens.ts`, derived in `createApi`, `successorKey` required, so `users`' `sessions` becomes required): sound. No default service can be built without the key.
- **LA1-D3** (EC2: `rate_limits` has no id, so it sweeps ordered by `reset_at, key`, `LIMIT 5,000`, re-checking `reset_at` on the deleted row): sound. The earliest-ended rows go first, and a key hit at that moment keeps its window.
- **LA1-D4** (the `hasActed` port, wired in `app.ts` to the audit read model): sound layering. Auth doesn't import the read model, and the read is one statement in `tx`. Its criteria are R2-F2's subject.
- **LA1-D5** (`users` judges its half of S1 and re-reads under the lock; auth orchestrates the locks in conventions §13 order; register reads the holder before the insert): sound. A racing registration still meets the unique key and answers `EMAIL_TAKEN`.
- **LA1-D6** (the web's `LIST_STATUSES` narrowed until D6.4): acceptable as a step. I didn't check D6.4's head state (R-web's).
- **LA1-D7** (T46 as an API test): sound. What it measures is PostgreSQL's own view.
- **LA1-D8** (the swept rows under data-model's *Users and sessions*, not *Operations*): acceptable. It is the rows' own home.
- **LA1-D9** (T49 "the four others"; B40 uses the read's time because `updatedAt` isn't selected): acceptable.
- **LA1-D10** (`addedAt` required, eight web fixtures updated): sound.
- **LA2-D1** (DEBT, CREDIT and totals `bigint` + `Number()`): sound, but incomplete: R2-F4.
- **LA2-D2** (the written-off list lives in `payments`, since `visits`, a level below, may not read payments): sound.
- **LA2-D3** (`JobDone` as `Record<string, number | boolean>`; `JobsRun.stalled`): the types are fine. The rule they carry is the plan's and is wrong (R2-F1).
- **LA2-D4** (reclaim at most 200 a run, ten at once): sound. Only files `spaces/{k}/*.webp` with no row holding `{k}` in any space, deleted spaces included, and older than an hour are removed. Uploads store the files before the row, and only photos write to storage, so a referenced photo or a file mid-upload is never removed. OD11 holds.
- **LA2-D5** (`customerId` in `visit.checkedIn` only for a customer's visit): sound.
- **LA2-D6** (`publishedPeriod` on the desk's answers, not in the created audit): acceptable. The audit's `after` still names the price and terms.
- **LA2-D7** (the file reads `spaceSettings.read` in its snapshot): sound. A space without its settings row already fails elsewhere at the desk.
- **LA2-D8** (retired amenities named by `lookups`, the view now async and taking `tx`): sound.
- **LA2-D9** (the admin's single report is `not_found` for a soft-deleted space): sound, the same rule as the list.
- **LA2-D10** (T52 compares date and minute): sound, and stronger than planned.
- **LA2-D11** (per-commit eslint and tsc): acceptable.
- **The lead's A2 join** (a semantic conflict in T54's job list fixed inside the stall commit by an edit stop): acceptable. The commit's tree is coherent at the head.
- **LEAD-D12 / LT** for `bd7e9d0f` (the container's one-time recreation left to the owner, `main`'s file kept untracked for the run): acceptable. The container is shared with worker B, and setup.md and the PR description name the one-time `db:up`.
- **§11's write cases not performed** (R19–R24 and the API halves of R22, R30, R32–R35): acceptable for the API only. Each behaviour has an API test: T61–T68 and T64/T65 for 171's 409. The browser-side 409 line is a web reviewer's.

## Outside my range
None noticed. I read web and U0 code only where my commits' fixtures or the error envelope touched it.

## Not checked, and why
- Nothing run: no tests, no breaks, no SQL against a database; the prompt forbids it. Break results are taken from `lane-a1/REPORT.md` and `lane-a2/REPORT.md`.
- The timeouts of the other 40 race files that `efb0d0d8` re-indented were not checked one by one. My scan script was refused by the tool's sandbox, so I read `sessionLock.api.test.ts` and the helper whole. `git log -G` shows no U2 commit touching the race helpers. Typecheck, green in CI, proves every race names its table (`on` is required).
- Cloudinary's real Admin API listing (EC8): only the mocked `fetch` (T57) and the URL and paging shape were read.
- The demo seed was read only for published-price subscriptions (none; it sells packages) and for photos (made through the photos service, keys `spaces/{k}/…`).
- `d9e81909` and `bd7e9d0f` were checked as text against their findings (98, 48); `docker compose config` was not run (lane T's report records it).
- The web halves of 32, 83, 89, 99, 106, 158, 160, 162, 164 and 171 belong to the web reviewers.
