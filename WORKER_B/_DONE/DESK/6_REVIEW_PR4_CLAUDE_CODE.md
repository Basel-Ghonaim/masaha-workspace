# Review — DESK PR 4 (#100, `feat/visit-debts`)

**Head:** `68edd9bc1fca52f1ebc0a81c7bca56c3a8c5a09d` · base `origin/main` `cf3190a4` · six commits · `gh pr checks 100`
all pass (lint, typecheck, format:check, check:links, check:classes, build, test:unit, test:api, test:component,
CodeRabbit) · `CLEAN` · the head was the same at the start and the end of the review.

**Verdict:** no blocker, and nothing needs a fix round on this PR. Mergeable as it is. The money rules, the
write-off, «تسجيل دينًا», the migration and the two carried commits do what the plan and the owner's note say.
What remains: four small document fixes, which belong to worker B's next PR; three findings to record; and
corrections to the PR description.

**Method:** I read only commit objects: `git diff origin/main...68edd9bc`, `git show 68edd9bc:<file>`, the six commit
messages, the PR description and `gh pr checks`. I ran no tests, builds, servers or database commands. Where this
report says "seen", I read it in the code. These come **only from `4_REPORT_PR4.md`**, and I did not re-run any of
them: every red-first run, the 39 planned breaks and the five carried ones, the migration created once, the function
being `t` on both databases, the real run on 3321, and the local `test:api` re-run (998 passed). The full API lane was
**not** left to CI as its judge. It was killed once for memory, the owner allowed one re-run, and that re-run passed
on `d48accf5`, before the rebase. The rebase brought in only `apps/web` and `docs` from `main`, so the `apps/api` and
`packages/shared` trees are the same. CI's `test:api` is green on the pushed head (seen).

---

## The five most important findings

### 1. finding to record (plausible) — a stay that always fails turns every cron call red, and a cron service may then switch the job off for every space
- **Where:** `apps/api/src/modules/visits/visits.service.ts:432` and `subscriptions.service.ts:103` (`if (failed > 0)
  throw …`), `shared/jobs/jobs.routes.ts:19` (500 when any job failed); `docs/development/setup.md`'s runbook
  (cron-job.org).
- **Seen:** the carried fix catches each stay and goes on, as asked. But a stay that cannot be closed stays in
  `due` on every run. The two ways seen are a space without its settings row, and a row the update refuses. So every
  run answers 500, forever, until someone fixes the data.
- **Failing scenario:** the runbook sends the owner to a free cron service such as cron-job.org. I *believe*, but did
  not verify, that cron-job.org disables a job after a run of failed executions. If it does, one bad stay ends the
  auto check-out for every space: the halt carried item 1 meant to remove, moved from the code to the cron service.
- **Plausible, not proven:** the service's policy is not in the repository, and no cause of a permanent failure is
  reachable today (item 2 removed the charge overflow).
- **Fix:** either the runbook says to turn the service's auto-disable off, and to read `stay not closed` in the logs;
  or the endpoint answers 200 with a `failed` count when every job ran and only stays failed, and 500 only when a job
  itself threw. That second choice changes the owner's "answers 500 when any failed", so it is the owner's call.
- **Where its fix belongs:** a finding to record (114); the runbook line, if chosen, in worker B's next PR.

### 2. should-fix (small) — three documents do not yet say what this PR built
- **Seen:**
  - `docs/features/payments.md:58`: its *History* stops at `#97`. Appendix A item 7 asks for a `#100` line: the fourth
    ledger rule, `balanceOfVisit`, `paidFor` taking a `tx`, and the payment after the check-out.
  - `docs/features/payments.md:10`: "Finds the payment a check-out's idempotency key already recorded". The payment
    route's key is found the same way now.
  - `docs/features/visits.md:33` and `:38`: *Leaves* names only "the check-out's transaction …", and *How it
    composes* says "the check-in and the check-out run in the desk's". Yet `:17`–`:18` of the same file say
    `writeOff`, `undoWriteOff` and `leaveTo` run in the desk's transaction too. Carried item 3 was worded in the
    first commit, and C2–C4 did not widen it.
  - `docs/backend/conventions.md:360`: "the four payment rules … never above the amount due, and a written-off visit
    takes no payment. **The last one** locks the item's row." "The last one" meant the ceiling and now points at the
    written-off rule. The count also leaves out `payments_visit_uncharged`, which `payments.md` and the data model
    list as a rule. That omission predates this PR, but this PR edited the line.
