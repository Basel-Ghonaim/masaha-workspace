# Review — SUBSCRIPTIONS PR 1 (#102, `feat/customers`)

**Head:** `900eebb4eb7299c4c0be79f3c181df7403fee142` · base `origin/main` `befd96f9` · `gh pr checks 102`: all green
(build, check:classes, check:links, format:check, lint, test:api, test:component, test:unit, typecheck, CodeRabbit) ·
`CLEAN`. The head was re-checked at the end: unchanged.

**Read from commit objects only** (`git diff origin/main...900eebb4`, `git show 900eebb4:<file>`), in
`C:\dev\masaha\app-design`. Nothing was run: no test, no query, no `EXPLAIN`. Statements marked **(code)** were seen
in the code; **(report)** are only the executor's `4_REPORT_PR1.md`.

## Verdict

**One fix round on this PR:** the balance query that decision 6 rests on joins the payments with an `OR`, so its cost
is the space's items × its paid items, and every list page, every payment filter and every file runs it over the whole
space. The rest is small: PR 2's first commit, or findings to record.

## The five most important findings

### 1. The balance query joins `paid` with an `OR`: quadratic in the space's items × paid items — should-fix, serious
- **Where (code):** `apps/api/src/modules/payments/payments.repository.ts`, `balancesOf` (≈ lines 108–131):
  `LEFT JOIN paid p ON (i.kind = 'VISIT' AND p.visit_id = i.id) OR (i.kind = 'SUBSCRIPTION' AND p.subscription_id = i.id)`.
  The SQL is the plan's own (D5), copied faithfully.
- **Why it fails at scale:** PostgreSQL can hash-join or merge-join only on an equality clause at the top of the join
  condition; an `OR` of two equalities on different columns is neither. The planner is left with a nested loop that
  tests each item against each row of `paid`. `paid` is an aggregate over **every** non-voided payment of the space,
  every paid walk-in visit included. It is a grouped subquery, so the indexes `payments(visit_id)` /
  `payments(subscription_id)` (`schema.prisma` ≈ 810–811) cannot be used through it either.
- **Who runs it over the whole space (code):**
  - `customerBalances` calls `balancesOf(spaceId, null, …)` and filters by `customer_id = ANY(…)` afterwards. Every
    `GET …/customers` page runs it (`desk.service.ts` `customers` → `payments.customerBalances(space.id, ids, at)`), and
    so does every file (`customerFile` → `customerBalances(space.id, [customerId], at)`).
  - `customerIdsByPayment` has no filter at all: once for `OWES` or `CREDIT`, twice for `SETTLED`.
  - `statesIn` for `currentOf` also calls `subscription_usage(space, NULL, …)` and filters by `customer_id` after the
    join. Whether the page's filter reaches inside the function depends on PostgreSQL inlining it — **plausible** that
    the work is whole-space, not proven.
- **Failing scenario:** a space a year in has ~2,000 subscriptions and debtor visits (items), and ~40,000 paid visits
  (rows of `paid`). `?payment=OWES` evaluates ~8·10⁷ join conditions, and the first page with no filter about as many.
  That is seconds per request, growing with every payment, on the screen the desk opens most. PR 2 then reads
  `itemBalances` inside the subscribe's transaction, **under the space's lock**: the aggregate over all the space's
  payments runs while every desk write of the space waits.
- **Not caught:** T26 (`desk/customers.api.test.ts` ≈ 234–257) seeds 20,000 subscriptions and **no payments**, so `paid`
  is empty and the loop is free. The report records no query plan for the balances, only for the customers' page (report).
- **Fix:**
  - Join two equi-joined aggregates: `paid_visits` grouped by `visit_id`, `paid_subscriptions` grouped by
    `subscription_id`, each `LEFT JOIN … ON i.kind = '…' AND x.id = i.id`. Or a correlated `LEFT JOIN LATERAL (SELECT
    sum(…) FROM payments WHERE visit_id = i.id AND voided_at IS NULL)` per branch, which uses the existing indexes.
  - Restrict the items to the customers asked: pass the ids into `balancesOf` (an array parameter on the visits branch;
    `subscription_usage` filtered by `customer_id` before it groups, or given an array). `customerBalances` and the file
    then cost what their page holds. The file can also sum its own `itemBalances` rows instead of a second whole-space
    query.
  - Prove it: give T26's seed one payment per subscription (one `INSERT … SELECT`), or `EXPLAIN` the three queries at the
    plan's scale and record the plans, with B32–B37 re-run.
- **Where the fix belongs:** **a fix round on this PR** — it is decision 6's core query, and PR 2 builds on it under the
  lock.

