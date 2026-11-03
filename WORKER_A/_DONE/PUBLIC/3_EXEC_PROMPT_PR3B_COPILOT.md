# PUBLIC PR 3b (`feat/space-photos-status`) — the space page's photos and live status — for GitHub Copilot

You are the **executor** of one pull request in the Masaha repository, in a fresh session. You did not plan
it and you will not review it; a reviewer and the supervisor check every claim in the code afterwards. **The
plan is approved: do not re-decide anything in it.** This file is self-contained: every file to read and every
command is named. Run commands **in PowerShell**; read each exit code with `$LASTEXITCODE` right after the
command (a command passed only if it is 0). Write long outputs to a file under the scripts folder and read only
the lines you need.

- Repository: `C:\dev\masaha\app` (worker A's). Never touch `C:\dev\masaha\app-b` or `C:\dev\masaha\app-design`.
- Workspace folder: `C:\dev\masaha\workspace\WORKER_A\PUBLIC\` (below: `PUBLIC\`). Outside the repository write
  only there: `4_REPORT_PR3B.md`, `scripts\`, `shots\pr3b\`.
- API on port 3320, web on 5320, database `masaha_dev` (Docker container `masaha-postgres-1`, port 5433).

## 1. What to read — only this

1. `C:\dev\masaha\app\CLAUDE.md` — the project's rules (they bind you too): v1 scope, task scope, atomic
   Conventional Commits, **no tool attribution anywhere**, every user-facing string in both copy catalogues
   (Arabic and English), the design system in `apps/web/src/shared/design-system/` only (semantic tokens,
   logical classes — `ms-`/`me-`/`ps-`/`pe-`/`start`/`end`, never `ml-`/`mr-`/`left`/`right`).
2. `PUBLIC\2_PLAN.md` — **these lines only:** 1–40 (the owner's approval note: it binds and wins); 505–532 (§7,
   PR 3's files — yours are the photos' and the live status's); 625–655 (§8, PR 3's design issues — design issue
   32 is yours); **1264–1297 (§9, PR 3 commits 5 and 6 — exactly what you build)**; 1468–1490 (§10, PR 3's tests
   — yours are **76, 77 and 78**); 1558–1745 (§13, the procedure; the real run's PR 3 cases; the stop rule).
3. `PUBLIC\0_CARRIED_FROM_107.md` whole (items 1–10, the owner's decisions) and, in
   `PUBLIC\6_REVIEW_PR3A_CLAUDE_CODE.md`, the findings it cites.
4. The code the plan names, as each step needs it: `apps/web/src/features/directory/` (the space page from
   PR 3a: `components/page/`, `hooks/page/`, `repository/directoryRepository.ts`, `hooks/queryKeys.ts`),
   `apps/web/src/shared/copy/{arabic,english}/directory.ts`, `docs/features/directory.md`,
   `docs/frontend/architecture.md` (§6, §7). Search before reading a whole file.
5. For the real run: `PUBLIC\scripts\cdp2.mjs` and `PUBLIC\scripts\run2b.mjs` (how this project drives a
   headless Chrome over CDP).

## 2. Preconditions — all must hold, else stop

```powershell
cd C:\dev\masaha\app
gh pr view 107 --json state --jq .state      # expect: MERGED
git fetch origin; git status --short         # expect: nothing
git branch --show-current                    # expect: main
git rev-parse --short HEAD; git rev-parse --short origin/main   # expect: the same sha
docker ps --format '{{.Names}} {{.Status}}'  # expect: masaha-postgres-1 Up …
cd apps\api; npx prisma migrate status; cd ..\..   # expect: "Database schema is up to date!"
```
Docker not running, or a migration pending → stop and ask the owner.
Then: `npm run build -w @masaha/shared` (exit 0) and `git switch --no-track -c feat/space-photos-status origin/main`.

## 3. The work, in this order

**A. The carried items first** — `0_CARRIED_FROM_107.md` items 1–10, as dedicated commits before the plan's
commit 5 (its suggested subjects). **B. Then the plan's PR 3 commit 5** (`feat(directory): show the space's
photos`: `useGallery`, `Gallery`, the words, design issue 32, test 76) **and commit 6** (`feat(directory):
refresh a space's live status`: the repository's `status`, the key, `useLiveStatusQuery` with
`refetchInterval: 60_000` and `refetchOnWindowFocus: 'always'`, `StatusPanel`'s states, the words, tests 77
and 78, the documents). Build exactly what lines 1264–1297 say; nothing of PR 4.

