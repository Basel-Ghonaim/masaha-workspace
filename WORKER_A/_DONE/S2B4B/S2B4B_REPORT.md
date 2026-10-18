# S2b-4b — The admin's space editor: opening hours with shifts, and prices — REPORT

## 1. The pull request
- **#79** — `feat(spaces): the editor's hours and prices` — https://github.com/Basel-Ghonaim/masaha/pull/79
- Branch `feat/space-hours-prices`, head **`7782391f91285f4ab8fe199b3967dd1102b1808e`**.
- CI green on that head (build, check:classes, check:links, format:check, lint, typecheck, test:unit, test:component, test:api); GitHub `mergeStateStatus: CLEAN`.
- Labels `feat`, `area:web`, `area:docs`; assigned to the owner. Not merged.

## 2. The commits
1. `f88b1339` fix(lookups): show a space's own hidden area — finding 60: `useGovernoratesQuery({ enabled })`, `useAreaOptions` returns `kept`, `AreaSelect` draws it first; `areaSelect.hidden`; tests 50–52; `lookups.md`, `spaces.md` (Open findings), finding 60 resolved and moved in the index.
2. `340940cd` feat(spaces): the editor's opening hours — `clockTime`, `hoursForm`, `updateHours`, `useHoursSection`, `useReadOnlyHours`, `HoursSection`, `ReadOnlyHours`, `SectionCard`'s `action`, `ReadOnlyItem`'s label widened, editor wiring, `editor.hours` copy; tests 1–9, 16, 18 (hours), 19–35, 53–54; editor tests updated; `spaces.md`.
3. `7782391f` feat(spaces): the editor's prices — `pricesForm`, `priceText`, `updatePrices`, `usePricesSection`, `useReadOnlyPrices`, `PricesSection`, `ReadOnlyPrices`, `SECTIONS = FACT_GROUPS`, every checklist line a link, `hoursUnsaved`, `editor.prices` copy; tests 10–15, 17, 18 (prices), 36–49, 55; editor tests updated; `spaces.md`, `overview.md`, finding 67 (new) and the index.

`#PRNUM` replaced by `#79` in every commit's tree (filter-branch) just before the push; `git grep '#PRNUM'` empty. Lint and typecheck clean on each commit (`git rebase --exec`).

## 3. What was run
Lanes one at a time, after checking with `Get-CimInstance … vitest` that no other folder ran one (none did, each time):
- `test:unit`: 208 + 718 + 793 tests (three workspaces), all passed — on the final code.
- `test:component`: 934 tests in 142 files, all passed — on the final code (a first run failed once, §5).
- `NODE_ENV=production npm run build` and `check:build`: passed (no showcase; no dashboard code, data table or Leaflet in the first download).
- `lint`, `typecheck` (also per commit), `check:classes`, `format:check`, `check:links`: clean.
- Only documents changed after the lanes and the build (finding 67 and the PR number); `check:links` ran again after them.
- **Not run:** `test:api` — no API change (CI ran it: passed).
- **Real run:** API 3320, web 5320, headless Chrome over CDP at `localhost:5320`, the seeded admin. Every step of the plan's §14.6 was done (one changed, §8); the demo space `masaha-demo` exists in `masaha_dev`, so the verified read-only page was checked. 27 screenshots in `Downloads\s2b4b-shots\`. Servers and Chrome stopped by PID; ports 3320, 5320 and 9333 free.

