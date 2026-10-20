# Review — DESK PR 2 (#95, `feat/desk-visits`)

**Head:** `b225d1fa8fc3f6baa23985c1ebfea6c262639ef9` · base `origin/main` `7d48c9c3` · `gh pr checks 95`: every
lane `pass` (CodeRabbit skipped) · `CLEAN` · the head was the same at the start and at the end of the review.
**Method:** I read only commit objects (`git diff origin/main...b225d1fa`, `git show <commit>`, `git show
b225d1fa:<file>`), with no checkout, run or edit. **Seen in the code** means I read it at the head. **From the
report** means I took it from `4_REPORT_PR2.md` and did not re-run it: every red-first line, every break, the real
run, and §12.2 check 2's P2039 shape.

**Verdict:** no blocker. The money path, the locks and the authorization do what the plan and the owner's note
say. There are two should-fix items on the check-out (one a 500 on client input, one a cashier's payment silently
dropped with a 200) and a few small items. **Nothing needs a fix round on this PR.**

## The five most important findings

1. **should-fix — a quote time earlier than the check-in answers 500.**
   `apps/api/src/modules/desk/desk.service.ts:65-73` (`pricedAt`) only checks that `checkedOutAt` is at most 5
   minutes old and not in the future. It never compares it with the visit's `checkedInAt`.
   - **What happens:** a visit is checked in at 10:18. A check-out at 10:20 sends `checkedOutAt` = 10:16, which
     is within the bound. `chargeOf` bills the 1-minute minimum (`billedMinutesOf` clamps a negative stay). Then
     `visits.close` writes `checked_out_at < checked_in_at`, and the front-desk migration's
     `visits_checked_out_at_check` refuses it (seen in `20260929120200_front_desk/migration.sql`).
     `checkViolationOf` reads that name, but `CONSTRAINT_CODES` (`shared/errors/constraintCodes.ts`) has no
     line for it, so `toAppError` answers a generic 500.
   - **Who can cause it:** a buggy or hostile desk client, or a quote kept from another visit. The contract's
     check-out errors (`api-contract.md`, *Front desk*) name no such case.
   - **Fix:** in `pricedAt`, or right after `lockIn`, refuse a time before `locked.checkedInAt` with 422
     `out_of_range` on `checkedOutAt`. Add a test, and a break (the comparison removed → 500).
   - **Where:** PR 3's first commit (small).

