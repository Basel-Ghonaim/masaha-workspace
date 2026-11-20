# SPACE_PROFILE — Phase 2 report: PR-C (#143)

> Executor: Claude Code (Opus 5.5), 2026-11-11, **a resumed session** (`3_EXEC_PROMPT_C_RESUME.md`): the first session
> built C1–C5 and ran out of context before verifying, pushing or reporting. This session trusted none of its
> verification and ran all of it again. Plan: `2_PLAN_PROD.md`. **Never merged; no branch deleted.**

## 1. The pull request and its head

| PR | Branch | Head (full SHA) | CI | GitHub |
|---|---|---|---|---|
| **#143** `feat(spaces): the space profile, view first` | `feat/space-profile` | `29a25054cca12d714bb2ede8e83dbf47dd13be07` | 10 pass, CodeRabbit skipped (component job on its 2nd attempt, §6) | `CLEAN` |

Assigned to the owner; labels `feat`, `area:web`, `area:docs`, `area:design-system`. **#143, not the expected #142**:
#142 went to the palette lab's `design/ink-spark` meanwhile (merged 16:13). `#PRNUM` → `#143` in each commit's tree
just before the push (filter-branch); none left. **217 files.** Base: `origin/main` `93fe4105`; `main` then moved to
`f0709d28` (#142) — a merge apart (§6).

## 2. The commits

| Commit | Subject | Files |
|---|---|---|
| `549c1918` | C1 `feat(lookups): area combobox and amenity catalogue` | 17 |
| `f7a3414b` | C2 `feat(spaces): the space profile, view first` (+ T48's Arabic half, folded) | 180 |
| `1ba8748c` | C3 `feat(spaces): drag to order photos and contacts` | 16 |
| `f719d2c5` | C4 `feat(spaces): admin hide and delete in the top bar` | 9 |
| `29a25054` | C5 `feat(spaces): prices edited in the profile only` | 15 |

No `fixup!` left. Backups: `backup/space-profile-3` (`dec5da08`, the first session's head) and `-4` (`a95368b7`, before
the rewrite); `-1`, `-2` from the first session.

## 3. What was run

All on the head, **one heavy command at a time** (free memory 2.6–4.9 GB; another worker running).

| Check | Result |
|---|---|
| `lint`, `typecheck` | clean on **each of the five commits**, one command at a time, back on the branch after each |
| `format:check` | clean for the repository (only the local, git-excluded `.claude/launch.json` flagged, as in #140/#141) |
| `check:classes` / `check:links` / `check:conflicts` | clean (1982 files) / 3268 links / clean — `check:links` and Prettier re-run after the `#PRNUM` rewrite: same |
| `NODE_ENV=production npm run build` + `check:build` | clean; `sortable` neither in the site's first download nor reached by a site page |
| `test:unit` (shared / API / web) | 323 / 921 / 1256 — all passed |
| `test:component` | 346 files, 2083 tests — all passed |
| `test:api` | 125 files, 1432 tests — all passed |

No lane was killed for memory. **Not run:** E2E (end of project); a real phone and a real screen reader (Review Focus).

**Real run** — API on 3342 against the throwaway `masaha_wi142_dev` (the demo set; **`masaha_dev` untouched, never
seeded**), web on 5342, headless Chrome over CDP (`run.mjs` in this session's scratchpad):
- the owner's profile (space 1) at 1440 / 768 / 390 × ar / en × light / dark (six shots), the admin's editor (space
  11, unverified) at 1440 / 768 / 390: **no horizontal overflow, no console error**;
- every Sheet (seven) at 1440 ar, 390 ar, 768 en: opens without overflow; Escape closes it; the focus returns to its
  «تعديل»; a changed hours Sheet asks «تجاهل التغييرات؟»;
- «نسخ الرابط»: the clipboard holds `http://localhost:5342/spaces/masaha-demo`, toast «نُسخ رابط الصفحة العامة»;
- «استخدم موقعي الحالي» (DevTools geolocation): inside → `31.50120, 34.46650`, toast «نُقل الدبوس إلى موقعك الحالي…»;
  outside → coordinates kept, «الموقع خارج قطاع غزة»;
- photos: one upload with its bar; **keyboard** — «رُفعت الصورة 2، المكان 2 من 4.», ArrowLeft (RTL) «… المكان 3 من 4», drop
  → one order saved (`mtkUX3 GTgF1Y SYGOPB SD7JO7 → mtkUX3 SYGOPB GTgF1Y SD7JO7`); **mouse** — the third onto the
  first becomes the cover; **touch** at 390 — a swipe scrolls (300 → 717 px) and moves nothing, a press-and-hold drags;
  a mouse click and a finger's tap on a delete each ask «حذف هذه الصورة؟» (the cover's with the next-cover line);
- contacts' Sheet (a second row added in the draft, then discarded): keyboard lift / ArrowUp / drop moves it first,
  the Sheet staying open; a mouse drag of the handle moves it back;
- admin: «Unverified» and «Link an owner» in the header; below 768 px «إجراءات الصفحة» = «إخفاء عن الزوار · حذف
  المساحة»; hide → toast «أُخفيت بيت المستقلين من الموقع» with «تراجع», the badge shows; «تراجع» restores; a verified
  space (1) shows no «تعديل» and no «إدارة الصور».
- Servers stopped by PID (tsx, its server, vite, their `cmd` wrappers); ports 3342 and 5342 free; no CDP Chrome left.
- **Screenshots:** `C:\Users\basel\Downloads\wi142-shots` (45, curated by name, never pushed). The first session's
  31 were moved, not deleted, to `Downloads\wi142-shots-previous-session`.

**Executor checks for PR-C:**
- **EC2:** the built `sortable` chunk is **42.57 kB, 14.01 kB gzipped** (`dist/assets/sortable-DftcJyh5.js`), held
  out of the first download by `check:build`.
- **EC4:** touch emulation at 390 — a press-and-hold drags, a swipe scrolls, a tap on a tile's delete is a click
  (the dialog opens).
- **EC7:** the contact and UI glyphs are the installed Lucide names (typecheck and build).
- **EC9:** the glossary holds «الأسعار المعلنة» and «سعر» (C2).
- EC1, EC3, EC5, EC6, EC8, EC10: #140 / #141 (`4_REPORT_AB.md`).

## 4. Breaks made and tests seen failing first

- **The matrix (§12) was checked test by test** against the branch: T21–T26, T30–T53 for PR-C all present, **except
  T48's Arabic half for the photos' edit state** (axe ran in English only). Added to the existing test (now «in
  English and in Arabic»); **seen failing** with the Arabic photo names blanked in the catalogue (axe `button-name` on
  the tiles 2 and 3, English half unaffected); restored from a `cp` backup; folded into C2.
- **The first session's tests:** its scratchpad keeps red runs — three logs of component tests failing before their
  code (the Sheets, the header, the index, the admin's page, the photos, the leave guard, `usePackageShiftIds`, among
  others) and the lookups' and the services' files backed up for their breaks — but its per-test account was never
  written. Not re-run here; every lane passes on the head.

## 5. Problems met and how they were solved

- **The PR number moved** (#142 taken by the palette lab): `#143` used in the docs; the number checked again in the
  same command as the push and `gh pr create`.
- **Three commit subjects over 50 characters** (§14's wording; the workflow and the prompt cap them at 50):
  shortened in the same filter-branch as the `#PRNUM` replacement. The rewrite was verified to change nothing but the
  55 placeholder lines, commit by commit.
- **CI's first `test:component` failed with all 2083 tests passing:** one unhandled error after the tests —
  `ReferenceError: window is not defined` from sonner's removal timer (`Timeout._onTimeout` → `dispatchSetState`),
  attributed to `features/spaces/hooks/delete/useDeleteSpace.component.test.tsx`: its `afterEach` dismisses the
  toasts, sonner removes them on a short timer, and the timer fired once the file's jsdom was gone. The file and
  `useDeleteSpace` are unchanged by this PR; the error was not in the local run, nor in the logs of the last fifteen
  failed runs. **Re-run once** (the prompt's rule for a failure the PR did not cause): green. Said in the PR.
- **My own run script** first missed three things (fixed in the script, nothing in the app): «نسخ الرابط» clicked
  off-screen after a scroll; space 1 has one contact, so the Sheet draws no handle (nothing to order against) — a
  second row was added in the draft; the photo order read the file name instead of its key.

## 6. Anything that behaved unexpectedly

- **`main` moved during the session:** #142 (`f0709d28`, «ink and berry») changed only `docs/design/` (58 prototype
  files, `CHANGES.md`, `INDEX.md`): no code, no tokens, nothing deleted or renamed, none of #143's files — a merge
  apart; #143's CI ran after it. The plan's risk (token renames from the palette lab) did not happen.
- **The sonner teardown race** (§5): a flake in a file outside this PR. **Offered as finding 219** (not recorded:
  the prompt says retry once, then report): "A toast's removal timer can outlive its test file's jsdom".
- **At 390 px a contact tile's long value is cut with «…»** in the two-column grid (`+970599000…`); the whole value
  stays in the link's text. In the PR's Review Focus.
- **The amenities' Sheet tests live in `ContactsSheet.component.test.tsx`** (its second `describe`), not a file of
  their own — they pass and prove A2; left as written (no drive-by move).
- **The throwaway `masaha_wi142_dev`** keeps this run's writes (an upload and reorders on space 1, a hide and its undo
  on space 11) and its photos under `apps/api/.storage/`; drop it when no longer wanted.

## 7. The early conflict check

Open PRs at the report: **#143 only** — nothing to compare. Against the new `main` (`f0709d28`): GitHub `CLEAN`; no
shared file.

## 8. Departures from the prompt and the plan

1. **The context restart** — the build is the first session's; this session's work is the matrix check, T48's
   Arabic half, the whole verification, the rewrite, the PR and this report.
2. **#143 instead of #142** (§1); the screenshots stay in the folder the prompt named, `wi142-shots`.
3. **Commit subjects shortened** to 50 characters (§5).
4. **The `sortable` library chunk joins in C3** (as #141 said).
5. **Finding 216 written with C2** (where the shifts' Sheet holds a package's shift), not C5.
6. **`weekRows` moved to `shared/lib/time`** (the profile's hours view is its second user) — not in §8's list.
7. **Names differ from §8:** `useSheetFrame` + `useResetOnOpen` for `useEditSheet`; `SectionEmpty` added; the badges
   inside `ProfileHeader` (no `SpaceStatusBadges`); `noticeGroup.ts` → `noticeSection.ts`; `profileChanges.ts` kept,
   `useProfileSheet` the one form of «عن المساحة» and «الموقع» (each still sends only its own fields, T33).
8. **Two files beyond §8 in C5:** `DataReportsPage.tsx` (the report link no longer takes the field) and
   `SpaceSettingsCards.tsx` (visit pricing's link words name the profile).
9. **The CI component job re-run once** (§5).

## Findings

- **216** (Accepted, in C2): the admin's shifts Sheet cannot mark a shift a package uses.
- **Offered, not recorded:** 219 — the toast timer outliving a test file's jsdom (§6). Next free: 219.

Then stop: never merged; no branch deleted (the `backup/*` branches are kept).

## Fix round (2026-11-12) — the review's F1–F10, FR1–FR4, finding 219

> Executor: Claude Code (Opus 5.5), one session, `7_FIX_ROUND_C.md`. **Never merged; no branch deleted.**

### 1. The pull request and its head

| PR | Branch | Head (full SHA) | CI | GitHub |
|---|---|---|---|---|
| **#143** | `feat/space-profile` | `14d3bb6e9982664b9de6f3a710571faae6e3ab4b` | run 43199243125, **10 pass** (`test:api` included), CodeRabbit skipped — first attempt | `CLEAN` |

Base kept: `93fe4105` (`main` is `f0709d28`, a merge apart, docs/design only). Pushed with `--force-with-lease` against `29a25054`. The PR description gained **"Review fixes"** (each F, its commit and test, FR1–FR4, finding 219, the fix round's evidence and what was not run), and its final-state lines (documents list, deviation 7, screenshots).

### 2. The commits

| Commit | Subject | Files | Folded in |
|---|---|---|---|
| `bd7bbd6d` | C1 `feat(lookups): area combobox and amenity catalogue` | 18 | F3 (`useAreaLine`), F9 (the catalogue says its read failed) |
| `89bb16cc` | C2 `feat(spaces): the space profile, view first` | 190 | F1, F2 + FR3, F3 (the header's `·`), F4, F5, F6, F7, F8, F9, finding 219 |
| `b035dd46` | C3 `feat(spaces): drag to order photos and contacts` | 16 | — |
| `a25425d8` | C4 `feat(spaces): admin hide and delete in the top bar` | 9 | F10 (the menu's items) |
| `14d3bb6e` | C5 `feat(spaces): prices edited in the profile only` | 15 | F10 (the notice "inside") |

Fixups + `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash 93fe4105`; five commits, no `fixup!`, subjects unchanged (≤ 50); bodies updated for C1, C2 and C4 (each now does more); no tool attribution. **The head's tree is the pre-rebase tree** (`5df84a5a`, checked). Backups: `backup/space-profile-5` (`29a25054`, before the round), `-6` (the fixups before the autosquash), `-7` (after it, before the rewording).

### 3. What was run

On the head, one heavy command at a time (free memory 1–6 GB; another session planning in `app-design`):

| Check | Result |
|---|---|
| `lint`, `typecheck` | clean on **each of the five commits**, one at a time, back on the branch after each |
| `format:check` | clean (only the local, git-excluded `.claude/launch.json`, as before) |
| `check:classes` / `check:links` / `check:conflicts` | 1984 files clean / 3269 links resolve / no marker |
| `NODE_ENV=production npm run build` + `check:build` | clean; `sortable` 42.57 kB (14.01 kB gzipped), out of the first download |
| `test:unit` | shared 323 · API 921 · web 1257 — all passed |
| `test:component` | 347 files, 2097 tests — all passed (15 new, 1 removed with the hold) |
| `test:api` | **not run locally** — the round changes no API, shared or schema code; **CI ran it: passed** |

No lane was killed for memory. **Real run** (API on 3342 against `masaha_wi142_dev` — checked in `pg_stat_activity` before any write; web on 5342; headless Chrome over CDP; `masaha_dev` untouched, never seeded):
- **F1:** the admin opens «عن المساحة» of the unverified space 10 «مكان التفاح», types; a second tab deletes the space («حذف المساحة» → «حذف»); the first tab's «حفظ» → «الصفحة غير موجودة»; the sidebar's «المساحات» lands on the spaces list, **no dialog**.
- **F3:** the admin hides «الرمال» (lookups); the demo owner's «ملف المساحة» (space 1): header «المنطقة الحالية — لم تعد متاحة للاختيار · موثّقة», «الموقع»'s first line the same; English, dark, 390 px: "Current area — no longer offered · Verified", no horizontal overflow. No console error in either.
- Servers stopped by PID (tsx, its server, pino-pretty, vite and their `cmd`/`npx` wrappers — the other sessions' `app-design` and `app-pr143` vites left alone); ports 3342 and 5342 free; no CDP Chrome left.
- **The throwaway database keeps two writes:** space 10 deleted (restorable from the deleted spaces), «الرمال» hidden (spaces 1, 2, 11 keep it).
- **Screenshots:** `C:\Users\basel\Downloads\wi143-fix-shots` (8: `01`–`04` F1, `05`–`08` F3), never pushed.

**Not run:** `test:api` locally (above); E2E (end of project).

### 4. The breaks made, and the tests seen failing first

Every new or changed test was run at the old code first (all in their own lane), then the fix; breaks of existing or redundant code were made from a `cp` backup (`breaks.py`, `shutil.copy2`) and restored from it, never `git checkout`.

| Fix | Test | Seen failing |
|---|---|---|
| F1 | `EditSheet` — a changed «عن المساحة» saved into a 404, then a link lands | at the old code ("Elsewhere" never shown: blocked, no dialog) |
| F1 | `EditSheet` — a 403: focus on «عن المساحة»'s heading, `beforeunload` not prevented, a link lands | at the old code (focus on `body`); **breaks:** the editor's drop removed → fails; the focus read from the closure again → fails |
| F1 | `useSheetFrame` — the unmount reports `false` | at the old code; **break:** the unmount report removed → fails (the `EditSheet` tests stay green: the drop covers them) |
| F1 | the guard's not-ready reset | **its break fails no test** — the unmount report and the drop already disarm the guard on every path (said in the PR) |
| F2 | `ProfileSheets` — read again while open (another's `nameAr`, `addressAr`) → body `{ descriptionEn }` | at the old code (`nameAr` and `addressAr` sent back); **break:** `profileOf(space)` for `filledFrom` → fails |
| F2 | `profileEdit.unit` — the other part's change never in the result | at the old code |
| FR3 | `HoursSheet` — a shift added by a read while open is sent; the shifts' Sheet sends a Friday opened meanwhile | both at the old code |
| F3 | `AreaLine` — a hidden area on the public source says the kept wording | at the old code |
| F4 | `ContactsSheet` (amenities) — retired, not held: saved as own; held: refused | at the old code; **break:** `|| space.amenityIds.includes(id)` removed → the held half fails |
| F6 | `HoursSheet` / `PricesSheet` — «أضف ساعات العمل» / «أضف وردية» with no hours open «تعديل ساعات العمل» | **the review's break** (`'hours'` → `'shifts'`, both places) → **both fail** |
| F7 | `EditSheet` `?sheet=` on a verified space opens nothing | the `?sheet=` check alone, or with F1's drop, removed → still green (the section mounts no Sheet while not editable); **all three removed → fails** |
| F7 | `SpaceEditor` letter tile; 403's and 404's own titles | **breaks:** the letter removed → fails; the two states swapped → both fail |
| F8 | `ProfileSheets` — the landmark's `lang`/`dir` | at the old code |
| F9 | `SpaceEditor` header (gallery 403 → the line, retry → «6 من 7»); `ContactsSheet` amenities (failure + retry); `useAmenityCatalogue` (failed, read again) | each at the old code |
| F10 | `SpaceEditorActions` — while a hide waits, ArrowDown reaches the marked item, Enter sends nothing | at the old code (a disabled item takes no focus) |

### 5. Problems met, and how each was solved

- **The autosquash conflicted in `docs/features/spaces.md`** three times (the C2 fixup, then C3's and C4's own picks): C3 and C4 change lines beside this round's. Resolved by writing each commit's original file with this round's eight edits applied (a script, eight changed lines checked each time); the final tree equals the pre-rebase one.
- **`?sheet=`'s check became redundant** with F1's drop (see §4, F7); kept, since it avoids opening a Sheet for one render — the test proves the behaviour and its full break.
- **"Drawn" needed the owner's 403** to mean "the state that draws the dialog": the owner's 403 moved from `SpaceEditor`'s render into `useSpaceEditor` as its own `forbidden` state (it also stops the hash landing on that page).
- **F9's catalogue failure needed `lookups`:** only `lookups` knows its read failed, so `useAmenityCatalogue` returns `{ entries, failed, retry }` (C1), and spaces' `AmenityCatalogue` slot follows (C2).
- My own scripts: Python's `-I` ignores `PYTHONIOENCODING` (stdout reconfigured instead); a path's backslashes eaten in a generated script; the run script's `setSelectionRange` on an email field, and the lookups switch's name isolated (U+2068/2069). All fixed in the scripts; nothing in the app.

### 6. Anything that behaved unexpectedly

- **On the admin's 404 page, the top bar still offers «إخفاء عن الزوار» and «حذف المساحة»** for the space just found deleted (shot `03`): `SpaceEditorActions` (C4) reads the space query, whose earlier data stays after the 404. Not this round's defect and not changed; **offered as finding 220** (not recorded: the prompt allowed only 219).
- **The owner's checklist offers a retired amenity the space holds** (from the space's read), but the own-amenity clash checks only the catalogue an owner reads, which holds no retired amenity — so on the owner's page an own amenity named like a held, retired one is not refused. The opposite case to F4, minor; noted, not changed.
- `masaha_wi142_dev` now holds space 10 deleted and «الرمال» hidden (§3).

### 7. The early conflict check

Open PRs: **#143 only** — nothing to compare. `git merge-tree` with `origin/main` (`f0709d28`): clean.

### 8. Departures from the prompt

1. **F1's third part: I chose "reset the guard when not ready"** (the prompt's choice to make): no state but the drawn profile has anything to lose, so asking there would be untrue. Its break fails no test, said.
2. **F9 also touches C1** (the prompt said C2): only `lookups` can say its read failed. **F9's wording:** the header «تعذّر حساب اكتمال الملف: لم تُحمَّل الصور» / "We couldn't count the profile: the photos didn't load", with the gallery's own retry; «المرافق» «تعذّر تحميل قائمة المرافق» / "We couldn't load the amenities list" in the page's failure line, with the list's retry. The index keeps no dots after a failure (it claims nothing).
3. **The owner's 403 became a hook state** (§5) — needed for F1's "drawn".
4. **F8 changes the catalogue's landmark line** from a sentence to its label («علامة مميزة:»), so the landmark can sit in its own element with its `lang`.
5. **"Review fixes" is a section of the PR description**, as the prompt says (workflow §3 names one comment).
