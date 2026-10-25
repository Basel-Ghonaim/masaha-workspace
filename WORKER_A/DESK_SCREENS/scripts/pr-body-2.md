## Summary

DESK_SCREENS PR 2, the desk's subscribers (screen 13), on the desk #116 and #117 built: **the desk's one search**, a
**subscriber's check-in and check-out**, and **«استلام دفعة»**, a payment on one of a customer's items.

- **The one search** (K1), above the page, focused on arrival from 768 px only (S10): once typing pauses (400 ms),
  «حاضر الآن» — the people present whose name, or whose phone's last two digits or more, answer it, with their
  «خروج» (`occupancy`'s group, from the same state now) — then «زبائن», the first six customers the customers
  list's search finds, a card each (phone, current subscription with its status and end, one balance badge, DI-40),
  then «تسجيل زيارة باسم «X»», the primary only when nothing matched (DI-20), with the no-match line that promises
  no record (DI-36). Groups `h2`, cards `h3` (DI-38); the count said politely; a failed search says so with a retry.
- **«حضور»**: on a subscription that runs, one tap, one key until it lands; on none, an expired or a not-started one —
  what the row already says — a choice first: «تسجيل كزيارة» (a visit by their name, not added to their file:
  finding 160) or «تسجيل على أي حال» (DI-14, S6). The server's warnings are said after; `MEMBER_ALREADY_CHECKED_IN`
  says they are here. A coming subscription's start is read from the customer's file.
- **A subscriber's «خروج»**: one tap, no key (S3), in the present list and the search's group; the toast says the stay
  and what the subscription still owes, with «استلام». The button keeps the focus so the list hands it on (DI-31).
  The open check-ins give the search the phones and the present list each subscriber's first progress line.
- **«استلام دفعة»** (top bar from 768 px, the «⋯» below; a card's «استلام {المبلغ}»; the check-out toast's
  «استلام»): the debtors, present first (DI-21); the customer's open items, one payment per item (DI-22); the amount
  follows the item only while untouched (DI-35); a usage-based subscription takes more as credit; one key per opening.
- After a check-in or a check-out started from the search, it is cleared and takes the focus (S10).

## Carried from #117

- `fix(desk): show the last uncollected page in range` — the uncollected card's page kept in range with
  `usePageInRange` (the last page in place of one past it, the address replaced); the card reads empty only when the
  list's total is 0 (#117's review, F1). Its test seen red first; its break (`usePageInRange` removed) red.

## Scope

- `features/occupancy`: `matchesPerson`, `usePresentMatches`, `PresentMatches`; `PresentList`'s usage slot.
- `features/desk`: the repository (the customers search, a subscriber's check-in and check-out, the open check-ins, a
  customer's file); the search and the card; a subscriber's check-in with its choice and check-out; the open
  check-ins' phones and progress; «استلام دفعة»; `balanceView`, `statusView`, `dayText`, `progressLines`, `openItems`;
  the toasts.
- `pages/dashboard/space/desk/DeskPage.tsx`: the search above the page; «استلام دفعة»; one payment dialog for every
  entry.
- Copy: `occupancy.present.matches`; `desk.search`, `desk.customer`, `desk.subscriber`, `desk.pay`, both languages.
- Docs: `desk.md` (behaviour, decisions, code map, history), `occupancy.md`, `customers.md`, `subscriptions.md`,
  `payments.md`; finding 160 (new).

## Acceptance criteria

- [x] The desk's search (from 768 px it takes the focus on arrival) finds the people present by name or a phone's
  last digits first, with «خروج»; then customers (server search), each a card with «حضور», «استلام {المبلغ}» when
  they owe; then «تسجيل زيارة باسم «X»» (primary when nothing matches) — never two equal buttons (DI-20).
- [x] «حضور» checks the customer in on their current subscription in one tap; with none, or an expired or not
  started one, a dialog first offers «تسجيل كزيارة» and «تسجيل على أي حال» (DI-14); the server's warnings after are
  said; `MEMBER_ALREADY_CHECKED_IN` says they are here.
- [x] A subscriber's «خروج» is one tap; the toast names the stay and what the subscription owes, with «استلام»
  opening the payment on it.
- [x] «استلام» pays one item: the customer's unpaid visits and owing subscriptions, the chosen one preset; the picker
  lists the present debtors first (DI-21).
- [x] After a check-in or check-out started from the search, the search is cleared and takes the focus.
- [x] Lint, typecheck, `test:unit`, the scoped `test:component`, the production build, `check:build`,
  `check:classes`, `format:check`, `check:links`, `check:conflicts`; CI green; `CLEAN`.

## Out of scope

The card's «⋯» and the name's link to the file, the customers list and a customer's file (PR 3); the subscription
sheet and «زبون جديد» (PR 4). Step 9's payments list and void. A visit's check-in naming its customer (finding 160).
No `apps/api`, `packages/shared`, schema, migration, seed or dependency change.

## Change type

Feature (web) · fix (web, carried) · docs.

## Evidence

Run locally on the head (before a last alignment fix, which re-ran the tests it touches, lint and typecheck):
- `npm run lint` · `npm run typecheck` — exit 0.
- `npm run test:unit -w @masaha/web` — `Test Files 132 passed (132)`, `Tests 967 passed (967)`.
- `npm run test:component -w @masaha/web -- src/features/desk src/features/occupancy src/pages/dashboard
  src/shared/copy src/shared/lists` — 163 of 164 passed; the one miss is `routes.component.test.tsx` › "lists
  reception’s four pages…" at 3 031 ms (finding 87's family), and that file alone passed 49 of 49.
- The production build · `npm run check:build` (no dashboard code, data table or Leaflet in the site's first
  download: 1,036,538 B) · `check:classes` · `format:check` · `check:links` · `check:conflicts`.
- Each new test seen red before its code; the plan's breaks for the key, money, state, warning and width guards made,
  each red, each restored.
- The real run in local headless Chrome, as the owner and as reception, Arabic light and English dark at 390, 768
  and 1440: the search asks the server once typing pauses (one request for four letters); «سارة»'s check-in through
  the choice, first sent offline then retried (four requests, one key, one check-in, the expiry warning after);
  her one-tap check-out (no key) and «استلام» 5 ₪ from its toast, first sent offline (four requests, one key, one
  payment); «يوسف» in and out; «رامي»'s visit paid from «استلام دفعة»; touch targets 44 px at 390. Not shown live:
  the present debtors first (no debtor was present; test 53 proves it) and the carried fix (one page of uncollected
  visits; its test proves it).

Not run locally — CI judges: the full `test:component`, `test:unit` of `apps/api` and `packages/shared`, `test:api`
(no API change).

## Screenshots

Attached by the owner.
