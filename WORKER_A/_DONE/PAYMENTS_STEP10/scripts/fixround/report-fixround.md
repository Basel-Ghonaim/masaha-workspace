## The reviews' fix round (2026-10-28)

From `6_REVIEW_LEAD_R1_CLAUDE_CODE.md`, `…_R2_…`, `…_R3_…` and `7_FIX_ROUND_LEAD.md` (the owner: every finding fixed,
nothing carried; R3-F1 option (a) on DI-58). Done by the lead alone, no sub-agents; worker B ran on the machine.

### The base

- `git fetch origin`: `origin/main` `76661f7c` (unmoved); `gh pr view 129 --json mergeStateStatus` → `CLEAN` → **no
  rebase**. `backup/step10-pre-review-fix` at `fcf46637` before the first fold.

### Each fix (the red before the fix, the green after, the break; outputs in `scripts\fixround\`)

- **R1-F1 (blocker)** → `feat(announcements): post and edit an announcement`. `editRequestOf` decides "changed" at the
  sheet's precision: the typed Gaza date and minute against the loaded instant's `gazaClockOf` date and minute
  (`sameMinute`), start and end alike. Tests: `sheetRequest.unit.test.ts` (a loaded start `…T05:00:42.123Z` and end
  `…T15:00:07.900Z`: nothing changed → `{}`, only `textEn` → `{ textEn }`, the start or the end moved one minute → sent on
  the minute typed); `useAnnouncementSheet.component.test.tsx` («Save» untouched on a start posted «now» says «Nothing
  changed», sends nothing) with the fixture `announcementPostedNow()` in `src/test/announcement.ts`. **Red:** "× sends
  nothing for a start and an end the user did not move, though loaded with their seconds", "× sends a start or an end
  moved by one minute, on the minute typed" — "Tests 2 failed | 10 passed (12)"; the component "× says nothing changed
  for a start posted «now»…" — "Tests 1 failed | 8 passed (9)" (`r1f1-red-comp.txt`, `sheetRequest.ts` as at `fcf46637`).
  **Green:** 12/12 and 9/9. **Break:** the code as before (millisecond compare) — the same reds. `announcements.md`'s
  sheet paragraph says it.
- **R1-F2** → `feat(announcements): end, start or delete one` (the delete) and `feat(announcements): extend after a
  closure` (the extension). The opened delete and extension dialogs are **held by the list** (`AnnouncementsList`, as it
  holds the sheet: `CardDialog` = `{ kind, … }` with the card's key and the opener), the openers (`AnnouncementMenu`'s
  «حذف…», `ExtensionAction`) only open them; closed, the focus goes back to the opener while it is there, else to the
  card's first action, else the next card's or the tab (`useCardFocus.settle`, beside `leave`). Tests in
  `AnnouncementsList.component.test.tsx`: the extension answered `409 CLOSURE_ALREADY_EXTENDED`, the list read again with
  the closure extended → the dialog and its line stay until «Back», then the focus on a card's action or the tab; the
  delete answered `CLOSURE_EXTENDED` likewise. **Red** (the six files as at HEAD, `CardDialog.ts` removed): both "Unable
  to find an accessible element with the role "alertdialog"" — "Tests 2 failed | 6 passed (8)". **Green:** 8/8; the
  feature's 12 files / 63 tests. **Break:** the focus not placed once the opener is gone → both red ("expected <body …>
  not to be <body …>"). Split over its two homes (the delete-only state built from saved copies, checked — typecheck 0,
  63 tests — and folded first, then the extension); the tree after the fold identical to the pre-fold backup.
- **R1-F3** → `feat(announcements): post and edit an announcement`. Finding 169's resolution: "…which only the ledger's
  filters, the announcement sheet's period and the showcase import"; finding 180 already named the sheet's date fields.
