# DIRECTORY_PROD — report

> Executor: Claude Code, Opus 5.5 · 2026-11-08 · on `40cb481d` (`origin/main`, unchanged through the item)

## 1. The pull request and its head

- **PR #139**, `feat(directory): filter by the hours, price and order`: https://github.com/Basel-Ghonaim/masaha/pull/139
  - Assigned to the owner.
  - Labels: `feat`, `area:web`, `area:api`, `area:docs`, `area:design-system`.
- **Head:** `e1838447d6d113b3f48f043d8654a933748620cc`.
- **CI:** run 42486266509 on that head, `success`. All ten checks passed: build, `check:classes`, `check:conflicts`, `check:links`, `format:check`, lint, `test:api` (6 m 2 s), `test:component` (6 m 42 s, 342 files / 2,084 tests), `test:unit`, typecheck. CodeRabbit skipped.
- **GitHub:** `CLEAN`.
- **Size:** **107 files**, +3,332 / −684. A separate review conversation follows; the owner has prepared it.

## 2. The commits

1. `f391bdfc fix(web): wait for the directory's own search` — finding 214 (the test, `warm` with 60 s, the finding and its index line) and #136's two nits in `ListPagination`.
2. `d735c69c feat(design-system): add the segmented control` — `SegmentedControl`, its test, the layer's export, the showcase section, foundation §3 and §12.
3. `dbc543cc feat(directory): filter by the hours` — items 7–12 without the price:
   - `openNow`, `evening`, `hoursStatus` (shared, API, web);
   - the panel's «الدوام»/«أخرى»;
   - Home on `openNow`;
   - «ساعات العمل غير متوفرة»;
   - ADR 0008, the data model, the contract, conventions, `directory`/`occupancy`/`announcements`/`space-links`, the overview.
4. `d93fc646 feat(directory): price by subscription and order` — items 3–6:
   - the price orders, `priceAgorot`, `GET /price-ranges`;
   - the subscription on `SegmentedControl`, the range with its hints, the sort's price items, the card's price;
   - the contract, `directory.md`, `spaces.md`, foundation §13.
5. `e1838447 feat(directory): page by 18 and fit the panel` — items 13–14:
   - the 4/12 column, the sheet's plurals, 18 a page;
   - the prototype's paging and `CHANGES.md` R9;
   - finding 215 (OD7 b).

Each commit has a body and no attribution. Two fixups were folded into their commits before the push (autosquash on the merge base; the tree was identical before and after):
- finding 215, into commit 5;
- one sentence of `directory.md` that read as a roadmap note, into commit 3.

`#PRNUM` was replaced by `#139` in every commit's tree (`filter-branch`). A word diff showed only those 54 replacements, and none is left.

## 3. What was run, and what was not

All local, on the head unless said.

