# Review — DESK PR 3 (#97, `feat/auto-checkout`)

**Head:** `e122b95d39479a3a58bfdebe6ae1a6002acc87ff` · base `origin/main` `c91f5b42` · `gh pr checks 97` all
pass (lint, format:check, typecheck, test:unit, test:component, check:classes, check:links, build, test:api) ·
`CLEAN` · the head was the same at the start and the end of the review.

**Verdict:** no blocker. Mergeable as it is. Two should-fix items in the code and documents, and one in the
process, are small enough for DESK PR 4's first commit. Nothing needs a fix round on this PR.

**Method:** I read only commit objects: `git diff origin/main...e122b95d`, `git show e122b95d:<file>`, the five
commit messages and the PR description. I ran no tests, builds or servers. Wherever this report says "seen", I read
it in the code. The red-first runs, the 22 breaks, the timer check and the real run on 3321 come **only from
`4_REPORT_PR3.md`**; I did not re-run any of them.

---

## The five most important findings

### 1. should-fix — one stay that keeps failing blocks every later stay, and the skip for a space without settings never runs
- **Where:** `apps/api/src/modules/visits/visits.service.ts`, `autoCheckOut`: the `for … of due.slice(0, 500)` loop
  has no `try` around each `runInTransaction`. The same holds for `subscriptions.service.ts`'s `autoCheckOut`.
  Also `if (!rules) return [];` in both, after `spaceSettings.settingsFor(spaceIds)`.
- **Seen:** `settingsFor` maps every id through `present(spaceId, rows.get(spaceId) ?? null)`, which throws for a
  missing row. So `settings.get(...)` never returns `undefined`, and the `!rules` skip cannot run. T4 depends on
  exactly this: it deletes one space's settings row, and the whole `visits.autoCheckOut` fails, for every space.
- **Failing scenario:** the open stays are read oldest first, so the order is fixed. Suppose one stay fails on
  every run (a space without its settings row, or any row the update refuses). Every run then throws at that stay
  or before the loop. No later visit on the platform is ever closed, and every cron call answers 500 until someone
  fixes the data by hand. Each closing is committed on its own, so nothing is *undone*. But the plan's D-PR3-2 aim,
  "one failure must not undo the others", stops at the job level. A single bad stay or space halts that job
  everywhere.
- **Plausible, not proven:** I found no reachable cause today. Every space is created with its settings row, and
  the closing respects `visits_checked_out_at_check` (`>=`) and the charge checks.
- **Fix:** in each job, catch per stay: log `{ err, job, stayId }`, count it (`failed`), go on with the next one.
  Make the run fail (500) when `failed > 0`. Either let `settingsFor` skip an absent row so the `!rules` branch
  is real, or delete the branch. Add one test with two stays, the first made to fail.
- **Where its fix belongs:** DESK PR 4's first commit (small: two loops and one test).

