## Summary

DESK_SCREENS PR 1a, the first slice of the desk's visits (screen 13): **«مكتب الاستقبال»** replaces its
placeholder for the owner and reception.

- **Who is present** («الحاضرون الآن», `occupancy`): read on arrival, every 30 s while the page is visible and
  never while hidden, and at once on returning; a table from 768 px, a card each below it; a visit's charge so far
  is the server's; the count with the capacity («27 / 40»).
- **The live status's control** (P2): one button in the colour of what visitors see, the whole line from 768 px,
  named by it at every width; it sets a state for 30 minutes, an hour, two hours or until closing, and returns to
  the automatic status; it is disabled with its reason while the space is closed, and the server's `SPACE_NOT_OPEN`
  is said in its panel.
- **A visitor's check-in** («تسجيل زيارة», in the top bar from 768 px, in a bar at the foot below it): the name,
  «طالب» only where the terms carry student rates, «الوردية» only where the space has shifts (the current one
  chosen), the rate the visit will copy; the server's warnings are said after, in the toast.
- **A visit's check-out**: the server's quote, read each minute while open and again before sending when older
  than 4 minutes; the money block fills «المستلم الآن» with the due and records never more than it; a remainder
  asks a name and a phone; a visit with no rate takes a typed price with its reason, or closes unpriced for
  whoever may not type one; the toast says what the answer recorded.
- **One `Idempotency-Key` per intent** (`useIntentKey`): kept across the transport's re-sends, a second press and
  «إعادة المحاولة»; a lost answer says a retry is safe, a refusal that nothing was recorded.
- **«تبديل الموظف»**: signs out on the server and opens sign-in with the desk as `next`.

## Scope

- `shared/api`: `useIntentKey`, `withIdempotencyKey`, `api.postWithMeta`.
- `pages/dashboard/shell`: `PageActionBar` and its slot; `shared/routing`'s `showActionBar` / `useActionBarShown`,
  read by `app/providers.tsx` so the toasts sit above the bar while it shows (the owner's choice during the run).
- `features/occupancy`: the state now, `PresentList`, `LiveStatusControl`, the override's writes.
- `features/desk` (new, dashboard-only): the repository, the terms, the check-in, the quote and the check-out, the
  money block, the toasts.
- `pages/dashboard/space/desk/`: `DeskPage`, «تبديل الموظف»; `routes.tsx`: the desk's screen.
- Copy: `occupancy` and `desk` (new), both languages.
- Docs: `desk.md`, `occupancy.md`, `visits.md` (web parts), `architecture.md` §2, §3 (`desk`'s exception to the
  naming rule, S1) and §7, `overview.md`, `docs/README.md`; finding 161.

## Acceptance criteria

- [x] `/dashboard/spaces/:id/desk` (owner and reception) shows «الحاضرون الآن» with the people present (name, kind,
  since, duration, a visit's charge so far — the server's), read on arrival, every 30 s while visible and on
  returning; never polled while hidden.
- [x] The live status control reads what visitors see (with «يدويًا · 0:30» under an override); sets a state for
  30 min, 1 h, 2 h or until closing and returns to automatic; disabled with its reason while closed;
  `SPACE_NOT_OPEN` said in the popover.
- [x] «تسجيل زيارة» (top bar from 768 px, the bottom bar below it) checks a visitor in by name, «طالب» only where
  the terms carry student rates, «الوردية» only where the space has shifts; the warnings in the toast.
- [x] «خروج» opens the check-out with the server's quote; the money block fills «المستلم الآن» with the due; a
  remainder needs a name and a phone when the visit has no customer; no rate → a typed price and its reason, or an
  unpriced close with a phone; the toast from the answer.
- [x] Every create carries one `Idempotency-Key` per intent, kept across a retry and a double press; a lost answer
  says a retry is safe; the contract's 409s are worded; a 403 says it is no longer open to them.
- [x] «تبديل الموظف» signs out and opens sign-in with the desk as `next`.
- [x] Lint, typecheck, `test:unit`, `test:component`, the production build, `check:build`, `check:classes`,
  `format:check`, `check:links`; CI green; `CLEAN`.

## Out of scope

PR 1b: the uncollected visits (collect, «تسجيل دين», the write-off and its undo) and the unpriced visits' pricing.
PR 2–4: the desk's search and subscribers, Customers and a customer's file, the subscription sheet. No `apps/api`,
`packages/shared`, schema, migration, seed or dependency change. The attendance log tab (finding 161).

## Change type

Feature (web) · docs.

## Evidence

Run locally on the head, after the rebase on #114:
- `npm run lint` · `npm run typecheck` — exit 0.
- `npm run test:unit -w @masaha/web` — `Test Files 125 passed (125)`, `Tests 946 passed (946)`.
- `npm run test:component -w @masaha/web -- src/shared/api src/features/occupancy src/features/desk
  src/pages/dashboard src/shared/copy src/shared/routing src/app` — `Tests 1 failed | 179 passed (180)`: the app
  shell's `App` › "renders the main landmark" missed its 3 s waiting for the site's lazy chunk under load; it and
  `router` › "shows the root's general error…" pass alone (`Tests 3 passed (3)`). CI's full lane judges.
- The production build · `npm run check:build` (no dashboard code, data table or Leaflet in the site's first
  download: 1,011,159 B → 1,024,617 B, the growth the new copy sections) · `check:classes` · `format:check` ·
  `check:links` · `check:conflicts`.
- Each new test seen red before its code; the plan's breaks made, each red, each restored.
- The real run in local headless Chrome, as the owner and as reception, Arabic light and English dark at 390, 768
  and 1440: a check-in sent offline then «إعادة المحاولة» (four requests, one key, one visit), the bar at the foot,
  the layouts, the touch targets (44 px, the bar 48 px), a cash check-out with change, an unpaid one left to a new
  phone, the override set and cleared, `CLOSURE_IN_FORCE` at a closed space with its check-out, the width break,
  «تبديل الموظف».

Not run locally (CI judges): the full `test:component` lane, `test:unit` of `apps/api` and `packages/shared`,
`test:api` (no API change).

Not performed, by design: `SPACE_FULL` as the owner and as reception (the owner's decision; no space is full in the
demo data — tests 21 and 12).

## For `OPEN_DECISIONS.md` point 4 (the supervisor's line)

> **Built as (DESK_SCREENS, 2026-10-24):** the server ends a session of an account whose only active links are
> reception links after 15 minutes with no request other than the desk's polled state; the access token names its
> session (`sid`); every other request renews it; the refusal is 401 `SESSION_IDLE`, which ends only that device's
> session (spec C, worker B). The web shows «تبديل الموظف» on the desk (sign out, back to sign-in with the desk as
> `next`) and the sign-in page says why a session ended.

This PR builds «تبديل الموظف»; spec C and the sign-in page's line come later (worker B's DESK_API, then PR 3).

## Screenshots

Attached by the owner.

## Definition of Done

- [x] Scope as the plan's PR 1 commits 1–4 (A1); atomic commits, each with its reason.
- [x] Every user-facing word through the catalogue, in both languages; Arabic plural forms for the counts.
- [x] No design-system change; semantic tokens only.
- [x] Docs updated where the behaviour lives; `#116` in their history.
- [x] Lint, typecheck, tests, build and checks green locally; CI green on the pushed head.
