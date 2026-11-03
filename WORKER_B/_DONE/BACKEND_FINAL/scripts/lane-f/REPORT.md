# Lane F — report (returned as text, saved by the lead)

Lane F: DONE · SERIOUS: none · lane/f head 4bfd1054 on b0cd0ae4 (after the join: 8cd2bcfa, f7cd3a13, 2d8c0b86).

Commits: 539c15b8 feat(finance): read a space's income (36, 25 files) · ab239b41 feat(finance): read who owes and who
paid (41, 20 files) · 4bfd1054 feat(finance): read a space's occupancy (39, 15 files).

Tests: U-F1 red "TypeError: monthOf is not a function" → 7/7; U-F4, U-F2 red "Cannot find module" → green; income
(6) and access red taken with the route unmounted (the service written before its API tests) → green; debts (5),
payers (2) red unmounted (8 failed) → green; U-F3 and a daysOfMonth test red → green; occupancy (3) red unmounted → green.
Breaks (each restored by copy): B-F1 "expected '2026-13' to be '2027-01'"; B-F2 3 red; B-F3 28-days red; B-F6/B-F7
"expected 422 to be 403"; B-F7a "expected 404 to be 403"; B-F8 3 red; B-F9 4 red; B-F10 "expected [30000, 8800] …
[30000, 3800]"; B-F11, B-F12 "expected 200 to be 422"; B-F13, B-F14 2 red; B-F16 "expected null to be 'عليك {المبلغ}'";
B-F17; B-P1, B-P3 first green on debts → cases added → red; B-F4 "expected 0.7 to be 1.3"; B-F5 "expected 2.8 to be
3.7"; B-F18; B-F19 "expected 1.7 to be 1.5"; B-F20 "[0.3, 0.3, 0, 0] … [0.3, 0.5, 0.5, 0]"; B-F21 "{ all: 88 } … { all: 86 }".

EC2: unnest WITH ORDINALITY binds (ISO strings, '-infinity'/'infinity' for open ends). EC3: balancesOf unchanged. EC6:
deskVisitsOf takes tx; names in the snapshot.

Decisions: (1) all time -infinity..infinity (D9 said to: now); (2) contactsOf's archived leaked into deskCheckIns'
answer — narrowed in subscriptions.service.ts (one line); (3) payersQuerySchema .extend (merge deprecated); (4) month
bound AppError.validation({ month: ['out_of_range'] }); (5) occupancy reads separate statements in parallel; (6)
finance.md rewritten whole in C7 (C5/C6's wording differs from the final).

Heavy runs (grants, no kill): lint 0; typecheck 0; test:unit 27/269, 75/893, 157/1075; test:api 105 files / 1284 tests.

Docs: api-contract *Finance* (after Front desk (managed)); data-model Income, Collections, Occupancy statistics;
conventions §7 finance row; security bullet; finance.md new; payments.md, customers.md, subscriptions.md lines.

app.ts: finance import; `const finance = createFinanceService({ readSnapshot: createReadSnapshot(), payments, users,
customers, subscriptions, visits, spaceSettings, now: clock })` after payments; `manage.use('/finance',
createFinanceManageRouter(createFinanceController(finance)))` after the audit-log mount. gazaTime: monthOf, addMonths
appended; unit test import rewritten multi-line.

Real run: GET …/finance/income?month, …/debts?state&page&limit, …/payers?month&page&limit, …/occupancy?month; SQL
cross-checks in the hand-back (income sum, debtors archived included via subscription_usage, closed visits by Gaza day).
C16: v1-mvp finance row (four routes, no export route — the web builds the CSV), step 11 Built; overview.md Built
Finance; docs/README.md map finance.md; conventions Built gains finance.
