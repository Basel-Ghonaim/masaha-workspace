# DESK_SCREENS — PR 2 report (`feat/desk-subscribers`)

Executor's report, written as the work goes (prompt `3_EXEC_PROMPT_PR2.md`).

## Preconditions

- `gh pr view 117 --json state` → `{"state":"MERGED"}`.
- `C:\dev\masaha\app` on `main`, clean; `git fetch`; `git pull --ff-only` → "Already up to date." (`b1e94b41`).
- `npm run build -w @masaha/shared` → exit 0. `docker start masaha-postgres-1` → started.
- `apps/api`: `npx prisma migrate status` → "26 migrations found … Database schema is up to date!".

## First checks

- **1** ✔ clean, fetched, on `main`, pulled.
- **3 — the base diff** `git diff --name-status a1193e77 origin/main` → empty (the merge's tree is PR 1b's head).
  No `packages/shared` change since.
- **4 — open PRs:** `gh pr list --state open` → **#118 `feat/desk-api`** (worker B, head `12abd264`). Its files:
  `apps/api/*`, `packages/shared/src/{auth,core/errors,desk/requests,subscriptions/requests}`, the web's two
  `shared/copy/*/errors.ts`, and documents — among them `docs/features/desk.md`, `payments.md`, `subscriptions.md`,
  the findings index, which this PR also edits (text conflicts; whichever merges second rebases). No other web code
  file is shared. It is **not merged**, so `@masaha/shared/customers`, `subscriptions`, `payments` are read as on
  `main` (its changes are the subscribe's request and the statement's read, neither used here).
- **5c** ✔ (PR 1a's) the layer's `Alert` passes `role`.
- **5g** `@masaha/shared` exports no search fold (`git grep -n -i "fold\|normali[sz]e" packages/shared/src` → only
  `normalisePhone` and NFC) → `matchesPerson` trims and compares (`includes`), as the plan's fallback says.
- **5h** `shared/lib` has no day formatter (`time/` holds `clockOf`, `updatedAgo`); the feature holds PR 1b's
  `services/dayWord.ts` (today / yesterday / short date) → the plan's `services/dayText.ts` for «حتى {date}».
- **5j** `CardTitle` renders a `div` and takes no level → the fallback: the heading (`h3`) inside it.
- **5l** ✔ `useMediaQuery` exported by the layer (`design-system/index.ts:210`).
- **Finding numbers:** the index's highest is 164 (`161`, `164` are this item's); 160 is free (PR 2 writes it); a new
  one would take 165.

## The data inventory (read-only; `scripts\inventory2.mjs`, output `scripts\inventory2.out.txt`)

API on 3320 for the inventory only (stopped by its process ids 13608, 20716, 11880; 3320 and 5320 free).
Space `masaha-demo` (7): owner and reception; nobody present; no open check-in; uncollected total 2 (one page).

| Case (§13 PR 2 writes) | Record | Holds? |
|---|---|---|
| Reception: search «سارة», her card | customer 1 «سارة خالد», debt ₪36.60, current sub 1 «امتحانات بالساعة» `EXPIRED` `PER_HOUR` ₪4/h | ✔ |
| «حضور» (a warning if her limits say) | her subscription is `EXPIRED` → the pre-check-in dialog (DI-14), «تسجيل على أي حال» → `SUBSCRIPTION_EXPIRED` | ✔ |
| «خروج», the usage-based balance and «استلام» 5 ₪ | sub 1 is usage-based: its balance after the stay; a usage-based sub takes any amount | ✔ |
| «يوسف» checked in and out | customer 4 «يوسف أبو علي», sub 4 «20 ساعة» `ENDING_SOON` `FIXED`, settled → one tap | ✔ |
| «رامي»'s visit debt paid from «استلام دفعة» | customer 5 «رامي سالم», unpaid visit 4, charge ₪15, balance ₪15 | ✔ |
| The carried fix live (uncollected page past the last) | uncollected total 2 → one page | **NOT PERFORMED, by design** — the carried test |

## Branch

