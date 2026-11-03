# Review of #129 — R2: the data reports (the owner's and the admin's) — Claude Code
Head: fcf46637 · range 2fa45cf8..dc427a54 (3 commits: 7d892c86, 44e8ee1f, dc427a54) · checks: green (build, lint, typecheck, test:unit, test:component, test:api, check:classes, check:conflicts, check:links, format:check; CodeRabbit skipping) · head moved during the review: no (`fcf46637` at the start and the end)
Verdict for my range: mergeable after a fix round (one should-fix to the document, and one should-fix to the sheet after `REPORT_ALREADY_DECIDED`; no blocker)

Everything below I saw in the code at `fcf46637`, unless it says *Only in a report*. I read every file my range adds or changes as it stands at the head, and diffed each one against `dc427a54`, so I know which later commits changed it (see *Outside my range*).

## Findings (verified defects only, most severe first)

### R2-F1 — should-fix · `data-reports.md` does not list finding 167 under *Open findings*
- Where: docs/features/data-reports.md:103–106 at fcf46637 (at `dc427a54`: line 91, «None.»)
- Seen in the code: `dc427a54` records finding 167 (*The admin's reports cannot be filtered by who handles them*, Open). That finding is about this capability's admin list. Yet the same commit leaves the capability document's *Open findings* as «None.». At the head, later commits add findings 168 and 180 to that section, but 167 is still missing. The template (documentation.md §5, item 9) says this section links the capability's open findings. The document's *Web decisions* links 167 inline (DI-39), so this only fixes the section's list.
- Scenario: a reader opens *Open findings* before changing the admin's list → it says nothing is open (at `dc427a54`), or it lists 168 and 180 only (at the head), while 167 is open about that same list.
- Fix: add «- [167. The admin's reports cannot be filtered by who handles them](../architecture/findings/167-the-admins-reports-cannot-be-filtered-by-who-handles-them.md) — no `verified` parameter on `GET /admin/data-reports`; «يعالجه» per row only.» · Belongs: a fix round on #129, folded into dc427a54. The section's later lines from R3 and the lead stay as they are.

### R2-F2 — should-fix · after `REPORT_ALREADY_DECIDED` under «جديدة», the sheet still says «جديد» and shows no decision
- Where: apps/web/src/features/data-reports/hooks/space/useSpaceReports.ts:74 and hooks/admin/useAdminReports.ts:99 (`latest = reports.find(…) ?? opened`), read by hooks/decide/useDecideSheet.ts:115 (`status`) and the `decided` block, at fcf46637
- Seen in the code: the sheet reads its report from the latest list page and falls back to the copy captured when it opened. On `REPORT_ALREADY_DECIDED`, `useDecideReport` invalidates the list, and `settled` makes the sheet read-only. Under the «جديدة» chip (`status=OPEN`), the refetched page no longer holds the report, because it is decided now. So `latest` is the stale open copy: the badge still says «جديد», `decision` is `null` (no «القرار» / «الردّ: …» block), and the alert says it was already decided. Under «الكل» it works, because the refetched row carries the decision. S4 is binding and says «… refetched, the sheet then read-only with the decision». The test («words REPORT_ALREADY_DECIDED, reads the list again and takes no decision then») renders the sheet over a fixed target, so it never reaches this path.
- Scenario: the owner triages under «جديدة» and presses «تم التصحيح». The answer is lost, so they press «لم يُعتمد» with a reply → 409 `REPORT_ALREADY_DECIDED` → the sheet shows «سبق البتّ في هذا البلاغ.» next to a «جديد» badge, with no decision and no buttons. The same thing happens to an admin when a second admin (or the space's new owner) decided first.
- Fix: one of these, smallest first:
  - once `settled` and the report is missing from the page, drop the stale status badge, or show «تمت المراجعة»;
  - keep the decided report, read it from the «الكل» key of the same scope (`client.getQueriesData` over `spaceAll`/`adminAll`), or refetch it into the sheet.

  Add a case to `SpaceReportsList.component.test.tsx` under `?status=open` (409, then a read without the row → no «New» in the sheet). · Belongs: a fix round on #129, folded into 44e8ee1f (the owner's; the admin's line folds into dc427a54).

### R2-F3 — nit · removing a filter tag, or pressing «مسح الفلاتر», drops the focus to the page
- Where: apps/web/src/features/data-reports/components/admin/FilterTags.tsx:15–23 at fcf46637
- Seen in the code: each tag's remove button unmounts as soon as the address changes, and so does «مسح الفلاتر» (`clear` becomes `null`, and with no tags `FilterTags` returns `null`). Nothing places the focus afterwards, unlike the rows' «فتح» (`onLeave` → the count).
- Scenario: a keyboard or screen-reader user removes «الحقل: …» → the focus goes to `body`, and the screen reader loses its place. The browser's sequential focus starting point usually survives, so Tab still continues near where the tag was.
- Fix: hand the focus to the next tag's remove button, else to «مسح الفلاتر», else to the count. One test: remove the first of two tags, and the second's button has the focus. · Belongs: a fix round on #129 (folded into dc427a54), or a finding (184) if the owner prefers.

### R2-F4 — nit (Plausible) · «تعديل الحقل»'s `#section` probably does not scroll on arrival
- Where: apps/web/src/pages/dashboard/space/reports/DataReportsPage.tsx:37 and admin/DataReportsPage.tsx:15 (the `#hours` / `#contacts` / … anchors) at fcf46637
- Seen in the code: the link carries the editor's anchor (LB-D14). The only thing that scrolls to a hash is React Router's `ScrollRestoration`, and it looks up the element once, as the navigation lands. The editor's cards (`SectionCard`, `ReadOnly*` with `id=…`) render only after the space's query answers. No editor code reads `location.hash` on arrival; only the desk's uncollected card does.
- Scenario (Plausible: not run, since this review runs no browser): from a report about the hours, press «تعديل الحقل» → the profile opens at its top, not at «ساعات العمل», unless the space was already cached. The real run did not follow the link (*Only in a report*: the lead's real run lists no visit to it).
- Fix: check it in the browser. If it does not scroll, have the editor scroll to (and focus) `location.hash`'s card once it has drawn, as `useUncollectedCard` does for its own. That change belongs to `spaces`, so record a finding (184 or 185) rather than fix it here.

## The plan's tests and breaks for my range (one line each: present / missing / weaker; would it fail?)

- **45** `FilterTag.component.test.tsx`: present (label, the button named by `removeLabel`, click and Enter, axe). Would fail: yes. Break «name left out» red (*Only in a report*: `break-45.txt`).
- **46** `dataReportsRepository.unit.test.ts`: present (the owner's list and decision, the admin's list and decision: paths, params, bodies; an `AppError`). Would fail: yes (breaks #46 and #46-admin, *in a report*).
- **47** `reportView`, `reportsQueryOf`, `adminReportsQueryOf` unit tests: present (six fields; status by audience; the Gaza day, never the time, with the year when not this one; no-message line; each filter read, a wrong one dropped). Would fail: yes (breaks #47a/b/c, *in a report*).
- **48** `useSpaceReports` «A visitor for every report, never a name»: present. It injects a `reporter` into one answer row and asserts that no row carries it, and that no time appears. Would fail: yes, if a row read `report.reporter` (break #48, *in a report*).
- **49** `useSpaceReports` states and chips + `SpaceReportsList` «decides a new report: it leaves «New», the toast says where it went»: present, split across two files (LB-D8). Would fail: yes (breaks #49, #53-leave, *in a report*).
- **50** `useDecideSheet` blank «Not accepted» focused, sends nothing; «Corrected» `{ status }` alone, once (three presses, one request): present. Would fail: yes.
- **51** `useDecideSheet` `REPORT_ALREADY_DECIDED` / decided read-only / 403 / the admin's verified read-only with its link / the admin's 403: present. **Weaker** on one point: the 409 case runs over a fixed target, so the sheet "read-only *with the decision*" after a refetch is never exercised (R2-F2).
- **52** `DecideSheet.component.test.tsx`: present at 390 and 1440 (named, the description «A visitor · 21 October», the reply focused first, «Edit the field» a link, axe). Would fail: yes (#52, #52-focus, *in a report*).
- **53** `SpaceReportsList` five columns from 768, cards at 390: present. Would fail: yes.
- **54** `useAdminReports` reporter named, «يعالجه», verified read-only, unverified decidable: present (the decision itself is in 51's admin case). Would fail: yes (#54a/b, *in a report*).
- **55** `useAdminReports` tags, removal replacing the address, «مسح الفلاتر» clears both with the chip kept: present. «At every width» is proven in 56 (the tag at 1024 and at 390). Would fail: yes (#55a/b/c; c green at first, then a test added, *in a report*).
- **56** `AdminReportsList` table from 1024, cards at 768, a sheet below 768, axe: present. Would fail: yes (#56).
- **57** `AdminSpaceFilter.component.test.tsx`: present (searches only while open, after typing pauses; «All spaces» clears; the chosen name or «A chosen space»). Would fail: yes (#57).
- **58** `routes.component.test.tsx`: present (owner: the page, the reporter a visitor; reception 403; admin: the page, the reporter named; an owner 403). Would fail: yes (#58, #58-admin).
- **Separate files the plan named and the lane folded:** `useSpaceReportsFilters` and `useAdminReportsFilters` have no tests of their own. Their address rules are proven through the hooks' tests (chip, page 1, `REPLACE`, every filter). Not weaker.
- **No test** for the focus after a tag's removal (R2-F3), and none for «تعديل الحقل»'s scroll (R2-F4). Neither was planned.

## Decisions taken without the owner in my range, judged

- **LB-D1** — the remove button is 32 px, and `--control-height` (44) on a coarse pointer: **sound**. The plan's `size="icon"` would be 40 px on a desktop inside a body-sm pill. 44 on touch is kept (*Only in a report*: measured 44×44 in the real run).
- **LB-D2** — foundation §3's `display` row lists `FilterTag`: **sound** (one map of the layer).
- **LB-D3** — the showcase's words are kept apart from the catalogue («… في العرض»): **sound** (finding 4's clash in `check:build`).
- **LB-D4** — commit 2's keys and repository hold the owner's parts only: **sound** (atomic commits; commit 3 adds the admin's).
- **LB-D5** — `byline` and `sheet.close` added; `admin.allSpaces` replaced by `spaceLinks.choices.allSpaces`; the phone sheet's count reuses `payments.ledger.filters.applied`:
  - the first two: **sound**;
  - `allSpaces`: **sound** (§9 already named that key; one word, one home);
  - the reuse of `payments`' words: **acceptable**, though it ties data reports' wording to the ledger's section. A neutral shared key would be cleaner.
- **LB-D6** — the decision's status in the form's values (`setValue` / `useWatch`): **sound**. It keeps `useServerForm`'s one schema check, with `required` on `note`.
- **LB-D7** — the sheet's first focus left to Radix: **sound**. Radix's `FocusScope` skips links (`removeLinks`), so the focus lands on the reply, past «تعديل الحقل». Test 52 proves it, and the browser confirmed it (*in a report*).
- **LB-D8** — test 49 split between the hook's test and the list's: **acceptable**.
- **LB-D9** — the focus goes to the count when the opened row leaves (a layout effect's cleanup, `onLeave` stable through `useCallback`): **sound**.
- **LB-D10** — the fixtures in `src/test/dataReport.ts`: **sound**.
- **LB-D11** — `toastDecided` in `components/toast/`: **sound** (it draws JSX).
- **LB-D12** — `AdminSpaceFilterSlot`, with `space-links`' own Combobox over `useSpaceChoices({ enabled: open })`: **sound**. No feature imports another, and the page composes.
- **LB-D13** — `ReportListParts.tsx` moved unchanged: **sound**.
- **LB-D14** — the field → anchor map in `pages/dashboard/fieldSections.ts`: **sound** placement (pages own routes). See R2-F4 for whether the anchor scrolls.
- **LB-D15** — any admin 403 on a decision worded as «هذه المساحة موثّقة…», the list re-read, `['me']` untouched: **acceptable**. It is S5's line. A demoted admin's 403 would be worded the same way, which is rare and harmless.
- **LB-D16** — «مسح الفلاتر» takes off the space and the field and keeps the chip; «عرض الكل» clears everything; the toast's «عرض» sets `decided` and keeps the rest: **sound**. The chip is always visible, and the tags are the space and the field (DI-40).
- **LB-D17** — the admin's non-admin 403 test uses the existing heading pattern: **sound**.
- **LEAD-D1** (no seam commit): **sound** for this range. The joins kept both sides, and I found no duplicated or lost line in `routes.tsx`, the copy indexes, `routes.component.test.tsx` or architecture §2.
- **LEAD-D2** (lane C rebased onto lane B's commit 2): **sound**. R3's additions to my files are purely additive (below).

## Outside my range (one line each, for the other reviewers)

- R3: in my range's files R3 only **adds**: `queryKeys.ts` gains `mineAll`/`mine` (note `mineAll` is a constant while `spaceAll`/`adminAll` are functions; style only); the repository gains `myReports` and `report` (S15's `apiClient.post` + `unwrap`); `index.ts` gains `MyReportsList` and `ReportAction`; the copy gains `mine` and `report`; `src/test/dataReport.ts` gains `myReport()`; `data-reports.md` gains the user's lines. No line of the owner's or the admin's code changed after `dc427a54`. Nothing defective seen in those additions as they touch my files.
- Lead (commit 6 / LEAD-D10): `data-reports.md`'s *Open findings* gains 180. The section's missing 167 is mine (R2-F1), not theirs.

## Checked and fine

- **Privacy (owner):**
  - `SpaceReport` has no reporter. The owner's rows, card, sheet (`description` «زائر · {day}»), toast, query key (`['space', id, 'dataReports', { status?, page, limit }]`), address (`?status=&page=`), fixture (`spaceReport()`), routes test and documents name or hint at no one.
  - No per-person count. The day only, never the time (`reportDay`, Gaza calendar, year when not this one).
  - The reporter appears only in `AdminReport` / the admin's rows, sheet and tests.
- **Who decides:**
  - The owner's page is owner-only (reception's 403 in the routes test). The decision is `PATCH /manage/…/data-reports/:id`.
  - The admin decides only `verified: false` (read-only notice, «عرض المساحة», «عرض» on the row's button); the server's 403 is still worded and settles the sheet.
  - The owner's 404, and 403 with no code, invalidate `['me']`; the admin's do not.
- **The decision:**
  - `decideReportSchema` through `useServerForm`: a blank reply is `undefined`, trimmed and bounded (1–500, NFC) by the shared `paragraphSchema`.
  - «لم يُعتمد» blank → `required` on `note`, focused, nothing sent. «تم التصحيح» → `{ status }` alone.
  - Sent once (the buttons `aria-disabled` and guarded while pending; no key header). A lost answer gets the sheet's own line and a retry.
  - Escape and outside-press are blocked while busy. The focus returns to «فتح», else to the count.
- **Invalidations:** the owner's → `['space', id, 'dataReports']`; the admin's → `['admin', 'dataReports']`, as S3 says. No sidebar counts exist yet (step 12).
- **The admin's filters:**
  - status, field and space in the address, each fallback by the server's rule (`positive`, the six fields); every change `replace`s and returns to page 1.
  - «مسح الفلاتر» and «عرض الكل» behave as LB-D16 says. Tags at every width. The space's name comes from the page's rows, else «مساحة محددة». The phone sheet shows the count and «عرض {n} بلاغ» / «لا نتائج — غيّر الفلاتر».
- **`FilterTag`:**
  - semantic tokens only (`bg-secondary`, `text-secondary-foreground`, `rounded-(--radius-pill)`, `text-body-sm`) and logical `ps-3`;
  - the `XIcon` is `aria-hidden`, and the button is named by `removeLabel` (no built-in words);
  - exported from the layer's barrel; foundation §3 and §12 rows; the showcase section and its fixtures.json words in both languages.
- **Layout:**
  - the owner's table from 768 px (`DataTable` default) with five columns, the message `line-clamp-2` and `dir="auto"`, a card below 768;
  - the admin's `cardsBelow="lg"` with eight columns, and the filters inline from 768 (`useMediaQuery`);
  - the sheet `side="end"`.
- **Copy:** every string goes through `dataReports` / `spaceLinks.choices.allSpaces` in both catalogues. The Arabic matches §9 as approved, plus LB-D5's two words.
- **Documents:**
  - `data-reports.md`'s header, *Who uses it*, both web *Behaviour* paragraphs, *Web decisions* (S8, DI-31…43, S4), code map and *Web history* are true to the code (apart from R2-F1).
  - `space-links.md`'s one line; foundation §3 and §12; architecture §2 (both clauses, in place after the joins); `overview.md`'s Data reports line.
  - Finding 8 is *Resolved*, with its resolution and its index move. Finding 150 has its evidence line. Finding 167 is Open and indexed. Every one carries `#129`, with no `#PRNUM` left.
- `features/space-links` exports `AdminSpaceFilter`. The pages compose it (no feature → feature import), and the admin's page builds both slots at module level, so they are stable.
- The size of `data-reports.md` (1,429 → 2,681 words in the range; 3,629 at the head) passes the template's ≈ 1,200. Merged documents of the same kind are larger (`payments.md` 3,402), and the plan watches this under finding 98, so I record no finding.

## Not checked, and why

- No browser, test or build was run (this review is read-only). The 44 px touch target, LB-D7's first focus, the widths and the real-run writes are *Only in a report* (`4_REPORT_LEAD.md` › *The real run*; `scripts\lane-b\REPORT.md`).
- Whether «تعديل الحقل»'s anchor scrolls (R2-F4): needs a browser.
- The red and break outputs (`scripts\lane-b\break-*.txt`) were not opened one by one. I judged each test's ability to fail from its assertions against the code.
- Lane A's and lane C's code, the API and `packages/shared` beyond the data-reports schemas and types the web imports: other ranges, and the API is merged.
