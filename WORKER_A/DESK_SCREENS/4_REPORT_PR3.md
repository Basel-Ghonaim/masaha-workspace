# DESK_SCREENS — PR 3 report (`feat/customers-file`)

Executor, 2026-10-25. Prompt: `3_EXEC_PROMPT_PR3.md`. Read as §0 says (no `start-work-item`, no `workflow.md`).

## Preconditions

- `C:\dev\masaha\app` on `main`, clean; `git pull --ff-only` → "Already up to date"; `main` = `541f3e63` (#119).
- #118 (`feat/desk-api`) and #119 merged; #120 merged. `git grep -n SESSION_IDLE origin/main -- packages/shared` →
  `packages/shared/src/core/errors.ts:75:  'SESSION_IDLE',`.
- `npm run build -w @masaha/shared` exit 0. `npx prisma migrate status` → "28 migrations found … Database schema is
  up to date!" (nothing applied).
- `docker start masaha-postgres-1` → running.

## First checks (§13)

1. Clean, fetched, `main` pulled ✔.
2. What must have merged: PR 2 (#119) ✔, DESK_API (#118) ✔, `SESSION_IDLE` in `packages/shared` ✔; **finding 124's
   *Resolution* line is DESK_API's**: «**Resolution (2026-10-25, #118):** the first. The statement and the file are each
   read in one read-only `REPEATABLE READ` transaction…» ✔ (Status: Resolved).
3. **Base diff** `8d087c5e..origin/main` (9 commits: #120 and three #118-review commits it carried — `8b40f4b3`
   test(auth), `045f09eb` test(desk), `b52bbc1f` docs). Outside `apps/api`: the two `errors.ts`
   (`REPORT_ALREADY_DECIDED`), `packages/shared/src/core/errors.ts`, `packages/shared/src/data-reports/*`, documents
   (findings 170, 171 added). `git diff --stat 8d087c5e origin/main -- packages/shared/src/{customers,subscriptions,
   payments,desk}` → empty. Re-read those four modules against §10: `Customer`, `CustomerRow`, `CustomerFile`,
   `SubscriptionWithMoney`, `UnpaidVisit`, `SubscriptionStatement`, `StatementCheckIn`, `ItemPayment`,
   `updateCustomerSchema` (partial, `phone` nullable), `customersQuerySchema` (`CUSTOMER_STATUS_FILTERS`,
   `CUSTOMER_KINDS`, `PAYMENT_FILTERS`) — as §10 uses them ✔.
4. Open PRs: `gh pr list --state open` → `[]` ✔.
5. i. `RequireAuth` sends a guest to `signInPath(location)` (the page as `next`) ✔. j. `CardTitle` is a `div`
   (`ComponentProps<'div'>`) → fallback: the heading inside it (as PR 2's card and the sign-in page do). n. The
   sign-in page: `apps/web/src/pages/site/auth/SignInPage.tsx` ✔.
6. Finding numbers: on `main` 160, 161, 164, 170, 171 exist; **162 and 163 free** ✔.
7. **The data inventory** (`scripts\inventory3.mjs`, output `scripts\inventory3.out.txt`; API on 3320 for it only,
   stopped by its process ids 18024, 3380, 19268; 3320 and 5320 free). Space 7 (`masaha-demo`), 7 customers, none
   present, none archived:
   - «نور حسن» (customer 3): no phone; subscription 3 «يوم بعد يوم» custom, typed, ENDING_SOON, paid in full; its
     statement holds **1 voided payment** of 2 ✔ (the voided case).
   - The customer made in PR 1a: «زائر تجربة 2» (customer 6), owes 5 ₪ (unpaid visit 27) → the archive's dialog ✔.
     «زائر تجربة 1» has no customer (paid in full in PR 1a).
   - «يوسف أبو علي» (customer 4): subscription 4 «20 ساعة», custom, ENDING_SOON, no dates, paid ✔ (to end).
   - Filters: ENDING_SOON 2, EXPIRED 2, UPCOMING 0, ACTIVE 0; PACKAGE 2, CUSTOM 2, NONE 3; OWES 4, SETTLED 3, CREDIT 0;
     ARCHIVED 0 for the owner (the «archived empty» state), **403 for reception** (the server's guard).
   - A statement with an auto check-out: «سارة خالد»'s subscription 1 (5 check-ins, 1 auto).

## Branch

`git switch --no-track -c feat/customers-file origin/main` (`541f3e63`). Before each focused run: no `vitest` of
`app-b` (only worker B's `eslint`, pid 11808, at the first run); free memory 2,233,972 KB at the first.

## Carried from #119 — 1. `0e732e61` fix(desk): say when a customer's file fails (43)

- Test (`useSubscriberCheckIn.component.test.tsx` › "says when a coming subscription’s file fails, with its retry,
  then the start date"): the file's read answers 500 (three times: the transport's two re-sends) → the dialog's
  `alert` «We couldn’t read when the subscription starts» with «Try again», no skeleton; the retry answered → the
  start date, no alert.
- **Red before the code:** `× says when a coming subscription’s file fails, with its retry, then the start date` —
  `TestingLibraryElementError: Unable to find role="alert"` (`p3-red-carried1.txt`).
- **Green:** `useSubscriberCheckIn` + `components/subscriber` → "Test Files 2 passed (2) · Tests 10 passed (10)".
- **Break** (the dialog's failure branch removed, the skeleton back): `× says when …` — `Unable to find
  role="alert"`, "Tests 1 failed | 7 passed (8)" (`p3-break-carried1.txt`); restored.
- **A new line in both catalogues** (none fitted: `desk.pay.fileFailed` says «مستحقات الزبون», the file's dues):
  `desk.subscriber.pre.startFailed` «تعذّرت قراءة تاريخ بدء الاشتراك» / "We couldn’t read when the subscription
  starts". The message under it is `useRefusalView`'s (the server's line with its reference), the retry
  `file.refetch()`, as `PayDialog`'s file failure.
- lint exit 0; typecheck exit 0; Prettier on the touched folders "All matched files use Prettier code style!".

## Carried from #119 — 2. `dd4d8e79` fix(desk): clear the search after a named visit (47)

- `DeskSearch`'s `checkIn(name, after)` hands its `after`; `DeskPage` passes it to `visit.setOpen(true, name,
  after)`; `useVisitDialog` keeps it per opening and runs `after.done()` only after the check-in lands; `VisitDialog`'s
  `onCloseAutoFocus` sends the focus to the search after such a check-in (`focusAfter`), else Radix's default (the
  trigger). The `SearchAfter` type is imported by the hook (type only).
- Test (`DeskSearch.component.test.tsx` › "is cleared and focused after a named visit is checked in; a failed one
  keeps the term", the search and the visit dialog composed as the page does): a refused check-in (403) → the
  dialog's alert, Escape, the term kept; then a successful one → the toast, the field focused and empty. The first
  test's `toHaveBeenCalledWith('Sa')` became `('Sa', expect.anything())`.
- **Red before the code:** `× is cleared and focused after …` — `expect(element).toHaveFocus()` (and the first test
  `expected "vi.fn()" to be called with arguments: [ 'Sa', Anything ]`) (`p3-red-carried2.txt`).
- **Green:** `components/search` + `hooks/check-in` → "Test Files 2 passed (2) · Tests 7 passed (7)".
- **Break** (`after.current?.done()` removed): `× is cleared and focused …` — `expect(element).toHaveValue()`
  "Tests 1 failed | 2 passed (3)" (`p3-break-carried2.txt`); restored.
- lint exit 0; typecheck exit 0; Prettier "All matched files use Prettier code style!".

## Commit 1 — `e579cce2` feat(desk): list the space's customers (38) — 20 files

- **Red before the code** (each new test, its module not yet written): 54 `customersQueryOf.unit.test.ts` — "Error:
  Cannot find module './customersQueryOf'" (`p3-red-c1-unit.txt`); 55 `useCustomersFilters` — "Failed to resolve
  import \"./useCustomersFilters\"" (`p3-red-c1-55.txt`); 56 `useCustomersList` — "Failed to resolve import
  \"./useCustomersList\"" (`p3-red-c1-56.txt`); 57 `CustomersList` — "Failed to resolve import \"./CustomersList\""
  (`p3-red-c1-57.txt`). The routes test's list case (written after the route) made red by taking the page out of
  `SPACE_PAGES`: `× shows the owner the customers under its title…` / `× shows reception…` — `Unable to find
  role="link" and name "Sara Khalid"` (`p3-red-c1-routes.txt`); restored.
- **Green:** unit "Test Files 1 passed (1) · Tests 4 passed (4)"; component `hooks/customers`, `components/customers`,
  `hooks/card`, `components/search` "Test Files 5 passed (5) · Tests 18 passed (18)" (free memory 3,225,936 KB; no
  `vitest` of app-b); routes `-t customers` "Tests 2 passed | 49 skipped (51)".
- **Breaks** (`scripts\breaks_p3.py` + `breaks_p3.json`, each restored from its copy):
  - 54 [role] `ARCHIVED` kept for reception → `× keeps «Archived» for the owner only`, "Tests 1 failed | 3 passed (4)".
  - 56 [state] one empty state → `× at /c?q=Zed … noMatch`, `× at /c?kind=CUSTOM … noMatch`, `× at /c?status=ARCHIVED
    … archivedEmpty`, "Tests 3 failed | 4 passed (7)".
  - 57 [width] the sheet at 1440 → `× shows five columns from 768 px, … its filters inline; axe-clean at 1440`, "Tests 1
    failed | 2 passed (3)".
- lint exit 0 (after one unused import fixed); typecheck exit 0; `check:links` "2801 links in 225 documents and 1968
  source files all resolve."; Prettier "All matched files use Prettier code style!".
- **Departures in commit 1:**
  - **No `presentIds` option** on `useCustomersList` (§10's signature): nothing in the list reads it (PR 2 removed the
    card's presence badge; a row has no presence column in §10's five). `rows` are `{ id, key, card: CustomerCardView,
    archived }`; `customerCardView(row, words, language)` is PR 2's `useCustomerCard` body made a plain function so a list
    can word its rows (the hook calls it).
  - **`customersQueryOf` returns `{ filters, query }`** (§10: `{ query; page }`): `filters` holds the page; `query` adds
    `limit: 20`.
  - **The actions column is empty in this commit** (commit 3 puts the «⋯» there; «زبون جديد» is PR 4's).
  - **The list's card below 768 px** is drawn in `CustomersList.tsx` (the name's link, the phone, the subscription, its
    status and the balance), not the desk's `CustomerCard` (whose «حضور» and «استلام» are the desk search's).
  - **The kind and payment inline from 768 px is chosen with `useMediaQuery`** (so test 57 proves it), as `DataTable`
    chooses its table.
  - **Copy beyond §10:** `desk.customers.filters.close` «إغلاق» / "Close" (the sheet's close button's name); the search
    field's label and placeholder reuse `desk.search.label` / `.placeholder`; the four statuses reuse
    `desk.customer.statuses`; a failed refresh reuses `occupancy.present.refreshFailed`.
  - **Files beyond §9:** `useCustomerCard.ts` (the plain function); docs `architecture.md` §2 (as §10 says). The
    repository and the keys needed no change (PR 2's `customers` and `deskKeys.customers` serve the list).

## Commit 2 — `bdfebb94` feat(desk): show a customer's file (34) — 22 files

- **Red before the code:** 58 `termsLine` / `payStatus` — "Error: Cannot find module './payStatus'", "… './termsLine'"
  (`p3-red-c2-unit.txt`); 59 `useCustomerFile` — "Failed to resolve import \"./useCustomerFile\"" (`p3-red-c2-59.txt`);
  60 `CustomerFile` — "Failed to resolve import \"./CustomerFile\"" (`p3-red-c2-60.txt`); 61 (written after the
  route) red by its own break below.
- **Green:** unit `features/desk/services` + `shared/copy` (the catalogues' parity, test 40, among them) "Test Files 17
  passed (17) · Tests 69 passed (69)"; component `hooks/file`, `components/file`, `components/pay`, `hooks/pay`,
  `hooks/subscriber` and the whole `routes.component.test.tsx` "Test Files 7 passed (7) · Tests 79 passed (79)".
- **Breaks:**
  - 58 [money] partial when nothing paid (`paidAgorot >= 0`) → `× is paid when nothing is owed, partly paid …` —
    "expected { key: 'partial', … } to deeply equal { key: 'unpaid', tone: 'destructive' }".
  - 59 [money] the left computed (`due − paid`) → `× says each subscription’s due, paid and left as the server answers
    them` — "expected '₪50' to be '₪30'".
  - 60 [a11y] cards with no heading → `× heads its sections h2 and its cards h3 …` — "Unable to find an accessible
    element with the role \"heading\"".
  - 61 [role] the record title not given → `× shows the owner a customer’s file titled by their name …`, `× shows
    reception …` — "Unable to find role=\"heading\" and name \"Sara Khalid\"", "Tests 2 failed | 3 passed | 49 skipped".
- lint exit 0 (after one needless `?.`); typecheck exit 0; `check:links` "2803 links in 225 documents and 1981 source
  files all resolve."; Prettier "All matched files use Prettier code style!".
- **A slip, corrected:** while checking formats I ran `git checkout -- docs/features/desk.md`, which reset that file to
  commit 1; its commit-2 edits (written by a script minutes before) were re-applied by the same script before the commit,
  and the diff checked. Nothing else was touched.
- **Departures in commit 2:**
  - **`useCustomerFile(spaceId, customerId)`** — no `abilities` yet (commit 3 adds them with the archive); the header's
    `actions` come with commit 3, the card's `statement` and `end` with commit 4. `title` is a hook of its own
    (`useFileTitle`, §9's file) that the page reads for `useRecordTitle`; the file's view holds `pay` (the payment
    dialog's item) and `CustomerFile` mounts `PayDialog` itself, as «غير محصّل» mounts its dialogs.
  - **The header's status** is the current subscription's: the one running, else the next, else the latest — the rule
    the customers list's row reads from the server (`current`), applied to the file's list (the file answers no
    `current`). A copy of a server rule in the browser, small; noted for review.
  - **A card's dates:** «{from} – {to}», the end «بدون تاريخ نهاية» when it has none; no line when it has no start
    («يوسف»'s «20 ساعة»). Its `left` is the server's balance, never below zero (a usage-based one in credit leaves
    nothing).
  - **The unpaid rows** reuse `UncollectedRow` (DI-24): the name line is «زيارة {day}» (`desk.pay.itemVisit`), the how line
    «غير محصّل»'s (`how` / `howManual`), «تحصيل» its word.
  - **Copy beyond §10:** `desk.file.here` «حاضر الآن» / "Here now" (the header's presence; PR 2 dropped the card's).
    Reused: `desk.customer.noPhone`, `.noEnd`, `.statuses`, `.owes/.credit/.settled`, `desk.subscriber.progress`,
    `desk.uncollected.how/howManual/collect/today/yesterday`, `desk.pay.itemVisit`, `dashboard.pages.customers`.
  - **The title carries no `lang`/`dir`** (a name's language is unknown, #119's F3 ruling); the breadcrumb's page is
    `dir="auto"`.
  - **Files beyond §9:** `test/deskCustomer.ts` (`customerFile` fixture). The route's guard takes the customers item's
    roles from `SPACE_NAV` (`CUSTOMERS_ROLES`).

## Commit 3 — `16d1f05c` feat(desk): edit, archive and restore a customer (48) — 33 files

- **Red before the code:** the repository's new case — `× edits, archives and restores a customer, each with no key` —
  "TypeError: repository.editCustomer is not a function" (`p3-red-c3-repo.txt`); 62 `useEditDialog` — "Failed to resolve
  import \"../../components/edit/EditCustomerDialog\"" (`p3-red-c3-62.txt`); 63 `useArchiveFlow` — "Failed to resolve
  import \"../../components/archive/ArchiveDialog\"" (`p3-red-c3-63.txt`); 64 `CustomerMenu` — "Failed to resolve import
  \"./CustomerMenu\"" (`p3-red-c3-64.txt`).
- **Green:** unit `features/desk` + `shared/copy` "Test Files 18 passed (18) · Tests 77 passed (77)"; component
  `features/desk` + `pages/dashboard` "Test Files 33 … Tests 183" with one failure (below), then after the fix the whole
  `routes.component.test.tsx` "Tests 54 passed (54)" and each touched folder green (62: 5, 63: 5, 64: 3 passed).
- **A failure my change caused, and its fix:** `routes.component.test.tsx` › "lists reception’s four pages at its space,
  the front desk among them" — `Unable to find role="navigation" and name "Space dashboard"`, the body empty at 3 s —
  failed in the folder run, **alone** (`-t`), and in the whole file (free memory 4.0–4.4 GB, no app-b `vitest`), so it is
  not finding 87's exception (which needs it to pass alone). Diagnosis (not a lane result): with `--testTimeout=20000` it
  still fails at 3.04 s (the `findBy` wait), and a throwaway test timed the desk page's cold import in this lane at
  **10,789 ms** — the router holds the first render until the lazy desk page is transformed, which the «⋯» and its
  dialogs made longer. **Fix:** the navigation describe imports the desk page in a `beforeAll`, as the file's other
  sections do for their lazy pages (finding 28's idiom). No timeout or config changed. Then the file: "Tests 54 passed
  (54)". (Decision listed below.)
- **Breaks:**
  - 62 [key] the whole form sent → `× sends only what changed …`, `× sends nothing when nothing changed …`, `× sends null
    for a cleared phone`, `× is never sent again by itself …` — "expected { name: 'Sara Khalid', …(1) } to deeply equal {
    phone: '+970599000304' }", "Tests 4 failed | 1 passed (5)".
  - 63 [role][state] the dialog skipped when owing → `× asks first for a customer who owes, naming the debt`, `× says a
    customer present is checked out first`, "Tests 2 failed | 3 passed (5)".
  - 64 [a11y] **the plan's break (the menu's own label off) stayed green** — "Tests 3 passed (3)"
    (`p3-break-64-green.txt`): Radix names the menu content by its trigger (`aria-labelledby`), so that label cannot
    change the outcome. **The break that can:** the trigger's `aria-label` off → `× is named by the customer, its menu
    too; axe-clean` and the other two — "Unable to find an accessible element with the role \"button\" and name \"More
    actions: Sara Khalid\"", "Tests 3 failed (3)" (`p3-break-64b.txt`). A departure.
- lint exit 0 and typecheck exit 0 (after a test helper's generic type and one needless `?.`); `check:links` "2806 links
  in 225 documents and 1993 source files all resolve."; Prettier: `english/desk.ts` was flagged after the commit — fixed
  and folded (`--fixup` + `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash origin/main`), then "All matched files use
  Prettier code style!".
- **Finding 123** → Resolved (its *Resolution* line, #PRNUM), moved to the index's *Resolved* group.
- **Departures in commit 3:**
  - **`CustomerActions`** (`components/menu/`, beyond §9): the «⋯» with its edit and archive dialogs, or the owner's
    «استرجاع», for a row, a search card and the file's header alike; `CustomerMenu` takes a ready view.
  - **The search's card and `DeskSearch` take `menu: { owner, fileLink }`**, passed by `DeskPage` (`spaceCustomerPath`);
    `CustomerFile` and `CustomersList` take `owner` (S5's `abilities` reduced to the one this PR reads). Tests that render
    the card or the search pass reception's `menu`.
  - **The owing archive's toast has no «تراجع»** (§10 gives `doneOwing` without one; the undo is P9's for the settled,
    at-once archive). A lost answer on an at-once archive or a restore is a toast with «إعادة المحاولة» (the user's).
  - **«لم يتغيّر شيء»** is a polite `role="status"` line in the dialog, which stays open.
  - **Files beyond §9:** `CustomerActions.tsx`, `useRestore.ts`'s twin `useArchive.ts` (both in §9), the two tests
    above, `DeskSearch.tsx`, `DeskPage.tsx`, `CustomerPage.tsx`, `routes.component.test.tsx` (the warm-up), `desk.md`.

## Commit 4 — `2cbd2c3e` feat(desk): show a subscription's statement (43) — 22 files

- **Red before the code:** the repository's case — "TypeError: repository.statement is not a function"
  (`p3-red-c4-repo.txt`); 65 `useStatement` — "Failed to resolve import \"./useStatement\"" (`p3-red-c4-65.txt`); 66
  `useEndDialog` — "Failed to resolve import \"./useEndDialog\"" (`p3-red-c4-66.txt`); the `Statement` component's
  test (written after it) red by the statement never drawn once read: `× opens in its card, … axe-clean at 390` and `…
  at 1440` — "expected null not to be null" (`p3-break-statement-red.txt`).
- **Green:** component `features/desk` + `pages/dashboard` "Test Files 36 passed (36) · Tests 191 passed (191)" (free
  memory 5,194,884 KB, no app-b `vitest`); unit `features/desk` + `shared/copy` "Test Files 18 passed (18) · Tests 78
  passed (78)".
- **Breaks:** 65 [money][state] a voided payment counted as paid (`voided` always `null`) → `× strikes a voided payment
  with «Voided» and its reason, never as paid` — "expected null to deeply equal { label: 'Voided', …(1) }". (66 carries
  no marker: its red step is its break.)
- lint exit 0; typecheck exit 0; `check:links` "2812 links in 227 documents and 2002 source files all resolve.";
  Prettier "All matched files use Prettier code style!".
- **Findings:** **162** (no route names a space's staff to reception) and **163** (a subscription's corrections have no
  screen) written, Open, in the index. **124**'s *Resolution* line is DESK_API's (#118), checked in the first checks; the
  desk.md statement line links its rule.
- **Departures in commit 4:**
  - **`useStatement(spaceId, subscriptionId)`** holds its own open state (§10: `open` a parameter); `state` is `closed |
    loading | failed | ready`. The card calls `useStatement` and `useEndDialog` itself (the card view carries its
    `subscription`).
  - **The check-ins are a list of `dl` rows** (four columns from 768 px, two below), each value under its column's word —
    no table (DI-43's "a list"); the statement's two sections are `h4` under the card's `h3`.
  - **«إنهاء الاشتراك»** is offered while the subscription is neither ended nor `EXPIRED`; the dialog says the end the
    server will take (today, its start if not started, never past its end — the contract's rule, said before sending)
    with `textWas` when it had another end. The toast names the subscription from the answer.
  - **A `Statement` component test** (not in §11's table, §9 lists it): the toggle's `aria-expanded`/`aria-controls`,
    the voided payment, axe at 390 and 1440.

## Commit 5 — `39248050` feat(session): say a session ended for idleness (47) — 10 files

- **Red before the code:** 67 (`refresh.unit.test.ts`) `× ends a session the server ended for idleness, saying so
  until the next sign-in`, `× says no idleness for a session refused otherwise, or found ended by the restore` —
  "TypeError: getSessionEnd is not a function" (`p3-red-c5-67.txt`); 68 (`authPages.component.test.tsx`) `× says a
  session ended for idleness above the form` — "Unable to find an element with the text: Your session ended after 15
  minutes with no activity. Sign in again." (`p3-red-c5-68.txt`).
- **Green:** unit `shared/session` "Test Files 5 passed (5) · Tests 39 passed (39)"; component `pages/site/auth` +
  `shared/session` "Test Files 5 passed (5) · Tests 28 passed (28)".
- **Break** 67 [state] `endedBy` not set → both cases — "expected null to be 'idle'", "Tests 2 failed | 37 passed
  (39)". (68 has no marker: its red step is its break.)
- lint exit 0; typecheck exit 0; `check:links` "2814 links in 227 documents and 2002 source files all resolve.";
  Prettier "All matched files use Prettier code style!".
- **Departures in commit 5:** `endedBy` is kept in a second small store beside the session's (`getSessionEnd()`,
  `useSessionEnd()`), so `SessionState`'s shape and every test that compares it stay as they are; `endSession({
  endedBy })`; any established session clears it (a restore's too, not only a sign-in). The sign-in page's line is an
  `Alert variant="info"` (`role="status"`) inside the card, above Google's button. Tests: 67 in `refresh.unit.test.ts`
  (the unit lane, where the store's tests are), not the component lane §11 names. `desk.md`'s *Who uses it* no longer
  says the idle sign-out is not built.

## STOP — the size bound (prompt §1.6), 2026-10-25

All seven commits are made locally on `feat/customers-file`; **nothing is pushed**, no `#PRNUM` replaced, no PR, no
head-wide lanes run yet, **no real run**. `git status --short` clean, no rebase in progress, no server running
(3320 and 5320 free).

- **The PR's files:** `git diff --name-only 541f3e63 HEAD | wc -l` → **81** (51 code, 21 tests, 9 documents), past the
  prompt's "stop and ask only past 72 files" (the plan said ≈ 55 + the carried two). Per commit: carried 6 + 5; commit
  1 20; commit 2 22; commit 3 33; commit 4 22; commit 5 10. Commit 3 grew most: the «⋯» reaches three places (the
  list's rows, the desk search's card, the file's header), so `CustomerActions`, `DeskSearch`, `DeskPage`, the card,
  their tests and the fixtures moved with it; each commit also carries its own tests (21 test files in all).
- **`main` moved meanwhile:** #121 (worker B's favourites) merged; `origin/main` = `1a89da5d`. Shared with this PR:
  only `docs/architecture/findings/README.md`; `git merge-tree --write-tree HEAD origin/main` → no conflict. No open
  PR now.
- **Options for the owner:**
  - **A — one PR as it is,** 81 files, titled `feat(desk): show a customer's file`.
  - **B (recommended) — split after commit 3:** PR 3a = the carried two + commits 1–3 (the list, the file, edit /
    archive / restore) — **61 files**, title `feat(desk): show a customer's file`; PR 3b = commits 4–5 (the statement,
    the end, the idle line) — **31 files**, cut from `main` once 3a merges, title `feat(desk): show a subscription's
    statement`. Each stays under 72, and each half is a whole slice. Cost: a second CI and review.
  - **C — split after commit 2:** 44 and 56 files (commit 3's wiring then lands with the statement).
- **After the answer:** the head-wide lanes, the build checks, the real run (PR 3's writes), `#PRNUM`, the push and
  the PR, as §13 says — for the PR(s) the owner chooses.

## The owner's answer (2026-10-25, `3_EXEC_PROMPT_PR3_ANSWER.md`)

**Option A: one PR of 81 files**, a one-off exception to the 72-file bound (as #116's 90). Accepted as departures: the
routes test's warm-up import, break 64 on the trigger's label, the restored `desk.md` edits. No rebase (the branch
merges cleanly onto `1a89da5d`). The autonomy rule (`_SHARED\AUTONOMY_2026-10-25.md`) applies to the rest of this run.
