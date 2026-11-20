# GOOGLE_VERIFY — phase 2 report

## PR

- PR number: `148`
- PR URL: https://github.com/Basel-Ghonaim/masaha/pull/148
- Full head SHA: `6f0c9958b1150eb8229cb29aad34f78688de0778`
- Title: `chore(web): add Google's site verification file`
- Labels: `chore`, `area:web`, `area:docs`
- Assignee: `Basel-Ghonaim`

## Commits

- `b4c66150` — `docs(setup): the consent screen is published`
- `6f0c9958` — `chore(web): add Google's site verification file`

## Required checks

- `npm run format:check` — passed: `All matched files use Prettier code style!`
- `npm run check:links` — passed: `2782 links in 263 documents and 2689 source files all resolve.`
- `npm run check:conflicts` — passed: `No conflict markers found.`
- `node C:\dev\masaha\workspace\TASKS\IDENTITY\scripts\heavy.mjs gv npm run build` — passed: all workspaces built successfully; Vite reported `✓ built in 2.19s`.
- `Get-FileHash C:\dev\masaha\app\apps\web\dist\google17f1cc2beeef3f62.html -Algorithm SHA256` — passed: `9EDE73C80741852053B7FC3FD0347F429344E8F97636B8E7ADEFD4AECC3E6075`.
- `git status --short` after the build — passed: no output.

## Step 7 history outputs

`git log origin/main..HEAD --format='%h %s'`:
```text
6f0c9958 chore(web): add Google's site verification file
b4c66150 docs(setup): the consent screen is published
```

`git log origin/main..HEAD --format=%B`:
```text
chore(web): add Google's site verification file

Google refused the branding's verification: the home page was not
registered to the owner. Search Console proves the site's ownership
by this file, served at the site's root, and checks it again later,
so it stays for good. Prettier ignores it, to keep it byte for byte
as Google gave it, and setup.md's step 5 says why it is there.

docs(setup): the consent screen is published

Step 5 and the GOOGLE_CLIENT_ID row still said the consent screen
stays in Testing for want of a privacy page. The owner published it
on 2026-11-05, after /privacy shipped (#135): any Google account
signs in, and Google shows the app's name and logo on that screen
only once it has verified the branding.
```

`git diff origin/main --stat`:
```text
 .prettierignore                             | 3 +++
 apps/web/public/google17f1cc2beeef3f62.html | 1 +
 docs/development/setup.md                   | 4 ++--
 3 files changed, 6 insertions(+), 2 deletions(-)
```

No `Co-authored-by` or other trailer appears in either commit.

## CI

`gh pr checks 148`:
```text
CodeRabbit	skipping
build	pass	1m27s
check:classes	pass	49s
check:conflicts	pass	1m11s
check:links	pass	1m6s
format:check	pass	1m31s
lint	pass	2m52s
test:api	pass	8m53s
test:component	pass	5m22s
test:unit	pass	2m15s
typecheck	pass	1m29s
```

`gh pr view 148 --json headRefOid,mergeStateStatus,title,labels,assignees` reported:

- `headRefOid`: `6f0c9958b1150eb8229cb29aad34f78688de0778`
- `mergeStateStatus`: `CLEAN`

## Unexpected results

The first local `npm run format:check` attempt failed on the supervisor's untracked `.claude/launch.json`, which Git excludes. After the supervisor formatted that file, the check was rerun and passed. No commit was changed to address it.

The PR was not merged.
