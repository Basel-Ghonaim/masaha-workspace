# FINAL — handoff to another AI agent: finish the run (verification, real run, PR, CI, report)

You take over **the end** of a long, almost finished job. **All the code is written and committed.** You do not write
features. You run checks, run the app, open one pull request, watch CI, and write the end of a report. Work slowly and
carefully: **one step at a time; after each step, check its result before the next.** When a step goes wrong and this
file does not say what to do, **stop and write to the owner** (in the report and in your reply) — never improvise a fix.

## 0. Facts you need

- Repository: `C:\dev\masaha\app`. Branch: **`feat/final`**, head **`f4dcc6dd`**, **124 commits** on `origin/main`
  (`ce671b37`). The working tree must be clean.
- Workspace folder (outside the repository): `C:\dev\masaha\workspace\WORKER_A\FINAL\`. Scripts in `scripts\`.
  **The report** you finish: `C:\dev\masaha\workspace\WORKER_A\FINAL\4_REPORT_LEAD.md`.
- The PR description, drafted: `scripts\pr-body.md` (you fill two marked parts).
- Shell: use **Git Bash** paths like `/c/dev/masaha/app` (not PowerShell syntax) unless a step says PowerShell.
- Ports: web **5320**, API **3320**. Databases in Docker container `masaha-postgres-1`: `masaha_dev` (the app's),
  `masaha_test` (the API tests').
- The machine has little free memory. Heavy commands (`lint`, `typecheck`, a whole test lane, a build) must go one at a
  time, through the grant script: `node /c/dev/masaha/workspace/WORKER_A/FINAL/scripts/heavy.mjs lead <command>` —
  it waits until 4 GB are free, then runs the command. It may wait many minutes. That is normal.

## 1. The rules you must never break

- **Never** merge. **Never** push to `main`. **Never** force-push anything except `feat/final` with
  `--force-with-lease`. **Never** create an Issue. **Never** delete a remote branch.
- **Never** `git checkout -- <file>`, `git stash`, `git reset --hard`, `git add -A`, `git add .`.
- **Never** change a test, a timeout or a check to make it pass. **Never** skip a test.
- **Never** change data in a database except the steps here name. **Never** run `db:reset` or `db:seed`.
- **Never** touch `C:\dev\masaha\app-b`, databases named `masaha_b_*`, or port 3321 (another worker's).
- **Never** print a password or a token. Passwords are read by the scripts from `apps/api/.env`; do not open it.
- **No tool attribution**: no `Co-Authored-By`, no "generated with" in any commit, PR, or comment.
- Do not change application code, and make no commit: this file asks for none (`prnum.sh` rewrites the placeholder itself).

## 2. Check the starting state

```bash
cd /c/dev/masaha/app
git status --short          # must print nothing
git branch --show-current   # must print feat/final
git log --oneline -1        # must print f4dcc6dd docs: close the findings v1 resolves
git rev-list --count origin/main..HEAD   # must print 124
docker ps --format '{{.Names}} {{.Status}}'   # must show masaha-postgres-1 Up (healthy)
```

If Docker is not running: in PowerShell run `Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"`,
wait 1–2 minutes, then `docker start masaha-postgres-1`. If the state differs in any other way: stop and report.

Also remove leftover grant slots if any (they are empty folders):
`rmdir /c/dev/masaha/workspace/WORKER_A/FINAL/scripts/heavy-slot-* 2>/dev/null`.

## 3. Finish the local verification

Almost everything is already green on this branch (file `scripts\lead\final\summary.txt`): install, shared build,
lint, typecheck, check:classes, check:links, check:conflicts, unit tests (shared 280, api 912, web 1172), the whole
component lane (339 files, 2006 tests), the production build, check:build, the design checks. **Two steps remain:**

**3a. Formatting** (one file was fixed after that run):

```bash
cd /c/dev/masaha/app
npm run format:check
```

Expected last line: `All matched files use Prettier code style!`. If it names files: stop and report them.

**3b. The whole API test lane.** It did not run last time: its workers could not start (Windows error 0xC0000142 —
the machine was out of resources). Close other programs if you can, then:

