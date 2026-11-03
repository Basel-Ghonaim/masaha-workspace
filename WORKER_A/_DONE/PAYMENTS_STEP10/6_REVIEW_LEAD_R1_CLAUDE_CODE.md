# Review of #129 — R1: the foundation and the announcements — Claude Code
Head: fcf46637 · range origin/main (76661f7c)..2fa45cf8 (7 commits) · checks: green (10 pass, CodeRabbit skipping) · head moved during the review: no (`fcf46637bf84ab2de598abf0f8080bb42f8964f2` at the start and at the end)
Verdict for my range: **mergeable after a fix round** (R1-F1 is a blocker, R1-F2 should-fix)

Every point below was read from commit objects (`git show <sha>:<path>`, `git diff`); nothing was run. Files of my range that a
later commit changed (`AnnouncementSheet.tsx`, `ClosureNotice.tsx`, `AnnouncementItem.tsx`, `index.ts`, `announcements.md`,
`foundation.md`, `architecture.md`, `overview.md`, `src/test/announcement.ts`) were read at the head; none of those later changes
touches a finding below. No new finding numbers used (181–183 left free): every defect is in the PR's scope.

## Findings (verified defects only, most severe first)

### R1-F1 — blocker · An edit sends a start the user never touched, truncated to its minute
- Where: `apps/web/src/features/announcements/services/sheetRequest.ts:113` (`valuesOf`: `startsAt: clockOf(start.minute)`) and
  `:64` (`editRequestOf`: `if (!sameInstant(startsAt, loaded.startsAt)) request.startsAt = startsAt`) at fcf46637.
- Seen in the code: the sheet loads a start as its Gaza date and **minute** (`gazaClockOf(...).minute` drops seconds and
  milliseconds), then `editRequestOf` rebuilds the instant from that minute and compares it with the loaded instant to the
  millisecond. The server stores "now" with its seconds whenever a start is not typed: a post with «الآن» (the sheet's
  default — `announcements.service.ts` `startsAt = request.startsAt === undefined ? at : …`) and «ابدأ الآن» (`startsAt: at`).
  For every such announcement the two never match, so **any** save of its sheet — even one with nothing touched — sends
  `startsAt` moved back by up to 59.999 s. The API's `announcementChange` compares instants exactly, so it writes the new
  start and audits `announcement.edited` with a `startsAt` before/after nobody chose, and `periodErrors` then checks the start
  against now. Every fixture (`src/test/announcement.ts`, `sheetRequest.unit.test.ts`'s `LOADED`) is on a whole minute, so no
  test can see it.
- Scenario:
  1. Reception posts an announcement «الآن» (the default), opens «تعديل», presses «حفظ» without a change → `PATCH { startsAt:
     "…:00.000Z" }`, toast «حُفظ الإعلان», the start recorded and audited as moved; «لم يتغيّر شيء» (LA-D4) is never said
     for it. The same happens when only the English text is added — the real run's own case («إعلان تجربة», posted now,
     `announcement.edited` 13:29:21). I did not read that audit entry's body; by the code it carries `startsAt`.
  2. The owner extends a closure posted «الآن» (or started with «ابدأ الآن»), then corrects its text, which the contract
     allows (LA-D14 keeps «تعديل» for that) → `409 CLOSURE_EXTENDED`, worded «…فلا يمكن… تغيير نوعه أو بدايته…»: the text of
     an extended closure can never be corrected, and the refusal blames a start change the owner did not make.
  3. An announcement posted «الآن» with no end, running for more than 30 days: any edit of its text → `422 out_of_range` on
     `startsAt` («البداية بين 30 يومًا مضت و365 يومًا قادمة.») on a start the user never moved.
