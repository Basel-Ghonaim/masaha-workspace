## Summary

DESK_SCREENS PR 1b, the second slice of the desk's visits (screen 13), on the desk #116 built: **«غير محصّل»** and
**«بدون سعر»**.

- **«غير محصّل»** lists what `GET …/uncollected-visits` answers, filtering nothing — the auto check-out's visits,
  and (since #114) a hand-closed visit with no customer owing again after a void. The title counts the visits from
  the page's `meta`, never a sum of money (DI-3); three rows, then «عرض الكل» opens the page whole with its pages
  (DI-23); arriving at `#uncollected` opens it and focuses its heading (DI-19). Each row says who, how and when it
  closed, and what it still owes, the server's.
- **«تحصيل»** (the row's primary, DI-4): the money block filled with what the visit owes, recording at most that,
  with the opening's one `Idempotency-Key`; a remainder on a visit with no customer asks a name and a phone
  (DI-11). The toast speaks from the answer.
- **«تسجيل دين»**: the name first, then the phone; the visit's rest becomes that customer's debt. No key — sent once.
- **The owner's «لن يُحصَّل…»** in the row's «⋯» (destructive, DI-27): asks first, says it is reversible (DI-9),
  requires a reason; its toast stays until closed, with «تراجع», which undoes it once (DI-29). No key on either —
  neither is ever re-sent by itself (S3, finding 115).
- **«بدون سعر»**, only for whoever may type a price (`mayTypePrice`; the list is not read for anyone else): each
  visit priced with its amount and reason (DI-10). Absent with none.
- The focus returns to the control that opened a dialog, or — the row gone — to the card's heading (DI-30).

## Scope

- `features/desk`: the repository (the uncollected and unpriced visits, a payment, «تسجيل دين», the write-off and
  its undo, a price); their hooks; `UncollectedCard`, `UncollectedRow`, `CollectDialog`, `DebtDialog`,
  `WriteOffDialog`, `UnpricedCard`, `PriceDialog`; the toasts; `dayWord`; `DeskAbilities`.
- `pages/dashboard/space/desk/DeskPage.tsx`: the cards in the `xl` side column (under the list before it); the
  write-off shown for the owner, from the session's link at the space.
- Copy: `desk.uncollected`, `desk.collect`, `desk.debt`, `desk.writeOff`, `desk.unpriced`, three refusals, both
  languages.
- Docs: `desk.md` (web behaviour, decisions, code map, history), `payments.md` and `visits.md` (*Who uses it*);
  finding 110 resolved, 112 and 115 evidence, finding 164 (new).

## Acceptance criteria

- [x] «غير محصّل» lists the uncollected visits (count, never a client sum — DI-3); «تحصيل» records a payment (a
  remainder needs a phone); «تسجيل دين» leaves it to a customer by phone; the owner's «لن يُحصَّل…» (reason) and
  its undo («تراجع» in the write-off's toast, which stays until it is closed — DI-29; no screen lists a written-off
  visit after it, finding 164).
- [x] «بدون سعر» lists the unpriced visits, only for whoever may type a price (`mayTypePrice`), each priced with its
  reason.
- [x] «تحصيل» carries one key per intent, kept across the transport's re-sends and «إعادة المحاولة»; the unkeyed
  writes are sent once; every 409 the contract names for them is worded; a 403 says it is no longer open to them.
- [x] Lint, typecheck, `test:unit`, the scoped `test:component`, the production build, `check:build`,
  `check:classes`, `format:check`, `check:links`, `check:conflicts`; CI green; `CLEAN`.

## Out of scope

PR 2–4: the desk's search and subscribers, Customers and a customer's file, the subscription sheet. Step 9's
payments list and void. No `apps/api`, `packages/shared`, schema, migration, seed or dependency change. A list of
written-off visits (finding 164).

## Change type

Feature (web) · docs.

## Evidence

Run locally on the head:
- `npm run lint` · `npm run typecheck` — exit 0.
- `npm run test:unit -w @masaha/web` — `Test Files 126 passed (126)`, `Tests 950 passed (950)`.
- `npm run test:component -w @masaha/web -- src/features/desk src/features/occupancy src/pages/dashboard
  src/shared/copy` — `Test Files 22 passed (22)`, `Tests 131 passed (131)`.
- The production build · `npm run check:build` (no dashboard code, data table or Leaflet in the site's first
  download: 1,030,340 B, the growth over #116 the new copy lines) · `check:classes` · `format:check` ·
  `check:links` · `check:conflicts`.
- Each new test seen red before its code; the plan's breaks for the role, key, money and state guards made, each
  red, each restored.
- The real run in local headless Chrome, as the owner and as reception, Arabic light and English dark at 390, 768
  and 1440: the owner's write-off of a visit and its undo from the toast (one `POST`, one `DELETE`, no key, neither
  re-sent); reception's «تسجيل دين» to a phone; «تحصيل» ₪10 with the first send offline, then «إعادة المحاولة»
  (four requests, one key, one payment); touch targets 44 px at 390. The unpriced case not performed: the demo data
  holds no unpriced visit (its tests prove it).

Not run locally — CI judges: the full `test:component`, `test:unit` of `apps/api` and `packages/shared`, `test:api`
(no API change).

## Screenshots

Attached by the owner.

## Definition of Done

- [x] In v1 scope and in task scope; files staged by path.
- [x] Atomic Conventional Commits, each with its tests and documents.
- [x] Every string through the copy catalogue, in both languages; semantic tokens only.
- [x] Authorization stays on the server: the write-off's and the price's controls are hidden by role, and their
  refusals are still worded.
- [x] Documentation updated (one owner per fact); findings recorded.
- [x] CI green on the pushed head; `CLEAN`.