### 2. should-fix — "a stay never crosses into the next day" is not what the code does
- **Where:** `docs/architecture/data-model.md` › *Auto check-out* ("a stay never crosses into the next day, nor
  is it due before its check-in"); the comment on `LAST_MINUTE` in `apps/api/src/modules/spaces/autoCheckout.ts`
  ("a stay never crosses into the next"); the executor's reason for leaving #95's nit 9 ("PR 3's auto check-out
  bounds the stay to one Gaza day").
- **Seen:** `autoCheckoutDue` limits only the **closing** branch to the check-in's day. The stay-limit branch is
  `checkedInAt + maxStayMinutes`, and `updateSpaceSettingsSchema` allows up to 1,380 minutes (23 h).
- **Failing scenario:**
  - Closing check-out off, stay limit 23 h, check-in at 20:00: the stay is due at 19:00 the **next** day. It
    crosses midnight and is charged over it (the cap is one day price).
  - Closing check-out off and no stay limit: `null`, and the stay is never closed. So nit 9's overflow (a stay of
    about 215 h at an absurd hour price) is still reachable. The reason given for leaving nit 9 is false.
- **Fix:** the owner chooses one of these:
  - (a) the documentation follows the code: the closing is the check-in day's; the stay limit alone may cross
    midnight; with both off, no auto check-out;
  - (b) the code follows the documentation: the stay limit's due time is also capped at 23:59 of the check-in's
    Gaza day (one `Math.min`, one unit test).

  Either way, the comment is corrected and nit 9 is re-recorded with a true reason.
- **Where its fix belongs:** DESK PR 4's first commit, once the owner has chosen.

### 3. should-fix (process) — nits 7 and 8 were judged "not small" without stopping to ask, and nit 8 is now recorded nowhere
- **Where:** `0_CARRIED_FROM_95.md` item 4 says: "any the executor judges not small → stop and ask". The executor's
  report (C0) leaves nit 7 ("not small") and nit 8 ("a rule change, the owner's") undone, without asking.
- **Seen:** nit 8 is not in the findings index, in finding 100, or in a document of this diff. The report says
  `OPEN_DECISIONS.md` was edited only for points 1 and 4. I have not read that file; that part is from the report.
  Nit 8 is real: a key that closed a visit with no payment is not remembered, so the key can be reused on another
  visit and its true retry then gets `conflict`. It now lives only in #95's review file.
- **My view of the four:**
  - Nit 7 (one helper for *present*, in `occupancy`): fine to leave, but the owner should hear that it was left.
  - Nit 8: should have been asked about.
  - Nit 9: see finding 2.
  - Nit 10: rightly left.
- **Fix:** record nit 8, and nit 7 if the owner wants it kept, as findings. The owner assigns the numbers, since
  worker A now holds 101 and up. Or the owner decides nit 8 now, for PR 4.
- **Where its fix belongs:** a finding to record (the owner's call). A fix, if chosen, goes in PR 4's first commit.

### 4. nit — `visits.md`'s boundary contradicts itself and the code
- **Where:** `docs/features/visits.md` › *Responsibility boundary*.
- **Seen:** *Asks* says `visits` asks `prices.typeByHand` "under the space's lock (`spaces.lock`), for pricing an
  unpriced visit". The next line, *Leaves*, gives "the transaction, the space's lock, and the decision under it of
  who may type a price to `desk`". The code disagrees:
  - `visits.price` takes `spaces.lock` and decides `can()` itself;
  - `visits.autoCheckOut` runs its own transactions (`runInTransaction` is now a dependency).
- **Fix:** *Leaves* should say "the check-out's transaction, the space's lock and the check-out's typed-price
  decision to `desk`". *Owns* or *How it composes* should say that `visits` runs its own transactions for the auto
  check-out and the pricing.
- **Where its fix belongs:** DESK PR 4's first commit.

### 5. nit — the scheduler's local fact is in two homes, and `.env.example` suggests the timer depends on the secret
- **Where:** `docs/backend/conventions.md` §12, the *Scheduler* row; `apps/api/.env.example`'s `JOBS_SECRET`
  comment.
- **Seen:** the row's **Online** cell ends "…; locally, `server.ts` runs the same jobs every 5 minutes, the first
  10 s after start". That fact belongs to the **Locally** cell, which already says it. `.env.example` says "Empty
  locally: the endpoint is then not mounted, and the API runs the jobs itself", which reads as if the API stops
  running them once `JOBS_SECRET` is set. In fact `server.ts` always passes `startJobs`, so locally with the secret
  set, both the timer and the endpoint run. That is harmless: each row is locked and checked as still open.
- **Fix:** move the 5-minute and 10-second detail into the Locally cell. Reword the comment to "The API's own
  server runs the jobs every 5 minutes either way; without it, the endpoint is not mounted".
- **Where its fix belongs:** DESK PR 4's first commit.

---

## The rest

### 6. nit — the scheme's case
- **Where:** `apps/api/src/shared/jobs/secret.ts`.
- **Seen:** `matchesSecret` compares the whole header with `Bearer <secret>`, case and all. `readAccessToken`
  (`requireAuth.ts:44`) accepts the scheme in any case (`/i`), as RFC 7235 allows. A cron service set up with
  `bearer …` gets 401. The runbook spells `Bearer`, so this only bites a hand-typed setup.
- **Fix:** none needed, or say in setup's runbook that the header must be written exactly.
- **Where its fix belongs:** record or ignore.

### 7. nit (plausible, scale) — the uncollected read grows with every auto-closed visit ever
- **Where:** `payments.service.ts` `uncollectedIn`, `visits.repository.ts` `autoClosedIn` and `autoClosedPage`
  (`id: { notIn: [...] }`).
- **Seen:** every request reads every `AUTO` visit of the space ever, sums all their payments, and sends every
  settled id as bound parameters. The list only grows. At some tens of thousands of settled auto-closed visits in
  one space, the statement nears PostgreSQL's 65,535 bind parameters and the read answers 500. Long before that,
  it is slow. The plan put this down as "fine at v1's scale".
- **Fix (later):** filter in SQL, either with one `LEFT JOIN` / `HAVING` over non-voided payments in a raw query
  owned by `payments`, or by limiting the read to visits not yet settled through a stored flag. Either is an
  architecture choice for the owner.
- **Where its fix belongs:** a finding to record.

### 8. nit (plausible) — v1-mvp says "The step's API is built"
- **Where:** `docs/plans/v1-mvp.md` step 7 *Built*.
- **Seen:** the owner's approval note (A3) puts DESK PR 4, collecting an uncollected visit and writing one off,
  in this item, before the desk's screen. Step 7's goal names "uncollected visits" without saying whether
  collecting them is step 7's or step 9's. If PR 4 counts as step 7, the sentence is premature.
- **Fix:** PR 4 rewords it when it lands, or now: "…; collecting and writing off an uncollected visit remain
  (DESK PR 4)".
- **Where its fix belongs:** DESK PR 4 (its own documents).

---

## Departures, judged
- **The job registered as two** (`visits.autoCheckOut`, `subscriptions.autoCheckOut`): right. T4 needs one
  module's failure to leave the other's closings done. The contract's *Internal* names both, and the 200 answer
  carries both. Seen.
- **Moving `priceVisitSchema` to `visits`, reused by the check-out's `charge`:** right. The typed price's rule
  has one home. `CHARGE_REASON_MAX_LENGTH` moved with it, and `desk/requests.ts` now imports it. Seen. The bound
  is `PRICE_MAX_AGOROT`, the same 10,000,000 as before.
- **The pricing route's `requireCan('attendance.record')`:** right. `prices.typeByHand` needs the switch, which
  `requireCan` cannot read. The service asks `attendance.record` again and then `prices.typeByHand` on the links
  under the lock (`visits.service.ts` `price`). Seen. B18 (`can()` on `space.links`) is from the report only.
- **The reworded breaks:**
  - B10 as two edits: right. The open read never returns a closed visit, so the one-edit break could not fail.
  - B11 as "the stay limit not read at the run": right. No setting is stored on a visit.
  - B2's unit form: acceptable.

  All three are from the report; I could not see them in commits.
- **C3's subject changed** from the plan's "close a visit unpriced": right under A1. The close is #95's.
- **`test:api` not re-run after the rebase on #96:** acceptable. CI ran `test:api` green on this head.
- **The §12.2 check 2 timer check done by a script instead of Ctrl-C:** acceptable. From the report only. The code
  `unref`s both timers (`timer.ts`), seen.

## Checked and fine (seen in the code unless marked)
- **The secret:**
  - `timingSafeEqual` on the SHA-256 digests of the header and `Bearer <secret>`, so the lengths always match;
    `undefined` → false.
  - A missing or wrong secret → `AppError.unauthorized()` before `jobs.run()`. The envelope carries no code and
    reveals nothing. The 500 says only "A timed job failed".
  - Mounted only when set; `/internal/jobs` is mounted after the general limiter.
  - `readAccessToken` fails on the secret, so the call counts as a guest by address.
  - `JOBS_SECRET` is at least 32 characters when set and is on the production list (`env.ts`); U10 covers both.
  - The secret is never logged: the logged errors carry `err` and `job` only, and `authorization` is redacted.
- **The timer:** first run at 10 s, a tick skipped while one is in flight, both handles `unref`'d, the failure
  logged.
- **Due time, not run time:**
  - `closeAuto` writes `checkedOutAt: dueAt`, and the charge is `chargeOf({ from: checkedInAt, to: dueAt })`.
  - T5 at 18:04 → closed and charged at 18:00. T7 catches up two days, each stay at its own closing.
- **The due-time rules** (U1–U8):
  - a closed day or after closing → 23:59;
  - a 0–1440 day → 23:59;
  - never before the check-in (`Math.max`);
  - the earlier of closing and the stay limit;
  - the daylight-saving day on the new offset, read in Gaza's zone through `gazaClockOf` and `gazaInstant`.
- **Idempotent, and losing races properly:**
  - `lockOpen` is `FOR UPDATE … AND checked_out_at IS NULL`, re-checked after the wait, so a desk check-out that
    commits first wins. T12 covers it.
  - A second run closes and audits nothing (T6).
  - The lock order cannot deadlock: the job takes only the row; the desk and the pricing take the space, then
    the row.
- **Settings changed between check-in and the run:** read at the run. T9: a limit set later closes the stay at its
  past due time. Soft-deleted spaces' hours and settings are read too (`weeksFor` has no deletion filter).
- **Subscriptions:** check-ins are closed the same way, audited `checkIn.autoCheckedOut` with no actor (T11).
- **Pricing an unpriced visit:**
  - the space's lock, the links under it, `attendance.record`, then `prices.typeByHand` with the switch;
  - the visit `FOR UPDATE` and the space's own: 404 otherwise; open → 409 with no code; charged → 409
    `VISIT_ALREADY_PRICED`;
  - the rounding fields cleared, `chargeSetById` and `chargeReason` set (they satisfy `visits_charge_set_by_check`
    and `visits_charge_reason_check`);
  - audited `visit.priced`;
  - the reason is required by `priceVisitSchema`, 1–200 characters after trimming.
- **The uncollected visits:**
  - `AUTO`-closed visits only;
  - voided payments excluded (`voidedAt: null`);
  - settled ones (balance ≤ 0, by `balance.ts`) excluded **before** the page is cut, so pages are full and the
    total is right;
  - unpriced visits always listed, with `balanceAgorot: null`;
  - scoped by `spaceId` in every query;
  - staff only, through the boundary (T27);
  - composed as conventions §5 and §9 now say.
- **The carried commit:**
  - `checkedOutAt < locked.checkedInAt` → 422 `out_of_range` before any write, and only for an open visit;
  - a closed visit with no payment of this key and a request carrying `payment` → 409 `VISIT_ALREADY_CLOSED`;
  - a request with no payment, or `payment: null`, still answers 200 as before;
  - the race test now expects `[200, 409]` and one payment;
  - finding 100 filed and indexed;
  - `security.md`'s sentence ("its own `can()` action, owner-only or the staff's") and the contract's
    `roundingRule` comment are corrected.
- **The error codes:** `VISIT_ALREADY_PRICED` and `VISIT_ALREADY_CLOSED` are in `core/errors.ts`, both catalogues
  and contract §6. The Arabic for `VISIT_ALREADY_CLOSED` is listed in the PR description for the owner's approval.
- **Scope:**
  - `apps/api`, `packages/shared`, `docs`, and the two `errors.ts` catalogues only;
  - no `package.json`, lock file or `prisma/` change;
  - nothing on the *Not in v1* list.
- **The commits:** five, subjects of 49, 45, 42, 37 and 39 characters, Conventional Commits, each body saying why,
  no tool attribution, the carried commit first.
- **The documents:**
  - the contract's *Internal*, the three new routes, `UncollectedVisit` and §6;
  - security's *HTTP hardening*;
  - setup's *Timed jobs* runbook, as the plan's O2 wrote it;
  - the data model's *Auto check-out*, *Unpriced visit* and *Uncollected visits* (apart from finding 2's
    sentence);
  - `desk.md`, `payments.md`, `overview.md`, `spaces.md`'s code map;
  - conventions §9 and the header.

  Each is true to the code except findings 2, 4, 5 and 8.
