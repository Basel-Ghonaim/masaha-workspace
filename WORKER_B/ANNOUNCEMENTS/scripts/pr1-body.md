## Summary

Announcements on the API, step 10's first of four PRs (#112): the staff (owner and reception) post an announcement — idempotent, announcements gain their key — edit it, end it now, start it now and delete it (soft); the managed list, paged by state, carries each closure's extension state, and its summary answers the tabs' counts and the closures awaiting an extension; a space's public page carries its running and upcoming announcements; a check-in during a running closure succeeds with the warning `CLOSURE_IN_FORCE`.

No `0_CARRIED_FROM_*` file: nothing carried into this PR.

## Scope / Acceptance criteria / Out of scope

**Scope**
1. Migration `announcement_key`: `announcements.request_id` (UUID, required, backfilled), unique within the space.
2. `@masaha/shared/announcements` (new, L2); `@masaha/shared/directory` gains `PublicAnnouncement` on `PublicSpace`; `DESK_WARNINGS` gains `CLOSURE_IN_FORCE`.
3. `POST /manage/spaces/:spaceId/announcements` (🧾, `Idempotency-Key`), `PATCH …/announcements/:announcementId`, `POST …/:announcementId/end`, `POST …/:announcementId/start`, `DELETE …/:announcementId` (🧾).
4. `GET …/announcements?state=&page=&limit=` (🧾, paged, each closure with its extension state) and `GET …/announcements/summary` (🧾), composed by `subscriptions` (`subscriptions/closures/`).
5. `GET /spaces/:slug` carries `announcements`.
6. `occupancy.checkInWarnings` adds `CLOSURE_IN_FORCE` (both check-ins read it).
7. Error codes `ANNOUNCEMENT_NOT_STARTED` (409) and the warning `CLOSURE_IN_FORCE`.
8. `docs/features/announcements.md` (new).

**Acceptance criteria**
- [x] The owner and reception post an announcement: a type, Arabic text (required), English text (optional), a start (now when absent) and an optional end; audited; a retry with the same key answers the first, 201, never a second; two at once with one key make one. *(T1, T2)*
- [x] The period is checked: an end after the start, a new end after now, a start at most 30 days back and 365 days ahead, an end at most 365 days after the start; each refusal 422 on its field, writing nothing. *(U2, U4, T4)*
- [x] An edit changes only what it sends (`textEn: null` clears, `endsAt: null` removes the end), audited with before and after; the same values write nothing. *(U3, T7)*
- [x] End now sets the end to now on a running one; an ended one answers as it is; an upcoming one is refused 409 `ANNOUNCEMENT_NOT_STARTED`. Start now sets the start to now on an upcoming one; a started one answers as it is. Delete is soft, 204, a repeat 204 writing nothing; a deleted announcement leaves every read and the live status. *(T8–T11)*
- [x] The managed list pages one state (running and upcoming by start, ended by end, latest first), the total right; every closure carries `extension` (`null` until applied); the summary counts the three states and the closures started within the last 30 days with no extension (the owner's Q6). *(T12–T14)*
- [x] A stranger, another space's owner and the admin get `not_found` on every route; a link ended while a write waits on the space's lock is refused 403. *(T5, T6, T15)*
- [x] `GET /spaces/:slug` carries the running and upcoming announcements, never an ended or deleted one, ordered by start then id, at most 20, each with its start and end. *(T16, T17)*
- [x] A visit's check-in during a running closure succeeds 201 with `CLOSURE_IN_FORCE` in `meta.warnings`, after `SPACE_FULL` and `OUTSIDE_OPENING_HOURS`; the subscription check-in reads the same warnings. *(T18, a subscriber's check-in included)*

