## Summary

Build map step 9 on the web (screen 17), PAYMENTS_STEP10 PR 1: the owner's «الدفعات» ledger with its filters in the address and the server's totals, the owner's void of a payment (from the ledger and from a subscription's statement), and reception's «دفعاتي اليوم» with the handover's figures. Web and documents only; the API is #114's.

## Scope

- `shared/lib`: `dayText`, `dayWord` moved from `features/desk/services` (their second user, S7).
- `features/desk`: the owner's void — `VoidPaymentAction` (the «⋯» and its dialog), exported; a statement's payment offers it to the owner (S10).
- `features/payments` (new, dashboard-only): `PaymentsLedger` (owner) and `MyPaymentsToday` (reception).
- `features/staff`: `useStaffPeople(spaceId)`, exported (the ledger's staff filter, one cache with «الموظفون»).
- `pages/dashboard/space/payments/`: `PaymentsPage`, `MyPaymentsPage`; `routes.tsx`.
- Copy: `payments` (new), `desk.void`. Docs: `payments.md`, `desk.md`, `space-links.md`, `architecture.md` §2, `overview.md`; findings 165, 166, 169, 172 (new), 162 (evidence).

## Acceptance criteria

- [x] `/dashboard/spaces/:id/payments` (owner only): 20 a page, the latest first — day and time (Gaza), the customer (a link to their file) or the visitor, the item, the amount with its method, who recorded it; five columns from 768 px, a card each below.
- [x] Filters: the range (Gaza dates, at most 92 days, today by default), the staff member (the owner and the space's reception accounts, deactivated ones marked), the method, the kind, «إظهار الملغاة»; every filter and the page in the address; inline from 768 px, a bottom sheet below it with how many apply (the range counted); «مسح الفلاتر» resets all.
- [x] The totals line names its period and says `meta.totals` — received, cash, transfer, how many, the voided apart — never a sum of the rows.
- [x] A voided payment, when shown: struck, a visible «ملغاة», «ألغاها {name}: {reason}»; never counted as received.
- [x] The owner's «⋯» → «إلغاء الدفعة…»: a dialog naming the amount, the customer, the day and the method, the true consequence, a required reason (focused first); sent once with no key; a lost answer says a retry is safe; `VISIT_WRITTEN_OFF`, a 404 and a 403 worded; the focus back on «⋯», or once the row is gone the next row's «⋯», else the totals line.
- [x] A subscription's statement offers the owner the same «⋯» on a payment not voided; reception none.
- [x] `/dashboard/spaces/:id/my-payments` (reception only): the cash to hand over, the transfers (with «وصلت إلى حساب المساحة»), the total and the count, from the server's totals (one card below 768 px, three cards from it); its own payments of today, a voided one struck with who and why.
- [x] Lint, typecheck, `test:unit`, the scoped `test:component`, the production build, `check:build`, `check:classes`, `format:check`, `check:links`, `check:conflicts`; CI green; `CLEAN`.

## Out of scope

Any API, `packages/shared`, schema, seed, dependency or `errors.ts` change; the CSV export and collections per staff member (Finance, step 11); the overview's queue and the sidebar's counts (step 12); the grouped navigation (finding 165). Not in v1: online payment, QR check-in, in-app space claiming, booking, reviews.

## Change type

`feat` — four commits: `refactor(lib): share the day's words`, `feat(desk): void a payment`, `feat(payments): list the space's payments`, `feat(payments): show reception its payments today`.

## Evidence

Run locally on the head (outputs in the worker's report):
- `npm run lint`, `npm run typecheck` — exit 0.
- `npm run test:unit -w @masaha/web` — 143 files, 1004 tests passed.
- `npm run test:component -w @masaha/web -- src/features/payments src/features/desk src/features/staff src/shared/lib src/pages/dashboard src/shared/copy` — 54 files, 272 tests passed.
- Production build (`NODE_ENV=production`), `check:build` ("No dashboard code in the site's first download. No data-table or leaflet … in the site's first download."), `check:classes`, `format:check`, `check:links`, `check:conflicts` — all pass.
- Every new test seen red before its code; §10's breaks 2–23 each seen red, restored from a backup copy.
- Real run (local headless Chrome, `masaha-demo`, both roles, Arabic light and English dark at 390, 768 and 1440): two ₪1 payments as reception, the ledger and its filters, the void from the ledger and from a statement (each `POST …/void` sent once with no `Idempotency-Key`, `{"reason":"دفعة تجربة"}` → 200), «دفعاتي اليوم» before and after; the ledger's «⋯» 44×44 at 390 with touch; the filters' grid break at 768.

Not run locally — CI judges: the full `test:component` lane, `test:unit` of `apps/api` and `packages/shared`, `test:api` (no API or shared change).

**The first download grows by 81 KB (23 KB gzipped)**: the ledger's period is the first built use of the layer's `Calendar`, which the build places in the shared `design-system` chunk — recorded as finding 169 with the layer's `/data` entry pattern as its fix; `check:build` passes.

## Screenshots

From `PAYMENTS_STEP10\shots\pr1\` — attached by the owner.

## Definition of Done

- [x] In scope, v1 only; no API or shared change.
- [x] Tests in their lanes, each red first; breaks recorded.
- [x] Words in both catalogues; layer components and semantic tokens only.
- [x] Documents updated (capability docs, architecture §2, overview, findings).
- [x] Atomic Conventional Commits, no tool attribution.

## Decisions taken without the owner

- **The statement's void rides on `CustomerFile`'s existing `owner` flag** (no `DeskAbilities.void`, `CustomerPage` untouched): the smaller change, the same rule.
- **The «⋯» hands the focus on when it leaves under it**, and the ledger keeps the focus itself (`useFocusAfterLeave` in `PaymentsLedger`, its row slot handing a `gone` callback): the refetch that removes a voided row lands after the dialog closed.
- **The void's dialog places its first focus on the reason itself** (`onOpenAutoFocus`): the real run showed the alert dialog's own first focus on «رجوع»; the desk's write-off has the same defect, recorded as finding 172, not fixed here.
- **The calendar's cost to the first download is recorded, not fixed here** (finding 169): the fix is a layer entry of its own, beyond this PR.
- Two words beyond the plan's table (`payments.ledger.filters.close`), a row's «اليوم»/«أمس» reused from `desk.uncollected`.

