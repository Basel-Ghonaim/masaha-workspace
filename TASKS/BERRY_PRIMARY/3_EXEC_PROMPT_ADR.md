# WI-B, step 1 — add ADR 0022 (documentation only): the executor's prompt

You are adding one Architecture Decision Record to the repository `C:\dev\masaha\app` (GitHub
`Basel-Ghonaim/masaha`), revising another, and opening the pull request. **Every text is given to you as a file: copy
it, never retype or reword it.** The owner approved these texts. Do exactly the steps below, in order, and nothing
else. Another worker (WI-C2) runs in a different folder, `C:\dev\masaha\app-design`: never touch it.

## Hard limits
- Touch exactly three files in the repository: create `docs/architecture/decisions/0022-the-berry-on-the-main-action.md`;
  add one line to `docs/architecture/decisions/0019-ink-and-spark-brand.md`; add one line to `docs/README.md`.
- Stage by path only. Never `git add -A`, `git add .` or `git commit -a`.
- No tool attribution anywhere: no `Co-authored-by` trailer, no "generated with", in the commit or the PR.
- Never merge, never push to `main`, never force-push. The owner merges.
- If any step fails or anything differs from what this prompt expects, **stop and write what happened** in the
  report (last step) instead of improvising.

## The source files (in `C:\dev\masaha\workspace\TASKS\BERRY_PRIMARY\ADR\`)
- `0022-the-berry-on-the-main-action.md` — the ADR, the whole file.
- `adr-0019-revised-line.txt` — the one line for ADR 0019.
- `readme-line.txt` — the one line for `docs/README.md`.
- `commit-message.txt` — the commit message (subject, blank line, body).
- `pr-body.md` — the pull request's description.

## Steps
1. In `C:\dev\masaha\app`: `git status` must be clean and on `main`. Then `git fetch origin` and
   `git switch -c docs/adr-0022 origin/main`.
2. Copy the ADR byte for byte:
   `Copy-Item 'C:\dev\masaha\workspace\TASKS\BERRY_PRIMARY\ADR\0022-the-berry-on-the-main-action.md' 'docs\architecture\decisions\0022-the-berry-on-the-main-action.md'`
3. **The date.** Line 3 of the new ADR reads `> **Status:** Accepted · **Date:** 2026-11-24`, and the revised line
   for ADR 0019 starts `> **Revised:** 2026-11-24`. If today is not 2026-11-24, change only those two dates to
   today's (`YYYY-MM-DD`).
4. In `docs/architecture/decisions/0019-ink-and-spark-brand.md`, insert the line of `adr-0019-revised-line.txt`
   **directly after line 3** (the line starting `> **Status:** Accepted`), with no blank line between them. Then
   `git diff` of that file must show exactly one added line and nothing removed.
5. In `docs/README.md`, find the line that starts with
   `  - [0021](architecture/decisions/0021-sign-in-where-the-action-is.md)` and insert the line of `readme-line.txt`
   **directly after it**. `git diff docs/README.md` must show exactly one added line and nothing removed.
6. Checks, from `C:\dev\masaha\app`, each must pass:
   - `npm run check:links`
   - `npm run check:conflicts`
   - `npm run format:check`
7. Commit:
   - `git add docs/architecture/decisions/0022-the-berry-on-the-main-action.md docs/architecture/decisions/0019-ink-and-spark-brand.md docs/README.md`
   - `git commit -F C:\dev\masaha\workspace\TASKS\BERRY_PRIMARY\ADR\commit-message.txt`
   - `git show --stat HEAD` must list exactly the three files, and `git log -1 --format=%(trailers)` must print
     nothing (no trailer). **Note:** `git log -1 --format=%B` always ends with one extra newline that the file does
     not have; that is expected and is not a failure.
8. Push and open the pull request:
   - `git push -u origin docs/adr-0022`
   - `gh pr create --base main --head docs/adr-0022 --title "docs(adr): the berry on the main action" --body-file C:\dev\masaha\workspace\TASKS\BERRY_PRIMARY\ADR\pr-body.md`
9. Wait for CI, bounded: check `gh pr checks <number>` every 2 minutes, at most 15 times. A network error or "no
   checks reported" is not a failure: check again. When every check passes (a skipped one is fine), check
   `gh pr view <number> --json mergeStateStatus --jq .mergeStateStatus` (expected `CLEAN`).
10. Switch the checkout back: `git switch main` (leave the branch `docs/adr-0022` in place).
11. Write the report to `C:\dev\masaha\workspace\TASKS\BERRY_PRIMARY\4_REPORT_ADR.md`: the PR number and URL, the head
    commit's full sha, each check and its result, the merge state, the output of `git show --stat HEAD` (from step
    7), whether you changed the dates (step 3), and anything that did not go as written. Then stop.