### 2. T26 no longer proves "the ids reach the query as one parameter" — should-fix, small
- **Where (code):** `apps/api/src/modules/desk/customers.api.test.ts` ≈ 234–257, 20,000 ids.
- **Why:** PostgreSQL's bound is 65,535 parameters. A regression to one parameter per id (B43: `Prisma.join`) binds
  20,000 parameters, so it still runs and T26 stays green. B43 was seen red only in an uncommitted scratch run at 70,000
  (report, §12.2 check 4). The plan's check 7 said "never below 66,000 if it fits". The cost that forced 20,000 was the
  seed's (report).
- **Fix:** the bound needs no seed. Call the list with a filter that resolves to more than 65,535 ids that do not
  exist. Or, in the same file, call `customers.page` / the repository with `include: [[1…70_000]]` and assert 200 and an
  empty page: `unnest` of 70,000 integers runs in milliseconds. Keep the 20,000-row seed (it is what catches a revert to
  `= ANY`), or drop it if the new test also catches that.
- **Where:** PR 2's first commit (`0_CARRIED_FROM_102.md`), with B43 red in the lane.

### 3. The phone search misses an Israeli number typed in full, and any number typed with `00` — should-fix, small
- **Where (code):** `customers.repository.ts` `page`:
  `regexp_replace(coalesce(phone, ''), '[^0-9]', '', 'g') LIKE '%' || ${digits}`. And `customerSearch.ts`, which keeps
  the term's digits as typed.
- **Why:** phones are stored in E.164 (`core/phone.ts`): `+970599000205`, `+972521234567`.
  - Typing the local form `0599000205` finds the first only because `970` happens to end in `0`; T22 asserts exactly
    this case (`?q=0599000205`).
  - The local form of a `+972` mobile, `0521234567`, has the digits `0521234567`. They are not a suffix of
    `972521234567`, so the customer is not found.
  - `00970599000205` is not found either.
  - `normalisePhone` accepts all three forms, so the desk will type them.
- **Fix:** when `normalisePhone(q)` answers a number, match that phone exactly. Otherwise keep the suffix match on the
  digits. Add a `+972` case and a `00` case to T22 and U3.
- **Where:** PR 2's first commit.

### 4. Three documents now say something untrue — should-fix, small (documents)
- **(code)** `docs/features/occupancy.md:25`: "`subscriptions`, `customers` and `announcements` hold only these reads
  so far, with no capability document of their own". This PR created `customers.md` and `subscriptions.md` and gave both
  modules writes and reads beyond occupancy's.
- **(code)** ADR 0015 rule 4 (line 18) and line 49: "Subscriptions and customers do not carry the key yet". Conventions
  §13 and the data model now say customers carry it since #102. The plan puts ADR 0015's *Revised* line in PR 2 (Q10),
  so this is a planned gap of one PR. It becomes a contradiction on `main` the moment #102 merges.
- **(code)** `docs/features/payments.md`, the uncollected visits' decision: its head sentence still reads "composed
  without repeating the balance: `visits` names them, the ledger decides which are settled". Its own *Revised* tail and
  the code now page them in SQL by the subtraction, and `visits` names nothing.
