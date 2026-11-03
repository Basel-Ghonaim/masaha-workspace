# Review of #131 — R1: the foundation and the items left — Claude Code
Head: c41a5397 · range origin/main..6d563549 (8 commits) · checks: green (build, lint, typecheck, format:check, check:classes, check:conflicts, check:links, test:unit, test:api, test:component pass; CodeRabbit skipping) · head moved during the review: no (c41a5397 at the start and at the end, CLEAN)
Verdict for my range: mergeable (three nits, each a fold into its commit if a fix round runs anyway)

Read from `C:\dev\masaha\app-design`, commit objects only (`git show`/`git grep` pinned to `6d563549`, the range's commits and `c41a5397`). Later commits touching my range's files: `a05891e4` (finance), `447be920` and `57fa7992` (the overviews' counts) change `payments.repository.ts`/`data-reports.repository.ts`, so those I read at the head. No test was run (the rules say not to): "would it fail" below is from reading the test against the code, and the reds are **only in a report** (4_REPORT_LEAD.md, `scripts\lane-l\REPORT.md`).

## Findings (verified defects only, most severe first)

### R1-F1 — nit · `visits.service.ts`: the new `page` split `terms`'s doc comment off from `terms`
- Where: `apps/api/src/modules/visits/visits.service.ts:247-258` at c41a5397
- Seen in the code: `page` and its JSDoc were inserted between `terms`'s JSDoc ("The desk's terms for the caller: the rounding and the cap in force…", 247–251) and `async terms(`. So `page` now has two stacked doc comments, the first describing `terms`, and `terms` has none.
- Scenario: a reader or the editor hovering `page` sees the desk's terms first. `terms` shows no documentation.
- Fix: move lines 247–251 down so they sit directly above `async terms(`. · Belongs: a fix round on #131 (folded into `6d563549`)

### R1-F2 — nit · `payments.md` *Who uses it*: the desk's web sentences now sit under Finance, and the desk bullet still says the overview "will count"
- Where: `docs/features/payments.md:22-23` at c41a5397
- Seen in the code: `5f867d86` moved "On the web, the desk's screen lists the uncollected visits and records a payment on one (#117); «استلام دفعة» records a payment… (#119)" out of the **front desk** bullet. They now end the **Finance / the owner's overview** bullet, which is not what those sentences are about. Line 22 still ends "the uncollected visits, which the owner's «يحتاج انتباهك» will count". That is false at the head: `a12f928e` built the count, and line 23 says so.
- Scenario: a reader of the capability document is told that Finance's bullet covers the desk's screen, and that the overview's count is still to come.
- Fix: put the two web sentences back at the end of the front desk bullet, and make "will count" "counts" (or drop it, since line 23 says it). · Belongs: a fix round on #131 (the move folded into `5f867d86`; "will count" into `a12f928e`, R3's commit)

### R1-F3 — nit · `.env.example` still describes the seed's WhatsApp as any E.164 number
- Where: `apps/api/.env.example:33` at c41a5397
- Seen in the code: "WhatsApp in E.164, for example +970599000000." Since `62d76b81`, `seedEnvSchema` reads it through `phoneSchema`. That schema accepts only a Palestinian or Israeli number, and accepts it in any typed form (`059…`, `00970…`), not only E.164.
- Scenario: a developer sets `SEED_CONTACT_WHATSAPP=+201001234567`, which is valid by the comment, and `npm run db:seed` stops with "SEED_CONTACT_WHATSAPP: Not a Palestinian or Israeli phone number". The failure is clear; only the guidance is stale.
- Fix: "WhatsApp: a Palestinian or Israeli number, stored in its E.164 form, for example +970599000000." · Belongs: a fix round on #131 (folded into `62d76b81`)

## The plan's tests and breaks for my range (one line each: present / missing / weaker; would it fail?)
- T-L1 `publicContact.api.test.ts` "a contact stored in another form is answered as stored, to anyone and to the admin": present; both the public and the admin read are asserted as stored. It would fail if the read went through `phoneSchema` (B-L1 red only in a report).
- T-L2 `adminSettings.api.test.ts` "saving a contact stored in another form stores its one form, audited…": present; it asserts the exact `before`/`after` and the stored rows. It would fail on a normalised comparison (no write, no entry).
- T-L3: **weaker in form, by LEAD-D1**. It is a unit test of `seedEnvSchema` (`seedEnv.unit.test.ts`, 3 tests: normalised, empty left unset, foreign number naming its variable), not the plan's `seed.api.test.ts`. It would fail if `seedEnv.ts` went back to the regex. Nothing tests that `run.ts` uses `seedEnvSchema`; I saw that it does (`run.ts:16`).
- T-P1 `totals.api.test.ts` page order, paging, `total` past the last page, the oldest owing item (an earlier fully paid visit skipped; a later subscription not chosen): present; it would fail on ordering by customer id. Also covered: the tie broken by id, `CREDIT` with `oldest: null`, the empty space.
- T-P2 totals: present. It includes a credit beside a debt on one customer, an archived debtor, a written-off visit, an unpriced visit, a voided payment's visit owed again and another space's debt. It would fail on netting or on dropping the archived.
- T-P3 uncollected totals: present, compared to `uncollectedPage`'s total. The fixture holds the settled, written-off, customer's-hand-closed and another space's visits. It would fail with `written_off_at IS NULL` dropped.
- T-L5 `idle.api.test.ts` race: present and real. `whileHeld` waits until the request is blocked on a lock (`waitingOnLock`, failing after 4 s otherwise). The test asserts the race happened: the two rows end with different `last_activity_at`. With the 15-minute idle bound, the refresh at minute 20 is idle if it reads the newest row (0) and live if it reads the max (10). The test also asserts the new row carries 10, then a request at 20 is 200. So it would fail on both B-L5 (the newest row) and a rotation that copied `stored.lastActivityAt`.
- T-L6 `me.api.test.ts` "a user reads their own account": present, with `?userId=`/`?id=` of another user ignored (B-L6).
- T-L7 edit, audit only what changed, no change writes nothing: present. `{}`, the same name, and the same name and language each write nothing; the row is compared whole; the other user is untouched (B-L7).
- T-L8 guard: present, as 401 for a guest and a suspended account and 403 `PASSWORD_CHANGE_REQUIRED` for a pending one (the plan said suspended 403; see the decisions). Not tested: a `PATCH` carrying `role`/`email`/`password`. I checked by reading that it cannot write them: `validate` replaces the body with the parsed value (unknown keys stripped), and `editMyAccount` builds `after` from `name` and `language` only.
- T-L9 `adminReports.api.test.ts` `handledBy`: present. It covers both sides, with status, field, `spaceId` (the spread defect the lane caught) and paging, and `422 invalid_choice` (B-L9).
- T-L10 `visitsList.api.test.ts` range by Gaza days: present. Visits sit on both sides of two Gaza midnights; open and closed; a same-instant tie by id; page 2 (B-L10 by UTC days would fail).
- T-L11 reception today only; a range refused: present. Two ranges, `today..today` included, are each 403 (B-L11).
- T-L12 another space never; a stranger, another owner and the admin 404: present (B-L12).
- Added beyond the plan: the visits query's refusals (half a range, backwards, over 92 days, an invalid date; exactly 92 days accepted); the `/me` 422s; `platformEvents.unit.test.ts` keeps `user.profileEdited` off the admin's log.

## Decisions taken without the owner in my range, judged
- **LEAD-D1** (EC7 failed: the seed's environment schema in `seedEnv.ts`, with a unit test): **sound**. `run.ts` seeds on import, so it cannot be imported by a test; the file is the smallest seam, and `run.ts` is a three-line consumer.
- **LEAD-D3** (`handledByWhere`'s exact text given to two lanes): **sound**. At the head there is one helper (`data-reports.repository.ts:68`), used by `openCounts` (159–160) and `pageAll` (192).
- **C4's `uncollectedOf(spaceId)` as a function, not the plan's "one `const`"**: **sound**, because the fragment needs `spaceId`. `uncollectedPage` and `uncollectedTotals` both read it.
- **C4's count "apart only past the last page"**: **sound**. `count(*) OVER ()` is computed after `HAVING` and before `LIMIT`. An empty page at `skip = 0` is a true 0, and only `skip > 0` with no rows runs `countOwing` (same `HAVING`, same `tx`).
- **Lane L (1) the rotation reads `familyActivity` for its idle check and copies it**: **sound**. It is what D32 needs: without it the refresh is the request that ends the session.
- **Lane L (2) `PATCH /me {}` → 200, writing nothing**: **acceptable**. It departs from D33's "at least one (`required`)", but with a reason I checked. Every other partial body in the contract ("what is absent is kept": a customer, a price, the settings, an announcement, the lookups, a profile) has no at-least-one rule, and the contract states this behaviour (`api-contract.md:174`).
- **Lane L (3) a suspended account 401, not T-L8's 403**: **sound**. It is the guard's rule and the contract's, and `/me` adds no guard of its own.
- **Lane L (4) `AND: [handledByWhere(…)]`**: **sound**. A spread would replace `spaceId`; the test pins it.
- **Lane L (5) `REPORT_HANDLERS` exported**: **sound**. It sits beside the other report constants.
- **Lane L (6) findings 161 and 167 *Resolved* with "the screen is the web's"**: **acceptable**. The plan (D34; C14 in §8.1) says resolve them. But each finding's own *Resolves when* also names the screen (the desk's log tab; the admin's filter), and no open item now tracks those two screens. Worker A's next screens must take them from the resolution lines.
- **Lane L (7) the visits range by `can(actor, 'payments.read')`**: **sound**. `payments.read` is `'owner'` (`can.ts:82`), so the owner reads any range and reception only today, refused after validation as on the payments list. There is no new action and no `can.ts` change.
- **Lane L (8) EC13 in part: a local `daysWindow` and `VISITS_RANGE_MAX_DAYS = 92`**: **acceptable**. The levels forbid importing `payments`' window into `visits`, in the API and in the shared package. The cost is a second copy of the Gaza-midnight window and of the 92, which may drift. Both are stated in `visits.md` and the shared constant's comment.

## Outside my range
- `api-contract.md:726` (Finance › debts, `71a18c1b`, R2's) says "A walk-in's uncollected visit is no customer's debt: it is counted apart". But a visit left to a customer "stays uncollected… and counts in that customer's debt" (`:667`), and `balancesOf` plus `uncollectedOf` both include it. So `meta.totals.owed.agorot` and `meta.totals.uncollected.owedAgorot` can hold the same agorot, and a screen summing them would count it twice. The totals functions follow the existing rules. It is the sentence that implies the two figures are disjoint. Plausible doc should-fix for R2.
- `payments.md:22`'s "will count" (part of R1-F2) was made false by `a12f928e` (R3's).

## Checked and fine
- **The payments totals (money).**
  - Every figure reads `balancesOf` unchanged (EC3 held). Voided payments are left out in both `LATERAL` sums and in `uncollectedOf`. Written-off visits owe nothing (the visits branch `written_off_at IS NULL`; `uncollectedOf` the same), as the contract says. An unpriced visit owes nothing (`greatest(NULL − paid, 0)` → 0; `oldest` needs `due − paid > 0`). An archived customer is kept (no customer filter).
  - Set-based: one statement per figure, with `customerIds = null` over the whole space, so no N+1. `countOwing` runs only past the last page.
  - `tx` is taken by all three, through the service to the repository. Finance passes its snapshot's `tx` (`finance.service.ts:156-158`); the overview passes none (S21, as planned).
  - Each total equals the sum of its list: `owed.agorot` is the sum of `DEBT` per customer (≥ 0), `owed.customers` is the page's `HAVING DEBT > 0` count, and the same holds for credit. `uncollected.visits` equals `uncollectedPage`'s total.
  - The `oldest` order is `created_at`, then visit first, then id.
- **Finding 170.** `familyActivity` is `aggregate _max(lastActivityAt)` over the family. `rotate` checks idleness against it (falling back to the stored row) and issues the new token with it. `idleState` (`sessions.service.ts:195`) reads the same function. `renewActivity`'s per-row `lt unlessAfter` still renews the rows below the max. The unit test's fake gained `familyActivity`.
- **`/me`.**
  - Both routes sit in the existing `me` router behind `requireAuth()`. The user id comes from `signedIn(req)` only, never from the query or body.
  - The body is `updateMeSchema`, the shared schema: `textSchema(1, NAME_MAX_LENGTH)`, the same rule as registration (`auth/requests.ts:9`), and `z.enum(LANGUAGES)`, `.partial()`. Unknown keys are stripped by `validate`, and the service writes only the changed `name`/`language`.
  - The edit takes the account's lock, then `setProfile`, then one `user.profileEdited` entry with only the changed fields and no space. The action is in `AUDIT_ACTIONS` and kept off `PLATFORM_ACCOUNT_ACTIONS` by default deny, as D33 and EC12 say. `MyAccount` holds `{ id, name, email, language, role }`.
- **`GET …/visits`.** It is mounted in `visits`' manage router, inside `requireSpaceAccess`, so a stranger, another owner and the admin get 404. The query is validated first (`visitsQuerySchema`): both ends or neither, `to ≥ from`, at most 92 days with both counted. A range from anyone but the owner is a 403, refused, not narrowed. The window runs from Gaza midnight to the Gaza midnight after the last day (`gazaInstant`, `addDays`). The read filters on `spaceId` over `checkedInAt`, newest first then id, with `count` paging, on the `(space_id, checked_in_at)` index. The rows are `DeskVisit`, which the desk already shows reception for the day. No other `GET /visits` route collides.
- **Finding 167.** `handledBy` resolves to `spaceId notIn/in verifiedSpaceIds()`. That is the active-OWNER-link rule `space-links` answers (`space-links.repository.ts:42`). It is the same rule as each row's `space.verified` (`data-reports.service.ts:80-90`) and as the admin's decision authority (`can()` with the links under the space's lock, `data-reports.service.ts:228`). The ids are read only when the filter is given. `notIn: []` keeps every report.
- **#130's fixes and finding 153.**
  - The seed's contact goes through `emailSchema`/`phoneSchema`, and `run.ts` passes `parsed.data` to `seed()`. `seed.ts:40-41` stores what it is given, so it is normalised now.
  - The stored-form round trip is pinned (T-L1, T-L2). The contract has F1's sentence and F4's "changes no value" (`api-contract.md` *Platform settings*). In `platform-settings.md`, F3 drops "in the browser too", and F4 is applied at lines 11 and 51.
  - Finding 153's *Evidence* has F2's wording and the foreign-number case.
- **Documents.**
  - The contract's *Me*, *Front desk (managed)* › `GET …/visits` and *Data reports* › `handledBy` match the code.
  - `payments.md` (apart from R1-F2), `users.md`, `visits.md`, `data-reports.md` and conventions §9 *Composed reads* (R11's "how many owe, a count") match too.
  - Findings 97, 153, 161, 167 and 170 are each *Resolved* with a *Resolution* line, under *Resolved* in the index at the head and absent from *Open*. 167 is also off `data-reports.md`'s *Open findings*.
  - Finding 97's resolution matches `packages/shared/src/space-settings/requests.ts:50-66`.

## Not checked, and why
- No test, break, lint or build was run (read-only rules). Each red is **only in a report**. I judged from the code whether each test would fail.
- EC4's timings (no statement over 150 ms) and the real run's R11–R13: **only in a report**. No database or server was touched.
- The finance, overview and C16 commits (R2's and R3's ranges), except where my range's functions are called from them (`finance.service.ts:156-158`, `ownerOverview.ts:59-62`) and the docs those commits changed in my files.
