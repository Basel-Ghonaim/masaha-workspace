# Review — ANNOUNCEMENTS PR 1 (#112, `feat/announcements`) — independent reviewer

- **Head:** `fdae748b0fc21e948f362cd7522682a38b69dc19` · `mergeStateStatus: CLEAN` · base `origin/main` (merge base `8fc5939e`).
- **CI:** `gh pr checks 112`: all green (build, check:classes, check:links, format:check, lint, test:api, test:component, test:unit, typecheck; CodeRabbit "pass", rate limited, so no review from it).
- **Head moved?** No. `gh pr view 112 --json headRefOid` at the end gives `fdae748b` again.
- **How I read it:** only commit objects (`git diff origin/main...fdae748b`, `git show fdae748b:<path>`). Nothing run, checked out or edited. Note: partway through, this worktree's `FETCH_HEAD` was overwritten by another process's fetch (`e4e13e9e`, worker A's space-links branch). From then on every read was pinned to `fdae748b`, and the one file read from the wrong commit (conventions.md) was read again at `fdae748b`.

## Verdict

**Mergeable.** No blocker and nothing serious. Three small document fixes go to ANNOUNCEMENTS PR 2's first commit through `0_CARRIED_FROM_112.md`. The rest are nits.

## Findings, most severe first

### F1 — should-fix (small) · conventions §9 *Composed reads*: the new bullet splits the customers list from its sub-bullets
- **Where:** `docs/backend/conventions.md:284` at `fdae748b`.
- **What I saw:** the new top-level bullet "**The managed announcements list and its summary** → `subscriptions`…" sits between "**The customers list and the customer file** → `desk`." (line 283) and that bullet's own sub-bullets (line 285 on: "The status and payment filters resolve to customer ids…", "`customers` then applies the search…", "The file adds each subscription's progress…").
- **What goes wrong:** rendered, the customers list's three sub-bullets now sit under the announcements bullet. The page says the announcements list filters by subscription and payment status and pages customer ids. That is false, in a Contract-class document.
- **Fix:** move the announcements bullet below the customers list's last sub-bullet, at the same level as the other composed reads.
- **Where the fix belongs:** PR 2's first commit (`0_CARRIED_FROM_112.md`).

### F2 — should-fix (small) · `announcements.md` leaves out the public read that `directory.md` hands to it
- **Where:** `docs/features/announcements.md` (new), *What it does*, *Who uses it*, *Behaviour and flows*, *History*.
- **What I saw:** the code has `announcements.publicOf(spaceId, take)` (`announcements.service.ts`, repository `publicOf`: not deleted, `endsAt` null or after now, by `startsAt` then `id`, `take`). `directory.md` now says: "**Leaves** which announcements the public sees, and their order, to [`announcements`]". The `docs/README.md` map line for `announcements.md` says "…and the public ones". The capability document itself never names the public read: no line in *What it does*, the directory missing from *Who uses it*, no flow, and the history line lists only the staff's writes and the managed pages.
- **What goes wrong:** the rule's owner, by the document's own boundary, does not state the rule. A reader sent there by `directory.md` finds nothing. This breaks "one home per fact": the rule now lives only in the contract and in `directory.md`'s wording.
- **Fix:** in `announcements.md`, add a *What it does* line ("Answers a space's running and upcoming announcements, not deleted, by start then id, up to the count the caller gives, for its public page"), add [`directory`](directory.md) to *Who uses it*, and add the public read to *Behaviour and flows* and to the #112 history line.
- **Where the fix belongs:** PR 2's first commit.

### F3 — nit · The contract states the owner's overview as built
- **Where:** `docs/api/api-contract.md`, `GET …/announcements/summary`: "(the owner's overview reads the same count)".
- **What I saw:** no `overview` module exists. Conventions §9 (line 284) and `closures.service.ts`'s comment both say "will read".
- **Fix:** "the owner's overview will read the same count". The executor's line for `OPEN_DECISIONS.md` (report §9) has the same tense, "which the overview (step 12) reads"; it should say "will read" too.
- **Where the fix belongs:** PR 2's first commit, with F1 and F2.

### F4 — nit · Start now skips S5's 365-day period bound
- **Where:** `apps/api/src/modules/announcements/announcements.service.ts`, `start()` (`repository.update(announcementId, { startsAt: at }, tx)`, with no `periodErrors`).
- **Scenario:** post an upcoming announcement starting in 300 days, ending 365 days after that (both bounds pass: start ≤ 365 ahead, end ≤ 365 after start). Then `POST …/start`. The start becomes now and the end stays 665 days ahead, so the period is 665 days. S5 says "an end at most 365 days after its start". An edit that moves the start does check this (`checks.startsAt` → `tooLong`); start now does not.
- **Why only a nit:** it needs a deliberately far-off upcoming announcement. Nothing breaks: no constraint, and no extension until PR 4, where D10 caps the proposal at 365 days anyway.
- **Fix:** none needed now. If the owner wants S5 held on every path, `start()` refuses with 422 `endsAt` `out_of_range` (or clamps). Otherwise the contract says the bound applies to the post and the edit only. **Record it as finding 150 if the owner prefers to leave the code.**

### F5 — nit (plausible: a design question, not a defect) · A retry after a delete answers the deleted announcement as live
- **Where:** `announcements.service.ts` `create()`, which calls `repository.findByKey()` ("deleted or not") and then `toAnnouncement(recorded, now())`.
- **Scenario:** reception posts a closure with key K and the answer is lost. The owner deletes the closure. Reception's client retries K. It gets 201 with `state: 'RUNNING'` (or whatever the instants give) for a row that has left every read. The client shows a closure that does not exist.
- **Why plausible, not a defect:** ADR 0015 rule 3 and conventions §13 say "a retry returns the first result… never a conflict", and the contract says "as it is now". The code follows both, and ADR 0015 says nothing about a record deleted in between. The window is tiny: a retry arriving after another person's delete.
- **Fix, if the owner wants one:** none in code. The contract's POST line adds "a retry of a deleted announcement answers it as it was" (or a 404). This is a decision, not a bug: record it, don't fix it now.

### F6 — nit · History lines out of order
- `docs/features/desk.md:109–110`: `#112` comes before `#110`.
- `docs/features/subscriptions.md:99–100`: `#112` comes before `#109`.
- **Fix:** put `#112` last in each list. **Where:** PR 2's first commit, with F1–F3.

## Departures, each judged

1. **The migration written from `migrate diff`, not `--create-only`.** *Seen in the code:* `20261024095504_announcement_key/migration.sql` is D12's SQL statement for statement: a nullable `ADD COLUMN "request_id" UUID`, the `gen_random_uuid()` backfill, `SET NOT NULL`, then `CREATE UNIQUE INDEX "announcements_space_id_request_id_key" ON ("space_id","request_id")`. That index name is Prisma's default for the schema's `@@unique([spaceId, idempotencyKey])` on `request_id`, so the schema and the migration agree. There is no other schema change: the Prisma diff is the field, its doc comment, the realignment and the `@@unique`. *Only in the report:* `migrate status` up to date and both databases migrated (CI's test:api green on the head supports it). **Accepted.**
2. **The demo seed's closure gains a key.** *Seen:* `demoDirectory.ts:682`, `idempotencyKey: randomUUID()`, nothing else. It is required by `NOT NULL`, and §12.2 check 3 covers an extra insert. A10's "no announcement" was simply wrong. **Accepted.**
3. **`liveStatus.api.test.ts`'s page keys gain `announcements`.** *Seen:* one key added, plus the key on its insert. The test lists the page's keys exactly, so the new field had to appear there. **Accepted.**
4. **T10 widened** (the list in C3, the public page in C4, `seedSettings()` in the lifecycle file). *Seen:* it asserts the managed list `[]`, the page `announcements: []` and the live status `null` after a delete. This is the AC's "leaves every read" made real. **Accepted, a gain.**
5. **T18 widened to the subscriber's check-in.** *Seen:* `checkIn.api.test.ts` adds `POST …/check-ins` → `['SPACE_FULL', 'CLOSURE_IN_FORCE']`. This is the AC's second half. Without it, A5 would be assumed, not proven. **Accepted, a gain.**
6. **B18's test fix folded into C3.** *Seen:* in T12's data, the ended row that ended last started last (`days(-0.75)` against `days(-10)`), with a comment that an order by start fails. *Only in the report:* B18 red after the fold. A fold before the push is the standing rule; no fix commit remains. **Accepted.**
7. **B6's restore cleared `announcements` on `masaha_b_test`.** *Only in the report.* It touched the test database only, and every test resets it. **Accepted.**
8. **The `OPEN_DECISIONS.md` line left in the report §9.** The exec prompt §1.10 ("Write nothing outside the repository except this folder's report and `scripts\`") is newer than the plan's §12.8 and binds the executor, so leaving the file alone was right. The line is true to the code (`closures.summary` exists; no email is sent), except its tense (F3). **Accepted. The owner or the analyst applies it, with "will read".**
9. **(7) The instant and `since`/`take` passed between modules.** *Seen:* `closures.service` reads its own clock once, then passes `at` to `announcements.page/counts/startedClosureIds`, and `since = at − 30 d` to `startedClosureIds`. `directory` passes `PUBLIC_ANNOUNCEMENTS_MAX` to `announcements.publicOf`. **This is a boundary the conventions allow:**
   - R4 is a direct call to a lower module's public API (L3 → L2 and L5 → L2, both through `index.ts`, and lint is green in CI).
   - R5 prefers "passing a parameter" over any port.
   - §11's one clock is kept: the instant comes from the injected clock, and no rule calls `new Date()` for "now".
   - Precedent already on `main`: `announcements.closedAt(spaceIds, now, tx)` and `occupancy.checkInWarnings(spaceId, now, tx)` take the caller's instant.
   - Q6's 30-day rule stays with the summary's owner (`subscriptions`, S10). `announcements` only offers a neutral `since` filter, so no rule is copied.
   - One instant per summary keeps the tab counts and the awaiting count consistent.
   - `take` comes from `directory` because `PUBLIC_ANNOUNCEMENTS_MAX` is in `@masaha/shared/directory` (D2), which an L2 module may not import (§7).

   Cosmetic: `publicOf` reads its own clock while `page`/`counts` take `at`, two styles in one service. **Accepted.**

