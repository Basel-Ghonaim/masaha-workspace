# PACKAGES — the review fix round for PR #87

Send this to the **execution conversation** if it is still open; otherwise a fresh one reads, first,
`2_PLAN.md`, `3_EXEC_PROMPT.md` (its rules all hold: §2's stop rule, §5's final reply) and `4_REPORT.md`.

Read the review whole: `D:\masahaWorkspace\WORKER_B\PACKAGES\6_REVIEW_CLAUDE_CODE.md`. The analyst verified
findings 1–3 in the code. Work in `C:\Users\basel\masaha-b` on `feat/space-packages`; first check the head
is `9567da9a`, the tree clean, `origin/main` still `5e8c979d` (if `main` moved, say so before anything).

## What to fix (the owner's decision) — every change folds into the commit it belongs to

1. **The edit's lock and permission get their tests** (review 1), in C4's `packages.api.test.ts`, on
   `whileHeld` as T9/T10 do: *a PATCH by an owner unlinked while it waited for the space's lock is refused
   (403), and writes nothing*; *a PATCH while the space is deleted meanwhile answers 404, and writes
   nothing*. Each seen red first by its break, recorded: `update` without `lockFor` (both red), and
   `lockFor`'s `can` on `space.links` instead of the links read under the lock (the first red). Restore from
   a backup, never `git checkout`.
2. **Every commit gets its body** (review 2): one or two lines saying **why**, under each of the four
   subjects (subjects unchanged).
3. **`docs/README.md:18`** (review 3): the `spaces.md` line's em dash `—` restored (fold into C2).
4. **Nits, all folded:** the overview's Packages line placed **after** the Spaces line (C4's or C2's,
   wherever it was written); the test at `packages.api.test.ts:495` asserts the order or the places, not
   consecutive ids; the contract's §4 full stop mid-list (line 64) fixed; `written`'s comment names both
   cases (the name's key and the shift's key).
5. **Record finding 81** (C4, in finding 63's format, and the index): *a retired package that keeps its
   shift stops the owner from removing that shift* — evidence: the shifts' save answers 409 while any
   package names the shift, retired or not; the way out is clearing the shift on the retired package;
   *resolves when* the owner's packages screen says so, or retiring a package clears its shift (decide
   there). One line in `docs/features/packages.md`'s behaviour saying the same.
6. **`4_REPORT.md`:** remove the sections left over from the R6 stop and the pre-rewrite id `edcb9dc4`
   (keep the departure that records the stop); then append `## Review fixes`.

## How

- **Folding:** `git commit --fixup=<sha> -- <paths>` for each change, then
  `$env:GIT_SEQUENCE_EDITOR=':'; git rebase -i --autosquash 5e8c979d; Remove-Item Env:GIT_SEQUENCE_EDITOR`.
- **The bodies, after the fold, in Git Bash:** write `$TEMP/packages-msg/msg.py` (outside the repository): it
  reads a message on stdin, and when its first line is one of the four subjects and it has no body, prints
  the subject, a blank line and that commit's body; otherwise prints the message unchanged. UTF-8, no BOM,
  real line breaks. Then
  `git filter-branch -f --msg-filter 'python -I "$TEMP/packages-msg/msg.py"' 5e8c979d..HEAD`, then
  `git for-each-ref --format='%(refname)' refs/original/ | xargs -r -n1 git update-ref -d`. Check with
  `git log --format='%h %s%n%b' 5e8c979d..HEAD`: four subjects as before (count them), each with its body,
  no BOM, no literal `\n`, no tool attribution.
- **What to run (the owner's rule: only what the changes touch):** `git rebase -x "npm run lint && npm run
  typecheck" 5e8c979d`; the focused `npm run test:api -w @masaha/api -- src/modules/packages/packages.api.test.ts`;
  `npm run format:check`; `npm run check:links`. **Not** the full `test:unit` / `test:api` lanes (no code
  outside the test file changed; CI runs every lane). If a command cannot run: stop (`3_EXEC_PROMPT.md` §2).
- `git push --force-with-lease`; `gh pr checks 87` until green on the new head; `CLEAN`; one PR comment
  "Review fixes" listing review 1–3 and the nits → fixed (commit) / not done (why).

## Your final reply

`3_EXEC_PROMPT.md` §5's shape, with the new head and the four commits' new ids.