- Fix: decide "changed" at the precision the sheet shows: in `editRequestOf`, send `startsAt` (and `endsAt`) only when the
  typed Gaza date and minute differ from the loaded instant's `gazaClockOf` date and minute (or compare against the loaded
  instant truncated to its minute). Tests: `editRequestOf` with `startsAt: '2026-07-01T05:00:42.123Z'` and nothing changed →
  `{}`, and with only `textEn` changed → `{ textEn }`; in `useAnnouncementSheet.component.test.tsx`, «Save» untouched on such
  a start sends nothing and says «Nothing changed». Belongs: a fix round on #129 (folded into `74000c57 feat(announcements):
  post and edit an announcement`).

### R1-F2 — should-fix · A 409 in the extension's or the delete's dialog unmounts the dialog with the list's refetch
- Where: `apps/web/src/features/announcements/components/list/ClosureLine.tsx:16` (`ExtensionAction`, which owns the
  `ExtensionDialog`, `ExtensionAction.tsx:50`, is drawn only while `card.extension !== null`) and
  `apps/web/src/features/announcements/components/list/AnnouncementCard.tsx:80` (`AnnouncementMenu`, which owns the
  `DeleteDialog`, `AnnouncementMenu.tsx:73`, is drawn only while `remove !== null`) at fcf46637.
- Seen in the code: each dialog is a child of the control that opens it, and that control is drawn from the card's current
  state. On `409`/`404` both hooks call `settle(spaceId)` (by design, S3), which refetches the list; when the refetched card no
  longer offers the control — extended (`CLOSURE_ALREADY_EXTENDED` / `CLOSURE_EXTENDED`), moved to upcoming
  (`ANNOUNCEMENT_NOT_STARTED`) or deleted (404) — the control unmounts and the open dialog with it. The refusal the plan
  wants kept in the dialog (DI-19, §2 PR 2: "a failure stays in the dialog… `CLOSURE_ALREADY_EXTENDED` worded") shows only
  for the refetch's round trip. Plausible, not run: the focus then falls to `body` — the dialog's `onCloseAutoFocus` finds
  its trigger disconnected (`returnFocus` does nothing; the menu's `else onGone()` may move it only when the card has
  another action), and `useCardFocus` holds nothing, the focus having been in the dialog's portal.
- Scenario: two owners on one closure (the plan's own Review Focus case): A opens «تمديد الاشتراكات», B extends from another
  tab, A presses «مدّد 4 اشتراكات» → `409 CLOSURE_ALREADY_EXTENDED` → the line flashes and the dialog vanishes as the card
  turns to «مُدّد 4 اشتراكات · …», a keyboard or screen-reader user left on the page's body with nothing said. The same for
  «حذف…» on a closure extended meanwhile (`CLOSURE_EXTENDED`). The card's new line is true, so no wrong data is shown; the
  defect is the lost refusal and focus. Tests 38 and 41 render the hooks' dialogs alone, outside the list, so they pass.
- Fix: keep an open dialog mounted independent of the card's current offer — hold the opened dialog (the closure or the
  card being deleted) at the list, as `AnnouncementsList` already holds the sheet, or let `ExtensionAction` /
  `AnnouncementMenu` keep rendering while their dialog is open; on close, hand the focus to the card's next action or the
  tabs (`useCardFocus.leave`). Add a list-level test: the extension answered `409 CLOSURE_ALREADY_EXTENDED` and the list's
  refetch answering the closure extended → the dialog stays with its line until «رجوع», then the focus is on a card action
  or the tab. Belongs: a fix round on #129 (folded into `2fa45cf8` for the extension, `2279134a` for the delete).

### R1-F3 — nit · Finding 169's resolution says only the ledger and the showcase import the calendar entry
- Where: `docs/architecture/findings/169-the-calendar-rides-in-the-sites-first-download.md:9` at fcf46637.
- Seen in the code: `features/announcements/components/sheet/PeriodFields.tsx:7` imports `@shared/design-system/calendar`
  too (`74000c57`, the same PR). The line was true at `4ebc2785` and is false at the merge. A nit only because it is a dated
  resolution and finding 180 records the announcements' reach.
- Fix: "…which only the ledger's filters, the announcement sheet's period and the showcase import". Belongs: a fix round on
  #129 (folded into `74000c57`, which adds the importer).

### R1-F4 — nit · The sheet's calendar marks the browser's today, not Gaza's
- Where: `apps/web/src/features/announcements/components/sheet/PeriodFields.tsx:35` at fcf46637.
- Seen in the code: the dates are mapped Gaza date ↔ calendar day without a zone shift (correct), but `Calendar` gets no
  `today`, so react-day-picker marks `new Date()`'s day in the browser's zone (`aria-current`, the `today` style).
- Scenario: an owner whose device is not on Gaza's zone (travelling, or a wrong device zone) near midnight sees "today"
  ringed on the wrong day in a sheet whose every other date is Gaza's (S9).
- Fix: pass `today={dayOf(gazaClockOf(new Date()).date)}`. Belongs: a fix round on #129 (folded into `74000c57`), or left.

## The plan's tests and breaks for my range (one line each: present / missing / weaker; would it fail?)

The breaks below are as lane A's report records them (`scripts\lane-a\REPORT.md`, `break-*.txt`); I read each test's code,
not its run.

- 25 repository (list, summary, post with key, `PATCH` edit no key, end/start/delete, preview, extension with key) — present; would fail (break recorded: key dropped).
- 26 `periodText` same day / two days / no end / another year / 08:00 in summer and winter — present; the unit lane's `TZ` (New York) makes a browser-zone reading fail (break recorded).
- 27 `typeView`, `textOf`, `announcementsQueryOf` — present; would fail.
- 28 tabs' counts from the summary, tab and page in the address, server's order — present; would fail.
- 29 three skeletons, failure, empty per tab, pages only past one — present; would fail.
- 30 `AnnouncementsList` named tabs, badges, no status badge, tone, axe at 390 and 1440 — present; would fail.
- 31 `sheetRequest` Gaza instants summer/winter, «الآن» no start, no end, minimal edit, `textEn: null`, `endsAt: null` — present; **weaker**: every loaded instant is on a whole minute, so it cannot catch R1-F1.
- 32 one key for the post, kept on lost answer / double press, new opening new key — present; would fail.
- 33 `out_of_range` on fields, `CLOSURE_EXTENDED`, 403, unchanged edit sends nothing — present; **weaker**: the unchanged-edit case uses a whole-minute start (R1-F1), and its `CLOSURE_EXTENDED` case refuses a text-only edit, which the contract never does (only a type/start/later end is refused) — real only through R1-F1.
- 34 toast names the tab, «عرض» opens it — present; would fail.
- 35 checked radio focused first, closure line, preview, axe — present; would fail.
- 36 end now, its «تراجع» one `PATCH` with the old end, none on an extended closure, start now, nothing re-sent — present; would fail.
- 37 actions by state, no «حذف…» on an extended closure — present; would fail.
- 38 delete names it and its consequence by state, `CLOSURE_EXTENDED` worded, sent once — present; **weaker** for "keeps the dialog": rendered outside the list, so the unmount of R1-F2 is not reachable.
- 39 `AnnouncementMenu` named, focus back on «⋯», card gone → next card or tabs — present; would fail.
- 40 preview on opening, days prefilled, typed days sent with one key, same on retry, new opening new key — present; would fail ("proposal sent" break recorded). The "new opening" is two separate mounts, not a reopening through `ExtensionAction`; by the code a reopening remounts too (`opening` back to 0 on close), so equivalent.
- 41 failure stays with days kept, `CLOSURE_ALREADY_EXTENDED` worded and list read again, none covered → no submit, applied meanwhile → its line — present; **weaker**: dialog rendered alone (R1-F2).
- 42 reception: no action, its line; a 403 worded — present; would fail.
- 43 alertdialog named, submit counts in Arabic's forms (1, 2, 3, 11, 100), axe — present; would fail.
- 44 routes «الإعلانات» for both roles, titled — present; would fail.
- Finding 173: "starts a range on a first click, ends it on the second, and starts afresh on a third" — present and real (red recorded: the first click gave `to` = `from`). "A caller may still set it" is untested, but the spread order (`{...props}` last, `Calendar.tsx`) makes it hold.
- Finding 169: `libraryChunks.unit.test.ts` (react-day-picker, its locale, date-fns → `calendar`; `@date-fns/tz` and the layer's `Calendar.tsx` left out) and `layerEntries.unit.test.ts` (the entry allowed) — present; red recorded. `check:build` red through the main barrel recorded (LEAD-D3, below).
- Missing: none of 25–44. Missing beyond the plan: a test for R1-F1's case and a list-level test for R1-F2's.

## Decisions taken without the owner in my range, judged

- **LA-D1** (#128's count: «يشمل التمديد {n} اشتراكات.» / "The extension moves {n} subscriptions.", and the line naming the covered ones and their renewals not started) — **sound**: true to the contract's `ExtensionPreview.subscriptions` since #128; the six Arabic forms kept; S11's «لم يشمل هذا الإغلاق أي اشتراك» stays true (no covered one, no renewal). The title «…التي شملها الإغلاق؟» is a shade narrower than the count, but the text under it names both.
- **LA-D2** (report as text) — acceptable (harness).
- **LA-D3** (`SheetValues`' time fields named `startsAt`/`endsAt`, so a period refusal lands on its time) — sound.
- **LA-D4** (an unchanged edit says «لم يتغيّر شيء», sends nothing) — sound as designed; defeated by R1-F1 for any start with seconds.
- **LA-D5** (`sheet.close`), **LA-D6** (toasts file in c2), **LA-D13** (`useAnnouncementsFilters` own test, `onDone`), **LA-D15** (test 29 updated in c4) — acceptable.
- **LA-D7** (focus keeper `useCardFocus`, last resort the tab shown) — sound (the plan's "the tabs' list", made concrete).
- **LA-D8** (5.h by `onOpenAutoFocus`) — sound.
- **LA-D9** (`ExtensionAction.tsx`, not in §8; the card's next action takes the focus when it leaves) — acceptable; its placement of the dialog under a control drawn from the card's state is R1-F2's cause.
- **LA-D10** (the days focused at opening, or by `autoFocus` once the preview arrives) — sound.
- **LA-D11** («تراجع» calls `repository.edit` directly, then reads the space) — acceptable: one `PATCH`, no key, `linkEnded` and `settle` on failure.
- **LA-D12** (end/start failure toasts `duration: Infinity`) — acceptable: the toast holds the only retry.
- **LA-D14** (an extended running closure keeps «تعديل») — sound by the contract (its text and an earlier end change); broken in practice for a closure posted «الآن» by R1-F1.
- **LEAD-D1** (no seam commit) — sound.
- **LEAD-D3** (169's break through the main barrel from Home) — **acceptable**. Home is itself lazy, so the break shows the shared-chunk path — the barrel's chunk in the first download statically importing the `calendar` chunk — which is #127's mechanism. It does not reproduce #127's exact case (only a dashboard page drawing the calendar through the barrel); by the code the guard fires there too if Rolldown places the layer's `Calendar.tsx` in the barrel's shared chunk as it did then — plausible, not proven by the break. The lazy-shell break staying green is correct behaviour (outside "first download"), and finding 180 (R3's) is the honest record of what the guard does not cover.
- **LEAD-D4/D5/D6** (worktrees, the grant script, reports as text) — acceptable (process; no code effect).
- **LEAD-D7 → LEAD-D11** (react-day-picker pre-bundled for the component lane, `deps.optimizer.client`, its own commit `a23896a7`) — **sound**. `vite.config.ts` changes only `test.projects[component].test.deps`; `build` is untouched. It hides no user-facing defect: the build serves the library as one 71 KB chunk and the dev server pre-bundles dependencies anyway — the 3 s was Vitest reading date-fns module by module. It does not change what the tests prove: the same library code, bundled; a duplicate React would fail every calendar test, and they pass. Its own commit, placed in Lane 0, is right.

## Outside my range (one line each, for the other reviewers)

- `docs/features/announcements.md` *Web history* at fcf46637 — R3's added line starts "2026-10-28, #129 —", unlike every other *Web history* line in the repository ("#NNN —"); a format nit (commit `fcf46637`).
- `docs/architecture/findings/169-…md:9` — R1-F3 above is mine; finding 180's own text (R3's) should agree with it once fixed.

## Checked and fine

- **The extension (seen in the code):** offered to the owner only (`owner` from the session's link at the space in the URL, `AnnouncementsPage`), on a `CLOSURE` not `UPCOMING` with `extension` null; reception reads «يمدّد المالك الاشتراكات بعد بدء الإغلاق.», the owner on an upcoming one «يمكن تمديد الاشتراكات بعد أن يبدأ الإغلاق.»; the server guards (403 worded, `['me']` read). The preview read at each opening (`refetchOnMount: 'always'`); its days, Gaza days and count shown as the server answers; `none` (S11) and `applied` with «رجوع» only. Days typed, Arabic digits read (`wholeNumberOf`), checked by `extendSubscriptionsSchema` (1–365) before sending, the typed days sent (not the proposal). One key per mount (`useIntentKey`, never `renew`d; the dialog keyed by its opening and unmounted on close), kept across the transport's re-sends, «إعادة المحاولة» and a double press (the submit `disabled` while `loading`); no answer → «لم يصل الرد. أعد المحاولة — لن تُمدَّد مرتين.»; `CLOSURE_ALREADY_EXTENDED`, `ANNOUNCEMENT_NOT_STARTED` (from `errors`), 403 worded; a 404/409 reads the space again; done → the toast from the server's answer (`done.subscriptions`, `done.days`), `settle`, and the card's «مُدّد {count} · {days} · {name} · {date}» from the list (Gaza day, name isolated). Close blocked while sending.
- **The post:** one key per opening (the list keys the sheet by a never-reset opening count), kept on lost answer, double press and an edit of the form; the edit a `PATCH` with no key; «الآن» → no `startsAt`, «بلا موعد» → no `endsAt`, a blank English text left out, a cleared one `textEn: null`; typed dates and times sent as `gazaInstant(date, minute)` (summer/winter tested under New York's zone); the calendar's day ↔ Gaza date mapping drift-free; date over time below 640 px (`grid sm:grid-cols-2`); first focus the checked type's radio; focus back to the opener while it is connected. The type and start of an extended closure are not locked in the sheet: the server's `CLOSURE_EXTENDED` is shown as the form's failure, as the plan designed (S4).
- **End / start / delete:** end on running only (with «تراجع» → `PATCH { endsAt: <the loaded end, null included> }`, not on an extended closure), start on upcoming only, «حذف…» in any state but an extended closure, whose card says why; each sent once without a key (the repository and the tests read the header); failures as error toasts with «إعادة المحاولة» (end/start) or inside the dialog (delete); the delete's title names type and period, its text by state.
- **S12:** every write (`create`, `edit`, `end`, `start`, `remove`, the undo, `extend`) invalidates `['space', spaceId]`, not awaited; that prefix holds `occupancy`'s `now` (the space's live status, the desk's top bar), the desk's file/statement/lists and `payments`'; the check-in's closure warning comes from the check-in's own answer (no cache). A 404 / 403 without a code also reads `['me']`.
- **The list:** tabs in the address (`?state=upcoming|ended`, running not written, a wrong value → running, `replace`, back to page 1), paging past one page only, `usePageInRange` for a page past the last, counts from the summary (skeletons while it loads), three skeleton cards, failure with reference and retry, refresh failure over the cards, empty per tab.
- **Finding 169:** `calendar.ts` entry; `LAYER_ENTRIES` gains it; `calendar` library chunk (react-day-picker, date-fns; `@date-fns/tz` left out, rightly); `check:build` refuses every `LIBRARY_CHUNKS` name in the first download and refuses a build missing the chunk; every importer moved (`LedgerFilters`, the showcase's three sections; `PeriodFields` imports the entry); foundation §3 (tree, public-surface rule) and architecture §3 (heavy libraries) true.
- **Finding 173:** `resetOnSelect` set for `mode === 'range'` only, spread before the caller's props; foundation §12's row and the finding's resolution true; the ledger unchanged.
- **Documents:** `announcements.md` (header, *Who uses it*, the four web *Behaviour* paragraphs, *Web decisions*, code map, *Web history*), `subscriptions.md` *Who uses it*, foundation §13 screen 18 («… extend the subscriptions it covered, by the days typed, once», as §14.8 approved), architecture §2, §3 (S2's line), §7 (S12's line), `overview.md`, findings 169/173 *Resolved* and the index — true to the code except R1-F3 and the "a failure stays in the dialog" sentence R1-F2 makes untrue for the 409s; one home per fact; `#129` where the number goes. The contract's #128 changes (the count with the renewals, `renewalIds`) are reflected in the copy and `announcements.md` (DI-20's line).
- Routes: `SPACE_PAGES.announcements` lazy, both roles; the routes test for each.

## Not checked, and why

- Nothing run (the review's rules): no test, build, `check:build` or browser; every "would fail" above rests on the code and on lane A's recorded breaks.
- The real run's `announcement.edited` audit body (whether it carries `startsAt`, R1-F1's evidence in data): no database or API reads allowed.
- R1-F2's exact focus landing (Radix `FocusScope` unmount ordering) — reasoned, not run; the dialog's unmount itself is certain from the code.
- LEAD-D3's guard against #127's exact case (a dashboard-only draw through the barrel): needs a build.
- The showcase sections' rendering and the files of R2's and R3's ranges beyond what my range's files share with them.
