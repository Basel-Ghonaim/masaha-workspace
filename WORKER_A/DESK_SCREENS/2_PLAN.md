# DESK_SCREENS — the front desk and the subscribers on the web: Front desk, Customers, Customer details, New / renew subscription (build map steps 7 and 8's screens, screens 13–16) — the plan

> **Approved by the owner, 2026-10-24 — binding on every executor of this plan** (it wins where the plan
> below differs), every §14 point as recommended:
> - **The start (the owner's change):** **PR 1a starts now**, without waiting for the public-site fix PR (the
>   owner has not reviewed the site yet; that PR comes later, between two of this plan's PRs, and touches the
>   site, not the dashboard). The header's "starts only after worker A's public-site fix PR" no longer holds; PR
>   1a's first step stays `git diff --name-status 104d9d07 origin/main`.
> - **§14.1 — the plan as written**, S1–S13 (S1's `desk` feature and its exception to architecture §3's naming
>   rule; S4's one key per intent).
> - **§14.2 — A1 taken:** PR 1a (commits 1–4) and PR 1b (commits 5–6).
> - **§14.3 — finding 125: (c), no preview** (spec A not built).
> - **§14.4 — spec D taken:** reception subscribes from the published week and month prices; **the month is 30
>   days and the week 7, the first day counted** (the owner confirms). Built by worker B before PR 4.
> - **§14.5 — worker B's DESK_API** (specs B, C and D, one migration) runs **right after PAYMENTS** (step 9, already
>   executing) and before ANNOUNCEMENTS PRs 2–4; it must merge before PR 3 (B, C) and PR 4 (D).
> - **DESK_API's plan changed two specs (2026-10-25), binding on PR 3 and PR 4:** spec C's idle refusal — every
>   request answers 401 `SESSION_IDLE` and the **refresh** answers it too (deleting the session), so PR 3 shows
>   the line from the refresh's answer, as planned; spec D's request is **`published: { period, audience,
>   shiftId?, name }`** — the name **inside** `published` (#118; a top-level `name` is stripped and refused) —
>   never a `priceId` (price rows are re-created on every save) — PR 4 sends that. Finding 171 (a price changed
>   between the read and the subscribe is charged silently) is decided with PR 4.
> - **§14.6 — DI-1 … DI-53 approved as written;** what the owner dislikes when he tries the screens goes to the
>   next PR's carried file.
> - **§14.7 — the Arabic copy of §10 approved as written,** on the same terms.
> - **§14.8 — the documents** as proposed; the supervisor writes `OPEN_DECISIONS.md` point 4's *Built as* line
>   once spec C merges.
> - **§14.9 — S12 taken** (the end sheet full width below 768 px, PR 4, `area:design-system`).
> - **§14.10 — «27 / 40» kept as settled, no uncollected total (DI-3 stands).**
> - **§14.11 — the real run's writes as §13 lists them,** «يوسف»'s subscription ended in PR 3 included; FULL as
>   reception not performed.
> - **The owner's standing rules:** a small fix a review defers is the next PR's first commit
>   (`0_CARRIED_FROM_<n>.md` in this folder); a test seen red before its code is its own break, a separate break
>   only for a guard the red step did not prove; fix rounds run only what the change touches; a full lane killed
>   for memory is re-run once, then CI judges; a demo account or data lacking a real-run case → stop and report;
>   never leave a carried item or a review nit silently.

> Written 2026-10-24 from `origin/main` **`104d9d07`** (#112 merged: ANNOUNCEMENTS PR 1 — the closure
> warning `CLOSURE_IN_FORCE` at both check-ins is **on the base**, so nothing here waits for #112). Worker A,
> folder `C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\`. **The executor of PR 1 starts only after worker A's
> public-site fix PR (`0_CARRIED_FROM_111.md` + the owner's list) has merged**; its first step is
> `git diff --name-status 104d9d07 origin/main` (§13). Four PRs in sequence (the owner's decision 2), each cut
> from the latest `origin/main` once the one before has merged, each with its own execution prompt and review:
> - **PR 1** `feat/desk-visits` — the desk's visits: six commits, ≈ 88 files. **A1 (recommended) splits it:**
>   **PR 1a** `feat/desk-visits` — commits 1–4 (≈ 58 files), title = commit 4's subject
>   `feat(desk): check visitors in and out at the desk`; **PR 1b** `feat/desk-uncollected` — commits 5–6
>   (≈ 32 files), title = commit 5's subject, cut from `main` once 1a merges.
> - **PR 2** `feat/desk-subscribers` — the desk's subscribers: four commits, ≈ 38 files.
>   Title: `feat(desk): find customers from the desk's search` (commit 2's subject).
> - **PR 3** `feat/customers-file` — Customers and Customer details: five commits, ≈ 55 files.
>   **Waits for worker B's API item DESK_API (spec B, and spec C) to merge** (§6).
>   Title: `feat(desk): show a customer's file`.
> - **PR 4** `feat/subscription-sheet` — New / renew subscription: four commits, ≈ 40 files.
>   **Waits for spec D if the owner takes it** (§14.4). Title: `feat(desk): subscribe a new or known customer`.
>
> The executor may be any capable coding agent: no step depends on a Claude skill (the appendix is only a map).
> Finding numbers are this item's range, **160 and on**, in the order first recorded. `#PRNUM` stands for the
> PR's number until the push (§13). `{date}` is the day the line is committed (`YYYY-MM-DD`). Words are written
> Arabic first, then English. Design issues are **DI-n** (§8), stronger decisions **S-n** (§5), alternatives
> **A-n** (§5), API specs **spec A–D** (§6).

## 1. Summary

Screens 13–16 on the web, over the API of steps 7 and 8 (#94, #95, #97, #100, #102, #106, #109, #110, #112). The
dashboard shows a placeholder for «مكتب الاستقبال» and «الزبائن» today; this item replaces them and adds a
customer's file at `/dashboard/spaces/:spaceId/customers/:customerId`.

- **PR 1 — the desk's visits.** The desk page: «الحاضرون الآن» (the staff's state now, every 30 s and on
  focus), the live status's control and its override (P2), «تسجيل زيارة» (the bottom bar on a phone, P1), the
  visit's check-in with the rates the space offers now and the warnings the server answers, the visit's
  check-out with the server's quote, the money block (K2), a price typed by hand with its reason or an unpriced
  close, the unpaid rest left to a customer by phone; «غير محصّل» (the uncollected visits): collect one, «تسجيل
  دين», the owner's «لن يُحصَّل» and its undo; «بدون سعر» (the unpriced visits) priced by whoever may type a
  price; «تبديل الموظف». Two new web features: `desk` and the state-now part of `occupancy` (S1).
- **PR 2 — the desk's subscribers.** The desk's one search (K1): the people present first, then the customers
  (the customers list's search), then «تسجيل زيارة باسم «X»»; the customer card (current subscription, status,
  balance); «حضور» on the current subscription with the choice first when it has none or it has expired, and the
  server's warnings after; a subscriber's one-tap check-out and what their subscription then owes; a payment on
  one of a customer's items («استلام»).
- **PR 3 — Customers and Customer details.** The paged, searched, filtered list (URL state, P5, P6); the file:
  header and actions, the unpaid visits, each subscription's card with its progress and money and, on demand,
  its statement (check-ins and payments); edit, the owner's archive (at once with «تراجع» when settled, an
  `AlertDialog` when owing) and restore; ending a subscription early; the idle sign-out's answer (spec C).
- **PR 4 — New / renew subscription.** One sheet from every entry (the desk's search, the page action, the
  customers list, the card, the file): a new customer, a new subscription, a renewal; the space's offered
  packages or «مخصّص» (a typed price with its reason, for whoever may type one); the money block over what is
  owed from before (K3), allocated by the server; the debt warning.

No `apps/api`, `packages/shared`, schema, migration, seed or dependency change in this item: every API change it
needs is a worker-B spec (§6), merged before the PR that uses it.

## 2. The contract

### Scope

**PR 1 — the desk's visits**
- `shared/api`: `useIntentKey` and `withIdempotencyKey` (S4).
- `pages/dashboard/shell`: the page's bottom bar slot (`PageActionBar`, P1) and its room under the content.
- `features/occupancy` (any page group): the staff's state now, polled; `LiveStatusControl` (P2) with the
  override; `PresentList` with a row-action slot (S1).
- `features/desk` (new, dashboard-only): its repository, keys and hooks for a visit's check-in, quote,
  check-out, a visit's payment, «تسجيل دين», the write-off and its undo, the visit terms, the uncollected visits,
  the unpriced visits and their pricing; `VisitDialog`, `CheckOutDialog`, `MoneyBlock`, `UncollectedCard`,
  `UnpricedCard`, `CollectDialog`, `DebtDialog`, `WriteOffDialog`, `CheckOutAction`, the desk's toasts.
- `pages/dashboard/space/desk/`: `DeskPage` composing them; `SwitchStaffButton` («تبديل الموظف»).
- `pages/dashboard/routes.tsx`: the desk's screen. Copy: `desk` (new), `occupancy` (new), `dashboard`.
- Docs: `desk.md`, `occupancy.md`, `visits.md`, `payments.md` (their web parts, S1), `architecture.md` (§3 S1,
  §7 the desk's polling and keys, §2 the bottom bar), `overview.md`, `docs/README.md`; findings 160–164.

**PR 2 — the desk's subscribers**
- `features/desk`: the customers search (`GET …/customers?q`), the customer card, a subscriber's check-in and
  check-out, the open check-ins (`GET …/check-ins?open=true`), a payment on a customer's item (`PayDialog`, the
  customer's file read for its items).
- `features/occupancy`: `usePresentMatches(term)` for the search's first group.
- `pages/dashboard/space/desk/`: `DeskSearch` composed with the present matches.
- Copy: `desk.search`, `desk.customer`, `desk.subscriber`, `desk.pay`. Docs: `desk.md`, `subscriptions.md`,
  `customers.md` (web parts).

**PR 3 — Customers and Customer details**
- `features/desk`: the customers list (filters in the URL), the file, the statement, edit, archive, restore,
  end a subscription early.
- `shared/session` + the sign-in page: the idle sign-out's line (spec C's `SESSION_IDLE`).
- `pages/dashboard`: `CustomersPage`, `CustomerPage` (titled by the name), the route `customers/:customerId`.
- Copy: `desk.customers`, `desk.file`, `desk.statement`, `auth.signIn.idle`. Docs: `customers.md`,
  `subscriptions.md`, `desk.md`, `auth.md`, `architecture.md` §4; findings 124 and 125 resolved (§7).

**PR 4 — the subscription sheet**
- `features/packages`: `useOfferedPackages(spaceId)` (exported hook).
- `features/desk`: `SubscriptionSheet` and its hooks: new customer, subscribe, renew, custom terms.
- `pages/dashboard`: every entry opens the sheet; the page passes the packages and the shifts.
- `shared/design-system` (if §14.9 approves S12): `Sheet side="end"` full width below 768 px (finding 101).
- Copy: `desk.sheet`. Docs: `desk.md`, `subscriptions.md`, `packages.md`, `foundation.md` (if S12).

### Acceptance criteria

**PR 1**
- [ ] `/dashboard/spaces/:id/desk` (owner and reception) shows «الحاضرون الآن» with the people present (name,
  kind, since, duration, a visit's charge so far — the server's), read on arrival, every 30 s while visible and on
  returning; never polled while hidden.
- [ ] The live status control reads what visitors see («يظهر للزوار: …», with «يدويًا · 1:24» under an
  override); it sets a state for 30 min, 1 h, 2 h or until closing and returns to the automatic state; it is
  disabled with its reason while the space is closed now; `SPACE_NOT_OPEN` is said in the popover.
- [ ] «تسجيل زيارة» (top bar from 768 px, the bottom bar below it) checks a visitor in by name, «طالب» only where
  the terms carry student rates, «الوردية» only where the space has shifts (the current one chosen); the
  server's warnings (`SPACE_FULL`, `OUTSIDE_OPENING_HOURS`, `CLOSURE_IN_FORCE`) are said in the success toast.
- [ ] «خروج» of a visit opens the check-out with the server's quote (refreshed each minute while open, re-read
  before sending when older than 4 minutes); the money block fills «المستلم الآن» with the due; a remainder
  needs a name and a phone when the visit has no customer; a visit with no rate asks a typed price and its
  reason of whoever may type one, else closes unpriced (phone required); the toast names the amount, method and
  remainder from the server's answer.
- [ ] «غير محصّل» lists the uncollected visits (count, never a client sum — DI-3); «تحصيل» records a payment (a
  remainder needs a phone); «تسجيل دين» leaves it to a customer by phone; the owner's «لن يُحصَّل…» (reason) and
  its undo («تراجع» in the write-off's toast, which stays until it is closed — DI-29; no screen lists a
  written-off visit after it, finding 164).
- [ ] «بدون سعر» lists the unpriced visits, only for whoever may type a price (`mayTypePrice`), each priced with
  its reason.
- [ ] Every create carries one `Idempotency-Key` per intent, kept across a retry and a double press (S4); a lost
  answer says a retry is safe; every 409 the contract names is worded; a 403 says it is no longer open to them.
- [ ] «تبديل الموظف» signs out and opens sign-in with the desk as `next`.
- [ ] Lint, typecheck, `test:unit`, `test:component`, the production build, `check:build` (no desk code in the
  site's first download), `check:classes`, `format:check`, `check:links`; CI green; `CLEAN`.

**PR 2**
- [ ] The desk's search (from 768 px it takes the focus on arrival) finds the people present by name or a
  phone's last digits first, with «خروج»; then customers (server search), each a card with «حضور» or
  «خروج», «استلام {المبلغ}» when they owe, and «⋯»; then «تسجيل زيارة باسم «X»» (primary when nothing
  matches) — never two equal buttons (DI-20).
- [ ] «حضور» checks the customer in on their current subscription in one tap; with none, or an expired or not
  started one, a dialog first offers «تسجيل كزيارة» and «تسجيل على أي حال» (DI-14); the server's warnings
  after are said; `MEMBER_ALREADY_CHECKED_IN` says they are here.
- [ ] A subscriber's «خروج» is one tap; the toast names the stay and, for a usage-based subscription, what it
  owes, with «استلام» opening the payment on it.
- [ ] «استلام» pays one item: the customer's unpaid visits and owing subscriptions, the chosen one preset; the
  picker lists the present debtors first (DI-21).
- [ ] After a check-in or check-out started from the search, the search is cleared and takes the focus.
- [ ] The same checks and CI.

**PR 3**
- [ ] «الزبائن» lists the space's customers 20 a page (search, status chips, kind, payment; `ARCHIVED` for the
  owner only), every filter and the page in the URL; five columns from 768 px, cards below.
- [ ] A customer's file shows the header (phone, here now, status, balance «عليه / له رصيد / مسدّد» from one
  component), the actions by state (DK-013), the unpaid visits with «تحصيل», each subscription's card (dates,
  terms, progress, due/paid/left) with «عرض الكشف» opening its statement, «استلام المتبقي» and «إنهاء
  الاشتراك».
- [ ] Edit sends only what changed and is never retried by itself (finding 123); archive and restore are the
  owner's (at once with «تراجع», or an `AlertDialog` naming the debt); a present customer's archive says so.
- [ ] A reception session ended for idleness lands on sign-in with its line (spec C).
- [ ] The same checks and CI.

**PR 4**
- [ ] The sheet opens from every entry with what the entry knows (a typed name or phone, the customer, a
  renewal); new customer → name and phone (the phone required when anything stays owed); the space's offered
  packages (one line each, DK-007), «مخصّص» only for whoever may type a price; the dates (the renewal's
  proposed start from its statement); the money block over the prior debts and the new price (K3); one submit
  naming the amount.
- [ ] A new customer saved and the subscription refused says what was saved and keeps the sheet for the
  subscription alone (DI-37); every toast is worded from the server's answer (`payments`, `debtAgorot`,
  `CUSTOMER_HAS_DEBT`).
- [ ] The same checks and CI.

### Out of scope
- Any API, `packages/shared`, schema, seed or dependency change (§6 holds them as worker-B specs).
- Step 9: voiding a payment, the payments list («الدفعات», «دفعاتي اليوم»), collections per staff member,
  credit and balances screens; a payment's «⋯» (DK-016) — **left out, no dead control** (§4 decision 7).
- The attendance log tab («السجل»): no route reads visits by date (finding 161).
- The WhatsApp debt reminder in the file: finance's (step 11; the template is the owner's settings).
- Correcting a subscription's limits, dates, name or price: built on the API, not in the design (finding 163).
- The owner's overview («يحتاج انتباهك» linking `#uncollected`): step 12; the anchor is built (DI-19).
- Not in v1: online payment, QR check-in, booking, reviews.

## 3. The reading done

`CLAUDE.md`; `workflow.md` (whole); `testing.md` (whole); `architecture.md` (whole); `foundation.md` §5, §8–§13,
§15; `localisation.md`; `documentation.md` §5; `docs/features/desk.md`, `visits.md`, `occupancy.md`,
`customers.md`, `subscriptions.md`, `payments.md`, `packages.md`, `space-settings.md`, `auth.md`;
`api-contract.md` §1–4, *Session*, *Managed spaces*, *Packages*, *Occupancy*, *Customers*, *Subscriptions*,
*Front desk*, §6; `security.md` › *Tokens and cookies*, *Authorization*; ADR 0003, 0009, 0015 (whole), 0008,
0010 (their decisions); `v1-mvp.md` steps 7–12 and the planned surface; `SCREENS.md`; `glossary.md` › Package;
`data-model.md` › Package; `overview.md` › *Built*, *Not in v1*; `docs/README.md` › deferred documents; the
findings index and findings 84, 87, 97, 101, 110, 112, 115, 123, 124, 125, 130, 132. #112's diff (the closure
warning, the catalogue lines). The prototype: `Desk.html`, `Customers.html`, `Customer file.html`,
`desk-core.jsx`, `desk-sheet.jsx`, `desk-data.js` (progress, status and payment badges, methods), `owner.jsx`
(`PublicStateControl`). `DECISIONS_DESK.md`, `DECISIONS_SHARED.md`, `DECISIONS_OWNER.md`; the six reports
`R2-DK-AX`, `R2-DK-CP`, `R2-DK-EX`, `R2-DK-TR`, `R2-DK-UX`, `R2-DK-VD`; `_SHARED\OPEN_DECISIONS.md`. The code:
`pages/dashboard` (routes, navigation, the shell, `PageHeader`, the placeholder, Staff and Packages pages),
`features/staff` (the pattern: repository, keys, list hook, row write, dialog hook, toasts), `features/occupancy`,
`features/spaces`' `useSpaceShifts`, `shared/api` (client, `request.ts`, `retry.ts`, the query client,
`useLinkEnded`), `shared/forms` (`useServerForm`, `useRefusalView`), `shared/lists`, `shared/routing`'s exports,
`shared/session` (`useSignOut`), `shared/lib` (money, whole numbers), the design system's barrel (`DataTable`
props, `Sheet`, `Button` heights, `Toaster`), `src/test/` (helper names); `packages/shared`'s `core`
(idempotency key), `desk`, `visits`, `occupancy`, `customers`, `subscriptions`, `payments`, `packages`;
`apps/web/scripts/dashboardOnly.ts`; the demo seeds `demo.ts`, `demoDirectory.ts`; `TASKS\DEMO_DAILY_BASEL`;
`WORKER_A\PUBLIC\2_PLAN.md`, `3_EXEC_PROMPT_PR4.md` §2, `0_CARRIED_FROM_111.md`.

**What the reading changed.**
- **#112 merged during the reading:** the closure warning is built; the base moved to `104d9d07`.
- **The API answers the warnings after the check-in, never before** (they never refuse). The prototype's
  `WarnDialog` asks first; the web can ask first only what it already knows from the server (no current
  subscription, or its status `EXPIRED` / `UPCOMING`); the rest is said after, in the toast (S6, DI-14).
- **A payment pays one item** (`POST …/payments`, one `visitId` or `subscriptionId`): the prototype's «الأقدم
  أولًا» across items has no route; only a subscribe allocates (DI-22).
- **A visit's check-in carries no customer** (`checkInVisitSchema`): DK-020 «تسجيل كزيارة» as the customer
  cannot be built as designed (DI-14, finding 160).
- **A typed price needs a reason** (data model; `priceVisitSchema`, `customTermsSchema`): the prototype has
  none (DI-10).
- **The subscribe is one transaction with its payment:** the prototype's «حُفظ الاشتراك؛ لم تُسجَّل الدفعة»
  cannot happen; a *new customer* saved and its subscription refused can (two requests, DI-37).
- **The published week and month prices are packages** (glossary, data model), **but the subscribe takes only a
  `packageId` or custom terms**: reception, who may not type a price, cannot subscribe anyone to the published
  month (spec D, §14.4).
- **No route reads visits by date, a customer's paid visits, or the staff's names for reception** (findings 161,
  162; the log tab, the file's payments tab and «سجّلها» are left out).
- **Reception reads no settings** (owner-only): whether they may type a price is `visit-terms`' `mayTypePrice`,
  which `can()` answers for the caller — the one source for the visit and the sheet (S7).
- **The uncollected list holds the auto check-out's visits only;** a manual check-out's unpaid rest is a
  customer's debt (finding 110) — the prototype's «خرج بدون دفع» rows are not there.
- **The write-off is reversible** (K6 as built, finding 110): the prototype's «لا يمكن التراجع» is false.
- **The dashboard shell has no bottom bar** (P1's «تسجيل زيارة» on a phone): the shell gains a slot (S9).
- **`Sheet side="end"` is three-quarter width on a phone** (finding 101; DK-024 settled it full width).

## 4. The owner's decisions, as they will be built

1. **Worker A builds it** — the web's item.
2. **One plan, PRs in sequence**, as the header: the supervisor's cut, kept, with PR 1 split in two if the owner
   takes A1 (its file count passes ≈ 60).
3. **The allocation preview (finding 125): (c) no preview** — recommended (§6 compares). The sheet lists what is
   owed from before (each item and the total) and says «يُطبَّق المستلم على المستحق من قبل أولًا، ثم على الاشتراك
   الجديد.»; after saving, the toast lists each part the server's answer allocated (`NewSubscription.payments`).
   This is finding 125's own first *Resolves when*. Spec A (a quote route) is written for the owner who prefers
   (b).
4. **The statement's snapshot (finding 124):** spec B for worker B, merged before PR 3.
5. **The shared desk device:** spec C for worker B (reception's session ends after 15 minutes idle on the
   server), and «تبديل الموظف» on the desk (PR 1) and the idle answer's line (PR 3). The line that revises
   `OPEN_DECISIONS.md` point 4, for the supervisor (the file already carries the 2026-10-24 revision; this line
   records how it is built):
   > **Built as (DESK_SCREENS, 2026-10-24):** the server ends a session of an account whose only active links
   > are reception links after 15 minutes with no request other than the desk's polled state; the access token
   > names its session (`sid`); every other request renews it; the refusal is 401 `SESSION_IDLE`, which ends
   > only that device's session (spec C, worker B). The web shows «تبديل الموظف» on the desk (sign out, back to
   > sign-in with the desk as `next`) and the sign-in page says why a session ended.
6. **The design's basis:** the settled decisions; every defect the six reports prove is a design issue (§8),
   built once approved; what would change a settled decision is an alternative (§5).
7. **Step 9's parts, left out with no dead control:** voiding a payment (DK-016's «⋯» on a payment row, the void
   dialog), «دفعاتي اليوم», the payments list and its filters, collections per staff member, «سجّلها» (who
   recorded a payment, by name). Voided payments the API already marks are shown struck through with their
   reason (K4) — a read, not step 9's void. **Nothing of screens 13–16 needs step 9 to be safe:** a mistaken
   payment is voided by the owner once step 9 lands; until then the owner's write-off covers a visit.
