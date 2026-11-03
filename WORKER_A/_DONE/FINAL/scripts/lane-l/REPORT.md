# Lane L — the sub-agent's report (returned as text; saved by the lead)

Lane L · DONE
Branch lane/l head 19785eb8 (base 37a84e65)

Commits: ce04670d feat(design-system): add a meter (32) · a1137525 feat(design-system): draw bar charts and a heatmap
(50) · 21ef6d8a feat(design-system): reach a held menu item (43) · cda8bfbd feat(design-system): size a large input
(39) · 309ee6ae feat(lists): show a list's range and its steps (46) · e32170e2 feat(lists): mark the page asked while
it loads (47) · 6c9e9985 fix(lists): keep the scroll on a page change (44) · 7503db0f refactor(lib): read
Arabic-Indic digits once (44) · f59ba8c7 refactor(lists): share the row menus' triggers (46) · 3b3c4eaa feat(lib):
build a CSV and a WhatsApp link (42) · 19785eb8 docs: record finding 204 (24). No `fixup!` left; no attribution.
Fixes folded into C3.1–C3.3 (first lint run) and C3.5 (MyReportsList), C3.5's message reworded.

Red/green (each new test red before its code; notes `scripts\lane-l\notes.md`):
- C3.1 Meter: "Failed to resolve import ." → 1 file, 4 passed.
- C3.2 BarChart, Heatmap: "Failed to resolve import "."…" → 2 files, 7 passed.
- C3.3 × "is reached by the arrow keys and typeahead, its reason read" (React: non-boolean attribute `held`), × "does
  nothing when selected" (vi.fn called 1 times) → 11 passed.
- C3.4 × "is the large control at size lg…" (toHaveClass h-(--control-height-lg)) → 7 passed.
- C3.5 rangeSummary "Cannot find module"; paginationView × "keeps a one-page list its steps…"; ListPagination × "keeps
  a one-page list its steps, both disabled" → unit 9, component 2 passed.
- C3.6 × "marks the page asked current at once…" (aria-current); DataTable × "keeps its rows, dimmed and busy…" at
  1280 and 360; Refreshing unresolved import → 3 files, 19 passed.
- C3.7 × "keeps the scroll where it is when Page 2 / Next is followed" (scrollTo called once) → 6 passed.
- C3.8 westernDigits "Cannot find module"; extended-digit cases red in the five helpers → 13 files, 57 passed.
- C3.9 useRowTriggers "Failed to resolve import" → 2 passed.
- C3.10 csvOf, whatsappLink, downloadFile not found; fillReminder ×2 "not a function" → web lib 34, downloadFile 1,
  shared space-settings 8 passed.

Breaks (backup copy, restored by copy; `scripts\lane-l\break-*.txt`): B80 (role missing) 4 failed incl. axe · B81 ×
progressbar · B82 × hidden table second series · B83 × legend only for >1 series · B84 × every cell · B85 (`disabled`
instead of `held`) × reach (toHaveFocus) · B85c × skipping a disabled item (aria-disabled) · B86 × does nothing ·
B87 × size lg · B88 'Showing 0–20' ≠ '1–20' · B89 × one-page steps · B89b × onlyPastOne · B90 × page asked current ·
B91 × Refreshing busy · B91b × DataTable busy at both widths · B92 '۰۱۲…' ≠ '012…' · B93 × trigger focus back · B94 ×
quotes doubled · B95 × Page 2 · B95b × Next · B79 × wa.me/+970 · Bfill × every placeholder · Bfill2 '$1 $1' ≠
'{المبلغ} $1'.

Heavy checks (grant log): lint 0 (15:36:40 UTC, before the last two folds); typecheck 0 (15:41:19); test:unit web 162
files / 1089 tests 0 (15:25:19); test:unit shared 27 / 273 0 (15:25:27); test:component whole: 3 files failed | 304
passed, 7 failed | 1758 passed | 6 skipped (15:37:23) — 2 its own (MyReportsList counted list items; scoped to cards,
folded into C3.5), 5 finding 87's family (dashboard routes' beforeAll "Hook timed out in 10000ms", 3 guards tests,
the lookups tab; site routes' space page). Re-run through the grant 15:42:39: dashboard routes, site routes,
data-reports — 2 failed | 129 passed (site routes, body empty — finding 87); site routes alone 13/13. check:classes
(1686 files) and check:links (3120 links) green. The last two folds touched only MyReportsList's test (eslint alone
clean).

