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

## On the head (`39248050`) — `scripts\head3.sh`, outputs `scripts\h3-<name>.txt`, exits in `h3-exits.txt`

`git fetch origin` → `origin/main` `1a89da5d` (#121); no rebase (merge-tree clean). Before each lane: no `vitest` of
app-b; free memory 3,817,952 KB (unit), 4,404,444 KB (component).

- `npm run test:unit -w @masaha/web` — exit 0 (41 s): "Test Files 135 passed (135) · Tests 978 passed (978)".
- `npm run test:component -w @masaha/web -- src/features/desk src/features/occupancy src/pages/dashboard
  src/pages/site/auth src/shared/session src/shared/copy src/shared/lists` — exit 1 (130 s): "Test Files 1 failed | 46
  passed (47) · Tests 1 failed | 238 passed (239)". The one: `changePasswordPage.component.test.tsx` › "lands the user on
  the page they asked for once the password is saved" (3472 ms) — `Unable to find role="heading" and name "Workspaces"`,
  the `/spaces` page not yet loaded at 3 s. **This PR does not touch that file or the page it lands on.** Alone: exit 0,
  "Tests 4 passed (4)"; its folder `src/pages/site/auth` again (free memory 4,721,568 KB): exit 0, "Test Files 4 passed
  (4) · Tests 26 passed (26)". Decision below; CI's `test:component` judges.
- `NODE_ENV=production npm run build` — exit 0 ("✓ built in 1.96s").
- `npm run check:build` — exit 0: "No showcase code in 58 build files (1016 strings checked)." · "No dashboard code in
  the site's first download." · "No data-table or leaflet, nor Leaflet's stylesheet, in the site's first download."
- `npm run check:classes` — exit 0: "No physical direction or arbitrary-value classes in 1416 files."
- `npm run format:check` — exit 0: "All matched files use Prettier code style!"
- `npm run check:links` — exit 0: "2814 links in 227 documents and 2002 source files all resolve."
- `npm run check:conflicts` — exit 0: "No conflict markers found."

## The real run (2026-10-26; local headless Chrome over CDP, `scripts\run3.mjs` on `scripts\cdp3.mjs`, PR 2's model)

- **Docker Desktop was not running** this morning (`failed to connect to the docker API at
  npipe:////./pipe/dockerDesktopLinuxEngine`): asked the owner, who started it; then `docker start masaha-postgres-1`,
  `pg_isready` "accepting connections", `prisma migrate status` "Database schema is up to date!". API on 3320 (its first
  start had failed on the database: restarted), web on 5320, from `C:\dev\masaha\app`, worker A's `masaha_dev`.
- **A fix found by the run, folded:** the file's header stacked its items in a centred column — `CardContent` is
  `flex-col`, and `cn` keeps it beside `flex-wrap`; now `flex-row` (`FileHeader.tsx`), folded into commit 2 (`--fixup` +
  autosquash onto `541f3e63`). New shas: `a6c6303c` (2), `2b1e84f5` (3), `97752cb5` (4), `04abb8f1` (5); carried and
  commit 1 unchanged. That rebase rewrote files under the dev server, whose page reloads renewed the first idle run's
  session (08:07:37Z): that run was stopped and the idle case started again at 08:08:18Z, with no file changed until it
  ended.
- **Layouts** (`layouts`, reads only): the list, «نور حسن»'s file with its statement open, and at 1440 «سارة خالد»'s
  statement (an auto check-out) — owner and reception × Arabic light and English dark × 390, 768, 1440:
  `shots\pr3\3-list-<role>-<lang-theme>-<width>.png`, `3-file-…`, `3-statement-sara-…` (28 shots). Table from 768 px,
  cards below (logged `table: true/false`); the title «نور حسن · مساحة» / "· Masaha"; the voided payment struck with
  «ملغاة» and «أُلغيت: …»; dates and times on Gaza's clock.
- **Filters** (`filters`, reception, reads only): the chips «الكل, لم يبدأ, نشط, ينتهي قريبًا, منتهٍ» (no «مؤرشف»);
  «ينتهي قريبًا» → `?status=ENDING_SOON`, «زبونان»; reception's `?status=ARCHIVED` falls back to every customer (the
  address read for the owner only); the search «زائر» → «زبون واحد»; at 390 the sheet, and with `?kind=NONE&payment=OWES`
  its trigger counts 2 and «عرض الزبونين»; the owner's «مؤرشف» → «لا يوجد زبائن مؤرشفون». Shots `3-filter-*.png`.
