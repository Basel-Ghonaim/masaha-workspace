# MEDIA — review fixes for PR #77 (one round, with the rebase)

Two independent reviews of head `9bc0b70`: OpenCode accepted it with no finding
(`REPORT\REVIEW77_OPENCODE_REPORT.md`); Copilot asked for three changes
(`REPORT\REVIEW77_COPILOT_REPORT.md` — read it). The analyst checked each in the code. Meanwhile
`main` moved (#74, #75 merged): the PR is `DIRTY`, in documents only. One push does both.

Follow `receiving-code-review` as workflow §10 adapts it: verify each item before changing anything.
Fold each fix into the commit it corrects (fixup + autosquash); every subject stays ≤ 50.

## 1. Rebase (the fast path, workflow §9 *Conflicts*)

`git fetch --prune origin`, `git rebase origin/main`; keep both sides in the documents (`spaces.md`,
the findings index, the overview, and whatever else conflicts there); a conflict in code adds `lint`
and `typecheck`. If a conflict reaches code beyond a trivial keep-both, stop and say so.

## 2. Fix

1. **`overwrite: 'false'` on the Cloudinary upload** (Copilot 1, true: Cloudinary's default
   overwrites, and the port promises a key is never written twice; your plan's D1 named it). Add it to
   the signed parameters of `put` in `shared/storage/cloudinaryStorage.ts`, and assert it in the
   adapter's unit test (the signed fields and the signature).
2. **`asset_folder` on the Cloudinary upload** (Copilot 2, true: the owner's account was created in
   2025, so it most likely uses dynamic folders, where the `public_id`'s path does not place the asset
   in a folder; your plan's D1 named it). Add `asset_folder` = the key's folder under
   `masaha/<env>/…` to the signed parameters, assert it in the unit test, and **in the real run read
   the upload's answer**: its `asset_folder` is the folder you sent (say in the report what the
   account answered, which tells its folder mode). Delivery URLs do not change.
3. **Push back on Copilot 3** (the local adapter ignores `contentType`): conventions' storage line
   says a key's extension names its type, and the local handler serves by it, as Cloudinary's URL
   does. Do not change the adapter; add one sentence to the port's `StoredFile` comment that the
   content type must agree with the key's extension, and give this reason in the "Review fixes"
   comment.

## 3. Then

- **Verify:** `test:unit`, `test:api` (first check that worker B in `masaha-b` runs no lane), `lint`,
  `typecheck`, `format:check`, `check:links`; a real upload and removal against Cloudinary
  (`STORAGE_MODE=cloudinary`, the URL by its shape only, never printed), the answer's `asset_folder`
  checked, the file in the folder in the account, then removed.
- **The 18 test files** in Cloudinary's `masaha/development/` from your first real run, and this
  run's: remove them (by their keys, through the adapter or the API), and say so in the report. The two
  test spaces in `masaha_media_dev` stay; the database goes with the worktree after the merge.
- `git push --force-with-lease`; wait for CI on the pushed head and `CLEAN`.
- One **"Review fixes"** comment on #77 (the rebase, 1, 2, and 3 pushed back with its reason); update
  the PR description to the final state; a "Review fixes" section in `REPORT\MEDIA_REPORT.md`.
- At the report, `git merge-tree --write-tree` against #78 (documents expected; say which). Never
  print a secret. Don't merge. Stop every background shell you start.
