# lane W3 notes
## C7.1
red: WriteOffDialog.component.test.tsx › "focuses its reason on opening, not «Back»" — expected textbox Reason to have focus; focus on <button>Back</button>
green: 2 files 4 tests (write-off dialog + hook)
B209 = red step (handler absent, autoFocus stripped by the test's mock as a browser does)
## C7.2
T200 red: logRows.unit.test.ts — Cannot find module './logRows' (code absent)
B209 re-shown 2026-10-30 from a backup copy (brk.py): × focuses its reason on opening, not «Back» — focus on Back
## C7.2 (DeskLog)
T200 red: Cannot find module './logRows'; B200 (visits sorted first): × merges visits and check-ins latest first; × orders two stays…
B201 (day: true for reception): × reads the owner’s chosen day; reception reads today with no picker and no range
B202 (method null): × names each row’s kind, times, stay and how it ended…
B203 (empty title blank): × says «No one came on this day» for an empty day
green: DeskLog 4/4, logRows 2/2, copy+repository unit 46/46
routes.component.test: 2 failures (payments 403 / my-payments, role=main not found within 3 s) — finding 87's family; passed 55, the desk route green. -t payments alone: first test misses again (lazy first import).
## C7.6
T210/T211 written after the code; reds by breaks from backup copies:
B210 (the side block moved back after who is here): × puts the uncollected card before who is here… — AssertionError: expected +0 to be truthy
B210b (no hidden class on empty): × puts the uncollected card … hides it below xl when empty
B211 (usePresentList failed, not offline): × shows the offline state when who is here and the uncollected get no answer
Existing tests changed to the new decisions: useDeskSearch "says it is offline" (state offline), useUncollectedCard empty heading «Not collected».
green: 41/41 (occupancy, uncollected, search, DeskPage)
## C7.9
B216 (full by status): × is full by the count, with its ratio, not by a manual «Full»
B217 (chip deselect ignored): × offers the shifts as chips one may deselect, «Student» a switch…
B218 (calc []): × names the rate and the amount in its line, the cap…, and a day price alone
green: check-in 5, check-out 2, DeskPage 3+1, money/collect/pay/check-out hooks 21, copy 33; typecheck first run exit 2 (DeskSearch test's full:false) fixed, re-run exit 0
Decision: MoneyBlock side-by-side from md applies to every money block (collect, pay too)
Decision: capped charge line omits "= amount" (cap line says the day price) — the web never computes h×rate
## C7.10
B219 (no lookup: owner always null): × says whose file a valid typed phone adds to, once typing pauses, or a new customer
existing debt test counted every request; now counts the PUT (the lookup is a read)
green: debt 4, check-out/uncollected 17; eslint 0, typecheck 0
## C7.11
B220 (limited branch off): × says a 429 recorded nothing, and that a retry after it won’t record twice
green: 37 + 63 desk/occupancy component tests; eslint 0 typecheck 0
Decision: PhoneInput component in desk for the placeholder; icons from the layer
## C7.12
B221 (dialog branch off): × opens a usage-based subscriber’s due after the tap…
B222 (dialog for every one): × keeps a fixed subscriber’s check-out one tap, with its toast
green DeskPage 5 + subscriber/search 23; eslint 0 typecheck 0
Decision: the dialog lives in DeskPage (the row leaves on check-out); focus returns to who-is-present's heading
## C7.13
T224 red: Cannot find module './endNote'
B223 (native date input): × asks its dates with the layer’s date pickers…
B224 (always noEnd): × words a total and an end, a total alone, and neither
B225 (due label not Total): × warns of an earlier debt…
B225b (no prefill): × prefills a usage-based custom rate…
useSubscriptionSheet tests: two 'From' toHaveValue asserts changed to the date picker's button name
eslint first run: 3 String() errors fixed, re-run clean; typecheck 0
- rebase onto a417ed04: conflicts in docs/features/occupancy.md (C7.6) and docs/features/visits.md (C7.14) History; kept both lines. After: desk/occupancy/desk-page component 46/188, unit 26/102 green
## C7.3 (second agent)
T204–T206 red (code absent): WrittenOffVisits.component.test.tsx × 4 — "Unable to find role="radio" and name "Written off""; reception test passed (nothing to see) → proven by B206
B204 (writtenOffBy name dropped): × lists who, when, how much and why, by whom…
B205 (mutation retry: 1): × sends a failed undo once… — expected 2 to have a length of 1
B206 (toggle for every role): × is never offered to reception… — expected <button> to be null
green: written-off 5, uncollected card+hook 9 (14)
RWO (repository sends no page): × reads the owner’s page of the written-off visits
C7.3 commit 63599430; checks prettier 0, eslint 0, typecheck 0 (first exit 2: stale Prisma client after the rebase → npx prisma generate in apps/api, gitignored output; then 0)
## C7.4
T207 red (test first): useSubscriberCheckIn › "checks one with no subscription in as their visit, by their id and name…" — expect(element).not.toHaveTextContent (the note still there)
B207 (by name only): same test — expected { visitorName, …(1) } to deeply equal { …(2) }
green: subscriber hooks/components + search 18; copy unit 33; prettier/eslint/typecheck 0
## C7.5
T208 red (tests first): useSubscriptionSheet × "subscribes from a published price…" (expected published …(3) to deeply equal …(4)); × "keeps the sheet open on a changed price…" (refreshPrices called 0 times); "keeps an amount the desk typed…" passed (existing rule) → proven by B208b
B208 (closes on PUBLISHED_PRICE_CHANGED): × keeps the sheet open… — onClose called 1 times
B208b (money block ignores the typed figure): × keeps an amount the desk typed… (+2 existing)
publishedChoices unit test updated to the amount sent (red before: deeply equal …(2))
green: sheet hooks+components 27, desk services unit 46; prettier/eslint/typecheck 0
## C7.7
T212/T213 red (tests first): PresentList × "links a subscriber’s name to their file, names their plan, and shows the time alone" (no link Sara); × "says a student’s visit «Visit · student»"
B212 (plan ignored): × links a subscriber’s name…; B213 (always «Visit»): × says a student’s visit…; B212b (no link in PresentName): × links…; B212c (uncollected row no link): × leads a customer’s visit to their file…; B212d (no optional mark): same; B212e (since worded in the cell): × links…; B212f (card title no link): × DeskSearch is named and controls…
Existing tests changed to the new shape: usePresentList kind object/customerId/time; usePresentMatches kind object; MemoryRouter added to DeskSearch and useSubscriberCheckIn tests (card title is a Link)
green: occupancy+desk+desk page 197/47 files; copy+occupancy unit 45; prettier/eslint/typecheck 0; check:classes, check:links clean
## C7.8
T214/T215 red (tests first): CustomerCard.component.test × 4 — "Unable to find … This week 3 of 3", "… button Renew", "… Check in Sara Khalid" (test matcher fixed to heard())
B214 (no progress lines): × shows its subscription’s progress and «Not here»…; B214b (no «Not here»): same; B215 (no card «Renew»): × renews one ending soon…; B215b (no choice «Renew»): × offers «Renew» on an expired one’s choice…
progressLines refactored: limitLines exported (progressLines unit 3 green)
eslint first exit 1: fetchQuery deprecated → client.query; re-run 0; typecheck 0
green: desk components+hooks+page 180; copy+services unit 79
## C8.1 (third agent)
T230–T232 red (tests first): StateActions.component.test × 3 — "Unable to find role="menuitem" and name "Check out""; × 2 "No header actions" (no state buttons in the header)
B230 (no state items in the menu): × a present customer's menu… ; × offers «Renew»… (menuitem Check out not found)
B230b (no oldest description): × a present customer's menu… — expected '' to match /^Oldest item: Visit of /
B231 (no header buttons): × the file's header holds… — expected [ 'More actions: Sara Khalid' ] to deeply equal [...]
B232 (header renew when ACTIVE): × the file's header… ; × offers «Renew» only while…
B232b (card renew always): × offers «Renew» only while…
green: state actions 3/3; desk comp (file, customers, menu, pay, card, check-out, search, hooks) 15 files / 55; unit copy+services 21/79; prettier 0, eslint 0 (first 1: nested objectContaining any → mock.calls), typecheck 0, links, classes clean
## C8.2
T233 red (tests first): CustomerFile × "the file's reminder link holds the filled template…", × "offers no reminder… the default text" — Unable to find role="link" and name "WhatsApp reminder"
B233 (default always): × the file's reminder link holds the filled template
B233b (whole name): × both reminder tests
green: file/statement/state-actions/file hook 4 files 16; prettier, eslint, typecheck 0
## C8.3
T234 red (tests first): Statement × 2 (390, 1440) — Unable to find text "Recorded by Ahmad"; CustomerFile × "heads its sections…" — Unable to find /Recorded by Mona/
Existing tests changed to D8.3: Statement "offers reception no «⋯»" and useStatement "strikes a voided payment…" now expect «Voided by Ahmad: Entered twice» (the ledger's line), voidedReason removed
B234 (no recordedBy in the statement): × opens in its card… at 390, at 1440
B234b (unpaid payments not passed): × heads its sections h2…
green: statement/file/uncollected/hooks 20; prettier, eslint, typecheck 0; links clean
## C8.4
T235–T238 red (tests first; code written, card not wired): CorrectSheet.component.test × 6 — Unable to find button "More actions: Exams by the hour" (no card «⋯»)
First green run: 1 × (test's fake answered the PATCH without the saved hours → resent; test fixed to answer what it saved)
B235 (name always sent): × sends only the changed fields…; × PRICE_BELOW_PAID…
B236 (price for every role): × shows reception no price section
B237 (no failure in the sheet): × says PRICE_BELOW_PAID inside the sheet…
B238 (never held): × holds an ended subscription's item…
B235f (onOpenAutoFocus handler removed): stayed green — Radix's own first focus is the name; handler removed as redundant (LW3-D15); B235g (name not tabbable): × sends only the changed fields, the name focused first…
RCS (correctPrice to the PATCH path): × corrects a subscription's terms and its price, each with no key
green: correct 6, file/statement 17 total; repository+copy unit; prettier, eslint, typecheck 0; links, classes clean
## C8.5
T239 red (test first): useCustomersList × "offers the type filter monthly and weekly first…" (order PACKAGE, WEEK, MONTH…)
B239 (no MONTH/WEEK): × same
green: customers hooks+list 14; prettier, eslint, typecheck 0
## C8.6
T240–T243 red (tests first): CustomersList × "says no customers yet with its icon…" (expected null not to be null: no svg); CustomerFile × 2 ("They count in their balance." / "Here since" not found); PaymentsLedger, MyPaymentsToday × "shows its range in the footer…" (no "Showing 1–2 of 2")
Existing test changed: useCustomerFile header.here now «Here since 10:00»
B240 (add hidden in the row): × says no customers yet…; B240b (no empty icon): same; B240c (no summary): same
B241 (more null): × offers the owner «Write off…»…
B242 (success badge): × says «Here since {time}», info…; B242b («Here now»): same; B242c (only-visits always): same
B243 (ledger no summary): × shows its range…; B243b (mine no summary): × same (mine)
B243c (one icon for both empty states): first stayed GREEN — the test's 'Clear filters' found the toolbar's button, closest(empty-state) undefined passed not.toBeNull; test strengthened (icon class read from the empty state itself) → × shows its range… and its empty states' icons
B243d (mine no icon): × shows its range… and its empty state's icon
green: 14 files / 63; copy unit 33; prettier, eslint, typecheck 0; links, classes clean
## finding 212 — own commit (docs: record finding 212)
## C8.7
T244 red (tests first): useLedger × "names the space's other owners after the owner signed in…" (label 'Mona' not 'Mona · owner'); ledgerPeople unit — Cannot find module './ledgerPeople'; useSpaceOwners — Failed to resolve import "./useSpaceOwners"
PaymentsPage page test written after the code → B244 (page passes owners: []): × names the space's other owners in the staff filter…
B244b (no owner label): × names the space's other owners after the owner signed in…
green: spaces owners 2, payments comp 24 (with the page 1), payments+copy unit 49; prettier, eslint, typecheck 0; links clean