| Command | Result |
|---|---|
| `npm run typecheck` | clean on **each of the five commits**, one at a time, back on the branch after each, and on the head |
| `npm run lint` | clean on the head; per commit **not run** (below) |
| `npm run format:check` | clean for the repository; it flags only `.claude/launch.json`, the owner's local file, which `.git/info/exclude` hides and CI never sees |
| `npm run check:classes` | no physical-direction or arbitrary-value classes in 1,930 files |
| `npm run check:links` | 3,259 links in 253 documents and 2,623 source files resolve |
| `npm run check:conflicts` | no markers |
| `NODE_ENV=production npm run build` + `npm run check:build` | built; no showcase code in 76 files; no dashboard code, and no data-table, Leaflet or calendar code, in the site's first download (EC17) |
| `npm run test:unit` (full) | shared 28 files / 304 tests · API 77 / 921 · web 188 / 1,198 — all pass (53 s) |
| `npm run test:api` (full, `masaha_test`) | 125 files / 1,427 tests — all pass (12 m 4 s) |
| `npm run test:component` (full) ×3, one at a time | 342 / 2,084 each run, all pass: 7 m 01 s, 6 m 46 s, 6 m 45 s. No lane killed |
| Real run (GET only, `masaha_dev`) | below |
| Screenshots | 34 in `C:\Users\basel\Downloads\directory-prod-shots\`, never pushed |

**The real run.** The API dev server ran on 3320 against `masaha_dev`; `prisma migrate status` was up to date and nothing was seeded.
- `/spaces`: 37 listed.
  - `openNow=true`: 34, and their ids equal the cards that say `OPEN`.
  - `evening=true`: 20.
  - `period=MONTH`: 19, each card with `priceAgorot`.
  - `period=DAY`: 35, including Daraj Corner (no hours) and Beit Lahia Desk (unverified, `CLOSED` by its hours).
  - `priceAsc`/`priceDesc`: correct orders; the price ties end by id.
  - `?availableNow=true`: 37 (unfiltered).
  - `sort=priceAsc` without a period: 422 `{ sort: ['invalid_choice'] }`.
- `/price-ranges`: `public, max-age=30`, with HOUR 300–600, DAY 1000–3000, WEEK 8000–15000, MONTH 16000–50000.
- `/map/spaces?openNow=true`: the same ids as the list.
- `/spaces/pal-hub/occupancy`: `{"status":"AVAILABLE","hoursStatus":"OPEN"}`.
- The web dev server ran on 5320 for the shots.
- Both servers were stopped. `TaskStop` left `tsx watch`, the server, `pino-pretty` and Vite running, so I stopped them by PID; ports 3320 and 5320 were then free.

**The screenshots.** RTL/LTR × light/dark at 1440 and 390 for:
- the panel with «شهر» and its range (placeholders 160/500);
- «الكل» with its hint;
- the phone sheet («عرض 29 نتيجة»);
- the unverified by-hours cards;
- the hours group checked, the open sort's price items, a space without hours (its card and its page), an unverified page's neutral «مغلقة الآن» with its line, and Home's «مفتوحة الآن».

Plus 1024, 1100 and 1300 in both languages, for the 4/12 column and the segments fitting (V7).

**Not run**
- **Per-commit lint.** The first per-commit check (lint and typecheck together) was stopped by Claude Code for low memory. The owner then asked for typecheck only, per commit; lint passed on the head and in CI. The PR says so.
- **E2E**, which is run at the end of the project.

## 4. Breaks made, and tests seen failing first

Every new test failed before its code, or was proven by breaking that code once and restoring it from a backup (a script restored each file in a `finally`).

**Finding 214 (T80)**
- Fails when Home's pick goes to `/spaces`.
- Fails when the Directory draws no «Workspaces» h1.

**`SegmentedControl` (T50)**
- First red because the component did not exist.
- Home/End fail with Radix alone (EC1).
- `dir="ltr"` forced on the root fails the RTL keys.
- A second tab stop fails the tab-stop test.

**Shared (T1–T8)**
- New tests red before the schema: `openNow`/`evening` (5 tests).
- Breaks:
  - a price order needs no period (fails `priceDesc`);
  - a period required only with both bounds (4 fail);
  - `>=` for `>` (2 fail).

**API, the hours (T20–T34)**
- `<` at the opening (3 fail);
- `<=` at the close;
- closures ignored (2);
- `endsAt >= now`;
- deleted closures counted;
- the override not excluded (OD2 b);
- the UTC weekday and minute (4);
- a fixed +2 offset (the DST test);
- `evening` with `>`;
- `evening` read for today only;
- `evening` ignored (10, through the leave-one-out);
- `openFriday` OR-ed with verified (9).

**API, binding and states (T30, T31, T35)**
- The TypeScript rule drifting to `<=` (3, the binding test included).
- The state ignoring the closure (6).
- The occupancy read dropping `hoursStatus` (3).
- `hoursStatusOf` checking the closure before the week fails T37 (unit).

**API, the price (T10–T19)**
- `max()` for `min()`;
- the audience dropped (2);
- `>`/`<` at each bound (2 each);
- the hidden-price rule dropped (2);
- `id DESC` in `priceDesc` (2);
- no tie-break (3);
- the order ignoring the price (3);
- `null` sent in place of an absent `priceAgorot` (4);
- the ranges' hidden rule dropped;
- the ranges' audience dropped.

**Web, unit**
- The old `available` read as open;
- the by-hours badge in `success`;
- a verified card reading the hours;
- no hours drawn as nothing (2);
- a price order kept without its period (2);
- the period sent only with a bound;
- the placeholder rounded up;
- price orders offered under «الكل»;
- the card's price without a period.

**Web, component**
- The count drops `evening`;
- the hours group's order swapped;
- the page's by-hours badge in `success`;
- the address writing `available` (2);
- `evening` not sent;
- Home asking `availableNow` (2);
- Home linking `?available=1`;
- the count reading the bounds (2);
- the price missing from the card's description;
- the subscription not described by its line;
- «الكل» keeping a refused text;
- 20 a page (3);
- the Arabic `two` form (2);
- the `many` form.

**Breaks that did not fail, and what was done**
- *A closure's `ENDED` state with `lt`.* That state is not the closure rule (the rule uses `RUNNING`), so the break was mistargeted and the result was expected.
- *`priceAgorot: x ?? undefined`.* A no-op, because JSON drops `undefined`. Redone as `null` sent where the key should be absent; it failed 4 tests.
- *«الكل» without `setTexts`.* It passed, because the test only had a valid bound, which the address sync clears anyway. I rewrote the test to type an invalid text only; the break now fails it.
- *«الكل» without `min`/`max: undefined`.* It passed, because the address writes no bound without a period, so the code was redundant. I removed it (`apply({ period: undefined })`).

## 5. Problems met, and how each was solved

- **A hung shell.** My command opened `cat > file` with no input. I stopped it; nothing had changed.
- **Heredoc parse failures.** Long Python heredocs failed in Git Bash. I wrote the scripts to the scratchpad instead, as the memory says.
- **422 in the new API tests.** I used `limit=100`, above `MAX_PAGE_SIZE` (50); changed to 50.
- **The leave-one-out test (T33).** Two problems:
  - unverified candidates had `prices_updated_at` null, so their prices were hidden; I dated them now;
  - at a Friday clock, «Friday closed» also failed `openNow`; I moved the clock to Thursday so each space fails exactly one filter.
- **A unique price constraint.** Two general DAY prices with no shift and no label conflict; the second now carries a label, as the space's own rows do.
- **Web fakes counting `/price-ranges`.** The new read broke tests that count every request or answer by call index. Four test files now answer `/price-ranges` apart and count only their own requests; what each test proves is unchanged.
- **Arabic test names crashed the break script's print** (cp1252). Fixed with `PYTHONIOENCODING=utf-8`; the files were restored by the `finally`.
- **The per-commit lint and typecheck loop was stopped for low memory.**
  - It left the repository detached at commit 1; I put it back on the branch, with no file changed.
  - It left an orphan ESLint (2.9 GB). My attempt to stop it was refused by the permission check, so I stopped and asked.
  - The owner confirmed the processes were gone and asked for typecheck only, per commit, which passed on all five.
- **#138 was taken** by the parallel space-profile PR before the push, so this PR is #139.

## 6. Anything that behaved unexpectedly

- **EC5: `1e3` is accepted** as a price bound (1000 agorot), because `z.coerce.number()` reads scientific notation. It is existing behaviour and the web never sends it. Recorded here, not changed; T4 tests the codes seen (`0`, `-100`, `10000001` → `out_of_range`; `12.5`, `abc` → `invalid_format`).
- **`NOT h.is_closed` in the `openNow` predicate is redundant.** A closed day's minutes are null, so the comparisons fail anyway, and the plan's T21 break ("the closed flag ignored") cannot fail. T21 still proves a closed day fails. The predicate stays, as in `evening` and `openFriday`.
- **`TaskStop` on a backgrounded dev server leaves its children** (`tsx watch`, the server, `pino-pretty`, Vite), as the memory says. Stopped by PID.
- **Some remaining matches of `availableNow` or «متاحة الآن» are left on purpose** (EC11):
  - `docs/plans/v1-mvp.md`: a dated "Built" log of the earlier step;
  - `docs/frontend/localisation.md`: an example of a copy key's spelling;
  - foundation §5: "Available now" as an example of the success role, still the live status's;
  - the contact's «متاحة الآن» ("available") in the directory's catalogue, and the Checkbox showcase and test samples.

  Each is history, an example, or true.

## 7. Early conflict check

| Open PR | Head | Result |
|---|---|---|
| #138 `design/space-profile` | `54139379` | **conflict in `docs/design/CHANGES.md`** only: both append rows at the end. Documents only, so the fast path (keep both, `format:check`, one push) applies to whichever merges second |

## 8. Departures from the prompt and the plan

- **The PR number is #139, not #138.** #138 was opened by the parallel task before the push (EC10).
- **Per-commit lint was not run**, by the owner's instruction after the memory stop; lint passed on the head and in CI.
- **The PR title** is `feat(directory): filter by the hours, price and order`. The workflow asks for the main commit's subject, but the item has three equal main commits, so the title names all three.
- **Two price tests in `list.api.test.ts` were removed** (the period within the bounds; the stale unverified space). `price.api.test.ts` proves both fully (T10, T11, T14), so keeping them would prove one behaviour twice (testing §1).
- **Test placement.** The plan's T10–T18 live in a new `price.api.test.ts`, not in `filters.api.test.ts`, which holds the hours (T20–T29, T32, T33). The binding and the states (T30, T31) live in `hours.api.test.ts`, as planned.
- **`SegmentedControl`'s chosen segment uses `text-card-foreground` on `bg-card`** (the verified "-foreground on its surface" pair, EC2) rather than the plan's `text-foreground`.
- **Its label in the price filter is `aria-label`, not a visible Field label.** The group's heading «السعر» is visible, as in the prototype. The hint and the help line describe it through `aria-describedby`, rendered after the range, which keeps the prototype's order (DI-7).
- **`todayHours` now always returns a string** («ساعات العمل غير متوفرة» for no hours), so the card's and the status card's `today` is no longer nullable.
- **Finding 215 was written during verification** and folded into commit 5. The plan lists it in §6 but not in §14's commits.
- **EC19:** `docs/design/INDEX.md` describes no frame of the Directory's paging, so it gets no line. `CHANGES.md` has R9 and a note on P6.

## Executor checks (EC)

- **EC1:** `@radix-ui/react-radio-group` 1.4.7 checks only on `ARROW_KEYS`. T50's Home/End failed with Radix alone before the handler.
- **EC2:** every utility exists.
  - `bg-muted`, `bg-card` and `shadow-raised` (from `--elevation-raised`, which is none in dark); `border-(--card-border)`; `data-checked:`; `pointer-coarse:h-(--control-height)`.
  - The pairs are §5's verified ones: `muted-foreground` on `muted`, `card-foreground` on `card`.
  - `check:classes` passes.
- **EC3:** `liveStatusFor` and `availableAmong` had no reader outside `directory`. The first became `publicStatesFor(targets, at)`; the second was deleted.
- **EC4:** `availableNow` is stripped, not refused (T6, T32, and the real run).
- **EC5:** codes in §6.
- **EC6:**
  - both CI attempts re-read: 156 ms and 206 ms, line 101, "element could not be found in the document";
  - two breaks made;
  - three full component runs green locally, and green in CI;
  - the optional local repro of the detached element was not attempted.
- **EC7:** `directory.title` is "Workspaces"; Home's h1 is "Find a workspace in the Gaza Strip".
- **EC8:** `closureInForce(now)` is the one `where` that `closedAt` and `closedSpaceIdsAt` share. T23 runs against the filter, and its deleted-closure break fails.
- **EC9:** each expectation was re-derived. `limit: 18` only where a test asserts the list's own request; the repository's and the key tests pass their own limits. The default-`DAY` tests were rewritten for `period: undefined`.
- **EC10:** #139; `#PRNUM` → `#139` in every commit's tree; none left.
- **EC11:** §6.
- **EC12:** overnight ranges are forbidden in the four places named; T27 covers a close at midnight.
- **EC13:** the lateral join works in `findPage` (rows and count, T16's totals), `findFirst` (the pins with `period`, T15) and the order.
- **EC14:** the glossary has no "available now" and lists no filters; no change.
- **EC15:** `viewAll.to` is `'open'`; Home links `/spaces?open=1` (T61).
- **EC16:** the favourites' tests compare against the list's cards and still pass. The card carries `hoursStatus`, and no `priceAgorot` without a period (T15, T36).
- **EC17:** `check:build` clean.
- **EC18:** no other branch or open PR holds findings 214 or 215.
- **EC19:** §8.
- **EC20:** `masaha_dev` was read with GET only, and never seeded.

## Findings

- **214 (Resolved).** The Home test's wait found Home's own search box.
- **215 (Open).** The prototype's Home (`verified && open`, `?available=1`) and `TodayHours` (the browser's day) disagree with production.

