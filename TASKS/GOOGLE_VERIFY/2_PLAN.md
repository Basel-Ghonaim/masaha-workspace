# GOOGLE_VERIFY — Copilot's plan
## 1. Starting state

- `git status --short --branch`
  - Output: `## main...origin/main`
  - Matches "Expected": Yes; the worktree is clean on `main`.
- `git fetch origin`
  - Output: completed successfully with no output.
  - Matches "Expected": Yes.
- `git rev-parse origin/main`
  - Output: `3a85169030554387ab6893ed1eab559ed7dedc82`
  - Matches "Expected": Yes; this is the current remote-main revision.
- `git rev-parse HEAD`
  - Output: `3a85169030554387ab6893ed1eab559ed7dedc82`
  - Matches "Expected": Yes; `HEAD` equals `origin/main`.
- `Get-FileHash C:\dev\masaha\workspace\TASKS\GOOGLE_VERIFY\google17f1cc2beeef3f62.html -Algorithm SHA256`
  - Output: `9EDE73C80741852053B7FC3FD0347F429344E8F97636B8E7ADEFD4AECC3E6075`
  - Matches "Expected": Yes; this is the expected SHA-256, case-insensitively.
- `(Get-Item C:\dev\masaha\workspace\TASKS\GOOGLE_VERIFY\google17f1cc2beeef3f62.html).Length`
  - Output: `53`
  - Matches "Expected": Yes.
- `Test-Path C:\dev\masaha\app\apps\web\public\google17f1cc2beeef3f62.html`
  - Output: `False`
  - Matches "Expected": Yes; the destination file is absent.
- `gh auth status`
  - Output: signed in to `github.com` as `Basel-Ghonaim`; active account; token scopes include `gist`, `read:org`, and `repo`.
  - Matches "Expected": Yes; GitHub is authenticated.
- `gh pr list --state open`
  - Output: no output.
  - Matches "Expected": Yes; no open pull requests were listed.
- `(Select-String -Path docs\development\setup.md -SimpleMatch -Pattern 'Its consent screen stays in *Testing* (step 5) |').Count`
  - Output: `1`
  - Matches "Expected": Yes.
- `(Select-String -Path docs\development\setup.md -SimpleMatch -Pattern '**The consent screen stays in *Testing*:** publishing it needs a homepage').Count`
  - Output: `1`
  - Matches "Expected": Yes.
- Old text C is not checked in phase 1 because it exists only after edit B.

## 2. Steps

1. **The branch**
   - Commands:
     ```
     cd C:\dev\masaha\app
     git fetch origin
     git status --short
     git switch -c chore/google-site-verification origin/main
     ```
   - Expected result: fetch succeeds; `git status --short` prints nothing; branch `chore/google-site-verification` is created from `origin/main`.

2. **Commit 1 — the document's correction**
   - Edit A and edit B in `docs/development/setup.md`, and nothing else on their lines.
   - Commands:
     ```
     git diff --stat
     git status --short
     git add docs/development/setup.md
     git commit -F C:\dev\masaha\workspace\TASKS\GOOGLE_VERIFY\msg-1.txt
     ```
   - Expected result: `git diff --stat` shows only `docs/development/setup.md`, with `2 insertions(+), 2 deletions(-)`; status shows only that file; commit 1 succeeds using `msg-1.txt`.

3. **The file — copy it**
   - Commands:
     ```
     Copy-Item C:\dev\masaha\workspace\TASKS\GOOGLE_VERIFY\google17f1cc2beeef3f62.html C:\dev\masaha\app\apps\web\public\google17f1cc2beeef3f62.html
     Get-FileHash C:\dev\masaha\app\apps\web\public\google17f1cc2beeef3f62.html -Algorithm SHA256
     (Get-Item C:\dev\masaha\app\apps\web\public\google17f1cc2beeef3f62.html).Length
     ```
   - Expected result: the copied file has SHA-256 `9ede73c80741852053b7fc3fd0347f429344e8f97636b8e7adefd4aecc3e6075` and length `53`.

4. **The ignore entry and the sentence**
   - Make edit D in `.prettierignore` and edit C in `docs/development/setup.md`.
   - Expected result: only the specified ignore entry and sentence are added, with `.prettierignore` retaining its final newline and the sentence remaining on the same line.

5. **Commit 2**
   - Commands:
     ```
     git status --short
     git add apps/web/public/google17f1cc2beeef3f62.html .prettierignore docs/development/setup.md
     git commit -F C:\dev\masaha\workspace\TASKS\GOOGLE_VERIFY\msg-2.txt
     ```
   - Expected result: before staging, status lists exactly `?? apps/web/public/google17f1cc2beeef3f62.html`, `M .prettierignore`, and `M docs/development/setup.md`; commit 2 succeeds using `msg-2.txt`.

6. **Checks, on the head**
   - Commands, each run one at a time:
     ```
     npm run format:check
     npm run check:links
     npm run check:conflicts
     node C:\dev\masaha\workspace\TASKS\IDENTITY\scripts\heavy.mjs gv npm run build
     Get-FileHash C:\dev\masaha\app\apps\web\dist\google17f1cc2beeef3f62.html -Algorithm SHA256
     ```
   - Expected result: every command passes; the built file has SHA-256 `9ede73c80741852053b7fc3fd0347f429344e8f97636b8e7adefd4aecc3e6075`; after the build `git status --short` prints nothing. If the grant script exits with code 75, stop and report.

