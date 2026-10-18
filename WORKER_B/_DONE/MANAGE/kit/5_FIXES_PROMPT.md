# MANAGE — review fixes (send to the **execution** conversation, not a new one)

Read the review report(s) for this PR in `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\` (`REVIEW_MANAGE_*_REPORT.md`). Verify each
finding against the code before changing anything; push back with reasons where one is wrong.
- **Small fixes** (the owner's rule): a new commit on top (subject ≤ 50, counted), tested only where it
  touches (that test file, then lint and typecheck); a plain `git push`; CI runs every lane.
- **Larger fixes:** fold each into the commit it corrects (fixup + autosquash), run the plan's local
  verification again, `git push --force-with-lease`.
- If `main` moved and GitHub shows a conflict: rebase, keep both sides; documents only → `format:check`
  alone; code → add lint and typecheck.
- Then: wait for CI on the pushed head and `CLEAN`; post **one** "Review fixes" comment on the PR; add a
  "Review fixes" section to `C:\Users\basel\.prompt\MASAHA_WORKER_B\REPORT\MANAGE_REPORT.md`. Never merge.