## Outside scope, noticed

- The `1e3` coercion (§6).
- The redundant `is_closed` in the `openNow` SQL (§6).
- The owner's local `apps/web/.env` still sets `NODE_ENV=development`, hence the explicit `NODE_ENV=production` build.
- The local `.claude/launch.json` fails Prettier locally only.

---

# Review fixes, round 1 (2026-11-08)

The input was `6_REVIEW_CLAUDE_CODE.md` on head `e1838447` (verdict: mergeable after a fix round), with the fix list `7_FIX_ROUND.md`.

## 1. The pull request and its head

- **PR #139.** The new head is **`79a94b3ab055bfd2247b1fb9e99622c8b57e8b19`**, pushed with `--force-with-lease`.
- **CI:** run 42494854737 on that head, `success`. All ten checks passed, including `test:api` (8 m 50 s) and `test:component` (9 m 19 s). CodeRabbit skipped.
- **GitHub:** `CLEAN`.
- **The PR description** gained a "Review fixes" section.
- `git diff e1838447 79a94b3a` shows 11 files, +61/−14: exactly the fixes below.

## 2. The commits

The history keeps five commits with no fix commits. Before the round I cut `backup/directory-filters-3`, because `-2` already existed from the `#PRNUM` rewrite. Each fix was a `--fixup`, then `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash origin/main` (`origin/main` is still `40cb481d`).

