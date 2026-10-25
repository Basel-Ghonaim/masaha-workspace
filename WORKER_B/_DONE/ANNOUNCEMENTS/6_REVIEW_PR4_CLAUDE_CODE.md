# Review — ANNOUNCEMENTS PR 4, #123 `feat/closure-extension`

- **Head:** `ff8743c89b769c7808977d2967c766ed5fe16a40`, base `origin/main` = `3855e37f` (the merge base). Every read
  is pinned to that sha (`git show ff8743c8:…`, `git diff origin/main...ff8743c8`).
- **CI:** all green on the head (`gh pr checks 123`): lint, typecheck, test:unit, test:api (7m48s), test:component,
  build, check:classes, check:conflicts, check:links, format:check, CodeRabbit. `mergeStateStatus` CLEAN.
- **Head moved:** no. Re-read at the end: still `ff8743c8…`, CLEAN.
- **Files:** 42, one migration, no dependency, `apps/web` limited to the two `errors.ts`.

## Verdict

**Mergeable.** No blocker and no should-fix in the PR's code. Three small nits go to worker B's next PR. One
decision-level gap (finding 1) should be recorded as a finding for the owner. It does not block, because the PR
implements decision 4 as the owner approved it.

## Findings, most severe first

### 1. Finding to record (151): a renewal sold before the extension stays where it is, and the renewed subscription is moved into it

- **Where:**
  - `apps/api/src/modules/subscriptions/closures/closures.repository.ts:50-54`, the covered fragment;
  - `closures.service.ts:152`, the move;
  - `apps/api/src/modules/subscriptions/renewal.ts:17`.
- **Seen in the code:**
  - A renewal's proposed start is `addDays(renewed.endsOn, 1)`, the day after the old subscription's end.
  - The covered rule ignores `renewal_of_id`.
  - `moveEnds` moves only the covered ids.
  - `currentSubscription.ts:22-38` picks, of two running subscriptions, the one with the latest start. Its header says "Two may run at once (the owner's decision 2)".
- **Scenario:** subscription S runs 11-01 → 11-30. The desk renews it early, so R runs 12-01 → 12-30. A closure covers
  11-08 → 11-10, and the owner extends by 3.
  - S now ends 12-03. R is not covered, because it starts after the last day, so it still starts on 12-01.
  - From 12-01 to 12-03 both run, and R is the "current" one. The customer's three days run alongside the renewal
    they already bought, and they finish on 12-30 as before. The compensation is effectively lost.
- **Not seen:** plan §10 names only the other overlap case (a renewal started *during* the closure). Its effect on
  the desk's check-in choice is only partly verified: I saw the current-subscription rule, but not which
  subscription the desk checks in when two run. **Plausible** in effect; the mechanism is seen.