2. **should-fix (a decision, plausible as a risk) — a check-out that loses the race drops the second desk's
   payment and still answers 200.** `desk.service.ts:138` answers a visit already closed with
   `{ visit, payment: recorded?.payment ?? null }`, whatever the body carried.
   - **What happens:** in `checkOut.api.test.ts:299-318`, two desks check one visit out at once, each sending
     `payment: 1,500 CASH`. Both get **200**. One gets `payment: null`, and its cash is never recorded. The same
     happens with another key after the visit was closed (`:285-297`). The client can only tell from
     `payment: null` beside a payment it did send. On a weak connection, or with two cashiers, that reads as
     success while money taken at the desk is in no ledger.
   - **Why it is not a code defect:** this is what the plan specified (T20, *desk.md*'s decision "answers it as
     it is and records nothing"), so the code is true to the plan. The risk is in the decision itself.
   - **Fix (the owner's decision):** when the request carries a `payment` (or a `charge`) and the visit was
     closed by another key, answer `conflict` (409) with a code such as `VISIT_ALREADY_CLOSED`, with the closed
     visit available to re-read. The retry with the same key would stay 200.
   - **Where:** record as a finding now, so the owner decides before the desk's screen (step 13) is built
     against it.

3. **should-fix (small) — `security.md` contradicts itself again in the same sentence the carried item 3 fixed.**
   `docs/backend/security.md` (*Authorization*, the boundary bullet) says "Each write is then decided by its own
   `can()` action (owner-only, or the staff's for the override)". The next sentence adds the desk's writes
   (`attendance.record`, the staff's). Item 3's wording is already stale in the PR that wrote it.
   - **Fix:** "(owner-only, or the staff's for the override and the desk's writes)", or a wording that does not
     list the actions.
   - **Where:** PR 3's first commit.

4. **nit (record) — the unpaid rest replaces a visit's own customer.** `desk.service.ts:174-184`: when any part
   is left unpaid, `customerId` becomes the phone's customer, even when the locked visit already has one
   (`locked.customerId`). The name falls back to `''` when the visit has no `visitorName` (`:177`). Neither can
   happen in PR 2: every visit is checked in by name, and step 8 builds the customer check-in (DK-020).
   - **What would happen:** once step 8 checks a customer in as a visit, an unpaid check-out with another phone
     would move that customer's debt to someone else.
   - **Fix (step 8):** a visit with a customer keeps it (the phone is not asked, or must match it).
   - **Where:** a finding to record, named for step 8.

5. **nit — two places say who may type a price.** `docs/features/visits.md` (*Responsibility boundary*) says
   `visits` **leaves** "`can()` and who may type a price to `desk`". In the code, `visits.service.ts:197-200`
   (`terms`) calls `can(actor, 'prices.typeByHand', …)` itself, from the boundary's links.
   - **Fix:** say that `visits` asks `can()` for the terms' `mayTypePrice`, and that `desk` decides under the
     lock.
   - **Where:** PR 3's first commit.

## The rest

6. **nit — the contract's `VisitCharge.roundingRule` comment is incomplete.** `api-contract.md` says
   "`// … null when typed`". `chargeOf` (`visitCharge.ts:98-107`) also stores `null` for a computed day-price
   charge (no hour rate), as do `roundingMinutes` and `capApplied`. **Fix:** "null when typed, or when the charge
   is the day price alone". PR 3's first commit.
7. **nit — the check-in's warnings count *present* a second time.** `occupancy.service.ts`'s `checkInWarnings`
   adds `visits.openIn(…).length + subscriptions.openCheckInsIn(…).length` itself. The read (`peopleIn`) and the
   directory (`liveStatusFor`) have their own forms. The three agree today, but `occupancy.md` and PR 1's
   acceptance call *present* "one definition". It also loads every open row only to count them. **Fix:** one
   `presentIn(spaceId, tx)` helper that the read and the warnings both use. A finding, or PR 3 if it touches
   `occupancy` anyway.
8. **nit — a key that closed a visit unpaid is not remembered.** `desk.service.ts:134-137` detects a reused key
   only through a payment row. Take a check-out with key K that records no payment (all left unpaid, or an
   unpriced close). If K is later reused for visit B, B is checked out normally. A real retry of the first
   request then gets `conflict` ("paid another item") instead of its first result. This needs a client that
   reuses keys across actions, which is a client bug. Record with item 2 if the owner revisits the rule.
9. **nit (plausible) — the charge can overflow its `Int` column.** The cap off, an hour price near
   `PRICE_MAX_AGOROT` (10,000,000), and a stay of about 215 hours or more make `byRounding`
   (`visitCharge.ts:71-84`) exceed 2³¹. The insert then fails, and the check-out answers 500. The prices this
   needs are absurd, and PR 3's auto check-out bounds the stay. Plausible only. Record or ignore.
10. **nit — commit `ec37ae95`'s body does not mention finding 98.** The commit holds finding 98 (folded in by
    `3c_RESUME_PR2.md`, by design), but its body speaks only of the override. The PR description does say it.
    No fix needed now (the history would have to be rewritten). Noted for the record.
11. **Seen, by design, not a finding:** the cap is one day price even for a stay over midnight (Review Focus 1).
    `occupancy.md` is not trimmed (finding 98). A check-in during a closure in force gives no warning, since P9
    lists only the hours.

## Departures and breaks, judged (from the report, with the code read where it applies)

- **`ratesFor` without `studentPrices`:** sound. `visits.ratesAt` (`visits.service.ts:97-99`) refuses `STUDENT`
  before it is called, and `terms` hides the student rates when the setting is off.
- **`visits` and `customers` audit their own entries;** **`announcements.closedAt(…, tx)`;** **`overrideInUse`;**
  **`spaces.shiftsOf`:** each is seen in the code and used as the report says. None crosses a level.
- **B25 reworded; B31 made as one break:** acceptable. No rounding is stored at check-in, so the plan's form
  cannot exist.
- **The data model's *Live status* 3 left unchanged:** still true.
- **A1:** built as approved. The four tests are in `checkOut.api.test.ts:445-510`.
- **The quote's age:** 5 minutes (`QUOTE_MAX_AGE_MS`), and the audit records `checkedOutAt` and `requestedAt`.
  Both are seen in the code and asserted in T22.
- **The real run's demo data left in `masaha_b_dev`, the switch turned off and back on:** from the report.
  Harmless.

## Checked and fine

- **The migration:** the function is the payments migration's, character for character, except
  `CREATE OR REPLACE` and the one `RAISE` (I diffed the two at the head). `visits_charge_reason_check` is as
  planned. The schema adds the one field and nothing else.
- **The ledger:** the service repeats no rule. `PAYMENT_EXCEEDS_DUE` and `VISIT_NOT_PRICED` reach the client
  through one table. Any other check violation stays 500. The visit is closed before the payment is inserted, so
  the trigger reads the new charge.
- **The money rules** (`visitCharge.ts`):
  - P7's three roundings, the 1-minute minimum, half-up agorot, and the cap with `capApplied` are as planned.
  - Day price only when there is no hour rate; no charge when there is neither.
  - `roundingMinutes` is set only for `UP_AFTER_MINUTES`, which matches `visits_rounding_check`.
  - P8's student and shift fallbacks work period by period; only standard (unlabelled) prices count.
- **Part payment:** a phone is required for any part left unpaid. The customer is found among those not
  archived (the partial unique index), or created and audited. The name given for a found customer is ignored.
- **The hand-typed price:** allowed only where the visit has no rate (`invalid_choice` otherwise).
  - `can('prices.typeByHand')` is decided on the links read under the lock and the settings read in the
    transaction. The owner always; reception only with the switch; never the admin or anyone else.
  - Whoever may type must type (`required`); anyone else closes the visit unpriced.
  - The reason and the typer are stored together, as the `CHECK` requires.
- **Retries:**
  - The check-in's key is read first, under the space's lock, so a retry writes no second row.
  - The check-out's closed check comes before `pricedAt`, so a retry later than 5 minutes still gets its first
    result rather than 422.
  - A payment key used for another visit answers `conflict`.
- **Locks:** the space's lock (`FOR NO KEY UPDATE`, which the foreign keys' `KEY SHARE` does not block), then
  the visit `FOR UPDATE`, then the customer, then the payment (the trigger's `FOR UPDATE` on a row this
  transaction already holds). The override takes the space only. No two orders cross.
- **Authorization:** both writes go through `requireCan('attendance.record')`, then `requireIdempotencyKey`,
  then `validate`. `can()` runs again under the lock. Every query is scoped by `spaceId` (`lockIn`, `findIn`,
  `findByKey`, `ratesOf`), and a shift of another space is caught by the composite foreign key. The reads sit
  behind the boundary. No public answer changed. `DeskVisit.customer.phone` appears only on managed routes.
- **The carried commits:**
  - Item 1's test asserts the closure and the override on the card, the pin and `/occupancy`.
  - Item 4 refuses an override under a closure (read in the transaction) and on an unverified space (links read
    under the lock), with `SPACE_NOT_OPEN`.
  - Item 5: the staff's read answers the override through `overrideInUse`, which `liveStatus` itself calls.
  - `SPACE_NOT_OPEN`'s line names the three cases in both catalogues.
  - `v1-mvp.md`'s reception sentence is fixed.
- **Documents:**
  - The contract's *Front desk* section, §1 and §6 match the code; the exceptions are items 1 and 6 above.
  - The data model's *Visit charge*, *Unpaid visit* and *Constraints* bullets match.
  - Conventions §4, §13 and the *Built* header match.
  - `desk.md`, `payments.md` and `occupancy.md` match, as does `visits.md` apart from item 5.
  - Finding 15 is resolved and its index line moved. Finding 98 is recorded as directed and takes no side.
  - `overview.md` and `v1-mvp.md` say only what is built.
- **Scope:** `apps/api`, `packages/shared` and `docs`, plus the two web catalogues. No dependency and no
  lockfile change. No PR 3 code (no job, no list, no pricing route).
- **Commits:** 6 commits, Conventional Commits subjects of 49 / 42 / 39 / 30 / 46 / 45 characters, each body
  saying why, no tool attribution.
