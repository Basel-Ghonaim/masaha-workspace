# GALLERY — the review fix round for PR #85 (a fresh Claude Code conversation)

You fix PR **#85** (`feat/space-gallery`, head `b40a69b8`) after its independent review. You did not
build it and you are not its reviewer. Work in `C:\Users\basel\masaha`. Read `CLAUDE.md`, then
**the review whole**: `C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\REVIEW85_CLAUDE_REPORT.md`, then only
the parts of the plan (`C:\Users\basel\.prompt\MASAHA_WORKER_A\PLAN\GALLERY_PLAN.md`) and of the code each
finding names. No plan mode; do not use the project's skills except `open-pr`'s checks if you wish.

## 1. Before anything

`git status --short` empty, branch `feat/space-gallery`, `git rev-parse --short HEAD` = `b40a69b8`. If
not, stop. **Verify each finding in the code before changing it**; if one is wrong, do not fix it — say
why in the report.

## 2. What to fix (the owner's decision: all of these, in this PR)

| Review # | Fix |
|---|---|
| 1 | A failed removal stays visible: the Delete action does not close the dialog before the answer (prevent Radix's default close; close on success only); the failure shows in the open dialog. |
| 2 | A second move/cover acts on the current list: await the photos' refetch (or block the tile's moves until it lands); the arrows use `aria-disabled` (AC 5), not `disabled`, so focus stays. |
| 3 | The upload's own timeout: `sendMultipart` passes a longer `timeout` for the multipart POST (state the value and why in a one-line comment, e.g. 120 s); the client's 15 s stays for everything else. |
| 4 | "Uploaded N of M" counts what actually uploaded, clears when the next selection starts (or when dismissed), and is announced (`role="status"`). |
| 5 | Leaving stops the queue: on unmount, no new upload starts and the one in flight is aborted (an `AbortSignal` passed through `sendMultipart` — production uses it, so it is no test-only parameter). Verify first that the queue really continues after unmount. |
| 6 | Write errors refresh the gallery: invalidate the photos key on 404/409; a photo already removed by someone else says so (one new line in both catalogues: «هذه الصورة حُذفت من قبل» / "That photo was already removed") instead of "the space was deleted"; `remove.reset()` in `ask` and `cancel`. |
| 7 | `makeCoverNamed` names the cover button; an upload 409 shows `galleryFull` and refetches; delete the unused `before` and `after` lines from both catalogues. |
| 8 | A read-only tile has an accessible name (`alt` = its label, or a visually hidden label). |
| 9 | The 409 order message is visible, not only `sr-only`, and says what happened (the gallery was refreshed), not "reload". |
| 10 | A transparent PNG becomes white, not black: fill the canvas white before `drawImage`; `fakeCanvas` records it. |
| 11 | «إضافة صور» is not disabled while an upload runs (only at ten, as planned); if you keep it unavailable, use `aria-disabled` and show the reason. |
| 12 | An upload failure with no `AppError` shows an upload sentence, not `loadFailed`. |
| Docs | `docs/features/spaces.md:19` ("photos are still API-only") corrected; the paragraph's claims made true by 1, 2, 9; the #85 history line says "documented", not "placed"; the curly apostrophe; finding 73's wording (the `Spinner` is the status); *Last Updated* on `overview.md` and `frontend/architecture.md`. Every new decision line ends `2026-10-17, #85`. |
| Nits (§17) | The deleted row's empty `BadgeList` on the phone card; `useLeaveGuard`'s unused `= false` default. |

Anything else in the review: leave it, and list it in the report as not done.

## 3. How — the owner's rules for this round

- **Tests:** each fix gets **one** test that proves it, written first and seen failing (record the red
  line). Where the review says a planned claim has no assertion (§13: the refetch after a move, after a
  409 and after a removal; the dialog's confirm path), add that assertion **only where your fix touches**.
  No new test for code you did not change.
- **Run only what your change touches:** the touched test files, focused —
  `npx vitest run --project unit <files>` / `npx vitest run --project component <files>` from `apps/web`.
  **Do not run the full `test:component` or `test:unit` lanes, nor `test:api`, nor `build`/`check:build`**
  unless you changed a file they alone cover; CI runs every lane on the push. Then `npm run lint`,
  `npm run typecheck`, `npm run check:classes`; `npm run format:check` and `npm run check:links` only if a
  document or a formatted file changed.
- **Commits:** new commits on top (the owner's rule for review fixes), at most three, grouped by area —
  e.g. `fix(web): give uploads their own timeout` and `fix(spaces): correct the gallery after review`;
  each subject counted ≤ 50; message written to a UTF-8 file, `git commit -F`; stage by path; no tool
  attribution. A fix to your own new commit before the push folds into it.
- `main` moved (#86 merged) but GitHub shows #85 `CLEAN`: **do not rebase**. Plain `git push`. If GitHub
  then shows a conflict: rebase on `origin/main` keeping both sides; documents only → `format:check`
  alone; code → lint and typecheck; `git push --force-with-lease`.
- No real run is needed unless a fix cannot be proven by a test; if you do one, the database is
  `docker start masaha-postgres-1`, never `db:up`.

## 4. Then

`gh pr checks 85` until green on the pushed head, and `CLEAN`. Post **one** PR comment "Review fixes"
listing each review number → fixed (commit) / not done (why). Append `## Review fixes` to
`C:\Users\basel\.prompt\MASAHA_WORKER_A\REPORT\GALLERY_REPORT.md`: the head, the commits with their
lengths, each fix with its red line, what you ran and did not run, and anything not done. Never merge.
