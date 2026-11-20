# CONTACT_RULES — the fix round of PR #149 (OpenCode)

You fix every point the review of PR #149 found, run every check, push, and report. **You start with no context:
this file is everything you need.** Read it whole before you run anything. Work alone, without sub-agents, and load
no skill — this file replaces the project's skills (the owner's decision C11). `CLAUDE.md`'s rules still bind you.

## 0. The situation

- Repository folder (a git worktree): **`C:\dev\masaha\app-cr`**, branch **`fix/contact-rules`**, PR **#149**, head
  **`a28f74dfce93bfc5900db2ccbdbfdde96ac4f976`**, CI green, `CLEAN`. Its databases: `masaha_cr_dev` / `masaha_cr_test`
  (already in its `apps/api/.env`); its ports: API 3337, web 5337. Docker's PostgreSQL is up (port 5433).
- Its five commits, oldest first:
  1. `840a7c2b fix(shared): read Arabic-Indic digits in phones`
  2. `1873382b fix(spaces): accept only real links in contacts`
  3. `c93b2afc fix(design-system): wash a row's ghost control`
  4. `afea0331 test(web): wait out toast timers, warm lazy routes`
  5. `a28f74df docs: resolve findings 217, 218, 219, 225, 226`
- Task folder: `C:\dev\masaha\workspace\TASKS\CONTACT_RULES\`. Read `0_OWNER_DECISIONS.md` (C1–C11; C11 is this
  round) and `7_REVIEW.md` (the review). `2_PLAN.md` and `4_REPORT.md` only to look something up.
- You are the only worker on the machine; about 7 GB of memory is free.
- **The shell is Windows PowerShell 5.1:** no `&&` / `||` — one command per call, or `;`. Paths with backslashes.
- **Every heavy command goes through the machine's grant script** (lint, typecheck, any test, build):
  `$H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr <command>` from `C:\dev\masaha\app-cr`.
  If it waits for memory, let it wait; exit code 75 = no grant → stop and report.

## 1. Hard limits

- Never merge, never push to `main`, never create an Issue, never touch `C:\dev\masaha\app` or any other worktree.
- The only force-push allowed: `git push --force-with-lease origin fix/contact-rules`.
- Stage by path only; never `git add -A`, `git add .`, `git commit -a`.
- **Fixes fold into the commit they correct** (`git commit --fixup=<sha>`, then an autosquash rebase, §3). No new
  "fix" commits; the PR keeps five commits with their subjects.
- No migration, no seed change, no data written beyond the test database. Never weaken or delete a test.
- **No tool attribution** anywhere (no `Co-authored-by`, no "Generated with", no tool name) — commits, PR, comments.
- **No-stop rule:** work through to the end. Stop only for: a check that fails twice after your fix, exit 75 from the
  grant script, a rebase conflict, or something this file does not cover. A test lane killed for memory: retry once,
  then record it and go on (CI judges it).
- **Lint, typecheck and `format:check` after every fixup commit**, before the next one.

## 2. The fixes

Each says which commit it folds into. Before each, read the code it names at the current head.

### Fix 1 — finding 217's quoted number (review F1) → commit 5 (`a28f74df`)

`docs/architecture/findings/217-contacts-and-every-phone-refuse-arabic-indic-digits.md`, the **Resolution** line
says the Sheet sends `+970599777888` for `٠٥٩٩٧٧٧٧٨٨٨` — that is **eleven** digits, which the rule refuses. Replace
`٠٥٩٩٧٧٧٧٨٨٨` with `٠٥٩٩٧٧٧٨٨٨` (ten digits: ٠ ٥ ٩ ٩ ٧ ٧ ٧ ٨ ٨ ٨), the value
`apps/web/src/features/spaces/components/contacts/ContactsSheet.component.test.tsx` actually types (check it there).
Nothing else on the line changes.

### Fix 2 — the untested link rows (review F2) → commit 2 (`1873382b`)

In `packages/shared/src/spaces/contacts.unit.test.ts`, add these inputs to the existing **refusal** tests (the same
`it.each` / `one(...)` style already there; expect the same invalid result the neighbouring rows expect):

- WEBSITE: `javascript:alert(1)`
- FACEBOOK, one path segment each: `facebook.com/search/?q=x`, `facebook.com/events`, `facebook.com/share`,
  `facebook.com/reels`, `facebook.com/videos`, `facebook.com/posts`
- FACEBOOK: `facebook.com/masaha/about` (decision C10: a page's tab is refused, not shortened),
  `facebook.com/profile.php` (no id), `notfacebook.com/masaha`

Do not change `contacts.ts`: the review traced every one of these as already refused. If one is **not** refused when
you run the test, stop and report (that would be a real defect, not a test to adjust).

**Prove each new row can fail** (record each in the report's Breaks log, then restore): remove `search` from the
Facebook paths word list in `contacts.ts` → the `/search/?q=x` row fails; remove `events` → the `/events` row fails.

### Fix 3 — the untested phone rows (the review's R2 trace) → commit 1 (`840a7c2b`)

In `packages/shared/src/core/phone.unit.test.ts`, add rows in the existing style:

| Input | Expected |
|---|---|
| `00972599123456` | `+970599123456` |
| `022981234` | `+97022981234` |
| `+1 202 555 0100` | refused |
| `abc` | refused |

If a result differs, stop and report — do not change `phone.ts` to fit.

### Fix 4 — finding 219's test must be able to fail (review F3) → commit 4 (`afea0331`)

Today `apps/web/src/test/toastTeardown.component.test.tsx` passed before the fix too, so it proves nothing. Make the
wait testable:

1. Move the wait out of `apps/web/src/test/componentSetup.ts`'s `afterAll` into a named, exported helper in a new
   test-support file `apps/web/src/test/toastRemoval.ts`: `export async function waitOutToastRemoval(): Promise<void>`
   — it switches to real timers (`vi.useRealTimers()`) and waits `TOAST_REMOVAL_MS + 100` ms, exactly as the current
   `afterAll` does (move the constant and its comment with it). `componentSetup.ts`'s `afterAll` keeps its
   `if (!drewToast) return;` and then calls `await waitOutToastRemoval();`. Behaviour is unchanged.
2. Rewrite the test so it **fails without the wait**: render `<Toaster label="Notifications" />`, show a toast
   (`toast('Saved')` in `act`), find it, dismiss it (`toast.dismiss()` in `act`), then
   `await act(async () => { await waitOutToastRemoval(); });` and assert the toast is **gone from the document**
   (`expect(screen.queryByText('Saved')).not.toBeInTheDocument()`). Keep the file's header comment, reworded to say
   what it now proves: the helper outlasts the library's removal timer, so the setup's wait leaves no timer running.
3. **Prove it can fail:** make `waitOutToastRemoval` resolve at once (no timer) → the test must fail (the toast is
   still in the document); restore. If it passes even then, stop and report. Record the break.
4. Update finding 219's **Resolution** line (in commit 5's file, so that edit folds into **commit 5**): replace the
   sentence about the race not reproducing and CI being its evidence with what is now proved — the setup's wait is
   the helper `waitOutToastRemoval` (`apps/web/src/test/toastRemoval.ts`), and
   `toastTeardown.component.test.tsx` shows a dismissed toast is removed within it, and fails if the helper does not
   wait. Keep the rest of the line.

These files are test support (`apps/web/src/test/`), not production code.

### Fix 5 — finding 228: a phone's last digits in Arabic-Indic digits (C11) → commit 1 (`840a7c2b`) and commit 5

The owner decided to fix it in this round (C11 overrides C10). Today
`apps/api/src/modules/customers/customerSearch.ts` (`searchTermsOf`) strips separators and tests `/^\d{2,}$/`, and
JavaScript's `\d` reads Western digits only, so `٥٦٧٨` is searched as a name.

1. In `searchTermsOf`, read the term's digits through the shared reader before the digit test:
   `const digits = toWesternDigits(q).replace(/[\s+\-.()]/g, '');` — import `toWesternDigits` from
   `@masaha/shared/core` (where it lives since this PR; check the export). `{ name: q }` still gets the original `q`.
   Update the function's doc comment: a term of digits, Western, Arabic-Indic or Eastern, searches the end of a phone.
2. Tests: find the existing unit tests of `searchTermsOf` (`git grep -n searchTermsOf -- apps/api/src`) and add, in
   their style: `'٥٦٧٨'` → `{ phoneDigits: '5678' }`; `'۵۶۷۸'` → `{ phoneDigits: '5678' }`; `'٠٥٩ ١٢٣'` →
   `{ phoneDigits: '059123' }`; and a name with Arabic letters (e.g. `'أحمد'`) still → `{ name: 'أحمد' }`.
   **Prove it can fail:** remove `toWesternDigits(...)` from that line → the Arabic-Indic rows fail; restore.
   If an API test of the customers' list search exists (`customers*.api.test.ts`, search for `q=`), add one case:
   a customer with phone `+970599123456` is found by `q=٣٤٥٦`.
3. **The desk's search of the people present:** find how the desk search's first group (the people present) matches
   the typed term (start at `apps/web/src/features/desk/components/search/DeskSearch.tsx`, `present.group(term, …)`,
   and follow it). If it matches phone digits with Western-only logic (`\d`, `/[0-9]/`, digit comparison), read the
   term through `toWesternDigits` the same way and add a test case with Arabic-Indic last digits. If it only uses the
   API's search (already fixed by step 1) or matches names only, change nothing and say so in the report, with the
   file and line that show it.
4. Documents — fold into **commit 5**: finding 228's file → `**Status:** Resolved`, add its **Resolution
   (2026-11-16, #149):** line saying what the code now does and which tests prove it (the style of 217's line); in
   `docs/architecture/findings/README.md`, move 228's line from **Open** to **Resolved** (same format as its
   neighbours there). `docs/features/customers.md`'s `2026-11-15, #149` change-log line (it says a whole phone in
   Arabic-Indic digits is searched as a phone) → extend it: and a phone's last digits so typed search the end of the
   phone (finding 228). Find which commit holds that line (`git log --format=%h -- docs/features/customers.md` on the
   branch) and fold into that one if it is not commit 5.

