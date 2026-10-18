# Review — PR #79 (S2b-4b: the admin's space editor, hours with shifts and prices; finding 60)

Head `7782391f91285f4ab8fe199b3967dd1102b1808e` (from `gh pr view 79 --json headRefOid`; base `bfe1749d8d29507cf13d85baf0a92ceb752e3788`). Scope holds: 41 files, web and docs only, nothing in `apps/api` or `packages/shared`, no dependency change. Three commits, subjects 44 / 40 / 33 characters (all ≤ 50).

Verdict: no blockers; one should-fix below, then accept.

## Findings (most severe first)

### 1. should-fix — amounts with more than two decimals that compute to whole agorot are accepted instead of refused
- File: `apps/web/src/features/spaces/services/pricesForm.ts:53` (`return decimals <= 2 ? Math.round(shekels * 100) : shekels * 100;`).
- Scenario A: an admin types `12.500` in a price's amount and saves. `decimals` is 3, so the code returns `Number('12.500') * 100 = 1250` — an integer — and `updateSpacePricesSchema` (`amountAgorot: z.number().int()`) accepts it as ₪12.50. The plan (P4, §11) requires more than two decimals to be refused as `invalid_format`. The unit test only pins the non-integer case (`12.555`), so this passes unnoticed.
- Scenario B (same line): an admin types a thousands comma such as `1,000`. Line 47 maps the comma to `.` giving `1.000`, decimals 3, and the same path returns `100` agorot (₪1.00) instead of refusing it.
- Fix: when `decimals > 2`, return the typed text (`text`) so the schema refuses it as `invalid_format`, e.g. `return decimals <= 2 ? Math.round(shekels * 100) : text;`, and extend the `pricesForm.unit.test.ts` "more than two decimals" case with `expect(agorotOf('12.500')).toBe('12.500')`.

## Checked and fine
- Hours body: week sent Sunday-first with closed days as `null`, saved shifts keep `id`, new shifts omit it, `24:00` sent as 1440 only from an end field (`hoursForm.ts`, `clockTime.ts` `minuteOf`).
- Prices body: `''` shift and blank labels sent as `null`, amounts via `agorotOf` with Arabic digits and `,`/`٫` separators, `Math.round` at ≤ 2 decimals (`pricesForm.ts`).
- 409 shows `inUse409` and invalidates the space; 422 on `shifts.<i>.id` shows `shiftsChanged` and invalidates; 422 on `prices.<i>.shiftId` lands on the row's shift field via `shiftGone` and invalidates (`useHoursSection.ts` submit, `usePricesSection.ts` submit). 403/404/429 go through the unchanged `useSaveGroup`/`useSectionFrame` path as in PR #74.
- Copy-to-all writes open days only, disabled with reason while none is open; shift-outside-every-open-day refused on the shift (`outside`/`noneOpen`), partial fit shown as helper via `daysNotCovering`; shift used by a saved price has its Remove disabled with `inUse` beside it, read from `space.prices` (an unsaved price does not block; removal is therefore impossible in exactly the case the 409 guards).
- Shift select lists saved shifts only with `noShifts` / `hoursUnsaved` lines rendered once above the rows; dirty/discard/`filledFrom` semantics, `hoursUnsaved` plumbing, checklist links (`#hours`, `#prices`), five-item navigation order, and read-only verified rendering (Saturday-first, `dir="ltr"` ranges/amounts, `priceText` with `ar-u-nu-latn`) all match the plan.
- Finding 60: `kept` is set only when the catalogue is loaded and lacks the value, read from the admin list only then, rendered first and marked `(مخفية)`/`(hidden)`, never added to the groups; the `?? []` hardening for the empty/failed catalogue is in place.
- Finding 67: correctly recorded, not fixed — the `md:` twelve-column table is the plan's §8 layout, so no fix exists within the plan (moving the breakpoint or reflowing the row would deviate from it).
- Copy: every new key exists in both catalogues with the plan's wording; no hardcoded user-facing text in the new components; semantic tokens and logical classes only; time/amount inputs `dir="ltr"`, switches named via `openOn`, selects expose `ref` for refusal focus.
- Tests: hook files use `renderHook`, component files assert rendering only, repository file asserts paths and whole bodies; the departures in the executor's report (`ReadOnlyItem` label widening, `ar-PS` break, finding 67, real-run Sunday reset, checklist test touched in both commits, `?? []`, remove-text/placeholder, `text-label` h3) are each reasoned and owner-approved where approval was needed.
- Documents: `spaces.md` (What it does, editor bullets, decisions P1–P4/D3/D4/D6/D7/S1–S3/E/G, superseded checklist line, code map, findings, history), `lookups.md`, finding 60 resolved, finding 67 added, findings index ordering, `overview.md` Built line — all true to the code.

Trial judgment: the plan left the executor almost nothing to guess — every behavior above traces to a named section (§4–§11); the executor's departures are edge details (§16 asks honored), not gaps.

Head re-checked at the end: `7782391f91285f4ab8fe199b3967dd1102b1808e`.