1. `f391bdfc fix(web): wait for the directory's own search` — unchanged.
2. `d735c69c feat(design-system): add the segmented control` — unchanged.
3. `595ad478 feat(directory): filter by the hours` — F4, and F6 (`HoursStatus`, `cardStatusOf`).
4. `2a982cbc feat(directory): price by subscription and order` — F1, F3, F5, and F1's line in `directory.md`.
5. `79a94b3a feat(directory): page by 18 and fit the panel` — F2, F6 (`DIRECTORY_PAGE_SIZE`), and F7, a body sentence: "Records finding 215 (OD7 b)…".

The fixes:
- **F1.** `useDirectoryList` keeps `shownPeriod`, the subscription the shown answer was asked with. It changes only once a real answer arrives (`!isPlaceholderData`), the way Home's `shownNearest` works, and words the card's price by it. `directory.md` says the cards shown keep their own period while another subscription's page loads.
- **F2.** In the prototype's `Directory.html`, `dir-results` moved from the results' section to the column wrapper, which is the grid's item, so R8's rule sizes it.
- **F3.** In T14, «Stale Verified» and «Fresh» (30 days) gain student prices. The test asserts `names('&studentPrices=true')` equals `['Fresh', 'Stale Verified']`, written by hand.
- **F4.** ADR 0008's *Decision* bullet is restored byte for byte from `40cb481d`. The *Revised* line now also names `GET /spaces/:slug/occupancy` returning `{ status, hoursStatus }`.
- **F5.** `pricePlaceholders`' lowest is `Math.max(1, Math.floor(…))`. Its test expects `'1'` for 1 agora and for a 50–99 agorot range. `directory.md`'s rule reads "never under 1".
- **F6.**
  - `export type HoursStatus = 'OPEN' | 'CLOSED'`; `HOURS_STATUSES` removed, since nothing read it.
  - `cardStatusOf` and `DIRECTORY_PAGE_SIZE` are module-local, since only their own files read them (`git grep`).