```bash
cd /c/dev/masaha/app
npm run build -w @masaha/shared
(cd apps/api && npx prisma generate)
node /c/dev/masaha/workspace/WORKER_A/FINAL/scripts/heavy.mjs lead npm run test:api -w @masaha/api > /c/dev/masaha/workspace/WORKER_A/FINAL/scripts/lead/final/api2.txt 2>&1
grep -E "Test Files|Tests " /c/dev/masaha/workspace/WORKER_A/FINAL/scripts/lead/final/api2.txt
```

It takes 20–30 minutes. **Do not give it a short time limit.** Expected: `Test Files 120 passed (120)` and about
`Tests 1374 passed (1374)`.

- If it again shows `Worker exited unexpectedly`: wait, then run it once more. If it fails that way again, run it in
  parts, each through the grant: `npm run test:api -w @masaha/api -- src/modules` then `… -- src/shared src/db test`.
  Write every result line in the report.
- If one or two tests fail with "Test timed out": run **only that file** again
  (`npm run test:api -w @masaha/api -- <the file path>`). If it passes alone, write both results in the report (a timing
  miss on a busy machine). If it fails alone too: stop and report the test's name and its error lines.
- Any other failure: stop and report it with its error lines.

**3c. The first download of `main`, for the comparison.** Optional; skip it if memory is short, and say so. In a new
folder: `git -C /c/dev/masaha/app worktree add /c/dev/masaha/app-base origin/main`, then in it `npm ci`, `npm run build
-w @masaha/shared`, and `NODE_ENV=production node /c/dev/masaha/workspace/WORKER_A/FINAL/scripts/heavy.mjs lead npm run
build -w @masaha/web`, then `node /c/dev/masaha/workspace/WORKER_A/FINAL/scripts/firstDownload.mjs
/c/dev/masaha/app-base/apps/web/dist | grep total`. The head's figure is already measured: **1,158,388 bytes, 7 chunks**
(`scripts\firstDownload-head.txt`). Afterwards: `git -C /c/dev/masaha/app worktree remove --force /c/dev/masaha/app-base`.

Write all results under **## The final verification** in the report.

## 4. The real run (the app in a browser)

**4a. Put the two new migrations on the development database** (this is a named write the plan allows):

```bash
cd /c/dev/masaha/app/apps/api
npx prisma migrate deploy      # must end "All migrations have been successfully applied." (2 applied)
npx prisma generate
```

**4b. Start the two servers**, each in its own background terminal (they keep running):

```bash
cd /c/dev/masaha/app && npm run dev -w @masaha/api      # wait for "listening" on 3320
cd /c/dev/masaha/app && npm run dev                     # wait for the web on http://localhost:5320
```

