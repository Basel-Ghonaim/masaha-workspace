## Summary

The closure extension, on the API. Once a closure has started, the staff preview it: the closure's covered Gaza days, the days the server proposes and how many subscriptions it covered. The owner then moves every covered subscription's end by the days typed, once per closure, under one key. An extended closure is guarded by the database: it keeps its type, its start and its existence, and its end may only come earlier.

**Carried from #121** (its review; the first two commits):
- **Item 1:** the favourite's "is it listed" read now runs before the user's lock (conventions §8), and the answers keep their order.
- **Item 2:** #121's decision, contract and conventions lines are dated.
- **Item 3:** `directory.md`'s *Authority* names the signed-in favourites.
- **Item 4:** two documented behaviours are tested: a saved space that left is still 204 when saved again; a favourite in an inactive area is `listed: false`. Each was seen red under its break.
- **Item 5:** the favourites' tie now states its direction ("the higher space id first").
- `0_CARRIED_FROM_120` item 4 (`apps/api/test/app.ts`) stays open: no commit touches that file.

## Scope / Acceptance criteria / Out of scope

**Scope**
1. Migration `closure_extension_key`:
   - `closure_extensions.request_id` (UUID, required, unique on its own; existing rows backfilled);
   - the trigger `announcements_guard_extended` (decision 6, refined by S3).
2. `GET …/announcements/:announcementId/extend-subscriptions` (🧾, the preview) and `POST …` (🏢, `Idempotency-Key`), in `subscriptions`.
3. `CLOSURE_ALREADY_EXTENDED` and `CLOSURE_EXTENDED` (409); `ANNOUNCEMENT_NOT_STARTED` reused.
4. Documents rewritten for decision 4 (approved 2026-10-21): `data-model.md` and `overview.md`, plus ADR 0009's row and a *Revised* line.

**Acceptance criteria**
- [x] The preview answers the closure's first and last covered Gaza day, the proposed days and how many subscriptions it covered, writing nothing. An applied extension is answered instead (T1, T8).
- [x] Only the owner extends: reception gets 403 before the key or the body is read. It needs a started closure (`ANNOUNCEMENT_NOT_STARTED`), happens once per closure (`CLOSURE_ALREADY_EXTENDED`), and takes 1–365 days (T4, T5, T7, U3).
- [x] Every subscription of the space running on any covered day moves its end by the days typed (T2, T3):
  - it started on or before the last day and ends on or after the first, even if it ended during the closure;
  - never one ended early, or one with no end;
  - one `SubscriptionExtension` each, in one transaction, audited.
- [x] A retry with the same key answers the first result, 201; two owners at once make one extension (T5, T6).
- [x] An extended closure is not deleted, retyped, restarted or given a later end: 409 `CLOSURE_EXTENDED`, held by the database. Its text and an earlier end (end now included) still change (D1, T12).

**Out of scope:** the screens (worker A's later items); the owner's overview (step 12); notifications; an undo of an extension (decision 5: corrected per subscription).

## Change type

feat — API code, the shared contract, tests and documents.
- A migration: the extension's key and the trigger.
- The two new codes' catalogue lines in `apps/web` (worker B's licence).

## New error codes (the Arabic needs the owner's approval)

| Code | Answer | English | Arabic |
|---|---|---|---|
| `CLOSURE_EXTENDED` | 409 | Subscriptions were extended for this closure: it is not deleted, and its type, start and later end stay as they are. | مُدّدت الاشتراكات بسبب هذا الإغلاق، فلا يمكن حذفه ولا تغيير نوعه أو بدايته ولا تأخير نهايته. *(Q1, approved 2026-10-21)* |
| `CLOSURE_ALREADY_EXTENDED` | 409 | This closure's subscriptions were already extended. | مُدّدت اشتراكات هذا الإغلاق من قبل. |

## Departures from the plan

- **`daysFrom` moved, not added:** it moved from `subscriptionStatus.ts` (private) to `packages/shared/src/core/gazaTime.ts`, is exported, and is imported back. One function, not a copy.
- **`lockClosure` reuses the existing lock:** it is `repository.lockIn` plus the `CLOSURE` check, with no second lock statement.
- **The repository's names:** `isExtended` stands for D11's `findFor`, and `createExtension` writes the extension with its links (D11's `linkSubscriptions`), still two statements.
- **One more test file gains keys:** `list.api.test.ts` also inserts extensions (PR 1's), so it gains `idempotencyKey` beside `schema.api.test.ts`.
- **T9 adds a covered subscription** where the plan named a renewal starting after the last day (which is never covered). The renewal case proves nothing about the race; the covered insert proves that a write made while the extension waits is read as committed.

## Evidence

- **On the head:**
  - `lint`, `typecheck` (also each commit), `format:check`, `check:links`, `check:conflicts`, `build -w @masaha/shared`: all green.
  - `test:unit`: 261, 877 and 978 tests passed (the three workspaces).
  - `test:api`: 95 files, 1224 tests passed (the second run: the first was killed for low memory, no test failed)
- **Seen failing first:**
  - U1: `TypeError: daysFrom is not a function`.
  - U2: `Cannot find module './closureSpan.ts'`.
  - U3: `Cannot read properties of undefined (reading 'parse')`.
  - T1, T7, T8: `expected 404 to be 200/409`.
  - T2–T7, T9–T13: 11 failed (`404`, or `never waited on a lock`).
- **Deliberate breaks, each red, then restored from a backup and green:**
  - C0a, C0b (carried item 4);
  - B1–B4 (`daysFrom`, the UTC dates, `− 1 ms`, the upper bound);
  - B5–B6 (the trigger dropped, the key's index dropped);
  - B7–B11 (the covered rule's clauses, and the days moved);
  - B12 (the permission), B13 (the key), B14 (the space's lock), B15 (the started check), B16 (the applied answer);
  - B17–B19 (lock order, closure read under the lock, `can()` under the lock), B20 (the translation).
- **Real run on 3321 (`masaha_b_dev`, the demo space), ALL PASS:**
  - reception posts a closure started two days ago: 201;
  - the preview: `proposedDays: 3`, 4 subscriptions;
  - reception extends: 403;
  - the owner extends `{ days: 3 }`: 201; the same key again: 201 with the same body; another key: 409 `CLOSURE_ALREADY_EXTENDED`;
  - each of the 4 ends moved +3 days;
  - `PATCH` type and `DELETE`: 409 `CLOSURE_EXTENDED`; end now: 200;
  - one `subscription_extensions` row each.
- **Not run locally:** `test:component`, the web's `build`, `check:build`, `check:classes`. The web change is two catalogue lines each, whose parity the typecheck enforces; CI runs them.

## Screenshots

None: API and documents only.

## Definition of Done checklist
- [x] Acceptance criteria met, scope kept.
- [x] Lint and typecheck clean; `packages/shared` builds.
- [x] Tests added in the owning lanes, each seen failing.
- [x] No hardcoded user-facing text (codes only; both catalogues).
- [x] Authorization on the server (`requireCan('subscriptions.extendAfterClosure')`, `can()` under the space's lock).
- [x] Triggered documentation updated in this PR.
- [x] One home per fact; nothing claimed that is not built.
- [x] Every claim names its test or command.
- [x] Atomic history, pushed.
