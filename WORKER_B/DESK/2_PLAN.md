# DESK — the front desk and visits, on the API (build map step 7) — the plan

> **Base:** `origin/main` at `eff0a3d1` (Merge #92, SETTINGS, 2026-10-19). **Worker:** B, in
> `C:\dev\masaha\app-b`. **Folder:** `C:\dev\masaha\workspace\WORKER_B\DESK\` — this plan `2_PLAN.md`;
> the reports `4_REPORT_PR<n>.md`.
> **Three PRs in sequence**, each cut from the latest `origin/main` once the one before it has merged:
> **PR 1** `feat/live-status` (≈ 58 files) · **PR 2** `feat/desk-visits` (≈ 52 files) · **PR 3**
> `feat/auto-checkout` (≈ 44 files). Each is over 25 files and touches authorization, transactions or the
> schema: each gets a separate review conversation (workflow §2, phase 7).
> **Read only from commit objects** (`git show origin/main:…`); nothing was run, built, installed or checked
> out. Every point this plan could not prove by reading is an **executor check** (§12.2 of each PR), with what
> to do if it fails.
> **In parallel:** worker A's USERS (`feat/admin-users`, `apps/web` and `docs`). No code file is shared. Its
> shared documents are likely text conflicts: `docs/project/overview.md` (*Built* lines) and, only if this
> item records a finding, `docs/architecture/findings/README.md`. This plan does not edit
> `docs/frontend/architecture.md`. The web's copy catalogues `apps/web/src/shared/copy/{arabic,english}/errors.ts`
> are edited here (the error codes' lines, worker B's licence); USERS's plan does not list them.
> **Finding numbers:** none is planned; any finding the executor records takes the next free number on the
> latest index (USERS may take 98 and on) — written `<n>` below.

> **Approved by the owner, 2026-10-19 — binding on every executor of this plan:**
> - **§13 as recommended:** **Q1** `@date-fns/tz` (A2 not taken); **Q2** the six codes with their lines as
>   written; **Q3** the rounding details; **Q4** a shift without a price falls back to the unshifted price;
>   **Q5** a check-in on a closed day or after closing is due at 23:59; **Q6** PR 2's migration; **Q7**
>   `JOBS_SECRET`; **Q8** S3 (a retry recomputes its warnings); **Q11** no split of PR 1 (A5 not taken).
> - **Changed from the plan — the quote's age (P6, S5):** at most **5 minutes**, not 10; the audit entry of
>   the check-out records **both** the quote time used and the request's own time.
> - **A1 taken:** the unpriced close (Q4 of the prompt) is built in **PR 2's** check-out, not PR 3 —
>   `VISIT_NOT_PRICED` and its tests move to PR 2 as A1 says; PR 3 keeps the reads and the pricing.
> - **A3 taken — a PR 4** after PR 3, before the desk's screen: collecting an uncollected visit and writing
>   one off (K6, DK-012), planned from A3 in its own short plan section when PR 3 has merged (the supervisor
>   asks for it). **A4 taken — finding 17's sweep** as a small item after PR 4. **A6 not taken.**
> - **Reviews:** each PR in its own Claude Code conversation, split across two subagents.
> - **Each PR has its own execution prompt** (`3_EXEC_PROMPT_PR<n>.md`); an executor builds only the PR its
>   prompt names, and the next PR starts only after the previous one has merged.

---

## 1. Summary

Step 7's API: the staff run the day at the desk.

- **PR 1 — presence and the live status.** `occupancy` gains the one definition of *present* (open visits
  plus open subscription check-ins), the count and the one list of who is present, answered to the staff
  with the capacity and the live status (`GET …/occupancy`); the pure live-status rule of ADR 0008, every
  branch; the manual override (`PUT` / `DELETE …/status-override`), which never outlives the space's next
  closing. The public directory gains the live state: on the card and the pin, the `availableNow` filter
  (applied before the page is cut), and ADR 0008's `GET /spaces/:slug/occupancy`. Gaza time arrives
  (`@date-fns/tz`, conventions §11).
- **PR 2 — the visit.** `desk` checks a visitor in and out, each in one transaction. Check-in copies the
  visit's rates (DI-41's student fallback, the shift's prices) and warns when the space is full or outside
  its hours. Check-out computes the charge from the rounding and the cap in force, at the moment the desk
  quoted it, records **the first payment ever written** (ADR 0010; finding 15 resolved by a new constraint
  name), leaves the rest unpaid only with a phone number (a customer found or created by it), and lets a price
  be typed by hand, with its required reason, by the owner always and by reception only where the space
  allows it. Check-in and check-out are idempotent (ADR 0015).
- **PR 3 — auto check-out and uncollected visits.** The scheduler port (ADR 0014): one job, run every
  5 minutes by an in-process timer locally and by a free external cron calling a secret-protected endpoint
  online, closes every stay **at its due time** — never at the run's time — idempotently, catching up. Q4:
  reception without the right to type a price closes a visit with no rate **unpriced**; the owner prices it.
  `payments` answers the uncollected visits; `visits` the unpriced ones; both are what the owner's
  «يحتاج انتباهك» will count.

Nothing in `apps/web` except the error codes' catalogue lines. No subscription, customer list, payment
route, announcement, debt or shared-device rule beyond what each PR names (§2, *Out of scope*).

---

## 2. The contract

### Scope

**PR 1**
1. `@date-fns/tz` as a direct dependency of `apps/api` and `packages/shared`; `core/gazaTime.ts`: an
   instant's Gaza date, weekday and minute, and a Gaza date and minute as an instant.
2. `occupancy`: the pure live-status rule (`liveStatus.ts`) and the override's end (`overrideUntil.ts`);
   *present* from `visits` and `subscriptions` (new, each a read of its own open rows), names from
   `customers` (new, one read), closures from `announcements` (new, one read), the week from `spaces`.
3. `GET /manage/spaces/:spaceId/occupancy` (🧾): status, capacity, present, the override in force and the
   people present, whole.
4. `PUT` / `DELETE /manage/spaces/:spaceId/status-override` (🧾): set for 30 min, 1 h, 2 h or until
   closing, capped at today's closing; refused while the space is not open by its hours; cleared early.
5. `directory`: `liveStatus` on `DirectorySpace` and `MapPin`; `availableNow=true` on the list and the
   map; `GET /spaces/:slug/occupancy` → `{ status }`.
6. Error code `SPACE_NOT_OPEN`.

**PR 2**
1. Migration `desk_visit_charge`: `visits.charge_reason` with its `CHECK`; the payments insert trigger
   raises `payments_visit_uncharged` for an uncharged visit (finding 15, item 2).
2. `visits` (pure `visitCharge.ts`: the rates, the charge), `customers` (found or created by phone),
   `payments` (new: the payment of a visit at its check-out; the translation table's first lines), `desk`
   (new: the two orchestrations).
3. `POST /manage/spaces/:spaceId/visits` (🧾, `Idempotency-Key`): check in by name, with
   `meta.warnings`.
4. `POST /manage/spaces/:spaceId/visits/:visitId/check-out` (🧾, `Idempotency-Key`): the charge, the
   payment, the unpaid rest with a phone, the typed price with its reason.
5. `GET /manage/spaces/:spaceId/visits/:visitId` (🧾, the quote while open) and
   `GET /manage/spaces/:spaceId/visit-terms` (🧾); the occupancy read's visits gain their charge so far.
6. `can()`: `prices.typeByHand`, owner always, reception where the space allows it.
7. Error codes `SPACE_FULL` (a warning), `PAYMENT_EXCEEDS_DUE`, `PRICE_TYPING_NOT_ALLOWED`.

**PR 3**
1. `spaces`: the pure auto check-out due time (`autoCheckout.ts`).
2. `shared/jobs`: the job runner, the in-process timer (`server.ts`), the internal endpoint
   `POST /api/v1/internal/jobs/run` behind `JOBS_SECRET`.
3. The job `autoCheckOut`: `visits` closes its open visits, `subscriptions` its open check-ins, each at its
   due time, with the visit's charge as at that time.
4. Q4: a visit with no rate, checked out by someone who may not type a price, closes **unpriced** (a phone
   required); `GET …/unpriced-visits` (🧾); `PUT …/visits/:visitId/charge` (🧾, the hand-typed rule).
5. `GET …/uncollected-visits` (🧾, `payments`).
6. Error codes `VISIT_NOT_PRICED` (translated from `payments_visit_uncharged`), `VISIT_ALREADY_PRICED`.

### Acceptance criteria

**PR 1**
- [ ] `liveStatus` returns, in data-model order: `null` unverified; `CLOSED` under an active closure or
      outside today's hours; the override's state while one is in force; `null` with no hours or no
      capacity; `FULL` at present ≥ capacity; else `AVAILABLE` — each branch a unit test.
- [ ] *Present* is the open visits plus the open subscription check-ins of the space, one definition, used
      by the staff's read, the directory and (PR 2) the full warning.
- [ ] `GET …/occupancy` answers the owner and reception; anyone else 404; no public answer carries a
      capacity or a count (key-exact tests).
- [ ] An override ends at `min(now + duration, today's closing)`; refused with 409 `SPACE_NOT_OPEN` while the
      space is not open by its hours or has none; set and cleared under the space's lock, `can()` on the
      links read there; audited.
- [ ] Every directory card and pin carries `liveStatus`; `availableNow=true` keeps only `AVAILABLE` spaces,
      before the page is cut; `GET /spaces/:slug/occupancy` answers `{ status }` only.

**PR 2**
- [ ] Check-in stores the rates of the visit's audience and shift as they are then; refuses `STUDENT` where
      the space turns student prices off; warns `SPACE_FULL` / `OUTSIDE_OPENING_HOURS`, never blocks; one
      transaction; a retry with the same key returns the same visit, 201, never a second row.
- [ ] Check-out stores the charge from the rounding and cap in force; records the payment; refuses an amount
      above the charge through the database's trigger (`PAYMENT_EXCEEDS_DUE`); requires a phone when any of
      the charge stays unpaid, finding or creating that customer; one transaction; a retry returns the first
      result; a check-out of a visit already closed records nothing.
- [ ] A typed price (only where the visit has no rate) carries a required reason and who typed it; reception
      types only where the space allows it (403 `PRICE_TYPING_NOT_ALLOWED`).
- [ ] The trigger names an uncharged visit `payments_visit_uncharged`; finding 15 resolved.

**PR 3**
- [ ] A stay due at 18:00 and closed by a run at 18:04 is closed at 18:00, charged to 18:00; a second run
      closes nothing and audits nothing; a run after a day without runs closes every past-due stay at its own
      time.
- [ ] The endpoint answers 401 without the secret or with a wrong one, and runs the job with it; it is absent
      when `JOBS_SECRET` is unset; production requires `JOBS_SECRET`.
- [ ] Reception, without the right to type, checks out a visit with no rate: closed unpriced, never free;
      it is listed among the unpriced visits; the owner prices it with a reason.
- [ ] The uncollected visits are the visits closed by the auto check-out and not fully paid, the unpriced
      ones included; paged.

### Out of scope

- The desk's screen (13) and every web change but the catalogue lines: worker A's later item.
- Checking a **customer** in as a visit (DK-020), subscription check-ins, the customers list and file, a
  customer's debt read: step 8. `MEMBER_ALREADY_CHECKED_IN` stays unused.
- A payment outside a visit's check-out (`POST …/payments`), collecting an uncollected visit (DK-012), its
  write-off (K6), voids, collections: step 9 — or the *Proposed alternatives*' PR 4.
- The shared desk device (`OPEN_DECISIONS.md` point 4): no idle sign-out, no staff switch.
- Announcements' writes (step 10): `announcements` gains one read only.
- The overview's work queue (step 12): PR 3 only exposes its inputs.
- The online function entry (F-7): the endpoint is built; the entry that serves it online is not.
- Sweeping expired rate-limit counters and tokens (finding 17): not folded (§6).

---

## 3. The reading done

From `origin/main` at `eff0a3d1`: `CLAUDE.md`; `docs/development/workflow.md` (whole); `testing.md`
(whole); `docs/backend/conventions.md` (whole: §4 errors, §6 audit, §7–§8, §9 *settings*, *occupancy*, *the
front desk*, *composed reads*, §11, §12, §13); `docs/backend/security.md` (*Authorization*, *Rate limits*,
*HTTP hardening*); `docs/api/api-contract.md` (§1–§4, *Managed spaces*, *Packages*, *Staff*, *Settings*,
*Capacity*, *Directory*, §6); `docs/architecture/data-model.md` (whole); ADRs 0002, 0008, 0009 (with its
revisions), 0010, 0014, 0015, and 0012 (its ports); `docs/plans/v1-mvp.md` (steps 6–12, *Ordering notes*,
*Planned API surface*); `docs/features/{occupancy,space-settings,directory}.md` (whole), `spaces.md` (its
locks and hours); `docs/README.md` (the map, *Deferred documents*); `docs/architecture/documentation.md` §5;
`docs/project/overview.md` (*Built*, the desk's v1 lines); `docs/design/SCREENS.md` (13);
`docs/design/prototype/masaha/desk-{core,sheet,data}.*` (the charge, the debt by phone, K6, DK-012);
`C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_DESK.md` (K1–K8, DK-001…024) and `DECISIONS_OWNER.md`
(O3); `C:\dev\masaha\workspace\_SHARED\OPEN_DECISIONS.md`; the findings index and findings 15, 17, 23, 52,
77, 84, 96, 97; `apps/api/prisma/schema.prisma` (spaces, settings, occupancy, customers, subscriptions,
check-ins, visits, payments, announcements, audit) and the migrations `front_desk`, `payments`,
`space_occupancy_table`, `reception_typed_prices`; the code of `occupancy`, `space-settings` (its service's
exports), `spaces` (`spaces.service.ts`, its repository's `lock`, `hours.repository.ts`,
`prices.repository.ts`, `publicListing.service.ts`), `packages` (service, routes, controller), `directory`
(service, routes, controller), `shared/auth` (`can.ts`, `spaceAccess.ts`, the index), `shared/audit`,
`shared/errors/errorHandler.ts`, `shared/http/sendSuccess.ts`, `db/` (`transaction.ts`, the violation
helpers), `config/env.ts`, `app.ts`, `server.ts`, `apps/api/.env.example`; the tests' helpers
(`test/app.ts`, `factories.ts`, `locks.ts`, `spaces.ts` signatures) and `occupancy.api.test.ts`,
`db/payments.api.test.ts` (their patterns); `packages/shared` (its folders, `core/errors.ts`,
`core/envelope.ts`, `package.json`); `eslint.config.js` (the level map); `package-lock.json` (`@date-fns/tz`
1.5.0 and `date-fns` 4.4.0 already locked through the web); worker A's USERS plan (§7, its files);
`C:\dev\masaha\workspace\WORKER_B\_DONE\SETTINGS\{2_PLAN,3_EXEC_PROMPT}.md` (the procedure and the stop rule).

---

## 4. The prompt's settled decisions, as they will be built

### O1 — three PRs, in sequence
As §1. Each PR is cut from `origin/main` after the previous one merged; each has its own report
`4_REPORT_PR<n>.md` and its own executor conversation. A better cut is only proposed (*Proposed
alternatives* A1, A5).

### O2 — the scheduler (ADR 0014)
- **The endpoint:** `POST /api/v1/internal/jobs/run`, mounted only when `JOBS_SECRET` is set, after the
  general limit (it carries no access token, so it counts under the general guest limit by address, 1,200 /
  15 min — 12 calls an hour use almost none of it; no limit of its own: a 32-character random secret is not
  guessed, and a refusal costs one digest).
- **Its auth:** `Authorization: Bearer <JOBS_SECRET>`, compared in constant time (`timingSafeEqual` on the
  two SHA-256 digests, so the lengths match); a missing or wrong secret is `unauthorized` (401), no code, and
  runs nothing. The header is redacted from the request log already (security › HTTP hardening).
- **The env var:** `JOBS_SECRET`, at least 32 characters when set; **required in production**
  (`config/env.ts`'s production list); absent locally by default (the endpoint is then not mounted: 404).
- **Its rate:** a free external cron service (the runbook names cron-job.org as an example) calls it
  **every 5 minutes**. Locally, `server.ts` starts an in-process timer: the same run 10 s after start, then
  every 5 minutes, a tick skipped while a run is in flight, `unref()`'d so it never holds the process.
- **What a run does:** each registered job in turn (today one, `autoCheckOut`); a job that throws is logged
  and the others still run. The answer: 200 `{ ranAt, jobs: [{ name, done }] }` when every job ran, 500
  (the envelope, `server`) when one failed, so the cron service shows the failure.
- **Its logging:** one `info` line per job run — `{ job, ...done, ms }`, `'job ran'`; one `error` line with
  `err` and `job` for a failed one. The request's own line as every request's.
- **Idempotent and catching up:** each stay is closed in its own small transaction under its row's lock,
  only while still open; a run closes every stay whose due time has passed, however long since the last run,
  up to 500 per job per run (`remaining` is reported; the next run continues).
- **Closed at its due time:** `checkedOutAt` = the due time (the closing, or the end of the stay limit),
  never the run's time; the visit's charge is computed for the stay up to that time.
- **The deployment documents gain** (PR 3): `docs/development/setup.md` › *The API* gains *Timed jobs*, the
  runbook line: *"Online, set `JOBS_SECRET` (a random value of at least 32 characters) in the host's
  settings, and create one job on a free external cron service (for example cron-job.org): `POST
  https://<host>/api/v1/internal/jobs/run` every 5 minutes, with the header `Authorization: Bearer
  <JOBS_SECRET>`. A failed run answers 500, which the service shows; a missed run is caught up by the next."*;
  `apps/api/.env.example` gains `JOBS_SECRET=` with its comment; conventions §12's *Scheduler* row names the
  endpoint and the variable; ADR 0014 is unchanged (its decision stands).

### O3 — the override ends by itself, at the next closing at the latest
`until = min(now + duration, today's closing)`, `UNTIL_CLOSING` = today's closing. It is refused while
the space is not open by its hours (outside today's range, a closed day, or no hours at all: 409
`SPACE_NOT_OPEN`), so no override is ever stored past its day. Staff clear it early (`DELETE`). The rule
counts an override only while `until > now` (data model, *Live status* 3) — expiry is derived, no job.

### O4 — the shared desk device: not here
Nothing in this plan signs out idle reception accounts or switches staff. `OPEN_DECISIONS.md` point 4 stays
open for step 9.

### O5 — the unpaid visit's customer: the minimum
`customers` gains `findOrCreateByPhone`: the space's customer with that phone among those not archived,
else a new one named by `customerName` (or the visit's name), audited `customer.created`. The visit's charge
then counts in that customer's debt by the data model's rule; no debt read is built (step 8/9).

### O6 — Claude Code throughout
Executor and reviewer are Claude Code conversations (Appendix B).

### Q4 (settled) — the unpriced close (PR 3)
With the switch off (or, generally, whoever may not type a price) and no rate at all, the visit closes
**unpriced**: `chargeAgorot` null, `checkoutMethod` `MANUAL`, no payment (a payment on it is the trigger's
`payments_visit_uncharged` → 409 `VISIT_NOT_PRICED`). A phone is required, as for any visit left unpaid, so
the debt has a customer once priced. It is listed by `GET …/unpriced-visits` and priced by `PUT
…/visits/:visitId/charge`. Whoever may type a price must type it (422 `required` on `charge`), so the
unpriced path is the switch's consequence only. **Until PR 3 merges**, PR 2 answers that case — reception
without the switch, a visit with no rate, whether a charge is typed or not — with 403
`PRICE_TYPING_NOT_ALLOWED`, writing nothing (PR 2's T24 covers both bodies); PR 3 turns the untyped one into
the unpriced close (alternative A1 removes the interim).

### The plan's own decisions (inside the agreed item)

- **P1 — the modules.** Per conventions §7: `visits` (L3) owns `visits`; `subscriptions` (L3) `check_ins`;
  `customers` (L2) `customers`; `announcements` (L2) `announcements`; `payments` (L4) `payments`; `desk`
  (L5) orchestrates. PR 1 creates `visits`, `subscriptions`, `customers` and `announcements` with **only
  the reads `occupancy` needs** (R1: only the owner reads its table through its repository); each grows in
  its own step. *Why:* the one definition of *present* reads two tables owned by two L3 modules.
- **P2 — the staff's read is one request** (K8): `GET …/occupancy` answers the status, the capacity, the
  count and the people present, whole (an exception of api-contract §4: bounded by the people present).
  *Why:* the desk's main view on a weak connection; the planned `{ capacity, present }` plus `?open=true`
  lists would be three requests.
- **P3 — staff reads ask no `requireCan`;** the boundary (`space.read`, staff) is that check (#86's
  decision). Every write asks `requireCan` before its body is read, and `can()` again under the space's lock.
- **P4 — desk writes take the space's lock** (`spaces.lock`, `FOR NO KEY UPDATE`) and decide `can()` on
  `linksUnder(tx)` (finding 43's pattern). *Why:* a reception link ended meanwhile must refuse; the lock also
  serializes a space's desk creates, which makes the idempotency pre-check race-free (S1). The order: the
  space's row, then the visit's row (`FOR UPDATE`, the trigger's own mode), then the customer, then the
  payment. The auto check-out takes only a visit's or a check-in's row, so no two orders cross.
- **P5 — the time is the one clock's** (conventions §11): `checkedInAt`, `checkedOutAt`, `receivedAt`, an
  override's `until` come from the injected clock, never the database's `now()`.
- **P6 — the check-out is priced at the desk's quote** (PR 2). `checkedOutAt` may be sent: the time of the
  quote the desk showed (`GET …/visits/:visitId`'s `quote.at`), at most 10 minutes old and not in the
  future, else 422 `out_of_range`; absent, now. *Why:* with per-minute rounding the charge changes every
  minute; a visitor who paid what the screen said must not owe a few agorot more by the time the request
  lands, and a refusal-and-retry loop would be worse.
- **P7 — rounding details** (PR 2; data model *Visit charge* gains them; §13 Q3): billed minutes are the
  stay's whole minutes, at least 1; `UP_AFTER_MINUTES` N: whole hours, plus one when **more than** N
  minutes of the started hour passed, at least one hour (the prototype's `visitCharge`); `NEAREST_HALF_HOUR`:
  half hours rounded to the nearest, a quarter rounding up, at least one, × half the hour rate;
  `PER_MINUTE`: minutes × the hour rate / 60; every fraction of an agora rounded half up; the cap
  `min(charge, day rate)` when on and a day rate exists (`capApplied` = the cap cut it); no hour rate → the
  day rate, rounding fields `null`; neither → no charge (typed, or unpriced in PR 3).
- **P8 — the visit's rates** (PR 2): from the space's prices with no label: for each period (`HOUR`,
  `DAY`) apart, the audience's price in the visit's shift, else the general one in that shift; and for a
  visit with no shift, the prices with no shift. **A visit in a shift whose shift has no price** falls back
  to the prices with no shift, period by period (§13 Q4 — a rule the data model does not state yet).
  `STUDENT` is refused (422 `invalid_choice` on `audience`) where `visitStudentPrices` is off.
- **P9 — warnings** (PR 2): `meta.warnings`, a list of `SPACE_FULL` (present ≥ capacity before this
  check-in; none without a capacity) and `OUTSIDE_OPENING_HOURS` (the space has hours and is not open by
  them now). A retry recomputes them as of now, counting the visit as already present (S3).
- **P10 — the occupancy read is several statements, without a lock.** *Why:* a live read; a check-in
  committing between two of them can make the count lag one stay for one answer, which the next poll fixes.
- **P11 — feature documents** (documentation §5): PR 1 updates `occupancy.md` and `directory.md`; PR 2
  writes `visits.md`, `desk.md` and `payments.md` (their first stable cores); PR 3 updates the three.
  `subscriptions`, `customers` and `announcements` hold one or two reads each, no stable core: no document
  yet; `occupancy.md` and `desk.md` name what they read.
- **P12 — idempotency keys are read from the `Idempotency-Key` header** by a route middleware in
  `shared/http` (`requireIdempotencyKey`): missing → 422 `required`, not a UUID → 422 `invalid_format`, on
  the field `idempotencyKey`; the controller reads it from `res.locals` (as the directory's list query).
  A key already used for a different record of the same kind is `conflict` (409), no code (a client bug).

### The code, PR by PR (interfaces; the commit in brackets)

#### PR 1 — `feat/live-status`

| Where | What |
|---|---|
| `package.json` (`apps/api`, `packages/shared`), `package-lock.json` | `"@date-fns/tz": "^1.5.0"` in each `dependencies` [C1] |
| `packages/shared/src/core/gazaTime.ts` (+ `.unit.test.ts`), `core/index.ts` | `GAZA_TIME_ZONE = 'Asia/Gaza'`; `interface GazaClock { date: string /* YYYY-MM-DD */; dayOfWeek: number /* 0 = Sunday */; minute: number /* 0–1439 */ }`; `gazaClockOf(instant: Date): GazaClock`; `gazaInstant(date: string, minute: number /* 0–1440; 1440 = the next day's 00:00 */): Date`. Through `TZDate`; never reads the clock [C1] |
| `packages/shared/src/occupancy/{requests,responses,index}.ts` (+ `requests.unit.test.ts`) | `LIVE_STATUSES = ['AVAILABLE','FULL','CLOSED']`, `LiveStatus`; `OVERRIDE_DURATIONS = ['MINUTES_30','HOUR_1','HOURS_2','UNTIL_CLOSING']`; `setStatusOverrideSchema = z.object({ state: z.enum(LIVE_STATUSES), duration: z.enum(OVERRIDE_DURATIONS) })` (each `invalid_choice` / `required` through `toFieldErrors`), `SetStatusOverrideRequest`; `PresentPerson = { kind: 'VISIT', id, name, since: string } \| { kind: 'CHECK_IN', id, customerId, name, since }`; `SpaceOccupancyNow = { status: LiveStatus \| null, capacity: number \| null, present: number, override: { state: LiveStatus, until: string } \| null, people: PresentPerson[] }`; `PublicOccupancy = { status: LiveStatus \| null }` [C2, C3; `PublicOccupancy` C4] |
| `packages/shared/src/core/errors.ts`; `apps/web/src/shared/copy/{arabic,english}/errors.ts` | `SPACE_NOT_OPEN` under `// occupancy` [C3] |
| `packages/shared/src/directory/{requests,responses}.ts` (+ `requests.unit.test.ts`) | `availableNow` in the filters the list and the map share, parsed as `openFriday` is (`true` only); `liveStatus: LiveStatus \| null` on `DirectorySpace` and `MapPin` [C4] |
| `apps/api/src/modules/occupancy/liveStatus.ts` (+ `.unit.test.ts`) | `type Week = readonly (OpeningRange \| null)[] \| null`; `interface Override { state: LiveStatus; until: Date }`; `interface LiveStatusInput { verified: boolean; closureNow: boolean; week: Week; at: GazaClock; now: Date; override: Override \| null; capacity: number \| null; present: number }`; `liveStatus(input): LiveStatus \| null` (data-model order); `openRangeAt(week, at): OpeningRange \| null` (the day's range when `opensMinute ≤ at.minute < closesMinute`); `isFull(present, capacity): boolean` (`capacity !== null && present >= capacity`) [C2] |
| `occupancy/overrideUntil.ts` (+ `.unit.test.ts`) | `overrideUntil(duration, now: Date, closesAt: Date): Date` = `UNTIL_CLOSING ? closesAt : min(now + 30/60/120 min, closesAt)` [C3] |
| `occupancy/occupancy.repository.ts` | + `stateOf(spaceId, tx?)` → `{ capacity, override: Override \| null, overrideById }`; `statesFor(spaceIds)` → `Map`; `setOverride(spaceId, { state, until, byId }, tx)` (upsert; creates the row with `capacity: null`; writes only the three override columns); `clearOverride(spaceId, tx)` (the three to `null`) [C2, C3] |
| `occupancy/occupancy.service.ts` | deps + `now: () => Date`, `visits`, `subscriptions`, `customers`, `announcements`; + `now(space: LoadedSpace): Promise<SpaceOccupancyNow>`; `setOverride(actor, space, request)`, `clearOverride(actor, space)` (both answer `SpaceOccupancyNow`); `liveStatusFor(spaces: readonly { id: number; verified: boolean; week?: Week }[]): Promise<Map<number, LiveStatus \| null>>`; `availableAmong(verifiedIds): Promise<number[]>` [C2–C4] |
| `occupancy/occupancy.controller.ts`, `occupancy.manage.routes.ts` | `GET /occupancy` (no `requireCan`, P3); `PUT /status-override` (`requireCan('space.liveStatus.override')`, `validate(setStatusOverrideSchema)`); `DELETE /status-override` (same `requireCan`) [C2, C3] |
| `apps/api/src/modules/visits/{index,visits.service,visits.repository}.ts` (new) | `createVisitsService()` → `openIn(spaceId, tx?)`: `{ id, visitorName, customerId, checkedInAt }[]`, oldest first then id; `openCountsIn(spaceIds)`: `Map<spaceId, number>` (`groupBy`, `checkedOutAt: null`) [C2] |
| `modules/subscriptions/{index,subscriptions.service,subscriptions.repository}.ts` (new) | `createSubscriptionsService()` → `openCheckInsIn(spaceId, tx?)`: `{ id, customerId, checkedInAt }[]`; `openCheckInCountsIn(spaceIds)` [C2] |
| `modules/customers/{index,customers.service,customers.repository}.ts` (new) | `createCustomersService(…)` → `namesOf(spaceId, ids, tx?)`: `Map<id, name>` [C2] |
| `modules/announcements/{index,announcements.service,announcements.repository}.ts` (new) | `createAnnouncementsService()` → `closedAt(spaceIds, now: Date): Promise<Set<number>>`: `type = CLOSURE`, `deletedAt` null, `startsAt ≤ now`, `endsAt` null or `> now` [C2] |
| `modules/spaces/spaces.service.ts` | + `weekOf(spaceId, tx?)`, `weeksFor(spaceIds, tx?)` (through `createHoursRepository`) [C2] |
| `modules/spaces/public/publicListing.{repository,service}.ts` | `PublicFilter` + `onlyIds?: readonly number[]` (narrows before the order and the page, as `verifiedIds` does) [C4] |
| `modules/directory/directory.{service,controller,routes}.ts` | deps + `occupancy`; `list` and `pins` add `liveStatus` (one `liveStatusFor` per answer, the rows' weeks passed in); `filterOf` adds `onlyIds = await occupancy.availableAmong(verifiedIds)` when `availableNow`; + `occupancy(slug): Promise<PublicOccupancy>` (not listed → 404, as `page`; verified from `spaceLinks.linksAt`); route `GET /spaces/:slug/occupancy`, `cachePublicly` [C4] |
| `apps/api/src/app.ts` | builds `visits`, `subscriptions`, `customers`, `announcements`; `occupancy` with them and `now: clock`; `directory` with `occupancy` [C2, C4] |

#### PR 2 — `feat/desk-visits`

| Where | What |
|---|---|
| `apps/api/prisma/schema.prisma`; migration `<ts>_desk_visit_charge` | `Visit.chargeReason String? @map("charge_reason")` (`/// Why the desk typed the charge; set with chargeSetById.`); the raw SQL of §12.2 (PR 2) [C1] |
| `apps/api/src/db/front-desk.api.test.ts`, `db/payments.api.test.ts` | the reason's `CHECK`; the uncharged visit's constraint renamed [C1] |
| `packages/shared/src/core/idempotencyKey.ts`, `core/envelope.ts`, `core/index.ts` | `IDEMPOTENCY_KEY_HEADER = 'Idempotency-Key'`, `idempotencyKeySchema = z.uuid()`; `WarningsMeta = { warnings: DomainErrorCode[] }` [C2] |
| `packages/shared/src/visits/{requests,responses,index}.ts` (+ `requests.unit.test.ts`) (new, L3) | `checkInVisitSchema = z.object({ visitorName: textSchema 1–60, audience: z.enum(PRICE_AUDIENCES).default('GENERAL'), shiftId: positive id, optional, nullable })`; `DeskVisit = { id, visitorName: string \| null, customer: { id, name, phone: string \| null } \| null, audience, shiftId: number \| null, hourRateAgorot: number \| null, dayRateAgorot: number \| null, checkedInAt: string, checkedOutAt: string \| null, checkoutMethod: 'MANUAL' \| 'AUTO' \| null, charge: VisitCharge \| null }`; `VisitCharge = { amountAgorot, roundingRule: VisitRounding \| null, roundingMinutes: number \| null, capApplied: boolean \| null, typedById: number \| null, reason: string \| null }`; `VisitQuote = { at: string, chargeAgorot: number \| null, billedMinutes: number, capApplied: boolean \| null }`; `QuotedVisit = DeskVisit & { quote: VisitQuote \| null }`; `VisitTerms = { rounding: { rule: VisitRounding, minutes: number \| null }, capAtDayPrice: boolean, mayTypePrice: boolean, rates: { shiftId: number \| null, general: Rates, student: Rates \| null }[] }`, `Rates = { hourAgorot: number \| null, dayAgorot: number \| null }` [C2, C3, C4] |
| `packages/shared/src/payments/{requests,responses,index}.ts` (new, L4) | `PAYMENT_METHODS = ['CASH','TRANSFER']`; `paymentSchema = z.object({ amountAgorot: whole 1–10,000,000, method: z.enum(PAYMENT_METHODS), note: textSchema 1–200, optional })`; `VisitPayment = { id, amountAgorot, method, note: string \| null, receivedAt: string, recordedById: number }` [C3] |
| `packages/shared/src/desk/{requests,responses,index}.ts` (new, L5) | `checkOutVisitSchema = z.object({ checkedOutAt: ISO datetime, optional; payment: paymentSchema.nullable().optional(); phone: phoneSchema, optional; customerName: textSchema 1–60, optional; charge: z.object({ amountAgorot: whole 1–10,000,000, reason: textSchema 1–200 }).optional() })`; `VisitCheckOut = { visit: DeskVisit, payment: VisitPayment \| null }`; `DESK_WARNINGS = ['SPACE_FULL','OUTSIDE_OPENING_HOURS']` [C2, C3] |
| `packages/shared/src/core/errors.ts`; the two `errors.ts` catalogues | `SPACE_FULL` (C2); `PAYMENT_EXCEEDS_DUE`, `PRICE_TYPING_NOT_ALLOWED` (C3) |
| `apps/api/src/shared/http/idempotencyKey.ts`, `http/index.ts`, `http/sendSuccess.ts` | `requireIdempotencyKey: RequestHandler` (P12), `idempotencyKeyOf(res): string`; `SuccessOptions.meta?: PaginationMeta \| WarningsMeta` [C2] |
| `apps/api/src/shared/auth/can.ts` (+ `can.unit.test.ts`), `index.ts` | rule `'ownerOrAllowedReception'` with `PriceTypingResource = SpaceResource & { receptionMayTypePrices: boolean }`: the space's `OWNER`, or its `RECEPTION` when the switch is on; action `'prices.typeByHand'` [C3] |
| `apps/api/src/db/checkViolation.ts`, `db/index.ts`; `shared/errors/constraintCodes.ts`, `errorHandler.ts` | `checkViolationOf(error): string \| null` (the constraint a check violation names, from Prisma's error — §12.2 check 2); `CONSTRAINT_CODES = { payments_within_due: { type: 'conflict', code: 'PAYMENT_EXCEEDS_DUE' } }`; `toAppError` maps a named constraint through it, before the generic `server` [C3] |
| `modules/visits/visitCharge.ts` (+ `.unit.test.ts`) | `ratesFor(prices: readonly Price[], visit: { audience; shiftId: number \| null; studentPrices: boolean }): Rates` (P8); `chargeOf(stay: { from: Date; to: Date }, rates: Rates, rule: { rounding: VisitRounding; roundingMinutes: number \| null; capAtDayPrice: boolean }): Charge \| null` with `Charge = { amountAgorot, billedMinutes, roundingRule, roundingMinutes, capApplied }` (P7) [C3] |
| `modules/visits/visits.{service,repository,mapper}.ts`, `visits.controller.ts`, `visits.manage.routes.ts` | deps `{ spaces, spaceSettings, customers, now }`; `findByKey(spaceId, key, tx)`; `create(tx, { spaceId, key, visitorName, audience, shiftId, rates, checkedInAt })` (a foreign-key refusal on the shift → 422 `invalid_choice` on `shiftId`); `lockIn(spaceId, visitId, tx)` (`FOR UPDATE`; `null` when not the space's); `close(tx, visitId, { checkedOutAt, method, charge, typedById, reason, customerId })`; `ratesAt(spaceId, request, tx)`; `quoteOf(visit, at)`; `quote(spaceId, visitId): Promise<QuotedVisit>`; `terms(actor, space): Promise<VisitTerms>`; `chargesNow(spaceId, visitIds): Promise<Map<id, number \| null>>`; routes `GET /visits/:visitId`, `GET /visit-terms` [C2–C4] |
| `modules/space-settings/space-settings.service.ts` | `read(spaceId, tx?)` takes an optional `tx` (the desk reads the settings in its transaction) [C2] |
| `modules/spaces/spaces.service.ts` | + `pricesOf(spaceId, tx?)` (through `createPricesRepository`) [C2] |
| `modules/customers/customers.{service,repository}.ts` | deps `{ audit }`; + `findOrCreateByPhone(tx, { spaceId, phone, name, actorId }): Promise<{ id, name, phone }>` (audited `customer.created`, `after: { name, phone }`, when created) [C3] |
| `modules/payments/{index,payments.service,payments.repository,payments.mapper}.ts` (new, L4) | deps `{ audit }`; `findByKey(spaceId, key, tx)`; `recordForVisit(tx, { spaceId, visitId, key, amountAgorot, method, note, recordedById, receivedAt }): Promise<VisitPayment>` (audited `payment.recorded`, entity `payment`, `after: { visitId, amountAgorot, method }`) — no ledger rule repeated [C3] |
| `modules/occupancy/occupancy.service.ts` | + `checkInWarnings(spaceId, now, tx): Promise<DomainErrorCode[]>` (P9); the read's `VISIT` people gain `chargeNowAgorot` through `visits.chargesNow` [C2, C4] |
| `modules/desk/{index,desk.service,desk.controller,desk.manage.routes}.ts` (new, L5) | deps `{ runInTransaction, spaces, spaceSettings, visits, customers, payments, occupancy, now }`; `checkInVisit(actor, space, key, request): Promise<{ visit: DeskVisit; warnings: DomainErrorCode[] }>`; `checkOutVisit(actor, space, visitId, key, request): Promise<VisitCheckOut>`; routes `POST /visits` and `POST /visits/:visitId/check-out`, each `requireCan('attendance.record')` → `requireIdempotencyKey` → `validate` [C2, C3] |
| `apps/api/src/app.ts` | builds `payments`, `desk`; mounts `desk`'s and `visits`' manage routers [C2–C4] |

#### PR 3 — `feat/auto-checkout`

| Where | What |
|---|---|
| `modules/spaces/autoCheckout.ts` (+ `.unit.test.ts`), `spaces.service.ts` | `autoCheckoutDue({ checkedInAt: Date; week: Week; autoCheckoutAtClosing: boolean; maxStayMinutes: number \| null }): Date \| null` (§ D-PR3-1); `SpacesService.autoCheckoutDue` passes it through [C1] |
| `modules/space-settings/space-settings.service.ts` | + `settingsFor(spaceIds, tx?)`: `Map<spaceId, SpaceSettings>` [C2] |
| `apps/api/src/shared/jobs/{index,jobs,timer,jobs.routes,secret}.ts` (new) | `interface Job { name: string; run(now: Date): Promise<Record<string, number>> }`; `createJobs({ jobs, now, logger }): { run(): Promise<JobsRun> }`, `JobsRun = { ranAt: string; jobs: { name: string; done: Record<string, number> \| null }[]; failed: boolean }`; `startEvery(ms, run, logger): () => void` (first run after 10 s, a tick skipped while one runs, `unref`); `matchesSecret(header: string \| undefined, secret: string): boolean`; `createJobsRouter(jobs, secret): Router` (`POST /run`) [C2] |
| `apps/api/src/config/env.ts` (+ `env.unit.test.ts`), `apps/api/.env.example` | `JOBS_SECRET`: optional, at least 32 characters when set, required in production [C2] |
| `apps/api/src/app.ts`, `server.ts` | `ApiOptions` + `jobsSecret?: string`, `startJobs?: (run: () => Promise<unknown>) => void`; `createApi` registers `autoCheckOut` (`visits.autoCheckOut`, then `subscriptions.autoCheckOut`), mounts `/internal/jobs` when `jobsSecret` is set (after the general limit), calls `startJobs?.(run)`; `createAppFromEnv(env, { logger, checkDatabase, startJobs? })` passes `env.JOBS_SECRET`; `server.ts` passes `startJobs: (run) => startEvery(FIVE_MINUTES, run, logger)` [C2] |
| `modules/visits/visits.{service,repository}.ts` | + `autoCheckOut(now: Date): Promise<{ visits: number; remaining: number }>` (D-PR3-2); C3: + `unpricedIn(spaceId, page)`, `price(actor, space, visitId, request)`; route `GET /unpriced-visits`, `PUT /visits/:visitId/charge` [C2, C3] |
| `modules/subscriptions/subscriptions.{service,repository}.ts` | + `autoCheckOut(now): Promise<{ checkIns: number; remaining: number }>`; deps `{ spaces, spaceSettings, audit }` [C2] |
| `modules/desk/desk.service.ts` | the check-out's unpriced branch (Q4) [C3] |
| `packages/shared/src/visits/requests.ts` | `priceVisitSchema = z.object({ amountAgorot: whole 1–10,000,000, reason: textSchema 1–200 })` [C3] |
| `packages/shared/src/payments/responses.ts` | `UncollectedVisit = { visit: DeskVisit, paidAgorot: number, balanceAgorot: number \| null }` [C4] |
| `shared/errors/constraintCodes.ts`; `core/errors.ts`; the catalogues | `payments_visit_uncharged → { type: 'conflict', code: 'VISIT_NOT_PRICED' }`; `VISIT_NOT_PRICED`, `VISIT_ALREADY_PRICED` [C3] |
| `modules/payments/payments.{service,repository,controller,manage.routes}.ts` | deps + `visits`; `uncollectedIn(spaceId, page): Promise<{ rows: UncollectedVisit[]; total: number }>` (D-PR3-4); route `GET /uncollected-visits` [C4] |

### Decisions taken for PR 3 (with the reason)

- **D-PR3-1 — the due time.** On the check-in's Gaza date: with `autoCheckoutAtClosing` on, the day's
  closing when the check-in fell before it (a range `closesMinute` of 1,440 counts as 23:59); **23:59**
  when the space has no hours at all (the data model), **and also on a closed day or after that day's
  closing** (§13 Q5 — the data model is silent); with it off, none. With `maxStayMinutes`, also
  `checkedInAt + maxStayMinutes`; the earlier of the two wins. Never before `checkedInAt`. *Why:* a stay never
  crosses into the next Gaza day, as v1's hours never do (spaces F4).
- **D-PR3-2 — the job's order and batch.** All open visits (then check-ins) of every space, oldest first
  then id (conventions §13's order), the current week and settings of their spaces (two set-based reads),
  the due time of each; those due at or before `now`, up to 500, each closed in its own transaction: the
  row `FOR UPDATE`, still open, `checkedOutAt = due`, `checkoutMethod = AUTO`, the charge `chargeOf({ from:
  checkedInAt, to: due }, the visit's rates, the settings now)` (or none without a rate), audited
  `visit.autoCheckedOut` (`checkIn.autoCheckedOut`) with `actorId: null`, `after: { checkedOutAt,
  chargeAgorot }`. A soft-deleted or hidden space's stays are closed too. *Why:* one failure must not undo
  the others; a manual check-out meanwhile wins by the row lock.
- **D-PR3-3 — "a change applies from then on":** the job reads the week and the settings at the run, so a
  shorter stay limit or the closing check-out turned on closes open stays at their new due time — possibly
  in the past (data model, 2026-10-19, #92).
- **D-PR3-4 — uncollected, composed without repeating the balance** (conventions §5, §9): `visits` gives
  the ids of the space's visits closed `AUTO`; `payments` sums their non-voided payments (one grouped query)
  and, with each one's charge from `visits`, computes the balance by its own pure rule
  (`payments/balance.ts`: `due − paid`) and the settled ids (balance ≤ 0); `visits` then lists the space's
  `AUTO`-closed visits not among them, newest closed first then id, and pages (the unpriced ones included:
  no due, never settled). *Cost:* three queries over the space's auto-closed visits; fine at v1's scale
  (Review Focus).
- **D-PR3-5 — pricing a visit** (`PUT …/visits/:visitId/charge`): under the space's lock, `can(actor,
  'prices.typeByHand', { links: linksUnder(tx), receptionMayTypePrices })`, the visit `FOR UPDATE`; a visit
  not the space's → 404; an open one → 409 (no code: it is priced at its check-out); one with a charge →
  409 `VISIT_ALREADY_PRICED`; else `chargeAgorot`, `chargeSetById`, `chargeReason` set, rounding fields
  `null`, audited `visit.priced` (`after: { chargeAgorot, reason }`).

---

## 5. Stronger decisions

### S1 — the idempotency key is checked first, under the space's lock — **needed, planned**
Conventions §13 says the unique violation on the key "is caught by the service, which returns the record
that already exists". Inside an interactive transaction PostgreSQL aborts the transaction on that violation,
so the service cannot read the existing row in it. The plan reads the record by `(spaceId, key)` first, under
the space's lock (P4), which serializes the space's desk creates, so the read is race-free; the unique key
stays the backstop (a violation would then be a bug, answered 500). *Cost:* conventions §13's sentence
rewritten (PR 2); the race test T-PR2-8 proves two same-key requests at once make one row. **Recommended.**

### S2 — finding 15 by a new constraint name, not by unreachability — **recommended, planned**
The finding allows either. The PR 2 migration replaces `payments_guard_insert` so an uncharged visit raises
`payments_visit_uncharged`: step 9's general payment route will reach it, and only a name of its own maps to
its own code. *Cost:* one `CREATE OR REPLACE FUNCTION` in the migration; the db test's expectation changes.

### S3 — a retried check-in recomputes its warnings — **weakens ADR 0015's "same body", stated**
ADR 0015: a retry returns "the same status and body". The warnings describe *now*, not the record; storing
them would add a column for advice. A retry returns the same visit and 201, with the warnings as of the
retry (the visit counted as present). *Alternative:* store the warnings on the visit. **Recommended as
planned**; §13 Q8.

### S4 — the hand-typed rule lives in `can()` — **recommended, planned**
`can()` gains a rule that reads the setting from its resource (`PriceTypingResource`), so who may type a
price has one home with every other permission, and its six-actor unit test (ADR 0009's consequence) covers
it with the switch on and off. *Alternative:* the desk's service compares the role and the switch.

### S5 — the check-out's quote time (P6) — **recommended, planned**
Stronger money correctness than "now" at the request; bounded to 10 minutes, so it cannot back-date a stay.

### S6 — the override refused while the space is not open — **recommended, planned**
The data model counts an override only "while the space is open by its hours"; storing one outside them would
be a silent no-op. A refusal with `SPACE_NOT_OPEN` tells the desk why (and keeps O3's "no override outlives
its day").

### Rules the item touches, stated
- **ADR 0008** keeps `GET /spaces/:slug/occupancy` → `{ status }`; the card and the pin carry the state too,
  never a count. Its *Consequences* line on `SPACE_CAPACITY_NOT_SET` is untouched: no endpoint answers it yet.
- **Conventions §9:** "auto check-out: `visits` and `subscriptions` each close their own records; the
  cut-off is a pure function in `spaces`; the timer is `shared/jobs`, wired in the composition root" — built
  as written.
- **Conventions §11:** the library is `@date-fns/tz` alone; `date-fns` is not needed (conventions §11's line
  corrected in PR 1).
- **The level map** is unchanged: every module this plan creates is already placed.

---

## 6. Related findings

| Finding | Folded? | Why, and the cost |
|---|---|---|
| **15** The payments migration predates ADR 0015 | **Yes, PR 2** (the build map's *Closes*) | S2: a new constraint name, the translation table's first lines, the trigger reached through the check-out. Status → Resolved, resolution line, index moved [PR 2 C3] |
| **17** Expired counters and abandoned sessions never swept | No | It names the scheduler port, which PR 3 builds; the sweep is a second job over `sessions` and `shared/rate-limit`, each with its own expiry rules and tests (≈ 8 files). Proposed as a small item right after PR 3 (alternative A4) |
| **23** No per-address ceiling for signed-in requests | No | Untouched: the desk's polling stays within 300 / 15 min per user; the jobs endpoint carries no token (guest limit) |
| **52** The race tests wait a fixed time | Resolved | Every new race test acts once its request waits on a lock (`whileHeld`, `waitingOnLock`) |
| **77** The race helper counts any waiting backend | No | The new races use `whileHeld` as the existing ones do; one test file runs at a time against its own database. Folding it changes `test/locks.ts` and the lane's timeout for every race (its own item) |
| **96** The attendance card saves two capabilities | No | Screen 24's |
| **97** The visit-rounding rule is written twice | No | It is about the settings' validation (step 11); this plan's charge rule reads the stored rule, adding no third copy |

No new finding is planned. One met while working is recorded with `<n>`, its own file and its index line,
in the commit where it is found.

---

## 7. The files it edits

Only `apps/api`, `packages/shared`, `docs`, `package.json`/`package-lock.json` (PR 1's dependency), and,
under worker B's licence (workflow §9), the error codes' lines in
`apps/web/src/shared/copy/{arabic,english}/errors.ts`. **Shared with worker A's USERS:**
`docs/project/overview.md` (*Built*: each side its own line) — a likely text conflict, the documents' fast
path; the findings index only if a finding is recorded. No code file is shared.

| PR | Code (new +) | Documents |
|---|---|---|
| 1 | `apps/api/package.json`, `packages/shared/package.json`, `package-lock.json`; shared: + `core/gazaTime.ts` (+ test), `core/index.ts`, `core/errors.ts`, `occupancy/{requests,responses,index}.ts`, `occupancy/requests.unit.test.ts`, `directory/{requests,responses}.ts`, `directory/requests.unit.test.ts`; web: 2 catalogues; api: `occupancy/` + `liveStatus.ts` (+ test), + `overrideUntil.ts` (+ test), `occupancy.{service,repository,controller,manage.routes}.ts`, `occupancy.api.test.ts`, + `present.api.test.ts`, + `override.api.test.ts`; + `visits/{index,visits.service,visits.repository}.ts`; + `subscriptions/{…}` (3); + `customers/{…}` (3); + `announcements/{…}` (3); `spaces/spaces.service.ts`, `spaces/public/publicListing.{repository,service}.ts`; `directory/directory.{service,controller,routes}.ts`, + `directory/liveStatus.api.test.ts`; `app.ts` | `api-contract.md`, `data-model.md`, `conventions.md`, `security.md`, `features/occupancy.md`, `features/directory.md`, `docs/README.md` (map line), `plans/v1-mvp.md`, `project/overview.md` — ≈ 58 |
| 2 | `schema.prisma`, + migration; `db/front-desk.api.test.ts`, `db/payments.api.test.ts`, + `db/checkViolation.ts`, `db/index.ts`; shared: + `core/idempotencyKey.ts`, `core/envelope.ts`, `core/index.ts`, `core/errors.ts`, + `visits/{requests,responses,index}.ts` (+ test), + `payments/{requests,responses,index}.ts`, + `desk/{requests,responses,index}.ts` (+ test); web: 2 catalogues; api: + `shared/http/idempotencyKey.ts`, `http/index.ts`, `http/sendSuccess.ts`, `shared/auth/{can,can.unit.test,index}.ts`, + `shared/errors/constraintCodes.ts`, `errors/errorHandler.ts`, `errors/index.ts`; `visits/` + `visitCharge.ts` (+ test), `visits.{service,repository}.ts`, + `visits.{mapper,controller,manage.routes}.ts`, `index.ts`, + `visits.api.test.ts`; `customers.{service,repository}.ts`, `customers/index.ts`; + `payments/{index,payments.service,payments.repository,payments.mapper}.ts`; + `desk/{index,desk.service,desk.controller,desk.manage.routes}.ts`, + `desk/checkIn.api.test.ts`, + `desk/checkOut.api.test.ts`; `occupancy/occupancy.service.ts`, `present.api.test.ts`; `space-settings/space-settings.service.ts`; `spaces/spaces.service.ts`; `app.ts` | `api-contract.md`, `data-model.md`, `conventions.md`, `security.md`, + `features/{visits,desk,payments}.md`, `features/occupancy.md`, `docs/README.md`, `plans/v1-mvp.md`, `project/overview.md`, finding 15 + index — ≈ 52 + the docs |
| 3 | `spaces/` + `autoCheckout.ts` (+ test), `spaces.service.ts`; `space-settings/space-settings.service.ts`; + `shared/jobs/{index,jobs,timer,jobs.routes,secret}.ts`, + `shared/jobs/secret.unit.test.ts`; `config/env.ts` (+ test), `.env.example`; `app.ts`, `server.ts`; `visits/visits.{service,repository,controller,manage.routes}.ts`, + `visits/autoCheckOut.api.test.ts`, + `visits/unpriced.api.test.ts`; `subscriptions/subscriptions.{service,repository}.ts`, `subscriptions/index.ts`; `desk/desk.service.ts`, `desk/checkOut.api.test.ts`; `payments/` + `balance.ts` (+ test), `payments.{service,repository}.ts`, + `payments.{controller,manage.routes}.ts`, `index.ts`, + `uncollected.api.test.ts`; + `shared/jobs/jobs.api.test.ts`; shared: `visits/requests.ts`, `payments/responses.ts`, `core/errors.ts`; `shared/errors/constraintCodes.ts`; web: 2 catalogues | `api-contract.md`, `data-model.md`, `conventions.md`, `security.md`, `development/setup.md`, `features/{visits,desk,payments}.md`, `plans/v1-mvp.md`, `project/overview.md`, `OPEN_DECISIONS.md` (outside the repository, by the report) — ≈ 44 |

---

## 8. Design issues

None: no screen is built or changed. The design decisions this API serves are named where they bind (K2,
K8, DI-41, DK-021, DK-023, O3); K6 and DK-012 are raised in *Proposed alternatives* A3.

---

## 9. Tests — lane, title, the break each catches

Every test is seen failing first in its own lane (testing §3 rule 5); every expectation is written by hand.
Tests on time use a fixed clock through `createTestApp({ clock })`. Gaza is UTC+2 in winter and UTC+3 in
summer: each test states its instants with their offset (as `stay()` does). Roles in every API file: the
owner, reception of this space, a stranger, an owner of another space, the admin (testing §4).

### PR 1

**Unit — `packages/shared/src/core/gazaTime.unit.test.ts`** [C1]
- U1 `reads a winter and a summer instant as Gaza's date, weekday and minute` — break: the zone `UTC`.
- U2 `turns a Gaza date and minute into the instant, on both sides of a daylight-saving change` (the
  transition pinned by §12.2 check 2) — break: a fixed `+02:00` offset.
- U3 `reads minute 1440 as the next day's midnight` — break: `minute % 1440`.

**Unit — `apps/api/src/modules/occupancy/liveStatus.unit.test.ts`** [C2]
- U4 `an unverified space has no live state, even under a closure or an override`
- U5 `an active closure makes it CLOSED, over an override and within its hours` (and an ended or
  not-yet-started closure does not — the service decides `closureNow`; this proves the order only)
- U6 `outside today's hours it is CLOSED: before opening, at the closing minute, on a closed day`
- U7 `an override in force gives its state while open, even without a capacity`
- U8 `an override whose end has passed counts for nothing`
- U9 `without any hours there is no live state, an override included`
- U10 `open without a capacity has no live state`
- U11 `present equal to capacity is FULL; one below is AVAILABLE`
- U12 `a day open 0–1440 is open at 23:59`
- Breaks: each branch removed or two swapped (B1–B6).

**Unit — `occupancy/overrideUntil.unit.test.ts`** [C3]
- U13 `each duration ends after its time, or at closing when closing comes first`; `until closing ends at
  closing` — break: no `min` (B7).

**Unit — `packages/shared/src/occupancy/requests.unit.test.ts`** [C3]
- U14 `an override takes one of the three states and one of the four durations` (`invalid_choice`,
  `required`) — break: `z.string()` for the state (B8).

**Unit — `packages/shared/src/directory/requests.unit.test.ts`** [C4]
- U15 `availableNow takes true only` (`invalid_choice` / `invalid_format` as `openFriday` answers) — break:
  `z.coerce.boolean()` (B9).

**API — `apps/api/src/modules/occupancy/present.api.test.ts`** [C2]
- T1 `answers the owner and reception the status, the capacity, the count and the people present` — break:
  `requireCan('space.capacity.manage')` on `GET /occupancy` (B10).
- T2 `answers not_found to a stranger, an owner of another space and the admin` — break: the router mounted
  outside `manage` (B11).
- T3 `counts open visits and open subscription check-ins, never closed ones or another space's` — breaks:
  `checkedOutAt` filter dropped in `visits.openCountsIn`/`openIn` (B12); in `subscriptions` (B13).
- T4 `lists the people present oldest first, a check-in by its customer's name` — break: order by id
  desc (B14).
- T5 `reads the status from the hours, the capacity and the override` (FULL at capacity; CLOSED outside
  hours; an override's state; `null` without a capacity) — break: `present` passed as 0 (B15).
- T6 `a CLOSURE announcement in force closes it; a deleted, ended or other-type one does not` — break:
  `deletedAt` filter dropped (B16); `type` filter dropped (B17).

**API — `apps/api/src/modules/occupancy/override.api.test.ts`** [C3]
- T7 `the owner and reception set an override for 30 minutes, ending at now + 30 min, audited` (fixed clock,
  `space.statusOverridden`, `after: { state, until }`) — break: `until` from `now()` of the database (B18).
- T8 `an override asked for 2 hours ends at today's closing when closing is sooner`
- T9 `a new override replaces the one in force, audited with both` (`before` / `after`)
- T10 `refuses an override while the space is not open by its hours, or has none: 409 SPACE_NOT_OPEN,
  writing nothing` — break: the open check removed (B19).
- T11 `clears the override in force, audited space.statusOverrideCleared; clearing none writes nothing` —
  break: the "in force" check removed (B20).
- T12 `refuses a stranger, an owner of another space and the admin with not_found, on both routes`
- T13 `refuses an invalid body with 422 before anything is written` — break: `validate` removed (B21).
- T14 `the first override creates the occupancy row with no capacity; it never touches a capacity` —
  break: `setOverride`'s upsert writes `capacity: null` on update (B22).
- T15 `a reception link deactivated while the override waits on the space's lock refuses it with 403`
  (`whileHeld`: the test locks the space, then deactivates the link) — break: `can()` on `space.links`
  (B23).

**API — `apps/api/src/modules/occupancy/occupancy.api.test.ts`** [C3]
- T16 (new beside the capacity's tests) `setting the capacity keeps an override in force` — break: the
  capacity's upsert also nulls the override's columns (B24).

**API — `apps/api/src/modules/directory/liveStatus.api.test.ts`** [C4]
- T17 `every card and pin carries its live status; an unverified space's is null` — break: `liveStatus`
  set `null` for all (B25).
- T18 `no public answer carries a capacity, a count or an override` (the card's, the pin's, the page's and
  `/occupancy`'s keys exactly) — break: `present` added to `PublicOccupancy`'s answer (B26).
- T19 `availableNow keeps only AVAILABLE spaces, before the page is cut: every page full, the total right`
  (FULL, CLOSED, unverified and no-capacity spaces left out; `limit=1`, two pages) — break: the filter
  applied to the page after it is fetched (B27).
- T20 `availableNow on the map keeps the same spaces`
- T21 `GET /spaces/:slug/occupancy answers { status } for a listed space, with the public cache; 404 for a
  hidden, deleted or unknown one` — break: the listed check removed (B28).

### PR 2

**API — `apps/api/src/db/front-desk.api.test.ts`** [C1]
- T1 `a typed charge's reason comes with who typed it, and is never blank` — break (database):
  `ALTER TABLE visits DROP CONSTRAINT visits_charge_reason_check` on `masaha_b_test`, restored after (B1).

**API — `apps/api/src/db/payments.api.test.ts`** [C1]
- T2 (changed) `a visit is paid only once its charge is set: payments_visit_uncharged` — break (database):
  the old function restored by `CREATE OR REPLACE` from the payments migration (B2).

**Unit — `apps/api/src/modules/visits/visitCharge.unit.test.ts`** [C3]
- U1 `copies the general hour and day prices for a general visit` (labelled prices ignored)
- U2 `a student visit takes the student prices, each missing one falling back to the general, hour and day
  apart` — break: the fallback by the pair (B3).
- U3 `a visit in a shift takes the shift's prices; a shift without a price falls back to the prices with no
  shift` — break: no shift fallback (B4). *(If §13 Q4 is answered "no fallback", U3 asserts `null` rates
  instead and B4 removes the shift filter.)*
- U4 `up after N minutes: whole hours, one more past N minutes, at least one hour` (59 min; 1 h 15 min with
  N 15 → 1 h; 1 h 16 min → 2 h) — break: `>=` (B5); no minimum (B6).
- U5 `to the nearest half hour, a quarter rounding up, at least one half hour` — break: `Math.floor` (B7).
- U6 `per minute, a fraction of an agora rounded half up` — break: `Math.floor` (B8).
- U7 `caps at the day price when on, and says so; never above it; off, the hours stand` — break: cap ignored
  (B9).
- U8 `with no hour price the charge is the day price; with neither, none` — break: `0` instead of `null`
  (B10).

**Unit — `packages/shared/src/visits/requests.unit.test.ts`, `desk/requests.unit.test.ts`** [C2, C3]
- U9 `a check-in takes a name of 1–60 characters, an audience from its list and an optional shift` — break:
  `max(60)` removed (B11).
- U10 `a check-out's payment is 1 to 10,000,000 whole agorot by cash or transfer; a typed charge needs its
  reason; the phone is normalised by phoneSchema` — breaks: `min(1)` on the amount (B12); `reason` optional
  (B13).

**Unit — `apps/api/src/shared/auth/can.unit.test.ts`** [C3]
- U11 `prices.typeByHand: the owner always; reception only with the switch on; reception of another space,
  an owner of another space, a user and the admin never` — break: the rule returns `staff` (B14).

**API — `apps/api/src/modules/desk/checkIn.api.test.ts`** [C2]
- T3 `the owner and reception check a visitor in: 201, the rates of the visit's audience copied, audited
  visit.checkedIn` — break: the rates read from the request (B15).
- T4 `refuses a stranger, an owner of another space and the admin with not_found`
- T5 `refuses a STUDENT visit where the space turns student prices off (422 invalid_choice on audience)`
  — break: the setting not read (B16).
- T6 `refuses a shift of another space (422 invalid_choice on shiftId), writing nothing`
- T7 `a retry with the same key answers the same visit, 201, and writes one row` — break: the pre-check
  removed (the second insert fails: 500) (B17).
- T8 `two requests with one key at once make one visit` (`whileHeld` on the space; both wait;
  `waitingOnLock({ count: 2 })` through a held transaction) — break: `spaces.lock` removed from the
  check-in (B18).
- T9 `a missing or malformed Idempotency-Key is refused with 422 before the body is read` — break: the
  middleware after `validate` (B19).
- T10 `warns SPACE_FULL at capacity and OUTSIDE_OPENING_HOURS outside the hours, and checks in anyway;
  no warnings, no meta` — break: `isFull` with `>` (B20).
- T11 `a reception link deactivated while the check-in waits on the space's lock refuses it with 403` —
  break: `can()` on `space.links` (B21).
- T12 `checkedInAt is the clock's` (fixed clock) — break: the column's default used (B22).

**API — `apps/api/src/modules/desk/checkOut.api.test.ts`** [C3]
- T13 `a check-out paid in full stores the charge with its rule and cap, records the payment, audits both`
  (fixed clock; 2 h 20 min at 5 ₪ with N = 15 → 3 h → 15 ₪; `visit.checkedOut`, `payment.recorded`) —
  break: the charge from `checkedInAt` to the database's `now()` (B23).
- T14 `the rates are those copied at check-in, the rounding and the cap those in force at check-out`
  (prices and settings changed between the two) — break: the rates re-read at check-out (B24); the rounding
  read at check-in (B25).
- T15 `a part left unpaid needs a phone: 422 required, writing nothing` — break: the phone check removed
  (B26).
- T16 `with a phone, the rest is the debt of the customer with that phone, created with the visit's name
  when new, audited customer.created` — break: a customer always created (B27).
- T17 `an archived customer's phone makes a new customer`
- T18 `an amount above the charge is refused by the ledger: 409 PAYMENT_EXCEEDS_DUE, writing nothing` —
  break: the translation table's line removed (500) (B28).
- T19 `a retry with the same key answers the first result: the same visit and payment, one payment` —
  break: the payment's key not looked up (B29).
- T20 `a check-out of a visit already closed answers it closed and records no payment` (another key) —
  break: the closed check removed (the update re-closes it: a second payment) (B30).
- T21 `two check-outs of one visit at once record one payment` (`whileHeld` on the space) — break:
  `lockIn` without `FOR UPDATE` and no space lock (B31).
- T22 `the quote's time prices the stay; a time older than 10 minutes or in the future is refused (422
  out_of_range)` — break: the bound removed (B32).
- T23 `a visit with no rate: the owner types its charge with a reason, recorded with who typed it` — break:
  `chargeSetById` not written (B33).
- T24 `reception types a charge only where the space allows it: 403 PRICE_TYPING_NOT_ALLOWED otherwise,
  writing nothing` — break: `can()` replaced by `staff` (B34).
- T25 `a typed charge needs a reason (422 required) and is refused where the visit has a rate (422
  invalid_choice on charge)` — break: the rate check removed (B35).
- T26 `refuses a stranger, an owner of another space and the admin with not_found; a visit of another space
  is not_found` — break: `lockIn` without `spaceId` (B36).
- T27 `a reception link deactivated while the check-out waits on the space's lock refuses it with 403` —
  break: `can()` on `space.links` (B37).

**API — `apps/api/src/modules/visits/visits.api.test.ts`** [C4]
- T28 `the quote of an open visit is its charge now; a closed visit has none`
- T29 `the visit terms: the rounding, the cap, the rates per shift, the student rates only where they change
  one, and whether the caller may type a price` (owner true; reception false, then true with the switch) —
  break: `student` always returned (B38).
- T30 `refuses a stranger, an owner of another space and the admin with not_found`

**API — `apps/api/src/modules/occupancy/present.api.test.ts`** [C4]
- T31 `each visit present carries its charge so far, or none without a rate` — break: `chargesNow`
  computed at `checkedInAt` (B39).

### PR 3

**Unit — `apps/api/src/modules/spaces/autoCheckout.unit.test.ts`** [C1]
- U1 `due at the day's closing` · U2 `at 23:59 without any hours` · U3 `at 23:59 on a closed day or after
  closing` · U4 `none when the closing check-out is off and no stay limit` · U5 `the stay limit when it ends
  sooner; the closing when it comes first` · U6 `a 0–1440 day ends at 23:59` · U7 `on a daylight-saving day`
  · U8 `never before the check-in` — breaks: `max` for `min` (B1); the closing read from the run's day
  instead of the check-in's (B2).

**Unit — `apps/api/src/shared/jobs/secret.unit.test.ts`** [C2]
- U9 `matches only "Bearer <secret>"`: missing, another scheme, a prefix, a longer value — break:
  `header.includes(secret)` (B3).

**Unit — `apps/api/src/config/env.unit.test.ts`** [C2]
- U10 `JOBS_SECRET is at least 32 characters when set, and required in production` — break: the production
  list without it (B4).

**Unit — `apps/api/src/modules/payments/balance.unit.test.ts`** [C4]
- U11 `the balance is the due less what was paid; no due, no balance` — break: `paid − due` (B5).

**API — `apps/api/src/shared/jobs/jobs.api.test.ts`** [C2]
- T1 `the endpoint refuses a missing or wrong secret with 401 and runs nothing` — break: the secret check
  removed (B6).
- T2 `with the secret it runs the jobs and answers what each did`
- T3 `without JOBS_SECRET the endpoint does not exist` (404) — break: mounted always (B7).
- T4 `a failing job answers 500, logs it, and the other jobs still ran` (through the real composition: the
  test deletes one space's settings row, a fault by `space-settings`' rule, so `visits.autoCheckOut` throws;
  `subscriptions.autoCheckOut` still closes its due check-in) — break: the `try` per job removed (B8). *(If
  this needs any seam the code does not already receive, drop T4 and say so: Review Focus.)*

**API — `apps/api/src/modules/visits/autoCheckOut.api.test.ts`** [C2]
- T5 `a visit due at closing is closed at closing, not at the run's time, and charged to then` (run at
  18:04, closing 18:00) — break: `checkedOutAt = now` (B9).
- T6 `a second run closes nothing more and audits nothing` — break: the "still open" check removed (B10).
- T7 `a run after two days without runs closes each stay at its own due time` — break: due computed from
  the run's day (B2 again, API side).
- T8 `a stay not yet due stays open`
- T9 `the stay limit closes a stay before closing; turned on later, it closes an open stay at its new due
  time` — break: settings read at check-in (B11).
- T10 `a visit with no rate is closed with no charge, uncollected` 
- T11 `open subscription check-ins are closed the same way, audited with no actor` — break: subscriptions'
  job not registered (B12).
- T12 `a manual check-out meanwhile wins: the job finds the visit closed and leaves it` (`whileHeld` on the
  visit's row; the test closes it, commits) — break: no `FOR UPDATE` (B13).
- T13 `audits visit.autoCheckedOut with no actor`

**API — `apps/api/src/modules/desk/checkOut.api.test.ts`** [C3]
- T14 `reception without the switch closes a visit with no rate unpriced, with a phone; never free` —
  break: `chargeAgorot: 0` (B14).
- T15 `the unpriced close still needs a phone (422 required)`
- T16 `the owner, who may type, must: 422 required on charge` 
- T17 `a payment on an unpriced close is refused by the ledger: 409 VISIT_NOT_PRICED` — break: the
  translation line removed (B15).

**API — `apps/api/src/modules/visits/unpriced.api.test.ts`** [C3]
- T18 `lists the closed visits with no charge, paged, newest first, to the owner and reception`
- T19 `the owner prices one with a reason: recorded with who typed it, audited visit.priced` 
- T20 `reception prices one only where the space allows it (403 PRICE_TYPING_NOT_ALLOWED)` — break: `can()`
  as `staff` (B16).
- T21 `a priced visit is refused with 409 VISIT_ALREADY_PRICED; an open one with 409` — break: the charge
  check removed (B17).
- T22 `refuses a stranger, an owner of another space and the admin with not_found; another space's visit is
  not_found`
- T23 `a link deactivated while the pricing waits on the space's lock refuses it with 403` — break: `can()`
  on `space.links` (B18).

**API — `apps/api/src/modules/payments/uncollected.api.test.ts`** [C4]
- T24 `lists the visits closed automatically and not fully paid, the unpriced ones included; never a
  manual check-out's` — break: the `AUTO` filter dropped (B19).
- T25 `a visit paid in full leaves the list; a voided payment does not count` — break: voided payments
  summed (B20).
- T26 `every page is full and the total right` (`limit=1`) — break: the settled ids filtered after the page
  (B21).
- T27 `answers the owner and reception; not_found to a stranger, an owner of another space and the admin`

### Not tested, and said
- The in-process timer (`timer.ts`): its interval and its skip are plain `setInterval` wiring; proven by
  the real run (the log line every 5 minutes), not a test (a test would need a fake timer the code never
  receives: testing §3 rule 2).
- The 500-row batch: no test inserts 501 stays (Review Focus).
- Daylight-saving dates beyond the one pinned (conventions §11's mitigation).

---

## 10. Review Focus — the inputs no planned test exercises

**PR 1**
1. A closure announcement whose `endsAt` equals now exactly (`> now` excludes it).
2. Two directory requests across a status change within the 30-second cache: the card may lag 30 s.
3. `availableAmong` over many verified spaces: five set-based queries over all of them (≈ 1,000).
4. A space whose hours were saved with every day closed: `CLOSED` always (not `null`).
5. An override set at 23:59 on a 0–1440 day: `until` is the next midnight.

**PR 2**
1. A stay over midnight with the closing check-out off and no stay limit: the cap at one day price.
2. `NEAREST_HALF_HOUR` with an odd hour rate: half an agora rounded up.
3. A retry whose first check-in's warnings differed (S3).
4. Two check-ins of one key from two different staff (one wins; the other gets the first's body).
5. A customer found by phone whose name differs from `customerName`: the stored name is kept.
6. A check-out quoted 9 min 59 s ago, crossing a rounding boundary in that window.

**PR 3**
1. More than 500 due stays in one run (`remaining` > 0; the next run continues).
2. A visit whose space was soft-deleted while it was open: closed with its hours and settings as stored.
3. Two cron calls overlapping: two runs racing on one row (each row locked; the second skips).
4. A run during a daylight-saving change.
5. An unpriced visit later priced, then paid at step 9: `payments_within_due` then applies.

---

## 11. The commits

Each commit holds its code, tests and documents (Appendix A); `lint` and `typecheck` on each. Every new
decision and history line ends with `<the day's date>, #PRNUM`.

### PR 1 — `feat/live-status`, title `feat(occupancy): derive the live status` (39)
| # | Subject | Chars | Holds |
|---|---|---|---|
| C1 | `feat(core): read the time in Gaza` | 33 | the dependency; `gazaTime.ts`, U1–U3; conventions §11 |
| C2 | `feat(occupancy): derive the live status` | 39 | `liveStatus.ts`, the four new modules' reads, `spaces.weekOf/weeksFor`, `GET /occupancy`, U4–U12, T1–T6; contract *Occupancy (managed)* (the read, §4's exception); `occupancy.md`; data model; conventions §9; map line; overview; v1-mvp |
| C3 | `feat(occupancy): override the live status` | 41 | `overrideUntil.ts`, `PUT`/`DELETE …/status-override`, `SPACE_NOT_OPEN` (+ catalogues), U13–U14, T7–T16; contract; §6; security's `requireCan` list; data model *Live status* 3; `occupancy.md` |
| C4 | `feat(directory): show the live status` | 37 | the directory's fields, filter and route; `onlyIds`; U15, T17–T21; contract *Directory*; `directory.md`; v1-mvp ordering note and surface; overview |

### PR 2 — `feat/desk-visits`, title `feat(desk): check a visit out and take payment` (46)
| # | Subject | Chars | Holds |
|---|---|---|---|
| C1 | `feat(db): record why a charge was typed` | 39 | schema, migration (reason + trigger split), T1–T2; data model *Constraints* |
| C2 | `feat(desk): check a visitor in` | 30 | `idempotencyKey` (core + middleware), `WarningsMeta`, shared `visits`, `desk` check-in, `visits.create`, `occupancy.checkInWarnings`, `spaces.pricesOf`, `space-settings.read(tx)`, `SPACE_FULL`, U9, T3–T12; contract (§1's key, *Front desk (managed)*: the check-in, §6); `visits.md`, `desk.md` (first); conventions §13 (S1); map lines |
| C3 | `feat(desk): check a visit out and take payment` | 46 | `visitCharge.ts`, `payments`, `customers.findOrCreateByPhone`, the translation table, `prices.typeByHand`, the check-out, `PAYMENT_EXCEEDS_DUE`, `PRICE_TYPING_NOT_ALLOWED`, U1–U8, U10–U11, T13–T27; contract; `payments.md`; data model *Visit charge* (P7, P8), *Unpaid visit*; conventions §4, §13; security; finding 15 resolved + index; overview; v1-mvp |
| C4 | `feat(visits): read a visit's terms and charge` | 45 | `GET …/visits/:visitId`, `GET …/visit-terms`, the read's charge so far, T28–T31; contract; `visits.md`, `occupancy.md` |

### PR 3 — `feat/auto-checkout`, title `feat(jobs): close open stays automatically` (42)
| # | Subject | Chars | Holds |
|---|---|---|---|
| C1 | `feat(spaces): compute the auto check-out time` | 45 | `autoCheckout.ts`, U1–U8; data model *Auto check-out* (D-PR3-1); `spaces.md` code map line |
| C2 | `feat(jobs): close open stays automatically` | 42 | `shared/jobs`, env, `server.ts`, `app.ts`, `settingsFor`, both `autoCheckOut`s, U9–U10, T1–T13; contract (*Internal*); conventions §1, §12; security; setup's runbook; `.env.example`; `visits.md`, `desk.md`; overview; v1-mvp |
| C3 | `feat(visits): close a visit unpriced` | 36 | Q4's branch, `unpricedIn`, `price`, `VISIT_NOT_PRICED`, `VISIT_ALREADY_PRICED`, T14–T23; contract; data model; `visits.md`, `desk.md` |
| C4 | `feat(payments): list uncollected visits` | 39 | `balance.ts`, `uncollectedIn`, U11, T24–T27; contract; conventions §9's line; `payments.md`; overview; v1-mvp |

---

## 12. Verification and the procedure

**The same procedure for each PR**, with that PR's branch, base and checks. The executor of PR *n* reads this
whole plan and executes only PR *n*.

### 12.1 Before the branch
```powershell
Set-Location C:\dev\masaha\app-b
git fetch origin
git status --short --branch            # clean, detached at origin/main
git log --oneline -5 origin/main
gh pr list --state open --json number,title,headRefName,headRefOid,files
git diff --name-status eff0a3d1 origin/main
```
**PR 1:** a change since `eff0a3d1` to a code file of §4's PR 1 table, to `shared/auth/*`, `shared/audit/*`,
`shared/http/*`, `shared/validation/*`, `spaces/spaces.service.ts`, `spaces/public/*`, `directory/*`,
`occupancy/*`, `apps/api/test/*`, `schema.prisma`, `eslint.config.js`, `packages/shared/src/core/*` or
`package.json`/`package-lock.json`: re-read it; **if it contradicts this plan, stop and ask.**
**PR 2 and PR 3:** the same diff; the earlier PRs' files must match what this plan says they hold (PR 1's
for PR 2; PR 1's and PR 2's for PR 3); any other change to a code file this PR names → stop and ask.
An open PR that edits a code file of this PR: stop and ask. Its documents: re-read the shared ones on the
merged tree before editing. **The finding's number** (only if one is recorded): the first free number on the
latest index.

```powershell
git switch --no-track -c <feat/live-status | feat/desk-visits | feat/auto-checkout> origin/main
docker start masaha-postgres-1         # never npm run db:up; never npm ci
npm run build -w @masaha/shared
```
`apps/api/.env` must name `masaha_b_dev` / `masaha_b_test` and `PORT=3321` (check with `Select-String`;
never print the file). **After PR 1 or PR 2 merged** (a dependency, a migration): `npm install` once in the
worktree (never `npm ci`), `npm exec -w @masaha/api -- prisma generate`, `npm run db:migrate` (applies to
`masaha_b_dev`).

**One full test run at a time on this machine.** Before each full lane:
```powershell
Get-CimInstance Win32_Process -Filter "Name = 'node.exe'" |
  Where-Object { $_.CommandLine -match 'vitest' } | Select-Object ProcessId, CommandLine
```
A line under `C:\dev\masaha\app\` (worker A): wait for it to end.

### 12.2 First checks (each when its code exists)

**PR 1**
1. **The dependency:**
   `npm install -w @masaha/api -w @masaha/shared @date-fns/tz@^1.5.0`; then `git diff --stat
   package-lock.json` shows only the two workspaces' dependency entries (the package is already locked at
   1.5.0). Another version resolved, or `node_modules` entries added: stop and ask. `import { TZDate } from
   '@date-fns/tz'` must typecheck in both workspaces; if not, stop and ask (alternative A2 is the fallback,
   the owner's to choose).
2. **A Gaza daylight-saving transition to pin:** read one from Node's own zone data, for example
   `node -e "for(let d=Date.UTC(2025,0,1);d<Date.UTC(2026,0,1);d+=36e5){const o=new Intl.DateTimeFormat('en',{timeZone:'Asia/Gaza',timeZoneName:'longOffset'}).format(d).slice(-9);if(o!==globalThis.p)console.log(new Date(d).toISOString(),o),globalThis.p=o}"`,
   and write the instants into U2 **by hand**. Record the output in the report.
3. **The level rule:** `npm run lint` after C2 passes with `occupancy` importing `visits`, `subscriptions`,
   `customers`, `announcements` and `spaces`, and after C4 with `directory` importing `occupancy` and
   `@masaha/shared/occupancy` (L4 under L5). A refusal: stop and ask.
4. **`onlyIds` in the public listing:** read `publicListing.repository.ts` first; apply `onlyIds` exactly as
   `verifiedIds` is applied (raw SQL or Prisma, whichever it is), before the order and the page. If the
   query cannot take it there, stop and ask.
5. **`groupBy` with `_count`** for the open counts compiles and reads one query each (`DEBUG=prisma:query`
   not needed: T3 proves the counts).

**PR 2**
1. **The migration, created once** (after the schema edit):
   ```powershell
   npm exec -w @masaha/api -- prisma migrate dev --create-only --name desk_visit_charge
   Get-ChildItem apps/api/prisma/migrations | Select-Object -Last 2
   ```
   Run it **once**, then list the folder. Keep Prisma's `ALTER TABLE "visits" ADD COLUMN "charge_reason"
   TEXT;` and append, under a raw-SQL header as the earlier migrations have:
   ```sql
   -- A typed charge's reason comes with who typed it, and is never blank (data-model › Hand-typed prices).
   ALTER TABLE "visits" ADD CONSTRAINT "visits_charge_reason_check"
     CHECK (
       ("charge_set_by_id" IS NULL) = ("charge_reason" IS NULL)
       AND ("charge_reason" IS NULL OR btrim("charge_reason") <> '')
     );

   -- Finding 15: an uncharged visit gets a constraint name of its own, so it translates to its own code.
   -- The function is the payments migration's, with only that RAISE changed.
   CREATE OR REPLACE FUNCTION "payments_guard_insert"() RETURNS trigger LANGUAGE plpgsql AS $$
   … the body of 20260929120300_payments, copied whole, except:
       RAISE EXCEPTION 'payments_visit_uncharged: a visit is paid once its charge is set'
         USING ERRCODE = 'check_violation', TABLE = 'payments', CONSTRAINT = 'payments_visit_uncharged';
   $$;
   ```
   *On a data-loss refusal* (not expected: a nullable column): `prisma migrate diff --from-migrations
   apps/api/prisma/migrations --to-schema-datamodel apps/api/prisma/schema.prisma --script` into the folder,
   then append, and say so. Then `npm run db:migrate` (`masaha_b_dev`; regenerates the client: check
   `apps/api/src/generated/prisma/models/Visit.ts` names `chargeReason`). `masaha_b_test` is migrated by the
   API lane's global setup. Prove the function: `docker exec masaha-postgres-1 psql -U <the .env user> -d
   masaha_b_dev -c "SELECT prosrc LIKE '%payments_visit_uncharged%' FROM pg_proc WHERE proname =
   'payments_guard_insert'"` → `t`.
2. **The trigger's error as Prisma throws it:** with T18 written, log once (then remove) the error's
   `constructor.name`, `code` and `meta` for an amount above the charge. Write `checkViolationOf` to read
   the constraint's name from where it is (the `meta`, or the message's leading `payments_within_due:`),
   and record the shape in the report. If Prisma gives no way to tell the constraint, stop and ask.
3. **`res.locals` typing** for the key: as `listQueryOf(res)` does in `directory/listQuery.ts`.
4. **The space lock before the visit's row, then the trigger's `FOR UPDATE` on the same row** in one
   transaction: T13 and T21 green prove it; a deadlock or a wait: stop and ask.
5. **`sendSuccess`'s meta widened:** `npm run typecheck` (every workspace) green; the web's typecheck reads
   `SuccessEnvelope` — a failure there: stop and ask (no web code change is licensed for it).

**PR 3**
1. **The secret's compare:** `timingSafeEqual` on two `sha256` digests of `Buffer.from(header)` and
   `Buffer.from('Bearer ' + secret)`.
2. **The timer leaves no handle:** `npm run dev -w @masaha/api` then Ctrl-C (or the stop by process id):
   the process exits within the shutdown's timeout.
3. **`createApp`'s 404 for `/api/v1/internal/jobs/run`** without the secret: T3 proves it.
4. **The level rule:** `payments` importing `visits`; `subscriptions` importing `spaces` and
   `space-settings`; `shared/jobs` importing no module (the composition root wires the jobs).

### 12.3 Implement, commit by commit
Stage **by path** (`git add <path> …`; never `-A` or `.`); `git status` before each commit; after each
commit `npm run lint` and `npm run typecheck`. Inside each commit: the test first, run red in its lane (the
output into the report), then the code, then green, then its documents (Appendix A). The error codes follow
`add-error-code`: the code in `packages/shared`, both catalogues, its line in api-contract §6, the test that
provokes it.

**A fix before the push** folds into its commit:
```powershell
git commit --fixup=<sha> -- <paths>
$env:GIT_SEQUENCE_EDITOR=':'; git rebase -i --autosquash $(git merge-base HEAD origin/main); Remove-Item Env:GIT_SEQUENCE_EDITOR
git rebase -x "npm run lint && npm run typecheck" $(git merge-base HEAD origin/main)
```

### 12.4 Verification on the head (phase 4)
One at a time: `npm run lint` · `npm run typecheck` · `npm run test:unit` · `npm run test:api` ·
`npm run format:check` · `npm run check:links` · `npm run build -w @masaha/shared` (every PR changes the
shared package). Also: `git grep -n "#PRNUM"` lists only documents (before §12.7). **PR 1 and PR 2–3:**
`git diff --stat origin/main -- apps/web` shows only the two `errors.ts` catalogues; **PR 2–3:** `git diff
--stat origin/main -- package.json package-lock.json` is empty. **Not run, with why:** `test:component`,
the web's `build`, `check:build`, `check:classes` — the web's change is two catalogue files of strings,
whose parity the unit lane checks; CI runs them on the pushed head.

### 12.5 The breaks (testing §3 rule 7), each recorded
For each: copy the file to `$env:TEMP\desk-breaks\` (a backup), make the one edit, run the named test file
in its lane, copy the red lines into the report, restore **from the backup** (never `git checkout`; no CRLF
change if a script copies), run it green, then `git diff --stat` shows only the item's own work. The breaks
are §9's B-numbers, per PR; the database ones:
- **PR 2 B1:** `docker exec masaha-postgres-1 psql -U <user> -d masaha_b_test -c "ALTER TABLE visits DROP
  CONSTRAINT visits_charge_reason_check"`; T1 red; restore by re-running the migration's `ALTER TABLE …
  ADD CONSTRAINT` on `masaha_b_test`; T1 green.
- **PR 2 B2:** on `masaha_b_test`, `CREATE OR REPLACE` the function from the payments migration's text; T2
  red; restore with the new migration's function; T2 green.

Every permission (the role tests' `requireCan` and `can()` breaks), every money rule (the charge, the cap,
the fallbacks, the ledger's two translations, the phone rule, the typed price), every idempotency key
(PR 2 B17, B29) and every race (PR 1 B23; PR 2 B18, B21, B31, B37; PR 3 B13, B18) has its break above.
**A break that stays green: stop and ask.**

### 12.6 The real run (API on 3321, `masaha_b_dev`)
Start `npm run dev -w @masaha/api` in the background; `curl.exe -s http://localhost:3321/health` →
`db: up`. Sign in as the demo owner (`demo-owner@example.com`, `SEED_DEMO_PASSWORD` read from
`apps/api/.env` into a variable, never printed) or, without the demo, create a space and an owner as the
`SEED_ADMIN_*` admin and make the forced change; reception: the demo's, or one the owner adds.
- **PR 1:** the owner sets the hours (`PUT …/hours`, open now) and the capacity (`PUT …/capacity` 1); insert
  one open visit through `psql` (`INSERT INTO visits (space_id, request_id, visitor_name, checked_in_at,
  updated_at) VALUES (<id>, gen_random_uuid(), 'Real run', now(), now())`); `GET …/occupancy` as reception
  → `present: 1`, `status: "FULL"`, the person listed; `PUT …/status-override { state: "AVAILABLE",
  duration: "MINUTES_30" }` → `until` 30 min ahead; `GET /api/v1/spaces?availableNow=true` lists the space;
  `GET /api/v1/spaces/<slug>/occupancy` → `{ status: "AVAILABLE" }` only; `DELETE …/status-override` →
  `FULL` again; as the admin, `GET …/occupancy` → 404. Close the inserted visit through `psql` afterwards.
- **PR 2:** set an hour price and a day price; `POST …/visits` with a fresh UUID key → 201 (`meta.warnings`
  as the capacity says); the same request again → 201, the same id; `GET …/visits/:id` → a quote; `POST
  …/check-out` with `payment` below the charge and no phone → 422; with `phone: "0599000123"` → 200, the
  customer created; the same check-out again (same key) → the same body; a second visit, the prices removed:
  reception's check-out → 403 `PRICE_TYPING_NOT_ALLOWED`; the owner's with `charge: { amountAgorot, reason }`
  → 200. `SELECT action FROM audit_logs ORDER BY id DESC LIMIT 6` through `psql`.
- **PR 3:** set `JOBS_SECRET` in `apps/api/.env` (a random value; never printed) and restart; open a visit
  with `checked_in_at` three hours ago through `psql`, with the stay limit set to 1 hour (`PATCH
  …/settings { maxStayMinutes: 60 }`); `curl.exe -s -X POST http://localhost:3321/api/v1/internal/jobs/run`
  → 401; with `-H "Authorization: Bearer $env:JOBS_SECRET_VALUE"` (read from the file into a variable) → 200,
  `visits: 1`; the visit's `checked_out_at` = check-in + 1 h; again → `visits: 0`; the server's log shows
  `'job ran'` lines, and the timer's own run within 5 minutes. `GET …/uncollected-visits` lists it. A visit
  with no rate checked out by reception (switch off) with a phone → closed unpriced; `GET
  …/unpriced-visits` lists it; the owner's `PUT …/charge` → 200. Remove `JOBS_SECRET` from `.env` afterwards
  (it was added only for the run) — or keep it, and say which.
- Stop the server by its process id (the `tsx watch` child and the server); `Get-NetTCPConnection
  -LocalPort 3321 -ErrorAction SilentlyContinue` prints nothing.

### 12.7 The PR number, push and PR
Just before the push, in Git Bash:
```bash
n=$(( $(gh api "repos/{owner}/{repo}/issues?state=all&per_page=1&sort=created&direction=desc" --jq '.[0].number') + 1 ))
base=$(git merge-base HEAD origin/main)
git filter-branch -f --tree-filter "grep -rl '#PRNUM' docs | xargs -r sed -i 's/#PRNUM/#$n/g'" $base..HEAD
git for-each-ref --format='%(refname)' refs/original/ | xargs -r -n1 git update-ref -d
git grep -n '#PRNUM' ; echo "expect nothing above; PR will be #$n"
git push -u origin <branch>
```
Then `gh label list` (create `feat`, `area:api`, `area:docs` if missing, each with a description and a
colour; PR 1–3 also touch two web catalogue files: add `area:web`), and at once:
```powershell
gh pr create --assignee @me --label feat --label area:api --label area:docs --label area:web `
  --title "<the PR's title, §11>" --body-file <§12.9's text, saved in $env:TEMP>
```
GitHub's number must equal `n`; if not, replace it in the documents (a fixup into the commits that hold it)
and `git push --force-with-lease`.

### 12.8 CI, CLEAN, conflicts, report
- `gh pr checks <n> --watch`, then `gh pr view <n> --json headRefOid,mergeStateStatus,statusCheckRollup`:
  green **on the pushed head** and `CLEAN`. Never merge; never rebase a `CLEAN` PR.
- **Conflicts, early:** for every other open PR, `git merge-tree --write-tree HEAD <its headRefOid>`;
  record clean or the conflicted paths. Documents only (`overview.md`, the findings index): the fast path
  when its turn comes (keep both sides, `format:check`, one push). Code: stop and ask.
- **The report**, `C:\dev\masaha\workspace\WORKER_B\DESK\4_REPORT_PR<n>.md`, written in parts (UTF-8): the
  head and the commits; each command run and not run; each test's red-first output; each break with its
  red lines; §12.2's results; the real run's statuses; the owner's answers to §13 as built; the problems
  and their solutions; anything unexpected, even unsolved; the conflict check; every departure from this
  plan with its reason. **PR 3's report also** updates `C:\dev\masaha\workspace\_SHARED\OPEN_DECISIONS.md`
  point 1's *Carried to step 7* line: "built (#n): reception closes the visit unpriced; the owner prices it
  (`PUT …/visits/:visitId/charge`); «يحتاج انتباهك» counts `GET …/unpriced-visits` and `GET
  …/uncollected-visits`" — and point 4 stays open for step 9.

### 12.9 The PR description (fill the evidence from the runs)
```markdown
## Summary
<PR 1: the staff's live read (present, capacity, status), the manual override, the live status in the directory; Gaza time.
 PR 2: checking a visitor in and out at the desk: rates copied, the charge, the first payment, the unpaid rest with a phone, the typed price with its reason; finding 15.
 PR 3: the scheduler (a timer locally, a secret-protected endpoint for an external cron online), auto check-out at the due time, unpriced visits (Q4), uncollected visits.>

## Scope / Acceptance criteria / Out of scope
<§2, this PR's part>

## Change type
feat — API code, the shared contract, tests and documents; <PR 1: a dependency (@date-fns/tz) | PR 2: a migration | PR 3: an environment variable (JOBS_SECRET)>; the new error codes' catalogue lines in apps/web (worker B's licence).

## New error codes (the Arabic needs the owner's approval)
<each code: its English and Arabic line, from §13>

## Evidence
- `npm run lint`, `npm run typecheck` (each commit), `test:unit`, `test:api`, `format:check`, `check:links`, `build -w @masaha/shared`: <results>.
- Seen failing first: <each test, its red line>.
- Deliberate breaks, each red then restored: <the PR's B-list>.
- Real run on 3321: <statuses>.
- Not run: `test:component`, the web's `build`, `check:build`, `check:classes` — the web change is two catalogues of strings; CI runs them.

## Screenshots
None: API and documents only.

## Definition of Done checklist
- [x] Acceptance criteria met, scope kept.
- [x] Lint and typecheck clean; `packages/shared` builds.
- [x] Tests added in the owning lanes, each seen failing.
- [x] No hardcoded user-facing text (the API sends codes; both catalogues have the new codes).
- [x] Authorization enforced on the server (the boundary, `requireCan`, `can()` under the space's lock).
- [x] Triggered documentation updated in this PR.
- [x] One home per fact; nothing claimed that is not built.
- [x] Every claim names its test or command.
- [x] Atomic history, pushed.
```

### The executor's stop rule — a test you cannot run stops the work
A test **failing** because its code is not written yet is the plan's red step — normal. A test, lane or
command you **cannot run** is not: it errors before any test runs (the database unreachable, Docker down, a
port taken, a module or `dist` missing, a migration pending, `No test files found`, a Vitest or TypeScript
startup error, the whole run timing out, a crash with no result); a break you could not make or run; a
real-run case you could not perform. **Then stop at once** — never skip, `.skip` or delete a test, never
change a config, a timeout, `.env`, a script or a lane, never mock what the plan does not, never run a
narrower command and call it the lane, never call it "flaky" and move on. Write the command, its exact
error and where you were into the report, and reply with the exec prompt's final shape, `Status: STOPPED`.

**A plan that proves false against the code:** stop too, say exactly what and why, and offer the fix — do
not choose it yourself. **A break that stays green:** stop — unless it is plainly your own test's defect;
then strengthen the test, see the break go red, and state it as a departure.

**Never claim a result you did not see:** a command passed only if you saw its own output say so; copy that
line (read it by its exit code, not the tail). A break counts only when you saw it red.

---

## 13. Decisions needed from the owner

1. **Q1 — the dependency** (PR 1): `@date-fns/tz` 1.5.0 as a direct dependency of `apps/api` and
   `packages/shared` (already in the lockfile through the web), as conventions §11 names it; `date-fns`
   itself is not needed. *Alternative A2:* `Intl` only, no dependency.
2. **Q2 — the new error codes** (the Arabic for your approval):
   | Code | PR | Answer | English | Arabic |
   |---|---|---|---|---|
   | `SPACE_NOT_OPEN` | 1 | 409 | The status can be set only while the space is open by its hours. | لا تُضبط الحالة إلا والمساحة مفتوحة حسب ساعات عملها. |
   | `SPACE_FULL` | 2 | a warning in `meta.warnings` | The space is full; the check-in was recorded anyway. | المساحة ممتلئة، وسُجّل الحضور رغم ذلك. |
   | `PAYMENT_EXCEEDS_DUE` | 2 | 409 | The amount is more than what is due. | المبلغ أكبر من المستحق. |
   | `PRICE_TYPING_NOT_ALLOWED` | 2 | 403 | The space's settings do not let reception type a price. | إعدادات المساحة لا تسمح للاستقبال بكتابة سعر يدويًا. |
   | `VISIT_NOT_PRICED` | 3 | 409 | A visit without a price takes no payment; price it first. | لا تُستلم دفعة لزيارة بلا سعر؛ سعّرها أولًا. |
   | `VISIT_ALREADY_PRICED` | 3 | 409 | This visit already has a price. | لهذه الزيارة سعر بالفعل. |
3. **Q3 — the rounding's details** (P7): at least one hour (or half hour, or minute); "more than N minutes"
   (the prototype's `>`), not "N minutes or more"; a quarter hour rounds up to the half; fractions of an
   agora round half up. Each changes one unit test and the data model's line.
4. **Q4 — a shift without a price falls back to the space's price with no shift** (P8), period by period,
   as a student price falls back to the general one. *Otherwise:* that visit has no rate and its charge is
   typed (or unpriced in PR 3). The data model gains the line either way.
5. **Q5 — a check-in on a closed day or after closing is due at 23:59** (D-PR3-1), as a space without
   hours. *Otherwise:* due at once (charged nothing) — not recommended.
6. **Q6 — the schema changes:** PR 2's migration (`visits.charge_reason` with its `CHECK`; the trigger's
   new constraint name, S2). PR 1 and PR 3 change no schema.
7. **Q7 — the new environment variable `JOBS_SECRET`** (PR 3), required in production; the cron service is
   yours to set up by the runbook line (O2).
8. **Q8 — S3:** a retried check-in recomputes its warnings (not the "same body" to the letter).
9. **Q9 — K6 and DK-012** (the uncollected visit's write-off, its collection and its debt by phone): the
   desk decisions place them in step 7, but the prompt does not. Build them as **PR 4** (alternative A3) or
   leave them to step 9. *Recommended:* PR 4, after PR 3, before the desk's screen.
10. **Q10 — finding 17's sweep** as a small item right after PR 3 (A4), or later.
11. **Q11 — the sizes:** ≈ 58, 52 and 44 files; each over 25, each with a separate review. *Alternative
    A5:* PR 1 split in two (occupancy; the directory).

---

## 14. Stop and ask

- `origin/main` changed a code file §12.1 names in a way this plan does not cover; or an open PR edits a code
  file of the PR in hand; or an earlier PR of this plan merged with a different shape than this plan says.
- A change is needed in `apps/web` beyond the two catalogue files, a dependency other than PR 1's, an error
  code not in §13 Q2, or a schema change not in §13 Q6.
- More than about 70 files would change in one PR.
- The migration cannot be made as §12.2 (PR 2) says, or the function's text cannot be copied whole.
- The level rule refuses an import this plan names (§12.2).
- Prisma's error gives no constraint name (PR 2 §12.2 check 2).
- The dependency resolves another version or changes other lockfile entries (PR 1 §12.2 check 1).
- A break of §12.5 stays green.
- A failure not understood after three root-cause fixes; CI failing for a reason not reproduced locally after
  three.
- A conflict with another open PR in a code file.
- The owner's answer to §13 changes a test or a rule: follow the answer as written in the approval note; a
  case the answer does not cover: stop and ask.

---

## Proposed alternatives

**A1 — Q4's unpriced close in PR 2, not PR 3.** *What:* PR 2's check-out closes a no-rate visit unpriced
for whoever may not type, instead of answering 403 until PR 3. *Why:* no interim behaviour that PR 3
changes; the check-out is complete in one PR. *Cost:* PR 2 +1 code (`VISIT_NOT_PRICED`), +4 tests; PR 3
keeps the read and the pricing. *Changes in the plan:* PR 3 C3's T14–T17 and the branch move to PR 2 C3.

**A2 — `Intl` instead of `@date-fns/tz`.** *What:* `gazaClockOf` through `Intl.DateTimeFormat(...,
{ timeZone: 'Asia/Gaza' }).formatToParts`, and `gazaInstant` by computing the offset at a first guess and
correcting once. *Why:* no dependency; the web (`updatedAgo.ts`, `updatedOn.ts`) and the seed already use
`Intl` for Gaza. *Cost:* ≈ 20 lines of offset arithmetic to own, against conventions §11's named library
(its line changes). *Changes:* PR 1 C1 without the dependency; §13 Q1 dropped.

**A3 — PR 4: collect an uncollected visit, and write one off (K6, DK-012).** *What:* `POST
…/visits/:visitId/payments` (🧾, `Idempotency-Key`: a payment on a closed, priced visit; a remaining debt
needs a phone, which attaches the customer — DK-012's «تسجيل دينًا» with no payment is the same route with
`payment: null`); `POST …/visits/:visitId/write-off { reason }` (🏢; a migration: `written_off_at`,
`written_off_by_id`, `write_off_reason`, together, non-blank, only on a closed visit; the uncollected list
and the debt rule leave it out; audited `visit.writtenOff`). *Why:* the desk decisions K6 and DK-012 place
them in step 7, and the desk's screen needs them for its «غير محصّلة» tab. *Cost:* ≈ 30 files, one
migration, two codes; the data model's *Customer debt* and *Uncollected visits* lines gain the write-off.
*Changes:* none to PR 1–3; PR 4's plan would be written from this section.

**A4 — finding 17's sweep as a second job, right after PR 3.** *What:* a job deleting expired
`rate_limits` rows, expired refresh and reset tokens, and expired recoveries. *Why:* the scheduler exists
after PR 3; the free tier's 0.5 GB is the risk the finding names. *Cost:* ≈ 8 files in `sessions` and
`shared/rate-limit`, their expiry rules each tested. *Changes:* none to this plan.

**A5 — PR 1 in two.** *What:* PR 1a the staff's side (C1–C3, ≈ 45 files), PR 1b the directory (C4, ≈ 13).
*Why:* a smaller review of the security-relevant part. *Cost:* one more PR cycle. *Changes:* PR 1's
commits split as said; PR 2 waits for 1a only.

**A6 — the live status on the space's page too.** *What:* `PublicSpace.liveStatus` instead of, or beside,
`GET /spaces/:slug/occupancy`. *Why:* one request for the page. *Cost:* ADR 0008's *Decision* line on the
endpoint revised. **Not recommended:** the page is cached whole for 30 s and the endpoint lets it refresh
the state alone.

---

## Appendix A — the documents, line by line (the commit in brackets)

Every new decision and history line ends with `<date>, #PRNUM`; *Last Updated* on each document changed.

### PR 1
1. **`docs/api/api-contract.md`** — new section *Occupancy (managed)* after *Capacity (managed)*: the
   read `GET …/occupancy` (🧾), its `SpaceOccupancyNow` and `PresentPerson` shapes, "answered whole" [C2];
   `PUT` / `DELETE …/status-override` (🧾; body; `until`'s rule; `SPACE_NOT_OPEN`; audit names;
   `forbidden` for an owner or reception whose link ended meanwhile) [C3]; §4's exceptions gain the people
   present [C2]; *Directory (public)*: "No answer carries a capacity, a count or a live status" → "No answer
   carries a capacity or a count; the card and the pin carry the live status ([ADR 0008])"; `availableNow`
   among the filters; `liveStatus` in `DirectorySpace` and `MapPin`; `GET /spaces/:slug/occupancy` [C4];
   §6: `SPACE_NOT_OPEN` [C3].
2. **`docs/architecture/data-model.md`** — *Live status* 3: "The owner or reception sets it for 30 min, 1 h,
   2 h or until today's closing time, never past it, and only while the space is open by its hours"
   [C3]; *SpaceOccupancy*'s line unchanged.
3. **`docs/backend/conventions.md`** — header *Built*: + "Gaza time (§11)" [C1], "the occupancy reads of
   `visits`, `subscriptions`, `customers` and `announcements`" [C2]; §11: "Built" for the library, "`@date-fns/tz`
   alone" (the `date-fns` mention corrected) and the shared calendar file [C1]; §9 *occupancy*: no change
   of rule (built as written).
4. **`docs/backend/security.md`** — header and *Authorization*: `requireCan` on "the live status's
   override" [C3].
5. **`docs/features/occupancy.md`** — *What it does*, *Who uses it* (reception reads the state and the
   people; the public its state through the directory), *Responsibility boundary* (owns *present*, the
   status, the override; reads `visits`, `subscriptions`, `customers`, `announcements`, `spaces`),
   *Behaviour and flows* (the read; the override), *API decisions* (P2, P3, P10, O3, S6), *Code map*,
   *API history* [C2, C3].
6. **`docs/features/directory.md`** — *What it does* (the live state), the line "Live status … not built"
   narrowed, *Responsibility boundary* ("Leaves the live status to `occupancy`" kept, step 7 removed),
   *How it composes* (`availableNow` resolved to ids by `occupancy` first), *API decisions*, *API history*
   [C4].
7. **`docs/README.md`** — the map's `occupancy.md` line: "a space's state now: its private capacity, who is
   present, the live status and its override (API only)" [C2].
8. **`docs/plans/v1-mvp.md`** — step 7: "**Built:** … (#PRNUM)" [C2–C4]; *Ordering notes*: "Until the
   front desk (step 7), Home, the directory and the space page show no live state" → "The directory's API
   carries the live state since step 7 (#PRNUM); Home and the pages show it with their screens" [C4];
   *Planned API surface*: the `/spaces?availableNow=`, `/spaces/:slug/occupancy`, `…/occupancy` and
   `…/status-override` rows removed into the *Built* sentences [C2–C4].
9. **`docs/project/overview.md`** — *Built*: an *Occupancy* line (the staff's live read and the override,
   on the API) [C2, C3]; the *Directory* line gains the live state [C4].

### PR 2
1. **`api-contract.md`** — §1's *Idempotency key*: "Not built yet …" → "Built for a visit's check-in and
   check-out; a key missing or not a UUID answers `validation` (422) on `idempotencyKey`" [C2]; new section
   *Front desk (managed)*: `POST …/visits` [C2], `POST …/visits/:visitId/check-out` [C3], `GET
   …/visits/:visitId`, `GET …/visit-terms` [C4], with `DeskVisit`, `VisitCheckOut`, `VisitPayment`,
   `VisitTerms`, the warnings, the retry rule (S3), P6's quote time; *Occupancy (managed)*'s `PresentPerson`
   gains `chargeNowAgorot` [C4]; §6: `SPACE_FULL` [C2], `PAYMENT_EXCEEDS_DUE`, `PRICE_TYPING_NOT_ALLOWED`
   [C3].
2. **`data-model.md`** — *Constraints worth stating*: the reason's `CHECK`; the ledger's bullet: "a visit is
   paid only once its charge is set (its own constraint, `payments_visit_uncharged`)" [C1]; *Visit* entity:
   "… and who typed it, and why" [C1]; *Visit charge*: P8's rates (shift fallback per §13 Q4), P7's
   rounding [C3]; *Unpaid visit*: "the customer with that phone among those not archived (created if new,
   with the name given or the visit's)" [C3].
3. **`conventions.md`** — header *Built*: + "the idempotent creates of the desk (visits)", "the ledger's
   translation table" [C2, C3]; §4: the table is built in `shared/errors` with its first lines [C3]; §13
   *Idempotency*: S1's sentence ("read first, under the space's lock; the unique key the backstop") [C2];
   §9 *The front desk*: unchanged rule, built for visits [C3].
4. **`security.md`** — *Authorization*: `requireCan` on the desk's writes; "a price typed by hand: `can()`'s
   `prices.typeByHand`, from the space's switch" [C3].
5. **`docs/features/visits.md`** (new) — the visit: check-in's rates, the charge's rule's home (linked to the
   data model), the quote, the terms; *API decisions*: P6, P7, P8, P9, S3 [C2–C4].
6. **`docs/features/desk.md`** (new) — the orchestrations; the transactions and their order (P4); the
   customer found by phone (O5); S1; *Who uses it* (the owner and reception); the shared device not settled
   (O4) [C2, C3].
7. **`docs/features/payments.md`** (new) — the first slice: a visit's payment at its check-out; the ledger's
   rules the database owns; the translation table; finding 15 [C3].
8. **`docs/features/occupancy.md`** — the full warning's input; the charge so far [C2, C4].
9. **`docs/README.md`** — map lines for `visits.md`, `desk.md`, `payments.md` [C2, C3].
10. **`docs/architecture/findings/15-the-payments-migration-predates-adr-0015.md`** — *Status:* Resolved;
    *Resolution (<date>, #PRNUM):* "item 2: the insert trigger names an uncharged visit
    `payments_visit_uncharged` (migration `desk_visit_charge`); the translation table maps
    `payments_within_due` to `PAYMENT_EXCEEDS_DUE`, proven through the check-out; item 1 stays accepted";
    index moved [C3].
11. **`v1-mvp.md`** — step 7's *Built* line (the visit) and its *Closes* noted done; the surface's
    `…/visits` and `…/check-out` rows into the *Built* sentence [C2, C3].
12. **`overview.md`** — *Built*: a *Front desk* line (checking visitors in and out, on the API) [C3].

### PR 3
1. **`api-contract.md`** — new section *Internal*: `POST /internal/jobs/run` (the secret, 401, the answer,
   500, not mounted without `JOBS_SECRET`) [C2]; *Front desk (managed)*: the unpriced close (Q4), `GET
   …/unpriced-visits`, `PUT …/visits/:visitId/charge` [C3], `GET …/uncollected-visits` [C4]; §6:
   `VISIT_NOT_PRICED`, `VISIT_ALREADY_PRICED` [C3].
2. **`data-model.md`** — *Auto check-out*: D-PR3-1 (23:59 on a closed day or after closing), "closed at its
   due time, charged to it" [C1, C2]; *Uncollected visits*: "… the unpriced ones included" [C4]; a new
   *Unpriced visit* bullet (Q4) [C3].
3. **`conventions.md`** — header *Built*: + "the scheduler port (§12)"; §1's `jobs/` line unchanged; §12's
   *Scheduler* row: "`POST /api/v1/internal/jobs/run`, behind `JOBS_SECRET`, every 5 minutes from an
   external cron; locally the same run every 5 minutes from `server.ts`" [C2]; §9 *Composed reads*'s
   uncollected line: D-PR3-4 [C4].
4. **`security.md`** — *HTTP hardening*: "`JOBS_SECRET` is a secret: required in production, compared in
   constant time, never logged" [C2]; *Authorization*: pricing a visit by `prices.typeByHand` [C3].
5. **`docs/development/setup.md`** — *The API* › new *Timed jobs*: O2's runbook line [C2].
6. **`apps/api/.env.example`** — `JOBS_SECRET=` with its comment (the endpoint mounted only when set;
   required in production) [C2].
7. **`visits.md`, `desk.md`, `payments.md`** — the auto check-out (D-PR3-1…3), Q4, the pricing, the
   uncollected read; *API history* [C2–C4].
8. **`docs/features/spaces.md`** — *Code map*: the auto check-out's due time in `spaces` [C1].
9. **`v1-mvp.md`** — step 7's *Built* complete, *Settles* done (the scheduling mechanism); the surface's
   remaining step 7 rows removed [C2, C4].
10. **`overview.md`** — *Front desk* line: + auto check-out, unpriced and uncollected visits [C4].

## Appendix B — Claude Code skills, only a map

| Step | Skill (if the executor is Claude Code) |
|---|---|
| §12.1, the branch | `start-work-item` (its git part) |
| Each test red first, each break | `superpowers:test-driven-development` (workflow §10) |
| Each new error code (§13 Q2) | `add-error-code` |
| Any failure | `superpowers:systematic-debugging` |
| §12.4 before any claim | `superpowers:verification-before-completion` |
| §12.7–12.8 | `open-pr`, then `final-report` |

Only a map: the plan and the documents decide; a skill that disagrees with them loses.
