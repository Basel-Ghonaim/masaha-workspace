# S2b-4a — The admin's space editor, first half (web) — Report

## 1. The pull request

**#74** `feat(spaces): the admin's space editor` — https://github.com/Basel-Ghonaim/masaha/pull/74
Head **`b5406c0c26536463d84fe997ec02d0944f318f11`**, on `main` at `3c3dc47b` (after #73). CI passed on
that head (lint, typecheck, format:check, check:classes, check:links, build, test:unit,
test:component, test:api); GitHub shows **`CLEAN`**. Labels `feat`, `area:web`, `area:docs`; assigned
to the owner; `Closes #70`. 106 files: an independent review follows. Not merged.

## 2. The commits

1. `43f5871e` fix(web): no empty heading on an untitled page — #70: `PageHeader` falls back to the wordmark.
2. `09d37283` feat(web): a page titled by its record's name — `RecordTitleProvider` in `RootLayout`, `useRecordTitle`, `usePageTitle` returns `PageTitle` (`text`, `lang`, `dir`), the top bar's title on one line; architecture §2.
3. `f15e1724` feat(lookups): amenities checklist and area name — `AmenityChecklist`, `AmenityNames`, `AreaName`; `lookups.md`.
4. `c89214b0` feat(spaces): the admin's space editor — the route, `SpaceEditPage`, `SpaceEditor` (frame, navigation, checklist, «المساحة», read-only, leave guard), the repository's five calls; `spaces.md`, the overview, findings 59–60.
5. `b06cf242` feat(spaces): a space's amenities and contacts — the two sections and their read-only views; the carrier rule.
6. `b5406c0c` feat(spaces): open the editor from list and add — «تعديل» in the row menu, the name a link (`space-links`), the add page lands on the editor (D6 supersedes #57's D2); `space-links.md`.

Each commit typechecks and lints on its own (checked with `git rebase -x`).

## 3. What was run

Locally, one at a time, no other lane running (`Get-Process node` checked before each full lane):
- `test:unit`: 70 files, **761 passed**.
- `test:component`: 130 files, **848 passed** (400 s), on the code of the head (the commits after it changed only comments and documents, and the rebase onto `main` brought new files in `apps/api` and `packages/shared/src/directory` only).
- `NODE_ENV=production npm run build`, `check:build`: no showcase, no dashboard code, no data-table or Leaflet in the site's first download.
- `lint`, `typecheck`, `check:classes`, `format:check`, `check:links`: clean.
- A real run in headless Chrome over CDP, API 3320 and web 5320 (§5 below); servers stopped by PID, ports 3320 and 5320 checked free; no headless Chrome left.
- **Not run:** `test:api` — no API change (CI ran it on the head: pass).

## 4. Breaks made, tests seen failing first

Every new test was seen failing in its lane before its code: the `PageHeader` test (empty `h1`), the record title's three tests (against a no-op hook), the lookups' 11 tests (against `null` stubs), the repository's 7, the services' (`profileValues`, `profileEditInput`, `profileChanges`, `updatedAgo`, `carrierOf`), the editor's 21 then 14 more (against a stub editor), the route tests, the menu's and the list's 4, and the landing's 2.

Breaks made and restored, each caught:
- `useRecordTitle` without its cleanup → "lets the next page's title show once the record's page has gone" failed.
- `SpaceEditPage` without `useRecordTitle(name)` → "is titled by the space's name once it has loaded…" failed.
- The leave guard blocking whatever the path → "never asks for a move within the page, to a section" failed.
- No refetch on a 403/404 → "turns the page read-only once a save finds the space verified meanwhile" failed.

## 5. Problems met, and how each was solved

- **Toasts leaked between the editor's tests** (sonner's store is global): "Found multiple elements with the text: Amenities saved". Solved as the other files do: `toast.dismiss()` in `afterEach`.
- **A repeat and an unstorable contact in one save**: the shared schema finds a repeat only once every contact can be stored (its `superRefine` runs after the transforms pass), as the server does. The test asked for both at once; split into two tests, and the rule written in `spaces.md`.
- **`restrict-template-expressions`** on the field paths of the field arrays: small typed helpers (`ownName`, `contactField`) with `String(index)`.
- **The spaces page's 429 route test** expected every menu item to wait; Edit, a way to a page, never does by design. The test now checks the actions (Hide, Delete); folded into commit 6.
- **The sticky chips' offset**: the prototype measures the top bar, which an arbitrary value outside the layer would need. Solved as planned (S7): the top bar's title keeps one line (`truncate`), so the row sticks at `top-14`.
- **A form's box inside a `Card`**: the card's gap is a token only the layer may bind; the section's `<form>` is `contents`, so its content and footer are the card's own children.
- **The real run's sign-in switched the interface to the account's language and theme** (Arabic, dark): the script switched to English and light through the top bar's toggles.
- **The rebase onto `main` after #73**: conflicts in `spaces.md`, `lookups.md` and the overview only; resolved by the fast path, both sides kept (the directory's lines and the editor's).
- **The PR number in the documents**: written as a placeholder, then replaced with `#74` in every commit's own tree (`filter-branch --tree-filter`) just before the push; a `rebase -x` amending each commit had made the later patches conflict, and was aborted. The PR got #74.

## 6. What behaved unexpectedly

- **Full component lanes on a loaded machine**: two runs took 469 s and 515 s (the usual ~250 s). The first failed findings 28/55's two lazy-shell tests ("lists the owner's eleven pages", "shows its page to a guest…") and the real 429-test break above; the second failed `RootLayout` › "shows the general error in place of a shell that fails, with no header" by its 5 s test timeout. That test passed 3 of 3 alone (~15 s per run), and the third full run, with the dev servers stopped, passed whole (848). The `RootLayout` test is no lazy-shell wait, so finding 55 does not cover it; I did not record a new finding, as it never failed alone or in CI.
- **Finding 60, in the real run**: with the space's area (Al-Mawasi) hidden, the area field shows **nothing at all** — not even its placeholder, as the finding first said; the finding was corrected. **What the admin sees:** an empty Area field on an existing space, as if it had none. The profile still saves (only the changed field is sent). Screenshot `11-finding60-area-hidden-1440-en-light.png`. The area was hidden through the API for the run and restored after it.
- `Intl.RelativeTimeFormat` in Arabic says «أول أمس» for two days ago, not the prototype's «قبل يومين»; kept, as the browser's own Arabic.
- Two files written by Python's text mode on Windows took CRLF in the working tree; git normalised them, and the rest were written with `newline=''`.

## 7. The early conflict check

`gh pr list --state open`: **#74 only**; no other open pull request to check. `main` (`3c3dc47b`) is in the branch.

## 8. Departures from the prompt

- **The prompt said "Plan only… then stop"; the reply said save the plan, cut the branch and build.** Followed the reply.
- **`DocumentTitle.component.test.tsx`** was listed as updated in the plan; it needed no change (the new record-title test covers the tab).
- **The verified page's Alert** reads «يعدّلها مالكها» with no name and offers no unlink (the owner's Q1 (b), finding 59).
- **Extra component files** beyond the plan's list, one responsibility each: `ReadOnlyCard`, `ReadOnlyRows`, `EditorLoading`, `EditorFailure`, the read-only hooks, `useSaveGroup` and `useSpaceAnswer` (shared by the three sections' saves), `profileFieldOrder.ts`, `useProfileFields.ts` (shared by the add form and the editor), and `test/fakeIntersectionObserver.ts`.
- **The section in view's test with several sections** arrived with commit 5, when there were several; commit 4 tests the first one marked.