- **Edit** (`edit`, owner, «نور حسن»): her phone typed `+970599000304`, the save sent **offline** → «لم يصل الرد. أعد
  المحاولة — لن تُسجَّل مرتين.», nothing re-sent in the next 6 s; online, «إعادة المحاولة» → saved, «حُفظت بيانات نور حسن»;
  then cleared → saved, «بدون رقم جوال». Network (`shots\pr3\3-edit-network.txt`, the phone masked):
  - `08:12:17Z PATCH /api/v1/manage/spaces/7/customers/3 failed (net::ERR_INTERNET_DISCONNECTED) Idempotency-Key: none
    body: {"phone":"<phone>"}`
  - `08:12:24Z PATCH …/customers/3 200 Idempotency-Key: none body: {"phone":"<phone>"}`
  - `08:12:28Z PATCH …/customers/3 200 Idempotency-Key: none body: {"phone":null}`
  — only the changed field, never the name; no key; one send per press.
- **Archive and restore** (`archive`, owner, «زائر تجربة 2», owes 5 ₪): «⋯» → «أرشفة…» → the `AlertDialog` «أرشفة زائر
  تجربة 2؟ | عليه 5 ₪ غير مسدّدة. …» → «أرشفة رغم الدين» → «أُرشف زائر تجربة 2 · عليه 5 ₪»; the header «مؤرشف» with
  «استرجاع»; under «مؤرشف» in the list, «استرجاع» → «استُرجع زائر تجربة 2». Network: `POST …/customers/6/archive 200
  Idempotency-Key: none`, `POST …/customers/6/restore 200 Idempotency-Key: none`.