- **F7.** Commit 5's body now names finding 215.

## 3. What was run, and what was not

All on `79a94b3a`, one at a time.

| Command | Result |
|---|---|
| `npm run lint` · `typecheck` · `check:classes` · `check:links` (3,259 links) · `check:conflicts` | clean |
| `npm run format:check` | clean for the repository; it flags only the local, git-excluded `.claude/launch.json`, as before |
| `NODE_ENV=production npm run build` + `check:build` | clean (no showcase code in 76 files; nothing heavy in the first download) |
| `npm run test:unit` (full) | shared 28 / 304 · API 77 / 921 · web 188 / 1,198 |
| `npm run test:component` (full) | 342 files / 2,085 tests (+1, F1's test) |
| `npm run test:api` (full) | 125 files / 1,427 tests (11 m 42 s) |

- **The prototype check (F2).** I served a scratchpad copy of `docs/design/prototype` with Python's `http.server`, holding the head's page and the fixed page side by side, and measured both in headless Chrome. The server was stopped and port 8765 was then free.

  | Page | 1100 px | 1300 px |
  |---|---|---|
  | `e1838447` | results dropped under the filters (results top 889 against the filters' 246) | side by side |
  | fixed | filters 329 px (4/12) beside results of 683 px (8/12) | unchanged: 286 px and 906 px |

  The screenshots are `Downloads\directory-prod-shots\14-prototype-column-1100-ar-light.png` and `…-1300-…`.
- **Not run:**
  - per-commit typecheck and lint, which the round asked for neither of; typecheck and lint pass on the head and in CI;
  - the real run and the full screenshot set, since nothing in the production UI changed but F1's loading state, which its hook test proves;
  - E2E.

## 4. Breaks made, and tests seen failing first

- **F1.** The test failed first on exactly the defect: `Expected «‏20 ₪ / يوم», Received «‏20 ₪ / شهر»`. It passed after the fix.
- **F3.** Student prices read by freshness alone, as `s.prices_updated_at >= cutoff`: T14 fails (and the leave-one-out). As `verified OR prices_updated_at > cutoff`: T14 fails (the 30-day boundary). Both were restored.
- **F5.** The test failed on `'0'` before `Math.max(1, …)`.
- **F2.** Measured at the head, as above, before and after the fix.

## 5. Problems met, and how each was solved

- **The autosquash conflicted twice.** F1's test and F1's sentence in `directory.md` sit at places where commit 5 also appends (the test file's end; the list's paragraph, which commit 5 changes to 18 a page).
  - On the fixup step, I kept commit 4's text plus the fix.
  - On commit 5's step, I kept both sides.
  - The tree then differed from the pre-rebase head only in the order of two tests and in the F1 test's marks.
- **The F1 test's invisible marks.** Written through the shell, they landed as literal characters. I rewrote them as `⁦`-style escapes, as the rest of the file has them.
- **The prototype server.** After `TaskStop`, `netstat` still showed port 8765 under PID 0, a closing socket. No Python process held it, and it was gone at the next check.

## 6. Anything that behaved unexpectedly

Nothing beyond §5.

## 7. Early conflict check

| Open PR | Head | Result |
|---|---|---|
| #138 `design/space-profile` | `7ab1798f` (moved since the first report) | **conflict in `docs/design/CHANGES.md`** only, where both PRs append rows. Documents only, so whichever merges second takes the fast path |

## 8. Departures from the fix list

- **The backup branch is `backup/directory-filters-3`, not `-2`.** `-2` already held the pre-`#PRNUM` head, and I didn't overwrite it.
- **F4's *Revised* line also names the occupancy read's `{ status, hoursStatus }`.** The restored bullet no longer says so, so the revision carries it.
- **F1 also adds one sentence to `directory.md`**, so the document states the behaviour the fix adds.