Then **tell the owner the servers are open** (he asked to look at the screens): the site at `http://localhost:5320`,
the demo owner `demo-owner@example.com`, reception `demo-reception@example.com`, and the admin (the seed's admin); he
knows the passwords. Ask him to only look, not save changes, until you finish 4c.

**4c. Run the tour** (reads only; it writes nothing). It visits every screen as guest, owner, reception and admin,
checks the expected words, logs PASS/FAIL, and saves screenshots to `C:\dev\masaha\workspace\WORKER_A\FINAL\shots\tour\`:

```bash
cd /c/dev/masaha/workspace/WORKER_A/FINAL/scripts
node tour.mjs guest
node tour.mjs owner
node tour.mjs reception
node tour.mjs admin
grep -E "PASS|FAIL|TOTAL|PAGE ERRORS|5xx: [1-9]" tour-log.txt | tail -80
```

(The `user` role is skipped unless `RUN_USER_EMAIL` and `RUN_USER_PASSWORD` are set; leave it skipped.)

- Write every `FAIL` line in the report. **Do not change code for it.** Open that screen's screenshot (the file name is
  role + path + language + width) and describe in the report what you see.
- A `FAIL` because a page loaded slowly (the text simply missing): run that role once more and compare.
- The screen sizes 390 / 768 / 1440 and the dark theme are in the screenshots for the owner to review.

**4d. Stop the servers** by their process ids and check the ports are free (PowerShell):

```powershell
Get-NetTCPConnection -LocalPort 3320,5320 -State Listen -ErrorAction SilentlyContinue | Select-Object LocalPort, OwningProcess
```

Stop each `OwningProcess` with `Stop-Process -Id <id>`; also stop the `tsx watch` and `pino-pretty` node processes the
API started (look for them with `Get-CimInstance Win32_Process -Filter "Name='node.exe'"` and their command lines in
`C:\dev\masaha\app`). Run the port check again: it must print nothing. `git -C /c/dev/masaha/app status --short` must
print nothing.

Write under **## The real run**: the date, M1/M2 applied to `masaha_dev`, the PASS/FAIL totals per role, each FAIL, the
writes (only the migration; the tour writes nothing), and that the plan's write cases (R1, R11, R12, R19–R24, R26,
R30, R32–R35, R38) were **not performed** in this run, with the reason: the run was handed to another agent to keep
within the session's limits; each of those behaviours is proven by its component or API test (name the test file
areas: desk, finance, audit, platform-settings, space-links, lookups, users).

## 5. The PR

**5a. The PR number.** The documents hold the placeholder `#PRNUM`. Find the next number:

```bash
gh api "repos/Basel-Ghonaim/masaha/issues?state=all&per_page=1" --jq '.[0].number'
```

Add 1. Call it N. Then (this rewrites only the placeholder, in every commit, and in `scripts\pr-body.md`):

```bash
bash /c/dev/masaha/workspace/WORKER_A/FINAL/scripts/prnum.sh N
```

It must print `PRNUM OK #N <new head>`. If it prints `PRNUM STOP: …`: stop and report the line (a backup branch
`backup/final-pre-prnum` holds the old head).

**5b. Fill the PR description** `scripts\pr-body.md`: replace the two `<!-- … -->` comments and the `<…>` marks with
the results of steps 3 and 4 (copy the lines from the report). Replace `<HEAD>` with the head's short sha.

**5c. Push and open the PR:**

```bash
cd /c/dev/masaha/app
git push -u origin feat/final
gh pr create --base main --head feat/final --assignee @me --label feat --label area:web --label area:api --label area:docs --title "feat: complete every screen and close the findings" --body-file /c/dev/masaha/workspace/WORKER_A/FINAL/scripts/pr-body.md
```

Check the PR's number equals N (`gh pr view --json number --jq .number`). If it differs (someone opened another
issue or PR meanwhile), the documents name the wrong number: **stop and report it to the owner**; do not rewrite or
force-push without his word.

## 6. CI

```bash
gh pr checks <N> --watch --interval 60
```

Wait until every check is done. Then `gh pr view <N> --json mergeStateStatus --jq .mergeStateStatus` should print
`CLEAN`.

- All green and CLEAN: go to step 7.
- A check red: open its log (`gh run view <run-id> --log-failed | tail -80`). If it is a test that timed out (a timing
  miss), re-run the failed job once: `gh run rerun <run-id> --failed`. Any other red: **stop**, write the failing
  check's name and its error lines in the report, and tell the owner. Do not try to fix code.

## 7. Finish the report and clean up

In `4_REPORT_LEAD.md`, under **## Push, the PR, CI**: N, the head sha, the files count (`git diff --stat
origin/main...HEAD | tail -1`), each CI check and its result, CLEAN or not.

Clean up (each only after the PR is open):
- drop the lane test databases (named writes the run allows):
  `docker exec masaha-postgres-1 psql -U masaha -d masaha_dev -c "DROP DATABASE masaha_a_lane_a1_test"` — and the same
  for `masaha_a_lane_a2_test` and `masaha_a_lane_a2_dev`;
- delete the local lane branches: `git branch -D lane/a1 lane/a2 lane/l lane/t lane/w1 lane/w2 lane/w3 lane/w4 lane/u10`;
- keep the `backup/final-*` branches (the owner removes them after the merge); list them in the report under
  **## Leftovers** (`git branch --list 'backup/final-*'`).

Under **## Decisions taken without the owner**, write one line per decision you took (if any), and copy the lead's
list from `scripts\pr-body.md`'s section of the same name.

## 8. Your final reply to the owner (in Arabic, short)

```
الحالة: جاهز للمراجعة | غير مكتمل (اذكر السبب)
الـ PR: #N · الـ head · CI أخضر/أحمر · CLEAN أو لا
التحقق المحلي: سطر لكل أمر ونتيجته
التشغيل الحقيقي: مجموع PASS/FAIL لكل دور، وكل FAIL
ما لم يُنفَّذ ولماذا
قواعد البيانات المحذوفة، والفروع الباقية
التقرير: C:\dev\masaha\workspace\WORKER_A\FINAL\4_REPORT_LEAD.md
```

If anything in this file does not match what you see: stop, write what you saw in the report, and ask the owner.