## 3. How to fold the fixes (do this exactly)

```powershell
cd C:\dev\masaha\app-cr
git status --short
git fetch origin
git branch backup/contact-rules-pre-review-fixes
```

`git status --short` must print nothing first. Then, for each fix: edit, run its own tests through the grant script
(the touched test files, e.g. `node $H cr npx vitest run <file>` from the package folder, or the lane with a file
filter), then lint + typecheck + format:check, then:

```powershell
git add <each changed path>
git commit --fixup=<the sha of the commit it folds into>
```

When all fixups are made, squash them into their commits **without changing the base** (the PR is `CLEAN`; do not
rebase onto the new `main`):

```powershell
$base = git merge-base HEAD origin/main
git -c sequence.editor=: rebase -i --autosquash $base
git log --format='%h %s' "$base..HEAD"
```

The log must show exactly the five subjects of §0, in order, and no `fixup!`. A conflict: `git rebase --abort`, stop
and report. Compare the result with the backup: `git diff backup/contact-rules-pre-review-fixes HEAD --stat` must
list only the files the fixes touched.

## 4. Verification on the final head (all, one at a time, through the grant script)

```powershell
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run lint
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run typecheck
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run format:check
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run check:classes
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run check:links
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run check:conflicts
Set-Location C:\dev\masaha\app-cr; $env:NODE_ENV = 'production'; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run build; Remove-Item Env:NODE_ENV
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run check:build
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run test:unit
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run test:component
Set-Location C:\dev\masaha\app-cr; $H = 'C:/dev/masaha/workspace/TASKS/IDENTITY/scripts/heavy.mjs'; node $H cr npm run test:api
```