Shared files touched: design-system `index.ts` (exports), `tokens/semantic.css` (`--control-height-lg` 48/52,
`--chart-height-md/sm` 200/120, `--heatmap-step-1…5`, `--refreshing` 0.6); foundation §4 token rows and §12 rows
(Meter, BarChart, Heatmap, Refreshing, DropdownMenu `held`, Input `size="lg"`, DataTable `refreshing`); architecture
§1's `shared/` zone row; copy `forms.ts` `listRange`; `reminderTemplate.ts` (`fillReminder`, `ReminderValues`);
`space-settings.md` (code map Shared line, one Web history line); `space-links.md` (staff code map); the showcase
(`fixtures.json`, `registry.tsx`, Meter/Charts/Refreshing sections, Input's lg); `useAnnouncementsList.ts`
(`onlyPastOne: true`); `StaffList.tsx`, `UsersPage.tsx` (imports only); tests updated in AdminSpacesList,
useAdminSpacesList, useDirectoryList, MyReportsList.

Findings closed: 103 (C3.8), 104 (C3.9), 132 (C3.6) — status `Resolved · Date: 2026-10-21 · Resolved: 2026-10-29`
with *Resolution (#PRNUM)*. 73, 105 left Open (W1/W2 close them). Recorded: **204** (a CSV built in the browser keeps
a value that reads as a formula), its own commit. Index untouched.

Decisions (none SERIOUS):
- LL-D1 lint/typecheck per commit replaced by `npx eslint` on touched files + tests/prettier/checks, full
  lint+typecheck through the grant mid-lane (8 errors folded into C3.1–C3.3) and at the end. Why: memory waits.
  Undo: per-commit full runs.
- LL-D2 a one-page list keeps its steps everywhere (D3.5), announcements opting out (`onlyPastOne`, DI-26); four
  consumer tests rewritten, three item-counting tests scoped to cards.
- LL-D3 `rangeSummary(meta, { range })`, range and total isolated; DataTable shows `summary` only in table mode
  (≥ 768, existing behaviour).
- LL-D4 ListPagination finds the page asked by comparing the address's search with each link's search.
- LL-D5 chart sizes per plan (200/120); Heatmap step `floor(v/max·5)`; legend `aria-hidden`; one showcase file, two
  registry entries.
- LL-D6 Input `size="lg"`; native `size` dropped from InputProps; value text stays body.
- LL-D7 `fillReminder` in one pass (a value holding a placeholder or `$` goes in literally); T130 is U5's.
- LL-D8 downloadFile's test in the component lane (jsdom `Blob.text()` drops the BOM; bytes checked).
- LL-D9 formula values not neutralised (would depart from D3.9) → finding 204 for the owner.
- LL-D10 own defect in C3.3 (`aria-disabled={undefined}` wiped Radix's on disabled items) fixed inside C3.3.

Left out: none in scope. No consumer passes `refreshing`, `summary`, or `held` yet (U5, U6, U8, U9).

Notes for the lead: W1/W3/W4 can use Meter, BarChart, Heatmap, Refreshing, `held`, Input lg, DataTable
`refreshing`, `rangeSummary`, `useRowTriggers`, `toWesternDigits`, `csvOf`, `downloadFile`, `whatsappLink`,
`fillReminder` (rebuild shared after the join). `#PRNUM` in findings 103, 104, 132, 204 and `space-settings.md`.
Join conflict risk: foundation §4/§12, showcase fixtures/registry, architecture §1, space-links.md, space-settings.md,
useAnnouncementsList.ts. Any new list test counting listitems now also counts a one-page list's steps.
