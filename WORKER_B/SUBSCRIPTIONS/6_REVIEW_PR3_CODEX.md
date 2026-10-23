# Review — SUBSCRIPTIONS PR 3 (#109)

**Head reviewed:** `e262298eb5efdd47ebb82fefc182080b507db0a2`  
**CI:** all listed checks passed: build, check:classes, check:links, format:check, lint, test:api, test:component, test:unit, typecheck, and CodeRabbit (pass; “Review rate limited”).  
**Head movement:** no movement; the final PR head is still `e262298eb5efdd47ebb82fefc182080b507db0a2`.

## Verdict

**Mergeable.**

## Five most important findings

None. I found no verified code defect requiring a finding or fix.

## Rest

None.

## Executor departures, judged

1. **Carried item 5’s test was green before its code:** acceptable. The commit replaces a second TypeScript minutes calculation with SQL’s `subscription_usage` expression. The PR code uses `STAY_MINUTES` in `subscriptions.repository.ts`; I did not independently run the reported mutation/break.
2. **C1’s T2 was green before the refactor:** acceptable for the same reason. I saw `occupancy/present.ts` centralize `presentIn`, `presentCountsIn`, and `isPresent`, with the occupancy read, warning, directory, archive, and customer file calling the shared service. The report’s B4 break result is report-only.
3. **A check-in key reused for another subscription returns 409:** acceptable and consistent with the carried idempotency rule. In `desk.service.ts`, the key lookup is under the space lock and a mismatched subscription is rejected before returning a retry.
4. **`DeskCheckIn` lives in shared subscriptions; `contactsOf` and app wiring were added:** acceptable interface placement. The list is owned by the subscriptions router and the list answers include customer and subscription state. I saw the wiring and code; I did not independently run its tests.
5. **C2’s API red was captured with the route unmounted:** evidence departure only; the code review found no implementation defect from this. The report says the corrected API tests passed; that evidence is report-only.
6. **The demo did not contain the planned already-present subscriber; a substitute exercised the refusal, and the expired demo subscription warned as expired:** acceptable under the owner’s recorded acceptance in the executor report. This real-run account is report-only; I did not access or alter demo data.
7. **No “outside its shift” warning:** correct to the approved plan. D11 defines only the space-full and opening-hours warnings, followed by four subscription warnings; the executor’s prompt’s shift wording is not part of the approved D11 contract.
8. **C1 also routed archive and customer-file presence reads through occupancy:** consistent with D12’s requirement that no other *present* count remain.
9. **No migration:** correct; the plan specifies none.

## Checked and fine

- **Authorization and scope:** the manage-space boundary applies authentication and space access to all three routes. Writes require `attendance.record`; check-in and check-out recheck permission under the space lock. The check-in subscription and customer are looked up within the requested space; check-out locks a check-in only when it belongs to that space. The check-in list uses the existing staff space boundary, as the approved plan specifies.
- **Transactions, retries, and races:** check-in reads the key after taking the space lock; the same-key retry returns its row, while a mismatched subscription conflicts. A new check-in locks the subscription, checks archived/present state, computes warnings, then inserts and audits in the same transaction. The database’s one-open-check-in constraint remains the backstop. Check-out takes the space lock and then the space-scoped check-in row lock; a closed row is returned unchanged.
- **Warnings and dates:** code order is space fullness, opening hours, not started, expired, days-per-week, hours-per-day. These are warnings and do not block a successful check-in. The day and minutes accounting use Gaza-day SQL expressions and the shared usage calculation.
- **Occupancy:** staff reads, check-in warnings/refusal, and directory counts consume the occupancy helper; visits and subscription check-ins both contribute.
- **Lists:** the query schema requires either `open=true` or both date bounds, rejects mixed modes and ranges beyond the 92-day difference; SQL scopes reads to one space and dates by Gaza day. Open results are unpaged and dated results are paged and bounded.
- **Documents and scope:** reviewed the changed API contract, data model, conventions, security, feature docs, findings, v1-mvp, and overview against the code. The diff has 47 files, only the two allowed web error catalogues, no migration or package manifest changes, and no remaining `#PRNUM`. Commit subjects are within 50 characters and each has a body.
- **Executor-only evidence:** the red/green test runs, mutation breaks, local full-lane runs, database constraint check, real run, push, and conflict check are claims in `4_REPORT_PR3.md`; I did not rerun them. CI status above and the reviewed commit content were observed independently.
