# DESK_SCREENS — PR 1b report (`feat/desk-uncollected`)

Written as the work goes, 2026-10-25.

## Preconditions

- `gh pr view 116 --json state` → `{"state":"MERGED"}`. `C:\dev\masaha\app` on `main`, clean; `git pull --ff-only`
  → "Already up to date." (`93225c3c`, the merge of #116). `npm run build -w @masaha/shared` → exit 0.
- No `0_CARRIED_FROM_116.md`: nothing carried.

## Worker A's database

- `docker start masaha-postgres-1` → started.
- `npx prisma migrate status` → "26 migrations found … Following migration have not yet been applied:
  20261024133344_payment_void_guard" (the one expected, #114's).
- `npx prisma migrate deploy` → "All migrations have been successfully applied."; `npx prisma generate` →
  "✔ Generated Prisma Client (7.10.0)"; `npx prisma migrate status` → "Database schema is up to date!".
- `$env:SEED_DEMO='true'; npm run db:seed` → exit 0 (`scripts\seed1b.txt`): "Seeded the lookups, the admin
  account and the settings." · "The demo space exists; left unchanged." · "The directory's demo set exists; left
  unchanged." (`run.ts` prints "left unchanged" when the directory set's renewal returns false — nothing to renew.)

## First checks

- **1** ✔ clean, fetched, on `main`, pulled.
- **3 — the base diff** `git diff --name-status 30c48633 origin/main` → empty (the merge's tree is PR 1a's head).
  No `packages/shared` change since; the types this PR reads (`UncollectedVisit`, `DeskVisit`, `ReceivedPayment`,
  `ReceivePaymentRequest`, `LeaveToCustomerRequest`, `WriteOffVisitRequest`, `PriceVisitRequest`) are as §10 uses
  them.
- **4 — open PRs:** `gh pr list --state open` → none (worker B's `feat/desk-api` is not open). No conflict check
  to make now; checked again before the push.
- **5c** ✔ (PR 1a's) `Alert` passes `role`. **5h** `shared/lib` still has no day formatter (`time/` holds `clockOf`,
  `updatedAgo`) → the plan's `services/dayWord.ts`.
- **Finding numbers:** the index's highest is 161 (PR 1a's). 164 is free; a new one would take 165.
- **#114 widened the uncollected visits** (`api-contract.md` › `GET …/uncollected-visits`; `UncollectedVisit`'s
  comment in `@masaha/shared/payments`): besides the auto check-out's visits, a priced visit closed by hand with no
  customer that owes again after a void. The web lists what the server answers and filters by nothing. What the
  plan assumed `AUTO` only: §10's row line `uncollected.how` («خروج تلقائي عند الإغلاق · {day} {range}») — false for
  such a row. Adapted (a departure): a manual row reads «خروج يدوي · {day} {range}» / "Checked out by hand · {day}
  {range}" (`uncollected.howManual`); DI-2 ("each row says how it closed") holds. No design issue's words become
  false: DI-9's write-off line and DI-11's remainder rule hold for a row with no customer whatever its close.
