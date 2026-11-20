# SPACE_PROFILE — fix round on #143 (PR-C, the space profile) — approved by the owner 2026-11-12

You are a **Claude Code fixer** on **Masaha**, starting with an empty context, in **`C:\dev\masaha\app`** on branch
**`feat/space-profile`** — **PR #143**, head **`29a25054cca12d714bb2ede8e83dbf47dd13be07`**, five commits, CI green,
`CLEAN`, not merged. A Claude review says **mergeable after a fix round**; the main supervisor verified **all ten
findings** in the code; the owner approved fixing them all now, as recommended. **Model Opus 5.5, effort high.** No
stop until the report, unless a stop rule of `docs/development/workflow.md` §8 says so.

## Read first

1. `CLAUDE.md`; `docs/development/workflow.md` (§3 commits, §5 Definition of Done, §8 stop rules); `testing.md`
   (§3's rules — seen failing, name the break, make the break).
2. **`C:\dev\masaha\workspace\TASKS\SPACE_PROFILE\6_REVIEW_PR-C.md` whole** — each finding's place, scenario and fix.
3. `C:\dev\masaha\workspace\TASKS\SPACE_PROFILE\0_OWNER_DECISIONS.md` — the last section, **FR1–FR4** (binding); and
   DI-1, DI-3 and DI-4 in `C:\dev\masaha\workspace\TASKS\SPACE_PROFILE\2_PLAN_PROD.md` (search `DI-`).
4. `C:\dev\masaha\workspace\TASKS\SPACE_PROFILE\4_REPORT_C.md` — what the first executors ran and how.

## The fixes (each folded into the commit named; each new or changed test **seen failing first** at the old code)

The commits: C1 `549c1918` (lookups), C2 `f7a3414b` (the profile), C3 `1ba8748c` (drag), C4 `f719d2c5` (the admin's
top bar), C5 `29a25054` (prices).

- **F1 (blocker) → C2.** A Sheet that unmounts while it has changes reports "no changes" (the cleanup main's
  `useSectionFrame` had); the editor drops an open Sheet whose section can no longer be edited (`!editable`, or the
  space gone); the leave guard never blocks with no dialog to answer it (draw `LeaveDialog` in every state, or reset
  the guard when not ready — choose, say which). Tests: **(a)** a changed Sheet's save answered 404, after which a
  link to another page lands; **(b)** a 403 after which leaving the page does not ask; the focus after the refusal
  lands somewhere sensible (assert it). Correct `EditSheet.component.test.tsx`'s test whose title claims words it
  does not assert.
- **F2 → C2.** «عن المساحة» / «الموقع» compare with the values the Sheet **opened on** (set where it resets), and
  send only their own part's fields. A T33 variant: open, the space read again with another field changed, save —
  the body holds the typed field only. **FR3:** the hours' and the shifts' Sheets take the other half of their group
  from the **latest read at the save** (`useHoursSheet`, `useShiftsSheet`), with a test each (the other half changed
  by a read while the Sheet is open; the body carries the new other half). Make the docstrings and
  `docs/features/spaces.md` say exactly what is sent.
- **F3 → C1 and C2.** `AreaLine` on the public source, once the catalogue has loaded and holds no such area, writes
  the kept wording (the one the area field uses for a hidden area); the header drops its `·` when the line is empty.
  A test with a hidden area on the public source; `lookups.md` corrected where it says "nothing".
- **F4 → C2.** The own-amenity clash is checked against what the checklist **offers** (`isActive`, or held by the
  space) — `isActive` gains its production reader. The retired case in the unit or Sheet test.
- **F5 → C2 (FR2, option (a)).** `unsaved` leaves the owners' slot (`OwnedSpace` / `OwnersSlot`) and `space-links`
  loses its hold: the hook's lines, the `unsavedReason` copy in **both** catalogues, the test that reached it,
  `docs/features/space-links.md` (the lines the review names, ~104 and ~201) and `spaces.md`'s decision line. Grep
  that nothing names them after.
- **F6 → C2.** With a space without hours: «الورديات»'s «أضف ساعات العمل» opens «تعديل ساعات العمل»; the prices
  Sheet's «أضف وردية» does the same. Correct the misleading title in `HoursSheet.component.test.tsx`. Make the break
  the review names (`'hours'` → `'shifts'`) and see both fail.
- **F7 → C2.** The test titles that claim more than they prove; the assertion that cannot fail; the stray
  `restoreTransport()`; the letter tile asserted; the 403 and 404 tests each assert their own state's title (so a
  swap fails).
