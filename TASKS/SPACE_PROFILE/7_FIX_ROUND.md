# SPACE_PROFILE — fix round on #138 (draft; sent only on the owner's word)

The Claude review of #138 (`C:\dev\masaha\workspace\TASKS\SPACE_PROFILE\6_REVIEW_CLAUDE_CODE.md`, head `54139379`)
says **mergeable after a fix round**. The supervisor confirmed F1–F4 in the code (F1: the vendored Radix listens for
Escape on `document` in the capture phase). Read the review whole, then fix **F1–F9**, all folded into the one commit.

- **Method:** `git branch backup/space-profile-1` first; fixes as `git commit --fixup=HEAD~0` then
  `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash origin/main` (one commit at the end). Only `docs/design/`; stage
  by path; no tool attribution.
- **F1** Escape during a keyboard move cancels the move, not the Sheet. **F2** the hours Sheet compares with the copy
  taken at opening. **F3** `Owner settings.html` links to `Owner space profile.html?sheet=prices#prices`
  («الأسعار المعلنة»). **F4** «إدارة قائمة المرافق» goes through `close(then)`. **F5** Packages reads the profile's
  shifts (`?demo=shifts` there too). **F6** a CHANGES line (the pin moves by a second tap; dragging is the production
  map's). **F7** hide/delete in the top bar for `id=new`, or the reason in CHANGES. **F8** CHANGES' Refactor 2 table
  one row per decision. **F9** each custom-hours day a `fieldset` with its `legend`. Also check the phone anchors'
  `scroll-margin-top` (the review's "also seen").
- **Verify:** both checks (`check-parse`, `check-classes`); the browser at 390/768/1024/1440 × ar/en × light/dark for
  each touched state, F1/F2/F4 by hand; Space details still works; screenshots to Downloads\space-profile-shots.
- `git push --force-with-lease`; the PR description gains a "Review fixes" section; CI green, `CLEAN`; print the new
  full head sha and stop. Never merge.
