# DESK_SCREENS — PR 1a report (`feat/desk-visits`)

**Status: STOPPED at §13 first check 7 (the data inventory), before any branch or edit.**
Written 2026-10-24, about 13:54 UTC (16:54 Gaza).

## Where the work stands

- `C:\dev\masaha\app` on `main` at `5c0cdcba` (#113 merged), clean. No branch cut, no file edited, no commit.
- The API ran on 3320 only for the inventory. It is stopped by its process ids (19396 tsx watch, 1380 the
  server, 12436 pino-pretty). Ports 3320 and 5320 are free. `masaha-postgres-1` is still running.
- Nothing written to `masaha_dev`: the inventory sent sign-ins and `GET`s only.

## Preconditions

- `git fetch`, `git switch main`, `git pull --ff-only`: fast-forwarded from `104d9d07` to `5c0cdcba`.
- `npm run build -w @masaha/shared`: ran (`tsc -p tsconfig.build.json`, exit 0).
- No `0_CARRIED_FROM_*.md` in this folder: nothing carried. Check 2 is replaced by the approval note, so
  nothing had to merge first.

## First checks

- **1** ✔ clean, fetched, on `main`, pulled.
- **3 — the base diff** `git diff --name-status 104d9d07 origin/main`: only #113 (chore/conflict-guard):
  `.github/workflows/ci.yml`, `CLAUDE.md`, `apps/api/package.json`, `apps/api/scripts/checkConflicts.ts`
  (+ unit test), findings 137 and 138 (A) and the findings `README.md`, `docs/design/INDEX.md`,
  `docs/development/setup.md`, `docs/development/workflow.md`, `docs/features/lookups.md`,
  `docs/frontend/architecture.md` (one line: "(2026-10-24, #111)" on `RetryState`'s line), `package.json`.
  No web code file and no `packages/shared` file changed. ✔ `npm run check:conflicts` now exists on `main`.
- **4 — open PRs:** `gh pr list --state open` → `[]`. No open PR (worker B's `feat/payments` was not open). ✔
- **5a** ✔ `crypto.randomUUID` is a function in jsdom 30.1.1 on Node 24.
- **5b** ✔ `api` (`shared/api/client/request.ts`) has no call that answers an optional `meta`
  (`getPage` rejects without one). Commit 1 adds `postWithMeta`, as planned.
- **5c** ✔ `Alert` sets `role="alert"` for `destructive` and passes `role` through (`{...props}` after it).
- **5d** ✔ `Toaster` passes the other props to Sonner 2.0.8, whose props include `offset` and `mobileOffset`.
- **5e** ✔ `DataTable`'s `label` is only the `aria-label` of the table (and of the cards' `ul`).
- **5f** ✔ `VISIT_ROUNDINGS` = `UP_AFTER_MINUTES`, `NEAREST_HALF_HOUR`, `PER_MINUTE`
  (`@masaha/shared/space-settings`). `spaceSettings.pricing` words them: `upAfter`, `half`, `minute`.
- **5g** `@masaha/shared` exports no search fold → PR 2's `matchesPerson` trims and compares (the plan's fallback).
- **5h** `shared/lib` has no day formatter (it has `clockOf` and `updatedAgo`) → PR 1b's `dayText.ts` (the
  fallback).
- **5i** ✔ `RequireAuth` sends a guest to `signInPath(place)`, which is `/login?next=…`
  (`shared/routing/returnUrl.ts`, tests in `RequireSpaceRole.component.test.tsx`). `SIGN_IN_PATH` is exported.
- **5j** `CardTitle` is a `div` and does not take a heading level → the heading goes inside it (the fallback).
- **5k** Recorded: the layer's `Dialog` is Radix's, which hides the rest of the page from assistive
  technology while open (`hideOthers`).
- **5l** ✔ `useMediaQuery` is exported by `@shared/design-system`.
- **5m** ✔ eslint's `zoneEntries` lets a feature import the layer's `index.ts` and `data.ts`.
  `features/staff/components/StaffList.tsx` already imports `@shared/design-system/data`.