8. **The decisions are proposals the worker may challenge:** §5's alternatives.

## 5. Stronger decisions

**S1 — the features: `desk` holds the desk's screens; `occupancy` holds the state now.**
- `features/desk` (dashboard-only): every route screens 13–16 write or read, **except** the state now and the
  override (`occupancy`'s), the packages' list (`packages`') and the space's shifts (`spaces`'): the desk
  module's (check-ins, check-outs, payments, «تسجيل دين», write-off, the customers list and file, archive,
  subscribe, the statement), **and** the visits', payments', customers' and subscriptions' routes those screens
  call (visit terms, quote, unpriced visits and pricing; uncollected visits; create, edit, restore; the open
  check-ins, the end).
- `features/occupancy` (any page group, exists): `useStateNowQuery`, `LiveStatusControl`, `PresentList`,
  `usePresentMatches` — the state now is a fact of its own, read by the overview later (step 12).
- **What stays in `pages/dashboard`:** the routes and titles; `DeskPage`, `CustomersPage`, `CustomerPage`, which
  compose `occupancy`'s list with `desk`'s check-out action (a slot), `desk`'s sheet with `packages`' and
  `spaces`' data (props), and the role's abilities (S5); the shell's bottom bar; «تبديل الموظف».
- **Dependency rule:** `desk` and `occupancy` never import each other (lint); the page sets one in the other's
  slot, as the site sets `lookups` in `directory`'s. Their keys meet only in the space's scope: every `desk` write
  invalidates `['space', spaceId]` (architecture §7 already says so), which refetches `occupancy`'s state now.
- *Why:* architecture §3 already names `desk` "the front desk: check-in, check-out with payment, subscribe with
  payment; the customers list and file"; the same audience works these routes on the same screens; a feature
  per module would put every dialog that reads one module and writes another (the check-out: `visits`' quote,
  `desk`'s check-out; the sheet: `customers`' create, `desk`'s subscribe) in the page (A2). *Cost:* a document
  change — architecture §3's "names match the backend" gains the exception, in PR 1's documents: «`desk` on the
  web holds the desk's screens: it calls the desk module's routes and those of `visits`, `payments`,
  `customers` and `subscriptions` that the same staff call on the same screens; each of those capabilities gets a
  web feature of its own only with a screen of its own (step 9's payments)». The capability documents get their
  web parts where the route is owned (S13). *Recommend:* take it.

**S2 — the desk's state, what refreshes when:**
| Read | Key | Refreshes |
|---|---|---|
| State now (`GET …/occupancy`) | `['space', id, 'occupancy', 'now']` | arrival; **every 30 s while visible** (`refetchInterval: 30_000`, never in background); on focus always (`refetchOnWindowFocus: 'always'`) — architecture §7's line, as built |
| Uncollected visits (page) | `['space', id, 'desk', 'uncollected', page]` | arrival; focus once stale (defaults); after any desk write |
| Unpriced visits (page) | `['space', id, 'desk', 'unpriced', page]` | the same; enabled only with `mayTypePrice` |
| Visit terms | `['space', id, 'desk', 'terms']` | arrival; defaults; after a 403 `PRICE_TYPING_NOT_ALLOWED` |
| A visit's quote | `['space', id, 'desk', 'quote', visitId]` | on the dialog's open; **every 60 s while it is open**; again before sending when its `at` is older than 4 min |
| Open check-ins (PR 2) | `['space', id, 'desk', 'checkIns', 'open']` | arrival; again whenever the state now's set of `CHECK_IN` ids changes (an effect on the ids), never polled |
| Customers search (PR 2) / list (PR 3) | `['space', id, 'desk', 'customers', query]` | paused typing (400 ms, `usePausedSearch`); `keepPreviousData` |
| A customer's file (PR 2–3) | `['space', id, 'desk', 'file', customerId]` | arrival; defaults; after any desk write |
| A statement (PR 3) | `['space', id, 'desk', 'statement', subscriptionId]` | when opened; after any desk write |

**After each write:** invalidate `['space', spaceId]` (S1), **without awaiting it** at the desk: the dialog closes
and the toast speaks from the write's own answer at once (K7); the lists follow. *Why:* on a weak connection a
toast that waits for three refetches tells the receptionist nothing for seconds. *Cost:* the list shows the old
row for a moment. *Recommend:* take it.

**S3 — the desk never retries a write by itself beyond the transport's rule.** The transport re-sends only a
keyed request (ADR 0015, `retry.ts`): check-ins, a visit's check-out, payments, a customer's creation, a
subscribe. The unkeyed writes — the override, «تسجيل دين», the write-off and its undo, a subscriber's check-out,
pricing, edit, archive, restore, the end — are sent once; a lost answer says «لم يصل الرد…» and the user decides
(findings 115, 123). *Recommend:* take it (it is the transport's rule; the plan makes it explicit and tested).

**S4 — idempotency in the web: one key per intent.**
- `shared/api/idempotency/useIntentKey.ts`: `useIntentKey(): { key: string; renew: () => void }` — a UUID
  (`crypto.randomUUID()`) made on first use and **kept until `renew()`**; `withIdempotencyKey(key):
  AxiosRequestConfig` sets `IDEMPOTENCY_KEY_HEADER` (`@masaha/shared/core`).
- **An intent** is a dialog or sheet opened for one item (one visitor's check-in, one visit's check-out, one
  payment on one item, one new customer, one subscribe) or one tap that writes without a dialog (a subscriber's
  «حضور»). The dialog's hook calls `renew()` when it opens; the key is kept across the transport's re-sends, a
  second press while pending (the submit is `aria-disabled` then), a «إعادة المحاولة» after a lost answer, and
  **an edit of the form while it stays open** (a changed amount after a lost answer must not record a second
  payment: if the first landed, the server answers it, and the toast says what was recorded — S8). A new key
  only for a new opening; after success the dialog closes.
- After a refusal (4xx) the server wrote nothing; the same key is still safe to resend.
- **The new customer and its subscription are two intents, two keys** (the sheet holds both; DI-37).
- *Why:* ADR 0015 rule 1; a key per press would record twice on a double press over a weak connection. *Cost:*
  one hook. *Recommend:* take it. **No test-only parameter:** tests read the header the fake adapter received.

**S5 — roles: what each sees, always the server's to decide.**
| Control | Owner | Reception | Server's guard |
|---|---|---|---|
| The desk, the customers, a file | ✓ | ✓ | the boundary (404 without a link) |
| Override, check-in/out, collect, «تسجيل دين», subscribe, edit, end | ✓ | ✓ | `requireCan` (403) |
| «لن يُحصَّل» and its undo | ✓ | — | `visits.writeOff` (403) |
| Archive, restore, the «مؤرشف» chip | ✓ | — | `customers.archive` (403) |
| A typed price (a visit with no rate, «مخصّص», «بدون سعر») | ✓ | where `mayTypePrice` | `prices.typeByHand` (403 `PRICE_TYPING_NOT_ALLOWED`) |
The page passes `abilities: { writeOff: boolean; archive: boolean }` from the session's link role at the space in
the URL (never the global role); price typing is `visit-terms`' `mayTypePrice` (the server's answer for the
caller). Every 403 is handled: `PRICE_TYPING_NOT_ALLOWED` refetches the terms and says «لم يعد مسموحًا
للاستقبال بكتابة سعر في هذه المساحة.»; any other 403 says «لم يعد هذا متاحًا لك في هذه المساحة.» and
invalidates `['me']` (the switcher and the navigation follow). A test per hidden control proves the server's
refusal is still worded when the control is shown by mistake (the break: the line left out). *Recommend:* take it.

**S6 — warnings are the server's, said after; the desk asks first only what it already knows.** A check-in is sent
at once; `meta.warnings` (`DESK_WARNINGS`) are said in the success toast's description, each its catalogue line
(`errors.<code>`, which #112 and earlier already worded «…، وسُجّل الحضور رغم ذلك.»), the toast `warning` when
any. Before a subscriber's check-in, a dialog only when the customer row says it already: no current
subscription, or `EXPIRED`, or `UPCOMING` (DI-14). *Why:* a second copy of the full, hours and limits rules in the
browser would drift from the server's. *Recommend:* take it.

**S7 — money in the web: agorot end to end.** Every amount the web holds is agorot (`number`); typed amounts are
read with `agorotOf` (`shared/lib`: shekels, up to two decimals, Arabic-Indic digits) and checked by the
contract's schema (`paymentSchema`, `priceVisitSchema`); shown with `priceText` (`ILS`, LTR, isolated). **The
due is always the server's** (the quote's `chargeAgorot`, an item's `balanceAgorot`, a package's
`priceAgorot`); the money block computes only the line under it — `recorded = min(received, due)` (a visit, a
fixed price), `change = received − due`, `left = due − received`, `credit = received − due` (a usage-based
subscription) — never a charge. The submit sends `recorded`; the toast reads the answer's amounts.
*Recommend:* take it.

**S8 — every line after a write is worded from the server's answer:** the toasts (amount, method, item, what
stays owed: `VisitCheckOut.payment`, `ReceivedPayment.balanceAgorot`, `NewSubscription.payments`,
`debtAgorot`), never from the form. A retry answered with the first result shows what was recorded first.
*Recommend:* take it.

**S9 — the dashboard shell gains a bottom bar slot (P1)**: `PageActionBar` (`pages/dashboard/shell/`), a portal
target like `PageHeaderSlot`, drawn below 768 px only as `fixed inset-x-0 bottom-0 z-sticky border-t
border-border bg-background px-4 py-3` with the page's one action (`Button size="lg" className="w-full"`), the
`main` padded (`pb-24 md:pb-6`) only while a page fills it, and the `Toaster` above it (§13 check 5.d). Only the
desk fills it. *Recommend:* take it.

**S10 — the desk's keyboard at speed.** From 768 px the search takes the focus on arrival (PR 2; not on a phone,
where it would raise the keyboard over the list); after a check-in or check-out started from it, it is cleared
and focused again; each dialog's first field takes the focus (the check-out: «المستلم الآن», or the typed price
when there is no rate); Enter submits; a closed dialog returns the focus to its trigger, or — the trigger gone
(a row checked out) — to the next row's «خروج», else the section's heading (DI-31). *Recommend:* take it.

**S11 — the customers list's URL** (PR 3): `q`, `status` (`UPCOMING`|`ACTIVE`|`ENDING_SOON`|`EXPIRED`|`ARCHIVED`,
the last kept only for the owner), `kind` (`PACKAGE`|`CUSTOM`|`NONE`), `payment` (`OWES`|`CREDIT`|`SETTLED`),
`page` (from 2); a value the server would refuse falls back; a change replaces the address and returns to page
1 (`useAdminSpacesFilters`' pattern). `packageId` is not offered (the design has none). *Recommend:* take it.

**S12 — the layer's end sheet full width below 768 px** (DK-024 / OW-010, settled; finding 101): `Sheet.tsx`'s
`end` and `start` sides become `w-full md:w-3/4 md:max-w-sm` and `SheetBody` gains `min-w-0`; one design-system
commit in PR 4 with its component test (`area:design-system`). *Why:* the sheet holds the busiest form of the
desk; the package sheet benefits too. *Cost:* a layer change in a feature's item (the precedent kept them apart),
reviewed as such. *Recommend:* take it (§14.9); otherwise the sheet ships at three quarters and finding 101 stays.

**S13 — the capability documents:** `desk.md` gains its *Web decisions* and *Web history* and holds the screens'
behaviour; `visits.md`, `payments.md`, `customers.md`, `subscriptions.md` each gain one *Web* line naming what
`desk` reads or writes of theirs (a link, never a copy); `occupancy.md`'s scope becomes «…, the state now, the
override and the people present on the desk». finding 98 (size) is watched: `desk.md` grows ≈ 600 words.
*Recommend:* take it.

**No rule is weakened** except architecture §3's naming rule, extended by S1 with its reason (owner's approval).

### Proposed alternatives (none applied)

- **A1 — split PR 1 in two (recommended, §14.2):** the reading counts PR 1 at ≈ 88 files (the `desk` feature's
  first slice, `occupancy`'s state now, `shared/api`'s key, the shell's bar, two catalogues, five documents), past
  the owner's ≈ 60. **PR 1a** = commits 1–4 (the key, the bar, the present list and the status, the visit's
  check-in and check-out: a working desk, ≈ 58 files); **PR 1b** = commits 5–6 (the uncollected and the
  unpriced visits, ≈ 32 files), cut from `main` once 1a merges. *Cost:* a fifth PR and its CI and review.
  The other cuts weighed and not taken: moving the subscribers' one-tap check-out into PR 1 (PR 2's search is
  what reaches a subscriber), and PR 3 split (≈ 55 files, under the bound).
- **A2 — one web feature per module** (`desk`, `visits`, `payments`, `customers`, `subscriptions`): the names
  follow architecture §3 as written; the check-out dialog, the collect dialog and the sheet move to the page
  (each reads one module and writes another), ≈ 25 more page files. Not taken (S1).
- **A3 — hide the capacity on the desk** (R2-DK-TR-001): «الحاضرون الآن 27» without «/ 40». Changes foundation §13
  screen 13 («27 / 40»), settled. Not taken; the owner's call (§14.10).
- **A4 — no money total on the uncollected card** (R2-DK-TR-002): the count only. Changes K4's title (count ·
  total). DI-3 already takes the total off for a different reason (no server sum); the owner may decide the
  total stays off even once the server answers one. Not taken as a rule.
- **A5 — «لم يدفع شيئًا» in the payment dialog too** (R2-DK-VD-003, K2 "identical"): a payment of nothing records
  nothing, so the button would only empty the field. Not taken; the block takes `none` only where paying nothing
  is an outcome (check-out, sheet).
- **A6 — warnings before the check-in, as the prototype** (`WarnDialog` for full, limits, hours): needs a read of
  the subscription's progress and the space's hours before each tap, and a second copy of the rules. Not taken
  (S6).