- **Fix (owner's decision):** for example, move a covered subscription's not-yet-started renewal chain by the same
  days, or leave it and state the case in the contract.
- **Where it belongs:** a finding to record, number 151 (151–159 are free on `main`). It is not a fix on this PR.

### 2. Nit: a key retried against another space's URL answers that space's extension

- **Where:** `closures.service.ts:135-141`.
- **Seen:** `findByKey(key, tx)` is global, since the key is unique on its own (S11). The retry only compares
  `recorded.announcementId !== announcementId`. It never checks that this closure is the URL's space's: the closure
  is read only later, by `lockClosure(space.id, …)`.
- **Scenario:** the owner of space B calls
  `POST /manage/spaces/B/announcements/<A's closure id>/extend-subscriptions` with the key that extended A's closure.
  The answer is 201 with A's extension: its days, its count, and the applier's id and name. The space check would
  have answered `not_found`.
- **Risk:** exploiting it requires another client's UUID, so the risk is negligible. It is still a cross-space read
  that the boundary otherwise forbids.
- **Fix:** have `findByKey` also select the extension's announcement's `spaceId` and treat another space's as
  `conflict` (or `not_found`). Alternatively, read `closureIn(space.id, id)` with `tx` before answering a retry. Add
  one line to T5.
- **Where it belongs:** worker B's next PR, first commit (`0_CARRIED_FROM_123.md`).

### 3. Nit: `data-model.md:23` says the extension's key is "unique within its space"

- **Where:** `docs/architecture/data-model.md:23` (*Conventions › Idempotency*).
- **Problem:** the PR adds "a closure's extension, 2026-10-26, #123" to the list that sentence governs. The schema
  (`@unique`, `closure_extensions_request_id_key` on `request_id` alone) and the same document's line 140 say the key
  is unique on its own. Two homes now disagree.
- **Fix:** add "(unique on its own: it has no space column)" after the extension in line 23, or leave it out of that
  list and link line 140.
- **Where it belongs:** next PR, first commit.

### 4. Nit: `subscriptions.md`'s API history is out of order

- **Where:** `docs/features/subscriptions.md:110-111`. The `#123` line is inserted above the `#118` line, where every
  other line is in PR order.
- **Fix:** move `#123` below `#118`.
- **Where it belongs:** next PR, first commit.

## The two codes, quoted

Both lines are byte-identical to the approved text: the same pattern matched both `2_PLAN.md` and the head's
`arabic/errors.ts`.

- `CLOSURE_EXTENDED` (409), Arabic as Q1 approved:
  «مُدّدت الاشتراكات بسبب هذا الإغلاق، فلا يمكن حذفه ولا تغيير نوعه أو بدايته ولا تأخير نهايته.»
  English (§13 Q1, unchanged): "Subscriptions were extended for this closure: it is not deleted, and its type,
  start and later end stay as they are."
- `CLOSURE_ALREADY_EXTENDED` (409): «مُدّدت اشتراكات هذا الإغلاق من قبل.» — "This closure's subscriptions were
  already extended."
- Where they appear: in `packages/shared` `DOMAIN_ERROR_CODES`, after `ANNOUNCEMENT_NOT_STARTED`, and in both
  catalogues and contract §6. `CLOSURE_EXTENDED` comes from the trigger through `constraintCodes.ts`
  (`announcements_closure_extended → conflict`), never a 500. T12 asserts 409 on all five refusals; that its break
  (B20) answered 500 is only in the report.

## Departures and decisions taken without the owner, each judged

1. **`daysFrom` moved to `packages/shared/src/core/gazaTime.ts`:** **right**, and `subscriptionStatus` behaves
   exactly as before.
   - Old: `Date.parse(`${to}T00:00:00Z`) − Date.parse(`${from}T00:00:00Z`)` over 86 400 000.
   - New: `utcDay(to) − utcDay(from)`, where `utcDay` is `Date.UTC(y, m − 1, d)`. That is the same UTC-midnight
     arithmetic for every `YYYY-MM-DD`. Both call sites (`subscriptionStatus.ts:53,55`) are unchanged, and the
     private copy is deleted, so one function remains.
   - U1 covers month, year, leap day, negative and DST. That the subscriptions unit tests passed (25) is only in the
     report; CI's test:unit is green.
2. **`lockClosure` = `repository.lockIn` plus the `CLOSURE` check:** **right.** `lockIn` takes `FOR UPDATE` by id and
   space, then reads the row and treats a deleted one as `null`. The type is checked on the row read after the lock,
   so a type changed while it waited is seen. There is no second lock statement.
3. **The migration made by `migrate diff --script`:** **right.**
   - Read whole: nullable add, then `gen_random_uuid()` backfill, then `SET NOT NULL`, then the unique index. The
     function and trigger match D12 word for word. No PR number in the SQL.
   - The Prisma line (`idempotencyKey String @unique @map("request_id") @db.Uuid`) names exactly the index the SQL
     creates (`closure_extensions_request_id_key`), so there is no drift by name.
   - That `migrate dev` proposed nothing more is only in the report (not run here).
4. **`isExtended` / `createExtension` names, with the links folded in:** **right.** Still two statements, both on `tx`.
5. **`list.api.test.ts` gains keys:** **right.** The column is required, and that file inserts extensions.
6. **T9 inserts a covered subscription instead of a renewal that starts after the last day:** **right.**
   - The planned row could never be covered, so it could not show the race. The covered insert, plus the early end
     of `through`, shows that the set is read as committed under the space's lock.
   - The "renewed" wording of D13's race is covered in substance: a renewal is an insert.
   - See finding 1 for what a renewal *outside* the span does.
7. **U2's and D1–D2's red came from "Cannot find module" and from breaks B5–B6:** **acceptable** under the owner's
   rule. Each break is a guard the red step did not prove.
8. **`OPEN_DECISIONS.md` not written:** **right.** The prompt (§1.6) allowed only the report outside the
   repository. The supervisor owes that line.
9. **Decision 1 (an applied preview's `subscriptions` is how many it moved, with the span recomputed at now):**
   **right.** It matches the list's `extension.subscriptions`, and the contract's `ExtensionPreview` comment says it
   ("once applied, how many it moved"). The PR description does not list it among its decisions; that is worth a
   line, not a finding.
10. **Decision 2 (API lane re-run once after a memory kill):** **right**, per the owner's memory rule. CI's
    test:api is green on the head.
11. **Decision 3 (B6 restored after deleting `masaha_b_test`'s extension rows):** **acceptable.** It touched only
    the test database, which every test resets.

## Checked and fine

**The migration and the trigger**
- The trigger's condition is exactly D12/S3. An earlier end and end-now pass. A later end is refused. `NULL`
  is handled both ways: an end removed is refused, and an end given to an open one passes.
- `WHEN (OLD."type" = 'CLOSURE')` catches a closure retyped *to* anything, because OLD is still `CLOSURE`.
- No extension can exist on a non-closure: the apply checks the type under the lock.
- The only `announcement.update` in the code is `announcements.repository.ts:183`. No `updateMany` and no raw
  `UPDATE` exist outside migrations, so every edit and soft delete fires the trigger. A hard delete is held by the
  FK's `RESTRICT`.

**The apply** (`closures.service.ts:128-176`) follows D11's order:
- `spaces.lock`, then `can()` on `space.linksUnder(tx)`;
- `findByKey` (same closure → its stored result, read through `tx`, `namesFor(…, tx)`, 201; another closure →
  `conflict`);
- `lockClosure`, then `isExtended` → `CLOSURE_ALREADY_EXTENDED`, then started, then the span at `now()`;
- `lockCovered` (`ORDER BY "id" FOR UPDATE`), then one `UPDATE … "ends_on" + ${days}::integer … ANY(${ids}::integer[])`;
- the extension and its links (`createMany`), then the audit;
- every read inside goes through `tx`, and a retry answers the stored row, not a recomputation.

**The covered rule and the days**
- Covered rule: one `Prisma.sql` fragment, used by both `coveredCount` (no `tx`, no lock, no write) and
  `lockCovered`. It is exactly D11's five clauses.
- `closureSpan`: Gaza dates by `gazaClockOf`; `endsAt − 1 ms` only once ended; `now` while running. Midnight and
  23:30 UTC are tested.
- `proposedDays = min(days, 365)`. `extendSubscriptionsSchema` is `int().min(1).max(365)` in `packages/shared`;
  365 passes; 0 and 366 are 422 at the API.

**Authorization and races**
- The route order is `requireCan('subscriptions.extendAfterClosure')`, then `requireIdempotencyKey`, then
  `validate`. T4 sends reception with no key and a bad body and gets 403. The stranger and the admin get 404 from
  the boundary on both routes. `can()` runs again under the lock (T11).
- The tests reach the planned behaviours:
  - T5: retry, another key, a key reused on another closure;
  - T6: `waitingOnLock({ count: 2 })`, [201, 409];
  - T9–T11: `whileHeld` on the space's row;
  - D1: type, start, delete, later end, end removed, text, earlier end, an open one given an end, another closure
    untouched;
  - D2: the key;
  - T12: 409 `CLOSURE_EXTENDED` on all five refusals, with nothing written and only the extension audited.
  
  The breaks' red lines (B1–B20) are only in the report. Each test as written would fail under its named break.

**Carried from #121**
- Item 1: `isListed` is read before `runInTransaction`. Inside, the order is the lock, then already saved → 204,
  then `!listed` → `not_found`, then the ceiling, then the insert. No answer changes.
- Item 4: (a) hidden then saved again → 204, one row; this would fail with the listed check moved ahead. (b) an
  inactive-area favourite → `listed: false` with its name. Both are real tests.
- Items 2, 3, 5 are true to the code: `orderBy: [{ createdAt: 'desc' }, { spaceId: 'desc' }]`, and the dates and
  `directory.md`'s Authority are as the file asked.
- #120 item 4 stays open (only `src/app.ts` is touched), as allowed.

**The documents**
- The contract's two routes and §6, the data model (*Constraints*, *Derived values*, *ClosureExtension*, *Checked by
  the service*), ADR 0009's row and *Revised*, conventions §6, §7 row, §13 and *The ledger's rules*, security,
  `announcements.md`, `v1-mvp.md` and `overview.md` (line 62 and *Built*) are all true to the code and carry `#123`
  and the date. Findings 3 and 4 above are the exceptions.
- `subscriptions.md` keeps #122's line ("a customer's file … ends it early (`POST …/end`) (2026-10-25, #122)").

**Scope and history**
- Scope: `apps/api`, `packages/shared`, `docs`, and the two `errors.ts`; one migration; no `package*.json`.
- Commits: five subjects of 48, 45, 35, 50 and 43 characters, each with a body. No `fixup!` and no tool attribution.