Record each result with its counts (files, tests). All must pass. Then the history check:

```powershell
git log --format=%B "$base..HEAD" | Select-String -Pattern 'Co-Authored|Generated with|fixup!'
git grep -n "#PRNUM" -- docs
```

Both must print nothing.

## 5. Push, the PR, CI

```powershell
git push --force-with-lease origin fix/contact-rules
```

1. Write `C:\dev\masaha\workspace\TASKS\CONTACT_RULES\scripts\review-fixes.md` — one comment, in this shape, no tool
   name:
   ```
   ## Review fixes
   Folded into their commits (head <new full sha>):
   - F1 — finding 217's quoted number corrected (docs: resolve findings…)
   - F2 — the untested link rows tested: <list> (fix(spaces)…)
   - Phone rows tested: 00972…, 02 landline, +1 with spaces, letters (fix(shared)…)
   - F3 — finding 219's test now fails without the wait: <how> (test(web)…; finding 219's resolution updated)
   - Finding 228 fixed (the owner's decision): <what>; the desk's present search: <changed / unchanged, why>
   Verification: <each check and lane with its counts>.
   ```
   Then: `gh pr comment 149 --body-file C:\dev\masaha\workspace\TASKS\CONTACT_RULES\scripts\review-fixes.md`
2. Update the PR description to the final state: `gh pr view 149 --json body --jq .body > <scratch file in the task
   folder's scripts\>`, edit only what changed (finding 228 now resolved in the summary / scope lines; the Evidence
   counts), then `gh pr edit 149 --body-file <that file>`.
3. Wait for CI, bounded: `Start-Sleep -Seconds 300; gh pr checks 149` — at most 12 times. Then
   `gh pr view 149 --json headRefOid,mergeStateStatus` must show `CLEAN` and your head. A red check: read
   `gh run view <id> --log-failed`, fix it in the commit that caused it (fixup + the same autosquash), rerun that check
   locally, push with `--force-with-lease`, wait again — at most two such rounds; a third red: stop and report.

## 6. The report

Add a section **"Review fix round (2026-11-16)"** at the end of
`C:\dev\masaha\workspace\TASKS\CONTACT_RULES\4_REPORT.md`: the new head (full sha); each fix (1–5) with the files
changed and the commit it folded into; the Breaks log of this round (each break: what you changed, which test failed,
restored); Fix 5 step 3's finding about the desk's present search, with file and line; every check of §4 with its
counts; CI's result and `mergeStateStatus`; anything unexpected. Leave the backup branch in place. Stop any server you
started, by PID, and check ports 3337 / 5337 are free. Then stop. **Never merge.**