## Checked and fine (seen in the code)

- **Authorization.**
  - Both routers are mounted on `manage` (`app.ts`), behind `requireSpaceAccess`.
  - Every write has `requireCan('announcements.manage')` (staff) before the key and the body, and the service's `lockFor` checks `can()` again on `space.linksUnder(tx)` under `spaces.lock`.
  - The reads ask no `can()` (#86).
  - Nothing owner-only is touched: the extension is PR 4's.
  - Another space's id: `lockIn` filters `space_id` in the `FOR UPDATE`, so it is 404 (T11, B17). The list, the counts and the started closures filter by `spaceId`.
  - A stranger, another space's owner and the admin get 404 on every route (T6, T15).
  - A reception link ended while the post waits is refused 403 (T5, B11).
- **Idempotency and races.**
  - The key is unique per space (`@@unique([spaceId, idempotencyKey])`; D1 test, B6), so another space's same key is a new post.
  - `findByKey` is read under the space's lock, after `can()`.
  - A retry answers the first row with 201, before the period is re-checked, so a retry after the end passed still answers.
  - Two at once with one key make one (T2 with `waitingOnLock({ count: 2 })`, B8, B9).
  - A key reused with another body answers the first, as ADR 0015 rule 3 and the contract say; the plan names no refusal.
  - Lock order: the space's row, then the announcement's, the same as the other desk writes (space first). Check-ins read announcements unlocked inside their transaction, so no orders cross.
- **The state (D3).**
  - `announcementState`, `STATE_WHERE`, `counts`' `FILTER`s, `publicOf` and `closedAt` use the same comparisons (`startsAt ≤ now`, `endsAt > now` or null). Boundaries are in U1.
  - End: upcoming gives 409 `ANNOUNCEMENT_NOT_STARTED`, ended answers as is, running gets end = now.
  - Start: only an upcoming one; others answer as is.
  - Delete: any state, soft; a repeat is 204 with nothing written.
  - Each change is audited with D7's before/after.
  - Raw-SQL `Date` parameters have precedent (`sessions.repository.ts:176`, `rate-limit/counter.ts:35`).
- **Gaza time.** PR 1 has no calendar-day rule: instants only. S4 is PR 4's `closureSpan`. The 30-day window is 30 × 24 h of instants, which matches "started within the last 30 days" whatever a DST change does to the wall clock.
- **S5.** The post checks both bounds, `endsAt` after now and ≤ 365 days after the start (U2, T4). An edit checks only what it changes and the merged end against the merged start (U2, the edit's 422 test). The schema refines end > start. The one gap is F4.
- **The list and the summary (D4, S10, Q6).**
  - Composed in `subscriptions/closures/`, with the writes in `announcements`.
  - Orders: running and upcoming by start then id; ended by end desc then id desc (T12, B18).
  - `extension` is on `CLOSURE` rows only, `null` before one (T13, with its count from `_count.subscriptions`, B19).
  - The summary counts closures started in `[at − 30 d, at]`, not deleted, minus the extended ones. T14 proves that a 31-day-old, an upcoming, a deleted, an outage and another space's closure are not counted.
  - The query count is fixed whatever the page size: one page + count, one extensions query, one names query.
- **The public page (D5).**
  - The announcements are read only after `view` is found, so an unlisted, hidden or deleted space is 404 before anything of it is returned.
  - Its `state` is stripped.
  - The page shows running and upcoming only, never ended, deleted or another space's (T16, B22); at most 20, by start (T17, B23).
  - Express's weak ETag is computed from the body (`directory/cache.ts`), so a new announcement changes it.
- **The closure warning (D6).**
  - `checkInWarnings` appends `CLOSURE_IN_FORCE` after `SPACE_FULL` and `OUTSIDE_OPENING_HOURS`, from `closedAt` in the same `tx`, and never refuses. It reaches both check-ins (T18, B24).
  - `DESK_WARNINGS` places it third.
  - *Present* is untouched: `present.api.test.ts` changed only its inserts' keys.
  - The live status and the directory are unchanged apart from the keys.
- **Codes.** `ANNOUNCEMENT_NOT_STARTED` and `CLOSURE_IN_FORCE` are in `core/errors.ts`, both catalogues word for word as in Q1 (Arabic «لم يبدأ هذا الإعلان بعد.» and «المساحة معلَنة مغلقة الآن، وسُجّل الحضور رغم ذلك.»), and api-contract §6.
- **Scope.** 55 files, all under `apps/api`, `packages/shared`, `docs`, the two `errors.ts` and `apps/web/src/test/publicSpace.ts` (one line, `announcements: []`). No dependency change. Nothing from the *Not in v1* list.
- **Commits.** Five subjects, 48 / 45 / 49 / 45 / 46 characters, each with a body saying why. No tool attribution, no fixup left.
- **Documents.** `#112` is wherever a number goes. Built claims are limited to the API: the screens are said to be planned, and `directory.md` says the page's announcements are not shown on the site. The contract, data model, security, `occupancy.md`, `desk.md`, `subscriptions.md`, v1-mvp, overview and the README map are true to the code, except F1–F3 and F6.