- **A7 — search results announced `assertive`** (R2-DK-AX-001): not taken (AX's own doubt D1); the results'
  count line is `polite`, the input `aria-controls` the results.
- **A8 — the idle limit in the web only:** not taken — the owner's revision (2026-10-24): a browser sign-out
  protects nothing.

## 6. API specs for worker B (each self-contained; none is this item's to build)

**The order the plan needs:** one worker-B item, **DESK_API** (specs **B** and **C**, ≈ 15 files), merged
**before PR 3**; **spec D**, if the owner takes it (§14.4), merged **before PR 4** (it may ride in DESK_API);
**spec A** only if the owner prefers (b) to (c) for finding 125. Each spec lists the documents it changes; the
web lines it needs (catalogue entries of a new code) are worker B's licence (workflow §9).

### The comparison for finding 125 (the owner's decision 3)

| | (a) `createdAt` on each item | (b) an allocation quote | (c) no preview **(recommended)** |
|---|---|---|---|
| What the sheet shows before saving | the parts, computed in the browser | the parts, as the server will cut them | the prior items and the total, and «يُطبَّق المستلم على المستحق من قبل أولًا» |
| Owners of the rule | two: `allocation.ts` and a web copy (drift; or `allocate` moved to `packages/shared`) | one (the server) | one (the server) |
| Requests | none more | one per typed amount (paused, 400 ms), on a weak connection | none more |
| Truth | breaks when another desk pays meanwhile | the same race (the quote is not a lock) | exact: the toast lists the parts the answer carries |
| Cost | S on the API, M on the web | S–M on the API, S on the web | none on the API |

*Why (c):* the settled K3 sheet shows the prior items and the total, never the parts; the default «المستلم
الآن» is the whole due, which pays every part, so the order matters only for a partial amount; the answer's
`payments` list then says exactly what each part paid (K4). It is finding 125's own first *Resolves when*.

### Spec A — an allocation quote (only if the owner chooses (b))
- **Route:** `GET /manage/spaces/:spaceId/customers/:customerId/allocation?amountAgorot=` · 🧾 · read without a
  lock.
- **Rule:** the customer's items that still owe, in `itemBalances`' order (`created_at`, a visit first, then id),
  each at most its balance, the 49 oldest at most, by `payments`' `allocate` — the same function the subscribe
  uses; `amountAgorot` 1–10,000,000 (`out_of_range`).
- **Answer:** `{ parts: { item: { visitId } | { subscriptionId }, amountAgorot }[], restAgorot }` — the rest is what
  the new subscription would take.
- **Tests (API lane):** the parts for an amount below, equal to and above the debts; a visit and a subscription
  made at the same instant (the visit first); 50 debts (the 49th cut); another space's customer → 404; the order
  equals a subscribe's own `payments` for the same amount (the same function).
- **Documents:** api-contract (*Customers (managed)*); `payments.md` and `desk.md` (*API decisions*, *API
  history*); finding 125 resolved.

### Spec B — the statement and the file read from one snapshot (finding 124)
- **Where:** `desk.service.ts`, `statement` and `customerFile`: their reads (`itemBalances`, the payments, the
  check-ins, the renewal; the file's states, balances, presence, unpaid visits) run inside **one read-only
  `REPEATABLE READ` transaction** (`prisma.$transaction(fn, { isolationLevel: 'RepeatableRead' })`), passing its
  `tx` to the reads that already take one. No lock; nothing else changes.
- **Rule written:** conventions §13 (or the desk's section): "a composed read whose sums and lists must agree
  (a statement, a customer's file) reads one snapshot".
- **Tests (API lane):** a statement read while a payment on its subscription commits between its first and
  last read answers a `paidAgorot` equal to the sum of its listed payments not voided, and `progress.minutesUsed`
  equal to the sum of its check-ins' minutes; the same for the file's balances and unpaid visits. The interleaving
  is made with the race helper (`apps/api/test/locks.ts`): the test holds a row lock the second read must wait
  on, commits the payment, then releases (testing §3.7: the test acts once the read is seen waiting). **Break:**
  `isolationLevel: 'ReadCommitted'` → red, recorded. If no honest interleaving can be made, worker B says so and
  proves it by that break alone (a departure for the owner).
- **Documents:** `desk.md` (*API decisions*: «A statement and a file are each read in one `REPEATABLE READ`
  snapshot. *Why:* their sums and their lists must agree (finding 124). {date}, #PRNUM»; *API history*);
  finding 124 resolved.

### Spec C — reception's session ends after 15 minutes idle (the owner's revision, 2026-10-24)
- **Who:** a session whose account holds **at least one active `RECEPTION` link, no active `OWNER` link, and is not
  `ADMIN`**, as the links read on the request say. An owner, the admin and a plain user are never idle-ended.
- **Where the idle time is kept:** the session (the refresh-token family) gains `lastActivityAt timestamptz NOT
  NULL DEFAULT now()`, set at sign-in and copied on each rotation (as the family's deadline is). The access token
  gains the claim **`sid`** (the family's id); a token without it is refused 401 as a token without
  `sessionVersion` was, and the web's refresh replaces it.
- **What renews it:** `requireAuth`, on a request by an idle-bound account, after the account's checks: when
  `now − lastActivityAt > 15 min` → the family is deleted (this device only; the session version is **not**
  raised, so the person's other devices stay) and the request answers **401 `SESSION_IDLE`**; otherwise, unless
  the route is **passive**, `lastActivityAt = now` (written only when older than 60 s, so a burst is one write).
  **Passive routes** are marked on the router: today only `GET /manage/spaces/:spaceId/occupancy` (the desk's
  state, polled every 30 s): a desk left open with no one at it ends its session.
- **The refresh:** for an idle-bound account, the same test before the rotation: past 15 min → the family deleted,
  **401 `SESSION_IDLE`**, the cookies cleared; the refresh itself renews nothing.
- **Constants:** `RECEPTION_IDLE_MINUTES = 15` in `@masaha/shared/auth`; `SESSION_IDLE` in `DOMAIN_ERROR_CODES`
  with its two catalogue lines (worker B's licence): «انتهت جلستك بعد 15 دقيقة دون نشاط. سجّل الدخول من جديد.» /
  "Your session ended after 15 minutes with no activity. Sign in again."
- **Tests (API lane, the clock port):** reception at 14:59 idle → 200 and renewed; at 15:01 → 401 `SESSION_IDLE`,
  the family gone, a second device's session untouched; the polled occupancy read every 30 s for 16 min →
  `SESSION_IDLE` on the next request; an owner (and an owner who is also reception elsewhere) idle 2 h → 200; a
  refresh after 15:01 → 401 `SESSION_IDLE` and the cookies cleared; a token without `sid` → 401; the renewal
  written at most once a minute. **Breaks:** the passive mark removed (the poll keeps the session) → red; the
  version raised (the second device ends) → red; owners included → red.
- **Documents:** `security.md` › *Tokens and cookies* (a row *Idle (reception)*) and *Authorization*
  (`requireAuth`'s check); ADR 0003 (*Revised:* 2026-10-24 — reception's session ends after 15 minutes idle, on
  the server); api-contract §1 (auth) and §6 (`SESSION_IDLE`); `auth.md` (*API decisions*, *API history*);
  `OPEN_DECISIONS.md` point 4 is the supervisor's (§4.5 gives the line).
- **Schema:** one column and its migration (worker B's), the item's one schema change.

### Spec D — subscribe from a published week or month price (glossary › Package; §14.4)
- **Request:** `subscribeSchema` gains `priceId` (a `SpacePrice` of the space with period `WEEK` or `MONTH`, no
  custom label): exactly one of `packageId`, `priceId`, `custom` (else `invalid_choice` on `packageId`).
- **Request (cont.):** with `priceId`, a `name` (1–60, as a package's), which the desk sends in the language it
  works in («شهري», «أسبوعي», or what the receptionist types) — the server stores the name it is sent and words
  nothing.
- **Rule:** the terms copied from the price: billing `FIXED`, `priceAgorot` its amount, the audience and the
  shift its own, no limits; the end `startsOn + 6` days (week) or `+ 29` days (month) — the prototype's 7 and 30
  days, both included (the owner confirms the month's 30 days, §14.4). No `reason` (nothing is typed): reception
  may use it. A price that is not the space's, has a custom label, or is another period → `invalid_choice` on
  `priceId`.
- **Tests (API lane):** reception subscribes from the month price (201, the terms copied, no `priceTyped`); a
  later price change leaves the subscription as it was; `priceId` with `packageId` → 422; an `HOUR` price → 422;
  another space's price → 422.
- **Documents:** api-contract (*Subscriptions*); `desk.md`, `subscriptions.md` (*API decisions*); data model ›
  Package's sentence then holds.

## 7. Related findings

| Finding | Folded? | Why · cost |
|---|---|---|
| 110 the desk prototype's uncollected visits disagree with the decisions | **Yes, PR 1b** (PR 1 commit 5) | the web builds the contract: auto-closed visits only, a remainder needs a phone, the write-off undone (DI-9, DI-11); resolved there. S |
| 115 a write-off and its undo carry no key | Evidence line, PR 1b | its acceptance holds "provided the desk never retries these two routes automatically": S3 and test 41 prove it |
| 123 a delayed retry of a customer edit can revert another's | **Yes, PR 3** | edit sends only the changed fields, never retried (S3); its first *Resolves when*. S |
| 124 a statement's sums and payments, two snapshots | Spec B (worker B) | resolved by DESK_API; PR 3 starts after it |
| 125 the allocation's order is not exposed | **Yes, PR 4** (decision 3, (c)) | the screen shows the allocation after the request; resolved there |
| 101 the end sheet is not full width on a phone | **Yes, PR 4, if S12** | one layer commit; else unchanged |
| 112 a key that closed a visit with no payment is not remembered | No | S4 never reuses a key across two actions, the finding's precondition; evidence line in PR 1a |
| 130 the dashboard's shells have no skip link | No | the shells' item; this item adds no shell landmark (the bar is inside `main`'s inset) |
| 132 a paged list shows no sign of the next page loading | No | the customers list (PR 3) takes `keepPreviousData` and `aria-busy` as every list does; the owner's call stays open |
| 97 the rounding rule written twice | No | the desk shows the rounding from `visit-terms`, never a rule of its own |
| 84 a person cannot work at two desks | No | unchanged |
| 87, 55 the slow routes tests | No | the known exception (§13); each PR records the times |
| 27 two dashboard chunks import each other | No, re-checked | PR 1a's manifest records whether the new `desk` chunk joins the cycle |
| **New 160** a visit's check-in cannot name its customer | Recorded, PR 2 | DK-020 built as a visit by the customer's name (DI-14) |
| **New 161** no route reads the visits of a day | Recorded, PR 1a | the log tab not built; v1-mvp plans `GET …/visits` |
| **New 162** no route names a space's staff to reception | Recorded, PR 3 | «سجّلها» and a void's «ألغاها {name}» left out |
| **New 163** a subscription's corrections have no screen | Recorded, PR 3 | the API (#106) is built; the design has none |
| **New 164** a written-off visit is listed nowhere | Recorded, PR 1b | its undo lives only in the toast (DI-29) |
| **New 165** the published prices cannot be subscribed | Recorded, PR 4, only if spec D is declined | |

## 8. Design issues (built only once the reply approves them)

Each: the mistake, where it is proven, the fix from the layer's components and tokens. **⟨report · issue⟩** marks a
point a round-2 report proves, which the web must not copy.

### PR 1 — the desk's visits
1. **The present list is named twice** ⟨R2-DK-EX · EX-001⟩. *Fix:* the section is `aria-labelledby` its `h2`
   («الحاضرون الآن» and the count); the table's `label` is «قائمة الحاضرين», which names the table, not the
   section.
2. **The uncollected card's description repeats its rows** ⟨R2-DK-EX · EX-002⟩. *Fix:* no description; each row
   says how it closed.
3. **The uncollected card's money total** has no source: the list is paged (20), its `meta` counts visits, no
   answer sums them; a page's sum would be false past 20. *Fix:* the title counts (`meta.totalRecords`) with the
   plural forms; no total (A4 asks whether it stays off once a server sum exists).
4. **«تحصيل» has no primary weight** ⟨R2-DK-UX · UX-004⟩. *Fix:* «تحصيل» `variant="primary"`; «تسجيل دين»
   `outline`; the owner's «⋯» `ghost`.
5. **«تسجيل دين» / «تسجيل دينًا»** ⟨R2-DK-CP · CP-003⟩. *Fix:* «تسجيل دين» everywhere; "Record a debt".
6. **One money act, several verbs** ⟨R2-DK-CP · CP-001, CP-006⟩. *Fix:* «استلام» for receiving money (buttons,
   toasts); «تحصيل» only on an uncollected visit's button; «غير محصّل» only for visits; a subscription's money
   «المتبقي».
7. **English "take"** ⟨R2-DK-CP · CP-004⟩. *Fix:* "Check out and receive ₪12", "Renew and receive", "Save and
   receive".
8. **The retry's promise worded two ways, one untrue** ⟨R2-DK-CP · CP-002⟩: CP-002's merged line «لم يُسجَّل شيء»
   is false after a lost answer (the first request may have landed). *Fix:* two lines, two facts — no answer
   (`network`, `timeout`): «لم يصل الرد. أعد المحاولة — لن تُسجَّل مرتين.»; a refusal (429, any 4xx): «لم يُسجَّل
   شيء.» before its reason.
9. **The write-off called irreversible** ⟨finding 110; R2-DK-CP · CP-010⟩. *Fix:* «تخرج الزيارة من «غير محصّل»
   (ومن دين زبونها إن كان لها زبون). ليست دفعة ولا حذفًا: تبقى في السجل مع السبب، ويمكن التراجع عنها من
   الإشعار.»
10. **A typed price has no reason** (data model; `priceVisitSchema`). *Fix:* «سبب السعر» (`Textarea`, required,
    1–200) under «مبلغ الزيارة (₪)», with «سعر يدوي» `info` badge; the same in «بدون سعر»'s pricing and the
    sheet's «مخصّص» (PR 4).
11. **A partial collection leaves the rest «غير محصّل» with no phone** ⟨finding 110⟩. *Fix:* the collect dialog's
    remainder line «يبقى دينًا على صاحب هذا الرقم» and the name + phone fields, required while anything stays
    and the visit has no customer (the contract's rule).
12. **«لم يدفع شيئًا» is one-way** ⟨R2-DK-UX · UX-006⟩. *Fix:* at 0 it reads «استلام المبلغ كاملًا» and
    restores the due; one place, one toggle.
13. **The debt fields jump while typing** ⟨R2-DK-UX · UX-008⟩. *Fix:* once shown in a dialog's life they stay
    (empty, not required) when the amount covers the due; required only while a remainder exists.
15. **The auto-filled amount is unexplained** ⟨R2-DK-AX · AX-002⟩. *Fix:* «المستلم الآن» `aria-describedby` a
    visually hidden «مُلئ بالمستحق؛ غيّره إن دفع غيره.»
16. **Row buttons and the bottom bar under 44 px on touch** ⟨R2-DK-AX · AX-003, AX-018, AX-019⟩. *Fix:* row
    actions take the layer's default size (`--control-height`, 44 px on touch), never `sm`; the bottom bar's
    button `size="lg"`; checked in the real run (§13).
17. **The debt dialog focuses its second field** ⟨R2-DK-AX · AX-004⟩. *Fix:* the name first, focused first.
18. **A money failure is not announced** ⟨R2-DK-AX · AX-013⟩. *Fix:* a dialog's failure is `Alert
    variant="destructive"` with `role="alert"` (the layer's `Alert` takes `role`; §13 check 5.c).
19. **The landing on the uncollected list arrives collapsed** ⟨R2-DK-UX · UX-002⟩. *Fix:* the card's id is
    `uncollected`; arriving with that hash it opens whole and takes the focus to its heading (the overview links
    there in step 12).
23. **«عرض الكل» says nothing** ⟨R2-DK-AX · AX-006⟩. *Fix:* the card shows 3 rows, then «عرض الكل ({n})»
    (`aria-expanded`); the list's pages from 20.
24. **Two row gutters and two type styles** ⟨R2-DK-VD · VD-004, VD-005⟩. *Fix:* every person or visit row `px-5
    py-3`; its how/when line `text-caption text-muted-foreground`, on the desk and in the file alike.
25. **The due figure has no weight** ⟨R2-DK-VD · VD-011⟩. *Fix:* «المستحق» line `text-heading-2`.
26. **Three money facts, overlapping words** ⟨R2-DK-CP · CP-007⟩. *Fix:* the live line says one of four:
    «يُسجَّل المبلغ كاملًا.», «الباقي للزبون {amount}», «يصبح له رصيد {amount}», «يبقى {amount} دينًا على {name}»
    (or «… على صاحب هذا الرقم» before one is typed).
27. **Destructive items look ordinary** ⟨R2-DK-VD · VD-008; R2-DK-AX · AX-016⟩. *Fix:* «لن يُحصَّل…» (and
    «أرشفة…», PR 3) `variant="destructive"`, its consequence said in the dialog it opens.
28. **Reception's unpriced close is silent** (the contract: no rate, may not type → closed unpriced). *Fix:* the
    dialog says «لا سعر لهذه الزيارة. تُغلق بدون سعر، ويحدّده المالك لاحقًا.» and asks the phone (the whole
    stays owed).
29. **The write-off's undo has no home** (finding 164): the uncollected list drops the visit, and no read lists
    written-off visits. *Fix:* the write-off's toast stays until closed (`duration: Infinity`) with «تراجع»,
    which undoes it (`DELETE …/write-off`) and says «أُعيدت الزيارة إلى «غير محصّل»».
30. **The focus is lost after a dialog opened from a menu** ⟨R2-DK-AX · AX-010⟩. *Fix:* the dialog returns the
    focus to the row's «⋯» trigger (`onCloseAutoFocus`), or, the row gone, to the card's heading.
31. **The focus is lost after a one-tap check-out** ⟨R2-DK-AX · AX-012⟩. *Fix:* S10's rule.
32. **The live status control at closed hours** (P2's «متاح خلال ساعات العمل فقط»): the web knows only the
    status. *Fix:* while the status is `CLOSED` with no override, the control is disabled with «لا تُضبط
    الحالة والمساحة مغلقة الآن.» beside it (foundation §10's reason shown); `SPACE_NOT_OPEN` from the server is
    said in the popover.
33. **A space with no capacity** has no «/ N» and no live status. *Fix:* «الحاضرون الآن {n}» without «/», the
    control reads «يظهر للزوار: بلا حالة مباشرة».
34. **The prototype's present-list detail computes a charge in the browser** (`visitCharge`). *Fix:* «حتى الآن
    {chargeNowAgorot}» from the server, or «يُحدَّد عند الخروج» when `null`.

### PR 2 — the desk's subscribers
14. **«تسجيل كزيارة» as the customer** (DK-020) has no route: a visit's check-in names no customer (finding 160).
    *Fix:* the pre-check-in dialog (no subscription, expired, not started) offers «تسجيل كزيارة» — a visit by
    the customer's name — and «تسجيل على أي حال» on the subscription (not for «بدون اشتراك»), with «اشتراك
    جديد» / «تجديد» from PR 4; its line says «تُسجَّل زيارة باسمه، ولا تُضاف إلى ملفه.»
20. **Two equal buttons on no match** ⟨R2-DK-EX · EX-003⟩. *Fix:* «تسجيل زيارة باسم «X»» primary; «زبون جديد باسم
    «X»» (PR 4) a `link` button.
21. **The payment picker ignores who is present** ⟨R2-DK-UX · UX-003⟩. *Fix:* the picker's first list (the
    customers who owe, `payment=OWES`) puts those present now first (by the state now's check-ins' customer ids).
22. **«الأقدم أولًا» across items has no route** (a payment pays one item). *Fix:* the dialog lists the
    customer's open items (unpaid visits oldest first, then owing subscriptions), the first chosen; one payment
    per submit; no «الأقدم أولًا».
35. **Switching items wipes a typed amount** ⟨R2-DK-UX · UX-009⟩. *Fix:* the amount follows the item only while
    untouched.
36. **The no-match line implies a record** ⟨R2-DK-CP · CP-012⟩. *Fix:* «زائر لمرة واحدة؟ سجّله كزيارة (لا يُنشأ
    ملف زبون).»
38. **Cards outweigh their groups** ⟨R2-DK-VD · VD-010⟩. *Fix:* the groups «حاضر الآن» and «زبائن» are `h2
    text-heading-3`; a card's name is its `CardTitle` at `h3`.
39. **A row menu does not say whose** ⟨R2-DK-AX · AX-015⟩. *Fix:* the trigger «إجراءات أخرى: {name}» and the
    menu `aria-label` the same.
40. **«مسدّد» drawn two ways** ⟨R2-DK-VD · VD-002⟩. *Fix:* one `BalanceBadge`: «عليه {n}» `warning`, «له رصيد
    {n}» `success`, «مسدّد» `neutral`.
41. **«طالب» shown where the space has no student rate** ⟨R2-DK-CP · CP-013⟩. *Fix:* one rule (`visitRates`):
    «طالب» only where the terms carry student rates.

### PR 3 — Customers and Customer details
42. **Subscription cards have no headings** ⟨R2-DK-VD · VD-009⟩. *Fix:* each card's name an `h3`; the file's
    sections `h2`.
43. **The file's tabs promise what the API does not hold** (a customer's paid visits; their attendance across
    subscriptions) ⟨and R2-DK-VD · VD-001's plain table⟩. *Fix:* no tabs: the unpaid visits, then the
    subscriptions, each with «عرض الكشف» (`aria-expanded`) opening its statement in the card: its check-ins (a
    list: day, in, out, duration — rows that stack below 768 px) and its payments (amount with the method under
    it, VD-006; a voided one struck through with a visible «ملغاة» badge and «أُلغيت: {reason}», AX-017,
    CP-009 without a name, finding 162).
44. **A subscription's arrears need a round trip** ⟨R2-DK-UX · UX-005⟩. *Fix:* «استلام المتبقي» on a card that
    owes, opening the payment with that item chosen.
46. **«أرشفة» looks ordinary** ⟨R2-DK-VD · VD-008⟩. *Fix:* «أرشفة…» destructive; settled → at once with
    «تراجع» (restore); owing → `AlertDialog` naming the debt (DK-014, P9).
47. **Archiving a present customer** fails with no word. *Fix:* `MEMBER_ALREADY_CHECKED_IN` → «{name} حاضر الآن؛
    سجّل خروجه قبل الأرشفة.»
48. **«سجّلها» (who recorded a payment)** has no name source for reception (finding 162). *Fix:* not shown.
49. **The WhatsApp reminder** reads the owner's settings (reception cannot) and is finance's (step 11). *Fix:* not
    built here.

### PR 4 — the subscription sheet
37. **A new customer saved, the subscription refused** (two requests): the prototype's half state assumed the
    payment apart, which the API makes atomic. *Fix:* the sheet says «أُضيف {name} إلى الزبائن؛ لم يُحفظ
    الاشتراك.» with the reason, keeps every field, and «حفظ الاشتراك» sends the subscribe alone (its own key);
    closing then toasts «{name} في الزبائن بدون اشتراك.» ⟨R2-DK-UX · UX-001's silent close⟩.
45. **«بلا حدّ» wears a warning icon** ⟨R2-DK-VD · VD-007⟩. *Fix:* a plain `text-caption text-muted-foreground`
    line.
50. **A package's price edited in the sheet** (the prototype's «تعديل السعر»): a package's terms are copied.
    *Fix:* no price field on a package; another price is «مخصّص».
51. **«منشورة للزوار»** lists the published prices, which the API cannot subscribe from (spec D). *Fix:* with spec
    D, the week and month prices first under «منشورة للزوار»; without it, only «باقات المساحة» (the offered
    packages) and «مخصّص», finding 165.
52. **«مخصّص» lacks what the contract requires:** the audience («لمن»), a name (required, 1–60), the reason.
    *Fix:* «لمن» chips (الجميع · الطلاب), the name prefilled «مخصّص» / "Custom" (editable), «سبب السعر»
    required; billing «سعر ثابت · بالساعة · باليوم» (the contract's three), the limits as four optional numbers
    («مجموع الأيام», «أيام بالأسبوع», «ساعات باليوم», «مجموع الساعات»); «ملاحظة» dropped (no field).
53. **The phone demanded of a known customer** to leave a debt: the customer is already the debtor. *Fix:* the
    phone is asked only of a new customer (required while anything stays owed, K2); a known customer without
    one gets the line «لا رقم جوال لهذا الزبون؛ أضفه من «تعديل البيانات» لتذكيره بالدين.», not blocking.

**Not built, the reports' own improvements:** A3 (TR-001), A4 (TR-002), A5 (VD-003), A7 (AX-001). **Not
applicable to this item:** R2-DK-UX-007, R2-DK-EX-007 (the log, finding 161), R2-DK-EX-005, R2-DK-EX-006,
R2-DK-TR-005, R2-DK-VD-006's «دفعاتي اليوم», R2-DK-VD-012, R2-DK-CP-011 (step 9), R2-DK-TR-004 (K8 as built),
R2-DK-AX-007 (no log date picker); refuted in their browser pass: AX-008, AX-011, AX-020, VD-013. Decisions in
doubt raised by the reports (K7 vs P8; K4 handover) stay as settled.

## 9. The files

A: added · M: modified · R: moved. Paths under `apps/web/src/` unless they start with `docs/`, `apps/` or
`packages/`. Every test sits beside its file. The counts are estimates; `git diff --stat` decides.

### PR 1 (with A1: 1a = commits 1–4, 1b = commits 5–6)
- **Commit 1** `shared/api/` — A `idempotency/useIntentKey.ts` (+ `.component.test.tsx`), A
  `idempotency/withIdempotencyKey.ts` (+ `.unit.test.ts`); M `client/request.ts` (`postWithMeta`) and
  `client/request.unit.test.ts` (or its existing test file); M `index.ts`. Docs: `architecture.md` §7. (≈ 8)
- **Commit 2** `pages/dashboard/shell/` — A `PageActionBar.tsx`, A `PageActionSlot.ts`; M `DashboardLayout.tsx`
  and its component test (A if none). Docs: `architecture.md` §2. (≈ 5)
- **Commit 3** `features/occupancy/` — M `repository/occupancyRepository.ts` (+ its unit test, A if none), M
  `hooks/queryKeys.ts`; A `hooks/now/useStateNowQuery.ts` (+ test), `hooks/now/usePresentList.ts` (+ test), A
  `hooks/status/useLiveStatusControl.ts` (+ test), `hooks/status/useSetOverride.ts`, `useClearOverride.ts`; A
  `services/overrideLeft.ts` (+ unit), `services/stayDuration.ts` (+ unit); A `types/PresentRowView.ts`; A
  `components/PresentList.tsx` (+ test), `components/LiveStatusControl.tsx` (+ test); M `index.ts`. Copy
  `{english,arabic}/occupancy.ts` A, `index.ts` M ×2. Docs `occupancy.md`, `architecture.md` §7. (≈ 26)
- **Commit 4** `features/desk/` (new) — A `index.ts`; `repository/deskRepository.ts` (+ unit); `hooks/queryKeys.ts`;
  `hooks/useDeskWrite.ts` (the invalidation and the refusal reading every write shares); `hooks/terms/
  useVisitTermsQuery.ts`; `hooks/check-in/useCheckInVisit.ts`, `useVisitDialog.ts` (+ test);
  `hooks/check-out/useQuoteQuery.ts`, `useCheckOutVisit.ts`, `useCheckOutDialog.ts` (+ test);
  `hooks/money/useMoneyBlock.ts` (+ test); `services/moneyOf.ts` (+ unit), `visitRates.ts` (+ unit),
  `currentShift.ts` (+ unit), `quoteAge.ts` (+ unit), `warningLines.ts` (+ unit), `deskRefusal.ts` (+ unit);
  `types/MoneyBlockView.ts`, `DeskAbilities.ts`; `components/visit/VisitDialog.tsx` (+ test),
  `components/check-out/CheckOutDialog.tsx` (+ test), `CheckOutAction.tsx`, `components/money/MoneyBlock.tsx`,
  `components/toast/deskToasts.tsx`. `pages/dashboard/` — A `space/desk/DeskPage.tsx`,
  `space/desk/SwitchStaffButton.tsx`, `space/desk/useSwitchStaff.ts` (+ test); M `routes.tsx`,
  `routes.component.test.tsx`. Copy `{english,arabic}/desk.ts` A, `index.ts` M ×2. Docs `desk.md`, `visits.md`,
  `architecture.md` §3, `overview.md`, `docs/README.md`, finding 161 A, findings `README.md` M. (≈ 45)
- **Commit 5** `features/desk/` — A `hooks/uncollected/useUncollectedQuery.ts`, `useUncollectedCard.ts` (+ test),
  `hooks/collect/useReceivePayment.ts`, `useCollectDialog.ts` (+ test), `hooks/debt/useLeaveToCustomer.ts`,
  `useDebtDialog.ts` (+ test), `hooks/write-off/useWriteOff.ts`, `useUndoWriteOff.ts`, `useWriteOffDialog.ts`
  (+ test), `services/dayWord.ts` (+ unit); `components/uncollected/UncollectedCard.tsx` (+ test),
  `UncollectedRow.tsx`, `components/collect/CollectDialog.tsx`, `components/debt/DebtDialog.tsx`,
  `components/write-off/WriteOffDialog.tsx`; M `repository/deskRepository.ts` (+ test), `hooks/queryKeys.ts`,
  `index.ts`; M `DeskPage.tsx`; copy `desk.ts` ×2. Docs `desk.md`, `payments.md`, findings 110 (resolved), 115,
  112 (evidence), 164 A, `README.md`. (≈ 27)
- **Commit 6** `features/desk/` — A `hooks/unpriced/useUnpricedQuery.ts`, `useUnpricedCard.ts` (+ test),
  `usePriceVisit.ts`, `usePriceDialog.ts` (+ test); `components/unpriced/UnpricedCard.tsx`, `PriceDialog.tsx`; M
  repository (+ test), keys, `index.ts`, `DeskPage.tsx`; copy ×2. Docs `desk.md`, `visits.md`. (≈ 14)

### PR 2
- **Commit 1** `features/occupancy/` — A `hooks/present/usePresentMatches.ts` (+ test), `services/
  matchesPerson.ts` (+ unit), `components/PresentMatches.tsx`; M `index.ts`; copy `occupancy.ts` ×2. (≈ 8)
- **Commit 2** `features/desk/` — A `hooks/search/useCustomersSearchQuery.ts`, `useDeskSearch.ts` (+ test);
  `hooks/card/useCustomerCard.ts` (+ test); `services/balanceView.ts` (+ unit), `statusView.ts` (+ unit);
  `components/search/DeskSearch.tsx` (+ test), `components/card/CustomerCard.tsx`, `BalanceBadge.tsx`; M
  repository (+ test), keys, `index.ts`; `pages/dashboard/space/desk/DeskPage.tsx` M; copy `desk.ts` ×2. Docs
  `desk.md`, `customers.md`; finding 160 A. (≈ 20)
- **Commit 3** `features/desk/` — A `hooks/subscriber/useCheckInSubscriber.ts`, `useSubscriberCheckIn.ts`
  (+ test), `useCheckOutSubscriber.ts` (+ test), `useOpenCheckInsQuery.ts`, `services/progressLines.ts`
  (+ unit); `components/subscriber/
  PreCheckInDialog.tsx` (+ test); M `CheckOutAction.tsx`, `CustomerCard.tsx`, repository (+ test), keys; M
  `occupancy`'s `PresentList.tsx` (the usage cell slot); copy ×2. Docs `desk.md`, `subscriptions.md`. (≈ 14)
- **Commit 4** `features/desk/` — A `hooks/pay/useCustomerFileQuery.ts`, `usePayDialog.ts` (+ test),
  `services/openItems.ts` (+ unit); `components/pay/PayDialog.tsx` (+ test); M `CustomerCard.tsx`, repository,
  keys, `index.ts`, `DeskPage.tsx` (the page action «استلام دفعة»); copy ×2. Docs `desk.md`, `payments.md`. (≈ 12)

### PR 3
- **Commit 1** `features/desk/` — A `hooks/customers/useCustomersFilters.ts` (+ test), `useCustomersList.ts`
  (+ test), `services/customersQueryOf.ts` (+ unit); `components/customers/CustomersList.tsx` (+ test),
  `CustomersFilters.tsx`; M repository, keys, `index.ts`. `pages/dashboard/` — A `space/customers/
  CustomersPage.tsx`; M `navigation.ts` (`spaceCustomerPath`), `routes.tsx`, `routes.component.test.tsx`. Copy
  ×2. Docs `customers.md`, `desk.md`. (≈ 17)
- **Commit 2** `features/desk/` — A `hooks/file/useCustomerFile.ts` (+ test), `useFileTitle.ts`;
  `services/termsLine.ts` (+ unit), `payStatus.ts` (+ unit) (`progressLines` is PR 2's);
  `components/file/CustomerFile.tsx` (+ test), `FileHeader.tsx`, `SubscriptionCard.tsx`, `UnpaidVisits.tsx`; M
  `index.ts`. `pages/dashboard/space/customers/CustomerPage.tsx` A; M `routes.tsx`, routes test. Copy ×2. Docs
  `desk.md`, `subscriptions.md`. (≈ 17)
- **Commit 3** `features/desk/` — A `hooks/edit/useEditCustomer.ts`, `useEditDialog.ts` (+ test),
  `hooks/archive/useArchive.ts`, `useRestore.ts`, `useArchiveFlow.ts` (+ test); `components/edit/
  EditCustomerDialog.tsx`, `components/archive/ArchiveDialog.tsx`, `components/menu/CustomerMenu.tsx`
  (+ test); M repository (+ test), card, header, list; copy ×2. Docs `customers.md`, finding 123 resolved. (≈ 14)
- **Commit 4** `features/desk/` — A `hooks/statement/useStatementQuery.ts`, `useStatement.ts` (+ test),
  `hooks/end/useEndSubscription.ts`, `useEndDialog.ts` (+ test); `components/statement/Statement.tsx`
  (+ test), `components/end/EndDialog.tsx`; M `SubscriptionCard.tsx`, repository (+ test), keys; copy ×2. Docs
  `desk.md`, `subscriptions.md`; findings 124 (resolved by DESK_API, the line checked), 162, 163 A. (≈ 13)
- **Commit 5** `shared/session/` — M `store.ts` (`endedBy`), `services/refresh.ts` (+ their tests); the sign-in
  page `pages/site/auth/…SignInPage.tsx` M (+ its test) — the file named by `git grep -n "SignInForm"
  apps/web/src/pages/site`. Docs `auth.md`, `architecture.md` §4. (≈ 6)

### PR 4
- **Commit 1 (S12, if approved)** `shared/design-system/components/overlays/Sheet/Sheet.tsx` and its component
  test M; `foundation.md` §12 (Sheet's row). (≈ 3)
- **Commit 2** `features/packages/` — A `hooks/offered/useOfferedPackages.ts` (+ test); M `index.ts`. Docs
  `packages.md`. (≈ 4)
- **Commit 3** `features/desk/` — A `hooks/sheet/useSubscriptionSheet.ts` (+ test), `useSheetForm.ts`,
  `useCreateCustomer.ts`, `useSubscribe.ts`, `services/sheetRequest.ts` (+ unit), `services/endOf.ts`
  (+ unit), `services/packageLine.ts` (+ unit); `types/SheetEntry.ts`, `PackageChoice.ts`; `components/sheet/
  SubscriptionSheet.tsx` (+ test), `PackageOptions.tsx`, `CustomTerms.tsx`, `PriorDebts.tsx`; M repository
  (+ test), keys, `index.ts`, `DeskSearch.tsx`, `CustomerCard.tsx`, `CustomerMenu.tsx`, `CustomersList.tsx`.
  `pages/dashboard/space/` — M `desk/DeskPage.tsx`, `customers/CustomersPage.tsx`, `customers/CustomerPage.tsx`
  (each passes the packages and the shifts). Copy ×2. Docs `desk.md`, `customers.md`; finding 125 resolved. (≈ 28)
- **Commit 4** `features/desk/` — M `useSubscriptionSheet.ts` (+ test: renewal), `PriorDebts.tsx`,
  `sheetRequest.ts` (+ unit); copy ×2. Docs `desk.md`, `subscriptions.md`; finding 165 if spec D is declined.
  (≈ 8)

### Shared with the other open items
- **Worker A's public fix PR** (before this item): `pages/site/*`, `features/directory`, `shared/routing/states`
  (RetryState), `shared/copy/*/site.ts`, `directory.ts`. PR 1–4 touch none of them; PR 3 commit 5 touches the
  sign-in page only. Its documents (`overview.md`, `docs/README.md`, `architecture.md`) are shared lines.
- **Worker B (step 9, DESK_API, ANNOUNCEMENTS 2–4):** no code file is shared — this item touches no
  `apps/api`, no `packages/shared`, and no `shared/copy/*/errors.ts` (B adds `SESSION_IDLE` there). Step 9 will
  change `packages/shared/src/payments` and may add `features/payments` on the web: **if B's step 9 PR changes
  a type this item reads (`ItemPayment`, `ReceivedPayment`, `CustomerFile`) before a PR here is pushed → stop and
  ask.** Shared documents, each side its own part: `desk.md`, `payments.md`, `subscriptions.md`,
  `customers.md`, `auth.md` (*API* vs *Web* parts), `overview.md`, the findings index.
- **ANNOUNCEMENTS PRs 2–4 (B; screens 18):** their web screen may touch `pages/dashboard/routes.tsx` and
  `navigation.ts` — a conflict there is a text conflict; each keeps its own entries.

## 10. What is built — interfaces, words, states

Words: Arabic, then English. A counted line gives `arabicPlural` all six forms and `englishPlural` `one`/`other`
(`shared/copy/plural.ts`); every Arabic section `satisfies Catalogue['<section>']`. A value in a sentence is
isolated (`isolate`); a customer's or visitor's name with `lineParts` when the line names it (its language may
differ). Amounts (`priceText`), times (`HH:MM`, `clockOf`), phones and durations are LTR. **The owner approves
every Arabic line below** (§14.7). Lines already in the catalogue are reused, never copied: `errors.<code>`
(every warning and refusal the contract names, `CLOSURE_IN_FORCE` included since #112), `status.retry`,
`terms.liveStatuses` («متاح» · «ممتلئ» · «مغلق الآن»).

**Every dialog's states:** open → its fields (the first focused, S10); sending → the submit `loading` and
`aria-disabled`, the fields `disabled`; refused → the dialog stays, every value kept, the failure an `Alert
variant="destructive" role="alert"` above the footer (DI-18): «لم يُسجَّل شيء.» + the reason (`useRefusalView`,
the dialog's `refusals` lines) with the reference when no code; **no answer** (`network`, `timeout`) → the lost
line (DI-8) and «إعادة المحاولة» sending again **with the same key** (S4); 429 → the countdown (`useRefusalView`),
the submit blocked until it ends; a 403 → S5's lines; done → closes, the toast (K7) from the answer (S8).
**Every list's states:** loading (skeletons: `DataTable loading` / three `Skeleton` rows), failed (destructive
`Alert` with the reference and «إعادة المحاولة»), failed again over shown rows (a muted line «تعذّر التحديث؛
تظهر آخر قائمة.», the rows kept), empty (its own `EmptyState`), offline (`network` → `errors.network`, the same
retry).

### PR 1 · Commit 1 — `feat(api): keep one idempotency key per intent`
- `withIdempotencyKey(key: string): AxiosRequestConfig` → `{ headers: { [IDEMPOTENCY_KEY_HEADER]: key } }`.
- `useIntentKey(): { key: string; renew: () => void }` — `useState(() => crypto.randomUUID())`; `renew` sets a new
  one; the same `key` across renders until `renew`.
- `api.postWithMeta<T, M>(url, body, config): Promise<{ data: T; meta: M | undefined }>` — the envelope's `data`
  and its optional `meta` (a check-in's and a subscribe's `meta.warnings`, absent without warnings; `getPage`
  rejects an answer without `meta`, so it does not fit).
- Docs: `architecture.md` §7 › *Retries*: «**One key per intent:** a dialog or sheet opened for one item, or one
  tap that writes without one, holds one `Idempotency-Key` (`useIntentKey`), kept across the transport's
  re-sends, a second press, a retry after a lost answer and an edit of the form; a new opening is a new key
  ({date}, #PRNUM).» No words.

### PR 1 · Commit 2 — `feat(dashboard): add the page's bottom action bar`
- `PageActionSlot` (a context, like `PageHeaderSlot`, holding the bar's element and a `setFilled(boolean)`);
  `DashboardLayout` renders, after `<main>`, the bar's `div` — `fixed inset-x-0 bottom-0 z-sticky border-t
  border-border bg-background px-4 py-3 md:hidden`, always in the tree (the portal's target) but `hidden` until a
  page fills it (`filled`, set by `PageActionBar` on mount and cleared on unmount), and then adds `pb-24 md:pb-6` to
  `main` so nothing hides under it.
- `PageActionBar({ children })` — a portal into the slot, below 768 px only (the page's top-bar action stays from
  768 px).
- Docs: `architecture.md` §2 › *The dashboard's shell*: «Below 768 px a page may put its one all-day action in a
  bar fixed at the foot (`PageActionBar`, P1); only the desk does ({date}, #PRNUM).»

### PR 1 · Commit 3 — `feat(occupancy): show the desk who is present`
- **Repository:** `stateNow(spaceId): Promise<SpaceOccupancyNow>` (`GET …/occupancy`); `setOverride(spaceId,
  body: SetStatusOverrideRequest)`, `clearOverride(spaceId)` → `SpaceOccupancyNow`. Keys `occupancyKeys.now(id)
  = ['space', id, 'occupancy', 'now']`.
- **`useStateNowQuery(spaceId)`**: `refetchInterval: 30_000`, `refetchIntervalInBackground: false`,
  `refetchOnWindowFocus: 'always'` (S2). The override's answer replaces the query's data (`setQueryData`).
- **`usePresentList(spaceId, { now })`** → `{ heading: { title, count }; label; state: 'loading' | 'failed' |
  'empty' | 'ready'; rows: PresentRowView[]; summary; failure; refreshFailure; empty }` with `PresentRowView = {
  key: string /* 'VISIT-12' */; person: PresentPerson; name: string; kind: string; since: string; duration:
  string; detail: string | null }` — `detail`: «حتى الآن {amount}» from `chargeNowAgorot`, «يُحدَّد عند الخروج»
  when `null` (DI-34); for a check-in, `null` until PR 2's usage slot. `now` ticks every 60 s in the component
  (`stayDuration(since, now)`: whole minutes → «{h} س {m} د»).
- **`useLiveStatusControl(spaceId)`** → `{ trigger: { label: string; name: string; tone: 'success' | 'warning' |
  'neutral'; disabled: boolean; reason: string | null }; panel: { title; states: { value: LiveStatus; label }[];
  state; choose; forLabel; durations: { value: OverrideDuration; label; run }[]; back: { label; run } | null; now:
  string | null; note: string; failure: FormFailureView | null; busy: boolean } }` — the shown state is
  `override.state` while one is in force, else `status`; `disabled` with `reason` while `status === 'CLOSED'`
  and no override (DI-32); `SPACE_NOT_OPEN` → its `errors` line in `failure`; done → the popover closes, toast
  «تظهر المساحة «{state}» للزوار». `overrideLeft(until, now)` → «1:24» (h:mm, ceiling minutes), ticking each
  30 s.
- **Components:** `LiveStatusControl({ spaceId })` (exported) — `Popover`; its trigger an outline `Button size="sm"`
  skinned by tone (`border-success bg-success-subtle text-success-subtle-foreground` / warning / `border-border
  bg-secondary text-secondary-foreground`), its label the full line from 768 px and the state word alone below
  (`useMediaQuery`), its `aria-label` always the full name; the panel `w-72`: the states `ToggleGroup
  type="single"`, the durations a 2 × 2 grid of outline buttons, «العودة للحالة التلقائية» (ghost, with
  `XIcon`) while an override is in force, the note; the reason beside a disabled trigger (`text-caption
  text-muted-foreground`). `PresentList({ spaceId, action, usage? })` (exported) — `<section
  aria-labelledby>`: an `h2` (`text-heading-3`) «الحاضرون الآن» and the count (`<span dir="ltr">27 / 40</span>`,
  or «27» with no capacity, DI-33); `DataTable` (`@shared/design-system/data`) `label="قائمة الحاضرين"` (DI-1),
  columns name · kind (`Badge neutral`) · since · duration · detail (`hidden lg:table-cell`) · actions
  (`action(person)`), `renderCard` below 768 px (name, kind, since · duration, detail, the action at the end),
  `summary` «{subscribers} · {visits}», `loading`, `empty`.
- **Words** (`occupancy`, new section):

| key | ar | en |
|---|---|---|
| `present.title` / `present.table` | الحاضرون الآن / قائمة الحاضرين | Present now / People present |
| `present.columns` | name «الاسم» · kind «النوع» · since «منذ» · duration «المدة» · detail «الاستخدام» · actions «إجراءات» | Name · Type · Since · Duration · Usage · Actions |
| `present.kinds` | VISIT «زيارة» · CHECK_IN «اشتراك» | Visit · Subscription |
| `present.soFar({amount})` / `present.atCheckOut` | حتى الآن {amount} / يُحدَّد عند الخروج | {amount} so far / Set at check-out |
| `present.since({time})` / `present.duration({hours, minutes})` / `present.minutes({minutes})` | منذ {time} / {hours} س {minutes} د / {minutes} د | Since {time} / {hours}h {minutes}m / {minutes}m |
| `present.subscribers(n)` | zero «لا مشتركين» · one «مشترك واحد» · two «مشتركان» · few «{n} مشتركين» · many «{n} مشتركًا» · other «{n} مشترك» | one «1 subscriber» · other «{n} subscribers» |
| `present.visits(n)` | zero «لا زيارات» · one «زيارة واحدة» · two «زيارتان» · few «{n} زيارات» · many «{n} زيارة» · other «{n} زيارة» | one «1 visit» · other «{n} visits» |
| `present.summary({subscribers, visits})` | {subscribers} · {visits} | {subscribers} · {visits} |
| `present.empty.title` / `.text` | لا أحد حاضر الآن / سجّل زيارة لأول من يصل. | No one is here right now / Check in a visit for the first arrival. |
| `present.loadFailed` / `present.refreshFailed` | تعذّر تحميل الحاضرين / تعذّر التحديث؛ تظهر آخر قائمة. | We couldn’t load who is present / We couldn’t refresh; showing the last list. |
| `status.line({state})` / `status.manual({state, left})` | يظهر للزوار: {state} / يظهر للزوار: {state} يدويًا · {left} | Visitors see: {state} / Visitors see: {state}, set by hand · {left} |
| `status.name({state})` / `status.manualName({state, left})` | يظهر للزوار: {state} — غيّرها / يظهر للزوار: {state} يدويًا، {left} متبقية — غيّرها | Visitors see: {state} — change it / Visitors see: {state}, set by hand, {left} left — change it |
| `status.none` | بلا حالة مباشرة | No live status |
| `override.title` / `override.for` | الحالة التي يراها الزوار / لمدة | What visitors see / For |
| `override.durations` | MINUTES_30 «30 د» · HOUR_1 «ساعة» · HOURS_2 «ساعتان» · UNTIL_CLOSING «حتى الإغلاق» | 30 min · 1 hour · 2 hours · Until closing |
| `override.now({state, left})` | الآن: {state} يدويًا · {left} متبقية | Now: {state}, set by hand · {left} left |
| `override.back` / `override.note` / `override.replaces` | العودة للحالة التلقائية / بعدها تعود الحالة تلقائيًا حسب الحضور. / يحلّ محل الضبط الحالي. | Back to the automatic status / Then the status follows attendance again. / It replaces the current setting. |
| `override.closed` | لا تُضبط الحالة والمساحة مغلقة الآن. | The status can’t be set while the space is closed. |
| `override.done({state})` / `override.cleared` / `override.failed` | تظهر المساحة «{state}» للزوار / عادت الحالة تلقائية / تعذّر ضبط الحالة | Visitors now see “{state}” / The status is automatic again / We couldn’t set the status |

- **Docs:** `occupancy.md` — header scope («…; the web feature `features/occupancy`: the capacity's hooks, and the
  desk's state now, override and people present»); *Who uses it* (the desk, on the web); *Behaviour* «**The state
  now on the web**» (polled every 30 s while visible, on focus always; the control; the list); *Web decisions*:
  S2's first row, DI-1, DI-32, DI-33, DI-34; code map; *Web history*. `architecture.md` §7 › *Polling*'s desk line
  gains «(built: `occupancy`'s state now, {date}, #PRNUM)».

### PR 1 · Commit 4 — `feat(desk): check visitors in and out at the desk`
- **Repository** `DeskRepository` (`createDeskRepository()`): `terms(spaceId): VisitTerms`; `checkInVisit(spaceId,
  body: CheckInVisitRequest, key): { data: DeskVisit; meta: { warnings: DeskWarning[] } | undefined }`
  (`postWithMeta`); `quote(spaceId, visitId): QuotedVisit`; `checkOutVisit(spaceId, visitId, body:
  CheckOutVisitRequest, key): VisitCheckOut`. Paths `/manage/spaces/{id}/visit-terms`, `…/visits`,
  `…/visits/{visitId}`, `…/visits/{visitId}/check-out`.
- **Keys** `deskKeys`: `all(id) = ['space', id, 'desk']`; `terms(id)`, `quote(id, visitId)`, then PR 1b–4's.
- **`useDeskWrite()`** → `{ settle: (spaceId) => void /* invalidates ['space', spaceId], not awaited (S2) */;
  linkEnded: (error) => void /* a 403 with no code or a 404 → invalidate ['me'] */ }`.
- **`services/visitRates.ts`**: `ratesFor(terms, { shiftId, student }): Rates` — the terms' row of the shift (else
  the no-shift row), `student` only where that row's `student` is not `null`; `offersStudent(terms): boolean`
  (DI-41's one rule). **`currentShift(shifts, now)`**: the shift whose range holds Gaza's minute now
  (`gazaClockOf`), else none.
- **`useVisitDialog({ spaceId, shifts, name })`** → `{ open; setOpen; title; rate: string /* the line, by
  ratesFor */; full: boolean /* status FULL, from the page */; fields: name, student (when offered), shift
  (options, current chosen; when the space has shifts); submit; failure; busy }` — `useServerForm` over
  `checkInVisitSchema`; the key from `useIntentKey`, renewed on open. Done → toast `toastCheckedIn(name,
  warnings)` and `settle`.
- **`useQuoteQuery(spaceId, visitId)`**: `refetchInterval: 60_000` while the dialog is open; `quoteAge(at, now) >
  4 min` before sending → `refetch()`; a changed `chargeAgorot` stops the send and shows `quoteChanged`.
- **`useMoneyBlock({ due, open, none, owes })`** → `MoneyBlockView = { due: { label; amount }; received: { label;
  text; change; error; description }; method: { label; value: 'CASH' | 'TRANSFER'; options; choose } | null /* only
  while received > 0 */; line: string; toggle: { label; run } | null; recorded: number; left: number; change:
  number; credit: number; untouched: boolean }` — `moneyOf(due, received, open)` (S7); `received` starts at the
  due (untouched) and follows it while untouched; `toggle` «لم يدفع شيئًا» ↔ «استلام المبلغ كاملًا» (DI-12),
  only with `none`.
- **`useCheckOutDialog({ spaceId, person, terms })`** → `{ title; kind; rows: { label; value }[] /* in, out (the
  quote's at), duration */; calc: string[] /* «مدة محسوبة {time}», the rounding, the cap — from the quote and the
  terms, no arithmetic */; money: MoneyBlockView; typed: { amount; reason; badge; help } | null /* no rate and
  mayTypePrice */; unpriced: string | null /* no rate, may not type (DI-28) */; debt: { name; phone; shown } /*
  shown once a remainder appeared (DI-13); required while left > 0 and the visit has no customer */; submit: {
  label; run; busy; blocked }; failure }` — sends `{ checkedOutAt: quote.at, payment: recorded > 0 ? { amountAgorot:
  recorded, method } : null, phone?, customerName?, charge?: { amountAgorot, reason } }`, checked by
  `checkOutVisitSchema`; refusals: `VISIT_ALREADY_CLOSED`, `PAYMENT_EXCEEDS_DUE` (refetch the quote),
  `VISIT_HAS_CUSTOMER` (on the phone), `out_of_range` on `checkedOutAt` (refetch the quote, `quoteChanged`),
  `PRICE_TYPING_NOT_ALLOWED` (refetch the terms), 409 no code (`conflict` line). Done → `toastCheckedOut` from
  `VisitCheckOut` and `settle`.
- **Components:** `VisitDialog`, `CheckOutDialog`, `MoneyBlock` (a `rounded-lg bg-muted p-3` group, `role="group"`
  named «الدفع»: the calc lines `text-body-sm`, «المستحق {amount}» `text-heading-2` (DI-25), «المستلم الآن (₪)»
  `Input dir="ltr" inputMode="decimal"` with its description (DI-15), the method `ToggleGroup`, the line `<p
  aria-live="polite">`, the debt fields as children, the toggle an outline button), `CheckOutAction({ spaceId,
  person, terms })` (exported: «خروج» `Button variant="outline"` default size (DI-16), `aria-label` «خروج
  {name}»; a visit opens `CheckOutDialog`; a check-in from PR 2), `deskToasts.tsx` (`toastCheckedIn`,
  `toastCheckedOut`, …, worded with `currentCopy()` when they land; a warning toast when `meta.warnings`).
- **`DeskPage`** (`pages/dashboard/space/desk/`): `PageHeader` with, from 768 px, `LiveStatusControl`,
  `SwitchStaffButton` (outline) and «تسجيل زيارة» (primary, last); below 768 px the header holds the control
  (short) and a «⋯» `DropdownMenu` («تبديل الموظف»), and `PageActionBar` holds «تسجيل زيارة» (`size="lg"
  w-full`, DI-16). Body: `flex flex-col gap-6 xl:grid xl:grid-cols-12 xl:items-start`: the uncollected card
  (1b: `xl:order-last xl:col-span-4`), then `PresentList` (`xl:col-span-8`) with `action={(p) => <CheckOutAction
  …/>}`. The abilities from the session's link (S5). `key={spaceId}` around the body, as Packages does.
- **`useSwitchStaff(spaceId)`** → `{ label; run; busy; failure }` — `useSignOut()`, then `navigate(SIGN_IN_PATH +
  '?next=' + encodeURIComponent(spaceDeskPath(spaceId)), { replace: true })`; a failure stays a toast with
  «إعادة المحاولة» (the session is the server's, architecture §4).
- **Routes:** `SPACE_PAGES.desk` → `DeskPage`.
- **Words** (`desk`, new section):

| key | ar | en |
|---|---|---|
| `actions.checkIn` / `actions.switchStaff` / `actions.more` | تسجيل زيارة / تبديل الموظف / إجراءات أخرى | Check in a visit / Switch staff / More actions |
| `switchStaff.failed` | تعذّر الخروج من الحساب؛ أعد المحاولة. | We couldn’t sign out; try again. |
| `visit.title` / `visit.noRecord` | تسجيل زيارة / لا يُنشأ ملف زبون. | Check in a visit / No customer file is created. |
| `visit.rate.hour({hour})` / `.hourCapped({hour, day})` / `.day({day})` / `.none` | تُحسب {hour} للساعة. / تُحسب {hour} للساعة، حتى {day}. / تُحسب بسعر اليوم {day}. / لا سعر منشورًا؛ يُكتب المبلغ عند الخروج. | Charged {hour} an hour. / Charged {hour} an hour, up to {day}. / Charged at the day price, {day}. / No published price; the amount is entered at check-out. |
| `visit.name` / `.student` / `.shift` / `.optional` / `.noShift` | الاسم / طالب / الوردية / اختياري / بدون وردية | Name / Student / Shift / Optional / No shift |
| `visit.full` | المساحة ممتلئة؛ يمكنك التسجيل على أي حال، وتبقى حالتها للزوار «ممتلئ». | The space is full; you can still check in, and visitors keep seeing “Full”. |
| `visit.submit` / `.submitAnyway` / `.failed` | تسجيل الزيارة / تسجيل على أي حال / تعذّر تسجيل الزيارة | Check in / Check in anyway / We couldn’t check the visit in |
| `visit.done({name})` | سُجّلت زيارة {name} | {name} checked in |
| `checkOut.title({name})` / `.visit` / `.studentVisit` | تسجيل خروج · {name} / زيارة / زيارة · طالب | Check out · {name} / Visit / Visit · student |
| `checkOut.rows` | in «الدخول» · out «الخروج» · duration «المدة» | In · Out · Duration |
| `checkOut.billed({time})` / `.cap` | مدة محسوبة {time} / السقف: سعر اليوم | Billed time {time} / Capped at the day price |
| `checkOut.rounding` | UP_AFTER_MINUTES({minutes}) «تقريب لأعلى بعد {minutes}» · the other rules their `spaceSettings` words, reused by key, not copied (§13 check 5.f) | Rounded up after {minutes} · … |
| `checkOut.minutes(n)` | zero/other «{n} دقيقة» · one «دقيقة واحدة» · two «دقيقتين» · few «{n} دقائق» · many «{n} دقيقة» | one «1 minute» · other «{n} minutes» |
| `checkOut.typed.amount` / `.badge` / `.help` / `.reason` | مبلغ الزيارة (₪) / سعر يدوي / لا سعر ساعة ولا سعر يوم منشور. / سبب السعر | Visit amount (₪) / Typed price / There’s no published hour or day price. / Reason for the price |
| `checkOut.unpriced` | لا سعر لهذه الزيارة. تُغلق بدون سعر، ويحدّده المالك لاحقًا. | This visit has no price. It closes unpriced, and the owner prices it later. |
| `checkOut.submit({amount})` / `.submitNone` / `.failed` | خروج واستلام {amount} / خروج بدون دفع / تعذّر تسجيل الخروج | Check out and receive {amount} / Check out without paying / We couldn’t check out |
| `checkOut.quoteChanged({amount})` / `.quoteFailed` | تغيّر المستحق إلى {amount}؛ راجع المبلغ ثم أكّد. / تعذّر حساب المستحق | The amount due changed to {amount}; check it, then confirm. / We couldn’t work out the amount due |
| `checkOut.done({name})` | سُجّل خروج {name} | {name} checked out |
| `money.group` / `.due` / `.received` / `.prefilled` | الدفع / المستحق / المستلم الآن (₪) / مُلئ بالمستحق؛ غيّره إن دفع غيره. | Payment / Due / Received now (₪) / Filled with the amount due; change it if they pay another amount. |
| `money.method` / `.methods` | الطريقة / CASH «نقدًا» · TRANSFER «تحويل» | Method / Cash · Transfer |
| `money.methodIn` | CASH «نقدًا» · TRANSFER «تحويلًا» | in cash · by transfer |
| `money.full` / `.nothingDue` | يُسجَّل المبلغ كاملًا. / لا شيء مستحق الآن. | Paid in full. / Nothing is due now. |
| `money.change({amount})` / `.credit({amount})` | الباقي للزبون {amount} / يصبح له رصيد {amount} | {amount} change / {amount} becomes credit |
| `money.owes({amount, name})` / `.owesPhone({amount})` / `.onSubscription({amount})` | يبقى {amount} دينًا على {name} / يبقى {amount} دينًا على صاحب رقم الجوال — رقم الجوال مطلوب / يبقى {amount} على الاشتراك | {amount} stays owed by {name} / {amount} stays owed by the mobile number’s holder — a mobile number is required / {amount} stays on the subscription |
| `money.none` / `.all` | لم يدفع شيئًا / استلام المبلغ كاملًا | Paid nothing / Receive the full amount |
| `money.amountInvalid` / `.amountZero` | اكتب مبلغًا بالشيكل، حتى منزلتين عشريتين / اكتب مبلغًا أكبر من صفر | Enter an amount in shekels, up to two decimals / Enter an amount above zero |
| `debt.name` / `.phone` / `.phoneRequired` | الاسم / رقم الجوال / رقم الجوال مطلوب ليُسجَّل المبلغ دينًا، مثل ‎+970 59 000 0000 | Name / Mobile number / A mobile number is needed to record the debt, e.g. +970 59 000 0000 |
| `debt.adds({name})` | يُضاف إلى ملف {name} | Added to {name}’s file |
| `toast.paid({amount, method})` / `.notPaid` / `.unpriced` | استُلم {amount} {method} / لم يدفع / أُغلقت بدون سعر | {amount} received {method} / Not paid / Closed unpriced |
| `failure.lost` / `.nothing` | لم يصل الرد. أعد المحاولة — لن تُسجَّل مرتين. / لم يُسجَّل شيء. | No answer came back. Try again — it won’t be recorded twice. / Nothing was recorded. |
| `refusals.VISIT_ALREADY_CLOSED` | سجّل مكتب آخر خروج هذه الزيارة قبلك، فلم تُسجَّل هذه الدفعة. لا تأخذ المبلغ مرة ثانية. | Another desk checked this visit out first, so this payment wasn’t recorded. Don’t take the money twice. |
| `refusals.PAYMENT_EXCEEDS_DUE` | المبلغ أكبر من المستحق الآن؛ حُدّث المستحق. | The amount is more than is due now; the amount due was updated. |
| `refusals.VISIT_HAS_CUSTOMER` | لهذه الزيارة زبون آخر؛ لا يُغيَّر رقمه هنا. | This visit belongs to another customer; their number can’t change here. |
| `refusals.PRICE_TYPING_NOT_ALLOWED` / `.forbidden` | لم يعد مسموحًا للاستقبال بكتابة سعر في هذه المساحة. / لم يعد هذا متاحًا لك في هذه المساحة. | Reception may no longer type a price at this space. / This is no longer open to you at this space. |
| `refusals.conflict` / `.not_found` | تعارض هذا الطلب مع طلب سابق؛ أغلق النافذة وأعد فتحها. / لم تعد هذه الزيارة موجودة. | This request clashed with an earlier one; close it and open it again. / This visit no longer exists. |
| `terms.loadFailed` | تعذّر تحميل أسعار الزيارات | We couldn’t load the visit prices |

- **Docs:** `desk.md` — header (*Scope*: «…; the web feature `features/desk`, dashboard-only: the desk's screens»,
  the *Authority*'s "no web screen yet" gone); *Who uses it* (the owner and reception, on «مكتب الاستقبال»);
  *Behaviour* «**The desk on the web**» (the check-in, the check-out, the money block, the intent's key, the
  warnings after); *Web decisions*: S1, S3, S4, S6, S7, S8, S10, DI-8, DI-10, DI-12, DI-13, DI-16, DI-25, DI-26,
  DI-28 — each «{date}, #PRNUM»; code map *Web*; *Web history*. `visits.md` *Who uses it* (the desk on the web reads
  the terms and the quote — one line). `architecture.md` §3 (S1's line), §2 (*Built so far*: the desk page).
  `overview.md` *Built* (Front desk: «on the dashboard, the desk: who is present, the live status and its override,
  a visit's check-in and check-out with its payment»). `docs/README.md` (desk's line). Finding 161 (Open: no
  route reads a day's visits; *Resolves when* the planned `GET …/visits` and the log tab are built). Finding 27
  re-checked (§13).

### PR 1 · Commit 5 — `feat(desk): collect the uncollected visits` (PR 1b's title)
- **Repository:** `uncollected(spaceId, page): Page<UncollectedVisit[]>`; `receivePayment(spaceId, body:
  ReceivePaymentRequest, key): ReceivedPayment`; `leaveToCustomer(spaceId, visitId, body:
  LeaveToCustomerRequest): DeskVisit`; `writeOff(spaceId, visitId, body: WriteOffVisitRequest): DeskVisit`;
  `undoWriteOff(spaceId, visitId): DeskVisit`.
- **`useUncollectedCard(spaceId, abilities)`** → `{ id: 'uncollected'; title /* counted, DI-3 */; state; rows: {
  key; name; how /* «خروج تلقائي عند الإغلاق · {day} {range}» */; amount: string | null /* balance, «بدون سعر» when
  null */; collect: { label; run } | null /* not while unpriced */; debt: { label; run } | null /* no customer */;
  more: { label; writeOff: { label; run } } | null /* the owner */ }[]; expanded; toggle: { label; expanded; run }
  | null; pagination; failure; empty }` — three rows, then all (DI-23); expanded on arrival at `#uncollected`
  (DI-19).
- **`useCollectDialog`**: the money block (due = `balanceAgorot`, `none: false`), a note (optional), the debt
  fields while a remainder stays on a visit with no customer (DI-11); sends `{ visitId, amountAgorot, method,
  note?, phone?, customerName? }` (`receivePaymentSchema`); refusals `VISIT_WRITTEN_OFF`, `VISIT_NOT_PRICED`,
  `PAYMENT_EXCEEDS_DUE`, `VISIT_HAS_CUSTOMER`, 409 «open visit».
- **`useDebtDialog`**: name (first, focused, DI-17) and phone, `leaveToCustomerSchema`; refusals
  `VISIT_ALREADY_PAID`, `VISIT_WRITTEN_OFF`, `VISIT_HAS_CUSTOMER`. No key (idempotent by design).
- **`useWriteOffDialog`** (owner): an `AlertDialog`, the reason (`writeOffVisitSchema`), the action
  `destructive`; done → `toastWrittenOff(amount, who, undo)` with `duration: Infinity` and «تراجع» (DI-29),
  which calls `undoWriteOff` once (never retried, S3) and says `undone` or `undoFailed`.
- **Components** as §9; the card's rows DI-24; «تحصيل» primary (DI-4); the «⋯» `ghost`, `aria-label` «إجراءات أخرى
  لزيارة {name}», its item destructive (DI-27), the focus back to the trigger after its dialog (DI-30).
- **Words** (`desk.uncollected`, `desk.collect`, `desk.debt`, `desk.writeOff`):

| key | ar | en |
|---|---|---|
| `uncollected.title(n)` | zero «لا زيارات غير محصّلة» · one «زيارة واحدة غير محصّلة» · two «زيارتان غير محصّلتين» · few «{n} زيارات غير محصّلة» · many/other «{n} زيارة غير محصّلة» | one «1 visit not collected» · other «{n} visits not collected» |
| `uncollected.none` / `.loadFailed` | لا توجد مبالغ غير محصّلة. / تعذّر تحميل الزيارات غير المحصّلة | Nothing left to collect. / We couldn’t load the uncollected visits |
| `uncollected.how({day, range})` / `.today` / `.yesterday` | خروج تلقائي عند الإغلاق · {day} {range} / اليوم / أمس | Auto check-out at closing · {day} {range} / today / yesterday |
| `uncollected.unpriced` | بدون سعر | No price |
| `uncollected.showAll({count})` / `.showFewer` | عرض الكل ({count}) / عرض أقل | Show all ({count}) / Show fewer |
| `uncollected.collect` / `.debt` / `.more({name})` / `.writeOff` | تحصيل / تسجيل دين / إجراءات أخرى لزيارة {name} / لن يُحصَّل… | Collect / Record a debt / More actions for {name}’s visit / Write off… |
| `uncollected.pagination` | label «صفحات الزيارات غير المحصّلة» · previous «السابق» · next «التالي» · page «الصفحة {page}» · summary «صفحة {page} من {total}» · more «صفحات أخرى» | Pages of uncollected visits · Previous · Next · Page {page} · Page {page} of {total} · More pages |
| `collect.title({name})` / `.note` / `.submit({amount})` / `.submitEmpty` / `.failed` | تحصيل زيارة · {name} / ملاحظة / تسجيل {amount} / تسجيل الدفعة / تعذّر تسجيل الدفعة | Collect a visit · {name} / Note / Record {amount} / Record payment / We couldn’t record the payment |
| `collect.done({name, day})` | {name} · زيارة {day} | {name} · visit of {day} |
| `debt.title({name})` / `.text({amount})` | تسجيل دين · {name} / يبقى {amount} دينًا على صاحب هذا الرقم، ويُنشأ له ملف زبون إن لم يكن له ملف. | Record a debt · {name} / {amount} stays owed by this number’s holder; a customer file is created if there is none. |
| `debt.submit` / `.done({amount, name})` / `.failed` | تسجيل الدين / سُجّل {amount} دينًا على {name} / تعذّر تسجيل الدين | Record the debt / {amount} recorded as a debt for {name} / We couldn’t record the debt |
| `refusals.VISIT_ALREADY_PAID` / `.VISIT_WRITTEN_OFF` / `.VISIT_NOT_PRICED` | لم يبقَ على هذه الزيارة شيء. / شُطبت هذه الزيارة. / لا سعر لهذه الزيارة بعد؛ يُحدَّد سعرها أولًا. | Nothing is owed on this visit any more. / This visit was written off. / This visit has no price yet; it is priced first. |
| `writeOff.title` / `.text({who, day, amount})` | لن يُحصَّل مبلغ هذه الزيارة؟ / {who} · {day} · {amount}. تخرج الزيارة من «غير محصّل» (ومن دين زبونها إن كان لها زبون). ليست دفعة ولا حذفًا: تبقى في السجل مع السبب، ويمكن التراجع عنها من الإشعار. | Write off this visit? / {who} · {day} · {amount}. It leaves “Not collected” (and its customer’s debt, if it has one). It isn’t a payment or a deletion: it stays on record with the reason, and it can be undone from the notice. |
| `writeOff.reason` / `.reasonRequired` / `.confirm` / `.back` | السبب / اكتب السبب / لن يُحصَّل / رجوع | Reason / Write the reason / Write off / Back |
| `writeOff.done({amount, who})` / `.undo` / `.undone` / `.undoFailed` / `.failed` | لن يُحصَّل {amount} · {who} / تراجع / أُعيدت الزيارة إلى «غير محصّل» / تعذّر التراجع عن الشطب / تعذّر الشطب | {amount} written off · {who} / Undo / The visit is back in “Not collected” / We couldn’t undo the write-off / We couldn’t write it off |

- **Docs:** `desk.md` *Behaviour* (the uncollected visits on the web, collect, the debt, the write-off and its
  undo), *Web decisions* (S3 for the unkeyed routes, DI-3, DI-4, DI-9, DI-11, DI-19, DI-23, DI-29, DI-30),
  *Web history*; `payments.md` *Who uses it* (the desk reads the uncollected visits — one line); finding 110
  → Resolved («#PRNUM: the web builds the uncollected list and its dialogs to the contract»); finding 115's
  evidence («#PRNUM: the desk never re-sends the write-off or its undo by itself (test 41)»); finding 112's
  evidence («#PRNUM: the web holds one key per intent and never reuses it across two visits»); finding 164 (Open).

### PR 1 · Commit 6 — `feat(desk): price the unpriced visits`
- **Repository:** `unpriced(spaceId, page): Page<DeskVisit[]>`; `price(spaceId, visitId, body: PriceVisitRequest):
  DeskVisit`.
- **`useUnpricedCard(spaceId, { mayTypePrice })`** — the query `enabled: mayTypePrice` (S5); rows (name, how, day,
  range, «تحديد السعر»); **`usePriceDialog`**: amount (`agorotOf`) and reason, `priceVisitSchema`; refusals
  `VISIT_ALREADY_PRICED`, `PRICE_TYPING_NOT_ALLOWED`, 409 open. The card sits under the uncollected one (`xl`
  side column), absent with none.
- **Words** (`desk.unpriced`):

| key | ar | en |
|---|---|---|
| `title(n)` | zero «لا زيارات بدون سعر» · one «زيارة واحدة بدون سعر» · two «زيارتان بدون سعر» · few «{n} زيارات بدون سعر» · many/other «{n} زيارة بدون سعر» | one «1 visit without a price» · other «{n} visits without a price» |
| `price` / `dialogTitle({name})` / `submit` | تحديد السعر / سعر زيارة · {name} / حفظ السعر | Set the price / Price a visit · {name} / Save the price |
| `done({name, amount})` / `failed` / `loadFailed` | حُدّد سعر زيارة {name}: {amount} / تعذّر حفظ السعر / تعذّر تحميل الزيارات بدون سعر | {name}’s visit priced at {amount} / We couldn’t save the price / We couldn’t load the visits without a price |
| `refusals.VISIT_ALREADY_PRICED` | حُدّد سعر هذه الزيارة من قبل. | This visit already has a price. |

  (The amount and reason fields reuse `checkOut.typed.amount` and `.reason`.)
- **Docs:** `desk.md` (the unpriced visits on the web, for whoever may type a price), `visits.md` *Who uses it*.

### PR 2 · Commit 1 — `feat(occupancy): match the present to a search`
- **`matchesPerson(person, term)`** (pure): the name contains the term (Arabic folded as `normaliseSearch`
  in `@masaha/shared` if exported — §13 check 5.g — else a plain `includes` after trimming), or the term is two or
  more digits (separators removed) and the person is a check-in whose customer's phone ends with them (the phone
  from PR 2's open check-ins, passed in; a visit has none).
- **`usePresentMatches(spaceId, term, phones)`** → `{ heading: 'حاضر الآن'; rows: PresentRowView[] }` (none for
  an empty term). **`PresentMatches({ spaceId, term, phones, action })`** (exported): `<section
  aria-labelledby>` with `h2 text-heading-3` (DI-38) and a `ul` of rows (`px-5 py-3`, DI-24), each with
  `action(person)`; nothing when no row.
- Words (`occupancy`): `present.matches` «حاضر الآن» / "Here now". `present.empty.text` becomes «ابحث عن زبون أو
  سجّل زيارة لأول من يصل.» / "Search for a customer, or check in a visit for the first arrival."

### PR 2 · Commit 2 — `feat(desk): find customers from the desk's search`
- **Repository:** `customers(spaceId, query: CustomersQuery): Page<CustomerRow[]>` (`GET …/customers`, the query
  checked by `customersQuerySchema`).
- **`useDeskSearch(spaceId, { presentCustomerIds })`** → `{ input: { label; placeholder; text; change; clear;
  autoFocus: boolean /* from 768 px */ }; term: string /* after the 400 ms pause */; customers: { heading: 'زبائن';
  state; cards: CustomerCardView[] /* the present ones left out: they are in the first group */; failure };
  checkIn: { label /* «تسجيل زيارة باسم «X»» or «تسجيل زيارة» for digits */; name: string; primary: boolean /*
  nothing matched */ }; none: { title; text } | null; count: string /* polite */ }` — `limit: 6` (the prototype's);
  `q` only once it is 1–60 characters.
- **`CustomerCardView`** = `{ key; name; phone: string | null; here: string | null /* «حاضر منذ HH:MM» */;
  subscription: { name; status: { label; tone } ; until: string } | null; balance: BalanceView; actions:
  CustomerActionsView }`; `balanceView(row)` (DI-40): `{ label, tone: 'warning' | 'success' | 'neutral' }`;
  `statusView(status)`: UPCOMING `info`, ACTIVE `success`, ENDING_SOON `warning`, EXPIRED `neutral`.
- **Components:** `DeskSearch({ spaceId, present, checkIn, abilities })` (exported): `<section aria-label="البحث">`
  with `Input role="searchbox" size="lg"` (`aria-controls` the results), the results (`present(term)` — the
  page's slot for `PresentMatches` —, then the customers' cards `grid gap-4 md:grid-cols-2 xl:grid-cols-3`, then
  the check-in button), the count line `aria-live="polite"` (A7); no match → `EmptyState` (DI-36) with the one
  primary (DI-20). `CustomerCard` (`CardTitle` as `h3`, DI-38; the phone `dir="ltr"`; `CardAction` the presence
  badge; the subscription line and badges; `CardFooter` the actions). `BalanceBadge`. In PR 2 the card's
  actions are «حضور» / «خروج» (commit 3) and «استلام {amount}» (commit 4); the «⋯» and the name's link come with
  PR 3.
- **`DeskPage`**: the search above the body; `present={(term) => <PresentMatches … action={checkOutAction} />}`.
- **Words** (`desk.search`, `desk.customer`):

| key | ar | en |
|---|---|---|
| `search.region` / `.label` / `.placeholder` | البحث / ابحث بالاسم أو آخر أرقام الجوال / الاسم أو آخر أرقام الجوال | Search / Search by name or the mobile’s last digits / Name or the mobile’s last digits |
| `search.customers` | زبائن | Customers |
| `search.found(n)` | zero «لا نتائج» · one «نتيجة واحدة» · two «نتيجتان» · few «{n} نتائج» · many/other «{n} نتيجة» | one «1 result» · other «{n} results» |
| `search.checkInNamed({name})` | تسجيل زيارة باسم «{name}» | Check in a visit for “{name}” |
| `search.none.title` / `.text` | لا أحد بهذا الاسم أو الرقم / زائر لمرة واحدة؟ سجّله كزيارة (لا يُنشأ ملف زبون). | No one by this name or number / A one-off visitor? Check them in as a visit (no customer file is created). |
| `search.failed` | تعذّر البحث في الزبائن | We couldn’t search the customers |
| `customer.noPhone` / `.hereSince({time})` / `.notHere` | بدون رقم جوال / حاضر منذ {time} / غير حاضر | No mobile number / Here since {time} / Not here |
| `customer.noSubscription` / `.until({date})` / `.noEnd` | بدون اشتراك / حتى {date} / بلا تاريخ نهاية | No subscription / until {date} / No end date |
| `customer.statuses` | UPCOMING «لم يبدأ» · ACTIVE «نشط» · ENDING_SOON «ينتهي قريبًا» · EXPIRED «منتهٍ» | Not started · Active · Ending soon · Expired |
| `customer.owes({amount})` / `.credit({amount})` / `.settled` | عليه {amount} / له رصيد {amount} / مسدّد | Owes {amount} / In credit {amount} / Settled |
| `customer.checkIn` / `.checkOut` / `.receive({amount})` | حضور / خروج / استلام {amount} | Check in / Check out / Receive {amount} |

  Dates: a day formatter in `shared/lib` if one exists (§13 check 5.h); else `features/desk/services/dayText.ts`
  (`Intl.DateTimeFormat`, `ar-u-nu-latn` for Arabic, `day: 'numeric', month: 'long'`, `timeZone: 'Asia/Gaza'`;
  one user, so it stays in the feature until a second one).
- **Docs:** `desk.md` *Behaviour* (the one search: present first, then customers, then the visit), *Web
  decisions* (K1 as built, DI-20, DI-36, DI-38, DI-40); `customers.md` *Who uses it* (the desk reads the list's
  search — one line); finding 160 (Open).

### PR 2 · Commit 3 — `feat(desk): check subscribers in and out`
- **Repository:** `checkInSubscriber(spaceId, body: CheckInSubscriberRequest, key): { data: DeskCheckIn; meta }`;
  `checkOutSubscriber(spaceId, checkInId): CheckInCheckOut`; `openCheckIns(spaceId): DeskCheckIn[]` (`?open=true`).
- **`useSubscriberCheckIn(spaceId, row)`** → `{ tap: { label; run; busy }; dialog: { open; title; reason: string /*
  none, expired, upcoming */; asVisit: { label; note; run }; anyway: { label; run } | null /* not with none */; back
  } }` — the tap sends at once when `row.current` is `ACTIVE` or `ENDING_SOON` (key: one per tap, S4); else opens
  the dialog (DI-14, S6). «تسجيل كزيارة» calls the visit's check-in with the customer's name (its own key).
  Refusals: `MEMBER_ALREADY_CHECKED_IN` (`alreadyHere`), `CUSTOMER_ARCHIVED`, 409 no code. Done → toast with the
  warnings (S6), `settle`, the search cleared and focused (S10).
- **`useCheckOutSubscriber(spaceId, person)`** — one tap, no key (S3); done → `toastSubscriberOut(name, minutes,
  balance)`: the stay («{h} س {m} د», from `checkedInAt`/`checkedOutAt` of the answer) and, when
  `balanceAgorot > 0`, «يبقى {amount} على الاشتراك» with an action «استلام» opening the payment on that
  subscription (commit 4); the focus to the next row's «خروج» (S10, DI-31).
- **`useOpenCheckInsQuery(spaceId, ids)`** — refetched when the state now's check-in ids change (S2); gives
  `PresentList`'s usage cell (`usage` prop) the subscription's first progress line («هذا الأسبوع 2 من 3» …, the
  same `progressLines` as the file — moved here from PR 3's list: `services/progressLines.ts` is created in this
  commit), and `matchesPerson` the phones.
- **Words** (`desk.subscriber`):

| key | ar | en |
|---|---|---|
| `pre.title({name})` | تسجيل حضور · {name} | Check in · {name} |
| `pre.none` / `pre.expired({name, date})` / `pre.upcoming({name, date})` | لا يوجد اشتراك. / انتهى الاشتراك «{name}» في {date}. / يبدأ الاشتراك «{name}» في {date}. | No subscription. / The subscription “{name}” ended on {date}. / The subscription “{name}” starts on {date}. |
| `pre.asVisit` / `pre.asVisitNote` / `pre.anyway` / `pre.back` | تسجيل كزيارة / تُسجَّل زيارة باسمه، ولا تُضاف إلى ملفه. / تسجيل على أي حال / رجوع | Check in as a visit / A visit is recorded under their name; it isn’t added to their file. / Check in anyway / Back |
| `in.done({name})` / `in.failed` / `in.alreadyHere({name})` | سُجّل حضور {name} / تعذّر تسجيل الحضور / {name} حاضر الآن. | {name} checked in / We couldn’t check them in / {name} is already here. |
| `out.done({name})` / `out.stay({time})` / `out.owes({amount})` / `out.receive` / `out.failed` | سُجّل خروج {name} / مدة الحضور {time} / يبقى {amount} على الاشتراك / استلام / تعذّر تسجيل الخروج | {name} checked out / Stayed {time} / {amount} stays on the subscription / Receive / We couldn’t check them out |
| `progress.days({used, total})` / `.week({used, total})` / `.today({used, total})` / `.hours({used, total})` | أيام {used} من {total} / هذا الأسبوع {used} من {total} / ساعات اليوم {used} من {total} س / الساعات {used} من {total} س | Days {used} of {total} / This week {used} of {total} / Today {used} of {total} h / Hours {used} of {total} h |
| `progress.billed({rate, unit})` / `.units` | يُحسب من الحضور: {rate} {unit} / PER_HOUR «للساعة» · PER_DAY «لليوم» | Billed from attendance: {rate} {unit} / per hour · per day |
| `progress.validUntil({date})` / `.endedOn({date})` / `.startsOn({date})` / `.noEnd` | صالح حتى {date} / انتهى في {date} / يبدأ في {date} / بلا تاريخ نهاية | Valid until {date} / Ended {date} / Starts {date} / No end date |

  (`used` of today's and the hours' lines: `minutesToday`, `minutesUsed` as «2:30», h:mm, LTR.)
- **Docs:** `desk.md` (a subscriber's check-in and check-out on the web; S6's pre-dialog; DI-14, DI-31);
  `subscriptions.md` *Who uses it* (the desk reads the open check-ins — one line).

### PR 2 · Commit 4 — `feat(desk): receive a payment on a customer's item`
- **Repository:** `file(spaceId, customerId): CustomerFile`.
- **`openItems(file)`** (pure): the unpaid visits (oldest first, each `{ key: 'visit-{id}'; label: «زيارة {day}»;
  due: charge; paid; left: balance; usage: false }`, an unpriced one left out — nothing to pay) then the
  subscriptions with `balanceAgorot > 0` (`label`: the name; `usage`: billing ≠ FIXED). A usage-based
  subscription with no balance is still offered when chosen from its card (credit).
- **`usePayDialog(spaceId, { customerId?, itemKey?, presentIds })`** → `{ step: 'pick' | 'items' | 'nothing';
  pick: { input; heading /* «عليهم مبالغ:» */; rows: { key; name; phone; balance; choose }[] /* payment=OWES,
  present first (DI-21) */; none; another }; items: { legend; options: { key; label; line; usage }[]; chosen;
  choose }; money: MoneyBlockView /* none: false; open while a usage item */; note; submit; failure }` —
  the amount follows the item only while untouched (DI-35); one payment per submit (DI-22), its key per opening;
  `{ visitId | subscriptionId, amountAgorot, method, note? }` (+ phone and name for a visit's remainder with no
  customer — rare here: the file's visits have their customer).
- **`PayDialog`**; the page action «استلام دفعة» (top bar «⋯» on a phone, an outline button from 768 px); the card's
  «استلام {amount}» (`secondary`); the subscriber's check-out toast's «استلام».
- **Words** (`desk.pay`):

| key | ar | en |
|---|---|---|
| `title` / `titleFor({name})` / `choose` | استلام دفعة / استلام دفعة · {name} / اختر الزبون | Receive a payment / Receive a payment · {name} / Choose the customer |
| `owing` / `pick` / `another` / `noCustomer` | عليهم مبالغ: / اختيار / زبون آخر / لا زبون بهذا الاسم أو الرقم. | Customers who owe: / Choose / Another customer / No customer with this name or number. |
| `item` / `itemVisit({day})` / `itemLine({due, paid, left})` | الدفعة عن / زيارة {day} / المستحق {due} · المدفوع {paid} · المتبقي {left} | The payment is for / Visit of {day} / Due {due} · Paid {paid} · Left {left} |
| `owesNothing` / `usageNote` | لا مبلغ مستحق على هذا الزبون. / اشتراك يُحسب من الحضور: ما يزيد يصبح رصيدًا. | This customer owes nothing. / Billed from attendance: anything extra becomes credit. |
| `submit({amount})` / `done({name, item, left})` / `failed` / `fileFailed` | تسجيل {amount} / {name} · {item} · المتبقي {left} / تعذّر تسجيل الدفعة / تعذّر تحميل مستحقات الزبون | Record {amount} / {name} · {item} · {left} left / We couldn’t record the payment / We couldn’t load what the customer owes |

  (`refusals` and `failure` reuse PR 1's.)
- **Docs:** `desk.md` (a payment on one item; DI-21, DI-22, DI-35); `payments.md` *Who uses it* (one line).

### PR 3 · Commit 1 — `feat(desk): list the space's customers`
- **`customersQueryOf(params, owner)`** (pure, S11) → `{ query: CustomersQuery; page }`, and `paramsOf`.
  **`useCustomersFilters`** (`useSearchParams`, `usePausedSearch`, `usePageInRange` from `shared/lists`).
- **`useCustomersList(spaceId, { owner, presentIds })`** → `{ label; toolbar: { search; status: { label; value;
  options /* «الكل» + the four + «مؤرشف» for the owner */; choose }; kind: { label; value; options; choose };
  payment: { … }; sheet: { count; applied; clear } }; count: string; state; rows: CustomerCardView[]; pagination;
  failure; empty: { title; text } }` — `keepPreviousData`, `aria-busy`.
- **`CustomersList({ spaceId, owner, fileLink, newCustomer })`** (exported): `DataTable` (five columns from 768 px:
  name with the phone under it — the name a `Link` to `fileLink(id)` —, subscription with its end under it, status,
  balance (`BalanceBadge`), actions); `renderCard` below; the toolbar: the search, then (P5) the kind and payment
  `Select`s inline from 768 px and in a bottom `Sheet` below it with the active count, the status chips
  (`ToggleGroup type="single"`), the count, and «زبون جديد» (PR 4; absent before it).
- **Pages:** `CustomersPage` (`PageHeader`; `CustomersList`); `navigation.ts` `SPACE_CUSTOMER_PATH =
  ${spaceOverviewPath(':spaceId')}/customers/:customerId` and `spaceCustomerPath(spaceId, customerId)`.
- **Words** (`desk.customers`):

| key | ar | en |
|---|---|---|
| `label` / `columns` | زبائن المساحة / name «الاسم» · subscription «الاشتراك» · status «الحالة» · balance «الرصيد» · actions «إجراءات» | The space’s customers / Name · Subscription · Status · Balance · Actions |
| `status.label` / `status.all` / `status.ARCHIVED` | تصفية حسب الحالة / الكل / مؤرشف | Filter by status / All / Archived |
| `kind.label` / `kind.options` | نوع الاشتراك / all «كل الأنواع» · PACKAGE «باقة» · CUSTOM «مخصّص» · NONE «بدون اشتراك» | Subscription type / All types · Package · Custom · No subscription |
| `payment.label` / `payment.options` | الدفع / all «كل حالات الدفع» · OWES «عليه دين» · CREDIT «له رصيد» · SETTLED «مسدّد» | Payment / All payment states · Owes money · In credit · Settled |
| `filters.title` / `.applied(n)` / `.show(n)` / `.clear` | الفلاتر / zero «لا فلاتر مطبّقة» · one «فلتر واحد مطبّق» · two «فلتران مطبّقان» · few «{n} فلاتر مطبّقة» · many «{n} فلترًا مطبّقًا» · other «{n} فلتر مطبّق» / one «عرض الزبون» · two «عرض الزبونين» · few «عرض {n} زبائن» · many «عرض {n} زبونًا» · zero/other «عرض {n} زبون» / مسح الفلاتر | Filters / 1 filter applied · {n} filters applied / Show 1 customer · Show {n} customers / Clear filters |
| `count(n)` | zero «لا زبائن» · one «زبون واحد» · two «زبونان» · few «{n} زبائن» · many «{n} زبونًا» · other «{n} زبون» | one «1 customer» · other «{n} customers» |
| `empty.title` / `.text` | لا يوجد زبائن بعد / يُضاف الزبون عند أول اشتراك، أو عندما يخرج زائر بدون دفع. | No customers yet / A customer is added with their first subscription, or when a visitor leaves without paying. |
| `noMatch.title` / `.text` / `archivedEmpty` | لا يوجد زبائن يطابقون البحث / جرّب اسمًا أو رقمًا آخر، أو غيّر الفلاتر. / لا يوجد زبائن مؤرشفون | No customers match / Try another name or number, or change the filters. / No archived customers |
| `loadFailed` / `pagination` | تعذّر تحميل الزبائن / label «صفحات الزبائن» and the list's five words | We couldn’t load the customers / Pages of customers … |

- **Docs:** `customers.md` (*Who uses it*: «الزبائن» on the web; a *Web decisions* line: S11), `desk.md` (*Behaviour*:
  the list on the web), `architecture.md` §2 (*Built so far*).

### PR 3 · Commit 2 — `feat(desk): show a customer's file`
- **`useCustomerFile(spaceId, customerId, abilities)`** → `{ state: 'loading' | 'failed' | 'notFound' | 'ready';
  title: PageTitle /* the name, for useRecordTitle */; header: { phone; here: string | null; status; balance:
  BalanceView; archived: boolean; actions /* commit 3 */ }; unpaid: { title; rows /* UncollectedRow's shape,
  DI-24; «تحصيل» → PayDialog with the item */ } | null; subscriptions: SubscriptionCardView[]; failure; notFound }`
  with `SubscriptionCardView = { key; title: { name; typed: string | null /* «سعر يدوي» */ }; dates: string;
  terms: string /* termsLine */; badges: { status; pay } ; money: { due; paid; left; dueLabel }; progress:
  string[]; receive: { label; run } | null /* left > 0, DI-44 */; statement /* commit 4 */; end /* commit 4 */ }`.
  `payStatus(sub)`: paid `success` (balance ≤ 0), partial `warning` (paid > 0), unpaid `destructive`.
- **`CustomerPage`**: `parseSpaceId`, `customerId` from `useParams`; `useRecordTitle(file.title)`; `Breadcrumb`
  (named «مسار التنقّل») «الزبائن» › the name; `CustomerFile`. The route `customers/:customerId` under the space
  branch, `RequireSpaceRole roles={BOTH}`, its title «ملف الزبون» until the name arrives.
- **Words** (`desk.file`):

| key | ar | en |
|---|---|---|
| `title` / `breadcrumb` / `notFound.title` / `.text` | ملف الزبون / مسار التنقّل / لم نجد هذا الزبون / ربما ليس من زبائن هذه المساحة. | Customer file / Breadcrumb / We couldn’t find this customer / They may not be a customer of this space. |
| `balance` / `archived` / `loadFailed` | الرصيد / مؤرشف / تعذّر تحميل ملف الزبون | Balance / Archived / We couldn’t load the customer’s file |
| `unpaid.title` / `.unpriced` | زيارات غير مدفوعة / بدون سعر بعد | Unpaid visits / Not priced yet |
| `subscriptions.title` / `.none` / `.onlyVisits` | الاشتراكات / لا توجد اشتراكات / هذا الزبون يأتي بزيارات فقط. | Subscriptions / No subscriptions / This customer only comes for visits. |
| `card.dates({from, to})` / `.typed` | {from} – {to} / سعر يدوي | {from} – {to} / Typed price |
| `card.terms` | totalDays(n) «{n} أيام» (one «يوم واحد» · two «يومان» · few «{n} أيام» · many «{n} يومًا» · other «{n} يوم») · daysPerWeek({n}) «{n} بالأسبوع» · hoursPerDay({n}) «{n} س باليوم» · totalHours({n}) «{n} س إجمالًا» · student «للطلاب» · none «بدون شروط إضافية» | {n} days · {n} a week · {n} h a day · {n} h in all · Students · No extra terms |
| `card.due` / `.dueSoFar` / `.paid` / `.left` | المستحق / المستحق حتى الآن / المدفوع / المتبقي | Due / Due so far / Paid / Left |
| `card.pay` | paid «مدفوع» · partial «مدفوع جزئيًا» · unpaid «غير مدفوع» | Paid · Partly paid · Unpaid |
| `card.receiveLeft` | استلام المتبقي | Receive what’s left |

- **Docs:** `desk.md` (the file on the web; DI-42, DI-43, DI-44), `subscriptions.md` *Who uses it*, `architecture.md` §2.

### PR 3 · Commit 3 — `feat(desk): edit, archive and restore a customer`
- **Repository:** `edit(spaceId, customerId, body: UpdateCustomerRequest): Customer`; `archive`, `restore` →
  `Customer`.
- **`useEditDialog`** — `useServerForm` over `updateCustomerSchema`, `prepare` sends **only the fields that
  differ from the customer as loaded** (finding 123), nothing when none («لم يتغيّر شيء»); a cleared phone →
  `null`; no key and never re-sent (S3); `PHONE_TAKEN` on the phone, `CUSTOMER_ARCHIVED`.
- **`useArchiveFlow(spaceId, customer, balance)`** (owner) — settled: archive at once, a toast with «تراجع»
  (restore; P9); owing: `ArchiveDialog` (`AlertDialog`, the debt named, action `destructive`); refusals
  `MEMBER_ALREADY_CHECKED_IN` (DI-47). Restore: `PHONE_TAKEN` → `restorePhoneTaken`.
- **`CustomerMenu({ actions })`** — the «⋯» (`ghost`, `aria-label` «إجراءات أخرى: {name}», the content labelled the
  same, DI-39): «ملف الزبون» (not in the file), «تعديل البيانات», and for the owner «أرشفة…» (destructive, DI-46).
  The card (PR 2) and the list's rows gain it; an archived customer's row shows «استرجاع» (owner) instead.
- **Words** (`desk.edit`, `desk.archive`, `desk.customer.menu`):

| key | ar | en |
|---|---|---|
| `customer.menu({name})` / `.file` / `.edit` / `.archive` / `.restore` | إجراءات أخرى: {name} / ملف الزبون / تعديل البيانات / أرشفة… / استرجاع | More actions: {name} / Customer file / Edit details / Archive… / Restore |
| `edit.title` / `.name` / `.phone` / `.optional` / `.phoneHelp` | تعديل البيانات / الاسم / رقم الجوال / اختياري / إليه يُرسل تذكير الدين على واتساب. | Edit details / Name / Mobile number / Optional / Debt reminders go to this number on WhatsApp. |
| `edit.save` / `.nothingChanged` / `.done({name})` / `.failed` | حفظ / لم يتغيّر شيء / حُفظت بيانات {name} / تعذّر حفظ البيانات | Save / Nothing changed / {name}’s details saved / We couldn’t save the details |
| `archive.done({name})` / `.undo` / `.restored({name})` | أُرشف {name} / تراجع / استُرجع {name} | {name} archived / Undo / {name} restored |
| `archive.title({name})` / `.text({amount})` / `.confirm` / `.back` | أرشفة {name}؟ / عليه {amount} غير مسدّدة. يبقى المبلغ في سجله، ويخرج من البحث ومن المكتب، ويبقى تحت «مؤرشف» في الزبائن. / أرشفة رغم الدين / رجوع | Archive {name}? / They owe {amount}. The amount stays on their record; they leave the search and the desk, and stay under “Archived” in Customers. / Archive anyway / Back |
| `archive.doneOwing({name, amount})` / `.present({name})` / `.failed` | أُرشف {name} · عليه {amount} / {name} حاضر الآن؛ سجّل خروجه قبل الأرشفة. / تعذّرت الأرشفة | {name} archived · owes {amount} / {name} is here now; check them out before archiving. / We couldn’t archive them |
| `archive.restorePhoneTaken` / `.restoreFailed` | رقمه مسجّل الآن لزبون آخر؛ لا يُسترجع قبل تغيير أحد الرقمين. / تعذّر الاسترجاع | Their number now belongs to another customer; change one of them before restoring. / We couldn’t restore them |

- **Docs:** `customers.md` (*Web decisions*: the edit sends only what changed, never re-sent; archive and restore,
  DK-014, P9), finding 123 → Resolved («#PRNUM: …»).

### PR 3 · Commit 4 — `feat(desk): show a subscription's statement`
- **Repository:** `statement(spaceId, subscriptionId): SubscriptionStatement`; `endSubscription(spaceId,
  subscriptionId): SubscriptionState`.
- **`useStatement(spaceId, subscriptionId, open)`** (enabled while open) → `{ toggle: { label; expanded; run };
  checkIns: { title; rows: { key; day; in; out: string | null /* «حاضر الآن» while open */; duration; auto:
  boolean }[]; none }; payments: { title; rows: { key; date; amount; method; voided: { label: 'ملغاة'; reason }
  | null }[]; none }; renewal: string | null; state; failure }` (DI-43).
- **`useEndDialog`** — `AlertDialog` (destructive), the new end (`today`, or the start if not started), «المبالغ…
  لا تتغيّر»; no key, never re-sent (S3).
- **Words** (`desk.statement`, `desk.end`):

| key | ar | en |
|---|---|---|
| `statement.show` / `.hide` / `.loadFailed` | عرض الكشف / إخفاء الكشف / تعذّر تحميل الكشف | Show the statement / Hide the statement / We couldn’t load the statement |
| `statement.checkIns` / `.columns` / `.here` / `.auto` / `.noCheckIns` | الحضور / day «اليوم» · in «الدخول» · out «الخروج» · duration «المدة» / حاضر الآن / خروج تلقائي / لا حضور بعد. | Attendance / Day · In · Out · Duration / Here now / Auto check-out / No attendance yet. |
| `statement.payments` / `.noPayments` / `.voided` / `.voidedReason({reason})` | الدفعات / لا دفعات بعد. / ملغاة / أُلغيت: {reason} | Payments / No payments yet. / Voided / Voided: {reason} |
| `statement.renewal({date})` | التجديد يبدأ في {date} | A renewal would start on {date} |
| `end.action` / `.title` / `.text({name, end})` / `.textWas({name, end, was})` | إنهاء الاشتراك / إنهاء الاشتراك اليوم؟ / {name} · يصبح تاريخ النهاية {end}. المبالغ المدفوعة والمستحقة لا تتغيّر. / {name} · يصبح تاريخ النهاية {end} بدل {was}. المبالغ المدفوعة والمستحقة لا تتغيّر. | End subscription / End the subscription today? / {name} · The end date becomes {end}. Amounts paid and due don’t change. / {name} · The end date becomes {end} instead of {was}. Amounts paid and due don’t change. |
| `end.confirm` / `.back` / `.done({name})` / `.failed` | إنهاء الاشتراك / رجوع / انتهى الاشتراك «{name}» اليوم / تعذّر إنهاء الاشتراك | End subscription / Back / “{name}” ended today / We couldn’t end the subscription |

- **Docs:** `desk.md` (the statement on the web; the end), `subscriptions.md` (*Who uses it*); findings 162, 163
  (Open); finding 124: its *Resolved* line is DESK_API's — the executor checks it (§13 check 2).

### PR 3 · Commit 5 — `feat(session): say a session ended for idleness`
- `shared/session`: the store gains `endedBy: 'idle' | null`, set when the refresh (or the restore) is refused
  401 with `code === 'SESSION_IDLE'`, cleared on the next sign-in. The sign-in page shows, while it holds,
  `Alert variant="info"` with `copy.errors.SESSION_IDLE` (worker B's line) above the form.
- No words of this item's own. Docs: `auth.md` (*Web decisions*: «A session the server ended for idleness says so
  on sign-in. {date}, #PRNUM»), `architecture.md` §4 (the status's line: `endedBy`).

### PR 4 · Commit 1 — `feat(design-system): open the end sheet full width` (S12)
- `Sheet` sides `start` and `end`: `w-full md:w-3/4 md:max-w-sm`; `SheetBody` `min-w-0`. The showcase unchanged.
  Docs: `foundation.md` §12 (Sheet: «full width below 768 px»), finding 101 → Resolved.

### PR 4 · Commit 2 — `feat(packages): offer the packages to the desk`
- **`useOfferedPackages(spaceId)`** (exported) → `{ state; packages: SpacePackage[] /* isActive only, in order */;
  retry }` — the list's own query (the owner's key: one cache).
- Docs: `packages.md` (*Who uses it*: reception's desk reads the offered packages on the web; *Web history*).

### PR 4 · Commit 3 — `feat(desk): subscribe a new or known customer`
- **Repository:** `createCustomer(spaceId, body: CreateCustomerRequest, key): Customer`; `subscribe(spaceId,
  customerId, body: SubscribeRequest, key): { data: NewSubscription; meta }`.
- **`SheetEntry`** = `{ mode: 'new'; name?: string; phone?: string } | { mode: 'subscribe'; customer: Customer &
  CustomerBalance } | { mode: 'renew'; customer: …; renews: SubscriptionState }`.
- **`useSubscriptionSheet({ spaceId, entry, packages, shifts, mayTypePrice, published? })`** → `{ open; title;
  description; customer: { name; phone; phoneRequired } | null /* new only */; noPhone: string | null /* DI-53 */;
  prior: { title; items: string[]; note } | null /* the file's open items, K3, decision 3 */; packages: { legend;
  groups: { heading; options: PackageChoice[] }[]; chosen; choose; current: string | null /* a renewal's one line,
  «تغيير الباقة» */ }; dates: { from; to; toHelp; endNote }; custom: CustomTermsView | null; money:
  MoneyBlockView /* due = prior total + new price; open with usage billing; none: true */; submit: { label; run;
  busy }; half: { title; retry: { label; run } } | null /* DI-37 */; failure }`. `PackageChoice = { value: string
  /* 'pkg-{id}' | 'custom' */; title; amount: string | null; terms: string }`. A new customer: `createCustomer`
  (key 1) then `subscribe` (key 2); a refusal of the second keeps the first (DI-37). The request: `{ packageId |
  custom, startsOn, renewalOfId?, payment?: { amountAgorot: recorded, method } }`, checked by `subscribeSchema`.
  Done → toast: the title, the parts (`payments`: each item's word and amount, K4), «يبقى {debt} دينًا» from
  `debtAgorot`, the warning `CUSTOMER_HAS_DEBT`'s line when in `meta.warnings`.
- **`endOf(start, validityDays)`** (pure): `start + validityDays − 1` (both days counted, the server's rule, shown
  only).
- **Entries:** the desk's «زبون جديد» (page action) and the search's «زبون جديد باسم «X»» (link, DI-20), the card's
  and the file's «اشتراك جديد» (menu), the customers list's «زبون جديد». The page passes `packages`
  (`useOfferedPackages`), `shifts` (`useSpaceShifts('owner', spaceId)`), `mayTypePrice` (the terms).
- **Words** (`desk.sheet`):

| key | ar | en |
|---|---|---|
| `title.new` / `.subscribe` / `.renew` / `newText` | زبون جديد / اشتراك جديد / تجديد الاشتراك / الاسم والجوال، ثم الاشتراك والدفع. | New customer / New subscription / Renew subscription / The name and mobile, then the subscription and the payment. |
| `entry.newNamed({name})` / `entry.newNumber` | زبون جديد باسم «{name}» / زبون جديد بهذا الرقم | New customer named “{name}” / New customer with this number |
| `name` / `phone` / `optional` / `noPhone` | الاسم / رقم الجوال / اختياري / لا رقم جوال لهذا الزبون؛ أضفه من «تعديل البيانات» لتذكيره بالدين. | Name / Mobile number / Optional / This customer has no mobile number; add one from “Edit details” to remind them of the debt. |
| `phoneRequired({amount})` | رقم الجوال مطلوب: يبقى {amount} دينًا، مثل ‎+970 59 000 0000 | A mobile number is required: {amount} stays owed, e.g. +970 59 000 0000 |
| `package` / `groups.published` / `groups.packages` | الباقة / منشورة للزوار / باقات المساحة — لا تظهر للزوار | Package / Published / The space’s packages — not shown to visitors |
| `custom.title` / `custom.terms` / `noPackages` / `packagesFailed` | مخصّص / حدّد الشروط والسعر بنفسك / لا باقات متاحة بعد. / تعذّر تحميل الباقات | Custom / Set the terms and the price yourself / No packages offered yet. / We couldn’t load the packages |
| `validity(n)` | one «يوم واحد» · two «يومان» · few «{n} أيام» · many «{n} يومًا» · zero/other «{n} يوم» | one «1 day» · other «{n} days» |
| `from` / `to` / `toFromPackage` / `changePackage` | من / إلى / تُحسب من الباقة / تغيير الباقة | From / To / From the package / Change package |
| `noEnd` | بلا تاريخ نهاية · يبقى نشطًا حتى يُنهى | No end date · it stays active until it is ended |
| `custom.name` / `.audience` / `.audiences` | اسم الاشتراك / لمن / GENERAL «الجميع» · STUDENT «الطلاب» | Subscription name / For / Everyone · Students |
| `custom.billing` / `.billings` | طريقة الحساب / FIXED «سعر ثابت» · PER_HOUR «بالساعة» · PER_DAY «باليوم» | Billing / Fixed price · Per hour · Per day |
| `custom.price` / `.rate` / `.limits` | السعر (₪) / سعر الوحدة (₪) / الحدود — اختيارية | Price (₪) / Rate (₪) / Limits — optional |
| `custom.limits` items | totalDays «مجموع الأيام» · daysPerWeek «أيام بالأسبوع» · hoursPerDay «ساعات باليوم» · totalHours «مجموع الساعات» | Total days · Days a week · Hours a day · Total hours |
| `custom.shift` / `.reason` / `.defaultName` | الوردية / سبب السعر / مخصّص | Shift / Reason for the price / Custom |
| `prior.title({amount})` / `.note` / `total` | مستحق من قبل: {amount} / يُطبَّق المستلم على المستحق من قبل أولًا، ثم على الاشتراك الجديد. / المجموع | Owed from before: {amount} / What you receive pays what was owed first, then the new subscription. / Total |
| `submit.save({amount})` / `.renew({amount})` / `.saveNone` / `.renewNone` | حفظ واستلام {amount} / تجديد واستلام {amount} / حفظ بدون دفع / تجديد بدون دفع | Save and receive {amount} / Renew and receive {amount} / Save without payment / Renew without payment |
| `half.title({name})` / `.retry` / `.closed({name})` | أُضيف {name} إلى الزبائن؛ لم يُحفظ الاشتراك. / حفظ الاشتراك / {name} في الزبائن بدون اشتراك. | {name} was added to the customers; the subscription wasn’t saved. / Save the subscription / {name} is in the customers, with no subscription. |
| `done.new({name})` / `.renewed({name})` / `.noPayment` / `.owes({amount})` / `.failed` | حُفظ الاشتراك · {name} / جُدّد اشتراك {name} / بدون دفع / يبقى {amount} دينًا / تعذّر حفظ الاشتراك | Subscription saved · {name} / {name}’s subscription renewed / No payment / {amount} stays owed / We couldn’t save the subscription |

  (The money block, «طالب», the shifts' «بدون وردية» and the refusals reuse PR 1–2's lines; `CUSTOMER_HAS_DEBT`,
  `SUBSCRIPTION_ALREADY_RENEWED`, `CUSTOMER_ARCHIVED`, `PHONE_TAKEN` are `errors`'.)
- **Docs:** `desk.md` (the sheet on the web; decision 3; DI-37, DI-45, DI-50–53), `customers.md` (*Who uses it*:
  the sheet creates a customer), finding 125 → Resolved («#PRNUM: the sheet shows the prior debts and their total,
  and the allocation after the request, from the answer»).

### PR 4 · Commit 4 — `feat(desk): renew a subscription with its debts`
- The renewal: `renewalOfId` the renewed one; the start from its statement's `renewal.startsOn` (read when the
  sheet opens; `null` → `SUBSCRIPTION_ALREADY_RENEWED`'s line and the sheet offers «اشتراك جديد» instead); the
  package the renewed one's (`packageId`), shown as one line with «تغيير الباقة» (DK-007), «مخصّص» repeating its
  terms when it was custom; K3's prior items from the file. Words: none new beyond commit 3's. Docs: `desk.md`,
  `subscriptions.md` (*Who uses it*); finding 165 if spec D is declined.
- **With spec D (if taken):** `PackageChoice` gains `price-{id}` for the space's published WEEK and MONTH prices
  (read from `GET /manage/spaces/:id`'s prices through `spaces`, passed by the page as the shifts are), first
  under «منشورة للزوار», named «أسبوعي» / «شهري» (`sheet.published.WEEK` «أسبوعي» / "Weekly", `.MONTH` «شهري» /
  "Monthly", `.students` «· للطلاب» / "· students"); the request `{ priceId, name }`.

## 11. Tests — each with its lane, title and the break that must make it fail

Each new test is seen red first (testing §3.5), its red line recorded; for code that exists, the break is made
once, its red output recorded, then restored (§3.7). **Markers:** [role] a permission shown or hidden, [money] a
money figure, [key] an idempotency key or a retry, [warn] a warning, [state] loading, empty, failure, offline or a
409, [width], [a11y]. A width is proven in the component lane through `useMediaQuery` and `stubScreenWidth`; a
layout drawn by classes alone is checked in the real run with its own break (§13). Hooks are tested with
`renderHook` through `fakeTransport`/`fakeAdapter` (the platform's seam); components with Testing Library and
`vitest-axe`.

### PR 1
| # | Lane · file | Title | Break |
|---|---|---|---|
| 1 | unit · `shared/api/idempotency/withIdempotencyKey.unit.test.ts` | puts the key in the `Idempotency-Key` header | another header name |
| 2 | component · `useIntentKey.component.test.tsx` | **keeps one key across renders until renewed, then gives a new one** [key] | a new UUID each render |
| 3 | unit · `request` test (M) | `postWithMeta` hands back `data` and the warnings, and `undefined` without `meta` | `meta` required |
| 4 | component · `DashboardLayout.component.test.tsx` | **below 768 px a page's action stands in the bottom bar and the content makes room for it; from 768 px there is no bar; a page with no action has none** [width] | the bar always drawn |
| 5 | unit · `occupancy` repository test | reads the state now; sets and clears the override with its body; a failure is an `AppError` | `DELETE` → `PUT` |
| 6 | component · `useStateNowQuery.component.test.tsx` (fake timers, `document.visibilityState`) | **reads again every 30 s while visible, never while hidden, and at once on returning** [state] | `refetchIntervalInBackground: true`; `refetchOnWindowFocus: false` |
| 7 | component · `usePresentList.component.test.tsx` | lists people in the server's order with kind, since and a visit's charge so far from the server; «يُحدَّد عند الخروج» with none [money] | the charge computed from the rates |
| 8 | same | **loading, a failure with its reference and a retry, empty, and a failed refresh that keeps the rows** [state] | the rows dropped on a failed refetch |
| 9 | unit · `stayDuration.unit.test.ts`, `overrideLeft.unit.test.ts` | 2 h 05 m; 0 m; an override's 84 min left as «1:24», rounded up | rounded down |
| 10 | component · `PresentList.component.test.tsx` | **one `h2` naming the section with «27 / 40» (or «3» with no capacity); the table named «قائمة الحاضرين»; each row's action named by the person; cards below 768 px; axe-clean at 390 and 1440** [a11y] [width] | the table labelled «الحاضرون الآن» |
| 11 | component · `useLiveStatusControl.component.test.tsx` | **shows what visitors see, under an override with its time left; sets a state for each duration and returns to automatic** | the duration not sent |
| 12 | same | **disabled with its reason while closed; `SPACE_NOT_OPEN` said in the panel** [state] | enabled while closed |
| 13 | component · `LiveStatusControl.component.test.tsx` | **the trigger's name is the full line at 390 though it shows the state word only** [a11y] [width] | `aria-label` left out |
| 14 | unit · `visitRates.unit.test.ts` | a shift's rates, else the no-shift row; student only where the terms carry them [money] | student offered always |
| 15 | unit · `currentShift.unit.test.ts` | the shift whose range holds Gaza's minute; none outside every shift; midnight in Gaza, not UTC | `getUTCHours()` |
| 16 | unit · `moneyOf.unit.test.ts` | **recorded never above the due for a visit; change above it; credit above it for a usage-based one; the remainder below it** [money] | recorded = received |
| 17 | unit · `quoteAge.unit.test.ts` | a quote older than 4 minutes is stale; 3:59 is not | `>=` 5 min |
| 18 | unit · `warningLines.unit.test.ts` | each `DESK_WARNINGS` code to its catalogue line, in the server's order; none → none [warn] | sorted |
| 19 | unit · `desk` repository test | each call's method, path and body; **a check-in, a check-out and a payment carry the key they are given** [key] | the header dropped on the check-out |
| 20 | component · `useVisitDialog.component.test.tsx` | sends the name, the audience only where offered, the current shift; **the same key on a retry after no answer, and on a second press while pending; a new key when opened again** [key] | `renew()` in `submit` |
| 21 | same | **the server's warnings are said in the toast as a warning** [warn] | warnings ignored |
| 22 | component · `useMoneyBlock.component.test.tsx` | **«المستلم الآن» follows the due until typed; «لم يدفع شيئًا» empties it and «استلام المبلغ كاملًا» restores it** [money] | follows the due after typing |
| 23 | component · `useCheckOutDialog.component.test.tsx` | **sends the quote's time and the recorded amount, never the typed amount above the due** [money] | `amountAgorot: received` |
| 24 | same | **a remainder on a visit with no customer asks the name and the phone; they stay once shown** [state] | unmounted when covered |
| 25 | same | **a stale quote is read again before sending, and a changed due stops the send with its line** [money] | sent with the old `at` |
| 26 | same | **no rate: whoever may type types the amount and its reason; whoever may not closes it unpriced with a phone** [role] [money] | the reason not required |
| 27 | same | **`VISIT_ALREADY_CLOSED` says the payment was not recorded; `PAYMENT_EXCEEDS_DUE` reads the quote again; no answer says a retry is safe; a 403 says it is no longer open and refreshes `['me']`** [state] | one generic line for all |
| 28 | component · `CheckOutDialog.component.test.tsx` | **the money block is a named group; «المستلم الآن» described as filled with the due; the failure is an alert; the first field focused; axe-clean** [a11y] | `role="alert"` dropped |
| 29 | component · `useSwitchStaff.component.test.tsx` | signs out, then opens sign-in with the desk as `next`; a failed sign-out keeps the session and says so | navigate before the sign-out |
| 30 | component · `pages/dashboard/routes.component.test.tsx` (M) | the desk's page for the owner and reception, titled «مكتب الاستقبال»; «تسجيل زيارة» in the bar below 768 px [role] [width] | the placeholder kept |
| 31 | component · `useUncollectedCard.component.test.tsx` | **counts the visits from the page's meta, no money total; three rows, then all; open on `#uncollected`** [money] [state] | a client sum in the title |
| 32 | same | **the owner sees «لن يُحصَّل…», reception does not** [role] | shown to reception |
| 33 | component · `useCollectDialog.component.test.tsx` | **pays the visit with its key; a remainder with no customer asks the phone; `VISIT_WRITTEN_OFF` and `VISIT_NOT_PRICED` worded** [money] [key] [state] | the phone not required |
| 34 | component · `useDebtDialog.component.test.tsx` | leaves the visit to the phone with the name; **no key, never re-sent after no answer**; `VISIT_HAS_CUSTOMER` worded | the transport retry enabled by a key |
| 35 | component · `useWriteOffDialog.component.test.tsx` | **requires a reason; the toast offers «تراجع», which undoes it once** | the toast's undo missing |
| 36 | same | **a write-off refused 403 for reception (shown by mistake) is worded** [role] | the 403 line left out |
| 37 | component · `UncollectedCard.component.test.tsx` | **«تحصيل» is the primary; each row's «⋯» named by the visit; the focus returns to it after its dialog; axe-clean at 390** [a11y] | focus left on `body` |
| 38 | component · `useUnpricedCard.component.test.tsx` | **read only for whoever may type a price; prices a visit with its reason; `VISIT_ALREADY_PRICED` worded** [role] | the query always enabled |
| 39 | unit · `dayWord.unit.test.ts` | today, yesterday, else the date, on Gaza's calendar | UTC date |
| 40 | unit · `shared/copy/catalogues.unit.test.ts` (existing) | the new sections' parity | (existing) |
| 41 | component · `useWriteOffDialog.component.test.tsx` | **a write-off or its undo with no answer is not re-sent by itself** [key] | a key added to the write-off |

### PR 2
| # | Lane · file | Title | Break |
|---|---|---|---|
| 42 | unit · `matchesPerson.unit.test.ts` | a name's part; a phone's last two digits or more for a check-in; a visit never by digits | digits matched anywhere |
| 43 | component · `usePresentMatches.component.test.tsx` | the people present who match, first group, none for an empty term | listed for an empty term |
| 44 | component · `useDeskSearch.component.test.tsx` | **asks the server only once typing pauses, leaves out the customers present, and makes the visit button primary only with no match** | a request per key |
| 45 | same | **a failed search says so with a retry; offline says so** [state] | the failure hidden as no match |
| 46 | component · `DeskSearch.component.test.tsx` | **the search is named and controls the results; the groups are `h2`, the cards `h3`; the count is polite; takes the focus from 768 px, not at 390; axe-clean** [a11y] [width] | `autoFocus` at every width |
| 47 | unit · `balanceView.unit.test.ts`, `statusView.unit.test.ts` | owes `warning`, credit `success`, settled `neutral`; each status its tone [money] | settled → `null` |
| 48 | component · `useSubscriberCheckIn.component.test.tsx` | **an active subscription checks in at once with one key per tap; none, expired or not started open the choice first** [key] [warn] | the dialog always |
| 49 | same | **`MEMBER_ALREADY_CHECKED_IN` says they are here; the warnings after are said; the search cleared and focused after** [state] [warn] | the search kept |
| 50 | component · `useCheckOutSubscriber.component.test.tsx` | **one tap, no key; the toast names the stay and what the subscription owes, with «استلام»; the focus to the next row's «خروج»** [money] [a11y] | focus left on `body` |
| 51 | unit · `progressLines.unit.test.ts` | each limit's line, the billing, and the end's line, in order | the end first |
| 52 | unit · `openItems.unit.test.ts` | unpaid visits oldest first, unpriced left out, then owing subscriptions [money] | unpriced kept |
| 53 | component · `usePayDialog.component.test.tsx` | **the debtors present first; one item per payment with its key; the amount follows the item until typed; a usage-based item takes more as credit** [money] [key] | the typed amount reset |

### PR 3
| # | Lane · file | Title | Break |
|---|---|---|---|
| 54 | unit · `customersQueryOf.unit.test.ts` | reads each filter; **`ARCHIVED` dropped for reception**; a value the server would refuse falls back; no default written [role] | `ARCHIVED` kept for reception |
| 55 | component · `useCustomersFilters.component.test.tsx` | a filter replaces the address and returns to page 1; the search after the pause | the page kept |
| 56 | component · `useCustomersList.component.test.tsx` | **loading, failure, empty, no match, archived empty; keeps the rows while the next page loads** [state] | one empty state |
| 57 | component · `CustomersList.component.test.tsx` | **five columns from 768 px, cards below; the status chips named; the filters a sheet below 768 px with the count; axe-clean at 390 and 1440** [width] [a11y] | the sheet at 1440 |
| 58 | unit · `termsLine.unit.test.ts`, `payStatus.unit.test.ts` | the terms' line and «بدون شروط إضافية»; paid, partly paid, unpaid [money] | partial when nothing paid |
| 59 | component · `useCustomerFile.component.test.tsx` | **the header's balance from one view; each subscription's due, paid and left from the server; «استلام المتبقي» only when it owes; a 404 is its own state** [money] [state] | the left computed |
| 60 | component · `CustomerFile.component.test.tsx` | **one `h1` (the page's), `h2` sections, `h3` cards; the breadcrumb named; axe-clean** [a11y] | cards with no heading |
| 61 | component · `routes.component.test.tsx` (M) | the file's route titled by the customer's name for both roles; the list's route [role] | the record title not given |
| 62 | component · `useEditDialog.component.test.tsx` | **sends only what changed, nothing when nothing did, `null` for a cleared phone; never re-sent after no answer; `PHONE_TAKEN` on the phone** [key] [state] | the whole form sent |
| 63 | component · `useArchiveFlow.component.test.tsx` | **settled: at once with «تراجع»; owing: the dialog naming the debt; present: its line; reception never offered** [role] [state] | the dialog skipped when owing |
| 64 | component · `CustomerMenu.component.test.tsx` | **named by the customer; «أرشفة…» destructive; focus back to the trigger** [a11y] | menu not named |
| 65 | component · `useStatement.component.test.tsx` | read only when opened; check-ins with «حاضر الآن»; **a voided payment struck with «ملغاة» and its reason** [money] [state] | voided counted as paid |
| 66 | component · `useEndDialog.component.test.tsx` | ends today, says the old end; never re-sent; the card refreshed | re-sent on no answer |
| 67 | component · `store` / `refresh` tests (M) | **a refresh refused `SESSION_IDLE` ends the session with `endedBy: 'idle'`; a sign-in clears it** [state] | `endedBy` not set |
| 68 | component · the sign-in page's test (M) | says why the session ended, only after an idle end | always shown |

### PR 4
| # | Lane · file | Title | Break |
|---|---|---|---|
| 69 | component · `Sheet.component.test.tsx` (M, S12) | the end sheet takes the full width below 768 px | `w-3/4` kept |
| 70 | component · `useOfferedPackages.component.test.tsx` | the offered packages only, in order | retired kept |
| 71 | unit · `endOf.unit.test.ts`, `packageLine.unit.test.ts` | 30 days from the 1st end on the 30th; a package's line with its limits [money] | off by one |
| 72 | unit · `sheetRequest.unit.test.ts` | **a package's request carries `packageId` only; custom carries its terms and reason; the payment is the recorded amount** [money] | custom with `packageId` |
| 73 | component · `useSubscriptionSheet.component.test.tsx` | **«مخصّص» offered only with `mayTypePrice`; the reason required** [role] | always offered |
| 74 | same | **a new customer then the subscription, two keys; the second refused keeps the first and sends the subscription alone** [key] [state] | one key for both |
| 75 | same | **the due is the prior debts plus the new price; the toast lists the parts and the debt from the answer, and the debt warning** [money] [warn] | the toast from the form |
| 76 | same | **a renewal sends `renewalOfId` and the statement's start; `SUBSCRIPTION_ALREADY_RENEWED` worded** [state] | the start computed |
| 77 | component · `SubscriptionSheet.component.test.tsx` | **titled by its mode; the first field focused; «بلا حدّ» with no warning icon; axe-clean at 390 and 1440** [a11y] [width] | autofocus off |

### Review Focus — inputs no planned test exercises
- A visitor checked in at 23:50 in Gaza, checked out after midnight (the due time closes it: the toast's stay).
- A quote opened, the tab hidden for 10 minutes, then «خروج» (the 60 s refetch paused while hidden).
- Two desks: one checks a visit out with a payment while the other's dialog is open (`VISIT_ALREADY_CLOSED`).
- 49 debts and a renewal paying them all (the allocation's cap).
- An English-only customer name in the Arabic interface in the card, the toast and the file's title (`lineParts`).
- A phone typed «0599 000 301», «+970599000301», «00970599000301» (one customer).
- The override set «حتى الإغلاق» five minutes before closing.
- A customers search of one digit; of 60 characters; of tashkeel only.
- A usage-based subscriber paying above the due (credit) and then checking out.

## 12. The commits

| PR | # | Subject (chars) | Body (why) |
|---|---|---|---|
| 1a | 1 | `feat(api): keep one idempotency key per intent` (47) | ADR 0015 rule 1 on the web (S4) |
| 1a | 2 | `feat(dashboard): add the page's bottom action bar` (49) | P1's «تسجيل زيارة» on a phone (S9) |
| 1a | 3 | `feat(occupancy): show the desk who is present` (45) | screen 13's present list and P2 (S1, S2) |
| 1a | 4 | `feat(desk): check visitors in and out at the desk` (49) | screen 13's visits, K2, the typed price's reason |
| 1b | 5 | `feat(desk): collect the uncollected visits` (42) | K6, DK-012, finding 110 |
| 1b | 6 | `feat(desk): price the unpriced visits` (37) | step 7's pricing on the web |
| 2 | 1 | `feat(occupancy): match the present to a search` (46) | K1's first group |
| 2 | 2 | `feat(desk): find customers from the desk's search` (49) | K1 |
| 2 | 3 | `feat(desk): check subscribers in and out` (40) | step 8's check-ins (S6) |
| 2 | 4 | `feat(desk): receive a payment on a customer's item` (50) | DK-012, a payment per item |
| 3 | 1 | `feat(desk): list the space's customers` (38) | screen 14 (S11) |
| 3 | 2 | `feat(desk): show a customer's file` (34) | screen 15 |
| 3 | 3 | `feat(desk): edit, archive and restore a customer` (48) | DK-014, P9, finding 123 |
| 3 | 4 | `feat(desk): show a subscription's statement` (43) | screen 15's statement; the end |
| 3 | 5 | `feat(session): say a session ended for idleness` (47) | the owner's revision of point 4 (spec C) |
| 4 | 1 | `feat(design-system): open the end sheet full width` (50) | DK-024, finding 101 (S12) |
| 4 | 2 | `feat(packages): offer the packages to the desk` (46) | the sheet's packages |
| 4 | 3 | `feat(desk): subscribe a new or known customer` (45) | screen 16, decision 3 |
| 4 | 4 | `feat(desk): renew a subscription with its debts` (47) | K3, DK-007 |

**PR titles:** 1a = commit 4's; 1b = commit 5's; PR 2 = commit 2's; PR 3 = commit 2's; PR 4 = commit 3's (with A1
not taken, PR 1 = commit 4's). **Recount each subject before committing (≤ 50)** — the table's counts are
the planner's; the executor's count decides. A unit's code, tests and docs in its commit. A fix before the push
folds into its commit (`git commit --fixup <sha>`, then `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash
origin/main`). No tool attribution. Stage by path; `git status` before each commit. **Carried items:** a
`C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\0_CARRIED_FROM_<n>.md` left by the previous PR's review is that
PR's first commit(s), each code fix red first, then green, with its break; the PR's description says "Carried
from #<n>". PR 1's carried file, if any, is the public fix PR's.

## 13. The procedure and the verification

Work in `C:\dev\masaha\app` only — never in `C:\dev\masaha\app-b` (worker B) or `C:\dev\masaha\app-design`
(reviewers and planners read there). Each commit message is a UTF-8 file **without a BOM, LF endings**, with a
body saying why, committed with `git commit -F <file>`. Scripts in `C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\
scripts\`, never committed; screenshots in `…\DESK_SCREENS\shots\pr<n>\`, never committed; the report
`…\DESK_SCREENS\4_REPORT_PR<n>.md`, written **as you go**.

### First checks (before any edit), each PR
1. `git status --short` clean in `C:\dev\masaha\app`; `git fetch origin`; `git switch main`; `git pull --ff-only`.
2. **What must have merged:** PR 1(a): the public fix PR (`gh pr list --state merged --search "head:fix/"`, the
   one the supervisor names); PR 1b: 1a; PR 2: PR 1(b); **PR 3: PR 2 and worker B's DESK_API** (`gh pr list
   --state merged --search DESK_API` or the PR the supervisor names; `git grep -n SESSION_IDLE origin/main --
   packages/shared` non-empty; finding 124 *Resolved*); **PR 4: PR 3, and spec D's PR if §14.4 took it**. Missing
   → **stop**.
3. **The base diff:** PR 1: `git diff --name-status 104d9d07 origin/main`; later PRs: from the previous PR's
   reported head. Read the previous `4_REPORT_PR<n>.md` for its departures. A code file this plan names changed in
   a way it does not cover → **stop and ask**. `packages/shared` changed → `npm run build -w @masaha/shared` before
   any web check, and re-read `packages/shared/src/{desk,visits,occupancy,customers,subscriptions,payments,
   packages,core}` against §10; a difference → **stop**.
4. **Open PRs:** `gh pr list --state open --json number,headRefName,files`; one that edits a code file of this PR
   → **stop and ask**; note the others' heads for the conflict check.
5. **Checks against the code, each with its fallback:**
   - a. `crypto.randomUUID` exists in the component lane (jsdom on Node 24). Else **stop and ask** (no polyfill
     only for tests).
   - b. `api` has no call answering an optional `meta` (commit 1 adds `postWithMeta`). If one exists, use it.
   - c. The layer's `Alert` passes `role` through. Else the failure's container `div role="alert"` wraps it.
   - d. The `Toaster` can be raised above a bottom bar (`offset`/`mobileOffset`, SH-012). Else **stop and ask**
     (a design-system change).
   - e. `DataTable`'s `label` is an `aria-label` only (read: it is), so DI-1's distinct label holds.
   - f. `VISIT_ROUNDINGS`' values and `spaceSettings`' words for them; the check-out reuses them by key.
   - g. Whether `@masaha/shared` exports the directory's search fold; else `matchesPerson` trims and compares.
   - h. Whether `shared/lib` has a day formatter; else `features/desk/services/dayText.ts`.
   - i. `RequireAuth` sends a guest to sign-in with the page as `next`, and `SIGN_IN_PATH` takes `?next=`. Else
     «تبديل الموظف» navigates to `SIGN_IN_PATH` plainly; a departure.
   - j. `CardTitle` renders the heading level it is given (SH-017). Else the heading inside it.
   - k. Radix's `Dialog` marks the rest of the page hidden (`aria-hidden` outside) — AX-009. Recorded.
   - l. `useMediaQuery` is exported by the layer (PUBLIC's S6). Else **stop**.
   - m. eslint lets a dashboard-only feature import `@shared/design-system/data`. Else **stop**.
   - n. PR 3: the sign-in page's file (`git grep -n SignInForm apps/web/src/pages/site`).
   - o. PR 4: `useSpaceShifts('owner', id)` answers reception (the managed read is 🧾). Else **stop**.
6. **Finding numbers:** the index's highest; this item's are 160 and on. If taken, the next free ones, said.
7. **The data inventory (read-only, before any edit).** `docker start masaha-postgres-1` (never `npm run db:up`,
   never `npm ci`); `npx prisma migrate status` in `apps/api` — pending → `npx prisma migrate deploy` then `npx
   prisma generate` (worker A's `masaha_dev` to `main`); the API on 3320 (`npm run dev -w @masaha/api`). A script
   signs in (`POST /api/v1/auth/login`) as `demo-owner@example.com` and `demo-reception@example.com` (the demo's
   password from `apps/api/.env`, never printed or written to the report) and reads, with `GET`s only: the
   occupancy, the visit terms, the uncollected and unpriced visits, the customers (every page), each file, the
   packages; and, as `demo-directory-owner@example.com`, `GET /manage/spaces` and each space's occupancy. It
   records, for each case of this PR's real run (below), the space and the record that holds it. **A case the data
   does not hold → stop and report** — never change data through the app, the API or the seed to get past it.
   Stop the API by its process id.
8. **Branch:** `git switch --no-track -c <branch> origin/main`.

### Per commit
`npm run lint` and `npm run typecheck`; focused runs of the touched test files; each new test seen red first,
its red line recorded; each break of §11 made, its red output recorded, then restored.

### On the head, once each
First: no `vitest`, `tsc` or dev server of `C:\dev\masaha\app-b\` runs —
`Get-CimInstance Win32_Process -Filter "Name='node.exe'" | Where-Object { $_.CommandLine -match 'app-b' }` empty
(else wait; never stop worker B's processes); then the free memory, recorded —
`(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory` — **before each full lane**; one full lane at a time.
Then: `npm run test:unit` · `npm run test:component` (record the time of `pages/dashboard/routes.component.test.tsx`
› "lists the owner's eleven pages", finding 87) · `$env:NODE_ENV='production'; npm run build; Remove-Item
Env:NODE_ENV` · `npm run check:build` (the desk's code stays out of the site's first download) · `npm run
check:classes` · `npm run format:check` · `npm run check:links`.
- **The first download, recorded** (manifest: the entry and its static imports, bytes, base and head): no
  `features/desk` module, no `data-table`, no `dashboard`. PR 1a also records whether the new chunks join finding
  27's cycle.
- **Not run:** `test:api` (no API or shared change; CI runs it).

### The real run
- `docker start masaha-postgres-1`; the API on 3320; the web on 5320 (`npm run dev`), worker A's `masaha_dev`.
- **Browser:** local headless Chrome over CDP, a script in `scripts\` on the model of
  `WORKER_A\PUBLIC\scripts\run2b.mjs` (Enter sent with `text: '\r'`); say which. **As the owner and as reception;
  Arabic light and English dark; at 390, 768 and 1440** for every layout that changes with width (the desk's top
  bar and bottom bar, the present list's table and cards, the `xl` side column at 1440, the customers list, the
  file, the sheet). **The network log** of each case: every request's method, URL, status and `Idempotency-Key`
  (the proof that a retry and a double press reuse one key: CDP `Network.emulateNetworkConditions` offline for
  the first send of a check-in, then online and «إعادة المحاولة» → two requests, one key, one visit).
- **The writes, each named, on `masaha-demo` unless said** (and only these):
  - PR 1a: as reception — check in «زائر تجربة 1» (then out, paid cash, the change line) and «زائر تجربة 2» (out
    with 0 received, name «زائر تجربة 2», phone `+970599000301`: a new customer with a debt); as owner — set the
    override «ممتلئ» 30 min, then back to automatic; a check-in at the directory set's closure space as
    `demo-directory-owner` («زائر تجربة 3», for `CLOSURE_IN_FORCE`), checked out unpaid with phone
    `+970599000302`. FULL as the owner of the directory set's full space (capacity 4): one check-in «زائر تجربة
    4» (the warning), checked out. **FULL as reception: not performed** (no reception account on a full space;
    tests 21 and 12 prove it).
  - PR 1b: as owner — on the uncollected visit «خالد»: «لن يُحصَّل…» with a reason, then «تراجع»; as reception —
    «تسجيل دين» with phone `+970599000303`, then «تحصيل» 10 ₪ cash; the unpriced case only if the inventory finds
    a visit with no charge (else **not performed**, test 38 proves it).
  - PR 2: as reception — search «سارة» (her card), «حضور» (a warning if her limits say), «خروج» (her usage-based
    subscription's balance and «استلام» 5 ₪); «يوسف» checked in and out; «رامي»'s visit debt paid from «استلام
    دفعة».
  - PR 3: as owner — edit «نور حسن»'s phone to `+970599000304`, then back to none; archive «زائر تجربة 1»'s
    customer if one exists, else the customer made in PR 1a (owes → the dialog), then restore; end no subscription
    of the seed's four (the end is proven by test 66) — or, if the owner allows one write more, end
    «يوسف»'s; as reception — the list's filters, a file, a statement.
  - PR 4: as reception — a new customer «مشترك تجربة» (`+970599000305`) on «أسبوعي», paid in full; «محمد عوض»'s
    renewal with his debt (partial: the toast's parts); as owner — «مخصّص» with a reason.
- **Width breaks in the real run** (layouts drawn by classes): PR 1 — the desk body's `xl:grid-cols-12` removed
  once (the 1440 screenshot shows one column), restored; PR 3 — the file's cards' grid. Each `break-<what>.png`.
- **Touch targets (DI-16):** at 390 with touch emulation (`Emulation.setTouchEmulationEnabled`), the computed
  height of «خروج», «تحصيل», «تسجيل دين» and the bottom bar's button ≥ 44 px, recorded.
- **Not performed, by design:** FULL as reception; a 429 (test 27's path); a lost answer on a payment (test 20's
  path, the check-in shows it live); the idle sign-out (PR 3: needs 15 minutes — performed **only** if DESK_API is
  merged and the run can wait; else test 67 owns it). Any other case not performed → the stop rule.
- Screenshots `<pr>-<case>-<owner|reception>-<ar-light|en-dark>-<width>.png`. Stop the servers by process id
  (`Get-CimInstance Win32_Process -Filter "Name='node.exe'" | Where-Object { $_.CommandLine -match
  'C:\\dev\\masaha\\app\\' }`, `Stop-Process -Id …`); `Get-NetTCPConnection -LocalPort 3320,5320 -State Listen`
  empty; `git status --short` clean.

### Push and the PR
1. `git grep -n "#PRNUM" HEAD`; the next number: `gh api "repos/{owner}/{repo}/issues?state=all&per_page=1&sort=
   created&direction=desc" --jq '.[0].number'` + 1 (worker B may take it first: check at that moment).
2. `#PRNUM` replaced per commit tree by a self-checking script in `scripts\` on the model of
   `WORKER_A\PUBLIC\scripts\prnum3b.sh` (`git filter-branch -f --tree-filter …` over `origin/main..HEAD`, then
   `git update-ref -d refs/original/refs/heads/<branch>`; it fails unless `git grep -n "#PRNUM" HEAD` is empty and
   `git diff origin/main --stat` lists the same files as before).
3. `git push -u origin <branch>`; `gh pr create --assignee @me --label feat --label area:web --label area:docs`
   (+ `--label area:design-system` on PR 4 with S12), the title §12's; the description per workflow §3 (Summary;
   Scope / Acceptance criteria / Out of scope; Change type; Evidence — run and not run; Screenshots — attached by
   the owner; the Definition of Done) and, for PR 1a, §4.5's line for `OPEN_DECISIONS.md`. Confirm the number.
4. `gh pr checks <n>` green on the pushed head's SHA; `gh pr view <n> --json mergeStateStatus` → `CLEAN`.
5. The conflict check: for each other open PR, `git fetch origin <its head ref>` and `git merge-tree --write-tree
   origin/<branch> origin/<other>`; recorded.
6. The report, written as you go. **Never merge.** Each PR is reviewed in a separate conversation.

### The stop rule (as `WORKER_A\PUBLIC\3_EXEC_PROMPT_PR4.md` §2)

**A test you cannot run stops the work.** A test **failing** because its code is not written yet is the plan's
red step — normal. A test, lane or command you **cannot run** is not: it errors before any test runs (the database
unreachable, Docker down, a port taken, a module or `dist` missing, a migration pending, `No test files found`, a
Vitest or TypeScript startup error, the whole run timing out, a crash with no result); a break you could not make
or run; a real-run case you could not perform (other than those §13 names). **Then stop at once** — never skip,
`.skip` or delete a test, never change a config, a timeout, `.env`, a script or a lane, never mock what the plan
does not, never run a narrower command and call it the lane, never call it "flaky" and move on. Write the
command, its exact error and where you were into the report, and reply `Status: STOPPED`.

**The owner's standing exceptions:**
- `routes.component.test.tsx` › "lists the owner's eleven pages" (finding 87) may miss its 3 s locally when the
  machine is loaded. If **only that test** fails and it passes alone, record both runs (times, free memory) and go
  on; **CI's `test:component` is the judge** — if it fails there, stop.
- A run **killed for low memory** is re-run **once** when the machine is quieter (no `vitest` of
  `C:\dev\masaha\app-b\` running, the free memory recorded); killed again → record it, carry on, and CI's run of
  that lane on the pushed head is the judge — red there → stop.

**A plan that proves false against the code:** stop, say exactly what and why, and offer the fix — do not choose
it yourself. **A break that stays green:** stop — unless it is plainly your own test's defect, or the plan's break
cannot change the outcome; then make the break that can, see it red, and state it as a departure. **A design
issue, a carried item or a review point you would leave undone: stop and ask.** **Never claim a result you did
not see:** a command passed only if its own output said so (its exit code); a break counts only when seen red; a
scoped lane with failures is not green — name each failing file and test.

**A demo account or demo data that does not hold what a real-run case needs → stop and report;** never change
data through the app, the API or the seed to get past it. The real run's own writes are only §13's list.

### Stop and ask
- What must have merged has not (check 2); a base diff changes a code file this plan names in a way it does not
  cover; an open PR edits one of this PR's code files.
- Anything would need `apps/api`, `packages/shared`, the schema, a migration, the seed, a dependency,
  `shared/copy/*/errors.ts`, or a design-system change beyond S12 (PR 4, if approved).
- `packages/shared`'s desk, visits, occupancy, customers, subscriptions, payments or packages types differ from
  §10's use (worker B's step 9 may change `payments`).
- Check 5's a, d, l, m or o fails; the data inventory lacks a case (check 7).
- `check:build` fails because a module of this item reaches the site's first download.
- A server answer the contract does not list reaches a dialog (a code with no catalogue line).
- Three fixes of one failure have failed; a decision this plan does not settle.

## 14. Decisions needed from the owner

1. **The plan as written,** with S1–S13 — above all **S1** (the `desk` web feature spans the desk's screens;
   architecture §3's naming rule gains its exception) and **S4** (one key per intent, kept across an edit of the
   open form). *Recommend:* approve.
2. **A1 — PR 1 split in two** (≈ 58 and ≈ 32 files). *Recommend:* take it.
3. **Finding 125: (c), no preview** (§6's table), or (b) with spec A for worker B before PR 4. *Recommend:* (c).
4. **Spec D — subscribing from the published week and month prices.** The glossary and the data model say they are
   the public packages; the API (#106) takes only a package or custom terms, so reception — who may not type a
   price — cannot sell the month that is on the space's public page. Options: (a) spec D before PR 4 (worker B,
   S–M), the month 30 days and the week 7, both counted; (b) v1 as built: the owner keeps a package for each
   published price, finding 165. *Recommend:* (a).
5. **Worker B's DESK_API item** (specs B and C, one migration: `sessions.lastActivityAt`), merged before PR 3;
   its place in worker B's queue (before step 9's API, or after). *Recommend:* before step 9 — PR 3 waits on it.
6. **The design issues DI-1 … DI-53,** each as written (§8).
7. **The Arabic copy of §10,** every line (localisation › Catalogues).
8. **The documents this decision set changes:** architecture §3 (S1's exception), §2 (the bottom bar), §4
   (`endedBy`), §7 (one key per intent, the desk's polling built); and the supervisor's line for
   `OPEN_DECISIONS.md` point 4 (§4.5).
9. **S12 — the end sheet full width below 768 px in PR 4** (a design-system commit, `area:design-system`;
   finding 101 resolved). *Recommend:* take it.
10. **A3 / A4 — the desk's capacity and an uncollected total in customers' view** (R2-DK-TR-001, -002): keep
    «27 / 40» as settled and no total (DI-3), or hide the capacity too. *Recommend:* keep as settled; DI-3 stands.
11. **The real run's writes** on the demo data (§13), FULL as reception not performed, and «يوسف»'s subscription
    ended only if the owner allows that one extra write.

## Appendix — steps mapped to Claude Code skills (only a map; no step depends on them)

| Step | Skill (if present) |
|---|---|
| Before the branch | `start-work-item` (its git checks; the plan is already saved) |
| Each test red first; each break | Superpowers `test-driven-development` (with `writing-good-tests.md`), per workflow §10 |
| A failure or a flake | `systematic-debugging` |
| Claims in the report and the PR | `verification-before-completion` |
| Opening the PR, its self-review, a conflict with `main` | `open-pr` |
| After CI is green and `CLEAN` | `final-report` |
| The real run's screenshots | `run`, or the Chrome tools; else headless Chrome over CDP |
