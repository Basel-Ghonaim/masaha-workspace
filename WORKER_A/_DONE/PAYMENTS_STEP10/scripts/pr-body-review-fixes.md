

## Review fixes (2026-10-27)

From the Claude review; each fix folded into the commit that made the code (no fix commit). `main` unmoved (`39ef0504`): no rebase.

- **F1 — the period's calendar took two openings.** react-day-picker 10 ends a range on its first click (`{ from: day, to: day }`), so the ledger applied a one-day range and closed. The range `Calendar` now gets `resetOnSelect`: each opening's first click starts a range and keeps the picker open, the second applies it (the earlier day first). A new test clicks through it; red without `resetOnSelect` (the picker closed after the first click), green with it. In `feat(payments): list the space's payments`.
- **F2 — the zone case could not fail where the lanes run.** The web's unit lane now runs in `America/New_York` (`test.env.TZ` on the unit project in `apps/web/vite.config.ts` — a line every unit test shares, said in the commit body), so the moved `dayText` case is real too. Break 11 (`timeZone: 'UTC'` dropped) is now red with no change of environment; so is `dayText`'s. CI's unit lane on the head judges the rest. In `feat(payments): list the space's payments`.
- **F3 — the statement's «⋯» and its focus fallback tested.** `Statement.component.test.tsx`: the owner's statement offers «⋯» on the payment not voided only, reception's none, and once a void's refetch strikes the payment the focus is on the «Payments» heading; red with the heading's `tabIndex={-1}` removed. In `feat(desk): void a payment`.
- **F4 — finding 169's wording.** "every component a page draws through the barrel"; the split between chunks (`design-system` +81,438, `jsx-runtime` +7,089, `routing` −4,809, +84,506 in all), the cause read by size only; the owner scheduled it as an item of its own before PAYMENTS_STEP10's PR 4.
- **F5 — recorded as finding 173**: the layer's range `Calendar` ends a range on its first click (its `DateRange` comment is false for react-day-picker 10); `Calendar.tsx` is not changed here.

Run for this round (the owner's rule: no full lane locally, no build checks; CI on the head judges the rest): the touched test files (the ledger's 4, the statement's 5, `periodText` and `shared/lib/time` 18), each new test seen red first; `lint`, `typecheck`, Prettier on the touched files, `check:links`.