- **#114 reworded `VISIT_WRITTEN_OFF`'s two catalogue lines:** reused as they are (`errors.VISIT_WRITTEN_OFF`,
  through `useRefusalView`'s fallback); §10's `desk.refusals.VISIT_WRITTEN_OFF` («شُطبت هذه الزيارة.») is not added
  (a departure, the prompt's instruction).

## The data inventory (read-only; `scripts\inventory1b.mjs`, output `scripts\inventory1b.out.txt`)

API on 3320 for the inventory only (stopped by its process ids 30968, 12104, 18632; 3320 and 5320 free).

| Case (§13 PR 1b writes) | Record | Holds? |
|---|---|---|
| Owner: «لن يُحصَّل…» on «خالد», a reason, then «تراجع» | `masaha-demo` (7), visit 3 «خالد», `AUTO`, 2026-10-06, no customer, charge ₪25, paid 0, balance ₪25, not written off | ✔ |
| Reception: «تسجيل دين» on «خالد» with `+970599000303`, then «تحصيل» 10 ₪ cash | the same visit; `+970599000303` belongs to no customer (PR 1a's new ones are …301, …302) | ✔ |
| The unpriced case | `unpriced-visits` total 0 (owner and reception) | **NOT PERFORMED, by design** — test 38 |

Also listed: visit 1 «عمر» (`AUTO`, 2026-10-07, ₪25 owed, no customer) — left untouched. Owner `mayTypePrice: true`,
reception `false`.

## Branch

`git switch --no-track -c feat/desk-uncollected origin/main` (at `93225c3c`).

## Commit 5 — `06bb8c58` feat(desk): collect the uncollected visits (42)

- Red before the code: unit — `dayWord.unit.test.ts` "Error: Cannot find module './dayWord'" (test 39);
  `deskRepository.unit.test.ts` › "reads the uncollected visits’ page, and sends a payment, a debt, a write-off and
  its undo" "TypeError: repository.uncollected is not a function". Component (tests 31–37, 41; the five new
  components moved aside, then restored and `cmp`-checked; `scripts\red-c5.txt`) — "Failed to resolve import" for
  `UncollectedCard`, `CollectDialog`, `DebtDialog`, `WriteOffDialog`: "Test Files 5 failed (5)".
- Green after: `test:component -- src/features/desk/hooks/{uncollected,collect,debt,write-off}
  src/features/desk/components/uncollected` "Test Files 5 passed (5) · Tests 18 passed (18)";
  `test:unit -- src/features/desk src/shared/copy` "Test Files 10 passed (10) · Tests 55 passed (55)" (test 40,
  the catalogues' parity, among them); `test:component -- src/features/desk src/pages/dashboard` "Test Files 15
  passed (15) · Tests 109 passed (109)" (free memory 2 893 416 KB; app-b's `vitest` waited out first);
  `npm run lint` exit 0; `npm run typecheck` exit 0; `npm run format:check` "All matched files use Prettier code
  style!".
- Fixes on the way (before the commit): a blank write-off reason is sent as absent so it reads `required`
  («اكتب السبب»); the write-off test's dialog closes as the card closes it; Sonner's action pressed by Enter
  (jsdom has no pointer capture), as `useDeleteSpace`'s test does.
- Breaks (`scripts\breaks_c5.py`, each restored and `cmp`-equal; outputs `scripts\break-c5-<n>.txt`):
  31 a client sum in the title → red (3 tests); 32 the menu shown to reception → red "× shows reception no
  write-off"; 33 the phone not required → red "× asks the phone for a remainder on a visit with no customer";
  34 a key on «تسجيل دين» (the transport's retry enabled) → red "× carries no key, and is never sent again by
  itself after no answer"; 36 the desk's 403 line left out → red "× words a write-off refused 403 for reception,
  shown by mistake"; 41 a key added to the write-off → red "× never sends a write-off or its undo again by itself
  after no answer". Tests 35, 37, 39: their red step is their break (no [key]/[role]/[money]/[state] marker).
- **Departures in commit 5:**
  - `uncollected.howManual` «خروج يدوي · {day} {range}» / "Checked out by hand · {day} {range}" — #114's
    hand-closed rows (first checks); tested ("says how each row closed…").
  - `desk.refusals.VISIT_WRITTEN_OFF` not added: `errors.VISIT_WRITTEN_OFF` (#114's) is reused as it is.
  - `types/DeskAbilities.ts` holds `writeOff` only: `archive` comes with PR 3's archive (PR 1a's rule: no type
    nothing reads).
  - The owner's «⋯» is not shown on an unpriced row: the server refuses its write-off (`VISIT_NOT_PRICED`); it is
    priced first.
  - `types/UncollectedItem.ts` (the row's visit, name and day the dialogs share) and `test/deskVisit.ts`'s
    `uncollectedVisit`, `uncollectedPage` fixtures — files beyond §9.
  - The list's page is the address's `uncollectedPage` (from 2), as every paged list's page is a link.
  - The refresh-failure line reuses `occupancy.present.refreshFailed` («تعذّر التحديث؛ تظهر آخر قائمة.»).
  - Finding 112's evidence line, which §7 placed in PR 1a and PR 1a did not write, is written here (as §10's commit
    5 lists it).

## STOP — the size bound (prompt §1.6)

Commit 5 alone changes **39 files** (the plan: ≈ 27): 18 new web files (10 of them tests or test-only
companions: 6 test files, the fixtures; the 5 hooks' mutation files, 5 components, 2 types, 1 service), 9 modified
web files, 7 documents and findings. Commit 6 adds, as §9 lists it, ≈ 8 new web files and `visits.md`: the PR would
be **≈ 48 files**, past the prompt's 45. Nothing is pushed; asked the owner.
- **Owner's decision (asked):** "Keep PR 1b at ~48" — commit 6 as the plan lists it. Work resumes at commit 6.

## Commit 6 — `3a509bcb` feat(desk): price the unpriced visits (37)

- Red before the code: unit — `deskRepository.unit.test.ts` › "reads the unpriced visits’ page, and prices a visit
  with no key" "TypeError: repository.unpriced is not a function". Component (test 38, `scripts\red-c6.txt`) —
  "Failed to resolve import" for `../../components/unpriced/PriceDialog` and `../../components/unpriced/UnpricedCard`:
  "Test Files 2 failed (2)".
- Green after: `test:component -- src/features/desk/hooks/unpriced` "Test Files 2 passed (2) · Tests 5 passed (5)";
  `test:unit -- src/features/desk src/shared/copy` "Test Files 10 passed (10) · Tests 56 passed (56)"; lint exit 0;
  typecheck exit 0; `format:check` passed.
- `test:component -- src/features/desk src/pages/dashboard` (free memory 3 029 612 KB, no app-b `vitest`) →
  "Tests 2 failed | 112 passed (114)": `routes.component.test.tsx` › "lists the owner’s eleven pages…" and › "lists
  reception’s four pages at its space…", each an empty `<body>` at 3 0xx ms (the lazy shell not loaded). The file
  alone, first (2 999 212 KB): "1 failed | 48 passed (49)", 43.03 s — "lists reception’s four pages" again, empty
  `<body>`, 3 037 ms; alone again (4 781 472 KB): **"Tests 49 passed (49)", 27.35 s**. Finding 87's pattern; the
  reception test is in the same file but **not one the standing exception names** — said plainly. CI's full
  `test:component` judges.
- **Break 38** [role] (the query always enabled): first **stayed green** — my own test's defect (it looked for no
  request after one microtask, before any fetch could start). The test now waits 200 ms; the break then went red
  "× reads nothing, and shows nothing, for whoever may not type a price" (`scripts\break-c5-38.txt`), restored,
  green "Tests 5 passed (5)". A departure.
- **Departures in commit 6:**
  - **No pages on «بدون سعر»:** the card reads page 1 (its title counts all; each priced leaves it). The plan's
    §10 names no pagination for it, and the uncollected card's page words would misname it.
  - Test 38 is split in two files as §9 lists them: `useUnpricedCard` (read only for whoever may type a price;
    absent with none) and `usePriceDialog` (priced with its reason; `VISIT_ALREADY_PRICED` worded;
    `PRICE_TYPING_NOT_ALLOWED` reads the terms again).
- **Files:** `git diff --stat origin/main` → 48 files changed, 3 017 insertions(+), 14 deletions(-) (the owner's
  "Keep PR 1b at ~48").

## On the head (`3a509bcb`) — `scripts\head1b.sh`, outputs `scripts\h-<name>.txt`

No app-b `vitest` before each lane; free memory 2 243 732 KB (unit), 3 401 740 KB (component).
- `npm run test:unit -w @masaha/web` → "Test Files 126 passed (126) · Tests 950 passed (950)", 38.80 s.
- `npm run test:component -w @masaha/web -- src/features/desk src/features/occupancy src/pages/dashboard
  src/shared/copy` (the prompt's folders; no other folder's files changed) → "Test Files 22 passed (22) · Tests 131
  passed (131)", 72.26 s — the routes file's "lists the owner’s eleven pages" passed in this run.
- `NODE_ENV=production npm run build` → exit 0.
- `npm run check:build` → "No showcase code in 57 build files (1017 strings checked). No dashboard code in the
  site's first download. No data-table or leaflet, nor Leaflet's stylesheet, in the site's first download."
- `npm run check:classes` → "No physical direction or arbitrary-value classes in 1333 files."
- `npm run format:check` → "All matched files use Prettier code style!"
- `npm run check:links` → "2722 links in 221 documents and 1894 source files all resolve."
- `npm run check:conflicts` → "No conflict markers found."
- **The first download** (`scripts\firstDownload-1b.txt`): 1 030 340 bytes, 6 chunks (PR 1a's head: 1 024 617 — the
  growth is the copy catalogue's new lines, which ship in both languages); no `features/desk`, `data-table`,
  `dashboard`, leaflet; "space shell chunks: none" (finding 27: no cycle).
- Not run locally (CI judges): the full `test:component`, `test:unit` of `apps/api` and `packages/shared`,
  `test:api`.

## The real run (local headless Chrome over CDP; `scripts\run1b.mjs` on `scripts\cdp1b.mjs`, PR 1a's model)

API on 3320 and web on 5320 (`npm run dev`), worker A's `masaha_dev` ("Database schema is up to date!"). Enter sent
with its text (`'\r'`). Screenshots in `shots\pr1b\`; each case's output `scripts\run1b-<case>.txt`.

| Case | Who · where | Result | Screenshots |
|---|---|---|---|
| Layouts | owner and reception × ar light / en dark × 390, 768, 1440 (12) | «زيارتان غير محصّلتين» / "2 visits not collected", rows «عمر» and «خالد» (₪25 each, «خروج تلقائي عند الإغلاق · 6 أكتوبر 14:00–22:00»); the card under the list at 390 and 768 (full width), beside it at 1440 (`xl` side column: card 360 px, list 744 px); no «بدون سعر» card (no unpriced visit); the owner's «⋯» per row, reception none | `1b-desk-<role>-<lang>-<width>` (12), `1b-row-menu-owner-{ar-light,en-dark}-390` |
| «لن يُحصَّل…» on «خالد», then «تراجع» | owner · ar light 1440 | the dialog: «لن يُحصَّل مبلغ هذه الزيارة؟ · خالد · 6 أكتوبر · 25 ₪. تخرج الزيارة من «غير محصّل» … ويمكن التراجع عنها من الإشعار.», reason typed; toast «لن يُحصَّل 25 ₪ · خالد» with «تراجع», still there 12 s later; the card «زيارة واحدة غير محصّلة», the focus on its heading (the row gone, DI-30); «تراجع» → «أُعيدت الزيارة إلى «غير محصّل»», «خالد» back | `1b-writeoff-dialog-…`, `1b-writeoff-toast-…`, `1b-writeoff-undone-owner-ar-light-1440` |
| «تسجيل دين» on «خالد», `+970599000303` | reception · ar light 390 | «يبقى 25 ₪ دينًا على صاحب هذا الرقم، ويُنشأ له ملف زبون إن لم يكن له ملف.»; the name focused first («خالد»); toast «سُجّل 25 ₪ دينًا على خالد»; the row keeps «تحصيل», no «تسجيل دين» (it has a customer now) | `1b-debt-dialog-…`, `1b-debt-toast-reception-ar-light-390` |
| «تحصيل» 10 ₪ cash on «خالد», first send offline | reception · en dark 1440 | filled with ₪25; 10 typed → "₪15 stays owed by خالد" · "Added to خالد’s file" (no phone asked: it has a customer), "Record ₪10"; offline → "No answer came back. Try again — it won’t be recorded twice." with "Try again"; online, the retry → toast "خالد · visit of 6 Oct" · "₪10 received in cash · ₪15 stays owed by خالد"; the row now ₪15 | `1b-collect-dialog-…`, `1b-collect-lost-…`, `1b-collect-toast-reception-en-dark-1440` |
| Touch targets (DI-16) | reception and owner · ar light 390, touch emulation (`pointer: coarse` true) | «تحصيل» 44 px, «تسجيل دين» 44 px, the owner's «⋯» 44 × 44 px, the bar's «تسجيل زيارة» 48 px (`shots\pr1b\1b-touch-sizes-<role>.txt`); «خروج» not on screen (no one present; PR 1a measured it, 44 px) | `1b-touch-{reception,owner}-ar-light-390` |
| The unpriced case | — | **NOT PERFORMED, by design** — the inventory found no unpriced visit; tests 38 (`useUnpricedCard`, `usePriceDialog`) prove it | — |

**The network log:**
- «تحصيل» (`shots\pr1b\1b-collect-network.txt`): four `POST /api/v1/manage/spaces/7/payments` — three `failed
  (net::ERR_INTERNET_DISCONNECTED)` (the first send and the transport's two re-sends) and one `201` after "Try
  again" — all with `Idempotency-Key: 169c12b1-c3f0-4ed4-9b7a-c8fdd774b646`; one payment (the row went ₪25 → ₪15).
- The write-off and its undo (`shots\pr1b\1b-writeoff-network.txt`): `POST …/visits/3/write-off 200` and, 15 s
  later, `DELETE …/visits/3/write-off 200`, **no `Idempotency-Key` on either**, and no other write in the 12 s
  after the undo — neither re-sent by itself (test 41, finding 115).
- «تسجيل دين» (`shots\pr1b\1b-debt-network.txt`): one `PUT …/visits/3/customer 200`, no key.

**A fix the real run found, folded into its commits** (`--fixup`, autosquash on `origin/main`): in the English
interface an Arabic name stood at the row's far end (its `dir="auto"` span stretched to the column's width) → the name
span `self-start`, in `UncollectedRow` (commit 5) and `UnpricedCard` (commit 6). After it: `test:component --
src/features/desk/components/uncollected src/features/desk/hooks/uncollected src/features/desk/hooks/unpriced` "Test
Files 4 passed (4) · Tests 13 passed (13)"; lint exit 0; typecheck exit 0; `format:check` passed; `check:classes`
"No physical direction or arbitrary-value classes in 1333 files." Seen again in the app (reads only): each name 20 px
from its row's start (`run1b-names.txt`; `1b-names-fixed-reception-en-dark-{390,1440}`). New heads: `d87b4e6d`
(commit 5), `87655cdc` (commit 6).

**Data left in `masaha_dev`** (masaha-demo, visit 3 «خالد»): written off and undone (audit `visit.writtenOff`,
`visit.writeOffUndone`); left to a new customer «خالد» `+970599000303` (audit `customer.created`,
`visit.leftToCustomer`); a payment of ₪10 cash by reception — the visit owes ₪15, in that customer's debt, and is still
listed uncollected (closed by the auto check-out). Visit 1 «عمر» untouched. The servers stopped by their process ids
(12396, 16264, 5652, 15424); 3320 and 5320 free.

Not repeated here: the width break (`xl:grid-cols-12` removed), made in PR 1a's real run; this run's 1440 boxes show
the side column (x 32 vs 416 in Arabic, 1048 vs 280 in English).

## #PRNUM, push and the PR

- Before the push: `origin/main` still `93225c3c`; `gh pr list --state open` → none (no conflict check to make);
  the last number 116 → expected 117.
- `scripts\prnum1b.sh 117` (PR 1a's, its branch, backup and description adapted, its checks kept, plus "the files
  changed against main are the same") → "PRNUM OK #117 a1193e77 (was 87655cdc)". `#PRNUM` in neither commit's tree;
  `git diff backup/desk-uncollected-pre-prnum HEAD --stat` → 7 files, 15 lines both ways (the number only).
  Backup branch left: **`backup/desk-uncollected-pre-prnum`**.
- Commits (subjects counted): `336982e2` feat(desk): collect the uncollected visits (42) · `a1193e77` feat(desk):
  price the unpriced visits (37). No `fixup!`, `style:` or `wip`; no tool attribution.
- `git push -u origin feat/desk-uncollected`; `gh pr create --assignee @me --label feat --label area:web --label
  area:docs`, titled `feat(desk): collect the uncollected visits` → **#117**
  https://github.com/Basel-Ghonaim/masaha/pull/117. Files: 48.

## CI and the end (2026-10-25)

`gh pr checks 117` on the pushed head `a1193e77` (the run's `head_sha` the same): build, check:classes,
check:conflicts, check:links, format:check, lint, test:api (5m21s), **test:component (11m53s)**, test:unit, typecheck —
all **pass**; CodeRabbit "Review completed". `mergeStateStatus` **CLEAN**. CI's full `test:component` passing judges
the local routes-file timeouts of commit 6's run.
- `origin/main` still `93225c3c`; open PRs: #117 only. Worker B's `feat/desk-api` (local branch of `app-b`, head
  `069aed70`, no PR yet) shares documents only with this PR — `docs/architecture/findings/README.md`,
  `docs/features/desk.md`, `docs/features/payments.md`; `git merge-tree --write-tree HEAD feat/desk-api` → no
  conflict. No shared code file (it does not touch this PR's code; this PR touches no `errors.ts`).
- No rebase in progress; `git status --short` clean; ports 3320 and 5320 free (servers stopped by process id).
  Local branch left: **`backup/desk-uncollected-pre-prnum`** (`backup/desk-api-pre-rebase` is worker B's).
- **Not merged.** Finding numbers: 164 (the plan's); no new one.