## Screenshots

`C:\Users\basel\Downloads\s2b4a-shots\` (not committed): `01-editor-unverified-{1440,768,390}-{en,ar}-{light,dark}` (12), `02-chips-sticky-390-ar-light`, `03-after-create-1440-en-light`, `04-verified-readonly-{1440,390}-en-light`, `05-row-menu-edit-1440-en-light`, `07-amenities-dirty-…`, `08-contact-refused-…`, `09-contact-stored-form-…`, `10-leave-dialog-…`, `11-finding60-area-hidden-…`.

---

# Review fixes — round 1 (`REVIEW74_FIXES.md`)

## 1. The pull request

**#74**, new head **`e858f16b7c52f322b03e2195dbbcf3a1f2535546`**, on `main` at `3c3dc47b` (unchanged). CI passed on that head (every job, `test:api` included); GitHub shows **`CLEAN`**. One "Review fixes" comment posted (no thread replies); the description updated to the final state. Not merged.

## 2. The commits

Still six, each fix folded into the commit it corrects (fixup + autosquash), each subject ≤ 50, each commit typechecked and linted on its own:
`43f5871e` fix(web): no empty heading on an untitled page · `712f272e` feat(web): a page titled by its record's name · `8733caa1` feat(lookups): amenities checklist and area name · `a1ae5c71` feat(spaces): the admin's space editor · `07d999ec` feat(spaces): a space's amenities and contacts · `e858f16b` feat(spaces): open the editor from list and add.

## 3. What was run

On `e858f16`, one at a time, after checking no other folder ran a lane (no node process outside this folder): `test:unit` web **768** (other workspaces 205 and 667); `test:component` **895** (140 files, 326 s); `NODE_ENV=production` build and `check:build`; `lint`, `typecheck`, `check:classes`, `format:check`, `check:links`: clean. **Not run:** `test:api` (no API change; CI: pass). Real run in headless Chrome (API 3320, web 5320): the section jumps before and after the change at 1440 and 390; finding 3's concurrent edit through the API; finding 2's save of a space deleted meanwhile; a confirm answered 429 (intercepted with CDP's `Fetch`, as no limit is reachable by hand). Servers stopped by PID (the API's `tsx watch` and `pino-pretty` included), ports 3320 and 5320 free, no headless Chrome left.

## 4. Breaks made, tests seen failing first

New behaviours, each test failing before its code: 2 (the 404 with an earlier read; the name of a deleted space), 3 (another admin's change), 4 (the hold under a 429), 8 (the type change), 9 (proceed; the "being saved" line), 10 (sections drawn anew), 13 (Discard and confirm clear), 14 (the answer kept fresh), 15 (no cached editor refetched), 16 (Remove held), 18 (the mixed 422 and the refetch), 1 (the chip-click test: the plain anchor put back fails it).
Moved and gap tests, each proven by a break made once and restored: the dirty check of each section's follow-effect (6a, three sections), `onDirtyChange(false)` and `beforeunload`'s removal (6b), the frame's unmount cleanup (6c), the confirm's group hard-coded (6d), `amenitiesForm`'s sort, blank-name and own-order rules and the contacts' comparison (6e), the lookups' retired filter, toggle, Arabic names and the area's governorate, and fix 15's predicate.

## 5. Problems met, and how each was solved

- **Finding 8:** validating the type's own path left the value's error standing (the resolver's result is applied per field name); the hook triggers the row's value instead.
- **`react-hooks/refs`** refused a ref written during render for finding 3's latest space; the follow-effect is keyed by the profile's own fields (`profileOf`) instead.
- **The amenities' 6(a) test** first changed only the profile, which never reruns the amenities' follow-effect; it now changes the amenities group itself, and the break fails it.
- **Finding 19:** the lint's `no-deprecated` refuses `returnValue` (pushed back, §8).
- **Heredoc scripts** failed to parse twice; written as files instead (the known Git Bash quirk).
- The run script's chip selector matched `href="#contacts"`; the router's link renders the full path, so it matches the end.

## 6. What behaved unexpectedly

- **Finding 1 did not reproduce.** Before the change, every chip and checklist click landed on its section and stayed (`scrollY` steady at 150/600/1500 ms; 1440: Contacts at the page's end, Amenities' top 80 px; 390: 112 px), with no dialog. The router's link gives the same landings after. The mechanism the review read may need conditions this run did not meet (a scroll position saved earlier under the first entry's key); the change removes the dependence either way.
- **The 404 after a deleted space's save was titled by the gone space's name** (cached read): `useSpaceName` now gives no name for a space found deleted (folded into commit 4, own test).
- **The checklist's accessible name ran two words together**, "GeneratorInactive"; a space now separates them.
- **6(f)'s break passes now, by design:** fix 18 catches a refusal on `amenityIds` where it arrives, so adding `amenityIds.0` to `FIELDS` no longer hides it.
- **Finding 12** cannot be shown in jsdom (one frame); the change is made and the clearing test still holds.
- A run of the affected files with the dev servers up failed two route tests by their 3 s wait ("lists the owner's eleven pages", finding 55's; "shows the admin the lookups page"); the file passed alone twice, and the full lane on the head passed whole.

## 7. The early conflict check

#75 `design/account` (`f100a287`): clean · #76 `design/owner` (`5a226763`): clean · **#77 `feat/space-photos` (`9bc0b705`): conflicts in documents only** — `docs/features/spaces.md`, `docs/architecture/findings/README.md`, `docs/project/overview.md`. The PR merged second takes the fast path (both sides kept).

## 8. Departures, pushed-back items

- **19 — pushed back:** `event.returnValue` is refused by the project's lint as deprecated, and `preventDefault()` alone asks in every current browser (Chrome 119+, Firefox, Safari); disabling the rule for a browser three years old seemed the worse trade.
- **1:** changed although not reproduced (as the prompt asked: "whatever you see").
- **Beyond the list:** the deleted space's name dropped from the 404's title, and the checklist's name/mark space, both found in this round.
- **New Arabic line** for the owner's approval: «التغييرات في {الأقسام} قيد الحفظ.»
- Screenshots added: `12-jump-…` (before/after), `13-deleted-meanwhile-404-1440-en-light`, `14-confirm-429-held-1440-en-light`.
