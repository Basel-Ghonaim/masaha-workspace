# PUBLIC PR 2 (`feat/directory-map`) — finish it: squash, three real-run cases, push, PR, CI

> **RESUME (2026-10-22): steps 1–3 are done.** §2's squash is done (head `f0fc8a73`, five commits, the same
> tree as `026ad224`); §3's three cases were redone by the supervisor (`4_REPORT_PR2.md`, *§3 redone by the
> supervisor*). **Do not run §1–§3 again.** Check only: `git status --short` → nothing; `git rev-parse --short
> HEAD` → `f0fc8a73`; `git log --format='%h %s' c3391d0e..HEAD` → the five commits of §2; nothing listens on
> 3320, 5320, 5321. Then **start at §4** and go on to §8. In §5's description, Evidence names the real run's
> cases from the report's §6 table and the supervisor's §3 table.

**This is not a Work Item.** Do not plan, do not use any skill, do not create an Issue, do not change any code
or document of the repository except what step 4 does to `#PRNUM`. Every command is spelled out; run them as
written. **You judge nothing:** anything that fails, errors or differs from what this file expects → stop at
once, write what you saw into the report, and reply with §8's shape, `Status: STOPPED`. Never retry a failing
step a different way, never skip one, never fix code.

- Repository: `C:\dev\masaha\app` (worker A's). Never touch `C:\dev\masaha\app-b` or `C:\dev\masaha\app-design`.
- Workspace folder: `C:\dev\masaha\workspace\WORKER_A\PUBLIC\` (below: `PUBLIC\`). Write only there:
  `4_REPORT_PR2.md` (append) and `scripts\`.
- Shell: Git Bash unless a step says PowerShell. No `jq` (use `gh … --jq`). Every wait is bounded.
- Never print a secret. Never merge. Never force-push except where step 5 says so.

## 1. Preconditions — all must hold, else stop

```bash
cd /c/dev/masaha/app
git status --short                       # expect: nothing
git branch --show-current                # expect: feat/directory-map
git rev-parse --short HEAD               # expect: 026ad224
git merge-base HEAD origin/main | cut -c1-8   # expect: c3391d0e
git ls-remote --heads origin feat/directory-map   # expect: nothing (not pushed)
git log --format='%h %s' c3391d0e..HEAD  # expect these 11, newest first:
```
```
026ad224 feat(directory): set my location on the map
0b41f9ff feat(directory): show the spaces on a map
44b18ea8 feat(map): show many marks and pick a centre
9aff83e7 docs(findings): record the place filter's cap
3fdc64af docs(findings): widen 130 to the focus shell
571fb717 fix(directory): close the sheet when it widens
3d644be9 fix(directory): reset the price on clearing
a4a35948 test(directory): prove near me's privacy gates
31415093 fix(directory): clear what found nothing
28f0bde6 fix(directory): stop locating when no answer comes
355287b6 fix(directory): keep near me's focus and status
```
`docker ps --format '{{.Names}} {{.Status}}'` → `masaha-postgres-1 Up …`. If not: stop and ask the owner.

## 2. Squash the history (the owner's decision, 2026-10-22)

The six carried fix commits become **one** commit; the two findings commits become **one**; the three feature
commits stay as they are. The messages are written already: `PUBLIC\scripts\squash-fix-msg.txt` and
`PUBLIC\scripts\squash-docs-msg.txt` — use them unchanged.

```bash
cd /c/dev/masaha/app
M=/c/dev/masaha/workspace/WORKER_A/PUBLIC/scripts
git branch backup/directory-map-pre-squash 026ad224
git switch -C feat/directory-map 571fb717
git reset --soft c3391d0e
git commit -F "$M/squash-fix-msg.txt"
git cherry-pick -n 3fdc64af 9aff83e7
git commit -F "$M/squash-docs-msg.txt"
git cherry-pick 44b18ea8 0b41f9ff 026ad224
```
Then check — each must hold, else stop (the backup branch keeps the old history; do not delete it):
```bash
git diff 026ad224 HEAD --stat            # expect: nothing (the same tree)
git log --format='%h %s' c3391d0e..HEAD  # expect 5 commits, oldest at the bottom:
                                         #   feat(directory): set my location on the map
                                         #   feat(directory): show the spaces on a map
                                         #   feat(map): show many marks and pick a centre
                                         #   docs(findings): record #103's review findings
                                         #   fix(directory): carry #103's review fixes
git log --format='%an <%ae>%n%B' c3391d0e..HEAD | grep -iE 'co-authored|generated with|opencode|claude'   # expect: nothing
git status --short                       # expect: nothing
npx tsc -b apps/web; echo "tsc exit $?"  # expect: tsc exit 0
```
Record the five new shas in the report.

## 3. The three real-run cases left (read-only; no sign-in, no write)

Start the servers (PowerShell, from `C:\dev\masaha\app`):
```powershell
$S = 'C:\dev\masaha\workspace\WORKER_A\PUBLIC\scripts'
Start-Process -WindowStyle Hidden -FilePath npm.cmd -ArgumentList 'run','dev','-w','@masaha/api' -RedirectStandardOutput "$S\api-dev-3.log" -RedirectStandardError "$S\api-dev-3.err.log"
Start-Process -WindowStyle Hidden -WorkingDirectory 'C:\dev\masaha\app\apps\web' -FilePath npx.cmd -ArgumentList 'vite','--port','5320','--strictPort' -RedirectStandardOutput "$S\web-vite-3.log" -RedirectStandardError "$S\web-vite-3.err.log"
```
Wait (at most 60 s) until both answer: `curl.exe -s http://localhost:3320/health` shows `up`, and `curl.exe -s -o
NUL -w "%{http_code}" http://localhost:5320/` prints `200`. Not within 60 s → stop.

Run each case once, from the scripts folder, keeping its output:
```bash
cd /c/dev/masaha/workspace/WORKER_A/PUBLIC/scripts
node run2.mjs centre  > run2-centre.txt  2>&1; echo "centre exit $?"
node run2.mjs leaflet > run2-leaflet.txt 2>&1; echo "leaflet exit $?"
node run2.mjs carried > run2-carried.txt 2>&1; echo "carried exit $?"
ls ../shots/pr2 | grep -E '^2-(centre|leaflet|carried)'
```
Each exit must be 0, else stop. Copy into the report, as they are: the last 15 lines of each `.txt`, the list
of new screenshots, and the first line of each `../shots/pr2/2-leaflet-*-log.txt` (the count before «خريطة»).
Do not judge the screenshots; the supervisor does.

Stop the servers by the ports' owning processes (PowerShell), then check the ports are free:
```powershell
foreach ($p in 3320,5320) { Get-NetTCPConnection -LocalPort $p -State Listen -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force } }
Get-CimInstance Win32_Process -Filter "Name='node.exe'" | Where-Object { $_.CommandLine -match 'C:\\dev\\masaha\\app\\' -and $_.CommandLine -match 'tsx|vite|pino' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
Get-NetTCPConnection -LocalPort 3320,5320 -ErrorAction SilentlyContinue   # expect: nothing
```
`git -C C:\dev\masaha\app status --short` → nothing (a screenshot inside the repository → move it to
`PUBLIC\shots\pr2\`).

## 4. The PR number

```bash
cd /c/dev/masaha/app
git fetch origin
n=$(( $(gh api "repos/{owner}/{repo}/issues?state=all&per_page=1&sort=created&direction=desc" --jq '.[0].number') + 1 ))
echo "PR will be #$n"
base=$(git merge-base HEAD origin/main)
git filter-branch -f --tree-filter "grep -rl '#PRNUM' docs | xargs -r sed -i 's/#PRNUM/#$n/g'" $base..HEAD
git for-each-ref --format='%(refname)' refs/original/ | xargs -r -n1 git update-ref -d
git grep -n '#PRNUM'; echo "expect nothing above"
npm run check:links; echo "links exit $?"
npm run format:check; echo "format exit $?"
git status --short                       # expect: nothing
```
Both exits 0, else stop. Do **not** rebase onto `origin/main`.

## 5. Push and open the PR

1. Write the description to `PUBLIC\scripts\pr-body-2.md`: the same sections as `PUBLIC\scripts\pr-body-1b.md`
   (Summary; Scope / Acceptance criteria / Out of scope; Change type; Evidence; Screenshots; Definition of Done
   checklist). Take every fact from `PUBLIC\4_REPORT_PR2.md` and `PUBLIC\2_PLAN.md`'s PR 2 only — invent
   nothing. It has a section **"Carried from #103"** listing items 1–12: 1–7 and 11 in the fix commit (its new
   sha), 8–10 in the findings commit (finding 130 widened, finding 133), 12 kept as it is. Evidence lists the
   commands and result lines the report holds, and says the full `test:component` lane, `test:unit` of
   `apps/api` and `packages/shared` and `test:api` are CI's. No tool attribution anywhere.
2. Push and create:
```bash
git push -u origin feat/directory-map
gh pr create --assignee @me --label feat --label area:web --label area:design-system --label area:docs \
  --title "feat(directory): show the spaces on a map" \
  --body-file /c/dev/masaha/workspace/WORKER_A/PUBLIC/scripts/pr-body-2.md
```
3. GitHub's number must equal `n`. If not: stop and report both numbers (do not fix it).

## 6. CI

```bash
timeout 2400 gh pr checks <n> --watch; echo "checks exit $?"
gh pr view <n> --json headRefOid,mergeStateStatus --jq '.headRefOid + " " + .mergeStateStatus'
git rev-parse HEAD
```
Green means every check passed **on the pushed head** (the two shas equal). Red or a timeout → copy the failed
check's name and `gh run view <id> --log-failed | tail -60` into the report and stop. Then, for every other open
PR: `git merge-tree --write-tree HEAD <its headRefOid>` → record clean or the conflicted paths.

## 7. The report

Append to `PUBLIC\4_REPORT_PR2.md` a section `## 7. Finished by OpenCode (2026-10-22)`, written as you go:
§1's results; §2's five shas and checks; §3's outputs; §4's `n` and exits; §5's PR URL; §6's result.

## 8. Your final reply — this shape

```
Status: DONE | STOPPED
PR: #<n> <url> · head <sha> · CI <green/red/pending> · <CLEAN/not CLEAN>   (or "no PR")
Commits: <sha> <subject> (<chars>) — the five, oldest first
Same tree as 026ad224: <yes/no>
Real run: centre <exit> · leaflet <exit, the before-count lines> · carried <exit> · shots <count>
Ran and passed: <each command, with the result line you saw>
Ran and failed: <each, what failed>   (or "none")
Ports 3320/5320 free: <yes/no> · git status clean: <yes/no>
Stopped at (if STOPPED): <the step, the exact command and output>
Report: C:\dev\masaha\workspace\WORKER_A\PUBLIC\4_REPORT_PR2.md
```