7. **The history check, before the push**
   - Commands:
     ```
     git log origin/main..HEAD --format='%h %s'
     git log origin/main..HEAD --format=%B
     git diff origin/main --stat
     ```
   - Expected result: exactly two commits, with subjects `docs(setup): the consent screen is published` then `chore(web): add Google's site verification file`; bodies exactly match `msg-1.txt` and `msg-2.txt` with no `Co-authored-by` or other trailer; the diff contains exactly the three specified files. If a trailer appears, amend commit 2 with its message file; for commit 1, stop and report.

8. **Push and open the PR**
   - Commands:
     ```
     git push -u origin chore/google-site-verification
     gh pr create --base main --head chore/google-site-verification --title "chore(web): add Google's site verification file" --body-file C:\dev\masaha\workspace\TASKS\GOOGLE_VERIFY\pr-body.md --assignee "@me" --label chore --label area:web --label area:docs
     ```
   - Expected result: the branch is pushed and one PR is opened with the specified title, body file, assignee, and labels; note the PR number.

9. **Wait for CI**
   - Commands:
     ```
     gh pr checks <number> --watch --interval 30
     gh pr view <number> --json headRefOid,mergeStateStatus,title,labels,assignees
     ```
   - Expected result: all checks pass and the PR state is read; if `mergeStateStatus` is `UNKNOWN`, read it again after one minute, at most five times. If any check fails, do not fix it; record the failing check and the end of `gh run view --log-failed`, then stop.

10. **The report**
    - Write `C:\dev\masaha\workspace\TASKS\GOOGLE_VERIFY\4_REPORT.md`.
    - Expected result: the report contains the PR number and URL, full head SHA, both commit SHAs and subjects, each step-6 result line, step-7 outputs, CI result, `mergeStateStatus`, and anything unexpected; do not merge.

## 3. The edits

- **A — `docs/development/setup.md`, the `GOOGLE_CLIENT_ID` row (commit 1)**
  - Old:
    ```
    Its consent screen stays in *Testing* (step 5) |
    ```
  - New:
    ```
    Its consent screen is published (step 5) |
    ```
- **B — `docs/development/setup.md`, step 5 of *The owner's steps* (commit 1)**
  - Old:
    ```
    **The consent screen stays in *Testing*:** publishing it needs a homepage and a privacy-policy address, and Masaha has no privacy page (outside v1). So online, Google sign-in works only for the test users listed on the consent screen (at most 100); everyone else registers by email. Add each test user's Google account there (the owner's decision, 2026-11-01; its branding and publishing are discussed with the owner on 2026-11-02).
    ```
  - New:
    ```
    **The consent screen is published** (*In production*, the owner, 2026-11-05): its homepage is the public address and its privacy policy the site's `/privacy` page, so any Google account signs in. Google shows the app's name and logo on that screen only once it has verified the branding; until then it shows the address.
    ```
- **C — `docs/development/setup.md`, the same line, after B (commit 2)**
  - Old:
    ```
    until then it shows the address.
    ```
  - New:
    ```
    until then it shows the address. That verification needs the site's ownership proved in Google Search Console, by the file `apps/web/public/google17f1cc2beeef3f62.html` served at the site's root: never remove or edit it, since Google checks it again (`.prettierignore` keeps it byte for byte).
    ```
- **D — `.prettierignore` (commit 2)**
  - Old: the file ends with:
    ```
    coverage/
    ```
  - New: after `coverage/`, add one empty line and:
    ```
    # Google Search Console's proof of the site's ownership, kept byte for byte (docs/development/setup.md, step 5)
    apps/web/public/google17f1cc2beeef3f62.html
    ```
    Keep a newline at the end of the file.

## 4. Checks

- `npm run format:check` proves the requested document and ignore-file changes meet the repository formatter rules while the Google file remains excluded from formatting.
- `npm run check:links` proves the documentation links, image paths, anchors, and cited documentation paths resolve.
- `npm run check:conflicts` proves no merge-conflict markers were introduced in tracked files.
- `node C:\dev\masaha\workspace\TASKS\IDENTITY\scripts\heavy.mjs gv npm run build` proves the application builds through the required memory-grant script and that the public file is included in the build.
- `Get-FileHash C:\dev\masaha\app\apps\web\dist\google17f1cc2beeef3f62.html -Algorithm SHA256` proves the built root file remains byte-for-byte identical to Google's source file.
- No tests, lint, or typecheck will be run because G3 says this is a documentation/static-file change with no code and explicitly limits the checks.

## 5. Commits and the PR

- Commit 1: use `C:\dev\masaha\workspace\TASKS\GOOGLE_VERIFY\msg-1.txt`; files: `docs/development/setup.md`; subject: `docs(setup): the consent screen is published`.
- Commit 2: use `C:\dev\masaha\workspace\TASKS\GOOGLE_VERIFY\msg-2.txt`; files: `apps/web/public/google17f1cc2beeef3f62.html`, `.prettierignore`, and `docs/development/setup.md`; subject: `chore(web): add Google's site verification file`.
- PR title: `chore(web): add Google's site verification file`.
- PR labels: `chore`, `area:web`, `area:docs`.
- PR assignee: `@me`.
- PR body file: `C:\dev\masaha\workspace\TASKS\GOOGLE_VERIFY\pr-body.md`.
- The PR will target `main` from `chore/google-site-verification`; it will not be merged.

## 6. Risks and questions

- The Google verification file must remain byte-for-byte identical, including its lack of a final newline; copying it and ignoring it in Prettier mitigates that risk.
- The build may wait for free memory or exit with code 75 if no grant is available; in either case, follow the prompt's stop/report rule.
- None.

## 7. Proposed alternatives

- The owner decisions file's G6 parenthetical says a Copilot `Co-authored-by` trailer is included, but the execution prompt explicitly forbids tool attribution and step 7 requires no such trailer. I will follow the explicit no-attribution rule and the step-7 expectation: no `Co-authored-by` trailer.
