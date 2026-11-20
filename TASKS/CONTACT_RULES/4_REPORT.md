# CONTACT_RULES report

## 1. The PR

[PR #149](https://github.com/Basel-Ghonaim/masaha/pull/149) — `fix/contact-rules` — head `a28f74dfce93bfc5900db2ccbdbfdde96ac4f976`. GitHub CI is green; `mergeStateStatus` is `CLEAN`, and its `headRefOid` matches this head. The PR is open and was not merged.

## 2. The commits

- `a28f74df docs: resolve findings 217, 218, 219, 225, 226`
- `afea0331 test(web): wait out toast timers, warm lazy routes`
- `c93b2afc fix(design-system): wash a row's ghost control`
- `1873382b fix(spaces): accept only real links in contacts`
- `840a7c2b fix(shared): read Arabic-Indic digits in phones`

The change contains the plan's 37 distinct files plus the owner-directed finding 228 file: 38 paths total, including two renames and two additions.

## 3. What was run

**Per-commit gates**

- Commit 1: lint, typecheck, Prettier (15 code files), shared unit 7 files / 138 tests, web unit 20 / 75, component 2 / 27, API 1 / 11 — passed.
- Commit 2: lint, typecheck, Prettier (4 code files), shared unit 4 / 123, component 21 / 186, API 17 / 282 — passed.
- Commit 3: lint, typecheck, Prettier (3 code files), `check:classes` (1,988 files), token unit 1 / 200, component 15 / 96 — passed.
- Commit 4: lint, typecheck, Prettier (6 code files), component 8 / 60 — passed.
- After rebasing on PR #147: lint and typecheck — passed.
- Commit 5: `format:check` and `check:links` — passed; 2,784 links in 226 documents and 2,689 source files resolve.
- After each PR-number-only documentation rewrite: `format:check` and `check:links` — passed.

**Final local verification**

- Lint, typecheck, `format:check`, `check:classes` (1,989 files), `check:links`, `check:conflicts`, production build, and `check:build` — passed. The built CSS contains the table-row-scoped rule; `check:build` found no showcase code in 73 build files and checked 1,132 strings.
- `test:unit`: shared 29 files / 371 tests; API 77 / 924; web 196 / 1,403 — 302 files / 2,698 tests passed.
- `test:component`: 349 files / 2,152 tests passed.
- Initial full `test:api`: 126 files / 1,451 tests, 7 failures / 1,444 passed during PostgreSQL memory pressure. The retry repeated directory open-hours failures, so I stopped under the prompt's repeated-failure rule. On resumption, the owner restarted Docker, passed the two affected files on this branch and on main (37 tests each), then passed the full API lane on this branch through `heavy.mjs` (126 files / 1,451 tests, exit 0). No code changed after the original stop. The logs are `diag-branch.log`, `diag-main.log`, and `diag-full-api.log` in the task folder. The complete CI API lane also passed on the pushed head.
- Live API `/health` on port 3337 returned `status: ok`, `db: up`. PID 20984 was stopped; port 3337 is free. The showcase browser printed no errors. Its server PID 23900 was stopped; port 5337 is free.
- On PR #149, build, `check:classes`, `check:conflicts`, `check:links`, `format:check`, lint, `test:api`, `test:component`, `test:unit`, and typecheck all passed. CodeRabbit was skipped. GitHub reports `CLEAN`.
- Not run: the release E2E smoke, which is outside this task.

## 4. Breaks log

- Commit 1 tests-first: shared unit tests had 7 failures across the six Arabic/Eastern phone cases and OTHER-number normalization; component tests had 2 failures (normalized description and save toast); the API test expected 200 and got 422. All were before the code.
- Commit 1 mutations: changing the Eastern zero mapping failed the digit test; removing the `00` prefix failed four phone cases; fabricating a number for a failed match broke invalid-input refusals; returning the invalid input from `phoneSchema` broke browser validation. Each mutation was restored.
- Commit 2 tests-first: shared contacts tests had 27 failures over invalid domains, Facebook paths/handles and OTHER IP links; the Sheet failed to report an IP website on its row; 3 API cases expected 422 and got 200. All were before the code.
- Commit 2 mutations: replacing the domain regex with a dot check caused 8 failures; removing Facebook path checks caused 19; bypassing handle path checks caused 2; removing `/people/<name>/<id>`, changing profile-check order, dropping username hyphens, or requiring a letter at the start of each domain label each broke its corresponding acceptance test. All mutations were restored.
- Commit 3 tests-first: token tests passed before the Button change; the new ghost row-class assertion failed while the other 95 tests passed. Removing the classes failed that assertion; changing the light wash from 10% to 2% failed both fill-over-ground checks. Both mutations were restored.
- Commit 4 toast test: it passed cleanly in three runs before the setup fix; the teardown race did not reproduce locally. The temporary `./NoSuchPage` warm-up mutation failed Vite import analysis (one failed suite, no tests) and typecheck (TS2307); the real import was restored.
- API environment incident: after the first full API run, PostgreSQL was healthy again (`pg_isready`, `SELECT 1`, restart count 0), but a retry repeated the directory open-hours failures. The owner later restarted Docker; the branch and main targeted runs and the full branch API lane passed. The issue was environmental, not a code change.

## 5. Data count

Read-only counts on the local copy `masaha_cr_dev`; no contact data was changed.

| Source | Type | Total | Refused | Refused on deleted spaces | Refused values |
|---|---|---:|---:|---:|---|
| data | FACEBOOK | 1 | 0 | 0 | none |
| data | WEBSITE | 1 | 0 | 0 | none |
| self-test | FACEBOOK | 7 | 4 | 0 | n/a |
| self-test | OTHER | 3 | 1 | 0 | n/a |
| self-test | WEBSITE | 6 | 4 | 0 | n/a |

Self-test mismatches: 0 for every row.

## 6. Captures

Saved in `C:\Users\basel\Downloads\contact-rules-shots\`; each is 1440 × 900. Browser errors: `[]`.

- `row-hover-ar-light-1440.png`: row `rgb(221, 229, 237)`; trigger transparent; light, RTL.
- `ghost-hover-ar-light-1440.png`: trigger `oklab(0.236863 -0.00398637 -0.0131455 / 0.1)`; row `rgb(221, 229, 237)`; light, RTL.
- `menu-open-ar-light-1440.png`: same wash; `aria-expanded=true`; light, RTL.
- `row-hover-ar-dark-1440.png`: row `rgb(44, 49, 55)`; trigger transparent; dark, RTL.
- `ghost-hover-ar-dark-1440.png`: trigger `oklab(0.986198 -0.00252253 -0.00630087 / 0.08)`; row `rgb(44, 49, 55)`; dark, RTL.
- `menu-open-ar-dark-1440.png`: same wash; `aria-expanded=true`; dark, RTL.
- `ghost-hover-en-light-1440.png`: light wash; English, LTR.
- `ghost-hover-en-dark-1440.png`: dark wash; English, LTR.

All eight PNGs were opened and visually checked. The ghost wash differs from its hovered row in both themes; both menu captures show the menu open.

## 7. Problems met and how they were solved

- PROTOTYPE_SPLIT PR #147 remained open for 14 five-minute checks and merged at check 15 (`2026-11-15T13:55:44Z`). The pre-rebase backup was kept; rebase completed without conflicts, then lint and typecheck passed.
- Finding 219's toast race did not reproduce in three isolated pre-fix runs. The regression test and timer wait were retained as the plan directs.
- PostgreSQL memory pressure caused the first full API run and retry to fail on unrelated tests. The task was stopped and documented; after the supervisor cleared `heavy-slot-1` and the owner restarted Docker, the owner verified the targeted files and full API lane green without changing code.
- GitHub's latest issue/PR number advanced to 148 while preparing the PR. I created a new backup, changed Markdown references from 148 to 149, confirmed that rewrite changed only those references, and reran formatting and link checks. PR creation returned #149 as expected.
- A jsdom message, `Not implemented: navigation to another Document`, appeared during the full component lane; the lane passed all 2,152 tests.

## 8. Unexpected behavior

The toast teardown race was not reproducible locally, as noted above. The component lane printed the jsdom navigation message but finished green. The first API run and retry encountered PostgreSQL connection pressure; after Docker restarted, the owner reran the affected tests on both branches and the full API lane passed. No code changes were made to address that environment issue.

## 9. Early conflict check

At the check on 2026-11-16, `gh pr list --state open` listed only this PR (#149). There were no other open PR branches to fetch or compare with `git merge-tree`.

## 10. Departures from the plan

- The worktree was created with `--no-track`, as the plan's stated departure requires.
- Each unit's documents were committed with its code; the fifth commit waited until PROTOTYPE_SPLIT merged before changing the findings index and `foundation.md`.
- `check:classes` is `apps/web/scripts/checkClasses.ts`, as the plan notes.
- `toWesternDigits` moved to `packages/shared/src/core/digits.ts`, the plan's approved shared home.
- The owner directed adding finding 228 as an Open file and index entry in commit 5; it records the customers' partial Arabic-Indic phone suffix search behavior without fixing it. This adds one path, bringing the plan's 37 distinct files to 38.
- The first API failures triggered the required stop and report. The owner resumed on 2026-11-16 with verified green logs and directed continuation at §12.2 without rerunning full lanes. I used those logs and the green CI lane; no full test lane was rerun after resumption.

## 11. Observations for the owner

Finding 228 is fixed in this round: `customerSearch.ts` reads the term's digits through `toWesternDigits` before the digit test, and the desk's present search (`matchesPerson.ts`) does the same. The observation about the desk's search was acted on, not left for a later item.

## 12. Review fix round (2026-11-16)

New head: `23f79af37a7fd3932c3c3d2b75f8b8a04bfb742c` (full sha). The PR keeps five commits with their subjects; each fix folds into the commit it corrects via `git commit --fixup` then autosquash rebase onto `3a851690` (`origin/main`).

**Fix 1 — finding 217's quoted number (F1) → commit `docs: resolve findings 217, 218, 219, 225, 226`.**
- File changed: `docs/architecture/findings/217-contacts-and-every-phone-refuse-arabic-indic-digits.md`
- Change: `٠٥٩٩٧٧٧٧٨٨٨` (eleven digits) → `٠٥٩٩٧٧٧٨٨٨` (ten digits) on the Resolution line, matching what `ContactsSheet.component.test.tsx` types.

**Fix 2 — the untested link rows (F2) → commit `fix(spaces): accept only real links in contacts`.**
- File changed: `packages/shared/src/spaces/contacts.unit.test.ts`
- Added refusal rows: `WEBSITE javascript:alert(1)`; `FACEBOOK facebook.com/search/?q.x`, `facebook.com/events`, `facebook.com/share`, `facebook.com/reels`, `facebook.com/videos`, `facebook.com/posts`; `facebook.com/masaha/about`, `facebook.com/profile.php`, `notfacebook.com/masaha`. No change to `contacts.ts`; every row is already refused by the code.
- Breaks proved: removing `search` from the Facebook paths word list makes `/search/?q.x` fail; removing `events` makes `/events` fail. Both restored.

**Fix 3 — the untested phone rows (R2 trace) → commit `fix(shared): read Arabic-Indic digits in phones`.**
- File changed: `packages/shared/src/core/phone.unit.test.ts`
- Added rows: `00972599123456` → `+970599123456`; `022981234` → `+97022981234`; `+1 202 555 0100` → refused; `abc` → refused.

**Fix 4 — finding 219's test must be able to fail (F3) → commit `test(web): wait out toast timers, warm lazy routes`.**
- Files changed: `apps/web/src/test/toastRemoval.ts` (new), `apps/web/src/test/componentSetup.ts`, `apps/web/src/test/toastTeardown.component.test.tsx`
- Change: moved the wait from `componentSetup.ts`'s `afterAll` into exported helper `waitOutToastRemoval` in `toastRemoval.ts` (real timers, `TOAST_REMOVAL_MS + 100` ms, constant and comment moved with it); `afterAll` now calls `await waitOutToastRemoval()`. Rewrote `toastTeardown.component.test.tsx` to render, show, dismiss, await the wait, then assert the toast is gone from the document. Finding 219's Resolution line updated (folds into commit 5).
- Break proved: making `waitOutToastRemoval` resolve at once makes the test fail (toast still in the document); restoring the wait passes.

**Fix 5 — finding 228 fixed (C11) → commit `fix(shared): read Arabic-Indic digits in phones` and commit `docs: resolve findings 217, 218, 219, 225, 226`.**
- Commit 1 files changed: `apps/api/src/modules/customers/customerSearch.ts` (read digits through `toWesternDigits` before `/^\d{2,}$/`), `apps/api/src/modules/customers/customerSearch.unit.test.ts` (added `٥٦٧٨`, `۵۶۷۸`, `٠٥٩ ١٢٣` → phoneDigits, `أحمد` → name), `apps/web/src/features/occupancy/services/matchesPerson.ts` (desk's present search reads digits through `toWesternDigits`), `apps/web/src/features/occupancy/services/matchesPerson.unit.test.ts` (added `٠١` row), `docs/features/customers.md` (extended the `#149` change-log line).
- Commit 5 files changed: `docs/architecture/findings/228-customers-search-reads-a-phones-arabic-indic-last-digits-as-a-name.md` (Status → Resolved, Resolution line added), `docs/architecture/findings/README.md` (moved 228 from Open to Resolved).
- Breaks proved: removing `toWesternDigits(...)` from `searchTermsOf` makes the Arabic-Indic suffix rows fail; removing it from `matchesPerson` makes `٠١` fail. Both restored.
- Desk's present search: **changed**. `apps/web/src/features/occupancy/services/matchesPerson.ts` matched phone digits with Western-only logic (`/^\d{2,}$/` on `text.replace(SEPARATORS, '')`). Now reads `toWesternDigits(text.replace(SEPARATORS, ''))` before the test and `endsWith` comparison, and a test case `٠١` (Arabic-Indic for `01`) was added to `matchesPerson.unit.test.ts`.

**Breaks log of this round:** each break above (what was changed, which test failed, restored): Fix 2 (`search` → `/search/?q.x`; `events` → `/events`); Fix 4 (`waitOutToastRemoval` resolves at once → toast still present); Fix 5 (`toWesternDigits` removed from `customerSearch.ts` → `٥٦٧٨` row fails; from `matchesPerson.ts` → `٠١` row fails). All restored; every new row passes with its code.

**§4 verification on the final head (all through the grant script):**
- lint: passed
- typecheck: passed
- format:check: passed
- check:classes: passed — 1,990 files, no physical direction / arbitrary-value / selected-tint hover classes
- check:links: passed — 2,784 links in 226 documents and 2,690 source files all resolve
- check:conflicts: passed — no conflict markers found
- build (`NODE_ENV=production`): passed
- check:build: passed — no showcase code in 73 build files; 1,132 strings checked; table-row-scoped rule present in built CSS
- test:unit: passed — shared 29 files / 384 tests; API 77 / 924; web 196 / 1,403
- test:component: passed — 349 files / 2,152 tests
- test:api: passed — 126 files / 1,451 tests

**History check:** `git log --format=%B` on the five commits prints nothing for `Co-Authored|Generated with|fixup!`; `git grep -n "#PRNUM" -- docs` prints nothing. No tool attribution.

**CI result:** all 10 checks pass (`build`, `format:check`, `lint`, `check:classes`, `check:conflicts`, `check:links`, `test:component`, `test:unit`, `test:api`, `typecheck`; CodeRabbit skipped). `gh pr view 149 --json headRefOid,mergeStateStatus` shows `headRefOid` `23f79af37a7fd3932c3c3d2b75f8b8a04bfb742c` and `mergeStateStatus` `CLEAN`.

**Backup:** `backup/contact-rules-pre-review-fixes` left in place; `git diff backup HEAD --stat` lists only the 14 fix files.

**Servers / ports:** no server was started during this round; ports 3337 and 5337 were not used and are free.

**Unexpected:** none. Every temporary break reproduced its intended failure and restored cleanly.