- **6 — finding numbers:** the index's highest is 138. 160 and up are free.

## Check 7 — the data inventory (read-only) → STOP

Docker: `docker start masaha-postgres-1`. `npx prisma migrate status` in `apps/api`: "25 migrations found …
Database schema is up to date!". API on 3320 (`npm run dev -w @masaha/api`), `/health` ok.
Script: `scripts\inventory1a.mjs`. Output: `scripts\inventory1a.out.txt` (no password in it).

What the data holds for PR 1a's cases:

| Case (§13 PR 1a writes) | Space / record | Holds? |
|---|---|---|
| Reception checks in «زائر تجربة 1», out paid cash with change | `masaha-demo` (7), reception id 15; status `AVAILABLE`, capacity 40, 0 present; rates ₪5/h, ₪25/day (student ₪4 / ₪20); 3 shifts (1 صباحي 480–960, 2 مسائي 960–1320, 5 مسائية 960–1200); `mayTypePrice: false` for reception | ✔ |
| Reception: «زائر تجربة 2» out with 0, phone `+970599000301` (new customer with a debt) | `masaha-demo`. Its 5 customers' phones are …201, …202, …204 (`+970569000204`), …205 and none, so …301 is new | ✔ |
| Owner sets the override «ممتلئ» 30 min, then back to automatic | `masaha-demo`, owner id 14, status `AVAILABLE` (open now), no override | ✔ (while it is open) |
| `CLOSURE_IN_FORCE`: «زائر تجربة 3» as `demo-directory-owner`, out unpaid, `+970599000302` | `shati-sea-view` (52): status `CLOSED`, a running closure (`running: 1`) | ✔ |
| **FULL as owner:** one check-in «زائر تجربة 4» at the directory set's full space (capacity 4), with the warning | **`sada-space` (49): capacity 4, but 0 present, status `AVAILABLE`** | **✘** |
| FULL as reception | not performed by design (tests 21 and 12) | — |

