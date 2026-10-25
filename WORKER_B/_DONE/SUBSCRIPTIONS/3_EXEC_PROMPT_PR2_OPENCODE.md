# SUBSCRIPTIONS PR 2 (`feat/subscriptions`) — phase 2: lanes, real run, PR number, push, PR, CI

**This is not a Work Item.** Do not plan, do not use any skill, do not create an Issue, do not change any code
or document of the repository. Every command is spelled out; run them **in PowerShell, as written**. **You
judge nothing:** anything that fails, errors or differs from what this file expects → stop at once, write what
you saw into the report, and reply with §8's shape, `Status: STOPPED`. Never retry a failing step a different
way, never skip one, never fix code, never run a command this file does not name.

- Repository: `C:\dev\masaha\app-b` (worker B's). Never touch `C:\dev\masaha\app` or `C:\dev\masaha\app-design`.
- Folder: `C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\` (below: `SUBS\`). Write only there:
  `4_REPORT_PR2.md` (append) and `scripts\`.
- Read an exit code with `$LASTEXITCODE` right after the command; a command passed only if it is 0.
- Never print a secret or a phone number. Never merge. Never force-push.
- **The owner's decision (2026-10-22):** the PR stays one PR (74 files), as PR 1 was answered.
- **`main` moved (2026-10-22):** worker A's #105 (the Directory's map: `apps/web` and documents only, no
  migration) merged at `a3828e09`. This branch stays on `5a0cda1a`: **do not rebase, do not merge `main` in.**
  GitHub judges the two together in §6 (`mergeStateStatus`); anything but `CLEAN` → stop, the supervisor decides.

## 1. Preconditions — all must hold, else stop

```powershell
cd C:\dev\masaha\app-b
git status --short                     # expect: nothing
git branch --show-current              # expect: feat/subscriptions
git rev-parse --short HEAD             # expect: 3d6bf290
git ls-remote --heads origin feat/subscriptions   # expect: nothing
docker ps --format '{{.Names}} {{.Status}}'       # expect: masaha-postgres-1 Up …
Get-NetTCPConnection -LocalPort 3321 -State Listen -ErrorAction SilentlyContinue   # expect: nothing
gh pr view 105 --json state --jq .state          # expect: MERGED
gh pr list --state open --json number --jq '.[].number'   # expect: nothing
```
Memory: if `Get-CimInstance Win32_Process -Filter "Name='node.exe'" | Where-Object { $_.CommandLine -match 'vitest' }`
lists anything, wait (check every 2 minutes, at most 30 minutes) until it lists nothing; never stop it.

## 2. The lanes, once each, one at a time

```powershell
cd C:\dev\masaha\app-b
$S = 'C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\scripts'
npm run build -w @masaha/shared *> "$S\p2-shared.txt"; "shared exit $LASTEXITCODE"
npm run test:unit    *> "$S\p2-unit.txt";   "unit exit $LASTEXITCODE"
npm run test:api     *> "$S\p2-api.txt";    "api exit $LASTEXITCODE"
npm run format:check *> "$S\p2-format.txt"; "format exit $LASTEXITCODE"
npm run check:links  *> "$S\p2-links.txt";  "links exit $LASTEXITCODE"
```
For each, copy into the report the exit code and the result lines: `Select-String -Path <file> -Pattern
'Test Files|Tests |All matched|links in|error' | Select-Object -Last 6`. A non-zero exit → stop.
**Killed for low memory** (the output ends without a result, or says killed / out of memory): run that lane
once more after the memory check of §1; killed again → record it and go on (CI judges it).

## 3. The real run — once only (it changes the demo data)

```powershell
cd C:\dev\masaha\app-b
$S = 'C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\scripts'
Start-Process -WindowStyle Hidden -WorkingDirectory 'C:\dev\masaha\app-b' -FilePath npm.cmd -ArgumentList 'run','dev','-w','@masaha/api' -RedirectStandardOutput "$S\server.log" -RedirectStandardError "$S\server.err.log"
$end = (Get-Date).AddSeconds(60); do { Start-Sleep 2; $h = curl.exe -s http://localhost:3321/health } until ($h -match '"db":"up"' -or (Get-Date) -gt $end); "health: $h"
node "$S\realrun2.mjs" *> "$S\p2-realrun.txt"; "realrun exit $LASTEXITCODE"
Get-Content "$S\p2-realrun.txt"
```
Health not `"db":"up"` within 60 s → stop (servers stopped as below). Copy the whole output into the report.
Exit 0 with `ALL PASS` → go on; anything else → stop **without running it again**.

Then stop the API and clean up:
```powershell
Get-NetTCPConnection -LocalPort 3321 -State Listen -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }
Get-CimInstance Win32_Process -Filter "Name='node.exe'" | Where-Object { $_.CommandLine -match 'masaha\\app-b\\' -and $_.CommandLine -match 'tsx|pino' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
Get-NetTCPConnection -LocalPort 3321 -State Listen -ErrorAction SilentlyContinue   # expect: nothing
Remove-Item "$S\server.log","$S\server.err.log"
git -C C:\dev\masaha\app-b status --short     # expect: nothing
```

## 4. The PR number — one script, Git Bash through its full path

The next PR number is expected to be **106** (#105, worker A's, is the last one, merged). The script checks it, rewrites the
documents in every commit, checks the rewrite changed nothing else, and sets the number in the description:
```powershell
& "C:\Program Files\Git\bin\bash.exe" C:/dev/masaha/workspace/WORKER_B/SUBSCRIPTIONS/scripts/prnum.sh 106; "prnum exit $LASTEXITCODE"
```
It must print `PRNUM OK #106 <new head> (was 3d6bf290)` and exit 0. `PRNUM STOP: …` → copy it and stop (the
script changes nothing on a stop, or names its backup branch). Do not compute or replace the number yourself.
Then, once:
```powershell
cd C:\dev\masaha\app-b
npm run check:links; "links exit $LASTEXITCODE"
npm run format:check; "format exit $LASTEXITCODE"
git status --short    # expect: nothing
```

## 5. The description, push and PR

1. In `SUBS\scripts\pr2-body.md`, replace the four `<phase 2: …>` placeholders **only**, with the result lines
   from §2 and §3 (for the real run: its `PASS` lines, the audit's actions and `ALL PASS`). Change nothing else.
   Then `Select-String -Path "$S\pr2-body.md" -Pattern '<phase 2|PRNUM'` → nothing.
2. Push and create — with `gh pr create`, not the API:
```powershell
cd C:\dev\masaha\app-b
git push -u origin feat/subscriptions; "push exit $LASTEXITCODE"
gh pr create --assignee "@me" --label feat --label area:api --label area:docs --label area:web --title "feat(desk): run customers' subscriptions" --body-file C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\scripts\pr2-body.md
gh pr view --json number,url,labels --jq '.number, .url, ([.labels[].name] | join(","))'
```
3. The number must be 106 and the four labels present. If not: stop and report what you see (do not fix it).

## 6. CI

```powershell
gh pr checks 106 --watch --interval 60; "checks exit $LASTEXITCODE"
gh pr view 106 --json headRefOid,mergeStateStatus --jq '.headRefOid, .mergeStateStatus'
git -C C:\dev\masaha\app-b rev-parse HEAD
```
If `--watch` is still waiting after 40 minutes, stop it and report "pending". Green = every check passed **on
the pushed head** (the two shas equal) and `mergeStateStatus` is `CLEAN` (`DIRTY`, `BEHIND` or anything else →
stop; never rebase). A red check → copy its name and `gh run view <run id> --log-failed`'s
last 60 lines into the report and stop. Then, for every other open PR (`gh pr list --state open --json
number,headRefOid`): `git -C C:\dev\masaha\app-b merge-tree --write-tree HEAD <its headRefOid>` → record clean
or the conflicted paths.

## 7. The report

Append to `SUBS\4_REPORT_PR2.md` a section `## Phase 2 (OpenCode, 2026-10-22)`, written as you go: §1's
results; each lane's exit and result lines; the real run's whole output and **what it changed in the demo data**
(رامي's ₪15 visit paid; two «أسبوعي» subscriptions for him, the first paid ₪50 and ended, the second its unpaid
renewal; their audit entries); §4's line; the PR URL; CI's result; the conflict check.

## 8. Your final reply — this shape

```
Status: DONE | STOPPED
PR: #<n> <url> · head <sha> · CI <green/red/pending> · <CLEAN/not CLEAN> · labels <list>   (or "no PR")
Lanes: shared <exit> · test:unit <exit, result line> · test:api <exit, result line> · format <exit> · links <exit>
Real run: <exit> · <ALL PASS or the FAIL lines>
PR number: <the script's line>
Conflicts with open PRs: <each: clean / paths>
Ran and failed: <each, what failed>   (or "none")
Port 3321 free: <yes/no> · git status clean: <yes/no>
Stopped at (if STOPPED): <the step, the exact command and output>
Report: C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\4_REPORT_PR2.md
```
