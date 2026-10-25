## Summary
Data reports, on the API: a signed-in user's report of a listed space's wrong information (10 an hour, a repeat answering the open one), their own list with the reply and who gave it; the owner's and the admin's lists and decisions, the reporter anonymous to the owner. A decided report is final (`REPORT_ALREADY_DECIDED`); the same decision again answers as it is.

**Carried from #118** (its review, `0_CARRIED_FROM_118.md`), the first three commits, each new test proven red under its break:
1. A refresh renews no idle clock: reception refreshes at T+10 min, the new row keeps T, and T+15:01 is `SESSION_IDLE` (break: `issueInFamily` writes `at` → red).
2. Spec D with a shift's published price: the shift's price and its `shiftId` copied, the price with no shift copying none (break: `findStandard` drops the shift → red).
3. ADR 0003's revised line (the guard refuses an idle session, the refresh ends it); `security.md`'s *Idle (reception)* row: a soft-deleted space's links count, as for `OWNER`.
4. The test helper's session clock: `signAccess` sets `lastActivityAt` far ahead.
5. Findings **170** (a renewal racing a rotation can be lost on the newest row) and **171** (a published price changed before the subscribe is charged silently), recorded.

## Scope / Acceptance criteria / Out of scope
**Scope**
1. Migration `data_report_rules`: the enum `DataReportResolver` and `data_reports.resolved_as`; the partial unique index of one open report per user, space and field; `CHECK`s on a decision's fields, a dismissal's reply and «أخرى»'s message.
2. `@masaha/shared/data-reports` (L3).
3. `POST /spaces/:slug/reports` (👤, the 10-per-hour limit) and `GET /me/reports` (👤, paged).
4. `GET /manage/spaces/:spaceId/data-reports` and `PATCH …/data-reports/:reportId` (🏢).
5. `GET /admin/data-reports` and `PATCH /admin/data-reports/:reportId` (🛡).
6. Error code `REPORT_ALREADY_DECIDED` (409). `security.md`'s *Not yet built: the data-report limit* → built.
7. `docs/features/data-reports.md` (new).

**Acceptance criteria**
- [x] A signed-in user reports a listed space's field group (`OTHER` with a message), 201 `OPEN`; an unlisted or unknown space is 404; anonymous is 401.
- [x] The same user, space and field while one is open answers that report, 200, writing nothing; two at once make one; the database holds the rule (partial unique index).
- [x] The 11th report of a user within the hour is 429 with `Retry-After`, counted at the route before the body is read, repeats included; another user at the same address is unaffected.
- [x] `GET /me/reports` pages the caller's reports newest first, filtered by open or decided; each decided one carries its status, reply and `repliedBy` (`SPACE` or `MASAHA`, as stored); a space that left the directory carries `listed: false` and its name.
- [x] The owner (🏢; reception 403 before anything is read) lists the space's reports, never the reporter (no name, id or email anywhere in the answer), and resolves (reply optional) or dismisses (reply required) an open one, audited; the admin lists every report with the reporter's name and decides an unverified space's only (403 for a verified one).
- [x] A decided report is final: another decision is 409 `REPORT_ALREADY_DECIDED`; the same decision by the same person with the same reply answers as it is.
- [x] Who decides is read under the space's lock: an owner linked or unlinked while a decision waits decides it.

**Out of scope:** the screens 11, 23 and 28 and the space page's report button (worker A's later items); editing the space from a report («تعديل الحقل» is navigation); notifications; reviews, booking, QR, claiming, online payment (*Not in v1*).

## Change type
feat — API code, the shared contract, tests and documents; a migration (the reports' rules and who replied); the new code's catalogue lines in `apps/web` (worker B's licence). C0: tests and documents only.

## New error codes (the Arabic needs the owner's approval)
- `REPORT_ALREADY_DECIDED` (409) — English: «This report was already decided.» — Arabic: «سبق البتّ في هذا البلاغ.» (as approved in the plan's Q1; listed for the owner's approval)

## Evidence
- `lint`, `typecheck` (each commit), `test:unit` (shared 259, api 875, web 950 passed), `test:api` (90 files, 1198 tests passed), `format:check`, `check:links`, `check:conflicts`, `build -w @masaha/shared`: all exit 0 on the head.
- Seen failing first: U1, U2 (the module missing); D1–D3 proven by their database breaks; T1–T5 (4 of 5 red, `404`; T2 proven by B7); T6–T8 (3 of 3); T9–T15 (6 of 7; T13 proven by B19); T16–T19 (4 of 4).
- Deliberate breaks, each red then restored from its backup (SHA-256 same) and green: C0-1, C0-2, B1–B24 (B3–B5 on the test database, restored and compared with the dev database: identical).
- Real run on 3321 (`masaha_b_dev`, the demo set), `ALL PASS`: 201 · 200 (the same id) · 201 · 422 · 200 · 200 (no reporter anywhere) · 200 (SPACE) · 409 `REPORT_ALREADY_DECIDED` · 200 (the reporter's name) · 403 · 422 · 200 (MASAHA) · 200 (SPACE and MASAHA) · 201 · 429 with `Retry-After` on the 11th request.
- Not run locally: `test:component`, the web's `build`, `check:build`, `check:classes` — the web change is two catalogue strings, whose parity the typecheck enforces; CI runs them.

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