## 4. Breaks made and tests seen failing first
Each break on a backup copy of the file, run in the test's own lane, then copied back (never `git checkout`); the script in the scratchpad (`brk.py`) asserted each break text was found once.
- 1 `clockOf(1440)` → `00:00` · 2 no Arabic-Indic mapping · 3 24:00 accepted as a start · 4 a blank as `0` — each failed its test.
- 5 Friday open · 6 days in shown order · 7 `id: null` for a new shift · 8 shifts compared sorted · 9 closed days in the helper — each failed.
- 10 no `× 100` · 11 rounded past two decimals · 12 always two decimals · 13 `shiftId: ''` sent · 14 prices compared sorted — each failed.
- 15 the Arabic locale `ar-PS` instead of `ar-u-nu-latn` (the owner's choice, §8) — failed.
- 16 path `/hour` · 17 prices sent as a bare array · 18 confirm path `/confirm/<group>` for hours, then for prices — each failed.
- 19–35 (hours hook), each failed: Sunday first; a missing group as unchanged; the shift's id dropped; no blur rewrite; a copy to every day (opening the closed ones); the copy never disabled; `shifts.<i>` dropped from `FIELDS`; no helper; the closing time's `fieldLines` dropped; prices read from `[]`; the 409's invalidation dropped; the 422's invalidation dropped; never unchanged; `MAX_SHIFTS + 1`; a reset on every new space; `'profile'` confirmed; `isPending` dropped from Remove.
- 36–48 (prices hook), each failed: the amount sent as typed; a missing group as unchanged; never unchanged; the shift field never disabled; `hoursUnsaved` ignored; `.shiftId` dropped from `FIELDS`; the amount's lines dropped; the Arabic label's `required` line dropped; the invalidation dropped; `MAX_PRICES + 1`; a reset on every new space; `'hours'` confirmed; `isPending` dropped from Remove.
- 49 `hoursUnsaved: false` — failed.
- 50 `kept` never set · 51 the admin's list always read (`enabled: true`) · 52 `kept` not drawn — each failed.
- Editor test updates: the checklist's hours, then prices, line without a link; hours, then prices, dropped from the navigation; `ReadOnlyHours`, then `ReadOnlyPrices`, left out — each failed.
- 53 a closed day's times drawn — failed only once both `opens` and `closes` were forced (the component draws them together; the first break, `opens` alone, passed, so it was widened).
- 54 the in-use reason not drawn · 55 the note drawn per row — each failed.
- Breaks 34 and 47 (the wrong group confirmed) failed every test of their file, not only their own: the hook test's space has no date for the other group, so the frame throws. Their own test fails as it should.

## 5. Problems met, and how each was solved
- **Radix select and `''`:** this Radix version reads a select's value `''` as no choice and shows its placeholder, so «بدون وردية» could not be the option `''`. The shift's select uses the option `none`, mapped to and from `''` in the hook; the form holds `''` as the plan says.
- **The React lint's "refs during render":** an object holding a `ref` passed as one prop was flagged; the price selects take their props spread, as the profile's area field does.
- **Toasts leaking between hook tests:** a toast from an earlier test made "Prices saved" found twice; both new hook test files dismiss the toasts after each test, as the amenities hook test does.
- **A hook test of commit 2 not updated:** `useSpaceEditor`'s checklist test still expected no link for the hours; fixed and folded into commit 2 (fixup + autosquash).
- **The full component lane failed once:** `pages/dashboard/routes.component.test.tsx` answers every other request, `/lookups` included, with `[]`; commit 1's `useAreaOptions` read `query.data.governorates.some(…)` and threw. It now reads `query.data?.governorates ?? []` once, as the code before it did; folded into commit 1; the lane then passed whole.
- **Docker Desktop was down** at the real run: started it, then `npm run db:up`.
- **Device emulation resets** when a CDP client disconnects: one shot came out dark (renamed `05-…-ar-dark`); every later script sets its viewport and theme.

## 6. Anything that behaved unexpectedly
- **The prices table at 768 px cuts the shift's words** («بدون و»): the twelve-column table is cramped between 768 px and about 900 px. Recorded as **finding 67** (in commit 3), not changed: a layout decision for the owner.
- **Plain `ar` gives Western digits on this engine** (Node 24, ICU 78.3, CLDR 48): the plan's break for test 15 could not fail; the owner chose `ar-PS` as the break (§8).
- **The plan's real-run step "a shift 20:00–23:30 fits Saturday only"** cannot hold after «نسخ إلى كل الأيام», which gives every open day 09:00–24:00; Sunday was set back to 18:00 to see the helper (§8).
- The space added in the real run, «مساحة الساعات» (id 39, `masaha_dev`), stays, with its hours, four prices and empty amenities and contacts. «الرمال» was hidden and shown again.
- The 409 reproduced on one page (a shift removed in the hours, a price for it saved alone, then the hours saved).
- The prototype still says «المدة»/«الفئة» for the price columns (D5); `docs/design/` was not touched.

## 7. Early conflict check
No other pull request is open (`gh pr list --state open` lists only #79): nothing to check.

## 8. Departures from the plan or the prompt
- **`ReadOnlyRows.tsx` changed** (not in §7's list): `ReadOnlyItem`'s `label` is `ReactNode`, so a shift named only in Arabic carries `lang="ar"` in English. Asked under §16; **the owner chose this.**
- **Test 15's break** is the locale `ar-PS`, not `ar` (plain `ar` already writes Western digits here). Asked under §16; **the owner chose this.**
- **Finding 67** added (§6 of the plan allows 67 for what is observed and not fixed).
- **Real run:** Sunday set back to 18:00 after the copy, so the shift's helper could show (see §6).
- **`useSpaceEditor.component.test.tsx`'s checklist test** was updated in both commits (§10 named only `SpaceEditor`'s); its title now says "each line a link to its section".
- **Finding 60's resolution line** follows the findings' own form, `**Resolution (2026-10-14, #79):** …`; the documents' *Last Updated* is 2026-10-14 (today); the decisions keep 2026-10-13, the date of the owner's approval.
- **`useAreaOptions`** reads the catalogue's governorates through `?? []` (§5), which the plan did not spell out.
- The remove button of a shift returns a `text` («حذف الوردية») beside its `label` («حذف الوردية {n}»), and the English label field a `placeholder`: the plan's design needs both strings, its type listed one.
- The h3 «الورديات» uses `text-label` (no `text-title-sm` exists; `AmenitiesSection`'s heading class), as the plan said to check.

---

## Review fixes (round 1, 2026-10-14)

From `REVIEW79_OPENCODE_REPORT.md`: no blockers, one should-fix, confirmed by the analyst.

1. **The pull request:** #79, head **`d611642abc25230e3f7c84bbe904674a49fea265`**; CI green on it (every lane), `CLEAN`. Not merged.
2. **The commit:** `d611642a` fix(spaces): refuse an amount past two decimals — a commit of its own on top (the owner's exception to folding), a plain push, no rebase.
   - `pricesForm.ts` › `agorotOf`: more than two decimals now hands back the text as typed (was `shekels * 100`, whole whenever the extra digits were zeros: `12.500` → ₪12.50, `1,000` → ₪1). The doc comment says so.
   - `pricesForm.unit.test.ts`: "hands back an amount past two decimals as typed, a thousands separator included" replaces "leaves an amount with more than two decimals as no whole number of agorot": `1,000`, `12.500`, `٣٫٠٠٠`, `12.555` returned as typed; `12.5`, `12,50`, `١٢٫٥` still 1,250.
   - `docs/features/spaces.md`: the amount's decision line said "more than two decimals is no whole number of agorot, which the contract refuses", no longer how it works; it now says an amount past two decimals is refused on its field, `12.500` and `1,000` too.
3. **Run:** the one test file (7 passed), `lint`, `typecheck`, `check:links` — locally. **Not run locally:** the full lanes (the owner: CI runs them on the push); CI passed every lane on `d611642a`.
4. **Seen failing first:** the new test, against the old branch — `expected 100 to be '1,000'`; green with the fix.
5. **Problems met:** a description edit's search text named the head as `7782391` where the description says `7782391f`; corrected and the edit made.
6. **Unexpected:** none.
7. **Early conflict check:** #80 (`design/desk`, «design: the front desk») opened meanwhile: `git merge-tree --write-tree` of `d611642a` and its head is clean.
8. **Departures:** the `spaces.md` decision line was edited with the fix, so the document stays true (the prompt named only the code and its test). The PR description was brought to the final state (head, the acceptance line on amounts, the break, the commit count); one "Review fixes" comment posted.
9. **Follow-up (the owner):** `2bccc7f2` fix(spaces): no separator in the amount's limit — «أكبر من صفر، حتى 100000 ₪» / "Above zero, up to ₪100000" (was 100,000, teaching the separator the field now refuses); its hook test updated. Run: `usePricesSection.component.test.tsx` (15 passed), `lint`, `typecheck`; CI passed every lane on `2bccc7f2`; `CLEAN`. The PR's description (head, the Arabic line) and the "Review fixes" comment updated. `priceText`'s read-only `₪100,000` (Intl's formatting of a saved price) is unchanged.