- **Failing scenario:** a reader of `payments.md` or `visits.md` does not learn that this PR changed them, or which
  writes `visits` leaves to `desk`. A reader of §13 takes the wrong rule as the one that locks the row.
- **Fix:** a `#100` history line, and "a check-out's or a payment's key", in `payments.md`. In `visits.md`, "the desk's
  transactions (check-in, check-out, write-off and its undo, `leaveTo`)". In conventions, "The ceiling locks the
  item's row", and either name the uncharged rule or say "among them".
- **Where its fix belongs:** worker B's next PR (SUBSCRIPTIONS PR 1), its first commit.

### 3. finding to record — a write-off and its undo have no key, so a delayed retry can flip the state back
- **Where:** `apps/api/src/modules/desk/desk.service.ts:371`–`403`; contract `POST` / `DELETE …/write-off`; `desk.md`'s
  decision "a second of either answers the visit as it is".
- **Seen:** each route is idempotent against a repeat of itself only. Nothing ties a request to the state it saw.
- **Failing scenario:** the owner, on a weak connection, writes a visit off. The response is lost. The owner undoes
  it, and that request lands. A client or proxy retry of the first `POST` then arrives, and the visit is written off
  again, with the first reason. The owner believes it is collectable, and the desk is refused `VISIT_WRITTEN_OFF`. The
  reverse order (a late `DELETE` after a re-write-off) re-opens a written-off debt.
- **Not against the plan:** D1 and the owner's Q1 chose "idempotent by design, no key". This interleaving was not
  discussed. It needs a retry that outlives a later action, which is rare. Every flip is audited.