- **End** (`end`, owner, «يوسف»'s «20 ساعة», the approval note's §14.11): «End the subscription today? | 20 ساعة · The end
  date becomes 26 October. …» → «“20 ساعة” ended today»; the card read again: «Expired», «Ended 26 October». Network:
  `POST …/subscriptions/4/end 200 Idempotency-Key: none`. (Its first try found no button: the page was still in the
  account's language; a navigation after the preference fixed the script.)
- **Carried item 1, live** (`carried1`, reception): `Network.setBlockedURLs` on `…/customers/1` alone → the file's
  failure «تعذّر تحميل ملف الزبون | لا يوجد اتصال…» with «إعادة المحاولة» (three blocked GETs: the transport's two
  re-sends); unblocked, the retry → 200 and the file. **The pre-check-in dialog's own failure is not shown live:** the
  data holds no `UPCOMING` subscription (inventory: UPCOMING 0), and none may be made; the carried test owns it
  (decision below). Shots `3-carried1-*.png`.
- **Carried item 2, live** (`carried2`, reception, the desk): «زائر تجربة 5» typed, «تسجيل زيارة باسم «زائر تجربة 5»»,
  Enter → «سُجّلت زيارة زائر تجربة 5», the search `{"value":"","focused":true}`; then «خروج» at once, paid in full:
  «سُجّل خروج زائر تجربة 5 | استُلم 5 ₪ نقدًا». Network: `POST …/visits 201 Idempotency-Key: a1999351-…` (visit 50),
  `POST …/visits/50/check-out 200 Idempotency-Key: c3b88f99-…` body `{"payment":{"amountAgorot":500,"method":"CASH"}}`.
- **Touch targets at 390** (`touch`, touch emulation): every list control 44 px — «الفلاتر», the seven chips, each «⋯»
  («إجراءات أخرى: …»); the file's «⋯», «استلام المتبقي», «عرض الكشف» 44 px.
- **A second fix found by the run, folded:** a customer with no subscription said «بدون اشتراك» twice (the subscription
  column and the status column; both lines of a card). The status now shows nothing then (`StatusBadge`), folded into
  commit 1. Re-run as the rule says: `components/customers` + `routes.component.test.tsx` "Test Files 2 passed (2) ·
  Tests 57 passed (57)"; lint exit 0; typecheck exit 0; Prettier clean. New shas: `a5c96d25` (1), `bb91aec3` (2),
  `13d9d062` (3), `e40720f8` (4), `dfcb8631` (5).
- **The width break** (§13): the file's cards' grid at 1440 — before, `gridTemplateColumns` "365.328px 365.328px
  365.328px" (`3-grid-owner-en-dark-1440.png`); the grid's `md:grid-cols-2 xl:grid-cols-3` removed once → "1128px", one
  column (`break-file-cards-grid.png`); restored from its copy (`bak-p3-grid.tsx`), `git status` clean.
- **The idle sign-out, first try:** reception on the desk untouched from 08:08:18Z to 08:24:18Z; the script then
  looked for the sidebar's link and found none, and threw before its shot — the page had most likely already moved to
  sign-in on its own (the desk's 30 s poll refused). The script now records where the page is first; it runs again
  after the push, while CI runs (no file changes then).

## #PRNUM, push and the PR (2026-10-26)

- The issues API's last number → 121; next **122**. `scripts\prnum3.sh 122` (PR 2's script, its branch, backup and
  description adapted, its checks kept) → "PRNUM OK #122 358765e3 (was dfcb8631)"; `git grep '#PRNUM'` empty; the
  local backup branch it left: **`backup/customers-file-pre-prnum`**. Checked again just before the push: 121.
- Final shas: `0e732e61`, `dd4d8e79`, `6304ecbd` (1), `4e04734b` (2), `4dc09af1` (3), `156fdb3f` (4), `358765e3` (5).
- `git push -u origin feat/customers-file`; `gh pr create --assignee @me --label feat --label area:web --label
  area:docs`, title `feat(desk): show a customer's file`, the description (`scripts\pr-body-3.md`) with "Carried from
  #119" and the size exception → **https://github.com/Basel-Ghonaim/masaha/pull/122**.

## The idle sign-out, performed (2026-10-26)

Reception signed in at 08:30:50Z and left on the desk, untouched; at 08:46:55Z the page was already
`/login?next=%2Fdashboard%2Fspaces%2F7%2Fdesk`, with «انتهت جلستك بعد 15 دقيقة دون نشاط. سجّل الدخول من جديد.» above the
form (`3-idle-reception-ar-light-1440.png`). Network (`3-idle-network.txt`): `08:45:57.002Z GET …/occupancy 401`, then
`08:45:57.059Z POST /api/v1/auth/refresh 401` — the desk's passive poll kept nothing alive, and the refresh's
`SESSION_IDLE` ended the session with its line.

**A slip, corrected:** that log line for the sign-in (`POST /auth/login`) recorded its body, **the demo account's
password**, in `scripts\run3-idle.txt` and `shots\pr3\3-idle-network.txt`; it also showed in the session's output.
Both files were scrubbed at once (`"password":"<hidden>"`; a search of `scripts\` and `shots\pr3\` finds none), before
the workspace's nightly snapshot took them (both untracked then). `run3.mjs` now never keeps an `/auth/` request's body.
The owner may want to rotate `SEED_DEMO_PASSWORD` (a demo account's, development data only).

## CI and the end (2026-10-26)

- `gh pr checks 122` on head `358765e3` (run 40292751716): **all pass** — build 47s, check:classes, check:conflicts,
  check:links, format:check, lint 2m28s, test:api 7m22s, test:component 20m31s, test:unit 1m40s, typecheck 48s,
  CodeRabbit. `gh pr view 122 --json mergeStateStatus` → **CLEAN**.
- Not run locally, CI judged on the head: the full `test:component` — pass (the local miss in
  `changePasswordPage.component.test.tsx` did not recur); `test:unit` of `apps/api` and `packages/shared` — pass;
  `test:api` — pass.
- Open PRs: only #122; no conflict check needed (#121 merged; `merge-tree` clean against `1a89da5d`, and GitHub CLEAN).
- `git status --short` clean; no rebase in progress; both servers stopped by process id (11648, 28008, 15724, 11492);
  3320 and 5320 free. Local backup branch left: `backup/customers-file-pre-prnum`.
- **Data left in `masaha_dev`:** «نور حسن»'s phone set and cleared (none, as before; two edits audited); «زائر تجربة 2»
  archived and restored (as before; audited); «يوسف»'s subscription 4 ended 2026-10-26 (now EXPIRED); visit 50 «زائر
  تجربة 5» checked in and out, 5 ₪ cash. Never merged.

## Decisions taken without the owner (under `_SHARED\AUTONOMY_2026-10-25.md`)

1. **The local miss in `changePasswordPage.component.test.tsx`** (head lane). Met: one failure at 3 472 ms in a file this
   PR does not touch, passing alone and in its folder. Options: stop; treat it as finding 87's slowness and let CI judge.
   Chose: CI judges (it passed there). Undo: none needed; the owner may add it to finding 87's family.
2. **Carried item 1's dialog not shown live.** Met: no `UPCOMING` subscription in the data, and none may be made.
   Options: make one (a forbidden write); show the file's own read failing and retrying (CDP blocking that one URL).
   Chose: the latter, the dialog's failure proven by its test. Undo: the owner allows a subscription not started and
   the case runs.
3. **Two layout fixes found by the run, folded** into their commits (the file's header a row; no second «بدون اشتراك»),
   re-running only what they touch. Undo: revert the `flex-row` in `FileHeader.tsx` and the `null` in `StatusBadge`.
4. **The idle run started again** after a rebase's page reloads renewed the first; then again after the script threw.
   Chose: re-run with no file changes during it. Undo: none.
