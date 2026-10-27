# PAYMENTS_STEP10 — PR 1 (`feat/payments`) — the executor's report

Written as the work went. Logs under `scripts\`.

## Preconditions and first checks (2026-10-27)

- `git status --short` empty in `C:\dev\masaha\app`; `git fetch origin`; `git log -1` = `39ef0504 Merge pull request #124 …` = `origin/main` (`39ef05043c9a…`).
- `gh pr view 124 --json state` → `MERGED`.
- `npm run build -w @masaha/shared` → exit 0 (`scripts\shared-build.log`).
- `npx prisma migrate status` (apps/api) → "29 migrations found … Database schema is up to date!" (`masaha_dev`). Nothing deployed.
- Docker: `docker info` exit 0; `masaha-postgres-1 Up (healthy)`.
- **Base diff** `git diff --name-status e6737da5 origin/main`: 70 lines — #124's files only (`features/desk` sheet, `features/packages` offered, `features/spaces` prices, the desk/customer pages, `SubscriptionSheetSlot`, `useSheetOpener`, `Sheet`, copy `desk.ts`, docs). No `packages/shared` change.
- **Open PRs** (`gh pr list --state open`): none. Worker B's FINANCE_AUDIT PR not open yet.
- **Finding numbers:** the highest in `docs/architecture/findings` are 164, 170, 171; 165 and 166 free.
- **5.a** `git grep -l "services/day\(Text\|Word\)" apps/web/src` → ten `features/desk` hooks (`useCustomerCard`, `useEndDialog`, `useCustomerFile`, `usePayDialog`, `useSubscriptionSheet`, `useStatement`, `useOpenCheckIns`, `useSubscriberCheckIn`, `useUncollectedCard`, `useUnpricedCard`); no importer outside `desk`.
- **5.b** the desk's customers call: `api.getPage<CustomerRow[]>(…/customers, { params: query })` — the ledger does the same. `paymentsQuerySchema` is refined (`superRefine`): its fields are read by their own schemas (`dateSchema`, `PAYMENT_METHODS`, `PAYMENT_KINDS`), the plan's fallback.
- **5.c** `deskFailure(failure, refused, { title, lost, nothing, retryLabel, retry })` and `useDeskWrite()` → `{ settle, linkEnded }` take what §9 gives them. `CustomerFile` has **no `abilities` object: it has `owner: boolean`** (the archive and restore); `SubscriptionCard` has neither. See decision D1.
- **5.d** `staffKeys.list(spaceId) = ['space', spaceId, 'staff']` (`useStaffQuery`): `useStaffPeople` reads the same query.
- **5.e** `Calendar mode="range"` takes `selected: DateRange` / `onSelect`, `lang`, `previousMonthLabel`, `nextMonthLabel`; `DatePicker` + `DatePickerTrigger` + `DatePickerContent label` (the showcase's range). `Intl.DateTimeFormat#formatRange` in Node 24: «1–21 أكتوبر 2026», "25 September – 21 October 2026", «25 ديسمبر 2025 – 3 يناير 2026» — it works; no fallback.
- **7. The data inventory** (read-only; `scripts\inventory1.mjs` → `inventory1.out.txt`; sign-ins with the password read from `.env`, never printed; no `/auth/` body kept; GETs only). The API started on 3320 and stopped by its process ids (2628, 8240, 18112); port 3320 free after.
  - `demo-owner` = user 14 «أحمد الشوا», OWNER of space 7 (`masaha-demo`); `demo-reception` = user 15 «ليلى النجار», RECEPTION of 7.
  - Space 7 today: 0 payments. 27 Sep – 27 Oct: 16 payments (15 received ₪1,065, cash ₪965, transfer ₪100; 1 voided ₪200 — payment 4, «أحمد الشوا: سُجّلت مرتين», the seed's).
  - Staff of 7: 15 «ليلى النجار» (active), 35 «موظف تجريبي» (active).
  - **The run's ₪1 targets:** subscription 1 «امتحانات بالساعة» of customer 1 «سارة خالد» (balance ₪31.60); visit 3 of customer 8 «خالد» (balance ₪15, uncollected).
  - Reception's own payments today: 0. Reception with a range → 403 `forbidden` (the server's guard).