- **Fix, for the owner to choose:** accept it as is; or make the write-off a create with an `Idempotency-Key` (ADR
  0015's "every create the desk performs"); or have each request send the state it expects, `writtenOffAt` or
  `null`, and answer 409 when it differs.
- **Where its fix belongs:** a finding to record (115). The desk's screen item should know it before it wires any
  automatic retry on these two routes.

### 4. finding to record — "a charge is bounded by one day" holds for the job only: a desk check-out of an overdue stay is priced up to now
- **Where:** `desk.service.ts:213` (`pricedAt(request.checkedOutAt, requestedAt)`, then `chargeOf` up to that time);
  commit `6172ac5b`'s body ("resolves #95's nit 9"); `data-model.md` *Auto check-out* ("a stay never crosses into
  the next day … every stay is due by 23:59").
- **Seen:** `autoCheckoutDue` now always bounds a stay by 23:59 of its check-in's Gaza day. The manual check-out never
  reads that due time: it charges up to the quote's time, which is at most 5 minutes old.
- **Failing scenario:** suppose the cron is down or switched off (see finding 1), or the check-out lands in the
  minutes between 23:59 and the next run. A desk check-out the next morning closes and charges a visit across
  midnight, for every hour since check-in, capped only when `visitCapAtDayPrice` is on. So a stay can cross into the
  next day, and nit 9's overflow is bounded only by the job running. At the largest rate it overflows after about
  214 hours, which is not a realistic risk; the overcharge is.
- **Fix, for the owner:** either the check-out charges up to `min(quote time, the stay's due time)`, which makes the
  documents true for every path; or the data model says the bound is the job's, and that the desk closes what it
  finds. #97 made "a check-out at the desk meanwhile wins" a decision, so this is a rule choice, not a code slip.
- **Where its fix belongs:** a finding to record (116).

### 5. nit — the PR description misstates two facts and leaves out departures
- **Seen in the PR body:**
  - "B1–B39 (B12 has no break of its own; B1 covers it)". It is **T12** that has no break of its own. B12 (the
    no-charge check removed) was run, red, as the report records.
  - "**On the head:** … `test:unit` … `test:api` …". Both ran on `d48accf5`, before the rebase, not on
    `68edd9bc`. The next bullet explains this, but the heading claims more than happened.
  - *Departures* leaves out four things: the schema edited by hand after `prisma format` realigned unrelated blocks;
    D1 and D2 written after the migration, so their red came only through B5 and B6; B12's and B18's red differing
    from the plan's expectation; and the PR-number fix (`#99` → `#100` by `filter-branch`). The report states all
    four.
- **Fix:** edit the description (no commit): T12; "on `d48accf5`, the code tree of the head"; the four departures.
- **Where its fix belongs:** the description, now (no commit, no CI).

---

## The rest

### 6. nit — `customerFor`'s departure keeps a debt on an archived customer when the number has been reused
- **Where:** `desk.service.ts:107`–`111`.
- **Seen:** for a visit that has a customer, the phone is compared with that customer's stored phone. The plan instead
  looked the phone up among the customers not archived.
- **Failing scenario:** the visit is customer A's, and A has since been archived. A new customer B has A's old number.
  The desk sends that number, meaning B. `customerFor` answers A, the visit is answered as it is (200, writing
  nothing), and the debt stays on archived A. The plan's lookup would have refused it (`VISIT_HAS_CUSTOMER`).
- **Judgement:** acceptable, and stated honestly in the report and the PR. The answer names A, so the desk can see
  it. And keeping a visit's own customer is the point of finding 100. No change; mention it in the screen item's
  brief.

### 7. nit — the undo route's refusals are only partly tested
- **Where:** `writeOff.api.test.ts` *undoing a write-off*.
- **Seen:** reception's 403 is tested (T12). The contract also claims these for the undo: `not_found` for a stranger,
  another space's owner, the admin and another space's visit; and 403 for an owner whose link ended meanwhile.
  None of them is tested. They share `lockAtDesk` and `visits.lockIn` with the write-off, whose tests cover them (T4,
  T5, B11), so the risk is a later divergence only.
- **Fix:** if wanted, a few lines in T11/T12.
- **Where its fix belongs:** worker B's next PR, only if that PR touches the file. Otherwise leave it.

### 8. nit — the 23:59 bound closes a check-in made in the day's last minute at once
- **Where:** `apps/api/src/modules/spaces/autoCheckout.ts` (`Math.max(Math.min(...dues), checkedInAt)`).
- **Seen:** a check-in at 23:59:30 is due at its own check-in time, so the next run closes it with a stay of
  seconds. Before this PR, the same held only for spaces with closing time on. With both switches off, such a stay was
  never closed.
- **Judgement:** this follows from the owner's choice (b), "always". Opening ranges are inside the day by their
  `CHECK`, so no space is open across midnight. No change.

---

## Checked and fine

- **CI:** green on the pushed head, and `CLEAN`; the head did not move during the review.
- **Commits:** six subjects, 48, 46, 39, 42, 41 and 46 characters, each with a body saying why. There is no tool
  attribution. The two carried commits come first, then C1–C4 as §11 lists them.
- **Scope:** `apps/api`, `packages/shared`, `docs`, the two `errors.ts` catalogues (error lines only), and
  `.env.example` (carried item 4). There is no `package.json` or lockfile change, and nothing on the *Not in v1* list.
- **The payment:** `POST …/payments` (`desk.service.ts:285`–`336`) checks, in this order:
  - `lockAtDesk(…, 'payments.record')`: the space's lock, then `can()` on `linksUnder(tx)`;
  - `visits.lockIn`, scoped to the space (404);
  - `findByKey`, scoped to the space: another item → 409, this visit → the retry, answered with the sums now (S5);
  - an open visit → 409;
  - the insert, so the ledger's refusals come before any phone is asked for;
  - `balanceOfVisit` read in the transaction under the visit's lock;
  - the unpaid-part rule only when `rest > 0`.

  The route runs `requireCan` → `requireIdempotencyKey` → `validate`, so the key and the body are refused before
  anything is read. `recordedById` is the caller. A 422 for the phone after the insert rolls the insert back. An open
  visit is also refused in the database: it has no charge, so `payments_visit_uncharged` fires.
- **The trigger** (`20261020124728_visit_write_off`): `payments_guard_insert` is copied whole from
  `desk_visit_charge`. The only changes are `written_off boolean`, the visit's `SELECT … INTO due, written_off …
  FOR UPDATE`, and the `payments_visit_written_off` raise after `IF NOT FOUND`. I compared the two texts.
  `CONSTRAINT_CODES` maps the new name to `VISIT_WRITTEN_OFF`. The written-off check runs under the visit's row lock,
  so a write-off and a payment are decided in turn, by the space's lock first and the row lock as a backstop.
- **The `CHECK`:** it requires the three columns together, a non-blank `btrim` reason, and a closed (`checked_out_at`)
  and priced (`charge_agorot`) visit (S4). The FK is `RESTRICT`. Pricing refuses a priced visit
  (`VISIT_ALREADY_PRICED`), so a written-off visit's charge cannot change. D1 and D2 prove them.
- **The write-off and its undo:**
  - `requireCan('visits.writeOff')` at both routes, before `validate`, and again under the lock; `'visits.writeOff':
    'owner'` in `can()`, and U1 checks all six actors;
  - open → 409; already written off → answered as it is; no charge → `VISIT_NOT_PRICED`; balance ≤ 0 →
    `VISIT_ALREADY_PAID`; the amount written off is audited (`after: { reason, balanceAgorot }`), and the payments are
    untouched;
  - the undo clears the three columns, audited `before: { writtenOffAt, writtenOffById, reason }`; one with nothing
    to undo writes nothing;
  - the reason is `textSchema(1, 200)`, trimmed;
  - `autoClosedIn` and `autoClosedPage` both filter `writtenOffAt: null`; T1, T34 and B7 cover it;
  - ADR 0009's row, and its *Revised* line, are under rule 5.
- **«تسجيل دينًا»:**
  - space lock → `lockClosed` (404 / 409) → written off (`VISIT_WRITTEN_OFF`) → balance ≤ 0 (`VISIT_ALREADY_PAID`;
    unpriced allowed) → `customerFor` → the same customer answered as it is, else `leaveTo`, audited;
  - the customer is found or created by `customers.findOrCreateByPhone` under the space's lock;
  - two desks with two phones: T33 and B39 cover it.
- **Finding 100 folded:** one helper serves the check-out, the payment and the debt. T26 covers the check-out. The
  finding is marked Resolved and moved in the index.
- **The carried commits:**
  - each stay is caught, logged `{ err, job, stayId }` and counted, in both jobs, and the run throws when
    `failed > 0`;
  - `settingsFor` leaves an absent row out, so the `!rules` branch is real. Its only callers are the two jobs (`git
    grep`);
  - `autoCheckoutDue` is one `Math.min` over 23:59 always, the closing when on, and the limit when set, never before
    the check-in; it returns a `Date`, and the callers' `dueAt &&` is gone;
  - the unit tests cover the three branches;
  - the new jobs test has two stays, the first failing;
  - findings 111–113 are recorded with their index lines; the runbook names `Bearer` exactly; and the scheduler row
    has one home.
- **The documents, against the code:** these match what was built, apart from findings 2–4:
  - the contract's four routes, their error orders, `DeskVisit.writeOff`, `ReceivedPayment`, §1's key line and §6's
    three codes;
  - the data model's *Visit*, *Unpaid visit*, *Uncollected visits*, *Written-off visit*, *Customer debt*, the
    `CHECK` line, the ledger bullet and *Checked by the service*;
  - security's *Authorization*; conventions §9; `desk.md`; `v1-mvp.md` step 7 (*Goal* and *Built*: carried item 6),
    step 9's *Goal* and the route table; `overview.md`; `docs/README.md`'s two map lines; finding 110's three points.
- **The catalogues:** the Arabic and English lines match §13 Q2 word for word, including `VISIT_NOT_PRICED`'s two
  revised lines.
- **The departures, judged:**
  - `balanceOfVisit` for one visit: fine;
  - `customerFor` comparing the stored phone: fine (see 6);
  - D1 and D2 red only through B5 and B6: acceptable, because each break proves its test catches the rule;
  - the schema edited by hand: fine. Only `Visit` and one `User` line changed, and the migration's columns, FK and
    names match it.
