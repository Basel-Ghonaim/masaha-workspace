## Summary
Step 8's last API slice: a subscriber's check-in, with the limits' warnings (never a refusal), the check-out, and the open and dated lists of check-ins; *present* defined once in `occupancy` (finding 111 resolved). Step 8's API is complete; the screens are worker A's.

**Carried from #106** (its review, `0_CARRIED_FROM_106.md`), the first five commits:
1. A subscribe retry with a key that subscribed another customer is refused 409, no code, as the payment routes do (red then green).
2. `subscriptions.md`'s *Authority* names the module's own routes and the desk's.
3. A whole phone keeps its suffix match: `+970521234567` is found by `0521234567` (red then green, unit and API).
4. `CUSTOMER_HAS_DEBT` counts only items older than the subscription, in the allocation's order (red then green).
5. A statement's check-in minutes come from SQL, by `subscription_usage`'s expression (green before, as the two rules agreed; its break red).
6. The contract dates the owner's decision on the archived file 2026-10-21.
7. `payments.md` says what happens past the 49th debt, and why the cap is acceptable.
8. Findings 124 (a statement's sums and its payments read in different snapshots) and 125 (the allocation's order not exposed).

## Scope
1. `occupancy/present.ts`: *present* defined once (`presentIn`, `presentCountsIn`, `isPresent`), used by the staff's read, the check-in's warnings, the directory, and the desk's archive and file.
2. `POST …/check-ins` (🧾, `Idempotency-Key`) and `POST …/check-ins/:checkInId/check-out` (🧾), in `desk`.
3. `GET …/check-ins?open=true` (whole) and `GET …/check-ins?from=&to=` (paged), in `subscriptions`.
4. Warnings `SUBSCRIPTION_NOT_STARTED`, `SUBSCRIPTION_EXPIRED`, `DAYS_PER_WEEK_USED`, `HOURS_PER_DAY_USED`; `MEMBER_ALREADY_CHECKED_IN` and `CUSTOMER_ARCHIVED` refuse.
5. Finding 111 resolved.

## Acceptance criteria
- [x] A check-in names a subscription of the space; its customer must not be archived (`CUSTOMER_ARCHIVED`) nor present by a check-in or a visit (`MEMBER_ALREADY_CHECKED_IN`); it warns, never refuses: `SPACE_FULL`, `OUTSIDE_OPENING_HOURS`, `SUBSCRIPTION_NOT_STARTED`, `SUBSCRIPTION_EXPIRED`, `DAYS_PER_WEEK_USED`, `HOURS_PER_DAY_USED`, in that order; one transaction under the space's lock; a retry answers the same check-in, 201.
- [x] Check-out closes it now, `MANUAL`, audited, and answers the subscription's due, paid and balance; a check-out of a closed check-in answers it as it is.
- [x] The open list is whole; the dated list pages a Gaza date range, latest first.
- [x] *Present* has one definition in `occupancy`, used by the staff's read, the check-in warnings (visit and subscription) and the directory.

## Out of scope
The screens (14, 15, 16, the desk's subscriber parts); a payment inside the check-out (the desk calls `POST …/payments` after it); «تسجيل كزيارة» (DK-020); voids, collections and finance (steps 9 and 11).

## Change type
feat — API code, the shared contract, tests and documents; no migration; the new codes' catalogue lines in apps/web (worker B's licence).

## New error codes (the Arabic needs the owner's approval)
| Code | Answer | English | Arabic |
|---|---|---|---|
| `SUBSCRIPTION_NOT_STARTED` | warning | The subscription has not started yet; the check-in was recorded anyway. | لم يبدأ الاشتراك بعد، وسُجّل الحضور رغم ذلك. |
| `SUBSCRIPTION_EXPIRED` | warning | The subscription has expired; the check-in was recorded anyway. | انتهى الاشتراك، وسُجّل الحضور رغم ذلك. |
| `DAYS_PER_WEEK_USED` | warning | This week's days are used up; the check-in was recorded anyway. | استنفد أيامه هذا الأسبوع، وسُجّل الحضور رغم ذلك. |
| `HOURS_PER_DAY_USED` | warning | Today's hours are used up; the check-in was recorded anyway. | استنفد ساعاته اليوم، وسُجّل الحضور رغم ذلك. |

## Departures from the plan
- A check-in key that checked in **another subscription** is 409 `conflict`, no code (carried item 1's rule, applied to the new create); break B7k.
- The desk's archive and the customer's file also read *present* through `occupancy` (D12: "no other count of *present* remains").
- `DeskCheckIn` lives in `@masaha/shared/subscriptions` (L3), since the lists are `subscriptions`'; `customers` gains `contactsOf` for them.
- Seen green before their code, each proved by its break instead: carried item 5's test (I5) and the *present* refactor's T2 (B4).

## Evidence
- `lint`, `typecheck` (each commit, `rebase -x`), `build -w @masaha/shared`, `test:unit` (shared 249, web 857, api 917 tests passed), `test:api` (79 files, 1107 tests passed), `format:check`, `check:links` (2626 links): all exit 0 on the head before the PR number.
- Seen failing first: carried 1 `expected 201 to be 409`; carried 3 (unit ×; API `expected [ 'Dana' ] to deeply equal [ 'Dana', 'Huda' ]`); carried 4 `expected { warnings: [ 'CUSTOMER_HAS_DEBT' ] } to be undefined`; U1 `Cannot find module './limits.ts'`; the check-in API file with the route not mounted, 9 of 9 failed; T12–T14 and T15–T17 `expected 404 to be 200`; U2 `Cannot read properties of undefined (reading 'parse')`.
- Deliberate breaks, each red then restored (sha256 same): I5, B1, B1h, B2, B3, B4, B5, B6, B7, B7k, B8, B9, B10, B11, B12, B13, B14, B15, B16, B17, B18.
- §12.2: only `present.ts` reads the two sources in `occupancy`; the level rule passes; the partial unique index refuses a second open check-in (`check_ins_customer_id_key`).
- Real run on 3321: a subscriber checked in 201 (the demo subscription has expired: `SUBSCRIPTION_EXPIRED`; its week held 0 days, so no `DAYS_PER_WEEK_USED`), the same key 201 with the same check-in and warnings, the occupancy counting them, the open list, the check-out 200 with paid and balance, a second check-out answered as it is, the last week's list. The plan's "present سارة → 409" could not be shown: nobody is present in the demo data, because the auto check-out closed her stay. The same refusal was shown on the run's own check-in instead (another key → 409 `MEMBER_ALREADY_CHECKED_IN`), which the owner accepted.
- Not run locally: `test:component`, the web's `build`, `check:build`, `check:classes` — two catalogues of strings; CI runs them.

## Screenshots
None: API and documents only.

## Definition of Done checklist
- [x] Acceptance criteria met, scope kept.
- [x] Lint and typecheck clean; `packages/shared` builds.
- [x] Tests added in the owning lanes, each seen failing, but two, named in Evidence with their breaks.
- [x] No hardcoded user-facing text (codes only; both catalogues).
- [x] Authorization on the server (the boundary, `requireCan`, `can()` under the space's lock).
- [x] Triggered documentation updated in this PR.
- [x] One home per fact; nothing claimed that is not built.
- [x] Every claim names its test or command.
- [x] Atomic history, pushed.
