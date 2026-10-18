`main` did move: PR #40 merged after you cut the branch (main is now `1944f60`). It added its own
**finding 29** (the dev ports fixed for one folder), so #41 now conflicts with main in
`docs/architecture/findings.md` (GitHub: `DIRTY`). This is the conflict case of adjustment D, so
rebase.

1. `git fetch --prune origin`, then rebase `feat/admin-lookups-api` on `origin/main`.
2. In `findings.md`, keep main's finding 29 as it is and renumber yours (English names aren't
   unique) to **30**, in the amenities commit where it was added. Fix any link or mention of
   "finding 29" in your commits and in the PR description to say 30.
3. Checks: lint and typecheck on the head; then `test:api` and `build` + `check:build` on the head,
   one at a time (the rebase brings #40's web code under your branch; your code is unchanged).
4. Push with `--force-with-lease`; update the PR description (the new head, the base, finding 30).
5. Report once CI is green and GitHub shows `CLEAN`. Don't merge. No subagents.