- **R1-F4** → the same commit. `PeriodFields` passes `today={dayOf(gazaClockOf(new Date()).date)}`. Test in
  `AnnouncementSheet.component.test.tsx` at 22:30 UTC on 21 October (Gaza's 22nd): the calendar's `aria-current="date"`
  day is `2026-10-22`. **Red under `TZ=UTC`** (CI's zone): "× marks Gaza’s today in its calendar, not the browser’s" —
  "Tests 1 failed | 2 passed (3)". **Green** under UTC, New York and Gaza's zone. On this machine (Gaza's zone) the
  test cannot fail without the fix — its red was seen under `TZ=UTC`, which CI runs (F2's lesson, recorded).
- **R1's outside line** → `feat(announcements): show a space's announcements`: its *Web history* line starts "#129 —".
- **R2-F1** → `feat(data-reports): list every space's reports`: *Open findings* lists 167 (the reviewer's line) — by
  the document pass, below.
- **R2-F2** → `feat(data-reports): decide a space's reports` (the owner's, the sheet) and `…list every space's reports`
  (the admin's). While the opened report is gone from the page shown (decided elsewhere, under «جديدة»), the list's hook
  reads page 1 of the same scope's «الكل» (the chip's own query, key and cache; the admin's with its space and field)
  and the sheet takes the report from it — its status and its decision; and once `REPORT_ALREADY_DECIDED` says it is
  decided, the sheet never draws a stale «جديد»: «تمت المراجعة» (`dataReports.chips.decided`) until it is read. Tests in
  `SpaceReportsList.component.test.tsx` under `?status=open` (409, then the page without the row: with «الكل» holding it
  → «Not accepted» and its reply, no «New»; with «الكل» not holding it → «Reviewed», no «New») and
  `AdminReportsList.component.test.tsx` (the admin's). **Red:** "Unable to find an element with the text: Not accepted"
  / "…: Reviewed" — "Tests 2 failed | 4 passed (6)"; the admin's "…: Corrected" — "Tests 1 failed | 3 passed (4)".
  **Green:** the feature's 11 files / 54 tests. **Breaks:** the «الكل» read disabled → the first red; the stale guard
  dropped → the second red; the admin's read disabled → its red.
- **R2-F3** → `…list every space's reports`. `FilterTags` keeps the focus: a tag removed hands it to the button now at
  its place (the next tag's, else «مسح الفلاتر»), «مسح الفلاتر» or the last tag gone to the count (`onEmptied`). Tests:
  remove the first of two tags → the second's button; remove the second → «Clear filters», then «Clear filters» → the
  count. **Red:** both `toHaveFocus` — "Tests 2 failed | 4 passed (6)". **Green** twice. **Break:** the keeper never
  acting → both red.
- **R2-F4** → `…list every space's reports`: **finding 184** recorded ("A report's «تعديل الحقل» may not scroll to its
  section"; Plausible — not run in a browser), linked from `data-reports.md`'s *Open findings* and the index.
- **R3-F1** → `feat(favorites): list a user's favourite spaces`. «إزالة» of a space that left says «أُزيلت {name} من
  المفضّلة. لا يمكن حفظها من جديد ما دامت خارج الدليل.» / "{name} removed from favourites. It can’t be saved again
  while it’s out of the directory." (`favorites.removedLeft`, both catalogues), with **no «تراجع»** (`writeFavorite`'s
  `say: 'left'`, `useFavoriteToggle`'s `say`). Test 81's undo case is now "no «Undo»" (one `DELETE`, no button in the
  toast). **Red:** the toast's line not found — "Tests 1 failed (1)". **Green:** 5 files / 17 tests. **Break:** the
  undo restored (`say: 'undoable'`) → red. `favorites.md` and `directory.md` corrected; **finding 187** recorded ("A
  favourite just removed cannot be saved again for an undo"), linked from `favorites.md` and the index.
- **R3-F2** → `feat(data-reports): report wrong information` (the report, the shared signal, the shell) and
  `feat(favorites): save a space from its card` (the favourite). Each held intent lets itself go after 15 minutes
  (`HOLD_MS`, a timer), and when a guest lands on another page of the site: the site's shell reports each page it shows
  (`useGuestIntents` → `@shared/routing`'s `noteSitePage`), and each intent registers to let go (`onGuestLeaving`). The
  sign-in and register pages are outside the site's shell, so the round trip through them keeps the intent. S14 kept:
  memory only. Tests: the intents' unit tests (held 15 minutes less a millisecond kept, 15 minutes let go); the space
  page's "a guest who leaves for another page" — the held favourite not saved by a later sign-in, the held report's
  dialog not opened on the return signed in. **Red:** unit "expected undefined to be 900000" (`HOLD_MS` absent); the
  page's "expected [ { …(19) } ] to have a length of +0 but got 1" and "Unable to find role="heading" and name "Noor
  Hub"" (the dialog opened over it) — "Tests 2 failed | 7 passed (9)". **Green:** 9/9 and 7/7. **Break:** the shell not
  reporting its pages → both page tests red.
- **R3-F3** → `feat(favorites): save a space from its card`. The heart keeps one name, «حفظ {name} في المفضّلة», with
  `aria-pressed` (the WAI-ARIA toggle). Tests 77 and the toggle's updated. **Red:** "× keeps its one name and is
  pressed…", the toggle's label — "Tests 2 failed | 6 passed (8)". **Green:** 12 files / 74 tests. **Break:** its red
  (the changing name). `favorites.md`'s heart paragraph says it, a departure from §9's two names.
- **R3-F4** → `feat(data-reports): report wrong information`: `overview.md` names the report from a space's page.
