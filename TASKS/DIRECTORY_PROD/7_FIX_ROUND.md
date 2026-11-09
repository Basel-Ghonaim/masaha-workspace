# DIRECTORY_PROD — fix round on #139 (draft; sent only on the owner's word)

The Claude review of #139 (`C:\dev\masaha\workspace\TASKS\DIRECTORY_PROD\6_REVIEW_CLAUDE_CODE.md`, head `e1838447`)
says **mergeable after a fix round**. The supervisor confirmed F1, F2 and F4 in the code; F3 matches the test at the
head. Read the review whole, then fix **F1–F7**, each folded into the commit the review names.

- **Method:** `git branch backup/directory-filters-2` first; each fix as `git commit --fixup=<sha>`; then
  `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash origin/main`; F7 is a reword of commit 5's body (one sentence:
  finding 215, OD7 b). Stage by path; no tool attribution; no fix commits left.
- **F1:** word the card's price by the period of the answer on screen (or no price while `isPlaceholderData` with a
  changed period) + the hook test: DAY answered, MONTH pending → no card says «/ شهر» over a DAY price. Seen failing
  first.
- **F2:** the prototype's R8 rule must reach the results' wrapper at 1024–1279 (check `Directory.html` at 1100 and
  1300 px in the browser).
- **F3:** T14 — give «Stale Verified» and «Fresh» a student price; assert `studentPrices=true` equals exactly
  `['Fresh', 'Stale verified']` by hand; break it once (`prices_updated_at >= cutoff`) and see it fail.
- **F4:** ADR 0008 line 16 back as first written; the *Revised* line carries the change.
- **F5:** `Math.max(1, …)` for the lowest placeholder; the test expects `'1'`.
- **F6:** drop `HOURS_STATUSES` (a plain union type) or keep it only if read; drop `export` from `DIRECTORY_PAGE_SIZE`
  and `cardStatusOf` if nothing outside reads them.
- **Verify:** lint, typecheck, format:check, check:* , build + check:build; `test:unit` and `test:component` in full
  (one at a time), `test:api` in full. A lane killed for memory: retry once, then CI judges.
- `git push --force-with-lease`; the PR description gains a "Review fixes" section; CI green on the new head,
  `CLEAN`; update `4_REPORT.md` (new head, the fixes, the commands). Then stop. Never merge.
