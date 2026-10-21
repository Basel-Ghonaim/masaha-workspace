# ANNOUNCEMENTS — announcements with the closure extension, data reports and favourites, on the API (build map step 10) — the plan

> **Base:** `origin/main` at `befd96f9` (Merge #101, `feat/directory-list`, 2026-10-21). **Not on `main` yet, and
> built before this item:** SUBSCRIPTIONS PRs 1–3 (#102 `feat/customers` open; PRs 2–3 planned in
> `C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\2_PLAN.md` with its approval note) and DEMO_SEED
> (`WORKER_B\DEMO_SEED\3_EXEC_PROMPT.md`). This plan builds on what they say they build (§3, *Assumptions*
> A1–A11); **its executor starts only after all of them have merged**, and §12.1 checks what merged against
> those assumptions.
> **Worker:** B, in `C:\dev\masaha\app-b`. **Folder:** `C:\dev\masaha\workspace\WORKER_B\ANNOUNCEMENTS\`: this
> plan `2_PLAN.md`; the reports `4_REPORT_PR<n>.md`; the executor's scripts in `scripts\` (never committed).
> **Four PRs in sequence**, each cut from the latest `origin/main` once the one before it has merged:
> **PR 1** `feat/announcements` (≈ 50 files, one migration) · **PR 2** `feat/data-reports` (≈ 40 files, one
> migration) · **PR 3** `feat/favorites` (≈ 22 files, no migration) · **PR 4** `feat/closure-extension` (≈ 30
> files, one migration). PRs 1, 2 and 4 touch authorization, transactions and the schema; PR 3 authorization and
> a transaction: each gets its own review conversation.
> **Read only from commit objects** (`git show origin/main:…`, `git grep`, `git ls-tree`, `gh`). Nothing was run,
> built, installed or checked out. Every point reading could not prove is an **executor check** (§12.2), with
> what to do if it fails.
> **In parallel:** worker A's PUBLIC (`apps/web`, `docs`). Its space-page PR consumes `GET /spaces/:slug` and
> `@masaha/shared/directory`, which PR 1 extends (`PublicSpace.announcements`) and PR 3 reads
> (`FavoriteSpace`). **Shared code files, each a likely text conflict:** `packages/shared/src/directory/
> {responses,index}.ts` (PR 1, PR 3), the web's `apps/web/src/shared/copy/{arabic,english}/errors.ts` (the
> error lines, every PR) and any web test fixture typed `PublicSpace` (PR 1, §12.2 PR 1 check 5). **Shared
> documents:** `docs/features/directory.md`, `docs/api/api-contract.md`, `docs/plans/v1-mvp.md`,
> `docs/project/overview.md`, `docs/architecture/findings/README.md`, `docs/README.md`.
> **Finding numbers:** this item's start at **150**. No finding is planned; any finding an executor records
> takes **150**, then 151, and so on, across the four PRs, in order.

> **Approved by the owner, 2026-10-21 — binding on every executor of this plan** (it wins where the plan
> below differs):
> - **Q1 — the codes:** the six as §13 lists them, the Arabic as written for five; **`CLOSURE_EXTENDED`'s
>   Arabic is «مُدّدت الاشتراكات بسبب هذا الإغلاق، فلا يمكن حذفه ولا تغيير نوعه أو بدايته ولا تأخير نهايته.»**
>   (its English unchanged).
> - **Q2 — S10:** the managed announcements list and its summary composed by `subscriptions` (A1, A2 not taken).
> - **Q3 — S3:** an extended closure's end may still come earlier, end now included; a later end, a new start
>   or type, and deletion refused (decision 6 refined).
> - **Q4 — the schema as planned:** PR 1 `announcements.request_id` (S1); PR 2 `data_reports.resolved_as` (S7),
>   the partial unique index and the three `CHECK`s (S6); PR 4 `closure_extensions.request_id` and the trigger
>   (S2, S11); PR 3 none.
> - **Q5 — S8:** a decision retried identically answers as it is; any other decision of a decided report → 409.
> - **Q6 — the overview's count:** only closures **started within the last 30 days** with no extension (decision 2
>   refined) — `closures.summary` says so, and its test proves a 31-day-old one is not counted.
> - **Q7 — S5's bounds** as written.
> - **Q8 — the order as decided:** announcements, data reports, favourites, **the extension last** (A8 not taken).
> - **Q9 — D9:** `sort=distance` with `Masaha-Near` on `GET /me/favorites` (AC-014), by the directory's privacy
>   rules (A5 not taken).
> - **Q10 — the web fixtures typed `PublicSpace`** (PR 1, §12.2 check 5): worker B edits **only the lines the
>   type change breaks**; if a worker-A PR touching those files is open when PR 1 is ready, PR 1 merges after it
>   and rebases.
> - **The owner's standing rules:** a small fix a review defers is the next PR's first commit
>   (`0_CARRIED_FROM_<n>.md`); a test seen red before its code is its own break, a separate break only for a guard
>   the red step did not prove; fix rounds run only what the change touches; a full lane killed for memory is
>   re-run once, then CI judges; a demo account or data lacking a real-run case → stop and report.

---

## 1. Summary

Step 10's API: a space tells its users what changes; users report wrong information and see the reply; users
keep their favourite spaces.

- **PR 1 — announcements.** The staff (owner and reception) post an announcement (idempotent: announcements
  gain their key), edit it, end it now, start it now, delete it (soft). The managed list is paged by state
  (running, upcoming, ended) and carries each closure's extension state; a summary answers the tabs' counts and
  the closures awaiting an extension, the read the owner's overview (step 12) will use. The space's public page
  carries its running and upcoming announcements. A check-in (a visit's, and a subscription's through the same
  warnings) during a running closure succeeds with the warning `CLOSURE_IN_FORCE`.
- **PR 2 — data reports.** A signed-in user reports a listed space's wrong information (10 an hour); a repeat
  while one is open answers the open one. The user's own reports, paged, with the reply and who wrote it
  (`repliedBy`), `listed: false` for a space that left the directory. The owner reads and decides the space's
  reports, never seeing the reporter; the admin reads all, named, and decides an unverified space's. Dismissing
  needs a reply; a decided report is final.
- **PR 3 — favourites.** Save and remove a listed space, idempotent, at most 200; the favourites answered whole
  as the directory's cards, `listed: false` for those that left, ordered by distance when the device's location
  is sent.
- **PR 4 — the closure extension.** The owner, once a closure has started, sees the days the server proposes and
  how many subscriptions it covered, types the days, and moves every covered subscription's end by them, once
  per closure, under one key. An extended closure keeps its type, start and existence; its text may change and
  its end may come earlier.

Nothing in `apps/web` except the error codes' catalogue lines and the `PublicSpace` fixtures the type change
breaks (worker B's licence). No booking, online payment, QR, claiming or reviews (overview *Not in v1*).

---

## 2. The contract

### Scope

**PR 1 — `feat/announcements`**
1. Migration `announcement_key`: `announcements.request_id` (UUID, required, backfilled), unique within the space.
2. `@masaha/shared/announcements` (new, L2); `@masaha/shared/directory` gains `PublicAnnouncement` on
   `PublicSpace`; `DESK_WARNINGS` gains `CLOSURE_IN_FORCE`.
3. `POST /manage/spaces/:spaceId/announcements` (🧾, `Idempotency-Key`), `PATCH …/announcements/:announcementId`
   (🧾), `POST …/:announcementId/end` (🧾), `POST …/:announcementId/start` (🧾), `DELETE …/:announcementId` (🧾).
4. `GET …/announcements?state=&page=&limit=` (🧾, paged, each closure with its extension state) and
   `GET …/announcements/summary` (🧾), composed by `subscriptions` (D4).
5. `GET /spaces/:slug` carries `announcements` (D5).
6. `occupancy.checkInWarnings` adds `CLOSURE_IN_FORCE` (D6).
7. Error codes `ANNOUNCEMENT_NOT_STARTED` (409) and the warning `CLOSURE_IN_FORCE`.
8. `docs/features/announcements.md` (new); `OPEN_DECISIONS.md` point 2 updated by the report.

**PR 2 — `feat/data-reports`**
1. Migration `data_report_rules`: the enum `DataReportResolver` and `data_reports.resolved_as`; the partial unique
   index of one open report per user, space and field (decision 9); `CHECK`s on a decision's fields, a
   dismissal's reply and «أخرى»'s message.
2. `@masaha/shared/data-reports` (new, L3).
3. `POST /spaces/:slug/reports` (👤, the 10-per-hour limit) and `GET /me/reports` (👤, paged).
4. `GET /manage/spaces/:spaceId/data-reports` and `PATCH …/data-reports/:reportId` (🏢).
5. `GET /admin/data-reports` and `PATCH /admin/data-reports/:reportId` (🛡).
6. Error code `REPORT_ALREADY_DECIDED` (409). `security.md`'s *Not yet built: the data-report limit* → built.
7. `docs/features/data-reports.md` (new).

**PR 3 — `feat/favorites`**
1. `@masaha/shared/favorites` (new, L2: `FAVORITES_MAX = 200`); `@masaha/shared/directory` gains `FavoriteSpace`.
2. `POST /me/favorites/:spaceId` and `DELETE /me/favorites/:spaceId` (👤, idempotent), in `favorites`.
3. `GET /me/favorites` (👤, whole; `sort=distance` with `Masaha-Near`), in `directory` (its new `me` router).
4. Error code `FAVORITES_LIMIT_REACHED` (409); api-contract §4 gains the exception (C8).
5. `docs/features/favorites.md` (new).

**PR 4 — `feat/closure-extension`**
1. Migration `closure_extension_key`: `closure_extensions.request_id` (UUID, required, unique); the trigger
   `announcements_guard_extended` (decision 6, S2).
2. `GET …/announcements/:announcementId/extend-subscriptions` (🧾, the preview: proposed days and the count) and
   `POST …/announcements/:announcementId/extend-subscriptions` (🏢, `Idempotency-Key`), in `subscriptions`.
3. Error codes `CLOSURE_ALREADY_EXTENDED` and `CLOSURE_EXTENDED` (409); `ANNOUNCEMENT_NOT_STARTED` reused.
4. `data-model.md` and `overview.md` rewritten for decision 4 (approved 2026-10-21); ADR 0009's row revised.

### Acceptance criteria

**PR 1**
- [ ] The owner and reception post an announcement: a type, Arabic text (required), English text (optional), a
      start (now when absent) and an optional end; audited; a retry with the same key answers the first, 201,
      never a second; two at once with one key make one.
- [ ] The period is checked: an end after the start, a new end after now, a start at most 30 days back and 365
      days ahead, an end at most 365 days after the start (S5); each refusal 422 on its field, writing nothing.
- [ ] An edit changes only what it sends (`textEn: null` clears, `endsAt: null` removes the end), audited with
      before and after; the same values write nothing.
- [ ] End now sets the end to now on a running one; an ended one answers as it is; an upcoming one is refused
      409 `ANNOUNCEMENT_NOT_STARTED`. Start now sets the start to now on an upcoming one; a started one answers as
      it is. Delete is soft (the row kept, `deletedAt` set), 204, a repeat 204 writing nothing; a deleted
      announcement leaves every read and the live status.
- [ ] The managed list pages one state (running and upcoming by start, ended by end, latest first), the total
      right; every closure carries `extension` (`null` until applied); the summary counts the three states and
      the started closures with no extension.
- [ ] A stranger, another space's owner and the admin get `not_found` on every route; a link ended while a write
      waits on the space's lock is refused 403.
- [ ] `GET /spaces/:slug` carries the running and upcoming announcements, never an ended or deleted one, ordered
      by start then id, at most 20, each with its start and end.
- [ ] A visit's check-in during a running closure succeeds 201 with `CLOSURE_IN_FORCE` in `meta.warnings`, after
      `SPACE_FULL` and `OUTSIDE_OPENING_HOURS`; the subscription check-in reads the same warnings.

**PR 2**
- [ ] A signed-in user reports a listed space's field group (`OTHER` with a message), 201 `OPEN`; an unlisted or
      unknown space is 404; anonymous is 401.
- [ ] The same user, space and field while one is open answers that report, 200, writing nothing; two at once
      make one; the database holds the rule (partial unique index).
- [ ] The 11th report of a user within the hour is 429 with `Retry-After`, counted at the route before the body
      is read, repeats included; another user at the same address is unaffected.
- [ ] `GET /me/reports` pages the caller's reports newest first, filtered by open or decided; each decided one
      carries its status, reply and `repliedBy` (`SPACE` or `MASAHA`, who decided, as stored); a space that left
      the directory carries `listed: false` and its name.
- [ ] The owner (🏢; reception 403 before anything is read) lists the space's reports, **never the reporter**
      (no name, id or email anywhere in the answer), and resolves (reply optional) or dismisses (reply required)
      an open one, audited; the admin lists every report with the reporter's name and decides an unverified
      space's only (403 for a verified one).
- [ ] A decided report is final: another decision is 409 `REPORT_ALREADY_DECIDED`; the same decision by the
      same person with the same reply answers as it is (S8).
- [ ] Who decides is read under the space's lock: an owner linked or unlinked while a decision waits decides it.

**PR 3**
- [ ] A signed-in user saves a listed space (204) and removes one (204); a repeat writes nothing; two at once make
      one; an unlisted or unknown space is not saved (404); the 201st is 409 `FAVORITES_LIMIT_REACHED`, the limit
      held under the user's lock.
- [ ] `GET /me/favorites` answers every favourite, newest saved first: a listed space as the directory's card with
      its live status; one that left with `listed: false` and its name; another user's never.
- [ ] With `sort=distance` and `Masaha-Near`, the listed ones nearest first with their distance, those that left
      last, `Cache-Control: no-store` (security › Location); the header without `sort=distance` is
      `invalid_choice` on `near`.

**PR 4**
- [ ] The preview answers the closure's first and last covered Gaza day, the proposed days and how many
      subscriptions it covered, writing nothing; an applied extension is answered instead of a proposal.
- [ ] Only the owner extends (reception 403 before the key or body is read), once the closure has started
      (`ANNOUNCEMENT_NOT_STARTED`), once per closure (`CLOSURE_ALREADY_EXTENDED`), 1–365 days.
- [ ] Every subscription of the space running on any covered day moves its end by the days typed — started on or
      before the last day, ending on or after the first, even one that ended during the closure; never one ended
      early or with no end; one `SubscriptionExtension` each; one transaction; audited.
- [ ] A retry with the same key answers the first result, 201; two owners at once make one extension.
- [ ] An extended closure is not deleted, retyped, restarted or given a later end (409 `CLOSURE_EXTENDED`, by the
      database); its text and an earlier end (end now included) change.

### Out of scope
- The screens 10, 11, 18, 23, 28 and the space page's announcements, report button and heart: worker A's later
  items, planned once this API has merged. Every web change but the catalogue lines and the broken fixtures.
- The owner's overview («يحتاج انتباهك», step 12): it will read the summary's service function (D4).
- Notifications of any kind, email included (decision 2): the owner learns of a closure in the app only.
- An undo of an extension (decision 5): a wrong one is corrected per subscription (SUBSCRIPTIONS' correction).
- Editing the space from a report («تعديل الحقل» is navigation, conventions §9).
- A title or an author on an announcement (O9); the audit records who.
- Reviews, booking, QR, claiming, online payment (overview *Not in v1*).

---

## 3. The reading done, and what it changed

From `origin/main` at `befd96f9`: `CLAUDE.md`; `docs/development/workflow.md` (whole) and `testing.md` (whole);
`docs/backend/conventions.md` (whole); `security.md` (whole); ADR 0007, 0009 (with its *Revised* lines), 0015;
`docs/architecture/data-model.md` (whole); `docs/api/api-contract.md` (§1–§4, *Occupancy (managed)*, *Front desk
(managed)*, *Directory (public)*, §6); `docs/features/occupancy.md` and `directory.md` (their headings and
boundaries); `docs/plans/v1-mvp.md` (steps 8–10, the ordering notes, the route tables); `docs/project/overview.md`
(scope lines); `docs/README.md` (the features map, the deferred documents); the findings index;
`C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_OWNER.md` (whole), `DECISIONS_ACCOUNT.md` (whole),
`DECISIONS_ADMIN.md` (A7, A8, AD-012), `DECISIONS_PUBLIC.md` (U8, U10), `_DONE\FIX_ACCOUNT\FIX_ACCOUNT_PLAN.md`
(AC-009's `repliedBy`); `_SHARED\OPEN_DECISIONS.md`; `WORKER_B\SUBSCRIPTIONS\2_PLAN.md` (whole) and
`0_CARRIED_FROM_102.md`; `WORKER_B\DESK\3_EXEC_PROMPT_PR3.md` (§2–§4); `WORKER_B\DEMO_SEED\3_EXEC_PROMPT.md`;
`WORKER_A\PUBLIC\2_PLAN.md` (its shared paths); `schema.prisma` (the five tables, `Subscription`, `CheckIn`,
`RateLimit`, `AuditLog`, the enums); the migrations `init` (the five tables, `announcements_dates_check`) and
`space_settings` (`closure_extensions`, `subscription_extensions`, `closure_extensions_days_check`); the code of
`announcements` (whole), `occupancy` (service, index), `directory` (service, routes, index), `spaces` (index,
`spaces.service`'s lock and `findShown`, `spaces.repository`, `publicListing.service`), `users` (service's
`namesFor`, `lockAccount`, routes), `space-links` (service's functions, the staff router's limiter, the me
router), `lookups` (service), `shared/auth/can.ts`, `shared/rate-limit` (limiter, policy), `shared/http/
idempotencyKey.ts`, `app.ts` (whole); #102's `subscriptions.service.ts`, `calendar.ts` and `core/gazaTime.ts`;
`packages/shared` (`core/{fields,errors}.ts`, `desk/responses.ts`'s `DESK_WARNINGS`, `directory/responses.ts`);
`eslint.config.js` (the level map); `apps/web/scripts/dashboardOnly.ts`; `apps/api/test/{factories,locks}.ts`
(exports); the tests that insert announcements and closure extensions (`git grep`); the prototype's
`Announcements.html` (states, actions, the extension dialog); `.claude/skills/add-error-code`.

**What the reading changed:**
- **`announcements` (L2) cannot read `closure_extensions`,** which `subscriptions` (L3) owns (conventions §7). So
  the managed list that shows each closure's extension state is **composed by `subscriptions`**, the module above
  both (D4), and decision 6's refusals are **the database's**, a trigger on `announcements` (S2), the way the
  ledger's rules are.
- **`announcements_dates_check` refuses an end at or before the start.** "End now" on an upcoming announcement
  would break it: the API refuses it with `ANNOUNCEMENT_NOT_STARTED` (the prototype offers delete there).
- **Decision 6 as written would trap a running closure:** extended while it runs (decision 3 allows it) and with
  no end, it could never be ended, and the space would show «مغلق الآن» for ever. S3 lets its end come earlier
  (end now included) and refuses only a later one (§13 Q3).
- **The prototype pages the announcements by tab, with a count on each**, and the overview counts started
  closures without an extension: one summary read answers both (D4).
- **Six tests insert announcements and closure extensions directly**; a required key breaks them, so they gain
  one (§7).
- **`PublicSpace` gains a required field:** any web fixture typed by it fails the typecheck; PR 1 fixes those
  lines under worker B's licence (§12.2 PR 1 check 5).
- **Every `can()` action this item needs already exists:** `announcements.manage` (staff),
  `subscriptions.extendAfterClosure` (owner), `dataReports.resolve` (`adminWhileUnverifiedElseOwner`),
  `space.dataReports.read` (`adminOrOwner`), `platform.dataReports.read` (admin), `dataReports.readOwn` (self),
  `dataReports.create` (signedIn), `favorites.manage` (self). No change to `can.ts`.
- **AC-009's `repliedBy`** is the reply's author "from the resolver", not today's verification (the prototype's
  note): it is stored with the decision (S7).
- **The "publicly listed" rule already lives in `publicListing`'s filter and in `findShown`:** reports and
  favourites reuse them (S12), so no third copy is written.

### Assumptions from SUBSCRIPTIONS PRs 1–3 and DEMO_SEED (each re-read by §12.1)
- **A1** — `subscriptions.starts_on` / `ends_on` are Gaza calendar dates (`@db.Date`), read with
  `toISOString().slice(0, 10)` and written as `new Date(date + 'T00:00:00Z')` (SUBSCRIPTIONS D13).
- **A2** — ending early sets `ended_at` and `ended_by_id` and moves `ends_on` to today (SUBSCRIPTIONS D10): such a
  subscription is excluded by `ended_at IS NOT NULL` (decision 4).
- **A3** — every subscription write (subscribe, renew, correct, correct the price, end) and the subscription
  check-in take the space's lock first (SUBSCRIPTIONS D7, D8, D10, D11, D14): they serialise with the extension.
- **A4** — a subscription's status and progress are computed only by `subscriptions` (`statesOf`, SUBSCRIPTIONS
  PR 1); the extension computes none.
- **A5** — the subscription check-in reads the space's warnings from `occupancy.checkInWarnings(spaceId, now, tx)`
  (SUBSCRIPTIONS D11 step 6, kept by D12's `present.ts`), so one added warning reaches both check-ins.
- **A6** — `core/gazaTime.ts` holds `gazaClockOf`, `addDays` and `weekStartOf` (#102, built).
- **A7** — `subscriptions_dates_check` (`ends_on >= starts_on`) holds; moving an end later never breaks it.
- **A8** — `subscriptions_space_id_ends_on_idx` exists (`@@index([spaceId, endsOn])`).
- **A9** — `subscriptions/` grows into use-case folders as SUBSCRIPTIONS builds it; this plan adds
  `subscriptions/closures/` beside them (conventions §8, *Growth*).
- **A10** — DEMO_SEED adds ≈ 24 listed spaces, verified ones owned by `demo-directory-owner@example.com`, at least
  one unverified; no announcement, report or favourite; the admin is the seed's `SEED_ADMIN_*` account.
- **A11** — the demo space keeps the four scenario subscriptions (data model › *Subscription scenarios*), at
  least one running today.

---

## 4. The decisions as built

### The owner's decisions (2026-10-21), as built
1. **Four PRs** (§1). The reading shows no better cut that would serve the screens sooner; *Proposed
   alternatives* A8 offers PR 4 second.
2. **The closure's notice, in the app only:** the managed list's `extension` per closure (none yet: `null`;
   applied: days, how many moved, who, when), and `GET …/announcements/summary`'s `closuresAwaitingExtension`.
   **The overview (step 12) will call `subscriptions`' `closures.summary(spaceId, now)`**, the same service
   function the summary route answers: no route of its own. PR 1's report updates `OPEN_DECISIONS.md` point 2.
3. **The days:** D11 — proposed from the closure's first to its last covered Gaza day (to today while it runs);
   the owner types 1–365 (`EXTENSION_MAX_DAYS`).
4. **Which subscriptions move:** D11's covered rule, one SQL fragment for the preview and the move; data model
   and overview rewritten (approved).
5. **No undo:** no route; the contract says so.
6. **An extended closure:** the trigger of S2 (`CLOSURE_EXTENDED`), with S3's earlier end.
7. **The public page:** D5.
8. **The check-in warning:** a new code `CLOSURE_IN_FORCE` (D6). *Why not `OUTSIDE_OPENING_HOURS`:* the desk
   says something different (the space announced itself closed, not its hours), and a closure inside the hours
   would otherwise read as a mistake in the hours.
9. **A repeated report:** 200 with the open report, no new row; **it counts toward the hourly limit** (counted at
   the route, before the body is read, as every limit of its kind — conventions §2). Alternative A4.
10. **Dismissing needs its reply** (both deciders): the schema's refinement and a `CHECK`. The build map's two
    rows say so.
11. **A decided report is final:** `REPORT_ALREADY_DECIDED`; S8 lets an identical retry answer as it is.
12. **Favourites' ceiling 200** (`FAVORITES_MAX`), `FAVORITES_LIMIT_REACHED`.
- **Unchanged (settled):** the writers (ADR 0009); no title, no author, no schema change for them (O9); end now,
  start now, delete, no end (O10); the reporter anonymous to the owner, named to the admin (O12); who decides
  (`can()` with "verified"); resolving never edits the space; `listed: false` (C7); the field groups and «أخرى»'s
  message; the 10-per-hour limit.

### D1 — routes and answers

| PR | Route | Access | Key | Body / query | 2xx | Module |
|---|---|---|---|---|---|---|
| 1 | `POST /manage/spaces/:spaceId/announcements` | 🧾 `requireCan('announcements.manage')` | ✓ | `createAnnouncementSchema` | **201** `Announcement` | `announcements` |
| 1 | `PATCH …/announcements/:announcementId` | 🧾 `requireCan('announcements.manage')` | — | `editAnnouncementSchema` | **200** `Announcement` | `announcements` |
| 1 | `POST …/announcements/:announcementId/end` | 🧾 `requireCan('announcements.manage')` | — | — | **200** `Announcement` | `announcements` |
| 1 | `POST …/announcements/:announcementId/start` | 🧾 `requireCan('announcements.manage')` | — | — | **200** `Announcement` | `announcements` |
| 1 | `DELETE …/announcements/:announcementId` | 🧾 `requireCan('announcements.manage')` | — | — | **204** | `announcements` |
| 1 | `GET …/announcements` | 🧾 | — | `?state=&page=&limit=` | **200** `ManagedAnnouncement[]`, `meta` | `subscriptions` (composed) |
| 1 | `GET …/announcements/summary` | 🧾 | — | — | **200** `AnnouncementsSummary` | `subscriptions` (composed) |
| 1 | `GET /spaces/:slug` (gains) | 🌐 | — | — | **200** `PublicSpace` + `announcements` | `directory` |
| 2 | `POST /spaces/:slug/reports` | 👤 + `DATA_REPORT` limit | — | `createReportSchema` | **201** `MyReport`, or **200** the open one | `data-reports` |
| 2 | `GET /me/reports` | 👤 | — | `?status=&page=&limit=` | **200** `MyReport[]`, `meta` | `data-reports` |
| 2 | `GET /manage/spaces/:spaceId/data-reports` | 🏢 `requireCan('space.dataReports.read')` | — | `?status=&field=&page=&limit=` | **200** `SpaceReport[]`, `meta` | `data-reports` |
| 2 | `PATCH …/data-reports/:reportId` | 🏢 `requireCan('dataReports.resolve')` | — | `decideReportSchema` | **200** `SpaceReport` | `data-reports` |
| 2 | `GET /admin/data-reports` | 🛡 | — | `?status=&field=&spaceId=&page=&limit=` | **200** `AdminReport[]`, `meta` | `data-reports` |
| 2 | `PATCH /admin/data-reports/:reportId` | 🛡 (+ `can()` under the lock) | — | `decideReportSchema` | **200** `AdminReport` | `data-reports` |
| 3 | `POST /me/favorites/:spaceId` | 👤 | — | — | **204** | `favorites` |
| 3 | `DELETE /me/favorites/:spaceId` | 👤 | — | — | **204** | `favorites` |
| 3 | `GET /me/favorites` | 👤 | — | `?sort=distance` + `Masaha-Near` | **200** `FavoriteSpace[]`, whole | `directory` |
| 4 | `GET …/announcements/:announcementId/extend-subscriptions` | 🧾 | — | — | **200** `ExtensionPreview` | `subscriptions` |
| 4 | `POST …/announcements/:announcementId/extend-subscriptions` | 🏢 `requireCan('subscriptions.extendAfterClosure')` | ✓ | `{ days }` | **201** `ClosureExtension` | `subscriptions` |

- **Placement and levels** (conventions §7–§9, R3, R4): every write of one module is its own router
  (`announcements`, `favorites`, `data-reports`); the extension spans `announcements` (the closure's row) and
  `subscriptions` (the ends, the extension rows), so it belongs to `subscriptions`, the module above
  (`subscriptions` L3 → `announcements` L2, `spaces` L1, `users` L1). The managed list and the summary show an
  `announcements` value and a `subscriptions` value: composed by `subscriptions` (above `announcements`).
  `data-reports` (L3) imports `spaces`, `users` (L1), `lookups` (L0) and `space-links` (L2), as conventions §9
  allows for "verified". `favorites` (L2) imports `users`, `spaces` (L1) and `lookups` (L0). `directory` (L5)
  imports `announcements`, `favorites` (L2). No level rule breaks; §12.2 check 2 runs `lint` on them.
- **Path ids** answer `not_found` (404) when not the space's (or the user's, or gone); body fields `validation`.
- **Reads ask no `requireCan`** (#86) except the owner-only reports (🏢), refused before the query is read.
- **The routers' mounting** (`app.ts`): `announcements`' manage router and `subscriptions`' closures manage
  router both at `manage.use('/announcements', …)` (their paths do not overlap); `data-reports`' site router at the
  API's root (`/spaces/:slug/reports`, `/me/reports`), its manage router at `manage.use('/data-reports', …)`, its
  admin router inside `admin`; `favorites`' me router at `api.use('/me', …)`; `directory`'s new me router at the
  root (`/me/favorites`). The users' `/me` router has only `POST /password`, so the others are reached after it.

### D2 — the shapes (`@masaha/shared`)

```ts
// announcements (L2)
ANNOUNCEMENT_TYPES = ['GENERAL', 'OUTAGE', 'CLOSURE', 'OFFER', 'EVENT'] as const
ANNOUNCEMENT_STATES = ['RUNNING', 'UPCOMING', 'ENDED'] as const
ANNOUNCEMENT_TEXT_MAX_LENGTH = 500
instant = z.iso.datetime({ offset: true })
createAnnouncementSchema = z.object({
  type: z.enum(ANNOUNCEMENT_TYPES), textAr: paragraphSchema(1, 500),
  textEn: paragraphSchema(1, 500).nullable().optional(),
  startsAt: instant.optional(),                    // absent: now («يبدأ الآن»)
  endsAt: instant.nullable().optional(),           // absent or null: no end
}).refine(both given → endsAt > startsAt, { path: ['endsAt'], code: 'out_of_range' })
editAnnouncementSchema = createAnnouncementSchema's fields, .partial(), the same refinement   // textEn null clears; endsAt null removes the end
announcementsQuerySchema = paginationQuerySchema.extend({ state: z.enum(ANNOUNCEMENT_STATES).default('RUNNING') })
Announcement = { id, type, textAr, textEn: string | null, startsAt, endsAt: string | null, state }
ExtensionApplied = { days, subscriptions: number, appliedAt, appliedBy: { id, name } }
ManagedAnnouncement = Announcement & { extension?: ExtensionApplied | null }   // present on closures only; null: none yet
AnnouncementsSummary = { running, upcoming, ended, closuresAwaitingExtension }  // counts
EXTENSION_MAX_DAYS = 365
extendSubscriptionsSchema = z.object({ days: z.number().int().min(1).max(365) })    // PR 4
ExtensionPreview = { firstDay, lastDay, proposedDays, subscriptions: number, applied: ExtensionApplied | null }   // Gaza dates
ClosureExtension = ExtensionApplied & { announcementId }

// directory (L5)
PublicAnnouncement = { id, type, textAr, textEn: string | null, startsAt, endsAt: string | null }
PublicSpace += { announcements: PublicAnnouncement[] }       // running then upcoming, by start then id, ≤ 20
PUBLIC_ANNOUNCEMENTS_MAX = 20
FavoriteSpace =                                                // PR 3
  | { listed: true, savedAt, space: DirectorySpace }
  | { listed: false, savedAt, space: { id, nameEn, nameAr: string | null } }
favoritesQuerySchema = z.object({ sort: z.literal('distance').optional() })   // the point travels in Masaha-Near

// desk (L5)
DESK_WARNINGS = ['SPACE_FULL', 'OUTSIDE_OPENING_HOURS', 'CLOSURE_IN_FORCE', …]   // appended after OUTSIDE_OPENING_HOURS

// data-reports (L3)
DATA_REPORT_FIELDS = ['PRICES', 'HOURS', 'CONTACT', 'LOCATION', 'AMENITIES', 'OTHER'] as const
DATA_REPORT_DECISIONS = ['RESOLVED', 'DISMISSED'] as const
REPORT_TEXT_MAX_LENGTH = 500
createReportSchema = z.object({ field: z.enum(DATA_REPORT_FIELDS), message: paragraphSchema(1, 500).optional() })
  .refine(field !== 'OTHER' || message, { path: ['message'], code: 'required' })
decideReportSchema = z.object({ status: z.enum(DATA_REPORT_DECISIONS), note: paragraphSchema(1, 500).optional() })
  .refine(status !== 'DISMISSED' || note, { path: ['note'], code: 'required' })
REPORT_STATUS_FILTERS = ['OPEN', 'DECIDED'] as const
myReportsQuerySchema = paginationQuerySchema.extend({ status: z.enum(REPORT_STATUS_FILTERS).optional() })
spaceReportsQuerySchema = myReportsQuerySchema.extend({ field: z.enum(DATA_REPORT_FIELDS).optional() })
adminReportsQuerySchema = spaceReportsQuerySchema.extend({ spaceId: id.optional() })
ReportDecision = { status: 'RESOLVED' | 'DISMISSED', at, note: string | null, repliedBy: 'SPACE' | 'MASAHA' }
SpaceReport = { id, field, message: string | null, createdAt, status, decision: ReportDecision | null }  // never the reporter
MyReport = SpaceReport & { space: { id, slug, nameEn, nameAr: string | null, listed: boolean } }
AdminReport = SpaceReport & { space: { id, slug, nameEn, nameAr, verified: boolean }, reporter: { id, name },
                              decidedBy: { id, name } | null }

// favorites (L2)
FAVORITES_MAX = 200
```
- `paragraphSchema` keeps line breaks (an announcement, a report and a reply are short paragraphs);
  `textSchema` would refuse them. The bounds: §5 S5.
- **`MyReport` keeps `slug`** even when `listed: false`: a slug is never reused (data model › IDs), and the web
  shows the name as text then (C7).

### D3 — an announcement's state, and Gaza time
- **The state** (`announcements/announcementState.ts`, pure), from instants, no zone: `UPCOMING` while `startsAt >
  now`; `ENDED` once `endsAt ≤ now`; else `RUNNING` (no end: running until ended). The same comparisons as
  `closedAt` (`startsAt ≤ now`, `endsAt > now` or none), so a running closure is exactly what makes the live
  status `CLOSED`. A deleted one has no state: every read leaves it out (ADR 0007).
- **The list's orders:** `RUNNING` and `UPCOMING` by `startsAt`, then `id`; `ENDED` by `endsAt` descending, then
  `id` descending (the tab that grows).
- **Gaza dates** only where a calendar day is meant: the closure's covered days and "today" (D11), by
  `gazaClockOf(instant).date` (conventions §11); a subscription's `ends_on` is a Gaza date (A1) moved with
  `ends_on + days` in SQL (date arithmetic, no zone).

### D4 — the managed list and the summary (`subscriptions/closures/`, composed)
1. `announcements.page(spaceId, { state, page, limit }, now)` → `{ rows: AnnouncementRow[]; total }` — one
   `findMany` + `count` in parallel (conventions §5), `deletedAt: null`, the state as a `where` on the instants.
2. `closures.extensionsOf(closureIds)` (its repository, one query): `closure_extensions` joined to the count of
   their `subscription_extensions` and the applier's id; names by `users.namesFor(ids)` (one query).
3. Each row mapped to `ManagedAnnouncement`; `extension` set only on `CLOSURE` rows.
- **The summary:** `announcements.counts(spaceId, now)` (one grouped query: running, upcoming, ended) and
  `announcements.startedClosureIds(spaceId, now)` (not deleted, `CLOSURE`, `startsAt ≤ now`); then
  `closures.extendedAmong(ids)` → `closuresAwaitingExtension = ids.length − extended.size`. *Bound:* a space's
  closures, tens at most.
- **The overview (step 12)** calls `closures.summary(spaceId, now)`; it computes nothing (conventions §9).

### D5 — the public page (`directory.page`)
After the space's whole read, `announcements.publicOf(spaceId, now)`: not deleted, `endsAt` null or after now,
ordered by `startsAt`, then `id`, `take: PUBLIC_ANNOUNCEMENTS_MAX` (20). Read outside the space's share lock: an
announcement is no fact group, and a write landing between the two reads shows on the next (30 s cache).
- **The cache** (`directory/cache.ts`, 30 s and the `ETag`) is unchanged: an announcement that starts or ends shows
  within 30 s. Stated in the contract.

### D6 — the closure warning at check-in (`occupancy.checkInWarnings`)
After `OUTSIDE_OPENING_HOURS`: `if ((await announcements.closedAt([spaceId], now, tx)).has(spaceId))
warnings.push('CLOSURE_IN_FORCE')`. Never a refusal. Both check-ins read it (A5). *Order:* appended, so the
existing orders and their tests stay; the subscription's own warnings follow (SUBSCRIPTIONS D11).

### D7 — announcements' writes (`announcements`, PR 1)
Each in one transaction, in this order: `spaces.lock(space.id, tx)` (404 when gone); `can(actor,
'announcements.manage', { links: await space.linksUnder(tx) })` else 403; then:
- **Create:** `findByKey(space.id, key, tx)` → a retry answers it, 201; `now`; `periodErrors({ startsAt: startsAt ??
  now, endsAt }, now, 'create')` (pure, `announcements/period.ts`: start within [now − 30 d, now + 365 d]; an end
  after now and at most 365 d after the start) → 422 with its field codes; `create(…, key)`; audit
  `announcement.created` (`after`: `{ type, startsAt, endsAt }`).
- **Edit:** `lockIn(space.id, id, tx)` (`FOR UPDATE`, not deleted; else 404); `announcementChange(current, edit)`
  (pure: only fields set to a new value); nothing → answered as it is; the merged period checked
  (`periodErrors(…, 'edit')`: a changed `endsAt` after now; a changed `startsAt` in the create's window; the end
  after the start) → 422; update; audit `announcement.edited` (`before`/`after`: the changed fields).
- **End now:** `lockIn`; upcoming → 409 `ANNOUNCEMENT_NOT_STARTED`; ended → as it is; else `endsAt = now`, audit
  `announcement.ended` (`before: { endsAt }`, `after: { endsAt }`).
- **Start now:** `lockIn`; started → as it is; else `startsAt = now`, audit `announcement.started`.
- **Delete:** `lockIn` **including deleted ones** — deleted → 204, nothing written; none → 404; else `deletedAt =
  now`, audit `announcement.deleted` (`before: { type, startsAt, endsAt }`).
- PR 4's trigger may refuse the edit, the end's move later, the start and the delete of an extended closure: the
  error handler translates it (`CLOSURE_EXTENDED`); the service repeats nothing (conventions §13).

### D8 — a data report (`data-reports`, PR 2)
**Create** (`POST /spaces/:slug/reports`): `requireAuth()` → `limitRequests(DATA_REPORT by the user)` →
`validate(createReportSchema)` → service, in one transaction:
1. `publicSpace.findShown(slug)` and `lookups.isActiveArea(areaId)` (the page's own test) → else 404.
2. `users.lockAccount(actor.id, tx)` (the user's row, `FOR NO KEY UPDATE`): one user's reports serialise.
3. `repository.findOpen(userId, spaceId, field, tx)` → found: answered, **200**, nothing written.
4. `repository.create({ userId, spaceId, field, message }, tx)` → **201**. Not audited (conventions §6 lists the
   decisions only).
- `DATA_REPORT = { name: 'data-report', limit: 10, windowMs: 60 * 60_000 }` (`data-reports.limits.ts`).

**Reads:**
- `GET /me/reports`: `repository.pageOfUser(userId, { status }, page)` (newest first, then id desc); the spaces'
  names (`spaces.namesWithDeleted(ids)`, new, soft-deleted included); `listed` from
  `publicListing.upTo({ areaIds: await lookups.listedAreaIds(), verifiedIds: [], onlyIds: ids }, ids.length)`
  (S12); `repliedBy` from `resolved_as` (`OWNER` → `SPACE`, `ADMIN` → `MASAHA`).
- The owner's: `repository.pageOfSpace(spaceId, { status, field }, page)`, mapped by `toSpaceReport` (no `userId`
  selected at all: the repository's `select` leaves it out, so no mapper can leak it — B-privacy).
- The admin's: `repository.pageAll({ status, field, spaceId }, page)` — reports of soft-deleted spaces left out
  (ADR 0007) — with the reporters' and deciders' names (`users.namesFor`), each space's names and `verified`
  (`spaceLinks.verifiedSpaceIds()` intersected, one query).

**Decide** (`decide(actor, reportId, request, scope)`, `scope` = the path's space or the admin): in one transaction:
1. `repository.findSpaceOf(reportId)` (no lock) → none, or not the path's space → 404.
2. `spaces.lock(spaceId, tx)` → gone → 404.
3. Links under the lock: the manage route's `space.linksUnder(tx)`; the admin's `spaceLinks.linksAt(spaceId, tx)`.
4. `can(actor, 'dataReports.resolve', { links })` → else 403 (the owner of a verified space; the admin of an
   unverified one).
5. `repository.lockIn(reportId, tx)` (`FOR UPDATE`).
6. `decisionOf(report, request, actor.id)` (pure, `data-reports/decision.ts`): open → `decide`; decided with the same
   status, the same note and the same decider → `as-is` (200, nothing written); else → 409
   `REPORT_ALREADY_DECIDED`.
7. Update `status`, `resolvedById`, `resolvedAt = now`, `resolutionNote`, `resolvedAs` (`OWNER` on the manage route,
   `ADMIN` on the admin's); audit `dataReport.resolved` / `dataReport.dismissed` (`after: { note }`), the report as
   the entity, the space as the entry's space.
- **Lock order:** the space's row, then the report's; the create takes the user's row only. No two orders cross.

### D9 — favourites (`favorites` and `directory`, PR 3)
- **Save** (`favorites.save(actor, spaceId)`), in one transaction: `users.lockAccount(actor.id, tx)`; already saved
  → 204, nothing written; not listed (`publicListing.upTo({ areaIds: listedAreaIds, verifiedIds: [], onlyIds:
  [spaceId] }, 1)` empty) → 404; `count(userId) ≥ FAVORITES_MAX` → 409 `FAVORITES_LIMIT_REACHED`; insert.
  *Order:* an already-saved one at the ceiling answers 204 (idempotent first).
- **Remove:** `deleteMany({ userId, spaceId })` → 204 whatever it removed (idempotent by design). An unlisted space
  is removable (C7's «إزالة»).
- **Read** (`directory.favorites(userId, near?)`): `favorites.of(userId)` → `{ spaceId, savedAt }[]` newest first
  (≤ 200); `publicListing.page({ areaIds: listed, verifiedIds, onlyIds: ids }, near ? { by: 'distance', from: near }
  : { by: 'updated' }, { page: 1, limit: FAVORITES_MAX })`; the live statuses and area names as `list` does; the
  ids not returned → `spaces.namesWithDeleted(rest)` → `listed: false`. **Order:** without `near`, by `savedAt`
  descending (then space id); with it, the listed ones by distance (the listing's order), then the unlisted by
  `savedAt`. No audit (a person's own choice).
- **`Masaha-Near`** is read by the directory's existing `listQuery.ts` rule (§12.2 PR 3 check 2): only with
  `sort=distance`, rounded to 3 decimals, inside the Strip; every answer to a request carrying it `no-store`.
- **No cache header** on `GET /me/favorites` beyond the API's default (a signed-in answer).

### D10 — the closure's covered days (`announcements/closureSpan.ts`, pure, PR 4)
`closureSpan({ startsAt, endsAt }, now)` for a started closure (`startsAt ≤ now`):
- `firstDay = gazaClockOf(startsAt).date`;
- **its last instant:** `endsAt − 1 ms` when it has ended (`endsAt ≤ now`), else `now` (no end, or still running);
  `lastDay = gazaClockOf(lastInstant).date` (S4: an end at midnight covers the day before, not the next);
- `days = daysFrom(firstDay, lastDay) + 1` (`core/gazaTime.ts` gains `daysFrom(a, b)`: whole calendar days, pure).
- `proposedDays = min(days, EXTENSION_MAX_DAYS)`.

### D11 — the extension (`subscriptions/closures/`, PR 4)
**The covered rule** (`closures.repository.ts`, one `Prisma.sql` fragment both reads use):
```sql
"space_id" = ${spaceId} AND "ended_at" IS NULL AND "ends_on" IS NOT NULL
AND "ends_on" >= ${firstDay}::date AND ("starts_on" IS NULL OR "starts_on" <= ${lastDay}::date)
```
(a subscription with no start date counts as started; `subscriptions_space_id_ends_on_idx` serves it, A8).
- `coveredCount(spaceId, span)` → `count(*)` (the preview); `lockCovered(spaceId, span, tx)` → `SELECT "id" … ORDER BY
  "id" FOR UPDATE` (the move).

**Preview** (`GET`, no lock): `announcements.closureIn(space.id, id)` (a `CLOSURE`, not deleted, the space's; else
404); applied → `{ …span, proposedDays, subscriptions: count, applied }` with the stored extension; upcoming → 409
`ANNOUNCEMENT_NOT_STARTED`; else the span, the proposal and `coveredCount`.

**Apply** (`POST`), in one transaction, in this order:
1. `spaces.lock(space.id, tx)` (404); `can(actor, 'subscriptions.extendAfterClosure', { links: linksUnder(tx) })`
   else 403.
2. `repository.findByKey(key, tx)` → for this announcement: its result, 201; for another: 409 (no code).
3. `announcements.lockClosure(space.id, id, tx)` (`FOR UPDATE`; a `CLOSURE`, not deleted, the space's) → else 404.
4. `repository.findFor(announcementId, tx)` → exists: 409 `CLOSURE_ALREADY_EXTENDED` (the unique key the backstop).
5. `now`; `startsAt > now` → 409 `ANNOUNCEMENT_NOT_STARTED`.
6. `span = closureSpan(closure, now)`; `ids = lockCovered(space.id, span, tx)`.
7. `moveEnds(ids, days, now, tx)`: `UPDATE "subscriptions" SET "ends_on" = "ends_on" + ${days}, "updated_at" =
   ${now} WHERE "id" = ANY(${ids}::integer[])` — one statement, one array parameter.
8. `createExtension({ announcementId, days, appliedById: actor.id, key }, tx)`, then `linkSubscriptions(extensionId,
   ids, tx)` (`createMany`, one statement).
9. Audit `closure.subscriptionsExtended` (entity the announcement, the space's entry; `after: { days,
   subscriptionIds: ids }`). 201 `ClosureExtension`.
- **Its status and progress** come only from `subscriptions` (A4): the extension changes `ends_on`; the next read
  derives the rest.
- **A retry** answers the stored extension (its count from its links): the first result, not recomputed.

### D12 — the migrations

**PR 1 `announcement_key`** — Prisma's part (`idempotencyKey String @map("request_id") @db.Uuid` +
`@@unique([spaceId, idempotencyKey])`), edited so existing rows get a key first:
```sql
ALTER TABLE "announcements" ADD COLUMN "request_id" UUID;
-- Rows made before the key (tests, the dev data) get one of their own.
UPDATE "announcements" SET "request_id" = gen_random_uuid() WHERE "request_id" IS NULL;
ALTER TABLE "announcements" ALTER COLUMN "request_id" SET NOT NULL;
CREATE UNIQUE INDEX "announcements_space_id_request_id_key" ON "announcements"("space_id", "request_id");
```
No other index: a space's announcements are tens to hundreds, and `announcements_space_id_idx` serves every
read (data model › *Indexes only for queries that run*).

**PR 2 `data_report_rules`** — Prisma's part: `enum DataReportResolver { OWNER ADMIN }`, `resolvedAs
DataReportResolver? @map("resolved_as")`, `@@unique([userId, spaceId, field], map: "data_reports_open_key", where:
{ status: 'OPEN' })` (§12.2 PR 2 check 1). Appended:
```sql
-- A decision's fields come together, and only with a decision (docs/architecture/data-model.md › Constraints).
ALTER TABLE "data_reports" ADD CONSTRAINT "data_reports_decision_check" CHECK (
  ("status" = 'OPEN') = ("resolved_at" IS NULL)
  AND ("resolved_at" IS NULL) = ("resolved_by_id" IS NULL)
  AND ("resolved_at" IS NULL) = ("resolved_as" IS NULL)
  AND ("status" <> 'OPEN' OR "resolution_note" IS NULL)
  AND ("resolution_note" IS NULL OR btrim("resolution_note") <> ''));
-- A dismissal carries its reply (decision 10); «أخرى» its message.
ALTER TABLE "data_reports" ADD CONSTRAINT "data_reports_dismissal_note_check"
  CHECK ("status" <> 'DISMISSED' OR "resolution_note" IS NOT NULL);
ALTER TABLE "data_reports" ADD CONSTRAINT "data_reports_other_message_check"
  CHECK ("field" <> 'OTHER' OR ("message" IS NOT NULL AND btrim("message") <> ''));
```
No backfill: no route wrote a report (the dev data holds none, A10).

**PR 4 `closure_extension_key`** — Prisma's part (`idempotencyKey String @unique @map("request_id") @db.Uuid`),
edited as PR 1's (`ADD COLUMN` nullable, `UPDATE … gen_random_uuid()`, `SET NOT NULL`, then the unique index).
Appended:
```sql
-- Decision 6 (2026-10-21): once a closure's subscriptions were extended, it keeps its type and its start, is
-- never deleted, and its end only comes earlier (S3: a running closure must still be able to end). Its text
-- may change. The database owns the rule: `announcements` cannot read this table (conventions §7).
CREATE FUNCTION "announcements_guard_extended"() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF EXISTS (SELECT 1 FROM "closure_extensions" WHERE "announcement_id" = OLD."id") AND (
       NEW."type" <> OLD."type" OR NEW."starts_at" <> OLD."starts_at"
       OR NEW."deleted_at" IS DISTINCT FROM OLD."deleted_at"
       OR (NEW."ends_at" IS DISTINCT FROM OLD."ends_at"
           AND NOT (NEW."ends_at" IS NOT NULL AND (OLD."ends_at" IS NULL OR NEW."ends_at" < OLD."ends_at")))) THEN
    RAISE EXCEPTION 'announcements_closure_extended: closure % had its subscriptions extended', OLD."id"
      USING ERRCODE = 'check_violation', TABLE = 'announcements', CONSTRAINT = 'announcements_closure_extended';
  END IF;
  RETURN NEW;
END;
$$;
CREATE TRIGGER "announcements_guard_extended"
  BEFORE UPDATE OF "type", "starts_at", "ends_at", "deleted_at" ON "announcements"
  FOR EACH ROW WHEN (OLD."type" = 'CLOSURE') EXECUTE FUNCTION "announcements_guard_extended"();
```
- `constraintCodes.ts` gains `announcements_closure_extended → { type: 'conflict', code: 'CLOSURE_EXTENDED' }`.
- A hard delete is already refused by `closure_extensions_announcement_id_fkey` (`ON DELETE RESTRICT`).

### D13 — idempotency, locks, order and races

**Keys** (ADR 0015): announcements (new, S1), the extension (new, S11) — each read first under the space's lock,
the unique key the backstop. **Idempotent by design:** a report (decision 9: the open one answers), a favourite
(204 either way), end now, start now, delete, a decision retried identically (S8).

**Lock orders:** an announcement write: the space's row, then the announcement's. The extension: the space's
row, the announcement's, then the covered subscriptions' by id (conventions §13: one fixed order). A report's
decision: the space's row, then the report's. A report's create and a favourite: the user's row only (the session
lock's row, held briefly; no token is touched). SUBSCRIPTIONS' writes take the space's row first (A3), the auto
check-out a check-in's row only: no two orders cross.

| Race | What decides | Test |
|---|---|---|
| One key sent twice at once (an announcement) | The space's lock; the second reads the first by its key | PR1 T2 |
| A link ended while a write waits | `can()` on `linksUnder(tx)` | PR1 T5; PR2 T15; PR4 T11 |
| Two identical reports at once | The user's row lock; the second reads the open one (the partial index the backstop) | PR2 T4 |
| The owner and the admin decide one report while the owner is linked or unlinked | The space's lock; links read under it; the second sees a decided report | PR2 T15, T18, T19 |
| A favourite saved twice at once; two saves at the ceiling | The user's row lock; the second sees the first | PR3 T2, T5 |
| Two owners (two tabs) apply one extension with two keys | The space's lock; the second sees the extension → `CLOSURE_ALREADY_EXTENDED` | PR4 T6 |
| An extension while its closure is edited, ended or deleted | The space's lock; the extension reads the closure under it; after it, the trigger | PR4 T10, T12 |
| An extension while a subscription is ended, corrected or renewed | The space's lock (A3): the covered set is read as committed | PR4 T9 |

### D14 — the audit lines (conventions §6, a new list line for announcements and the extension)
`announcement.created` · `announcement.edited` · `announcement.ended` · `announcement.started` ·
`announcement.deleted` (PR 1) · `dataReport.resolved` · `dataReport.dismissed` (PR 2) ·
`closure.subscriptionsExtended` (PR 4). Each in the change's own transaction, with the space as the entry's
space. None is on the admin's platform list (default deny, conventions §6); the reports' are platform events the
audit reader's item decides on (not built).

### D15 — the code, PR by PR (interfaces; the commit in brackets)

**PR 1**
| Where | What |
|---|---|
| `announcements/announcements.repository.ts` | + `findByKey(spaceId, key, tx)`, `lockIn(spaceId, id, tx, { withDeleted? })` (`FOR UPDATE`), `create(data, tx)`, `update(id, data, tx)`, `page(spaceId, { state, now }, { skip, take })`, `counts(spaceId, now)`, `startedClosureIds(spaceId, now)`, `publicOf(spaceId, now, take)` [C1–C4] |
| `announcements/announcements.service.ts` | deps `{ runInTransaction, audit, spaces, now }`; + `create(actor, space, key, request)`, `edit(actor, space, id, request)`, `end(actor, space, id)`, `start(actor, space, id)`, `remove(actor, space, id)`, `page(spaceId, query)`, `counts(spaceId)`, `startedClosureIds(spaceId)`, `publicOf(spaceId)` [C1–C4] |
| `announcements/{announcementState,period,announcementChange}.ts` | `announcementState(a, now): AnnouncementState`; `periodErrors(period, now, mode: 'create' \| 'edit', changed?): FieldErrors \| null`; `announcementChange(current, edit): { data, before, after }` [C1] |
| `announcements/announcements.{controller,manage.routes,mapper}.ts` | the five writes (D1; `requireCan` → `requireIdempotencyKey` (create) → `validate`); `toAnnouncement(row, now)` [C1, C2] |
| `subscriptions/closures/{closures.service,closures.repository,closures.controller,closures.manage.routes,closures.mapper}.ts` | `createClosuresService({ announcements, users, now })`: `page(space, query)`, `summary(spaceId, now)`; repository `extensionsOf(ids)`, `extendedAmong(ids)`; `GET /` (`validate(announcementsQuerySchema, 'query')`), `GET /summary` [C3] |
| `directory/directory.service.ts` | `page` adds `announcements: await announcements.publicOf(view.id)`; deps + `announcements` [C4] |
| `occupancy/occupancy.service.ts` | `checkInWarnings` + `CLOSURE_IN_FORCE` (D6) [C5] |
| `app.ts` | one `announcements` service (`runInTransaction`, `audit`, `spaces`, `now`) given to `occupancy`, `directory` and `closures`; the two `/announcements` routers mounted [C1–C4] |

**PR 2**
| Where | What |
|---|---|
| `data-reports/data-reports.repository.ts` | `findOpen(userId, spaceId, field, tx)`, `create(data, tx)`, `pageOfUser`, `pageOfSpace`, `pageAll`, `findSpaceOf(id)`, `lockIn(id, tx)`, `decide(id, data, tx)` — every `select` names its columns; `pageOfSpace`'s never `userId` [C1–C4] |
| `data-reports/data-reports.service.ts` | deps `{ runInTransaction, audit, spaces, publicSpace, publicListing, lookups, spaceLinks, users, now }`; `create(actor, slug, request): { report: MyReport; created: boolean }`, `mine(actor, query)`, `ofSpace(space, query)`, `all(query)`, `decide(actor, scope, reportId, request)` [C1–C4] |
| `data-reports/{decision,data-reports.limits}.ts` | `decisionOf(report, request, actorId): 'decide' \| 'as-is' \| 'conflict'`; `DATA_REPORT` [C1, C3] |
| `data-reports/data-reports.{controller,site.routes,manage.routes,admin.routes,mapper}.ts` | D1's six routes; `toMyReport`, `toSpaceReport`, `toAdminReport` [C1–C4] |
| `spaces/spaces.{service,repository}.ts` | + `namesWithDeleted(ids, tx?)` → `{ id, slug, nameEn, nameAr }[]` [C2] |
| `shared/errors/…` | nothing (no constraint translated: the CHECKs guard bugs, a violation is a 500) |
| `app.ts` | `dataReports` built; its three routers mounted (D1) [C1, C3, C4] |

**PR 3**
| Where | What |
|---|---|
| `favorites/favorites.{repository,service,controller,me.routes}.ts`, `index.ts` | deps `{ runInTransaction, users, publicListing, lookups }`; `save(actor, spaceId)`, `remove(actor, spaceId)`, `of(userId): Promise<{ spaceId; savedAt }[]>`; `POST`/`DELETE /favorites/:spaceId` (`parseId`) [C1] |
| `directory/directory.{service,controller,me.routes}.ts` | `favorites(userId, near?)`; `GET /me/favorites` (`requireAuth()` → the near/sort rule → controller; `no-store` with the header) [C2] |
| `app.ts` | `favorites` built; its router at `/me`; `directory` gains `favorites`, `spaces` [C1, C2] |

**PR 4**
| Where | What |
|---|---|
| `packages/shared/src/core/gazaTime.ts` | + `daysFrom(a, b): number` [C2] |
| `announcements/closureSpan.ts`, service | `closureSpan(closure, now): { firstDay, lastDay, days }`; + `closureIn(spaceId, id)`, `lockClosure(spaceId, id, tx)` [C2, C3] |
| `subscriptions/closures/closures.{repository,service,controller,manage.routes}.ts` | + `coveredCount`, `lockCovered`, `moveEnds`, `findByKey`, `findFor`, `createExtension`, `linkSubscriptions`; `preview(space, id)`, `extend(actor, space, id, key, request)`; `GET`/`POST /:announcementId/extend-subscriptions` [C2, C3] |
| `shared/errors/constraintCodes.ts` | + `announcements_closure_extended` [C1] |

---

## 5. Stronger decisions, and Proposed alternatives

### S1 — announcements carry an idempotency key — **recommended, planned (PR 1's migration)**
*What:* `POST …/announcements` sends `Idempotency-Key`, stored unique within the space. *Why:* reception posts a
closure on the spot, on the desk's weak connection (OPEN_DECISIONS point 2); a retried post would make two
closures, and the owner could extend the subscriptions twice — money moved twice. ADR 0015 rule 1 covers every
desk create. *Cost:* one column (backfilled), one index, six tests that insert announcements gain a key.
*Alternative A6:* none.

### S2 — decision 6 held by a trigger — **recommended, planned (PR 4)**
*What:* `announcements_guard_extended` refuses the delete, the type, the start and a later end of an extended
closure, translated to `CLOSURE_EXTENDED`. *Why:* `announcements` (L2) cannot read `closure_extensions`
(`subscriptions`', L3), and a check in the service would race with an extension; the database already owns the
ledger's rules this way (conventions §13). *Cost:* one trigger, one translation line, a database test and an API
test. *Alternative A3.*

### S3 — an extended closure's end may still come earlier — **refines decision 6, needs the owner (Q3)**
*What:* "changing its period is refused" except bringing its end earlier, end now included. *Why:* decision 3
allows extending a closure that has not ended; one with no end, extended while it runs, could otherwise never end,
and the space would stay «مغلق الآن». An earlier end never covers more days than the owner already gave.
*Cost:* none beyond the trigger's one clause. *Otherwise:* refuse every period change, and allow the extension
only once the closure has ended (decision 3 changed).

### S4 — a closure ending at midnight covers the day before — **recommended, planned**
The last covered day is the Gaza date of the closure's last instant (`endsAt − 1 ms`), so «من الخميس 08:00 حتى
السبت 00:00» proposes two days, not three. *Cost:* one line, one unit test.

### S5 — bounds — **recommended, planned**
Texts 1–500 characters (paragraphs); a start at most 30 days back (a closure posted late) and 365 days ahead; a
new or changed end after now (ending is `…/end`); an end at most 365 days after its start; the public page's 20;
the extension's 1–365 days; the report's message and reply 1–500. *Why:* api-contract §4's bounds, and a typo in
a year never makes a closure of a decade. *Cost:* one pure rule (`period.ts`), its unit test.

### S6 — the database holds decision 9 and the decision's fields — **recommended, planned (PR 2)**
A partial unique index (one open report per user, space and field) is the race's backstop; `CHECK`s keep a
decision's time, decider and side together, a dismissal's reply, and «أخرى»'s message (the schema's note says
"checked by the input schema"; the `CHECK` makes it hold for any writer). *Cost:* three `CHECK`s, one index, one
database test file.

### S7 — who replied is stored with the decision — **recommended, planned (PR 2), needs the owner (Q4)**
*What:* `data_reports.resolved_as` (`OWNER` | `ADMIN`), answered as `repliedBy` (`SPACE` | `MASAHA`). *Why:*
AC-009: the label follows who answered, not today's verification; deriving it from the decider's role now would
change it if an admin's role changes later. *Cost:* one enum, one column, one `CHECK` clause. *Alternative A7.*

### S8 — a decision retried identically answers as it is — **refines decision 11, needs the owner (Q5)**
*What:* the same status, the same reply, by the same person → 200, nothing written; any other decision of a
decided report → 409. *Why:* conventions §13: updates are idempotent by design, so a decision retried after a
lost answer must not read as a refusal. *Cost:* one pure rule and its unit test.

### S9 — the favourites' ceiling under the user's lock — **recommended, planned (PR 3)**
Two saves at 199 would otherwise both pass the count. The user's row (`users.lockAccount`) serialises one user's
saves; the primary key is the backstop of the same space twice. *Cost:* one lock, briefly beside sessions.

### S10 — the managed list composed by `subscriptions` — **a placement, stated (§13 Q2)**
The list shows `announcements`' rows and `subscriptions`' extension state; `subscriptions` is the lowest module
above both, and it owns the extension. The writes stay `announcements`'. *Alternatives A1, A2.*

### S11 — the extension's key unique on its own — **recommended, planned (PR 4)**
`closure_extensions` has no `space_id`; a UUID unique on its own is stronger than "within its space". A key that
extended another closure answers 409 (no code), as a desk payment's does. *Cost:* none beyond the column.

### S12 — "publicly listed" read through `publicListing`, never written again — **recommended, planned**
Reports and favourites ask `publicListing.upTo` with `onlyIds` which of their spaces are listed, and the report's
create asks `findShown` and `isActiveArea` as the page does. *Why:* the rule is already in two queries; a third
copy would drift. *Cost:* the listing's weeks and covers are read for those few spaces (≤ 50 a page, ≤ 200
favourites).

### Rules the item touches, stated
- **conventions §6** gains "announcements created, edited, started, ended and deleted; a closure's extension";
  **§7**'s table: `announcements` "Announcements, including closure notices; their key; the public ones" (routers:
  manage), `subscriptions` "+ the managed announcements list with each closure's extension, and the extension"
  (manage), `data-reports` (me → site and me, manage, admin), `favorites` (me), `directory` (public, **me**: the
  favourites); **§9** *Composed reads* gains the managed announcements list (S10) and *The front desk* the closure
  warning; **§13** *Idempotency* gains announcements and the extension.
- **data-model** — *Conventions › Idempotency*: + announcements, closure extensions; *Constraints*: the two keys,
  the report rules (S6), the trigger (S2); *Checked by the service*: "a closure extension belongs to a `CLOSURE`
  announcement, and extends only that space's active subscriptions" → decision 4's covered rule, started and once
  (the trigger and the unique key the database's); *Entities › ClosureExtension*: "extended the subscriptions the
  closure covered"; *Derived values*: the closure's covered days (S4), an announcement's state; *Front desk and
  money › Full warning*: + the closure warning.
- **ADR 0009** — the row "Extend all active subscriptions after a closure" → "Extend the subscriptions a closure
  covered, once it has started" + a *Revised* line (PR 4).
- **api-contract §4's exceptions** gain the favourites (C8, PR 3) and the public page's announcements (≤ 20, PR 1).
- **security.md** — *Built*: the data-report limit; *Authorization*: `requireCan` on the announcements' writes,
  the reports' owner routes, the extension.
- **The level map** is unchanged; `@masaha/shared` gains `announcements` (L2), `data-reports` (L3), `favorites`
  (L2). None is on the web's dashboard-only list (the site reads all three).

### Proposed alternatives (the owner may prefer them)
- **A1 — `closure_extensions` owned by `announcements`**, the list self-contained in L2. *Cost:* a settled owner
  moves (conventions §7), the count of moved subscriptions is still `subscriptions`' (a second read or a stored,
  duplicated count). **Not recommended.**
- **A2 — the list composed by `desk`** (L5). Works; `desk` is the front desk's orchestrator, and announcements are
  not desk work. **Not recommended.**
- **A3 — decision 6 checked by the service** through a port into `subscriptions` (R5's "genuine upward need").
  *Cost:* a port for one rule, and a check before the write that the database would still need to hold under a
  race. **Not recommended.**
- **A4 — a repeated report not counted** (the limit counted in the service after the open check). *Cost:* the limit
  moves out of the route (conventions §2's placement), and a body is read before it counts. **Not recommended:**
  ten repeats an hour is no hardship.
- **A5 — no distance on the favourites:** `GET /me/favorites` takes no header, AC-014's «الأقرب إليّ» deferred.
  Smaller, but the screen's decision would wait. **Not recommended.**
- **A6 — no key on announcements** (S1 not taken). **Not recommended:** a duplicated closure doubles an extension.
- **A7 — `repliedBy` derived from the decider's role** (no column). Correct until an admin's role changes.
- **A8 — PR 4 second** (announcements, the extension, then reports, favourites): the closures' code stays fresh in
  one reviewer's hands; reports and favourites depend on nothing of it. Equal cost; the owner's order is kept
  unless chosen.

---

## 6. Related findings

| Finding | Folded? | Why, and the cost |
|---|---|---|
| **17** Expired rate-limit counters are never swept | No | PR 2 adds one more policy's rows (one per reporting user an hour); the sweep is its own item |
| **23** No per-address ceiling for signed-in requests | No | The report limit counts by the user, as security.md says; unrelated to the address |
| **77** The race helper counts any waiting backend | No | The new races use `whileHeld` / `waitingOnLock` as the existing ones do |
| **79** The users' names reader keeps an optional transaction | No | PR 2 and PR 1's list call `users.namesFor` outside a transaction, as today |
| **111** The check-in's warnings count *present* a second time | No (SUBSCRIPTIONS PR 3 resolves it) | D6 adds one line to the same function; §12.1 reads its merged shape |
| **98** The capability documents outgrow their size guide | No | Three new documents follow the template; none is large |
| **8** The applied-filter tag has no component (step 10 "closes" it) | No | A web item (the build map says "at the start of the step"): worker A's |

No new finding is planned. Numbers 150 and on are this item's (header).

---

## 7. The files it edits

Only `apps/api`, `packages/shared`, `docs`, the two web catalogues' error lines and any web fixture typed
`PublicSpace` (worker B's licence: what a shared type change breaks). No dependency.

| PR | Code (new +) | Documents |
|---|---|---|
| 1 | `schema.prisma`; + migration; `db/schema.api.test.ts`, `directory/liveStatus.api.test.ts`, `occupancy/override.api.test.ts`, `occupancy/present.api.test.ts` (a key on each announcement they insert); shared: `core/errors.ts`, + `announcements/{requests,responses,index}.ts` (+ `requests.unit.test.ts`), `directory/responses.ts`, `desk/responses.ts`; web: 2 catalogues, the `PublicSpace` fixtures (check 5); api: `announcements/` repository, service, index, + `announcementState.ts` (+ test), + `period.ts` (+ test), + `announcementChange.ts` (+ test), + controller, + `announcements.manage.routes.ts`, + mapper, + `announcements.api.test.ts`, + `lifecycle.api.test.ts`; `subscriptions/index.ts`, + `subscriptions/closures/{closures.service,closures.repository,closures.controller,closures.manage.routes,closures.mapper}.ts`, + `subscriptions/closures/list.api.test.ts`; `directory/directory.service.ts`, `directory/page.api.test.ts`; `occupancy/occupancy.service.ts`; `desk/checkIn.api.test.ts`; `app.ts` | `api-contract.md`, `data-model.md`, `conventions.md`, `security.md`, + `features/announcements.md`, `features/{directory,occupancy,desk,subscriptions}.md`, `docs/README.md`, `plans/v1-mvp.md`, `project/overview.md` — ≈ 50 |
| 2 | `schema.prisma`; + migration; + `db/dataReports.api.test.ts`; shared: `core/errors.ts`, + `data-reports/{requests,responses,index}.ts` (+ test); web: 2 catalogues; api: + `data-reports/` (repository, service, index, controller, site/manage/admin routes, mapper, `decision.ts` (+ test), `data-reports.limits.ts`), + `create.api.test.ts`, + `myReports.api.test.ts`, + `spaceReports.api.test.ts`, + `adminReports.api.test.ts`; `spaces/spaces.{service,repository}.ts`; `app.ts` | `api-contract.md`, `data-model.md`, `conventions.md`, `security.md`, + `features/data-reports.md`, `features/spaces.md` (*Who uses it*), `docs/README.md`, `plans/v1-mvp.md`, `project/overview.md` — ≈ 40 |
| 3 | shared: `core/errors.ts`, + `favorites/{responses,index}.ts`, `directory/{requests,responses,index}.ts`; web: 2 catalogues; api: + `favorites/` (repository, service, index, controller, me routes), + `favorites/favorites.api.test.ts`; `directory/directory.{service,controller}.ts`, + `directory/directory.me.routes.ts`, `directory/index.ts`, + `directory/favorites.api.test.ts`; `app.ts` | `api-contract.md`, `conventions.md`, `security.md`, + `features/favorites.md`, `features/directory.md`, `docs/README.md`, `plans/v1-mvp.md`, `project/overview.md` — ≈ 25 |
| 4 | `schema.prisma`; + migration; `db/schema.api.test.ts` (a key on its extensions), + `db/closureExtensions.api.test.ts`; shared: `core/gazaTime.ts` (+ test), `core/errors.ts`, `announcements/{requests,responses}.ts` (+ test); web: 2 catalogues; api: `shared/errors/constraintCodes.ts`; `announcements/` service, repository, + `closureSpan.ts` (+ test); `subscriptions/closures/` service, repository, controller, routes, mapper, + `extension.api.test.ts`, + `extendedClosure.api.test.ts` | `api-contract.md`, `data-model.md`, `conventions.md`, `security.md`, ADR 0009, `features/{announcements,subscriptions}.md`, `plans/v1-mvp.md`, `project/overview.md` — ≈ 32 |

Over about 70 in one PR → stop and ask.

---

## 8. Design issues

No screen is built. The API follows `Announcements.html` (the three tabs with counts, end now on a running one,
delete on a scheduled one, the extension once started, its dialog's count and days), O9–O12, OW-014, C6–C8,
AC-009, AC-016, A7, A8, AD-012, U8, U10. Points for the screens' items, not findings:
- **Delete is allowed in any state** (O10 says "be deleted"); the prototype offers it on a scheduled one only, and
  its dialog says «يُحذف قبل أن يظهر للزوار». A running closure deleted reopens the space at once.
- **«تراجع» after end now** is an edit of `endsAt` back to its old value (allowed while it is after now; refused for
  an extended closure, S3).
- **The extension dialog's count** is the preview's `subscriptions`; it counts subscriptions the closure covered,
  not "active" ones (decision 4), and the prototype's line «تتأخر نهاية N اشتراكات نشطة» should say so.

---

## 9. Tests — lane, title, the break each catches

Every test is seen failing first in its own lane; every expectation is written by hand. A fixed clock through
`createTestApp({ clock })`; instants with their offset; Gaza dates as strings. Roles in each API file (testing
§4): **anonymous** (public and `/me` routes), a **signed-in user**, the space's **owner**, its **reception**, a
**stranger**, **another space's owner**, the **admin**. B-numbers are §12.5's breaks, each run once, its red lines
recorded.

### PR 1
**Unit**
- U1 `announcements/announcementState.unit.test.ts`: `upcoming before its start, running from its start, ended from
  its end; no end runs` (the boundaries `startsAt = now` running, `endsAt = now` ended) — B1: `startsAt >= now` for
  upcoming.
- U2 `announcements/period.unit.test.ts`: `a start 30 days back and 365 ahead at most; an end after now when set;
  at most 365 days after the start; an unchanged end on an edit is not checked against now` — B2: the end-after-now
  check dropped; B3: the edit checks an unchanged end.
- U3 `announcements/announcementChange.unit.test.ts`: `only fields set to a new value; null clears textEn and the
  end` — B4: every sent field counted as changed.
- U4 `packages/shared announcements/requests.unit.test.ts`: `a type of five, Arabic text 1–500 required, English
  nullable, instants with an offset, an end after the start (out_of_range on endsAt)` — B5: the refinement removed.

**API — `db/schema.api.test.ts`** [C1]
- D1 `two announcements never share a key in a space; two spaces may` — B6 (database): drop
  `announcements_space_id_request_id_key`.

**API — `announcements/announcements.api.test.ts`** [C1]
- T1 `the owner and reception post an announcement, 201, its state, audited announcement.created` — B7: the audit
  removed.
- T2 `a retry with the same key answers the first, 201; two at once with one key make one` (`waitingOnLock({ count:
  2 })`) — B8: `findByKey` skipped; B9: the space's lock removed.
- T3 `a missing or invalid key, and an invalid body, are 422 before anything is read` — B10:
  `requireIdempotencyKey` removed.
- T4 `the period's refusals: an end before now, a start 31 days back, an end 366 days after the start, each 422 on
  its field, writing nothing`.
- T5 `a reception link ended while the post waits on the space's lock is refused 403, writing nothing`
  (`whileHeld`) — B11: `can()` on `space.links`.
- T6 `a stranger, another space's owner and the admin get not_found on every route` — B12: the router mounted
  outside `manage` (before the boundary).
- T7 `an edit changes only what it sends, audited with before and after; the same values write nothing; textEn null
  clears; endsAt null removes the end` — B13: the no-change branch removed (an audit line appears).

**API — `announcements/lifecycle.api.test.ts`** [C2]
- T8 `end now sets the end to now on a running one, audited; an ended one answers as it is; an upcoming one is
  ANNOUNCEMENT_NOT_STARTED` — B14: the upcoming check removed (the dates `CHECK` then answers 500).
- T9 `start now sets the start to now on an upcoming one, audited; a started one answers as it is, nothing
  audited` — B15: the "started" branch removed.
- T10 `delete is soft and 204, audited; again 204 writing nothing; then it leaves the list, the public page and the
  live status` — B16: `delete` instead of setting `deletedAt` (the row gone).
- T11 `an edit, an end or a start of a deleted or another space's announcement is not_found` — B17: `lockIn`
  without the space filter.

**API — `subscriptions/closures/list.api.test.ts`** [C3]
- T12 `the list pages one state: running and upcoming by start, ended by end latest first; the total right` —
  B18: the ended tab ordered by start.
- T13 `a closure carries extension null, or its days, how many moved and who applied it; other types carry none`
  (an extension row and two links inserted directly) — B19: the count taken from the days.
- T14 `the summary counts running, upcoming and ended, and the started closures with no extension` — B20: an
  upcoming closure counted as awaiting.
- T15 `reception reads the list and the summary; a stranger and the admin not_found` — covered by B12's twin
  (the closures router mounted outside `manage`, B21).

**API — `directory/page.api.test.ts`** [C4] (existing, gaining)
- T16 `the page carries the running and upcoming announcements by start then id, each with its start and end;
  never an ended or deleted one` — B22: the `endsAt` filter dropped.
- T17 `at most 20` (21 upcoming) — B23: the `take` removed.

**API — `desk/checkIn.api.test.ts`** [C5] (existing, gaining)
- T18 `a check-in during a running closure succeeds 201 with CLOSURE_IN_FORCE after SPACE_FULL and
  OUTSIDE_OPENING_HOURS; an outage, an ended or a deleted closure warns nothing` — B24: `closedAt` replaced by any
  running announcement (an outage warns).

### PR 2
**Unit**
- U1 `packages/shared data-reports/requests.unit.test.ts`: `«أخرى» needs its message; a dismissal its note; a
  resolution's note is optional; the fields are the six` — B1: the dismissal refinement removed.
- U2 `data-reports/decision.unit.test.ts`: `an open report is decided; the same status, note and decider is as-is;
  anything else conflicts` — B2: the comparison by status only.

**API — `db/dataReports.api.test.ts`** [C1]
- D1 `one open report per user, space and field; a decided one frees the field` — B3 (database): drop
  `data_reports_open_key`.
- D2 `a decision's time, decider and side come together, and only with a decision` — B4 (database): drop
  `data_reports_decision_check`.
- D3 `a dismissal carries its reply; «أخرى» its message` — B5 (database): drop `data_reports_dismissal_note_check`.

**API — `data-reports/create.api.test.ts`** [C1]
- T1 `a signed-in user reports a listed space, 201 OPEN; anonymous is 401` — B6: `requireAuth()` removed from the
  route.
- T2 `an unknown slug, a hidden or deleted space, an inactive area are not_found` — B7: `isActiveArea` skipped.
- T3 `the same field while one is open answers it, 200, no new row; once decided a new one is 201` — B8:
  `findOpen` skipped (the index then answers 500).
- T4 `two identical reports at once make one` (`waitingOnLock` on the user's row) — B9: `lockAccount` removed.
- T5 `the 11th report within the hour is 429 with Retry-After, repeats and invalid bodies counted; another user at
  the same address is not` — B10: the limiter removed; B11: counted by address (`clientAddress`) instead of the
  user.

**API — `data-reports/myReports.api.test.ts`** [C2]
- T6 `the caller's reports, newest first, paged, filtered open or decided; another user's never` — B12: the user
  filter dropped.
- T7 `a decided report carries its status, reply and repliedBy: SPACE when the owner decided, MASAHA when the admin
  did, even after the space gained an owner` — B13: `repliedBy` from the space's verification now.
- T8 `a space that left the directory (hidden, deleted, inactive area) is listed false, with its name` — B14:
  `listed` from `deletedAt` only.

**API — `data-reports/spaceReports.api.test.ts`** [C3]
- T9 `the owner lists the space's reports, newest first, filtered; the reporter is nowhere in the answer` (the
  body serialised and searched for the reporter's id key, name and email) — B15: `userId` added to the
  repository's `select` and the mapper (the privacy rule).
- T10 `reception is 403 before the query is read; a stranger, another space's owner and the admin not_found` —
  B16: `requireCan('space.dataReports.read')` removed.
- T11 `the owner resolves with or without a reply, and dismisses with one; audited dataReport.resolved,
  dataReport.dismissed; a dismissal without a reply is 422` — B17: the audit removed.
- T12 `a decided report is REPORT_ALREADY_DECIDED; the same decision again answers it, writing nothing` — B18: the
  open check removed (the decision overwritten).
- T13 `another space's report through this space's path is not_found` — B19: `findSpaceOf` compared to nothing.
- T14 `reception's PATCH is 403 before the body is read` — B20: `requireCan('dataReports.resolve')` removed.
- T15 `an owner unlinked while the decision waits is refused 403` (`whileHeld`: the link deactivated meanwhile) —
  B21: `can()` on `space.links`.

**API — `data-reports/adminReports.api.test.ts`** [C4]
- T16 `the admin lists every report with the reporter's and decider's names, the space and whether it is verified;
  filtered by status, field and space; a deleted space's left out; a non-admin 403` — B22: the `field` filter
  ignored.
- T17 `the admin decides an unverified space's report; a verified space's is 403` — B23: `can()` replaced by the
  admin role alone.
- T18 `an owner linked while the admin's decision waits makes it 403` (`whileHeld`: an owner link inserted) — B24:
  the links read before `spaces.lock`.
- T19 `the owner and the admin at once: the second sees a decided report` (`whileHeld`: the owner's decision
  committed meanwhile, the space verified then unlinked by the test) — covered by B18.

### PR 3
**Unit**
- U1 `directory/favoritesOrder.unit.test.ts`: `saved newest first; by distance the listed nearest first and those
  that left last` — B1: the unlisted ones mixed by `savedAt`.

**API — `favorites/favorites.api.test.ts`** [C1]
- T1 `a signed-in user saves a listed space, 204; again 204 with one row` — B2: the "already saved" check removed
  (the key then answers 500).
- T2 `two saves at once make one, both 204` (`waitingOnLock` on the user's row) — B3: `lockAccount` removed.
- T3 `a hidden, deleted, unknown space, or one in an inactive area, is not saved: not_found` — B4: the listed check
  removed.
- T4 `the 201st is FAVORITES_LIMIT_REACHED; one already saved at 200 answers 204` — B5: `>` for `≥`.
- T5 `two saves of different spaces at 199 at once: one 204, one FAVORITES_LIMIT_REACHED` — covered by B3.
- T6 `remove is 204 whether saved or not; another user's favourite stays` — B6: the delete without `userId`.
- T7 `anonymous is 401 on the three routes`.

**API — `directory/favorites.api.test.ts`** [C2]
- T8 `the favourites, whole, newest saved first: a listed space as its card with its live status; a deleted or
  hidden one listed false with its name` — B7: the unlisted ones dropped.
- T9 `sort=distance with Masaha-Near: nearest first with their distance, those that left last, no-store; the header
  without sort is invalid_choice on near` — B8: `no-store` not set.
- T10 `another user's favourites never; no card carries a capacity or a count` — B9: the `userId` filter dropped.

### PR 4
**Unit**
- U1 `core/gazaTime.unit.test.ts`: `daysFrom counts calendar days across a month, a year and a leap day` — B1: off
  by one (`+ 1` inside).
- U2 `announcements/closureSpan.unit.test.ts`: `a closure's days from its start's Gaza day to its end's; an end at
  midnight covers the day before; a running one to today; a start at 23:30 UTC is the next Gaza day` — B2: dates by
  UTC; B3: `endsAt` without `− 1 ms`.
- U3 `packages/shared announcements/requests.unit.test.ts`: `days are whole, 1 to 365` — B4: the upper bound
  removed.

**API — `db/closureExtensions.api.test.ts`** [C1]
- D1 `an extended closure refuses a new type, start, deletion or later end; its text and an earlier end pass;
  another closure is untouched` — B5 (database): drop the trigger.
- D2 `an extension's key is unique` — B6 (database): drop `closure_extensions_request_id_key`.

**API — `subscriptions/closures/extension.api.test.ts`** [C2, C3]
- T1 `the preview answers the covered days, the proposal and how many it covered, writing nothing` (hand-counted) —
  B7: the preview's fragment without `ends_on >= first`.
- T2 `the owner extends: each covered subscription's end moves by the days typed, one link each, audited
  closure.subscriptionsExtended; 201 with the count` (dates by hand) — B8: the ends moved by the proposal, not the
  days.
- T3 `which move: one running through, one ending during it; not one starting after its last day, one ended before
  its first, one ended early, one with no end, another space's` — B9: `ended_at IS NULL` dropped; B10: `starts_on <=
  last` dropped; B11: the space filter dropped.
- T4 `reception is 403 before the key or body is read; a stranger and the admin not_found` — B12:
  `requireCan('subscriptions.extendAfterClosure')` removed.
- T5 `a retry with the same key answers the first, 201, moving nothing twice; another key is
  CLOSURE_ALREADY_EXTENDED; a key that extended another closure is a conflict` — B13: `findByKey` skipped.
- T6 `two owners at once with two keys make one extension` (`waitingOnLock({ count: 2 })`) — B14: the space's lock
  removed.
- T7 `an upcoming closure is ANNOUNCEMENT_NOT_STARTED; an announcement of another type, a deleted one, another
  space's, not_found; 0 or 366 days 422` — B15: the started check removed.
- T8 `an applied extension is answered by the preview instead of a proposal` — B16: `applied` not read.
- T9 `a subscription ended early, or renewed, while the extension waits is read as committed` (`whileHeld`:
  `ended_at` set; a renewal starting after the last day inserted) — B17: `lockCovered` before `spaces.lock`.
- T10 `a closure whose end moved earlier while the extension waits is extended on its new span` (`whileHeld`) —
  B18: the closure read before the lock.
- T11 `an owner whose link ended while waiting is refused 403` — B19: `can()` on `space.links`.

**API — `announcements/extendedClosure.api.test.ts`** [C3]
- T12 `after its extension a closure's delete, new type, new start and later end are CLOSURE_EXTENDED, writing
  nothing; its text and end now are 200` — B20: the translation line removed (→ 500).
- T13 `the list shows the extension applied, and the summary no longer awaits it`.

### Not tested, and said
- A closure across a daylight-saving night: the Gaza dates come from `gazaClockOf`, whose transition is pinned by
  `core/gazaTime.unit.test.ts` (#94).
- 200 real favourites with distances: T4 inserts 200 rows directly; the ordering by distance is proven on three.

---

## 10. Review Focus — inputs no planned test exercises

- A closure of more than 365 days: the proposal stops at 365 (D10); the owner cannot type more.
- A subscription covered by two closures: each extension moves it (the rule is per closure).
- A renewal started during a closure, beside the subscription it renewed: both move, and their periods overlap.
- An archived customer's subscription: covered like any other (decision 4 names no exception).
- A closure the owner chooses not to extend stays in `closuresAwaitingExtension` for ever (decision 2 as written,
  §13 Q6).
- An announcement edited from `CLOSURE` to `GENERAL` while running: the space reopens at once; the public page's
  30 s cache.
- A report on a space whose owner is suspended: still verified (security › Authorization), so the owner decides;
  the admin must unlink first.
- The admin's list with thousands of reports: paged by `status`'s index; `field` and `spaceId` filter in the same
  query.
- A favourite whose space is restored after deletion: `listed` again, the row kept (no cascade on soft delete).

---

## 11. The commits

Conventional Commits; subjects counted (≤ 50); a body that says why; no tool attribution; staged by path. Every new
decision and history line ends with `<the day's date>, #PRNUM`. **C0**, in each PR, only if a
`0_CARRIED_FROM_<n>.md` naming that PR exists in this folder when its executor starts: its items, as it says, in that
PR's first commit(s), each red first, then green, with its break; the description says "Carried from #n".

### PR 1 — `feat/announcements`, title `feat(announcements): tell users what changes` (44)
| # | Subject | Chars | Holds |
|---|---|---|---|
| C1 | `feat(announcements): post and edit announcements` | 48 | migration `announcement_key`; the six tests' keys; shared `announcements`; create and edit; U1–U4, D1, T1–T7; contract *Announcements (managed)* (create, edit); data model (*Idempotency*, *Constraints*, the state); `announcements.md` (first); conventions §6, §7, §13; security |
| C2 | `feat(announcements): end, start or delete one` | 45 | the three actions, `ANNOUNCEMENT_NOT_STARTED`; T8–T11; contract; §6 |
| C3 | `feat(subscriptions): list notices with extensions` | 49 | the composed list and summary (D4); T12–T15; contract; conventions §9 (S10); `subscriptions.md`; `announcements.md` |
| C4 | `feat(directory): show a space's announcements` | 45 | `PublicSpace.announcements` (D5), the web fixtures; T16–T17; contract (*Directory (public)*, §4); `directory.md`; v1-mvp (the `/spaces/:slug` row) |
| C5 | `feat(occupancy): warn of a closure at check-in` | 46 | D6, `CLOSURE_IN_FORCE`; T18; contract (*Front desk*'s warnings, §6); data model (*Full warning*); `occupancy.md`, `desk.md`; v1-mvp (step 10 *Built*), overview; `docs/README.md` |

### PR 2 — `feat/data-reports`, title `feat(data-reports): report and decide wrong data` (48)
| # | Subject | Chars | Holds |
|---|---|---|---|
| C1 | `feat(data-reports): report a space's wrong data` | 47 | migration `data_report_rules`; shared `data-reports`; the create, the limit; U1, D1–D3, T1–T5; contract *Data reports*; data model; security (*Built*, the limit); `data-reports.md` (first) |
| C2 | `feat(data-reports): list a user's own reports` | 45 | `GET /me/reports`, `spaces.namesWithDeleted`; T6–T8; contract; `spaces.md` (*Who uses it*) |
| C3 | `feat(data-reports): let the owner decide reports` | 48 | the owner's routes, `decision.ts` (U2), `REPORT_ALREADY_DECIDED`; T9–T15; contract, §6; conventions §6; security |
| C4 | `feat(data-reports): let the admin decide reports` | 48 | the admin's routes; T16–T19; contract; v1-mvp (the two rows, decision 10; *Built*); overview (lines 58, 62 and *Built*); `docs/README.md` |

### PR 3 — `feat/favorites`, title `feat(favorites): keep a user's favourite spaces` (47)
| # | Subject | Chars | Holds |
|---|---|---|---|
| C1 | `feat(favorites): save and remove a favourite` | 44 | shared `favorites`, `FAVORITES_LIMIT_REACHED`; T1–T7; contract *Favourites*; §6; `favorites.md` (first); security |
| C2 | `feat(directory): answer a user's favourites` | 43 | `GET /me/favorites` (D9), `FavoriteSpace`; U1, T8–T10; contract, §4's exception (C8); conventions §7, §9; `directory.md`; v1-mvp, overview; `docs/README.md` |

### PR 4 — `feat/closure-extension`, title `feat(subscriptions): extend them after a closure` (48)
| # | Subject | Chars | Holds |
|---|---|---|---|
| C1 | `feat(db): guard an extended closure` | 35 | migration `closure_extension_key` (D12), the schema test's extensions, `constraintCodes.ts`, `CLOSURE_EXTENDED`; D1–D2; data model (*Constraints*) |
| C2 | `feat(subscriptions): preview a closure's extension` | 50 | `daysFrom` (U1), `closureSpan` (U2), the covered rule, the preview; T1, T7 (its read part), T8; contract; data model (*Derived values*: covered days) |
| C3 | `feat(subscriptions): extend after a closure` | 43 | the apply, `CLOSURE_ALREADY_EXTENDED`; U3, T2–T7, T9–T13; contract, §6; data model (decision 4; *Checked by the service*; *ClosureExtension*); ADR 0009's row and *Revised*; conventions §6, §13; security; `announcements.md`, `subscriptions.md`; v1-mvp; overview (line 57, *Built*) |

---

## 12. Verification and the procedure

**The same procedure for each PR**, with that PR's branch and checks. The executor of PR *n* reads this whole
plan and builds only PR *n*.

### 12.1 Before the branch
```powershell
Set-Location C:\dev\masaha\app-b
git fetch origin
git status --short --branch            # clean, detached at origin/main
git log --oneline -10 origin/main
git diff --name-status befd96f9 origin/main
gh pr list --state open --json number,title,headRefName,headRefOid,files
Get-ChildItem C:\dev\masaha\workspace\WORKER_B\ANNOUNCEMENTS -Filter '0_CARRIED_FROM_*.md'
```
- **PR 1:** SUBSCRIPTIONS PRs 1–3 and DEMO_SEED merged (`gh pr list --state merged --search "head:feat/customers
  head:feat/subscriptions head:feat/subscription-check-ins head:chore/directory-demo-set" --json
  number,headRefName,mergeCommit`); else stop. **Re-read the merged code against §3's assumptions:** A1 (the date
  rule in `subscriptions`), A2 (`end` sets `endedAt`), A3 (each subscription write's first statement is the space's
  lock), A4, A5 (`occupancy.checkInWarnings`' signature and that `desk`'s subscriber check-in calls it), A6, A7
  (`\d subscriptions` on `masaha_b_test` lists `subscriptions_dates_check` or its equal), A8, A9 (the folders in
  `subscriptions/`), A10–A11 (the seed's accounts and the scenario subscriptions' dates). **A difference this plan
  does not cover → stop and ask.** Any other change to a code file this PR names → stop and ask.
- **PRs 2–4:** the same diff from `befd96f9`; the previous PRs' files must hold what this plan says; any other
  change to a code file this PR names → stop and ask.
- An open PR that edits a code file of this PR (worker A's PUBLIC may touch `packages/shared/src/directory/*` or
  the catalogues): stop and ask. Its documents: re-read the shared ones on the merged tree before editing.
- `0_CARRIED_FROM_<n>.md` naming this PR: read it whole and the review it cites; its items are C0 (§11). If they
  contradict this plan: stop and ask.

```powershell
git switch --no-track -c <feat/announcements | feat/data-reports | feat/favorites | feat/closure-extension> origin/main
docker start masaha-postgres-1         # never npm run db:up; never npm ci
npm run build -w @masaha/shared
```
- `apps/api/.env` names `masaha_b_dev` / `masaha_b_test` and `PORT=3321` (`Select-String` by pattern; never print
  the file).
- After a merged migration (SUBSCRIPTIONS', this item's): `npm exec -w @masaha/api -- prisma generate`, `npm run
  db:migrate` (applies to `masaha_b_dev`); `prisma migrate status` → up to date. No dependency changes; if
  `node_modules` misses a package: stop and ask.

**Memory: one full test run at a time on this machine.** Before each full lane, write the free memory into the
report and check that nothing of worker A's runs:
```powershell
Get-CimInstance Win32_OperatingSystem | Select-Object FreePhysicalMemory
Get-CimInstance Win32_Process -Filter "Name = 'node.exe'" |
  Where-Object { $_.CommandLine -match 'vitest|tsc' } | Select-Object ProcessId, CommandLine
```
- A `vitest` (or `tsc`) under `C:\dev\masaha\app\` (worker A's): wait for it to end; never stop it.
- **A full lane killed for low memory is re-run once, when the machine is quieter** (the free memory recorded
  again); **killed again → record it, carry on, and CI's run of that lane on the pushed head judges it** (red there
  → stop).

### 12.2 First checks (each when its code exists)

**Every PR**
1. **A migration, created once:** after the schema edit, `npm exec -w @masaha/api -- prisma migrate dev
   --create-only --name <name>` **once**, then `Get-ChildItem apps/api/prisma/migrations | Select-Object -Last 2`.
   Edit Prisma's `ADD COLUMN … NOT NULL` into D12's nullable column, backfill and `SET NOT NULL` before the
   unique index; append D12's raw SQL under a header comment; `npm run db:migrate`. **Never run `--create-only`
   twice** (a second run applies the first). On a data-loss refusal: `npm exec -w @masaha/api -- prisma migrate
   diff --from-migrations apps/api/prisma/migrations --to-schema-datamodel apps/api/prisma/schema.prisma
   --script` into the folder, then append, and say so. `masaha_b_test` is migrated by the API lane's global setup;
   confirm it in the first API run's output. Then check `apps/api/src/generated/prisma/models/<Model>.ts` names
   the new field.
2. **The level rule:** `npm run lint` passes with the imports of D1's *Placement*. A refusal: stop and ask.

**PR 1**
3. **The six tests that insert announcements** (`git grep -n "announcement.create" apps/api/src`): each gains
   `idempotencyKey: randomUUID()` and nothing else; if more files than §7's four do, add them and say so.
4. **Two routers on one path:** `GET …/announcements` reaches `closures`' router and `POST` reaches
   `announcements`' (T12, T1). If Express answers 404 for one: mount both in one `Router()` built in `app.ts` from
   the two modules' route functions, and say so.
5. **The web fixtures:** `git grep -n "PublicSpace" apps/web/src` — each object literal typed `PublicSpace` gains
   `announcements: []`, nothing else; `npm run typecheck` green. A fixture that needs more, or a component change:
   stop and ask (worker A's).

**PR 2**
1. **The partial unique index on an enum:** `@@unique([userId, spaceId, field], map: "data_reports_open_key",
   where: { status: 'OPEN' })` with `partialIndexes`; `prisma validate` accepts it and the migration writes `WHERE
   ("status" = 'OPEN')`. If Prisma refuses the enum literal: `where: raw("\"status\" = 'OPEN'")`; if that fails
   too: stop and ask (a raw index Prisma does not know would be dropped by a later migration).
2. **`users.lockAccount(id, tx)`** answers the account under `FOR NO KEY UPDATE` (the session lock). If its
   signature differs: use the one that locks the user's row only; if none: stop and ask.
3. **`publicListing.upTo` with `onlyIds` and `verifiedIds: []`** lists exactly the listed spaces among the ids
   (T8, T2 of PR 3). If `verifiedIds` filters instead of marking: pass `spaceLinks.verifiedSpaceIds()` and say so.
4. **The site router at the root** does not shadow `GET /spaces/:slug` (directory's existing tests stay green).

**PR 3**
1. **The ceiling's test data:** T4 inserts 200 favourites by one `INSERT … SELECT` over 200 created spaces (one
   `createMany` of spaces); if slower than Vitest's 5 s: stop and ask.
2. **The near rule:** `directory/listQuery.ts`' parsing of `Masaha-Near` is reused, not copied; if it is bound to
   `GET /spaces`' query schema, extract its header part into one function both routes call, and say so.

**PR 4**
1. **The trigger's error:** `checkViolationOf` reads `announcements_closure_extended:` (T12). If 500: stop and ask.
2. **`ends_on + integer`** in PostgreSQL is a date; Prisma's `$executeRaw` binds `days` as an integer
   (`${days}::integer`). If not: stop and ask.
3. **The demo data (A11):** at least one demo subscription is covered by a closure started two days ago; if none:
   stop and report (§12.6).

### 12.3 Implement, commit by commit
- Stage **by path** (never `-A` or `.`), `git status --short` before each commit; after each commit `npm run lint`
  and `npm run typecheck`.
- Inside each commit: the test first, run red in its lane (the red output in the report); the code, then green; the
  commit's documents (Appendix A).
- **Each new error code follows conventions §4, in this order** (the `add-error-code` skill's steps): (1) the code
  in `packages/shared/src/core/errors.ts`'s list; (2) its text in **both** `apps/web/src/shared/copy/arabic/
  errors.ts` and `…/english/errors.ts` (the typecheck fails while one is missing), the Arabic as §13 Q1 writes it;
  (3) its line in api-contract §6; (4) the test that provokes it (§9); and in the PR description, each code with
  its English and Arabic, the Arabic marked for the owner's approval.
- Each commit message in a UTF-8 file, **no BOM, LF line endings**, with a body; `git commit -F <file>`.
- **A fix before the push** folds into its commit:
  ```powershell
  git commit --fixup=<sha> -- <paths>
  $env:GIT_SEQUENCE_EDITOR=':'; git rebase -i --autosquash $(git merge-base HEAD origin/main); Remove-Item Env:GIT_SEQUENCE_EDITOR
  git rebase -x "npm run lint && npm run typecheck" $(git merge-base HEAD origin/main)
  ```
- **Fix rounds** (after a review) run only what the change touches: its lanes' files, lint, typecheck, and the
  head's lanes again only where a file they cover changed.

### 12.4 Verification on the head (phase 4)
- One at a time, each **once, on the head** (re-run only if a file it covers changed after it passed): `npm run
  lint` · `npm run typecheck` · `npm run test:unit` · `npm run test:api` · `npm run format:check` · `npm run
  check:links` · `npm run build -w @masaha/shared` (the shared package changes in every PR).
- Also: `git grep -n "#PRNUM"` lists only documents (before §12.7); `git diff --stat origin/main -- apps/web` shows
  only the two `errors.ts` (and PR 1's fixtures); `git diff --stat origin/main -- package.json package-lock.json` is
  empty.
- **Not run, with why:** `test:component`, the web's `build`, `check:build`, `check:classes`: the web change is
  catalogue strings (and PR 1's typed fixtures), whose parity and types the typecheck enforces; CI runs them on the
  pushed head.

### 12.5 The breaks — every one run, its red recorded
- For each B of §9: back up the file into `scripts\breaks\` (this folder), make the one edit, run the named test file
  in its lane, copy the red lines into the report, restore **from the backup** (never `git checkout`; SHA-256 before
  and after, no CRLF change — Python writes with `newline=""`), run it green, then `git diff --stat` shows only the
  item's own work. The scripts (`scripts\brk.py` and its JSON, as SUBSCRIPTIONS did) stay uncommitted.
- **Database breaks** (on `masaha_b_test` only, through `docker exec masaha-postgres-1 psql`): drop the index,
  constraint or trigger (PR 1 B6; PR 2 B3–B5; PR 4 B5–B6); the named test red; restore by re-running the
  migration's statement; green.
- **Every permission, privacy rule, limit, key and race has its break:**
  - permissions — owner, reception, admin, signed-in user, anonymous: PR 1 B11, B12, B21; PR 2 B6, B16, B20, B21,
    B23, B24; PR 3 B6, B9 (and T7's anonymous); PR 4 B12, B19;
  - privacy (the reporter never shown to the owner): PR 2 B15;
  - the rate limit: PR 2 B10, B11;
  - idempotency: PR 1 B8, B10; PR 2 B8; PR 3 B2; PR 4 B13;
  - races: PR 1 B9, B11; PR 2 B9, B21, B24; PR 3 B3; PR 4 B14, B17, B18, B19.
- **A break that stays green: stop**, unless it is plainly your own test's defect, or the plan's break cannot
  change the outcome (a bound already excluded by another rule); then make the break that can, see it red, and
  state it as a departure.

### 12.6 The real run (API on 3321, `masaha_b_dev`)
Start `npm run dev -w @masaha/api` in the background (log to `scripts\server.log`, deleted afterwards);
`curl.exe -s http://localhost:3321/health` → `db: up`. Sign in as `demo-owner@example.com`,
`demo-reception@example.com`, `demo-directory-owner@example.com` and the seed's admin (`SEED_DEMO_PASSWORD` and
`SEED_ADMIN_*` read from `apps/api/.env` into variables, never printed). The script is `scripts\realrun<n>.mjs`.
Record each status. **A demo account or data that does not hold what a case needs → stop and report; never change
data through the app to get past it.** The cases' own writes are the feature under test; say what they changed.
- **PR 1** (the demo space): reception `POST …/announcements { type: CLOSURE, textAr, startsAt: now }` with key K →
  201 `RUNNING`; K again → the same id; `GET …/announcements?state=RUNNING` → it, `extension: null`; anonymous `GET
  /spaces/<slug>` → it in `announcements`; `GET /spaces/<slug>/occupancy` → `CLOSED`; reception `POST …/visits`
  (a key) → 201 with `CLOSURE_IN_FORCE`; then its check-out (a key) with a payment equal to the charge its quote
  shows (`GET …/visits/:visitId`), so no stay is left open — with no rate, the owner closes it with a typed charge
  and a reason; record which; `PATCH` the text → 200; `POST …/end` → 200 `ENDED`; the page no longer shows it; an upcoming `GENERAL`
  tomorrow → `UPCOMING`; `POST …/start` → `RUNNING`; `DELETE` → 204; again → 204; `GET …/summary`; the
  directory owner on the demo space → 404. `SELECT action FROM audit_logs ORDER BY id DESC LIMIT 10`.
- **PR 2** (the limit counts every request of `demo-reception`'s, so its cases run in this order): `demo-reception`
  (a global USER) `POST /spaces/<a verified set space>/reports { field: PRICES }` → 201; again → 200, the same id;
  `POST /spaces/<an unverified set space>/reports { field: HOURS }` → 201; `{ field: OTHER }` without a message →
  422; `GET /me/reports` → both `OPEN`; the directory owner `GET …/data-reports` → no reporter anywhere (search the
  body for the reporter's name, email and id); `PATCH { status: RESOLVED, note }` → 200; `{ status: DISMISSED }` →
  409 `REPORT_ALREADY_DECIDED`; the admin `GET /admin/data-reports` → the reporter's name; the admin on the
  verified space's report → 403; on the unverified one `PATCH { status: DISMISSED }` → 422, with a note → 200;
  `GET /me/reports?status=DECIDED` → `repliedBy: SPACE` and `MASAHA`; last, on the verified space, `{ field:
  CONTACT }` once (201), then the same again until the 11th request of the hour → 429 with `Retry-After` (the
  repeats write nothing; record how many requests were sent).
- **PR 3:** `demo-reception` `POST /me/favorites/<listed id>` → 204, twice; `GET /me/favorites` → its card; with
  `Masaha-Near` and `sort=distance` → `distanceMeters`, `no-store`; `POST` an unknown id → 404; `DELETE` → 204;
  anonymous → 401.
- **PR 4** (the demo space, check 3): reception `POST …/announcements { CLOSURE, startsAt: now − 2 days, endsAt: now
  + 1 hour }` (a key); `GET …/extend-subscriptions` → `proposedDays: 3` and the count (record which subscriptions);
  reception `POST` → 403; the owner `POST { days: 3 }` with key E → 201 and the count; E again → the same; another
  key → 409 `CLOSURE_ALREADY_EXTENDED`; `GET …/customers/<id>` (or the statement) → the end three days later;
  `PATCH { type: GENERAL }` → 409 `CLOSURE_EXTENDED`; `DELETE` → 409; `POST …/end` → 200. `SELECT * FROM
  subscription_extensions` → one row each.
- Stop the server by its process ids (the `tsx watch` child, the server, `pino-pretty`); `Get-NetTCPConnection
  -LocalPort 3321 -ErrorAction SilentlyContinue` prints nothing.

### 12.7 The PR number, push and PR
Just before the push, in Git Bash:
```bash
n=$(( $(gh api "repos/{owner}/{repo}/issues?state=all&per_page=1&sort=created&direction=desc" --jq '.[0].number') + 1 ))
base=$(git merge-base HEAD origin/main)
git filter-branch -f --tree-filter "grep -rl '#PRNUM' docs | xargs -r sed -i 's/#PRNUM/#$n/g'" $base..HEAD
git for-each-ref --format='%(refname)' refs/original/ | xargs -r -n1 git update-ref -d
git grep -n '#PRNUM' ; echo "expect nothing above; PR will be #$n"
npm run check:links; npm run format:check
git push -u origin <branch>
```
- `gh label list`: `feat`, `area:api`, `area:docs`, `area:web` must exist (create a missing one with a description
  and a colour).
- Then at once:
  ```powershell
  gh pr create --assignee @me --label feat --label area:api --label area:docs --label area:web `
    --title "<the PR's title, §11>" --body-file <§12.9's text, saved in scripts\>
  ```
- GitHub's number must equal `n`; if not, fix the documents (a fixup into the commits that hold it) and `git push
  --force-with-lease`.

### 12.8 CI, CLEAN, conflicts, report
- `gh pr checks <n> --watch` (bounded), then `gh pr view <n> --json headRefOid,mergeStateStatus`: green **on the
  pushed head** (= `git rev-parse HEAD`) and `CLEAN`. Never merge; never rebase a `CLEAN` PR.
- **Conflicts:** for every other open PR, `git merge-tree --write-tree HEAD <its headRefOid>`; record clean or the
  conflicted paths. Documents only: the fast path when its turn comes. Code: stop and ask.
- **The report**, `4_REPORT_PR<n>.md` in this folder, written **as the work goes**: after the first checks, after
  each commit (sha, subject with its length, red, green), after each break, after the real run, after the push. It
  holds each command run or not, §12.2's results, the owner's answers to §13 as built, problems and their solutions,
  anything unexpected, the conflict check, every departure with why.
- **PR 1's report** updates `C:\dev\masaha\workspace\_SHARED\OPEN_DECISIONS.md` point 2: "**settled (#n, <date>):**
  reception posts a closure; the owner learns of it in the app only — the managed list's extension state per
  closure and the summary's `closuresAwaitingExtension`, which the overview (step 12) reads through `subscriptions`'
  `closures.summary`; no email". **PR 4's report** appends "the extension built (#n)". The supervisor commits
  nothing there.
- **Never leave silently:** an executor that would leave a carried item, a review nit or a planned break undone
  stops and asks.

### 12.9 The PR description
```markdown
## Summary
<PR 1: announcements posted (idempotent), edited, ended, started and deleted by the staff; the managed list with each closure's extension state and the summary; the public page's announcements; the closure warning at check-in.
 PR 2: data reports: a signed-in user's report (10 an hour, a repeat answers the open one), their own list with the reply; the owner's and the admin's lists and decisions, the reporter anonymous to the owner.
 PR 3: favourites saved and removed (idempotent, at most 200), answered whole as the directory's cards.
 PR 4: the closure extension: the preview, the owner's extension once per closure under one key, an extended closure guarded by the database.>
<"Carried from #n": each item, if C0 exists>

## Scope / Acceptance criteria / Out of scope
<§2, this PR's part>

## Change type
feat — API code, the shared contract, tests and documents; <PR 1: a migration (announcements' key) | PR 2: a migration (the reports' rules and who replied) | PR 3: none | PR 4: a migration (the extension's key and the trigger)>; the new codes' catalogue lines in apps/web (and PR 1's PublicSpace fixtures), worker B's licence.

## New error codes (the Arabic needs the owner's approval)
<this PR's lines of §13 Q1>

## Evidence
- `lint`, `typecheck` (each commit), `test:unit`, `test:api`, `format:check`, `check:links`, `build -w @masaha/shared`: <results>.
- Seen failing first: <each test, its red line>.
- Deliberate breaks, each red then restored: <the PR's B-list>.
- Real run on 3321: <statuses>.
- Not run: `test:component`, the web's `build`, `check:build`, `check:classes` — catalogue strings (and typed fixtures); CI runs them.

## Screenshots
None: API and documents only.

## Definition of Done checklist
- [x] Acceptance criteria met, scope kept.
- [x] Lint and typecheck clean; `packages/shared` builds.
- [x] Tests added in the owning lanes, each seen failing.
- [x] No hardcoded user-facing text (codes only; both catalogues).
- [x] Authorization on the server (`requireAuth`, the boundary, `requireRole`, `requireCan`, `can()` under the lock).
- [x] Triggered documentation updated in this PR.
- [x] One home per fact; nothing claimed that is not built.
- [x] Every claim names its test or command.
- [x] Atomic history, pushed.
```

### The executor's stop rule — a test you cannot run stops the work
A test **failing** because its code is not written yet is the plan's red step — normal. A test, lane or command you
**cannot run** is not: it errors before any test runs (the database unreachable, Docker down, a port taken, a module
or `dist` missing, a migration pending, `No test files found`, a Vitest or TypeScript startup error, the whole run
timing out, a crash with no result); a break you could not make or run; a real-run case you could not perform.
**Then stop at once** — never skip, `.skip` or delete a test, never change a config, a timeout, `.env`, a script or a
lane, never mock what the plan does not, never run a narrower command and call it the lane, never call it "flaky" and
move on. Write the command, its exact error and where you were into the report, and reply with the exec prompt's
final shape, `Status: STOPPED`. (The one exception is a full lane killed for low memory: §12.1's rule.)

**A plan that proves false against the code:** stop too, say exactly what and why, and offer the fix — do not choose
it yourself. **A break that stays green:** stop — unless it is plainly your own test's defect, or the plan's break
cannot change the outcome (a bound already excluded by another rule); then make the break that can, see it red, and
state it as a departure.

**Never claim a result you did not see:** a command passed only if you saw its own output say so; copy that line
(read it by its exit code, not the tail). A break counts only when you saw it red.

### Stop and ask
- SUBSCRIPTIONS PRs 1–3 or DEMO_SEED not merged, or merged with a shape §12.1's re-read does not match (A1–A11);
  `origin/main` changed a code file of §7 otherwise; an open PR edits one of them; a carried file contradicts this
  plan.
- A change needed in `apps/web` beyond the catalogues and PR 1's typed fixtures, a dependency, an error code not in
  §13 Q1, or a schema change beyond D12.
- More than about 70 files in one PR.
- A migration that cannot be made as §12.2 says; Prisma refusing the partial index on an enum with both forms.
- `checkViolationOf` not naming `announcements_closure_extended`.
- The level rule refusing an import of D1.
- A real-run case the demo data cannot hold.
- A break that stays green (§12.5's exception aside).
- A failure not understood after three root-cause fixes; CI failing for a reason not reproduced locally after three.
- A conflict with another open PR in a code file.
- An item you would leave undone (a carried item, a review nit, a break).
- The owner's answer to §13 changing a test or a rule beyond what it says.

---

## 13. Decisions needed from the owner

1. **Q1 — the new codes and their lines (the Arabic for your approval):**

   | Code | PR | Answer | English | Arabic |
   |---|---|---|---|---|
   | `ANNOUNCEMENT_NOT_STARTED` | 1 | 409 | This announcement has not started yet. | لم يبدأ هذا الإعلان بعد. |
   | `CLOSURE_IN_FORCE` | 1 | warning | The space is announced closed now; the check-in was recorded anyway. | المساحة معلَنة مغلقة الآن، وسُجّل الحضور رغم ذلك. |
   | `REPORT_ALREADY_DECIDED` | 2 | 409 | This report was already decided. | سبق البتّ في هذا البلاغ. |
   | `FAVORITES_LIMIT_REACHED` | 3 | 409 | Your favourites are full; remove a space first. | امتلأت مفضّلتك؛ أزل مساحة أولًا. |
   | `CLOSURE_ALREADY_EXTENDED` | 4 | 409 | This closure's subscriptions were already extended. | مُدّدت اشتراكات هذا الإغلاق من قبل. |
   | `CLOSURE_EXTENDED` | 4 | 409 | Subscriptions were extended for this closure: it is not deleted, and its type, start and later end stay as they are. | مُدّدت الاشتراكات بهذا الإغلاق، فلا يُحذف، ولا يتغيّر نوعه ولا بدايته، ولا تتأخر نهايته. |

   Reused: `SPACE_FULL`, `OUTSIDE_OPENING_HOURS` (D6's order), and the 429 of the rate limiter (no code).
2. **Q2 — the placements (S10):** the managed announcements list and its summary composed by `subscriptions`; the
   overview (step 12) reads `closures.summary`. *Alternatives:* A1, A2.
3. **Q3 — S3:** an extended closure's end may still come earlier (end now included); a later end, a new start or
   type, and deletion refused. *Otherwise:* every period change refused, and the extension only once the closure
   has ended (decision 3 changed).
4. **Q4 — the schema:** PR 1 `announcements.request_id` (S1); PR 2 `data_reports.resolved_as` (S7), the partial
   unique index and the three `CHECK`s (S6); PR 4 `closure_extensions.request_id` and the trigger (S2, S11). PR 3:
   none.
5. **Q5 — S8:** a decision retried identically answers as it is (decision 11 refined).
6. **Q6 — the overview's count:** every started closure with no extension, however old (decision 2 as written).
   *Otherwise:* only those started within the last 30 days, so a closure deliberately left unextended stops
   asking.
7. **Q7 — S5's bounds:** texts 1–500; a start at most 30 days back and 365 ahead; an end at most 365 days after its
   start; 20 announcements on the page; 1–365 days of extension.
8. **Q8 — A8:** PR 4 second, or the order as decided.
9. **Q9 — the favourites' distance (D9):** `sort=distance` with `Masaha-Near` on `GET /me/favorites` (AC-014).
   *Otherwise:* A5.

---

## Appendix A — the documents, line by line (the commit in brackets)

Every new decision and history line ends with `<the day's date>, #PRNUM`; *Last Updated* on each document changed.
New capability documents follow the template of `docs/architecture/documentation.md` §5.

### PR 1
1. **`api-contract.md`** — new section *Announcements (managed)* after *Front desk (managed)*: the five writes (body,
   the period's rules, the key, the retry, the answers, `ANNOUNCEMENT_NOT_STARTED`), the list (query, state, order,
   `ManagedAnnouncement`, `extension`), the summary; `Announcement`, `ExtensionApplied`; audit names [C1–C3]; §1's
   *Idempotency key* "Built for …" + "an announcement's post" [C1]; *Directory (public)*: `PublicSpace.announcements`
   and `PublicAnnouncement`, the 30 s cache line [C4]; §4: the public page's announcements (≤ 20) [C4]; *Front desk*'s
   warnings: `CLOSURE_IN_FORCE` third [C5]; §6: the two codes [C2, C5].
2. **`data-model.md`** — *Conventions › Idempotency*: + announcements [C1]; *Constraints*: the key [C1]; *Derived
   values*: an announcement's state (D3) [C1]; *Full warning*: + "and while a closure runs, `CLOSURE_IN_FORCE`"
   [C5].
3. **`conventions.md`** — header *Built*: + "`announcements` (posting, editing, ending, starting, deleting; the
   public ones)" [C1]; §6's list + "announcements created, edited, started, ended and deleted" [C1]; §7's table
   (`announcements`' and `subscriptions`' *Holds*) [C1, C3]; §9 *Composed reads*: the managed announcements list
   (S10) [C3]; *The front desk*: the closure warning [C5]; §13: announcements carry the key [C1].
4. **`security.md`** — *Authorization*: `requireCan('announcements.manage')` on the announcements' writes [C1].
5. **`docs/features/announcements.md`** (new) [C1–C3]; **`subscriptions.md`** (the composed list) [C3];
   **`directory.md`** (the page's announcements; remove "The announcements … are not built" for them) [C4];
   **`occupancy.md`** (the warning; `announcements`' boundary line now links its document) [C5]; **`desk.md`** (the
   warning) [C5].
6. **`docs/README.md`** — the map's line for `announcements.md` [C5].
7. **`v1-mvp.md`** — step 10 *Built*: "announcements and the closure warning (#PRNUM)"; the `/spaces/:slug` row's
   note, the two announcements rows into the *Built* sentence [C4, C5].
8. **`overview.md`** — *Built*: an *Announcements* line (on the API) [C5].

### PR 2
1. **`api-contract.md`** — new section *Data reports*: the create (the limit, the repeat's 200, 404, 401), the user's
   list (`listed`, `repliedBy`), the owner's list and decision (🏢, the reporter never answered), the admin's list
   and decision (verified → 403); the shapes; audit names; §6: `REPORT_ALREADY_DECIDED` [C1–C4].
2. **`data-model.md`** — *Entities › DataReport*: + who replied (S7); *Constraints*: S6's index and `CHECK`s;
   *Derived values* or *Checked by the service*: "a repeated report while one is open is the open one" [C1, C3].
3. **`conventions.md`** — header *Built*: + `data-reports`; §7's routers line [C1, C4].
4. **`security.md`** — header: the data-report limit moves to *Built*; *Rate limits*: unchanged numbers; *Authorization*:
   the owner's routes' `requireCan`, the admin's `can()` under the lock [C1, C3, C4].
5. **`docs/features/data-reports.md`** (new) [C1–C4]; **`spaces.md`** — *Who uses it*: `namesWithDeleted` [C2].
6. **`docs/README.md`** [C4]; **`v1-mvp.md`** — the two `data-reports` rows (decision 10: "resolve with an optional
   note, or dismiss with a required one"), the `POST /spaces/:slug/reports` and `/me/reports` rows into *Built* [C4];
   **`overview.md`** — lines 58 and 62 ("resolved with an optional note, or dismissed with a reply"), *Built* [C4].

### PR 3
1. **`api-contract.md`** — new section *Favourites*: the three routes, `FavoriteSpace`, the order, the near rule;
   §4's exception (C8); §6 [C1, C2].
2. **`conventions.md`** — §7: `directory`'s routers + me; §9's favourites line as built [C2].
3. **`security.md`** — *Location*: + `GET /me/favorites` [C2].
4. **`docs/features/favorites.md`** (new) [C1, C2]; **`directory.md`** — the favourites' cards [C2].
5. **`docs/README.md`**, **`v1-mvp.md`** (the `/me/favorites` row), **`overview.md`** (*Built*) [C2].

### PR 4
1. **`api-contract.md`** — *Announcements (managed)* gains the preview and the extension (the rule, the days, the key,
   the retry, no undo); `CLOSURE_EXTENDED` on the writes; §6: the two codes [C1–C3].
2. **`data-model.md`** — *Constraints*: the trigger and the key [C1]; *Derived values*: the covered days (S4) [C2];
   *Entities › ClosureExtension* and *Checked by the service*: decision 4's rule (approved 2026-10-21) [C3].
3. **`conventions.md`** — §6: + "a closure's extension"; §13: the extension's key; *The ledger's rules* neighbour: the
   trigger is the database's, as the ledger's are [C1, C3].
4. **`security.md`** — `requireCan('subscriptions.extendAfterClosure')` [C3].
5. **ADR 0009** — row "Extend the subscriptions a closure covered, once it has started" + *Revised* [C3].
6. **`announcements.md`**, **`subscriptions.md`** [C1–C3].
7. **`v1-mvp.md`** — step 10 *Built* complete; the extension row [C3]. **`overview.md`** — line 57 ("after a closure,
   the owner extends the subscriptions it covered by the days typed"), *Built* [C3].

## Appendix B — Claude Code skills, only a map

| Step | Skill (if the executor is Claude Code) |
|---|---|
| §12.1, the branch | `start-work-item` (its git part) |
| Each test red first, each break | `superpowers:test-driven-development` (workflow §10) |
| Each new error code (§13 Q1) | `add-error-code` |
| Any failure | `superpowers:systematic-debugging` |
| §12.4 before any claim | `superpowers:verification-before-completion` |
| §12.7–12.8 | `open-pr`, then `final-report` |

Only a map: the plan and the documents decide, and a skill that disagrees with them loses.
