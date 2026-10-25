## Summary

DESK_SCREENS PR 4, New / renew subscription (screen 16), the last PR of the plan, on the desk, the customers list and
the file (#116–#122) and spec D (#118): **the subscription sheet** — a new customer then their subscription, a known
customer's new subscription, or a renewal — from a **published week or month price**, an offered package or
«مخصّص», over the customer's earlier debts, with the payment. And the layer's end sheet **full width on a phone**
(S12, finding 101).

- **One sheet from every entry** (DK-024): «زبون جديد» in the desk's and the customers' top bars (the desk's «⋯» at
  390), the desk search's «زبون جديد باسم «X»» / «زبون جديد بهذا الرقم» (a link beside the visit's button, never a
  second primary: DI-20), «اشتراك جديد» in every customer's «⋯» (a list row, a search card, the file's header), and
  «تجديد» on the file's latest subscription. Each opening mounts a new sheet, so its keys are that opening's.
- **The choices**, one line each (DK-007): **«منشورة للزوار»** first — the space's standard WEEK and MONTH prices,
  «أسبوعي» / «شهري» with «· للطلاب» and a shift's name — then «باقات المساحة — لا تظهر للزوار» (`packages`' offered
  ones), then **«مخصّص»** only for whoever may type a price (`visit-terms`' `mayTypePrice`, S5) with what the contract
  needs (DI-52): name, «لمن», billing, price or rate, four optional limits, the shift, an optional end and «سبب السعر».
  A package's price is never edited (DI-50); no warning icon for no limit (DI-45).
- **The money** (K3, decision 3 — finding 125 resolved): the earlier debts listed with their total and «يُطبَّق
  المستلم على المستحق من قبل أولًا، ثم على الاشتراك الجديد.»; «المستلم الآن» starts at the debts plus the new price;
  the toast lists the price the server charged, each part the answer allocated, the debt left, and
  `CUSTOMER_HAS_DEBT`'s line. A new customer's phone is required only while something stays owed; a known one with
  none gets a line, never a block (DI-53).
- **Two intents, two keys** (S4, DI-37): the customer is created, then subscribed; a subscribe refused or lost after
  the customer was saved says «أُضيف {name} إلى الزبائن؛ لم يُحفظ الاشتراك.», keeps every field and sends the
  subscribe alone with its own key; closing then says the customer stays with no subscription.
- **The renewal**: its start from the statement's `renewal.startsOn`, the renewed package as one line with «تغيير
  الباقة» (or its custom terms repeated), `renewalOfId` sent; renewed meanwhile → `SUBSCRIPTION_ALREADY_RENEWED`'s line
  and a new subscription instead.
- **S12**: `Sheet`'s `start` and `end` sides are full width below 768 px, three quarters (at most 24 rem) from there
  on; `SheetBody` lets its content shrink.

## Spec D and finding 171 (the supervisor's decision, for the owner to confirm)

A published price is sent as **`published: { period, audience, shiftId?, name }`** — `name` the line the desk shows,
in its language — **never a `priceId`**. The API is not changed: the sheet **reads the space's prices again each time
it opens** (no older read shown), the done toast states **the amount the server charged, from the answer**, and a
subscribe refused for the price (`invalid_choice` on `published`, or `PAYMENT_EXCEEDS_DUE`) is worded, keeps every
field and reads the prices again. **Finding 171 stays Open** (its other option, an amount the server compares, is API
work for later); no line is added to it.

## Carried from #122

- `fix(desk): return the focus after edit and archive` — `CustomerActions` keeps its «⋯» and gives the focus back to
  it after the edit dialog and the owing archive's question (review F1).
- `fix(desk): compare the edited phone normalised` — the same number typed in its local form is no change (F2).
- `test(desk): retitle the idle test; archive present` — test 67's title (F3); the at-once archive of a present
  customer's toast line (F4).

Each test seen red before its code (F4's by its break: `lines` dropped from that path).

## Scope

- `shared/design-system`: `Sheet` (S12) and its test.
- `features/packages`: `useOfferedPackages` (exported).
- `features/spaces`: `useSpacePrices` (exported), the published prices read afresh.
- `features/desk`: the repository's `createCustomer` and `subscribe`; `SubscriptionSheet`, `PackageOptions`,
  `CustomTerms`, `PriorDebts`; `useSubscriptionSheet`, `useSheetForm`, `useCreateCustomer`, `useSubscribe`; the
  services `sheetRequest`, `endOf`, `packageLine`, `publishedChoices`; the entries in the search, the card, the «⋯»,
  the list and the file; the toast.
- `pages/dashboard/space`: `SubscriptionSheetSlot`, `useSheetOpener`; `DeskPage`, `CustomersPage`, `CustomerPage`.
- Copy: `desk.sheet`, both languages.
- Docs: `desk.md`, `customers.md`, `subscriptions.md`, `packages.md`, `spaces.md`, `overview.md`, `foundation.md` §12;
  findings 101 and 125 resolved.

## Acceptance criteria

- [x] The sheet opens from every entry with what the entry knows (a typed name or phone, the customer, a renewal); a
  new customer → name and phone (the phone required when anything stays owed); the published week and month prices,
  the offered packages (one line each), «مخصّص» only for whoever may type a price; the dates (the renewal's start from
  its statement); the money block over the prior debts and the new price; one submit naming the amount.
- [x] A new customer saved and the subscription refused says what was saved and keeps the sheet for the subscription
  alone (DI-37); every toast is worded from the server's answer (`payments`, `debtAgorot`, `CUSTOMER_HAS_DEBT`).
- [x] The end sheet is full width below 768 px (S12).
- [x] Lint, typecheck, `test:unit`, the scoped `test:component`, the production build, `check:build`,
  `check:classes`, `format:check`, `check:links`, `check:conflicts`; CI green; `CLEAN`.

## Out of scope

No `apps/api`, `packages/shared`, schema, migration, seed, dependency or `errors.ts` change. An amount the server
compares for a published price (finding 171's other option). Step 9's screens. Not in v1: online payment, QR
check-in, booking, reviews.

## Change type

Feature (web, design system) · fix (web, carried) · docs.

## Evidence

Run locally on the head:
- `npm run lint` · `npm run typecheck` — exit 0.
- `npm run test:unit -w @masaha/web` — `Test Files 139 passed (139)`, `Tests 989 passed (989)`.
- `npm run test:component -w @masaha/web -- src/features/desk src/features/packages src/features/spaces
  src/shared/design-system src/pages/dashboard src/shared/session src/shared/copy` — `Test Files 106 passed (106)`,
  `Tests 706 passed (706)`; after the real run's fix, the two files it touches — `Tests 16 passed (16)`.
- The production build · `npm run check:build` (no dashboard code, data table or Leaflet in the site's first
  download) · `check:classes` · `format:check` · `check:links` · `check:conflicts` — each exit 0.
- Tests 69–77 and the carried tests: each red before its code, or proven by its break seen red ([key] one key for
  both, [role] «مخصّص» always offered, [money] the toast's price from the form, [state] the start computed, the prices
  not read again, the width kept at three quarters, autofocus prevented); each restored.
- The real run in local headless Chrome, as the owner and as reception, Arabic light and English dark at 390, 768 and
  1440: the sheet 390 px wide at 390 and 384 px from 768; reception's new customer on the published «أسبوعي», paid in
  full — the customer and the subscribe with two different keys, the subscribe blocked once and sent again with its
  key, `published` with its name and no `priceId`, the payment the amount recorded; the owner's «مخصّص» with its
  reason; the renewal sheet; carried F1 live (the focus back on «⋯»); touch targets 44 px. **The run found a defect,
  fixed here:** «تغيير الباقة» and the choices' «إعادة المحاولة» were plain buttons inside the sheet's form and sent it
  (now `type="button"`, with tests); before the fix it renewed one demo customer's subscription twice on the local
  data — see the report.

Not run locally — CI judges: the full `test:component`, `test:unit` of `apps/api` and `packages/shared`, `test:api`
(no API change).

## Screenshots

Attached by the owner.

## Definition of Done

- [x] In scope, in v1; no tool attribution; atomic commits, the carried ones first.
- [x] Copy in both catalogues; design-system tokens only; authorization on the server (the sheet hides «مخصّص», the
  server refuses).
- [x] Documents updated; findings 101 and 125 resolved (#124).

## Review fixes (2026-10-26)

Rebased onto `main` after #123 (the closure extension) merged — no conflict; `subscriptions.md` and `overview.md`
keep both PRs' lines. Every finding of the review fixed, each folded into its commit:

- **F1 (money)** — only a **refused** subscribe (a 4xx) after the customer was saved shows DI-37's half state and
  «… في الزبائن بدون اشتراك.» on close. A lost answer keeps «لم يصل الرد…» and «إعادة المحاولة» with the same key,
  and closing says nothing definite: the subscription may have been recorded.
- **F2** — the sheet gives the focus back to what opened it, or to the «⋯» whose item did (a card's, a row's, the
  file's, the desk's phone «⋯»), while it is on the page: the page's opener records it (`OpenSheet`'s `from`), and
  the sheet's `onCloseAutoFocus` uses it.
- **F3 (money)** — a renewal preselects what it renews: its package, its custom terms, or **its published price**,
  matched by the name the sheet gave it, else by audience, shift and its 7- or 30-day span. Nothing matching →
  **nothing chosen** and the submit blocked until a choice (never the first line).
- **F4** — a test makes "the payment is the recorded amount" able to fail: ₪200 typed on ₪150 sends 15000; ₪100
  sends 10000 (red under a break sending the typed amount).
- **F5** — the published prices stay shown while the space is read again behind the sheet (a return to the window);
  they hide only until a read since the sheet opened answered (`isFetchedAfterMount`), and during a refresh after a
  refusal. Finding 171's rule stands: a fresh read on every opening.
- **F6** — `desk.md`'s web code map names the sheet's hooks, services, components, and the page's
  `SubscriptionSheetSlot` / `useSheetOpener`.

The fix round ran only the test files it touches, `lint`, `typecheck` and Prettier (the owner's rule); CI judges the
rest on the new head.