- **Fix:**
  - `occupancy.md`: only `announcements` lacks a capability document; link `customers.md` and `subscriptions.md`.
  - ADR 0015: a *Revised* line for customers now ("customers carry the key, nullable; subscriptions with step 8's next
    PR"), or keep it in PR 2 as planned and say so in PR 2's description.
  - `payments.md`: reword the decision's head to what is built.
- **Where:** PR 2's first commit.

### 5. The auto check-out can stall silently behind 500 stays that always fail — nit, plausible, record
- **Where (code):**
  - `visits.service.ts` `autoCheckOut` (≈ 418–480) and `subscriptions.service.ts`'s twin.
  - The due stays are taken earliest first (`due.slice(0, AUTO_CHECKOUT_BATCH)`). A stay whose transaction always fails
    stays due, so it is taken again on every run.
  - Since item 1 (finding 114), the run answers 200 with `failed`.
- **Scenario:** 500 or more stays whose close always fails sit at the head of the batch on every run. The job closes
  nothing for every other space, while the cron sees 200. Two things do not count here: a space without its settings
  row is filtered before the batch, and `remaining` counts only what lies beyond the batch.
- **Plausible, not proven:** no path that makes a close fail permanently is known today. The #100 review's examples
  were the missing settings row, now outside the batch, and "a row the update refuses".
- **Fix:** leave out of the batch the stays that failed on the last run, or order the failed ones last. Or answer 500
  when a run closed nothing while `failed` reached the batch.
- **Where:** a finding to record (121).

## The rest

### 6. `subscription_usage` overflows `integer` on extreme prices and breaks the whole space's reads — nit, record
- **(code)** The migration's `count(DISTINCT c.day)::integer * s."price_agorot"` (integer × integer) and
  `round(…)::integer`. With `PRICE_MAX_AGOROT = 10_000_000`, a per-day subscription at that rate overflows after 215
  days used; a per-hour one after ~215 hours.
- Every list page, filter and file computes the function for every subscription of the space (finding 1). So one such
  row answers 500 to the space's whole customers screen, not only to its own customer.
- **Unrealistic prices; recorded:** compute in `bigint` and keep the 500 local, or bound the usage-based price lower.

### 7. Reception reads an archived customer's file, with the phone, by id — nit, owner's call
- **(code)** `desk.service.ts` `customerFile`: `customers.findIn(space.id, customerId)`, with no archived check. Listing
  archived customers is the owner's (`status=ARCHIVED` → 403 for reception), but `GET …/customers/:id` answers any
  customer of the space.
- **Arguably intended:** an archived customer's debts are still collected at the desk, and a visit's `customer` already
  shows the phone.
- **Fix, if the owner wants archived customers to be the owner's:** 403 for reception on an archived file. Otherwise
  state it in the contract. **Where:** record, or the owner's word.

### 8. A delayed retry of an edit can revert another desk's edit — nit, record (the screen item)
- **(code)** `PATCH …/customers/:id` carries no key and no expected state; `customerChange` applies any field sent.
- **Scenario:** desk A saves the whole form (name and phone) and the answer is lost. Desk B renames the customer. A's
  retry lands and writes the old name back. Both are audited.
- This is the class of finding 115.
- **Fix:** the screen sends only the fields the user changed and never retries automatically. Or the edit sends what it
  saw and is refused 409 on a difference. **Where:** a finding for the customers' screen item (with 115).

### 9. Small code points — nits, PR 2's first commit if touched
- `customerSearch.ts` drops spaces and `+` but not `-`, `.`, `(`, `)`, which `phoneSchema` accepts. `059-900-0205` is
  searched as a name. Drop the same separators as `core/phone.ts` (fold into finding 3).
- `packages/shared/src/core/errors.ts`: `CUSTOMER_ARCHIVED`'s comment says "edited or checked in no more". Checking in is
  PR 3's; say "edited", as the contract's gloss does.
- `customers.repository.ts` `page`: the doc comment's line about `= ANY(…)` runs past the file's width (Prettier leaves
  comments). It is cosmetic.

### Departures, judged
- **The two migrations by the fallbacks (report):** `migrate dev` refused a non-TTY shell. A `migrate diff --script` and
  a hand-made folder are the plan's own fallbacks. **(code)** The SQL is only `ADD COLUMN` + `CREATE UNIQUE INDEX` and
  `CREATE FUNCTION`, nothing dropped, the function identical to D3. The timestamps sort after `visit_write_off`.
  Applied to `masaha_b_dev` and `masaha_b_test`: report only. CI's API lane applied them from scratch.
- **`unnest` instead of `= ANY` (code):** correct, still one array parameter. It is the better form for long lists.
  `= ANY` remains only on lists of a page (≤ 50), which is fine. The measured 45.8 s → 0.2 s is report only.
- **T26 at 20,000 with `ANALYZE` (code):** the `ANALYZE` is the test seed's and harmless. The size breaks the test's
  point: finding 2.
- **T16–T20 on the repository (code):** acceptable. They hit the real database, as the `db/` tests do, and C5's
  endpoint tests cover the service path.
- **B25 → B25b, B36 → B36b, C6-d → C6-d2 (report; reasoning checked against the code):** sound. `spaceOf` answers 404
  without a loaded space. The payments' composite foreign key keeps a payment with its own space's item, so `paid`'s
  space filter cannot change the result. `ORDER BY v.id` matches the tests' data.
- **The archive's *present* check through the open reads (code):** `subscriptions.openCheckInsIn` and `visits.openIn`
  under the lock are bounded by who is present, and `OpenVisit` carries `customerId`. Fine until PR 3's
  `occupancy.isPresent`.
- **The overdue cap extended to the quote and the charges so far (code):** necessary, so the desk shows what it charges.
  One helper (`stayEnd`) serves all three paths, and the auto check-out uses the same `autoCheckoutDue`.
  `checkedOutAt` records the capped time, and the audit's `requestedAt` keeps the request's.
- **The jobs' 500 unit-tested (code):** `createJobs` decides `failed`, and the router's `if (failed) throw` is
  unchanged. Acceptable.
- **84 files in one PR:** the owner's answer (report).
- **Small additions (code):** `customerChange.ts`, `CustomerRow.current.packageId`, `OpenCheckIn.subscriptionId`, and
  `DeskSubscription` without PR 2's columns. Each is needed and claims nothing unbuilt.

## Checked and fine (code)
- **Authorization:**
  - Customers' writes sit behind the managed boundary, and the router is mounted on `manage`.
  - Create and edit: `requireCan('customers.manage')` → key → `validate`.
  - Restore: `requireCan('customers.archive')`, then `lockFor(…, 'customers.archive')` with `linksUnder(tx)`.
  - Archive: `requireCan('customers.archive')`, then `lockAtDesk(…, 'customers.archive')`.
  - `status=ARCHIVED` is refused to reception by `can()` before any read.
  - Every lookup by id is space-scoped: `findIn` by `id_spaceId`, `deskVisitsOf` and `paymentsOfVisits` by `spaceId`,
    `statesIn` by `subscription_usage`'s space, and the balances by `space_id`.
  - Stranger, other owner and admin get 404 on every route (tests).
  - No export route; the list is capped at 50 a page. Paging through every customer is possible, as the owner's point 3
    allows.
- **Money:**
  - Debt, credit and the payment filter come from one SQL shape in `payments`.
  - `voided_at IS NULL` in `paid` and in the uncollected page. `written_off_at IS NULL` on visits.
  - An unpriced visit is no debt (`greatest(NULL, 0)` = 0). Credit is filtered to `usage_based`.
  - The file's debt and the list's come from the same `customerBalances`.
  - The check-out cap: `min(pricedTo, due)` and `pricedTo ≥ checkedInAt` checked first.
- **The customer:**
  - Phone normalised by `phoneSchema`. `PHONE_TAKEN` is read under the lock before the write, on create, edit (new phone
    only) and restore.
  - The key is unique per space and read first under the lock. A retry answers the same row, 201.
  - Edit by both roles; `CUSTOMER_ARCHIVED` on edit; an edit that changes nothing writes nothing.
  - Present → `MEMBER_ALREADY_CHECKED_IN`; an owing customer is archived. A repeated archive or restore writes nothing.
  - The name search uses `strpos` on `masaha_search_text`, so `%` and `_` in `q` are not wildcards.
- **Status and progress:**
  - `today = gazaClockOf(at).date`; `weekStartOf` gives the Saturday on or before (`(dow + 1) % 7`).
  - The order is ended → `UPCOMING` → `EXPIRED` → `ENDING_SOON` → `ACTIVE`. "At most 7 days" is inclusive. The 20 %
    rule uses `≤`.
  - `@db.Date` is read at UTC. `currentSubscription` ranks running, then upcoming, then expired, then the latest start,
    then the id.
  - `subscription_usage`:
    - days by the Gaza date, open or closed;
    - closed stays' whole minutes, with `floor`;
    - per-hour due `round(numeric)`, which is half up for positive amounts;
    - the week from the caller.
- **Finding 113 (C6):** one query and its count, the settled visits left out in SQL, the unpriced kept, newest closed
  first. `autoClosedIn` and `autoClosedPage` are gone; nothing else calls them.
- **Carried items 1–5 (code):**
  - Each job counts `failed` and logs `stay not closed` with `{ err, job, stayId }`; the endpoint answers 500 only when a
    job threw.
  - Finding 116's cap is on every pricing path.
  - Finding 115 is recorded Open with its condition, and findings 114 and 116 are Resolved.
  - The index is moved: 113, 114 and 116 under *Resolved*; 115 and 120 under *Open*.
  - `payments.md`, `visits.md` and conventions §13 are as item 4 asks. Nit 7's tests are added.
- **Documents:**
  - The contract: *Customers (managed)*, §1's key line, §4's exception for the file, §6's `CUSTOMER_ARCHIVED` and the
    `PHONE_TAKEN` and `MEMBER_ALREADY_CHECKED_IN` glosses.
  - The data model: idempotency, progress, status with `UPCOMING`, ended → expired and "at most 7 days", amount due,
    customer debt, the constraint line.
  - Conventions §8, §9 and §13; `security.md`; ADR 0009's two rows and its *Revised* line.
  - `customers.md` and `subscriptions.md` (template), `desk.md`, `visits.md`, `v1-mvp.md`, `overview.md`, finding 120.
  - All of these match the code, with the three exceptions in finding 4.
- **Errors and catalogues:** `CUSTOMER_ARCHIVED` is in shared and both catalogues, with the Arabic and English exactly
  as §13 Q2. `apps/web` has only those two lines changed.
- **Scope:** only `apps/api`, `packages/shared`, `docs` and the two catalogues. No dependency. Nothing from PR 2 or 3
  beyond the shared statuses.
- **Commits:** ten Conventional subjects of at most 47 characters, each with a body that says why. No tool attribution.

## Where each fix belongs
- **Fix round on #102:** 1.
- **`0_CARRIED_FROM_102.md` → SUBSCRIPTIONS PR 2's first commit(s):** 2, 3 (with 9's separators), 4, and 9's comment.
- **Findings to record (121 on):** 5, 6, 8; 7 as the owner decides.
