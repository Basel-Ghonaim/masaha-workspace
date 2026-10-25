## Summary
The owner voids a payment with a reason (idempotent, audited; a written-off visit's payment once the write-off is undone); the payments list: the owner's ledger by Gaza days, staff, method, kind and void, with its totals; reception's own payments of today. A priced visit closed by hand with no customer that owes after a void is uncollected.

### Carried from #112
- start now holds the 365-day bound (`start()`, its test red first) — `fix(announcements): hold the period on start now`;
- conventions §9's announcements bullet moved; `announcements.md` states the public read; the contract's "will read" and the retry-after-delete line; `#112` last in `desk.md` and `subscriptions.md` — `docs(announcements): state the public read`.

## Scope
1. Carried from #112 (items 1–6).
2. Migration `payment_void_guard`: `payments_guard_change` replaced, the void of a written-off visit's payment refused (`payments_visit_written_off`, already translated to `VISIT_WRITTEN_OFF`).
3. `@masaha/shared/payments`: `voidPaymentSchema`, `paymentsQuerySchema` and their constants; `PaymentRow`, `PaymentItem`, `PaymentTotals`, `PaymentsMeta`.
4. `POST /manage/spaces/:spaceId/payments/:paymentId/void` (🏢, `requireCan('payments.void')`), in `desk`.
5. `GET /manage/spaces/:spaceId/payments` (🧾; the owner's whole ledger, reception's own today), in `payments`.
6. The uncollected visits include a priced visit closed by hand with no customer that owes after a void.
7. `subscriptions.namesOf`; `payments` gains `users`, `customers`, `subscriptions` (and the clock) as dependencies.
8. Documents: api-contract, data-model, conventions, security, `features/{payments,desk,subscriptions,announcements,visits,customers,users}.md`, v1-mvp, overview, the docs map.

## Acceptance criteria
- [x] Start now on an upcoming announcement whose end would fall more than 365 days after now is 422 `endsAt: out_of_range`, writing nothing; the carried documents say what `0_CARRIED_FROM_112.md` says.
- [x] The owner voids a payment with a reason (1–200 characters, required): 200 with the payment as the list shows it, its void at now, by the owner, with the reason; audited `payment.voided`; the payment counts nowhere from then on.
- [x] A second void answers the voided payment as it is, its first reason and voider kept, writing nothing; two at once void it once.
- [x] Reception is 403 before the body is read; a stranger, another space's owner and the admin are 404; another space's payment, or an unknown id, is 404; an owner whose link ended while the void waited is 403.
- [x] A written-off visit's payment is refused 409 `VISIT_WRITTEN_OFF`, by the database; once the write-off is undone it is voided.
- [x] Voiding one payment changes no other row.
- [x] A visit paid in full at a manual check-out with no customer, its payment voided, is listed in the uncollected visits with what it owes; an open visit never is; one closed by hand unpriced is not.
- [x] The owner's list: a range of Gaza days (both included, at most 92 days; neither → today), `recordedById`, `method`, `kind`, `voided`; newest received first, then id; paged; each row names the item, its customer, who recorded it and the void; `meta.totals` over the whole filter but `voided` and the page.
- [x] Reception's list is its own payments of today (Gaza), voided ones listed and marked, totals its own; `from`, `to` or `recordedById` from reception is 403; another space's payments are never listed.

## Out of scope
Screen 17 (worker A's later item) and its CSV export; income, collections and debtors by period (step 11); the owner's overview (step 12); DESK_SCREENS' API specs; a refund, a transfer of credit, an edit, a delete or an undo of a void (ADR 0010); an idempotency key on the void (ADR 0015 rule 2).

## Change type
feat — API code, the shared contract, tests and documents; a migration (the payments' change trigger replaced: a written-off visit's payment is voided once the write-off is undone). No new error code; `VISIT_WRITTEN_OFF`'s two catalogue lines reworded to cover a void (the Arabic, as approved: «سُجّلت هذه الزيارة «لن يُحصَّل»؛ يتراجع المالك عن ذلك أولًا قبل استلام أي دفعة لها أو إلغاء إحدى دفعاتها.»).

## Evidence
- `lint` and `typecheck` exit 0 at each commit; `test:unit` exit 0 (shared 255, api 865, web 918 tests); the API lane (`vitest run --project api`) exit 0, `Test Files 84 passed (84)`, `Tests 1156 passed (1156)`; `format:check`, `check:links`, `build -w @masaha/shared` exit 0.
- Seen failing first: T0 (`expected 200 to be 422`); U1 (the void's and the query's schemas held back); U2 (the window not written); T1–T13 (the void's route held back: 12 failed); T15 (`expected [] to deeply equal [ { … } ]`); T16–T23 (the list's route held back: 8 failed); D1 through B4.
- Deliberate breaks, each red then restored: B1–B15, BQ1 (the priced-only clause), B16b (B16 alone cannot change the outcome: an open visit has no charge and no checkout method), B17–B24, B4 on `masaha_b_test` for D1 and T7.
- Real run on 3321 (the demo data reseeded): 19 cases, `ALL PASS` — the ledger's totals 47,500 / cash 37,500 / transfer 10,000 / voided 1 of 20,000; reception's own today; the 403s and 404s; a second void keeping the first reason; «هبة» uncollected after its void; `VISIT_WRITTEN_OFF` until the write-off is undone.
- Not run locally (CI judges): `test:component`, the web's `build`, `check:build`, `check:classes` — the web change is one catalogue line per language.

## Screenshots
None: API and documents only.

## Definition of Done checklist
- [x] Acceptance criteria met, scope kept.
- [x] Lint and typecheck clean; `packages/shared` builds.
- [x] Tests added in the owning lanes, each seen failing.
- [x] No hardcoded user-facing text (codes only).
- [x] Authorization on the server (the boundary, `requireCan('payments.void')`, `can()` under the lock, the list's narrowing).
- [x] Triggered documentation updated in this PR.
- [x] One home per fact; nothing claimed that is not built.
- [x] Every claim names its test or command.
- [x] Atomic history, pushed.