**Out of scope:** the screens (18 Announcements, the space page's announcements) — worker A's later items; the owner's overview (step 12, it will read `closures.summary`); notifications of any kind; the closure extension itself and its guard (PR 4); data reports (PR 2); favourites (PR 3); a title or an author on an announcement (O9). Nothing of the overview's *Not in v1*.

## Change type

feat — API code, the shared contract, tests and documents; a migration (announcements' key); the new codes' catalogue lines in `apps/web` and one line of the `PublicSpace` test fixture (`apps/web/src/test/publicSpace.ts` gains `announcements: []`), worker B's licence for a shared type change.

## New error codes (the Arabic needs the owner's approval)

| Code | Answer | English | Arabic |
|---|---|---|---|
| `ANNOUNCEMENT_NOT_STARTED` | 409 | This announcement has not started yet. | لم يبدأ هذا الإعلان بعد. |
| `CLOSURE_IN_FORCE` | warning | The space is announced closed now; the check-in was recorded anyway. | المساحة معلَنة مغلقة الآن، وسُجّل الحضور رغم ذلك. |

Both as approved in the plan's Q1 (2026-10-21).

## Evidence

- Each commit: `npm run lint` and `npm run typecheck` exit 0, and the test files it touches in their lanes.
- On the head, once: `npm run lint` exit 0 · `npm run typecheck` exit 0 · `npm run test:unit` exit 0 (shared 253, api 864, web 918 tests) · `npm run test:api` exit 0 (`Test Files 82 passed (82)  Tests 1131 passed (1131)`) · `npm run format:check` exit 0 · `npm run check:links` exit 0 (2673 links) · `npm run build -w @masaha/shared` exit 0. One test fix after the lanes (B18, below) re-ran its file, lint and typecheck.
- Seen failing first: U1–U3 and U4 (`Cannot find module` before their code); T1–T7 with the router unmounted (8 of 9 red); T8–T10 (3 red); T12–T15 (4 red); T16–T17 and the whole-page test (3 red); T18 (no `meta`).
- Deliberate breaks, each red then restored from its backup (SHA-256 the same) and green: B1–B5 (unit), B6 (database: the key's unique index dropped on the test database, restored), B7 audit removed, B8 `findByKey` skipped, B9 the space's lock removed, B10 `requireIdempotencyKey` removed, B11 `can()` on links read outside the lock, B12 / B21 a router mounted outside the managed boundary, B13 the no-change branch removed, B14 the upcoming check removed, B15 the started branch removed, B16 a hard delete, B17 `lockIn` without the space, B18 the ended tab by start (green first: the test's own data could not tell the two orders apart; fixed and folded into its commit, then red), B19 the count from the days, B20 an upcoming closure counted as awaiting, B22 the public end filter dropped, B23 the 20 cap removed, B24 any running announcement warning.
- Real run on 3321 (`masaha_b_dev`, the demo space), all pass: a closure posted by reception 201 `RUNNING`, its key again the same id; the list with `extension: null`; the public page with it; the public live status `CLOSED`; a visit's check-in 201 with `CLOSURE_IN_FORCE`, then its check-out with its quote's charge paid; the edit 200; end 200 `ENDED`, gone from the page, the live status reopened; an upcoming general one 201 `UPCOMING`, started 200 `RUNNING`, deleted 204 twice; the summary 200; the directory owner 404 on the demo space.
- Not run locally (CI judges): `test:component`, the web's `build`, `check:build`, `check:classes` — catalogue strings and one typed fixture line.

**Open PRs:** worker A's #111 (`feat/home-about`) shares three documents with this PR (`docs/README.md`, `docs/features/directory.md`, `docs/project/overview.md`) and no code or fixture file; `git merge-tree` of the two heads is clean, so either may merge first.

## Screenshots

None: API and documents only.

## Definition of Done checklist

- [x] Acceptance criteria met, scope kept.
- [x] Lint and typecheck clean; `packages/shared` builds.
- [x] Tests added in the owning lanes, each seen failing.
- [x] No hardcoded user-facing text (codes only; both catalogues).
- [x] Authorization on the server (`requireAuth`, the boundary, `requireCan`, `can()` under the lock).
- [x] Triggered documentation updated in this PR.
- [x] One home per fact; nothing claimed that is not built.
- [x] Every claim names its test or command.
- [x] Atomic history, pushed.
