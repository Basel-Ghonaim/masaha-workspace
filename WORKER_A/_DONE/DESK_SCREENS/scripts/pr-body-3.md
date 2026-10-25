## Summary

DESK_SCREENS PR 3, Customers and Customer details (screens 14–15), on the desk #116, #117 and #119 built, over
DESK_API (#118): **«الزبائن»**, the space's customers list; **«ملف الزبون»**, a customer's file; **edit, archive and
restore** a customer; a subscription's **statement** and its **end**; and the sign-in page saying a session ended
**for idleness**.

- **«الزبائن»** (S11): 20 a page from `GET …/customers`, the search once typing pauses, the status chips («مؤرشف» the
  owner's only), the kind and the payment — every filter and the page in the address, read by the contract's own rules
  (a value the server would refuse falls back), a change replacing it and returning to page 1. Five columns from 768 px
  (the name a link to the file, with the phone under it; the subscription and its end; its status; the balance badge,
  DI-40; the actions), a card per customer below, where the kind and the payment move into a sheet with their count
  (P5). Its states: loading, failed with its reference and a retry, failed again over the rows, empty, no match, no
  archived customer; busy while another page loads.
- **«ملف الزبون»** (`…/customers/:customerId`, both roles): titled by the customer's name once it loads, under
  «الزبائن» › the name. The header (phone, «حاضر الآن», the current subscription's status, the balance badge,
  «مؤرشف», the «⋯»); «زيارات غير مدفوعة» as «غير محصّل» draws its rows, «تحصيل» opening the payment on one (DI-24);
  «الاشتراكات», a card each under one heading (DI-42): its dates, terms, status and payment badges, progress, and the
  server's due, paid and left, with «استلام المتبقي» while it owes (DI-44). No tabs (DI-43).
- **Edit, archive, restore** (DK-014, P9): each customer's «⋯», named by them (DI-39) — on a list row, a desk search
  card and the file's header — holds «ملف الزبون», «تعديل البيانات» and the owner's «أرشفة…», destructive (DI-46). The
  edit sends **only the fields that differ** from the customer as loaded (a cleared phone as `null`), nothing when none
  does, with **no key, never re-sent by itself** (S3; finding 123 resolved). A settled customer is archived at once with
  «تراجع»; one who owes is asked first in an `AlertDialog` naming the debt; a present one is refused with its line
  (DI-47); an archived one offers the owner «استرجاع».
- **The statement** opens in its card with «عرض الكشف», read only then: check-ins on Gaza's clock («حاضر الآن» while
  open, an auto check-out marked) and payments, the amount with its method under it, a voided one struck through with
  «ملغاة» and its reason. **«إنهاء الاشتراك»** asks first, naming the end it takes and the end it had; no key, sent once.
- **The idle line** (spec C, #118): a refresh refused 401 `SESSION_IDLE` ends the session as ended for idleness
  (`endedBy`), and the sign-in page says the error's line above its form until the next sign-in.

## Carried from #119

- `fix(desk): say when a customer's file fails` — a not-started subscription's choice reads its start from the file;
  a failed read now says so with a retry instead of a loading line for ever (#119's review, F1).
- `fix(desk): clear the search after a named visit` — «تسجيل زيارة باسم «X»» now clears the search and gives it the
  focus once the check-in lands; a failed one keeps the term (#119's review, F2).

Each test seen red before its code; each break (the failure branch removed; the callback not called) red.

## Size — a one-off exception

**81 files** (51 code, 21 tests, 9 documents), past the 72-file bound: the owner granted this PR as a one-off
exception (as #116's 90 files) rather than a split.

## Scope

- `features/desk`: the repository (edit, archive, restore, the statement, the end); the customers list and its
  filters (`customersQueryOf`); the file (`useCustomerFile`, `useFileTitle`, `termsLine`, `payStatus`); the «⋯»
  (`CustomerMenu`, `CustomerActions`), the edit, archive and end dialogs; the statement; the search's card and the
  search gain the «⋯».
- `pages/dashboard`: `CustomersPage`, `CustomerPage` and its route `customers/:customerId` (`SPACE_CUSTOMER_PATH`);
  `DeskPage` passes the cards' «⋯».
- `shared/session`: `endedBy` (`useSessionEnd`, `getSessionEnd`); `pages/site/auth/SignInPage.tsx`: its line.
- Copy: `desk.customers`, `desk.file`, `desk.edit`, `desk.archive`, `desk.customer.menu`, `desk.statement`,
  `desk.end`, `desk.subscriber.pre.startFailed`, both languages.
- Docs: `desk.md`, `customers.md`, `subscriptions.md`, `auth.md`, `architecture.md` (§2, §4); findings 123 resolved,
  162 and 163 new.

## Acceptance criteria

- [x] «الزبائن» lists the space's customers 20 a page (search, status chips, kind, payment; `ARCHIVED` for the owner
  only), every filter and the page in the URL; five columns from 768 px, cards below.
- [x] A customer's file shows the header (phone, here now, status, balance from one component), the actions by state,
  the unpaid visits with «تحصيل», each subscription's card (dates, terms, progress, due/paid/left) with «عرض الكشف»
  opening its statement, «استلام المتبقي» and «إنهاء الاشتراك».
- [x] Edit sends only what changed and is never retried by itself (finding 123); archive and restore are the owner's
  (at once with «تراجع», or an `AlertDialog` naming the debt); a present customer's archive says so.
- [x] A reception session ended for idleness lands on sign-in with its line (spec C).
- [x] Lint, typecheck, `test:unit`, the scoped `test:component`, the production build, `check:build`,
  `check:classes`, `format:check`, `check:links`, `check:conflicts`; CI green; `CLEAN`.

## Out of scope

The subscription sheet and «زبون جديد» (PR 4). Step 9's void and payments list; who recorded or voided a payment
(finding 162); a subscription's corrections (finding 163); the attendance log tab (finding 161); the WhatsApp reminder.
No `apps/api`, `packages/shared`, schema, migration, seed or dependency change.

## Change type

Feature (web) · fix (web, carried) · docs.

## Evidence

Run locally on the head:
- `npm run lint` · `npm run typecheck` — exit 0.
- `npm run test:unit -w @masaha/web` — `Test Files 135 passed (135)`, `Tests 978 passed (978)`.
- `npm run test:component -w @masaha/web -- src/features/desk src/features/occupancy src/pages/dashboard
  src/pages/site/auth src/shared/session src/shared/copy src/shared/lists` — 238 of 239 passed; the one miss is
  `changePasswordPage.component.test.tsx` › "lands the user on the page they asked for…" at 3 472 ms (the `/spaces` page
  not loaded yet; a file this PR does not touch), which passed alone (4 of 4) and in its folder (26 of 26).
- The production build · `npm run check:build` (no dashboard code, data table or Leaflet in the site's first
  download) · `check:classes` · `format:check` · `check:links` · `check:conflicts` — each exit 0.
- Each new test seen red before its code; the plan's breaks for the role, money, state, key, width and a11y guards
  made, each red, each restored (the menu's break made on its trigger's label: Radix names the menu by it).
- The real run in local headless Chrome, as the owner and as reception, Arabic light and English dark at 390, 768 and
  1440: the list, the file and its statements; the filters in the address and the sheet; «نور حسن»'s phone edited — the
  first save sent offline, not re-sent, then retried: each PATCH carries only `phone`, no key — and cleared; «زائر
  تجربة 2» archived through the debt's dialog and restored (no key); «يوسف»'s subscription ended (no key); the file's
  read blocked, then retried; a named visit from the search, the search cleared and focused; touch targets 44 px at
  390; the idle sign-out (see the report).

Not run locally — CI judges: the full `test:component`, `test:unit` of `apps/api` and `packages/shared`, `test:api`
(no API change).

## Screenshots

Attached by the owner.
