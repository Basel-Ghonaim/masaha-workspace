# OWNER_SETUP — PR 2 report (`feat/owner-packages`, Packages & prices)

Executor: Claude Code (Opus 5.5), 2026-10-20. Written as the work goes.

## 1. First checks (plan §13, read for this PR)

1. `gh pr view 96 --json state` → `MERGED` (merge commit `c91f5b42`). `git status` clean on `main`;
   `git fetch origin`; `git pull --ff-only` → `Already up to date.` (`main` = `origin/main` = `c91f5b42`).
2. Base diff `git diff --name-status 9fae4e00 origin/main` → **empty** (only #96's merge since its head). No code
   file of this PR changed; `packages/shared` unchanged (no rebuild needed beyond the existing `dist`).
3. Open PRs: `gh pr list --state open` → `[]` (DESK has no open PR; nothing for the conflict check yet).
4. Check 5 — `toFieldErrors` (`packages/shared/src/core/fieldErrors.ts`): `invalid_type` gives `required` only when
   the value is `undefined`; a count sent as `''` gives **`invalid_format`**. As the plan's fallback says: the
   limits' `fieldLines` word `invalid_format` with `fieldErrors.limitEmpty` too (a departure, stated).
5. Check 6 — `Sheet side="end"` (`shared/design-system/components/overlays/Sheet/Sheet.tsx`): `w-3/4 max-w-sm` at
   every width — **not** full width below 768 px; `SheetBody` has no `min-w-0`. Built with it as it is; finding
   **101** recorded (no design-system change).
6. `packages/shared/src/packages` read against §9: `createPackageSchema`, `updatePackageSchema` (`.partial()`, with
   `isActive`), `SpacePackage`, `SUBSCRIPTION_BILLINGS`, `PACKAGE_NAME_MAX_LENGTH` 60, `MAX_DAYS_PER_WEEK` 7,
   `MAX_HOURS_PER_DAY` 24, `priceAgorot` 1…`PRICE_MAX_AGOROT` — as §9.
7. Finding numbers: the index ends at 99 (100 is worker B's) → this PR's first is **101**.
8. Branch: `git switch --no-track -c feat/owner-packages origin/main`.

## 2. Commits

### Carried from #96 (`0_CARRIED_FROM_96.md`, review `6_REVIEW_PR1_CLAUDE_CODE.md`) — three commits

Lint and typecheck on the three together, before committing: `npm run lint` (eslint, no output) → exit 0;
`npm run typecheck` (`tsc -b`) → exit 0. `npx prettier --check` on the changed code → `All matched files use
Prettier code style!`. `npx vitest run --project component src/features/spaces src/features/lookups` →
`Test Files  46 passed (46)` / `Tests  356 passed (356)`.

- **`e9d24369` `fix(lookups): count only linked retired amenities` (49)** — items 1 and 9.
  `useAmenityChecklist`: the count is `value ∩ linked` the catalogue no longer names; a toggle keeps only the
  ids offered or linked (both sources — item 9, the admin's side, is the same three lines, so no stop).
  `useAmenitiesSection`'s JSDoc and `spaces.md` *Behaviour* no longer say "so the checklist marks it";
  `lookups.md` *Behaviour* and *Web history*.
  - Red (two new tests, before the code): `Tests  2 failed | 7 passed (9)` —
    `AssertionError: expected 'One amenity no longer on the platform…' to be null` and
    `AssertionError: expected last "vi.fn()" call to have been called with [ [ 3, 1 ] ]`.
  - Green: `Tests  9 passed (9)`.
  - Break 1 (count from `value` again): `Tests  1 failed | 8 passed (9)`, `expected 'One amenity no longer on the
    platform…' to be null`; restored. Break 2 (toggle from `value`): `Tests  2 failed | 7 passed (9)`, `expected
    last "vi.fn()" call to have been called with [ [ 3, 1 ] ]`; restored.
- **`2a2e4149` `fix(spaces): refresh an owner's spaces on a 404` (47)** — items 5–8.
  - Item 8 confirmed before the code: `useMySpacesQuery` has no polling and nothing invalidates `['me']` on a
    refusal, so the switcher keeps the space until a focus refetch. `useSpaceAnswer.refused`: an owner's 404 also
    invalidates `scope.answered`. New test in `useSaveGroup.component.test.tsx` ("fetches the user’s spaces again
    when an owner’s write finds the space no longer theirs (404)"): red `Tests  1 failed | 1 passed (2)`,
    `AssertionError: expected [ { …(19) } ] to have a length of 2 but got 1`; green `Tests  2 passed (2)`; break
    (the 404 test never matching) → the same red; restored.
  - Item 5: `PricesLinkCard`'s dot is its own `<span aria-hidden>·</span>`. Assertion added to «shows the owner
    «الباقات والأسعار»…»: green `Tests  1 passed | 30 skipped (31)`; break (the old markup) →
    `TestingLibraryElementError: Unable to find an element with the text: ·`; restored.
  - Item 6: `pricesLink.missing` dropped; the test asserts «Not added yet» (title now "…with its date, stale or
    never added").
  - Item 7: the photo hooks' admin causes reworded; `useSpaceEditor`'s and `AmenitiesSection`'s JSDoc re-wrapped.
- **`cf019de1` `docs: bring the owner's profile docs up to date` (47)** — items 2–4: `architecture.md` §7 names
  the owner's `['me']` and the editor's lookups scope; `spaces.md` *Authority* ("…and its owner edits it", "the
  managed-space routes"); `lookups.md` *Scope* ("for the admin and the owner's profile"); `overview.md` ("its
  prices a link to Packages & prices, not built yet").
- Not carried as code: item 5 of the review (the demo passwords) is the owner's (the prompt's §1.9).

### Plan commit 6 — `6b1597d0` `feat(spaces): edit prices on packages & prices` (46)
- Built: `useSpacePricesEditor(place, spaceId)` (the space's states, `mayEdit`, its own leave guard naming
  «الأسعار المعلنة»), `SpacePricesEditor({ spaceId, hoursLink })` (exported; `ForbiddenState` for a place that may
  not edit, as the owner's editor); `PricesSection`/`usePricesSection` take `hoursLink: string | null` (required: the
  admin's editor passes `null`), `notes` become `{ text, link }[]`, the owner's frame titled `publishedTitle`, its
  intro `publishedIntro`; `pages/dashboard/space/PackagesPage.tsx`; `SPACE_PAGES.packages`; copy
  `spaces.editor.prices.{publishedTitle, publishedIntro, noShiftsLink}` ×2; `PricesSection`'s stale JSDoc ("from 768
  px") corrected to 1024. Docs: `spaces.md` *Behaviour* («The owner's prices on Packages & prices»), *Web decisions*
  (O6; design issue 8), code map, *Web history*; `architecture.md` *Built so far*; `overview.md`.
- **Departure:** `useSpaceShifts` moves to commit 7, where it is first used (no export without a caller).
- **Check 7 (`#hours` from another page):** React Router's `ScrollRestoration` (in `RootLayout`) scrolls to
  `location.hash` after the navigation renders. The link is drawn only on Packages & prices, once the space has
  loaded, under the same owner key (`['space', id, 'spaces', 'space']`) the profile's editor reads: the profile
  renders its sections from the cache on its first render, so `#hours` exists when the scroll runs. No effect
  added. (The real run's demo space has shifts, so the line is not drawn there — the plan's not-performed case.)
- Test 13 (`SpacePricesEditor.component.test.tsx`, new, written with its code): `Tests  3 passed (3)`.
  - Break (drop the guard: `useLeaveGuard([], …)`) → `Tests  1 failed | 2 passed (3)`,
    `TestingLibraryElementError: Unable to find role="alertdialog" and name "Leave with unsaved changes?"`; restored.
  - Break (omit the link) → `Tests  1 failed | 2 passed (3)`, `Unable to find role="link" and name "Add shifts in
    the opening hours"`; restored.
- Test 14's Packages case (`routes.component.test.tsx`, «the owner's packages and prices»): `Tests  1 passed | 41
  skipped (42)`; break (packages out of `SPACE_PAGES`) → `Tests  1 failed | 41 skipped (42)`, `Unable to find
  role="heading" and name "Published prices"`; restored.
- `usePricesSection`'s existing test follows the `notes` shape (titles unchanged).
- Checks: `npm run lint` → exit 0; `npm run typecheck` → exit 0; Prettier on the changed files → `All matched files
  use Prettier code style!` (after `--write` on the new test); `npm run check:links` → `2412 links in 185 documents
  and 1414 source files all resolve.`; `npm run check:classes` → `No physical direction or arbitrary-value classes
  in 954 files.`; `npx vitest run --project component src/features/spaces` → `Test Files  23 passed (23)` /
  `Tests  226 passed (226)`.

### Plan commit 7 — `e1240cf` `feat(packages): keep a space's private packages` (47)
- Built `features/packages` (dashboard-only, already in `DASHBOARD_ONLY_CAPABILITIES`): `PackagesRepository` (list,
  create, update at `/manage/spaces/:spaceId/packages`); keys `['space', id, 'packages']` and the rows' write key;
  `usePackagesQuery`, `usePackagesSection`, `useRowWrite` (the switch and «إزالة الوردية»: `setQueryData` from the
  answer, a toast that stays on a refusal), `usePackageSheet` and `useSavePackage`; `packageValues`
  (`valuesOf`, `packageInput`), `packageSummary` (`summaryOf`, `priceLineOf`, `shiftNameOf`); `PackagesSection`,
  `PackageRow`, `PackageSheet`, `LimitsField`, `ChipsField`, `toast/packageToasts`; types `ShiftChoice`,
  `PackageRowView`. `spaces` exports `useSpaceShifts` (moved here from commit 6). `PackagesPage` places the section
  under the prices. Copy `packages` ×2 (with the approval note's refusal lines). Docs: `packages.md` (header, *What it
  does*, *Who uses it*, *How it composes*, *Behaviour* «The owner's packages on the web», *Web decisions*, code map,
  open findings, *Web history*), `architecture.md` (*Built so far*; §7 the 422's `['space', id]`), `overview.md`,
  `docs/README.md`; finding 81 → Resolved (moved in the index); finding **101** recorded (Open).
- **Departures (shape, within the plan's lines):**
  - The edit is checked in the browser with `createPackageSchema`, not `updatePackageSchema`: the terms are sent whole
    (S11), and the update schema's `.partial()` would let a cleared required term (an empty validity) through as
    absent. The request is the same object; the PATCH takes it.
  - `useSetPackageActive` and `useClearPackageShift` are one hook, `useRowWrite` (the same PATCH, the same answer
    handling, the failure's title by the change); `useCreatePackage`/`useUpdatePackage` are one, `useSavePackage`.
  - The sheet's open state lives in `usePackagesSection`; `usePackageSheet` is the form, mounted only while the sheet is
    open (as `LookupSheet`'s forms), so each opening starts from the package as it stands.
  - `PackageValues` names the amount `priceAgorot` (text in shekels) — the field names must be the request's for a
    refusal to land on its field (as the prices' `amountAgorot`); `prepare` is `packageInput`, as `pricesInput`.
  - Check 5's fallback, made exact: an empty limit's `invalid_format` is worded «أدخل العدد أو أطفئ هذا الحد» only when
    the field is empty; a non-whole count typed there keeps «عدد صحيح من 1 فأكثر».
  - `fieldErrors.name.too_short` added (the same line as `required`): `textSchema(1, 60)` refuses an empty name as
    `too_short`, not `required`.
  - The rate lines isolate the amount (`… للساعة`), so its digits and sign never reorder the Arabic words.
  - Extra files beyond §7's list: `hooks/list/useRowWrite.ts`, `hooks/sheet/useSavePackage.ts`,
    `components/sheet/ChipsField.tsx`, `components/toast/packageToasts.tsx`.
  - «باقة جديدة» has no plus icon: the layer has none, and adding one is a design-system change.
  - The Arabic-Indic digit reading is a local helper, as `clockTime`, `shekels` and `coordinates` each keep theirs (no
    drive-by refactor).
- Tests (new code, each written with its code; red seen through its break):
  - 15 `packagesRepository.unit.test.ts`: `Tests  1 passed (1)`; break (the edit as `PUT`) → `Tests  1 failed (1)`,
    `AssertionError: expected [ …(3) ] to deeply equal [ …(3) ]`; restored.
  - 16 `packageSummary.unit.test.ts`: `Tests  2 passed (2)` (after correcting my own expectation: 30 takes the
    `many` form, «صالحة 30 يومًا», and comparing prices through `priceText`); break (`daysPerWeek` left out) →
    `Tests  1 failed | 1 passed (2)`, `expected 'صالحة 30 يومًا · 10 أيام · ساعة واحدة…' to be 'صالحة 30 يومًا · 10
    أيام · يومان بالأ…'`; restored.
  - 17 `packageValues.unit.test.ts`: `Tests  4 passed (4)`; break (an off limit sent as `undefined`) → `Tests  2 failed
    | 2 passed (4)`; restored.
  - 18 `usePackagesSection.component.test.tsx`: `Tests  5 passed (5)` (my own test's defect fixed first: a 500 on a
    GET is retried 1 s + 2 s by the transport, so the failure case uses a 404); breaks: `pending` removed from the
    switch → `Tests  1 failed | 4 passed (5)`, `AssertionError: expected false to be true`; `heldShift` offered for an
    active package → `Tests  1 failed | 4 passed (5)`, `AssertionError: expected { …(2) } to be null`; restored.
  - 19 `usePackageSheet.component.test.tsx`: `Tests  5 passed (5)`; breaks: a limit on and empty sent as `null` →
    `Tests  1 failed | 4 passed (5)`, `AssertionError: expected [ …(2) ] to deeply equal [ …(2) ]`; the `['space', id]`
    invalidation dropped → `Tests  1 failed | 4 passed (5)`, `AssertionError: expected false to be true`; restored.
  - 20 `PackagesSection.component.test.tsx` (axe clean): `Tests  3 passed (3)`; breaks: `availableNamed` dropped →
    `Tests  1 failed | 2 passed (3)`, `Unable to find role="switch" and name …`; the no-shift link omitted →
    `Tests  1 failed | 2 passed (3)`, `Unable to find an accessible element with the role "link" and name "Add shifts in
    the opening hours"`; restored.
  - Test 14's Packages case extended (the «Private packages» heading, `GET /manage/spaces/7/packages`): `Tests  1 passed
    | 41 skipped (42)`.
- A tool problem met: the file tool wrote the tests' `⁦-⁩` regex escapes as literal isolate characters;
  rewritten as escapes (via `chr(92)`), and every changed file scanned for invisible marks → none.
- Checks: `npm run lint` → exit 0 (after removing two unused names in test 17); `npm run typecheck` → exit 0;
  Prettier → `All matched files use Prettier code style!`; `npm run check:links` → `2424 links in 186 documents and
  1441 source files all resolve.`; `npm run check:classes` → `No physical direction or arbitrary-value classes in 981
  files.`; unit `src/features/packages src/shared/copy` → `Test Files  5 passed (5)` / `Tests  40 passed (40)`;
  component `src/features/packages` → `Test Files  3 passed (3)` / `Tests  13 passed (13)`.

## 3. On the head (`e1240cf3`) — STOPPED at the component lane (killed for memory)

- 14:55: `Get-CimInstance … app-b … vitest|tsc` → 0; free memory **5,031 MB of 15,680 MB**.
- `npm run test:unit` → exit 0: `Test Files  19 passed (19)` / `Tests  229 passed (229)`; `Test Files  49 passed (49)` /
  `Tests  772 passed (772)`; `Test Files  87 passed (87)` / `Tests  865 passed (865)`.
- 14:55:48: app-b vitest/tsc → 0; free memory **5,045 MB**. `npm run test:component -- --reporter=verbose` (output to
  the session scratchpad's `component-lane.txt`), in the background.
- **The lane was killed by Claude Code's memory guard** ("stopped because the system is running low on memory") before
  any test result: the output holds only `RUN  v5.0.2 C:/dev/masaha/app/apps/web` and a jsdom line `Not implemented:
  navigation to another Document` — no test file finished. As the prompt says (§3: a lane killed for memory → stop at
  once, no retry), **not run again**.
- 15:01: free memory 3,086 MB; the killed lane had left two `vitest` processes of `C:\dev\masaha\app` (mine — none of
  worker B's) running; stopped by PID → 0 left; free memory 3,756 MB.
- **Not run (stopped before them):** `test:component` on the head; the production build, `check:build`; on the head
  `check:classes`, `format:check`, `check:links` (each passed on commit 7's tree before the commit); the real run
  (scripts ready in `scripts\run1.mjs`–`run3.mjs`, no server started, no data changed); `#PRNUM`, the push, the PR, CI,
  the conflict check.
- **Where the work stands:** five commits on `feat/owner-packages`, local, not pushed; `git status` clean; ports 3320 and
  5320 not used by this run.
- **Noticed for the review (not changed):** on Packages & prices the prices' save toast says «حُفظ قسم «الأسعار»»
  while the card is titled «الأسعار المعلنة» (the toast's words come from `useSaveGroup`, by group).

## 4. The owner's answer — the component lane once more on the head (`e1240cf3`)
- 15:08: app-b vitest/tsc → 0, mine → 0; free memory **3,710 MB of 15,680 MB**. Run in the foreground this time (the
  memory guard reaps background shells while the session is idle).
- `npm run test:component -- --reporter=verbose` → exit 1, **`Test Files  1 failed | 176 passed (177)` / `Tests  1
  failed | 1175 passed (1176)`**, `Duration  371.11s`: only `routes.component.test.tsx` › «lists the owner’s eleven
  pages, the overview marked as the page shown» `3099ms`, `TestingLibraryElementError: Unable to find
  role="navigation" and name "Space dashboard"` — finding 87's known local miss (the prompt's §2 exception).
- The file alone (free memory 5,123 MB): `✓ … lists the owner’s eleven pages … 2019ms`, `Tests  42 passed (42)`,
  `Duration  20.21s`. Going on; CI's `test:component` judges.

## 5. On the head, the rest (`e1240cf3`)
- `NODE_ENV=production npm run build` → `✓ built in 1.67s`, exit 0; `npm run check:build` → `No showcase code in 40 build
  files (1033 strings checked).` / `No dashboard code in the site's first download.` / `No data-table or leaflet, nor
  Leaflet's stylesheet, in the site's first download.`; `npm run check:classes` → `No physical direction or
  arbitrary-value classes in 981 files.`; `npm run format:check` → `All matched files use Prettier code style!`;
  `npm run check:links` → `2424 links in 186 documents and 1441 source files all resolve.` Not run: `test:api` (no API or
  shared change; CI runs it).

## 6. The real run (head `e1240cf3`)
- **Browser:** local headless Chrome over CDP (no `playwright` MCP tools in this session). Scripts:
  `scripts\cdp.mjs`, `common.mjs` (PR 1's, shots to `pr2`), `probe.mjs`, `run1.mjs`–`run4.mjs`. Shots:
  `shots\pr2\` (35 PNG, 3 network logs).
- **Setup:** `docker start masaha-postgres-1`; `prisma migrate status` → `Database schema is up to date!`; API `/health`
  → `{"status":"ok","db":"up",…}`; web 5320 → 200. **The demo accounts accept `SEED_DEMO_PASSWORD`**
  (`probe.mjs`: `owner 200`, `reception 200`; no password printed).

| Case | Seen | Shots |
|---|---|---|
| The profile's prices row leads to the page | «الأسعار / تُعدَّل وتُؤكَّد في الباقات والأسعار / · / آخر تحديث قبل 377 يومًا / قديمة / الباقات والأسعار»; its link → `/dashboard/spaces/7/packages`, h1 «الباقات والأسعار» | `ar-light-1440-profile-prices-row`, `ar-light-1440-packages-page` |
| «الأسعار المعلنة» a table at 1440, cards at 768/390 | the header row `grid` at 1440 (ar, en), `none` at 768 and 390 (ar, en) | `{ar-light,en-dark}-{1440,768,390}-published-prices` (ar 1440: `…-published-prices-table`) |
| Saved, its leave guard, confirmed | an amount 5 → 6: «تغييرات غير محفوظة»; the sidebar's «الإعلانات» → «مغادرة الصفحة مع تغييرات غير محفوظة؟ / ستضيع التغييرات غير المحفوظة في الأسعار المعلنة. / البقاء / المغادرة», «البقاء» kept the page; saved → «حُفظ قسم «الأسعار»»; put back to 5 and saved; confirmed → ««الأسعار»: المعلومات ما زالت صحيحة», «آخر تحديث اليوم» | `ar-light-1440-published-prices-{unsaved,leave-guard,saved,confirmed}` |
| A package added: two limits, per day, students, a shift | «مسائي طلاب»: «عدد الأيام» `١٢` (Arabic digits), «ساعات باليوم» 5, «باليوم» 18.5, «الطلاب», «مسائي»; the summary «صالحة 30 يومًا · 12 يومًا · 5 ساعات باليوم · للطلاب · مسائي / 18.50 ₪ لليوم»; toast «حُفظت الباقة مسائي طلاب»; the row the same | `ar-light-1440-package-sheet-new`, `-package-added` |
| Edited | «تعديل الباقة»; validity 45 → the row «صالحة 45 يومًا · …» | `ar-light-1440-package-edited` |
| A repeated name refused | «اسم مستخدم لباقة أخرى، موقوفة أو متاحة» on the name (409) | `ar-light-1440-package-name-refused` |
| Paused by its switch | «موقوفة», muted; the switch named «مسائي طلاب: متاحة»; its held-shift line, as it kept «مسائي» | `ar-light-1440-package-paused` |
| «شهري صباحي» paused → its held shift → «إزالة الوردية» | «موقوفة وما زالت تحجز وردية «صباحي»؛ لا تُحذف الوردية قبل إزالتها منها.» with «إزالة الوردية»; cleared → the line gone, «صالحة 30 يومًا»; then put back (the sheet's «صباحي» chip, saved; the switch on) → «صالحة 30 يومًا · صباحي», offered | `ar-light-1440-package-held-shift`, `-package-shift-cleared` |
| The page and the sheet at each width | Arabic light 768/390, English dark 1440/768/390: the page, the packages, the sheet (three-quarter wide at 390 — finding 101); no horizontal scroll at any width | `{ar-light,en-dark}-{w}-{packages-page,private-packages,package-sheet}` |
| Reception refused | `/dashboard/spaces/7/packages` → «لا تملك صلاحية الوصول إلى هذه الصفحة / هذه الصفحة غير متاحة لحسابك.»; no «الباقات والأسعار» in its sidebar; 0 requests to `/packages` | `ar-light-1440-reception-packages-403` |
| Network log | **0** `/admin/` requests in every owner run (33, 16, 20 requests) | `ar-light-1440-network-log.txt`, `ar-light-network-log.txt`, `en-dark-network-log.txt` |

- Page errors: 0 in every run. Not performed, as the plan names (component tests prove them): a package's shift removed
  meanwhile (test 19), a space with no shift saved (tests 13, 20; the demo space has shifts).
- **Data left in `masaha_dev`:** the package «مسائي طلاب» (paused, its shift cleared — no delete exists); space 7's
  prices confirmed today (their date moved; their amounts as before); «شهري صباحي» as before (paused, cleared, re-set,
  offered again — four audit entries); the package audit entries for the run's writes.
- Servers and the CDP Chrome stopped by PID; `Get-NetTCPConnection -LocalPort 3320,5320 -State Listen` → none.

## 7. `#PRNUM`, the rebase, the push, the PR
- `git grep -n "#PRNUM" HEAD` → 15 lines; the next number → `gh api …issues… --jq '.[0].number'` → 97, so **98**.
  `git filter-branch … 's/#PRNUM/#98/g'` over `origin/main..HEAD`; `refs/original` removed; `git grep "#PRNUM" HEAD` → 0;
  the stat against `origin/main` the same before and after.
- `main` had moved: **#97 (`feat/auto-checkout`, worker B's) merged** (`abc28e73`). Its files shared with this PR:
  `docs/architecture/findings/README.md`, `docs/features/spaces.md`, `docs/project/overview.md` — no code file. `git
  merge-tree` → a conflict in the findings index, so rebased on `origin/main` (workflow §9): the one conflict, both
  lines kept in number order (100 worker B's, 101 this PR's); `spaces.md` and `overview.md` auto-merged. `packages/shared`
  changed on `main`: `npm run build -w @masaha/shared` → 0, `npx prisma generate` (apps/api) → 0. Then `npm run
  typecheck` and `npm run lint` → no error; `npm run check:links` → `2446 links in 187 documents and 1457 source files
  all resolve.`; `npm run format:check` → `All matched files use Prettier code style!`; unit `src/shared/copy
  src/features/packages` → `Test Files  5 passed (5)` / `Tests  40 passed (40)`.
- Commits now: `4c4e5468` fix(lookups): count only linked retired amenities (49) · `becb87d1` fix(spaces): refresh an
  owner's spaces on a 404 (47) · `46760271` docs: bring the owner's profile docs up to date (47) · `85696eb4`
  feat(spaces): edit prices on packages & prices (46) · `8c429ff4` feat(packages): keep a space's private packages (47).
- Pushed `feat/owner-packages`; **PR #98** https://github.com/Basel-Ghonaim/masaha/pull/98 (assignee me; `feat`,
  `area:web`, `area:docs`; title = commit 7's subject; the description says "Carried from #96"). The number matches.
- **CI on `8c429ff4`** (run 39421841777 `success`): lint, format:check, typecheck, test:unit, **test:component**,
  check:classes, check:links, build, test:api, CodeRabbit — all `pass`; `gh pr view 98 --json mergeStateStatus` →
  **`CLEAN`**. `git status --short` → empty.

## 8. Final report (`final-report`)
1. **PR #98** https://github.com/Basel-Ghonaim/masaha/pull/98 · head **`8c429ff4`** · CI green on that head (run
   39421841777) · **`CLEAN`**. Not merged.
2. **Commits:** the three carried (`4c4e5468`, `becb87d1`, `46760271`), then the plan's 6 (`85696eb4`) and 7
   (`8c429ff4`); subjects 49, 47, 47, 46, 47.
3. **Run:** per commit lint + typecheck; on the head `test:unit` (229 / 772 / 865 passed); `test:component` once killed
   by the memory guard (no result), once `1 failed | 1175 passed` (finding 87's local miss; the file alone 42/42, 2019
   ms) — CI's passed; build, `check:build`, `check:classes` (981), `format:check`, `check:links`; the real run (§6).
   **Not run:** `test:api` locally (no API change; CI passed it); E2E (end of project); a shift removed meanwhile and a
   space with no shift in a browser (tests 13, 19, 20).
4. **Breaks / red first:** carried items 1 (two breaks), 5, 8; plan tests 13 (2), 14's Packages case, 15, 16, 17, 18 (2),
   19 (2), 20 (2) — all seen red (§2).
5. **Problems and how solved:** long Bash heredocs would not parse (scripts written to files instead); the file tool
   turned `⁦-⁩` escapes into literal isolate characters (rewritten via `chr(92)`, every changed file scanned);
   my own test defects (30's plural form, the transport's retries of a 500, unused names); the killed component lane
   (left two of my `vitest` processes — stopped by PID; re-run in the foreground at the owner's word); `main` moving
   (#97) — rebased, one docs conflict.
6. **Unexpected, unsolved:** the routes test's finding-87 miss repeats locally (3099 ms) and passes alone and on CI. On
   Packages & prices the prices' save toast says «حُفظ قسم «الأسعار»» while the card is «الأسعار المعلنة». The demo space
   has a third shift «مسائية» left by #96's real run.
7. **Early conflict check:** `gh pr list --state open` → only #98 itself; no other open PR (DESK's #97 merged, conflict
   resolved by the rebase).
8. **Departures:** gathered in §1–§7 — the commit 7 shapes (the edit checked with `createPackageSchema`; `useRowWrite`,
   `useSavePackage`; the sheet's open state in the section; `priceAgorot` as the amount's field; `packageInput`; the
   empty-limit line by the field being empty; `name.too_short`; the isolated rate amount; four extra files; no plus
   icon; a local digit helper); `useSpaceShifts` in commit 7; finding 101 recorded; the component lane run in the
   foreground after the owner's answer; the rebase on #97.