- **F8 → C2.** A landmark shown in the other language gets its `lang` and is isolated, as the addresses are.
- **F9 → C2 (FR4).** A failed gallery read no longer leaves «اكتمال الملف» and the index as skeletons for good, nor a
  failed catalogue read «المرافق»: after a failure, say it (both languages) with the retry the page already offers —
  choose the smallest change that tells the truth, say which. A test for each.
- **F10 → C4 and C5.** The phone menu's items while an action waits: **marked, never disabled** (as `spaces.md` and
  the docstring say), with a test that the item stays reachable; `fieldSections.ts`'s comment and
  `data-reports.md`'s notice paragraph say the notice is **inside** its section.
- **Finding 219 → C2 (FR4).** Record it, **Open**: "A toast's removal timer can outlive its test file's jsdom" — CI's
  first `test:component` run on #143 (`useDeleteSpace.component.test.tsx`, `ReferenceError: window is not defined`
  after all tests passed; green on re-run). Check the index first (216–218 exist); add its index line.

No new scope: nothing beyond these fixes, no drive-by refactor. Where the review's recipe is wrong, fix the defect
correctly and say why.

## Method

- **`git branch backup/space-profile-5` first.** Fixes as `git commit --fixup=<commit>`, then
  `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash $(git merge-base HEAD origin/main)` — **keep the base**
  (`93fe4105`; GitHub says `CLEAN`, and the project rebases only a dirty PR). Five commits after, no `fixup!` left,
  subjects unchanged (≤ 50), bodies updated where a commit now does more. Stage by path; never `git add -A` / `.`;
  no tool attribution.
- A break for "seen failing": make it in the code, see the test fail, restore **from a `cp` backup** (never
  `git checkout -- <file>`).

## Verification (complete, before the push)

- `lint` and `typecheck` on **each of the five commits** after the autosquash (one command at a time, back on the
  branch after each); `format:check`; `check:classes`, `check:links`, `check:conflicts`; `NODE_ENV=production npm run
  build` then `check:build`; `test:unit` and `test:component` **in full** on the head. `test:api` may be left to CI:
  this round changes no API code — say so in the PR.
- **Memory is short** (1–3 GB free; another session is planning in `app-design`): one heavy command at a time. A
  lane killed for memory: **retry once; if killed again, CI judges** — said in the PR and the report.
- **A real run** of F1 and F3 on the throwaway **`masaha_wi142_dev`** (API on 3342, web on 5342, as `4_REPORT_C.md`
  did; **never `masaha_dev`, never `db:seed`**). Named writes, that database only: the admin deletes a space in a
  second tab while the first has a changed «عن المساحة» open, then saves → the 404 page, and a sidebar link leaves
  it; the admin hides an area a space holds → the owner's header and «الموقع» name it with the kept wording.
  Screenshots to `C:\Users\basel\Downloads\wi143-fix-shots\`, curated, never pushed. Stop your servers by PID and
  check the ports free.

## Then

`git push --force-with-lease`; the PR description gains a **"Review fixes"** section (each F with its commit and
test, FR1–FR4, finding 219, what was not run); wait for CI green on the new head and `CLEAN` (a failure the round did
not cause: re-run once, then report). Append a **"Fix round"** section to
`C:\dev\masaha\workspace\TASKS\SPACE_PROFILE\4_REPORT_C.md`: the **new full head sha**, each fix and its test (and
the break that made it fail), the choices you made (F1's guard, F9's wording), what was run, anything unexpected.
Then stop. **Never merge, never delete a branch.**
