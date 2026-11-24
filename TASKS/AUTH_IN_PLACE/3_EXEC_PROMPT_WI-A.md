# WI-A — add ADR 0021 (documentation only): the executor's prompt

You are adding one Architecture Decision Record to the repository `C:\dev\masaha\app` (GitHub
`Basel-Ghonaim/masaha`) and opening its pull request. **Every text is given to you as a file: copy it, never retype
or reword it.** The owner approved these texts. Do exactly the steps below, in order, and nothing else.

## Hard limits
- Touch exactly two files in the repository: create `docs/architecture/decisions/0021-sign-in-where-the-action-is.md`,
  and add one line to `docs/README.md`. Nothing else.
- Stage by path only. Never `git add -A`, `git add .` or `git commit -a`.
- No tool attribution anywhere: no `Co-authored-by` trailer, no "generated with", in the commit or the PR.
- Never merge, never push to `main`, never force-push. The owner merges.
- If any step fails or anything differs from what this prompt expects, **stop and write what happened** in the
  report (last step) instead of improvising.

## The source files (in `C:\dev\masaha\workspace\TASKS\AUTH_IN_PLACE\WI-A\`)
- `0021-sign-in-where-the-action-is.md` — the ADR, the whole file.
- `readme-line.txt` — the one line for `docs/README.md`.
- `commit-message.txt` — the commit message (subject, blank line, body).
- `pr-body.md` — the pull request's description.

## Steps
1. In `C:\dev\masaha\app`: `git status` must be clean and on `main`. Then
   `git fetch origin` and `git switch -c docs/adr-0021 origin/main`.
2. Copy the ADR byte for byte:
   `Copy-Item 'C:\dev\masaha\workspace\TASKS\AUTH_IN_PLACE\WI-A\0021-sign-in-where-the-action-is.md' 'docs\architecture\decisions\0021-sign-in-where-the-action-is.md'`
3. **The date.** Line 3 of the new file reads `> **Status:** Accepted · **Date:** 2026-11-24`. If today is not
   2026-11-24, change only that date to today's (`YYYY-MM-DD`), nothing else on the line.
4. In `docs/README.md`, find the line that starts with
   `  - [0020](architecture/decisions/0020-design-archive-own-repository.md)` and insert the line of
   `readme-line.txt` **directly after it** (same two-space indent, the file's line endings unchanged). Then
   `git diff docs/README.md` must show exactly one added line and nothing removed.
5. Checks, from `C:\dev\masaha\app`, each must pass:
   - `npm run check:links`
   - `npm run check:conflicts`
   - `npm run format:check`
6. Commit:
   - `git add docs/architecture/decisions/0021-sign-in-where-the-action-is.md docs/README.md`
   - `git commit -F C:\dev\masaha\workspace\TASKS\AUTH_IN_PLACE\WI-A\commit-message.txt`
   - `git log -1 --format=%B` must equal the file's text, with no trailer added. `git show --stat HEAD` must list
     exactly the two files.
7. Push and open the pull request:
   - `git push -u origin docs/adr-0021`
   - `gh pr create --base main --head docs/adr-0021 --title "docs(adr): sign in where the action is" --body-file C:\dev\masaha\workspace\TASKS\AUTH_IN_PLACE\WI-A\pr-body.md`
8. Wait for CI, bounded: check `gh pr checks <number>` every 2 minutes, at most 15 times. A network error or "no
   checks reported" is not a failure: check again. When every check passes (a skipped one is fine), check
   `gh pr view <number> --json mergeStateStatus --jq .mergeStateStatus` (expected `CLEAN`).
9. Switch the checkout back: `git switch main` (leave the branch `docs/adr-0021` in place).
10. Write the report to `C:\dev\masaha\workspace\TASKS\AUTH_IN_PLACE\4_REPORT_WI-A.md`: the PR number and URL, the
    head commit's full sha, each check and its result, the merge state, the output of `git show --stat HEAD` (from
    step 6), whether you changed the date (step 3), and anything that did not go as written. Then stop.