**Every code change is test-first:**
1. Write or extend the test; run **that file only**, e.g.
   `npm run test:component -w @masaha/web -- src/features/directory/components/page/SpaceDetails.component.test.tsx`
   (unit tests: `npm run test:unit -w @masaha/web -- <file>`).
2. See it **fail** for the right reason; copy the failing line into the report.
3. Write the code; run the same file; see it pass; copy the pass line.
4. Where §10's *Break* column names a guard the red step did not prove, make that break once (edit the code to
   the broken form), see the test fail, restore the code exactly (check `git diff` shows only your work), see it
   pass. Record both lines.

**Per commit:** `npm run lint` and `npm run typecheck` (both exit 0) before committing.

**Commits:** stage by path (`git add <path> <path>`, never `git add -A` or `git add .`). Write each message to a
file `PUBLIC\scripts\msg-<n>.txt` with your editor — UTF-8 **without BOM**, LF line endings: a subject in
Conventional Commits form of **50 characters or fewer** (count them), a blank line, a body of 2–6 lines saying
**why**. Commit with `git commit -F <file>`. No `Co-Authored-By`, no "generated with", no tool name. A fix to an
earlier commit before the push: `git commit --fixup <sha>`, then `$env:GIT_SEQUENCE_EDITOR=':'; git rebase -i
--autosquash origin/main; Remove-Item Env:GIT_SEQUENCE_EDITOR`.

**Documents:** where the plan dates a decision with the PR number, write `#PRNUM` (step 7 replaces it). A new
finding takes **137** and on (a file in `docs/architecture/findings/` and a line in its `README.md`).

**Size:** about 35 files is expected; past 50 files (`git diff --name-only origin/main | Measure-Object`) →
stop and ask.

## 4. On the head, once each

```powershell
cd C:\dev\masaha\app
$S = 'C:\dev\masaha\workspace\WORKER_A\PUBLIC\scripts'
npm run test:unit -w @masaha/web *> "$S\3b-unit.txt"; "unit exit $LASTEXITCODE"
npm run test:component -w @masaha/web -- src/features/directory src/pages/site src/shared/map src/shared/design-system *> "$S\3b-component.txt"; "component exit $LASTEXITCODE"
$env:NODE_ENV='production'; npm run build *> "$S\3b-build.txt"; "build exit $LASTEXITCODE"; Remove-Item Env:NODE_ENV
npm run check:build *> "$S\3b-checkbuild.txt"; "checkbuild exit $LASTEXITCODE"
npm run check:classes; "classes exit $LASTEXITCODE"
npm run format:check; "format exit $LASTEXITCODE"
npm run check:links; "links exit $LASTEXITCODE"
```
Add to the component command any other folder whose files you changed. For each, copy the exit code and the
result lines into the report (`Select-String -Path <file> -Pattern 'Test Files|Tests |error' | Select-Object -Last 4`).
Before each test run: `Get-CimInstance Win32_Process -Filter "Name='node.exe'" | Where-Object { $_.CommandLine
-match 'app-b' -and $_.CommandLine -match 'vitest' }` lists nothing (else wait; never stop it).
**Not run locally — CI judges:** the full `test:component` lane, `test:unit` of `apps/api` and
`packages/shared`, `test:api`. A fix after a lane passed re-runs only the files it touches, plus lint and
typecheck.

## 5. The real run