`git switch --no-track -c feat/desk-subscribers origin/main` (at `b1e94b41`).

## Carried from #117 — `3d87e797` fix(desk): show the last uncollected page in range (50)

- Test (`useUncollectedCard.component.test.tsx` › "shows the last page in place of one past it, never the empty
  line"): `/desk?uncollectedPage=3`, page 3 answered empty with 21 visits (`totalPages: 2`) → page 2's row, its
  «Collect», the pagination, no «Nothing left to collect.», the requests `page 3` then `page 2`.
- Red before the code: "× shows the last page in place of one past it, never the empty line" —
  "TestingLibraryElementError: Unable to find an element with the text: Visitor 21" ("Tests 1 failed | 6 passed (7)").
- The fix: `usePageInRange` (`replacePage` sets `uncollectedPage` with `{ replace: true }`, deleted for page 1);
  `state` reads `loading` while past the last, `empty` only when `totalRecords` is 0.
- Green after: `test:component -- src/features/desk/hooks/uncollected src/features/desk/components/uncollected`
  "Test Files 2 passed (2) · Tests 9 passed (9)"; `npm run lint` exit 0 (after typing the test's `params` as
  `unknown`: `no-unsafe-return`); `npm run typecheck` exit 0.
- **Break** (`usePageInRange` removed, `pastLast = false`): red "× shows the last page in place of one past it, never
  the empty line" ("Tests 1 failed | 6 passed (7)", `scripts\break-carried.txt`); restored from the copy, `cmp`
  equal, green "Tests 7 passed (7)".

## Commit 1 — `a9dde28c` feat(occupancy): match the present to a search (46)

- Red before the code: unit — `matchesPerson.unit.test.ts` "Error: Cannot find module './matchesPerson'" (test 42);
  component — `usePresentMatches.component.test.tsx` "Failed to resolve import "./usePresentMatches"" (test 43).
- Green after: `test:unit -- src/features/occupancy src/shared/copy` "Test Files 6 passed (6) · Tests 45 passed (45)"
  (test 40, the catalogues' parity, among them); `test:component -- src/features/occupancy` "Test Files 6 passed (6) ·
  Tests 20 passed (20)"; `npm run lint` exit 0; `npm run typecheck` exit 0; `check:classes` "No physical direction or
  arbitrary-value classes in 1338 files."
- Breaks: tests 42 and 43 carry no [key]/[role]/[money]/[state]/[warn] marker — their red step is their break
  (test 42's "digits matched anywhere" is asserted by `'0599'` → false).
- Built as: `matchesPerson(person, term, phones: ReadonlyMap<customerId, phone>)`; `usePresentMatches` filters
  `usePresentList`'s rows (the same state now, no request more, the rows worded alike); `PresentMatches` returns
  nothing with no row. `present.empty.text` changed; the existing test's expectation updated with it.

## Commit 2 — `7ee8ae2e` feat(desk): find customers from the desk's search (49)

- Red before the code: unit — "Cannot find module" for `./balanceView`, `./statusView`, `./dayText` (test 47, the
  date's own test); `deskRepository.unit.test.ts` › "searches the customers with the query it is given"
  "TypeError: repository.customers is not a function". Component — "Failed to resolve import" for `./useDeskSearch`
  (tests 44, 45), `./useCustomerCard`, `./DeskSearch` (test 46): "Test Files 3 failed (3)" (`scripts\red-c2-*.txt`).
- Green after: `test:unit -- src/features/desk src/shared/copy` "Test Files 13 passed (13) · Tests 63 passed (63)"
  (test 40 among them); `test:component -- src/features/desk src/features/occupancy src/pages/dashboard` (free memory
  4 003 628 KB, no app-b `node`) "Tests 1 failed | 143 passed (144)", 75.83 s — the one failure
  `routes.component.test.tsx` › "lists reception’s four pages at its space, the front desk among them", 3 050 ms,
  an empty `<body>` (finding 87's family, the prompt's standing exception); the file alone (free 4 024 436 KB): "Test
  Files 1 passed (1) · Tests 49 passed (49)", 23.72 s. `npm run lint` exit 0; `npm run typecheck` exit 0;
  `check:classes` "… in 1354 files."; `check:links` "2728 links in 222 documents and 1915 source files all resolve.";
  `prettier --check apps/web/src docs` "All matched files use Prettier code style!".
- Breaks (`scripts\breaks_pr2_c2.py`, each restored from its copy and `cmp`-equal; outputs `scripts\break-pr2-<n>.txt`):
  45 [state] the failure shown as a ready search → red "× says a failed search with a retry, never as no match", "× says
  it is offline"; 46 [a11y][width] `autoFocus` at every width → red "× takes the focus on arrival from 768 px, not at
  390"; 47 [money] settled → `null` → red "× says settled, neutral, with neither". Test 44 carries no marker: its red
  step is its break.
- **Departures in commit 2:**
  - **`Input` has no `size` prop** (§10's `size="lg"`): the layer's default size; a design-system change is out of
    scope. The field is `type="search"` (role `searchbox`).
  - **The cards leave the present out, so no presence badge:** §10's `CustomerCardView.here`, the card's `CardAction`
    badge and the words `customer.hereSince` / `customer.notHere` are not added — a present customer is in the first
    group only, so a card's badge would always read «غير حاضر» (no unused words). A card shown in the 30 s before the
    state now lists a check-in made at another desk answers `MEMBER_ALREADY_CHECKED_IN` (commit 3).
  - **`useDeskSearch` returns the rows, `CustomerCard` reads its own view** (`useCustomerCard(row)`): a card's
    actions (commits 3–4) keep their state per card. `DeskSearch`'s props are `{ spaceId, present: { customerIds,
    matches, group }, checkIn }` — `present.matches` counts the present a term finds, so «لا أحد…» and the primary
    visit button hold only when no one matched in either group, and the count counts both. No `abilities` prop:
    nothing in PR 2 reads one.
  - **`useVisitDialog.setOpen(open, visitorName?)`** (a PR 1a file): the search's «تسجيل زيارة باسم «X»» opens the
    dialog with the name typed. `matchesPerson` exported from `occupancy` for the page's count.
  - **`dayText` says the date in UTC**, not `Asia/Gaza`: a `YYYY-MM-DD` is read at its UTC midnight, so UTC keeps its
    own day (Gaza's zone would say the same day; UTC states it without a zone's rule).
  - Files beyond §9: `test/deskCustomer.ts` (fixtures), `dayText.unit.test.ts`, `useCustomerCard`'s test file exists
    as §9 lists it. Commit 2 changes **29 files** (§9: ≈ 20).

## `main` moved: #118 (worker B's `feat/desk-api`) merged during commit 3

`origin/main` → `7f724dd5` (Merge #118). Re-read against §10 (`git diff b1e94b41 origin/main -- packages/shared/src/{desk,
subscriptions,payments,customers,core}`): only the subscribe's request (spec D's `published`) and `SESSION_IDLE` in
`DOMAIN_ERROR_CODES` — neither used by PR 2; no response type changed. Shared files: the web's `errors.ts` (not
touched here), `desk.md`, `payments.md`, `subscriptions.md`, the findings index — text conflicts; this PR rebases.

## Commit 3 — `a58e4095` feat(desk): check subscribers in and out (40)

- **Owner's decision (asked mid-run):** the pre-check-in line for a subscription not started («يبدأ الاشتراك «{name}» في
  {date}.») needs its start, which `CustomerRow.current` does not carry (its end only) → "Read the file": the
  customer's file is read when the choice opens for a coming subscription only; the line shows once it arrives
  (`useCustomerFileQuery`, moved from commit 4 to `hooks/file/`).
- Red before the code (the new files moved aside, the repository at its committed version, then restored and
  `cmp`-checked): unit — `progressLines.unit.test.ts` "Cannot find module './progressLines'" (test 51);
  `deskRepository.unit.test.ts` › "checks a subscriber in with its key, out with none; reads the open check-ins and a
  file" "TypeError: repository.checkInSubscriber is not a function"; component — "Failed to resolve import" for
  `./PreCheckInDialog`, `…/useCheckOutSubscriber` (test 50), `…/useSubscriberCheckIn` (tests 48, 49): "Test Files 3
  failed (3)" (`scripts\red-c3-*.txt`).
- Green after: `test:unit -- src/features/desk src/features/occupancy src/shared/copy` "Test Files 18 passed (18) ·
  Tests 79 passed (79)"; `test:component -- src/features/desk/hooks/subscriber` "Tests 11 passed (11)" (after two test
  fixes: `toHaveTextContent` takes no function → `within(dialog).getByText`; Sonner's «Try again» pressed by Enter,
  jsdom having no pointer capture).
- `test:component -- src/features/desk src/features/occupancy src/pages/dashboard` (free 3 289 196 KB; **2 app-b
  `node` processes were running then** — gone before the re-run) → "Tests 3 failed | 154 passed (157)": the routes
  file's "lists reception’s four pages" (3 028 ms, finding 87's family) and, **new**, "sends a user back to the space
  they entered last" and "closes the drawer when another space is chosen in it". Alone (free 3 804 152 KB, no app-b):
  the same 3 failed — a real failure, not load. Cause: the routes test's fake server answers any unknown URL with the
  spaces list, so the desk's new `GET …/check-ins?open=true` got space rows and `useOpenCheckIns` read
  `checkIn.customer.phone` of `undefined`. Fix (as PR 1a did for the desk's two reads): `signIn`'s transport answers
  `/check-ins` with `[]`. Alone again (free 1 798 028 KB): "Test Files 1 passed (1) · Tests 49 passed (49)", 28.75 s.
- `npm run lint` exit 0; `npm run typecheck` exit 0 (after the dialog test's `view.anyway` possibly null);
  `check:classes` "… in 1366 files."; `check:links` "2731 links in 222 documents and 1927 source files all resolve.";
  `prettier --check apps/web/src` "All matched files use Prettier code style!".
- Breaks (`scripts\breaks_pr2.py`, each restored and `cmp`-equal; `scripts\break-pr2-<n>.txt`): 48a [key][warn] the
  dialog always → red (3 tests: "× checks an active subscription in at once, with one key per check-in", "× keeps the
  key across a retry after no answer", "× says they are already here…"); 48b [key] the key not renewed after a check-in
  → red "× checks an active subscription in at once, with one key per check-in"; 49 [state][warn] the search kept
  (`done` not called) → red (2 tests); 50 [money][a11y] focus left on `body` → red "× checks out in one tap with no
  key; the toast names the stay…". Test 51 carries no marker: its red step is its break.
- A fixup of commit 1 (`856a29a6`, to be autosquashed): `occupancy.md` names `PresentMatches` and `matchesPerson`
  (commit 1's documents, missed there).
- **Departures in commit 3:**
  - **Test 50's "the focus to the next row's «خروج»"** is `occupancy`'s `PresentList` rule (PR 1a, its own test); `desk`
    may not import `occupancy` even in a test, so test 50 proves the one-tap «خروج» keeps the focus (busy,
    `aria-disabled`, never `disabled`) until the row leaves; break 50 blurs it → red.
  - **«استلام» in the check-out toast** comes with commit 4 (the payment it opens).
  - **No «خروج» on a card:** a present customer is in the search's first group, whose rows carry `CheckOutAction`
    (commit 2's departure).
  - **«تسجيل كزيارة» sends no shift** (`checkInVisitSchema`'s `shiftId` is optional): the card has no shifts; the
    visit takes the no-shift rates.
  - **Copy beyond §10:** `desk.customer.checkInName({name})` «حضور {name}» — the button's accessible name (as PR 1a's
    `checkOut.openName`).
  - **Files beyond §9:** `useOpenCheckIns.ts` (the phones and usage lines for the page, beside the query),
    `hooks/file/useCustomerFileQuery.ts` (moved from commit 4), `CheckOutDialog.tsx` (`onCheckedOut`),
    `deskToasts.tsx`, `test/deskCustomer.ts`, `routes.component.test.tsx`, `occupancy.md`.

## STOP — the size bound (prompt §1.6)

`git diff --name-only b1e94b41 HEAD | wc -l` → **58 files** after commit 3 (the plan: ≈ 38 + the carried commit;
the prompt: stop and ask only past 55). Commit 4 adds, as §9 lists it, ≈ 6 new web files and `payments.md`: the PR
would be **≈ 65 files**. Nothing is pushed; asked the owner.
- **Owner's decision (asked):** "Keep PR 2 at ~65" — commit 4 as the plan lists it.

## Rebased on `7f724dd5` (#118)

`git branch backup/desk-subscribers-pre-rebase`; `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash origin/main` →
"Successfully rebased" with no conflict; the fixup folded into commit 1. New shas: `3e00146d` (carried), `f37833b9`
(1), `a5d089f4` (2), `43f73d14` (3). `npm run build -w @masaha/shared` exit 0. `prisma migrate status` showed #118's
migration `20261025081716_session_activity` pending on worker A's `masaha_dev` → `npx prisma migrate deploy` ("All
migrations have been successfully applied.") and `npx prisma generate` (§13 check 7's rule).

## The owner's autonomy rule (2026-10-25, `_SHARED\AUTONOMY_2026-10-25.md`)

Received from the main supervisor mid-run, then confirmed by the owner in this session: decisions are taken without
stopping and listed under "Decisions taken without the owner" below. The two asked before it (the coming
subscription's start; the size at 58 → keep at ~65) are the owner's own answers.

## Commit 4 — `d315965b` feat(desk): receive a payment on a customer's item (50)

- Red before the code (`openItems.ts`, `usePayDialog.ts`, `PayDialog.tsx` moved aside, then moved back): unit —
  `openItems.unit.test.ts` "Error: Cannot find module './openItems'" (test 52); component — `usePayDialog` "Failed to
  resolve import "../../components/pay/PayDialog"" (test 53) (`scripts\red-c4-*.txt`).
- First green run: 3 of 5 pay tests failed — no payment was sent: `useServerForm`'s `prepare` kept the first
  render's chosen item (none yet), so the body failed the schema on a field the dialog does not show. Fix: the item's
  `visitId` / `subscriptionId` live in the form's values, set with the amount (as the collect dialog keeps its
  `visitId`). Then "Tests 5 passed (5)".
- Green after: `test:unit -- src/features/desk src/shared/copy` "Test Files 15 passed (15) · Tests 69 passed (69)";
  `test:component -- src/features/desk src/features/occupancy src/pages/dashboard` (free 5 683 436 KB; 1 app-b `node`
  process, not a `vitest` of the routes) "Test Files 31 passed (31) · Tests 164 passed (164)", 81.86 s; lint exit 0;
  typecheck exit 0; `check:classes` "… in 1372 files."; `check:links` "2746 links in 222 documents and 1937 source
  files all resolve."; `prettier --check apps/web/src` passed.
- Breaks (`scripts\breaks_pr2.py`): 52 [money] unpriced kept → red "× lists the unpaid visits oldest first, the
  unpriced left out, then the subscriptions that owe"; 53 [money][key] the typed amount reset on switching items →
  red "× pays one item, with the opening’s key; the amount follows the item until typed". Both restored, `cmp`-equal.
  Test 53's [key] is also proven by "keeps the key across a retry after no answer" (4 requests, one key).
- **Departures in commit 4:**
  - `useCustomersSearchQuery(spaceId, query | null)` takes the list's query (`q`, `payment`, `limit`), so the picker
    reads `payment=OWES` through the same hook as the search.
  - The payment dialog is mounted per opening (`key` = an opening counter in the page): a new opening is a new key
    without a `renew()`.
  - Copy reused rather than added: the note's label (`desk.collect.note`), the picker's placeholder
    (`desk.search.placeholder`), the picker's failure (`desk.search.failed`); the page action is `desk.pay.title`.
  - The toast's «استلام» shows only while the subscription still owes after the check-out (a usage-based one paid
    ahead is paid from its card).
  - `PayDialog.component.test.tsx` (named groups, the first field focused, axe-clean): §9 lists it; no §11 number.
- **Files:** `git diff --name-only origin/main HEAD | wc -l` → **65** (the owner's "Keep PR 2 at ~65").

## On the head (`d315965b`) — `scripts\head2.sh`, outputs `scripts\h2-<name>.txt`, exits in `h2-exits.txt`

Before each test lane: no `vitest` of `app-b` running; free memory 3 695 860 KB (unit), 3 608 360 KB (component).
- `npm run test:unit -w @masaha/web` — exit 0, "Test Files 132 passed (132) · Tests 967 passed (967)".
- `npm run test:component -w @masaha/web -- src/features/desk src/features/occupancy src/pages/dashboard
  src/shared/copy src/shared/lists` — exit 1, "Tests 1 failed | 163 passed (164)", 92.11 s: only
  `routes.component.test.tsx` › "lists reception’s four pages at its space, the front desk among them", 3 031 ms
  (finding 87's family, the standing exception). The file alone (free 6 494 172 KB): "Test Files 1 passed (1) ·
  Tests 49 passed (49)", 24.07 s. CI's `test:component` judges. (Commit 4's own run of the same folders less
  `shared/copy` and `shared/lists` passed 164 of 164.)
- `NODE_ENV=production npm run build` — exit 0. `npm run check:build` — exit 0: "No showcase code in 57 build files",
  "No dashboard code in the site's first download.", "No data-table or leaflet, nor Leaflet's stylesheet, in the
  site's first download."
- The first download (`scripts\firstDownload.mjs apps/web/dist`): **1 036 538 B, 6 chunks** (PR 1b: 1 030 340 B; the
  growth is the new copy lines and #118's), no `features/desk`, `dashboard`, `directory`, data table.
- `check:classes` — "No physical direction or arbitrary-value classes in 1372 files." · `format:check` — "All matched
  files use Prettier code style!" · `check:links` — "2746 links in 222 documents and 1937 source files all resolve."
  · `check:conflicts` — "No conflict markers found." (each exit 0).
- **Not run locally (CI judges):** the full `test:component`, `test:unit` of `apps/api` and `packages/shared`,
  `test:api` (no API change).

## A fix after the head's lanes: the card's name in English (folded)

The layouts' screenshots showed the card's Arabic name at the far end of its English card (`h3 dir="auto"` aligns to
its own direction — PR 1b's names case). Fix: the name an inline `span dir="auto"` inside the `h3` (commit 2), and
the pay picker's name `self-start` (commit 4); each a fixup, autosquashed (`git rebase -i --autosquash origin/main`,
no conflict). New shas: `7406576a` (2), `67607e98` (3), `9ebc7cd2` (4); carried and commit 1 unchanged. Re-run, as
the rule says, only what it touches: `test:component -- src/features/desk/components src/features/desk/hooks/pay
src/features/desk/hooks/subscriber` "Test Files 8 passed (8) · Tests 25 passed (25)"; lint exit 0; typecheck exit 0;
`check:classes` and `prettier --check` passed. Live: the name 0 px from its heading's start at 390 and 1440
(`2-namefix-owner-en-dark-*.png`).

## The real run (local headless Chrome over CDP; `scripts\run2.mjs` on `scripts\cdp2.mjs`, PR 1b's model)

API on 3320 and web on 5320 from `C:\dev\masaha\app`, worker A's `masaha_dev`; stopped by their process ids (26296,
27792, 5736, 14404); 3320 and 5320 free. Enter sent with `text: '\r'`. Screenshots in `shots\pr2\`; phones masked in
every log (`<phone>`). Output: `scripts\run2-layouts.txt` and this section.

| Case | Result | Screenshots |
|---|---|---|
| **Layouts** — owner and reception, Arabic light and English dark, 390 / 768 / 1440 (reads only): the search with «سارة» (the customers group, her card: phone, «امتحانات بالساعة» «منتهٍ» «حتى 21 أكتوبر», «عليه 36.60 ₪», «حضور», «استلام 36.60 ₪», then «تسجيل زيارة باسم «سارة»» outlined); the no match («لا أحد بهذا الاسم أو الرقم» + DI-36's line, the visit button primary); «استلام دفعة»'s picker (the five debtors) | the field focused on arrival at 768 and 1440 («INPUT search …»), **not at 390** («BODY»); one card column at 390 (358 px) and 768 (305 px), the `xl` grid's first cell at 1440 (365 px); «استلام دفعة» an outline button from 768, in the «⋯» at 390 | `2-search-*`, `2-nomatch-*`, `2-pay-picker-*` (36) |
| **Network — the search** (reception): «سارة» typed a letter each 120 ms | **one** request: `GET …/customers?q=سارة&limit=6&page=1 200` | `shots\pr2\2-search-network.txt` |
| **«سارة» «حضور»** (reception, ar 1440): expired → the choice «تسجيل حضور · سارة خالد» / «انتهى الاشتراك «امتحانات بالساعة» في 21 أكتوبر.» / «تُسجَّل زيارة باسمه، ولا تُضاف إلى ملفه.» / «رجوع» «تسجيل على أي حال» «تسجيل كزيارة»; «تسجيل على أي حال» first sent **offline** → «تعذّر تسجيل الحضور · لم يصل الرد. أعد المحاولة — لن تُسجَّل مرتين.»; online, «إعادة المحاولة» | toast (warning) «سُجّل حضور سارة خالد · انتهى الاشتراك، وسُجّل الحضور رغم ذلك.»; the search emptied and focused; **4 requests, 1 key, one check-in** (3 × `ERR_INTERNET_DISCONNECTED`, then 201) | `2-sara-choice-…`, `2-sara-lost-…`, `2-sara-in-…`; `2-sara-in-network.txt` |
| **Touch targets at 390** (touch emulation, `pointer: coarse` true; «سارة» present) | «حضور رامي سالم» 44, «استلام 15 ₪» 44, «حضور يوسف أبو علي» 44, «تسجيل زيارة باسم «ي»» 44, «خروج سارة خالد» 44 px; the bar's button 48 px | `2-touch-reception-ar-light-390`; `2-touch-sizes.txt` |
| **«سارة» «خروج»** from the search (reception, ar 1440): the present list's usage cell «يُحسب من الحضور: 4 ₪ للساعة»; the search's «حاضر الآن» group with «خروج» | one tap: `POST …/check-ins/12/check-out 200`, **no key**; toast «سُجّل خروج سارة خالد · مدة الحضور 0 د · يبقى 36.60 ₪ على الاشتراك» with «استلام»; the search emptied and focused | `2-sara-present-…`, `2-sara-out-…` |
| **«استلام» 5 ₪** from that toast: the dialog on «امتحانات بالساعة» («المستحق 96.60 ₪ · المدفوع 60 ₪ · المتبقي 36.60 ₪», the usage note); 5 typed; first sent **offline**, then «إعادة المحاولة» | **4 requests, 1 key, one payment**; toast «سارة خالد · امتحانات بالساعة · المتبقي 31.60 ₪ · استُلم 5 ₪ نقدًا» | `2-sara-pay-…`, `2-sara-paid-…`; `2-sara-out-network.txt` |
| **«يوسف»** (reception, en dark 768): «Check in» → at once, no dialog (ending soon); then «Check out» from the search's «Here now» | toast «يوسف أبو علي checked in»; focus back on the search; `POST …/check-ins 201` with a key, `POST …/check-ins/13/check-out 200` with none; «Stayed 0m» (settled: no owed line, no «Receive») | `2-yusuf-*`; `2-yusuf-network.txt` |
| **«رامي»'s visit debt from «استلام دفعة»** (reception, ar 390, the page's «⋯»): the picker → «اختيار» «رامي سالم» → «زيارة 5 أكتوبر · المستحق 15 ₪ · المدفوع 0 ₪ · المتبقي 15 ₪», 15 filled | `POST …/payments 201` with its key; toast «رامي سالم · زيارة 5 أكتوبر · المتبقي 0 ₪ · استُلم 15 ₪ نقدًا» | `2-rami-pay-…`, `2-rami-paid-…`; `2-rami-network.txt` |
| **The debtors present first** (DI-21) | **not performed live**: no debtor was present while the picker was open, and making one present is a write §13 does not list — test 53's "lists the customers who owe, those present first" proves it | — |
| **The carried fix live** | **not performed, by design**: two uncollected visits, one page — the carried test proves it | — |

## #PRNUM, push and the PR

- `gh pr list --state all --limit 1` → 118; the issues API's last → 118; next **119**. `scripts\prnum2.sh 119` (PR 1b's
  script, its branch and backup names adapted, its checks kept) → "PRNUM OK #119 8d087c5e (was 9ebc7cd2)"; `git grep
  "#119" HEAD -- docs` 12 lines; no `#PRNUM` left; no tool attribution in any message.
- Commits (subjects counted): `3e00146d` fix(desk): show the last uncollected page in range (50) · `f37833b9`
  feat(occupancy): match the present to a search (46) · `bb101bc5` feat(desk): find customers from the desk's search
  (49) · `8b69646a` feat(desk): check subscribers in and out (40) · `8d087c5e` feat(desk): receive a payment on a
  customer's item (50).
- `git push -u origin feat/desk-subscribers`; `gh pr create --assignee @me --label feat --label area:web --label
  area:docs`, title "feat(desk): find customers from the desk's search" → **#119**
  https://github.com/Basel-Ghonaim/masaha/pull/119 · head `8d087c5e` · 65 files. Description:
  `scripts\pr-body-2.md` ("Carried from #117" named).
- Local backup branches: `backup/desk-subscribers-pre-rebase`, `backup/desk-subscribers-pre-prnum`.
- Open PRs: none other than #119 (`gh pr list --state open`; #118 merged before it). No conflict check to make.

## Decisions taken without the owner (under `_SHARED\AUTONOMY_2026-10-25.md`)

1. **The debtors present first, not shown live.** Met: no debtor was present while the picker was open; making one
   present (a check-in of a debtor) is a write §13 does not list. Options: an extra write; not performed. Chose: not
   performed, test 53 ("lists the customers who owe, those present first") proves it. Undo: the owner allows the
   extra write and the case is run (`run2.mjs` with a debtor checked in).
2. **The card's name alignment fix after the head's lanes** (folded into commits 2 and 4). Met: an Arabic name at the
   far end of an English card. Options: leave it for review; fix now. Chose: fix now (PR 1b's own fix), re-running
   only what it touches. Undo: revert the `span` / `self-start` in `CustomerCard.tsx` and `PayDialog.tsx`.
3. **Departures recorded per commit above** (no «خروج» or presence badge on a card; the toast's «استلام» only while
   owing; copy reused rather than added; `useCustomerFileQuery` in `hooks/file/`; `dayText` in UTC; the visit by
   name sends no shift) — each a choice the plan left open, taken toward the smaller change. Undo: each is local to
   the file named.

(Asked before the autonomy rule, and answered by the owner: the coming subscription's start read from the file;
PR 2 kept at ~65 files.)

## CI and the end (2026-10-25)

- `gh pr checks 119` on head `8d087c5e` (run 40191729675): **all pass** — lint, typecheck, test:unit (2m21s),
  test:component (13m47s), test:api (6m53s), build, check:classes, check:conflicts, check:links, format:check,
  CodeRabbit. `gh pr view 119 --json mergeStateStatus` → **CLEAN**.
- Not run locally, CI judged on the head: the full `test:component` — pass; `test:unit` of `apps/api` and
  `packages/shared` (inside CI's `test:unit`) — pass; `test:api` — pass.
- `git status --short` clean; no rebase in progress; both servers stopped; 3320 and 5320 free. Data left in
  `masaha_dev`: «سارة»'s check-in 12 (closed), a 5 ₪ cash payment on her subscription 1; «يوسف»'s check-in 13 (closed);
  a 15 ₪ cash payment on «رامي»'s visit 4; #118's migration applied. Never merged.
