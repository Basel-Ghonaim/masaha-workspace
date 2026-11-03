# Lane L working notes

## C3.1 Meter
- RED: Meter.component.test.tsx — "Test Files 1 failed (1) · Tests no tests" (module ./ not found: Meter not yet written)
- GREEN: Test Files 1 passed (1) · Tests 4 passed (4)

## C3.2 charts
- RED: BarChart/Heatmap component tests — "Failed to resolve import "." … Does the file exist?" · Test Files 2 failed (2)
- GREEN: Test Files 2 passed (2) · Tests 7 passed (7)
- B80 role missing: 4 failed (named meter, progressbar, bounds, axe)
- B81 kind ignored: × "as progress is a progressbar"
- B82: × "holds every value of every series in its hidden table" — expected ['August 2026120 ILS', …] to deeply equal ['August 2026120 ILS300 ILS', …]
- B83: × "draws a legend only for more than one series" — expected <ul> to be null
- B84: × "holds every cell in its hidden table, its caption the unit" — expected ['Sunday271'] to deeply equal ['Saturday049','Sunday271']

## C3.3 held item
- RED (before the code): × "is reached by the arrow keys and typeahead, its reason read" (React: Received `true` for a non-boolean attribute `held`; no aria-disabled) · × "does nothing when selected" — expected "vi.fn()" to not be called at all, but actually been called 1 times
- GREEN: Test Files 1 passed (1) · Tests 11 passed (11)
- B85 (`disabled` instead): × "is reached by the arrow keys and typeahead…" — expect(element).toHaveFocus()
- B86 (onSelect not prevented): × "does nothing when selected" — vi.fn() called 1 times

## C3.4 Input lg
- RED: × "is the large control at size lg, and the standard one by default" — expect(element).toHaveClass("h-(--control-height-lg)")
- GREEN: Test Files 1 passed (1) · Tests 7 passed (7)
- B87 (size ignored): × same test — Expected the element to have class

## Lint 1 (lane-l grant, tree at C3.3 + C3.4 wip): exit 1, 8 errors (restrict-template-expressions ×6, no-non-null-assertion, no-confusing-void-expression) → fixed by fixups into C3.1–C3.3

## C3.5 range and steps
- RED: rangeSummary.unit — "Cannot find module './rangeSummary'"; paginationView.unit — × "keeps a one-page list its steps, with no page before or after" (expected undefined to be null); ListPagination.component — × "keeps a one-page list its steps, both disabled" (Error: no pages)
- GREEN: unit Test Files 3 passed (3) · Tests 9 passed (9); component Test Files 1 passed · Tests 2 passed
- B88 (off by one): × "says 1–20 of 312 on the first page" — expected 'Showing ⁨0–20⁩ of ⁨312⁩' to be 'Showing ⁨1–20⁩ of ⁨312⁩'
- B89 (null at one page): × "keeps a one-page list its steps, both disabled"
- B89b (onlyPastOne ignored): × "gives a list that shows its steps only past one page none for one page" — expected {…} to be null
- Consumers' tests updated: AdminSpacesList "shows no pages when there is only one" → "keeps the steps of its one page, Previous and Next unavailable"; "shows a deleted space as a card" scoped to the cards (the pages are a list too); useAdminSpacesList, useDirectoryList: pagination null → steps null

## C3.6 page asked, refreshing
- RED: × "marks the page asked current at once, before its answer arrives" (aria-current); × DataTable "keeps its rows, dimmed and busy, while the next page refreshes them at 1280px/360px" (aria-busy); Refreshing — Failed to resolve import "."
- GREEN: Test Files 3 passed (3) · Tests 19 passed (19)
- B90 (the answer's page): × "marks the page asked current at once…"
- B91 (no aria-busy in Refreshing): × "marks its list busy and dimmed while it refreshes, the cards kept"
- B91b (DataTable's busy ignores refreshing): × both widths
- check:classes caught px-(--card-padding) in the showcase section → px-5
- C3.5's broad feature run (heavy) was queued and stopped before it started (machine under 4 GB): deferred to the lane-end full component lane

## C3.7 scroll
- RED: × "keeps the scroll where it is when Page 2 is followed" / "…when Next is followed" — expected "vi.fn()" (window.scrollTo) to not be called at all, but actually been called 1 times
- GREEN: Test Files 1 passed (1) · Tests 6 passed (6)
- B95 (page link without preventScrollReset): × "…when Page 2 is followed"; B95b (Next without it): × "…when Next is followed"

## C3.8 digits
- RED: westernDigits.unit — "Cannot find module './westernDigits'"; the five helpers' new extended-set cases × (wholeNumber, shekels, clockTime, coordinates "reads "۳۱٫۵۲، ۳۴٫۴۵" as a point", packageValues) — Test Files 6 failed | 7 passed (13) · Tests 5 failed
- GREEN: Test Files 13 passed (13) · Tests 57 passed (57)
- B92 (extended set dropped): × "reads both Arabic-Indic sets as Western digits" — expected '۰۱۲۳۴۵۶۷۸۹' to be '0123456789'; × wholeNumber — expected '۴۰' to be 40

## C3.9 row triggers
- RED: useRowTriggers.component — Failed to resolve import "./useRowTriggers" (before the move)
- GREEN: Test Files 1 passed · Tests 2 passed; staff + UsersPage + DropdownMenu green after the C3.3 fix
- B93 (trigger not registered): × "the row’s trigger takes the focus back when its dialog closes…" — Expected element with focus
- REGRESSION found by UsersPage tests: C3.3 passed aria-disabled={undefined} for an item not held, which overrode Radix's aria-disabled on a disabled item (× "holds the link for an admin, saying why", × "puts the role change first…"). Fixed in C3.3 (spread only when held) with a new assertion in "moves with the arrow keys, skipping a disabled item"; B85c (old line back): × that test — Expected the element to have attribute

## C3.10 csv, WhatsApp, fillReminder
- RED: csvOf.unit "Cannot find module './csvOf'"; whatsappLink.unit "Cannot find module './whatsappLink'"; downloadFile.component "Failed to resolve import "./downloadFile""; reminderTemplate.unit × fillReminder (2) — "TypeError: fillReminder is not a function"
- GREEN: web lib unit Test Files 12 passed · Tests 34 passed; downloadFile component 1 passed; shared space-settings Test Files 2 passed · Tests 8 passed; web space-settings unit 3 passed
- downloadFile's first green attempt failed on the test, not the code: jsdom's Blob.text() drops the BOM while decoding; the test reads the bytes
- B94 (no doubling of "): × "quotes commas, quotes and line breaks, and starts with a BOM"
- B79 (the + kept): × both whatsappLink tests — expected 'https://wa.me/+970591234567?…'
- Bfill (space not filled): × "fills every placeholder, each time it appears…"
- Bfill2 (replaceAll in sequence): × "puts a value in as it is…" — expected '$1 $1' to be '{المبلغ} $1'