1. Start the servers (PowerShell, from `C:\dev\masaha\app`):
```powershell
$S = 'C:\dev\masaha\workspace\WORKER_A\PUBLIC\scripts'
Start-Process -WindowStyle Hidden -FilePath npm.cmd -ArgumentList 'run','dev','-w','@masaha/api' -RedirectStandardOutput "$S\3b-api.log" -RedirectStandardError "$S\3b-api.err.log"
Start-Process -WindowStyle Hidden -WorkingDirectory 'C:\dev\masaha\app\apps\web' -FilePath npx.cmd -ArgumentList 'vite','--port','5320','--strictPort' -RedirectStandardOutput "$S\3b-web.log" -RedirectStandardError "$S\3b-web.err.log"
```
   Wait (≤ 60 s) until `curl.exe -s http://localhost:3320/health` contains `"db":"up"` and `curl.exe -s -o NUL -w
   "%{http_code}" http://localhost:5320/` prints `200`.
2. **Inventory first (read-only):** a script `PUBLIC\scripts\inventory3b.mjs` with plain `fetch` GETs to
   `http://localhost:3320/api/v1/...` finding: a verified space with several photos, one with exactly one photo,
   one with none; a verified space with a live status and one without; an unverified space. Save its output.
   A case the data does not hold → record it as **NOT PERFORMED** with the test that proves it, only for what
   §13 allows (lines 1676–1680); any other → stop and report. **Never add or change data** through the app, the
   API, the database or the seed.