**Why FULL as owner cannot happen.** The API warns `SPACE_FULL` when the people present *before* the new
check-in are as many as the capacity (`occupancy.service.ts` › `checkInWarnings`: `isFull(count, capacity)`,
counted before the visit is inserted). The seed (`demoDirectory.ts`, `sada-space`: "As many present as it
holds: full", `present: 4`) creates 4 open visits "checked in within today, so no auto check-out has closed
them". Those visits have closed since the seed ran, so today nobody is present at `sada-space`. Checking in
«زائر تجربة 4» would give no warning. None of the 13 directory spaces has anyone present
(`present=0` everywhere), so no other full space exists either.

The rules (prompt §1.8, plan §13 check 7 and *Stop and ask*) allow "not performed, by design" only for FULL
as reception, and forbid changing data to get past a case. So I stopped here.

## What the owner must decide (one of these)

1. **Mark FULL as owner "not performed, by design" too,** like FULL as reception. Tests 21 (the warnings in
   the toast) and 12 prove it in the component lane. The real run would still show one live warning,
   `CLOSURE_IN_FORCE` at `shati-sea-view`, which goes through the same toast path as `SPACE_FULL`.
   *(My recommendation: the toast's warning path is the same for every code, and the closure case shows it live.)*
2. **Allow four more real-run writes:** check in four visitors at `sada-space` as `demo-directory-owner`
   (for example «زائر تجربة 4أ…د»). The fifth, «زائر تجربة 4», then gets `SPACE_FULL`, and all five are
   checked out afterwards. These are writes the plan does not list, so only the owner can allow them.
3. **The owner re-runs the demo seed** for the directory set (`SEED_DEMO=true npm run db:seed`) on the day of
   the run. That brings `sada-space`'s 4 present back. It is a data change I may not make myself.

Once the owner decides, the work starts again at §13 check 8 (the branch). Checks 1–6 above stay valid unless
`main` moves. If it moves, run check 3 and check 4 again.

## Resumed — the owner's decision (option 1)

**FULL as the owner: NOT PERFORMED, by design**, proven by tests 21 and 12; `CLOSURE_IN_FORCE` at
`shati-sea-view` shows the warning toast live. `origin/main` still `5c0cdcba`, no open PR (checks 3 and 4 hold).
Check 8: `git switch --no-track -c feat/desk-visits origin/main`.

## Commit 1 — `74029488` feat(api): keep one idempotency key per intent (46)

- Red before the code (tests 1, 2, 3): `withIdempotencyKey.unit.test.ts` "Cannot find module './withIdempotencyKey'";
  `useIntentKey.component.test.tsx` "Failed to resolve import './useIntentKey'"; `request.unit.test.ts` ›
  "hand back a POST's data and its meta…" `TypeError: warned.api.postWithMeta is not a function`.
- Green after: `test:unit -- src/shared/api` "Test Files 8 passed (8) · Tests 55 passed (55)";
  `test:component -- src/shared/api/idempotency` "Tests 1 passed (1)"; `npm run lint` exit 0; `npm run typecheck` exit 0.
- A lint fix on the way: `@typescript-eslint/no-unnecessary-type-parameters` on `postWithMeta`'s return type →
  the `WithMeta<T, M>` alias (as `getPage`'s `Page<T, M>`), exported beside `Page`.
- **Owner's decision (asked mid-run, S9's toast raise):** "Raise only with the bar" — a small store the bar sets on
  mount; `app/providers.tsx` passes the `Toaster` `offset`/`mobileOffset` bottom 5.5rem only while it is shown
  (the prototype's `PageToaster`). A departure in files: `app/providers.tsx` and the store, in commit 2.

## Commit 2 — `98f66858` feat(dashboard): add the page's bottom action bar (49)

- Red before the code (test 4): `DashboardLayout.component.test.tsx` "Failed to resolve import './PageActionBar'".
- Green after: `test:component -- src/pages/dashboard/shell` "Tests 6 passed (6)"; lint exit 0; typecheck exit 0;
  `prettier --check apps/web/src docs/frontend/architecture.md` "All matched files use Prettier code style!".
- **Break [width]** (`hidden={false}`, the bar always drawn): red — "× draws no bar for a page with no action …
  expect(element).not.toBeVisible() Received element is visible" (`scripts\break-4.txt`); restored from the
  `cp` backup, green "Tests 3 passed (3)".
- **Departure (the owner's choice):** `app/providers.tsx` (the Toaster's `offset`/`mobileOffset` 5.5rem while a bar
  shows) and `shared/routing/actionBar/actionBarShown.ts` (`showActionBar`, `useActionBarShown`), added to the files.
  The store sits in `shared/routing` because a file of `pages/dashboard/shell` would put dashboard code in the
  first download (`isDashboardModule`), and `shared/` may not import `pages/`. Test 4 also proves the store follows
  the bar ("Bar shown" / "No bar").

## Commit 3 — `15898ed4` feat(occupancy): show the desk who is present (45)

- Red before the code: unit — `occupancyRepository.unit.test.ts` "TypeError: repository.stateNow is not a function"
  (test 5); `stayDuration`/`overrideLeft` "Cannot find module" (test 9). Component — "Failed to resolve import"
  for `./useStateNowQuery`, `./usePresentList`, `./useLiveStatusControl`, `./PresentList`, `./LiveStatusControl`
  (tests 6, 7, 8, 10, 11, 12, 13).
- Green after: `test:component -- src/features/occupancy` "Tests 16 passed (16)"; `test:unit -- src/features/occupancy
  src/shared/copy` "Tests 41 passed (41)" (test 40, the catalogues' parity, among them); lint exit 0; typecheck exit 0.
- Breaks (`scripts\breaks.py`, each restored from its copy and checked byte-equal; outputs `scripts\break-<n>.txt`):
  6a `refetchIntervalInBackground: true` → red "× reads again every 30 s …"; 6b `refetchOnWindowFocus: false` → red,
  same test; 7 → red "× lists people … charge so far from the server"; 8 rows dropped on a failed refetch → red
  "× keeps the rows after a failed refresh"; 10 the table labelled «Present now» → red (both PresentList tests);
  12 enabled while closed → red "× is disabled with its reason while the space is closed"; 13 `aria-label` left out
  → red (3 LiveStatusControl tests).
- **Departure, break 7:** the plan's break "the charge computed from the rates" cannot be made (the state now carries
  no rates), so the break computes a charge in the browser from the stay (`hours × ₪5`); it went red.
- Fixes on the way, before the commit: the popover's dialog had no name (axe `aria-dialog-name`) → named by its
  title; a single-choice `ToggleGroup` is a `radiogroup` (the test asked for `group`); the heading needed a space before
  its count; lint: no state set synchronously in the tick's effect (the clock now ticks every 30 s throughout),
  `useMutation` without `void`, the language narrowed to `'ar' | 'en'`.

## Commit 4 — `b12ddf50` feat(desk): check visitors in and out at the desk (49)

- Red before the code: unit — "Cannot find module" for `./deskRepository` (test 19), `./visitRates` (14),
  `./currentShift` (15), `./moneyOf` (16), `./quoteAge` (17), `./warningLines` (18), `./deskRefusal`. Component —
  "Failed to resolve import" for `./useMoneyBlock` (22), `../../components/visit/VisitDialog` (20, 21),
  `../../components/check-out/CheckOutDialog` (23–28), `./useSwitchStaff` (29); routes (30) — "× shows the owner
  the desk under its title …", "× shows reception …", "× puts «Check in a visit» in the bar …" (the placeholder kept).
- Green after: `test:unit -- src/features/desk src/shared/copy` "Tests 52 passed (52)";
  `test:component -- src/features/desk src/features/occupancy src/pages/dashboard` "Tests 3 failed | 105 passed (108)"
  — the 3 are `routes.component.test.tsx`'s first tests ("lists the owner's eleven pages", "lists reception's four
  pages", "shows the admin the lookups page"), each with an empty `<body>` (the lazy shell not loaded within 3 s;
  free memory 4 152 740 KB); the routes file alone: "Tests 49 passed (49)", 24.44 s. Finding 87's case; the head's
  run and CI judge. `npm run lint` exit 0; `npm run typecheck` exit 0; `format:check` passed; `check:links` "2695 links …
  all resolve".
- Breaks, each red, each restored (`scripts\breaks_c4.py`, `breaks_c4b.py`, outputs `scripts\break-<n>.txt`): 14 student
  always → red; 15 UTC hours → red (3 tests); 16 recorded = received → red; 17 the bound at 5 min → red; 18 sorted →
  red; 19 the key dropped on the check-out → red; 20 `renew()` in `submit` → red; 21 warnings ignored → red; 22 follows
  the due after typing → red; 27 one generic line → red (2); 28 the failure not an alert → red; 29 navigate before
  the sign-out → red (the failure test); 30 the placeholder kept → red (3); S10 focus not moved → red. 23–26 were made
  twice: before the lint restructuring of the check-out's hook and again after it (23b–26b), each red.
- **Departures in commit 4:**
  - **Break 26:** "the reason not required" cannot change the outcome (the contract's schema requires the reason, so
    the form is blocked anyway); the break that can — the typed charge not sent — went red.
  - **Break 29:** "navigate before the sign-out" leaves the success test green (the same request and the same final
    address); it went red in the failure test (the address left the desk with the session kept).
  - **Copy beyond §10:** `desk.checkOut.open` «خروج» / "Check out" and `desk.checkOut.openName({name})` «خروج {name}» —
    §10 names the button (DI-16, test 10) but its table has no line for it; `desk.checkOut.rounding.UP_AFTER_MINUTES`
    is §10's `checkOut.rounding` line, keyed by its rule.
  - **`types/DeskAbilities.ts` not added:** nothing in 1a reads `writeOff` or `archive` (1b's write-off, PR 3's
    archive); a type nothing uses is not added (the owner's no-unused-code rule). It comes with 1b's write-off.
  - **S10's focus rule in `occupancy`'s `PresentList`** (a commit-3 file, changed in commit 4 with its own test): the
    person whose «خروج» had the focus leaves the list → the next row's «خروج», else the heading.
  - **`useStateNowQuery` exported from `occupancy`:** the page passes `full` (the status `FULL`) to the check-in, as §10
    says ("from the page"); the same query, no extra request.
  - **The routes test's `signIn` transport** now answers the desk's two reads (occupancy, visit terms): reception lands
    on the desk, which is no longer a placeholder.
  - **Lint restructuring:** the check-out's hook keeps no ref (the React compiler's `react-hooks/refs`): the form holds
    `typing` and `needsDebt`, set in an effect, and `submit` adds the quote's time and the payment.

## STOPPED — the size bound (prompt §1.5)

`git diff --stat origin/main`: **90 files changed** (4 907 insertions, 27 deletions) — past the bound of 72. By area:
features/desk 34 (16 tests), features/occupancy 21 (8 tests), pages 10, shared/api 7, shared/copy 6, docs 8,
shared/routing 2, app 1, test 1. By commit: 1 → 8, 2 → 8, 3 → 27, 4 → 55. The plan's ≈ 58 counted commit 3 at ≈ 26
and commit 4 at ≈ 45; the excess is mostly commit 4's test files and services (a test beside each file, as the plan
lists them) and the documents. Nothing is pushed.
- **Owner's decision (asked):** "Keep PR 1a at 90 files". Work resumes at the head's checks.

## On the head (`b12ddf50`)

No `vitest`/`tsc`/dev server of `app-b` running (0 processes); free memory before each lane: 3 306 712 KB (unit),
3 588 152 KB (component).
- `npm run test:unit -w @masaha/web` → "Test Files 125 passed (125) · Tests 946 passed (946)", 33.61 s.
- `npm run test:component -w @masaha/web -- src/shared/api src/features/occupancy src/features/desk src/pages/dashboard
  src/shared/copy src/shared/routing src/app` (the prompt's folders, plus `src/shared/routing` and `src/app`, whose files
  this PR changes) → "Tests 1 failed | 179 passed (180)", 72.63 s: **`src/app/App.component.test.tsx` › "renders the
  main landmark"** — "Unable to find role="main"" at 3 070 ms (the home page's lazy chunk not loaded in 3 s). Alone:
  `npm run test:component -w @masaha/web -- src/app/App` → "Tests 2 passed (2)", 15.39 s. It renders the app at `/`
  and waits for the lazy page, finding 87's pattern, but it is **not one of the tests the standing exception names**
  — said here plainly. CI's full `test:component` on the pushed head is the judge; red there → stop.
  The routes file's "lists the owner's eleven pages" passed in this run.
- `$env:NODE_ENV='production'; npm run build; Remove-Item Env:NODE_ENV` → exit 0.
- `npm run check:build` → "No showcase code in 57 build files (1017 strings checked). No dashboard code in the site's
  first download. No data-table or leaflet, nor Leaflet's stylesheet, in the site's first download."
- `npm run check:classes` → "No physical direction or arbitrary-value classes in 1302 files."
- `npm run format:check` → "All matched files use Prettier code style!"
- `npm run check:links` → "2695 links in 220 documents and 1857 source files all resolve."
- `npm run check:conflicts` → "No conflict markers found."
- **The first download** (`scripts\firstDownload-base.txt`, `firstDownload-head2.txt`; base = `origin/main` `b2f13a47`
  built the same way): 1 011 159 → 1 024 544 bytes (+13 385), 6 chunks both: `index` +565, `index.css` +259,
  `jsx-runtime` +11 733, `routing` +792, `design-system` +36. The `jsx-runtime` growth is the copy catalogue's new
  `desk` and `occupancy` sections, in both languages (their lines are found in that chunk), as every catalogue section
  ships; no `features/desk` module, no `data-table`, no `dashboard` in the first download. Finding 27: "space shell
  chunks: none" at base and head, one dashboard chunk — the new pages joined no cycle.
- **`main` moved during the run:** `origin/main` is now `b2f13a47` (#115 chore/demo-daily: `apps/api/src/db/seed/
  demoDirectory.ts` + its test, `docs/development/setup.md`). No file of this PR, nothing deleted or renamed: a
  merge apart, no rebase (workflow §9).
- **Open PR #114** `feat/payments` (worker B, head `8ae243f0`): shares no code file with this PR; shared documents:
  `docs/README.md`, `docs/features/desk.md`, `docs/features/visits.md`, `docs/project/overview.md`. Its
  `packages/shared/src/payments` changes only add (`voidPaymentSchema`, `paymentsQuerySchema`, `PaymentRow`, …); the
  types this PR reads (`VisitPayment`, `PAYMENT_METHODS`, `paymentSchema`) are unchanged.

## The real run (local headless Chrome over CDP; `scripts\run1a.mjs` on `scripts\cdp1a.mjs`, PUBLIC's `cdp4.mjs` model)

API on 3320 and web on 5320 (`npm run dev`), worker A's `masaha_dev` (`prisma migrate status` up to date). Enter is
sent with its text where a key is used; a sign-in takes the account's language, so each case sets its language and
theme again after signing in and reads the desk anew. Screenshots in `shots\pr1a\`; each case's output
`scripts\run1a-<case>.txt`.

| Case | Who · where | Result | Screenshots |
|---|---|---|---|
| Offline first send, then «إعادة المحاولة» | reception · `masaha-demo` · ar light 1440 | the dialog said «لم يصل الرد. أعد المحاولة — لن تُسجَّل مرتين.» with «إعادة المحاولة»; online, the retry checked «زائر تجربة 1» in; one row of them in the list | `1a-offline-lost-…`, `1a-offline-retried-reception-ar-light-1440` |
| «زائر تجربة 2» from the bar at the foot | reception · ar light 390 | the dialog (name, «طالب», «الوردية» «مسائي» chosen at 18:2x Gaza, «تُحسب 5 ₪ للساعة، حتى 25 ₪.»); toast «سُجّلت زيارة زائر تجربة 2» above the bar | `1a-bar-…`, `1a-checkin-dialog-…`, `1a-checkin-toast-reception-ar-light-390` |
| Layouts | owner and reception × ar light / en dark × 390, 768, 1440 (12) | cards and the bar below 768; the table from 768 («الاستخدام» from 1024); the list in 8 of 12 columns at 1440; «⋯» holds «تبديل الموظف» at 390 | `1a-desk-<role>-<lang>-<width>` (12), `1a-desk-menu-<role>-<lang>-390` (4) |
| Touch targets (DI-16) | reception · 390, touch emulation (`pointer: coarse` true) | «خروج» 44 px, 44 px; the bar's «تسجيل زيارة» 48 px (`shots\pr1a\1a-touch-sizes.txt`) | `1a-touch-reception-ar-light-390` |
| «زائر تجربة 1» out, cash, the change | reception · en dark 1440 | filled with ₪5; 20 typed → «₪15 change», submit «Check out and receive ₪5»; toast «… checked out · ₪5 received in cash» | `1a-checkout-change-…`, `1a-checkout-paid-reception-en-dark-1440` |
| «زائر تجربة 2» out, nothing received, `+970599000301` | reception · ar light 390 | «لم يدفع شيئًا» → «يبقى 5 ₪ دينًا على زائر تجربة 2», the name and the phone, «استلام المبلغ كاملًا»; toast «لم يدفع · يبقى 5 ₪ دينًا على زائر تجربة 2» | `1a-checkout-debt-…`, `1a-checkout-debt-toast-reception-ar-light-390` |
| Override «ممتلئ» 30 min, then automatic | owner · ar light 1440 (and the panel at en dark 390) | toast «تظهر المساحة «ممتلئ» للزوار»; trigger «يظهر للزوار: ممتلئ يدويًا · 0:30»; «العودة للحالة التلقائية» → «عادت الحالة تلقائية»; `PUT` 200, `DELETE` 200 | `1a-override-panel-…` (2), `1a-override-set-…`, `1a-override-inforce-…`, `1a-override-cleared-owner-ar-light-1440` |
| `CLOSURE_IN_FORCE`: «زائر تجربة 3», out unpaid `+970599000302` | `demo-directory-owner` · `shati-sea-view` (52) · ar light 1440 | the control disabled with «لا تُضبط الحالة والمساحة مغلقة الآن.»; the warning toast «… المساحة معلَنة مغلقة الآن، وسُجّل الحضور رغم ذلك.», kept until closed; out with «لم يدفع · يبقى 5 ₪ دينًا على زائر تجربة 3» | `1a-closure-desk-…`, `1a-closure-warning-…`, `1a-closure-checkout-…`, `1a-closure-out-owner-ar-light-1440` |
| Width break | owner · ar light 1440 | with the grid the list is 744 px of `main`'s 1 192; `xl:grid-cols-12` removed → 1 128 px (one column); restored (copy, `cmp` equal) → 744 | `1a-width-grid-…`, `1a-width-break-…`, `1a-width-restored-owner-ar-light-1440` |
| «تبديل الموظف» | reception · en dark 1440 | signed out, at `/login?next=/dashboard/spaces/7/desk` | `1a-switch-reception-en-dark-1440` |
| FULL as owner, FULL as reception | — | **NOT PERFORMED, by design** (the owner's decision for the owner; §13 for reception): tests 21 and 12 | — |

**Fixes the real run found, folded into their commits** (`--fixup`, autosquash on the branch's own base): the billed
time read as a clock («مدة محسوبة 00:05») → the stay's own words («5 د»); the check-out's rows were forced left to right
(«د 6») → each value isolated in its direction; a 30-minute override read «0:31» (the control's clock up to 30 s old,
rounded up) → the clock read again when the desk sets it. After them: `test:component -- src/features/desk
src/features/occupancy/hooks/status` "Tests 20 passed (20)", lint exit 0, typecheck exit 0, `format:check` passed.
The override was set and cleared a second time to see the fix (one more `PUT` and `DELETE`).

**The network log** (`shots\pr1a\1a-offline-network.txt`): four `POST /api/v1/manage/spaces/7/visits`, three
`failed (net::ERR_INTERNET_DISCONNECTED)` (the first send and the transport's two re-sends) and one `201` after
«إعادة المحاولة», all with `Idempotency-Key: 866630be-993d-4110-b5af-97c5a144278b`; one visit of «زائر تجربة 1».

**Data left in `masaha_dev`:** at `masaha-demo` — visit «زائر تجربة 1» (26) closed, ₪5 cash; visit «زائر تجربة 2» (27)
closed unpaid, left to a new customer `+970599000301` «زائر تجربة 2» owing ₪5; the override set and cleared twice
(audit `space.statusOverridden`, `space.statusOverrideCleared` ×2). At `shati-sea-view` — visit «زائر تجربة 3» closed
unpaid, left to a new customer `+970599000302` «زائر تجربة 3» owing ₪5. The servers stopped by their process ids
(18932, 13396, 8136, 31156); 3320 and 5320 free.

## `main` moved again: #114 merged → rebased

During the fold, `origin/main` was `b7fe343e` (#114 `feat/payments` merged). Its files shared with this PR are
documents only (`docs/README.md`, `docs/features/desk.md`, `docs/features/visits.md`, `docs/project/overview.md`), so
this PR, merging second, rebased (`backup/desk-visits-pre-rebase` kept): the three conflicts kept both sides — the
desk's lines this PR's, the payments' lines #114's; `desk.md`'s web paragraph after #114's «A payment's void», and its
*Web history* after #114's *API history* line. `overview.md` merged by itself. `packages/shared/src/payments` only
gained exports; `npm run build -w @masaha/shared` exit 0.

**The head's checks again, on `27249d0f`:** lint exit 0; typecheck exit 0; `test:unit -w @masaha/web` "Test Files 125
passed (125) · Tests 946 passed (946)"; the scoped `test:component` (same folders) "Tests 1 failed | 179 passed (180)",
68.60 s — again `App.component.test.tsx` › "renders the main landmark". Compared: `main` (`b7fe343e`) with the same
folders but no `features/desk` "Tests 138 passed (138)", 40.61 s; the head with exactly those folders "2 failed | 162
passed (164)", 55.06 s (`App` › "renders the main landmark" and `router.component.test.tsx` › "shows the root's general
error, with no header, when the site shell fails", each 3 0xx ms); those two files alone: "Tests 3 passed (3)", 12.31 s.
Both wait for the site shell's lazy chunk; the head's folders hold more test files (23 against 15), so more load in
parallel. Neither is a test the standing exception names; **CI's full `test:component` on the pushed head judges —
red there → stop.** Build exit 0; `check:build` (the same three lines); `check:classes` (1302 files); `format:check`;
`check:links` "2713 links in 220 documents and 1863 source files all resolve."; `check:conflicts` "No conflict markers
found."; the first download 1 024 617 bytes, no dashboard, data-table or leaflet; "space shell chunks: none".
Files: `git diff --stat origin/main` → 90 files changed, 4 912 insertions(+), 27 deletions(-).

## #PRNUM, push and the PR

- `gh api …/issues?state=all&per_page=1…` → 115; expected 116. `scripts\prnum1a.sh 116` (PUBLIC's `prnum3b.sh`, its
  branch, backup and paths adapted, its checks kept) → "PRNUM OK #116 30c48633 (was 27249d0f)". `#PRNUM` in no commit's
  tree (each of the four checked); `git diff backup/desk-visits-pre-prnum HEAD --stat` → 5 files, 31 lines changed both
  ways (the number only). Backup branches left: **`backup/desk-visits-pre-rebase`**, **`backup/desk-visits-pre-prnum`**.
- Commits (subjects counted): `ac1dfd9e` feat(api): keep one idempotency key per intent (46) · `f582856d`
  feat(dashboard): add the page's bottom action bar (49) · `5f5809e2` feat(occupancy): show the desk who is present (45)
  · `30c48633` feat(desk): check visitors in and out at the desk (49). No `fixup!`, `style:` or `wip`; no tool attribution.
- `git push -u origin feat/desk-visits`; `gh pr create --assignee @me --label feat --label area:web --label area:docs`,
  titled `feat(desk): check visitors in and out at the desk` → **#116** https://github.com/Basel-Ghonaim/masaha/pull/116.
- Open PRs besides it: none (#114 merged into `b7fe343e`, the base) — no conflict check to make.

## CI and the end (2026-10-25)

`gh pr checks 116` on the pushed head `30c48633`: build, check:classes, check:conflicts, check:links, format:check,
lint, test:api (5m35s), **test:component (13m46s) pass** — so the two site-shell tests that missed 3 s locally pass in
CI's full lane — test:unit, typecheck: all pass (CodeRabbit "pass, review rate limited"). `mergeStateStatus` **CLEAN**.
`origin/main` still `b7fe343e`; no other open PR. No rebase in progress; `git status` clean; ports 3320 and 5320 free.
Local branches left: `backup/desk-visits-pre-rebase`, `backup/desk-visits-pre-prnum`.