3. **The browser:** copy `cdp2.mjs` to `PUBLIC\scripts\cdp3b.mjs` with `SHOTS` set to
   `C:/dev/masaha/workspace/WORKER_A/PUBLIC/shots/pr3b`, and write `PUBLIC\scripts\run3b.mjs` in the style of
   `run2b.mjs`. **Send Enter with its text** (`text: '\r'` in `Input.dispatchKeyEvent`), or a native button does
   not activate. Cases (Arabic light and English dark; widths below):
   - a space with photos: the grid at 390, 768, 1440; «عرض كل الصور (n)»; the viewer opens, «التالية» and
     «السابقة» move round, its position, Escape closes it with the focus back;
   - a space with one photo and one with none (the header's caption);
   - the live status: verified with a status, verified without (`unset`), unverified; the network log shows
     `/occupancy` read again after about 60 s while visible, **not** while hidden (CDP
     `Page.setWebLifecycleState` `frozen` then `active`, or `Emulation.setFocusEmulationEnabled`), and at once
     on returning;
   - the carried items a browser shows: the footer above the contact bar at the bottom of the page at 390; a
     touch scroll over the place map at 390 scrolls the page (CDP `Input.dispatchTouchEvent`), the map does not
     pan; the dialog's `none` line; the phone's live line on the map; the hidden `h1` while loading.
   Widths: the layouts that change with width at 390, 768 and 1440 in both; every other case once in Arabic
   light at 390 and once in English dark at 1440. Screenshots named `3b-<case>-<ar-light|en-dark>-<width>.png`.
4. Stop the servers and check:
```powershell
foreach ($p in 3320,5320) { Get-NetTCPConnection -LocalPort $p -State Listen -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force } }
Get-CimInstance Win32_Process -Filter "Name='node.exe'" | Where-Object { $_.CommandLine -match 'masaha\\app\\' -and $_.CommandLine -match 'tsx|vite|pino' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
Get-NetTCPConnection -LocalPort 3320,5320 -State Listen -ErrorAction SilentlyContinue   # expect: nothing
git status --short                                                                       # expect: nothing
```

## 6. The description

Write `PUBLIC\scripts\pr-body-3b.md` with the sections of `PUBLIC\scripts\pr-body-1b.md` (Summary; Scope /
Acceptance criteria / Out of scope; Change type; Evidence; Screenshots; Definition of Done checklist). A section
**"Carried from #107"** lists items 1–10, each with its commit. Evidence lists each command and the result line
you saw, the real run's cases, and says the full `test:component`, `test:unit` of `apps/api` and
`packages/shared` and `test:api` are CI's. Every fact from your report; invent nothing; no tool attribution.

## 7. The PR number, push, PR, CI

1. The next number is **108**, or **109** if worker B's PR was opened first. Read the last number given to an
   issue or a PR (they share one sequence): `gh api "repos/{owner}/{repo}/issues?state=all&per_page=1&sort=created&direction=desc" --jq '.[0].number'`;
   yours is that + 1. Then run the script with it — **do not replace the number yourself**:
```powershell
& "C:\Program Files\Git\bin\bash.exe" C:/dev/masaha/workspace/WORKER_A/PUBLIC/scripts/prnum3b.sh <that number + 1>; "prnum exit $LASTEXITCODE"
```
   It must print `PRNUM OK #<n> <new head> (was <old>)`; `PRNUM STOP: …` → copy it and stop.
2. Then `npm run check:links` and `npm run format:check` (exit 0), `git status --short` (nothing).
3. Push and create:
```powershell
git push -u origin feat/space-photos-status; "push exit $LASTEXITCODE"
gh pr create --assignee "@me" --label feat --label area:web --label area:docs --title "feat(directory): add the space's photos and status" --body-file C:\dev\masaha\workspace\WORKER_A\PUBLIC\scripts\pr-body-3b.md
gh pr view --json number,url,labels --jq '.number, .url, ([.labels[].name] | join(","))'
```
   The number must equal the script's; if not, stop and report both (do not fix it).
4. CI: `gh pr checks <n> --watch --interval 60` (stop waiting after 40 minutes and report "pending"); then
   `gh pr view <n> --json headRefOid,mergeStateStatus --jq '.headRefOid, .mergeStateStatus'` and `git rev-parse
   HEAD` — green on the pushed head (the shas equal) and `CLEAN`. A red check → read `gh run view <run id>
   --log-failed`, fix the cause in the right commit (fixup + autosquash), push again with `git push
   --force-with-lease`; red twice → stop and report. Never merge. Never rebase a `CLEAN` PR.

## 8. The stop rule

A test **failing** because its code is not written yet is normal. A test, lane or command you **cannot run**
(Docker down, a port taken, a module missing, `No test files found`, a startup error, a timeout, a crash with
no result), a break you cannot make, a real-run case you cannot perform → **stop at once**: never skip,
`.skip` or delete a test, never change a config, a timeout, `.env`, a script or a lane, never mock what the plan
does not, never call a failure "flaky". **The plan proves false against the code** → stop, say what and why,
offer the fix, do not choose it. **A break that stays green** → stop. **A carried item or design issue you
would leave undone** → stop and ask. A run killed for low memory → once more when the machine is quieter;
killed again → record it, CI judges. **Never claim a result you did not see**: copy the line that says it.

Write `PUBLIC\4_REPORT_PR3B.md` **as you go**: after the preconditions, after each commit (sha, subject and its
length, the red line, the green line), after each break, after §4, after the real run, after the push, after CI.

## 9. Your final reply — this shape

```
Status: DONE | STOPPED
PR: #<n> <url> · head <sha> · CI <green/red/pending> · <CLEAN/not CLEAN> · files <count>   (or "no PR")
Commits: <sha> <subject> (<chars>) — one line each, the carried ones first
Carried from #107: <each item 1–10: done in <sha>, red then green / docs / checked, no change (item 10)>
Tests 76–78: <each: red seen, then green / its break>
Ran and passed: <each command, with the result line you saw>
Ran and failed: <each, what failed, what you did>   (or "none")
Not run locally (CI judges): <each lane, and CI's result on the head>
COULD NOT RUN: <each, the exact command and error>   (or "none")
Real run: <each case and its screenshot, or NOT PERFORMED (by design) with the test that proves it>
Data left in masaha_dev: <what the run changed>   (expected: nothing)
Departures from the plan: <each, with its reason>   (or "none")
Stopped at (if STOPPED): <the step, the exact command and output, what the owner must decide>
Report: C:\dev\masaha\workspace\WORKER_A\PUBLIC\4_REPORT_PR3B.md
```
